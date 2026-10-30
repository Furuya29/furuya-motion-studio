#!/usr/bin/env python3
"""Local, zero-hosting-cost video generation gateway for Furuya Motion Studio.

Runs on 127.0.0.1 only. Serves generate.html and /api endpoints.
Viggle credentials stay in this Python process, never in GitHub Pages/JS.
By default does no remote requests or renders. POST /api/start is the only
route that can submit one credit-metered render, after explicit confirmation.
"""
from __future__ import annotations

import argparse
from email.parser import BytesParser
from email.policy import default
import json
import math
import os
from pathlib import Path
import re
import shutil
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs
from uuid import uuid4

from viggle_remix_api import BASE, api_json, download, probe_seconds
from engine_registry import get, candidates
from auto_router import recommend
from comfyui_web_jobs import ComfyJobs, parse_upload as parse_comfy_upload, UPLOAD_LIMIT as COMFY_UPLOAD_LIMIT

MAX_UPLOAD = 35 * 1024 * 1024
SAFE_RENDER = re.compile(r"^render_[A-Za-z0-9_-]+$")


def parse_form(content_type: str, data: bytes) -> dict:
    if not content_type.lower().startswith("multipart/form-data;"):
        raise ValueError("Expected multipart/form-data.")
    source = b"Content-Type: " + content_type.encode("ascii") + b"\r\nMIME-Version: 1.0\r\n\r\n" + data
    message = BytesParser(policy=default).parsebytes(source)
    if not message.is_multipart():
        raise ValueError("Malformed multipart request.")
    files = {}
    for part in message.iter_parts():
        name = part.get_param("name", header="Content-Disposition")
        payload = part.get_payload(decode=True)
        if name in ("engine_id", "task"):
            if name in files or payload is None or len(payload) > 60:
                raise ValueError("Invalid or duplicate engine/task field.")
            files[name] = payload.decode("utf-8")
            continue
        if name == "background_mode":
            if payload != b"original":
                raise ValueError("Only original background mode is permitted.")
            continue
        if name in files or name not in ("image", "motion_video", "repaint"):
            raise ValueError("Unexpected or duplicate form field.")
        if not part.get_filename() or not payload:
            raise ValueError("Missing file for " + str(name))
        files[name] = payload
    if set(files) - {"image", "motion_video", "repaint"} or not {"image", "motion_video"} <= set(files):
        raise ValueError("Character image and driving video are required.")
    return files


