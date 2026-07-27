# Handover correction — v1.0.25.2 최신 대응

작성일: 2026-07-27
브랜치: `codex/v1025_2-physics-conformance`

이 문서는 다음 기존 기록의 사실 오류와 최신 계보 누락을
supersede한다. 기존 파일은 감사 이력 보존을 위해 덮어쓰지 않는다.

- `HANDOVER_V1025_3_CONFORMANCE_BRANCH.md`
- `PHASE_044_053_V1025_2_CONFORMANCE_EXECUTION_LEDGER.md`
- `PHASE_046_053_V1025_3_RECONSTRUCTION_RESULT.md`의 publication-state 문장

## 1. 정정된 공개 상태

| 항목 | 정정 상태 |
|---|---|
| 기존 후보 commit | yes — `2abf019` |
| 기존 후보 push | yes — 원격 동일 브랜치 |
| 기존 후보의 `main` merge | no |
| 기존 후보의 정본 승격 | no |
| 최신 v1.0.25.2 계보 통합 | yes — merge `4316d8a` |
| Phase 054 리뷰 checkpoint | yes — `30a874e` |
| Phase 054 checkpoint push | yes |
| `main` 수정 | no |
| v1.0.26을 과학적 입력으로 사용 | no |

기존 “commit/push/merge performed: no”와 “아직 commit/push하지 않았다”는
문장은 잘못됐다. 정확한 뜻은 “브랜치에는 commit/push했으나 main에는
merge/promote하지 않았다”이다.

## 2. 최신 입력

- 최신 인정 v1.0.25.2 tip:
  `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`
- 기본값 복구:
  `7b342dd88aad6bf9ff08cb3568da374837008ca7`
- 기존 후보 기준점:
  `ab196b292e14492b647f87a6c0d1d8c9ed0630ab`
- 기존 후보 tip:
  `2abf019c7fee9bebd84b49cc9530f6983b08a8fa`

기존 후보와 최신본의 merge-base는 `ab196b2`다. 기존 후보는 기본값
복구를 포함하지 않았으므로 “최신 v1.0.25.2 대응”이라는 표현은 Phase
054 이전 산출물 전체에 적용할 수 없다.

공개 브랜치의 이력을 강제 재작성하지 않기 위해 rebase/force-push
대신 `3b5fd05`를 non-force merge했다.

## 3. 최신 판정 요약

1. 현 기본은 흑연 4전이 + `sic` Si 2전이다.
2. 7+7 skew는 `use_skew7_default(True)` 또는 명시 transition으로만
   활성화된다.
3. 현 기본의 288.15→308.15 K 최대 차는 `0.5252164419568519`다.
4. 7+7 opt-in의 같은 차는 `6.394884621840902e-14`로 수치적으로 0이다.
5. direct14 저장 profile의 `R²=0.99964941790404`는 그대로 재현된다.
6. direct14는 실제 데이터 피팅 결과이지만 현 기본, 원 optimizer replay,
   흑연/Si 상 분해 중 어느 것도 아니다.
7. 최신 코드 자체에 철회 전 default 설명과 삭제된 함수명이 남아 있다.
8. 정칙용액 `eq:sifr-twophase` 대조는 기존에도 있었다. Phase 054는
   Claude의 3항을 넓은 sweep 표로 보강했다.
9. 해당 식의 면적·subcritical gap·값 연속성은 통과하지만 “1차 Ω
   도함수 발산”은 질량 상쇄 때문에 성립하지 않는다.

## 4. 후보 산출물의 정확한 지위

후보는 다음 세 층을 묶은 병행 산출물이다.

- independent reconstruction manuscript candidate
- bounded reference implementation
- manuscript/reference conformance suite

따라서 단순 검사 도구나 v1.0.25.3 정본 후속판으로 읽지 않는다.
현재 상태는 `parallel and non-canonical`이다. 새 원고와 새 참조 구현의
내부 대응은 보존 가능하지만 최신 legacy 배포본 검증은 별도 Phase 054
probe가 담당한다.

## 5. 검증 결과

- 최신 legacy compile: PASS
- `test_gates_v1025.py`: PASS 9/9
- `test_gates_v1024.py`: 전 항목 PASS
- reflect gate: PASS 4/4
- selfconsistent gate: PASS 5/5
- 독립 conformance suite: PASS 51/51 with warnings-as-errors
- 원고 구조: PASS — 16 sources, 15 include edges, 183 labels, 32 references
- 최신 source probe: PASS, 기대된 legacy warning 3건 재현
- 정칙용액 sweep: PASS
- 기존 PDF inspect: PASS, 28쪽·폰트 내장
- fresh PDF build: BLOCKED — 실행 환경에 지정 한글 폰트 없음

legacy gate 통과는 shipped fresh-import default 검증이 아니다. v1024는
로드 후 4전이로 강제 복귀하고 나머지도 명시 transition을 쓴다.
51개 독립 시험 또한 latest legacy source를 import하지 않는다.

## 6. 읽기 순서

1. `PHASE_054_V1025_2_LATEST_LINEAGE_REVIEW_ADDENDUM.md`
2. `V1025_2_LATEST_RELEASE_ALIGNMENT_MATRIX.md`
3. `PHASE_054_V1025_2_LATEST_REVIEW_EXECUTION_LEDGER.md`
4. `PHASE_054_V1025_2_LATEST_SOURCE_FREEZE_MANIFEST.json`
5. `PHASE_054_V1025_2_LATEST_SOURCE_PROBES.json`
6. `PHASE_054_V1025_2_REGSOL_CROSSCHECK.json`

Phase 044 파일은 `ab196b2` 당시의 역사 기록으로 읽고, latest/shipped
현재형 판정은 위 Phase 054 자료를 우선한다.

## 7. 다음 작업의 우선순위

### P0

- 코드 헤더·구 주석·생성자 docstring을 실제 4+2 기본에 맞춘다.
- 허용된 구현 부록에서 삭제 symbol을 `use_skew7_default` 계약으로
  정정한다.
- 이론 본문의 버전/default/runtime 경고 서술을 물리 영역과
  구현 부록으로 분리한다.
- 정칙용액 “1차 Ω 도함수 발산” 문장을 철회한다.
- fresh-import default gate를 추가한다.

### P1

7-gallery를 다온도 열역학에 올리기 전에 각 gallery 군집의 staging
entropy 부모를 물리적으로 결정한다. 최근접 U 자동배정은 금지한다.

### P2

mutable global switch 대신 명시적·불변 profile configuration을
도입하고 invalid `si_case` 검증을 profile과 무관하게 만든다.

### P3

후보를 검증 전용, 정본 후보, 부분 역이식 중 어디에 둘지 사용자가
결정한다. 그 전에는 원 Claude 문건을 조용히 덮어쓰거나 main으로
승격하지 않는다.

## 8. 보존 사항

이번 최신 대응은 리뷰·probe·기록 작업이다. 최신 계보에 이미 존재한
Claude 변경을 merge했을 뿐, 그 원본 이론·legacy 코드를 새로 수정하지
않았다.

작업 시작 전부터 있던
`Claude/docs/v1.0.24.1/CODE_GUIDE_v24.html` 변경은 읽기·수정·stage하지
않았다.

Phase 054 리뷰 산출물 checkpoint `30a874e`는 원격에 확인됐다. 이
correction과 execution ledger는 그 뒤의 별도 기록 커밋으로 추가한다.
