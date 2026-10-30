#!/usr/bin/env python3
"""Furuya user-facing ComfyUI/Openjutsu jobs, hosted by local_render_gateway.

The only supported backend is an already-running ComfyUI on loopback.  This
does not install ComfyUI, models, custom nodes, or provision a GPU.  No paid
cloud fallback.  POST /prompt is attempted at most once for each confirmed job.
"""
from __future__ import annotations

from email.parser import BytesParser
from email.policy import default
import json
from pathlib import Path
import re
import shutil
import threading
import time
from uuid import uuid4

from comfyui_local_bridge import (
    api_json, local_base, stage, video_outputs, download, bind, workflow_api,
)
from openjutsu_advanced_adapter import prepare as prepare_openjutsu
from viggle_remix_api import probe_seconds

UPLOAD_LIMIT = 48 * 1024 * 1024
MAX_VIDEO = 25 * 1024 * 1024
MAX_IMAGE = 12 * 1024 * 1024
MAX_WORKFLOW = 2 * 1024 * 1024
RENDER_ID = re.compile(r"^[a-fA-F0-9-]{36}$")


def uploaded_image_suffix(payload: bytes) -> str:
    if payload.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if payload.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if payload[:4] == b"RIFF" and payload[8:12] == b"WEBP":
        return ".webp"
    raise ValueError("Character reference must be PNG, JPEG or WebP")


def parse_upload(mime: str, raw: bytes) -> dict:
    if len(raw) > UPLOAD_LIMIT:
        raise ValueError("Upload exceeds the 48MB limit")
    if not mime.lower().startswith("multipart/form-data;"):
        raise ValueError("Expected multipart form data")
    source = b"Content-Type: " + mime.encode("ascii") + b"\r\nMIME-Version: 1.0\r\n\r\n" + raw
    message = BytesParser(policy=default).parsebytes(source)
    if not message.is_multipart():
        raise ValueError("Invalid multipart format")
    fields = {}
    approved = {"workflow", "motion_video"} | {"image_" + str(i) for i in range(1, 5)} | {
        "role_" + str(i) for i in range(1, 5)}
    for part in message.iter_parts():
        key = part.get_param("name", header="Content-Disposition")
        if key not in approved or key in fields:
            raise ValueError("Unexpected or duplicate field: " + str(key))
        value = part.get_payload(decode=True)
        if value is None:
            raise ValueError("Empty field")
        if key.startswith("role_"):
            if len(value) > 240:
                raise ValueError("Role label exceeds 240 bytes")
            fields[key] = value.decode("utf-8").strip()
        else:
            if not part.get_filename() or not value:
                raise ValueError("File missing: " + key)
            fields[key] = value
    if not {"workflow", "motion_video", "image_1"} <= set(fields):
        raise ValueError("Provide an Openjutsu API workflow, MP4 and the first character image")
    return fields


