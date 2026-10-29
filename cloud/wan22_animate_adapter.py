#!/usr/bin/env python3
"""Wan2.2 Animate (14B) official replacement / motion adapter.

No automatic download, installation, paid provider or execution.
Uses upstream preprocess_data.py + generate.py. No MediaPipe JSON from Furuya;
the upstream official preprocess is mandatory.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def plan(args) -> dict:
    root = args.checkout.expanduser().resolve()
    ckpt = args.checkpoint.expanduser().resolve()
    video = args.video.expanduser().resolve()
    image = args.image.expanduser().resolve()
    output_dir = args.preprocessed.expanduser().resolve()
    preprocess_script = root / "wan/modules/animate/preprocess/preprocess_data.py"
    generate_script = root / "generate.py"
    mode = args.mode
    if mode not in ("replace", "animate"):
        raise ValueError("Unknown Wan2.2 mode.")
    if not preprocess_script.is_file() or not generate_script.is_file():
        raise ValueError("Wan2.2 official checkout not found; cannot run.")
    if not ckpt.is_dir() or not (ckpt / "process_checkpoint").is_dir():
        raise ValueError("Full checkpoint and process_checkpoint not found. No download will occur.")
    if not video.is_file() or video.suffix.lower() not in (".mp4", ".mov", ".webm"):
        raise ValueError("Driving video not present.")
    if not image.is_file() or image.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        raise ValueError("Character reference not present.")
    if args.stage == "preprocess" and output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("Preprocess destination is not empty. Refusing to overwrite.")
    if args.stage == "render" and not output_dir.is_dir():
        raise ValueError("Upstream preprocess results do not exist. First run the official preprocessing stage.")
    if args.stage == "render" and not any(output_dir.rglob("*")):
        raise ValueError("Preprocess results are empty.")
    if not output_dir.parent.is_dir():
        raise ValueError("Preprocess parent directory does not exist.")
    preprocess = [
        args.python, str(preprocess_script),
        "--ckpt_path", str(ckpt / "process_checkpoint"),
        "--video_path", str(video),
        "--refer_path", str(image),
        "--save_path", str(output_dir),
        "--resolution_area", "1280", "720",
    ]
    if mode == "replace":
        preprocess += ["--iterations", "3", "--k", "7", "--w_len", "1",
                       "--h_len", "1", "--replace_flag"]
    else:
        preprocess += ["--retarget_flag", "--use_flux"]
    render = [
        args.python, str(generate_script),
        "--task", "animate-14B",
        "--ckpt_dir", str(ckpt),
        "--src_root_path", str(output_dir),
        "--refert_num", "1",
    ]
    if mode == "replace":
        render += ["--replace_flag", "--use_relighting_lora"]
    return {
        "schema": "furuya-wan22-adapter/1",
        "engine": "wan22_replace" if mode == "replace" else "wan22_motion",
        "stage": args.stage,
        "command": preprocess if args.stage == "preprocess" else render,
        "cwd": str(root),
        "status": "PREFLIGHT_COMPLETE_NOT_GPU_VERIFIED",
        "execution": "DISABLED" if not args.execute else "OPT_IN_GPU",
        "output_path": "UPSTREAM_MANAGED; locate and audit final render separately",
        "full_character_replacement": mode == "replace",
        "preprocessing_verified": args.stage == "render",
        "notes": [
            "User's 8GB AMD GPU is not qualified for official 14B inferencing.",
            "The Furuya 2D polygon mask is not the official pose/face/background/mask tensor preparation.",
            "No cloud GPU or free quota has been provisioned or confirmed.",
            "Bystanders and the correct target must be evaluated; upstream does not guarantee crowded-scene accuracy.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--preprocessed", type=Path, required=True)
    parser.add_argument("--mode", choices=("replace", "animate"), default="replace")
    parser.add_argument("--stage", choices=("preprocess", "render"), default="preprocess")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-free-gpu", action="store_true",
                        help="Confirm pre-existing sufficient GPU and no paid resources.")
    args = parser.parse_args(argv)
    try:
        job = plan(args)
        print(json.dumps(job, ensure_ascii=False, indent=2))
        if not args.execute:
            return 0
        if not args.confirm_free_gpu:
            raise ValueError("Cannot start inference without --confirm-free-gpu.")
        return subprocess.run(job["command"], cwd=job["cwd"],
                              check=False).returncode
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "NO_GO", "reason": str(error)},
                         ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
