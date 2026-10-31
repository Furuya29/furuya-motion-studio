"""Synthetic ComfyUI/Openjutsu end-to-end tests; no actual AI or GPU involved."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cloud"))
from comfyui_web_jobs import ComfyJobs, parse_upload
from comfyui_readiness import MODEL_FIELDS, GIB
from local_render_gateway import Handler, RenderState

WORKFLOW = (ROOT / "workflows" / "openjutsu_advanced.api.json").read_bytes()
GRAPH = json.loads(WORKFLOW)
PROMPT_ID = "550bcb4d-c2af-42d9-b4c3-fccb381e96cc"
FAKE_MP4 = b"\x00\x00\x00\x18ftypisom" + b"x" * 4096


class FakeComfy(BaseHTTPRequestHandler):
    prompts = []
    allow_nodes = True
    model_missing = False
    gpu_gib = 24
    ram_gib = 96

    def send_json(self, data):
        raw = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/object_info":
            classes = {node["class_type"] for node in GRAPH.values()}
            if not self.allow_nodes:
                classes.discard("H3AdvancedSwapPlan")
            info = {name: {} for name in classes}
            for class_type, fields in MODEL_FIELDS.items():
                if class_type not in info:
                    continue
                allowed = {}
                for field in fields:
                    values = sorted({n["inputs"].get(field) for n in GRAPH.values()
                                     if n["class_type"] == class_type and isinstance(n["inputs"].get(field), str)})
                    if self.model_missing and values:
                        values = ["other_model_not_installed.safetensors"]
                    allowed[field] = [values]
                info[class_type] = {"input": {"required": allowed}}
            self.send_json(info)
        elif self.path == "/system_stats":
            self.send_json({"system": {"ram_total": self.ram_gib * GIB},
                            "devices": [{"name": "Synthetic NVIDIA RTX 4090 (NOT REAL GPU)",
                                         "type": "cuda", "vram_total": self.gpu_gib * GIB}]})
        elif self.path == "/history/" + PROMPT_ID:
            self.send_json({PROMPT_ID: {
                "outputs": {"44": {"gifs": [{"filename": "test.mp4",
                  "subfolder": "", "type": "output"}]}},
                "status": {"completed": True}
            }})
        elif self.path.startswith("/view?"):
            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Content-Length", str(len(FAKE_MP4)))
            self.end_headers()
            self.wfile.write(FAKE_MP4)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/prompt":
            self.send_error(404)
            return
        size = int(self.headers.get("Content-Length", "0"))
        self.prompts.append(json.loads(self.rfile.read(size)))
        self.send_json({"prompt_id": PROMPT_ID})

    def log_message(self, *args):
        return


def multipart(fields):
    boundary = "furuya-test-20261030"
    pieces = []
    for name, value in fields.items():
        content = value if isinstance(value, bytes) else str(value).encode()
        filename = name + (".json" if name == "workflow" else ".mp4" if name == "motion_video" else ".png")
        pieces.append(b"--" + boundary.encode() + b"\r\n"
                      + ("Content-Disposition: form-data; name=\"" + name +
                         "\"; filename=\"" + filename + "\"\r\n"
                         "Content-Type: application/octet-stream\r\n\r\n").encode()
                      + content + b"\r\n")
    pieces.append(b"--" + boundary.encode() + b"--\r\n")
    return b"".join(pieces), "multipart/form-data; boundary=" + boundary


def media(n):
    return {
        "workflow": WORKFLOW,
        "motion_video": b"\x00\x00\x00\x18ftypisom" + b"v" * 1300,
        **{"image_" + str(i): b"\x89PNG\r\n\x1a\n" + bytes([i]) * 1300 for i in range(1, n+1)},
        **{"role_" + str(i): "the dancer at position " + str(i) for i in range(1, n+1)},
    }


class GatewayComfyTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.input = self.root / "ComfyUI" / "input"
        self.input.mkdir(parents=True)
        FakeComfy.prompts = []
        FakeComfy.allow_nodes = True
        FakeComfy.model_missing = False
        FakeComfy.gpu_gib = 24
        FakeComfy.ram_gib = 96
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeComfy)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.backend = "http://127.0.0.1:" + str(self.server.server_port)
        self.jobs = ComfyJobs(self.root / "comfy-jobs", server=self.backend,
                              input_dir=self.input)

        class Gateway(Handler):
            pass
        Gateway.root = ROOT
        Gateway.state = RenderState(self.root / "viggle-job-state")
        Gateway.comfy = self.jobs
        self.gateway = ThreadingHTTPServer(("127.0.0.1", 0), Gateway)
        threading.Thread(target=self.gateway.serve_forever, daemon=True).start()
        self.addCleanup(self.gateway.server_close)
        self.addCleanup(self.gateway.shutdown)
        self.url = "http://127.0.0.1:" + str(self.gateway.server_port)

    def post(self, route, data=b"", headers=None):
        return Request(self.url + route, data=data, method="POST",
                       headers={"X-Furuya-Intent":"local-explicit-user-action", **(headers or {})})

    def test_default_vendored_workflow_prepares_two_references_without_network(self):
        fields = media(2)
        with mock.patch("comfyui_web_jobs.api_json", side_effect=AssertionError("network used in prepare")):
            with mock.patch("comfyui_web_jobs.probe_seconds", return_value=3.0):
                report = self.jobs.prepare(fields)
        self.assertEqual(report["status"], "PREPARED")
        self.assertEqual(report["characters"], 2)
        self.assertEqual(report["image_node_ids"], ["2", "5"])
        generated = json.loads((self.jobs.session / "prepared_api.json").read_text())
        self.assertNotIn("8", generated)
        self.assertNotIn("11", generated)
        self.assertEqual(generated["20"]["inputs"]["roles"],
                         "the dancer at position 1\nthe dancer at position 2")
        self.assertFalse(report["actual_ai_inference_verified"] if "actual_ai_inference_verified" in report else report["inference_executed"])

    def test_openjutsu_maxq_prepare_two_and_reject_three(self):
        maxq = (ROOT / "workflows/openjutsu_advanced_maxq.api.json").read_bytes()
        with mock.patch("comfyui_web_jobs.probe_seconds", return_value=3.0):
            fields = media(2)
            fields["workflow"] = maxq
            prepared = self.jobs.prepare(fields)
            self.assertEqual(prepared["characters"], 2)
            self.assertEqual(prepared["workflow_variant"], "one_pass_per_person_2slot")
            self.assertEqual(prepared["workflow_character_capacity"], 2)
            self.assertEqual(prepared["source_video_node"], "8")
            self.assertEqual(prepared["image_node_ids"], ["2", "5"])
            with self.assertRaisesRegex(ValueError, "at most 2"):
                extra = media(3)
                extra["workflow"] = maxq
                self.jobs.prepare(extra)
        self.assertEqual(len(FakeComfy.prompts), 0)

    def test_http_prepare_submit_and_recover_video_with_one_post(self):
        body, mime = multipart(media(3))
        request = self.post("/api/comfy/prepare", body, {"Content-Type": mime})
        with mock.patch("comfyui_web_jobs.probe_seconds", return_value=3.0):
            with urlopen(request, timeout=8) as response:
                prepared = json.load(response)
            self.assertEqual(prepared["characters"], 3)
            self.assertEqual(prepared["status"], "PREPARED")
            with self.assertRaises(HTTPError) as blocked:
                urlopen(self.post("/api/comfy/start"), timeout=8)
            self.assertEqual(blocked.exception.code, 400)
            self.assertEqual(len(FakeComfy.prompts), 0)
            with urlopen(self.post("/api/comfy/start", headers={"X-Furuya-Confirm": "AUTHORIZE_LOCAL_GPU"}),
                         timeout=8) as response:
                start = json.load(response)
            self.assertEqual(start["status"], "SUBMISSION_UNCERTAIN")
            for _ in range(80):
                current = self.jobs.public()
                if current["status"] == "RENDERED_UNREVIEWED":
                    break
                time.sleep(0.05)
            self.assertEqual(current["status"], "RENDERED_UNREVIEWED", current)
        self.assertEqual(len(FakeComfy.prompts), 1)
        received = FakeComfy.prompts[0]["prompt"]
        self.assertIn("video", received["14"]["inputs"])
        self.assertEqual(len({received[i]["inputs"]["image"] for i in ("2","5","8")}), 3)
        with urlopen(self.url + "/api/comfy/result", timeout=8) as response:
            self.assertEqual(response.read(), FAKE_MP4)
        with self.assertRaises(HTTPError) as err:
            urlopen(self.post("/api/comfy/start", headers={"X-Furuya-Confirm":"AUTHORIZE_LOCAL_GPU"}),
                    timeout=8)
        self.assertEqual(err.exception.code, 400)
        self.assertEqual(len(FakeComfy.prompts), 1)
        self.assertFalse(current["actual_ai_inference_verified"])

    def test_restarted_gateway_restores_receipt_without_resubmission(self):
        with mock.patch("comfyui_web_jobs.probe_seconds", return_value=3):
            self.jobs.prepare(media(1))
        self.jobs.job.update(status="SUBMITTED", prompt_id=PROMPT_ID)
        self.jobs.save()
        restored = ComfyJobs(self.jobs.root, server=self.backend, input_dir=self.input)
        self.assertEqual(restored.public()["status"], "PENDING")
        with mock.patch("comfyui_web_jobs.api_json", side_effect=AssertionError("no calls allowed")):
            with self.assertRaisesRegex(ValueError, "Existing ComfyUI job"):
                restored.prepare(media(1))
        self.assertEqual(len(FakeComfy.prompts), 0)

    def test_missing_nodes_block_before_any_post(self):
        FakeComfy.allow_nodes = False
        with mock.patch("comfyui_web_jobs.probe_seconds", return_value=3.0):
            self.jobs.prepare(media(1))
        with self.assertRaisesRegex(ValueError, "Openjutsu preflight NO_GO"):
            self.jobs.start()
        self.assertEqual(self.jobs.public()["status"], "PREPARED")
        self.assertEqual(len(FakeComfy.prompts), 0)

    def test_missing_model_blocks_render_before_post(self):
        FakeComfy.model_missing = True
        with mock.patch("comfyui_web_jobs.probe_seconds", return_value=3):
            self.jobs.prepare(media(1))
        report = self.jobs.check()
        self.assertFalse(report["can_attempt_render"])
        self.assertEqual(report["readiness"]["status"], "NO_GO_MISSING_COMPONENTS")
        with self.assertRaisesRegex(ValueError, "Openjutsu preflight NO_GO"):
            self.jobs.start()
        self.assertEqual(len(FakeComfy.prompts), 0)

    def test_small_gpu_blocks_render_without_wasting_quota(self):
        FakeComfy.gpu_gib = 8
        with mock.patch("comfyui_web_jobs.probe_seconds", return_value=3):
            self.jobs.prepare(media(1))
        report = self.jobs.check()
        self.assertFalse(report["can_attempt_render"])
        self.assertEqual(report["readiness"]["status"], "BELOW_OPENJUTSU_TESTED_BASELINE")
        with self.assertRaisesRegex(ValueError, "Openjutsu preflight NO_GO"):
            self.jobs.start()
        self.assertEqual(len(FakeComfy.prompts), 0)

    def test_http_check_and_origin_protection(self):
        with urlopen(self.url + "/api/comfy/check", timeout=8) as response:
            result = json.load(response)
        self.assertTrue(result["connected"])
        self.assertTrue(result["openjutsu_present"])
        with self.assertRaises(HTTPError) as blocked:
            urlopen(self.post("/api/comfy/resume", headers={"Origin":"https://evil.example"}),timeout=8)
        self.assertEqual(blocked.exception.code, 403)

    def test_multipart_no_missing_or_duplicate_fields(self):
        body, mime = multipart(media(1))
        data = parse_upload(mime, body)
        self.assertEqual(data["role_1"], "the dancer at position 1")
        self.assertIn("workflow", data)
        with self.assertRaisesRegex(ValueError, "Expected multipart"):
            parse_upload("text/plain", b"bad")


if __name__ == "__main__":
    unittest.main()
