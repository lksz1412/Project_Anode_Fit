# Rigorous Physics Chapter 1 v2 Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. If independent literature/source review ranges become separable, use `superpowers:subagent-driven-development` only with explicit file/range assignments and final Codex integration. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild Chapter 1 into a paper-grade theoretical background for graphite negative-electrode ICA tail behavior, with no unsupported shortcuts, no step/cap-like barrier treatment, and no logical leaps.

**Architecture:** The new Chapter 1 must be derived from conservation, thermodynamics, transition-state or kinetic theory, and clearly labeled reduced-model assumptions. Every equation must have an origin class, an applicability domain, and a failure mode. Existing ChatGPT/Codex drafts may be used only as review material, hazard lists, and structure references, not as equation authority.

**Tech Stack:** LaTeX manuscript, Markdown result reports, equation-origin ledger, assumption-evidence ledger, static TeX checks, literature/source verification notes.

---

## Summary

The user clarified that the prior ChatGPT material, even when directionally imperfect, correctly aimed for a paper/patent-grade standard:

- physical meaning takes priority over fitting convenience;
- no hidden logical jumps;
- all assumptions must be defensible through theory or literature;
- arbitrary mathematical devices must not be mistaken for physics;
- the final text should be followable by an undergraduate reader while remaining rigorous enough for scholarly development.

This plan supersedes the previous "final Chapter 1" status of:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_first_principles_final.tex`

That file is now a reviewed draft with useful residual-tail structure, not the canonical final.

The new Chapter 1 v2 will focus only on the core theoretical logic:

1. graphite ICA peak tail is observed after a phase-transition peak;
2. temperature-dependent activation slows or accelerates relaxation;
3. present electrode potential may assist the transition by reducing an activation free-energy barrier;
4. finite relaxation produces a residual post-peak tail;
5. the capacity-axis tail length and voltage-axis ICA tail are connected without conflating axes;
6. peak area is not the Chapter 1 core argument.

## Current Ground Truth

| Item | Status |
|---|---|
| Active project | `D:\Projects\Project_Anode_Fit` |
| Active Codex workspace | `D:\Projects\Project_Anode_Fit\Codex` |
| Plan directory | `D:\Projects\Project_Anode_Fit\Codex\plans` |
| Results directory | `D:\Projects\Project_Anode_Fit\Codex\results` |
| Previous Codex Chapter 1 | Reviewed; not canonical |
| Previous Codex self-review | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_022_CODEX_CHAPTER1_SELF_REVIEW.md` |
| ChatGPT ch1-ch6 review | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_021_CHATGPT_CH1_CH6_FINAL_TEX_REVIEW.md` |
| User-provided ChatGPT final TeX | `C:\Users\lksz1\Downloads\graphite_ica_ch1_ch6_physical_v3_rechecked.tex` |
| TeX compile status | TeX engine not found in current environment; static checks only unless engine is installed |
| Claude folder | Do not modify unless explicitly requested |

## User Correction Locked As Ground Truth

- A barrier must not be handled by a step-function-like `max`, hard cap, clipping, or softplus device in the core physical theory.
- If an activation barrier is driven to zero or below by the reduced expression, that means the active-barrier approximation has left its validity domain; it does not authorize a clipped barrier law.
- Saturation or limiting behavior must be explained by physical bottlenecks such as attempt frequency, site availability, phase-boundary motion, diffusion, transport, or current conservation.
- The equilibrium target and the kinetic mobility may both depend on electrode potential only if the manuscript explains why this is not double counting.
- Assumptions must be explicitly labeled and must have a defensible basis in thermodynamics, kinetics, electrochemistry, or cited literature.
- Chapter 1 must stay about the basic theoretical logic of ICA tail behavior; fitting, solver construction, heat generation, and hysteresis are later chapters.

## Phase Range

| Phase | Name | Step Range | Primary Output | Gate |
|---|---|---:|---|---|
| Phase 023 | Rigorous Standard Reset And Evidence Policy | 1-20 | `PHASE_023_RIGOROUS_STANDARD_RESET_RESULT.md` | `PASS_RIGOR_POLICY_LOCKED` |
| Phase 024 | Source And Literature Evidence Inventory | 21-55 | `PHASE_024_SOURCE_EVIDENCE_INVENTORY_RESULT.md` | `PASS_EVIDENCE_INVENTORY` |
| Phase 025 | First-Principles Derivation Rebuild | 56-105 | `PHASE_025_CH1_V2_DERIVATION_LEDGER.md` | `PASS_DERIVATION_NO_LEAP_DRAFT` |
| Phase 026 | Assumption And Double-Counting Audit | 106-145 | `PHASE_026_ASSUMPTION_DOUBLE_COUNTING_AUDIT.md` | `PASS_ASSUMPTION_AUDIT` |
| Phase 027 | Chapter 1 v2 Manuscript Construction | 146-190 | `graphite_ica_chapter1_physics_rigorous_v2.tex` | `PASS_CH1_V2_MANUSCRIPT_CREATED` |
| Phase 028 | Ralph-Wiggum Logic Loop And Reviewer Attack | 191-245 | `PHASE_028_CH1_V2_LOGIC_ATTACK_RESULT.md` | `PASS_NO_CRITICAL_LOGIC_GAP` |
| Phase 029 | Static Verification And Handover | 246-275 | `PHASE_029_CH1_V2_FINAL_HANDOVER.md` | `PASS_CH1_V2_HANDOVER` |

Phase and step counts are minimum coverage. If a literature source, sign convention, or equation fails a gate, add repair subphases. Do not force the work into the listed phase count.

## Non-Goals

- Do not patch the previous `graphite_ica_chapter1_first_principles_final.tex` in place.
- Do not copy equations from ChatGPT/Codex prior drafts as authority.
- Do not use `max`, `min`, clipping, softplus, hard saturation, bounded transform, or step-function-like barrier treatment as the main physics.
- Do not build a solver.
- Do not write fitting code.
- Do not move Chapter 1 into heat generation, `dV/dT`, Butler-Volmer implementation, full-cell mapping, or hysteresis except as scoped roadmap notes.
- Do not claim literature support without actually reading and recording the source or section used.
- Do not modify `D:\Projects\Project_Anode_Fit\Claude`.
- Do not modify source TeX/PDF files in downloads or original folders.

## Implementation Changes

### Create

| Path | Purpose |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-rigorous-physics-chapter1-v2-plan.md` | This plan |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_023_029_CH1_V2_EXECUTION_LEDGER.md` | Phase ledger and compaction recovery index |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_023_RIGOROUS_STANDARD_RESET_RESULT.md` | User standard, banned shortcuts, equation policy |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_024_SOURCE_EVIDENCE_INVENTORY_RESULT.md` | Source list, literature basis, read coverage |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_025_CH1_V2_DERIVATION_LEDGER.md` | Equation-by-equation derivation and origin classes |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_026_ASSUMPTION_DOUBLE_COUNTING_AUDIT.md` | Assumption, double counting, sign, unit audit |
| `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_physics_rigorous_v2.tex` | New Chapter 1 v2 manuscript |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_028_CH1_V2_LOGIC_ATTACK_RESULT.md` | Ralph-Wiggum/adversarial review loop result |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_029_CH1_V2_FINAL_HANDOVER.md` | Final handover and continuation instructions |

### Preserve

| Path | Rule |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_first_principles_final.tex` | Preserve as reviewed non-canonical draft |
| `C:\Users\lksz1\Downloads\graphite_ica_ch1_ch6_physical_v3_rechecked.tex` | Read-only reference |
| `D:\Projects\Project_Anode_Fit\Claude` | Do not modify |

