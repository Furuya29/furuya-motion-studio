"""Openjutsu official Find People graph and one-shot ComfyUI transport tests.

Everything here is a synthetic HTTP fixture, NOT GPU, SAM tracking or model
inference. No billing, model download or video generation.
"""
from __future__ import annotations
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock
from urllib.parse import parse_qs, urlsplit
from urllib.request import urlopen, Request
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cloud"))
from comfyui_web_jobs import ComfyJobs
from comfyui_readiness import GIB, MODEL_FIELDS
from openjutsu_find_people_jobs import PeopleJobs, validate_result, people_output
from local_render_gateway import Handler, RenderState
from comfyui_local_bridge import workflow_api

GRAPH = workflow_api(ROOT / "workflows/openjutsu_find_people.api.json")
PID = "6ae31c74-5e9d-43ba-89bd-b1961623f4bf"
REVIEW = {"frames": 72, "tracks": "h3_montage_people_00001_.npz", "people": [{
    "track": 1, "start": 0, "end": 72, "role": 1, "pick": 1,
    "area": .22, "on": [[0, 72]],
    "image": "data:image/jpeg;base64," + "a" * 32,
}]}


class FakePeopleServer(BaseHTTPRequestHandler):
    posts = []
    bad_nodes = False

    def respond(self, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/object_info":
            info = {n["class_type"]: {} for n in GRAPH.values()}
            if self.bad_nodes:
                del info["H3TrackRoles"]
            for cls, fields in MODEL_FIELDS.items():
                if cls in info:
                    selection = {field: [[n["inputs"][field] for n in GRAPH.values()
                        if n["class_type"] == cls and field in n["inputs"]]]
                        for field in fields}
                    info[cls] = {"input": {"required": selection}}
            self.respond(info)
        elif self.path == "/system_stats":
            self.respond({"system": {"ram_total": 96*GIB},
                          "devices": [{"type": "cuda", "name": "Synthetic NVIDIA RTX 4090",
                                       "vram_total": 24*GIB}]})
        elif self.path == "/history/" + PID:
            self.respond({PID: {"status": {"completed": True},
                "outputs": {"10": {"files": [{"filename": "h3_montage_people_00001_.json",
                    "subfolder": "", "type": "temp"}]}}}})
        elif self.path.startswith("/view?"):
            query = parse_qs(urlsplit(self.path).query)
            if query.get("filename") != ["h3_montage_people_00001_.json"]:
                self.send_error(404)
                return
            self.respond(REVIEW)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/prompt":
            self.send_error(404)
            return
        size = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(size))
        self.posts.append(payload)
        self.respond({"prompt_id": PID})

    def log_message(self, *args):
        pass


class FindPeopleTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.input = self.root / "ComfyUI/input"
        self.input.mkdir(parents=True)
        FakePeopleServer.posts = []
        FakePeopleServer.bad_nodes = False
        self.mock_server = ThreadingHTTPServer(("127.0.0.1", 0), FakePeopleServer)
        threading.Thread(target=self.mock_server.serve_forever, daemon=True).start()
        self.addCleanup(self.mock_server.server_close)
        self.addCleanup(self.mock_server.shutdown)
        address = f"http://127.0.0.1:{self.mock_server.server_port}"
        self.comfy = ComfyJobs(self.root / "comfy-jobs", server=address, input_dir=self.input)
        self.people = PeopleJobs(self.root / "people-jobs", self.comfy)

        class Local(Handler):
            pass
        Local.root = ROOT
        Local.state = RenderState(self.root / "viggle")
        Local.comfy = self.comfy
        Local.people = self.people
        self.gateway = ThreadingHTTPServer(("127.0.0.1", 0), Local)
        threading.Thread(target=self.gateway.serve_forever, daemon=True).start()
        self.addCleanup(self.gateway.server_close)
        self.addCleanup(self.gateway.shutdown)
        self.address = f"http://127.0.0.1:{self.gateway.server_port}"

    def prepared(self):
        folder = self.comfy.root / "job-synthetic"
        folder.mkdir()
        (folder / "source.mp4").write_bytes(b"\x00\x00\x00\x18ftypisom" + b"v"*2000)
        self.comfy.session = folder
        self.comfy.job = {"status": "PREPARED", "roles": ["the central dancer"],
                          "characters": 1}
        self.comfy.save()

    def post(self, route, headers=None):
        return Request(self.address + route, data=b"", method="POST",
                       headers={"X-Furuya-Intent":"local-explicit-user-action", **(headers or {})})

    def test_find_people_requires_parent_and_explicit_confirmation(self):
        with self.assertRaisesRegex(ValueError, "Prepare the original"):
            self.people.start()
        self.prepared()
        with self.assertRaises(HTTPError) as exc:
            urlopen(self.post("/api/comfy/people/start"),timeout=5)
        self.assertEqual(exc.exception.code, 400)
        self.assertEqual(FakePeopleServer.posts, [])

    def test_submit_once_and_review_real_official_track_json_protocol(self):
        self.prepared()
        with urlopen(self.post("/api/comfy/people/start",
                 {"X-Furuya-Confirm": "AUTHORIZE_LOCAL_GPU"}),timeout=6) as response:
            first = json.load(response)
        self.assertEqual(first["status"], "SUBMISSION_UNCERTAIN")
        state = None
        for _ in range(100):
            state = self.people.public()
            if state["status"] == "TRACKS_READY_UNREVIEWED":
                break
            time.sleep(.02)
        self.assertEqual(state["status"], "TRACKS_READY_UNREVIEWED", state)
        self.assertEqual(len(FakePeopleServer.posts), 1)
        graph = FakePeopleServer.posts[0]["prompt"]
        self.assertEqual(graph["6"]["inputs"]["people"], "<Subject 1>: the central dancer")
        self.assertTrue(graph["1"]["inputs"]["video"].startswith("furuya_"))
        with urlopen(self.address + "/api/comfy/people/review",timeout=5) as response:
            result = json.load(response)
        self.assertEqual(result["people"][0]["track"], 1)
        self.assertEqual(result["tracks"], "h3_montage_people_00001_.npz")
        self.assertFalse(result["rendered_video"])
        self.assertFalse(result["identity_assignments_reviewed"])
        with self.assertRaises(HTTPError) as repeat:
            urlopen(self.post("/api/comfy/people/start",
                    {"X-Furuya-Confirm":"AUTHORIZE_LOCAL_GPU"}),timeout=5)
        self.assertEqual(repeat.exception.code, 400)
        self.assertEqual(len(FakePeopleServer.posts), 1)
        restored=PeopleJobs(self.people.root,self.comfy)
        self.assertEqual(restored.public()["status"],"TRACKS_READY_UNREVIEWED")
        self.assertEqual(restored.review()["people"][0]["role"],1)

    def test_no_models_or_nodes_blocks_before_prompt(self):
        self.prepared()
        FakePeopleServer.bad_nodes = True
        with self.assertRaisesRegex(ValueError, "preflight blocked"):
            self.people.start()
        self.assertEqual(len(FakePeopleServer.posts), 0)
        self.assertEqual(self.people.public()["status"], "IDLE")

    def test_invalid_tracks_path_not_trusted(self):
        invalid = dict(REVIEW, tracks="../etc/passwd")
        with self.assertRaisesRegex(ValueError, "unsafe"):
            validate_result(invalid)
        invalid = dict(REVIEW, people=[dict(REVIEW["people"][0], start=-1)])
        with self.assertRaisesRegex(ValueError, "frame range"):
            validate_result(invalid)
        forged = {PID: {"outputs":{"10":{"files":[{"filename":"../../secret.json","type":"temp"}]}}}}
        self.assertIsNone(people_output(forged,PID))

    def test_official_graph_is_tracking_only(self):
        self.assertEqual(GRAPH["5"]["class_type"],"SAM3_VideoTrack")
        self.assertEqual(GRAPH["6"]["class_type"],"H3TrackCrops")
        self.assertEqual(GRAPH["9"]["class_type"],"H3TrackRoles")
        self.assertEqual(GRAPH["10"]["class_type"],"H3MontagePeople")
        self.assertNotIn("SaveVideo",{x["class_type"] for x in GRAPH.values()})


if __name__ == "__main__":
    unittest.main()
