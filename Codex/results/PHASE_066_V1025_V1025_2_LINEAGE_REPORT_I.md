# Phase 066 v1.0.25/v1.0.25.2 Lineage Report I

## Document Role

This is a lineage-audit record, not the main scholarly body and not a substitute for
the v1.0.25/v1.0.25.2 LaTeX or PDF deliverables. It integrates the persisted Phase 066
activation and Steps 76–81.1 without promoting missing source, optimizer, experiment,
material, or publication evidence.

## Result-First Persistence Contract

- Selected phase gate: `CONDITIONAL_P066`
- Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`
- Expected parent: `bdad7375d70c3734cc63265d94a61dd82afd143d`
- Expected subject: `audit(phase066): close v1025 lineage gate`
- Postcommit persistence terminal: `PASS_P066_STEP81_2_PERSISTENCE`
- Declared final path count: `8`
- Canonical-history denominator: precommit `7` + persistence `7` = `14`
- Ordinary validation fresh historical replay: `0/14`
- Fresh historical collection is permitted only through the validator's explicit
  `--collect` mode.

## Integrated Evidence Boundary

The integrated denominator is the persisted Phase 066 plan activation plus the
persisted Step 76, 77, 78, 79, 80, and 81.1 commits. Each unit is bound to its exact
commit, parent, subject, declared path set, result bytes, machine-artifact bytes,
semantic seal, validator bytes, precommit terminal, and persistence terminal in
`PHASE_066_VALIDATION.json`. The stored fourteen-record canonical history is reused
by ordinary artifact, precommit, and persistence validation.

### Machine evidence cross-bind

| Machine artifact | Owning commit | Raw SHA-256 | Semantic SHA-256 | Bound status/count |
|---|---|---|---|---|
| `Codex/results/PHASE_066_PLAN_ACTIVATION_VALIDATION.json` | `f9ee0599ff07d36e4b23547a835549552a51ce26` | `00b4cc2f3f184cd17ed4b326d94194e3cd4fb7500277e5b6ca09c160a5f7e841` | `d0f5d42b6a404c196541e26e6d7297ac73c5ccd20669230ff2c15e0b8e832101` | activation persisted |
| `Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json` | `38e00020906e3a024e493c214c1a99a6f8ab07d2` | `e24462702966dfb679953c6726b20b923eb7cf9591a24ba5297e7b20308f4d2b` | `4df7d88cac29b09301645b4477fe30d3952a01abb27a4720a29f347b75b67a1c` | source `433/167`, process `17/20` |
| `Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json` | `38e00020906e3a024e493c214c1a99a6f8ab07d2` | `b419291dca9849e94f1b7e4fa4a3ddc08970385e446dca45f15d469777bcfcfe` | `381ae01809a56ac4aa23a786a6170033057df4e838956b535e55bb3bad7e96c3` | text `158/30,597`, PDF `6/308`, image `3/3` |
| `Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json` | `5d26e0746864cea7a8bd37a22874093b73c1a12f` | `ff8141e7f0d950cfb6f588f41743e7b9221c5f4cb73ecc76522b0beb45a70d80` | `567c8b65886851e34fff8e913e6ad81819d8ce022001df6bf20a9b26fce6b029` | actual fit executed; selected trial nonconverged; `runtime_success=false` |
| `Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json` | `5d26e0746864cea7a8bd37a22874093b73c1a12f` | `ce8b9b8d6c2941833351f1651ec85b4e9075b96bdcfd1cc93bbc16ccb4e7a6e0` | `e56db8c1eb226596d5bee98147444125d030fe969422dd542241eb64692b5a4e` | raw rows `16,735`; exact specimen/protocol binding `GROUND_NOT_FOUND` |
| `Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json` | `fedb2031fbfabeaba84f86427c35334526234d73` | `d9dead0f766abeed899e7357b964719361054d87e31ded971fb3640b3182656e` | `86842e6e53164271b70ae4b9410223b9aa40be4d85692c15f669c5c08a5b7418` | original-state fields `25/25` `GROUND_NOT_FOUND` |
| `Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json` | `d091e7881f9f22d5dfe9511427afdf4ef22e3280` | `2bb07774d5ea59b578dcfc1520a3e524ec32b42ca590a90b5cca967ae63499a1` | `ccf7a972cd5a061840cf83bd3d6861bd3c840361433245d5fbf75ad3445a62ba` | rows `8`; empirical PASS `1`; external/material authority `0` |
| `Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json` | `ec02d8e0017c4441d9d02c08e22ad432b8c47bc5` | `7bab3f907ab6879fec0854c94f05e7d0b42fc618d6585f2737750e2a2b1b0695` | `da615e36ce8df9d16e8ca7dfb69d1a74137510c1212cf2e2fcb53e8850fc2f75` | routes `16`; temperature dependent/independent `9/7` |
| `Codex/results/PHASE_066_RUNTIME_ATTESTATION.json` | `ec02d8e0017c4441d9d02c08e22ad432b8c47bc5` | `a5c909105280cf11a72ca9189070feb59c9005a824eeee4f3e161660394539d4` | `3a393149d36513233e46ebbdbb0ce36f0393e28cb88e1fd3704cef5bf83fb040` | isolated processes `36/36` |
| `Codex/results/PHASE_066_SOURCE_DISPOSITION_MATRIX.json` | `bdad7375d70c3734cc63265d94a61dd82afd143d` | `a04e5567b9771b299742fa5f3c2313559f51f32b41ba1844d823b4e0162257de` | `005bd904dc3225df1cd82906be5ff08a54e55dbe8f36521520b87a24d7a31569` | `PRESERVE/CORRECT/WITHHOLD=424/3/6` |
| `Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json` | `bdad7375d70c3734cc63265d94a61dd82afd143d` | `847e74956d16cc9bdcc42c36b0ddd1d73ea5ac79464d55461d2e08cf09a60003` | `b7847cd1ce29fee7b0304c1ee92e81645ab149949a80aab1d9c6fc77003856c6` | owner registry/active `355/219`; Ref. 7 `GROUND_NOT_FOUND` |

### Source/read/process reconstruction

- Manifest occurrences / unique blobs: `433/167` across releases `143/144/146`.
- Unique text / physical lines: `158/30,597`; PDFs / pages: `6/308`; images: `3`.
- Narrative controls: manifest-backed `40/9,019`, supplemental `2/655`, expanded
  total `42/9,674`.
- Routed process denominator: `20`; release commits: `17`; routed reference IDs:
  `105`.
- Independent read coverage: occurrences `433/433`, blobs `167/167`, text
  `158/158`, PDF pages `308/308`, images `3/3`, narrative lines `9,674/9,674`.
- Pairwise occurrence deltas are `143/133/10/1/0` for v1.0.25→v1.0.25.1,
  `144/133/11/2/0` for v1.0.25.1→v1.0.25.2, and `143/127/16/3/0` for
  v1.0.25→v1.0.25.2, in shared/same/changed/added/removed order.
- The three v1.0.25.2 PDF pairs remain byte-identical to the v1.0.25.1 PDFs.
  They are stale genealogy evidence, not proof of a v1.0.25.2 rebuild.
- One clipped PDF equation and nine embedded-plot Korean glyph defects remain
  recorded. No defect is silently repaired or promoted here.

### Direct14 fit and optimizer reconstruction

- The stored raw input is `Claude/results/comp_v24/sintef_data/sigr.csv`, SHA-256
  `e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6`, with
  `16,735` rows. It is an `absolute_mAh_not_mass_normalized` axis; exact specimen and
  protocol binding status is
  `SOURCE_DECLARED_BUT_EXACT_BINDING_GROUND_NOT_FOUND` (`GROUND_NOT_FOUND`).
- The processed fit input has `1,280` points. The optimizer contract has `14`
  components, `57` free parameters, `12` deterministic starts, and
  `max_nfev=6000`.
- Optimizer execution completed, but the selected trial did not converge and the
  Step 77 runtime success is `false`.
- Replay is numerically reproducible across Python 3.12 and 3.14. Stored↔replay
  ordered parameters are not equal; their maximum parameter difference is
  `1.2482043497`. The curve is tolerance-equivalent, with curve RMSE
  `0.0005229` and relative cost difference `0.0000531`.
- The original full-precision optimizer state and its original runtime diagnostics
  are `GROUND_NOT_FOUND`. Stored rounded parameters, current replay parameters,
  and curve equivalence are not substituted for that missing state.

### Authority adjudication

- Step 79 contains `8` closed-schema claim rows. Direct14 is the only row with
  `empirical_pass=true`.
- External authority, phase authority, proposition authority, and physical authority
  are false for all eight rows. Held-out testing is not established for six rows;
  Ref. 7 primary full text remains unavailable for the literature row.
- Fit quality is therefore bounded empirical evidence. It is not proof of unique
  parameter identifiability, a physically true decomposition, exact material or
  protocol provenance, or external predictive validity.
- Ref. 7 original full text remains `GROUND_NOT_FOUND` under sole owner
  `PHASE-071-PRIMARY-SOURCE-ACQUISITION`. No substitute citation or secondary
  description is promoted to primary-source authority.

### Profile/default/temperature adjudication

- Step 80 closes `16` route rows with `36/36` successful isolated-process probes.
- A fresh default is `GRAPHITE_STAGING_LIT_4_PLUS_SIC_LIT_2`; skew `7+7` is an
  explicit/toggle opt-in route only. No process-global order leak was observed.
- Temperature-dependent / independent routes are `9/7`.
- These routing results establish implementation behavior only. External material,
  profile correctness, and multi-temperature authority remain false.

### Disposition and carry-forward

- Source dispositions are `PRESERVE/CORRECT/WITHHOLD=424/3/6`; supplemental
  controls are `2`; routed/release process records are `20/17`.
- Phase 057 prior/new/AY-overlap/union counts are `82/95/10/177`; Step 76–80
  disposition records total `68`.
- Owner registry / active obligation counts are `355/219`. Ownerless, multiple-owner,
  lost-obligation, AY-duplicate, and external-promotion violations are all `0`.
- The above closes accounting, not the underlying missing evidence.

## Gate Adjudication

### Confirmed

- The v1.0.25/v1.0.25.2 source, read, process, fit, optimizer, authority, profile,
  default, temperature, and disposition assertions are cross-bound to their
  persisted evidence.
- Historical activation and Step 76–81.1 validation evidence is preserved as an
  exact `14`-record canonical history.
- Step 81.2 uses result-first documents and a JSON-last deterministic collector.

### Ground Not Found

- Ref. 7 original full text.
- Original full-precision optimizer state and original optimizer diagnostics.
- Exact specimen/protocol binding for the stored raw Direct14 input.
- Evidence sufficient to convert the stale v1.0.25.2 PDFs into current rebuilt
  publication artifacts.

### Authority Ceiling

The selected gate is `CONDITIONAL_P066`. `PASS_P066_LINEAGE_I` is rejected because
the missing primary source, missing original optimizer state, absent held-out,
external, and material authority, and stale PDFs remain open. `FAIL_P066` is also
rejected because the bounded internal lineage reconstruction and disposition
accounting are complete and reproducible within their stated ceiling.

## Next-Phase Recovery Boundary

Step 81.2 must first be persisted as exactly the eight declared paths with the
expected parent and subject, pushed, and verified under Python 3.12 and 3.14 as
`PASS_P066_STEP81_2_PERSISTENCE`. Only then may the Phase 067 detailed plan be
activated. Cumulative Step 82 remains blocked until that activation persists.
Phase 067 must inherit every unresolved authority item without rewriting it as
resolved.