## Equation Origin Classes

Every equation in the derivation ledger and final manuscript must be assigned one of these classes:

| Class | Meaning | Requirement |
|---|---|---|
| `DEF` | Definition of a coordinate, variable, or observable | Must state units and sign convention |
| `CALC` | Algebraic or calculus consequence | Must show previous equation dependency |
| `CONS` | Conservation law or balance relation | Must identify conserved quantity |
| `THERMO` | Thermodynamic identity or free-energy relation | Must state thermodynamic variables and constraints |
| `KIN-TST` | Transition-state or activated-rate theory | Must cite theory/literature or clearly state reduced assumption |
| `KIN-RED` | Reduced kinetic model | Must state physical interpretation and failure mode |
| `LOCAL` | Local approximation | Must state expansion point and validity condition |
| `LIMIT` | Limiting regime | Must state what becomes dominant or non-rate-limiting |
| `ROADMAP` | Later-chapter relation | Must not be used as Chapter 1 proof |

Forbidden origin classes:

| Class | Reason |
|---|---|
| `FITTING_CONVENIENCE` | Not allowed as physical theory |
| `NUMERICAL_STABILIZER` | Not allowed in Chapter 1 core |
| `COPIED_PRIOR_DRAFT` | Prior drafts are not equation authority |
| `UNSUPPORTED_INTUITION` | Must be repaired or removed |

## Phase 023 — Rigorous Standard Reset And Evidence Policy

**Purpose:** Convert the user's correction into enforceable working rules before rewriting.

**Inputs:**

- User message on paper-grade physical meaning and valid assumptions.
- `PHASE_021_CHATGPT_CH1_CH6_FINAL_TEX_REVIEW.md`
- `PHASE_022_CODEX_CHAPTER1_SELF_REVIEW.md`
- Current plan.

**Steps:**

