# Phase 005 — Double-Counting And Regime Audit

## Summary

Gate result: `PASS_REGIME_AUDIT`

The derivation was attacked for double counting, sign ambiguity, regime misuse, and hidden fitting convenience.

## Reviewer Objection Table

| Attack ID | Role | Objection | Resolution | Status |
|---|---|---|---|---|
| A-01 | Thermodynamics | `theta_e(varphi,T)` and `k(T,psi)` both use potential. Is that double counting? | Add two-state consistency: `theta_e` is stationary ratio, `k` is mobility `r_++r_-`. Same potential may affect both if local detailed-balance consistency is stated. | RESOLVED |
| A-02 | Kinetics | Active barrier can become zero. Why not clip it? | Do not clip. State that the active-barrier approximation exits its domain; physical bottleneck controls later. | RESOLVED |
| A-03 | Electrochemistry | Does `F psi` have correct units and sign? | Define `psi` signed to assist forward transition; `F psi` is J/mol; `Lambda_psi>=0`. | RESOLVED |
| A-04 | ICA/DVA | `L_Q` is not voltage-axis length. | Add `L_varphi approx |dvarphi/dQ| L_Q` and local mapping caveat. | RESOLVED |
| A-05 | Modeler | First-order relaxation might be too simple. | Label as local reduced linearized relaxation; list nucleation, phase-boundary, diffusion as failure modes. | RESOLVED |
| A-06 | Graphite specialist | Equilibrium heterogeneity can also make tails. | State Chapter 1 derives kinetic residual component, not every possible tail. | RESOLVED |
| A-07 | Temperature reviewer | High temperature does not always shorten tail. | Derive conditional derivative and state net-rate condition. | RESOLVED |
| A-08 | Numerical skeptic | Hidden bounded transform? | Final equations contain no `max`, clipping, softplus, hard rate bound, or step-like barrier law. | RESOLVED |

## Regime Separation

| Regime | Allowed Statement | Forbidden Statement |
|---|---|---|
| Active-barrier | `Delta G_act^ddagger>0`; activated expression controls `k` | valid for all `psi` |
| Barrier-exhausted | activation barrier no longer controls rate | barrier is clipped to zero |
| Bottleneck-limited | later physical mechanisms may limit observed rate | arbitrary numerical upper bound is physics |

## Validation

| Check | Result |
|---|---|
| No P1/P2 unresolved objection | PASS |
| Double-counting objection answered | PASS |
| No clipped barrier logic | PASS |
| Trend claims conditional | PASS |
| Assumptions support/labeled | PASS |

## Gate

`PASS_REGIME_AUDIT`

## Next

Proceed to Phase 006 manuscript.

