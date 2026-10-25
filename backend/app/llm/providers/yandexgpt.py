"""YandexGPT через Yandex AI Studio.

Если структурированный вывод недоступен, просит JSON в тексте и проверяет его через
app.llm.json_utils.
"""

from app.config import Settings
from app.llm.base import LLMProvider, LLMRequest, LLMResponse, T


class YandexGPTProvider(LLMProvider):
    name = "yandexgpt"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def complete_json(self, request: LLMRequest, schema: type[T]) -> LLMResponse[T]:
        raise NotImplementedError("YandexGPTProvider ещё не реализован (этап 3.2 ТЗ)")

    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("YandexGPTProvider ещё не реализован (этап 3.2 ТЗ)")
