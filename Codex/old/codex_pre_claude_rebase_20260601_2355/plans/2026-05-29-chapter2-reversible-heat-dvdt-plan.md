# Chapter 2 Reversible Heat and dV/dT Extension Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:verification-before-completion` before any completion claim. This plan is a manuscript-theory phase. It is not a solver, fitting-code, or numerical implementation phase.

**Goal:** Build Chapter 2 from zero-base as the thermodynamic extension of Chapter 1. Chapter 2 must derive how the Chapter 1 graphite-anode ICA tail framework connects to equilibrium entropy coefficient, reversible heat, apparent/dynamic `dV/dT`, and the boundary between reversible and irreversible heat.

**Architecture:** Treat Chapter 1 v5 as the current canonical input. Reuse its conventions and logical chain, but do not copy older Chapter 2 equations as ground truth. The old merged `ver.2` material may be used only as a table-of-contents hint: heat layer, `dV/dT`, reversible/irreversible heat split, thermal feedback handoff. All equations in this phase must be re-derived under the Chapter 1 v5 convention.

**Tech Stack:** LaTeX manuscript source, PowerShell UTF-8 file operations, static LaTeX/convention checks, manual mathematical audit with 10 review passes.

---

## Summary

This phase responds to the user's instruction:

- `챕터2 계획서 및 작성 그리고 10회 검수`.
- Chapter 2 must follow the updated plan-and-phase-record operation.
- Chapter 2 must be written in Korean prose, but academic technical terms should remain in English when that is the natural term.
- Chapter 2 must not become fitting code, solver construction, or implementation detail.
- The output must be a logically complete manuscript draft whose equations can be followed by an undergraduate reader without hidden jumps.

The physical target that must be stated at the beginning of the manuscript and preserved through the derivation:

- LIB graphite anode ICA (`dQ/dV`) peak-tail behavior is the target system.
- In the ICA peak region, phase transition creates a peak/tail structure.
- The observed issue is the tail shape: at low temperature the post-peak tail is longer; at high temperature the tail ends more quickly.
- The basic explanation retained from Chapter 1 is that an activation barrier and a distribution of effective relaxation lengths shape the post-peak tail.
- Electrode-potential assistance lowers the effective barrier smoothly; it must not be treated as a discontinuous step-function or a sudden `0 -> 1` switch.
- Chapter 2 extends that logic into thermal quantities: equilibrium `dV/dT`, reversible heat, apparent/dynamic `dV/dT`, and the heat terms that should or should not be interpreted as thermodynamic entropy.

The perspective inherited from the user's ChatGPT manuscript work:

- Physical meaning is more important than compactness.
- Every assumption must have a thermodynamic, electrochemical, or literature-grounded reason.
- Any fitted expression must be distinguishable from a thermodynamic identity.
- A mathematical closure may be proposed only after its domain of validity and failure mode are stated.
- Do not hide convention choices. Define coordinates, current sign, heat sign, and state variables before using them.
- Do not use an unphysical barrier-as-step approximation. Activation barrier is allowed only as a smooth thermodynamic/kinetic quantity.
- Do not preserve a previous equation merely because an older file contains it.

## Current Ground Truth

