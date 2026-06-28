# v11_final 클래스 계산 진행 플로우차트 (v7 문건의 공유 척추 spine)

> 출처 = `Anode_Fit_v11_final.py` (706줄, master 전문 정독 행범위 1–706). v7 문건은 **이 진행 순서를 절 순서로** 따라 각 단계의 물리식을 *유도*한다. 코드 식별자와 1:1.

## 진입 경로 (facade → core)

```
curve(V_app, direction, c_rate, Q_cell, T, I_abs?)        [L487-512]
  ├─ direction → σ_d (+1 방전 / −1 충전)                  [_direction_to_sigma L514]
  ├─ |I| = c_rate · Q_cell   (I_abs 주면 우선)             [L507-511]
  └─→ dqdv(V_app, T, |I|, Q_cell, s=σ_d)                  [L374-484]  ★코어
```

## 코어 진행 (dqdv) — 한 곡선을 그리는 전 과정

```
[N0] 실험조건 → 모델입력 : σ_d, |I|, T(스칼라 또는 T(V) 배열), Q_cell
       │
[N1] 분극(過전압)        V_n = V_app − σ_d·|I|·R_n                      [L412]
       │                  (관측 전위에서 IR 분극을 벗겨 열역학 전위로)
       │
      작업격자 V_work(꼬리 여유 pad), grid_step, T_work, T_rep=mean     [L414-433]
      배경 baseline C_bg                                                [L431-433]
       │
   ┌── 전이 j 마다 반복 (staging transition) ────────────────────────┐ [L435]
   │                                                                    │
   │ [N2] 평형중심  U_j(T) = (−ΔH_rxn + T·ΔS_rxn)/F                     │ [func_U_j L68, 호출 L438]
   │        (또는 'U' 직접)  — 열역학(ΔG=−FU)에서 전이 전위            │
   │                                                                    │
   │ [N3] 히스테리시스 분기                                             │
   │        ΔU_hys(T,Ω) = (2/F)[Ω·u − 2RT·artanh u], u=√(1−2RT/Ω)      │ [func_dU_hys L123]
   │        Ω ≤ 2RT → ΔU_hys=0 (분리 상호작용 임계 미만)               │
   │        분기중심 U_j^d = U_j + ½·σ_d·h_η·γ·ΔU_hys                   │ [func_U_branch L133, 호출 L451]
   │        (방전/충전이 ±로 갈림; γ=0 → 분기 없음)                    │
   │        center = U_j + hys_shift                                    │ [L448-454]
   │                                                                    │
   │ [N4] 폭        w = n·RT/F   (옵션 w^eff=(RT/F)(1−Ω/2RT))           │ [func_w L64 / func_w_eff L141, _width L283]
   │                                                                    │
   │ [N5] 평형점유  ξ_eq = logistic[ σ_d·(V_work − center)/w ]          │ [func_ksi_eq L84, 호출 L459]
   │                                                                    │
   │ [N6] 평형 peak (|I|→0 한계)  Q_j·ξ_eq(1−ξ_eq)/w  = Q_j·|dξ/dV|     │ [L468]  (= equilibrium())
   │                                                                    │
   │ [N7] 동역학 지연길이 L_V  (resolver)                               │ [_resolve_lag_length L307]
   │        컷 affinity A = min(z_cut·n·RT, A_cap·RT)                   │ [L335]
   │        방향 χ_d = chi_split(χ, σ_d)  (방전 χ / 충전 1−χ)           │ [func_chi_d L155, _chi_d L291]
   │        유효장벽 ΔH_a^eff = ΔH_a − χ_d·Ω                            │ [func_dH_a_eff L149]
   │        L_q = (|I|h/Q_cell kB T)·e^{(ΔH_a^eff−χ_d A)/RT}/(1+e^{−A/RT})│ [func_L_q L90, 호출 L346]
   │        L_V = |dV/dq|_qa · L_q                                      │ [L351]
   │                                                                    │
   │ [N8] 인과 기억 꼬리  (L_V ≥ min_lag·grid_step 일 때)               │ [L466-479]
   │        ξ_lagged = causal_lowpass(ξ_eq, grid_step, L_V)             │ [_causal_lowpass L100]
   │        ★충전(σ_d<0): 격자 역전 ξ[::-1] 필터 후 [::-1]             │ [L474-477]
   │        peak_shape = (ξ_eq − ξ_lagged)/L_V                          │ [L479]
   │        (L_V 작으면 N6 평형 peak 로 환원)                           │ [L467-468]
   │                                                                    │
   │ [N9-부분]  dqdv_work += Q_j · peak_shape                           │ [L481]
   └────────────────────────────────────────────────────────────────┘
       │
[N9] 합산·역보간  dQ/dV(V_n) = interp(V_n, V_work, dqdv_work)            [L483]
       = C_bg + Σ_j Q_j[ 평형 peak − 지연 꼬리 ]
       │
      반환 dQ/dV
```

기준선: `equilibrium(V_n, T)` [L354] = C_bg + Σ_j Q_j·ξ_eq(1−ξ_eq)/w (|I|→0, 충방전 불변·히스 미반영).

## 노드 ↔ 식 ↔ v5 출처 매핑 (작가가 채울 출처 — 정독으로 확정)

| 노드 | 물리식 | v11 식별자 | v5 eq 라벨(후보·정독 확정) |
|---|---|---|---|
| N1 | V_n = V_app − σ_d|I|R_n | dqdv L412 | (master/분극 — v5 후반) |
| N2 | U_j(T)=(−ΔH+TΔS)/F | func_U_j | eq:gibbsdef·eq:mudef·eq:eqcond 계열 |
| N3 | ΔU_hys, U_j^d | func_dU_hys/func_U_branch | eq:spinodal·eq:binodal·히스 계열 |
| N4 | w, w^eff | func_w/func_w_eff | eq:weff·eq:isoslope·eq:logslope |
| N5 | ξ_eq logistic | func_ksi_eq | eq:logistic·eq:logisticsolve |
| N6 | ξ(1−ξ)/w | (인라인) | eq:gxi·eq:dxidV 계열 |
| N7 | A·χ_d·ΔH_a^eff·L_q | _resolve_lag_length 등 | eq:affinity·eq:chisum·eq:bv·eq:db·eq:kuniv·eq:lnLq(후반) |
| N8 | 인과 꼬리·충전역전 | _causal_lowpass | eq:relax·eq:stationary·eq:memory(후반) |
| N9 | Σ Q_j | interp 합산 | eq:closed/eq:total(후반) |

★커브에 *불필요*한 v5 내용(예: 순수 통계역학 유도 W·Stirling·smix 의 *세부*, lever rule·chord/cotangent 의 상평형 일반론)은 **그 결과식이 N2~N9에 쓰이는 한에서만** 최소 인용. 곡선 진행에 안 물리면 v7 범위 밖(완결성 orphan 0).

## 부호 규약 (★최우선 결함 클래스)
- σ_d = +1 방전 / −1 충전. s_I 전류부호.
- 방전: V 증가 → 탈리튬화 진행 ξ 증가. ξ_eq = logistic[σ_d(V−U)/w].
- dξ/dV peak 는 방향 불변(평형 peak 양수).
- 꼬리: 충전은 진행방향(V 감소)이 반대 → 격자 역전. 충전 dQ/dV 는 방전의 거울(양수 유지).
- 분극 부호 V_n = V_app − σ_d|I|R_n (방전 시 관측 V 가 평형보다 낮음 보정).
- ΔU_hys ≥ 0, Ω≤2RT 에서 0. ∂lnL_q/∂V < 0 (전위↑→장벽↓→꼬리↓).
