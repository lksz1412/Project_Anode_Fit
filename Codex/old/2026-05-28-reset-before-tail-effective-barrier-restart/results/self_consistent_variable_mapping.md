# Self-Consistent Variable Mapping

Project: `D:\Projects\Project_Anode_Fit`

Phase: 005

Date: 2026-05-27

Inputs:

- `D:\Projects\Project_Anode_Fit\Codex\results\ver1_charge_balance_dependency_graph.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\ref6_ref7_method_notes.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\ver5_chapter_structure_map.md`

## Executive Mapping Decision

The graphite problem should be formulated first as a coupled algebraic-root / nonlinear Volterra integral system, or equivalently as a differential-algebraic equation (DAE) with an algebraic charge-balance constraint.

It should not be forced into a literal Fredholm problem merely because refs. 6/7 use Fredholm integral equations of the second kind.

The portable method from refs. 6/7 is:

```text
derive the self-consistent integral form
-> isolate an unknown feedback ratio/correction
-> close it using a simpler reference solution
-> verify against direct numerical solution
```

For the graphite dQ/dV model, the exact state formulation remains:

```text
G(V_n; q,T,xi) = Q_bg(V_n,T) + sum_j Q_j,tot xi_j - Q_cell q = 0

dxi_j/dq = (Q_cell/|I|) k_j(V_n,q,T,I)
          [xi_eq,j(V_n,T) - xi_j]
```

and the corresponding q-domain integral form is:

```text
xi_j(q) = xi_j(q0)
        + integral_{q0}^{q} (Q_cell/|I(s)|) k_j(V_n(s),s,T(s),I(s))
          [xi_eq,j(V_n(s),T(s)) - xi_j(s)] ds
```

where `V_n(s)` is not prescribed; it is the root of charge balance at the current `xi(s)`.

## Abstract Ref. 6/7 Method Form

| Required Field | Ref. 6/7 / 2017 Paper Form | Evidence |
|---|---|---|
| unknown function | survival/separation probability, written as `W(r)` or `\bar W_u(r)` | user paper page 5, Eq. (32)-(39) context |
| known kernel | functions such as `\chi`, `\Lambda`, potential factors, geometry factors | user paper page 5 |
| boundary condition | survival tends to unity at infinity; inner condition at contact radius | user paper pages 3-4 |
| self-consistent variable | the unknown `W` appears inside the integral equation | user paper page 5, Eq. (32) context |
| iteration or solver | not naive fixed-point only; formally exact reciprocal rewrite plus ratio closure | user paper page 5; ref. 6 metadata |
| normalization | contracted reactivity / reference delta-sink matching | user paper page 5, Eq. (35)-(38) context |

## Graphite Abstract Problem Form

| Required Field | Graphite Form | Evidence |
|---|---|---|
| unknown quantity | `V_n(q)` and dynamic states `xi_j(q)` or `xi_j(t)` | ver1 lines 121-129, 268-286 |
| measured quantity | `Q_ext`, current/time history, apparent voltage / dQdV data | ver1 lines 95-105, 394-411 |
| thermodynamic OCV relation | equilibrium OCV is an implicit charge-balance solution | ver1 lines 148-162 |
| background capacity | `Q_bg(V_n,T)` with positive slope floor | ver1 lines 121-129, 176-182 |
| phase fraction | `xi_j`, `xi_eq,j(V_n,T)`, optional distributed `xi_j(g,t)` | ver1 lines 109-117, 184-201, 320-349 |
| voltage variable | `V_n` internal, `V_app` apparent, `V_drive` kinetic | ver1 lines 203-237 |
| capacity variable | external `Q_ext=Q_cell q`, not arbitrary modeled `Q_n(q)` | ver1 lines 95-105, 394-411 |

## Variable Mapping Table

