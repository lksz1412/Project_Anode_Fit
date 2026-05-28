# Chapter 1 Rebuild With Claude Strengths And Relaxation-Length Spectrum Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` or an equivalent stepwise execution loop to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Store all phase outputs under `D:\Projects\Project_Anode_Fit\Codex\results`. Do not modify `D:\Projects\Project_Anode_Fit\Claude` or original source folders.

**Goal:** Rebuild Chapter 1 from zero as a paper/patent-grade theoretical background for graphite negative-electrode ICA tail behavior, using Claude Code's manuscript strengths while making `activation free-energy barrier distribution -> rate constant distribution -> relaxation-length spectrum -> ICA tail kernel` the central tail theory.

**Architecture:** The chapter begins with review-paper-like convention definitions and forbidden-model boundaries, then derives smooth equilibrium thermodynamics, charge conservation and internal potential, local activation-assisted relaxation, relaxation-length spectrum formation, ICA mapping, self-consistent integral handling, and falsification logic. Claude Code is used only as a scaffold/evidence-quality reference; the chapter text and derivation are newly written.

**Tech Stack:** LaTeX manuscript, Markdown phase reports, static TeX syntax checks, grep-based banned-pattern checks, manual logic review loop.

---

## Summary

The user target is a theoretical Chapter 1 for LIB graphite negative-electrode ICA (`dQ/dV`) peak-tail behavior. The observed phenomenon is that a phase-transition-related graphite ICA peak has a post-peak tail that becomes longer at low `temperature` and shorter at higher `temperature`. The intended physical explanation keeps `activation free-energy barrier` as a core concept, adds smooth `electrode-potential assistance` that lowers the effective barrier, and interprets the measured tail through kinetic lag and a `relaxation-length spectrum`.

The forbidden mistake is the old step-function logic: a local state must not jump discontinuously from 0 to 1 after crossing a threshold. All phase progress must remain smooth in state variables. A single exponential tail is allowed only as the local response of one mode. The measured broad/asymmetric tail must be represented as a kernel integral over many relaxation lengths.

This plan supersedes the prior compact Codex candidate:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_activation_barrier_spectrum_v1.tex`

The prior candidate remains useful as the mechanism spine, but it is not final. The new output is a zero-base rewrite:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v1.tex`

## Current Ground Truth

### Confirmed User Requirements

- Target system: lithium-ion battery graphite negative electrode.
- Observable: `ICA`, especially graphite phase-transition-related peak tail.
- Phenomenon: low `T` gives long post-peak tail; high `T` gives shorter post-peak tail.
- Main goal: theoretical background and logical derivation, not solver construction and not fitting-code implementation.
- Chapter 1 focus: foundational equation logic for the tail; peak area/final fitting is later work.
- Writing style: Korean explanatory prose with English academic terms.
- Derivation depth: undergraduate-followable, no hidden equation jumps.
- Physical standard: assumptions must be grounded in theory/literature or explicitly labeled as reduced-model assumptions.
- Forbidden model: `Heaviside`, hard threshold, hard switch, `0 -> 1` completion jump, or artificial `max/min` clipping of state completion.
- Allowed and required concept: `activation energy barrier` / `activation free-energy barrier`, as long as it remains a smooth rate-control concept rather than a discontinuous completion threshold.

### Confirmed Comparison Result

Source:

`D:\Projects\Project_Anode_Fit\Codex\results\PHASE_004_CLAUDE_CODEX_CH1_COMPARISON.md`

Confirmed comparison:

- Claude Code Chapter 1 is stronger as a manuscript scaffold.
- Claude Code has better convention structure, `lattice-gas` / `regular-solution` thermodynamics, charge conservation, `V_n` bridge, `effective barrier` validity cautions, falsification protocol, and bibliography.
- Claude Code is weaker at the newest tail-core point because it can read too much like a single-mode `l_tail` theory.
- Codex candidate is stronger at the corrected tail object: barrier distribution mapped to rate distribution and then to relaxation-length spectrum.
- Final rewrite should combine Claude's document-level discipline with Codex's spectrum-kernel tail core.

### Source Files And Use Level

