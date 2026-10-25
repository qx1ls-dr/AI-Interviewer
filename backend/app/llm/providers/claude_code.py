"""Модуль Claude по подписке разработчика через Claude Code (п. 4.5.3 ТЗ).

Вызывает установленный у разработчика Claude Code в неинтерактивном режиме
(`claude -p`), поэтому расходуется подписка Claude Pro/Max, а не платный API.

Только для разработки и тестов на синтетических данных: реальные ответы студентов
сюда не отправляем, в эксплуатации (APP_ENV=production) модуль не включается.
Перед первым запуском один раз выполните `claude` в терминале и войдите в аккаунт.
"""

import asyncio
import json
import os

from pydantic import BaseModel

from app.llm.base import LLMProvider, Message
from app.llm.json_utils import dialog_as_text


class ClaudeCodeProvider(LLMProvider):
    def __init__(self, model: str = "", timeout: float = 120) -> None:
        self.model = model
        self.timeout = timeout

    def build_command(self, system: str, schema: type[BaseModel]) -> list[str]:
        command = [
            "claude",
            "-p",  # неинтерактивный режим: один запрос, один ответ
            "--output-format", "json",
            "--json-schema", json.dumps(schema.model_json_schema(), ensure_ascii=False),
            "--system-prompt", system,
            "--tools", "",  # без доступа к файлам и командам: модель только отвечает
            "--no-session-persistence",
        ]  # fmt: skip
        if self.model:
            command += ["--model", self.model]
        return command

    @staticmethod
    def subscription_env() -> dict[str, str]:
        # Если в окружении есть ANTHROPIC_API_KEY, Claude Code возьмёт платный API
        # вместо подписки. Убираем ключ, чтобы гарантированно шла подписка.
        return {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}

    async def _ask(self, system: str, messages: list[Message], schema: type[BaseModel]) -> str:
        process = await asyncio.create_subprocess_exec(
            *self.build_command(system, schema),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=self.subscription_env(),
        )
        # История диалога идёт через stdin, чтобы не упереться в длину командной строки.
        stdout, stderr = await asyncio.wait_for(
            process.communicate(dialog_as_text(messages).encode()), self.timeout
        )
        if process.returncode != 0:
            raise RuntimeError(f"Claude Code завершился с ошибкой: {stderr.decode()[:500]}")
        result = json.loads(stdout)
        if result.get("is_error"):
            raise RuntimeError(f"Claude Code вернул ошибку: {result.get('result')}")
        # С --json-schema готовый объект лежит в structured_output.
        return json.dumps(result.get("structured_output") or result["result"], ensure_ascii=False)
