from datetime import UTC, datetime
from threading import Lock
from uuid import uuid4

from app.graph.connection import graph_connection
from app.config import settings

_seed_lock = Lock()
_seeded_graphs: set[str] = set()

ASSESSMENT_QUESTIONS = {
    "fractions": ("Which is equal to 3/4 + 1/2?", ["5/4", "4/6", "1/4"], "A"),
    "ratios": ("A recipe uses 2 cups flour for 3 cups water. How much flour for 6 cups water?", ["3 cups", "4 cups", "6 cups"], "B"),
    "linear_equations": ("Solve 2x + 3 = 11.", ["x = 4", "x = 7", "x = 14"], "A"),
    "coordinate_plane": ("Which quadrant contains the point (-2, 3)?", ["I", "II", "IV"], "B"),
    "functions": ("If f(x) = 2x + 1, what is f(3)?", ["5", "6", "7"], "C"),
    "polynomials": ("What is the degree of 4x³ - 2x + 1?", ["1", "2", "3"], "C"),
    "exponents": ("Simplify 2³ × 2².", ["2⁵", "4⁵", "2⁶"], "A"),
    "factoring": ("Factor x² + 5x + 6.", ["(x + 2)(x + 3)", "(x + 1)(x + 6)", "(x - 2)(x - 3)"], "A"),
    "quadratics": ("Which are the solutions of x² - 5x + 6 = 0?", ["1 and 6", "2 and 3", "-2 and -3"], "B"),
    "sequences": ("What is the next term: 2, 5, 8, ...?", ["10", "11", "12"], "B"),
    "limits": ("What is lim(x→2) (x + 3)?", ["3", "5", "Does not exist"], "B"),
    "derivatives": ("What is the derivative of x²?", ["x", "2x", "2"], "B"),
}


def _rows(query: str, params: dict | None = None) -> list:
    return graph_connection().query(query, params=params or {}).result_set


def health() -> bool:
    try:
        _rows("RETURN 1")
        return True
    except Exception:
        return False


def seed_course() -> None:
    """Seed the static demo corpus once per process/graph, retrying on failure."""
    with _seed_lock:
        if settings.graph_name in _seeded_graphs:
            return
        _seed_course_graph()
        _seeded_graphs.add(settings.graph_name)


