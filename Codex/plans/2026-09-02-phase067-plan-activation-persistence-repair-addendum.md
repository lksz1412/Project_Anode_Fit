# Phase 067 Plan Activation Persistence Repair Addendum Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to execute this repair in the current isolated worktree. Preserve the original activation commit and its artifacts as historical evidence; this addendum creates a separate exact-seven repair transaction.

**Goal:** Repair the Phase 067 activation persistence proof without rewriting the valid activation commit or beginning cumulative Step 82.

**Architecture:** The repair validator addresses two identities independently. The original activation certificate is read from commit `7e5529658ef15443df7e8bea6f8aefaa081f0d2d` and its parent-addressed Git objects, while the repair transaction is checked against the current branch, index/worktree, and eventual child commit. Fixed predecessor evidence therefore never requires the current HEAD to equal the activation commit's predecessor.

**Tech Stack:** Git object database and read-only plumbing, Python 3.12 and 3.14 standard library, deterministic strict JSON, repository-local Markdown records, atomic JSON-last collection.

---

Date: 2026-09-02

Status: `ACTIVE_REPAIR_PENDING_PERSISTENCE`

Affected phase: `067`

Repair unit: Phase 067 detailed-plan activation persistence repair before cumulative Step 82

Original activation commit: `7e5529658ef15443df7e8bea6f8aefaa081f0d2d`

Repair expected parent: `7e5529658ef15443df7e8bea6f8aefaa081f0d2d`

Repair expected subject: `fix(phase067): repair activation persistence proof`

Content Gate: `PASS_P067_ACTIVATION_REPAIR`

Persistence terminal: `PASS_P067_PLAN_ACTIVATION_PERSISTENCE_REPAIR`

Execution ledgers:

- `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
- `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`

Recovery handover: `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

## Summary

Phase 067 activation content was committed and pushed on exact-seven commit
`7e5529658ef15443df7e8bea6f8aefaa081f0d2d`, but the original validator could
not produce its postcommit terminal. The activation content is not being
rewritten or invalidated. This addendum repairs only the persistence proof and
keeps cumulative Step 82 blocked until the new repair transaction is committed,
pushed, and verified under Python 3.12 and Python 3.14.

The repair must make the original activation commit a fixed, commit-addressed
certificate. It must separately make the current branch/index/worktree or future
repair commit the repair transaction. No check may substitute one identity for
the other.

## Current Ground Truth

### Directly reproduced failure

Both commands fail at the same diagnostic while HEAD is the activation commit:

```powershell
py -3.12 -B Codex/work/v1010_v1025_2_reaudit/validate_phase067_plan.py --verify-persistence --expected-commit 7e5529658ef15443df7e8bea6f8aefaa081f0d2d
py -3.14 -B Codex/work/v1010_v1025_2_reaudit/validate_phase067_plan.py --verify-persistence --expected-commit 7e5529658ef15443df7e8bea6f8aefaa081f0d2d
```

Observed result on both runtimes:

```text
FAIL_P067_PLAN_CONTENT E_REPOSITORY_HEAD: E_REPOSITORY_HEAD
```

For each runtime, the exact argv uses that runtime's `py -3.12` or `py -3.14`
selector followed by `-B`, the original validator path, and
`--verify-persistence --expected-commit 7e5529658ef15443df7e8bea6f8aefaa081f0d2d`.
Entry HEAD was `7e5529658ef15443df7e8bea6f8aefaa081f0d2d`; return code was `1`;
stdout was exactly `61` bytes with SHA-256
`3aff633deb85e468551238987ded68176ce1b12e641e6487a9d71f9ba3b50140`;
stderr was exactly `0` bytes with SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

### Root cause

The original postcommit path reconstructs the ordinary activation payload, then
calls `predecessor_contract()`, which calls
`repository_snapshot(EXPECTED_PARENT)`. In that validator `EXPECTED_PARENT` is
the Phase 066 closing commit
`7241b331ff76bc8d43cb1bc6b69634977e0884a0`. During valid Phase 067 activation
persistence, current HEAD is instead the activation commit
`7e5529658ef15443df7e8bea6f8aefaa081f0d2d`. The check therefore conflates a
fixed predecessor certificate with the current repository tip and necessarily
raises `E_REPOSITORY_HEAD`.

The old activation commit remains exact-seven, single-parented, correctly
subjected, pushed, and live-remote equal. What is absent is only the original
dual-runtime persistence terminal. The old validator and every original
activation artifact remain immutable historical evidence.

