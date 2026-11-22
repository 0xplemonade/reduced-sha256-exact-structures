import unittest
from tests.support import run_result


class ConditionalModificationTest(unittest.TestCase):
    def test_normal_form_and_replay(self):
        result = run_result("conditional-modification")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["admissible_fixture_replays"], 6)
        self.assertEqual(result["arbitrary_context_identity_checks"], 2048)
        self.assertEqual(result["synthetic_input_origin_covariance_checks"], 256)
        self.assertEqual(result["row29_inverse_coordinate_checks"], 6)
        self.assertEqual(result["small_sigma0_inverse_two_sided_basis_checks"], 64)


if __name__ == "__main__":
    unittest.main()
