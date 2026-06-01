# Chapter 1 Codex Rebuild from Claude Review Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:verification-before-completion` before any completion claim. This plan is a manuscript-theory rebuild plan, not an instruction to patch Claude files in place.

**Goal:** Rebuild Chapter 1 into a clean, paper/patent-facing theory chapter that explains graphite ICA post-peak tail behavior with no logical jumps and ends with a simple real-data fitting approximation.

**Architecture:** Use Claude's rebuilt Chapter 1 only as reference material. Preserve its good physical ingredients, but rewrite the chapter around a stricter causal spine: `charge conservation -> equilibrium target -> smooth effective mobility barrier -> single-mode lag -> relaxation-length spectrum -> ICA expression -> simplefit`. Keep solver/DAE/Plan A/B validation outside the main proof unless explicitly needed as an appendix.

**Tech Stack:** LaTeX manuscript source, PowerShell static verification, manual mathematical review, chunked 10-pass audit records.

---

## Summary

The user identified a serious readability and logic-continuity failure in Claude's Chapter 1, especially from section 7 onward:

- integrals appeared abruptly;
- variables did not clearly explain what physical quantity they measure;
- section 7+ did not connect smoothly to sections 1--6;
- the chapter was not self-contained enough to derive a simple real-data fitting approximation;
- prior reviews likely checked correctness without checking followability and usability;
- future review must use smaller chunks and not rely on one long-context pass.

Codex's review confirms that Claude's latest copied version has improved section 7+ compared with the user's reported version, but the chapter still has structural problems:

- too much solver/fitting/Plan A/B machinery in Chapter 1 main text;
- convention drift (`\xi`, plain `L`) against Codex's current `theta`, `Theta`, `L_q` convention;
- process metadata inside the manuscript body;
- overloaded \(A_L\);
- over-generalized equilibrium-broadening argument;
- simplefit section present but not yet operational enough.

This plan proposes a zero-base Codex rewrite of Chapter 1, using Claude's manuscript only as a source of candidate material.

## Current Ground Truth

Reference copies created under Codex:

- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch1_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch2_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch3_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch4_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch5_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_ch6_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_full_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\graphite_ica_refs_rebuilt.tex`
- Manifest: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\manifest.json`

Primary Claude Chapter 1 reference:

```text
Lines: 839 by scanner
SHA256: 2AFD3B0B4B9D66EE373240A5238673590259F8C366B6257C14F9B702D6909A07
Missing refs/cites: none
```

Current Codex-side convention from previous Chapter 1/2 work:

- `q`: primary normalized charge coordinate.
- `Q_ext=Q_cell q`: dimensional charge only when needed.
- `V_n`: internal graphite-anode potential.
- `V_{n,app}`: apparent/measured potential after polarization.
- `theta_j`: local transition progress variable.
- `Theta`: summed transition inventory.
- `theta_eq,j`: equilibrium target.
- `L_q`: normalized relaxation length along `q`.
- `A_L(lambda;T,psi)`: relaxation-length spectrum/density, but to be redefined carefully to avoid probability/amplitude overload.

## Phase Range

| Phase | Name | Step Range | Purpose |
|---|---|---:|---|
| 021 | Source freeze and rebuild charter | 1-12 | Freeze reference files, define target scope, remove process contamination. |
| 022 | Spine and convention rebuild | 13-31 | Establish the causal spine, conventions, and section map. |
| 023 | Mathematical body rewrite | 32-74 | Rewrite the theory sections from charge balance through kernel integral. |
| 024 | Simplefit and falsification layer | 75-104 | Add a minimal usable fitting approximation without turning Ch1 into solver code. |
| 025 | 10-pass review and repair | 105-134 | Run chunked review, repair, static checks, and save results. |

## Non-goals

- Do not modify Claude files.
- Do not patch Claude Chapter 1 in place.
- Do not write solver code.
- Do not place Plan A/B validator machinery in the main proof unless the user explicitly requests it.
- Do not use old equations just because Claude or ChatGPT used them.
- Do not introduce a step-function activation threshold.
- Do not claim equilibrium broadening is impossible in all forms; only the ideal \(RT/F\) broadening argument is established.
- Do not call a dynamic tail term reversible heat.
- Do not put phase/audit/work-history metadata in the LaTeX manuscript body.

## Implementation Changes

