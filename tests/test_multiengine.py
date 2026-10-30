"""Offline tests for Furuya multimotor orchestration and guarded adapters."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cloud"))
import engine_registry as registry
import wan22_animate_adapter as wan22
import wan_animate2_adapter as wan2


class RegistryTests(unittest.TestCase):
    def test_scene_replacement_is_not_viggle_remix(self):
        found = registry.candidates("scene_replacement")
        ids = {e["id"] for e in found}
        self.assertIn("wan22_replace", ids)
        self.assertIn("viggle_animate_open", ids)
        self.assertNotIn("viggle_video_remix", ids)
        self.assertNotIn("wan_animate2_motion", ids)
        self.assertTrue(all(not e["generation_ready"] for e in found))

    def test_motion_transfer_excludes_paid_kling(self):
        ids = {e["id"] for e in registry.candidates("motion_transfer")}
        self.assertIn("wan_animate2_motion", ids)
        self.assertIn("viggle_video_remix", ids)
        self.assertNotIn("kling3_motion", ids)
        self.assertFalse(registry.manifest(task="scene_replacement", clip_seconds=3)["auto_run"])

    def test_bad_duration_and_target_count(self):
        for seconds in (-1, 0, 31):
            with self.assertRaises(ValueError):
                registry.manifest(task="motion_transfer", clip_seconds=seconds)
        with self.assertRaises(ValueError):
            registry.manifest(task="scene_replacement", clip_seconds=3, target_count=0)


class AdapterTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.video = self.root / "dance.mp4"
        self.image = self.root / "Albedo.png"
        self.video.write_bytes(b"video fixture")
        self.image.write_bytes(b"image fixture")

    def test_wan22_needs_official_preprocess_not_mask_only(self):
        checkout = self.root / "Wan2.2"
        script = checkout / "wan/modules/animate/preprocess/preprocess_data.py"
        script.parent.mkdir(parents=True)
        script.touch()
        (checkout / "generate.py").touch()
        checkpoint = self.root / "weights"
        (checkpoint / "process_checkpoint").mkdir(parents=True)
        dest = self.root / "process"
        args = argparse.Namespace(
            checkout=checkout, checkpoint=checkpoint, video=self.video,
            image=self.image, preprocessed=dest,
            mode="replace", stage="preprocess",
            python="python", execute=False,
        )
        plan = wan22.plan(args)
        cmd = plan["command"]
        self.assertIn("--replace_flag", cmd)
        self.assertIn("--ckpt_path", cmd)
        self.assertIn("--iterations", cmd)
        self.assertEqual(plan["full_character_replacement"], True)
        args.stage = "render"
        dest.mkdir()
        for name in ("src_pose.mp4", "src_face.mp4", "src_bg.mp4", "src_mask.mp4"):
            (dest / name).write_bytes(b"video fixture")
        render = wan22.plan(args)
        self.assertIn("--use_relighting_lora", render["command"])

    def test_wan22_incomplete_crowd_mask_blocks_render(self):
        checkout = self.root / "Wan2.2"
        prep = checkout / "wan/modules/animate/preprocess/preprocess_data.py"
        prep.parent.mkdir(parents=True)
        prep.touch()
        (checkout / "generate.py").touch()
        ckpt = self.root / "weights"
        (ckpt / "process_checkpoint").mkdir(parents=True)
        work = self.root / "processed"
        work.mkdir()
        (work / "src_pose.mp4").write_bytes(b"fixture")
        args = argparse.Namespace(checkout=checkout, checkpoint=ckpt,
              video=self.video, image=self.image, preprocessed=work,
              mode="replace", stage="render", python="python", execute=False)
        with self.assertRaisesRegex(ValueError, "Incomplete official preprocessing"):
            wan22.plan(args)
        for name in ("src_face.mp4", "src_bg.mp4", "src_mask.mp4"):
            (work / name).write_bytes(b"fixture")
        (ckpt / "wan.safetensors").write_bytes(b"fake weights")
        args.crowd_scene = True
        args.verified_target_mask = False
        self.assertTrue(wan22.plan(args)["preprocessing_files_present"])
        with self.assertRaisesRegex(ValueError, "Crowd scene blocked"):
            wan22.execution_preflight(args)
        args.verified_target_mask = True
        wan22.execution_preflight(args)

    def test_wan_animate2_execute_blocks_missing_weights_and_gpus(self):
        root = self.root / "Wan-Animate-2"
        config_dir = root / "infer"
        config_dir.mkdir(parents=True)
        (config_dir / "wan_animate_2_distillation.yaml").write_text(
           "model_path: '../ckpts/model.safetensors'\nsp_size: 2\nsharding_size: 2\n"
        )
        checkpoints = root / "ckpts"
        checkpoints.mkdir()
        args = argparse.Namespace(checkout=root, distilled=True,
                                  require_model_dir=checkpoints)
        with self.assertRaisesRegex(ValueError, "does not exist"):
            wan2.execution_preflight(args)
        (checkpoints / "model.safetensors").write_bytes(b"x" * 2048)
        with mock.patch.object(wan2.subprocess, "run") as invoke:
            invoke.return_value.stdout = "NVIDIA GPU A\n"
            with self.assertRaisesRegex(ValueError, "requires at least 2"):
                wan2.execution_preflight(args)
            invoke.assert_called_once()
        with mock.patch.object(wan2.subprocess, "run") as invoke:
            invoke.return_value.stdout = "NVIDIA GPU A\nNVIDIA GPU B\n"
            wan2.execution_preflight(args)

    def test_wan_animate2_motion_only_distilled(self):
        root = self.root / "Wan-Animate-2"
        inf = root / "infer"
        inf.mkdir(parents=True)
        for path in ("wan_animate_2_demo.py", "wan_animate_2.yaml",
                     "wan_animate_2_distillation.yaml"):
            (inf / path).touch()
        args = argparse.Namespace(
            checkout=root, image=self.image, video=self.video,
            prompt="Adult Albedo, pale skin, white and gold dress, black wings.",
            distilled=True, require_model_dir=None, python="python", execute=False,
        )
        planned = wan2.plan(args)
        self.assertEqual(planned["engine"], "wan_animate2_motion")
        self.assertFalse(planned["preserves_original_background"])
        self.assertEqual(planned["command"][-4:], ["--sample_guide_scale", "1.0", "--step", "10"])
        self.assertEqual(planned["execution"], "DISABLED")

    def test_no_external_install_or_execution_in_tests(self):
        with mock.patch.object(wan22.subprocess, "run", side_effect=AssertionError("GPU run attempted")):
            with mock.patch.object(wan2.subprocess, "run", side_effect=AssertionError("GPU run attempted")):
                self.assertEqual(len(registry.ENGINES), 8)
                multi = registry.candidates("multi_scene_replacement")
                self.assertEqual(len(multi), 3)
                self.assertEqual({e["state"] for e in multi}, {"RESEARCH_ONLY", "OFFLINE_ADAPTER"})
                self.assertEqual(next(e["state"] for e in multi if e["id"] == "openjutsu_advanced"), "OFFLINE_ADAPTER")


if __name__ == "__main__":
    unittest.main()
