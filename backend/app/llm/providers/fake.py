"""Заглушка для тестов: отдаёт заранее заданные ответы, в сеть не ходит."""

import json

from pydantic import BaseModel

from app.llm.base import LLMProvider, Message


class FakeProvider(LLMProvider):
    def __init__(self, replies: list[dict | str] | None = None) -> None:
        # Ответ-строка отдаётся как есть: так можно проверить невалидный JSON.
        self.replies = list(replies or [])
        self.calls = 0

    async def _ask(self, system: str, messages: list[Message], schema: type[BaseModel]) -> str:
        self.calls += 1
        reply = self.replies.pop(0) if self.replies else {}
        return reply if isinstance(reply, str) else json.dumps(reply, ensure_ascii=False)