def _seed_course_graph() -> None:
    graph = graph_connection()
    topics = [
        ("fractions", "Fractions and arithmetic", 1, 20),
        ("ratios", "Ratios and proportions", 2, 20),
        ("linear_equations", "Linear equations", 3, 25),
        ("coordinate_plane", "Coordinate plane", 4, 20),
        ("functions", "Functions", 5, 30),
        ("polynomials", "Polynomials", 6, 25),
        ("exponents", "Exponents and radicals", 7, 25),
        ("factoring", "Factoring expressions", 8, 30),
        ("quadratics", "Quadratic equations", 9, 35),
        ("sequences", "Sequences and series basics", 10, 30),
        ("limits", "Limits", 11, 35),
        ("derivatives", "Derivatives", 12, 40),
    ]
    graph.query(
        "MERGE (c:Course {id: $id}) SET c.title=$title, c.description=$description, c.source=$source",
        params={"id": "foundational_math", "title": "Foundational Mathematics", "description": "A short path from arithmetic foundations to introductory calculus.", "source": "Hand-authored demo syllabus"},
    )
    for topic_id, title, order, minutes in topics:
        graph.query(
            "MERGE (t:Topic {id: $id}) SET t.title=$title, t.order=$order, t.estimated_minutes=$minutes, t.exam_weight=$weight "
            "WITH t MATCH (c:Course {id: $course_id}) MERGE (c)-[:CONTAINS]->(t)",
            params={"id": topic_id, "title": title, "order": order, "minutes": minutes, "weight": 1.0, "course_id": "foundational_math"},
        )
        graph.query(
            "MERGE (a:Assessment {id:$assessment_id}) SET a.title=$title, a.max_score=$max_score, "
            "a.prompt=$prompt, a.options=$options, a.correct_answer=$answer, a.source=$source "
            "WITH a MATCH (t:Topic {id:$topic_id}) MERGE (a)-[:CHECKS]->(t)",
            params={"assessment_id": f"quick_check_{topic_id}", "title": f"{title} quick check", "max_score": 5,
                    "prompt": ASSESSMENT_QUESTIONS[topic_id][0], "options": ASSESSMENT_QUESTIONS[topic_id][1],
                    "answer": ASSESSMENT_QUESTIONS[topic_id][2], "source": "Hand-authored demo diagnostic", "topic_id": topic_id},
        )
    edges = [("fractions", "ratios"), ("ratios", "linear_equations"), ("linear_equations", "functions"),
             ("coordinate_plane", "functions"), ("functions", "polynomials"), ("exponents", "polynomials"),
             ("polynomials", "factoring"), ("factoring", "quadratics"), ("functions", "sequences"),
             ("functions", "limits"), ("limits", "derivatives"), ("functions", "derivatives")]
    for prerequisite, next_topic in edges:
        graph.query(
            "MATCH (a:Topic {id:$a}), (b:Topic {id:$b}) MERGE (a)-[:PREREQUISITE_OF]->(b)",
            params={"a": prerequisite, "b": next_topic},
        )
    resources = [
        ("fractions_practice", "Fractions: worked examples and practice", "https://www.khanacademy.org/math/arithmetic/fraction-arithmetic", "fractions"),
        ("ratio_practice", "Ratios and proportions", "https://www.khanacademy.org/math/pre-algebra/pre-algebra-ratios-rates", "ratios"),
        ("functions_intro", "Understanding functions", "https://www.khanacademy.org/math/algebra", "functions"),
        ("limits_intro", "Introduction to limits", "https://www.khanacademy.org/math/ap-calculus-ab/ab-limits-new", "limits"),
        ("derivatives_intro", "Derivative rules and meaning", "https://www.khanacademy.org/math/ap-calculus-ab/ab-differentiation-1-new", "derivatives"),
    ]
    for resource_id, title, url, topic_id in resources:
        graph.query(
            "MERGE (r:Resource {id:$id}) SET r.title=$title, r.url=$url, r.kind=$kind, r.source=$source, r.reference=$reference "
            "WITH r MATCH (t:Topic {id:$topic}) MERGE (r)-[:TEACHES]->(t)",
            params={"id": resource_id, "title": title, "url": url, "kind": "learning resource", "source": "Khan Academy", "reference": title, "topic": topic_id},
        )


def ensure_learner(uid: str, display_name: str = "Learner") -> None:
    _rows("MERGE (l:Learner {uid:$uid}) ON CREATE SET l.display_name=$name, l.created_at=$now", {"uid": uid, "name": display_name, "now": datetime.now(UTC).isoformat()})


def get_course() -> dict:
    rows = _rows(
        "MATCH (c:Course {id:$course_id})-[:CONTAINS]->(t:Topic) "
        "RETURN c.id, c.title, c.description, t.id, t.title, t.order, t.estimated_minutes ORDER BY t.order",
        {"course_id": "foundational_math"},
    )
    if not rows:
        raise RuntimeError("Foundational Mathematics is not seeded. Run the seed command.")
    return {"id": rows[0][0], "title": rows[0][1], "description": rows[0][2], "topics": [
        {"id": row[3], "title": row[4], "order": row[5], "minutes": row[6]} for row in rows
    ]}


def save_learner_preferences(uid: str, exam_date: str, minutes_per_day: int, exam_topic: str) -> None:
    _rows(
        "MATCH (l:Learner {uid:$uid}) SET l.exam_date=$date, l.minutes_per_day=$minutes, l.exam_topic=$topic",
        {"uid": uid, "date": exam_date, "minutes": minutes_per_day, "topic": exam_topic},
    )


def get_assessment(topic_id: str) -> dict | None:
    rows = _rows(
        "MATCH (a:Assessment)-[:CHECKS]->(t:Topic {id:$topic_id}) "
        "RETURN a.id, a.title, a.prompt, a.options, a.max_score, t.id, t.title, a.source",
        {"topic_id": topic_id},
    )
    if not rows:
        return None
    row = rows[0]
    return {"assessment_id": row[0], "title": row[1], "question": row[2], "options": row[3],
            "max_score": row[4], "topic_id": row[5], "topic": row[6], "source": row[7]}


