# Phase 006 Chapter 2 Scientific Audit and Strengthening Result

## Chain

- Active plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-07-19-v1010-v1023-ch1-ch3-scientific-audit-master-plan-v2.md`
- Plan steps: 71-85
- Canonical snapshot: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Read-coverage prerequisite: `FULL_READ_SCOPE_PASS`
- Source prerequisite: `SOURCE_BASELINE_PASS`
- Detailed independent audit: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase006\P6_ch2_summary.md`
- Finding register: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase006\P6_ch2_findings.csv`
- Finding-register SHA-256: `2CDE46AFA9CBD4061E2E122286823A0F916B89D90484B3F72401C7B0380D6E56`
- Detailed-audit SHA-256: `26FBFFE269F9A63A8162DCABFE64D6BCF8EA68A8B023648989801BCB69E78396`
- Git commands executed: none
- Writes outside `D:\Projects\Project_Anode_Fit\Codex`: none

## Scope And Verification

The latest Chapter 2 master, all transitive LCO sections, the inherited thermal
and entropy chain, code, tests, fitting guide, handover, v1.0.19-v1.0.22
comparators, source matrices, direct numerical probes, and three full-source
checks were read in full. The independent report records the exact physical line
range for every file and distinguishes direct line reads from byte-identical
duplicate coverage.

The final register contains 20 unique findings with the required 13-column
schema. Codex directly read every CSV field and all 674 lines of the detailed
report, rechecked the cited Motohashi DSC and DOS passages, and accepted the
register only after the late Reynier, Motohashi, and temperature-freeze evidence
was incorporated.

| Severity | Count |
|---|---:|
| Critical | 4 |
| High | 8 |
| Medium | 6 |
| Info | 2 |

| Evidence status | Count |
|---|---:|
| `확정` | 12 |
| `미검증` | 5 |
| `근거 미발견` | 2 |
| `미결` | 1 |

## Scientific Verdict

Chapter 2 is not scientifically void. Its independent-site grand partition,
occupancy/logistic mapping, configurational partial-molar sign, same-model
implicit OCV derivative, Einstein reference cancellation, regular-solution
spinodal formula, and the Bernardi reversible-heat sign under the stated current
convention are mathematically reproducible.

The chapter nevertheless does not pass as the claimed literature-grounded,
composition-local LCO entropy model. The principal problem is that a correct
Sommerfeld identity is connected to an unsupported composition kernel and then
implemented as a different, frozen model. Internal finite-difference and
round-trip tests confirm the frozen implementation only; they do not validate
the displayed physical model or its literature provenance.

### Critical findings

1. **Reynier quantity identity:** approximately `0.18 k_B/atom` is an electronic
   state entropy at metallic `x=0.833`, not a total partial-molar
   configuration-plus-vibration-plus-electronic lithiation entropy. State
   entropy, its composition derivative, and measured lithiation entropy were
   conflated.
2. **Electronic gate derivation:** Fermi-Dirac occupation in energy, a Mott
   transition, and a two-phase composition interval do not derive a logistic
   DOS-versus-composition kernel, `Delta x=0.05`, or the calculated
   `-45.7 J/(mol K)` electronic partial-molar peak. No source establishing that
   quantitative gate was found.
3. **Composition locality:** the document presents `Delta S_e(x,T)`, but the
   code evaluates one point, `x_center=x_MIT=0.85`, and applies the resulting
   constant to the T1 slot. There is no stoichiometric `x(V)` or `x(xi)` path.
4. **Temperature integration:** the document integrates `Delta S_e=a_e T` to a
   quadratic center shift with the required factor `1/2`; the code freezes the
   electronic entropy at `T_ref` and uses a linear shift. The isolated mismatch
   is `79.39 microV` at `|Delta T|=10 K`, `317.57 microV` at `20 K`, and about
   `1.985 mV` at `50 K` for the current parameters.

### High findings

- Motohashi's `13 electrons/eV for CoO2` is inferred from a susceptibility
  difference under a Pauli attribution assumption. It is not a direct DOS
  measurement, does not establish `/atom` normalization, belongs to O1 `x=0`,
  and does not independently fix an O3 Li-rich gate near `x=0.85`.
- At the frozen center, `g_max`, `Delta x`, and `x_MIT` are not separately
  identifiable: the amplitude reduces to `g_max/(4 Delta x)` and a locked
  translation of center and gate location cancels.
- The fixed-enthalpy gate-off example changes reference calibration. Rebaselining
  the gate-off enthalpy preserves the 298.15 K OCV and removes the reported
  91 mV reference shift, so that shift is not independent evidence that the
  electronic gate is indispensable.
- The additive configuration/vibration/electronic factorization lacks a bound on
  cross terms near the coupled ordering and metal-insulator interval.
- A multicluster LCO expansion and ordered ground state are not equivalent to a
  single symmetric regular-solution `Omega`; `Omega>2RT` is the chosen surrogate's
  demixing criterion, not an if-and-only-if microscopic order criterion.
- A fitted two-phase or heterogeneous peak width cannot be promoted to
  equilibrium configurational entropy merely because `w=nRT/F` makes the
  derivative algebra close.
- Arithmetic charge/discharge branch averaging recovers equilibrium entropy only
  under an exact antisymmetry condition that the cited material evidence does not
  establish generally.
- The Chapter 2 master is an inherited extension built from Chapter 1 section
  families, not a self-contained review/textbook chapter under its present
  prerequisite and code-boundary presentation.

## Confirmed Implementation Defects

Two additional shared-code defects require correction even apart from the
electronic model:

- LCO transition records provide both `w` and `n=1`; `_n_factor` gives `n`
  precedence, so the displayed `w=0.030/0.024/0.028 V` values are dead and all
  three actual widths are `RT/F=0.025691238 V` at 298.15 K.
- With neither `n` nor `w`, the width path defaults to `RT/F`, while `_dwdT`
  returns zero. The curve and entropy paths therefore differentiate different
  definitions.

The reversible-heat formula itself is retained conditionally, but the API needs
an explicit cell-current and electrode/full-cell assembly contract to prevent
caller-level sign inversion.

## Primary-source Corrections

- **Reynier 2004:** distinguish `S_el(x)`, `dS_el/dx`, measured lithiation
  entropy, and the two-phase endpoint comparison. The paper assigns most of the
  O3 composition trend over much of `0.6<x<0.833` to configurational entropy and
  does not establish electronic-only uniqueness.
- **Motohashi 2009:** downgrade `13 electrons/eV for CoO2` to an
  assumption-dependent endpoint prior until normalization is reconstructed.
  Motohashi is, however, the direct DSC source of latent heats `82.2` and
  `272 J/mol`, corresponding to transition entropies about `0.47` and
  `1.49 J/(mol K)` at `x=0.50` and `0.67`. Their assignment to T2/T3 OCV slots
  remains unverified.
- **Marianetti 2004:** retain the Mott/correlation mechanism as context but do not
  treat it as a derivation of the logistic kernel or width.
- **Van der Ven 1998:** retain multibody phase-stability evidence but remove the
  unproved direct correspondence to one scalar `Omega`.

## Strengthening Order

1. Correct source identities and epistemic tiers before adjusting parameters.
2. Name the existing path `frozen_demo` and stop describing the local dynamic
   path as implemented.
3. Define a unique stoichiometric mapping and implement the electronic free-energy
   term, including the quadratic temperature integral, only if the local model is
   retained.
4. Compare no-gate, configurational-only, coupled, and alternative electronic
   kernels with the same reference calibration and nested refitting.
5. Replace the three frozen gate parameters by one identifiable amplitude, or
   demonstrate profile likelihood and covariance using composition-resolved,
   multi-temperature data.
6. Separate ideal thermodynamic width from heterogeneity, coherency, kinetics,
   transport, and instrument broadening before propagating width into reversible
   heat.
7. Use relaxed equilibrium entropymetry as the reference; retain branch averaging
   only as a tested symmetry diagnostic.
8. Add O3 composition-resolved electronic structure or calorimetry, controlled
   phonon evidence, and real-data external-oracle tests. Synthetic round trips
   remain implementation tests.

## Gate

`CH2_AUDIT_COMPLETE`; **`CH2_PASS` NOT CLOSED**.

Reason: all load-bearing chains received a disposition and the valid algebraic
subchains were independently reproduced, but four Critical document/source/code
mismatches and eight High provenance, identifiability, transfer, and structural
problems remain. Chapter 2 should not be represented as a source-validated local
LCO entropy model until the required corrections above are made and externally
tested.
