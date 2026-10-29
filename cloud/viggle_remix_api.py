#!/usr/bin/env python3
"""Viggle V1 Video Remix adapter for Furuya Motion Studio.

Offline dry-run by default. The only paid-metered operation is an explicitly
requested --execute, which uses available Viggle API credits (not local GPU).
No API keys are ever written to files or included in logs. One POST at most:
never automatically retry a potentially billable POST after a network failure.
Official guide: https://docs.viggle.ai/v1/guides/quickstart-mix
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from uuid import uuid4

BASE = "https://apis.viggle.ai/v1"
USER_AGENT = "FuruyaMotionStudio/0.8.1"
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def probe_seconds(path: Path, ffprobe: str) -> float:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True, timeout=30,
    )
    seconds = float(json.loads(result.stdout)["format"]["duration"])
    if not math.isfinite(seconds) or not 0.25 <= seconds <= 60:
        raise ValueError("Driving video duration must be between 0.25 and 60 seconds.")
    return seconds


def prepare(image: Path, video: Path, output: Path, ffprobe: str) -> dict:
    image, video, output = (p.expanduser().resolve() for p in (image, video, output))
    if not image.is_file() or image.suffix.lower() not in IMAGE_EXTENSIONS:
        raise ValueError("Original character image must exist as PNG/JPG.")
    if not video.is_file() or video.suffix.lower() not in VIDEO_EXTENSIONS:
        raise ValueError("Driving video must exist as MP4/WebM/MOV.")
    if output.suffix.lower() != ".mp4" or not output.parent.is_dir():
        raise ValueError("Output must end in .mp4 and its parent directory must exist.")
    if output.exists():
        raise ValueError("Refusing to overwrite an existing output video.")
    seconds = probe_seconds(video, ffprobe)
    return {
        "schema": "furuya-viggle-video-remix-plan/1",
        "character": str(image),
        "driving_video": str(video),
        "output": str(output),
        "duration_seconds": round(seconds, 3),
        "estimated_credits": round(seconds, 2),
        "required_available_credits_floor": math.ceil(seconds) + 1,
        "mode": "Video Remix; one character; preserve original background",
        "endpoint": "POST /v1/renders",
        "generation_status": "NOT_STARTED",
        "notes": [
            "The public price is 1 credit per output second; reservation can differ.",
            "No charge occurs in dry-run. --execute submits one metered job using existing API credits.",
            "The credit balance does not reveal whether credits were free or purchased.",
            "No API key is sent to GitHub Pages or written in the output folder.",
            "This workflow does not require repainted-ref.png; that asset remains required for the separate open Viggle-Animate pipeline.",
            "A successfully returned MP4 does not prove Albedo visual fidelity or temporal consistency.",
        ],
    }


def api_json(method: str, url: str, token: str, *, body: bytes | None = None,
             content_type: str | None = None) -> dict:
    headers = {"Authorization": "Bearer " + token, "User-Agent": USER_AGENT,
               "Accept": "application/json"}
    if content_type:
        headers["Content-Type"] = content_type
    request = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=120 if body is not None else 30) as response:
            data = json.load(response)
            if not isinstance(data, dict):
                raise ValueError("API returned a non-object JSON result.")
            return data
    except HTTPError as exc:
        details = exc.read(2048).decode("utf-8", errors="replace")
        raise RuntimeError("Viggle API HTTP %s: %s" % (exc.code, details)) from None


def multipart(image: Path, video: Path) -> tuple[bytes, str]:
    boundary = "furuya-" + uuid4().hex
    chunks = []

    def field(name: str, value: bytes, filename: str | None = None,
              mime: str | None = None) -> None:
        head = '--%s\r\nContent-Disposition: form-data; name="%s"' % (boundary, name)
        if filename:
            head += '; filename="%s"' % re.sub(r'[^A-Za-z0-9_.-]', "_", filename)
        head += "\r\n"
        if mime:
            head += "Content-Type: %s\r\n" % mime
        chunks.append(head.encode("ascii") + b"\r\n" + value + b"\r\n")

    field("image", image.read_bytes(), image.name,
          "image/png" if image.suffix.lower() == ".png" else "image/jpeg")
    field("motion_video", video.read_bytes(), video.name,
          "video/mp4" if video.suffix.lower() == ".mp4" else "video/" +
          ("webm" if video.suffix.lower() == ".webm" else "quicktime"))
    field("background_mode", b"original")
    chunks.append(("--%s--\r\n" % boundary).encode("ascii"))
    return b"".join(chunks), "multipart/form-data; boundary=" + boundary


def download(url: str, output: Path) -> int:
    if urlparse(url).scheme != "https":
        raise ValueError("Refusing to download output from a non-HTTPS URL.")
    part = output.with_name(output.name + ".part")
    if part.exists() or output.exists():
        raise ValueError("Existing .part or .mp4 would be overwritten; aborting.")
    size = 0
    try:
        with urlopen(Request(url, headers={"User-Agent": USER_AGENT}), timeout=120) as response:
            with part.open("xb") as dest:
                while True:
                    buf = response.read(1024 * 1024)
                    if not buf:
                        break
                    size += len(buf)
                    if size > 500 * 1024 * 1024:
                        raise ValueError("Video exceeds 500 MB safety limit.")
                    dest.write(buf)
        if size < 1024:
            raise ValueError("Downloaded video is suspiciously small.")
        part.rename(output)
    finally:
        if part.exists():
            part.unlink()
    return size


def execute(plan: dict, token: str, *, resume_id: str | None, poll_seconds: int) -> dict:
    balance = api_json("GET", BASE + "/credits", token).get("balance")
    if not isinstance(balance, (int, float)) or isinstance(balance, bool):
        raise ValueError("Viggle credit balance is missing or malformed.")
    if balance < plan["required_available_credits_floor"] and not resume_id:
        raise ValueError("Insufficient available credits; no render submitted.")
    output = Path(plan["output"])
    receipt_path = output.with_name(output.name + ".job.json")
    if not resume_id and receipt_path.exists():
        raise ValueError("A receipt already exists: resume the job, do not submit twice.")

    if resume_id:
        if not re.fullmatch(r"render_[A-Za-z0-9_-]+", resume_id):
            raise ValueError("Invalid render id.")
        render_id = resume_id
        print(json.dumps({"status": "RESUMING", "render_id": render_id}))
    else:
        payload, content_type = multipart(Path(plan["character"]), Path(plan["driving_video"]))
        created = api_json("POST", BASE + "/renders", token,
                           body=payload, content_type=content_type)
        render_id = created.get("id")
        if not isinstance(render_id, str) or not re.fullmatch(r"render_[A-Za-z0-9_-]+", render_id):
            raise ValueError("Submission response lacked a valid render id; do not retry blindly.")
        receipt_path.write_text(json.dumps({
            "render_id": render_id, "status": "SUBMITTED",
            "estimated_credits": plan["estimated_credits"],
            "video_output": plan["output"],
        }, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "SUBMITTED", "render_id": render_id}))

    for _ in range(120):
        job = api_json("GET", BASE + "/videos/" + render_id, token)
        status = job.get("status")
        if status in ("failed", "cancelled"):
            raise RuntimeError("Video render %s: %s" % (status, job.get("error")))
        if status == "ready":
            url = job.get("video_url")
            if not isinstance(url, str):
                raise ValueError("Ready response did not contain a video_url.")
            size = download(url, output)
            return {"status": "RENDERED_UNREVIEWED", "render_id": render_id,
                    "bytes": size, "file": str(output),
                    "visual_fidelity_verified": False,
                    "credits_after": api_json("GET", BASE + "/credits", token).get("balance")}
        time.sleep(poll_seconds)
    return {"status": "PENDING", "render_id": render_id,
            "message": "Polling ended. Resume this render id; do not submit a duplicate."}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, required=True, help="Original character PNG/JPG")
    parser.add_argument("--video", type=Path, required=True, help="driving.mp4")
    parser.add_argument("--output", type=Path, required=True, help="New output MP4")
    parser.add_argument("--ffprobe", default="ffprobe")
    parser.add_argument("--execute", action="store_true", help="Submit one metered API job")
    parser.add_argument("--resume-id", help="Existing render id to poll without resubmitting")
    parser.add_argument("--poll-seconds", type=int, default=5)
    args = parser.parse_args(argv)
    try:
        if args.resume_id and not args.execute:
            raise ValueError("--resume-id requires --execute")
        if not 1 <= args.poll_seconds <= 60:
            raise ValueError("--poll-seconds must be 1..60")
        plan = prepare(args.image, args.video, args.output, args.ffprobe)
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        if not args.execute:
            return 0
        token = os.environ.get("VIGGLE_API_KEY", "").strip()
        if not token:
            raise ValueError("VIGGLE_API_KEY is not set in the local environment.")
        result = execute(plan, token, resume_id=args.resume_id,
                         poll_seconds=args.poll_seconds)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["status"] == "RENDERED_UNREVIEWED" else 4
    except (ValueError, RuntimeError, OSError, URLError, subprocess.SubprocessError,
            KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "NO_GO", "reason": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
