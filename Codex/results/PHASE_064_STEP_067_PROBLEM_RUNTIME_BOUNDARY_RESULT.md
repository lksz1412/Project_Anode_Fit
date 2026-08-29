# Phase 064 Step 67 — v1.0.23 Algebraic/Volterra and Code/Runtime Boundary Result

정본일: 2026-08-29

## 1. Result Summary

- Gate: `PASS_P064_STEP67_PROBLEM_RUNTIME_BOUNDARY_WITH_CONCERNS`
- Phase/Step: `064 / 67`
- frozen baseline: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`
- expected parent: `0be2e45e56081e141fbd2f58be7a01b023ca16a3`
- expected subject: `audit(phase064): bound v1023 algebraic volterra runtime`
- containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`
- postcommit terminal: `PENDING_AT_PRECOMMIT_BY_DESIGN`
- Phase ceiling: `CONDITIONAL_P064`
- 변경 범위: `Codex/**`의 Step 67 감사 증거와 복구 문건뿐이다.
- `Claude/**` frozen source는 읽기와 저장소 밖 격리 복사만 했고 수정하지 않았다.

이 Gate는 v1.0.23의 세 수학적 문제군을 분리하고, ratio/reference 경로가 인과적 Volterra/ODE 문제에만 적용됨을 고정하며, frozen code와 내부 gate의 정적·격리-runtime 경계를 닫는다. 이 Gate는 열린 구현 결함을 해결하지 않으며, 재료·실험·외부 1차 문헌의 진실, canonical 채택 또는 출판 준비를 승인하지 않는다.

## 2. 복구 입력과 직접 확인 범위

### 2.1 복구 기준

- 활성 master plan, Phase 064 detailed plan, Step 66 result, 두 execution ledger와 active handover를 재확인했다.
- Step 66 exact-seven commit `0be2e45e56081e141fbd2f58be7a01b023ca16a3`와 `PASS_P064_STEP66_PERSISTENCE`를 Step 67 parent로 사용했다.
- Phase 063 Step 61 result 278/278행을 직접 다시 읽고, 이미 열린 code/runtime finding을 새 발견처럼 중복 발급하지 않았다.
- frozen baseline의 v1.0.23 production, primary/self-consistency gate, P1 observation script와 관련 TeX/process 기록을 Git blob identity에 묶었다.

### 2.2 Step 67 전문 검독 범위

다음 대상은 1..EOF를 직접 읽었다.

- `Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md` 225/225행
- `Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py` 1,585/1,585행
- `Claude/docs/v1.0.23/test_gates_v1023.py` 626/626행
- `Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py` 128/128행
- `Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py` 68/68행
- `Claude/docs/v1.0.23/results/comp_v23/COND_AUDIT.md` 301/301행
- `Claude/docs/v1.0.23/results/PHASE_P1_RESULT.md` 112/112행
- `Claude/docs/v1.0.23/results/PHASE_P3_RESULT.md` 102/102행
- `Claude/docs/v1.0.23/results/PHASE_P5_RESULT.md` 95/95행
- `Claude/docs/v1.0.23/results/comp_v23/AUD_REPORT_v23.md` 65/65행
- `Claude/docs/v1.0.23/results/MERGE_READINESS_v23.md` 52/52행
- `Claude/docs/v1.0.23/results/HANDOVER_v23.md` 43/43행
- `Claude/docs/v1.0.23/results/V1023_EXECUTION_LEDGER.md` 12/12행
- `Claude/docs/v1.0.23/results/V1023_CHANGE_LOG.md` 17/17행
- `Claude/docs/v1.0.23/results/qa_images/CURVE_QA_v23.md` 38/38행
- `Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex` 212/212행
- `Claude/docs/v1.0.23/_sections/ch1_sec01_n0n1.tex` 257/257행
- `Claude/docs/v1.0.23/_sections/ch1_sec06_eqpeak.tex` 89/89행
- `Claude/docs/v1.0.23/_sections/ch1_sec08_lag.tex` 145/145행
- `Claude/docs/v1.0.23/_sections/ch1_sec09_tail.tex` 245/245행
- `Claude/docs/v1.0.23/CODE_GUIDE_v23.md` 196/196행

