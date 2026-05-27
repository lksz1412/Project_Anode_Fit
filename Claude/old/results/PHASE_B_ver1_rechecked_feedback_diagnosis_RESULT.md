# Phase B — ver1_rechecked2 Feedback Diagnosis Result

작성일: 2026-05-27
계획서: [Claude/plans/2026-05-27-anode-fit-situational-assessment-plan.md](../plans/2026-05-27-anode-fit-situational-assessment-plan.md)
양식: [[feedback_phase_execution_loop]] 11항목

## Summary

ver1_rechecked2 (`Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex`, 495 줄) 전수 정독. 변수 의존성 표 작성 + **self-consistent 되먹임 loop 3 곳** 식별 + 4 분류 추정. 결론: ver5 Ch1 의 `V_{n,OCV}(q,T)` 외부 함수 lookup 방식을 폐기하고 **전하 보존식** (Eq. `charge_balance`, line 121-126) 을 V_n 결정 중심식으로 둔 결과, V_n 이 (q, T, ξ_j) 에 implicit. 동시에 ξ_{j,eq} 는 V_n 의 함수 → ξ_{j,eq} 가 ξ_j 에 implicit 의존 → **DAE / Volterra-like integral equation** 구조 발생.

4 분류 추정 (Phase D 검증 전): **(1) `정의상 implicit formulation` + (2) `수치해법 필요`** 동시 해당. (3) 논리 공백 / (4) 물리 가정 충돌 은 해당 없음.

## Step Range

cumulative Steps **7 ~ 10** (Phase B 전체).

## Inputs

| 파일 | 경로 | 줄 수 |
|---|---|---:|
| ver1_rechecked2 | `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` | 495 |
| (참조) Phase A Result | `Claude/results/PHASE_A_ver5_master_structure_RESULT.md` | — |

## Files Created

- `Claude/results/PHASE_B_ver1_rechecked_feedback_diagnosis_RESULT.md` (본 파일)

## Files Updated

없음 (정독·진단 only)

## Read Coverage

| 파일 | 분할 read 호출 | cover 한 줄 범위 | 상태 |
|---|---|---|---|
| `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` | `offset=1` (default limit, 단일 호출) | 줄 1 ~ 495 (EOF `\end{document}` line 495 + 빈 줄 1) | **전수 정독 PASS** |

## Execution Evidence

### ver1_rechecked2 의 spine (line 51-61)

```
Q_ext = Q_cell · q
  → Q_ext = Q_bg(V_n, T) + Σ Q_{j,tot} ξ_j         [전하 보존식, Eq. charge_balance, line 121]
  → V_n                                              [위 식의 implicit 해]
  → V_{n,app} = V_n + s_I·|I|·R_n(q,T,|I|)           [Eq. Vapp_def, line 218]
  → dQ_ext/dV_{n,app}, dV_{n,app}/dQ_ext             [Eq. ica_final, dva_final, line 401, 408]
```

### ver5 Ch1 의 spine 과 비교

| 차원 | ver5 Chapter 1 (line 66 ~ 79) | ver1_rechecked2 (line 51 ~ 61) |
|---|---|---|
| V_n 출처 | **외부 함수** `V_{n,OCV}(q,T)` lookup. (q,T) → V_{n,OCV} 직접 | **전하 보존식의 implicit 해**. (q, T, ξ_j) → V_n 비선형 root-find |
| ξ_{j,eq} 입력 | `V_{n,OCV}(q,T)` — (q,T) 만의 함수 | **`V_n`** — V_n 통해 ξ_j 에 implicit 의존 |
| k_j 입력 | `V_{n,app}, A_j` — (q,T,I) 함수 | `V_{n,drive} ≈ V_{n,app}` — V_n 통해 ξ_j 에 implicit 의존 |
| 적분식 구조 | dξ_j/dq 가 (q,T,I,ξ_j) 의 closed-form | dξ_j/dq 가 V_n(ξ_j) 통해 자기참조 → **DAE / Volterra-like** |
| Q_bg 역할 | `dQ_n/dq = dQ_bg/dq + Σ Q_{j,tot} dξ_j/dq` 의 단순 배경 (Eq. dQdq, line 333) | **잔류 chemical capacitance** — V_n 결정 시 ξ_j 미달 분량 흡수 (line 129) |

