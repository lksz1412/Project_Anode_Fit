# Phase 060 v1.0.19 Lineage Reaudit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` task by task. Phase 060 uses cumulative Steps 40–45; numbering must not restart. Every completed Step or declared substep requires its result, machine evidence, ledger/handover update, atomic commit, push and remote-tip verification before the next unit begins.

**Goal:** v1.0.19의 문서 주도(doc-leads) 재작성 계보를 source topology, 작업·검수 기록, 코드·시험·저장 artifact, 독립 수식 재유도의 다섯 축에서 전건 재감사하고, 채택 가능 자산과 잔존 결함을 근거·권위 경계와 함께 닫는다.

**Architecture:** frozen v1.0.19 release corpus 66개와 V1019 생성 과정 corpus 11개를 서로 다른 권위층으로 보존한다. Ch1/Ch2 include graph와 과학 claim을 먼저 복원하고, process/Fable 자기평가를 독립 증거로 승격하지 않은 채 실제 production call flow와 시험·artifact를 연결한다. 마지막으로 production implementation을 과학 권위로 사용하지 않는 독립 재유도와 수치 probe로 단위·부호·식별성·극한을 검증한다.

**Tech Stack:** Git/GitHub, Markdown/JSON evidence ledgers, Python standard library와 NumPy/SciPy 기반 독립 probe, disposable runtime fixture, Poppler 기반 PDF 95-page render audit, Git-blob SHA-1/SHA-256와 POSIX path canonicalization.

---

정본일: 2026-08-25

상위 master plan:
`Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`

직전 Phase plan:
`Codex/plans/2026-08-25-phase059-resume-closure-detailed-plan.md`

직전 Phase result:
`Codex/results/PHASE_059_RESULT.md`

직전 final Step result:
`Codex/results/PHASE_059_STEP_039_6_GATE_RESULT.md`

활성 branch:
`codex/anode-fit-v1025_2-canonical-completion`

계획 작성 전 clean HEAD:
`e01049489bf601c433d97d4b4121cf0fdcfca085`

Phase 범위: Phase 060, cumulative Steps 40–45

정확한 다음 실행 단위: 이 계획의 activation commit·push·remote 검증 후 Step 40

## Summary

Phase 059는 `PASS_P059_LINEAGE_B`로 frozen v1.0.14–v1.0.18.2 감사 범위와 routing을 닫았다. 그 PASS는 canonical model, defect repair, 문헌 truth, 외부 재료 타당성, parameter 식별성 또는 최종 PDF 권위를 부여하지 않는다. Phase 060도 같은 권위 경계를 유지한다.

v1.0.19는 단일 파일 증분판이 아니다. Ch1/Ch2 root에서 39개 section을 include하는 42개 TeX source, 4개 runtime Python file, 3개 운영·인계 text, 3개 PDF, 13개 image, 1개 NPZ로 구성된 66-path release corpus다. 이 release corpus 밖에는 rewrite plan과 Fable/asset/union/continuity/execution records 11개가 있다. 두 corpus는 모두 전문 검독하지만 다음처럼 권위를 분리한다.

1. release corpus는 실제 문서·구현·시험·artifact 상태의 근거다.
2. process corpus는 의도, 검수 절차와 자기보고의 근거이며 과학적 참·외부 타당성의 단독 근거가 아니다.
3. v1.0.20 아래의 v1019 명명 파일 2개는 cross-version witness다. Phase 061 소유권을 보존하며 Phase 060 primary count에 넣지 않는다.

Step 40–45는 source topology, process authority, code/runtime/artifact, doc-to-code conformance, independent physics rederivation, disposition/final gate 순서다. Step 45는 45.1 disposition과 45.2 integrated closure로 나눠 각각 원격 복구점을 만든다.

## Current Ground Truth

### Git and protection state

- active local HEAD, upstream과 origin active tip은 계획 작성 직전 모두 `e01049489bf601c433d97d4b4121cf0fdcfca085`였다.
- protected Codex tip은 `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`이다.
- `main` tip은 `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`이다.
- Phase 056 frozen source baseline은 `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`이다.
- frozen baseline과 protected tip 사이 `Claude/**` diff는 0이다.
- Phase 060은 `Claude/**`, protected branch 또는 `main`을 수정하지 않는다.
- 현재 sparse checkout에는 v1.0.19가 없다. plan activation 원격 복구점 뒤 active isolated worktree에만 `Claude/docs/v1.0.19`, 필요한 V1019 plan/process path를 추가한다.

### Predecessor gate

- Phase 059 final gate는 `PASS_P059_LINEAGE_B`다.
- 52개 carry-forward row 중 41개가 `OPEN`이며, target Phase가 060인 row는 0개다.
- target Phase 060 row 0은 Phase 060 생략 근거가 아니다. Phase 060은 상위 master가 고정한 v1.0.19 lineage reaudit다.
- Phase 059의 external material truth validated count는 0이다.

### Frozen v1.0.19 release corpus

`Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json`에서 `version == "v1.0.19"`인 exact set은 다음과 같다.

| Measure | Frozen value |
|---|---:|
| path occurrences | 66 |
| unique Git blobs | 66 |
| `FULL_TEXT` | 49 files / 7,756 lines |
| `FULL_PDF` | 3 files / 95 pages |
| `FULL_IMAGE` | 13 files |
| `BINARY_INTROSPECTION` | 1 file / 13 arrays |
| Ch1 sections | 24 files / 3,668 lines |
| Ch2 sections | 15 files / 1,391 lines |
| root TeX | 3 files / 577 lines |
| operational text | 3 files / 324 lines |
| runtime Python | 4 files / 1,796 lines |

모든 66개 release path는 서로 다른 Git blob이다. 전체 42개 TeX source는 5,636 lines다.

### V1019 process corpus

baseline tree에서 확인한 supplementary process corpus는 11 paths, 11 unique blobs, 1,028 physical lines/889 nonblank lines, 148,934 bytes다. Release corpus와 합치면 Phase 060 primary audit queue는 77 paths, 77 unique blobs, 60 text files/8,784 physical lines/8,025 nonblank lines, 3 PDFs/95 pages, 13 images와 1 binary artifact다. 빈 행을 보존하는 Git-blob `splitlines()` physical count를 canonical coverage denominator로 사용하고, 889-line historical shell metric은 nonblank count로 함께 보존한다.

