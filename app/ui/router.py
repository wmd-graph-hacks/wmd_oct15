from datetime import date
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth import current_user, firebase_auth, make_demo_cookie
from app.config import settings
from app.graph import repository

BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=BASE_DIR / "templates")
router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"auth_mode": settings.auth_mode, "firebase_api_key": settings.firebase_api_key, "firebase_auth_domain": settings.firebase_auth_domain, "firebase_project_id": settings.firebase_project_id, "firebase_app_id": settings.firebase_app_id})


@router.post("/auth/demo")
def demo_login():
    if settings.auth_mode != "demo" or settings.app_env == "production":
        return RedirectResponse("/login", status_code=303)
    response = RedirectResponse("/", status_code=303)
    response.set_cookie("study_session", make_demo_cookie(), httponly=True, secure=settings.session_cookie_secure, samesite="lax", max_age=3600)
    return response


@router.post("/auth/session")
async def create_session(request: Request):
    if settings.auth_mode != "firebase":
        return RedirectResponse("/login", status_code=303)
    origin = request.headers.get("origin")
    if not origin or origin.removeprefix("https://").removeprefix("http://").rstrip("/") != request.url.netloc:
        return PlainTextResponse("Invalid request origin", status_code=403)
    payload = await request.json()
    if not payload.get("id_token"):
        return RedirectResponse("/login", status_code=303)
    try:
        auth = firebase_auth()
        decoded = auth.verify_id_token(payload["id_token"])
        cookie = auth.create_session_cookie(payload["id_token"], expires_in=60 * 60 * 24 * 5)
        repository.ensure_learner(decoded["uid"], decoded.get("name", "Learner"))
        response = RedirectResponse("/", status_code=303)
        response.set_cookie("study_session", cookie, httponly=True, secure=settings.session_cookie_secure, samesite="lax", max_age=60 * 60 * 24 * 5)
        return response
    except Exception:
        return RedirectResponse("/login?error=auth", status_code=303)


@router.post("/auth/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("study_session")
    return response


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    user = current_user(request)
    repository.seed_course()
    repository.ensure_learner(user["uid"], user.get("name", "Learner"))
    course = repository.get_course()
    try:
        recommendations = repository.plan(user["uid"])
    except Exception:
        recommendations = []
    attempts = repository.latest_attempts(user["uid"])
    return templates.TemplateResponse(request, "home.html", {"user": user, "course": course, "recommendations": recommendations, "attempts": attempts, "preferences": repository.learner_preferences(user["uid"]), "today": date.today().isoformat()})


@router.post("/plans")
def save_plan(request: Request, exam_date: str = Form(...), minutes_per_day: int = Form(...), exam_topic: str = Form(...)):
    user = current_user(request)
    parsed_date = date.fromisoformat(exam_date)
    if parsed_date < date.today() or not 10 <= minutes_per_day <= 480 or exam_topic not in {"quadratics", "limits", "derivatives"}:
        return RedirectResponse("/?error=inputs", status_code=303)
    repository.save_learner_preferences(user["uid"], exam_date, minutes_per_day, exam_topic)
    return RedirectResponse("/", status_code=303)


@router.post("/attempts")
def save_attempt(request: Request, topic_id: str = Form(...), score: int = Form(...), max_score: int = Form(5)):
    user = current_user(request)
    if not 0 <= score <= max_score <= 100:
        return RedirectResponse("/?error=score", status_code=303)
    repository.create_attempt(user["uid"], topic_id, score, max_score)
    return RedirectResponse("/", status_code=303)


@router.post("/sessions/complete")
def complete_session(request: Request, topic_id: str = Form(...)):
    user = current_user(request)
    repository.record_session(user["uid"], topic_id)
    return RedirectResponse("/", status_code=303)


@router.post("/demo/reset")
def reset_demo(request: Request):
    user = current_user(request)
    if settings.auth_mode != "demo" or settings.app_env == "production" or user["uid"] != "demo-nimesh":
        return RedirectResponse("/", status_code=303)
    repository.reset_demo()
    return RedirectResponse("/", status_code=303)
