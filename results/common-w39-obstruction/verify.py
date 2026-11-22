#!/usr/bin/env python3
"""Independent verifier for the common-W39 schedule exclusion.

Default mode re-expands both explicit schedule pairs, checks every stated
dependency, and checks the saved exhaustive counts.

Use --full-scan to rebuild scan_family.c in a temporary directory and rerun
both exact 2^32-domain image/count scans (about 45 seconds wall here).
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

MASK = (1 << 32) - 1
ROOT = Path(__file__).resolve().parent

def rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK


def s0(x: int) -> int:
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def s1(x: int) -> int:
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def derivative(f, x: int, d: int) -> int:
    return (f((x + d) & MASK) - f(x)) & MASK


def expand(words: list[int], count: int = 40) -> list[int]:
    out = list(words)
    for t in range(16, count):
        out.append((s1(out[t - 2]) + out[t - 7] + s0(out[t - 15]) + out[t - 16]) & MASK)
    return out


def parse(words: list[str]) -> list[int]:
    return [int(x, 16) for x in words]


def differences(left: list[int], right: list[int]) -> list[int]:
    return [(b - a) & MASK for a, b in zip(left, right)]


def gf2_rank(f) -> int:
    basis: dict[int, int] = {}
    for bit in range(32):
        value = f(1 << bit)
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def verify_pair(left0: list[int], right0: list[int], expected_support: list[int]) -> tuple[list[int], list[int], list[int]]:
    left, right = expand(left0), expand(right0)
    delta = differences(left, right)
    assert [i for i, value in enumerate(delta[:39]) if value] == expected_support
    expected = {
        6: 0x31DE0240, 7: 0xFFFFFFFC, 9: 0x00028000,
        14: 4, 22: 0x07FF0000, 23: 0xFFFFFFFC,
    }
    assert all(delta[i] == value for i, value in expected.items())
    assert delta[37] == derivative(s0, left[22], expected[22])
    assert delta[38] == 0
    assert delta[39] == (derivative(s1, left[37], delta[37]) + delta[23]) & MASK
    return left, right, delta


def run_full_scan(expected_r38: dict, expected_r37: dict) -> None:
    with tempfile.TemporaryDirectory(prefix="r40-w39-scan-") as tmp:
        binary = Path(tmp) / "scan_family"
        subprocess.run(
            ["gcc", "-O3", "-march=native", "-fopenmp", str(ROOT / "scan_family.c"), "-o", str(binary)],
            check=True,
        )
        env = dict(os.environ)
        env["OMP_NUM_THREADS"] = "4"
        for arm, expected in (("r38", expected_r38), ("r37", expected_r37)):
            replay = subprocess.run([str(binary), arm], check=True, capture_output=True, text=True, env=env)
            assert json.loads(replay.stdout) == expected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-scan", action="store_true")
    args = parser.parse_args()

    result = json.loads((ROOT / "RESULT.json").read_text())
    scan_r38 = json.loads((ROOT / "SCAN_R38.json").read_text())
    scan_r37 = json.loads((ROOT / "SCAN_R37.json").read_text())
    primary = result["primary"]
    supplied = primary["supplied_witness"]

    left_stored, right_stored = parse(supplied["left_W0_W39"]), parse(supplied["right_W0_W39"])
    left, right, delta = verify_pair(left_stored[:16], right_stored[:16], primary["support_through_W38"])
    assert left == left_stored and right == right_stored
    assert left[22] == int(supplied["W22_left"], 16)
    assert derivative(s1, left[22], delta[22]) == int(supplied["row24_D_s1"], 16)
    assert derivative(s0, left[9], delta[9]) == int(supplied["row24_D_s0"], 16)
    assert (derivative(s1, left[22], delta[22]) + derivative(s0, left[9], delta[9])) & MASK == 0
    assert derivative(s0, left[23], delta[23]) + delta[22] & MASK == 0
    assert delta[37] == int(supplied["dW37"], 16)
    assert derivative(s1, left[37], delta[37]) == int(supplied["D_s1_W37"], 16)
    assert left[38] == right[38] == int(supplied["common_W38"], 16)
    assert delta[39] == int(supplied["dW39"], 16) != 0

    family = primary["fixed_active_core_family"]
    left2, right2, delta2 = verify_pair(
        parse(family["second_pair_left_W0_W15"]),
        parse(family["second_pair_right_W0_W15"]),
        primary["support_through_W38"],
    )
    for i in (6, 7, 9, 14, 22, 23):
        assert left2[i] == left[i]
    assert left2[37] == int(family["second_pair_W37_left"], 16) != left[37]
    assert delta2[37] == int(family["second_pair_dW37"], 16)
    assert left2[38] == right2[38] == int(family["second_pair_common_W38"], 16)
    assert delta2[39] == int(family["second_pair_dW39"], 16) != 0
    assert gf2_rank(s0) == gf2_rank(s1) == 32

    expected_r38 = {
        "arm": "shifted-public-r38", "dW9": "00028000", "dW22": "07ff0000",
        "dW8": "00000000", "terminal_D_s1_target": "00000004",
        **primary["exact_exhaustive_count"], "inverse_sample_failures": 0,
    }
    analogous = result["analogous_public_r37"]
    expected_r37 = {
        "arm": "public-r37", "dW9": "0000a000", "dW22": "fdffc000",
        "dW8": "d0007c70", "terminal_D_s1_target": "00000001",
        **analogous["exact_exhaustive_count"], "inverse_sample_failures": 0,
    }
    assert scan_r38 == expected_r38
    assert scan_r37 == expected_r37
    assert scan_r38["W22_passing_both"] == scan_r37["W22_passing_both"] == 0

    if args.full_scan:
        run_full_scan(scan_r38, scan_r37)

    print(json.dumps({
        "status": "PASS",
        "primary_common_W39_feasible": False,
        "primary_W22_passing_both": scan_r38["W22_passing_both"],
        "analogous_r37_common_W39_feasible": False,
        "analogous_r37_W22_passing_both": scan_r37["W22_passing_both"],
        "full_scans_replayed": args.full_scan,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
