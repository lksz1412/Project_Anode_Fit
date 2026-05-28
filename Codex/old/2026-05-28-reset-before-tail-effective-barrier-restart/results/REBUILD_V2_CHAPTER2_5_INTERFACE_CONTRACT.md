# Rebuild v2 Chapter 2-5 Interface Contract

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 010 - Chapter 2-5 Interface And Expansion Skeleton`

Created: 2026-05-27

## Contract Role

This contract fixes how Chapters 2-5 may extend the Chapter 1 charge-balance foundation. It does not fully derive heat, kinetics, fitting, or hysteresis. The selected architecture for the first rebuilt manuscript remains:

**Chapter 1 fully drafted + Chapter 2-5 controlled skeletons.**

Chapter 1 must stand alone as the valid thermodynamic and self-consistent foundation.

## Non-Negotiable Inherited Definitions

| Definition | Owner | Later Chapter Rule |
|---|---|---|
| measured charge `Q_ext`, `q` | Chapter 1 | cannot be redefined |
| internal states `xi_j` | Chapter 1 | may be extended only by declared additional states |
| background storage `Q_bg` | Chapter 1 | may receive temperature dependence but remains storage |
| charge-balance residual `G` | Chapter 1 | cannot be bypassed |
| internal potential `V_n` | Chapter 1 | always root-solved from charge balance |
| apparent voltage `V_app` / `V_{n,app}` | Chapter 1 / observation interface | may be refined only as observation mapping |
| driving voltage `V_drive` / `V_{n,drive}` | Chapter 1 / kinetic interface | may be refined only in kinetic chapter |
| direct solver validation | Phase 008 / Chapter 4 | required before fitting or closure claims |

## Chapter 2 Heat / Temperature Interface

### Inputs From Chapter 1

| Input | Required Form | Note |
|---|---|---|
| `T(t)` or `T(q)` | measured path or model state | Chapter 1 treats as input until heat model exists |
| `V_n(t)` | root-solved internal potential | must come from charge balance |
| `V_{n,app}(t)` | apparent voltage | observation voltage for heat terms if needed |
| `xi_j(t)` | internal states | state trajectory from direct solver |
| `dxi_j/dt` | time-domain transition rates | heat uses time rates, not only q-rates |
| `I(t)` | current with sign convention | irreversible/ohmic heat if modeled |

### Outputs

| Output | Allowed Use |
|---|---|
| updated or modeled `T(t)` | feed back as input to Chapter 1 equations only through declared temperature coupling |
| heat-generation terms | downstream thermal analysis and fitting residuals |
| thermal parameter constraints | Phase 009/Chapter 4 fitting protocol |

### Stop Condition

Stop Chapter 2 expansion if no temperature data, thermal boundary model, or declared isothermal assumption exists. Do not invent heat equations to patch voltage residuals.

### Required Guard

Chapter 2 must use `dxi_j/dt` for transition heat. It cannot use only `dxi_j/dq` because rest relaxation and time-dependent heat require time-domain rates.

## Chapter 3 Kinetic / Overpotential Interface

### Inputs

| Input | Required Form | Note |
|---|---|---|
| `V_n` | root-solved internal potential | not prescribed |
| `V_{n,app}` | apparent voltage | observation-side quantity |
| `V_{n,drive}` | declared kinetic driving voltage | must remain distinct from `V_n` and `V_app` |
| `U_j(T)` | transition center | from thermodynamic parameter group |
| `xi_j`, `xi_{j,eq}` | states and equilibrium target | from Chapter 1 |
| `I`, `T`, `q` | measured/model inputs | used only after root solve |

### Outputs

| Output | Allowed Use |
|---|---|
| refined `k_j` | update state dynamics |
| kinetic affinity `A_j` | explain rate/overpotential relation |
| kinetic parameter constraints | Phase 009/Chapter 4 fitting |

### Required Separation

`V_n`, `V_{n,app}`, and `V_{n,drive}` must remain separate. Chapter 3 may define a modeling choice such as \(V_{n,\mathrm{drive}}\approx V_{n,\mathrm{app}}\), but only if it records the approximation and fitting consequence.

### Stop Condition

Stop Chapter 3 expansion if Butler-Volmer or overpotential terms would double-count the same dynamic shift already assigned to `R_n`. The fitting protocol must decide whether kinetic lag or observation resistance is active/free in a given stage.

## Chapter 4 Fitting / State / Observation System Interface

### Inputs

| Input | Source |
|---|---|
| direct solver trajectory | Phase 008 protocol |
| parameter groups | Phase 009 protocol |
| residual definitions | Phase 008-009 |
| voltage/ICA/DVA observables | Chapter 1 |
| Chapter 2 thermal terms | only if validated |
| Chapter 3 kinetic terms | only if not duplicating `R_n` |
| Chapter 5 hysteresis terms | only after residual diagnosis |

### Outputs

| Output | Allowed Use |
|---|---|
| fitted parameter report | only after data and solver implementation exist |
| residual/gate report | document pass/warning/fail |
| unidentifiable parameter report | fix, constrain, defer, or request new data |
| model comparison report | compare baseline, kinetic, thermal, hysteresis variants |

### Hard Residual Gates Inherited From Chapter 1

- charge-balance residual;
- root range;
- slope floor or conditioning rule;
- state bounds;
- capacity closure;
- q-domain/rest validity;
- ICA/DVA denominator safety;
- direct-solver comparison for closure.

### Stop Condition

Stop Chapter 4 expansion if the optimizer can silently violate charge balance, clip `V_n`, update states during rest using q-domain equations, or fit derivative peaks while raw voltage residual fails.

## Chapter 5 Hysteresis / Branch / Memory Interface

### Inputs

| Input | Required Form |
|---|---|
| charge/discharge branch labels | measured or declared |
| residual diagnosis from Chapters 1-4 | required before memory terms |
| `q`, `T`, `xi_j`, `V_n` | inherited from Chapter 1 |
| direct solver results | baseline trajectory |
| fitting residuals | evidence that non-memory model is insufficient |

### Outputs

| Output | Allowed Use |
|---|---|
| memory state variables | modulate allowed quantities only |
| branch-dependent corrections | explain residuals after baseline failure |
| hysteresis parameter report | must include identifiability warning |

### Allowed Modulation Targets

Chapter 5 may modulate:

- transition centers \(U_j\) through a declared memory state;
- kinetic rates \(k_j\) through path-dependent lag;
- apparent voltage mapping through constrained observation terms;
- reference path selection for closure, if validated.

### Forbidden Modulation Targets

Chapter 5 may not:

- bypass or remove the charge-balance residual;
- redefine \(Q_{\mathrm{ext}}\), \(q\), or \(Q_{\mathrm{cell}}\);
- prescribe \(V_n\) independently;
- use hysteresis to hide failed capacity closure;
- use memory states without reporting identifiability risk.

### Stop Condition

Stop Chapter 5 expansion if hysteresis breaks charge conservation, bypasses root-solved \(V_n\), or is introduced before thermodynamic/dynamic residuals are diagnosed.

## Cross-Chapter Dataflow

| From | To | Data | Rule |
|---|---|---|---|
| Chapter 1 | Chapter 2 | `T`, `V_n`, `V_app`, `xi_j`, `dxi_j/dt`, `I` | heat consumes time rates |
| Chapter 1 | Chapter 3 | `V_n`, `V_app`, `V_drive`, `xi_j`, `xi_eq`, `U_j` | kinetics follows root solve |
| Chapter 1 | Chapter 4 | equations, observables, residual gates | fitting cannot violate charge balance |
| Chapter 2 | Chapter 4 | thermal parameters/residuals | only if temperature model/data exist |
| Chapter 3 | Chapter 4 | kinetic parameters/residuals | no unconstrained duplicate with `R_n` |
| Chapter 4 | Chapter 5 | residual diagnosis | memory only after baseline failure |
| Chapter 5 | Chapter 4 | memory-state parameters | fit with identifiability warning |

## Chapter-Level Artifact Table

| Chapter | First Rebuild Status | Canonical Artifact |
|---|---|---|
| Chapter 1 | fully drafted in Phase 011 | final LaTeX body from Phase 006 math package |
| Chapter 2 | skeleton only | interface section plus deferred equations appendix note |
| Chapter 3 | skeleton only | interface section plus kinetic guard |
| Chapter 4 | skeleton only | fitting protocol summary from Phase 009 |
| Chapter 5 | skeleton only | hysteresis boundary and stop conditions |

## Ready-To-Expand Criteria

| Chapter | Ready To Expand When |
|---|---|
| Chapter 2 | temperature data/model and heat equation scope are available |
| Chapter 3 | kinetic law choice and `R_n`/kinetic identifiability control are settled |
| Chapter 4 | direct solver exists and data/fitting target are selected |
| Chapter 5 | baseline residual diagnosis shows memory/hysteresis is needed |

## Do-Not-Expand-Yet Criteria

| Chapter | Do Not Expand If |
|---|---|
| Chapter 2 | no temperature model/data or only voltage residual patching motivation exists |
| Chapter 3 | BV/overpotential terms duplicate `R_n` |
| Chapter 4 | optimizer can bypass residual gates or no solver exists |
| Chapter 5 | hysteresis is being used before thermodynamic/kinetic residual diagnosis |

## Historical ver2-ver5 Mapping

| Historical Layer | New Chapter Mapping | Allowed Use |
|---|---|---|
| ver2 heat layer | Chapter 2 | interface direction only |
| ver3 kinetics layer | Chapter 3 | interface direction only |
| ver4 integrated fitting layer | Chapter 4 | architecture direction only |
| ver5 hysteresis layer | Chapter 5 | future extension direction only |

Old ver5 may be referenced only as project history or architecture evidence in results files. The final manuscript must not copy old ver5 body text or require the reader to know old version history.

## Manuscript Wording For Later-Chapter Interface

Allowed wording:

> The following chapters are written as controlled interfaces in the first rebuild. They specify what later heat, kinetic, fitting, and hysteresis models may consume from Chapter 1, and which definitions they may not alter.

Allowed wording:

> Chapter 1 remains the owner of charge balance and the root-solved internal potential. Later chapters may add coupling terms or observation models only through this interface.

Forbidden wording:

- "Chapter 2 redefines the temperature-dependent charge balance."
- "Chapter 3 replaces \(V_n\) with overpotential."
- "Chapter 5 corrects charge balance through hysteresis."

## Appendix Policy For Deferred Equations

Deferred equations may be placed in appendices only if they are clearly labeled as:

- interface candidate;
- not validated;
- not part of the Chapter 1 foundation;
- requiring later data/model gates.

No appendix may silently introduce a primary variable that the main text depends on.

## Interface Validation Table

| Gate | Required Result |
|---|---|
| Chapter 2 input/output/stop condition | PASS |
| Chapter 3 input/output/stop condition | PASS |
| Chapter 4 input/output/stop condition | PASS |
| Chapter 5 input/output/stop condition | PASS |
| no later chapter redefines `V_n` | PASS |
| Chapter 5 cannot bypass charge balance | PASS |
| Chapter 2 uses `dxi/dt` where heat needs time rate | PASS |
| Chapter 3 and `R_n` duplicate shift control | constrained by Phase 009 |
| Chapter 1 stands alone | PASS |

## Open Interface Risks

- Heat feedback can make \(T\) a dynamic state; Chapter 1 currently treats \(T\) as input.
- Kinetic overpotential and apparent resistance remain a high-risk identifiability pair.
- Fitting system implementation does not yet exist.
- Hysteresis can overfit residuals if introduced too early.
- Chapter 2-5 skeletons must stay visibly subordinate to Chapter 1 in Phase 011.

## User Decisions Needed Before Expanding Chapter 2-5 Bodies

| Decision | Default Until Decided |
|---|---|
| whether to fully derive heat equations | keep Chapter 2 skeleton only |
| whether to use Butler-Volmer or another kinetic law | keep Chapter 3 interface only |
| whether to implement actual fitting code | keep Chapter 4 protocol only |
| whether to model hysteresis now | keep Chapter 5 skeleton only |
| whether old ver2-ver5 history should appear in final manuscript | omit from body; keep in results |

These are not blocking decisions for Phase 011 because the selected architecture uses skeletons.

## Source Evidence Links

| Interface | Source Evidence |
|---|---|
| Chapter 2 heat | corrected ver1 lines 462-471; ver5 heat layer lines 525-852 as architecture evidence |
| Chapter 3 kinetics | corrected ver1 lines 203-286; ver5 kinetic layer lines 855-1118 as architecture evidence |
| Chapter 4 fitting | Phase 008 solver protocol; Phase 009 fitting protocol; ver5 integrated layer lines 1122-1516 as architecture evidence |
| Chapter 5 hysteresis | Phase 009 degeneracy controls; ver5 hysteresis layer lines 1520-1974 as architecture evidence |

## Synthesis Status

| Rule | Status |
|---|---|
| later chapters cannot redefine `V_n` | direct continuation of Phase 005-006 |
| heat must consume `dxi/dt` | source-supported and interface formalized |
| Chapter 3 cannot duplicate `R_n` | Phase 009 risk formalized |
| fitting cannot bypass charge balance | Phase 008-009 synthesis |
| hysteresis only after residual diagnosis | synthesis from identifiability risk |

## Commands Not Run

| Command / Action | Reason |
|---|---|
| heat model derivation | skeleton/interface phase only |
| kinetic BV derivation | skeleton/interface phase only |
| fitting implementation | no solver/data yet |
| hysteresis simulation | deferred |
| LaTeX build | Phase 011 not yet assembled |

## Phase 011 Table Of Contents

The Phase 011 manuscript should use:

1. Introduction and problem statement
2. Measured charge coordinate
3. Storage and internal states
4. Charge balance and root-solved \(V_n\)
5. Equilibrium OCV as special root
6. Apparent/driving voltages and kinetic interface
7. Self-consistent dynamics and exact solver
8. Reference-closure strategy
9. Derivative observables and validation gates
10. Chapter 2 heat interface skeleton
11. Chapter 3 kinetic interface skeleton
12. Chapter 4 fitting/interface skeleton
13. Chapter 5 hysteresis/interface skeleton
14. Appendices / deferred derivations

## Gate Statement

Gate: `PASS_REBUILD_V2_CHAPTER_INTERFACES`

This contract passes because Chapters 2-5 each have inputs, outputs, stop conditions, expansion criteria, source links, and hard boundaries preventing redefinition of Chapter 1 charge balance.
