# Phase 065 Step 75.1 Source Disposition and Carry-Forward Result

정본일: 2026-08-31

## 1. Status

- Phase: `065`
- cumulative Step: `75.1`
- status: `PASS_WITH_CONCERNS_PENDING_PERSISTENCE`
- implementation-specific precommit content gate: `PASS_P065_STEP75_1_DISPOSITION_WITH_CONCERNS`
- required terminal after commit/push: `PASS_P065_STEP75_1_PERSISTENCE`
- expected parent: `a04bca9c73941e1a4fbc0ab6e4f4e49514dcce12`
- expected subject: `audit(phase065): disposition v1024 lineage`
- branch: `codex/anode-fit-v1025_2-canonical-completion`
- baseline: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`
- containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`
- push/live-remote state: `PENDING_AT_PRECOMMIT_BY_DESIGN`

이 detailed plan은 Step 75.1 precommit terminal 이름을 따로 정하지 않았다. 위
`PASS_P065_STEP75_1_DISPOSITION_WITH_CONCERNS`는 이 구현이 content validation과
commit 이후 persistence validation을 구분하기 위해 도입한 Step 75.1 전용 표지이며,
계획서에 이미 존재하던 이름이라고 주장하지 않는다. 계획서가 요구한 terminal은
commit/push 이후의 `PASS_P065_STEP75_1_PERSISTENCE`다.

## 2. Scope and authority ceiling

이 Step은 frozen v1.0.24/v1.0.24.1 source와 Steps 70–74 감사 근거를 수정하지
않고, 모든 source occurrence와 열린 observation을 disposition하고 downstream의
정확히 한 canonical owner와 acceptance criterion에 연결한다. 이 결과가 부여하는
권위는 내부 계보 disposition뿐이다.

- external scientific truth: `false`
- external material truth: `false`
- external experimental truth: `false`
- external proposition/page/equation support: `false`
- canonical model selected: `false`
- production repair complete: `false`
- publication ready: `false`
- new Phase 065 blocker created: `false`

`CORRECT`는 frozen source를 소급 수정한다는 뜻이 아니다. 원 source identity와 오류
근거를 그대로 보존하고, 후속 owner가 canonical assembly 전에 교정된 proposition을
명시적으로 구현·검증해야 한다는 뜻이다. v1.0.24.1 mirror는 독립 corroboration이
아니다.

## 3. Recovery checkpoint: Step 74 persistence

Step 74의 control 문서에는 precommit 상태가 남아 있었지만 controller가 실제 Git
상태와 양쪽 runtime persistence validator를 직접 다시 확인했다.

- Step 74 commit: `a04bca9c73941e1a4fbc0ab6e4f4e49514dcce12`
- parent: `5c5c555462f1dbf0603eedda6a1d5b62684cffdf`
- subject: `audit(phase065): adjudicate v1024 doc code guide`
- path set: exact-seven; `Claude/**` 변경 `0`
- local HEAD/upstream/tracking/live remote: 모두 Step 74 commit과 일치
- protected local/tracking/live: `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`
- main tracking/live: `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`
- Python 3.12: `PASS_P065_STEP74_PERSISTENCE`
- Python 3.14: `PASS_P065_STEP74_PERSISTENCE`
- persistence metrics: conformance rows/routes/nodes/depth `41/17/2536/5`
- negative/source-policy/output/transaction: `19/56/1/4`
- matrix SHA-256 pin:
  `bb8b38f8c882e6fe55497cc06af6109bf72b7ff87798307bf15e8e24d6d85adb`

따라서 Step 75.1 entry condition은 충족됐다. 이 섹션은 stale precommit control을
근거 없이 성공으로 바꾼 것이 아니라, controller가 실제로 재실행한 terminal과 Git
remote equality를 다음 Step 기록에 영속화한 것이다.

## 4. Inputs and complete-read coverage

### 4.1 Control documents

다음 control 문서는 1행부터 EOF까지 직접 읽거나 독립 분담 검독 후 controller가
결과를 통합 대조했다.

- canonical master plan Markdown: `1–665`
- canonical master plan JSON: `1–148`, strict traversal `568` key-plus-value nodes
- Phase 065 detailed plan: `1–851`
- parent execution ledger: `1–56`
- canonical execution ledger: `1–138`
- active handover before this update: `1–395`
- Step 74 result: `1–312`
- project `Codex/AGENTS.md`: `1–180`

### 4.2 Machine evidence

