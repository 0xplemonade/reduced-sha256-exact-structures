from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ClaimCatalogTest(unittest.TestCase):
    def test_catalog_has_one_entry_per_result_directory(self):
        catalog = json.loads((ROOT / "claims.json").read_text())
        self.assertEqual(catalog["schema"], "reduced-sha256-claims-v1")
        ids = [claim["id"] for claim in catalog["claims"]]
        self.assertEqual(
            ids,
            [
                "schedule-constructions",
                "conditional-modification",
                "common-w39-obstruction",
                "derivative-fibres",
                "carry-characteristics",
            ],
        )
        for claim in catalog["claims"]:
            self.assertIn(
                claim["evidence_class"],
                {"proved", "exhaustively-counted", "constructive-witnesses"},
            )
            self.assertTrue((ROOT / claim["directory"] / "README.md").is_file())
            self.assertEqual(claim["command"], ["python3", "verify.py"])


if __name__ == "__main__":
    unittest.main()
