#!/usr/bin/env python3
"""Prepare actual 1–5-character Google Flow video-edit inputs, without spending.

Only offline FFprobe/FFmpeg and local file copies. Flow Omni Flash 1.2 is a
hosted browser editor; this module has NO reverse-engineered API or automatic
claim to upload, generate, debit credits or download an AI video. The official
free edit window is <=10s, with estimated 1 credit/sec at 360p or 3 at 720p
(reference: https://support.google.com/flow/answer/16526234, 2026-11-10).
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess

MAX_CLIP_SECONDS = 10.0
DEFAULT_SEGMENT_SECONDS = 8.0
DEFAULT_CREDITS = 50
REFERENCE_NAMES = (
    "Albedo",
    "Shalltear Bloodfallen",
    "Solution Epsilon",
    "Lupusregina Beta",
    "Narberal Gamma (Nabe)",
)
SOURCE_DESCRIPTIONS = (
    "front-center dancer wearing a blue denim shirt",
    "explicitly selected dancer visible in the left-side crowd",
    "explicitly selected dancer behind-left of the main dancer",
    "dancer wearing a grey shirt and cap on the right when visible",
    "dancer with dark sunglasses behind-right of the central dancer",
)
CHARACTER_DESCRIPTIONS = (
    "adult Albedo, golden eyes, very long black hair, white curved horns, "
    "large natural black feathered wings and white/gold dress",
    "Shalltear Bloodfallen, silver hair, red eyes, dark burgundy/black "
    "gothic aristocratic dress",
    "Solution Epsilon, long dark-green hair, gold eyes, black/white battle maid uniform",
    "Lupusregina Beta, red braided hair, playful expression, battle maid uniform",
    "Narberal Gamma, straight black hair, stoic expression, black/white battle maid uniform",
)


def duration_seconds(video: Path, ffprobe: str = "ffprobe") -> float:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
        capture_output=True, text=True, timeout=45, check=True)
    value = float(result.stdout.strip())
    if not math.isfinite(value) or value < 0.5 or value > 600:
        raise ValueError("Source video duration outside 0.5–600s")
    return value


def partition(duration: float, *, seconds: float = DEFAULT_SEGMENT_SECONDS) -> list[tuple[float, float]]:
    if not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration <= 0:
        raise ValueError("Invalid source duration")
    if not 1 <= seconds <= MAX_CLIP_SECONDS:
        raise ValueError("Flow free video-edit segments must be 1–10 seconds")
    chunks = []
    offset = 0.0
    while offset < duration - 1e-5:
        size = round(min(seconds, duration - offset), 3)
        if size < 0.5:
            # The last sub-second sliver belongs to the previous chunk if
            # both still fit in the official 10-second editing window.
            start, prev = chunks[-1]
            if prev + size > MAX_CLIP_SECONDS:
                raise ValueError("A trailing clip is too short; adjust segment length")
            chunks[-1] = (start, round(prev + size, 3))
            break
        chunks.append((round(offset, 3), size))
        offset += size
    return chunks


def estimate_credits(durations: list[float], resolution: int = 360) -> int:
    if resolution not in (360, 720):
        raise ValueError("Only supported credit estimate resolutions: 360, 720")
    per_second = 1 if resolution == 360 else 3
    return sum(math.ceil(seconds * per_second) for seconds in durations)


def make_prompt(names: list[str], positions: list[str], identity: list[str]) -> str:
    lines = [
        "Edit the UPLOADED source video, which depicts a real crowded nighttime street dance.",
        "This is a full-body character replacement edit, NOT a face swap, motion-only",
        "sticker, 2D overlay, cutaway, or independently invented dance sequence.",
        "Keep original camera motion, video timing, choreography, spectators,",
        "street architecture, lighting and synchronized ambience unchanged.",
        "Replace only the specifically selected original on-screen people:",
    ]
    for i, (n, pos, description) in enumerate(zip(names, positions, identity), 1):
        lines.append(f"{i}. {n}: source target = {pos}; resulting identity = {description}.")
    lines.extend([
        "Maintain a consistent high-quality semi-realistic 3D-anime rendering",
        "style for all replacements, realistic cloth/wing/hair secondary motion,",
        "correct depth ordering and occlusions. Do not exchange identities",
        "between targets at any point or insert extra copies of characters.",
        "Unselected crowd members MUST NOT change. If a selected target",
        "cannot be reliably identified or leaves the frame, preserve the",
        "original region instead of inventing a new dancer.",
        "Vertical 9:16 composition. Match original source duration precisely.",
        "Use uploaded character images as reference ingredients; one girl per",
        "assigned source target. Keep the original scene, not a new setting.",
        "If multiple replacements are unstable, prioritize Albedo on the",
        "foreground center dancer and do not damage other people.",
    ])
    return "\n".join(lines) + "\n"


def plan(video: Path, images: list[Path], *, free_balance: int = DEFAULT_CREDITS,
         resolution: int = 360, segment_seconds: float = DEFAULT_SEGMENT_SECONDS,
         pilot_seconds: float = 3, ffprobe: str = "ffprobe") -> dict:
    if not 1 <= len(images) <= 5:
        raise ValueError("Provide 1–5 separate character reference images")
    if not video.is_file() or video.suffix.lower() not in (".mp4", ".mov"):
        raise ValueError("Existing MP4/MOV source video required")
    if not all(p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
               for p in images):
        raise ValueError("Images must exist and be PNG/JPEG/WebP")
    if not isinstance(free_balance, int) or not 0 <= free_balance <= 10000:
        raise ValueError("Balance must be a nonnegative integer")
    seconds = duration_seconds(video, ffprobe)
    clips = partition(seconds, seconds=segment_seconds)
    pilot = min(float(pilot_seconds), seconds, MAX_CLIP_SECONDS)
    if pilot < 0.5:
        raise ValueError("Pilot duration must be at least 0.5 seconds")
    cost_pilot = estimate_credits([pilot], resolution)
    total = estimate_credits([length for _, length in clips], resolution)
    # Do NOT assume the full job can fit into the free daily quota. Allow
    # incremental zero-spend generation over subsequent days.
    if cost_pilot > free_balance:
        raise ValueError(f"Pilot alone costs ~{cost_pilot} credits; free budget {free_balance}")
    return {
        "schema": "furuya-flow-free-job/1",
        "engine": "flow_omni_flash_1_2",
        "mode": "EXISTING_VIDEO_EDIT_WITH_REFERENCES",
        "style_mode": "semi_real_3d",
        "preserve_original_scene": True,
        "target_count": len(images),
        "target_mapping_confirmed": False,
        "clip_seconds": round(seconds, 3),
        "pilot_duration": round(pilot, 3),
        "resolution": resolution,
        "estimated_pilot_credits": cost_pilot,
        "estimated_full_credits_excluding_pilot": total,
        "estimated_all_credits": cost_pilot + total,
        "free_budget_entered_not_checked_live": free_balance,
        "can_prepare_without_spending": True,
        "rendered_by_flow": False,
        "uploaded_to_flow": False,
        "generation_authorized": False,
        "free_credits_verified": False,
        "execution_status": "PREPARED_OFFLINE",
        "segments": [{"start_seconds": start, "seconds": length,
                      "estimated_credits": estimate_credits([length], resolution)}
                     for start, length in clips],
        "characters": [{"name": REFERENCE_NAMES[i],
                         "reference_filename": images[i].name,
                         "source_target_description": SOURCE_DESCRIPTIONS[i]}
                        for i in range(len(images))],
        "notes": "Only create 1 output per submission; never buy extra credits. Five separate"
                 " identities in a crowded scene may require shorter edits or individual refinements."
                 " Flow can modify the original crowd despite this prompt; audit every shot.",
    }


def prepare(video: Path, images: list[Path], output: Path, *,
            free_balance: int = DEFAULT_CREDITS,
            resolution: int = 360, segment_seconds: float = DEFAULT_SEGMENT_SECONDS,
            pilot_seconds: float = 3,
            ffmpeg: str = "ffmpeg", ffprobe: str = "ffprobe",
            dry_run: bool = False) -> dict:
    report = plan(video, images, free_balance=free_balance,
                  resolution=resolution, segment_seconds=segment_seconds,
                  pilot_seconds=pilot_seconds, ffprobe=ffprobe)
    if dry_run:
        return report
    if output.exists():
        raise ValueError("Refusing to overwrite an existing job directory")
    output.mkdir(parents=True)
    try:
        ref_dir = output / "references"
        ref_dir.mkdir()
        names = []
        for i, img in enumerate(images):
            dest = ref_dir / f"{i+1:02d}_{img.name}"
            shutil.copyfile(img, dest)
            names.append(str(dest.relative_to(output)))
        report["reference_paths"] = names
        clip_dir = output / "clips"
        clip_dir.mkdir()
        segments = [("pilot", 0, report["pilot_duration"])] + [
            (f"clip_{i:02d}", s["start_seconds"], s["seconds"])
            for i, s in enumerate(report["segments"], 1)
        ]
        for name, start, seconds in segments:
            dest = clip_dir / f"{name}.mp4"
            subprocess.run(
                [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
                 "-ss", str(start), "-i", str(video), "-t", str(seconds),
                 "-map", "0:v:0", "-map", "0:a?", "-c:v", "libx264",
                 "-preset", "veryfast", "-crf", "22", "-c:a", "aac",
                 "-b:a", "96k", "-movflags", "+faststart", str(dest)],
                capture_output=True, text=True, timeout=240, check=True)
            if not dest.is_file() or dest.stat().st_size == 0:
                raise ValueError("FFmpeg did not produce " + name)
        prompt = make_prompt(
            REFERENCE_NAMES[:len(images)], SOURCE_DESCRIPTIONS[:len(images)],
            CHARACTER_DESCRIPTIONS[:len(images)])
        (output / "flow_prompt.txt").write_text(prompt, encoding="utf-8")
        (output / "flow_job.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return report
    except Exception:
        shutil.rmtree(output)
        raise


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--video", type=Path, required=True)
    p.add_argument("--image", type=Path, nargs="+", required=True,
                   help="Order: Albedo, Shalltear, Solution, Lupusregina, Narberal (1–5)")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--free-balance", type=int, default=DEFAULT_CREDITS)
    p.add_argument("--resolution", type=int, choices=[360, 720], default=360)
    p.add_argument("--segment-seconds", type=float, default=8)
    p.add_argument("--pilot-seconds", type=float, default=3)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    try:
        result = prepare(args.video, args.image, args.output,
                         free_balance=args.free_balance,
                         resolution=args.resolution,
                         segment_seconds=args.segment_seconds,
                         pilot_seconds=args.pilot_seconds, dry_run=args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(json.dumps({"status": "NOT_PREPARED", "reason": str(e)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
