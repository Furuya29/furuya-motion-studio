"""Read-only compatibility gate for official Openjutsu Advanced on local ComfyUI.

No downloads, inference, shell calls, API submits, secrets or payments.
Checks selected workflow node classes, listed model filenames and published
Openjutsu *tested* resource baseline (RTX 4060 Ti 16GiB + 64GiB host RAM).
Passing this gate is permission to *attempt* a render, never proof it works.
"""
from __future__ import annotations

from pathlib import PurePosixPath

GIB = 1024 ** 3
# Installed 16GB GPU / 64GB host RAM may report less after reservations and
# decimal-vs-binary unit differences. Treat >=15GiB / >=58GiB as comparable.
# These are advisory thresholds, not documented minimum requirements.
MIN_TESTED_VRAM = 15 * GIB
MIN_TESTED_RAM = 58 * GIB
MODEL_FIELDS = {
    "UNETLoader": {"unet_name": "diffusion_models"},
    "LoraLoaderModelOnly": {"lora_name": "loras"},
    "CLIPLoader": {"clip_name": "text_encoders"},
    "VAELoader": {"vae_name": "vae"},
    "CheckpointLoaderSimple": {"ckpt_name": "checkpoints"},
    "SAMLoader": {"model_name": "sams"},
}
MODEL_INFO_SOURCE = "ComfyUI /object_info node option lists (not model-file integrity)"


def model_choices(metadata: dict, field: str) -> set[str] | None:
    if not isinstance(metadata, dict):
        return None
    inputs = metadata.get("input")
    if not isinstance(inputs, dict):
        return None
    for category in ("required", "optional"):
        fields = inputs.get(category, {})
        if not isinstance(fields, dict):
            continue
        schema = fields.get(field)
        if not isinstance(schema, list) or not schema:
            continue
        choices = schema[0]
        if isinstance(choices, list) and all(isinstance(x, str) for x in choices):
            return set(choices)
    return None


def analyze(graph: dict, node_info: dict, stats: dict | None) -> dict:
    if not isinstance(graph, dict) or not graph or not isinstance(node_info, dict):
        raise ValueError("Need workflow API nodes and ComfyUI object_info")
    missing_nodes = sorted({node["class_type"] for node in graph.values()} - set(node_info))
    model_checks = []
    for node_id, node in graph.items():
        mapping = MODEL_FIELDS.get(node.get("class_type"), {})
        for field, folder in mapping.items():
            name = node.get("inputs", {}).get(field)
            if not isinstance(name, str) or not name.strip():
                continue
            options = model_choices(node_info.get(node["class_type"], {}), field)
            model_checks.append({
                "node_id": node_id, "folder": folder, "filename": name,
                "listed": (name in options) if options is not None else None,
            })
    missing_models = [row for row in model_checks if row["listed"] is False]
    unchecked_models = [row for row in model_checks if row["listed"] is None]
    details = stats if isinstance(stats, dict) else {}
    devices = details.get("devices", [])
    system = details.get("system", {})
    if not isinstance(devices, list):
        devices = []
    if not isinstance(system, dict):
        system = {}
    gpu_records = []
    for d in devices[:12]:
        if not isinstance(d, dict):
            continue
        name = str(d.get("name", ""))[:130]
        is_nvidia = d.get("type") == "cuda" and any(
            word in name.lower() for word in ("nvidia", "geforce", "tesla", "quadro", "rtx", "a100", "h100", "l4 gpu")
        )
        vram = d.get("vram_total", 0)
        if isinstance(vram, bool) or not isinstance(vram, (int, float)):
            vram = 0
        gpu_records.append({"name": name, "type": str(d.get("type", "")),
                            "vram_gib": round(vram / GIB, 2),
                            "nvidia_cuda": is_nvidia,
                            "meets_tested_vram": is_nvidia and vram >= MIN_TESTED_VRAM})
    ram = system.get("ram_total", 0)
    if isinstance(ram, bool) or not isinstance(ram, (int, float)):
        ram = 0
    hw_ok = any(gpu["meets_tested_vram"] for gpu in gpu_records) and ram >= MIN_TESTED_RAM
    if missing_nodes or missing_models:
        status = "NO_GO_MISSING_COMPONENTS"
    elif not hw_ok:
        status = "BELOW_OPENJUTSU_TESTED_BASELINE"
    elif unchecked_models:
        status = "UNVERIFIED_MODEL_CHOICES"
    else:
        status = "PREFLIGHT_PASSED_NOT_RENDERED"
    return {
        "schema": "furuya-openjutsu-readiness/1",
        "status": status,
        "can_attempt_render": status == "PREFLIGHT_PASSED_NOT_RENDERED",
        "nodes_required": len({n["class_type"] for n in graph.values()}),
        "missing_node_classes": missing_nodes,
        "model_checks": model_checks,
        "missing_models": missing_models,
        "unchecked_models": unchecked_models,
        "model_info_source": MODEL_INFO_SOURCE,
        "hardware": {
            "devices": gpu_records, "ram_total_gib": round(ram/GIB, 2),
            "tested_baseline_vram_gib": 16, "tested_baseline_ram_gib": 64,
            "acceptance_threshold_vram_gib": 15, "acceptance_threshold_ram_gib": 58,
            "meets_tested_baseline": hw_ok,
        },
        "output_created": False, "model_integrity_verified": False,
        "free_gpu_verified": False,
        "notice": "Only model names exposed by ComfyUI are checked, not weights or VRAM actually sufficient. 16GiB/64GiB is an upstream tested configuration, not a universal mathematical minimum. No fees or GPU jobs triggered by this check.",
    }
