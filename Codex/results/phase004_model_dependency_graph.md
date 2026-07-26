# Phase 004 Model Dependency Graph

Status: working baseline for the Chapter 1-3 scientific audit. An edge labelled `declared gap` is intentionally not closed by v1.0.23.

```mermaid
flowchart TD
    EXP["Experimental inputs: V_app, direction, c_rate, Q_cell, T"]
    MAP["Electrode-aware direction map: cell label -> sigma_d"]
    CUR["Current magnitude and time scale: I_abs, I/Q_cell"]
    POL["Lumped polarization: V_n = V_app - sigma_d I_abs R_n"]

    TH["Transition thermodynamics: DeltaH_rxn, DeltaS_rxn, electronic/vibrational terms"]
    CTR["Centers U_j(T)"]
    WID["Widths w_j(T) or fitted constant w_j"]
    INT["Regular-solution branch parameters: Omega_j, gamma_j"]
    KIN["Activation parameters and Eyring lag"]

    OCC["Per-transition equilibrium progress xi_eq,j(U,T)"]
    BAL["Fixed-charge implicit balance: sum Q_j xi_j = Q x_bar"]
    UOC["Equilibrium potential U_oc(x_bar,T)"]
    ICA["ICA/DVA response: sum Q_j dxi_j/dV + C_bg"]
    ENT["Entropy coefficient at fixed x_bar: dU_oc/dT"]
    HEAT["Reversible heat: -I T dU_oc/dT"]

    HGR["Graphite host"]
    HSI["Si host effective components"]
    MASS["Blend declaration: m_Si, q_Si, q_gr"]
    FRAC["Capacity fraction f_Si"]
    BLEND["Shared-potential host sum and pooled charge balance"]

    STRESS["Stress state and partial molar volume"]
    SHIFT["Linear mean-stress potential offset"]
    PLASTIC["Path-dependent elastoplastic / particle-SEI law"]
    DAMAGE["Fracture, SEI growth, active-material loss"]

    DATA["Multi-temperature, multi-rate, structural and calorimetric data"]
    FIT["Parameter inference"]
    ID["Identifiability and uncertainty analysis"]

    EXP --> MAP --> POL
    EXP --> CUR --> POL
    CUR --> KIN
    TH --> CTR
    TH --> WID
    INT --> OCC
    CTR --> OCC
    WID --> OCC
    POL --> OCC
    KIN --> ICA
    OCC --> ICA
    OCC --> BAL --> UOC
    UOC --> ENT --> HEAT
    TH --> ENT

    MASS --> FRAC
    FRAC --> HGR
    FRAC --> HSI
    HGR --> BLEND
    HSI --> BLEND
    BLEND --> BAL
    BLEND --> ICA

    STRESS --> SHIFT --> CTR
    PLASTIC -. "declared gap GS-1" .-> STRESS
    DAMAGE -. "not represented" .-> HSI
    DAMAGE -. "not represented" .-> FRAC

    DATA --> FIT
    ICA --> FIT
    HEAT --> FIT
    FIT --> ID
    ID --> TH
    ID --> INT
    ID --> KIN
    ID --> FRAC
```

## Edge Classes

| Class | Meaning | Current audit use |
|---|---|---|
| Exact accounting identity | Charge/capacity conservation and host summation after the normalization basis is fixed | Re-derive and unit-test |
| Equilibrium relation | Chemical-potential balance, logistic response, and implicit inversion | Check signs, reference states, and domains |
| Near-equilibrium approximation | Lumped resistance, low-rate entropy measurement, reduced heat balance | Require rate and relaxation limits |
| Phenomenological law | Effective transition components, fitted widths, branch shrinkage, and lag kernel | Prevent microscopic over-interpretation |
| Numerical device | Bisection, clipped logit, seed lag, and ratio correction | Test convergence and ensure it is not presented as new physics |
| Declared missing closure | Si plasticity/current partition/nonadditivity and damage evolution | Preserve as a boundary; propose evidence-backed next models |

## Confirmed Broken Or Ambiguous Edges

1. `c_rate -> I/Q_cell -> Eyring lag`: hours are passed into a seconds-based attempt-frequency expression without conversion.
2. `m_Si -> f_Si -> host capacities`: the fraction is correct, but the implementation holds graphite capacity fixed, so absolute capacity is on a fixed-graphite-add-Si basis rather than a fixed-total-mass blend basis.
3. `biaxial thin-film stress measurement -> mean-stress coefficient`: the source and chapter differentiate with respect to different stress variables.
4. `small-strain Larché-Cahn term -> high-lithiation Si`: the source itself warns that finite kinematics and high solute concentration can produce substantial errors.
