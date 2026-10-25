"""Единый интерфейс обращения к LLM (п. 4.5.2 ТЗ).

Остальной код платформы работает только с LLMProvider и не знает, какая модель
стоит за ним. Чтобы подключить новую модель (Claude, YandexGPT), достаточно
написать ещё один класс-наследник в папке providers/.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@dataclass
class Message:
    role: str  # "user" или "assistant"
    content: str


class LLMProvider(ABC):
    @abstractmethod
    async def complete_json(self, system: str, messages: list[Message], schema: type[T]) -> T:
        """Отправить диалог модели и получить ответ в виде объекта Pydantic-схемы."""
