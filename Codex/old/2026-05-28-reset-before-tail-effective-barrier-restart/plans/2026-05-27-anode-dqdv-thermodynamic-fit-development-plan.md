# Anode dQdV Thermodynamic Fit Development Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Also apply `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md` and `D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md`.

**Goal:** Develop the current Chapter 1 / ver.1 charge-balance argument into the Chapter 1-5 structure inferred from the ver.5 master draft, and resolve the self-consistent feedback-loop problem using the user's JCP 147(14) 144111 (2017) paper and its refs. 6, 7.

**Architecture:** Treat all source files as read-only evidence. Build a phase ledger, full read-coverage records, structure maps, equation/dependency graphs, ref. 6/7 method extraction, variable mapping, and only then produce a rewritten Chapter 1 development draft plus Chapter 1-5 integration specification under `Codex\results`.

**Tech Stack:** Markdown phase records, LaTeX source inspection, PDF/text/OCR inspection as needed, PowerShell file inventory, optional Python only when shell tools cannot inspect PDF/page/text structure, LaTeX syntax/build checks when a standalone draft exists.

---

## Summary

This plan covers the first full execution path for the graphite anode ICA(dQ/dV) / DVA(dV/dQ) fitting-method document.

The user's initial target is not a simple edit. The task is to:

- infer the intended structure of the merged `ver.1`-`ver.5` material inside `graphite_ica_dynamic_ver5.tex`;
- reinterpret that historical `ver.1`-`ver.5` layering as Chapter 1-5;
- use `graphite_ica_charge_balance_ver1_rechecked2.tex` as the current corrected Chapter 1 starting point;
- find and classify the current logical issue where a variable is fed back into itself;
- use the user's JCP 147(14) 144111 (2017) paper, especially refs. 6 and 7, to import a valid self-consistent integral-equation solution method;
- develop a mathematically and physically defensible plan for thermodynamic shape construction and fitting of LIB graphite dQ/dV.

This plan is written before full source reading. Any item not directly verified in this planning pass is marked as `미검증` or `근거 미발견` rather than filled by inference.

## Current Ground Truth

### Confirmed From User Instruction

- Active working project: `D:\Projects\Project_Anode_Fit`.
- Codex work area: `D:\Projects\Project_Anode_Fit\Codex`.
- Plans are stored in `D:\Projects\Project_Anode_Fit\Codex\plans`.
- Results, phase reports, ledgers, audits, and handovers are stored in `D:\Projects\Project_Anode_Fit\Codex\results`.
- Claude is working in parallel. Codex must not modify `D:\Projects\Project_Anode_Fit\Claude` unless the user explicitly instructs it.
- The original source folder named by the user is:
  `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001`
- The user described two `.tex` files and one paper PDF as the essential sources.
- The user stated that `graphite_ica_dynamic_ver5.tex` is the broad direction, but its internal `ver.1`-`ver.5` labels should likely become chapters.
- The user stated that `graphite_ica_charge_balance_ver1_rechecked2.tex` is the restart/correction file and contains the current logical development for Chapter 1.
- The user stated that a specific feedback/self-consistency problem remains in `ver1`.
- The user stated that the user's own JCP 147(14) 144111 (2017) paper contains refs. 6 and 7, and those refs. include a method for solving integral equations with feedback/self-consistency.

### Confirmed By File Inventory

Source folder inventory by extension:

| Extension | Count | Total Bytes | Scope In This Plan |
|---|---:|---:|---|
| `.tex` | 2 | 104192 | Primary source |
| `.pdf` | 1 | 2075558 | Primary source |
| `.md` | 1 | 19297 | Secondary, inspect only if it affects source interpretation |
| `.py` | 2 | 310051 | Non-goal unless the user expands scope to application/code |
| `.jpg` | 55 | 88289372 | Non-goal unless the PDF/source interpretation requires image/OCR cross-check |
| directories/no extension | 2 | not summarized | Non-goal unless execution discovers relevant assets |

Primary file metadata:

