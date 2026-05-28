# Phase 006 — Notation And Dependency Bible

## Summary

This phase fixes the symbol roles and dependency structure before deriving the effective barrier and tail scale. The central conclusion is that the apparent feedback among `q`, `xi_j`, `V_n`, `xi_{j,eq}`, and `k_j` is not a logical contradiction if it is treated as an algebraic-differential system:

```text
state xi_j at current q
  -> solve charge balance for V_n
  -> evaluate xi_eq and k_j
  -> compute dxi_j/dq
  -> advance xi_j
```

The prohibited error is to define the same voltage or peak broadening twice, for example by using apparent voltage both as the equilibrium coordinate and as an unconstrained kinetic driving term.

Gate result: `PASS_NOTATION_DEPENDENCY`

## Step Range

Planned steps: 73-90

Actual steps completed: 73-90

## Symbol Table

| Symbol | Role | Type | Definition / constraint | Source |
|---|---|---|---|---|
| `t` | time | independent coordinate | physical time | standard |
| `I` | applied current | controlled/measured input | use `|I|` for discharge progress speed | `graphite_ica_charge_balance_ver1_rechecked2.tex:95-106` |
| `Q_{\ext}` | externally passed charge | derived input | `Q_{\ext}(t)=int_0^t |I(t')|dt'` | `graphite_ica_charge_balance_ver1_rechecked2.tex:95-98` |
| `Q_{\cell}` | cell capacity scale | parameter | converts charge to dimensionless progress coordinate | `graphite_ica_charge_balance_ver1_rechecked2.tex:100-105` |
| `q` | discharge progress coordinate | independent coordinate in CC segment | `q=Q_{\ext}/Q_{\cell}`, `dq/dt=|I|/Q_{\cell}` for constant current | `graphite_ica_charge_balance_ver1_rechecked2.tex:100-106` |
| `T` | temperature | controlled/measured input or slow state | may be held isothermal in Chapter 1 core | plan scope |
| `Q_{\bg}(V_n,T)` | residual storage / chemical capacitance term | constitutive function | not a visual baseline; absorbs capacity not assigned to explicit staging transitions | `graphite_ica_charge_balance_ver1_rechecked2.tex:118-129` |
| `Q_{j,\tot}` | transition capacity weight | parameter | capacity contribution of transition `j` | `graphite_ica_charge_balance_ver1_rechecked2.tex:122-124` |
| `xi_j` | actual progress of transition `j` | state variable | evolves by relaxation equation | `graphite_ica_charge_balance_ver1_rechecked2.tex:268-286` |
| `xi_{j,\eq}` | equilibrium target progress | algebraic target | `xi_{j,\eq}=xi_{j,\eq}(V_n,T)` | `graphite_ica_charge_balance_ver1_rechecked2.tex:184-201` |
| `V_n` | internal graphite negative-electrode potential | algebraic variable | solved from charge balance, not prescribed externally | `graphite_ica_charge_balance_ver1_rechecked2.tex:118-129` |
| `V_{n,\app}` | apparent/measured negative-electrode potential | observable or derived algebraic variable | `V_{n,\app}=V_n+s_I|I|R_n(q,T,|I|)` | `graphite_ica_charge_balance_ver1_rechecked2.tex:217-222` |
| `V_{n,\drive}` | kinetic driving voltage | algebraic/model variable | voltage used to compute `A_j`; may be approximated by `V_{n,\app}` only with restrictions | `graphite_ica_charge_balance_ver1_rechecked2.tex:203-238` |
| `V_{n,\OCV}` | quasi-equilibrium potential | limiting observable/root | equilibrium charge-balance root when `xi_j=xi_{j,\eq}` | `graphite_ica_charge_balance_ver1_rechecked2.tex:148-162`; `graphite_ica_dynamic_ver5.tex:857-869` |
| `R_n` | reduced resistance/polarization term | constitutive function/parameterized function | shifts apparent voltage; must not freely duplicate kinetic lag | `graphite_ica_charge_balance_ver1_rechecked2.tex:217-238` |
| `U_j(T)` | transition center potential | parameter/function | center of equilibrium progress and reference for affinity | `graphite_ica_charge_balance_ver1_rechecked2.tex:184-201`, `224-228` |
| `w_j(T)` | equilibrium transition width | parameter/function | controls equilibrium logistic width, not kinetic tail length | `graphite_ica_charge_balance_ver1_rechecked2.tex:189-201` |
| `s_{\xi,j}` | equilibrium-progress direction sign | sign convention | default `+1`; changing it requires revisiting `q`, `Q_j`, `xi_j` definitions | `graphite_ica_charge_balance_ver1_rechecked2.tex:196-201` |
| `s_{\phi,j}` | driving-affinity direction sign | sign convention | positive when voltage displacement assists forward transition | `graphite_ica_charge_balance_ver1_rechecked2.tex:224-228` |
| `F` | Faraday constant | physical constant | converts voltage to energy per mole of charge | standard electrochemistry |
| `\mathcal A_j` | present-potential driving affinity/work | algebraic variable | `s_{\phi,j}F[V_{n,\drive}-U_j(T)]` | `graphite_ica_charge_balance_ver1_rechecked2.tex:224-233` |
| `\chi_j` | barrier-coupling coefficient | parameter | fraction/sensitivity by which affinity lowers activation barrier | `graphite_ica_charge_balance_ver1_rechecked2.tex:245-249` |
| `\Delta G_{a,j}` | intrinsic activation free energy | parameter/function | `\Delta H_{a,j}-T\Delta S_{a,j}` | `graphite_ica_charge_balance_ver1_rechecked2.tex:240-244` |
| `\Delta G_{\eff,j}` | potential-assisted effective barrier | algebraic variable | `\Delta G_{a,j}(T)-\chi_j\mathcal A_j` | `graphite_ica_charge_balance_ver1_rechecked2.tex:245-249` |
| `\Delta G_{\eff,j}^{+}` | regularized positive effective barrier | algebraic variable | softplus or positive part to avoid unbounded rate extrapolation | `graphite_ica_charge_balance_ver1_rechecked2.tex:250-266` |
| `\epsilon_G` | barrier softplus scale | numerical regularization | not a new physical barrier | `graphite_ica_charge_balance_ver1_rechecked2.tex:254-266` |
| `\nu_j(T)` | attempt frequency/prefactor | parameter/function | Arrhenius-like prefactor, may be temperature dependent | `graphite_ica_dynamic_ver5.tex:971-975` |
| `k_j` | relaxation rate constant | algebraic variable | `\nu_j(T) exp[-\Delta G_{\eff,j}^{+}/(RT)]` | `graphite_ica_charge_balance_ver1_rechecked2.tex:259-265` |
| `\rho_j(g)` | kinetic activation barrier distribution | optional extension | support `g>=0`, not equilibrium center distribution | `graphite_ica_charge_balance_ver1_rechecked2.tex:320-350` |
| `dQ_{\ext}/dV_{n,\app}` | ICA observable | derived observable | `Q_{\cell}/(dV_{n,\app}/dq)` | `graphite_ica_charge_balance_ver1_rechecked2.tex:394-405` |
| `dV_{n,\app}/dQ_{\ext}` | DVA observable | derived observable | `(1/Q_{\cell})dV_{n,\app}/dq` | `graphite_ica_charge_balance_ver1_rechecked2.tex:406-412` |