class RenderState:
    def __init__(self, root: Path):
        self.root = root
        self.lock = threading.RLock()
        self.job: dict = {"status": "IDLE"}
        self.session: Path | None = None
        self.image: Path | None = None
        self.motion: Path | None = None
        # Restore the latest receipt; a restart must never enable duplicate billing.
        receipts = sorted(root.glob("job-*/receipt.json"),
                          key=lambda p: p.stat().st_mtime, reverse=True)
        if receipts:
            try:
                previous = json.loads(receipts[0].read_text(encoding="utf-8"))
                if isinstance(previous, dict) and isinstance(previous.get("status"), str):
                    self.session = receipts[0].parent
                    self.image = self.session / "character.png"
                    self.motion = self.session / "driving.mp4"
                    if not self.image.is_file() or not self.motion.is_file():
                        raise ValueError("receipt without original media")
                    self.job = previous
                    if self.job["status"] == "SUBMITTED":
                        self.job["status"] = "PENDING"
                        self.job["stage"] = "AWAITING_MANUAL_RESUME"
                        self.store()
            except (OSError, ValueError, TypeError):
                # Corrupt receipt must fail closed; never silently permit a new POST.
                self.job = {"status": "SUBMISSION_UNCERTAIN",
                            "stage": "RECOVERY_BLOCKED",
                            "error": "Unreadable receipt: review job folder manually."}

    def public(self) -> dict:
        with self.lock:
            details = dict(self.job)
            details["api_key_configured"] = bool(os.getenv("VIGGLE_API_KEY", "").strip())
            details["gateway"] = "LOCAL_ONLY"
            details["output_ready"] = details["status"] == "RENDERED_UNREVIEWED"
            return details

    def store(self) -> None:
        if self.session:
            (self.session / "receipt.json").write_text(
                json.dumps(self.job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def prepare(self, files: dict) -> dict:
        task = files.get("task", "motion_transfer")
        engine_id = files.get("engine_id", "viggle_video_remix")
        engine = get(engine_id)
        if task == "multi_scene_replacement":
            raise ValueError("For multiple people use multicast.html to export assignments. Multi-object tracking and rendering backends are not connected.")
        if task not in engine.tasks:
            raise ValueError("Engine does not support the requested task.")
        if engine.state == "RESEARCH_ONLY" or engine.expected_paid_cost is True:
            raise ValueError("Research-only/paid engine disabled by zero-budget policy.")
        with self.lock:
            if self.job["status"] not in ("IDLE", "PREPARED", "FAILED", "RENDERED_UNREVIEWED"):
                raise ValueError("Previous render is pending or uncertain. Do not submit another.")
            directory = self.root / ("job-" + uuid4().hex)
            directory.mkdir(parents=True, exist_ok=False)
            image = directory / "character.png"
            video = directory / "driving.mp4"
            try:
                image.write_bytes(files["image"])
                video.write_bytes(files["motion_video"])
                if "repaint" in files:
                    (directory / "repainted-ref.png").write_bytes(files["repaint"])
                if len(files["image"]) > 16 * 1024 * 1024 or len(files["motion_video"]) > 24 * 1024 * 1024:
                    raise ValueError("Image/video exceeds this gateway's short-clip safety limits.")
                # Validate file signatures, not filenames. This P0 path uses MP4 H.264.
                if not files["image"].startswith(b"\x89PNG\r\n\x1a\n"):
                    raise ValueError("Albedo character reference must be PNG.")
                if b"ftyp" not in files["motion_video"][:32]:
                    raise ValueError("This P0 gateway requires an MP4 driving video.")
                seconds = probe_seconds(video, "ffprobe")
                if not 0.5 <= seconds <= 5.2:
                    raise ValueError("P0 test duration must be 0.5–5.2 seconds.")
            except Exception:
                shutil.rmtree(directory)
                raise
            self.session = directory
            self.image = image
            self.motion = video
            self.job = {
                "status": "PREPARED",
                "duration_seconds": round(seconds, 3),
                "credit_estimate": round(seconds, 3),
                "required_balance": math.ceil(seconds),
                "route": engine.id,
                "task": task,
                "backend_ready_for_submission": engine.id == "viggle_video_remix",
                "engine_status": engine.state,
                "background_mode": "original",
                "repaint_included": "repaint" in files,
                "notice": "Repaint is saved for Viggle-Animate, not used by Video Remix.",
                "character_source": "ORIGINAL_UPLOAD",
                "stage": "WAITING_FOR_EXPLICIT_CONFIRMATION",
            }
            self.store()
            return self.public()

    def credits(self) -> dict:
        token = os.getenv("VIGGLE_API_KEY", "").strip()
        if not token:
            return {"status": "NOT_CONFIGURED", "available": None}
        result = api_json("GET", BASE + "/credits", token)
        balance = result.get("balance")
        if not isinstance(balance, (int, float)) or isinstance(balance, bool):
            raise ValueError("Invalid balance returned by Viggle.")
        return {"status": "OK", "available": balance,
                "note": "Credit origin (free/purchased) cannot be verified by this endpoint."}

    def start(self) -> dict:
        token = os.getenv("VIGGLE_API_KEY", "").strip()
        if not token:
            raise ValueError("Viggle API key not configured in the local server.")
        with self.lock:
            if self.job.get("route") != "viggle_video_remix" or self.job.get("task") != "motion_transfer":
                raise ValueError("This engine has no live API render backend. Use its guarded offline adapter after verifying free GPU availability.")
            if self.job.get("status") != "PREPARED" or not self.image or not self.motion:
                raise ValueError("Prepare the files first. No retries or duplicate renders.")
            balance = self.credits()["available"]
            if balance < self.job["required_balance"]:
                raise ValueError("Insufficient Viggle credits. No job submitted.")
            self.job.update(status="SUBMISSION_UNCERTAIN",
                            stage="API_REQUEST_STARTED", credits_before=balance)
            self.store()
            runner = threading.Thread(target=self._render, args=(token,), daemon=True)
            runner.start()
            return self.public()

    def _render(self, token: str) -> None:
        from viggle_remix_api import multipart
        try:
            payload, content_type = multipart(self.image, self.motion)
            # One POST only. A timeout must NEVER cause an automatic retry.
            created = api_json("POST", BASE + "/renders", token,
                               body=payload, content_type=content_type)
            render_id = created.get("id")
            if not isinstance(render_id, str) or not SAFE_RENDER.fullmatch(render_id):
                raise ValueError("Submission response missing a valid render id. Check provider before retrying.")
            with self.lock:
                self.job.update(status="SUBMITTED", stage="QUEUED", render_id=render_id)
                self.store()
            self._poll(token, render_id)
        except Exception as error:
            with self.lock:
                # Once a render_id is known, recovery must use GET, never a new POST.
                known_id = self.job.get("render_id")
                if known_id:
                    self.job.update(status="PENDING", stage="POLL_ERROR",
                                    error=str(error)[:400])
                else:
                    # Error after attempting POST may still mean a charge/job exists.
                    self.job.update(status="SUBMISSION_UNCERTAIN", stage="CHECK_PROVIDER",
                                    error=str(error)[:400])
                self.store()

    def _poll(self, token: str, render_id: str) -> None:
        import time
        try:
            for _ in range(120):
                result = api_json("GET", BASE + "/videos/" + render_id, token)
                state = str(result.get("status", "unknown"))
                if state in ("failed", "cancelled"):
                    with self.lock:
                        self.job.update(status="FAILED", stage=state,
                                        error=str(result.get("error", ""))[:400])
                        self.store()
                    return
                if state == "ready":
                    url = result.get("video_url")
                    if not isinstance(url, str):
                        raise ValueError("Ready without video_url.")
                    dest = self.session / "albedo_3s_rendered.mp4"
                    size = download(url, dest)
                    with self.lock:
                        self.job.update(status="RENDERED_UNREVIEWED", stage="FINISHED",
                                        output_bytes=size, visual_validation="PENDING")
                        self.store()
                    return
                with self.lock:
                    self.job["stage"] = state
                time.sleep(5)
            with self.lock:
                self.job.update(status="PENDING", stage="POLL_TIMEOUT")
                self.store()
        except Exception as error:
            with self.lock:
                self.job.update(status="PENDING", stage="POLL_ERROR",
                                error=str(error)[:400])
                self.store()

    def resume(self) -> dict:
        token = os.getenv("VIGGLE_API_KEY", "").strip()
        with self.lock:
            render_id = self.job.get("render_id")
            if not render_id or not SAFE_RENDER.fullmatch(render_id):
                raise ValueError("No known render id. Verify provider externally; never retry POST.")
            if self.job["status"] not in ("PENDING", "SUBMITTED"):
                raise ValueError("This render is not waiting for recovery.")
            self.job.update(status="SUBMITTED", stage="RESUMING_EXISTING_ID")
            self.store()
            threading.Thread(target=self._poll, args=(token, render_id), daemon=True).start()
            return self.public()


class Handler(BaseHTTPRequestHandler):
    state: RenderState
    comfy: ComfyJobs
    root: Path

    def _json(self, data: dict, code: int = 200):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _file(self, path: Path, mime: str, *, download_name: str | None = None):
        raw = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; img-src 'self' data: blob:; media-src 'self' blob:; style-src 'self' 'unsafe-inline'; script-src 'self'")
        if download_name:
            self.send_header("Content-Disposition", 'attachment; filename="' + download_name + '"')
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        route = urlsplit(self.path).path
        if route in ("/", "/generate.html"):
            return self._file(self.root / "generate.html", "text/html; charset=utf-8")
        if route == "/generate.js":
            return self._file(self.root / "generate.js", "text/javascript; charset=utf-8")
        if route == "/routing-policy.json":
            return self._file(self.root / "routing-policy.json", "application/json; charset=utf-8")
        if route == "/multicast.html":
            return self._file(self.root / "multicast.html", "text/html; charset=utf-8")
        if route == "/multicast.js":
            return self._file(self.root / "multicast.js", "text/javascript; charset=utf-8")
        if route == "/api/status":
            return self._json(self.state.public())
        if route == "/api/comfy/status":
            return self._json(self.comfy.public())
        if route == "/api/comfy/check":
            return self._json(self.comfy.check())
        if route == "/api/comfy/result":
            output = self.comfy.result_path()
            if output:
                mime = "video/mp4" if output.suffix == ".mp4" else "video/webm"
                return self._file(output, mime, download_name=output.name)
            return self._json({"error": "No verified received video available"}, 404)
        if route == "/api/recommend":
            params = parse_qs(urlsplit(self.path).query)
            try:
                if any(len(values) != 1 for values in params.values()):
                    raise ValueError("Duplicate route inputs are not allowed.")
                if set(params) - {"targets", "preserve_scene"}:
                    raise ValueError("Unsupported routing input.")
                count = int(params.get("targets", ["1"])[0])
                scene_raw = params.get("preserve_scene", ["true"])[0]
                if scene_raw not in ("true", "false"):
                    raise ValueError("preserve_scene must be true or false")
                return self._json(recommend(target_count=count,
                                            preserve_original_scene=(scene_raw == "true")))
            except (ValueError, TypeError) as exc:
                return self._json({"error": str(exc)[:250]}, 400)
        if route == "/api/engines":
            return self._json({
                "schema": "furuya-engine-catalog/1",
                "scene_replacement": candidates("scene_replacement"),
                "motion_transfer": candidates("motion_transfer"),
                "multi_scene_replacement": candidates("multi_scene_replacement"),
                "notes": "An adapter or listed engine is not proof that GPU, free quota or real inference works.",
            })
        if route == "/api/credits":
            try:
                return self._json(self.state.credits())
            except Exception as err:
                return self._json({"error": str(err)[:300]}, 502)
        if route == "/api/result" and self.state.public()["output_ready"]:
            return self._file(self.state.session / "albedo_3s_rendered.mp4",
                              "video/mp4", download_name="albedo_3s_rendered.mp4")
        self._json({"error": "Not found"}, 404)

    def do_POST(self):
        route = urlsplit(self.path).path
        origin = self.headers.get("Origin")
        expected = {"http://127.0.0.1:" + str(self.server.server_port),
                    "http://localhost:" + str(self.server.server_port)}
        if origin and origin not in expected:
            return self._json({"error": "Cross-origin requests are not allowed."}, 403)
        if self.headers.get("X-Furuya-Intent") != "local-explicit-user-action":
            return self._json({"error": "Explicit request header required."}, 403)
        try:
            if route == "/api/comfy/prepare":
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= COMFY_UPLOAD_LIMIT:
                    raise ValueError("Upload exceeds Openjutsu 48MB limit")
                files = parse_comfy_upload(self.headers.get("Content-Type", ""),
                                           self.rfile.read(length))
                return self._json(self.comfy.prepare(files))
            if route == "/api/comfy/start":
                if self.headers.get("X-Furuya-Confirm") != "AUTHORIZE_LOCAL_GPU":
                    raise ValueError("Explicit local GPU authorization required")
                if self.headers.get("Content-Length", "0") not in ("0", ""):
                    raise ValueError("Unexpected body")
                return self._json(self.comfy.start(), 202)
            if route == "/api/comfy/resume":
                if self.headers.get("Content-Length", "0") not in ("0", ""):
                    raise ValueError("Unexpected body")
                return self._json(self.comfy.resume(), 202)
            if route == "/api/prepare":
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= MAX_UPLOAD:
                    raise ValueError("Upload must be between 1 byte and 35 MB.")
                files = parse_form(self.headers.get("Content-Type", ""), self.rfile.read(length))
                return self._json(self.state.prepare(files))
            if route == "/api/start":
                if self.headers.get("X-Furuya-Confirm") != "AUTHORIZE_EXISTING_CREDITS":
                    raise ValueError("Explicit credit authorization missing.")
                if self.headers.get("Content-Length", "0") not in ("0", ""):
                    raise ValueError("No payload expected.")
                return self._json(self.state.start(), 202)
            if route == "/api/resume":
                return self._json(self.state.resume(), 202)
            return self._json({"error": "Not found"}, 404)
        except Exception as error:
            return self._json({"error": str(error)[:350]}, 400)

    def log_message(self, fmt, *args):
        # Do not log tokens, uploaded form contents, or signed output URLs.
        if not self.path.startswith("/api"):
            super().log_message(fmt, *args)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--workdir", type=Path, default=Path("local-render-jobs"))
    parser.add_argument("--comfy-server", default="http://127.0.0.1:8188",
                        help="Only loopback ComfyUI server permitted")
    parser.add_argument("--comfy-input-dir", type=Path, default=None,
                        help="Existing local ComfyUI/input folder; no installation performed")
    args = parser.parse_args(argv)
    if not 1024 <= args.port <= 65535:
        parser.error("port must be between 1024 and 65535")
    root = Path(__file__).resolve().parents[1]
    for name in ("generate.html", "generate.js"):
        if not (root / name).is_file():
            parser.error("missing UI file " + name)
    workdir = args.workdir.expanduser().resolve()
    workdir.mkdir(parents=True, exist_ok=True)
    class LocalHandler(Handler):
        pass
    LocalHandler.state = RenderState(workdir)
    LocalHandler.comfy = ComfyJobs(workdir / "comfy-jobs",
                                   server=args.comfy_server, input_dir=args.comfy_input_dir)
    LocalHandler.root = root
    server = ThreadingHTTPServer(("127.0.0.1", args.port), LocalHandler)
    print("Furuya local gateway: http://127.0.0.1:%d/generate.html" % args.port, flush=True)
    print("Viggle key configured: %s. No render starts automatically." %
          bool(os.getenv("VIGGLE_API_KEY", "").strip()), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
