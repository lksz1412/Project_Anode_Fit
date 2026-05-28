# Phase 005 — Tail Scope Contract

## Summary

This phase locks the corrected Chapter 1 problem definition before any derivation is written. The manuscript target is not a fitting routine, not a solver, not a peak-area model, and not a repair of the previous draft. The target is a logically complete theoretical derivation of graphite ICA peak-tail behavior caused by finite phase-transition kinetics under temperature and present-electrode-potential-dependent effective barrier lowering.

Gate result: `PASS_SCOPE_LOCK`

## Step Range

Planned steps: 59-72

Actual steps completed: 59-72

## Fixed Observation Statement

The phenomenon to explain is:

1. In graphite LIB ICA analysis, a phase-transition peak has a trailing side whose shape changes with temperature and present electrode potential state.
2. Low temperature shows a longer tail.
3. High temperature shows a relatively shorter tail.
4. A simple equilibrium Gaussian-like or logistic broadening can locate a transition and give a finite width, but by itself it does not explain a finite-rate asymmetric tail that stretches after the equilibrium transition has moved ahead.
5. The working hypothesis is that, in addition to the intrinsic thermal activation barrier, the present electrode potential supplies a driving affinity that lowers the effective barrier for the forward phase transition.
6. The Chapter 1 deliverable is a derivation that later fitting can use, not a fitting implementation.

## Central Hypothesis

For transition `j`, the intrinsic thermal activation free energy is:

```tex
\Delta G_{a,j}(T)=\Delta H_{a,j}-T\Delta S_{a,j}.
```

The present-potential driving affinity is:

```tex
\mathcal A_j=s_{\phi,j}F\left[V_{n,\drive}-U_j(T)\right].
```

The effective barrier is:

```tex
\Delta G_{\eff,j}=\Delta G_{a,j}(T)-\chi_j\mathcal A_j.
```

After positive-barrier handling:

```tex
k_j=\nu_j(T)\exp\left[-\frac{\Delta G_{\eff,j}^{+}}{RT}\right].
```

The peak tail comes from the finite relaxation of the actual progress `xi_j` toward the equilibrium progress `xi_{j,eq}`:

```tex
\frac{d\xi_j}{dq}
=\frac{Q_{\cell}}{|I|}k_j
\left[\xi_{j,\mathrm{eq}}(V_n,T)-\xi_j\right].
```

This is the minimum logic chain that must survive all later audits.

## Required Reader Level

The manuscript must be readable by a university undergraduate who knows basic calculus, thermodynamics, and electrochemical notation but has not already accepted this model.

Therefore the manuscript must explicitly show:

- what each variable means before it is used;
- why `q` is a useful coordinate under constant current;
- why `V_n` is not freely chosen but solved from charge balance;
- why `V_{n,\app}` and `V_{n,\drive}` cannot be conflated without restrictions;
- why `F * voltage` has units compatible with energy per mole;
- why lowering a positive activation barrier increases `k_j`;
- how `dxi/dt` becomes `dxi/dq`;
- how the residual lag gives an exponential tail scale under local assumptions;
- how `dxi/dq` appears in ICA/DVA through charge-balance differentiation.

## Core Scope

| Item | Status | Reason |
|---|---|---|
| Charge coordinate `q` | included | needed to connect time relaxation to ICA coordinate |
| Charge balance and internal `V_n` | included | closes the feedback loop without assuming an external `V_n(q)` |
| Equilibrium progress `xi_eq(V_n,T)` | included | defines the equilibrium target of phase transition |
| Voltage role separation | included | prevents double-counting and circular voltage definitions |
| Affinity `A_j` | included | expresses present-potential assistance |
| Intrinsic thermal barrier | included | explains temperature dependence baseline |
| Effective barrier lowering | included | main hypothesis requested by user |
| Rate constant `k_j` | included | connects barrier to kinetic lag |
| Phase-progress ODE in `t` and `q` | included | direct source of tail behavior |
| Tail length derivation | included | required to explain long/short tail |
| ICA/DVA mapping | included | connects theoretical tail to observable dQ/dV and dV/dQ |

## Non-Goals Locked For Chapter 1

| Item | Status | Reason |
|---|---|---|
| Fitting code | excluded | user explicitly wants theoretical background, not implementation |
| Numerical solver construction | excluded | current derivation can proceed analytically through local tail scale |
| Peak area as main argument | excluded | peak area is later fitting/capacity decomposition |
| EMG as physical model | excluded | source says EMG is initial/comparison model only |
| Branch hysteresis state variables | excluded from main body | future chapter material |
| Heat coupling | excluded from main body | future chapter material after `dxi/dt` is fixed |
| Full Butler-Volmer model | excluded from main body | extension only unless voltage components are separated |
| Ref. 6/7 Fredholm method as core | excluded for now | verified in Phase 004 but no Fredholm-type graphite equation has yet been derived |

