# Phase 061 v1.0.20 Lineage Reaudit Implementation Plan

> **For Codex:** Execute this plan one cumulative Step at a time. Save the Step result first, validate it, then commit and push the exact declared path set. Do not begin Step 46 until this detailed-plan activation unit itself has been committed, pushed, and remote-verified.

정본일: 2026-08-26

활성 branch: `codex/anode-fit-v1025_2-canonical-completion`

Phase: 061

Cumulative Steps: 46–51, executed as 46, 47, 48, 49, 50, 51.1, 51.2

Goal: frozen baseline의 v1.0.20 source 232경로를 전건 감사하고, v1.0.19에서 실제로 바뀐 내용, 내부 process/review 주장, 경쟁 초안, 채택 문건, 인용·수식·그림 권위의 경계를 분리하여 `PASS_P061_LINEAGE_D`, `CONDITIONAL_P061`, `FAIL_P061` 중 하나만 선택한다.

Architecture: immutable manifest → exact source/read topology → process/authority matrix → v1.0.19↔v1.0.20 delta and snapshot genealogy → citation/equation authority matrix → review/visual artifact matrix → one-row-per-source disposition and carry-forward delta → integrated Lineage Report D and exclusive gate.

Tech Stack: Git object reads at frozen commit, Python 3 strict JSON validators, LaTeX/PDF structural inspection, Poppler-compatible page rendering for visual review, image inspection, SHA-256/Git-blob identity, Markdown recovery records, atomic Git commit/push/persistence checks.

## Summary

Phase 061은 Claude v1.0.20 결과를 좋은 문장이나 빌드 성공 여부만으로 평가하지 않는다. release source, 계획·결과·검토 문건, 경쟁 초안, snapshot, PDF, 그림, 코드·테스트를 같은 권위로 취급하지 않고 각각의 역할과 채택 상태를 먼저 복구한다. 그 뒤 v1.0.19와의 실제 blob/text/equation/citation 차이를 독립적으로 재현하고, 모든 232 source occurrence에 정확히 하나의 disposition과 후속 target을 부여한다.

이 Phase의 PASS는 계보·감사·분류·routing 완결성만 뜻한다. primary literature 원문과 DOI의 진실성, 외부 재료 물성, 실험 데이터 적합성, canonical equation/model 선택, 결함 수리, 최종 학술 LaTeX/PDF, publication readiness는 후속 Phase의 별도 gate 없이는 확립되지 않는다.

## Current Ground Truth

### Git and protection state

