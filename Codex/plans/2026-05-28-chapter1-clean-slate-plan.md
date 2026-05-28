# Chapter 1 Clean-Slate Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Do not restore archived equations. Do not use previous Codex or ChatGPT drafts as formula authority. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild Chapter 1 from zero as a paper-grade theoretical background for graphite negative-electrode ICA peak-tail behavior in lithium-ion batteries.

**Architecture:** Previous outputs have been moved to `Codex\old`. The new chain begins from the user's physical observation and from defensible theory only: conservation/calculus, thermodynamics, transition-state or activated-rate reasoning, and explicitly labeled reduced assumptions. Every assumption must have evidence status; every equation must have origin, domain, and failure mode.

**Tech Stack:** LaTeX, Markdown phase reports, equation-origin ledger, assumption-evidence ledger, source/literature read coverage, static TeX checks.

---

## Summary

This plan restarts Chapter 1 from scratch.

The core physical problem is:

- In LIB graphite negative-electrode ICA, a phase-transition-related peak shows a post-peak tail.
- The tail is longer at low temperature and shorter at higher temperature.
- A purely equilibrium peak shape is not enough for the target explanation.
- The intended theory is that finite phase-transition relaxation produces a residual tail.
- Temperature affects the relaxation rate through an activation free-energy barrier.
- The present electrode-potential state may assist the transition by lowering an effective activation barrier.
- The work must avoid fitting convenience, arbitrary caps, hidden step functions, and unsupported assumptions.
- The final Chapter 1 must be readable at undergraduate level while being rigorous enough for paper/patent development.

## Current Ground Truth

| Item | State |
|---|---|
| Active project | `D:\Projects\Project_Anode_Fit` |
| Active Codex workspace | `D:\Projects\Project_Anode_Fit\Codex` |
| New plan path | `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-chapter1-clean-slate-plan.md` |
| Previous outputs archive | `D:\Projects\Project_Anode_Fit\Codex\old\2026-05-28-reset-before-chapter1-clean-restart` |
| Current `results` status | Clean slate after archive |
| Current `plans` status | Only operations guide plus this new plan |
| Canonical Chapter 1 | Not yet created |
| User core requirement | Paper-grade physical logic; no unsupported assumptions; no logical leaps |

## Phase Range

| Phase | Name | Step Range | Primary Output | Gate |
|---|---|---:|---|---|
| Phase 001 | Clean-Slate Baseline | 1-18 | `PHASE_001_CLEAN_SLATE_BASELINE_RESULT.md` | `PASS_CLEAN_SLATE_BASELINE` |
| Phase 002 | Evidence And Source Inventory | 19-55 | `PHASE_002_EVIDENCE_SOURCE_INVENTORY_RESULT.md` | `PASS_EVIDENCE_SCOPE` |
| Phase 003 | Assumption Contract | 56-85 | `PHASE_003_ASSUMPTION_CONTRACT_RESULT.md` | `PASS_ASSUMPTION_CONTRACT` |
| Phase 004 | Derivation Ledger | 86-135 | `PHASE_004_CH1_DERIVATION_LEDGER.md` | `PASS_NO_LEAP_DERIVATION` |
| Phase 005 | Double-Counting And Regime Audit | 136-175 | `PHASE_005_DOUBLE_COUNTING_REGIME_AUDIT.md` | `PASS_REGIME_AUDIT` |
| Phase 006 | Chapter 1 Manuscript v1 | 176-225 | `graphite_ica_chapter1_clean_slate_v1.tex` | `PASS_MANUSCRIPT_DRAFT` |
| Phase 007 | Ralph-Wiggum Logic Loop | 226-285 | `PHASE_007_RALPH_WIGGUM_LOGIC_LOOP_RESULT.md` | `PASS_NO_CRITICAL_GAP` |
| Phase 008 | Final Verification And Handover | 286-320 | `PHASE_008_CH1_CLEAN_SLATE_HANDOVER.md` | `PASS_CLEAN_SLATE_HANDOVER` |

