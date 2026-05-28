# Graphite ICA/DVA From-Scratch Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Use subagents only for independent read-only review ranges, and record their exact read coverage before accepting their results.

**Goal:** Create a new graphite-anode ICA/DVA manuscript from a blank structure, using the existing ver1/ver5/PDF materials only as evidence and not as text to patch.

**Architecture:** The rebuild separates source evidence, mathematical foundation, manuscript architecture, exact self-consistent formulation, approximate closure method, fitting/validation protocol, and final LaTeX drafting. The new manuscript treats Chapter 1 as the thermodynamic charge-balance foundation and treats Chapters 2-5 as downstream interfaces unless explicitly expanded in later phases.

**Tech Stack:** LaTeX (`kotex`, `amsmath`, `mathtools`, `booktabs`, `hyperref`), Markdown phase records, PowerShell source validation, bundled Python `pypdf` for PDF text extraction, optional LaTeX engine if available.

---

## Summary

This plan supersedes the previous development-draft direction for manuscript writing. The previous artifacts remain useful as evidence, but the new manuscript must not be edited from the existing draft. It must be written from a blank file with a fresh structure.

Primary output:

```text
D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_rebuilt_manuscript_v1.tex
```

Supporting outputs:

```text
D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_001_SOURCE_EVIDENCE_INDEX.md
D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_002_MANUSCRIPT_ARCHITECTURE_RESULT.md
D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_003_MATH_FOUNDATION_RESULT.md
D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_004_CLOSURE_METHOD_RESULT.md
D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_005_FITTING_VALIDATION_RESULT.md
D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_006_DRAFT_RESULT.md
D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_007_VALIDATION_HANDOVER.md
D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_EXECUTION_LEDGER.md
```

## Current Ground Truth

Confirmed:

- `graphite_ica_dynamic_ver5.tex` is a historical merged document whose ver1-ver5 layers should become Chapter 1-5.
- `graphite_ica_charge_balance_ver1_rechecked2.tex` contains the corrected Chapter 1 foundation.
- The central equation is:

```text
Q_cell q = Q_bg(V_n,T) + sum_j Q_j,tot xi_j
```

- `V_n` is solved from charge balance.
- `V_OCV(q,T)` is the equilibrium charge-balance root, not a primary input curve.
- The self-consistency loop is a DAE/Volterra-type problem, not a fatal contradiction.
- refs. 6/7 contribute a mathematical closure pattern, not graphite physical assumptions.

Open:

- exact visual verification of PDF equations;
- full original refs. 6/7 papers;
- LaTeX build;
- direct numerical solver;
- final choice of document language and scope.

## Phase Range

| Phase | Step Range | Name | Gate |
|---:|---:|---|---|
| 001 | 1-12 | Source Evidence Index | `PASS_REBUILD_SOURCE_INDEX` |
| 002 | 13-27 | Blank Manuscript Architecture | `PASS_REBUILD_ARCHITECTURE` |
| 003 | 28-48 | Mathematical Foundation | `PASS_REBUILD_MATH_FOUNDATION` |
| 004 | 49-66 | Ref. 6/7 Closure Method | `PASS_REBUILD_CLOSURE_METHOD` |
| 005 | 67-86 | Fitting And Validation Protocol | `PASS_REBUILD_FIT_VALIDATION` |
| 006 | 87-112 | New LaTeX Manuscript Draft | `PASS_REBUILD_DRAFT` |
| 007 | 113-132 | Validation, Review, Handover | `PASS_REBUILD_HANDOVER` |

## Non-Goals

- Do not overwrite original `.tex` files in the source download folder.
- Do not edit `D:\Projects\Project_Anode_Fit\Claude`.
- Do not patch `graphite_ica_chapter1_development_draft.tex`.
- Do not import geminate-pair recombination physics into graphite.
- Do not claim a full numerical fitting method has been validated unless a direct solver has been implemented and run.
- Do not put phase labels, audit notes, or change history into the manuscript body.

## Implementation Changes

