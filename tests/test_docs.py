from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DocumentationTest(unittest.TestCase):
    def test_required_sections_and_claim_links(self):
        readme = (ROOT / "README.md").read_text()
        for heading in (
            "# Reduced SHA-256 exact structures",
            "## What this repository contains",
            "## What this repository does not claim",
            "## Generate a valid paired schedule",
            "## Results",
            "## Verify the release",
            "## Reuse and citation",
            "## Open questions",
        ):
            self.assertIn(heading, readme)
        for slug in (
            "schedule-constructions",
            "conditional-modification",
            "common-w39-obstruction",
            "derivative-fibres",
            "carry-characteristics",
        ):
            self.assertIn(f"results/{slug}/README.md", readme)

    def test_relative_markdown_links_resolve(self):
        for document in ROOT.rglob("*.md"):
            if "superpowers" in document.parts:
                continue
            text = document.read_text()
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                path = target.split("#", 1)[0]
                self.assertTrue((document.parent / path).resolve().exists(), (document, target))

    def test_no_private_workspace_paths(self):
        forbidden = "/root/" + ".t3/"
        paths = list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.py")) + list(ROOT.rglob("*.json"))
        for path in paths:
            if "superpowers" in path.parts:
                continue
            self.assertNotIn(forbidden, path.read_text(errors="ignore"), path)


if __name__ == "__main__":
    unittest.main()
