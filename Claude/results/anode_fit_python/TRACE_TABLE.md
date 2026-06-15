# Anode_Fit Python 함수 추적표 (TRACE TABLE)

> 모듈 `anode_fit_lib.py` 의 각 함수가 정본 `graphite_ica_ch1_Opus_v4.tex` 의 **몇번식**(또는
> 몇번식 + 몇번식의 **조합**)인지, **어떤 가정·근사**를 취했는지, **x축이 V냐 Q냐**를 한 표로 닫는다.
> 식 번호 (1.x) = PDF 렌더 번호. 출처 = `graphite_ica_ch1_Opus_v4.aux` 의 `\newlabel` 권위 매핑.

---

## 0. 축(axis) 규약 — "x축을 V로 두는지 Q로 두는지"

본 모델에는 좌표축이 셋 있다. 함수마다 어느 축인지 표에 명시한다.

| 축 | 단위 | 무엇의 축인가 | 왜 그 축인가 |
|---|---|---|---|
| **[A] V** | mV vs Li/Li⁺ | dQ/dV 평형 peak 모델 | 관측량 dQ/dV 의 자연 축. peak 가 전위 U_j 에 **선다**. |
| **[B] q** | 무차원 q=Q/Q_cell | 동역학(꼬리) 유도 축 | 완화 ODE (1.53)·기억 커널 (1.57)·꼬리 길이 L_q (1.54) 가 q 에서 유도. 최종모델에선 \|dV/dq\| 로 V축 L_V (1.63) 로 환산·흡수. |
| **[C] Q** | q 또는 Ah | 풀셀 분해 축 | 두 전극이 같은 전하를 흘림(직렬) → V_FC(Q)=V_CT(Q)−V_AN(Q). 매칭/피팅의 축(BDD 규약). |

**[A]↔[C] 다리** = OCV 곡선 `Q(V)=∫(dQ/dV)dV` = (1.42) 전하보존 / (1.47) 관측식의 적분.
`electrode_QV` 가 V→Q, `invert_QV` 가 Q→V.

---

## 1. Primitive 함수층 (식 하나 = 함수 하나)

| 함수 | 출처식 | 조합·근사 | 가정 | x축 |
|---|---|---|---|---|
| `xi_eq(V,U,w,s)` | **(1.27)** eq:logistic | 단독. 정·역 속도 (1.25) 정지점서 회수된 logistic | 평형 등온선 smooth(급점프 금지). 폭 w: 이상 RT/F, 상호작용시 (1.32) w_eff | **V** |
| `bell(V,U,w,Q,s)` | **(1.50)** eq:dxidV ×Q | (1.49) belliden ξ(1−ξ) 에 연쇄율 s/w. dξ_eq/dV=s·ξ(1−ξ)/w | 평형 추종(상승부). 정점 Q/4w·면적 Q ((1.51)) | **V** |
| `ln_Lq(...)` | **(1.69)** eq:lnLq | **(1.54)+(1.64)+(1.68) 조합**: L_q=\|I\|/(Q_cell·k), k=Eyring 유효장벽 | forward 극한(A≳3RT, 아니면 괄호인자로 나눔). 상수-L 동결. b=−ΔS_a/R+pref | 스칼라 |
| `L_V_from_Lq(Lq,dVn_dq)` | **(1.63)** eq:tail 의 L_V | L_V=\|dV_n/dq\|_qa·L_q (★ [B]q축→[A]V축 환산) | post-peak 국소 기울기 일정 | 스칼라(V↔q) |
| `tail(V,V_a,L_V,r_a,Q,s)` | **(1.78)** eq:taildiff | =(1.61) rsol 미분 =(1.63). (r_a/L_V)e^{−(V−V_a)/L_V} | ρ_G→δ(좁은 분포)·원천 소멸·단방향 indicator. 면적 Q·r_a | **V** |
| `dU_hys(T,Omega)` | **(1.88)** eq:hysdU | 단독. spinodal 상한 | Ω≤2RT→0 분기(NaN 영역, M1) | 스칼라 |
| `U_branch(T,U,Omega,gamma,sigma_d)` | **(1.91)** eq:hyscenter | (1.88) 사용. U ± ½(h_η γ)ΔU^hys | γ=분기 축소 인자. 부분 cycle h(η)γ | 스칼라 |