| File | Use Level | Read Status Used For This Plan |
|---|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md` | Project rule source | Read in this session |
| `D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md` | Planning convention source | Read in this session |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_004_CLAUDE_CODEX_CH1_COMPARISON.md` | Immediate comparison baseline | Read in this session |
| `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_chapter1.tex` | Scaffold/evidence reference only | Previously full-read; targeted sections re-read in this session |
| `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_activation_barrier_spectrum_v1.tex` | Mechanism-spine reference only | Previously full-read; targeted sections re-read in this session |

### Ground Truth Formula Chain

The rebuild must preserve this chain:

```text
smooth equilibrium progress
-> local finite-rate relaxation toward equilibrium
-> activation free-energy barrier with electrode-potential assistance
-> rate constant
-> local relaxation length
-> relaxation-length spectrum
-> kernel integral
-> ICA tail contribution
```

## Phase Range

| Phase | Name | Step Range | Main Output | Gate |
|---|---|---:|---|---|
| Phase 005 | Rebuild Plan And Source Boundary | 1-12 | This plan | `PASS_PLAN_SAVED` |
| Phase 006 | Zero-Base Chapter 1 Manuscript | 13-36 | `graphite_ica_chapter1_rebuilt_v1.tex` | `PASS_CH1_DRAFT_COMPLETE` |
| Phase 007 | Ralph Wiggum Logic Review Loop | 37-54 | `PHASE_007_CH1_REBUILD_LOGIC_REVIEW_10PASS.md` | `PASS_10_LOGIC_LOOPS` |
| Phase 008 | Final Repair, Ledger, Handover | 55-68 | final tex, ledger, handover | `PASS_REBUILD_HANDOVER_READY` |

Phase and step counts are minimum criteria. If additional source checking, notation repair, equation repair, literature checking, or logic loops are needed, add subphases and record them in the ledger.

## Non-Goals

- Do not implement a fitting solver.
- Do not implement numerical code.
- Do not decide final fitting parameter bounds beyond conceptual identifiability notes.
- Do not modify Claude files.
- Do not modify original downloaded `.tex` files or user paper PDFs.
- Do not overwrite previous Codex result files.
- Do not use the old ChatGPT/ver files as equation sources. They may only inform chapter scope and historical structure.
- Do not claim refs 6/7 have been fully integrated unless their bibliographic identity, original method, and variable mapping are actually checked.
- Do not put phase history, audit metadata, commit hashes, or work-log text inside the LaTeX manuscript body.

## Implementation Changes

### Files To Create

- `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-chapter1-rebuild-claude-strengths-spectrum-plan.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_006_CH1_REBUILD_DRAFT_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_CH1_REBUILD_LOGIC_REVIEW_10PASS.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_005_008_CH1_REBUILD_LEDGER.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_008_CH1_REBUILD_HANDOVER.md`

### Files To Read Without Modification

- `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md`
- `D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_004_CLAUDE_CODEX_CH1_COMPARISON.md`
- `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_chapter1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_activation_barrier_spectrum_v1.tex`

## Phase 005 — Rebuild Plan And Source Boundary

- [ ] **Step 1: Confirm active project boundary.**

  Confirm:

  ```text
  active project = D:\Projects\Project_Anode_Fit
  Codex workspace = D:\Projects\Project_Anode_Fit\Codex
  plan path = D:\Projects\Project_Anode_Fit\Codex\plans
  result path = D:\Projects\Project_Anode_Fit\Codex\results
  ```

- [ ] **Step 2: Read project-local rule files.**

  Read:

  ```text
  D:\Projects\Project_Anode_Fit\Codex\AGENTS.md
  D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md
  ```

- [ ] **Step 3: Read comparison baseline.**

  Read:

  ```text
  D:\Projects\Project_Anode_Fit\Codex\results\PHASE_004_CLAUDE_CODEX_CH1_COMPARISON.md
  ```

- [ ] **Step 4: Re-check the exact Claude strengths to import.**

  Use Claude only for structure and verification discipline:

  ```text
  convention block
  user requirement statement
  smooth equilibrium thermodynamics
  charge conservation and V_n bridge
  effective-barrier lowering validity cautions
  self-consistent integral placement
  falsification and identifiability protocol
  bibliography style
  ```

- [ ] **Step 5: Re-check the exact Codex mechanism spine to import.**

  Use Codex only for the corrected tail core:

  ```text
  barrier distribution
  rate constant distribution
  relaxation-length spectrum
  exponential kernel integral
  spectrum shift by temperature and electrode-potential assistance
  ```