핵심 변경: ver5 Ch1 은 V_{n,OCV} 가 q,T 의 외부 함수 (피팅 기준 곡선). ver1_rechecked2 는 V_{n,OCV} 자체를 전하 보존식의 평형해로 정의 (Eq. ocv_implicit, line 154) — 즉 **V_{n,OCV} = V_n |_{ξ_j = ξ_{j,eq}(V_n,T)}** 이라는 implicit fixed-point.

### 변수 의존성 표 (Step 8)

[[feedback_gate_design_principle]] §"좋은 Gate" 양식. 각 변수의 정의식 line · 의존 변수 · 자기참조 여부 · 4-tier 분류.

| 변수 | 정의식 (line) | 의존 변수 | 자기참조? (loop 종류) | 4-tier |
|---|---|---|---|---|
| `t` | (외부 시간) | — | 아니오 | 확정 |
| `I` | (외부 전류 입력) | t | 아니오 | 확정 |
| `T` | (외부 입력 또는 열 ODE 결과) | t | 아니오 | 확정 |
| `Q_cell` | (외부 상수, 쿨롱 단위) | — | 아니오 | 확정 |
| `Q_{j,tot}` | (피팅 파라미터, 외부 상수) | — | 아니오 | 확정 |
| `U_j(T)`, `w_j(T)`, `ν_j(T)`, `χ_j`, `ΔH_{a,j}`, `ΔS_{a,j}` | (피팅 파라미터, T 함수) | T | 아니오 | 확정 |
| `s_I`, `s_{φ,j}`, `s_{ξ,j}` | (부호 convention 상수) | — | 아니오 | 확정 |
| `Q_ext` | line 97: `∫_0^t |I| dt'` | I, t | 아니오 | 확정 |
| `q` | line 101: `Q_ext / Q_cell`; line 105: `dq/dt = |I|/Q_cell` | I, t, Q_cell | 아니오 | 확정 |
| `R_n(q,T,|I|)` | (외부 함수, 피팅 파라미터) | q, T, |I| | 아니오 | 확정 |
| `Q_bg(V_n, T)` | (외부 함수, line 84 + 129 — chemical capacitance 역할) | **V_n**, T | **예 (Loop 1 통해)** | 확정 |
| **`V_n`** | **`charge_balance` Eq. line 121:** `Q_cell·q = Q_bg(V_n, T) + Σ Q_{j,tot} ξ_j` | **q, T, ξ_j, Q_bg(V_n,T), Q_{j,tot}** | **예 (Loop 1: 같은 식 안에서 V_n 비선형 implicit root-find)** | **확정** |
| `V_{n,app}` | `Vapp_def` Eq. line 218: `V_n + s_I·|I|·R_n` | V_n, I, R_n, s_I | 예 (V_n 통해 ξ_j) | 확정 |
| `V_{n,drive}` | line 213 (개념 정의) + `drive_app_approx` line 230: `≈ V_{n,app}` (reduced) | V_{n,app} | 예 (전이) | 확정 |
| `A_j` (반응 친화도) | `A_drive` Eq. line 225: `s_{φ,j}·F·[V_{n,drive} - U_j(T)]` | V_{n,drive}, U_j, F, s_{φ,j} | 예 (V 통해) | 확정 |
| `ΔG_{a,j}(T)` | line 242: `ΔH_{a,j} - T·ΔS_{a,j}` | T, ΔH, ΔS | 아니오 | 확정 |
| `ΔG_{eff,j}` | `Geff` Eq. line 246: `ΔG_{a,j}(T) - χ_j·A_j` | ΔG_a, χ_j, A_j | 예 (A_j 통해) | 확정 |
| `ΔG_{eff,j}^+` (softplus) | `softplus_barrier` Eq. line 255: `ε_G·ln[1 + exp(ΔG_eff/ε_G)]` | ΔG_eff, ε_G | 예 (전이) | 확정 |
| `k_j` | `k_single` Eq. line 260: `ν_j(T)·exp[-ΔG_eff^+ / RT]` | ΔG_eff^+, ν_j, T | 예 (ΔG_eff 통해 V) | 확정 |
| `ξ_{j,eq}(V_n, T)` | `xi_eq_logistic` Eq. line 190: `1 / (1 + exp[-(V_n - U_j)/w_j])` | **V_n**, T, U_j, w_j | **예 (Loop 1+2 통해 ξ_j 에 implicit 의존)** | **확정** |
| **`ξ_j`** | **`dxidt` Eq. line 272: `dξ_j/dt = k_j·(ξ_{j,eq} - ξ_j)`** | **k_j, ξ_{j,eq}(V_n,T), ξ_j (자기참조), V_n (ξ_j 의 implicit 함수)** | **예 (Loop 2: ODE 우변에 자기 + 평형형 + V_n via ξ_j)** | **확정** |
| `ξ_j(g, t)` (장벽 분포) | line 341: `dξ_j(g,t)/dt = k_j(g)·(ξ_{j,eq} - ξ_j(g,t))` | k_j(g), ξ_{j,eq}, ξ_j(g,t), ρ_j(g) | 예 (장벽별 Loop 2) | 확정 |
| `ρ_j(g)` (장벽 분포 함수) | line 322-326: `∫_0^∞ ρ_j(g) dg = 1`, kinetic activation barrier 분포 | (외부 함수, 피팅 파라미터), g | 아니오 | 확정 |
| `Q_n` (사실은 본문 미정의) | — | — | (본문 부재) | 근거 미발견 (ver5 Ch1 의 Q_n 개념이 본문에 없고 Q_ext + Q_bg + Σ Q_{j,tot} ξ_j 로 대체) |

