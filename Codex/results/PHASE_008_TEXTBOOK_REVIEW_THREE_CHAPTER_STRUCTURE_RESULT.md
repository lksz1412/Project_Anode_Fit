# Phase 008 Textbook/Review Three-Chapter Structure Result

## Chain

- Active plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-07-19-v1010-v1023-ch1-ch3-scientific-audit-master-plan-v2.md`
- Plan steps: 102-116
- Canonical snapshot: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Section-purpose map: `D:\Projects\Project_Anode_Fit\Codex\results\phase008_section_purpose_map.csv`
- Adjudicated score matrix: `D:\Projects\Project_Anode_Fit\Codex\results\phase008_adjudicated_structure_scores.csv`
- Reorganization map: `D:\Projects\Project_Anode_Fit\Codex\results\phase008_reorganization_map.csv`
- Detailed Sol adjudication: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase008\P8_sol_summary.md`
- Score-matrix SHA-256: `B4F2A595767BC22EED4C8932654111F2B919EFDBA1B205E91239D4A4B45194E5`
- Reorganization-map SHA-256: `E080563FAA7BD3E2243BC283275CCE431C009F6A17E6408A193FE1BB5500437C`
- Git commands executed: none

## Coverage

The recursive closure of all three v1.0.23 masters was read in full: 53 unique
TeX files and 7,695 unique physical lines after deduplicating the shared
preamble. The 49-row section-purpose map, Terra's 30 structural scores and 18
reorganization proposals, the complete Phase 004 convention/literature
baseline, the dependency graph, the active 342-line plan, and the relevant
v1.0.19-v1.0.22 architecture plans, reports, and handovers were also read in
full. The Sol adjudication then re-read those inputs independently.

The canonical score matrix contains 30 complete rows: ten dimensions for each
chapter. Terra and Sol agree on 14 rows, Sol modifies 14, and Sol rejects two.
The canonical reorganization map contains 18 complete, uniquely identified
proposals: eight adopted, nine modified, and one rejected. Fifteen are required
and three are high-value. There are no blank fields.

## Gate

**`STRUCTURE_PASS_WITH_REQUIRED_REORGANIZATION`.**

This is a conditional structure/genre pass, not a scientific-correctness pass.
The chapters have defensible organizing spines, but none yet closes the stated
textbook/review/fitting contract. Required changes in the 18-row reorganization
map remain binding. Phase 005-007 scientific findings and Phase 009 code-fidelity
findings remain open independently.

## Genre Adjudication

| Chapter | Defensible current genre | Adjudication |
|---|---|---|
| Chapter 1 | Textbook foundation plus graphite review/application | Part 0 and the state-to-observable derivations are the strongest textbook portion and should remain in the main master. Evidence balance, identifiability, and uncertainty quantification are not closed. |
| Chapter 2 | Dependent volume chapter and LCO material-delta review | It is coherent under its actual contract of inheriting Chapter 1 equations and adding LCO-specific terms. It is not a standalone derivational review and should not claim that genre. |
| Chapter 3 | Literature-grounded transfer/research roadmap with bounded textbook derivations | The survival map, equilibrium blend derivation, and GS-1/GS-2 stopping points form a valid roadmap. Missing host-resolved validation, mechanics closure, inverse analysis, and UQ prevent a closed textbook/review classification. |

## Controlling Judgments

1. **Keep Chapter 1 Part 0.** Moving the complete 865-line common foundation to
   an appendix would put later use before derivation and break the approved
   dependency architecture. Add a short fast route and dependency map; move only
   optional excursions after a label and premise-use audit.
2. **Keep only the necessary Part T recap.** A canonical width/regime/status
   table should reduce duplication, while the local thermal recap and
   entropy-specific derivation remain because they are prerequisites, not mere
   repetition.
3. **Name Chapter 2's dependency honestly.** Add a compact state/equation recap
   but do not duplicate the Chapter 1 derivations or pretend that the chapter is
   a standalone review.
4. **Keep Chapter 3's survival map first.** It determines whether inherited
   equations may be reused; moving it after examples or a full model would turn
   a prerequisite test into a retrospective summary.
5. **Move Chapter 3 API detail, not its scientific gates.** API names,
   signatures, docstring instructions, and detailed procedures belong in a
   same-master reproducibility appendix. A compact main-text account of G1-G3
   and GS-1/GS-2 must remain because it defines scientific recoveries and
   exclusions.