- [ ] **Step 6: Lock the manuscript target.**

  The manuscript must explain:

  ```text
  low T -> smaller rate constants and larger relaxation lengths -> longer tail
  high T -> larger rate constants and shorter relaxation lengths -> shorter tail
  potential assistance -> lower effective barrier -> shorter relaxation lengths
  observed broad tail -> spectrum of kernels, not one barrier-shaped object
  ```

- [ ] **Step 7: Lock forbidden patterns.**

  The manuscript must not use these as state-completion models:

  ```text
  Heaviside completion
  threshold jump
  hard switch
  0 -> 1 instantaneous phase completion
  max/min clipping of completion state
  ```

- [ ] **Step 8: Choose output filenames.**

  Use:

  ```text
  D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v1.tex
  D:\Projects\Project_Anode_Fit\Codex\results\PHASE_006_CH1_REBUILD_DRAFT_RESULT.md
  D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_CH1_REBUILD_LOGIC_REVIEW_10PASS.md
  D:\Projects\Project_Anode_Fit\Codex\results\PHASE_005_008_CH1_REBUILD_LEDGER.md
  D:\Projects\Project_Anode_Fit\Codex\results\PHASE_008_CH1_REBUILD_HANDOVER.md
  ```

- [ ] **Step 9: Define Chapter 1 section order.**

  The manuscript section order is:

  ```text
  1. Convention and Scope
  2. Observation and Required Explanation
  3. State Variable and Smooth Equilibrium Target
  4. Charge Conservation and Internal Potential
  5. Local Relaxation Toward Equilibrium
  6. Effective Activation Barrier With Electrode-Potential Assistance
  7. Barrier-to-Rate-to-Length Mapping
  8. Relaxation-Length Spectrum and ICA Tail Kernel
  9. Self-Consistent Integral Layer and Refs 6/7 Placement
  10. ICA/DVA Observable Mapping
  11. What Would Falsify This Explanation
  12. Chapter 1 Deliverables To Later Chapters
  ```

- [ ] **Step 10: Define notation.**

  Use stable symbols:

  ```text
  q: normalized external charge coordinate
  Q: dimensional charge coordinate
  T: temperature
  V_app: measured/applied cell voltage proxy
  V_n: negative-electrode internal potential
  U_j(T): equilibrium center potential for transition j
  xi_j: local/stage progress variable
  xi_eq,j: smooth equilibrium target
  r_j = xi_eq,j - xi_j: kinetic lag
  Delta G_a,j: activation free energy before potential assistance
  W_el,j: electrode-potential assistance work
  Delta G_eff,j: effective activation free-energy barrier
  k_j: local rate constant
  L_j: local relaxation length in charge coordinate
  rho_G: activation-barrier distribution
  A_L: relaxation-length spectrum
  K: local exponential kernel
  ```

- [ ] **Step 11: Save this plan.**

  Create the plan at:

  ```text
  D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-chapter1-rebuild-claude-strengths-spectrum-plan.md
  ```

- [ ] **Step 12: Proceed directly to Phase 006 unless a hard blocker appears.**

  No user decision is needed at this boundary because the user asked to proceed into rewriting.

Gate `PASS_PLAN_SAVED`:

- Plan is saved at the path above.
- Plan states the user target at the top.
- Plan separates Claude scaffold strengths from Codex spectrum-core strengths.
- Plan forbids step-function completion and artificial state clipping.

## Phase 006 — Zero-Base Chapter 1 Manuscript

- [ ] **Step 13: Create LaTeX skeleton.**

  Create:

  ```text
  D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v1.tex
  ```

  Include a minimal compilable article structure:

  ```latex
  \documentclass[11pt]{article}
  \usepackage[a4paper,margin=25mm]{geometry}
  \usepackage{amsmath,amssymb,bm}
  \usepackage{booktabs,longtable}
  \usepackage{enumitem}
  \usepackage{hyperref}
  \newcommand{\dd}{\mathrm{d}}
  \newcommand{\eq}{\mathrm{eq}}
  \newcommand{\eff}{\mathrm{eff}}
  \begin{document}
  ...
  \end{document}
  ```

