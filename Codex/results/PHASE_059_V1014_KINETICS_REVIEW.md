# Phase 059 v1.0.14 kinetics·barrier·저온×유한전류 독립 재유도

정본일: 2026-07-28

판정: `CONDITIONAL_P059_V1014_KINETIC_SKELETON_PRESERVED_BUT_CONSTANT_CURRENT_LOCAL_BARRIER_AND_JOINT_LIMIT_FAIL`

## 결론

다음 최소 골격은 보존할 가치가 있다.

- `dξ/dt = k(ξ_eq-ξ)`의 1차 인과 완화
- 같은 단위계에서 `L_q=|I|/(Q_scale k)`
- 국소 선형화가 유효할 때 `L_V=|dV/dq|L_q`
- 연속계에서 유한 `L_V`가 peak를 낮추고 넓히며 진행방향으로 민다는 정성 결과

그러나 v1.0.14는 사용자의 출발 관측을 정본 수준으로 닫지 못했다.
저장 default에서는 current broadening이 꺼져 있고, 저온에서는 RT/F
평형폭만 줄어 peak가 오히려 높고 좁아진다. 실제 피팅이 된다는 사실은
경험적 `L_V` 또는 조정 파라미터가 곡선을 표현할 수 있음을 보일 뿐,
그 값이 전위·온도·전류에 따른 물리 장벽을 식별했다는 뜻은 아니다.

## 실험 관측과 기작의 지위

Fly–Chen은 고율에서 ICA peak가 낮아지고 넓어지며 이동·소실할 수
있음을 보였고, Gismero 등은 graphite/NMC532에서 온도 하강 또는
전류 증가가 선택된 peak를 flatten/broaden한다는 것을 직접 보였다.
따라서 사용자의 관측 목표는 문헌과 양립한다.

다만 둘 다 full-cell 결과다. 저항, 전해질·고체 확산, 전하전달,
전극 balancing, 상경계 운동, feature overlap이 함께 들어간다.
따라서 단일 지수 꼬리는 가능한 reduced mechanism이지 문헌이
유일하게 확정한 mechanism이 아니다.

## 정전류 좌표와 3,600배 단위 결함

시간초를 쓰는 Eyring rate와 결합하려면
`qdot = I[A]/Q[C]`여야 한다. 그런데 facade는 C-rate를 h^-1로
받아 `I=c_rate*Q_cell`로 만든 뒤 같은 숫자를 seconds-based
`kBT/h`와 결합한다.

- code numeric qdot: 0.1
- correct qdot: 2.7777778e-05 s^-1
- L_q ratio: 3600
- equivalent barrier bias at 298.15 K: 20.299 kJ/mol

즉 같은 broadening을 맞출 때 현재 hour/second 경로는 유효 장벽을
약 20.3 kJ/mol 낮게 보이게 한다. `L_V/w=1`의 예에서 code
수치계약은 77.643
kJ/mol, SI 일관 계약은
97.942 kJ/mol을 요구한다.

## 전위·조성 의존 장벽이 계산에서 사라지는 지점

default n=1이면 `min(4.357 n RT, 4 RT)`는 항상 `A=4RT`다.
이 지점의 logistic derivative는 정점의 7.065%로,
문건이 먼저 말한 5%도 아니다. 더 중요한 것은 A를 전이당 상수로
동결하므로 실제 code의 `d ln L_q/dV=0`이라는 점이다.
동일 식을 local A로 유지했다면 298.15 K, chi=0.5, A=4RT에서
`d ln L_q/dV=-18.761 V^-1`이다.

Bazant의 비평형 열역학이 요구하는 것은 local activity와 reaction
free energy다. `DeltaH_a_eff=DeltaH_a-chi*Omega`는 속도만
바꾸고 forward/reverse 비에는 regular-solution chemical
potential을 복원하지 않으므로 nonideal detailed balance closure가 아니다.

## 저장 default의 joint limit

대표 단일 전이에서 IR shift를 끄고 0.1C와 1C를 비교하면 세 온도
모두 shape 차이가 0이다. 모든 lag가 grid switch 아래이기 때문이다.

- 258.15 K / 298.15 K peak-height ratio: 1.154949
- 258.15 K / 298.15 K FWHM ratio: 0.865839
- low-T taller: True
- low-T narrower: True

