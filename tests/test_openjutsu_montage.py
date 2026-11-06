"""Offline reviewed Montage tests against Openjutsu's exact API workflow."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cloud"))
from comfyui_local_bridge import workflow_api
from openjutsu_montage_review import build_reviewed_montage


def fixture():
    return {
        "schema": "furuya-find-people-review/1",
        "frames": 72, "tracks": "h3_montage_people_00001_.npz",
        "identity_assignments_reviewed": False,
        "people": [
            {"track": 7, "start": 0, "end": 72, "pick": 1,
             "role": 1, "area": 0.2, "on": [[0, 72]]},
            {"track": 8, "start": 12, "end": 67, "pick": 2,
             "role": 2, "area": 0.17, "on": [[12, 67]]},
            {"track": 9, "start": 0, "end": 31, "pick": 1,
             "role": 1, "area": 0.10, "on": [[0, 31]]},
        ],
    }


def source():
    return workflow_api(ROOT / "workflows/openjutsu_montage.api.json")


class ReviewedMontageTests(unittest.TestCase):
    def test_official_graph_preserves_selected_tracks_only(self):
        graph, result = build_reviewed_montage(
            source(), fixture(), 2, ["the center dancer", "the left dancer"],
            [{"track": 7, "start": 0, "end": 72, "pick": 1},
             {"track": 8, "start": 12, "end": 67, "pick": 2}])
        self.assertEqual(result["selected_replacements"], 2)
        self.assertEqual(result["source_video_node"], "8")
        self.assertEqual(result["character_image_nodes"], ["2", "5"])
        self.assertFalse(result["rendered_video"])
        self.assertFalse(result["gpu_used"])
        self.assertEqual(graph["109"]["inputs"]["file"],
                         "h3_montage_people_00001_.npz")
        self.assertEqual(graph["14"]["inputs"]["track_data"], ["109", 0])
        self.assertEqual(json.loads(graph["14"]["inputs"]["labels"]), [
            {"track": 7, "start": 0, "end": 72, "role": 1},
            {"track": 8, "start": 12, "end": 67, "role": 2},
        ])
        self.assertNotIn("121", graph)
        self.assertNotIn("122", graph)
        self.assertNotIn("124", graph)
        self.assertNotIn("125", graph)
        self.assertNotIn("103", graph)  # Third optional reference removed
        self.assertNotIn("106", graph)  # Fourth optional reference removed
        self.assertTrue(all(not isinstance(value, list) or
                            not len(value)==2 or
                            not isinstance(value[0], str) or
                            not value[0].isdigit() or value[0] in graph
                            for node in graph.values() for value in node["inputs"].values()))

    def test_one_person_and_four_people(self):
        for count in (1, 4):
            graph, result = build_reviewed_montage(
                source(), fixture(), count,
                [f"person {n}" for n in range(1, count+1)],
                [{"track":7, "start":0, "end":72, "pick":count}])
            self.assertEqual(result["characters"], count)
            self.assertEqual(result["selected_replacements"], 1)
            self.assertEqual(len(result["character_image_nodes"]), count)
            self.assertEqual(json.loads(graph["14"]["inputs"]["labels"])[0]["role"],count)

    def test_defaults_do_not_automatically_swap_unreviewed_people(self):
        with self.assertRaisesRegex(ValueError, "Select at least one"):
            build_reviewed_montage(source(),fixture(),2,["one","two"],[])
        with self.assertRaisesRegex(ValueError, "Select at least one"):
            build_reviewed_montage(source(),fixture(),2,["one","two"],
                                  [{"track":7,"start":0,"end":72,"pick":0}])

    def test_cannot_forge_unknown_appearance_or_stale_file(self):
        with self.assertRaisesRegex(ValueError, "Unknown"):
            build_reviewed_montage(source(),fixture(),1,["one"],
                                  [{"track":22,"start":0,"end":72,"pick":1}])
        review=fixture()
        review["tracks"]="../secret.npz"
        with self.assertRaisesRegex(ValueError, "No valid"):
            build_reviewed_montage(source(),review,1,["one"],
                                  [{"track":7,"start":0,"end":72,"pick":1}])

    def test_reject_duplicate_and_non_integer_picks(self):
        selections=[{"track":7,"start":0,"end":72,"pick":1}]*2
        with self.assertRaisesRegex(ValueError, "duplicate"):
            build_reviewed_montage(source(),fixture(),1,["one"],selections)
        with self.assertRaisesRegex(ValueError, "out of range"):
            build_reviewed_montage(source(),fixture(),1,["one"],
                                  [{"track":7,"start":0,"end":72,"pick":True}])

if __name__ == "__main__":
    unittest.main()
