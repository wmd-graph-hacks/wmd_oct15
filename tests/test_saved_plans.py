from fastapi.testclient import TestClient
from app.auth import serializer
from app.main import app
from app.agent.tools import Toolbox, ProposeArgs, CommitArgs
from app.learn import plans, state

SID='math-foundations-of-mathematics-logic-and-quantifiers'


def client(uid):
    c=TestClient(app)
    c.cookies.set('study_session', serializer.dumps({'uid':uid,'name':'Test','email':''}))
    return c


def test_saved_plan_resume_and_completion(db, uid):
    c=client(uid)
    assert c.get('/api/learning/plans').json()=={'plans':[]}
    box=Toolbox(uid)
    proposal=box.propose_plan(ProposeArgs(subtopic_ids=[SID],hours_per_week=5,weeks_available=4,goal='Learn logic'))
    assert c.get('/api/learning/plans').json()=={'plans':[]}, 'Draft proposals must not appear as saved plans'
    box.commit_plan(CommitArgs(proposal_id=proposal['proposal_id']))
    saved=c.get('/api/learning/plans').json()['plans'][0]
    assert saved['next']['id']==SID and saved['completed']==0
    lesson=c.get(saved['next']['url'])
    assert lesson.status_code==200 and 'Mark as studied' in lesson.text
    assert 'logic' in lesson.text.lower()
    path=f"/api/learning/plans/{saved['id']}/lessons/{SID}/complete"
    assert c.post(path,headers={'origin':'https://attacker.example'}).status_code==403
    for _ in range(2):
        result=c.post(path,headers={'origin':'http://testserver'})
        assert result.status_code==200, result.text
        assert result.json()['completed']==1 and result.json()['finished']
        assert result.json()['next'] is None
    assert SID not in state.mastered_ids(uid), 'Reading is not evidence of mastery'
    assert plans.saved_plans(uid)[0]['completed']==1
    assert 'You’ve studied this lesson.' in c.get(saved['items'][0]['url']).text
    other=client(uid+'-other')
    assert other.get('/api/learning/plans').json()=={'plans':[]}
    assert other.get(saved['items'][0]['url']).status_code==404
    assert other.post(path,headers={'origin':'http://testserver'}).status_code==404
    assert c.get(f"/study/{saved['id']}/unknown-lesson").status_code==404