## 2. 전이·전극 모델층

| 함수 | 출처식 | 조합·근사 | 가정 | x축 |
|---|---|---|---|---|
| `peak_dQdV(V,tr,s)` | **(1.79)** eq:simplefit | **bell×(1−r_a) + tail×r_a**. 면적보존 (1.80) | ρ_G→δ 실무형. 저율 r_a→0 이면 순수 종 | **V** |
| `dQdV_app(V_app,T,I,Q_cell,sigma_d,par)` | **(1.96)** eq:hysmaster | M1–M6. (1.45) V_n 환산 + (1.91)+(1.50)+(1.69)→L_q→(1.63) | §1.16 울타리 ①~⑯. 방향 σ_d 두 자리(A_d·χ_d) | **V_app** |
| `electrode_dQdV(V,transitions,Cbg,s)` | **(1.82)** eq:total | C_bg + Σ_j peak_dQdV. 합산=(1.42) 직접 미분 | 전이 독립 가산. C_bg=(1.43) | **V** |

## 3. V↔Q 변환 + 전극 OCV

| 함수 | 출처식 | 조합·근사 | 가정 | x축 |
|---|---|---|---|---|
| `electrode_QV(V,transitions,Cbg,s,Q0)` | **∫(1.82)** = (1.42)/(1.47) 적분 | ∫bell=(1.27)ξ, ∫tail=r_a(1−e^…) closed-form. 구현은 누적 사다리꼴 | g_e≥0→Q(V) 단조. 적분상수 Q0=(1.42) anchor | **V→Q** |
| `invert_QV(Q_query,V_grid,Q_of_V)` | electrode_QV 역함수 | 단조 격자 선형 보간 | Q(V) 단조(g_e≥0) | **Q→V** |

## 4. 풀셀 분해 조립 — [확장: 문건은 반쪽셀까지]

> 문건 §1.1: full-cell 이면 양극 기여 제거 환산 선행. 본 절이 그 '환산'을 명시. FC=CT−AN 은
> BDD `BatteryData_Matching` 규약·전기화학 표준(두 반쪽셀 직렬).

| 함수 | 출처식 | 조합·근사 | 가정 | x축 |
|---|---|---|---|---|
| `build_electrode_curves(...)` | electrode_dQdV (1.82) + electrode_QV | modi_Capa=load·Q_e+off, modi_dVdQ=(1/g_e)/load (BDD 규약) | ★ load 와 Q_j 공선형 → peak-basis 는 **load=1 고정**, Q_j 가 용량 담음 | **V생성→Q좌표** |
| `full_cell_from_electrodes(Q,AN,CT)` | [확장] (1.47)+(1.82) | V_FC=V_CT−V_AN, dVdQ_FC=1/g_CT−1/g_AN, dQdV_FC=1/(…) | 직렬(동일 전하), lumped(접촉저항은 R_n 별도) | **Q** |
| `fc_residual(Q,meas,AN,CT,w...)` | [확장] BDD 3채널 | R_V·R_dVdQ·R_dQdV (BDD RMSE_1/2/3 동형). 고정 길이=측정 유효점 | 가중 LSQ(§1.16 (5)). dQdV 채널 잡음 증폭 주의 | **Q** |

## 5. 단계 피팅 — §1.11 비순환 + BDD RMSE_1→4

| 함수 | 출처식 | 조합·근사 | 가정 | x축 |
|---|---|---|---|---|
| `pack_params`/`unpack_params` | — | θ ↔ (전이들 + load/off) 평탄화 | — | 혼합 |
| `staged_fit(...)` | §1.11 식별의 원칙 + §1.16 S0–S5 | **coarse-to-fine**: P1 평활 V(basin 진입)→P2 dV/dQ 미세→P3 폭. 직전 동결 | 전이 수·대략 위치 사전 anchor(저율/반쪽셀). load=1·off_an=0 gauge | **Q** |

