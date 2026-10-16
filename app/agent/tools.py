"""Graph tools shared by the in-process agent and the MCP server. uid is bound at construction,
never a tool argument."""
from __future__ import annotations

import json
import math
import secrets
from datetime import date, timedelta
from typing import Any, Callable

from pydantic import BaseModel, Field

from app.kg import queries as kg
from app.kg.connection import kg_graph, rows, student_graph
from app.learn import bank, state


class ToolError(Exception):
    pass


# ---- argument models -------------------------------------------------------------------------
class FindTopicsArgs(BaseModel):
    query: str = Field(description="Free-text goal or topic keywords, e.g. 'KKT conditions'")
    limit: int = Field(default=6, ge=1, le=15)


class TargetsArgs(BaseModel):
    target_ids: list[str] = Field(min_length=1, max_length=10, description="Subtopic ids from find_topics")


class PathArgs(BaseModel):
    from_id: str
    to_id: str


class NoArgs(BaseModel):
    pass


class FeasibilityArgs(BaseModel):
    subtopic_ids: list[str] = Field(min_length=1, max_length=120)
    hours_per_week: float = Field(gt=0, le=80)
    weeks_available: int = Field(gt=0, le=104)


class ProposeArgs(BaseModel):
    subtopic_ids: list[str] = Field(min_length=1, max_length=120, description="Ordered study plan")
    hours_per_week: float = Field(gt=0, le=80)
    weeks_available: int = Field(gt=0, le=104)
    goal: str = Field(default="", max_length=300)
    checkpoint_quiz_ids: list[str] = Field(default_factory=list, max_length=10)


class CommitArgs(BaseModel):
    proposal_id: str


class QuizArgs(BaseModel):
    subtopic_id: str


class ToolSpec(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    name: str
    description: str
    args: type[BaseModel]
    fn: Callable[..., dict]
    mutates: bool = False


def _evidence(*groups: Any, pattern: Any = None) -> list[str]:
    ids: set[str] = set()

    def walk(x: Any) -> None:
        if isinstance(x, str) and pattern is not None and pattern.fullmatch(x):
            ids.add(x)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, (list, tuple)):
            for v in x:
                walk(v)

    walk(groups)
    return sorted(ids)