`ch1_sec02b_part0.tex`는 Step 67에서 188–217행과 282–418행, `ch3v22_sec03_blend.tex`는 1–133행과 229–278행을 관련 구간 전건으로 다시 읽었다. 두 파일의 1..EOF 전문은 Step 64의 frozen 83-source read attestation에서 이미 닫혔다. v1.0.22 production 1,500/1,500행은 Phase 063 Step 61 전문 검독을 상속하고 Step 67 격리 비교로 다시 결속했다. Phase 064 detailed plan 586/586행도 다시 읽었다. 식·코드·runtime 판정에 직접 들어간 frozen source `14`개의 exact Git blob, SHA-256, bytes, lines와 source span은 Step 67 machine artifact가 고정한다. 여기에는 `eq:n0map` 정의와 `func_ksi_eq` 정의가 직접 포함되며, equation–code map의 각 행은 양쪽 path·line range·slice SHA-256으로 결속된다. 위 process/history 전문의 exact identity와 read extent는 Step 64 source topology/read attestation을 상속한다.

## 3. 세 문제군의 분리

### 3.1 전하보존 대수 근

평형 전하보존 반전은

\[
\sum_j Q_j\,\xi_{\mathrm{eq},j}(U_{\mathrm{oc}},T)=Q_{\mathrm{tot}}\,\bar x
\]

의 단조 대수 근찾기다. production의 `GraphiteAnodeDischargeDQDV.solve_U_oc`와 blend의 pooled `solve_U_oc`가 이 경로를 담당한다. 적분핵, 인과 기억, ratio/reference substitution 또는 전달함수는 적용 대상이 아니다.

### 3.2 배경 대수 자기일관

문건의

\[
Q_{\mathrm{cell}}q=Q_{\mathrm{bg}}(V_n)+\sum_jQ_j\xi_j
\]

도 적분핵이 없는 대수 순환이다. 다만 production은 `Cbg`를 `equilibrium`/`dqdv`의 미분용량 배경으로 한 번 더할 뿐, `solve_U_oc`에서 누적 `Q_bg(V)`를 포함하는 자기일관 대수 근을 구현하지 않는다. 따라서 문건의 배경 대수식과 code root 사이에는 구현 공백이 있으며, 이 문제를 Volterra 또는 ratio 경로로 우회할 수 없다.

### 3.3 인과 지연 Volterra/ODE

동결 기준은

\[
\frac{\mathrm d r}{\mathrm dV}=\sigma(V)-\frac{r}{L_0},\qquad
r=\xi_{\mathrm{eq}}-\xi_{\mathrm{lag}}
\]

이고, 상태의존 완화율을 복원하면

\[
\frac{\mathrm d r}{\mathrm dV}=\sigma(V)-\kappa(\xi)r,
\qquad \xi=\xi_{\mathrm{eq}}-r
\]

인 비선형 인과 ODE, 동등하게 가변상한 Volterra 문제다. `_causal_memory_pointwise`, `_causal_memory_ratio`, `_lag_ratio_geff`, `_resolve_lag_length`와 `dqdv`의 opt-in branch가 이 유일한 ratio/reference 적용 경로다.

## 4. 정적 식–코드 경계

### 4.1 interaction quantity의 non-double-count 기준

본문의 깊은 꼬리 기준은 `dH_eff = dH_a - chi_d*Omega`로 `xi -> 1`의 상수 몫을 baseline에 흡수한다. opt-in 경로는 그 baseline `L0`에 `L_loc=L0*exp[g_eff*(1-xi0)]`, `g_eff=2*chi_d*Omega/(RT)`를 곱해 기준점으로부터의 점유 편차만 복원한다. 따라서 현재 대수 구조는 같은 전체 항을 두 번 더하는 것이 아니라 `상수 기준 + 편차 복원`이다. 이 판정은 선택한 reduced-feedback hypothesis 내부의 식 정합만 뜻하며, 그 hypothesis의 외부 물리적 참을 승인하지 않는다.

### 4.2 frozen/default/opt-in 경계

