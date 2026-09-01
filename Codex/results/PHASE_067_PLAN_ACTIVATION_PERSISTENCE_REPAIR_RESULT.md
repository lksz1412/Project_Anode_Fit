# Phase 067 Plan Activation Persistence Repair Result

Date: 2026-09-02

Phase: `067`

Unit: activation persistence repair before cumulative Step 82

Status: `PASS_PENDING_PERSISTENCE`

Selected content Gate: `PASS_P067_ACTIVATION_REPAIR`

Persistence terminal contract: `PASS_P067_PLAN_ACTIVATION_PERSISTENCE_REPAIR`

Containing repair commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

Repair expected parent: `7e5529658ef15443df7e8bea6f8aefaa081f0d2d`

Repair expected subject: `fix(phase067): repair activation persistence proof`

Addendum plan: `Codex/plans/2026-09-02-phase067-plan-activation-persistence-repair-addendum.md`

Validator: `Codex/work/v1010_v1025_2_reaudit/validate_phase067_activation_persistence_repair.py`

Machine validation: `Codex/results/PHASE_067_PLAN_ACTIVATION_PERSISTENCE_REPAIR_VALIDATION.json`

## Result

The original Phase 067 activation commit is retained as a valid, exact-seven,
pushed and live-remote checkpoint. Its content Gate
`PASS_P067_PLAN_ACTIVATION` is not withdrawn. Its original validator did not,
however, obtain `PASS_P067_PLAN_ACTIVATION_PERSISTENCE`. This result activates a
separate repair transaction for that missing proof and does not start Step 82.

The repair content Gate is `PASS_P067_ACTIVATION_REPAIR`. The current record is a
precommit contract only. It does not claim that the repair validator has run,
that either Python runtime has passed, that the exact-seven paths are staged, or
that a repair commit/push/persistence terminal exists.

## Directly Confirmed Original Failure

With local HEAD, upstream/tracking and live origin all at activation commit
`7e5529658ef15443df7e8bea6f8aefaa081f0d2d`, the original command was executed
under both available runtimes:

```powershell
py -3.12 -B Codex/work/v1010_v1025_2_reaudit/validate_phase067_plan.py --verify-persistence --expected-commit 7e5529658ef15443df7e8bea6f8aefaa081f0d2d
py -3.14 -B Codex/work/v1010_v1025_2_reaudit/validate_phase067_plan.py --verify-persistence --expected-commit 7e5529658ef15443df7e8bea6f8aefaa081f0d2d
```

Both returned exit 1 and exactly:

```text
FAIL_P067_PLAN_CONTENT E_REPOSITORY_HEAD: E_REPOSITORY_HEAD
```

For each runtime the exact argv was its `py -3.12` or `py -3.14` selector,
`-B`, the original validator path, and
`--verify-persistence --expected-commit 7e5529658ef15443df7e8bea6f8aefaa081f0d2d`.
Entry HEAD was the same activation OID; return code was `1`; stdout was `61`
bytes with SHA-256
`3aff633deb85e468551238987ded68176ce1b12e641e6487a9d71f9ba3b50140`;
stderr was `0` bytes with SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

This observation is the original validator failure, not a failure of the
activation commit's path, parent, subject, push, or live-remote identity.

## Root Cause

The original postcommit route reconstructs the activation payload and calls
`predecessor_contract()`. That function finishes by calling
`repository_snapshot(EXPECTED_PARENT)`, while its `EXPECTED_PARENT` remains the
Phase 066 closing commit
`7241b331ff76bc8d43cb1bc6b69634977e0884a0`. A valid postcommit activation
checkout instead has HEAD at `7e5529658ef15443df7e8bea6f8aefaa081f0d2d`.

The implementation therefore conflates two distinct facts:

1. the fixed Phase 066 predecessor evidence addressed by commit `7241b331...`;
2. the current repository tip addressed by activation commit `7e552965...`.

The repair validator keeps those facts independent. It validates the original
activation and its predecessor through explicit Git commit/tree/blob objects,
then validates the repair worktree/index or future repair commit through a
separate repository snapshot.

## Original Activation Certificate

| Field | Fixed value |
|---|---|
| activation commit | `7e5529658ef15443df7e8bea6f8aefaa081f0d2d` |
| single parent | `7241b331ff76bc8d43cb1bc6b69634977e0884a0` |
| subject | `docs(phase067): plan code test fitting cross-audit` |
| exact status | `A/A/A/A/M/M/M` |
| exact modes | seven times `100644` |
| original Gate | `PASS_P067_PLAN_ACTIVATION` |
| original persistence outcome | terminal not obtained; dual `E_REPOSITORY_HEAD` |
| push/live status | activation commit equals local upstream and live origin |

The repair binds all seven original paths directly from that commit. It uses
these fixed committed LF SHA-256 values for the four added content artifacts:

