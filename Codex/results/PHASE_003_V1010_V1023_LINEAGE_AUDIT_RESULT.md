# Phase 003 v1.0.10-v1.0.23 Lineage Audit Result

## Chain

- Active plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-07-19-v1010-v1023-ch1-ch3-scientific-audit-master-plan-v2.md`
- Plan steps: 24-36
- Canonical snapshot: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Atomic lineage matrix: `D:\Projects\Project_Anode_Fit\Codex\results\v1010_v1023_version_lineage.csv`
- Independent falsification matrix: `D:\Projects\Project_Anode_Fit\Codex\results\phase003_lineage_falsification.csv`
- First-pass report: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_003_VERSION_LINEAGE_FIRST_PASS_RESULT.md`
- Falsification report: `D:\Projects\Project_Anode_Fit\Codex\work\agent_reports\phase003\F1_lineage_falsification_summary.md`
- Atomic-matrix SHA-256: `023E51D8B4224DA532F4B5697CD04C2EFC667220078EDDC42BBD7B95DB1FEE59`
- Falsification SHA-256: `91B3BE1900CFC115210130CD3A41F8D823BEC1331DB4B13F01E6580F82E6C005`
- Git commands executed: none

## Coverage And Method

The atomic matrix contains 300 records from six independently read packages:
v1.0.10-v1.0.18.2, v1.0.19-v1.0.20, v1.0.21-v1.0.22,
v1.0.23, cross-version records, and direct integrator probes. Its 300 rows
contain 206 `확정`, 34 `미결`, 34 `근거 미발견`, 23 `미검증`, and three
`추정` records. Severity is audit priority, not a claim that every raw Critical
or High row survived adjudication.

The fresh-context falsification pass read the 198-line first-pass report, all
300 lineage rows, all 826 artifact-matrix rows, five detailed lineage reports,
the 342-line active plan, and all controlling source ranges. Every one of the
120 raw Critical/High records was targeted in 88 independent challenges. All
826 artifact paths matched recorded size and SHA-256.

Falsification results were 45 upheld, 25 downgraded, nine partial, six outside
the provenance scope, two refuted, and one upgraded. The two reports must be
read together: the atomic matrix preserves the unedited first-pass evidence;
this report and the falsification matrix control final wording and severity.

## Gate

Phase 003 is complete at **`LINEAGE_AUDIT_COMPLETE`**. The unconditional
**`LINEAGE_PASS` remains open** because five release-control adjudications are
not authorized changes in this read-only audit. The open lineage gate does not
invalidate the reconstructed version graph; it prevents stale or missing
release surfaces from being declared fully closed.

## Version Reconstruction

### v1.0.10-v1.0.11

- v1.0.10 is the first in-scope synchronized code/document baseline, but its
  problem and integrity records show a Critical width allegation that was later
  explicitly retracted as a false positive. That event is confidence history,
  not an open Critical endpoint defect.
- The old regression harness targeted v1.0.10 and defaulted to capture mode; its
  PASS output did not independently prove candidate-release parity.
- v1.0.11 made no material scientific text/code transition and did not land its
  planned conversion. It was not, however, a literal package clone: eight
  logical package/process assets disappeared and none were added.

### v1.0.12-v1.0.14

- v1.0.12 materially expanded explanation and corrected the Bragg-Williams sign
  and thermodynamic-versus-phenomenological width scope. Its documentary
  corrections are confirmed; its old test harness remained too narrow for broad
  physical-closure claims.
- v1.0.13 repaired candidate selection/capture semantics, introduced
  electrode-aware direction mapping, propagated `n` through configurational
  entropy, corrected `w`-only handling, and fixed the scalar-voltage dynamic
  branch.
- v1.0.14 added phase-separation and sign/reference controls. Named final-source
  edits exist, while several primary-source claims were still unavailable or
  not claim-level verified.

### v1.0.15-v1.0.18.2

- v1.0.15 deliberately removed the working-grid/recurrence architecture and
  replaced it with pointwise memory. Later controlling records show that this
  API break was approved, not an accidental loss. The grid-threshold jump and
  the direction-dependent tail-sign expression were correspondingly removed or
  corrected.
- v1.0.16 added `n(T)` and its temperature derivative to the entropy/reversible-
  heat route and repaired array-temperature APIs.
