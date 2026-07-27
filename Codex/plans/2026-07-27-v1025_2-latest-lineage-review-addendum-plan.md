# v1.0.25.2 Latest-Lineage Review Addendum Plan

## Summary

이미 원격에 게시된 `codex/v1025_2-physics-conformance`의 기준점이
`ab196b2`였음을 정정하고, 사용자 지정 최신본인 v1.0.25.2 계보
`3b5fd05`까지의 변경을 반영하여 기존 conformance 산출물의 유효 범위와
수정 필요 항목을 다시 판정한다.

이번 작업은 새 물리 원고를 다시 쓰는 단계가 아니라 최신 계보에 대한
독립 리뷰와 상태 정정 단계다. 이론 본문에는 코드명, 브랜치, 커밋 또는
검증 이력을 추가하지 않는다. 구현과 계보에 관한 판단은
`Codex/results`의 외부 리뷰 문건에만 기록한다.

## Current Ground Truth

- Working branch:
  `codex/v1025_2-physics-conformance`
- Published candidate tip before this addendum:
  `2abf019c7fee9bebd84b49cc9530f6983b08a8fa`
- Original candidate baseline:
  `ab196b292e14492b647f87a6c0d1d8c9ed0630ab`
- Latest accepted v1.0.25.2 lineage tip:
  `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`
- Material latest-lineage correction:
  `7b342dd88aad6bf9ff08cb3568da374837008ca7`
- Excluded scientific source:
  `main@4069cb3` and every v1.0.26 artifact
- Preserved unrelated working-tree change:
  `Claude/docs/v1.0.24.1/CODE_GUIDE_v24.html`

The unrelated working-tree change is not read, modified, restored, staged or
committed by this plan.

## Phase Range

| Phase | Name | Step Range | Purpose |
|---|---|---:|---|
| 054A | Latest lineage freeze | 1361--1370 | `ab196b2..3b5fd05`의 실제 변경과 ancestry를 고정한다. |
| 054B | Semantic revalidation | 1371--1390 | default wiring, source probes, tests, regular-solution claims를 다시 검증한다. |
| 054C | Review correction | 1391--1405 | 기존 보고의 오기와 유효 범위를 정정하고 최신 대응 리뷰를 남긴다. |
| 054D | Publication | 1406--1415 | branch-only merge, 선택 파일 commit, push 및 원격 검증을 수행한다. |

## Non-goals

- `main` 또는 v1.0.26을 과학 기준으로 승격하지 않는다.
- 기존 Claude 문건의 새 내용을 임의로 다시 쓰지 않는다.
- 기존 conformance 원고와 구현을 최신 release 구현의 대체물로 선언하지 않는다.
- 실제 데이터 피팅 성공을 부정하지 않는다.
- 저장된 direct14 성분을 graphite/Si 상으로 재해석하지 않는다.
- 기존 결과·handover의 역사적 원문을 덮어쓰지 않는다.
- 사용자 소유의 무관한 dirty file을 stage하지 않는다.
- PR 또는 merge-to-main을 생성하지 않는다.

## Inputs Requiring Complete Read

- 기존 branch plan, result, ledger, handover와 conformance matrix
- `ab196b2..3b5fd05`에서 변경된 v1.0.25.2 파일 전부
- current-source 및 regular-solution probe의 source와 machine result
- `eq:sifr-twophase`를 정의하고 해석하는 원문 절 전체
- 구현 부록과 manuscript/code static gate

## Outputs

- `Codex/results/PHASE_054_V1025_2_LATEST_LINEAGE_REVIEW_ADDENDUM.md`
- `Codex/results/PHASE_054_V1025_2_LATEST_REVIEW_EXECUTION_LEDGER.md`
- `Codex/results/PHASE_054_V1025_2_LATEST_SOURCE_PROBES.json`
- `Codex/results/PHASE_054_V1025_2_REGSOL_CROSSCHECK.json`
- 필요 시 검증용 probe/test의 branch-local 보완본

