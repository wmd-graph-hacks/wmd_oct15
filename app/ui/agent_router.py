"""Agent, quiz and graph-map endpoints. uid always comes from the verified session."""
from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from app.account_profile import (AccountProfileSubmission, get_account_profile,
                                 mark_dashboard_seen, save_account_profile)
from app.agent.models import AgentRequest
from app.agent.runner import get_run, run_agent
from app.agent.tools import CommitArgs, ToolError, Toolbox
from app.auth import current_user, require_same_origin
from app.config import settings
from app.kg import queries as kg
from app.kg.connection import kg_graph, rows
from app.learn import bank, quiz, state
from app.learn import plans as learning_plans
from app.learn.profile import Profile, get_profile, save_profile
from app.rag import answer as rag_answer
from app.rag import embed as rag_embed

templates = Jinja2Templates(directory=Path(__file__).resolve().parents[1] / "templates")
router = APIRouter()
DEMO_UID = "demo-nimesh"
# Demo learner: solid foundations and single-variable calculus basics.
DEMO_MASTERED = [  # maths only; other subjects start empty
    "math-foundations-of-mathematics-logic-and-quantifiers",
    "math-foundations-of-mathematics-proof-techniques",
    "math-foundations-of-mathematics-mathematical-induction",
    "math-foundations-of-mathematics-sets-and-operations",
    "math-foundations-of-mathematics-relations-and-equivalence",
    "math-foundations-of-mathematics-functions-and-cardinality",
    "math-single-variable-calculus-limits-and-continuity",
    "math-single-variable-calculus-derivatives-and-applications",
]


def user_or_401(request: Request) -> dict:
    try:
        return current_user(request)
    except FastAPIHTTPException as exc:
        if exc.status_code == 303:
            raise HTTPException(status_code=401, detail="Sign in required") from exc
        raise


