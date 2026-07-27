# Phase 057AV — v1.0.25.2 archive note 관찰

정본일: 2026-07-28
세부 Step: 19.8P
범위: 1 unique document, 381 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md`

1–210, 211–381의 연속 범위로 나눠 첫 행부터 마지막 행까지
전량 검독했다. U1–U12의 시간순 상태를 따라 중간 기본값과
최종 되돌림을 구분했다.

## Provisional Findings

### INTENT-PROV-0364 — v1.0.25.2의 최종 기본은 7-gallery가 아니라 legacy 4-transition이다

U10은 7-gallery skew를 default로 승격했지만, U12 자기감사에서
온도·동역학 입력 부재를 발견해 반려했다. 최종 조치는
`DEFAULT_GRAPHITE_TRANSITIONS=GRAPHITE_STAGING_LIT` 복원과
7-gallery를 켜는 opt-in switch다.

판정:

- 현재 상태를 “7-gallery가 기본”으로 읽으면 안 된다.
- v1.0.25.2의 최종 default는 thermodynamic inputs를 가진
  legacy 4-transition이며, skew7은 isothermal-fit-only
  opt-in이다.

### INTENT-PROV-0365 — skew7은 정온 곡선 표현에는 강하지만 thermodynamic model은 아니다

skew7 seed는 `U,w,Q,alpha`만 갖고 `dH_rxn,dS_rxn,n,Omega`와
kinetic parameters가 없다. U10 default에서는 288→308 K
곡선 변화가 0이었고, center와 width temperature contributions가
모두 사라졌다.

판정:

- 공개 RT data의 calibration asset으로 `PRESERVE`.
- multi-temperature equilibrium, entropy, reversible heat,
  finite-current model로의 승격은 `REJECT_UNTIL_COMPLETED`.
- gallery를 parent staging transition에 물리적으로 배정하고
  thermodynamic parameters와 uncertainty를 채워야 한다.

### INTENT-PROV-0366 — gate가 legacy를 강제해 새 default 결함을 숨겼다

golden harness는 module load 직후 legacy switch를 켰기 때문에
바뀐 public default를 시험하지 않았다. 모든 기존 gate가
GREEN이어도 새 default의 온도 의존 상실은 검사 대상 밖이었다.

판정:

- test harness가 production default를 mutate한 뒤 검증하는
  구조는 `REJECT`.
- canonical-default, explicit-legacy, custom-parameter paths를
  독립 process에서 각각 시험한다.
- default 변경에는 temperature/rate/heat feature-preservation
  gate를 자동 요구한다.

### INTENT-PROV-0367 — fit 성능 우세와 parameter 물리성은 문건 스스로 분리했다

같은 RT data에서 skew-logistic C가 graphite, Si, blend의
R²/BIC와 일부 peak/valley RMSE를 개선했다. 그러나 graphite
alpha 7개 중 5개, Si alpha 1개가 상한 8에 붙어 미식별이며
sub-resolution 급준 feature를 세우는 역할이라고 인정한다.

판정:

- fit improvement는 `PRESERVE_AS_IN_SAMPLE_EVIDENCE`.
- alpha 값의 물질 물리 해석은 `REJECT`.
- bound saturation, effective degrees of freedom, residual
  covariance, held-out cell/protocol/condition 성능을 다시 평가한다.

### INTENT-PROV-0368 — BIC 우세는 독립 validation을 대신하지 않는다

BIC는 parameter count를 벌점으로 주지만 동일 dataset의
likelihood 가정에 의존한다. alpha 경계 포화와 correlated
dQ/dV residual이 있으면 정규 근사와 effective parameter count도
불확실하다.

판정:

- 동일 noise model 아래 model-selection 보조 지표로 보존한다.
- cell/protocol/temperature/rate holdout과 posterior predictive
  checks 없이는 확정 구성이라 부르지 않는다.

### INTENT-PROV-0369 — fitted `Omega`를 logistic-skew 확정 구성의 phase 증거로 옮길 수 없다

보고된 graphite `Omega/RT=[1.916,2.027,2.472,2.604]`는
regular-solution 4-transition fit A의 결과다. 우세하다고
선택한 model C는 logistic-skew 7-transition이며 equilibrium
shape가 `Omega`에서 파생되지 않는다.

판정:

- A에서 fit한 `Omega`를 C의 gallery/phase classification으로
  전이하는 것은 `MODEL_CROSSOVER_ERROR`.
- parameter와 phase claim은 그것을 생성한 model/dataset에
  귀속시킨다.
- shared free-energy model이 없으면 logistic fit과
  `Omega/RT` 판정을 독립 evidence로 분리한다.

### INTENT-PROV-0370 — 새 `eq:sifr-twophase`는 가장 가치 있는 대조 대상이지만 채택 구현은 아니다

v1.0.25.2는 `Omega>2RT`에 대해 miscibility-gap mass와
solid-solution density를 broadening kernel과 합친 closed form을
추가하고, 면적·critical-limit 수치 검산을 보고한다. 동시에
fitting kernel은 logistic-only라고 유지한다.

판정:

- Phase 065에서 free-energy convexification부터 독립 재유도한다.
- 기존 Codex conformance의 `eq:sifr-twophase` 구현과
  mass, `Omega<2RT`, `Omega->2RT`, translation, grid
  convergence를 수치 대조한다.
- 맞더라도 canonical adopted model과 review-only theory의
  지위를 명확히 나눈다.

### INTENT-PROV-0371 — critical-point 연속성 설명은 선행 “불연속 전환” 문구를 사실상 교정한다

U9 검산은 `Omega->2RT`에서 dQ/dV 값 차이가 0으로 줄고
gap weight가 square-root로 닫혀 값은 연속이나 도함수는
발산한다고 보고한다. 그런데 §5b는 broadening 이전 등온선이
불연속 전환한다고 계속 설명한다.

판정:

- “branch 성격 변화”, “상태량 연속성”, “도함수 비해석성”을
  구분해 재작성한다.
- 단순히 broadening 전/후가 다르다는 각주로 물리적 연속성
  문제를 덮지 않고 order parameter와 convexified potential의
  극한을 재유도한다.

### INTENT-PROV-0372 — 구현 서술을 본문에서 옮긴 조치는 사용자 경계를 확인한다

사용자는 “문건은 코드 이야기를 하지 않고 코드 근간의 이론
문서여야 한다”고 지적했다. 이에 grid/rebin/smoothing 등은
본문에서 code section과 appendix로 이동됐다.

판정:

- 사용자 의도 복원으로 `PRESERVE`.
- 현재 사용자의 더 명확한 요구에 따라 code section/appendix도
  최종 이론 문건 밖의 별도 companion으로 완전히 분리한다.

### INTENT-PROV-0373 — width key의 두 API 결함은 v1.0.25.2에 남아 있다

`n`과 `w`가 모두 없으면 width는 `RT/F`로 계산하면서
`dw/dT=0`을 반환하고, 둘 다 있으면 `n`이 조용히 이겨 `w`가
비활성이다. preset 일부가 두 key를 함께 갖는다.

판정:

- 이는 Phase 067의 confirmed code defect로 우선 검사한다.
- ambiguous state는 명시적 error로 막고, width law를 typed
  variant로 분리해 value와 derivative를 한 source에서 계산한다.

### INTENT-PROV-0374 — time-base 3600 계약은 불변성 시험이 없어 아직 닫히지 않았다

문건은 `h^-1` 대 `s^-1`의 3600을 흡수 규약으로 설명하고
Coulomb `Q_cell` 우회로를 둔다고 한다. 그러나 단위 표현을
바꿔도 동일 물리 곡선이 나오는 invariance test는 없다.

판정:

- 주석이 있다는 이유로 `PASS`하지 않는다.
- unit-aware inputs와 hour/second equivalent-case test를
  Phase 067에 둔다.

### INTENT-PROV-0375 — single-cell fit seed를 `_LIT`로 부르는 명명은 evidence tier를 흐린다

`GRAPHITE_MSMR7_LIT`은 single-cell nonequilibrium pOCV fit,
free-background 부재 당시 aliasing, sub-resolution width의
tier-C seed라고 스스로 제한한다.

판정:

- literature-anchored value와 dataset-calibrated seed를
  같은 `_LIT` 이름으로 섞지 않는다.
- source/evidence tier가 드러나는 immutable parameter artifact로
  분리한다.

### INTENT-PROV-0376 — v1.0.25.2는 최신이지만 archive heading 자체는 stale하다

파일 첫 줄은 v1.0.25.1을 현행 최신이라고 쓰지만 U7은
v1.0.25.2가 최신이라고 정정한다. 사용자의 현재 설명과도
U7이 일치한다.

판정:

- latest authority는 v1.0.25.2, v1.0.26은 제외한다.
- additive chronology는 보존하되 canonical entrypoint의 첫
  상태 문장은 실제 최신성을 정확히 표시해야 한다.

### INTENT-PROV-0377 — high-voltage doped LCO와 연구의 온도·전류 현상은 여전히 미완이다

v1.0.25.2의 새 실측은 주로 RT graphite/Si/blend kernel
comparison이다. doped high-voltage LCO, multi-temperature
constant-current peak suppression/broadening, potential-dependent
barrier validation은 닫지 못했다.

판정:

- v1.0.25.2를 연구 endgame으로 보지 않는다.
- 해당 세 조건을 새 master plan의 scientific acceptance
  backbone으로 둔다.

## Direction Recovered

1. 정온 curve-fit basis가 열역학·동역학 model을 대체해서는 안 된다.
2. 새 default는 legacy test가 아니라 실제 public path로 검증한다.
3. parameter bound saturation은 물리량 확정이 아니라 미식별 신호다.
4. 이론 본문에서 구현 절차를 완전히 분리한다.
5. 물리 배정을 모르면 자동 nearest mapping으로 꾸미지 않는다.
6. 자기감사로 잘못된 default를 되돌린 결정을 보존한다.

## Coverage Status

- 이 batch의 1문건, 381행은 `READ`.
- 누적 coverage 반영 후 목표는 267문건, 53,562행이다.
- 전체 Phase 057 잔여 목표는 4문건, 4,233행이다.

## Next

Step 19.8Q:
v1.0.25.2 handover 1문건 175행을 전문 검독한다.