- plan: `a1ab5865581da95d71a86e5e6763f66ab0a4b42470d9fc00171355994e49ebf7`;
- validator: `d12577840a66db8e28fd2d94fe53a2c7277c496fccbc947ad83a66e8688b0949`;
- JSON raw: `b178b7bc25dfe9be9eaf478c9760702d240fb686ba393327c96dc048c463e15a`;
- JSON semantic: `b3a3ea02404db412dc55e8182b42f726837b6e652540abe15e82a951fddc77a3`;
- result: `7bc7aad461247650e0bb2b4c170202420eed4367bcf875fa9dc1e9af7a497ce7`.

The original ledger and handover hashes and all seven Git blob identities are
derived from the activation commit itself rather than copied from the current
modified recovery records.

## Exact-Seven Repair Set

1. A `Codex/plans/2026-09-02-phase067-plan-activation-persistence-repair-addendum.md`
2. A `Codex/work/v1010_v1025_2_reaudit/validate_phase067_activation_persistence_repair.py`
3. A `Codex/results/PHASE_067_PLAN_ACTIVATION_PERSISTENCE_REPAIR_VALIDATION.json`
4. A `Codex/results/PHASE_067_PLAN_ACTIVATION_PERSISTENCE_REPAIR_RESULT.md`
5. M `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. M `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. M `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required ordered status is exactly `A/A/A/A/M/M/M`; all seven modes are
`100644`. Rename, copy, deletion, extra path, mode drift, protected/main drift,
or any `Claude/**` difference fails the repair.

## Validation Boundary

The new validator has four mutually exclusive modes:

- `--collect`: result-first, canonical JSON-last, one atomic write, overwrite refusal;
- `--content-only`: exact-seven unstaged worktree and deterministic JSON validation;
- `--verify-staged`: exact-seven staged/index/worktree byte and mode validation;
- `--verify-persistence --expected-commit <commit>`: pushed repair child commit,
  clean tree, ref equality, exact subject/parent/path/mode/blob and terminal seal.

The fixed original activation certificate never requires current HEAD to equal
`7241b331...`. Precommit repair modes require current HEAD/upstream/live origin
to remain `7e552965...`. Persistence requires all three to equal the supplied
repair child commit, whose single parent must be `7e552965...`.

## Protected and Authority Boundary

- Protected branch `codex/lib-physics-endgame-v1025_2` remains fixed at
  `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`.
- Remote `main` remains fixed at
  `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`; local `main` remains absent.
- `Claude/**` remains unchanged from the activation commit and frozen baseline
  `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`.
- Production Python, LaTeX, bibliography, figures, PDFs, data, optimizer work,
  and fitting work are outside this repair.
- Ref. 7 original full text, original full-precision optimizer state,
  held-out/external/material/specimen/protocol evidence and stale PDFs remain open.
- No scientific, canonical-manuscript, or publication authority is promoted.

## Supersession Semantics

This result supersedes only the defective route used to prove Phase 067
activation persistence. It does not supersede or rewrite:

- activation plan content;
- activation Gate `PASS_P067_PLAN_ACTIVATION`;
- activation commit `7e552965...`;
- Phase 066 terminal `PASS_P066_STEP81_2_PERSISTENCE` or selected
  `CONDITIONAL_P066`;
- Steps 82–90.2 scope and denominators; or
- any open scientific-authority owner.

## Current Confirmed Decisions

- Original activation commit/path/parent/subject/push/live identity remains valid.
- Original dual-runtime persistence terminal was not obtained.
- The exact failure is transparently preserved as `E_REPOSITORY_HEAD`.
- Repair content Gate is `PASS_P067_ACTIVATION_REPAIR`.
- Repair status remains `PASS_PENDING_PERSISTENCE`.
- Repair containing commit remains `PENDING_AT_PRECOMMIT_BY_DESIGN`.
- Repair expected parent and subject are fixed as above.
- Step 82 remains blocked.
- Repair JSON records exact-seven paths/status/modes and exactly six non-JSON
  hashes; it records neither its own raw hash nor a future repair child OID.

## Unverified at This Precommit Record Boundary

- No repair JSON collection or content-only run is claimed here.
- No Python 3.12/3.14 repair PASS is claimed here.
- No independent P0/P1/P2 review is claimed here.
- No staging, repair commit, push, live equality, or persistence run is claimed.
- `PASS_P067_PLAN_ACTIVATION_PERSISTENCE_REPAIR` has not been observed.

## Exact Next Action

Complete the six non-JSON repair paths, collect the canonical JSON as the seventh
and last path, run Python 3.12/3.14 content-only and independent review, then let
the controller stage and verify exact-seven. The controller must commit with
parent `7e552965...` and subject
`fix(phase067): repair activation persistence proof`, push, verify local/upstream/
live equality and protected/main/Claude non-change, and run persistence mode on
both runtimes.

Cumulative Step 82 may begin only after independent review has P0/P1=`0/0`, the
same repair child OID is pushed/live-remote equal with a clean tree, and both
runtimes return `PASS_P067_PLAN_ACTIVATION_PERSISTENCE_REPAIR` for that child.
