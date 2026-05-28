# Phase 004 — Chapter 1 Derivation Ledger

## Summary

Gate result: `PASS_NO_LEAP_DERIVATION`

The derivation is rebuilt without archived equations. Every core relation is classified by origin, dependency, validity domain, and failure mode.

## Equation Ledger

| Eq ID | Equation / Relation | Origin | Depends On | Unit / Sign Check | Validity Domain | Failure Mode |
|---|---|---|---|---|---|---|
| E1 | `I_ICA=dQ/d\varphi`, `DVA=d\varphi/dQ` | `DEF/CALC` | A1,A2 | capacity per voltage; voltage per capacity | chosen analysis axis | full-cell axis not transformed |
| E2 | `\theta_e=\theta_e(\varphi,T)` | `DEF/THERMO` | A3 | dimensionless | local transition target | branch metastability |
| E3 | `r=\theta_e-\theta` | `DEF` | E2,A4 | dimensionless; positive means lag | chosen branch | sign reversal if convention changes |
| E4 | `d\theta/dt=k r` | `KIN-RED` | A5 | `s^-1` times dimensionless | local linear relaxation | multiple modes/nucleation |
| E5 | `d\theta/dQ=(k/v_Q)r` | `CALC` | E4,A1 | `1/capacity` | `v_Q>0` | rest/reversal |
| E6 | `dr/dQ+dtheta/dQ=dtheta_e/dQ` rearranged to `dr/dQ+(k/v_Q)r=dtheta_e/dQ` | `CALC` | E3,E5 | `1/capacity` | differentiable target | discontinuous jump |
| E7 | `dtheta_e/dQ=theta_e,varphi dvarphi/dQ+theta_e,T dT/dQ` | `CALC` | E2 | `1/capacity` | differentiable `theta_e` | noisy/unresolved data |
| E8 | General residual solution with exponential kernel | `CALC` | E6 | dimensionless | known `k/v_Q` | nonlocal memory |
| E9 | Post-peak local tail `r~exp[-(Q-Qa)/L_Q]`, `L_Q=v_Q/k` | `LOCAL/CALC` | E6,E8 | capacity | forcing small, `k/v_Q` local constant | forcing remains large |
| E10 | `Delta G0^ddagger(T)=Delta H^ddagger(T)-T Delta S^ddagger(T)` | `THERMO/KIN-TST` | A6 | J/mol | local temperature window | non-TST kinetics |
| E11 | `psi=s_psi[varphi-varphi_star(T)]` | `DEF` | A2,A7 | V | selected forward direction | wrong branch sign |
| E12 | `W_psi=Lambda_psi F psi` | `THERMO/REDUCED_MODEL` | A7 | J/mol | effective active-coordinate coupling | coupling not identifiable |
| E13 | `Delta G_act^ddagger=Delta G0^ddagger-Lambda_psi F psi`, with `Delta G_act^ddagger>0` | `KIN-RED/LOCAL` | E10-E12 | J/mol | active-barrier regime | barrier exhausted |
| E14 | `k=k0(T) exp[-Delta G_act^ddagger/(RT)]` | `KIN-TST/KIN-RED` | E13 | `s^-1` | active-barrier regime | transport/site/current limit |
| E15 | `L_Q=(v_Q/k0) exp[Delta G_act^ddagger/(RT)]` | `CALC` | E9,E14 | capacity | local constant rate | varying rate |
| E16 | `partial ln L_Q/partial psi= -Lambda_psi F/(RT)` under fixed `v_Q,k0,T` | `CALC/LOCAL` | E13,E15 | `1/V` | active-barrier regime | `k0` or mapping depends on `psi` |
| E17 | `partial ln L_Q/partial T = -partial_T ln k0 + (RT)^{-1} partial_T Delta G_act - Delta G_act/(RT^2)` | `CALC` | E15 | `1/K` | fixed `v_Q,psi` | nonisothermal coupling |
| E18 | `dQ=C_b dvarphi+Q_p dtheta` | `CONS/LOCAL` | storage decomposition | capacity | local storage balance | extra state variables |
| E19 | `dvarphi/dQ=(1-Q_p dtheta/dQ)/C_b` | `CALC` | E18 | V/capacity | denominator finite | singular peak center |
| E20 | `dQ/dvarphi=C_b/(1-Q_p dtheta/dQ)` | `CALC` | E19 | capacity/V | denominator finite | sign/singularity |
| E21 | `L_varphi approx |dvarphi/dQ|_Qa L_Q` | `LOCAL/CALC` | E9,E19 | voltage | local smooth mapping | strong nonlinear mapping |

## No-Leap Notes

1. The residual ODE follows directly from differentiating `r=\theta_e-\theta` and substituting the reduced relaxation law.
2. The post-peak exponential is not assumed; it is the local homogeneous limit of the forced residual ODE.
3. The active-barrier rate is not global. It is valid only while `Delta G_act^ddagger>0`.
4. No equation repairs a negative barrier by truncation.
5. The ICA expression is an implicit storage balance, not a fitted peak function.

## Validation

| Check | Result |
|---|---|
| Every core equation has origin class | PASS |
| No forbidden origin class | PASS |
| No cap/step barrier equation | PASS |
| Residual-to-tail derivation complete | PASS |
| Voltage-axis mapping present | PASS |
| Trend claims conditional | PASS |

## Gate

`PASS_NO_LEAP_DERIVATION`

## Next

Proceed to Phase 005 audit.

