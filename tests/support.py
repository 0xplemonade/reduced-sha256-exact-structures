from pathlib import Path
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run_result(name, *args):
    directory = ROOT / "results" / name
    process = subprocess.run(
        [sys.executable, "verify.py", *args],
        cwd=directory,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(process.stdout)
