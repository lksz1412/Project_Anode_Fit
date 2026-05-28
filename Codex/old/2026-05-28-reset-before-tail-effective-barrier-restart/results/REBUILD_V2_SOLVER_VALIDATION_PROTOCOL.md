# Rebuild v2 Solver Validation Protocol

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 008 - Direct Solver, Approximation, And Validation Protocol`

Created: 2026-05-27

## Protocol Role

This document specifies how the exact graphite charge-balance DAE/Volterra formulation and any reference-closure approximation should be solved and validated. It does not implement numerical code and does not claim that numerical validation has been run.

Status: **algorithm specified, not executed**.

## Exact Solver Objective

For a grid of measurement nodes \(i=0,\ldots,N\), compute a self-consistent sequence

\[
\{q_i,T_i,I_i,\boldsymbol{\xi}_i,V_{n,i},V_{n,\mathrm{app},i}\}
\]

such that:

1. \(V_{n,i}\) solves the charge-balance residual for \((q_i,T_i,\boldsymbol{\xi}_i)\);
2. \(\boldsymbol{\xi}_{i+1}\) is updated only after \(V_{n,i}\) has been solved;
3. q-domain updates are used only when \(I_{\mathrm{abs},i}>0\);
4. rest segments use time-domain updates at fixed \(q\);
5. derivative observables are evaluated after the state/root trajectory exists.

## Inputs

| Input | Role | Required Shape |
|---|---|---|
| `q_i` | normalized external charge grid | monotone over nonzero-current segment |
| `t_i` | time grid | required for time/rest update |
| `T_i` | temperature path | array or constant |
| `I_i` | current path with sign convention | array |
| `I_abs_i` | current magnitude | nonnegative array |
| `xi_0` | initial internal states | vector length `N_p` |
| `theta` | model parameters | includes `Q_bg`, `Q_j,tot`, `U_j`, `w_j`, kinetic parameters |
| `V_interval` | admissible graphite voltage interval | bracket or branch domain |
| tolerances | named numerical thresholds | see tolerance section |

## Root Solve At Node i

At each node, define

\[
\mathcal{G}_i(V)
=
Q_{\mathrm{bg}}(V,T_i;\theta)
+
\sum_{j=1}^{N_p} Q_{j,\mathrm{tot}}\xi_{j,i}
-
Q_{\mathrm{cell}}q_i.
\]

Solve

\[
\mathcal{G}_i(V_{n,i})=0,
\qquad V_{n,i}\in[V_{\min},V_{\max}].
\]

The rate \(k_j\), equilibrium occupancy \(\xi_{j,\mathrm{eq}}(V_{n,i},T_i)\), apparent voltage, and derivative observables are not evaluated until this root is obtained.

## Root Bracket Strategy

Default bracket:

\[
[V_{\min},V_{\max}]=\mathcal{I}_V
\]

from the declared graphite model interval.

Preferred numerical sequence:

1. evaluate \(\mathcal{G}_i(V_{\min})\) and \(\mathcal{G}_i(V_{\max})\);
2. if a sign change exists, use bracketed root solve;
3. if no sign change exists but the previous node root \(V_{n,i-1}\) exists, attempt a local bracket around \(V_{n,i-1}\);
4. if multiple roots are found, select the continuous admissible branch from the previous node;
5. if no admissible root is found, return root failure rather than silently clipping voltage.

## Root Failure Reporting

Root failure must report:

- node index `i`;
- `q_i`, `T_i`, `I_i`;
- state vector `xi_i`;
- bracket used;
- residual values at bracket endpoints;
- previous root if available;
- reason: no sign change, no convergence, multiple branch ambiguity, outside interval, slope-floor violation.

## Slope-Floor Check

At each accepted root:

\[
\frac{\partial Q_{\mathrm{bg}}}{\partial V}(V_{n,i},T_i;\theta)
\ge
\epsilon_Q.
\]

If the check fails, mark the node as at least a warning. If the derivative is zero or changes sign in a way that makes the root singular, mark failure unless a declared regularization is used.

## State Update Strategies

### Time-Domain Update

Use for general dynamic integration and rest:

\[
\frac{\mathrm{d}\xi_j}{\mathrm{d}t}
=
k_j(V_n,q,T,I;\theta)
\left[\xi_{j,\mathrm{eq}}(V_n,T)-\xi_j\right].
\]

At each time step, root-solve \(V_n\) before evaluating the right-hand side.

### q-Domain Update

Use only when \(I_{\mathrm{abs}}>0\):

\[
\frac{\mathrm{d}\xi_j}{\mathrm{d}q}
=
\frac{Q_{\mathrm{cell}}}{I_{\mathrm{abs}}}
k_j(V_n,q,T,I;\theta)
\left[\xi_{j,\mathrm{eq}}(V_n,T)-\xi_j\right].
\]

If \(I_{\mathrm{abs}}\le\epsilon_I\), switch to time-domain update or rest handling.

### Rest Update At Fixed q

During rest:

\[
q_i=q_{\mathrm{rest}},
\qquad
I_{\mathrm{abs},i}=0.
\]

Use time-domain state update, and solve

\[
V_{n,i}=\mathcal{V}(q_{\mathrm{rest}},T_i,\boldsymbol{\xi}_i;\theta)
\]

at each time node. q-domain update is forbidden during rest.

## Derivative Evaluation

Derivatives are evaluated only after the state and root trajectory are available.

Isothermal internal-potential derivative:

\[
\frac{\mathrm{d}V_n}{\mathrm{d}q}
=
\frac{
Q_{\mathrm{cell}}
-
\sum_j Q_{j,\mathrm{tot}}\frac{\mathrm{d}\xi_j}{\mathrm{d}q}
}{
\partial Q_{\mathrm{bg}}/\partial V
}.
\]

Apparent-voltage derivative:

\[
\frac{\mathrm{d}V_{n,\mathrm{app}}}{\mathrm{d}q}
=
\frac{\mathrm{d}V_n}{\mathrm{d}q}
+
s_I
\frac{\mathrm{d}}{\mathrm{d}q}
\left[I_{\mathrm{abs}}R_n(q,T,I_{\mathrm{abs}})\right].
\]

ICA and DVA:

\[
\frac{\mathrm{d}Q_{\mathrm{ext}}}{\mathrm{d}V_{n,\mathrm{app}}}
=
\frac{Q_{\mathrm{cell}}}{\mathrm{d}V_{n,\mathrm{app}}/\mathrm{d}q},
\qquad
\frac{\mathrm{d}V_{n,\mathrm{app}}}{\mathrm{d}Q_{\mathrm{ext}}}
=
\frac{1}{Q_{\mathrm{cell}}}
\frac{\mathrm{d}V_{n,\mathrm{app}}}{\mathrm{d}q}.
\]

## Direct DAE / Root-Solve Pseudocode

```text
inputs: q_grid, t_grid, T_grid, I_grid, xi0, theta, V_interval, tolerances
xi[0] = xi0
for i in 0..N:
    Vn[i] = solve_root(G(V; q[i], T[i], xi[i], theta), V_interval)
    check_charge_residual(i)
    check_slope_floor(i)
    check_state_bounds(i)

    if i == N:
        break

    if I_abs[i] > eps_I and q is the integration coordinate:
        rhs = dxi_dq(Vn[i], q[i], T[i], I[i], xi[i], theta)
        xi[i+1] = q_step_update(xi[i], rhs, q[i+1]-q[i])
    else:
        rhs = dxi_dt(Vn[i], q[i], T[i], I[i], xi[i], theta)
        xi[i+1] = time_step_update(xi[i], rhs, t[i+1]-t[i])

