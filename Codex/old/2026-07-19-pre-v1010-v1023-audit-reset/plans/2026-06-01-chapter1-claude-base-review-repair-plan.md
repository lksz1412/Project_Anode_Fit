# Chapter 1 Claude-Base Review and Repair Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:verification-before-completion` before any completion claim. This plan is for reviewing and repairing Claude-based Chapter 1 into a Codex completed candidate. Do not start by rewriting from zero.

**Goal:** Review Claude rebuilt Chapter 1 with small-chunk 10-pass scrutiny, classify problems, and repair it so Chapter 1 is logically followable, physically meaningful, and self-contained enough to produce a simple real-data ICA tail fitting approximation.

**Architecture:** Use `graphite_ica_ch1_rebuilt.tex` from the copied Claude reference set as the base. Create a Codex working copy, then repair only after the chunked review identifies concrete defects. The repair must preserve useful Claude derivations while improving section 7+ continuity, variable meaning, kernel/integral explanation, fitting usability, and manuscript hygiene.

**Tech Stack:** LaTeX manuscript source, PowerShell line-chunk scanner, manual physics/math review, static ref/cite checks, optional XeLaTeX build.

---

## Summary

The user flagged the following Chapter 1 failure mode:

- Sections 1--6 are dense but mostly logically traceable.
- From section 7 onward, equations and integrals appear without enough physical motivation.
- The reader cannot tell what quantity is being calculated or why a new variable/spectrum/integral is meaningful.
- The link from previous ODE/barrier logic to spectrum/kernel/fitting is too abrupt.
- Chapter 1 should itself give a simple real-data fitting approximation, instead of forcing the reader to wait for Chapter 6.
- Review must be done in small chunks and multiple passes, because one whole-document pass can miss followability failures.

This plan treats those comments as acceptance criteria, not optional polish.

## Current Ground Truth

Active base file:

`D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch1_rebuilt.tex`

Static snapshot from copied base:

```text
content lines: 839
SHA256: 2AFD3B0B4B9D66EE373240A5238673590259F8C366B6257C14F9B702D6909A07
begin/end: 49/49
brace count: 1108/1108
labels: 46
refs: 33
missing refs: none
cites: 21
bibitems: 21
missing cites: none
```

Known current structure:

- Intro and observation.
- Notation.
- Graphite staging.
- Charge conservation and internal potential.
- Equilibrium progress / logistic target.
- Effective barrier and rate constant.
- Progress dynamics and single-mode kernel.
- Barrier distribution to relaxation-length spectrum.
- Kernel integral.
- Self-consistent Volterra / Plan B / Plan A closure.
- ICA/DVA and fitting expression.
- Simple single-mode fitting approximation.
- Temperature dependence / falsification / identifiability.
- Plan B numerical appendix.
- Chapter 2--5 handoff.

Initial Codex reading:

- Claude's latest copy has improved the section 7+ jump by adding single-mode-to-Volterra derivation.
- However, it may have overcorrected by putting too much solver/fitting/Plan A/B machinery into Chapter 1.
- The repair should not discard useful content; it should reorganize and clarify it.

## Phase Range

| Phase | Name | Step Range | Purpose |
|---|---|---:|---|
| 022A | Ch1 source freeze and working copy | 1-8 | Copy Claude Ch1 into a Codex working file and verify static state. |
| 022B | 10-pass chunked review | 9-38 | Run ten full-file reviews with different chunk sizes and lenses. |
| 022C | Defect classification and repair map | 39-58 | Classify findings and map them to concrete repair actions. |
| 022D | Section 7+ repair design | 59-92 | Design specific repairs for spectrum/kernel/closure/fitting sections. |
| 022E | Verification gates and execution handoff | 93-115 | Define exact checks required before any repaired Ch1 can be called complete. |

## Non-goals

- Do not edit the Claude reference file.
- Do not bring back old Codex Chapter 1 as the base.
- Do not rewrite Chapter 1 from zero unless review shows the base is unrecoverable.
- Do not remove Chapter 6 content blindly; first classify whether it belongs in Ch1, Ch6, or an appendix.
- Do not hide numerical solver requirements inside the theoretical proof.
- Do not call a fitting convenience a thermodynamic identity.
- Do not add new assumptions without marking them as established, bounded, flagged, or requiring verification.

## Implementation Changes

