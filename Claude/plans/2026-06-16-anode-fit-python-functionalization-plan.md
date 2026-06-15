# Anode_Fit Python 함수화 + 풀셀 분해 피팅 Plan

> 정본 식 번호 = `graphite_ica_ch1_Opus_v4.aux` 에서 추출한 권위 매핑 (named label `eq:*` ↔ PDF 렌더 번호 `(1.x)`).
> 본 계획은 코드 산출물용 — 11-section 양식의 일부 섹션 의미는 코드 작업에 맞춰 재정의(이름·순서 보존, [[feedback_plan_template_11sections]] §3 허용).

---

## Summary

**목표.** Anode_Fit Chapter 1 (graphite ICA/dQdV 이론)의 닫힌 식들을 **추적 가능한 Python 함수**로 함수화한다.
핵심 요구(사용자 2차 지시): 함수마다 ① **문건 몇번식**인지(또는 몇번식 + 몇번식의 **조합**인지) ② **어떤 가정·근사**를
적용했는지 ③ **x축을 V(전위)로 두는지 Q(용량)로 두는지** 를 상세 주석으로 명기한다.

**왜.** 직전 턴에 제공한 추상 수식이 불명확했다(사용자 "보고 이해가 잘 안된다"). 식을 말로 푸는 대신,
**문건의 닫힌 식을 1:1 직역한 Python 함수 + 식 번호·가정·축 추적 주석**으로 제공하면 검증·재사용이 가능하다.
최종 목표는 사용자 원안(1차 지시) — **상전이마다 dQ/dV peak를 가정해 풀셀을 양·음극으로 분해하는 피팅** — 을
이 함수화 위에 세우는 것이다.

**이번 계획 범위.** 계획서 → primitive 함수층 → 전이/전극 모델층 → V↔Q 변환층 → 풀셀 분해 조립층 →
단계 피팅 메소드 → round-trip 검증 → 추적표·문서화. 단일 모듈(들)로 산출, round-trip 으로 실증.

---

## Current Ground Truth

**확정 (정독·추출로 검증).**
- 정본 = [graphite_ica_ch1_Opus_v4.tex](../docs/graphite_ica_ch1_Opus_v4.tex) (18절, 식 1.1–1.103). §1.17 = 예시구현,
  §1.18 = [확장]적층. §1.1–1.17 은 v3 와 byte-identical. HEAD `c06fb81`.
- **식 번호 매핑 권위 확보** = `graphite_ica_ch1_Opus_v4.aux` (정본과 동시각 Jun 13 23:04). 핵심:
  - `(1.27)` eq:logistic ξ_eq · `(1.49)` eq:belliden ξ(1−ξ) · `(1.50)` eq:dxidV dξ_eq/dV · `(1.51)` eq:eqpeak peak 3량
  - `(1.42)` eq:charge 전하보존 · `(1.43)` eq:cbg C_bg · `(1.45)` eq:vapp V_n=V_app−s|I|R_n · `(1.47)` eq:dQdV 관측식
  - `(1.54)` eq:Lq L_q · `(1.61)` eq:rsol 꼬리감쇠 · `(1.63)` eq:tail 꼬리 dQ/dV · `(1.64)` eq:keff 유효장벽
  - `(1.68)` eq:LqT L_q(T) · `(1.69)` eq:lnLq lnL_q · `(1.70)`/`(1.71)` Arrhenius 회귀
  - `(1.76)` eq:closed · `(1.78)` eq:taildiff · `(1.79)` eq:simplefit 단일전이 닫힌식 · `(1.80)` eq:areacons 면적보존
  - `(1.82)` eq:total 다전이 합산 · `(1.88)` eq:hysdU · `(1.91)` eq:hyscenter 분기중심 · `(1.93)` eq:hysobsgap
  - `(1.94)` eq:master 방전 통합 · `(1.95)` eq:dHeff · `(1.96)` eq:hysmaster 양방향 통합
- 기존 코드 자산: [§1.17 verbatim](../results/V2_E_codeexample/graphite_ica_model.py) (단일전극 모델 직역, M1–M6),
  [round-trip](../work/ch1_fit_roundtrip.py) (S1·S5 회복 PASS). 둘 다 **반쪽전지 단일전극** 한정.
- 문건은 **반쪽전지(half-cell) 전용** — §1.1 부호규약(L273): full-cell 이면 양극 기여 제거 환산이 선행. **즉 풀셀→양·음극 분해는 문건에 없음** (= 신규 확장 자리).

