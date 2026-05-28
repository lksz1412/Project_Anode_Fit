# Phase 017 — Equation-Origin Logic Audit

## Summary

The first-principles derivation was audited before manuscript writing. The audit checks equation origin, units, signs, residual-tail algebra, and scope drift.

Gate result: `PASS_EQUATION_ORIGIN_AUDIT`

## No-Copy Audit

| Check | Result |
|---|---|
| Old TeX line references used as formula support | PASS, none |
| Invalidated manuscript used as base | PASS, no |
| Equation-origin table present | PASS |
| Any equation classified as copied old TeX | PASS, none |

## Convention Audit

| Convention | Result |
|---|---|
| Electrode potential scope fixed before derivation | PASS |
| Full-cell voltage separated from negative-electrode potential | PASS |
| Scan coordinate direction fixed | PASS |
| ICA/DVA definitions fixed by calculus | PASS |
| Tail direction fixed | PASS |
| Assisting potential sign fixed | PASS |
| Units stated for work, barrier, rate, and tail length | PASS |

## Unit Audit

| Quantity | Unit check | Result |
|---|---|---|
| `v_Q=dQ/dt` | charge/time | PASS |
| `L_Q=v_Q/k` | `(charge/time)/(1/time)=charge` | PASS |
| `F psi` | `(C/mol)(J/C)=J/mol` | PASS |
| `G_0^\ddagger`, `B`, `RT` | all `J/mol` | PASS |
| `B/(RT)` | dimensionless | PASS |
| `C_b dphi` | `(charge/voltage)(voltage)=charge` | PASS |
| `Q_p dtheta` | `charge * dimensionless=charge` | PASS |

## Sign Audit

| Check | Result |
|---|---|
| `psi>0` defined as assisting forward transformation | PASS |
| assisting work lowers raw barrier | PASS |
| `partial B/partial psi=-alpha z_eff F` while barrier active | PASS |
| `partial ln L_Q/partial psi<=0` | PASS |
| low-temperature tail claim conditional on reduced net rate | PASS |
| high-temperature tail claim conditional on increased net rate | PASS |

## Residual Tail Algebra Audit

| Step | Result |
|---|---|
| `r=theta_e-theta` | PASS |
| `dtheta/dQ=(k/v_Q)r` | PASS |
| `dr/dQ=dtheta_e/dQ-(k/v_Q)r` | PASS |
| post-peak `dtheta_e/dQ approx 0` | PASS |
| `dr/dQ=-(k/v_Q)r` | PASS |
| `r=r_a exp[-(Q-Q_a)/L_Q]` | PASS |
| `L_Q=v_Q/k` | PASS |

## ICA Mapping Audit

| Step | Result |
|---|---|
| incremental storage `dQ=C_b dphi+Q_p dtheta` is declared as local conservation model | PASS |
| slope equation `1=C_b dphi/dQ+Q_p dtheta/dQ` follows | PASS |
| `dphi/dQ=(1-Q_p dtheta/dQ)/C_b` follows | PASS |
| `dQ/dphi=C_b/(1-Q_p dtheta/dQ)` follows | PASS |
| tail in `dtheta/dQ` transfers to ICA denominator | PASS |
| peak-area argument not used | PASS |

## Scope Audit

| Drift risk | Result |
|---|---|
| fitting code | PASS, absent |
| numerical solver | PASS, absent |
| peak-area-centered derivation | PASS, absent |
| Chapter 2 reversible heat derivation | PASS, roadmap only |
| Chapter 3 electrochemical kinetics | PASS, roadmap only |
| Chapter 4 heat-generation extension | PASS, roadmap only |
| Chapter 5 hysteresis | PASS, roadmap only |

## Gate

Gate: `PASS_EQUATION_ORIGIN_AUDIT`

Status: PASS

Reason:

- every equation has an acceptable first-principles or explicit model-assumption origin;
- no equation is classified as copied from old TeX;
- units, signs, residual-tail algebra, and ICA mapping pass;
- convention section requirement is ready for final manuscript.

## Confirmed Non-Changes

- Invalidated manuscript was not edited in this phase.
- Original source files were not modified.
- Claude folder was not modified.