def guarded(fn, *a):
    try:
        return fn(*a)
    except ToolError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except quiz.QuizError as exc:
        raise HTTPException(status_code=exc.status, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Graph storage is unavailable") from exc


def account_profile_guarded(fn, *a, **kw):
    try:
        return fn(*a, **kw)
    except Exception as exc:
        import logging
        logging.getLogger(__name__).exception("Account profile storage failed")
        raise HTTPException(status_code=503, detail="Your profile is temporarily unavailable. Please try again in a moment.") from exc


@router.get("/agent", response_class=HTMLResponse)
def agent_page(request: Request):
    user = current_user(request)
    account_profile = None
    returning = False
    if settings.auth_mode == "firebase":
        account_profile = account_profile_guarded(get_account_profile, user["uid"], user.get("email", ""), user.get("name", "Learner"))
        if not account_profile.complete:
            from fastapi.responses import RedirectResponse
            return RedirectResponse("/onboarding", status_code=303)
        returning = account_profile_guarded(mark_dashboard_seen, user["uid"])
    try:
        profile = get_profile(user["uid"])
    except Exception:
        profile = Profile()
    if settings.auth_mode == "demo" and not profile.onboarded:
        profile = guarded(save_profile, user["uid"], Profile(preferred_name=user.get("name") or "Demo Learner",
                                                               interest_subject="mathematics"))
    demo = user["uid"] == DEMO_UID and settings.auth_mode == "demo" and settings.app_env != "production"
    if demo:  # first visit: give the demo learner a starting point
        try:
            if not state.get_beliefs(DEMO_UID):
                state.seed_beliefs(DEMO_UID, DEMO_MASTERED)
        except Exception:
            pass
    return templates.TemplateResponse(request, "agent.html", {
        "user": user, "profile": profile, "account_profile": account_profile, "returning": returning,
        "is_demo": user["uid"] == DEMO_UID and settings.auth_mode == "demo",
        "llm_enabled": settings.ai_enabled})


@router.get("/onboarding", response_class=HTMLResponse)
def onboarding_page(request: Request):
    user = current_user(request)
    if settings.auth_mode != "firebase":
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/agent", status_code=303)
    profile = account_profile_guarded(get_account_profile, user["uid"], user.get("email", ""), user.get("name", "Learner"))
    if profile.complete and request.query_params.get("edit") != "1":
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/agent", status_code=303)
    return templates.TemplateResponse(request, "onboarding.html", {"user": user, "profile": profile})


@router.get("/quiz/{subtopic_id}", response_class=HTMLResponse)
def quiz_page(subtopic_id: str, request: Request):
    user = current_user(request)
    title = (guarded(kg.get_subtopic, subtopic_id) or {}).get("title")
    if not title:
        raise HTTPException(status_code=404, detail="Unknown subtopic")
    return templates.TemplateResponse(request, "quiz.html", {"user": user, "subtopic_id": subtopic_id, "title": title,
                                                             "available": len(bank.questions_for(subtopic_id))})


def _clean(title: str) -> str:
    return title.replace(" — study lesson", "")


def _require_subject(subject: str | None) -> str:
    from app.kg.loader import ensure_loaded
    ensure_loaded()
    known = {s["subject"] for s in kg.list_subjects()}
    if not known:
        raise HTTPException(status_code=503, detail="No curriculum is loaded yet")
    subject = subject or ("mathematics" if "mathematics" in known else sorted(known)[0])
    if subject not in known:
        raise HTTPException(status_code=404, detail=f"Unknown subject {subject!r}")
    return subject


@router.get("/api/agent/subjects")
def subjects(user: dict = Depends(user_or_401)):
    def build():
        from app.kg.loader import ensure_loaded
        ensure_loaded()
        beliefs = state.get_beliefs(user["uid"])
        out = []
        for sj in kg.list_subjects():
            ids = [r[0] for r in rows(kg_graph(), "MATCH (s:Subtopic {subject:$s}) RETURN s.id", {"s": sj["subject"]})]
            last = rows(kg_graph(), "MATCH (s:Subtopic {subject:$s}) RETURN s.title ORDER BY s.topic_order DESC, s.order LIMIT 1",
                        {"s": sj["subject"]})
            out.append({**sj, "title": sj["title"], "mastered": sum(1 for i in ids if beliefs.get(i, {}).get("status") == "mastered"),
                        "with_quiz": sum(1 for i in ids if bank.questions_for(i)),
                        "example_goal": "I want to understand KKT conditions for constrained optimization"
                        if sj["subject"] == "mathematics" else f"I want to learn {_clean(last[0][0])}" if last else ""})
        return {"subjects": out}
    return guarded(build)


@router.get('/api/learning/plans')
def saved_learning_plans(user: dict = Depends(user_or_401)):
    return {'plans': guarded(learning_plans.saved_plans, user['uid'])}


@router.get('/study/{plan_id}/{subtopic_id}', response_class=HTMLResponse)
def study_lesson(plan_id: str, subtopic_id: str, request: Request):
    user = current_user(request)
    try:
        plan, item = learning_plans.plan_lesson(user['uid'], plan_id, subtopic_id)
    except ToolError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail='Your saved plan is temporarily unavailable.') from exc
    sections = guarded(lambda: rows(kg_graph(),
        'MATCH (s:Subtopic {id:$sid})-[:HAS_CHUNK]->(c:Chunk) RETURN c.section, c.text ORDER BY c.idx',
        {'sid': subtopic_id}))
    return templates.TemplateResponse(request, 'study.html', {'plan': plan, 'item': item,
        'sections': sections, 'has_quiz': bool(bank.questions_for(subtopic_id))})


@router.post('/api/learning/plans/{plan_id}/lessons/{subtopic_id}/complete')
def complete_planned_lesson(plan_id: str, subtopic_id: str, request: Request,
                            user: dict = Depends(user_or_401)):
    require_same_origin(request)
    try:
        return learning_plans.complete_lesson(user['uid'], plan_id, subtopic_id)
    except ToolError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail='Your progress could not be saved. Please try again.') from exc


@router.get("/api/agent/graph")
def graph_data(subject: str | None = None, user: dict = Depends(user_or_401)):
    def build():
        sj = _require_subject(subject)
        nodes = rows(kg_graph(), "MATCH (s:Subtopic {subject:$s}) RETURN s.id, s.title, s.topic_id, s.topic_order, s.order, s.estimated_minutes",
                     {"s": sj})
        topics = rows(kg_graph(), "MATCH (t:Topic {subject:$s}) RETURN t.id, t.title, t.order ORDER BY t.order", {"s": sj})
        beliefs = state.get_beliefs(user["uid"])
        return {
            "subject": sj,
            "topics": [{"id": t[0], "title": t[1], "order": t[2]} for t in topics],
            "nodes": [{"id": n[0], "title": _clean(n[1]), "topic_id": n[2], "col": n[3] - 1, "row": n[4], "minutes": n[5],
                       "state": beliefs.get(n[0], {}).get("status", "unseen"), "has_quiz": bool(bank.questions_for(n[0]))}
                      for n in nodes],
            "edges": [{"a": a, "b": b, "soft": s in ("soft", "sequence"), "inferred": s == "sequence", "derived": d}
                      for a, b, s, d in kg.prerequisite_edges(True, subject=sj)],
        }
    return guarded(build)


