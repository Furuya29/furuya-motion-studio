#!/usr/bin/env python3
"""Furuya Motion Studio engine registry and honest zero-budget routing.

The registry describes *capabilities*, not proof of a working installation.
CANDIDATE engines require explicit verified availability; no paid fallback.
No downloads, network calls or inference on import or --list.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from typing import Literal

Task = Literal["scene_replacement", "motion_transfer", "multi_scene_replacement"]
State = Literal["INTEGRATED_API_UNVERIFIED", "OFFLINE_ADAPTER", "RESEARCH_ONLY"]


@dataclass(frozen=True)
class Engine:
    id: str
    name: str
    tasks: tuple[str, ...]
    state: State
    execution: str
    scene_preservation: bool
    target_selection: str
    requires_gpu: bool
    account_or_local_weights: bool
    expected_paid_cost: bool | None
    local_entrypoint: str | None
    strengths: str
    limitations: str
    official_source: str

    def public(self) -> dict:
        result = asdict(self)
        result["tasks"] = list(self.tasks)
        return result


ENGINES: tuple[Engine, ...] = (
    Engine(
        id="wan22_replace",
        name="Wan2.2-Animate 14B — replacement",
        tasks=("scene_replacement",),
        state="OFFLINE_ADAPTER",
        execution="OWN_CHECKOUT_GPU_ONLY",
        scene_preservation=True,
        target_selection="OFFICIAL_PREPROCESS_MASK; crowd target UNVERIFIED",
        requires_gpu=True,
        account_or_local_weights=True,
        expected_paid_cost=False,
        local_entrypoint="cloud/wan22_animate_adapter.py",
        strengths="Native replacement mode; pose, face, background, masks, relighting.",
        limitations="Requires official multistage preprocessing and heavy CUDA inference. No confirmed free GPU; user 8GB RX580 is insufficient.",
        official_source="https://github.com/Wan-Video/Wan2.2",
    ),
    Engine(
        id="viggle_animate_open",
        name="Viggle-Animate open — repainted-frame propagation",
        tasks=("scene_replacement",),
        state="OFFLINE_ADAPTER",
        execution="OWN_CHECKOUT_GPU_ONLY",
        scene_preservation=True,
        target_selection="REPAINTED_FRAME; must preserve every unrelated subject",
        requires_gpu=True,
        account_or_local_weights=True,
        expected_paid_cost=False,
        local_entrypoint="cloud/viggle_inference.py",
        strengths="Propagates the same-shot repainted edit; no pose preprocessing during temporal stage.",
        limitations="Model needs very high VRAM and quota; exact crowded-scene quality not tested.",
        official_source="https://huggingface.co/Viggle/Viggle-Animate",
    ),
    Engine(
        id="viggle_video_remix",
        name="Viggle V1 Video Remix — hosted",
        tasks=("motion_transfer",),
        state="INTEGRATED_API_UNVERIFIED",
        execution="CREDIT_METERED_API",
        scene_preservation=False,
        target_selection="ONE_PERSON_MOTION; not reliable crowd-localized replacement",
        requires_gpu=False,
        account_or_local_weights=True,
        expected_paid_cost=None,
        local_entrypoint="cloud/viggle_remix_api.py",
        strengths="Character reference + driving video; existing guarded local API integration.",
        limitations="Uses credits; balance origin free/paid unverified. Background mode may not preserve all bystanders.",
        official_source="https://docs.viggle.ai/v1/guides/quickstart-mix",
    ),
    Engine(
        id="wan_animate2_motion",
        name="Wan-Animate-2 (2026) — video-driven motion",
        tasks=("motion_transfer",),
        state="OFFLINE_ADAPTER",
        execution="OWN_CHECKOUT_GPU_ONLY",
        scene_preservation=False,
        target_selection="FULL_MOTION_VIDEO; may reconstruct scene",
        requires_gpu=True,
        account_or_local_weights=True,
        expected_paid_cost=False,
        local_entrypoint="cloud/wan_animate2_adapter.py",
        strengths="Direct driving video input; strong identity; no older pose extraction; 10-step distilled variant.",
        limitations="Official standard settings tuned to 8x A800 (720p) or 2x A800 (480p); not a validated scene-localized replacement.",
        official_source="https://github.com/Wan-Video/Wan-Animate-2",
    ),
    Engine(
        id="openjutsu_advanced",
        name="Openjutsu Advanced (MiniMax H3 + SAM 3.1)",
        tasks=("multi_scene_replacement",),
        state="OFFLINE_ADAPTER",
        execution="COMFYUI_GPU_CHECKOUT_UNCONFIGURED",
        scene_preservation=True,
        target_selection="SAM_3_1_TRACKS_WITH_ROLE_ASSIGNMENT",
        requires_gpu=True,
        account_or_local_weights=True,
        expected_paid_cost=False,
        local_entrypoint="cloud/openjutsu_advanced_adapter.py",
        strengths="Upstream documents 1–4 roles; Furuya now binds/prunes its official API graph for ComfyUI.",
        limitations="API-graph adaptation is implemented, but MiniMax H3/SAM3.1 weights, ComfyUI nodes and free GPU have NOT been installed or validated.",
        official_source="https://github.com/D3voz/openjutsu",
    ),
    Engine(
        id="henge_tara_multi",
        name="Henge TARA-H3 — multi-character motion/character swap",
        tasks=("multi_scene_replacement",),
        state="RESEARCH_ONLY",
        execution="COMFYUI_GPU_CHECKOUT_UNCONFIGURED",
        scene_preservation=False,
        target_selection="SAM_3_1_TRACKS_AND_REFERENCE_ROLES",
        requires_gpu=True,
        account_or_local_weights=True,
        expected_paid_cost=False,
        local_entrypoint=None,
        strengths="Two-person character replacements in demo; per-subject masks and shot-aware temporal alignment.",
        limitations="Original background is not guaranteed without masked mode; cited showcase used paid RunPod Serverless; not validated at zero cost.",
        official_source="https://github.com/alisson-anjos/Henge",
    ),
    Engine(
        id="wan_vace_masked",
        name="Wan2.1 VACE — masked video inpainting",
        tasks=("multi_scene_replacement",),
        state="RESEARCH_ONLY",
        execution="COMFYUI_GPU_CHECKOUT_UNCONFIGURED",
        scene_preservation=True,
        target_selection="REGION_MASKS_PER_PERSON; serial or composited passes",
        requires_gpu=True,
        account_or_local_weights=True,
        expected_paid_cost=False,
        local_entrypoint=None,
        strengths="Spatially localized video editing can preserve surrounding regions when masks are accurate.",
        limitations="Multi-person support requires masks, pass ordering and compositing; not a native validated one-pass multi-person swap; GPU unverified.",
        official_source="https://comfy.org/workflows/video_wan_vace_inpainting-a1bb55d904c9/",
    ),
    Engine(
        id="higgsfield_genjutsu_object_swap",
        name="Higgsfield Genjutsu — Object Swap (proprietary)",
        tasks=("scene_replacement",),
        state="RESEARCH_ONLY",
        execution="METERED_CLOSED_API",
        scene_preservation=True,
        target_selection="SELECTED_CHARACTER_OR_OBJECT; provider-managed",
        requires_gpu=False,
        account_or_local_weights=True,
        expected_paid_cost=True,
        local_entrypoint=None,
        strengths="Official Object Swap targets a person or item and aims to preserve the rest of the original shot.",
        limitations="Commercial credits/API; no Furuya adapter, free balance or end-to-end output verified. Website video input documented 4–30s, unlike Furuya's 3s P0.",
        official_source="https://higgsfield.ai/genjutsu",
    ),
    Engine(
        id="higgsfield_genjutsu_motion_transfer",
        name="Higgsfield Genjutsu — Motion Transfer (proprietary)",
        tasks=("motion_transfer",),
        state="RESEARCH_ONLY",
        execution="METERED_CLOSED_API",
        scene_preservation=False,
        target_selection="MOTION_VIDEO_AND_CHARACTER_REFERENCES; provider-managed",
        requires_gpu=False,
        account_or_local_weights=True,
        expected_paid_cost=True,
        local_entrypoint=None,
        strengths="Official Motion Transfer recreates character/environment from a reference dance while preserving motion and camera timing.",
        limitations="Commercial credits/API, no free account access or adapter confirmed. Motion Transfer may rebuild the Rio background.",
        official_source="https://open.higgsfield.ai/models/higgsfield/genjutsu/motion-transfer/v1.0/playground",
    ),
    Engine(
        id="kling3_motion",
        name="Kling VIDEO 3.0 Motion Control — candidate",
        tasks=("motion_transfer",),
        state="RESEARCH_ONLY",
        execution="METERED_CLOSED_API",
        scene_preservation=False,
        target_selection="DOMINANT_PERFORMER; one subject",
        requires_gpu=False,
        account_or_local_weights=True,
        expected_paid_cost=True,
        local_entrypoint=None,
        strengths="3–30s image + motion-video control; multi-angle face/identity features.",
        limitations="Paid API usage; no validated cost-zero endpoint. NOT enabled in zero-budget mode.",
        official_source="https://kling.ai/quickstart/motion-control-user-guide",
    ),
)


def get(engine_id: str) -> Engine:
    for engine in ENGINES:
        if engine.id == engine_id:
            return engine
    raise ValueError("Unknown engine: " + str(engine_id))


def candidates(task: Task, *, zero_paid_budget: bool = True) -> list[dict]:
    if task not in ("scene_replacement", "motion_transfer", "multi_scene_replacement"):
        raise ValueError("Unknown task: " + str(task))
    result = []
    for engine in ENGINES:
        if task not in engine.tasks:
            continue
        if zero_paid_budget and engine.expected_paid_cost is True:
            continue
        item = engine.public()
        # A documented API with a free starter quota is not the same as confirmed free credit.
        item["zero_cost_verified"] = False
        item["generation_ready"] = False
        item["reason"] = (
            "A valid runtime, accessible GPU or verified free credits, and live video test are still required."
        )
        result.append(item)
    return result


def manifest(*, task: Task, clip_seconds: float, target_count: int = 1,
             strict_background: bool = True) -> dict:
    if task not in ("scene_replacement", "motion_transfer", "multi_scene_replacement"):
        raise ValueError("Unsupported task")
    if not isinstance(clip_seconds, (int, float)) or not 0.5 <= clip_seconds <= 30:
        raise ValueError("Clip duration must be 0.5–30s")
    if target_count < 1 or target_count > 6:
        raise ValueError("Target count must be 1–6")
    rows = candidates(task)
    return {
        "schema": "furuya-multiengine-plan/1",
        "task": task,
        "duration_seconds": float(clip_seconds),
        "target_count": target_count,
        "strict_background": bool(strict_background),
        "auto_run": False,
        "zero_cost_budget": True,
        "free_inference_verified": False,
        "final_video_rendered": False,
        "candidates": rows,
        "blockers": [
            "No actual source-video/character transfer has completed through any engine yet.",
            "A crowded scene requires target localization and independent bystander preservation checks.",
            "No external paid backend may start without authorization; no paid fallback.",
        ],
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=["scene_replacement", "motion_transfer", "multi_scene_replacement"], default="scene_replacement")
    parser.add_argument("--duration", type=float, default=3)
    parser.add_argument("--targets", type=int, default=1)
    args = parser.parse_args()
    print(json.dumps(manifest(task=args.task, clip_seconds=args.duration,
                              target_count=args.targets), ensure_ascii=False, indent=2))