- v1.0.23 기본값 `lag_ratio_correction=False`는 v1.0.22 production 실행 AST와 기본 곡선 경로를 보존한다.
- explicit `False`와 default는 `Omega>0`인 실제 lag 경로에서도 bit-exact다.
- `g_eff=0`에서 opt-in ratio와 frozen path는 bit-exact다.
- `Omega>0`과 `use_dH_eff=True`에서는 opt-in branch가 실제로 발효한다.
- ratio 결과는 frozen trajectory를 coefficient에 넣은 첫 Picard iterate일 뿐, 일반적인 정확해 또는 수렴 증명이 아니다.

### 4.3 boundary/FFT/timebase 경계

- `_causal_memory_pointwise`와 `_causal_memory_ratio`는 첫 점을 `xi_eq[0]`로 고정한다. 임의의 finite initial state를 입력하는 API는 없다.
- `transfer_apparent_from_equilibrium`은 `dV=V[1]-V[0]`만 사용하고 균일성·단조성·길이를 검사하지 않으며, zero padding 없는 discrete Fourier transform을 사용한다. 따라서 저장 구현은 주기적/circular discrete transfer이고, 비균일 격자에서 조용히 수치를 반환한다.
- transfer variable은 전압좌표의 `omega_V`다. 시간, electrochemical impedance spectroscopy (EIS), 또는 기기응답으로 승격할 수 없다.
- `curve(c_rate=...)`는 `c_rate [h^-1]` 수치를 `I_use=c_rate*Q_cell`로 넘기고, `func_L_q`는 이를 Eyring second timebase와 직접 결합한다. `/3600`이 없어 lag length가 SI-corrected route보다 정확히 3,600배 커진다. 단, 전류 $I_A=C_hQ_{Ah}$가 들어가는 IR polarization과 kinetic normalized rate $C_h/3600\,[\mathrm{s}^{-1}]$는 분리해야 하며, 전류 전체를 3,600으로 나누는 수정은 허용되지 않는다.

## 5. 격리 runtime 결과

격리 실행은 frozen Git blob만 저장소 밖 disposable directory에 byte-identical materialize하고, production module은 child subprocess 안에서만 import했다. builder와 validator process는 production module을 import하지 않았다. 모든 정본 실행은 `-B -I -X utf8`, bytecode 금지, network 미사용 조건에서 Python 3.12와 3.14로 각각 재현한다.

최종 실행 행, Python/NumPy 버전, 명령, working directory, normalized stdout/stderr digest와 독립 probe의 전 필드 값을 저장한다. 또한 runtime별 필수 행에 frozen blob, invocation, environment, input/output SHA-256, metric, tolerance, 복잡도 관찰, 저장소 전후 projection, cleanup state, authority ceiling을 모두 넣는다. 전후 projection SHA-256은 `HEAD·branch·Claude tree·Claude diff/status` 범위를 명시하며 서로 같고, 별도로 full worktree raw projection의 전후 동등성도 검사한다. 이 기록은 `PHASE_064_V1023_RUNTIME_ATTESTATION.json`에 결속된다.

두 runtime은 Python 3.12.10/NumPy 2.3.5와 Python 3.14.4/NumPy 2.5.0이며, 다음 결정적 관찰이 서로 일치했다.

| Case | 관찰 | 판정 |
|---|---:|---|
| v1.0.22 default = v1.0.23 default | `array_equal=True` | frozen-off identity |
| v1.0.23 default = explicit `False` | `array_equal=True` | option-off identity |
| `g_eff=0` ratio ON = OFF | `array_equal=True` | frozen limit |
| ratio ON liveness | max absolute delta `0.9368234388674352` | option live |
| code ratio = independent first Picard reconstruction | max absolute delta `4.440892098500626e-16` | first iterate only |
| `2 A / 2 Ah` raw rate 대 `2 A / 7200 C` SI rate | lag ratio `3599.999999999992`; current `2 A` unchanged | factor-3600 defect reproduced without corrupting IR current |
| transfer = direct voltage-coordinate DFT identity | max absolute delta `3.3306690738754696e-16` | internal identity |
| nonuniform grid | reject `False`, finite output `True` | missing guard reproduced |
| circular wrap | first output magnitude `0.09741669081543047` | unpadded periodic boundary reproduced |
| version-text mutation | self gate exit `0`, PASS | identity blind spot reproduced |
| wrong working directory | nonzero `FileNotFoundError` | cwd-relative load reproduced |
| P1 script forced CP949 | nonzero `UnicodeEncodeError` | portability gap reproduced |

