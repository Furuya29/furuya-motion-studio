#!/usr/bin/env python3
"""Validate an offline, untracked multi-character assignment plan.

A plan assigns character references to *positions at specified timestamps*.
It does not magically track people, segment them, animate them or run GPU.
Dependencies: Python standard library only; no network or file uploads.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import re

SCHEMA = "furuya-multicast-plan/1"
SAFE_ID = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]{0,39}$")
MAX_TARGETS = 4
MAX_ANCHORS_PER_TARGET = 50


def validate(data: object) -> dict:
    problems = []
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ValueError("Unsupported multi-character plan schema")
    source = data.get("video")
    if not isinstance(source, dict):
        raise ValueError("Expected video metadata object")
    duration = source.get("duration_seconds")
    if isinstance(duration, bool) or not isinstance(duration, (float, int)) or not math.isfinite(duration) or duration <= 0 or duration > 600:
        raise ValueError("Expected finite video duration in (0, 600]")
    width, height = source.get("width"), source.get("height")
    if any(isinstance(v, bool) or not isinstance(v, int) or not (32 <= v <= 8192) for v in (width, height)):
        raise ValueError("Invalid video dimensions")
    if not isinstance(source.get("filename"), str) or not source["filename"].lower().endswith((".mp4", ".webm", ".mov")):
        raise ValueError("Video filename missing/unsupported")
    targets = data.get("targets")
    if not isinstance(targets, list) or not (1 <= len(targets) <= MAX_TARGETS):
        raise ValueError("Require 1–4 character targets")
    if data.get("source_immutable") is not True or data.get("tracking_state") != "NOT_RUN":
        raise ValueError("Source preservation and honest tracking state required")
    seen = set()
    anchors_total = 0
    for target in targets:
        if not isinstance(target, dict):
            raise ValueError("Invalid target")
        ident = target.get("id")
        if not isinstance(ident, str) or not SAFE_ID.fullmatch(ident) or ident in seen:
            raise ValueError("Target IDs must be valid and unique")
        seen.add(ident)
        ref = target.get("reference_filename")
        if not isinstance(ref, str) or not ref.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            raise ValueError(f"Target {ident}: image reference filename missing")
        anchors = target.get("anchors")
        if not isinstance(anchors, list) or not 1 <= len(anchors) <= MAX_ANCHORS_PER_TARGET:
            raise ValueError(f"Target {ident}: 1–50 anchor boxes required")
        times = set()
        for anchor in anchors:
            if not isinstance(anchor, dict):
                raise ValueError("Anchor must be an object")
            t = anchor.get("time_seconds")
            coords = anchor.get("box_xywh")
            if isinstance(t, bool) or not isinstance(t, (float, int)) or not math.isfinite(t) or t < 0 or t > duration:
                raise ValueError(f"{ident}: anchor timestamp outside clip")
            if round(t, 3) in times:
                raise ValueError(f"{ident}: duplicate anchor timestamp")
            times.add(round(t, 3))
            if not isinstance(coords, list) or len(coords) != 4:
                raise ValueError(f"{ident}: box must be [x, y, width, height]")
            if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in coords):
                raise ValueError(f"{ident}: nonfinite box coordinates")
            x, y, w, h = coords
            if min(x, y) < 0 or w <= 0 or h <= 0 or x + w > 1.000001 or y + h > 1.000001:
                raise ValueError(f"{ident}: normalized box outside image")
            if w < 0.02 or h < 0.02:
                problems.append(f"{ident}: very small box at {t}s")
            anchors_total += 1
    return {
        "schema": "furuya-multicast-validation/1",
        "status": "ASSIGNMENTS_VALID_NOT_TRACKED",
        "targets": len(targets),
        "anchors": anchors_total,
        "inference_executed": False,
        "target_tracking_verified": False,
        "segmentation_verified": False,
        "gpu_available": False,
        "next_steps": [
            "Use SAM 3/3.1 or SAM 2 to propagate individual identities across the video.",
            "Review masks, overlaps, occlusions and shot-boundary reidentification.",
            "Bind each verified track to its character reference in a multi-person backend.",
            "Render with verified free GPUs and inspect unrelated people and temporal consistency.",
        ],
        "warnings": problems,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    args = parser.parse_args(argv)
    try:
        result = validate(json.loads(args.plan.read_text(encoding="utf-8")))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "NO_GO", "reason": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