def create_attempt(uid: str, topic_id: str, score: int, max_score: int = 5, assessment_id: str | None = None) -> None:
    attempt_id = str(uuid4())
    _rows(
        "MATCH (l:Learner {uid:$uid}), (t:Topic {id:$topic}), (a:Assessment)-[:CHECKS]->(t) "
        "WHERE $assessment_id IS NULL OR a.id=$assessment_id "
        "CREATE (x:Attempt {id:$id, score:$score, max_score:$max_score, attempted_at:$now}) "
        "CREATE (l)-[:MADE_ATTEMPT]->(x)-[:ABOUT]->(t) CREATE (x)-[:USES_ASSESSMENT]->(a) "
        "MERGE (k:LearnerTopic {id:$knowledge_id}) ON CREATE SET k.mastery=0.0, k.attempt_count=0 "
        "WITH l, t, k, CASE WHEN $max_score > 0 THEN toFloat($score)/$max_score ELSE 0.0 END AS result "
        "SET k.mastery=(k.mastery*k.attempt_count+result)/(k.attempt_count+1), "
        "k.attempt_count=k.attempt_count+1, k.last_assessed_at=$now "
        "MERGE (l)-[:HAS_KNOWLEDGE]->(k) MERGE (k)-[:ABOUT]->(t)",
        {"uid": uid, "topic": topic_id, "id": attempt_id, "score": score, "max_score": max_score,
         "assessment_id": assessment_id, "now": datetime.now(UTC).isoformat(), "knowledge_id": f"{uid}:{topic_id}"},
    )


def submit_assessment(uid: str, assessment_id: str, answer: str) -> dict | None:
    rows = _rows(
        "MATCH (a:Assessment {id:$assessment_id})-[:CHECKS]->(t:Topic) "
        "RETURN a.correct_answer, a.max_score, t.id, t.title",
        {"assessment_id": assessment_id},
    )
    if not rows:
        return None
    correct_answer, max_score, topic_id, title = rows[0]
    score = max_score if answer.strip().upper() == correct_answer else 0
    create_attempt(uid, topic_id, score, max_score, assessment_id)
    knowledge = learner_knowledge(uid).get(topic_id, {})
    return {"topic_id": topic_id, "topic": title, "score": score, "max_score": max_score,
            "is_correct": score == max_score, "knowledge": knowledge}


def latest_attempts(uid: str) -> dict[str, dict]:
    rows = _rows(
        "MATCH (l:Learner {uid:$uid})-[:MADE_ATTEMPT]->(a:Attempt)-[:ABOUT]->(t:Topic) "
        "RETURN t.id, t.title, a.score, a.max_score, a.attempted_at ORDER BY a.attempted_at DESC",
        {"uid": uid},
    )
    latest = {}
    for row in rows:
        latest.setdefault(row[0], {"title": row[1], "score": row[2], "max_score": row[3], "at": row[4]})
    return latest


def learner_knowledge(uid: str) -> dict[str, dict]:
    rows = _rows(
        "MATCH (l:Learner {uid:$uid})-[:HAS_KNOWLEDGE]->(k:LearnerTopic)-[:ABOUT]->(t:Topic) "
        "RETURN t.id, k.mastery, k.attempt_count, k.last_assessed_at",
        {"uid": uid},
    )
    return {row[0]: {"mastery": row[1], "attempt_count": row[2], "last_assessed_at": row[3]} for row in rows}