| File | Lines or Page Markers | Bytes | Current Status |
|---|---:|---:|---|
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | 495 lines | 22000 | Inventory only; not yet fully read in this plan |
| `graphite_ica_dynamic_ver5.tex` | 1974 lines | 82192 | Inventory only; not yet fully read in this plan |
| `JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` | 10 `/Type /Page` markers | 2075558 | Page marker count only; PDF page count/content not yet verified |
| `backend_changes_extracted.md` | 433 lines | 19297 | Secondary; not part of initial source scope |

### Existing Codex Records

- Existing plan guide:
  `D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md`
- Existing results folder:
  `D:\Projects\Project_Anode_Fit\Codex\results`
- Current result/ledger/handover records before this plan:
  `근거 미발견` in `Codex\results`; no phase result was listed during inventory.

### Not Yet Verified

- The actual contents and internal structure of either `.tex` file.
- Whether `graphite_ica_dynamic_ver5.tex` is standalone LaTeX or a fragment.
- The exact section boundaries of the historical `ver.1`-`ver.5` blocks.
- The exact place where the self-consistent feedback loop appears in `graphite_ica_charge_balance_ver1_rechecked2.tex`.
- The exact bibliographic entries of refs. 6 and 7 in the user's paper.
- Whether refs. 6 and 7 are available inside the PDF reference list with enough detail to locate original papers without web search.
- Whether the PDF text is extractable or requires OCR/image inspection.
- Whether the final draft should be a standalone `.tex`, a patch proposal, or a structured Markdown-to-LaTeX development report. This plan assumes Codex will produce a working draft under `Codex\results` first, without modifying source originals.

## Phase Range

| Phase | Step Range | Name | Purpose | Primary Gate |
|---|---:|---|---|---|
| Phase 001 | 1-12 | Source Inventory and Recovery Baseline | Lock file list, read targets, output paths, and execution ledger | `PASS_SOURCE_BASELINE` |
| Phase 002 | 13-28 | ver.5 Structure Extraction | Read all 1974 lines and infer Chapter 1-5 architecture from historical ver.1-5 blocks | `PASS_VER5_STRUCTURE_MAP` |
| Phase 003 | 29-43 | ver.1 Charge-Balance Logic Audit | Read all 495 lines and isolate the feedback-loop/dependency problem | `PASS_VER1_DEPENDENCY_AUDIT` |
| Phase 004 | 44-59 | User Paper and Ref. 6/7 Extraction | Read the PDF sufficiently to identify refs. 6, 7 and their method context | `PASS_REF6_REF7_METHOD_SOURCE` |
| Phase 005 | 60-76 | Self-Consistent Method Mapping | Map ref. 6/7 integral/self-consistent method to graphite dQ/dV variables | `PASS_METHOD_MAPPING` |
| Phase 006 | 77-92 | Chapter 1 Development Specification | Build the revised Chapter 1 logic and its interfaces to Chapters 2-5 | `PASS_CHAPTER1_SPEC` |
| Phase 007 | 93-112 | Draft, Validation, and Handover | Produce Codex draft/report, validate consistency, update ledger, prepare handover | `PASS_DRAFT_HANDOVER` |

## Non-goals

- Do not modify the original source files in:
  `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001`
- Do not modify `D:\Projects\Project_Anode_Fit\Claude` or Claude's outputs.
- Do not rewrite the full document before source read coverage, dependency audit, and ref. 6/7 method extraction are complete.
- Do not treat `ver.1`-`ver.5` labels as final chapter names. They are historical names until mapped.
- Do not claim that refs. 6 and 7 solve the graphite problem until the method, assumptions, and variable mapping are explicitly checked.
- Do not use the JPG files or Python/backend files unless execution discovers that they are necessary for interpreting the TeX/PDF sources.
- Do not use OCR output alone as evidence for equations or references. OCR must be cross-checked against page images, units, symbols, captions, and context.
- Do not put phase labels, audit notes, dates, or change history into LaTeX content. Work history belongs in `Codex\results`.
- Do not commit, push, or merge unless the user separately asks.

## Implementation Changes

### Created By This Planning Task

