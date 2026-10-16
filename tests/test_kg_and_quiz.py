from app.kg import queries as q
from app.kg.loader import ARTIFACTS_ROOT
from app.kg.parse import load_curriculum
from app.learn import bank, quiz, state
from app.learn.mastery import Belief

KKT = "math-optimization-kkt-and-constrained-optimization"
LIM = "math-single-variable-calculus-limits-and-continuity"


def test_curriculum_counts():
    cur = load_curriculum(ARTIFACTS_ROOT / "mathematics")
    assert (len(cur.topics), len(cur.subtopics)) == (15, 84)
    assert any(e["derived"] for e in cur.edges)


def test_closure_cuts_at_mastered(db):
    full = {n["id"] for n in q.prerequisite_closure([KKT], [])}
    cut = {n["id"] for n in q.prerequisite_closure([KKT], [LIM])}
    assert KKT in full and LIM in full
    assert LIM not in cut and KKT in cut
    assert len(cut) < len(full)


def test_order_respects_prereqs(db):
    order = [n["id"] for n in q.order_by_dependency(q.prerequisite_closure([KKT], []))]
    assert order.index(LIM) < order.index(KKT)


def test_frontier_and_path(db):
    assert KKT not in {n["id"] for n in q.frontier([])}
    path = q.explain_path(LIM, KKT)
    assert path[0] == LIM and path[-1] == KKT


def test_bank_valid_against_graph(db):
    for sid, qs in bank.load_bank().items():
        assert q.get_subtopic(sid), sid
        assert len(qs) >= 3


def test_mastery_math():
    b = Belief()
    for _ in range(3):
        b = b.updated(3, 1.0)
    assert b.status == "mastered"
    assert Belief().status == "unseen"
    assert Belief().updated(2, 0.0).updated(2, 0.0).status == "gap"


def test_quiz_flow_no_key_leak_and_idempotent(db, uid):
    pub = quiz.start(uid, LIM)
    assert "answer" not in pub.model_dump() and "explanation" not in pub.model_dump()
    first = quiz.answer(uid, pub.attempt_id, 0)
    again = quiz.answer(uid, pub.attempt_id, 1)
    assert again.repeated and again.correct == first.correct
    beliefs = state.get_beliefs(uid)
    assert beliefs[LIM]["n_attempts"] == 1


def test_hints_reduce_credit_and_cross_user_isolated(db, uid):
    pub = quiz.start(uid, LIM)
    h = quiz.hint(uid, pub.attempt_id)
    assert h["hints_used"] == 1
    correct_pos = None
    for pos in range(len(pub.options)):
        pass
    import pytest
    with pytest.raises(quiz.QuizError):
        quiz.hint("someone-else", pub.attempt_id)
    res = quiz.answer(uid, pub.attempt_id, 0)
    assert res.hints_used == 1 and res.credit <= 0.75
