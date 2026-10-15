import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.auth import make_demo_cookie
from app.main import app
from app.graph import repository


class RoadmapApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.client.cookies.set("study_session", make_demo_cookie())

    def test_generate_persists_graph_plan_and_returns_grounded_items(self):
        item = {
            "topic_id": "limits", "topic": "Limits", "minutes": 20,
            "target": "Derivatives", "distance": 1, "resource_id": "limits_intro",
            "resource": "Introduction to limits", "url": "https://example.test/limits",
            "resource_source": "Textbook", "resource_reference": "Chapter 5",
            "order": 11, "attempt": None, "mastery": None, "attempt_count": 0,
            "path": ["Limits", "Derivatives"], "path_topic_ids": ["limits", "derivatives"], "session_done": False,
            "reason": "No check recorded; prerequisite for derivatives.",
        }
        with patch.object(repository, "seed_course"), patch.object(repository, "ensure_learner"), \
             patch.object(repository, "learner_preferences", return_value={"exam_topic": "derivatives", "minutes_per_day": 30}), \
             patch.object(repository, "plan", return_value=[item]), patch.object(repository, "save_plan", return_value="saved-plan-id"):
            response = self.client.post("/api/v1/plan/generate")

        self.assertEqual(response.status_code, 201, response.text)
        body = response.json()
        self.assertEqual(body["plan_id"], "saved-plan-id")
        self.assertEqual(body["recommendations"][0]["resource_reference"], "Chapter 5")
        self.assertIsNone(body["ai_summary"])

    def test_signed_out_plan_request_is_json_401(self):
        self.client.cookies.clear()
        response = self.client.get("/api/v1/plan")
        self.assertEqual(response.status_code, 401)

    def test_assessment_api_does_not_expose_answer_key(self):
        assessment = {"assessment_id": "quick_check_limits", "title": "Limits quick check", "question": "What is lim(x→2) (x + 3)?", "options": ["3", "5", "DNE"], "max_score": 1, "topic_id": "limits", "topic": "Limits", "source": "Hand-authored demo diagnostic"}
        with patch.object(repository, "seed_course"), patch.object(repository, "get_assessment", return_value=assessment):
            response = self.client.get("/api/v1/topics/limits/assessment")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("correct_answer", response.json())

    def test_assessment_submission_updates_knowledge_evidence(self):
        result = {"topic_id": "limits", "topic": "Limits", "score": 1, "max_score": 1, "is_correct": True, "knowledge": {"mastery": 1.0, "attempt_count": 1}}
        with patch.object(repository, "seed_course"), patch.object(repository, "ensure_learner"), patch.object(repository, "submit_assessment", return_value=result) as submit:
            response = self.client.post("/api/v1/assessments/submit", json={"assessment_id": "quick_check_limits", "answer": "B"})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["is_correct"])
        submit.assert_called_once_with("demo-nimesh", "quick_check_limits", "B")


if __name__ == "__main__":
    unittest.main()