### Cross-version witnesses

- `Claude/docs/v1.0.20/figs/graph_suite_v1019.png`는 v1.0.19의 같은 이름 figure와 동일 blob `d85e533d77317d7b72831c73e5b472faec3e0302`다.
- `Claude/docs/v1.0.20/results/snapshot_v1019_baseline.json`은 v1.0.20 소유의 1,120-line result witness다.
- 두 occurrence를 포함한 inspection workload는 79 path occurrences, 78 unique blobs, 61 text files/9,904 physical lines/9,145 nonblank lines, PDF 3/95 pages, image 14 occurrences/13 unique blobs와 binary 1개다.
- 이 witness는 v1.0.19 runtime claim을 교차대조하지만 Phase 061의 232-path disposition을 선행하거나 대신하지 않는다.

Baseline content search가 추가로 찾은 다음 3개는 후속 Phase 계획·색인의 V1019 언급이다. Phase 060 primary/witness queue에 넣지 않고 소유 Phase의 later planning metadata로 보존한다.

- `Claude/plans/2026-07-17-v1022-master-plan.md`: V1019 계보 언급은 Phase 062 계획 소유다.
- `Claude/plans/2026-07-22-v1024-feedback-revision-plan.md`: v1.0.19 code-origin 언급은 Phase 065 계획 소유다.
- `Claude/plans/INDEX.md`: 완료 계획 pointer이며 과학 또는 runtime evidence가 아니다.

### Known provisional findings, not Phase 060 conclusions

`Codex/results/PHASE_057D_V1019_INTENT_OBSERVATIONS.md`는 다음을 provisional로 기록했다. Phase 060은 이를 다시 원천 대조하며 자동 승계하지 않는다.

- 문맥을 보존한 전면 재작성과 doc-leads 원칙은 사용자 의도 후보다.
- 336/336 Ch1, 133/133 Ch2 asset preservation claim은 누락 방지 자기보고이지 각 자산의 물리 타당성 증거가 아니다.
- bit-exact regression, synthetic roundtrip와 continuity는 internal consistency이며 external material validation이 아니다.
- LCO interaction/activation anchors, 다온도 전자항과 비가역열은 미폐쇄 후보다.
- composition-to-OCV implicit solver는 구조 자산 후보지만 유일성, plateau, nonmonotone mapping와 실측 uncertainty는 미검증이다.

## Phase Range

| Phase | Steps | Name | Status before execution | Terminal artifact |
|---|---:|---|---|---|
| 060 | 40–45 | v1.0.19 lineage reaudit | detailed-plan activation pending | `Codex/results/PHASE_060_V1019_LINEAGE_REPORT_C.md` |

| Execution unit | Scope | Required remote checkpoint |
|---|---|---|
| plan activation | detailed plan, plan validator/result, ledgers, handover | before Step 40 |
| Step 40 | source freeze, Ch1/Ch2 include topology and full TeX read | before Step 41 |
| Step 41 | rewrite/Fable/process/intent authority | before Step 42 |
| Step 42 | code/test/runtime/PDF/image/NPZ artifact audit | before Step 43 |
| Step 43 | doc-leads theory-to-call-flow conformance | before Step 44 |
| Step 44 | independent charge/thermal/current/material rederivation | before Step 45.1 |
| Step 45.1 | claim/defect/carry-forward disposition | before Step 45.2 |
| Step 45.2 | integrated validation, Lineage Report C and Phase gate | before Phase 061 plan |

## Exact Read Inputs

### Control inputs — full read at every recovery boundary

- `Codex/AGENTS.md`
- `Codex/plans/phase_planning_operations_guide.md`
- `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`
- this detailed plan
- immediate previous Step result and its machine evidence
- `Codex/results/PHASE_059_RESULT.md`
- `Codex/results/PHASE_059_STEP_039_6_GATE_RESULT.md`
- `Codex/results/PHASE_059_V1014_V1018_2_LINEAGE_REPORT_B.md`
- `Codex/results/PHASE_059_VALIDATION.json`
- `Codex/results/PHASE_059_CARRY_FORWARD_REGISTER.json`
- `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
- `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Large JSON inputs require strict duplicate-key parse and full recursive traversal of the fields consumed by the current Step. Aggregate counts alone do not constitute a full read.

### Primary release corpus — exact 66-path set

Operational and runtime roots:

- `Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py`
- `Claude/docs/v1.0.19/FITTING_GUIDE.md`
- `Claude/docs/v1.0.19/HANDOVER_v1.0.19.md`
- `Claude/docs/v1.0.19/fit_roundtrip_demo.py`
- `Claude/docs/v1.0.19/graph_suite_v1019.py`
- `Claude/docs/v1.0.19/test_regression_v1019.py`

Ch1 root and exact section set:

- `Claude/docs/v1.0.19/graphite_ica_ch1_v1.0.19.tex`
- `Claude/docs/v1.0.19/_sections/ch1_preamble.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec00_intro.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec01_n0n1.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec02a_part0.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec02b_part0.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec03_center.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec04_hys.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec05_width.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec06_eqpeak.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec07_broadening.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec08_lag.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec09_tail.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec10_sum.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec11_lcointro.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec12_lcocenter.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec13_lcohys.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec14_lcodecomp.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec15_lcoelec.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec16_lcopeak.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec17_msmr.tex`
- `Claude/docs/v1.0.19/_sections/ch1_sec18_inputs.tex`
- `Claude/docs/v1.0.19/_sections/ch1_appA_signcheck.tex`
- `Claude/docs/v1.0.19/_sections/ch1_appB_codemap.tex`
- `Claude/docs/v1.0.19/_sections/ch1_bib.tex`

Ch2 root and exact section set:

