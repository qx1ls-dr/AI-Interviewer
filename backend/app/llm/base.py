"""Единый интерфейс обращения к LLM (п. 4.5.2 ТЗ).

Весь остальной код платформы работает только с LLMProvider и не знает,
какая модель стоит за ним. Конкретная модель выбирается в настройках.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

Role = Literal["user", "assistant"]
T = TypeVar("T", bound=BaseModel)


@dataclass(frozen=True)
class Message:
    role: Role
    content: str


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class LLMRequest:
    """Запрос к модели. Тексты в messages уже должны быть обезличены."""

    system: str
    messages: list[Message]
    max_tokens: int = 1024
    temperature: float | None = None
    # Можно ли закэшировать системный промпт (prompt caching у Claude).
    cache_system: bool = False
    # Версия промпта, чтобы связать ответ с файлом из prompts/.
    prompt_id: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class LLMResponse(Generic[T]):
    data: T
    raw_text: str
    usage: Usage


class LLMError(Exception):
    """Ошибка обращения к модели."""


class LLMSchemaError(LLMError):
    """Модель вернула ответ, не прошедший проверку JSON-схемы."""


class LLMProvider(ABC):
    """Модуль конкретной модели: ClaudeProvider, GigaChatProvider и т.д."""

    name: str

    @abstractmethod
    async def complete_json(self, request: LLMRequest, schema: type[T]) -> LLMResponse[T]:
        """Получить ответ, строго соответствующий Pydantic-схеме.

        Если модель не умеет структурированный вывод, модуль просит JSON
        в тексте и проверяет его сам (см. app.llm.json_utils).
        """

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Векторные представления текстов."""

    @property
    def supports_streaming(self) -> bool:
        return False