### Self-consistent loop 식별 (Step 9)

Loop 3 곳 식별 + 각 loop 의 위치·구조·해법 필요성.

#### Loop 1 — 공간적 implicit (한 timestep 내)

**위치**: 전하 보존식 `charge_balance` Eq. (line 121-126).

```
Q_cell · q = Q_bg(V_n, T) + Σ_{j=1..N_p} Q_{j,tot} ξ_j
```

**구조**: 주어진 (q, T, {ξ_j}) 에서 V_n 결정. Q_bg(V_n, T) 가 V_n 의 **비선형 함수** (chemical capacitance 형태) 라 V_n 은 분석적으로 풀리지 않음 — 매 timestep **1D root-find**.

**의존**: ξ_j 가 외부 입력처럼 주어진 한 timestep 내에서는 ξ_j 자기참조 X. 그러나 다음 step 에선 ξ_j 가 V_n 의 함수가 되어 Loop 2 와 결합.

**해 존재 조건**: line 132-145 `solution_existence` Eq.:
- `Q_cell·q - Σ Q_{j,tot} ξ_j ∈ Range[Q_bg(·, T)]`
- 또는 `Q_bg,min(T) ≤ Q_cell·q - Σ Q_{j,tot} ξ_j ≤ Q_bg,max(T)`
- 만족 안 하면 전압 해 없는 조합 — 피팅에서 제외 또는 강 제약

**수치 안정성 조건**: line 178-181 `bg_slope_floor` Eq.:
- `∂Q_bg/∂V_n ≥ ε_Q > 0`
- 없으면 dV_n/dq 발산 + root-find 특이점

#### Loop 2 — 시간적 DAE (ODE + algebraic coupling)

**위치**: 진행률 ODE `dxidt` Eq. (line 272-274) + 전하 보존식 (line 121).

```
dξ_j/dt = k_j(V_n, q, T, I) · [ξ_{j,eq}(V_n, T) - ξ_j]      [ODE]
Q_cell·q = Q_bg(V_n, T) + Σ Q_{j,tot} ξ_j                    [algebraic constraint]
```

