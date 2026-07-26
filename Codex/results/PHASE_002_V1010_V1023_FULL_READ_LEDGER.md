# Phase 002 - v1.0.10-v1.0.23 Full-read and Scope-freeze Result

## Chain

- Active plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-07-19-v1010-v1023-ch1-ch3-scientific-audit-master-plan-v2.md`
- Previous result: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_LATEST_SNAPSHOT_INTAKE_RESULT.md`
- Target commit: `8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Snapshot: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Manifest: `D:\Projects\Project_Anode_Fit\Codex\results\v1010_v1023_file_manifest.json`
- Canonical coverage ledger: `D:\Projects\Project_Anode_Fit\Codex\results\v1010_v1023_read_coverage.json`
- Worker evidence root: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase002`

## Gate Decision

**Status: `FULL_READ_SCOPE_PASS`.**

- Manifest files: 2,286
- Paths with exactly one primary assignment and disposition: 2,286 / 2,286
- Missing primary paths: 0
- Duplicate primary paths: 0
- Required files without an accepted read/inspection status: 0
- Scientific-correctness claims closed by this phase: 0

This gate establishes scope and evidence coverage. It does not establish that any equation, citation, scientific interpretation, code path, or prior defect-closure claim is correct.

## Frozen Scope

The pinned pre-v1.0.24 boundary contains every directory from v1.0.10 through v1.0.17, v1.0.18.1, v1.0.18.2, and v1.0.19 through v1.0.23. Phase 002 included the following material whenever it intersects Chapters 1-3 or the v1.0.10-v1.0.23 work history:

- shared and version-local plans, roadmaps, handovers, result ledgers, audits, defect unions, and reference ledgers;
- Chapter 1-3 TeX masters, included sections, appendices, bibliographies, figures, tables, and selected PDFs;
- implementation modules, graph scripts, fitting demonstrations, tests, data containers, and packaged archives;
- historical text artifacts needed to reconstruct deletion, relocation, supersession, recurrence, or regression;
- the JCP 147, 144111 (2017) source PDF included in the repository.

The five v1.0.23 precursor survey files stored under `Claude/docs/v1.0.22/results/comp_v23/` were resolved from `UNRESOLVED` to `REQUIRED_FULL_REVIEW`. Their directory placement does not remove them from the v1.0.23 lineage.

## Full-text Coverage

All 1,785 accepted text/code records were read first-to-last. The covered total is 410,053 lines. Worker summaries and path-level CSV files identify every file, assigned range, preliminary disposition, dependencies, and notes.

| Reviewer package | Assigned files | Full text files | Full text lines | Other records |
|---|---:|---:|---:|---:|
| A - plans | 88 | 88 | 8,544 | 0 |
| B - process core 1 | 184 | 184 | 26,898 | 0 |
| C - process core 2 | 183 | 167 | 27,571 | 16 |
| D - historical/derivative | 698 | 570 | 179,590 | 128 |
| E - docs v1.0.10-v1.0.18.2 | 173 | 107 | 57,331 | 66 |
| F - docs v1.0.19-v1.0.20 | 298 | 244 | 39,309 | 54 |
| G - docs v1.0.21-v1.0.22 | 272 | 263 | 51,267 | 9 |
| H - v1.0.23 and shared latest | 172 | 160 | 19,423 | 12 |
| Main - repository context/exclusions | 218 | 2 | 120 | 216 |
| **Total** | **2,286** | **1,785** | **410,053** | **501** |

The two main-context files are `CLAUDE.md` (87 lines) and `README.md` (33 lines). Worker-to-inventory validation found no line-count mismatch or partial text read. One previously truncated worker output range was reopened in a narrower interval and recovered before closure.

## PDF, Image, and Machine Coverage

### Required PDFs

- v1.0.10-v1.0.18.2 package: 26 PDFs, 707 / 707 pages rendered at 144 DPI and visually inspected.
- v1.0.19-v1.0.23 plus JCP source: 30 PDFs, 711 / 711 pages rendered at 144 DPI and visually inspected.
- Total: 56 PDFs, 1,418 / 1,418 pages.
- Missing pages: 0.
- Recheck pages remaining: 0.
- Detected critical/high/medium/low visual defects: 0 / 0 / 0 / 0.

The main integrator additionally inspected first, middle, and last contact-sheet samples from both PDF packages. The samples included prose-heavy derivations, equation/figure/table pages, and the terminal bibliography/conclusion pages.

### Required PNGs

- Required images: 86 / 86 visually inspected through 22 contact sheets.
- Blank or corrupt images: 0.
- Unintended clipping or overlap: 0.
- Two partial-frame assets were confirmed intentional rather than accidental crops.