Phase counts are minimum criteria. Add subphases when evidence, derivation, or logic audit fails.

## Non-Goals

- Do not revive any archived manuscript as the working base.
- Do not copy equations from archived Codex or ChatGPT outputs.
- Do not use `max`, `min`, clipping, softplus, hard cap, bounded transform, or step-function-like barrier treatment as Chapter 1 physics.
- Do not build fitting code or a solver.
- Do not make peak area the central argument.
- Do not write Chapter 2 heat, Chapter 3 electrochemical kinetics, Chapter 4 heat generation, or Chapter 5 hysteresis except as one-sentence roadmap.
- Do not modify `D:\Projects\Project_Anode_Fit\Claude`.
- Do not modify original download/source files.

## Implementation Changes

### Create

| Path | Purpose |
|---|---|
| `Codex\results\PHASE_001_008_CHAPTER1_CLEAN_SLATE_LEDGER.md` | New execution ledger |
| `Codex\results\PHASE_001_CLEAN_SLATE_BASELINE_RESULT.md` | Archive confirmation and restart baseline |
| `Codex\results\PHASE_002_EVIDENCE_SOURCE_INVENTORY_RESULT.md` | Source/literature evidence map |
| `Codex\results\PHASE_003_ASSUMPTION_CONTRACT_RESULT.md` | Allowed assumptions and wording |
| `Codex\results\PHASE_004_CH1_DERIVATION_LEDGER.md` | Equation-by-equation derivation |
| `Codex\results\PHASE_005_DOUBLE_COUNTING_REGIME_AUDIT.md` | Equilibrium/mobility, barrier regime, sign audit |
| `Codex\results\graphite_ica_chapter1_clean_slate_v1.tex` | New Chapter 1 manuscript |
| `Codex\results\PHASE_007_RALPH_WIGGUM_LOGIC_LOOP_RESULT.md` | Reader/reviewer logic attack |
| `Codex\results\PHASE_008_CH1_CLEAN_SLATE_HANDOVER.md` | Final handover |

### Preserve

| Path | Rule |
|---|---|
| `Codex\old\2026-05-28-reset-before-chapter1-clean-restart` | Archive only; not working base |
| `Codex\plans\phase_planning_operations_guide.md` | Keep in active plans folder |
| `Codex\AGENTS.md` | Keep active |

## Equation Origin Classes

| Class | Meaning | Requirement |
|---|---|---|
| `DEF` | Definition | Symbol, unit, sign convention |
| `CALC` | Calculus/algebra consequence | Must show dependency |
| `CONS` | Conservation/balance | Must identify conserved quantity |
| `THERMO` | Thermodynamic identity | Must state constraints |
| `KIN-TST` | Transition-state/activated-rate theory | Must cite or state theory basis |
| `KIN-RED` | Reduced kinetic model | Must state why reduced and when it fails |
| `LOCAL` | Local approximation | Must state expansion/validity range |
| `LIMIT` | Limiting regime | Must state what ceases to be rate-limiting |
| `ROADMAP` | Later chapter note | Cannot support Chapter 1 proof |

Forbidden origin:

- `FITTING_CONVENIENCE`
- `NUMERICAL_STABILIZER`
- `COPIED_ARCHIVE`
- `UNSUPPORTED_INTUITION`

## Phase 001 — Clean-Slate Baseline

**Steps:**

