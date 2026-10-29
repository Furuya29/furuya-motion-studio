#!/usr/bin/env python3
"""Generate temporal BOUNDING-BOX PROPOSALS from a Furuya cast plan.

CPU-only, stdlib-only. Files are PNG grayscale masks plus an index. These ARE
NOT SAM segmentation masks or identity tracking: interpolating a box through
occlusions does not prove it follows the correct person. One timestamp creates
one marked frame ONLY; frames outside annotated intervals are blank. Outputs
are proposals for checking / SAM prompts, NEVER approved for final replacement.
"""
from __future__ import annotations
import argparse
from bisect import bisect_left
import json
import math
from pathlib import Path
import struct
import sys
import zlib

from validate_multicast_plan import validate

PNG_HEADER = b"\x89PNG\r\n\x1a\n"


def chunk(kind: bytes, data: bytes) -> bytes:
    return (struct.pack(">I", len(data)) + kind + data +
            struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))


def render_png(path: Path, width: int, height: int,
               box: tuple[int, int, int, int] | None) -> None:
    compressor = zlib.compressobj(level=3)
    parts = []
    zero_row = bytes(width)
    if box:
        x0, y0, x1, y1 = box
        mid_row = bytes(x0) + bytes([255]) * (x1-x0) + bytes(width-x1)
    for y in range(height):
        row = mid_row if box and y0 <= y < y1 else zero_row
        parts.append(compressor.compress(b"\x00" + row))
    parts.append(compressor.flush())
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    path.write_bytes(PNG_HEADER + chunk(b"IHDR", ihdr) +
                     chunk(b"IDAT", b"".join(parts)) + chunk(b"IEND", b""))


def bbox_at(anchors: list[dict], t: float, fps: float) -> list[float] | None:
    entries = sorted(anchors, key=lambda a: a["time_seconds"])
    if not entries:
        return None
    if len(entries) == 1:
        return entries[0]["box_xywh"] if abs(t - entries[0]["time_seconds"]) <= 0.5 / fps + 1e-8 else None
    times = [a["time_seconds"] for a in entries]
    pos = bisect_left(times, t)
    if pos < len(times) and abs(times[pos] - t) < 1e-8:
        return entries[pos]["box_xywh"]
    if pos == 0 or pos >= len(entries):
        return None
    a, b = entries[pos-1], entries[pos]
    span = b["time_seconds"]-a["time_seconds"]
    if span <= 0:
        return None
    alpha = (t-a["time_seconds"])/span
    return [v+(w-v)*alpha for v, w in zip(a["box_xywh"],b["box_xywh"])]


def pixels(box: list[float], width: int, height: int) -> tuple[int, int, int, int]:
    x, y, w, h = box
    return (max(0, min(width, math.floor(x*width))),
            max(0, min(height, math.floor(y*height))),
            max(0, min(width, math.ceil((x+w)*width))),
            max(0, min(height, math.ceil((y+h)*height))))


def export(plan: dict, directory: Path, *, fps: float = 24.0,
           max_frames: int = 1800) -> dict:
    verified = validate(plan)
    if not math.isfinite(fps) or not 1 <= fps <= 60:
        raise ValueError("FPS must be between 1 and 60")
    count = round(float(plan["video"]["duration_seconds"])*fps)
    if not 1 <= count <= max_frames:
        raise ValueError("Frame count exceeds offline proposal limit")
    if directory.exists():
        raise ValueError("Output directory already exists. No overwrites or mixing assignments.")
    directory.mkdir(parents=True)
    width, height = plan["video"]["width"], plan["video"]["height"]
    summaries = []
    try:
        for role in plan["targets"]:
            sub = directory / role["id"]
            sub.mkdir()
            proposed = 0
            rows = []
            for frame in range(count):
                t = frame/fps
                box = bbox_at(role["anchors"], t, fps)
                rendered = pixels(box, width, height) if box else None
                name = f"frame_{frame:05d}.png"
                render_png(sub / name, width, height, rendered)
                if rendered is not None:
                    proposed += 1
                rows.append({"frame": frame, "timestamp": round(t, 6),
                             "bbox_proposal": rendered,
                             "mask": str(Path(role["id"]) / name)})
            summaries.append({
                "id": role["id"], "character": role["name"],
                "reference_filename": role["reference_filename"],
                "proposed_frames": proposed, "total_frames": count,
                "frame_map": rows,
            })
        result = {
            "schema": "furuya-multicast-bbox-proposals/1",
            "status": "DRAFT_BOX_PROPOSALS_NOT_SEGMENTATION",
            "source_plan_status": verified["status"],
            "frame_count": count, "fps": fps,
            "size": [width, height],
            "targets": summaries,
            "gpu_used": False, "network_used": False,
            "generative_video_created": False,
            "identity_tracking_validated": False,
            "never_use_as_final_sam_masks_without_review": True,
            "warning": "Rectangle interpolation is NOT person tracking, semantic segmentation, or accurate occlusion handling. Blank outside annotated intervals. These are draft box proposals for a human/SAM pipeline only.",
        }
        (directory / "proposals-index.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        return result
    except BaseException:
        # Do not leave incomplete masks that look like a finished export.
        import shutil
        shutil.rmtree(directory)
        raise


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--fps", type=float, default=24.0)
    parser.add_argument("--max-frames", type=int, default=1800)
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.plan.read_text(encoding="utf-8"))
        report = export(data, args.output_dir, fps=args.fps, max_frames=args.max_frames)
        print(json.dumps({key: value for key, value in report.items() if key != "targets"} |
                         {"proposed_frames_per_target": {r["id"]: r["proposed_frames"] for r in report["targets"]}},
                         ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"status": "NO_GO", "reason": str(e)}, ensure_ascii=False),
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