**소비처 = BDD `BatteryData_Matching`** ([99_Backend.py:858](../../Project_BatteryData_Display/Lib_LKS_BatteryData_99_Backend.py#L858)).
풀셀 분해 규약: `V_FC=V_CT−V_AN`, `(dV/dQ)_FC=(dV/dQ)_CT−(dV/dQ)_AN`, `(dQ/dV)_FC=1/[(dV/dQ)_CT−(dV/dQ)_AN]`.
3채널 잔차(Volt·dVdQ·dQdV) + 단조/비음 penalty. RMSE_1→2→3→4 단계 최적화. **이 클래스는 사용자 원본·무변경**(BDD CLAUDE.md).

**미확인 (Phase 0 에서 확정).**
- 전극 OCV 곡선 `Q_e(V)` 의 적분상수·기준점 규약 (문건 (1.42) 전하보존의 Q_bg 처리와 정합).
- 양극(cathode) 모델: 음극과 동일 peak-basis 일반형으로 둘지(기본값) — 특정 화학 가정 강제 X.

---

## Phase Range

| Phase | 이름 | Steps | 산출물 |
|---|---|---:|---|
| **0** | 전제 확정 (premise lock) | 1–10 | 함수 인벤토리·축 규약·식 매핑 동결 (본 계획 Implementation Interfaces) |
| **1** | Primitive 함수층 | 11–24 | `xi_eq`·`bell`·`tail`·`ln_Lq`·`L_q/L_V`·`dU_hys`·`U_branch` (단위 구성 루프) |
| **2** | 전이·전극 모델층 | 25–34 | `peak_dQdV`(1.79)·`dQdV_app`(1.96)·`electrode_dQdV`(1.82) |
| **3** | V↔Q 변환 + 전극 OCV | 35–44 | `electrode_QV`(∫1.82 closed-form)·`invert_QV` |
| **4** | 풀셀 분해 조립 | 45–54 | `full_cell_from_electrodes`(V_FC=V_CT−V_AN, 3채널) — [확장] flagged |
| **5** | 단계 피팅 메소드 | 55–66 | `staged_fit`(P1..P5, BDD RMSE_1→4 동형) |
| **6** | Round-trip 검증 | 67–74 | 합성 풀셀 → θ* 회복 실증 (PASS gate) |
| **7** | 종합·추적표·ledger | 75–82 | 함수↔식번호↔가정↔축 추적표 · RESULT · ledger |

(step 수 = 최소 기준점, [[feedback_step_granularity_flexibility]] 확장 OK. cumulative — phase 넘어 단조 누적.)

---

## Non-goals

- **BDD `BatteryData_Matching` 백엔드 직접 수정 X** (사용자 원본·무변경 — BDD CLAUDE.md). 본 작업은 Anode_Fit 측
  **독립 reference 모듈**. BDD 슬롯-인은 별도 GO 후(신규 클래스, 백엔드 무변경).
- **정본 `.tex` 본문 식·번호 변경 X.** 함수는 문건을 **따라가는** 직역이지 문건을 고치지 않는다. (문서 보완이
  필요하면 별도 phase·별도 사용자 결정.)
- 문건 밖 새 물리 주장 추가 X. 풀셀 조립(Phase 4)은 문건의 (1.42)/(1.47)/(1.96)에서 **유도**되는 확장이며,
  유도 못 하는 부분은 `# [확장: 문건 밖]` 으로 명시 flag.
- 피팅 솔버 라이브러리 강제 X — 문건 §1.16 (5) 가중 LSQ 규정만 지키면 scipy/optuna 등 무방(BDD 와 정합).

---

## Implementation Changes

생성 산출물 (전부 신규 — 기존 파일 무수정):
- `Claude/work/anode_fit_lib.py` — **개발·검증용** 작업본(gitignore). 단위별 작성·실행.
- `Claude/results/anode_fit_python/anode_fit_lib.py` — **최종 추적 모듈**(tracked). work 검증 통과본 동기.
- `Claude/results/anode_fit_python/roundtrip_fullcell.py` — 풀셀 분해 round-trip 실증.
- `Claude/results/anode_fit_python/TRACE_TABLE.md` — 함수 ↔ 식번호 ↔ 가정/근사 ↔ V/Q축 추적표.
- `Claude/results/PHASE_PYFUNC_*_RESULT.md` + `PHASE_PYFUNC_EXECUTION_LEDGER.md` — [[feedback_phase_execution_loop]] 양식.

---

## Phase 0 — 전제 확정 (Steps 1–10)

- **입력**: 본 계획 Current Ground Truth + aux 식 매핑 + BDD 매칭 규약.
- **Step 1–4**: 함수 인벤토리 확정 (아래 Implementation Interfaces 표) — 각 함수의 출처 식·축·가정 동결.
- **Step 5–7**: 축 규약 동결 — primitive·전이·전극층 = **x축 V(전위, mV vs Li)**; 풀셀 조립층 = **x축 Q(용량, /Q_cell 또는 Ah)**; V↔Q 변환은 (1.42) 전하보존의 적분으로 명시.
- **Step 8–9**: 단위·부호 규약 동결 (s=+1 방전, σ_d 방향, mV vs V, Q_cell 정규화 — 문건 §1.1·§1.16 그대로).
- **Step 10**: Phase 0 RESULT + ledger init.
- **Gate**: 인벤토리 표의 모든 행이 (함수명·출처식번호·축·핵심가정) 4열 채워짐 + aux 번호와 1:1 대조 0 불일치.
- **중단**: 식 매핑 불일치 발견 시 STOP → Correction History.

## Phase 1 — Primitive 함수층 (Steps 11–24)

자연 단위(함수 하나)씩 [정독 출처식 → 직역 구현 → 추적 주석 → 자체 수치검산 → ledger]. 통째 배치 X.
- **Step 11–12** `xi_eq(V, U, w, s=+1)` ← **(1.27)** eq:logistic. 축: **V**. 가정: 평형 등온선(smooth, 급점프 금지).
- **Step 13–14** `bell(V, U, w, Q, s=+1)` ← **(1.50)** eq:dxidV ×Q (= **(1.49)** belliden 의 연쇄율). 축: **V**. 가정: 평형 추종(상승부), 분리 단봉.
- **Step 15–16** `ln_Lq(...)` ← **(1.69)** eq:lnLq (= **(1.54)** Lq + **(1.64)** keff + **(1.68)** LqT 의 조합). 축: 스칼라(전이당 상수). 가정: forward 극한(A≳3RT), 상수-L 동결.
- **Step 17–18** `L_V(...)` ← **(1.63)** eq:tail 의 L_V = |dV_n/dq|_qa · L_q. 축: V↔q 환산. 가정: post-peak 국소 기울기.
- **Step 19–20** `tail(V, V_a, L_V, r_a, Q, s)` ← **(1.78)** eq:taildiff (= **(1.61)** rsol 미분 = **(1.63)** tail). 축: **V**. 가정: δ-좁은 분포, 단방향 indicator, 원천 소멸.
- **Step 21–22** `dU_hys(T, Omega)` ← **(1.88)** eq:hysdU. 축: 스칼라[V]. 가정: Ω≤2RT → 0 분기(NaN 영역).
- **Step 23–24** `U_branch(...)` ← **(1.91)** eq:hyscenter. 축: 스칼라[V]. 가정: 분기 중심 = 중점 ± ½γΔU^hys.
- **Gate**: 각 함수 docstring 에 (출처식·조합·가정·축) 4항 + 1줄 수치검산(예: bell 정점 = Q/4w =(1.51)) PASS.

## Phase 2 — 전이·전극 모델층 (Steps 25–34)

- **Step 25–28** `peak_dQdV(V, tr, s=+1)` ← **(1.79)** eq:simplefit = `bell`×(1−r_a) + `tail`×(면적 (1.80)). 축: **V**. 한 전이.
- **Step 29–31** `dQdV_app(V_app, T, I, Q_cell, sigma_d, par)` ← **(1.96)** eq:hysmaster (방향형, M1–M6). = §1.17 코드 직역 + 추적주석 강화. 축: **V_app**(→V_n via (1.45)).
- **Step 32–34** `electrode_dQdV(V, transitions, Cbg, s)` ← **(1.82)** eq:total = C_bg + Σ_j `peak_dQdV`. 축: **V**. 가정: 전이 간 독립 가산.
- **Gate**: `electrode_dQdV` 배경차감 적분 = Σ Q_j (면적보존 (1.80)) 수치 검산 PASS.

## Phase 3 — V↔Q 변환 + 전극 OCV (Steps 35–44)

- **Step 35–39** `electrode_QV(V, transitions, Cbg, s)` ← **∫(1.82)** : Q_e(V)=Q_0+∫C_bg+Σ_j Q_j[(1−r_a)ξ_j +r_a(1−e^…)]. 축: **V→Q**. (∫bell=(1.27)ξ, ∫tail=포화지수 — closed-form). `# 적분상수 = (1.42) 전하보존 anchor`.
- **Step 40–44** `invert_QV(Q_target, ...)` — 단조 Q_e(V) 역함수 → V_e(Q). 축: **Q→V**. 수치 역보간(g_e≥0 보장).
- **Gate**: round-trip `invert_QV(electrode_QV(V))≈V` 잔차 < 격자분해능. `d/dV electrode_QV == electrode_dQdV` 수치 일치.

## Phase 4 — 풀셀 분해 조립 (Steps 45–54) — [확장: 문건 밖, flag]

- **Step 45–49** `full_cell_from_electrodes(Q_grid, anode, cathode, load_an, off_an, load_ct, off_ct)`:
  공통 Q축 사상(loading A·offset B, BDD `modi_Capa` 규약) → `V_FC=V_CT−V_AN`, `(dV/dQ)_FC=1/g_CT−1/g_AN`, `(dQ/dV)_FC=1/(...)`. 축: **Q**. `# [확장] (1.47)+(1.82) 전극별 + 직렬 풀셀 — 문건은 반쪽셀까지만; FC=CT−AN 은 BDD 규약·문헌 표준`.
- **Step 50–54** `fc_residual(meas, model)` — BDD 3채널(R_V·R_dVdQ·R_dQdV) + 단조/비음 penalty 미러. 축: **Q**.
- **Gate**: loading=1·offset=0·cathode=평탄 극한에서 `full_cell` 이 단일전극 (1.96) 으로 환원 확인.

## Phase 5 — 단계 피팅 메소드 (Steps 55–66)

- **Step 55–62** `staged_fit(meas, init)` — 비순환 사슬(§1.16 S0–S5 철학)의 코드판, BDD RMSE_1→4 동형:
  P1 위치+loading(종만) → P2 면적+폭 → P3 꼬리(r_a,L_V)+dQdV채널 → P4 slippage/stage손실 → P5 정밀. 각 단계 직전 동결.
- **Step 63–66** 목적함수 = 가중 LSQ(§1.16 (5)). 솔버 = scipy.optimize.minimize(단계별) 기본.
- **Gate**: 각 단계 입력=직전 동결 출력 + 자유도 1겹만 개방 확인 (공선형 차단 구조).

## Phase 6 — Round-trip 검증 (Steps 67–74)

- **Step 67–72** 알려진 θ*(양극 N_c peak + 음극 N_a peak + loading/offset)로 합성 풀셀 생성 → 잡음 1% → `staged_fit` 회복.
- **Step 73–74** 합격 기준(i): 각 파라미터 참값에서 보고 불확도 2배 이내 (기존 round-trip 기준 계승).
- **Gate (PASS/FAIL)**: 회복 PASS. FAIL 이면 단계·축·식 재점검(STOP 조건).

## Phase 7 — 종합·추적표·ledger (Steps 75–82)

- **Step 75–79** `TRACE_TABLE.md` — 전 함수 행: 함수명 | 출처식(들) | 조합방식 | 가정·근사 | x축(V/Q) | 검산.
- **Step 80–82** 최종 모듈 results/ 동기, RESULT(11항목), ledger(12-col), commit+push.
- **Gate**: 모듈 cold import + round-trip 실행 재현 + 추적표 전 함수 cover 0 누락.

---

## Implementation Interfaces

★ 본 절이 사용자 핵심 요구(추적성)의 사양이다. 모든 함수는 아래 4열을 docstring 으로 갖는다:
`(1) 출처식 번호  (2) 조합/근사  (3) 적용 가정  (4) x축 = V 또는 Q`.

**함수 인벤토리 + 추적 사양 (Phase 0 동결):**

| 함수 | 출처식 | 조합·근사 | x축 | 핵심 가정 |
|---|---|---|---|---|
| `xi_eq` | (1.27) | 단독 | **V** | 평형 등온선, smooth |
| `bell` | (1.50)=(1.49)연쇄율 | (1.27)→미분×Q | **V** | 평형 추종, 분리 단봉 |
| `ln_Lq` | (1.69) | (1.54)+(1.64)+(1.68) 조합 | 스칼라 | forward 극한 A≳3RT, 상수-L |
| `L_V` | (1.63) | L_q×|dV/dq|_qa | V↔q | post-peak 국소 기울기 |
| `tail` | (1.78)=(1.61)미분 | =(1.63) | **V** | δ-좁은 분포, 단방향, 원천소멸 |
| `dU_hys` | (1.88) | 단독 | 스칼라 | Ω≤2RT→0 분기 |
| `U_branch` | (1.91) | (1.88) 사용 | 스칼라 | 중점±½γΔU |
| `peak_dQdV` | (1.79) | `bell`(1−r_a)+`tail`r_a, 면적(1.80) | **V** | 단일 전이 |
| `dQdV_app` | (1.96) | M1–M6, (1.45)환산 | **V_app** | 양방향 통합 |
| `electrode_dQdV` | (1.82) | C_bg+Σ`peak_dQdV` | **V** | 전이 독립 가산 |
| `electrode_QV` | ∫(1.82) | ∫bell=(1.27)ξ, ∫tail=포화지수 | **V→Q** | 적분상수=(1.42)anchor |
| `invert_QV` | — | electrode_QV 역함수 | **Q→V** | g_e≥0 단조 |
| `full_cell_from_electrodes` | [확장](1.47)+(1.82) | V_FC=V_CT−V_AN | **Q** | BDD FC=CT−AN, 직렬 |
| `fc_residual` | [확장] | BDD 3채널 | **Q** | 가중 LSQ |
| `staged_fit` | §1.16 S0–S5 | P1..P5 동결사슬 | **Q** | 비순환 식별 |

**데이터 구조.** transition dict: `{'U','w','Q','r_a','L_V','V_a','Omega','gamma'}` (문건 par 규약, §1.17 그대로 + 확장).
**ledger row (12-col)**: step | phase | 함수 | 출처식 | 축 | 작업 | 빌드/실행 | 검산 | 결과 | 결함 | 사유 | next.

---

## Test Plan

- **T1 cold import**: 모듈 import 0 error.
- **T2 수치 검산(함수별)**: bell 정점=Q/4w(1.51) · dU_hys(25℃,4RT)≈54.8mV(§1.17) · 면적보존 Σ=Q_j(1.80).
- **T3 V↔Q 일관**: `d/dV electrode_QV ≈ electrode_dQdV` · `invert∘QV ≈ id`.
- **T4 환원 극한**: full_cell(loading=1,offset=0,평탄 대극) → 단일전극 (1.96) 일치.
- **T5 round-trip(핵심)**: 합성 풀셀(잡음 1%) → staged_fit 가 θ* 를 불확도 2배 내 회복 (PASS/FAIL gate).
- **T6 추적표 완전성**: 전 함수가 TRACE_TABLE 에 (출처식·가정·축) 0 누락.

## Assumptions

- "계획서부터 최종 Python 함수까지 진행" = **GO 무중단** (Stop hook 조건과 일치) — 계획 저장 후 Phase 0→7 연속 실행.
- Workflow 금지(Agent 도구만, [[feedback_flow_interruption]]). ultracode 안 넘김.
- 양극 모델 = 음극과 동일 peak-basis 일반형(기본값, 특정 화학 미고정). 다르면 사용자 1줄 정정.
- 최종 모듈 = Anode_Fit 측 독립 reference (BDD 백엔드 무변경). BDD 슬롯-인은 별도 GO.
- 풀셀 조립(Phase 4–5)은 문건 밖 확장 — 유도 가능분은 (1.47)/(1.82)/(1.42)에서 유도하고 못 닫는 부분은 `# [확장]` flag.

## Correction History

(수정 1 — 본 계획의 존재 이유) 직전 턴은 사용자 1차 지시(풀셀 분해 + RMSE 단계 추가)에 대해 **추상 수식 + 미통합 코드 스니펫**을 제시 → 사용자 "보고 이해가 잘 안된다". 본 계획은 그것을 **문건 식 1:1 직역 + 식번호·가정·축 추적 주석 + round-trip 실증**의 함수화로 재수립한다. 추상 합성(5 RMSE 단계 등)은 Phase 5 의 grounded 단계 사슬로 대체, 풀셀은 문건 밖 확장으로 명시 flag.

(수정 2 — 대상 셀 화학 정정, 2026-06-16) round-trip 양극을 임의로 NCM 으로 둔 것을 사용자 정정: **LCO 기반 핸드폰용 파우치 셀**(흑연 음극 / LCO 양극). 양극 전이를 LCO 특성(주 육방정 ~3.93V + 질서무질서 ~4.07V + 단사정 ~4.18V)으로 교체. Assumptions 의 "양극 미고정 기본값" 은 LCO 로 확정.

(수정 3 — 실행 중 식별성 발견, round-trip 으로 실증) ① loading–Q_j 공선형 → load=1 고정(peak 면적이 용량 담음). ② dV/dQ 채널 rugged landscape(sharp LCO peak) → coarse-to-fine(평활 V 거친 정렬 → dV/dQ 미세) 로 staged_fit 재구성. ③ 절대 offset ~1% softness(§1.12 비유일성) 정직 보고. ④ trf(gradient) 가 np.interp 비평활서 stall → coarse V-채널로 basin 진입 후 미세 정렬로 회피. 상세 = `results/anode_fit_python/TRACE_TABLE.md` §6.
