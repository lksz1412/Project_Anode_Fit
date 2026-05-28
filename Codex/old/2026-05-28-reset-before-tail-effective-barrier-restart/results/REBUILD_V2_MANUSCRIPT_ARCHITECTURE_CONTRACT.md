# Rebuild v2 Manuscript Architecture Contract

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 004 - Manuscript Scope, Audience, And Architecture Contract`

Created: 2026-05-27

## Default Scope

Unless the user overrides it, the rebuild target is:

**Chapter 1 fully developed + Chapter 2-5 controlled skeleton.**

This means Chapter 1 will contain the complete thermodynamic charge-balance foundation, self-consistent formulation, exact-solve baseline, derivative-observable logic, and cautious closure-method entry point. Chapters 2-5 will not be fully derived yet; they will be written as controlled interfaces that consume Chapter 1 variables without redefining them.

## Alternative Scope Options

| Option | What It Produces | Benefit | Cost / Risk |
|---|---|---|---|
| Chapter 1 only | A complete first chapter with no later-chapter skeleton | Fastest path to fixing the logical core | Later chapters may drift unless interfaces are separately documented |
| Chapter 1 full + Chapter 2-5 skeleton | Complete Chapter 1 plus controlled downstream chapter map | Best balance for this project because ver5's intended trajectory is preserved without inheriting old errors | Requires careful boundary language so skeletons do not overclaim |
| Full Chapter 1-5 | Full manuscript across heat, kinetics, fitting, hysteresis | Most complete eventual document | Too risky before solver, validation, identifiability, and refs. 6/7 gates are complete |

Default: **Chapter 1 full + Chapter 2-5 skeleton**.

## Default Language

Unless the user overrides it, the rebuilt manuscript uses Korean explanatory prose with standard mathematical notation and English citation titles. This matches the user's working language while preserving scientific notation and bibliographic clarity.

| Option | Impact |
|---|---|
| Korean prose + standard math + English citation titles | Best fit for current collaboration and technical review |
| English manuscript prose | Better for direct journal-style drafting, slower for user review |
| Korean/English bilingual notes | Useful for transition, but risks bloated manuscript body |

Default: **Korean prose with standard mathematical notation and English citation titles**.

## Target Reader

The target reader is a battery-data modeler who needs to fit LIB graphite ICA/DVA shapes from a thermodynamic and self-consistent charge-balance basis without inheriting the old circular logic. The reader may know ICA/DVA and graphite staging qualitatively, but should not need to know the project's old ver1-ver5 history to understand the rebuilt manuscript.

## Manuscript Promise

The manuscript promises to define a graphite-anode ICA/DVA fitting framework in which the internal graphite potential is solved from charge balance, not prescribed as an external OCV input. It will show how measured charge, background storage, staging variables, equilibrium occupancy, dynamic relaxation, and derivative observables fit into one dependency-ordered formulation. It will also define how refs. 6/7 can be used as a mathematical closure strategy for a self-consistent integral problem, while keeping the direct root-solve formulation as the baseline.

## Manuscript Non-Promise

The manuscript does not promise validated fitted parameters, dataset-specific performance, completed heat generation theory, complete Butler-Volmer kinetics, or a fully validated hysteresis model until later phase gates provide those artifacts. It also does not claim that refs. 6/7 physically describe graphite staging; they only supply a transferable closure pattern after the graphite-specific exact formulation is defined.

## Top-Level Table Of Contents

### Front Matter

- Title
- Abstract or project summary
- Notation snapshot

### Chapter 1. Thermodynamic Charge-Balance Foundation For Graphite ICA/DVA

Owner concept: **charge-balance thermodynamic foundation**.

Planned sections:

1. Problem statement and modeling target
2. Measured external charge coordinate: `Q_ext`, `Q_cell`, `q`
3. Storage decomposition: `Q_bg(V,T)` and staging capacities
4. Internal progress variables and equilibrium occupancy
5. Charge-balance residual and root operator for `V_n`
6. Equilibrium OCV as a derived special case
7. Apparent and driving voltages: `V_n`, `V_{n,app}`, `V_{n,drive}`
8. Self-consistent dynamics in time and charge coordinates
9. Exact direct root-solve formulation
10. Reference-closure strategy adapted from refs. 6/7
11. Derivative observables: `dV/dq`, ICA, DVA
12. Chapter 1 validation gates
13. Interface handoff to later chapters

### Chapter 2. Heat / Temperature Coupling Interface

Owner concept: **temperature and heat-coupling interface**.

This chapter may consume `T`, `V_n`, `V_{n,app}`, `xi_j`, and `dxi_j/dt`. It may not redefine charge balance or use a different voltage root.

### Chapter 3. Kinetic / Overpotential Interface

Owner concept: **kinetic and overpotential interface**.

This chapter may introduce `V_{n,drive}`, affinity, and kinetic rate refinements. It may not move kinetic definitions before the Chapter 1 root solve.

### Chapter 4. Fitting, State, And Observation System

Owner concept: **fitting/state/observation system**.

This chapter may assemble residuals, constraints, observables, numerical protocols, and identifiability controls. It must preserve the Chapter 1 dependency graph and explicitly constrain `R_n`/kinetic double-counting risk.

### Chapter 5. Hysteresis / Branch / Memory Extension

Owner concept: **hysteresis and memory extension**.

This chapter may introduce branch states, structural memory, or hysteresis. It must preserve the charge-balance residual and voltage-role separation.

### Appendices

Candidates:

- Appendix A: notation table and units
- Appendix B: equation dependency DAG
- Appendix C: direct root-solve and integration pseudocode
- Appendix D: reference-closure derivation and refs. 6/7 comparison
- Appendix E: source comparison and rejected-history notes
- Appendix F: numerical validation checklist

Appendix E must remain factual and concise if included. Process logs, phase gates, and AI handover records remain in `Codex\results`, not in the manuscript body.

## Evidence Allowed By Chapter

| Manuscript Area | Allowed Evidence | New Synthesis Allowed? | Blocked Claims |
|---|---|---:|---|
| Chapter 1 sections 1-9 | corrected ver1 dependency graph, Phase 002 evidence index, Phase 003 inventory | yes | Old ver5 OCV-primary logic |
| Chapter 1 section 10 | refs. 6/7 notes, self-consistent mapping, user paper PDF metadata | yes, cautiously | Full original-paper derivation claims until refs. 6/7 are `READ_FULL` |
| Chapter 1 sections 11-13 | corrected ver1 derivative/interface material, Phase 003 inventory | yes | Completed validation or fitting performance |
| Chapter 2 | ver5 heat-layer map, integration notes | yes | Full heat derivation unless separately validated |
| Chapter 3 | ver5 kinetic-layer map, voltage-role inventory | yes | Butler-Volmer or kinetic details that redefine `V_n` |
| Chapter 4 | fitting/interface notes, identifiability risk inventory | yes | Unconstrained parameter co-fit or dataset performance |
| Chapter 5 | ver5 hysteresis layer as direction only | yes | Validated hysteresis claims |
| Appendices | notation contract, DAG, solver protocol, closure contract, evidence logs | yes | Raw phase history in body text |

## Reader Path

1. The reader starts with measured data coordinates: current, external charge, normalized charge, and temperature.
2. The reader sees graphite storage decomposed into background storage and staging progress variables.
3. The reader learns that `V_n` is an implicit root of charge balance.
4. Equilibrium OCV is introduced only as a special equilibrium root, not as the primary dynamic input.
5. Apparent and driving voltages are separated before any kinetic or observable formula.
6. The state dynamics are written with `V_n` already defined as a root-solved quantity.
7. The self-consistent loop is recognized explicitly.
8. The direct root-solve integration becomes the exact baseline.
9. The refs. 6/7-style closure is introduced as an approximation strategy relative to a reference path.
10. Derivative observables and ICA/DVA are defined after the state/root dependency is fixed.
11. Fitting and validation are introduced only after the mathematical dependencies are closed.

## Chapter Dependency Rules

| Dependency | Rule |
|---|---|
| Chapter 1 to all later chapters | Later chapters must consume Chapter 1 variables and cannot redefine charge balance. |
| Chapter 2 | May add temperature evolution, but `T` enters Chapter 1 equations as an input until heat coupling is explicitly solved. |
| Chapter 3 | May refine `k_j` and `V_{n,drive}`, but must not compute rates before `V_n` exists. |
| Chapter 4 | May fit parameters and observations, but must preserve the equation dependency DAG. |
| Chapter 5 | May add memory states, but must preserve `Q_ext`, `q`, `V_n`, `V_{n,app}`, and `V_{n,drive}` meanings. |
| Appendices | May expand derivations or algorithms, but must not introduce new primary definitions that the main chapters rely on without reference. |

## Placement Of Critical Logic

| Logic Item | First Introduced | Exact / Approximate Handling |
|---|---|---|
| Self-consistent feedback loop | Chapter 1 section 8 | Stated after root operator and voltage roles |
| Exact direct solution | Chapter 1 section 9; optional Appendix C | Direct root solve at each state update is the baseline |
| Approximate closure | Chapter 1 section 10; detailed in Appendix D | Introduced only after exact formulation |
| Fitting validation | Chapter 4; optional Appendix F | No performance claim before numerical evidence |

## Planned Figures And Tables

These are captions/placeholders only. No generated or fake data should be inserted.

| Item | Caption Intent | Evidence / Status |
|---|---|---|
| Figure 1 | Dependency path from measured charge to root-solved `V_n` to ICA/DVA | New synthesis from corrected ver1 |
| Figure 2 | Self-consistent loop among `xi_j`, charge balance, `V_n`, and rates | New synthesis from dependency graph |
| Figure 3 | Direct solver versus reference-closure concept | New synthesis; needs Phase 007-008 |
| Table 1 | Notation and units | Phase 005 output |
| Table 2 | Equation dependency DAG | Phase 005 output |
| Table 3 | Chapter 2-5 interface variables | Phase 010 output |
| Table 4 | Validation gates | Phase 008-009 output |

## What Must Stay In Results / Audit Files

- Phase numbers, gate labels, execution ledger rows, and handover chain.
- Detailed source-read coverage tables unless they are converted into concise methods notes.
- Old ver1-ver5 project history except a brief source-context statement if user wants it.
- Rejected item inventories and internal process notes.
- Unverified exact equations from PDF extraction.
- Claims marked `근거 미발견` or `미검증` in the source evidence index.

## Decision Boundary

| Decision | Default | User Override Impact |
|---|---|---|
| Scope | Chapter 1 full + Chapter 2-5 skeleton | Can narrow to Chapter 1 only or broaden to full Chapter 1-5 |
| Language | Korean prose, standard math notation, English citation titles | Can switch final manuscript to English or bilingual notes |
| refs. 6/7 positioning | Cautious method-pattern positioning | Can become stronger only after full refs. 6/7 read |
| Pseudocode inclusion | Keep in appendix/protocol until approved | Can move into main text if user wants a method-heavy manuscript |
| Source-history visibility | Keep old history out of main body | Can add a concise appendix/source note if needed |
| Chapter 2-5 depth | Interface skeleton only | Can expand after Chapter 1 and protocols are stable |

Execution may continue using these defaults unless the user overrides them.

## Architecture Gate

Gate: `PASS_REBUILD_V2_ARCHITECTURE`

This contract passes only if:

- The manuscript can be understood without knowing the old ver1-ver5 history.
- Chapter owner concepts are single and non-overlapping.
- Chapter 2-5 cannot overwrite Chapter 1 charge balance.
- refs. 6/7 closure is placed after the exact graphite formulation.
- Every planned section has an evidence source or is explicitly marked as new synthesis.
