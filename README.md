# Reduced SHA-256 exact structures

This repository collects exact, replayable results from a reduced-round
SHA-256 research campaign. It focuses on constructive schedule coordinates,
conditional message modification, finite extension obstructions, derivative
fibres, and local carry characteristics.

The root verifier uses no SAT or SMT solver. Each result links to its proof,
saved data, and focused verifier.

## What this repository contains

The repository separates algebraic proofs, complete finite counts, constructive
witnesses, and bounded implementation checks. [Methods and evidence](docs/methods.md)
defines those labels. [The claim catalog](claims.json) provides the command and
evidence class for each published result.

## What this repository does not claim

This release does not claim:

- a result on full SHA-256;
- a new collision or semi-free-start collision;
- an improved attack exponent or measured search speedup;
- independent recombination of the left and right lanes;
- literature novelty for any result.

The [prior-art review](docs/prior-art.md) records the search scope and the
closest primary sources.

## Generate a valid paired schedule

Run the constructive example:

```bash
python3 results/schedule-constructions/generate.py --example 0
```

The command reconstructs two 16-word message blocks from a common entry, a
ten-word prefix, `W22`, `W14`, `W23`, and three chosen left outputs. It verifies
the sparse support `{6, 7, 9, 14, 22, 23, 37}` and the pair digest
`b16fec39f5e4ae2041b91cd8f2a358417163b0ed098f1d2c30212ffba642d80f`.
The coordinate input does not contain the final messages. The output is a valid
paired message schedule, not a collision.

## Results

| Result | Evidence | Scope | Reproduce |
|---|---|---|---|
| [Constructive schedule coordinates and state-preserving fibres](results/schedule-constructions/README.md) | Proved, with bounded replay | Two retained sparse schedule families and their S13 and S14 fibres | `cd results/schedule-constructions && python3 verify.py` |
| [Conditional modification through `P(V),Q(V)`](results/conditional-modification/README.md) | Proved local identity | One admitted context at a time | `cd results/conditional-modification && python3 verify.py` |
| [Common-W39 extension obstruction](results/common-w39-obstruction/README.md) | Exhaustively counted | Two fixed numerical cores and supports | `cd results/common-w39-obstruction && python3 verify.py` |
| [Table 23 W24 derivative fibres](results/derivative-fibres/README.md) | Exhaustively counted and span-verified | One fixed small-sigma0 derivative equation | `cd results/derivative-fibres && python3 verify.py` |
| [Carry-transfer and carry-reset characteristics](results/carry-characteristics/README.md) | Proved local identity with constructive witnesses | Six retained r40 schedule pairs | `cd results/carry-characteristics && python3 verify.py` |

## Verify the release

Run every quick check:

```bash
python3 verify.py
```

The command verifies `MANIFEST.sha256`, runs all five focused verifiers, and
prints one JSON summary. It performs zero scientific solver queries. The two
complete 32-bit scans are opt-in because the saved results have compact quick
checks. See [Methods and evidence](docs/methods.md) for the full-scan commands.

## Reuse and citation

Original source code is licensed under Apache-2.0. Original documentation,
proofs, and datasets are licensed under CC BY 4.0. See [CITATION.cff](CITATION.cff),
[third-party material](THIRD_PARTY.md), and [provenance](docs/provenance.md)
before reusing an artifact.

## Relationship to sha256-structural-data

The earlier [`sha256-structural-data` release](https://github.com/0xplemonade/sha256-structural-data/releases/tag/v0.1.0)
publishes S16 roots, sparse schedule witnesses, S24 counterexamples, and honest
solver records. This repository contains later exact parameterizations, finite
counts, and scoped obstructions. It links to the earlier release instead of
duplicating that archive.

## Open questions

- Can a nonzero `Delta W39` be cancelled by the final r40 state transition?
- Does a justified bit or carry projection give a useful separator over a
  conditional S14 fibre?
- Can the coupled `P(V),Q(V)` target admit an inexpensive constructive preimage
  rule in an actual terminal context?
- Do changed numerical cores or changed support avoid the two common-W39
  obstructions?
