import unittest
from tests.support import run_result


class CarryCharacteristicsTest(unittest.TestCase):
    def test_six_witnesses_and_local_theorem_replay(self):
        result = run_result("carry-characteristics")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["witnesses_replayed"], 6)
        self.assertEqual(result["local_theorem_cases"], 3136)
        self.assertTrue(result["transfer_and_reset_verified"])


if __name__ == "__main__":
    unittest.main()
