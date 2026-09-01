# Phase 066 v1.0.25–v1.0.25.2 Lineage Reaudit Implementation Plan

Date: 2026-09-01
Status: `ACTIVE_PENDING_ACTIVATION_PERSISTENCE`
Parent master plan: `Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`
Canonical completion master plan: `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`
Previous canonical result: `Codex/results/PHASE_065_RESULT.md`
Execution ledger: `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
Canonical ledger: `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
Recovery handover: `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

## Summary

Phase 066은 frozen v1.0.25, v1.0.25.1 및 v1.0.25.2 계보를 source-complete,
process-complete, behavior-separated 방식으로 재감사한다. 세 directory의 파일 수,
release label, 성공한 내부 fit, 성공한 test, 생성된 PDF 또는 handover의 완료 문구를
그 자체로 과학적 권위로 채택하지 않는다.

이 phase의 핵심은 다음 여섯 경계를 독립적으로 재현하는 것이다.

1. 세 version directory의 실제 path/blob delta와 도입 commit 계보,
2. skew profile의 식과 도함수 및 direct14 fitting의 수학·수치·데이터 흐름,
3. 저장된 8자리 parameter vector와 원 optimizer state의 증거 차이,
4. direct14의 경험적 적합 성공과 물질 phase-decomposition 해석의 권한 차이,
5. 4+2, 7+7 및 source-declared profile/default의 실제 fresh-import·온도 경로,
6. v1.0.25.2가 채택 가능한 baseline인 범위와 잔존 결함.

누적 Step 번호는 76–81을 유지한다. Step 81은 source disposition을 먼저 원격
persistence한 뒤 최종 Lineage Report I gate를 닫기 위해 81.1과 81.2로 나눈다.
어느 substep도 새 integer Step을 만들지 않는다.

모든 execution unit은 result-first, exact-path allowlist, independent review,
atomic commit, push/fetch 및 dual-runtime persistence를 거친다. Machine evidence는
human-readable result와 ledger/handover가 먼저 고정된 뒤 validation JSON을 마지막에
수집·stage하는 `validation-JSON-last` 규칙을 따른다.

**Step 76은 `PASS_P066_PLAN_ACTIVATION_PERSISTENCE`가 Python 3.12와 3.14에서 모두
확인되기 전에는 시작할 수 없다.**

## Current Ground Truth

### Git and protection state

- Active branch는 `codex/anode-fit-v1025_2-canonical-completion`이다.
- Plan activation expected parent는
  `a2920fba07ab9ce75191134f0d68ed3b6ffda4e5`다.
- 위 commit은 Phase 065 Step 75.2의 commit/push/fetch 및 remote persistence가
  확인된 canonical predecessor다.
- Phase 065 selected gate는 `CONDITIONAL_P065`다.
- `CONDITIONAL_P065`는 persistence 성공으로 `PASS_P065_LINEAGE_H`로 승격되지 않는다.
- Frozen Claude source baseline은
  `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`다.
- 최신 Claude review lineage tip은
  `e3e1a634f34b711aa4803fd190fe9120f1755f13`다.
- `Claude/**`, protected branch 및 `main`은 전 phase에서 read-only다.
- Phase 066은 `Codex/**`의 명시된 plan/work/result 기록만 생성·수정한다.
- 각 unit 진입 시 local HEAD, upstream tracking ref 및 live `origin`이 직전
  persistence commit과 동일해야 한다.
- untracked 또는 staged extra path가 있으면 다음 unit에 진입하지 않는다.

### Frozen v1.0.25–v1.0.25.2 manifest denominator

Authoritative inventory는
`Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json`이다.
Phase 066 slice는 다음 값으로 고정한다.

| Measure | Frozen value |
|---|---:|
| Manifest occurrence indices, zero-based | `1087–1519` |
| Manifest occurrence ordinals, one-based | `1088–1520` |
| Total path occurrences | `433` |
| v1.0.25 occurrences | `143` |
| v1.0.25.1 occurrences | `144` |
| v1.0.25.2 occurrences | `146` |
| Unique Git blobs | `167` |
| Occurrence bytes | `26,391,541` |
| Unique-blob bytes | `12,483,701` |
| FULL_TEXT unique blobs | `158` |
| FULL_TEXT physical lines | `30,597` |
| FULL_PDF unique blobs/pages | `6 / 308` |
| FULL_IMAGE unique blobs | `3` |

Occurrence path-set SHA-256는 sorted UTF-8 paths를 LF로 결합해 계산한
`3c9bf954a5db4df5ce01a96ff8834f9e9284e6e35fdcecbfae0c3ae6b430b382`다.
같은 row order에서 path와 blob 사이에 NUL을 둔 path-plus-blob SHA-256는
`b3620bf1a76758cad818e9ea7ece5441ea88b86f8f030bb715f48e054086655c`다.
Sorted unique blob set의 SHA-256는
`f1982cf050f88b7145d5ea1a6afdf124316da1332afec9028ae6119730080bfa`다.

Manifest occurrence 433과 unique-blob read denominator 167을 합쳐 `600 sources`라고
부르지 않는다. 전자는 version history, 후자는 deduplicated review denominator다.

### Actual version deltas

세 archive는 byte-identical mirror가 아니다. Step 76은 다음 delta를 독립 재계산하고
각 changed path의 old/new blob과 introducing commit을 저장한다.

| Comparison | Shared paths | Same blobs | Changed blobs | Added paths |
|---|---:|---:|---:|---:|
| v1.0.25 → v1.0.25.1 | `143` | `133` | `10` | `1` |
| v1.0.25.1 → v1.0.25.2 | `144` | `133` | `11` | `2` |
| v1.0.25 → v1.0.25.2 | `143` | `127` | `16` | `3` |

새 relative paths는 다음 세 개다.

- `results/V1025_1_TOUCHUP_NOTE.md`
- `results/HANDOVER_v1025_2.md`
- `results/KERNEL_COMPARISON_REPORT_v1025_2.html`

경로 추가, blob 변경, commit 도입 및 현재 문구의 권위를 서로 분리한다.

### Stale v1.0.25.2 PDF boundary

- v1.0.25.2의 PDF 3개는 v1.0.25.1 대응 PDF와 동일 Git blobs다.
- 이 PDF들은 v1.0.25.2 source delta를 반영한 build evidence가 아니다.
- PDF의 존재, 정상 open 또는 과거 compile log는 v1.0.25.2 release build PASS가 아니다.
- Phase 066은 production LaTeX를 rebuild하거나 PDF를 교체하지 않고 후속 owner로 carry한다.

### Narrative and process denominators

Phase 066의 minimum narrative denominator는 `42 documents / 9,674 physical lines`다.

- `40` documents와 `9,019` lines는 frozen manifest-backed narrative queue다.
- `Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md`는 root
  supplemental process record이며 blob
  `c471f29944d766588b71dc026bc179f84f419e95`, `240` lines다.
- `Claude/results/HANDOVER_v1025_2_CARRYOVER.md`는 root supplemental process
  record이며 blob `76c248e76430dbfcd3915b4cbebadce46a5d3593`, `415` lines다.
- 두 root supplemental은 433 manifest occurrences에 합산하지 않는다.

Release process denominator는 `17` commits이며 digest prefix는 `f094…`다.
Routed process denominator는 `20` commits이며 digest prefix는 `57062…`다.
두 digest의 64-hex canonical value와 직렬화 규칙은 Step 76에서 immutable machine
artifact에 전부 저장하고 prefix만으로 비교하지 않는다.

- First selected process commit:
  `edbc4a2c68cda0dd21662cb6dd68ba8bed699a76`.
- Last selected process commit:
  `e3e1a634f34b711aa4803fd190fe9120f1755f13`.
- Release 17은 핵심 genealogy, routed 20은 supplemental lineage를 포함한 상위 universe다.
- Release 17을 complete process history로 보고하지 않는다.
- Step 76은 parents, subject, timestamp, changed paths 및 diff relevance를 모두 검증한다.

### Mandatory Phase 057 routing inputs

다음 observation documents를 filename이나 과거 summary만으로 대체하지 않고
1행부터 EOF까지 직접 읽는다.

- `Codex/results/PHASE_057AO_V1025_ARCHIVE_TOUCHUP_OBSERVATIONS.md`
- `Codex/results/PHASE_057AP_V1025_DATA_ADDENDUM_OBSERVATIONS.md`
- `Codex/results/PHASE_057AQ_V1025_CASCADE_LEDGER_OBSERVATIONS.md`
- `Codex/results/PHASE_057AR_V1025_T13_T14_OBSERVATIONS.md`
- `Codex/results/PHASE_057AS_V1025_DOC_EDIT_OBSERVATIONS.md`
- `Codex/results/PHASE_057AT_V1025_HANDOVER_INDEX_OBSERVATIONS.md`
- `Codex/results/PHASE_057AU_V1025_MERGE_READINESS_OBSERVATIONS.md`
- `Codex/results/PHASE_057AV_V1025_2_ARCHIVE_OBSERVATIONS.md`
- `Codex/results/PHASE_057AW_V1025_2_HANDOVER_OBSERVATIONS.md`
- `Codex/results/PHASE_057AY_V1024_SNAPSHOT_V1025_2_KERNEL_REPORT_OBSERVATIONS.md`

AO–AW는 `INTENT-PROV-0293–0387`의 `95` IDs를 라우팅한다. AY는
`INTENT-PROV-0395–0404`의 `10` IDs를 포함하지만 Phase 065에도 읽기·라우팅된 shared
observation이다. AY를 Phase 066에서 새 독립 의무로 이중 계수하지 않고 origin과 현재
owner를 보존한다.

### Recovered scientific and authority boundary

- Area-preserving skew나 direct14 in-sample 개선은 물질 parameter, phase count, gallery,
  species identity 또는 물리적 필연성의 증거가 아니다.
- 저장 문건의 8자리 vector는 raw input, preprocessing, weighting, bounds 및 original
  optimizer provenance와 아직 완전히 결합되지 않았다.
- Original full-precision state, active mask, gradient 및 covariance/Hessian 원 기록은
  `GROUND_NOT_FOUND`다. Step 77은 입력을 찾거나 GNF로 판정하고 Step 78은 역발명하지 않는다.
- Legacy 4-transition default, skew7 opt-in, 4+2/7+7 및 temperature dependence는 문구가
  아니라 fresh-import value/derivative/route로 확인한다.
- Kernel report는 room-temperature in-sample curve evidence이며 외적 타당성이 아니다.
- `direct14`와 `direct-14`는 같은 14-component empirical fit route를 뜻하고,
  `8-digit`와 `eight-digit`는 저장된 표시 정밀도만 뜻한다.
- `v1.0.26A` and `v1.0.26B` comparison artifacts are not a release and are not
  part of the frozen 433-occurrence denominator.
- N10 background aliasing은 저장된 absolute BIC와 fitted parameter의 권위를 막는
  provenance defect이며, 원 입력으로 재피팅하기 전에는 해소됐다고 기록하지 않는다.
- `GROUND_NOT_FOUND` means no source is available for the named authority claim;
  this audit authorizes no code or production-document edit.
- Ref. 7 original full text는 `GROUND_NOT_FOUND`, owner는
  `PHASE-071-PRIMARY-SOURCE-ACQUISITION`이다. Metadata나 secondary source로 대체하지 않는다.

## Phase Range

| Execution unit | Scope | Terminal required before next unit |
|---|---|---|
| Plan activation | Save this detailed plan and recovery contract | `PASS_P066_PLAN_ACTIVATION_PERSISTENCE` |
| Step 76 | Source/process delta and complete-read attestation | `PASS_P066_STEP76_PERSISTENCE` |
| Step 77 | Skew derivative and direct14 fitting reproduction | `PASS_P066_STEP77_PERSISTENCE` |
| Step 78 | Stored vector and optimizer-state binding | `PASS_P066_STEP78_PERSISTENCE` |
| Step 79 | Empirical-fit and physical-authority separation | `PASS_P066_STEP79_PERSISTENCE` |
| Step 80 | Profile/default/temperature runtime verification | `PASS_P066_STEP80_PERSISTENCE` |
| Step 81.1 | Complete source disposition and carry-forward delta | `PASS_P066_STEP81_1_PERSISTENCE` |
| Step 81.2 | Integrated validation, Lineage Report I and final gate | `PASS_P066_STEP81_2_PERSISTENCE` |

Step numbering은 전체 master에서 누적된다. Phase 066 내부에서 Step 1 또는 Step 76을
다시 시작하지 않는다. 다음 phase는 cumulative Step 82로 시작한다.

## Exact Read Inputs

### Recovery controls at every boundary

각 unit 시작 전에 이 plan, 직전 step result, 두 execution ledgers와
`ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`를 1행부터 EOF까지 다시 읽는다.

Activation에서는 추가로 다음 predecessor evidence를 strict-validate한다.

- `Codex/results/PHASE_065_VALIDATION.json`
- `Codex/results/PHASE_065_V1024_V1024_1_LINEAGE_REPORT_H.md`
- `Codex/results/PHASE_065_STEP_075_2_GATE_RESULT.md`
- `Codex/results/PHASE_065_RESULT.md`
- persisted commit `a2920fba07ab9ce75191134f0d68ed3b6ffda4e5`

Predecessor validation은 Phase 065의 historical 21-call replay를 다시 실행하지 않는다.
Committed JSON의 strict schema, canonical serialization, semantic SHA-256, output hashes,
selected `CONDITIONAL_P065`, Ref. 7 owner 및 remote persistence를 검증해 immutable
canonical predecessor evidence로 재사용한다.

### Source reads

Step 76은 frozen Git objects에서 다음을 직접 읽는다.

- manifest occurrences `433/433`,
- unique blobs `167/167`,
- FULL_TEXT blobs `158/158`와 lines `30,597/30,597`,
- FULL_PDF blobs `6/6`와 pages `308/308`,
- FULL_IMAGE blobs `3/3`,
- narrative documents `42/42`와 lines `9,674/9,674`,
- release process commits `17/17`,
- routed process commits `20/20`,
- Phase 057 AO–AW 및 AY documents 전부.

Sparse worktree에 파일이 없다는 이유로 `GROUND_NOT_FOUND`를 선언하지 않는다. 먼저
baseline Git tree와 blob을 읽고, Git object 자체가 없거나 corrupt할 때만 stop한다.

### Full-read rules

- Text는 1–EOF, decode, nonblank count와 LF hash; PDF는 page 1–end inspection; image는
  dimensions/mode/bytes와 visual inspection을 기록한다.
- Python과 JSON은 extension이 아니라 observed bytes와 parser result로 분류한다.
- 동일 blob의 human full-read는 한 번 수행할 수 있지만 모든 occurrence path를 그 blob의
  read attestation에 projection한다.
- Changed blobs는 양쪽 전문을 읽고, truncation은 작은 range 재독으로 해소한다.
- `READ_FULL`은 모든 line/page/chunk coverage가 artifact에 존재할 때만 사용한다.

## Non-goals and Scope Guards

- `Claude/**`와 production Python/LaTeX/bibliography/figure/PDF를 수정하지 않는다.
- skew/direct14를 고치거나 새 model/default/final parameter set을 선택하지 않는다.
- Phase 069 이전에 final equation/model/default를 채택하지 않는다.
- stale PDF를 rebuild하지 않고 Ref. 7을 metadata/secondary source로 `FOUND` 처리하지 않는다.
- raw dataset이 없을 때 synthetic data를 원 데이터로 대체하지 않는다.
- stored 8-digit vector를 original full-precision optimizer state라고 부르지 않는다.
- test state를 public default로, in-sample metric을 external validation으로, fit component를
  phase/gallery/species identity로 승격하지 않는다.
- derived HTML/PDF가 source, runtime 또는 원 실험 기록보다 우선하지 않는다.
- Phase 057 provisional finding을 무비판 승격하거나 새 과학 선택을 대신 내리지 않는다.

### Scholarly-body code-mention prohibition

Phase 066 audit plan, `Codex/work/**`, machine JSON 및 implementation companion 기록은
구현 식별자를 명시할 수 있다. 그러나 학술 정본의 main body, caption, footnote,
visible heading에는 code, function, class, file, schema key, API, test, commit, branch,
phase, step 또는 작업 이력을 언급하지 않는다.

학술 본문으로 carry하는 내용은 수식, 변수 정의, 가정, 유도, 물리·화학적 해석 및
검증된 문헌 권한만 포함한다. 구현 설명이 필요한 경우 지정된 implementation appendix
또는 별도 companion owner로만 라우팅한다. Phase 066은 학술 본문 자체를 쓰지 않는다.

## Implementation Changes

### Global execution-unit contract

각 unit은 아래 순서를 지킨다.

1. expected parent, branch/protected refs와 recovery inputs를 확인·전문 재독한다.
2. source-policy negatives를 RED로 증명한 뒤 bounded builder로 evidence를 만든다.
3. human result, 두 ledgers와 handover를 저장하고 exact staged allowlist를 검증한다.
4. validation JSON을 deterministic/atomic 방식으로 마지막에 생성한다.
5. Python 3.12/3.14와 independent science/security/records reviews를 수행한다.
6. P0/P1/P2 `0/0/0`일 때만 exact subject로 commit/push/fetch한다.
7. remote equality와 dual-runtime persistence PASS 후 다음 unit으로 이동한다.

Builders와 validators는 source Git objects와 선언된 `Codex/**` inputs만 읽는다.
Network, package install, shell string execution, arbitrary filesystem mutation 및
undeclared Git mutation을 허용하지 않는다. Temporary fixture는 system temp 아래에서만
생성하고 성공·실패 모두 cleanup을 검증한다.

## Plan Activation Unit — Save Before Step 76

### Exact-seven path allowlist

1. `Codex/plans/2026-09-01-phase066-v1025-v1025_2-lineage-detailed-plan.md`
2. `Codex/work/v1025_phase066/validate_phase066_plan.py`
3. `Codex/results/PHASE_066_PLAN_ACTIVATION_VALIDATION.json`
4. `Codex/results/PHASE_066_PLAN_ACTIVATION_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

### Tasks

1. expected parent를 `a2920fba07ab9ce75191134f0d68ed3b6ffda4e5`로 고정한다.
2. predecessor gate가 `CONDITIONAL_P065`임을 검증한다.
3. Phase 065 persisted artifact hashes와 live remote equality를 검증한다.
4. plan의 Steps 76–81, exact denominators, Ref. 7 carry 및 scope guards를 파싱한다.
5. exact-seven 이외 staged path가 있으면 fail한다.
6. missing plan token, count mutation, wrong parent/subject 및 gate promotion negative controls를
   실행한다.
7. activation result와 ledgers/handover를 result-first로 저장한다.
8. validation JSON을 마지막에 생성한다.

Commit subject는 정확히 다음과 같다.

`docs(phase066): plan v1025 lineage reaudit`

Postcommit validator는 exact-seven committed paths, committed bytes, subject, parent,
remote equality, clean status 및 protected/non-change를 검증하고
`PASS_P066_PLAN_ACTIVATION_PERSISTENCE`를 출력한다.

**이 terminal이 두 runtime에서 PASS하기 전에는 Step 76 builder 또는 산출물을 만들지 않는다.**

## Phase 066 — v1.0.25/v1.0.25.2 Reaudit

### Step 76 — Source, Process and Complete-Read Topology

### Goal

433 occurrences, 167 unique blobs, 42 narrative documents, release 17 및 routed 20의
identity와 delta를 재현하고 모든 source/process input의 complete-read attestation을
고정한다.

### Exact-eight path allowlist

1. `Codex/work/v1025_phase066/build_phase066_step76.py`
2. `Codex/work/v1025_phase066/validate_phase066_step76.py`
3. `Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json`
4. `Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json`
5. `Codex/results/PHASE_066_STEP_076_SOURCE_PROCESS_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

### Tasks

1. manifest slice 1087–1519와 세 canonical hashes를 독립 재계산한다.
2. occurrence별 path/blob/mode/bytes/role/review/extent를 보존한다.
3. 세 pairwise delta와 모든 changed/added path의 introducing commit/parent를 검증한다.
4. stale PDF 3개의 v1.0.25.1/v1.0.25.2 blob 동일성을 기록한다.
5. 40 manifest narrative와 두 root supplemental을 분리해 읽는다.
6. release 17/routed 20의 full digests, serialization과 first/last/parent edges를 저장한다.
7. AO–AW/AY IDs를 origin-preserving route로 결합하고 AY duplicate를 0으로 만든다.
8. machine extent와 human binding을 분리하고 unread/partial/orphan을 0으로 만든다.

### Validation and persistence

- Count/hash/delta/process/read-coverage mutation마다 named negative control을 둔다.
- Filename extension과 observed bytes가 다를 때 observed bytes가 우선해야 한다.
- Rerun은 volatile path/time 없이 byte-identical canonical JSON을 생성해야 한다.
- Commit subject:
  `audit(phase066): freeze v1025 source process delta`.
- 다음 unit 전 required terminal:
  `PASS_P066_STEP76_PERSISTENCE`.

### Step 77 — Skew Derivative and Direct14 Fit Reproduction

### Goal

Frozen source의 skew profile을 독립적으로 재유도하고 direct14 fitting의 raw input부터
stored result까지 실제 수학·수치·데이터 흐름을 재현한다. 문서의 성공 문구나 저장된
숫자를 실행 증거로 대체하지 않는다.

### Exact-eight path allowlist

1. `Codex/work/v1025_phase066/build_phase066_step77.py`
2. `Codex/work/v1025_phase066/validate_phase066_step77.py`
3. `Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json`
4. `Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json`
5. `Codex/results/PHASE_066_STEP_077_FIT_REPRODUCTION_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

### Mathematical tasks

1. base profile, skew transform, normalization, domains와 chain rule을 수식으로 전개한다.
2. area/center/sign/limit/zero-skew를 검산하고 analytic derivative를 수치차분과 비교한다.
3. piecewise/clipping/overflow branches를 probe하고 parameter label을 물질 의미로 승격하지 않는다.

### Data and runtime tasks

1. raw path/blob/columns/units/basis/specimen/protocol과 preprocessing/weighting을 찾는다.
2. parameter order, initial state, bounds, free mask, objective, seed, solver/tolerances를 고정한다.
3. Python 3.12/3.14 disposable environments에서 actual fit을 실행하고 logs/result를 보존한다.
4. stored report/vector/curve와 reproduced result를 사전 선언 tolerance로 비교한다.
5. synthetic/reconstructed inputs는 raw data와 분리하고 누락은 `GROUND_NOT_FOUND`로 남긴다.
6. 누락을 추정으로 채워 `REPRODUCED`라고 선언하지 않는다.

### Validation and persistence

- Derivative sign, normalization, parameter order, data hash, bound 또는 objective mutation이
  반드시 fail하도록 negative controls를 둔다.
- Runtime success와 scientific validity는 별도 fields와 gates로 저장한다.
- 실제 optimizer execution은 이 step에서 한 번 수행하고 immutable inputs/logs/hashes를
  봉인한다. 후속 validator는 비싼 fit을 반복하지 않고 봉인 증거를 검증한다.
- Commit subject:
  `audit(phase066): reproduce skew direct14 fitting`.
- 다음 unit 전 required terminal:
  `PASS_P066_STEP77_PERSISTENCE`.

### Step 78 — Stored Vector and Original Optimizer-State Binding

### Goal

문건의 8자리 vector, 재현된 returned vector 및 original optimizer state를 서로 다른
evidence objects로 비교한다. 원 state가 없으면 그 부재를 명시적으로 보존한다.

### Exact-seven path allowlist

1. `Codex/work/v1025_phase066/build_phase066_step78.py`
2. `Codex/work/v1025_phase066/validate_phase066_step78.py`
3. `Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json`
4. `Codex/results/PHASE_066_STEP_078_OPTIMIZER_VECTOR_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

### Tasks

1. displayed 8-digit tokens를 원문 bytes와 보존하고 full precision으로 오인하지 않는다.
2. reproduced vector와 component/objective/curve rounding delta를 계산한다.
3. success/status/evaluations, bounds, active mask와 boundary solution을 분리 기록한다.
4. gradient/Jacobian/covariance/Hessian 계열의 실제 저장 여부를 필드별 판정한다.
5. missing original state는 `GROUND_NOT_FOUND`로 두고 새 결과를 historical state로 투영하지 않는다.
6. non-identifiability, rounding ambiguity 및 equivalent minima를 분리한다.

### Validation and persistence

- 8-digit/full-precision substitution, fabricated optimizer fields, wrong parameter ordering,
  tolerance widening 및 missing-state promotion을 negative controls로 차단한다.
- `IDENTICAL`, `TOLERANCE_EQUIVALENT`, `NOT_EQUIVALENT`, `GROUND_NOT_FOUND`를 exclusive
  status로 사용한다.
- Commit subject:
  `audit(phase066): bind optimizer state vector`.
- 다음 unit 전 required terminal:
  `PASS_P066_STEP78_PERSISTENCE`.

### Step 79 — Empirical Fit and Physical Authority Separation

### Goal

direct14, skew profile 및 competing profile의 empirical performance를 material phase,
gallery, species 또는 thermodynamic mechanism에 대한 authority와 분리한다.

### Exact-seven path allowlist

1. `Codex/work/v1025_phase066/build_phase066_step79.py`
2. `Codex/work/v1025_phase066/validate_phase066_step79.py`
3. `Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json`
4. `Codex/results/PHASE_066_STEP_079_AUTHORITY_RESULT.md`
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

### Required matrix axes

각 claim row는 claim/source pointer, dataset/specimen/protocol/basis, profile/parameter count,
in-sample metric, held-out evidence, noise/weighting, information criterion, identifiability,
independent structural/thermodynamic support, empirical/physical ceilings 및 owner를 갖는다.

### Tasks

1. direct14를 observed metric/data scope로 한정하고 RT를 multi-temperature로 확장하지 않는다.
2. curve basis나 parameter label을 phase/gallery/species evidence로 승격하지 않는다.
3. holdout/noise/information/identifiability 누락은 `GROUND_NOT_FOUND`/`NOT_TESTED`로 둔다.
4. material claim은 exact proposition owner로, Ref. 7은 Phase 071 owner로 라우팅한다.
5. `empirical_pass=true`가 `physical_authority=true`를 자동 설정하지 못하게 한다.

### Validation and persistence

- In-sample-to-external promotion, component-to-phase promotion, metadata-to-proposition
  promotion 및 missing evidence omission을 named negative controls로 둔다.
- 모든 authority claim은 source pointer와 ceiling 없이는 fail한다.
- Commit subject:
  `audit(phase066): separate fit and material authority`.
- 다음 unit 전 required terminal:
  `PASS_P066_STEP79_PERSISTENCE`.

### Step 80 — Profile, Default and Temperature Verification

### Goal

4+2, 7+7 및 source-declared alternative profiles의 static route와 actual runtime behavior를
구분하고, fresh-import public default와 temperature dependence를 독립 검증한다.

### Exact-eight path allowlist

1. `Codex/work/v1025_phase066/build_phase066_step80.py`
2. `Codex/work/v1025_phase066/validate_phase066_step80.py`
3. `Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json`
4. `Codex/results/PHASE_066_RUNTIME_ATTESTATION.json`
5. `Codex/results/PHASE_066_STEP_080_PROFILE_TEMPERATURE_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

### Static tasks

1. public import/default/profile routes와 4+2, 7+7 및 다른 variants를 AST로 고정한다.
2. legacy/saved/alias/fallback과 test-mutated/production defaults를 분리한다.
3. 문서, guide, static literal 및 runtime 관찰을 다른 evidence columns로 둔다.

### Runtime tasks

1. test mutation 전 clean process에서 fresh public default를 기록한다.
2. 4+2, 7+7, remaining profiles와 legacy/serialized routes를 독립 실행한다.
3. 실행 순서 permutation으로 global-state leakage를 검사한다.
4. 두 개 이상 valid temperature에서 value/derivative/contributions/limits를 비교한다.
5. Python 3.12/3.14의 stdout/stderr/exit/cleanup을 저장한다.

### Validation and persistence

- Fresh-import-before-mutation 순서를 validator가 강제한다.
- Test-only default, omitted profile, temperature-independent false positive, order leakage,
  runtime-only authority promotion을 negative controls로 차단한다.
- Runtime agreement는 frozen implementation behavior의 증거일 뿐 외부 물질 타당성 PASS가 아니다.
- Commit subject:
  `audit(phase066): verify profile default temperature routes`.
- 다음 unit 전 required terminal:
  `PASS_P066_STEP80_PERSISTENCE`.

### Step 81.1 — Complete Disposition and Carry-Forward Delta

### Goal

433 occurrence paths와 167 unique blobs를 lossless disposition에 연결하고 inherited/new
obligations의 정확한 canonical owner를 고정한다.

### Exact-eight path allowlist

1. `Codex/work/v1025_phase066/build_phase066_step81_dispositions.py`
2. `Codex/work/v1025_phase066/validate_phase066_step81_dispositions.py`
3. `Codex/results/PHASE_066_SOURCE_DISPOSITION_MATRIX.json`
4. `Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json`
5. `Codex/results/PHASE_066_STEP_081_1_DISPOSITION_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

### Tasks

1. 각 occurrence에 exactly one row를 만들고 unique blob projection을 보존한다.
2. root supplemental은 별도 rows, release/routed commits는 orphan 0으로 유지한다.
3. Phase 057 IDs의 origin/owner를 보존하고 AY duplicate를 0으로 만든다.
4. Step 76–80을 `PRESERVE/CORRECT/WITHHOLD/DISCARD/GROUND_NOT_FOUND`로 판정한다.
5. empirical/physical axes를 분리하고 각 defect에 단일 owner/acceptance를 준다.
6. Ref. 7 status/Phase 071 owner를 carry하며 ownerless/multiple owners를 0으로 만든다.
7. closed route를 근거 없이 reopen하거나 open route를 drop하지 않는다.

### Validation and persistence

- Orphan occurrence, duplicate disposition, ownerless blocker, multiple owner, lost inherited ID,
  Ref. 7 promotion 및 stale-PDF closure를 negative controls로 둔다.
- Commit subject:
  `audit(phase066): disposition v1025 lineage evidence`.
- 다음 unit 전 required terminal:
  `PASS_P066_STEP81_1_PERSISTENCE`.

### Step 81.2 — Integrated Lineage Report I and Final Gate

### Goal

모든 persisted Phase 066 evidence를 통합해 Lineage Report I, exclusive gate 및 next-phase
recovery boundary를 봉인한다.

### Exact-eight path allowlist

1. `Codex/work/v1025_phase066/validate_phase066_final.py`
2. `Codex/results/PHASE_066_VALIDATION.json`
3. `Codex/results/PHASE_066_V1025_V1025_2_LINEAGE_REPORT_I.md`
4. `Codex/results/PHASE_066_STEP_081_2_GATE_RESULT.md`
5. `Codex/results/PHASE_066_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

### Tasks

1. Steps 76–81.1 commits/artifacts와 source/read/process/delta hashes를 strict 검증한다.
2. math/fit/optimizer/authority/profile/disposition assertions를 cross-bind한다.
3. human documents 먼저, exact-inventory/hash/semantic final JSON을 마지막에 생성한다.
4. exclusive gate를 모든 result/ledger/handover에 동일하게 쓴다.
5. next expected parent는 postcommit persistence에서만 확정한다.
6. independent reviews의 P0/P1/P2 `0/0/0`을 요구한다.

### Validation and persistence

- Commit subject:
  `audit(phase066): close v1025 lineage gate`.
- Postcommit validator는 exact-eight paths와 committed bytes를 검증한다.
- local/upstream/tracking/live-origin equality와 clean status를 검증한다.
- Python 3.12와 3.14가 모두
  `PASS_P066_STEP81_2_PERSISTENCE`를 출력해야 한다.
- Final persistence 전에는 Phase 067/Step 82를 시작하지 않는다.

## Phase Gate

Final validator는 다음 세 gate 중 정확히 하나를 선택한다.

### `PASS_P066_LINEAGE_I`

다음 조건이 모두 참일 때만 선택한다.

1. 433/167 source identities와 모든 read/page/image coverage가 완전하다.
2. 42 narrative documents와 release 17/routed 20 genealogy가 완전하다.
3. pairwise delta와 stale PDF 판정이 재현된다.
4. pinned raw input, preprocessing 및 objective로 actual direct14 fit이 재현된다.
5. stored 8-digit vector와 original optimizer state의 관계가 근거로 확정된다.
6. fresh-import/default, 4+2, 7+7, other profiles 및 temperature routes가 실제 관찰된다.
7. empirical fit와 material authority가 완전히 분리된다.
8. 모든 source/process/finding/carry row에 단일 canonical owner가 있다.
9. load-bearing source 또는 optimizer provenance가 `GROUND_NOT_FOUND`가 아니다.
10. Ref. 7 original full text와 필요한 exact proposition support가 lawful evidence로 확보된다.
11. P0/P1/P2가 `0/0/0`이고 exact commit/push/persistence가 성공한다.

### `CONDITIONAL_P066`

내부 lineage audit와 disposition은 완결됐지만 다음 중 하나 이상이 남을 때 선택한다.

- raw direct14 input 또는 preprocessing provenance가 `GROUND_NOT_FOUND`,
- original full-precision optimizer state가 `GROUND_NOT_FOUND`,
- held-out/external/material authority evidence가 부족,
- stale PDF의 후속 build owner가 open,
- Ref. 7 original full text가 `GROUND_NOT_FOUND`.

현재 Ref. 7 상태가 유지되는 한 `PASS_P066_LINEAGE_I`로 승격하지 않는다.
`CONDITIONAL_P066`는 open claim을 승인하지 않지만, 모든 debt가 lossless owner와 acceptance
condition을 가진 경우 persistence 후 다음 lineage phase로 진행할 수 있다.

### `FAIL_P066`

다음 중 하나라도 해당하면 선택한다.

- source/process identity 또는 full-read coverage가 불완전함,
- manifest와 supplemental denominators를 합침,
- actual fit을 실행하지 않고 `REPRODUCED`라고 주장함,
- missing raw data 또는 optimizer state를 추정으로 채움,
- test-mutated state를 fresh public default로 보고함,
- profile 또는 temperature routes를 서로 혼동함,
- empirical metric을 phase/material authority로 승격함,
- Ref. 7 DOI/metadata를 proposition support로 사용함,
- source disposition 또는 carry owner가 유실·중복됨,
- validator가 deterministic evidence를 재현하지 못함,
- exact staged path, Git protection 또는 remote persistence가 실패함.

Gate의 content selection과 postcommit persistence는 별도다. Content가
`PASS_P066_LINEAGE_I` 또는 `CONDITIONAL_P066`여도
`PASS_P066_STEP81_2_PERSISTENCE` 전에는 Phase 066 recovery point가 완결되지 않는다.

## Canonical-Evidence Reuse Protocol

### Predecessor reuse

- Phase 065 historical 21-call replay를 Phase 066에서 다시 실행하지 않는다.
- Phase 065 committed validation artifact의 strict schema, canonical bytes, semantic hash,
  output hashes, remote commit 및 terminal을 검증해 predecessor evidence로 재사용한다.
- self-rehashed 또는 uncommitted predecessor artifact는 허용하지 않는다.

### Phase 066 invocation history

Activation과 Steps 76, 77, 78, 79, 80, 81.1의 각 validator에 canonical precommit 1회와
persistence 1회를 선언한다. Final history denominator는 `7 + 7 = 14` records다.

- Step 81.2 explicit `--collect`만 이 14-record current-phase history를 한 번 수집한다.
- 이후 ordinary `--precommit`과 `--persistence`는 strict-validated stored canonical history를
  재사용하고 `fresh_historical_replay=0/14`를 보고한다.
- Metadata recollection은 historical optimizer fit을 새로 실행했다고 주장하지 않는다.
- Stored record의 args에서 system temp absolute path만 deterministic `<TEMP>/...`로
  normalize하고 실제 execution argv는 변경하지 않는다.
- Reuse 시 unit sequence, commits, validator hashes, terminal, pass/exit/stderr/cleanup,
  protected state 및 active branch invariants를 전부 재검증한다.
- Step 77 actual fitting은 Step 77 runtime evidence이며 14 validator records의 반복 실행과
  별개다.

## Implementation Interfaces

Machine envelope는 schema/artifact/phase/step/date, baseline/input/parent, inputs,
source contract, authority boundary, result-first, gate와 semantic SHA를 가진다.
Source records는 path/blob/raw-LF hashes/extent/read binding, runtime records는
runtime/argv/cwd/input/logs/exit/cleanup/result hashes를 가진다. Optimizer records는
displayed/reproduced/original state, precision/order/bounds/mask/objective/diagnostics를
분리하고 authority records는 empirical/physical ceilings를 분리한다.

Canonical JSON은 UTF-8, sorted keys, stable separators, LF line ending 및 terminal LF 하나를
사용한다. Semantic hash field 자체를 제외한 canonical semantic projection을 hash한다.
Absolute local workspace path, username, volatile timestamp 또는 temp random suffix를
semantic content에 넣지 않는다.

## Test and Validation Plan

### Runtime matrix

- Python 3.12: compile, unit precommit, final precommit, persistence.
- Python 3.14: compile, unit precommit, final precommit, persistence.
- 둘 중 하나라도 unavailable이면 성공으로 추정하지 않고 stop한다.

### Required positive controls

Parent/subject/path allowlist, frozen hashes, read coverage, process graph, pairwise delta,
derivative/direct14 evidence, vector-state classification, fresh profile/temperature routes,
disposition ownership, gate/JSON-last 및 remote persistence를 모두 확인한다.

### Required negative controls

Named probes는 path/hash/count/read/process/delta mutation, denominator fusion, stale-PDF
promotion, AY duplication, derivative/data/order/bounds mutation, synthetic-as-raw,
failed-fit-as-reproduced, 8-digit-as-full-state, fabricated diagnostics, empirical-to-material
promotion, test-state-as-default, omitted profile/temperature route, Ref. 7 metadata promotion,
owner loss/duplication, scholarly code mention, wrong gate/parent/subject/terminal, extra path와
protected/main/Claude change를 모두 reject한다.

No injected negative-control payload may execute. Validators fail closed on dynamic subprocess,
filesystem mutation, arbitrary Git argv, dynamic import/dunder lookup 또는 undeclared network
access. Legitimate fixed Git read commands와 disposable-temp fixture만 allowlist한다.

## Stop Conditions

즉시 중단하고 현재 result/handover에 원인을 기록하는 조건은 다음과 같다.

1. parent/remote/persistence 또는 activation-before-Step76 경계가 틀린다.
2. baseline object, digest나 433/167, 42/9,674, 17/20 분모를 재현할 수 없다.
3. truncation 또는 unread page/chunk를 해소할 수 없다.
4. missing raw input/state를 이용해 reproduction/historical-state claim을 만들려 한다.
5. fit 비결정성·수렴 실패를 분류할 수 없다.
6. fresh import 전 mutation 또는 profile/default/temperature 경로 혼합이 발생한다.
7. empirical/physical authority를 분리할 수 없거나 citation을 추정 생성하려 한다.
8. production/Claude/protected/main 변경이나 scholarly code mention이 필요하다.
9. independent review P0/P1이 남거나 push/persistence가 세 번 실패한다.
10. credential, paid source, 외부 승인 또는 사용자 과학 선택이 필요하다.

Missing raw input, optimizer state 또는 Ref. 7은 허위로 닫지 않는다. 다른 내부 감사가
완료됐다면 `GROUND_NOT_FOUND`와 owner를 기록하고 `CONDITIONAL_P066`로 닫을 수 있다.

## Assumptions

- Baseline objects와 persisted predecessor가 readable/immutable하고 Python 3.12/3.14가 있다.
- Production repair/manuscript authoring은 범위 밖이며 raw input/state 존재는 가정하지 않는다.
- Stored claims는 evidence queue이지 truth label이 아니며 Ref. 7 owner는 Phase 071이다.
- Conditional debt는 lossless carry하고 새 사용자 결정은 추정하지 않는다.

## Correction History

- 2026-09-01: persisted `CONDITIONAL_P065`에서 Steps 76–81.2 계획을 최초 작성했다.
- 2026-09-01: frozen source/narrative/process 분모·hash·delta와 stale PDF를 고정했다.
- 2026-09-01: fit/state/authority/default/temperature 경계와 Ref. 7 Phase 071 carry를 고정했다.
- 2026-09-01: predecessor replay 금지와 Phase 066 canonical 14-record 재사용을 정했다.
