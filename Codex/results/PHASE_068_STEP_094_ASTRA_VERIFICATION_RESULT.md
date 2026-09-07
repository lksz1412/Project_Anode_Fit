# Phase 068 Step 94 — Astra Verification Result

## Summary / Step Range

Precommit state: `CONTENT_VERIFIED_AWAITING_PUSH`.
기존 U13 유도 후보를 보존한 채 새 책임 전환 계약으로 전체 수치 artifact를 실제 생성하고,
Python 3.12/3.14의 재계산 대조 및 독립 검산을 완료했다.
이 상태는 과학 content 검증 결과이며 commit/push 완료를 미리 주장하지 않는다.
현재 저장 여부는 이 문건을 포함한 Git commit과 live origin으로 확인한다.

Master: `Codex/plans/2026-09-07-astra-canonical-completion-master-plan.md`.
Detailed plan: `Codex/plans/2026-09-07-phase068-astra-continuation-detailed-plan.md`.
Previous candidate: `Codex/results/PHASE_068_STEP_094_U13_REGSOL_REDERIVATION_RESULT.md`.
Responsibility checkpoint: `aedfd408281b97699ba7f75884e7108965ecf547`.
Plan activation / expected execution parent: `58d752b63b75a4e516e76f848c1e308adeca0e03`.
두 commit 모두 정상 push/live equality/clean을 실제 확인했다.

## Inputs / Read Coverage

- 이전 master 1–665, 이전 detailed plan 1–801, candidate result 1–394 전문 재확인.
- 프로젝트 AGENTS 1–180, planning operations guide 1–246 전문.
- 기존 validator 1–1224 및 builder 1–91: 앞선 Astra 전문 검독을 hash 확인 후 재사용한다.
  이번 continuation의 직접 재확인 구간은 validator 1–101, 229–312, 590–698, 1070–1224;
  builder 1–91이다. 이전 전체 검독과 현재 부분 재독을 구분한다.
- frozen source 8개 전체의 이전 read attestation은 candidate result의 표에 있다.
  이 새 runner 실행으로 fresh human full read가 생기는 것은 아니다.
- 현재 재개 시 active master 1–760, detailed plan 1–219, 이 결과서의 WIP 1–74,
  compact ledger/active handover 전문을 직접 재확인했다.
- U13-AFTER 190–235행과 실제 before/after patch, WIDTH-DEFINITION 264–276행,
  PEAK-DEFINITION 1–131행을 새로 대조했다. 재사용한 나머지 원천 범위를 fresh로 부풀리지 않는다.
- 신규 runner 1–159 및 test 1–111을 주 담당과 독립 검토자가 전문 검독했다.
  독립 검토자는 receipt 관련 실제 성공/실패 child 시험을 두 runtime에서 별도로 실행했다.
- 92,357-byte matrix 전체는 두 runtime의 독립 process 재계산·strict parse·canonical bytes·구조/값 비교로
  검사했다. 새 사람이 matrix의 모든 raw 문자를 전문 읽었다는 판정은 하지 않는다.
  주 담당은 8개 source identity, 고정밀 12행, convergence 9행, extension 첫/끝행을 별도 표시해 대조했다.

## Files Created / Updated

신규 작성: `run_phase068_step94_astra.py`, `test_phase068_step94_astra.py` (Codex/work/v1025_phase068), 이 결과서.
생성 완료: `PHASE_068_U13_REGSOL_REDERIVATION.json` (Codex/results).
최종 실행 capture 경로: `PHASE_068_STEP_094_ASTRA_RUNTIME_312.json`,
`PHASE_068_STEP_094_ASTRA_RUNTIME_314.json` (Codex/results). 두 receipt의 실제 성공/identity 확인은
이 결과서 동결 후 수행하는 commit 전 필수 gate이며, 단지 이 목록에 있다는 이유로 존재를 가정하지 않는다.
갱신: compact ledger/active handover, 사용자 요청 예상시간을 추가한 활성 master,
그 변경의 allowlist를 명시한 active detailed plan.
기존 candidate result/validator/builder/대형 controls/Claude 원천은 수정하지 않았다.

## Execution Evidence / Validation

1. Test-first RED:
   `py -3.12 -B Codex/work/v1025_phase068/test_phase068_step94_astra.py`.
   runner 생성 전에 실제 실행하여 exit 1, `Ran 8 tests`, `FAILED (failures=8)`.
   이유는 각 시험의 `Checkpoint-aware evidence runner is not implemented` assertion이다.
   중간 traceback 출력은 잘렸으므로 전체 raw stderr를 보존했다고 주장하지 않는다.
2. Runner 작성 후 같은 명령: exit 0, `Ran 8 tests in 0.178s`, `OK`.
3. `py -3.14 -B Codex/work/v1025_phase068/test_phase068_step94_astra.py`:
   exit 0, `Ran 8 tests in 0.167s`, `OK`.