Create:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_rebuilt_codex_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_022_CH1_CLAUDE_BASE_10PASS_REVIEW.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_022_CH1_DEFECT_LEDGER.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_022_CH1_REPAIR_MAP.md`
- `D:\Projects\Project_Anode_Fit\Codex\work\scan_ch1_codex_chunks.ps1`

Modify later, only after review:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_rebuilt_codex_v1.tex`

Do not modify:

- `Codex/results/PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01/graphite_ica_ch1_rebuilt.tex`
- Claude directory files.

## Phase 022A - Source Freeze and Working Copy

- [ ] **Step 1: Verify the active base path.**

  Run:

  ```powershell
  Get-Item 'D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch1_rebuilt.tex'
  ```

  Expected: file exists and timestamp/hash match the manifest.

- [ ] **Step 2: Create a Codex working copy.**

  Copy:

  ```powershell
  Copy-Item `
    'D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch1_rebuilt.tex' `
    'D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_rebuilt_codex_v1.tex'
  ```

  Expected: reference remains untouched.

- [ ] **Step 3: Record static baseline.**

  Extract:

  - line count;
  - SHA256;
  - begin/end balance;
  - brace balance;
  - labels/refs/cites/bibitems;
  - section headings.

- [ ] **Step 4: Save Phase 022A result.**

  Expected: baseline is written before review or editing.

## Phase 022B - 10-Pass Chunked Review

All ten passes read the full working copy, but each pass uses a different chunk size. The point is to prevent one context window from swallowing section boundaries and to force repeated local reading.

### Chunk Sizes

Use these exact chunk sizes:

```text
Pass 1: 37 lines
Pass 2: 49 lines
Pass 3: 61 lines
Pass 4: 73 lines
Pass 5: 89 lines
Pass 6: 109 lines
Pass 7: 131 lines
Pass 8: 157 lines
Pass 9: 191 lines
Pass 10: 233 lines
```

For each pass, record:

- chunk size;
- chunk count;
- line ranges read;
- findings by line number;
- unresolved questions;
- whether the pass found `잘못`, `부족`, `개선`, `좋은 점`, or `추가 검증 필요`.

### Pass Definitions

- [ ] **Step 5: Pass 1 - User-critique replay, 37-line chunks.**

  Question:

  ```text
  Would the user still feel that section 7+ introduces integrals abruptly?
  ```

  Check:

  - every integral after section 7 has a preceding physical motivation;
  - every new variable has a plain-language meaning;
  - transition from sections 1--6 to 7+ is explicit.

- [ ] **Step 6: Pass 2 - Section-boundary continuity, 49-line chunks.**

  Check:

  - intro -> notation;
  - charge conservation -> equilibrium target;
  - equilibrium target -> barrier/rate;
  - rate -> single-mode kernel;
  - single-mode kernel -> spectrum;
  - spectrum -> ICA/fitting.

- [ ] **Step 7: Pass 3 - Variable physical meaning, 61-line chunks.**

  For each of these symbols, require a meaning and a unit/domain:

  ```text
  q, Q_ext, Q_cell, V_n, V_app, V_drive,
  xi_j or theta_j, Theta, Q_p, G, A_j,
  Delta G_eff, k_j, L, A_L, rho_G, A_0,
  K(q,q'), Theta_init, Theta_A, c(q), b(q)
  ```

- [ ] **Step 8: Pass 4 - Equation provenance, 73-line chunks.**

  For every displayed equation, classify:

  - definition;
  - derived result;
  - approximation;
  - ansatz;
  - fitting convenience;
  - numerical/solver instruction.

  Equations that are not classified become repair targets.

- [ ] **Step 9: Pass 5 - Physics consistency, 89-line chunks.**

  Check:

  - ideal equilibrium width argument is not overgeneralized;
  - effective barrier is not treated as a step-function;
  - potential assistance is smooth;
  - common-mode mobility and directional reaction kinetics are not confused;
  - dynamic lag is not mislabeled as equilibrium thermodynamics.

- [ ] **Step 10: Pass 6 - Dimensional/sign audit, 109-line chunks.**

  Check:

  - \(G\), \(\Delta G\), \(RT\): J/mol;
  - \(\rho_G\): mol/J if \(G\) is J/mol;
  - \(L\) or \(L_q\): dimensionless in normalized charge coordinate;
  - \(A_L\) dimension depends on whether it is probability density or amplitude density;
  - \(dQ/dV\) and \(dV/dq\) conversions.

