"""Режим разработки, п. 4.5.3 ТЗ.

Запросы ставятся в очередь, их выполняет Claude в клиенте разработчика через MCP-сервер
(app.devmode), результат проходит ту же проверку схемы. Только синтетические данные.
"""

from pydantic import BaseModel

from app.config import Settings
from app.llm.base import LLMProvider, LLMRequest, Usage


class McpDevProvider(LLMProvider):
    name = "mcp_dev"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.max_retries = settings.llm_json_max_retries

    async def _complete_raw(
        self, request: LLMRequest, schema: type[BaseModel]
    ) -> tuple[str, Usage]:
        raise NotImplementedError("McpDevProvider ещё не реализован (этап 3.2 ТЗ)")

    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("McpDevProvider ещё не реализован (этап 3.2 ТЗ)")