- Create:
  `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-anode-dqdv-thermodynamic-fit-development-plan.md`

### Planned Phase Outputs

- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_SOURCE_BASELINE_RESULT.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_002_VER5_STRUCTURE_EXTRACTION_RESULT.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_003_VER1_DEPENDENCY_AUDIT_RESULT.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_004_REF6_REF7_METHOD_EXTRACTION_RESULT.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_005_SELF_CONSISTENT_METHOD_MAPPING_RESULT.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_006_CHAPTER1_DEVELOPMENT_SPEC_RESULT.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_DRAFT_VALIDATION_HANDOVER_RESULT.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_007_EXECUTION_LEDGER.md`
- Create if the work pauses or context pressure rises:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_ANODE_DQDV_HANDOVER.md`

### Planned Working Artifacts

- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\ver5_chapter_structure_map.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\ver1_charge_balance_dependency_graph.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\ref6_ref7_method_notes.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\self_consistent_variable_mapping.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\chapter1_rewrite_spec.md`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_development_draft.tex`
- Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\chapter1_to_chapter5_integration_notes.md`

## Phase 001 - Source Inventory and Recovery Baseline

**Purpose:** Establish the exact source set, output paths, read-coverage plan, and ledger before any content judgment.

**Inputs:**

- `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_charge_balance_ver1_rechecked2.tex`
- `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_dynamic_ver5.tex`
- `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\JCP_147(14)_144111_(2017) - Effects of external electric field.pdf`
- `D:\Projects\Project_Anode_Fit\Codex\AGENTS.md`
- `D:\Projects\Project_Anode_Fit\Codex\plans\phase_planning_operations_guide.md`

**Steps:**

- [ ] **Step 1:** Confirm active project and output paths.
  Run:
  ```powershell
  Get-ChildItem -LiteralPath 'D:\Projects\Project_Anode_Fit\Codex' -Force
  ```
  Expected: `plans`, `results`, and `AGENTS.md` are visible.

- [ ] **Step 2:** Record primary source metadata.
  Run:
  ```powershell
  $root='D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001'
  Get-ChildItem -LiteralPath $root -Force | Select-Object Mode,Length,LastWriteTime,Name,FullName
  ```
  Expected: both `.tex` files and the JCP PDF are present.

- [ ] **Step 3:** Count line ranges for both `.tex` files.
  Run:
  ```powershell
  $files=@(
    'D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_charge_balance_ver1_rechecked2.tex',
    'D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_dynamic_ver5.tex'
  )
  foreach($f in $files){ $c=Get-Content -LiteralPath $f; "{0}`t{1}`t{2}" -f $c.Count,(Get-Item -LiteralPath $f).Length,(Split-Path $f -Leaf) }
  ```
  Expected: `495` lines for `graphite_ica_charge_balance_ver1_rechecked2.tex`; `1974` lines for `graphite_ica_dynamic_ver5.tex`, unless the file changed after this plan was written.

- [ ] **Step 4:** Create the phase execution ledger.
  Output file:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_007_EXECUTION_LEDGER.md`
  Initial rows must include all seven phases with `Status=PLANNED`.

- [ ] **Step 5:** Create `PHASE_001_SOURCE_BASELINE_RESULT.md`.
  Include source list, line counts, source folder extension summary, and non-goal files.

- [ ] **Step 6:** Mark all source files as `미검독` except metadata inspected in this phase.

- [ ] **Step 7:** Decide whether PDF page count requires a PDF parser, `pdftotext`, manual page screenshots, or OCR in Phase 004.
  If no PDF parser is available, record `page marker count only` rather than claiming page count.

- [ ] **Step 8:** Confirm no files under the source folder or Claude folder were modified.

- [ ] **Step 9:** Update the ledger row for Phase 001.

- [ ] **Step 10:** Gate check `PASS_SOURCE_BASELINE`.
  Required evidence:
  source paths, line counts, read status, output paths, and non-goal list.

- [ ] **Step 11:** If any primary source is missing, stop and ask the user before continuing.

