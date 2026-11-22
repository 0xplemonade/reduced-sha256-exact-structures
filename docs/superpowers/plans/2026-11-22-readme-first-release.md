# README-first reduced SHA-256 release implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish `0xplemonade/reduced-sha256-exact-structures` as a small, README-first repository of five exact reduced-round SHA-256 result groups with deterministic verification and explicit claim limits.

**Architecture:** Preserve the two compact proof packets whose layouts are already self-contained. Repackage the other three result groups around public, path-independent verifiers. A root claim catalog drives one non-solving verifier, while each result directory owns its evidence, local README, and focused check.

**Tech stack:** Python 3 standard library, C11 with optional OpenMP for complete finite scans, Markdown, JSON, SHA-256 manifests, Git, and GitHub CLI.

---

## File map

The completed repository contains these files:

```text
.gitignore
README.md
claims.json
verify.py
MANIFEST.sha256
CITATION.cff
LICENSE
LICENSE-DOCS
THIRD_PARTY.md
docs/
  methods.md
  prior-art.md
  provenance.md
  discussion-1376.md
  release-notes-v0.1.0.md
  superpowers/specs/2026-11-22-readme-first-release-design.md
  superpowers/plans/2026-11-22-readme-first-release.md
results/
  schedule-constructions/
    README.md
    PROOF.md
    EXAMPLE.json
    INPUTS.json
    RESULTS.json
    SOURCE_BINDINGS.json
    chart.py
    fibre_algebra.py
    generate.py
    reference.py
    state_coordinates.py
    verify.py
  conditional-modification/
    README.md
    PROOF.md
    INPUTS.json
    RESULTS.json
    SOURCE_BINDINGS.json
    normal_form.py
    reference.py
    verify.py
  common-w39-obstruction/
    README.md
    PROOF.md
    RECONCILIATION.md
    RESULT.json
    SCAN_R37.json
    SCAN_R38.json
    scan_family.c
    verify.py
  derivative-fibres/
    README.md
    PROOF.md
    RESULTS.json
    scan.c
    verify.py
  carry-characteristics/
    README.md
    FORMULAS.md
    CORES.json
    WITNESSES.json
    verify.py
tests/
  __init__.py
  support.py
  test_carry_characteristics.py
  test_claim_catalog.py
  test_common_w39.py
  test_conditional_modification.py
  test_derivative_fibres.py
  test_docs.py
  test_manifest.py
  test_repository_metadata.py
  test_schedule_constructions.py
tools/
  build_manifest.py
```

`results/*/verify.py` owns semantic verification for one result group.
`claims.json` declares the command and evidence class for each group.
The root `verify.py` checks `MANIFEST.sha256`, runs every declared command, and
prints one JSON summary.

## Task 1: Add repository metadata and a standard test helper

**Files:**

- Create: `.gitignore`
- Create: `LICENSE`
- Create: `LICENSE-DOCS`
- Create: `CITATION.cff`
- Create: `THIRD_PARTY.md`
- Create: `tests/__init__.py`
- Create: `tests/support.py`
- Create: `tests/test_repository_metadata.py`

- [ ] **Step 1: Write the failing repository metadata test**

Create `tests/test_repository_metadata.py`:

```python
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
```

- [ ] **Step 2: Run the test and verify that it fails**

Run:

```bash
python3 -m unittest tests.test_repository_metadata -v
```

Expected: two errors because `LICENSE`, `LICENSE-DOCS`, `CITATION.cff`, and
`THIRD_PARTY.md` do not exist.

- [ ] **Step 3: Add the metadata files**

Add this `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
build/
*.o
*.out
.DS_Store
```

Use the unmodified Apache License 2.0 text from the GitHub license API for
`LICENSE`. Use the unmodified Creative Commons Attribution 4.0 legal code for
`LICENSE-DOCS`. Add this `CITATION.cff`:

```yaml
cff-version: 1.2.0
message: Cite this repository when you use its proofs, code, or datasets.
title: Reduced SHA-256 exact structures
type: software
authors:
  - family-names: 0xplemonade
repository-code: https://github.com/0xplemonade/reduced-sha256-exact-structures
version: 0.1.0
date-released: 2026-11-22
license: Apache-2.0 AND CC-BY-4.0
```

Add this initial `THIRD_PARTY.md`:

```markdown
# Third-party material

Original source code in this repository is licensed under Apache-2.0.
Original documentation, proofs, and datasets are licensed under CC BY 4.0.

Do not publish a copied file unless its reuse terms are known. A source hash
and a citation do not replace a license.

The release uses public reduced-round SHA-256 examples as attributed research
inputs. `docs/provenance.md` identifies each example and the exact result that
uses it. No third-party source file is redistributed unless this document lists
its license and source.
```

Create `tests/support.py`:

```python
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
```

Create an empty `tests/__init__.py` so module-based `unittest` commands always
resolve this repository's test package.

- [ ] **Step 4: Run the metadata test**

Run:

```bash
python3 -m unittest tests.test_repository_metadata -v
```

Expected: `Ran 2 tests` and `OK`.

- [ ] **Step 5: Commit the metadata foundation**

```bash
git add .gitignore LICENSE LICENSE-DOCS CITATION.cff THIRD_PARTY.md tests
git commit -m "chore: add release metadata and test helper"
```

## Task 2: Import the schedule-construction proof packet

**Files:**

