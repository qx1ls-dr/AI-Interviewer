from fastapi import APIRouter

from app import __version__

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Проверка, что сервер запущен."""
    return {"status": "ok", "version": __version__}
