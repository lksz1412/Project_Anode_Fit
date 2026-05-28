# ver1 Charge-Balance Dependency Graph

Source:
`D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_charge_balance_ver1_rechecked2.tex`

Created: 2026-05-27

Phase: 003

## Read Coverage

| Source | Required Range | Actual Range Read | Status | Notes |
|---|---:|---:|---|---|
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | 1-495 | 1-150, 151-300, 301-495 | READ_FULL | First line `\documentclass...`; last line `\end{document}`; heading/label scan cross-checked |

## Core Finding

The corrected ver.1 file changes the foundation from "read voltage from an OCV function of q" to "solve internal graphite potential from charge balance."

The central equation is:

```tex
Q_{\cell}q=Q_{\bg}(V_n,T)+\sum_{j=1}^{N_p}Q_{j,\tot}\xi_j.
```

Evidence: lines 121-127.

This creates a coupled implicit system:

```text
q, T, xi_j
  -> charge balance solve
  -> V_n
  -> xi_eq(V_n,T), V_app, V_drive, A_j, k_j
  -> dxi_j/dt or dxi_j/dq
  -> updated xi_j
  -> charge balance solve again
```

This is not automatically a logical contradiction. It is a differential-algebraic / self-consistent formulation. The current logical gap is that the document defines the feedback structure but does not yet specify a solver or integral-equation method for the feedback loop. Phase 004-005 should fill this gap using the user's JCP paper refs. 6 and 7.

## Variable Inventory

| Symbol | Meaning | Defined At | Used At | Independent / Dependent Status | Unit / Domain | Notes |
|---|---|---:|---:|---|---|---|
| `q` | discharge progress coordinate | 74, 100-105 | 121-145, 279-286, 353-411 | independent state / coordinate | dimensionless | `q=Q_ext/Q_cell`; increases in discharge direction |
| `Q_{\ext}` | external charge passed through circuit | 75, 95-101 | 51-60, 394-411 | measured/input-derived | C | final ICA/DVA uses `Q_ext`, not modeled `Q_n` |
| `Q_{\cell}` | reference cell capacity | 76, 88-93 | 121-145, 164-174, 279-286, 394-411 | fixed scale parameter | C | must be in coulomb; Ah conversion line 91 |
| `V_n` | internal anode potential solved from charge balance | 77, 118-129 | 148-162, 184-201, 203-299, 353-391 | algebraic unknown | V vs Li/Li+ implied | not an externally prescribed `V_n(q)` |
| `V_{n,\app}` | apparent measured anode potential | 78, 217-222 | 379-411, 421-430 | dependent observation | V | `V_n + s_I |I| R_n` |
| `V_{n,\drive}` | driving potential for kinetic rate | 79, 203-237 | 224-237, 245-264 | model-choice dependent | V | may be approximated by `V_{n,\app}` with double-counting warning |
| `R_n(q,T,|I|)` | effective resistance/polarization coefficient | 80, 217-222 | 217-237, 379-391, 421-430 | fitted or externally constrained function | Ohm-like effective coefficient | must not be freely co-fit with `k_j` without constraints |
| `\xi_j` | actual progress of transition j | 81, 109-117 | 121-145, 268-318, 320-349, 353-377 | dynamic state | [0,1] intended | feeds charge balance and is updated by ODE |
| `\xi_{j,\mathrm{eq}}` | equilibrium progress of transition j | 82, 148-162, 184-201 | 268-299, 314-318, 320-349 | dependent target function | [0,1] intended | depends on solved `V_n` |
| `Q_{j,\tot}` | capacity contribution of transition j | 83, 112-114 | 121-145, 164-174, 353-377, 449-460 | fitted parameter | C | constrained by total capacity and monotonicity |
| `Q_{\bg}(V_n,T)` | background/chemical capacitance reservoir | 84, 118-129 | 121-182, 353-377 | fitted function / algebraic storage term | C | must have positive slope floor |
| `U_j(T)` | transition center potential | 190-194 | 224-227, 240-264, 439-447 | fitted/temperature-dependent parameter | V | appears in equilibrium and driving force |
| `w_j(T)` | equilibrium transition width | 190-194 | 190-201, 439-460 | fitted/temperature-dependent parameter | V | distinct from ver5 heat-layer `w_j=Q_j/Q_cell` collision |
| `s_{\xi,j}` | optional equilibrium direction sign | 197-201 | 197-201 | optional extension | +/-1 | default fixed to +1 in ver.1 |
| `s_I` | current/sign convention for apparent voltage | 217-222 | 379-391, 421-430 | convention parameter | +/-1 | discharge apparent-voltage convention usually +1 |
| `s_{\phi,j}` | sign for transformation driving force | 224-227 | 224-237, 245-264 | convention/transition parameter | +/-1 | separate from `s_I` |
| `\mathcal A_j` | driving affinity | 224-227 | 245-264, 328-339 | dependent kinetic quantity | J/mol-like via F*V | built from driving potential |
| `\Delta G_{a,j}` | intrinsic activation free energy | 240-244 | 245-264 | fitted/temperature dependent | energy/mol | `Delta H - T Delta S` |
| `\Delta G_{\eff,j}` | effective barrier | 245-248 | 255-264 | dependent kinetic quantity | energy/mol | regularized by softplus barrier |
| `\Delta G_{\eff,j}^{+}` | regularized positive barrier | 255-266 | 260-264 | numerical regularization | energy/mol | not a new physical barrier |
| `k_j` | transition relaxation rate | 250-265 | 268-299, 414-419, 462-471 | dependent kinetic rate | 1/s | depends on `V_n`, q, T, I through driving path |
| `g` | kinetic activation barrier for domain | 320-339 | 320-349 | distributed internal coordinate | energy/mol | support restricted to `g>=0` |
| `\rho_j(g)` | kinetic barrier distribution | 320-326 | 345-349 | distribution function | normalized on [0,inf) | not equilibrium potential distribution |
| `T` | temperature | many | many | input/state | K | appears in charge balance, rates, and derivatives |
| `I` | current magnitude | 88-105 | 217-237, 279-299, 379-430 | input | A = C/s | q-coordinate ODE invalid at rest |