- Create: `results/schedule-constructions/README.md`
- Create: `results/schedule-constructions/PROOF.md`
- Create: `results/schedule-constructions/EXAMPLE.json`
- Create: `results/schedule-constructions/INPUTS.json`
- Create: `results/schedule-constructions/RESULTS.json`
- Create: `results/schedule-constructions/SOURCE_BINDINGS.json`
- Create: `results/schedule-constructions/chart.py`
- Create: `results/schedule-constructions/fibre_algebra.py`
- Create: `results/schedule-constructions/generate.py`
- Create: `results/schedule-constructions/reference.py`
- Create: `results/schedule-constructions/state_coordinates.py`
- Create: `results/schedule-constructions/verify.py`
- Create: `tests/test_schedule_constructions.py`

- [ ] **Step 1: Write the failing schedule-construction test**

Create `tests/test_schedule_constructions.py`:

```python
import json
import subprocess
import sys
import unittest
from tests.support import ROOT, run_result


class ScheduleConstructionsTest(unittest.TestCase):
    def test_saved_result_replays_exactly(self):
        result = run_result("schedule-constructions")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["admissible_pair_replays"], 384)
        self.assertEqual(result["unrestricted_Z_W13_inverse_checks"], 144)
        self.assertEqual(result["fibre_counts"]["p4_W14"], 1 << 27)
        self.assertEqual(result["fibre_counts"]["p4_W23"], 1 << 27)
        self.assertEqual(result["fibre_counts"]["p1_W14"], 138_936_320)
        self.assertEqual(result["fibre_counts"]["p1_W23"], 138_936_320)
        self.assertEqual(result["S14_fibre_counting"]["p4_average_including_empty"], 1 << 22)
        self.assertEqual(result["S14_fibre_counting"]["p1_average_including_empty"], 4_494_400)

    def test_generator_reconstructs_pair_from_coordinates(self):
        directory = ROOT / "results" / "schedule-constructions"
        process = subprocess.run(
            [sys.executable, "generate.py", "--example", "0"],
            cwd=directory,
            check=True,
            capture_output=True,
            text=True,
        )
        generated = json.loads(process.stdout)
        self.assertEqual(generated["status"], "PASS")
        self.assertEqual(generated["pair_sha256_be"], "b16fec39f5e4ae2041b91cd8f2a358417163b0ed098f1d2c30212ffba642d80f")
        self.assertEqual(generated["support"], [6, 7, 9, 14, 22, 23, 37])
        self.assertEqual(len(generated["left_W0_W15"]), 16)
        self.assertEqual(len(generated["right_W0_W15"]), 16)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify that it fails**

Run:

```bash
python3 -m unittest tests.test_schedule_constructions -v
```

Expected: error because `results/schedule-constructions/verify.py` does not exist.

- [ ] **Step 3: Copy the self-contained proof packet**

From the repository root, run:

```bash
mkdir -p results/schedule-constructions
cp ../state_coordinate_s13_chart/INPUTS.json results/schedule-constructions/
cp ../state_coordinate_s13_chart/PROOF.md results/schedule-constructions/
cp ../state_coordinate_s13_chart/RESULTS.json results/schedule-constructions/
cp ../state_coordinate_s13_chart/SOURCE_BINDINGS.json results/schedule-constructions/
cp ../state_coordinate_s13_chart/chart.py results/schedule-constructions/
cp ../state_coordinate_s13_chart/fibre_algebra.py results/schedule-constructions/
cp ../state_coordinate_s13_chart/reference.py results/schedule-constructions/
cp ../state_coordinate_s13_chart/state_coordinates.py results/schedule-constructions/
cp ../state_coordinate_s13_chart/verify.py results/schedule-constructions/
chmod +x results/schedule-constructions/verify.py
```

Do not copy the packet's old `README.md` or `SHA256SUMS`. The root release
manifest replaces the old packet manifest.

- [ ] **Step 4: Add a coordinate-only example and constructive CLI**

Create `results/schedule-constructions/EXAMPLE.json`:

```json
{
  "schema": "reduced-sha256-construction-example-v1",
  "examples": [
    {
      "arm": "p4",
      "entry_words": ["6a09e667", "bb67ae85", "3c6ef372", "a54ff53a", "510e527f", "9b05688c", "1f83d9ab", "5be0cd19"],
      "prefix_W0_W9": ["1112d7db", "0406f4a9", "07a0cec2", "545c4e7c", "d035005a", "9a29694a", "06440e60", "16185001", "9302d7a2", "d17ee0f6"],
      "W22": "0016c400",
      "V_W14": "f3cf8db0",
      "Z_W23": "dac76e5d",
      "left_A10_A12": ["00000000", "00000000", "00000000"],
      "expected_support": [6, 7, 9, 14, 22, 23, 37],
      "expected_pair_sha256_be": "b16fec39f5e4ae2041b91cd8f2a358417163b0ed098f1d2c30212ffba642d80f"
    }
  ]
}
```

Create `results/schedule-constructions/generate.py`:

```python
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
```

`EXAMPLE.json` contains coordinates and an expected digest, not the final
message pair. The command must reconstruct both messages through the public
chart before it prints them.

- [ ] **Step 5: Add the schedule-construction README**

Create `results/schedule-constructions/README.md` with this content:

```markdown
# Constructive schedule coordinates and state-preserving fibres

**Evidence class:** proved, with bounded independent replay.

This result gives an exact coordinate chart for two retained sparse SHA-256
schedule families. Three freely chosen left outputs fix both ordered states at
S13. The remaining admitted completions form exact S13-preserving fibres.

For the shifted-public-r38 numerical core, the fixed-S13 fibre has size `2^54`.
For the public-r37 core, its size is `N^2`, where `N = 138,936,320`. Fixing a
common W13 gives a conditional S14 fibre. Its exact average size, including
empty fibres, is `2^22` for the first core and `4,494,400` for the second.

This is a coordinate change, not additional freedom. It does not prove endpoint
success, independent lane recombination, a collision, or an attack cost.

