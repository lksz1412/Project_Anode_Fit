# Rebuild Readiness Assessment Report

Project: `D:\Projects\Project_Anode_Fit`

Date: 2026-05-27

Prepared by: Codex

Related plan/ledger:

- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_007_EXECUTION_LEDGER.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_ANODE_DQDV_HANDOVER.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\chapter1_rewrite_spec.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_development_draft.tex`

## 1. Executive Summary

The current state is good enough to start a full rebuild, but not good enough to treat the existing draft as the final manuscript base.

The most important technical understanding is:

```text
Q_cell q = Q_bg(V_n,T) + sum_j Q_j,tot xi_j
```

must be the foundation. `V_n` is solved from charge balance. It is not read from a prescribed OCV curve. Once `V_n` is solved, it determines `xi_eq`, kinetic rates, apparent voltage, and finally ICA/DVA observables.

The main circularity is:

```text
xi_j -> charge balance -> V_n -> xi_eq/k_j -> dxi_j/dq or dxi_j/dt -> xi_j
```

This should not be described as a fatal contradiction. It is a self-consistent algebraic/dynamic system. The correct rebuild direction is to define it as a charge-balance-constrained nonlinear Volterra/DAE system, then introduce a reference-closure method inspired by refs. 6/7 only after the exact coupled problem is stated.

User's latest instruction changes the work direction:

- Do not patch or polish the existing draft.
- Do not start from `graphite_ica_chapter1_development_draft.tex` as the manuscript body.
- Use all prior files only as reference/evidence.
- Write a new document from a blank structure.

## 2. What Was Understood

### 2.1 Project-Level Structure

Confirmed:

- `graphite_ica_dynamic_ver5.tex` is a merged historical document, not a clean final manuscript.
- The internal `ver.1`-`ver.5` layers should be reinterpreted as Chapter 1-5.
- Historical `ver.1` in the ver5 file is no longer the intended Chapter 1 core.
- Corrected `graphite_ica_charge_balance_ver1_rechecked2.tex` is the better source for the new Chapter 1 foundation.

Current chapter interpretation:

| New Chapter | Source Layer | Role |
|---:|---|---|
| Chapter 1 | corrected ver1 | thermodynamic charge balance and internal graphite potential |
| Chapter 2 | historical ver2 | heat / temperature coupling |
| Chapter 3 | historical ver3 | electrochemical kinetic interface |
| Chapter 4 | historical ver4 | integrated state / observation / fitting system |
| Chapter 5 | historical ver5 | hysteresis / branch / structural memory |

### 2.2 Correct Chapter 1 Foundation

Confirmed:

- Use `Q_ext=Q_cell q` as the external charge coordinate.
- Use charge balance to solve `V_n`.
- Treat equilibrium OCV as a derived special case:

```text
Q_cell q = Q_bg(V,T) + sum_j Q_j,tot xi_eq,j(V,T)
```

- Distinguish `V_n`, `V_app`, and `V_drive`.
- Evaluate kinetics and derivatives only after `V_n` has been solved.

### 2.3 The Feedback Problem

Confirmed:

- The corrected ver1 explicitly creates feedback.
- That feedback is not automatically wrong.
- It becomes wrong only if the manuscript presents dependent quantities as if they were independent inputs.
- The solution is to introduce a root-solve operator or equivalent algebraic constraint before using `V_n` in downstream equations.

Correct class:

```text
algebraic root solve + nonlinear state evolution
= charge-balance-constrained DAE
= Volterra-like integral form in q/time after integration
```

### 2.4 Role Of The User's Paper And Refs. 6/7

Confirmed from the 2017 JCP paper:

- refs. 6/7 are invoked for Fredholm integral equations of the second kind;
- the 2017 paper uses a reference-ratio closure pattern;
- the physical geminate-pair model is not portable to graphite;
- the mathematical closure idea is portable.

Portable pattern:

```text
self-consistent integral form
-> isolate unknown feedback as ratio/correction
-> choose a simpler reference solution
-> close the expression using that reference
-> validate against direct numerical solution
```

Non-portable parts:

- geminate-pair recombination physics;
- Smoluchowski diffusion coordinate;
- external-field orientation averaging;
- contact-radius / delta-sink / Onsager physical assumptions.

## 3. What Went Well

### 3.1 Source Coverage Became Clear

Good:

- ver5 source was read fully and mapped to a Chapter 1-5 candidate structure.
- corrected ver1 was read fully and audited for dependencies.
- the JCP 2017 PDF text was extracted across all 10 pages.
- refs. 6/7 were identified and their in-text use in the 2017 paper was located.

Why this matters:

- The rebuild can now start from actual source coverage, not from memory or ChatGPT-style reconstruction.

### 3.2 The Major Logical Error Was Located

Good:

- The error is no longer vaguely described as "circular variable reuse."
- It is specifically the lack of a declared solution method for:

```text
V_n = root(q,T,xi)
xi = integral/update involving V_n[xi]
```

Why this matters:

- This turns a conceptual contradiction into a solvable mathematical formulation.

### 3.3 ver5 Structure Was Useful

Good:

- ver5 successfully revealed the intended stack:
  thermodynamics -> heat -> kinetics -> full fitting -> hysteresis.

Why this matters:

- Even though the old body should not be patched, the macro-architecture can be reused.

### 3.4 Corrected ver1 Is A Stronger Foundation

Good:

- corrected ver1 contains the right central move: internal voltage from charge conservation.
- it also already distinguishes internal/apparent/driving voltages and external charge vs internal storage.

Why this matters:

- The rebuild can preserve the correct physical spine while discarding the unstable old narrative.

### 3.5 Guardrails Are Now Known

Good:

- `Q_ext` must remain the ICA/DVA capacity axis.
- `V_n` must not be demoted back to `V_OCV(q,T)`.
- heat should use `dxi/dt`, not only q-derivatives.
- `R_n` and `k_j` must not be freely co-fitted without staged constraints.
- hysteresis must not be allowed to violate charge balance.

## 4. What Is Still Insufficient

### 4.1 The Existing Draft Is A Skeleton, Not A Full Manuscript

Current draft:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_development_draft.tex`