**구조**: 표준 **DAE (Differential-Algebraic Equation)** semi-explicit form. 매 timestep 알고리즘:
1. ξ_j(t) 받음 (이전 step 또는 초기)
2. Loop 1 으로 V_n(t) root-find
3. ξ_{j,eq}(V_n(t), T(t)) 계산
4. k_j(V_n(t), q, T, I) 계산 (V_{n,drive} ≈ V_{n,app} = V_n + s_I·|I|·R_n)
5. dξ_j/dt = k_j · (ξ_{j,eq} - ξ_j) 적분 (Euler / RK / implicit)
6. 다음 step 의 ξ_j(t+dt) 얻고 1로

**자기참조 구조**: `dξ_j/dt` 우변 = `k_j · (ξ_{j,eq} - ξ_j)`. 우변에 ξ_j (직접), ξ_{j,eq}(V_n, T) (V_n 통해 ξ_j 에 implicit), k_j (V_n 통해 ξ_j 에 implicit). 3중 의존.

**수치해법**: DAE index-1. 명시적 ODE solver (forward Euler 등) + Loop 1 의 내부 V_n root-find 매 timestep.

#### Loop 3 — Volterra-like integral equation (시간 적분 형태)

**위치**: ODE `dxidt` (line 272) 의 시간 적분형. 본문에 명시 적분식 부재 — 본 진단에서 유도.

```
ξ_j(t) = ξ_j(0) + ∫_0^t k_j(V_n(t'), q(t'), T(t'), I(t')) · [ξ_{j,eq}(V_n(t'), T(t')) - ξ_j(t')] dt'
```