- [ ] Step 1: Confirm previous plans/results were moved to `Codex\old`.
- [ ] Step 2: Confirm active `results` contains only new clean-slate outputs.
- [ ] Step 3: Confirm active `plans` retains operations guide and this plan.
- [ ] Step 4: Record that archived drafts are non-canonical.
- [ ] Step 5: Record that archived equations are not allowed as equation authority.
- [ ] Step 6: Record user physical target in exact working form.
- [ ] Step 7: Record banned shortcuts: `max`, clipping, softplus, cap, step-function barrier.
- [ ] Step 8: Record barrier-exhausted handling: not clipped; active-barrier regime ends.
- [ ] Step 9: Record chapter scope and non-goals.
- [ ] Step 10: Create new execution ledger.
- [ ] Step 11: Create `PHASE_001_CLEAN_SLATE_BASELINE_RESULT.md`.
- [ ] Step 12: Update ledger row for Phase 001.
- [ ] Step 13: Gate check: archive path exists.
- [ ] Step 14: Gate check: previous working files are not in active `results`.
- [ ] Step 15: Gate check: no previous TeX is marked canonical.
- [ ] Step 16: Gate check: banned shortcuts are explicit.
- [ ] Step 17: Gate check: user physical target is present.
- [ ] Step 18: Proceed to Phase 002 only after pass.

**Gate:** `PASS_CLEAN_SLATE_BASELINE`

## Phase 002 — Evidence And Source Inventory

**Steps:**

- [ ] Step 19: List local source files relevant to Chapter 1.
- [ ] Step 20: Identify which files require full read and which are structure-only.
- [ ] Step 21: Identify source categories: user observation, prior drafts as hazards, theory/literature, original paper/PDF if needed.
- [ ] Step 22: Record source metadata: path, size, line/page count.
- [ ] Step 23: Decide whether ChatGPT final TeX is needed only as hazard checklist.
- [ ] Step 24: Decide whether old Codex files are needed only as hazard checklist.
- [ ] Step 25: Identify literature needed for activated-rate theory.
- [ ] Step 26: Identify literature/theory needed for electrochemical potential work and barrier lowering.
- [ ] Step 27: Identify literature/theory needed for graphite staging/phase transition language.
- [ ] Step 28: Identify whether ICA/DVA mapping can be derived purely from calculus and storage balance.
- [ ] Step 29: Search or inspect sources only where required.
- [ ] Step 30: Record read coverage for every inspected source.
- [ ] Step 31: For each planned assumption, assign support status: `TEXTBOOK`, `LITERATURE_CONFIRMED`, `DERIVED`, `REDUCED_MODEL`, `UNSUPPORTED_REMOVE`, or `DEFER`.
- [ ] Step 32: Do not cite or rely on unread literature.
- [ ] Step 33: If ref. 6/7 methods are relevant only to numerical integral solutions, defer to later chapter.
- [ ] Step 34: Create source/evidence table.
- [ ] Step 35: Create missing-evidence table.
- [ ] Step 36: Create `PHASE_002_EVIDENCE_SOURCE_INVENTORY_RESULT.md`.
- [ ] Step 37: Update ledger.
- [ ] Step 38: Gate check: every assumption has evidence status.
- [ ] Step 39: Gate check: unsupported claims are removed or deferred.
- [ ] Step 40: Gate check: read coverage is recorded.
- [ ] Step 41: Gate check: no unread source is cited as support.
- [ ] Step 42: Gate check: old drafts are not equation authority.
- [ ] Step 43: If essential evidence is missing, pause or search before Phase 003.
- [ ] Step 44: If a claim cannot be supported, weaken or remove it.
- [ ] Step 45: Record compaction recovery notes.
- [ ] Step 46: Record decision queue if user choice is required.
- [ ] Step 47: Proceed only if no essential assumption is unsupported.
- [ ] Step 48: Keep raw source files unmodified.
- [ ] Step 49: Keep Claude folder unmodified.
- [ ] Step 50: Verify result file has no fake PASS.
- [ ] Step 51: Verify phase output path.
- [ ] Step 52: Verify ledger row path.
- [ ] Step 53: Mark Phase 002 complete only after gate.
- [ ] Step 54: If not complete, record blocker.
- [ ] Step 55: Proceed to Phase 003.

**Gate:** `PASS_EVIDENCE_SCOPE`

## Phase 003 — Assumption Contract

**Steps:**

