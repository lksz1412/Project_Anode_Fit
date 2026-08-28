# Phase 063 v1.0.22 Lineage Reaudit Implementation Plan

> **For Codex:** Use `superpowers:executing-plans`, `superpowers:subagent-driven-development` when capacity permits, `superpowers:test-driven-development`, `superpowers:systematic-debugging`, `superpowers:verification-before-completion`, and `harness-core` evidence gates. Result-first artifacts, exact-path atomic commits, immediate pushes, and post-commit persistence terminals are mandatory.

정본일: 2026-08-28
Phase: 063
누적 Step 범위: 58–63 (`63.1`, `63.2` 포함)
대상 lineage: v1.0.22
예상 직전 commit: `69d938da0f5649d6342364c96bf612488879a8f8`
활성 branch: `codex/anode-fit-v1025_2-canonical-completion`
보호 branch: `codex/lib-physics-endgame-v1025_2`
보호 branch 고정 tip: `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`
main 고정 tip: `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`
frozen source baseline: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`
최종 Gate 후보: `PASS_P063_LINEAGE_F`, `CONDITIONAL_P063`, `FAIL_P063`

---

## Summary

Phase 063은 frozen v1.0.22의 204개 manifest occurrence와 release denominator 밖의 supplemental version master plan 1개를 전수 재감사한다. 목적은 v1.0.22가 수행한 graphite/LCO/Si 3장 재편, equation·label·bibliography 이동, graphite·열역학 교육 다리, LCO 축약 closure, Si/SiO_x/Si–C 및 graphite–Si blend의 첫 실질 이론·코드 확장, reviewer proposal과 master adoption, code/runtime, PDF build 및 말기 상태 문건의 충돌을 하나의 손실 없는 lineage로 복구하는 것이다.

이 Phase는 과거 `PASS`, `H0`, `치명 0`, build GREEN, DOI/Crossref 확인 또는 bit-exact 회귀를 external scientific/material/experimental truth로 승격하지 않는다. v1.0.22는 강한 내부 정합성과 중요한 중간 이론 자산을 가진 `VALUABLE_INTERMEDIATE_BASELINE`이지만, 독립 문헌 원문·공개 데이터·식별성·held-out 검증 전에는 canonical model 또는 publication-ready artifact가 아니다.

본 계획은 다음 원칙을 강제한다.

1. 204 release/process occurrences와 supplemental plan 1개를 합산해 “205 release sources”라고 부르지 않는다.
2. final release surface, version plans, status/machine/process records, competing reviewer/candidate records를 별도 identity universe로 유지한다.
3. Phase 057 P–Z의 101문건/16,855행 전문 검독과 96개 provisional findings는 routing input이지 Phase 063 결론이 아니다.
4. proposal, reviewer finding, cherry-pick decision, 실제 source patch, built PDF page를 분리한다.
5. 수식·코드·runtime·build·서지 metadata·외부 재료 truth의 권위를 서로 승격하지 않는다.
6. 물리 본문에서 코드/API/default를 제거해야 한다는 사용자의 최종 방향을 보존하되, frozen v1.0.22는 수정하지 않고 향후 canonical owner에 정확히 routing한다.

## Current Ground Truth

### Git and protection state

- Phase 062 Step 57.2 commit은 `69d938da0f5649d6342364c96bf612488879a8f8`이다.
- subject는 `audit(phase062): close v1021 lineage gate`, parent는 `247e9b0b28d185604753f40ee0244cfe0bf068cf`, changed paths는 exact eight다.
- `PASS_P062_STEP57_2_PERSISTENCE`가 실제 commit에서 관찰됐다.
- local HEAD, upstream, origin tracking ref와 live origin active tip은 위 commit으로 일치한다.
- 보호 branch local/tracking/live tip과 main tracking/live tip은 본문 상단의 고정값과 일치한다.
- `Claude/**`는 Phase 062 parent→Step 57.2 commit 사이에서 변경 0이다.

### Frozen v1.0.22 manifest denominator

Phase 056 source manifest의 immutable predicate를 사용한다.

```text
manifest = Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json
manifest_canonical_utf8_lf_normalized_sha256 = 60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef
baseline_commit = 3b5fd059ed09cdcdde38668c399cb35b8afbcca9
exact_v1022_set = every manifest.entries row whose version is exactly "v1.0.22"
```

확인된 immutable inventory:

- 204 path occurrences / 204 unique paths / 204 unique Git blobs / 4,974,148 bytes.
- review mode: `FULL_TEXT=200`, `FULL_PDF=4`; image와 binary-introspection occurrence는 0.
- text: 30,219 physical lines, 26,137 nonblank lines.
- PDF: 4 files / 133 pages (`8/83/25/17`).
- extension: Python 3, Markdown 101, TeX 95, PDF 4, JSON 1.
- role: code 1, implementation guide 1, theory 55, result 136, generated document 4, plan 6, test 1.
- Phase 056 manifest 1-based indices는 540–743이다.
- v1.0.21과 같은 relative path 42개: byte-identical 5, changed 37; v1.0.22-only 162, v1.0.21-only 26이다.
- v1.0.21/v1.0.22 cross-version shared blob은 5개다.

### Mandatory denominator partitions

204 occurrence는 다음 네 분할을 유지한다.

| Partition | Paths | Text | Physical / nonblank lines | PDF / pages | Bytes | Authority ceiling |
|---|---:|---:|---:|---:|---:|---|
| final release surface | 63 | 59 | 10,462 / 9,733 | 4 / 133 | 2,985,072 | frozen release content/build only |
| version-local plans | 6 | 6 | 287 / 242 | 0 / 0 | 30,249 | process intent only |
| status/machine/process | 10 | 10 | 2,398 / 2,236 | 0 / 0 | 158,352 | self-report or machine structure only |
| competing/reviewer/candidate | 125 | 125 | 17,072 / 13,926 | 0 / 0 | 1,800,475 | proposal/review evidence only |

Partition 규칙:

- `final release surface`: `Claude/docs/v1.0.22/` 바로 아래 파일과 `_sections/**`, 단 `plans/**`, `results/**` 제외.
- `version-local plans`: `Claude/docs/v1.0.22/plans/**`.
- `status/machine/process`: `Claude/docs/v1.0.22/results/**` 중 `comp_*` subtree 밖.
- `competing/reviewer/candidate`: `Claude/docs/v1.0.22/results/comp_*/**`.
- final release surface 63과 process 141을 합산한 204는 source-manifest workload이며, 모두 최종 채택 source라는 뜻이 아니다.

### Supplemental process-control denominator

`Claude/plans/2026-07-17-v1022-master-plan.md`는 204-row v1.0.22 manifest 밖에 있다. 그러나 D22-1–D22-8, R0–R9와 사용자 지시의 second-order process record를 담으므로 별도 supplemental identity로 감사한다.

- frozen Git blob: `f50deee51df77dca8d07a2d9b9fd150fa93309cc`.
- Git blob bytes: 16,115.
- physical/nonblank lines: 99/79.
- 이 파일의 사용자 지시 인용은 repository-reported actor evidence이며 독립 사용자 transcript로 승격하지 않는다.
- combined workload는 `204 manifest occurrences + 1 supplemental process-control occurrence`로만 병기한다.

### Process and history topology

- frozen baseline까지 `Claude/docs/v1.0.22/**`를 건드린 commit은 100개다.
- 최초 version commit은 `5d815235de4e302ff5d7a076d525921ab417eadf`, R1 재편은 `57109155f4ae45f3796ae8068260cf100d9e1ae0`, RA/R1b는 `704e8da60e956c31cc714cd067a2403dbc957abf`다.
- R2/R3/R4/R5/R6/R7/R8/R9, FR, AUD, C-041–C-056과 v1.0.23 survey가 같은 version subtree에 누적됐다.
- R9 마감 후에도 C-055/C-056과 PDF rebuild, 독립 AUD, downstream survey가 이어졌으므로 handover/index/merge-readiness의 self-report를 시간 독립 정본으로 취급하지 않는다.
- Step 58은 100개 commit의 parent/subject/path patch를 재구성하고 각 manifest occurrence에 first-add, last-touch, final-blob, actor/process role을 연결한다.

### Phase 057 v1.0.22 intent evidence

Phase 057 P–Z는 101 unique documents / 16,855 physical lines를 전문 검독했고 `INTENT-PROV-0096`–`INTENT-PROV-0191` 96개 provisional records를 남겼다.

- `USER_REQUIREMENT=6` records는 repository-reported evidence다.
- `REVIEW_FINDING=72` records는 direct reaudit finding이지만 current source patch 상태를 다시 대조해야 한다.
- `IMPLEMENTED_STATE=8` records는 patch confirmation이 필요하다.
- `MODEL_PROPOSAL=10` records는 explicit proposal/plan attribution일 뿐 채택이 아니다.
- 96개 finding은 Phase 063의 mandatory routing denominator다. orphan, duplicate closure, status promotion을 허용하지 않는다.

### Confirmed high-risk domains to re-adjudicate

아래는 계획 입력이며 아직 Phase 063 결론이 아니다.

1. R1은 equation block 188개와 bibliography key 66개를 보존하며 material chapter 책임을 재배치했지만 산문/물리 진실은 검증하지 않았다.
2. independent-site explicit logistic, regular-solution implicit mean field, two-phase coexistence가 산문과 식에서 혼합됐다.
3. TST partition-ratio, activation entropy/enthalpy와 high-temperature prefactor의 경계가 흔들렸다.
4. equilibrium fluctuation/susceptibility, empirical peak scale `n_j`, heterogeneity/observation broadening과 finite-current tail이 섞였다.
5. C-rate hour/second 혼용은 lag length를 3,600배 바꾸고 barrier에 `RT ln 3600` 규모로 흡수될 수 있다.
6. LCO local MIT/charge-order/regular-solution closure와 frozen global electronic entropy offset이 동일하지 않다.
7. charge-order `0.47/1.49 J mol^-1 K^-1`와 조성/출처 귀속은 primary-source confirmation이 없다.
8. graphite–Si common-potential charge balance는 equilibrium zero-order baseline이지만 host current partition, finite-rate nonadditivity와 stress/history closure를 제공하지 않는다.
9. external Si mass fraction `m_Si`, active mass, capacity fraction `f_Si`, loading과 ICE/utilization 변환을 분리해야 한다.
10. Si/SiO_x/Si–C demo transition parameters, SiO_x `U=0.300 V`, GS-1/GS-2는 schematic/unsupported 상태다.
11. Larché–Cahn stress–potential coupling은 reversible shift 출발점이나 plasticity/damage/path-history closure가 아니다.
12. reviewer report, cherry-pick, source patch, build/PDF와 external experimental validation은 서로 다른 evidence layer다.

### Carry-forward and debt boundary

- Phase 062가 보존한 inherited carry 52, Phase 060 blockers 5, canonical debt 91, Phase 061 blockers 5는 직접 acceptance evidence 없이 상태를 바꾸지 않는다.
- Phase 062 open findings 59와 v1.0.21 dispositions 68은 Phase 063 source coverage denominator와 합산하지 않는다. v1.0.22에서 실제 supersession 또는 persistence evidence가 있을 때만 corroborating edge를 추가한다.
- Phase 057 v1.0.22 provisional findings 96은 새 audit input layer이며 96개 모두 disposition과 downstream owner를 가져야 한다.
- v1.0.22에서 발견된 genuinely new blocker는 기존 canonical debt와 중복 여부를 먼저 판정한 뒤에만 생성한다.
- external literature, data, identifiability, canonical theory owner가 뒤 Phase에 있으면 Phase 063의 내부 재계산만으로 조기 resolve하지 않는다.

## Phase Range

| Phase | Step | Name | Primary output | Gate |
|---|---:|---|---|---|
| activation | pre-Step 58 | detailed-plan activation | plan + activation validation/result | `PASS_P063_PLAN_ACTIVATION` |
| 063 | 58 | source/process topology and full-read attestation | topology + read attestation | `PASS_P063_STEP58_SOURCE_PROCESS_TOPOLOGY` |
| 063 | 59 | equation/material rederivation | equation/material matrix | `PASS_P063_STEP59_EQUATION_MATERIAL_REDERIVATION_WITH_CONCERNS` |
| 063 | 60 | literature/quantity/scope authority | literature scope matrix | `PASS_P063_STEP60_LITERATURE_SCOPE_WITH_CONCERNS` |
| 063 | 61 | code/runtime/concordance delta | code matrix + runtime attestation | `PASS_P063_STEP61_CODE_RUNTIME_DELTA_WITH_CONCERNS` |
| 063 | 62 | review/adoption/build/state closure | closure matrix | `PASS_P063_STEP62_REVIEW_ADOPTION_CLOSURE_WITH_CONCERNS` |
| 063 | 63.1 | source disposition and carry-forward delta | disposition + carry delta | `PASS_P063_STEP63_1_DISPOSITIONS` |
| 063 | 63.2 | integrated validation and Lineage Report F | final validation/report/result | `PASS_P063_LINEAGE_F` or lower gate |

Step 번호는 Phase가 바뀌어도 재시작하지 않는다. Step 58은 Step 57.2 다음 누적 번호다.

## Exact Read Inputs

### Control inputs — full read at every recovery boundary

1. `Codex/AGENTS.md`.
2. `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`.
3. 이 detailed plan.
4. 직전 완료 Step result.
5. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`.
6. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`.
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`.
8. `Codex/results/PHASE_062_RESULT.md`와 `PHASE_062_VALIDATION.json`.

### Frozen inventory and prior routing inputs

1. `Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json`.
2. `Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json`.
3. Phase 057 P–Z observation documents 11개, 1–EOF.
4. `Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json`.
5. `Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json`.
6. `Codex/results/PHASE_062_V1021_DISPOSITION_MATRIX.json`.
7. `Codex/results/PHASE_062_V1021_CARRY_FORWARD_DELTA.json`.

### Primary v1.0.22 manifest corpus

Step 58은 immutable predicate로 204개 path를 정렬된 explicit queue로 materialize한다. 사람이 다시 입력한 glob/list를 정본으로 사용하지 않는다.

- `FULL_TEXT` 200개는 UTF-8 decode, physical/nonblank line denominator와 1–EOF coverage interval을 기록한다.
- `FULL_PDF` 4개는 raw SHA, page count와 각 page render/read attestation을 기록한다.
- final release 63, plan 6, status/machine/process 10, competing/reviewer/candidate 125 partition을 유지한다.
- competing TeX/Markdown은 proposal content이며 final source로 자동 승격하지 않는다.

### Supplemental process-control source

- `Claude/plans/2026-07-17-v1022-master-plan.md`, frozen blob `f50deee51df77dca8d07a2d9b9fd150fa93309cc`, 99/79 lines.

### Comparison and genealogy inputs

- v1.0.21 release 68 occurrence 및 Step 52–57.2 Phase 062 artifacts.
- v1.0.22 100-commit process chain.
- v1.0.23 first-copy and downstream survey commits for later correction/supersession evidence only.
- same-relative path pair 42, v1.0.22-only 162, v1.0.21-only 26, shared blob 5.
- R1 snapshot, change log, execution/reference ledgers, handover, index, merge readiness.

## Non-goals and Scope Guards

- `Claude/**`를 수정하지 않는다.
- 보호 branch와 main을 수정·merge·rebase하지 않는다.
- frozen v1.0.22 proposal LaTeX를 새 canonical manuscript로 cherry-pick하지 않는다.
- Phase 063에서 새 생산 물리식, 최종 LaTeX/PDF, 실제 fitting code 또는 dataset을 만들지 않는다.
- DOI/metadata/abstract만으로 equation, numerical parameter, material mechanism 또는 experimental truth를 승인하지 않는다.
- build/PDF page, test, bit-exact, internal round-trip을 external validity로 승격하지 않는다.
- graphite/LCO/Si/SiO_x/Si–C 또는 blend의 demo/placeholder parameter를 production default로 승인하지 않는다.
- `m_Si`와 `f_Si`, equilibrium common potential과 host current equality, regular-solution spinodal과 equilibrium hysteresis를 동일시하지 않는다.
- reviewer vote가 없으면 GNF로 기록하고 합성 vote를 만들지 않는다.
- stale handover/index/merge-readiness self-report를 실제 source/commit chronology 없이 최신 상태로 채택하지 않는다.
- 코드 함수명/API/default는 frozen source 분석 및 지정된 implementation evidence에서만 다룬다. 향후 physics manuscript 본문 권위로 승격하지 않는다.

## Implementation Changes

### Plan activation — exact seven

1. `Codex/plans/2026-08-28-phase063-v1022-lineage-detailed-plan.md`.
2. `Codex/work/v1022_phase063/validate_phase063_plan.py`.
3. `Codex/results/PHASE_063_PLAN_ACTIVATION_VALIDATION.json`.
4. `Codex/results/PHASE_063_PLAN_ACTIVATION_RESULT.md`.
5. active execution ledger.
6. parent execution ledger.
7. active handover.

### Step 58 — exact eight

1. `Codex/work/v1022_phase063/build_phase063_step58_source_process_topology.py`.
2. `Codex/work/v1022_phase063/validate_phase063_step58.py`.
3. `Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json`.
4. `Codex/results/PHASE_063_V1022_READ_ATTESTATION.json`.
5. `Codex/results/PHASE_063_STEP_058_SOURCE_PROCESS_TOPOLOGY_RESULT.md`.
6. both execution ledgers.
7. active handover.

### Step 59 — exact seven

1. `Codex/work/v1022_phase063/build_phase063_step59_equation_material_rederivation.py`.
2. `Codex/work/v1022_phase063/validate_phase063_step59.py`.
3. `Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json`.
4. `Codex/results/PHASE_063_STEP_059_EQUATION_MATERIAL_REDERIVATION_RESULT.md`.
5. both execution ledgers.
6. active handover.

### Step 60 — exact seven

1. `Codex/work/v1022_phase063/build_phase063_step60_literature_scope.py`.
2. `Codex/work/v1022_phase063/validate_phase063_step60.py`.
3. `Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json`.
4. `Codex/results/PHASE_063_STEP_060_LITERATURE_SCOPE_RESULT.md`.
5. both execution ledgers.
6. active handover.

### Step 61 — exact eight

1. `Codex/work/v1022_phase063/build_phase063_step61_code_runtime_delta.py`.
2. `Codex/work/v1022_phase063/validate_phase063_step61.py`.
3. `Codex/results/PHASE_063_V1022_CODE_DELTA_MATRIX.json`.
4. `Codex/results/PHASE_063_V1022_RUNTIME_ATTESTATION.json`.
5. `Codex/results/PHASE_063_STEP_061_CODE_RUNTIME_DELTA_RESULT.md`.
6. both execution ledgers.
7. active handover.

### Step 62 — exact seven

1. `Codex/work/v1022_phase063/build_phase063_step62_review_adoption_closure.py`.
2. `Codex/work/v1022_phase063/validate_phase063_step62.py`.
3. `Codex/results/PHASE_063_V1022_REVIEW_ADOPTION_CLOSURE_MATRIX.json`.
4. `Codex/results/PHASE_063_STEP_062_REVIEW_ADOPTION_CLOSURE_RESULT.md`.
5. both execution ledgers.
6. active handover.

### Step 63.1 — exact eight

1. `Codex/work/v1022_phase063/build_phase063_step63_dispositions.py`.
2. `Codex/work/v1022_phase063/validate_phase063_step63_dispositions.py`.
3. `Codex/results/PHASE_063_V1022_DISPOSITION_MATRIX.json`.
4. `Codex/results/PHASE_063_V1022_CARRY_FORWARD_DELTA.json`.
5. `Codex/results/PHASE_063_STEP_063_1_DISPOSITION_RESULT.md`.
6. both execution ledgers.
7. active handover.

### Step 63.2 — exact eight

1. `Codex/work/v1022_phase063/validate_phase063_final.py`.
2. `Codex/results/PHASE_063_VALIDATION.json`.
3. `Codex/results/PHASE_063_V1022_LINEAGE_REPORT_F.md`.
4. `Codex/results/PHASE_063_STEP_063_2_GATE_RESULT.md`.
5. `Codex/results/PHASE_063_RESULT.md`.
6. both execution ledgers.
7. active handover.

모든 result는 containing commit 전에 작성하며 `PENDING_AT_PRECOMMIT_BY_DESIGN`을 기록한다. precommit content Gate와 postcommit persistence terminal은 별개다. 각 checkpoint는 exact paths, exact subject, exact parent, local/upstream/live-origin equality와 clean status를 검증한 뒤 다음 Step을 연다.

## Plan Activation Unit — Save Before Step 58

### Activation A — Recovery and validator-first RED

1. AGENTS, master plan, Phase 062 final result/validation, both ledgers와 active handover를 전문 재독한다.
2. Phase 057 P–Z 11개 observation과 v1.0.22 supplemental plan을 1–EOF 재독한다.
3. activation exact-seven allowlist, parent, subject와 source denominators를 고정한다.
4. result-first로 `PHASE_063_PLAN_ACTIVATION_RESULT.md`를 작성한다.
5. validation JSON이 없는 상태에서 validator를 실행해 전용 missing-artifact RED를 확인한다.

### Activation B — Exact plan/source/process/routing validation

1. detailed plan의 누적 Step 58–63.2, phase range, 산출물 allowlist, gates, stop conditions를 검증한다.
2. manifest 204와 네 partition, text/PDF/lines/pages/bytes, supplemental 1을 frozen Git blob에서 독립 재계산한다.
3. Phase 057 v1.0.22 input 96 finding과 P–Z 11 files를 exact hash/line range로 검증한다.
4. Phase 062 predecessor persistence, branch/upstream/live/protected/main/Claude invariants를 검증한다.
5. semantic negative controls, strict JSON controls, deterministic projection과 exact staged boundary controls를 실행한다.
6. validation JSON은 result와 다른 nonself outputs가 모두 고정된 뒤 마지막에 쓴다.

### Activation C — Result, exact commit and persistence

1. activation result에 읽은 범위, denominators, outputs, commands, Gate와 Step 58 entry condition을 기록한다.
2. exact seven만 stage하고 index/worktree byte equality와 `git diff --check`를 확인한다.
3. subject `docs(phase063): plan v1022 lineage reaudit`로 atomic commit한다.
4. 즉시 active branch에 push한다.
5. full 40-character commit으로 `PASS_P063_PLAN_ACTIVATION_PERSISTENCE`를 확인한다.
6. 그 terminal 전에는 Step 58 implementation을 시작하지 않는다.

## Phase 063 — v1.0.22 Reaudit

### Step 58 — Source/Process Topology and Full-read Attestation

#### Task 58A — Immutable denominators and 100-commit genealogy

1. manifest predicate로 204 occurrence를 재구성한다.
2. 네 partition과 supplemental plan을 서로 다른 identity namespace로 고정한다.
3. first-add/last-touch/final-blob, commit subject, changed path와 actor/process role을 연결한다.
4. v1.0.21 same-relative/common-blob/renamed/split/removed/new 관계를 기록한다.

#### Task 58B — Full reads and PDF pages

1. text 200개, physical 30,219/nonblank 26,137행을 연속 coverage interval로 전문 검독한다.
2. PDF 4개/133쪽을 render하고 page별 시각 attestation을 남긴다.
3. root driver→included section→bibliography→PDF page genealogy를 연결한다.
4. missing, duplicate blob, decode failure, page loss, partition overlap을 fail한다.

#### Task 58C — Process authority and checkpoint

1. plan/self-report/reviewer/candidate/cherry-pick/source/build의 권위 층을 분류한다.
2. Phase 057 96 finding을 source/process rows에 연결하되 status를 승격하지 않는다.
3. result-first, deterministic builder, named negative controls와 exact-eight Git checkpoint를 통과한다.

### Step 59 — Equation and Material Rederivation

#### Task 59A — Thermodynamic/statistical-mechanical layers

1. independent-site grand partition, explicit logistic, susceptibility와 fluctuation identity를 재유도한다.
2. regular-solution free energy, implicit mean-field response, spinodal/binodal/Maxwell과 metastability를 분리한다.
3. equilibrium peak, observation convolution, empirical line shape와 finite-current memory를 별도 operator로 둔다.
4. TST partition ratio, prefactor, activation enthalpy/entropy와 temperature derivative를 재유도한다.

#### Task 59B — Graphite/LCO/Si/blend material equations

1. terminal/electrode/host potential, lithiation direction과 composition coordinates를 공통 sign ledger로 검산한다.
2. common-potential blend charge balance, unique-root 조건과 host-specific capacity sum을 재유도한다.
3. `m_Si` mass fraction→active/capacity fraction 변환을 Faraday/capacity basis로 검산한다.
4. Larché–Cahn stress–potential shift의 sign/dimension을 유도하고 path-history/plastic closure의 부재를 명시한다.
5. LCO local electronic/ordering/free-energy closure와 frozen global offset의 차이를 식으로 판정한다.

#### Task 59C — Finite-current and thermal checks

1. C-rate `h^-1`→`s^-1` 변환과 lag scale 3,600배, `RT ln 3600` barrier shift를 독립 계산한다.
2. arbitrary cut/cap/frozen-local approximation과 full local kinetics를 분리한다.
3. configurational/vibrational/electronic entropy, reversible heat, hysteretic dissipation과 temperature-dependent width를 분리한다.
4. symbolic, finite-difference, dimensional, limiting-case, mutation controls를 통과한다.

### Step 60 — Literature, Quantity and Scope Authority

#### Task 60A — Bibliography and claim inventory

1. final release와 process/candidate에 나타나는 bibliography keys, DOI/metadata claims, equation/numeric/material claims를 전수 inventory한다.
2. exact source span, bibliography identity, source tier와 current authority ceiling을 연결한다.
3. duplicate key, conflicting metadata, missing cited key와 uncited bibliography를 분리한다.

#### Task 60B — Evidence tiers

각 claim의 다음 축을 분리한다.

- bibliographic existence;
- full-text method;
- exact equation;
- exact numerical value and unit/basis;
- sample/material/composition/protocol;
- mapping to current model;
- external experimental support.

원문을 확보하지 못하면 `UNVERIFIED_EXTERNAL` 또는 `GROUND_NOT_FOUND`로 남기고 DOI/abstract로 채우지 않는다.

#### Task 60C — Material scope

1. pristine LCO와 doped high-voltage LCO, dopant/site/charge compensation/voltage window를 분리한다.
2. elemental Si, amorphous/crystalline Si, SiO_x, Si–C, graphite–Si blend와 formation/cycle state를 분리한다.
3. charge-order values, Si capacity, ICE, entropy coefficient, average potential와 demo transition parameters를 Faraday-law/units/source basis로 재검산한다.
4. primary-literature truth는 Phase 071 owner 전까지 승격하지 않는다.

### Step 61 — Code, Runtime and Concordance Delta

#### Task 61A — Static code identity and theory concordance

1. v1.0.21/v1.0.22/v1.0.23 Python/test/guide endpoints, AST, defaults, guards, unsupported paths를 비교한다.
2. theory equation/assumption ID와 actual code path를 연결한다.
3. `BlendedAnodeDQDV`, `from_wt`, background ownership, `f_Si=0`, GS-1/GS-2와 demo sets를 exact static evidence로 판정한다.
4. source import는 하지 않고 AST/static analysis와 isolated copied runtime만 사용한다.

#### Task 61B — Isolated runtime behavior

1. official gates와 independent probes를 disposable external directory에서 실행한다.
2. `f_Si=0` bit-exact, background-subtracted capacity, mass/capacity conversion, continuity, root solver와 error paths를 검증한다.
3. missing parameters/unsupported cases가 warning+placeholder로 진행하는지 fail-closed인지 직접 관찰한다.
4. SI time-unit correction probe와 current-partition limitation을 별도 판정한다.

#### Task 61C — Authority boundary and checkpoint

- static/bit-exact/internal runtime PASS를 scientific/material/experimental PASS로 승격하지 않는다.
- exact output delta, deterministic rebuild, negative controls와 atomic checkpoint를 수행한다.

### Step 62 — Review, Adoption, Build and State Closure

#### Task 62A — Proposal→decision→source adoption

1. 125 competing/reviewer/candidate records를 proposal family로 묶되 원 occurrence를 보존한다.
2. reviewer finding, H/M/L triage, cherry-pick decision, actual source patch와 rejection/skip/defer를 연결한다.
3. 96 Phase 057 finding 각각의 current source state를 `RESOLVED_IN_V1022`, `OPEN`, `SUPERSEDED`, `HISTORICAL_ONLY`, `UNVERIFIED`로 판정한다.
4. proposed LaTeX가 final source에 없으면 adoption을 만들지 않는다.

#### Task 62B — Build/page genealogy

1. 네 driver를 clean three-pass build하고 expected page counts와 current frozen PDF를 비교한다.
2. undefined refs/citations, multiply-defined labels, missing glyphs와 forbidden code mentions를 검사한다.
3. physics manuscript 영역과 implementation appendix/guide 영역의 code-mention boundary를 기록한다.

#### Task 62C — State-document conflicts

1. change log, execution/reference ledgers, index, handover, merge readiness의 as-of chronology를 재구성한다.
2. completed C-055/C-056이 stale pending으로 재등장한 경우를 충돌로 기록한다.
3. self-report와 source/commit/build evidence가 다르면 source chronology를 우선하고 self-report는 superseded로 남긴다.

### Step 63.1 — Source Disposition and Carry-forward Delta

1. 204 manifest occurrences와 supplemental 1을 각각 정확히 한 source disposition으로 판정한다.
2. disposition vocabulary는 `CORRECT`, `PRESERVE`, `SUPERSEDE`, `DISCARD`, `EMPIRICAL_ONLY`, `THEORY_ONLY`, `UNVERIFIED`를 사용한다.
3. 96 Phase 057 findings와 Phase 062 carry/debt/open findings를 lossless routing한다.
4. new blocker는 canonical owner 중복 검사를 통과한 경우만 생성한다.
5. 각 OPEN에는 exact evidence, owner, acceptance criterion, target phase와 non-double-count basis를 둔다.
6. external truth promotion count는 0이어야 한다.

### Step 63.2 — Integrated Validation, Lineage Report F and Final Gate

1. activation과 Steps 58–63.1 machine artifacts를 strict parse/full traversal한다.
2. historical staged/persistence validators를 exact commit context에서 fresh replay한다.
3. source/read/page/commit/equation/literature/code/runtime/adoption/build/disposition/carry denominators를 독립 재계산한다.
4. Lineage Report F, Gate Result, Phase Result와 integrated validation JSON을 result-first/JSON-last로 작성한다.
5. `PASS_P063_LINEAGE_F`, `CONDITIONAL_P063`, `FAIL_P063` 중 하나만 선택한다.
6. exact-eight commit/push/persistence 후에만 Phase 064 detailed plan을 저장한다.

## Phase Gate

### `PASS_P063_LINEAGE_F`

다음이 모두 충족될 때만 선택한다.

- 204 manifest + supplemental 1의 identity/partition/read/page coverage가 완전하다.
- 100-commit process genealogy와 proposal→decision→source/build edge가 손실 없이 재구성됐다.
- 핵심 수식·단위·부호·극한이 독립 재유도되고 known conflicts가 정확히 disposition됐다.
- literature/quantity/material scope의 authority ceiling과 GNF/UNVERIFIED가 유지된다.
- code/runtime/internal build evidence와 scientific/material/experimental truth가 분리된다.
- 96 provisional findings와 inherited carry/debt가 orphan/duplicate 없이 routing된다.
- protected/main/Claude invariants와 exact checkpoint persistence가 통과한다.

이 PASS는 internal lineage-audit completeness만 뜻한다. External scientific/material/experimental/primary-literature truth, canonical selection, defect repair, parameter identifiability, held-out fitting, final equation freeze, final LaTeX/PDF 또는 publication readiness를 뜻하지 않는다.

### `CONDITIONAL_P063`

release/source coverage와 핵심 내부 재유도는 유지되지만 noncritical process/adoption/build/routing evidence가 회수 가능하게 불완전할 때 선택한다. 누락 identity, owner, exact recovery criterion과 downstream block을 명시한다.

### `FAIL_P063`

manifest/read/page/commit identity 붕괴, invalid derivation, denominator fusion, authority promotion, lossy routing, protected drift, unrecoverable validator failure 또는 incomplete remote checkpoint가 있으면 선택한다.

## Implementation Interfaces

### Source topology row

```json
{
  "source_id": "P063-SRC-####",
  "path": "Claude/docs/v1.0.22/...",
  "blob_sha1": "40-hex",
  "sha256": "64-hex",
  "manifest_index": 540,
  "partition": "FINAL_RELEASE_SURFACE|VERSION_PLAN|STATUS_MACHINE_PROCESS|COMPETING_REVIEW_CANDIDATE",
  "review_mode": "FULL_TEXT|FULL_PDF",
  "extent": {"bytes": 0, "lines": 0, "nonblank_lines": 0, "pages": 0},
  "first_add_commit": "40-hex",
  "last_touch_commit": "40-hex",
  "authority_ceiling": "..."
}
```

### Finding/adoption row

```json
{
  "finding_id": "INTENT-PROV-####|P063-FIND-####",
  "proposal_sources": ["P063-SRC-####"],
  "decision_sources": ["P063-SRC-####"],
  "final_source_edges": ["P063-SRC-####"],
  "build_page_edges": [],
  "state": "RESOLVED_IN_V1022|OPEN|SUPERSEDED|HISTORICAL_ONLY|UNVERIFIED",
  "external_truth": false,
  "owner": "...",
  "acceptance_criterion": "..."
}
```

### Equation/material row

```json
{
  "equation_id": "P063-EQ-####",
  "source_span": {"source_id": "P063-SRC-####", "start_line": 1, "end_line": 2},
  "model_layer": "IDEAL|MEAN_FIELD|TWO_PHASE|KINETIC|MECHANICAL|THERMAL|OBSERVATION",
  "independent_derivation": "PASS|FAIL|CONDITIONAL",
  "dimensions": "PASS|FAIL",
  "sign_convention": "PASS|FAIL|NOT_APPLICABLE",
  "limits": [],
  "material_scope": [],
  "authority_ceiling": "INTERNAL_DERIVATION_ONLY",
  "findings": []
}
```

### Literature claim row

```json
{
  "claim_id": "P063-LIT-####",
  "source_span": {"source_id": "P063-SRC-####", "start_line": 1, "end_line": 2},
  "bibliography_key": "...",
  "metadata_state": "CONFIRMED|CONFLICTING|UNVERIFIED|GROUND_NOT_FOUND",
  "fulltext_method_state": "CONFIRMED|UNVERIFIED|GROUND_NOT_FOUND",
  "equation_state": "CONFIRMED|UNVERIFIED|NOT_APPLICABLE",
  "quantity_state": "CONFIRMED|CONFLICTING|UNVERIFIED|NOT_APPLICABLE",
  "material_protocol_scope": [],
  "external_truth_promoted": false,
  "downstream_owner": "Phase 071"
}
```

### Code/runtime row

```json
{
  "endpoint_id": "P063-CODE-####",
  "path": "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py",
  "symbol": "...",
  "ast_identity": "...",
  "theory_equation_ids": [],
  "runtime_probe_ids": [],
  "unsupported_paths": [],
  "authority": "STATIC_ONLY|ISOLATED_RUNTIME|INTERNAL_REGRESSION",
  "external_science": false
}
```

### Disposition row

```json
{
  "disposition_id": "P063-DISP-####",
  "source_id": "P063-SRC-####",
  "disposition": "CORRECT|PRESERVE|SUPERSEDE|DISCARD|EMPIRICAL_ONLY|THEORY_ONLY|UNVERIFIED",
  "status": "OPEN|PRESERVED_ACTIVE|RESOLVED_INFORMATIONAL",
  "reason": "...",
  "evidence_routes": [],
  "carry_forward_links": [],
  "primary_target_phase": 64,
  "acceptance_criterion": "...",
  "authority_ceiling": "..."
}
```

## Test and Validation Plan

### Plan, numbering and recovery

- master→detailed plan→latest result→both ledgers→handover chain이 복구 가능한지 확인한다.
- Step 번호가 58부터 누적되고 63.1/63.2 뒤 Phase 064로 넘어가는지 확인한다.
- 각 recovery boundary에서 읽은 path와 line interval을 result에 기록한다.

### Source/process/read coverage

- manifest hash, 204/204 path/blob, bytes 4,974,148을 독립 계산한다.
- partitions `63/6/10/125`, text 200, physical/nonblank `30,219/26,137`, PDF `4/133`을 검증한다.
- supplemental plan `1`, blob/bytes/lines `f50de.../16,115/99/79`를 별도 검증한다.
- 100-commit genealogy, same-relative `42=5+37`, new/removed `162/26`을 검증한다.
- Phase 057 P–Z 11 docs, 96 findings와 `0096–0191` 연속 ID를 검증한다.

### Equation and material science

- ideal/mean-field/two-phase model-layer mutation을 각각 고유 diagnostic으로 거부한다.
- TST high-temperature prefactor와 entropy derivative, C-rate 3,600 factor와 barrier shift를 독립 수치 재계산한다.
- common-potential unique-root, mass→capacity fraction, background accounting, Larché–Cahn units/sign과 material scope를 검산한다.
- external scientific/material authority promotion을 fail한다.

### Literature and quantity authority

- duplicate/missing citekey, metadata/equation/quantity tier collapse, abstract→fulltext promotion, pristine→doped promotion을 negative fixture로 거부한다.
- charge-order value, Si capacity, SiO_x placeholder와 entropy coefficient의 unit/basis/scope tampering을 검출한다.
- GNF에는 exact search/source context와 owner가 있어야 한다.

### Code/runtime and review/adoption

- source import 금지, AST allowlist, isolated runtime와 cleanup을 검증한다.
- `f_Si=0`, conversion, background, continuity, unsupported/error paths와 time-unit mutation을 검증한다.
- proposal-only, reviewer-only, cherry-pick-only, source-only, build-only edge를 서로 바꾸는 mutation을 거부한다.
- stale state document를 current truth로 승격하는 mutation을 거부한다.

### Negative validation

각 validator는 named controls를 singleton diagnostic으로 거부한다. 최소 공격군:

- duplicate/nonfinite/truncated JSON;
- missing/duplicate source identity;
- partition overlap or denominator fusion;
- partial read or lost PDF page;
- commit/path/blob genealogy tamper;
- model-layer, sign, unit, limit, coordinate and fraction-basis tamper;
- DOI/metadata authority promotion;
- code/runtime/build→external truth promotion;
- proposal→adoption fabrication;
- carry orphan, duplicate owner or premature resolution;
- protected/main/Claude drift;
- staged allowlist, subject, parent or remote mismatch.

### Determinism and Git persistence

- builder projections 2회 byte-identical.
- environment-dependent raw values는 별도 attestation에 두고 semantic projection에서 제외한다.
- exact staged set, index/worktree equality, no unstaged/untracked extras, `git diff --check`를 검사한다.
- commit 후 local/upstream/tracking/live-origin, exact parent/subject/paths/blob bytes와 clean status를 검증한다.
- full commit hash를 추정하지 않고 Git에서 직접 resolve한다.

## Stop Conditions

다음 중 하나라도 발생하면 현재 Step을 commit하지 않고 result에 정확한 blocker를 기록한다.

1. manifest predicate나 baseline hash가 불일치한다.
2. 204 occurrence 또는 supplemental 1의 identity를 재현할 수 없다.
3. text 1–EOF 또는 PDF 1–last-page coverage에 빈 구간이 있다.
4. output truncation/encoding 오류 뒤 재독으로 회복하지 못한다.
5. proposal/decision/source/build edge가 모호한데 채택을 추정해야 한다.
6. 수식의 sign/unit/limit/model layer가 독립 재유도에 실패한다.
7. literature full text 없이 load-bearing equation/quantity를 승인해야 한다.
8. runtime이 active source를 import하거나 production behavior를 변경해야 한다.
9. protected branch, main 또는 `Claude/**` 변경이 필요하다.
10. declared exact path 외 변경이 존재한다.
11. negative control이 escape하거나 deterministic rebuild가 불일치한다.
12. push 또는 live remote verification을 완료할 수 없다.

회수 가능한 external-source 부족은 곧바로 전역 FAIL로 만들지 않는다. 해당 claim을 `UNVERIFIED_EXTERNAL`/`GROUND_NOT_FOUND`와 owner/acceptance로 보존하고 Phase Gate 권위 범위를 제한한다.

## Assumptions

- frozen baseline과 manifest가 Phase 056에서 고정한 source universe다.
- Git object database와 GitHub origin은 Phase 063 실행 동안 읽기 가능하다.
- Python 3.12는 historical validator/runtime 기준이며, 다른 Python은 portability 보조 증거다.
- PDF 렌더/LaTeX 도구가 없으면 source coverage와 PDF raw/page attestation을 분리하고 missing tool을 숨기지 않는다.
- 외부 웹/논문 접근이 없으면 기존 metadata를 external truth로 승격하지 않는다.
- 향후 Phase 071–089가 literature/data/canonical theory/code/final PDF authority를 각각 소유한다.

## Correction History

- 2026-08-28: Phase 062 `PASS_P062_LINEAGE_E`와 Step 57.2 persistence 뒤 최초 작성.
- Phase 057 P–Z 11문건, 101 source documents/16,855 lines와 96 provisional findings를 전문 재독해 v1.0.22 특화 scope를 구성했다.
- Phase 056 manifest에서 v1.0.22 204 occurrence와 `63/6/10/125` partitions, text/PDF/line/page/byte denominators를 독립 재계산했다.
- Supplemental master plan은 release denominator와 분리하고 D22/R0–R9 process authority로만 유지했다.
- 사용자 요구에 따라 계획서는 `Codex/plans`, results/ledger/handover는 `Codex/results`, work scripts는 `Codex/work/v1022_phase063`에 둔다.