- v1.0.17 mainly polished register and consistency. An initially incomplete
  extraction omitted Chapter 2 and the appendix but was repaired before final
  review; this is workflow history, not final artifact loss.
- v1.0.18.1/.2 added optional Einstein voltage/entropy terms. The disabled-path
  behavioral parity claim is distinct from source/AST identity: v1.0.18.2 added
  four functions and changed three executable methods. Headers and fitting-guide
  pointers remained stale at v1.0.16-era identities.

### v1.0.19

- The scope began as a Chapter 1 Fable rewrite and expanded by explicit user
  direction to Chapter 2 and additive code APIs.
- `solve_U_oc`, `entropy_coefficient_x`, `reversible_heat_x`, and `return_terms`
  were added while inherited paths were retained.
- CU-1 corrected a High entropy-sign/molar-conversion error introduced during
  rewrite. Final source is corrected; any claim that the process had zero
  physical errors throughout is false.
- Round-trip evidence remained same-model internal consistency. LCO `Omega`,
  full local T/x electronics, empirical validation, and Chapter 3 remained open.

### v1.0.20

- The controlling plan converted v1.0.20 into a bounded quality/documentation
  edition and deferred substantive extensions to v1.0.21.
- The executable AST is identical to v1.0.19 after release metadata/comments;
  v1.0.20 was not a new scientific implementation.
- It added derivation bridges, caveats, references, and an exact-input convention
  that reproduces the stated 74.351141 mV calculation.
- The handover's blanket statement that no evidence gaps remained conflicts with
  the same release's guide, which retained LCO anchors, frozen electronics, and
  unverified candidate figures. The debt was disclosed elsewhere but the
  handover confidence language is incorrect.
- No independent Chapter 3 was produced.

### v1.0.21

- The Fable master session integrated Q2-Q7: grand-canonical/fluctuation and
  transition-state chains, figures, worked examples, an LCO demonstration, and a
  preliminary Si map.
- The code was not a new physics implementation; its executable AST remained the
  v1.0.20 body with release metadata changes.
- The selected independent Chapter 3 became a 91-line Chapter 1 appendix in this
  release. This is documented scope compression; the independent chapter form
  arrived in v1.0.22.
- Q9/Q10 were explicitly superseded by v1.0.22 R0, not independently completed
  inside v1.0.21.

### v1.0.22

- R1 reorganized by active material: graphite plus thermal content became
  Chapter 1, LCO became a dependent delta-only Chapter 2, and Si/blends became
  Chapter 3.
- Temporary `sec18`/bibliography omissions occurred during R1 and were repaired.
  Final extraction shows zero lost bibliography keys; seven removed labels are
  deliberate navigation labels. Final retention must not be rewritten as an
  omission-free process.
- Chapter 3 primary W drafts came from Opus streams; Fable selected and integrated
  them. Exact-line overlap supports that division. Model identity is provenance,
  not scientific quality.
- The code retained 38 AST-identical inherited functions and added nine
  `BlendedAnodeDQDV` methods. The new blend implementation was additive.
- Named C-040-C-049 edits exist in final TeX, but issue disposition is not proof
  that the corrected model is scientifically valid. A13 remained partially open,
  large Medium/Low pools and skipped items remained, and GS-1/GS-2 and empirical
  validation remained explicit debt.
- The fitting guide was a byte-identical v1.0.20-era carryover and did not
  document the blend API. G3 also did not test the converted 30 wt% Si-C endpoint
  near `f_Si = 0.78`.

### v1.0.23

- v1.0.23 is principally an additive Chapter 1 Appendix E/ratio-method release,
  not a three-chapter scientific rewrite.
- All 17 Chapter 2 and all eight Chapter 3 section bodies are byte-identical to
  v1.0.22. The master roots and PDFs are not byte-identical because version
  metadata changed; extracted scientific text is equivalent after version-token
  normalization. This wording supersedes the first-pass whole-chapter byte-
  identity claim.
- The ratio path is default-off and statically inherits the earlier runtime, but
  behavioral bit-exact parity was not re-executed in the provenance-only pass.
- The v1.0.23 reference ledger is stale and omits `lee2017jcp`, `lee2011jcp`, and
  `son2013jcp`, although all three entries are in the bibliography.
- `appendix_phase_separation.pdf` disappeared while its TeX source remained; it
  is the only non-process scientific release asset lost in the v1.0.22-to-23
  comparison.
