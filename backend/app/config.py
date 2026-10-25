"""Настройки платформы. Значения берутся из переменных окружения или файла .env.

Пример всех параметров лежит в .env.example в корне репозитория.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    app_env: str = "development"

    # Две раздельные БД (п. 4.8.1 ТЗ): учётные записи и аналитика без идентификаторов.
    identity_database_url: str = "postgresql://interviewer:interviewer@localhost:5432/identity"
    analytics_database_url: str = "postgresql://interviewer:interviewer@localhost:5432/analytics"
    redis_url: str = "redis://localhost:6379/0"

    # Какую модель использовать: "gigachat", "claude_code" (подписка Claude,
    # только разработка) или "fake" (заглушка для тестов).
    llm_provider: str = "gigachat"

    gigachat_credentials: str = ""
    gigachat_scope: str = "GIGACHAT_API_PERS"
    gigachat_model: str = "GigaChat"
    # GigaChat использует сертификат Минцифры. Если он не установлен в системе,
    # на время разработки можно поставить false, в эксплуатации — только true.
    gigachat_verify_ssl: bool = True

    # Модель в Claude Code, например "sonnet" или "opus". Пусто — по умолчанию.
    claude_code_model: str = ""

    # Порог анонимности k по умолчанию (п. 4.1.1 ТЗ).
    default_k_threshold: int = 5


@lru_cache
def get_settings() -> Settings:
    return Settings()
