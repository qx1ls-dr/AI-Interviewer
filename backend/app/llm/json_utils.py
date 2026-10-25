"""Разбор JSON из текстового ответа модели (п. 4.1.2 ТЗ)."""

import json
import re
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def parse_as(text: str, schema: type[T]) -> T:
    """Достаёт JSON из ответа (в том числе из блока ```json) и проверяет его по схеме.

    Если JSON нет или он не подходит под схему, будет исключение ValueError
    или ValidationError.
    """
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    raw = match.group(1) if match else text[text.find("{") : text.rfind("}") + 1]
    return schema.model_validate(json.loads(raw))


def schema_instruction(schema: type[BaseModel]) -> str:
    """Подсказка для модели, которая не умеет отвечать строго по схеме."""
    schema_json = json.dumps(schema.model_json_schema(), ensure_ascii=False)
    return f"Ответь только JSON-объектом без пояснений, строго по этой JSON-схеме:\n{schema_json}"


def dialog_as_text(messages: list) -> str:
    """Склеивает историю диалога в один текст (для моделей, которым передаём одну строку)."""
    names = {"user": "Респондент", "assistant": "Интервьюер"}
    return "\n\n".join(f"{names.get(m.role, m.role)}: {m.content}" for m in messages)
