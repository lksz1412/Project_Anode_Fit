# Chapter 1 Rewrite Specification

Project: `D:\Projects\Project_Anode_Fit`

Phase: 006

Date: 2026-05-27

Inputs:

- `D:\Projects\Project_Anode_Fit\Codex\results\ver5_chapter_structure_map.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\ver1_charge_balance_dependency_graph.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\self_consistent_variable_mapping.md`

## Chapter 1 Role

Chapter 1 defines the thermodynamic charge-balance model that determines the internal graphite potential `V_n` from external charge progress `q`, temperature `T`, and transition states `xi_j`. It establishes the equilibrium OCV relation as an implicit charge-balance solution, defines the self-consistent state equation in solver-neutral form, and derives the ICA/DVA observables from the solved apparent voltage path.

## Chapter 1 Non-Role

Chapter 1 must not solve the full heat model, full Butler-Volmer interface model, full multi-chapter fitting state system, or hysteresis/structural-memory model. It may define the minimal interfaces needed by later chapters, such as `dxi_j/dt`, `V_n`, `V_app`, charge-balance residuals, and derivative observables.

## Inputs

| Input | Meaning | Source / Evidence | Notes |
|---|---|---|---|
| `Q_ext(t)` | external charge passed through circuit | ver1 lines 95-101 | measured or current-integrated |
| `Q_cell` | reference cell capacity in coulomb | ver1 lines 88-93 | convert Ah to C before equations |
| `q=Q_ext/Q_cell` | dimensionless discharge coordinate | ver1 lines 100-105 | primary coordinate for ICA/DVA |
| `T(t)` or `T(q)` | temperature | throughout ver1 | can be fixed for isothermal Chapter 1 derivation |
| `I(t)` | current magnitude/sign convention | ver1 lines 95-105, 217-237 | q-domain ODE invalid at rest |
| `Q_bg(V,T)` | background storage function | ver1 lines 121-129 | must satisfy slope floor |
| `Q_j,tot` | transition capacity contribution | ver1 lines 112-114, 164-174 | constrained by capacity closure |
| `U_j(T), w_j(T)` | equilibrium transition center and width | ver1 lines 184-201 | reserve `w_j` for equilibrium width only |
| `R_n(q,T,|I|)` | apparent voltage resistance/polarization term | ver1 lines 217-237 | must not be freely co-fit with kinetics |
| kinetic parameters | parameters in `k_j` | ver1 lines 240-266 | needed only for dynamic interface |

## Unknowns / Solved Quantities

| Unknown | How It Is Determined | Evidence | Notes |
|---|---|---|---|
| `V_n` | root of charge-balance residual `G(V)=0` | ver1 lines 121-129 | never prescribe as arbitrary `V_n(q,T)` in Chapter 1 |
| `xi_j` | dynamic state or equilibrium state depending on subsection | ver1 lines 109-117, 268-286 | must be initialized consistently |
| `V_OCV(q,T)` | equilibrium solution with `xi_j=xi_eq,j(V,T)` | ver1 lines 148-162 | derived, not input |
| `V_app` | observation voltage after `V_n` plus apparent term | ver1 lines 217-222 | depends on current convention |
| `dxi_j/dq`, `dxi_j/dt` | evaluated after state/root solve | ver1 lines 268-286 | q-form only for nonzero current |
| `dV_n/dq`, `dV_app/dq` | derivative from charge balance and apparent term | ver1 lines 353-391 | derivative stage comes after state solve |

## Outputs / Interfaces

| Output | Passed To | Meaning |
|---|---|---|
| `V_n(q)` | Chapters 2-5 | internal graphite potential path |
| `V_app(q)` | fitting/observable chapters | apparent voltage path |
| `V_OCV(q,T)` | thermodynamic baseline / low-rate fitting | equilibrium OCV derived from charge balance |
| `xi_j(q)` / `xi_j(t)` | heat, kinetics, state fitting | transition progress states |
| `dxi_j/dt` | heat layer | physical rate for heat source terms |
| `dxi_j/dq` | ICA/DVA and constant-current analysis | q-coordinate rate |
| `dQ_ext/dV_app` | observable | ICA based on external charge |
| `dV_app/dQ_ext` | observable | DVA based on external charge |
| charge-balance residual | validation / optimizer | numerical consistency gate |
| monotonicity and capacity constraints | fitting system | physical admissibility gates |

## Required Logical Order

1. Define measured variables: `Q_ext`, `Q_cell`, `q`, `I`, `T`.
2. Define storage functions and parameters: `Q_bg`, `Q_j,tot`, `U_j`, `w_j`.
3. Define state variables `xi_j` and equilibrium functions `xi_eq,j(V,T)`.
4. Define charge-balance residual `G(V;q,T,xi)`.
5. Define `V_n = V_root(q,T,xi)` as the unique admissible root of `G=0`.
6. Define equilibrium OCV as the special root with `xi_j=xi_eq,j(V,T)`.
7. Define apparent and driving voltages after `V_n` exists.
8. Define kinetic rates and dynamic equations.
9. Rewrite the dynamic equation as a solver-neutral DAE/Volterra integral form.
10. Introduce the refs. 6/7-inspired reference closure only after the exact problem class is stated.
11. Derive `dV_n/dq`, `dV_app/dq`, ICA, and DVA after the state/root solve.
12. State validation gates and limitations.

