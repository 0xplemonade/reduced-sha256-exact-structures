import unittest
from tests.support import run_result


class DerivativeFibresTest(unittest.TestCase):
    def test_all_six_affine_components_replay(self):
        result = run_result("derivative-fibres")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["components"], 6)
        self.assertEqual(result["solutions_checked"], 1_259_520)
        self.assertTrue(result["affine_spans_disjoint"])


if __name__ == "__main__":
    unittest.main()
