#!/usr/bin/env python3
"""Furuya Motion Studio — FaceFusion desktop adapter (experimental).

Prepare the documented FaceFusion headless command, optionally execute it.
No installation, download, persistent service, admin operation, or network
exposure is performed by this wrapper. Default behavior is DRY RUN.

Requirements for --execute:
* A locally installed, functioning FaceFusion checkout and its dependencies.
* An existing source face image and target video with permission to edit.
* Owner must explicitly request --execute. Output must not already exist.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXT = {".mp4", ".mkv", ".webm", ".mov"}
PROVIDERS = ("cpu", "directml", "cuda", "rocm")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--facefusion-dir", type=Path, required=True, help="Existing local FaceFusion checkout")
    p.add_argument("--source", type=Path, required=True, help="Image containing source face")
    p.add_argument("--video", type=Path, required=True, help="Target video")
    p.add_argument("--output", type=Path, required=True, help="New output file")
    p.add_argument("--python", default=sys.executable, help="Python executable in FaceFusion environment")
    p.add_argument("--provider", choices=PROVIDERS, default="cpu", help="Inference backend: begin with cpu")
    p.add_argument("--reference-frame", type=int, default=0, help="Target frame to select reference face")
    p.add_argument("--reference-position", type=int, default=0, help="Face index in reference frame")
    p.add_argument("--scale", type=float, choices=(0.25, 0.5, 0.75, 1.0), default=0.5)
    p.add_argument("--threads", type=int, default=2)
    p.add_argument("--execute", action="store_true", help="Explicitly run FaceFusion (default: dry-run)")
    return p


def build_command(args: argparse.Namespace) -> tuple[list[str], Path]:
    repo = args.facefusion_dir.expanduser().resolve()
    entry = repo / "facefusion.py"
    source = args.source.expanduser().resolve()
    target = args.video.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not repo.is_dir() or not entry.is_file():
        raise ValueError("FaceFusion checkout not found: " + str(entry))
    if not source.is_file() or source.suffix.lower() not in IMAGE_EXT:
        raise ValueError("Source must be an existing face image: " + str(source))
    if not target.is_file() or target.suffix.lower() not in VIDEO_EXT:
        raise ValueError("Target must be an existing video: " + str(target))
    if output.suffix.lower() not in {".mp4", ".webm", ".mkv"}:
        raise ValueError("Output must end with .mp4, .webm, or .mkv")
    if output.exists():
        raise ValueError("Refusing to overwrite an existing output: " + str(output))
    if output == target or output == source:
        raise ValueError("Output cannot be an input file.")
    if not output.parent.is_dir():
        raise ValueError("Output parent folder does not exist: " + str(output.parent))
    if args.reference_frame < 0 or args.reference_position < 0:
        raise ValueError("Reference frame and position must be nonnegative.")
    if not (1 <= args.threads <= 8):
        raise ValueError("Threads must be between 1 and 8 for the limited desktop profile.")
    command = [
        args.python, str(entry), "headless-run",
        "--source-paths", str(source),
        "--target-path", str(target),
        "--output-path", str(output),
        "--processors", "face_swapper",
        "--face-selector-mode", "reference",
        "--reference-frame-number", str(args.reference_frame),
        "--reference-face-position", str(args.reference_position),
        "--execution-providers", args.provider,
        "--execution-thread-count", str(args.threads),
        "--output-video-scale", str(args.scale),
    ]
    return command, repo


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        command, repo = build_command(args)
    except ValueError as exc:
        print(json.dumps({"status": "INVALID_INPUT", "message": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({
        "status": "READY_TO_EXECUTE" if args.execute else "DRY_RUN",
        "engine": "FaceFusion (external, must already be installed)",
        "command": command,
        "quoted": shlex.join(command),
        "cwd": str(repo),
        "provider_requested": args.provider,
        "caveat": "This does not establish a stable identity in a crowd; reference selector may still target the wrong face.",
    }, ensure_ascii=False, indent=2))
    if not args.execute:
        return 0
    try:
        result = subprocess.run(command, cwd=repo, check=False, shell=False)
        if result.returncode:
            print("FaceFusion failed with exit code", result.returncode, file=sys.stderr)
        return result.returncode
    except OSError as exc:
        print("Could not start FaceFusion:", exc, file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
