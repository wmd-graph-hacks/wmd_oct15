import json
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from app.ai import roadmap_explainer


class RoadmapExplainerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        roadmap_explainer._PLAN_CACHE.clear()

    async def test_disabled_ai_uses_no_provider(self):
        config = SimpleNamespace(ai_enabled=False, ai_model="", ai_timeout_seconds=1)
        with patch.object(roadmap_explainer, "settings", config):
            summary = await roadmap_explainer.personalize_roadmap({"items": [{"topic_id": "limits", "topic": "Limits"}]})
        self.assertIsNone(summary)

    async def test_call_is_compact_cached_and_does_not_send_identity(self):
        context = {"course_id": "foundational_math", "target_topic": "derivatives", "items": [{"topic_id": "limits", "topic": "Limits", "minutes": 20, "graph_reason": "Prerequisite gap"}]}
        content = json.dumps({"selected_topic_ids": ["limits"], "summary": "Review limits before derivatives."})
        completion = AsyncMock(return_value=SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))]))
        fake_litellm = types.ModuleType("litellm")
        fake_litellm.acompletion = completion

        config = SimpleNamespace(ai_enabled=True, ai_model="test/provider-model", ai_timeout_seconds=1)
        with patch.object(roadmap_explainer, "settings", config), patch.dict(sys.modules, {"litellm": fake_litellm}):
            first = await roadmap_explainer.personalize_roadmap(context)
            second = await roadmap_explainer.personalize_roadmap(context)

        self.assertEqual(first, second)
        self.assertEqual(first["selected_topic_ids"], ["limits"])
        self.assertEqual(completion.await_count, 1)
        sent = json.loads(completion.await_args.kwargs["messages"][1]["content"])
        self.assertNotIn("uid", sent)
        self.assertEqual(completion.await_args.kwargs["num_retries"], 0)

    async def test_provider_failure_falls_back_without_raising(self):
        fake_litellm = types.ModuleType("litellm")
        fake_litellm.acompletion = AsyncMock(side_effect=RuntimeError("provider offline"))
        config = SimpleNamespace(ai_enabled=True, ai_model="test/provider-model", ai_timeout_seconds=1)
        with patch.object(roadmap_explainer, "settings", config), patch.dict(sys.modules, {"litellm": fake_litellm}):
            summary = await roadmap_explainer.personalize_roadmap({"items": [{"topic_id": "limits", "topic": "Limits"}]})
        self.assertIsNone(summary)

    async def test_provider_error_tries_fallback_and_parses_fenced_json(self):
        context = {"items": [{"topic_id": "limits", "topic": "Limits"}]}
        content = "```json\n" + json.dumps({"selected_topic_ids": ["limits"], "summary": "Review limits."}) + "\n```"
        completion = AsyncMock(side_effect=[RuntimeError("primary unavailable"), SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])])
        fake_litellm = types.ModuleType("litellm")
        fake_litellm.acompletion = completion
        config = SimpleNamespace(
            ai_enabled=True,
            ai_model="gemini/gemini-3.8-flash",
            ai_fallback_models=("gemini/gemini-3.6-flash", "gemini/gemini-3.5-flash-lite"),
            ai_timeout_seconds=1,
        )

        with patch.object(roadmap_explainer, "settings", config), patch.dict(sys.modules, {"litellm": fake_litellm}):
            result = await roadmap_explainer.personalize_roadmap(context)

        self.assertEqual(result["selected_topic_ids"], ["limits"])
        self.assertEqual(completion.await_count, 2)
        self.assertEqual(completion.await_args_list[0].kwargs["model"], "gemini/gemini-3.8-flash")
        self.assertEqual(completion.await_args_list[1].kwargs["model"], "gemini/gemini-3.6-flash")

    async def test_invalid_model_output_tries_next_fallback(self):
        context = {"items": [{"topic_id": "limits", "topic": "Limits"}]}
        valid = json.dumps({"selected_topic_ids": ["limits"], "summary": "Review limits."})
        completion = AsyncMock(side_effect=[SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="not json"))]), SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=valid))])])
        fake_litellm = types.ModuleType("litellm")
        fake_litellm.acompletion = completion
        config = SimpleNamespace(ai_enabled=True, ai_model="primary", ai_fallback_models=("fallback",), ai_timeout_seconds=1)

        with patch.object(roadmap_explainer, "settings", config), patch.dict(sys.modules, {"litellm": fake_litellm}):
            result = await roadmap_explainer.personalize_roadmap(context)

        self.assertEqual(result["summary"], "Review limits.")
        self.assertEqual(completion.await_count, 2)


if __name__ == "__main__":
    unittest.main()
