"""Agent controllers. Both only call tools; neither can commit a plan."""
from __future__ import annotations

import asyncio
import json
import logging
import math
import re
import time
from typing import Any, Awaitable, Callable

from app.agent.models import AgentRequest, AgentRun, TraceStep
from app.agent.tools import ToolError, Toolbox
from app.config import settings

logger = logging.getLogger(__name__)


def _summ(name: str, out: dict) -> str:
    if name == "find_topics":
        if out.get("topic_match"):
            return f"goal names the topic {out['topic_match']['title']} ({len(out['topic_match']['subtopic_ids'])} subtopics)"
        return "matched " + ", ".join(m["title"] for m in out["matches"][:3]) if out["matches"] else "no match"
    if name == "get_prerequisite_closure":
        return f"{len(out['needed'])} subtopics needed ({out['needed_minutes']} min), {len(out['skipped_because_mastered'])} skipped as mastered"
    if name == "explain_path":
        return f"{out['hops']} hops: " + " → ".join(p["title"] or p["id"] for p in out["path"])
    if name == "find_bottlenecks":
        return "gatekeepers: " + ", ".join(b["title"] for b in out["bottlenecks"][:3])
    if name == "critical_path":
        return f"critical chain {out['minutes']} min over {len(out['path'])} subtopics"
    if name == "list_subjects":
        return f"{len(out['subjects'])} subjects"
    if name == "get_student_state":
        return f"{len(out['mastered'])} mastered, {len(out['learning'])} learning, {len(out['gaps'])} gaps"
    if name == "get_frontier":
        return f"{out['total_ready']} subtopics ready to start"
    if name == "check_feasibility":
        return f"{out['total_minutes']} min needs {out['weeks_needed']} wk vs {out['weeks_available']} available ({'fits' if out['feasible'] else 'does not fit'})"
    if name == "assign_quiz":
        return f"{out['questions_available']} questions available"
    if name == "propose_plan":
        return f"proposal ready: {len(out['weeks'])} weeks, {out['total_minutes']} min"
    return "ok"


class Recorder:
    """Executes tools in a worker thread, records the trace, tracks evidence ids."""

    def __init__(self, box: Toolbox, run: AgentRun, max_calls: int):
        self.box, self.run, self.max_calls = box, run, max_calls
        self.seen: set[str] = set()
        self.outputs: dict[str, list[dict]] = {}

    async def call(self, name: str, args: dict) -> dict:
        if len(self.run.steps) >= self.max_calls and not (name == "propose_plan" and not self.run.proposal_id):
            raise ToolError("tool budget exhausted")
        t0 = time.perf_counter()
        try:
            out = await asyncio.to_thread(self.box.call, name, args)
            ok, summary = True, _summ(name, out)
        except ToolError as exc:
            out, ok, summary = {"error": str(exc), "evidence_ids": []}, False, f"error: {exc}"
        step = TraceStep(index=len(self.run.steps) + 1, tool=name, args=args, summary=summary,
                         evidence_ids=out.get("evidence_ids", []), ok=ok,
                         ms=int((time.perf_counter() - t0) * 1000))
        self.run.steps.append(step)
        if ok:
            self.seen.update(out.get("evidence_ids", []))
            self.outputs.setdefault(name, []).append(out)
            if name == "propose_plan":
                self.run.proposal_id = out["proposal_id"]
        return out

    def finalize(self) -> None:
        o = self.outputs

        def last(name: str) -> dict:
            return (o.get(name) or [{}])[-1]

        closure_steps = [st for st in self.run.steps if st.tool == "get_prerequisite_closure" and st.ok]
        self.run.highlight = {
            "targets": closure_steps[-1].args.get("target_ids", []) if closure_steps else [],
            "needed": [n["id"] for n in last("get_prerequisite_closure").get("needed", [])],
            "path": [p["id"] for p in last("explain_path").get("path", [])],
            "bottlenecks": [b["id"] for b in last("find_bottlenecks").get("bottlenecks", [])],
            "mastered": last("get_student_state").get("mastered", []),
        }