- [ ] Step 56: Define all Chapter 1 variables and units before equations.
- [ ] Step 57: Define branch direction and tail direction.
- [ ] Step 58: Define what is meant by equilibrium target.
- [ ] Step 59: Define what is meant by actual transformed fraction.
- [ ] Step 60: Define residual lag and sign.
- [ ] Step 61: Define first-order relaxation as reduced local assumption.
- [ ] Step 62: Define active-barrier regime.
- [ ] Step 63: Define present-potential assisting coordinate.
- [ ] Step 64: Define physical meaning of barrier lowering.
- [ ] Step 65: Define what happens when active barrier is exhausted.
- [ ] Step 66: Define ICA/DVA mapping assumptions.
- [ ] Step 67: Define voltage-axis versus capacity-axis tail.
- [ ] Step 68: Define equilibrium heterogeneity as possible non-kinetic contribution.
- [ ] Step 69: Define what Chapter 1 will not prove.
- [ ] Step 70: For each assumption, add allowed wording and forbidden wording.
- [ ] Step 71: For each assumption, add evidence status from Phase 002.
- [ ] Step 72: Remove assumptions without evidence or reduced-model label.
- [ ] Step 73: Create `PHASE_003_ASSUMPTION_CONTRACT_RESULT.md`.
- [ ] Step 74: Update ledger.
- [ ] Step 75: Gate check: no assumption appears after it is used.
- [ ] Step 76: Gate check: no unsupported assumption remains.
- [ ] Step 77: Gate check: barrier handling is not a cap.
- [ ] Step 78: Gate check: double-counting risk is flagged for audit.
- [ ] Step 79: Gate check: undergraduate-reader constraints are explicit.
- [ ] Step 80: Gate check: manuscript scope is Chapter 1 only.
- [ ] Step 81: If any assumption is undecidable, add decision queue.
- [ ] Step 82: If user decision is required, pause.
- [ ] Step 83: If not, proceed.
- [ ] Step 84: Record compaction recovery.
- [ ] Step 85: Proceed to Phase 004.

**Gate:** `PASS_ASSUMPTION_CONTRACT`

## Phase 004 — Derivation Ledger

**Steps:**

- [ ] Step 86: Derive ICA/DVA definitions from calculus.
- [ ] Step 87: Define equilibrium fraction `theta_e(varphi,T)`.
- [ ] Step 88: Define actual fraction `theta(Q)`.
- [ ] Step 89: Define residual `r=theta_e-theta`.
- [ ] Step 90: Apply first-order relaxation `dtheta/dt=k r`.
- [ ] Step 91: Convert with `v_Q=dQ/dt`.
- [ ] Step 92: Derive forced residual ODE.
- [ ] Step 93: Derive variable-rate residual integral solution.
- [ ] Step 94: Derive local constant-rate tail length `L_Q=v_Q/k`.
- [ ] Step 95: State that `L_Q` is capacity-axis length.
- [ ] Step 96: Define intrinsic activation free energy with temperature-window limits.
- [ ] Step 97: Define present-potential assisting work with units.
- [ ] Step 98: Define active-barrier expression without cap.
- [ ] Step 99: Derive activated rate in active-barrier regime.
- [ ] Step 100: Derive `L_Q(T,psi)` in active-barrier regime.
- [ ] Step 101: Derive potential derivative of log tail length.
- [ ] Step 102: Derive temperature derivative condition.
- [ ] Step 103: Define barrier-exhausted limit as regime transition.
- [ ] Step 104: Define possible physical bottlenecks only as later work or limit discussion.
- [ ] Step 105: Derive storage balance with background capacity and phase charge scale.
- [ ] Step 106: Derive DVA expression.
- [ ] Step 107: Derive ICA expression.
- [ ] Step 108: Derive local voltage-axis tail mapping.
- [ ] Step 109: Add denominator/singularity condition.
- [ ] Step 110: Add equilibrium heterogeneity caveat.
- [ ] Step 111: Build equation dependency graph.
- [ ] Step 112: Assign origin class to every equation.
- [ ] Step 113: Assign validity domain to every equation.
- [ ] Step 114: Assign failure mode to every equation.
- [ ] Step 115: Unit-check every equation.
- [ ] Step 116: Sign-check every equation.
- [ ] Step 117: Create `PHASE_004_CH1_DERIVATION_LEDGER.md`.
- [ ] Step 118: Update ledger.
- [ ] Step 119: Gate check: no equation has unsupported origin.
- [ ] Step 120: Gate check: no cap/step barrier equation appears.
- [ ] Step 121: Gate check: residual-to-tail derivation is complete.
- [ ] Step 122: Gate check: voltage-axis mapping is present.
- [ ] Step 123: Gate check: trend claims are conditional.
- [ ] Step 124: Gate check: no fitting code or solver appears.
- [ ] Step 125: Repair if any gate fails.
- [ ] Step 126: Re-run unit/sign checks after repair.
- [ ] Step 127: Record open issues.
- [ ] Step 128: Record compaction recovery.
- [ ] Step 129: Proceed to Phase 005.
- [ ] Step 130: Do not write final manuscript before gate.
- [ ] Step 131: Do not claim finality.
- [ ] Step 132: Keep old archive closed unless needed for hazard lookup.
- [ ] Step 133: If archive is consulted, record exact reason and read range.
- [ ] Step 134: Verify no copied archived equation.
- [ ] Step 135: Mark phase complete only after gate.

