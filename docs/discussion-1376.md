## Follow-up release: exact schedule constructions, fibres, and scoped obstructions

I have published a second compact research release:

- Repository: https://github.com/0xplemonade/reduced-sha256-exact-structures
- Stable release: https://github.com/0xplemonade/reduced-sha256-exact-structures/releases/tag/v0.1.0

The most directly reusable result is a constructive schedule chart:

```bash
python3 results/schedule-constructions/generate.py --example 0
```

The example consumes a common entry, a ten-word prefix, `W22`, `W14`, `W23`,
and three chosen left outputs. It reconstructs both 16-word message blocks and
verifies sparse support `{6,7,9,14,22,23,37}` plus pair digest
`b16fec39f5e4ae2041b91cd8f2a358417163b0ed098f1d2c30212ffba642d80f`.
The coordinate input does not contain the final messages.

The release contains five result groups:

- An exact raw-message coordinate chart with S13-preserving and conditional
  S14 fibres.
- A coupled one-parameter `P(V),Q(V)` interface for conditional message
  modification.
- Complete zero-intersection counts that exclude common W39 for two retained
  numerical cores and supports.
- A complete 1,259,520-word small-sigma0 derivative fibre, decomposed into six
  affine GF(2) components.
- A local carry-transfer and carry-reset identity with six complete r40
  schedule witnesses replayed from the standard IV.

Run the non-solving release verifier with:

```bash
python3 verify.py
```

It checks the manifest and all five result groups. Complete 32-bit scanners are
included as opt-in checks.

This release does not claim a collision, a result on full SHA-256, an improved
attack exponent, independent lane freedom, or literature novelty. The
prior-art note records the closest primary sources and uses conservative claim
wording.

Independent replays, prior-art pointers, corrections, and derived
constructions are welcome.
