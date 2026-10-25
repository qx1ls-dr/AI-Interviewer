from fastapi import APIRouter

from app import __version__
from app.config import get_settings

router = APIRouter(tags=["service"])


@router.get("/health")
def health() -> dict[str, str | bool]:
    settings = get_settings()
    return {"status": "ok", "version": __version__, "dev_mode": settings.dev_mode}