postprocess:
    compute dxi_dq only on nonzero-current nodes
    compute dVn_dq
    compute dVapp_dq
    compute ICA/DVA
    emit validation table
```

## Quasi-Equilibrium Reference Solver Pseudocode

```text
for each q[i], T[i]:
    solve V_ocv[i] from equilibrium charge balance:
        Q_cell q[i] = Q_bg(V,T[i]) + sum_j Q_j,tot xi_eq_j(V,T[i])
    xi_ref[j,i] = xi_eq_j(V_ocv[i], T[i])
    Vn_ref[i] = V_ocv[i]
emit reference path
```

This reference is not the dynamic truth model. It is a thermodynamic reference path for closure construction.

## Frozen-Feedback Reference Solver Pseudocode

```text
choose xi_ref path:
    quasi-equilibrium path, previous direct solve, or low-rate direct solve
for each node i:
    Vn_ref[i] = solve_root(G(V; q[i], T[i], xi_ref[i], theta), V_interval)
    Psi_ref[j,i] = integrand_j(q[i], xi_ref[i], Vn_ref[i], T[i], I[i], theta)
emit frozen-feedback reference integrand
```

## Closure Approximation Pseudocode

```text
inputs: reference path, correction model, direct-solver validation target
for each node i:
    compute Psi_ref[j,i]
    estimate C_j[i] or Delta_j[i]
    if ratio mode:
        require abs(Psi_ref[j,i]) >= eps_ratio_den
        Psi_closure[j,i] = Psi_ref[j,i] * C_j[i]
    if additive mode:
        Psi_closure[j,i] = Psi_ref[j,i] + Delta_j[i]
    integrate xi_closure over q or time
    solve Vn_closure from charge balance
