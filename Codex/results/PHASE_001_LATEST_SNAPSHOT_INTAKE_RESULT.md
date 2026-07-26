# Phase 001 - Latest Snapshot Intake Result

## Summary

- Phase: `001`
- Plan steps: `1-10`
- Status: `COMPLETED`
- Gate: `LATEST_SNAPSHOT_PASS`
- Repository: `lksz1412/Project_Anode_Fit`
- Observed branch: `claude/anode-fit-v1-0-20-cxshf9`
- Scientific audit target SHA: `8ea83fc6825d2e62c360e08d7738ef26d3171914`
- v1.0.23 artifact-tip SHA: `ae6c967830d866e8b45e6087ba128b50790f2840`
- Observation basis: GitHub connector plus read-only GitHub REST and codeload archive endpoints

Phase 001 fixed a reproducible, read-only source state for the user-requested v1.0.10-v1.0.23 audit. It did not perform scientific full reading, literature adjudication, code execution, or document correction.

## Current Ground Truth

### Confirmed

1. The repository is public and its default branch is `main`.
2. The active Claude work branch existed as `claude/anode-fit-v1-0-20-cxshf9`.
3. At observation, that branch HEAD was `404c1873ddd8319a547b3c8edeb910a26fcdb970`, timestamped `2026-07-19T10:44:49Z`, and already contained v1.0.24 work.
4. The final v1.0.23 artifact commit was `ae6c967830d866e8b45e6087ba128b50790f2840`.
5. One additional scientific planning commit followed it: `8ea83fc6825d2e62c360e08d7738ef26d3171914`, adding `Claude/plans/2026-07-18-anodefit-bdd-integration-plan.md` and changing no v1.0.23 artifact.
6. The first v1.0.24 commit is a direct child of that planning commit. Therefore `8ea83fc...` is the complete pre-v1.0.24 boundary and is the canonical audit target.
7. GitHub comparison reports the observed branch HEAD as 18 commits ahead and zero commits behind the target boundary.

### Scope decision

The audit does not silently expand to v1.0.24. The target includes the final v1.0.23 artifacts and the one intervening shared scientific plan because the user explicitly placed `Claude/plans` in the primary evidence scope. v1.0.24 artifacts and claims remain outside this audit unless the user later revises the boundary.

## Snapshot Evidence

### Canonical archive

- Archive: `D:\Projects\Project_Anode_Fit\Codex\work\source_archives\8ea83fc6825d2e62c360e08d7738ef26d3171914.zip`
- Bytes: `116637966`
- SHA-256: `d986ed6dcc73f1462aa984dfb1f3914c311374ecab1458365fdb0a0becbecb63`
- Snapshot root: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Canonical manifest: `D:\Projects\Project_Anode_Fit\Codex\results\v1010_v1023_file_manifest.json`

### Tree equivalence

| Measure | GitHub recursive tree | Extracted snapshot | Manifest |
|---|---:|---:|---:|
| Files/blobs | 2286 | 2286 | 2286 |
| Directories/trees | 231 | 231 | n/a |
| Total tree entries | 2517 | 2517 | n/a |
| API truncation | false | n/a | n/a |

GitHub tree SHA: `043d235b94cd5b7828b795b89f05c9ef1820636e`.

### Version coverage

The following document directories are present:

`v1.0.10`, `v1.0.11`, `v1.0.12`, `v1.0.13`, `v1.0.14`, `v1.0.15`, `v1.0.16`, `v1.0.17`, `v1.0.18.1`, `v1.0.18.2`, `v1.0.19`, `v1.0.20`, `v1.0.21`, `v1.0.22`, and `v1.0.23`.

There is no `Claude/docs/v1.0.24` directory in the canonical target. v1.0.18 is represented by the two actual split-version directories, not by a nonexistent synthetic `v1.0.18` directory.

### Process and latest-artifact surfaces

- `Claude/plans`: 88 files
- `Claude/results`: 909 files
- `Claude/docs`: 835 files
- v1.0.23 top-level TeX masters: 4
- v1.0.23 PDFs: 3
- v1.0.23 Python files including tests and QA utilities: 6
- v1.0.23 version-local result files: 18

