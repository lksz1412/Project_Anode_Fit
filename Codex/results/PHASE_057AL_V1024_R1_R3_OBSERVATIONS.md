# Phase 057AL — v1.0.24 R1–R3 결과 관찰

정본일: 2026-07-28
세부 Step: 19.8F
범위: 3 unique documents, 141 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `results/PHASE_R1_RESULT.md`
- `results/PHASE_R2_RESULT.md`
- `results/PHASE_R3_RESULT.md`

세 결과 문건을 첫 행부터 마지막 행까지 전량 검독했다.

## Provisional Findings

### INTENT-PROV-0266 — C-rate 3,600배 문제는 v1.0.24에서 교정되지 않고 주석화됐다

R2는 `func_L_q`의 #1 반영을 “단위계약 주석, 값 무변경,
bit-exact”라고 명시한다. G-R4도 기존 값이 그대로인지 검사한다.

판정:

- 단위 문제를 문서화한 것은 `PRESERVE`.
- 이를 코드 correction으로 부르는 것은 `REJECT`.
- v1.0.24의 lag/barrier 수치는 기존 unit gauge를 그대로
  상속하며, SI 교정과 재식별이 필요하다.

### INTENT-PROV-0267 — regular-solution 물리는 equilibrium에만 배선돼 실제 유한전류 경로를 완결하지 않는다

R2는 `_regsol_dqdv`를 `equilibrium()` 분기에만 추가했고,
finite-rate `dqdv()` 확장은 열린 후보라고 명시한다. 따라서
정전류 조건의 lag, peak suppression, broadening을 계산하는
생산 경로에는 새 Si/LCO regular-solution kernel이 적용되지
않는다.

판정:

- equilibrium kernel 구현은 `PARTIAL_IMPLEMENTATION`.
- “문건 물리가 fitting 코드에 100% 반영됐다”는 판정은
  `REJECT`.
- 최종 구현은 equilibrium free energy, kinetic evolution,
  observation dQ/dV가 같은 state variable과 chemical potential을
  공유하도록 한 경로로 구성한다.

### INTENT-PROV-0268 — R2의 kernel gate는 내부 수치 성질만 확인한다

G-R3은 결과가 유한·비음이고, 면적이 1.001이며, prominent
peak가 하나라는 것을 검사했다. 이는 normalization과 gross
shape smoke test다.

그러나 다음은 검사하지 않았다.

- Maxwell/binodal capacity accounting.
- `Omega→2RT` 양측 연속성.
- grid/cap/clip 의존성.
- parameter gradient.
- 실제 Si/LCO 데이터의 held-out prediction.

판정:

- 수치 smoke test는 `PRESERVE`.
- 물리 kernel validation은 `UNVERIFIED`.
- `_regsol_binodal_xa`와 `_regsol_dqdv`의 실제 알고리즘은
  Phase 067 code-history에서 직접 감사한다.

### INTENT-PROV-0269 — toggle 기본값 기록이 R3 안에서도 모순돼 state assertion을 신뢰할 수 없다

R3 18행은 R5 정정 뒤 기본 `OFF`라고 쓰지만, 23행 AUD-1은
코드 기본 `True`라고 쓰며 이를 문건 정합으로 판정한다.
R1은 최초에 회귀 우려로 임시 True를 썼다가 사용자 지적으로
False로 고쳤다고 설명한다.

판정:

- 최종 v1.0.24.1 코드 기본값은 실제 source에서 다시 확인한다.
- 사후 수정으로 부분 갱신된 result의 state assertion은
  `STALE_CONTRADICTORY`.
- 최종 handover는 commit hash와 executable default test에서
  자동 생성한다.

### INTENT-PROV-0270 — 외부 감사 창이 실패한 뒤 master가 스스로 CLEAN을 선언했다

R3의 세 background audit는 서버 오류로 종료됐고, 같은 master가
인라인 체크리스트를 실행해 blocker/major 0을 선언했다.
체크리스트 재실행 자체는 유용하지만 독립 검수와 방법론적으로
동등하지 않다.

판정:

- 재현된 대수·게이트 결과는 `PRESERVE`.
- “독립 적대검수 CLEAN”은 `SUPERSEDE`.
- 최종 major physics gate는 저작 가정을 공유하지 않은 검수와
  원문·데이터 반증을 요구한다.

### INTENT-PROV-0271 — T-split gate는 넣은 entropy 차를 다시 읽는 round-trip이다

G-R1은 `Delta S`를 `+15/-14`로 둔 상수에서
`0.301 mV/℃`를 얻고 Dahn 0.30과 정합한다고 판정했다.
이는 식 `Delta(Delta S)/F`의 구현을 검증하지만, entropy
값을 데이터에서 새로 추정한 것은 아니다.

판정:

- 열역학 항등의 코드 구현은 `PRESERVE`.
- 데이터 검증 또는 parameter validation으로 부르는 것은
  `REJECT`.
- 다온도 원자료에서 entropy 차를 추정하고 예측 온도에서
  peak separation을 검증한다.

### INTENT-PROV-0272 — 마스터가 JSON으로 덮인 사고는 복구 가능한 작업 이력의 필요성을 입증한다

R1은 master TeX가 JSON으로 덮인 손상을 발견해 v1.0.23 shell과
로그로 복구했다. 이는 과학 내용과 별개지만 사용자가 요구한
compaction·실수 내성 workflow에 직접 관련된다.

판정:

- 원본 불가침 branch, 작은 commit, manifest, reproducible
  build, active handover를 계속 유지한다.
- 본체 수정 phase에서는 생성·편집 대상 확장자와 schema를
  pre-write gate로 검사한다.

### INTENT-PROV-0273 — 내부 상수 자기정합은 외부 물리 정박이 아니다

R3은 `U(298)=(-dH+T dS)/F`가 상수 table의 라벨 전위와
0.1 mV 이내 일치한다고 확인했다. 이는 dH가 바로 그 전위와
dS를 만족하도록 구성됐다는 내부 대수 일치다.

판정:

- parameter table의 내부 consistency는 `PRESERVE`.
- 물성값의 실험적 정당화는 `UNVERIFIED`.
- 최종 table은 fitted/derived/measured/literature 값을 구분한다.

### INTENT-PROV-0274 — v1.0.24는 유용한 equilibrium 후보를 추가했지만 사용자 목표의 완결판은 아니다

v1.0.24의 실질 delta는 regular-solution equilibrium 후보,
5-feature 상수, electronic toggle과 저작 소절이다. 단위 문제는
남고, finite-rate 배선과 public-data validation이 없다.

최종 판정:

- v1.0.24 = `NONCANONICAL_PARTIAL_EQUILIBRIUM_EXTENSION`.
- 구현·문건에서 검증된 수학 조각만 후속 정본에 재사용한다.

## Coverage Status

- 이 batch의 3문건, 141행은 `READ`.
- 누적 coverage 반영 후 목표는 251문건, 50,368행이다.
- 전체 Phase 057 잔여 목표는 20문건, 7,427행이다.

## Next

Step 19.8G:
v1.0.24 handover·index·merge readiness 3문건 210행을 전문
검독한다.
