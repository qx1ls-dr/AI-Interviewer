"""Модуль GigaChat API (Сбер) через официальную библиотеку gigachat.

Ключ авторизации берётся в личном кабинете developers.sber.ru и кладётся
в .env как GIGACHAT_CREDENTIALS. Бесплатный тариф: GIGACHAT_SCOPE=GIGACHAT_API_PERS.
"""

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from pydantic import BaseModel

from app.llm.base import LLMProvider, Message
from app.llm.json_utils import schema_instruction


class GigaChatProvider(LLMProvider):
    def __init__(self, credentials: str, scope: str, model: str, verify_ssl: bool) -> None:
        if not credentials:
            raise ValueError("Не задан GIGACHAT_CREDENTIALS в .env")
        self.client = GigaChat(
            credentials=credentials, scope=scope, model=model, verify_ssl_certs=verify_ssl
        )

    async def _ask(self, system: str, messages: list[Message], schema: type[BaseModel]) -> str:
        chat = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM, content=system + "\n\n" + schema_instruction(schema)
                ),
                *(Messages(role=MessagesRole(m.role), content=m.content) for m in messages),
            ]
        )
        response = await self.client.achat(chat)
        return response.choices[0].message.content