- [ ] **Step 14: Write Section 1, Convention and Scope.**

  Include:

  ```text
  ICA = incremental capacity analysis
  DVA = differential voltage analysis
  graphite staging
  phase-transition-like progress
  activation free-energy barrier
  electrode-potential assistance
  relaxation-length spectrum
  ```

  Explicitly state that Korean prose uses English academic terms.

- [ ] **Step 15: Write forbidden-model boundary.**

  State in prose:

  ```text
  This chapter does not model phase progress as a Heaviside step, hard switch, or instantaneous 0 -> 1 completion.
  Barrier lowering changes rate constants; it does not directly complete the phase variable.
  ```

- [ ] **Step 16: Write Section 2, Observation and Required Explanation.**

  Must include:

  ```text
  low T long tail
  high T short tail
  homogeneous equilibrium width alone predicts the wrong direction for the low-T long tail
  peak area is outside the current chapter's main target
  ```

- [ ] **Step 17: Write Section 3, State Variable and Smooth Equilibrium Target.**

  Derive a smooth `lattice-gas` ideal limit:

  ```latex
  \mu_j(\xi_j)=\mu_j^0+RT\ln\frac{\xi_j}{1-\xi_j}+\Omega_j(1-2\xi_j)
  ```

  Then show the ideal smooth target:

  ```latex
  \xi_{\eq,j}(V_n,T)=
  \frac{1}{1+\exp[-s_j(V_n-U_j(T))/w_j(T)]},
  \qquad
  w_j(T)=RT/F
  ```

  Explain that this is smooth, not a completion jump.

- [ ] **Step 18: Derive equilibrium peak width implication.**

  Differentiate:

  ```latex
  \frac{\partial \xi_{\eq,j}}{\partial V_n}
  =
  \frac{s_j}{w_j}\xi_{\eq,j}(1-\xi_{\eq,j})
  ```

  State:

  ```text
  homogeneous ideal equilibrium width scales with RT/F, so lowering T narrows the reversible peak; it does not by itself explain a longer low-T tail.
  ```

- [ ] **Step 19: Write Section 4, Charge Conservation and Internal Potential.**

  Derive:

  ```latex
  Q(q)=Q_{\mathrm{bg}}(V_n,T)+\sum_j Q_{j,\mathrm{tot}}\xi_j(q)
  ```

  Explain:

  ```text
  V_n is implicit because xi_j depends on V_n through the equilibrium target and rate constants.
  This implicitness is not a logical error; it is the physical charge-balance closure.
  ```

- [ ] **Step 20: Write applied/internal potential bridge.**

  State a reduced bridge:

  ```latex
  V_{\mathrm{app}}(q)=V_p(q)-V_n(q)-I R_{\Omega}(q,T)-\eta_{\mathrm{tr}}(q,T)
  ```

  Explain that Chapter 1's theory is written in `V_n`; fitting to measured data needs a bridge to `V_app`.

- [ ] **Step 21: Write Section 5, Local Relaxation Toward Equilibrium.**

  Derive from forward/back rate linearization:

  ```latex
  \frac{\dd \xi_j}{\dd t}=k_j(T,V_n)\left[\xi_{\eq,j}(V_n,T)-\xi_j\right]
  ```

  Define:

  ```latex
  r_j=\xi_{\eq,j}-\xi_j
  ```

- [ ] **Step 22: Convert time coordinate to charge coordinate.**

  With:

  ```latex
  v_Q=\frac{\dd Q}{\dd t}
  ```

  derive:

  ```latex
  \frac{\dd r_j}{\dd Q}+\frac{k_j}{v_Q}r_j
  =
  \frac{\dd \xi_{\eq,j}}{\dd Q}
  ```

  Explain every term.

- [ ] **Step 23: Derive local post-peak kernel.**

  In post-peak region where `d xi_eq / dQ` becomes small:

  ```latex
  r_j(Q)\simeq r_j(Q_a)\exp[-(Q-Q_a)/L_j],
  \qquad
  L_j=\frac{v_Q}{k_j}
  ```

  State that this is one local kernel, not the whole observed tail.

- [ ] **Step 24: Write Section 6, Effective Activation Barrier With Electrode-Potential Assistance.**

  Define:

  ```latex
  \Delta G_{\eff,j}(T,V_n)=
  \Delta G_{a,j}(T)-W_{\mathrm{el},j}(V_n,T)
  ```

  and:

  ```latex
  \Delta G_{a,j}(T)=\Delta H_{a,j}-T\Delta S_{a,j}
  ```