def grounded(text: str, seen: set[str]) -> tuple[list[str], bool]:
    from app.kg.queries import id_pattern
    pat = id_pattern()
    cited = sorted(set(pat.findall(text))) if pat else []
    return cited, all(c in seen for c in cited)


class PlaybookController:
    name = "playbook"

    async def run(self, rec: Recorder) -> None:
        req = rec.run.request
        await rec.call("get_student_state", {})
        found = await rec.call("find_topics", {"query": req.goal, "limit": 6})
        matches = found.get("matches", [])
        if not matches:
            raise ToolError("No subtopic in the curriculum matches that goal")
        topic = found.get("topic_match")
        if topic:  # the goal names a whole topic: target all of its subtopics
            targets = topic["subtopic_ids"][:10]
        else:
            top = matches[0]["score"]
            targets = [m["id"] for m in matches if m["score"] == top][:2]
        closure = await rec.call("get_prerequisite_closure", {"target_ids": targets})
        needed = [n["id"] for n in closure.get("needed", [])]
        if not needed:
            raise ToolError("You already have everything needed for this goal")
        bott = await rec.call("find_bottlenecks", {"target_ids": targets})
        cp = await rec.call("critical_path", {"target_ids": targets})
        feas = await rec.call("check_feasibility", {"subtopic_ids": needed, "hours_per_week": req.hours_per_week,
                                                    "weeks_available": req.weeks_available})
        first_gate = next((b["id"] for b in bott.get("bottlenecks", []) if b["id"] != targets[0]), None)
        path_out = {}
        if first_gate:
            path_out = await rec.call("explain_path", {"from_id": first_gate, "to_id": targets[0]})
        checkpoints = [b["id"] for b in bott.get("bottlenecks", [])
                       if b["has_quiz"] and b["student_status"] == "unseen"][:3]
        for sid in checkpoints:
            await rec.call("assign_quiz", {"subtopic_id": sid})
        prop = await rec.call("propose_plan", {"subtopic_ids": needed, "hours_per_week": req.hours_per_week,
                                               "weeks_available": req.weeks_available, "goal": req.goal,
                                               "checkpoint_quiz_ids": checkpoints})
        titles = {n["id"]: n["title"] for n in closure["needed"]}
        tgt_title = topic["title"] if topic else titles.get(targets[0], targets[0])
        parts = [f"To reach **{tgt_title}** you still need {len(needed)} subtopics "
                 f"({closure['needed_minutes']} min); {len(closure['skipped_because_mastered'])} were skipped because you already master them."]
        if closure.get("basis", "").startswith("syllabus"):
            parts.append("Note: this subject's source files carry no authored prerequisites, so the order below follows the "
                         "syllabus stages (inferred), not verified dependencies.")
        if bott.get("bottlenecks"):
            b = bott["bottlenecks"][0]
            parts.append(f"The biggest gatekeeper is **{b['title']}** (`{b['id']}`); many later topics depend on it.")
        if path_out.get("path"):
            parts.append("Dependency chain: " + " → ".join(f"{p['title']} (`{p['id']}`)" for p in path_out["path"]) + ".")
        if cp.get("path"):
            parts.append(f"The longest unavoidable chain is {cp['minutes']} min.")
        if feas["feasible"]:
            parts.append(f"At {req.hours_per_week:g} h/week it takes {len(prop['weeks'])} weeks, within your {req.weeks_available}.")
        else:
            need_hpw = math.ceil(feas["total_minutes"] / 60 / req.weeks_available * 10) / 10
            parts.append(f"At {req.hours_per_week:g} h/week this takes {len(prop['weeks'])} weeks, over your {req.weeks_available}; you would need about {need_hpw:g} h/week to fit.")
        if checkpoints:
            parts.append("I added self-test checkpoints for unassessed gatekeepers: " + ", ".join(f"`{c}`" for c in checkpoints) + ".")
        text = " ".join(parts)
        cited, ok = grounded(text, rec.seen | set(needed) | set(targets))
        rec.run.explanation, rec.run.cited_ids = text, cited


