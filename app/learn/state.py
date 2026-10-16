"""Student-graph writes/reads (uid-scoped). The uid comes from the auth context only."""
from __future__ import annotations

import time
from typing import Any

from app.kg.connection import rows, student_graph
from app.learn.mastery import TAU_MS, Belief

_STATE_Q = (
    "MATCH (:Learner {uid:$uid})-[:HAS_KNOWLEDGE]->(k:LearnerSubtopic) "
    "RETURN k.subtopic_id, k.alpha, k.beta, k.updated_ms, k.n_attempts, k.inferred"
)


def now_ms() -> int:
    return int(time.time() * 1000)


def ensure_learner(uid: str, graph: Any | None = None) -> None:
    (graph or student_graph()).query("MERGE (l:Learner {uid:$uid})", {"uid": uid})


def get_beliefs(uid: str, at_ms: int | None = None, graph: Any | None = None) -> dict[str, dict]:
    at = at_ms or now_ms()
    out: dict[str, dict] = {}
    for sid, a, b, upd, n, inferred in rows(graph or student_graph(), _STATE_Q, {"uid": uid}):
        belief = Belief(float(a), float(b)).decayed(at - float(upd))
        out[sid] = {"subtopic_id": sid, "mean": round(belief.mean, 3), "evidence": round(belief.evidence, 2),
                    "status": belief.status, "n_attempts": int(n), "inferred": bool(inferred)}
    return out


def mastered_ids(uid: str, graph: Any | None = None) -> list[str]:
    return [s for s, v in get_beliefs(uid, graph=graph).items() if v["status"] == "mastered"]


_ANSWER_Q = (
    "MERGE (l:Learner {uid:$uid}) "
    "WITH l MERGE (k:LearnerSubtopic {key:$key}) "
    "ON CREATE SET k.uid=$uid, k.subtopic_id=$sid, k.alpha=1.0, k.beta=1.0, k.updated_ms=$now_ms, "
    "k.n_attempts=0, k.inferred=false "
    "MERGE (l)-[:HAS_KNOWLEDGE]->(k) "
    "WITH k, exp(-1.0*($now_ms-k.updated_ms)/$tau_ms) AS d "
    "SET k.alpha=1.0+(k.alpha-1.0)*d+$weight*$credit, k.beta=1.0+(k.beta-1.0)*d+$weight*(1.0-$credit), "
    "k.updated_ms=$now_ms, k.n_attempts=k.n_attempts+1, k.inferred=false "
    "RETURN k.alpha, k.beta"
)


def apply_evidence(uid: str, subtopic_id: str, weight: float, cr: float, *, now: int | None = None,
                   graph: Any | None = None) -> Belief:
    """Single atomic Cypher: decay in-query, then add weighted evidence."""
    res = rows(graph or student_graph(), _ANSWER_Q, {
        "uid": uid, "key": f"{uid}|{subtopic_id}", "sid": subtopic_id, "now_ms": now or now_ms(),
        "tau_ms": TAU_MS, "weight": weight, "credit": cr}, write=True)
    return Belief(float(res[0][0]), float(res[0][1]))


def seed_beliefs(uid: str, mastered: list[str], *, graph: Any | None = None) -> None:
    """Demo helper: give strong evidence on given subtopics."""
    g = graph or student_graph()
    ensure_learner(uid, g)
    for sid in mastered:
        for _ in range(3):
            apply_evidence(uid, sid, 1.4, 1.0, graph=g)


def reset_learner(uid: str, graph: Any | None = None) -> None:
    g = graph or student_graph()
    for q in (
        "MATCH (k:LearnerSubtopic {uid:$uid}) DETACH DELETE k",
        "MATCH (a:QuizAttempt {uid:$uid}) DETACH DELETE a",
        "MATCH (p:PlanProposal {uid:$uid}) DETACH DELETE p",
        "MATCH (r:AgentRun {uid:$uid}) DETACH DELETE r",
        "MATCH (p:StudyPlan {uid:$uid}) DETACH DELETE p",
    ):
        g.query(q, {"uid": uid})
