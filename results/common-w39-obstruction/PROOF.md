# Common-W39 compatibility of the compensated schedule families

## Verdict

The verified shifted-public-r38 compensated family cannot be extended to common W39 while preserving its core differences, row 24, and common W38.

This is a schedule impossibility result. It says nothing about compression-state reachability because no state or common-CV search is needed.

The exact count is zero. Among all 2^32 possible left W22 values:

| Test on W22 | Count |
|---|---:|
| Some W9 satisfies row 24 | 344,457,216 |
| Some 32-bit W37 can make W39 common | 64 |
| Both | **0** |

The 64-count test grants W37 every 32-bit value. Actual forward-schedule restrictions on W37 can only remove candidates, so they cannot change the zero intersection.

## Dependencies through W39

Differences are right minus left modulo 2^32. Write `D_f(x,d)=f(x+d)-f(x)`.

The fixed shifted core is:

```
dW6  = 31de0240    dW7  = fffffffc
dW9  = 00028000    dW14 = 00000004
dW22 = 07ff0000    dW23 = fffffffc
```

The rows that matter here are exact:

```
row 24:  D_s1(W22,07ff0000) + D_s0(W9,00028000) = 0
row 37:  dW37 = D_s0(W22,07ff0000)
row 38:  D_s0(W23,fffffffc) + 07ff0000 = 0
row 39:  dW39 = D_s1(W37,dW37) + fffffffc
```

W24 and W32 are common, so common W39 is equivalent to:

```
D_s1(W37,dW37) = 00000004.
```

This keeps the W9/W22 coupling in row 24. It also keeps the W23 condition that makes W38 common.

## The supplied witness

Independent scalar expansion reproduces support `{6,7,9,14,22,23,37}` through W38 and common `W38 = 4e4a7351`.

For that witness:

```
W22_L                  = 0016c400
D_s1(W22,07ff0000)     = a001fac1
D_s0(W9,00028000)      = 5ffe053f
row-24 sum              = 00000000
dW37                    = bf0f9c00
W37_L                   = 22d8e3a4
D_s1(W37,bf0f9c00)     = c27073c7
dW39                    = c27073c3
```

Thus the supplied witness fails W39 exactly as stated. A separate exhaustive scan of all W37 values finds no root of `D_s1(W37,bf0f9c00)=4`.

## Exact zero-count proof

Define two finite images:

```
A = { D_s0(x,00028000) : x in Z/(2^32) }
E = { s1_inverse(s1(x)+4)-x : x in Z/(2^32) }
```

The small sigma1 map has GF(2) rank 32, so its inverse exists. By construction:

```
d in E  iff  there is an x with D_s1(x,d)=4.
```

For every W22, the scanner computes:

```
q = D_s1(W22,07ff0000)
d = D_s0(W22,07ff0000)
```

Row 24 has some W9 solution exactly when `-q` belongs to A. Common W39 has some W37 solution exactly when `d` belongs to E.

`scan_family.c` enumerates each of the three 2^32-word domains once. It gets:

```
|A|                              = 1,770,752
|E|                              = 2,064,189
W22 with -q in A                 = 344,457,216
W22 with d in E                  = 64
W22 satisfying both              = 0
```

This is a complete count, not sampling. A separate bit-vector formulation of the two reduced equations also returns UNSAT.

## Is W37 freely translatable?

W37 moves when common earlier words move, but it is not an independent schedule coordinate. At a fixed active left core `(W6,W7,W9,W14,W22,W23)`, every schedule pair is parameterized by ten arbitrary common words:

```
(W17,W18,W19,W20,W21,W24,W25,W26,W27,W28).
```

The remaining W6..W21 window is reconstructed exactly:

```
W8  = W24 - s1(W22) - W17 - s0(W9)
W10 = s0_inverse(W25 - s1(W23) - W18 - W9)
W11 = s0_inverse(W26 - s1(W24) - W19 - W10)
W12 = s0_inverse(W27 - s1(W25) - W20 - W11)
W13 = s0_inverse(W28 - s1(W26) - W21 - W12)
W15 = W22 - s1(W20) - s0(W7) - W6
W16 = W23 - s1(W21) - s0(W8) - W7
```

Reverse expansion then gives W0..W5. Forward expansion gives W29 onward, including:

```
W37 = s1(W35) + W30 + s0(W22) + W21.
```

So the fixed-active-core family has exactly `2^320` schedule pairs, and W37 is the image of those ten common coordinates. The report does not assume that this image is all 2^32 words. Two explicit schedules in `RESULT.json` keep the same active absolute core but have different left W37 values, `22d8e3a4` and `b51fb3d0`. W37 is movable, but a direct free-translation claim is not licensed by the recurrence.

The impossibility proof is stronger than needed on this point. It tests all 2^32 possible W37 values for every derived dW37 and still gets zero compatible W22 values.

## Analogous public-r37 arm

For the public-r37 compensated family, `dW23 = ffffffff`, so common W39 requires:

```
D_s1(W37,dW37) = 00000001.
```

Keeping its actual row 24,

```
D_s1(W22,fdffc000) + D_s0(W9,0000a000) + d0007c70 = 0,
```

the same exact scan gives:

| Test on W22 | Count |
|---|---:|
| Some W9 satisfies row 24 | 540,494,592 |
| Some 32-bit W37 can make W39 common | 4,432 |
| Both | **0** |

Thus that schedule family also has no common-W39 member.

## Reproduction

Fast verification, including independent forward expansion and reduced-equation UNSAT checks when z3py is present:

```bash
python3 -I -B verify.py
```

Full finite replay, which rebuilds the C scanner in a temporary directory and reruns both exact counts:

```bash
python3 -I -B verify.py --full-scan
```

The two final scans used about 69 core-seconds in total. All exploratory and final work remained below the requested five core-minute budget. No network, GPU, Yukon action, compression-state search, common-CV search, or repository mutation was used.
