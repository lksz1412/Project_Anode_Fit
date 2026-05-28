# Chapter 1 To Chapter 5 Integration Notes

Project: `D:\Projects\Project_Anode_Fit`

Phase: 006

Date: 2026-05-27

Inputs:

- `D:\Projects\Project_Anode_Fit\Codex\results\ver5_chapter_structure_map.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\chapter1_rewrite_spec.md`

## Historical Version To Chapter Naming

The historical `ver.1`-`ver.5` names inside the merged ver5 file should become chapter roles:

| Historical Name In Merged ver5 | New Role | Treatment |
|---|---|---|
| historical ver.1 | Chapter 1 candidate, but obsolete core | replace with corrected charge-balance Chapter 1 |
| historical ver.2 | Chapter 2 | heat / temperature correction layer |
| historical ver.3 | Chapter 3 | electrochemical kinetics / BV-style interface layer |
| historical ver.4 | Chapter 4 | integrated state, observation, and fitting system |
| historical ver.5 | Chapter 5 | hysteresis, branch, and structural memory extension |

The new document body should use `Chapter 1`, `Chapter 2`, etc. Do not preserve historical version labels as body-level change history.

## Chapter Stack

| Chapter | Proposed Title | Primary Responsibility | Receives From Chapter 1 |
|---:|---|---|---|
| 1 | Thermodynamic Charge Balance and Internal Graphite Potential | define `V_n` by charge conservation; derive OCV and ICA/DVA interfaces | none |
| 2 | Temperature and Heat Coupling | approximate heat/temperature effects using Chapter 1 states/rates | `V_n`, `V_app`, `xi_j`, `dxi_j/dt`, `T` |
| 3 | Electrochemical Kinetic Interface | handle driving force, overpotential, and rate interfaces | `V_drive`, `A_j`, `k_j`, `R_n` constraints |
| 4 | Integrated State and Fitting System | assemble state equations, observation equations, constraints, fitting objectives | residuals, observables, parameter constraints |
| 5 | Hysteresis and Structural Memory | add branch/path memory without breaking charge conservation | Chapter 1 charge-balance residual and allowed parameter modulation hooks |

## Interface Contracts

### Chapter 1 -> Chapter 2

| Quantity | Meaning | Constraint |
|---|---|---|
| `dxi_j/dt` | physical transition rate | use time derivative, not q derivative, for heat |
| `V_n`, `V_app` | internal/apparent voltage paths | must satisfy charge-balance residual first |
| `T` | temperature state/input | Chapter 2 may feed `T` back, but must not redefine `V_n` |
| `Q_j,tot` | transition capacity scale | heat terms must respect capacity normalization |

### Chapter 1 -> Chapter 3

| Quantity | Meaning | Constraint |
|---|---|---|
| `V_drive` | kinetic driving voltage | may approximate `V_app`, but double-counting risk must be stated |
| `A_j=s_phi F(V_drive-U_j)` | driving affinity | must keep `U_j` role consistent with Chapter 1 equilibrium centers |
| `k_j` | relaxation rate | cannot be co-fitted freely with `R_n` without staged constraints |
| `V_n` | internal potential | Chapter 3 must consume it, not overwrite it |

### Chapter 1 -> Chapter 4

| Quantity | Meaning | Constraint |
|---|---|---|
| `G(V_n;q,T,xi)` | charge-balance residual | must be a hard or heavily weighted fitting gate |
| `dQ_ext/dV_app`, `dV_app/dQ_ext` | ICA/DVA observables | use external charge convention |
| `xi_j` bounds | physical state constraints | enforce `0 <= xi_j <= 1` or declared signed convention |
| capacity closure | normalization | constrain `Q_bg` and `Q_j,tot` together |
| reference closure residual | approximation quality | compare to direct DAE/root solve when possible |

### Chapter 1 -> Chapter 5

| Quantity | Meaning | Constraint |
|---|---|---|
| `V_n` root relation | thermodynamic base | hysteresis cannot violate charge conservation |
| `U_j(T)`, `w_j(T)`, `Q_j,tot` | possible branch-modulated parameters | branch modulation must be explicit and bounded |
| `xi_j` | memory-bearing state candidate | structural memory should extend state, not rename it |
| validation gates | residual/monotonicity checks | remain active under hysteresis extension |

## Old ver5 Dependencies To Update

| Old Dependency | Problem | Replacement |
|---|---|---|
| old Chapter 1 `V_OCV(q,T)` as a primary basis | conflicts with corrected charge-balance logic | derive `V_OCV` from equilibrium charge balance |
| old `Q_n(q)` observable path | can blur measured external charge vs internal storage | use `Q_ext=Q_cell q` for ICA/DVA |
| old dynamic lag without explicit algebraic root solve | hides feedback loop | define `V_n=V_root(q,T,xi)` before dynamics |
| possible `w_j` symbol reuse | notation collision | reserve `w_j` for transition width, use `a_j` for capacity fraction |
| heat layer consuming q-derivatives only | heat needs time rates | pass `dxi_j/dt`; convert only under constant current |
| later chapters absorbing Chapter 1 residual | overfitting risk | enforce charge-balance residual before later corrections |

## Minimum Integration Sequence

1. Replace historical ver5 Chapter 1 core with corrected charge-balance Chapter 1.
2. Preserve Chapter 2-5 as conceptual layers, but update their input contracts.
3. Move version-history language out of the LaTeX body and into project results/ledger.
4. Run notation pass for `V_n`, `V_app`, `V_drive`, `Q_ext`, `Q_bg`, `w_j`, `a_j`.
5. Add validation gates before allowing Chapter 4 fitting or Chapter 5 hysteresis flexibility.

## Integration Gate

The Chapter stack is consistent only if:

- Chapter 1 owns charge balance and internal potential determination;
- no later chapter defines a second independent `V_n`;
- all later corrections operate through declared interfaces;
- `Q_ext` remains the ICA/DVA capacity axis;
- hysteresis and heat do not erase charge-balance residual checks.
