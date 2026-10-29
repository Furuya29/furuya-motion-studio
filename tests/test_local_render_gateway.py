"""Offline regression tests for safe local Furuya generation bridge."""
from __future__ import annotations
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cloud"))
import local_render_gateway as gateway
from viggle_remix_api import multipart


class GatewayTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)
        self.image = self.folder / "Albedo.png"
        self.video = self.folder / "driving.mp4"
        self.image.write_bytes(b"\x89PNG\r\n\x1a\nFAKE_IMAGE_FIXTURE")
        self.video.write_bytes(b"\x00\x00\x00\x18ftypisomFAKE_MP4_FIXTURE")
        self.state = gateway.RenderState(self.folder)

    def test_parse_offline_multipart(self):
        body, content_type = multipart(self.image, self.video)
        files = gateway.parse_form(content_type, body)
        self.assertEqual(files["image"], self.image.read_bytes())
        self.assertEqual(files["motion_video"], self.video.read_bytes())
        self.assertEqual(set(files), {"image", "motion_video"})

    @mock.patch.object(gateway, "probe_seconds", return_value=3)
    def test_preparation_does_not_contact_network(self, probe):
        with mock.patch.object(gateway, "api_json", side_effect=AssertionError("unexpected network")):
            state = self.state.prepare({
                "image": self.image.read_bytes(),
                "motion_video": self.video.read_bytes(),
            })
        self.assertEqual(state["status"], "PREPARED")
        self.assertEqual(state["credit_estimate"], 3)
        self.assertEqual(state["required_balance"], 3)
        self.assertFalse(state["output_ready"])
        self.assertTrue((self.state.session / "receipt.json").exists())

    @mock.patch.object(gateway, "probe_seconds", return_value=3)
    def test_no_credit_key_prevents_render(self, probe):
        self.state.prepare({"image": self.image.read_bytes(),
                            "motion_video": self.video.read_bytes()})
        with mock.patch.dict(os.environ, {"VIGGLE_API_KEY": ""}):
            with mock.patch.object(gateway, "api_json", side_effect=AssertionError("network")):
                with self.assertRaisesRegex(ValueError, "not configured"):
                    self.state.start()
        self.assertEqual(self.state.public()["status"], "PREPARED")

    @mock.patch.object(gateway, "probe_seconds", return_value=3)
    def test_insufficient_balance_prevents_submission(self, probe):
        self.state.prepare({"image": self.image.read_bytes(),
                            "motion_video": self.video.read_bytes()})
        with mock.patch.dict(os.environ, {"VIGGLE_API_KEY": "synthetic-token"}):
            with mock.patch.object(gateway, "api_json", return_value={"balance": 1}) as api:
                with self.assertRaisesRegex(ValueError, "Insufficient"):
                    self.state.start()
        self.assertEqual(api.call_count, 1)
        self.assertEqual(api.call_args.args[0], "GET")
        self.assertEqual(self.state.public()["status"], "PREPARED")

    @mock.patch.object(gateway, "probe_seconds", return_value=3)
    def test_uncertain_submission_cannot_retry(self, probe):
        self.state.prepare({"image": self.image.read_bytes(),
                            "motion_video": self.video.read_bytes()})
        self.state.job["status"] = "SUBMISSION_UNCERTAIN"
        with mock.patch.dict(os.environ, {"VIGGLE_API_KEY": "synthetic-token"}):
            with self.assertRaisesRegex(ValueError, "Prepare the files"):
                self.state.start()
        self.assertEqual(self.state.public()["status"], "SUBMISSION_UNCERTAIN")

    def test_invalid_upload_headers(self):
        with self.assertRaises(ValueError):
            gateway.parse_form("text/plain", b"not multipart")


if __name__ == "__main__":
    unittest.main()