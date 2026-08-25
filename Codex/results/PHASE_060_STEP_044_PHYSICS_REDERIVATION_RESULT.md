# Phase 060 Step 44 Independent Physics Rederivation Result

상태: `PASS_WITH_CONCERNS`

Gate: `PASS_P060_STEP44_PHYSICS_REDERIVATION`

Phase/Step: `060/44`

활성 branch: `codex/anode-fit-v1025_2-canonical-completion`

동결 source commit: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`

직전 persistence checkpoint: Step 43 commit `7a4c1dbea22c53abe5a8dce3c3ccf58a0915e1dc`, local/upstream/origin-active 일치 및 remote verification 완료

## 1. 목표와 권위 경계

Step 44는 v1.0.19 문서의 물리·화학 수식을 production 구현과 독립적으로 재유도하고, 차원·부호·극한·국소 유일성·관측 변환·식별성·구현 영향을 판정한다. 이 Gate는 동결 source model의 내부 감사가 완료됐다는 뜻이며 다음을 확립하지 않는다.

- 외부 primary literature truth
- Graphite 또는 LCO 재료 수치의 실재성·보편성
- 실험 데이터 적합성
- canonical equation/model 채택
- Phase 071 이전의 DOI·서지 진실성

따라서 source-cited 수치, fit 초기값, 현상학적 closure와 ground-not-found 항목은 각각 분리된 authority disposition으로 유지했다.

## 2. 입력과 실제 확인 범위

### 2.1 Recovery chain

- `Codex/AGENTS.md` 1–180
- `Codex/plans/phase_planning_operations_guide.md` 1–246
- `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md` 1–665
- `Codex/plans/2026-08-25-phase060-v1019-lineage-detailed-plan.md` 1–831
- `Codex/results/PHASE_060_STEP_043_DOC_CODE_CONFORMANCE_RESULT.md` 1–324
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md` 1–217
- `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md` 1–48
- `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md` 1–89

### 2.2 Physics source coverage

동결 Git blob 31/31개, 4,544/4,544 physical lines를 1..EOF로 읽었다.

- Ch1 charge/observation/sign 담당: 14/14 files, 2,381/2,381 lines
- Ch1 LCO + Ch2 thermal/material 담당: 17/17 files, 2,163/2,163 lines
- machine coverage: 각 path의 Git blob SHA-1, blob-byte SHA-256, physical line count와 exact `1..EOF` interval
- `Claude/**` production module import/call: `false`
- `Claude/**` 수정: 없음

각 source anchor는 commit/path/start/end/blob/slice SHA-256으로 고정했다. 외부 문헌 확인은 Phase 071 소유권이므로 이 Step에서 source 서술을 primary-confirmed로 승격하지 않았다.

## 3. 독립 재유도 핵심

### 3.1 좌표·부호 분리

- `s=+1`: 삽입 반응 Gibbs 정의 전용
- `sigma_d=+1`: Ch1 Graphite half-cell 탈리튬화 방향
- Bernardi `I>0`: cell discharge; Graphite 음극에서는 lithiation
- `x`: Li 함량, `xbar=1-x`: 탈리튬화 분율
- `xi`: 탈리튬화 진행률, `theta=1-xi`: 점유율
- `U_cell=U_cat-U_an`: electrode 계수를 full-cell heat에 넣기 전 명시적 부호 조립이 필요

동일한 “discharge” 문자열이 반응 방향을 자동 결정하지 못하도록 reaction, half-cell direction, signed cell current와 control volume을 별도 상태로 고정했다.

### 3.2 Charge residual, ICA와 DVA

배경을 포함한 일반 residual은

\[
F(U;Q,T,I,\mathcal H,\mathbf p)
=Q_{\mathrm{bg}}(U)+\sum_jQ_j\xi_j(U,T,I,\mathcal H,\mathbf p)-Q=0
\]

이다. 미분 가능하고 history/독립 입력을 고정하며 `F_U != 0`인 국소 branch에서만

\[
\frac{\mathrm dU}{\mathrm dQ}=-\frac{F_Q}{F_U},\qquad
\frac{\mathrm dQ}{\mathrm dU}=F_U
\]

가 성립한다. `C_bg=dQ_bg/dV`만으로는 절대 residual에 필요한 `Q_bg` primitive와 reference-charge constant가 정해지지 않는다. `F_U -> 0`에서는 DVA reciprocal이 유한하지 않으며, monotone worked root가 일반 phase-separated/history branch의 전역 유일성을 증명하지 않는다.

### 3.3 Thermal derivative와 reversible heat

삽입 반응 convention에서

\[
\Delta G=\Delta H-T\Delta S=-FU,\qquad
\frac{\partial U}{\partial T}=\frac{\Delta S}{F}
\]

이고, `DeltaS(T)`이면 중심은 `T DeltaS(T)`의 기계적 대입이 아니라 `DeltaS/F`의 온도 적분으로 구성해야 한다. Implicit mixture에서는

\[
\left.\frac{\partial U}{\partial T}\right|_{\bar x}
=-\frac{\sum_jQ_j(\partial_T\xi_j)_U}{\sum_jQ_j(\partial_U\xi_j)_T}.
\]

