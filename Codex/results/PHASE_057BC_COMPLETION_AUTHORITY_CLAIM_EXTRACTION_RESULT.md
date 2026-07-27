# Phase 057BC 완료·권위·불변·정합 선언 추출 결과

정본일: 2026-07-28  
대상 단계: Phase 057 Step 20.3  
기준 커밋: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`

## 판정

`PASS_P057_COMPLETION_CLAIM_EXTRACTION`

이 판정은 모든 기준 문건에서 후보 표현을 위치 단위로 추출했다는
기계적 완결성만 뜻한다. 후보 문장이 실제로 입증됐다는 판정은 아니다.
`CONFIRMED`, `OVERCLAIMED`, `PARTIAL`, `UNVERIFIED` 판정은 Step 20.4에서
실제 patch, 시험 산출물, 후속 수정과 대조해 부여한다.

## 입력과 방법

- 기준 문건: 271개 고유 blob
- 입력 대기열:
  `Codex/results/PHASE_057_USER_INTENT_READ_QUEUE.json`
- 전문 검독 coverage:
  `Codex/results/PHASE_057_USER_INTENT_READ_COVERAGE.json`
- blob별 Git 계보:
  `Codex/results/PHASE_057_GIT_DOCUMENT_GENEALOGY.json`
- 추출기:
  `Codex/work/v1010_v1025_2_reaudit/generate_phase057_completion_claims.py`
- 기계 산출물:
  `Codex/results/PHASE_057_COMPLETION_AUTHORITY_CLAIMS.json`

Markdown, text와 authored HTML은 물리 행 단위로 스캔했다. 정상 JSON은 모든
문자열 scalar를 JSON pointer 단위로 순회하고, JSON이 아닌데 `.json`으로
저장된 `snapshot_v1024_R0.json`은 `INVALID_JSON_LINE_SCAN`으로 분리했다.
HTML의 embedded image와 4,000자를 넘는 vendor runtime 행은 프로젝트 작성자의
과학적 선언으로 오인하지 않도록 제외했다.

## 추출 결과

| 항목 | 결과 |
|---|---:|
| 스캔한 고유 문건 | 271 |
| 후보가 있는 문건 | 243 |
| 후보가 없는 문건 | 28 |
| 전체 후보 위치 | 3,487 |
| 물리 행 후보 | 3,487 |
| 정상 JSON scalar scan 문건 | 20 |
| invalid-JSON fallback 문건 | 1 |
| 일반 line scan 문건 | 250 |

한 위치가 여러 범주에 동시에 속할 수 있으므로 범주 합은 후보 수보다 크다.

| 범주 | 후보 위치 수 |
|---|---:|
| `COMPLETION` | 1,787 |
| `CONFORMANCE` | 1,195 |
| `INVARIANCE` | 1,118 |
| `AUTHORITY` | 84 |

빈도가 높은 literal은 `정합` 1,095건, `전건` 582건, `완료` 521건,
`PASS` 505건, `불변` 438건, `무변경` 284건, `bit-exact` 253건이었다.
후보가 존재하는 문건의 역할별 분포는 RESULT 135개,
DIRECTION_OR_AUDIT 43개, HANDOVER 18개, PLAN 16개를 포함한다.

## 후보 레코드의 증거 연결

각 후보는 다음 항목을 보존한다.

1. 안정적인 candidate/document ID
2. 실제 물리 행 또는 JSON pointer
3. literal, 문맥 excerpt와 원행 SHA-256
4. 고유 blob SHA와 전체 파일 SHA-256
5. 동일 blob의 최초 Git 등장 commit
6. Phase 057 전문 검독 evidence와 provisional claim ID
7. 아직 판정 전임을 나타내는 `UNADJUDICATED`

따라서 Step 20.4는 검색 결과를 다시 추정하지 않고, 같은 원문 위치를
commit patch 및 검증 산출물과 직접 대조할 수 있다.

## 중요한 해석 경계

- `미완료`는 문자열 `완료`를 포함한다.
- 계획서의 gate 정의와 향후 실행 명령도 `PASS`를 포함한다.
- 검토 문건이 과거의 “정합” 주장을 인용하거나 반박한 경우도 포함된다.
- `전건`, `bit-exact`, `무변경`은 대상 집합과 허용오차가 없으면
  과학적 불변성의 증거가 아니다.
- commit subject 또는 result의 자기보고는 실제 diff·로그와 대조되기 전에는
  독립 증거가 아니다.
- 같은 선언의 버전별 복제는 별도 문서 위치로 보존하되, 하나의 독립 검증을
  여러 검증으로 세지 않는다.

이 경계 때문에 3,487라는 수는 “완료된 항목 수”도 “오류 수”도 아니다.
Step 20.4의 보수적 판정 모집단이다.

## 재현성 검증

추출기를 연속 두 번 실행해 다음 SHA-256이 동일함을 확인했다.

`dc223d4d2ed637da4032eafd95715d8e49208c45dab05e62390441d1a76e00d2`

생성 JSON 크기는 2,674,564 bytes이며 다음 조건을 모두 만족했다.

- 271/271 문건 scan
- 모든 후보의 document ID 연결
- 모든 문건의 exact-blob 최초 commit 연결
- 모든 문건의 기존 전문 검독 evidence 연결
- 생성 HTML payload 제외
- 판정 미수행 상태의 명시

## 다음 단계

Phase 057 Step 20.4에서 먼저 부정·계획·정의·인용 문맥을 분리한다.
그 다음 실제 patch, machine result, 시험 로그와 연결하여 각 후보를
`CONFIRMED`, `OVERCLAIMED`, `PARTIAL`, `UNVERIFIED` 중 하나로 판정한다.
반복 복제된 선언은 claim family로 묶되 모든 원문 위치의 처분을 남긴다.