**Gate:** `PASS_NO_LEAP_DERIVATION`

## Phase 005 — Double-Counting And Regime Audit

**Steps:**

- [ ] Step 136: Attack whether `theta_e(varphi,T)` and `k(T,psi)` double count potential.
- [ ] Step 137: Require an explicit answer: equilibrium target vs mobility.
- [ ] Step 138: If needed, add forward/backward consistency condition.
- [ ] Step 139: Attack active-barrier expression validity.
- [ ] Step 140: Attack barrier-exhausted limit.
- [ ] Step 141: Attack temperature derivative claim.
- [ ] Step 142: Attack present-potential derivative claim.
- [ ] Step 143: Attack capacity-axis to voltage-axis mapping.
- [ ] Step 144: Attack branch sign convention.
- [ ] Step 145: Attack ICA denominator condition.
- [ ] Step 146: Attack equilibrium heterogeneity caveat.
- [ ] Step 147: Attack whether first-order relaxation is overclaimed.
- [ ] Step 148: Attack whether transition-state theory is overclaimed.
- [ ] Step 149: Attack whether graphite staging specificity is overclaimed.
- [ ] Step 150: Attack all assumptions for evidence status.
- [ ] Step 151: Create reviewer-objection table.
- [ ] Step 152: Repair derivation ledger if needed.
- [ ] Step 153: Re-run unit/sign/origin checks.
- [ ] Step 154: Create `PHASE_005_DOUBLE_COUNTING_REGIME_AUDIT.md`.
- [ ] Step 155: Update ledger.
- [ ] Step 156: Gate check: no P1/P2 unresolved objection remains.
- [ ] Step 157: Gate check: double-counting objection has an answer.
- [ ] Step 158: Gate check: no clipped barrier logic remains.
- [ ] Step 159: Gate check: all trend claims are conditional.
- [ ] Step 160: Gate check: all assumptions have support or reduced-model label.
- [ ] Step 161: If fails, loop back to Phase 003 or 004.
- [ ] Step 162: If source support fails, loop back to Phase 002.
- [ ] Step 163: Record compaction recovery.
- [ ] Step 164: Proceed only after gate.
- [ ] Step 165: Mark manuscript-ready.
- [ ] Step 166: Preserve raw source files.
- [ ] Step 167: Preserve Claude folder.
- [ ] Step 168: No commit.
- [ ] Step 169: No push.
- [ ] Step 170: Record open decision queue.
- [ ] Step 171: If user decision needed, pause.
- [ ] Step 172: If no user decision needed, proceed.
- [ ] Step 173: Verify audit report path.
- [ ] Step 174: Verify ledger row.
- [ ] Step 175: Proceed to Phase 006.