- [ ] Step 1: Create `PHASE_023_029_CH1_V2_EXECUTION_LEDGER.md`.
- [ ] Step 2: Record that the previous Codex Chapter 1 is non-canonical.
- [ ] Step 3: Record that ChatGPT ch1-ch6 is non-canonical but useful as physical-rigor reference and hazard checklist.
- [ ] Step 4: Lock the user standard: no hidden leaps, no unsupported assumptions, no mathematical cap as physics.
- [ ] Step 5: List explicitly banned Chapter 1 devices: `max`, `min`, clipping, softplus, capped transform, empirical residual, step-function barrier.
- [ ] Step 6: Define the allowed handling of barrier exhaustion: active-barrier regime ends; physical bottleneck or later-chapter rate limitation begins.
- [ ] Step 7: Define equation origin classes from this plan in the result file.
- [ ] Step 8: Define assumption evidence statuses: `SUPPORTED`, `TEXTBOOK_THEORY`, `LITERATURE_CONFIRMED`, `REDUCED_MODEL_DECLARED`, `UNSUPPORTED_REMOVE`, `LATER_CHAPTER`.
- [ ] Step 9: Define failure conditions for assumptions: e.g. if no source or theory basis is found, the assumption cannot enter final text as physical fact.
- [ ] Step 10: Define manuscript wording rule: assumptions must be introduced before being used in derivation.
- [ ] Step 11: Define undergraduate-followable rule: no equation transition may skip a required chain rule, sign convention, unit check, or limiting condition.
- [ ] Step 12: Define reviewer-attack rule: each core claim must survive at least one adversarial objection.
- [ ] Step 13: Define source citation policy for final TeX: cite only sources actually checked; if no citation is available, label as reduced assumption.
- [ ] Step 14: Define read coverage policy for all source files.
- [ ] Step 15: Create `PHASE_023_RIGOROUS_STANDARD_RESET_RESULT.md`.
- [ ] Step 16: Update ledger row for Phase 023.
- [ ] Step 17: Gate check: banned devices are named and mapped to replacement policy.
- [ ] Step 18: Gate check: prior drafts are not canonical equation sources.
- [ ] Step 19: Gate check: evidence statuses are defined.
- [ ] Step 20: If any gate fails, stop before Phase 024.

**Gate:** `PASS_RIGOR_POLICY_LOCKED`

Pass conditions:

- The banned shortcut list includes step/cap-like barrier handling.
- The replacement policy separates active-barrier regime from barrier-exhausted regime.
- Equation-origin and assumption-evidence classes are saved.

## Phase 024 — Source And Literature Evidence Inventory

**Purpose:** Gather the source basis required to support Chapter 1 assumptions.

**Inputs:**

- User-provided ChatGPT final TeX.
- Previous Codex Chapter 1 draft.
- ChatGPT and Codex review reports.
- Original project TeX/PDF files if needed.
- User's paper and references 6, 7 if they are needed for integral/self-consistent method context.
- External literature only when necessary for transition-state theory, thermodynamics, ICA/DVA, graphite staging, or activation barrier assumptions.

**Steps:**

- [ ] Step 21: List all local source files relevant to Chapter 1 in `D:\Projects\Project_Anode_Fit` and original provided folders.
- [ ] Step 22: Record file path, size, line count or page count, and intended use for each source.
- [ ] Step 23: Mark each source as `FULL_READ_REQUIRED`, `STRUCTURE_ONLY`, `REFERENCE_ONLY`, or `DO_NOT_USE_AS_AUTHORITY`.
- [ ] Step 24: Re-open `PHASE_021_CHATGPT_CH1_CH6_FINAL_TEX_REVIEW.md` and extract hazard items.
- [ ] Step 25: Re-open `PHASE_022_CODEX_CHAPTER1_SELF_REVIEW.md` and extract repair items.
- [ ] Step 26: Read the current Codex Chapter 1 draft only as reviewed non-canonical source; record exact line coverage.
- [ ] Step 27: Read the ChatGPT ch1-ch6 TeX only as structure/hazard source if line-level claims are reused; record exact line coverage.
- [ ] Step 28: Identify which assumptions need external theory support: activated rate, transition-state lowering by work, relaxation-to-target, graphite staging equilibrium fraction, ICA mapping.
- [ ] Step 29: Identify which assumptions can be supported by basic calculus/conservation without external citation.
- [ ] Step 30: Identify which assumptions are reduced model choices and must be labeled as such.
- [ ] Step 31: If using transition-state theory, locate a defensible source or textbook-level basis.
- [ ] Step 32: If using electrochemical activation/overpotential barrier lowering, locate a defensible electrochemical kinetics source.
- [ ] Step 33: If using graphite staging thermodynamics, locate graphite/staging/phase-transition source or explicitly avoid overclaiming.
- [ ] Step 34: If using ICA/DVA mapping, locate or derive from calculus and charge balance.
- [ ] Step 35: If ref. 6, 7 from user's paper are relevant, locate the user's paper and identify exact references.
- [ ] Step 36: Read the user's paper sections where ref. 6, 7 are cited before using them.
- [ ] Step 37: Do not import ref. 6, 7 method into Chapter 1 unless it is needed for self-consistent integral structure; otherwise classify as later numerical/method chapter.
- [ ] Step 38: Create an assumption-evidence table with columns: assumption, source type, exact source, support level, allowed wording.
- [ ] Step 39: Create a missing-evidence table with columns: claim, needed support, current status, action.
- [ ] Step 40: Mark any unsupported physical claim as `UNSUPPORTED_REMOVE`.
- [ ] Step 41: Create `PHASE_024_SOURCE_EVIDENCE_INVENTORY_RESULT.md`.
- [ ] Step 42: Update ledger row for Phase 024.
- [ ] Step 43: Gate check: every planned Chapter 1 assumption has an evidence status.
- [ ] Step 44: Gate check: no unsupported assumption is allowed into the final manuscript as fact.
- [ ] Step 45: Gate check: source read coverage is recorded.
- [ ] Step 46: Gate check: literature not yet read is not cited as support.
- [ ] Step 47: Gate check: ref. 6, 7 are either verified or explicitly deferred.
- [ ] Step 48: Gate check: old drafts are not equation authority.
- [ ] Step 49: If source support is insufficient for a core claim, revise the target claim before Phase 025.
- [ ] Step 50: If source files are too large for one pass, create subphase read ranges and continue until complete.
- [ ] Step 51: If web/literature search is needed, record URLs/DOI and access date.
- [ ] Step 52: If no reliable source is found for a claim, record `근거 미발견`.
- [ ] Step 53: Create a compact source map for later compaction recovery.
- [ ] Step 54: Validate result file contains no unverified `PASS`.
- [ ] Step 55: Stop if any essential assumption lacks either theory support or reduced-model labeling.

