# Tail Barrier Scope Review

Project: `D:\Projects\Project_Anode_Fit`

Date: 2026-05-28

Trigger: user clarification that current focus is peak-tail behavior from temperature and electrode-potential-dependent effective barrier, not peak area.

## Corrected Core Goal

The current Chapter 1 theory target is:

> Explain why the ICA peak tail becomes long at low temperature and short at high temperature, and derive a logically usable expression in which the effective phase-transition barrier is reduced by the present electrode potential state.

This is not a request for:

- peak-area theory as the main topic;
- fitted peak area;
- fitting code;
- numerical solver construction;
- parameter extraction from data.

## Review Of Current Artifact

Reviewed artifact:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_theory_complete.tex`

| Item | Assessment | Action |
|---|---|---|
| charge coordinate `Q_ext`, `q` | useful | salvage concept |
| charge balance and implicit `V_n` | useful and required | salvage concept |
| self-consistent state equation | useful | salvage concept |
| relaxation length `ell_q=|I|/(Q_cell k_j)` | useful but incomplete | salvage after linking to effective barrier |
| peak area section | overemphasized for current scope | remove from new main line; mention only as future fitting boundary if needed |
| temperature-only rate explanation | incomplete | replace with `Delta G_eff = Delta G_a(T) - chi A(V_drive,T)` logic |
| present potential state | mentioned but not structurally central | make central through affinity and barrier lowering |
| fitting/code exclusion | correct | keep |

## Source Evidence To Recenter

Corrected ver1 source lines 203-266 contain the needed structure:

- voltage roles: `V_n`, `V_{n,app}`, `V_{n,drive}`;
- apparent voltage: `V_{n,app}=V_n+s_I |I| R_n(q,T,|I|)`;
- affinity: `A_j=s_{\phi,j}F[V_{n,drive}-U_j(T)]`;
- intrinsic activation free energy: `Delta G_{a,j}(T)=Delta H_{a,j}-T Delta S_{a,j}`;
- effective barrier: `Delta G_eff,j = Delta G_a,j(T)-chi_j A_j`;
- positive barrier regularization: softplus;
- rate: `k_j=nu_j(T) exp[-Delta G_eff,j^+/(RT)]`.

## New Required Logic Spine

1. Define measured ICA tail as a distribution of `d xi_j/dV`, not peak area.
2. Define `V_n` from charge balance.
3. Define `V_{n,drive}` as the voltage that enters transition kinetics.
4. Define affinity `A_j=s_phi F(V_drive-U_j)`.
5. Define intrinsic barrier from temperature: `Delta G_a(T)=Delta H_a-T Delta S_a`.
6. Define effective barrier lowering by electrode potential: `Delta G_eff=Delta G_a(T)-chi A_j`.
7. Define bounded positive barrier `Delta G_eff^+`.
8. Define rate `k_j=nu exp[-Delta G_eff^+/(RT)]`.
9. Convert state relaxation to charge coordinate: `d xi/dq=(Q_cell/|I|) k_j (xi_eq-xi)`.
10. Derive tail decay of unrelaxed fraction: `u(q)=u(q_a) exp[-int kappa dq]`.
11. Define tail length `ell_q=|I|/(Q_cell k_j)`.
12. Substitute effective barrier: `ell_q=|I|/(Q_cell nu) exp[Delta G_eff^+/(RT)]`.
13. Interpret low temperature as longer tail through larger barrier exponent.
14. Interpret higher temperature and/or stronger present driving potential as shorter tail through smaller barrier exponent.
15. Connect ICA tail to `d xi/dV=(d xi/dq)/(dV/dq)` without doing parameter fitting.

## Decision

The current artifact should not be patched into final form. Create a new artifact from fundamentals:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_tail_effective_barrier_theory.tex`

The previous artifact remains a scaffold/reference, not the accepted Chapter 1 output.
