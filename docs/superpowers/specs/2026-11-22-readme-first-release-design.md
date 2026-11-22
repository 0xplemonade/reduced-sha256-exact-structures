# README-first release design

Date: 2026-11-22

Repository: `0xplemonade/reduced-sha256-exact-structures`

Status: Approved direction, pending review of this specification

## Goal

Create a small public repository for the exact reduced-round SHA-256 results
that emerged from the recent research campaign. The repository must help another
researcher understand each claim, reproduce it, and reuse the supporting code or
data without reading the original scratch workspace.

The initial release is a research artifact, not a paper. Its root `README.md` is
the main explanation. Each result has a short local README, the minimum evidence
needed to support the claim, and a focused verifier.

## Audience

The primary audience is researchers who work on reduced-round SHA-256,
differential cryptanalysis, SAT or SMT encodings, or exact finite searches.
Readers may know SHA-256 but should not need prior knowledge of the local packet
names, Yukon runs, or the history of this workspace.

## Claim policy

The repository must separate four evidence classes:

- **Proved:** an all-domain algebraic argument supports the claim.
- **Exhaustively counted:** a complete finite enumeration supports the claim.
- **Scoped finite result:** a complete search supports the claim only inside a
  declared family or grammar.
- **Experimental record:** a run reports what happened but proves no broader
  mathematical statement.

Every claim in the root README must name one class and link to its proof,
verifier, and saved result. A verifier confirms that the published artifact
matches the stated calculation. A verifier does not turn a scoped result into a
global theorem.

The initial release must not claim literature novelty. A targeted prior-art
review must finish before the README uses words such as "new", "first", or
"novel". Until then, the README describes the results as exact results from this
project.

## Version 0.1 scope

Version 0.1 contains five result groups.

### Constructive schedule coordinates and state-preserving fibres

Package the exact coordinate map between the retained sparse schedule family
and its message pairs. Include the S13-preserving chart, the conditional S14
fibre, and the domain-equivalence proof. Expose the construction as a small
command that regenerates a saved valid pair from its entry, prefix, fibre
coordinates, and three chosen left outputs.

Source packets:

- `state_coordinate_s13_chart`
- `sha256_research_synthesis`
- `r39_s24_formulation_comparison/DOMAIN_EQUIVALENCE.md`

The public text must distinguish a coordinate change from added freedom. It
must also state that a large fibre does not establish endpoint success or an
attack cost. The construction output must be called a paired message schedule
or a boundary-preserving construction, never a collision.

### Conditional message modification

Package the one-parameter `P(V), Q(V)` interface for the next state difference
inside a fixed admitted context. Include the normalized local map and the exact
target equations.

Source packets:

- `sha256_research_synthesis`
- `sha256_paper_transfer`

The public text must state that `P` and `Q` are coupled functions of one
parameter. It must not price them as independent trials or claim a cheap global
inverse.

### Common-W39 extension obstruction

Package the exact zero-intersection results for the shifted-public-r38 and
public-r37 numerical cores. Include the finite-image construction, counts,
independent checks, and reconciliation with the weaker parity filter.

Source packet:

- `r40_common_w39_compat`

The public text must scope the impossibility to the retained numerical
differences and support. It must state that nonzero `Delta W39` final-round
cancellation and changed cores remain open.

### Derivative fibre decomposition

Package the complete fibre count for the Table 23 `W24` derivative and its six
affine GF(2) components. Include the canonical representative and reduced basis
for each component.

Source packet:

- `r40_table23_w39_fibre`

The public text must state that membership in this derivative fibre does not
make `W39` common and does not prove that the compression state can reach a
required boundary.

### Carry-transfer characteristics

Package the carry-transfer and carry-reset identities with the retained,
independently replayed r40 witnesses. Include only results whose full schedules
and state trajectories can be reconstructed from saved coordinates.

Source packets:

- `r40_multibit_carry_characteristic`
- `r40_state_first_differential_search`
- `r40_state_characteristic_search`

The public text must distinguish an exact local characteristic from a complete
collision path or a measured attack improvement.

## Excluded material

Version 0.1 excludes the following material:

- Raw scratch directories and duplicated Yukon worktrees.
- Leaderboard snapshots and private submission notes.
- Monolithic Z3 and cvc5 timeout transcripts.
- The invalid A/B/C comparison as a headline result.
- Generated binaries, caches, temporary files, and absolute local paths.
- Third-party files whose license or provenance is not recorded.
- Statistical or complexity claims that lack a declared baseline.

The release may mention failed solver approaches in one short limitations
section. It must not publish large logs that do not help reproduction.

## Repository structure

The initial repository uses this structure:

```text
README.md
results/
  schedule-constructions/
  conditional-modification/
  common-w39-obstruction/
  derivative-fibres/
  carry-characteristics/
verify.py
MANIFEST.sha256
CITATION.cff
LICENSE
LICENSE-DOCS
THIRD_PARTY.md
docs/
  provenance.md
  methods.md
  superpowers/specs/
```