4. 실제 missing-matrix RED:
   `py -3.12 -B Codex/work/v1025_phase068/run_phase068_step94_astra.py --verify`:
   exit 1, `FAIL_P068_STEP94_ASTRA E_MATRIX_MISSING: E_MATRIX_MISSING: PHASE_068_U13_REGSOL_REDERIVATION.json`.

8개 시험은 missing input, source mismatch, canonical envelope roundtrip, resealed wrong checkpoint,
unsealed mutation, fresh-read 과장, no-clobber writer, duplicate JSON key를 검사한다.
전체 수치/원문/과학 검증을 대신하지 않는다. 실제 CLI missing 진단도 별도로 실패함을 확인했다.

## Decisions / Current Limits

- 기존 계산 모듈은 변경하지 않았다. 신규 runner는 기존 science candidate를 envelope 안에 넣고,
  옛 expected parent와 새 execution parent를 구분한다.
- 기존 pre-JSON 6개 identity는 checkpoint Git blob으로 정규화하여 checkout LF/CRLF 영향과 분리한다.
- 기존 source의 AST/negative-control 검사도 재사용하지만 그 통과를 새로운 범용 보안 보증으로 부르지 않는다.
- 이전 결과의 28 negative / 16 builder tests 문구는 최신 완료 수치로 사용하지 않는다.
  실제 전체 candidate negative controls는 두 runtime에서 각각 86개 통과했다.
  기존 builder의 별도 `--self-test` 전체를 실행한 것으로 보고하지 않는다.
- 사용자의 예상시간 질문에 master에 순수 활성 작업 40–80시간, 중심 약 60시간의 조건부 추정과
  phase별 범위/중간본/최종 완료기준을 추가했다. 원문·데이터 대기와 세션/토큰 중단은 제외한다.
- 위 예상시간은 완료 보장/실측 처리율이 아니며 과학 범위를 줄이는 허가도 아니다.

## Fresh Full Numerical Evidence

실제 명령:

```text
py -3.12 -B Codex/work/v1025_phase068/run_phase068_step94_astra.py --preview
py -3.14 -B Codex/work/v1025_phase068/run_phase068_step94_astra.py --preview
py -3.12 -B Codex/work/v1025_phase068/run_phase068_step94_astra.py --collect
py -3.12 -B Codex/work/v1025_phase068/run_phase068_step94_astra.py --verify
py -3.14 -B Codex/work/v1025_phase068/run_phase068_step94_astra.py --verify
```

위 명령 모두 exit 0. 최초 3.12 preview는 receipt 수정 전 wrapper이므로 envelope hash가 달랐다.
수정 후 3.14 preview, 3.12 collection 및 최종 두 verify의 artifact는 모두 다음과 같다.

- Bytes: `92357`.
- SHA-256: `20c9f6f3d2c3e9be2ab2c61933285c7a3444135071c6e8567fd69d0e4c9bb59a`.
- Content terminal: 두 runtime 모두 `PASS_P068_STEP94_ASTRA_CONTENT`.
- Source records: `8`, bytes `126576`, lines `1870`; proposition rows `7`.
- 수치 rows: historical Phase 044 `8`, Phase 054 `9`, normalization `25`, extension `55`,
  convergence `9`, high precision `12` (합계 118; full-factorial 실험이 아니다).
- 기존 negative controls: 각각 `86`. 이 안에는 과거 transaction fixture 시험이 포함되며,
  그 성공을 현재 Git persistence 성공으로 부르지 않는다.
- Binary64와 35/55 decimal-digit tanh-sinh 경로를 사용한다. JSON은 6 유효숫자이며
  절댓값 1e-11 미만을 0으로 직렬화한다. 실제 tolerance는 반올림 전 값으로 검사했다.
- historical 수치 결과를 독립 재구현으로 재현한 것이며, 이번 wrapper가 역사 원본 script를
  직접 실행했다는 뜻은 아니다. 원 candidate의 과거 실행 서술과 현재 실행 종류를 구분한다.

## Independent Mathematical Crosscheck and Disposition

기존 결과의 Independent Derivation 절을 기준으로 binodal series와 중앙 질량 대체를 직접 검산했다.
`a=Omega/(RT)=2+epsilon`, `theta_a=1/2-x`, `c=RT/F`에서
`x^2=3 epsilon/8 -27 epsilon^2/80 +1377 epsilon^3/5600+O(epsilon^4)`다.
중앙 구간의 상수 kernel 질량은 Maxwell mass와 상쇄되고, 홀함수 전위 편차의 1차 적분은 0이다.
따라서 제거/대체 차이의 선행항은
`-sqrt(6)/35 * Q*c^2*kappa''(V-U0)*epsilon^(7/2)`이며 visible gap mass의 제곱근 발산을
전체 미분으로 잘못 옮겨서는 안 된다. 이동 경계 미분항은 binodal 양 끝 전위가 U0여서 정확히 상쇄된다.
남은 stable-domain 미분 적분은 bounded kappa'에 대한 지배수렴으로 양쪽 모두
`D(V)=Q*c*integral_0^1(1-2theta)*kappa'(V-V_2(theta))dtheta`로 간다.

