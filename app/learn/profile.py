"""Learner profile from onboarding (enumerated fields only, safe to send to an LLM)."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from app.kg.connection import kg_graph, rows, student_graph
from app.learn import state

Level = Literal["beginner", "intermediate", "advanced"]


class Profile(BaseModel):
    level: Level = "intermediate"
    hours_per_week: float = Field(default=5, gt=0, le=60)
    known_topic_ids: list[str] = Field(default_factory=list, max_length=300)  # across all subjects
    onboarded: bool = False


def get_profile(uid: str, graph: Any | None = None) -> Profile:
    res = rows(graph or student_graph(),
               "MATCH (l:Learner {uid:$uid}) RETURN l.level, l.hours_per_week, l.known_topics", {"uid": uid})
    if not res or res[0][0] is None:
        return Profile()
    lvl, hpw, known = res[0]
    return Profile(level=lvl, hours_per_week=hpw or 5, known_topic_ids=list(known or []), onboarded=True)


def save_profile(uid: str, p: Profile, *, graph: Any | None = None) -> Profile:
    """Persist the profile and give self-reported topics provisional (not mastered) credit."""
    g = graph or student_graph()
    valid = {r[0]: r[1] for r in rows(kg_graph(),
             "MATCH (t:Topic) RETURN t.id, t.title")}
    known = [t for t in p.known_topic_ids if t in valid]
    g.query("MERGE (l:Learner {uid:$uid}) SET l.level=$lvl, l.hours_per_week=$h, l.known_topics=$known",
            {"uid": uid, "lvl": p.level, "h": p.hours_per_week, "known": known})
    already = state.get_beliefs(uid, graph=g)
    for tid in known:
        for r in rows(kg_graph(),
                      "MATCH (:Topic {id:$t})-[:CONTAINS]->(s:Subtopic) RETURN s.id", {"t": tid}):
            if r[0] not in already:  # never overwrite measured evidence
                state.apply_evidence(uid, r[0], 1.4, 1.0, graph=g)
    return Profile(level=p.level, hours_per_week=p.hours_per_week, known_topic_ids=known, onboarded=True)

