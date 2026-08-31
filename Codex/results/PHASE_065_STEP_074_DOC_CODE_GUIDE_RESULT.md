# Phase 065 Step 74 — Document, Code and Guide Conformance Result

정본일: 2026-08-31
세부 계획: `Codex/plans/2026-08-30-phase065-v1024-v1024_1-lineage-detailed-plan.md`
누적 Step: 74
예상 parent: `5c5c555462f1dbf0603eedda6a1d5b62684cffdf`
예상 subject: `audit(phase065): adjudicate v1024 doc code guide`
상태: `PASS_P065_STEP74_CONFORMANCE_WITH_CONCERNS`; `PASS_PENDING_PERSISTENCE`

## Summary

Step 74는 동결 v1.0.24/v1.0.24.1의 이론, 결과 기록, Markdown
가이드, 3,812행 HTML 가이드, 시험, 생성 문건을 claim 단위로 코드와
Step 73 실행 증거에 대조했다. 결과는 41개 conformance row다. 이
Gate는 확인한 scope와 exact denominator의 불일치를 분류하고 후속 owner에
연결했다는 뜻이며,
production repair, 외부 과학·재료·실험·proposition truth, 정본 모델
선택 또는 publication readiness를 뜻하지 않는다.

행별 권위는 섞지 않았다.

1. 실행 동작은 Step 73의 격리 runtime과 동결 executable source가
   우선한다.
2. 과학 명제는 원 논문 전문과 독립 수식 유도가 우선하며, 내부 실행
   성공은 이를 대신하지 않는다.
3. 채택·supersession은 Git chronology와 명시적 disposition이
   우선한다.
4. Markdown은 HTML의 authoring source다. HTML/PDF/image 반복은
   독립 근거를 늘리지 않는다.

## Scope and Non-goals

### 포함

- Step 70에서 Step 74로 route된 13개 finding.
- Step 71에서 Step 74로 route된 2개 finding.
- Step 72에서 Step 74로 route된 2개 finding.
- Step 73에서 runtime으로 분리된 regsol, root, `/3600`, width,
  LCO toggle, profile, fallback, explicit-zero, alias, unsupported 경계.
- HTML authored wrapper 1–219, embedded Mermaid vendor payload 220–3807,
  initialization/footer 3808–3812.
- visible scientific main text의 implementation name/history 후보.

### 제외

- `Claude/**` 수정.
- production 코드·가이드·그림의 실제 repair.
- 특정 식 또는 model family의 정본 채택.
- 외부 문헌 truth의 신규 취득·승격.
- 실제 데이터 calibration 또는 publication claim.

## Recovery and Read Coverage

### Controller `DIRECT_READ`

