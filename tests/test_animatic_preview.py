"""Unit tests for geometric motion-blocking; not artistic QA."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
try:
    from tools.animation_pilot import preview_animatic as renderer
except ImportError:
    renderer=None

SPEC=ROOT/'docs/projeto-animacao-automatizada/piloto_15s_shot_spec_v0_1.json'

@unittest.skipIf(renderer is None,'Pillow not available')
class TestAnimaticPreview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec=json.loads(SPEC.read_text(encoding='utf-8'))

    def test_contiguous_shots(self):
        shots=self.spec['shots']
        self.assertEqual([(s['start_frame'],s['end_frame']) for s in shots],[(0,120),(120,240),(240,360)])
        self.assertEqual(self.spec['timeline']['total_frames'],360)

    def test_camera_projection_changes_with_orbit(self):
        shot=self.spec['shots'][2]
        start=renderer.camera_at(shot,240,640,360)
        end=renderer.camera_at(shot,359,640,360)
        point=(.54,-.40,1.5)
        self.assertGreater(abs(start.project(point)[0]-end.project(point)[0]),5)

    def test_deterministic_frame_rendering(self):
        a=renderer.render_frame(self.spec,250,640,360)
        b=renderer.render_frame(self.spec,250,640,360)
        self.assertEqual(a.tobytes(),b.tobytes())

    def test_distinct_shot_visuals(self):
        frames=[renderer.render_frame(self.spec,frame,640,360) for frame in (40,160,300)]
        self.assertNotEqual(frames[0].tobytes(),frames[1].tobytes())
        self.assertNotEqual(frames[1].tobytes(),frames[2].tobytes())

if __name__=='__main__':
    unittest.main()