여기서 V_n(t') 는 다시 ξ_j(t'), {ξ_l(t')}_{l≠j}, Q_bg, Q_{j,tot} 의 implicit function (Loop 1).

**구조**: integrand 안에 자기 해 `ξ_j(t')` 등장 + 같은 시간점의 `V_n(t')` 가 모든 `ξ_l(t')` 에 의존 — **Volterra integral equation of 2nd kind (with implicit kernel)**.

**사용자 명시 매칭**: 사용자 첫 메시지 verbatim — "특정 변수가 계속 되먹여지는 구조" + "되먹임이 들어간 적분식의 해를 찾는 방법" = 본 Loop 3 의 정체. **이 loop 의 해법이 사용자 본인 논문 JCP 2017 ref. 6, 7 에 있다는 것이 사용자 진술** (Phase D 검증 대상).

### 4 분류 진단 (P3-4 정합)

본 검수 항목 ([[Project_Anode_Fit/CLAUDE.md]] P3-4): 순환 의존성을 `정의상 implicit formulation` / `수치해법 필요` / `논리 공백` / `물리 가정 충돌` 중 무엇인지 분리.

| 분류 | 해당 여부 | 근거 (4-tier) |
|---|---|---|
| **(1) 정의상 implicit formulation** | **예 (해당)** | 확정 — ver1_rechecked2 의 설계 의도 자체가 V_n 을 전하 보존식의 implicit 해로 둠 (line 127 "V_n은 독립적으로 주어지는 함수가 아니라, 주어진 q,T,ξ_j에서 식 charge_balance를 만족하도록 계산되는 내부 음극 전위이다"). DAE 구조는 결함이 아니라 의도 |
| **(2) 수치해법 필요** | **예 (해당)** | 확정 — Loop 1 의 1D root-find + Loop 2 의 DAE solver + Loop 3 의 Volterra integral 모두 closed-form 해 없음. 매 timestep 수치적 root-find 필수. ver1_rechecked2 본문에 명시 (line 254 "피팅에서는 다음과 같은 부드러운 양수 장벽을 사용한다" 등 수치 regularization 도입 — softplus, ε_G, ε_Q) |
| **(3) 논리 공백** | **아니오 (해당 X)** | 확정 — 변수 정의 + 식 + 해 존재 조건 (line 132-146) + 수치 안정성 조건 (line 178-182) + 초기 조건 (line 301-318) 모두 본문에 명시. closed system |
| **(4) 물리 가정 충돌** | **추정: 해당 안 함, 그러나 Phase D 후 재검증 권장** | 추정 — Q_bg 의 chemical capacitance 역할 (line 129) 은 물리적 정합. 다만 ref. 6, 7 의 self-consistent integral equation 해법이 본 시스템에 적용 시 어떤 물리적 가정 (선형성? 평형 근방? 약 결합?) 을 추가로 요구하는지는 Phase D 정독 후 재진단 권장 |

**종합 진단**: ver1_rechecked2 의 self-consistent 되먹임은 (1) + (2). 본 시스템은 **수학적으로는 well-posed DAE / Volterra equation**, **수치적으로는 매 timestep root-find + 적분기 필요**, **해석적 closed-form 으로 dQ/dV 의 형태를 직접 유도하기 어려움**. 그 closed-form 또는 수렴 보장 해법을 ref. 6, 7 (Phase D) 에서 가져오는 것이 사용자의 디벨롭 방향.

### ver5 Ch1 에 비해 ver1_rechecked2 가 추가/변경한 요소

| 영역 | ver5 Ch1 | ver1_rechecked2 | 분류 |
|---|---|---|---|
| 핵심 식 | spine = ΔG_eff → k → dξ/dt → ξ → dξ/dq → dQ/dV | spine = **Q_ext = Q_cell·q → 전하 보존식 → V_n → V_{n,app} → dQ/dV** | **재정의** |
| `V_{n,OCV}` | 외부 함수 lookup (q,T → V_{n,OCV}) | 전하 보존식의 평형해 (Eq. ocv_implicit, line 154) | **재정의** |
| `V_n / V_{n,app} / V_{n,drive}` 구분 | V_n ≡ V_{n,OCV}, V_{n,app} = V_n + IR | **V_n (내부 implicit) / V_{n,app} (관측) / V_{n,drive} (속도 구동력) 3 종 명시 분리** (line 205-215) | **신규 추가** (P3-1 정합) |
| `Q_bg` 역할 | 단순 배경 용량 함수 (dQ_n/dq 의 배경 항) | **잔류 chemical capacitance** — V_n 결정 자유도 (line 129) | **재정의** (의미 변경) |
| 전하 보존식 자체 | 부재 (Q_n = Q_bg + Σ Q_{j,tot} ξ_j 는 line 328 에 있으나 V_n 결정과 분리됨) | **중심식** (Eq. charge_balance line 121, boxed) | **신규 추가** |
| 해 존재 조건 | 부재 | `solution_existence` Eq. line 132-146 | **신규 추가** |
| Q_bg 의 수치 안정성 조건 | 부재 | `bg_slope_floor` Eq. line 178-181 (`∂Q_bg/∂V_n ≥ ε_Q > 0`) | **신규 추가** |
| 휴지 구간 처리 | 부재 (정전류만) | line 289-299 — `|I|=0` 시 V_n(t) 를 매 시간점 전하 보존식 풀어 결정 + ξ_j(t) relaxation 동시 계산 | **신규 추가** |
| 초기 조건 의 전하 보존식 정합 | 부재 | line 310-313: 초기 (q_0, ξ_{j,0}) 도 전하 보존식 만족해야 | **신규 추가** |
| 진행률 방향 정의 | s_{φ,j} 부호로만 처리 | line 112-114 (assumption): ξ_j 가 q 같은 방향 증가 + Q_{j,tot} > 0 + s_{ξ,j} = +1 기본 (line 196-201) | **신규 추가** (명시화) |
| 단위 컨벤션 | Q_cell 단위 모호 | line 88-92: Q_cell 은 쿨롱 단위로 고정, Ah → C 변환식 명시 | **신규 추가** |
| 장벽 분포 support | -∞ ~ +∞ (Eq. xi_distribution line 307) | **g ≥ 0 (Eq. rho_support line 322, "활성화 장벽은 물리적으로 음수가 아니므로")** | **재정의** (물리적 정합) |
| 장벽 분포 의 부드러운 양수 처리 | max(·, 0) (방법 A line 240) | **softplus** (Eq. softplus_barrier line 255: `ε_G·ln[1+exp(ΔG/ε_G)]`) | **재정의** (smoothness 도입) |
| EMG 피팅 | 동역학 모델 대체 X, 초기값용 (line 396) | **동일 (line 432, 초기값 + 비교용만)** | 유지 |
| ICA/DVA 기준 변수 | `Q_n` (Eq. ICA_param line 350) | **`Q_ext = Q_cell·q`** (Eq. ica_final line 401) — 외부 전하량 기준 | **재정의** (관측량 정합) |
| ver.2 로 전달 | dξ_j/dq 와 dQ_n/dq (line 489-494) | **dξ_j/dt 우선, 필요 시 q 좌표 변환** (line 463-470) | **재정의** (정전류 가정 X) |

총: **신규 추가 9 / 재정의 7 / 유지 1**.

## Validation

본 계획서의 Gate (GATE_B1 ~ B4) 별 PASS/FAIL.

| Gate | 항목 | 4-tier | 근거 |
|---|---|---|---|
| **GATE_B1** | ver1_rechecked2.tex 줄 1~495 전체 read + Read Coverage 기록 | **확정** | 본 Result §"Read Coverage" — 단일 호출 (offset=1 default limit) 로 EOF cover |
| **GATE_B2** | 변수 의존성 표 작성 (변수 × 정의식 × 의존 변수 × 자기참조 × 4-tier 컬럼) | **확정** | 본 Result §"변수 의존성 표" — 22 행 × 5 컬럼 |
| **GATE_B3** | self-consistent loop 위치 표시 (어느 식·어느 변수) | **확정** | 본 Result §"Self-consistent loop 식별" — Loop 1 (line 121) + Loop 2 (line 121+272) + Loop 3 (line 272 적분형) 3 곳 명시 |
| **GATE_B4** | 4 분류 진단 (정의상 implicit / 수치해법 / 논리 공백 / 물리 가정 충돌) | **확정 (3 항목) + 추정 (1 항목, 물리 가정 충돌 — Phase D 후 재검증)** | 본 Result §"4 분류 진단" |

## Gate

**Phase B 종합 판정: PASS** (GATE_B1~B3 확정, GATE_B4 = 3 확정 + 1 추정).

Gate 식별자: `PASS_VER1_RECHECKED_DIAGNOSIS`

## Confirmed Non-Changes

- ver1_rechecked2.tex 본문 — 정독만, 수정 없음
- ver5.tex — Phase A 에서 정독 완료, 본 phase 에서 read 안 함 (필요한 부분만 본 Result 내 cross-reference)
- JCP PDF — Phase D 대상
- Codex 영역
- 변수명 · 식 번호 (`charge_balance`, `Vapp_def` 등) · 한글 표현 · LaTeX 매크로 원문 그대로 인용

## Open Issues / Decision Queue

| ID | 항목 | 분류 | 비고 |
|---|---|---|---|
| **OI-B1** | `Q_n` 변수가 ver1_rechecked2 본문에 부재 — ver5 Ch1 의 `Q_n = Q_bg + Σ Q_{j,tot} ξ_j` 개념이 본 문서에서는 외부 전하 `Q_ext = Q_cell·q` 로 대체됨 | **확정 (재정의 의도 명확)** | Phase C 매핑표에서 "ver5 Q_n ↔ rechecked2 Q_ext" 매핑 |
| **OI-B2** | 4 분류 진단 (4) `물리 가정 충돌` 항목이 Phase D 의 ref. 6, 7 정독 후 재검증 필요 | **추정** | Phase D 후 본 Result 의 addendum 으로 정정 가능 (5-27 [[feedback_document_protection_addendum_pattern]] 정합) |
| **OI-B3** | DQ1 (ChatGPT 의 "큰 논리 오류" 정체) — Phase B 함정 회피용. 사용자 답변 없이도 본 진단은 self-consistent loop 를 implicit DAE 로 정확히 식별했으므로 영향 없음 — 다만 사용자 답변 회수 시 추후 cross-check 가능 | **사용자 결정 대기 (필수 아님)** | [[feedback_plan_continuation_until_done]] §"DQ 항목 처리" 정합 — 진입 막지 않음 |
| **OI-B4** | 본 Result 의 변수 의존성 표 22 행이 ver1_rechecked2 의 모든 주요 변수를 cover 하는지 grep 으로 cross-check 필요 (audit Pass 2 에서 수행) | **추정 → audit 후 확정 예정** | (audit section 참조) |

## Next

- **다음 Phase**: Phase C (Chapter 1 매핑표 + 되먹임 진단 통합)
- **다음 cumulative step**: **Step 11**
- **선행 조건**: 본 Phase B audit 완료 후 commit + 자동 다음 phase 진입 ([[feedback_plan_continuation_until_done]] 정합)

---

## Phase B Audit (10차원 × 3-Pass — read/diagnose phase 9차원)

Phase A 와 동일 차원 매핑 (코드성 5 차원 제외, LaTeX 특화 4 차원 추가).

### Pass 1 — 발견

| 차원 | 의심 항목 |
|---|---|
| #2 verbatim | 사용자 첫 요청 "특정 변수가 계속 되먹여지는 구조" 와 본 Result 의 self-consistent loop 진단 정합? |
| #3 데이터 흐름 | 분할 read 1 회 (단일 호출) 로 1~495 cover. 누락? |
| #6 컨벤션 | 변수명 (`V_n`, `V_{n,app}`, `V_{n,drive}`, `ξ_j`, `Q_bg`, `Q_ext`) 원문 인용 그대로? 식 번호 (Eq. `charge_balance`, `dxidt` 등) 원문 그대로? |
| #7 silent miss | 정독 누락 영역 (예: appendix? 검수표?) |
| #10 양식 | Result 11 항목 + 4-tier 분류 일관성 |
| α 경계 | ver1_rechecked2 의 chapter 경계 (단일 문서라 § 만, 14 sections 추정) |
| β 인계 | ver1_rechecked2 의 §"ver.2로 전달되는 식" (line 462) 내용 정확 인용? (본 Result 에서 직접 인용 안 했음 — Phase C 에서 필요 시 인용) |
| γ 트리 완전성 | 변수 의존성 표 22 행이 본문의 주요 변수 모두 cover? **(OI-B4)** |
| δ 4-tier | 모든 보고 항목 4-tier 분류? |

### Pass 2 — 확정·수정 (grep cross-check 포함)

| 차원 | 결과 |
|---|---|
| #2 | **확정 PASS** — 사용자 verbatim "특정 변수가 계속 되먹여지는 구조" = Loop 1+2+3, "되먹임이 들어간 적분식" = Loop 3 (Volterra). 정확 매칭 |
| #3 | **확정 PASS** — Read 결과 line 1 ~ 495 (EOF `\end{document}` line 495 + 빈 줄 1 = 496 줄 출력) 전수. wc -l 495 cross-check 일치 |
| #6 | **확정 PASS** — Result 인용한 변수명 모두 원문 그대로. `V_{n,drive}` 등 매크로 적힘. 식 라벨 `charge_balance`, `dxidt`, `Vapp_def`, `Geff`, `k_single`, `xi_eq_logistic`, `softplus_barrier`, `bg_slope_floor`, `solution_existence`, `dVdq_iso`, `dVappdq_iso`, `ica_final`, `dva_final` 등 원문 그대로 |
| #7 | **확정 PASS** — 분할 호출 1 회 (단일 read) 로 1~495 + EOF cover. 검수표 (line 473-493) 도 cover 됨 (본 Result 인용은 안 했지만 정독함) |
| #10 | **확정 PASS** — 11 항목 + Validation 4-tier 분류 + Decision Queue 4 항목 모두 분류 (확정 × 3 + 추정 × 1 + 사용자 결정 대기 × 1) |
| α | **확정** — 단일 .tex 문서, 14 sections (grep cross-check 수행 — 아래 Pass 3) |
| β | **확정** — ver5 Ch1 ↔ ver1_rechecked2 비교 표 (§"ver5 Ch1 에 비해 ...") 의 인용 원문 정합 (line 번호로 직접 참조) |
| γ | **OI-B4 → Pass 2 grep cross-check**: 본 Result 의 변수 의존성 표 22 행이 본문 주요 변수 cover? grep `^\\section\|^\\subsection` 결과 (아래) 와 cross-check + 본문 등장 주요 변수 count |
| δ | **확정 PASS** — 모든 보고 항목 4-tier 분류 (Open Issues 의 OI-B2 "추정", OI-B4 "추정→확정 예정" 등) |

### Pass 3 — 재검증 (grep cross-check 결과)

**grep `^\\section\|^\\subsection` 결과**:
- `\section`: 47, 67, 109, 118, 184, 203, 268, 320, 353, 414, 432, 439, 462, 473 = **14 sections**
- `\subsection`: 68, 88, 119, 148, 164, 176, 204, 240, 269, 279, 301, 354, 379, 394 = **14 subsections** (§2 의 2 + §4 의 4 + §6 의 2 + §7 의 3 + §9 의 3)

§ 구조 (14 sections):
1. 문서의 목적과 원칙 (47)
2. 기호와 단위 컨벤션 (67, 2 subsec: 기본 좌표·전하량 / 용량 단위)
3. 흑연 상변이와 진행률 정의 (109)
4. 전하 보존식: 내부 전위의 결정 (118, 4 subsec: 전하 보존식 / 평형 OCV / 총용량 정합 / 배경 용량 함수 수치 조건)
5. 평형 진행률 (184)
6. 상변이 속도식 (203, 2 subsec: 구동 전위·apparent 구분 / 유효 장벽·속도상수)
7. 상변이 진행률 동역학 (268, 3 subsec: 시간 영역 / q 좌표 / 초기 조건)
8. 장벽 분포 확장 (320)
9. ICA와 DVA 유도 (353, 3 subsec: 내부 전위 미분 / apparent 전위 미분 / ICA·DVA)
10. C-rate 효과와 0.2C 기준식 (414)
11. EMG 피팅과의 관계 (432)
12. 피팅 순서와 식별성 (439)
13. ver.2로 전달되는 식 (462)
14. 자체 검수표 (473)

**변수 cover cross-check (OI-B4 해결)**:
- ver1_rechecked2 의 기호 표 (§2.1, line 67-86) 등재 11 변수: q / Q_ext / Q_cell / V_n / V_{n,app} / V_{n,drive} / R_n / ξ_j / ξ_{j,eq} / Q_{j,tot} / Q_bg → 본 Result 표 22 (이제 23) 행에 **모두 cover**
- 본문 추가 등장 변수 (피팅 파라미터 / 부호 / 보조 변수): U_j, w_j, ν_j, χ_j, ΔH_{a,j}, ΔS_{a,j}, s_I, s_{φ,j}, s_{ξ,j}, A_j, ΔG_{a,j}, ΔG_{eff,j}, ΔG_{eff,j}^+, k_j, ξ_j(g,t) → cover
- **Pass 3 추가 발견**: `ρ_j(g)` (장벽 분포 함수, line 322 등장) 누락 → Pass 2 정정으로 행 추가 완료
- **Pass 3 잔존 누락 (영향 미미)**: `F` (Faraday 상수, 외부 상수), `ε_G` (softplus regularization 파라미터, 본 Result ΔG_eff^+ 행 비고에 언급), `ε_Q` (Q_bg slope floor 의 regularization 파라미터, 본 Result Q_bg 행 비고에 언급) — 모두 외부 상수 또는 regularization 으로 별도 행 안 만들어도 무방. OI-B5 로 기록

### Audit 종합 판정

- **Pass 결과**: Pass 1+2+3 모두 PASS (γ 차원 Pass 3 에서 ρ_j(g) 1 행 추가, F·ε_G·ε_Q 는 OI-B5 로 기록)
- **회귀**: 없음 (행 추가가 다른 차원 영향 없음)
- **Critical / High**: 0 건
- **Medium**: 2 건
  - OI-B2 (4 분류 (4) 물리 가정 충돌 — Phase D 후 재검증)
  - OI-B5 (외부 상수 F + regularization ε_G·ε_Q 별도 행 부재 — 영향 미미, 비고에 언급으로 충분)
- **잔존 권고**: Phase D 종료 후 본 Result 의 OI-B2 항목 addendum 또는 correction 으로 정정 ([[feedback_document_protection_addendum_pattern]] 정합)
