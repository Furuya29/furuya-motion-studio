"""Pure stdlib unit tests: multi-cast manifest is never a fake animation."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from validate_multicast_plan import validate


def fixture(n=3):
    return {
        "schema": "furuya-multicast-plan/1",
        "task": "multi_scene_replacement",
        "source_immutable": True,
        "tracking_state": "NOT_RUN",
        "render_state": "NOT_STARTED",
        "video": {"filename": "carnaval.mp4", "duration_seconds": 24.133,
                  "width": 720, "height": 1280},
        "targets": [
            {"id": "person_"+str(i), "name": "Character "+str(i),
             "reference_filename": "ref_"+str(i)+".png",
             "anchors": [{"time_seconds": 0.6+i, "box_xywh": [0.12+i*0.2, 0.12, 0.12, 0.45]}]}
            for i in range(n)
        ]
    }


class MultiCastValidationTests(unittest.TestCase):
    def test_three_characters_not_confused_with_tracking(self):
        result = validate(fixture())
        self.assertEqual(result["targets"], 3)
        self.assertEqual(result["anchors"], 3)
        self.assertEqual(result["status"], "ASSIGNMENTS_VALID_NOT_TRACKED")
        self.assertFalse(result["inference_executed"])
        self.assertFalse(result["target_tracking_verified"])

    def test_four_targets_accepted_five_blocked(self):
        self.assertEqual(validate(fixture(4))["targets"], 4)
        with self.assertRaisesRegex(ValueError, "1–4"):
            validate(fixture(5))

    def test_duplicate_id_rejected(self):
        f = fixture(2)
        f["targets"][1]["id"] = f["targets"][0]["id"]
        with self.assertRaisesRegex(ValueError, "unique"):
            validate(f)

    def test_bad_box_and_timestamp_rejected(self):
        f = fixture(1)
        f["targets"][0]["anchors"][0]["box_xywh"] = [0.9, 0.9, 0.2, 0.2]
        with self.assertRaisesRegex(ValueError, "outside image"):
            validate(f)
        f = fixture(1)
        f["targets"][0]["anchors"][0]["time_seconds"] = 25
        with self.assertRaisesRegex(ValueError, "outside clip"):
            validate(f)

    def test_tracking_cannot_be_marked_done(self):
        f = fixture()
        f["tracking_state"] = "VERIFIED"
        with self.assertRaisesRegex(ValueError, "honest tracking"):
            validate(f)


if __name__ == "__main__":
    unittest.main()