**Gate:** `PASS_EVIDENCE_INVENTORY`

Pass conditions:

- Every planned assumption is classified.
- Unsupported claims are removed, downgraded, or deferred.
- Source read coverage and literature status are recorded.

## Phase 025 — First-Principles Derivation Rebuild

**Purpose:** Rebuild the Chapter 1 derivation from the locked evidence basis.

**Steps:**

- [ ] Step 56: Start a new derivation ledger, not the manuscript.
- [ ] Step 57: Define the observed phenomenon in words: low-temperature long tail, high-temperature shorter tail, present-potential-assisted barrier lowering.
- [ ] Step 58: Define analysis coordinate `Q` and its unit.
- [ ] Step 59: Define analysis potential `\varphi` and branch direction.
- [ ] Step 60: Define ICA and DVA from calculus.
- [ ] Step 61: State full-cell exclusion and negative-electrode scope.
- [ ] Step 62: Define equilibrium transformed fraction `\theta_e(\varphi,T)` as a thermodynamic target, not a fitted peak shape.
- [ ] Step 63: State monotonic branch condition for the local transition region.
- [ ] Step 64: Define actual transformed fraction `\theta(Q)`.
- [ ] Step 65: Define residual lag `r=\theta_e-\theta`.
- [ ] Step 66: State sign condition for post-peak residual.
- [ ] Step 67: Introduce first-order relaxation as `KIN-RED`, not as a universal microscopic law.
- [ ] Step 68: Record physical interpretation of first-order relaxation: local coarse-grained return toward target.
- [ ] Step 69: Record failure mode of first-order relaxation: multiple modes, memory, nucleation, or strong hysteresis require later chapters.
- [ ] Step 70: Convert time derivative to capacity coordinate with `v_Q=dQ/dt`.
- [ ] Step 71: Derive residual ODE by explicit chain rule.
- [ ] Step 72: Derive post-peak homogeneous residual equation.
- [ ] Step 73: Derive capacity-axis tail length `L_Q=v_Q/k`.
- [ ] Step 74: Add variable-rate generalization: `r(Q)=r(Q_a)\exp[-\int_{Q_a}^{Q} k(Q')/v_Q\,dQ']`.
- [ ] Step 75: Use constant-rate exponential only as local approximation.
- [ ] Step 76: Define intrinsic activation free energy in a local temperature window.
- [ ] Step 77: Define present-potential assisting work without step/cap handling.
- [ ] Step 78: Replace projection ambiguity with an effective coupling coefficient whose units are explicit.
- [ ] Step 79: Define active-barrier regime: `\Delta G_act^\ddagger(T,\psi)>0`.
- [ ] Step 80: Derive active-regime Arrhenius rate.
- [ ] Step 81: Derive `\partial \ln L_Q/\partial \psi < 0` in the active-barrier regime.
- [ ] Step 82: Derive temperature trend condition from `\partial \ln L_Q/\partial T`.
- [ ] Step 83: State low-temperature long-tail condition as `k` decreases, not as an unconditional law.
- [ ] Step 84: State high-temperature short-tail condition as `k` increases, not as an unconditional law.
- [ ] Step 85: Define barrier-exhausted regime without clipping: activation barrier no longer rate-limiting.
- [ ] Step 86: List allowed physical bottlenecks in the barrier-exhausted regime but keep them outside Chapter 1 core.
- [ ] Step 87: Add equilibrium-target/mobility consistency condition to avoid double counting.
- [ ] Step 88: Show a minimal forward/backward consistency statement or explicitly mark the barrier term as reduced mobility assumption.
- [ ] Step 89: Define background differential capacity.
- [ ] Step 90: Define phase-transition charge contribution.
- [ ] Step 91: Derive incremental storage equation.
- [ ] Step 92: Derive `d\varphi/dQ`.
- [ ] Step 93: Derive ICA inverse relation.
- [ ] Step 94: State ICA denominator validity condition.
- [ ] Step 95: Derive capacity-axis tail inheritance into `d\theta/dQ`.
- [ ] Step 96: Add voltage-axis conversion `L_\varphi \approx |d\varphi/dQ|_a L_Q` as a local mapping.
- [ ] Step 97: State that the voltage-axis mapping can distort the apparent tail if `d\varphi/dQ` varies strongly.
- [ ] Step 98: Separate equilibrium heterogeneity from kinetic residual tail.
- [ ] Step 99: State that Chapter 1 explains the kinetic tail component, not every possible tail source.
- [ ] Step 100: Build an equation dependency graph.
- [ ] Step 101: Assign every equation an origin class.
- [ ] Step 102: Assign every assumption an evidence status from Phase 024.
- [ ] Step 103: Create `PHASE_025_CH1_V2_DERIVATION_LEDGER.md`.
- [ ] Step 104: Update ledger row for Phase 025.
- [ ] Step 105: Gate check: no equation has unsupported origin.

