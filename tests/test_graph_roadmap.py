import unittest
from unittest.mock import patch

from app.graph import repository


class GraphRoadmapTests(unittest.TestCase):
    def test_plan_uses_knowledge_state_and_graph_path(self):
        rows_by_query = {
            "RETURN l.exam_date": [["2099-01-01", 45, "derivatives"]],
            "MATCH path=": [
                ["fractions", "Fractions", 20, "Derivatives", 2, "r1", "Fractions practice", "https://example.test/fractions", "Textbook", "Chapter 1", 1, 12, ["Fractions", "Functions", "Derivatives"], ["fractions", "functions", "derivatives"]],
                ["functions", "Functions", 30, "Derivatives", 1, "r2", "Functions guide", "https://example.test/functions", "Textbook", "Chapter 2", 5, 12, ["Functions", "Derivatives"], ["functions", "derivatives"]],
                ["derivatives", "Derivatives", 40, "Derivatives", 0, "r3", "Derivative guide", "https://example.test/derivatives", "Textbook", "Chapter 3", 12, 12, ["Derivatives"], ["derivatives"]],
            ],
            "MADE_ATTEMPT": [["derivatives", "Derivatives", 4, 5, "2026-10-15T00:00:00+00:00"]],
            "HAS_KNOWLEDGE": [["derivatives", 0.8, 1, "2026-10-15T00:00:00+00:00"]],
            "HAS_SESSION": [],
        }

        def fake_rows(query, params=None):
            for marker, rows in rows_by_query.items():
                if marker in query:
                    return rows
            raise AssertionError(f"Unexpected graph query: {query}")

        with patch.object(repository, "_rows", side_effect=fake_rows):
            plan = repository.plan("learner-secret")

        self.assertEqual([item["topic_id"] for item in plan], ["fractions", "functions"])
        self.assertEqual(plan[0]["path"], ["Fractions", "Functions", "Derivatives"])
        self.assertEqual(plan[0]["resource_reference"], "Chapter 1")
        self.assertIsNone(plan[0]["mastery"])

    def test_assessment_evidence_changes_the_recommended_path(self):
        mastery = {"fractions": 0.8, "derivatives": 0.8}
        rows_by_query = {
            "RETURN l.exam_date": [["2099-01-01", 45, "derivatives"]],
            "MATCH path=": [
                ["fractions", "Fractions", 20, "Derivatives", 2, None, None, None, None, None, 1, 12, ["Fractions", "Functions", "Derivatives"], ["fractions", "functions", "derivatives"]],
                ["derivatives", "Derivatives", 40, "Derivatives", 0, None, None, None, None, None, 12, 12, ["Derivatives"], ["derivatives"]],
            ],
            "MADE_ATTEMPT": [["fractions", "Fractions", 4, 5, "2026-10-15T00:00:00+00:00"], ["derivatives", "Derivatives", 4, 5, "2026-10-15T00:00:00+00:00"]],
            "HAS_KNOWLEDGE": lambda: [[topic, score, 1, "2026-10-15T00:00:00+00:00"] for topic, score in mastery.items()],
            "HAS_SESSION": [],
        }

        def fake_rows(query, params=None):
            for marker, rows in rows_by_query.items():
                if marker in query:
                    return rows() if callable(rows) else rows
            raise AssertionError(f"Unexpected graph query: {query}")

        with patch.object(repository, "_rows", side_effect=fake_rows):
            mastered_plan = repository.plan("learner-secret")
            mastery["fractions"] = 0.2
            gap_plan = repository.plan("learner-secret")

        self.assertEqual(mastered_plan, [])
        self.assertEqual([item["topic_id"] for item in gap_plan], ["fractions"])
        self.assertIn("20%", gap_plan[0]["reason"])

    def test_attempt_write_keeps_values_as_parameters_and_updates_learner_graph(self):
        with patch.object(repository, "_rows") as rows:
            repository.create_attempt("learner-secret", "limits", 3, 5)

        query, params = rows.call_args.args
        self.assertIn("LearnerTopic", query)
        self.assertIn("HAS_KNOWLEDGE", query)
        self.assertNotIn("learner-secret", query)
        self.assertEqual(params["uid"], "learner-secret")
        self.assertEqual(params["knowledge_id"], "learner-secret:limits")

    def test_plan_persistence_links_topics_and_resources(self):
        item = {"topic_id": "limits", "resource_id": "limits_intro", "minutes": 20, "reason": "Prerequisite gap"}
        with patch.object(repository, "_rows") as rows:
            plan_id = repository.save_plan("learner-secret", "derivatives", [item])

        self.assertTrue(plan_id)
        creation_query, creation_params = rows.call_args.args
        self.assertIn("StudyPlan", creation_query)
        self.assertIn("PlanItem", creation_query)
        self.assertIn("USES", creation_query)
        self.assertNotIn("learner-secret", creation_query)
        self.assertEqual(creation_params["uid"], "learner-secret")
        self.assertEqual(creation_params["items"][0]["resource_id"], "limits_intro")

    def test_assessment_submission_records_a_scored_attempt(self):
        with patch.object(repository, "_rows", return_value=[["B", 1, "limits", "Limits"]]), \
             patch.object(repository, "create_attempt") as create_attempt, \
             patch.object(repository, "learner_knowledge", return_value={"limits": {"mastery": 1.0, "attempt_count": 1}}):
            result = repository.submit_assessment("learner-secret", "quick_check_limits", "b")

        self.assertTrue(result["is_correct"])
        self.assertEqual(result["knowledge"]["mastery"], 1.0)
        create_attempt.assert_called_once_with("learner-secret", "limits", 1, 1, "quick_check_limits")


if __name__ == "__main__":
    unittest.main()
