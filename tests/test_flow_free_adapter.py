"""Google Flow no-payment preparation: tests include real short FFmpeg file exports."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cloud"))
import flow_free_adapter as flow


class FlowPlanTests(unittest.TestCase):
    def test_24s_source_is_split_into_free_compatible_segments(self):
        self.assertEqual(flow.partition(24.255), [(0.,8.),(8.,8.),(16.,8.255)])
        self.assertEqual(flow.estimate_credits([3,8,8,8.255]), 28)
        self.assertEqual(flow.estimate_credits([3,8,8,8.255],720), 84)

    def test_credits_are_not_silent_payments(self):
        with self.assertRaisesRegex(ValueError, "1–10"):
            flow.partition(24, seconds=15)
        self.assertEqual(flow.partition(10.25, seconds=8), [(0.,8.),(8.,2.25)])

    def test_5_references_preserved_and_background_locked(self):
        names=flow.REFERENCE_NAMES
        prompt=flow.make_prompt(list(names), list(flow.SOURCE_DESCRIPTIONS),
                                list(flow.CHARACTER_DESCRIPTIONS))
        for name in names:
            self.assertIn(name, prompt)
        self.assertIn("Keep original camera motion", prompt)
        self.assertIn("Unselected crowd members MUST NOT change", prompt)
        self.assertIn("ALBEDO", prompt.upper())


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                     "FFmpeg/FFprobe required for real video fixture")
class FlowVideoPreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.source=self.root/"source.mp4"
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
                        "-f","lavfi","-i","color=c=black:s=180x320:r=12",
                        "-t","3.1","-c:v","libx264","-pix_fmt","yuv420p",
                        str(self.source)],check=True,timeout=40)
        self.images=[]
        for i in range(5):
            image=self.root/("ref"+str(i)+".png")
            image.write_bytes(b"\x89PNG\r\n\x1a\n"+bytes([i])*128)
            self.images.append(image)

    def test_real_ffmpeg_media_and_manifest(self):
        output=self.root/"prepared"
        result=flow.prepare(self.source,self.images,output,
                            free_balance=50,segment_seconds=2.0,pilot_seconds=1.0)
        self.assertEqual(result["target_count"],5)
        self.assertFalse(result["rendered_by_flow"])
        self.assertFalse(result["uploaded_to_flow"])
        self.assertFalse(result["free_credits_verified"])
        self.assertTrue((output/"clips/pilot.mp4").is_file())
        self.assertGreater((output/"clips/clip_01.mp4").stat().st_size,1000)
        self.assertTrue((output/"clips/clip_02.mp4").is_file())
        self.assertEqual(len(list((output/"references").iterdir())),5)
        self.assertEqual(len(json.loads((output/"flow_job.json").read_text())["reference_paths"]),5)
        self.assertIn("Shalltear", (output/"flow_prompt.txt").read_text())
        with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
            flow.prepare(self.source,self.images,output)

    def test_pilot_budget_enforced_before_any_file_creation(self):
        output=self.root/"blocked"
        with self.assertRaisesRegex(ValueError, "Pilot alone costs"):
            flow.prepare(self.source,self.images,output,resolution=720,
                         free_balance=1,pilot_seconds=2)
        self.assertFalse(output.exists())

    def test_dry_run_does_not_write_or_submit(self):
        output=self.root/"plan"
        with mock.patch.object(flow, "shutil") as spy:
            report=flow.prepare(self.source,self.images,output,dry_run=True)
        spy.copyfile.assert_not_called()
        self.assertEqual(report["execution_status"],"PREPARED_OFFLINE")
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