### Original activation identity

- commit: `7e5529658ef15443df7e8bea6f8aefaa081f0d2d`
- single parent: `7241b331ff76bc8d43cb1bc6b69634977e0884a0`
- subject: `docs(phase067): plan code test fitting cross-audit`
- status in exact path order: `A/A/A/A/M/M/M`
- mode for every path: `100644`
- active branch/upstream/live origin at repair start: all equal to the activation commit
- original activation content Gate: `PASS_P067_PLAN_ACTIVATION`
- original intended terminal: `PASS_P067_PLAN_ACTIVATION_PERSISTENCE`
- original terminal outcome: not obtained because of the reproduced validator defect

Fixed committed LF SHA-256 evidence:

| Original activation artifact | SHA-256 |
|---|---|
| `Codex/plans/2026-09-01-phase067-code-test-fitting-cross-audit-detailed-plan.md` | `a1ab5865581da95d71a86e5e6763f66ab0a4b42470d9fc00171355994e49ebf7` |
| `Codex/work/v1010_v1025_2_reaudit/validate_phase067_plan.py` | `d12577840a66db8e28fd2d94fe53a2c7277c496fccbc947ad83a66e8688b0949` |
| `Codex/results/PHASE_067_PLAN_ACTIVATION_VALIDATION.json` raw | `b178b7bc25dfe9be9eaf478c9760702d240fb686ba393327c96dc048c463e15a` |
| same JSON semantic | `b3a3ea02404db412dc55e8182b42f726837b6e652540abe15e82a951fddc77a3` |
| `Codex/results/PHASE_067_PLAN_ACTIVATION_RESULT.md` | `7bc7aad461247650e0bb2b4c170202420eed4367bcf875fa9dc1e9af7a497ce7` |

The three original control-record blobs are derived directly from the activation
commit tree and sealed into the repair JSON; no working-tree copy is accepted as
a substitute.

## Phase Range

| Execution unit | Scope | Terminal required |
|---|---|---|
| Phase 067 activation persistence repair | Preserve original activation, validate its commit-addressed certificate, persist a separate exact-seven repair | `PASS_P067_PLAN_ACTIVATION_PERSISTENCE_REPAIR` on Python 3.12 and 3.14 |
| Cumulative Step 82 | unchanged and blocked | may begin only after the repair terminal is observed on both runtimes |

This addendum creates no new cumulative Step number. It is a repair boundary
between activation and Step 82.

## Non-goals and Scope Guard

- Do not modify the original Phase 067 plan, validator, JSON, or result.
- Do not amend, replace, rebase, or reinterpret activation commit `7e552965...`.
- Do not modify `Claude/**`, production Python, LaTeX, bibliography, figures,
  PDFs, data, protected branch, or `main`.
- Do not begin any portion of Steps 82–90.2.
- Do not rerun historical optimizer or fitting work.
- Do not promote scientific, held-out, external, material, Ref. 7, optimizer,
  stale-PDF, canonical-manuscript, or publication authority.
- Do not claim the repair persistence terminal before its child commit exists,
  is pushed, live-remote equal, clean, and passes both runtimes.
- Do not add fallback paths, generic execution helpers, or unrelated source
  policy. The validator needs only its exact read-only Git calls and the atomic
  collect writer.

## Implementation Changes

The repair transaction contains exactly these seven paths in this order:

