#!/usr/bin/env python3
"""Pré-validação estrutural de um piloto de animação.

Não renderiza nada, não abre o PCRA, não certifica identidade visual ou qualidade.
Executar: python tools/animation_pilot/validate_shot_spec.py caminho.json
"""
import argparse
import json
import math
import sys
from pathlib import Path


def _positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _is_vector3(value):
    return (
        isinstance(value, list)
        and len(value) == 3
        and all(isinstance(v, (float, int)) and not isinstance(v, bool) and math.isfinite(v) for v in value)
    )


def validate(spec):
    """Retorna lista de erros verificáveis de estrutura; não realiza QA artístico."""
    errors = []
    if not isinstance(spec, dict):
        return ["raiz deve ser objeto JSON"]
    if spec.get("schema_version") != "pilot-shot-spec/0.1":
        errors.append("schema_version inesperada")
    timeline = spec.get("timeline", {})
    if not isinstance(timeline, dict):
        return errors + ["timeline deve ser objeto"]
    for field in ("fps", "width", "height", "total_frames"):
        if not _positive_int(timeline.get(field)):
            errors.append(f"timeline.{field} deve ser inteiro positivo")
    if timeline.get("interval_convention") != "start_inclusive_end_exclusive":
        errors.append("timeline deve declarar frames [start,end)")

    assets = spec.get("assets", [])
    if not isinstance(assets, list):
        return errors + ["assets deve ser lista"]
    ids = [a.get("id") for a in assets if isinstance(a, dict)]
    registry = {a["id"]: a for a in assets if isinstance(a, dict) and isinstance(a.get("id"), str)}
    if len(ids) != len(set(ids)) or len(ids) != len(assets):
        errors.append("asset IDs duplicados ou inválidos")
    shots = spec.get("shots", [])
    if not isinstance(shots, list) or not shots:
        return errors + ["shots deve ser lista não vazia"]
    expected_start = 0
    shot_ids = set()
    for n, shot in enumerate(shots, 1):
        if not isinstance(shot, dict):
            errors.append(f"shot #{n}: deve ser objeto")
            continue
        shot_id = shot.get("id")
        name = shot_id if isinstance(shot_id, str) and shot_id else f"shot #{n}"
        if not isinstance(shot_id, str) or not shot_id or shot_id in shot_ids:
            errors.append(f"{name}: ID ausente ou repetido")
        shot_ids.add(shot_id)
        start, end = shot.get("start_frame"), shot.get("end_frame")
        if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool) or end <= start:
            errors.append(f"{name}: intervalo de frames inválido")
            continue
        if start != expected_start:
            errors.append(f"{name}: lacuna/sobreposição, início esperado {expected_start}")
        expected_start = end
        refs = shot.get("asset_refs")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{name}: asset_refs obrigatório")
            refs = []
        for ref in refs:
            if ref not in registry:
                errors.append(f"{name}: asset inexistente {ref}")
        camera = shot.get("camera", {})
        if not isinstance(camera, dict):
            camera = {}
        if camera.get("projection") not in ("perspective", "orthographic"):
            errors.append(f"{name}: camera.projection inválida")
        focal = camera.get("focal_length_mm")
        if camera.get("projection") == "perspective" and not (isinstance(focal, (int, float)) and not isinstance(focal, bool) and math.isfinite(focal) and focal > 0):
            errors.append(f"{name}: focal_length_mm inválida")
        keys = camera.get("keyframes")
        if not isinstance(keys, list) or len(keys) < 2:
            errors.append(f"{name}: câmera exige pelo menos 2 keyframes")
        else:
            frames = []
            for key in keys:
                if not isinstance(key, dict) or not isinstance(key.get("frame"), int):
                    errors.append(f"{name}: camera keyframe inválido")
                    continue
                frames.append(key["frame"])
                if not (_is_vector3(key.get("position_m")) and _is_vector3(key.get("look_at_m"))):
                    errors.append(f"{name}: vetor de câmera inválido")
            if len(frames) == len(keys):
                if frames[0] != start or frames[-1] != end - 1 or frames != sorted(set(frames)):
                    errors.append(f"{name}: keyframes devem cobrir o plano, ordenados e sem repetições")
        for constraint in shot.get("constraints", []):
            if not isinstance(constraint, dict):
                errors.append(f"{name}: constraint inválida")
                continue
            prop = constraint.get("prop_id")
            if prop not in refs or registry.get(prop, {}).get("kind") != "prop":
                errors.append(f"{name}: prop não registrado/referenciado: {prop}")
            mode = constraint.get("attachment_mode")
            if mode not in ("world", "bone"):
                errors.append(f"{name}: attachment_mode inválido")
            if constraint.get("anchor_asset_id") not in refs:
                errors.append(f"{name}: anchor_asset_id fora do plano")
            if constraint.get("contact_actor_id") not in refs:
                errors.append(f"{name}: contact_actor_id fora do plano")
            if mode == "bone" and not constraint.get("contact_bone"):
                errors.append(f"{name}: attachment bone exige nome")
        checks = shot.get("qa_required")
        if not isinstance(checks, list) or not checks or len(checks) != len(set(checks)):
            errors.append(f"{name}: qa_required ausente ou duplicado")
        if shot.get("status") not in ("NOT_TESTED", "TESTING", "FAILED", "PASSED_WITH_EVIDENCE"):
            errors.append(f"{name}: status inválido")
    if _positive_int(timeline.get("total_frames")) and expected_start != timeline["total_frames"]:
        errors.append(f"frames totais divergentes: {expected_start} != {timeline['total_frames']}")
    evidence = spec.get("evidence", {})
    if not isinstance(evidence, dict):
        errors.append("evidence deve ser objeto")
    elif evidence.get("pilot_homologated") and not all(evidence.get(field) for field in
            ("mp4_rendered", "source_assets_ready", "ffprobe_verified", "visual_review_passed")):
        errors.append("homologação declarada sem evidências mínimas")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="JSON de shot spec")
    args = parser.parse_args(argv)
    try:
        spec = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERRO: não foi possível ler JSON: {exc}", file=sys.stderr)
        return 2
    errors = validate(spec)
    if errors:
        for error in errors:
            print("ERRO:", error, file=sys.stderr)
        return 1
    print(f"ESTRUTURA OK: {len(spec['shots'])} tomadas; {spec['timeline']['total_frames']} frames. Não é aprovação visual nem renderização.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
