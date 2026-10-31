#!/usr/bin/env python3
"""Furuya advisory engine selection for viral-video character replacement.

This is a transparent rules-based routing recommendation, not a trained AI
model or a completed inference. Never invokes GPUs, uploads videos or spends.
All registered engines remain installed/catalogued, including inactive
research candidates.
"""
from __future__ import annotations

import json
from pathlib import Path

from engine_registry import ENGINES, candidates

POLICY_FILE = Path(__file__).resolve().parents[1] / "routing-policy.json"
TASKS = {"scene_replacement", "motion_transfer", "multi_scene_replacement"}


def routing_policy() -> dict:
    policy = json.loads(POLICY_FILE.read_text(encoding="utf-8"))
    if policy.get("schema") != "furuya-routing-policy/1":
        raise ValueError("Unexpected router policy version")
    known = {e.id for e in ENGINES}
    priorities = policy.get("priorities")
    if not isinstance(priorities, dict) or set(priorities) != TASKS:
        raise ValueError("Missing or unknown task priorities")
    for task, ids in priorities.items():
        if not isinstance(ids, list) or len(ids) != len(set(ids)):
            raise ValueError("Duplicate or malformed engine priorities: " + task)
        if not ids or any(i not in known for i in ids):
            raise ValueError("Unknown engine in routing policy")
        if any(task not in next(e.tasks for e in ENGINES if e.id == i) for i in ids):
            raise ValueError("Policy engine is incompatible with task " + task)
    return policy


def recommend(*, target_count: int = 1,
              preserve_original_scene: bool = True) -> dict:
    if isinstance(target_count, bool) or not isinstance(target_count, int) or not 1 <= target_count <= 4:
        raise ValueError("Choose 1–4 people to replace")
    if not isinstance(preserve_original_scene, bool):
        raise ValueError("preserve_original_scene must be a boolean")

    policy = routing_policy()
    if target_count > 1:
        task = "multi_scene_replacement"
    elif preserve_original_scene:
        task = "scene_replacement"
    else:
        task = "motion_transfer"

    known = {e["id"]: e for e in candidates(task, zero_paid_budget=True)}
    priority_ids = policy["priorities"][task]
    ranked = []
    for engine_id in priority_ids:
        engine = known.get(engine_id)
        if engine is None:
            continue
        if engine_id in policy.get("exclusions", []):
            continue
        # Only explicitly available compatible engines can be recommended for execution.
        # All engines are currently candidates, none have verified operational resources.
        ranked.append({
            "id": engine_id, "name": engine["name"],
            "state": engine["state"],
            "generation_ready": bool(engine["generation_ready"]),
            "free_resources_verified": bool(engine["zero_cost_verified"]),
            "scene_preservation": engine["scene_preservation"],
            "reason": engine["strengths"],
            "limitation": engine["limitations"],
        })

    if not ranked:
        raise ValueError("No zero-budget compatible engine remains")

    # This is a PRIORITY for evaluation, not a live/inference-ready choice.
    first = ranked[0]
    return {
        "schema": "furuya-automatic-routing/1",
        "source": "POLICY_RULES_NOT_GENERATIVE_AI",
        "target_count": target_count,
        "preserve_original_scene": preserve_original_scene,
        "task": task,
        "preferred_engine": first["id"],
        "preferred_engine_name": first["name"],
        "evaluation_order": ranked,
        "explanation": policy["explanation"][task],
        "execution_authorized": False,
        "auto_render": False,
        "free_inference_verified": False,
        "can_generate_now": False,
        "next_action": "Validate target tracking, model weights and actually available free GPU/API quota before any rendering.",
        "notice": "Automatic routing suggests an engine; it does not install it, track people, run inference, or use credits.",
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", type=int, default=1)
    parser.add_argument("--recreate-scene", action="store_true",
                        help="Motion transfer may reconstruct the original background")
    args = parser.parse_args()
    print(json.dumps(recommend(target_count=args.targets,
                               preserve_original_scene=not args.recreate_scene),
                     ensure_ascii=False, indent=2))
