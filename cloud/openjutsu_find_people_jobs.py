"""Openjutsu Find People: a real, read-only-to-video SAM3.1+Qwen tracking job.

Operates on a previously PREPARED Furuya Openjutsu job. It never renders a
replacement and never starts on page load. Independent, durable one-shot
receipt; a timeout cannot cause an automatic second /prompt POST. The result
is only a reviewable person list, not approved masks and not a rendered MP4.
Uses the unmodified official Openjutsu people.api.json graph.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import threading
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from uuid import uuid4

from comfyui_local_bridge import api_json, stage, workflow_api
from comfyui_readiness import analyze

SAFE_JSON = re.compile(r"^h3_montage_people_[0-9]+_\.json$")
SAFE_NPZ = re.compile(r"^h3_montage_people_[0-9]+_\.npz$")
ID_RE = re.compile(r"^[a-f0-9-]{36}$")
MAX_BYTES = 6 * 1024 * 1024


def people_output(history: dict, prompt_id: str) -> dict | None:
    entry = history.get(prompt_id)
    if not isinstance(entry, dict):
        return None
    for output in entry.get("outputs", {}).values():
        if not isinstance(output, dict):
            continue
        for file in output.get("files", []) or []:
            if (isinstance(file, dict) and isinstance(file.get("filename"), str)
                    and SAFE_JSON.fullmatch(file["filename"])
                    and file.get("type") == "temp"
                    and file.get("subfolder", "") in ("", ".")):
                return {"filename": file["filename"], "type": "temp", "subfolder": ""}
    return None


def validate_result(raw: dict) -> dict:
    if not isinstance(raw, dict) or not isinstance(raw.get("frames"), int) or raw["frames"] < 1:
        raise ValueError("Find People returned invalid frame count")
    tracks = raw.get("tracks")
    if tracks is not None and (not isinstance(tracks, str) or not SAFE_NPZ.fullmatch(tracks)):
        raise ValueError("Invalid or unsafe ComfyUI tracking-file reference")
    people = raw.get("people")
    if not isinstance(people, list) or len(people) > 2000:
        raise ValueError("Invalid Find People person list")
    out = []
    for appearance in people:
        if not isinstance(appearance, dict):
            raise ValueError("Invalid person appearance object")
        keys = ("track", "start", "end", "role", "pick")
        if any(type(appearance.get(k)) is not int for k in keys):
            raise ValueError("Person appearance IDs and frame bounds must be integers")
        if (appearance["track"] < 0 or appearance["start"] < 0
                or appearance["end"] > raw["frames"]
                or appearance["start"] >= appearance["end"]
                or appearance["role"] < 0 or appearance["pick"] < 0):
            raise ValueError("Invalid person appearance frame range")
        area = appearance.get("area", 0)
        if not isinstance(area, (int, float)) or not 0 <= area <= 1:
            raise ValueError("Invalid person area")
        ranges = appearance.get("on", [])
        if not isinstance(ranges, list) or len(ranges) > 2000:
            raise ValueError("Invalid person visibility intervals")
        for pair in ranges:
            if (not isinstance(pair, list) or len(pair) != 2
                    or any(type(x) is not int for x in pair)
                    or pair[0] < appearance["start"] or pair[1] > appearance["end"]
                    or pair[0] >= pair[1]):
                raise ValueError("Invalid person visibility interval")
        image = appearance.get("image", "")
        if not isinstance(image, str) or not image.startswith("data:image/jpeg;base64,"):
            image = ""
        if len(image) > 180000:
            image = ""
        out.append({k: appearance[k] for k in keys} | {
            "area": area, "on": ranges, "image": image
        })
    return {"schema": "furuya-find-people-review/1", "frames": raw["frames"],
            "tracks": tracks, "people": out,
            "tracking_done": True, "identity_assignments_reviewed": False,
            "rendered_video": False, "source_video_preserved": True,
            "notice": "Tracks are temporary ComfyUI data. They are not automatically applied to Standard/MaxQ generation."}


class PeopleJobs:
    def __init__(self, root: Path, comfy):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.comfy = comfy
        self.lock = threading.RLock()
        self.receipt = self.root / "receipt.json"
        self.review_file = self.root / "people-review.json"
        self.job = {"status": "IDLE"}
        if self.receipt.exists():
            try:
                self.job = json.loads(self.receipt.read_text(encoding="utf-8"))
                if self.job.get("status") == "SUBMITTED":
                    self.job["status"] = "PENDING"
                    self._save()
            except Exception:
                self.job = {"status": "SUBMISSION_UNCERTAIN", "reason": "Corrupt receipt. Never automatically resend."}

    def _save(self):
        self.receipt.write_text(json.dumps(self.job, indent=2, ensure_ascii=False) + "\n",
                                encoding="utf-8")

    def public(self) -> dict:
        with self.lock:
            return {**self.job, "review_ready": self.review_file.is_file()
                    and self.job["status"] == "TRACKS_READY_UNREVIEWED"}

    def graph(self) -> dict:
        graph = workflow_api(Path(__file__).resolve().parents[1] /
                             "workflows/openjutsu_find_people.api.json")
        if graph.get("1", {}).get("class_type") != "VHS_LoadVideo":
            raise ValueError("Unexpected Find People source video node")
        if graph.get("6", {}).get("class_type") != "H3TrackCrops":
            raise ValueError("Unexpected Find People track crops node")
        if graph.get("10", {}).get("class_type") != "H3MontagePeople":
            raise ValueError("Unexpected Find People output node")
        return graph

    def preflight(self) -> dict:
        if not self.comfy.input_dir or not self.comfy.input_dir.is_dir():
            raise ValueError("ComfyUI input directory is not configured")
        graph = self.graph()
        metadata = api_json(self.comfy.server, "/object_info")
        try:
            stats = api_json(self.comfy.server, "/system_stats")
        except Exception:
            stats = {}
        return analyze(graph, metadata, stats)

    def start(self) -> dict:
        with self.lock:
            parent = self.comfy.public()
            if parent["status"] != "PREPARED" or not self.comfy.session:
                raise ValueError("Prepare the original character-swap job first.")
            if self.job["status"] not in ("IDLE", "FAILED", "TRACKS_READY_UNREVIEWED"):
                raise ValueError("Find People submission is still pending or uncertain. No automatic retry.")
            if self.job.get("source_job") == self.comfy.session.name:
                raise ValueError("Find People was already attempted for this prepared job. Do not resubmit.")
            report = self.preflight()
            if not report["can_attempt_render"]:
                raise ValueError("Find People preflight blocked: " + report["status"])
            roles = parent.get("roles", [])
            if not roles or len(roles) > 4:
                raise ValueError("No valid character role assignments")
            graph = self.graph()
            graph["6"]["inputs"]["people"] = "\n".join(
                f"<Subject {i}>: {role}" for i, role in enumerate(roles, 1))
            self.job = {"status": "SUBMISSION_UNCERTAIN",
                        "source_job": self.comfy.session.name,
                        "stage": "ONE_SUBMISSION_ATTEMPT_PLANNED",
                        "requested_roles": roles,
                        "rendered_video": False}
            self.review_file.unlink(missing_ok=True)
            self._save()
            threading.Thread(target=self._submit, args=(graph, self.comfy.session / "source.mp4"),
                             daemon=True).start()
            return self.public()

    def _submit(self, graph: dict, source_file: Path):
        try:
            filename = stage(source_file, self.comfy.input_dir)
            graph["1"]["inputs"]["video"] = filename
            with self.lock:
                self.job["stage"] = "POST_PROMPT_ATTEMPTED"
                self._save()
            result = api_json(self.comfy.server, "/prompt",
                              {"prompt": graph, "client_id": uuid4().hex})
            prompt_id = result.get("prompt_id")
            if not isinstance(prompt_id, str) or not ID_RE.fullmatch(prompt_id):
                raise ValueError("Find People prompt ID missing/invalid; check queue manually")
            with self.lock:
                self.job.update(status="SUBMITTED", prompt_id=prompt_id, stage="TRACKING_IN_PROGRESS")
                self._save()
            self._poll(prompt_id)
        except Exception as exc:
            with self.lock:
                self.job.update(status="PENDING" if self.job.get("prompt_id")
                                else "SUBMISSION_UNCERTAIN",
                                stage="CHECK_COMFYUI_QUEUE_MANUALLY", error=str(exc)[:200])
                self._save()

    def _poll(self, prompt_id: str):
        try:
            for _ in range(120):
                history = api_json(self.comfy.server, "/history/" + prompt_id)
                output = people_output(history, prompt_id)
                if output:
                    req = Request(self.comfy.server + "/view?" + urlencode(output))
                    with urlopen(req, timeout=40) as response:
                        data = response.read(MAX_BYTES + 1)
                        if len(data) > MAX_BYTES:
                            raise ValueError("Find People report exceeds 6MB")
                    review = validate_result(json.loads(data))
                    self.review_file.write_text(json.dumps(review, ensure_ascii=False) + "\n",
                                                encoding="utf-8")
                    with self.lock:
                        self.job.update(status="TRACKS_READY_UNREVIEWED",
                                        stage="REVIEW_ROLE_MATCHES_BEFORE_RENDER",
                                        appearances=len(review["people"]),
                                        frames=review["frames"],
                                        tracking_done=True)
                        self._save()
                    return
                entry = history.get(prompt_id)
                if isinstance(entry, dict) and entry.get("status", {}).get("completed"):
                    raise ValueError("Find People completed without output JSON; check ComfyUI logs")
                time.sleep(5)
            with self.lock:
                self.job.update(status="PENDING", stage="POLL_TIMEOUT_USE_RESUME")
                self._save()
        except Exception as exc:
            with self.lock:
                self.job.update(status="PENDING", stage="CHECK_COMFYUI_TRACKING_JOB",
                                error=str(exc)[:200])
                self._save()

    def resume(self) -> dict:
        with self.lock:
            pid = self.job.get("prompt_id")
            if not isinstance(pid, str) or not ID_RE.fullmatch(pid):
                raise ValueError("No known prompt ID; inspect ComfyUI queue without resubmitting")
            if self.job["status"] not in ("PENDING", "SUBMITTED"):
                raise ValueError("No pending job to resume")
            self.job.update(status="SUBMITTED", stage="POLL_EXISTING_ID_NO_POST")
            self._save()
            threading.Thread(target=self._poll, args=(pid,), daemon=True).start()
            return self.public()

    def review(self) -> dict:
        with self.lock:
            if self.job.get("status") != "TRACKS_READY_UNREVIEWED":
                raise ValueError("No tracking result ready for review")
            return json.loads(self.review_file.read_text(encoding="utf-8"))