## Allowed Extensions After Core Logic Is Stable

| Extension | Condition |
|---|---|
| Kinetic barrier distribution `rho_j(g)` | allowed after single-barrier tail scale is derived |
| Forward/backward rates | allowed as an appendix or future refinement |
| Fredholm ratio-closure method from refs. 6/7 | allowed only if a self-referential integral equation is explicitly derived |
| Empirical peak parameters | allowed only as later validation/initialization observables |

## Source-To-Claim Table

| Claim | Source support |
|---|---|
| Tail should be explained by phase-progress dynamics, not instantaneous completion | `graphite_ica_dynamic_ver5.tex:55`, `62-79`; `graphite_ica_charge_balance_ver1_rechecked2.tex:63-65` |
| `V_n` is determined by charge balance | `graphite_ica_charge_balance_ver1_rechecked2.tex:118-129` |
| Equilibrium progress depends on internal potential | `graphite_ica_charge_balance_ver1_rechecked2.tex:184-201` |
| `V_n`, `V_{n,\app}`, and `V_{n,\drive}` must be separated | `graphite_ica_charge_balance_ver1_rechecked2.tex:203-238` |
| Effective barrier is intrinsic thermal barrier minus potential-assisted affinity | `graphite_ica_charge_balance_ver1_rechecked2.tex:240-249` |
| Rate uses positive effective barrier | `graphite_ica_charge_balance_ver1_rechecked2.tex:250-266` |
| Phase progress relaxes toward equilibrium and creates tail/broadening | `graphite_ica_charge_balance_ver1_rechecked2.tex:268-286` |
| ICA/DVA must be derived from charge-balance differentiation | `graphite_ica_charge_balance_ver1_rechecked2.tex:353-412` |
| C-rate effect has residence-time and drive-enhanced-rate components | `graphite_ica_charge_balance_ver1_rechecked2.tex:414-418` |
| Double-counting and identifiability must be guarded | `graphite_ica_charge_balance_ver1_rechecked2.tex:236-238`, `439-458`; `graphite_ica_dynamic_ver5.tex:891-894` |

## User Requirement Mapping

| User requirement | Contract item | Status |
|---|---|---|
| Explain ICA peak-tail behavior, especially tail shape | fixed observation and core scope | represented |
| Low T long tail, high T short tail | fixed observation and later limiting-case audit | represented |
| Equilibrium Gaussian-like peak alone is insufficient | non-goals and observation statement | represented |
| Thermal barrier plus present electrode potential lowering | central hypothesis | represented |
| Derive logic useful for later fitting | core equations retained, fitting excluded | represented |
| No solver/code construction | non-goals | represented |
| Undergraduate-followable derivation | required reader level | represented |
| No logical jumps | minimum logic chain and future Ralph Wiggum audit | represented |
| Existing drafts are reference only; write from scratch | summary and non-goal framing | represented |
| Use ref. 6/7 only after checking | Phase 004 decision imported here | represented |

## Validation

| Check | Result |
|---|---|
| Observation statement includes low-T long tail and high-T short tail | PASS |
| Gaussian/logistic equilibrium-only explanation rejected as sufficient | PASS |
| Peak area marked as later fitting/capacity issue | PASS |
| Present-potential barrier-lowering hypothesis stated in equations | PASS |
| Deliverable is derivation, not code | PASS |
| Undergraduate-level explanation requirement made explicit | PASS |
| Allowed/prohibited extensions separated | PASS |
| User requirements mapped to contract items | PASS |
| No unmet user requirement found in this phase | PASS |

## Gate

Gate: `PASS_SCOPE_LOCK`

Status: PASS

Reason:

- the user’s corrected scope is fully represented;
- Chapter 1 core is narrowed to tail/effective-barrier theory;
- peak-area, solver, fitting, heat, and hysteresis drift are explicitly locked out of the main derivation;
- the ref. 6/7 method is verified but reserved until a matching integral-equation structure exists.

## Confirmed Non-Changes

- No source `.tex` file was modified.
- No PDF was modified.
- `D:\Projects\Project_Anode_Fit\Claude` was not modified.
- No commit, push, merge, or branch operation was performed.

## Open Issues / Decision Queue

| Issue | Status |
|---|---|
| Detailed notation/dependency DAG still needed | pending Phase 006 |
| Tail scale not yet derived in restart chain | pending Phase 008 |
| Final manuscript section order not yet written | pending Phase 011 |

No user decision is required before Phase 006.

## Next

Proceed directly to Phase 006 — Notation And Dependency Bible.
