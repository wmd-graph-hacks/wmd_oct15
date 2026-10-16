import asyncio
from pathlib import Path

from app.agent.models import AgentRequest
from app.agent.runner import run_agent
from app.kg import queries as q
from app.kg.connection import kg_graph, rows
from app.kg.loader import ARTIFACTS_ROOT
from app.kg.parse import discover_subjects, load_curriculum
from app.rag import answer
from test_http import client_for

QM = "physics-quantum-mechanics-core-concepts"
CM = "physics-classical-mechanics-core-concepts"
EXPECTED = {"artificial-intelligence-and-machine-learning", "backend-engineering", "biology", "chemistry",
            "computer-science-foundations", "cybersecurity", "devops-and-cloud", "mathematics", "physics"}


def go(c):
    return asyncio.run(c)


def test_all_subjects_discovered_and_loaded(db):
    assert {d.name for d in discover_subjects(ARTIFACTS_ROOT)} == EXPECTED
    loaded = {s["subject"]: s for s in q.list_subjects()}
    assert set(loaded) == EXPECTED
    assert loaded["mathematics"]["thin"] is False and loaded["mathematics"]["authored_edges"] == 92
    assert loaded["physics"]["thin"] is True and loaded["physics"]["authored_edges"] == 0
    assert loaded["physics"]["inferred_edges"] > 0


def test_ids_are_unique_across_subjects_and_nothing_crosses():
    ids = [s.id for d in discover_subjects(ARTIFACTS_ROOT) for s in load_curriculum(d).subtopics]
    assert len(ids) == len(set(ids))
    cross = rows(kg_graph(), "MATCH (a:Subtopic)-[:PREREQUISITE_OF]->(b:Subtopic) WHERE a.subject<>b.subject RETURN count(*)")
    assert cross[0][0] == 0


def test_flat_subject_gets_inferred_sequence_edges():
    cur = load_curriculum(ARTIFACTS_ROOT / "physics")
    assert {e["strength"] for e in cur.edges} == {"sequence"}
    assert len(cur.subtopics) == len(cur.topics) == 12


def test_boilerplate_chunks_are_dropped(db):
    n = rows(kg_graph(), "MATCH (c:Chunk {subject:'physics'}) RETURN count(c)")[0][0]
    assert n == 12  # only the topic-specific scope paragraph survives per lesson


def test_find_topics_is_scoped(db):
    assert q.find_topics("quantum", subject="mathematics")["matches"] == [] or all(
        m["id"].startswith("math-") for m in q.find_topics("quantum", subject="mathematics")["matches"])
    hits = q.find_topics("quantum mechanics", subject="physics")["matches"]
    assert hits and hits[0]["id"] == QM
    assert all(m["id"].startswith("physics-") for m in hits)


def test_agent_on_flat_subject_is_honest_about_inferred_order(db, uid):
    run = go(run_agent(uid, AgentRequest(goal="quantum mechanics", subject="physics"), use_llm=False))
    assert run.status == "proposed" and run.proposal_id
    assert QM in run.highlight["targets"] and CM in run.highlight["needed"]
    assert "inferred" in run.explanation
    assert all(i.startswith("physics-") for i in run.highlight["needed"])
    assert set(run.cited_ids) <= {i for s in run.steps for i in s.evidence_ids}


def test_tutor_is_subject_scoped(db, uid):
    ok = go(answer.ask(uid, "What is the Pauli exclusion principle?", subject="physics"))
    assert ok.covered and ok.focus_subtopic_id == QM
    no = go(answer.ask(uid, "What is the Pauli exclusion principle?", subject="mathematics"))
    assert not no.covered


def test_api_subjects_and_graph(db, uid):
    c = client_for(uid)
    subj = {s["subject"]: s for s in c.get("/api/agent/subjects").json()["subjects"]}
    assert set(subj) == EXPECTED and subj["biology"]["thin"]
    assert subj["mathematics"]["with_quiz"] > 0 and subj["physics"]["example_goal"].startswith("I want to learn")
    g = c.get("/api/agent/graph?subject=physics").json()
    assert len(g["nodes"]) == 12 and all(e["inferred"] for e in g["edges"])
    assert all(not n["title"].endswith("study lesson") for n in g["nodes"])
    assert c.get("/api/agent/graph?subject=nope").status_code == 404
    assert c.get("/api/agent/graph").json()["subject"] == "mathematics"


def test_quiz_bank_is_per_subject(db, uid):
    from app.learn import bank, quiz
    assert bank.questions_for(QM) and bank.questions_for("math-optimization-kkt-and-constrained-optimization")
    assert not bank.questions_for("biology-biochemistry-core-concepts")
    q = quiz.start(uid, QM)
    assert q.subtopic_id == QM
    c = client_for(uid)
    subj = {s["subject"]: s for s in c.get("/api/agent/subjects").json()["subjects"]}
    assert subj["physics"]["with_quiz"] == 3 and subj["biology"]["with_quiz"] == 0
