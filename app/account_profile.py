"""Account profiles, keyed by verified Firebase UID.

FalkorDB is the default durable store already required by this application.
Firestore can be selected explicitly with PROFILE_STORE=firestore once configured.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.config import settings
from app.kg.connection import rows, student_graph


class AccountProfileSubmission(BaseModel):
    full_name: str = Field(min_length=1, max_length=100)
    preferred_name: str = Field(min_length=1, max_length=50)
    phone_number: str | None = Field(default=None, max_length=30)
    role: Literal['student', 'educator', 'professional', 'other']
    industry: str = Field(min_length=1, max_length=80)
    interest_area: str = Field(min_length=1, max_length=100)

    @field_validator('full_name', 'preferred_name', 'phone_number', 'industry', 'interest_area', mode='before')
    @classmethod
    def clean_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator('phone_number')
    @classmethod
    def optional_phone(cls, value):
        if not value:
            return None
        if any(c not in '+0123456789 ()-.' for c in value) or not 7 <= sum(c.isdigit() for c in value) <= 15:
            raise ValueError('Enter a valid phone number, or leave it blank')
        return value


class AccountProfile(BaseModel):
    full_name: str | None = None
    preferred_name: str | None = None
    phone_number: str | None = None
    role: str | None = None
    industry: str | None = None
    interest_area: str | None = None
    complete: bool = False
    dashboard_seen: bool = False


FIELDS = ('full_name', 'preferred_name', 'phone_number', 'role', 'industry', 'interest_area')


def _document(uid):
    from firebase_admin import firestore
    from app.auth import firebase_app
    return firestore.client(app=firebase_app()).collection('users').document(uid)


def get_account_profile(uid: str, email: str = '', google_name: str = '') -> AccountProfile:
    if settings.profile_store == 'firestore':
        doc = _document(uid).get(timeout=5, retry=None)
        data = doc.to_dict() or {} if doc.exists else {}
    else:
        result = rows(student_graph(), 'MATCH (l:Learner {uid:$uid}) RETURN ' +
                      ', '.join('l.' + f for f in FIELDS) + ', l.account_profile_complete, l.dashboard_seen', {'uid': uid})
        if not result:
            return AccountProfile()
        values = result[0]
        data = dict(zip(FIELDS, values[:6]))
        data.update(complete=bool(values[6]), dashboard_seen=bool(values[7]))
    # A completion marker alone cannot skip required onboarding fields.
    data['complete'] = bool(data.get('complete') and all(data.get(k) for k in FIELDS if k != 'phone_number'))
    return AccountProfile(**{k: v for k, v in data.items() if k in AccountProfile.model_fields})


def save_account_profile(uid: str, *, email: str, google_name: str, profile: AccountProfileSubmission) -> AccountProfile:
    data = profile.model_dump()
    now = datetime.now(timezone.utc).isoformat()
    if settings.profile_store == 'firestore':
        _document(uid).set({**data, 'uid': uid, 'email': email, 'google_name': google_name,
                            'complete': True, 'updated_at': now}, merge=True, timeout=5, retry=None)
    else:
        params = {**data, 'uid': uid, 'email': email, 'updated': now}
        student_graph().query('MERGE (l:Learner {uid:$uid}) SET ' +
                              ', '.join('l.' + f + '=$' + f for f in FIELDS) +
                              ', l.email=$email, l.account_profile_complete=true, l.account_profile_updated_at=$updated', params)
    return AccountProfile(**data, complete=True)


def mark_dashboard_seen(uid: str) -> bool:
    profile = get_account_profile(uid)
    if not profile.dashboard_seen:
        if settings.profile_store == 'firestore':
            _document(uid).set({'dashboard_seen': True}, merge=True, timeout=5, retry=None)
        else:
            student_graph().query('MATCH (l:Learner {uid:$uid}) SET l.dashboard_seen=true', {'uid': uid})
    return profile.dashboard_seen