- [ ] **Step 12:** If all primary sources are present, proceed to Phase 002.

**Gate:** `PASS_SOURCE_BASELINE` only if the primary sources exist, output paths are fixed, and all uninspected contents are explicitly marked `미검독`.

## Phase 002 - ver.5 Structure Extraction

**Purpose:** Read `graphite_ica_dynamic_ver5.tex` fully and infer the intended Chapter 1-5 structure from the historical ver.1-ver.5 layering.

**Inputs:**

- `graphite_ica_dynamic_ver5.tex`, lines 1-1974.

**Steps:**

- [ ] **Step 13:** Read lines 1-400 and record section headings, labels, equations, and `ver.` markers.

- [ ] **Step 14:** Read lines 401-800 and record section headings, labels, equations, and `ver.` markers.

- [ ] **Step 15:** Read lines 801-1200 and record section headings, labels, equations, and `ver.` markers.

- [ ] **Step 16:** Read lines 1201-1600 and record section headings, labels, equations, and `ver.` markers.

- [ ] **Step 17:** Read lines 1601-1974 and record section headings, labels, equations, and `ver.` markers.

- [ ] **Step 18:** Re-check any truncated or garbled output ranges with narrower reads.

- [ ] **Step 19:** Create a section inventory table with columns:
  `Line Range`, `Original Heading`, `Historical ver label`, `Candidate Chapter`, `Main variables`, `Equations`, `Role in argument`, `Open issues`.

- [ ] **Step 20:** Identify whether the file's ver.1-ver.5 blocks correspond to:
  `Chapter 1 charge balance`, `Chapter 2 heat/thermal contribution`, `Chapter 3 kinetic contribution`, `Chapter 4 integrated state equation`, `Chapter 5 hysteresis/history layer`.
  Mark each assignment as `확정`, `추정`, or `근거 미발견`.

- [ ] **Step 21:** Extract all equations that define or transform `dQ/dV`, `dV/dQ`, OCV, graphite potential, charge-balance, heat/entropy, kinetics, and hysteresis.

- [ ] **Step 22:** Identify all notation collisions, repeated variable names, and possible changes of independent variable.

- [ ] **Step 23:** Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\ver5_chapter_structure_map.md`

- [ ] **Step 24:** Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_002_VER5_STRUCTURE_EXTRACTION_RESULT.md`

- [ ] **Step 25:** Update the execution ledger with read coverage `1-1974`.

- [ ] **Step 26:** Gate check that `ver5` was fully read.

- [ ] **Step 27:** Gate check that the Chapter 1-5 mapping is evidence-linked to line ranges.

- [ ] **Step 28:** Stop before using the mapping as ground truth if any major line range remains unread.

**Gate:** `PASS_VER5_STRUCTURE_MAP` only if all 1974 lines are read, the structure map exists, and each Chapter candidate is tied to line evidence.

## Phase 003 - ver.1 Charge-Balance Logic Audit

**Purpose:** Read `graphite_ica_charge_balance_ver1_rechecked2.tex` fully and isolate the current logical problem in the feedback/self-consistent variable chain.

**Inputs:**

- `graphite_ica_charge_balance_ver1_rechecked2.tex`, lines 1-495.
- `ver5_chapter_structure_map.md` from Phase 002.

**Steps:**

- [ ] **Step 29:** Read lines 1-150 and record headings, equations, and definitions.

- [ ] **Step 30:** Read lines 151-300 and record headings, equations, and definitions.

- [ ] **Step 31:** Read lines 301-495 and record headings, equations, and definitions.

- [ ] **Step 32:** Re-check any truncated or garbled output ranges with narrower reads.

- [ ] **Step 33:** Build a variable inventory with columns:
  `Symbol`, `Meaning`, `Defined at line`, `Used at lines`, `Independent/dependent status`, `Unit`, `Chapter role`.

- [ ] **Step 34:** Build a dependency graph for the charge-balance argument.
  Required nodes include any present forms of:
  `V_n`, `V_{n,app}`, `V_{n,drive}`, OCV, `xi_j`, `Q_bg`, `Q`, `dQ/dV`, `dV/dQ`.

