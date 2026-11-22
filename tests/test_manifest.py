from pathlib import Path
import hashlib
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ManifestTest(unittest.TestCase):
    def test_manifest_matches_every_tracked_release_file(self):
        lines = (ROOT / "MANIFEST.sha256").read_text().splitlines()
        entries = {}
        for line in lines:
            digest, path = line.split("  ", 1)
            self.assertNotIn(path, entries)
            entries[path] = digest
        expected = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
            and ".git" not in path.parts
            and path.name != "MANIFEST.sha256"
            and "__pycache__" not in path.parts
        }
        self.assertEqual(set(entries), expected)
        for path, digest in entries.items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
