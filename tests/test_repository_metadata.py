from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryMetadataTest(unittest.TestCase):
    def test_dual_license_and_citation_files_exist(self):
        self.assertIn("Apache License", (ROOT / "LICENSE").read_text())
        self.assertIn("Attribution 4.0 International", (ROOT / "LICENSE-DOCS").read_text())
        citation = (ROOT / "CITATION.cff").read_text()
        self.assertIn("title: Reduced SHA-256 exact structures", citation)
        self.assertIn("version: 0.1.0", citation)
        self.assertIn("Apache-2.0 AND CC-BY-4.0", citation)

    def test_third_party_policy_blocks_unlicensed_files(self):
        text = (ROOT / "THIRD_PARTY.md").read_text()
        self.assertIn("Do not publish a copied file unless its reuse terms are known", text)


if __name__ == "__main__":
    unittest.main()