- [ ] **Step 35:** Identify feedback loops in the dependency graph.
  Classify each as one of:
  `definition-level implicit system`, `requires numerical solution`, `logical gap`, `physical assumption conflict`, `notation conflict`.

- [ ] **Step 36:** Determine whether the feedback loop occurs because a variable is reused as both input and solution, because an integral lower/upper limit depends on the solution, or because background capacity/phase fraction is defined circularly.

- [ ] **Step 37:** Compare the ver.1 dependency graph to the Chapter 1 role inferred from ver.5.

- [ ] **Step 38:** Identify which equations must become Chapter 1 interface equations for later chapters.

- [ ] **Step 39:** Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\ver1_charge_balance_dependency_graph.md`

- [ ] **Step 40:** Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_003_VER1_DEPENDENCY_AUDIT_RESULT.md`

- [ ] **Step 41:** Update the execution ledger with read coverage `1-495`.

- [ ] **Step 42:** Gate check that every feedback-loop claim cites a line range/equation.

- [ ] **Step 43:** Stop before proposing a fix if the loop location is not evidence-linked.

**Gate:** `PASS_VER1_DEPENDENCY_AUDIT` only if all 495 lines are read and at least one evidence-linked dependency classification exists, or the result explicitly states `feedback loop 근거 미발견`.

## Phase 004 - User Paper and Ref. 6/7 Extraction

**Purpose:** Identify refs. 6 and 7 in the user's JCP paper and extract the method they support, without assuming the method from memory.

**Inputs:**

- `JCP_147(14)_144111_(2017) - Effects of external electric field.pdf`
- `ver1_charge_balance_dependency_graph.md`

**Steps:**

- [ ] **Step 44:** Determine whether the PDF text can be extracted reliably.
  Preferred command if available:
  ```powershell
  pdftotext 'D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\JCP_147(14)_144111_(2017) - Effects of external electric field.pdf' -
  ```
  If unavailable, record the missing tool and use another verifiable PDF inspection method.

- [ ] **Step 45:** Confirm the actual page count. If only `/Type /Page` markers are available, record it as marker count, not verified page count.

- [ ] **Step 46:** Locate the reference list and identify references numbered 6 and 7 exactly.

- [ ] **Step 47:** Record the full bibliographic data of refs. 6 and 7:
  authors, title, journal, volume, page/article number, year, DOI if present.

- [ ] **Step 48:** Locate every in-text citation of refs. 6 and 7 in the user's paper.

- [ ] **Step 49:** Extract the local context around each in-text citation:
  problem being solved, mathematical object, equation type, iterative/self-consistent method, boundary condition, convergence claim.

- [ ] **Step 50:** If the PDF does not contain enough bibliographic or method detail, use web search or DOI lookup in execution and cite the source. Do not fill missing titles or DOI from memory.

- [ ] **Step 51:** Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\ref6_ref7_method_notes.md`

- [ ] **Step 52:** Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_004_REF6_REF7_METHOD_EXTRACTION_RESULT.md`

- [ ] **Step 53:** Mark OCR-derived or manually transcribed equations as `판독 불확실` unless cross-checked against page image and context.

- [ ] **Step 54:** Update the execution ledger with PDF read coverage by page range.

- [ ] **Step 55:** Gate check that refs. 6 and 7 are identified exactly.

- [ ] **Step 56:** Gate check that the method extraction is tied to the user's paper context, not just reference titles.

- [ ] **Step 57:** Stop and ask the user if refs. 6 and 7 cannot be identified in the PDF.

- [ ] **Step 58:** Stop and ask the user if refs. 6 and 7 are identified but their original papers are inaccessible and method details are insufficient.

- [ ] **Step 59:** Proceed only when the method source is explicit enough to map variables.

**Gate:** `PASS_REF6_REF7_METHOD_SOURCE` only if refs. 6 and 7 are exactly identified and their use in the user's paper is recorded.

## Phase 005 - Self-Consistent Method Mapping

