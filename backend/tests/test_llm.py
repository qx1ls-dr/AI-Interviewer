import pytest
from pydantic import BaseModel

from app.config import LLMTask, ProviderName, Settings
from app.llm import LLMRequest, LLMSchemaError, Message
from app.llm.json_utils import parse_as
from app.llm.providers.fake import FakeProvider
from app.llm.registry import build_provider, get_provider


class Reply(BaseModel):
    reply: str
    next_action: str


def test_task_specific_provider() -> None:
    settings = Settings(
        llm_default_provider=ProviderName.FAKE,
        llm_task_providers={
            LLMTask.ANALYSIS: ProviderName.GIGACHAT,
            LLMTask.PII: ProviderName.YANDEXGPT,
        },
    )
    assert get_provider(LLMTask.INTERVIEW, settings).name == "fake"
    assert get_provider(LLMTask.ANALYSIS, settings).name == "gigachat"


def test_mcp_dev_requires_dev_mode() -> None:
    with pytest.raises(RuntimeError):
        build_provider(ProviderName.MCP_DEV, Settings(dev_mode=False))
    assert build_provider(ProviderName.MCP_DEV, Settings(dev_mode=True)).name == "mcp_dev"


def test_parse_json_from_text() -> None:
    text = 'Вот ответ:\n```json\n{"reply": "Расскажите подробнее?", "next_action": "probe"}\n```'
    assert parse_as(text, Reply).next_action == "probe"


def test_parse_rejects_invalid() -> None:
    with pytest.raises(LLMSchemaError):
        parse_as('{"reply": "нет поля next_action"}', Reply)


async def test_retries_invalid_json() -> None:
    provider = FakeProvider(replies=["не JSON", {"reply": "Что именно?", "next_action": "probe"}])
    request = LLMRequest(system="s", messages=[Message("user", "всё плохо")])
    response = await provider.complete_json(request, Reply)
    assert response.data.next_action == "probe"
    assert len(provider.requests) == 2


async def test_gives_up_after_max_retries() -> None:
    provider = FakeProvider(replies=["нет", "нет", "нет", {"reply": "x", "next_action": "end"}])
    request = LLMRequest(system="s", messages=[Message("user", "привет")])
    with pytest.raises(LLMSchemaError):
        await provider.complete_json(request, Reply)
    assert len(provider.requests) == 3  # первый запрос и два повтора


def test_parse_json_uppercase_fence() -> None:
    text = '```JSON\n{"reply": "Почему?", "next_action": "probe"}\n```'
    assert parse_as(text, Reply).reply == "Почему?"


async def test_fake_provider() -> None:
    provider = FakeProvider(replies=[{"reply": "Что именно?", "next_action": "probe"}])
    request = LLMRequest(system="s", messages=[Message("user", "всё плохо")])
    response = await provider.complete_json(request, Reply)
    assert response.data.reply == "Что именно?"
