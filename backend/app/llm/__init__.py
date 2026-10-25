from app.config import get_settings
from app.llm.base import LLMProvider, Message


def get_provider(name: str | None = None) -> LLMProvider:
    """Создаёт модуль модели. По умолчанию берётся настройка LLM_PROVIDER."""
    settings = get_settings()
    name = name or settings.llm_provider
    if name == "gigachat":
        from app.llm.providers.gigachat import GigaChatProvider

        return GigaChatProvider(
            credentials=settings.gigachat_credentials,
            scope=settings.gigachat_scope,
            model=settings.gigachat_model,
            verify_ssl=settings.gigachat_verify_ssl,
        )
    if name == "claude_code":
        # Подписка Claude только для разработки на синтетических данных (п. 4.5.3 ТЗ).
        if settings.app_env == "production":
            raise RuntimeError("claude_code нельзя использовать при APP_ENV=production")
        from app.llm.providers.claude_code import ClaudeCodeProvider

        return ClaudeCodeProvider(model=settings.claude_code_model)
    if name == "fake":
        from app.llm.providers.fake import FakeProvider

        return FakeProvider()
    raise ValueError(f"Неизвестная модель: {name}")


__all__ = ["LLMProvider", "Message", "get_provider"]
