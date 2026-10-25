"""Модуль GigaChat API (Сбер). Реализация на этапе 3.2 ТЗ."""

from app.llm.base import LLMProvider, Message, T


class GigaChatProvider(LLMProvider):
    def __init__(self, credentials: str) -> None:
        self.credentials = credentials

    async def complete_json(self, system: str, messages: list[Message], schema: type[T]) -> T:
        raise NotImplementedError("GigaChatProvider ещё не написан")