This is a presence and integrity check only. No file is marked `READ_FULL` in Phase 001.

## Local v1.0.10-v1.0.19 Comparison

Machine record: `D:\Projects\Project_Anode_Fit\Codex\results\snapshot_local_v1010_v1019_hash_comparison.csv`.

The comparison includes `v1.0.18.1` and `v1.0.18.2` explicitly.

| Relation | Count | Interpretation |
|---|---:|---|
| `BYTE_MATCH` | 186 | Local and pinned snapshot bytes are identical. |
| `EOL_OR_ENCODING_ONLY` | 51 | Text becomes identical after line-ending normalization. |
| `TEXT_CONTENT_DIFF` | 0 | No normalized text-content divergence detected. |
| `BINARY_DIFF` | 2 | Two v1.0.18.2 PDFs differ at binary level. |
| `LOCAL_ONLY` | 133 | Local build/cache artifacts: 51 `.log`, 29 `.aux`, 29 `.out`, 12 `.toc`, 11 `.pyc`, and 1 `.png`. |
| `SNAPSHOT_ONLY` | 0 | No pinned source file is absent locally within this comparison range. |

The two binary differences are:

- `v1.0.18.2/appendix_phase_separation.pdf`
- `v1.0.18.2/graphite_ica_ch1_v1.0.18.2.pdf`

Their semantic or visual equivalence is not inferred from binary hashes and remains a later PDF-verification item.

## Correction History

The first boundary candidate was the last explicitly labeled v1.0.23 commit, `ae6c967...`. A parent-chain check then found the one-file `Anode_Fit-BDD` scientific integration plan commit before v1.0.24 began. Because shared Claude plans are in scope, the canonical target was corrected to `8ea83fc...`.

The preliminary `ae6c967...` archive, snapshot, manifest, and local comparison were retained under `Codex/work` for provenance. They are not canonical audit inputs.

## Commands and Write Boundary

Executed command classes:

- GitHub connector reads for repository and branch discovery
- read-only GitHub REST commit, compare, and recursive-tree requests
- `curl.exe` against the GitHub codeload endpoint
- `tar.exe` extraction under the SHA-specific Codex snapshot directory
- PowerShell SHA-256, inventory, and comparison generation

No Git command was executed. All write destinations were under `D:\Projects\Project_Anode_Fit\Codex`. No command wrote to `D:\Projects\Project_Anode_Fit\Claude`.

## Confirmed, Unresolved, and Not Yet Verified

### Confirmed

- The v1.0.10-v1.0.23 source state is available and SHA-pinned.
- The canonical archive, extracted tree, and file manifest agree exactly in file count.
- The latest three-chapter v1.0.23 TeX, PDF, code, tests, result ledger, reference ledger, and handover surfaces are present.
- The configuration-update workstream is separate and was not executed.

### Unresolved

- The two locally different v1.0.18.2 PDFs require later page-level verification if local/remote visual divergence matters to lineage.
- Phase 002 must decide the full-read disposition of 2,286 snapshot files; presence is not equivalent to scientific relevance.
- The BDD integration plan is included as a forward scientific dependency, but it must not be mistaken for completed v1.0.23 work.

### Not yet verified

- Scientific correctness of Chapters 1-3
- Adequacy or correctness of cited literature
- Availability and utility of additional literature
- Textbook/review structure and prose quality
- Document-to-code fidelity
- Runtime, numerical, build, and PDF visual behavior

## Gate Decision

`LATEST_SNAPSHOT_PASS`

Rationale: the complete pre-v1.0.24 repository state is pinned by commit SHA, archived and hashed, extracted only under the Codex boundary, matched exactly to the GitHub recursive tree, and shown to contain all actual v1.0.10-v1.0.23 version directories including the v1.0.18 split variants.

## Next Phase Condition

Phase 002 may begin. It must construct a canonical in-scope inventory, classify every file, assign complete line/page coverage, and must not mark any artifact `READ_FULL` based only on the Phase 001 manifest.
