# Phase 066 Step 080 — Profile Default / Temperature Route Result

## 1. 판정

선택 Gate는 `PASS_P066_STEP80_PROFILE_DEFAULT_TEMPERATURE_VERIFICATION`이다.
이 PASS는 frozen v1.0.25.2 production blob의 정적 route와 격리 runtime 동작을
서로 대조했다는 뜻이다. 저장된 profile의 외부 재료 권위, profile 선택 권위 또는
다중 온도 실험 권위를 승인한다는 뜻은 아니다.

- fresh public `BlendedAnodeDQDV(0.2)` 기본 경로: graphite 4 + SiC 2 = `4+2`,
  288.15 K와 308.15 K 사이 온도 의존 관측.
- `use_skew7_default(True)` 또는 동일 상수를 명시한 경로: `7+7`, 온도 비의존 관측.
- 전체 matrix: 16개 route, 온도 의존 9개, 비의존 7개.
- 격리 실행: Python 3.12/3.14 route 32회 + 순서 복원 4회 = `36/36` 성공,
  stderr `36/36` 공백, runtime 간 count/class/numeric/hash 전부 일치.
- 외부 재료·profile 선택·다중 온도 실험 authority: 전부 false.
- saved-profile loader, profile alias registry, module export list: frozen production
  source에서 `GROUND_NOT_FOUND`.

Postcommit terminal은 `PASS_P066_STEP80_PERSISTENCE`다. 이 terminal 전에는 Step 81.1을
시작하지 않는다.

## 2. 입력과 실제 확인 범위

모든 입력은 baseline commit `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`의
immutable Git blob으로 고정했다.

| 입력 | 실제 확인 범위 |
|---|---|
| `Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py` | 1–2024행 전문 직접 검독; AST 전체 parse; 각 격리 process에서 전체 module import |
| `Claude/docs/v1.0.25.2/test_gates_v1024.py` | 1–637행 전문 분담 검독; 70–79행 test-only default mutation 직접 대조 |
| `Claude/docs/v1.0.25.2/test_gates_v1025.py` | 1–398행 전문 직접 검독 |
| `Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md` | 12–75행 default/temperature correction 직접 대조 |
| `Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md` | 253–364행 U10→U12 supersession 직접 대조 |
| `Claude/docs/v1.0.25.2/FITTING_GUIDE.md` | 29–49행 temperature-fit 조건 직접 대조 |
| `Claude/results/comp_v26_data/out_versions/A_regsol/params_blend.json` | strict JSON 전체; 총 8성분 저장 profile |
| `Claude/results/comp_v26_data/out_versions/B_gallery/params_blend.json` | strict JSON 전체; 총 14성분 저장 profile |
| `Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json` | strict JSON 전체; 총 14성분 저장 profile |

위 Step 80 입력 identity는 commit/path/blob/raw SHA-256, byte 및 line count로 machine
artifact에 저장했다. 교차 release 전체 blob 계보는 Step 76의 persisted evidence를
이어받되, Step 80의 profile runtime Gate로 다시 승격하거나 재주장하지 않는다.

## 3. 정적 route 판정

실행되는 마지막 대입문은
`DEFAULT_GRAPHITE_TRANSITIONS = GRAPHITE_STAGING_LIT`와
`DEFAULT_SI_TRANSITIONS = None`이다. 따라서 Si 명시값이 없을 때 constructor의
기본 `si_case='sic'` fallback이 `SIC_LIT`를 고르고 fresh public default는 `4+2`다.

정적 문건에는 다음 충돌이 남아 있다.

- 파일 상단 3–6행과 class docstring 1596–1601행의 “7-gallery default” 설명은
  1439–1470행의 실제 대입·toggle 및 fresh runtime과 모순된다.
- 주석에만 존재하는 `use_legacy_4transition` 함수는 실제 AST에 없다.
- 1394행은 graphite skew7에 `alpha`가 없다고 하지만 1400–1406행의 일곱 literal
  모두 `alpha`를 가진다.
- 1397행은 graphite skew7 + symmetric Si7을 예시로 들고, 1415–1420행은 별도의
  Si skew7을 “확정 구성” 짝으로 선언한다. 어느 것도 fresh default가 아니며 caller의
  명시적 선택이 필요하다.
- `DEFAULT_CBG_GRAPHITE`, `DEFAULT_CBG_SI`는 선언되지만 AST runtime load가 각각 0회다.
- `load_profile`, `from_profile`, `PROFILE_ALIASES`, `SAVED_PROFILES`, module `__all__`은
  production source에서 `GROUND_NOT_FOUND`다.

## 4. 16개 runtime route