compare closure path against direct solver path
emit closure residuals
```

## Residual Definitions

| Residual | Formula / Definition | Required For |
|---|---|---|
| charge balance | `r_G[i]=G(Vn_i;q_i,T_i,xi_i,theta)/Q_cell` | exact solver and closure |
| root bracket | endpoint residual signs and final root residual | root solve |
| slope floor | `dQ_bg/dV(Vn_i,T_i)-epsilon_Q` | root conditioning |
| state bounds | min violation of `0 <= xi_j <= 1` with tolerance | physical state |
| q-domain eligibility | `I_abs_i > eps_I` | q update |
| derivative denominator | `abs(dVapp_dq_i)` compared to threshold | ICA safety |
| capacity closure | endpoint storage versus `Q_cell q` | model consistency |
| closure state mismatch | `xi_closure - xi_direct` | closure validation |
| closure voltage mismatch | `Vn_closure - Vn_direct` | closure validation |
| closure observable mismatch | ICA/DVA closure residual | fitting relevance |

## Named Tolerances

Numerical tolerances are named variables, not final hard-coded values:

| Tolerance | Meaning | Default Proposal Status |
|---|---|---|
| `tol_charge` | maximum normalized charge residual | needs empirical calibration |
| `tol_root` | root solver residual tolerance | needs implementation calibration |
| `tol_state` | allowed state-bound violation | needs calibration |
| `eps_I` | nonzero-current floor for q-domain update | dataset dependent |
| `eps_Q` | storage slope floor | model dependent |
| `eps_dVdq` | denominator floor for ICA | model/data dependent |
| `eps_ratio_den` | closure ratio denominator floor | closure dependent |
| `tol_closure_xi` | state mismatch tolerance | to be set in Phase 008 implementation or later |
| `tol_closure_V` | voltage mismatch tolerance | to be set in Phase 008 implementation or later |
| `tol_closure_obs` | ICA/DVA mismatch tolerance | to be set in fitting protocol |

## Validation Table Format

Future numerical runs should emit:

| Field | Meaning |
|---|---|
| `node_count` | number of evaluated grid nodes |
| `root_success_count` | nodes with accepted root |
| `root_failure_count` | nodes with failure |
| `max_abs_r_G` | maximum normalized charge residual |
| `min_slope_floor_margin` | minimum slope margin |
| `max_state_bound_violation` | maximum state-domain violation |
| `min_abs_dVapp_dq` | denominator safety indicator |
| `closure_max_xi_error` | closure versus direct state error |
| `closure_max_V_error` | closure versus direct voltage error |
| `closure_max_obs_error` | closure versus direct ICA/DVA error |
| `status` | PASS / WARNING / FAIL |

## Synthetic Smoke-Test Scenario

Purpose: test solver ordering without using experimental claims.

Scenario:

- one transition, \(N_p=1\);
- constant temperature;
- constant nonzero current;
- monotone linear background storage, \(Q_{\mathrm{bg}}(V)=b_0+b_1V\) with \(b_1>0\);
- logistic \(\xi_{\mathrm{eq}}(V,T)\);
- simple positive constant rate \(k_1\);
- initial state inside `[0,1]`;
- voltage bracket wide enough to contain the root.

Expected qualitative result:

- root solve succeeds at all nodes;
- \(V_n\) changes continuously;
- \(\xi_1\) relaxes toward the local equilibrium occupancy;
- charge residual remains near zero;
- q-domain update is used only for nonzero current;
- ICA/DVA denominators are finite unless intentionally constructed otherwise.

This smoke test would validate algorithm ordering, not physical fit quality.

## Status Classes

| Status | Meaning |
|---|---|
| PASS | all roots accepted, residuals within tolerance, state bounds satisfied, denominator safe, closure comparison acceptable if closure used |
| WARNING | root solved but slope margin, denominator, closure mismatch, or state-bound margin is near threshold |
| FAIL | missing root, invalid q-domain rest update, charge residual above tolerance, state bounds severely violated, denominator singularity, closure lacks direct comparison |

## Manuscript-Level Algorithm Block

The final manuscript may include:

```text
Algorithm 1. Direct charge-balance root-solve integration
1. Initialize q, T, I, xi, theta, and voltage interval.
2. At each node, solve charge balance for V_n.
3. Evaluate equilibrium occupancy and rates at the solved V_n.
4. Update xi in time or q according to current condition.
5. Re-solve V_n after each state update.
6. Compute derivative observables after the trajectory is complete.
7. Validate charge residual, state bounds, root conditioning, and ICA denominator safety.
```

If no code has been run, the manuscript must say "algorithm specified" or "solver protocol defined", not "validated numerically."

## Future Result Artifact Shape

If a future Python solver is created, it should emit:

- `solver_config.json`: parameters, tolerances, model settings;
- `solver_trace.csv`: node-level `q`, `t`, `T`, `I`, `xi_j`, `V_n`, residuals;
- `validation_summary.json`: status classes and max/min residual metrics;
- `closure_comparison.csv`: direct versus closure path if closure is used;
- `figures/`: optional plots generated from real or synthetic data, labeled accordingly.

Minimal future command shape:

```text
python solve_graphite_charge_balance.py --config solver_config.json --out results_dir
```

No such command was run in Phase 008 because no solver implementation is required for the manuscript rebuild unless the user separately requests it.

## Relationship To Fitting Protocol

The solver protocol supplies the forward model and validation gates. The fitting protocol in Phase 009 must decide:

- which parameters are fitted first;
- which parameters are fixed or constrained;
- how to prevent `Q_bg`, transition capacities, `R_n`, and kinetic parameters from absorbing each other;
- which residuals are optimized;
- how uncertainty and identifiability are reported.

Fitting must not proceed until the solver protocol can produce a valid forward trajectory.

## Source Evidence Links For Solver Equations

| Solver Equation / Rule | Source Evidence |
|---|---|
| measured `q` and `Q_ext` | corrected ver1 lines 95-105; Phase 002 evidence index |
| charge-balance residual and root | corrected ver1 lines 121-129; Phase 006 equations C1.8-C1.13 |
| slope floor | corrected ver1 lines 176-182; Phase 006 C1.11 |
| voltage distinctions | corrected ver1 lines 203-237; Phase 006 C1.17-C1.20 |
| time/q dynamics | corrected ver1 lines 240-286; Phase 006 C1.21-C1.23 |
| rest relaxation | corrected ver1 lines 289-299; Phase 006 C1.25-C1.26 |
| ICA/DVA derivatives | corrected ver1 lines 353-411; Phase 006 C1.27-C1.31 |
| closure comparison | Phase 007 closure contract; ref6/ref7 method notes |

## New Synthesis Status

The solver algorithm order, result artifact shape, status classes, and smoke-test scenario are new synthesis based on Phase 006 equations and Phase 007 closure requirements. They are not copied from ver5 or the previous draft.

## Commands Not Run

| Command / Action | Reason |
|---|---|
| numerical direct solver | no implementation exists yet and Phase 008 requires protocol only |
| synthetic smoke-test execution | no solver implementation exists yet |
| experimental dataset fit | no dataset or fitting protocol is active yet |
| LaTeX build | final manuscript file has not been assembled |

## Open Issues

| Issue | Status |
|---|---|
| no numerical code exists | open |
| no experimental dataset loaded | open |
| tolerance values require empirical calibration | open |
| user decision needed if implementation appendix is desired | open |
| user decision needed if synthetic examples should be generated | open |

## Phase 009 Dependency

Phase 009 must build the fitting and identifiability protocol on top of this solver protocol. It must prevent unconstrained co-fitting of parameters that can absorb each other and must decide which residuals are fit.

## Gate Statement

Gate: `PASS_REBUILD_V2_SOLVER_VALIDATION`

This protocol passes because it specifies direct solver pseudocode, reference solver pseudocode, closure approximation pseudocode, residual definitions, tolerance names, validation table format, smoke-test scenario, status classes, future artifact shape, non-execution wording, and fitting-protocol dependency.