Canonical Chapter 1 input:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex`
- Chapter 1 v5 SHA256 from Phase 017: `9E5DCCE75CB650251FAAA7741591B1D23B89632545BAFF157EB5798E53E690F1`

Confirmed Chapter 1 v5 chain:

```text
charge conservation
-> theta_eq target
-> Delta G_eff = Delta G_a - chi A
-> k(G,T,psi)
-> L_q
-> A_L(lambda;T,psi)
-> spectrum kernel integral
-> dQ_ext/dV_n
```

Chapter 1 v5 conventions to preserve:

- `q`: primary normalized external charge coordinate.
- `Q_ext = Q_cell q`: dimensional charge only when needed.
- `V_n`: internal graphite-anode potential coordinate used in the theory.
- `V_{n,app}`: apparent/measured potential after polarization terms are included.
- `theta_j`: local transition progress variable for mode `j`.
- `Theta`: summed graphite transition inventory.
- `theta_eq,j`: equilibrium target under local potential and temperature.
- `r_j = theta_eq,j - theta_j`: lag variable.
- `L_q`: normalized relaxation length; dimensional `L_Q` only for explicit conversion.
- `A_L(lambda;T,psi)`: relaxation-length spectrum.
- `psi`: electrode-potential assistance coordinate.
- No `xi` coordinate in the new Chapter 2.

Chapter 1 v5 equations that may be used as input, not as unquestioned decoration:

```latex
Q_{\cell}q = Q_{\bg}(V_n,T) + Q_p\Theta(V_n,q,T)
```

```latex
\frac{\dd V_n}{\dd q}
=\frac{Q_{\cell}-Q_p\,\dd\Theta/\dd q}{C_{\bg}(V_n,T)}
```

```latex
\Delta G_{\eff,j}(V_n,T,\psi)=\Delta G_{a,j}(T)-\chi_j A_j(V_n,\psi)
```

```latex
L_q(G,T,\psi)
=\frac{|I|}{Q_{\cell}k_0(T)}
\exp\!\left[\frac{G-W_{\psi}}{RT}\right]
```

```latex
\frac{\dd\Theta_{\tail}}{\dd q}
\simeq
\int_0^\infty A_L(\lambda;T,\psi)\lambda^{-1}
\exp[-(q-q_a)/\lambda]\,\dd\lambda
```

```latex
\frac{\dd Q_{\ext}}{\dd V_n}
=
\frac{C_{\bg}(V_n,T)}
{1-\dfrac{Q_p}{Q_{\cell}}\dfrac{\dd\Theta}{\dd q}}
```

Old merged `ver.2` structural hints:

- It introduced heat as the next layer after the ICA-tail theory.
- It separated reversible heat and irreversible heat.
- It warned that apparent-potential temperature derivative must not be used directly as reversible entropy coefficient.
- It used a transition basis for heat features.

Old merged `ver.2` non-ground-truth items:

- Old state symbols such as `xi` must not be imported.
- Old equations must not be copied without re-derivation.
- Old heat basis forms must be treated as hints only.

## Phase Range

| Phase | Name | Step Range | Purpose |
|---|---|---:|---|
| 019 | Chapter 2 plan, manuscript, and 10-pass audit | 1-34 | Save plan, write Chapter 2 from zero-base, run 10 logical review passes, repair issues, and save recovery artifacts. |

## Non-goals

- Do not write fitting code.
- Do not build a numerical solver.
- Do not claim a parameter is identifiable unless the manuscript states what measurement separates it.
- Do not use old `ver.2` equations as authority.
- Do not use `xi` or any new coordinate that conflicts with Chapter 1 v5.
- Do not collapse equilibrium entropy coefficient and dynamic apparent `dV/dT` into the same quantity.
- Do not call a dynamic tail contribution true reversible heat unless it is explicitly reduced to an equilibrium/quasi-static limit.
- Do not model activation barrier as a step-function threshold.
- Do not promote Plan A/Fredholm-style analytic compression unless this chapter explicitly marks it as gated and non-essential.
- Do not put work-history, audit-pass labels, or phase metadata inside the LaTeX manuscript body.
- Do not overwrite Chapter 1, earlier Chapter 2 attempts, old reports, or Claude artifacts.

## Implementation Changes

Create:

- `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-29-chapter2-reversible-heat-dvdt-plan.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter2_reversible_heat_dvdt_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_019_CH2_REVERSIBLE_HEAT_DVDT_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_019_CH2_REVIEW_10PASS.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_019_CH2_REVERSIBLE_HEAT_DVDT_LEDGER.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_019_CH2_REVERSIBLE_HEAT_DVDT_HANDOVER.md`
- `D:\Projects\Project_Anode_Fit\Codex\work\verify_ch2_reversible_heat_dvdt_v1.ps1`

Modify:

- No existing project artifact is modified in place.

## Phase 019 - Chapter 2 Reversible Heat and dV/dT Extension

- [ ] **Step 1: Save this plan before manuscript writing.**

  Expected: plan exists under `Codex\plans` before the Chapter 2 `.tex` file is created.

- [ ] **Step 2: Reconfirm active project instructions.**

  Expected: `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md` remains the active project instruction file.

- [ ] **Step 3: Reconfirm Chapter 1 v5 as canonical input.**

  Expected: Chapter 2 cites Chapter 1 v5 conventions and does not use older Chapter 1 files as equation authority.

- [ ] **Step 4: Establish manuscript convention block.**

  Required definitions:

  - `q`, `Q_ext`, `Q_cell`
  - `V_n`, `V_{n,app}`
  - `theta_j`, `Theta`, `theta_eq,j`
  - `T`, `I`, `I_s`, `|I|`
  - `h_n^{eq}`, `h_n^{dyn}`, `\dot Q_{rev}`, `\dot Q_{irr}`
  - heat sign convention and current sign convention

- [ ] **Step 5: State the Chapter 2 central separation.**

  Required statement:

  - `h_n^{eq}=(\partial V_{n,eq}/\partial T)_q` is the equilibrium entropy coefficient candidate.
  - `( \partial V_{n,app}/\partial T )_q` from measurement is an apparent/dynamic derivative unless all polarization and kinetic-lag terms are removed.
  - Dynamic tail features can shape measured thermal response, but they are not automatically reversible heat.

- [ ] **Step 6: Derive equilibrium charge-balance temperature derivative.**

  Starting point:

  ```latex
  Q_{\cell}q = Q_{\bg}(V_{eq},T)+Q_p\Theta_{eq}(V_{eq},T)
  ```

  Required result:

  ```latex
  h_n^{eq}(q,T)
  =
  -\frac{(\partial Q_{\bg}/\partial T)_{V}
  +Q_p(\partial\Theta_{eq}/\partial T)_{V}}
  {C_{\bg}(V_{eq},T)+Q_p(\partial\Theta_{eq}/\partial V)_{T}}
  ```

  Gate: units must be `V/K`; the denominator must be differential capacity-like.

- [ ] **Step 7: Explain the thermodynamic meaning of `h_n^{eq}`.**

  Expected:

  - Link to reversible electrochemical entropy without overcommitting to a sign convention.
  - Define the operational sign used in this manuscript.
  - Cite battery energy-balance and insertion-electrode thermal modeling literature.

- [ ] **Step 8: Derive reversible heat expression.**

  Expected:

  - Signed expression with `I_s`.
  - Magnitude/sign-table expression for readers using the opposite current convention.
  - Explicit statement that this is valid for equilibrium/quasi-static `V_{n,eq}`, not raw `V_{n,app}`.

- [ ] **Step 9: Derive apparent/dynamic `dV/dT` expression.**

  Starting point:

  ```latex
  Q_{\cell}q = Q_{\bg}(V_n,T)+Q_p\Theta(V_n,q,T;\mathcal H)
  ```

  Required separation:

  - background thermal term
  - transition inventory term
  - kinetic-lag/history term
  - polarization term in `V_{n,app}`

- [ ] **Step 10: Connect Chapter 1 tail kernel to dynamic thermal response.**

  Expected:

  - Use `A_L(lambda;T,psi)` to explain why temperature changes move tail weight.
  - In `lambda`-space, temperature dependence enters through `A_L(lambda;T,psi)` at fixed `lambda`.
  - In `G`-space, temperature dependence enters through both `L_q(G,T,psi)` and the barrier distribution.
  - Avoid claiming that the post-peak tail area is the reversible heat.

- [ ] **Step 11: Build a conservative two-layer closure.**

  Required layers:

  - Layer E: equilibrium thermodynamic layer for `h_n^{eq}` and `\dot Q_{rev}`.
  - Layer D: dynamic apparent layer for measured `dV/dT`, tail-shape response, and thermal fitting features.

- [ ] **Step 12: Define an allowed reduced basis for Chapter 2.**

  Expected:

  - Equilibrium heat basis may use equilibrium transition shapes such as `\phi_j^{eq}`.
  - Dynamic heat-shape basis may use Chapter 1 tail kernels.
  - The manuscript must state which basis is thermodynamic and which is phenomenological/dynamic.

- [ ] **Step 13: Separate irreversible heat.**

  Expected:

  - Use `V_{n,app}-V_n` or overpotential-like term for irreversible heat.
  - Give `|I|^2R_n` only as a reduced approximation.
  - Do not bury kinetic-lag heat inside reversible heat.

- [ ] **Step 14: Add thermal balance handoff.**

  Expected:

  - Provide a lumped `C_th dT/dt` balance as a later-chapter bridge.
  - State that this chapter does not solve the thermal ODE.

- [ ] **Step 15: Add identifiability and measurement section.**

  Required distinctions:

  - slow OCV temperature-step measurement estimates `h_n^{eq}`
  - galvanostatic dynamic measurement estimates `h_n^{dyn}` or apparent thermal response
  - polarization correction is required before using `dV/dT` as entropy coefficient

- [ ] **Step 16: Add assumptions and failure modes.**

  Expected:

  - quasi-equilibrium requirement for `h_n^{eq}`
  - local uniform temperature assumption
  - graphite phase-transition basis limits
  - current-rate dependence and history dependence
  - Plan A analytic compression remains optional/gated

- [ ] **Step 17: Add Chapter 3/4/5 handoff.**

  Expected:

  - Chapter 3: electrochemical reaction kinetics extension.
  - Chapter 4: heat extension after kinetic expansion.
  - Chapter 5: charge/discharge hysteresis interpretation.

- [ ] **Step 18: Write Chapter 2 `.tex` from zero-base.**

  Expected: new file under `Codex\results`, not an edited copy of old `ver.2`.

- [ ] **Step 19: Review pass 1 - convention audit.**

  Check: `q`, `theta`, `Theta`, `L_q`, `A_L`, no `xi`, no conflicting coordinate.

- [ ] **Step 20: Review pass 2 - charge-balance algebra audit.**

  Check: fixed-`q` differentiation, denominator, units, signs.

- [ ] **Step 21: Review pass 3 - thermodynamic identity audit.**

  Check: entropy coefficient is equilibrium only; sign convention explicitly stated.

- [ ] **Step 22: Review pass 4 - apparent vs equilibrium audit.**

  Check: `V_{n,app}` derivative is not silently equated with reversible heat.

- [ ] **Step 23: Review pass 5 - reversible vs irreversible heat audit.**

  Check: `\dot Q_{rev}` and `\dot Q_{irr}` are separated and not double counted.

- [ ] **Step 24: Review pass 6 - tail-kernel thermal-response audit.**

  Check: dynamic tail effects are not mislabeled as equilibrium entropy.

- [ ] **Step 25: Review pass 7 - physical assumption and literature audit.**

  Check: every assumption is named, and literature references support the heat split.

- [ ] **Step 26: Review pass 8 - undergraduate-followability audit.**

  Check: no hidden differentiation step, no unexplained symbol, no jump from equation to interpretation.

- [ ] **Step 27: Review pass 9 - Chapter handoff audit.**

  Check: Chapter 2 stays within heat/`dV/dT` extension and does not pre-solve Chapter 3-5.

- [ ] **Step 28: Review pass 10 - manuscript hygiene and process-label audit.**

  Check: no phase labels, no audit labels, no `Codex`, no work-history inside the `.tex` body.

- [ ] **Step 29: Apply repairs found during the 10 passes.**

  Expected: if any issue is found, patch the manuscript and rerun affected checks.

- [ ] **Step 30: Run static LaTeX checks.**

  Required:

  - line count and SHA256
  - `\begin`/`\end` count
  - brace count
  - missing `\ref` targets
  - missing `\cite` targets
  - high-risk pattern search

- [ ] **Step 31: Check whether a TeX engine is available.**

  Expected:

  - If `xelatex` exists, compile.
  - If `xelatex` is missing, report `PDF build not run: xelatex NOT_FOUND`.

- [ ] **Step 32: Save 10-pass review report.**

  Expected: report lists each pass, finding, repair if any, and final gate result.

- [ ] **Step 33: Save phase result and ledger.**

  Expected: include input files, read coverage, created files, commands, validation evidence, unresolved gates.

- [ ] **Step 34: Save handover.**

  Expected: another agent can resume Chapter 3 or revise Chapter 2 without relying on conversation memory.

## Test Plan

Static verification commands:

- Read Chapter 2 line count.
- Compute SHA256.
- Count LaTeX `\begin` and `\end`.
- Count braces.
- Extract labels, refs, cites, and bibitems; report missing refs/cites.
- Search high-risk forbidden or risky patterns:
  - `\xi`
  - `V_{n,app}` used as reversible entropy coefficient
  - `step function`
  - `0 -> 1`
  - `solver`
  - `fallback`
  - `회귀`
  - `Codex`
  - `audit`
  - `phase`
  - `Ralph`
- Check that `h_n^{eq}` and `h_n^{dyn}` both appear and are distinguished.
- Check that reversible and irreversible heat equations both appear.
- Check whether `xelatex` exists.

Manual 10-pass verification:

1. Convention audit.
2. Charge-balance algebra audit.
3. Thermodynamic identity audit.
4. Apparent vs equilibrium audit.
5. Reversible vs irreversible heat audit.
6. Tail-kernel thermal-response audit.
7. Physical assumption and literature audit.
8. Undergraduate-followability audit.
9. Chapter handoff audit.
10. Manuscript hygiene and process-label audit.

PDF build:

- Optional only if a TeX engine is available.
- Failure to find `xelatex` is not a manuscript logic failure; report it explicitly.

## Assumptions

- Chapter 1 v5 remains the canonical Chapter 1 candidate.
- Chapter 2 is a new zero-base derivation under Chapter 1 v5 conventions.
- Reversible heat is tied to an equilibrium entropy coefficient, not to raw dynamic ICA tails.
- Dynamic ICA tail behavior can affect apparent thermal response and measured `dV/dT`, but that requires a separate dynamic layer.
- Literature-backed heat split follows battery energy-balance theory; the manuscript should cite Bernardi, Pawlikowski, and Newman, and insertion-electrode thermal modeling references.

## Correction History

- Phase 019 starts after Chapter 1 v5 was established as the current canonical candidate.
- This plan explicitly corrects the risk of importing old `ver.2` formulas or old `xi` notation.
- This plan adds the user's latest clarification as a front-loaded requirement: ICA peak tail, temperature barrier, smooth electrode-potential assistance of effective activation barrier, undergraduate-level derivation, no logical jump, and no ungrounded assumptions.