**Gate:** `PASS_DERIVATION_NO_LEAP_DRAFT`

Pass conditions:

- Residual-to-tail derivation is complete.
- Active-barrier regime is separated from barrier-exhausted regime.
- No step/cap barrier law appears in the core derivation.
- Every equation has origin class and dependency.

## Phase 026 — Assumption And Double-Counting Audit

**Purpose:** Attack the derivation before writing the polished manuscript.

**Steps:**

- [ ] Step 106: Audit dimensions of every equation.
- [ ] Step 107: Audit signs of `Q`, `\varphi`, `\psi`, `r`, and `d\theta/dQ`.
- [ ] Step 108: Audit the transition from time coordinate to capacity coordinate.
- [ ] Step 109: Audit whether `\theta_e(\varphi,T)` and `k(T,\psi)` double count the same free-energy term.
- [ ] Step 110: If double counting cannot be ruled out, rewrite as explicit reduced mobility assumption.
- [ ] Step 111: Audit active-barrier condition and ensure all derivative claims are limited to that condition.
- [ ] Step 112: Audit barrier-exhausted language and ensure no clipped expression sneaks back in.
- [ ] Step 113: Audit whether temperature trend claims are conditional.
- [ ] Step 114: Audit whether present-potential trend claims are conditional.
- [ ] Step 115: Audit whether equilibrium heterogeneity is acknowledged.
- [ ] Step 116: Audit ICA denominator and singularity conditions.
- [ ] Step 117: Audit voltage-axis mapping and local approximation condition.
- [ ] Step 118: Audit undergraduate readability: every equation transition must have a prose bridge.
- [ ] Step 119: Audit literature support for assumptions.
- [ ] Step 120: Audit that unsupported items are removed or marked as reduced assumptions.
- [ ] Step 121: Audit that Chapter 2-5 content does not enter Chapter 1 proof.
- [ ] Step 122: Audit that peak area is not used as the core explanation.
- [ ] Step 123: Audit that fitting language is absent from core derivation.
- [ ] Step 124: Audit that no previous draft equation is treated as authority.
- [ ] Step 125: Create an objections table with columns: reviewer objection, affected equation, answer, repair needed.
- [ ] Step 126: Repair derivation ledger if any objection exposes a real gap.
- [ ] Step 127: Re-run dimensions and signs after repair.
- [ ] Step 128: Create `PHASE_026_ASSUMPTION_DOUBLE_COUNTING_AUDIT.md`.
- [ ] Step 129: Update ledger row for Phase 026.
- [ ] Step 130: Gate check: no `UNSUPPORTED_REMOVE` item remains in the planned manuscript.
- [ ] Step 131: Gate check: no barrier cap appears.
- [ ] Step 132: Gate check: active-barrier and barrier-exhausted regimes are separated.
- [ ] Step 133: Gate check: double-counting objection has an explicit answer.
- [ ] Step 134: Gate check: all trend claims are conditional.
- [ ] Step 135: If any P1 issue remains, return to Phase 025.
- [ ] Step 136: If any source support is missing, return to Phase 024.
- [ ] Step 137: If only wording issues remain, carry them to Phase 027.
- [ ] Step 138: Validate audit report has read coverage and equation coverage.
- [ ] Step 139: Validate no unverified PASS wording.
- [ ] Step 140: Record decision queue for user if a physical assumption has two defensible options.
- [ ] Step 141: Do not proceed to manuscript if user decision is required for a core convention.
- [ ] Step 142: If no user decision is required, mark manuscript-ready.
- [ ] Step 143: Create compaction recovery notes.
- [ ] Step 144: Store final derivation dependency graph path.
- [ ] Step 145: Proceed to Phase 027 only after gate pass.

**Gate:** `PASS_ASSUMPTION_AUDIT`

Pass conditions:

- The derivation is internally consistent.
- No core assumption lacks support or explicit reduced-model labeling.
- No active reviewer objection remains unresolved at P1 severity.