**Gate:** `PASS_REGIME_AUDIT`

## Phase 006 — Chapter 1 Manuscript v1

**Steps:**

- [ ] Step 176: Create new TeX file `graphite_ica_chapter1_clean_slate_v1.tex`.
- [ ] Step 177: Write title and abstract.
- [ ] Step 178: Write convention section before derivation.
- [ ] Step 179: Write observation and target explanation.
- [ ] Step 180: Write equilibrium vs kinetic-tail distinction.
- [ ] Step 181: Write variables and assumptions before equations.
- [ ] Step 182: Write residual derivation.
- [ ] Step 183: Write local tail-length derivation.
- [ ] Step 184: Write variable-rate generalization.
- [ ] Step 185: Write active-barrier rate section.
- [ ] Step 186: Write barrier-exhausted limit section without cap.
- [ ] Step 187: Write temperature trend section.
- [ ] Step 188: Write present-potential trend section.
- [ ] Step 189: Write double-counting consistency section.
- [ ] Step 190: Write ICA/DVA mapping section.
- [ ] Step 191: Write voltage-axis mapping section.
- [ ] Step 192: Write limitations section.
- [ ] Step 193: Write Chapter 2-5 roadmap note.
- [ ] Step 194: Add references only if verified in Phase 002.
- [ ] Step 195: Ensure every equation appears in Phase 004 ledger.
- [ ] Step 196: Ensure every assumption appears in Phase 003 contract.
- [ ] Step 197: Search banned terms in final TeX.
- [ ] Step 198: Run label/ref check.
- [ ] Step 199: Run brace/environment check.
- [ ] Step 200: Record line count and hash.
- [ ] Step 201: Create manuscript result note if needed.
- [ ] Step 202: Update ledger.
- [ ] Step 203: Gate check: manuscript is new file.
- [ ] Step 204: Gate check: old drafts are not patched.
- [ ] Step 205: Gate check: no cap/step barrier treatment.
- [ ] Step 206: Gate check: every equation has ledger entry.
- [ ] Step 207: Gate check: every assumption has evidence status.
- [ ] Step 208: Gate check: Chapter 1 scope maintained.
- [ ] Step 209: If gate fails, repair before Phase 007.
- [ ] Step 210: Do not call this final yet.
- [ ] Step 211: Preserve archive.
- [ ] Step 212: Preserve source files.
- [ ] Step 213: Preserve Claude.
- [ ] Step 214: Record compaction recovery.
- [ ] Step 215: Proceed to Phase 007.
- [ ] Step 216: Verify abstract does not overclaim.
- [ ] Step 217: Verify conclusion does not overclaim.
- [ ] Step 218: Verify undergrad readability.
- [ ] Step 219: Verify no hidden literature claim.
- [ ] Step 220: Verify no fitting code.
- [ ] Step 221: Verify no solver.
- [ ] Step 222: Verify no peak-area centered argument.
- [ ] Step 223: Verify symbols introduced.
- [ ] Step 224: Verify unit table.
- [ ] Step 225: Mark phase complete.

**Gate:** `PASS_MANUSCRIPT_DRAFT`

## Phase 007 — Ralph-Wiggum Logic Loop

**Steps:**

