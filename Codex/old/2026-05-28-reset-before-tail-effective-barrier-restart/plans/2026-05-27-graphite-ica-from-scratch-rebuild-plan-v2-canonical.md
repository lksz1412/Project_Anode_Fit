# Graphite ICA/DVA From-Scratch Rebuild v2 Canonical Plan

## Summary

- This plan supersedes `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan.md` for execution detail.
- The previous plan correctly identified the from-scratch direction, but it was too shallow for controlled manuscript rebuilding.
- The objective is not to repair `graphite_ica_chapter1_development_draft.tex`.
- The objective is to write a new manuscript from a blank LaTeX file, using the previous source reads and audit outputs only as evidence.
- The new manuscript must preserve the central corrected ver1 insight:

```text
Q_cell q = Q_bg(V_n,T) + sum_j Q_j,tot xi_j
```

- `V_n` must be defined as a solved internal graphite potential, not as a prescribed `V_OCV(q,T)` input.
- The feedback loop must be formulated as a charge-balance-constrained nonlinear DAE / Volterra-type system.
- The user's JCP 147, 144111 (2017) paper and refs. 6/7 may be used only for a reference-closure method pattern unless the full original refs. 6/7 papers are later read and recorded.
- This plan intentionally mirrors the RO_SkillDict planning style: current ground truth, phase range, non-goals, planned artifacts, cumulative step numbering, phase gates, stop conditions, validation interfaces, test plan, assumptions, and correction history.

## Current Ground Truth

- Active project: `D:\Projects\Project_Anode_Fit`
- Codex workspace: `D:\Projects\Project_Anode_Fit\Codex`
- Plan directory: `D:\Projects\Project_Anode_Fit\Codex\plans`
- Result directory: `D:\Projects\Project_Anode_Fit\Codex\results`
- Claude workspace boundary: `D:\Projects\Project_Anode_Fit\Claude`, read or modify only if user explicitly asks.
- Source download folder:
  `D:\Projects\Project_BatteryData_Display_임시저장소\새 폴더\drive-download-20260527T100231Z-3-001`

Confirmed source coverage from prior phase records:

- `graphite_ica_dynamic_ver5.tex`: READ_FULL lines 1-1974 in Phase 002.
- `graphite_ica_charge_balance_ver1_rechecked2.tex`: READ_FULL lines 1-495 in Phase 003.
- `JCP_147(14)_144111_(2017) - Effects of external electric field.pdf`: READ_FULL_TEXT pages 1-10 via bundled Python `pypdf` in Phase 004.

Confirmed interpretation:

- `graphite_ica_dynamic_ver5.tex` is a merged historical file.
- Its internal ver1-ver5 stack is best reinterpreted as Chapter 1-5.
- Historical ver1 inside ver5 is not the new Chapter 1 core.
- Corrected `graphite_ica_charge_balance_ver1_rechecked2.tex` is the primary Chapter 1 evidence source.
- Corrected ver1 changes the foundation from "read voltage from OCV" to "solve internal graphite potential from charge balance."
- The feedback loop is:

```text
xi_j -> charge balance -> V_n -> xi_eq/k_j -> dxi_j/dt or dxi_j/dq -> xi_j
```

- This is not a fatal contradiction. It is a self-consistent mathematical system requiring explicit formulation and solution/closure rules.
- The safest exact formulation is:

```text
G(V; q,T,xi,theta)=0
dxi/dq = F(q,xi,V_root(q,T,xi),T,I,theta)
```

- The q-domain integral form is Volterra-like because the upper limit is the current coordinate.
- refs. 6/7 are Fredholm second-kind method sources in the 2017 paper, so their physical equation type must not be imposed on graphite.
- The portable refs. 6/7 idea is reference-ratio or reference-correction closure.

Current known limitations:

- `pdflatex`, `xelatex`, and `lualatex` were not found in PATH during Phase 007.
- Exact glyph-level visual verification of the 2017 PDF equations was not completed.
- Full original refs. 6 and 7 papers were not read.
- No direct DAE/root-solve numerical benchmark has been implemented.
- No real LIB dQ/dV fitting dataset has been loaded.

## Core Principle

The rebuild must separate four layers that the earlier drafts tended to blur:

1. **Thermodynamic storage identity**: charge conservation determines `V_n`.
2. **Dynamic state evolution**: `xi_j` evolves while `V_n` is repeatedly solved from charge balance.
3. **Approximate closure**: refs. 6/7-inspired reference correction may simplify the self-consistent loop, but cannot replace the exact system definition.
4. **Fitting / validation**: parameters are accepted only when charge-balance residuals, state bounds, peak observables, and direct-solver mismatch pass explicit gates.

No manuscript paragraph should let a later layer define a quantity that belongs to an earlier layer.

## Phase Range

- Phase 001: Canonical v2 plan and rebuild ledger baseline — Steps 1-18
- Phase 002: Source evidence recertification and reference-only boundary — Steps 19-50
- Phase 003: Failure analysis and salvage/reject inventory — Steps 51-84
- Phase 004: Manuscript scope, audience, and architecture contract — Steps 85-120
- Phase 005: Notation and equation dependency contract — Steps 121-160
- Phase 006: Chapter 1 mathematical foundation package — Steps 161-220
- Phase 007: refs. 6/7 closure method package — Steps 221-270
- Phase 008: Direct solver, approximation, and validation protocol — Steps 271-325
- Phase 009: Fitting strategy and identifiability protocol — Steps 326-385
- Phase 010: Chapter 2-5 interface and expansion skeleton — Steps 386-435
- Phase 011: Blank LaTeX manuscript assembly — Steps 436-515
- Phase 012: Review pass 1, structural/evidence audit — Steps 516-565
- Phase 013: Review pass 2, mathematical/physical audit — Steps 566-625
- Phase 014: Review pass 3, build/syntax/handover gate — Steps 626-675

## Non-goals

- Do not overwrite either original `.tex` source file.
- Do not overwrite the user's 2017 JCP PDF.
- Do not modify `D:\Projects\Project_Anode_Fit\Claude`.
- Do not modify prior phase result files except by creating new supersession or addendum files.
- Do not patch `graphite_ica_chapter1_development_draft.tex`.
- Do not use the existing draft as the body skeleton of the new manuscript.
- Do not copy old ver5 prose wholesale.
- Do not copy corrected ver1 prose wholesale.
- Do not put phase, audit, change-history, ledger, or Codex-process notes into manuscript body text.
- Do not present `V_OCV(q,T)` as a primary input curve for dynamic states.
- Do not collapse `V_n`, `V_app`, and `V_drive`.
- Do not use `Q_n(q)` or internal modeled storage as the ICA/DVA capacity axis unless explicitly contrasted with `Q_ext`.
- Do not treat refs. 6/7 physical diffusion/recombination assumptions as graphite assumptions.
- Do not call the graphite exact formulation Fredholm unless a later phase explicitly reformulates a global boundary-value problem and records the derivation.
- Do not claim numerical validity of a closure method without a direct root-solve benchmark.
- Do not allow heat, kinetic polarization, or hysteresis terms to absorb charge-balance residual failures.
- Do not proceed from architecture to LaTeX drafting until the notation and equation dependency contracts pass.

