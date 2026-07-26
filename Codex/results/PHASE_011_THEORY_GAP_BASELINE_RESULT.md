# Phase 011 Theory-gap Baseline Result

## Chain

- Active plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-07-20-recent-five-year-theory-literature-review-ch1-ch3-plan.md`
- Plan steps: 148-157
- Canonical audited snapshot: `D:\Projects\Project_Anode_Fit\Codex\work\source_snapshots\8ea83fc6825d2e62c360e08d7738ef26d3171914`
- Gap matrix: `D:\Projects\Project_Anode_Fit\Codex\results\phase011_theory_gap_search_matrix.csv`
- Git commands executed: none
- Writes outside `D:\Projects\Project_Anode_Fit\Codex`: none

## Ground Truth Rechecked

- Phase 006 LCO result was re-read first-to-last. It remains the controlling LCO
  scientific baseline: four Critical and eight High findings prevent a pass.
- The v1.0.23 LCO master include closure and all seven LCO-specific section files
  were read first-to-last. The code paths implementing the electronic entropy,
  transition dataset, entropy coefficient, implicit OCV solve, and LCO subclass
  were directly re-read.
- The visible live `D:\Projects\Project_Anode_Fit\Claude` tree still ends at
  v1.0.19 and has no file newer than 2026-07-13. Every compared v1.0.19 LCO
  section differs from the later audited v1.0.23 snapshot. The snapshot therefore
  remains the newer scientific comparison baseline; neither tree was modified.
- The scientific ledger contains 31 Critical/High findings across Phases 005-007:
  12 Chapter 1, 12 Chapter 2, and 7 Chapter 3. Every ID appears in the gap
  matrix's `linked_findings` field.

## Priority Interpretation

The scope is Chapters 1-3, with LCO as the priority recovery track rather than
the only track. The matrix separates:

1. `must-repair`: a present equation, source identity, code path, inference claim,
   or chapter contract is unsound or unverified at load-bearing level.
2. `valuable-enrichment`: recent theory may add state variables or validity tests
   that materially improve the model but is not required to correct an existing
   false statement.
3. `scope-boundary`: the source is needed to state where the reduced model stops,
   not to import new high-voltage or degradation physics into the current model.

## LCO Recovery Questions Fixed Before Search

The search will not treat the current logistic gate as the default truth. It must
answer, independently:

- whether an explicit occupational order parameter, sublattice model, or cluster
  expansion is required for the `x=1/2` and related ordered phases;
- whether a recent direct LCO source derives any composition-local logistic
  electronic DOS/entropy gate;
- whether electronic, configurational, vibrational, magnetic, strain, and
  microstructural contributions can be separated from the available observables;
- how a finite-temperature free energy maps to chemical potential, voltage,
  phase fractions, and ICA/DVA without promoting empirical width to entropy;
- which minimal, order-parameter, and cluster-expansion-informed recovery options
  are implementable and externally testable.

## Gate

`THEORY_GAP_BASELINE_PASS`.

Reason: all 31 controlling Critical/High findings have an explicit search or
non-search disposition, all three chapters are represented, LCO is designated as
the priority deep-recovery track, and prohibited material/model transfers are
recorded before source discovery.
