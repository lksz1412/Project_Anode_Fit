# Chapter 1 Theory Completion Ralph Wiggum Loop Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. This is a document-theory plan, not a software implementation plan. Steps use checkbox (`- [ ]`) syntax for tracking, but no git commit is performed unless the user explicitly asks.

**Goal:** Produce a logically complete Chapter 1 theory artifact for graphite ICA / dQdV, with every equation transition explicit enough for a university undergraduate reader to follow.

**Architecture:** The current rebuilt manuscript is treated as a scaffold, not as the final accepted Chapter 1. The new output isolates theory from solver/fitting implementation, derives the charge-balance model from first principles, and runs Ralph Wiggum-style fail-repair-reverify loops until no confirmed logical gap remains.

**Tech Stack:** LaTeX source only; PowerShell text scans for static checks; project-local markdown ledgers for evidence, loop state, and handover.

---

## Summary

This plan supersedes the implementation-adjacent direction recorded in rebuild v2 for the active task. The active task is not solver construction, fitting code, or actual data fitting. The active task is the theoretical derivation of graphite incremental capacity analysis (ICA, `dQ/dV`) and differential voltage analysis (DVA, `dV/dQ`) from a charge-balance formulation.

The central acceptance criterion is logical completeness:

- every symbol is defined before use;
- every dependent variable has an owner equation;
- `V_n` is introduced only as an implicit charge-balance root;
- self-consistent feedback is treated as a fixed-point / integral equation, not as a contradiction;
- `dV/dq`, `dQ/dV`, peak position, peak width, and peak area are derived through visible intermediate steps;
- solver/fitting implementation language is removed from the Chapter 1 body unless it is explicitly framed as outside the chapter scope.

The user-provided physical observation that must be explained is:

- in LIB ICA, peak structures arise from graphite phase transitions whose apparent shape depends on temperature and the current potential/state;
- for the same transition, the integrated peak area should remain tied to the same transition capacity if the transition completes over the analyzed interval;
- the tail shape changes: at low temperature the tail is longer, while at higher temperature it decays more quickly;
- the document must explain this through a thermodynamic/state-variable framework without jumping into solver or fitting implementation.

The Ralph Wiggum Loop is adapted from the local harness reference:

1. run a hard logic gate;
2. parse failure messages into exact defects;
3. update the plan/ledger with failure cause and repair direction;
4. repair the document from the saved plan/ledger state;
5. rerun the gate;
6. repeat up to 10 rounds, escalating if the same failure repeats 3 times or if a user decision is truly required.

## Current Ground Truth

| Item | Status |
|---|---|
| Active project | `D:\Projects\Project_Anode_Fit` |
| Codex workspace | `D:\Projects\Project_Anode_Fit\Codex` |
| Plan directory | `D:\Projects\Project_Anode_Fit\Codex\plans` |
| Result directory | `D:\Projects\Project_Anode_Fit\Codex\results` |
| User clarification | current scope is theory derivation only, not solver/fitting implementation |
| User physical observation | same transition area, temperature- and state-dependent tail shape; low temperature gives a longer tail, high temperature a shorter tail |
| Scope correction record | `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_SCOPE_CORRECTION_2026-05-28.md` |
| Current scaffold manuscript | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_rebuilt_manuscript_v1.tex` |
| New target manuscript | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_theory_complete.tex` |

## Phase Range

- Phase 001: Loop baseline and source reconfirmation — Steps 1-35
- Phase 002: Dependency graph and theory contract — Steps 36-85
- Phase 003: Chapter 1 theory manuscript construction — Steps 86-155
- Phase 004: Ralph Wiggum Loop Round 1, naive-reader and definition gate — Steps 156-205
- Phase 005: Ralph Wiggum Loop Round 2, mathematical dependency gate — Steps 206-260
- Phase 006: Ralph Wiggum Loop Round 3, physical interpretation gate — Steps 261-315
- Phase 007: Ralph Wiggum Loop Round 4, undergraduate continuity gate — Steps 316-370
- Phase 008: Ralph Wiggum Loop convergence and handover — Steps 371-425

## Non-goals

- Do not implement a numerical solver.
- Do not write fitting code.
- Do not fit experimental data.
- Do not claim fitted parameters, quantitative error bounds, or performance.
- Do not overwrite original `.tex` sources or the user PDF.
- Do not modify `D:\Projects\Project_Anode_Fit\Claude`.
- Do not place phase, audit, loop, or change-history notes inside the LaTeX manuscript body.
- Do not import molecular-pair physics from refs. 6/7 into graphite staging.
- Do not use `graphite_ica_rebuilt_manuscript_v1.tex` as an accepted final body; it is only a scaffold.

