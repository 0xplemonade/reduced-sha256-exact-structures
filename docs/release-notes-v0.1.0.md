# Reduced SHA-256 exact structures v0.1.0

Version 0.1.0 publishes five exact, replayable result groups from a
reduced-round SHA-256 research campaign.

## Included results

- **Constructive schedule coordinates and state-preserving fibres.** An exact
  coordinate chart generates valid paired message schedules and describes S13
  and conditional S14 fibres. Evidence class: proved, with bounded replay.
- **Conditional modification through `P(V),Q(V)`.** Two coupled functions of
  one parameter describe the immediate next-state target in an admitted
  context. Evidence class: proved local identity.
- **Common-W39 extension obstruction.** Complete 32-bit scans give an empty
  intersection for each of two retained numerical cores. Evidence class:
  exhaustively counted.
- **Table 23 W24 derivative fibres.** One small-sigma0 derivative equation has
  1,259,520 solutions in six affine GF(2) components. Evidence class:
  exhaustively counted and affine-span verified.
- **Carry-transfer and carry-reset characteristics.** A local carry identity
  and six complete r40 schedule witnesses replay from the standard IV.
  Evidence class: proved identity with constructive witnesses.

## Construct a paired schedule

```bash
python3 results/schedule-constructions/generate.py --example 0
```

The command builds both message blocks from coordinates and verifies their
sparse support and pair digest. The output is not a collision.

## Verify

```bash
python3 verify.py
```

The quick verifier checks the release manifest and all five result groups. It
runs no scientific SAT or SMT query.

Repeat the common-W39 full scans with:

```bash
python3 results/common-w39-obstruction/verify.py --full-scan
```

Compile `results/derivative-fibres/scan.c` with OpenMP to repeat the complete
derivative-fibre scan. [Methods and evidence](methods.md) gives the command.

## Claim limits

This release does not claim a result on full SHA-256, a new collision, an
improved attack exponent, independent lane freedom, or literature novelty.
Every result remains scoped to the entries, numerical cores, supports, and
finite domains stated in its README.

## Licenses

Original code is licensed under Apache-2.0. Original documentation, proofs, and
datasets are licensed under CC BY 4.0. See `THIRD_PARTY.md` and
`docs/provenance.md` before reusing an artifact.
