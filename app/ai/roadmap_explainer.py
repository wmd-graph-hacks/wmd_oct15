"""Low-cost, graph-grounded wording for a deterministic roadmap."""

import hashlib
import json
import logging
import re

from app.config import settings

_PLAN_CACHE: dict[str, dict] = {}
logger = logging.getLogger(__name__)


def _cache_key(graph_context: dict) -> str:
    canonical = json.dumps(graph_context, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


async def personalize_roadmap(graph_context: dict) -> dict | None:
    """Select/order retrieved candidates and summarize them, or return None.

    Only a small graph-derived context is sent. Learner identifiers are never
    accepted by this function. The model may select candidate IDs only; callers
    validate existence and prerequisite ordering before accepting its proposal.
    """
    if not settings.ai_enabled or not settings.ai_model or not graph_context.get("items"):
        return None

    key = _cache_key(graph_context)
    cached = _PLAN_CACHE.get(key)
    if cached:
        return cached

    try:
        from litellm import acompletion
    except ImportError:
        logger.warning("LiteLLM is not installed; using graph-ranked roadmap")
        return None

    messages = [
        {
            "role": "system",
            "content": (
                "You are selecting a short study plan from graph-retrieved candidates. "
                "Return only JSON with keys selected_topic_ids and summary. "
                "selected_topic_ids must contain up to 3 unique topic_id values copied "
                "from the candidates. Prefer prerequisite gaps supported by assessment "
                "evidence and attached resources. Respect prerequisite_path ordering. "
                "Never invent topics, dependencies, scores, resources, references, or mastery. "
                "summary is at most 2 short sentences using only supplied graph facts."
            ),
        },
        {"role": "user", "content": json.dumps(graph_context, ensure_ascii=False)},
    ]

    # Try the primary model and then the configured fallbacks. Invalid model
    # output also advances the chain, since it cannot be used safely.
    models = tuple(dict.fromkeys((settings.ai_model, *getattr(settings, "ai_fallback_models", ()))))
    for model in models:
        try:
            response = await acompletion(
                model=model,
                messages=messages,
                response_format={"type": "json_object"},
                max_tokens=settings.ai_max_tokens if hasattr(settings, "ai_max_tokens") else 200,
                timeout=settings.ai_timeout_seconds,
                num_retries=0,
            )
            proposal = _parse_proposal(response.choices[0].message.content)
            if proposal is None:
                logger.warning("LiteLLM model %s returned unusable roadmap JSON; trying next model", model)
                continue
            if len(_PLAN_CACHE) >= getattr(settings, "ai_cache_size", 256):
                _PLAN_CACHE.pop(next(iter(_PLAN_CACHE)))
            _PLAN_CACHE[key] = proposal
            logger.info("LiteLLM roadmap proposal accepted from model %s", model)
            return proposal
        except Exception as exc:
            # Avoid logging provider error text, which may contain sensitive details.
            logger.warning("LiteLLM request failed for model %s (%s); trying next model", model, type(exc).__name__)

    # The deterministic graph roadmap remains usable when every model fails.
    return None


def _parse_proposal(content: object) -> dict | None:
    if not isinstance(content, str) or not content.strip():
        return None
    candidate = content.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", candidate, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        candidate = fenced.group(1).strip()
    else:
        # Some models add a short preamble despite the JSON-only instruction.
        start, end = candidate.find("{"), candidate.rfind("}")
        if start >= 0 and end > start:
            candidate = candidate[start : end + 1]
    try:
        proposal = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    if not isinstance(proposal, dict):
        return None
    selected = proposal.get("selected_topic_ids")
    summary = proposal.get("summary")
    if (
        not isinstance(selected, list)
        or len(selected) > 3
        or any(not isinstance(topic_id, str) for topic_id in selected)
        or len(selected) != len(set(selected))
        or not isinstance(summary, str)
    ):
        return None
    return {"selected_topic_ids": selected, "summary": summary.strip()[:600]}