## Dependency Graph

| Node | Defined At | Depends On | Used By | Status | Issue Type | Evidence |
|---|---|---|---|---|---|---|
| `q` | 95-105 | `Q_ext`, `Q_cell` | charge balance, ODE q form, ICA/DVA | 확정 | none | lines 95-106 |
| `Q_ext` | 95-101 | `I(t)` integral | `q`, final ICA/DVA | 확정 | none | lines 95-101, 394-411 |
| `V_n` | 121-127 | `q`, `T`, `\xi_j`, `Q_bg`, `Q_j_tot` | `xi_eq`, `V_app`, `V_drive`, `k_j`, ICA/DVA | 확정 | algebraic implicit solve | lines 121-129 |
| `Q_bg(V_n,T)` | 121-129 | `V_n`, `T`, fitted background function | charge balance, `dV_n/dq`, capacity consistency | 확정 | inversion/conditioning risk | lines 121-145, 176-182 |
| `xi_eq(V_n,T)` | 148-162, 184-201 | `V_n`, `T`, `U_j`, `w_j` | progress ODE, equilibrium OCV | 확정 | implicit coupling through `V_n` | lines 150-162, 184-201 |
| `V_app` | 217-222 | `V_n`, `I`, `R_n`, `s_I` | observation, optional drive approximation, ICA/DVA | 확정 | double-count risk with `k_j` | lines 217-237, 379-391 |
| `V_drive` | 224-237 | model choice; often `V_app` | `A_j` | 확정 | approximation / double-count risk | lines 224-237 |
| `A_j` | 224-227 | `V_drive`, `U_j`, `s_phi`, `F` | `Delta G_eff` | 확정 | none by itself | lines 224-227 |
| `Delta G_eff` | 245-248 | `Delta G_a`, `chi_j`, `A_j` | `Delta G_eff+`, `k_j` | 확정 | runaway if negative without regularization | lines 245-266 |
| `k_j` | 250-265 | `Delta G_eff+`, `T`, `nu_j` | `dxi/dt`, `dxi/dq` | 확정 | coupled rate via `V_n`/`V_drive` | lines 250-265, 268-286 |
| `xi_j` | 109-117, 268-318 | previous `xi_j`, `k_j`, `xi_eq`, initial condition | charge balance, capacity, derivative equations | 확정 | dynamic feedback state | lines 112-117, 271-286, 301-318 |
| `dxi_j/dq` | 279-286 | `Q_cell`, `I`, `k_j(V_n,...)`, `xi_eq(V_n,T)`, `xi_j` | `dV_n/dq`, monotonicity, heat handoff | 확정 | coupled DAE derivative | lines 279-286, 353-377 |
| `dV_n/dq` | 353-367 | `Q_cell`, `dQ_bg/dV`, `dQ_bg/dT`, `dT/dq`, `dxi_j/dq` | `dV_app/dq`, ICA/DVA | 확정 | derivative-level feedback | lines 353-367 |
| `dV_app/dq` | 379-391 | `dV_n/dq`, derivatives of `R_n` | ICA/DVA | 확정 | observation derivative dependency | lines 379-391 |
| `dQ_ext/dV_app` | 394-405 | `Q_cell`, `dV_app/dq` | ICA observable | 확정 | denominator singularity risk | lines 394-405 |
| `dV_app/dQ_ext` | 407-411 | `Q_cell`, `dV_app/dq` | DVA observable | 확정 | none beyond `dV_app/dq` | lines 407-411 |
| `xi_j(g,t)` | 320-349 | `g`, `k_j(g)`, `xi_eq(V_n,T)` | distributed `xi_j(t)` | 확정 | distributed feedback state | lines 320-349 |

