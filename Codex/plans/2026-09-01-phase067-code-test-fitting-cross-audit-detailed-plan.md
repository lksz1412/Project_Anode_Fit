# Phase 067 Code, Test, and Fitting Cross-Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to execute this plan one cumulative Step at a time. Every execution unit requires result-first records, independent review, an exact commit, push, and dual-runtime persistence before the next unit.

**Goal:** Reconstruct the complete v1.0.10–v1.0.25.2 Python, test, demo, golden, guide, and fitting lineage and close a theory–code–test–data conformance gate without altering production sources.

**Architecture:** Frozen Git blobs from the Phase 056 manifest are the source universe. Static full-read evidence, isolated runtime evidence, numerical/unit probes, and fitting provenance are kept as separate evidence axes and only joined through content-addressed matrices. Every claim retains a source pointer, observed behavior, authority ceiling, disposition, and one canonical owner.

**Tech Stack:** Git object database, Python 3.12 and 3.14, Python AST and strict JSON, repository-local Markdown plans/results, deterministic canonical JSON, disposable external runtime fixtures.

---

Date: 2026-09-01

Status: `ACTIVE_PENDING_ACTIVATION_PERSISTENCE`

Parent master plan: `Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`

Canonical completion master plan: `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`

Previous canonical result: `Codex/results/PHASE_066_RESULT.md`

Execution ledger: `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`

Canonical ledger: `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`

