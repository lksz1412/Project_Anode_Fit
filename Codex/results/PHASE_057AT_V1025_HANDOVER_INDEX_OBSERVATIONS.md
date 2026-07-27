# Phase 057AT — v1.0.25 handover·index 관찰

정본일: 2026-07-28
세부 Step: 19.8N
범위: 2 unique documents, 308 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `Claude/docs/v1.0.25.1/results/HANDOVER_v25.md`
- `Claude/docs/v1.0.25.1/results/INDEX_v25.md`

두 문건을 첫 행부터 마지막 행까지 전량 검독했다. 사용자 발화,
당시 scope, 최종 검증 뒤 stale해진 상태를 구분했다.

## Provisional Findings

### INTENT-PROV-0345 — v1.0.25의 사용자 범위는 “전문 재작성 아님, 국소 패치”였다

handover는 v1.0.24.1 재검수에서 나온 결함만 국소 수정하고
연계 절만 보완하라는 사용자 지시를 기록한다. 기존 식 번호,
label, 표현 보존과 additive 방식은 그 scope에서 채택됐다.

판정:

- v1.0.25 계보 해석에는 `PRESERVE_AS_HISTORICAL_SCOPE`.
- 현재 사용자는 전체 계보 재감사 뒤 endgame 재설계를 요청했으므로
  과거 local-patch 경계는 새 canonical 작업을 구속하지 않는다.

### INTENT-PROV-0346 — “문건=코드”는 사용자가 명시한 핵심 기준이다

사용자는 문건이 선언한 것과 코드가 계산하는 것이 달라서는
안 되고 둘이 하나여야 한다고 지시했다. 당시에는 doc–code
30/30 audit로 구체화됐다.

판정:

- 1:1 conformance 원칙은 `PRESERVE`.
- 현재의 추가 제약에 따라 방향은 theory/chemistry document
  → implementation specification → code로 둔다.
- 같은 오류를 함께 복제하는 것을 막기 위해 literature와
  independent derivation gate를 앞에 둔다.

### INTENT-PROV-0347 — 공개 데이터 직접 fitting과 peak·valley 형상 평가는 사용자 의도다

사용자는 문헌 인용만 하지 말고 공개 data를 직접 fit하며,
R² 하나가 아니라 peak-region과 valley-region shape를 함께
판정하라고 했다.

판정:

- 이 검증 철학은 `PRESERVE_AND_EXPAND`.
- likelihood와 residual correlation, feature-wise error,
  charge conservation, cross-condition prediction, uncertainty를
  더한다.
- 사용자가 확인한 “실제 fitting은 된다”는 calibration evidence를
  버리지 않고 physics validity와 구분한다.

### INTENT-PROV-0348 — regsol 삭제는 특정 v1.0.25 구현에 대한 사용자 결정이었다

사용자는 DG-1에서 당시 @3 kernel을 완전 삭제하라고 결정했다.
그 근거는 낮은 transition count에서의 이득이 7+7 basis에서
부호 역전한 것이었다.

판정:

- v1.0.25 구현 계보에서는 `PRESERVE_AS_USER_DECISION`.
- 이것은 regular-solution thermodynamics 자체의 오류 판정이
  아니며 handover도 그렇게 구분한다.
- 새 정본에 관련 free-energy model을 검토하려면 독립 문헌,
  multi-cell/multi-condition evidence, 연속성·한계 검증과
  명시적 재채택 결정을 요구한다.

### INTENT-PROV-0349 — handover와 index는 최종 v1.0.25.1 상태보다 stale하다

두 문건은 build 미수행, gate 8종, edited section 14,
+250/+257 lines를 현 상태로 쓴다. 후속 document edit report는
최종 재검 후 XeLaTeX 성공, forbidden gate 추가로 9종,
15 files/+262 lines를 기록한다.

판정:

- handover/index의 상태 표는 chronology상 `SUPERSEDED`.
- 지시·의도·경로 정보는 유효하지만 acceptance status에는
  후속 report가 우선한다.
