"""Claude API (Anthropic).

Использует структурированный вывод по JSON-схеме, prompt caching для системного промпта
интервьюера и Message Batches API для анализа. Получает только обезличенные тексты (п. 4.8.1
ТЗ). Эмбеддинги делегирует общему локальному энкодеру.
"""

from pydantic import BaseModel

from app.config import Settings
from app.llm.base import LLMProvider, LLMRequest, Usage


class ClaudeProvider(LLMProvider):
    name = "claude"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.max_retries = settings.llm_json_max_retries

    async def _complete_raw(
        self, request: LLMRequest, schema: type[BaseModel]
    ) -> tuple[str, Usage]:
        raise NotImplementedError("ClaudeProvider ещё не реализован (этап 3.2 ТЗ)")

    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("ClaudeProvider ещё не реализован (этап 3.2 ТЗ)")
