# Phase 066 Step 079 — Empirical Fit / Physical Authority Separation Result

## 1. 판정

선택 Gate는 `PASS_P066_STEP79_EMPIRICAL_PHYSICAL_SEPARATION`이다. 이 PASS는
Step 79의 권위 분리 계약이 충족됐다는 뜻이며, 외부 과학 검증·재료 상 식별·문헌
명제 검증이 완료됐다는 뜻이 아니다.

- Direct14: `empirical_pass=true`, `external_authority=false`,
  `phase_authority=false`, `proposition_authority=false`,
  `physical_authority=false`.
- 8개 claim row 전체: `physical_authority=false`.
- held-out cell/rate/temperature: `NOT_TESTED` 또는 적용 불가.
- 독립 noise model, covariance, 구조상·종·열역학 corroboration:
  `GROUND_NOT_FOUND`.
- Ref. 7 primary text: `GROUND_NOT_FOUND`; owner
  `PHASE-071-PRIMARY-SOURCE-ACQUISITION`.

Postcommit terminal은 `PASS_P066_STEP79_PERSISTENCE`이며, 이 terminal 전에는 Step 80을
시작하지 않는다.

## 2. 입력과 실제 확인 범위

입력은 immutable Git blob으로 고정했다.

| 입력 | 고정 commit | 확인 |
|---|---|---|
| `PHASE_066_DIRECT14_FIT_REPRODUCTION.json` | `fedb2031fbfabeaba84f86427c35334526234d73` | strict JSON, 전체 recursive traversal |
| `PHASE_066_FIT_INPUT_PROVENANCE.json` | same | strict JSON, 전체 recursive traversal |
| `PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json` | same | strict JSON, 전체 recursive traversal |
| `PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json` | `272b8d331c55448182e96c75363a56061adf58f2` | strict JSON, 28 material rows·7 metadata rows 전체 |

독립 read-only 대조는 위 네 JSON과 Phase 065 source-disposition matrix를 합쳐
`25,216` recursive node를 확인했다. Step 79 계획은 452–491행, Phase 065 Step 72
결과서는 1–472행을 확인했다. Step 77/78 결과와 두 ledger, active handover의 현재
범위도 재확인했다.

## 3. Direct14의 허용 범위

Direct14의 허용된 주장은 한정된 수치 재현뿐이다.

- 입력: repository-derived `sigr.csv`, absolute mAh basis, 1,280 retained points.
- source-declared specimen/protocol: graphite+Si blend half-cell, pOCV, C/50,
  room temperature approximately 25 °C.
- exact original parquet/specimen/composition/protocol cryptographic binding:
  `GROUND_NOT_FOUND`.
- profile: skew-logistic 14 components, 57 free parameters.
- in-sample R² `0.999649399285802`, BIC `-4760.585852788185`, cost
  `11.287055224907945`.
- weighting: retained point별 unit weight; independent noise model/covariance는
  `GROUND_NOT_FOUND`.
- selected trial 11: nonconverged, `runtime_success=false`,
  `selected_trial_converged=false`.
- stored↔replay vector `NOT_EQUIVALENT`; replay cross-runtime vector `IDENTICAL`;
  replay↔stored curve/objective `TOLERANCE_EQUIVALENT`.

따라서 BIC와 R²는 이 한 profile의 in-sample record이며, competing-profile selection,
held-out generalization, multi-temperature behavior 또는 unique parameter/mechanism
authority가 아니다.

## 4. 8개 권위 행

| ID | 범위 | 판정 | owner/ceiling |
|---|---|---|---|
| E79-01 | Direct14 skew empirical | bounded in-sample replay만 PASS | Phase 066 Step 79; physical authority 없음 |
| E79-02 | competing-profile empirical | profile universe·parameter count·exact metric/BIC `GROUND_NOT_FOUND`; held-out `NOT_TESTED` | `PHASE-069-STEPS-102-104-MODEL-AND-DATA-SYNTHESIS` |
| P79-03 | graphite phase/gallery | whole-blend metric과 component label은 graphite-specific phase evidence가 아님 | `P071-PRIMARY-SOURCE-ACQUISITION` |
| P79-04 | LCO phase/species | Direct14 specimen scope에 LCO가 없고 real O3 multi-temperature support `GROUND_NOT_FOUND` | `P071-PRIMARY-SOURCE-ACQUISITION` |
| P79-05 | Si phase/mechanism | whole-blend metric은 Si를 분리하지 않으며 width-only inference는 unverified, symmetric Frumkin skew는 내부 대칭성에 반함 | `P071-PRIMARY-SOURCE-ACQUISITION` |
| P79-06 | blend material fraction | Q는 fitted absolute-mAh component area일 뿐 mass fraction/composition이 아님 | `P071-PRIMARY-SOURCE-ACQUISITION` |
| P79-07 | blend finite-rate | whole-curve fit은 `I=I_gr+I_Si`, host independence 또는 nonadditivity 시험이 아님 | `P067-CODE-HISTORY` |
| P79-08 | Ref. 7 proposition | metadata observation은 proposition/page/equation support가 아니며 primary text `GROUND_NOT_FOUND` | `PHASE-071-PRIMARY-SOURCE-ACQUISITION` |

모든 행은 dataset/specimen/protocol/basis, profile/parameter count, in-sample metric,
held-out evidence, noise/weighting, information criterion, identifiability, independent
structural/thermodynamic support, empirical/physical ceiling과 owner를 동일한 closed schema로
가진다. 적용 불가나 미확보 값을 생략하지 않고 `NOT_APPLICABLE`, `NOT_TESTED`,
`GROUND_NOT_FOUND`로 보존했다.

## 5. 검증 계약

Validator는 다음을 독립 확인한다.

- 네 입력의 commit/path/blob/raw SHA/byte identity, canonical JSON과 semantic seal.
- 모든 structured source pointer의 RFC 6901 해석 가능성과 expected record ID.
- 8개 행과 모든 nested evidence axis의 closed schema.
- Direct14 dataset/profile/metric/noise/BIC/vector-state source binding.
- `empirical_pass=true`가 external/phase/proposition/physical authority를 설정하지 않음.
- Step 77 `runtime_success=false`, selected-trial nonconvergence와 unsealed external
  process fields의 `GROUND_NOT_FOUND` 보존.
- exact-seven staged/commit transaction, branch/upstream/live remote, protected branch와
  main tip 불변, `Claude/**` 비변경, clean worktree.

Named negative controls 17개는 in-sample→external, component→phase,
metadata→proposition, missing-evidence omission, empirical-pass→physical-authority,
RT→multi-temperature, curve→identifiability, invalid source pointer, runtime-success
promotion, owner omission, nested unknown key, aggregate drift뿐 아니라 structural-support,
held-out cell, exact dataset-binding, noise-model 및 unidentified-pointer 승격을 거부한다.

## 6. 생성·수정 파일

- `Codex/work/v1025_phase066/build_phase066_step79.py`
- `Codex/work/v1025_phase066/validate_phase066_step79.py`
- `Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json`
- 본 결과 문건
- 두 execution ledger
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

현재 상태는 exact-seven commit/push 전 `PASS_PENDING_PERSISTENCE`다. Commit subject는
`audit(phase066): separate fit and material authority`다. Dual-runtime
`PASS_P066_STEP79_PERSISTENCE` 뒤 Step 80의 profile/default/temperature verification으로
진입한다.
