# Phase 065 v1.0.24–v1.0.24.1 Lineage Reaudit Implementation Plan

Date: 2026-08-30
Status: `ACTIVE_PENDING_ACTIVATION_PERSISTENCE`
Parent master plan: `Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`
Canonical completion master plan: `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`
Previous canonical result: `Codex/results/PHASE_064_RESULT.md`
Execution ledger: `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
Canonical ledger: `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
Recovery handover: `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

## Summary

Phase 065 performs a source-complete, process-complete and behavior-separated
reaudit of the frozen v1.0.24 and v1.0.24.1 lineage. It does not accept the
archive label, review status, successful build, synthetic fit or internal
runtime result as scientific authority. It reconstructs what changed, what was
only proposed, what was actually initialized at runtime, what was later copied
without semantic change, and what must be preserved, corrected, withheld or
discarded before canonical synthesis.

The phase follows cumulative Steps 70–75. The final integer step is split into
Steps 75.1 and 75.2 so that source disposition is persisted before the
integrated Lineage Report H gate. Phase 066 cannot start at Step 76 until the
Step 75.2 commit has been pushed and independently persistence-verified.

Every execution unit is result-first, uses an exact path allowlist, modifies
only `Codex/**`, receives independent review, is committed and pushed, and is
verified against the live remote before the next execution unit starts.
Machine evidence follows a `validation-JSON-last` collection rule.

## Current Ground Truth

### Git and protection state

- Active branch: `codex/anode-fit-v1025_2-canonical-completion`.
- Activation expected parent: `60ec2d2ad08a029224b86ddc3dcf6ff718c6d310`.
- The expected parent is the persisted Step 69.2 exact-eight commit with subject
  `audit(phase064): close v1023 lineage gate`.
- Phase 064 selected `CONDITIONAL_P064`, not `PASS_P064_LINEAGE_G`, because
  Ref. 7 original full text remains `GROUND_NOT_FOUND`.
- Protected branch `codex/lib-physics-endgame-v1025_2` remains pinned to
  `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`.
- `main`, its tracking reference and its live remote remain pinned to
  `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`.
- Frozen Claude source baseline:
  `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`.
- `Claude/**`, the protected branch and `main` are read-only.
- At activation entry, the parent snapshot's Phase 064 ledgers and active
  handover contained Step 69.2 precommit wording. This exact-seven working
  snapshot has replaced that wording with the persisted `60ec2d2...` terminal
  and moved the unique current position to Phase 065 activation pending
  persistence.

### Frozen v1.0.24/v1.0.24.1 manifest denominator

The authoritative inventory is
`Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json`. The Phase 065
slice is fixed as follows:

| Measure | Frozen value |
|---|---:|
| Manifest occurrence indices, zero-based | `826–1086` |
| Manifest occurrence ordinals, one-based | `827–1087` |
| Total path occurrences | `261` |
| v1.0.24 occurrences | `130` |
| v1.0.24.1 occurrences | `131` |
| Unique paths | `261` |
| Unique Git blobs | `131` |
| FULL_TEXT unique blobs | `125` |
| FULL_TEXT physical lines | `21,618` |
| FULL_PDF unique blobs/pages | `3 / 148` |
| FULL_IMAGE unique blobs | `3` |
| Unique-blob bytes | `7,812,647` |
| Occurrence bytes | `15,622,368` |

Occurrence roles are `theory=118`, `result=116`, `test=6`,
`generated_document=6`, `figure=6`, `implementation_guide=4`, `code=2`, and
`supporting_document=3`. Unique-blob roles are `theory=59`, `result=58`,
`test=3`, `generated_document=3`, `figure=3`, `implementation_guide=2`,
`code=1`, and `supporting_document=2`.

The occurrence path-set SHA-256, computed as sorted UTF-8 paths joined by LF
with one terminal LF, is
`815f37a830da3e5d6539d53bf6dc24c35dec012f39241818b070154b7b729aa7`; the
path-plus-blob SHA-256, computed with the same row ordering and a NUL between
each path and blob, is
`35c224df31807c02ab7d0f8ace3aad7edb36369b6d4d2dd97895589dd5624c0d`; and
the unique blob-set SHA-256 is
`0cc9e04e676dd9c5024842eeaf57180b515bbe2bb7d068dc7aa8eb10c83c8cdd`.

### Mirror and archive boundary

- All `130/130` paths shared by the two version directories are byte-identical
  Git blobs.
- v1.0.24.1 adds only `Claude/docs/v1.0.24.1/ARCHIVE_NOTE.md`.
- v1.0.24.1 therefore cannot be counted as a second independent scientific or
  implementation validation corpus.
- The archive snapshot commit is `2147abfac3fb6c82279aefb2b21c749a521112dc`
  with parent `b109707fbacf7a3e2b64bdc2d69aae3ada761ece`.
- The current sparse worktree does not materialize this frozen directory.
  Every source read must use the baseline Git object, never interpret an absent
  worktree path as `GROUND_NOT_FOUND`.

### Mandatory supplemental process inputs

The following six baseline Git blobs are immutable anchor records outside the
261-occurrence release slice. They are mandatory but are only a subset of the
complete routed-process evidence denominator below:

| Path | Blob | Lines | SHA-256 |
|---|---|---:|---|
| `Claude/plans/2026-07-18-v1024-completeness-validation-plan.md` | `b9286c77e686d8666033de553e6bbd8e66d2ad9d` | 198 | `0935ba2daa90bdaee860a0fe159f8772e0b74cb38f4b3a712876d0b3217dd252` |
| `Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md` | `ed1f2defdae29dc8a4351e63461fd1f1f6c21995` | 215 | `fa3bdcdcb4bb9cf07d307ef52344730dee295b1f2c6c1ffea48be4c455feb842` |
| `Claude/plans/2026-07-22-v1024-feedback-revision-plan.md` | `c6ec2d6c5b59e5fe7f3020b2d84e1ad325d0b401` | 226 | `8ae96b72514b412ac2d0a8b6bde1d39235e3ddb9a2c3bb4ec926d51c40bf33a0` |
| `Claude/results/V1024_EXECUTION_LEDGER.md` | `44fcc0042274d5453ed8d8c635d5fe90ec243e5b` | 14 | `b96103432ac5aa2ae60bacb160d12e3345470d0cd717c7d13f81e4cd4e63aa5f` |
| `Claude/results/V1024_PROGRESS_SUMMARY.md` | `d1a6ec7a3dc9244d6284216c704a75909b3fc02c` | 51 | `c6932755290032b786fda9ebe60d01a9d4b3bbfde9e20af033de3626a42c33c1` |
| `Claude/results/V1024_FEEDBACK_EXECUTION_LEDGER.md` | `eb82d88311d81d932dbb16a01684356052a0e7c5` | 24 | `44cbbf4cc13af7001fa23685ca120b5ef96fc834d2cae07e2f7ba27583cff296` |

Step 70 must additionally reconstruct and full-read the following baseline
process/evidence universe rather than stopping at those six anchors:

| Partition | Exact denominator |
|---|---:|
| v1.0.24 plans | `3 documents / 639 lines` |
| v1.0.24 root result/process records | `29 documents / 2,068 lines` |
| `Claude/results/comp_v24` Markdown | `31 files / 2,635 lines` |
| `comp_v24` Python | `29 files / 2,932 lines` |
| `comp_v24` JSON | `16 files / 1,650 lines` |
| `comp_v24` CSV | `10 files / 45,203 lines` |
| `comp_v24` TXT | `7 files / 171 lines` |
| `comp_v24` PNG | `33 files` |
| Phase 057 v1.0.24 routing read-map/observations | `11 documents / 1,890 lines` |

The minimum narrative-history denominator is `74 documents / 7,232 lines`:
the three plans, 29 root records, 31 `comp_v24` Markdown documents and 11
Phase 057 routing documents. The remaining `comp_v24` evidence is `95 files`,
comprising 62 code/data/text files with 49,956 physical lines and 33 PNGs.
Step 70 inventories and reads every narrative record; Steps 70–72 must fully
read or visually inspect the evidence files assigned to their source, runtime,
fit or scientific-claim role. No partition may be accepted from filename or
summary alone.

### Recovered process and authority boundary

The release-tree Git history contains 38 commits from
`04ebc0cf8b36d34f776ddbc2b356ca0246983fe8` (v1.0.23-to-v1.0.24 R0 clone)
through `2147abfac3fb6c82279aefb2b21c749a521112dc` (v1.0.24.1 archive). The
routed union of the release trees, three plans, three named ledger/summary
anchors and `Claude/results/comp_v24` contains 98 distinct commits. Step 70
must preserve both universes and must not report 38 as the complete process
history.
The sequence contains the R2 code patch,
nine-window competing drafts, R3/R4 review, R5 default and graft revisions,
doc-code corrections, optional six-gallery addition, code-guide generation,
FB0–FB9 editorial revision and the v1.0.24.1 archive. Step 70 must reconstruct
the full relevant commit graph from Git and inspect every selected commit's
parents, changed paths and diff; this paragraph is a routing hypothesis, not a
substitute for that census.

The following provisional boundaries are already binding until reaudited:

- v1.0.24 R0 inherited v1.0.23 behavior and its unresolved defects.
- The regular-solution, five-feature, LCO toggle and related R2 changes require
  separate static and runtime verification.
- A comment about the `3600` seconds-per-hour conversion is not evidence that
  the runtime timebase defect was repaired.
- A default stated in a brief, guide, review or ledger is not the runtime
  constructor/import default.
- Competition drafts and review artifacts are candidates, not adopted truth.
- Public pOCV fitting is internal calibration evidence unless specimen,
  protocol, capacity basis and held-out validation establish more.
- A component or peak is not automatically a phase, gallery or material
  identity.
- v1.0.24.1 is an editorial/archive identity unless a byte difference proves
  otherwise.
- Generated HTML and PDFs are derived artifacts and cannot overrule their
  source or executable behavior.
- The `.json`-suffixed snapshot occurrence is a 37-byte plain-text pointer,
  `snapshot -> ch1_graphite_v1.0.24.tex`, not JSON. Step 70 must classify it by
  observed bytes and must not send it to a strict JSON parser because of its
  filename suffix.
- Phase 057 provisional observations and all downstream corrections remain
  routed evidence; later conclusions cannot be silently back-projected into
  what v1.0.24 itself established.
- The Phase 057 v1.0.24/v1.0.24.1 routing universe is the read map plus
  observation documents AG–AN and AX–AY, with 82 provisional findings in
  `INTENT-PROV-0228–0292` and `INTENT-PROV-0388–0404`. Step 70 must read the
  documents themselves before claiming that denominator.
- The two master-plan JSON files are immutable Phase 059 planning snapshots,
  not live phase-position ledgers. Their scope and numbering remain normative,
  but their old current-position fields must not overwrite the two Markdown
  ledgers and active handover.
- Phase 064 routes six exact obligations into Phase 065: preserved assets
  `P059-CFR-CF-01`, `P059-CFR-CF-02`, `P059-CFR-CF-06`, and
  `P059-CFR-CF-07`, plus open repair blockers `P059-CFR-RB-02` and
  `P059-CFR-RB-03`. Step 75 must retain their identifiers and acceptance
  boundaries unless exact evidence closes them.

## Phase Range

| Execution unit | Scope | Terminal required before next unit |
|---|---|---|
| Plan activation | Save this detailed plan and recovery contract | `PASS_P065_PLAN_ACTIVATION_PERSISTENCE` |
| Step 70 | Source/process topology and complete-read attestation | `PASS_P065_STEP70_PERSISTENCE` |
| Step 71 | Code/profile/default static audit | `PASS_P065_STEP71_PERSISTENCE` |
| Step 72 | Skew-peak and material-decomposition authority audit | `PASS_P065_STEP72_PERSISTENCE` |
| Step 73 | Fresh-import, explicit-profile and legacy-restoration runtime audit | `PASS_P065_STEP73_PERSISTENCE` |
| Step 74 | Document/code/guide conformance audit | `PASS_P065_STEP74_PERSISTENCE` |
| Step 75.1 | Complete source disposition and carry-forward delta | `PASS_P065_STEP75_1_PERSISTENCE` |
| Step 75.2 | Integrated validation, Lineage Report H and final gate | `PASS_P065_STEP75_2_PERSISTENCE` |

Step numbering is cumulative. Phase 066 begins at Step 76; no Phase 065
substep creates a new integer step.

## Exact Read Inputs

### Recovery controls at every boundary

Before every execution unit, reread from line 1 through end of file:

1. both master plans named at the top of this plan;
2. this detailed plan;
3. both execution ledgers;
4. the active handover;
5. the immediately preceding execution-unit result;
6. every machine artifact that the next unit consumes.

The recovery note must distinguish `DIRECT_READ`, `AGENT_FULL_READ`,
`PARTIAL_READ`, `GROUND_NOT_FOUND`, and `NOT_APPLICABLE`. A summary, `rg`
result, manifest entry, successful parse, build or earlier report never replaces
the required source read.

### Frozen source inputs

- Reconstruct all 261 occurrence paths from the Phase 056 manifest.
- Read all 131 unique Git blobs at the frozen baseline.
- Read the 125 text blobs from first through last physical line, totaling
  21,618 lines.
- Extract and read all text from the three unique PDFs, 148 pages total; render
  every page with Poppler and visually inspect every rendered page.
- Inspect all three unique PNG blobs at original resolution.
- Record the 130 byte-identical cross-version pairs and the sole archive-note
  addition without double-counting read coverage.
- Read the six supplemental process inputs above from first through last line,
  totaling 728 lines.
- Read the complete 74-document narrative history and the remaining 95
  `comp_v24` evidence files under the partition rules above.
- Reconstruct both the 38-commit release-tree topology and the 98-commit routed
  process topology and inspect every selected
  commit's parent relation, message, path list and complete patch.
- Route every Phase 057 v1.0.24/v1.0.24.1 observation by exact identifier and
  evidence path; do not copy only a summary count.

### Full-read partitioning

Step 70 may partition work among independent reviewers by disjoint blob or page
ranges. Each partition report must include exact paths/blobs, covered line or
page intervals, hashes, truncation checks, findings and unreviewed intervals.
The controller must independently reconstruct the denominator and merge only
reports that prove full assigned coverage. Duplicate mirror paths may reuse a
verified blob read, but both occurrence identities remain in the mapping.

## Non-goals and Scope Guards

- Do not edit `Claude/**` or any frozen source branch.
- Do not merge, rebase, cherry-pick or rewrite existing branches.
- Do not repair production code during Phase 065.
- Do not choose the final canonical model, equation family or material default.
- Do not promote a build, import, golden roundtrip, synthetic curve, internal
  fit or visual similarity to external scientific or material validation.
- Do not treat a fit component as a phase, gallery or chemical species without
  primary structural/thermodynamic evidence.
- Do not treat v1.0.24.1 as independent corroboration of v1.0.24.
- Do not infer missing literature content from metadata, abstracts, citations,
  other papers or model memory.
- Do not invent a DOI, title, author, equation, parameter value or anchor.
- Do not accept a claimed default without tracing the actual initialization
  path and observing it in a fresh isolated process.
- Do not combine fresh import, explicit profile and legacy restoration into a
  single test outcome.
- Do not interpret a stale guide as runtime authority.
- Do not let later v1.0.25 corrections erase the historical v1.0.24 state; route
  them as downstream supersession evidence.
- Do not mention code, functions, files, classes, keys, APIs, tests, commits,
  phases, steps or work history in future main scientific prose. Such material
  belongs only in an explicitly designated implementation appendix or companion.
- Do not start Phase 066 before the final persistence terminal.

## Implementation Changes

All lists below are exact path allowlists. No rename is allowed. Every unit must
stage the result document before its machine JSON and must end with no unstaged
or untracked path.

### Plan activation — exact seven

1. `Codex/plans/2026-08-30-phase065-v1024-v1024_1-lineage-detailed-plan.md`
2. `Codex/work/v1024_phase065/validate_phase065_plan.py`
3. `Codex/results/PHASE_065_PLAN_ACTIVATION_VALIDATION.json`
4. `Codex/results/PHASE_065_PLAN_ACTIVATION_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Expected subject: `docs(phase065): plan v1024 lineage reaudit`.

### Step 70 — exact eight

1. `Codex/work/v1024_phase065/build_phase065_step70.py`
2. `Codex/work/v1024_phase065/validate_phase065_step70.py`
3. `Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json`
4. `Codex/results/PHASE_065_COMPLETE_READ_ATTESTATION.json`
5. `Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md`
6. parent execution ledger
7. canonical execution ledger
8. active handover

Expected subject: `audit(phase065): freeze v1024 source process topology`.

### Step 71 — exact eight

1. `Codex/work/v1024_phase065/build_phase065_step71.py`
2. `Codex/work/v1024_phase065/validate_phase065_step71.py`
3. `Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json`
4. `Codex/results/PHASE_065_STATIC_ROUTE_ATTESTATION.json`
5. `Codex/results/PHASE_065_STEP_071_CODE_PROFILE_DEFAULT_RESULT.md`
6. parent execution ledger
7. canonical execution ledger
8. active handover

Expected subject: `audit(phase065): trace v1024 code profile defaults`.

### Step 72 — exact seven

1. `Codex/work/v1024_phase065/build_phase065_step72.py`
2. `Codex/work/v1024_phase065/validate_phase065_step72.py`
3. `Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json`
4. `Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md`
5. parent execution ledger
6. canonical execution ledger
7. active handover

Expected subject: `audit(phase065): bound v1024 skew material authority`.

### Step 73 — exact eight

1. `Codex/work/v1024_phase065/build_phase065_step73.py`
2. `Codex/work/v1024_phase065/validate_phase065_step73.py`
3. `Codex/results/PHASE_065_INITIALIZATION_ROUTE_MATRIX.json`
4. `Codex/results/PHASE_065_RUNTIME_ATTESTATION.json`
5. `Codex/results/PHASE_065_STEP_073_INITIALIZATION_RUNTIME_RESULT.md`
6. parent execution ledger
7. canonical execution ledger
8. active handover

Expected subject: `audit(phase065): separate v1024 initialization routes`.

### Step 74 — exact seven

1. `Codex/work/v1024_phase065/build_phase065_step74.py`
2. `Codex/work/v1024_phase065/validate_phase065_step74.py`
3. `Codex/results/PHASE_065_DOC_CODE_GUIDE_CONFORMANCE_MATRIX.json`
4. `Codex/results/PHASE_065_STEP_074_DOC_CODE_GUIDE_RESULT.md`
5. parent execution ledger
6. canonical execution ledger
7. active handover

Expected subject: `audit(phase065): adjudicate v1024 doc code guide`.

### Step 75.1 — exact eight

1. `Codex/work/v1024_phase065/build_phase065_step75_1.py`
2. `Codex/work/v1024_phase065/validate_phase065_step75_1.py`
3. `Codex/results/PHASE_065_SOURCE_DISPOSITION_MATRIX.json`
4. `Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json`
5. `Codex/results/PHASE_065_STEP_075_1_DISPOSITION_RESULT.md`
6. parent execution ledger
7. canonical execution ledger
8. active handover

Expected subject: `audit(phase065): disposition v1024 lineage`.

### Step 75.2 — exact eight

1. `Codex/work/v1024_phase065/validate_phase065_final.py`
2. `Codex/results/PHASE_065_VALIDATION.json`
3. `Codex/results/PHASE_065_V1024_V1024_1_LINEAGE_REPORT_H.md`
4. `Codex/results/PHASE_065_STEP_075_2_GATE_RESULT.md`
5. `Codex/results/PHASE_065_RESULT.md`
6. parent execution ledger
7. canonical execution ledger
8. active handover

Expected subject: `audit(phase065): close v1024 lineage gate`.

## Plan Activation Unit — Save Before Step 70

### Activation A — recovery and validator-first RED

1. Verify active, upstream, tracking and live-remote tips equal the expected
   parent and verify protected/main tips and `Claude/**` cleanliness.
2. Reread both master plans, both ledgers, active handover, Phase 064 detailed
   plan, Phase 064 result and Step 69.2 gate record.
3. Save this detailed plan, validator and human activation result before the
   machine validation JSON.
4. Run the validator in content mode while the JSON is absent and record the
   expected `E_VALIDATION_ARTIFACT_MISSING` RED terminal.

### Activation B — content and boundary validation

1. Reconstruct the 261/131 manifest denominator from the frozen manifest.
2. Prove 130/130 pairwise blob equality and the sole v1.0.24.1 archive-note
   addition.
3. Verify all six supplemental input identities and extents against baseline
   Git blobs.
4. Validate required sections, cumulative numbering, exact allowlists,
   result-first rule, authority exclusions, separated runtime routes and stop
   conditions.
5. Run named semantic negative controls, strict-JSON rejection probes,
   deterministic double generation and actual Git boundary controls.
6. Write `PHASE_065_PLAN_ACTIVATION_VALIDATION.json` last and refuse overwrite.

### Activation C — exact commit and persistence

1. Stage exactly seven paths and verify index bytes equal worktree bytes.
2. Run full staged validation on Python 3.12 and Python 3.14.
3. Obtain independent scientific, validator and records reviews with
   `P0/P1/P2` counts; any P0 or P1 blocks commit.
4. Commit with the exact parent and subject, push the active branch, fetch and
   verify local/upstream/tracking/live equality.
5. Verify the exact commit path set, commit blob bytes, protected/main/Claude
   non-change and clean worktree on both runtimes.
6. Only `PASS_P065_PLAN_ACTIVATION_PERSISTENCE` releases Step 70.

## Phase 065 — v1.0.24/v1.0.24.1 Reaudit

### Step 70 — Source/Process Topology and Complete-read Attestation

#### Task 70A — immutable denominator

- Reconstruct all 261 occurrence rows and all 131 unique blob identities from
  the Phase 056 manifest.
- Recompute path, path/blob, unique-blob, size, role, modality and extent
  denominators without trusting the values copied into this plan.
- Prove the 130 shared pairs are byte-identical and bind the archive-note-only
  delta to exact paths and blobs.
- Record why zero-based indices and one-based ordinals differ by one.

#### Task 70B — full source reads

- Read every one of the 125 unique text blobs, 21,618 lines total.
- Extract, read, render and visually inspect all 148 pages of the three unique
  PDFs. Preserve page-level render and text-extraction attestation.
- Inspect the three images at original resolution.
- Read the six supplemental records, 728 lines total.
- Record line/page intervals and output-truncation rechecks. No interval may be
  inferred from a manifest or previous phase report.

#### Task 70C — process topology

- Enumerate the 38 release-tree commits and 98 routed-union commits with two
  explicit reproducible Git queries.
- Inspect parents, subjects, changed paths and complete patches.
- Separate proposal, competing draft, review, patch, build, feedback revision,
  archive and status/self-report states.
- Map Phase 057 observations and downstream correction routes without treating
  later corrections as evidence of what the original release already knew.

#### Task 70D — TeX reachability and derived-artifact topology

- Reconstruct the three adopted master dependency closures: graphite
  `34 files / 5,625 lines`, LCO `13 / 1,618`, and Si/blend `11 / 1,143`, with
  union `56 unique TeX files / 8,218 lines`.
- Separate the non-master TeX universe `34 files / 4,489 lines`: competition
  W1–W9, `refine_b`, phase-separation appendix, orphan Si appendix and legacy
  preambles.
- Bind each generated PDF, HTML and image to its source/producer route. The
  adopted PDFs have `97 + 30 + 21 = 148` pages.

### Step 71 — Code, Profile and Default Static Audit

#### Task 71A — code and test identity

- Compare v1.0.23, v1.0.24 and the v1.0.24.1 mirror by Git blob and normalized
  text.
- Parse every Python source/test blob with the intended grammar without
  importing the source checkout.
- Inventory constructor parameters, profile registries, factory paths, load
  paths, default values, option gates, restoration keys and silent fallbacks.

#### Task 71B — feature and initialization routing

- Trace the regular-solution @3 kernel, including its intended Si-host route
  and every actually reachable opt-in material route, separately from the
  graphite five-feature @5 replacement, optional six-gallery path, per-peak LCO
  interaction, LCO electronic-entropy toggle and blend-related initialization.
  Do not label graphite @5 as a `kernel='regsol'` route merely because its
  transition dictionaries carry interaction parameters.
- Distinguish absent argument, explicit false/zero, explicit profile, saved
  legacy state and current saved state.
- Pin each claimed default to a callable and exact source slice. A guide or
  ledger statement is not a default.

#### Task 71C — defect and non-change boundary

- Test statically whether the known seconds/hour, current partition, capacity
  basis, root validation and fallback routes changed or only received comments.
- Record additions, removals, signature changes and unchanged inherited logic.
- Withhold behavior conclusions for Step 73 runtime evidence.

### Step 72 — Skew Peak and Material-decomposition Authority

#### Task 72A — origin genealogy

- Search theory, plans, competing drafts, results, guides, code and commit diffs
  for each skew/asymmetry and material-decomposition statement.
- Separate proposed, reviewed, adopted, implemented, enabled-by-default,
  calibrated, externally validated and later superseded states.
- If the final skew implementation is absent from v1.0.24, record absence as a
  finding; do not import the v1.0.25 implementation backward.

#### Task 72B — independent derivations

- Re-derive the ideal lattice-gas/logistic peak, center, area and width under an
  explicit coordinate and sign convention.
- Re-derive the symmetric regular-solution chemical potential,
  `RT ln[x/(1-x)] + Omega(1-2x)`, critical condition `Omega=2RT`, spinodal
  condition and implicit binodal/common-tangent requirement.
- Derive how a state-dependent barrier or observation weight can create
  asymmetry and state exactly which assumptions are needed before calling it a
  skew-peak law.
- Derive the shared-voltage material sum and show that weights require a single
  declared capacity/mass basis; component additivity does not establish phase
  identity or finite-rate independence.

#### Task 72C — evidence ceilings

- Separate graphite, LCO, Si and blend claims.
- Bind every numerical or literature-dependent statement to an exact source or
  classify it `UNVERIFIED`/`GROUND_NOT_FOUND`.
- Preserve later removal or correction records as supersession evidence.
- Do not claim doped high-voltage LCO coverage from pristine or ordinary-LCO
  material evidence.

#### Task 72D — citation and DOI authority census

- Census all 90 TeX blobs: 95 bibliography-item occurrences/93 unique keys,
  561 citation occurrences/95 unique keys, and 91 DOI occurrences/85 unique
  DOI strings. Recompute these values rather than trusting the plan copy.
- Validate the adopted three-master dependency closure separately from the 34
  non-master candidate/orphan TeX files.
- The two currently identified cite-undefined keys, `fergusonbazant2014` and
  `guo2016`, occur only in rejected competition candidate
  `results/comp_R1/W1/gr_2L.tex`; verify the non-graft decision before treating
  them as non-blocking.
- For adopted load-bearing claims, distinguish bibliographic identity
  (title/authors/venue/DOI) from proposition, page and equation support. DOI
  existence or an internal reference table never proves proposition support.
- Any unavailable primary text remains `GROUND_NOT_FOUND` with an acquisition
  owner. Never fabricate a citation or infer its method from a secondary source.

### Step 73 — Independent Initialization and Runtime Gates

#### Task 73A — isolated runtime harness

- Materialize exact baseline Git blobs in a disposable directory outside the
  repository and verify every materialized path remains under that directory.
- Run with Python 3.12 and Python 3.14 using isolated, no-bytecode UTF-8 mode.
- Record interpreter and numerical-library versions, commands, stdout, stderr,
  exit code, input hash and output hash for every run.
- Never import the frozen source from the working checkout.

#### Task 73B — three required independent routes

1. **Fresh import:** no explicit profile/default override and no saved state.
2. **Explicit profile:** each named profile supplied through its public
   initialization path, independently of fresh defaults.
3. **Legacy restoration:** a legacy-compatible saved state reconstructed from
   the predecessor schema and loaded through the actual restoration path.

Each route must have its own process, fixture, observations and gate. A shared
downstream curve does not prove that all three initialization routes were used.
Mutation probes must make each route fail independently when its defining input
is removed or redirected. Step 73 must consume the exact symbol, constructor,
input-state and restoration-key mapping frozen by Step 71; the candidate names
known at activation time do not define what the master plan means by
`explicit profile`. Execute the routes in changed orders as a negative control
for leaked mutable module or global state.

Each route outcome must use exactly one of
`IMPLEMENTED_AND_OBSERVED`, `ABSENT_IN_FROZEN_SOURCE`, or
`GROUND_NOT_FOUND`. Absence may be a correct audit result but is not a passing
behavior route. In particular, no profile registry or saved-state restoration
loader may be invented if the Step 71 static census does not find one.

#### Task 73C — numerical and legacy observations

- Test default-off and enabled feature paths separately.
- Test old-key absence, explicit zero/false, current-key presence and legacy
  restoration without conflating them.
- Compare v1.0.23 fallback, v1.0.24 fresh defaults and v1.0.24 explicit options
  with bit-exact or tolerance-declared outputs.
- Measure the seconds/hour route directly; comments or unit labels are not
  behavior evidence.
- Preserve exceptions, unsupported paths and silent fallbacks as findings.

### Step 74 — Document, Code and Guide Conformance

- Build an exact claim-to-source-to-code-to-runtime matrix for the theory,
  result records, Markdown guide, HTML guide, tests and generated documents.
- Identify stale defaults, stale option names, unsupported features, outdated
  equations, missing caveats, version drift, archive wording and guide/source
  disagreements.
- Give executable behavior precedence for behavior claims, primary source text
  precedence for scientific claims and Git chronology precedence for adoption
  claims. No one authority class may overrule another class outside its domain.
- Distinguish source, generated and copied artifacts. HTML/PDF repetition does
  not multiply support.
- Inspect the 3,812-line HTML as authored wrapper, embedded Mermaid vendor
  payload and initialization footer. Verify the known candidate rendering
  defects around pipe-delimited `|I|`, `R_n` and `V_n` table content rather
  than accepting the HTML's existence as successful guide conformance.
- Audit visible main scientific text for implementation-history language and
  route necessary implementation detail to a designated appendix/companion.
- Record every mismatch with severity, exact anchors, accountable owner,
  acceptance criterion and target phase.

### Step 75.1 — Source Disposition and Carry-forward Delta

- Give all 261 source occurrences a disposition while preserving 131-blob
  deduplication identity.
- Allowed dispositions are `PRESERVE`, `CORRECT`, `THEORY_ONLY`, `UNVERIFIED`,
  `REJECTED_SOURCE` and `DISCARD`.
- `CORRECT` means a bounded proposition is retained only with an explicit
  correction; it never rewrites the frozen source.
- Route every open Phase 057 observation, Step 70–74 finding, inherited Phase
  064 route and downstream supersession to exactly one canonical owner and an
  exact acceptance criterion.
- Preserve old owner identifiers when the obligation is unchanged. Detect
  ownerless, multiply-owned and semantically duplicated obligations.
- State explicitly whether Phase 065 creates a new blocker; do not hide one in
  a general carry-forward row.

### Step 75.2 — Integrated Validation, Lineage Report H and Final Gate

- Strict-parse and fully traverse every Phase 065 machine artifact.
- Replay activation and Steps 70–75.1 validators at their exact historical
  precommit and persistence commits.
- Recompute all source/read/process/static/runtime/science/conformance/
  disposition/carry denominators independently.
- Run named semantic negative controls, malformed/duplicate/nonfinite JSON
  probes, deterministic double generation and disposable Git-boundary probes.
- Save Lineage Report H, gate result and Phase result before the final machine
  JSON; write the JSON last.
- Obtain independent science, validator and records reviews before commit.

## Phase Gate

### `PASS_P065_LINEAGE_H`

This gate may be selected only when all of the following are true:

1. all 261 occurrences map to 131 fully read unique blobs with exact extents;
2. all three PDFs/148 pages and three images are fully inspected;
3. all six supplemental records and the complete selected process topology are
   fully read;
4. the v1.0.24.1 mirror/archive boundary is exact and not double-counted;
5. code/profile/default changes and non-changes are source-anchored;
6. skew and material-decomposition claims have explicit derivations, evidence
   tiers and applicability limits;
7. fresh import, explicit profile and legacy restoration pass or fail as three
   separately observed runtime routes on both supported interpreters;
8. every stale document/code/guide mismatch has an exact disposition and owner;
9. all source and inherited obligations have one disposition and one route;
10. no external scientific/material/experimental authority is promoted beyond
    the acquired evidence;
11. all subordinate and final validation, exact-path, push and persistence
    controls pass.

`PASS_P065_LINEAGE_H` means only that the internal v1.0.24/v1.0.24.1 lineage,
behavior and authority boundaries are completely audited. It does not mean the
model is canonical, externally valid, publication-ready or scientifically
complete.

### `CONDITIONAL_P065`

Use this when internal coverage is complete but a required scientific source,
runtime route or authority boundary cannot be closed without new external
authority. Every condition must have an exact owner and acceptance criterion.
This gate does not authorize Phase 065 evidence to satisfy a missing Phase 071
primary-source requirement.

### `FAIL_P065`

Use this for incomplete unique-source coverage, unseparated initialization
routes, unresolved exact-path or persistence failure, ownerless blocking
conflict, source mutation, protected-branch drift or a false authority
promotion.

## Implementation Interfaces

### Source topology row

`occurrence_index`, `ordinal`, `version`, `path`, `blob`, `dedup_group`,
`role`, `review_mode`, `extent`, `size_bytes`, `read_status`, `read_ranges`,
`mirror_counterpart`, `process_routes`.

### Process row

`commit`, `parents`, `subject`, `changed_paths`, `complete_diff_read`,
`state_class`, `predecessors`, `successors`, `adoption_authority`, `notes`.

### Static initialization row

`callable`, `source_path`, `source_blob`, `line_range`, `argument`,
`declared_default`, `registry_default`, `factory_default`, `restore_key`,
`fallback`, `profile_routes`, `conflicts`.

### Scientific authority row

`claim_id`, `material`, `proposition`, `derivation_id`, `source_tier`,
`exact_anchor`, `implementation_state`, `default_state`, `validation_state`,
`applicability`, `status`, `supersession`.

### Runtime row

`route_id`, `route_class`, `runtime`, `interpreter`, `numpy`, `input_hash`,
`command`, `cwd`, `source_root`, `exit_code`, `stdout_hash`, `stderr_hash`,
`observations`, `mutation_probe`, `gate`.

### Conformance row

`finding_id`, `claim_class`, `claim_path`, `claim_anchor`, `authority_path`,
`authority_anchor`, `runtime_route`, `status`, `severity`, `owner`,
`acceptance_criterion`, `target_phase`.

### Disposition row

`source_path`, `blob`, `occurrence_identity`, `disposition`, `reason`,
`evidence_routes`, `open_routes`, `canonical_owner`, `acceptance_criterion`,
`target_phase`, `external_authority_promoted`.

## Test and Validation Plan

### Strict artifact validation

- UTF-8 decode and canonical LF serialization.
- Strict JSON parsing with duplicate-key and nonfinite-number rejection.
- Full recursive node traversal with exact schema and allowed-enum checks.
- Raw-byte, LF-normalized and semantic SHA-256 identities.
- Exact denominator, path, blob, range, page, process and route coverage.
- No NaN/Infinity, duplicate ID, duplicate route, orphan owner or implicit
  default.
- Deterministic generation `2/2` before every commit.

### Named semantic negative controls

At minimum mutate independently and require a unique rejection for:

1. expected parent or branch;
2. protected/main/baseline reference;
3. manifest occurrence or unique-blob count;
4. text line, PDF page or image count;
5. path-set, path/blob or unique-blob hash;
6. a shared-pair blob or the archive-only path;
7. a supplemental blob, line extent or hash;
8. cumulative step range;
9. exact activation or step allowlist;
10. result-first and JSON-last control;
11. fresh-import route presence;
12. explicit-profile route presence;
13. legacy-restoration route presence;
14. route independence;
15. scientific/material/external authority exclusion;
16. v1.0.24.1 independence false;
17. semantic hash;
18. persisted parent, subject, paths or bytes.

### Validator source-policy controls

- Permit `subprocess.run` only at the unique `run_process` call site and permit
  `run_process` only as the implementation of the Git wrapper. Reject direct,
  aliased, dynamic-attribute and `Popen` child execution.
- Reject unsafe Git alias/protocol command construction and callable aliasing.
- Permit filesystem mutators only in the atomic JSON-last collector and the
  boundary-checked disposable Git-fixture functions. Reject repository writes,
  deletes, moves or replacements from every other call site.
- Exercise each execution and filesystem escape with a named AST-only negative
  probe; no negative probe may execute its injected payload.

### Git and persistence controls

- active branch and upstream name;
- local/upstream/tracking/live-active equality;
- protected local/tracking/live equality;
- main tracking/live equality;
- exact staged or committed path set with rename rejection;
- index/worktree or commit/worktree byte equality;
- no `Claude/**` change;
- no unstaged or untracked path;
- `git diff --check`;
- exact parent and subject;
- both Python runtimes;
- push followed by fetch and live-remote verification.

## Stop Conditions

Stop the current execution unit and do not commit if any of these occurs:

- active branch divergence or unexpected parent;
- protected branch, main or `Claude/**` drift;
- incomplete text/PDF/image/process read coverage;
- output truncation that leaves an interval unverified;
- inconsistent manifest or mirror identity;
- an initialization route cannot be separated from another route;
- a required runtime cannot execute and no bounded diagnostic classification is
  possible;
- a load-bearing citation or equation depends on fabricated or inaccessible
  content and cannot remain explicitly unverified;
- a source is assigned contradictory dispositions;
- an obligation is ownerless or multiply owned;
- validator, negative-control, determinism, exact-path or persistence failure;
- any P0 or P1 independent-review finding;
- three consecutive push failures;
- new credentials, paid-source access, destructive action or a scientific
  choice requiring user authority.

## Assumptions

- Read-only Git object access is sufficient for frozen Claude sources.
- Python 3.12 and Python 3.14 remain available for validator and isolated
  runtime execution.
- Poppler and the pinned PDF/image libraries remain available for Step 70.
- Missing external literature may remain `GROUND_NOT_FOUND` with a precise
  acquisition owner; it must never be guessed.
- The user has authorized autonomous continuation, new-branch work and
  commit/push after every result-bearing execution unit.

## Correction History

- 2026-08-30: Initial Phase 065 detailed plan created after direct recovery of
  both master plans, the Phase 064 closure state, the frozen Phase 056 manifest
  slice and the v1.0.24 supplemental process records.
- 2026-08-30: Recorded indices as both zero-based `826–1086` and one-based
  ordinals `827–1087` to prevent the prior index/ordinal ambiguity from
  recurring.
- 2026-08-30: Bound v1.0.24.1 as a 130-blob exact mirror plus one archive note,
  not an independent validation corpus.
- 2026-08-30: Split Step 75 into disposition and final-gate units while
  preserving Phase 066's cumulative Step 76 start.
