# Reconciliation with the carry-class parity filter

The separate `r37-r38-core-clarifications-v1` calculation establishes a
correct necessary condition for common `W39`: the induced `Delta W37` must
be odd. It also corrects an overstatement in the earlier public-r37
extension report: the map

```text
W22_L -> D_s0(W22_L, Delta W22)
```

is nonconstant but not injective. Distinct admissible `W22_L` values can
produce the same `Delta W37`.

Those results are consistent with, but weaker than, the complete finite
audit in this directory. In the shifted-public-r38 slice with public `W9`,
the parity filter leaves `2^20` admissible `W22` values. The full audit then
requires the actual derivative equation

```text
D_s1(W37, Delta W37) = 00000004
```

and grants `W37` every possible 32-bit absolute value. None of the surviving
`W22` values admits such a `W37`.

The complete counts are:

| Arm | Some `W9` satisfies row 24 | Some arbitrary `W37` satisfies row 39 | Both |
|---|---:|---:|---:|
| Shifted public r38 | 344,457,216 | 64 | **0** |
| Public r37 | 540,494,592 | 4,432 | **0** |

Therefore varying `W9`, `W22`, or the common coordinates cannot produce a
common-`W39` member while the respective public numerical differences are
retained. The straightforward r39-then-r40 extension is closed for both
exact numerical cores.

This does not exclude an r40 path with nonzero `Delta W39` and final-round
state cancellation, or a construction that changes the core differences or
support.
