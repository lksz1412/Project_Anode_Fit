# Phase 009 Chapter 1-3 Document-to-Code Fidelity Result

## Chain

- Active plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-07-19-v1010-v1023-ch1-ch3-scientific-audit-master-plan-v2.md`
- Plan steps: 117-134
- Canonical snapshot: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Isolated runtime: `D:\Projects\Project_Anode_Fit\Codex\work\audit_runtime\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Canonical traceability: `D:\Projects\Project_Anode_Fit\Codex\results\equation_code_traceability.csv`
- Traceability SHA-256: `7F3C247858810236C71A390121185A6435FAC567D1BC4A6BC1643510966B60E4`
- Detailed independent audit: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase009\P9_code_fidelity_summary.md`
- Fidelity findings: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase009\P9_code_fidelity_findings.csv`
- Finding SHA-256: `0C31CD0CB69EB199230E4C8CE391665D135E4B067569DAE8B9721FEA369E0F8A`
- Detailed-audit SHA-256: `E898CE0A3CB2298986057F63FDE21C5F948536211686B20981D7C630DF14EA52`
- Git commands executed: none
- Source/runtime shared payload mismatches: 0 across 83 files

## Coverage

All recursive TeX inputs of the three v1.0.23 masters were read: 53 distinct
files after shared-preamble deduplication. The three rendered masters were
visually inspected across 129/129 pages, and 12 existing raster outputs were
inspected as nonblank and readable. The 1,585-line implementation, both current
gate scripts, code/fitting guides, QA tools, relevant v1.0.19 examples, AST
inventory, probes, and full-source check records were read in full.

The preliminary 32-row matrix covered only 42 unique equation labels. The final
63-row matrix covers **190/190 included equation labels** with zero unmapped
labels, blank fields, duplicate trace IDs, or invalid classes/statuses.

| Traceability class | Rows |
|---|---:|
| exact | 23 |
| numerical | 10 |
| approximate | 13 |
| document-only | 9 |
| code-only | 1 |
| naming-mismatch | 7 |
| unmapped | 0 |

The fidelity finding ledger contains 19 confirmed rows: five High, eight Medium,
three Low, and three Info. `확정` here means the observed mapping or bounded
adjudication is confirmed; it does not mean every row is a code bug.

## Fidelity Verdict

The code is not a careless transcription. Many central reduced equations are
implemented exactly or with traceable numerical methods: center thermodynamics,
independent logistic occupancy and peaks, pooled charge balance, entropy
derivatives, spinodal-gap helper, zero-Si recovery, additive host response,
Einstein reference term, and reversible/irreversible heat signs within the stated
reduction.

`DOC_CODE_PASS` nevertheless fails because five High findings remain. Two are
code/API defects, one is a shared document-and-code scientific defect, and two
are quantitative document/default problems faithfully carried into code or its
inputs.

### High blockers

1. **Hours versus seconds:** `curve(c_rate in 1/h)` feeds an unconverted inverse-
   hour rate into a seconds-based Eyring chain. This is a code/API defect with a
   demonstrated factor of 3600.
2. **Incomplete local affinity:** code faithfully implements Appendix E's
   forward-factor-only ratio, but both document and code omit the local reverse-
   rate denominator. This is a shared scientific-model defect, not a transcription
   mismatch.
3. **LCO endpoint provenance:** the code formula matches the document, but the
   `g_max=13`, `/atom`, O1-to-O3 transfer, Li-rich gate location, and logistic
   composition law exceed Motohashi's source evidence and directly set the
   quantitative entropy amplitude.
4. **Blend mass normalization:** code and figure agree on fixed graphite plus
   added Si. They do not represent a fixed-total-active-mass wt% series; absolute
   capacity is inflated by `1/(1-m_Si)` under that conventional interpretation.
5. **Stress source fidelity:** code accepts only a caller-computed offset, while
   the document conflates biaxial thin-film and hydrostatic coefficients and
   omits geometry/finite-strain transfer limits. The runtime does not repair or
   validate this input physics.

## Important Non-blocking Distinctions

