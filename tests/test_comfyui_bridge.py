"""Real loopback HTTP integration tests for Furuya's ComfyUI bridge.

The server is a synthetic protocol fixture. Tests prove request/response
plumbing, not that any ComfyUI model or GPU can perform inference.
"""
from __future__ import annotations
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cloud"))
import comfyui_local_bridge as comfy

PID = "c88144cf-ccca-43e2-a2fe-89fe79aaf12a"
SYNTHETIC_MP4 = b"\x00\x00\x00\x18ftypisom" + b"x" * 4096


class FakeComfy(BaseHTTPRequestHandler):
    submitted = []

    def do_GET(self):
        if self.path == "/object_info":
            self.reply({"VideoReaderFake": {}, "ImageReaderFake": {}})
        elif self.path == "/history/" + PID:
            self.reply({PID: {"outputs": {"3": {"gifs": [{
                "filename": "mock_output.mp4", "subfolder": "", "type": "output"
            }]}}, "status": {"completed": True}}})
        elif self.path.startswith("/view?"):
            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Content-Length", str(len(SYNTHETIC_MP4)))
            self.end_headers()
            self.wfile.write(SYNTHETIC_MP4)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/prompt":
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            self.submitted.append(payload)
            self.reply({"prompt_id": PID, "number": 1})
        else:
            self.send_error(404)

    def reply(self, content):
        raw = json.dumps(content).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *args):
        return


class LocalComfyBridgeTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.input = self.root / "ComfyUI" / "input"
        self.input.mkdir(parents=True)
        self.video = self.root / "dance.mp4"
        self.image = self.root / "Albedo.png"
        self.video.write_bytes(b"\x00\x00\x00\x18ftypisom" + b"v" * 1200)
        self.image.write_bytes(b"\x89PNG\r\n\x1a\n" + b"i" * 1300)
        self.workflow = self.root / "api.json"
        self.workflow.write_text(json.dumps({
            "1": {"class_type": "VideoReaderFake", "inputs": {"video": "placeholder.mp4"}},
            "2": {"class_type": "ImageReaderFake", "inputs": {"image": "placeholder.png"}},
        }), encoding="utf-8")
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeComfy)
        FakeComfy.submitted = []
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.args = argparse.Namespace(
            workflow=self.workflow, server=f"http://127.0.0.1:{self.server.server_port}",
            input_dir=self.input, video=self.video, image=self.image,
            video_node="1", video_field="video", image_node="2", image_field="image",
            output=self.root / "result.mp4", receipt=self.root / "receipt.json",
            max_wait=20, execute=False, confirm_free_gpu=False)

    def test_dry_run_no_gpu_no_network_no_staging(self):
        with mock.patch.object(comfy, "api_json", side_effect=AssertionError("network called")):
            self.assertEqual(comfy.run(self.args), 0)
        self.assertFalse(self.args.receipt.exists())
        self.assertEqual(list(self.input.iterdir()), [])

    def test_local_httprunner_submits_once_and_recovers_synthetic_video(self):
        self.args.execute = True
        self.args.confirm_free_gpu = True
        self.assertEqual(comfy.run(self.args), 0)
        self.assertEqual(len(FakeComfy.submitted), 1)
        job = FakeComfy.submitted[0]
        self.assertTrue(job["prompt"]["1"]["inputs"]["video"].startswith("furuya_"))
        self.assertTrue(job["prompt"]["2"]["inputs"]["image"].startswith("furuya_"))
        self.assertTrue(self.args.output.exists())
        self.assertEqual(self.args.output.read_bytes(), SYNTHETIC_MP4)
        receipt = json.loads(self.args.receipt.read_text())
        self.assertEqual(receipt["status"], "RENDERED_UNREVIEWED")
        with self.assertRaisesRegex(ValueError, "receipt exists"):
            comfy.run(self.args)
        self.assertEqual(len(FakeComfy.submitted), 1)

    def test_two_character_references_are_bound_without_identity_mixup(self):
        second = self.root / "Diana.png"
        second.write_bytes(b"\x89PNG\r\n\x1a\n" + b"b" * 1300)
        graph = json.loads(self.workflow.read_text())
        graph["3"] = {"class_type": "ImageReaderFake", "inputs": {"image": "other.png"}}
        self.workflow.write_text(json.dumps(graph))
        self.args.extra_image = ["3=" + str(second)]
        self.args.execute = True
        self.args.confirm_free_gpu = True
        self.assertEqual(comfy.run(self.args), 0)
        submitted = FakeComfy.submitted[0]["prompt"]
        self.assertNotEqual(submitted["2"]["inputs"]["image"],
                            submitted["3"]["inputs"]["image"])
        self.assertTrue((self.input / submitted["3"]["inputs"]["image"]).exists())

    def test_duplicate_extra_reference_node_refused(self):
        self.args.extra_image = ["2=" + str(self.image)]
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            comfy.run(self.args)

    def test_no_local_gpu_confirmation_no_prompt_submitted(self):
        self.args.execute = True
        with self.assertRaisesRegex(ValueError, "confirm-free-gpu"):
            comfy.run(self.args)
        self.assertFalse(FakeComfy.submitted)

    def test_rejects_remote_endpoints_and_graph_format(self):
        with self.assertRaisesRegex(ValueError, "Only an explicit local"):
            comfy.local_base("https://example.com:443")
        with self.assertRaisesRegex(ValueError, "Only an explicit local"):
            comfy.local_base("http://192.168.1.10:8188")
        graph = self.root / "ui.json"
        graph.write_text('{"nodes":[{"id":1}],"links":[]}')
        with self.assertRaisesRegex(ValueError, "UI graph JSON"):
            comfy.workflow_api(graph)

    def test_unavailable_comfy_nodes_block_before_submit(self):
        self.args.execute = True
        self.args.confirm_free_gpu = True
        self.workflow.write_text(json.dumps({
            "1": {"class_type": "UninstalledNode", "inputs": {"video": "old.mp4"}},
            "2": {"class_type": "ImageReaderFake", "inputs": {"image": "old.png"}}
        }))
        with self.assertRaisesRegex(ValueError, "Required ComfyUI nodes"):
            comfy.run(self.args)
        self.assertEqual(len(FakeComfy.submitted), 0)
        self.assertFalse(self.args.receipt.exists())


if __name__ == "__main__":
    unittest.main()
