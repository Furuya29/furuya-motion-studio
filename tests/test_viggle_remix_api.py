"""Offline tests for the Viggle Video Remix integration (no account, no charges)."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

MODULE = Path(__file__).resolve().parents[1] / "cloud" / "viggle_remix_api.py"
spec = importlib.util.spec_from_file_location("furuya_viggle_remix", MODULE)
remix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(remix)


class RemixTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.image = self.root / "albedo.png"
        self.video = self.root / "driving.mp4"
        self.output = self.root / "result.mp4"
        self.image.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
        self.video.write_bytes(b"fixture MP4")

    @mock.patch.object(remix, "probe_seconds", return_value=3.0)
    def test_preflight_uses_3_credit_estimate_and_no_network(self, probe):
        with mock.patch.object(remix, "urlopen", side_effect=AssertionError("no network")):
            plan = remix.prepare(self.image, self.video, self.output, "ffprobe")
        self.assertEqual(plan["estimated_credits"], 3)
        self.assertEqual(plan["required_available_credits_floor"], 4)
        self.assertEqual(plan["generation_status"], "NOT_STARTED")
        self.assertEqual(plan["endpoint"], "POST /v1/renders")
        self.assertFalse(self.output.exists())

    @mock.patch.object(remix, "probe_seconds", return_value=3.0)
    def test_no_overwrite_existing_video(self, probe):
        self.output.write_bytes(b"old output")
        with self.assertRaisesRegex(ValueError, "overwrite"):
            remix.prepare(self.image, self.video, self.output, "ffprobe")

    def test_multipart_has_original_background_and_two_media_files(self):
        body, content_type = remix.multipart(self.image, self.video)
        self.assertIn("multipart/form-data; boundary=furuya-", content_type)
        self.assertIn(b'name="image"; filename="albedo.png"', body)
        self.assertIn(b'name="motion_video"; filename="driving.mp4"', body)
        self.assertIn(b'name="background_mode"', body)
        self.assertIn(b"\r\noriginal\r\n", body)

    @mock.patch.object(remix, "probe_seconds", return_value=3.0)
    def test_insufficient_credits_prevents_submission(self, probe):
        plan = remix.prepare(self.image, self.video, self.output, "ffprobe")
        with mock.patch.object(remix, "api_json", return_value={"balance": 2}) as api:
            with self.assertRaisesRegex(ValueError, "Insufficient"):
                remix.execute(plan, "synthetic-test-token", resume_id=None, poll_seconds=1)
        self.assertEqual(api.call_count, 1)
        self.assertEqual(api.call_args.args[0], "GET")
        self.assertFalse(self.output.exists())
        self.assertFalse((self.root / "result.mp4.job.json").exists())

    @mock.patch.object(remix, "probe_seconds", return_value=3.0)
    def test_resuming_does_not_post_a_new_job(self, probe):
        plan = remix.prepare(self.image, self.video, self.output, "ffprobe")
        calls = []
        def fake(method, url, token, **kwargs):
            calls.append(method)
            if url.endswith("/credits"):
                return {"balance": 0}
            return {"status": "failed", "error": {"code": "synthetic_failure"}}
        with mock.patch.object(remix, "api_json", side_effect=fake):
            with self.assertRaisesRegex(RuntimeError, "synthetic_failure"):
                remix.execute(plan, "synthetic-test-token",
                              resume_id="render_existing123", poll_seconds=1)
        self.assertNotIn("POST", calls)


if __name__ == "__main__":
    unittest.main()