공식/변조 실행은 `10/10` 기대 상태 일치, 독립 probe는 `2/2` runtime set을 통과했다. 이 수치는 내부 synthetic/runtime 범위이며 외부 물리 검증이 아니다.

## 6. Finding 및 correction register

### 6.1 P0

1. `P064-S67-F001`: C-rate `h^-1`와 kinetic `s^-1`의 `/3600` 변환이 누락돼 lag가 3,600배 과대화된다. Phase 063 `P063-S61-F001`과 Step 66 `P064-S66-CORR-001`을 재현한 동일 finding이며 신규 중복 발급이 아니다. 상태는 `OPEN_ROUTED`, owner는 Phase 076/081이다.

### 6.2 P1

1. `P064-S67-F002`: 문건의 background algebraic self-consistency root가 production `solve_U_oc`에 구현되지 않았다. `Cbg`는 미분용량에만 가산된다. `OPEN_ROUTED`, owner Phase 081.
2. `P064-S67-F003`: transfer 함수가 선언한 uniform-grid contract를 enforce하지 않고, unpadded circular DFT를 사용한다. Step 66 `P064-S66-CORR-007`의 runtime/static 확인이다. `OPEN_ROUTED`, owner Phase 081.
3. `P064-S67-F004`: lag API가 finite initial state를 받지 않고 첫 점 equilibrium/remote-past 조건만 암묵 채택한다. `OPEN_ROUTED`, owner Phase 076/081.
4. `P064-S67-F005`: self-consistency gate가 production을 script 위치가 아닌 current working directory 상대경로로 load하며 exact path/blob/version을 pin하지 않는다. `OPEN_ROUTED`, owner Phase 081.
5. `P064-S67-F006`: production 및 gate의 transfer 설명이 voltage-coordinate identity를 기기 저역통과 응답으로 승격한다. Step 66의 금지 경계와 충돌한다. `OPEN_ROUTED`, owner Phase 068/081.

### 6.3 P2

1. `P064-S67-F007`: `p1_ratio_check.py`는 UTF-8 강제 시 실행되지만 Windows CP949 기본 출력에서 수치 계산 뒤 `UnicodeEncodeError`로 종료하며 assertion/nonzero scientific gate도 없다. Step 66 `P064-S66-CORR-010`과 Phase 063 `P063-S61-F011`을 함께 보존한다. `OPEN_ROUTED`, owner Phase 081.
2. `P064-S67-F008`: P1 기록이 인용한 `scratchpad/cond_audit_verify.py`는 frozen tree에 없고, 그 수치는 재실행할 원본이 없다. `GROUND_NOT_FOUND`, owner Phase 068.
3. `P064-S67-F009`: 현재 internal tests는 오식의 양변 또는 자기참조 구현을 비교하므로 `/3600` 누락, 독립 물리식, 재료·실험 진실을 검증하지 않는다. `OPEN_ROUTED`, owner Phase 068.

finding 수는 `P0/P1/P2 = 1/5/3`이다. 모두 frozen source를 수정하지 않은 채 열린 상태로 라우팅한다.

## 7. Machine Evidence

- `Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json`
  - exact frozen source identity와 line-slice hash
  - 문제군 `3`, ratio-applicable `1`, algebraic non-applicable `2`
  - equation/code mapping, non-double-count basis, inherited finding join
  - Step 67 finding `P0/P1/P2 = 1/5/3`
- `Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json`
  - Python 3.12/3.14 isolated execution
  - frozen-off/default/explicit-False, opt-in liveness, Picard/transfer, factor-3600, path/version, CP949 mutation
  - repository-before/after identity와 external-temp cleanup

<!-- P064_STEP67_HUMAN_EVIDENCE_BEGIN -->
```json
{"algebraic_problem_classes":2,"baseline_commit":"3b5fd059ed09cdcdde38668c399cb35b8afbcca9","finding_summary":{"P0":1,"P1":5,"P2":3},"gate":"PASS_P064_STEP67_PROBLEM_RUNTIME_BOUNDARY_WITH_CONCERNS","phase_ceiling":"CONDITIONAL_P064","problem_classes":3,"ratio_applicable_classes":1,"runtime_sets":2}
```
<!-- P064_STEP67_HUMAN_EVIDENCE_END -->

