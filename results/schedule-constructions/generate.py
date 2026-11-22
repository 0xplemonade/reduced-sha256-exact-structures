#!/usr/bin/env python3
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import struct


ROOT = Path(__file__).resolve().parent
MASK = (1 << 32) - 1


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


chart = load("construction_chart", "chart.py")
reference = load("construction_reference", "reference.py")
coordinates = load("construction_coordinates", "state_coordinates.py")


def parse(values):
    return [int(value, 16) for value in values]


def pack(values):
    return struct.pack(">16I", *values)


def hexdump(values):
    return [f"{value:08x}" for value in values]


def construct(example):
    differences = {
        "p4": chart.DIFF_SHIFTED_R38,
        "p1": chart.DIFF_R37,
    }[example["arm"]]
    entry = parse(example["entry_words"])
    prefix = parse(example["prefix_W0_W9"])
    outputs = parse(example["left_A10_A12"])
    result = coordinates.generate_from_left_A(
        entry,
        prefix,
        int(example["W22"], 16),
        int(example["V_W14"], 16),
        int(example["Z_W23"], 16),
        outputs,
        differences,
    )
    left = result["left"]
    right = result["right"]
    left_expanded = reference.expand(pack(left))
    right_expanded = reference.expand(pack(right))
    delta = [(b - a) & MASK for a, b in zip(left_expanded, right_expanded)]
    support = [index for index, value in enumerate(delta[:39]) if value]
    digest = hashlib.sha256(pack(left) + pack(right)).hexdigest()
    assert support == example["expected_support"]
    assert digest == example["expected_pair_sha256_be"]
    return {
        "status": "PASS",
        "arm": example["arm"],
        "left_W0_W15": hexdump(left),
        "right_W0_W15": hexdump(right),
        "support": support,
        "pair_sha256_be": digest,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", type=int, default=0)
    args = parser.parse_args()
    examples = json.loads((ROOT / "EXAMPLE.json").read_text())["examples"]
    if args.example < 0 or args.example >= len(examples):
        parser.error(f"example index must be between 0 and {len(examples) - 1}")
    print(json.dumps(construct(examples[args.example]), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
