"""Offline tests for the upstream Openjutsu Advanced 1–4 person graph adapter."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cloud"))
import openjutsu_advanced_adapter as oj


def workflow():
    nodes = {
        "14": {"class_type": "VHS_LoadVideo", "_meta": {"title": "Source video (people get replaced)"},
               "inputs": {"video": ""}},
        "20": {"class_type": "H3AdvancedSwapPlan",
               "_meta": {"title": "Swap Plan (roles, seed, size)"},
               "inputs": {"roles": "", **{f"picture_{k}": [str(3*k-1), 0] for k in range(1, 5)},
                          **{f"picture_{k}_text": [str(3*k+1), 0] for k in range(1, 5)}}},
        "40": {"class_type": "H3Reference", "inputs": {f"ref_images.{i}": [str(3*i-1),0]
                                                 for i in range(1,5)}},
    }
    for k in range(1, 5):
        image_id = str(3*k-1)
        scaler_id = str(3*k)
        describe_id = str(3*k+1)
        nodes[image_id] = {"class_type":"LoadImage", "_meta":{"title":f"Picture {k}"},
                           "inputs":{"image":"sample.png"}}
        nodes[scaler_id] = {"class_type":"ImageScaleToMaxDimension",
                            "_meta":{"title":f"Scale picture {k}"},
                            "inputs":{"image":[image_id,0]}}
        nodes[describe_id] = {"class_type":"TextGenerate",
                              "_meta":{"title":f"Describe picture {k}"},
                              "inputs":{"image":[scaler_id,0]}}
    return nodes


class OpenjutsuAdvancedTests(unittest.TestCase):
    def test_three_characters_prunes_fourth(self):
        before = workflow()
        graph, plan = oj.prepare(before, characters=3,
                                  roles=["central dancer", "the dancer at left", "the dancer at right"])
        self.assertEqual(plan["characters"], 3)
        self.assertEqual(plan["source_video_node"], "14")
        self.assertEqual(plan["character_image_nodes"], ["2","5","8"])
        self.assertNotIn("11", graph)
        self.assertNotIn("12", graph)
        self.assertNotIn("13", graph)
        self.assertNotIn("picture_4", graph["20"]["inputs"])
        self.assertNotIn("picture_4_text", graph["20"]["inputs"])
        self.assertEqual(graph["20"]["inputs"]["roles"],
                         "central dancer\nthe dancer at left\nthe dancer at right")
        self.assertEqual(before["20"]["inputs"]["roles"], "")
        self.assertFalse(plan["tracking_executed"])

    def test_one_character_never_claims_auto_target_identification(self):
        graph, info = oj.prepare(workflow(), characters=1)
        self.assertEqual(info["characters"], 1)
        self.assertEqual(len(info["character_image_nodes"]), 1)
        self.assertEqual(graph["20"]["inputs"]["roles"], "")
        self.assertEqual(info["preflight"], "API_GRAPH_PATCHED_NOT_GENERATED")

    def test_four_characters_need_no_pruning(self):
        orig = workflow()
        graph, info = oj.prepare(orig, characters=4)
        self.assertEqual(info["removed_optional_nodes"], 0)
        self.assertEqual(len(graph), len(orig))

    def test_official_maxq_prepares_one_or_two_characters(self):
        import json
        reference = Path(__file__).resolve().parents[1] / "workflows/openjutsu_advanced_maxq.api.json"
        source = json.loads(reference.read_text(encoding="utf-8"))
        for count in (1, 2):
            graph, report = oj.prepare(source, characters=count,
                                       roles=["the center dancer", "the right dancer"][:count])
            self.assertEqual(report["variant"], "one_pass_per_person_2slot")
            self.assertEqual(report["available_pictures"], 2)
            self.assertEqual(report["source_video_node"], "8")
            self.assertEqual(report["character_image_nodes"], ["2", "5"][:count])
            self.assertEqual(report["swap_plan_node"], "14")
            self.assertEqual(graph["14"]["inputs"]["roles"],
                             "\\n".join(["the center dancer", "the right dancer"][:count]))
            for node in graph.values():
                for value in node["inputs"].values():
                    if oj.is_link(value):
                        self.assertIn(value[0], graph, "Pruning left a reference to a missing node")
        with self.assertRaisesRegex(ValueError, "at most 2"):
            oj.prepare(source, characters=3)

    def test_official_standard_prep_three_and_four(self):
        import json
        source = Path(__file__).resolve().parents[1] / "workflows/openjutsu_advanced.api.json"
        original = json.loads(source.read_text(encoding="utf-8"))
        for count in (3, 4):
            graph, report = oj.prepare(original, characters=count)
            self.assertEqual(report["variant"], "standard_4slot")
            self.assertEqual(report["available_pictures"], 4)
            self.assertEqual(len(report["character_image_nodes"]), count)
            self.assertTrue(all(oj.is_link(v) is False or v[0] in graph
                                for n in graph.values() for v in n["inputs"].values()))

    def test_rejects_unknown_workflow_or_bad_roles(self):
        with self.assertRaisesRegex(ValueError, "Expected exactly one"):
            oj.prepare({"1": {"class_type": "LoadImage", "inputs": {}}}, characters=2)
        with self.assertRaisesRegex(ValueError, "exactly one role"):
            oj.prepare(workflow(), characters=3, roles=["one"])


if __name__ == "__main__":
    unittest.main()
