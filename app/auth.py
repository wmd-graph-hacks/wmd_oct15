from fastapi import HTTPException, Request
from itsdangerous import BadSignature, URLSafeSerializer

from app.config import settings

serializer = URLSafeSerializer(settings.session_secret, salt="study-planner-session")


def firebase_auth():
    import firebase_admin
    from firebase_admin import auth

    if not firebase_admin._apps:
        if settings.firebase_service_account:
            from firebase_admin import credentials
            firebase_admin.initialize_app(credentials.Certificate(settings.firebase_service_account))
        else:
            firebase_admin.initialize_app()
    return auth


def current_user(request: Request) -> dict:
    token = request.cookies.get("study_session")
    if not token:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    if settings.auth_mode == "demo":
        if settings.app_env == "production":
            raise HTTPException(status_code=503, detail="Demo authentication is disabled in production")
        try:
            return serializer.loads(token)
        except BadSignature as exc:
            raise HTTPException(status_code=303, headers={"Location": "/login"}) from exc
    try:
        auth = firebase_auth()
        claims = auth.verify_session_cookie(token, check_revoked=True)
        return {"uid": claims["uid"], "name": claims.get("name", "Learner"), "email": claims.get("email", "")}
    except Exception as exc:
        raise HTTPException(status_code=303, headers={"Location": "/login"}) from exc


def make_demo_cookie() -> str:
    return serializer.dumps({"uid": "demo-nimesh", "name": "Demo Learner", "email": ""})