def plan(uid: str, limit: int = 3) -> list[dict]:
    # FalkorDB supplies prerequisite ancestry; the compact LearnerTopic aggregate drives readiness.
    preferences = learner_preferences(uid)
    target_id = preferences.get("exam_topic") or "derivatives"
    rows = _rows(
        "MATCH (c:Course {id:$course_id})-[:CONTAINS]->(target:Topic) "
        "WHERE target.id=$target_id "
        "MATCH path=(pre:Topic)-[:PREREQUISITE_OF*0..]->(target) "
        "WITH pre, target, length(path) AS distance, path "
        "OPTIONAL MATCH (r:Resource)-[:TEACHES]->(pre) "
        "RETURN pre.id, pre.title, pre.estimated_minutes, target.title, distance, r.id, r.title, r.url, r.source, r.reference, "
        "pre.order, target.order, reduce(names=[], n IN nodes(path) | names + [n.title]) AS path_titles, "
        "reduce(ids=[], n IN nodes(path) | ids + [n.id]) AS path_topic_ids "
        "ORDER BY pre.order, distance DESC",
        {"course_id": "foundational_math", "target_id": target_id},
    )
    attempts = latest_attempts(uid)
    knowledge = learner_knowledge(uid)
    completed = completed_topics(uid)
    candidates = {}
    for row in rows:
        topic_id = row[0]
        evidence = attempts.get(topic_id)
        profile = knowledge.get(topic_id)
        ratio = profile["mastery"] if profile else None
        if ratio is not None and ratio >= 0.7:
            continue
        item = candidates.setdefault(topic_id, {
            "topic_id": topic_id, "topic": row[1], "minutes": row[2], "target": row[3],
            "distance": row[4], "resource_id": row[5], "resource": row[6], "url": row[7],
            "resource_source": row[8], "resource_reference": row[9], "order": row[10], "attempt": evidence,
            "mastery": ratio, "attempt_count": profile["attempt_count"] if profile else 0,
            "path": row[12], "path_topic_ids": row[13],
            "session_done": topic_id in completed,
        })
        item["distance"] = min(item["distance"], row[4])
    daily_budget = preferences.get("minutes_per_day") or 45
    ranked = sorted(candidates.values(), key=lambda item: (item["order"], -item["distance"], item["topic"]))
    output = []
    for item in ranked[:limit]:
        item["minutes"] = min(item["minutes"], daily_budget)
        evidence = item["attempt"]
        if evidence:
            reason = f"Your average across {item['attempt_count']} checks is {item['mastery']:.0%}; this topic is a prerequisite on the path to {item['target']}."
        elif item["session_done"]:
            reason = f"You marked this study session complete. Record a quick check to show whether this prerequisite is ready for {item['target']}."
        else:
            reason = f"There is no check recorded yet; this topic is a prerequisite on the path to {item['target']}."
        item["reason"] = reason
        output.append(item)
    return output


def save_plan(uid: str, target_id: str, recommendations: list[dict]) -> str:
    """Persist the graph-derived action plan and its resource links."""
    plan_id = str(uuid4())
    now = datetime.now(UTC).isoformat()
    items = [
        {"topic_id": item["topic_id"], "resource_id": item.get("resource_id"), "item_id": str(uuid4()),
         "rank": rank, "minutes": item["minutes"], "reason": item["reason"]}
        for rank, item in enumerate(recommendations, start=1)
    ]
    _rows(
        "MATCH (l:Learner {uid:$uid}) "
        "OPTIONAL MATCH (l)-[:HAS_PLAN]->(old:StudyPlan {status:$active}) "
        "WITH l, collect(old) AS old_plans "
        "FOREACH (old IN old_plans | SET old.status=$superseded) "
        "CREATE (p:StudyPlan {id:$plan_id, course_id:$course_id, target_topic_id:$target_id, status:$active, generated_at:$now}) "
        "CREATE (l)-[:HAS_PLAN]->(p) WITH p "
        "UNWIND $items AS item "
        "MATCH (t:Topic {id:item.topic_id}) OPTIONAL MATCH (r:Resource {id:item.resource_id}) "
        "CREATE (i:PlanItem {id:item.item_id, rank:item.rank, minutes:item.minutes, reason:item.reason}) "
        "CREATE (p)-[:INCLUDES]->(i)-[:FOCUSES_ON]->(t) "
        "FOREACH (resource IN CASE WHEN r IS NULL THEN [] ELSE [r] END | CREATE (i)-[:USES]->(resource))",
        {"uid": uid, "active": "active", "superseded": "superseded", "plan_id": plan_id,
         "course_id": "foundational_math", "target_id": target_id, "now": now, "items": items},
    )
    return plan_id