## Implementation Changes

Planned new files:

- `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`
- `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.json`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_EXECUTION_LEDGER.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_001_PLAN_BASELINE_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_002_SOURCE_EVIDENCE_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_SOURCE_EVIDENCE_INDEX.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_003_FAILURE_ANALYSIS_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_SALVAGE_REJECT_INVENTORY.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_004_ARCHITECTURE_CONTRACT_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_MANUSCRIPT_ARCHITECTURE_CONTRACT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_005_NOTATION_DEPENDENCY_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_NOTATION_BIBLE.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_EQUATION_DEPENDENCY_DAG.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_006_CHAPTER1_MATH_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_CHAPTER1_MATH_PACKAGE.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_007_REF_CLOSURE_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_REF6_REF7_CLOSURE_CONTRACT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_008_SOLVER_VALIDATION_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_SOLVER_VALIDATION_PROTOCOL.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_009_FITTING_IDENTIFIABILITY_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_FITTING_IDENTIFIABILITY_PROTOCOL.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_010_CHAPTER_INTERFACES_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_CHAPTER2_5_INTERFACE_CONTRACT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_rebuilt_manuscript_v1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_011_DRAFT_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_012_REVIEW_PASS1_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_013_REVIEW_PASS2_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_014_FINAL_HANDOVER.md`

Planned updated files:

- `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_EXECUTION_LEDGER.md`

Historical files to keep unmodified:

- `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_development_draft.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_007_EXECUTION_LEDGER.md`
- all prior `PHASE_*` result files unless a future user explicitly asks to revise them.

## Phase 001 — Canonical v2 Plan And Rebuild Ledger Baseline

1. Save this v2 canonical plan at `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`.
2. Save companion JSON metadata at `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.json`.
3. Record in the plan summary that v2 supersedes the earlier from-scratch rebuild plan for execution detail.
4. Confirm that the earlier plan remains historical context and is not edited.
5. Create `REBUILD_V2_EXECUTION_LEDGER.md`.
6. Ledger columns must include `Phase`, `Plan Steps`, `Status`, `Canonical Report`, `Machine Artifact`, `Gate Result`, `Next Step`, `Stop Condition`.
7. Add planned rows for Phase 001 through Phase 014.
8. Add a handover chain row pointing to the prior Phase 001-007 ledger and handover.
9. Add a handover chain row pointing to this v2 canonical plan.
10. Record active project, Codex workspace, source folder, and Claude boundary.
11. Record that no source `.tex` or PDF file is modified by planning.
12. Run file existence check for the v2 plan markdown.
13. Run JSON parse check for the companion JSON metadata.
14. Run file existence check for `REBUILD_V2_EXECUTION_LEDGER.md`.
15. Save `REBUILD_V2_PHASE_001_PLAN_BASELINE_RESULT.md`.
16. Update `REBUILD_V2_EXECUTION_LEDGER.md` with Phase 001 result.
17. Gate Phase 001 with `PASS_REBUILD_V2_PLAN_BASELINE` only if plan markdown exists, JSON parses, and ledger has Phase 001-014 planned rows.
18. Stop if the plan file or ledger cannot be saved under `Codex\plans` / `Codex\results`.

Outputs:

- v2 canonical plan markdown.
- v2 canonical plan JSON.
- rebuild v2 execution ledger.
- Phase 001 baseline result.

## Phase 002 — Source Evidence Recertification And Reference-Only Boundary

19. Re-open `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_007_EXECUTION_LEDGER.md`.
20. Re-open `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_007_ANODE_DQDV_HANDOVER.md`.
21. Re-open `D:\Projects\Project_Anode_Fit\Codex\results\ver5_chapter_structure_map.md`.
22. Re-open `D:\Projects\Project_Anode_Fit\Codex\results\ver1_charge_balance_dependency_graph.md`.
23. Re-open `D:\Projects\Project_Anode_Fit\Codex\results\ref6_ref7_method_notes.md`.
24. Re-open `D:\Projects\Project_Anode_Fit\Codex\results\self_consistent_variable_mapping.md`.
25. Re-open `D:\Projects\Project_Anode_Fit\Codex\results\chapter1_rewrite_spec.md`.
26. Re-open `D:\Projects\Project_Anode_Fit\Codex\results\2026-05-27-rebuild-readiness-assessment-report.md`.
27. Confirm `graphite_ica_dynamic_ver5.tex` exists in the source folder.
28. Confirm `graphite_ica_charge_balance_ver1_rechecked2.tex` exists in the source folder.
29. Confirm the JCP 147, 144111 PDF exists in the source folder.
30. Record line count and byte size for both `.tex` files.
31. Record parser page count and byte size for the PDF.
32. Reconfirm that ver5 READ_FULL coverage was recorded as lines 1-1974.
33. Reconfirm that corrected ver1 READ_FULL coverage was recorded as lines 1-495.
34. Reconfirm that PDF READ_FULL_TEXT coverage was recorded as pages 1-10.
35. Create `REBUILD_V2_SOURCE_EVIDENCE_INDEX.md` with columns `Source`, `Claim`, `Evidence File`, `Evidence Range`, `Confidence`, `Reuse Permission`.
36. Add every confirmed source claim needed for the rebuild.
37. Add every source claim that remains `미검증`.
38. Add every source claim that remains `근거 미발견`.
39. Mark `graphite_ica_chapter1_development_draft.tex` as reference sketch only.
40. Mark the earlier from-scratch plan as superseded planning context only.
41. Mark old ver5 prose as architecture evidence only, not body text.
42. Mark corrected ver1 equations as mathematical evidence, not prose to copy wholesale.
43. Mark the 2017 PDF's extracted text as citation/method evidence with equation-glyph caution.
44. Record that full refs. 6/7 papers are not yet READ_FULL.
45. Record that no source files are modified in this phase.
46. Save `REBUILD_V2_PHASE_002_SOURCE_EVIDENCE_RESULT.md`.
47. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
48. Gate Phase 002 with `PASS_REBUILD_V2_SOURCE_EVIDENCE` only if every planned source has an evidence-index row.
49. Stop if any mandatory source file is missing.
50. Stop if the evidence index cannot distinguish `확정`, `추정`, `미검증`, and `근거 미발견`.

Outputs:

- `REBUILD_V2_SOURCE_EVIDENCE_INDEX.md`
- `REBUILD_V2_PHASE_002_SOURCE_EVIDENCE_RESULT.md`

## Phase 003 — Failure Analysis And Salvage/Reject Inventory

51. Open `graphite_ica_chapter1_development_draft.tex` as a reference-only sketch.
52. Read the draft from line 1 to end and record exact line coverage.
53. Identify draft elements that are technically correct and reusable as ideas.
54. Identify draft elements that are too skeletal for the rebuilt manuscript.
55. Identify draft elements that should not be reused because they are scaffolding prose.
56. Identify old ver5 Chapter 1 ideas that are superseded by corrected ver1.
57. Identify old ver5 Chapter 2 ideas that remain useful only as heat-layer interface context.
58. Identify old ver5 Chapter 3 ideas that remain useful only as kinetic-interface context.
59. Identify old ver5 Chapter 4 ideas that remain useful only as fitting-system context.
60. Identify old ver5 Chapter 5 ideas that remain useful only as hysteresis/memory context.
61. Identify corrected ver1 equations that must be retained in the new manuscript.
62. Identify corrected ver1 equations that must be rewritten for dependency order.
63. Identify corrected ver1 statements that risk implying `V_n` is prescribed.
64. Identify corrected ver1 statements that correctly distinguish `V_n`, `V_app`, and `V_drive`.
65. Identify corrected ver1 statements that correctly use `Q_ext`.
66. Identify places where `Q_bg` must be treated as storage, not cosmetic baseline.
67. Identify all symbol-collision risks known so far.
68. Identify all physical-overreach risks from refs. 6/7.
69. Create `REBUILD_V2_SALVAGE_REJECT_INVENTORY.md`.
70. Inventory columns must include `Source`, `Item`, `Use As-Is?`, `Reuse As Idea?`, `Reject?`, `Reason`, `Required Rewrite`.
71. Add `Retain`, `Rewrite`, `Reject`, and `Defer` categories.
72. Add a section for "must not appear in final manuscript body."
73. Add a section for "requires user decision before final wording."
74. Add a section for "requires numerical validation before claim."
75. Add a section for "requires full refs. 6/7 read before stronger claim."
76. Save `REBUILD_V2_PHASE_003_FAILURE_ANALYSIS_RESULT.md`.
77. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
78. Gate Phase 003 with `PASS_REBUILD_V2_FAILURE_ANALYSIS` only if every prior artifact is classified as evidence, idea, reject, or defer.
79. Stop if the inventory attempts to use the old draft as a manuscript base.
80. Stop if the inventory allows old `V_OCV(q,T)` logic to survive as a primary dynamic voltage input.
81. Stop if any rejected item is still planned for direct manuscript insertion.
82. Stop if a required rewrite item has no destination phase.
83. Proceed only if the salvage inventory makes a blank rewrite feasible.
84. Record the exact next phase entry condition in the ledger.

Outputs:

- `REBUILD_V2_SALVAGE_REJECT_INVENTORY.md`
- `REBUILD_V2_PHASE_003_FAILURE_ANALYSIS_RESULT.md`

## Phase 004 — Manuscript Scope, Audience, And Architecture Contract

85. Decide default scope if user has not specified: write a full master skeleton with Chapter 1 fully developed and Chapter 2-5 as controlled interfaces.
86. Record alternative scope options and their impact:
  `Chapter 1 only`, `Chapter 1 full + Chapter 2-5 skeleton`, `full Chapter 1-5`.
87. Decide default language if user has not specified: Korean explanatory prose with standard mathematical notation and English citation titles.
88. Record alternative language options and their impact.
89. Define target reader: battery-data modeler who needs to fit LIB graphite ICA/DVA without inheriting the old circular logic.
90. Define manuscript promise in one paragraph.
91. Define manuscript non-promise in one paragraph.
92. Create a top-level table of contents from blank structure.
93. Assign each chapter a single owner concept.
94. Define Chapter 1 owner concept: charge-balance thermodynamic foundation.
95. Define Chapter 2 owner concept: heat/temperature coupling interface.
96. Define Chapter 3 owner concept: kinetic/overpotential interface.
97. Define Chapter 4 owner concept: fitting/state/observation system.
98. Define Chapter 5 owner concept: hysteresis/branch/memory extension.
99. Define appendix candidates: numerical solver, notation table, source comparison, ref closure derivation.
100. Define what evidence can be cited in each chapter.
101. Define what must remain in results/audit files rather than manuscript body.
102. Define planned figure/table captions only, not fake generated data.
103. Define where the self-consistent loop is first introduced.
104. Define where it is solved exactly.
105. Define where the approximate closure is introduced.
106. Define where fitting validation appears.
107. Create `REBUILD_V2_MANUSCRIPT_ARCHITECTURE_CONTRACT.md`.
108. Include a `Reader Path` section showing how a reader moves from data coordinate to fitting validation.
109. Include a `Chapter Dependency` section showing no later chapter defines earlier variables.
110. Include a `Decision Boundary` section listing user decisions before final polish.
111. Save `REBUILD_V2_PHASE_004_ARCHITECTURE_CONTRACT_RESULT.md`.
112. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
113. Gate Phase 004 with `PASS_REBUILD_V2_ARCHITECTURE`.
114. Gate requires top-level TOC, chapter owner concepts, non-goals, and appendix policy.
115. Stop if the architecture cannot be read without knowing old ver1-ver5 history.
116. Stop if Chapter 2-5 content is allowed to overwrite Chapter 1 charge balance.
117. Stop if the architecture places refs. 6/7 closure before exact formulation.
118. Proceed only if every planned manuscript section has an evidence source or is explicitly a new synthesis section.
119. Record unresolved scope/language decisions in the result file.
120. Record that execution may continue using defaults unless the user overrides them.

Outputs:

- `REBUILD_V2_MANUSCRIPT_ARCHITECTURE_CONTRACT.md`
- `REBUILD_V2_PHASE_004_ARCHITECTURE_CONTRACT_RESULT.md`

## Phase 005 — Notation And Equation Dependency Contract

121. Create `REBUILD_V2_NOTATION_BIBLE.md`.
122. Create `REBUILD_V2_EQUATION_DEPENDENCY_DAG.md`.
123. Define all measured variables before model variables.
124. Define `Q_ext`.
125. Define `Q_cell`.
126. Define `q=Q_ext/Q_cell`.
127. Define current `I` and sign convention.
128. Define temperature `T`.
129. Define internal state vector `xi`.
130. Define equilibrium occupancy `xi_eq(V,T)` using a dummy voltage `V`.
131. Define background storage `Q_bg(V,T)`.
132. Define transition capacities `Q_j,tot`.
133. Define transition centers `U_j(T)`.
134. Define transition widths `w_j(T)`.
135. Define dimensionless capacity fraction `a_j=Q_j,tot/Q_cell`.
136. Reserve `w_j` only for voltage width.
137. Define charge-balance residual `G(V;q,T,xi,theta)`.
138. Define root operator `mathcal V(q,T,xi;theta)`.
139. Define `V_n` only as the solved root.
140. Define `V_OCV` only as equilibrium special root.
141. Define `V_app`.
142. Define `V_drive`.
143. Define affinity `A_j`.
144. Define kinetic rate `k_j`.
145. Define `dxi/dt`.
146. Define `dxi/dq` only under nonzero current.
147. Define rest relaxation separately.
148. Define `dV_n/dq`.
149. Define `dV_app/dq`.
150. Define ICA observable `dQ_ext/dV_app`.
151. Define DVA observable `dV_app/dQ_ext`.
152. Build dependency DAG with each equation's prerequisites.
153. Add `Forbidden Reordering` section.
154. Add `Symbol Collision` section.
155. Add `Allowed Synonyms` section if Korean/English terminology differs.
156. Save `REBUILD_V2_PHASE_005_NOTATION_DEPENDENCY_RESULT.md`.
157. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
158. Gate Phase 005 with `PASS_REBUILD_V2_NOTATION_DEPENDENCY`.
159. Stop if any equation uses `V_n` before root operator definition.
160. Stop if any notation table entry has no role or unit/domain.

Outputs:

- `REBUILD_V2_NOTATION_BIBLE.md`
- `REBUILD_V2_EQUATION_DEPENDENCY_DAG.md`
- `REBUILD_V2_PHASE_005_NOTATION_DEPENDENCY_RESULT.md`

## Phase 006 — Chapter 1 Mathematical Foundation Package

161. Create `REBUILD_V2_CHAPTER1_MATH_PACKAGE.md`.
162. Write the Chapter 1 problem statement in manuscript-ready prose.
163. State why an OCV-input-only formulation is insufficient.
164. Define measured charge coordinate.
165. Define analysis interval and endpoint convention.
166. Define transition state variables.
167. Define equilibrium occupancy functions.
168. Define charge-balance residual.
169. Define root existence interval.
170. Define slope floor.
171. Define uniqueness or branch-selection rule.
172. Define internal potential root.
173. Define equilibrium OCV special case.
174. Define total capacity consistency.
175. Define apparent voltage.
176. Define driving voltage.
177. Define kinetic interface without expanding full Chapter 3.
178. Define time-domain state equation.
179. Define q-domain state equation.
180. Define Volterra integral form.
181. State exact self-consistency loop.
182. Define rest relaxation at fixed q.
183. Define derivative of charge balance in general thermal case.
184. Define isothermal simplification.
185. Define apparent voltage derivative.
186. Define ICA.
187. Define DVA.
188. Define monotonicity condition.
189. Define denominator-singularity warning.
190. Define validation residuals for Chapter 1.
191. Add a subsection explaining `Q_bg` as storage, not cosmetic baseline.
192. Add a subsection explaining why `V_OCV` is derived, not fitted first.
193. Add a subsection explaining exact vs approximate formulation.
194. Add a `Manuscript Equations To Insert` table.
195. Add a `Manuscript Claims Allowed` table.
196. Add a `Manuscript Claims Forbidden` table.
197. Add a `Requires Later Chapter` table.
198. Cross-check every equation against `REBUILD_V2_EQUATION_DEPENDENCY_DAG.md`.
199. Cross-check every notation entry against `REBUILD_V2_NOTATION_BIBLE.md`.
200. Cross-check every retained concept against `REBUILD_V2_SOURCE_EVIDENCE_INDEX.md`.
201. Record whether the package is Chapter 1-ready.
202. Save `REBUILD_V2_PHASE_006_CHAPTER1_MATH_RESULT.md`.
203. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
204. Gate Phase 006 with `PASS_REBUILD_V2_CHAPTER1_MATH`.
205. Gate requires charge balance, OCV special case, DAE/Volterra form, and ICA/DVA derivation.
206. Stop if the package introduces `V_OCV` before charge balance.
207. Stop if the package treats `Q_bg` as a visual baseline only.
208. Stop if the package allows kinetics to change charge conservation.
209. Stop if the package cannot state how `V_n` is solved.
210. Stop if the package cannot state when q-domain dynamics are invalid.
211. Proceed only if Chapter 1 can be written without importing Chapter 2-5 content.
212. Record all open mathematical risks.
213. Record all open physical risks.
214. Record all open notation risks.
215. Record all items needing user decision.
216. Record exact equations not yet visually verified.
217. Record exact source references for the central equation.
218. Record exact source references for final ICA/DVA equations.
219. Record exact source references for rest relaxation.
220. Record exact source references for voltage distinctions.

Outputs:

- `REBUILD_V2_CHAPTER1_MATH_PACKAGE.md`
- `REBUILD_V2_PHASE_006_CHAPTER1_MATH_RESULT.md`

## Phase 007 — refs. 6/7 Closure Method Package

221. Create `REBUILD_V2_REF6_REF7_CLOSURE_CONTRACT.md`.
222. Re-open `ref6_ref7_method_notes.md`.
223. Re-open the 2017 PDF extraction evidence if needed.
224. Record exact local evidence for where refs. 6/7 are cited in the 2017 paper.
225. Record exact bibliographic entries for refs. 6 and 7.
226. Record that full original refs. 6/7 papers are not yet READ_FULL unless retrieved later.
227. Define the source method pattern from the 2017 paper:
  integral equation, formal ratio expression, reference ratio, closed approximation, numerical validation.
228. Define the graphite exact problem to which a closure may be applied.
229. Define why the graphite exact problem is not literally the same physical problem.
230. Define the direct DAE/root-solve path as the primary truth model.
231. Define quasi-equilibrium reference path.
232. Define low-rate direct-solve reference path.
233. Define frozen-feedback reference path.
234. Define criteria for choosing a default reference path.
235. Define correction functional `C_j(q)`.
236. Define acceptable dimensions and normalization for `C_j(q)`.
237. Define denominator safety if a ratio is used.
238. Define fallback to additive residual correction if ratio is ill-conditioned.
239. Define closure residual against direct solve.
240. Define low-rate limit check.
241. Define high-rate rejection check.
242. Define rest-relaxation compatibility check.
243. Define distributed barrier compatibility check if `rho_j(g)` is later used.
244. Define manuscript wording for "inspired by refs. 6/7" that avoids overclaiming.
245. Define manuscript wording for "not a direct physical import."
246. Define citation policy for 2017 paper, ref. 6, and ref. 7.
247. Define condition under which full original refs. 6/7 must be retrieved.
248. Add table `Portable Method Parts`.
249. Add table `Non-Portable Assumptions`.
250. Add table `Closure Acceptance Gates`.
251. Add table `Closure Rejection Conditions`.
252. Add table `Manuscript Claims Allowed`.
253. Add table `Manuscript Claims Forbidden`.
254. Cross-check against Phase 006 exact formulation.
255. Save `REBUILD_V2_PHASE_007_REF_CLOSURE_RESULT.md`.
256. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
257. Gate Phase 007 with `PASS_REBUILD_V2_REF_CLOSURE`.
258. Gate requires explicit separation between exact system and approximate closure.
259. Gate requires every refs. 6/7 claim to point to local PDF evidence or external metadata.
260. Gate requires all non-portable physical assumptions to be listed.
261. Stop if closure is written as exact graphite theory.
262. Stop if graphite is labeled Fredholm without derivation.
263. Stop if refs. 6/7 are used to justify a physical LIB assumption.
264. Stop if no direct-solver comparison is planned.
265. Proceed only if closure can be placed after exact formulation in the manuscript.
266. Record open issue if full refs. 6/7 papers are still unread.
267. Record open issue if exact equation glyphs remain visually unverified.
268. Record open issue if the closure correction functional remains only schematic.
269. Record user decision needed if stronger literature claim is desired.
270. Record next-phase dependency on solver validation protocol.

Outputs:

- `REBUILD_V2_REF6_REF7_CLOSURE_CONTRACT.md`
- `REBUILD_V2_PHASE_007_REF_CLOSURE_RESULT.md`

## Phase 008 — Direct Solver, Approximation, And Validation Protocol

271. Create `REBUILD_V2_SOLVER_VALIDATION_PROTOCOL.md`.
272. Define exact solver objective: compute `V_n(q_i)` and `xi(q_i)` consistently.
273. Define input arrays: `q_i`, `T_i`, `I_i`, initial `xi_0`, parameter vector `theta`.
274. Define charge-balance root solve at node `i`.
275. Define root bracket strategy.
276. Define root failure reporting.
277. Define slope-floor check.
278. Define state update strategy in time domain.
279. Define state update strategy in q domain for nonzero current.
280. Define rest update strategy at fixed q.
281. Define derivative evaluation after state/root solve.
282. Define direct DAE/root-solve pseudocode.
283. Define quasi-equilibrium reference solver pseudocode.
284. Define frozen-feedback reference solver pseudocode.
285. Define closure approximation pseudocode.
286. Define residuals:
  charge balance, state bounds, derivative denominator, capacity closure, closure mismatch.
287. Define numerical tolerances as named variables, not hard-coded final values.
288. Define tolerance default proposal:
  charge residual normalized by `Q_cell`, root bracket residual, state bound tolerance, derivative singularity threshold.
289. Define validation table format.
290. Define synthetic smoke-test scenario with one transition and monotone `Q_bg`.
291. Define expected qualitative result for the smoke test.
292. Define what counts as solver pass.
293. Define what counts as solver warning.
294. Define what counts as solver failure.
295. Define manuscript-level algorithm block.
296. Define result artifact shape for future numerical implementation.
297. Define minimal command if a future Python solver is created.
298. Define that no code implementation is required in this manuscript rebuild unless user separately requests it.
299. Define how to report "algorithm specified, not executed."
300. Define relationship between solver protocol and fitting protocol.
301. Cross-check solver protocol against Phase 006 equations.
302. Cross-check solver protocol against Phase 007 closure contract.
303. Save `REBUILD_V2_PHASE_008_SOLVER_VALIDATION_RESULT.md`.
304. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
305. Gate Phase 008 with `PASS_REBUILD_V2_SOLVER_VALIDATION`.
306. Gate requires direct solver pseudocode, reference solver pseudocode, residual definitions, and failure modes.
307. Stop if solver order evaluates `k_j` before solving `V_n`.
308. Stop if q-domain update is used during rest.
309. Stop if closure approximation lacks comparison to direct solve.
310. Stop if validation criteria do not include charge-balance residual.
311. Stop if validation criteria do not include state bounds.
312. Stop if validation criteria do not include denominator safety for ICA.
313. Proceed only if solver protocol can be described in manuscript without pretending implementation was run.
314. Record open issue if no numerical code exists.
315. Record open issue if no experimental dataset exists.
316. Record open issue if tolerance values need empirical calibration.
317. Record user decision if implementation should be added as an appendix.
318. Record user decision if synthetic examples should be generated.
319. Record source evidence links for each solver equation.
320. Record new synthesis status for solver algorithm itself.
321. Record no-source-modification check.
322. Record no-Claude-modification check.
323. Record all commands run.
324. Record all commands not run and why.
325. Record next-phase dependency on identifiability protocol.

Outputs:

- `REBUILD_V2_SOLVER_VALIDATION_PROTOCOL.md`
- `REBUILD_V2_PHASE_008_SOLVER_VALIDATION_RESULT.md`

## Phase 009 — Fitting Strategy And Identifiability Protocol

326. Create `REBUILD_V2_FITTING_IDENTIFIABILITY_PROTOCOL.md`.
327. Define fitting purpose: estimate thermodynamic/dynamic parameters while preserving charge balance.
328. Define data prerequisites:
  voltage path, current/time, capacity axis, temperature, dQ/dV or raw V-Q data.
329. Define preprocessing assumptions.
330. Define Stage 0: unit normalization and sign convention.
331. Define Stage 1: low-rate thermodynamic baseline.
332. Define Stage 2: charge-balance residual and capacity closure.
333. Define Stage 3: transition centers/widths/capacities.
334. Define Stage 4: kinetic lag parameters.
335. Define Stage 5: apparent resistance/polarization `R_n`.
336. Define Stage 6: thermal correction, only if temperature data or model exists.
337. Define Stage 7: hysteresis/memory, only after previous residuals fail.
338. Define parameter group `theta_thermo`.
339. Define parameter group `theta_storage`.
340. Define parameter group `theta_kinetic`.
341. Define parameter group `theta_observation`.
342. Define parameter group `theta_thermal`.
343. Define parameter group `theta_hysteresis`.
344. Define which groups are fixed, constrained, regularized, or free in each stage.
345. Define degeneracy `Q_bg` vs `Q_j,tot`.
346. Define degeneracy `U_j` vs voltage offset.
347. Define degeneracy `w_j` vs kinetic broadening.
348. Define degeneracy `R_n` vs `k_j`.
349. Define degeneracy heat shift vs kinetic lag.
350. Define degeneracy hysteresis vs thermodynamic asymmetry.
351. Define residual terms:
  voltage residual, ICA residual, DVA residual, charge residual, smoothness penalty, parameter prior.
352. Define objective function schematic.
353. Define constraints:
  state bounds, capacity closure, slope floor, monotonicity, root range, denominator safety.
354. Define staged acceptance criteria.
355. Define rejection criteria.
356. Define reporting table for each fitting stage.
357. Define how to report unidentifiable parameters.
358. Define how to report fixed parameters.
359. Define how to report parameters deferred to later chapters.
360. Define how to avoid using later chapters to patch Chapter 1 failure.
361. Define manuscript section outline for fitting.
362. Define appendix candidate for future implementation.
363. Cross-check against Phase 008 solver protocol.
364. Cross-check against Phase 010 chapter interfaces when available; if Phase 010 not yet complete, mark as forward dependency.
365. Save `REBUILD_V2_PHASE_009_FITTING_IDENTIFIABILITY_RESULT.md`.
366. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
367. Gate Phase 009 with `PASS_REBUILD_V2_FITTING_IDENTIFIABILITY`.
368. Gate requires staged fit order, parameter groups, degeneracy table, residual table, and rejection rules.
369. Stop if `R_n` and `k_j` are both freely fitted in the same stage without constraints.
370. Stop if `Q_bg` can absorb arbitrary peak area without capacity closure.
371. Stop if hysteresis is allowed before thermodynamic residuals are diagnosed.
372. Stop if the protocol lacks a direct-solver comparison.
373. Proceed only if the fitting section can be written as a protocol, not as a claimed completed fit.
374. Record open issue if no dataset exists.
375. Record open issue if no implementation exists.
376. Record open issue if parameter priors require user/domain input.
377. Record user decision if actual data fitting is desired next.
378. Record source evidence for every parameter family.
379. Record synthesis status for every new fitting rule.
380. Record no-source-modification check.
381. Record no-Claude-modification check.
382. Record all validation commands.
383. Record all commands not run and why.
384. Record next phase dependency on Chapter 2-5 interface boundaries.
385. Record any unresolved notation conflict.

Outputs:

- `REBUILD_V2_FITTING_IDENTIFIABILITY_PROTOCOL.md`
- `REBUILD_V2_PHASE_009_FITTING_IDENTIFIABILITY_RESULT.md`

## Phase 010 — Chapter 2-5 Interface And Expansion Skeleton

386. Create `REBUILD_V2_CHAPTER2_5_INTERFACE_CONTRACT.md`.
387. Define Chapter 2 heat interface inputs from Chapter 1.
388. Define Chapter 2 heat interface outputs back to Chapter 1 or later fitting.
389. Define that Chapter 2 uses `dxi/dt` for heat, not only `dxi/dq`.
390. Define Chapter 2 stop condition if temperature model is absent.
391. Define Chapter 3 kinetic interface inputs.
392. Define Chapter 3 kinetic outputs.
393. Define Chapter 3 separation between `V_drive`, `V_app`, and `V_n`.
394. Define Chapter 3 stop condition if BV expansion would double-count `R_n`.
395. Define Chapter 4 fitting-system inputs.
396. Define Chapter 4 fitting-system outputs.
397. Define Chapter 4 hard residual gates inherited from Chapter 1.
398. Define Chapter 4 stop condition if optimizer can violate charge balance silently.
399. Define Chapter 5 hysteresis/memory inputs.
400. Define Chapter 5 outputs.
401. Define Chapter 5 allowed modulation targets.
402. Define Chapter 5 forbidden modulation targets.
403. Define Chapter 5 stop condition if hysteresis breaks charge conservation.
404. Define cross-chapter dataflow diagram in text table form.
405. Define chapter-level artifact table.
406. Define which chapters are fully drafted in the first rebuild.
407. Define which chapters remain skeletons.
408. Define per-chapter "ready to expand" criteria.
409. Define per-chapter "do not expand yet" criteria.
410. Define how historical ver2-ver5 evidence maps into each chapter.
411. Define how to cite or reference old ver5 without copying body text.
412. Define manuscript wording for "later chapter interface."
413. Define appendix policy for deferred equations.
414. Define chapter interface validation table.
415. Save `REBUILD_V2_PHASE_010_CHAPTER_INTERFACES_RESULT.md`.
416. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
417. Gate Phase 010 with `PASS_REBUILD_V2_CHAPTER_INTERFACES`.
418. Gate requires input/output/stop condition for Chapters 2-5.
419. Stop if any later chapter redefines `V_n`.
420. Stop if Chapter 5 can bypass charge-balance residual checks.
421. Stop if Chapter 2 heat consumes q-rate where time-rate is required.
422. Stop if Chapter 3 kinetic terms and `R_n` are unconstrained duplicates.
423. Proceed only if Chapter 1 can stand as a valid foundation alone.
424. Record open interface risks.
425. Record user decisions needed before expanding Chapter 2-5 bodies.
426. Record source evidence links for each chapter interface.
427. Record synthesis status for each new interface rule.
428. Record no-source-modification check.
429. Record no-Claude-modification check.
430. Record all validation commands.
431. Record all commands not run and why.
432. Record next phase dependency on LaTeX manuscript assembly.
433. Record final architecture selected for draft.
434. Record manuscript table of contents final for Phase 011.
435. Record all deferred chapters in the ledger.

Outputs:

- `REBUILD_V2_CHAPTER2_5_INTERFACE_CONTRACT.md`
- `REBUILD_V2_PHASE_010_CHAPTER_INTERFACES_RESULT.md`

## Phase 011 — Blank LaTeX Manuscript Assembly

436. Confirm `graphite_ica_rebuilt_manuscript_v1.tex` does not exist or is explicitly a new target.
437. If the target exists from an interrupted run, stop and create a superseding filename instead of overwriting without review.
438. Create the new LaTeX file from a blank file.
439. Add minimal preamble based on source documents but without copying old title metadata.
440. Add notation macros only after checking `REBUILD_V2_NOTATION_BIBLE.md`.
441. Add title that does not include ver-history language.
442. Add abstract or summary paragraph.
443. Add table of contents if the document is standalone.
444. Add Introduction section from Phase 004 architecture.
445. Add Problem Statement section.
446. Add Measured Coordinate section.
447. Add Notation and State Variables section.
448. Add Charge Balance section.
449. Add Internal Potential Root section.
450. Add Equilibrium OCV section.
451. Add Voltage Role Distinction section.
452. Add Exact Self-Consistent Dynamics section.
453. Add Volterra Integral Form section.
454. Add Direct Solver Definition section.
455. Add Reference Closure section.
456. Add ICA/DVA Observable Derivation section.
457. Add Validation Residuals section.
458. Add Fitting Protocol section.
459. Add Chapter 2-5 Interface section.
460. Add Limitations section.
461. Add Bibliography.
462. Insert only verified DOI entries.
463. Insert note if full refs. 6/7 papers remain unread, but keep that note in result file unless manuscript limitation wording is appropriate.
464. Do not insert Codex phase or audit notes into body.
465. Do not insert old draft paragraphs wholesale.
466. Do not insert old ver5 paragraphs wholesale.
467. Use new prose for every explanatory paragraph.
468. Use equations from Phase 006 package where allowed.
469. Use closure language from Phase 007 package where allowed.
470. Use fitting language from Phase 009 package where allowed.
471. Use interface language from Phase 010 package where allowed.
472. Add labels to all numbered equations.
473. Add references only to labels that exist.
474. Check macro definitions for collisions.
475. Check for raw `ver.1`, `ver.2`, `Phase`, `audit`, and `change history` strings in manuscript body.
476. Check for `V_OCV` before charge-balance definition.
477. Check for `V_n` use before root definition.
478. Check for `Q_n(q)` as observable axis.
479. Check for `Q_ext` observable axis.
480. Check for `V_app`/`V_drive` collapse.
481. Check for `w_j` misuse as capacity fraction.
482. Check for `R_n`/`k_j` free co-fit statement.
483. Check for refs. 6/7 overclaim.
484. Check for unsupported numerical validation claims.
485. Run label/reference scan.
486. Run brace balance scan.
487. Run forbidden body word scan.
488. If LaTeX engine exists, run build.
489. If LaTeX engine does not exist, record build limitation.
490. Save all validation outputs in Phase 011 result.
491. Save `REBUILD_V2_PHASE_011_DRAFT_RESULT.md`.
492. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
493. Gate Phase 011 with `PASS_REBUILD_V2_DRAFT`.
494. Gate requires new manuscript file, no old body copy, dependency order checks, and citation checks.
495. Stop if target manuscript overwrites an existing file without explicit supersession.
496. Stop if forbidden phase/audit wording appears in manuscript body.
497. Stop if `V_n` is used before root definition.
498. Stop if refs. 6/7 are described as direct graphite physics.
499. Stop if the manuscript claims a numerical fit was performed.
500. Stop if LaTeX syntax checks fail and cannot be repaired within scope.
501. Stop if a build failure indicates missing package only and user wants environment setup before continuing.
502. Proceed only if the draft is internally coherent enough for review passes.
503. Record exact manuscript line count.
504. Record exact labels count.
505. Record exact references count.
506. Record missing references count.
507. Record brace balance result.
508. Record forbidden-word scan result.
509. Record build result or build limitation.
510. Record source files not modified.
511. Record Claude files not modified.
512. Record git status.
513. Record all open issues.
514. Record next phase entry condition.
515. Record whether user review is recommended before further expansion.

Outputs:

- `graphite_ica_rebuilt_manuscript_v1.tex`
- `REBUILD_V2_PHASE_011_DRAFT_RESULT.md`

## Phase 012 — Review Pass 1, Structural/Evidence Audit

516. Read the new manuscript from line 1 to end.
517. Record line coverage.
518. Check manuscript section order against Phase 004 architecture.
519. Check manuscript notation against Phase 005 notation bible.
520. Check manuscript equations against Phase 006 math package.
521. Check closure section against Phase 007 closure contract.
522. Check solver/validation section against Phase 008 protocol.
523. Check fitting section against Phase 009 protocol.
524. Check Chapter 2-5 interfaces against Phase 010 contract.
525. Create evidence trace table from manuscript claims to source/result artifacts.
526. Mark claims with direct source evidence.
527. Mark claims that are new synthesis.
528. Mark claims that are unsupported.
529. Mark claims that require user decision.
530. Mark claims that require numerical implementation.
531. Mark claims that require full refs. 6/7 read.
532. Check that body text does not mention phase/audit process.
533. Check that old draft text was not copied wholesale.
534. Check that old source prose was not copied wholesale.
535. Create `REBUILD_V2_PHASE_012_REVIEW_PASS1_RESULT.md`.
536. Include findings table with severity, file line, issue, required action.
537. If structural issues are found, repair only the new manuscript.
538. If evidence issues are found, either add evidence trace or weaken the claim.
539. If unsupported claims are not repairable, remove or mark as limitation.
540. Rerun targeted structural scans after repairs.
541. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
542. Gate Phase 012 with `PASS_REBUILD_V2_REVIEW_PASS1`.
543. Gate requires no unsupported core claims.
544. Gate requires all synthesis claims labeled as synthesis in result file.
545. Gate requires no source/body-copy issue.
546. Stop if old draft copying is detected.
547. Stop if a core claim cannot be traced or weakened.
548. Stop if architecture mismatch requires user decision.
549. Stop if manuscript scope exceeds Phase 004 decision.
550. Proceed only if structure and evidence are coherent.
551. Record exact repairs made.
552. Record exact files modified.
553. Record commands run.
554. Record commands not run and why.
555. Record source files not modified.
556. Record Claude files not modified.
557. Record open issues.
558. Record next phase entry condition.
559. Record whether any user decision is required before pass 2.
560. If user decision is required, stop and present decision packet.
561. If no user decision is required, proceed to pass 2.
562. Keep all rejected findings in result file.
563. Keep all false-positive findings with evidence.
564. Update ledger gate.
565. Record handover chain.

Outputs:

- `REBUILD_V2_PHASE_012_REVIEW_PASS1_RESULT.md`

## Phase 013 — Review Pass 2, Mathematical/Physical Audit

566. Read the current manuscript from line 1 to end after pass 1 repairs.
567. Record line coverage.
568. Audit dimensions of all equations where units are declared.
569. Audit sign conventions for `q`, `I`, `s_I`, and `s_phi`.
570. Audit charge-balance residual definition.
571. Audit equilibrium OCV definition.
572. Audit state equation time-domain form.
573. Audit q-domain conversion.
574. Audit rest condition.
575. Audit derivative `dV_n/dq`.
576. Audit apparent voltage derivative.
577. Audit ICA/DVA reciprocal relation.
578. Audit monotonicity condition.
579. Audit slope-floor condition.
580. Audit state bounds.
581. Audit capacity closure.
582. Audit `Q_bg` role.
583. Audit `R_n`/`k_j` identifiability statement.
584. Audit heat interface `dxi/dt`.
585. Audit hysteresis interface charge-conservation constraint.
586. Audit refs. 6/7 closure language.
587. Audit no Fredholm overclaim.
588. Audit no direct physical import from geminate-pair model.
589. Audit no claim of completed fitting.
590. Create mathematical issue table.
591. Classify each issue as confirmed problem, caution, false positive, or requires user decision.
592. Repair confirmed manuscript problems within new manuscript only.
593. If repair requires changing a prior result artifact, create addendum instead of editing old result.
594. If repair requires new physics decision, stop and ask user.
595. Rerun math-related scans after repairs.
596. Save `REBUILD_V2_PHASE_013_REVIEW_PASS2_RESULT.md`.
597. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
598. Gate Phase 013 with `PASS_REBUILD_V2_REVIEW_PASS2`.
599. Gate requires no confirmed mathematical dependency error.
600. Gate requires no confirmed `V_OCV` primary-input regression.
601. Gate requires no confirmed refs. 6/7 physical-overimport.
602. Gate requires all unresolved physics decisions visible.
603. Stop if charge-balance equation is inconsistent.
604. Stop if `dV_n/dq` derivation contradicts the state equation.
605. Stop if q-domain equation is used during rest.
606. Stop if closure section hides approximation status.
607. Proceed only if manuscript is physically coherent enough for build/final review.
608. Record exact repairs made.
609. Record exact files modified.
610. Record commands run.
611. Record commands not run and why.
612. Record source files not modified.
613. Record Claude files not modified.
614. Record open issues.
615. Record next phase entry condition.
616. Record whether full refs. 6/7 read is recommended before publication.
617. Record whether numerical solver implementation is recommended before publication.
618. Record whether actual data fitting is recommended before publication.
619. Record all remaining limitations.
620. Update ledger gate.
621. Record handover chain.
622. If user decision required, stop at decision boundary.
623. If no user decision required, proceed to pass 3.
624. Preserve all issue classifications in result file.
625. Preserve all rejected fixes with rationale.

Outputs:

- `REBUILD_V2_PHASE_013_REVIEW_PASS2_RESULT.md`

## Phase 014 — Review Pass 3, Build/Syntax/Handover Gate

626. Read the current manuscript from line 1 to end after pass 2 repairs.
627. Record line coverage.
628. Run file existence check for every planned artifact.
629. Run label/reference scan.
630. Run brace balance scan.
631. Run forbidden body word scan.
632. Run notation token scan for `V_n`, `V_{n,\app}`, `V_{n,\drive}`, `Q_{\ext}`, `Q_{\bg}`, `w_j`, `a_j`.
633. Run citation token scan for 2017 paper, ref. 6, and ref. 7.
634. Run build engine discovery:
  `where.exe pdflatex`, `where.exe xelatex`, `where.exe lualatex`.
635. If `xelatex` is available, build with `xelatex -interaction=nonstopmode -halt-on-error`.
636. If only `pdflatex` is available and Korean text is present, record that `kotex` compatibility must be verified before trusting build.
637. If no engine is available, record build limitation and do not claim PDF build pass.
638. If build is run, inspect log for undefined references.
639. If build is run, inspect log for overfull boxes at warning level.
640. If build is run, record PDF output path.
641. Confirm original source `.tex` files unchanged.
642. Confirm source PDF unchanged.
643. Confirm Claude folder unchanged by Codex.
644. Run project git status.
645. Create final artifact list.
646. Create final source coverage table.
647. Create final confirmed decisions table.
648. Create final open issues table.
649. Create final `근거 미발견` table.
650. Create final user decision queue.
651. Create `REBUILD_V2_PHASE_014_FINAL_HANDOVER.md`.
652. Update `REBUILD_V2_EXECUTION_LEDGER.md`.
653. Gate Phase 014 with `PASS_REBUILD_V2_HANDOVER` if all previous gates pass and build/syntax status is explicit.
654. Gate may be `PASS_REBUILD_V2_HANDOVER_WITH_BUILD_LIMITATION` if no LaTeX engine is available but syntax scans pass.
655. Stop if any planned phase result file is missing.
656. Stop if manuscript target file is missing.
657. Stop if syntax scans fail.
658. Stop if source files were modified.
659. Stop if Claude files were modified.
660. Stop if build fails due manuscript syntax that can be repaired within scope; repair and rerun.
661. Stop for user decision if build fails due missing environment/package.
662. Stop for user decision if final manuscript scope differs from Phase 004.
663. Stop for user decision if full refs. 6/7 read is required before stronger claims.
664. Stop for user decision if numerical solver must be implemented before acceptance.
665. Prepare final user-facing summary.
666. Include exact paths to manuscript, plan, ledger, and handover.
667. Include exact build/syntax status.
668. Include exact open issues.
669. Include recommended next action.
670. Do not commit unless user asks.
671. Do not push unless user asks.
672. Preserve all phase result files.
673. Preserve all validation commands and outputs.
674. Close ledger.
675. End at user review boundary.

Outputs:

- `REBUILD_V2_PHASE_014_FINAL_HANDOVER.md`
- updated `REBUILD_V2_EXECUTION_LEDGER.md`

## Implementation Interfaces

### Rebuild Ledger Row Shape

```markdown
| Phase | Plan Steps | Status | Canonical Report | Machine Artifact | Gate Result | Next Step | Stop Condition |
|---|---:|---|---|---|---|---:|---|
| Phase 001 - plan baseline | 1-18 | PLANNED | `...` | `...` | PENDING | 19 | plan/ledger save failure |
```

### Source Evidence Index Shape

```markdown
| Source | Claim | Evidence File | Evidence Range | Confidence | Reuse Permission |
|---|---|---|---|---|---|
| `graphite_ica_charge_balance_ver1_rechecked2.tex` | `V_n` is solved from charge balance | `ver1_charge_balance_dependency_graph.md` | lines 121-129 cited there | 확정 | equation idea only |
```

### Salvage / Reject Inventory Shape

```markdown
| Source | Item | Use As-Is? | Reuse As Idea? | Reject? | Reason | Required Rewrite |
|---|---|---|---|---|---|---|
| old draft | Reference-closure paragraph | no | yes | no | useful but too skeletal | rewrite after exact DAE definition |
```

### Equation Dependency Record Shape

```markdown
| Equation ID | Equation Role | Requires Defined First | Defines | May Be Used By | Failure If Reordered |
|---|---|---|---|---|---|
| E-CB-001 | charge-balance residual | `q`, `Q_cell`, `Q_bg`, `Q_j,tot`, `xi_j` | `G(V;...)` | root operator | circular `V_n` use |
```

### Notation Bible Row Shape

```markdown
| Symbol | Role | Unit / Domain | Defined In | Forbidden Use | Notes |
|---|---|---|---|---|---|
| `V_n` | solved internal graphite potential | V | root operator section | prescribed OCV input | solve before kinetics |
```

### Manuscript Section Contract Shape

```markdown
| Section | Purpose | Inputs From Previous Sections | Equations Introduced | Claims Allowed | Claims Forbidden |
|---|---|---|---|---|---|
| Charge Balance | define internal potential root | measured coordinate, states | `G=0`, `V_n=mathcal V(...)` | `V_n` solved | `V_n` read from OCV |
```

### Validation Finding Shape

```markdown
| ID | Severity | File | Line | Finding | Evidence | Required Action | Status |
|---|---:|---|---:|---|---|---|---|
| RV2-P2-001 | 2 | `graphite_ica_rebuilt_manuscript_v1.tex` | 0 | example | evidence | action | open |
```

## Test Plan

File and artifact checks:

- `Test-Path` for every planned created file.
- `Get-Item` size/time check for source files.
- line count check for generated LaTeX manuscript.
- `git status --short` scoped to project root.

JSON checks:

- parse v2 companion plan JSON.
- if any later JSON artifacts are created, parse every JSON artifact before gate.

Text scans:

- forbidden body terms:
  `Phase`, `phase`, `audit`, `Audit`, `change history`, `PHASE_`, `ver.1`, `ver.2`, `ver.3`, `ver.4`, `ver.5` inside manuscript body.
- dependency order indicators:
  `V_{n,\OCV}` before charge-balance root section;
  `V_n` before root operator;
  `Q_n(q)` as observable capacity axis.
- notation collision indicators:
  `w_j` used outside transition-width context;
  missing `a_j` if dimensionless capacity fraction is needed.

LaTeX checks:

- label/reference scan: all `\eqref{...}` and `\ref{...}` point to labels.
- brace balance scan.
- macro collision scan for new commands.
- engine discovery:
  `where.exe pdflatex`, `where.exe xelatex`, `where.exe lualatex`.
- build only if an engine exists and required packages are available.

Scientific checks:

- `V_n` is solved by charge balance before kinetics or derivatives.
- `V_OCV` is only equilibrium special root.
- `Q_ext=Q_cell q` remains the ICA/DVA axis.
- `Q_bg` is storage, not cosmetic baseline.
- q-domain dynamics are not used during rest.
- closure method is clearly approximate unless direct solve is used.
- refs. 6/7 are not physically over-imported.
- `R_n` and `k_j` co-fit risk is stated and constrained.
- later chapters cannot violate charge-balance residual gates.

Review pass checks:

- Pass 1: structure/evidence.
- Pass 2: mathematical/physical consistency.
- Pass 3: syntax/build/handover.

## Assumptions

- The user wants a new manuscript, not a patched old draft.
- The new manuscript is stored under `Codex\results` until user asks to promote it elsewhere.
- The default manuscript scope is Chapter 1 fully developed with Chapter 2-5 controlled skeletons unless the user overrides it.
- The default language is Korean explanatory prose with standard mathematical notation unless the user overrides it.
- Previous READ_FULL records are valid recovery anchors, but execution must reopen the relevant result files before using them.
- Full original refs. 6/7 papers are not mandatory for cautious closure-language drafting, but are mandatory for stronger derivation claims.
- No numerical solver implementation is part of this rewrite unless the user separately requests implementation.
- No git commit is made unless the user requests it.

## Correction History

- v1 from-scratch plan created a broad phase outline but lacked RO_SkillDict-level contractual detail.
- User rejected v1 as too shallow and requested a plan at the reference project's level of detail.
- v2 adds cumulative step numbering, artifact contracts, pass gates, stop conditions, validation interfaces, review passes, and explicit non-goals.
