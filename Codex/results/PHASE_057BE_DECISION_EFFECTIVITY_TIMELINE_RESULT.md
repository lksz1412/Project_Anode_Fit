# Phase 057BE 결정 효력·복제·철회 계보 결과

정본일: 2026-07-28  
대상 단계: Phase 057 Step 20.5  
기준 커밋: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`

## 판정

`PASS_P057_DECISION_EFFECTIVITY`

229개 commit의 first-parent 이력, 271개 고유 문건 blob의 673개 path event,
3,487개 완료·권위·정합 후보 판정을 연결했다. 현재 효력이 있는 결정,
복제돼 남은 stale 표현, 후속 commit으로 철회된 결정과 검증 범위가 좁아진
PASS를 분리했다.

## Merge와 copy-forward를 분리한 결과

- 이 범위의 merge commit: **0**
- 문건 path event: **673**
- 여러 경로에 같은 current blob이 존재: **42 blob**
- current blob이 대표 경로보다 다른 경로에서 먼저 등장: **34 blob**
- 한 current blob의 최대 복제 경로: **9**

따라서 과거 문건의 “merge-ready”는 Git merge가 발생했다는 뜻이 아니다.
버전 폴더를 통째로 복제한 뒤 국소 수정한 이력이 많으며, 이 과정에서
이전 버전의 “현행 최신”, “완결”, “무변경” 표현도 함께 복제됐다.
같은 문장을 여러 버전에서 발견해도 독립 검증 횟수로 세지 않는다.

## 주요 효력 변화

### v1.0.10–v1.0.11: R1 물리 재설계 오판 철회

`945a091`은 near-delta/broadening의 전면 재설계가 필요하다는 R1 판단을
철회했고, `0c29745`가 이를 v1.0.11 handover rev.2에 반영했다.
따라서 최초 R1 진단은 현재 물리 요구로 승계하지 않는다. 다만 이 사례는
실제 출력과 구현을 실행하기 전 비판을 확정하면 안 된다는 운영 교훈으로
승계한다.

### v1.0.25: regsol 구현 삭제와 Ω 논리의 분리

`edbc4a2`에서 equilibrium의 regular-solution kernel은 코드에서 삭제됐다.
하지만 Ω는 히스테리시스·장벽·상 판정 서술에 남았다. 그러므로 이후의
“문건=코드 완결”은 regular-solution 이론이 equilibrium fitting 경로에
구현됐다는 뜻으로 읽을 수 없다. Ω의 역할을 하나의 자유에너지 계보로
다시 연결하기 전까지 상태는 `DISCONNECTED`다.

### v1.0.25.1→v1.0.25.2: 권위 문구의 stale 복제

`27062ee` 시점에는 v1.0.25.1이 최신이었다. `99a6017`에서 v1.0.25.2
폴더를 copy-forward하면서 `ARCHIVE_NOTE` 제목의 “v1.0.25.1 현행 최신”도
복제됐다. 후반 추가 문단과 최종 handover는 v1.0.25.2를 최신으로 정정하지만
첫 행은 남았다. 현재 권위는 경로 이름이 아니라 최종 기준 commit과 사용자
재확인으로 v1.0.25.2에 부여한다.

### v1.0.25.2: 7-gallery default 도입과 철회

| commit | 변화 | 현재 효력 |
|---|---|---|
| `c768153` | Si 7-gallery skew seed와 two-phase probe 추가 | 후보 증거, 자동 정본 아님 |
| `77ae0d9` | 기본 transition set을 7-gallery skew로 역전 | `7b342dd`에서 철회 |
| `ab196b2` | 마감 handover·final 표현 | U11/U12 및 최종 handover가 supersede |
| `eb6b88b` | 새 default가 `dw/dT`를 소거함을 명기 | 결함 발견으로 유효 |
| `7b342dd` | default 역전 철회, legacy4 default 복원 | 현재 기준선에 유효 |
| `3b5fd05` | 최종 handover 재작성 | 현재 v1.0.25.2 기준 |

현재 code state는 **legacy4 + 열역학 입력이 있는 case set이 기본**이고,
7-gallery skew는 **opt-in isothermal curve representation**으로만 남는다.
7-gallery를 상 수로 읽지 않는 경고는 보존하지만, 이를 최종 물리 default나
다온도 모델로 승격하지 않는다.

## GREEN의 효력 범위

`77ae0d9` 시기의 legacy gate는 module load 직후 legacy4를 복원했다.
따라서 gate가 GREEN이었다는 사실은 legacy 경로의 회귀에는 유효하지만,
당시 새 default였던 7-gallery 경로의 온도 의존을 검증하지 못했다.

현재 운영 규칙은 다음과 같다.

1. default 변경 시험은 **시험 자체가 default를 다른 값으로 바꾸기 전에**
   새 default를 검증해야 한다.
2. GREEN은 검사한 path, 입력, 단위, 허용오차와 미검사 path를 함께 기록한다.
3. bit-exact legacy 회귀와 새 물리 타당성은 다른 gate로 둔다.
4. 문건–코드 동일성은 양쪽에 같은 오류가 복제될 수 있으므로 외부 타당성의
   대체물이 아니다.

## 현재 효력 상태

| 주제 | 현재 상태 |
|---|---|
| 과학 기준선 | v1.0.25.2 `3b5fd05` |
| v1.0.26 | 명시 제외 |
| 기본 transition 경로 | legacy4 + thermal-input cases |
| 7-gallery skew | opt-in, empirical/isothermal only |
| 7-gallery default | 철회 |
| regsol equilibrium code | 삭제됨; Ω의 다른 역할과 단절 |
| 코드 없는 이론 문건 | 아직 달성되지 않은 사용자 요구 |
| 과거 GREEN | 실제 선택 경로로 범위 제한 |
| Claude/Codex 후속 fork | Phase 068 검토 입력, baseline 아님 |

## 기계 기록

세부 사건과 현재 효력은
`Codex/results/PHASE_057_DECISION_EFFECTIVITY_TIMELINE.json`에 저장했다.
JSON parser 검증, 모든 critical commit의 baseline history 존재,
merge와 copy-forward의 분리, 철회된 default와 현재 default의 분리를
확인했다.

## 다음 단계

Phase 057 Step 21에서 문건 속 발화를
`USER_REQUIREMENT`, `MODEL_PROPOSAL`, `REVIEW_FINDING`,
`IMPLEMENTED_STATE`로 분리한다. 특히 모델이 사용자 발언이라고 요약한
문장은 실제 대화 원문이 저장돼 있지 않으면 곧바로 사용자 요구로 확정하지
않고, 여러 후속 버전에서 반복 승인·유지된 범위를 별도로 표시한다.