따라서 shipped default는 사용자의 `저온 × 유한전류 -> peak
suppression/broadening`을 재현하지 않는다. 반대로 별도 mesoscopic
rate를 둔 차원 일관 causal existence probe는 같은 관측을 정성적으로
재현했다: low-T/room-T peak ratio=0.646834,
FWHM ratio=1.456489.
이는 1차 완화 골격의 가능성만 보존하며 현 파라미터를 검증하지 않는다.

## 수치·극한 결함

- direct L_V: max |I=0-I=1|=0.000e+00,
  max |I=0-equilibrium|=10.3291.
  즉 zero-current limit를 위반한다.
- two-grid-step handoff: kinetic area=0.770747,
  jump=22.925%.
- 큰 장벽/저온에서 `L_q=+inf`가 되면 resolver는 `L_V=0`으로
  바꾼다(검산 result=0.0 V).
  물리적 frozen limit를 equilibrium limit로 뒤집는 오류다.
- 비등온 입력은 mean T에서 lag를 한 번만 평가하고, voltage sorting은
  되돌림·휴지·비단조 protocol의 chronology를 잃는다.

## v1.0.10에서 실제로 고쳐졌는가

`func_L_q`, `_causal_lowpass`, `func_dH_a_eff`,
`_resolve_lag_length`의 docstring 제외 executable AST는
v1.0.10과 v1.0.14가 모두 동일하다. v1.0.14의 scalar-input
guard와 설명 확장은 필요하지만, unit·frozen affinity·Omega
shortcut·direct lag·grid switch의 핵심 blocker를 고치지 않았다.

## 권고하는 정본 구조

문건은 코드 이름 없이 다음 물리 순서로 다시 세워야 한다.

1. 반응 방향과 signed current를 고정한다.
2. host별 하나의 자유에너지에서 equilibrium chemical potential을 유도한다.
3. local composition, phase fraction, stress, T, overpotential에서 affinity를 계산한다.
4. 하나의 transition-state free energy에서 forward/reverse rate를 만들고 detailed balance를 검산한다.
5. 전하전달·확산·핵생성/상경계·porous transport의 축약 순서를 명시한다.
6. imposed current와 모든 reaction current의 합을 보존하며 terminal voltage를 푼다.
7. 마지막에만 instrument/processing/heterogeneity observation operator를 적용한다.

코드는 이 이론이 동결된 뒤 SI 내부단위, time/charge-domain state
integration, local rate, current conservation, continuous small-lag
limit, k->0 frozen limit를 그대로 구현해야 한다.

## 직접 대조한 1차 문헌

