# Phase 003 - v1.0.10-v1.0.23 Version Lineage First-pass Result

## 1. Status

- Phase: 003, Steps 24-34 and 36 first pass complete; Step 35 independent falsification pending.
- Current gate: `LINEAGE_PASS_PENDING_FALSIFICATION`.
- Snapshot: `8ea83fc6825d2e62c360e08d7738ef26d3171914`.
- Git: not used.
- Source artifacts: read-only.
- Canonical first-pass matrix: `Codex/results/v1010_v1023_version_lineage.csv`.

The first-pass matrix contains 300 atomic records:

| Status | Count |
|---|---:|
| 확정 | 206 |
| 미결 | 34 |
| 근거 미발견 | 34 |
| 미검증 | 23 |
| 추정 | 3 |

| Severity | Count |
|---|---:|
| Critical | 13 |
| High | 107 |
| Medium | 74 |
| Low | 29 |
| Info | 77 |

The severity count is an audit-priority count, not a statement that all 13 Critical rows are independently upheld scientific defects. Several are intentionally awaiting refutation or source adjudication.

## 2. Inputs and Direct Coverage

This report integrates six packages that were each fully read and then validated row by row:

| Package | Scope | Atomic rows |
|---|---|---:|
| `L1_v1010_v10182` | v1.0.10-v1.0.18.2 | 56 |
| `L2_v1019_v1020` | v1.0.19-v1.0.20 | 50 |
| `L3_v1021_v1022` | v1.0.21-v1.0.22 | 69 |
| `L4_v1023` | v1.0.23 | 61 |
| `L5_cross_version` | cross-version plans, ledgers, handovers, and claims | 48 |
| `M_main` | independent scientific and code probes | 16 |

The resolved Phase 002 ledger remains the coverage authority: 2,286 snapshot paths received an explicit disposition, including 410,053 text/code lines, 1,418/1,418 required PDF pages, 86/86 required PNGs, and 18/18 required machine artifacts. Phase 003 used the assigned version-local full reads and exact comparisons; it did not infer version history from filenames alone.

## 3. Version-by-version Reconstruction

### v1.0.10-v1.0.11

- v1.0.10 is the first in-scope synchronized code/document baseline, but its own problem and integrity reports show that the handover required correction and clarification.
- v1.0.11 is effectively a no-op package relative to v1.0.10. Version identity changed without a material scientific implementation transition.
- Therefore, any claim that v1.0.11 independently closed new LCO science is unsupported by final-artifact change.

### v1.0.12-v1.0.14

- v1.0.12 materially expanded the explanatory document and fitting guide, but its old regression harness was too narrow to support broad physical-closure language.
- v1.0.13 reorganized and expanded the treatment. The declared two-zero gate was not demonstrated as closed by the final evidence.
- v1.0.14 added the phase-separation appendix and raised tone/rigor, sign, and reference controls. The appendix remained a separately rendered dependency rather than a chapter-integrated artifact.

### v1.0.15-v1.0.18.2

- v1.0.15 removed the hidden working-grid/resampling route and restored direct pointwise evaluation. This is a substantive and beneficial document-code correction.
- v1.0.16 added `n(T)` and propagated its temperature derivative into the reversible-heat path.
- v1.0.17 primarily polished register and consistency rather than creating a new physical model.
- v1.0.18.1/.2 added optional Einstein vibrational corrections with an off-state bit-exact contract.
- The v1.0.18.2 guides and headers still retained stale v1.0.16-era pointers, and no Chapter 3 existed.

### v1.0.19

- The plan started as a Chapter-1-only Fable rewrite, then expanded to Chapter 2 and code under a doc-leads workflow.
- `solve_U_oc`, `entropy_coefficient_x`, `reversible_heat_x`, and `return_terms` were added without perturbing the inherited tested path.
- CU-1 corrected a High sign/molar-conversion error found during review. Earlier zero-physical-error language is therefore historically superseded even though the final CU-1 artifact is corrected.
- The round-trip evidence is synthetic internal consistency, not real-data validation.
- LCO `Omega`, full T/x electronic behavior, and three-part irreversible heat remained unresolved; Chapter 3 did not yet exist.

