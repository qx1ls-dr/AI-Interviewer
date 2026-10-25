"""Режим разработки (п.

4.5.3 ТЗ). Запросы ставятся в очередь, их выполняет Claude в клиенте разработчика через MCP-
сервер (app.devmode), результат проходит ту же проверку схемы. Только синтетические данные.
"""

from app.config import Settings
from app.llm.base import LLMProvider, LLMRequest, LLMResponse, T


class McpDevProvider(LLMProvider):
    name = "mcp_dev"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def complete_json(self, request: LLMRequest, schema: type[T]) -> LLMResponse[T]:
        raise NotImplementedError("McpDevProvider ещё не реализован (этап 3.2 ТЗ)")

    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("McpDevProvider ещё не реализован (этап 3.2 ТЗ)")