Each directory under `results/` contains:

- `README.md`, which states the claim and its limits.
- The smallest source program that regenerates or checks the result.
- A deterministic saved result in JSON or another documented text format.
- A focused verifier that exits nonzero on a mismatch.
- `SOURCE_BINDINGS.json` when the result depends on an external fixture or
  copied source.

`results/schedule-constructions/` also contains `generate.py`. Running
`python3 generate.py --example 0` reconstructs the first saved pair from its
coordinates and prints both 16-word message blocks, their sparse support, and
their pair digest as JSON.

Do not copy a source packet as a directory without review. Select the minimal
files, remove workspace-specific wrappers, and preserve the mathematical
meaning and source hashes.

## Root README

The root README is the primary publication. It follows this order:

1. A two-paragraph summary of the repository.
2. A prominent statement of what the repository does not claim.
3. A result table with evidence class, scope, and reproduction link.
4. A "Generate a valid paired schedule" example using the constructive chart.
5. Plain-language explanations of the five result groups.
6. A quick verification command and expected output.
7. Reuse guidance for code, data, and citations.
8. Provenance and relationship to `sha256-structural-data`.
9. Open questions that follow from the exact results.

Use equations only when the equation is the result or defines its scope. Define
each local symbol near its first use. Avoid packet names in the explanatory
text. Put packet names and source hashes in `docs/provenance.md`.

## Verification contract

The default command is:

```bash
python3 verify.py
```

The default verifier must:

- Use only Python's standard library, except when it invokes a documented C
  compiler for a compact checker.
- Check the release manifest.
- Run each focused verifier in deterministic quick mode.
- Replay every published witness.
- Check saved counts and proof certificates without repeating a `2^32` scan.
- Print one JSON summary and exit zero only when every required check passes.

Each result README documents its complete scan command. The root verifier may
also expose `python3 verify.py --full-scan` as a dispatcher for those commands.
The root README must state their expected time, CPU use, memory use, and
compiler requirements. Quick verification must not silently launch a long
search.

The root verifier must not run a scientific solver query. SAT or SMT files may
be included as supporting material, but they are not part of the default trust
path for version 0.1.

## Licensing

Use Apache-2.0 for original source code. Store the license text in `LICENSE`.

Use CC BY 4.0 for original documentation, proofs, and datasets. Store the
license text in `LICENSE-DOCS` and state the file mapping in the root README.

Record every third-party input in `THIRD_PARTY.md`. Preserve its original
license and attribution. Do not publish a third-party file when its reuse terms
are unclear. A source hash and citation do not replace a license.

## Provenance and attribution

`docs/provenance.md` maps every public claim to:

- The original local packet and file.
- The full SHA-256 digest of each imported source file.
- The generation or verification command.
- The related prior public release or HashSmash submission.
- Any material dependency on another researcher's work.

The new repository links to `0xplemonade/sha256-structural-data` but does not
duplicate that release. When a new result extends a result from the old
repository, the README names the dependency and links to the stable release.

## Publication sequence

Publish in this order:

1. Assemble the repository locally from reviewed source files.
2. Run the quick verifier from a clean checkout.
3. Run every documented full scan needed for the release and save its semantic
   result.
4. Perform a targeted prior-art review for each potential novelty claim.
5. Review licenses, provenance, absolute paths, secrets, and generated files.
6. Create the public GitHub repository.
7. Tag `v0.1.0` and attach a deterministic source archive.
8. Add a substantial update to Layr Labs HashSmash discussion #1376.
9. Create a separate discussion only if a later paper or sustained topic needs
   its own thread.

Do not post a discussion before the stable release exists. Public discussion
text must link to immutable release artifacts rather than the moving `main`
branch alone.

## Acceptance criteria

Version 0.1 is ready when all of these statements are true:

- A fresh clone passes `python3 verify.py`.
- Every README claim links to an evidence file and states its scope.
- Every saved witness replays with an independent implementation.
- The documented construction command regenerates its saved message pair and
  pair digest from coordinates rather than reading the final pair as output.
- Every exhaustive count has either a replayable full scan or a compact proof
  certificate and a documented full-scan command.
- The quick verifier runs no long search and no SAT or SMT query.
- The repository contains no absolute workspace paths, credentials, caches,
  generated binaries, or duplicate worktrees.
- `MANIFEST.sha256` covers every release file except itself.
- `CITATION.cff` identifies the release, author, repository, and license split.
- `THIRD_PARTY.md` records every imported external artifact and its license.
- The prior-art review supports every novelty phrase, or the README omits that
  phrase.
- The GitHub release and discussion text use the same claims and limitations as
  the repository.

## Deferred work

A formal paper, DOI archive, benchmark submission, and solver campaign are not
part of version 0.1. Consider them only after researchers can reproduce the
README claims and the prior-art review identifies a defensible contribution.
