#!/usr/bin/env python3
"""Official Wan-Animate-2 (Aug 2026) motion-transfer adapter.

This model is NOT represented as preserving the Rio crowd; it may create
a new scene. Requires pre-existing official checkout, configured weights,
NVIDIA GPUs and compatible PyTorch/CUDA. Dry-run only by default.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def plan(args) -> dict:
    root = args.checkout.expanduser().resolve()
    image = args.image.expanduser().resolve()
    video = args.video.expanduser().resolve()
    stage = "distilled" if args.distilled else "base"
    entry = root / "infer/wan_animate_2_demo.py"
    config = root / "infer" / ("wan_animate_2_distillation.yaml"
                              if args.distilled else "wan_animate_2.yaml")
    if not entry.is_file() or not config.is_file():
        raise ValueError("Wan-Animate-2 official inference script/config are missing.")
    if not image.is_file() or image.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        raise ValueError("Character image missing.")
    if not video.is_file() or video.suffix.lower() not in (".mp4", ".webm", ".mov"):
        raise ValueError("Driving video missing.")
    if not args.prompt.strip() or len(args.prompt) > 5000:
        raise ValueError("Provide a visual description prompt (up to 5000 chars).")
    if args.require_model_dir and not args.require_model_dir.expanduser().is_dir():
        raise ValueError("Existing model directory not found. No checkpoints will be downloaded.")
    cmd = [args.python, str(entry),
           "--prompt", args.prompt.strip(),
           "--refer-img-file", str(image),
           "--refer-video-file", str(video),
           "--config", str(config)]
    if args.distilled:
        cmd += ["--sample_guide_scale", "1.0", "--step", "10"]
    return {
        "schema": "furuya-wan-animate2-plan/1",
        "engine": "wan_animate2_motion",
        "variant": stage,
        "command": cmd,
        "cwd": str(root / "infer"),
        "environment": {"PYTHONPATH": str(root)},
        "status": "COMMAND_PREPARED_WEIGHTS_AND_GPU_NOT_VERIFIED",
        "execution": "DISABLED" if not args.execute else "OPT_IN_GPU",
        "preserves_original_background": False,
        "output_path": "UPSTREAM_MANAGED; inspect generated MP4 manually",
        "notes": [
            "Official examples use 8x A800 at 720p, 2x A800 at 480p; no small GPU support proven.",
            "Model files and checkout must already exist; config must point to weights.",
            "No motion detector/pose JSON is needed for the model.",
            "This is motion-transfer output; NOT an existing-crowd video replacement.",
        ],
    }


def execution_preflight(args) -> None:
    """Verify model file referenced by the upstream YAML without executing it."""
    import re
    config = args.checkout.expanduser().resolve() / "infer" / (
        "wan_animate_2_distillation.yaml" if args.distilled else "wan_animate_2.yaml"
    )
    text = config.read_text(encoding="utf-8")
    match = re.search(r"^\\s*model_path:\\s*['\\\"]?([^'\\\"#\\r\\n]+)", text, flags=re.MULTILINE)
    if not match:
        raise ValueError("Upstream config lacks a model_path entry; verify weights manually.")
    path = (config.parent / match.group(1).strip()).resolve()
    if not path.is_file() or path.stat().st_size < 1024:
        raise ValueError("Checkpoint referenced in YAML does not exist: " + str(path))
    configured = args.require_model_dir.expanduser().resolve()
    if not path.is_relative_to(configured):
        raise ValueError("Configured model checkpoint is outside --require-model-dir.")
    # The YAML also controls GPU parallelism; never silently modify it.
    matches = re.findall(r"^\\s*(sp_size|sharding_size):\\s*(\\d+)", text, flags=re.MULTILINE)
    params = {name: int(value) for name, value in matches}
    requested = max(params.get("sp_size", 1), params.get("sharding_size", 1))
    try:
        checked = subprocess.run(["nvidia-smi", "--query-gpu=name",
                                  "--format=csv,noheader"],
                                 capture_output=True, text=True, timeout=6, check=True)
        present = len([line for line in checked.stdout.splitlines() if line.strip()])
    except (OSError, subprocess.SubprocessError):
        present = 0
    if present < requested:
        raise ValueError(
            f"Upstream YAML requires at least {requested} CUDA GPUs, found {present}. "
            "Adjust parallel configs only in a compatible validated environment."
        )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, required=True)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--distilled", action="store_true")
    parser.add_argument("--require-model-dir", type=Path)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-free-gpu", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = plan(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if not args.execute:
            return 0
        if not args.confirm_free_gpu or not args.require_model_dir:
            raise ValueError("Execution requires verified local checkpoints and --confirm-free-gpu.")
        execution_preflight(args)
        import os
        env = os.environ.copy()
        env["PYTHONPATH"] = result["environment"]["PYTHONPATH"]
        return subprocess.run(result["command"], cwd=result["cwd"],
                              env=env, check=False).returncode
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "NO_GO", "reason": str(error)},
                         ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
