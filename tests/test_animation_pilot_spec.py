"""Regressões do contrato inicial de tomada (sem motor de render)."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.animation_pilot.validate_shot_spec import validate  # noqa: E402

SPEC_PATH = ROOT / "docs/projeto-animacao-automatizada/piloto_15s_shot_spec_v0_1.json"


class TestShotSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))

    def test_spec_inicial_valido(self):
        self.assertEqual(validate(self.spec), [])
        self.assertEqual(self.spec["timeline"]["total_frames"], 15 * 24)

    def test_overlap_is_rejected(self):
        bad = copy.deepcopy(self.spec)
        bad["shots"][1]["start_frame"] = 119
        self.assertTrue(any("lacuna/sobreposição" in e for e in validate(bad)))

    def test_missing_prop_is_rejected(self):
        bad = copy.deepcopy(self.spec)
        bad["shots"][2]["constraints"][0]["prop_id"] = "prop.inexistente"
        self.assertTrue(any("prop não registrado" in e for e in validate(bad)))

    def test_unsubstantiated_approval_is_rejected(self):
        bad = copy.deepcopy(self.spec)
        bad["evidence"]["pilot_homologated"] = True
        self.assertTrue(any("sem evidências mínimas" in e for e in validate(bad)))

    def test_camera_keyframe_outside_shot_is_rejected(self):
        bad = copy.deepcopy(self.spec)
        bad["shots"][2]["camera"]["keyframes"][1]["frame"] = 360
        self.assertTrue(any("keyframes devem cobrir" in e for e in validate(bad)))


if __name__ == "__main__":
    unittest.main()
