# Phase 057AS — v1.0.25 document edit report 관찰

정본일: 2026-07-28
세부 Step: 19.8M
범위: 1 unique document, 312 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `Claude/docs/v1.0.25.1/results/V1025_DOC_EDIT_REPORT.md`

첫 행부터 마지막 행까지 전량 검독했다. 초도 검사와 마감 후
재검사, 기계 정합성과 물리 타당성을 분리했다.

## Provisional Findings

### INTENT-PROV-0335 — v1.0.25.1은 최종 source에 대해 기계 검증을 다시 실행했다

초도 보고 이후 변경된 파일 때문에 stale했던 structure,
strict, doc–code 검사를 최종 상태에서 재실행했고,
forbidden gate도 추가했다. 이후 XeLaTeX로 세 장을 실제
build해 error와 undefined reference/citation이 0임을 보고한다.

판정:

- chronology를 반영하면 v1.0.25.1의 build·structure
  verification은 `PASS_REPORTED`.
- 이는 앞선 “TeX 미검증” 기록을 시간상 supersede한다.
- 다만 commit SHA와 environment lock을 Phase 065에서 다시
  확인한다.

### INTENT-PROV-0336 — skew 재모수화는 독립-site thermodynamic susceptibility를 보존하지 않는다

보고서는 `xi=sigma^alpha`가 독립-site 분산
`M theta(1-theta)` 형태를 보존하지 않으므로 기존 susceptibility
유도가 `alpha=1`에만 해당한다고 명시한다. 그런데 alpha를
평형 peak 확장으로 채택했다.

판정:

- `alpha != 1` 경로를 같은 microscopic equilibrium model의
  열역학 susceptibility로 부르는 것은 `FAIL_UNLESS_DERIVED`.
- empirical cumulative distribution 또는 heterogeneity
  convolution으로 쓸 수는 있지만 그 경우 free energy,
  composition coordinate, susceptibility와 구분한다.

### INTENT-PROV-0337 — empirical alpha가 entropy·reversible-heat 경로에 들어가면 열역학 오염 위험이 있다

`equilibrium`, finite-rate `dqdv`, `solve_U_oc`,
`entropy_coefficient`가 같은 alpha 경로를 사용한다고 보고한다.
수치적 일관성은 향상되지만, alpha에 물리적 free-energy
근거가 없으면 fitting shape가 entropy coefficient와 reversible
heat를 바꾼다.

판정:

- “같은 함수 사용”만으로 thermodynamic consistency가 되지
  않는다.
- entropy는 승인된 Gibbs/free-energy model의 temperature
  derivative에서만 파생한다.
- empirical observation kernel은 entropy·heat 경로에서
  분리하거나 명시적 latent heterogeneity model로 유도한다.

### INTENT-PROV-0338 — alpha는 비대칭뿐 아니라 위치와 폭도 바꾸는 강한 비식별 손잡이다

alpha는 apex를 `w ln(alpha)`만큼 옮기고, FWHM과 반폭비를
동시에 바꾼다. 문건도 alpha, lag, gallery, width의 4-way
degeneracy와 single-curve 비유일성을 인정한다.

판정:

- 이 정직한 식별성 경고는 `PRESERVE`.
- single-condition fitting에서 alpha를 material parameter로
  보고하지 않는다.
- multi-rate, multi-temperature, structural prior와
  parameter-profile test 없이 default로 열지 않는다.

### INTENT-PROV-0339 — `Omega=2RT`에서 “불연속 전환”이라는 표현은 재검토가 필요하다

보고서는 판정자가 임계값을 넘는 순간 Maxwell 공존평탄으로
불연속 전환한다고 쓴다. 대칭 regular solution에서는 임계점에
접근할수록 binodal 두 조성이 1/2로 모이고 gap이 0으로
닫혀야 한다. branch의 수학적 성격은 바뀌지만 상태량의
연속성·미분 특성은 별도 문제다.

판정:

- 현재 표현은 `PHYSICS_REVIEW_REQUIRED`.
- Phase 065에서 free energy convexification, binodal gap,
  susceptibility와 FWHM의 `Omega -> 2RT` 양쪽 극한을 재유도한다.