6. **Use common checkpoints, not identical chapter order.** Each chapter should
   expose scope/state, equilibrium status, observable mapping,
   kinetics/mechanisms, inverse/identifiability, validity/UQ, and
   reproducibility, but order them according to its dependency graph:
   foundation-first for Chapter 1, delta-first for Chapter 2, and
   survival-map-first for Chapter 3.

## Required Reorganization

### Chapter 1

- Retain Part 0 and add a 2-4 page fast-route/prerequisite map.
- Put an equilibrium/metastability/nucleation/transport/path-hysteresis status
  hierarchy before branch interpretation.
- Create one canonical width/regime/status table while retaining Part T's
  minimal local derivation.
- Add an early observable/operator and non-identifiability orientation without
  moving the load-bearing derivations ahead of their prerequisites.
- Add inverse/identifiability, validity/UQ, and reproducibility closures.
- Move LCO-only workflow/interface material to Chapter 2 and retain one
  canonical code map.
- Preserve non-rendered source-provenance comments; they are audit anchors, not
  body-level API leakage.

### Chapter 2

- Label the chapter explicitly as a dependent volume chapter and add a compact
  inherited-state/equation recap.
- Place LCO phase, ordering, and observable evidence before the effective
  regular-solution reduction.
- Surface the project-factorization, frozen-approximation, and MSMR
  non-identity warning before the electronic gate is first used.
- Add Chapter 2-local inverse/identifiability, validity/UQ, fitting, and
  reproducibility sections.
- Localize LCO-only inputs while linking to, rather than copying, the shared
  implementation map.

### Chapter 3

- Add a concise pre-map orientation defining material identity, cycle/history,
  reference state, geometry/stress measure, and mass/capacity basis; keep the
  survival map as the first substantive section.
- Distinguish directly measured observables from latent reduced host components
  before the equilibrium blend derivation.
- Put formulation basis, biaxial-to-hydrostatic mapping, kinematics,
  finite-deformation range, geometry, plasticity, contact, and SEI limits before
  the first mechanics equation.
- Move detailed API prose to a same-master appendix and retain compact scientific
  gate/exclusion meanings in the body.
- Add inverse/identifiability, quantitative UQ, validation requirements, and a
  scope-controlled equilibrium fitting guide before reproducibility.

## Literature Placement Guard

Literature placement must obey the Phase 004 access and adoption matrix.
Metadata- or abstract-only records may support organization, terminology, or a
bounded research gap, but may not support equations, numerical coefficients,
material-specific calibration, or proof of identifiability. `ADOPT` applies only
to the recorded role; `CANDIDATE`, `HOLD`, and `REJECT` must not be silently
promoted. Structural relocation cannot repair a misattributed or contradictory
source claim.

## Confirmed, Unresolved, And Unverified

- **확정:** Chapter 1 has a defensible textbook foundation; Chapter 2 is an
  intentionally dependent material-delta chapter; Chapter 3 is a valid research
  roadmap rather than a closed textbook/review chapter.
- **확정:** all three chapters lack a sufficient inverse/identifiability and UQ
  closure for defensible fitting claims.
- **확정:** Chapter 3's mass-basis and mechanics validity boundaries are
  underdeclared and must precede quantitative use.
- **미결/미검증:** literature claims whose full text was unavailable or whose
  Phase 004 support status is insufficient remain open; reorganization does not
  upgrade them.
- **미검증:** no source files were reorganized, so post-move label resolution,
  TeX build status, page layout, and cross-master reference integrity have not
  been tested.
- **미검증:** no company experimental data were available; worked examples and
  regression gates remain demonstrations, not empirical validation.

## Verification

- Score rows: 30; Chapter 1/2/3: 10 each; dimensions: 10.
- Agreement: 14 `AFFIRM`, 14 `MODIFY`, two `REJECT`.
- Reorganization rows: 18 unique IDs; 15 required, three high-value.
- Disposition: eight `ADOPT`, nine `MODIFY`, one `REJECT`.
- Blank cells: zero.
- Agent citation-range validation: 402 file/line citations checked with zero
  range errors.
- Source changes: none.
- Git commands: none.

## Phase Result

Phase 008 is complete at `STRUCTURE_PASS_WITH_REQUIRED_REORGANIZATION`. An
unconditional `STRUCTURE_PASS` is not closed, and this conditional structure
gate does not close any scientific, empirical, inverse, or code-fidelity gate.
