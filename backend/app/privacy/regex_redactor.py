"""Первый шаг обезличивания: прямые идентификаторы по регулярным выражениям.

Следующие шаги (Natasha NER, список запрещённых имён, LLM для косвенных
идентификаторов) добавляются на этапе 3.4 ТЗ.
"""

import re
from dataclasses import dataclass

# Порядок важен: сначала более специфичные шаблоны.
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("ССЫЛКА", re.compile(r"(?:https?://|www\.|(?:vk\.com|t\.me)/)\S+", re.IGNORECASE)),
    (
        "ТЕЛЕФОН",
        re.compile(r"(?<!\d)(?:\+7|8)[\s(-]*\d{3}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?!\d)"),
    ),
    # Номер учебной группы ГУАП: 4 цифры, иногда с буквой, например 4618 или 4618К.
    ("ГРУППА", re.compile(r"(?i)(?<!\d)(?:гр(?:\.|уппа|уппы|уппе)?\s*)?\d{4}[а-яa-z]?(?!\d)")),
]


@dataclass(frozen=True)
class Redaction:
    label: str
    start: int
    end: int


def redact(text: str) -> tuple[str, list[Redaction]]:
    """Заменяет найденные идентификаторы метками вида [ТЕЛЕФОН]."""
    found: list[Redaction] = []
    for label, pattern in PATTERNS:
        for m in pattern.finditer(text):
            if not any(r.start < m.end() and m.start() < r.end for r in found):
                found.append(Redaction(label, m.start(), m.end()))
    found.sort(key=lambda r: r.start)
    out, pos = [], 0
    for r in found:
        out.append(text[pos : r.start])
        out.append(f"[{r.label}]")
        pos = r.end
    out.append(text[pos:])
    return "".join(out), found