- [ ] **Step 11: Pass 7 - Spectrum and kernel audit, 131-line chunks.**

  Check:

  - \(A_L\) is not overloaded;
  - the \(RT/L\) Jacobian and kernel \(1/L\) have separate origins;
  - discrete mode summation to continuous integral is explained;
  - \(q_a\), \(L\), and amplitude are not mutually free without warning.

- [ ] **Step 12: Pass 8 - Self-consistency / Plan A/B audit, 157-line chunks.**

  Check:

  - Volterra equation is motivated before shown;
  - Plan A is clearly bounded and not presented as established;
  - Plan B is not turned into a solver implementation inside theory proof;
  - ratio-substitution from user's refs 6/7 is mapped carefully and not overclaimed.

- [ ] **Step 13: Pass 9 - Simplefit usability audit, 191-line chunks.**

  Check whether Chapter 1 alone lets a reader do:

  - choose a tail window;
  - fix \(q_a\);
  - subtract background/equilibrium contribution;
  - fit a single exponential tail;
  - extract \(L\);
  - relate \(L(T,V)\) to \(G-\chi\mathcal A\);
  - know when the single-mode approximation fails.

- [ ] **Step 14: Pass 10 - Manuscript hygiene and scope audit, 233-line chunks.**

  Check:

  - no paper-facing work history;
  - no `RB plan`, `Date`, `Author`, process labels in final candidate;
  - Ch6 references are either purposeful or redistributed;
  - chapter handoff is clear.

