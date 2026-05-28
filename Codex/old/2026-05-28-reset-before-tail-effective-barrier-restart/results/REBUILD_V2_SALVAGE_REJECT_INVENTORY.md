# Rebuild v2 Salvage / Rewrite / Reject Inventory

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 003 - Failure Analysis And Salvage/Reject Inventory`

Created: 2026-05-27

## Purpose

This inventory classifies every prior artifact and major idea before any new manuscript body is written. The rebuild is a blank rewrite. Prior files may supply evidence, architecture, equations, failure modes, or future interfaces, but the old draft and old ver5 prose are not manuscript bases.

## Prior Artifact Classification

| Artifact | Classification | Allowed Use | Forbidden Use |
|---|---|---|---|
| `PHASE_001_007_EXECUTION_LEDGER.md` | Retain as recovery/evidence log | Restore earlier phase trail and evidence provenance | Treat as manuscript content |
| `PHASE_007_ANODE_DQDV_HANDOVER.md` | Retain as handover context | Recover prior conclusions and remaining risks | Treat as final analysis |
| `ver5_chapter_structure_map.md` | Retain as architecture evidence | Identify intended Chapter 1-5 trajectory and old failure points | Copy old ver5 body prose |
| `ver1_charge_balance_dependency_graph.md` | Retain as primary math evidence | Define dependency order, charge balance, voltage distinctions, derivative dependencies | Copy prose wholesale without notation contract |
| `ref6_ref7_method_notes.md` | Retain with caution | Use bibliographic metadata and closure-pattern bridge | Claim full refs. 6/7 derivations were read |
| `self_consistent_variable_mapping.md` | Retain as method mapping | Classify graphite problem as self-consistent DAE/Volterra-like structure and define portable closure strategy | Import molecular-pair physics into graphite |
| `chapter1_rewrite_spec.md` | Retain as Chapter 1 role contract | Use required logical order and non-goals | Treat as final section text |
| `chapter1_to_chapter5_integration_notes.md` | Retain as future interface context | Preserve downstream chapter handoff constraints | Pull heat/kinetic/hysteresis detail into Chapter 1 |
| `graphite_ica_chapter1_development_draft.tex` | Reference sketch only | Mine line-level ideas after full read lines 1-375 | Use as manuscript base or copy body text |
| `2026-05-27-rebuild-readiness-assessment-report.md` | Retain as rebuild boundary report | Preserve “rewrite from scratch” decision and open issues | Treat readiness status as final validation |
| `2026-05-27-graphite-ica-from-scratch-rebuild-plan.md` | Superseded planning context | Understand why v2 plan was needed | Execute as canonical plan |
| `2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md` | Active canonical plan | Execute phase steps and gates | Skip gates or collapse phases |
| `REBUILD_V2_SOURCE_EVIDENCE_INDEX.md` | Active evidence boundary | Use as the source boundary for all later phases | Override without recording addendum |

## Main Inventory

| Category | Source | Item | Use As-Is? | Reuse As Idea? | Reject? | Reason | Required Rewrite |
|---|---|---|---:|---:|---:|---|---|
| Retain | corrected ver1 / draft lines 87-111 | Measured external charge coordinate `Q_ext`, normalized `q`, and time-to-charge conversion | no | yes | no | Measurement coordinate must precede internal-state equations. | Rewrite in final notation after the notation bible fixes sign conventions and units. Destination: Phase 005-006. |
| Retain | corrected ver1 / draft lines 113-137 | Internal transition states `xi_j`, equilibrium occupancy, and capacity fraction separation | no | yes | no | Graphite staging needs explicit internal states; `w_j` must remain voltage width, not capacity fraction. | Rewrite with collision-free symbols and explicit orientation convention. Destination: Phase 005-006. |
| Retain | corrected ver1 / draft lines 139-164 | Charge-balance residual and root operator for `V_n` | no | yes | no | This is the core correction: `V_n` is solved by charge conservation. | Rewrite as the first mathematical anchor of Chapter 1. Destination: Phase 006. |
| Retain | corrected ver1 / draft lines 166-186 | Equilibrium OCV as derived implicit relation | no | yes | no | Prevents old logic where OCV curve is treated as independent primary input. | Rewrite after root operator so `V_{n,OCV}` is a special case, not a starting assumption. Destination: Phase 006. |
| Retain | corrected ver1 / draft lines 188-204 | Distinction among `V_n`, `V_{n,app}`, and `V_{n,drive}` | no | yes | no | Avoids voltage-role collapse and later double-counting. | Rewrite with a notation table and explicit modeling-choice language. Destination: Phase 005-006. |
| Retain | corrected ver1 / draft lines 206-243 | Self-consistent dynamics and Volterra-like integral form | no | yes | no | Captures the feedback loop that caused the user's concern. | Rewrite in dependency order: root solve first, then rate, then state update, then integral form. Destination: Phase 006-008. |
| Retain | draft lines 245-280 | Reference-closure strategy using refs. 6/7 as a method pattern | no | yes | no | Useful direction, but currently too schematic and must not overclaim. | Rewrite only after Phase 007 formal closure contract; state that direct solve is baseline. |
| Retain | draft lines 282-320 | Derivative observables for `dV/dq`, ICA, and DVA | no | yes | no | Correct dependency: derivatives follow after state/root definitions. | Rewrite after mathematical package and solver protocol are fixed. Destination: Phase 006-008. |
| Retain | draft lines 322-338 | Validation gates | no | yes | no | Gate list is useful but not yet tied to actual solver/data. | Rewrite as protocol, not as completed validation. Destination: Phase 008-009. |
| Retain | draft lines 340-348 | Later chapter interfaces | no | yes | no | Preserves Chapter 2-5 boundaries. | Rewrite as interface contract, not full model expansion. Destination: Phase 010. |
| Rewrite | draft lines 59-85 | Purpose and scope paragraph plus central chain | no | yes | no | Direction is correct, but it reads like a development note and still compresses too many concepts. | Expand into a manuscript-quality Chapter 1 introduction with measured variables, problem statement, and no process wording. Destination: Phase 006/011. |
| Rewrite | draft lines 120-132 | Logistic equilibrium occupancy expression | no | yes | no | Needs notation audit, physical interpretation, and orientation sign explanation. | Recast after notation bible; verify `s_{\xi,j}` and `w_j` definitions. Destination: Phase 005-006. |
| Rewrite | draft lines 158-164 | Slope floor | no | yes | no | Useful numerical conditioning idea, but not fundamental thermodynamics. | Move to validation/numerical protocol; weaken wording. Destination: Phase 008. |
| Rewrite | draft lines 184-186 | Capacity normalization coupling | no | yes | no | Important, but too compressed and may affect fitting constraints. | Expand into parameter-dependency discussion with identifiability guard. Destination: Phase 009. |
| Rewrite | draft lines 201-204 | `R_n` and kinetic prefactor double-count warning | no | yes | no | Correct risk, but needs formal identifiability protocol. | Move to fitting constraints and parameter grouping. Destination: Phase 009. |
| Rewrite | old ver5 Chapter 1 | Historical OCV/staging structure | no | partial | yes for old logic | Superseded by corrected charge-balance formulation. | Extract only any useful explanatory motivation; rebuild equations from corrected ver1. Destination: Phase 003-006. |
| Rewrite | old ver5 Chapter 2 | Heat layer | no | yes | no | Useful as downstream layer only. | Convert to Chapter 2 interface: inputs `T`, `V_n`, `V_app`, `xi_j`, `dxi_j/dt`; no Chapter 1 expansion. Destination: Phase 010. |
| Rewrite | old ver5 Chapter 3 | Kinetic layer | no | yes | no | Useful as downstream kinetic interface only. | Convert to Chapter 3 interface: `V_drive`, affinity, kinetic rates; no premature BV model in Chapter 1. Destination: Phase 010. |
| Rewrite | old ver5 Chapter 4 | Integrated fitting layer | no | yes | no | Useful as architecture for residuals/constraints. | Convert to fitting-system interface after identifiability protocol. Destination: Phase 009-010. |
| Rewrite | old ver5 Chapter 5 | Hysteresis/memory layer | no | yes | no | Useful as future extension, but high identifiability risk. | Defer to controlled Chapter 5 skeleton. Destination: Phase 010-011. |
| Reject | draft lines 50-54 | `Development draft` title and draft identity | no | no | yes | Final manuscript body must not contain process/draft labels. | Replace with final manuscript title structure in Phase 011. |
| Reject | old draft as a file | Using `graphite_ica_chapter1_development_draft.tex` as the manuscript base | no | no | yes | User explicitly requested rebuilding from scratch and not fixing the old text. | Start a new LaTeX file in Phase 011 after contracts are complete. |
| Reject | old ver5 Chapter 1 | Treating `V_{n,OCV}(q,T)` as a primary dynamic voltage input | no | no | yes | This is the logical direction the rebuild must repair. | Replace with root-defined `V_n` and derived equilibrium OCV. Destination: Phase 006. |
| Reject | old ver5 / old draft risk | Collapsing `V_n`, `V_{n,app}`, and `V_{n,drive}` | no | no | yes | Causes ambiguous derivatives and kinetic double-counting. | Maintain separate voltage roles in notation bible and equations. Destination: Phase 005-006. |
| Reject | old ver5 / fitting idea | Unconstrained simultaneous fitting of `R_n` and kinetic prefactors as independent dynamic shift absorbers | no | no | yes | Identifiability failure risk. | Define staged or constrained fitting strategy. Destination: Phase 009. |
| Reject | refs. 6/7 | Importing geminate-pair diffusion physics, Smoluchowski coordinate, Coulomb pair potential, contact sink, or Onsager assumptions into graphite | no | no | yes | Those are source-domain physics, not LIB graphite thermodynamics. | Use only the reference/ratio/correction closure pattern. Destination: Phase 007. |
| Reject | PDF extraction | Transcribing exact equations from extracted text without visual/source check | no | no | yes | OCR/text extraction can distort equation glyphs and layout. | Require visual/source equation audit before exact formula use. Destination: Phase 007. |
| Reject | process records | Phase logs, gates, correction history, or handover chain inside final manuscript body | no | no | yes | User/project rule forbids body change-history/process notes. | Keep all such records in `Codex\results`. |
| Defer | numerical validation | Claims that direct root-solve integration validates closure approximation | no | no | no | No direct solver result exists yet. | Defer until solver/validation protocol and execution. Destination: Phase 008. |
| Defer | fitting performance | Any fitted parameter values, goodness-of-fit, robustness, or dataset-specific conclusion | no | no | no | No actual dataset/fitting artifact exists in rebuild chain. | Defer until fitting protocol and data are available. Destination: Phase 009 or later. |
| Defer | refs. 6/7 | Strong claims about exact derivation details in refs. 6/7 | no | no | no | Original refs. 6/7 are not yet `READ_FULL`. | Defer until full paper reads or keep as cautious method-pattern statement. Destination: Phase 007. |
| Defer | heat model | Detailed irreversible/reversible heat equations | no | yes | no | Heat belongs downstream. | Defer to Chapter 2 interface or later manuscript phase. Destination: Phase 010. |
| Defer | hysteresis | Memory state equations and hysteresis fitting | no | yes | no | Useful direction but high risk without identifiability controls. | Defer to Chapter 5 skeleton and future validation. Destination: Phase 010-011. |

## Symbol-Collision And Dependency Risks

| Risk | Status | Required Control |
|---|---|---|
| `w_j` used as voltage width versus capacity fraction | confirmed risk | Reserve `w_j` for voltage width; use `a_j` or another symbol for normalized capacity fraction. |
| `Q_n`, `Q_ext`, and `Q_cell q` conflation | confirmed risk | Use `Q_ext=Q_cell q` for measured external charge and keep electrode-storage terms separate. |
| `V_n`, `V_{n,app}`, and `V_{n,drive}` collapse | confirmed risk | Define roles before using them in rates, observables, or fitting. |
| `R_n` and kinetic prefactors both absorbing dynamic voltage shifts | confirmed risk | Add identifiability constraint or staged fitting protocol. |
| `Q_bg` treated as cosmetic baseline rather than storage term | confirmed risk | Define `Q_bg(V,T)` as a storage component in charge balance. |
| `q` used as both measured coordinate and hidden state | possible risk | Reserve `q` for normalized external charge; use `xi_j` for internal states. |
| Sign conventions `s_I`, `s_{\xi,j}`, `s_{\phi,j}` | possible risk | Fix orientation conventions in the notation bible before drafting equations. |

## Physical-Overreach Risks From Refs. 6/7

- Do not identify graphite staging with molecular geminate-pair diffusion.
- Do not import the Smoluchowski radial coordinate as a graphite coordinate.
- Do not import Coulomb pair potential, external-field pair-potential terms, contact sink, or Onsager probability as graphite assumptions.
- Do not claim refs. 6/7 directly solve the LIB charge-balance DAE.
- Do not claim the reference-closure approximation is valid before comparing it against a direct root-solve integration.

## Must Not Appear In Final Manuscript Body

- `Development draft`, phase numbers, gate labels, handover chain, correction history, or AI-process notes.
- Direct copies of old ver5 prose or the previous Chapter 1 draft body.
- Statements that treat `V_n` as externally prescribed before charge balance is solved.
- Statements that present old `V_OCV(q,T)` logic as the primary dynamic voltage input.
- Exact formulas from the 2017 PDF or refs. 6/7 that have not been visually/source verified.
- Physical assumptions from refs. 6/7 that belong to molecular-pair reaction theory rather than graphite staging.
- Numerical validation or fitting-performance claims that have not been run.

## Requires User Decision Before Final Wording

| Topic | Why User Decision Is Needed | Default Until Decided |
|---|---|---|
| Final manuscript language | User has written project instructions in Korean, but citation and technical notation may remain English. | Korean explanatory prose with standard mathematical notation and English citation titles. |
| Scope of final output | Could be Chapter 1 only, Chapter 1 plus Chapter 2-5 skeleton, or full Chapter 1-5. | Chapter 1 fully developed plus controlled Chapter 2-5 skeleton unless user narrows scope. |
| How strongly to position refs. 6/7 | User paper points to the method, but original refs. 6/7 are not yet full-read. | Cautious method-pattern positioning. |
| Whether to include implementation pseudocode | Useful for fitting, but may change manuscript style. | Keep in protocol/results notes until user approves inclusion. |

## Requires Numerical Validation Before Claim

- Accuracy of any reference-closure approximation.
- Robustness of `V_n` root solve under realistic data grids.
- Stability of `dV/dq`, ICA, and DVA denominators near flat regions.
- Identifiability of `Q_bg`, `Q_{j,tot}`, `U_j`, `w_j`, `R_n`, and kinetic parameters.
- Fit quality or parameter values for any real LIB dataset.

## Requires Full Refs. 6/7 Read Before Stronger Claim

- Any claim about exact derivation sequence in ref. 6 or ref. 7.
- Any direct equation imported from ref. 6 or ref. 7.
- Any assertion that a specific ratio/correction expression is mathematically identical to the graphite closure.
- Any comparison of approximation error bounds from refs. 6/7 to the graphite problem.

## Blank-Rewrite Entry Condition

The blank rewrite is feasible only after Phase 004-010 convert this inventory into manuscript architecture, notation, mathematical package, closure contract, solver/validation protocol, fitting protocol, and chapter-interface contract. Until then, no manuscript body file should be treated as canonical.
