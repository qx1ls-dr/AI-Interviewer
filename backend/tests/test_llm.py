from pydantic import BaseModel

from app.llm import Message
from app.llm.json_utils import parse_as
from app.llm.providers.fake import FakeProvider


class Reply(BaseModel):
    reply: str
    next_action: str


def test_parse_json_from_text() -> None:
    text = 'Вот ответ:\n```json\n{"reply": "Расскажите подробнее?", "next_action": "probe"}\n```'
    assert parse_as(text, Reply).next_action == "probe"


async def test_fake_provider() -> None:
    provider = FakeProvider(replies=[{"reply": "Что именно?", "next_action": "probe"}])
    answer = await provider.complete_json("system", [Message("user", "всё плохо")], Reply)
    assert answer.reply == "Что именно?"