- [ ] **Step 25: Define smooth potential assistance.**

  Use:

  ```latex
  W_{\mathrm{el},j}(V_n,T)
  =
  \chi_j s_j F\,[V_n-U_j(T)]
  ```

  Include:

  ```text
  0 <= chi_j <= 1
  valid as a local leading-order approximation around the tail region
  no max/min clipping when the expression leaves its activated-regime validity range
  ```

- [ ] **Step 26: Write rate constant expression.**

  Use:

  ```latex
  k_j(T,V_n)=\nu_j(T)\exp[-\Delta G_{\eff,j}(T,V_n)/(RT)]
  ```

  Explain:

  ```text
  potential assistance lowers the barrier, increasing k_j, which shortens L_j.
  ```

- [ ] **Step 27: Write Section 7, Barrier-to-Rate-to-Length Mapping.**

  Introduce local barrier variable `G`:

  ```latex
  k(G,T,\psi)=k_0(T)\exp[-(G-W_\psi)/(RT)]
  ```

  with:

  ```latex
  L(G,T,\psi)=\frac{v_Q}{k_0(T)}
  \exp[(G-W_\psi)/(RT)]
  ```

- [ ] **Step 28: Derive Jacobian for spectrum mapping.**

  Use:

  ```latex
  G(L,T,\psi)=W_\psi+RT\ln\left[\frac{k_0(T)L}{v_Q}\right]
  ```

  and:

  ```latex
  \left|\frac{\dd G}{\dd L}\right|=\frac{RT}{L}
  ```

- [ ] **Step 29: Define relaxation-length spectrum.**

  Use:

  ```latex
  A_L(L;T,\psi)=
  \rho_G(G(L,T,\psi);T,\psi)\frac{RT}{L}A_0(L;T,\psi)
  ```

  Explain that `A_L` is not identical to `rho_G`.

- [ ] **Step 30: Write Section 8, Kernel integral for measured tail.**

  Use:

  ```latex
  \mathcal T(Q;T,\psi)
  =
  \int_0^\infty
  A_L(L;T,\psi)\frac{1}{L}
  \exp[-(Q-Q_a)/L]\,\dd L
  ```

  State this is the central Chapter 1 tail equation.

- [ ] **Step 31: Explain temperature and potential trends.**

  Include:

  ```latex
  \frac{\partial \ln L}{\partial \psi}
  =
  -\frac{\Lambda_\psi F}{RT}
  ```

  Explain:

  ```text
  low T shifts weight toward larger L for activated modes;
  higher T and positive potential assistance shift weight toward shorter L;
  this creates asymmetric/non-Gaussian tails without a step transition.
  ```

- [ ] **Step 32: Write Section 9, Self-Consistent Integral Layer and Refs 6/7 Placement.**

  State:

  ```text
  The local relaxation equation becomes self-consistent because V_n, xi_eq, and k depend on evolving charge and state.
  The user's paper refs 6/7 should be used for the mathematical treatment of feedback/Volterra-like integral equations after bibliographic and variable-mapping verification.
  This method is separate from the physical spectrum integral.
  ```

  Do not claim full ref 6/7 integration unless actually verified in a later phase.

- [ ] **Step 33: Write Section 10, ICA/DVA Observable Mapping.**

  Use:

  ```latex
  \dd Q=C_{\mathrm{bg}}(V_n,T)\dd V_n+\sum_j Q_{j,\mathrm{tot}}\dd \xi_j
  ```

  and derive:

  ```latex
  \frac{\dd Q}{\dd V_n}
  =
  \frac{C_{\mathrm{bg}}(V_n,T)}
  {1-\sum_j Q_{j,\mathrm{tot}}\dd \xi_j/\dd Q}
  ```

  Mark the measured `V_app` correction as a fitting bridge, not a Chapter 1 solver.

- [ ] **Step 34: Write Section 11, Falsification and competing mechanisms.**

  Include checks for:

  ```text
  equilibrium width
  ohmic/polarization shift
  diffusion/transport limitation
  barrier-spectrum vs single-mode relaxation
  potential-assistance Arrhenius slope or peak-shift signature
  ```