- `Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.tex`
- `Claude/docs/v1.0.19/_sections/ch2_preamble.tex`
- `Claude/docs/v1.0.19/_sections/ch2_sec00_intro.tex`
- `Claude/docs/v1.0.19/_sections/ch2_sec01_partition.tex`
- `Claude/docs/v1.0.19/_sections/ch2_sec02_config.tex`
- `Claude/docs/v1.0.19/_sections/ch2_sec03_vibel.tex`
- `Claude/docs/v1.0.19/_sections/ch2_sec04_einstein.tex`
- `Claude/docs/v1.0.19/_sections/ch2_sec05_mixing.tex`
- `Claude/docs/v1.0.19/_sections/ch2_sec06_limits.tex`
- `Claude/docs/v1.0.19/_sections/ch2_sec07_revheat.tex`
- `Claude/docs/v1.0.19/_sections/ch2_sec08_synthesis.tex`
- `Claude/docs/v1.0.19/_sections/ch2_sec09_method.tex`
- `Claude/docs/v1.0.19/_sections/ch2_sec10_closing.tex`
- `Claude/docs/v1.0.19/_sections/ch2_appA_traps.tex`
- `Claude/docs/v1.0.19/_sections/ch2_appB_codemap.tex`
- `Claude/docs/v1.0.19/_sections/ch2_bib.tex`

Standalone theory, PDF, images and data:

- `Claude/docs/v1.0.19/appendix_phase_separation.tex`
- `Claude/docs/v1.0.19/appendix_phase_separation.pdf`
- `Claude/docs/v1.0.19/graphite_ica_ch1_v1.0.19.pdf`
- `Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.pdf`
- `Claude/docs/v1.0.19/golden_graphite_ref.npz`
- `Claude/docs/v1.0.19/figs/P4_lco_heat_validation.png`
- `Claude/docs/v1.0.19/figs/anode_fit_v1_0_14_dqdv.png`
- `Claude/docs/v1.0.19/figs/graph_suite_v1015.png`
- `Claude/docs/v1.0.19/figs/graph_suite_v1016.png`
- `Claude/docs/v1.0.19/figs/graph_suite_v1019.png`
- `Claude/docs/v1.0.19/samples/continuity_scan_report.txt`
- `Claude/docs/v1.0.19/samples/fig_Uoc_x.png`
- `Claude/docs/v1.0.19/samples/fig_dUdT_x.png`
- `Claude/docs/v1.0.19/samples/fig_dqdv_graphite.png`
- `Claude/docs/v1.0.19/samples/fig_dqdv_lco.png`
- `Claude/docs/v1.0.19/samples/fig_dqdv_temperature.png`
- `Claude/docs/v1.0.19/samples/fig_fit_roundtrip.png`
- `Claude/docs/v1.0.19/samples/fig_qrev_x.png`
- `Claude/docs/v1.0.19/samples/fig_vib_einstein.png`

### Supplementary V1019 process corpus — exact 11-path set

- `Claude/plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md`
- `Claude/results/process/V1019_ASSET_CHECKLIST.md`
- `Claude/results/process/V1019_CH2_ASSET_CHECKLIST.md`
- `Claude/results/process/V1019_CH2_FABLE_BRIEF.md`
- `Claude/results/process/V1019_CH2_UNION_DEFECTS.md`
- `Claude/results/process/V1019_CODE_FABLE_BRIEF.md`
- `Claude/results/process/V1019_CONTINUITY_JUDGMENT.md`
- `Claude/results/process/V1019_EXECUTION_LEDGER.md`
- `Claude/results/process/V1019_FABLE_BRIEF.md`
- `Claude/results/process/V1019_FINAL_REVIEW_UNION.md`
- `Claude/results/process/V1019_UNION_DEFECTS.md`

### Cross-version witnesses — exact 2-path set

- `Claude/docs/v1.0.20/figs/graph_suite_v1019.png`
- `Claude/docs/v1.0.20/results/snapshot_v1019_baseline.json`

### Deferred later-plan mentions — metadata exclusion set

- `Claude/plans/2026-07-17-v1022-master-plan.md`
- `Claude/plans/2026-07-22-v1024-feedback-revision-plan.md`
- `Claude/plans/INDEX.md`

## Non-goals and Scope Guards

- `Claude/**` source, process record, PDF, image, NPZ 또는 v1.0.20 witness를 수정하지 않는다.
- Phase 060에서 발견한 production defect를 구현으로 수리하지 않는다.
- v1.0.20의 나머지 230 paths를 감사하거나 Phase 061 disposition을 선행하지 않는다.
- Fable/union/final-review의 “완료”, “0 defects” 또는 asset count를 과학 truth로 자동 승격하지 않는다.
- 코드 실행·golden·roundtrip·synthetic curve·PDF 존재를 external material validation으로 승격하지 않는다.
- 문서에 인용된 reference를 Phase 071 전 full literature truth로 선언하지 않는다. Phase 060은 source 내 citation/claim linkage와 명백한 충돌만 기록한다.
- v1.0.19을 final canonical model로 선택하지 않는다.
- final scholarly LaTeX/PDF를 작성하거나 현재 scholarly body를 수정하지 않는다.
- old Phase 059 artifact, result, ledger history를 덮어쓰지 않는다.
- runtime을 `Claude/docs/v1.0.19`에서 직접 실행해 source directory에 artifact/cache를 생성하지 않는다.
- code-map section을 코드 금지 학술 본문의 허용 선례로 사용하지 않는다. 최종 code-free boundary는 Phase 087–089에서 별도로 강제한다.

## Implementation Changes

### Plan activation

- Create `Codex/plans/2026-08-25-phase060-v1019-lineage-detailed-plan.md`.
- Create `Codex/work/v1019_phase060/validate_phase060_plan.py`.
- Create `Codex/results/PHASE_060_PLAN_ACTIVATION_VALIDATION.json`.
- Create `Codex/results/PHASE_060_PLAN_ACTIVATION_RESULT.md`.
- Update `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`.
- Update Phase 060 row only in `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`.
- Update `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`.

### Step 40

- Create `Codex/work/v1019_phase060/build_phase060_step40_source_topology.py`.
- Create `Codex/work/v1019_phase060/validate_phase060_step40_source_topology.py`.
- Create `Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json`.
- Create `Codex/results/PHASE_060_STEP_040_SOURCE_TOPOLOGY_RESULT.md`.

### Step 41

- Create `Codex/work/v1019_phase060/build_phase060_step41_process_authority.py`.
- Create `Codex/work/v1019_phase060/validate_phase060_step41_process_authority.py`.
- Create `Codex/results/PHASE_060_V1019_PROCESS_INTENT_MATRIX.json`.
- Create `Codex/results/PHASE_060_STEP_041_PROCESS_AUTHORITY_RESULT.md`.

### Step 42

