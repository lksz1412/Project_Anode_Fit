# Phase 007 Chapter 3 Scientific Audit and Strengthening Result

## Chain

- Active plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-07-19-v1010-v1023-ch1-ch3-scientific-audit-master-plan-v2.md`
- Plan steps: 86-101
- Canonical snapshot: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Detailed independent audit: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase007\P7_ch3_summary.md`
- Finding register: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase007\P7_ch3_findings.csv`
- Finding-register SHA-256: `9F9886A6661759A5EC373904A81D41635404198F5CAB9600EA7967B5C921A8E5`
- Detailed-audit SHA-256: `230772239E7D45B77546CA8A0C59DFAC33580667EDC7964E2D08526D734C5F20`
- Direct primary-source check: `D:\Projects\Project_Anode_Fit\Codex\work\phase007\ch3_sethuraman_geometry_source_check.md`
- Git commands executed: none
- Writes outside `D:\Projects\Project_Anode_Fit\Codex`: none

## Scope And Verification

The Chapter 3 master and its complete transitive TeX graph, rendered text,
latest code, relevant Chapter 1 equations, version records, handovers, source
matrices, blend and time-unit probes, and the Sethuraman full-source record were
read under the phase's stated coverage rules. Chapter 3 scientific section files
are byte-identical between v1.0.22 and v1.0.23; the findings therefore apply to
both unless marked code-only.

Codex directly read all 19 CSV records and all 448 lines of the independent
report. It independently checked the key mass-basis algebra, stress tensor
conversion, and the Andersen per-Si normalization and capacity-limited cycling
statements against the official open article before accepting the findings.

| Severity | Count |
|---|---:|
| High | 7 |
| Medium | 10 |
| Low | 2 |

| Evidence status | Count |
|---|---:|
| `확정` | 18 |
| `근거 미발견` | 1 |

## Scientific Verdict

Chapter 3 contains a coherent **restricted equilibrium forward model**. Within
an independent-host additive closure, the common-potential pooled balance, the
mass-to-capacity-fraction algebra, zero-Si recovery, one-time background term,
normalized equilibrium curves, and the tension-positive stress sign are
internally correct.

It does not pass as a quantitatively transferable Si/SiOx/Si-C composite model.
The current document and code leave the mass basis, material-specific capacity
denominator, inter-host coupling, finite-rate current partition, stress measure,
finite-strain domain, degradation states, and inverse identifiability either
incorrectly specified or outside the implementation while still permitting
stronger physical readings.

## High Findings

1. **Blend mass basis:** `from_wt()` computes
   `f_Si=m q_Si/[m q_Si+(1-m)q_gr]` correctly, but the constructor holds graphite
   capacity fixed and adds Si. A nominal fixed-total-mass series is therefore a
   fixed-graphite-addition series. Absolute capacity is inflated by
   `1/(1-m)`: 1.111, 1.25, and 1.429 at 10, 20, and 30 wt%. Normalized shapes
   remain unchanged, which is why the internal area gate misses the defect.
2. **Restricted blend exactness:** common equilibrium chemical potential is
   exact, but factorized host partition functions and additive pure-host response
   require `G_int=0` or an equivalent separable closure. Common terminal voltage
   is not evidence that elastic, interfacial, or activity coupling is absent.
3. **Stress measure:** Sethuraman measured equi-biaxial in-plane thin-film slopes,
   not hydrostatic slopes. For plane stress,
   `sigma_h=2 sigma_b/3` and `dV/dsigma_h=(3/2)dV/dsigma_b`. The source's
   approximate theory is about 62 mV/GPa biaxial, while measured biaxial slopes
   are 125, 104, and 110 mV/GPa. These must not be equated with one hydrostatic
   `vbar/F` coefficient.
4. **Finite strain:** the scalar Larché-Cahn relation is a local small-strain,
   small-solute, isotropic-expansion approximation. The primary source expressly
   warns that errors can be substantial near roughly 270% volume strain. It is
   not a full-cycle constitutive law for 270-300% Si expansion.
5. **Material capacity basis:** elemental Si, SiO, and Si-C defaults use
   noncommensurate denominators and cycle states. In particular, Andersen's
   `3117 mAh/g` is effectively per gram of Si in a 60% Si composite, not per gram
   of a generic Si-C component or total electrode. One `m_Si/q_Si` interface
   cannot safely represent all three.
6. **Stress identifiability:** only `U_j+si_stress_offset` enters the model.
   Shifting every Si center by `delta` and the offset by `-delta` leaves every
   output unchanged. ICA/DVA alone cannot identify stress, stress-free centers,
   or partial molar volume.
7. **Composition identifiability:** normalized curves identify at most effective
   capacity fraction under assumed host shapes. `m_Si` and `q_Si` are exactly
   non-identifiable without independent mass/loading and capacity calibration;
   dividing by total `Q` removes the absolute scale.

## Medium And Boundary Findings

- The existing G3 area check is an internal identity and cannot validate the
  external fixed-mass basis.
- Public finite-rate wrappers pass the same electrode-level `I_abs` and `Q_cell`
  to both hosts and do not solve `I_gr+I_Si=I`; GS-2 honestly exposes the omission,
  but returned curves remain heuristic.
- The scalar partial molar volume lacks a fully declared molar denominator,
  composition/phase/history dependence, provenance, uncertainty, and transfer
  rule. Its numerical absence is already disclosed, so this is Medium rather
  than High.
- First-cycle/two-phase and later-cycle/solid-solution narratives need initial
  crystallinity, cutoff, rate, geometry, cycle, and Li15Si4-state qualifiers.
- Thin-film experiments confirm a substantial mechanical contribution, not
  universal dominance of Si hysteresis over phase-path, kinetic, SEI/interfacial,
  and structural-relaxation mechanisms.
- `1-ICE=41.5%` is total irreversible charge. It does not allocate that amount
  specifically to silicate/Li2O without a phase-resolved lithium balance.
- Andersen's greater-than-1200-cycle result is capacity-limited half-cell cycling
  with FEC and CMC/SBR. The source warns that degradation is masked while
  resistance and end voltage rise; it is not unrestricted stability evidence.
- Fracture, electrical isolation/loss of active material, SEI, parasitic lithium,
  resistance, electrolyte depletion, and aging are discussed but have no states
  or complete formal exclusion boundary in the forward model.
- The Chapter 3 finite-rate path inherits the Chapter 1 hours-versus-seconds
  defect, producing a 3600-fold lag difference for equivalent Ah and coulomb
  representations.

The stress sign itself passes. With tension positive and positive chemical
expansion, compression lowers potential and tension raises it. The remaining
reference-state requirement is to hold composition, temperature,
phase/microstructure, and branch history fixed. The omitted stress-squared
compliance-derivative term is a Low approximation-label issue because the
chapter selects a first-order term and the primary paper likewise neglects it
for its simplified estimate.

## Document-Code Correspondence

| Item | Verdict |
|---|---|
| Independent-host pooled equilibrium balance | Exact inside the declared additive closure; no `G_int` state |
| `m_Si` to `f_Si` formula | Algebraically exact; constructor uses the wrong basis for a fixed-total-mass interpretation |
| Additive equilibrium `dQ/dV` | Exact for isolated host responses; not proof of real coupled nonideality |
| Finite-rate blend | Numerical sum exists; no host-current partition and inherits the 3600 unit defect |
| `f_Si=0` recovery and one-time `Cbg` | Confirmed correct |
| Stress term | A precomputed voltage offset is applied; no stress measure, geometry conversion, constitutive state, or identifiable decomposition |
| GS-1 and GS-2 | Honest `NotImplementedError` boundaries; other omitted degradation outputs need the same clarity |
| Figures | Normalized shape coordinates agree with code; absolute capacities and material labels inherit basis defects |

## Strengthening Order

1. Define whether each constructor means fixed total active mass, fixed graphite
   mass plus addition, total electrode mass, or elemental-Si mass. Add a machine-
   checked basis registry and fixed-mass capacity/area gates.
2. Separate `m_component`, elemental-Si mass, active utilization, and all
   per-material/per-electrode specific capacities. Repair the Si-C default and
   regenerate capacity labels.
3. Qualify common-potential/additive balance as exact only in the independent-host
   equilibrium model and show the excluded coupled stationarity equation.
4. Restrict the current blend API to equilibrium or implement host-specific
   kinetics and a current partition satisfying `I_gr+I_Si=I`.
5. Split hydrostatic and equi-biaxial coefficients and require callers to declare
   stress measure and geometry. Preserve theory, measurement, and converted
   values as separate quantities.
6. Put small-strain, small-solute, isotropic-expansion, reference-state, and
   omitted-compliance assumptions before the scalar equation; use a finite-
   deformation chemo-mechanical framework for full-cycle prediction.
7. Add a path-state table for material, initial structure, cycle, cutoff, rate,
   geometry, Li15Si4 formation, and history. Keep logistic components explicitly
   phenomenological until those states are modeled.
8. Add formal exclusions for fracture/LAM, SEI/lithium inventory, resistance,
   electrolyte depletion, and aging, or introduce independently validated state
   equations and data.
9. Require absolute capacity, independent composition/loading, stress
   measurement or stress-free OCV, profile likelihood/Jacobian rank, and
   uncertainty before physical inverse claims.
10. Repair the inherited time-unit path before any finite-rate Chapter 3
    comparison.

## Gate

`CH3_AUDIT_COMPLETE`; **`CH3_PASS` NOT CLOSED**.

Reason: the restricted forward algebra has useful and correct pieces, and no
Critical contradiction was established. Seven High findings nevertheless block
quantitative material transfer and physical inverse interpretation. The chapter
must correct the basis, geometry, validity-domain, and identifiability problems
before it can serve as a review-grade or predictive composite-electrode model.
