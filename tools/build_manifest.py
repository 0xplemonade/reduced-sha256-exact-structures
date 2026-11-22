#!/usr/bin/env python3
from pathlib import Path
import hashlib


ROOT = Path(__file__).resolve().parents[1]


def included(path):
    return (
        path.is_file()
        and ".git" not in path.parts
        and path.name != "MANIFEST.sha256"
        and "__pycache__" not in path.parts
    )


paths = sorted(path for path in ROOT.rglob("*") if included(path))
lines = []
for path in paths:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
(ROOT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
