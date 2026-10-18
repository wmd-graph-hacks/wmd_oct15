"""Regression coverage for the real HTTP flow and durable per-UID profiles."""
from dataclasses import replace
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from itsdangerous import SignatureExpired

from app import account_profile, auth
from app.main import app
from app.ui import router as web
from app.ui import agent_router as agent

ORIGIN = {'origin': 'http://testserver'}
DETAILS = {'full_name': 'Nimesh Maslekar', 'preferred_name': 'Nim', 'phone_number': '',
           'role': 'student', 'industry': 'Technology', 'interest_area': 'Mathematics'}


@pytest.fixture
def signed_client(monkeypatch, uid):
    config = replace(auth.settings, auth_mode='firebase', app_env='development', profile_store='falkordb')
    for module in (auth, web, agent, account_profile):
        monkeypatch.setattr(module, 'settings', config)
    monkeypatch.setattr(web, 'firebase_auth', lambda: SimpleNamespace(
        verify_id_token=lambda token: {'uid': uid, 'name': 'Nimesh', 'email': 'nim@example.com'}))
    return TestClient(app)


def sign_in(client):
    response = client.post('/auth/session', headers=ORIGIN, json={'id_token': 'verified-by-mocked-firebase'})
    assert response.status_code == 200
    assert response.json() == {'next': '/agent'}
    assert 'HttpOnly' in response.headers['set-cookie']
    assert 'SameSite=lax' in response.headers['set-cookie']


def test_first_signup_returning_login_and_logout(signed_client, uid):
    c = signed_client
    assert c.get('/').status_code == 200
    assert 'Big goals.' in c.get('/').text
    sign_in(c)
    r = c.get('/agent', follow_redirects=False)
    assert r.headers['location'] == '/onboarding'
    assert 'Your name' in c.get('/onboarding').text
    r = c.post('/api/account-profile', headers=ORIGIN, json=DETAILS)
    assert r.status_code == 200, r.text
    assert r.json()['complete'] is True
    assert r.json()['phone_number'] is None
    assert 'Hi, Nim' in c.get('/agent').text
    assert 'Welcome back, Nim' in c.get('/agent').text
    assert c.get('/onboarding', follow_redirects=False).headers['location'] == '/agent'
    assert c.get('/onboarding?edit=1').status_code == 200
    assert c.get('/login', follow_redirects=False).headers['location'] == '/agent'
    assert c.post('/auth/logout', headers=ORIGIN, follow_redirects=False).status_code == 303
    assert c.get('/agent', follow_redirects=False).headers['location'] == '/login'
    sign_in(c)
    assert 'Welcome back, Nim' in c.get('/agent').text
    assert account_profile.get_account_profile(uid).preferred_name == 'Nim'


def test_profile_validation_and_ownership(signed_client, uid):
    c = signed_client
    sign_in(c)
    for invalid in ({'preferred_name': '   '}, {'phone_number': 'hello'}, {'role': 'admin'}):
        assert c.post('/api/account-profile', headers=ORIGIN, json={**DETAILS, **invalid}).status_code == 422
    assert c.post('/api/account-profile', headers={'origin':'https://attacker.example'}, json=DETAILS).status_code == 403
    assert c.post('/api/account-profile', headers=ORIGIN, json=DETAILS).status_code == 200
    other = TestClient(app)
    other.cookies.set('study_session', auth.serializer.dumps({'uid':uid+'-other', 'mode':'firebase', 'name':'Other'}))
    assert other.get('/agent', follow_redirects=False).headers['location'] == '/onboarding'
    assert not account_profile.get_account_profile(uid+'-other').complete
    escaped = {**DETAILS, 'preferred_name':'<script>alert(1)</script>'}
    assert c.post('/api/account-profile', headers=ORIGIN, json=escaped).status_code == 200
    html = c.get('/agent').text
    assert '&lt;script&gt;alert(1)&lt;/script&gt;' in html


def test_rejected_tokens_bad_requests_and_expired_sessions(signed_client, monkeypatch):
    c = signed_client
    assert c.post('/auth/session', json={'id_token':'x'}).status_code == 403
    assert c.post('/auth/session', headers=ORIGIN, json={}).status_code == 422
    def invalid(token):
        raise ValueError('secret provider details')
    monkeypatch.setattr(web, 'firebase_auth', lambda: SimpleNamespace(verify_id_token=invalid))
    response = c.post('/auth/session', headers=ORIGIN, json={'id_token':'bad'})
    assert response.status_code == 401
    assert 'secret provider details' not in response.text
    assert 'study_session' not in response.cookies
    c.cookies.set('study_session', auth.serializer.dumps({'uid':'expired', 'mode':'firebase'}))
    def expired(*args, **kwargs):
        raise SignatureExpired('expired')
    monkeypatch.setattr(auth.serializer, 'loads', expired)
    assert c.get('/agent', follow_redirects=False).headers['location'] == '/login'


def test_storage_failure_is_recoverable(signed_client, monkeypatch):
    sign_in(signed_client)
    def unavailable(*args, **kwargs):
        raise ConnectionError('storage unavailable')
    monkeypatch.setattr(agent, 'get_account_profile', unavailable)
    r = signed_client.get('/agent')
    assert r.status_code == 503
    assert 'Your sign-in is still active' in r.text
    assert 'Try again' in r.text
    assert 'study_session' in signed_client.cookies


def test_production_cookie_verification_and_secure_flags(signed_client, monkeypatch):
    config = replace(auth.settings, app_env='production', session_cookie_secure=True)
    monkeypatch.setattr(auth, 'settings', config)
    monkeypatch.setattr(web, 'settings', config)
    provider = SimpleNamespace(
        verify_id_token=lambda token: {'uid':'production-test','name':'Prod'},
        create_session_cookie=lambda token, expires_in: 'firebase-session-cookie',
        verify_session_cookie=lambda token, check_revoked: {'uid':'production-test','name':'Prod'})
    monkeypatch.setattr(web, 'firebase_auth', lambda: provider)
    monkeypatch.setattr(auth, 'firebase_auth', lambda: provider)
    r = signed_client.post('/auth/session', headers=ORIGIN, json={'id_token':'valid'})
    assert r.status_code == 200
    assert '; Secure' in r.headers['set-cookie']
    assert r.cookies['study_session'] == 'firebase-session-cookie'


def test_explicit_firestore_backend(monkeypatch):
    values = {}
    calls = []
    class Document:
        def get(self, **kwargs):
            calls.append(kwargs)
            return SimpleNamespace(exists=bool(values), to_dict=lambda:values.copy())
        def set(self, data, **kwargs):
            calls.append(kwargs)
            values.update(data)
    monkeypatch.setattr(account_profile, 'settings', replace(account_profile.settings, profile_store='firestore'))
    monkeypatch.setattr(account_profile, '_document', lambda uid:Document())
    assert not account_profile.get_account_profile('firestore-test').complete
    submitted = account_profile.AccountProfileSubmission(**DETAILS)
    saved = account_profile.save_account_profile('firestore-test', email='x@example.invalid', google_name='X', profile=submitted)
    assert saved.complete
    assert account_profile.get_account_profile('firestore-test').preferred_name == 'Nim'
    assert account_profile.mark_dashboard_seen('firestore-test') is False
    assert account_profile.mark_dashboard_seen('firestore-test') is True
    assert all(call.get('timeout') == 5 and call.get('retry') is None for call in calls)
