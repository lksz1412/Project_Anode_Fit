# Rebuild v2 Source Evidence Index

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 002 - Source Evidence Recertification And Reference-Only Boundary`

Created: 2026-05-27

## Purpose

This index is the rebuild boundary table for the from-scratch manuscript work. It separates confirmed source claims from unverified claims and missing evidence so the rebuilt manuscript does not silently inherit old prose, old logical errors, or unsupported claims.

## Mandatory Source File Metadata

| Source File | Exists | Size | Count | Coverage Status |
|---|---:|---:|---:|---|
| `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_dynamic_ver5.tex` | yes | 82,192 bytes | 1,974 lines | prior `READ_FULL` coverage recorded as lines 1-1974 |
| `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\graphite_ica_charge_balance_ver1_rechecked2.tex` | yes | 22,000 bytes | 495 lines | prior `READ_FULL` coverage recorded as lines 1-495 |
| `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001\JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` | yes | 2,075,558 bytes | 10 pages | prior extracted-text coverage recorded as pages 1-10; exact equation glyphs require visual/source check before transcription |

## Evidence Classification

| Source | Claim | Evidence File | Evidence Range | Confidence | Reuse Permission |
|---|---|---|---|---|---|
| `graphite_ica_dynamic_ver5.tex` | The file is a single stacked LaTeX document containing historical ver.1-ver.5 layers that should now be treated as chapter-development history rather than separate final files. | `ver5_chapter_structure_map.md` | full source coverage recorded as lines 1-1974; map identifies preamble and five historical layers | 확정 | Architecture evidence only; do not copy body prose wholesale. |
| `graphite_ica_dynamic_ver5.tex` | Preamble and document setup occupy the initial block before the historical chapter layers. | `ver5_chapter_structure_map.md` | lines 1-61 | 확정 | Use only for LaTeX setup reference if needed. |
| `graphite_ica_dynamic_ver5.tex` | Historical ver.1 / Chapter 1 candidate occupies the first conceptual layer, but it is not the final Chapter 1 base because the user identified a major logic error and restarted from corrected ver1. | `ver5_chapter_structure_map.md`; user instruction; `2026-05-27-rebuild-readiness-assessment-report.md` | lines 62-523 | 확정 | Treat as ancestor/reject context only. |
| `graphite_ica_dynamic_ver5.tex` | Historical ver.2 contains a heat/thermal expansion layer. | `ver5_chapter_structure_map.md` | lines 525-852 | 확정 | Later-chapter interface idea only; do not import as active Chapter 1 logic. |
| `graphite_ica_dynamic_ver5.tex` | Historical ver.3 contains a kinetic expansion layer. | `ver5_chapter_structure_map.md` | lines 855-1118 | 확정 | Later-chapter interface idea only. |
| `graphite_ica_dynamic_ver5.tex` | Historical ver.4 contains an integrated-system layer. | `ver5_chapter_structure_map.md` | lines 1122-1516 | 확정 | Architecture context only. |
| `graphite_ica_dynamic_ver5.tex` | Historical ver.5 contains hysteresis/advanced fitting direction. | `ver5_chapter_structure_map.md` | lines 1520-1974 | 확정 | Future chapter/interface context only. |
| `graphite_ica_dynamic_ver5.tex` | The old ver5 body still carries risks such as old Chapter 1 OCV basis, `Q_n`/`Q_ext` confusion, `w_j` notation collision, `R_n`/Butler-Volmer double-count risk, heat derivative caution, and hysteresis identifiability risk. | `ver5_chapter_structure_map.md`; `2026-05-27-rebuild-readiness-assessment-report.md` | structural issue notes across mapped chapters | 확정 | Use as failure inventory input, not as reusable prose. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | The corrected ver1 file is the mathematical foundation source for rebuilding Chapter 1. | `ver1_charge_balance_dependency_graph.md` | full source coverage recorded as lines 1-495 | 확정 | Use as mathematical evidence; do not copy prose wholesale. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | `Q_ext` and normalized external charge `q` are defined before the charge-balance model. | `ver1_charge_balance_dependency_graph.md` | lines 95-105 | 확정 | Rebuild manuscript should preserve this measurement-first ordering. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | Internal gallery/stage fractions `xi_j` are defined as thermodynamic internal states. | `ver1_charge_balance_dependency_graph.md` | lines 109-117 | 확정 | Use as Chapter 1 state-variable evidence. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | The central corrected charge-balance relation is `Q_cell q = Q_bg(V_n,T) + sum_j Q_{j,tot} xi_j`. | `ver1_charge_balance_dependency_graph.md` | lines 121-127 | 확정 | Use as core equation idea; exact notation will be controlled by the notation contract. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | `V_n` is solved from the charge-balance residual and must not be prescribed as an independent external variable. | `ver1_charge_balance_dependency_graph.md`; `self_consistent_variable_mapping.md` | lines 121-129; self-consistency mapping | 확정 | Core rebuild rule. Any equation depending on `V_n` must follow the root/operator definition. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | Equilibrium open-circuit voltage is implicit through charge balance rather than a standalone empirical axis. | `ver1_charge_balance_dependency_graph.md` | lines 148-162 | 확정 | Preserve this as the thermodynamic basis for Chapter 1. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | A slope floor or monotonicity regularization appears as a local numerical protection concept. | `ver1_charge_balance_dependency_graph.md` | lines 176-182 | 확정 | Treat as numerical protocol detail, not fundamental thermodynamics. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | Distinct voltages are introduced and must not be collapsed: internal negative electrode potential, apparent/equilibrium potential, and driven/measured cell voltage roles need separation. | `ver1_charge_balance_dependency_graph.md` | lines 203-237 | 확정 | Use in notation/equation dependency contract. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | State dynamics feed back through `V_n`, giving a coupled self-consistent structure. | `ver1_charge_balance_dependency_graph.md` | lines 240-286 | 확정 | Classify as nonlinear DAE/Volterra-like feedback problem; do not present as explicit one-pass ODE. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | At rest, `q` is fixed while internal states can relax through the same constrained potential structure. | `ver1_charge_balance_dependency_graph.md` | lines 289-299 | 확정 | Use only after defining the dynamic/root structure. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | Barrier distribution or multi-stage population ideas appear as optional broadening detail. | `ver1_charge_balance_dependency_graph.md` | lines 320-349 | 확정 | Later fitting/identifiability material; keep out of the minimum Chapter 1 foundation unless needed. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | ICA/DVA expressions must be taken with respect to external charge and the implicitly solved potential. | `ver1_charge_balance_dependency_graph.md` | lines 353-411 | 확정 | Use in solver/validation protocol after the dependency graph is fixed. |
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | Heat coupling handoff uses `dxi_j/dt` and belongs to later chapters. | `ver1_charge_balance_dependency_graph.md` | lines 462-471 | 확정 | Interface only; do not expand full heat model in Chapter 1. |
| Corrected ver1 plus method mapping | The apparent circularity is not a contradiction by itself; it is a self-consistent DAE/Volterra-like feedback structure requiring an explicit closure/solution method. | `self_consistent_variable_mapping.md`; `ver1_charge_balance_dependency_graph.md` | mapping sections on direct DAE baseline, quasi-equilibrium reference, frozen-feedback reference, discretized integral solve | 확정 | This is the main logic repair direction for the rebuild. |
| 2017 user paper PDF | The paper is DOI `10.1063/1.5000882` and contains citations to refs. 6 and 7 that are relevant to integral-equation/closure methods. | `ref6_ref7_method_notes.md`; PDF extracted text | PDF pages 1-10; citation hits on pages 2, 5, 8 | 확정 for metadata and extracted-text citation context | Use as bridge evidence; exact formulas require visual/source confirmation. |
| Ref. 6 | Ref. 6 is S. Lee, C. Y. Son, J. Sung, S. Chong, JCP 134, 121102 (2011), DOI `10.1063/1.3565476`. | `ref6_ref7_method_notes.md` | reference identification section | 확정 for bibliographic metadata from prior extraction | Not yet `READ_FULL`; do not claim complete derivation from ref. 6 itself. |
| Ref. 7 | Ref. 7 is C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, S. Lee, JCP 138, 164123 (2013), DOI `10.1063/1.4802584`. | `ref6_ref7_method_notes.md` | reference identification section | 확정 for bibliographic metadata from prior extraction | Not yet `READ_FULL`; do not claim complete derivation from ref. 7 itself. |
| User paper plus refs. 6/7 notes | The portable method pattern is: start from an integral/self-consistent expression, define a reference problem, express the unknown result through a correction or ratio relative to the reference, close the expression approximately, then validate against a direct or more exact calculation. | `ref6_ref7_method_notes.md`; `self_consistent_variable_mapping.md` | method extraction and graphite mapping sections | 확정 as method pattern from available notes; 추정 when transferred to graphite until formalized | Use as closure strategy only, not as direct physical equivalence. |
| Refs. 6/7 physical content | Geminate-pair diffusion physics, Smoluchowski radial coordinate, Coulomb/external-field pair potential, contact sink, and Onsager-specific assumptions are not portable to graphite staging as physical assumptions. | `self_consistent_variable_mapping.md` | non-portable/ref-specific items section | 확정 as scope guard | Do not import into the LIB/graphite model. |
| 2017 user paper PDF | Exact equation glyphs and formula layout in the PDF were not visually verified during this phase. | `ref6_ref7_method_notes.md`; Phase 002 PDF metadata check | extracted text pages 1-10; no visual equation-glyph audit in Phase 002 | 미검증 | Do not transcribe exact equations from the PDF without visual/source check. |
| Full ref. 6 paper | Full paper text and exact derivation of ref. 6 were not read in this project record. | `ref6_ref7_method_notes.md`; readiness report | notes identify reference but do not record `READ_FULL` for original ref. 6 | 미검증 | Can cite metadata as pending; cannot claim complete ref. 6 derivation. |
| Full ref. 7 paper | Full paper text and exact derivation of ref. 7 were not read in this project record. | `ref6_ref7_method_notes.md`; readiness report | notes identify reference but do not record `READ_FULL` for original ref. 7 | 미검증 | Can cite metadata as pending; cannot claim complete ref. 7 derivation. |
| `graphite_ica_chapter1_development_draft.tex` | The previous Chapter 1 draft is a reference sketch produced before the from-scratch rebuild boundary. | `2026-05-27-rebuild-readiness-assessment-report.md`; file listing | draft file exists in `Codex\results` | 확정 | Reference sketch only; not a manuscript base and not body text source. |
| Earlier v1 rebuild plan | `2026-05-27-graphite-ica-from-scratch-rebuild-plan.md` is superseded by the v2 canonical plan. | `REBUILD_V2_PHASE_001_PLAN_BASELINE_RESULT.md`; `REBUILD_V2_EXECUTION_LEDGER.md` | Phase 001 baseline | 확정 | Planning context only. |
| Numerical fitting data | No actual LIB/graphite ICA dataset has been loaded or recorded in the rebuild evidence chain. | current project records | no dataset artifact found in Phase 001-002 evidence chain | 근거 미발견 | Do not claim fitted parameter values or data performance. |
| Direct numerical solver | No implemented direct DAE/Volterra solver artifact exists yet in the rebuild v2 chain. | current project records | no solver artifact before Phase 008 | 근거 미발견 | Solver claims must wait for protocol/implementation phase. |
| LaTeX build evidence | No successful LaTeX build has been recorded for the final rebuilt manuscript because the manuscript has not yet been assembled. | current project records | no Phase 011-014 artifact yet | 근거 미발견 | Do not claim final build/syntax success. |
| Source modification status | Phase 002 did not modify source `.tex` files, the PDF, or Claude workspace files. | git status; file operation record | only Codex result files targeted | 확정 | Source files remain read-only evidence for this phase. |

## Boundary Rules For Rebuild

- Old ver5 is allowed to define the intended chapter trajectory, not the final text.
- Corrected ver1 is allowed to define the core mathematical problem, not final prose.
- Refs. 6/7 are allowed to motivate a closure pattern only after the graphite feedback structure is stated in its own variables.
- Unsupported fitting, solver, or exact-formula claims must remain out of manuscript body text until their phase gate is passed.
- Phase/audit/change-history notes belong in `Codex\results`, not in the eventual LaTeX manuscript body.
