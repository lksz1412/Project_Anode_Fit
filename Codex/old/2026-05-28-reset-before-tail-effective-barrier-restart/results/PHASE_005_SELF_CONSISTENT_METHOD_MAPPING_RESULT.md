# Phase 005 - Self-Consistent Method Mapping Result

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-anode-dqdv-thermodynamic-fit-development-plan.md`

Ledger: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_001_007_EXECUTION_LEDGER.md`

Mapping: `D:\Projects\Project_Anode_Fit\Codex\results\self_consistent_variable_mapping.md`

Date: 2026-05-27

## Summary

Phase 005 mapped the refs. 6/7 method pattern onto the corrected graphite ver.1 feedback loop.

Gate result: `PASS_METHOD_MAPPING`

Main finding:

- The graphite system is primarily a charge-balance-constrained nonlinear Volterra/DAE problem.
- `V_n` is an algebraic root of charge balance, and `xi_j` evolves by an ODE/integral equation whose right-hand side depends on that root.
- The refs. 6/7 method is portable only as a mathematical closure pattern: isolate feedback, use a reference solution/correction, and validate against a direct coupled solve.
- A literal Fredholm physical analogy would be wrong.

## Step Range

| Planned Steps | Actual Steps | Status |
|---:|---:|---|
| 60-76 | 60-76 | PASS |

## Inputs

| Role | Path | Status |
|---|---|---|
| ver1 dependency graph | `D:\Projects\Project_Anode_Fit\Codex\results\ver1_charge_balance_dependency_graph.md` | used |
| ref. 6/7 method notes | `D:\Projects\Project_Anode_Fit\Codex\results\ref6_ref7_method_notes.md` | used |
| ver5 structure map | `D:\Projects\Project_Anode_Fit\Codex\results\ver5_chapter_structure_map.md` | used |

## Files Created

| Path | Purpose |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\results\self_consistent_variable_mapping.md` | Evidence-linked method mapping and problem-class decision |
| `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_005_SELF_CONSISTENT_METHOD_MAPPING_RESULT.md` | This Phase 005 result |

## Method Classification

| Candidate | Decision | Evidence |
|---|---|---|
| algebraic root-finding | required | ver1 charge balance lines 121-129 |
| nonlinear ODE / DAE | required | ver1 ODE lines 268-286 plus algebraic root |
| Volterra-type integral equation | primary integral form | q/time marching from initial state |
| Fredholm-type integral equation | not primary | refs. 6/7 source context, but graphite has causal q evolution |
| fixed-point equation | algorithm only | unsafe as the problem definition |
| reference-ratio/correction closure | portable method pattern | Phase 004 extraction of refs. 6/7 use |

## Solver-Neutral Graphite Form

The mathematical problem should be written as:

```text
G(V; q,T,xi,theta)
  = Q_bg(V,T;theta)
  + sum_j Q_j,tot xi_j
  - Q_cell q
  = 0
```

and:

```text
xi_j(q) = xi_j(q0)
        + integral_{q0}^{q} F_j(s,xi(s),T(s),I(s);theta) ds
```

where:

```text
F_j = (Q_cell/|I|) k_j(V_n(s),s,T(s),I(s);theta)
      [xi_eq,j(V_n(s),T(s);theta)-xi_j(s)]
```

and `V_n(s)` is the root of `G=0`.

No numerical algorithm is assumed at this level.

## Portable And Non-Portable Parts

Portable:

- second-kind/self-consistent integral formulation;
- feedback isolation;
- reference solution or correction closure;
- validation against direct numerical solution;
- regime limits.

Not portable:

- geminate-pair recombination physics;
- Smoluchowski relative-coordinate diffusion;
- external-field orientation averaging;
- contact sink / Onsager / Debye-Huckel physical parameters;
- Fredholm equation identity as a claim about graphite.

## Recommended Solver Options For Later Draft

| Option | Role | Include In Chapter 1? |
|---|---|---|
| direct DAE/root-solve integration | benchmark truth method | yes, as primary numerical definition |
| quasi-equilibrium reference closure | thermodynamic low-rate shape | yes, as safe reference closure |
| frozen-feedback reference closure | analytic/fast fitting surrogate | optional, with residual gate |
| discretized constrained integral solve | robust fitting implementation | yes, as implementation option |
| raw fixed-point iteration | simple but riskier | only as rejected/limited baseline |

## Validation

| Check | Result | Evidence |
|---|---|---|
| abstract ref. method fields filled | PASS | mapping table section |
| graphite abstract fields filled | PASS | mapping table section |
| every mapping marked with confidence/assumption | PASS | variable mapping table |
| non-portable assumptions listed | PASS | non-portable physical assumptions section |
| problem class selected | PASS | nonlinear Volterra/DAE with algebraic root |
| solver-neutral form produced | PASS | `G=0` plus integral state equation |
| no physical analogy overreach | PASS | Fredholm source explicitly separated from graphite problem class |

## Gate

Gate: `PASS_METHOD_MAPPING`

Gate conditions:

| Condition | Status |
|---|---|
| self-consistent loop converted into explicit mathematical problem class | PASS |
| variable mapping has evidence or is marked as assumed | PASS |
| non-portable physical assumptions listed | PASS |
| solver-neutral formulation exists | PASS |
| no conflict with ver1 or ver5 found | PASS |

## Confirmed Decisions

| Item | Status | Evidence |
|---|---|---|
| `V_n` must remain solved from charge balance | 확정 | Phase 003 |
| dynamic `xi_j` feedback should be treated as DAE/Volterra, not deleted | 확정 | Phase 003 and Phase 005 |
| refs. 6/7 provide a closure pattern, not LIB physics | 확정 | Phase 004 and Phase 005 |
| final Chapter 1 should expose validation gates | 확정 | Phase 005 |

## Open Issues / Decision Queue

| ID | Type | Item | Status | Next |
|---|---|---|---|---|
| MAPP-ISS-001 | implementation | choose exact numerical algorithm for root solve and integral solve | open | Phase 006/007 |
| MAPP-ISS-002 | reference path | choose default reference closure path | open | Phase 006 |
| MAPP-ISS-003 | visual equation fidelity | exact equations copied from PDF need visual check before final manuscript use | open | Phase 007 or manual user check |
| MAPP-ISS-004 | source depth | full refs. 6/7 papers not read, only metadata and 2017-paper use | open | retrieve only if needed later |

## Next

Proceed to Phase 006 Step 77:

- convert the mapping into a Chapter 1 development specification;
- define which content replaces historical ver5 Chapter 1;
- define interfaces to Chapters 2-5.
