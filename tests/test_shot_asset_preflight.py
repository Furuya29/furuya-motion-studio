"""Regression checks for non-destructive original-asset intake."""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.animation_pilot.shot_asset_preflight import check, SCHEMA


def sample(path, alpha=True):
    Image.new('RGBA' if alpha else 'RGB', (8, 12), (10, 20, 30, 0) if alpha else (10, 20, 30)).save(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(sha=None, approval='production_approved', path='body.png', needs_alpha=True):
    return {'schema': SCHEMA, 'shot_id': 'AEN_TEST_001', 'fps': 24, 'frames': 72,
            'required_roles': ['rig_layer'], 'assets': [
                {'id': 'torso_a', 'role': 'rig_layer', 'path': path, 'approval': approval,
                 'sha256': sha, 'dimensions': [8, 12], 'needs_alpha': needs_alpha}]}


class TestPreflight(unittest.TestCase):
    def test_verified_layer_passes_without_promotion(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            digest = sample(root / 'body.png')
            report = check(manifest(digest), root)
            self.assertEqual(report['intake_gate'], 'PASS')
            self.assertFalse(report['animation_rendered'])
            self.assertEqual(report['artistic_approval'], 'NOT_EVALUATED')

    def test_chat_approved_requires_hash_and_production_binding(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sample(root / 'body.png')
            report = check(manifest(None, 'chat_approved_unbound'), root)
            self.assertEqual(report['intake_gate'], 'BLOCKED')
            self.assertTrue(any('sha256 not locked' in x for x in report['blockers']))
            self.assertTrue(any('production approval' in x for x in report['blockers']))

    def test_source_mismatch_and_transparency(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sample(root / 'body.png', alpha=False)
            report = check(manifest('0' * 64), root)
            self.assertTrue(any('sha256 mismatch' in x for x in report['blockers']))
            self.assertTrue(any('no transparency' in x for x in report['blockers']))

    def test_path_traversal_is_denied(self):
        with tempfile.TemporaryDirectory() as folder:
            r = check(manifest('0' * 64, path='../secret.png'), Path(folder))
            self.assertTrue(any('unsafe path' in x for x in r['blockers']))

    def test_missing_asset_never_reports_render_success(self):
        with tempfile.TemporaryDirectory() as folder:
            r = check(manifest('0' * 64), Path(folder))
            self.assertEqual(r['intake_gate'], 'BLOCKED')
            self.assertFalse(r['animation_rendered'])

    def test_missing_required_role(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            digest = sample(root / 'body.png')
            m = manifest(digest)
            m['required_roles'].append('genga_end')
            r = check(m, root)
            self.assertTrue(any('genga_end' in x for x in r['blockers']))


if __name__ == '__main__':
    unittest.main()
