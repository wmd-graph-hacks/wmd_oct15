"""Smoke-test Gemini connectivity through LiteLLM using the project's .env."""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

# Import after loading this project's .env so the same model chain as the app
# is used, even when this script is launched from another working directory.
from app.config import settings  # noqa: E402


def _safe_error(exc: Exception) -> str:
    message = str(exc)
    secret = os.getenv("GEMINI_API_KEY", "")
    if secret:
        message = message.replace(secret, "[REDACTED]")
    return f"{type(exc).__name__}: {message[:300]}"


async def check_litellm() -> int:
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY is missing. Add it to the project .env file.")
        return 1

    try:
        from litellm import acompletion
    except ImportError:
        print("ERROR: LiteLLM is not installed. Run: pip install -e '.[llm]'")
        return 1

    models = tuple(dict.fromkeys((settings.ai_model, *settings.ai_fallback_models)))
    if not models or not models[0]:
        print("ERROR: No models configured. Check llm_config.json or AI_MODEL in .env.")
        return 1

    for model in models:
        try:
            response = await acompletion(
                model=model,
                messages=[{"role": "user", "content": "Reply with exactly: LiteLLM is connected."}],
                max_tokens=20,
                timeout=settings.ai_timeout_seconds,
                num_retries=0,
            )
            content = response.choices[0].message.content
            if isinstance(content, str) and content.strip():
                print(f"OK: Gemini responded through LiteLLM using {model}.")
                return 0
            print(f"FAILED: {model} returned an empty response; trying the next model.")
        except Exception as exc:
            print(f"FAILED: {model} — {_safe_error(exc)}")

    print("ERROR: None of the configured Gemini models responded successfully.")
    return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(check_litellm()))
