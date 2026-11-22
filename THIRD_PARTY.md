# Third-party material

Original source code in this repository is licensed under Apache-2.0.
Original documentation, proofs, and datasets are licensed under CC BY 4.0.

Do not publish a copied file unless its reuse terms are known. A source hash
and a citation do not replace a license.

The release uses public reduced-round SHA-256 examples as attributed numerical
inputs. `docs/provenance.md` identifies each example and the exact result that
uses it. No paper PDF, competitor source file, or benchmark repository file is
redistributed.

## Public numerical fixtures

Some message pairs and differential parameters were previously published in
[`sha256-structural-data` v0.1.0](https://github.com/0xplemonade/sha256-structural-data/releases/tag/v0.1.0)
and [Layr Labs HashSmash discussion #1376](https://github.com/Layr-Labs/hash-smash/discussions/1376).
This repository republishes derived numerical fixtures and attributes their
public predecessor. The project does not copy third-party implementation code.

## Cited research

The release cites the following primary sources without redistributing them:

- [Analysis of Step-Reduced SHA-256](https://eprint.iacr.org/2008/130.pdf),
  Mendel, Pramstaller, Rechberger, and Rijmen.
- [Collisions and Other Non-random Properties for Step-Reduced
  SHA-256](https://eprint.iacr.org/2008/131.pdf), Indesteege, Mendel, Preneel,
  and Rechberger.
- [Improving Local Collisions: New Attacks on Reduced
  SHA-256](https://eprint.iacr.org/2015/350.pdf), Mendel, Nad, and Schläffer.
- [New Records in Collision Attacks on SHA-2](https://eprint.iacr.org/2024/349.pdf),
  Li, Isobe, and Wang.
- [SHA-256 Collision Attack with Programmatic SAT](https://arxiv.org/abs/2406.20072),
  Alamgir, Nejati, and Bright.
- [Solving Systems of Differential Equations of Addition and Cryptanalysis of
  the Helix Cipher](https://eprint.iacr.org/2004/294.pdf), Paul and Preneel.
