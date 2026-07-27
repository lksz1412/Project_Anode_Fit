# Phase 057AN — v1.0.24 Markdown code guide 관찰

정본일: 2026-07-28
세부 Step: 19.8H
범위: 1 unique document, 374 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `CODE_GUIDE_v24.md`

1–200, 201–374의 연속 범위로 나눠 첫 행부터 마지막 행까지
전량 검독했다.

## Provisional Findings

### INTENT-PROV-0284 — 한 객체의 관측 연산자들이 서로 다른 평형 열역학을 사용한다

guide는 `kernel='regsol'`이 `equilibrium()`에서만 작동하고,
다음은 같은 transition 설정의 kernel을 무시해 항상 logistic을
쓴다고 명시한다.

- finite-rate `dqdv()`와 `curve()`.
- `solve_U_oc()`.
- `entropy_coefficient()`.
- reversible heat.

따라서 regular-solution으로 계산한 평형 dQ/dV와, logistic으로
푼 OCV·entropy·finite-current curve는 하나의 동일 free energy의
서로 다른 미분/응답이 아니다.

판정:

- 코드의 scope disclosure는 `PRESERVE`.
- thermodynamic self-consistency는 `FAIL`.
- 최종 코드는 한 chemical potential/free energy interface에서
  equilibrium, OCV inversion, derivatives, kinetics를 파생한다.

### INTENT-PROV-0285 — equilibrium binodal에 `delta=w` broadening을 넣으면 물리층이 섞인다

guide는 `Omega>2RT`에서 Maxwell binodal을 찾은 뒤
`U0 near-delta + delta=w broadening`을 적용한다고 설명하고,
transition key `delta`를 “regsol kinetic width”라고 부른다.

평형 two-phase measure의 이상적 singularity, 재료 이질성/
유한입자 분포, kinetic broadening, instrument smoothing은
원인이 다르다. equilibrium 함수 안에서 `w` 또는 `delta`로
한 번에 넓히면 fit은 가능해도 parameter 의미가 섞인다.

판정:

- binodal 계산 자체는 `PRESERVE_FOR_CODE_AUDIT`.
- equilibrium singular measure와 observation/kinetic kernels를
  계층 분리한다.
- `delta`의 물리 정의와 단위를 재유도하지 못하면 empirical
  observation parameter로 명시한다.

### INTENT-PROV-0286 — hard cap·clamp·grid guard는 사용자 금지 원칙과 충돌한다

옵션표에는 다음 고정 수치가 있다.

- `z_cut=4.357`.
- `A_cap_RT=4.0`.
- `z=4.0≈7%`를 실현하는 clamp.
- `L_V*40 > grid spacing` 해상 guard.
- `_finite_pos`, `_finite_nonneg` 범위 guard.

일부 입력 검증은 필요하지만, 물리 유도 없는 cap·clip과
해상도 의존 branch는 curve shape와 gradient를 바꿀 수 있다.

판정:

- NaN/invalid input rejection은 `NUMERICAL_SAFETY`.
- 값을 물리 범위로 몰래 자르는 clamp와 fixed cap은
  `REJECT_UNLESS_DERIVED`.
- 최종 구현은 domain-preserving parameterization, explicit
  failure, adaptive resolution을 우선한다.

### INTENT-PROV-0287 — 상수 모음은 피팅 seed이지 재료 기본값 권위가 아니다

guide는 graphite 4/5/6, LCO 3-transition, Si/SiOx/SiC case
constants와 specific capacity를 제공하면서 대부분을
“시연값·피팅 override”라고 표기한다. `Q_j` 단위도 상대값이다.

판정:

- example seed로서의 유용성은 `PRESERVE`.
- graphite/LCO/Si numerical defaults로의 과학적 승격은
  `REJECT`.
- 최종 public API는 universal physical constants 외 재료
  parameter set을 명시적 dataset/calibration artifact로 로드한다.

### INTENT-PROV-0288 — wt%→capacity fraction 변환은 capacity source와 상태에 민감하다

blend `from_wt()`는 고정 specific capacity table을 사용해
mass fraction을 capacity fraction으로 바꾼다. guide 값은
graphite 372와 Si case별 1000/1710/3117이다.

실제 accessible capacity는 formation, cutoff, rate, cycle,
particle/composite formulation에 따라 달라지므로 하나의 고정값은
조성 의미를 바꿀 수 있다.

판정:

- algebraic conversion은 `PRESERVE`.
- specific capacities를 universal default로 쓰는 것은
  `EMPIRICAL_ONLY`.
- 실험 cell의 measured reversible capacity와 uncertainty를
  입력으로 요구하거나 명시적 prior로 둔다.

### INTENT-PROV-0289 — fitting 예시는 평형 in-sample curve fit이며 연구 목표 전체를 검증하지 않는다

H.6 예시는 한 온도의 `equilibrium()`을 `curve_fit`으로
center, width, capacity, background에 맞춘다. 이는 공개 pOCV
calibration을 재현하는 기본 도구다.

그러나 finite-current, temperature series, parameter
correlation, noise covariance, cross-validation은 포함하지 않는다.

판정:

- 최소 재현 예시는 `PRESERVE_IN_COMPANION`.
- 최종 fitting stack은 global multi-condition likelihood와
  calibration/validation split을 사용한다.

### INTENT-PROV-0290 — LCO와 Si의 software reuse 경계가 물리 closure의 공백을 다시 확인시킨다

guide는 LCO가 graphite class의 한 entropy seam만 바꾸고,
blend는 graphite instances의 가산 조합이며 plasticity/
nonadditivity는 stub이라고 명시한다.

판정:

- 공통 API·solver 재사용은 `IMPLEMENTATION_PRESERVE`.
- 재료별 physics closure는 `INCOMPLETE`.
- doped high-voltage LCO와 Si stress/path dependence를 별도
  model component로 만든다.

### INTENT-PROV-0291 — code guide의 구조는 최종 conformance companion으로 재사용한다

flowchart, option table, transition key table, example, constant
tier, symbol–code–unit mapping은 추적성이 높다.

판정:

- 이 구조는 `PRESERVE_AND_REBUILD`.
- 이론 문건에서 분리하고 machine-readable schema와 test link를
  추가한다.
- 각 옵션에는 physical status, default authority, unit,
  differentiability, data evidence를 표시한다.

### INTENT-PROV-0292 — v1.0.24 서술 queue는 완료됐지만 HTML·JSON은 아직 별도 대상이다

v1.0.24.1 서술 26문건 2,080행을 전량 읽었다. HTML code guide
3,812행과 snapshot JSON 1행은 Step 19.9에서 markup/value
전 범위를 별도로 검사한다.

## Coverage Status

- 이 batch의 1문건, 374행은 `READ`.
- 누적 coverage 반영 후 목표는 255문건, 50,952행이다.
- v1.0.24.1 서술 queue는 26/26문건, 2,080/2,080행 `READ`.
- 전체 Phase 057 잔여 목표는 16문건, 6,843행이다.

## Next

Step 19.8I:
v1.0.25·v1.0.25.1 archive와 touchup 3문건 288행을 전문
검독한다.
