# Prior-art review

Review date: 2026-11-22

## Scope

This review searched IACR ePrint, IACR conference records, Springer proceedings,
arXiv, and the references of the closest papers. Search terms combined
`SHA-256` with `message schedule`, `message modification`, `neutral bits`,
`state-preserving`, `affine fibre`, `modular derivative`, `carry`, `SAT`, and
`semi-free-start collision`.

The review supports conservative wording. It is not a proof that no earlier
publication contains an equivalent construction.

## Closest primary sources

- Mendel, Pramstaller, Rechberger, and Rijmen describe collision-producing
  characteristics, message modification, and carry extension for step-reduced
  SHA-256 in [Analysis of Step-Reduced SHA-256](https://eprint.iacr.org/2008/130.pdf).
- Indesteege, Mendel, Preneel, and Rechberger give collision and near-collision
  methods for step-reduced SHA-256 in [Collisions and Other Non-random
  Properties for Step-Reduced SHA-256](https://eprint.iacr.org/2008/131.pdf).
- Mendel, Nad, and Schläffer construct longer local collisions and a 38-step
  semi-free-start collision in [Improving Local Collisions: New Attacks on
  Reduced SHA-256](https://eprint.iacr.org/2015/350.pdf).
- Li, Isobe, and Wang report a 39-step semi-free-start pair and SAT or SMT
  message modification in [New Records in Collision Attacks on
  SHA-2](https://eprint.iacr.org/2024/349.pdf).
- Alamgir, Nejati, and Bright combine SAT with programmatic algebraic
  propagation in [SHA-256 Collision Attack with Programmatic
  SAT](https://arxiv.org/abs/2406.20072).
- Paul and Preneel study systems of differential equations that mix modular
  addition and XOR in [Solving Systems of Differential Equations of Addition
  and Cryptanalysis of the Helix Cipher](https://eprint.iacr.org/2004/294.pdf).

## Result-by-result assessment

### Constructive schedule coordinates and state-preserving fibres

Prior work establishes message modification, neutral-bit methods, sparse local
collisions, and automated schedule or state constraints. The reviewed sources
do not present the same raw-message-to-coordinate bijection, the exact S13
preservation statement, or the reported S14 fibre averages for these two
numerical cores.

**Wording decision:** potentially distinct, with no literature novelty claim.

### Conditional modification through P(V) and Q(V)

Message modification in SHA-256 is established prior art. The 2008 analysis
solves early state conditions through message words and describes how to repair
contradicting conditions. The reviewed sources do not use the same normalized
one-parameter `P(V),Q(V)` representation for the immediate differential in the
declared schedule chart.

**Wording decision:** potentially distinct normalization of a known technique,
with no literature novelty claim.

### Common-W39 extension obstruction

Published work studies local-collision supports, schedule conditions, and
conforming message pairs. The reviewed sources do not report the same complete
intersection count between the row-24 derivative image and the terminal
small-sigma1 derivative image for either retained numerical core.

**Wording decision:** potentially distinct scoped obstruction, with no
literature novelty claim.

### Table 23 W24 derivative fibres

The differential-equation literature covers modular addition and XOR, and the
SHA-256 literature uses modular derivatives of the small sigma functions. The
reviewed sources do not report the exact 1,259,520-word fibre or its six affine
GF(2) components for this equation.

**Wording decision:** potentially distinct finite decomposition, with no
literature novelty claim.

### Carry-transfer and carry-reset characteristics

Carry extension and deliberate carry cancellation are explicit in the 2008
SHA-256 analysis. The identity `beta = sigma + kappa - 2*kappa_next` follows
from binary addition. The six complete schedules are useful constructive
examples, but the underlying carry technique is established prior art.

**Wording decision:** no novelty claim; publish as replayable evidence and
examples.

## Publication rule

Version 0.1 uses “exact result from this project.” It does not use “new,”
“first,” or “novel” for a mathematical claim. A later paper can sharpen a
novelty statement only after a broader expert review.
