import asyncio
import json

from mcp.client import Client

from app.agent.tools import Toolbox
from app.learn import state
from app.mcp_server.server import build_server

KKT = "math-optimization-kkt-and-constrained-optimization"


def run(coro):
    return asyncio.run(coro)


def test_mcp_lists_tools_and_never_exposes_uid_or_commit(db, uid):
    async def go():
        async with Client(build_server(uid)) as c:
            tools = (await c.list_tools()).tools
            names = {t.name for t in tools}
            assert {"find_topics", "get_prerequisite_closure", "propose_plan", "find_bottlenecks"} <= names
            assert "commit_plan" not in names
            for t in tools:
                assert "uid" not in json.dumps(t.input_schema if hasattr(t, "input_schema") else t.inputSchema)
            r = await c.call_tool("find_topics", {"query": "kkt constrained", "limit": 3})
            return json.loads(r.content[0].text)
    out = run(go())
    assert out["matches"][0]["id"] == KKT
    assert KKT in out["evidence_ids"]


def test_tools_respect_student_state(db, uid):
    box = Toolbox(uid)
    full = box.call("get_prerequisite_closure", {"target_ids": [KKT]})
    state.seed_beliefs(uid, ["math-foundations-of-mathematics-logic-and-quantifiers",
                             "math-foundations-of-mathematics-proof-techniques"])
    cut = box.call("get_prerequisite_closure", {"target_ids": [KKT]})
    assert len(cut["needed"]) == len(full["needed"]) - 2
    assert len(cut["skipped_because_mastered"]) == 2


def test_propose_validates_and_commit_is_idempotent(db, uid):
    box = Toolbox(uid)
    ids = [n["id"] for n in box.call("get_prerequisite_closure", {"target_ids": [KKT]})["needed"]]
    import pytest
    from app.agent.tools import ToolError
    with pytest.raises(ToolError):
        box.call("propose_plan", {"subtopic_ids": ids[::-1], "hours_per_week": 6, "weeks_available": 20})
    with pytest.raises(ToolError):
        box.call("propose_plan", {"subtopic_ids": [KKT], "hours_per_week": 6, "weeks_available": 20})
    prop = box.call("propose_plan", {"subtopic_ids": ids, "hours_per_week": 6, "weeks_available": 40})
    assert "commit_plan" not in box.specs()
    a = box.call("commit_plan", {"proposal_id": prop["proposal_id"]}, allow_commit=True)
    b = box.call("commit_plan", {"proposal_id": prop["proposal_id"]}, allow_commit=True)
    assert a["status"] == "committed" and not a["already"] and b["already"]
    other = Toolbox("intruder")
    assert other.get_proposal(prop["proposal_id"]) is None
