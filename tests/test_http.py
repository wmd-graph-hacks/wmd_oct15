from fastapi.testclient import TestClient

from app.auth import serializer
from app.main import app


def client_for(uid: str) -> TestClient:
    c = TestClient(app)
    c.cookies.set("study_session", serializer.dumps({"uid": uid, "name": "T", "email": ""}))
    return c


def test_requires_auth(db):
    r = TestClient(app).post("/api/agent/runs", json={"goal": "kkt"})
    assert r.status_code == 401


def test_full_flow_and_isolation(db, uid):
    c = client_for(uid)
    run = c.post("/api/agent/runs", json={"goal": "KKT constrained optimization", "hours_per_week": 6, "weeks_available": 40}).json()
    assert run["status"] == "proposed" and run["proposal_id"]
    pid = run["proposal_id"]
    assert client_for("someone-else").get(f"/api/agent/proposals/{pid}").status_code == 404
    assert client_for("someone-else").post(f"/api/agent/proposals/{pid}/approve").status_code == 400
    assert c.post(f"/api/agent/proposals/{pid}/approve").json()["status"] == "committed"
    assert c.get(f"/api/agent/proposals/{pid}").json()["status"] == "committed"
    assert c.get(f"/api/agent/runs/{run['id']}").status_code == 200
    g = c.get("/api/agent/graph").json()
    assert len(g["nodes"]) == 84 and len(g["edges"]) == 92


def test_quiz_http_never_leaks_key(db, uid):
    c = client_for(uid)
    sid = "math-single-variable-calculus-limits-and-continuity"
    q = c.post(f"/api/quiz/{sid}/start").json()
    assert set(q) == {"attempt_id", "subtopic_id", "level", "stem", "options", "hints_available"}
    assert c.post(f"/api/quiz/attempts/{q['attempt_id']}/answer", json={"position": 9}).status_code == 400
    r = c.post(f"/api/quiz/attempts/{q['attempt_id']}/answer", json={"position": 0}).json()
    assert "correct" in r
    assert client_for("x").post(f"/api/quiz/attempts/{q['attempt_id']}/hint").status_code == 404


def test_pages_render(db, uid):
    c = client_for(uid)
    assert c.get("/agent").status_code == 200
    assert c.get("/quiz/math-optimization-kkt-and-constrained-optimization").status_code == 200
    assert c.get("/quiz/nope").status_code == 404