- Create `Codex/work/v1019_phase060/audit_phase060_step42_runtime_artifacts.py`.
- Create `Codex/work/v1019_phase060/validate_phase060_step42_runtime_artifacts.py`.
- Create `Codex/results/PHASE_060_V1019_CODE_TEST_RUNTIME_MATRIX.json`.
- Create `Codex/results/PHASE_060_V1019_ARTIFACT_AUDIT.json`.
- Create `Codex/results/PHASE_060_STEP_042_RUNTIME_ARTIFACT_RESULT.md`.

### Step 43

- Create `Codex/work/v1019_phase060/build_phase060_step43_doc_code_trace.py`.
- Create `Codex/work/v1019_phase060/validate_phase060_step43_doc_code_trace.py`.
- Create `Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json`.
- Create `Codex/results/PHASE_060_STEP_043_DOC_CODE_CONFORMANCE_RESULT.md`.

### Step 44

- Create `Codex/work/v1019_phase060/build_phase060_step44_physics_validation.py`.
- Create `Codex/work/v1019_phase060/validate_phase060_step44_physics_validation.py`.
- Create `Codex/results/PHASE_060_V1019_PHYSICS_REDERIVATION.md`.
- Create `Codex/results/PHASE_060_V1019_PHYSICS_VALIDATION.json`.
- Create `Codex/results/PHASE_060_STEP_044_PHYSICS_REDERIVATION_RESULT.md`.

### Step 45.1

- Create `Codex/work/v1019_phase060/build_phase060_step45_dispositions.py`.
- Create `Codex/work/v1019_phase060/validate_phase060_step45_dispositions.py`.
- Create `Codex/results/PHASE_060_V1019_DISPOSITION_MATRIX.json`.
- Create `Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json`.
- Create `Codex/results/PHASE_060_STEP_045_1_DISPOSITION_RESULT.md`.

### Step 45.2

- Create `Codex/work/v1019_phase060/validate_phase060_final.py`.
- Create `Codex/results/PHASE_060_VALIDATION.json`.
- Create `Codex/results/PHASE_060_V1019_LINEAGE_REPORT_C.md`.
- Create `Codex/results/PHASE_060_STEP_045_2_GATE_RESULT.md`.
- Create `Codex/results/PHASE_060_RESULT.md`.
- Update both execution ledgers and the active handover.

## Plan Activation Unit — Save Before Step 40

1. Save this detailed plan before reading v1.0.19 source as Phase 060 execution.
2. Validate required sections, cumulative Steps 40–45, exact 66/11/2 corpus boundary, all planned output paths, gate authority and commit/push policy.
3. Record planning inputs, metadata-only inventory scope and unreviewed scientific source state in `PHASE_060_PLAN_ACTIVATION_RESULT.md`.
4. Set both ledger Phase 060 rows to `IN_PROGRESS`, Detailed Plan to this path and Exact Next to Step 40.
5. Put this plan in the active handover canonical chain and set the current result to the plan activation result.
6. Run plan validator twice and require byte-identical JSON.
7. Stage only the seven declared plan-activation paths, commit, push and compare local HEAD/upstream/remote tip.

Run:

```powershell
python Codex\work\v1019_phase060\validate_phase060_plan.py
python -m json.tool Codex\results\PHASE_060_PLAN_ACTIVATION_VALIDATION.json > $null
git diff --check
git diff --exit-code origin/codex/lib-physics-endgame-v1025_2 -- Claude
```

Commit subject:

```text
docs(phase060): plan v1019 lineage reaudit
```

## Phase 060 — v1.0.19 Reaudit

### Step 40 — Source Freeze, Ch1/Ch2 Full Read and Include Topology

#### Task 40A — Recovery and frozen queue

- [ ] Re-read the master, this plan, Phase 059 result/gate, both ledgers and active handover to EOF.
- [ ] Confirm local HEAD = upstream = origin active, protected/main fixed and clean status.
- [ ] Extend sparse checkout in the active isolated worktree only; no tracked file change is allowed.
- [ ] Reconstruct all 66 release entries from the Phase 056 manifest and all 11 supplementary paths from baseline Git tree.
- [ ] Register the 2 cross-version witnesses separately and prove the duplicate graph-suite image blob identity.
- [ ] Record Git blob SHA-1, canonical SHA-256, size, extent, role, review mode and ownership for every occurrence.
- [ ] Reject any missing path, unexpected blob, duplicate primary identity, line/page mismatch or protected/Claude drift.

#### Task 40B — Failing validator first

- [ ] Write the validator before the topology artifact.
- [ ] Require primary `77/77` paths/blobs, release `66/66`, process `11/11`, witness `2` occurrences/`1` new blob.
- [ ] Require primary text `60/8,784 physical/8,025 nonblank` and separate witness text `1/1,120 physical/1,120 nonblank`.
- [ ] Require 42/42 TeX, Ch1 24, Ch2 15 and root 3 with exact 5,636 lines.
- [ ] Require PDF `3/95 pages`, image `13 unique/14 occurrences`, binary `1`.
- [ ] Require every root `\input`/`\include` edge to resolve to a frozen source path and every included section to have an expansion ordinal.
- [ ] Run before output exists and record controlled non-zero missing-artifact failure.

#### Task 40C — Full source read and topology build

- [ ] Read all 42 TeX files from line 1 through EOF in actual Ch1/Ch2/standalone expansion order.
- [ ] Record displayed equations, definitions, assumptions, sign/unit declarations, citation keys, labels, refs, external document links, code mentions and forward references with exact line anchors.
- [ ] Build Ch1 and Ch2 include DAGs and the actual linear expansion sequence.
- [ ] Detect missing/duplicate include, unreachable section, circular include/external-reference dependency, duplicate label and unresolved cite/ref candidate without claiming LaTeX build success.
- [ ] Distinguish scientific body, bibliography, sign-check appendix, code-map appendix and standalone phase-separation authority.
- [ ] Compare the topology with the Phase 059 predecessor evidence without treating copied text as newly validated.

#### Task 40D — Verify, result, commit and push

- [ ] Run builder twice and require byte-identical normalized JSON.
- [ ] Run validator normal mode and negative mutations for missing path, altered blob, skipped line, broken edge and duplicated identity.
- [ ] Write Step 40 result with actual read coverage, findings, unverified items, commands, non-changes and exact next Step 41.
- [ ] Update ledgers/handover, including the plan activation containing commit and remote verification.
- [ ] Commit Step 40 script, validator, JSON, result, ledgers and handover atomically; push and remote-verify.

