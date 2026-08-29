# Phase 064 v1.0.23 Lineage Reaudit Implementation Plan

정본일: 2026-08-29

상위 계획:

- `Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`
- `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`

직전 복구 checkpoint:

- Phase 063 Step 63.2 commit `696e6300a63ba47d773ca211362818987790a63f`
- subject `audit(phase063): close v1022 lineage gate`
- terminal `PASS_P063_STEP63_2_PERSISTENCE`

누적 Step 범위: 64–69

유일 Phase Gate: `PASS_P064_LINEAGE_G`

## Summary

Phase 064는 frozen baseline `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`에 보존된 `Claude/docs/v1.0.23/**` 전체와 그 계획·검토·문헌 계보를 다시 감사한다. 목표는 v1.0.23이 주장한 Fredholm 제2종 ratio/reference substitution, causal lag Volterra closure, voltage-domain transfer function, algebraic self-consistency 경계와 내부 검증의 실제 권위 범위를 원문·수식·코드·Git 이력에서 분리해 확정하는 것이다.

본 Phase는 v1.0.23 산출물을 수정하거나 정본으로 승격하지 않는다. `Claude/**`, protected branch `codex/lib-physics-endgame-v1025_2`, `main`은 read-only다. 모든 신규 산출물은 현재 active branch의 `Codex/**` 아래에만 저장한다.

Phase 064는 cumulative Steps `64`, `65`, `66`, `67`, `68`, `69.1`, `69.2`를 사용한다. 각 Step은 result-first로 계획된 exact allowlist만 저장하고, 독립 검증 뒤 atomic commit과 immediate push를 수행하며, postcommit persistence terminal을 확인하기 전 다음 Step으로 넘어가지 않는다.

현재 저장소에는 JCP 147(14), 144111 (2017) 원문이 있으나 그 논문이 인용하는 Ref. 6과 Ref. 7 원문은 발견되지 않았다. 따라서 두 원문을 실제 확보하고 1–EOF/전 페이지 검독하기 전에는 master plan이 요구하는 `PASS_P064_LINEAGE_G`를 부여할 수 없다. DOI/서지만 확인된 상태를 원문 확인으로 대체하지 않으며, 현재 가능한 Phase 상한은 `CONDITIONAL_P064`다.

## Current Ground Truth

### Git and protection state