## Variable Categories

| Category | Members |
|---|---|
| Independent / control | `t`, `q`, `I`, `T` |
| State variables | `xi_j`; optional extension `xi_j(g,q)` |
| Algebraic variables | `V_n`, `V_{n,\app}`, `V_{n,\drive}`, `xi_{j,\eq}`, `A_j`, `Delta G_eff`, `Delta G_eff^+`, `k_j` |
| Parameters / constitutive functions | `Q_cell`, `Q_bg`, `Q_j,tot`, `U_j`, `w_j`, `R_n`, `Delta H_a`, `Delta S_a`, `chi_j`, `nu_j`, `epsilon_G`, optional `rho_j(g)` |
| Observables | `V_{n,\app}`, `dQ_ext/dV_app`, `dV_app/dQ_ext` |

## Dependency DAG

Chapter 1 core dependency graph:

```text
controls / coordinate:
  q, T, |I|

state at current q:
  xi_j

charge balance:
  q, T, xi_j, Q_bg, Q_j,tot
    -> solve V_n from Q_cell q = Q_bg(V_n,T)+sum_j Q_j,tot xi_j

equilibrium target:
  V_n, T, U_j(T), w_j(T)
    -> xi_j,eq(V_n,T)

apparent voltage:
  V_n, q, T, |I|, R_n
    -> V_n,app

driving voltage:
  full model: kinetic submodel -> V_n,drive
  reduced model: V_n,drive approx V_n,app with R_n/k_j constraints

affinity and barrier:
  V_n,drive, U_j(T), s_phi,j, F
    -> A_j
  T, DeltaH_a,j, DeltaS_a,j
    -> DeltaG_a,j(T)
  DeltaG_a,j(T), chi_j, A_j
    -> DeltaG_eff,j
  DeltaG_eff,j, epsilon_G
    -> DeltaG_eff,j^+
  DeltaG_eff,j^+, T, nu_j(T)
    -> k_j

state derivative:
  k_j, xi_j, xi_j,eq, Q_cell, |I|
    -> dxi_j/dq

observables:
  dxi_j/dq and charge-balance derivative
    -> dV_n/dq
  dV_n/dq and R_n derivative
    -> dV_n,app/dq
  dV_n,app/dq
    -> dQ_ext/dV_n,app and dV_n,app/dQ_ext
```