## 8. Validation Contract

Validator는 다음을 독립 검증한다.

- strict duplicate-key/nonfinite/overflow/truncation JSON parse와 full recursive traversal
- 모든 frozen source의 baseline Git blob/SHA-256/bytes/lines와 exact source-slice hash
- 세 problem class, equation/code symbol, applicable/non-applicable target과 non-double-count identity
- inherited Step 61/66 finding의 exact join과 Step 67 `1/5/3` register
- external disposable materialization, child-subprocess-only production import, dual-runtime exact replay
- frozen/default/explicit-False, `g_eff=0`, opt-in liveness, first-Picard and voltage-coordinate transfer identity
- `/3600`, nonuniform-grid, wrong-cwd/path, version-string, CP949 named mutation의 exact diagnostic
- result evidence block와 네 control document의 LF-only digest
- builder deterministic reconstruction, exact-eight Git boundary, protected/main/`Claude/**` 불변

현재 artifact mode는 Python 3.12/3.14 양쪽에서 named semantic negative `63/63`(재귀적 exact JSON leaf-type projection과 bool/int/float 동치 우회 음성시험 포함), strict JSON `7/7`, disposable Git mutation fixture `10/10`, validator self-identity fixture `3/3`, strict traversal code/runtime `1,407/1,101`, source `14/14`, official/mutation run `10/10`, builder determinism `2/2`와 Gate terminal을 통과했다. Staged와 persistence mode는 exact-eight stage 및 실제 commit/push 뒤 각각 실행한다.

blocking P0/P1/P2 review defect가 하나라도 남으면 commit하지 않는다. frozen source에 기록된 열린 scientific/implementation finding은 이 Step의 commit blocker가 아니라 downstream owner가 있는 conditional ceiling 사유다.

## 9. 생성·수정 파일

1. `Codex/work/v1023_phase064/build_phase064_step67_problem_runtime_boundary.py`
2. `Codex/work/v1023_phase064/validate_phase064_step67.py`
3. `Codex/results/PHASE_064_V1023_PROBLEM_CODE_DELTA.json`
4. `Codex/results/PHASE_064_V1023_RUNTIME_ATTESTATION.json`
5. `Codex/results/PHASE_064_STEP_067_PROBLEM_RUNTIME_BOUNDARY_RESULT.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

## 10. 확정·미결·근거 미발견

### 확정

- 세 문제군은 대수 근 2개와 인과 Volterra/ODE 1개로 분리되며 ratio/reference route는 마지막 하나에만 적용된다.
- effective-barrier baseline과 local occupancy modulation은 선택한 reduced model 내부에서 상수 기준과 편차 복원으로 분리되어 같은 전체 상호작용 항을 이중 가산하지 않는다.
- 내부 option/gate의 실행 범위와 C-rate, FFT/grid, boundary, path/version, encoding 경계가 정적 source 또는 isolated runtime에 연결됐다.

### 미결

- `/3600` 수정과 단위 contract
- background algebraic root 구현 여부와 `Q_bg(V)` 정의
- finite initial-state API와 boundary contract
- uniform-grid validation, linear-versus-circular transfer policy
- self-consistency gate의 exact path/blob/version pin
- transfer 설명의 voltage-coordinate 한정
- 열린 Phase 063 current partition, capacity basis, root-domain/solver-control finding

### 근거 미발견

- `scratchpad/cond_audit_verify.py` frozen 원본
- 내부 synthetic gate를 material/experimental validation으로 승격하는 독립 근거
- 배경 대수 자기일관을 현재 production `solve_U_oc`가 실행한다는 경로

## 11. 다음 단계 조건

Step 67은 exact-eight commit/push와 `PASS_P064_STEP67_PERSISTENCE`가 확인된 뒤에만 닫힌다. 그 뒤 Step 68에서 각 내부 gate를 synthetic numerical, implementation regression, Picard/iteration, transfer identity, material, experimental, external primary-literature authority 축으로 분리한다. Step 68은 이번 runtime PASS를 외부 과학적 참으로 승격할 수 없고 열린 finding을 무단 해결 처리할 수 없다.
