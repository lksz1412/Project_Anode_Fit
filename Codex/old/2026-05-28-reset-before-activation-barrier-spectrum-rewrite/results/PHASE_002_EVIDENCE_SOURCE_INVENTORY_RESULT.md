# Phase 002 — Evidence And Source Inventory Result

## Summary

Gate result: `PASS_EVIDENCE_SCOPE`

The new Chapter 1 will not use archived Codex/ChatGPT equations as authority. The evidence basis is limited to:

- user observation and scope constraints;
- calculus/conservation for ICA/DVA and charge storage;
- transition-state/activated-rate theory for activation free energy;
- nonequilibrium electrochemical kinetics for driving-force and mobility language;
- graphite staging literature for phase-transition context;
- ICA literature for the diagnostic observable context.

## Step Range

Steps 19-55.

## Sources And Evidence Status

| Claim / Assumption | Evidence Status | Source / Basis | Allowed Use |
|---|---|---|---|
| ICA is a differential capacity observable | `DERIVED` plus literature context | Calculus; Dubarry et al. 2006 DOI `10.1149/1.2221767`; Dubarry and Ansean 2022 DOI `10.3389/fenrg.2022.1023555` | Define `dQ/dV`/`dQ/d\varphi`; do not overclaim diagnostic uniqueness |
| Graphite lithiation proceeds through staged phases / phase transitions | `LITERATURE_CONFIRMED` | Dahn 1991 DOI `10.1103/PhysRevB.44.9170`; Funabiki et al. 1999 DOI `10.1016/S0013-4686(99)00290-X` | Motivate phase-transition peak/tail language |
| Stage transformation kinetics can involve nucleation, growth, phase-boundary movement, and diffusion | `LITERATURE_CONFIRMED` | Funabiki et al. 1999 abstract and introduction | Use as warning that first-order relaxation is reduced, not microscopic universal law |
| Activated rate depends on activation free energy | `TEXTBOOK_THEORY` / `LITERATURE_CONFIRMED` | Eyring 1935 DOI `10.1063/1.1749604`; Chemical Reviews 1935 DOI `10.1021/cr60056a006` | Use active-barrier Arrhenius/Eyring form in stated regime |
| Electrochemical reaction rate depends on thermodynamic driving force and phase/order variables | `LITERATURE_CONFIRMED` | Bazant 2013 DOI `10.1021/ar300145c`; arXiv `1208.1587` | Support mobility/driving-force language and double-counting guard |
| Equilibrium target and kinetic mobility must not double count the same thermodynamic force | `DERIVED` plus `LITERATURE_CONFIRMED` | Two-state forward/backward reduction; Bazant 2013 | Require local detailed-balance or reduced-mobility caveat |
| Present potential can lower an active barrier | `REDUCED_MODEL` with electrochemical kinetics support | Work scale `F\psi`; Bazant 2013 driving-force framing | Use only in active-barrier regime and with explicit coupling coefficient |
| Barrier exhaustion must not be clipped | `DERIVED_LIMIT` | Logical consequence of active-barrier regime | Treat as exit from active-barrier approximation, not a repaired formula |

## Read Coverage / Web Evidence

| Source | Coverage |
|---|---|
| Dahn 1991 metadata page | Opened lines 77-115: title, author, journal, DOI |
| Bazant arXiv page | Opened lines 31-50: title, abstract, DOI relation |
| Funabiki et al. ScienceDirect page | Opened lines 36-58: title, DOI, abstract/introduction snippets |
| Dubarry and Ansean 2022 Frontiers page | Opened lines 1131-1139 for citation and DOI; references lines 817-820 for Dubarry 2006 |
| Dubarry et al. 2006 INL page | Opened lines 16-47, 81-93, 129-138 for title, DOI, abstract metadata |
| Eyring evidence | Search result confirmed DOI `10.1063/1.1749604`; ACS Chem. Rev. DOI `10.1021/cr60056a006` |

## Deferred / Not Used As Authority

| Source | Status |
|---|---|
| Archived Codex drafts | `DO_NOT_USE_AS_AUTHORITY`; may be hazard record only |
| ChatGPT ch1-ch6 final TeX | `DO_NOT_USE_AS_AUTHORITY`; may be hazard record only |
| User JCP 2017 paper ref. 6/7 | `DEFER`; integral equation/numerical method context is not needed for Chapter 1 theoretical tail derivation |
| Claude folder outputs | Not read or modified in this phase |

## Missing Evidence Handling

No core Chapter 1 claim remains as unsupported fact. Claims that exceed the evidence are downgraded:

- First-order relaxation is a local reduced kinetic model, not a universal graphite microscopic law.
- Present-potential barrier lowering is a reduced active-barrier mobility assumption, not a completed microscopic transition-state surface.
- Equilibrium heterogeneity may contribute to tails; Chapter 1 derives the kinetic residual-tail component.

## Validation

| Check | Result |
|---|---|
| Every planned assumption has evidence status | PASS |
| Unsupported claims removed or downgraded | PASS |
| Archived drafts not equation authority | PASS |
| Ref. 6/7 deferred rather than falsely integrated | PASS |
| Claude folder unmodified | PASS |

## Gate

`PASS_EVIDENCE_SCOPE`

## Next

Proceed to Phase 003 assumption contract.