## Implementation Changes

Planned new files:

- `D:\Projects\Project_Anode_Fit\Codex\results\CHAPTER1_THEORY_RALPH_LOOP_LEDGER.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\CHAPTER1_THEORY_DEPENDENCY_GRAPH.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\CHAPTER1_THEORY_DERIVATION_CONTRACT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_theory_complete.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\CHAPTER1_THEORY_RALPH_LOOP_ROUND_001_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\CHAPTER1_THEORY_RALPH_LOOP_ROUND_002_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\CHAPTER1_THEORY_RALPH_LOOP_ROUND_003_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\CHAPTER1_THEORY_RALPH_LOOP_ROUND_004_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\CHAPTER1_THEORY_FINAL_HANDOVER.md`

Planned updated files:

- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_EXECUTION_LEDGER.md`

## Phase 001 — Loop Baseline And Source Reconfirmation

- [ ] **Step 1:** Confirm active project and Codex workspace paths.
- [ ] **Step 2:** Re-open project `AGENTS.md`.
- [ ] **Step 3:** Re-open the scope correction file.
- [ ] **Step 4:** Re-open the Ralph Wiggum Loop reference.
- [ ] **Step 5:** Record that the current user instruction requests looped logic verification until convergence.
- [ ] **Step 6:** Create `CHAPTER1_THEORY_RALPH_LOOP_LEDGER.md`.
- [ ] **Step 7:** Add ledger columns: `Round`, `Gate`, `Failures`, `Repair`, `Status`, `Evidence`.
- [ ] **Step 8:** Record max 10 loop rounds and 3 repeated-failure escalation rule.
- [ ] **Step 9:** Record that phase boundaries do not require user interruption unless a real decision is reached.
- [ ] **Step 10:** Confirm mandatory source paths exist.
- [ ] **Step 11:** Re-read corrected ver1 source metadata and line count.
- [ ] **Step 12:** Re-read current scaffold manuscript metadata and section map.
- [ ] **Step 13:** Re-read Phase 006 math package metadata.
- [ ] **Step 14:** Re-read Phase 007 closure contract metadata.
- [ ] **Step 15:** Re-read Phase 014 final handover metadata.
- [ ] **Step 16:** Record read coverage actually used in this plan.
- [ ] **Step 17:** Mark source files read-only.
- [ ] **Step 18:** Mark Claude folder out of write scope.
- [ ] **Step 19:** Define active output as a new file, not a patch of the existing scaffold.
- [ ] **Step 20:** Gate Phase 001 only if the loop ledger exists and source boundaries are recorded.
- [ ] **Step 21:** Stop if corrected ver1 source is missing.
- [ ] **Step 22:** Stop if the output target would overwrite an original source.
- [ ] **Step 23:** Stop if the loop state cannot be saved under `Codex\results`.
- [ ] **Step 24:** Save Phase 001 result in the loop ledger.
- [ ] **Step 25:** Proceed directly to Phase 002 if no user decision is required.

Additional source-check steps:

- [ ] **Step 26:** Record exact source path for corrected ver1.
- [ ] **Step 27:** Record exact source path for ver5 only as historical chapter structure.
- [ ] **Step 28:** Record exact source path for user PDF only as methodological background.
- [ ] **Step 29:** Record that full refs. 6/7 are not used for strong derivation claims.
- [ ] **Step 30:** Record no solver/fitting artifact is required for acceptance.
- [ ] **Step 31:** Record the undergraduate-reader acceptance criterion.
- [ ] **Step 32:** Record no PDF build is required for logic acceptance.
- [ ] **Step 33:** Record static LaTeX checks to be run after writing.
- [ ] **Step 34:** Record git status.
- [ ] **Step 35:** Gate Phase 001 with `PASS_CH1_THEORY_LOOP_BASELINE`.

## Phase 002 — Dependency Graph And Theory Contract

- [ ] **Step 36:** Create `CHAPTER1_THEORY_DEPENDENCY_GRAPH.md`.
- [ ] **Step 37:** Create `CHAPTER1_THEORY_DERIVATION_CONTRACT.md`.
- [ ] **Step 38:** Define all independent variables: `t`, `q`, `Q_ext`, `T`, current orientation.
- [ ] **Step 39:** Define all dependent variables: `V_n`, `V_app`, `xi_j`, `Q_bg`.
- [ ] **Step 40:** Define all parameters: `Q_cell`, `Q_{j,tot}`, stage index `j`, transition parameters.
- [ ] **Step 41:** Define observable target: ICA as `dQ_ext/dV` and DVA as `dV/dQ_ext`.
- [ ] **Step 42:** Build dependency order from measurement coordinate to ICA.
- [ ] **Step 43:** Mark `Q_ext -> q` as measurement transformation.
- [ ] **Step 44:** Mark `q, xi, T -> V_n` as implicit charge-balance root.
- [ ] **Step 45:** Mark equilibrium `xi_eq(V_n,T)` as a special-state relation.
- [ ] **Step 46:** Mark equilibrium OCV as a result of the same root, not a primary input.
- [ ] **Step 47:** Mark non-equilibrium `xi_j(q)` as an unknown function governed by state evolution.
- [ ] **Step 48:** Mark self-consistency as an integral/fixed-point problem.
- [ ] **Step 49:** Mark derivative chain `F=0 -> dV_n/dq -> dQ_ext/dV`.
- [ ] **Step 50:** Mark apparent voltage transformation separately from internal potential.
- [ ] **Step 51:** Mark peak location as maximum slope of transition contribution, not arbitrary peak placement.
- [ ] **Step 52:** Mark peak area as integrated capacity contribution.
- [ ] **Step 53:** Mark peak width as transition sharpness plus dynamic broadening.
- [ ] **Step 54:** Mark all later fitting statements as outside Chapter 1 acceptance.
- [ ] **Step 55:** Write a required-equation list.
- [ ] **Step 56:** Write a forbidden-equation list.
- [ ] **Step 57:** Write a required-explanation list.
- [ ] **Step 58:** Write a naive-reader question list.
- [ ] **Step 59:** Write a failure taxonomy: undefined symbol, early use, hidden assumption, circular dependency, derivative jump, sign ambiguity, unsupported physical claim, implementation drift.
- [ ] **Step 60:** Define hard gate `G1` for definition-before-use.
- [ ] **Step 61:** Define hard gate `G2` for dependency acyclicity except explicit fixed point.
- [ ] **Step 62:** Define hard gate `G3` for derivative completeness.
- [ ] **Step 63:** Define hard gate `G4` for physical ICA interpretation.
- [ ] **Step 64:** Define hard gate `G5` for undergraduate continuity.
- [ ] **Step 65:** Define hard gate `G6` for implementation-scope exclusion.
- [ ] **Step 66:** Define hard gate `G7` for LaTeX/static body cleanliness.
- [ ] **Step 67:** Record equations that may use implicit-function theorem.
- [ ] **Step 68:** Record equations that may use Volterra/Picard fixed-point language.
- [ ] **Step 69:** Record that advanced theorem names must be explained plainly.
- [ ] **Step 70:** Record that no theorem may hide the concrete algebra.
- [ ] **Step 71:** Gate Phase 002 only if every planned section has a dependency owner.
- [ ] **Step 72:** Stop if `V_n` cannot be derived from charge balance.
- [ ] **Step 73:** Stop if ICA shape cannot be connected to derivative terms.
- [ ] **Step 74:** Stop if any required theorem would require external research not yet read.
- [ ] **Step 75:** Save Phase 002 result in the loop ledger.
- [ ] **Step 76:** Proceed directly to Phase 003 if no user decision is required.

Additional contract steps:

- [ ] **Step 77:** Choose manuscript section order.
- [ ] **Step 78:** Choose notation conventions that preserve existing source meanings.
- [ ] **Step 79:** Choose sign handling as explicit orientation variables where necessary.
- [ ] **Step 80:** Choose an equilibrium-transition generic model, not an over-specific fitted model.
- [ ] **Step 81:** Choose a generic sigmoid example only as an explanatory example.
- [ ] **Step 82:** Choose whether refs. 6/7 appear in body or only in notes.
- [ ] **Step 83:** Record citation caution.
- [ ] **Step 84:** Run dependency graph self-check.
- [ ] **Step 85:** Gate Phase 002 with `PASS_CH1_THEORY_CONTRACT`.

## Phase 003 — Chapter 1 Theory Manuscript Construction

- [ ] **Step 86:** Create `graphite_ica_chapter1_theory_complete.tex` from a blank target.
- [ ] **Step 87:** Add minimal LaTeX preamble.
- [ ] **Step 88:** Add title focused on graphite ICA theory.
- [ ] **Step 89:** Add abstract with no implementation claims.
- [ ] **Step 90:** Add section `What ICA Measures`.
- [ ] **Step 91:** Define external charge and normalized charge.
- [ ] **Step 92:** Define ICA/DVA observables at the measurement level.
- [ ] **Step 93:** Explain why peak fitting alone is not a derivation.
- [ ] **Step 94:** Add section `Storage Decomposition`.
- [ ] **Step 95:** Define background storage.
- [ ] **Step 96:** Define staging/transition storage.
- [ ] **Step 97:** Define transition state variables and bounds.
- [ ] **Step 98:** Add section `Charge Balance Before Voltage`.
- [ ] **Step 99:** Derive charge-balance residual.
- [ ] **Step 100:** Define root interval and nonzero slope condition.
- [ ] **Step 101:** Add plain-language implicit root explanation.
- [ ] **Step 102:** Define `V_n = Phi(q,xi,T)`.
- [ ] **Step 103:** Add section `Equilibrium As A Special Case`.
- [ ] **Step 104:** Define `xi_eq(V,T)`.
- [ ] **Step 105:** Substitute equilibrium states into charge balance.
- [ ] **Step 106:** Derive equilibrium OCV as the same root.
- [ ] **Step 107:** Add section `Why Feedback Is Not A Contradiction`.
- [ ] **Step 108:** Define dynamic state equation abstractly.
- [ ] **Step 109:** Convert time equation to charge-domain equation only when current is nonzero.
- [ ] **Step 110:** Substitute implicit potential into state equation.
- [ ] **Step 111:** Write integral/fixed-point form.
- [ ] **Step 112:** Explain fixed point in undergraduate terms.
- [ ] **Step 113:** Add section `Differentiating Charge Balance`.
- [ ] **Step 114:** Differentiate general charge balance step by step.
- [ ] **Step 115:** Solve for `dV_n/dq`.
- [ ] **Step 116:** Derive equilibrium derivative as a special case.
- [ ] **Step 117:** Add section `From Internal Potential To Measured Voltage`.
- [ ] **Step 118:** Define apparent voltage map with sign/offset terms.
- [ ] **Step 119:** Derive `dV_app/dq`.
- [ ] **Step 120:** Add section `ICA and DVA`.
- [ ] **Step 121:** Derive `dQ_ext/dV_app`.
- [ ] **Step 122:** Derive `dV_app/dQ_ext`.
- [ ] **Step 123:** Add section `Where Peaks Come From`.
- [ ] **Step 124:** Decompose ICA into background plus transition contributions.
- [ ] **Step 125:** Explain peak location.
- [ ] **Step 126:** Explain peak area.
- [ ] **Step 127:** Explain peak width.
- [ ] **Step 128:** Explain overlap of multiple transitions.
- [ ] **Step 129:** Add a generic sigmoid transition example.
- [ ] **Step 130:** Derive derivative of sigmoid example.
- [ ] **Step 131:** Interpret the example without claiming it is the only graphite model.
- [ ] **Step 132:** Add section `Non-equilibrium Distortion`.
- [ ] **Step 133:** Explain lag/broadening through `d xi/dq`.
- [ ] **Step 134:** Explain why peak area is conserved by transition capacity while tail length depends on the rate of state relaxation in the charge coordinate.
- [ ] **Step 135:** Explain why lower temperature can produce a longer tail through slower thermally activated relaxation.
- [ ] **Step 136:** Explain why higher temperature can produce a shorter tail through faster relaxation toward the equilibrium transition state.
- [ ] **Step 137:** Keep all implementation/fitting claims out.
- [ ] **Step 138:** Add section `Logical Checklist`.
- [ ] **Step 139:** State all dependencies in prose for reader audit.
- [ ] **Step 140:** Add bibliography only for actually used cautious citations.
- [ ] **Step 141:** Avoid `Phase`, `audit`, `loop`, `solver implementation`, and fitting-code language in body.
- [ ] **Step 142:** Save the manuscript.
- [ ] **Step 143:** Run label/reference scan.
- [ ] **Step 144:** Run brace balance scan.
- [ ] **Step 145:** Run forbidden-term scan.
- [ ] **Step 146:** Run section-order scan.
- [ ] **Step 147:** Record static results in ledger.
- [ ] **Step 148:** Gate Phase 003 only if manuscript exists and static scans pass.
- [ ] **Step 149:** Stop if the manuscript contains implementation instructions.
- [ ] **Step 150:** Stop if it claims data fitting.
- [ ] **Step 151:** Stop if it uses `V_n` before defining the root.
- [ ] **Step 152:** Stop if it derives `dQ/dV` before deriving `dV/dq`.
- [ ] **Step 153:** Save Phase 003 result in the loop ledger.
- [ ] **Step 154:** Proceed directly to Ralph Wiggum Round 1.
- [ ] **Step 155:** Record no source files modified.
- [ ] **Step 156:** Record no Claude files modified.
- [ ] **Step 157:** Record git status.
- [ ] **Step 158:** Gate Phase 003 with `PASS_CH1_THEORY_MANUSCRIPT_INITIAL`.

## Phase 004 — Ralph Wiggum Round 1, Naive Reader And Definition Gate

- [ ] **Step 156:** Read the full new manuscript from line 1 to end.
- [ ] **Step 157:** Ask naive-reader question for every symbol: "What is this, where did it come from, and why can it be used here?"
- [ ] **Step 158:** Build undefined-symbol list.
- [ ] **Step 159:** Build definition-after-use list.
- [ ] **Step 160:** Build unexplained-equation list.
- [ ] **Step 161:** Build hidden-assumption list.
- [ ] **Step 162:** Build reader-jump list.
- [ ] **Step 163:** Convert each confirmed issue into a repair item.
- [ ] **Step 164:** If no issue, record pass.
- [ ] **Step 165:** If issues exist, patch manuscript.
- [ ] **Step 166:** Re-run static scans.
- [ ] **Step 167:** Re-run naive-reader checks on patched lines.
- [ ] **Step 168:** Save `CHAPTER1_THEORY_RALPH_LOOP_ROUND_001_RESULT.md`.
- [ ] **Step 169:** Update loop ledger.
- [ ] **Step 170:** Repeat Round 1 locally until zero confirmed definition/reader issues or same error repeats 3 times.
- [ ] **Step 171:** Stop for user only if a symbol meaning cannot be inferred from source and no conservative definition is possible.
- [ ] **Step 172:** Gate with `PASS_RALPH_ROUND_001_DEFINITIONS`.

Additional Round 1 checks:

- [ ] **Step 173:** Confirm `q` is defined before ICA.
- [ ] **Step 174:** Confirm `Q_ext` is defined before `q`.
- [ ] **Step 175:** Confirm `xi_j` is defined before charge balance.
- [ ] **Step 176:** Confirm `Q_bg` is defined before charge balance.
- [ ] **Step 177:** Confirm `V_n` is introduced by residual/root only.
- [ ] **Step 178:** Confirm `V_app` is not collapsed into `V_n`.
- [ ] **Step 179:** Confirm transition capacity terms are defined.
- [ ] **Step 180:** Confirm derivative notation is defined.
- [ ] **Step 181:** Confirm sign/orientation convention is explicit.
- [ ] **Step 182:** Confirm equilibrium state is not used before dynamic state.
- [ ] **Step 183:** Confirm later examples do not redefine core variables.
- [ ] **Step 184:** Confirm no fitting parameters are treated as fitted results.
- [ ] **Step 185:** Confirm no code/solver action is requested.
- [ ] **Step 186:** Confirm bibliography entries are cited only if used.
- [ ] **Step 187:** Confirm all section intros tell the reader why the section exists.
- [ ] **Step 188:** Confirm no old version-history language remains.
- [ ] **Step 189:** Confirm every equation has a preceding sentence.
- [ ] **Step 190:** Confirm every equation has a following interpretation.
- [ ] **Step 191:** Confirm no theorem name appears without plain explanation.
- [ ] **Step 192:** Confirm no unsupported claim of novelty appears.
- [ ] **Step 193:** Confirm no patent/paper claim is asserted.
- [ ] **Step 194:** Confirm no original source is modified.
- [ ] **Step 195:** Confirm no Claude workspace is modified.
- [ ] **Step 196:** Record all repairs in the result file.
- [ ] **Step 197:** Record all rejected findings in the result file.
- [ ] **Step 198:** Record remaining limitations.
- [ ] **Step 199:** Record next round entry condition.
- [ ] **Step 200:** Update ledger.
- [ ] **Step 201:** Run git status.
- [ ] **Step 202:** Preserve loop state on disk.
- [ ] **Step 203:** Proceed to Round 2.
- [ ] **Step 204:** Do not ask user at phase boundary.
- [ ] **Step 205:** Gate Phase 004 with `PASS_RALPH_ROUND_001_DEFINITIONS`.

## Phase 005 — Ralph Wiggum Round 2, Mathematical Dependency Gate

- [ ] **Step 206:** Read the full manuscript after Round 1 repairs.
- [ ] **Step 207:** Check charge-balance algebra line by line.
- [ ] **Step 208:** Check implicit root conditions.
- [ ] **Step 209:** Check equilibrium special-case derivation.
- [ ] **Step 210:** Check time-to-charge conversion.
- [ ] **Step 211:** Check fixed-point/integral form.
- [ ] **Step 212:** Check derivative of charge balance.
- [ ] **Step 213:** Check solution for `dV_n/dq`.
- [ ] **Step 214:** Check equilibrium derivative reduction.
- [ ] **Step 215:** Check `V_app` derivative.
- [ ] **Step 216:** Check ICA reciprocal relation.
- [ ] **Step 217:** Check DVA reciprocal relation.
- [ ] **Step 218:** Check units/dimensions.
- [ ] **Step 219:** Check sign conventions.
- [ ] **Step 220:** Check denominator/singularity warnings.
- [ ] **Step 221:** Convert each confirmed issue into a repair item.
- [ ] **Step 222:** If issues exist, patch manuscript.
- [ ] **Step 223:** Re-run algebra scans.
- [ ] **Step 224:** Save `CHAPTER1_THEORY_RALPH_LOOP_ROUND_002_RESULT.md`.
- [ ] **Step 225:** Update loop ledger.
- [ ] **Step 226:** Repeat Round 2 locally until zero confirmed mathematical issues or same error repeats 3 times.
- [ ] **Step 227:** Gate with `PASS_RALPH_ROUND_002_MATH`.
- [ ] **Step 228:** Stop for user only if a physical sign convention cannot be chosen without user preference.
- [ ] **Step 229:** If sign convention is arbitrary but harmless, keep orientation factors explicit.
- [ ] **Step 230:** Confirm no external theorem hides algebra.
- [ ] **Step 231:** Confirm no dimensioned quantity is added to dimensionless quantity.
- [ ] **Step 232:** Confirm derivatives with respect to `q`, `Q_ext`, `V_n`, and `V_app` are not mixed.
- [ ] **Step 233:** Confirm dynamic and equilibrium derivatives are separated.
- [ ] **Step 234:** Confirm rest condition is separated from charge-domain derivative.
- [ ] **Step 235:** Confirm no ref. 6/7 physical assumption enters equations.
- [ ] **Step 236:** Confirm the fixed-point form is theoretical, not implementation.
- [ ] **Step 237:** Confirm the manuscript can be read without a solver trace.
- [ ] **Step 238:** Confirm no data is needed for derivation.
- [ ] **Step 239:** Confirm peak area equation follows from an integral.
- [ ] **Step 240:** Confirm peak width explanation follows from transition derivative width.
- [ ] **Step 241:** Confirm peak position explanation follows from slope maximum.
- [ ] **Step 242:** Confirm background contribution is not visual baseline only.
- [ ] **Step 243:** Confirm apparent voltage relation has its derivative term.
- [ ] **Step 244:** Confirm state bounds appear where needed.
- [ ] **Step 245:** Confirm the manuscript does not overclaim uniqueness beyond stated assumptions.
- [ ] **Step 246:** Record all repairs.
- [ ] **Step 247:** Record all residual limitations.
- [ ] **Step 248:** Record commands run.
- [ ] **Step 249:** Run static scans.
- [ ] **Step 250:** Run git status.
- [ ] **Step 251:** Preserve loop state on disk.
- [ ] **Step 252:** Proceed to Round 3.
- [ ] **Step 253:** Do not ask user at phase boundary.
- [ ] **Step 254:** Gate Phase 005 with `PASS_RALPH_ROUND_002_MATH`.

Reserve steps 255-260 for same-round repairs if needed.

## Phase 006 — Ralph Wiggum Round 3, Physical Interpretation Gate

- [ ] **Step 261:** Read the full manuscript after Round 2 repairs.
- [ ] **Step 262:** Check whether ICA peak origin is explained without assuming peaks.
- [ ] **Step 263:** Check peak location interpretation.
- [ ] **Step 264:** Check peak area interpretation.
- [ ] **Step 265:** Check peak width interpretation.
- [ ] **Step 266:** Check overlapping-transition interpretation.
- [ ] **Step 267:** Check non-equilibrium distortion language.
- [ ] **Step 267a:** Check that low-temperature long-tail and high-temperature short-tail observations are explained without claiming fitted results.
- [ ] **Step 267b:** Check that transition peak area conservation is derived from integrated state change.
- [ ] **Step 268:** Check graphite-specific claims are supported or stated generically.
- [ ] **Step 269:** Check refs. 6/7 are not physically overimported.
- [ ] **Step 270:** Check no fitted-result claim appears.
- [ ] **Step 271:** Check no patent/novelty claim appears.
- [ ] **Step 272:** Convert confirmed issues into repair items.
- [ ] **Step 273:** If issues exist, patch manuscript.
- [ ] **Step 274:** Re-run physical-claim scans.
- [ ] **Step 275:** Save `CHAPTER1_THEORY_RALPH_LOOP_ROUND_003_RESULT.md`.
- [ ] **Step 276:** Update loop ledger.
- [ ] **Step 277:** Repeat Round 3 locally until zero confirmed physical interpretation issues or same error repeats 3 times.
- [ ] **Step 278:** Gate with `PASS_RALPH_ROUND_003_PHYSICS`.
- [ ] **Step 279:** Stop for user only if a stronger graphite physical claim requires evidence not present.
- [ ] **Step 280:** Otherwise weaken claims conservatively.
- [ ] **Step 281:** Confirm all strong claims have a derivation or are removed.
- [ ] **Step 282:** Confirm examples are labeled examples.
- [ ] **Step 283:** Confirm generic transition model is not presented as fitted truth.
- [ ] **Step 284:** Confirm DVA is linked to ICA reciprocal safely.
- [ ] **Step 285:** Confirm denominator near-zero caveat is visible.
- [ ] **Step 286:** Confirm finite resolution / smoothing is not overdiscussed.
- [ ] **Step 287:** Confirm no Chapter 2-5 scope creep.
- [ ] **Step 288:** Confirm no solver/fitting task appears in body.
- [ ] **Step 289:** Record repairs.
- [ ] **Step 290:** Record rejected findings.
- [ ] **Step 291:** Record residual limitations.
- [ ] **Step 292:** Run static scans.
- [ ] **Step 293:** Run git status.
- [ ] **Step 294:** Preserve loop state.
- [ ] **Step 295:** Proceed to Round 4.
- [ ] **Step 296:** Do not ask user at phase boundary.
- [ ] **Step 297:** Gate Phase 006 with `PASS_RALPH_ROUND_003_PHYSICS`.

Reserve steps 298-315 for same-round repairs if needed.

## Phase 007 — Ralph Wiggum Round 4, Undergraduate Continuity Gate

- [ ] **Step 316:** Read the full manuscript after Round 3 repairs.
- [ ] **Step 317:** Test every section with the question: "Can a reader follow this without already knowing the answer?"
- [ ] **Step 318:** Check whether every equation is motivated.
- [ ] **Step 319:** Check whether every equation is interpreted.
- [ ] **Step 320:** Check whether every transformation has an intermediate step.
- [ ] **Step 321:** Check whether advanced theorem language is explained plainly.
- [ ] **Step 322:** Check whether symbols are overloaded.
- [ ] **Step 323:** Check whether prose accidentally skips from thermodynamics to ICA shape.
- [ ] **Step 324:** Check whether the final logical checklist matches the actual body.
- [ ] **Step 325:** Convert confirmed continuity issues into repair items.
- [ ] **Step 326:** If issues exist, patch manuscript.
- [ ] **Step 327:** Re-read repaired sections.
- [ ] **Step 328:** Save `CHAPTER1_THEORY_RALPH_LOOP_ROUND_004_RESULT.md`.
- [ ] **Step 329:** Update loop ledger.
- [ ] **Step 330:** Repeat Round 4 locally until zero confirmed undergraduate-continuity issues or same error repeats 3 times.
- [ ] **Step 331:** Gate with `PASS_RALPH_ROUND_004_UNDERGRAD_CONTINUITY`.
- [ ] **Step 332:** Stop for user only if the target audience must be redefined.
- [ ] **Step 333:** Confirm title and abstract match scope.
- [ ] **Step 334:** Confirm no implementation terms dominate.
- [ ] **Step 335:** Confirm final document is Chapter 1 only.
- [ ] **Step 336:** Confirm no future-work section implies current incompleteness of theory.
- [ ] **Step 337:** Confirm limitations only cover evidence boundaries, not missing derivation.
- [ ] **Step 338:** Confirm definitions are concise but complete.
- [ ] **Step 339:** Confirm all variables in the logical checklist appear earlier.
- [ ] **Step 340:** Confirm every displayed equation has a label if referenced.
- [ ] **Step 341:** Confirm all labels are unique.
- [ ] **Step 342:** Run label/reference scan.
- [ ] **Step 343:** Run brace balance scan.
- [ ] **Step 344:** Run forbidden-term scan.
- [ ] **Step 345:** Run body-scope scan.
- [ ] **Step 346:** Run git status.
- [ ] **Step 347:** Preserve loop state.
- [ ] **Step 348:** Proceed to convergence phase.
- [ ] **Step 349:** Do not ask user at phase boundary.
- [ ] **Step 350:** Gate Phase 007 with `PASS_RALPH_ROUND_004_UNDERGRAD_CONTINUITY`.

Reserve steps 351-370 for same-round repairs if needed.

## Phase 008 — Ralph Wiggum Convergence And Handover

- [ ] **Step 371:** Re-read loop ledger.
- [ ] **Step 372:** Confirm no round has unresolved confirmed issues.
- [ ] **Step 373:** Confirm no repeated error hit escalation threshold.
- [ ] **Step 374:** Re-run full static checks.
- [ ] **Step 375:** Re-run dependency-owner check.
- [ ] **Step 376:** Re-run forbidden implementation-scope scan.
- [ ] **Step 377:** Re-run source-modification boundary check.
- [ ] **Step 378:** Re-run Claude-boundary check.
- [ ] **Step 379:** Create `CHAPTER1_THEORY_FINAL_HANDOVER.md`.
- [ ] **Step 380:** Add final artifact list.
- [ ] **Step 381:** Add final logic-gate table.
- [ ] **Step 382:** Add final remaining limitations.
- [ ] **Step 383:** Add exact non-goals preserved.
- [ ] **Step 384:** Add recommended next actions only within theory/polish/PDF build scope.
- [ ] **Step 385:** Update `REBUILD_V2_EXECUTION_LEDGER.md`.
- [ ] **Step 386:** Gate with `PASS_CH1_THEORY_RALPH_CONVERGED` only if all loop rounds pass.
- [ ] **Step 387:** If any confirmed issue remains, do not claim completion; start next loop round if below max 10.
- [ ] **Step 388:** If same issue repeats 3 times, stop for user with exact issue and options.
- [ ] **Step 389:** If external evidence is required, mark `미검증` and weaken/remove claim.
- [ ] **Step 390:** If no issues remain, prepare final user-facing summary.
- [ ] **Step 391:** Include exact paths to new manuscript, loop ledger, and handover.
- [ ] **Step 392:** Include exact verification status.
- [ ] **Step 393:** Include exact build status if checked.
- [ ] **Step 394:** Do not commit unless user asks.
- [ ] **Step 395:** Preserve all validation commands and outputs.
- [ ] **Step 396:** Close loop at user review boundary.

Reserve steps 397-425 for additional loop rounds if the first four rounds do not converge.

## Implementation Interfaces

### Loop Ledger Row

```markdown
| Round | Gate | Failures | Repair | Status | Evidence |
|---:|---|---|---|---|---|
| 1 | definition/naive-reader | ... | ... | PASS/FAIL | file/line refs |
```

### Theory Dependency Graph Row

```markdown
| Object | Depends On | Defined In | Used For | Failure If Missing |
|---|---|---|---|---|
| `V_n` | `q`, `xi`, `T`, charge-balance residual | root section | ICA derivative chain | circular voltage input |
```

### Ralph Failure Record

```markdown
| Issue ID | Gate | Location | Failure Message | Repair Rule | Status |
|---|---|---:|---|---|---|
| R1-001 | G1 | line ... | symbol used before definition | define or reorder before use | fixed |
```

## Test Plan

Static checks:

- target `.tex` exists;
- line count recorded;
- label/reference scan has zero missing internal references;
- brace count is balanced;
- forbidden terms absent from body: `solver implementation`, `fitting code`, `completed fit`, `parameter values`, `Phase`, `audit`, `Ralph`, `loop`;
- `V_n` first appears only after root-introduction context;
- `dQ/dV` expressions appear only after `dV/dq` derivation;
- no original source file modified;
- no Claude file modified.

Logic checks:

- definition-before-use;
- dependency-owner table complete;
- charge-balance residual precedes internal potential;
- equilibrium OCV derived as special root;
- self-consistency explained as fixed-point/integral equation;
- derivative chain includes all intermediate steps;
- ICA peak location, area, and width are derived from derivative terms;
- low-temperature long-tail and high-temperature short-tail behavior is explained through temperature-dependent relaxation in the charge coordinate;
- peak area conservation is separated from peak/tail shape change;
- implementation/fitting scope excluded.

## Assumptions

- The user wants a new Chapter 1 theory-complete artifact, not another scaffold.
- The current target audience is a university undergraduate reader with calculus, basic thermodynamics, and basic electrochemistry exposure.
- If a stronger paper/patent claim requires additional evidence, the claim is weakened or removed rather than asserted.
- PDF build is optional and not required for logical convergence.
- Full refs. 6/7 original paper reading is not required if the body does not make strong derivation claims from those papers.
- The observed long-tail/short-tail temperature trend is treated as a physical phenomenon to explain theoretically, not as a completed fit result.

## Correction History

- 2026-05-28: Created after user clarified that solver/fitting implementation is outside current scope and that the priority is a fully verified theoretical Chapter 1 derivation.
