"""Заглушка для тестов: отдаёт заранее заданные ответы, в сеть не ходит."""

import json

from app.llm.base import LLMProvider, Message, T
from app.llm.json_utils import parse_as


class FakeProvider(LLMProvider):
    def __init__(self, replies: list[dict] | None = None) -> None:
        self.replies = list(replies or [])

    async def complete_json(self, system: str, messages: list[Message], schema: type[T]) -> T:
        reply = self.replies.pop(0) if self.replies else {}
        return parse_as(json.dumps(reply, ensure_ascii=False), schema)