## Phase 027 — Chapter 1 v2 Manuscript Construction

**Purpose:** Write the new Chapter 1 manuscript from the audited derivation, not by patching the old file.

**Steps:**

- [ ] Step 146: Create `graphite_ica_chapter1_physics_rigorous_v2.tex`.
- [ ] Step 147: Add title and abstract that do not mention finality beyond the actual result.
- [ ] Step 148: Add convention section before derivation.
- [ ] Step 149: Include negative-electrode/full-cell boundary.
- [ ] Step 150: Include axis definitions and units.
- [ ] Step 151: Include observation statement focused on tail behavior.
- [ ] Step 152: Include equilibrium vs kinetic-tail distinction with caveat about heterogeneity.
- [ ] Step 153: Define equilibrium target and actual fraction.
- [ ] Step 154: Define branch monotonicity assumptions.
- [ ] Step 155: Define residual lag.
- [ ] Step 156: Derive first-order relaxation with assumption label in prose.
- [ ] Step 157: Derive capacity-coordinate residual ODE.
- [ ] Step 158: Derive local exponential tail.
- [ ] Step 159: Include variable-rate integral form.
- [ ] Step 160: Define active activation free-energy regime.
- [ ] Step 161: Define present-potential assisting work with explicit units.
- [ ] Step 162: Avoid `max`, clipping, or bounded barrier expression.
- [ ] Step 163: Derive active-regime rate.
- [ ] Step 164: Derive tail length in active regime.
- [ ] Step 165: Derive potential derivative of tail length.
- [ ] Step 166: Derive temperature derivative condition.
- [ ] Step 167: Add barrier-exhausted regime as limit, not as formula cap.
- [ ] Step 168: Add equilibrium-target/mobility consistency subsection.
- [ ] Step 169: Add ICA mapping from incremental storage.
- [ ] Step 170: Add denominator validity and peak-center caveat.
- [ ] Step 171: Add voltage-axis conversion.
- [ ] Step 172: Add interpretation summary.
- [ ] Step 173: Add limitations.
- [ ] Step 174: Add Chapter 2-5 roadmap.
- [ ] Step 175: Add references only for actually checked literature.
- [ ] Step 176: Ensure manuscript body contains no phase/work-history notes.
- [ ] Step 177: Ensure all symbols are introduced before use.
- [ ] Step 178: Ensure all equations in final TeX are present in derivation ledger.
- [ ] Step 179: Ensure all assumptions in final TeX appear in assumption ledger.
- [ ] Step 180: Run static label/ref check.
- [ ] Step 181: Run brace/environment check.
- [ ] Step 182: Check for banned terms and patterns: `max`, `softplus`, `clip`, `cap`, `step`, `bounded transform` in core equations.
- [ ] Step 183: Check for old file names or invalidated manuscript references in final body.
- [ ] Step 184: Record line count and hash.
- [ ] Step 185: Create manuscript construction result note if needed.
- [ ] Step 186: Update ledger row for Phase 027.
- [ ] Step 187: Gate check: final manuscript follows audited derivation.
- [ ] Step 188: Gate check: no core equation appears without ledger entry.
- [ ] Step 189: Gate check: no banned barrier shortcut appears.
- [ ] Step 190: If gate fails, repair manuscript before Phase 028.

**Gate:** `PASS_CH1_V2_MANUSCRIPT_CREATED`

Pass conditions:

- New manuscript exists.
- It is not a patch of the old file.
- No unsupported or capped barrier law appears.

## Phase 028 — Ralph-Wiggum Logic Loop And Reviewer Attack

**Purpose:** Run repeated simple-reader and adversarial-review passes until the logic no longer depends on hidden intuition.

**Review Roles:**

| Role | Question |
|---|---|
| Undergraduate reader | Can every equation transition be followed from prior definitions? |
| Reviewer 1: thermodynamics | Are equilibrium and kinetic terms double counted? |
| Reviewer 2: kinetics | Is the barrier-lowering rate law valid only in its stated regime? |
| Reviewer 3: electrochemistry | Are potential, overpotential, and work terms convention-safe? |
| Reviewer 4: ICA/DVA | Does capacity-axis tail actually map to voltage-axis ICA? |
| Reviewer 5: skeptical modeler | Is any fitting convenience disguised as physics? |

**Steps:**

