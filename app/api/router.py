from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from starlette.concurrency import run_in_threadpool

from app.auth import current_user
from app.api.schemas import AssessmentAnswer, AttemptInput, PlanPreferences, SessionInput
from app.graph import repository
from app.services.roadmap import personalize_retrieved_roadmap, retrieve_roadmap

router = APIRouter(prefix="/api/v1", tags=["planner API"])
VALID_EXAM_TOPICS = {"quadratics", "limits", "derivatives"}


def api_user(request: Request) -> dict:
    """Use the same verified identity as the UI, with JSON-friendly auth errors."""
    try:
        return current_user(request)
    except FastAPIHTTPException as exc:
        if exc.status_code == 303:
            raise HTTPException(status_code=401, detail="Sign in required") from exc
        raise


def graph_call(operation):
    try:
        return operation()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Planner storage is unavailable") from exc


@router.get("/health")
def api_health():
    connected = repository.health()
    return {"status": "ok" if connected else "degraded", "graph": "ok" if connected else "unavailable"}


@router.get("/courses/{course_id}")
def get_course(course_id: str):
    if course_id != "foundational_math":
        raise HTTPException(status_code=404, detail="Course not found")
    def read():
        repository.seed_course()
        return repository.get_course()

    course = graph_call(read)
    return course


@router.get("/plan")
async def get_plan(user: dict = Depends(api_user)):
    result = await run_in_threadpool(graph_call, lambda: retrieve_roadmap(user["uid"], user.get("name", "Learner")))
    return await personalize_retrieved_roadmap(result)


def preview_roadmap_sync(user: dict):
    """Build the graph response before the optional async AI step."""
    return retrieve_roadmap(user["uid"], user.get("name", "Learner"))


@router.post("/plan/generate", status_code=201)
async def create_plan(user: dict = Depends(api_user)):
    graph_data = await run_in_threadpool(graph_call, lambda: preview_roadmap_sync(user))
    plan = await personalize_retrieved_roadmap(graph_data)
    plan_id = await run_in_threadpool(graph_call, lambda: repository.save_plan(user["uid"], plan["target_topic"], plan["recommendations"]))
    plan["plan_id"] = plan_id
    return plan


@router.get("/plans/{plan_id}")
def read_saved_plan(plan_id: str, user: dict = Depends(api_user)):
    plan = graph_call(lambda: repository.get_saved_plan(user["uid"], plan_id))
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.put("/plan/preferences")
def save_preferences(payload: PlanPreferences, user: dict = Depends(api_user)):
    if payload.exam_date < date.today():
        raise HTTPException(status_code=422, detail="exam_date cannot be in the past")
    if payload.exam_topic not in VALID_EXAM_TOPICS:
        raise HTTPException(status_code=422, detail="exam_topic must be quadratics, limits, or derivatives")

    def save():
        repository.seed_course()
        repository.ensure_learner(user["uid"], user.get("name", "Learner"))
        repository.save_learner_preferences(user["uid"], payload.exam_date.isoformat(), payload.minutes_per_day, payload.exam_topic)
        return {"preferences": repository.learner_preferences(user["uid"])}

    return graph_call(save)


@router.post("/attempts", status_code=201)
def create_attempt(payload: AttemptInput, user: dict = Depends(api_user)):
    if payload.score > payload.max_score:
        raise HTTPException(status_code=422, detail="score cannot exceed max_score")

    def save():
        repository.seed_course()
        repository.ensure_learner(user["uid"], user.get("name", "Learner"))
        repository.create_attempt(user["uid"], payload.topic_id, payload.score, payload.max_score)
        latest = repository.latest_attempts(user["uid"]).get(payload.topic_id)
        if latest is None:
            raise HTTPException(status_code=404, detail="Topic or assessment not found")
        return {"topic_id": payload.topic_id, "attempt": latest}

    return graph_call(save)


@router.get("/topics/{topic_id}/assessment")
def get_topic_assessment(topic_id: str, _: dict = Depends(api_user)):
    def read():
        repository.seed_course()
        return repository.get_assessment(topic_id)

    assessment = graph_call(read)
    if assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment


@router.post("/assessments/submit", status_code=201)
def submit_assessment(payload: AssessmentAnswer, user: dict = Depends(api_user)):
    def save():
        repository.seed_course()
        repository.ensure_learner(user["uid"], user.get("name", "Learner"))
        return repository.submit_assessment(user["uid"], payload.assessment_id, payload.answer)

    result = graph_call(save)
    if result is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return result


@router.post("/sessions/complete", status_code=201)
def complete_session(payload: SessionInput, user: dict = Depends(api_user)):
    def save():
        repository.seed_course()
        repository.ensure_learner(user["uid"], user.get("name", "Learner"))
        repository.record_session(user["uid"], payload.topic_id)
        completed = repository.completed_topics(user["uid"])
        if payload.topic_id not in completed:
            raise HTTPException(status_code=404, detail="Topic not found")
        return {"topic_id": payload.topic_id, "status": "completed"}

    return graph_call(save)