`w=n(T)RT/F`이면 `dw/dT=(R/F)(n+T dn/dT)`이고, 직접 입력한 frozen `w`이면 이 항은 0이다. 두 width 상태를 합치면 안 된다. Bernardi convention의 reversible heat는 `qdot_rev=-IT dU/dT`이나 half-cell coefficient를 full-cell electrode contribution으로 사용할 때 별도 부호 map이 필요하다.

### 3.4 Regular solution, memory와 LCO electronic path

- symmetric regular solution의 real spinodal은 `Omega>2RT`; algebraic gap은 임계점에서 연속적으로 0이 된다.
- `gamma*h_eta` branch scale은 thermodynamic derivation이 아니라 현상학적·식별 불가능한 곱이다.
- semi-infinite monotone convolution은 kernel normalization, positivity, charge/discharge mirror와 small-lag limit를 만족한다.
- finite-window initialization, rest relaxation, mid-protocol reversal state transfer는 source에 상태식이 없어 `NOT_DERIVABLE/ABSENT`다.
- Eyring `k[s^-1]`에 c-rate `[h^-1]` numeric을 직접 결합한 lag seed는 정확히 3,600배 timebase ambiguity를 만든다.
- LCO Sommerfeld gate의 molar conversion에는 `N_A`와 states/eV의 eV-to-J 변환이 필요하며, `DeltaS_e=a_e T`의 중심 shift는 `a_e(T^2-T_ref^2)/(2F)`이다.
- 현행 reachable LCO path는 `x_center`와 298.15 K에 동결되어 source의 full `x,V,T`/`T^2` 경로를 구현하지 않는다.

## 4. 판정 집계

22개 derivation check 결과:

- `PASS=5`
- `FAIL=6`
- `CONDITIONAL=9`
- `UNVERIFIED=2`
- `NOT_APPLICABLE=0`

Severity finding:

- `P0=0`
- `P1=12`
- `P2=8`

10개 source conflict는 해결된 것으로 덮지 않고 `PRESERVED`했다. 독립 전문 검독에서 발견된 다음 두 항목도 초안에 추가했다.

1. charge 진행축의 signed `dQ/dV`와 positive ICA magnitude를 source가 같은 기호로 사용한다.
2. 한 절은 nonzero `gamma` hysteresis가 `I->0`에서도 남는다고 하고, 다른 절은 zero-current baseline을 direction-invariant라고 하므로 `gamma->0` 조건 없이는 직접 충돌한다.

## 5. 독립 수치 witness

- four-transition implicit root: `U_oc=74.349724 mV` at `xbar=0.25`, `T=298.15 K`
- `dQ/dU=6.176820556 Q_cell/V`
- analytic `dU/dQ=0.161895589 V/Q_cell`
- charge finite-difference absolute error: `8.672e-11 V/Q_cell`
- complete `dU/dT=-0.203949 mV/K`
- thermal finite-difference absolute error: `5.025e-15 V/K`
- `qdot_rev/I=60.807459 mV`
- lag unconverted/canonical ratio: `3600.0`
- Einstein free-energy roundtrip maximum error: `4.109e-16 V/K`
- LCO electronic gate-center `DeltaS_e=-45.964250 J/(mol K)` and `T^2` roundtrip error `1.266e-14 V/K`

이 수치 일치는 source equation 내부 왕복만 검증하며 material truth 또는 실험 재현으로 해석하지 않는다.

## 6. 생성·수정 파일

1. `Codex/work/v1019_phase060/build_phase060_step44_physics_validation.py`
2. `Codex/work/v1019_phase060/validate_phase060_step44_physics_validation.py`
3. `Codex/results/PHASE_060_V1019_PHYSICS_REDERIVATION.md`
4. `Codex/results/PHASE_060_V1019_PHYSICS_VALIDATION.json`
5. `Codex/results/PHASE_060_STEP_044_PHYSICS_REDERIVATION_RESULT.md`
6. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`
7. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
8. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`

이 8개만 Step 44 atomic commit allowlist다.

## 7. 실행 명령과 검증 결과

### 7.1 TDD RED

Artifact 생성 전 validator:

```text
FAIL missing_artifact: Codex/results/PHASE_060_V1019_PHYSICS_VALIDATION.json
FAIL_P060_STEP44_PHYSICS_REDERIVATION 0/1
RED_EXIT=1
```

### 7.2 Syntax, builder와 final validator

```text
PY_COMPILE_EXIT=0
BUILT checks=22 files=31 lines=4544 findings={'P0': 0, 'P1': 12, 'P2': 8}
BUILD_EXIT=0
PASS schema=phase060-step44-v1 checks=22 files=31 lines=4544 results=5/6/9/2/0 findings=0/12/8 conflicts=10
PASS negative_controls=49/49
PASS determinism=2/2 production_imported=false
PASS_P060_STEP44_PHYSICS_REDERIVATION
VALIDATE_EXIT=0
```