- [ ] Step 191: Read final TeX from line 1 to end.
- [ ] Step 192: Create a claim list from the manuscript.
- [ ] Step 193: For each claim, identify supporting equation or source.
- [ ] Step 194: Run undergraduate-reader pass.
- [ ] Step 195: Mark any skipped algebra step.
- [ ] Step 196: Repair skipped steps in manuscript.
- [ ] Step 197: Run thermodynamics reviewer pass.
- [ ] Step 198: Attack equilibrium/mobility double-counting.
- [ ] Step 199: Repair if the answer is not explicit.
- [ ] Step 200: Run kinetics reviewer pass.
- [ ] Step 201: Attack activation-barrier regime and barrier-exhausted limit.
- [ ] Step 202: Repair if active-regime boundaries are unclear.
- [ ] Step 203: Run electrochemistry reviewer pass.
- [ ] Step 204: Attack sign and unit of potential work.
- [ ] Step 205: Repair if convention is ambiguous.
- [ ] Step 206: Run ICA/DVA reviewer pass.
- [ ] Step 207: Attack voltage-axis mapping.
- [ ] Step 208: Repair if only capacity-axis result is shown.
- [ ] Step 209: Run skeptical-modeler pass.
- [ ] Step 210: Search for fitting convenience or numerical stabilizer language.
- [ ] Step 211: Remove or quarantine any such language.
- [ ] Step 212: Re-run banned pattern search.
- [ ] Step 213: Re-run static TeX checks.
- [ ] Step 214: Re-open assumption ledger and verify final text matches it.
- [ ] Step 215: Re-open equation ledger and verify final equations match it.
- [ ] Step 216: If any P1 issue remains, return to Phase 027.
- [ ] Step 217: If any assumption lacks support, return to Phase 024 or remove claim.
- [ ] Step 218: If any derivation gap remains, return to Phase 025.
- [ ] Step 219: If only style issues remain, repair in Phase 028.
- [ ] Step 220: Create `PHASE_028_CH1_V2_LOGIC_ATTACK_RESULT.md`.
- [ ] Step 221: Update ledger row for Phase 028.
- [ ] Step 222: Gate check: no P1/P2 unresolved findings remain.
- [ ] Step 223: Gate check: every reviewer objection has answer or repair.
- [ ] Step 224: Gate check: simple-reader pass can follow every equation transition.
- [ ] Step 225: Gate check: no unsupported assumption remains.
- [ ] Step 226: Gate check: no banned barrier treatment remains.
- [ ] Step 227: If gate fails, document failure and loop.
- [ ] Step 228: If gate passes, mark manuscript final-candidate.
- [ ] Step 229: Record line count and hash after repairs.
- [ ] Step 230: Record TeX engine availability.
- [ ] Step 231: If TeX engine exists, compile and record log.
- [ ] Step 232: If TeX engine does not exist, record static-only verification.
- [ ] Step 233: Record non-changes: original sources untouched, Claude untouched.
- [ ] Step 234: Prepare handover notes.
- [ ] Step 235: Verify result files can recover work after compaction.
- [ ] Step 236: Verify plan step numbers and result references match.
- [ ] Step 237: Verify no work-history notes are inside final TeX body.
- [ ] Step 238: Verify final TeX references only checked literature.
- [ ] Step 239: Verify final TeX does not claim peak area theory.
- [ ] Step 240: Verify final TeX keeps Chapter 2-5 as roadmap.
- [ ] Step 241: Re-read final abstract after all repairs.
- [ ] Step 242: Re-read final conclusion after all repairs.
- [ ] Step 243: Check abstract and conclusion do not overclaim.
- [ ] Step 244: Save final Phase 028 report.
- [ ] Step 245: Proceed to Phase 029.

**Gate:** `PASS_NO_CRITICAL_LOGIC_GAP`

Pass conditions:

- Every P1/P2 reviewer attack is resolved.
- The manuscript contains no hidden cap/step barrier handling.
- The central claim is conditional, physical, and traceable.

## Phase 029 — Static Verification And Handover

**Purpose:** Leave a clean recovery point and final status report.

**Steps:**

- [ ] Step 246: Re-run label/ref check.
- [ ] Step 247: Re-run brace/environment check.
- [ ] Step 248: Re-run banned pattern search.
- [ ] Step 249: Re-run source-reference check.
- [ ] Step 250: Re-run equation-ledger coverage check.
- [ ] Step 251: Re-run assumption-ledger coverage check.
- [ ] Step 252: Check TeX engine availability.
- [ ] Step 253: Compile if available.
- [ ] Step 254: If compile unavailable, record exact missing tools.
- [ ] Step 255: Record final manuscript path.
- [ ] Step 256: Record final line count.
- [ ] Step 257: Record final SHA256.
- [ ] Step 258: Record all result files.
- [ ] Step 259: Record actual read coverage.
- [ ] Step 260: Record actual literature/source coverage.
- [ ] Step 261: Record unresolved issues if any.
- [ ] Step 262: Record decision queue if user input is required.
- [ ] Step 263: Record confirmed non-changes.
- [ ] Step 264: Record how to resume after compaction.
- [ ] Step 265: Create `PHASE_029_CH1_V2_FINAL_HANDOVER.md`.
- [ ] Step 266: Update `PHASE_023_029_CH1_V2_EXECUTION_LEDGER.md`.
- [ ] Step 267: Gate check: final files exist.
- [ ] Step 268: Gate check: verification results are recorded.
- [ ] Step 269: Gate check: no incomplete phase is reported as complete.
- [ ] Step 270: Gate check: final answer to user separates completed, unverified, and open items.
- [ ] Step 271: If user requested only plan, do not execute beyond plan without instruction.
- [ ] Step 272: If execution was requested, provide final concise report.
- [ ] Step 273: Do not commit unless user explicitly asks.
- [ ] Step 274: Do not push or merge.
- [ ] Step 275: End with clear next action.

