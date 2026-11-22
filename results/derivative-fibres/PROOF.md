# Table 23 W24 derivative fibre

Date: 2026-11-10

This artifact counts the exact fibre

```text
F = {x in Z/2^32 : sigma0(x + 03010000) - sigma0(x) = c05a1dc0}.
```

Differences use right minus left modulo `2^32`. The target is the `Delta W39`
value of the independently replayed Table 23 pair when `Delta W23`, `Delta W32`,
and `Delta W37` are zero.

## Result

The complete fibre has

```text
|F| = 1,259,520 = 615 * 2^11,
log2(|F|) = 20.2644426002.
```

Its density among all 32-bit words is about `2^-11.7355573998`.

The fibre is a disjoint union of six affine GF(2) components. Each component is
identified by the XOR mask `x xor (x + 03010000)`.

| XOR mask | Count | Affine dimension |
|---|---:|---:|
| `03010000` | `1,048,576` | 20 |
| `03030000` | `131,072` | 17 |
| `07010000` | `65,536` | 16 |
| `07030000` | `8,192` | 13 |
| `0f030000` | `2,048` | 11 |
| `1f010000` | `4,096` | 12 |

`RESULTS.json` records a canonical representative and a reduced GF(2) basis for
each component.

The public left word is

```text
W24_L = cc584832,
W24_R = cf594832.
```

It belongs to the first component, whose XOR mask is `03010000` and whose size
is exactly `2^20`. This is the no-carry component identified in the earlier
algebraic audit.

## Method

`scan.c` enumerates every 32-bit left word. For each solution it groups the word
by its addition XOR mask and builds the affine span of the words in that group.
It then reduces each basis to a deterministic form.

The program verifies each component by enumerating every word in its affine span.
For each word it checks both the addition XOR mask and the modular sigma derivative.
The verified affine span size must equal the exhaustive count for that component.

The scan was run once with 14 OpenMP threads and once with one thread. The semantic
JSON outputs were identical. Only the recorded thread count differed.

Reproduce with:

```text
gcc -O3 -march=native -fopenmp -Wall -Wextra -Werror scan.c -o scan
OMP_NUM_THREADS=$(nproc) ./scan > RESULTS.json
OMP_NUM_THREADS=1 ./scan > RESULTS.single.json
```

## Scope

This fibre describes where the fixed derivative `c05a1dc0` occurs. It does not
make `W39` common. Under the fixed Table 23 support,

```text
Delta W39 = D_sigma0(W24, 03010000),
```

and injectivity of `sigma0` keeps this value nonzero for every member of the
fibre. A common `W39` needs another active schedule term to cancel it.

For an r40-only final-round merge, the derivative sets the required entering
state difference. The component count does not establish that the earlier rounds
can reach that state, a success probability, or an attack cost.