- 구현 branch가 물리적으로 연속이어야 할 값을 불연속으로
  만들지 수치 대조한다.

### INTENT-PROV-0340 — FWHM closed form은 유용하지만 homogeneous branch의 적용 범위를 명시해야 한다

`eq:gr2l-fwhm`의 closed form과 `lambda^(3/2)` 점근,
중심 높이 scale과 폭 scale의 분리는 선행 오류를 고친다.
그러나 이는 `Omega<2RT` homogeneous branch의 응답이며,
`Omega>2RT` equilibrium two-phase measure의 유한 폭을
설명하지 않는다.

판정:

- 독립 symbolic/numerical derivation 후 `PRESERVE_IF_VERIFIED`.
- phase coexistence, finite-size/disorder, kinetics,
  differentiation/instrument broadening을 한 width로 합치지 않는다.

### INTENT-PROV-0341 — forbidden grep은 회귀 보조이지 의미 정합성 증명이 아니다

금지 표현 4종과 self-test를 추가한 것은 누락된 gate를
보완했다. 그러나 문장 패턴 검사는 동의어, 수식 변화,
다른 절의 의미 충돌을 완전히 잡지 못한다.

판정:

- lightweight lint로 `PRESERVE`.
- 최종 conformance는 equation/claim ID와 model-status schema,
  symbolic limits, executable tests를 함께 사용한다.

### INTENT-PROV-0342 — doc–code 30/30은 구현 충실도를 보이지만 같은 오류의 복제를 배제하지 못한다

감사는 skew 위치·높이·면적, pad constants, SI values,
regsol 부재, FWHM 수치를 코드로 재현한다. 문건과 코드가 같은
수식·상수를 공유한다는 증거이지, 그 수식이 실제 재료와
열역학을 설명한다는 외부 검증은 아니다.

판정:

- conformance test로 `PRESERVE`.
- independent derivation, primary literature, synthetic
  limiting case, public-data out-of-sample test를 별도 gate로 둔다.

### INTENT-PROV-0343 — code map과 구현 각주는 최종 이론 문건에서 분리해야 한다

부록과 여러 본문 각주에 함수, key, cap, gate, bit-exact,
legacy constant가 들어갔다. 이것은 당시 추적성에는 기여했지만
사용자의 최종 문건 경계와 맞지 않는다.

판정:

- 내용은 conformance companion으로 이동해 재사용한다.
- 이론 본문에는 physical equation, assumptions, validity,
  evidence만 남긴다.

### INTENT-PROV-0344 — 배경과 gallery의 정직한 경고는 보존하되 causal claim은 낮춰야 한다

문건은 background가 전역 상수가 아니고, gallery·alpha가
phase count를 측정하지 않으며, multi-rate/XRD가 필요하다고
경고한다. 이는 좋은 방향이다. 반면 4 cell에서 같은 감소가
나왔다는 이유로 background를 material behavior로 확정하거나
hold-only feature를 특정 결정화 pair로 곧바로 귀속하는 부분은
외부 근거가 더 필요하다.

판정:

- scope/identifiability 경고는 `PRESERVE`.
- mechanism attribution은 `UNVERIFIED`로 낮춘다.

## Direction Recovered

1. 오류가 발견되면 계획 밖이라도 정량 유도와 self-correction을
   수행한다.
2. 최종 source 변경 뒤 모든 gate와 build를 다시 실행한다.
3. 물리적 비식별성을 문건에서 숨기지 않는다.
4. 앞으로는 empirical shape와 thermodynamic state function을
   분리한다.
5. theory-only manuscript와 implementation companion의 경계를
   다시 세운다.

## Coverage Status

- 이 batch의 1문건, 312행은 `READ`.
- 누적 coverage 반영 후 목표는 263문건, 52,669행이다.
- 전체 Phase 057 잔여 목표는 8문건, 5,126행이다.

## Next

Step 19.8N:
v1.0.25 handover와 index 2문건 308행을 전문 검독한다.
