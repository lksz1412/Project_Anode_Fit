# Phase 003 — Assumption Contract Result

## Summary

Gate result: `PASS_ASSUMPTION_CONTRACT`

This contract fixes which assumptions may enter the clean-slate Chapter 1 manuscript and how they must be worded.

## Step Range

Steps 56-85.

## Assumption Contract

| ID | Assumption | Evidence Status | Allowed Wording | Forbidden Wording | Failure Mode |
|---|---|---|---|---|---|
| A1 | `Q` is a monotone branch coordinate with `v_Q=dQ/dt>0` | `DEF` | "analysis branch coordinate" | "universal SOC coordinate for every branch" | branch reversal or hysteresis |
| A2 | `\varphi` is a negative-electrode analysis potential chosen in the forward direction | `DEF` | "signed analysis potential" | "full-cell voltage" | full-cell mixing |
| A3 | `\theta_e(\varphi,T)` is an equilibrium or quasi-equilibrium target | `THERMO/REDUCED_MODEL` | "target fraction" | "measured dynamic fraction" | nonequilibrium branch target |
| A4 | Actual fraction `\theta(Q)` may lag behind `\theta_e` | `KIN-RED` | "reduced state variable" | "microscopic phase fraction always exactly known" | multiple modes, memory |
| A5 | Local first-order relaxation is a linearized reduced model | `KIN-RED` | "local coarse-grained relaxation" | "exact graphite microscopic law" | nucleation/growth/diffusion dominate |
| A6 | Active-barrier rate is valid only when `\Delta G^\ddagger_act>0` | `KIN-TST/LOCAL` | "active-barrier regime" | "valid over all potentials" | barrier-exhausted regime |
| A7 | Present potential enters through work scale `F\psi` and effective coupling `\Lambda_\psi` | `REDUCED_MODEL` | "effective coupling to activated coordinate" | "all electrical work necessarily lowers the barrier" | wrong transition coordinate |
| A8 | Barrier exhaustion is a regime change | `LIMIT` | "activation step no longer controls the rate" | "clip the barrier to zero" | physical bottleneck needed |
| A9 | `L_Q=v_Q/k` is local capacity-axis tail length | `CALC/LOCAL` | "local constant-rate approximation" | "global voltage-axis tail length" | strongly varying mapping/rate |
| A10 | Voltage-axis tail requires local mapping | `CALC/LOCAL` | "`L_\varphi` inherits `L_Q` through local DVA" | "same length without conversion" | nonlinear voltage mapping |
| A11 | ICA denominator must not cross singularity in tail region | `CALC/LOCAL` | "valid away from singular denominator" | "always finite" | peak-center divergence |
| A12 | Equilibrium heterogeneity may also shape the peak | `LITERATURE/CAUTION` | "kinetic residual-tail component" | "all tails are kinetic" | heterogeneity-dominated data |

## Locked Wording Rules

- Use "active-barrier regime" before writing any activated rate expression.
- Use "reduced mobility" or "coarse-grained relaxation" for `k`.
- State all low-temperature/high-temperature tail claims as conditional on `k` decreasing/increasing.
- State present-potential shortening only at fixed `v_Q`, fixed prefactor, and active-barrier regime.
- Do not use a formula that repairs a negative barrier by mathematical truncation.

## Validation

| Check | Result |
|---|---|
| Variables and units defined before use | PASS |
| Unsupported assumptions removed or downgraded | PASS |
| Barrier handling not a cap | PASS |
| Double-counting risk flagged | PASS |
| Chapter 1 scope preserved | PASS |

## Gate

`PASS_ASSUMPTION_CONTRACT`

## Next

Proceed to Phase 004 derivation ledger.