Run `python3 generate.py --example 0` to construct and print a verified paired
message schedule from coordinates. The input file does not contain the final
message pair.

Run `python3 verify.py` to replay 384 admitted schedule pairs and 144 inverse
checks. See [PROOF.md](PROOF.md) for the all-domain argument.
```

- [ ] **Step 6: Run the focused test**

Run:

```bash
python3 -m unittest tests.test_schedule_constructions -v
```

Expected: `Ran 2 tests` and `OK`.

- [ ] **Step 7: Commit the schedule-construction result**

```bash
git add results/schedule-constructions tests/test_schedule_constructions.py
git commit -m "feat: publish constructive schedule chart"
```

## Task 3: Import the conditional-modification interface

**Files:**

- Create: `results/conditional-modification/README.md`
- Create: `results/conditional-modification/PROOF.md`
- Create: `results/conditional-modification/INPUTS.json`
- Create: `results/conditional-modification/RESULTS.json`
- Create: `results/conditional-modification/SOURCE_BINDINGS.json`
- Create: `results/conditional-modification/normal_form.py`
- Create: `results/conditional-modification/reference.py`
- Create: `results/conditional-modification/verify.py`
- Create: `tests/test_conditional_modification.py`

- [ ] **Step 1: Write the failing conditional-modification test**

Create `tests/test_conditional_modification.py`:

```python
import unittest
from tests.support import run_result


class ConditionalModificationTest(unittest.TestCase):
    def test_normal_form_and_replay(self):
        result = run_result("conditional-modification")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["admissible_fixture_replays"], 6)
        self.assertEqual(result["arbitrary_context_identity_checks"], 2048)
        self.assertEqual(result["synthetic_input_origin_covariance_checks"], 256)
        self.assertEqual(result["row29_inverse_coordinate_checks"], 6)
        self.assertEqual(result["small_sigma0_inverse_two_sided_basis_checks"], 64)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify that it fails**

Run:

```bash
python3 -m unittest tests.test_conditional_modification -v
```

Expected: error because `results/conditional-modification/verify.py` does not
exist.

- [ ] **Step 3: Copy the bounded identity packet**

```bash
mkdir -p results/conditional-modification
cp ../sha256_paper_transfer/REPORT.md results/conditional-modification/PROOF.md
cp ../sha256_paper_transfer/checks/INPUTS.json results/conditional-modification/
cp ../sha256_paper_transfer/checks/RESULTS.json results/conditional-modification/
cp ../sha256_paper_transfer/checks/SOURCE_BINDINGS.json results/conditional-modification/
cp ../sha256_paper_transfer/checks/normal_form.py results/conditional-modification/
cp ../sha256_paper_transfer/checks/reference.py results/conditional-modification/
cp ../sha256_paper_transfer/checks/verify.py results/conditional-modification/
chmod +x results/conditional-modification/verify.py
```

- [ ] **Step 4: Add the conditional-modification README**

Create `results/conditional-modification/README.md`:

```markdown
# Conditional message modification through P(V) and Q(V)

**Evidence class:** proved local identity, with bounded replay.

At a fixed admitted context, the round-15 state difference is controlled by two
explicit functions, `P(V)` and `Q(V)`, of one 32-bit parameter. A target on the
two varying output words is therefore an exact joint preimage condition on one
parameter.

The two functions are coupled. This result does not make them independent
32-bit trials, prove a cheap inverse, or construct an r39 or r40 endpoint.

Run `python3 verify.py` to replay six genuine schedules, 2,048 unrestricted
algebra checks, 256 coordinate-shift checks, and both directions of the
small-sigma0 inverse on the 32 basis vectors.
```

- [ ] **Step 5: Run the focused test**

```bash
python3 -m unittest tests.test_conditional_modification -v
```

Expected: `Ran 1 test` and `OK`.

- [ ] **Step 6: Commit the conditional interface**

```bash
git add results/conditional-modification tests/test_conditional_modification.py
git commit -m "feat: publish conditional modification interface"
```

## Task 4: Make the common-W39 obstruction packet public and path-independent

**Files:**

- Create: `results/common-w39-obstruction/README.md`
- Create: `results/common-w39-obstruction/PROOF.md`
- Create: `results/common-w39-obstruction/RECONCILIATION.md`
- Create: `results/common-w39-obstruction/RESULT.json`
- Create: `results/common-w39-obstruction/SCAN_R37.json`
- Create: `results/common-w39-obstruction/SCAN_R38.json`
- Create: `results/common-w39-obstruction/scan_family.c`
- Create: `results/common-w39-obstruction/verify.py`
- Create: `tests/test_common_w39.py`

- [ ] **Step 1: Write the failing common-W39 test**

Create `tests/test_common_w39.py`:

