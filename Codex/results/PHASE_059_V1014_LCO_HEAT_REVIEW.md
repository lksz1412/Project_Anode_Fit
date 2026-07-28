# Phase 059 v1.0.14 LCO·열·부호 독립 재유도

정본일: 2026-07-28

판정: `CONDITIONAL_P059_V1014_LCO_HEAT_ALGEBRA_PRESERVED_WITH_REFERENCE_DOS_GATE_CODE_AND_DOPING_BLOCKERS`

## 결론

전극 반응에 대해 `E=-DeltaG/F`, `dE/dT=DeltaS/F`와
`q_rev,gen=-I_lith*T*dE/dT`의 열역학 골격은 보존한다.
Sommerfeld 전자 엔트로피와 T-선형 엔트로피를 적분한 T² 중심
곡률도 각각의 가정 안에서는 대수적으로 맞다.

그러나 v1.0.14의 LCO 정량화와 구현 정합은 통과하지 못한다.
가장 큰 오류는 +0.83 mV/K의 intrinsic single-electrode
coefficient를 Li 기준 half-cell 전압 기울기로 사용한 것이다.
인용 원 논문이 보고한 isothermal Li|LCO half-cell 값은
-0.25 mV/K이므로 엔트로피 anchor의 부호가 뒤집힌다.

## 전위 기준과 열 부호

같은 Faraday 상수로 역산하면:

- manuscript +0.83 mV/K -> 80.083 J/(mol K)
- measured Li|LCO -0.25 mV/K -> -24.121 J/(mol K)
- inferred intrinsic difference (0.83-1.03) mV/K = -0.200 mV/K

따라서 문건의 `+80 J/(mol K)` 검산은 문건이 실제로 피팅하는
`V vs Li/Li+` 좌표의 검산이 아니다. 최종 문건은 intrinsic
전극전위와 reference를 포함한 half-cell voltage를 분리해야 한다.
열 부호도 charge/discharge 문자열이 아니라 삽입 반응 진행을 양으로
정한 `I_lith`에 연결해야 한다.

## 전자 엔트로피 gate

금속상에서 다음 Sommerfeld 선도항은 보존한다:

`S_e=(pi^2/3) k_B^2 T g(E_F)`.

하지만 Motohashi 원문은 susceptibility 차이를 Pauli 성분으로
가정해 CoO2에 대해 `13 electrons/eV`를 계산한다. 인용 구절은
직접 DOS 측정도 아니고 `per atom`이라고 쓰지도 않는다. 더구나
x=0 끝점을 x~0.85 MIT의 연속곡선 높이로 옮기는 근거가 없다.

현재 gate는 298.15 K에서 endpoint S_e=1.0988 k_B, 중심 깊이=-45.678 J/(mol K)를 만든다.
x=1에서도 g=0.6165 e/eV (4.74% residual)다.

중심 깊이는 `1/dx_MIT`에 비례하므로 -46이라는 수치는
`dx_MIT=0.05` 선택의 산출물이다. 원문들이 지지하는 것은
0.75<=x<=0.94의 전자전이·2상역이지 이 유일한 smooth gate가
아니다. 두-상 구간은 우선 두 상의 엔트로피, 공존 조성, lever
rule로 닫고 실험 분해능이 필요할 때만 observation convolution을
별도로 두어야 한다.

## 이론과 코드

문건은 전자 엔트로피의 T-선형성과 `a_e(T^2-T_ref^2)/(2F)`를 유도하지만 코드는 `x_center`와 298.15 K에서 전자항을 동결한다.
268.15/298.15/328.15 K code center second difference는 4.441e-16 V, 이론 gate가 요구하는 값은 -1.429e-03 V다.
즉 조성 의존 gate와 T² 곡률은 둘 다 미구현이다.

이론 전이 중심은 [3.9, 4.05, 4.17] V, code는 [3.93, 3.88, 4.049994] V다.
4.17 V 전이가 없고 4.15 V보다 높은 중심은 0개다. 도핑 변수,
LCO Omega, 실제 doped high-voltage 데이터 경로도 없다.

## 고전압 도핑

도핑을 `Omega_pure -> Omega_dop` 하나로 줄이는 것은 정본 후보가
될 수 없다. 2024년 Er/Mg LCO 1차 연구는 Mg의 Co-site 치환이
~4.2 V 상전이를 억제하면서도 >4.45 V 산소 안정성을 악화시킬
수 있고, Li-site Er은 산소 안정화를 담당함을 보인다. 즉 site,
전자구조, 산소 화학, 정합변형, 수송, 표면반응을 분리해야 한다.

## 문헌 정정

v1.0.14의 `ml2024`는 article/DOI를 105727로 적었지만 실제는
105726이다. 더 중요하게 그 논문은 MIT plateau를 포착하지
못한다고 명시하므로 logistic electronic gate의 검증 근거가 아니다.