- 새 workflow는 canonical status 한 곳에서 파생된 index와
  handover를 생성해 상호 drift를 막는다.

### INTENT-PROV-0350 — v1.0.25 당시 code guide와 fitting guide가 이미 stale했다

index는 `CODE_GUIDE_v24`가 삭제된 regsol 경로를 계속 설명하고,
`FITTING_GUIDE`가 alpha와 SI opt-in을 반영하지 않았다고
명시한다.

판정:

- v1.0.25는 repository-wide document–code conformance가
  완료된 version이 아니다.
- Phase 067에서 guide, tests, examples, defaults까지 public
  surface 전체를 감사한다.

### INTENT-PROV-0351 — 다온도·다율속 데이터가 핵심 식별 gate라는 사용자 방향이 남아 있다

N13은 stage-2L 온도 변화, `Omega` 점값, O3-LCO 전자항
온도의존, alpha–lag 분리에 다온도·다율속 half-cell data가
필요하다고 명시한다.

판정:

- 이 요구는 연구 시작 동기와 직접 일치하므로
  `PRESERVE_AS_TOP_LEVEL_ACCEPTANCE`.
- 회사 data만을 기다리지 않고 공개 graphite, Si,
  graphite+Si, doped high-voltage LCO 자료를 문헌·repository에서
  병렬 확보한다.

### INTENT-PROV-0352 — 역할 배분 기록은 Fable 계보 비교의 근거다

v1.0.25 code·gate와 cascade TODO는 Fable 5.0이 실행하고,
Opus 5.0이 계획·물리 문건·통합 검수를 맡았다고 기록한다.

판정:

- v1.0.21–v1.0.23만이 아니라 v1.0.25의 일부 구현도 Fable
  계보임을 comparison matrix에 포함한다.
- 모델 이름을 품질 증거로 쓰지 않고 commit별 수식·코드·시험으로
  재판정한다.

### INTENT-PROV-0353 — “Omega 물리는 전량 유효”는 검증 결과가 아니라 당시 handover 명령이다

handover는 regsol kernel 삭제와 별개로 `Omega` hysteresis,
barrier, phase classification을 전량 유효라고 반복한다.
그러나 equilibrium chemical potential과의 연결이 끊긴 문제는
검사하지 않는다.

판정:

- history 보존 주의로는 유효하지만 scientific acceptance는
  `UNVERIFIED`.
- Phase 067에서 각 `Omega` 사용처의 단위, 정의, calibration,
  shared-parameter consistency를 직접 감사한다.

### INTENT-PROV-0354 — 원본 보존과 GitHub 기록은 사용자 운영 의도다

handover는 v1.0.24/24.1 원본 불가침, master만 commit/push,
GitHub upload 요청을 기록한다.

판정:

- 현재 작업도 원본과 main을 건드리지 않고 branch-only
  commit/push를 계속한다.
- 새 산출물은 작은 검증 단위로 자주 커밋하되, acceptance
  status는 freeze된 commit에만 붙인다.

## Direction Recovered

1. 문건과 코드는 동일한 물리를 표현해야 한다.
2. 이론이 먼저이고 코드는 그 이론에서 파생돼야 한다.
3. 공개 실험 data를 직접 fit하되 형상과 조건 외삽을 본다.
4. 원본·실패·철회 이력을 삭제하지 않는다.
5. 과거 local patch 경계를 새 endgame의 품질 상한으로 삼지 않는다.
6. stale handover가 최신 상태를 덮지 않도록 machine state에서
   문서를 생성한다.

## Coverage Status

- 이 batch의 2문건, 308행은 `READ`.
- 누적 coverage 반영 후 목표는 265문건, 52,977행이다.
- 전체 Phase 057 잔여 목표는 6문건, 4,818행이다.

## Next

Step 19.8O:
v1.0.25 merge readiness 1문건 204행을 전문 검독한다.
