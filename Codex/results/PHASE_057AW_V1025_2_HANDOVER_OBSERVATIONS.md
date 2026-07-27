# Phase 057AW — v1.0.25.2 handover 관찰

정본일: 2026-07-28
세부 Step: 19.8Q
범위: 1 unique document, 175 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md`

첫 행부터 마지막 행까지 전량 검독했다. 사용자 결정,
commit sequence, current default, unresolved P1–P4를 구분했다.

## Provisional Findings

### INTENT-PROV-0378 — v1.0.25.2가 최신이고 v1.0.26은 authority가 아니다

handover는 v1.0.25.2를 현행 최신으로 지정하고 v1.0.26의
일부 재검증 결과만 채택해 반영했다고 설명한다.

판정:

- 현재 기준은 `Claude/docs/v1.0.25.2/`.
- v1.0.26 자체를 scientific authority나 작업 baseline으로
  사용하지 않는다.
- v1.0.25.2에 실제 반영된 식·코드·시험만 독립 재검토한다.

### INTENT-PROV-0379 — “이론 regsol, fitting logistic”은 사용자 확정 이력이지만 최종 consistency 해법은 아니다

D1은 regular-solution을 이론층에 유지하고 fit kernel은
logistic 계열로 분리했다. 이는 당시 실패한 regsol curve fit과
유효한 이론 유도를 함께 보존하는 실용적 결정이었다.

판정:

- historical decision으로 `PRESERVE`.
- 그러나 하나의 물리 모델을 주장하려면 equilibrium,
  observation, kinetics가 어떻게 같은 latent state/free
  energy에서 연결되는지 명시해야 한다.
- review-only regsol과 adopted logistic을 단순 병치하는 것으로
  “코드가 문건을 100% 반영”했다고 보지 않는다.

### INTENT-PROV-0380 — 문건의 코드 배제는 사용자가 직접 확정한 규칙이다

D5는 “문건은 코드 이야기를 하지 않는다—이론 문서여야 한다”는
사용자 결정을 기록한다. 당시 구현 절차를 code section과
appendix로 이관했다.

판정:

- 사용자 방향으로 `PRESERVE_AND_STRENGTHEN`.
- 최종 theory manuscript에는 그 code section/appendix도
  포함하지 않고 별도 implementation/conformance companion으로
  분리한다.

### INTENT-PROV-0381 — 7-gallery component를 staging transition에 억지 배정하면 안 된다

P1은 각 gallery가 어느 parent staging transition의 entropy를
상속할지 미결이라고 하며 nearest-voltage 배정이 같은 cluster를
서로 다른 parent로 쪼갠다고 보고한다.

판정:

- evidence 없는 자동 배정은 `REJECT`.
- 이 결정은 사용자 취향이 아니라 primary literature,
  multi-temperature data, structural constraints가 판단한다.
- component가 단순 basis라면 개별 thermodynamic transition으로
  승격하지 않는다.

### INTENT-PROV-0382 — 더 나은 closure는 physical transition과 shape basis를 계층 분리하는 것이다

7개 logistic/skew peak를 각각 독립 thermodynamic species로
만들면 gallery–phase 혼동과 entropy 상속 문제가 생긴다.

판정:

- parent physical transition은 구조·free-energy evidence로
  정의한다.
- 한 parent 안의 disorder, particle/strain/composition
  heterogeneity를 normalized distribution 또는 observation
  kernel로 표현하고 parent의 center-temperature law를 공유한다.
- finite-rate lag는 별도 kinetic layer로 두어 equilibrium
  heterogeneity와 식별한다.

### INTENT-PROV-0383 — latest 문건은 build가 끝나지 않았다

v1.0.25.1은 PDF build가 완료됐지만 v1.0.25.2의 신규 식,
각주, 두 subsection은 XeLaTeX 3-pass가 미수행이다.

판정:

- v1.0.25.2는 source latest이지만 build-verified latest는 아니다.
- 후속 implementation 전에 source audit은 가능하나 release
  artifact로는 `BUILD_UNVERIFIED`.

### INTENT-PROV-0384 — blend normalization과 capacity denominator가 최우선 code-audit 항목이다

handover는 Codex P0-4를 아직 대조하지 않았고 14-component
blend와 직접 연결되므로 다음 1순위라고 명시한다.

판정:

- Phase 067에서 mass fraction, capacity fraction, total
  electrode/cell capacity denominator, stoichiometric range와
  dQ/dV integral을 end-to-end 대조한다.
- graphite+Si fit의 높은 R²를 이 검증 전에는 조성 추론
  evidence로 쓰지 않는다.

### INTENT-PROV-0385 — 현재 confirmed code defects를 carryover가 아니라 blocker로 올린다

`n/w` 부재 시 value/derivative 불일치, 동시 보유 시 silent
precedence, untested P0-2–P0-5가 남아 있다.

판정:

- 이 항목들은 새 code completion 이전에 repair/test가 필요한
  blocking defects다.
- silent fallback/precedence 대신 explicit typed law와 validation
  error를 사용한다.

### INTENT-PROV-0386 — 작업 방식 자기반성은 새 운영 규칙과 직접 일치한다

handover는 default를 바꾸기 전에 default test를 만들 것,
실행 가능한 진단은 기록 전에 실행할 것, 예산 부족으로 문건
경계를 우회하지 말 것, 식은 검산 후 반영할 것, 수치는
원자료에서 읽을 것, GREEN의 측정 범위를 밝힐 것을 규칙으로
남겼다.

판정:

- 전부 `PRESERVE_AS_GOVERNANCE`.
- master plan의 phase gate와 step history schema에 명문화한다.

### INTENT-PROV-0387 — v1.0.25.2는 사용자의 연구 목표를 위한 좋은 진단점이지 완성본은 아니다

현재는 RT curve-fit seed, theory-only two-phase equation,
legacy thermodynamic default가 병존한다. P1 열역학 input,
P2 build, P3 code defects, P4 model-family wording이 열려 있고
high-voltage doped LCO와 multi-condition validation도 없다.

판정:

- 최신 baseline으로 보존하되 endgame authority로 승격하지 않는다.
- 새 작업은 이 실패가 드러낸 “fit basis와 thermodynamic
  transition의 계층 분리”를 중심 설계 원칙으로 삼는다.

## Direction Recovered

1. 최신 기준은 v1.0.25.2이며 v1.0.26은 제외한다.
2. 문건은 물리·화학 이론만 담는다.
3. fitting basis를 물리 상이나 thermodynamic species로
   자동 승격하지 않는다.
4. physical transition–heterogeneity–kinetics–observation을
   계층화한다.
5. 확인 전 결론, untested default, silent fallback을 금지한다.
6. 공개 data fit 성공은 보존하되 multi-condition prediction과
   분리한다.

## Coverage Status

- 이 batch의 1문건, 175행은 `READ`.
- 누적 coverage 반영 후 목표는 268문건, 53,737행이다.
- v1.0.24.1–v1.0.25.2 서술 queue는 38/38문건,
  4,865/4,865행 전량 `READ`.
- 전체 Phase 057 잔여 목표는 3문건, 4,058행이다.

## Next

Step 19.9A:
v1.0.24 HTML code guide 1문건 3,812행을 최대 400행 연속
구간으로 나눠 전문 검독한다.
