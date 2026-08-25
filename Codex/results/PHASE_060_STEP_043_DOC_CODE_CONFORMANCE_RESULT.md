# Phase 060 Step 43 문서 주도 구현 추적 결과

정본일: 2026-08-26

Phase: 060 — v1.0.19 계보 재감사

Step: 43

상태: `PASS_WITH_CONCERNS`

Gate: `PASS_P060_STEP43_DOC_CODE_CONFORMANCE`

과학 권위: `DEFERRED_TO_STEP44_AND_PHASE071`

## 1. 목적과 판정 범위

이 Step은 v1.0.19 문건의 핵심 이론·수식·부호·단위 명제를 출발점으로 삼아, 동결된 구현의 실제 정의, 호출 사슬, source gate, 저장 artifact 소비 경로까지 역추적했다. 판정은 다음 네 층위를 분리한다.

1. 문서 앵커: frozen TeX의 어휘·수식 위치를 증명한다.
2. 구현 앵커: frozen Python source가 실제로 계산하는 경로를 증명한다.
3. 시험 앵커: source에 존재하는 gate와 그 강도만 증명한다. 네 파일의 Python `assert` 문은 0개다.
4. artifact 앵커: PDF, 그림, NPZ가 존재하고 Step 42에서 재생성·대조된 내부 witness임을 증명한다.

따라서 이 Step의 `ALIGNED` 또는 gate `PASS`는 문헌 진실성, 독립 물리 타당성, 실험 재현성, 재료 일반성 또는 primary-reference 권위를 뜻하지 않는다. 그 권위는 Step 44와 Phase 071에 남아 있다.

## 2. 복구 지점과 입력

본격 작업 전 다음 복구 정본을 직접 재독했다.