- `Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`: 1–520.
- `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`: 1–665.
- `Codex/plans/2026-08-30-phase065-v1024-v1024_1-lineage-detailed-plan.md`: 1–851.
- `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`: 1–56.
- `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`: 1–138.
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`: 1–395.
- `Codex/results/PHASE_065_STEP_073_INITIALIZATION_RUNTIME_RESULT.md`: 1–213.
- `Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md`: 1–1720.
- `Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md`: 1–472.
- `Codex/results/PHASE_057AN_V1024_CODE_GUIDE_OBSERVATIONS.md`: 1–169.
- `Codex/results/PHASE_057AX_V1024_HTML_GUIDE_OBSERVATIONS.md`: 1–189.
- frozen `Claude/results/comp_v24/INV_code_in_body.md`: 1–39.
- frozen `PHASE_R2_RESULT.md`: 1–49 and `PHASE_R3_RESULT.md`: 1–39.

### Independent `AGENT_FULL_READ`

- Step 70 result 1–1720, topology JSON full traversal, read-attestation JSON
  full traversal.
- frozen `Claude/results/comp_v24/*.png` 33개 blob을 모두 decode하고 original
  image visual pass를 수행했다. missing-glyph box는 15개 exact path에서 직접
  관찰했으며 inherited count 17의 나머지 2개 identity는 찾지 못했다.
- frozen HTML 3,594,138 bytes, 3,812 physical lines: authored 1–219,
  vendor 220–3807, footer 3808–3812.
- frozen Markdown code guide 1–374 and fitting guide 1–137.
- Step 71 result 1–1031 and Step 73 result 1–213.
- Step 71 matrix/attestation and Step 73 route/runtime JSON strict parse and
  full recursive traversal.
- frozen reflect/self-consistent tests 1–EOF and claim-bearing main gate,
  source, result and TeX ranges bound in the matrix.
- frozen Step 72 theory/material result and the selected LCO, Si,
  rejected-candidate and main-body implementation surfaces bound in the matrix.

Mirror paths reuse the same verified blob read but keep both occurrence
identities. 읽지 않은 범위를 추론으로 메우지 않았다. 외부 Ref. 7
proposition support는 `GROUND_NOT_FOUND`로 유지한다.

## Exact Denominators

| Denominator | Count | Rule |
|---|---:|---|
| Conformance rows | 41 | `D74-001`–`D74-041`, 단조·중복 없음 |
| Step 70 input routes | 13 | F06/F08/F10/F11/F14/F34/F35/F36/F39/F41/F42/F43/F44 |
| Step 71 input routes | 2 | F01/F06 |
| Step 72 input routes | 2 | F02/F05 |
| Total exact prior routes | 17 | 원 `origin_record` 보존 |
| Source bindings | 56 | frozen Git blob 또는 expected-parent artifact |
| HTML physical lines | 3,812 | 219 authored + 3,588 vendor + 5 footer |
| HTML damaged table rows | 3 | physical 142, 166, 214 |
| no-final-LF Markdown | 2 | exact paths fixed below |

## Confirmed Conformance Boundaries

### 1. Regular-solution route

- `CODE_GUIDE_v24.md:200–218`의 equilibrium-only disclosure는 실제
  source/runtime과 맞는다.
- `REFLECT_SEED_TABLE.md:14`의 equilibrium과 derivative 모두 분기한다는
  주장은 틀린다. `equilibrium()`만 `kernel == 'regsol'`을 보고,
  `dqdv`, entropy, `solve_U_oc`는 logistic이다.
- guide의 blanket “문건 식 그대로 구현” 표현은 route-specific matrix로
  대체해야 한다.
- Si의 `w=nRT/F`와 direct regular-solution denominator 조합은 n-generalized
  denominator/critical condition이 유도되지 않았다.
- LCO per-peak Omega prose는 named `LCO_MSMR_LIT` executable route가 아니다.

### 2. Defaults, initialization and unsupported paths

- final v1.0.24 source와 current Markdown guide의 LCO electronic entropy
  default는 `False`다. Step 73에서 default/False/0/None OFF와 explicit ON을
  분리 확인했다.
- `PHASE_R2_RESULT`의 default ON, `PHASE_R3_RESULT` 내부의 OFF/True 혼재는
  current truth가 아니라 supersession이 필요한 historical self-report다.
- XRD profile의 Omega만으로 regsol이 활성화되지 않는다.
- MSMR6은 direct explicit injection만 확인됐으며 자동 endpoint 선택은
  확인되지 않았다.
- legacy/current saved-state schema, restore loader와 key는
  `ABSENT_IN_FROZEN_SOURCE`다. absence corroboration은 behavior PASS가 아니다.
- plastic hysteresis와 nonadditive correction은 명시적 unsupported stub다.

### 3. Root, unit, width and blend

- guide의 `solve_U_oc` “유일근” 표현은 수학적 조건과 구현 convergence를
  구분하지 않는다. source는 `max_iter` 소진 후 midpoint를 조용히 반환한다.
- R4 “unit contract” 시험은 finite/positive와 값 불변만 확인한다.
  executable path에는 `/3600` migration이 없다.
- no-n/no-w와 `n_T1=None`은 width value와 derivative가 서로 다른 fallback/
  exception 경로를 가진다.
- R6-G3 capacity conservation은 equilibrium area만 검사한다. finite-rate
  blend는 두 host에 동일한 full `I_abs`와 external `Q_cell`을 전달하므로
  current partition/denominator closure를 증명하지 않는다.

### 4. Tests and aggregate records

- reflect “single peak” predicate는 실제로 local maximum count `>=1`을
  허용한다. exact-one 증거가 아니다.
- self-consistent fixed point는 같은 구현을 반복한 내부 회귀이며 독립
  physical truth가 아니다.
- `MERGE_READINESS_v24`의 BUG0/MERGE-READY와 `HANDOVER_v24`의 전면 정합은
  위 exact contradictions 때문에 current aggregate truth로 유지할 수 없다.

## Generated and Copied Artifacts

### HTML

- HTML raw SHA-256:
  `c795a947a44b31eb4d0039e67d067a96d51d807e9a3de9fda799534180908aa1`.
- 220–3807 vendor bundle은 project scientific semantics를 추가하지 않는다.
- exact generator command, renderer version/hash는 `GROUND_NOT_FOUND`다.
- Markdown source의 `\|I\|`는 올바르지만 generated HTML은 다음처럼
  손상됐다.

| HTML line | Intended source | Expected / actual cells |
|---:|---|---:|
| 142 | Markdown 176 `equilibrium` | 3 / 5 |
| 166 | Markdown 228 `Rn` | 3 / 5 |
| 214 | Markdown 350 `V_n` | 4 / 6 |

### PDF and v1.0.24.1

- PDF는 TeX closure의 generated artifact이며 존재 자체가 source/runtime/
  primary-literature truth를 늘리지 않는다.
- v1.0.24.1은 130개 byte-identical mirror pair와 archive note 하나다.
  archive-only wording은 경계로서 맞지만 independent corroboration은 아니다.

### Images and exact-output defects

- Step 70의 missing-glyph count 17에 대해 33개 PNG를 fresh decode/visual
  inspection한 결과 직접 관찰된 exact numerator는 15다:
  `bdd_vs_savgol.png`, `cathode_fit.png`, `consistency.png`,
  `gr_4vs6_transitions.png`, `gr_angular_diag.png`, `gr_sym_vs_asym.png`,
  `model_vs_data.png`, `new_materials.png`, `param_distributions.png`,
  `quality_vs_r2.png`, `rate_broadening.png`, `rate_quant.png`,
  `regsol_proto.png`, `temperature_entropy.png`, `wavelet_denoise_check.png`.
  inherited 17의 나머지 2개 identity는 `GROUND_NOT_FOUND`이며 15를 17로
  조용히 맞추지 않는다.
- exact named visual defects:
  `gr_dva_Mremoval.png`, `lco_phase.png`, `param_distributions.png`,
  `quality_vs_r2.png`.
- no-final-LF exact paths:
  `Claude/results/comp_v24/fit_registry.md`와
  `Claude/results/comp_v24/param_dist_stats.md`.

## Units, Version and Reproduction Findings

- `v24_graphite_firstlook.py:12,72`: capacity를 mAh라고 표시한 뒤 1,000을
  다시 곱해 같은 label을 유지한다.
- `v24_rate_broadening.py:67–70`: V/mA slope를 1,000배 해 Ω로 환산한 뒤
  `Ω/mA`로 표시한다. coherent derived unit가 아니다.
- `FITTING_GUIDE.md:1,3,5`는 v1.0.24 surface에서 v1.0.20과
  `Anode_Fit_v1.0.20.py`를 current target처럼 적는다.
- 같은 guide의 v1.0.19 suite는 v1.0.24 self-contained reproduction command가
  아니다.
- historical absolute paths는 provenance이지 portable execution command가
  아니다.

## Scientific and Adoption Findings

- `VALIDATION_SYNTHESIS.md:15,24`의 “첫 실피팅”은 analytic PyBaMM LCO
  proxy다. LCO-specific measured raw data가 없으므로 real-data fit 또는
  experimental validation으로 부를 수 없다.
- rejected W1의 `fergusonbazant2014`, `guo2016` undefined keys는 formal
  non-graft decision 때문에 adopted closure blocker가 아니다.
- Ref. 7 proposition/page/equation support는 이 Step에서 취득되지 않았다.
  DOI/metadata나 repository self-report로 보충하지 않는다.
- graphite regular-solution helper의 모든 `Omega >= 2.02 RT` bound 뒤
  `Omega > 2 RT` 결과를 phase confirmation으로 승격할 수 없다. 이는
  bound-constrained in-sample diagnostic이며 Phase 075에서 독립 식별성과
  불확도를 다시 다뤄야 한다.
- Si fitted width ratio는 같은 문건에서 fit-tier diagnostic으로 제한된다.
  따라서 direct single-phase material evidence가 아니라 stated fit/extraction
  assumptions 아래 single-phase-consistent observation으로만 유지한다.
- graphite asymmetric prototype의 약 1 percentage-point in-sample 개선은
  자유 parameter 증가와 production capacity normalization 불일치를 포함한다.
  transferable physical-skew evidence가 아니다.
- main scientific text의 implementation/history 위반은 기존 literal-token
  inventory의 17행보다 넓다. main-tree `ch3v22_sec05_code.tex`와 prose-level
  implementation/default/bit-exact/history 표현은 Phase 087에서 prose-aware
  전수 inventory 후 designated appendix 또는 Implementation Companion으로
  이동해야 한다.

## Machine Artifact

`Codex/results/PHASE_065_DOC_CODE_GUIDE_CONFORMANCE_MATRIX.json`은 다음을
JSON-last로 고정한다.

- 41 claim-to-source-to-code-to-runtime rows.
- row별 severity, exact anchor, owner, acceptance criterion, target phase.
- 17개 prior route의 exact `origin_record`.
- source/generated/copied genealogy와 four-class authority precedence.
- source Git blob, raw SHA-256, lines, bytes, read range; control Git blob,
  raw SHA-256와 bytes.
- external/canonical/publication authority false.

## TDD and Validation Record

Validator-first RED:

```text
FAIL_P065_STEP74 E_CONFORMANCE_ARTIFACT_MISSING:
Codex\results\PHASE_065_DOC_CODE_GUIDE_CONFORMANCE_MATRIX.json
EXIT=1
```

JSON-last builder와 validator는 다음을 요구한다.

- strict duplicate/nonfinite JSON rejection and full recursive traversal.
- exact-seven stage, no unstaged control drift, no `Claude/**` change.
- source/control blob and raw-byte binding.
- semantic negative controls and deterministic generation `2/2`.
- active/upstream/tracking/live commit equality at persistence.
- protected branch와 `origin/main` pin 불변.
- Python 3.12와 3.14에서 같은 precommit/persistence Gate.

Precommit 수치와 terminal은 final freeze 뒤 이 문서의 `Final Freeze`에
고정한다.

## Findings and Owners

| ID | Severity | Finding | Owner / target |
|---|---|---|---|
| S74-F01 | P1 | regsol/root/unit/width/blend route와 blanket/full-conformance 기록 충돌 | `PHASE-083-IMPLEMENTATION-CONTRACT` / Phase 083 |
| S74-F02 | P1 | LCO Omega, analytic real-fit, capacity basis, main-body implementation claim의 authority 초과 | `PHASE-078-LCO-CLOSURE` 및 row별 owner |
| S74-F03 | P2 | HTML/version/unit/portable command/visual/exact-output repair 필요 | `PHASE-089-RELEASE-QA` 및 row별 owner |
| S74-F04 | P2 | inherited 17-image count와 fresh-observed 15-path numerator 충돌; 나머지 2개 identity 부재 | `PHASE-089-RELEASE-QA` |

Owner는 이 표의 대표 owner이고 machine row의 accountable owner가
정확한 정본이다. Step 75.1은 의미가 같은 기존 owner를 보존하고
ownerless/multiply-owned/semantic duplicate를 검사해야 한다.

## Final Freeze

- 독립 evidence 검독: 3개 분할 완료.
- 독립 final artifact 검독: `P0/P1/P2=0/0/0`.
- Python 3.12 precommit: `PASS_P065_STEP74_CONFORMANCE_WITH_CONCERNS`; rows/routes/nodes/depth=`41/17/2536/5`; negative/source-policy/output/transaction=`19/56/1/4`.
- Python 3.14 precommit: `PASS_P065_STEP74_CONFORMANCE_WITH_CONCERNS`; rows/routes/nodes/depth=`41/17/2536/5`; negative/source-policy/output/transaction=`19/56/1/4`.
- deterministic generation: `2/2 BYTE_IDENTICAL`.
- exact-seven stage: `PASS`.
- containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`.
- persistence: `PASS_PENDING_PERSISTENCE`.

## Confirmed Non-changes

- `Claude/**`를 수정하지 않았다.
- protected `codex/lib-physics-endgame-v1025_2`, `origin/main`, frozen baseline을
  변경하지 않았다.
- 기존 Step 70–73 machine artifacts와 results를 덮어쓰지 않았다.
- external scientific/material/experimental/proposition truth, canonical model,
  production repair와 publication readiness를 승격하지 않았다.

## Next Exact Action

Final artifact reviews에서 P0/P1/P2=`0/0/0`을 얻은 뒤 외부 `%LOCALAPPDATA%/Temp/p065-step74-manual-fixture`에 exact `matrix-step74-one.json`, `matrix-step74-two.json`, byte-exact `P065_STEP74_SENTINEL\n`의 `not-a-matrix-name.json`을 재생성한다.
Precommit에서는 Git index의 builder, validator, matrix blob bytes를 독립 SHA-256하여 세 pin을 얻고, 두 runtime validator에 `--determinism-one`, `--determinism-two`, `--output-sentinel`의 exact 경로와
`--expected-builder-sha256`, `--expected-validator-sha256`, `--expected-matrix-sha256`를 모두 넘긴다. 통과 뒤 exact-seven을 subject
`audit(phase065): adjudicate v1024 doc code guide`로 commit/push하고 fetch한다. Persistence에서는 같은 세 pin을 `<HEAD>:<path>` Git blob bytes에서 다시 독립 계산하고 두 runtime에 앞의 여섯 필수 인수와
`--persistence --expected-commit <HEAD>`를 함께 넘긴다. local/upstream/tracking/live remote equality, protected/main/Claude 불변과 clean
worktree 및 두 `PASS_P065_STEP74_PERSISTENCE`를 확인해야 Step 75.1이 열린다.
