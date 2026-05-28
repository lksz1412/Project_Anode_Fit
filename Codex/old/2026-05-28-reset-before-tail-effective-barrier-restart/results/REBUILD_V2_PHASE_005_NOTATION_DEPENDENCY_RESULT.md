# Rebuild v2 Phase 005 Notation Dependency Result

Project: `D:\Projects\Project_Anode_Fit`

Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-05-27-graphite-ica-from-scratch-rebuild-plan-v2-canonical.md`

Phase: `Phase 005 - Notation And Equation Dependency Contract`

Date: 2026-05-27

Gate: `PASS_REBUILD_V2_NOTATION_DEPENDENCY`

## Scope

Phase 005 fixed notation roles and equation dependencies before manuscript drafting. It created the notation bible and equation dependency DAG required to prevent the old circular use of `V_n`.

## Step Execution

| Step | Planned Action | Status | Evidence |
|---:|---|---|---|
| 121 | Create notation bible. | DONE | `REBUILD_V2_NOTATION_BIBLE.md` created. |
| 122 | Create equation dependency DAG. | DONE | `REBUILD_V2_EQUATION_DEPENDENCY_DAG.md` created. |
| 123 | Define measured variables before model variables. | DONE | Notation bible begins with measured variables. |
| 124 | Define `Q_ext`. | DONE | `Q_ext(t)` entry added. |
| 125 | Define `Q_cell`. | DONE | `Q_cell` entry added. |
| 126 | Define `q=Q_ext/Q_cell`. | DONE | `q` entry added. |
| 127 | Define current `I` and sign convention. | DONE | `I(t)`, `I_abs(t)`, `s_I` entries added. |
| 128 | Define temperature `T`. | DONE | `T(t)` or `T(q)` entry added. |
| 129 | Define internal state vector `xi`. | DONE | `xi_j` and vector `xi` entries added. |
| 130 | Define equilibrium occupancy with dummy voltage `V`. | DONE | `xi_{j,eq}(V,T)` entry added before `V_n`. |
| 131 | Define `Q_bg(V,T)`. | DONE | Storage entry added. |
| 132 | Define transition capacities `Q_j,tot`. | DONE | `Q_{j,tot}` entry added. |
| 133 | Define transition centers `U_j(T)`. | DONE | `U_j(T)` entry added. |
| 134 | Define transition widths `w_j(T)`. | DONE | `w_j(T)` entry added. |
| 135 | Define `a_j=Q_j,tot/Q_cell`. | DONE | `a_j` entry added. |
| 136 | Reserve `w_j` only for voltage width. | DONE | Symbol collision controls added. |
| 137 | Define charge-balance residual `G`. | DONE | `G(V;q,T,xi,theta)` entry and DAG E07 added. |
| 138 | Define root operator `mathcal V`. | DONE | Root operator entry and DAG E08 added. |
| 139 | Define `V_n` only as solved root. | DONE | `V_n` entry and DAG E09 added. |
| 140 | Define `V_OCV` only as equilibrium special root. | DONE | `V_{n,OCV}` entry and DAG E10 added. |
| 141 | Define `V_app`. | DONE | `V_{n,app}` entry and DAG E11 added. |
| 142 | Define `V_drive`. | DONE | `V_{n,drive}` entry and DAG E12 added. |
| 143 | Define affinity `A_j`. | DONE | `A_j` entry and DAG E13 added. |
| 144 | Define kinetic rate `k_j`. | DONE | `k_j` entry and DAG E14 added after `V_n`. |
| 145 | Define `dxi/dt`. | DONE | Entry and DAG E15 added. |
| 146 | Define `dxi/dq` only under nonzero current. | DONE | Entry and DAG E16 added with `I_abs>0` condition. |
| 147 | Define rest relaxation separately. | DONE | DAG E17 added. |
| 148 | Define `dV_n/dq`. | DONE | Entry and DAG E22 added after dynamics. |
| 149 | Define `dV_app/dq`. | DONE | Entry and DAG E23 added. |
| 150 | Define ICA observable. | DONE | Entry and DAG E24 added. |
| 151 | Define DVA observable. | DONE | Entry and DAG E25 added. |
| 152 | Build dependency DAG with prerequisites. | DONE | Dependency table and Mermaid graph added. |
| 153 | Add Forbidden Reordering section. | DONE | Added in both notation bible and DAG. |
| 154 | Add Symbol Collision section. | DONE | Added in both notation bible and DAG. |
| 155 | Add Allowed Synonyms section. | DONE | Added in both notation bible and DAG. |
| 156 | Save Phase 005 result. | DONE | This file saved. |
| 157 | Update execution ledger. | DONE | `REBUILD_V2_EXECUTION_LEDGER.md` updated after this result. |
| 158 | Gate Phase 005. | PASS | `PASS_REBUILD_V2_NOTATION_DEPENDENCY`. |
| 159 | Stop if any equation uses `V_n` before root operator. | NOT TRIGGERED | DAG E09 defines `V_n`; all later `V_n` uses depend on E08-E09. |
| 160 | Stop if any notation entry lacks role or unit/domain. | NOT TRIGGERED | Notation tables include role, unit, and domain columns. |

## Key Controls Fixed

- `q` is reserved for normalized external charge.
- `xi_j` is reserved for internal transition state.
- `V` is a dummy argument before root solving.
- `V_n` exists only after `G` and `mathcal V` are defined.
- `V_{n,OCV}` is a derived equilibrium special root.
- `V_{n,app}` and `V_{n,drive}` are distinct downstream voltages.
- `w_j` is reserved for transition voltage width; `a_j` is capacity fraction.
- `dxi_j/dq` is only valid for nonzero-current segments.
- refs. 6/7 closure comes after the exact direct formulation.

## Gate Check

| Gate Item | Result |
|---|---|
| Notation bible exists | PASS |
| Equation dependency DAG exists | PASS |
| Measured variables precede model variables | PASS |
| `V_n` depends on root operator | PASS |
| `V_OCV` is special root only | PASS |
| `dxi/dq` restricted to nonzero current | PASS |
| Forbidden reordering listed | PASS |
| Symbol collisions listed | PASS |
| Allowed synonyms listed | PASS |
| Every notation entry has role/unit/domain | PASS |

Gate result: `PASS_REBUILD_V2_NOTATION_DEPENDENCY`

## Files Created Or Updated

| File | Action |
|---|---|
| `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_NOTATION_BIBLE.md` | created |
| `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_EQUATION_DEPENDENCY_DAG.md` | created |
| `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_PHASE_005_NOTATION_DEPENDENCY_RESULT.md` | created |
| `D:\Projects\Project_Anode_Fit\Codex\results\REBUILD_V2_EXECUTION_LEDGER.md` | updated |

## Next Phase Entry Condition

Proceed to Phase 006 Step 161 only if the next work is the Chapter 1 mathematical foundation package. Final LaTeX manuscript drafting remains blocked until Phase 010 is complete.
