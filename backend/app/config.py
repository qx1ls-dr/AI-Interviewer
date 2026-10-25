"""Настройки платформы. Значения берутся из переменных окружения или файла .env.

Пример всех параметров лежит в .env.example в корне репозитория.
"""

from enum import StrEnum
from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProviderName(StrEnum):
    """Доступные модули LLM (п. 4.5.2 ТЗ)."""

    CLAUDE = "claude"
    GIGACHAT = "gigachat"
    YANDEXGPT = "yandexgpt"
    MCP_DEV = "mcp_dev"  # только режим разработки, п. 4.5.3 ТЗ
    FAKE = "fake"  # детерминированная заглушка для тестов


class LLMTask(StrEnum):
    """Задачи, для которых модель выбирается отдельно."""

    INTERVIEW = "interview"
    MODERATION = "moderation"
    PII = "pii"
    ANALYSIS = "analysis"
    REPORT = "report"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    app_env: str = "development"
    # Режим разработки с MCP и подпиской Claude. В эксплуатации обязан быть false.
    dev_mode: bool = False

    # Две раздельные БД (п. 4.8.1 ТЗ): учётные записи и аналитика без идентификаторов.
    identity_database_url: str = (
        "postgresql+psycopg://interviewer:interviewer@localhost:5432/identity"
    )
    analytics_database_url: str = (
        "postgresql+psycopg://interviewer:interviewer@localhost:5432/analytics"
    )
    redis_url: str = "redis://localhost:6379/0"

    # Провайдер по умолчанию и переопределения по задачам.
    llm_default_provider: ProviderName = ProviderName.CLAUDE
    llm_task_providers: dict[LLMTask, ProviderName] = Field(default_factory=dict)

    anthropic_api_key: SecretStr | None = None
    claude_model: str = "claude-sonnet-5-5"

    gigachat_credentials: SecretStr | None = None
    gigachat_scope: str = "GIGACHAT_API_PERS"
    gigachat_model: str = "GigaChat-2-Max"

    yandex_api_key: SecretStr | None = None
    yandex_folder_id: str | None = None
    yandex_model: str = "yandexgpt"

    # Лимит токенов на один опрос (п. 4.5.2 ТЗ), 0 — без лимита.
    llm_token_limit_per_survey: int = 0
    # Повторы при невалидном JSON от модели (п. 4.1.2 ТЗ).
    llm_json_max_retries: int = 2

    # Порог анонимности k по умолчанию (п. 4.1.1 ТЗ).
    default_k_threshold: int = 5

    def provider_for(self, task: LLMTask) -> ProviderName:
        return self.llm_task_providers.get(task, self.llm_default_provider)


@lru_cache
def get_settings() -> Settings:
    return Settings()