## Feedback Loop Classification

### Loop 1 - Main Dynamic Charge-Balance Loop

| Field | Description |
|---|---|
| Evidence | charge balance lines 121-129; equilibrium progress lines 184-201; rate lines 250-265; ODE lines 268-286 |
| Loop | `xi_j -> charge_balance -> V_n -> xi_eq/k_j -> dxi_j/dt or dxi_j/dq -> xi_j` |
| Classification | `definition-level implicit system` + `수치해법 필요` |
| Logical Status | Not a contradiction by itself; it is a differential-algebraic self-consistent system |
| Missing Piece | explicit solution/integration method for the algebraic `V_n` solve coupled to the progress ODE |
| Candidate Fix Location | Phase 004-005, using refs. 6 and 7 method extraction |

### Loop 2 - Equilibrium OCV Inversion

| Field | Description |
|---|---|
| Evidence | equilibrium condition lines 148-162 |
| Loop | `V_n -> xi_eq(V_n,T)` and `V_n -> Q_bg(V_n,T)`, both inside `Q_cell q = Q_bg + sum Q_j xi_eq` |
| Classification | `implicit scalar inversion` |
| Logical Status | Valid if monotonic/range conditions hold |
| Existing Safeguards | range condition lines 131-146; slope floor lines 176-182 |
| Missing Piece | numerical inversion method and branch selection if multiple roots appear |

### Loop 3 - Rest Relaxation Loop

| Field | Description |
|---|---|
| Evidence | rest section lines 289-299 |
| Loop | at fixed `q`, `xi_j(t)` relaxes; charge balance must be re-solved for `V_n(t)` at every time |
| Classification | `time-domain algebraic re-solve` |
| Logical Status | Valid DAE rest-relaxation interpretation |
| Missing Piece | solver ordering/timestep rule |

### Loop 4 - Derivative / ICA Loop

| Field | Description |
|---|---|
| Evidence | `dxi/dq` lines 279-286; `dV_n/dq` lines 353-367; ICA/DVA lines 394-411 |
| Loop | `dV_n/dq` depends on `dxi_j/dq`; `dxi_j/dq` depends on `V_n`; `V_n` is solved from charge balance |
| Classification | `coupled derivative evaluation` |
| Logical Status | Valid if evaluated after the algebraic state solve at each q/time point |
| Existing Safeguards | `dQ_bg/dV_n` slope floor lines 176-182; monotonicity constraint lines 370-377 |
| Missing Piece | explicit algorithm distinguishing state solve, derivative evaluation, and observable calculation |

