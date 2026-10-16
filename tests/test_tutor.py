import asyncio
from types import SimpleNamespace as NS

from fastapi.testclient import TestClient

from app.auth import serializer
from app.learn import state
from app.learn.profile import Profile, get_profile, save_profile
from app.main import app
from app.rag import answer, chunks, embed, retrieve

KKT = "math-optimization-kkt-and-constrained-optimization"
LP = "math-optimization-linear-programming-simplex-duality"


def go(c):
    return asyncio.run(c)


def test_chunking_keeps_sections_and_ids():
    md = "---\nid: x\n---\n\n# T\n\nintro para.\n\n## Study sequence\n\nstudy.\n\n## Lesson: a\n\n" + ("word " * 300) + "\n\n" + ("more " * 300)
    cs = chunks.split_subtopic("x", md)
    assert [c.section for c in cs][0] == "T" and any(c.section == "Study sequence" for c in cs)
    assert all(len(c.text) < 2000 for c in cs) and len({c.id for c in cs}) == len(cs)


def test_graph_has_chunks_for_every_subtopic(db):
    from app.kg.connection import kg_graph, rows
    n = rows(kg_graph(), "MATCH (s:Subtopic) WHERE NOT (s)-[:HAS_CHUNK]->() RETURN count(s)")[0][0]
    assert n == 0


def test_retrieval_finds_topic_and_typos(db):
    r = retrieve.retrieve("what are the KKT conditions")
    assert r.covered and r.focus["id"] == KKT
    assert retrieve.retrieve("explain compleentary slackness").focus["id"] == KKT
    assert not retrieve.retrieve("capital of france").covered


def test_answer_is_cited_and_personalized(db, uid):
    state.seed_beliefs(uid, [LP])
    a = go(answer.ask(uid, "what are the KKT conditions?"))
    assert a.mode == "extractive" and a.covered and a.citations
    assert all(f"[{c.n}]" in a.answer for c in a.citations[:1])
    assert LP not in [w.subtopic_id for w in a.weak_prerequisites]      # mastered prerequisite is not flagged
    b = go(answer.ask("fresh-" + uid, "what are the KKT conditions?"))
    assert LP in [w.subtopic_id for w in b.weak_prerequisites]          # unseen prerequisite is flagged


def test_level_follows_mastery_over_profile(db, uid):
    save_profile(uid, Profile(level="beginner"))
    assert go(answer.ask(uid, "what are the KKT conditions?")).level_used == "beginner"
    state.seed_beliefs(uid, [KKT])
    assert go(answer.ask(uid, "what are the KKT conditions?")).level_used == "advanced"


def test_not_covered_does_not_guess(db, uid):
    a = go(answer.ask(uid, "who won the world cup"))
    assert not a.covered and a.mode == "not_covered" and not a.citations


def test_llm_answer_must_cite_real_passages(db, uid, monkeypatch):
    monkeypatch.setattr(answer, "settings", NS(ai_enabled=True, ai_model="m", ai_fallback_models=(), tutor_max_tokens=100, agent_timeout_seconds=5))

    async def good(**kw):
        return NS(choices=[NS(message=NS(content="KKT adds multiplier conditions [1]."))])

    async def bad(**kw):
        return NS(choices=[NS(message=NS(content="Totally made up [99]."))])
    a = go(answer.ask(uid, "what are the KKT conditions?", completion=good))
    assert a.mode == "llm" and "[1]" in a.answer
    b = go(answer.ask(uid, "what are the KKT conditions?", completion=bad))
    assert b.mode == "extractive" and "not grounded" in (b.fallback_reason or "")


def test_profile_self_report_is_provisional(db, uid):
    save_profile(uid, Profile(level="advanced", known_topic_ids=["math-single-variable-calculus"]))
    p = get_profile(uid)
    assert p.onboarded and p.known_topic_ids == ["math-single-variable-calculus"]
    beliefs = state.get_beliefs(uid)
    assert beliefs and all(v["status"] != "mastered" for v in beliefs.values())  # claims need quiz confirmation


def test_embeddings_fusion(db):
    calls = {}

    async def fake(texts):
        calls["n"] = calls.get("n", 0) + len(texts)
        return [[float(len(t) % 7), 1.0, 0.5] for t in texts]
    n = go(embed.embed_all_chunks(fake))
    assert n > 0 and go(embed.embed_all_chunks(fake)) == 0   # idempotent
    r = retrieve.retrieve("kkt conditions", query_embedding=[1.0, 1.0, 0.5])
    assert r.method == "bm25+embeddings" and r.focus
    from app.kg.connection import kg_graph
    kg_graph().query("MATCH (c:Chunk) REMOVE c.embedding"); retrieve.reset_index()


def test_http_tutor_and_profile(db, uid):
    c = TestClient(app)
    c.cookies.set("study_session", serializer.dumps({"uid": uid, "name": "T", "email": ""}))
    assert TestClient(app).post("/api/tutor/ask", json={"question": "kkt"}).status_code == 401
    r = c.post("/api/tutor/ask", json={"question": "What is a gradient descent step?"}).json()
    assert r["covered"] and r["citations"]
    assert c.post("/api/profile", json={"level": "beginner", "hours_per_week": 3}).json()["onboarded"]
    assert c.get("/api/profile").json()["level"] == "beginner"
    assert c.post("/api/profile", json={"level": "wizard"}).status_code == 422
    assert c.get("/tutor").status_code == 200
