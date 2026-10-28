#!/usr/bin/env python3
"""Prepare an official Viggle-Animate invocation from Furuya clips.

This is a LOCAL/CLOUD adapter, NOT an inference service. By default it only
prints the command. --execute is needed to run existing, downloaded weights.
No downloads, installation, login or paid GPU request is performed.
Official model: https://huggingface.co/Viggle/Viggle-Animate
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def build(args: argparse.Namespace) -> dict:
    checkout = args.checkout.expanduser().resolve()
    model = args.model_dir.expanduser().resolve()
    video = args.video.expanduser().resolve()
    repainted = args.repaint.expanduser().resolve()
    output = args.output.expanduser().resolve()
    entry = checkout / "inference" / "sample.py"
    if not entry.is_file():
        raise ValueError("Official Viggle-Animate inference/sample.py checkout not found.")
    if not model.is_dir():
        raise ValueError("Existing MiniMax-H3 model directory not found. No model will be downloaded.")
    if not any(model.rglob("*.safetensors")):
        raise ValueError("No locally available model .safetensors found. Checkpoint download is not automatic.")
    if not video.is_file() or video.suffix.lower() not in (".mp4", ".webm", ".mov"):
        raise ValueError("Driving video is missing or unsupported.")
    if not repainted.is_file() or repainted.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        raise ValueError("Repainted frame is missing or unsupported.")
    if output.exists():
        raise ValueError("Refusing to overwrite an existing output video.")
    if not output.parent.is_dir():
        raise ValueError("Output parent directory must already exist.")
    if output.suffix.lower() != ".mp4":
        raise ValueError("The output path must end in .mp4")
    cmd = [args.python, str(entry), "--model-dir", str(model),
           "--cond", str(video), "--ref", str(repainted), "--out", str(output)]
    if args.offload:
        cmd += ["--offload"]
    return {
        "schema": "furuya-viggle-inference-preflight/1",
        "status": "READY_TO_EXECUTE" if args.execute else "DRY_RUN",
        "command": cmd, "cwd": str(checkout), "output": str(output),
        "downloads": False, "paid_services": False,
        "caveats": [
            "This does NOT confirm GPU/CPU RAM sufficiency, daily quotas, checkpoint completeness, model license or final image fidelity.",
            "Ref image must be fully repainted from one frame of THIS driving clip, not an unrelated character portrait.",
            "Multi-person tracking and replacement quality are not guaranteed.",
            "The model loads weights and performs GPU inference only when --execute is supplied.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkout", type=Path, required=True, help="Existing Viggle-Animate source checkout")
    p.add_argument("--model-dir", type=Path, required=True, help="Existing MiniMax-H3 weights root")
    p.add_argument("--video", type=Path, required=True, help="driving.mp4")
    p.add_argument("--repaint", type=Path, required=True, help="repainted-ref.png")
    p.add_argument("--output", type=Path, required=True, help="output.mp4 (must not exist)")
    p.add_argument("--python", default=sys.executable, help="Python in the installed model environment")
    p.add_argument("--offload", action="store_true", help="Request CPU offload (very slow)")
    p.add_argument("--execute", action="store_true", help="Explicitly run already-installed model")
    args = p.parse_args(argv)
    try:
        job = build(args)
    except (OSError, ValueError) as e:
        print(json.dumps({"status": "NO_GO", "message": str(e)}, ensure_ascii=False))
        return 2
    print(json.dumps(job, ensure_ascii=False, indent=2))
    if not args.execute:
        return 0
    try:
        return subprocess.run(job["command"], cwd=job["cwd"], check=False).returncode
    except OSError as e:
        print("Cannot start inference:", e, file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
