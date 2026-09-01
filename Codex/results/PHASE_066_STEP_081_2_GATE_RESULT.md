# Phase 066 Step 81.2 Integrated Gate Result

## Outcome

- Selected gate: `CONDITIONAL_P066`
- Rejected promotion: `PASS_P066_LINEAGE_I`
- Rejected terminal: `FAIL_P066`
- Status: `CONDITIONAL_PENDING_PERSISTENCE`
- Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`
- Expected parent: `bdad7375d70c3734cc63265d94a61dd82afd143d`
- Expected subject: `audit(phase066): close v1025 lineage gate`
- Postcommit persistence terminal: `PASS_P066_STEP81_2_PERSISTENCE`

This is an audit gate record, not the main scholarly body.

## Evidence Integrated

The persisted Phase 066 plan activation and Steps 76–81.1 provide seven precommit
and seven persistence records. The canonical-history denominator is therefore
`14/14`. The explicit collector is the only mode that may replay those records;
ordinary artifact, precommit, and persistence modes must report
`fresh_historical_replay=0/14` and validate the stored history instead.

Cross-binding confirms the following bounded facts:

1. Source/read/process coverage is `433/167`, text `158/30,597`, PDF `6/308`,
   images `3`, narrative `42/9,674`, release/routed process `17/20`, and routed IDs
   `105`, with no read gap or orphan.
2. Direct14 has `14` components and `57` free parameters. Runtime reconstruction is
   cross-runtime reproducible, but `runtime_success=false`, the selected trial is
   nonconverged, and stored↔replay parameters are `NOT_EQUIVALENT`.
   Its raw input is `Claude/results/comp_v24/sintef_data/sigr.csv`, raw SHA-256
   `e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6`,
   with `16,735` rows and exact specimen/protocol binding `GROUND_NOT_FOUND`.
3. The original full-precision optimizer state is `GROUND_NOT_FOUND`; curve
   tolerance equivalence is not parameter identity or physical identifiability.
4. Of eight authority rows only Direct14 has `empirical_pass=true`; all external,
   phase, proposition, and physical authority flags remain false.
5. The fresh default is `4+2`; skew `7+7` is opt-in only. Sixteen routes and `36/36`
   isolated probes do not grant external material/profile/multi-temperature authority.
6. Source dispositions are `424/3/6`; owner registry/active obligations are
   `355/219`; ownerless/multiple/lost/AY-duplicate/external-promotion violations are
   all zero.

The eleven owning-commit/raw-SHA/semantic-seal bindings and their counts/statuses are
enumerated in `Codex/results/PHASE_066_V1025_V1025_2_LINEAGE_REPORT_I.md`; the final
validator checks each committed blob against the current bytes and exact recursive
schema topology.

## Conditional Reasons

- Ref. 7 original full text remains `GROUND_NOT_FOUND`, owned solely by
  `PHASE-071-PRIMARY-SOURCE-ACQUISITION`.
- Original full-precision optimizer state and original runtime diagnostics remain
  `GROUND_NOT_FOUND`.
- Held-out, external, material/protocol, profile, and multi-temperature authority are
  not established.
- Three v1.0.25.2 PDF pairs remain stale byte-identical carryovers from v1.0.25.1.

These are authority ceilings, not clerical omissions. They may not be converted to
resolved status by fit quality, replay agreement, secondary evidence, or disposition
completion.

## Persistence Boundary

Precommit validation must require exactly eight staged paths, result-first and JSON-last
ordering, branch/upstream/live-origin equality at the expected parent, and no changes to
`main`, protected history, production source, or `Claude/**`. This document does not
claim staged PASS because Step 81.2 has not been staged.

Postcommit validation must require exact committed bytes for all eight paths, a clean
worktree/index, exact subject and parent, and local/upstream/tracking/live-origin
equality. Only that state may emit `PASS_P066_STEP81_2_PERSISTENCE`.

## Exact Next Condition

Persist the exact eight Step 81.2 paths, verify the postcommit terminal under Python
3.12 and 3.14, then activate and persist the Phase 067 detailed plan. Cumulative Step
82 must not begin earlier.
