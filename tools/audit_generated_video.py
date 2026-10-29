#!/usr/bin/env python3
"""Furuya final MP4 audit. Never claims AI identity fidelity from metadata.

Requires existing ffprobe and files. No GPU, network, image models, upload or
billing. Detects source-only copies and disallows automatic quality PASS.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess


REVIEW_KEYS = (
    "correct_person_replaced", "character_face", "hair", "horns", "wings",
    "white_gold_dress", "body_motion", "bystanders_preserved",
    "background_preserved", "occlusion_consistency",
)


def file_hash(file: Path) -> str:
    digest = hashlib.sha256()
    with file.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect(path: Path, ffprobe: str = "ffprobe") -> dict:
    if not path.is_file() or path.stat().st_size < 1024:
        raise ValueError("Expected a non-empty video file at " + str(path))
    command = [ffprobe, "-v", "error", "-count_frames", "-select_streams", "v:0",
               "-show_entries", "format=duration:stream=codec_name,width,height,nb_read_frames,avg_frame_rate",
               "-of", "json", str(path)]
    response = subprocess.run(command, check=True, capture_output=True,
                              text=True, timeout=35)
    data = json.loads(response.stdout)
    streams = data.get("streams") or []
    if not streams:
        raise ValueError("File lacks a decodable video stream.")
    stream = streams[0]
    duration = float(data.get("format", {}).get("duration", 0))
    fps = float(Fraction(stream.get("avg_frame_rate", "0/1")))
    frames_raw = stream.get("nb_read_frames", "N/A")
    frames = int(frames_raw) if str(frames_raw).isdigit() else round(duration * fps)
    if duration <= 0 or fps <= 0 or frames <= 0:
        raise ValueError("Invalid duration, fps or frame count.")
    return {"width": int(stream["width"]), "height": int(stream["height"]),
            "frames": frames, "fps": round(fps, 4),
            "duration": round(duration, 4), "codec": stream.get("codec_name", "unknown")}


def audit(source: Path, result: Path, *, review: dict | None = None,
          ffprobe: str = "ffprobe") -> dict:
    src, out = inspect(source, ffprobe), inspect(result, ffprobe)
    same_sha = file_hash(source) == file_hash(result)
    duration_diff = abs(src["duration"] - out["duration"])
    aspect_diff = abs(src["width"] / src["height"] - out["width"] / out["height"])
    checks = {
        "output_differs_from_input_bytes": not same_sha,
        "duration_similar": duration_diff <= 0.35,
        "portrait_aspect_kept": aspect_diff <= 0.035,
        "has_multiple_frames": out["frames"] >= max(2, int(0.65 * src["frames"])),
    }
    structural_pass = all(checks.values())
    manual = {key: (review or {}).get(key) is True for key in REVIEW_KEYS}
    human_pass = bool(review) and all(manual.values())
    result_status = ("FAIL_STRUCTURAL" if not structural_pass else
                     "PASS_REVIEWED" if human_pass else
                     "RENDERED_NEEDS_VISUAL_REVIEW")
    return {
        "schema": "furuya-video-acceptance/1",
        "source": src, "output": out,
        "same_sha256": same_sha,
        "structural_checks": checks,
        "manual_review_checks": manual,
        "status": result_status,
        "caveats": [
            "Different output bytes do not prove generative replacement.",
            "All ten visual checks must be explicitly reviewed before PASS.",
            "Temporal quality and copyright/consent require independent review.",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--review", type=Path, help="Optional JSON with ten visual booleans")
    parser.add_argument("--ffprobe", default="ffprobe")
    args = parser.parse_args(argv)
    try:
        review = json.loads(args.review.read_text(encoding="utf-8")) if args.review else None
        data = audit(args.source, args.output, review=review, ffprobe=args.ffprobe)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0 if data["status"] != "FAIL_STRUCTURAL" else 2
    except (ValueError, OSError, subprocess.SubprocessError, json.JSONDecodeError, ZeroDivisionError) as err:
        print(json.dumps({"status": "NO_GO", "error": str(err)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