### v1.0.20

- v1.0.20 became a bounded quality and documentation edition after substantive extensions were deferred to v1.0.21.
- It added derivation bridges, citations, caveats, and a small number of displayed identities, while code function bodies remained those of v1.0.19.
- Candidate Q2/Q3 equations and candidate figures were precursor material, not final v1.0.20 content.
- The handover claim `근거 미발견: 없음` is contradicted by retained LCO anchors, frozen electronic behavior, and real-data debt.
- The guide and visible code-map pointers were not fully synchronized.

### v1.0.21

- D21-6 prime assigned the final integration and writing to one Fable master session.
- Q2 added the multi-class grand-canonical balance and fluctuation chain; Q3 added the transition-state-theory chain; Q4-Q7 added five scientific figures, worked examples, navigation variants, an LCO demonstration, and a Si preliminary map.
- No inherited v1.0.20 scientific label was lost.
- The code was not a new physical implementation: the 1,152-line body differs from v1.0.20 only in version/header identity.
- D21-3 selected an independent Chapter 3, but v1.0.21 delivered a 91-line Chapter 1 appendix. The content exists; the selected artifact form was deferred.
- Q9/Q10 closeout was absorbed into v1.0.22 R0, so a standalone v1.0.21 integrated scientific closeout is not established.

### v1.0.22

- R1 deliberately reorganized by active material: graphite plus all thermal material became Chapter 1, LCO became delta-only Chapter 2, and Si/blends became Chapter 3.
- Navigation-only artifacts were deliberately removed, while their symbol function was partly relocated to local notation tables.
- Temporary `sec18`/bibliography omissions occurred during R1 and were repaired before finalization. The final state is retained; the claim of an uninterrupted omission-free process is false.
- Chapter 3's primary W1/W2/W3 drafts were produced by Opus streams. Fable was the master/cherry-picker, not the primary author of all three drafts.
- Named C-040-C-049 High corrections are present in final TeX.
- This does not close the science: one A13 generalization remained partial, 158 Medium plus roughly 120 Low findings were deferred, twelve Medium and twenty-one R8 items were skipped, and empirical/model gaps remained.
- R6 added `BlendedAnodeDQDV`, three Si presets, `from_wt`, pooled charge balance, and explicit GS-1/GS-2 boundaries.
- G3 tested selected capacity fractions only and did not cover the converted 30 wt% Si-C endpoint near `f_Si=0.78`.
- The fitting guide remained a v1.0.20/v1.0.19 carryover and did not document the new blend API.

### v1.0.23

- v1.0.23 is an additive Appendix E/ratio-method release, not a broad rewrite of Chapters 2 and 3. Those chapters are byte-identical to v1.0.22.
- The optional ratio path is default-off and preserves the frozen route when disabled.
- The v1.0.23 reference ledger was copied from v1.0.22 and omits the three new JCP bibliography entries.
- `appendix_phase_separation.pdf` disappeared from the v1.0.23 package although the TeX source remained.
- The new FFT transfer helper lacks an explicit circular-boundary contract.
- G-E3 compares a same-update Picard-like approximation, not an independent nonlinear fixed-point solution.
- Curve QA states the sign of the activation-enthalpy/lag relation backwards.
- Chapter 3 section 3.5 still speaks in future tense although R6 code already exists.
- Real-data validation and the BDD/fitting program remain outstanding.

## 4. Change Classes and Retention

### Deliberate retention

- Core graphite/LCO equation and code identities were repeatedly preserved through additive releases.
- v1.0.22 retained all preexisting scientific citation keys and all non-navigation scientific labels.
- v1.0.23 retained Chapter 2 and Chapter 3 exactly.

### Deliberate relocation

- v1.0.22 moved old thermal Chapter 2 into Chapter 1 Part T.
- Old LCO Part II moved into Chapter 2 with new intro/notation/bibliography wrappers.
- The v1.0.21 Si appendix became the source dependency for v1.0.22 Chapter 3.

### Deliberate deletion or supersession

- v1.0.22 removed navigation-only editions and seven navigation labels under D22-1.
- Competing drafts, figure candidates, and `comp_v23` surveys remained precursor provenance and were not silently promoted to final science.

