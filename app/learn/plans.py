"""Saved approved plans and lesson completion, always scoped to the signed-in UID."""
import json
from urllib.parse import quote

from app.agent.tools import ToolError
from app.kg.connection import rows, student_graph


def saved_plans(uid):
    records = rows(student_graph(),
        "MATCH (p:PlanProposal {uid:$uid, status:'committed'}) "
        "RETURN p.id, p.payload, p.completed_ids, p.committed_ms ORDER BY p.committed_ms DESC, p.id", {'uid': uid})
    plans = []
    for pid, payload, completed, committed in records:
        data = json.loads(payload)
        done = set(completed or [])
        items = [{**item, 'week': week['week'], 'done': item['id'] in done,
                  'url': f'/study/{quote(pid, safe="")}/{quote(item["id"], safe="")}'}
                 for week in data['weeks'] for item in week['items']]
        next_item = next((i for i in items if not i['done']), None)
        plans.append({'id': pid, 'goal': data['goal'], 'items': items,
                      'total': len(items), 'completed': sum(i['done'] for i in items),
                      'minutes': data['total_minutes'], 'next': next_item,
                      'finished': next_item is None, 'committed_ms': committed})
    return plans


def plan_lesson(uid, plan_id, subtopic_id):
    plan = next((p for p in saved_plans(uid) if p['id'] == plan_id), None)
    if not plan:
        raise ToolError('Saved plan not found')
    item = next((i for i in plan['items'] if i['id'] == subtopic_id), None)
    if not item:
        raise ToolError('This lesson is not part of your saved plan')
    return plan, item


def complete_lesson(uid, plan_id, subtopic_id):
    plan_lesson(uid, plan_id, subtopic_id)
    # Atomic membership check keeps repeated clicks and concurrent requests idempotent.
    student_graph().query(
        "MATCH (p:PlanProposal {id:$id, uid:$uid, status:'committed'}) "
        "WHERE NOT $sid IN coalesce(p.completed_ids,[]) "
        "SET p.completed_ids=coalesce(p.completed_ids,[])+[$sid]",
        {'id': plan_id, 'uid': uid, 'sid': subtopic_id})
    return next(p for p in saved_plans(uid) if p['id'] == plan_id)