- [ ] **Step 35: Write Section 12, Deliverables to later chapters.**

  State:

  ```text
  Chapter 2 may connect dV/dT and reversible heat;
  Chapter 3 may extend rate/electrochemical kinetics;
  Chapter 4 may add heat generation;
  Chapter 5 may connect charge/discharge hysteresis.
  ```

- [ ] **Step 36: Save Phase 006 draft result report.**

  Create:

  ```text
  D:\Projects\Project_Anode_Fit\Codex\results\PHASE_006_CH1_REBUILD_DRAFT_RESULT.md
  ```

  Include inputs, generated file, read coverage, and known unresolved items.

Gate `PASS_CH1_DRAFT_COMPLETE`:

- `graphite_ica_chapter1_rebuilt_v1.tex` exists.
- All 12 planned manuscript sections exist.
- The central kernel integral exists.
- The document explains that local single exponential is only a kernel.
- The document does not present step-function completion as the model.

## Phase 007 — Ralph Wiggum Logic Review Loop

The "Ralph Wiggum loop" means deliberately checking for simple, embarrassing, foundational logic failures before claiming the derivation is sound.

- [ ] **Step 37: Pass 1, target alignment review.**

  Check whether the manuscript directly answers:

  ```text
  low T long tail
  high T short tail
  potential assistance lowers effective barrier
  ```

- [ ] **Step 38: Pass 2, forbidden discontinuity review.**

  Search for and inspect:

  ```text
  Heaviside
  step
  hard switch
  0 -> 1
  max(
  min(
  threshold completion
  ```

  Any appearance must either be in the forbidden-model discussion or removed.

- [ ] **Step 39: Pass 3, state/rate double-counting review.**

  Confirm:

  ```text
  xi_eq is a target, not the actual state;
  xi is the actual progress;
  k controls approach speed;
  barrier lowering modifies k, not xi directly.
  ```

- [ ] **Step 40: Pass 4, thermodynamic equilibrium review.**

  Confirm:

  ```text
  lattice-gas equation is smooth;
  homogeneous equilibrium width direction is correctly explained;
  Gaussian language is not treated as a thermodynamic necessity.
  ```

- [ ] **Step 41: Pass 5, charge conservation review.**

  Confirm:

  ```text
  V_n is implicit;
  V_app bridge is not confused with V_n;
  implicitness is not described as an algebraic failure.
  ```

- [ ] **Step 42: Pass 6, effective barrier review.**

  Confirm:

  ```text
  Delta G_eff has energy per mol units;
  W_el has energy per mol units;
  sign convention matches "positive assistance lowers barrier";
  invalid large-driving region is bounded without artificial clipping.
  ```

- [ ] **Step 43: Pass 7, local ODE review.**

  Confirm:

  ```text
  dxi/dt = k(xi_eq - xi) has correct sign;
  residual equation has correct sign;
  L = v_Q/k has charge units.
  ```

- [ ] **Step 44: Pass 8, spectrum mapping review.**

  Confirm:

  ```text
  G -> L mapping is exponential;
  inverse G(L) is correct;
  Jacobian RT/L is correct;
  A_L is not confused with rho_G.
  ```

- [ ] **Step 45: Pass 9, ICA mapping review.**

  Confirm:

  ```text
  dQ/dV expression follows from dQ = C_bg dV + Q_phase dxi;
  denominator sign and dimensions are explicitly explained;
  measured V_app limitations are stated.
  ```

- [ ] **Step 46: Pass 10, falsification/non-identifiability review.**

  Confirm:

  ```text
  competing mechanisms are named;
  current-dependence alone is not overclaimed;
  potential-assistance hypothesis is presented as testable, not proven.
  ```

- [ ] **Step 47: Repair critical defects found in Passes 1-10.**

  Only repair confirmed logic defects. Do not rewrite unrelated sections for style.

- [ ] **Step 48: Run static brace/environment check.**

  Use a simple static scan:

  ```text
  count braces, begin/end environments, labels, refs
  ```

- [ ] **Step 49: Run banned-pattern check.**

  Search the final manuscript for forbidden patterns and record context.

- [ ] **Step 50: Run label/ref inventory.**

  Confirm that every `\ref`/`\eqref` target exists or record unresolved references.

- [ ] **Step 51: Run citation inventory.**

  Confirm that every `\cite` target has a corresponding `thebibliography` item.