**Gate:** `PASS_CH1_V2_HANDOVER`

Pass conditions:

- Final handover and ledger are complete.
- Verification evidence is explicit.
- Remaining limitations are not hidden.

## Implementation Interfaces

### Equation Ledger Row

```markdown
| Eq ID | Equation | Origin Class | Depends On | Units Check | Assumptions | Validity Domain | Failure Mode | Final TeX Section |
|---|---|---|---|---|---|---|---|---|
```

### Assumption Ledger Row

```markdown
| Assumption ID | Statement | Evidence Status | Source / Basis | Allowed Wording | Not Allowed Wording | Failure Mode |
|---|---|---|---|---|---|---|
```

### Reviewer Objection Row

```markdown
| Objection ID | Reviewer Role | Objection | Affected Eq/Claim | Status | Repair / Answer | Verified In |
|---|---|---|---|---|---|---|
```

### Required Core Equations For v2

These are not final wording; they are required logical targets.

```tex
r(Q)=\theta_e(\varphi(Q),T)-\theta(Q)
```

```tex
\frac{\dd\theta}{\dd t}=k\,r
```

```tex
\frac{\dd r}{\dd Q}
+
\frac{k}{v_Q}r
=
\frac{\dd\theta_e}{\dd Q}
```

```tex
r(Q)
=
r(Q_a)
\exp\!\left[
-\int_{Q_a}^{Q}\frac{k(Q')}{v_Q}\,\dd Q'
\right]
```

```tex
L_Q=\frac{v_Q}{k}
\quad
\text{only when } k/v_Q \text{ is locally constant}
```

```tex
\Delta G_{\mathrm{act}}^\ddagger(T,\psi)
=
\Delta G_0^\ddagger(T)-\Lambda_\psi F\psi,
\qquad
\Delta G_{\mathrm{act}}^\ddagger>0
```

```tex
k(T,\psi)
=
k_0(T)
\exp\!\left[
-\frac{\Delta G_{\mathrm{act}}^\ddagger(T,\psi)}{RT}
\right]
```

```tex
\frac{\partial \ln L_Q}{\partial \psi}
=
-\frac{1}{RT}
\frac{\partial \Delta G_{\mathrm{act}}^\ddagger}{\partial \psi}
<
0
\quad
\text{if } \partial \Delta G_{\mathrm{act}}^\ddagger/\partial \psi<0
```

```tex
L_\varphi
\approx
\left|
\frac{\dd\varphi}{\dd Q}
\right|_{Q_a}
L_Q
```

### Forbidden Core Equation Patterns

```tex
B=\max(\cdots,0)
```

```tex
B=\operatorname{softplus}(\cdots)
```

```tex
k=\min(k_{\mathrm{act}},k_{\max})
```

```tex
\Delta G_{\mathrm{eff}}=\text{clipped value}
```

These may appear only in a result report as rejected ideas, not in the final Chapter 1 core theory.

## Test Plan

| Test | Method | Pass Condition |
|---|---|---|
| Read coverage | Record line/page ranges in each result | No source used without coverage record |
| Equation origin | Ledger check | Every final equation has origin class |
| Assumption evidence | Ledger check | Every physical assumption has support or reduced-model label |
| Unit audit | Manual equation table | Energy, rate, capacity, ICA units consistent |
| Sign audit | Manual branch table | `Q`, `\varphi`, `\psi`, `r`, `L_Q` signs consistent |
| Double-counting audit | Reviewer objection table | Equilibrium target and mobility relation explained |
| Barrier audit | Search final TeX and logic report | No `max`, clipping, softplus, cap in core theory |
| Temperature trend audit | Derivative and prose check | Low/high temperature claims are conditional |
| Potential trend audit | Derivative and prose check | Present-potential tail shortening limited to active regime |
| ICA mapping audit | Equation chain check | Capacity-axis and voltage-axis tails separated |
| TeX static check | Regex/PowerShell/Python | Brace, environment, label/ref pass |
| Compile check | `xelatex`/`pdflatex`/`tectonic` if available | PDF builds or missing engine recorded |

## Assumptions

- Chapter 1 may use a first-order relaxation law only as a reduced local kinetic model, not as a universal microscopic law.
- Chapter 1 may use transition-state/activated-rate logic only in an explicitly stated active-barrier regime.
- Present-potential assistance may enter mobility only if double-counting with equilibrium target is addressed.
- Equilibrium heterogeneity may shape peaks; Chapter 1 v2 focuses on kinetic residual tail.
- Literature support may be collected during execution; until read and recorded, no source is treated as confirmed.

## Correction History

- This plan supersedes the previous `first-principles Chapter 1 final` status.
- It incorporates the Phase 022 finding that `B=max(G_raw,0)` is not acceptable as core physics.
- It incorporates the user's requirement that assumptions be paper-grade, physically meaningful, and theory/literature defensible.