Insufficient because:

- it is only Chapter 1;
- it is mostly mathematical scaffolding;
- it does not yet develop the narrative from physical problem to fitting method;
- it does not include Chapter 2-5 as real chapters;
- it does not include numerical examples, fitting workflow, parameter staging, or synthetic validation.

### 4.2 The Reference Closure Is Not Yet Operational

Current state:

- We know the closure pattern from refs. 6/7.
- We have not yet chosen the exact graphite reference problem.
- We have not defined the correction functional in a validated way.

Missing:

- direct DAE/root-solve benchmark;
- quasi-equilibrium baseline definition;
- frozen-feedback closure definition;
- residual criteria for accepting a closed approximation;
- proof or numerical evidence of when the closure is valid.

### 4.3 The Full refs. 6/7 Papers Were Not Read

Current state:

- The 2017 paper's use of refs. 6/7 was extracted.
- Metadata for refs. 6/7 was checked.
- The full original refs. 6/7 papers were not locally read.

Implication:

- The current understanding is enough to state the closure pattern cautiously.
- It is not enough to reproduce or extend the original derivation in detail.

### 4.4 No LaTeX Build Was Performed

Current state:

- `pdflatex`, `xelatex`, and `lualatex` were unavailable.
- Targeted checks passed, but no PDF was generated.

Implication:

- Layout, Korean typesetting, equation overflow, bibliography rendering, and PDF-level polish remain unverified.

### 4.5 Data/Fitting Layer Is Not Yet Grounded In Actual Data

Current state:

- The work is theoretical/document-level.
- No real LIB dQ/dV dataset was loaded.
- No parameter fit was attempted.

Implication:

- Identifiability risks are known conceptually but not numerically ranked.

## 5. What Was Wrong Or Risky

### 5.1 Treating The Existing Draft As The New Manuscript Would Be Wrong

Reason:

- It was generated as a development draft after a planning/audit phase.
- It is too close to an explanatory scaffold.
- It does not yet have a clean manuscript architecture.

Correction:

- Archive it as a reference sketch.
- Start a new manuscript from blank structure.
- Reintroduce only selected equations and ideas after a new outline is fixed.

### 5.2 Forcing The Graphite Problem Into A Fredholm Label Would Be Wrong

Reason:

- refs. 6/7 are Fredholm second-kind sources in the 2017 paper.
- graphite state evolution in q/time is naturally causal and Volterra-like after integration.

Correction:

- Use:

```text
primary exact model: DAE / nonlinear Volterra
optional approximation: refs. 6/7-inspired reference closure
```

### 5.3 Using `V_OCV(q,T)` As A Primary Input Would Recreate The Original Error

Reason:

- corrected ver1 explicitly replaces that with charge-balance root solving.

Correction:

- Define `V_OCV` only after equilibrium charge balance is written.
- Use a root operator for dynamic `V_n`.

### 5.4 Mixing Thermodynamics, Kinetics, Heat, And Hysteresis Too Early Would Overfit

Reason:

- each layer can absorb the same peak shifts or broadening.
- `Q_bg`, `Q_j,tot`, `w_j`, `R_n`, `k_j`, temperature terms, and hysteresis can become mutually degenerate.