| Ref Method Symbol / Role | Ref Method Meaning | Graphite Symbol / Role | Graphite Meaning | Mapping Confidence | Assumption Required |
|---|---|---|---|---|---|
| `W(r)` / `\bar W_u(r)` | unknown observable to solve | `xi_j(q)` | dynamic phase/transition progress | medium | use state trajectory, not probability, as the unknown function |
| `W(r)` / `\bar W_u(r)` | unknown observable to solve | `V_n(q)` | algebraic internal potential solved from charge balance | medium | treat `V_n` as a functional of `xi(q)`, not an independent prescribed function |
| kernel in Eq. (32) | known integral weighting once model functions are fixed | `(Q_cell/|I|) k_j(...)` | q-domain kinetic weight in the integral form | medium | root-solve `V_n` before evaluating rate; not a closed known kernel until reference closure is chosen |
| `\chi`, `\Lambda`, potential factors | analytic kernel components | `Q_bg`, `xi_eq`, `k_j`, `R_n` | thermodynamic/kinetic model functions | low-medium | these are not physically analogous; only their mathematical role as model functions is portable |
| boundary `W(\infty)=1` | far-field survival normalization | initial condition plus endpoint capacity constraints | charge-balance-consistent start/end states | low | graphite has initial-value and capacity-closure constraints, not far-field survival |
| inner boundary at `r=\sigma` | contact condition | `q=0/1` or selected fitting window endpoints | edge of usable SOC/q range | low | endpoint behavior must come from data and thermodynamic constraints |
| ratio `W(r1)/W(r)` | unknown ratio moved into exact reciprocal expression | feedback correction ratio or residual ratio | correction between actual coupled path and reference path | medium | ratio must be defined so denominator cannot vanish or must be regularized |
| delta-sink reference solution | simpler solvable reference problem | quasi-equilibrium charge-balance path | `xi_j=xi_eq(V_n,T)` and implicit `V_OCV(q,T)` | medium-high | valid as thermodynamic reference, not as dynamic truth |
| delta-sink reference solution | simpler solvable reference problem | frozen-kinetic or low-C reference path | baseline dynamic path used for closure | medium | must be validated against direct coupled solve |
| contracted reactivity | normalization matching long-range sink to reference sink | capacity / peak-area normalization | match `sum Q_j,tot` and `Q_bg` endpoints to `Q_cell` | medium | normalization is capacity-based, not reaction-rate based |
| finite-element benchmark | direct numerical truth model | direct DAE/root-solve integration | validation baseline for closure approximation | high | direct solver must be implemented or specified before claiming accuracy |

## Portable Method Parts

| Part | Portable? | How To Use In Graphite |
|---|---|---|
| second-kind self-consistent formulation | yes, conceptually | write `xi = xi0 + integral[F(xi)]` after substituting charge-balance root |
| formal isolation of feedback | yes | isolate the unknown correction caused by `V_n[xi]` re-entering `xi_eq` and `k_j` |
| reference-solution closure | yes | use quasi-equilibrium or stable low-rate path as reference closure |
| ratio/correction rather than absolute-function guessing | yes | approximate a dimensionless correction/residual, not raw `xi_j` if possible |
| validation against direct numerical solution | yes | compare closure against DAE/root-solve integration and experimental ICA/DVA |
| regime statement for approximation | yes | state when closure is expected to work and when it should be rejected |

## Non-Portable Physical Assumptions

| Assumption From Ref. 6/7 / 2017 Paper | Portable? | Reason |
|---|---|---|
| geminate charge-pair recombination | no | not LIB graphite phase thermodynamics |
| Smoluchowski diffusion in relative coordinate `r` | no | graphite `q` is an electrochemical capacity coordinate |
| central Coulomb or screened Coulomb potential | no | graphite potential is charge-balance/internal chemical potential |
| external electric field orientation averaging | no | graphite voltage/current roles are scalar circuit variables in this draft |
| contact radius / delta-function sink physics | no | graphite has transition capacities and OCV peaks, not a reaction contact radius |
| Onsager distance / Debye-Huckel length | no | no corresponding graphite parameter |
| mean-value theorem approximation over orientation `mu` | no | only the idea of declaring approximation regimes is portable |
| finite-element solution of Smoluchowski PDE as benchmark | partly | direct numerical benchmark is portable, but not the PDE itself |

## Mathematical Class Decision

| Candidate Class | Status For Graphite | Reason |
|---|---|---|
| algebraic root-finding problem | required | `V_n` must be solved from charge balance at each state |
| nonlinear ODE / DAE | required | `xi_j` evolves while constrained by algebraic charge balance |
| Volterra-type integral equation | primary integral form | q/time evolution has causal upper limit from initial condition |
| Fredholm-type integral equation | not primary | only appears if the whole q window is reformulated as a global boundary/inversion problem |
| fixed-point equation | algorithmic option | not the safest definition of the problem itself |
| coupled differential/integral system | preferred complete class | covers algebraic solve, ODE/integral update, and observables |

Decision:

```text
Primary formulation = charge-balance-constrained nonlinear Volterra/DAE system.
Ref. 6/7 contribution = reference-ratio/correction closure for analytic or fast fitting surrogates.
```

## Solver-Neutral Formulation

Define the charge-balance residual:

```text
G(V; q,T,xi,theta)
  = Q_bg(V,T;theta)
  + sum_j Q_j,tot xi_j
  - Q_cell q
```

At each state, solve:

```text
G(V_n; q,T,xi,theta)=0
```

Then define:

