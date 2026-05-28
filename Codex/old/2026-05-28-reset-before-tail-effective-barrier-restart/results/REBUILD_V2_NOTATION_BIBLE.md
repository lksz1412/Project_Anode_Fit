# Rebuild v2 Notation Bible

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 005 - Notation And Equation Dependency Contract`

Created: 2026-05-27

## Purpose

This notation bible fixes the symbol roles before manuscript drafting. It prevents the old circular logic by requiring measured variables to be defined first, the charge-balance residual second, and `V_n` only as the solved root of that residual.

## Core Ordering Rule

1. Define measured variables.
2. Define internal states and storage functions using a dummy voltage argument `V`.
3. Define the charge-balance residual `G`.
4. Define the root operator `mathcal V`.
5. Define `V_n` only through the root operator.
6. Define equilibrium OCV only as a special root.
7. Define apparent/driving voltages and kinetic rates.
8. Define dynamics, derivatives, ICA, and DVA.
9. Define approximations or closure strategies only after the exact formulation.

## Measured Variables

| Symbol | Role | Unit | Domain | Defined Before | Notes |
|---|---|---|---|---|---|
| `t` | time coordinate | s | analysis interval | all dynamic quantities | Independent time coordinate. |
| `I(t)` | applied current with sign convention | A | measured profile | `Q_ext`, rate conversion | Sign convention must be stated before use. |
| `I_abs(t)=abs(I(t))` | current magnitude | A | nonnegative | charge-domain conversion | Use only when orientation is handled separately. |
| `Q_ext(t)` | external charge passed through circuit | C | nonnegative over selected charge/discharge segment | `q`, ICA/DVA | Defined by time integral of measured current magnitude or signed convention chosen by user. |
| `Q_cell` | reference cell capacity | C | positive scalar | `q`, capacity normalization | If source is Ah, convert by `Q_cell[C]=3600 Q_cell[Ah]`. |
| `q` | normalized external charge, `Q_ext/Q_cell` | dimensionless | analysis window, usually `[0,1]` after normalization | all model equations using external coordinate | Reserved for measured external charge coordinate, not an internal state. |
| `T(t)` or `T(q)` | temperature | K | measured or modeled thermal path | storage, equilibrium, kinetics | Chapter 1 treats it as input unless heat coupling is later activated. |

## Internal States And Storage

| Symbol | Role | Unit | Domain | Defined Before | Notes |
|---|---|---|---|---|---|
| `j` | staging transition index | dimensionless | `1,...,N_p` | transition sums | Index only. |
| `N_p` | number of transition populations | dimensionless | positive integer | transition sums | Chosen by model order/fitting protocol. |
| `xi_j` | internal progress/state of transition `j` | dimensionless | typically `[0,1]` | charge balance, dynamics | Internal state, not the measured charge coordinate. |
| `xi` or `bold xi` | vector of all `xi_j` | dimensionless | product of state domains | charge balance root | Use consistently after notation bible. |
| `V` | dummy voltage argument | V | admissible graphite voltage interval | `xi_eq`, `Q_bg`, `G` | Dummy variable only; not yet the solved `V_n`. |
| `xi_{j,eq}(V,T)` | equilibrium occupancy as a function of dummy voltage and temperature | dimensionless | `[0,1]` | equilibrium OCV, dynamics | May use logistic or other monotone form; do not write `xi_eq(V_n,T)` before `V_n` is defined. |
| `Q_bg(V,T)` | background storage contribution | C | differentiable storage function | `G`, implicit derivative | Storage term, not a cosmetic baseline. |
| `Q_{j,tot}` | capacity carried by transition `j` | C | nonnegative | charge balance | Transition capacity scale. |
| `a_j` | dimensionless capacity fraction, `Q_{j,tot}/Q_cell` | dimensionless | nonnegative | normalized forms | Use `a_j` instead of reusing `w_j`. |
| `U_j(T)` | transition center potential | V | temperature-dependent scalar/function | `xi_{j,eq}`, affinity | Center for transition `j`. |
| `w_j(T)` | transition voltage width | V | positive | `xi_{j,eq}` | Reserved only for voltage width. Never use for capacity fraction. |
| `s_{xi,j}` | occupancy orientation sign | dimensionless | `+1` or `-1` | `xi_{j,eq}` | Must match charge/discharge convention. |
| `theta` | model parameter set | mixed | declared per model | `G`, rates, fitting | Do not hide measured variables inside `theta`. |

## Charge-Balance Root

| Symbol | Role | Unit | Domain | Defined Before | Notes |
|---|---|---|---|---|---|
| `G(V;q,T,xi,theta)` | charge-balance residual | C | function over admissible `V` | root operator | Preferred sign: storage minus external charge. |
| `mathcal V(q,T,xi;theta)` | root operator mapping state and measured coordinate to internal potential | V | admissible voltage interval | `V_n`, `V_OCV`, rates | Defined by `G(mathcal V; q,T,xi,theta)=0`. |
| `V_n` | solved internal graphite potential | V | admissible root of `G=0` | `V_app`, `V_drive`, rates, derivatives | Never prescribed independently. It exists only after `mathcal V` is defined. |
| `V_{n,OCV}(q,T)` | equilibrium OCV special root | V | equilibrium state path | OCV discussion only | Derived by setting `xi_j=xi_{j,eq}(V,T)` inside charge balance. Not the primary dynamic input. |

## Apparent, Driving, And Kinetic Quantities

| Symbol | Role | Unit | Domain | Defined Before | Notes |
|---|---|---|---|---|---|
| `V_{n,app}` | apparent voltage used for observation | V | model output path | ICA/DVA | May include ohmic or apparent shift from `V_n`. |
| `R_n(q,T,I_abs)` | apparent resistance/shift factor | ohm or V/A equivalent | constrained nonnegative or signed by model | `V_app` if used | Must not be unconstrained together with kinetic shift absorbers. |
| `s_I` | current-orientation sign in apparent shift | dimensionless | `+1` or `-1` | `V_app` | Define from charge/discharge convention. |
| `V_{n,drive}` | driving voltage used for kinetic affinity | V | declared model choice | affinity, rates | May equal `V_app` only by explicit approximation. |
| `A_j` or `mathcal A_j` | kinetic affinity for transition `j` | J/mol or C V per mol depending convention | real scalar | `k_j` | Use one notation consistently. |
| `s_{phi,j}` | affinity orientation sign | dimensionless | `+1` or `-1` | affinity | Must be coordinated with `s_{xi,j}`. |
| `F` | Faraday constant | C/mol | positive constant | affinity if electrochemical form used | Use only if affinity is written in electrochemical units. |
| `k_j(V_n,q,T,I;theta)` | kinetic relaxation rate | 1/s | nonnegative | `dxi_j/dt`, `dxi_j/dq` | Can depend on solved `V_n`, measured `q`, temperature, and current. |

## Dynamics And Observables

| Symbol | Role | Unit | Domain | Defined Before | Notes |
|---|---|---|---|---|---|
| `dxi_j/dt` | time-domain state rate | 1/s | dynamic segment and rest | heat handoff, time integration | Always valid if model rate is defined. |
| `dxi_j/dq` | charge-domain state rate | dimensionless per normalized charge | only where `I_abs>0` | derivative observables | Define separately; not valid during rest. |
| `q_0` | initial normalized charge for integration | dimensionless | start of segment | integral form | Must match initial state. |
| `dV_n/dq` | derivative of internal potential wrt normalized external charge | V | nonzero-current segment | `dV_app/dq`, ICA/DVA | Derived by differentiating charge balance after state dynamics are defined. |
| `dV_{n,app}/dq` | derivative of apparent voltage wrt normalized external charge | V | nonzero-current segment | ICA/DVA | Includes apparent-shift derivative if `R_n` is used. |
| `dQ_ext/dV_{n,app}` | ICA observable | C/V | where denominator is nonsingular | fitting observations | Based on external charge. |
| `dV_{n,app}/dQ_ext` | DVA observable | V/C | where derivative exists | fitting observations | Reciprocal form scaled by `Q_cell`. |

## Closure And Validation Terms

| Symbol | Role | Unit | Domain | Defined Before | Notes |
|---|---|---|---|---|---|
| `xi_j^ref(q)` | reference state path for closure approximation | dimensionless | selected reference trajectory | closure correction | May be equilibrium, frozen-feedback, or low-rate direct solve path. |
| `V_n^ref(q)` | root-solved potential along reference path | V | admissible voltage interval | closure correction | Must still be computed through charge balance. |
| `F_j^ref(q)` | reference integrand | dimensionless per normalized charge | integration interval | closure schematic | Name may change in final notation to avoid conflict with Faraday constant. |
| `C_j(q)` or `mathcal C_j` | dimensionless feedback correction | dimensionless | approximation-dependent | closure approximation | Must specify estimation rule and validation. |
| `epsilon_Q` | slope floor/conditioning threshold | C/V | positive | numerical validation | Numerical safeguard, not a physical fitted shape knob unless justified. |

## Forbidden Reordering

- Do not write `k_j(V_n,...)` before defining the root operator that gives `V_n`.
- Do not define `V_{n,OCV}(q,T)` as an independent input before charge balance.
- Do not define `dV_n/dq`, ICA, or DVA before defining `dxi_j/dq`.
- Do not introduce refs. 6/7 closure before the exact direct formulation.
- Do not move Chapter 2 heat or Chapter 3 kinetic refinements ahead of Chapter 1 charge balance.

## Symbol Collision Controls

| Collision | Control |
|---|---|
| `w_j` as width versus capacity weight | Reserve `w_j` for voltage width; use `a_j` for capacity fraction. |
| `Q_ext`, `Q_cell q`, and electrode storage | Use `Q_ext=Q_cell q` only for measured external charge; storage terms stay inside charge balance. |
| `V_n`, `V_{n,app}`, `V_{n,drive}` | Keep three roles separate. |
| `F` Faraday constant versus reference integrand | Avoid naming a reference integrand `F_j^ref` in final prose if Faraday constant appears nearby; prefer `Phi_j^ref` if needed. |
| `R_n` and kinetic shifts | Constrain fitting or stage parameters to avoid double-counting. |
| `q` and `xi_j` | `q` is external coordinate; `xi_j` is internal state. |

## Allowed Synonyms

| Preferred Symbol / Term | Allowed Korean Term | Allowed English Term | Forbidden Synonym |
|---|---|---|---|
| `Q_ext` | 외부 전하, 통과 전하 | external charge, passed charge | electrode stored charge |
| `q` | 정규화 외부 전하 | normalized external charge | internal reaction coordinate |
| `V_n` | 내부 흑연 전위, root-solved negative-electrode potential | internal graphite potential | prescribed OCV input |
| `V_{n,OCV}` | 평형 OCV 특수해 | equilibrium OCV special root | dynamic voltage input |
| `Q_bg` | 배경 저장 용량항 | background storage term | cosmetic baseline |
| `xi_j` | 전이 진행 변수, 내부 상태 | progress variable, internal state | measured charge coordinate |
| closure | 기준해 보정 폐쇄 | reference-correction closure | direct physical import from refs. 6/7 |

## Gate Status

Gate: `PASS_REBUILD_V2_NOTATION_DEPENDENCY`

No notation entry in this bible is allowed into the manuscript unless its role, unit, and domain are preserved or deliberately revised in a later recorded addendum.
