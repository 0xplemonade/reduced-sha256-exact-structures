# Provenance

Every path in this document is relative to the private assembly workspace or to
this public repository. No public verifier depends on a private path.

## Imported source files

### Constructive schedule coordinates

Source packet: `state_coordinate_s13_chart`.

| Public file | Source file | Source SHA-256 | Import action |
|---|---|---|---|
| `INPUTS.json` | `INPUTS.json` | `8683145011148b0d91431e71eebb4aecc60939830d3c28bb6b00e522c60b8540` | Unchanged copy |
| `PROOF.md` | `PROOF.md` | `69f5b6ab6156bf68e9b5ce69ecbf17b0fcfd71d10a00d62769bcbd703fe2ebef` | Unchanged copy |
| `RESULTS.json` | `RESULTS.json` | `e3740cabb67784deefc13481fbfbe97d82f7aecaf6d482139eef9f3d975003ae` | Unchanged copy |
| `SOURCE_BINDINGS.json` | `SOURCE_BINDINGS.json` | `243c9f6e2c97780287924f0c5c799aac44cce61ebbbb517258bd6bdc4322e9ac` | Unchanged copy |
| `chart.py` | `chart.py` | `9690b2ab2d5d1c60ed9f83eaad3e2397168fe9b93c584db880aa3d3bf79c540c` | Unchanged copy |
| `fibre_algebra.py` | `fibre_algebra.py` | `56144e0b73d7ac0c55ed411d176719757aa3bfdae24791ec58b04b62d284d7ac` | Unchanged copy |
| `reference.py` | `reference.py` | `17284e7c90e5d82eefbdb8e551b9477edc4760724ef920a1155a12953f94e36a` | Unchanged copy |
| `state_coordinates.py` | `state_coordinates.py` | `f8d1d09ce1c9ce70fbf9e7c181e4553238073e2089a0ce47d49fa56247985760` | Unchanged copy |
| `verify.py` | `verify.py` | `39d7ad1efd1b36412daa10ed2b00d6228fe3ccd7182cf3aaf4149bb8ec25c295` | Unchanged copy |

`EXAMPLE.json`, `generate.py`, and `README.md` are release-specific files. The
coordinate-only example is derived from the first saved replay in
`RESULTS.json`.

### Conditional message modification

Source packet: `sha256_paper_transfer`.

| Public file | Source file | Source SHA-256 | Import action |
|---|---|---|---|
| `PROOF.md` | `REPORT.md` | `e626067ef0a2693e4b5b4e94faff022b14c65590bbfbd5bacde3653e1d585cee` | Renamed, content unchanged |
| `INPUTS.json` | `checks/INPUTS.json` | `bacb01815ae5e694b89662ed21cf6bbd1a0ab6507b18eb02781a761f10279a37` | Unchanged copy |
| `RESULTS.json` | `checks/RESULTS.json` | `8720c2e1905b59b8720d9c35833ea04bf5a771e1a6511ac1bc66bf28aca32f5a` | Unchanged copy |
| `SOURCE_BINDINGS.json` | `checks/SOURCE_BINDINGS.json` | `cad8818d14a3a3d6f01bded732c858a3afa7db81ac62a140f2c600a72a83c996` | Unchanged copy |
| `normal_form.py` | `checks/normal_form.py` | `6cfb2ef1899b42a2cc5903adc243d17a25055582990d4d17fe0c39a13ca973c6` | Unchanged copy |
| `reference.py` | `checks/reference.py` | `17284e7c90e5d82eefbdb8e551b9477edc4760724ef920a1155a12953f94e36a` | Unchanged copy |
| `verify.py` | `checks/verify.py` | `7d68047ac11aefbf834d805e80f89a4b6fa6d01eb85a8713cc5145f82670cf4c` | Unchanged copy |

### Common-W39 obstruction

Source packet: `r40_common_w39_compat`.

| Public file | Source file | Source SHA-256 | Import action |
|---|---|---|---|
| `PROOF.md` | `REPORT.md` | `b0eb15198dd720c382d8dd2c02e08280413ea393fdf76c7fe182c8b17902f0e5` | Renamed, content unchanged |
| `RECONCILIATION.md` | `RECONCILIATION.md` | `74d3b689bd20d031ad98ed0c07b781a8904cc31705e09808d230262e606aad96` | Unchanged copy |
| `RESULT.json` | `RESULT.json` | `c4850877030ea89dc9c6199118678d767d8e1dcaca73f2cfabe8b16842940668` | Unchanged copy |
| `SCAN_R37.json` | `SCAN_R37.json` | `472075c361f38b4714453a5631e7f1dc5947bdbbcdb798b4d909bbd628e1f4a7` | Unchanged copy |
| `SCAN_R38.json` | `SCAN_R38.json` | `16c96619b3b047cc48a77c89f45fd16da052f3c8dc58d66e63bda760c6f33b87` | Unchanged copy |
| `scan_family.c` | `scan_family.c` | `4bfee41f98575b5928ffb8f2899c0e1caa554c24b6658d84b0943dbc5dcbf9aa` | Unchanged copy |
| `verify.py` | `verify.py` | `fdce64b77a6272882f0da1f8ac871c44653deb712bb45359e2ce2ec36a0afbe9` | Removed private input paths and optional Z3 query |

### Derivative fibres

Source packet: `r40_table23_w39_fibre`.

| Public file | Source file | Source SHA-256 | Import action |
|---|---|---|---|
| `PROOF.md` | `REPORT.md` | `1eb2623d5b96f68d503745159e8d26e6ceaae1b4074b616a3442f06dcbec9bea` | Renamed, content unchanged |
| `RESULTS.json` | `RESULTS.json` | `dbdf3b647add3d33ebee6c564d7586e2e808d36f35aedd4a5f9230fe25d6b342` | Unchanged copy |
| `scan.c` | `scan.c` | `ef756cfce053a65995a5f97cd3a53cb9fd973c6b7fef105cf72f2c3b99853a36` | Unchanged copy |

The public `verify.py` is a new compact affine-span checker.

### Carry characteristics

Source packets: `r40_multibit_carry_characteristic` and
`r40_state_first_differential_search`.

| Public file | Source file | Source SHA-256 | Import action |
|---|---|---|---|
| `FORMULAS.md` | `r40_multibit_carry_characteristic/FORMULAS.md` | `54983ed45581359f9d53efaa5f635d4daf90a2fb5d30952458b474636b2d507c` | Unchanged copy |
| `CORES.json` | `r40_state_first_differential_search/inputs/CORES.json` | `a2f8e4f8f9361b60810414fb86cf036b73fd8d15bacad8e8475da878dcdd25c6` | Unchanged copy |
| `WITNESSES.json` | `r40_multibit_carry_characteristic/results/WITNESSES.json` | `d391fab2b457e717e0ff3185ea7a9ecd5255929e1f484c80cdbcab47ddca5fdf` | Unchanged copy |

The public `verify.py` is a new independent scalar replay that does not use
hidden answers or search code.

## Public predecessor

The public predecessor is
[`sha256-structural-data` v0.1.0](https://github.com/0xplemonade/sha256-structural-data/releases/tag/v0.1.0).
Layr Labs HashSmash [discussion #1376](https://github.com/Layr-Labs/hash-smash/discussions/1376)
records that release and its scope.
