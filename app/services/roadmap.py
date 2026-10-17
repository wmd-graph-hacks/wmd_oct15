from datetime import UTC, datetime

from app.ai.roadmap_explainer import personalize_roadmap
from app.graph import repository


def retrieve_roadmap(uid: str, display_name: str = "Learner") -> dict:
    """Retrieve graph candidates, evidence, paths, and resource citations."""
    repository.seed_course()
    repository.ensure_learner(uid, display_name)
    preferences = repository.learner_preferences(uid)
    candidates = repository.plan(uid, limit=12)
    target_id = preferences.get("exam_topic") or "derivatives"
    context = {
        "course_id": "foundational_math",
        "target_topic": target_id,
        "items": [
            {
                "topic_id": item["topic_id"],
                "topic": item["topic"],
                "minutes": item["minutes"],
                "prerequisite_path": item["path"],
                "path_topic_ids": item["path_topic_ids"],
                "resource": {
                    "title": item["resource"],
                    "source": item["resource_source"],
                    "reference": item["resource_reference"],
                    "url": item["url"],
                } if item["resource"] else None,
                "latest_check": item["attempt"],
                "aggregate_mastery_signal": item["mastery"],
                "graph_reason": item["reason"],
            }
            for item in candidates
        ],
    }
    return {
        "course_id": "foundational_math",
        "target_topic": target_id,
        "preferences": preferences,
        "recommendations": candidates,
        "generated_at": datetime.now(UTC).isoformat(),
        "_graph_context": context,
    }


def _valid_graph_order(candidates: list[dict], selected: list[dict]) -> bool:
    """Check that every unresolved retrieved prerequisite precedes its dependent."""
    candidate_ids = {item["topic_id"] for item in candidates}
    selected_ids = [item["topic_id"] for item in selected]
    for index, item in enumerate(selected):
        for prerequisite in candidates:
            prerequisite_id = prerequisite["topic_id"]
            is_upstream = item["topic_id"] in prerequisite["path_topic_ids"] and prerequisite_id != item["topic_id"]
            if is_upstream and prerequisite.get("mastery") is not None and prerequisite["mastery"] >= 0.7:
                continue
            if is_upstream and prerequisite_id in candidate_ids and prerequisite_id not in selected_ids[:index]:
                return False
    return True


async def personalize_retrieved_roadmap(result: dict) -> dict:
    """Accept model selection only when candidate IDs and graph order validate."""
    candidates = result["recommendations"]
    proposal = await personalize_roadmap(result.pop("_graph_context"))
    if proposal:
        by_id = {item["topic_id"]: item for item in candidates}
        selected_ids = proposal["selected_topic_ids"]
        if selected_ids and all(topic_id in by_id for topic_id in selected_ids):
            selected = [by_id[topic_id] for topic_id in selected_ids]
            if _valid_graph_order(candidates, selected):
                result["recommendations"] = selected
                result["ai_summary"] = proposal["summary"] or None
                result["plan_selection"] = "graph_context_ai"
                return result
    result["recommendations"] = candidates[:3]
    result["ai_summary"] = None
    result["plan_selection"] = "graph_ranked_fallback"
    return result