```text
F_j(q,xi,T,I;theta)
  = (Q_cell/|I|) k_j(V_n(q,xi),q,T,I;theta)
    [xi_eq,j(V_n(q,xi),T;theta)-xi_j]
```

and:

```text
xi_j(q) = xi_j(q0) + integral_{q0}^{q} F_j(s,xi(s),T(s),I(s);theta) ds
```

This formulation does not require choosing Newton, secant, Picard, quadrature, or an optimizer yet.

## Ref. 6/7-Inspired Closure Options

### Option A - Direct DAE Baseline

Purpose:

- establish numerical truth;
- avoid approximation while testing model logic.

Use:

```text
state -> solve V_n root -> evaluate xi_eq/k -> integrate xi -> repeat
```

This is required as the benchmark even if a closure approximation is later used for fitting.

### Option B - Quasi-Equilibrium Reference Closure

Reference path:

```text
xi_j^ref(q) = xi_eq,j(V_OCV(q,T),T)
```

where `V_OCV` is the implicit equilibrium charge-balance solution.

Use:

- best for thermodynamic dQ/dV shape and low-rate baseline;
- good candidate for Chapter 1's "thermodynamic shape" role.

Risk:

- loses kinetic lag and hysteresis unless later chapters add them as interfaces.

### Option C - Frozen-Feedback Reference Closure

Reference path:

```text
V_n^ref(q) = solve charge balance using xi^ref
```

then use the reference to approximate the correction:

```text
actual feedback correction ~= reference feedback correction
```

Use:

- can preserve a closed fitting expression while avoiding an unstable raw fixed-point loop.

Risk:

- needs residual gates; otherwise it can hide the same circularity under a reference label.

### Option D - Discretized Integral Solve

Discretize q, keep the charge-balance root at each node, and solve all node states with constrained nonlinear least squares.

Use:

- robust for fitting;
- easiest to enforce bounds, monotonicity, and charge-balance residual.

Risk:

- less analytic; may be heavier than needed for a chapter derivation.

## Identifiability Risks

| Risk | Why It Matters | Gate / Mitigation |
|---|---|---|
| `Q_bg` vs transition capacities | both can absorb broad capacity | constrain slope floor and endpoint capacity |
| `R_n` vs `k_j` | both can shift apparent dynamic voltage response | do not freely co-fit without priors or staged fit |
| `U_j,w_j` vs `Q_j,tot` | peak location, width, and area can trade off | use charge-balance residual plus ICA/DVA peak constraints |
| kinetic lag vs thermodynamic broadening | lag can look like broadened dQ/dV peaks | fit low-rate thermodynamic baseline before rate effects |
| hysteresis vs path-dependent `xi_j` | later Chapter 5 can absorb errors from Chapter 1 | declare Chapter 1 interface and defer hysteresis |
| distributed barrier `rho_j(g)` | can overfit any peak asymmetry | keep optional until single-barrier model fails |
| denominator singularity in ICA | `dV_app/dq` near zero or sign errors break observables | enforce monotonicity and denominator gates |

## Validation Observables

| Observable / Residual | Formula / Check | Pass Meaning |
|---|---|---|
| charge-balance residual | `G(V_n;q,T,xi)/Q_cell` | algebraic loop actually solved |
| root uniqueness / conditioning | `dQ_bg/dV_n >= epsilon_Q` plus bracket/range check | no hidden multi-root branch jump |
| phase bounds | `0 <= xi_j <= 1` and optional monotonic direction | state remains physical |
| capacity closure | endpoint `Q_bg + sum Q_j xi_j` matches `Q_cell q` | no missing charge reservoir |
| dQ/dV peak positions | predicted ICA peaks vs measured peaks | thermodynamic shape credible |
| dV/dQ consistency | reciprocal derivative relation away from singular points | observable definitions consistent |
| direct solver comparison | closure path vs DAE/root-solve path | reference closure is not just a circular assumption |
| low-rate limit | approaches implicit OCV / equilibrium path | thermodynamic limit correct |
| rest behavior | fixed q, `xi(t)` relaxes and `V_n(t)` re-solves | rest voltage logic preserved |

## Phase 006 Interface Decision

Chapter 1 should include:

- charge-balance equation as the primary definition of internal graphite potential;
- implicit equilibrium OCV as a derived relation;
- dynamic self-consistency as a solver-neutral DAE/Volterra formulation;
- refs. 6/7-inspired closure as a method section for stable fitting / analytic approximation;
- explicit validation gates.

Chapter 1 should not include:

- heat approximation as a solved subsystem;
- full Butler-Volmer electrochemical interface model;
- hysteresis structural memory model;
- physical assumptions from geminate pair diffusion.

Those belong to later chapters or interfaces.