---

## 6. ★ 핵심 식별성 발견 (round-trip 으로 실증된 가정·한계)

1. **loading–Q_j 공선형** (§1.11): peak 면적 Q_j 가 용량을 담으므로 별도 loading 은 Q_j 와 분리
   불가 → **load=1 고정**. (BD 처럼 측정 참조곡선의 임의 스케일을 쓸 때만 loading 자유.)
2. **dV/dQ 채널의 rugged landscape**: 날카로운 LCO peak(w≈12mV)은 dV/dQ 가 미세 정렬 어긋남에
   폭발적 민감 → 바늘구멍 cost. **평활한 V_FC(=적분)로 거친 정렬 먼저, dV/dQ(=미분)로 미세 정렬**
   (coarse-to-fine). 이게 BDD 가 어려운 단계에 optuna 전역탐색을 쓰는 이유.
3. **★ 전압 gauge 자유도** (정확): 모든 peak 위치를 공통 δ 만큼 이동(U_j→U_j−δ, 양·음극 동시)하면
   V_CT·V_AN 둘 다 δ 내려가 **V_FC=V_CT−V_AN 불변**. 즉 풀셀은 전극의 **상대** 위치만 결정하고
   **절대 전위 기준은 비식별**. → 반쪽셀 참조의 한 peak(예: LCO 주 3930mV)를 **anchor 로 고정**해
   gauge 잠금(`reverse_an`·anchor 미적용 시 ~15mV 균일 이동으로 드러남).
4. **음극 반전(reverse) = 물리 부호** (정확): 풀셀 충전(Q↑) 시 음극 리튬화 → V_AN **감소** → dV/dQ_AN<0
   → dV/dQ_FC=dV/dQ_CT−dV/dQ_AN 이 두 양수의 **합**(직렬 저항). 미반영 시 풀셀 dV/dQ 가 음으로
   내려가는 비물리. `build_electrode_curves(reverse=True)`(음극)로 BDD 측정 음극 곡선 방향과 일치.
5. **인접 peak 면적 비유일** (§1.12): 흑연 120/85mV 처럼 가까운 두 peak 은 합은 결정되나 개별 면적
   분배가 비유일 → 반쪽셀 참조로 면적·폭을 ±40% 구속(붕괴 방지).
6. **절대 offset(slippage) softness** (§1.12): 단일 풀셀곡선서 인벤토리 절대 offset 은 ~1% 용량 softness.
7. **비순환 staging 필수**: 전역 동시 자유 피팅은 공선형으로 발산(§1.16 "전역 동시 최소화 금지").
   자유도 점진 개방·직전 동결이 식별성을 만든다 = 사용자의 "RMSE3/RMSE4/더 많은 단계" 의 근거.

## 7. 실행 검증 (수록 코드 = 실행 파일)

- `test_anode_fit_lib.py` — T2~T4: bell 정점=Q/4w (1.51)·dU_hys=54.76mV (1.88)·면적보존 (1.80)·
  V↔Q 일관 (1.42/1.47)·풀셀 환원. **ALL PASS**.
- `roundtrip_fullcell.py` — T5: LCO/흑연 풀셀 합성(잡음 1%, 음극 reverse) → staged_fit 분해 회복.
  gauge anchor(LCO 주 peak) + 면적·폭 참조 구속. 음극·양극 peak ±4mV·면적 ±0.028, off_ct ±0.007,
  재구성 V_FC RMSE 0.73mV(≪잡음 5.9mV). **PASS**.
- `plot_samples.py` — 함수 개형 샘플 4 그림: ① 단일 peak 해부(종/꼬리/r_a/L_V) ② 세 인자(T·C-rate)
  의존 ③ 전극=peak 합 + OCV 곡선 ④ LCO/흑연 풀셀 분해(V·dV/dQ·dQ/dV, x=Q). PNG fig1~4.
