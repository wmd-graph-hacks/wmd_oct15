from datetime import date
import logging
from pathlib import Path

from fastapi import APIRouter, Form, Request
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth import FIREBASE_SESSION_SECONDS, current_user, firebase_auth, make_demo_cookie, serializer, optional_user, require_same_origin
from app.config import settings
from app.graph import repository

BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=BASE_DIR / "templates")
router = APIRouter()


@router.get("/signup", response_class=HTMLResponse)
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if optional_user(request):
        return RedirectResponse("/agent", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"auth_mode": settings.auth_mode, "firebase_api_key": settings.firebase_api_key, "firebase_auth_domain": settings.firebase_auth_domain, "firebase_project_id": settings.firebase_project_id, "firebase_app_id": settings.firebase_app_id})


@router.post("/auth/demo")
def demo_login():
    if settings.auth_mode != "demo" or settings.app_env == "production":
        return RedirectResponse("/login", status_code=303)
    response = RedirectResponse("/", status_code=303)
    response.set_cookie("study_session", make_demo_cookie(), httponly=True, secure=settings.session_cookie_secure, samesite="lax", max_age=3600)
    return response


class SessionBody(BaseModel):
    id_token: str = Field(min_length=1, max_length=20000)


@router.post("/auth/session")
def create_session(request: Request, payload: SessionBody):
    if settings.auth_mode != "firebase":
        return RedirectResponse("/login", status_code=303)
    require_same_origin(request)
    try:
        auth = firebase_auth()
        claims = auth.verify_id_token(payload.id_token)
        if settings.app_env == "production":
            cookie = auth.create_session_cookie(payload.id_token, expires_in=FIREBASE_SESSION_SECONDS)
        else:
            # Local ADC can verify tokens even when it lacks a quota project for Firebase cookie minting.
            cookie = serializer.dumps({
                "uid": claims["uid"], "name": claims.get("name", "Learner"),
                "email": claims.get("email", ""), "mode": "firebase",
            })
        response = JSONResponse({"next": "/agent"})
        response.set_cookie("study_session", cookie, httponly=True, secure=settings.session_cookie_secure,
                            samesite="lax", max_age=FIREBASE_SESSION_SECONDS)
        return response
    except Exception as exc:
        logging.getLogger(__name__).exception("Firebase sign-in session creation failed")
        return JSONResponse({"detail": "We couldn’t finish signing you in. Please try again. If this continues, contact the app owner."}, status_code=401)


@router.post("/auth/logout")
def logout(request: Request):
    if request.headers.get("origin"):
        require_same_origin(request)
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("study_session")
    return response


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    if optional_user(request):
        return RedirectResponse("/agent", status_code=303)
    return templates.TemplateResponse(request, "landing.html", {})


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
