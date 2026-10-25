"""Выбор модуля LLM по настройкам, в том числе отдельно для каждой задачи."""

from app.config import LLMTask, ProviderName, Settings, get_settings
from app.llm.base import LLMProvider


def build_provider(name: ProviderName, settings: Settings) -> LLMProvider:
    # Импорты внутри, чтобы не тянуть SDK всех моделей сразу.
    match name:
        case ProviderName.CLAUDE:
            from app.llm.providers.claude import ClaudeProvider

            return ClaudeProvider(settings)
        case ProviderName.GIGACHAT:
            from app.llm.providers.gigachat import GigaChatProvider

            return GigaChatProvider(settings)
        case ProviderName.YANDEXGPT:
            from app.llm.providers.yandexgpt import YandexGPTProvider

            return YandexGPTProvider(settings)
        case ProviderName.MCP_DEV:
            if not settings.dev_mode:
                raise RuntimeError("McpDevProvider доступен только при DEV_MODE=true")
            from app.llm.providers.mcp_dev import McpDevProvider

            return McpDevProvider(settings)
        case ProviderName.FAKE:
            from app.llm.providers.fake import FakeProvider

            return FakeProvider()
    raise ValueError(f"Неизвестный провайдер: {name}")


def get_provider(task: LLMTask, settings: Settings | None = None) -> LLMProvider:
    settings = settings or get_settings()
    return build_provider(settings.provider_for(task), settings)