- `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md` 1–665.
- `Codex/plans/2026-08-25-phase060-v1019-lineage-detailed-plan.md` 1–831.
- `Codex/results/PHASE_060_STEP_042_RUNTIME_ARTIFACT_RESULT.md` 1–273.
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md` 1–206.
- `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md` 1–48.
- `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md` 1–88.

입력 machine evidence의 SHA-256은 다음과 같다.

| 입력 | SHA-256 |
|---|---|
| `PHASE_060_V1019_SOURCE_TOPOLOGY.json` | `c246a05e2d13d1d33dab1682bda712611367412d241cd277694a35aaf7bcf140` |
| `PHASE_060_V1019_TEX_READ_ATTESTATION.json` | `36616b86f934b7c594e68e1b991c261c7b391b70e2c4c52375d452b3d69a06ad` |
| `PHASE_060_V1019_PROCESS_INTENT_MATRIX.json` | `d61e514712a91b7eea89e723cf33745b00a20ee59387abcb450db778122174f7` |
| `PHASE_060_V1019_CODE_TEST_RUNTIME_MATRIX.json` | `4f38d3678870c32b1910701e62506547f2bc471684ceb0578775ba29fb57e2af` |
| `PHASE_060_V1019_ARTIFACT_AUDIT.json` | `9fc8d1f4bd797c394effe5d72771cca0a3d4b6426e53c3a2d95d0f9f5e446bcf` |

동결 source commit은 `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`다.

## 3. TDD RED

builder 작성 전에 validator를 먼저 만들고 artifact가 없는 상태에서 실행했다.

```text
FAIL missing_artifact: Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json
FAIL_P060_STEP43_DOC_CODE_CONFORMANCE 0/1
```

이 실패는 요구된 artifact 부재를 정확히 차단한 의도된 RED다.

독립 사전 커밋 검독은 최초 GREEN 후보를 `NO_GO`로 판정했다. 당시 validator가 flat edge ID의 존재만 검사해 ordered/contiguous call path를 증명하지 못했고, 단위·부호 evidence가 행별 경계 대신 일반 문구였으며, 28개 행과 29개 optional record의 분모 표현이 과도했다. 보강 validator를 기존 schema v1 artifact에 먼저 적용한 두 번째 RED는 다음과 같다.

```text
FAIL schema.top_keys
FAIL schema.version
FAIL determinism.committed_artifact
FAIL_P060_STEP43_DOC_CODE_CONFORMANCE 8598/8601
```

이후 schema v2는 각 DIRECT 행에 복수 대안 경로를 분리한 ordered/contiguous local 또는 dynamic-dispatch call path, 모든 edge endpoint의 definition anchor, DIRECT 행의 모든 non-class implementation definition이 실제 path에 참여한다는 gate, strong assertion과 weak/print gate 분리, 행별 단위·부호 문장과 exact anchor, 조건부 reachability, artifact generator/consumer source anchor를 요구하도록 보강했다. validator는 frozen source에서 정의와 882개 AST call의 caller/callee/line/column/ordinal/AST hash, LCO 상속 관계를 독립 재생성한다.

같은 독립 검독에서 non-class implementation anchor relevance와 public-entry semantic join을 추가로 요구했다. 강화 validator를 직전 artifact에 적용해 다음 RED를 각각 재현했다.

```text
FAIL trace.unused_impl_anchor:TRC-CH1-LAG-LENGTH
FAIL trace.unused_impl_anchor:TRC-CH1-LCO-DIRECTION-CENTER
FAIL trace.unused_impl_anchor:TRC-CH2-WIDTH-T-DEPENDENCE
FAIL trace.unused_impl_anchor:TRC-CH2-REVERSIBLE-HEAT
FAIL_P060_STEP43_DOC_CODE_CONFORMANCE 11706/11710
```

```text
FAIL public.trace_join:GraphiteAnodeDischargeDQDV:TRC-CH1-CHARGE-BALANCE
FAIL public.trace_join:GraphiteAnodeDischargeDQDV:TRC-CH2-COMPLETE-SYNTHESIS
FAIL public.trace_join:GraphiteAnodeDischargeDQDV.equilibrium:TRC-CH1-LCO-PEAK
FAIL public.trace_join:GraphiteAnodeDischargeDQDV.irreversible_heat:TRC-CH2-REVERSIBLE-HEAT
FAIL determinism.committed_artifact
FAIL_P060_STEP43_DOC_CODE_CONFORMANCE 11799/11804
```

최종 보강은 관련 경로를 추가하거나 stale public mapping을 제거했고, 모든 production public `trace_ids`가 존재하며 해당 public definition을 trace implementation anchor에 실제 포함하는지 검증한다. 기본 `chi_split=func_chi_d`와 `self.chi_split=chi_split`도 frozen `__init__` AST에서 독립 재구성한다.

## 4. 문서 검독 범위

직접 전문 검독한 핵심 문서는 다음과 같다.

- Chapter 1: `ch1_sec01_n0n1.tex`, `ch1_sec03_center.tex`, `ch1_sec04_hys.tex`, `ch1_sec05_width.tex`, `ch1_sec06_eqpeak.tex`, `ch1_sec07_broadening.tex`, `ch1_sec08_lag.tex`, `ch1_sec09_tail.tex`, `ch1_sec10_sum.tex`, `ch1_sec11_lcointro.tex`, `ch1_sec12_lcocenter.tex`, `ch1_sec13_lcohys.tex`, `ch1_sec14_lcodecomp.tex`, `ch1_sec15_lcoelec.tex`, `ch1_sec16_lcopeak.tex`, `ch1_sec17_msmr.tex`, `ch1_sec18_inputs.tex`, `ch1_appA_signcheck.tex`, `ch1_appB_codemap.tex`.
- Chapter 2: `ch2_sec01_partition.tex`–`ch2_sec08_synthesis.tex`, `ch2_appB_codemap.tex`.
- 문서측 분담 검독은 Step 40 topology JSON 31,953행을 strict parse하고 값 노드 28,852개와 key 노드 25,819개를 전수 순회했다. Ch2 핵심 10개 파일과 양 장 코드맵·함정 부록을 전문 검독했다.

Step 40의 비구조 lexical candidate 분모는 정확히 914개다.

```text
DISPLAYED_EQUATION                  188
DEFINITION_CANDIDATE                 89
ASSUMPTION_CANDIDATE                 51
SIGN_UNIT_DECLARATION_CANDIDATE     229
CODE_MENTION_CANDIDATE              255
FORWARD_REFERENCE_CANDIDATE         102
합계                                914
```

914개는 모두 `OVERLAPS_CURATED_OBLIGATION_ANCHOR` 또는 `SUPPORTING_OR_OUTSIDE_STEP43_CURATED_SCOPE`로 처분했다. 376개 overlap은 넓은 행 범위가 28개 curated obligation과 교차한다는 뜻이며, 독립적으로 “모든 load-bearing claim”을 열거했다는 뜻이 아니다. 이 기계 처분은 Step 43의 14개 필수 family와 curated 28행에 대한 coverage routing이지, 28행 밖에 중요한 문서 명제가 없거나 나머지 문장이 과학적으로 중요하지 않다고 판정한 것이 아니다.

## 5. 구현·시험 전문 검독 범위

다음 Python source를 1행부터 끝까지 직접 또는 분담 전문 검독했다.

| 파일 | 행 범위 |
|---|---:|
| `Anode_Fit_v1.0.19.py` | 1–1,151 |
| `fit_roundtrip_demo.py` | 1–368 |
| `graph_suite_v1019.py` | 1–150 |
| `test_regression_v1019.py` | 1–127 |
| 합계 | 1,796/1,796 |

독립 AST 재생성 결과는 정의 57개, `ast.Call` node 882개, public lexical definition 34개, Python `assert` 0개다.

Step 42의 정의 56개·호출 edge 444개는 함수 정의 본문 범위의 색인이었다. 모듈 실행부와 `Anode_Fit_v1.0.19.py:983-984`의 `_ok` 정의가 빠져 있었다. Step 43은 이를 전체 실행 source의 정의 57개·호출 882개로 교정했으며, Step 42 결과를 소급 변경하지 않고 증거 범위 차이로 보존했다.

## 6. 정본 추적 분모

| 항목 | 분모 | 결과 |
|---|---:|---:|
| lexical candidate 처분 | 914 | 914/914 |
| 필수 focus family | 14 | 14/14 |
| curated document obligation row | 28 | 28/28 |
| 생산 공개 entry | 20 | 20/20 |
| test/demo/graph support entry | 14 | 14/14 명시 제외 |
| 전체 AST 정의 | 57 | 57/57 |
| 전체 AST 호출 | 882 | 882/882 |
| source gate | 46 | 46/46 |
| Python `assert` | 0 | 0 |
| artifact consumer | 17 | 17/17 |
| optional/conditional input disposition group | 29 | 29/29; 고유 member name 45 |
| candidate/curated-row/public orphan | — | 0/0/0 |
| invalid anchor | — | 0 |
| missing authority boundary | — | 0 |

생산 공개 entry 20개는 module function 9개, public class 2개, public method 9개다. 나머지 14개는 fit 8개, graph 1개, regression 5개이며 실행형 script의 lexical helper라 생산 API로 승격하지 않았다.

## 7. Trace 판정 분포

### 관계

- `DIRECT`: 22.
- `RELATED_NOT_DIRECT`: 6.
- `NOT_APPLICABLE`: 0.

### 구현 상태

- `ALIGNED`: 5.
- `PARTIAL`: 18.
- `MISALIGNED`: 1.
- `ABSENT`: 1.
- `UNVERIFIED`: 3.

### 구현 disposition

- `IMPLEMENTED`: 18.
- `PARTIAL`: 9.
- `MISSING`: 1.

## 8. 핵심 확정 판정

### 8.1 정합 또는 bounded 정합

- 반응 중심 `U=(-ΔH+TΔS)/F`, logistic, 명시적 `n`/`n(T)` 폭, 전하보존 음함수, simple/complete/config 분해, `x_bar` 진입점, `q_rev=-IT∂U/∂T`의 실제 호출 경로를 확인했다. 대안·분기 경로는 서로 다른 `call_paths`로 저장했고 flat chain으로 합치지 않았다.
- `x_bar=0.25` worked example, 5-SOC 부호 교대, 유한차분 round trip은 실제 수치 gate에 연결된다.
- `equilibrium`은 `gamma`가 있는 실제 저전류 한계가 아니라 branch를 의도적으로 제외한 별도의 가역 기준선이다.
- `dqdv`의 저전류 경로는 `gamma≠0`이면 branch 중심을 유지한다. 두 의미를 별도 trace로 분리했다. 다만 이 경계의 source gate `MAIN-09`는 print-only이므로 해당 행은 `ALIGNED`가 아니라 `PARTIAL`이다.
- 직접 `L_V`는 동역학 계산을 우회하고, 계산 경로는 `chi_d`, `ΔH_a^eff`, cutoff affinity, `func_L_q`, `|dV/dq|`를 거친다.
- `theta_E`가 있으면 `ΔU_vib`와 `ΔS_vib`가 함께 적용되며, 없으면 0 경로다. 다만 dedicated failing source gate는 없고 Step 42 supplemental probe만 있다.

### 8.2 관련은 있으나 DIRECT가 아닌 항목

- broadening의 ensemble forward 평균과 width budget은 `w`·`L_V` 소비 경로와 관련은 있으나 production 계산기로 구현되지 않았다.
- MSMR 대응은 함수형 동형이며 물리량 동일성이 아니다.
- 분배함수·Bragg–Williams 유도는 구현 logistic·hysteresis helper의 과학적 직접 증명이 아니다.
- LCO full plug-in은 `x_center`와 298.15 K를 동결한 제한 경로만 존재한다.

### 8.3 MISALIGNED 1건

`n`과 `w`가 모두 없으면 `_n_factor`가 `1.0`을 반환해 실제 폭은 `RT/F`로 온도 의존한다. 그러나 `_dwdT`는 같은 default 경로에서 0을 반환해 가역열 config 항은 동결 폭처럼 계산한다. 문건의 `n=1` 기본·`∂w/∂T=R/F` 사슬과 내부 구현이 일치하지 않는다.

### 8.4 ABSENT 1건

문건의 명시적 충·방전 branch별 `∂U/∂T` 평균 경로는 없다. 현 `entropy_coefficient`는 branch shift 없는 평형 중심을 사용해 대칭·선형화 근사를 실현하지만, 유한 hysteresis gap의 branch 평균과 고차 보정을 구현하지 않는다.

## 9. Findings

### P0 — 0

현재 Step 43 범위에서 즉시 중단 또는 source 동결 위반을 요구하는 P0는 없다.

### P1 — 12

1. no-`n`/no-`w`의 thermal width와 `_dwdT=0` 불일치.
2. LCO electronic entropy가 298.15 K에 동결되어 문서의 full T-dependent center curvature 미복원.
3. 명시적 reversible hysteresis branch-average 경로 부재.
4. Ch2 부록 B의 prospective authority와 Ch1 부록 B의 current-description register 충돌 위험.
5. physical low-current hysteresis와 branch-free reversible baseline 혼합 위험.
6. Step 42의 444-edge 범위를 full module execution graph로 읽을 수 있는 evidence-scope 과장.
7. graph suite의 aggregate failing exit gate 부재.
8. module `overall OK`가 출력한 기대의 일부만 결합.
9. regression PASS가 area와 optional-key absence를 제외.
10. fit의 `area conservation` 라벨이 곡선 적분이 아니라 `sum(Q)` 비율만 gate.
11. broadening ensemble forward 평균과 width-budget 계산 경로 부재.
12. `irreversible_heat`가 4-file scope에서 dormant이며 public total-heat composition entry 부재.

### P2 — 13

1. `solve_U_oc`의 `tol`/`max_iter` 미검증과 iteration exhaustion failure 부재.
2. 전이별 `Q_j>0` 미검증.
3. `equilibrium` 입력 V와 callable `Cbg` 출력 finite 검증 부재.
4. low-level helper·transition 입력의 일관된 finite/range guard 부재.
5. fit optimizer fallback의 import 원인·optimizer success 기록 부재.
6. fit plot 실패 warning-only.
7. graph manual simple helper의 vib 항 누락.
8. regression capture의 mutation 경로 격리 필요.
9. Step 42 `SEM-002`의 `chi_split=x` 기록 오류. 실제는 `chi=None→self.x`, `chi_split=func_chi_d`다.
10. Step 42 `SEM-006`의 seed `20250718` 기록 오류. 실제 source는 `20260713`이다.
11. LCO electronic opt-in field의 명시적 schema/range guard 부재.
12. `theta_E_Tref`가 finite만 검사되고 양수는 강제되지 않음.
13. code-map 이름 대응만으로 reachability 또는 과학적 동일성을 확정할 수 없음.

## 10. Optional input 상태

45개 고유 member name을 포괄하는 29개 optional/conditional disposition group을 `accepted`, `validated`, `used`, `ignored`, `overwritten`, `bypassed`, `dormant`, `diagnostic-only`로 분해했다. `seed_T/seed_I/seed_Q_cell`, `Omega/gamma/h_eta`처럼 동일한 수명주기 경계를 공유하는 변수는 한 group이므로 “개별 입력 29개”로 세지 않는다. 특히 다음 경계를 고정했다.

- `n`이 있으면 `w`는 무검증 상태로 무시된다.
- `I_abs`가 있으면 `c_rate`는 검증 없이 무시된다.
- 직접 `L_V`가 있으면 kinetic parameter 경로 전체가 우회된다.
- `seed_L_V`는 eager diagnostic state이며 production `dqdv`에 소비되지 않는다.
- `electronic=True`일 때만 LCO MIT field가 소비되며 호출 T 대신 298.15 K가 사용된다.
- `direction` facade는 LCO cell label을 탈리튬화 부호로 변환하지만 low-level `dqdv(s=...)`는 이를 우회한다.
- 배열 `T(V)`는 중심·폭에 점별 적용되지만 hysteresis branch와 lag는 평균 `T_rep`를 쓴다.

## 11. 생성 산출물

| 파일 | 크기 | 행 | SHA-256 |
|---|---:|---:|---|
| `Codex/work/v1019_phase060/build_phase060_step43_doc_code_trace.py` | 70,454 bytes | 1,150 | `ba384cbb303d76272876653df091f8489b317173be6463032bab828bbdc0cae3` |
| `Codex/work/v1019_phase060/validate_phase060_step43_doc_code_trace.py` | 52,160 bytes | 827 | `a5919840060675d5516d88ce893dca071ee6f331ffb96f624bbb1ef6061de16d` |
| `Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json` | 1,182,261 bytes | 28,424 | `95c89d7536b492d21ccfdee3d6077bcd04f2054805d52bf4f067f70689864ebe` |

machine matrix는 strict JSON으로 parse됐고 duplicate/non-finite를 허용하지 않는다. 재귀 순회는 value node 25,232개, key node 20,629개, 합계 45,861개, 최대 깊이 6을 확인했다. Call path는 local 28개, dynamic-dispatch 5개, 합계 33개이며 DIRECT/non-missing 행의 미사용 non-class implementation definition과 production public semantic-join 오류는 0개다.

## 12. 검증

정상 validator 출력은 다음과 같다.

```text
PASS candidates=914 curated_claims=28 production=20 support=14
PASS definitions=57 calls=882 source_gates=46 ast_asserts=0
PASS orphans candidate=0 curated_doc=0 public=0 focus_missing=0
PASS findings P0=0 P1=12 P2=13 result=PASS_WITH_CONCERNS
PASS determinism=4/4 negative_controls=20/20
PASS_P060_STEP43_DOC_CODE_CONFORMANCE 11815/11815
```

negative control은 다음 20개를 모두 거부했다.

1. 실제 call edge 삭제.
2. `q_rev` 부호 반전.
3. MSMR을 허위 `DIRECT`로 승격.
4. 기본 비활성 LCO hysteresis를 활성으로 위조.
5. source gate `MAIN-12` 삭제.

6. duplicate trace ID.
7. unknown status enum.
8. ordered call path의 edge 순서 교환.
9. call path endpoint definition anchor 삭제.
10. print-only 저전류 행을 `ALIGNED`로 허위 승격.
11. `generation` 임의 key 삽입.
12. `enumerations` 삭제.
13. input evidence 중복 record 삽입.
14. `gate_summary` 임의 key 삽입.
15. exact artifact generator/consumer anchor 삭제.
16. LCO electronic trace를 public entry가 아니라 private override에서 시작하도록 절단.
17. PDF의 `DIRECT_TEX_SOURCE`와 exact TeX anchor를 `GROUND_NOT_FOUND`로 강등.
18. DIRECT 행에 call path가 소비하지 않는 non-class implementation definition 삽입.
19. LCO override 동적 dispatch를 정적 local call로 위조.
20. `irreversible_heat` public entry를 무관한 center trace에 연결.

builder 두 번의 임시 출력과 저장 artifact는 byte-identical이었다. 모든 definition과 call edge는 validator가 frozen AST에서 독립 재생성한 object와 일치했다.

## 13. 변경 경계

- `Claude/` tracked source 변경 0.
- protected Codex branch 변경 0.
- `main` 변경 0.
- source commit 변경 0.
- 외부 문헌·실험·재료 권위 승격 0.
- 코드 수정 또는 결함 수리 0. 본 Step은 감사·routing 범위다.

## 14. Step 43 원자 커밋 계약

Step 43 결과를 포함하는 exact allowlist는 다음 7개다.

1. `Codex/work/v1019_phase060/build_phase060_step43_doc_code_trace.py`
2. `Codex/work/v1019_phase060/validate_phase060_step43_doc_code_trace.py`
3. `Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json`
4. `Codex/results/PHASE_060_STEP_043_DOC_CODE_CONFORMANCE_RESULT.md`
5. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`

계획 subject는 `audit(phase060): trace doc-led implementation`이다. 이 문서는 자기 자신을 포함하는 commit hash를 미리 알 수 없으므로 containing commit hash와 push/remote 검증은 controller의 post-commit 확인 사항이다.

## 15. 다음 단계

Step 43 exact-seven을 원자 commit·push·remote verify한 뒤 Step 44로 간다. Step 44는 이 Step의 구현 정합 판정을 과학 진실로 승격하지 않고, 핵심 식의 독립 재유도, 차원·부호·극한·보존 검산, P1/P2 원인 분리, Step 45에 넘길 blocker를 작성한다.

정확한 다음 Step은 누적 번호 `44`다.
