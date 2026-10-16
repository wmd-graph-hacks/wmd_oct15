from dataclasses import dataclass
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

_LLM_CONFIG_PATH = Path(__file__).resolve().parent.parent / "llm_config.json"
try:
    _LLM_CONFIG = json.loads(_LLM_CONFIG_PATH.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    _LLM_CONFIG = {}


def _fallback_models() -> tuple[str, ...]:
    configured = os.getenv("AI_FALLBACK_MODELS")
    if configured is not None:
        return tuple(model.strip() for model in configured.split(",") if model.strip())
    return tuple(_LLM_CONFIG.get("fallback_models", ()))


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    auth_mode: str = os.getenv("AUTH_MODE", "demo")
    session_secret: str = os.getenv("SESSION_SECRET", "local-only-change-me")
    falkordb_host: str = os.getenv("FALKORDB_HOST", "localhost")
    falkordb_port: int = int(os.getenv("FALKORDB_PORT", "6379"))
    graph_name: str = os.getenv("FALKORDB_GRAPH", "study_planner")
    firebase_api_key: str = os.getenv("FIREBASE_API_KEY", "")
    firebase_auth_domain: str = os.getenv("FIREBASE_AUTH_DOMAIN", "")
    firebase_project_id: str = os.getenv("FIREBASE_PROJECT_ID", "")
    firebase_app_id: str = os.getenv("FIREBASE_APP_ID", "")
    firebase_service_account: str = os.getenv("FIREBASE_SERVICE_ACCOUNT", "")
    session_cookie_secure: bool = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    ai_enabled: bool = os.getenv("AI_ENABLED", "false").lower() == "true"
    ai_model: str = os.getenv("AI_MODEL", "") or _LLM_CONFIG.get("primary_model", "")
    ai_fallback_models: tuple[str, ...] = _fallback_models()
    ai_timeout_seconds: float = float(os.getenv("AI_TIMEOUT_SECONDS", str(_LLM_CONFIG.get("timeout_seconds", 8))))
    ai_max_tokens: int = int(os.getenv("AI_MAX_TOKENS", str(_LLM_CONFIG.get("max_tokens", 200))))
    ai_cache_size: int = int(os.getenv("AI_CACHE_SIZE", str(_LLM_CONFIG.get("cache_size", 256))))


settings = Settings()