- The LCO electronic term is frozen at 298.15 K in code. This differs from the
  displayed dynamic `T` and `T^2` chain, but the guide discloses the approximation.
  It is a predictive limitation and cross-document inconsistency, not a hidden
  transcription error.
- Chapter 3 mechanics and plastic hysteresis are not implemented. A scalar
  precomputed offset and an explicit `NotImplementedError` honestly expose the
  boundary. Claims that the runtime itself solves mechanics must therefore be
  rejected, but absence under GS-1 is not a covert code defect.
- Finite-rate host switching/nonadditivity is similarly outside GS-2. Smooth
  additive curves validate numerical continuity only.
- The regular-solution equations motivate hysteresis, while equilibrium occupancy
  remains an independent logistic reduction. The document marks that reduction;
  it should not be presented as an implemented mean-field equilibrium solver.
- The preliminary “irreversible heat is code-only” finding was refuted.
  `eq:qrev` contains both irreversible and reversible heat terms, and both code
  methods map correctly to them.

## Medium Test And API Findings

- G-E3 iterates the same update as the candidate, so it proves convergence of the
  reduced map rather than correctness against an independent nonlinear oracle.
- The FFT transfer helper is circular because it is unpadded. An edge impulse
  sends 90.3% relative response into the early segment; the public API does not
  declare periodic boundaries.
- Existing gates omit hour-second invariance, complete-affinity denominator,
  fixed-total-mass normalization, nonperiodic FFT endpoints, and independent
  physical oracles.
- The only inverse demo is same-model, high-SNR synthetic recovery. Its small
  errors do not establish real-data uniqueness or identify kinetics, LCO gate,
  blend composition, PSD, or mechanics.
- FITTING_GUIDE retains older version paths; `curve_qa.py` hard-codes a Unix
  path and writes source-relative outputs, reducing portability.
- G1 compares v1.0.23 to v1.0.19 rather than directly to v1.0.22.

## Runtime Evidence

- Compileall: exit 0.
- Main gate: exit 0.
- Self-consistent gate: wrong-CWD run exits 1 as expected from its path loader;
  isolated-runtime CWD run exits 0 with G-E1 through G-E5 PASS.
- Main module demonstration: exit 0, `overall: OK`.
- v1.0.19 synthetic inverse against v1.0.23 runtime: exit 0, final objective
  `2.433e-5`, maximum center error 0.1749 mV, `n` error 0.436%, and capacity
  error 1.195% under that closed scenario.
- Independent probes reproduce the 3600 unit ratio, 3.7178 incomplete-affinity
  ratio, 317.574 microV frozen-electronic center difference, `1/(1-m)` blend
  inflation, FFT wraparound, and internal entropy finite-difference agreement.

Existing tests establish implementation consistency for their selected cases.
They do not supersede the orthogonal physical-invariance failures.

## Required Corrections

1. Enforce a single SI or explicitly converted time/charge contract and add
   representation-invariance gates.
2. Re-derive and test the complete local-affinity rate; distinguish the reduced
   forward-only approximation if retained.
3. Add independent nonlinear solver and boundary-oracle tests, including padded
   FFT edge cases.
4. Reclassify LCO source tiers/defaults and separate source evidence from
   phenomenological interpolation.
5. Expose a declared blend mass basis and add fixed-total-mass conservation
   gates; preserve the current behavior only under an explicit fixed-graphite-
   addition name.
6. Rename the stress input as a precomputed voltage offset or implement a typed,
   geometry-aware adapter only after the mechanics model is defined.
7. Add real-data, multi-start, misspecified-model, profile-likelihood/Jacobian,
   and uncertainty tests before inverse-use claims.
8. Make tools path-relative, output-directed, and no-write capable; add direct
   v1.0.22-to-v1.0.23 regression coverage.

## Gate

**`DOC_CODE_PASS: FAIL`**.

Reason: every included equation/group has a status, but five confirmed High
findings remain in unit invariance, complete-affinity kinetics, LCO parameter
provenance, blend normalization, and stress-source fidelity. Passing internal
gates cannot close these scientific and API failures.
