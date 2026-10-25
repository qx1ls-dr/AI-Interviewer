"""Единый интерфейс обращения к LLM (п. 4.5.2 ТЗ).

Весь остальной код платформы работает только с LLMProvider и не знает,
какая модель стоит за ним. Конкретная модель выбирается в настройках.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

from app.llm.errors import LLMError as LLMError  # реэкспорт
from app.llm.errors import LLMSchemaError
from app.llm.json_utils import parse_as

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


class LLMProvider(ABC):
    """Модуль конкретной модели: ClaudeProvider, GigaChatProvider и т.д.

    Наследник реализует только `_complete_raw`. Проверка ответа по схеме
    и повторы при ошибке (не более `max_retries`, п. 4.1.2 ТЗ) общие для всех.
    """

    name: str
    max_retries: int = 2

    async def complete_json(self, request: LLMRequest, schema: type[T]) -> LLMResponse[T]:
        """Получить ответ, строго соответствующий Pydantic-схеме."""
        usage = Usage()
        last_error: LLMSchemaError | None = None
        for _ in range(self.max_retries + 1):
            raw, step_usage = await self._complete_raw(request, schema)
            usage.input_tokens += step_usage.input_tokens
            usage.output_tokens += step_usage.output_tokens
            try:
                data = parse_as(raw, schema)
            except LLMSchemaError as exc:
                last_error = exc
                continue
            return LLMResponse(data=data, raw_text=raw, usage=usage)
        assert last_error is not None
        raise last_error

    @abstractmethod
    async def _complete_raw(
        self, request: LLMRequest, schema: type[BaseModel]
    ) -> tuple[str, Usage]:
        """Один запрос к модели, возвращает текст ответа (ожидается JSON) и расход токенов.

        Модель со структурированным выводом передаёт ей схему напрямую. Модель
        без него добавляет к промпту `schema_instruction(schema)` из json_utils.
        """

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Векторные представления текстов.

        У Claude своего API эмбеддингов нет, поэтому ClaudeProvider будет
        делегировать общему локальному энкодеру (sentence-transformers, п. 4.5.1 ТЗ).
        """

    @property
    def supports_streaming(self) -> bool:
        return False
