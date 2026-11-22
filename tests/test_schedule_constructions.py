import json
import subprocess
import sys
import unittest
from tests.support import ROOT, run_result


class ScheduleConstructionsTest(unittest.TestCase):
    def test_saved_result_replays_exactly(self):
        result = run_result("schedule-constructions")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["admissible_pair_replays"], 384)
        self.assertEqual(result["unrestricted_Z_W13_inverse_checks"], 144)
        self.assertEqual(result["fibre_counts"]["p4_W14"], 1 << 27)
        self.assertEqual(result["fibre_counts"]["p4_W23"], 1 << 27)
        self.assertEqual(result["fibre_counts"]["p1_W14"], 138_936_320)
        self.assertEqual(result["fibre_counts"]["p1_W23"], 138_936_320)
        self.assertEqual(result["S14_fibre_counting"]["p4_average_including_empty"], 1 << 22)
        self.assertEqual(result["S14_fibre_counting"]["p1_average_including_empty"], 4_494_400)

    def test_generator_reconstructs_pair_from_coordinates(self):
        directory = ROOT / "results" / "schedule-constructions"
        process = subprocess.run(
            [sys.executable, "generate.py", "--example", "0"],
            cwd=directory,
            check=True,
            capture_output=True,
            text=True,
        )
        generated = json.loads(process.stdout)
        self.assertEqual(generated["status"], "PASS")
        self.assertEqual(
            generated["pair_sha256_be"],
            "b16fec39f5e4ae2041b91cd8f2a358417163b0ed098f1d2c30212ffba642d80f",
        )
        self.assertEqual(generated["support"], [6, 7, 9, 14, 22, 23, 37])
        self.assertEqual(len(generated["left_W0_W15"]), 16)
        self.assertEqual(len(generated["right_W0_W15"]), 16)


if __name__ == "__main__":
    unittest.main()
