import json

import pytest
from pydantic import BaseModel, ValidationError

from app.config import get_settings
from app.llm import Message, get_provider
from app.llm.json_utils import parse_as
from app.llm.providers.claude_code import ClaudeCodeProvider
from app.llm.providers.fake import FakeProvider


class Reply(BaseModel):
    reply: str
    next_action: str


def test_parse_json_from_text() -> None:
    text = 'Вот ответ:\n```json\n{"reply": "Расскажите подробнее?", "next_action": "probe"}\n```'
    assert parse_as(text, Reply).next_action == "probe"


async def test_fake_provider() -> None:
    provider = FakeProvider(replies=[{"reply": "Что именно?", "next_action": "probe"}])
    answer = await provider.complete_json("system", [Message("user", "всё плохо")], Reply)
    assert answer.reply == "Что именно?"


async def test_retries_on_bad_json() -> None:
    provider = FakeProvider(replies=["не JSON", {"reply": "Почему?", "next_action": "probe"}])
    answer = await provider.complete_json("system", [Message("user", "так себе")], Reply)
    assert answer.reply == "Почему?"
    assert provider.calls == 2


async def test_gives_up_after_two_retries() -> None:
    provider = FakeProvider(replies=["нет", "нет", "нет", {"reply": "x", "next_action": "end"}])
    with pytest.raises((ValueError, ValidationError)):
        await provider.complete_json("system", [Message("user", "привет")], Reply)
    assert provider.calls == 3  # первый запрос и два повтора


class FakeProcess:
    """Подмена запущенного процесса claude, чтобы тест не ходил в сеть."""

    returncode = 0

    def __init__(self, stdout: dict) -> None:
        self.stdout = json.dumps(stdout).encode()
        self.stdin = b""

    async def communicate(self, data: bytes) -> tuple[bytes, bytes]:
        self.stdin = data
        return self.stdout, b""


async def test_claude_code_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    started: dict = {}
    process = FakeProcess(
        {"is_error": False, "structured_output": {"reply": "Каких?", "next_action": "probe"}}
    )

    async def fake_exec(*command, **kwargs):
        started["command"] = command
        return process

    monkeypatch.setattr("asyncio.create_subprocess_exec", fake_exec)
    provider = ClaudeCodeProvider()
    answer = await provider.complete_json(
        "Ты интервьюер", [Message("user", "мало примеров")], Reply
    )

    assert answer.reply == "Каких?"
    assert started["command"][:2] == ("claude", "-p")
    assert "--json-schema" in started["command"]
    assert "Респондент: мало примеров" in process.stdin.decode()


def test_claude_code_forbidden_in_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    get_settings.cache_clear()
    with pytest.raises(RuntimeError):
        get_provider("claude_code")
    get_settings.cache_clear()


def test_gigachat_needs_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIGACHAT_CREDENTIALS", "")
    get_settings.cache_clear()
    with pytest.raises(ValueError):
        get_provider("gigachat")
    get_settings.cache_clear()