```python
import unittest
from tests.support import run_result


class CommonW39Test(unittest.TestCase):
    def test_both_numerical_cores_have_empty_intersection(self):
        result = run_result("common-w39-obstruction")
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["primary_common_W39_feasible"])
        self.assertEqual(result["primary_W22_passing_both"], 0)
        self.assertFalse(result["analogous_r37_common_W39_feasible"])
        self.assertEqual(result["analogous_r37_W22_passing_both"], 0)
        self.assertFalse(result["full_scans_replayed"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify that it fails**

```bash
python3 -m unittest tests.test_common_w39 -v
```

Expected: error because the result directory does not exist.

- [ ] **Step 3: Copy the proof, counts, scanner, and verifier**

```bash
mkdir -p results/common-w39-obstruction
cp ../r40_common_w39_compat/REPORT.md results/common-w39-obstruction/PROOF.md
cp ../r40_common_w39_compat/RECONCILIATION.md results/common-w39-obstruction/
cp ../r40_common_w39_compat/RESULT.json results/common-w39-obstruction/
cp ../r40_common_w39_compat/SCAN_R37.json results/common-w39-obstruction/
cp ../r40_common_w39_compat/SCAN_R38.json results/common-w39-obstruction/
cp ../r40_common_w39_compat/scan_family.c results/common-w39-obstruction/
cp ../r40_common_w39_compat/verify.py results/common-w39-obstruction/
chmod +x results/common-w39-obstruction/verify.py
```

- [ ] **Step 4: Remove private paths and solver use from the verifier**

In `results/common-w39-obstruction/verify.py`:

1. Delete the `INPUTS` constant and the `sha256()` helper.
2. Delete the loop that hashes `INPUTS` near the end of `main()`.
3. Delete `reduced_z3_unsat()` and the conditional `import z3` block.
4. Replace the final summary with:

```python
    print(json.dumps({
        "status": "PASS",
        "primary_common_W39_feasible": False,
        "primary_W22_passing_both": scan_r38["W22_passing_both"],
        "analogous_r37_common_W39_feasible": False,
        "analogous_r37_W22_passing_both": scan_r37["W22_passing_both"],
        "full_scans_replayed": args.full_scan,
    }, indent=2, sort_keys=True))
```

The saved `RESULT.json` already contains both complete schedule witnesses and
all numerical claims needed by the public verifier. The public verifier must
read no file outside its own result directory.

- [ ] **Step 5: Add the common-W39 README**

Create `results/common-w39-obstruction/README.md`:

```markdown
# Common-W39 extension obstruction

**Evidence class:** exhaustively counted, with algebraic reduction.

For each of two retained numerical cores, common W39 requires one exact
small-sigma1 derivative condition while row 24 requires membership in a second
finite derivative image. Complete enumeration over all 32-bit W22 values gives
zero values that satisfy both requirements.

The shifted-public-r38 arm has 344,457,216 W22 values that pass row 24 and 64
whose derived dW37 admits the terminal derivative. Their intersection is empty.
The public-r37 arm has counts 540,494,592 and 4,432, with the same empty
intersection.

This closes only the retained numerical differences and support. It does not
exclude nonzero dW39 final-round cancellation or a changed core.

Run `python3 verify.py` for the compact check. Run `python3 verify.py
--full-scan` to rebuild the C scanner and repeat both complete enumerations.
```

- [ ] **Step 6: Run the focused test**

```bash
python3 -m unittest tests.test_common_w39 -v
```

Expected: `Ran 1 test` and `OK` without importing Z3.

- [ ] **Step 7: Commit the obstruction packet**

```bash
git add results/common-w39-obstruction tests/test_common_w39.py
git commit -m "feat: publish common-W39 obstruction"
```

## Task 5: Add a compact verifier for the derivative fibre decomposition

**Files:**

- Create: `results/derivative-fibres/README.md`
- Create: `results/derivative-fibres/PROOF.md`
- Create: `results/derivative-fibres/RESULTS.json`
- Create: `results/derivative-fibres/scan.c`
- Create: `results/derivative-fibres/verify.py`
- Create: `tests/test_derivative_fibres.py`

- [ ] **Step 1: Write the failing derivative-fibre test**

Create `tests/test_derivative_fibres.py`:

```python
import unittest
from tests.support import run_result


