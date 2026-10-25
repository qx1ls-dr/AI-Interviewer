import pytest

from app.privacy.regex_redactor import redact


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("пишите на ivan.petrov@mail.ru", "пишите на [EMAIL]"),
        ("пишите на a@b.ru.", "пишите на [EMAIL]."),
        ("мой номер +7 (921) 123-45-67", "мой номер [ТЕЛЕФОН]"),
        ("звоните 89211234567", "звоните [ТЕЛЕФОН]"),
        ("звоните 9211234567", "звоните [ТЕЛЕФОН]"),
        ("я из группы 4618", "я из [ГРУППА]"),
        ("гр. 4618К", "[ГРУППА]"),
        ("страница vk.com/id123, пишите", "страница [ССЫЛКА], пишите"),
        ("см. https://example.com/a.", "см. [ССЫЛКА]."),
        ("мой ник @ivan_petrov", "мой ник [НИК]"),
    ],
)
def test_redacts_direct_identifiers(text: str, expected: str) -> None:
    assert redact(text)[0] == expected


@pytest.mark.parametrize(
    "text",
    [
        "лекции интересные, но задания приходят поздно",
        "в 2026 году стало лучше",
        "набрал 1500 баллов",
        "дедлайн 12.10.2025",
        "год 2026г",
        "вариант 2021/1234",
    ],
)
def test_keeps_plain_text(text: str) -> None:
    assert redact(text) == (text, [])


def test_known_groups_without_keyword() -> None:
    assert redact("мы с 4618 и 4619 сдавали вместе", known_groups=["4618"])[0] == (
        "мы с [ГРУППА] и 4619 сдавали вместе"
    )
