"""Извлечение и проверка JSON из текстового ответа модели.

Используется модулями, у которых нет структурированного вывода по схеме,
и как общая проверка для всех ответов (п. 4.1.2 ТЗ).
"""

import json
import re
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.llm.errors import LLMSchemaError

T = TypeVar("T", bound=BaseModel)

_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def extract_json(text: str) -> str:
    """Достаёт JSON-объект из ответа: из блока ```json или по первой/последней скобке."""
    match = _FENCE_RE.search(text)
    if match:
        return match.group(1).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise LLMSchemaError("В ответе модели нет JSON-объекта")
    return text[start : end + 1]


def parse_as(text: str, schema: type[T]) -> T:
    try:
        return schema.model_validate(json.loads(extract_json(text)))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise LLMSchemaError(f"Ответ не соответствует схеме {schema.__name__}: {exc}") from exc


def schema_instruction(schema: type[BaseModel]) -> str:
    """Текст-подсказка для моделей без структурированного вывода."""
    return "Ответь только JSON-объектом без пояснений, строго по этой JSON-схеме:\n" + json.dumps(
        schema.model_json_schema(), ensure_ascii=False
    )
