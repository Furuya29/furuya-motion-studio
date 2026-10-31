#!/usr/bin/env python3
"""Prepare official Openjutsu Advanced (1–4) or MaxQ (1–2) API workflows.

Furuya does not reimplement MiniMax H3, SAM3.1 or the ComfyUI custom nodes.
Input workflow must be exported from the Openjutsu project. This patch follows
its public lib/advanced.ts logic for unused reference pictures only, without
other optional node toggles. No network, GPU, checkpoint downloads or renders.

Source: https://github.com/D3voz/openjutsu/blob/main/lib/advanced.ts
Upstream project is MIT licensed; model weights have separate licenses.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

from comfyui_local_bridge import workflow_api


def find_title(graph: dict, title: str, *, required: bool = True) -> str | None:
    ids = [id for id, node in graph.items() if node.get("_meta", {}).get("title") == title]
    if len(ids) == 1:
        return ids[0]
    if required:
        raise ValueError(f"Expected exactly one Openjutsu node titled {title!r}; found {len(ids)}")
    if len(ids) > 1:
        raise ValueError(f"Ambiguous node title {title!r}")
    return None


def is_link(value: object) -> bool:
    return isinstance(value, list) and len(value) == 2 and isinstance(value[0], str) and value[0].isdigit()


def prepare(graph: dict, *, characters: int, roles: list[str] | None = None) -> tuple[dict, dict]:
    if isinstance(characters, bool) or not isinstance(characters, int) or not 1 <= characters <= 4:
        raise ValueError("Openjutsu Advanced accepts 1–4 characters")
    nodes = json.loads(json.dumps(graph))
    video_id = find_title(nodes, "Source video (people get replaced)")
    if nodes[video_id]["class_type"] != "VHS_LoadVideo":
        raise ValueError("Expected official Openjutsu VHS_LoadVideo source node")
    plan_id = find_title(nodes, "Swap Plan (roles, seed, size)")
    if nodes[plan_id]["class_type"] != "H3AdvancedSwapPlan":
        raise ValueError("Expected Openjutsu H3AdvancedSwapPlan")
    available = sum(1 for node in nodes.values()
                    if node["class_type"] == "LoadImage"
                    and re.fullmatch(r"Picture [1-4]", node.get("_meta", {}).get("title", "")))
    if available not in (2, 4):
        raise ValueError("Openjutsu Advanced workflows must expose 2 (MaxQ) or 4 (Standard) picture nodes")
    if characters > available:
        raise ValueError(f"This Openjutsu workflow supports at most {available} characters")
    pictures = [find_title(nodes, f"Picture {i}") for i in range(1, available + 1)]
    if any(nodes[id]["class_type"] != "LoadImage" for id in pictures):
        raise ValueError("Expected official Openjutsu LoadImage picture nodes")

    # Remove unselected pictures, their scaling and visual descriptions, then
    # remove optional plan inputs pointing to those nodes. This mimics the
    # corresponding subset of upstream pruneAdvanced().
    removed = set()
    for index in range(characters + 1, available + 1):
        image_id = pictures[index-1]
        description_id = find_title(nodes, f"Describe picture {index}")
        scaler = next((
            id for id, node in nodes.items()
            if node["class_type"] == "ImageScaleToMaxDimension"
            and is_link(node["inputs"].get("image"))
            and node["inputs"]["image"][0] == image_id
        ), None)
        if not scaler:
            raise ValueError(f"Cannot find Openjutsu Picture {index} scale node")
        removed.update((image_id, scaler, description_id))
    for id in removed:
        del nodes[id]
    for id, node in nodes.items():
        for key, value in list(node["inputs"].items()):
            if is_link(value) and value[0] in removed:
                if re.match(r"^picture_\d", key) or key.startswith("ref_images."):
                    del node["inputs"][key]
                else:
                    raise ValueError(
                        f"Node {id}.{key} still references a pruned node {value[0]}; "
                        "this workflow is not compatible with safe automatic pruning"
                    )

    if roles is None:
        roles = [""] * characters
    if len(roles) != characters:
        raise ValueError("Provide exactly one role label per character, or none")
    cleaned = [re.sub(r"\s+", " ", r).strip() for r in roles]
    if any(len(r) > 140 for r in cleaned):
        raise ValueError("Each role label must be at most 140 characters")
    if any(cleaned):
        defaults = (["the main person"] if characters == 1 else
                    [f"the person with the {ord}most screen time" for ord in ("", "second ", "third ", "fourth ")][:characters])
        nodes[plan_id]["inputs"]["roles"] = "\n".join(r or defaults[i] for i, r in enumerate(cleaned))
    else:
        nodes[plan_id]["inputs"]["roles"] = ""
    selected_ids = pictures[:characters]
    return nodes, {
        "schema": "furuya-openjutsu-advanced-preflight/1",
        "characters": characters,
        "available_pictures": available,
        "variant": "one_pass_per_person_2slot" if available == 2 else "standard_4slot",
        "source_video_node": video_id,
        "character_image_nodes": selected_ids,
        "swap_plan_node": plan_id,
        "removed_optional_nodes": len(removed),
        "preflight": "API_GRAPH_PATCHED_NOT_GENERATED",
        "tracking_executed": False, "gpu_used": False,
        "notes": "The official H3 and SAM3.1 custom nodes, models and GPU are still mandatory.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow", type=Path, required=True)
    parser.add_argument("--characters", type=int, choices=range(1, 5), required=True)
    parser.add_argument("--roles", nargs="*", default=None)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.output.exists():
            raise ValueError("Refusing to overwrite an existing workflow")
        graph, report = prepare(workflow_api(args.workflow),
                                characters=args.characters, roles=args.roles)
        if not args.output.parent.is_dir():
            raise ValueError("Output parent directory missing")
        args.output.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "NO_GO", "reason": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
