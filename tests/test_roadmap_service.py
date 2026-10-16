import unittest
from unittest.mock import AsyncMock, patch

from app.services.roadmap import personalize_retrieved_roadmap


def candidate(topic_id, path_ids, mastery=None):
    return {"topic_id": topic_id, "path_topic_ids": path_ids, "mastery": mastery, "minutes": 20}


class RoadmapServiceTests(unittest.IsolatedAsyncioTestCase):
    def make_result(self):
        candidates = [
            candidate("fractions", ["fractions", "functions", "derivatives"]),
            candidate("functions", ["functions", "derivatives"]),
            candidate("derivatives", ["derivatives"]),
        ]
        return {"recommendations": candidates, "_graph_context": {"items": [{"topic_id": "fractions"}]}}

    async def test_accepts_model_order_when_graph_prerequisites_are_respected(self):
        proposal = {"selected_topic_ids": ["fractions", "functions", "derivatives"], "summary": "Build from foundations."}
        with patch("app.services.roadmap.personalize_roadmap", new_callable=AsyncMock, return_value=proposal):
            result = await personalize_retrieved_roadmap(self.make_result())
        self.assertEqual([item["topic_id"] for item in result["recommendations"]], proposal["selected_topic_ids"])
        self.assertEqual(result["plan_selection"], "graph_context_ai")

    async def test_rejects_hallucinated_or_out_of_order_topic_ids(self):
        proposal = {"selected_topic_ids": ["derivatives", "fractions"], "summary": "Unsupported ordering."}
        with patch("app.services.roadmap.personalize_roadmap", new_callable=AsyncMock, return_value=proposal):
            result = await personalize_retrieved_roadmap(self.make_result())
        self.assertEqual([item["topic_id"] for item in result["recommendations"]], ["fractions", "functions", "derivatives"])
        self.assertEqual(result["plan_selection"], "graph_ranked_fallback")

    async def test_falls_back_if_model_returns_unknown_topic(self):
        proposal = {"selected_topic_ids": ["imaginary_topic"], "summary": "Invented."}
        with patch("app.services.roadmap.personalize_roadmap", new_callable=AsyncMock, return_value=proposal):
            result = await personalize_retrieved_roadmap(self.make_result())
        self.assertEqual(result["plan_selection"], "graph_ranked_fallback")


if __name__ == "__main__":
    unittest.main()
