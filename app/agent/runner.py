from __future__ import annotations

import asyncio
import json
import secrets
import logging

from app.agent.controllers import LLMController, PlaybookController, Recorder
from app.agent.models import AgentRequest, AgentRun
from app.agent.tools import ToolError, Toolbox
from app.config import settings
from app.kg.connection import rows, student_graph
from app.learn import state

logger = logging.getLogger(__name__)


async def run_agent(uid: str, req: AgentRequest, *, llm: LLMController | None = None, use_llm: bool | None = None,
                    box: Toolbox | None = None) -> AgentRun:
    """Run the LLM controller if enabled, otherwise (or on any failure) the deterministic playbook."""
    want_llm = settings.ai_enabled if use_llm is None else use_llm
    box = box or Toolbox(uid, subject=req.subject)
    run = AgentRun(id=secrets.token_urlsafe(8), controller="playbook", request=req)
    fallback: str | None = None
    if want_llm:
        run.controller = "llm"
        rec = Recorder(box, run, settings.agent_max_tool_calls)
        try:
            async with asyncio.timeout(settings.agent_run_timeout_seconds):
                await (llm or LLMController()).run(rec)
            rec.finalize()
            _persist(uid, run)
            return run
        except TimeoutError:
            fallback = f"LLM agent exceeded its {settings.agent_run_timeout_seconds:g}s total budget"
            logger.warning("agent LLM controller exceeded total budget, using playbook")
            run = AgentRun(id=run.id, controller="playbook", request=req, fallback_reason=fallback)
        except Exception as exc:
            fallback = f"{type(exc).__name__}: {exc}"[:160]
            logger.warning("agent LLM controller failed, using playbook (%s)", type(exc).__name__)
            run = AgentRun(id=run.id, controller="playbook", request=req, fallback_reason=fallback)
    rec = Recorder(box, run, 16)
    try:
        await PlaybookController().run(rec)
        rec.finalize()
        logger.info("agent playbook completed subject=%s tool_calls=%d", req.subject or "all", len(run.steps))
    except ToolError as exc:
        run.status, run.explanation = "failed", str(exc)
    _persist(uid, run)
    return run


def _persist(uid: str, run: AgentRun) -> None:
    student_graph().query(
        "MERGE (l:Learner {uid:$uid}) CREATE (l)-[:RAN]->(:AgentRun {id:$id, uid:$uid, payload:$p, created_ms:$now})",
        {"uid": uid, "id": run.id, "p": run.model_dump_json(), "now": state.now_ms()})


def get_run(uid: str, run_id: str) -> AgentRun | None:
    res = rows(student_graph(), "MATCH (r:AgentRun {id:$id, uid:$uid}) RETURN r.payload", {"id": run_id, "uid": uid})
    return AgentRun(**json.loads(res[0][0])) if res else None
