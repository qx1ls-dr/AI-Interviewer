from app.config import get_settings
from app.llm.base import LLMProvider, Message


def get_provider() -> LLMProvider:
    """Создаёт модуль модели, указанной в настройке LLM_PROVIDER."""
    settings = get_settings()
    if settings.llm_provider == "gigachat":
        from app.llm.providers.gigachat import GigaChatProvider

        return GigaChatProvider(settings.gigachat_credentials)
    if settings.llm_provider == "fake":
        from app.llm.providers.fake import FakeProvider

        return FakeProvider()
    raise ValueError(f"Неизвестная модель: {settings.llm_provider}")


__all__ = ["LLMProvider", "Message", "get_provider"]