- [ ] **Step 15: Save 10-pass review report.**

  Expected file:

  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_022_CH1_CLAUDE_BASE_10PASS_REVIEW.md`

## Phase 022C - Defect Classification and Repair Map

- [ ] **Step 16: Classify findings by severity.**

  Severity classes:

  - Critical: mathematical/physical contradiction.
  - High: reader cannot follow or chapter deliverable fails.
  - Medium: ambiguous convention/scope/assumption.
  - Low: manuscript polish.

- [ ] **Step 17: Classify findings by type.**

  Required buckets:

  - `잘못된 부분`
  - `부족한 부분`
  - `개선할 부분`
  - `좋은 점/흡수할 부분`
  - `추가 검증 필요`

- [ ] **Step 18: Create a section repair map.**

  Expected map:

  | Section | Keep | Repair | Move/Appendix | Verify |
  |---|---|---|---|---|
  | Intro | observation-first framing | remove process metadata | none | user-critique alignment |
  | Notation | most definitions | resolve xi/theta and L/L_q policy | none | convention |
  | Charge conservation | keep | make derivative bridge visible | none | units/sign |
  | Equilibrium target | keep | narrow ideal-width claim | none | physics |
  | Effective barrier | keep | front-load common-mode mobility boundary | Ch3 directional kinetics | detailed balance |
  | Single-mode kernel | keep | ensure L constant assumptions visible | none | followability |
  | Spectrum | keep idea | reduce A_L overload | none | dimension |
  | Kernel integral | keep | derive from discrete sum before integral | none | meaning |
  | Volterra/Plan A/B | demote | make boundary/appendix | possible Ch6 | scope |
  | ICA/DVA | keep | bridge q/Q/V axes cleanly | none | units |
  | Simplefit | keep and expand | operational recipe | none | usability |
  | Numeric appendix | compress/move | remove solver dominance | Ch6/appx | scope |

- [ ] **Step 19: Save defect ledger and repair map.**

  Expected:

  - `PHASE_022_CH1_DEFECT_LEDGER.md`
  - `PHASE_022_CH1_REPAIR_MAP.md`

## Phase 022D - Section 7+ Repair Direction

This phase defines the actual repair direction before edits.

- [ ] **Step 20: Repair spectrum section.**

  Direction:

  - Start from a finite set of local modes.
  - State that each mode has a barrier \(G_m\), rate \(k_m\), and length \(L_m\).
  - Show the discrete sum:

    ```latex
    \frac{\dd\Theta_{\tail}}{\dd q}
    \simeq
    \sum_m a_m \frac{1}{L_m}e^{-(q-q_a)/L_m}
    ```

  - Then take the continuum limit.

  Reason:

  - This prevents the integral from appearing abruptly.

- [ ] **Step 21: Repair \(A_L\) meaning.**

  Direction:

  - Define a probability spectrum and an amplitude spectrum separately.
  - If keeping \(A_L\), state explicitly:

    ```text
    A_L(\lambda)d\lambda is the amount of tail-amplitude carried by modes whose relaxation length lies in [lambda, lambda+d lambda].
    ```

  - Do not let the reader wonder whether \(A_L\) is probability, capacity, or fitting amplitude.

- [ ] **Step 22: Repair kernel integral.**

  Direction:

  - Before the equation, write:

    ```text
    The observed tail is the sum of each local mode's progress derivative, not the sum of residuals.
    ```

  - After the equation, explain:

    - integration variable;
    - kernel;
    - amplitude density;
    - why low temperature shifts weight to large lengths.

- [ ] **Step 23: Repair Volterra/Plan A/B placement.**

  Direction:

  - Main text: state self-consistency as a boundary.
  - Appendix or later Ch6: detailed Plan A/B.
  - If Plan A remains in Chapter 1, label it clearly as `optional analytic closure`, not central theory.

- [ ] **Step 24: Repair simplefit section.**

  Direction:

  Add a boxed practical formula:

  ```latex
  Y_{\tail}(q)
  =
  \left(\frac{\dd Q}{\dd V}\right)_{\mathrm{meas}}
  -
  \left(\frac{\dd Q}{\dd V}\right)_{\mathrm{baseline}}
  \approx
  B\exp[-(q-q_a)/L]
  ```

  Then define:

  - what baseline means;
  - how \(q_a\) is fixed;
  - what \(B\) contains;
  - how \(L\) maps to barrier expression;
  - when curvature in semi-log plot signals spectrum rather than single-mode.

- [ ] **Step 25: Repair fitting-vs-theory scope.**

  Direction:

  - Keep minimal simplefit in Chapter 1.
  - Move full numerical implementation and DAE/root-find details to appendix/Ch6.
  - Leave enough logic in Chapter 1 to understand why the fitting expression has physical meaning.

- [ ] **Step 26: Repair manuscript metadata.**

  Direction:

  - Remove visible paper-body process labels.
  - Keep work history in phase result files only.

- [ ] **Step 27: Save section 7+ repair design.**

  Expected:

  `PHASE_022_CH1_SECTION7_REPAIR_DESIGN.md`

## Phase 022E - Verification Gates and Execution Handoff

- [ ] **Step 28: Define followability gate.**

  A section passes only if:

  - every equation has a preceding physical sentence;
  - every equation has a following interpretation;
  - every integral says what is integrated and what the result measures;
  - assumptions are stated before use.

- [ ] **Step 29: Define usability gate.**

  Chapter 1 passes only if a reader can extract a simple \(L\) from real data using Chapter 1 alone.

- [ ] **Step 30: Define scope gate.**

  Chapter 1 passes only if solver/Plan A/B details do not dominate the main proof.

- [ ] **Step 31: Define static gate.**

  Required checks:

  ```text
  begin/end match
  braces match
  no missing refs
  no missing cites
  no duplicate labels
  no process metadata in body
  no unexplained new symbols
  ```

- [ ] **Step 32: Define build gate.**

  If `xelatex` is available:

  - run two passes;
  - record PDF page count;
  - record undefined reference/citation warnings;
  - record overfull hbox warnings.

  If unavailable:

  - report `xelatex NOT_FOUND`.

- [ ] **Step 33: Define completion report format.**

  Final Chapter 1 repair result must include:

  - input file;
  - output file;
  - exact lines/sections changed;
  - before/after logic summary;
  - 10-pass review summary;
  - static/build verification;
  - remaining uncertainties.

- [ ] **Step 34: Save execution handoff.**

  Expected:

  `PHASE_022_CH1_REVIEW_REPAIR_HANDOVER.md`

## Test Plan

Before any edit:

```powershell
# line count, SHA256, refs/cites, section headings
```

During review:

```powershell
# chunk scanner with sizes 37,49,61,73,89,109,131,157,191,233
```

After repair:

```powershell
# static LaTeX integrity
# high-risk pattern search
# optional xelatex 2-pass build
```

High-risk patterns:

```text
Date:
Author:
RB 재구성본
plan 2026
audit
phase
TBD
TODO
step-function
0 -> 1
unexplained Plan A
unexplained solver
```

## Assumptions

- Claude Chapter 1 is recoverable and should be repaired, not discarded.
- The user's critique is strongest for section 7 onward, but sections 1--6 still require bridge review because their notation feeds section 7+.
- Chapter 1 should include a simple fitting approximation, but not a full numerical solver.
- Chapter 6 may remain as fitting/numerical practice only after Chapter 1 becomes self-contained.

## Correction History

- 2026-06-01: Plan rewritten after user clarified that Codex must archive old Codex drafts and build from the copied Claude rebuilt set.