## 직접 대조한 1차 문헌

- [Swiderska-Mocek et al. 2019](https://doi.org/10.1039/C8CP06638H)
- [Motohashi et al. 2009](https://doi.org/10.1103/PhysRevB.80.165114)
- [Ménétrier et al. 1999](https://doi.org/10.1039/A900016J)
- [Reynier et al. 2004](https://doi.org/10.1103/PhysRevB.70.174304)
- [Bernardi et al. 1985](https://doi.org/10.1149/1.2113792)
- [Shojaei et al. 2024](https://doi.org/10.1016/j.jmps.2024.105726)
- [Xia et al. 2024](https://doi.org/10.1002/smll.202311578)

## 판정표

| ID | topic | disposition | blocker/debt |
|---|---|---|---|
| LH-059-01 | electrode_thermodynamic_identity | PRESERVE_WITH_EXPLICIT_REACTION_COORDINATE | The reference electrode and reaction-current coordinate must be fixed before applying the identity. |
| LH-059-02 | lco_temperature_coefficient_anchor | REJECT_REFERENCE_CONFLATION_AND_SIGN | The manuscript applies it to U versus Li. The same primary paper reports -0.25 mV/K for the isothermal Li|LCO half-cell, reversing the entropy sign. |
| LH-059-03 | direction_and_current_labels | CORRECT_TO_SIGNED_REACTION_CURRENT | The heat API takes an unrelated signed I, while the same word discharge denotes opposite graphite chemical directions in the curve and heat prose. |
| LH-059-04 | reversible_heat_identity | PRESERVE_WITH_SIGN_AND_OMITTED_TERM_BOUNDARY | A half-electrode implementation must bind I to the written reaction, and the reduced equation must retain the mixing/phase-change omission boundary. |
| LH-059-05 | sommerfeld_functional_form | PRESERVE_ONLY_IN_VERIFIED_METALLIC_REGIME | It cannot be carried unchanged through a strongly composition-dependent first-order MIT without validating the Fermi-liquid and smooth-DOS assumptions. |
| LH-059-06 | dos_13_anchor | REJECT_TIER_A_PER_ATOM_PROMOTION | It is not stated as a direct 13 e/eV/atom measurement, and the x=0 endpoint does not validate a gate at x~0.85. |
| LH-059-07 | mit_logistic_gate | EMPIRICAL_ONLY | No cited primary source supplies the continuous g(E_F,x) or dx=0.05. The -46 J/(mol K) depth scales as 1/dx and is a model output, not a measured anchor. |
| LH-059-08 | mit_two_phase_thermodynamics | CORRECT_TO_COEXISTENCE_AND_LEVER_RULE | A homogeneous smooth DOS derivative across that interval replaces phase coexistence by an unstated observation regularization. |
| LH-059-09 | entropy_component_decomposition | PRESERVE_AS_CANDIDATE_WITH_COUPLING_RESIDUAL | The simple additive factorization neglects coupling and does not identify the proposed gate from measured entropy. |
| LH-059-10 | temperature_integration | PRESERVE_THEORY_REJECT_IMPLEMENTATION_MATCH | The code freezes both x and T at 298.15 K and produces zero T-squared curvature. |
| LH-059-11 | composition_mapping | FAIL_THEORY_CODE_CONFORMANCE | Production code evaluates the gate only at tr['x_center']; the electronic term is a constant offset across the peak. |
| LH-059-12 | lco_transition_map | REJECT_AS_MATERIAL_SPECIFIC_MAPPING | Code defaults produce about 3.93, 3.88, and 4.05 V, omit the 4.17 V transition, and are demonstration priors only. |
| LH-059-13 | doping_mechanism | REJECT_SCALAR_OMEGA_ONLY_GENERALIZATION | Primary evidence shows site-specific and competing oxygen, structure, and electronic effects. LCO code has neither doping variables nor Omega values. |
| LH-059-14 | doped_high_voltage_coverage | FAIL_SCOPE_ABSENT | It is out of scope; the code has no center above 4.15 V and no doped-LCO experimental profile or fit path. |
| LH-059-15 | ml2024_citation_support | CORRECT_CITATION_AND_REJECT_CLAIM_SUPPORT | The correct article/DOI is 105726, not 105727, and the paper explicitly does not capture the MIT plateau; it cannot validate the electronic gate. |
| LH-059-16 | graphite_electronic_entropy | CORRECT_ABSENCE_TO_QUANTIFIED_NEGLECT | The categorical 'absent in graphite' wording is not a thermodynamic identity and needs a dataset-specific error bound. |

## 다음 단계

Step 36.4에서 v1.0.14의 kinetics/barrier/current broadening
사슬을 독립 재유도하고, 저온×유한전류에서 peak suppression과
broadening을 낼 수 있는지 theory-code joint limit로 판정한다.
