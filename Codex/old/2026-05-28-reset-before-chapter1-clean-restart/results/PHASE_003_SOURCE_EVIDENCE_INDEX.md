# Phase 003 — Source Evidence Extraction Result

## Summary

This phase extracts source-grounded evidence for the corrected Chapter 1 direction: graphite LIB ICA peak-tail behavior should be derived from charge balance, internal potential, present-potential-assisted effective barrier lowering, relaxation in charge coordinate, and ICA/DVA observable mapping.

The active foundation is `graphite_ica_charge_balance_ver1_rechecked2.tex` because it closes the feedback loop by solving `V_n` from charge balance and separates `V_n`, `V_{n,\app}`, and `V_{n,\drive}`. The historical `graphite_ica_dynamic_ver5.tex` remains useful for the kinetic spine and later chapter structure, but its older shortcuts must not override the corrected charge-balance formulation.

Gate result: `PASS_SOURCE_EVIDENCE_INDEX`

## Step Range

Planned steps: 27-42

Actual steps completed: 27-42

## Inputs

| Input | Coverage basis |
|---|---|
| `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_dynamic_ver5.tex` | Phase 002 `READ_FULL`, lines 1-1974 |
| `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_charge_balance_ver1_rechecked2.tex` | Phase 002 `READ_FULL`, lines 1-495 |

## Classification Legend

| Class | Meaning |
|---|---|
| `core` | May enter Chapter 1 main derivation directly if notation is made consistent |
| `extension` | Useful after the single-barrier logic is complete |
| `warning` | Constraint or failure mode that must be visible in the derivation/audit |
| `reject` | Do not use as Chapter 1 core logic |
| `future chapter` | Relevant to later chapter structure, not Chapter 1 body |

## Core Evidence Index