## Intentional Implicit System

The following feedback is intentional:

```text
xi_j -> charge balance -> V_n -> xi_eq and k_j -> dxi_j/dq -> xi_j
```

This is not a circular definition if evaluated as an algebraic-differential system. At a given `q`, the current state `xi_j(q)` is known from the previous step or initial condition. The charge-balance equation then determines `V_n(q)`. Only after `V_n(q)` is determined do `xi_eq`, `A_j`, `Delta G_eff`, `k_j`, and `dxi_j/dq` become evaluable.

For the written theory, this should be stated as:

```text
The model is implicit in voltage but explicit in logical order: current phase state fixes the internal potential through charge balance; that potential fixes the equilibrium target and rate; the rate then updates the phase state.
```

## Closing Equation For Feedback

The feedback-closing equation is:

```tex
Q_{\cell}q=Q_{\bg}(V_n,T)+\sum_{j=1}^{N_p}Q_{j,\tot}\xi_j.
```

The manuscript must not replace this with an arbitrary `V_n(q)` unless it explicitly states a quasi-equilibrium or empirical approximation.

## Prohibited Circular Definitions

| Prohibited loop | Why it fails |
|---|---|
| Define `V_n` from `V_{n,\app}` while defining `V_{n,\app}` from the same unconstrained `V_n` | algebraic role collapse |
| Use `V_{n,\app}` to set `xi_eq` and also use the same apparent shift to increase `k_j` | overpotential affects equilibrium and kinetics twice |
| Fit `R_n` and `k_j` freely from the same tail/broadening feature | double-counting and non-identifiability |
| Use EMG tail parameter to define `k_j`, then claim the model derived the tail | empirical peak function replaces derivation |
| Treat `rho_j(g)` as both kinetic barrier distribution and equilibrium transition-center distribution | mixes rate heterogeneity with voltage-location heterogeneity |
| Treat `epsilon_G` as a physical barrier | source defines it as numerical regularization |
| Derive peak area first and infer tail dynamics from area conservation | user scope places peak area in later fitting, not Chapter 1 core |

