"""Quiz runner: server-side hint counting, shuffled options, idempotent submit, no key leakage."""
from __future__ import annotations

import secrets
from typing import Any

from pydantic import BaseModel

from app.kg.connection import rows, student_graph
from app.learn import bank, state
from app.learn.mastery import Belief, credit


class QuizError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


class PublicQuestion(BaseModel):
    attempt_id: str
    subtopic_id: str
    level: int
    stem: str
    options: list[str]
    hints_available: int


class AnswerResult(BaseModel):
    correct: bool
    correct_position: int
    explanation: str
    hints_used: int
    credit: float
    mean: float
    status: str
    repeated: bool = False


def _level_for(mean: float) -> int:
    return 1 if mean < 0.5 else 2 if mean < 0.7 else 3


def start(uid: str, subtopic_id: str, *, graph: Any | None = None) -> PublicQuestion:
    g = graph or student_graph()
    qs = bank.questions_for(subtopic_id)
    if not qs:
        raise QuizError("No questions for this subtopic yet", 404)
    belief = state.get_beliefs(uid, graph=g).get(subtopic_id)
    target = _level_for(belief["mean"] if belief else 0.5)
    answered = {r[0]: r[1] for r in rows(g,
        "MATCH (a:QuizAttempt {uid:$uid, subtopic_id:$sid}) WHERE a.answered_ms IS NOT NULL "
        "RETURN a.qid, max(a.answered_ms)", {"uid": uid, "sid": subtopic_id})}
    # least-recently answered first, then closest level to the target
    q = min(qs, key=lambda x: (answered.get(x.id, 0), abs(x.level - target), x.id))
    attempt_id = secrets.token_urlsafe(9)
    seed = secrets.token_hex(8)
    g.query(
        "MERGE (l:Learner {uid:$uid}) CREATE (l)-[:TOOK]->(:QuizAttempt {id:$id, uid:$uid, subtopic_id:$sid, "
        "qid:$qid, level:$lvl, seed:$seed, hints_used:0, started_ms:$now})",
        {"uid": uid, "id": attempt_id, "sid": subtopic_id, "qid": q.id, "lvl": q.level, "seed": seed,
         "now": state.now_ms()})
    order = bank.shuffled_order(seed, len(q.options))
    return PublicQuestion(attempt_id=attempt_id, subtopic_id=subtopic_id, level=q.level, stem=q.stem,
                          options=[q.options[i] for i in order], hints_available=len(q.hints))


def _load(uid: str, attempt_id: str, g: Any) -> dict:
    res = rows(g,
        "MATCH (a:QuizAttempt {id:$id, uid:$uid}) RETURN a.subtopic_id, a.qid, a.level, a.seed, a.hints_used, "
        "a.answered_ms, a.correct, a.credit, a.correct_pos", {"id": attempt_id, "uid": uid})
    if not res:
        raise QuizError("Unknown attempt", 404)
    r = res[0]
    return {"sid": r[0], "qid": r[1], "level": int(r[2]), "seed": r[3], "hints": int(r[4]),
            "answered": r[5], "correct": r[6], "credit": r[7], "correct_pos": r[8]}


def hint(uid: str, attempt_id: str, *, graph: Any | None = None) -> dict:
    g = graph or student_graph()
    a = _load(uid, attempt_id, g)
    if a["answered"] is not None:
        raise QuizError("Already answered", 409)
    q = bank.find_question(a["sid"], a["qid"])
    if q is None or a["hints"] >= len(q.hints):
        raise QuizError("No more hints", 409)
    res = rows(g,
        "MATCH (a:QuizAttempt {id:$id, uid:$uid}) WHERE a.answered_ms IS NULL AND a.hints_used = $n "
        "SET a.hints_used = a.hints_used + 1 RETURN a.hints_used",
        {"id": attempt_id, "uid": uid, "n": a["hints"]}, write=True)
    if not res:  # concurrent hint request already advanced the counter
        a = _load(uid, attempt_id, g)
        return {"hint": q.hints[a["hints"] - 1], "hints_used": a["hints"]}
    return {"hint": q.hints[a["hints"]], "hints_used": a["hints"] + 1}


def answer(uid: str, attempt_id: str, selected_position: int, *, graph: Any | None = None) -> AnswerResult:
    g = graph or student_graph()
    a = _load(uid, attempt_id, g)
    q = bank.find_question(a["sid"], a["qid"])
    if q is None:
        raise QuizError("Question no longer available", 410)
    order = bank.shuffled_order(a["seed"], len(q.options))
    correct_pos = order.index(q.answer)
    if a["answered"] is not None:  # idempotent replay
        belief = state.get_beliefs(uid, graph=g).get(a["sid"], {"mean": 0.5, "status": "unseen"})
        return AnswerResult(correct=bool(a["correct"]), correct_position=int(a["correct_pos"]),
                            explanation=q.explanation, hints_used=a["hints"], credit=float(a["credit"]),
                            mean=belief["mean"], status=belief["status"], repeated=True)
    if not 0 <= selected_position < len(q.options):
        raise QuizError("Invalid option")
    is_correct = selected_position == correct_pos
    cr = credit(is_correct, a["hints"])
    marked = rows(g,
        "MATCH (a:QuizAttempt {id:$id, uid:$uid}) WHERE a.answered_ms IS NULL "
        "SET a.answered_ms=$now, a.selected=$sel, a.correct=$ok, a.credit=$cr, a.correct_pos=$cp RETURN a.id",
        {"id": attempt_id, "uid": uid, "now": state.now_ms(), "sel": selected_position, "ok": is_correct,
         "cr": cr, "cp": correct_pos}, write=True)
    if not marked:  # lost the race to a concurrent submit
        return answer(uid, attempt_id, selected_position, graph=g)
    from app.learn.mastery import LEVEL_WEIGHT
    b: Belief = state.apply_evidence(uid, a["sid"], LEVEL_WEIGHT[a["level"]], cr, graph=g)
    return AnswerResult(correct=is_correct, correct_position=correct_pos, explanation=q.explanation,
                        hints_used=a["hints"], credit=cr, mean=round(b.mean, 3), status=b.status)