_SYSTEM = (
    "You are a study-planning agent over a curriculum prerequisite graph for one subject. Use the tools to ground every claim. "
    "Work out the student's goal target subtopic(s) with find_topics (if it returns topic_match, use its subtopic_ids as the targets), then call get_student_state and "
    "get_prerequisite_closure, then find_bottlenecks / critical_path / check_feasibility as needed, and finish by "
    "calling propose_plan with the closure's subtopic ids in the order returned. Never invent subtopic ids, "
    "prerequisites, scores or durations. You cannot activate plans; the student approves proposals. "
    "When done, reply with a 3-5 sentence explanation that cites subtopic ids in backticks, using only ids that tools returned."
)

Completion = Callable[..., Awaitable[Any]]


class LLMController:
    name = "llm"

    def __init__(self, completion: Completion | None = None, models: tuple[str, ...] | None = None):
        self._completion = completion
        self._models = models or tuple(dict.fromkeys((settings.ai_model, *settings.ai_fallback_models)))

    def _tool_schemas(self, rec: Recorder) -> list[dict]:
        out = []
        for name, spec in rec.box.specs().items():
            schema = spec.args.model_json_schema()
            schema.pop("title", None)
            out.append({"type": "function", "function": {"name": name, "description": spec.description,
                                                         "parameters": schema}})
        return out

    async def run(self, rec: Recorder) -> None:
        completion = self._completion
        if completion is None:
            from litellm import acompletion  # raises ImportError -> caller falls back
            completion = acompletion
        if not settings.ai_enabled or not self._models:
            raise RuntimeError("LLM disabled")
        req = rec.run.request
        messages: list[dict] = [
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": json.dumps({"goal": req.goal, "hours_per_week": req.hours_per_week,
                                                    "weeks_available": req.weeks_available})},
        ]
        tools = self._tool_schemas(rec)
        last_error: Exception | None = None
        for model in self._models:
            try:
                await self._loop(completion, model, messages, tools, rec)
                return
            except Exception as exc:
                last_error = exc
                logger.warning("agent LLM %s failed (%s)", model, type(exc).__name__)
                if rec.run.steps:  # partial trace under one model: do not mix models
                    break
        raise RuntimeError(f"LLM controller failed: {last_error}") from last_error

    async def _loop(self, completion: Completion, model: str, messages: list[dict], tools: list[dict], rec: Recorder) -> None:
        msgs = list(messages)
        for _ in range(settings.agent_max_tool_calls + 4):
            resp = await completion(model=model, messages=msgs, tools=tools, tool_choice="auto",
                                    max_tokens=settings.agent_max_tokens, timeout=settings.agent_timeout_seconds,
                                    num_retries=0)
            msg = resp.choices[0].message
            calls = getattr(msg, "tool_calls", None) or []
            if not calls:
                text = (msg.content or "").strip()
                if not rec.run.proposal_id:
                    raise RuntimeError("model finished without proposing a plan")
                cited, ok = grounded(text, rec.seen)
                if not ok or not text:
                    raise RuntimeError("explanation cites ids no tool returned")
                rec.run.explanation, rec.run.cited_ids = text, cited
                return
            msgs.append({"role": "assistant", "content": msg.content or "", "tool_calls": [
                {"id": c.id, "type": "function", "function": {"name": c.function.name, "arguments": c.function.arguments}}
                for c in calls]})
            for c in calls:
                try:
                    args = json.loads(c.function.arguments or "{}")
                    out = await rec.call(c.function.name, args)
                except json.JSONDecodeError:
                    out = {"error": "arguments were not valid JSON"}
                except ToolError as exc:
                    out = {"error": str(exc) + ("; stop exploring and call propose_plan now" if "budget" in str(exc) else "")}
                msgs.append({"role": "tool", "tool_call_id": c.id, "content": json.dumps(out)[:6000]})
        raise RuntimeError("model did not finish within the tool budget")