- [ ] **Step 52: Record unresolved literature boundaries.**

  Specifically record:

  ```text
  user refs 6/7 not fully integrated unless independently verified;
  citations used as general theoretical anchors;
  no claim of experimental validation.
  ```

- [ ] **Step 53: Save the 10-pass review report.**

  Create:

  ```text
  D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_CH1_REBUILD_LOGIC_REVIEW_10PASS.md
  ```

- [ ] **Step 54: Decide gate status.**

  Mark:

  ```text
  PASS_10_LOGIC_LOOPS
  ```

  only if critical and high-severity logic defects are absent after repair.

Gate `PASS_10_LOGIC_LOOPS`:

- 10 logic passes are documented.
- Any found critical issue is repaired or explicitly marked as unresolved.
- Static TeX checks have run.
- No forbidden step-function completion model remains as adopted theory.

## Phase 008 — Final Repair, Ledger, Handover

- [ ] **Step 55: Apply final critical repairs.**

  Repair only defects found in Phase 007.

- [ ] **Step 56: Re-run static checks after repairs.**

  Repeat brace/environment, label/ref, cite, and banned-pattern scans.

- [ ] **Step 57: Read final manuscript sections.**

  Read the final `.tex` from start to end and confirm that all 12 sections exist.

- [ ] **Step 58: Write final ledger.**

  Create:

  ```text
  D:\Projects\Project_Anode_Fit\Codex\results\PHASE_005_008_CH1_REBUILD_LEDGER.md
  ```

  Include:

  ```text
  phase
  planned steps
  actual steps
  status
  plan path
  result path
  manuscript artifact
  validation summary
  gate status
  next step
  ```

- [ ] **Step 59: Write handover.**

  Create:

  ```text
  D:\Projects\Project_Anode_Fit\Codex\results\PHASE_008_CH1_REBUILD_HANDOVER.md
  ```

  Include:

  ```text
  plan path
  comparison report path
  final manuscript path
  logic review path
  ledger path
  unresolved items
  next recommended phase
  ```

- [ ] **Step 60: Record confirmed non-changes.**

  State that no Claude files and no original source files were modified.

- [ ] **Step 61: Record output status.**

  Mark the manuscript as:

  ```text
  Chapter 1 rebuilt candidate after 10-pass logic loop
  ```

  Do not call it publication-final if literature verification or user review remains.

- [ ] **Step 62: Prepare user-facing summary.**

  Summarize:

  ```text
  what was created
  what logic changed from Claude
  what remains unresolved
  where files are
  ```

- [ ] **Step 63: Check git status.**

  Inspect changed files without committing.

- [ ] **Step 64: Do not commit unless explicitly asked.**

  The user did not request Codex commit in this task.

- [ ] **Step 65: Final response.**

  Provide file paths and gate status.

- [ ] **Step 66: If compaction occurs before final response, resume from saved plan and ledger.**

  Open:

  ```text
  D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-chapter1-rebuild-claude-strengths-spectrum-plan.md
  D:\Projects\Project_Anode_Fit\Codex\results\PHASE_005_008_CH1_REBUILD_LEDGER.md
  ```

  Then continue from the recorded next step.

- [ ] **Step 67: If critical unresolved logic remains, do not report final completion.**

  Report the unresolved item and the exact section/equation affected.

- [ ] **Step 68: If all gates pass, report completion as a reviewed candidate.**

  Use:

  ```text
  챕터1 재작성 후보 완성, 10-pass logic review 완료
  ```

  Do not overstate experimental validation.

Gate `PASS_REBUILD_HANDOVER_READY`:

- Final manuscript exists.
- Review report exists.
- Ledger exists.
- Handover exists.
- No unverified source claim is reported as verified.

## Implementation Interfaces

### Required Central Equation Set

Smooth equilibrium target:

```latex
\xi_{\eq,j}(V_n,T)=
\frac{1}{1+\exp[-s_j(V_n-U_j(T))/w_j(T)]}
```

Local relaxation:

```latex
\frac{\dd \xi_j}{\dd t}
=
k_j(T,V_n)[\xi_{\eq,j}(V_n,T)-\xi_j]
```

Residual ODE:

```latex
\frac{\dd r_j}{\dd Q}+\frac{k_j}{v_Q}r_j
=
\frac{\dd \xi_{\eq,j}}{\dd Q}
```

Effective barrier:

