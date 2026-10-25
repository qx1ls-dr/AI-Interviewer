"""Единый интерфейс обращения к LLM (п. 4.5.2 ТЗ).

Остальной код платформы работает только с LLMProvider и не знает, какая модель
стоит за ним. Чтобы подключить новую модель, достаточно написать ещё один
класс-наследник в папке providers/ и реализовать в нём метод _ask.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.llm.json_utils import parse_as

T = TypeVar("T", bound=BaseModel)

# Сколько раз переспрашиваем модель, если она вернула JSON не по схеме (п. 4.1.2 ТЗ).
MAX_RETRIES = 2


@dataclass
class Message:
    role: str  # "user" или "assistant"
    content: str


class LLMProvider(ABC):
    async def complete_json(self, system: str, messages: list[Message], schema: type[T]) -> T:
        """Отправить диалог модели и получить ответ в виде объекта Pydantic-схемы."""
        for attempt in range(MAX_RETRIES + 1):
            text = await self._ask(system, messages, schema)
            try:
                return parse_as(text, schema)
            except (ValueError, ValidationError):
                if attempt == MAX_RETRIES:
                    raise
        raise AssertionError("недостижимо")

    @abstractmethod
    async def _ask(self, system: str, messages: list[Message], schema: type[BaseModel]) -> str:
        """Один запрос к модели. Возвращает текст ответа, в котором должен быть JSON."""