1. A `Codex/plans/2026-09-02-phase067-plan-activation-persistence-repair-addendum.md`
2. A `Codex/work/v1010_v1025_2_reaudit/validate_phase067_activation_persistence_repair.py`
3. A `Codex/results/PHASE_067_PLAN_ACTIVATION_PERSISTENCE_REPAIR_VALIDATION.json`
4. A `Codex/results/PHASE_067_PLAN_ACTIVATION_PERSISTENCE_REPAIR_RESULT.md`
5. M `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. M `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. M `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required ordered status is exactly `A/A/A/A/M/M/M`; all modes are `100644`.
Rename, copy, deletion, extra path, mode drift, or `Claude/**` difference fails.

## Repair Execution Tasks

### Task 1 — Freeze the addendum before implementation

**Files:**

- Create: `Codex/plans/2026-09-02-phase067-plan-activation-persistence-repair-addendum.md`

- [x] **Record the reproduced dual-runtime failure and exact root cause.**
- [x] **Separate original activation certificate identity from repair transaction identity.**
- [x] **Freeze the exact-seven path/status/mode/subject/gate/terminal contract.**
- [x] **Keep Step 82 explicitly blocked.**

Gate: this plan is the first changed path. Validator/result/control-record edits
must not begin before this file exists.

### Task 2 — RED: prove the repair behavior is absent

**Files:**

- Create later: `Codex/work/v1010_v1025_2_reaudit/validate_phase067_activation_persistence_repair.py`

- [ ] **Verify the new validator path is absent.**
- [ ] **Run both old persistence commands and retain the exact `E_REPOSITORY_HEAD` failure.**
- [ ] **Confirm the working tree contains only this addendum before validator implementation.**

Expected RED: the new validator cannot yet produce
`PASS_P067_ACTIVATION_REPAIR`; the old validator fails exactly as documented.

### Task 3 — Implement the independent original activation certificate

**Files:**

- Create: `Codex/work/v1010_v1025_2_reaudit/validate_phase067_activation_persistence_repair.py`

- [ ] **Validate original activation commit genealogy.** Require the exact commit,
  exactly one `%P` parent equal to `7241b331...`, and exact subject.
- [ ] **Validate original exact-seven status and order.** Require the seven original
  paths and `A/A/A/A/M/M/M` without rename/copy/delete/extra paths.
- [ ] **Read modes and bytes from `7e552965...` directly.** Require seven `100644`
  entries, recompute every committed LF SHA-256 and Git blob identity, and compare
  the four fixed hashes above. Derive ledger/handover hashes from the commit.
- [ ] **Strict-parse the committed original JSON.** Reject duplicate keys,
  non-finite values, BOM, CR, missing terminal newline, raw-hash drift, semantic-hash
  drift, wrong Gate, or wrong precommit boundary.
- [ ] **Prove the regression boundary.** The predecessor certificate must pass when
  repository HEAD is `7e552965...`; a named old-conflation control must demonstrate
  that requiring current HEAD `7241b331...` is the rejected behavior.

Gate: `original_activation_certificate.valid=true` is based only on commit-addressed
objects and does not inspect current HEAD for Phase 066 equality.

### Task 4 — Implement repair precommit modes

**Files:**

- Create/complete: `Codex/work/v1010_v1025_2_reaudit/validate_phase067_activation_persistence_repair.py`
- Create later by collect only: `Codex/results/PHASE_067_PLAN_ACTIVATION_PERSISTENCE_REPAIR_VALIDATION.json`

- [ ] **Implement `--collect`.** Require current HEAD/upstream/live origin equal
  `7e552965...`, exact nonself repair worktree paths, clean index, no extra path,
  correct modes, immutable original artifacts, protected/main/Claude boundaries,
  deterministic two-pass reconstruction, and absent output. Write the JSON once,
  atomically, as the last path; refuse overwrite with an exact diagnostic.
- [ ] **Implement `--content-only`.** Validate the existing exact-seven worktree
  snapshot and machine JSON without mutation; require JSON bytes to equal a fresh
  deterministic reconstruction.
- [ ] **Implement `--verify-staged`.** Require the exact-seven paths staged in order
  with `A/A/A/A/M/M/M`, index modes `100644`, index bytes equal reviewed worktree
  bytes, no unstaged drift, current refs still at activation, and terminal snapshot
  equality before returning `PASS_P067_ACTIVATION_REPAIR`.
- [ ] **Seal read-only Git argv.** Allow only the exact argument shapes actually
  used for `branch --show-current`, `diff`, `diff-tree`, `ls-files`, `ls-remote`,
  `ls-tree`, `remote get-url`, `rev-parse`, `show`, `show-ref`, and `status`.
  Reject every unknown subcommand, mutable option, or output-writing option.
- [ ] **Restrict mutation.** Outside the single collect writer, reject process,
  network, filesystem mutation, dynamic evaluation/import, and arbitrary callback
  execution. Collection permits only one temporary same-directory write followed
  by `os.replace`, with failure cleanup.

Gate: Python 3.12 performs the sole successful `--collect` JSON-last write.
Python 3.12 and 3.14 must then both select `PASS_P067_ACTIVATION_REPAIR` in
`--content-only`. Python 3.14 must not perform a second successful collection;
any later `--collect` invocation is only the expected overwrite-refusal probe.
This is precommit evidence and does not claim the persistence terminal.

### Task 5 — Implement repair persistence mode

**Files:**

- Complete: `Codex/work/v1010_v1025_2_reaudit/validate_phase067_activation_persistence_repair.py`

- [ ] **Validate `--expected-commit` before Git use.** Require lowercase 40-hex and
  accept it only with `--verify-persistence`.
- [ ] **Bind the repair child commit.** Require exactly one parent equal to
  `7e552965...`, exact subject `fix(phase067): repair activation persistence proof`,
  exact-seven path/status/order/modes, and committed bytes equal the reviewed repair
  snapshot recorded in the canonical JSON.
- [ ] **Bind repository refs independently.** Require local HEAD, upstream/tracking,
  and live origin all equal the supplied repair commit; require the expected origin
  URL, clean index/worktree, local `main` absent, and protected/main tips unchanged.
- [ ] **Bind protected content.** Require no `Claude/**` difference from activation
  to repair commit and no frozen `Claude/**` difference from baseline
  `3b5fd059...`; preserve protected/main objects exactly.
- [ ] **Recheck terminal transaction snapshot.** After all semantic/path/blob checks,
  re-read refs, status, modes, index/worktree bytes, original immutable artifact
  hashes, and exact inputs; require equality with the entry seal before returning.

Terminal: only this mode may print
`PASS_P067_PLAN_ACTIVATION_PERSISTENCE_REPAIR`.

### Task 6 — Add real negative and determinism controls

**Files:**

- Complete: `Codex/work/v1010_v1025_2_reaudit/validate_phase067_activation_persistence_repair.py`

- [ ] **Original-certificate controls:** old HEAD/predecessor conflation, activation
  parent drift, subject drift, path drift, mode drift, blob drift.
- [ ] **Repair-transaction controls:** parent drift, subject drift, extra/missing/
  reordered/renamed path, mode drift, blob drift, local/upstream/live ref drift,
  protected/main drift, dirty worktree/index, Claude drift.
- [ ] **JSON controls:** duplicate key, NaN/Infinity, BOM/CR/no terminal newline,
  semantic drift, raw drift, overwrite refusal.
- [ ] **Argument controls:** missing/malformed persistence commit, unexpected commit
  outside persistence mode, mutable/unknown Git argv.
- [ ] **Determinism:** reconstruct the payload twice and require byte identity.

Each negative case must execute the real predicate with one mutation and match one
named diagnostic. Literal precomputed pass counts are forbidden.

### Task 7 — Save result and supersession records

**Files:**

- Create: `Codex/results/PHASE_067_PLAN_ACTIVATION_PERSISTENCE_REPAIR_RESULT.md`
- Modify: `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
- Modify: `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
- Modify: `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

- [ ] **Record the original activation as committed/pushed/live valid but without its
  intended original persistence terminal.** Preserve the exact diagnostic and cause.
- [ ] **Mark the repair current status `PASS_PENDING_PERSISTENCE`.** Use content Gate
  `PASS_P067_ACTIVATION_REPAIR`; containing repair commit remains
  `PENDING_AT_PRECOMMIT_BY_DESIGN`.
- [ ] **Supersede only the persistence route.** Never rewrite the original activation
  decision or imply the original validator passed postcommit.
- [ ] **Keep Step 82 blocked.** Release it only after the same repair child commit is
  pushed/live-remote equal, the worktree is clean, independent review has
  P0/P1=`0/0`, and Python 3.12 and 3.14 both return
  `PASS_P067_PLAN_ACTIVATION_PERSISTENCE_REPAIR` for that identical child OID.
- [ ] **Update handover top and bottom pointers.** Point to this addendum, repair
  result, repair JSON, validator, both ledgers, and exact next action.

Gate: the three recovery records agree on activation commit, failure, repair
status, expected parent/subject, and Step 82 boundary.

### Task 8 — JSON-last collection and precommit verification

**Files:**

- Create last: `Codex/results/PHASE_067_PLAN_ACTIVATION_PERSISTENCE_REPAIR_VALIDATION.json`

- [ ] **Confirm the output path is absent.** Collection must refuse an existing file.
- [ ] **Run `--collect` under Python 3.12.** Require an atomic JSON-last write.
- [ ] **Run `--content-only` under Python 3.12 and 3.14.** Both must select the content
  Gate and agree on raw/semantic hashes and all actual control counts.
- [ ] **Compile with no bytecode write under Python 3.12 and 3.14.** Use `compile()`
  on source bytes or `PYTHONDONTWRITEBYTECODE=1`; do not create an eighth path.
- [ ] **Run overwrite-refusal probe.** A second `--collect` must fail at the exact
  overwrite diagnostic and leave JSON bytes unchanged.
- [ ] **Run `git diff --check`, exact-seven status/order/mode checks, HEAD/upstream/live
  checks, and `git status --short -- Claude`.** All must match this plan.

Precommit stop: stage, commit, and push are controller-only actions and are not
performed by this implementation unit.

### Task 9 — Controller-only persistence completion

**Files:** exact-seven repair set above, no additional path.

- [ ] **Independent review P0/P1/P2=`0/0/0`.** Any P0 or P1 requires repair and full
  re-review before staging.
- [ ] **Stage exact-seven and run `--verify-staged` on both runtimes.** Require
  `PASS_P067_ACTIVATION_REPAIR`.
- [ ] **Commit exactly once.** Parent must be `7e552965...`; subject must be
  `fix(phase067): repair activation persistence proof`.
- [ ] **Push and verify live origin.** Local HEAD, upstream/tracking, and live origin
  must equal the new child commit.
- [ ] **Run `--verify-persistence --expected-commit <child>` on Python 3.12 and 3.14.**
  Both must return `PASS_P067_PLAN_ACTIVATION_PERSISTENCE_REPAIR`.
- [ ] **Only then release cumulative Step 82.** Both runtimes must name the same
  child OID, which must already be pushed/live equal with a clean tree and
  independent P0/P1=`0/0`.

## Implementation Interfaces

### CLI contract

```text
validate_phase067_activation_persistence_repair.py
  (--collect | --content-only | --verify-staged | --verify-persistence)
  [--expected-commit <lowercase-40-hex>]
```

Exactly one mode is required. `--expected-commit` is required only for
`--verify-persistence` and forbidden otherwise.

### JSON top-level contract

```json
{
  "content_gate": "PASS_P067_ACTIVATION_REPAIR",
  "generated_date": "2026-09-02",
  "original_activation_certificate": {},
  "repair_transaction": {},
  "root_cause": {},
  "negative_contract": {},
  "determinism": {},
  "persistence_terminal": "PASS_P067_PLAN_ACTIVATION_PERSISTENCE_REPAIR",
  "precommit_status": "PASS_PENDING_PERSISTENCE",
  "schema": "phase067-activation-persistence-repair-v1"
}
```

The JSON records the future terminal as a contract string only. It must not state
that staged or persistence verification has already run. It contains the exact
seven repair paths, ordered status and modes, plus hashes for exactly the six
non-JSON paths. It must not contain its own raw SHA-256 or any future child commit
OID. Persistence binds the child JSON blob to the strict stored raw bytes and a
fresh deterministic reconstruction, then binds the other six committed blobs to
the six recorded nonself hashes.

## Test Plan

1. Reproduce original Python 3.12/3.14 `E_REPOSITORY_HEAD` failure.
2. Run real original-certificate and repair-transaction negative mutations with
   exact diagnostics.
3. Verify two deterministic payload reconstructions and strict JSON round-trip.
4. Collect JSON exactly once, last, then verify overwrite refusal.
5. Run content-only and compile checks under Python 3.12 and 3.14.
6. Verify exact-seven `A/A/A/A/M/M/M`, `100644`, no rename/delete/extra path,
   correct current refs, and zero `Claude/**` changes.
7. Leave staged and persistence modes unclaimed until controller execution.

## Stopping Conditions

Stop without persistence claim if any of the following occurs:

- activation commit genealogy, original fixed hash, exact-seven tree, or live
  origin differs from the frozen contract;
- protected/main/Claude content or ref drift is observed;
- a repair path is missing, extra, renamed, deleted, reordered, or non-`100644`;
- Python 3.12 and 3.14 disagree;
- deterministic reconstruction differs;
- JSON already exists before intended collection or changes after refusal;
- independent review reports P0 or P1;
- credentials or remote authority not already available are required.

## Assumptions

- Git object `7e552965...` remains locally available and live at the tracked origin.
- Python 3.12 and 3.14 remain available via the Windows `py` launcher.
- The controller, not this implementation worker, performs stage/commit/push.
- Existing activation artifacts are historical evidence and remain byte-for-byte
  immutable even though their original persistence route is defective.

## Correction History

- 2026-09-02: Created this addendum after directly reproducing dual-runtime
  `E_REPOSITORY_HEAD`. It supersedes only the Phase 067 activation persistence
  mechanism, not the activation content, commit, or Phase 066 evidence.
