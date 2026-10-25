"""Разбор JSON из текстового ответа модели (п. 4.1.2 ТЗ)."""

import json
import re
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def parse_as(text: str, schema: type[T]) -> T:
    """Достаёт JSON из ответа (в том числе из блока ```json) и проверяет его по схеме.

    Если JSON нет или он не подходит под схему, будет исключение — тогда запрос
    к модели нужно повторить (не больше двух раз).
    """
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    raw = match.group(1) if match else text[text.find("{") : text.rfind("}") + 1]
    return schema.model_validate(json.loads(raw))
