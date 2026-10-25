"""Заглушка для тестов: возвращает заранее заданные ответы без обращения к сети."""

import json

from pydantic import BaseModel

from app.llm.base import LLMProvider, LLMRequest, Usage


class FakeProvider(LLMProvider):
    name = "fake"

    def __init__(self, replies: list[dict | str] | None = None) -> None:
        # Ответ-строка отдаётся как есть: так можно проверить невалидный JSON.
        self.replies = list(replies or [])
        self.requests: list[LLMRequest] = []

    async def _complete_raw(
        self, request: LLMRequest, schema: type[BaseModel]
    ) -> tuple[str, Usage]:
        self.requests.append(request)
        payload = self.replies.pop(0) if self.replies else {}
        raw = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
        return raw, Usage()

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(t)), 0.0, 1.0] for t in texts]
