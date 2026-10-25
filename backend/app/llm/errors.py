class LLMError(Exception):
    """Ошибка обращения к модели."""


class LLMSchemaError(LLMError):
    """Модель вернула ответ, не прошедший проверку JSON-схемы."""
