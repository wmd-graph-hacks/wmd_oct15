"""Learner profile from onboarding (enumerated fields only, safe to send to an LLM)."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from app.kg.connection import kg_graph, rows, student_graph
from app.learn import state

Level = Literal["beginner", "intermediate", "advanced"]


class Profile(BaseModel):
    level: Level = "intermediate"
    hours_per_week: float = Field(default=5, gt=0, le=60)
    known_topic_ids: list[str] = Field(default_factory=list, max_length=300)  # across all subjects
    preferred_name: str | None = Field(default=None, min_length=1, max_length=50)
    interest_subject: str | None = Field(default=None, min_length=1, max_length=80)
    onboarded: bool = False

    @field_validator("preferred_name", "interest_subject")
    @classmethod
    def trim_profile_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be blank")
        return value


def get_profile(uid: str, graph: Any | None = None) -> Profile:
    res = rows(graph or student_graph(),
               "MATCH (l:Learner {uid:$uid}) RETURN l.level, l.hours_per_week, l.known_topics, l.preferred_name, l.interest_subject, l.onboarded", {"uid": uid})
    if not res:
        return Profile()
    lvl, hpw, known, name, interest, onboarded = res[0]
    if lvl is None and not name and not interest:
        return Profile()
    return Profile(level=lvl or "intermediate", hours_per_week=hpw or 5, known_topic_ids=list(known or []),
                   preferred_name=name, interest_subject=interest, onboarded=bool(onboarded))


def save_profile(uid: str, p: Profile, *, graph: Any | None = None) -> Profile:
    """Persist the profile and give self-reported topics provisional (not mastered) credit."""
    g = graph or student_graph()
    valid = {r[0]: r[1] for r in rows(kg_graph(),
             "MATCH (t:Topic) RETURN t.id, t.title")}
    known = [t for t in p.known_topic_ids if t in valid]
    previous = get_profile(uid, graph=g)
    preferred_name = (p.preferred_name or previous.preferred_name or "Learner").strip()
    interest = p.interest_subject or previous.interest_subject or "mathematics"
    # If a saved interest no longer exists in the loaded curriculum, select the first available one.
    subjects = rows(kg_graph(), "MATCH (c:Course) WHERE c.subject IS NOT NULL RETURN c.subject ORDER BY c.title")
    valid_subjects = [r[0] for r in subjects]
    if valid_subjects and interest not in valid_subjects:
        interest = "mathematics" if "mathematics" in valid_subjects else valid_subjects[0]
    g.query("MERGE (l:Learner {uid:$uid}) SET l.level=$lvl, l.hours_per_week=$h, l.known_topics=$known, "
            "l.preferred_name=$name, l.interest_subject=$interest, l.onboarded=true",
            {"uid": uid, "lvl": p.level, "h": p.hours_per_week, "known": known,
             "name": preferred_name, "interest": interest})
    already = state.get_beliefs(uid, graph=g)
    for tid in known:
        for r in rows(kg_graph(),
                      "MATCH (:Topic {id:$t})-[:CONTAINS]->(s:Subtopic) RETURN s.id", {"t": tid}):
            if r[0] not in already:  # never overwrite measured evidence
                state.apply_evidence(uid, r[0], 1.4, 1.0, graph=g)
    return Profile(level=p.level, hours_per_week=p.hours_per_week, known_topic_ids=known,
                   preferred_name=preferred_name, interest_subject=interest, onboarded=True)