- [The Activated Complex in Chemical Reactions](https://doi.org/10.1063/1.1749604)
- [Theory of Chemical Kinetics and Charge Transfer based on Nonequilibrium Thermodynamics](https://doi.org/10.1021/ar300145c)
- [Rate dependency of incremental capacity analysis (dQ/dV) as a diagnostic tool for lithium-ion batteries](https://doi.org/10.1016/j.est.2020.101329)
- [The Influence of Testing Conditions on State of Health Estimations of Electric Vehicle Lithium-Ion Batteries Using an Incremental Capacity Analysis](https://doi.org/10.3390/batteries9120568)
- [Thermodynamic and kinetic properties of the Li-graphite system from first-principles calculations](https://doi.org/10.1103/PhysRevB.82.125416)
- [Lithium Diffusion in Graphitic Carbon](https://doi.org/10.1021/jz100188d)
- [Modeling of Galvanostatic Charge and Discharge of the Lithium/Polymer/Insertion Cell](https://doi.org/10.1149/1.2221597)

## 판정표

| ID | topic | disposition | reason |
|---|---|---|---|
| KIN-059-01 | experimental_target | PRESERVE_TARGET_NOT_UNIQUE_MECHANISM | Primary full-cell data support lower, broader, shifted or vanishing peaks at higher rate and lower temperature, but do not identify a unique single-exponential electrode tail. |
| KIN-059-02 | linear_relaxation_limit | PRESERVE_AS_REDUCED_CAUSAL_LIMIT | dξ/dt=k(ξeq-ξ) has the correct causal, area-preserving continuum limit when the equilibrium target and k are well-defined. |
| KIN-059-03 | constant_current_unit_contract | REJECT_FACTOR_3600_DUAL_UNIT_API | The facade accepts C-rate in h^-1 and Ah-like capacity while func_L_q combines I/Q numerically with a seconds-based Eyring prefactor. Lq is 3600 times too large in that path. |
| KIN-059-04 | galvanostatic_forward_closure | REJECT_AS_CLOSED_CONSTANT_CURRENT_MODEL | The code prescribes a voltage grid and filters equilibrium occupancy on it; it does not solve current balance, transition-current partition, transport, and terminal voltage under imposed current. |
| KIN-059-05 | local_affinity | REJECT_FROZEN_CUT_AFFINITY | Default n=1 always selects A=4RT, so implemented d ln Lq/dV=0. The user's potential-dependent barrier hypothesis is removed from the computation. |
| KIN-059-06 | nonideal_detailed_balance | REJECT_OMEGA_BARRIER_SHORTCUT | Subtracting χΩ from a common activation enthalpy changes the speed but leaves r+/r-=exp(Aideal/RT). It does not recover the regular-solution local chemical affinity. |
| KIN-059-07 | migration_barrier_anchor | REJECT_AS_MACRO_RELAXATION_ENTHALPY | Persson studies support bulk Li migration and diffusion physics, not the direct assignment of those barriers to electrode-scale phase-fraction relaxation. |
| KIN-059-08 | eyring_prefactor | REQUIRE_MESOSCOPIC_COARSE_GRAINING | kBT/h with a hop barrier omits active area, site density, nucleation population, phase-boundary mobility, particle geometry, diffusion, and porous-electrode transport. |
| KIN-059-09 | default_current_broadening | FAIL_DORMANT_DEFAULT_PATH | All four default lag lengths remain below the grid switch for the audited rate/temperature range, so 0.1C and 1C single-transition shapes are identical when IR shift is removed. |
| KIN-059-10 | low_temperature_finite_current_joint_limit | FAIL_USER_TARGET_ON_SHIPPED_DEFAULT | With the lag branch dormant, lower temperature only narrows the RT/F equilibrium width and raises the peak, opposite the target finite-current trend. |
| KIN-059-11 | direct_lag_override | EMPIRICAL_ONLY_REQUIRE_PROTOCOL_SCALING | A direct L_V produces the same nonequilibrium curve at I=0 and I>0. It may be a nuisance kernel only if a protocol law forces L_V to zero with current and constrains T. |
| KIN-059-12 | small_lag_numerics | REJECT_DISCONTINUOUS_GRID_HANDOFF | At the two-grid-step threshold the kinetic branch carries only 0.7707 of an impulse while the equilibrium branch carries one, causing a 22.9% fit-objective jump. |
| KIN-059-13 | low_temperature_overflow | FAIL_NONFINITE_PHYSICS_REVERSAL | An infinite Lq from a vanishing rate is converted to L_V=0, which returns the equilibrium peak instead of a frozen transition. |
| KIN-059-14 | nonisothermal_rate | REQUIRE_LOCAL_T_STATE_RATE | The lag is evaluated once at mean T and mean n; Arrhenius kinetics along a varying T(V) path is not implemented. |
| KIN-059-15 | chronology | REQUIRE_MONOTONE_SEGMENT_OR_TIME_SOLVER | Sorting/interpolation by voltage discards revisits and protocol chronology. Hysteresis and memory require an explicit monotone-segment contract or time integration. |
| KIN-059-16 | ohmic_polarization | PRESERVE_AS_SHIFT_NOT_BROADENING | For constant I and R, Vn=Vapp-sigma*IR shifts a peak but cannot change its width or height. |
| KIN-059-17 | parameter_identifiability | REQUIRE_MULTI_T_MULTI_RATE_RELAXATION_DATA | One curve cannot separate equilibrium width, heterogeneity, charge transfer, diffusion, phase motion, IR, observation smoothing, activation enthalpy, and activation entropy. |
| KIN-059-18 | v1010_to_v1014_lineage | BLOCKERS_CARRIED_FORWARD | The executable AST of func_L_q, _causal_lowpass, func_dH_a_eff, and _resolve_lag_length is unchanged from v1.0.10 to v1.0.14. |
| KIN-059-19 | mechanism_existence | PRESERVE_QUALITATIVE_EXISTENCE_PROOF | A dimensionally consistent causal reduced model with a separately calibrated mesoscopic Arrhenius rate can qualitatively reproduce low-T peak suppression/broadening. |
| KIN-059-20 | repair_architecture | REPLACE_WITH_SIGNED_TIME_DOMAIN_STATE_MODEL | Use one free-energy state definition, local affinity and transition-state law, current conservation, material/host states, transport, and a separate observation operator. |

## 다음 단계

Step 36.5에서 v1.0.14의 다수 review round가 선언한 수렴·완주·
물리 오류 0 주장을 이번 독립 blocker와 대조해 v1.0.14 최종
권위 판정을 닫는다.
