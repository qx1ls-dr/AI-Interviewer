"""Заглушка для тестов: возвращает заранее заданные ответы без обращения к сети."""

import json

from app.llm.base import LLMProvider, LLMRequest, LLMResponse, T, Usage
from app.llm.json_utils import parse_as


class FakeProvider(LLMProvider):
    name = "fake"

    def __init__(self, replies: list[dict] | None = None) -> None:
        self.replies = list(replies or [])
        self.requests: list[LLMRequest] = []

    async def complete_json(self, request: LLMRequest, schema: type[T]) -> LLMResponse[T]:
        self.requests.append(request)
        payload = self.replies.pop(0) if self.replies else {}
        raw = json.dumps(payload, ensure_ascii=False)
        return LLMResponse(data=parse_as(raw, schema), raw_text=raw, usage=Usage())

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(t)), 0.0, 1.0] for t in texts]
