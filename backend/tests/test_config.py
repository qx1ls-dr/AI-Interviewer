import pytest
from pydantic import ValidationError

from app.config import LLMTask, ProviderName, Settings


def test_pii_defaults_to_russian_model() -> None:
    assert Settings().provider_for(LLMTask.PII) == ProviderName.GIGACHAT


def test_pii_cannot_go_to_claude() -> None:
    with pytest.raises(ValidationError):
        Settings(llm_task_providers={LLMTask.PII: ProviderName.CLAUDE})
    with pytest.raises(ValidationError):
        Settings(llm_task_providers={})  # pii упадёт на провайдера по умолчанию, т.е. Claude


def test_dev_mode_forbidden_in_production() -> None:
    with pytest.raises(ValidationError):
        Settings(app_env="production", dev_mode=True)


def test_empty_env_values_are_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    monkeypatch.setenv("YANDEX_FOLDER_ID", "")
    settings = Settings()
    assert settings.anthropic_api_key is None
    assert settings.yandex_folder_id is None


def test_task_providers_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_TASK_PROVIDERS", '{"pii": "yandexgpt", "analysis": "gigachat"}')
    settings = Settings()
    assert settings.provider_for(LLMTask.PII) == ProviderName.YANDEXGPT
    assert settings.provider_for(LLMTask.INTERVIEW) == ProviderName.CLAUDE
