"""Offline safety checks: third-party ComfyUI interfaces are not generation engines."""
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cloud"))
from auto_router import recommend
from engine_registry import ENGINES


class FrontendCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "frontend-catalog.json").read_text(encoding="utf-8"))

    def test_research_schema_and_unique_ids(self):
        self.assertEqual(self.catalog["schema"], "furuya-comfyui-frontends/1")
        ids = [entry["id"] for entry in self.catalog["frontends"]]
        self.assertEqual(set(ids), {"comfyart", "creativefield"})
        self.assertEqual(len(ids), len(set(ids)))

    def test_no_automatic_execution_or_spend(self):
        self.assertFalse(self.catalog["default_execution_authorized"])
        self.assertFalse(self.catalog["inference_or_spend_triggered"])
        for entry in self.catalog["frontends"]:
            with self.subTest(frontend=entry["id"]):
                self.assertEqual(entry["status"], "RESEARCH_ONLY")
                self.assertFalse(entry["free_gpu_verified"])
                self.assertFalse(entry["owner_pc_validated"])
                self.assertFalse(entry["can_generate_now"])
                self.assertFalse(entry["eligible_for_auto_router"])
                self.assertFalse(entry["paid_fallback_allowed"])
                self.assertTrue(entry["upstream"].startswith("https://github.com/"))

    def test_frontends_are_not_generation_engines(self):
        engine_ids = {engine.id for engine in ENGINES}
        self.assertTrue({x["id"] for x in self.catalog["frontends"]}.isdisjoint(engine_ids))
        self.assertEqual(len(ENGINES), 11)

    def test_source_faithful_router_preserves_previous_safety(self):
        one = recommend(target_count=1, preserve_original_scene=True)
        self.assertEqual(one["preferred_engine"], "openjutsu_advanced")
        self.assertFalse(one["can_generate_now"])
        five = recommend(target_count=5, preserve_original_scene=True)
        self.assertIsNone(five["preferred_engine"])
        self.assertEqual(five["reason_code"], "NO_SOURCE_FAITHFUL_FIVE_PERSON_ENGINE")
        self.assertFalse(five["execution_authorized"])


if __name__ == "__main__":
    unittest.main()
