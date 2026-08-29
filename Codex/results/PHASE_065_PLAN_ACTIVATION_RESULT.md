# Phase 065 v1.0.24–v1.0.24.1 Lineage Reaudit Plan Activation Result

Date: 2026-08-30
Phase: `065`
Unit: detailed-plan activation before cumulative Step 70
Status: `PASS_PENDING_PERSISTENCE`
Gate: `PASS_P065_PLAN_ACTIVATION`
Persistence terminal: `PASS_P065_PLAN_ACTIVATION_PERSISTENCE`
Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`
Expected parent: `60ec2d2ad08a029224b86ddc3dcf6ff718c6d310`
Expected subject: `docs(phase065): plan v1024 lineage reaudit`
Plan: `Codex/plans/2026-08-30-phase065-v1024-v1024_1-lineage-detailed-plan.md`
Validation: `Codex/results/PHASE_065_PLAN_ACTIVATION_VALIDATION.json`

## 1. Outcome

The Phase 065 detailed plan is saved and the activation gate is selected at
precommit. The plan preserves cumulative Steps 70–75 and executes them as
`70`, `71`, `72`, `73`, `74`, `75.1`, and `75.2`. Step 70 remains barred until
this exact-seven unit is committed, pushed and persistence-verified on both
supported Python runtimes.

The activation authorizes only the v1.0.24/v1.0.24.1 lineage reaudit. It does
not authorize a production-code edit, canonical model selection, external
scientific/material/experimental validation, final manuscript prose or final
LaTeX/PDF production.

## 2. Git and Protection Preconditions

Direct checks before authoring established:

- active branch `codex/anode-fit-v1025_2-canonical-completion`;
- local HEAD, upstream, tracking and live active tip all
  `60ec2d2ad08a029224b86ddc3dcf6ff718c6d310`;
- parent of that tip `ec1fb2eda54feb35cd6c15d2ab15f2478b26fc6d`;
- parent subject `audit(phase064): close v1023 lineage gate`;
- protected local/tracking/live tip
  `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`;
- main tracking/live tip
  `4069cb36a8a52b1b88c29d68aa54dcbe915b1618` and local `main` absent;
- frozen Claude baseline
  `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`;
- clean index/worktree before plan authoring and no `Claude/**` change.

Phase 064 is now reconciled as persisted `CONDITIONAL_P064`, with exact-eight
commit `60ec2d2...` and `PASS_P064_STEP69_2_PERSISTENCE`. The Ref. 7 original
full-text debt remains `GROUND_NOT_FOUND` under
`PHASE-071-PRIMARY-SOURCE-ACQUISITION`; this activation does not close it.

## 3. Recovery and Direct-read Coverage

The controller directly reread the following authoritative recovery surfaces
from line 1 through end in this logical continuation:

- canonical completion master plan, 665 lines;
- machine master plan, 148 lines;
- inherited full-lineage master plan, 520 lines;
- Phase 064 detailed plan, 586 lines;
- Phase 064 activation result, 179 lines;
- Phase 064 result, 62 lines;
- parent execution ledger, 49 lines before this activation edit;
- canonical execution ledger, 125 lines before this activation edit;
- active handover recovery tail and exact current-state sections, with the
  complete 370-line file independently read by records and validator reviewers.

Independent reviewers additionally full-read the project rules, planning
guide, both master-plan JSON snapshots, Phase 063/064 activation validators and
artifacts, all six anchor supplemental records, the Phase 057 v1.0.24 read map,
the v1.0.24 production source/tests/helpers, and the selected source/process
partitions documented in their reports. No reviewer edited, staged, committed
or pushed any repository path.

The two master-plan JSON files are treated as immutable Phase 059 planning
snapshots. Their old live-position fields are not used to override the Markdown
ledgers or active handover.

## 4. Frozen Release Denominator

The controller independently reconstructed the target slice from
`PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json` at frozen baseline
`3b5fd059...`.

| Measure | Result |
|---|---:|
| Zero-based manifest indices | `826–1086` |
| One-based occurrence ordinals | `827–1087` |
| Occurrences/paths | `261/261` |
| v1.0.24 / v1.0.24.1 occurrences | `130 / 131` |
| Unique Git blobs | `131` |
| Occurrence bytes | `15,622,368` |
| Unique-blob bytes | `7,812,647` |
| Text occurrence / lines | `249 / 43,196` |
| Unique text blob / lines | `125 / 21,618` |
| PDF occurrence / pages | `6 / 296` |
| Unique PDF blob / pages | `3 / 148` |
| Image occurrence / unique blob | `6 / 3` |

All 130 relative paths shared by v1.0.24 and v1.0.24.1 have identical Git
blobs. The only v1.0.24.1-only path is `ARCHIVE_NOTE.md`. Therefore v1.0.24.1
is a mirror/archive snapshot, not an independent scientific or runtime
corroboration corpus.

The plan records exact, algorithm-labelled path-set, path/blob and unique-blob
SHA-256 values. It also records that the `.json`-suffixed snapshot is a 37-byte
plain-text pointer rather than JSON, so Step 70 will route it by observed bytes.

## 5. Complete Process and Evidence Denominator

The initial six supplemental anchors total 728 lines but are not treated as the
complete work history. Independent review expanded the mandatory plan contract
to:

- three v1.0.24 plans, 639 lines;
- 29 root result/process documents, 2,068 lines;
- 31 `comp_v24` Markdown documents, 2,635 lines;
- Phase 057 read map and ten v1.0.24 observation documents, 1,890 lines;
- minimum narrative history `74 documents / 7,232 lines`;
- remaining `comp_v24` evidence `95 files`: 62 text/data/code files with
  49,956 lines and 33 PNGs;
- release-tree history `38 commits`;
- routed release/plan/result/`comp_v24` union `98 commits`.

Step 70 must read the entire narrative denominator, inventory and route the
remaining evidence, inspect both commit universes, and produce interval-level
attestation. The release manifest and process evidence are separate
denominators and cannot be double-counted.

## 6. Scientific and Citation Boundary

The plan makes the following high-risk questions explicit without deciding
them at activation:

- homogeneous regular solution, binodal/common-tangent equilibrium and
  observation broadening are separate mathematical objects;
- local center curvature is not a global full width at half maximum law;
- stage-2L entropy/merger values and feature locations may be internal seeds,
  not data-derived material truth;
- LCO electronic-entropy default records conflict and require fresh isolated
  runtime observation;
- the seconds/hour factor must be tested numerically because a comment is not a
  repair;
- shared-voltage additive hosts do not prove a material-specific common-host
  topology;
- fitted interaction parameters, peaks and gallery basis functions do not
  establish phase/species identity;
- public pOCV fits are calibration evidence until protocol, capacity basis and
  held-out reconstruction establish more.

Step 72 must also census all 90 TeX blobs: bibliography items `95` occurrences/
`93` unique keys, citations `561` occurrences/`95` unique keys, and DOI strings
`91` occurrences/`85` unique values. Adopted master closure `56 TeX / 8,218
lines` is separated from non-master candidates/orphans `34 / 4,489`. Undefined
candidate-only keys are not silently promoted into adopted-source defects, and
no DOI or proposition support may be fabricated.

## 7. Runtime Gate Separation

The sole inherited Phase 065 gate requires independent observation of:

1. fresh import;
2. explicit profile;
3. legacy restoration.

The source does not yet establish what exact object the master plan meant by
`explicit profile`, and an initial science review found no demonstrated profile
registry or saved-state restoration loader in the frozen production source.
Step 71 must first freeze exact symbols, constructors, input state and restore
keys. Step 73 may then return only `IMPLEMENTED_AND_OBSERVED`,
`ABSENT_IN_FROZEN_SOURCE`, or `GROUND_NOT_FOUND` for each separate route.
Absence is an honest audit result but is not a passing behavior route. No name
or loader may be invented to make the gate pass.

Each route must run in its own isolated process on Python 3.12 and 3.14, include
route-specific mutation probes, and execute in changed orders to detect leaked
mutable global/module state.

## 8. Exact Execution Contract

The detailed plan fixes these units:

| Unit | Purpose |
|---|---|
| Step 70 | source/process topology and complete-read attestation |
| Step 71 | code/profile/default static audit |
| Step 72 | skew/material-decomposition derivation and authority audit |
| Step 73 | three-route isolated runtime audit |
| Step 74 | document/code/guide conformance audit |
| Step 75.1 | complete source disposition and carry-forward delta |
| Step 75.2 | integrated validation, Lineage Report H and final gate |

Each unit has an exact seven- or eight-path allowlist, result-first/JSON-last
ordering, independent review, exact commit subject, push and persistence gate.
The final gate is exactly one of `PASS_P065_LINEAGE_H`, `CONDITIONAL_P065`, or
`FAIL_P065`.

## 9. Validator-first RED Evidence

Before `PHASE_065_PLAN_ACTIVATION_VALIDATION.json` existed, the controller ran:

```text
py -3.12 -B -X utf8 Codex/work/v1024_phase065/validate_phase065_plan.py --content-only
```

Observed terminal and exit state:

```text
FAIL_P065_PLAN_CONTENT E_VALIDATION_ARTIFACT_MISSING: ...PHASE_065_PLAN_ACTIVATION_VALIDATION.json
EXIT=1
```

This proves that the machine artifact cannot be omitted and that collection is
not being used as a substitute for the human result-first surfaces.

## 10. Precommit Validation Contract

The activation validator requires:

- frozen manifest and both 38/98-commit process identities;
- all six supplemental anchor identities and line extents;
- plan heading/order/token/cumulative-numbering controls;
- hard-pinned plan, validator and four control-document hashes;
- strict JSON duplicate/nonfinite/overflow/truncation rejection and full
  recursive traversal;
- named semantic negative controls;
- validator source-policy attacks;
- real disposable-Git negative controls;
- `--no-renames` exact A/M status maps, not path-only diffs;
- active/upstream/tracking/live equality;
- protected local/tracking/live equality;
- local-main absence and main tracking/live equality;
- baseline/parent/working-tree `Claude/**` non-change;
- exact index/worktree and commit/worktree blob equality;
- deterministic double reconstruction;
- Python 3.12/3.14 staged and persistence validation.

The activation's independent plan reviews initially reported P0/P1/P2 as
`0/3/2`, `0/1/1`, and `0/2/3`. The P1 findings were design findings, not source
mutations: stale Phase 064 precommit pointers, occurrence/blob denominator
confusion, unresolved meaning of explicit profile, rename-aware Git status and
an incomplete process/citation denominator. The current plan and validator
incorporate their required corrections. Final independent review must rerun
against the collected, staged exact-seven unit and return no P0 or P1 before
commit.

The first final validator review then found one additional blocking P1: the
source-policy checker rejected direct `eval`/`os.system` but did not confine
generic child execution, callable aliases, dynamic attribute access or
filesystem mutators to their intended call sites. Commit remained blocked. The
validator now permits `subprocess.run` only in the unique process wrapper,
permits that wrapper only behind Git, rejects direct/aliased/`Popen`/`getattr`
execution escapes, and permits file mutation only inside the atomic JSON-last
collector or boundary-checked disposable Git fixtures. A subsequent read-only
adversarial review found four further routes: a top-level function borrowing the
nested cleanup callback name, an unchecked `git_blob` caller, a `tempfile`
constructor, and `os.symlink`. The current policy therefore uses qualified
function ownership, pins every privileged Git caller, confines sensitive module
objects, and rejects additional metadata/archive/dynamic-attribute mutations.
A later frozen-candidate review found builtin-function laundering,
`__builtins__`/function-reflection access, nested sensitive-module attributes,
and unlisted process-launch APIs. The policy now rejects forbidden builtin
names on every load, confines each sensitive module to its exact observed
attribute surface for every imported module, qualifies owners through nested
class/function scopes, and blocks unapproved dunder, module-loader and frame
introspection. Sixty-four
AST-only source-policy negative probes must all reject without executing the
injected payload before the final sign-off can supersede those P1 findings.

The first final science review also caught an origin-label error in the plan:
the @3 regular-solution kernel was described as a graphite feature even though
the frozen source/intent route is general and Si-focused, while graphite @5
uses interaction parameters without thereby proving a `kernel='regsol'` route.
The plan now requires Step 71 to trace every actually reachable @3 material
route and keeps @3, graphite @5 and the optional six-gallery basis separate.

## 11. Exact Activation Unit

The only permitted paths are:

1. `Codex/plans/2026-08-30-phase065-v1024-v1024_1-lineage-detailed-plan.md`
2. `Codex/work/v1024_phase065/validate_phase065_plan.py`
3. `Codex/results/PHASE_065_PLAN_ACTIVATION_VALIDATION.json`
4. `Codex/results/PHASE_065_PLAN_ACTIVATION_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Expected statuses are `A/A/A/A/M/M/M`; renames are forbidden.

## 12. Confirmed, Unverified and Ground Not Found

### Confirmed

- Phase 064 persistence terminal and exact parent state.
- Frozen 261-occurrence/131-blob release topology and mirror boundary.
- Six anchor supplemental identities.
- 38 release-tree and 98 routed-union commit identities.
- Cumulative Phase 065 step range and exact runtime-route separation rule.
- No source or code modification is authorized in this activation.

### Unverified / not promoted

- exact profile/default/restore symbol mapping before Step 71;
- external material or experimental validity;
- fitted-component phase/gallery/species identity;
- independent held-out validation;
- final model, equation family, defaults or publication readiness.

### Ground not found

- Ref. 7 original full text remains `GROUND_NOT_FOUND`;
- any profile registry or saved-state restoration route absent from the frozen
  static census must remain `ABSENT_IN_FROZEN_SOURCE` or `GROUND_NOT_FOUND`;
- unavailable primary proposition/page/equation support remains acquisition
  debt rather than inferred evidence.

## 13. Gate and Exact Next Condition

`PASS_P065_PLAN_ACTIVATION` is selected at precommit. The record intentionally
does not claim its own future containing hash. Stage exactly the seven declared
paths, run dual-runtime staged validation and final independent reviews, commit
with the exact parent and subject, push, fetch, and verify exact refs/status/
paths/blobs/protection/cleanliness on both runtimes.

Only `PASS_P065_PLAN_ACTIVATION_PERSISTENCE` releases Step 70. No Step 70 source
artifact or implementation file may enter this activation commit.