원 모듈을 import하지 않는 독립 45자리 계산도 실행했다. `u=log(theta/(1-theta))`,
`p=sigma(u)`, `q=sigma(c*(u+2*(1-2*p))/w)`로 바꾸면 V=U0, alpha=1에서
적분 함수는 `c*(1-2*p)*q*(1-q)*(1-2*q)*p*(1-p)/w^2`다.
mpmath 적분 구간 `[-inf,-8,-2,0,2,8,inf]`, `R=8.314`, `T=298.15`, `F=96485`, `w=.01`에서:

```text
D_U0=5.89913989674473867704663972256975902127484
footnote_units=11.7982797934894773540932794451395180425497
central_coefficient=-0.0699854212223765170913509735630254683418842
coefficient_error=1.09476e-47
PASS_INDEPENDENT_LOGIT_COORDINATE_QUADRATURE
```

중앙 계수는 `k=sqrt(3/8)`에서 `-2*integral_{-k}^k t^2*(1-t^2/k^2)^2 dt`를
직접 적분하여 `-sqrt(6)/35`와 비교했다. D 값 오차 1e-35, 계수 오차 1e-40 이하 assertion 통과.
이는 고정 매끄러운 kernel의 수학적 검산이지 문헌·재료·실험 진위 검증이 아니다.

확정 판정:

- 정규화된 비절단 kernel의 전 실수축 면적 Q, 부임계 gap 0, C0,
  좌/우 미분의 공통 D 및 조건부 C1이 유도·수치에서 일치한다.
- U13 원래의 기울기 발산 주장은 이 고정 kernel 범위에서 기각된다.
- 수정 각주의 eta=abs(a/2-1)는 abs(epsilon)/2이므로 숫자 5.90을 유지하면 2배 환산 오류다.
  eta 정의를 유지할 경우 약 11.79828 및 epsilon 구간 변환이 필요하다.
- source의 실제 물리적 채택 여부, alpha/width/temperature가 변하는 경로,
  simultaneous zero-width limit, 외부 재료/기전 진위는 이 결과의 권위 밖이다.
- finite-window area와 sampled maximum은 전축 면적 정리/연속 supremum이 아니다.
  역사적 clip kernel을 전 실수축의 정규화 kernel로 취급하지 않는다.

## Independent Review and Repair Evidence

독립 검수에서 P1 1건: 초기 runner receipt가 exit/stdout/stderr를 자체 선언하는 문제를 찾았다.
실제 success child와 failure child(exit 7) 보존 시험을 먼저 추가해 `Ran 2 tests`, 2 failures RED를 확인했다.
이후 같은 executable의 numerical child를 실행하고 CompletedProcess의 실제 returncode/stdout/stderr를
기록하도록 바꿨다. 성공에서만 summary를 추가하고 실패 exit도 그대로 보존한다.
전체 wrapper tests는 Python 3.12/3.14 각각 `Ran 10 tests`, `OK`, exit 0.
독립 검토자가 runner 1–159/test 1–111 전문 재검독과 capture 시험 두 개를 양 runtime에서 직접 실행하여
P1 해소를 확인했다. 추가 quality 결함은 미발견이다. 그 검토자의 범위에 전체 수치·Git 검증은 포함되지 않는다.

## Gate / Git Closeout / Next

Content Gate: `PASS_P068_STEP94_ASTRA_CONTENT` — 두 runtime의 실제 전체 verify에서 확인.
precommit 상태는 `CONTENT_VERIFIED_AWAITING_PUSH`다.
expected parent `58d752b63b75a4e516e76f848c1e308adeca0e03`,
subject `audit(phase068): complete Astra U13 rederivation verification`.
exact changed paths는 상세계획에 선언한 신규 6 + 갱신 4 = 10개다.

이 결과서 동결 후 두 `--verify --record-runtime` receipt가 실제 exit 0/동일 matrix 및 result identity를
가지는지 확인하고, exact path/status/mode, commit, active push/live equality, clean tree를 확인한다.
그때만 `P068_STEP94_ASTRA_PERSISTED`로 다음 Step의 원장에 기록한다.
구형 transaction validator의 `PASS_P068_STEP94_PERSISTENCE` 실행을 주장하지 않는다.

다음: Step 95 exact source/output manifest addendum 저장 후 conformance model 판정.
최종 LaTeX/PDF/zip, primary-literature/재료/held-out 검증은 아직 남아 있으며 Step 94로 해소하지 않는다.
