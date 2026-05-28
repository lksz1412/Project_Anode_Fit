# Chapter 1 Theory Derivation Contract

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-28-chapter1-theory-ralph-wiggum-loop-plan.md`

Created: 2026-05-28

## Purpose

This contract states what the Chapter 1 theory-complete manuscript must prove or explain. A later Ralph Wiggum Loop round fails if the manuscript violates any required item below.

## Required Derivations

| ID | Required Derivation | Minimum Visible Steps |
|---|---|---|
| D1 | measured charge coordinate | define `Q_ext`, define `Q_cell`, define `q=Q_ext/Q_cell`, state `dq/dt=|I|/Q_cell` only for nonzero current |
| D2 | ICA and DVA measurement target | define `dQ_ext/dV_obs` and `dV_obs/dQ_ext` before modeling peak shape |
| D3 | graphite storage decomposition | split storage into `Q_bg(V,T)` plus `sum Q_j,tot xi_j` |
| D4 | charge-balance residual | write residual with dummy voltage before naming `V_n` |
| D5 | implicit internal potential | define `V_n` as the root of the residual and state root/branch conditions |
| D6 | equilibrium OCV | set `xi_j=xi_j,eq(V,T)`, substitute into charge balance, define OCV as special root |
| D7 | self-consistent dynamic state | write `dxi_j/dq` after `V_n` is defined and show `V_n=Phi(q,xi,T)` feedback |
| D8 | fixed-point/integral form | integrate `dxi_j/dq` and explain why unknown `xi` on both sides is not a contradiction |
| D9 | derivative of charge balance | differentiate every term before solving for `dV_n/dq` |
| D10 | equilibrium derivative reduction | substitute `dxi_j/dq=(partial xi_eq/partial V)(dV_n/dq)` and solve |
| D11 | apparent voltage derivative | map internal potential to observed/apparent voltage before ICA |
| D12 | ICA/DVA reciprocal | derive from `Q_ext=Q_cell q` and `dV_app/dq` |
| D13 | peak area | integrate transition contribution `Q_j,tot dxi_j/dV` over voltage |
| D14 | peak location | identify peak as maximum transition derivative contribution |
| D15 | peak width | relate equilibrium width and dynamic relaxation length separately |
| D16 | low-T/high-T tail | derive relaxation length `ell_q=|I|/(Q_cell k_j)` and connect lower `k_j` to longer tail |

## Required Physical Statements

| ID | Statement | Allowed Strength |
|---|---|---|
| P1 | ICA peaks arise when graphite transition state variables change rapidly with voltage. | strong, derived |
| P2 | The area of an isolated completed transition peak is tied to `Q_j,tot Delta xi_j`. | strong, with baseline/isolation caveat |
| P3 | Tail shape can vary while area remains fixed. | strong, derived from redistribution of `dxi/dV` |
| P4 | Low temperature can produce a longer tail because activated relaxation is slower in the charge coordinate. | strong as a model explanation of the user's observation |
| P5 | High temperature can shorten the tail because relaxation toward equilibrium is faster. | strong as a model explanation of the user's observation |
| P6 | Equilibrium thermal broadening and dynamic kinetic tailing are distinct. | strong, required caution |
| P7 | If a transition does not complete inside the analyzed voltage window, the visible area need not equal the full transition capacity. | strong caveat |
| P8 | The present chapter does not claim fitted parameters or numerical validation. | mandatory scope statement |

## Forbidden Claims

| Forbidden Claim | Reason |
|---|---|
| "solver implementation is required for Chapter 1 completion" | user clarified current task is theoretical derivation |
| "the long tail is caused only by equilibrium thermal broadening" | contradicts likely direction of simple thermal occupancy broadening and ignores rate lag |
| "peak area is always visually identical without baseline/window caveats" | measured area depends on isolation, baseline, and completion window |
| "refs. 6/7 prove graphite physics" | those references are methodological background, not graphite staging evidence |
| "parameters were fitted" | no fitting was performed |
| "the manuscript is patent-ready" | novelty/legal readiness was not evaluated |

## Ralph Wiggum Failure Messages

These are the exact kinds of messages to write into loop result files.

| Gate | Failure Message Template | Repair Rule |
|---|---|---|
| G1 | `Symbol X is used before it is defined at line Y.` | define X earlier or move the use later |
| G2 | `Equation Y depends on V_n before V_n is derived as a root.` | rewrite with dummy voltage or move after root definition |
| G3 | `Derivative step Y skips term Z.` | expand the derivative and then simplify |
| G4 | `Peak-area statement lacks completion/baseline caveat.` | add the caveat or weaken the statement |
| G5 | `Reader jump from A to B lacks intermediate explanation.` | add the missing algebra/prose step |
| G6 | `Implementation/fitting scope drift appears at line Y.` | remove or recast as out-of-scope limitation |

## Acceptance Gate

The Chapter 1 theory manuscript may be called complete for the current task only when:

1. every required derivation D1-D16 is present;
2. every required physical statement P1-P8 is present with allowed strength;
3. every forbidden claim is absent;
4. all Ralph Wiggum rounds record zero unresolved confirmed issues;
5. static LaTeX checks pass, excluding PDF build.
