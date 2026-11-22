#!/usr/bin/env python3
import json
from pathlib import Path


MASK = (1 << 32) - 1
ROOT = Path(__file__).resolve().parent


def rotate_right(value, count):
    return ((value >> count) | (value << (32 - count))) & MASK


def small_sigma0(value):
    return rotate_right(value, 7) ^ rotate_right(value, 18) ^ (value >> 3)


def derivative(value, delta):
    return (small_sigma0((value + delta) & MASK) - small_sigma0(value)) & MASK


def span(component, delta, target):
    representative = int(component["representative"], 16)
    basis = [int(value, 16) for value in component["basis"]]
    expected_mask = int(component["xor_mask"], 16)
    assert len(basis) == component["rank"]
    value = representative
    previous_gray = 0
    count = 0
    for index in range(1 << len(basis)):
        gray = index ^ (index >> 1)
        if index:
            changed = gray ^ previous_gray
            value ^= basis[changed.bit_length() - 1]
        previous_gray = gray
        assert value ^ ((value + delta) & MASK) == expected_mask
        assert derivative(value, delta) == target
        count += 1
    assert count == component["count"]
    return count, expected_mask


def main():
    data = json.loads((ROOT / "RESULTS.json").read_text())
    delta = int(data["delta"], 16)
    target = int(data["target"], 16)
    total = 0
    masks = []
    for component in data["components"]:
        count, mask = span(component, delta, target)
        total += count
        masks.append(mask)
    assert len(masks) == len(set(masks))
    assert total == data["total_solutions"] == 1_259_520
    assert data["all_components_verified"] is True
    print(
        json.dumps(
            {
                "status": "PASS",
                "components": len(masks),
                "solutions_checked": total,
                "affine_spans_disjoint": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
