# Chapter 1 V5 Repair and Chapter 2--5 Resume Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` or equivalent phase execution discipline. Use `superpowers:verification-before-completion` before any completion/pass claim. Store plans in `D:\Projects\Project_Anode_Fit\Codex\plans` and deliverables/results in `D:\Projects\Project_Anode_Fit\Codex\results`.

**Goal:** Cancel the previous unconditional Chapter 1 V4 PASS, repair Chapter 1 into a V5 candidate using Claude's adversarial 10-pass review, then resume Chapter 2--5 sequential work from the repaired V5 convention spine.

**Architecture:** Treat `graphite_ica_ch1_codex_candidate_v4.tex` as a repair base, not as a final. Treat `D:\Projects\Project_Anode_Fit\Claude\results\RB_CODEX_V4_CH1_REVIEW_CLAUDE_10PASS.md` as an external adversarial review artifact. Do not edit Claude files. Do not continue Chapter 2--5 until Chapter 1 V5 has fixed or explicitly bounded every Critical/High item that affects downstream notation, fitting logic, or thermodynamic/kinetic separation.

**Tech Stack:** LaTeX manuscript source, chunked full-document review, static label/ref/cite/risk scans, XeLaTeX build when available, phase result and ledger recovery records.

---

## Summary

The user pointed out that the previous long-running instruction was not merely "review Claude final"; it required whole-chapter continuation. Codex did produce a Claude-final full-set review, but did not continue the actual Codex Chapter 2--5 writing sequence after Chapter 1 V4. This plan corrects that execution drift.

The immediate blocker is that Claude's independent adversarial review of Codex Chapter 1 V4 found real unresolved defects. Therefore Chapter 1 V4 is no longer treated as final. The next canonical target is Chapter 1 V5.

The physical target remains the user's original system:

- graphite anode ICA, especially phase-transition peak tail behavior;
- low temperature gives a long tail, high temperature gives a shorter tail;
- temperature-controlled activation barrier alone is insufficient;
- electrode-potential-assisted effective barrier modifies the relaxation length and tail;
- no step-function-like jump or artificial clipping is allowed;
- Korean prose with English scientific terms is preferred;
- undergraduate-level derivation with no hidden algebra, no unexplained variables, and no unsupported assumptions;
- final Chapter 1 must provide a self-contained first-pass fitting approximation, while distinguishing narrow single-mode tails from stretched/spectrum tails.

## Current Ground Truth

### Confirmed Inputs

- Codex Chapter 1 V4:
  `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v4.tex`
  - lines: 945
  - previous SHA256: `C1607A7E101B1D3BA4BD4CDF9D88D0C8AEDAFADCEA6BBFF1E525EC540C876517`
  - previous result incorrectly reported residual critical 0.

- Claude adversarial review:
  `D:\Projects\Project_Anode_Fit\Claude\results\RB_CODEX_V4_CH1_REVIEW_CLAUDE_10PASS.md`
  - lines: 132
  - SHA256: `B3A1BDC758E853FAD6188C8C0C8E7658ED180F873834DFAC20F8B57B9F8B31AD`
  - read in full during plan setup.

- Existing Codex roadmaps and ledgers:
  - `D:\Projects\Project_Anode_Fit\Codex\plans\2026-06-01-claude-rebuilt-base-codex-completion-roadmap.md`
  - `D:\Projects\Project_Anode_Fit\Codex\plans\2026-06-02-chapter1-v4-full-rebuild-10pass-plan.md`
  - `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_021_031_CLAUDE_BASE_COMPLETION_LEDGER.md`
  - `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_030_CH1_V4_CHANGE_HISTORY_AND_HANDOVER.md`

### Defect Categories To Repair

Critical:

1. AL ledger discontinuity: AL-8 and AL-9 absent while GS-3 claims closed assumption ledger.
2. Basic constants missing from notation: R, F, T, k_B, h, plus practical symbols such as q_a and kappa.
3. Stretched-tail spectrum conflicts with single-L Eyring/N2 falsification if the single-mode extraction is applied outside narrow-spectrum conditions.

High:

