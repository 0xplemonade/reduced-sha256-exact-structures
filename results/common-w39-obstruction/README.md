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
