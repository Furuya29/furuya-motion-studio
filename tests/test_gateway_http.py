"""Gateway HTTP smoke tests: localhost only, no external requests/credits."""
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cloud"))
from local_render_gateway import Handler, RenderState


class LocalHTTPTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(__file__).resolve().parents[1]
        class HandlerTest(Handler):
            pass
        HandlerTest.state = RenderState(Path(tmp.name))
        HandlerTest.root = root
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), HandlerTest)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.base = "http://127.0.0.1:" + str(self.server.server_port)

    def test_automatic_routing_never_executes(self):
        with urlopen(self.base + "/api/recommend?targets=1&preserve_scene=true", timeout=5) as response:
            value = json.load(response)
        self.assertEqual(value["preferred_engine"], "openjutsu_advanced")
        self.assertFalse(value["execution_authorized"])
        self.assertFalse(value["can_generate_now"])
        with urlopen(self.base + "/api/recommend?targets=3&preserve_scene=true", timeout=5) as response:
            three = json.load(response)
        self.assertEqual(three["task"], "multi_scene_replacement")
        self.assertEqual(three["preferred_engine"], "openjutsu_advanced")
        with urlopen(self.base + "/routing-policy.json", timeout=5) as response:
            policy = json.load(response)
        self.assertEqual(policy["mode"], "ADVISORY_ONLY")

    def test_automatic_routing_invalid_input(self):
        with self.assertRaises(HTTPError) as error:
            urlopen(self.base + "/api/recommend?targets=50", timeout=5)
        self.assertEqual(error.exception.code, 400)
        with self.assertRaises(HTTPError) as error:
            urlopen(self.base + "/api/recommend?targets=2&preserve_scene=unknown", timeout=5)
        self.assertEqual(error.exception.code, 400)

    def test_multimotor_catalog_http(self):
        with urlopen(self.base + "/api/engines", timeout=5) as response:
            payload = json.load(response)
        self.assertEqual(payload["schema"], "furuya-engine-catalog/1")
        scene = {item["id"] for item in payload["scene_replacement"]}
        motion = {item["id"] for item in payload["motion_transfer"]}
        self.assertIn("wan22_replace", scene)
        self.assertNotIn("viggle_video_remix", scene)
        self.assertIn("wan_animate2_motion", motion)

    def test_ui_status_and_forbidden_post(self):
        with urlopen(self.base + "/api/status", timeout=5) as response:
            state = json.load(response)
        self.assertEqual(state["gateway"], "LOCAL_ONLY")
        self.assertEqual(state["status"], "IDLE")
        with urlopen(self.base + "/generate.html", timeout=5) as response:
            html = response.read().decode("utf-8")
        self.assertIn("Furuya Motion Studio", html)
        self.assertIn("Gerar vídeo com motor selecionado", html)
        request = Request(self.base + "/api/start", data=b"", method="POST")
        with self.assertRaises(HTTPError) as error:
            urlopen(request, timeout=5)
        self.assertEqual(error.exception.code, 403)

    def test_cross_origin_post_rejected(self):
        request = Request(
            self.base + "/api/resume", data=b"", method="POST",
            headers={"Origin": "https://untrusted.example",
                     "X-Furuya-Intent": "local-explicit-user-action"},
        )
        with self.assertRaises(HTTPError) as error:
            urlopen(request, timeout=5)
        self.assertEqual(error.exception.code, 403)


if __name__ == "__main__":
    unittest.main()