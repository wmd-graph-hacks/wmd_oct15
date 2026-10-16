from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import router as api_router
from app.config import settings
from app.graph import repository
from app.ui.agent_router import router as agent_router
from app.ui.router import router as ui_router

BASE_DIR = Path(__file__).parent
app = FastAPI(title="Study planner")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(ui_router)
app.include_router(api_router)
app.include_router(agent_router)


@app.on_event("startup")
def validate_security_settings():
    if settings.app_env == "production" and settings.auth_mode != "firebase":
        raise RuntimeError("Production requires AUTH_MODE=firebase")
    if settings.app_env == "production" and settings.session_secret == "local-only-change-me":
        raise RuntimeError("Set a strong SESSION_SECRET before production deployment")
    _load_curriculum_if_missing()


def _load_curriculum_if_missing() -> None:
    """Load the maths curriculum at start; never block app start if the graph is down (it retries on use)."""
    import logging
    try:
        from app.kg.loader import ensure_loaded
        ensure_loaded()
    except Exception as exc:
        logging.getLogger(__name__).warning("curriculum not loaded at startup (%s)", type(exc).__name__)


@app.get("/health")
def health():
    return {"app": "ok", "falkordb": repository.health()}