고정 parent의 다음 JSON을 duplicate-key/nonfinite 거부 parser로 읽고 전체 node를
순회한다.

1. `PHASE_065_SOURCE_PROCESS_TOPOLOGY.json`
2. `PHASE_065_COMPLETE_READ_ATTESTATION.json`
3. `PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json`
4. `PHASE_065_STATIC_ROUTE_ATTESTATION.json`
5. `PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json`
6. `PHASE_065_INITIALIZATION_ROUTE_MATRIX.json`
7. `PHASE_065_RUNTIME_ATTESTATION.json`
8. `PHASE_065_DOC_CODE_GUIDE_CONFORMANCE_MATRIX.json`
9. `PHASE_064_V1023_DISPOSITION_MATRIX.json`
10. `PHASE_064_V1023_CARRY_FORWARD_DELTA.json`

독립 검독에서 Step 70 topology `45,772` nodes/depth `9`, complete-read
attestation `571/7`, Step 71 matrix `2,482/4`, static attestation `46/2`, Step 72
matrix `3,436/5`, Step 73 initialization/runtime `1,096/4` 및 `2,835/9`, Step 74
matrix `2,536/5`, Phase 064 disposition/carry `9,003/6` 및 `34,112/14`를
전수 순회했다. Step 70 source occurrence `261/261`, unique source `131/131`,
Step 71 endpoint `20/20`, Step 72 direct binding `28/28`의 baseline Git blob과
raw SHA/bytes/lines 대조 오류는 `0`이었다.

## 5. Source disposition

### 5.1 Denominators

- source occurrences: `261`
- v1.0.24 occurrences: `130`
- v1.0.24.1 occurrences: `131`
- unique blobs: `131`
- byte-identical mirror pairs: `130`
- v1.0.24.1 archive-only occurrence: `1`
- ownerless source rows: `0`
- contradictory per-blob dispositions: `0`
- external-authority promotions: `0`

각 disposition row는 Step 70 `occurrences[*]`의 전체 identity를 복사해
`ordinal`, `occurrence_index`, `version`, `path`, `git_mode`, `blob`, extent/size,
role, review/read ranges, mirror counterpart와 process route를 보존한다. 각 unique
blob은 131개 `blob_disposition_groups` 중 정확히 하나에 속하며 mirror pair에는 같은
disposition이 적용된다.

### 5.2 Allowed enum and result

허용 enum은 정확히 다음 여섯 개다.

`PRESERVE`, `CORRECT`, `THEORY_ONLY`, `UNVERIFIED`, `REJECTED_SOURCE`, `DISCARD`

Occurrence distribution:

- `PRESERVE=114`
- `CORRECT=41`
- `THEORY_ONLY=96`
- `UNVERIFIED=8`
- `REJECTED_SOURCE=2`
- `DISCARD=0`

Rejected 두 occurrence는 v1.0.24/v1.0.24.1 mirror의 같은 frozen blob이며 exact
normalized source는
`Claude/docs/v1.0.24/results/comp_R1/W1/gr_2L.tex`다. 이 후보의
`fergusonbazant2014`와 `guo2016`은 채택된 bibliography의 외부 근거로 graft하지
않는다.

## 6. Observation carry-forward

### 6.1 Partition

- Phase 057 observations: `82`, active `17`
- Step 70 findings: `44`, input open `39`, current active `24`
- Step 71 findings: `13`, input open `13`, current active `10`
- Step 72 findings: `6`, input open `5`, current active `3`
- Step 74 conformance rows: `41`, input open `35`, Step 75.1 이후 open `34`
- exact Phase 064 inherited routes: `6`
- total observation records: `192`
- Step 74 exact origin routes superseded upstream: `17`
- Ref. 7 semantic authority chain superseded upstream: `4`
- active obligations: `94`
- ownerless active obligations: `0`
- multiply-owned active obligations: `0`
- unresolved semantic duplicates: `0`
- new Phase 065 blockers: `0`

Step 73은 Step 71 F01–F11에 runtime evidence를 공급하지만 별도 finding/blocker
identity를 만들지 않았으므로 192 denominator에 중복 삽입하지 않는다. Step 74의
17 exact origin route는 원 identity를 보존하되 `SUPERSEDED_BY_STEP74`로 비활성화하고
row-level successor만 active로 센다. Ref. 7의 같은 primary-source authority chain 네
upstream identity도 D74-006 하나로 귀속하여 이중 계수를 제거한다.

### 6.2 Step 74 D74-007 closure

