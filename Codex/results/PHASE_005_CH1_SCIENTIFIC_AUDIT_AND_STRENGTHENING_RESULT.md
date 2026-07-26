# Phase 005 Chapter 1 Scientific Audit and Strengthening Result

## Chain

- Active plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-07-19-v1010-v1023-ch1-ch3-scientific-audit-master-plan-v2.md`
- Plan steps: 55-70
- Canonical snapshot: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Detailed independent audit: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase005\P5_ch1_summary.md`
- Finding register: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase005\P5_ch1_findings.csv`
- Finding-register SHA-256: `304D720C32138350250BDF9B9F9B17FA6B1E48AD9584787D13B54CFBD45495D1`
- Detailed-audit SHA-256: `884DCE8EA382FFA81FA322D9ED67784AF8DD023ACD204C7C983EF8224F3E1CED`
- Independent probe: `D:\Projects\Project_Anode_Fit\Codex\work\phase005\ch1_scientific_probe_results.csv`
- Git commands executed: none
- Writes outside `D:\Projects\Project_Anode_Fit\Codex`: none

## Scope And Verification

The Chapter 1 master and every transitive TeX input, code, tests, guides,
handovers, relevant v1.0.19-v1.0.22 comparators, source matrices, eight fully
read primary-text records, and all assigned probes were read in full. Earlier
versions were covered through the Phase 002 full-read ledger and Phase 003
lineage rather than inferred from the endpoint.

Codex directly read every field of all 16 finding rows and all 659 lines of the
detailed report, then rechecked the complete-affinity and hour/second probe data
before accepting the findings.

| Severity | Count |
|---|---:|
| Critical | 2 |
| High | 10 |
| Medium | 4 |

| Evidence status | Count |
|---|---:|
| `확정` | 13 |
| `미검증` | 2 |
| `근거 미발견` | 1 |

## Scientific Verdict

Chapter 1 has a substantial correct mathematical core. The charge-balance
derivative, center-potential sign convention, ideal-logistic peak area, height,
full width at half maximum and variance, regular-solution spinodal algebra,
Gaussian convolution normalization and variance addition, independent
summation, zero-current/zero-lag limits, and explicit-`n` thermal implicit
derivative were reproduced.

The chapter does not pass as a physically closed kinetic/inverse framework.
Two Critical implementation/model defects and ten High validation, memory,
identifiability, and source-provenance issues remain. The current script gates
validate legacy bit-exactness and same-model arithmetic; they do not test the
physical invariants that expose these defects.

## Critical Findings

1. **C-rate/Eyring unit contract:** the public path accepts C-rate in `h^-1` but
   combines `I/Q` with a seconds-based Eyring attempt frequency without one
   canonical conversion. The same 1 Ah, 1 A experiment represented as Ah or
   coulombs changes `L_q` and `L_V` by exactly 3600. Fitted lag and activation
   parameters therefore depend on the user's unit representation.
2. **Incomplete detailed-balance closure:** the optional v1.0.23 ratio path
   updates the state-dependent forward barrier but freezes the reverse-rate
   denominator at the cut affinity. A single local forward/reverse pair requires
   both factors to use the same local total affinity. The omitted denominator
   produces relative lag-length errors of 13.25%, 36.66%, 99.93%, and 271.78%
   in the checked tail states for `Omega/RT=2,3,4,5`.

## High Findings

- **Causal state contract:** every call initializes the lag state at the first
  equilibrium value and sorts by potential. Cropping prior history gives state
  error 0.0446 and peak error 1.4878 V^-1, while arbitrary sample permutation is
  erased by sorting. The API does not represent incoming state, acquisition
  order, reset, or reversal semantics.
- **Heuristic presented as certificate:** the `epsilon` quantity is a regime
  indicator, not an error certificate. An independent nonlinear ODE solve gives
  a converged peak error about 29.6% at `epsilon=0.25`; at `epsilon=1`, the ratio
  correction is worse than the frozen approximation.
- **Thermal fallback mismatch:** with neither `n` nor `w`, `_width` uses
  `RT/F`, but `_dwdT` returns zero. The analytic entropy coefficient then differs
  from finite difference by `9.4666e-5 V/K`; explicit `n=1` passes.
- **PSD/transport overclaim:** the cited evidence does not justify universal
  zero interparticle center spread or dynamically negligible particle-size
  distribution. `tau` varies by 225 from 1 to 15 micrometers, and the checked
  5-micrometer diffusion times are comparable to the cited pulse/relaxation
  protocol.
- **Finite-mixture identifiability:** identical components identify only
  `Q1+Q2`; the capacity Jacobian condition number is `1.19e16`. It remains 17.89
  for 5 mV separation at 20 mV width. The chapter's correct warning against
  nonparametric inversion does not address its own finite fitted mixture.
- **Staging anchors:** exact 0.085, 0.120, 0.125/0.140, and 0.210 V source
  assignments were not verified from fully read primary pages. Treat them as
  sample- and protocol-dependent initialization priors.
- **Reversed Persson trend:** the cited primary calculation reports increasing
  migration barriers and decreasing diffusivity with increasing Li content, not
  the claimed decreasing 48-to-40 kJ/mol trend. The source observable also is not
  automatically the fitted effective Eyring barrier.
- **Material-system transfer:** a potassium-graphite paper is load-bearing for a
  lithium-graphite phase-class decision. It is valid comparison context, not
  direct Li-graphite evidence.
- **Bibliographic identity:** the claimed MCMB Part 1 method uses the Garrick JES
  key, but the intended MCMB article is a distinct ECS Advances paper,
  `10.1149/2754-2734/ad7d1c`.
- **Entropy magnitude:** `+3 to +4 mV/K` remains in the body although the local
  footnote admits a possible factor-ten conflict. Full equation/figure evidence
  was not retrieved, so neither that number nor `about +0.3 mV/K` is promoted to
  a final equation-level fact in this phase.

## Model-boundary Findings

The executable peak is an ideal-logistic phenomenological response even when
the same transition's `Omega>2RT` is interpreted through a regular-solution
double well. These are two model strata, not one equilibrium free-energy
derivative. The current reduced model can remain, but `Omega` must be described
as a separate metastability prior rather than inferred from logistic peak shape.

The spinodal voltage span is mathematically correct as a metastability upper
bound. It is not the Maxwell equilibrium plateau gap or a universal zero-current
hysteresis law. The document now states this correctly in several places, so the
remaining issue is narrower: keep Maxwell/binodal, spinodal, nucleation,
mosaic/ensemble, and transport regimes visibly separate.

The optional FFT transfer helper performs unpadded circular convolution. A late
impulse creates an early-window wrap amplitude 0.4899 of the peak. This is Medium
because the helper is optional, but it must use padded linear causal convolution
if retained.

The `+60.8 mV` reversible-heat example is a same-model regression, not external
graphite validation. The cited Hales work supports potentiometric measurement
methodology only.

## Strengthening Order

1. Enforce one charge/current/time API contract and add Ah-versus-coulomb
   representation-invariance gates.
2. Re-derive the optional rate from one local detailed-balance pair, including
   the reverse denominator, before enabling or calling it self-consistent.
3. Introduce a stateful causal-path API with incoming state, caller order,
   monotone branch, reset, and reversal semantics.
4. Rename `epsilon` as a heuristic indicator and validate against an independent
   nonlinear IVP/Volterra oracle with residual, tolerance and grid convergence,
   reported error norms, and a direct-solve fallback.
5. Make the no-key thermal fallback consistent or reject it; preserve explicit
   `w` as frozen and explicit/default `n` as thermal under one schema.
6. Separate equilibrium width, static heterogeneity, PSD, kinetics, transport,
   and measurement convolution. Keep PSD omission as a tested prior, not an
   identity.
7. Add Jacobian rank/SVD, profile likelihood or posterior correlation, and
   multi-rate/multi-temperature/both-branch data before interpreting individual
   reaction parameters.
8. Replace the FFT helper with a padded causal convolution and edge-impulse test.
9. Correct the Persson trend and MCMB citation identity; downgrade exact staging
   voltages and unresolved entropy magnitude until primary locators are available.
10. Add direct Li-graphite operando phase evidence and external graphite
    half-cell entropy/reversible-heat data. Keep all synthetic worked gates
    labeled as internal consistency tests.

## Runtime Evidence

- `python test_gates_v1023.py`: exit 0; G1/G2/G3, `n(T)`, and R6 printed PASS.
- `python test_gates_v1023_selfconsistent.py`: exit 0; G-E1 through G-E5 printed PASS.
- `python -m pytest -q`: exit 1 because no tests were collected; the gate files
  are script-style executables.
- Independent scientific probe: exit 0 and 63 result rows covering unit
  invariance, complete affinity, analytic limits, state history, FFT causality,
  nonlinear ODE error, thermal finite difference, convolution, identifiability,
  and PSD scaling.

Passing script gates are retained as implementation evidence. They do not refute
the Critical/High findings because they do not test those external invariants.

## Gate

`CH1_AUDIT_COMPLETE`; **`CH1_PASS` NOT CLOSED**.

Reason: all load-bearing Chapter 1 claims have a disposition and the valid
mathematical core was independently reproduced, but two Critical defects and ten
High issues remain in unit invariance, detailed balance, memory semantics,
validation, identifiability, and source interpretation.