class ComfyJobs:
    def __init__(self, root: Path, *, server: str, input_dir: Path | None):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.server = local_base(server)
        self.input_dir = input_dir.expanduser().resolve() if input_dir else None
        self.lock = threading.RLock()
        self.session: Path | None = None
        self.job: dict = {"status": "IDLE"}
        receipts = sorted(root.glob("job-*/receipt.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if receipts:
            try:
                job = json.loads(receipts[0].read_text(encoding="utf-8"))
                if not isinstance(job, dict) or "status" not in job:
                    raise ValueError("Incomplete job receipt")
                self.session = receipts[0].parent
                self.job = job
                if job["status"] == "SUBMITTED":
                    self.job.update(status="PENDING", stage="RECOVER_EXISTING_PROMPT")
                    self.save()
            except (OSError, ValueError, TypeError):
                self.job = {"status": "SUBMISSION_UNCERTAIN",
                            "stage": "CORRUPT_RECEIPT_CHECK_MANUALLY"}

    def public(self) -> dict:
        with self.lock:
            return {**self.job, "server": self.server,
                    "configured": bool(self.input_dir and self.input_dir.is_dir()),
                    "mode": "COMFYUI_LOCAL_ONLY",
                    "output_ready": self.job["status"] == "RENDERED_UNREVIEWED"}

    def save(self):
        if self.session:
            (self.session / "receipt.json").write_text(
                json.dumps(self.job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def check(self) -> dict:
        if not self.input_dir or not self.input_dir.is_dir():
            return {"status": "NOT_CONFIGURED", "connected": False,
                    "message": "Start gateway with --comfy-input-dir pointing to ComfyUI/input."}
        try:
            nodes = api_json(self.server, "/object_info")
            result = {"status": "CONNECTED", "connected": True,
                      "class_count": len(nodes),
                      "openjutsu_present": all(k in nodes for k in
                          ("VHS_LoadVideo", "LoadImage", "H3AdvancedSwapPlan")),
                      "weights_verified": False, "gpu_capacity_verified": False}
            try:
                stats = api_json(self.server, "/system_stats")
                devices = stats.get("devices", [])
                result["devices"] = [
                    {"name": str(d.get("name", ""))[:120],
                     "vram_total": d.get("vram_total")}
                    for d in devices[:8] if isinstance(d, dict)
                ]
            except Exception:
                result["devices"] = []
            return result
        except Exception as error:
            return {"status": "OFFLINE", "connected": False,
                    "message": "Local ComfyUI not reachable: " + str(error)[:150]}

    def prepare(self, fields: dict) -> dict:
        with self.lock:
            if self.job["status"] not in ("IDLE", "PREPARED", "FAILED", "RENDERED_UNREVIEWED"):
                raise ValueError("Existing ComfyUI job pending or uncertain; do not resubmit.")
            if not self.input_dir or not self.input_dir.is_dir():
                raise ValueError("Set --comfy-input-dir on the local Furuya gateway first")
            image_ids = [i for i in range(1, 5) if "image_" + str(i) in fields]
            if image_ids != list(range(1, len(image_ids) + 1)):
                raise ValueError("Character references must be sequential (image_1..image_N)")
            count = len(image_ids)
            if not 1 <= count <= 4:
                raise ValueError("Select 1–4 characters")
            if len(fields["motion_video"]) > MAX_VIDEO or b"ftyp" not in fields["motion_video"][:32]:
                raise ValueError("Driving video must be MP4 and below 25MB")
            if len(fields["workflow"]) > MAX_WORKFLOW:
                raise ValueError("Workflow exceeds 2MB")
            if not all(len(fields["image_" + str(i)]) <= MAX_IMAGE for i in image_ids):
                raise ValueError("Character image exceeds 12MB")
            roles = [fields.get("role_" + str(i), "").strip() for i in image_ids]
            if count > 1 and any(not role for role in roles):
                raise ValueError("Describe each person in the original video to prevent identity mix-ups")
            if any(len(role) > 140 for role in roles):
                raise ValueError("Role labels must be at most 140 characters")
            directory = self.root / ("job-" + uuid4().hex)
            directory.mkdir()
            try:
                wf = directory / "openjutsu_api.json"
                wf.write_bytes(fields["workflow"])
                graph, report = prepare_openjutsu(workflow_api(wf),
                                                  characters=count, roles=roles)
                (directory / "prepared_api.json").write_text(
                    json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
                video = directory / "source.mp4"
                video.write_bytes(fields["motion_video"])
                seconds = probe_seconds(video, "ffprobe")
                if not 0.5 <= seconds <= 30:
                    raise ValueError("Openjutsu P0 input duration must be 0.5–30s")
                for i in image_ids:
                    payload = fields["image_" + str(i)]
                    (directory / ("person-" + str(i) + uploaded_image_suffix(payload))).write_bytes(payload)
            except Exception:
                shutil.rmtree(directory)
                raise
            self.session = directory
            self.job = {
                "status": "PREPARED", "stage": "AWAITING_LOCAL_GPU_CONFIRMATION",
                "engine_id": "openjutsu_advanced",
                "task": "multi_scene_replacement" if count > 1 else "scene_replacement",
                "characters": count, "roles": roles,
                "seconds": round(seconds, 3), "source_video_node": report["source_video_node"],
                "image_node_ids": report["character_image_nodes"],
                "tracking_verified": False, "model_weights_verified": False,
                "gpu_verified": False, "inference_executed": False,
                "notice": "Openjutsu graph prepared locally; masks and final video NOT generated.",
            }
            self.save()
            return self.public()

    def start(self) -> dict:
        with self.lock:
            if self.job.get("status") != "PREPARED" or not self.session:
                raise ValueError("Prepare once and do not repeat uncertain renders")
            if not self.input_dir or not self.input_dir.is_dir():
                raise ValueError("No local ComfyUI input directory configured")
            graph = json.loads((self.session / "prepared_api.json").read_text(encoding="utf-8"))
            available = api_json(self.server, "/object_info")
            missing = sorted({node["class_type"] for node in graph.values()} - set(available))
            if missing:
                raise ValueError("Missing Openjutsu/ComfyUI nodes: " + ", ".join(missing)[:350])
            self.job.update(status="SUBMISSION_UNCERTAIN", stage="STAGING_LOCAL_FILES")
            self.save()
            threading.Thread(target=self._worker, daemon=True).start()
            return self.public()

    def _worker(self):
        # This method owns exactly one /prompt POST. A timeout never causes a retry.
        try:
            graph = json.loads((self.session / "prepared_api.json").read_text(encoding="utf-8"))
            source = stage(self.session / "source.mp4", self.input_dir)
            video_id = self.job["source_video_node"]
            graph[video_id]["inputs"]["video"] = source
            for i, node_id in enumerate(self.job["image_node_ids"], 1):
                files = list(self.session.glob("person-" + str(i) + ".*"))
                if len(files) != 1:
                    raise ValueError("Missing character reference file")
                graph[node_id]["inputs"]["image"] = stage(files[0], self.input_dir)
            with self.lock:
                self.job["stage"] = "POST_PROMPT_ATTEMPTED"
                self.save()
            result = api_json(self.server, "/prompt", {"prompt": graph, "client_id": uuid4().hex})
            prompt_id = result.get("prompt_id")
            if not isinstance(prompt_id, str) or not RENDER_ID.fullmatch(prompt_id):
                raise ValueError("Provider did not return a verifiable prompt_id")
            with self.lock:
                self.job.update(status="SUBMITTED", stage="QUEUED", prompt_id=prompt_id)
                self.save()
            self._poll(prompt_id)
        except Exception as error:
            with self.lock:
                if self.job.get("prompt_id"):
                    self.job.update(status="PENDING", stage="CHECK_EXISTING_PROMPT")
                else:
                    self.job.update(status="SUBMISSION_UNCERTAIN", stage="CHECK_COMFY_QUEUE")
                self.job["error"] = str(error)[:350]
                self.save()

    def _poll(self, prompt_id: str):
        try:
            for _ in range(120):
                history = api_json(self.server, "/history/" + prompt_id)
                entry = history.get(prompt_id)
                if isinstance(entry, dict):
                    videos = video_outputs(history, prompt_id)
                    if videos:
                        filename = videos[0]["filename"]
                        suffix = Path(filename).suffix.lower()
                        output = self.session / ("furuya_openjutsu_render" + suffix)
                        size = download(self.server, videos[0], output)
                        seconds = probe_seconds(output, "ffprobe")
                        if not 0 < seconds <= 600:
                            raise ValueError("Output has invalid video duration")
                        with self.lock:
                            self.job.update(status="RENDERED_UNREVIEWED",
                                            stage="VIDEO_RECEIVED_NOT_VISUALLY_VALIDATED",
                                            result_filename=output.name,
                                            output_bytes=size,
                                            output_duration_seconds=round(seconds, 3),
                                            output_received=True,
                                            actual_ai_inference_verified=False,
                                            visual_review="PENDING")
                            self.save()
                        return
                    if entry.get("status", {}).get("completed"):
                        with self.lock:
                            self.job.update(status="FAILED", stage="NO_VIDEO_OUTPUT",
                                            error="ComfyUI completed without video returned in /history; inspect workflow output.")
                            self.save()
                        return
                time.sleep(5)
            with self.lock:
                self.job.update(status="PENDING", stage="POLL_TIMEOUT_EXISTING_PROMPT")
                self.save()
        except Exception as error:
            with self.lock:
                self.job.update(status="PENDING", stage="CHECK_EXISTING_PROMPT",
                                error=str(error)[:350])
                self.save()

    def resume(self) -> dict:
        with self.lock:
            prompt_id = self.job.get("prompt_id")
            if not prompt_id or not RENDER_ID.fullmatch(prompt_id):
                raise ValueError("No prompt_id. Check ComfyUI queue manually; never retry POST.")
            if self.job["status"] not in ("PENDING", "SUBMITTED"):
                raise ValueError("There is no pending prompt to recover")
            self.job.update(status="SUBMITTED", stage="RECOVER_USING_GET_ONLY")
            self.save()
            threading.Thread(target=self._poll, args=(prompt_id,), daemon=True).start()
            return self.public()

    def result_path(self) -> Path | None:
        with self.lock:
            name = self.job.get("result_filename")
            if self.job.get("status") != "RENDERED_UNREVIEWED" or not name:
                return None
            if not re.fullmatch(r"furuya_openjutsu_render\.(mp4|webm)", name):
                return None
            path = self.session / name
            return path if path.is_file() else None
