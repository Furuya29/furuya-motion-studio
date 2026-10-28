#!/usr/bin/env python3
"""Furuya Motion Studio — prepare a SHORT driving clip for video-to-video models.

Zero network, zero GPU, zero paid API. Dry-run by default.
With --execute, uses an EXISTING ffmpeg/ffprobe installation to convert
a user-owned video into driving.mp4 and extract aligned source-ref.png.
Optionally scales a MANUALLY retouched frame into repainted-ref.png.
Does not synthesize new identity or infer missing human motion.

Example:
 python tools/prepare_clip.py --project project.json --video source.mp4 --outdir output
 python tools/prepare_clip.py --project project.json --video source.mp4 --outdir output \
    --repaint edited.png --execute
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path


def die(message: str) -> None:
    raise ValueError(message)


def probe(path: Path, ffprobe: str) -> dict:
    cmd = [ffprobe, "-v", "error", "-show_entries",
           "format=duration:stream=width,height,codec_type",
           "-of", "json", str(path)]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=True)
    data = json.loads(out.stdout)
    video = next((v for v in data.get("streams", [])
                  if v.get("codec_type") == "video"), None)
    if not video:
        die("No video/image stream found: " + str(path))
    return {"width": int(video["width"]), "height": int(video["height"]),
            "duration": float(data.get("format", {}).get("duration", 0) or 0)}


def safe_manifest(path: Path) -> tuple[dict, list[dict]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") not in ("furuya-recast-project/0.7", "furuya-recast-project/0.8"):
        die("Expected a Furuya Recasting v0.7 or v0.8 JSON.")
    video = data.get("video", {})
    for key in ("clipStart", "clipDuration", "width", "height", "duration"):
        if not isinstance(video.get(key), (int, float)) or not math.isfinite(video[key]):
            die("Invalid video property: " + key)
    start, duration, total = video["clipStart"], video["clipDuration"], video["duration"]
    if start < 0 or not 0.25 < duration <= 5.2 or start + duration > total + .15:
        die("Clip must last 0.25–5.2 s and lie within original video duration.")
    kfs = data.get("keyframes") or [
        {"time": data.get("keyframe", {}).get("sourceTime", 0),
         "fullRepaintFilename": data.get("keyframe", {}).get("referenceFilename")}]
    if not isinstance(kfs, list) or len(kfs) > 200:
        die("Invalid keyframe list.")
    valid = sorted((k for k in kfs
                    if isinstance(k, dict) and isinstance(k.get("time"), (int, float))
                    and math.isfinite(k["time"]) and start-.001 <= k["time"] <= start+duration+.001),
                   key=lambda k: (not bool(k.get("fullRepaintFilename")), k["time"]))
    if not valid:
        die("No keyframe inside the chosen clip. Mark and save one in the editor.")
    return data, valid


def plan(args: argparse.Namespace) -> dict:
    project = args.project.expanduser().resolve()
    source = args.video.expanduser().resolve()
    outdir = args.outdir.expanduser().resolve()
    if not project.is_file() or not source.is_file():
        die("Project JSON and source video must exist.")
    if not outdir.is_dir():
        die("Output directory must already exist (no automatic filesystem changes).")
    data, frames = safe_manifest(project)
    requested = data["video"]
    ffmpeg = shutil.which(args.ffmpeg)
    ffprobe = shutil.which(args.ffprobe)
    if not ffmpeg or not ffprobe:
        die("ffmpeg and ffprobe must already be installed and in PATH.")
    details = probe(source, ffprobe)
    if (details["width"], details["height"]) != (requested["width"], requested["height"]):
        die("Input video dimensions disagree with saved project.")
    if abs(details["duration"] - requested["duration"]) > 1.25:
        die("Input duration differs substantially from the saved project.")
    start, seconds = requested["clipStart"], requested["clipDuration"]
    keyframe = frames[0]
    relative = max(0., min(seconds-.001, keyframe["time"]-start))
    # Make the emitted clip dimensions acceptable for common 32px latent grids.
    scale = min(1., args.max_dimension / max(details["width"], details["height"]))
    width = max(32, round(details["width"]*scale/32)*32)
    height = max(32, round(details["height"]*scale/32)*32)
    ratio_error = abs(width/height - details["width"]/details["height"])
    if ratio_error > .03:
        die("Aligned output aspect ratio differs too much from original.")
    drive = outdir / "driving.mp4"
    original = outdir / "source-ref.png"
    edited = outdir / "repainted-ref.png"
    used = [drive, original]
    if args.repaint is not None:
        used.append(edited)
    if any(p.exists() for p in used):
        die("An output file already exists; refusing to overwrite: " +
            ", ".join(p.name for p in used if p.exists()))
    clip_cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-n",
                "-ss", str(start), "-i", str(source),
                "-t", str(seconds), "-an",
                "-vf", f"fps=24,scale={width}:{height}:flags=lanczos,format=yuv420p",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                "-movflags", "+faststart", str(drive)]
    source_cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-n",
                  "-ss", str(relative), "-i", str(drive),
                  "-frames:v", "1", str(original)]
    commands = [clip_cmd, source_cmd]
    if args.repaint:
        repaint_path = args.repaint.expanduser().resolve()
        if not repaint_path.is_file():
            die("Edited reference frame does not exist.")
        ref = probe(repaint_path, ffprobe)
        if abs(ref["width"]/ref["height"] - width/height) > .035:
            die("Edited image has a different aspect ratio from the driving clip.")
        commands.append([ffmpeg, "-hide_banner", "-loglevel", "error", "-n",
                         "-i", str(repaint_path), "-frames:v", "1",
                         "-vf", f"scale={width}:{height}:flags=lanczos",
                         str(edited)])
    return {
        "schema": "furuya-clip-preflight/1",
        "ready_for_preparation": True,
        "mode": "EXECUTE" if args.execute else "DRY_RUN",
        "clip_source": str(source),
        "start": start, "duration_seconds": seconds, "reference_absolute_time": keyframe["time"],
        "reference_relative_time": round(relative, 4),
        "output_resolution": [width, height],
        "output_dimension_multiple_of_32": True,
        "source_aspect_ratio_difference": round(ratio_error, 5),
        "has_manually_repainted_frame": bool(args.repaint),
        "commands": commands,
        "expected": [str(p) for p in used],
        "privacy": "No uploads, no model downloads, no paid APIs.",
        "generation_status": "PREPARATION_ONLY",
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project", required=True, type=Path)
    p.add_argument("--video", required=True, type=Path)
    p.add_argument("--outdir", required=True, type=Path)
    p.add_argument("--repaint", type=Path, help="Existing final repainted frame, NOT the PNG overlay draft")
    p.add_argument("--max-dimension", type=int, choices=(512, 768, 1024), default=768)
    p.add_argument("--ffmpeg", default="ffmpeg")
    p.add_argument("--ffprobe", default="ffprobe")
    p.add_argument("--execute", action="store_true", help="Opt-in to CPU video transcoding")
    args = p.parse_args(argv)
    try:
        job = plan(args)
    except (ValueError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as e:
        print(json.dumps({"status": "NO_GO", "error": str(e)}, ensure_ascii=False))
        return 2
    print(json.dumps(job, ensure_ascii=False, indent=2))
    if not args.execute:
        return 0
    for i, command in enumerate(job["commands"]):
        result = subprocess.run(command, check=False)
        if result.returncode:
            print(f"ERROR: ffmpeg command {i+1} exited {result.returncode}", file=sys.stderr)
            return result.returncode
    print("PASS: prepared assets (not AI generated).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
