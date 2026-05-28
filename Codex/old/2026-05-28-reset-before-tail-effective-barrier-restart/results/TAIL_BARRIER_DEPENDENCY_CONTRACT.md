# Tail Barrier Dependency Contract

Project: `D:\Projects\Project_Anode_Fit`

Created: 2026-05-28

## Required Dependency Spine

```text
Q_ext, q
  -> charge balance
  -> V_n
  -> V_app
  -> V_drive
  -> A_j = s_phi F (V_drive - U_j)
  -> Delta G_a,j(T) = Delta H_a,j - T Delta S_a,j
  -> Delta G_eff,j = Delta G_a,j(T) - chi_j A_j
  -> Delta G_eff,j^+ positive barrier
  -> k_j = nu_j exp[-Delta G_eff,j^+/(RT)]
  -> dxi_j/dq = (Q_cell/|I|) k_j (xi_eq - xi_j)
  -> tail decay u_j(q)
  -> ell_q,j = |I|/(Q_cell k_j)
  -> ICA tail via dxi_j/dV_obs
```

## Required Equations

| ID | Equation | Purpose |
|---|---|---|
| E1 | `Q_ext = int |I| dt`, `q=Q_ext/Q_cell` | charge coordinate |
| E2 | `Q_cell q = Q_bg(V_n,T)+sum Q_j xi_j` | internal potential root |
| E3 | `V_app=V_n+s_I |I| R_n` | apparent voltage |
| E4 | `A_j=s_phi,j F(V_drive-U_j(T))` | electrode-potential driving affinity |
| E5 | `Delta G_a,j=Delta H_a,j-T Delta S_a,j` | intrinsic temperature barrier |
| E6 | `Delta G_eff,j=Delta G_a,j-chi_j A_j` | potential-assisted barrier lowering |
| E7 | `Delta G_eff,j^+=epsilon_G ln[1+exp(Delta G_eff,j/epsilon_G)]` | positive effective barrier |
| E8 | `k_j=nu_j exp[-Delta G_eff,j^+/(RT)]` | transition rate |
| E9 | `dxi_j/dq=(Q_cell/|I|) k_j (xi_eq-xi_j)` | charge-domain relaxation |
| E10 | `u_j(q)=u_j(q_a) exp[-int kappa_j dq]` | tail decay |
| E11 | `ell_q,j=|I|/(Q_cell k_j)` | tail length |
| E12 | `ell_q,j=|I|/(Q_cell nu_j) exp[Delta G_eff,j^+/(RT)]` | barrier-to-tail expression |
| E13 | `dQ_tail/dV_obs proportional Q_j dxi_j/dV_obs` | ICA tail connection |

## Required Interpretations

| ID | Interpretation | Required Direction |
|---|---|---|
| I1 | low temperature | lower `T` increases barrier exponent and tends to lengthen tail |
| I2 | high temperature | higher `T` reduces barrier exponent and tends to shorten tail |
| I3 | present electrode potential | larger forward driving affinity lowers `Delta G_eff` and shortens tail |
| I4 | Gaussian expectation | equilibrium-only peak can look symmetric, but barrier-limited relaxation creates asymmetric tail |
| I5 | fitting-use equation | provide equations that future fitting can use, but do not fit data |

## Current Artifact Decision

`graphite_ica_chapter1_theory_complete.tex` is not edited into the final target. It is reference-only because it centers peak area too strongly for the corrected task.