Create:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_rebuilt_manuscript_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_EXECUTION_LEDGER.md`
- phase result files listed in the Summary.

Read-only references:

- `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_dynamic_ver5.tex`
- `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_charge_balance_ver1_rechecked2.tex`
- `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\JCP_147(14)_144111_(2017) - Effects of external electric field.pdf`
- all prior Codex result files in `D:\Projects\Project_Anode_Fit\Codex\results`.

## Phase 001 - Source Evidence Index

**Purpose:** Create a clean evidence index so the rewrite does not depend on memory or copied old prose.

**Files:**

- Create: `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_001_SOURCE_EVIDENCE_INDEX.md`
- Create/update: `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_EXECUTION_LEDGER.md`

Steps:

- [ ] **Step 1:** Confirm the active project and Codex workspace boundaries.
  Expected: active project is `D:\Projects\Project_Anode_Fit`; output files are under `Codex\results`.

- [ ] **Step 2:** Re-open the previous ledger and handover.
  Files:
  `PHASE_001_007_EXECUTION_LEDGER.md`,
  `PHASE_007_ANODE_DQDV_HANDOVER.md`.

- [ ] **Step 3:** Build an evidence table with source, exact read coverage, and current confidence.

- [ ] **Step 4:** Re-check existence and metadata of the two `.tex` files and the PDF.

- [ ] **Step 5:** Record that existing drafts are reference-only, not rewrite bases.

- [ ] **Step 6:** Extract a compact list of equations that can be reused as mathematical ideas.

- [ ] **Step 7:** Extract a compact list of statements that must not be reused.

- [ ] **Step 8:** Mark all unverified items as `미검증`, not as assumptions.

- [ ] **Step 9:** Create `REBUILD_PHASE_001_SOURCE_EVIDENCE_INDEX.md`.

- [ ] **Step 10:** Create or update `REBUILD_EXECUTION_LEDGER.md`.

- [ ] **Step 11:** Gate check: every source claim has an evidence pointer.

- [ ] **Step 12:** Proceed only if the source index distinguishes `확정`, `추정`, `미검증`, and `근거 미발견`.

Gate: `PASS_REBUILD_SOURCE_INDEX`.

## Phase 002 - Blank Manuscript Architecture

**Purpose:** Decide the new manuscript structure before writing any body text.

**Files:**

- Create: `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_002_MANUSCRIPT_ARCHITECTURE_RESULT.md`

Steps:

- [ ] **Step 13:** Decide scope option:
  `Chapter 1 only`, `Chapter 1 filled + Chapter 2-5 skeleton`, or `full Chapter 1-5 manuscript`.

- [ ] **Step 14:** Decide language option:
  Korean, English, or Korean explanatory body with English mathematical notation.

- [ ] **Step 15:** Define the target reader:
  battery modeler, electrochemist, fitting-algorithm developer, or internal research note reader.

- [ ] **Step 16:** Draft the table of contents from scratch without copying old section order.

- [ ] **Step 17:** Assign each chapter one owner concept.

- [ ] **Step 18:** Define what belongs in Chapter 1 and what is interface-only.

- [ ] **Step 19:** Define what belongs in Chapter 2 heat layer.

- [ ] **Step 20:** Define what belongs in Chapter 3 kinetic interface.

- [ ] **Step 21:** Define what belongs in Chapter 4 fitting system.

- [ ] **Step 22:** Define what belongs in Chapter 5 hysteresis/memory.

- [ ] **Step 23:** Write a "do not include in body" list for version history and audit notes.

- [ ] **Step 24:** Define notation conventions before drafting.

- [ ] **Step 25:** Create `REBUILD_PHASE_002_MANUSCRIPT_ARCHITECTURE_RESULT.md`.

- [ ] **Step 26:** Update `REBUILD_EXECUTION_LEDGER.md`.

- [ ] **Step 27:** Gate check: the architecture can be read without knowing old ver1-ver5 history.

Gate: `PASS_REBUILD_ARCHITECTURE`.

## Phase 003 - Mathematical Foundation

**Purpose:** Write the exact mathematical backbone before any approximation or fitting story.

**Files:**

- Create: `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_003_MATH_FOUNDATION_RESULT.md`

Steps:

- [ ] **Step 28:** Define measured coordinate `Q_ext`, `Q_cell`, `q`, `I`, `T`.

- [ ] **Step 29:** Define state vector `xi`.

- [ ] **Step 30:** Define equilibrium occupancy `xi_eq(V,T)` using a dummy voltage argument.

- [ ] **Step 31:** Define `Q_bg(V,T)` as a storage term.

- [ ] **Step 32:** Define charge-balance residual `G(V;q,T,xi)`.

- [ ] **Step 33:** Define root operator `V_n = mathcal V(q,T,xi;theta)`.

- [ ] **Step 34:** Define existence, bracket, and slope-floor conditions.

- [ ] **Step 35:** Define equilibrium OCV as a special root.

- [ ] **Step 36:** Define apparent voltage `V_app`.

- [ ] **Step 37:** Define driving voltage `V_drive`.

- [ ] **Step 38:** Define kinetic rate interface without overcommitting to full BV.

- [ ] **Step 39:** Define time-domain `dxi/dt`.

- [ ] **Step 40:** Define q-domain `dxi/dq` only for nonzero current.

- [ ] **Step 41:** Write Volterra integral form.

- [ ] **Step 42:** Derive `dV_n/dq`.

- [ ] **Step 43:** Derive `dV_app/dq`.

- [ ] **Step 44:** Derive ICA/DVA observables from `Q_ext`.

- [ ] **Step 45:** Define rest relaxation.

- [ ] **Step 46:** Create `REBUILD_PHASE_003_MATH_FOUNDATION_RESULT.md`.

- [ ] **Step 47:** Update `REBUILD_EXECUTION_LEDGER.md`.

- [ ] **Step 48:** Gate check: no downstream variable appears before it is defined or solved.

Gate: `PASS_REBUILD_MATH_FOUNDATION`.

## Phase 004 - Ref. 6/7 Closure Method

**Purpose:** Add the self-consistency solution method carefully, without physical over-import.

**Files:**

- Create: `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_004_CLOSURE_METHOD_RESULT.md`

Steps:

- [ ] **Step 49:** Re-open `ref6_ref7_method_notes.md`.

- [ ] **Step 50:** Decide whether full refs. 6/7 PDFs are required before manuscript drafting.

- [ ] **Step 51:** If not required, state the limitation explicitly in the result file.

- [ ] **Step 52:** Define exact direct solver as the primary truth model.

- [ ] **Step 53:** Define quasi-equilibrium reference path.

- [ ] **Step 54:** Define optional frozen-feedback reference path.

- [ ] **Step 55:** Define correction functional `C_j`.

- [ ] **Step 56:** Define admissibility conditions for `C_j`.

- [ ] **Step 57:** Define how closure error is measured against direct solve.

- [ ] **Step 58:** Define low-rate limit check.

- [ ] **Step 59:** Define high-rate rejection condition.

- [ ] **Step 60:** Define how refs. 6/7 are cited in the manuscript.

- [ ] **Step 61:** List non-portable assumptions from the source paper.

- [ ] **Step 62:** Create a manuscript-ready subsection outline for closure.

- [ ] **Step 63:** Create `REBUILD_PHASE_004_CLOSURE_METHOD_RESULT.md`.

- [ ] **Step 64:** Update `REBUILD_EXECUTION_LEDGER.md`.

- [ ] **Step 65:** Gate check: closure is not presented as exact unless directly solved.

- [ ] **Step 66:** Proceed only if the closure section preserves the DAE/Volterra primary formulation.

Gate: `PASS_REBUILD_CLOSURE_METHOD`.

## Phase 005 - Fitting And Validation Protocol

**Purpose:** Design how the new document will support actual fitting without hiding parameter degeneracy.

**Files:**

- Create: `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_005_FITTING_VALIDATION_RESULT.md`

Steps:

- [ ] **Step 67:** Define staged fitting order.

- [ ] **Step 68:** Stage 1: thermodynamic low-rate baseline.

- [ ] **Step 69:** Stage 2: charge-balance residual and capacity closure.

- [ ] **Step 70:** Stage 3: kinetic lag.

- [ ] **Step 71:** Stage 4: thermal correction.

- [ ] **Step 72:** Stage 5: hysteresis/memory only after residual evidence.

- [ ] **Step 73:** Define parameter groups.

- [ ] **Step 74:** Define fixed/regularized/free parameter policy.

- [ ] **Step 75:** Define identifiability risks.

- [ ] **Step 76:** Define residual metrics.

- [ ] **Step 77:** Define ICA/DVA validation observables.

- [ ] **Step 78:** Define monotonicity and state-bound constraints.

- [ ] **Step 79:** Define root-conditioning checks.

- [ ] **Step 80:** Define reporting table for fit results.

- [ ] **Step 81:** Define failure modes and rejection rules.

- [ ] **Step 82:** Create manuscript-ready fitting protocol outline.

- [ ] **Step 83:** Create `REBUILD_PHASE_005_FITTING_VALIDATION_RESULT.md`.

- [ ] **Step 84:** Update `REBUILD_EXECUTION_LEDGER.md`.

- [ ] **Step 85:** Gate check: every fitted quantity has a validation observable or is explicitly deferred.

- [ ] **Step 86:** Proceed only if `R_n`, `k_j`, `Q_bg`, `Q_j,tot`, `U_j`, and `w_j` degeneracies are addressed.

Gate: `PASS_REBUILD_FIT_VALIDATION`.

## Phase 006 - New LaTeX Manuscript Draft

**Purpose:** Write the new manuscript from a blank LaTeX file.

**Files:**

- Create: `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_rebuilt_manuscript_v1.tex`
- Create: `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_006_DRAFT_RESULT.md`

Steps:

- [ ] **Step 87:** Create a new LaTeX file from scratch.

- [ ] **Step 88:** Add preamble and notation commands.

- [ ] **Step 89:** Add title and abstract/summary.

- [ ] **Step 90:** Add introduction/problem statement.

- [ ] **Step 91:** Add measured coordinate section.

- [ ] **Step 92:** Add graphite transition state section.

- [ ] **Step 93:** Add charge-balance root section.

- [ ] **Step 94:** Add equilibrium OCV section.

- [ ] **Step 95:** Add self-consistent DAE/Volterra section.

- [ ] **Step 96:** Add refs. 6/7 closure section.

- [ ] **Step 97:** Add ICA/DVA observable section.

- [ ] **Step 98:** Add fitting protocol section.

- [ ] **Step 99:** Add Chapter 2-5 interface section or chapter skeleton according to Phase 002 decision.

- [ ] **Step 100:** Add validation and limitations section.

- [ ] **Step 101:** Add bibliography entries with verified DOI data only.

- [ ] **Step 102:** Scan the body for phase/audit/change-history wording.

- [ ] **Step 103:** Scan notation for `V_n`, `V_app`, `V_drive`, `Q_ext`, `Q_bg`, `w_j`, `a_j`.

- [ ] **Step 104:** Check equation labels and references.

- [ ] **Step 105:** Check brace balance.

- [ ] **Step 106:** If a LaTeX engine is available, build the PDF.

- [ ] **Step 107:** If no LaTeX engine is available, record build limitation and run targeted syntax checks.

- [ ] **Step 108:** Compare draft against Phase 002 architecture.

- [ ] **Step 109:** Compare draft against Phase 003 mathematical foundation.

- [ ] **Step 110:** Create `REBUILD_PHASE_006_DRAFT_RESULT.md`.

- [ ] **Step 111:** Update `REBUILD_EXECUTION_LEDGER.md`.

- [ ] **Step 112:** Gate check: the new manuscript is not a patched copy of the prior draft.

Gate: `PASS_REBUILD_DRAFT`.

## Phase 007 - Validation, Review, Handover

**Purpose:** Close the rebuild loop with explicit evidence, open issues, and next decisions.

**Files:**

- Create: `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_PHASE_007_VALIDATION_HANDOVER.md`
- Update: `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_EXECUTION_LEDGER.md`

Steps:

- [ ] **Step 113:** Validate source coverage table.

- [ ] **Step 114:** Validate manuscript does not overwrite source files.

- [ ] **Step 115:** Validate no old draft body was copied wholesale.

- [ ] **Step 116:** Validate mathematical dependency order.

- [ ] **Step 117:** Validate closure method caution.

- [ ] **Step 118:** Validate fitting/identifiability gates.

- [ ] **Step 119:** Validate citations and DOI entries.

- [ ] **Step 120:** Validate LaTeX build result or build limitation.

- [ ] **Step 121:** List confirmed decisions.

- [ ] **Step 122:** List open issues.

- [ ] **Step 123:** List `근거 미발견`.

- [ ] **Step 124:** List files read and exact ranges.

- [ ] **Step 125:** List files created.

- [ ] **Step 126:** Create handover chain.

- [ ] **Step 127:** Create `REBUILD_PHASE_007_VALIDATION_HANDOVER.md`.

- [ ] **Step 128:** Update `REBUILD_EXECUTION_LEDGER.md`.

- [ ] **Step 129:** Run final `git status`.

- [ ] **Step 130:** Prepare user-facing summary.

- [ ] **Step 131:** Gate check: every phase result exists.

- [ ] **Step 132:** Stop for user review before any merge into source/manuscript master.

Gate: `PASS_REBUILD_HANDOVER`.

## Test Plan

Document-level checks:

- source coverage table exists and distinguishes `READ_FULL`, `READ_FULL_TEXT`, `부분 검독`, `미검독`;
- equation dependency order has no variable used before definition/solve;
- all citations have verified DOI or are marked unverified;
- no phase/audit/change-history text appears in the LaTeX body;
- no original source file is modified;
- no Claude folder file is modified.

LaTeX checks:

- `where.exe pdflatex`, `where.exe xelatex`, `where.exe lualatex`;
- if available, compile with the chosen engine;
- if unavailable, run label/ref scan, brace balance scan, and forbidden-body-word scan.

Scientific checks:

- `V_n` is always a solved variable;
- `V_OCV` is derived only as equilibrium special case;
- `Q_ext=Q_cell q` remains the ICA/DVA axis;
- `R_n` and `k_j` co-fit risk is explicitly constrained;
- closure approximation is validated or clearly labeled as approximation.

## Assumptions

- The source `.tex` files and the 2017 PDF remain the authoritative local sources.
- The new manuscript will be stored under `Codex\results` until the user asks to promote or merge it elsewhere.
- The user may later decide whether the manuscript is Korean, English, or mixed; if not specified before execution, default to Korean explanatory text with standard mathematical notation.
- Full original refs. 6/7 papers are not required unless the closure derivation needs more detail than the 2017 paper's own explanation.

## Correction History

- 2026-05-27: Created because user clarified that the next manuscript should be rebuilt from scratch, not repaired from the existing draft.