Run:

```powershell
python Codex\work\v1019_phase060\build_phase060_step40_source_topology.py
python Codex\work\v1019_phase060\validate_phase060_step40_source_topology.py
python -m json.tool Codex\results\PHASE_060_V1019_SOURCE_TOPOLOGY.json > $null
git diff --check
git diff --exit-code origin/codex/lib-physics-endgame-v1025_2 -- Claude
```

Commit subject:

```text
audit(phase060): freeze v1019 source topology
```

### Step 41 — Rewrite, Fable and Process Authority Audit

#### Task 41A — Exact process full read

- [ ] Read all 11 supplementary process files line 1 through EOF, total 1,028 physical lines; reconcile the historical 889-line shell metric as nonblank lines rather than a competing EOF denominator.
- [ ] Re-read `FITTING_GUIDE.md`, `HANDOVER_v1.0.19.md`, `samples/continuity_scan_report.txt` and both code-map sections to EOF in this Step's authority context.
- [ ] Parse rewrite plan → Fable brief → union defects → asset checklists → execution ledger → final review/handover chronology.
- [ ] Record every claimed asset count, defect, correction, reviewer role, completion statement and unresolved item with exact anchors.

#### Task 41B — Authority matrix

- [ ] Write a failing validator requiring all 11 process paths and exact line coverage before creating the matrix.
- [ ] Classify each process claim as `USER_REQUIREMENT`, `PROCESS_EVIDENCE`, `SELF_ASSERTION`, `SCIENTIFIC_CLAIM`, `RUNTIME_CLAIM` or `UNVERIFIED`.
- [ ] Require independent release-source evidence for every scientific/runtime completion claim.
- [ ] Distinguish asset presence/preservation from physical validity and citation truth.
- [ ] Test whether Fable/union passes actually cover Ch1, Ch2 and code or only report their own checklist state.
- [ ] Preserve contradictions rather than resolving them by majority vote or latest-file preference.

#### Task 41C — Verify, result, commit and push

- [ ] Require source/process orphan 0, unsupported authority promotion 0 and every contradiction routed.
- [ ] Run deterministic generation, strict JSON, negative mutation and path/hash validation.
- [ ] Write Step 41 result and update ledger/handover to exact next Step 42.
- [ ] Commit all Step 41 artifacts and result atomically, push and remote-verify.

Run:

```powershell
python Codex\work\v1019_phase060\build_phase060_step41_process_authority.py
python Codex\work\v1019_phase060\validate_phase060_step41_process_authority.py
python -m json.tool Codex\results\PHASE_060_V1019_PROCESS_INTENT_MATRIX.json > $null
git diff --check
```

Commit subject:

```text
audit(phase060): adjudicate v1019 process authority
```

### Step 42 — Code, Test, Runtime and Stored-artifact Audit

#### Task 42A — Full code and assertion read

- [ ] Read all 4 Python files line 1 through EOF, total 1,796 lines.
- [ ] Build module/function/class/public entry/call-edge/state/input/output/unit/default/error/fallback index.
- [ ] Enumerate every regression assertion, demo claim, plot claim, roundtrip criterion and golden comparison.
- [ ] Record dormant code, ignored inputs, direct-vs-indirect call paths and side effects.
- [ ] Inspect all 13 arrays in `golden_graphite_ref.npz` non-destructively: keys, shapes, dtypes, finite values, ranges, hashes and load safety.

#### Task 42B — Disposable runtime execution

- [ ] Read the PDF skill instructions before any PDF work and record the toolchain used.
- [ ] Create a disposable fixture outside `Claude/**` from frozen Git blobs; source directory must remain byte/metadata unchanged.
- [ ] Capture Python and dependency versions, command, cwd, exit, stdout/stderr hash, generated path and output hash for each run.
- [ ] Execute regression, roundtrip and graph-suite paths exactly as their source contracts permit.
- [ ] Rerun deterministic paths and separate expected stochastic/timestamp fields from unexplained drift.
- [ ] Parse the 1,120-line v1.0.20 snapshot witness strictly and compare only claims it explicitly anchors to v1.0.19.

#### Task 42C — PDF, image and genealogy audit

- [ ] Render all 3 PDFs, all 95 pages, and inspect every page at readable resolution.
- [ ] Inspect all 13 unique image blobs; record the v1.0.20 duplicate occurrence without double-counting review authority.
- [ ] Link each stored figure/PDF/data artifact to a source generator or mark generator/provenance `GROUND_NOT_FOUND`.
- [ ] Compare stored, freshly generated and cross-version artifacts by byte hash and semantic/numeric fields.
- [ ] Do not convert visual agreement, internal golden success or synthetic roundtrip into experimental validation.

#### Task 42D — Verify, result, commit and push

- [ ] Write the failing runtime/artifact validator first, then build artifacts until normal mode passes.
- [ ] Require full code/test/demo assertion coverage, runtime records, PDF 95/95 page coverage, image 13/13 unique coverage and NPZ inspection.
- [ ] Negative-test skipped page, altered assertion, missing call edge, dirty `Claude/**`, extra runtime output and golden mismatch.
- [ ] Write Step 42 result and update ledger/handover to Step 43.
- [ ] Commit only Codex scripts/evidence/result/control updates, push and remote-verify.

Run:

```powershell
python Codex\work\v1019_phase060\audit_phase060_step42_runtime_artifacts.py
python Codex\work\v1019_phase060\validate_phase060_step42_runtime_artifacts.py
python -m json.tool Codex\results\PHASE_060_V1019_CODE_TEST_RUNTIME_MATRIX.json > $null
python -m json.tool Codex\results\PHASE_060_V1019_ARTIFACT_AUDIT.json > $null
git diff --check
git diff --exit-code origin/codex/lib-physics-endgame-v1025_2 -- Claude
```

Commit subject:

```text
audit(phase060): verify v1019 runtime artifacts
```

### Step 43 — Doc-leads Theory-to-call-flow Conformance

#### Task 43A — Trace schema and failing validator

