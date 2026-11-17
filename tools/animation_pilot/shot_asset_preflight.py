#!/usr/bin/env python3
"""Read-only asset gate for a real character-animation shot.

Never derives layers from a flattened image and never upgrades approval.
Example:
 python shot_asset_preflight.py --manifest shot.json --root E:/Aenvarath/animation/assets --report report.json
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

SCHEMA = 'aenvarath-shot-assets/1'
APPROVALS = {'chat_approved_unbound', 'production_approved', 'pending'}
ROLES = {'canonical_turnaround', 'shot_still', 'background', 'genga_start', 'genga_end',
         'character_rig', 'rig_layer', 'motion_reference'}


def _inside(root, relative):
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError('empty path')
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts or re.match(r'^[A-Za-z]:', relative):
        raise ValueError('unsafe path')
    full = (root / p).resolve()
    if not full.is_relative_to(root.resolve()):
        raise ValueError('path escapes asset root')
    return full


def check(manifest, root):
    """Return an evidence report. A PASS is technical intake only, never artistic approval."""
    problems = []
    if manifest.get('schema') != SCHEMA:
        problems.append('unsupported schema')
    shot = manifest.get('shot_id')
    if not isinstance(shot, str) or not re.fullmatch(r'[A-Za-z0-9_-]{5,80}', shot):
        problems.append('invalid shot_id')
    fps, frames = manifest.get('fps'), manifest.get('frames')
    if not isinstance(fps, int) or not (1 <= fps <= 120) or isinstance(fps, bool):
        problems.append('invalid fps')
    if not isinstance(frames, int) or not (1 <= frames <= 14400) or isinstance(frames, bool):
        problems.append('invalid frames')
    assets = manifest.get('assets')
    if not isinstance(assets, list) or not assets:
        assets = []
        problems.append('assets list required')
    required_roles = manifest.get('required_roles', [])
    if not isinstance(required_roles, list) or any(x not in ROLES for x in required_roles):
        problems.append('invalid required_roles')
        required_roles = []
    ids = set()
    verified_roles = set()
    results = []
    for a in assets:
        if not isinstance(a, dict):
            problems.append('asset entry must be object')
            continue
        asset_id, role = a.get('id'), a.get('role')
        entry = {'id': asset_id, 'role': role, 'path': a.get('path'), 'state': 'blocked', 'issues': []}
        issues = entry['issues']
        if not isinstance(asset_id, str) or not re.fullmatch(r'[a-z][a-z0-9_-]{2,79}', asset_id):
            issues.append('invalid asset id')
        elif asset_id in ids:
            issues.append('duplicate asset id')
        ids.add(asset_id)
        if role not in ROLES:
            issues.append('invalid asset role')
        if a.get('approval') not in APPROVALS:
            issues.append('invalid approval state')
        try:
            path = _inside(root, a.get('path'))
        except (ValueError, OSError, TypeError) as exc:
            issues.append('unsafe path: ' + str(exc))
            path = None
        if path is not None and path.is_file():
            try:
                with path.open('rb') as source:
                    digest = hashlib.file_digest(source, 'sha256').hexdigest()
                entry['observed_sha256'] = digest
                entry['bytes'] = path.stat().st_size
                if not entry['bytes']:
                    issues.append('empty file')
                if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'}:
                    try:
                        from PIL import Image
                        with Image.open(path) as img:
                            img.verify()
                        with Image.open(path) as img:
                            entry['dimensions'] = [img.width, img.height]
                            entry['alpha'] = 'A' in img.getbands() or 'transparency' in img.info
                            expected_size = a.get('dimensions')
                            if expected_size is not None and entry['dimensions'] != expected_size:
                                issues.append('dimensions mismatch')
                            if a.get('needs_alpha') is True and not entry['alpha']:
                                issues.append('rig layer has no transparency')
                    except (ImportError, OSError, ValueError) as exc:
                        issues.append('image decoding unavailable or invalid: ' + type(exc).__name__)
                elif a.get('needs_alpha') is True:
                    issues.append('alpha required for non-image asset')
                expected = a.get('sha256')
                if expected is None:
                    issues.append('sha256 not locked against approved original')
                elif not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
                    issues.append('invalid sha256 lock')
                elif expected != digest:
                    issues.append('sha256 mismatch')
            except OSError as exc:
                issues.append('unreadable file: ' + type(exc).__name__)
        else:
            issues.append('source binary unavailable')
        if a.get('approval') != 'production_approved':
            issues.append('not bound to production approval')
        if not issues:
            entry['state'] = 'verified'
            verified_roles.add(role)
        else:
            problems.extend(f'{asset_id}: {i}' for i in issues)
        results.append(entry)
    for role in sorted(set(required_roles) - verified_roles):
        problems.append('no production-verified asset for required role ' + role)
    return {
        'schema': SCHEMA,
        'shot_id': shot,
        'fps': fps,
        'frames': frames,
        'duration_seconds': round(frames / fps, 5) if isinstance(fps, int) and fps > 0 and isinstance(frames, int) else None,
        'intake_gate': 'BLOCKED' if problems else 'PASS',
        'artistic_approval': 'NOT_EVALUATED',
        'animation_rendered': False,
        'assets': results,
        'blockers': sorted(set(problems)),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', required=True, type=Path)
    p.add_argument('--root', required=True, type=Path)
    p.add_argument('--report', type=Path)
    args = p.parse_args(argv)
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    report = check(manifest, args.root)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding='utf-8')
    print(rendered)
    return 2 if report['intake_gate'] != 'PASS' else 0


if __name__ == '__main__':
    raise SystemExit(main())