`D74-007`은 Step 75.1에서 `CLOSED_SUPERSEDED_IN_STEP75_1`로 닫는다. 현재 frozen
code의 LCO default-false 상태를 보존하고, R2/R3의 default-ON/default-True 문구는
stale·superseded로 명시한다. 이는 production repair나 canonical model 선택을
뜻하지 않는다.

### 6.3 Exact-text semantic duplicate resolution

정확히 같은 claim text를 가진 한 그룹이 발견됐다.

- origin: `P065-S70-F44`
- refinement: `D74-028`
- inherited owner preserved in origin record: `PHASE-074-DOCUMENT-REPAIR`
- current canonical owner for both identities: `PHASE-089-RELEASE-QA`
- target: Phase `089`
- resolution: `RESOLVED_BY_STEP74_REFINEMENT`

두 identity를 합치거나 삭제하지 않는다. `P065-S70-F44`는 superseded historical
identity로 보존하고 `D74-028`만 active로 센다. origin route와 양방향
refines/refined-by 관계로 관계를 공개하고 current accountable owner를 하나로
통일한다.

### 6.4 Ref. 7 semantic authority-chain resolution

정확 문구는 다르지만 같은 Ref. 7 proposition/page/equation authority를 요구하는
`P065-S70-F09`, `P065-S70-F24`, `P065-S71-F13`, `P065-S72-F06`, `D74-006`을
`P065-SEM-002`로 공개한다. 앞의 네 identity는 `SUPERSEDED_BY_STEP74`로 보존하고,
`D74-006`만 active obligation이다. `P065-S71-F13`의 Step 70 links,
`P065-S72-F06`의 Step 71 link, `D74-006`의 Step 72 link를 연속 relation chain으로
기록한다. 모든 current canonical owner는 정확히
`PHASE-071-PRIMARY-SOURCE-ACQUISITION`이고 target은 Phase 071이다. 원 Step 72의
`P071-PRIMARY-SOURCE-ACQUISITION` 표기는 `origin_record`의 inherited owner로만
보존하며 canonical owner alias로 사용하지 않는다.

### 6.5 Exact inherited Phase 064 obligations

다음 여섯 owner identifier를 바꾸지 않고 Phase 065에 정확히 한 번 이어받는다.

- `P059-CFR-CF-01`, `PRESERVED_ACTIVE`: bounded ideal statistical-mechanics와
  logistic-kernel identity를 material-validation 승격 없이 보존한다.
- `P059-CFR-CF-02`, `PRESERVED_ACTIVE`: homogeneous symmetric regular-solution
  algebra를 stated assumptions 아래 보존하고 convexified equilibrium과 분리한다.
- `P059-CFR-CF-06`, `PRESERVED_ACTIVE`: entropy-temperature coefficient와
  reversible heat identity를 sign/reference convention과 함께 보존한다.
- `P059-CFR-CF-07`, `PRESERVED_ACTIVE`: Sommerfeld electronic-entropy
  endpoint/unit bridge를 placeholder material constant로 승격하지 않는다.
- `P059-CFR-RB-02`, `OPEN_CARRY`: homogeneous branch, binodal, common tangent,
  spinodal, measured hysteresis를 명시적으로 분리한다.
- `P059-CFR-RB-03`, `OPEN_CARRY`: material별 independent extent,
  mutually-exclusive state 또는 continuous host free energy 중 하나를 선택한다.

Phase 064의 326-record owner universe는 content-addressed snapshot으로 참조해
보존하고, 그 전체를 Phase 065 active obligation으로 재활성화하지 않는다.

## 7. Generated artifacts

- `Codex/results/PHASE_065_SOURCE_DISPOSITION_MATRIX.json`
- `Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json`

두 artifact는 control 문서와 builder/validator staged blob을 먼저 고정한 뒤
JSON-last로 생성한다. 각 input은 fixed parent Git blob, raw SHA-256, bytes,
strict traversal node/depth를 보존하고, 각 artifact는 자신의 semantic payload
SHA-256을 기록한다.

## 8. Validation contract and evidence

Precommit과 persistence validator는 다음을 fail-closed로 확인한다.

- strict JSON duplicate-key/nonfinite rejection
- fixed-parent input Git blob/raw hash/full traversal
- staged/committed control-source bindings
- exact source/observation denominators와 full origin-record identity
- one-disposition-per-blob와 허용 enum
- exact-six inherited obligations와 unchanged owner ID
- D74-007 supersession, exact semantic-duplicate resolution, single-owner routing
- no hidden/new blocker와 authority ceiling
- external deterministic build `2/2`
- hostile semantic/source-policy/output-guard/transaction probes
- exact-eight staged or committed path set
- expected parent/subject/branch, protected/main/`Claude/**` preservation
- persistence `expected_commit` exact lowercase 40-hex validation before any Git call
- persistence에서 HEAD/upstream/tracking/live equality와 clean worktree