Recovery handover: `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

## Summary

Phase 067은 v1.0.10부터 v1.0.25.2까지 20개 release directory에 나타나는 모든
Python occurrence, unique Git blob, test, demo, golden artifact, fitting guide 및 실제
fitting 경로를 전수 교차감사한다. 파일명, docstring, test 이름, 성공한 과거 로그,
saved output 또는 최신 release라는 이유만으로 동작·물리·재료·외적 타당성을 채택하지
않는다.

이 phase는 다음을 서로 독립된 증거 축으로 유지한다.

1. occurrence path와 deduplicated Git blob identity,
2. module/function/class/state/input/output/call graph의 static behavior,
3. test/demo/golden의 실제 assertion·실행·fixture·failure behavior,
4. 단위·부호·극한·수치 guard의 독립 계산,
5. real-data fitting, synthetic/demo fitting 및 saved artifact의 provenance,
6. theory–code–test–data의 네 방향 conformance와 권위 ceiling.

누적 Step 번호는 `82–90`이며 Step 90은 source disposition을 먼저 persistence한 뒤
통합 gate를 닫기 위해 `90.1`과 `90.2`로 나눈다. 어느 substep도 새 integer Step을
만들지 않는다. 모든 execution unit은 result-first, canonical JSON-last, exact path
allowlist, 독립 검토, atomic commit, push/live-origin 확인, Python 3.12/3.14 persistence를
거친다.

**Step 82는 `PASS_P067_PLAN_ACTIVATION_PERSISTENCE`가 Python 3.12와 3.14에서 모두
확인되기 전에는 시작할 수 없다.**

## Current Ground Truth

### Git and predecessor boundary

- Active branch는 `codex/anode-fit-v1025_2-canonical-completion`이다.
- Phase 067 activation expected parent는
  `7241b331ff76bc8d43cb1bc6b69634977e0884a0`이다.
- 위 commit의 parent는 `bdad7375d70c3734cc63265d94a61dd82afd143d`, subject는
  `audit(phase066): close v1025 lineage gate`다.
- Phase 066 Step 81.2 exact-eight commit은 push/live-remote verified됐고 Python
  3.12/3.14에서 `PASS_P066_STEP81_2_PERSISTENCE`를 반환했다.
- Phase 066 selected gate는 `CONDITIONAL_P066`이며 persistence 성공으로
  `PASS_P066_LINEAGE_I`로 승격되지 않는다.
- Frozen Claude baseline은 `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`다.
- Protected branch `codex/lib-physics-endgame-v1025_2` tip은
  `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`이고 `main` tip은
  `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`이다.
- `Claude/**`, production Python, LaTeX, bibliography, figure, PDF, data, protected branch와
  `main`은 전 phase에서 read-only다.

### Frozen Python universe

Authoritative inventory는
`Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json`이다. Extension `py`인
occurrence를 20개 release에 투영하고 Git blob으로 deduplicate한 고정 분모는 다음과 같다.

| Surface | Occurrences | Unique Git blobs | Unique-blob physical lines |
|---|---:|---:|---:|
| all Python | `129` | `84` | `29,952` |
| production code role | `20` | `15` | Step 82에서 blob별 고정 |
| test role | `44` | `29` | Step 86에서 blob별 고정 |
| demo role | `30` | `26` | Step 86에서 blob별 고정 |
| result/tool Python role | `35` | `14` | Step 82/86에서 역할별 고정 |

Release denominator는 정확히 `20`이다.

`v1.0.10`, `v1.0.11`, `v1.0.12`, `v1.0.13`, `v1.0.14`, `v1.0.15`,
`v1.0.16`, `v1.0.17`, `v1.0.18.1`, `v1.0.18.2`, `v1.0.19`, `v1.0.20`,
`v1.0.21`, `v1.0.22`, `v1.0.23`, `v1.0.24`, `v1.0.24.1`, `v1.0.25`,
`v1.0.25.1`, `v1.0.25.2`다.

Occurrence `129`와 unique blob `84`를 더해 `213 sources`라고 부르지 않는다. Physical
line `29,952`는 unique Python blob을 한 번씩 계산한 분모이며 occurrence line sum이 아니다.

### Test, demo, golden, tool, and guide boundary

- Test는 `44` occurrences / `29` unique Git blobs다.
- Demo는 `30` occurrences / `26` unique Git blobs다.
- Golden artifacts는 `8` occurrences / `2` unique Git blobs다.
- Result/tool Python은 `35` occurrences / `14` unique Git blobs다.
- `FITTING_GUIDE`는 `20` occurrences / `8` unique Git blobs / `854` unique-blob physical
  lines다.
- Golden과 guide는 Python `129/84`에 합산하지 않는다.
- 동일 golden blob의 release 반복은 독립 실험 corroboration이 아니다.
- Test pass는 tested path의 bounded behavior만 증명하며 unexecuted branch, public default,
  물리적 정확성 또는 외적 타당성을 자동 증명하지 않는다.
- Demo의 print, plot, finite check 또는 정상 exit는 assertion과 구분한다.
- Guide의 self-report는 executable source나 fresh runtime보다 우선하지 않는다.

### Canonical predecessor evidence reuse

Phase 066 final canonical JSON은
`Codex/results/PHASE_066_VALIDATION.json`이며 committed LF SHA-256는
`2893670d87ab414c7243d0ed862ba19d2055d84260ca2f6f5c2ebc3ff5407577`, semantic
SHA-256는 `925556e534b9be49f4aed6d1889729d4f567350c5d09c6b09685d08442e3419e`다.
Final validator `Codex/work/v1025_phase066/validate_phase066_final.py`의 committed LF
SHA-256는 `7ae55f2d1d541aacc89ba7b067d3027f1f9af18635fb9b90dbdc7515d33bc164`다.

Phase 066 activation과 Steps 76, 77, 78, 79, 80, 81.1의 precommit/persistence 기록은
`7 + 7 = 14` canonical records다. Phase 067 activation은 이 14개를 다시 실행하거나
historical optimizer/fit을 재실행하지 않는다. Strict schema, semantic seal, output hash,
commit genealogy와 persistence terminal을 검증해 `CANONICAL_REUSED_14/14`,
`fresh_historical_replay=0/14`로 재사용한다.

### Active Phase 067 owner set

`Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json`에서 canonical owner가
`P067-CODE-HISTORY`인 active obligation은 정확히 세 건이다.

| Obligation | Origin | Required handling |
|---|---|---|
| `P065-OBL-0054` | `P065-S72-F04` | bounded scientific-authority finding을 외부 증거 없이 승격하지 않고 resolve 또는 explicit bound |
| `P066-OBL-0120` | `P066-P79-07` | empirical/physical authority observation을 canonical release 전 resolve 또는 explicit bound |
| `P066-OBL-0125` | `P066-R80-14` | saved loader/alias/export behavior를 source/runtime evidence로 resolve 또는 explicit bound |

Ownerless, duplicate owner, silent reassignment 또는 세 obligation의 backward projection을
허용하지 않는다.

### Preserved open authority boundary

- Ref. 7 original full text는 `GROUND_NOT_FOUND`; owner는
  `PHASE-071-PRIMARY-SOURCE-ACQUISITION`이다.
- Original full-precision optimizer state와 historical diagnostics는 `GROUND_NOT_FOUND`다.
- Held-out/external/material/specimen/protocol authority는 open이다.
- Current v1.0.25.2 PDFs는 stale이며 fresh build evidence가 아니다.
- Phase 067은 이 debt를 코드 behavior로 닫거나 authority를 승격하지 않는다.

## Phase Range

| Execution unit | Scope | Terminal required before next unit |
|---|---|---|
| Plan activation | Save this detailed plan and recovery contract | `PASS_P067_PLAN_ACTIVATION_PERSISTENCE` |
| Step 82 | Complete Python occurrence/blob full read and semantic topology | `PASS_P067_STEP82_PERSISTENCE` |
| Step 83 | Voltage/current/capacity/composition/temperature flow | `PASS_P067_STEP83_PERSISTENCE` |
| Step 84 | Charge, lag, kinetics, heat, observation call graph | `PASS_P067_STEP84_PERSISTENCE` |
| Step 85 | Mutable globals, defaults, profiles, imports and saved-state routes | `PASS_P067_STEP85_PERSISTENCE` |
| Step 86 | Test, demo, golden and guide actual-behavior audit | `PASS_P067_STEP86_PERSISTENCE` |
| Step 87 | Unit and numerical invariance checks | `PASS_P067_STEP87_PERSISTENCE` |
| Step 88 | Overflow, clipping, sorting, padding and fallback impacts | `PASS_P067_STEP88_PERSISTENCE` |
| Step 89 | Real-data versus synthetic/demo fitting authority | `PASS_P067_STEP89_PERSISTENCE` |
| Step 90.1 | Complete disposition and carry-forward delta | `PASS_P067_STEP90_1_PERSISTENCE` |
| Step 90.2 | Four-way conformance report and final gate | `PASS_P067_STEP90_2_PERSISTENCE` |

Step numbering은 master plan 전체에서 누적된다. Phase 067에서 Step 1이나 Step 82를
다시 시작하지 않으며 다음 phase는 cumulative Step 91로 시작한다.

## Exact Read Inputs

### Recovery controls at every boundary

각 unit 시작 전에 이 detailed plan, 직전 result, 두 execution ledgers와
`ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`를 1행부터 EOF까지 다시 읽는다. Activation은
추가로 다음을 strict/full-read한다.

- `Codex/results/PHASE_066_RESULT.md`
- `Codex/results/PHASE_066_STEP_081_2_GATE_RESULT.md`
- `Codex/results/PHASE_066_V1025_V1025_2_LINEAGE_REPORT_I.md`
- `Codex/results/PHASE_066_VALIDATION.json`
- `Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json`
- `Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json`
- persisted commit `7241b331ff76bc8d43cb1bc6b69634977e0884a0`

### Full-read requirements

- Step 82는 Python `129/129` occurrences를 `84/84` unique blobs에 projection하고 모든
  unique blob `29,952/29,952` physical lines를 1–EOF 읽는다.
- 모든 blob은 AST parse와 raw/LF hash, encoding, module/class/function/state/I/O signature,
  branch/error/fallback/side-effect coverage를 가진다.
- Step 86은 tests `44/44`와 unique blobs `29/29`, demos `30/30`과 unique blobs `26/26`,
  golden `8/8`과 blobs `2/2`, result/tool Python `35/35`, fitting guide `20/20`과
  blobs/lines `8/854`를 전수 disposition한다.
- Sparse checkout에 path가 없으면 baseline Git tree/blob을 먼저 읽는다. Git object가
  없거나 corrupt한 경우에만 stop한다.
- `READ_FULL`은 line/page/member/chunk coverage가 전부 있는 경우에만 사용한다.
- 동일 blob의 human read는 한 번 수행할 수 있으나 모든 occurrence path와 release가
  그 attestation에 lossless projection돼야 한다.

### Step 89 supplemental fitting inputs

Step 89는 Phase 066에서 routed된 다음 supplemental fit paths를 baseline Git object와
각 Step의 containing Git object에서 직접 읽는다. Directory label이나 sparse-checkout
presence로 blob identity를 추정하지 않는다.

| Path | Bounded role | Phase 080 saved-profile route |
|---|---|---|
| `Claude/results/comp_v24/sintef_data/sigr.csv` | Direct14 raw-data candidate; exact specimen/protocol authority remains separate | no |
| `Claude/results/comp_v24/sintef_data/SOURCES.md` | source/provenance statement; not raw data or proposition proof | no |
| `Claude/results/comp_v26_data/build_two_versions.py` | comparison builder | no |
| `Claude/results/comp_v26_data/test_skew_regsol_v2.py` | comparison test route | no |
| `Claude/results/comp_v26_data/bdd_dqdv.py` | comparison calculation helper | no |
| `Claude/results/comp_v26_data/test_gallery_vs_regsol.py` | gallery/regular-solution comparison test | no |
| `Claude/results/comp_v26_data/out_versions/summary_versions.json` | saved comparison summary | no |
| `Claude/results/comp_v26_data/out_versions/A_regsol/params_blend.json` | saved regular-solution profile | yes |
| `Claude/results/comp_v26_data/out_versions/B_gallery/params_blend.json` | saved gallery profile | yes |
| `Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json` | saved skew profile | yes |

각 row는 baseline/containing commit, tree path, Git blob OID, mode, raw bytes SHA-256,
byte extent와 role을 가진다. 실제 tree/blob가 없으면 `GROUND_NOT_FOUND`로 중단·기록하며
다른 file이나 generated output으로 대체하지 않는다. `comp_v26_data`와 A/B/C output은
comparison/saved-route evidence일 뿐 canonical baseline, release, held-out, external 또는
material authority로 승격하지 않는다.

## Non-goals and Scope Guards

- `Claude/**`, production Python/LaTeX/bibliography/figure/PDF/data를 수정하지 않는다.
- Phase 067에서는 defect repair, refactor, new API, new model, new default, fitting parameter
  재선택, final equation 또는 canonical manuscript를 작성하지 않는다.
- Test를 통과시키기 위해 source나 fixture를 고치지 않는다.
- Historical output을 재생성 output으로 덮어쓰지 않는다.
- Missing real data를 synthetic/demo data로 대체하지 않는다.
- Stored parameter vector를 original optimizer state로 부르지 않는다.
- Guide claim, demo output 또는 test state를 public default나 production behavior로 승격하지 않는다.
- Ref. 7 metadata/DOI/secondary source를 original proposition support로 사용하지 않는다.
- Stale PDF를 rebuild하거나 publication-ready로 부르지 않는다.
- Phase 068의 Claude/Codex fork 판정을 선행하지 않는다.
- No production change is authorized by this audit phase.

### Scholarly-body code-mention prohibition

Phase 067 plan/result/machine evidence와 implementation companion은 구현 식별자를 기록할
수 있다. 학술 정본 main body, caption, footnote 및 visible heading에는 code, function,
class, file, schema key, API, test, commit, branch, phase, step 또는 작업 이력을 언급하지
않는다. Phase 067은 main scholarly body 자체를 수정하지 않는다. 후속 문건 반영이 필요하면
수식·변수·가정·유도·물리/화학 해석만 scholarly owner에 전달하고 구현 설명은 지정된
appendix/companion owner로 분리한다.

## Implementation Changes

### Global execution-unit contract

각 unit은 다음 순서로 실행한다.

1. expected parent, branch/upstream/live origin, protected/main refs와 recovery inputs를 확인한다.
2. exact source universe를 Git objects에서 구성하고 source-policy negative controls를 먼저 확인한다.
3. bounded builder가 machine evidence를 만들고 human result를 먼저 저장한다.
4. 두 ledgers와 handover를 갱신한 뒤 canonical validation JSON을 마지막에 수집한다.
5. Python 3.12/3.14, independent specification/quality review를 수행한다.
6. P0/P1/P2 `0/0/0`과 exact path/mode/status가 확인된 때만 commit/push한다.
7. live-origin equality와 dual-runtime persistence PASS 뒤 다음 unit으로 이동한다.

Builders/validators는 frozen Git objects와 선언된 `Codex/**` inputs만 읽는다. Network,
package installation, arbitrary dynamic import, shell string execution, undeclared Git mutation,
production import 또는 repository source mutation을 허용하지 않는다. Runtime이 필요한 경우
Git blobs를 system temp 또는 repository 밖 disposable root에 materialize하고 전후 source
hash 및 cleanup을 확인한다.

## Plan Activation Unit — Save Before Step 82

### Exact-seven path allowlist

1. `Codex/plans/2026-09-01-phase067-code-test-fitting-cross-audit-detailed-plan.md`
2. `Codex/work/v1010_v1025_2_reaudit/validate_phase067_plan.py`
3. `Codex/results/PHASE_067_PLAN_ACTIVATION_VALIDATION.json`
4. `Codex/results/PHASE_067_PLAN_ACTIVATION_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

### Activation tasks

1. expected parent를 `7241b331ff76bc8d43cb1bc6b69634977e0884a0`으로 고정한다.
2. predecessor selected gate `CONDITIONAL_P066`, exact-eight commit/push/live-remote 및 dual-runtime
   `PASS_P066_STEP81_2_PERSISTENCE`를 검증한다.
3. Phase 066 final validator/JSON hashes와 canonical history `14/14`를 strict 검증한다.
4. manifest에서 Python/test/demo/golden/result/tool/FITTING_GUIDE 분모를 독립 재계산한다.
5. P067 owner가 위 세 obligation뿐임을 strict 검증한다.
6. Steps `82–90.2`, exact outputs, triad gates, scope guards와 authority ceilings를 파싱한다.
7. human result와 ledgers/handover를 먼저 저장하고 validation JSON을 마지막에 수집한다.
8. exact-seven 외 staged path, rename, deletion, non-`100644`, wrong parent/subject/gate를 fail한다.

Commit subject는 정확히 다음과 같다.

`docs(phase067): plan code test fitting cross-audit`

Precommit status map은 path order 기준 정확히 `A/A/A/A/M/M/M`이다. Postcommit validator는
exact-seven paths/modes/blob bytes, parent, subject, clean worktree, local/upstream/tracking/live
origin equality, protected/main/Claude non-change를 확인하고
`PASS_P067_PLAN_ACTIVATION_PERSISTENCE`를 출력한다.

## Phase 067 — Code, Test, and Fitting Cross-Audit

### Step 82 — Complete Python Source Topology and Full Read

**Goal:** `129/84/29,952` source identity와 20-release projection을 고정하고 모든 unique
Python blob을 module/function/class/state/I/O 수준으로 1–EOF 검독한다.

**Exact-eight outputs:**

1. `Codex/work/v1025_phase067/build_phase067_step82.py`
2. `Codex/work/v1025_phase067/validate_phase067_step82.py`
3. `Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json`
4. `Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json`
5. `Codex/results/PHASE_067_STEP_082_SOURCE_TOPOLOGY_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status in this order: `A/A/A/A/A/M/M/M`.

**Tasks and checks:**

- occurrence→blob→release and role projection을 exact bijection으로 만든다.
- 각 unique blob에 first introducing commit, 이후 touch commits, path history와
  rename/copy classification을 부여한다. Genealogy row는 commit/tree/blob/mode/parent/time/subject
  contract를 모두 포함하며 directory timestamp나 later self-report로 대체하지 않는다.
- introducing/touch/rename/copy commit genealogy는 `git log --follow`의 convenience output만
  신뢰하지 않고 parent tree와 current tree의 path/blob/mode를 대조한다. Rename/copy는
  similarity claim과 exact blob/path evidence를 분리하고 ambiguous relation을 추정하지 않는다.
- AST definition은 nested definition까지 포함하고 signature/default/annotation/return,
  state read/write, exceptions, fallbacks, imports, side effects를 기록한다.
- parser failure, unread line, orphan occurrence/blob, role substitution은 0이어야 한다.
- no test/runtime claim is made in this Step.

Commit subject: `audit(phase067): freeze complete python topology`.

Required terminal: `PASS_P067_STEP82_PERSISTENCE`.

### Step 83 — State-Quantity Flow Audit

**Goal:** voltage, current, capacity, composition과 temperature가 public input에서 내부 state,
calculation 및 output까지 이동하는 경로를 release별로 연결한다.

**Exact-seven outputs:**

1. `Codex/work/v1025_phase067/build_phase067_step83.py`
2. `Codex/work/v1025_phase067/validate_phase067_step83.py`
3. `Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json`
4. `Codex/results/PHASE_067_STEP_083_STATE_FLOW_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status in this order: `A/A/A/A/M/M/M`.

**Tasks and checks:**

- 각 quantity에 definition, unit/basis/sign, producer, transform, consumer와 output을 부여한다.
- current A, C-rate h^-1, normalized rate s^-1를 분리하고 implicit conversion을 기록한다.
- capacity Ah/C, mass/capacity fraction 및 total-capacity denominator를 분리한다.
- global/representative/local composition과 temperature를 별도 state identity로 둔다.
- direct, inherited, overwritten, ignored, fallback path를 exclusive classification한다.

Commit subject: `audit(phase067): trace state quantity flows`.

Required terminal: `PASS_P067_STEP83_PERSISTENCE`.

### Step 84 — Physics Call-Graph Audit

**Goal:** charge-balance root, background/self-consistency, lag/trajectory, kinetics, heat와
observation transformation의 실제 호출 순서와 state dependency를 고정한다.

**Exact-seven outputs:**

1. `Codex/work/v1025_phase067/build_phase067_step84.py`
2. `Codex/work/v1025_phase067/validate_phase067_step84.py`
3. `Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json`
4. `Codex/results/PHASE_067_STEP_084_PHYSICS_CALL_GRAPH_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status in this order: `A/A/A/A/M/M/M`.

**Tasks and checks:**

- algebraic root, causal Volterra/ODE memory와 observation postprocessing을 분리한다.
- fresh public entry에서 ordered/contiguous call path와 branch predicate를 기록한다.
- option-off, missing-kinetics, zero-current, reversal, rest와 invalid-root behavior를 분리한다.
- equilibrium, finite-rate, thermal 및 observation order를 theory claim과 cross-reference한다.
- absent call edge를 prose/self-report로 채우지 않는다.

Commit subject: `audit(phase067): reconstruct physics call graph`.

Required terminal: `PASS_P067_STEP84_PERSISTENCE`.

### Step 85 — Mutable State, Defaults, Profiles, Imports, and Persistence

**Goal:** mutable globals/class state, constructor defaults, profile selection, import side effects,
aliases/exports와 saved loader behavior를 fresh-process 기준으로 분리한다.

**Exact-eight outputs:**

1. `Codex/work/v1025_phase067/build_phase067_step85.py`
2. `Codex/work/v1025_phase067/validate_phase067_step85.py`
3. `Codex/results/PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX.json`
4. `Codex/results/PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION.json`
5. `Codex/results/PHASE_067_STEP_085_STATE_DEFAULT_IMPORT_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status in this order: `A/A/A/A/A/M/M/M`.

**Tasks and checks:**

- clean process fresh import before any mutation을 강제한다.
- explicit profile, test mutation, global alias, repeated import와 execution-order permutation을 실행한다.
- available loader/schema/export를 실제 frozen source에서 찾고 absent surface는 `GROUND_NOT_FOUND`로 둔다.
- `P066-OBL-0125/P066-R80-14`을 saved loader/alias/export 증거에 직접 연결한다.
- order-dependent state leakage와 serialization roundtrip을 public default와 구분한다.

Commit subject: `audit(phase067): separate defaults state persistence`.

Required terminal: `PASS_P067_STEP85_PERSISTENCE`.

### Step 86 — Test, Demo, Golden, Tool, and Guide Behavior

**Goal:** tests `44/29`, demos `30/26`, golden `8/2`, result/tool Python `35/14`와
FITTING_GUIDE `20/8/854`의 실제 assertion·execution·artifact·claim 범위를 전수 판정한다.

**Exact-eight outputs:**

1. `Codex/work/v1025_phase067/build_phase067_step86.py`
2. `Codex/work/v1025_phase067/validate_phase067_step86.py`
3. `Codex/results/PHASE_067_TEST_DEMO_GOLDEN_MATRIX.json`
4. `Codex/results/PHASE_067_GUIDE_TOOL_CONFORMANCE_MATRIX.json`
5. `Codex/results/PHASE_067_STEP_086_TEST_DEMO_GOLDEN_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status in this order: `A/A/A/A/A/M/M/M`.

**Tasks and checks:**

- test별 collected/executed/skipped/assertion/failure-path/fixture/mutation/cleanup을 기록한다.
- demo의 print/plot/finite/manual observation과 gating assertion을 분리한다.
- golden member/schema/dtype/shape/value/hash와 overwrite behavior를 직접 검사한다.
- result/tool script의 inputs, hard-coded path, optional dependency, outputs와 enforcement를 기록한다.
- guide claim을 actual source/test/runtime evidence와 연결하고 stale claim을 보존한다.
- untested code가 동작한다고 가정하지 않는다.

Commit subject: `audit(phase067): adjudicate test demo golden behavior`.

Required terminal: `PASS_P067_STEP86_PERSISTENCE`.

### Step 87 — Unit and Numerical Invariance Checks

**Goal:** C-rate/seconds, energy, entropy, heat와 capacity basis를 독립 수치 계산으로 확인한다.

**Exact-seven outputs:**

1. `Codex/work/v1025_phase067/build_phase067_step87.py`
2. `Codex/work/v1025_phase067/validate_phase067_step87.py`
3. `Codex/results/PHASE_067_UNIT_NUMERICAL_CHECK_MATRIX.json`
4. `Codex/results/PHASE_067_STEP_087_UNIT_NUMERICAL_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status in this order: `A/A/A/A/M/M/M`.

**Required probes:**

- same physical C-rate의 h^-1↔s^-1 invariance 및 exact factor `3600`,
- current sign/reaction direction/zero-current equilibrium,
- Ah↔C energy and heat conversion without duplicate `3600`,
- entropy coefficient and reversible heat sign/unit,
- mass fraction, capacity fraction, component/total capacity and dQ/dV area closure,
- finite difference versus analytic derivative with declared tolerance.

Commit subject: `audit(phase067): verify units numerical invariants`.

Required terminal: `PASS_P067_STEP87_PERSISTENCE`.

### Step 88 — Numerical Guard and Fallback Impact

**Goal:** overflow, clipping, sorting, padding, interpolation, root fallback와 numerical default가
곡선·보존식·물리적 해석에 미치는 영향을 경계별로 정량화한다.

**Exact-seven outputs:**

1. `Codex/work/v1025_phase067/build_phase067_step88.py`
2. `Codex/work/v1025_phase067/validate_phase067_step88.py`
3. `Codex/results/PHASE_067_NUMERICAL_GUARD_IMPACT_MATRIX.json`
4. `Codex/results/PHASE_067_STEP_088_NUMERICAL_GUARD_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status in this order: `A/A/A/A/M/M/M`.

**Tasks and checks:**

- 각 guard의 trigger predicate, returned value/state, warning/error와 silent behavior를 기록한다.
- clipping 전후 area/center/sign/continuity/monotonicity delta를 계산한다.
- sorting/padding이 trajectory causality 또는 sample correspondence를 바꾸는지 확인한다.
- nonconverged root/optimizer result를 success로 승격하지 않는다.
- fallback을 intended model behavior와 구분하고 physical ceiling을 부여한다.

Commit subject: `audit(phase067): bound numerical guard impacts`.

Required terminal: `PASS_P067_STEP88_PERSISTENCE`.

### Step 89 — Real, Synthetic, Demo, and Saved-Fit Authority

**Goal:** real-data fit, reconstructed/synthetic/demo routes, saved curves/metrics와 original
optimizer evidence를 서로 다른 provenance objects로 판정한다.

**Exact-eight outputs:**

1. `Codex/work/v1025_phase067/build_phase067_step89.py`
2. `Codex/work/v1025_phase067/validate_phase067_step89.py`
3. `Codex/results/PHASE_067_FITTING_EVIDENCE_MATRIX.json`
4. `Codex/results/PHASE_067_FITTING_RUNTIME_ATTESTATION.json`
5. `Codex/results/PHASE_067_STEP_089_FITTING_AUTHORITY_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status in this order: `A/A/A/A/A/M/M/M`.

**Tasks and checks:**

- data path/blob/columns/units/basis/specimen/protocol/preprocessing/weighting을 찾는다.
- parameter order/initial/bounds/free mask/objective/seed/solver/tolerance를 고정한다.
- real, synthetic, reconstructed, demo와 saved-only rows를 exclusive classification한다.
- training/in-sample, held-out, external, material/protocol authority를 분리한다.
- historical optimizer fit을 무조건 재실행하지 않고 Phase 066 sealed evidence를 재사용한다.
- `P065-OBL-0054/P065-S72-F04`와 `P066-OBL-0120/P066-P79-07`을 explicit bound한다.

Commit subject: `audit(phase067): separate fitting evidence authority`.

Required terminal: `PASS_P067_STEP89_PERSISTENCE`.

### Step 90.1 — Complete Disposition and Carry-Forward Delta

**Goal:** Python/test/demo/golden/guide/tool occurrence와 Step 82–89 finding을 lossless
disposition하고 active owners를 고정한다.

**Exact-eight outputs:**

1. `Codex/work/v1025_phase067/build_phase067_step90_dispositions.py`
2. `Codex/work/v1025_phase067/validate_phase067_step90_dispositions.py`
3. `Codex/results/PHASE_067_SOURCE_DISPOSITION_MATRIX.json`
4. `Codex/results/PHASE_067_CARRY_FORWARD_DELTA.json`
5. `Codex/results/PHASE_067_STEP_090_1_DISPOSITION_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status in this order: `A/A/A/A/A/M/M/M`.

**Tasks and checks:**

- 129 Python occurrences/84 blobs와 non-Python audit surfaces를 각각 exact row에 연결한다.
- `PRESERVE/CORRECT/WITHHOLD/DISCARD/GROUND_NOT_FOUND`를 exclusive 적용한다.
- three active Phase 067 owners를 resolve 또는 explicit bound하고 silent drop을 금지한다.
- new defects에는 one canonical owner, acceptance criterion, authority ceiling을 부여한다.
- Ref. 7/original optimizer/held-out/external/material/stale-PDF owners를 그대로 보존한다.

Commit subject: `audit(phase067): disposition code test fitting evidence`.

Required terminal: `PASS_P067_STEP90_1_PERSISTENCE`.

### Step 90.2 — Theory–Code–Test–Data Conformance and Final Gate

**Goal:** 모든 persisted Phase 067 evidence를 four-way matrix와 exclusive final gate로 봉인한다.

**Exact-eight outputs:**

1. `Codex/work/v1025_phase067/validate_phase067_final.py`
2. `Codex/results/PHASE_067_VALIDATION.json`
3. `Codex/results/PHASE_067_THEORY_CODE_TEST_DATA_CONFORMANCE_REPORT.md`
4. `Codex/results/PHASE_067_STEP_090_2_GATE_RESULT.md`
5. `Codex/results/PHASE_067_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Required status in this order: `A/A/A/A/A/M/M/M`.

**Tasks and checks:**

- persisted Steps 82–90.1 exact commits/artifacts와 invocation history를 strict 검증한다.
- theory–code, code–test, test–data, theory–data 네 축을 independent status로 둔다.
- no-axis evidence는 `GROUND_NOT_FOUND/NOT_TESTED/NOT_APPLICABLE`로 보존한다.
- human reports와 recovery records를 먼저, validation JSON을 마지막에 생성한다.
- selected gate를 report/result/ledgers/handover에 exact 일치시킨다.
- P0/P1/P2 `0/0/0`, exact commit/push/live-origin, dual-runtime persistence를 요구한다.

Commit subject: `audit(phase067): close code history gate`.

Required terminal: `PASS_P067_STEP90_2_PERSISTENCE`.

## Phase Gate

Final validator는 다음 세 gate 중 정확히 하나를 선택한다.

### `PASS_P067_CODE_HISTORY`

다음 조건이 모두 참일 때만 선택한다.

1. Python `129/84/29,952`와 20 releases가 complete-read 및 disposition됐다.
2. test `44/29`, demo `30/26`, golden `8/2`, result/tool `35/14`, fitting guide
   `20/8/854`가 전수 판정됐다.
3. voltage/current/capacity/composition/temperature와 charge/lag/kinetics/heat/observation
   call graph가 source와 runtime으로 연결됐다.
4. mutable globals/default/profile/import/saved routes가 fresh-process evidence로 분리됐다.
5. C-rate/sec, energy/entropy/heat/capacity basis와 numerical guards가 독립 검산됐다.
6. real/synthetic/demo/saved fit authority가 분리되고 missing evidence가 명시됐다.
7. 모든 theory–code–test–data row에 source, status, ceiling 및 owner가 있다.
8. 모든 unique Python blob과 test path가 coverage에 있고 untested code를 working으로
   가정하지 않는다.
9. three Phase 067 owners와 모든 new finding이 lossless disposition됐다.
10. Steps 82–90.1의 persistence가 모두 확인되고 current Step 90.2 precommit review가
    P0/P1/P2 `0/0/0`이다. Step 90.2 자신의 commit/push/persistence는 content Gate 선택 뒤
    별도 terminal에서만 확인하며 content Gate의 선행조건으로 순환 참조하지 않는다.

이 gate는 code-history audit completeness이며 primary-literature, external material/experimental
truth, held-out validation, unique parameter identifiability, final model/manuscript/PDF 또는
publication readiness를 뜻하지 않는다. Ref. 7 original text, original optimizer state,
held-out/external/material authority와 stale-PDF debt는 `PASS_P067_CODE_HISTORY`에서도
authority ceiling/open carry로 남으며 Phase 067 gate 선택 determinant가 아니다.

### `CONDITIONAL_P067`

Source identity/read/disposition coverage와 lossless owner routing은 완결됐지만 Phase 067이
직접 소유한 required internal code-history/test/behavior cell 중 하나 이상이 다음 상태일 때만
선택한다.

- required runtime가 dependency/environment로 실행되지 않아 bounded `NOT_TESTED`인 경우,
- required internal route/behavior가 absent internal artifact 또는 blocked reachability 때문에
  `GROUND_NOT_FOUND` 또는 `PARTIAL`인 경우,
- saved loader/alias/export 또는 fitting route의 required internal behavior cell이 source/runtime
  evidence로 완결되지 않았지만 exact absence와 owner가 lossless하게 기록된 경우.

`CONDITIONAL_P067`는 open claim을 승인하지 않는다. 내부 coverage와 owner routing이 완전한
경우 persistence 후 Phase 068로 진행할 수 있다.

Ref. 7, original optimizer, held-out/external/material authority와 stale-PDF 상태만으로
`CONDITIONAL_P067`을 선택하지 않는다. 이 known external/open debt는 PASS와 CONDITIONAL
모두에서 동일 ceiling으로 보존되고 gate determinant가 아니다.

### `FAIL_P067`

다음 중 하나라도 해당하면 선택한다.

- source/test/demo/golden/guide 분모 또는 full-read coverage가 불완전하다.
- occurrence, blob, line, release 또는 role 분모를 혼합한다.
- untested code, print-only demo 또는 stale guide를 working behavior로 가정한다.
- current test mutation을 fresh public default로 보고한다.
- unit/sign/basis factor, call order, fallback 또는 fitting provenance를 누락한다.
- synthetic/demo/saved output을 real/held-out/external evidence로 승격한다.
- missing optimizer/Ref. 7/material/stale-PDF evidence를 추정으로 닫는다.
- ownerless/duplicate/lost carry 또는 authority promotion이 있다.
- JSON/determinism/source-policy/exact path/Git protection/remote persistence가 실패한다.

`FAIL_P067`는 incomplete identity/read/disposition, lost owner, false authority promotion 또는
validation/Git failure에만 적용한다. Required internal coverage가 완전하면 FAIL이 아니며,
모든 required internal behavior cell이 complete면 PASS, bounded internal GNF/NOT_TESTED/PARTIAL
cell이 하나 이상이면 CONDITIONAL이다. 세 gate는 이 규칙으로 mutually exclusive and exhaustive다.

Content gate와 persistence terminal은 별도다. Content가
`PASS_P067_CODE_HISTORY` 또는 `CONDITIONAL_P067`이어도
`PASS_P067_STEP90_2_PERSISTENCE` 전에는 Phase 067 recovery point가 완결되지 않는다.

## Canonical-Evidence Reuse Protocol

- Phase 066 historical validator/optimizer/fit을 Phase 067 activation에서 재실행하지 않는다.
- Committed final JSON/validator bytes, semantic seal, exact commit and remote persistence를 검증한다.
- Canonical Phase 066 history denominator는 `14/14`, fresh replay는 `0/14`다.
- Phase 067 각 unit은 own precommit/persistence record만 새로 만들며 과거 evidence를
  current execution처럼 중복 계수하지 않는다.
- JSON semantic content에는 absolute workspace path, username, volatile timestamp 또는 temp
  random suffix를 넣지 않는다.

## Implementation Interfaces

Machine envelope는 schema/artifact/phase/step/date, baseline/expected parent, input identities,
authority boundary, result-first/JSON-last, gate와 semantic SHA-256을 가진다. Source row는
occurrence path/release/role/blob/mode/bytes/lines/read status, AST row는 qualified identity,
signature/state/I/O/calls/branches/errors/fallbacks, runtime row는 Python/argv/cwd/input/output/
exit/stdout/stderr/cleanup/hash, conformance row는 theory/code/test/data status와 ceiling/owner를
갖는다.

Canonical JSON은 UTF-8, sorted keys, stable separators, LF line ending 및 terminal LF 하나를
사용한다. Semantic hash field 자체를 제외한 canonical semantic projection을 hash한다.

## Test and Validation Plan

### Runtime matrix

- Python 3.12: compile, content, staged precommit, persistence.
- Python 3.14: compile, content, staged precommit, persistence.
- 하나라도 unavailable이면 성공으로 추정하지 않고 stop한다.

### Positive controls

- exact parent/subject/path/status/mode, source manifest and predecessor hashes,
- `129/84/29,952`, 20 releases, role partitions, test/demo/golden/guide counts,
- three P067 owners, Steps `82–90.2`, triad gate and authority ceilings,
- result-first/canonical JSON-last/determinism `2/2`,
- local/upstream/tracking/live-origin equality and protected/main/Claude non-change.

### Negative controls

Count/role/blob/line/release mutation, missing Step/substep, wrong gate/parent/subject/terminal,
P066 gate promotion, history replay inflation, lost owner, Ref. 7/optimizer/held-out/external/material/
stale-PDF promotion, source/test/demo/guide authority substitution, scholarly code mention, extra path,
rename/delete/wrong mode, dirty worktree와 protected/main/Claude drift를 named singleton으로 reject한다.

Validators fail closed on duplicate JSON keys, nonfinite numbers, deep/unbounded structures, dynamic
subprocess, shell execution, arbitrary Git argv, filesystem mutation outside declared atomic JSON
collection, dynamic import/dunder lookup 또는 undeclared network access. Injected negative payload는
실행하지 않는다.

## Stop Conditions

다음 중 하나면 즉시 중단하고 result/handover에 기록한다.

1. expected parent/remote/protected/main/persistence가 틀린다.
2. `129/84/29,952`, 20 releases 또는 role/artifact/guide 분모를 재현할 수 없다.
3. unread blob/line, parser failure, orphan occurrence 또는 truncated output을 해소할 수 없다.
4. source/test/demo/golden/guide/runtime 역할을 분리할 수 없다.
5. unit/sign/basis/current/temperature/capacity state를 식별할 수 없다.
6. missing real data/state/source를 합성해 fit/authority claim을 만들려 한다.
7. production/Claude/protected/main 변경 또는 scholarly main-body code mention이 필요하다.
8. P0/P1 finding이 남거나 push/persistence가 세 번 실패한다.
9. credentials, paid source, external approval 또는 사용자 과학 선택이 필요하다.

Open evidence는 허위로 닫지 않는다. 내부 감사가 완결되면 GNF/NOT_TESTED와 owner를
보존하고 `CONDITIONAL_P067`로 닫을 수 있다.

## Assumptions

- Frozen Git objects, Phase 056 manifest와 persisted Phase 066 evidence가 readable/immutable하다.
- Python 3.12/3.14가 있으며 package availability 차이는 evidence로 기록한다.
- Production repair와 manuscript authoring은 범위 밖이다.
- Stored claims are evidence queues, not truth labels.
- Three Phase 067 owners와 all open authority debts는 evidence 없이 자동 해소되지 않는다.

## Correction History

- 2026-09-01: persisted `CONDITIONAL_P066`에서 cumulative Steps `82–90.2` 계획을 최초 작성했다.
- 2026-09-01: manifest에서 Python `129/84/29,952`, 20 releases와 role별 분모를 고정했다.
- 2026-09-01: tests `44/29`, demos `30/26`, golden `8/2`, result/tool `35/14`,
  FITTING_GUIDE `20/8/854`를 별도 분모로 고정했다.
- 2026-09-01: P067 active owner 3건과 Phase 066 canonical history reuse `14/14`, fresh replay
  `0/14`를 고정했다.
- 2026-09-01: `PASS_P067_CODE_HISTORY`, `CONDITIONAL_P067`, `FAIL_P067` exclusive gate와
  no-production/no-authority-promotion 경계를 고정했다.