@router.post("/api/agent/runs")
async def create_run(body: AgentRequest, user: dict = Depends(user_or_401)):
    try:
        run = await run_agent(user["uid"], body)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Agent could not run") from exc
    return run


@router.get("/api/agent/runs/{run_id}")
def read_run(run_id: str, user: dict = Depends(user_or_401)):
    run = guarded(get_run, user["uid"], run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.get("/api/agent/proposals/{proposal_id}")
def read_proposal(proposal_id: str, user: dict = Depends(user_or_401)):
    prop = guarded(Toolbox(user["uid"]).get_proposal, proposal_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return prop


@router.post("/api/agent/proposals/{proposal_id}/approve")
def approve(proposal_id: str, user: dict = Depends(user_or_401)):
    return guarded(lambda: Toolbox(user["uid"]).call("commit_plan", {"proposal_id": proposal_id}, allow_commit=True))


@router.post("/api/agent/proposals/{proposal_id}/reject")
def reject(proposal_id: str, user: dict = Depends(user_or_401)):
    return guarded(Toolbox(user["uid"]).reject_plan, proposal_id)


class AnswerBody(BaseModel):
    position: int


@router.post("/api/quiz/{subtopic_id}/start")
def quiz_start(subtopic_id: str, user: dict = Depends(user_or_401)):
    return guarded(quiz.start, user["uid"], subtopic_id)


@router.post("/api/quiz/attempts/{attempt_id}/hint")
def quiz_hint(attempt_id: str, user: dict = Depends(user_or_401)):
    return guarded(quiz.hint, user["uid"], attempt_id)


@router.post("/api/quiz/attempts/{attempt_id}/answer")
def quiz_answer(attempt_id: str, body: AnswerBody, user: dict = Depends(user_or_401)):
    return guarded(quiz.answer, user["uid"], attempt_id, body.position)


@router.post("/api/agent/demo/reset")
def demo_reset(user: dict = Depends(user_or_401)):
    if settings.auth_mode != "demo" or settings.app_env == "production" or user["uid"] != DEMO_UID:
        raise HTTPException(status_code=403, detail="Demo reset is only available to the demo learner")

    def do():
        state.reset_learner(DEMO_UID)
        state.seed_beliefs(DEMO_UID, DEMO_MASTERED)
        return {"status": "reset", "mastered": len(DEMO_MASTERED)}
    return guarded(do)


class AskBody(BaseModel):
    question: str = Field(min_length=3, max_length=400)
    subtopic_id: str | None = None
    subject: str | None = Field(default=None, max_length=80)


@router.get("/tutor", response_class=HTMLResponse)
def tutor_page(request: Request):
    user = current_user(request)
    return templates.TemplateResponse(request, "tutor.html", {"user": user, "llm_enabled": settings.ai_enabled})


@router.post("/api/tutor/ask")
async def tutor_ask(body: AskBody, user: dict = Depends(user_or_401)):
    embed = rag_embed.litellm_embed if rag_embed.EMBEDDING_MODEL else None
    try:
        return await rag_answer.ask(user["uid"], body.question, subtopic_id=body.subtopic_id, subject=body.subject, embed=embed)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="The tutor could not reach the graph") from exc


@router.get("/api/profile")
def profile_get(user: dict = Depends(user_or_401)):
    return guarded(get_profile, user["uid"])


@router.post("/api/profile")
def profile_save(body: Profile, user: dict = Depends(user_or_401)):
    # Keep older profile forms working while new learners can set these explicitly.
    body = body.model_copy(update={"preferred_name": body.preferred_name or user.get("name") or "Learner"})
    return guarded(lambda: save_profile(user["uid"], body))


@router.post("/api/account-profile")
def account_profile_save(request: Request, body: AccountProfileSubmission, user: dict = Depends(user_or_401)):
    require_same_origin(request)
    if settings.auth_mode != "firebase":
        raise HTTPException(status_code=403, detail="Firebase account profiles are only available with Google sign-in")
    return account_profile_guarded(save_account_profile, user["uid"], email=user.get("email", ""),
                                   google_name=user.get("name", "Learner"), profile=body)