**Purpose:** Translate the ref. 6/7 method into the graphite ICA/DVA charge-balance problem without importing invalid physical assumptions.

**Inputs:**

- `ver1_charge_balance_dependency_graph.md`
- `ref6_ref7_method_notes.md`
- `ver5_chapter_structure_map.md`

**Steps:**

- [ ] **Step 60:** Define the abstract mathematical form of the ref. 6/7 method.
  Required fields:
  `unknown function`, `known kernel`, `boundary condition`, `self-consistent variable`, `iteration or solver`, `normalization`.

- [ ] **Step 61:** Define the graphite problem's abstract form from ver.1.
  Required fields:
  `unknown quantity`, `measured quantity`, `thermodynamic OCV relation`, `background capacity`, `phase fraction`, `voltage variable`, `capacity variable`.

- [ ] **Step 62:** Build a variable mapping table:
  `Ref method symbol`, `Ref method meaning`, `Graphite dQ/dV symbol`, `Graphite meaning`, `mapping confidence`, `assumption required`.

- [ ] **Step 63:** Identify which parts of the reference method are mathematical and portable.

- [ ] **Step 64:** Identify which parts of the reference method are physical and not automatically portable.

- [ ] **Step 65:** Decide whether the graphite problem should be formulated as:
  `implicit equation`, `Fredholm-type integral equation`, `Volterra-type integral equation`, `fixed-point equation`, `root-finding problem`, or `coupled differential/integral system`.
  The choice must cite evidence from Phase 003 and Phase 004.

- [ ] **Step 66:** Define a solver-neutral formulation first.
  Do not choose numerical algorithms before the mathematical form is fixed.

- [ ] **Step 67:** Propose numerical solution options only after Step 65:
  fixed-point iteration, Newton/secant root solve, discretized integral solve, regularized least-squares fit, or constrained optimization.

- [ ] **Step 68:** Define identifiability risks:
  parameter degeneracy, OCV/background-capacity separability, smoothing of dQ/dV peaks, hysteresis confounding, kinetic/thermal leakage into thermodynamic shape.

- [ ] **Step 69:** Define validation observables:
  reproduced dQ/dV peak positions, dV/dQ consistency, charge-balance residual, monotonicity/normalization of phase fraction, physically plausible OCV.

- [ ] **Step 70:** Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\self_consistent_variable_mapping.md`

- [ ] **Step 71:** Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_005_SELF_CONSISTENT_METHOD_MAPPING_RESULT.md`

- [ ] **Step 72:** Update the execution ledger.

- [ ] **Step 73:** Gate check that every variable mapping has an evidence source or is marked `추정`.

- [ ] **Step 74:** Gate check that all non-portable assumptions are listed.

- [ ] **Step 75:** Stop if the method mapping requires a physical assumption that conflicts with ver.1 or ver.5.

- [ ] **Step 76:** Proceed only if the graphite problem has a solver-neutral mathematical formulation.

**Gate:** `PASS_METHOD_MAPPING` only if the self-consistent loop is converted into an explicit mathematical problem class with evidence-linked variable mapping.

## Phase 006 - Chapter 1 Development Specification

**Purpose:** Convert the audited ver.1 logic and method mapping into a revised Chapter 1 specification that can support later Chapter 2-5 development.

**Inputs:**

- `ver5_chapter_structure_map.md`
- `ver1_charge_balance_dependency_graph.md`
- `self_consistent_variable_mapping.md`

**Steps:**

- [ ] **Step 77:** Define Chapter 1's role in one paragraph:
  thermodynamic charge-balance and internal graphite-potential determination.

- [ ] **Step 78:** Define Chapter 1 non-role:
  thermal correction, kinetic overpotential, full state equation, and hysteresis are not solved in Chapter 1 unless explicitly required as interfaces.

- [ ] **Step 79:** List Chapter 1 input quantities.

- [ ] **Step 80:** List Chapter 1 unknowns.

- [ ] **Step 81:** List Chapter 1 output/interface quantities passed to Chapter 2-5.