Create, if execution is approved:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_codex_rebuild_v6_clean_spine.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_021_CH1_CODEX_REBUILD_CHARTER_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_022_CH1_CODEX_SPINE_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_023_CH1_CODEX_MATH_BODY_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_024_CH1_CODEX_SIMPLEFIT_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_025_CH1_CODEX_REBUILD_10PASS_REVIEW.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_021_025_CH1_CODEX_REBUILD_LEDGER.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_025_CH1_CODEX_REBUILD_HANDOVER.md`

Do not modify:

- Claude directory.
- Existing Codex Chapter 1 artifacts.
- Source PDFs.

## Phase 021 - Source Freeze and Rebuild Charter

- [ ] **Step 1: Verify copied reference set.**

  Run:

  ```powershell
  Get-Content -Raw 'D:\Projects\Project_Anode_Fit\Codex\results\PHASE_020_CLAUDE_REBUILT_REFERENCE_2026-06-01\manifest.json' |
    ConvertFrom-Json | Select-Object Name,SHA256
  ```

  Expected: eight rebuilt `.tex` files are listed.

- [ ] **Step 2: Re-read user critique.**

  Record the critique as the rebuild acceptance criteria:

  - section 7+ must not introduce integrals abruptly;
  - every new variable must state what physical quantity it measures;
  - the reader must be able to follow from sections 1--6 into spectrum/kernel;
  - Chapter 1 alone must produce a simple real-data fitting approximation.

- [ ] **Step 3: Freeze the target chapter scope.**

  Chapter 1 includes:

  - observation;
  - conventions;
  - charge conservation;
  - equilibrium target;
  - smooth effective mobility barrier;
  - single-mode lag;
  - relaxation-length spectrum;
  - kernel integral;
  - ICA expression;
  - simplefit approximation;
  - validity/falsification.

  Chapter 1 excludes:

  - solver implementation;
  - full g-grid DAE algorithm;
  - Plan A validation as central proof;
  - EMG practical initialization as main model;
  - Ch6 deconstruction narrative.

- [ ] **Step 4: Save Phase 021 result.**

  Expected: source files, accepted scope, and exclusions are recorded.

## Phase 022 - Spine and Convention Rebuild

- [ ] **Step 5: Create the new TeX file with manuscript-only metadata.**

  Use a neutral title and no process labels:

  ```latex
  \title{\textbf{리튬이온전지 graphite anode ICA(\(dQ/dV\)) tail 이론}\\
  \large Chapter 1: charge conservation, effective mobility barrier, and relaxation-length spectrum}
  ```

- [ ] **Step 6: Define conventions before equations.**

  Required table:

  - `q`, `Q_ext`, `Q_cell`;
  - `V_n`, `V_{n,app}`, `V_{n,drive}`;
  - `theta_j`, `theta_eq,j`, `Theta`;
  - `r_j`;
  - `G`, `Delta G_eff`;
  - `k_j`, `k_0`;
  - `L_q`, `L_Q`, `L_phi`;
  - `A_L` or a measure notation `dM_L`.

- [ ] **Step 7: State the central thesis in one paragraph.**

  Exact content:

  ```text
  Ideal equilibrium broadening alone does not explain the low-temperature long tail.
  The tail is primarily a finite-rate relaxation effect.
  Temperature and electrode-potential assistance enter through the effective mobility barrier and therefore through the relaxation-length spectrum.
  ```

- [ ] **Step 8: Add a "what this chapter will not prove" box.**

  Include:

  - no full solver;
  - no unique inversion of `rho_G`;
  - no step-function transition;
  - no raw apparent-voltage derivative as thermodynamic entropy.

- [ ] **Step 9: Save Phase 022 result.**

  Gate: no `RB`, `Date:`, `Author`, `audit`, or `phase` text in the LaTeX body.

## Phase 023 - Mathematical Body Rewrite

- [ ] **Step 10: Rewrite charge conservation.**

  Use:

  ```latex
  Q_{\cell}q = Q_{\bg}(V_n,T)+Q_p\Theta(q,V_n,T)
  ```

  Then define:

  ```latex
  \Theta=\sum_j \alpha_j\theta_j,\qquad \sum_j\alpha_j=1
  ```

  Explain `Q_p alpha_j` as transition capacity contribution.

- [ ] **Step 11: Derive internal potential sensitivity.**

  At fixed `q`:

  ```latex
  \left(\frac{\partial V_n}{\partial \Theta}\right)_{q,T}
  =
  -\frac{Q_p}{C_{\bg}(V_n,T)}
  ```

  State this is the source of self-consistency, but not yet a solver.

- [ ] **Step 12: Rewrite equilibrium target.**

  Use general `theta_eq,j(V_n,T)` first. Then show logistic as a grounded special case.

  Avoid:

  ```text
  equilibrium theory always predicts the opposite
  ```

  Use:

  ```text
  ideal logistic broadening alone predicts the wrong temperature trend.
  ```

- [ ] **Step 13: Rewrite the effective barrier section.**

  Rename the core quantity:

  ```latex
  \Delta G_{\mathrm{mob},j}^{\eff}
  =
  G_j-\chi_j\mathcal A_j
  ```

  Text:

  ```text
  This is a reduced mobility barrier for the relaxation timescale. It does not change theta_eq in Chapter 1.
  Forward/backward directional barrier splitting is Chapter 3.
  ```

- [ ] **Step 14: Derive rate constant and relaxation length.**

  Use normalized length:

  ```latex
  L_{q,j}
  =
  \frac{|I|}{Q_{\cell}k_j}
  =
  \frac{|I|}{Q_{\cell}k_{0,j}(T)}
  \exp\left[\frac{G_j-\chi_j\mathcal A_j}{RT}\right]
  ```

  State units explicitly.

- [ ] **Step 15: Derive single-mode post-peak tail.**

  Starting from:

  ```latex
  r_j=\theta_{\eq,j}-\theta_j
  ```

  Show:

  ```latex
  \frac{\dd r_j}{\dd q}\simeq-\frac{r_j}{L_{q,j}},
  \qquad
  \frac{\dd\theta_j}{\dd q}\simeq
  \frac{r_j(q_a)}{L_{q,j}}\exp[-(q-q_a)/L_{q,j}]
  ```

  Add a small box:

  ```text
  This is one local mode, not the observed whole peak.
  ```

- [ ] **Step 16: Replace overloaded `A_L` with a measure-first spectrum.**

  Define:

  ```latex
  \dd M_j(\lambda;T,\psi)
  =
  a_j(G,T,\psi)\rho_{G,j}(G;T)
  \left|\frac{\dd G}{\dd\lambda}\right|\dd\lambda
  ```

  Then:

  ```latex
  A_{L,j}(\lambda;T,\psi)
  =
  a_j(G(\lambda),T,\psi)\rho_{G,j}(G(\lambda);T)
  \frac{RT}{\lambda}
  ```

  Explain that `a_j` carries capacity/site/amplitude weighting, while `rho_G` is the barrier distribution.

- [ ] **Step 17: Derive the kernel integral from single-mode summation.**

  Use:

  ```latex
  \frac{\dd\Theta_{\tail}}{\dd q}
  \simeq
  \sum_j \int_0^\infty
  A_{L,j}(\lambda;T,\psi)
  \lambda^{-1}
  e^{-(q-q_{a,j})/\lambda}\,\dd\lambda
  ```

  Every term must have a one-sentence physical meaning.

- [ ] **Step 18: Put self-consistency after the kernel, as a boundary.**

  Text:

  ```text
  The kernel proof above is the weak-feedback/frozen-local-potential form. If \(V_n\) strongly changes the target during the tail, the exact object becomes an implicit causal integral equation. This is a validity boundary, not the main proof.
  ```

  Optional appendix equation:

  ```latex
  \Theta(q)=\Theta_{\init}(q)+\int_0^q K(q,q')\Theta_{\eq}(V_n(q',\Theta(q')),T)\,\dd q'
  ```

  Do not put Plan A ratio-substitution in main text.

- [ ] **Step 19: Save Phase 023 result.**

  Gate:

  - all new equations trace to a preceding sentence;
  - every integral states what is being integrated over and why;
  - no plain `L` as core coordinate length.

## Phase 024 - Simplefit and Falsification Layer

- [ ] **Step 20: Derive ICA expression.**

  Use:

  ```latex
  \frac{\dd Q_{\ext}}{\dd V_n}
  =
  \frac{C_{\bg}(V_n,T)}
  {1-\dfrac{Q_p}{Q_{\cell}}\dfrac{\dd\Theta}{\dd q}}
  ```

  This keeps the `q` coordinate visible and avoids switching silently to `Q`.

- [ ] **Step 21: Add small-tail linearized residual form.**

  Define a residual after background/equilibrium subtraction:

  ```latex
  Y_{\tail}(q)
  \equiv
  \left(\frac{\dd Q}{\dd V_n}\right)_{\mathrm{meas}}
  -
  \left(\frac{\dd Q}{\dd V_n}\right)_{\mathrm{bg+eq}}
  ```

  In the one-mode/small-tail limit:

  ```latex
  Y_{\tail}(q)
  \approx
  B_j\exp[-(q-q_{a,j})/L_{q,j}]
  ```

  Then define:

  ```latex
  L_{q,j}(T,\psi)
  =
  \frac{|I|}{Q_{\cell}k_{0,j}(T)}
  \exp\left[\frac{G_j-\chi_j\mathcal A_j}{RT}\right]
  ```

- [ ] **Step 22: Add a one-page practical simplefit recipe.**

  Required substeps:

  1. Estimate and subtract background/equilibrium peak shoulder.
  2. Fix \(q_a\) from a stated rule before fitting \(L_q\).
  3. Fit \(\log Y_{\tail}\) versus \(q-q_a\) only in a stated post-peak window.
  4. Extract \(L_q=-1/\text{slope}\).
  5. Compare \(L_q(T)\) and \(L_q(\psi)\) to the barrier expression.
  6. Stop if the semi-log tail is curved; that is evidence for a spectrum, not a failure to be hidden.

- [ ] **Step 23: Add identifiability boundaries.**

  Must state:

  - \(R_n\), \(q_a\), \(B_j\), and \(L_q\) are confounded if all are free.
  - \(R_n\) requires independent pulse/relaxation/impedance constraint.
  - \(\rho_G\) is forward-predicted, not uniquely inverted from a single tail.

- [ ] **Step 24: Add falsification checks.**

  Checks:

  - ideal equilibrium peak width trend alone fails to explain low-temperature long tail;
  - \(L_q\) should increase at lower temperature under activation control;
  - potential assistance should shift weight toward shorter \(L_q\);
  - if calorimetry or rate-dependence contradicts the same \(L_q\) trend, kinetic-spectrum attribution must be revisited.

- [ ] **Step 25: Save Phase 024 result.**

  Gate: the chapter must now give a reader a usable simplefit formula without requiring Plan A/B solver machinery.

## Phase 025 - 10-Pass Review and Repair

- [ ] **Step 26: Run 10 chunked read passes with different chunk sizes.**

  Required chunk sizes:

  ```text
  37, 49, 61, 73, 89, 109, 131, 157, 191, 233 lines
  ```

- [ ] **Step 27: Pass 1 - user-critique replay.**

  Verify section 7+ no longer feels abrupt.

- [ ] **Step 28: Pass 2 - convention audit.**

  Verify `theta`, `Theta`, `L_q`, no unplanned `xi`.

- [ ] **Step 29: Pass 3 - equation provenance audit.**

  Each equation must have a preceding physical sentence and following interpretation.

- [ ] **Step 30: Pass 4 - units audit.**

  Check \(G\), \(RT\), \(A_L\), \(L_q\), \(dQ/dV\), and \(B_j\).

- [ ] **Step 31: Pass 5 - equilibrium/dynamic separation audit.**

  Check ideal equilibrium argument is not overclaimed.

- [ ] **Step 32: Pass 6 - barrier/potential audit.**

  Check mobility barrier vs directional reaction barrier is not confused.

- [ ] **Step 33: Pass 7 - spectrum/kernel audit.**

  Check \(A_L\) or \(\dd M_L\) is not overloaded.

- [ ] **Step 34: Pass 8 - simplefit usability audit.**

  Verify a reader can extract \(L_q\) from a real tail in a defined window.

- [ ] **Step 35: Pass 9 - scope audit.**

  Check solver/DAE/Plan A/B is appendix-gated or removed from main proof.

- [ ] **Step 36: Pass 10 - manuscript hygiene audit.**

  Check no process labels, no broken refs/cites, no work-history.

- [ ] **Step 37: Run static verification.**

  Required:

  - line count and SHA256;
  - begin/end count;
  - brace count;
  - missing refs/cites;
  - search for forbidden patterns.

- [ ] **Step 38: Save Phase 025 result, ledger, and handover.**

  The handover must state:

  - current canonical Chapter 1 candidate;
  - remaining uncertainties;
  - whether Chapter 2 should be adjusted after Ch1 rewrite.

## Test Plan

Static checks:

```powershell
# refs/cites/braces/environments
# high-risk strings
# chunk scan with ten chunk sizes
```

High-risk strings:

```text
RB
Date:
Author:
audit
phase
\xi
plain " L=" for core relaxation length
solver
root-find
DAE
Plan A 단독
step-function
0 -> 1
```

Manual gates:

- Can a reader explain what each integral integrates over?
- Can a reader state the physical meaning of \(A_L\) or \(\dd M_L\)?
- Can a reader derive the one-mode tail formula from the ODE?
- Can a reader use the final simplefit recipe without opening Chapter 6?
- Are all assumptions marked as established, bounded, or flagged?

## Assumptions

- Claude reference material contains useful derivation fragments but should not be treated as canonical.
- Codex Chapter 1 should be written as a clean manuscript, not a repair log.
- The user's current priority is logical clarity and physical meaning, not solver implementation.
- Chapter 2 may need a later convention adjustment if Chapter 1 changes from Claude's `xi/L` convention to Codex's `theta/L_q` convention.

## Correction History

- 2026-06-01: Initial plan written after copying Claude rebuilt TeX reference set and performing the 10-pass chunk review of Claude Chapter 1.

