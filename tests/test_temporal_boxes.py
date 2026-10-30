"""No-GPU regression tests for temporal bbox masks (NOT SAM segmentation)."""
from __future__ import annotations
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import export_temporal_boxes as masks


def example():
    return {
        "schema": "furuya-multicast-plan/1",
        "task": "multi_scene_replacement",
        "source_immutable": True,
        "tracking_state": "NOT_RUN",
        "render_state": "NOT_STARTED",
        "video": {"filename": "rio.mp4", "duration_seconds": 1.0,
                  "width": 32, "height": 32},
        "targets": [
            {"id": "albedo", "name": "Albedo", "reference_filename": "albedo.png",
             "anchors": [
                 {"time_seconds": 0.0, "box_xywh": [0.1, 0.1, 0.25, 0.5]},
                 {"time_seconds": 0.75, "box_xywh": [0.25, 0.1, 0.25, 0.5]},
             ]},
            {"id": "diana", "name": "Diana", "reference_filename": "diana.png",
             "anchors": [{"time_seconds": 0.5,
                          "box_xywh": [0.6, 0.1, 0.2, 0.6]}]},
        ],
    }


def decode_png(path):
    raw = path.read_bytes()
    assert raw.startswith(masks.PNG_HEADER)
    ptr = 8
    data = b""
    width, height = 0, 0
    while ptr < len(raw):
        n = struct.unpack(">I", raw[ptr:ptr+4])[0]
        kind = raw[ptr+4:ptr+8]
        blob = raw[ptr+8:ptr+8+n]
        if kind == b"IHDR":
            width, height = struct.unpack(">II", blob[:8])
        if kind == b"IDAT":
            data += blob
        ptr += 12+n
    decoded = zlib.decompress(data)
    rows = [decoded[i*(width+1)+1:(i+1)*(width+1)]
            for i in range(height)]
    return width, height, rows


class TemporalBoxExportTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def test_interpolates_boxes_only_inside_anchors(self):
        dst = self.dir / "proposals"
        result = masks.export(example(), dst, fps=4)
        self.assertEqual(result["frame_count"], 4)
        self.assertFalse(result["identity_tracking_validated"])
        self.assertFalse(result["generative_video_created"])
        self.assertEqual(result["targets"][0]["proposed_frames"], 4)
        self.assertEqual(result["targets"][1]["proposed_frames"], 1)
        first = decode_png(dst / "albedo" / "frame_00000.png")
        middle = decode_png(dst / "albedo" / "frame_00002.png")
        self.assertEqual(first[:2], (32, 32))
        self.assertTrue(any(255 in row for row in first[2]))
        self.assertTrue(any(255 in row for row in middle[2]))
        diana = decode_png(dst / "diana" / "frame_00000.png")
        self.assertFalse(any(255 in row for row in diana[2]))
        diana_mid = decode_png(dst / "diana" / "frame_00002.png")
        self.assertTrue(any(255 in row for row in diana_mid[2]))
        self.assertTrue((dst / "proposals-index.json").is_file())

    def test_no_tracking_extrapolated_outside_anchors(self):
        anchors = [{"time_seconds": 0.25, "box_xywh": [0.1, 0.1, 0.25, 0.5]},
                   {"time_seconds": 0.5, "box_xywh": [0.3, 0.1, 0.25, 0.5]}]
        self.assertIsNone(masks.bbox_at(anchors, 0.0, 4))
        self.assertIsNone(masks.bbox_at(anchors, 0.75, 4))
        self.assertIsNotNone(masks.bbox_at(anchors, 0.375, 4))

    def test_never_overwrites_and_limits_resolution(self):
        plan = example()
        dst = self.dir / "proposals"
        masks.export(plan, dst, fps=2)
        with self.assertRaisesRegex(ValueError, "already exists"):
            masks.export(plan, dst, fps=2)
        with self.assertRaisesRegex(ValueError, "Frame count exceeds"):
            masks.export(plan, self.dir / "too_many", fps=60, max_frames=2)

    def test_invalid_tracking_plan_cannot_export(self):
        plan = example()
        plan["tracking_state"] = "VERIFIED"
        with self.assertRaisesRegex(ValueError, "honest tracking"):
            masks.export(plan, self.dir / "bad", fps=4)


if __name__ == "__main__":
    unittest.main()