```latex
\Delta G_{\eff,j}
=
\Delta G_{a,j}(T)-W_{\mathrm{el},j}(V_n,T)
```

Rate:

```latex
k_j
=
\nu_j(T)\exp[-\Delta G_{\eff,j}/(RT)]
```

Relaxation length:

```latex
L=\frac{v_Q}{k}
```

Barrier-to-length mapping:

```latex
L(G,T,\psi)
=
\frac{v_Q}{k_0(T)}
\exp[(G-W_\psi)/(RT)]
```

Length spectrum:

```latex
A_L(L;T,\psi)=
\rho_G(G(L,T,\psi);T,\psi)\frac{RT}{L}A_0(L;T,\psi)
```

Observed tail kernel:

```latex
\mathcal T(Q;T,\psi)
=
\int_0^\infty
A_L(L;T,\psi)
\frac{1}{L}
\exp[-(Q-Q_a)/L]\,\dd L
```

### Required Logic Statements

- `activation free-energy barrier` controls `rate constant`, not direct state completion.
- `electrode-potential assistance` lowers the effective barrier smoothly.
- The local single exponential is a kernel, not the measured tail as a whole.
- The measured tail is a `relaxation-length spectrum` mixture.
- `low T` lengthens the tail through smaller rates/larger relaxation lengths.
- `high T` shortens the tail through larger rates/smaller relaxation lengths.
- Positive potential assistance shortens relaxation lengths.
- Homogeneous equilibrium width alone cannot explain the low-temperature long tail direction.
- Falsification against polarization, diffusion, and heterogeneity remains mandatory.

## Test Plan

### Static File Checks

Run:

```powershell
Test-Path -LiteralPath 'D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v1.tex'
```

Expected:

```text
True
```

### Section Inventory Check

Run a `Select-String` or equivalent scan for:

```text
\section{Convention
\section{Observation
\section{State Variable
\section{Charge Conservation
\section{Local Relaxation
\section{Effective Activation
\section{Barrier-To-Rate
\section{Relaxation-Length Spectrum
\section{Self-Consistent
\section{ICA
\section{Falsification
\section{Deliverables
```

Expected: all 12 section headings found.

### Banned Adopted-Model Check

Search for:

```text
Heaviside
hard switch
0 -> 1
\max
\min
threshold completion
```

Expected: any hits are only in the forbidden-model explanation or validity-warning prose, not in adopted equations.

### Equation Logic Check

Manual checks:

- `\Delta G_{\eff}` has the same unit as `\Delta G_a` and `W_el`.
- Positive `W_el` increases `k`.
- Increasing `k` decreases `L`.
- The residual equation sign makes `r` decay when `d xi_eq / dQ` is small.
- `A_L` includes the Jacobian `RT/L`.

### Citation Inventory Check

Manual or grep check:

- Every `\cite{...}` key exists in the `thebibliography`.
- No unsupported DOI or exact bibliographic claim is invented without source verification.

### Logic Review Check

The 10-pass review file must explicitly mark each pass as:

```text
PASS
REPAIRED
UNRESOLVED
```

Critical unresolved items block final completion.

## Assumptions

- The current rewrite can use general established theory references for `lattice-gas`, `transition state theory`, `Butler-Volmer`/transfer-coefficient style barrier lowering, and graphite ICA literature.
- The user's refs 6/7 are known to be relevant to feedback/self-consistent integral solution methods, but this plan does not claim their full integration until bibliographic and variable-mapping verification is performed.
- The current chapter is a theoretical candidate, not experimental validation.
- `V_n` is the correct primary theoretical potential; `V_app` is a measured bridge that may include ohmic, kinetic, and transport terms.
- The `relaxation-length spectrum` is a reduced representation of heterogeneous local kinetics, not a claim that only one microscopic source of heterogeneity exists.

## Correction History

- Supersedes `2026-05-28-chapter1-activation-barrier-spectrum-plan.md` because that earlier plan produced a compact mechanism note but did not fully absorb Claude Code's manuscript-level strengths.
- Incorporates user clarification that `activation barrier` is valid; the invalid old model was the discontinuous step-function completion.
- Incorporates user preference for Korean prose with English academic terms.
- Incorporates Phase 004 comparison result: Claude's structure should be retained, but Claude's single-mode tail emphasis must be upgraded to a relaxation-length spectrum kernel theory.