- [ ] Start from Step 40 claim/equation anchors, not code symbol names.
- [ ] Require every load-bearing document claim to have an implementation disposition and every public production path to have a document authority disposition.
- [ ] Use `DIRECT`, `RELATED_NOT_DIRECT`, `NOT_APPLICABLE` for evidence relation and `ALIGNED`, `PARTIAL`, `MISALIGNED`, `ABSENT`, `UNVERIFIED` for conformance.
- [ ] Require exact theory source line, code definition line, actual call chain, test assertion and artifact consumer anchors.
- [ ] Validator must fail before the trace artifact exists.

#### Task 43B — End-to-end doc-leads audit

- [ ] Trace Ch1 charge balance, centers, hysteresis, width, broadening, lag/tail, LCO and MSMR routes through actual public call flow.
- [ ] Trace Ch2 partition/configurational/vibrational/electronic/mixing/reversible-heat routes through actual public call flow.
- [ ] Verify whether documented optional inputs are accepted, validated, used, ignored, overwritten or dormant.
- [ ] Verify units and signs at document boundary, public API, internal state, observation output and test assertion.
- [ ] Distinguish a code-map statement from an actual reachable implementation.
- [ ] Detect implementation that predates, bypasses or contradicts v1.0.19 source; retain provenance rather than forcing alignment.

#### Task 43C — Verify, result, commit and push

- [ ] Require document orphan 0, public-call orphan 0, invalid anchor 0 and missing authority boundary 0.
- [ ] Negative-test removed call edge, swapped sign, false direct relation, dormant-as-active promotion and missing assertion.
- [ ] Write Step 43 result, ledger and handover; exact next is Step 44.
- [ ] Commit, push and remote-verify atomically.

Run:

```powershell
python Codex\work\v1019_phase060\build_phase060_step43_doc_code_trace.py
python Codex\work\v1019_phase060\validate_phase060_step43_doc_code_trace.py
python -m json.tool Codex\results\PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json > $null
git diff --check
```

Commit subject:

```text
audit(phase060): trace doc-led implementation
```

### Step 44 — Independent Physics Rederivation

#### Task 44A — Convention and dependency freeze

- [ ] Extract, without silently reconciling, v1.0.19 definitions of external capacity/composition, internal potential, terminal voltage, signed current, temperature and history/state.
- [ ] Establish a symbol/unit/sign table with source anchors and conflict flags.
- [ ] Draw dependency cycles for `xi_j`, background capacity, total charge balance, internal potential, `dQ/dV`, `dV/dQ`, entropy and heat.
- [ ] Separate explicit definition, implicit system, numerical method, observation operator and empirical closure.

#### Task 44B — Charge-balance and observation derivation

- [ ] Re-derive the governing residual as `F(U; Q, T, I, history, parameters) = 0` using source-defined coordinates.
- [ ] Derive the local implicit sensitivity `dU/dQ = -F_Q/F_U` only where differentiability and nonzero `F_U` are justified.
- [ ] Prove or delimit uniqueness/monotonicity assumptions; plateau, multi-root and nonmonotone cases must remain conditional if not closed.
- [ ] Derive `dQ/dV` and `dV/dQ` transformations, singular cases, normalization and capacity conservation.
- [ ] Check every step dimensionally and by an independent finite-difference route.

#### Task 44C — Temperature, current and material observation derivation

- [ ] Re-derive center and width temperature laws, entropy coefficients, reversible heat and any Einstein/mixing contributions from stated thermodynamic potentials.
- [ ] Re-derive current/kinetic/lag/tail dependence with chronology, zero-current, rest, reversal and finite-window limits.
- [ ] Re-derive graphite and LCO observation paths separately before any full-cell or common-output composition.
- [ ] Separate half-cell/full-cell sign conventions and electrode/reaction/control-volume heat signs.
- [ ] Check whether material-specific numbers have primary-source authority, fit-only authority or no found authority.

#### Task 44D — Identifiability and independent probes

- [ ] Identify parameter combinations that are structurally inseparable from the equations and observation operator.
- [ ] Calculate symbolic or analytic limits and independent numerical finite differences without importing production functions.
- [ ] Probe conservation, monotonicity, finite values, continuity, zero-current, equilibrium, high/low-temperature and small-perturbation limits where the source model defines them.
- [ ] Classify every check as `PASS`, `FAIL`, `CONDITIONAL`, `UNVERIFIED` or `NOT_APPLICABLE`; a numerical match cannot repair a missing physical assumption.

#### Task 44E — Verify, result, commit and push

- [ ] Write the derivation validator before the final derivation artifact and record controlled initial failure.
- [ ] Require equation anchors, derivation steps, units, signs, domains, assumptions, limits, independent probe and code-conformance impact.
- [ ] Have independent spec and quality reviewers report P0/P1/P2 findings; controller resolves or records each finding.
- [ ] Write Step 44 result and update ledger/handover to Step 45.1.
- [ ] Commit, push and remote-verify atomically.

Run:

```powershell
python Codex\work\v1019_phase060\build_phase060_step44_physics_validation.py
python Codex\work\v1019_phase060\validate_phase060_step44_physics_validation.py
python -m json.tool Codex\results\PHASE_060_V1019_PHYSICS_VALIDATION.json > $null
git diff --check
```

Commit subject:

```text
audit(phase060): rederive v1019 physics
```

### Step 45.1 — Claim, Defect and Carry-forward Disposition

- [ ] Build the disposition schema and failing validator before outputs.
- [ ] Route every Step 40 scientific claim, Step 41 process claim, Step 42 runtime/artifact finding, Step 43 conformance row and Step 44 derivation finding.
- [ ] Assign exactly one primary disposition: `PRESERVE`, `CORRECT`, `SUPERSEDE`, `EMPIRICAL_ONLY`, `THEORY_ONLY`, `REJECT` or `UNVERIFIED`.
- [ ] Record source anchors, evidence paths, authority boundary, acceptance criterion, affected implementation/test/artifact and target Phase.
- [ ] Reconcile inherited Phase 059 open items touched by v1.0.19 without treating new evidence as resolution unless their stored acceptance criterion is fully met.
- [ ] Register genuinely new blockers with non-colliding IDs and do not duplicate an existing finding family.
- [ ] Separate Phase 061–069 lineage targets from Phase 070+ conditional science/data/implementation targets.
- [ ] Require source orphan 0, disposition conflict 0, missing acceptance/authority/target 0 and external-validity promotion 0.
- [ ] Write Step 45.1 result, update ledger/handover to Step 45.2, commit, push and remote-verify.