class DerivativeFibresTest(unittest.TestCase):
    def test_all_six_affine_components_replay(self):
        result = run_result("derivative-fibres")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["components"], 6)
        self.assertEqual(result["solutions_checked"], 1_259_520)
        self.assertTrue(result["affine_spans_disjoint"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify that it fails**

```bash
python3 -m unittest tests.test_derivative_fibres -v
```

Expected: error because the verifier does not exist.

- [ ] **Step 3: Copy the proof, result, and full scanner**

```bash
mkdir -p results/derivative-fibres
cp ../r40_table23_w39_fibre/REPORT.md results/derivative-fibres/PROOF.md
cp ../r40_table23_w39_fibre/RESULTS.json results/derivative-fibres/
cp ../r40_table23_w39_fibre/scan.c results/derivative-fibres/
```

Do not copy the compiled `scan` binary.

- [ ] **Step 4: Implement the affine-span verifier**

Create `results/derivative-fibres/verify.py`:

```python
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
    print(json.dumps({
        "status": "PASS",
        "components": len(masks),
        "solutions_checked": total,
        "affine_spans_disjoint": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Add the derivative-fibre README**

Create `results/derivative-fibres/README.md`:

```markdown
# Table 23 W24 derivative fibres

**Evidence class:** exhaustively counted and affine-span verified.

The equation

`small_sigma0(x + 0x03010000) - small_sigma0(x) = 0xc05a1dc0`

has exactly 1,259,520 solutions. They form six disjoint affine GF(2)
components with dimensions 20, 17, 16, 13, 11, and 12.

Run `python3 verify.py` to enumerate all six saved affine spans and check every
member. Run the documented C scanner to repeat the original complete 32-bit
enumeration.

This derivative fibre does not make W39 common and does not prove state
reachability or a collision path.
```

- [ ] **Step 6: Run the focused test**

```bash
python3 -m unittest tests.test_derivative_fibres -v
```

Expected: `Ran 1 test` and `OK` after checking 1,259,520 span members.

- [ ] **Step 7: Commit the fibre decomposition**

```bash
git add results/derivative-fibres tests/test_derivative_fibres.py
git commit -m "feat: publish derivative fibre decomposition"
```

## Task 6: Publish independently replayable carry characteristics

**Files:**

- Create: `results/carry-characteristics/README.md`
- Create: `results/carry-characteristics/FORMULAS.md`
- Create: `results/carry-characteristics/CORES.json`
- Create: `results/carry-characteristics/WITNESSES.json`
- Create: `results/carry-characteristics/verify.py`
- Create: `tests/test_carry_characteristics.py`

- [ ] **Step 1: Write the failing carry-characteristic test**

Create `tests/test_carry_characteristics.py`:

```python
import unittest
from tests.support import run_result


class CarryCharacteristicsTest(unittest.TestCase):
    def test_six_witnesses_and_local_theorem_replay(self):
        result = run_result("carry-characteristics")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["witnesses_replayed"], 6)
        self.assertEqual(result["local_theorem_cases"], 3136)
        self.assertTrue(result["transfer_and_reset_verified"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify that it fails**

```bash
python3 -m unittest tests.test_carry_characteristics -v
```

Expected: error because the result directory does not exist.

- [ ] **Step 3: Copy only the proof inputs and six complete witnesses**

```bash
mkdir -p results/carry-characteristics
cp ../r40_multibit_carry_characteristic/FORMULAS.md results/carry-characteristics/
cp ../r40_state_first_differential_search/inputs/CORES.json results/carry-characteristics/
cp ../r40_multibit_carry_characteristic/results/WITNESSES.json results/carry-characteristics/
```

Do not copy hidden answers, generated headers, compiled binaries, solver files,
or the 12,582,912-cell census. Version 0.1 publishes the local theorem and six
constructive witnesses, not the original census-rate claim.

- [ ] **Step 4: Implement an independent witness verifier**

Create `results/carry-characteristics/verify.py` with this prefix and the
`main()` below it:

```python
#!/usr/bin/env python3
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent
MASK = (1 << 32) - 1
IV = (
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
)
K = tuple(int(value, 16) for value in """
428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967
27b70a85 2e1b2138 4d2c6dfc 53380d13 650a7354 766a0abb 81c2c92e 92722c85
""".split())


def rotate_right(value, count):
    return ((value >> count) | (value << (32 - count))) & MASK


def small_sigma0(value):
    return rotate_right(value, 7) ^ rotate_right(value, 18) ^ (value >> 3)


def small_sigma1(value):
    return rotate_right(value, 17) ^ rotate_right(value, 19) ^ (value >> 10)


def big_sigma0(value):
    return rotate_right(value, 2) ^ rotate_right(value, 13) ^ rotate_right(value, 22)


def big_sigma1(value):
    return rotate_right(value, 6) ^ rotate_right(value, 11) ^ rotate_right(value, 25)


def choose(x, y, z):
    return (x & y) ^ ((~x) & z)


def majority(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def expand(seed):
    words = list(seed)
    for index in range(16, 40):
        words.append((words[index - 16] + small_sigma0(words[index - 15]) + words[index - 7] + small_sigma1(words[index - 2])) & MASK)
    return words


def step(state, word, index):
    a, b, c, d, e, f, g, h = state
    first = (h + big_sigma1(e) + choose(e, f, g) + K[index] + word) & MASK
    second = (big_sigma0(a) + majority(a, b, c)) & MASK
    return ((first + second) & MASK, a, b, c, (d + first) & MASK, e, f, g)
```

Append this `main()`:

```python
def main():
    cores = json.loads((ROOT / "CORES.json").read_text())
    witnesses = json.loads((ROOT / "WITNESSES.json").read_text())["witnesses"]
    for row in witnesses:
        core = cores[row["ci"]]
        left = row["left"]
        right = row["right"]
        assert expand(left[:16]) == left
        assert expand(right[:16]) == right
        assert [i for i, (a, b) in enumerate(zip(left, right)) if a != b] == core["support"]
        left_trace = [IV]
        right_trace = [IV]
        for index in range(40):
            left_trace.append(step(left_trace[-1], left[index], index))
            right_trace.append(step(right_trace[-1], right[index], index))
        t = core["t"]
        assert list(left_trace[t]) == row["state_l"]
        assert list(right_trace[t]) == row["state_r"]
        assert list(left_trace[t + 1]) == row["next_l"]
        assert list(right_trace[t + 1]) == row["next_r"]
        assert list(left_trace[-1]) == row["final_l"]
        assert list(right_trace[-1]) == row["final_r"]
        left_state = left_trace[t]
        right_state = right_trace[t]
        left_operands = (
            left_state[7], big_sigma1(left_state[4]),
            choose(*left_state[4:7]), K[t], left[t],
            big_sigma0(left_state[0]), majority(*left_state[:3]),
        )
        right_operands = (
            right_state[7], big_sigma1(right_state[4]),
            choose(*right_state[4:7]), K[t], right[t],
            big_sigma0(right_state[0]), majority(*right_state[:3]),
        )
        left_carry = right_carry = 0
        sigma = []
        kappa = [0]
        beta = []
        for bit in range(32):
            left_sum = sum(value >> bit & 1 for value in left_operands)
            right_sum = sum(value >> bit & 1 for value in right_operands)
            sigma.append(right_sum - left_sum)
            beta.append(((right_sum + right_carry) & 1) - ((left_sum + left_carry) & 1))
            left_carry = (left_sum + left_carry) >> 1
            right_carry = (right_sum + right_carry) >> 1
            kappa.append(right_carry - left_carry)
            assert beta[-1] == sigma[-1] + kappa[-2] - 2 * kappa[-1]
        assert sigma == row["sigma"]
        assert kappa == row["kappa"]
        assert beta == row["beta"]
        b0 = (right_state[0] - left_state[0] + core["delta"][core["last"]]) & MASK
        b1 = (right_trace[t + 1][0] - left_trace[t + 1][0]) & MASK
        assert (b0, b1) == (row["B0"], row["B1"])
        assert not (b0 & 1023) and not (b1 & 1023)
        assert sigma[8] + kappa[8] == 2 * kappa[9]
        assert sigma[9] + kappa[9] == 0 and kappa[10] == 0

    local_cases = 0
    for left_sum in range(8):
        for right_sum in range(8):
            for left_carry in range(7):
                for right_carry in range(7):
                    sigma = right_sum - left_sum
                    kappa = right_carry - left_carry
                    beta = ((right_sum + right_carry) & 1) - ((left_sum + left_carry) & 1)
                    next_kappa = (right_sum + right_carry) // 2 - (left_sum + left_carry) // 2
                    assert beta == sigma + kappa - 2 * next_kappa
                    if (sigma + kappa) % 2 == 0:
                        assert beta == 0
                        assert next_kappa == (sigma + kappa) // 2
                    local_cases += 1

    print(json.dumps({
        "status": "PASS",
        "witnesses_replayed": len(witnesses),
        "local_theorem_cases": local_cases,
        "transfer_and_reset_verified": True,
    }, sort_keys=True))
```

- [ ] **Step 5: Add the carry-characteristic README**

Create `results/carry-characteristics/README.md`:

```markdown
# Carry-transfer and carry-reset characteristics

**Evidence class:** proved local carry identity with six constructive witnesses.

For one bit of the seven-operand SHA-256 round sum, let `sigma` be the signed
operand-bit difference and `kappa` the incoming carry difference. The output
bit difference satisfies `beta = sigma + kappa - 2*kappa_next`. When
`sigma + kappa` is even, the output bit closes and the carry difference becomes
half that sum.

Six complete 40-word schedule pairs exhibit a two-bit transfer and reset inside
the declared r40 families. The verifier reconstructs both schedules, replays
both compression traces from the standard IV, and checks every saved carry.

These local characteristics are not full boundary roots, collisions, or attack
cost improvements.
```

- [ ] **Step 6: Run the focused test**

```bash
python3 -m unittest tests.test_carry_characteristics -v
```

Expected: `Ran 1 test` and `OK` after six complete schedule and state replays.

- [ ] **Step 7: Commit the carry characteristics**

```bash
git add results/carry-characteristics tests/test_carry_characteristics.py
git commit -m "feat: publish carry-reset witnesses"
```

## Task 7: Add the claim catalog, manifest builder, and root verifier

**Files:**

- Create: `claims.json`
- Create: `verify.py`
- Create: `tools/build_manifest.py`
- Create: `tests/test_claim_catalog.py`
- Create: `tests/test_manifest.py`

- [ ] **Step 1: Write failing catalog and manifest tests**

Create `tests/test_claim_catalog.py`:

```python
from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ClaimCatalogTest(unittest.TestCase):
    def test_catalog_has_one_entry_per_result_directory(self):
        catalog = json.loads((ROOT / "claims.json").read_text())
        self.assertEqual(catalog["schema"], "reduced-sha256-claims-v1")
        ids = [claim["id"] for claim in catalog["claims"]]
        self.assertEqual(ids, [
            "schedule-constructions",
            "conditional-modification",
            "common-w39-obstruction",
            "derivative-fibres",
            "carry-characteristics",
        ])
        for claim in catalog["claims"]:
            self.assertIn(claim["evidence_class"], {
                "proved", "exhaustively-counted", "constructive-witnesses"
            })
            self.assertTrue((ROOT / claim["directory"] / "README.md").is_file())
            self.assertEqual(claim["command"], ["python3", "verify.py"])


if __name__ == "__main__":
    unittest.main()
```

Create `tests/test_manifest.py`:

```python
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
```

- [ ] **Step 2: Run the tests and verify that they fail**

```bash
python3 -m unittest tests.test_claim_catalog tests.test_manifest -v
```

Expected: errors because `claims.json` and `MANIFEST.sha256` do not exist.

- [ ] **Step 3: Create the claim catalog**

Create `claims.json`:

```json
{
  "schema": "reduced-sha256-claims-v1",
  "claims": [
    {"id": "schedule-constructions", "title": "Constructive schedule coordinates and state-preserving fibres", "evidence_class": "proved", "directory": "results/schedule-constructions", "command": ["python3", "verify.py"]},
    {"id": "conditional-modification", "title": "Conditional message modification through P(V) and Q(V)", "evidence_class": "proved", "directory": "results/conditional-modification", "command": ["python3", "verify.py"]},
    {"id": "common-w39-obstruction", "title": "Common-W39 extension obstruction", "evidence_class": "exhaustively-counted", "directory": "results/common-w39-obstruction", "command": ["python3", "verify.py"]},
    {"id": "derivative-fibres", "title": "Table 23 W24 derivative fibres", "evidence_class": "exhaustively-counted", "directory": "results/derivative-fibres", "command": ["python3", "verify.py"]},
    {"id": "carry-characteristics", "title": "Carry-transfer and carry-reset characteristics", "evidence_class": "constructive-witnesses", "directory": "results/carry-characteristics", "command": ["python3", "verify.py"]}
  ]
}
```

- [ ] **Step 4: Implement the deterministic manifest builder**

Create `tools/build_manifest.py`:

```python
#!/usr/bin/env python3
from pathlib import Path
import hashlib


ROOT = Path(__file__).resolve().parents[1]


def included(path):
    return path.is_file() and ".git" not in path.parts and path.name != "MANIFEST.sha256" and "__pycache__" not in path.parts


paths = sorted(path for path in ROOT.rglob("*") if included(path))
lines = []
for path in paths:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
(ROOT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
```

- [ ] **Step 5: Implement the root verifier**

Create `verify.py`:

```python
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
    process = subprocess.run(claim["command"], cwd=ROOT / claim["directory"], check=True, capture_output=True, text=True)
    result = json.loads(process.stdout)
    assert result["status"] == "PASS", claim["id"]
    return {"id": claim["id"], "evidence_class": claim["evidence_class"], "status": result["status"]}


def main():
    manifest_files = verify_manifest()
    catalog = json.loads((ROOT / "claims.json").read_text())
    assert catalog["schema"] == "reduced-sha256-claims-v1"
    claims = [verify_claim(claim) for claim in catalog["claims"]]
    print(json.dumps({"status": "PASS", "manifest_files": manifest_files, "claims": claims, "scientific_solver_queries": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Build the first manifest and run the tests**

```bash
python3 tools/build_manifest.py
python3 -m unittest tests.test_claim_catalog tests.test_manifest -v
python3 verify.py
```

Expected: both unit tests pass. The root verifier prints JSON with
`"status": "PASS"`, five claims, and `"scientific_solver_queries": 0`.

- [ ] **Step 7: Commit the root verification system**

```bash
git add claims.json verify.py tools tests/test_claim_catalog.py tests/test_manifest.py MANIFEST.sha256
git commit -m "feat: add root claim verifier"
```

## Task 8: Write the README, provenance, methods, and prior-art review

**Files:**

- Create: `README.md`
- Create: `docs/methods.md`
- Create: `docs/prior-art.md`
- Create: `docs/provenance.md`
- Modify: `THIRD_PARTY.md`
- Create: `tests/test_docs.py`

- [ ] **Step 1: Write the failing documentation test**

Create `tests/test_docs.py`:

```python
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DocumentationTest(unittest.TestCase):
    def test_required_sections_and_claim_links(self):
        readme = (ROOT / "README.md").read_text()
        for heading in ("# Reduced SHA-256 exact structures", "## What this repository contains", "## What this repository does not claim", "## Generate a valid paired schedule", "## Results", "## Verify the release", "## Reuse and citation", "## Open questions"):
            self.assertIn(heading, readme)
        for slug in ("schedule-constructions", "conditional-modification", "common-w39-obstruction", "derivative-fibres", "carry-characteristics"):
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
        for path in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.py")) + list(ROOT.rglob("*.json")):
            self.assertNotIn("/root/.t3/", path.read_text(errors="ignore"), path)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify that it fails**

```bash
python3 -m unittest tests.test_docs -v
```

Expected: error because the root `README.md` does not exist.

- [ ] **Step 3: Write the root README**

Use this exact heading order:

```text
# Reduced SHA-256 exact structures
## What this repository contains
## What this repository does not claim
## Results
## Verify the release
## Reuse and citation
## Relationship to sha256-structural-data
## Open questions
```

Open with two paragraphs that say the repository contains exact, replayable
reduced-round SHA-256 results and that the root verifier uses no SAT or SMT
solver. Add a five-row result table with columns Result, Evidence, Scope, and
Reproduce. Link the rows to `results/schedule-constructions/README.md`,
`results/conditional-modification/README.md`,
`results/common-w39-obstruction/README.md`,
`results/derivative-fibres/README.md`, and
`results/carry-characteristics/README.md`. State that the release
does not claim a full SHA-256 result, a new collision, an improved attack
exponent, independent lane freedom, or literature novelty. Document
`python3 verify.py` and explain that complete 2^32 scans are opt-in.

Add `## Generate a valid paired schedule` before the result table. Show this
command:

```bash
python3 results/schedule-constructions/generate.py --example 0
```

Explain that the command reconstructs both 16-word message blocks from an
entry, ten-word prefix, W22, W14, W23, and three chosen left outputs. Call the
output a valid paired message schedule with verified sparse support. State in
the same paragraph that it is not a collision.

- [ ] **Step 4: Write methods and provenance documents**

`docs/methods.md` must explain right-minus-left modular differences, the four
evidence classes, why quick verification does not repeat a 2^32 scan, and how
full-scan commands rebuild native scanners in temporary directories.

`docs/provenance.md` must contain one table row per result group with source
packet names, full SHA-256 hashes of every copied source file, the import
transformation, and the related public predecessor. Generate hashes with
`sha256sum` from the original workspace. Do not include absolute paths.

- [ ] **Step 5: Perform and record the targeted prior-art review**

Create `docs/prior-art.md`. Search IACR ePrint, Springer proceedings, DOI
records, and authors' official paper pages for these claim families:

1. Exact schedule-coordinate bijections and state-preserving fibres in
   reduced-round SHA-256.
2. One-parameter conditional message modification through coupled next-state
   functions.
3. Complete derivative-image intersection obstructions for a fixed support.
4. Affine decomposition of small-sigma modular derivative fibres.

Include Mendel, Nad, and Schlaeffer's 2013 reduced SHA-256 work, SAT-based
SHA-256 cryptanalysis, and work on differential equations of modular addition.
For each result group, record search terms, closest primary sources, overlap,
remaining distinction, and one wording decision: `no novelty claim`,
`potentially distinct`, or `covered by prior work`.

- [ ] **Step 6: Complete third-party attribution**

Update `THIRD_PARTY.md` with every public message pair, HashSmash submission,
paper, and copied source file used by the release. For each redistributed file,
record its source URL, SHA-256 hash, author, and license. Replace a file with a
derived numerical fixture when reuse permission is unclear.

- [ ] **Step 7: Run documentation and full unit tests**

```bash
python3 -m unittest discover -s tests -v
python3 tools/build_manifest.py
python3 verify.py
```

Expected: all tests pass. The root verifier reports five passing claims and no
scientific solver queries.

- [ ] **Step 8: Commit the public documentation**

```bash
git add README.md docs THIRD_PARTY.md tests/test_docs.py MANIFEST.sha256
git commit -m "docs: explain exact reduced SHA-256 results"
```

## Task 9: Run release verification from a clean checkout

**Files:**

- Create: `docs/release-notes-v0.1.0.md`
- Update: `MANIFEST.sha256`

- [ ] **Step 1: Run both complete native scans**

```bash
python3 results/common-w39-obstruction/verify.py --full-scan
```

Expected: status `PASS`, both intersection counts equal zero, and
`full_scans_replayed` equals `true`.

Compile and run the derivative scanner:

```bash
tmpdir=$(mktemp -d)
cc -O3 -march=native -fopenmp -Wall -Wextra -Werror results/derivative-fibres/scan.c -o "$tmpdir/scan"
OMP_NUM_THREADS="$(nproc)" "$tmpdir/scan" > "$tmpdir/results.json"
jq 'del(.threads)' "$tmpdir/results.json" > "$tmpdir/semantic.json"
jq 'del(.threads)' results/derivative-fibres/RESULTS.json > "$tmpdir/expected.json"
cmp "$tmpdir/semantic.json" "$tmpdir/expected.json"
```

Expected: `cmp` exits zero. Remove the explicit temporary directory after
recording the result.

- [ ] **Step 2: Regenerate the manifest and run every check**

```bash
python3 tools/build_manifest.py
python3 -m unittest discover -s tests -v
python3 verify.py
git diff --check
```

Expected: all tests pass, the root verifier reports `PASS`, and
`git diff --check` prints nothing.

- [ ] **Step 3: Test a fresh clone**

```bash
tmpclone=$(mktemp -d)
git clone . "$tmpclone/release"
cd "$tmpclone/release"
python3 verify.py
python3 -m unittest discover -s tests -v
```

Expected: the fresh clone reports the same passing claims and test count.

- [ ] **Step 4: Check for private or generated material**

```bash
rg -n '/root/\.t3/|BEGIN .*PRIVATE KEY|github_pat_|ghp_|api[_-]?key' . --glob '!.git/**' || true
find . -type d -name __pycache__ -o -type f \( -name '*.pyc' -o -perm -111 \)
git status --short
```

Expected: no private path or secret match, no generated bytecode or compiled
binary, and only intentional executable scripts.

- [ ] **Step 5: Write and commit release notes**

Create `docs/release-notes-v0.1.0.md` with the five result groups, evidence
classes, claim limits, quick verification command, full-scan commands,
dual-license statement, constructive generation command, and no-collision or
attack-cost nonclaim.

```bash
python3 tools/build_manifest.py
git add docs/release-notes-v0.1.0.md MANIFEST.sha256
git commit -m "chore: prepare v0.1.0 release"
git status --short
```

Expected: clean worktree.

## Task 10: Publish the repository, release, and discussion update

**Files:**

- Create: `docs/discussion-1376.md`
- Update: `MANIFEST.sha256`

- [ ] **Step 1: Draft the Layr Labs discussion update**

Create `docs/discussion-1376.md` with a link to the repository and immutable
`v0.1.0` release, one bullet per result group, `python3 verify.py`, the exact
nonclaims, and a request for independent replay, prior-art pointers, and
corrections. Lead with the constructive schedule command and say exactly which
entry, prefix, and coordinates it consumes. Do not include local paths,
leaderboard notes, or novelty claims.

- [ ] **Step 2: Regenerate and verify the final manifest**

```bash
python3 tools/build_manifest.py
python3 verify.py
python3 -m unittest discover -s tests -v
git add docs/discussion-1376.md MANIFEST.sha256
git commit -m "docs: prepare public discussion update"
```

Expected: all checks pass and the worktree is clean.

- [ ] **Step 3: Create and push the public repository**

```bash
gh repo create 0xplemonade/reduced-sha256-exact-structures \
  --public --source . --remote origin --push \
  --description "Exact, replayable structures and scoped obstructions for reduced-round SHA-256"
```

Expected: GitHub returns
`https://github.com/0xplemonade/reduced-sha256-exact-structures` and pushes
`main`.

- [ ] **Step 4: Tag and publish version 0.1.0**

```bash
git tag -a v0.1.0 -m "Reduced SHA-256 exact structures v0.1.0"
git push origin v0.1.0
gh release create v0.1.0 --repo 0xplemonade/reduced-sha256-exact-structures \
  --title "Reduced SHA-256 exact structures v0.1.0" \
  --notes-file docs/release-notes-v0.1.0.md
```

Expected: a public GitHub release page whose source archive points to the tagged
commit.

- [ ] **Step 5: Post the update to discussion #1376**

After replacing the links in `docs/discussion-1376.md` with immutable public
URLs, run:

```bash
gh api graphql \
  -F discussionId='D_kwDOUNbOWs4Aqidh' \
  -F body=@docs/discussion-1376.md \
  -f query='mutation($discussionId:ID!,$body:String!){addDiscussionComment(input:{discussionId:$discussionId,body:$body}){comment{url}}}'
```

Expected: GitHub returns the new comment URL under
`https://github.com/Layr-Labs/hash-smash/discussions/1376`.

- [ ] **Step 6: Verify public links and hand off**

```bash
gh repo view 0xplemonade/reduced-sha256-exact-structures --web=false
gh release view v0.1.0 --repo 0xplemonade/reduced-sha256-exact-structures
git status --short
```

Expected: the repository and release are public, and the local worktree is
clean. Record the repository URL, release URL, tag commit, discussion comment
URL, and final `MANIFEST.sha256` digest in the handoff.
