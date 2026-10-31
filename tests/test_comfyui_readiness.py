"""Offline readiness tests. No GPU, network or model downloads."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cloud"))
from comfyui_readiness import analyze, MODEL_FIELDS, GIB
from comfyui_local_bridge import workflow_api


def complete_report():
    graph = workflow_api(ROOT / "workflows/openjutsu_advanced.api.json")
    info = {node["class_type"]: {} for node in graph.values()}
    for cls, fields in MODEL_FIELDS.items():
        if cls not in info:
            continue
        values = {}
        for field in fields:
            filenames = sorted({node["inputs"][field] for node in graph.values()
                                if node["class_type"] == cls and field in node["inputs"]
                                and isinstance(node["inputs"][field], str)})
            values[field] = [filenames]
        info[cls] = {"input": {"required": values}}
    stats = {"system": {"ram_total": 96*GIB},
             "devices": [{"type": "cuda", "name": "Synthetic NVIDIA RTX 4090 (TEST ONLY)",
                          "vram_total": 24*GIB}]}
    return graph, info, stats


class ReadinessTests(unittest.TestCase):
    def test_complete_synthetic_environment_only_passes_preflight(self):
        graph, nodes, stats = complete_report()
        report = analyze(graph, nodes, stats)
        self.assertTrue(report["can_attempt_render"])
        self.assertEqual(report["status"], "PREFLIGHT_PASSED_NOT_RENDERED")
        self.assertFalse(report["free_gpu_verified"])
        self.assertFalse(report["model_integrity_verified"])
        self.assertFalse(report["output_created"])
        self.assertEqual(len(report["missing_models"]), 0)
        self.assertGreaterEqual(len(report["model_checks"]), 7)

    def test_missing_exact_model_is_reported(self):
        graph, nodes, stats = complete_report()
        nodes["UNETLoader"]["input"]["required"]["unet_name"] = [["another_diffusion_model.safetensors"]]
        report = analyze(graph, nodes, stats)
        self.assertFalse(report["can_attempt_render"])
        self.assertEqual(report["status"], "NO_GO_MISSING_COMPONENTS")
        self.assertEqual(report["missing_models"][0]["folder"], "diffusion_models")
        self.assertEqual(report["missing_models"][0]["filename"],
                         "minimax_h3_ref2va_pruned_int8_convrot.safetensors")

    def test_missing_custom_node_is_reported(self):
        graph, nodes, stats = complete_report()
        nodes.pop("H3AdvancedSwapPlan")
        report = analyze(graph, nodes, stats)
        self.assertFalse(report["can_attempt_render"])
        self.assertIn("H3AdvancedSwapPlan", report["missing_node_classes"])

    def test_unknown_model_options_is_not_silently_approved(self):
        graph, nodes, stats = complete_report()
        nodes["UNETLoader"] = {}
        report = analyze(graph, nodes, stats)
        self.assertEqual(report["status"], "UNVERIFIED_MODEL_CHOICES")
        self.assertTrue(report["unchecked_models"])
        self.assertFalse(report["can_attempt_render"])

    def test_8gb_gpu_and_29gb_ram_below_tested_baseline(self):
        graph, nodes, stats = complete_report()
        stats["devices"][0]["vram_total"] = 8*GIB
        stats["system"]["ram_total"] = 29*GIB
        report = analyze(graph, nodes, stats)
        self.assertEqual(report["status"], "BELOW_OPENJUTSU_TESTED_BASELINE")
        self.assertFalse(report["can_attempt_render"])
        self.assertEqual(report["hardware"]["ram_total_gib"], 29)
        self.assertEqual(report["hardware"]["devices"][0]["vram_gib"], 8)

    def test_no_stats_or_non_nvidia_gpu_fail_closed(self):
        graph, nodes, stats = complete_report()
        self.assertFalse(analyze(graph, nodes, {})["can_attempt_render"])
        stats["devices"][0]["type"] = "cpu"
        self.assertFalse(analyze(graph, nodes, stats)["can_attempt_render"])

    def test_does_not_mutate_graph(self):
        graph, nodes, stats = complete_report()
        original = graph["24"]["inputs"]["unet_name"]
        analyze(graph, nodes, stats)
        self.assertEqual(graph["24"]["inputs"]["unet_name"], original)


if __name__ == "__main__":
    unittest.main()