| Route | 성분 | 온도 판정 | 의미 |
|---|---:|---|---|
| fresh default | 4+2 | dependent | 실제 public default |
| explicit legacy | 4+2 | dependent | 명시적 동일 구성 |
| `from_wt(..., si_case='sic')` | 4+2 | dependent | factory fallback |
| global skew toggle | 7+7 | independent | 명시 toggle 후 fresh process |
| explicit skew pair | 7+7 | independent | graphite/Si skew literal 직접 주입 |
| explicit XRD | 5+2 | dependent | XRD5 + SiC2 |
| explicit MSMR6 | 6+2 | independent | fixed-U/w graphite6 + SiC2 |
| legacy graphite + symmetric Si7 | 4+7 | dependent | 혼합 thermal/fixed profile |
| skew graphite + symmetric Si7 | 7+7 | independent | source example 경로 |
| legacy graphite + elemental Si | 4+2 | dependent | Si case 대안 |
| legacy graphite + SiOx | 4+1 | dependent | Si case 대안 |
| LCO3 electronic OFF | 3+0 | dependent | cathode 독립 경로 |
| LCO3 electronic ON | 3+0 | dependent | electronic contribution 포함 |
| serialized regsol | 총 8 | independent | host split 미결속; current public logistic replay; stored kernel metadata는 dispatch되지 않음 |
| serialized gallery | 총 14 | independent | host split 미결속; 저장 parameter replay |
| serialized skew | 총 14 | independent | host split 미결속; 저장 parameter replay |

Public blend route에서는 host별 contribution을 독립 저장했고 `f_Si=0` limit가 graphite
단독 결과와 bit-exact임을 확인했다. 온도 판정은 288.15 K와 308.15 K의 equilibrium,
curve, finite-difference derivative 및 open-circuit voltage를 서로 분리해 계산했다.
fixed `U/w`만 가진 profile은 온도 비의존이고 `dH_rxn/dS_rxn/n` thermal input을 가진
route만 온도 의존한다.

## 5. 순서·전역 상태·runtime 독립성

각 route는 저장소 밖에 materialize한 frozen source를 Python `-B -I -X utf8` 새
process에서 실행했다. 각 runtime에서 두 순서 probe를 수행했다. 첫 순서는 fresh
4+2 → toggle true 7+7 → toggled 상태의 explicit legacy 4+2 → restore false 4+2이고,
둘째는 fresh 4+2 → non-mutating explicit skew 7+7 → toggle true 7+7 → restore false
4+2다. 양쪽 runtime에서 복원 후 관측값이 초기 상태와 일치해
`order_restoration_pass=true`다. 이는 명시적으로 복원한
순서의 동작 확인이며, mutable global API 자체를 thread-safe 또는 무상태라고 승인하지
않는다.

Python 3.12와 3.14 사이에는 16개 route의 component count, 온도 분류, 모든 scalar,
배열 통계와 little-endian float64 SHA-256이 일치했다. 저장 profile 3종은 현재 public
logistic evaluator로 재생했으며, 저장된 `regsol` kernel metadata가 production loader에
의해 자동 dispatch됐다는 의미로 해석하지 않는다.

## 6. 검증 계약

Validator는 다음을 독립 확인한다.

- 두 JSON의 strict canonical serialization과 semantic seal.
- 9개 입력의 commit/blob/raw identity와 모든 source line pointer.
- 16개 route의 exact component count·온도 분류·authority ceiling.
- 36개 process의 argv/cwd/exit/stdout/stderr/cleanup 및 양 runtime 일치.
- toggle 순서 복원, public contribution, `f_Si=0` bit-exact limit.
- 각 Python validator invocation에서 builder를 1회 재생성한 두 JSON byte identity,
  validator와 builder의 import/process/write source-policy 제한.
- exact-eight staged/commit transaction, expected parent/subject, branch/upstream/live
  remote, protected branch·main·`Claude/**` 불변과 clean worktree.

Named negative controls 13개는 fresh-import-before-mutation 위반, test-mutated default의
public default 승격, route 누락, 온도 분류 뒤집기, 순서 복원 실패 은폐, runtime의 외부
authority 승격, regsol kernel-equivalence 승격, stale comment의 executable-default 승격을
거부한다. 추가로 probe source hash, argv, run unknown field, 재봉인된 cross-runtime
observation divergence와 matrix runtime-field fabrication을 거부한다. Strict JSON,
semantic seal, stderr 및 component count도 별도의 본 검증에서 거부한다.

## 7. 생성·수정 파일

- `Codex/work/v1025_phase066/build_phase066_step80.py`
- `Codex/work/v1025_phase066/validate_phase066_step80.py`
- `Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json`
- `Codex/results/PHASE_066_RUNTIME_ATTESTATION.json`
- 본 결과 문건
- 두 execution ledger
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

현재 상태는 exact-eight commit/push 전 `PASS_PENDING_PERSISTENCE`다. Commit subject는
`audit(phase066): verify profile default temperature routes`다. Python 3.12/3.14
`PASS_P066_STEP80_PERSISTENCE` 뒤 Step 81.1 source disposition으로 진입한다.
