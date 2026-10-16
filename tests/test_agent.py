import asyncio
import json
from types import SimpleNamespace as NS

from app.agent.controllers import LLMController
from app.agent.models import AgentRequest
from app.agent.runner import get_run, run_agent
from app.agent.tools import Toolbox
from app.learn import state

KKT = "math-optimization-kkt-and-constrained-optimization"
FOUND = "math-foundations-of-mathematics-logic-and-quantifiers"


def go(coro):
    return asyncio.run(coro)


def test_playbook_end_to_end_is_grounded(db, uid):
    state.seed_beliefs(uid, [FOUND])
    run = go(run_agent(uid, AgentRequest(goal="KKT constrained optimization", hours_per_week=6, weeks_available=30), use_llm=False))
    assert run.status == "proposed" and run.controller == "playbook"
    tools = [s.tool for s in run.steps]
    assert tools[0] == "get_student_state" and "propose_plan" in tools and "commit_plan" not in tools
    assert run.proposal_id and KKT in run.highlight["targets"]
    seen = {i for s in run.steps for i in s.evidence_ids}
    assert set(run.cited_ids) <= seen
    assert FOUND not in run.highlight["needed"] and FOUND in run.highlight["mastered"]
    assert get_run(uid, run.id).id == run.id
    assert get_run("other-user", run.id) is None


def test_infeasible_deadline_is_reported(db, uid):
    run = go(run_agent(uid, AgentRequest(goal="KKT", hours_per_week=1, weeks_available=2), use_llm=False))
    assert "need about" in run.explanation


def test_unknown_goal_fails_cleanly(db, uid):
    run = go(run_agent(uid, AgentRequest(goal="quantum basket weaving", subject="mathematics"), use_llm=False))
    assert run.status == "failed"


def _call(i, name, args):
    return NS(id=f"c{i}", function=NS(name=name, arguments=json.dumps(args)))


def scripted(box_ids):
    """Fake LLM: find_topics -> closure -> propose -> explanation."""
    state_ = {"n": 0, "ids": box_ids}

    async def completion(**kw):
        state_["n"] += 1
        n = state_["n"]
        if n == 1:
            m = NS(content=None, tool_calls=[_call(1, "find_topics", {"query": "kkt"})])
        elif n == 2:
            m = NS(content=None, tool_calls=[_call(2, "get_prerequisite_closure", {"target_ids": [KKT]})])
        elif n == 3:
            ids = state_["ids"]()
            m = NS(content=None, tool_calls=[_call(3, "propose_plan", {"subtopic_ids": ids, "hours_per_week": 6, "weeks_available": 40})])
        else:
            m = NS(content=state_.get("final", f"Start with the basics and finish at `{KKT}`."), tool_calls=None)
        return NS(choices=[NS(message=m)])
    return completion, state_


def test_llm_controller_happy_path(db, uid, monkeypatch):
    from app.config import settings
    monkeypatch.setattr("app.agent.runner.settings", NS(ai_enabled=True, agent_max_tool_calls=8))
    monkeypatch.setattr("app.agent.controllers.settings", NS(ai_enabled=True, ai_model="m", ai_fallback_models=(), agent_max_tool_calls=8, agent_max_tokens=500, agent_timeout_seconds=5))
    box = Toolbox(uid)
    ids = lambda: [n["id"] for n in box.call("get_prerequisite_closure", {"target_ids": [KKT]})["needed"]]
    comp, _ = scripted(ids)
    run = go(run_agent(uid, AgentRequest(goal="kkt"), llm=LLMController(comp, ("m",)), use_llm=True, box=box))
    assert run.controller == "llm" and run.fallback_reason is None and run.proposal_id


def test_llm_hallucinated_id_falls_back_to_playbook(db, uid, monkeypatch):
    monkeypatch.setattr("app.agent.controllers.settings", NS(ai_enabled=True, ai_model="m", ai_fallback_models=(), agent_max_tool_calls=8, agent_max_tokens=500, agent_timeout_seconds=5))
    box = Toolbox(uid)
    ids = lambda: [n["id"] for n in box.call("get_prerequisite_closure", {"target_ids": [KKT]})["needed"]]
    comp, st = scripted(ids)
    st["final"] = "You should study `math-made-up-topic` first."
    run = go(run_agent(uid, AgentRequest(goal="kkt"), llm=LLMController(comp, ("m",)), use_llm=True, box=box))
    assert run.controller == "playbook" and "cites ids" in (run.fallback_reason or "")


def test_llm_error_falls_back(db, uid, monkeypatch):
    monkeypatch.setattr("app.agent.controllers.settings", NS(ai_enabled=True, ai_model="m", ai_fallback_models=(), agent_max_tool_calls=8, agent_max_tokens=500, agent_timeout_seconds=5))

    async def boom(**kw):
        raise TimeoutError("down")
    run = go(run_agent(uid, AgentRequest(goal="kkt"), llm=LLMController(boom, ("m",)), use_llm=True))
    assert run.controller == "playbook" and run.status == "proposed"


def test_misspelled_topic_goal_targets_whole_topic(db, uid):
    run = go(run_agent(uid, AgentRequest(goal="I want to learn calculas", hours_per_week=6, weeks_available=10), use_llm=False))
    assert run.status == "proposed", run.explanation
    assert len(run.highlight["targets"]) >= 6
    assert all("calculus" in t for t in run.highlight["targets"])


def test_find_topics_fuzzy_and_stopwords(db):
    from app.kg import queries as q
    assert q.find_topics("I want to understand kkt conditions")["matches"][0]["id"].endswith("kkt-and-constrained-optimization")
    assert q.find_topics("optimisation")["matches"]
    assert q.find_topics("basket weaving")["matches"] == []


def test_llm_budget_is_reported_not_fatal(db, uid, monkeypatch):
    monkeypatch.setattr("app.agent.controllers.settings", NS(ai_enabled=True, ai_model="m", ai_fallback_models=(), agent_max_tool_calls=2, agent_max_tokens=500, agent_timeout_seconds=5))
    monkeypatch.setattr("app.agent.runner.settings", NS(ai_enabled=True, agent_max_tool_calls=2))
    box = Toolbox(uid)
    ids = lambda: [n["id"] for n in box.call("get_prerequisite_closure", {"target_ids": [KKT]})["needed"]]
    n = {"i": 0}

    async def comp(**kw):
        n["i"] += 1
        i = n["i"]
        if i <= 3:
            m = NS(content=None, tool_calls=[_call(i, "get_student_state", {})])
        elif i == 4:
            m = NS(content=None, tool_calls=[_call(i, "propose_plan", {"subtopic_ids": ids(), "hours_per_week": 6, "weeks_available": 40})])
        else:
            m = NS(content="Done.", tool_calls=None)
        return NS(choices=[NS(message=m)])
    run = go(run_agent(uid, AgentRequest(goal="kkt"), llm=LLMController(comp, ("m",)), use_llm=True, box=box))
    assert run.controller == "llm" and run.proposal_id