- [ ] Step 226: Read manuscript from line 1 to end.
- [ ] Step 227: Build claim list.
- [ ] Step 228: For every claim, identify support.
- [ ] Step 229: Run undergraduate reader pass.
- [ ] Step 230: Mark skipped algebra.
- [ ] Step 231: Repair skipped algebra.
- [ ] Step 232: Run thermodynamic reviewer pass.
- [ ] Step 233: Repair equilibrium/mobility ambiguity.
- [ ] Step 234: Run kinetic reviewer pass.
- [ ] Step 235: Repair barrier regime ambiguity.
- [ ] Step 236: Run electrochemical reviewer pass.
- [ ] Step 237: Repair potential/work sign ambiguity.
- [ ] Step 238: Run ICA/DVA reviewer pass.
- [ ] Step 239: Repair voltage-axis mapping ambiguity.
- [ ] Step 240: Run skeptical modeler pass.
- [ ] Step 241: Remove disguised fitting convenience.
- [ ] Step 242: Re-run banned pattern search.
- [ ] Step 243: Re-run static TeX checks.
- [ ] Step 244: Re-run equation ledger coverage.
- [ ] Step 245: Re-run assumption contract coverage.
- [ ] Step 246: If P1/P2 issue remains, repair and repeat.
- [ ] Step 247: Create `PHASE_007_RALPH_WIGGUM_LOGIC_LOOP_RESULT.md`.
- [ ] Step 248: Update ledger.
- [ ] Step 249: Gate check: no critical logic gap.
- [ ] Step 250: Gate check: all objections answered.
- [ ] Step 251: Gate check: no unsupported claim.
- [ ] Step 252: Gate check: no barrier shortcut.
- [ ] Step 253: Gate check: reader can follow derivation.
- [ ] Step 254: If fails, loop.
- [ ] Step 255: If passes, mark final candidate.
- [ ] Step 256: Record line count and hash.
- [ ] Step 257: Record TeX engine status.
- [ ] Step 258: Record unresolved limitations.
- [ ] Step 259: Record compaction recovery.
- [ ] Step 260: Proceed to Phase 008.
- [ ] Step 261: Verify no old equation source.
- [ ] Step 262: Verify no old file reference in body.
- [ ] Step 263: Verify no phase/work-history in body.
- [ ] Step 264: Verify final scope note.
- [ ] Step 265: Verify no Chapter 2 content leaks.
- [ ] Step 266: Verify no Chapter 3 content leaks beyond roadmap.
- [ ] Step 267: Verify no heat/hysteresis proof.
- [ ] Step 268: Verify peak area deferred.
- [ ] Step 269: Verify final claim is conditional.
- [ ] Step 270: Verify source citations.
- [ ] Step 271: Verify no unread citation.
- [ ] Step 272: Verify result paths.
- [ ] Step 273: Verify ledger consistency.
- [ ] Step 274: Save final audit.
- [ ] Step 275: Continue if clean.
- [ ] Step 276: If not clean, repeat relevant pass.
- [ ] Step 277: Document every loop.
- [ ] Step 278: Keep previous loop reports.
- [ ] Step 279: Do not overwrite result reports.
- [ ] Step 280: Mark all repairs.
- [ ] Step 281: Re-read repaired sections.
- [ ] Step 282: Re-check static state.
- [ ] Step 283: Re-check final abstract.
- [ ] Step 284: Re-check final summary.
- [ ] Step 285: Mark phase complete.

**Gate:** `PASS_NO_CRITICAL_GAP`

## Phase 008 — Final Verification And Handover

**Steps:**

- [ ] Step 286: Re-run label/ref check.
- [ ] Step 287: Re-run brace/environment check.
- [ ] Step 288: Re-run banned pattern search.
- [ ] Step 289: Check TeX engine availability.
- [ ] Step 290: Compile if engine available.
- [ ] Step 291: If compile unavailable, record missing tools.
- [ ] Step 292: Record final manuscript path.
- [ ] Step 293: Record line count.
- [ ] Step 294: Record hash.
- [ ] Step 295: Record all result paths.
- [ ] Step 296: Record read coverage.
- [ ] Step 297: Record literature/source support status.
- [ ] Step 298: Record unresolved issues.
- [ ] Step 299: Record next chapter handoff.
- [ ] Step 300: Record confirmed non-changes.
- [ ] Step 301: Create `PHASE_008_CH1_CLEAN_SLATE_HANDOVER.md`.
- [ ] Step 302: Update ledger.
- [ ] Step 303: Gate check: final manuscript exists.
- [ ] Step 304: Gate check: verification evidence exists.
- [ ] Step 305: Gate check: no hidden unresolved issue.
- [ ] Step 306: Gate check: no incomplete phase reported complete.
- [ ] Step 307: Do not commit unless user asks.
- [ ] Step 308: Do not push.
- [ ] Step 309: Do not modify Claude.
- [ ] Step 310: Do not modify original sources.
- [ ] Step 311: Provide concise final report.
- [ ] Step 312: Include if PDF compile unavailable.
- [ ] Step 313: Include limitations.
- [ ] Step 314: Include next recommended action.
- [ ] Step 315: Preserve all artifacts.
- [ ] Step 316: Verify archive still exists.
- [ ] Step 317: Verify old not mixed into active results.
- [ ] Step 318: Verify current plan remains.
- [ ] Step 319: Save handover.
- [ ] Step 320: Mark final gate.

