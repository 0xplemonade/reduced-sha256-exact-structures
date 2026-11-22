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