| Topic | Class | Source lines | Extracted content | Chapter 1 use |
|---|---|---|---|---|
| Kinetic spine from barrier to ICA/DVA | `core` | `graphite_ica_dynamic_ver5.tex:55`, `65-79` | Tail is explained by phase-progress dynamics; the spine is `Delta G_eff -> k_j -> dxi/dt -> xi(q) -> dxi/dq -> dQ/dV,dV/dQ`. | Use as the high-level derivation order, but rebuild the equations from the corrected charge-balance source. |
| Charge-balance spine | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:48-65` | The intended flow is `Q_ext=Q_cell q -> Q_ext=Q_bg(V_n,T)+sum Q_j xi_j -> V_n -> V_app -> dQ/dV,dV/dQ`; barrier-threshold completion is explicitly rejected. | Use as the Chapter 1 architecture and scope guard. |
| Charge coordinate | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:95-106` | `Q_ext(t)=int |I|dt`, `q=Q_ext/Q_cell`, and at constant current `dq/dt=|I|/Q_cell`. | Required before converting time dynamics to `q` dynamics and deriving tail length. |
| Internal potential closure | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:118-129` | `Q_cell q=Q_bg(V_n,T)+sum_j Q_{j,tot} xi_j`; `V_n` is not independently prescribed but solved from the charge-balance equation. | This closes the self-consistent feedback loop. Every later `V_n` dependence must point back to this algebraic equation. |
| Equilibrium progress | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:184-201` | `xi_{j,eq}=xi_{j,eq}(V_n,T)`; logistic example with center `U_j(T)` and width `w_j(T)`; default direction sign is `s_xi=+1`. | Equilibrium peak shape is defined through internal potential, not through an externally guessed Gaussian peak. |
| Voltage role separation | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:203-238` | `V_n` is internal charge-balance potential, `V_{n,\app}` is measured apparent potential, `V_{n,\drive}` is rate-driving voltage; reduced model may use `V_{n,\drive}\approx V_{n,\app}` only with restrictions. | Prevents circular or double-counted use of apparent voltage in both equilibrium and kinetics. |
| Affinity / driving work | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:224-233`; `graphite_ica_dynamic_ver5.tex:871-888` | `A_j=s_{\phi,j}F[V_{n,\drive}-U_j(T)]`; later version also notes `A_j=F eta_j`. | Define the present-potential assistance term. `F * voltage` has energy-per-mole units, so it can modify an activation free energy. |
| Intrinsic activation free energy | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:240-244`; `graphite_ica_dynamic_ver5.tex:203-210` | `Delta G_{a,j}(T)=Delta H_{a,j}-T Delta S_{a,j}`. | This is the thermal barrier baseline before potential assistance. |
| Effective barrier | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:245-249`; `graphite_ica_dynamic_ver5.tex:220-226` | `Delta G_eff,j=Delta G_a,j(T)-chi_j A_j`. | Main hypothesis: favorable present electrode potential lowers the effective barrier. |
| Positive barrier handling | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:250-266`; `graphite_ica_dynamic_ver5.tex:236-250` | Direct Arrhenius extrapolation can make `k_j>nu_j`; corrected source uses softplus `Delta G_eff^+` and states `epsilon_G` is numerical regularization. | Use softplus or an explicitly bounded positive barrier in the manuscript; do not treat `epsilon_G` as a new physical barrier. |
| Single-barrier rate | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:259-265` | `k_j=nu_j(T) exp[-Delta G_eff,j^+/(RT)]`. | Converts effective barrier into the relaxation rate that controls tail length. |
| Relaxation dynamics in time | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:268-277`; `graphite_ica_dynamic_ver5.tex:252-261` | `dxi_j/dt=k_j(...)[xi_{j,eq}(V_n,T)-xi_j]`; lag creates tail and broadening. | Starting point for tail residual equation. |
| Relaxation dynamics in charge coordinate | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:279-286`; `graphite_ica_dynamic_ver5.tex:263-274` | `dxi_j/dq=(Q_cell/|I|) k_j(...)[xi_{j,eq}-xi_j]`. | Direct basis for deriving `ell_q,j=|I|/(Q_cell k_j)` under a local tail approximation. |
| ICA/DVA mapping | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:353-412` | Differentiate charge balance, derive `dV_n/dq`, then `dV_app/dq`, then `dQ_ext/dV_app=Q_cell/(dV_app/dq)` and `dV_app/dQ_ext=(1/Q_cell)dV_app/dq`. | Maps the kinetic tail term `dxi/dq` into the observable ICA/DVA curves without replacing physics by empirical peaks. |
| C-rate competition | `core` | `graphite_ica_charge_balance_ver1_rechecked2.tex:414-418`; `graphite_ica_dynamic_ver5.tex:277-284` | Larger `|I|` shortens residence time, while changed `V_drive`/`A_j` can increase `k_j`; in `q` coordinates `dxi/dq ∝ k_j(I)/|I|`. | Required to avoid the false rule “higher current always lengthens tail” or “higher drive always shortens tail.” |

## Extension Evidence

| Topic | Class | Source lines | Extracted content | Use condition |
|---|---|---|---|---|
| Kinetic barrier distribution | `extension` | `graphite_ica_charge_balance_ver1_rechecked2.tex:320-350` | `rho_j(g)` is a kinetic activation barrier distribution with support `g>=0`; each `g` group relaxes with its own `k_j(g)`, and `xi_j(t)=int_0^infty rho_j(g) xi_j(g,t) dg`. | Use after the single-barrier tail derivation if one relaxation scale is insufficient. |
| Older barrier distribution in ver5 | `warning` | `graphite_ica_dynamic_ver5.tex:286-323` | The older form integrates `rho_j(g)` from `-infty` to `infty`. It also correctly states that high-barrier groups follow slowly and create long tails. | Keep the physical interpretation, but replace support with the corrected `g>=0` form from `rechecked2`. |
| Forward/backward rates | `extension` | `graphite_ica_dynamic_ver5.tex:977-1008` | Reversible phase transition can be written as `dxi/dt=k^+(1-xi)-k^-xi`, which reduces to relaxation form with `xi_eq=k^+/(k^++k^-)` and `k_relax=k^++k^-`. | Useful for a later refinement or appendix; not necessary for the main Chapter 1 tail-scale derivation. |
| Butler-Volmer / overpotential form | `extension` | `graphite_ica_dynamic_ver5.tex:857-894` | Later chapter separates equilibrium position from kinetic speed and allows `A_j=F eta_j`. | Do not import as core unless `R_n` and BV components are explicitly separated. |
| Temperature-dependent `i0` and `nu` | `extension` | `graphite_ica_dynamic_ver5.tex:963-975` | `i0(T)` and `nu_j(T)` may increase with temperature; they are identifiable only under constraints. | Use qualitatively in low-T/high-T tail explanation; reserve detailed electrochemical kinetics for future chapters. |

## Warning / Failure-Mode Evidence

| Warning | Source lines | Meaning for new derivation |
|---|---|---|
| `R_n` and `k_j` double counting | `graphite_ica_charge_balance_ver1_rechecked2.tex:236-238`, `439-458`; `graphite_ica_dynamic_ver5.tex:891-894`, `1461-1464` | If `V_{n,\drive}\approx V_{n,\app}` is used, `R_n` must not freely explain the same broadening/tail that `k_j` explains. |
| Equilibrium location and kinetic speed must stay separated | `graphite_ica_dynamic_ver5.tex:857-869`, `1461` | `xi_eq` determines where the equilibrium transition wants to be; `A_j`/`k_j` determines how fast the phase catches up. |
| `rho_j(g)` is not an equilibrium center distribution | `graphite_ica_charge_balance_ver1_rechecked2.tex:320-326` | Kinetic activation barrier distribution must not be confused with distributions of `U_j`, `w_j`, or `p_j(U)`. |
| `epsilon_G` is not a physical barrier | `graphite_ica_charge_balance_ver1_rechecked2.tex:254-266`, `487-488` | Softplus is a reduced-model regularizer; the physics remains intrinsic thermal barrier plus potential assistance. |
| Prefactor-barrier identifiability | `graphite_ica_charge_balance_ver1_rechecked2.tex:455-457`; `graphite_ica_dynamic_ver5.tex:963-975` | Later fitting must constrain `nu`, `Delta G_a`, `chi`, `R_n`, and `w_j`; Chapter 1 should not pretend they are independently identifiable from one curve. |

## Rejected Or Future-Chapter Material For Chapter 1 Core

| Material | Class | Source lines | Reason |
|---|---|---|---|
| Empirical EMG peak as main model | `reject` | `graphite_ica_charge_balance_ver1_rechecked2.tex:432-437` | EMG can generate initial values or comparisons, but the source states the dynamic tail comes from `k_j`, `rho(g)`, `R_n`, and charge balance. |
| Peak-area-first explanation | `reject` | User restart statement and scope-drift rule in active plan | Peak area is later fitting/capacity decomposition; the current logic target is tail behavior and effective barrier. |
| Solver/fitting implementation | `reject` | Active plan non-goals | The requested output is theoretical derivation, not numerical fitting code. |
| Branch hysteresis mechanics | `future chapter` | `graphite_ica_dynamic_ver5.tex:1844-1863` | Branch tail length observations can support future validation, but Chapter 1 should not depend on branch/hysteresis state variables. |
| Heat-layer coupling as Chapter 1 body | `future chapter` | `graphite_ica_charge_balance_ver1_rechecked2.tex:462-471`; plan non-goals | Heat terms need `dxi/dt`, but Chapter 1 first needs the tail/effective-barrier derivation. |

## Source-To-Claim Direction Decision

The rebuilt Chapter 1 should use this evidence order:

1. Define `Q_ext`, `q`, and constant-current conversion from `t` to `q`.
2. Define charge balance and solve `V_n` implicitly from `Q_cell q=Q_bg(V_n,T)+sum Q_j xi_j`.
3. Define `xi_{j,eq}(V_n,T)` as the equilibrium target, not an empirical peak curve.
4. Separate `V_n`, `V_{n,\app}`, and `V_{n,\drive}` before defining affinity.
5. Define `A_j=s_{\phi,j}F[V_{n,\drive}-U_j(T)]`.
6. Define thermal intrinsic barrier `Delta G_a,j(T)=Delta H_a,j-T Delta S_a,j`.
7. Define potential-assisted barrier `Delta G_eff,j=Delta G_a,j(T)-chi_j A_j`.
8. Apply positive-barrier handling to form `Delta G_eff,j^+`.
9. Define `k_j=nu_j(T) exp[-Delta G_eff,j^+/(RT)]`.
10. Derive `dxi_j/dq=(Q_cell/|I|)k_j[xi_{j,eq}-xi_j]`.
11. Derive the local tail residual and tail scale in Phase 008.
12. Map `dxi_j/dq` into ICA/DVA through the differentiated charge balance in Phase 009.

This direction is consistent with the user's corrected observation:

- low temperature produces longer tails because the exponential factor and possibly `nu_j(T)` reduce `k_j`;
- high temperature shortens tails because `RT` and kinetic prefactors make relaxation faster;
- present electrode potential can shorten or reshape the tail when favorable `A_j` lowers `Delta G_eff,j^+`;
- a simple equilibrium Gaussian/logistic broadening alone cannot explain an asymmetric finite-rate lag tail.

## Validation

| Check | Result | Evidence |
|---|---|---|
| Main kinetic spine extracted | PASS | `graphite_ica_dynamic_ver5.tex:55`, `65-79` |
| Charge balance and internal `V_n` extracted | PASS | `graphite_ica_charge_balance_ver1_rechecked2.tex:118-129` |
| Voltage role separation extracted | PASS | `graphite_ica_charge_balance_ver1_rechecked2.tex:203-238` |
| Equilibrium progress extracted | PASS | `graphite_ica_charge_balance_ver1_rechecked2.tex:184-201` |
| `Delta G_a`, `A_j`, `Delta G_eff`, `Delta G_eff^+`, `k_j` extracted | PASS | `graphite_ica_charge_balance_ver1_rechecked2.tex:224-266` |
| `dxi/dt` and `dxi/dq` extracted | PASS | `graphite_ica_charge_balance_ver1_rechecked2.tex:268-286` |
| Barrier distribution extracted and corrected-source priority marked | PASS | `graphite_ica_charge_balance_ver1_rechecked2.tex:320-350` |
| ICA/DVA mapping extracted | PASS | `graphite_ica_charge_balance_ver1_rechecked2.tex:353-412` |
| Double-counting / identifiability warnings extracted | PASS | `graphite_ica_charge_balance_ver1_rechecked2.tex:236-238`, `439-458`; `graphite_ica_dynamic_ver5.tex:891-894`, `1461-1464` |
| Peak-area / EMG / solver drift excluded from Chapter 1 core | PASS | `graphite_ica_charge_balance_ver1_rechecked2.tex:432-437`; active plan non-goals |

## Gate

Gate: `PASS_SOURCE_EVIDENCE_INDEX`

Status: PASS

Reason:

- every Chapter 1 core equation needed for the planned derivation has a source line reference;
- corrected `rechecked2` lines are prioritized where older `ver5` shortcuts conflict;
- out-of-scope fitting, solver, branch, heat, and peak-area material is explicitly classified outside Chapter 1 core.

## Confirmed Non-Changes

- No original `.tex` source file was modified.
- No PDF was modified.
- `D:\Projects\Project_Anode_Fit\Claude` was not modified.
- No commit, push, merge, or branch operation was performed.

## Open Issues / Decision Queue

| Issue | Status |
|---|---|
| PDF ref. 6/7 method has not yet been checked in the current restart chain | pending Phase 004 |
| Whether ref. 6/7 belongs in Chapter 1 main text or only an implicit-method note is undecided | pending Phase 004 |
| Tail scale `ell_q,j` has not yet been derived in the restart chain | pending Phase 008 |

No user decision is required before Phase 004.

## Next

Proceed directly to Phase 004 — PDF Ref. 6/7 Method Extraction.