**Gate:** `PASS_CLEAN_SLATE_HANDOVER`

## Implementation Interfaces

### Equation Ledger

```markdown
| Eq ID | Equation | Origin Class | Depends On | Unit Check | Sign Check | Assumption IDs | Validity Domain | Failure Mode |
|---|---|---|---|---|---|---|---|---|
```

### Assumption Contract

```markdown
| Assumption ID | Statement | Evidence Status | Allowed Wording | Forbidden Wording | Failure Mode |
|---|---|---|---|---|---|
```

### Reviewer Attack Row

```markdown
| Attack ID | Role | Objection | Affected Claim/Eq | Resolution | Status |
|---|---|---|---|---|---|
```

## Required Core Logic Targets

These are target relations, not final manuscript wording.

```tex
r(Q)=\theta_e(\varphi(Q),T)-\theta(Q)
```

```tex
\frac{\dd\theta}{\dd t}=k r
```

```tex
\frac{\dd r}{\dd Q}+\frac{k}{v_Q}r=\frac{\dd\theta_e}{\dd Q}
```

```tex
r(Q)=r(Q_a)\exp\left[-\int_{Q_a}^{Q}\frac{k(Q')}{v_Q}\,\dd Q'\right]
```

```tex
L_Q=\frac{v_Q}{k}
\quad
\text{only as local constant-rate approximation}
```

```tex
\Delta G^\ddagger_{\mathrm{act}}(T,\psi)
=
\Delta G^\ddagger_0(T)-\Lambda_\psi F\psi,
\qquad
\Delta G^\ddagger_{\mathrm{act}}>0
```

```tex
k(T,\psi)=k_0(T)\exp\left[-\frac{\Delta G^\ddagger_{\mathrm{act}}(T,\psi)}{RT}\right]
```

```tex
L_\varphi\approx
\left|\frac{\dd\varphi}{\dd Q}\right|_{Q_a}L_Q
```

## Test Plan

| Test | Method | Pass Condition |
|---|---|---|
| Archive check | Directory listing | Old files under `Codex\old`, not active `results` |
| Source read coverage | Result tables | No cited source without read coverage |
| Equation origin | Ledger | Every equation has allowed origin |
| Assumption support | Contract | No `UNSUPPORTED_REMOVE` in manuscript |
| Unit audit | Manual table | Energy/rate/capacity/ICA units consistent |
| Sign audit | Manual table | Branch signs consistent |
| Double-counting audit | Reviewer table | Equilibrium target and mobility relation explained |
| Barrier audit | Search and logic audit | No cap/step/clipping barrier |
| ICA mapping audit | Derivation ledger | Capacity and voltage axes separated |
| Static TeX | regex/tool check | labels, refs, braces, environments pass |
| Compile | TeX engine if available | PDF builds or missing engine recorded |

## Assumptions

- The user wants execution after this restart unless a gate reveals a required decision.
- Chapter 1 is limited to theoretical background for tail behavior.
- Literature/source support may require browsing or local PDF review during Phase 002.
- Prior drafts are archive records, not source authority.

## Correction History

- This clean-slate plan starts after moving previous plans/results to `Codex\old\2026-05-28-reset-before-chapter1-clean-restart`.
- It replaces all prior active Chapter 1 plans.