Validator는 strict duplicate-key/nonfinite parse, exact nested schemas, 31개 Git blob·line coverage, source slice hash, Step 43 exact trace mapping, enum/count/authority 경계, exact dependency edge/topology, 독립 수치 재계산과 full-probe canonical digest, builder/validator AST import·dynamic-execution policy, Markdown hash·필수 section, 49/49 controlled mutations와 임시 경로 2회 byte-identical rebuild를 강제한다.

## 8. 독립 검토

- source-side charge/observation/sign reviewer: 14/14 files, 2,381/2,381 lines; production import/call·파일 수정 없음; 결론 `P0=0/P1=3/P2=5`
- source-side thermal/LCO/material reviewer: 17/17 files, 2,163/2,163 lines; production import/call·파일 수정 없음; 결론 `P0=0/P1=4/P2=4`
- initial exact-eight SPEC review: `P0=0/P1=2/P2=1`, `NO_GO`. 실제 cycle이 아닌 두 path를 `cycles` 아래 둔 구조와 production non-import 선언만 검사한 validator 약점을 확인했다. 파일 mtime 기반 validator-before-builder 지적은 현재 파일의 delete/re-add 시각만 반영하며, 실제 실행 순서는 initial validator skeleton RED → builder source 작성 → complete validator RED → builder 최초 실행/artifact 생성이었다. 상세 계획의 강제 조건은 validator-before-final-artifact다.
- initial exact-eight QUALITY review: validator 자체는 PASS했으나, valid trace 교환·parameter disposition swap·empty graph·probe extra key/stored FD 변조·identifiability ID 변경·convention/finding 의미 훼손을 독립 in-memory mutation에서 놓쳐 `NO_GO`였다.
- corrective action: graph를 edge-contiguous `CLOSED_CYCLE` 1개와 `OPEN_PATH` 2개로 재분류하고 ordered topology를 validator가 강제한다. Reversible heat dependency는 `I_abs`가 아니라 `I_signed`, `T`, `dUdT`로 고쳤다. Exact semantic digests, probe nested schemas/stored witness, parameter/identifiability mapping, exact edge set과 AST policy를 추가하고 위 8개 mutation을 negative suite에 넣었다.
- second QUALITY probe found seven stored witness fields that exact schemas alone did not numerically bind. Logistic temperature/area, hysteresis gap, causal scale, Einstein sample temperature, LCO electronic finite difference와 unconverted lag를 독립 관계식과 full-probe canonical digest로 묶고 모두 negative suite에 추가했다.
- corrected validator: `PASS`, negative controls `49/49`, deterministic rebuild `2/2`, production import/call `false`.
- corrected exact-eight final SPEC review: `PASS / commit GO`, review finding `P0/P1/P2=0/0/0`; graph topology, validator chronology와 AST production-import gate의 이전 지적은 모두 폐쇄됐다.
- corrected exact-eight final QUALITY review: `PASS / commit GO`, review finding `P0/P1/P2=0/0/0`; 이전에 빠져나간 semantic/stored-witness 변이 15/15를 독립 재시험해 전부 검출했고, 58 numeric assertions, graph `26 nodes/35 edges/1 closed cycle+2 open paths`, exact-eight/Claude-clean/diff-check를 확인했다.

두 source reviewer의 공통 및 비중복 finding을 22개 check와 20개 severity finding에 통합했다. Reviewer가 확인하지 않은 외부 truth를 controller가 추론으로 채우지 않았다.

## 9. 확정·미결·근거 미발견

### 확정

- 동결 source 내부의 Gibbs/logistic/local implicit derivative/Einstein/regular-solution algebraic core는 명시된 가정 아래 재유도된다.
- production import 없이 독립 수치 왕복이 성립한다.
- signed ICA와 magnitude, half-cell과 full-cell current/control-volume, thermal width와 direct frozen width를 분리해야 한다.
- timebase 3,600배, background primitive, finite protocol state, full LCO electronic path의 결함 경계가 실제로 존재한다.

### 미결

- 모든 FAIL/CONDITIONAL/UNVERIFIED check의 수정·채택 disposition은 Step 45.1 소유권이다.
- 외부 primary references와 DOI 진실성은 Phase 071 소유권이다.
- 실제 material parameter 및 실험 적합성은 Phase 071/072/086 소유권이다.

### 근거 미발견

- absolute `Q_bg` reference state
- arbitrary rest/reversal history-state transfer law
- transition-specific Graphite kinetic/interaction authority
- continuous LCO DOS gate와 `Omega_cat/gamma/h_eta`의 primary-confirmed material law
- v1.0.19 source 범위의 final full-cell thermal assembly

## 10. Commit/Push checkpoint

Commit subject: `audit(phase060): rederive v1019 physics`

상태: exact-eight final review, atomic commit, push와 remote verification 전. Controller가 완료 후 이 절과 ledger/handover의 commit hash를 확정한다.

## 11. 다음 단계 조건

Step 44 exact-eight commit이 push·remote verification되고 local HEAD/upstream/origin-active가 일치하며 protected branch/main/`Claude/**`가 불변인 경우에만 Step 45.1 claim/defect/carry-forward disposition을 시작한다.