- [ ] **Step 82:** Rewrite the logical order as:
  definitions -> measured variables -> thermodynamic relation -> charge-balance constraint -> self-consistent equation -> solution method -> dQ/dV/DVA observable -> limitations.

- [ ] **Step 83:** Identify equations that must be retained from ver.1 unchanged.

- [ ] **Step 84:** Identify equations that must be rewritten due to circular dependency.

- [ ] **Step 85:** Identify equations that must be deferred to later chapters.

- [ ] **Step 86:** Define notation rules to prevent reuse of the same symbol as both input and solved quantity.

- [ ] **Step 87:** Define how historical `ver.1`-`ver.5` names become Chapter 1-5 names in the new draft.

- [ ] **Step 88:** Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\chapter1_rewrite_spec.md`

- [ ] **Step 89:** Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\chapter1_to_chapter5_integration_notes.md`

- [ ] **Step 90:** Create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_006_CHAPTER1_DEVELOPMENT_SPEC_RESULT.md`

- [ ] **Step 91:** Update the execution ledger.

- [ ] **Step 92:** Gate check that Chapter 1 no longer depends on a variable before it is defined or solved.

**Gate:** `PASS_CHAPTER1_SPEC` only if Chapter 1 has a clear input/unknown/output contract and a non-circular self-consistent formulation.

## Phase 007 - Draft, Validation, and Handover

**Purpose:** Produce a Codex-side development draft and close the phase loop with validation evidence and handover.

**Inputs:**

- All Phase 001-006 outputs.
- Primary sources as read-only evidence.

**Steps:**

- [ ] **Step 93:** Create a working LaTeX draft:
  `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_development_draft.tex`

- [ ] **Step 94:** The draft must not overwrite either original `.tex` source.

- [ ] **Step 95:** The draft must not include phase labels, audit notes, or change-history comments in the LaTeX body.

- [ ] **Step 96:** Include citations or placeholders only where the source was verified.
  If refs. 6/7 details are verified, use their actual citation keys or bibliographic names.
  If not verified, write the issue in the result document, not as a fake citation.

- [ ] **Step 97:** Create a Markdown companion report explaining the draft:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_DRAFT_VALIDATION_HANDOVER_RESULT.md`

- [ ] **Step 98:** Validate notation consistency against `chapter1_rewrite_spec.md`.

- [ ] **Step 99:** Validate dependency graph consistency against `ver1_charge_balance_dependency_graph.md`.

- [ ] **Step 100:** Validate Chapter 1-5 interfaces against `chapter1_to_chapter5_integration_notes.md`.

- [ ] **Step 101:** Validate that no unverified ref. 6/7 claim is presented as confirmed.

- [ ] **Step 102:** Validate that OCR-derived text, if any, is marked with certainty level.

- [ ] **Step 103:** If the draft is standalone, run a LaTeX build.
  Candidate command:
  ```powershell
  pdflatex -interaction=nonstopmode -halt-on-error 'D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_development_draft.tex'
  ```
  If the draft is not standalone, record `LaTeX build not applicable` and run a targeted syntax/brace check instead.

- [ ] **Step 104:** Record all validation commands and results.

- [ ] **Step 105:** Create or update:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_007_EXECUTION_LEDGER.md`

- [ ] **Step 106:** If work stops before user review, create:
  `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_ANODE_DQDV_HANDOVER.md`

- [ ] **Step 107:** Handover chain must include this plan and all phase results created so far.

- [ ] **Step 108:** List confirmed decisions, open questions, and `근거 미발견` separately.

- [ ] **Step 109:** List exact files read fully and their line/page ranges.

- [ ] **Step 110:** List exact files created.

- [ ] **Step 111:** Gate check that every phase result exists or is explicitly marked incomplete.

- [ ] **Step 112:** Final report to user with next execution choices.

**Gate:** `PASS_DRAFT_HANDOVER` only if the draft/report exists, validation evidence is recorded, and source coverage is explicit.

## Implementation Interfaces

### Read Coverage Record

Each result file must include:

```markdown
## Read Coverage

