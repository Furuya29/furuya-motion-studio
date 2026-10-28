"""Offline tests for the inference adapter: no GPU use or model execution."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

FILE = Path(__file__).resolve().parents[1] / "cloud" / "viggle_inference.py"
spec = importlib.util.spec_from_file_location("viggle_adapter", FILE)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class AdapterTests(unittest.TestCase):
    def test_dry_run_guards_and_command(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            checkout = root / "Viggle-Animate"
            entry = checkout / "inference" / "sample.py"
            entry.parent.mkdir(parents=True)
            entry.write_text("raise RuntimeError('Should never execute in dry-run')\n")
            model = root / "MiniMax-H3"
            model.mkdir()
            (model / "stub.safetensors").write_bytes(b"DO NOT LOAD MODEL")
            video = root / "driving.mp4"
            video.write_bytes(b"")
            frame = root / "repainted-ref.png"
            frame.write_bytes(b"")
            output = root / "output.mp4"
            args = adapter.argparse.Namespace(
                checkout=checkout, model_dir=model, video=video,
                repaint=frame, output=output, python="python",
                offload=False, execute=False)
            job = adapter.build(args)
            self.assertEqual(job["status"], "DRY_RUN")
            self.assertEqual(job["command"][-6:],
                             ["--cond", str(video), "--ref", str(frame), "--out", str(output)])
            self.assertEqual(job["downloads"], False)
            self.assertFalse(output.exists())
            self.assertEqual(adapter.main([
                "--checkout", str(checkout), "--model-dir", str(model),
                "--video", str(video), "--repaint", str(frame), "--output", str(output)]), 0)
            output.write_bytes(b"existing")
            with self.assertRaisesRegex(ValueError, "overwrite"):
                adapter.build(args)


if __name__ == "__main__":
    unittest.main()
