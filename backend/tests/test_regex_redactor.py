import pytest

from app.privacy.regex_redactor import redact


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("пишите на ivan.petrov@mail.ru", "пишите на [EMAIL]"),
        ("мой номер +7 (921) 123-45-67", "мой номер [ТЕЛЕФОН]"),
        ("звоните 89211234567", "звоните [ТЕЛЕФОН]"),
        ("я из группы 4618", "я из [ГРУППА]"),
        ("страница vk.com/id123", "страница [ССЫЛКА]"),
    ],
)
def test_redacts_direct_identifiers(text: str, expected: str) -> None:
    assert redact(text)[0] == expected


def test_keeps_plain_text() -> None:
    text = "лекции интересные, но задания приходят поздно"
    assert redact(text) == (text, [])
