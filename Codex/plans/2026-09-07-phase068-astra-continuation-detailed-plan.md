# Phase 068 — Astra continuation detailed plan

## Summary

사용자의 Sol→Astra 전환 및 개정 계획 실행 지시에 따라, Step 94 후보를 보존한 채
실제 검산·결과 artifact·정정 이력·Git 복구점을 닫고 Steps 95–98로 이어간다.
과학 판정 범위는 기존 Phase 068 상세계획과 같다. 이 문건은 기존 계획을 덮어쓰지 않는
명시적 continuation/supersession이다.

Master: `Codex/plans/2026-09-07-astra-canonical-completion-master-plan.md`.
이전 상세계획: `Codex/plans/2026-09-07-phase068-claude-codex-fork-adjudication-detailed-plan.md`.
이전 결과: `Codex/results/PHASE_068_STEP_094_U13_REGSOL_REDERIVATION_RESULT.md` (후보).
전환 기록: `Codex/results/PHASE_068_STEP_094_SOL_ASTRA_HANDOFF_CHECKPOINT.md`.
이전 완료 Step: 93, commit `0b850ea9ffa33e04356d11b83190f9a7cfbea37c`.
WIP checkpoint: `aedfd408281b97699ba7f75884e7108965ecf547`.

## Current Ground Truth

- checkpoint commit/push 및 live origin 일치 확인. 이 사실은 과학 content PASS가 아니다.
- 기존 Step 94 matrix 없음, `--content-only` exit 1 `E_MATRIX_MISSING` 확인.
- 기존 validator 1224행 및 builder 91행은 checkpoint에서 보존됐다.
- 기존 도구의 고정 parent와 exact-seven A/M 계약은 checkpoint 이후 HEAD에 적용되지 않는다.
- 기존 수식 유도와 숫자는 새로 지어내지 않는다. 현재 코드/원천 identity를 검증한 뒤 재사용한다.
- 이전 candidate result/ledger의 완료처럼 보이는 표현 및 오래된 test counts는 신규 결과에서 정정한다.
- Step 95 진입은 아래 Step 94 새 내용 검증과 정상 commit/push/원격 확인 뒤다.

## Phase Range

| Step | 작업 | 산출물 / Gate |
|---:|---|---|
| 94 | U13 후보 실제 검산·정정·저장 | ASTRA_VERIFICATION_RESULT + matrix; 내용 검증 후 persistence |
| 95 | 병행 conformance model 판정 | model adjudication matrix/result |
| 96 | 모든 fork claim 충돌 판정 | conflict matrix/result |
| 97 | file/issue 5상태·carry | disposition register, carry delta, result |
| 98 | 전체 fork gate | final validation, adjudication report, gate/phase result |

번호는 기존 94–98을 그대로 쓴다. 전환 checkpoint/계획 activation에는 새 번호를 부여하지 않는다.

## Non-goals