- 활성 branch/HEAD/upstream/live origin tip: `codex/anode-fit-v1025_2-canonical-completion` / `136a73804d714706bad1be6d58c99351e606fe0e`.
- Phase 060 final commit subject: `audit(phase060): close v1019 lineage gate`.
- 보호 Codex tip: `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`.
- `origin/main`: `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`.
- Frozen source baseline: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`.
- frozen baseline과 보호 tip 사이 `Claude/**` tracked diff는 0이며 Phase 061은 `Claude/**`를 수정하지 않는다.

### Predecessor gate

- Phase 060은 `PASS_P060_LINEAGE_C`로 닫혔다.
- Step 45.2 exact-eight commit/push/remote persistence는 완료됐고 local/upstream/live origin은 같은 commit을 가리킨다.
- inherited carry-forward 52건은 `OPEN=41`, `PRESERVED_ACTIVE=11`; acceptance satisfied/resolved는 0/0이다.
- Phase 060 신규 blocker 5건도 모두 OPEN이며 Phase 061이 해결했다고 임의 승격하지 않는다.
- target Phase 061인 inherited/new carry item은 0건이다. 이는 Phase 061 source 232경로 감사를 생략한다는 뜻이 아니다.
- Phase 060 source disposition 중 target Phase 061인 evidence route는 36건이다. 이는 inherited/new carry identity와 다른 계층이며 Step 46–51에서 전건 consume/re-adjudicate하되 자동 resolution하지 않는다.

### Frozen v1.0.20 corpus

Phase 056 source manifest에서 다음 immutable predicate로 exact source set을 정의한다.

```text
manifest = Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json
manifest_historical_current_checkout_raw_sha256 = 21c74d2714ad2777445c839a6c9b877d186824cbf15b0bb0cedefefc0b665557
manifest_canonical_utf8_lf_normalized_sha256 = 60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef
baseline_commit = 3b5fd059ed09cdcdde38668c399cb35b8afbcca9
exact_set = every manifest.entries row whose version is exactly "v1.0.20"
```

이 filter는 경로 표본이나 glob이 아니라 232행 전건의 exact machine boundary다. Step 46 machine artifact가 232개 exact path를 정렬된 명시 목록으로 materialize하고 이후 모든 Step은 그 목록을 재사용한다.

확인된 inventory:

- 232 path occurrences, 231 unique Git blobs, 8,158,832 bytes.
- review mode: `FULL_TEXT=195`, `FULL_PDF=14`, `FULL_IMAGE=23`.
- text: 31,553 physical lines, 29,335 nonblank lines, 2,154,776 bytes.
- PDF: 14 files / 130 pages.
- image: 23 occurrences / 23 unique blobs.
- extension: JSON 11, Markdown 69, PDF 14, PNG 23, Python 8, TeX 105, TXT 2.
- role: code 1, figure 23, generated document 14, implementation guide 1, plan 10, result 141, test 1, theory 41.
- v1.0.19과 shared blob identity: 18 occurrences / 18 unique blobs; new blob occurrence는 214 / 213 unique다.
- same-relative-path comparison pair는 47개이며 그중 identical blob 18, changed blob 29다. Versioned Python은 파일명이 달라 별도 semantic/AST comparison이 필요하다.
- 내부 duplicate group은 정확히 하나다. Blob `8dfea239d1787582c6c37c41fe6d06f7b204d72b`를 `snapshot_v1020_p5.json`과 `snapshot_v1020_p6.json` 두 경로가 공유한다.
- v1.0.20 범위에는 NPZ나 별도 binary-introspection item이 없다.

### Provisional intent observations that must be reverified

Phase 057의 v1.0.20 intent recovery는 계획 입력일 뿐 Phase 061 결론이 아니다. 다음 관찰은 frozen source를 다시 읽고 독립 delta를 재현하기 전까지 `PROVISIONAL`이다.

- v1.0.20은 새 물리 구현보다 품질·명료성·인용·그림·리뷰 보강판으로 보인다.
- Ch1에는 bare-site/background 계열 6개 equation asset과 bibliography 확대가 있고 Ch2는 주로 bibliography 확대일 가능성이 있다.
- P5/P6 snapshot은 byte-identical일 가능성이 있으나 구조 증거일 뿐 과학 진실이 아니다.
- multi-review consensus, green build, `H=0`, equation hash stability는 각각 제한된 내부 evidence이며 외부 물리 권위가 아니다.
- Q2/Q3와 figure competition 산출물은 v1.0.21 후보 또는 내부 경쟁 draft일 수 있어 v1.0.20 adopted truth와 분리해야 한다.
- citation key/metadata 혼합 가능성, LCO/Si material law, two-phase width law, Mott/logistic gate 등은 여전히 검증되지 않았을 수 있다.
- P8 final result/log는 source에서 직접 찾지 못할 가능성이 있으며 없으면 추정하지 않고 `GROUND_NOT_FOUND`로 남긴다.

## Phase Range

| Phase | Cumulative Steps | Name | Mandatory Gate | Next |
|---|---|---|---|---|
| 061 | 46–51, actual 46/47/48/49/50/51.1/51.2 | v1.0.20 lineage reaudit | exactly one of `PASS_P061_LINEAGE_D`, `CONDITIONAL_P061`, `FAIL_P061` | Phase 062 detailed-plan activation before Step 52 |

Step numbering does not restart. Substeps 51.1 and 51.2 split disposition from integrated closure without creating a new cumulative Step family.

## Exact Read Inputs

### Control inputs — full read at every recovery boundary

- `Codex/AGENTS.md`
- `Codex/plans/phase_planning_operations_guide.md`
- `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`
- `Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`
- `Codex/plans/2026-08-25-phase060-v1019-lineage-detailed-plan.md`
- `Codex/results/PHASE_060_RESULT.md`
- `Codex/results/PHASE_060_STEP_045_2_GATE_RESULT.md`
- `Codex/results/PHASE_060_V1019_LINEAGE_REPORT_C.md`
- `Codex/results/PHASE_060_VALIDATION.json`
- `Codex/results/PHASE_060_V1019_DISPOSITION_MATRIX.json`
- `Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json`
- `Codex/results/PHASE_059_CARRY_FORWARD_REGISTER.json`
- `Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json`
- `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
- `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

### Phase 057 intent inputs — full read in Step 47

- `Codex/results/PHASE_057E_V1020_FOUNDATION_INTENT_OBSERVATIONS.md`
- `Codex/results/PHASE_057F_V1020_P2_P6_INTENT_OBSERVATIONS.md`
- `Codex/results/PHASE_057G_V1020_P7_REVIEW_DIRECTION_OBSERVATIONS.md`
- `Codex/results/PHASE_057H_V1020_CLOSING_DIRECTION_INTENT_OBSERVATIONS.md`
- `Codex/results/PHASE_057I_V1020_SNAPSHOT_LINEAGE_OBSERVATIONS.md`

### Primary v1.0.20 release/process corpus — exact 232-path set

Step 46은 frozen manifest의 exact predicate를 사용해 232경로 전부를 정렬된 machine list로 기록한다. 사람의 손으로 다시 입력한 경로 목록을 정본으로 삼지 않는다. 필수 분할은 다음과 같다.

- root code/fitting/handover and three root documents.
- `_sections` 39 TeX sections: Chapter 1 24, Chapter 2 15.
- appendix TeX/PDF, Chapter 1 root TeX/PDF, Chapter 2 root TeX/PDF.
- `figs` 5 items and all figure-competition items.
- plans 10: master plus P0–P8.
- results 168, including top-level results and all competition/review/snapshot groups.
- one frozen test source.

Manifest-order recovery groups are fixed as final/release surfaces 53, master/P0–P8 plans 10, core process/results 31, competitive drafts/reviews/figure candidates 126, snapshots 10 occurrences/9 blobs, structure tool 1, and test gate 1. Step 46 preserves the manifest `role` field and records any derived final/adopted authority group separately; it must not rewrite a manifest role to make the topology look cleaner.

Every FULL_TEXT file must be read from first line through EOF. Every PDF page must be rendered or otherwise visually inspected page-by-page. Every image occurrence must receive a visual inspection record even when a blob is duplicated; duplicate blobs may share pixel analysis only if both path occurrences remain separately attested.

### v1.0.19 comparison corpus

Step 48 uses the frozen v1.0.19 release rows from the same manifest and Phase 060 topology as comparison only. Comparison-source reads do not change the v1.0.20 denominator and no v1.0.19 disposition is rewritten.

## Non-goals and Scope Guards

- Do not modify `Claude/**`, protected branches, `main`, source LaTeX, PDFs, PNGs, Python, test data, snapshots, plans, or results.
- Do not select a final canonical model or repair scientific defects in Phase 061.
- Do not treat process plans, self-review, multi-review consensus, build success, snapshots, generated figures, or equation hashes as primary scientific authority.
- Do not validate DOI/primary-paper claim support beyond recording exact claims and routes. External source truth belongs to Phase 071 unless an earlier lineage gate only checks metadata consistency.
- Do not treat Q2/Q3 or other competitive drafts as adopted v1.0.20 content without a source-backed adoption edge.
- Do not claim experiment, held-out fit, identifiability, material validity, final manuscript, or publication readiness.
- Do not introduce code discussion into scholarly main-body source. Phase 061 only audits historical artifacts and writes Codex audit records; any later implementation discussion must remain in its designated appendix/companion.
- Do not silently resolve inherited 52 items or Phase 060 new blockers 5. Preserve identity, status, acceptance criteria, authority, and target unless direct evidence proves an allowed delta.
- Do not stage ignored caches, rendered temporary pages, browser state, credentials, local configuration, or disposable clones.

## Implementation Changes

### Plan activation

1. `Codex/plans/2026-08-26-phase061-v1020-lineage-detailed-plan.md`
2. `Codex/work/v1020_phase061/validate_phase061_plan.py`
3. `Codex/results/PHASE_061_PLAN_ACTIVATION_VALIDATION.json`
4. `Codex/results/PHASE_061_PLAN_ACTIVATION_RESULT.md`
5. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

### Step 46

- `Codex/work/v1020_phase061/build_phase061_step46_source_topology.py`
- `Codex/work/v1020_phase061/validate_phase061_step46.py`
- `Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json`
- `Codex/results/PHASE_061_V1020_READ_ATTESTATION.json`
- `Codex/results/PHASE_061_STEP_046_SOURCE_TOPOLOGY_RESULT.md`
- both execution ledgers and active handover.

### Step 47

- `Codex/work/v1020_phase061/build_phase061_step47_process_authority.py`
- `Codex/work/v1020_phase061/validate_phase061_step47.py`
- `Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json`
- `Codex/results/PHASE_061_STEP_047_PROCESS_AUTHORITY_RESULT.md`
- both execution ledgers and active handover.

### Step 48

- `Codex/work/v1020_phase061/build_phase061_step48_lineage_diff.py`
- `Codex/work/v1020_phase061/validate_phase061_step48.py`
- `Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json`
- `Codex/results/PHASE_061_V1020_SNAPSHOT_GENEALOGY.json`
- `Codex/results/PHASE_061_STEP_048_LINEAGE_DIFF_RESULT.md`
- both execution ledgers and active handover.

### Step 49

- `Codex/work/v1020_phase061/build_phase061_step49_citation_authority.py`
- `Codex/work/v1020_phase061/validate_phase061_step49.py`
- `Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json`
- `Codex/results/PHASE_061_STEP_049_CITATION_AUTHORITY_RESULT.md`
- both execution ledgers and active handover.

### Step 50

- `Codex/work/v1020_phase061/audit_phase061_step50_review_artifacts.py`
- `Codex/work/v1020_phase061/validate_phase061_step50.py`
- `Codex/results/PHASE_061_V1020_REVIEW_ARTIFACT_MATRIX.json`
- `Codex/results/PHASE_061_V1020_VISUAL_READ_ATTESTATION.json`
- `Codex/results/PHASE_061_STEP_050_REVIEW_ARTIFACT_RESULT.md`
- both execution ledgers and active handover.

### Step 51.1

- `Codex/work/v1020_phase061/build_phase061_step51_dispositions.py`
- `Codex/work/v1020_phase061/validate_phase061_step51_dispositions.py`
- `Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json`
- `Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json`
- `Codex/results/PHASE_061_STEP_051_1_DISPOSITION_RESULT.md`
- both execution ledgers and active handover.

### Step 51.2

- `Codex/work/v1020_phase061/validate_phase061_final.py`
- `Codex/results/PHASE_061_VALIDATION.json`
- `Codex/results/PHASE_061_V1020_LINEAGE_REPORT_D.md`
- `Codex/results/PHASE_061_STEP_051_2_GATE_RESULT.md`
- `Codex/results/PHASE_061_RESULT.md`
- both execution ledgers and active handover.

## Plan Activation Unit — Save Before Step 46

### Activation A — Recovery and validator-first RED

1. Re-read all control inputs and verify Phase 060 persistence at `136a73804d714706bad1be6d58c99351e606fe0e`.
2. Save this detailed plan before any v1.0.20 source audit begins.
3. Write `validate_phase061_plan.py` and first run it before activation result/control edits exist. It must fail with named diagnostics, not traceback or silent success.
4. The validator must strict-parse the 24,507-line manifest and full-traverse all JSON nodes; duplicate keys and non-finite numbers are fatal.

### Activation B — Exact plan and source-boundary validation

1. Verify ordered plan sections, exact cumulative Step headings, source counts, role/mode/extension counts, duplicate group, comparison boundary, gates, outputs, stop conditions, atomic commit/push rules, and Phase 062 boundary.
2. Verify all 232 manifest rows resolve to the recorded baseline Git blob and reproduce text/PDF/image extents.
3. Verify carry-forward target Phase 061 count is zero without dropping inherited 52 or new blocker 5 from later routing.
4. Run semantic negative probes and deterministic reconstruction. Every mutation must be rejected by its intended diagnostic.

### Activation C — Result, control records, exact commit and persistence

1. Save `PHASE_061_PLAN_ACTIVATION_RESULT.md` with actual reads, commands, RED/PASS evidence, confirmed/unverified/ground-not-found, protection state, and exact next condition.
2. Update only the Phase 061 rows and append the activation checkpoint to both ledgers; reconcile the stale Phase 060 Step 45.2 precommit sentinel to commit `136a73804d714706bad1be6d58c99351e606fe0e`.
3. Update active handover to make this plan current, record the closed Phase 060 persistence checkpoint, and name Step 46 as blocked until activation persistence passes.
4. Stage exactly the seven plan-activation paths, commit subject `docs(phase061): plan v1020 lineage reaudit`, push the active branch, and verify parent, subject, exact path set, clean status, local/upstream/live-origin equality, protected/main tips, and Claude diff 0.

Activation gate: `PASS_P061_PLAN_ACTIVATION`. Failure or missing remote recovery point blocks Step 46.

## Phase 061 — v1.0.20 Reaudit

### Step 46 — Frozen Source Topology and Full-read Attestation

#### Task 46A — Recovery and exact queue

1. Re-read this plan, activation result, both ledgers, handover, Phase 060 result/gate, source manifest, and relevant carry registers.
2. Resolve every `version == "v1.0.20"` manifest entry against baseline Git objects and freeze the sorted 232-path queue.
3. Prove 232 occurrences/231 blobs, exact review modes, roles, extensions, bytes, duplicate group, and v1.0.19 overlap/new counts.

#### Task 46B — Validator-first RED and complete read

1. Run Step 46 validator before topology/attestation artifacts exist and capture its named failure.
2. Read all 195 text files line 1–EOF, recording physical/nonblank lines, byte count, content SHA-256, Git blob, decoding, and completion state.
3. Render/inspect all 14 PDFs page 1–130 and all 23 image occurrences; record page/image evidence without inferring scientific truth from appearance.
4. Record source role, authority class, group, basename, duplicate/overlap relation, and read mode per occurrence.

#### Task 46C — Validation and checkpoint

1. Validate no missing/orphan/duplicate-attestation row; strict JSON, extent totals, Git blobs, deterministic reconstruction, and negative mutations.
2. Save `PHASE_061_STEP_046_SOURCE_TOPOLOGY_RESULT.md` before committing.
3. Exact-eight commit subject: `audit(phase061): freeze v1020 source topology`.
4. Push and remote-tip verification are mandatory. Step 47 is blocked until persistence passes.

Gate: `PASS_P061_STEP46_SOURCE_TOPOLOGY`.

### Step 47 — Direction, Style, Process and Authority Audit

#### Task 47A — Process corpus full read

1. Re-read all Phase 057 E–I observations as provisional intent evidence.
2. Re-read the v1.0.20 master, P0–P8 plans, phase results, step logs, direction reports, style rubric, reference ledger, review records, and competing-draft instructions from the frozen 232-path set.
3. Track P0–P8 planned/actual/result/gate relationships and record any missing P8 completion evidence as `GROUND_NOT_FOUND`.

#### Task 47B — Authority matrix

For each process claim, record claimant path/line range, object, claim type, expected evidence, actual evidence path, adoption edge, contradiction, authority ceiling, and downstream target. Required authority classes include `USER_REQUIREMENT`, `PLAN_INTENT`, `PROCESS_SELF_ASSESSMENT`, `INTERNAL_REVIEW`, `COMPETING_DRAFT`, `ADOPTED_RELEASE_SOURCE`, `STRUCTURAL_WITNESS`, `EXTERNAL_SCIENTIFIC_UNVERIFIED`.

No plan/result/review statement may promote a competitive asset, bibliography entry, equation, figure, parameter, or code claim beyond evidence actually present in adopted release source.

#### Task 47C — Validation and checkpoint

1. Require every process document and every extracted claim to have exactly one authority class and evidence route.
2. Reject missing adoption edges, circular self-certification, false P8 closure, and process-to-science promotion via negative probes.
3. Save result first; exact-seven commit subject `audit(phase061): adjudicate v1020 process authority`; push and remote-verify before Step 48.

Gate: `PASS_P061_STEP47_PROCESS_AUTHORITY` or bounded `PASS_WITH_CONCERNS` only when coverage is complete and unresolved authority debts remain routed.

### Step 48 — v1.0.19↔v1.0.20 Delta and Snapshot Genealogy

#### Task 48A — Actual release delta

1. Pair v1.0.19 and v1.0.20 source by normalized role/chapter/section identity, never by basename alone.
2. Record added/deleted/modified/unchanged/renamed/copied occurrence classes, old/new blobs, exact text hunks, equation-label/hash changes, bibliography changes, include topology, code/test changes, and generated-PDF/page deltas.
3. Independently verify the provisional Ch1 `+6 equation blocks/+6 labels/+8 bibliography` and Ch2 bibliography-only claims or replace them with measured results.

#### Task 48B — Snapshot and adopted-source genealogy

1. Parse all v1.0.20 snapshots strictly and compare stage-to-stage structures and source pointers.
2. Preserve the exact P5/P6 duplicate occurrence relation and prove whether it is byte-identical.
3. Separate structural witness, generated output, source-of-record, competitive candidate, and adopted content. Snapshot or PDF equality does not prove scientific correctness.
4. Independently compare frozen Python/test content to v1.0.19; version-string or pointer changes must not be confused with behavioral changes.

#### Task 48C — Validation and checkpoint

1. Require all 232 occurrences to appear in the delta matrix exactly once and every comparison edge to resolve to both blobs.
2. Negative probes cover wrong pairing, dropped add/delete, false unchanged, duplicated snapshot identity, equation-hash promotion, and generated/source inversion.
3. Save result first; exact-eight commit subject `audit(phase061): trace v1019-v1020 lineage delta`; push and remote-verify before Step 49.

Gate: `PASS_P061_STEP48_LINEAGE_DIFF`.

### Step 49 — Citation, Background and Equation-authority Audit

#### Task 49A — Citation and equation inventory

1. Extract all bibliography entries, citation keys, cite occurrences, displayed-equation labels, equation bodies, new background prose claims, and explicit source-attribution statements from adopted release source.
2. Link each v1.0.20 addition to its old/new delta and process rationale without treating rationale as support.
3. Distinguish bibliographic metadata consistency from primary-source claim support. Phase 061 may flag malformed/mixed keys and metadata conflicts, but uninspected primary-source truth remains `UNVERIFIED_EXTERNAL` and routes to Phase 071.

#### Task 49B — Authority ceilings

1. Classify equations as unchanged source model, algebraic restatement, newly introduced background relation, newly introduced governing relation, or competitive-only candidate.
2. Require derivation provenance and assumptions for every equation promotion claim. Bare equation insertion, review approval, or citation adjacency is insufficient.
3. Check code-free main-body compliance: implementation details may occur only in the designated implementation appendix/companion. Historical code references in process artifacts are not main-body evidence.
4. Preserve all unresolved graphite/LCO/Si/thermal/kinetic material authority debts and create new carry items only for genuinely new source identities.

#### Task 49C — Validation and checkpoint

1. Require one authority row for every new/modified cite/equation/background claim and no orphan citation key or unsupported promotion.
2. Negative probes cover fake DOI certainty, citation-key alias collapse, bibliography-presence-as-support, equation-hash-as-validity, review-consensus promotion, and code leakage misclassification.
3. Save result first; exact-seven commit subject `audit(phase061): bound v1020 citation authority`; push and remote-verify before Step 50.

Gate: `PASS_P061_STEP49_CITATION_AUTHORITY` or bounded `PASS_WITH_CONCERNS` when unresolved external truth is fully routed.

### Step 50 — Figure Competition, Multi-review and Artifact Audit

#### Task 50A — Figure and review genealogy

1. Full-read figure competition specifications, candidates, scoring sheets, multi-review records, consolidated judgments, and adopted-source references.
2. Visually inspect all 23 PNG occurrences at original resolution and all 130 PDF pages; record dimensions, pixel/page identity, labels, axes, legends, caption/source relationship, and visible defects.
3. Build edges among source model/data claim, renderer or generation record, candidate figure, reviewer vote, adopted figure, TeX include, and generated PDF page.

#### Task 50B — Scientific scope adjudication

1. Separate aesthetic/readability selection from numerical reproduction, internal consistency, material validation, and experimental evidence.
2. Generated visuals and multi-review consensus are internal artifacts. They do not become experiment or primary scientific authority.
3. Q2/Q3, `comp_P*`, `comp_Q*`, review candidates, and later-version proposals require explicit adoption edges; otherwise classify as competing/not-adopted and route forward without contaminating v1.0.20 truth.
4. Record every missing renderer/source-data/provenance edge as `GROUND_NOT_FOUND` or `UNVERIFIED`, not inferred completion.

#### Task 50C — Validation and checkpoint

1. Require 23/23 occurrence attestations, 14/14 PDF and 130/130 page attestations, review-source coverage, exact adoption edges, and no evidence-class promotion.
2. Negative probes cover skipped duplicate occurrence, missing page, false adoption, review-count inflation, generated-as-experiment, and visual-pass-as-numeric-validity.
3. Save result first; exact-eight commit subject `audit(phase061): adjudicate v1020 review artifacts`; push and remote-verify before Step 51.1.

Gate: `PASS_P061_STEP50_REVIEW_ARTIFACTS` or bounded `PASS_WITH_CONCERNS` when evidence debt is fully routed.

### Step 51.1 — Source Disposition and Carry-forward Delta

1. Create exactly one disposition row for every frozen v1.0.20 source occurrence: `PRESERVE`, `CORRECT`, `DISCARD`, `SUPERSEDE`, `COMPETING_ONLY`, or `UNVERIFIED` with evidence, authority ceiling, reason, source identity, target Phase, acceptance criterion, and status.
2. Competitive draft and adopted source must never share a disposition identity merely because text/blob content overlaps.
3. Reconcile inherited carry 52 and Phase 060 new blocker 5 without deleting, duplicating, or claiming resolution. Record touched/unchanged/refined/resolved only from direct evidence.
4. New blockers must have stable IDs, origin path/line or artifact anchor, exact acceptance criterion, validity domain, owning target Phase, and OPEN status.
5. Validator rejects missing/duplicate source occurrence, illegal disposition, missing target, acceptance-free blocker, inherited status mutation, and false authority promotion.
6. Save result first; exact-eight commit subject `audit(phase061): disposition v1020 lineage`; push and remote-verify before Step 51.2.

Gate: `PASS_P061_STEP51_1_DISPOSITIONS` or bounded `PASS_WITH_CONCERNS` only when all rows route losslessly.

### Step 51.2 — Integrated Validation, Lineage Report D and Final Gate

1. Start with a failing final validator before `PHASE_061_VALIDATION.json` exists.
2. Fresh-run every subordinate validator from Steps 46–51.1; strict-parse/full-traverse every machine artifact and verify content-addressed source/report hashes.
3. Reconstruct 232/232 occurrence coverage, 231/231 blobs, 195/195 text and 31,553/31,553 physical lines, 29,335/29,335 nonblank lines, 14/14 PDFs and 130/130 pages, 23/23 image occurrences, all authority/delta/disposition rows, all carry identities, and all Git checkpoint ancestry.
4. Run named semantic negative controls and at least two normalized deterministic reconstructions. Environment-dependent fields must be separated from deterministic projections.
5. Write `PHASE_061_V1020_LINEAGE_REPORT_D.md`, Step 51.2 gate result, and standalone `PHASE_061_RESULT.md` with confirmed, unverified, ground-not-found, carry queue, protected non-changes, and exact Phase 062 entry condition.
6. Select exactly one gate. Missing mandatory coverage, invalid genealogy/routing, unbounded evidence promotion, validator failure, protected drift, or incomplete remote checkpoint requires `CONDITIONAL_P061` or `FAIL_P061`, never an optimistic PASS.
7. Exact-eight commit subject `audit(phase061): close v1020 lineage gate`; push and persistence-verify before creating the Phase 062 detailed plan.

## Phase Gate

### `PASS_P061_LINEAGE_D`

Allowed only when all 232 path occurrences are full-read/inspected and each has exactly one source disposition; adopted release, process self-assessment, internal review, generated artifact, and competing draft are separately classified; v1.0.19↔v1.0.20 deltas and snapshot genealogy are reproducible; citation/equation/review authority ceilings are lossless; carry-forward identities and acceptance criteria are complete; all validators, negative controls, deterministic checks, atomic commits, pushes, and remote persistence checks pass.

This PASS does not mean external scientific/material/experimental validity, primary-literature truth, defect repair, canonical selection, identifiability, final LaTeX/PDF, or publication readiness.

### `CONDITIONAL_P061`

Use when mandatory coverage is substantially complete but a bounded source/read/genealogy/authority/routing requirement remains unresolved and is explicitly named. Ordinary downstream scientific uncertainty with complete routing is not by itself a reason for CONDITIONAL.

### `FAIL_P061`

Use when source identity/read coverage is incomplete, process/draft/adopted authority is conflated, delta or snapshot genealogy is invalid, visual/page coverage is missing, dispositions/carry identities are lossy, validators cannot reproduce evidence, protected state drifts, or no safe remote recovery point exists.

Phase 062 Step 52 may not begin before a new Phase 062 detailed plan is saved, validated, reviewed, atomically committed, pushed, and remote-verified.

## Implementation Interfaces

### Source/read topology row

```json
{
  "source_id": "P061-SRC-0001",
  "path": "Claude/docs/v1.0.20/...",
  "blob_sha1": "...",
  "sha256": "...",
  "role": "theory|plan|result|figure|generated_document|code|test|implementation_guide",
  "review_mode": "FULL_TEXT|FULL_PDF|FULL_IMAGE",
  "extent": {"lines": 0, "nonblank_lines": 0, "pages": 0, "bytes": 0},
  "read_state": "READ_FULL|VISUAL_FULL",
  "authority_class": "...",
  "duplicate_group": null
}
```

### Process/adoption authority row

```json
{
  "claim_id": "P061-PROC-0001",
  "claimant": {"path": "...", "line_start": 1, "line_end": 1},
  "claim_type": "plan|self_review|multi_review|adoption|completion|scientific",
  "object_id": "...",
  "evidence_paths": ["..."],
  "adoption_edge": null,
  "authority_ceiling": "INTERNAL_PROCESS_ONLY",
  "status": "CONFIRMED|CONTRADICTED|GROUND_NOT_FOUND|UNVERIFIED",
  "target_phase": 61
}
```

### Lineage delta row

```json
{
  "v1020_source_id": "P061-SRC-0001",
  "comparison_class": "ADDED|MODIFIED|UNCHANGED|RENAMED|COPIED|DELETED_COUNTERPART",
  "v1019_path": null,
  "v1019_blob": null,
  "v1020_path": "...",
  "v1020_blob": "...",
  "semantic_delta": "...",
  "equation_delta_ids": [],
  "citation_delta_ids": [],
  "authority_limit": "LINEAGE_ONLY"
}
```

### Citation/equation authority row

```json
{
  "asset_id": "P061-AUTH-0001",
  "asset_type": "CITATION|BIB_ENTRY|EQUATION|BACKGROUND_CLAIM",
  "source_anchor": {"path": "...", "line_start": 1, "line_end": 1},
  "delta_class": "NEW|MODIFIED|UNCHANGED|COMPETITIVE_ONLY",
  "metadata_state": "CONSISTENT|CONFLICT|UNVERIFIED",
  "primary_support_state": "UNVERIFIED_EXTERNAL",
  "derivation_state": "SOURCE_DERIVED|RESTATEMENT|BARE_INSERTION|GROUND_NOT_FOUND",
  "target_phase": 71
}
```

### Disposition row

```json
{
  "source_id": "P061-SRC-0001",
  "disposition": "PRESERVE|CORRECT|DISCARD|SUPERSEDE|COMPETING_ONLY|UNVERIFIED",
  "evidence_ids": ["..."],
  "reason": "...",
  "authority_ceiling": "...",
  "target_phase": 62,
  "acceptance_criterion": "...",
  "status": "OPEN|PRESERVED_ACTIVE|RESOLVED"
}
```

## Test and Validation Plan

### Plan and numbering

- Required section order, exact Phase 061 heading, and cumulative Steps 46, 47, 48, 49, 50, 51.1, 51.2.
- No Step 1 restart and no Step 52 execution before Phase 062 activation.
- All declared output paths, commit subjects, gates, stop conditions, and code-free scholarly-body boundary are present.

### Source and read coverage

- Strict manifest SHA/baseline verification and full recursive traversal.
- Exact 232/231 source identities, 195 text, 31,553 physical/29,335 nonblank lines, 14 PDF/130 pages, 23 image occurrences, roles/extensions, 18 overlap/214 new, and the single two-path duplicate group.
- First-line-through-EOF text attestation, page-by-page PDF attestation, occurrence-by-occurrence image attestation, Git blob/SHA-256/content extent checks.

### Authority, lineage and scientific boundaries

- Process claim/adoption completeness; no circular self-certification.
- Exact old/new blob and semantic delta reproduction; snapshot genealogy and P5/P6 duplicate proof.
- Citation metadata vs primary support separation; equation derivation/authority ceiling; competing draft vs adopted source separation.
- Review/figure aesthetic scope vs numerical/scientific/experimental authority separation.
- Code-free main-body policy is checked without modifying scholarly source.

### Disposition and carry-forward

- Exactly 232 source dispositions; zero orphan/duplicate identity.
- Inherited 52 and Phase 060 new 5 preserved unless direct evidence permits a recorded delta.
- Every new blocker has source anchor, acceptance criterion, authority domain, target, status, and collision-free ID.

### Negative validation

- Duplicate JSON keys, non-finite numbers, missing path/page/line/image, blob mismatch, wrong duplicate group, wrong old/new pairing.
- Process claim promoted to scientific truth, review consensus promoted to primary authority, snapshot promoted to scientific correctness, generated visual promoted to experiment.
- Competitive draft marked adopted without edge, bibliography presence treated as support, fake DOI certainty, equation hash treated as physical validity.
- Missing disposition, duplicate routing, changed inherited status, acceptance-free blocker, invalid gate combination, extra dirty path, protected drift.
- Every negative mutation must fail with its intended unique diagnostic; an unrelated failure does not count.

### Determinism and Git persistence

- At least two byte-identical normalized artifact reconstructions per execution unit.
- Environment-dependent raw paths/executables/stdout may be recorded separately but cannot contaminate deterministic projections.
- `git diff --check`, strict JSON parse, exact staged path set, exact subject/parent, clean postcommit status, local/upstream/live-origin equality, protected/main fixed tips, Claude diff 0.

## Stop Conditions

Stop the current execution unit and do not commit if any of the following occurs:

- frozen manifest hash/baseline/source blob mismatch;
- required text/PDF/image cannot be fully read or visually inspected;
- ambiguous source identity, adoption edge, or old/new pairing would require guessing;
- process/review/competition evidence cannot be separated from adopted source;
- DOI or primary reference truth would need invention or unverified web metadata;
- validator/negative/determinism failure remains unresolved;
- unexpected dirty path, `Claude/**` change, protected/main drift, credential/config mutation, or remote divergence;
- exact Step result has not been written before commit;
- push or remote persistence cannot be verified.

A stop condition is recorded as `BLOCKED`, `CONDITIONAL`, `FAIL`, `GROUND_NOT_FOUND`, or `UNVERIFIED` according to evidence. It is never silently repaired by assumption.

## Assumptions

- Frozen manifest and baseline Git objects remain readable and immutable.
- The active remote branch remains writable; Phase 060 persistence already demonstrated branch push authority.
- Sparse checkout may be extended after plan activation without tracked changes; Git-object reads remain the source identity authority.
- PDF/image inspection tools can operate on disposable rendered copies outside the staged exact set.
- Phase 057 observations are navigation aids, not substitute reads or conclusions.
- External literature truth remains a later gate even when Phase 061 detects internal metadata contradictions.
- Uncertainty and unresolved defects are acceptable only when explicitly preserved and routed; they are not equivalent to missing audit coverage.

## Correction History

- 2026-08-26: Created the Phase 061 detailed plan after remote persistence of Phase 060 Step 45.2.
- This plan preserves the previous master Steps 46–51 while splitting Step 51 into 51.1 disposition and 51.2 integrated closure, without restarting cumulative numbering.
- It replaces the provisional shortcut “review v1.0.20 improvements” with exact 232-path source/read, authority, delta, citation, visual, disposition, negative-validation, atomic commit/push, and remote-persistence contracts.
