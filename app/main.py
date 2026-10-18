from pathlib import Path

from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.templating import Jinja2Templates
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


@app.exception_handler(HTTPException)
async def friendly_http_error(request: Request, exc: HTTPException):
    if exc.status_code == 503 and request.method == 'GET' and not request.url.path.startswith('/api/'):
        return Jinja2Templates(directory=BASE_DIR / 'templates').TemplateResponse(
            request, 'unavailable.html', {'retry_path': request.url.path}, status_code=503)
    return await http_exception_handler(request, exc)


@app.on_event("startup")
def validate_security_settings():
    if settings.profile_store not in ('falkordb', 'firestore'):
        raise RuntimeError('PROFILE_STORE must be falkordb or firestore')
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
