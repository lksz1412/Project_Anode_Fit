# Phase 066 Step 078 — Stored Vector and Original Optimizer-State Binding Result

정본일: 2026-09-01

계획: `Codex/plans/2026-09-01-phase066-v1025-v1025_2-lineage-detailed-plan.md`

선행 persistence: Step 77 commit
`5d26e0746864cea7a8bd37a22874093b73c1a12f`, Python 3.12/3.14
`PASS_P066_STEP77_PERSISTENCE`

## 1. 판정

선택 Gate는
`CONDITIONAL_P066_STEP78_VECTOR_BOUND_WITH_ORIGINAL_STATE_GROUND_NOT_FOUND`다.

저장된 57개 숫자는 source가 최적화 반환값을 8자리로 반올림해 JSON에 기록한
`DISPLAYED_ROUNDED_VECTOR`다. Python 3.12/3.14 replay의 57개 full-precision vector는
서로 `IDENTICAL`하지만 저장 vector와는 `NOT_EQUIVALENT`다. 저장소에 남지 않은 original
historical full-precision vector와 optimizer state는 모두 `GROUND_NOT_FOUND`이며, 저장
vector나 replay vector로 대체하지 않는다.

## 2. 직접 확인 범위

- Phase 066 상세 계획: 1–760행.
- persisted Step 77 fit JSON: 1–3,592행, strict canonical/semantic traversal.
- persisted Step 77 provenance JSON: 1–224행, strict canonical/semantic traversal.
- persisted Step 77 결과 문건: 1–203행.
- frozen `summary_versions.json`: 1–873행, `C_skew/blend/params` 원 numeric token 57개.

입력은 Step 77 commit `5d26e0746864cea7a8bd37a22874093b73c1a12f`과 baseline
`3b5fd059ed09cdcdde38668c399cb35b8afbcca9`의 Git blob으로 고정했다.

## 3. Vector 계층과 정밀도

Parameter 순서는 `[U×14, w×14, Q×14, alpha×14, bg]`이고 flat index는 0부터 센다.
저장 token 57개의 소수 자릿수 분포는 2자리 1개, 7자리 8개, 8자리 48개다. 따라서
이를 “고정 폭 8-decimal 문자열”이라고 부르지 않고, source의 `round(..., 8)`을 거친
JSON numeric token이라고 부른다. 원 token sequence의 SHA-256은
`8b5b739160c782ea63a55df93930e803c692ba446072811d7ef777820cee9d39`다.

| 비교 | 판정 | 원소 분류 | 최대 절대차 | 평균 절대차 |
|---|---|---:|---:|---:|
| stored 8dp ↔ Python 3.12 replay | `NOT_EQUIVALENT` | identical 0 / tolerance 1 / not-equivalent 56 | 1.2482043497025828 | 0.09219197958910194 |
| stored 8dp ↔ Python 3.14 replay | `NOT_EQUIVALENT` | identical 0 / tolerance 1 / not-equivalent 56 | 1.2482043497025828 | 0.09219197958910194 |
| Python 3.12 ↔ Python 3.14 replay | `IDENTICAL` | identical 57 / tolerance 0 / not-equivalent 0 | 0 | 0 |
| original historical ↔ any retained vector | `GROUND_NOT_FOUND` | 해당 없음 | 해당 없음 | 해당 없음 |

사전 절대 tolerance는 `5e-8`이다. Replay 값을 다시 소수 8자리로 반올림해도 stored
numeric value와 같은 원소는 0/57이다. 최대 차이는 alpha component 7, flat index 48이다.

Family별 stored↔replay 최대/평균 절대차는 다음과 같으며 두 runtime이 같다.

| Family | 최대 절대차 | 평균 절대차 | 최대 flat index |
|---|---:|---:|---:|
| U | 0.02073040586764388 | 0.003128687053876198 | 6 |
| w | 0.09142841999999998 | 0.01315281444538911 | 20 |
| Q | 1.0319157430667991 | 0.14854553325960657 | 34 |
| alpha | 1.2482043497025828 | 0.2103038674267983 | 48 |
| bg | 0.0031102059794280157 | 0.0031102059794280157 | 56 |

## 4. Curve/objective와 parameter equivalence 분리

- Python 3.12↔3.14 prediction과 objective는 `IDENTICAL`이다.
- Replay↔stored prediction RMSE는 `0.0005229047404880496`, tolerance `0.002` 이내라
  `TOLERANCE_EQUIVALENT`다.
- Replay cost의 stored-vector self-evaluation 대비 상대차는
  `5.310664260083087e-05`, tolerance `0.001` 이내라 `TOLERANCE_EQUIVALENT`다.
- 이 curve/objective equivalence는 ordered vector equality나 parameter identifiability를
  뜻하지 않는다.

## 5. Selected replay trial과 경계

두 runtime의 selected trial 11은 같은 vector와 다음 진단값을 가진다.

- `success=false`, `status=0`, `nfev=6000`, `njev=5656`.
- cost `11.287055224907945`, optimality `0.11459771897658692`.
- active mask lower/free/upper = `0/56/1`.
- 유일한 active parameter는 w component 7, flat index 20이며 값
  `0.11999999999999998`, upper bound `0.12`, 거리
  `1.3877787807814457e-17`이다.
- Stored 8dp vector는 out-of-bounds 0이고, w component 13, flat index 26이 upper bound
  `0.12`와 exact-equal이다. Replay의 near-bound component와 stored의 exact-bound component는
  서로 다르므로 boundary state도 동일하다고 보지 않는다.

이 값들은 sealed replay runtime record의 진단값이지 original historical fit의 진단값이
아니다. 따라서 `runtime_success=false`를 유지한다.

## 6. Original optimizer state availability

다음 original historical fields는 모두 `GROUND_NOT_FOUND`다.

- full-precision returned/initial vector, prediction, residual, RSS, cost.
- success, status, termination message, nfev, njev, optimality, active mask.
- Jacobian, gradient, covariance, Hessian, inverse Hessian.
- historical Python/NumPy/SciPy 및 resolved loss/method/tolerances/Jacobian scheme.

Source-explicit solver, bounds, `max_nfev`, objective와 reconstructed RNG/start matrix는
계약·재구성 증거다. 이를 original runtime state로 승격하지 않는다.

## 7. 생성·수정 파일과 검증

- `Codex/work/v1025_phase066/build_phase066_step78.py`
- `Codex/work/v1025_phase066/validate_phase066_step78.py`
- `Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json`
- 본 결과 문건
- 두 execution ledger
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

Validator는 frozen source token, vector 순서와 정밀도, pairwise/family/component delta,
curve/objective tolerance, selected trial/boundary, original-state GNF와 authority ceiling을
독립 재계산한다. 8-digit/full-precision substitution, original-state promotion, wrong vector
classification/order, tolerance widening, replay-diagnostic promotion, identifiability promotion,
unknown-key mutation 8종을 거부한다.

현재 exact-seven commit/push/persistence 전 상태는 `PASS_PENDING_PERSISTENCE`다. Step 79는
commit subject `audit(phase066): bind optimizer state vector`와 Python 3.12/3.14
`PASS_P066_STEP78_PERSISTENCE` 뒤에만 시작한다.