Run:

```powershell
python Codex\work\v1019_phase060\build_phase060_step45_dispositions.py
python Codex\work\v1019_phase060\validate_phase060_step45_dispositions.py
python -m json.tool Codex\results\PHASE_060_V1019_DISPOSITION_MATRIX.json > $null
python -m json.tool Codex\results\PHASE_060_V1019_CARRY_FORWARD_DELTA.json > $null
git diff --check
```

Commit subject:

```text
audit(phase060): disposition v1019 lineage
```

### Step 45.2 — Integrated Validation, Lineage Report C and Final Gate

- [ ] Re-read master, this detailed plan, Step 45.1 result, all Step 40–45.1 results and all machine artifacts to their full applicable scope.
- [ ] Reconstruct primary coverage `77/77` paths/blobs and witness coverage `2/2` occurrences with `1` new blob.
- [ ] Reconstruct full inspection workload: text 61/61 and 9,904/9,904 physical plus 9,145/9,145 nonblank lines, PDFs 3/3 and 95/95 pages, images 13/13 unique and 14/14 occurrences, binary 1/1.
- [ ] Enumerate every subordinate validator and fresh result. Platform/environment failures remain raw and separated from normalized/scientific checks.
- [ ] Verify every Step result and required machine artifact is co-committed and every containing commit belongs to origin-active ancestry.
- [ ] Run final validator in normal mode, deterministic rerun, negative mutation suite, exact clean descendant and dirty tracked/untracked fixtures.
- [ ] Write `LINEAGE_REPORT_C` with Summary, Step Range, Inputs, Files, Read Coverage, Source Topology, Process Authority, Runtime/Artifact Evidence, Doc-code Conformance, Physics Rederivation, Dispositions, Gate Boundary, Non-changes, Open Issues and Next.
- [ ] Write `PHASE_060_RESULT.md` as an independent recovery document with Objective/Authority, cumulative Step Range, exact Inputs and Actual Read Coverage, Files Created/Updated, Commands and Execution Evidence, Validation, exclusive Gate, Confirmed, Unverified, Ground Not Found, Unresolved/Decision Queue, Protected Non-changes and the exact Phase 061 entry condition.
- [ ] Select exactly one of `PASS_P060_LINEAGE_C`, `CONDITIONAL_P060` or `FAIL_P060`.
- [ ] Update both ledgers and active handover to the selected gate and exact next Phase 061 detailed-plan creation. Step 46 may not begin before that plan is saved and reviewed.
- [ ] Write Phase result and Step 45.2 gate result before the containing commit.
- [ ] Commit all final Step artifacts/result/control updates atomically, push and remote-verify.

Run:

```powershell
python Codex\work\v1019_phase060\validate_phase060_final.py
python -m json.tool Codex\results\PHASE_060_VALIDATION.json > $null
git diff --check
git diff --exit-code origin/codex/lib-physics-endgame-v1025_2 -- Claude
```

Commit subject:

```text
audit(phase060): close v1019 lineage gate
```

## Phase Gate

`PASS_P060_LINEAGE_C` may be assigned only when all of the following are true.

- Primary 77-path/77-blob queue and separate 2-path witness queue have complete recorded disposition.
- All 60 primary text files/8,784 physical and 8,025 nonblank lines plus the 1,120-physical/nonblank-line witness JSON are fully read or strictly parsed; all 42 TeX/5,636 lines have source-order coverage.
- Ch1/Ch2 root include expansion and all section edges are complete, with unresolved external references explicitly bounded.
- All 4 Python files/1,796 lines, public call paths and release assertions are fully read.
- Runtime is executed in a disposable fixture, and stored/fresh artifact disagreements are recorded rather than hidden.
- All 3 PDFs/95 pages, 13 unique images and the NPZ have full audit coverage.
- Doc-leads claims are connected to actual reachable call flow, tests and artifacts with no orphan.
- Charge-balance, temperature/current, LCO/graphite observation paths are independently rederived with assumptions, dimensions, signs, limits and identifiability recorded.
- Every claim/finding has one disposition, authority boundary, acceptance criterion and target; external validity remains outside PASS.
- Protected branch, `main` and `Claude/**` are unchanged.
- Every execution unit result is contained in its atomic commit, pushed and remote-verified.

`PASS_P060_LINEAGE_C` means the declared v1.0.19 lineage audit, internal conformance routing and independent derivation review are complete. It does not mean canonical-model selection, defect repair, primary-literature truth, graphite/LCO/Si/blend external validation, parameter identifiability, low-temperature mechanism identification, final LaTeX/PDF or publication readiness.

`CONDITIONAL_P060` is allowed only when a bounded declared Phase 060 audit requirement cannot be completed but the exact missing path/evidence/authority and downstream consequence are recorded. `UNVERIFIED` scientific truth alone does not force conditional status when audit coverage and routing are complete.

`FAIL_P060` is required for missing frozen source, incomplete mandatory read/page coverage, unresolved source/output genealogy, invalid disposition routing, unexplained protected/Claude drift, or a failed required validator that cannot be isolated as an environment-only debt.

## Implementation Interfaces

### Source coverage record

```json
{
  "path": "Claude/docs/v1.0.19/_sections/ch1_sec01_n0n1.tex",
  "owner": "P060_PRIMARY_RELEASE",
  "git_blob_sha1": "695b5610120395989ad1143661d9c9bcaea07235",
  "sha256": "ef5c9b92d9619c565620392d82e8cd36d3d466423d5a4b3e41c5fc95572139af",
  "review_mode": "FULL_TEXT",
  "expected_extent": {"lines": 205},
  "actual_coverage": [{"start": 1, "end": 205}],
  "coverage_status": "READ_FULL",
  "evidence": ["P060-SRC-CH1-SEC01"],
  "authority_boundary": "source presence and content, not external truth"
}
```

### Theory–implementation trace row