1. chi_j extraction is confounded with current prefactor unless `ln L - ln |I|` or fixed-current potential sweep is used.
2. Marcus symmetric derivation gives chi_j = 1/2 only; general chi_j in [0,1] must be empirical BEP/BV analogy or moved to Ch3.
3. Several algebraic steps are compressed: homogeneous term spectrum, Taylor intercept a(q'), and closed denominator derivation.
4. Plan B is declared primary, but practical fitting output relies on Plan A; low-temperature stretched cases need explicit Plan B handoff.
5. Eyring slope still contains ln kappa(T) unless kappa is flat or independently corrected.
6. Q_bg mixes equilibrium chemical capacitance and lag absorber roles; split into Q_bg^eq and Q_bg^lag or remove the lag role from Ch1 fitting denominator.
7. Kernel residue visualization and target Volterra kernel must not be conflated.

## Phase Range

| Phase | Name | Step Range | Purpose |
|---|---|---:|---|
| 035 | Review intake and V4 PASS cancellation | 391-410 | Ingest Claude review, record execution drift, define V5 repair gates. |
| 036 | Chapter 1 V5 repair drafting | 411-470 | Create V5 TeX candidate and repair every Critical/High item affecting Ch1 logic. |
| 037 | Chapter 1 V5 10-pass re-review | 471-520 | Re-run varied-chunk full review against V5, including adversarial checks from Claude. |
| 038 | Chapter 1 V5 verification and handover | 521-550 | Static checks, XeLaTeX build, result, ledger, handover. |
| 039 | Chapter 2 repair/write plan from V5 spine | 551-585 | Start Ch2 only after V5 gate; align reversible heat/dVdT with repaired Ch1. |
| 040 | Chapter 2 execution and 10-pass review | 586-650 | Produce Ch2 Codex candidate and verify. |
| 041 | Chapter 3 execution and 10-pass review | 651-720 | Produce Ch3 candidate with Level-A/Level-B boundary fixed. |
| 042 | Chapter 4 execution and 10-pass review | 721-790 | Produce Ch4 heat-generation candidate without double counting. |
| 043 | Chapter 5 execution and 10-pass review | 791-860 | Produce Ch5 hysteresis candidate with branch signs and Ch1/Ch3 conventions aligned. |
| 044 | Integrated refs/full manuscript | 861-920 | Rebuild integrated manuscript, refs, cross-refs, and final ledger. |

## Non-goals

- Do not edit Claude directory files.
- Do not treat Claude's review as automatically correct; verify each finding against V4 before repairing.
- Do not rewrite Ch2--5 against V4 after V5 repairs change conventions.
- Do not implement a numerical solver or fitting code; only provide theory, formulas, validity gates, and first-pass fitting expressions.
- Do not hide phase/change history in TeX body.
- Do not claim completion of any chapter without static checks, build attempt if possible, and 10-pass review.

## Implementation Changes

Create:

- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_035_CLAUDE_CH1_REVIEW_INTAKE_AND_V5_GATE.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v5.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_036_CH1_V5_REPAIR_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_037_CH1_V5_10PASS_REVIEW.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_038_CH1_V5_VERIFICATION_AND_HANDOVER.md`

Update by addendum only:

- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_021_031_CLAUDE_BASE_COMPLETION_LEDGER.md`

Future chapter candidates:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch2_codex_candidate_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch3_codex_candidate_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch4_codex_candidate_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch5_codex_candidate_v1.tex`

## Phase 035 — Review Intake and V4 PASS Cancellation

- [ ] Step 391: Record Claude review path, line count, SHA256, and full-read status.
- [ ] Step 392: Record execution drift: previous work produced full Claude review but did not continue all chapter writing.
- [ ] Step 393: Reclassify Chapter 1 V4 as superseded, not final.
- [ ] Step 394: Map every Claude Critical/High finding to V4 line ranges.
- [ ] Step 395: Save intake/result document.

Gate: V5 repair cannot start until every Critical/High finding has an action: repair, reject with evidence, or bound with explicit validity condition.

## Phase 036 — Chapter 1 V5 Repair Drafting

- [ ] Step 411: Copy V4 to V5 working candidate without modifying V4.
- [ ] Step 412: Add constants and practical symbols to notation table.
- [ ] Step 413: Repair AL ledger continuity and split mixed AL entries where needed.
- [ ] Step 414: Rewrite chi_j derivation so symmetric Marcus only supports chi_j=1/2; general chi_j is empirical scalar mobility sensitivity, not Level-B transfer coefficient.
- [ ] Step 415: Add explicit small-drive and non-negative effective-barrier validity statement without clipping.
- [ ] Step 416: Repair spectrum vs single-mode boundary: single-L Eyring extraction is narrow-spectrum only; stretched spectrum uses forward-prediction curvature and mode-averaged barrier descriptors.
- [ ] Step 417: Repair chi_j extraction: remove current-prefactor confounding by fitting `ln L - ln |I|` or using fixed-current potential sweeps.
- [ ] Step 418: Add ln kappa(T) term and a bounded condition for ignoring it.
- [ ] Step 419: Split Q_bg roles so C_bg uses only equilibrium background capacitance.
- [ ] Step 420: Expand missing algebraic steps in Volterra/Plan A closure.
- [ ] Step 421: Clarify Plan B vs Plan A handoff: low-temperature stretched cases require Plan B/spectrum forward prediction; Plan A is narrow/validated approximation.
- [ ] Step 422: Repair falsification rules N2/N3/N5 using the new narrow-spectrum vs stretched-spectrum distinction.

Gate: V5 must preserve the user's core story while removing the self-contradiction between stretched tails and single-L Arrhenius extraction.

## Phase 037 — Chapter 1 V5 10-Pass Re-Review

Each pass must cover the entire V5 file with a different chunking logic.

- [ ] Step 471: P1 section-level structure/convention/metadata.
- [ ] Step 472: P2 70-line variables and definitions.
- [ ] Step 473: P3 90-line equation continuity.
- [ ] Step 474: P4 120-line assumptions and grounding.
- [ ] Step 475: P5 55-line units, signs, and dimensions.
- [ ] Step 476: P6 dependency chain from observation to fitting formula.
- [ ] Step 477: P7 reverse-order forward-reference pass.
- [ ] Step 478: P8 fitting usability and non-circularity.
- [ ] Step 479: P9 adversarial physics: stretched/single-L, transport degeneracy, Q_bg roles.
- [ ] Step 480: P10 final full sweep against user criteria.

Gate: No unresolved Critical/High. Medium items must be either fixed or explicitly bounded.

## Phase 038 — Chapter 1 V5 Verification and Handover

- [ ] Step 521: Run static scans: labels, refs, cites, duplicate labels, missing refs/cites, unused bibs.
- [ ] Step 522: Run risk scans: AL gaps, undefined constants, chi_j=beta_j, Heaviside support, amplitude-less delta, plus-sign Eyring double-counting, placeholder references, process metadata.
- [ ] Step 523: Run XeLaTeX build if the engine is available.
- [ ] Step 524: Save verification result and handover.
- [ ] Step 525: Update ledger by addendum.

Gate: Chapter 2 work may start only after V5 has a clean handover listing the exact formulas and conventions passed downstream.

## Chapter 2--5 Resume Rule

Chapter 2--5 must not inherit stale V4 assumptions. Their plans must explicitly quote the V5 downstream interface:

- state variables: `V_n`, `V_{n,app}`, `V_{n,drive}`, `xi_j`, `xi_eq,j`;
- kinetic object: Level-A scalar mobility `k_j` and `chi_j`;
- Ch3 boundary: directional forward/backward splitting and transfer coefficient `beta_j` are introduced only in Ch3;
- fitting boundary: single-mode formulas apply only under narrow-spectrum gate; stretched tails require spectrum/Plan B forward prediction;
- thermal boundary: Ch2 uses equilibrium entropy coefficient and does not reinterpret kinetic tails as reversible heat.

## Test Plan

- Full-read coverage for all review artifacts used in this phase.
- Static label/ref/cite parse after TeX edits.
- Risk-pattern scan for known failure modes.
- Algebra spot-checks for Eyring sign, current-prefactor subtraction, and single-mode vs spectrum boundary.
- XeLaTeX build if available.
- Result and ledger readback before reporting.

## Assumptions

- The Claude review file is read-only evidence, not an editable target.
- V4 remains preserved as a superseded artifact.
- Chapter 1 V5 may be longer than V4 if needed to remove logical gaps.
- PDF creation is verification-only; final user-facing artifact can be TeX.

## Correction History

- This plan supersedes the previous Chapter 1 V4 PASS result for downstream purposes.
- This plan corrects the execution drift where Codex reviewed Claude's final full set but did not continue the whole Chapter 2--5 writing sequence.