def get_saved_plan(uid: str, plan_id: str) -> dict | None:
    rows = _rows(
        "MATCH (l:Learner {uid:$uid})-[:HAS_PLAN]->(p:StudyPlan {id:$plan_id}) "
        "OPTIONAL MATCH (p)-[:INCLUDES]->(i:PlanItem)-[:FOCUSES_ON]->(t:Topic) "
        "OPTIONAL MATCH (i)-[:USES]->(r:Resource) "
        "RETURN p.id, p.course_id, p.target_topic_id, p.status, p.generated_at, "
        "i.rank, i.minutes, i.reason, t.id, t.title, r.title, r.source, r.reference, r.url "
        "ORDER BY i.rank",
        {"uid": uid, "plan_id": plan_id},
    )
    if not rows:
        return None
    first = rows[0]
    items = []
    for row in rows:
        if row[8] is None:
            continue
        items.append({
            "rank": row[5], "minutes": row[6], "reason": row[7],
            "topic_id": row[8], "topic": row[9],
            "resource": {"title": row[10], "source": row[11], "reference": row[12], "url": row[13]} if row[10] else None,
        })
    return {"plan_id": first[0], "course_id": first[1], "target_topic": first[2], "status": first[3], "generated_at": first[4], "items": items}


def learner_preferences(uid: str) -> dict:
    rows = _rows("MATCH (l:Learner {uid:$uid}) RETURN l.exam_date, l.minutes_per_day, l.exam_topic", {"uid": uid})
    if not rows:
        return {}
    return {"exam_date": rows[0][0], "minutes_per_day": rows[0][1], "exam_topic": rows[0][2]}


def completed_topics(uid: str) -> set[str]:
    rows = _rows(
        "MATCH (l:Learner {uid:$uid})-[:HAS_SESSION]->(s:StudySession {status:$status})-[:FOCUSES_ON]->(t:Topic) "
        "RETURN DISTINCT t.id",
        {"uid": uid, "status": "completed"},
    )
    return {row[0] for row in rows}


def record_session(uid: str, topic_id: str) -> None:
    _rows(
        "MATCH (l:Learner {uid:$uid}), (t:Topic {id:$topic}) "
        "CREATE (s:StudySession {id:$id, status:$status, planned_minutes:t.estimated_minutes, completed_at:$now}) "
        "CREATE (l)-[:HAS_SESSION]->(s)-[:FOCUSES_ON]->(t)",
        {"uid": uid, "topic": topic_id, "id": str(uuid4()), "status": "completed", "now": datetime.now(UTC).isoformat()},
    )


def reset_demo() -> None:
    _rows(
        "MATCH (l:Learner {uid:$uid})-[r:MADE_ATTEMPT]->(a:Attempt) "
        "OPTIONAL MATCH (a)-[ar]->() DELETE r, ar, a",
        {"uid": "demo-nimesh"},
    )
    _rows(
        "MATCH (l:Learner {uid:$uid})-[r:HAS_SESSION]->(s:StudySession) "
        "OPTIONAL MATCH (s)-[sr]->() DELETE r, sr, s",
        {"uid": "demo-nimesh"},
    )
    _rows("MATCH (l:Learner {uid:$uid}) REMOVE l.exam_date, l.minutes_per_day, l.exam_topic", {"uid": "demo-nimesh"})
    _rows(
        "MATCH (l:Learner {uid:$uid})-[r:HAS_KNOWLEDGE]->(k:LearnerTopic) "
        "OPTIONAL MATCH (k)-[kr]->() DELETE r, kr, k",
        {"uid": "demo-nimesh"},
    )
    _rows(
        "MATCH (l:Learner {uid:$uid})-[r:HAS_PLAN]->(p:StudyPlan) "
        "OPTIONAL MATCH (p)-[pr]->(i:PlanItem) OPTIONAL MATCH (i)-[ir]->() "
        "DELETE r, pr, ir, i, p",
        {"uid": "demo-nimesh"},
    )