| Source | Required Range | Actual Range Read | Status | Notes |
|---|---:|---:|---|---|
| `path` | `1-end` | `1-400, 401-800` | `READ_FULL` / `부분 검독` / `미검독` | evidence note |
```

Use `READ_FULL` only when all lines/pages were actually read and truncation risk was checked.

### Dependency Graph Record

Use this table in `ver1_charge_balance_dependency_graph.md`:

```markdown
| Node | Defined At | Depends On | Used By | Status | Issue Type | Evidence |
|---|---|---|---|---|---|---|
| `V_n` | line/equation | `...` | `...` | `확정` | `none` / `implicit` / `logical gap` | source line |
```

### Chapter Mapping Record

Use this table in `ver5_chapter_structure_map.md`:

```markdown
| Candidate Chapter | Historical Label | Source Line Range | Core Claim | Equations | Interface To Other Chapters | Confidence |
|---|---|---:|---|---|---|---|
| Chapter 1 | ver.1 | `x-y` | charge-balance thermodynamic basis | `...` | passes `...` | `확정` / `추정` |
```

### Ref. 6/7 Method Record

Use this table in `ref6_ref7_method_notes.md`:

```markdown
| Ref No. | Bibliography | User Paper Citation Context | Mathematical Object | Solver/Method | Portable To Graphite? | Non-portable Assumptions |
|---:|---|---|---|---|---|---|
| 6 | full citation | page/equation | integral/self-consistent object | method | yes/no/partial | list |
```

### Ledger Row

Use this ledger structure:

```markdown
| Phase/Subphase | Planned Steps | Actual Steps | Block | Purpose | Status | Plan | Result | Machine Artifacts | Validation | Gate | Next Step |
|---|---:|---:|---|---|---|---|---|---|---|---|---:|
| Phase001 | 1-12 | 1-12 | source | Source inventory and baseline | PASS | `plans/...md` | `results/...md` | none | source metadata checked | `PASS_SOURCE_BASELINE` | 13 |
```

## Test Plan

### Source Coverage Tests

- Both `.tex` files must have read coverage from line 1 to end.
- PDF must have page-level coverage or an explicit explanation why page-level coverage could not be extracted.
- Any OCR-derived content must be marked `판독 불확실` until cross-checked.

### Structure Tests

- Every proposed Chapter 1-5 assignment must cite source line ranges from `graphite_ica_dynamic_ver5.tex`.
- Historical `ver.1`-`ver.5` names must not be silently overwritten; they must be mapped.

### Logic Tests

- Every self-consistency claim must be represented in the dependency graph.
- The feedback loop must be classified as implicit formulation, numerical-solution requirement, logical gap, physical assumption conflict, or notation conflict.
- The revised Chapter 1 specification must have explicit input, unknown, and output/interface sets.

### Literature Tests

- Refs. 6 and 7 must be identified by exact bibliographic entries.
- Their use in the user's paper must be recorded before importing their method.
- If external lookup is used, DOI or source URL must be recorded.

### Draft Tests

- Draft file must live under `Codex\results`.
- Draft must not modify source `.tex` files.
- Draft must not contain phase/audit/change-history labels in the LaTeX body.
- LaTeX build or syntax check must be attempted if the draft format allows it.

## Assumptions

- The two `.tex` files in the source folder are the primary drafts the user referred to.
- The PDF named `JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` is the user's paper mentioned in the request.
- The `/Type /Page` marker count of 10 is only an inventory clue, not a verified page count.
- `graphite_ica_dynamic_ver5.tex` probably contains historical ver.1-ver.5 material, but the exact block boundaries are `미검증` until Phase 002.
- `graphite_ica_charge_balance_ver1_rechecked2.tex` probably represents the current Chapter 1 restart draft, but the exact logic is `미검증` until Phase 003.
- Refs. 6 and 7 are assumed relevant because the user stated so; their exact content and applicability are `미검증` until Phase 004-005.

## Correction History

| Date | Change | Reason |
|---|---|---|
| 2026-05-27 | Initial plan created under updated Codex plan format | User requested the original situation-assessment plan using the updated plan/AGENTS rules |