```json
{
  "trace_id": "P060-TRACE-0001",
  "claim_id": "P060-CLM-0001",
  "theory_anchor": {"path": "Claude/docs/v1.0.19/_sections/ch1_sec01_n0n1.tex", "lines": "1-205"},
  "implementation_anchor": {"path": "Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py", "lines": "1-1151", "symbol": "UNRESOLVED_AT_PLAN_STAGE"},
  "call_chain": [],
  "test_assertions": [],
  "artifact_consumers": [],
  "relation": "DIRECT|RELATED_NOT_DIRECT|NOT_APPLICABLE",
  "status": "ALIGNED|PARTIAL|MISALIGNED|ABSENT|UNVERIFIED",
  "unit_check": "PASS|FAIL|UNVERIFIED|NOT_APPLICABLE",
  "sign_check": "PASS|FAIL|UNVERIFIED|NOT_APPLICABLE",
  "authority_boundary": "UNVERIFIED until Step 43 resolves an exact reachable implementation anchor"
}
```

### Independent derivation check

```json
{
  "check_id": "P060-PHY-0001",
  "equation_or_claim_ids": [],
  "source_anchors": [],
  "assumptions": [],
  "derivation_steps": [],
  "dimensions": {},
  "sign_convention": "SOURCE_CONVENTION_TO_BE_EXTRACTED_WITHOUT_RECONCILIATION",
  "domain": "UNVERIFIED_AT_PLAN_STAGE",
  "analytic_limits": [],
  "independent_probe": {},
  "result": "PASS|FAIL|CONDITIONAL|UNVERIFIED|NOT_APPLICABLE",
  "implementation_impact": [],
  "authority_boundary": "A numerical probe cannot establish an unstated physical assumption"
}
```

### Disposition row

```json
{
  "disposition_id": "P060-DISP-0001",
  "source_ids": [],
  "primary_disposition": "PRESERVE|CORRECT|SUPERSEDE|EMPIRICAL_ONLY|THEORY_ONLY|REJECT|UNVERIFIED",
  "evidence_paths": [],
  "acceptance_criterion": "Exact source, derivation, implementation and test anchors must agree within the recorded domain",
  "authority_boundary": "Internal lineage disposition only; external material truth remains false",
  "target_phase": 61,
  "activation_gate": "PASS_P060_LINEAGE_C",
  "external_material_truth_validated": false
}
```

## Test and Validation Plan

### Plan and numbering

- Validate required section order and exact detailed-plan path.
- Validate cumulative Steps 40, 41, 42, 43, 44, 45.1 and 45.2 with no reset.
- Validate all declared result/machine/script paths and commit subjects.
- Validate both ledgers and handover point to the same plan, status and exact next.

### Source and read coverage

- Derive expected paths and blobs from Git objects, not checkout enumeration alone.
- Use Git blob bytes for canonical hashes and POSIX paths in JSON.
- Require unioned read intervals to cover `1..EOF` with no gap or overlap ambiguity.
- Strict-parse JSON with duplicate-key rejection and recursively traverse every consumed record.
- Validate PDF page count and image identity from file content, not extension only.

### Scientific and conformance checks

- Check dimensions, signs, independent variables, domains, boundaries and implicit dependencies separately.
- Compare analytic derivative with finite difference without importing production implementation.
- Check equilibrium, zero-current, rest/reversal, low/high-temperature and singular limits only where the source model defines a valid domain.
- Separate internal consistency, external validity, model selection and parameter identifiability.

### Runtime and artifact checks

- Execute only in a disposable fixture outside `Claude/**`.
- Record environment and every command/exit/hash.
- Compare generated and stored results structurally and numerically; do not require byte identity for fields proven environment-dependent.
- Preserve raw failures and document normalized comparison rules before applying them.

### Negative validation

- Mutate one required condition per fixture: path, blob, extent, include edge, source anchor, assertion, call edge, unit, sign, disposition, authority, acceptance, target, output genealogy or dirty state.
- Require each mutation to fail for the intended diagnostic.
- Run validators against an external clean descendant and dirty tracked/untracked fixtures.

### Git and remote gates

- Before every unit: clean status, local/upstream/origin equality, protected/main expected tips.
- Before commit: exact file allowlist, `git diff --check`, JSON parse and `Claude/**` diff 0.
- After commit: verify exact commit files, push active branch, compare local HEAD/upstream/`git ls-remote`, and confirm protected/main unchanged.
- Three consecutive same-cause push failures are a hard stop.

## Stop Conditions

- Any of the 77 primary paths or expected Git blobs differs from the frozen baseline without a recorded branch/source-boundary correction.
- Protected branch, `main`, or `Claude/**` changes unexpectedly.
- Active remote branch diverges from the expected local ancestry.
- Source execution would require writing tracked/untracked artifacts into `Claude/**` and a disposable fixture cannot reproduce the path.
- A required PDF/image/blob cannot be read after three independent tool/path investigations.
- A physical claim cannot be safely classified as `UNVERIFIED`, `CONDITIONAL` or an alternative without inventing a model/parameter.
- Validator failure remains inseparable between scientific/content defect and environment/portability debt after three independent investigations.
- Same-cause push failure occurs three times.

## Assumptions

- Phase 059 artifacts are predecessor evidence, not automatic approval of v1.0.19 copy-forward content.
- The 66 release entries and 11 supplementary entries remain exact at frozen Git baseline; Step 40 independently rechecks this.
- Process records are fully reviewed because the user asked to preserve working history, but their self-assessment authority remains bounded.
- The v1.0.20 snapshot witness may clarify runtime continuity but cannot decide Phase 061 content or inflate Phase 060 primary coverage.
- Runtime dependencies available in the workspace are sufficient for at least structural and isolated tests; missing optional dependency becomes explicit environment debt, not fabricated PASS.
- Phase 060 can PASS as an audit with open scientific defects if every defect is detected, bounded and routed. It cannot PASS with incomplete mandatory source/page/call-flow coverage.
- Phase 061 detailed plan must be saved, reviewed, committed and pushed before Step 46.

## Correction History

- 2026-08-25: Created as the required Phase 060 child plan after Phase 059 Step 39.6 commit `e01049489bf601c433d97d4b4121cf0fdcfca085` was pushed and remote-verified.
- 2026-08-25: Expanded the 66-path release manifest with 11 V1019 process records required by inherited Step 41 while keeping v1.0.20 witnesses outside the primary Phase 060 count.
- 2026-08-25: Split final Step 45 into 45.1 disposition and 45.2 integrated gate so each risky closure has an atomic remote recovery point without restarting cumulative numbering.
- 2026-08-25: Added disposable runtime, PDF 95-page, 13-unique-image, NPZ, strict JSON, negative mutation and clean-descendant gates.
