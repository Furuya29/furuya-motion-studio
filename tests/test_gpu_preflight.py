"""Regression checks for the v0.8 keyframe manifest. CPU-only, offline."""
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "cloud" / "free_gpu_preflight.py"
spec = importlib.util.spec_from_file_location("furuya_gpu_preflight", SCRIPT)
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class GPUPreflightManifestTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.project = self.root / "project.json"

    def run_preflight(self, data):
        self.project.write_text(json.dumps(data), encoding="utf-8")
        buffer = io.StringIO()
        with mock.patch.object(sys, "argv", [
            "free_gpu_preflight.py", "--workdir", str(self.root),
            "--project", str(self.project),
        ]), mock.patch.object(preflight, "gpu_info", return_value=[]), \
             contextlib.redirect_stdout(buffer):
            code = preflight.main()
        return code, json.loads(buffer.getvalue())

    def test_v08_manifest_keyframes(self):
        payload = {
            "schema": "furuya-recast-project/0.8",
            "video": {"clipDuration": 3, "filename": "driving.mp4"},
            "characters": [{"id": 1}],
            "keyframes": [
                {"time": 0.5},
                {"time": 1.5, "fullRepaintFilename": "repainted-ref.png"}
            ]
        }
        code, report = self.run_preflight(payload)
        self.assertEqual(code, 0)
        self.assertEqual(report["project_summary"]["schema"], payload["schema"])
        self.assertEqual(report["project_summary"]["keyframes"], 2)
        self.assertTrue(report["project_summary"]["has_repainted_frame"])
        self.assertEqual(report["project_summary"]["repaint_image_loaded"], "UNKNOWN_FROM_JSON")
        self.assertEqual(report["spent_money"], 0)
        self.assertFalse(report["models_loaded"])

    def test_legacy_v07_manifest(self):
        payload = {
            "schema": "furuya-recast-project/0.7",
            "video": {"clipDuration": 3, "filename": "source.mp4"},
            "characters": [],
            "keyframe": {"hasFullRepaint": True},
        }
        code, report = self.run_preflight(payload)
        self.assertEqual(code, 0)
        self.assertEqual(report["project_summary"]["keyframes"], 0)
        self.assertTrue(report["project_summary"]["has_repainted_frame"])


if __name__ == "__main__":
    unittest.main()