## Source Conflicts And Resolutions

| Conflict | Older / alternate source | Corrected resolution |
|---|---|---|
| Affinity voltage | `graphite_ica_dynamic_ver5.tex` often uses `V_{n,\app}` directly in `A_j` | Use `V_{n,\drive}` as the primary symbol; reduced model may set `V_{n,\drive}\approx V_{n,\app}` with restrictions |
| Barrier distribution support | `graphite_ica_dynamic_ver5.tex:305-318` uses an integral over `-\infty` to `\infty` | Use corrected `g>=0` support from `graphite_ica_charge_balance_ver1_rechecked2.tex:320-350` |
| Capacity/voltage formulation | early ver5 uses parameterized `Q_n(q)` and `V_OCV(q)` style expressions | Use charge-balance root `V_n` from `rechecked2` as Chapter 1 foundation |
| Equilibrium coordinate | later ver3 warns `xi_eq` should not be shifted by kinetic overpotential | Use internal/quasi-equilibrium potential for `xi_eq`; keep `A_j` in rate |
| Ref. 6/7 method | user paper verifies Fredholm ratio-closure method | Do not import unless graphite model is explicitly recast as a Fredholm second-kind integral equation |

## Minimal Manuscript Dependency Rule

The Chapter 1 manuscript must introduce equations in this order:

1. `Q_ext`, `q`, `dq/dt`.
2. charge balance and `V_n`.
3. `xi_eq(V_n,T)`.
4. `V_app`, `V_drive`, and role restrictions.
5. `A_j`.
6. `Delta G_a(T)`.
7. `Delta G_eff` and `Delta G_eff^+`.
8. `k_j`.
9. `dxi/dt` and `dxi/dq`.
10. tail residual and tail scale.
11. charge-balance differentiation.
12. ICA/DVA observables.

No later equation may be used before the variable it depends on has been defined.

## Validation

| Check | Result |
|---|---|
| `Q_ext`, `Q_cell`, and `q` defined | PASS |
| `Q_bg(V_n,T)` defined as residual storage, not visual baseline | PASS |
| `xi_j` and `xi_eq` roles separated | PASS |
| `V_n`, `V_app`, `V_drive`, `V_OCV` roles separated | PASS |
| `U_j`, `w_j`, `s_phi`, and direction signs identified | PASS |
| `A_j`, `chi_j`, `DeltaG_a`, `DeltaG_eff`, `DeltaG_eff^+`, `nu_j`, `k_j` defined | PASS |
| State/algebraic/parameter/observable categories created | PASS |
| Dependency DAG created | PASS |
| Intentional implicit loop marked and closed by charge balance | PASS |
| Prohibited circular definitions listed | PASS |
| Source conflicts identified instead of guessed away | PASS |

## Gate

Gate: `PASS_NOTATION_DEPENDENCY`

Status: PASS

Reason:

- every core symbol has one declared role;
- the self-consistent voltage feedback is closed by charge balance;
- voltage-role conflation and kinetic/equilibrium double-counting are explicitly prohibited;
- source conflicts are resolved in favor of the corrected charge-balance source.

## Confirmed Non-Changes

- No source `.tex` file was modified.
- No PDF was modified.
- `D:\Projects\Project_Anode_Fit\Claude` was not modified.
- No commit, push, merge, or branch operation was performed.

## Open Issues / Decision Queue

| Issue | Status |
|---|---|
| Effective barrier sign and unit checks still need formal derivation | pending Phase 007 |
| Tail residual equation and local approximation still need derivation | pending Phase 008 |
| ICA/DVA sign convention needs audit after mapping | pending Phase 009 |

No user decision is required before Phase 007.

## Next

Proceed directly to Phase 007 — Effective Barrier Derivation.
