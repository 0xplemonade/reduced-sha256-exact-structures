# Methods and evidence

## Difference convention

All word differences are right minus left modulo `2^32`. For a word function
`f`, the derivative is

```text
D_f(x, d) = f(x + d) - f(x) mod 2^32.
```

Each result README names the numerical core, support, entry, and round boundary
that define its scope.

## Evidence classes

**Proved** means an all-domain algebraic argument supports the claim. A bounded
verifier checks the implementation but is not the proof.

**Exhaustively counted** means a native program enumerated the complete stated
finite domain. A saved count remains scoped to that domain.

**Constructive witnesses** means the release contains complete inputs that an
independent scalar implementation reconstructs and replays.

**Bounded replay** checks selected examples, identities, or basis vectors. It
detects implementation errors but does not extend a theorem's domain.

## Quick verification

`python3 verify.py` checks the release manifest and runs the five focused
verifiers. The quick path does not invoke Z3, cvc5, or another scientific
solver. It also avoids complete `2^32` scans.

The derivative-fibre quick verifier enumerates the six saved affine spans. That
check covers 1,259,520 words rather than all 32-bit words. The common-W39 quick
verifier replays the saved counts, the algebraic dependencies, and two complete
schedule pairs.

## Complete scans

Repeat the common-W39 enumerations with:

```bash
python3 results/common-w39-obstruction/verify.py --full-scan
```

The verifier compiles `scan_family.c` in a temporary directory and checks both
saved JSON results.

Repeat the derivative-fibre enumeration with:

```bash
cc -O3 -march=native -fopenmp -Wall -Wextra -Werror \
  results/derivative-fibres/scan.c -o /tmp/reduced-sha256-fibre-scan
OMP_NUM_THREADS="$(nproc)" /tmp/reduced-sha256-fibre-scan
```

The scanner enumerates all `2^32` left words. Its semantic JSON output must
match `results/derivative-fibres/RESULTS.json`; the recorded thread count may
differ.

## Integrity

`MANIFEST.sha256` covers every release file except itself. The root verifier
checks the manifest before it runs a semantic verifier. `docs/provenance.md`
binds every imported file to its source packet and source SHA-256 digest.
