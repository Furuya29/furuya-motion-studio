"""No GPU, network, account or cloud resources required for these tests."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "prepare_clip.py"
spec = importlib.util.spec_from_file_location("furuya_prepare_clip", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ClipTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.addCleanup(self.root.cleanup)
        self.folder = Path(self.root.name)
        self.output = self.folder / "out"
        self.output.mkdir()
        self.project = self.folder / "project.json"
        self.base = {
            "schema": "furuya-recast-project/0.8",
            "video": {
                "filename": "source.mp4", "width": 360, "height": 640,
                "duration": 2.5, "clipStart": 0.3, "clipDuration": 1.5
            },
            "keyframes": [{"time": 1.0, "fullRepaintFilename": "edited.png",
                           "characters": []}]
        }
        self.project.write_text(json.dumps(self.base), encoding="utf-8")

    def test_manifest_and_boundaries(self):
        data, frames = mod.safe_manifest(self.project)
        self.assertEqual(frames[0]["time"], 1.0)
        self.assertEqual(data["schema"], "furuya-recast-project/0.8")
        self.base["video"]["clipDuration"] = 8
        self.project.write_text(json.dumps(self.base), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Clip must last"):
            mod.safe_manifest(self.project)

    def test_keyframe_must_be_inside_clip(self):
        self.base["keyframes"][0]["time"] = 2.4
        self.project.write_text(json.dumps(self.base), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "No keyframe"):
            mod.safe_manifest(self.project)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg unavailable")
    def test_dry_run_then_prepare_cpu(self):
        source = self.folder / "source.mp4"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=360x640:rate=24",
            "-t", "2.5", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(source),
        ], check=True, timeout=50)
        argv = ["--project", str(self.project), "--video", str(source),
                "--outdir", str(self.output), "--max-dimension", "512"]
        self.assertEqual(mod.main(argv), 0)
        self.assertFalse((self.output / "driving.mp4").exists())
        self.assertEqual(mod.main(argv + ["--execute"]), 0)
        result = mod.probe(self.output / "driving.mp4", "ffprobe")
        self.assertAlmostEqual(result["duration"], 1.5, delta=.09)
        self.assertEqual(result["width"] % 32, 0)
        self.assertEqual(result["height"] % 32, 0)
        self.assertTrue((self.output / "source-ref.png").is_file())
        self.assertEqual(mod.main(argv), 2, "Refuse to overwrite outputs")


if __name__ == "__main__":
    unittest.main()