- active branch: `codex/anode-fit-v1025_2-canonical-completion`.
- activation expected parent: `696e6300a63ba47d773ca211362818987790a63f`.
- expected activation subject: `docs(phase064): plan v1023 lineage reaudit`.
- protected branch fixed tip: `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`.
- main fixed tip: `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`.
- frozen source baseline: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`.
- Phase 063 Step 63.2 commit은 local HEAD, upstream, origin tracking과 live origin active tip에서 동일하다.
- Phase 063 Step 63.2 exact-eight blob과 worktree가 일치하고 작업트리는 clean이다.
- Phase 063 postcommit validator는 Python 3.12와 3.14에서 각각 `PASS_P063_STEP63_2_PERSISTENCE`를 반환했다.
- `Claude/**` tracked/untracked diff는 0이며 이 Phase에서 계속 0이어야 한다.

### Frozen v1.0.23 manifest denominator

정본 inventory는 `Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json`의 indices `744–826`이다.

- source occurrences: `83`.
- unique paths/blobs: `83/83`.
- total bytes: `3,338,330`.
- exact sorted path-set canonical SHA-256: `7b37fe84d8cbceebafb8801e5489545ace1a7052ed33668ec2ec2200abb422b5`.
- `FULL_TEXT=78`, physical lines `12,508`.
  - `.py`: `6` files / `2,733` lines.
  - `.md`: `15` files / `1,359` lines.
  - `.tex`: `57` files / `8,416` lines.
- `FULL_PDF=3`, total `129` pages (`3/129`).
- `FULL_IMAGE=2`.
- roles: theory `56`, result `17`, generated document `3`, figure `2`, code `1`, test `2`, implementation guide `1`, supporting document `1`.

Step 64에서 위 숫자를 frozen Git blob으로 독립 재구성한다. 현재 조사에서 manifest identity는 확인했지만 78개 text 1–EOF, PDF 129쪽과 image 2개 전수 검독은 Step 64 실행 범위다.

### Mandatory supplemental process and literature inputs

83-source manifest와 별도로 다음 입력을 읽고 별도 occurrence로 관리한다. 이들을 84번째 이후 manifest row로 오인하지 않는다.

- `Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md`, 225 lines.
- `Claude/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf`:
  - Git blob `4fbe2b91b2b3f62cea76feb4272b1e3275dab986`.
  - raw SHA-256 `47c7c415093bf5e3ee78215d6efa9141e4cd574e74e206cd9e3e863c5da85bd9`.
  - `2,075,558` bytes, `10` pages.
- `Claude/jcp_extract.txt`, Git blob `2588ac5da0e9ce4c25141f302a1e33e460ff7966`, 725 lines. Step 65에서 raw SHA-256과 encoding을 다시 고정한다.
- Phase 057 v1.0.23 read map과 `PHASE_057AA`–`PHASE_057AF` observation 6개.
- Phase 057 provisional findings `INTENT-PROV-0192`–`INTENT-PROV-0227`, 36 records.
- 과거 Ref. 6/7 extraction·closure dossier. 해당 문서는 과거 관찰이며 원 논문을 대신하지 않는다.

### v1.0.23 process topology

핵심 commit chain은 다음과 같다.

| Stage | Commit | Meaning |
|---|---|---|
| initial plan | `9cb1ad900b6b170976fa41f31dd5a2ca8330b2d6` | ratio/advanced-method plan 최초 저장 |
| survey | `63972cfc0af6ba232a361c3d96fcedc656f647d0` | survey synthesis |
| P0 | `d47d4dbb79fdaba284f15faca62ee9d6a280c3d8` | v1.0.23 skeleton/baseline |
| partial P1 | `ee0371f74524460e908bb548d10e9592e1807fe9` | conditional derivation work |
| plan correction | `a722313ac19ece6bb72c87b7cd99e498fca25876` | 11-section/cumulative-step correction |
| P1 | `3aa791aeb7357f23dbfb1d232277fd84276ca16b` | condition gate |
| P2 | `802673049bc54f0f11282af1334970042584229d` | Appendix E authoring |
| P3 | `ff840987a99348c092d3ab535c934ac7f303c5b1` | code options |
| P5 | `b6e51105341696ad97a5d5d6ec0c414c8bd0c62d` | adversarial review/closure |
| P5 ledger | `4b781d31d31771ee6275805be8931c2a510df010` | ledger/change-log close |
| curve QA | `4d56dc9f78a9aaf5d00e3479298371fde91a170e` | internal curve QA |
| Ref.7 metadata | `ce1e5e7e0b1407f6f5fd366bd30f3c9c8fa41bde` | Ref.7 DOI metadata update |
| code guide | `ae6c967830d866e8b45e6087ba128b50790f2840` | code guide |
| later Ref.6 metadata | `1ad0e2c70ff213e2fc89ff77d50e74da25080d06` | v1.0.24 session에서 v1.0.23 ledger 보강 |

P4는 D3 승인 미수신 때문에 의도적으로 skip됐다. `PHASE_P4_RESULT.md`는 존재하지 않으며, 이를 누락이나 위조 결과로 채우지 않는다.

### Literature ground truth and conflicts

- JCP147 원문은 local Git blob으로 존재한다. Step 65에서 페이지와 Eqs. 32–39를 원문에서 재확인한다.
- Ref. 6 metadata: Lee et al., *J. Chem. Phys.* 134, 121102 (2011), DOI `10.1063/1.3565476`.
- Ref. 7 metadata: Son et al., *J. Chem. Phys.* 138, 164123 (2013), DOI `10.1063/1.4802584`.
- Ref. 6/7의 full text는 current tree와 전체 Git filename inventory에서 발견되지 않았다. 현재 method-content authority는 `GROUND_NOT_FOUND`다.
- 오래된 dossier의 Ref. 7 DOI `10.1063/1.4802005`는 adopted bibliography/JCP147 reference list의 `10.1063/1.4802584`와 충돌한다. Step 65에서 false DOI 음성 대조를 둔다.
- `V1023_REFERENCE_LEDGER.md` 제목과 내용은 v1.0.22 ledger를 승계하며 JCP147/Ref. 6/7의 실제 adopted bibliography inventory를 완전하게 대표하지 않는다.
- 실제 추가 bibliography identity는 `Claude/docs/v1.0.23/_sections/ch1v22_bib.tex`의 JCP147/Ref. 6/7 항목과 별도로 대조해야 한다.

### Mathematical and physical risk boundary

- JCP147의 문제는 fixed-domain, two-sided, global Fredholm second kind다.
- v1.0.23 lag 문제는 variable-upper-limit, causal Volterra second kind이고 exponential kernel이면 first-order ordinary differential equation으로 환원된다.
- 직접 이식 가능한 것은 Eq. 34의 ratio/reference substitution 논리이지 Fredholm 장치의 literal transfer가 아니다.
- algebraic charge-balance root와 background algebraic self-consistency loop는 integral-kernel ratio method의 적용 대상이 아니다.
- transfer variable은 voltage coordinate의 Fourier conjugate `omega_V`다. time response, electrochemical impedance spectroscopy 또는 instrument response authority로 승격하지 않는다.
- frozen lag와 Picard/ratio 경로가 모두 실질적으로 `O(N)`일 수 있으므로 positive speedup을 가정하지 않는다. 측정 결과가 zero, no benefit 또는 regression이면 그대로 기록한다.
- 선행 v1.0.23 C-rate/timebase 주장에는 3600배 단위 부채가 있다. `L_V/w`, current-regime window와 성능 숫자는 이 부채를 분리하기 전 승인하지 않는다.

### Carry-forward and authority boundary

Phase 063의 open/carry universe와 Phase 057 v1.0.23 observations는 routing input이다. 이전 문서의 `PASS`, `치명 0`, `완결`, curve QA 또는 synthetic gate를 external scientific/material/experimental truth로 자동 승격하지 않는다.

다음 authority는 Phase 064 내부 PASS에서도 false를 유지한다.

- external scientific truth.
- material truth.
- experimental truth.
- primary-literature method truth for Ref. 6/7 until full text is read.
- canonical model/equation selection.
- defect repair completion.
- identifiability and held-out fitting.
- final equation/LaTeX/PDF freeze.
- publication readiness.

## Phase Range

| Unit | Cumulative Step | Purpose | Expected output Gate |
|---|---:|---|---|
| plan activation | pre-Step 64 | plan/source/recovery boundary | `PASS_P064_PLAN_ACTIVATION` |
| source/process/read | 64 | 83-source topology and full-read attestation | `PASS_P064_STEP64_SOURCE_PROCESS` |
| literature authority | 65 | JCP147 and Ref. 6/7 authority | `PASS_P064_STEP65_LITERATURE` or bounded GNF result |
| mathematical rederivation | 66 | ratio closure and voltage transfer rederivation | `PASS_P064_STEP66_REDERIVATION` |
| problem/code/runtime boundary | 67 | algebraic vs Volterra and runtime | `PASS_P064_STEP67_BOUNDARY` |
| validation authority | 68 | synthetic/internal vs experimental | `PASS_P064_STEP68_AUTHORITY` |
| dispositions/carry | 69.1 | source and finding disposition | `PASS_P064_STEP69_1_DISPOSITIONS` |
| integrated close | 69.2 | Lineage Report G and sole Phase Gate | `PASS_P064_LINEAGE_G`, `CONDITIONAL_P064`, or `FAIL_P064` |

Step numbering does not restart inside this Phase. Phase 065 starts at cumulative Step 70 only after Step 69.2 commit/push/persistence.

## Exact Read Inputs

### Control inputs at every recovery boundary

1. `Codex/AGENTS.md` 1–EOF.
2. both master plans 1–EOF.
3. this detailed plan 1–EOF.
4. latest completed Step result and machine artifact 1–EOF/full traversal.
5. both execution ledgers 1–EOF.
6. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md` 1–EOF.
7. Git branch, HEAD/upstream/tracking/live refs, protected/main tips and `Claude/**` diff.

After compaction or handoff, the controller must re-read the master plan, this detailed plan and the immediately preceding Step result before resuming.

### Frozen inventory and routing inputs

- Phase 056 source manifest strict full traversal.
- Phase 057 v1.0.23 read map, AA–AF observations and provisional finding rows 0192–0227.
- Phase 063 final result, validation, ledgers and active handover.
- all 83 frozen v1.0.23 source blobs.
- supplemental v1.0.23 plan, JCP147 PDF, extract and Ref. 6/7 dossiers.

### Full-read policy

- text: Git blob bytes, UTF-8/declared encoding, physical line count, 1–EOF coverage.
- PDF: raw blob hash, page count, text extraction and every-page visual attestation.
- images: raw blob hash, dimensions/mode and full visual attestation.
- source code: 1–EOF static read; runtime is a separate evidence class.
- missing Ref. 6/7 originals: `GROUND_NOT_FOUND`, never inferred from JCP147, DOI metadata or later summaries.

## Non-goals and Scope Guards

- `Claude/**` 수정, generated-file normalization, metadata repair 또는 history rewrite 금지.
- protected branch/main 수정·merge·rebase 금지.
- v1.0.23 self-report를 external truth로 채택 금지.
- JCP147을 Ref. 6/7 원문 대용으로 표시 금지.
- DOI landing page/abstract를 full-text method verification으로 표시 금지.
- Fredholm과 Volterra equation class를 합치거나 literal-equivalence를 주장 금지.
- algebraic roots에 integral-kernel ratio method 적용 금지.
- first Picard/ratio iterate를 exact solution 또는 general convergence로 승격 금지.
- voltage-domain Fourier response를 time/EIS/instrument response로 승격 금지.
- positive computational benefit 사전 가정 금지.
- C-rate 3600배 부채를 해결하지 않은 regime 숫자 승인 금지.
- P4 result fabrication 또는 missing-result failure 처리 금지.
- 본 Phase에서 canonical theory, production code 또는 최종 LaTeX/PDF 수정 금지.

## Implementation Changes

### Plan activation — exact seven

1. `Codex/plans/2026-08-29-phase064-v1023-lineage-detailed-plan.md`
2. `Codex/work/v1023_phase064/validate_phase064_plan.py`
3. `Codex/results/PHASE_064_PLAN_ACTIVATION_VALIDATION.json`
4. `Codex/results/PHASE_064_PLAN_ACTIVATION_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Expected subject: `docs(phase064): plan v1023 lineage reaudit`.

### Step 64 — exact eight

1. builder `Codex/work/v1023_phase064/build_phase064_step64_source_process_topology.py`
2. validator `Codex/work/v1023_phase064/validate_phase064_step64.py`
3. `Codex/results/PHASE_064_V1023_SOURCE_PROCESS_TOPOLOGY.json`
4. `Codex/results/PHASE_064_V1023_READ_ATTESTATION.json`
5. `Codex/results/PHASE_064_STEP_064_SOURCE_PROCESS_TOPOLOGY_RESULT.md`
6. parent ledger
7. active ledger
8. active handover

Expected subject: `audit(phase064): freeze v1023 source process topology`.

### Step 65 — exact eight

1. builder `Codex/work/v1023_phase064/build_phase064_step65_literature_authority.py`
2. validator `Codex/work/v1023_phase064/validate_phase064_step65.py`
3. `Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json`
4. `Codex/results/PHASE_064_V1023_LITERATURE_READ_ATTESTATION.json`
5. `Codex/results/PHASE_064_STEP_065_LITERATURE_AUTHORITY_RESULT.md`
6. parent ledger
7. active ledger
8. active handover

Expected subject: `audit(phase064): bound v1023 literature authority`.

### Step 66 — exact seven

1. builder `Codex/work/v1023_phase064/build_phase064_step66_ratio_transfer_rederivation.py`
2. validator `Codex/work/v1023_phase064/validate_phase064_step66.py`
3. `Codex/results/PHASE_064_V1023_RATIO_TRANSFER_REDERIVATION.json`
4. `Codex/results/PHASE_064_STEP_066_RATIO_TRANSFER_REDERIVATION_RESULT.md`
5. parent ledger
6. active ledger
7. active handover

Expected subject: `audit(phase064): rederive v1023 ratio transfer closure`.

### Step 67 — exact eight

1. builder `Codex/work/v1023_phase064/build_phase064_step67_problem_runtime_boundary.py`
2. validator `Codex/work/v1023_phase064/validate_phase064_step67.py`
3. `Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json`
4. `Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json`
5. `Codex/results/PHASE_064_STEP_067_PROBLEM_RUNTIME_BOUNDARY_RESULT.md`
6. parent ledger
7. active ledger
8. active handover

Expected subject: `audit(phase064): bound v1023 algebraic volterra runtime`.

### Step 68 — exact seven

1. builder `Codex/work/v1023_phase064/build_phase064_step68_validation_authority.py`
2. validator `Codex/work/v1023_phase064/validate_phase064_step68.py`
3. `Codex/results/PHASE_064_V1023_VALIDATION_AUTHORITY_MATRIX.json`
4. `Codex/results/PHASE_064_STEP_068_VALIDATION_AUTHORITY_RESULT.md`
5. parent ledger
6. active ledger
7. active handover

Expected subject: `audit(phase064): adjudicate v1023 validation authority`.

### Step 69.1 — exact eight

1. builder `Codex/work/v1023_phase064/build_phase064_step69_dispositions.py`
2. validator `Codex/work/v1023_phase064/validate_phase064_step69_dispositions.py`
3. `Codex/results/PHASE_064_V1023_DISPOSITION_MATRIX.json`
4. `Codex/results/PHASE_064_V1023_CARRY_FORWARD_DELTA.json`
5. `Codex/results/PHASE_064_STEP_069_1_DISPOSITION_RESULT.md`
6. parent ledger
7. active ledger
8. active handover

Expected subject: `audit(phase064): disposition v1023 lineage`.

### Step 69.2 — exact eight

1. final validator `Codex/work/v1023_phase064/validate_phase064_final.py`
2. `Codex/results/PHASE_064_VALIDATION.json`
3. `Codex/results/PHASE_064_V1023_LINEAGE_REPORT_G.md`
4. `Codex/results/PHASE_064_STEP_069_2_GATE_RESULT.md`
5. `Codex/results/PHASE_064_RESULT.md`
6. parent ledger
7. active ledger
8. active handover

Expected subject: `audit(phase064): close v1023 lineage gate`.

## Plan Activation Unit — Save Before Step 64

### Activation A — recovery and validator-first RED

- verify Phase 063 commit/push/persistence and exact repository boundaries.
- save plan before Step 64 execution.
- write activation validator with missing-validation-artifact RED.
- compile validator on Python 3.12 and 3.14.
- no production source import or execution.

### Activation B — exact plan/source/process validation

- independently reconstruct manifest indices 744–826.
- bind 83 paths, path-set SHA, bytes, text/PDF/image extents and roles.
- bind v1.0.23 process commits and P4 skip.
- bind JCP147 presence and Ref. 6/7 GNF/DOI conflict without promoting literature truth.
- validate cumulative Steps 64–69.2, exact outputs, gates, stop conditions and recovery pointers.
- execute named semantic, strict-JSON and real Git boundary negative controls.
- build validation JSON result-first and JSON-last.

### Activation C — exact commit and persistence

- independent review must report P0/P1/P2 counts.
- stage exact seven and reject any other staged/unstaged/untracked path.
- run Python 3.12 and 3.14 precommit modes.
- commit with exact expected parent and subject, then push immediately.
- verify local/upstream/tracking/live equality, committed paths/blob bytes, protected/main/Claude non-change and clean status.
- run Python 3.12 and 3.14 persistence modes against the actual commit.
- only `PASS_P064_PLAN_ACTIVATION_PERSISTENCE` permits Step 64.

## Phase 064 — v1.0.23 Reaudit

### Step 64 — Source/Process Topology and Full-read Attestation

#### Task 64A — immutable denominator

- reconstruct all 83 frozen manifest rows from Git blobs.
- verify exact path/blob/size/role/review-mode/extent identity.
- verify sorted path-set SHA and manifest indices.
- reconstruct v1.0.23 commit genealogy and last-touch identity.

#### Task 64B — full reads

- read 78 text files, 12,508/12,508 physical lines.
- inspect 3 PDFs, 129/129 pages using raw hash, extraction and visual render.
- inspect 2 images, 2/2 occurrences.
- attest no truncation, duplicate routing or source mutation.

#### Task 64C — process state

- distinguish plan, P0, P1, P2, P3, P4-skip and P5 records.
- distinguish reference ledger from adopted bibliography.
- route Phase 057 36 observations without treating them as conclusions.
- save source/process topology, read attestation and Step result first.

Gate: `PASS_P064_STEP64_SOURCE_PROCESS` only for internal inventory/read completeness.

### Step 65 — JCP147 and Ref. 6/7 Literature Authority

#### Task 65A — source acquisition and identity

- re-read JCP147 original 10/10 pages and exact bibliography entries.
- attempt lawful retrieval of Ref. 6/7 originals using exact DOI/title/official source routes.
- record source URL/access date/license/access status separately.
- absence, paywall or inaccessible full text remains `GROUND_NOT_FOUND`; metadata is not full text.

#### Task 65B — page/equation claims

- bind JCP147 Eqs. 32, 33, 34, 35–38 and 39 to page/equation anchors.
- bind three applicability conditions and degradation condition.
- create exact equation-slice hashes without excessive copyrighted quotation.
- separately classify Ref. 6/7 bibliographic identity and method-content authority.

#### Task 65C — conflicts and ceiling

- reject Ref. 7 DOI `10.1063/1.4802005` unless primary authoritative evidence overturns it.
- verify adopted bibliography versus stale reference ledger.
- if either Ref. 6/7 original remains unread, record an OPEN acquisition owner and cap the Phase at `CONDITIONAL_P064`.

### Step 66 — Ratio Closure and Transfer-function Rederivation

#### Task 66A — Fredholm source derivation

- independently derive Eq. 32 to Eq. 39 logic.
- separate exact transformations from the reference-ratio approximation.
- state domain, kernel directionality, boundary conditions and assumptions.

#### Task 66B — Volterra/ODE derivation

- derive frozen reference `r0`, nonlinear causal Volterra equation, ratio/Picard correction `r1` and local ODE equivalent.
- derive contraction/validity parameter and its dimensionless units.
- prove the frozen limit recovers the baseline path.
- reject literal Fredholm–Volterra identity.

#### Task 66C — transfer and computation

- derive `H(omega_V)=1/(1+i omega_V L_V)` in the voltage coordinate.
- prohibit time/EIS/instrument-response promotion.
- correct C-rate/timebase projection before approving any regime number.
- benchmark runtime and error for frozen/Picard/ratio routes; positive, zero or negative benefit are equally reportable.

### Step 67 — Algebraic/Volterra and Code/Runtime Boundary

#### Task 67A — problem classes

1. charge-balance algebraic root.
2. background algebraic self-consistency.
3. causal lag Volterra/ODE.

Only the third can receive a bounded ratio/reference route. The first two remain algebraic.

#### Task 67B — static identity

- map equations, symbols and code functions from frozen blobs.
- validate no double count between effective interaction/regular-solution quantities.
- distinguish static concordance from runtime behavior.

#### Task 67C — isolated runtime

- materialize frozen code in disposable external directories.
- execute only through subprocess; never import frozen production code into builder/validator.
- test frozen-off identity, new-option behavior, Picard/transfer identities, factor-3600 mutation and path/version mutation.
- verify active repository is byte-identical before/after runs and disposable outputs are cleaned.

### Step 68 — Validation-authority Adjudication

Classify every gate along separate axes:

- synthetic numerical.
- implementation regression.
- Picard/iteration behavior.
- transfer identity.
- material validation.
- experimental validation.
- external primary-literature validation.

P3/P5 `PASS`, round-trip, bit-exact, curve QA and adversarial review apply only to the axis they actually test. They do not create material/experimental truth. Save an authority matrix and route every overclaim/conflict to an owner.

### Step 69.1 — Source Disposition and Carry-forward Delta

- produce 83 source disposition rows and keep supplemental plan/literature/process inputs separate.
- preserve P4 skip as a process decision, not a discarded source.
- assign `CORRECT`, `PRESERVE`, `THEORY_ONLY`, `UNVERIFIED` or an explicitly justified equivalent.
- keep Ref. 6/7 acquisition debt OPEN until originals are read.
- route C-rate, transfer-axis, DOI, computational-benefit and authority conflicts losslessly.
- prevent ownerless or multiply-owned active routes.

### Step 69.2 — Integrated Validation, Lineage Report G and Final Gate

- replay activation and Steps 64–69.1 exact historical staged and persistence validators in disposable clones.
- pin commit, parent, subject, paths and validator hashes.
- strict-traverse every machine artifact and independently reconstruct high-risk equations/numerics.
- write Report G, Gate Result, Phase Result, ledgers and handover before validation JSON.
- write `PHASE_064_VALIDATION.json` last.
- parse output control documents structurally, not by global token presence.
- execute real disposable Git boundary mutations.
- run both Python 3.12 and 3.14 precommit and postcommit persistence.

## Phase Gate

### `PASS_P064_LINEAGE_G`

PASS requires all of the following:

1. all 83 frozen sources and supplemental process/literature inputs are identity-verified and fully read at the declared level.
2. JCP147 and both Ref. 6/7 originals are acquired and fully read.
3. exact bibliography, page/equation anchors and method claims have primary-source support.
4. ratio/reference substitution is rederived without conflating Fredholm and Volterra classes.
5. variable mapping and non-applicable algebraic assumptions are explicit.
6. transfer function remains voltage-coordinate bounded.
7. C-rate/timebase debt is resolved before quantitative regime approval.
8. actual computational benefit is benchmarked and reported without sign assumption.
9. synthetic/internal gates are separated from material/experimental authority.
10. all source/finding/carry routes are lossless and owner-complete.
11. exact-step commits, pushes and persistence terminals all pass.

### `CONDITIONAL_P064`

Use when internal lineage/read/derivation/runtime work is complete but one or both Ref. 6/7 originals remain unavailable, or another explicit external-authority dependency remains unresolved. Conditional status must carry an owner, acceptance criterion and target. It cannot be relabeled PASS through JCP147-only fallback.

### `FAIL_P064`

Use for denominator/read gaps, false source-presence claims, equation-anchor conflict, Fredholm/Volterra class conflation, unresolved unit error used as approved evidence, fabricated P4 state, escaped negative control, nondeterminism, repository boundary violation or contradictory control documents.

## Implementation Interfaces

### Source topology row

Required fields include occurrence ID, path, Git blob, byte size, role, review mode, extent, first/last commit, process stage, full-read state and evidence pointer.

### Literature authority row

Required fields include source ID, citation metadata, DOI, original-full-text status, raw hash, page/equation anchor, equation-slice hash, claim, authority tier, applicability assumption, contradiction/GNF state, downstream owner and acceptance criterion.

### Equation mapping row

Required fields include problem class, source equation, exact/approximate operation, domain, directionality, boundary/initial condition, variable map, dimension/unit, limiting recovery, non-applicable target, code symbol and evidence.

### Runtime row

Required fields include frozen blob, runtime, invocation, environment, input hash, output hash, metric, tolerance, complexity observation, repository-before/after projection, cleanup state and authority ceiling.

### Disposition row

Required fields include source/finding identity, evidence, disposition, reason, inherited owner, current owner, acceptance criterion, target Phase/Step, non-double-count basis and authority flags.

## Test and Validation Plan

### Strict artifact validation

- reject duplicate JSON keys, NaN, Infinity, numeric overflow and truncated JSON.
- full recursive traversal with node counts and schema/exact-key checks.
- canonical serialization and semantic hash.
- result-first and JSON-last atomic write.
- two independent deterministic reconstructions.

### Named semantic negative controls

At minimum cover:

- manifest path/blob/extent/page/line omission.
- Ref. 6/7 false-present and JCP147-as-substitute.
- wrong Ref. 7 DOI `10.1063/1.4802005`.
- reference-ledger/adopted-bibliography conflation.
- missing/fabricated P4 result.
- Eq. 32/33/34/37/39 anchor mutation.
- omission of any JCP applicability condition.
- Fredholm/Volterra class swap.
- algebraic root to integral-kernel promotion.
- first ratio/Picard iterate to exact/general convergence promotion.
- interaction-quantity double count.
- C-rate factor 3600 removal/inversion.
- voltage Fourier variable to time/EIS/instrument-response promotion.
- synthetic/internal gate to material/experimental truth promotion.
- claimed positive speedup without benchmark.
- ownerless/unresolvable correction evidence.
- result/ledger/handover status, parent, subject or persistence conflict.

Each named mutation must produce the exact intended diagnostic or exact intended diagnostic set; escaped and non-singleton failures are Gate failures.

### Git and persistence controls

- exact branch, parent, subject, path allowlist and staged/index/worktree equality.
- reject extra staged, unstaged and untracked files.
- active HEAD/upstream/tracking/live equality.
- protected local/tracking/live and main tracking/live fixed tips.
- `Claude/**` tracked/untracked diff zero.
- CRLF-equivalent normalized identities only where explicitly declared; raw blob identities otherwise.
- commit blob/worktree equality and clean postcommit status.
- disposable Git fixture cases for branch/upstream/HEAD/live/protected/main/Claude/path/diff-check mutations.

## Stop Conditions

Stop before commit when any of the following occurs:

- 83-source denominator or path-set hash mismatch.
- text/PDF/image coverage omission or truncation.
- Ref. 6/7 original absence is being relabeled as original verification.
- equation glyph/page/slice identity mismatch.
- Fredholm/Volterra equation classes cannot be kept distinct.
- JCP assumptions and graphite mapping cannot be separately grounded.
- C-rate/timebase is unresolved while regime numbers are being approved.
- actual computational-benefit measurement is absent but benefit is claimed.
- internal gate is promoted to material/experimental/primary-literature truth.
- P4 skip is lost, fabricated or treated as an execution failure.
- negative diagnostic escapes or is non-singleton outside a declared exact set.
- deterministic reconstruction differs.
- exact allowlist or Git/live/protected/main/Claude boundary fails.
- controller cannot re-establish the master plan, this plan and preceding result recovery chain.

## Assumptions

- Phase 056 manifest remains the frozen source-inventory authority; Step 64 independently verifies rather than trusts it.
- JCP147 local PDF is authentic to the recorded Git blob; bibliographic authenticity and equation content are rechecked in Step 65.
- Ref. 6/7 metadata is provisional until authoritative metadata and full text are separately verified.
- lawful source access may remain blocked. This produces `CONDITIONAL_P064`, not a fabricated fallback.
- runtime evidence can establish implementation behavior only for executed frozen inputs/environment.
- no Phase 064 audit result modifies scientific production artifacts.

## Correction History

- 2026-08-29: initial Phase 064 detailed plan stored after Phase 063 Step 63.2 commit/push and dual-runtime persistence.
- cumulative numbering continues from Step 63.2 to Step 64 and subdivides only final Step 69 into `69.1` and `69.2`.
- Phase 063 result-first/exact-path/JSON-last/persistence pattern is retained.
- v1.0.23 original plan's JCP147-only fallback is explicitly rejected as sufficient for the master Gate because the master plan requires Ref. 6/7 originals.
- P4 is recorded as intentionally skipped by decision, not inferred missing.
- Ref. 7 DOI conflict, stale reference-ledger boundary, voltage-coordinate transfer axis, C-rate factor 3600 and non-positive computational benefit are promoted to first-class validation controls.
