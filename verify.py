#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import subprocess


ROOT = Path(__file__).resolve().parent


def verify_manifest():
    checked = 0
    for line in (ROOT / "MANIFEST.sha256").read_text().splitlines():
        digest, relative = line.split("  ", 1)
        path = ROOT / relative
        assert path.is_file(), relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, relative
        checked += 1
    return checked


def verify_claim(claim):
    process = subprocess.run(
        claim["command"],
        cwd=ROOT / claim["directory"],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(process.stdout)
    assert result["status"] == "PASS", claim["id"]
    return {
        "id": claim["id"],
        "evidence_class": claim["evidence_class"],
        "status": result["status"],
    }


def main():
    manifest_files = verify_manifest()
    catalog = json.loads((ROOT / "claims.json").read_text())
    assert catalog["schema"] == "reduced-sha256-claims-v1"
    claims = [verify_claim(claim) for claim in catalog["claims"]]
    print(
        json.dumps(
            {
                "status": "PASS",
                "manifest_files": manifest_files,
                "claims": claims,
                "scientific_solver_queries": 0,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
