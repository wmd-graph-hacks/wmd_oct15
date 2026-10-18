from fastapi import HTTPException, Request
from itsdangerous import BadSignature, URLSafeTimedSerializer

from app.config import settings
from urllib.parse import urlsplit

serializer = URLSafeTimedSerializer(settings.session_secret, salt="study-planner-session")
FIREBASE_SESSION_SECONDS = 60 * 60 * 24 * 5
DEMO_SESSION_SECONDS = 60 * 60


def require_same_origin(request: Request) -> None:
    origin = urlsplit(request.headers.get('origin', ''))
    if origin.scheme not in ('http', 'https') or (origin.scheme, origin.netloc) != (request.url.scheme, request.url.netloc):
        raise HTTPException(status_code=403, detail='Please reload this page and try again.')


def optional_user(request: Request) -> dict | None:
    try:
        return current_user(request)
    except HTTPException as exc:
        if exc.status_code == 303:
            return None
        raise


def firebase_app():
    import firebase_admin
    if not firebase_admin._apps:
        options = {"projectId": settings.firebase_project_id} if settings.firebase_project_id else None
        if settings.firebase_service_account:
            from firebase_admin import credentials
            firebase_admin.initialize_app(
                credentials.Certificate(settings.firebase_service_account),
                options=options,
            )
        else:
            firebase_admin.initialize_app(options=options)
    return firebase_admin.get_app()


def firebase_auth():
    from firebase_admin import auth
    firebase_app()
    return auth


def current_user(request: Request) -> dict:
    token = request.cookies.get("study_session")
    if not token:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    if settings.auth_mode == "demo" and settings.app_env == "production":
        raise HTTPException(status_code=503, detail="Demo authentication is disabled in production")
    try:
        if settings.auth_mode == "firebase" and settings.app_env == "production":
            claims = firebase_auth().verify_session_cookie(token, check_revoked=True)
        else:
            age = DEMO_SESSION_SECONDS if settings.auth_mode == "demo" else FIREBASE_SESSION_SECONDS
            claims = serializer.loads(token, max_age=age)
            if not isinstance(claims, dict) or claims.get("mode", "demo") != settings.auth_mode:
                raise BadSignature("Wrong session mode")
        if not isinstance(claims.get("uid"), str) or not claims["uid"]:
            raise BadSignature("Missing identity")
        return {"uid": claims["uid"], "name": claims.get("name") or "Learner", "email": claims.get("email") or ""}
    except Exception as exc:
        raise HTTPException(status_code=303, headers={"Location": "/login"}) from exc


def make_demo_cookie() -> str:
    return serializer.dumps({"uid": "demo-nimesh", "name": "Demo Learner", "email": "", "mode": "demo"})
