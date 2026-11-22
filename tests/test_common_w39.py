import unittest
from tests.support import run_result


class CommonW39Test(unittest.TestCase):
    def test_both_numerical_cores_have_empty_intersection(self):
        result = run_result("common-w39-obstruction")
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["primary_common_W39_feasible"])
        self.assertEqual(result["primary_W22_passing_both"], 0)
        self.assertFalse(result["analogous_r37_common_W39_feasible"])
        self.assertEqual(result["analogous_r37_W22_passing_both"], 0)
        self.assertFalse(result["full_scans_replayed"])


if __name__ == "__main__":
    unittest.main()
