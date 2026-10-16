from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import router as api_router
from app.config import settings
from app.graph import repository
from app.ui.router import router as ui_router

BASE_DIR = Path(__file__).parent
app = FastAPI(title="Study planner")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(ui_router)
app.include_router(api_router)


@app.on_event("startup")
def validate_security_settings():
    if settings.app_env == "production" and settings.auth_mode != "firebase":
        raise RuntimeError("Production requires AUTH_MODE=firebase")
    if settings.app_env == "production" and settings.session_secret == "local-only-change-me":
        raise RuntimeError("Set a strong SESSION_SECRET before production deployment")


@app.get("/health")
def health():
    return {"app": "ok", "falkordb": repository.health()}
