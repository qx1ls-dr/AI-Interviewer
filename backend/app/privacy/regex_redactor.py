"""Первый шаг обезличивания: прямые идентификаторы по регулярным выражениям.

Следующие шаги (Natasha NER, список запрещённых имён, LLM для косвенных
идентификаторов) добавляются на этапе 3.4 ТЗ.
"""

import re
from collections.abc import Iterable
from dataclasses import dataclass

# Пунктуация, которая стоит после ссылки или адреса и не входит в них.
_TRAILING = r"(?<![.,;:!?)\]»\"'])"

# Порядок важен: сначала более специфичные шаблоны.
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    (
        "ССЫЛКА",
        re.compile(r"(?:https?://|www\.|\b(?:vk\.com|t\.me)/)\S+" + _TRAILING, re.IGNORECASE),
    ),
    # Ник в Telegram и т.п.: @ivan_petrov.
    ("НИК", re.compile(r"(?<![\w.])@[A-Za-z][A-Za-z0-9_]{3,31}\b")),
    (
        "ТЕЛЕФОН",
        re.compile(
            r"(?<![\w.])(?:(?:\+7|8)[\s(-]*)?9\d{2}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?![\w.])"
            r"|(?<![\w.])(?:\+7|8)[\s(-]*\d{3}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?![\w.])"
        ),
    ),
    # Номер учебной группы только со словом «группа»/«гр.», чтобы не задевать годы,
    # баллы и прочие 4-значные числа. Номера без слова ловит known_groups в redact().
    (
        "ГРУППА",
        re.compile(
            r"(?i)\b(?:гр\.?|групп[аыеуой]{0,2})\s*№?\s*[a-zа-яё]?\d{3,4}[a-zа-яё]?(?![\w/])"
        ),
    ),
]


@dataclass(frozen=True)
class Redaction:
    label: str
    start: int
    end: int


def _patterns(known_groups: Iterable[str]) -> list[tuple[str, re.Pattern[str]]]:
    groups = sorted({g.strip() for g in known_groups if g.strip()}, key=len, reverse=True)
    if not groups:
        return PATTERNS
    known = re.compile(
        r"(?<![\w./])(?:" + "|".join(map(re.escape, groups)) + r")(?![\w/])", re.IGNORECASE
    )
    return [*PATTERNS, ("ГРУППА", known)]


def redact(text: str, known_groups: Iterable[str] = ()) -> tuple[str, list[Redaction]]:
    """Заменяет найденные идентификаторы метками вида [ТЕЛЕФОН].

    known_groups — номера групп, участвующих в опросе: они заменяются и без слова «группа».
    """
    found: list[Redaction] = []
    for label, pattern in _patterns(known_groups):
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