## Phase 054A — Latest Lineage Freeze

- [ ] Step 1361: 원격 refs를 fetch하고 v1.0.26을 제외한 최신 v1.0.25.2 tip을 확정한다.
- [ ] Step 1362: `2abf019`, `ab196b2`, `7b342dd`, `3b5fd05`의 ancestry와 시간을 기록한다.
- [ ] Step 1363: `ab196b2..3b5fd05` 변경 파일을 전부 읽는다.
- [ ] Step 1364: 기존 conformance 보고 중 baseline에 의존하는 문장을 전수 검색한다.
- [ ] Step 1365: 기존 commit/push/merge 상태 오기를 전수 검색한다.

Gate:

- 최신본과 후보본의 공통 기준점 및 누락된 커밋이 명시되어야 한다.
- 파일 일부만 읽고 나머지 내용을 추론하지 않는다.

## Phase 054B — Semantic Revalidation

- [ ] Step 1371: 최신 default transition 수와 Si case 경로를 실행 확인한다.
- [ ] Step 1372: 최신 invalid-case rejection, derivative, overflow와 conversion factor를 확인한다.
- [ ] Step 1373: legacy gate와 conformance gate가 최신 default의 의미 변화를 잡는지 판정한다.
- [ ] Step 1374: source freeze/probe를 최신 tree에서 다시 생성한다.
- [ ] Step 1375: regular-solution 면적, gap, 임계 연속성 및 우측 미분 주장을 독립 검산한다.
- [ ] Step 1376: implementation appendix의 release symbol 참조가 최신 코드에 존재하는지 확인한다.

Gate:

- PASS한 시험이 실제로 보증하는 주장과 보증하지 않는 주장을 분리한다.
- 수치 검산에는 식, 단위, 적분창 또는 극한 절차를 함께 기록한다.

## Phase 054C — Review Correction

- [ ] Step 1391: 기존 handover의 publication-state 오기를 정정한다.
- [ ] Step 1392: 기존 branch 산출물의 artifact class와 manuscript lineage를 명시한다.
- [ ] Step 1393: 최신 default 변경이 기존 source probe 결론에 미친 영향을 정량 기록한다.
- [ ] Step 1394: regular-solution 대조가 실제로 있었던 범위와 추가 검산 범위를 구분한다.
- [ ] Step 1395: 사용자 결정 없이 promotion하지 않을 항목을 명시한다.

Gate:

- `확정`, `조건부`, `오류`, `미검증`, `사용자 결정`을 분리한다.
- 코드 관련 내용은 외부 리뷰/부록에만 두고 이론 본문에는 삽입하지 않는다.

## Phase 054D — Publication

- [ ] Step 1406: 최신 v1.0.25.2 tip을 현재 review branch에 merge하여 계보를 보존한다.
- [ ] Step 1407: conformance, legacy, source-probe 및 static manuscript gates를 실행한다.
- [ ] Step 1408: 새 결과·ledger·machine artifacts만 명시적으로 stage한다.
- [ ] Step 1409: unrelated dirty file이 stage되지 않았는지 확인한다.
- [ ] Step 1410: correction commit을 push하고 원격 branch tip을 재조회한다.

Gate:

- `main`은 변경되지 않아야 한다.
- 기존 공개 branch history는 force-push로 재작성하지 않는다.
- 로컬과 원격 branch tip이 일치해야 한다.

## Test Plan

- Git ancestry and changed-file audit
- latest default source probes
- invalid Si-case and transition-count assertions
- legacy v1.0.24/v1.0.25 gates
- 51-test independent conformance suite
- manuscript static code-token boundary check
- regular-solution analytic and numerical cross-check
- selective staging audit
- remote branch tip verification

## Decision Boundary

이 addendum은 최신 v1.0.25.2에 대응하는 검토 기록이다. 기존 독립 원고를
정식 후속본, 검증 전용 reference 또는 선택적 추출 원천 중 무엇으로
승격할지는 사용자 결정 전까지 열어 둔다.