### Required machine artifacts

- NPZ: 8 / 8 loaded with `allow_pickle=False`; all 13-array structures, shapes, dtypes, finite counts, and numeric ranges recorded.
- PYC: 6 / 6 headers and marshalled code-object structures inspected without execution.
- ZIP: 4 / 4 member listings and CRC integrity checked without extracting into the reviewed snapshot.
- Integrity failures: 0.
- Source/consumer provenance links still requiring Phase 003/009 adjudication: 12. These are not scope gaps.

## Explicit Exclusions

Exactly 216 text/config records were not read because they are outside the newly reset scientific workstream:

- 210 previous remote `Codex` artifacts excluded by the user's fresh-start instruction;
- 3 historical repository archive duplicates;
- 2 editor/runtime metadata files;
- 1 Git metadata/config file.

Exactly 125 historical derivative binaries were not re-rendered:

- 107 derivative PDFs;
- 18 derivative PNGs.

All 125 occur in package D. Their source text and selected version artifacts are covered elsewhere, and their exclusion is recorded path-by-path as `DERIVATIVE_SUPERSEDED` with status `NOT_READ_DERIVATIVE_BINARY_WITH_REASON`. They are not silently counted as reviewed media.

## Local-copy Cross-check

The local v1.0.10-v1.0.19 comparison produced:

- 186 byte-identical files;
- 51 line-ending or encoding-only differences;
- 0 normalized text-content differences;
- 2 binary PDF differences;
- 133 local-only build/cache artifacts;
- 0 snapshot-only files in the compared version scope.

Both differing v1.0.18.2 PDFs were independently rendered at 120 DPI. All 67 compared page-image hashes matched: 8 / 8 pages for `appendix_phase_separation.pdf` and 59 / 59 pages for `graphite_ica_ch1_v1.0.18.2.pdf`. The binary differences therefore do not produce a rendered visual difference at the checked resolution.

## Reconciliation Evidence

The following validations were rerun by the main integrator after all worker reports completed:

1. A-H assignments contain 2,068 unique `Claude` paths with zero missing, extra, or duplicate paths.
2. A-H plus MAIN contain 2,286 unique paths, exactly equal to the SHA-pinned manifest.
3. P, Q, R, and S contain 160 unique required binary paths and no path outside the primary inventory.
4. The 285 non-text primary records decompose into 160 separately verified required binaries plus 125 reasoned derivative exclusions.
5. Required accepted statuses are restricted to `FULL_TEXT_READ`, `FULL_PDF_VISUAL_READ`, `FULL_IMAGE_VISUAL_READ`, and `MACHINE_ARTIFACT_INSPECTED`.
6. Required records lacking one of those statuses: 0.
7. The integrated JSON parses successfully, contains 2,286 unique paths, has no empty status, and reports `FULL_READ_SCOPE_PASS`.

The exact-duplicate map contains 289 path rows and is retained at `D:\Projects\Project_Anode_Fit\Codex\results\phase002_exact_duplicate_map.csv` for Phase 003 supersession and semantic-diff adjudication.

## Confirmed, Pending, and Not Found

### Confirmed

- The intended v1.0.10-v1.0.23 evidence universe is frozen at the target SHA.
- Every manifest path has an explicit primary disposition.
- Every accepted required text file has complete first-to-last line coverage.
- Every selected required PDF page and required PNG has visual coverage.
- Every required NPZ/PYC/ZIP has an integrity/structure record.
- No reviewed `Claude` artifact, repository ref, or Git state was modified.

### Pending

- Canonical/successor relationships among non-identical historical artifacts require Phase 003 semantic lineage analysis.
- Twelve machine-artifact provenance links require Phase 003 or Phase 009 source/consumer mapping.
- Physical, chemical, mathematical, bibliographic, structural, and document-code correctness remain unverified until later phases.

### Evidence Not Found

- No undisposed in-scope file was found.
- No missing required PDF page or required image was found.
- No normalized text-content divergence was found in the local v1.0.10-v1.0.19 comparison.

## Files Created or Updated

- Created this Phase 002 result.
- Replaced the machine-only placeholder in `v1010_v1023_read_coverage.json` with the reconciled path-level coverage ledger.
- Added `D:\Projects\Project_Anode_Fit\Codex\work\scripts\integrate_phase002_coverage.ps1` so the reconciliation can be rerun deterministically.
- Updated the master plan and execution ledger at the phase boundary.

## Next Condition

Phase 003 may begin. It must use the frozen path ledger to reconstruct version goals, supersessions, chapter reorganizations, prior defect claims, artifact changes, and regressions. It may not reinterpret a reasoned derivative exclusion as scientific validation.