### Repaired regression

- R1 temporarily omitted `sec18` and bibliography anchors, then restored them.
- v1.0.19 CU-1 corrected a High entropy-sign error introduced during rewriting.

### Stale or lost release surfaces

- Fitting guides and headers repeatedly lagged the actual API/version.
- The separately rendered phase-separation PDF was no longer shipped in v1.0.23.
- v1.0.23's reference ledger does not include its three new bibliography entries.

No bounded evidence of accidental loss of inherited scientific labels or citation keys was found after the repaired R1 incident. This does not mean that caveats, evidentiary strength, or scientific correctness were preserved perfectly.

## 5. Prior Claims Reopened

| Prior claim | First-pass disposition |
|---|---|
| `H0`, zero physical defects, or no unresolved evidence | `근거 미발견`; later High findings and retained debt refute the broad reading. |
| Model consensus or multiple PASS reports prove science | `근거 미발견`; these are review/process evidence only. |
| Asset retention is complete | `미결`; scientific labels/citations are retained, but release surfaces and phase-separation PDF/reference-ledger synchronization are not. |
| v1.0.21 delivered independent Chapter 3 | `미결`; content was an appendix, chapter form arrived in v1.0.22. |
| Fable authored v1.0.22 Chapter 3 | `근거 미발견`; Opus produced primary streams and Fable integrated them. |
| All v1.0.22 High/Medium/Low debt is closed | `근거 미발견`; substantial pools and skips remain. |
| v1.0.23 is a three-chapter scientific upgrade | `근거 미발견`; it is principally an additive Chapter 1 Appendix E/code change. |
| v1.0.23 ratio path is independently self-consistent and certified | `미결`; the reported gate and epsilon language do not establish that stronger claim. |

## 6. Model-authored Transitions

- v1.0.19: Fable rewrite/review workflow materially changed prose, Chapter 2, and code APIs.
- v1.0.20: competing reviews and drafts influenced quality corrections, but substantive expansion was frozen.
- v1.0.21: Fable master was the final author/integrator and materially expanded the theoretical and pedagogical surface.
- v1.0.22 Chapter 3: Opus streams produced primary candidate drafts; Fable performed final selection and integration.
- v1.0.23: advanced-method surveys and implementation added Appendix E/ratio mechanics, while most final chapter science was inherited.

Model identity is provenance, not evidence quality. No scientific claim is accepted because it was produced by Opus, Fable, or a consensus of models.

## 7. Unresolved at the Lineage Boundary

- External truth of load-bearing graphite, LCO, and Si references is Phase 004-007 work, not closed by the lineage record.
- LCO `Omega`, transition assignments, frozen T/x electronics, and source-to-parameter transfer remain unresolved.
- Chapter 3 SiOx placeholders, mass-basis normalization, finite-strain mechanics, GS-1/GS-2, and identifiability remain unresolved.
- Real-data round trip, fitting stability, uncertainty quantification, and full composition coverage remain unresolved.
- Appendix E's original-source mapping, complete-affinity implementation, residual/fixed-point convergence, FFT boundary behavior, and claimed certificate remain unresolved.
- The merged single-document deliverable is outside the frozen release scope.

## 8. First-pass Gate Decision

Steps 24-34 and 36 are complete at first pass. Step 35 remains mandatory because the merged record contains 13 Critical and 107 High priority rows, some based on direct integrator probes and some based on claims about source support. A fresh Sol critic must attempt to falsify the version graph, asset-retention result, authorship attribution, and every Critical/High lineage conclusion.

Current gate: `LINEAGE_PASS_PENDING_FALSIFICATION`.

## 9. Machine Validation

- Matrix rows: 300.
- Required columns: 17/17.
- Blank record IDs: 0.
- Duplicate package-local IDs: 0.
- Canonical status vocabulary: 5/5 only.
- Canonical severity vocabulary: 5/5 only.
- SHA-256: `023E51D8B4224DA532F4B5697CD04C2EFC667220078EDDC42BBD7B95DB1FEE59`.

The merge script records any normalized original status/severity in the row notes instead of silently erasing it.
