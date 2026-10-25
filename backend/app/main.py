"""Точка входа FastAPI-приложения."""

from fastapi import FastAPI

from app import __version__
from app.api.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI-интервьюер",
        version=__version__,
        description="Платформа динамических опросов с AI-интервьюером",
    )
    app.include_router(health_router, prefix="/api")
    return app


app = create_app()
