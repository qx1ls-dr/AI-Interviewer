"""Claude API (Anthropic).

Использует структурированный вывод по JSON-схеме, prompt caching для системного промпта
интервьюера и Message Batches API для анализа. Получает только обезличенные тексты (п. 4.8.1
ТЗ).
"""

from app.config import Settings
from app.llm.base import LLMProvider, LLMRequest, LLMResponse, T


class ClaudeProvider(LLMProvider):
    name = "claude"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def complete_json(self, request: LLMRequest, schema: type[T]) -> LLMResponse[T]:
        raise NotImplementedError("ClaudeProvider ещё не реализован (этап 3.2 ТЗ)")

    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("ClaudeProvider ещё не реализован (этап 3.2 ТЗ)")
