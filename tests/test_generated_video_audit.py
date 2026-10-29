"""Video acceptance tests run entirely offline; no real AI inferred."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import audit_generated_video as report


class VideoAcceptanceTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.source = self.dir / "source.mp4"
        self.output = self.dir / "output.mp4"
        self.source.write_bytes(b"fake-original" * 100)
        self.output.write_bytes(b"fake-output" * 100)
        self.meta = {
            "width": 576, "height": 1024, "duration": 3.0,
            "fps": 24, "frames": 72, "codec": "h264",
        }

    def test_original_copy_cannot_pass(self):
        self.output.write_bytes(self.source.read_bytes())
        with mock.patch.object(report, "inspect", return_value=self.meta):
            result = report.audit(self.source, self.output)
        self.assertEqual(result["status"], "FAIL_STRUCTURAL")
        self.assertTrue(result["same_sha256"])

    def test_different_video_without_review_not_approved(self):
        with mock.patch.object(report, "inspect", return_value=self.meta):
            result = report.audit(self.source, self.output)
        self.assertEqual(result["status"], "RENDERED_NEEDS_VISUAL_REVIEW")
        self.assertFalse(all(result["manual_review_checks"].values()))

    def test_explicit_full_review_required(self):
        all_checks = {k: True for k in report.REVIEW_KEYS}
        with mock.patch.object(report, "inspect", return_value=self.meta):
            result = report.audit(self.source, self.output, review=all_checks)
        self.assertEqual(result["status"], "PASS_REVIEWED")
        all_checks["bystanders_preserved"] = False
        with mock.patch.object(report, "inspect", return_value=self.meta):
            result = report.audit(self.source, self.output, review=all_checks)
        self.assertEqual(result["status"], "RENDERED_NEEDS_VISUAL_REVIEW")

    def test_duration_mismatch_blocks_pass(self):
        wrong = dict(self.meta, duration=9.0, frames=216)
        with mock.patch.object(report, "inspect", side_effect=[self.meta, wrong]):
            result = report.audit(self.source, self.output)
        self.assertEqual(result["status"], "FAIL_STRUCTURAL")


if __name__ == "__main__":
    unittest.main()
