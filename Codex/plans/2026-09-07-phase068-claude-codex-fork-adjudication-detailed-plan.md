# Phase 068 Claude/Codex Fork Adjudication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to execute this plan one cumulative Step at a time. Steps use checkbox (`- [ ]`) syntax for tracking. Every execution unit requires a result-first record, independent review, an exact commit, push, and dual-runtime persistence before the next unit.

**Goal:** Completely read and independently adjudicate the frozen Claude and Codex v1.0.25.2 review forks at commit-, parent-edge-, path-, claim-, equation-, and runtime-evidence level without changing either fork or adopting any commit wholesale.

**Architecture:** Git objects, not checkout labels or self-reports, define the two frozen evidence universes. Separate inventories preserve commit topology, parent-edge patches, full-read coverage, mathematical rederivation, runtime observations, authority ceilings, conflicts, and final file/issue-specific dispositions; later Steps join them only through content-addressed identifiers and explicit owners.

**Tech Stack:** Git object database, Python 3.12 and 3.14, strict canonical JSON, Markdown recovery records, symbolic series and independent numerical quadrature, disposable external runtime fixtures, Poppler PDF rendering.

---

Date: 2026-09-07
Status: `PASS_PENDING_PERSISTENCE`
Parent master plan: `Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`
Canonical completion master plan: `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`
Previous canonical result: `Codex/results/PHASE_067_RESULT.md`
Previous Gate result: `Codex/results/PHASE_067_STEP_090_2_GATE_RESULT.md`
Execution ledger: `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
Canonical ledger: `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
Recovery handover: `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

## Summary

Phase 068은 공통 조상 이후 Claude 고유 2개 commit과 Codex 고유 5개 commit을 다시 판정한다.
비교 대상은 브랜치명, commit message, handover의 자기보고 또는 최종 tree diff 하나가 아니다.
모든 commit의 실제 parent, 각 commit-parent edge의 patch, edge별 path/blob/mode, 최종 net tree,
산출물 전문, 수식, 실행 결과와 주장 사이의 관계를 서로 분리하여 검증한다.

이 phase는 특히 다음 오류를 차단한다.

1. merge commit의 첫 부모만 읽고 둘째 부모 edge를 누락하는 것,
2. net path 수와 commit-parent path event 수를 같은 분모로 부르는 것,
3. Claude의 U13 수정 또는 Codex의 이전 검토 결론을 독립 유도 없이 채택하는 것,
4. 실행되는 병행 모델을 과학적 이론 권위로 승격하는 것,
5. 성공한 test나 생성 PDF를 canonical release 또는 외적 타당성으로 오인하는 것,
6. commit을 통째로 가져와 file/issue-specific 판단과 provenance를 잃는 것.

누적 Step 번호는 정확히 `91–98`이다. Phase 경계에서 번호를 다시 시작하지 않는다. 각 Step은
human result와 control records를 먼저 작성하고 machine JSON을 마지막에 수집하며, exact allowlist만
stage한다. commit, push, live-origin 일치 및 Python 3.12/3.14 persistence가 모두 확인되기 전에는 다음 Step에 들어가지 않는다.

**Step 91은 `PASS_P068_PLAN_ACTIVATION_PERSISTENCE`가 두 Python runtime에서 모두
확인되기 전에는 시작할 수 없다.**

## Current Ground Truth

### Git and predecessor boundary

- Active branch는 `codex/anode-fit-v1025_2-canonical-completion`이다.
- Phase 068 plan activation expected predecessor는 `0371387f582fb63f5c3858d7e6905ed83eee885f`다.
- 이 predecessor의 subject는 `audit(phase067): close code history gate`다.
- Phase 067 selected Gate는 `CONDITIONAL_P067`이며, persisted terminal은 `PASS_P067_STEP90_2_PERSISTENCE`다. Persistence가 content Gate를 승격하지 않는다.
- protected branch `codex/lib-physics-endgame-v1025_2` tip은 `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`이다.
- current `main` tracking/live tip은 `f0c381bd6dc315ac75cbffa93dd86ce83a37949b`이다.
- active local HEAD, upstream, tracking ref와 live origin은 activation 직전 모두 `0371387f582fb63f5c3858d7e6905ed83eee885f`여야 하며 worktree/index는 clean이어야 한다.
- `Claude/**`, production source, frozen fork refs, protected branch와 `main`은 Phase 068 전체에서 read-only다.

### Frozen fork topology and exact denominators

공통 조상은 `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`다.

- Claude unique commits: `2`
- Codex unique commits: `5`
- Claude net paths: `3`
- Codex net paths: `69`
- Codex parent edges: `6`

Claude frozen tip은 `e3e1a634f34b711aa4803fd190fe9120f1755f13`이고 고유 commit은 다음 두 개뿐이다.

| Commit | Parent | Edge paths | Subject |
|---|---|---:|---|
| `2802395dd03e6cabe3e981bddddbba139e3963bc` | `3b5fd059ed09cdcdde38668c399cb35b8afbcca9` | `2` | `fix(v1.0.25.2): 문턱 근방 스케일링 각주 오류 정정 — Codex 교차검증 수용 (U13)` |
| `e3e1a634f34b711aa4803fd190fe9120f1755f13` | `2802395dd03e6cabe3e981bddddbba139e3963bc` | `1` | `docs(v1.0.25.2): 핸드오버 갱신 — Codex 11f9054 대조 상태 + U13 오류 기록` |

Base-to-tip net tree의 세 path는 모두 modified `100644` Claude 문건이다.

1. `Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md`
2. `Claude/docs/v1.0.25.2/_sections/ch3v22_sec02b_sifr.tex`
3. `Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md`

Codex frozen tip은 `11f90544865dd179739ca5bc5062b28c1078e504`이고 고유 commit set과 실제 edge는 다음과 같다.
`2abf019c...`의 parent는 공통 조상이 아니라 `ab196b292e14492b647f87a6c0d1d8c9ed0630ab`이므로 선형 base-child 관계를 추정하지 않는다.

| Commit | Parent edge | Edge paths | Subject |
|---|---|---:|---|
| `2abf019c7fee9bebd84b49cc9530f6983b08a8fa` | `ab196b292e14492b647f87a6c0d1d8c9ed0630ab` | `58` | `feat: add v1.0.25.3 physics conformance baseline` |
| `eed5d4850215b22ea7775de3365cd3d3cbfc4414` | `2abf019c7fee9bebd84b49cc9530f6983b08a8fa` | `1` | `plan: align conformance review with latest v1.0.25.2` |
| `4316d8a5423d0ba229931a3c43c1f833fdc2fe1e` | first parent `eed5d4850215b22ea7775de3365cd3d3cbfc4414` | `6` | `Merge latest v1.0.25.2 lineage for review` |
| `4316d8a5423d0ba229931a3c43c1f833fdc2fe1e` | second parent `3b5fd059ed09cdcdde38668c399cb35b8afbcca9` | `59` | same merge, separately audited edge |
| `30a874e906f2be72a36efaac7cb8fd8138e7b401` | `4316d8a5423d0ba229931a3c43c1f833fdc2fe1e` | `8` | `docs: add latest v1.0.25.2 alignment review` |
| `11f90544865dd179739ca5bc5062b28c1078e504` | `30a874e906f2be72a36efaac7cb8fd8138e7b401` | `3` | `docs: record latest review handover and verification` |

Codex six parent edges contain `135` path events in total (`58+1+6+59+8+3`), while the base-to-tip net tree
contains `69` distinct paths: `68` under `Codex/**` and one `output/pdf/Anode_Physics_v1.0.25.3_conformance.pdf`.
Neither denominator substitutes for the other.

The merge's first-parent edge modifies exactly six `Claude/**` paths and must be read apart
from its second-parent edge:

1. `Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md`
2. `Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py`
3. `Claude/docs/v1.0.25.2/_sections/ch1_sec05b_gr2L.tex`
4. `Claude/docs/v1.0.25.2/_sections/ch1_sec18_inputs.tex`
5. `Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md`
6. `Claude/docs/v1.0.25.2/test_gates_v1024.py`

The second-parent edge contains `58` Codex paths plus the one PDF. A combined merge diff, `--first-parent`
history, or tip-only tree cannot replace these two edge attestations.

### Later main drift is a separate input

Current `main` has seven later commits from `4069cb36a8a52b1b88c29d68aa54dcbe915b1618` through
`f0c381bd6dc315ac75cbffa93dd86ce83a37949b`. They contain `31` commit-path occurrences and `25`
distinct/final `Claude/**` paths, all in 2026-09-03 plan/handoff work. They are later Claude-side planning
drift, not the frozen v1.0.25.2 Claude review fork and not production changes. Phase 068 inventories this
drift separately so it cannot silently enter either the `2`-commit or `5`-commit denominator. Scientific or
planning adoption of that drift is routed forward; it is not adjudicated as one of the frozen fork commits here.

### Predecessor authority and open boundaries

- Phase 067 completed source/read/disposition/ownership audit coverage but selected `CONDITIONAL_P067` because seven required internal conformance rows remain incomplete.
- Original optimizer state, specimen/protocol binding, held-out evidence, material/phase/mechanism evidence, original Ref. 7 full text and current release-PDF authority remain open.
- Those open items cannot be manufactured from fork code, test output, commit prose or a PDF.
- Phase 068 determines what the two reviews established and what they did not establish. It does not select the final model, publish a new theory source, repair production code or establish external scientific truth.
- The frozen Codex `conformance_model` is an audit candidate. Executability can establish bounded implementation behavior, never primary-source or material authority by itself.

## Phase Range

| Execution unit | Scope | Content terminal | Required before next unit |
|---|---|---|---|
| Plan activation | Persist this detailed plan and recovery contract | `PASS_P068_PLAN_ACTIVATION` | `PASS_P068_PLAN_ACTIVATION_PERSISTENCE` |
| Step 91 | Claude two-commit/two-edge/net-tree full read | `PASS_P068_STEP91_CLAUDE_FORK_READ` | `PASS_P068_STEP91_PERSISTENCE` |
| Step 92 | Codex five-commit/six-edge/69-path full read | `PASS_P068_STEP92_CODEX_FORK_READ` | `PASS_P068_STEP92_PERSISTENCE` |
| Step 93 | Phase 044/054 coverage, evidence and supersession audit | `PASS_P068_STEP93_PRIOR_REVIEW_REAUDIT` | `PASS_P068_STEP93_PERSISTENCE` |
| Step 94 | U13 analytic and numerical independent rederivation | `PASS_P068_STEP94_U13_REDERIVATION` | `PASS_P068_STEP94_PERSISTENCE` |
| Step 95 | `conformance_model` authority/value/duplication adjudication | `PASS_P068_STEP95_CONFORMANCE_MODEL` | `PASS_P068_STEP95_PERSISTENCE` |
| Step 96 | Fork claim-conflict adjudication | `PASS_P068_STEP96_CONFLICT_ADJUDICATION` | `PASS_P068_STEP96_PERSISTENCE` |
| Step 97 | Exhaustive five-state file/issue disposition and carry | `PASS_P068_STEP97_DISPOSITION` | `PASS_P068_STEP97_PERSISTENCE` |
| Step 98 | File/issue adoption plan and final Phase Gate | selected Gate or `NOT_ACHIEVED` | `PASS_P068_STEP98_PERSISTENCE` |

These are cumulative Steps. No additional integer Step is created inside this phase.

## Exact Read Inputs

### Recovery controls at every execution-unit boundary

Before every unit, read this detailed plan, the immediately preceding Step result and machine
artifact, both execution ledgers, and `ACTIVE_HANDOVER_CANONICAL_COMPLETION.md` from line 1 to
EOF. Activation additionally reads and verifies:

- `Codex/results/PHASE_067_RESULT.md`
- `Codex/results/PHASE_067_STEP_090_2_GATE_RESULT.md`
- `Codex/results/PHASE_067_THEORY_CODE_TEST_DATA_CONFORMANCE_REPORT.md`
- `Codex/results/PHASE_067_VALIDATION.json`
- `Codex/results/PHASE_067_CARRY_FORWARD_DELTA.json`
- `Codex/work/v1025_phase067/validate_phase067_final.py`
- persisted commit `0371387f582fb63f5c3858d7e6905ed83eee885f`

The Git child and live remote are the persistence authority for the already committed Phase
067 transaction; precommit wording embedded in result files is historical state, not evidence
that the child is still pending.

### Git-object read rules

- Use exact commit, tree and blob object IDs. Do not populate the worktree with either fork.
- For each commit, read metadata and every actual parent edge separately. Record parent order, path status, mode before/after, blob before/after, raw byte extent and LF-normalized extent.
- For text, cover `1..EOF` with no gaps. For JSON, preserve a raw full-read attestation and a duplicate-key/nonfinite/depth-limited strict parse. For Python, add AST coverage without treating AST parsing as a human full read.
- Render the Codex PDF to an external disposable directory and inspect every page. PDF metadata, text extraction or successful opening alone is not visual coverage.
- Missing/corrupt Git objects, truncated command output or uncovered ranges are explicit `UNVERIFIED` evidence and prevent the Phase Gate; they are never inferred from neighboring files.

### Step-specific source universes

- Step 91 reads both Claude commits, both parent edges, all three net paths and every before/after blob implicated by those edges. Commit messages and the two changed self-reports are claim inputs, not truth sources.
- Step 92 reads all five Codex commits, all six parent edges, all `135/135` edge path events, all `69/69` net paths and every implicated blob. The merge is audited against both ordered parents.
- Step 93 reads from `11f90544865dd179739ca5bc5062b28c1078e504` the two branch plans,
  all Phase 044/054 results and machine artifacts, and all seven Phase 044/054 scripts:
  - `Codex/plans/2026-07-27-v1025_2-physics-conformance-branch-plan.md`
  - `Codex/plans/2026-07-27-v1025_2-latest-lineage-review-addendum-plan.md`
  - `Codex/results/PHASE_044_053_V1025_2_CONFORMANCE_EXECUTION_LEDGER.md`
  - `Codex/results/PHASE_044_CURRENT_SOURCE_PROBES.json`
  - `Codex/results/PHASE_044_LINEAGE_DIFF.json`
  - `Codex/results/PHASE_044_REGSOL_THRESHOLD_PROBE.json`
  - `Codex/results/PHASE_044_SOURCE_FREEZE_MANIFEST.json`
  - `Codex/results/PHASE_044_V1010_V1025_2_LINEAGE_REVIEW.md`
  - `Codex/results/PHASE_044_V1025_2_SOURCE_FREEZE_AND_COMPARISON_RESULT.md`
  - `Codex/results/PHASE_054_V1025_2_LATEST_LINEAGE_REVIEW_ADDENDUM.md`
  - `Codex/results/PHASE_054_V1025_2_LATEST_REVIEW_EXECUTION_LEDGER.md`
  - `Codex/results/PHASE_054_V1025_2_LATEST_SOURCE_FREEZE_MANIFEST.json`
  - `Codex/results/PHASE_054_V1025_2_LATEST_SOURCE_PROBES.json`
  - `Codex/results/PHASE_054_V1025_2_REGSOL_CROSSCHECK.json`
  - `Codex/work/v1025_2_physics_branch/phase044_current_source_probes.py`
  - `Codex/work/v1025_2_physics_branch/phase044_lineage_diff.py`
  - `Codex/work/v1025_2_physics_branch/phase044_regsol_threshold_probe.py`
  - `Codex/work/v1025_2_physics_branch/phase044_source_manifest.py`
  - `Codex/work/v1025_2_physics_branch/phase054_latest_source_manifest.py`
  - `Codex/work/v1025_2_physics_branch/phase054_latest_source_probes.py`
  - `Codex/work/v1025_2_physics_branch/phase054_regsol_crosscheck.py`
- Step 94 reads the exact `eq:sifr-twophase` source before and after Claude U13, the Phase 044 threshold probe, the Phase 054 crosscheck and their JSON outputs. It also reads definitions mapping `theta`, `Omega`, `R`, `T`, `Q`, `U^circ`, `rho` and `kappa`.
- Step 95 reads all eleven `Codex/work/v1025_2_physics_branch/conformance_model/**` paths, all ten `Codex/work/v1025_2_physics_branch/tests/**` paths, their README/contracts, the empirical artifact and every manuscript equation they claim to implement.
- Step 96 reads every claim-bearing plan, result, ledger, handover, conformance matrix, manuscript and commit message in the frozen 69-path Codex tree plus all three Claude net paths. Step 91–95 attestations may be reused only after exact blob/hash verification.
- Steps 97–98 read all persisted Step 91–96 machine and human artifacts and the inherited Phase 067 carry-forward registry. No finding may disappear between conflict and disposition tables.

## Non-goals and Scope Guards

- Do not modify `Claude/**`, production Python/LaTeX/bibliography/figure/PDF/data, either frozen fork, protected branch or `main`.
- Do not merge, rebase, reset, cherry-pick or copy a fork tree into the active worktree.
- A whole-commit cherry-pick is prohibited even when every file in that commit later receives a favorable disposition. Adoption is always file/issue-specific and occurs only in a later authorized implementation phase.
- Do not repair U13, production code, tests, manuscript or PDF in Phase 068. This phase records the independent judgment and exact downstream action only.
- Do not treat a commit subject, handover, plan checkbox, past Gate, test exit, saved JSON or PDF as proof of the claim it reports.
- Do not infer an original source, paper, DOI, equation or experimental result that was not read. A real DOI with unread proposition support remains `UNVERIFIED`; a fabricated citation is a hard failure.
- Do not promote synthetic/self-consistency/runtime evidence to held-out, specimen, material, mechanism or external validity.
- Do not treat the current main drift as part of the frozen `2/5` fork denominator.
- Phase 068 output is not canonical theory, not a canonical implementation, not a release and not publication readiness. It is a bounded fork-adjudication input for the next phase.

### Scholarly-body code-mention prohibition

Phase 068 plans, results and machine evidence may identify code, paths, commits and tests because they are audit records.
The main scholarly body, its captions, footnotes and visible headings may not mention code, function, class, file, schema key, API, test, commit, branch, phase, step or work history. Phase 068 does not modify the main scholarly body. A later scholarly rewrite may receive only the validated equation, assumptions, derivation and physical/chemical interpretation; all
implementation mapping remains in a designated appendix or companion.

## Implementation Changes

### Global execution-unit contract

Each unit uses the following order.

1. Verify branch, exact predecessor, upstream/live origin, protected/main/frozen refs and clean index.
2. Read the declared inputs fully and freeze their commit/tree/blob/mode/raw/LF identities.
3. Run the validator before its required new machine JSON exists; it must fail with the named
   missing-artifact diagnostic rather than pass from prose.
4. Write the human Step result, update both ledgers and update the handover.
5. Run the bounded builder and atomically create canonical machine JSON last.
6. Run Python 3.12 and Python 3.14 content validation, negative controls and byte-determinism `2/2`.
7. Freeze builder, validator, machine and result hashes; obtain independent specification and
   quality reviews with P0/P1/P2=`0/0/0`.
8. Stage only the exact allowlist; verify status, mode, blob bytes and dual-runtime staged state.
9. Commit with the exact subject, push only the active branch, compare local/upstream/tracking/live
   origin and require a clean tree.
10. Run dual-runtime persistence validation on the exact child before the next unit.

P0 or P1 forbids commit and requires repair plus full re-review. A P2 must also be resolved or
explicitly accepted by the detailed specification before the required `0/0/0` release review.

### Three disjoint transaction identities

Validators must not use one mutable `HEAD` assertion for three different states.

- The **fixed predecessor certificate** is commit-addressed and authenticates the already persisted predecessor and its
  prior terminal from immutable Git objects and live remote identity.
- The **current precommit transaction** requires current HEAD/upstream/live to equal that fixed
  predecessor while the exact allowlist exists only in worktree/index state.
- The **persistence child transaction** requires one exact child whose sole parent is the fixed
  predecessor, whose subject and path/mode/blob set match the contract, and whose local/upstream/
  tracking/live identities are equal.

After persistence, that child becomes the next unit's fixed predecessor. No validator may demand
that a postcommit HEAD simultaneously equal its parent.

### Builder and validator safety

- Read Git through fixed argv arrays with an explicit command allowlist; never invoke a shell string.
- No arbitrary network, package installation, dynamic import, dunder lookup, `eval`, `exec`, source
  checkout, source mutation or Git mutation is allowed in builders/validators. The sole network exception
  is the fixed-argv, read-only `git ls-remote origin <exact-ref>` query required to authenticate live refs.
- Runtime candidates are materialized only from frozen blobs into a system temp directory or other
  repository-external disposable root. Record source hashes before/after and cleanup.
- Builders may write only their declared new JSON paths by same-directory atomic replacement and
  must refuse overwrite unless the mode explicitly authorizes a deterministic comparison run.
- Every validator exposes exactly four mutually exclusive modes: `--collect`, `--content-only`,
  `--verify-staged`, and `--verify-persistence --expected-commit <lowercase40>`. The commit argument
  is mandatory only for persistence and forbidden in the other three modes.
- Canonical JSON uses UTF-8, sorted keys, stable separators, POSIX relative paths, finite numbers,
  LF endings and one terminal LF. The semantic seal excludes only its own field.
- Strict loaders reject duplicate keys, nonfinite numbers, excessive depth/member/byte counts and
  unknown fields where the schema is closed.

### Common Git closeout

For every unit, `git diff --cached --name-status` and `git ls-files --stage` must equal that unit's
ordered allowlist and all tracked files must be mode `100644`. The only permitted mutation is the
active branch's exact atomic commit. Push command scope is
`git push origin codex/anode-fit-v1025_2-canonical-completion`; live verification uses the exact
branch ref, not a cached remote-tracking ref alone.

## Plan Activation Unit — Save Before Step 91

### Exact-seven path allowlist

1. `Codex/plans/2026-09-07-phase068-claude-codex-fork-adjudication-detailed-plan.md`
2. `Codex/work/v1025_phase068/validate_phase068_plan.py`
3. `Codex/results/PHASE_068_PLAN_ACTIVATION_VALIDATION.json`
4. `Codex/results/PHASE_068_PLAN_ACTIVATION_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required precommit status map in this exact order: `A/A/A/A/M/M/M`.

### Activation control contract

The activation result, both ledgers and handover must name all four new artifact paths, expected
parent `0371387f582fb63f5c3858d7e6905ed83eee885f`, exact subject, activation Gate, current status,
`PENDING_AT_PRECOMMIT_BY_DESIGN`, reserved persistence terminal, exact next Step 91 and inherited
`PASS_P067_STEP90_2_PERSISTENCE`. The validation JSON is collected only after those human/control
bytes are frozen.

- [ ] Verify the predecessor commit, Phase 067 `CONDITIONAL_P067`, its exact subject and dual
  persistence without conflating the predecessor with the future child.
- [ ] Verify the common base, both frozen tips, `2/5` unique commits, `3/69` net paths, six Codex
  parent edges, the two merge-edge counts and current protected/main tips.
- [ ] Verify the later main `7`-commit/`25`-path drift is represented only as separate drift.
- [ ] Parse headings, cumulative Step 91–98 sections, every output allowlist, subject, terminal,
  source guard, authority ceiling, disposition enum and sole positive Phase Gate.
- [ ] Require result-first and JSON-last ordering, exact-seven status/modes, independent review,
  push/live verification and dual persistence.
- [ ] Reject any extra path, rename, deletion, mode change, production/Claude edit, branch drift,
  wholesale adoption or missing recovery-control token.

Commit subject: `docs(phase068): plan claude codex fork adjudication`
Content terminal: `PASS_P068_PLAN_ACTIVATION`
Required terminal: `PASS_P068_PLAN_ACTIVATION_PERSISTENCE`

## Phase 068 — Existing Claude/Codex Review Adjudication

### Step 91 — Claude Unique Commit, Edge, and Artifact Full Read

**Goal:** Prove complete coverage of the frozen Claude two fixed commits, both parent edges, all three
net paths, their before/after blobs and every U13/handover claim without accepting self-report as truth.

**Exact-eight outputs:**

1. `Codex/work/v1025_phase068/build_phase068_step91.py`
2. `Codex/work/v1025_phase068/validate_phase068_step91.py`
3. `Codex/results/PHASE_068_CLAUDE_FORK_DIFF_INVENTORY.json`
4. `Codex/results/PHASE_068_CLAUDE_FORK_FULL_READ_ATTESTATION.json`
5. `Codex/results/PHASE_068_STEP_091_CLAUDE_FORK_REVIEW_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status: `A/A/A/A/A/M/M/M`.

- [ ] Recompute merge base and exact `base..Claude-tip` commit set; require exactly the two fixed
  commits in topological order and their fixed parents/subjects.
- [ ] Inventory both parent edges with exact path status, old/new mode and blob. Require edge path
  counts `2` and `1` and net modified paths `3/3`.
- [ ] Read each unique before/after text blob from byte 0 to EOF and map line coverage losslessly to
  every occurrence; record raw and LF SHA-256 separately.
- [ ] Extract each atomic claim from commit messages, archive note, TeX footnote and handover, with
  exact line/blob pointers and self-report status.
- [ ] Record the U13 equation change as a claim requiring Step 94; do not decide C0 or C1 here.
- [ ] Generate both JSON artifacts after the result/control records, prove deterministic bytes `2/2`,
  then run dual content and staged validation.

Commit subject: `audit(phase068): read claude fork history`
Content terminal: `PASS_P068_STEP91_CLAUDE_FORK_READ`
Required terminal: `PASS_P068_STEP91_PERSISTENCE`

### Step 92 — Codex Unique Commit, Parent-Edge, and Artifact Full Read

**Goal:** Prove complete coverage of the frozen Codex five-commit set, all six ordered parent edges,
135 edge events, 69 net paths and every generated or claim-bearing artifact.

**Exact-eight outputs:**

1. `Codex/work/v1025_phase068/build_phase068_step92.py`
2. `Codex/work/v1025_phase068/validate_phase068_step92.py`
3. `Codex/results/PHASE_068_CODEX_FORK_DIFF_INVENTORY.json`
4. `Codex/results/PHASE_068_CODEX_FORK_FULL_READ_ATTESTATION.json`
5. `Codex/results/PHASE_068_STEP_092_CODEX_FORK_REVIEW_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status: `A/A/A/A/A/M/M/M`.

- [ ] Recompute `base..Codex-tip` and require the fixed five-commit set; preserve the non-base
  parent of `2abf019c...` and both ordered parents of `4316d8a...`.
- [ ] Audit all six parent edges at path/mode/blob level and require edge counts
  `58,1,6,59,8,3`, totaling `135/135` path events.
- [ ] Require the merge first-parent edge's six exact Claude paths and second-parent edge's
  `58 Codex + 1 PDF`; reject combined-diff substitution.
- [ ] Recompute the base-to-tip `69/69` net tree and partition `68 Codex + 1 PDF`; keep edge-event,
  net-path, occurrence and unique-blob denominators separate.
- [ ] Read all text blobs through EOF, inspect JSON structure and bytes, inspect all Python source,
  and render/visually cover every PDF page. Record unread/truncated members as Gate-blocking.
- [ ] Extract commit-message, plan, result, handover, manuscript, model, test and PDF claims with
  exact object pointers. A claimed success remains self-report until later evidence supports it.
- [ ] Generate JSON only after result/control records, prove deterministic bytes `2/2`, then run
  dual content and staged validation.

Commit subject: `audit(phase068): read codex fork history`
Content terminal: `PASS_P068_STEP92_CODEX_FORK_READ`
Required terminal: `PASS_P068_STEP92_PERSISTENCE`

### Step 93 — Phase 044/054 Coverage, Evidence, and Supersession Reaudit

**Goal:** Reconstruct what Phase 044 and Phase 054 actually read, calculated and concluded; identify
claim-level confirmation, correction, supersession and still-open evidence without treating the addendum
as a blanket replacement.

**Exact-seven outputs:**

1. `Codex/work/v1025_phase068/build_phase068_step93.py`
2. `Codex/work/v1025_phase068/validate_phase068_step93.py`
3. `Codex/results/PHASE_068_PHASE044_054_REAUDIT_MATRIX.json`
4. `Codex/results/PHASE_068_STEP_093_PHASE044_054_REAUDIT_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status: `A/A/A/A/M/M/M`.

- [ ] Verify all 21 declared Phase 044/054 inputs against their exact tip blobs and full-read
  attestations from Step 92; no checkout copy may silently replace a blob.
- [ ] Recompute every source-manifest and lineage denominator from Git trees and compare each
  report's declared coverage with its actual input set.
- [ ] Trace each machine result to the exact script bytes, argv, fixed parameters, source objects,
  numerical tolerance and output fields; distinguish stored output from a fresh rerun.
- [ ] Re-execute only deterministic, bounded historical probes in an external disposable directory
  on both runtimes, and record dependency/environment differences rather than editing them.
- [ ] Build one row per Phase 044 judgment and link Phase 054 as `CONFIRMS`, `CORRECTS`,
  `SUPERSEDES`, or `UNCHANGED_OPEN`; require exact successor evidence for every supersession.
- [ ] Compare the reconstructed judgments with Phase 067 evidence and mark conflict, scope mismatch,
  overclaim and still-open authority explicitly.
- [ ] Run RED before the matrix exists, JSON-last collection, determinism, dual content/staged checks
  and independent review before closeout.

Commit subject: `audit(phase068): revalidate phase044 phase054 reviews`
Content terminal: `PASS_P068_STEP93_PRIOR_REVIEW_REAUDIT`
Required terminal: `PASS_P068_STEP93_PERSISTENCE`

### Step 94 — U13 Regular-Solution Threshold Independent Rederivation

**Goal:** Independently determine the regular-solution threshold regularity of the broadened two-phase measure and
separate area conservation, C0 continuity, one-sided derivative existence and C1 equality.

**Exact-seven outputs:**

1. `Codex/work/v1025_phase068/build_phase068_step94.py`
2. `Codex/work/v1025_phase068/validate_phase068_step94.py`
3. `Codex/results/PHASE_068_U13_REGSOL_REDERIVATION.json`
4. `Codex/results/PHASE_068_STEP_094_U13_REGSOL_REDERIVATION_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status: `A/A/A/A/M/M/M`.

- [ ] Start from the documented binodal equation
  `ln(theta/(1-theta)) + (Omega/(R T))(1-2 theta) = 0` and the exact
  `eq:sifr-twophase` measure; do not start from either fork's conclusion.
- [ ] Set `a=Omega/(R T)=2+epsilon`, expand `theta_a=1/2-x` to sufficient order,
  derive the gap mass and explicitly track the matching central stable-branch mass removed from
  the convolution. Preserve assumptions on the kernel, window, normalization and differentiability.
- [ ] Derive the below-threshold and above-threshold curve expansions as functions of voltage.
  Linear `O(epsilon)` norm scaling can show the absence of a leading square-root divergence, but
  it does not by itself prove equality of the two one-sided derivatives. C1 is not assumed.
- [ ] Determine area `Q`, subcritical gap weight, C0 continuity, left derivative, right derivative
  and C1 equality as separate propositions, each with analytic status and an authority ceiling.
- [ ] Reproduce historical rows, then extend precision, epsilon sequence, voltage window/grid,
  quadrature order, kernel width and supported alpha cases. Use one-sided difference/Richardson
  convergence and pointwise plus norm comparisons; report cancellation and truncation error.
- [ ] Classify C1 as confirmed, refuted or `UNVERIFIED` only after analytic and numerical evidence
  agree within declared tolerances. Do not convert one finite max-norm ratio into a theorem.
- [ ] Run RED, JSON-last deterministic collection, dual-runtime validation, independent equation
  review and exact staged/persistence checks.

Commit subject: `audit(phase068): rederive u13 threshold regularity`
Content terminal: `PASS_P068_STEP94_U13_REDERIVATION`
Required terminal: `PASS_P068_STEP94_PERSISTENCE`

### Step 95 — Parallel Conformance Model Authority, Value, and Duplication

**Goal:** Judge every parallel `conformance_model`/test/manuscript asset on three independent axes: scientific
authority, implementation value and duplicate-lineage risk.

**Exact-seven outputs:**

1. `Codex/work/v1025_phase068/build_phase068_step95.py`
2. `Codex/work/v1025_phase068/validate_phase068_step95.py`
3. `Codex/results/PHASE_068_CONFORMANCE_MODEL_ADJUDICATION.json`
4. `Codex/results/PHASE_068_STEP_095_CONFORMANCE_MODEL_ADJUDICATION_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status: `A/A/A/A/M/M/M`.

- [ ] Map all eleven model paths, ten test paths, empirical artifact and manuscript interfaces to
  the exact equations/assumptions they claim to realize.
- [ ] Compare each formula, unit, sign, state transition, default, guard, fallback and serialization
  path with frozen theory and Phase 067 conformance evidence.
- [ ] Materialize exact blobs externally and run the declared test entry points under Python 3.12
  and 3.14. Record collected/executed/skipped/dependency-missing/assertion/failure behavior and cleanup.
- [ ] Score scientific authority only from verified derivation/source support; score implementation
  value from bounded behavior, contract clarity and test evidence; score duplication from semantic
  overlap, divergent defaults, independent history and maintenance/provenance risk.
- [ ] Do not allow a passing test, clean API, or manuscript agreement to promote an unverified
  scientific claim. Do not reject useful implementation structure merely because it lacks theory authority.
- [ ] Assign a downstream action recommendation per file and issue without copying or editing the
  candidate. Final five-state disposition remains Step 97's responsibility.
- [ ] Run RED, result-first/JSON-last, deterministic and negative controls, dual-runtime content/
  staged validation and independent code-plus-physics review.

Commit subject: `audit(phase068): adjudicate conformance model`
Content terminal: `PASS_P068_STEP95_CONFORMANCE_MODEL`
Required terminal: `PASS_P068_STEP95_PERSISTENCE`

### Step 96 — Fork Claim-Conflict Adjudication

**Goal:** Resolve or bound every material disagreement between Claude and Codex using source blobs,
equation derivations and actual runtime evidence rather than chronology or author identity.

**Exact-seven outputs:**

1. `Codex/work/v1025_phase068/build_phase068_step96.py`
2. `Codex/work/v1025_phase068/validate_phase068_step96.py`
3. `Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json`
4. `Codex/results/PHASE_068_STEP_096_FORK_CONFLICT_ADJUDICATION_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status: `A/A/A/A/M/M/M`.

- [ ] Form the lossless union of atomic claims from both forks, including commit-message versus
  actual-patch claims, coverage claims, U13, defaults, tests, model status, generated PDF and handover state.
- [ ] Give each conflict exact left/right claim IDs, source object/range, equation/runtime evidence,
  scope, premise differences, verdict, residual uncertainty, authority ceiling and one owner.
- [ ] Apply evidence precedence narrowly: actual Git objects over self-report for repository state;
  valid derivation over numerical impression for mathematical claims; fresh bounded runtime over stored
  exit prose for observed behavior; verified primary source over citation metadata for literature claims.
- [ ] Preserve compatible claims as non-conflicts and distinguish apparent wording differences from
  different domain, variable, limit, default or authority scope.
- [ ] Route unavailable primary propositions and experiments to `UNVERIFIED`; never invent a DOI,
  quote, parameter, mechanism or material assignment to close a row.
- [ ] Record current main drift separately and prove it neither changes the frozen claim union nor
  enters a disposition denominator.
- [ ] Require all Step 91–95 claim IDs to be represented exactly once as conflict, compatible,
  superseded-with-evidence or open; then run RED, JSON-last, determinism, dual validation and review.

Commit subject: `audit(phase068): adjudicate fork claim conflicts`
Content terminal: `PASS_P068_STEP96_CONFLICT_ADJUDICATION`
Required terminal: `PASS_P068_STEP96_PERSISTENCE`

### Step 97 — Exhaustive Five-State Disposition and Carry-Forward Delta

**Goal:** Give every frozen fork file, atomic issue and claim exactly one allowed disposition and
preserve every unresolved owner into a lossless carry-forward delta.

**Exact-eight outputs:**

1. `Codex/work/v1025_phase068/build_phase068_step97.py`
2. `Codex/work/v1025_phase068/validate_phase068_step97.py`
3. `Codex/results/PHASE_068_FORK_DISPOSITION_REGISTER.json`
4. `Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json`
5. `Codex/results/PHASE_068_STEP_097_FORK_DISPOSITION_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status: `A/A/A/A/A/M/M/M`.

- [ ] Apply exactly one of `ADOPT`, `REWRITE`, `REFERENCE_ONLY`, `REJECT`, `UNVERIFIED` to every
  file/issue record; no alias, null, compound status or silent omission is allowed.
- [ ] Define `ADOPT` as a validated concept/equation/asset eligible for later file-scoped transfer,
  not permission to copy its containing commit or branch.
- [ ] Define `REWRITE` as preserving bounded content while recreating it under the future canonical
  architecture with corrected derivation, scope, prose, defaults or provenance.
- [ ] Define `REFERENCE_ONLY` as historical/audit/test evidence that must not enter the canonical
  scholarly or implementation surface; define `REJECT` by a specific conflict; keep missing support
  `UNVERIFIED` with one owner and acceptance criterion.
- [ ] Require every Step 91–96 source, claim, conflict and recommendation to project to one disposition
  row; preserve many-to-one relations explicitly rather than dropping duplicate history.
- [ ] Create the carry-forward delta with inherited/resolved/new IDs, canonical owner, target phase,
  acceptance criterion, authority ceiling and no ownerless, multiply owned or lost active item.
- [ ] Prove no disposition target is a whole commit and no adoption has modified source; run RED,
  JSON-last, determinism, dual validation and independent disposition review.

Commit subject: `audit(phase068): classify fork evidence`
Content terminal: `PASS_P068_STEP97_DISPOSITION`
Required terminal: `PASS_P068_STEP97_PERSISTENCE`

### Step 98 — File/Issue Adoption Plan and Final Fork Gate

**Goal:** Integrate persisted Phase 068 evidence into a file/issue-specific downstream adoption plan with no whole-commit cherry-pick,
seal the audit report and select the sole positive Phase Gate only if every completeness predicate holds.

**Exact-eight outputs:**

1. `Codex/work/v1025_phase068/validate_phase068_final.py`
2. `Codex/results/PHASE_068_VALIDATION.json`
3. `Codex/results/PHASE_068_FORK_ADJUDICATION_REPORT.md`
4. `Codex/results/PHASE_068_STEP_098_GATE_RESULT.md`
5. `Codex/results/PHASE_068_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status: `A/A/A/A/A/M/M/M`.

- [ ] Strictly verify persisted activation and Steps 91–97 by commit genealogy, subject, exact
  path/mode/blob set, semantic seals, dual-runtime terminal and live-origin identity without replay inflation.
- [ ] Require Claude `2/2` commits, `2/2` edges and `3/3` net paths plus Codex `5/5` commits,
  `6/6` edges, `135/135` edge events and `69/69` net paths with complete full-read coverage.
- [ ] Require both merge edges, every Phase 044/054 judgment, the U13 independent result, every
  conformance-model asset, every fork conflict and every five-state disposition to be losslessly linked.
- [ ] Write an adoption section whose rows identify exact source object/path, issue/claim, disposition,
  bounded content to carry, required rewrite, destination owner, acceptance test and prohibited overclaim.
  No row authorizes source modification or whole-commit transfer in this phase.
- [ ] Write report, Gate result, phase result, ledgers and handover first; collect final canonical
  validation JSON last and require deterministic bytes `2/2`.
- [ ] Select `PASS_P068_FORK_ADJUDICATION` only when every predicate below is true. Otherwise record
  `NOT_ACHIEVED`, name each diagnostic, retain affected items as `UNVERIFIED` with owners, persist the
  recovery transaction, and do not enter the next phase.
- [ ] Obtain independent specification, Git/topology, equation and authority reviews at
  P0/P1/P2=`0/0/0`, then exact staged, commit/push/live/clean and dual persistence verification.

Commit subject: `audit(phase068): close fork adjudication gate`
Content terminal: selected `PASS_P068_FORK_ADJUDICATION` or `NOT_ACHIEVED`
Required terminal: `PASS_P068_STEP98_PERSISTENCE`

## Phase Gate

### `PASS_P068_FORK_ADJUDICATION`

This is the only positive Phase 068 Gate. It is selected only when all conditions are true:

1. The common base and both frozen tips match the fixed Git objects.
2. Claude `2/2` commits, two parent edges, three net paths and all implicated blobs are fully read.
3. Codex `5/5` commits, six parent edges, `135/135` path events, `69/69` net paths and all
   implicated blobs are fully read.
4. Both ordered edges of the merge commit are independently covered and their `6` versus `59`
   path sets are not conflated.
5. Every text/binary/PDF artifact has its required full-read or full-page coverage with no gap.
6. Phase 044 and Phase 054 source coverage, runtime provenance, judgments and supersession relations
   are independently reconstructed.
7. U13 area, subcritical gap, C0, one-sided derivatives and C1 status are independently derived;
   linear scaling alone is not used as proof of C1.
8. Every parallel conformance model/test/manuscript asset has separate scientific-authority,
   implementation-value and duplicate-lineage judgments.
9. Every self-report/actual-Git mismatch and every material fork claim conflict is adjudicated or
   explicitly `UNVERIFIED` with one owner and acceptance criterion.
10. Every file/issue/claim has exactly one allowed five-state disposition, and the carry-forward
    delta has no lost, ownerless or multiply owned active item.
11. The current main `7`-commit/`25`-path drift is recorded separately and does not inflate frozen
    fork denominators.
12. No commit is cherry-picked wholesale, no source or protected ref changes, no unsupported DOI or
    authority promotion occurs, and the downstream adoption plan is exact and file/issue-specific.
13. Activation and Steps 91–97 are persisted; current Step 98 precommit validation and independent
    reviews close at P0/P1/P2=`0/0/0`. Step 98's own persistence is verified afterward by its separate
    terminal and is not a circular content-Gate prerequisite.

This Gate proves completeness and integrity of the frozen fork adjudication only. It does not make
either fork canonical, does not validate a material model externally, does not approve publication,
and does not close the Phase 067 or literature/data debts outside this scope.

If any predicate is false, the positive Gate is not selected. The result state is `NOT_ACHIEVED`;
the exact diagnostics and affected `UNVERIFIED` owners are preserved without inventing an alternate
Phase Gate label. Content outcome and `PASS_P068_STEP98_PERSISTENCE` remain separate: the latter can
prove that an honest non-passing recovery result was committed and pushed, not that the Gate passed.

## Canonical-Evidence Reuse Protocol

- Phase 067 committed bytes, semantic seals, genealogy and persisted terminal are verified as prior
  evidence; historical validators and fits are not rerun merely to inflate execution counts.
- Step 91/92 full-read attestations may be reused in Steps 93–98 only after exact commit/path/blob/raw/LF
  identity checks. Reuse is counted separately from fresh reads.
- Historical Phase 044/054 JSON and logs are evidence under review, not self-authenticating canonical
  facts. Fresh reruns are explicitly labeled and never overwrite them.
- A repeated path across edges remains multiple genealogy events but may reuse one byte-identical
  blob read. Coverage records preserve both the unique blob and every occurrence projection.
- Stored test/PDF/output evidence is never reported as a current execution. Current execution records
  runtime, argv, cwd class, inputs, outputs, exit, stdout/stderr digest, dependencies and cleanup.
- Machine artifacts contain no username, absolute workspace path, volatile timestamp, temp-random suffix
  or cached tracking ref as semantic evidence.

## Implementation Interfaces

### Commit and parent-edge row

Each commit row contains fork, commit OID, ordered parent OIDs, author/committer timestamps, subject,
tree OID and set membership. Each edge row contains commit, parent index/OID, old/new path, status,
old/new mode, old/new blob, raw byte extents and whether it belongs to the net tree.

### Full-read row

Each source row contains commit/tree/path/blob/mode, media role, raw/LF SHA-256, bytes, lines/pages,
review mode, exact coverage intervals, parser/renderer evidence, claim IDs and `READ_FULL` only when
the union covers the entire declared extent.

### Claim and conflict row

Each atomic claim contains claimant surface, exact object/range, normalized proposition, domain,
assumptions, quantity/unit/sign/basis, self-report status, supporting/refuting evidence IDs, authority
ceiling and owner. Conflict rows contain both sides, premise differences, evidence precedence,
verdict and remaining uncertainty.

### U13 row

Each proposition row separately records the binodal series order, kernel/window assumptions, analytic
derivation, numeric method/precision/grid/window, epsilon, left/right difference quotient, convergence
order, tolerance, result and authority ceiling. C0 and C1 are distinct fields.

### Model and disposition row

Model rows contain file/symbol/equation mapping, input/output/state/default/guard/test/runtime evidence,
scientific authority, implementation value and duplication risk. Disposition rows contain exact target
kind/ID, one of the five allowed values, rationale/evidence, bounded carry content, destination owner,
acceptance criterion and prohibited authority promotion.

## Test and Validation Plan

### TDD and runtime matrix

- Before each new JSON exists, both Python 3.12 and 3.14 validators must fail with the named missing
  artifact diagnostic. A false PASS is a validator defect.
- After result/control freeze and JSON-last collection, both runtimes must return that Step's exact
  content terminal.
- Two independent external-temp collections must be byte-identical to each other and semantically
  identical to the repository artifact.
- After exact staging, both runtimes must pass staged verification. After commit/push/live equality,
  both must return that Step's exact persistence terminal.
- If either runtime is unavailable, do not infer equivalence; record the environment failure and stop
  the transaction before commit.

### Positive controls

- Fixed predecessor/subject/terminal, exact branch refs and clean state.
- Common base, Claude/Codex tips, exact `2/5` commits, `3/69` net paths, six Codex parent edges,
  `135` path events and two merge-edge partitions.
- Full text/blob/PDF extent coverage and strict JSON parsing.
- Phase 044/054 source/result/script relationships and claim-level supersession.
- U13 analytic/numeric provenance with separate C0/left derivative/right derivative/C1 fields.
- Model authority/value/duplication axes, conflict union, five-state disposition, carry ownership.
- result-first, JSON-last, exact path/status/mode, review `0/0/0`, local/upstream/tracking/live equality.

### Named negative controls

- Drop or replace either Claude commit, any Codex commit, either merge parent or any edge path.
- Swap parent order; accept only a combined merge diff; confuse 69 net paths with 135 events; inflate
  the frozen denominator with protected/active history or current main drift.
- Change one path/blob/mode/status, truncate one read range, mark metadata-only PDF inspection full,
  accept duplicate JSON keys/nonfinite/deep input or reuse a different checkout blob.
- Treat Phase 054 as blanket supersession, a commit message as patch evidence, stored output as fresh
  runtime, or a passed test as scientific/material authority.
- Infer C1 only from `O(epsilon)` magnitude, omit either one-sided derivative, alter the binodal sign,
  normalize away an area/unit error or hide window/quadrature dependence.
- Give an item two dispositions, use a sixth enum, lose an owner, adopt a whole commit, silently copy
  source, fabricate a DOI/reference or claim canonical/publication status.
- Add an undeclared path, rename/delete, change non-control source, use the wrong subject/parent,
  push another ref, leave a dirty tree or accept cached tracking state without live remote equality.

Validators execute negative payloads as data, never as code. All negative controls must be named,
reachable and mutation-restoring; a failure must identify the exact violated predicate.

## Stop Conditions

Stop the current execution unit and record the exact evidence state when any of the following occurs:

1. The expected predecessor, active/upstream/live ref, protected tip, main tip, common base or frozen
   fork tip differs from the fixed boundary and cannot be explained as separately inventoried drift.
2. A required commit, parent, tree, blob, line range, binary member or PDF page is missing, corrupt,
   truncated or cannot be independently inspected.
3. Commit/edge/net-path denominators cannot be reproduced, or merge-parent coverage is incomplete.
4. Phase 044/054 scripts, inputs and outputs cannot be bound without substituting a different source.
5. U13 cannot be resolved without assuming the desired regularity, suppressing a limit/window error or
   altering the documented equation.
6. Model/runtime evidence cannot be separated from theory, literature, material or external authority.
7. A conclusion requires an unread/paywalled source, missing credential, unavailable experiment or
   user-only scientific choice and cannot safely remain `UNVERIFIED` with alternatives.
8. Source/Claude/protected/main mutation, whole-commit adoption, an extra staged path, wrong mode,
   P0/P1 finding or nonzero unresolved release review is present.
9. The same push/persistence cause fails three times or live remote diverges unexpectedly.

A bounded unknown is not filled by inference. It remains `UNVERIFIED` with owner and acceptance
criterion. If that unknown violates a Phase Gate predicate, the honest final state is `NOT_ACHIEVED`.

## Assumptions

- All fixed Git objects are locally readable and live refs remain stable during each atomic unit.
- Byte-identical blobs may reuse one human read only when every occurrence and edge projects to the
  attestation without loss.
- Python 3.12, Python 3.14 and Poppler are available; missing capability is recorded, not simulated.
- The original fork artifacts are evidence to adjudicate, not authority to inherit.
- Phase 067 open obligations remain open unless exact Phase 068 evidence satisfies their acceptance
  criteria; fork agreement alone is insufficient.
- No production or scholarly authoring is authorized in this phase.

## Correction History

- 2026-09-07: Created the Phase 068 detailed plan from persisted Phase 067 commit
  `0371387f582fb63f5c3858d7e6905ed83eee885f` and cumulative Steps `91–98`.
- 2026-09-07: Fixed the frozen fork denominators at Claude `2` commits/`3` net paths and Codex
  `5` commits/`6` parent edges/`69` net paths, with the merge's two edges audited separately.
- 2026-09-07: Separated current main's seven-commit/25-path planning drift from the frozen comparison.
- 2026-09-07: Required analytic plus numerical U13 rederivation with C0 and C1 separated and C1 not assumed.
- 2026-09-07: Fixed the five dispositions, prohibited whole-commit transfer, and retained only
  `PASS_P068_FORK_ADJUDICATION` as a positive Phase Gate.