class Toolbox:
    def __init__(self, uid: str, *, subject: str | None = None, kg_graph: Any | None = None,
                 sgraph: Any | None = None):
        from app.kg.loader import ensure_loaded
        if kg_graph is None:
            ensure_loaded()
        self.uid = uid
        self.subject = subject
        self._subject_ids: set[str] | None = None
        self._kg = kg_graph
        self._sg = sgraph

    # -- helpers
    def _g(self):
        return self._sg or student_graph()

    def _mastered(self) -> list[str]:
        return state.mastered_ids(self.uid, graph=self._sg)

    def _scoped(self, ids: list[str]) -> list[str]:
        """Restrict ids to the selected subject (all subjects when none selected)."""
        if not self.subject:
            return ids
        if self._subject_ids is None:
            self._subject_ids = {r[0] for r in rows(self._kg or kg_graph(), "MATCH (s:Subtopic {subject:$s}) RETURN s.id",
                                                    {"s": self.subject})}
        return [i for i in ids if i in self._subject_ids]

    def _known(self, ids: list[str]) -> None:
        bad = [i for i in ids if not kg.get_subtopic(i, self._kg)]
        if bad:
            raise ToolError(f"unknown subtopic ids: {bad[:5]}")

    # -- read tools
    def find_topics(self, a: FindTopicsArgs) -> dict:
        return kg.find_topics(a.query, a.limit, self._kg, self.subject)

    def list_subjects(self, a: NoArgs) -> dict:
        subjects = kg.list_subjects(self._kg)
        return {"subjects": subjects, "selected": self.subject}

    def get_prerequisite_closure(self, a: TargetsArgs) -> dict:
        self._known(a.target_ids)
        mastered = self._mastered()
        nodes = kg.prerequisite_closure(a.target_ids, mastered, True, self._kg)
        ordered = kg.order_by_dependency(nodes, True, self._kg)
        full = kg.prerequisite_closure(a.target_ids, [], True, self._kg)
        ids = {n["id"] for n in full} | set(a.target_ids)
        kinds = {st for x, y, st, _ in kg.prerequisite_edges(True, self._kg) if x in ids and y in ids}
        basis = "authored" if kinds & {"recommended", "soft"} else "syllabus-stage order (inferred)" if kinds else "none"
        return {"basis": basis, "needed": [{"id": n["id"], "title": n["title"], "minutes": n["minutes"]} for n in ordered],
                "needed_minutes": sum(int(n["minutes"] or 0) for n in ordered),
                "skipped_because_mastered": sorted({n["id"] for n in full} - {n["id"] for n in ordered}),
                "mastered_count": len(self._scoped(mastered))}

    def explain_path(self, a: PathArgs) -> dict:
        self._known([a.from_id, a.to_id])
        path = kg.explain_path(a.from_id, a.to_id, self._kg)
        titles = {i: (kg.get_subtopic(i, self._kg) or {}).get("title") for i in path}
        return {"path": [{"id": i, "title": titles[i]} for i in path], "hops": max(len(path) - 1, 0)}

    def find_bottlenecks(self, a: TargetsArgs) -> dict:
        self._known(a.target_ids)
        needed = [n["id"] for n in kg.prerequisite_closure(a.target_ids, self._mastered(), True, self._kg)]
        ranked = kg.bottlenecks(needed, 5, self._kg)
        beliefs = state.get_beliefs(self.uid, graph=self._sg)
        for r in ranked:
            r["student_status"] = beliefs.get(r["id"], {}).get("status", "unseen")
            r["has_quiz"] = bool(bank.questions_for(r["id"]))
        return {"bottlenecks": ranked}

    def critical_path(self, a: TargetsArgs) -> dict:
        self._known(a.target_ids)
        needed = [n["id"] for n in kg.prerequisite_closure(a.target_ids, self._mastered(), True, self._kg)]
        cp = kg.critical_path(needed, True, self._kg)
        return {"minutes": cp["minutes"], "path": cp["path"]}

    def get_student_state(self, a: NoArgs) -> dict:
        beliefs = state.get_beliefs(self.uid, graph=self._sg)
        keep = set(self._scoped(list(beliefs)))
        by_status: dict[str, list[str]] = {}
        for sid, v in beliefs.items():
            if sid not in keep:
                continue
            by_status.setdefault(v["status"], []).append(sid)
        return {"mastered": sorted(by_status.get("mastered", [])), "learning": sorted(by_status.get("learning", [])),
                "gaps": sorted(by_status.get("gap", [])), "assessed_count": len(keep)}

    def get_frontier(self, a: NoArgs) -> dict:
        fr = kg.frontier(self._mastered(), True, self._kg, self.subject)
        return {"ready_now": fr[:12], "total_ready": len(fr)}

    def check_feasibility(self, a: FeasibilityArgs) -> dict:
        self._known(a.subtopic_ids)
        minutes = sum(int((kg.get_subtopic(i, self._kg) or {}).get("minutes") or 0) for i in a.subtopic_ids)
        budget = a.hours_per_week * 60
        weeks_needed = math.ceil(minutes / budget) if budget else 0
        cp = kg.critical_path(a.subtopic_ids, True, self._kg)
        hard = kg.critical_path(a.subtopic_ids, False, self._kg)
        return {"total_minutes": minutes, "weeks_needed": weeks_needed, "weeks_available": a.weeks_available,
                "feasible": weeks_needed <= a.weeks_available,
                "shortfall_minutes": max(0, minutes - int(budget * a.weeks_available)),
                "critical_path_minutes": cp["minutes"], "hard_prereq_only_chain_minutes": hard["minutes"]}

    # -- action tools
    def assign_quiz(self, a: QuizArgs) -> dict:
        self._known([a.subtopic_id])
        n = len(bank.questions_for(a.subtopic_id))
        return {"subtopic_id": a.subtopic_id, "questions_available": n, "url": f"/quiz/{a.subtopic_id}",
                "action": "self-test" if n else "no questions yet"}

    def _schedule(self, ids: list[str], hours_per_week: float, start: date) -> list[dict]:
        budget = int(hours_per_week * 60)
        weeks: list[dict] = []
        cur: list[dict] = []
        used = 0
        for sid in ids:
            s = kg.get_subtopic(sid, self._kg) or {}
            m = int(s.get("minutes") or 45)
            if cur and used + m > budget:
                weeks.append({"items": cur, "minutes": used})
                cur, used = [], 0
            cur.append({"id": sid, "title": s.get("title"), "minutes": m})
            used += m
        if cur:
            weeks.append({"items": cur, "minutes": used})
        for i, w in enumerate(weeks):
            w["week"] = i + 1
            w["starts"] = (start + timedelta(weeks=i)).isoformat()
        return weeks

    def validate_plan(self, ids: list[str]) -> list[str]:
        """Return a list of problems: unknown ids, duplicates, or a prerequisite after its dependent."""
        problems: list[str] = []
        if len(ids) != len(set(ids)):
            problems.append("duplicate subtopics")
        try:
            self._known(ids)
        except ToolError as exc:
            return [str(exc)]
        pos = {sid: i for i, sid in enumerate(ids)}
        for a, b, _, _ in kg.prerequisite_edges(True, self._kg):
            if a in pos and b in pos and pos[a] > pos[b]:
                problems.append(f"{a} must come before {b}")
        needed = {n["id"] for n in kg.prerequisite_closure(ids, self._mastered(), True, self._kg)}
        missing = sorted(needed - set(ids))
        if missing:
            problems.append(f"missing prerequisites: {missing[:6]}")
        return problems

    def propose_plan(self, a: ProposeArgs) -> dict:
        problems = self.validate_plan(a.subtopic_ids)
        if problems:
            raise ToolError("plan invalid: " + "; ".join(problems))
        weeks = self._schedule(a.subtopic_ids, a.hours_per_week, date.today() + timedelta(days=(7 - date.today().weekday()) % 7 or 7))
        total = sum(w["minutes"] for w in weeks)
        payload = {"goal": a.goal, "weeks": weeks, "total_minutes": total, "hours_per_week": a.hours_per_week,
                   "weeks_available": a.weeks_available, "fits_deadline": len(weeks) <= a.weeks_available,
                   "checkpoint_quizzes": [i for i in a.checkpoint_quiz_ids if bank.questions_for(i)]}
        pid = secrets.token_urlsafe(8)
        self._g().query(
            "MERGE (l:Learner {uid:$uid}) CREATE (l)-[:PROPOSED]->(:PlanProposal {id:$id, uid:$uid, "
            "status:'proposed', payload:$payload, created_ms:$now})",
            {"uid": self.uid, "id": pid, "payload": json.dumps(payload), "now": state.now_ms()})
        return {"proposal_id": pid, **payload, "status": "proposed (waiting for the student to approve)"}

    def commit_plan(self, a: CommitArgs) -> dict:
        """Only reachable through the approve endpoint, never offered to the agent."""
        res = rows(self._g(),
            "MATCH (p:PlanProposal {id:$id, uid:$uid}) RETURN p.status, p.payload", {"id": a.proposal_id, "uid": self.uid})
        if not res:
            raise ToolError("unknown proposal")
        payload = json.loads(res[0][1])
        ids = [i["id"] for w in payload["weeks"] for i in w["items"]]
        problems = self.validate_plan(ids)
        if problems:
            raise ToolError("plan no longer valid: " + "; ".join(problems))
        done = rows(self._g(),
            "MATCH (p:PlanProposal {id:$id, uid:$uid}) WHERE p.status='proposed' "
            "SET p.status='committed', p.committed_ms=$now RETURN p.id",
            {"id": a.proposal_id, "uid": self.uid, "now": state.now_ms()}, write=True)
        return {"proposal_id": a.proposal_id, "status": "committed", "already": not done}

    def reject_plan(self, proposal_id: str) -> dict:
        rows(self._g(), "MATCH (p:PlanProposal {id:$id, uid:$uid}) WHERE p.status='proposed' SET p.status='rejected'",
             {"id": proposal_id, "uid": self.uid}, write=True)
        return {"proposal_id": proposal_id, "status": "rejected"}

    def get_proposal(self, proposal_id: str) -> dict | None:
        res = rows(self._g(), "MATCH (p:PlanProposal {id:$id, uid:$uid}) RETURN p.status, p.payload",
                   {"id": proposal_id, "uid": self.uid})
        if not res:
            return None
        return {"proposal_id": proposal_id, "status": res[0][0], **json.loads(res[0][1])}

    # -- registry
    def specs(self, *, include_commit: bool = False) -> dict[str, ToolSpec]:
        t = [
            ToolSpec(name="list_subjects", description="Subjects available in the curriculum graph.", args=NoArgs, fn=self.list_subjects),
            ToolSpec(name="find_topics", description="Find subtopics matching a goal's keywords.", args=FindTopicsArgs, fn=self.find_topics),
            ToolSpec(name="get_prerequisite_closure", description="Everything the student still needs before the targets, in study order, skipping mastered material.", args=TargetsArgs, fn=self.get_prerequisite_closure),
            ToolSpec(name="explain_path", description="Shortest prerequisite chain between two subtopics.", args=PathArgs, fn=self.explain_path),
            ToolSpec(name="find_bottlenecks", description="Graph-betweenness gatekeeper subtopics among what the student still needs.", args=TargetsArgs, fn=self.find_bottlenecks),
            ToolSpec(name="critical_path", description="Longest dependency chain (minutes) among what is still needed.", args=TargetsArgs, fn=self.critical_path),
            ToolSpec(name="get_student_state", description="What the student has mastered, is learning, or has gaps in.", args=NoArgs, fn=self.get_student_state),
            ToolSpec(name="get_frontier", description="Subtopics the student can start right now.", args=NoArgs, fn=self.get_frontier),
            ToolSpec(name="check_feasibility", description="Check whether a set of subtopics fits hours per week and a deadline.", args=FeasibilityArgs, fn=self.check_feasibility),
            ToolSpec(name="assign_quiz", description="Point the student at a self-test for a subtopic.", args=QuizArgs, fn=self.assign_quiz, mutates=False),
            ToolSpec(name="propose_plan", description="Create a weekly plan proposal (not active until the student approves).", args=ProposeArgs, fn=self.propose_plan, mutates=True),
        ]
        if include_commit:
            t.append(ToolSpec(name="commit_plan", description="Activate an approved proposal.", args=CommitArgs, fn=self.commit_plan, mutates=True))
        return {s.name: s for s in t}

    def call(self, name: str, raw_args: dict, *, allow_commit: bool = False) -> dict:
        spec = self.specs(include_commit=allow_commit).get(name)
        if spec is None:
            raise ToolError(f"unknown tool {name}")
        try:
            args = spec.args(**raw_args)
        except Exception as exc:
            raise ToolError(f"bad arguments for {name}: {exc}") from exc
        out = spec.fn(args)
        out["evidence_ids"] = _evidence(out, pattern=kg.id_pattern(self._kg))
        return out
