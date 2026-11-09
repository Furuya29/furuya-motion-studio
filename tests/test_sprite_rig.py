"""Sprite-rig FK, asset switch and deterministic tests; no anime QA."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
try:
    from tools.animation_pilot import sprite_rig, make_sprite_demo
except ImportError:
    sprite_rig = None
    make_sprite_demo = None

@unittest.skipIf(sprite_rig is None, 'Pillow is not installed in core recast CI')
class TestSpriteRig(unittest.TestCase):
    def test_affine_inversion(self):
        a=sprite_rig.matmul(sprite_rig.translate(30,19),sprite_rig.rotate(45))
        x=sprite_rig.matmul(a,sprite_rig.invert(a))
        for got,want in zip(x,(1,0,0,0,1,0)):
            self.assertAlmostEqual(got,want,places=6)

    def test_interpolation_and_step(self):
        keys=[{'frame':0,'value':0},{'frame':10,'value':20}]
        self.assertEqual(sprite_rig.sample(keys,5),10)
        self.assertEqual(sprite_rig.sample(keys,5,step=True),0)

    def test_asset_protection_and_cycle(self):
        rig={'version':'sprite-rig/0.1','canvas':[640,360],'fps':24,'frames':4,'parts':[
            {'id':'A','sprite':'../outside.png','parent':'B','pivot':[0,0],'offset':[1,1]},
            {'id':'B','sprite':'valid.png','parent':'A','pivot':[0,0],'offset':[1,1]}]}
        issues=sprite_rig.validate(rig)
        self.assertTrue(any('unsafe' in error for error in issues))
        self.assertTrue(any('cycle' in error for error in issues))

    def test_frames_deterministic_and_swap(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            make_sprite_demo.make(root)
            rig=json.loads((root/'rig.json').read_text())
            self.assertEqual(sprite_rig.validate(rig),[])
            frame25=sprite_rig.render_frame(rig,root,25).tobytes()
            self.assertEqual(frame25,sprite_rig.render_frame(rig,root,25).tobytes())
            self.assertNotEqual(frame25,sprite_rig.render_frame(rig,root,31).tobytes())

if __name__=='__main__':
    unittest.main()
