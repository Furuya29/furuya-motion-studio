"""Prepare official Openjutsu Montage graph from explicitly reviewed Find People tracks.

No GPU, networking, mask generation or render here. Takes a valid PeopleJobs
report, only explicit appearance selections, and a character count/role list.
All unselected appearances keep their original identity. Adaptation follows
upstream D3voz/openjutsu/lib/montage.ts pruneMontage(review) semantics.
"""
from __future__ import annotations

import json
import re

from comfyui_local_bridge import workflow_api
from openjutsu_advanced_adapter import prepare as prune_character_images, find_title, is_link
from openjutsu_find_people_jobs import SAFE_NPZ

REQUIRED_KEYS = frozenset({"track", "start", "end", "pick"})
REMOVE_TITLES = (
    "SAM 3.1 track every person (whole video)",
    "Show each track per shot",
    "Who is each track (Qwen3-VL)",
    "Picks without review",
)


def build_reviewed_montage(source: dict, review: dict,
                           characters: int, roles: list[str],
                           selections: list[dict]) -> tuple[dict, dict]:
    if not isinstance(review, dict) or review.get("schema") != "furuya-find-people-review/1":
        raise ValueError("Expected validated Furuya Find People report")
    trackfile = review.get("tracks")
    if not isinstance(trackfile, str) or not SAFE_NPZ.fullmatch(trackfile):
        raise ValueError("No valid ComfyUI .npz track file exists for this review")
    if review.get("identity_assignments_reviewed") is True:
        raise ValueError("Unexpected pre-approved tracking report; require explicit selections")
    appearances = review.get("people", [])
    if not isinstance(appearances, list) or len(appearances) > 2000:
        raise ValueError("Invalid appearance list")
    if not isinstance(selections, list) or len(selections) > len(appearances):
        raise ValueError("Invalid review selections")
    if type(characters) is not int or not 1 <= characters <= 4:
        raise ValueError("Montage supports 1–4 character references")
    if len(roles) != characters or any(not isinstance(x, str) or not x.strip() for x in roles):
        raise ValueError("Every selected character needs an original-video role")

    known = {}
    for a in appearances:
        if not isinstance(a, dict):
            raise ValueError("Invalid appearance")
        k = (a.get("track"), a.get("start"), a.get("end"))
        if any(type(x) is not int for x in k) or k in known:
            raise ValueError("Duplicate or invalid source appearance ID")
        known[k] = a

    selected = {}
    for selection in selections:
        if not isinstance(selection, dict) or set(selection) != REQUIRED_KEYS:
            raise ValueError("Selections require exactly track/start/end/pick")
        k = tuple(selection[x] for x in ("track", "start", "end"))
        pick = selection["pick"]
        if any(type(x) is not int for x in k) or k not in known or k in selected:
            raise ValueError("Unknown, duplicate or malformed appearance selection")
        if type(pick) is not int or not 0 <= pick <= characters:
            raise ValueError("Character reference index out of range")
        selected[k] = pick

    # Deliberate, explicit selections only. No guessed matching is silently
    # promoted to a rendered substitution.
    labels = [{"track": k[0], "start": k[1], "end": k[2], "role": pick}
              for k, pick in selected.items() if pick > 0]
    if not labels:
        raise ValueError("Select at least one person to swap; everyone else stays original")

    graph, meta = prune_character_images(source, characters=characters, roles=roles)
    plan_id = find_title(graph, "Swap Plan (roles, seed, size)")
    if graph[plan_id]["class_type"] != "H3MontagePlan":
        raise ValueError("Expected H3MontagePlan, not Standard or MaxQ")
    track_id = find_title(graph, "Tracks from Find people")
    if graph[track_id]["class_type"] != "H3MontageTracks":
        raise ValueError("Expected H3MontageTracks")
    sam_id = find_title(graph, REMOVE_TITLES[0])
    removed = {find_title(graph, title) for title in REMOVE_TITLES}
    for id in removed:
        del graph[id]
    for node_id, node in graph.items():
        for field, val in list(node["inputs"].items()):
            if is_link(val) and val[0] == sam_id:
                node["inputs"][field] = [track_id, 0]
            elif is_link(val) and val[0] in removed:
                raise ValueError("Orphan link to tracking node " + val[0])
    graph[track_id]["inputs"]["file"] = trackfile
    graph[plan_id]["inputs"]["labels"] = json.dumps(labels, separators=(",", ":"))
    graph[plan_id]["inputs"]["track_data"] = [track_id, 0]
    for node in graph.values():
        for val in node["inputs"].values():
            if is_link(val) and val[0] not in graph:
                raise ValueError("Montage graph contains unresolved ComfyUI node " + val[0])

    return graph, {
        "schema": "furuya-reviewed-montage/1",
        "variant": "reviewed_montage_4slot",
        "characters": characters,
        "source_video_node": meta["source_video_node"],
        "character_image_nodes": meta["character_image_nodes"],
        "track_file": trackfile,
        "reviewed_appearances": len(selected),
        "selected_replacements": len(labels),
        "other_people_preserved_by_selection": True,
        "gpu_used": False,
        "model_run": False,
        "rendered_video": False,
        "review_required_before_submission": False,
        "note": "API workflow prepared only; ComfyUI's temp track file must still exist and match the video.",
    }