- Claude/**, 기존 원문/계획/완료 결과, frozen refs, protected branch, main 수정 금지.
- 기존 Step 94 수식/검증 소스를 새 알고리즘으로 통째로 재작성하거나 범용 sandbox를 개발하지 않는다.
- Phase 068에서 canonical 이론/production 구현/PDF를 수정하지 않는다.
- code/test 결과를 원문·재료·기전·held-out 권위로 올리지 않는다.
- current main drift를 frozen fork의 2/5 commit, 3/69 path 분모에 섞지 않는다.
- 검증이 안 된 후보를 persisted 체크포인트만으로 완료 처리하지 않는다.

## Explicit Procedural Supersession

다음 변경은 이 계획 activation 이후 Steps 94–98의 **운영 방식**에만 적용한다.
91–93과 checkpoint의 역사적 계약/증거는 그대로 보존한다.

1. 매 Step 두 대형 ledger와 기존 handover 전체를 재전사·재독하는 규칙을 종료한다.
   새 compact ledger/active handover와 Step 결과를 사용한다. 컴팩션/재개/모델 교체 후에는
   활성 master·현재 detailed plan·직전 result 전문 재독을 반드시 수행한다.
2. 기존 exact-seven/eight path 개수와 A/M 고정 패턴을 후속 실행에서 재사용하지 않는다.
   각 Step의 실제 신규/기존 파일에 맞는 **정확한 path allowlist**로 바꾸며 extra path 금지는 유지한다.
3. 기존 Step 94 builder/validator는 checkpoint 당시 소스를 보존한다.
   새 작은 runner가 그 소스의 analytic/source/numeric 계산 및 payload negative tests를 재사용한다.
   기존 `main`, precommit/staged/persistence entrypoint를 새 HEAD에 억지로 적용하지 않는다.
4. 새 matrix는 기존 scientific candidate를 `legacy_candidate`로 포함하고,
   checkpoint·현재 실행 도구·적용 계약을 바깥 envelope에서 명시한다.
   안쪽 expected_parent는 **과거 Step 93 science certificate**이지 현재 commit parent가 아니다.
5. 현재 Git parent는 계획 activation commit이다. staged/persisted 검증은 명시한 실제 pathset,
   subject, 단일 parent, blob identity, active live origin 및 보호 refs로 수행한다.
   이 Git 확인을 위해 매 Step 수천 행 Python 검증기를 복제하지 않는다.
6. Python 3.12/3.14 실제 수치 content 검증과 독립 검수는 유지한다.
   Git 객체 확인은 runtime 독립적이므로 native Git 한 번으로 검증하며 dual-Python Git 반복을 요구하지 않는다.
7. result-first/JSON-last를 유지하되 result는 검증 전 `IN_PROGRESS` / 수치 확인 후
   `CONTENT_VERIFIED_AWAITING_PUSH`를 정확히 사용한다. runtime receipt는 실행 사실을 별도 보존한다.
   완료 commit hash를 자기 문건 안에 미리 넣는 자기참조 요구는 없다.
8. 내용 검증 명칭은 `PASS_P068_STEP94_ASTRA_CONTENT`, 저장 검증은 `P068_STEP94_ASTRA_PERSISTED`다.
   구형 `PASS_P068_STEP94_PERSISTENCE`를 실행했다고 주장하지 않는다.

## Implementation Changes / Plan Activation

계획 activation에는 아래 다섯 신규 파일만 포함한다.

- `Codex/plans/2026-09-07-astra-canonical-completion-master-plan.md`
- 이 detailed plan.
- `Codex/results/ASTRA_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
- `Codex/results/ACTIVE_HANDOVER_ASTRA_CANONICAL_COMPLETION.md`
- `Codex/results/PHASE_068_ASTRA_PLAN_ACTIVATION_RESULT.md`

activation subject: `docs(plan): activate Astra canonical completion revision`.
parent는 WIP checkpoint다. 번호·원문 action 보존·경로·현재 미완료 상태를 검사하고
commit/push/live equality를 확인한다. activation은 과학 Step 완료가 아니다.

## Step 94 — U13 실제 검산과 정정 완료

### 입력과 검독 범위

- 기존 Step 94 result 1–394 및 checkpoint 전문.
- 기존 validator 1–1224, builder 1–91: 직전 Astra 직접 검독의 hash 불변을 확인하여 재사용하되
  fresh read로 부풀리지 않는다. 실제 사용 함수와 wrapper 변경부는 직접 검토한다.
- 원천 8개는 기존 result의 exact commit/path/blob/bytes/lines 표를 손실 없이 승계한다.
  이전 원천 전문 검독은 재사용으로 기록하고 source identity를 전부 재검증한다.
- U13 전후 TeX의 식·각주, width/peak 정의 중 이번 판단에 필요한 원문을 다시 대조한다.
- 이전 Step 93 matrix/result를 commit-addressed certificate로 검증한다.

### 세부 실행

- [ ] runtime receipt가 실제 명령/환경/결과를 보존하고, matrix 누락/변조/원천 불일치를 잡는 실패 시험을 먼저 작성한다.
- [ ] 신규 runner는 고정된 기존 소스 identity를 확인한 뒤 기존 계산 모듈만 사용한다.
  original CLI의 현재 branch transaction은 실행하지 않는다.
- [ ] binodal series, 중앙 대체 질량 상쇄, 고정 smooth kernel의 좌우 미분,
  C0/C1/면적/부임계 gap을 분리 검산한다. O(epsilon) norm 하나로 C1을 증명하지 않는다.
- [ ] epsilon=a-2와 eta=abs(a/2-1) 차이, 5.89914→11.79828 변환,
  sampled maximum/연속 supremum, clipped numerical kernel/정규화된 이론 kernel을 분리한다.
- [ ] 원래 8+9 historical threshold, 25 normalization, 55 extension, 9 convergence,
  12 high-precision rows를 실제 생성하고 기존 내부 tolerance/negative controls를 실행한다.
- [ ] Python 3.12와 3.14가 독립 process에서 같은 scientific payload를 계산하는지 비교한다.
  stdout/환경/exit/precision을 runtime receipt로 보존한다. rounding/tiny-to-zero 경계를 명시한다.
- [ ] 새 결과서는 원 후보의 유도를 다시 복제하지 않고 해당 절을 근거로 연결하며,
  실제 실행·차이·test counts·read coverage·미검증·권위 한계를 정정한다.
- [ ] result/control이 준비된 뒤 matrix를 생성하고 양 runtime 검증, 결정적 본체 일치 및 독립 검수를 확인한다.
- [ ] exact paths를 확인한 완료 commit과 push/live/clean을 닫고 95로 간다.

### Step 94 exact output allowlist

신규:

- `Codex/work/v1025_phase068/run_phase068_step94_astra.py`
- `Codex/work/v1025_phase068/test_phase068_step94_astra.py`
- `Codex/results/PHASE_068_U13_REGSOL_REDERIVATION.json`
- `Codex/results/PHASE_068_STEP_094_ASTRA_VERIFICATION_RESULT.md`
- `Codex/results/PHASE_068_STEP_094_ASTRA_RUNTIME_312.json`
- `Codex/results/PHASE_068_STEP_094_ASTRA_RUNTIME_314.json`

갱신: 새 compact ledger와 새 active handover 두 파일.
기존 builder/validator/result/대형 controls는 변경하지 않는다.
subject: `audit(phase068): complete Astra U13 rederivation verification`.

### Gate / Stop

원천 identity, 독립 유도 검독, 실제 수치 rows/tolerance, 두 runtime payload 일치,
negative controls, 결과서의 권위 한계가 확인되어야 content PASS다.
matrix가 없거나 변조/비결정/수식 불일치/미확인 필수 근거가 있으면 완료 금지.
중요 수학 claim은 지정 가정 안에서만 확정하며 외부 재료 타당성은 이 단계 gate가 아니다.

## Step 95 — Conformance Model Authority / Value / Duplication

입력: frozen tip `11f90544865dd179739ca5bc5062b28c1078e504`의 model 11 files,
tests 10 files, README/contracts, empirical artifact와 주장한 모든 manuscript equation.
실행 전 Step 92 inventory에서 exact 파일명/blob/전문 범위를 뽑아 이 phase의 Step 95
source/output manifest addendum을 먼저 저장한다. 입력 21개만 보고 원고식을 생략하지 않는다.

공식·단위·부호·state/default/guard/fallback/serialization을 frozen theory와 Phase 067 결과에 대조한다.
외부 disposable runtime에서 Python 3.12/3.14로 실제 tests를 실행하고 collected/executed/skipped/
dependency failure/assertion을 구분한다. 기존 원본을 수정하지 않는다.
각 파일/issue에 scientific authority, implementation value, duplicate-lineage risk와 추천 처분을 쓴다.
최종 5상태는 97에서 부여한다. runtime 성공만으로 science PASS를 부여하지 않는다.

산출물: `PHASE_068_CONFORMANCE_MODEL_ADJUDICATION.json`,
`PHASE_068_STEP_095_CONFORMANCE_MODEL_ADJUDICATION_RESULT.md` 및 실행 receipt.
Gate: 전 입력/주장식 전문 coverage와 세 축 판정/실행 근거, 미결 owner가 갖춰져야 다음으로 간다.
필수 파일 누락, 원천-구현 매핑 미확인 또는 과학/코드 권위 혼동이 남으면 중단한다.

## Step 96 — Fork Claim Conflicts

입력: persisted 91–95의 모든 claim과 frozen 두 fork의 claim-bearing 자료.
기존 exact blob/hash read attestation 재사용은 fresh read와 분리한다.
claim union을 lossless하게 만들고 source 범위/가정/domain/단위/변수/근거/판정/owner를 연결한다.
commit 자기보고보다 실제 Git, 수치 인상보다 유도, metadata보다 원문 support를 좁게 우선한다.
각 claim은 conflict/compatible/superseded-with-evidence/open 중 하나로 추적한다.
main drift는 별도 기록한다. 원문을 얻지 못한 것은 UNVERIFIED다.

산출물: `PHASE_068_FORK_CONFLICT_MATRIX.json`,
`PHASE_068_STEP_096_FORK_CONFLICT_ADJUDICATION_RESULT.md`.
Gate: 모든 input claim ID의 빠짐 없는 분류와 충돌 근거. 누락/owner 없음이면 97 금지.

## Step 97 — Five-state Disposition and Carry

입력: persisted 91–96, Phase 067 carry register 및 96 union.
각 file/issue/claim은 ADOPT/REWRITE/REFERENCE_ONLY/REJECT/UNVERIFIED 중 정확히 하나.
ADOPT는 후속 file-scoped transfer 자격이지 현재 수정/whole commit 채택 허가가 아니다.
REWRITE는 근거 있는 내용의 정정/재구성, REFERENCE_ONLY는 역사/검증 근거,
REJECT는 구체 충돌, UNVERIFIED는 부족한 근거와 owner/수용 조건을 뜻한다.
상속/해결/신규 항목과 many-to-one 관계를 잃지 않고 delta로 옮긴다.

산출물: `PHASE_068_FORK_DISPOSITION_REGISTER.json`, `PHASE_068_CARRY_FORWARD_DELTA.json`,
`PHASE_068_STEP_097_FORK_DISPOSITION_RESULT.md`.
Gate: 중복 disposition/분모 누락/owner 없는 active issue/whole commit target이 없어야 98 진입.

## Step 98 — Phase Gate

입력: 91–97의 Git-addressed 결과/기계 자료, fork read coverage와 원래 Phase 068 Gate 13조건.
역사적 실행은 현재 실행으로 부풀리지 않는다. 각 source/claim/equation/runtime/conflict/disposition을 연결한다.
채택 계획에 source object/path, issue, bounded content, rewrite, destination owner,
acceptance test와 금지 승격을 명시한다.

산출물: `PHASE_068_VALIDATION.json`, `PHASE_068_FORK_ADJUDICATION_REPORT.md`,
`PHASE_068_STEP_098_GATE_RESULT.md`, `PHASE_068_RESULT.md`.
Gate: 기존 13조건의 과학/coverage predicates를 모두 보존한다. 운영 persistence는 위 새 계약으로 검증한다.
모두 충족할 때만 `PASS_P068_FORK_ADJUDICATION`, 아니면 `NOT_ACHIEVED`다.
정본 선택/출판/외부 재료 검증 완료를 뜻하지 않는다. Step 98 push 확인 후에만 Phase 069 계획으로 간다.

## Implementation Interfaces / Test Plan

- 각 Step 입력과 exact output allowlist를 실행 전 manifest/addendum으로 확정한다.
- read coverage는 file, commit/blob, lines/pages, fresh/reused, 미확인 범위를 분리한다.
- runtime receipt는 명령, Python/dependency version, input/output identities, exit, stdout/stderr를 보존한다.
- machine JSON은 finite 값, canonical LF/UTF-8, source identity와 scientific assumptions를 유지한다.
- 새 runner는 실제 필요한 누락/변조/권위/입출력 검증만 추가한다. 기존 negative tests를 임의 삭제하지 않는다.
- 실제 pathset/status/mode, 단일 parent와 subject, result 포함, active push/live/clean을 native Git으로 확인한다.
- 단계별 source/과학 reviewer 범위는 독립적으로 분담하고 파일/행·근거·미확인을 결과서에 통합한다.
- 예상치 못한 ref 이동, 보호/Claude 변경, 동일 push 원인 3회 실패는 hard stop이다.
  수정 가능한 과학 오류는 해당 Step gate failure로 처리하고 수정·동일 검증·재검토한다.
  근거 없는 정본 선택이나 필수 외부 권한처럼 master의 Hard Stops에 해당할 때만 전체 작업을 중단한다.

## Assumptions / Correction History

기존 수식은 candidate이며 fresh runtime/해석 검증을 통과해야 현재 content 근거가 된다.
원문·실험 부채는 이 단계의 독립 수학 검산으로 해소되지 않는다.
2026-09-07: 사용자 지정 WIP checkpoint 이후의 계약을 새로 정의했다.
3단 기록·Codex/{plans,results,docs}·컴팩션 후 두 계획과 직전 결과 전문 재독·누적 번호·매 Step 결과 포함 push는 유지한다.
