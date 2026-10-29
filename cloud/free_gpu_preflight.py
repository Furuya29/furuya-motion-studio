#!/usr/bin/env python3
"""Furuya Motion Studio — free GPU environment preflight (NO downloads/charges).

Runs on Colab/Kaggle/own PC using standard Python. Reports hardware only.
Never downloads weights, initializes CUDA kernels, installs packages, or
requests paid resources. A passing result is a CANDIDATE, not a guarantee.
"""
from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def command(args: list[str], seconds: int = 5) -> str:
    try:
        p = subprocess.run(args, text=True, capture_output=True, timeout=seconds, check=False)
        return p.stdout.strip() if p.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def ram_gib() -> float | None:
    try:
        if Path("/proc/meminfo").is_file():
            for line in Path("/proc/meminfo").read_text().splitlines():
                if line.startswith("MemTotal:"):
                    return round(int(line.split()[1]) / 1024**2, 2)
        import ctypes
        class MemoryStatus(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]
        info = MemoryStatus()
        info.dwLength = ctypes.sizeof(info)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(info)):
            return round(info.ullTotalPhys / (1024**3), 2)
    except (OSError, AttributeError, ImportError, ValueError):
        pass
    return None


def gpu_info() -> list[dict]:
    output = command([
        "nvidia-smi", "--query-gpu=name,memory.total,compute_cap",
        "--format=csv,noheader,nounits",
    ])
    result = []
    for line in output.splitlines():
        cols = [x.strip() for x in line.split(",")]
        if len(cols) < 2:
            continue
        try:
            memory_gib = round(float(cols[1]) / 1024, 2)
        except ValueError:
            continue
        result.append({
            "device_name": cols[0],
            "vram_gib": memory_gib,
            "cuda_compute_capability": cols[2] if len(cols) > 2 else None,
        })
    return result


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workdir", default=".", help="Existing directory for disk check")
    p.add_argument("--project", help="Optional exported Furuya v0.7 JSON manifest")
    p.add_argument("--json-out", type=Path, help="Optional report file; never overwrites")
    args = p.parse_args()
    folder = Path(args.workdir).expanduser().resolve()
    if not folder.is_dir():
        p.error("workdir must exist")
    project = None
    if args.project:
        project_path = Path(args.project).expanduser().resolve()
        try:
            data = json.loads(project_path.read_text(encoding="utf-8"))
            if data.get("schema") not in ("furuya-recast-project/0.7", "furuya-recast-project/0.8"):
                p.error("incompatible project schema")
            source = data.get("video", {})
            keyframes = data.get("keyframes", [])
            if not isinstance(keyframes, list):
                p.error("invalid keyframes list")
            legacy_frame = data.get("keyframe") or {}
            if not isinstance(legacy_frame, dict):
                p.error("invalid legacy keyframe")
            characters = data.get("characters", [])
            if not isinstance(characters, list):
                p.error("invalid characters list")
            repaint_candidates = [k for k in keyframes
                                  if isinstance(k, dict) and
                                  (k.get("hasFullRepaint") or k.get("fullRepaintFilename"))]
            project = {"schema": data["schema"],
                       "clip_duration_seconds": source.get("clipDuration"),
                       "input_file": source.get("filename"),
                       "characters": len(characters),
                       "keyframes": len(keyframes),
                       "has_repainted_frame": bool(
                           repaint_candidates or legacy_frame.get("hasFullRepaint")),
                       "repaint_image_loaded": "UNKNOWN_FROM_JSON"}
        except (OSError, ValueError, AttributeError, TypeError) as e:
            p.error(f"Cannot read project: {e}")
    free_disk = round(shutil.disk_usage(folder).free / 1024**3, 2)
    memory = ram_gib()
    gpus = gpu_info()
    largest = max((g["vram_gib"] for g in gpus), default=0.0)
    checks = {
        "viggle_animate_bf16_96_gib": {
            "gpu_memory_sufficient": largest >= 96,
            "status": "HARDWARE_CANDIDATE" if largest >= 96 else "NOT_CONFIRMED_ON_THIS_GPU",
            "notes": "Official repo recommends >=96GB GPU; model files ~69GB; server runtime and free GPU quota remain separate blockers.",
        },
        "wan22_animate_14b_quantized_offload": {
            "gpu_memory_test_candidate": largest >= 12,
            "cpu_ram_test_candidate": memory is not None and memory >= 24,
            "disk_test_candidate": free_disk >= 40,
            "status": "INVESTIGATION_ONLY",
            "notes": "These are rough exploration thresholds, NOT official memory minima. Low VRAM quantized setups can fail or be extremely slow.",
        },
    }
    report = {
        "schema": "furuya-free-gpu-preflight/1",
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "ram_gib": memory,
        "available_disk_gib": free_disk,
        "nvidia_gpus": gpus,
        "project_summary": project,
        "checks": checks,
        "spent_money": 0,
        "downloads_started": False,
        "models_loaded": False,
        "environment_changed": False,
        "caveat": "GPU count/VRAM alone does not verify a working end-to-end pipeline. Free provider policies may change. Test 3-second clip before download of very large weights.",
    }
    result = json.dumps(report, ensure_ascii=False, indent=2)
    print(result)
    if args.json_out:
        target = args.json_out.expanduser().resolve()
        if target.exists():
            p.error("Refusing to overwrite existing report")
        target.write_text(result + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