Test-first RED는 machine artifacts를 만들기 전에 Python 3.12와 3.14에서 각각
실행했고 둘 다 `FAIL_P065_STEP75_1 E_ARTIFACT_MISSING`, exit `1`로 의도대로
거부됐다.

첫 precommit candidate는 Python 3.12/3.14에서 gate 문자열을 반환했지만 독립 검토가
그 결과를 승인하지 않았다. 그 candidate는 Step 74 origin 17개를 predecessor와
successor 양쪽에서 active로 세었고, Step 72 관계 ID 두 개가 dangling이었으며,
Ref. 7 owner alias와 semantic authority chain을 하나로 귀속하지 않았다. 검증기도
coherent extra-key·owner/evidence mutation과 module/callable escape 일부를 fail-open으로
수용했다. 따라서 첫 candidate의 모든 PASS와 `114 active`, 기존 traversal/negative
수치는 폐기·supersede하며 final evidence로 사용하지 않는다.

보정본은 exact origin 17개와 Ref. 7 upstream 4개를 비활성화해 active obligation을
`94`로 재계산했고, Step 72 ID namespace, 관계 양방향성, canonical owner,
`D74-007` current open route 제거를 고쳤다. validator에는 exact nested schema와
source status/reason/acceptance/group link 재계산, 192 observation 독립 contract,
coherent semantic mutations, exact import signature와 sensitive callable/value escape
검사를 추가했다. 최종 JSON-last 생성과 dual-runtime 수치는 이 보정본의 exact-eight
freeze 뒤 새로 기록했다. Python 3.12와 3.14는 모두
`PASS_P065_STEP75_1_DISPOSITION_WITH_CONCERNS`를 반환했다. 공통 측정치는
source/carry traversal `17,151/11,021` nodes, depth `7/10`, semantic negative `35`,
source-policy negative `41`, output-guard `7`, transaction negative `4`,
persistence-argument negative `5`, deterministic pair `2/2`다. Python 3.14가 빈 AST field를 기본 출력에서 생략해 첫 보정 시도의
AST-string hash를 거부한 이식성 문제도 발견했으며, 모든 AST field를 명시적으로
직렬화하는 runtime-neutral hash로 교체한 뒤 양 runtime에서 같은 정책 hash와 gate를
확인했다. 독립 재검토가 지적한 arbitrary callback, duplicate writer,
file-handle/tempfile/dunder-dict escape는 생성기 전체 module AST와 유일한
`atomic_write` AST를 별도로 고정하고 8개 회귀 probe를 추가해 차단했다.
마지막 독립 검토가 발견한 persistence `expected_commit` option-injection 경로는
어떤 Git 호출보다 먼저 exact lowercase 40-hex를 요구하고 `--output=C`, uppercase,
short hash, precommit에서의 unexpected hash를 포함한 비실행 회귀 probe `5/5`로
차단했다. 이 공격 payload는 실행하지 않았다.

이 result의 실제 containing commit과 remote equality는 다음 persisted checkpoint에서
기록하며, 미실행 상태를 완료로 표현하지 않는다.

## 9. Exact Step 75.1 commit set

1. `Codex/work/v1024_phase065/build_phase065_step75_1.py`
2. `Codex/work/v1024_phase065/validate_phase065_step75_1.py`
3. `Codex/results/PHASE_065_SOURCE_DISPOSITION_MATRIX.json`
4. `Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json`
5. `Codex/results/PHASE_065_STEP_075_1_DISPOSITION_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

`Claude/**`는 수정하지 않는다.

## 10. Gate decision and next condition

Content decision은 `PASS_WITH_CONCERNS`다. 모든 occurrence와 active obligation은
분모 손실 없이 disposition/owner/acceptance에 연결됐지만 외부 과학·재료·실험
권위와 canonical/publication readiness는 여전히 false다.

Step 75.2는 exact-eight commit/push 후 Python 3.12와 3.14 양쪽에서
`PASS_P065_STEP75_1_PERSISTENCE`를 받고 local/upstream/tracking/live remote equality,
protected/main/Claude 불변, clean worktree를 확인한 뒤에만 시작한다.
