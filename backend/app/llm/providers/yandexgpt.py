"""YandexGPT через Yandex AI Studio.

Если структурированный вывод недоступен, просит JSON в тексте (schema_instruction) и проверяет
его через общий цикл в LLMProvider.
"""

from pydantic import BaseModel

from app.config import Settings
from app.llm.base import LLMProvider, LLMRequest, Usage


class YandexGPTProvider(LLMProvider):
    name = "yandexgpt"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.max_retries = settings.llm_json_max_retries

    async def _complete_raw(
        self, request: LLMRequest, schema: type[BaseModel]
    ) -> tuple[str, Usage]:
        raise NotImplementedError("YandexGPTProvider ещё не реализован (этап 3.2 ТЗ)")

    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("YandexGPTProvider ещё не реализован (этап 3.2 ТЗ)")