This order removes the circular dependency by defining `V_n` as a root-solve operator before any downstream quantity uses it.

## Equations To Retain

| Equation / Block | Retain? | Required Treatment |
|---|---|---|
| Ah-to-C conversion and `q=Q_ext/Q_cell` | yes | keep as the measured coordinate basis |
| `Q_cell q = Q_bg(V_n,T)+sum Q_j,tot xi_j` | yes | promote to Chapter 1 central equation |
| solution range / existence condition | yes | keep as admissibility condition |
| equilibrium OCV implicit equation | yes | define as derived equilibrium relation |
| total capacity consistency | yes | keep as fitting/normalization constraint |
| slope floor `partial Q_bg / partial V_n >= epsilon_Q` | yes | keep as root conditioning gate |
| `xi_eq,j(V_n,T)` logistic/signed form | yes | keep, but define before use |
| `V_app=V_n+s_I|I|R_n` | yes | keep as observation interface, with staged fitting warning |
| softplus barrier and `k_j` | yes | keep as dynamic interface, not thermodynamic definition |
| `dxi_j/dt` and nonzero-current `dxi_j/dq` | yes | place after `V_n` root solve |
| rest relaxation | yes | keep as fixed-q time-domain re-solve |
| `dV_n/dq`, `dV_app/dq`, ICA/DVA | yes | derive after state/root definition |

## Equations / Statements To Rewrite

| Item | Why Rewrite | Replacement |
|---|---|---|
| any phrase implying `V_n(q,T)` is an arbitrary OCV input | conflicts with charge-balance correction | write `V_n = V_root(q,T,xi)` |
| dynamic equations before root-solve definition | creates apparent circularity | introduce `G=0` and root operator first |
| `xi_eq(V_n,T)` before `V_n` status is clear | reader may think `V_n` is prescribed | define `xi_eq(V,T)` for a dummy voltage `V`, then evaluate at solved `V_n` |
| derivative equations without solution ordering | hides feedback in `dxi/dq` | state: solve state/root first, then evaluate derivatives |
| reference method as direct physical import | false analogy | state it is a mathematical closure pattern |
| free co-fitting of `R_n` and `k_j` | identifiability risk | stage or constrain one before fitting the other |
| historical `ver.1` labels inside body | obsolete after chapter conversion | rename to Chapter 1 and remove version-history body notes |

## Content To Defer

| Content | Defer To | Chapter 1 Handling |
|---|---|---|
| heat approximation / heat source fitting | Chapter 2 | pass `dxi_j/dt`, `V_n`, `V_app`, `T` |
| Butler-Volmer electrochemical interface expansion | Chapter 3 | pass `V_drive`, `A_j`, `k_j` interface only |
| integrated optimization/state-observation system | Chapter 4 | provide residuals and constraints |
| hysteresis / branch / structural memory | Chapter 5 | expose extension hooks but do not solve |
| distributed barrier `rho_j(g)` | optional appendix or later extension | mention as optional if needed |

## Notation Rules

| Rule | Purpose |
|---|---|
| Use `V_n` only for the solved internal graphite potential | prevents treating it as an independent input |
| Use `\mathcal V(q,T,\boldsymbol\xi;\theta)` or `V_root` for the root-solve operator | makes self-consistency explicit |
| Use `V_{n,\mathrm{OCV}}(q,T)` only for the equilibrium charge-balance root | prevents dynamic/OCV collapse |
| Use `Q_ext=Q_cell q` for external measured charge | avoids reverting to old `Q_n(q)` observable |
| Reserve `Q_bg` for background storage, not visual baseline only | preserves charge conservation |
| Reserve `w_j` for equilibrium transition width | avoids collision with any heat-layer weight |
| Use `a_j=Q_j,tot/Q_cell` if a dimensionless capacity fraction is needed | avoids overloading `w_j` |
| Keep `V_n`, `V_app`, and `V_drive` distinct | prevents double-counting polarization and kinetics |
| Mark reference-closure quantities with superscript `ref` | separates approximation from solved state |
| Do not include change-history notes in LaTeX body | follows project/global document rule |

## Chapter 1 Section Skeleton

1. Purpose and scope of Chapter 1.
2. Measured charge coordinate and sign convention.
3. Transition states and equilibrium occupancy functions.
4. Charge-balance equation and internal potential root.
5. Equilibrium OCV as an implicit special case.
6. Capacity consistency and admissible solution range.
7. Apparent voltage and driving voltage interfaces.
8. Dynamic self-consistent formulation as DAE/Volterra integral equation.
9. Ref. 6/7-inspired reference closure for stable fitting approximation.
10. Derivative observables: `dV/dq`, ICA, and DVA.
11. Validation gates and limitations.
12. Interfaces to Chapters 2-5.

## Gate Check

Chapter 1 no longer depends on a variable before it is defined if:

- `q`, `Q_ext`, `Q_cell`, `T`, and `I` are introduced before all model equations;
- `xi_eq(V,T)` is defined for a dummy voltage before evaluation at `V_n`;
- `V_n` is introduced as `V_root(q,T,xi)` immediately after charge balance;
- `k_j`, `V_app`, `V_drive`, and derivatives appear only after `V_n` exists;
- the self-consistent method is described as a solver for the coupled system, not as a pre-existing value.