Correction:

- staged fitting:
  1. thermodynamic low-rate shape;
  2. charge-balance residual and peak area;
  3. kinetic lag;
  4. thermal correction;
  5. hysteresis only after residuals prove it is needed.

### 5.5 Leaving `Q_bg` As A Cosmetic Baseline Would Be Wrong

Reason:

- corrected ver1 uses `Q_bg` as a storage term inside charge conservation.

Correction:

- Treat `Q_bg(V,T)` as a real background capacity reservoir with slope, endpoint, and residual constraints.

### 5.6 Reusing Symbols Without A Naming Discipline Would Be Risky

Risk examples:

- `w_j` as width vs capacity fraction;
- `V_n` vs `V_app` vs `V_drive`;
- modeled internal capacity vs external `Q_ext`;
- dynamic `xi_j` vs equilibrium `xi_eq`.

Correction:

- Reserve `w_j` for transition width.
- Use `a_j=Q_j,tot/Q_cell` for dimensionless capacity fraction.
- Use explicit root operator `\mathcal V(q,T,\boldsymbol{\xi};\theta)`.

## 6. How To Solve The Problems

### 6.1 Rebuild From A Blank Manuscript

Do not patch:

- `graphite_ica_dynamic_ver5.tex`
- `graphite_ica_charge_balance_ver1_rechecked2.tex`
- `graphite_ica_chapter1_development_draft.tex`

Instead create:

```text
D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_rebuilt_manuscript_v1.tex
```

The new manuscript should use prior files only as source evidence.

### 6.2 Separate Exact Formulation From Approximate Closure

The manuscript should first define the exact system:

```text
G(V;q,T,xi)=0
dxi/dq = F(q,xi,V_root(q,T,xi))
```

Only after that should it introduce the closure:

```text
F(q,xi,V_root) = F_ref(q) * C(q; xi, xi_ref)
```

This prevents the closure from being mistaken for a definition.

### 6.3 Make Chapter 1 The Foundation, Not The Whole Theory

Chapter 1 should prove:

- what `V_n` is;
- how charge conservation determines it;
- how OCV is derived;
- how dQ/dV and dV/dQ are computed;
- what residuals must pass.

It should not try to fully solve heat, BV kinetics, global fitting, or hysteresis.

### 6.4 Add A Numerical Benchmark Appendix Or Section

The rebuild should include an explicit benchmark algorithm:

```text
for each q_i:
  solve G(V_i; q_i,T_i,xi_i)=0
  compute xi_eq(V_i,T_i)
  compute k_i
  advance xi_i -> xi_{i+1}
  recompute V_{i+1}
```

This benchmark is the truth model used to test any reference closure.

### 6.5 Define Acceptance Gates

Every proposed fit or closure must report:

- charge-balance residual;
- root uniqueness/conditioning;
- `0 <= xi_j <= 1`;
- capacity closure;
- dQ/dV peak position/area;
- derivative denominator safety;
- direct benchmark mismatch;
- low-rate equilibrium limit.

## 7. Recommended Rebuild Direction

The new manuscript should be structured as follows:

1. Problem statement: why conventional OCV-based dQ/dV fitting is insufficient.
2. Measured charge coordinate and sign conventions.
3. Graphite transition variables and equilibrium occupancy.
4. Charge-balance residual and internal potential root.
5. OCV as equilibrium limit.
6. Dynamic self-consistency as DAE/Volterra system.
7. Reference-closure method inspired by refs. 6/7.
8. ICA/DVA observable derivation.
9. Parameter identifiability and staged fitting.
10. Interfaces to heat, electrochemical kinetics, integrated fitting, and hysteresis.
11. Validation protocol.
12. Limitations and next implementation steps.

## 8. Source And Verification Status

| Item | Status |
|---|---|
| ver5 full read | confirmed in prior phase result |
| corrected ver1 full read | confirmed in prior phase result |
| user JCP paper page text extraction | confirmed, pages 1-10 |
| exact visual verification of PDF equations | not complete |
| full original refs. 6/7 papers | not read |
| LaTeX build | not run, engine unavailable |
| direct numerical solver | not implemented |

## 9. Decision Needed Before Execution

Before actual rewrite execution, decide:

1. Should the new manuscript be only Chapter 1, or a Chapter 1-5 full master skeleton with Chapter 1 filled first?
2. Should the document language be Korean, English, or mixed Korean explanation with English mathematical section titles?
3. Should refs. 6/7 be used at the level already verified from the 2017 paper, or should their full original papers be retrieved and read first?
4. Should the next deliverable be a manuscript-only rebuild or manuscript plus numerical solver specification?
