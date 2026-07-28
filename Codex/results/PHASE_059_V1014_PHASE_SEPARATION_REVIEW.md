# Phase 059 v1.0.14 상분리 부록 독립 재유도

정본일: 2026-07-28

판정: `CONDITIONAL_P059_V1014_PHASE_SEPARATION_CORE_CORRECT_WITH_DIMENSIONAL_BOUNDARY_AND_ELASTICITY_BLOCKERS`

## 결론

정규용액의 homogeneous thermodynamics는 대체로 맞다. 자유에너지,
공통접선, binodal, chemical spinodal, Maxwell 등면적, 구형 CNT
식과 Cahn–Hilliard 성장 band의 대수는 독립 재유도된다.

그러나 Cahn–Hilliard 절은 현재 형태로 차원이 닫히지 않는다.
앞에서 \(f\)를 J/mol로 정의한 뒤 site density 또는 molar-volume
환산 없이 \(\int f\,dV\)를 쓰고, \(\kappa\)와 \(M\)의 단위를
정의하지 않았다. 경계조건도 없어 질량보존과 자유에너지 감소를
증명할 수 없다. 또한 고체 삽입전극에서 중요한 coherency elasticity
가 chemical spinodal을 바꿀 수 있다는 적용 경계를 누락했다.

## 정규용액 수치 재유도

\(\Omega/(RT)=3\)에서 독립 계산은 다음을 준다.

- binodal:
  \(\xi_b^-=0.0707202\),
  \(\xi_b^+=0.9292798\)
- spinodal:
  \(\xi_s^-=0.2113249\),
  \(\xi_s^+=0.7886751\)
- \(f(\xi_b)/(RT)=-0.0583413\)
- Maxwell equal-area residual:
  0.000e+00
- common-tangent chord slope:
  -6.466e-17

따라서 문건의 0.0707/0.9293, 0.2113/0.7887, \(-0.0583\)
수치는 재현된다.

## Cahn–Hilliard 식의 대수와 차원

문건은 gradient energy를 \(\kappa|\nabla\xi|^2\)로 썼으므로
변분의 \(-2\kappa\nabla^2\xi\)와 성장률
\[
R(k)=-Mk^2[f''+2\kappa k^2]
\]
은 같은 convention 안에서는 일관된다. 독립 probe에서도
\(k_c=1.4142136\),
\(k_m=1.0000000=k_c/\sqrt2\),
\(R(k_c)=-8.882e-16\)가 재현된다.

하지만 이 대수는 단위를 복구한 뒤에만 물리식이 된다.
[Cahn–Hilliard 1958 원 논문](https://doi.org/10.1063/1.1744102)은
per-particle homogeneous free energy와 gradient term 앞에
number-density factor를 둔다. v1.0.14는 molar \(f\)를 그대로
volume integral에 넣어 그 연결을 빠뜨렸다.

최종 문건의 권장 계약은
\[
\mathcal G[\xi]=\int c_s\left[f_m(\xi)+
\frac{K}{2}|\nabla\xi|^2\right]d^3r,\qquad
\mu=f_m'(\xi)-K\nabla^2\xi
\]
이다. 여기서 \(c_s\)[mol m\(^{-3}\)],
\(f_m\)[J mol\(^{-1}\)], \(K\)[J m\(^2\) mol\(^{-1}\)]다.
몰 flux \(\mathbf N_B=-\mathcal L\nabla\mu\)와
\(c_s\partial_t\xi=-\nabla\cdot\mathbf N_B\)를 쓰면
\(M=\mathcal L/c_s\)[mol m\(^2\) J\(^{-1}\) s\(^{-1}\)]이고,
\[
R(k)=-Mk^2[f_m''+Kk^2].
\]
문건 convention으로 돌아가려면 volumetric \(\kappa\)에 대해
\(K=2\kappa/c_s\)를 명시해야 한다.

## 빠진 경계조건과 고체 적용 경계

source에서 explicit \(\kappa\) unit, mobility unit, no-flux
boundary, composition natural boundary count는 각각
0,
0,
0,
0이다.

폐계라면
\(\mathbf n\cdot\nabla\mu=0\)와
\(\mathbf n\cdot\nabla\xi=0\), 또는 periodic boundary가 필요하다.
그때만
\[
\frac{d}{dt}\int\xi\,dV=0,\qquad
\frac{d\mathcal G}{dt}=-\int\mathcal L|\nabla\mu|^2dV\le0
\]
를 닫을 수 있다.

[Cahn 1961 원 논문](https://doi.org/10.1016/0001-6160(61)90182-1)은
고체에서 조성에 따른 molar-volume 변화와 elastic energy가
metastability limit를 이동시킬 수 있음을 명시한다. 따라서
v1.0.14의 \(f''=0\)은 일반 LIB 고체의 spinodal이 아니라
`stress-free chemical spinodal`로 한정해야 한다.

## 판정표

| ID | topic | disposition | blocker/debt |
|---|---|---|---|
| PS-059-01 | regular_solution | PRESERVE_WITH_UNIT_WORDING_CORRECTION | The prose conflates per-site and per-mole quantities; k_B and R versions must be separated explicitly. |
| PS-059-02 | chemical_spinodal_scope | CORRECT_MAJOR_SCOPE_BOUNDARY | Cahn 1961 explicitly shows coherency elasticity and composition-dependent molar volume can shift the instability criterion; the LIB-solid appendix omits that boundary. |
| PS-059-03 | gradient_functional_units | FAIL_DIMENSIONAL_CLOSURE | A site density/molar-volume conversion and an explicit gradient-coefficient convention are required. |
| PS-059-04 | factor_two_convention | PRESERVE_AFTER_DEFINITION | The convention and units are not defined, making comparison with the common (K/2)|grad xi|^2 form ambiguous. |
| PS-059-05 | linear_stability | PRESERVE_AFTER_DIMENSIONAL_REPAIR | As printed, k_c is dimensionally undefined because f'' is molar and kappa has no declared compatible unit. |
| PS-059-06 | mobility | FAIL_UNIT_AND_STATE_CLOSURE | Mobility units, flux definition, site density, possible composition/temperature dependence, and relation to diffusivity are absent. |
| PS-059-07 | boundary_conditions | FAIL_MISSING | Without boundary conditions the claimed conserved dynamics does not close mass conservation or free-energy dissipation. |
| PS-059-08 | classical_nucleation | PRESERVE_WITH_ASSUMPTION_BOUNDARY | Isotropic sharp-interface gamma, negligible coherency strain, bulk reservoir, and homogeneous nucleation assumptions must be stated before use for electrode particles. |
| PS-059-09 | coordinate_and_symbols | CORRECT_TERMINOLOGY_AND_COLLISION | f(xi)=f(1-xi) is mirror symmetry about 1/2, not evenness about zero, and dV for volume collides with V for voltage. |
| PS-059-10 | final_authority | PRESERVE_DERIVATION_ASSET_NOT_CANON | Dimensional, boundary-condition, mobility, elasticity, and solid-electrode scope blockers prevent canonical promotion. |

## 다음 단계

Step 36.3에서 v1.0.14의 LCO electronic term, graphite/LCO sign
map, heat convention과 high-voltage/doping scope를 독립
재유도·검산한다.
