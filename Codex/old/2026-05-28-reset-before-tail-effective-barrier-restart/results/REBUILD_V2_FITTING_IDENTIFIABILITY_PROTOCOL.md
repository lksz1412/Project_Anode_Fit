# Rebuild v2 Fitting Identifiability Protocol

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 009 - Fitting Strategy And Identifiability Protocol`

Created: 2026-05-27

## Protocol Role

This document defines how graphite ICA/DVA fitting should be staged so thermodynamic, storage, kinetic, observation, thermal, and hysteresis parameters do not absorb each other. It is a fitting protocol, not a completed fit.

Status: **fitting strategy specified, not executed**.

## Fitting Purpose

The fitting purpose is to estimate thermodynamic and dynamic parameters while preserving the Phase 006 charge-balance structure:

\[
\mathcal{G}(V_n;q,T,\boldsymbol{\xi};\theta)=0.
\]

The fitted model must reproduce voltage/ICA/DVA features only through a valid forward trajectory: measured charge coordinate, root-solved internal potential, state evolution, apparent voltage, and validated derivatives. No fitting stage may replace charge conservation with a shape-only empirical curve.

## Data Prerequisites

| Data | Required Use | Notes |
|---|---|---|
| voltage path | compare apparent voltage and derivative observables | raw \(V(Q)\) preferred over derivative-only data |
| current/time path | determine \(Q_{\mathrm{ext}}\), `q`, rest, and rate conditions | rest intervals must be explicitly marked |
| capacity axis | define \(Q_{\mathrm{ext}}\), \(Q_{\mathrm{cell}}\), and q-grid | units must be normalized first |
| temperature path | fit or defer thermal correction | if absent, use isothermal protocol and record limitation |
| raw V-Q data | derivative reconstruction and voltage residual | preferred for stable fitting |
| dQ/dV or dV/dQ data | shape residual and peak constraints | derivative preprocessing must be documented |
| cycle/branch labels | hysteresis diagnosis | required before Chapter 5 memory fitting |

## Preprocessing Assumptions

- Convert capacity to coulomb or a declared normalized unit before fitting.
- Fix current sign convention and orientation before assigning \(s_I\), \(s_{\xi,j}\), and \(s_{\phi,j}\).
- Smooth derivative data only with a declared method; do not let smoothing create or remove peaks silently.
- Separate rest, low-rate, high-rate, charge, and discharge segments before fitting.
- Keep raw voltage residual available even when fitting ICA/DVA.
- Do not infer fitted performance from derivative-only visual agreement.

## Staged Fitting Order

| Stage | Name | Main Goal | Free Groups | Fixed / Constrained Groups | Acceptance Gate |
|---:|---|---|---|---|---|
| 0 | unit normalization and sign convention | establish reliable \(q,T,I,V\) axes | none | all model parameters fixed | consistent units, monotone q on active segments |
| 1 | low-rate thermodynamic baseline | estimate equilibrium storage/transition shape | `theta_thermo`, selected `theta_storage` | kinetics, `R_n`, heat, hysteresis fixed/off | OCV/special-root path and low-rate derivative shape credible |
| 2 | charge-balance residual and capacity closure | enforce storage conservation | constrained storage/capacity terms | kinetics and observation shifts fixed/off | normalized charge residual and endpoint capacity closure pass |
| 3 | transition centers, widths, capacities | refine peak position/width/area | `U_j`, `w_j`, `Q_j,tot` under constraints | `Q_bg` slope and capacity closure constrained | peaks explained without arbitrary background absorption |
| 4 | kinetic lag parameters | explain rate-dependent state lag | `theta_kinetic` | thermodynamic/storage fixed or tightly regularized; `R_n` fixed or constrained | direct solver residuals and low/high-rate consistency pass |
| 5 | apparent resistance/polarization `R_n` | explain observation voltage shift | selected `theta_observation` | kinetic parameters fixed or regularized | no unconstrained `R_n`/`k_j` co-fit |
| 6 | thermal correction | account for measured/modelled temperature effects | `theta_thermal` | previous groups constrained | only if temperature data or validated thermal model exists |
| 7 | hysteresis/memory | diagnose irreducible branch/memory effects | `theta_hysteresis` | all earlier groups constrained and residual failure documented | only after thermodynamic/dynamic residuals fail |

## Parameter Groups

| Group | Contents | Default Treatment |
|---|---|---|
| `theta_thermo` | transition centers `U_j(T)`, widths `w_j(T)`, orientation signs, equilibrium occupancy shape | fitted first under monotonicity and physical bounds |
| `theta_storage` | `Q_bg(V,T)`, `Q_j,tot`, `Q_cell` normalization, slope floor | constrained by capacity closure and residuals |
| `theta_kinetic` | relaxation rates `k_j`, rate dependence, activation/barrier options | fitted after thermodynamic baseline |
| `theta_observation` | `R_n`, apparent-voltage offset/scale, measurement shift | fitted after kinetic lag or with strong constraints |
| `theta_thermal` | temperature dependence of storage, centers, rates, heat-coupling proxy | deferred unless temperature information exists |
| `theta_hysteresis` | branch state, memory variable, path-dependence terms | deferred until earlier residuals fail |

## Stage-Wise Parameter Freedom

| Stage | Fixed | Constrained | Regularized | Free |
|---:|---|---|---|---|
| 0 | all model groups | axes only | none | none |
| 1 | kinetic, observation, thermal, hysteresis | `Q_bg`, capacities | smoothness of equilibrium shape | selected thermodynamic parameters |
| 2 | kinetic, observation, thermal, hysteresis | storage and transition capacity closure | `Q_bg` smoothness/slope | limited storage/capacity corrections |
| 3 | kinetic, observation, thermal, hysteresis | capacity sum, slope floor, root range | widths and peak overlap | transition centers/widths/capacities |
| 4 | observation, thermal, hysteresis | thermodynamic/storage | kinetic priors and rate smoothness | kinetic lag parameters |
| 5 | thermal, hysteresis | thermodynamic/storage/kinetic | `R_n` smoothness and magnitude | selected observation shift terms |
| 6 | hysteresis | all prior groups | thermal smoothness/physical priors | thermal correction terms if data supports them |
| 7 | all prior groups constrained | hysteresis magnitude/domain | memory smoothness | hysteresis terms only after failure diagnosis |

## Degeneracy Controls

| Degeneracy | Failure Mode | Control |
|---|---|---|
| `Q_bg` vs `Q_j,tot` | broad background absorbs peak area or transition capacities absorb baseline storage | capacity closure, slope floor, endpoint constraints, staged storage fit |
| `U_j` vs voltage offset | peak centers move to compensate measurement offset | fix or constrain voltage offset before freeing centers |
| `w_j` vs kinetic broadening | equilibrium width absorbs dynamic lag | fit low-rate thermodynamic widths before kinetic parameters |
| `R_n` vs `k_j` | apparent resistance and kinetic lag both shift dynamic voltage | never fit both freely in same stage; stage or regularize |
| heat shift vs kinetic lag | temperature-driven voltage/rate shifts mimic dynamics | require measured/modelled temperature before thermal parameters |
| hysteresis vs thermodynamic asymmetry | memory terms absorb poor thermodynamic baseline | allow hysteresis only after earlier residuals fail |
| smoothing vs true ICA peaks | preprocessing creates fit targets | record smoothing and compare raw voltage residual |
| closure approximation vs direct solve | fast surrogate hides model failure | compare closure against direct solver before fitting claims |

## Residual Terms

| Residual | Role | Stage Use |
|---|---|---|
| voltage residual `r_V` | compare model apparent voltage to measured voltage | all stages after Stage 1 |
| ICA residual `r_ICA` | compare derivative peak shape/area | Stage 1 onward |
| DVA residual `r_DVA` | compare reciprocal derivative behavior | optional but useful cross-check |
| charge residual `r_G` | enforce charge balance | mandatory all solver/fitting stages |
| capacity closure residual `r_cap` | enforce endpoint/storage consistency | Stage 2 onward |
| state-bound residual `r_xi` | keep states physical | mandatory |
| derivative denominator penalty `r_den` | avoid ICA singularity | derivative stages |
| smoothness penalty `r_smooth` | avoid unphysical background/parameter oscillation | storage, observation, thermal |
| parameter prior `r_prior` | encode physical/domain prior | constrained stages |
| closure mismatch `r_closure` | compare closure to direct solve | any closure-based fitting |

## Objective Function Schematic

A staged objective may be written as

\[
\mathcal{J}
=
w_V\|r_V\|^2
+
w_{\mathrm{ICA}}\|r_{\mathrm{ICA}}\|^2
+
w_{\mathrm{DVA}}\|r_{\mathrm{DVA}}\|^2
+
w_G\|r_G\|^2
+
w_{\mathrm{cap}}\|r_{\mathrm{cap}}\|^2
+
w_{\mathrm{den}}\|r_{\mathrm{den}}\|^2
+
w_{\mathrm{smooth}}\|r_{\mathrm{smooth}}\|^2
+
w_{\mathrm{prior}}\|r_{\mathrm{prior}}\|^2.
\]

Weights are stage-dependent. A residual weight cannot be used to hide a failed hard constraint such as missing charge-balance root, invalid state bounds, or q-domain rest misuse.

## Hard Constraints

| Constraint | Requirement |
|---|---|
| state bounds | \(0\le \xi_j\le 1\) within tolerance |
| capacity closure | endpoint storage and transition capacities must match external capacity window |
| slope floor | \(\partial Q_{\mathrm{bg}}/\partial V\ge\epsilon_Q\) or declared regularization |
| monotonicity | q-grid monotone on q-domain segments; storage function physically conditioned |
| root range | \(V_n\in\mathcal{I}_V\) |
| denominator safety | \(|\mathrm{d}V_{n,\mathrm{app}}/\mathrm{d}q|\ge\epsilon_{dVdq}\) where ICA is evaluated |
| direct solver comparison | closure path must be compared to direct root-solve path |
| no unconstrained `R_n`/`k_j` co-fit | observation and kinetic shift terms cannot both be free in one unconstrained stage |

## Staged Acceptance Criteria

| Stage | Accept If |
|---:|---|
| 0 | units, sign convention, q-grid, and segment labels are consistent |
| 1 | low-rate baseline explains main thermodynamic peak structure without dynamic shifts |
| 2 | charge residual and capacity closure pass |
| 3 | transition parameters improve peak representation without breaking storage constraints |
| 4 | kinetic lag improves rate-dependent residuals and preserves low-rate limit |
| 5 | `R_n` improves apparent-voltage residual without duplicating kinetic lag |
| 6 | thermal correction improves temperature-dependent residuals using actual temperature evidence |
| 7 | hysteresis improves branch residuals only after earlier models are documented insufficient |

## Rejection Criteria

| Rejection | Reason |
|---|---|
| no direct forward trajectory | fitting target has no valid model path |
| charge residual fails | fit violates conservation |
| `Q_bg` absorbs arbitrary peak area | thermodynamic decomposition unidentifiable |
| `R_n` and `k_j` both free without constraints | dynamic voltage shift unidentifiable |
| q-domain dynamics used during rest | invalid state update |
| hysteresis introduced before baseline diagnosis | masks Chapter 1-4 model failure |
| derivative denominator singular without handling | ICA target invalid |
| closure fit lacks direct-solver comparison | approximation not validated |
| only derivative data fit while raw voltage residual fails | shape-only artifact risk |

## Reporting Table For Each Fitting Stage

| Field | Meaning |
|---|---|
| `stage_id` | 0-7 |
| `data_segments_used` | low-rate, high-rate, rest, charge/discharge, temperature |
| `free_parameters` | parameters allowed to move |
| `fixed_parameters` | parameters held fixed |
| `constraints` | active hard constraints |
| `regularizers` | smoothness or prior terms |
| `objective_terms` | residual terms and weights |
| `gate_result` | PASS / WARNING / FAIL |
| `max_abs_r_G` | charge residual |
| `capacity_closure_error` | endpoint/storage error |
| `min_denominator_margin` | ICA/DVA safety |
| `unidentifiable_parameters` | parameters not separable in this stage |
| `deferred_parameters` | moved to later chapter/stage |

## Reporting Unidentifiable, Fixed, And Deferred Parameters

Unidentifiable parameters must be reported as:

```text
parameter: <name>
stage: <stage id>
confounded_with: <parameter or group>
evidence: <residual/diagnostic>
action: fixed | constrained | deferred | requires new data
```

Fixed parameters must state the value/source and why they are fixed. Deferred parameters must name the later phase/chapter that is allowed to revisit them.

## Preventing Later Chapters From Patching Chapter 1 Failure

Chapter 2 heat, Chapter 3 kinetics, Chapter 4 fitting machinery, and Chapter 5 hysteresis cannot be used to hide a failed Chapter 1 charge-balance model. Before later chapters add complexity, the report must show:

- charge-balance residual status;
- root validity and slope-floor status;
- capacity closure status;
- low-rate thermodynamic baseline status;
- whether the failure is structural or data/regime-specific.

If Chapter 1 fails these gates, fix the Chapter 1 model or report the limitation before adding later effects.

## Manuscript Section Outline For Fitting

1. Fitting objective and required data.
2. Forward model dependency on the direct solver.
3. Parameter groups and staged release.
4. Residual terms and hard constraints.
5. Identifiability risks and degeneracy controls.
6. Closure validation requirement.
7. Reporting format and unresolved parameters.
8. Boundary to heat, kinetics, and hysteresis extensions.

## Appendix Candidate For Future Implementation

An appendix may include:

- pseudocode for staged fitting;
- parameter table template;
- JSON schema for fitting configuration;
- synthetic smoke-test example;
- diagnostic plots for residuals and identifiability.

This appendix should be added only after the user requests implementation-level material or after a solver exists.

## Phase 008 Solver Cross-Check

| Requirement From Phase 008 | Phase 009 Use |
|---|---|
| solve `V_n` before evaluating rates | mandatory forward model ordering |
| q-domain update only for nonzero current | fitting segments must label rest |
| charge residual `r_G` | hard constraint/residual |
| state bounds | hard constraint |
| denominator safety | derivative fitting gate |
| closure direct comparison | required before closure-based fitting claims |
| algorithm specified, not executed | Phase 009 also remains protocol-only |

## Phase 010 Forward Dependency

Phase 010 is not complete at this point. Therefore Chapter 2-5 boundaries are a forward dependency:

- thermal correction must wait for Chapter 2 interface boundaries;
- kinetic expansion must wait for Chapter 3 interface boundaries;
- fitting-system assembly must align with Chapter 4 interface boundaries;
- hysteresis/memory must wait for Chapter 5 interface boundaries.

## Source Evidence For Parameter Families

| Parameter Family | Source Evidence |
|---|---|
| `Q_ext`, `q`, `Q_cell` | corrected ver1 lines 95-105; Phase 002 evidence |
| `Q_bg`, `Q_j,tot` | corrected ver1 lines 121-129; Phase 006 charge balance |
| `U_j`, `w_j`, `xi_eq` | corrected ver1 lines 184-201; Phase 006 equilibrium occupancy |
| `V_n`, `V_app`, `V_drive` | corrected ver1 lines 203-237; Phase 006 voltage distinctions |
| `k_j`, `xi` dynamics | corrected ver1 lines 240-286; Phase 006 dynamics |
| rest relaxation | corrected ver1 lines 289-299 |
| ICA/DVA residuals | corrected ver1 lines 353-411; Phase 006 observables |
| closure mismatch | Phase 007 closure contract |
| thermal and hysteresis groups | old ver5 architecture only; later-interface context, not Chapter 1 evidence |

## Synthesis Status For New Fitting Rules

| Rule | Status |
|---|---|
| staged release order | new synthesis from Phase 006-008 constraints |
| no unconstrained `R_n`/`k_j` co-fit | source-supported risk, formalized here |
| `Q_bg` capacity-closure control | source-supported risk, formalized here |
| hysteresis only after residual diagnosis | architecture/scope synthesis |
| reporting table | new synthesis |
| objective function schematic | new synthesis |

## Commands Not Run

| Command / Action | Reason |
|---|---|
| actual fitting | no dataset loaded and Phase 009 is protocol-only |
| parameter optimization | no solver implementation exists |
| uncertainty analysis | requires fitted model and data |
| LaTeX build | final manuscript assembly not yet started |

## Open Issues

| Issue | Status |
|---|---|
| no dataset exists in the rebuild chain | open |
| no solver implementation exists | open |
| parameter priors require user/domain input | open |
| actual data fitting requires user request and data selection | open |
| Phase 010 chapter interface boundaries not yet complete | forward dependency |
| unresolved notation conflict | none newly found beyond Phase 006 open notation risks |

## Gate Statement

Gate: `PASS_REBUILD_V2_FITTING_IDENTIFIABILITY`

This protocol passes because it defines staged fit order, parameter groups, group freedom by stage, degeneracy controls, residuals, objective function, hard constraints, staged acceptance/rejection criteria, reporting tables, direct-solver dependency, and non-execution boundaries.