### Loop 5 - Distributed Barrier Loop

| Field | Description |
|---|---|
| Evidence | distributed barrier section lines 320-349 |
| Loop | `xi_j(g,t)` depends on `xi_eq(V_n,T)` and `k_j(g)`; averaged `xi_j` re-enters charge balance |
| Classification | `distributed-state self-consistent DAE` |
| Logical Status | Valid extension but numerically larger |
| Existing Safeguards | `rho_j(g)` support/normalization lines 320-326 |
| Missing Piece | discretization/quadrature and coupled solver method |

## Comparison To ver5 Historical Chapter 1

| Topic | Historical ver5 Chapter 1 | Rechecked ver1 | Consequence |
|---|---|---|---|
| Voltage source | `V_{n,\OCV}(q,T)` treated as a basis function in old ver.1 | `V_n` solved from charge balance | Final Chapter 1 should be rebuilt from rechecked ver1 |
| Capacity derivative | old ver.1 uses modeled `Q_n(q)` and `dQ_n/dq` | rechecked ver1 uses external `Q_ext=Q_cell q` for ICA/DVA | Downstream interfaces must distinguish modeled internal storage from external charge |
| Core equation | progress-dynamics spine | charge-balance algebraic solve plus progress dynamics | Chapter 2-5 must receive `V_n` and `V_app` from charge-balance solve |
| Main risk | notation/identifiability | implicit feedback solver missing | ref. 6/7 method should attach to this point |

## Interface Equations For Later Chapters

These equations should be treated as Chapter 1 interface candidates for Chapter 2-5:

| Interface | Evidence | Purpose |
|---|---:|---|
| `Q_cell q = Q_bg(V_n,T)+sum Q_j xi_j` | 121-127 | algebraic internal-potential solve |
| range / existence condition | 131-146 | admissible state/parameter constraint |
| OCV implicit equation | 148-162 | equilibrium voltage as charge-balance solution |
| total-capacity consistency | 164-174 | parameter constraint |
| background slope floor | 176-182 | numerical stability |
| `xi_eq(V_n,T)` logistic/signed form | 184-201 | equilibrium target |
| `V_app = V_n+s_I|I|R_n` | 217-222 | observable voltage |
| `A_j=s_phi F(V_drive-U_j)` and `V_drive approx V_app` | 224-237 | kinetic driving force |
| softplus barrier and `k_j` | 240-266 | bounded kinetic rate |
| `dxi_j/dt` | 268-276 | time-domain progress dynamics |
| `dxi_j/dq` | 279-286 | constant-current q-domain dynamics |
| rest-relaxation re-solve | 289-299 | rest voltage relaxation |
| barrier distribution | 320-349 | optional distributed kinetics |
| `dV_n/dq` general/isothermal | 353-367 | voltage derivative from charge balance |
| monotonicity constraint | 370-377 | physical/numerical constraint |
| `dV_app/dq` | 379-391 | apparent voltage derivative |
| ICA/DVA final | 394-411 | observables based on `Q_ext` |
| ver.2 handoff `dxi_j/dt` | 462-471 | heat-layer input |

## Required Method Development

The next mathematical development must supply at least:

1. An algebraic root solve for `V_n` at given `(q,T,xi_j)`.
2. A time or q integration scheme for `xi_j`.
3. A consistent order:
   state -> solve `V_n` -> compute `xi_eq`, `V_app`, `V_drive`, `k_j` -> update `xi_j` -> recompute `V_n`.
4. A method for the distributed case:
   discretize `g`, evolve `xi_j(g)`, integrate to `xi_j`, solve charge balance.
5. A rule for equilibrium OCV:
   solve the implicit equation with `xi_j=xi_eq(V_n,T)`.
6. A check for root existence, slope floor, monotonicity, and denominator singularities in ICA.

Refs. 6 and 7 from the user's JCP paper are expected to contribute here if they contain a self-consistent integral-equation solution method.
