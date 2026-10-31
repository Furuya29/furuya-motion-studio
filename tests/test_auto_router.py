"""Offline tests for the Furuya advisory engine router."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cloud"))
from auto_router import recommend, routing_policy
from engine_registry import ENGINES


class AutoRouterTests(unittest.TestCase):
    def test_scene_preserving_one_person(self):
        result = recommend(target_count=1, preserve_original_scene=True)
        self.assertEqual(result["task"], "scene_replacement")
        self.assertEqual(result["preferred_engine"], "openjutsu_advanced")
        self.assertFalse(result["can_generate_now"])

    def test_motion_transfer_one_person(self):
        result = recommend(target_count=1, preserve_original_scene=False)
        self.assertEqual(result["task"], "motion_transfer")
        self.assertEqual(result["preferred_engine"], "wan_animate2_motion")

    def test_multi_targets(self):
        for n in (2, 3, 4):
            result = recommend(target_count=n)
            self.assertEqual(result["task"], "multi_scene_replacement")
            self.assertEqual(result["preferred_engine"], "openjutsu_advanced")
            self.assertEqual(len(result["evaluation_order"]), 3)

    def test_no_old_engines_removed(self):
        self.assertEqual(len(ENGINES), 10)
        self.assertIn("kling3_motion", {engine.id for engine in ENGINES})
        self.assertIn("higgsfield_genjutsu_object_swap", {engine.id for engine in ENGINES})
        self.assertIn("higgsfield_genjutsu_motion_transfer", {engine.id for engine in ENGINES})

    def test_no_paid_or_automatic_execution(self):
        for count in (1, 2):
            for preserve in (False, True):
                result = recommend(target_count=count, preserve_original_scene=preserve)
                self.assertFalse(result["execution_authorized"])
                self.assertFalse(result["auto_render"])
                self.assertFalse(result["free_inference_verified"])
                self.assertNotIn("kling3_motion", [row["id"] for row in result["evaluation_order"]])
                self.assertTrue(all(not row["id"].startswith("higgsfield_genjutsu")
                                    for row in result["evaluation_order"]))

    def test_bad_inputs(self):
        for value in (-1, 0, 5, True, "2", 1.0):
            with self.assertRaises(ValueError):
                recommend(target_count=value)
        with self.assertRaises(ValueError):
            recommend(preserve_original_scene="false")

    def test_policy_constraints(self):
        policy = routing_policy()
        self.assertTrue(policy["constraints"]["never_auto_submit"])
        self.assertTrue(policy["constraints"]["block_paid_fallback"])
        self.assertEqual(policy["mode"], "ADVISORY_ONLY")


if __name__ == "__main__":
    unittest.main()
