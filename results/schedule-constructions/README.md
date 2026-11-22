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