- The final handover says curve/image QA is planned, but `CURVE_QA_v23.md` and
  nonblank QA PNGs exist. The stale pending marker is refuted. The QA's sampled
  smoothness does not establish global `C2`, and its activation-enthalpy/lag
  direction sentence conflicts with the implemented exponential.
- The FFT helper uses unpadded circular convolution and lacks a general boundary
  contract. G-E3 uses iterations of the same map without an independent solve,
  residual/convergence assertion, grid refinement, or epsilon-order study; it
  does not certify the stronger fixed-point/error claim.
- The fitting guide still identifies v1.0.20/v1.0.19-era assets, and Chapter 3
  describes already-present R6 code in future tense.

## Prior-Claim Disposition

| Prior claim | Final lineage disposition |
|---|---|
| Zero physics defects, `H0`, or no unresolved evidence | `근거 미발견`. Later corrections and retained debt refute an unbounded reading. |
| Many PASS/model reviews prove correctness | `근거 미발견`. They are bounded process/test evidence. |
| Complete asset retention | `미결`. Scientific labels/citations are substantially retained, but the phase PDF, stale ledger, and stale release surfaces remain. |
| v1.0.21 delivered independent Chapter 3 | `근거 미발견` as an artifact-form claim; it delivered preliminary appendix content. |
| Fable authored all v1.0.22 Chapter 3 drafts | `근거 미발견`; Opus produced primary streams and Fable integrated them. |
| All v1.0.22 High/Medium/Low debt closed | `근거 미발견`; disposition records and scientific closure are different gates. |
| v1.0.23 upgraded all three chapters scientifically | `근거 미발견`; Chapter 2/3 section science was inherited. |
| v1.0.23 ratio path is independently self-consistent/certified | `미검증`; the stated gates do not establish that stronger result. |

## Confirmed Retention And Regression

- **확정:** no bounded evidence of accidental final loss of inherited
  bibliography keys or non-navigation scientific labels at v1.0.22.
- **확정:** v1.0.22 Chapter 3 authorship is Opus-primary-draft plus
  Fable-selection/integration.
- **확정:** v1.0.22 code is additive over 38 AST-identical inherited functions.
- **확정:** v1.0.23 retains all Chapter 2/3 section bodies and changes their
  release wrappers/version metadata only.
- **확정:** the v1.0.23 reference ledger, handover QA state, fitting guide, and
  Chapter 3 future-tense implementation prose are stale.
- **확정:** sampled or same-model tests cannot be promoted to empirical or global
  scientific validation.
- **미검증:** external truth of graphite, LCO, Si, entropy, stress, capacity, and
  fitting claims is controlled by Phases 004-009, not this lineage gate.

## Required Lineage Adjudications

`LINEAGE_PASS` can close only after the project owner authorizes correction or
explicit waiver of these release-control items:

1. Replace whole-Chapter-2/3 byte-identity language with section-body byte
   identity plus version-normalized scientific-text equivalence.
2. Update the v1.0.23 reference ledger with the three JCP entries or explicitly
   declare that ledger non-current.
3. Restore `appendix_phase_separation.pdf` or record an intentional exclusion or
   waiver.
4. Describe v1.0.11 as a scientific-text/code no-op with eight dropped package/
   process assets, not a literal package clone.
5. Correct or explicitly waive the stale v1.0.23 handover QA status, fitting
   guide, and Chapter 3 future-tense implementation prose.

## Verification

- Atomic lineage rows: 300; exact 17-column schema; zero blank or duplicate IDs.
- Atomic evidence status: 206 `확정`, 34 `미결`, 34 `근거 미발견`, 23
  `미검증`, three `추정`.
- Artifact records: 826/826 resolved; zero missing files, size mismatches, or
  SHA-256 mismatches.
- Falsification challenges: 88; all 120 raw Critical/High records covered.
- Falsification schema: exact ten columns; zero blank cells, duplicate IDs, or
  invalid status/severity values.
- Falsification: 45 upheld, 25 downgraded, nine partial, six not testable, two
  refuted, one upgraded.
- Source changes: none.
- Git commands: none.

## Phase Result

The version graph, content inheritance, deliberate moves/deletions, code
inheritance, and authorship provenance are sufficiently reconstructed and
falsified for Phase 003 completion. The appropriate gate is
`LINEAGE_AUDIT_COMPLETE`; `LINEAGE_PASS` remains open for the five explicit
release-control adjudications above.
