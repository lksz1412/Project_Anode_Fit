# Phase 065 Step 73 — Independent Initialization and Runtime Result

정본일: 2026-08-31
대상 frozen baseline: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`
직전 persisted Step: Step 72 commit
`272b8d331c55448182e96c75363a56061adf58f2`
계획: `Codex/plans/2026-08-30-phase065-v1024-v1024_1-lineage-detailed-plan.md`

## 1. Outcome

선택 Gate는 **`PASS_P065_STEP73_INITIALIZATION_RUNTIME_WITH_CONCERNS`** 다.
이 Gate는 frozen Git blob을 저장소 밖 disposable directory에 materialize한 뒤
Python 3.12와 3.14의 별도 프로세스에서 확인한 내부 실행 동작만 통과시킨다.

- `fresh_import`: `IMPLEMENTED_AND_OBSERVED`
- `explicit_profile`: `IMPLEMENTED_AND_OBSERVED`
- `legacy_restoration`: `ABSENT_IN_FROZEN_SOURCE`

마지막 항목은 audit closure이지 behavior PASS가 아니다. v1.0.23 또는 v1.0.24에
model saved-state schema, restore key, restoration loader가 없으므로 predecessor
schema fixture나 adapter를 만들지 않았다. 부재를 구현된 migration으로 승격하는
변이는 반드시 실패한다.

Containing commit은 result-first 설계상
`PENDING_AT_PRECOMMIT_BY_DESIGN`이며, Step 종료 commit/push 뒤 별도 persistence
검증으로 결속한다.

## 2. Recovery and Evidence Boundary

Controller는 Phase 065 detailed plan의 Step 73 계약, Step 71 result/matrix의
40개 initialization row와 11개 profile surface, Step 72 result/matrix 및 두 실행
ledger와 active handover를 직접 다시 확인했다. 세 독립 검토자는 다음 범위를
나눠 확인했다.

- source-contract reviewer: `Codex/AGENTS.md`와 Step 71 result 전문,
  Step 71 machine artifacts의 strict full traversal, Step 73 plan 구간,
  frozen v1.0.23/v1.0.24 runtime-relevant API와 loader/test anchors
- runtime-probe reviewer: constructor/profile/fallback/seconds-hour/root/alias
  계약과 저장상태 부재 census
- evidence-quality reviewer: Step 71/72 controls, 이전 runtime builder/validator
  patterns, exact-eight/result-first/JSON-last 및 negative-control 요구사항

Frozen production module은 working checkout에서 import하지 않았다. Exact baseline
blob만 `git cat-file blob`으로 외부 임시 디렉터리에 썼고, 모든 resolved path가
그 임시 root 아래인지 확인했다. Probe는 `-B -I -X utf8`로 실행되어 bytecode를
쓰지 않았고 network를 요청하지 않았다. `Claude/**`는 읽기 전용이었다.

## 3. Initialization Routes

### 3.1 Fresh import/default route

이 route의 model observation은 profile override와 saved state 없이 필요한
`f_Si`만 넣은 `BlendedAnodeDQDV(0.0)`이다.

- graphite default는 4-entry `GRAPHITE_STAGING_LIT`
- Si default selector는 `si_case='sic'`, 2-entry `SIC_LIT`
- `Q_Si=0`
- `lag_ratio_correction=False`, `use_dH_eff=True`
- `GraphiteAnodeDischargeDQDV()`와 `LCOCathodeDQDV()`는 `transitions`가 필수라
  `TypeError`; 이를 zero-argument default model로 보고하지 않는다.

Fresh route를 v1.0.23 blob으로 redirect하면서 v1.0.24-only symbol identity를
요구한 mutation은 두 runtime 모두 실패했다.

### 3.2 Explicit named profiles

Step 71의 11개 surface를 다음 public route로 모두 실행했다.

| Surface | Public route |
|---|---|
| `GRAPHITE_STAGING_LIT` | `GraphiteAnodeDischargeDQDV(transitions)` |
| `GRAPHITE_STAGING_XRD_v1024` | same direct constructor |
| `GRAPHITE_STAGING_MSMR6_LIT` | same direct constructor |
| `LCO_MSMR_LIT` | `LCOCathodeDQDV(transitions)` |
| `SI_ELEMENTAL_LIT`, `SIOX_LIT`, `SIC_LIT` | `BlendedAnodeDQDV(si_transitions=...)` |
| `SI_CASE_SETS` | `BlendedAnodeDQDV(si_case=..., si_transitions=None)` |
| `SI_CASE_GAPS` | constructed blend의 `gaps` |
| `SI_SPECIFIC_CAPACITY` | `BlendedAnodeDQDV.from_wt(q_Si=None)` |
| `GRAPHITE_SPECIFIC_CAPACITY` | `BlendedAnodeDQDV.from_wt(...)` with `q_gr` omitted |

XRD5를 4-stage list로 redirect한 mutation은 profile hash mismatch로 두 runtime
모두 실패했다. Normal route는 registry hash를 보존했다. 별도 마지막 alias
observation은 Graphite constructor가 transition list를 reference로 보유하므로
같은 프로세스에서 instance mutation이 module registry도 바꿀 수 있음을 재현했고,
즉시 원상복구했다. Canonical route는 매번 새 프로세스를 쓰므로 이 alias leak를
서로 공유하지 않는다.

### 3.3 Legacy restoration

Step 71의 모든 40 initialization row는
`restore_key=ABSENT_IN_FROZEN_SOURCE`이며 frozen endpoint census에서도 schema와
loader가 없다. Step 73의 child observation은 선택된 candidate surface가 없음을
corroborate할 뿐 restoration을 실행한 것이 아니다. 따라서:

- `process_run_ids=[]`
- 별도 `absence_corroboration_run_ids`만 기록
- predecessor schema fixture: `ABSENT_IN_FROZEN_SOURCE`
- passing behavior route: `false`

Old-key absence와 current saved-state-key presence는 둘 다 별도 질문으로 유지했지만,
두 persistence schema 자체가 없으므로 각각 `ABSENT_IN_FROZEN_SOURCE`다. `kernel`,
constructor option 또는 `from_wt`를 current persistence key나 restoration path로
대체하지 않았다.

가짜 implemented-restoration claim은 negative control에서 거부했다.

## 4. Runtime and Numerical Observations

두 runtime에서 v1.0.23 main/selfconsistent와 v1.0.24
main/selfconsistent/reflect 공식 gate, 합계 `10/10`이 exit 0이었다. Route schedule은
forward `fresh→explicit→legacy`와 reverse `legacy→explicit→fresh`이며 각 route를
고유 materialized source/probe fixture를 가진 독립 child process에서 실행했다.
구현 route `8/8`, absence corroboration `4/4`,
route mutation `6/6`, changed-order equality `6/6`이다.

Step 71 F01–F11의 runtime 결론은 다음과 같다.

| Finding | Step 73 observation |
|---|---|
| F01 | exact `kernel='regsol'`은 equilibrium에서만 logistic과 달랐고 `dqdv`, entropy, root는 logistic과 bit-exact였다. Named profile은 regsol을 선택하지 않았다. |
| F02 | Runtime call observation에서 Blend 두 host가 같은 full `I_abs`와 external `Q_cell`을 받았고 internal `Q`와 external `Q_cell`은 독립이었다. Partition solver 부재는 이 probe의 상수 판단이 아니라 Step 71 static census가 소유한다. |
| F03 | 정상 bracket root는 수렴했지만 `max_iter=0` 또는 음수는 같은 silent initial midpoint를 반환했다. Reversed/non-bracketing interval은 예외였다. |
| F04 | `curve(c_rate=1,Q_cell=2)`는 direct `I_abs=2`와 bit-exact이고 `2/3600` 경로와 달랐으며 lag ratio는 3600이었다. 실행 code에는 seconds migration이 없다. |
| F05 | missing `n`은 `_n_factor=1`이지만 `_dwdT=0`; explicit `n_T1=None`은 `_n_factor`에서는 absent처럼 처리되고 `_dwdT`에서는 예외였다. `n=0` width는 예외였다. |
| F06 | v1.0.23 LCO default는 v1.0.24 explicit ON과 bit-exact. v1.0.24 omitted/False/0/None은 OFF로 같고 298.15 K 보존 tolerance 안에서 ON과 일치하지만 318.15 K에서 달랐다. |
| F07 | saved-state restoration/migration은 `ABSENT_IN_FROZEN_SOURCE`; 동작 PASS가 아니다. |
| F08 | XRD5의 `Omega`를 제거해도 `kernel` 부재 경로 equilibrium은 bit-exact였다. |
| F09 | MSMR6는 direct explicit injection으로만 관찰됐다. Frozen Python endpoint 자동 activation은 없다. |
| F10 | kernel absent/None/False/typo는 logistic bit-exact; exact `regsol`만 활성. delta absent는 width, `None`은 예외, zero/False/negative는 `1e-9` clamp와 같은 finite 결과였다. |
| F11 | `I_abs=None`은 `c_rate*Q_cell`, explicit zero/False는 nonzero c-rate를 override했고 numeric direction 0은 positive direction이었다. |

추가로 `use_dH_eff` omitted/True와 False/0/None을 분리했고,
`lag_ratio_correction` omitted/False/0/None과 True liveness를 분리했다.
Invalid Si case, empty graphite profile, missing capacity registry, GS-1 plastic loop,
GS-2 nonadditive correction의 예외/미구현 경계를 그대로 보존했다.

## 5. Machine Evidence

Result-first control 문서를 고정한 뒤 builder가 다음 JSON을 마지막에 생성한다.

1. `Codex/results/PHASE_065_INITIALIZATION_ROUTE_MATRIX.json`
2. `Codex/results/PHASE_065_RUNTIME_ATTESTATION.json`

각 route run은 고유 fixture ID와 source root, launcher, isolated flags, normalized
command/cwd, interpreter 및 NumPy version, observations, mutation probe, gate,
materialized input manifest hash, source before/after hash, stdout/stderr 전문과 hash,
exit code와 combined output hash를 보존한다. Matrix는 Step 71의 exact initialization/profile
mapping을 그대로 소비하며 runtime attestation의 semantic identity에 결속한다.

Runtime-environment 2건과 official gate 10건은 공통 frozen base fixture를 사용하며,
base fixture의 실제 파일 목록과 source hash는 top-level isolation record가 실행 전후로
소유한다. 고유 fixture 및 run별 before/after hash 주장은 18개 route run에만 적용한다.

### 5.1 Approved-plan source-policy correction

Detailed plan 782–784행은 유일한 `run_process`/`subprocess.run` 지점을 Git wrapper
구현에만 허용한다고 적었다. 그러나 Step 73의 승인된 본체는 frozen blob을 별도
Python 3.12/3.14 child process에서 실행해 environment, official gate, route 및
mutation evidence를 수집해야 하므로 Git child만으로는 실행 계약을 만족시킬 수 없다.
이에 원 계획을 덮어쓰지 않고 다음과 같이 제한적으로 교정해 구현했다.

- 유일한 `subprocess.run` call site는 `_run_subprocess` 하나다.
- `_run_subprocess`의 허용 caller는 `run_git`과 `run_runtime` 두 wrapper뿐이다.
- validator는 direct, aliased, dynamic-attribute, `Popen` 실행과 제3 caller를
  AST negative control로 거부한다.
- 이 교정은 disposable runtime evidence 수집만 허용하며 production source write나
  scientific/material/external authority를 추가하지 않는다.

## 6. Authority Ceiling

이 Step이 확정하는 것은 exact frozen blob, 두 실제 interpreter/NumPy 환경, 고정
합성 fixture와 관찰 predicate에 한정된다. 다음 권위는 모두 `false`다.

- external scientific truth
- material truth
- experimental truth
- primary-source proposition/page/equation support
- canonical adoption/default selection
- publication readiness

v1.0.24.1은 v1.0.24 byte-identical mirror이므로 독립 runtime corroboration으로
계수하지 않는다.

## 7. Validation and Review Gate

Precommit 필수 조건은 다음과 같다.

- strict duplicate/nonfinite JSON parse, full recursive traversal 및 exact schema fingerprint
- Python 3.12/3.14 content 및 staged validation
- semantic mutations, embedded-probe AST/source policy, exact baseline blob binding
- environment/official exit code exact zero 및 live Python/NumPy identity 재대조
- official stdout와 fresh/explicit/legacy route observation의 exact semantic pin
- explicit `--output-dir` repository-containment rejection before any write
- exclusive random temporary output and pre-existing temp-link escape rejection
- provisional builder determinism `2/2`
- exact-eight stage, no unstaged exact-path bytes
- exact symbolic upstream name, one-row full remote ref identity 및 index/worktree raw-byte equality
- independent reviews P0/P1/P2=`0/0/0`

위 수치는 최종 freeze에서 validator와 review가 다시 확인해야 하며 실패 시 이
결과의 PASS candidate는 폐기하고 repair/re-review한다.

## 8. Exact Transaction

Step 73 exact-eight는 builder, validator, route matrix, runtime attestation, 본 result,
두 execution ledger, active handover다. Expected parent는
`272b8d331c55448182e96c75363a56061adf58f2`, subject는
`audit(phase065): separate v1024 initialization routes`다.

Commit/push/fetch 뒤 Python 3.12와 3.14에서
`--persistence --expected-commit <new HEAD>`를 실행하고 local HEAD, upstream,
tracking ref, live origin, protected/main pins, exact-eight bytes와 clean worktree를
확인해야만 `PASS_P065_STEP73_PERSISTENCE`가 성립하고 Step 74가 열린다.
