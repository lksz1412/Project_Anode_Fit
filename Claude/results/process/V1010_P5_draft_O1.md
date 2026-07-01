# V1010 P5 최종점검 감사 드래프트 — O1 (A조: code↔Ch1 상호 충실도)

> 감사자 **O1** · 조 **A조 = code↔Ch1 상호 충실도**. 감사 의견 전용 — 코드/문건 수정 X(정정·그래프는 master). 독립 작성. 추정 금지(코드 줄·tex 식 근거 병기). refute 우선·빈 통과 금지·허위적발 금지.
>
> **대상**: 코드 `docs/v1.0.10/Anode_Fit_v1.0.10.py`(740줄) · Ch1 `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex`(1932줄) · 앵커 `V1010_P4_code-revision_RESULT.md`(P5 이월)·`V1010_P1_code-audit_RESULT.md`·`GRAPH_VERIFY_RESULT.md`. Ch2 는 seam 경계 항(config)만 교차참조.
>
> **정독 커버리지(head→tail)**: 코드 전문 L1-850 · Ch1 전문 L1-1932(서론·N0~N9·sec:lco 계열·sec:signcheck·thebibliography 포함) · P4 result 전문 · P1 result Read Coverage 절 · GRAPH_VERIFY 전문. 수치 검증 = 실행(func_dSe_molar·func_U_j·seam·func_w·func_dU_hys·func_chi_d·func_dH_a_eff) 6종 재산출.

---

## 0. 감사 결론 (먼저)

- **코드↔Ch1 핵심 물리식은 양방향 1:1 대응이 성립한다** — 부호·단위·계수 어긋남 0 (아래 §1 매핑표 20식 전건 PASS, 수치 재산출 일치).
- **확정 갭 = 4건**(전부 LOW~MEDIUM, CRIT/HIGH 0): ① LCO 데이터셋 식별자 이름 불일치(`LCO_STAGING_LIT` vs `LCO_MSMR_LIT`) ② 전자항 좌표매핑 x↔ξ 미구현(Ch1 본문 서술 vs 코드 상수 x_center) ③ x_MIT 값 불일치(Ch1 0.85 vs 코드 0.50, P4 이월) ④ tab:nodemap N1 줄번호 오기(L408 vs 실제 L430).
- **근거 미발견/추정 = 2건**: Ch1 eq:lco-decomp config 항 부호 표기(Ch1 인라인 L1698 vs Ch2·코드) — Ch2 가 정합 해소하므로 Ch1 인라인만 outlier(추정 등급). / Ch1 z_cut 서술이 코드 docstring 보다 정밀(code→Ch1 비대칭, 결함 아님).
- **최중대 갭** = ① 식별자 이름 불일치(`LCO_STAGING_LIT`) — Ch1 4곳(L312·L322 caption·L1750·L1844 nodemap)이 코드에 없는 심볼을 지시하므로 "이 문건만으로 코드 재현" 시 즉시 실패. 단 물리·구조는 무결.

---

## 1. 양방향 매핑표 (Ch1 식 ↔ 코드 심볼)

### 1-A. Ch1 → 코드 (각 핵심 식이 코드에 1:1 있나)

| # | Ch1 식(라벨·줄) | 코드 심볼(줄) | 부호·단위·계수 | 판정 |
|---|---|---|---|---|
| 1 | 분극 $V_n=V_\app-\sigma_d|I|R_n$ (eq:vn, L368) | `V_n = V_in - sigma_d*I_abs*self.Rn` (L430) | 부호 σ_d 일치·[V] | **PASS** |
| 2 | 평형 중심 $U_j=(-\Delta H+T\Delta S)/F$ (eq:Uj, L448) | `func_U_j`: `(-dH_rxn + T*dS_rxn)/F` (L78-79) | 분자 부호·÷F 일치 | **PASS**(수치: gr U(298) 4전이 sub-mV 정합) |
| 3 | 분기 gap $\Delta U_\hys=\frac{2}{F}[\Omega u-2RT\,\mathrm{artanh}\,u]$, $u=\sqrt{1-2RT/\Omega}$ (eq:dUhys, L610) | `func_dU_hys` (L133-140)·死 `func_U_j_hys` (L82-91) | 2/F·계수 일치·Ω≤2RT→0 분기 | **PASS**(수치: Ω=12000→86.7mV·Ω=2RT→0) |
| 4 | 분기 중심 $U_j^d=U_j+\tfrac12\sigma_d h_\eta\gamma\Delta U_\hys$ (eq:Ubranch, L630) | `func_U_branch`: `U_j+0.5*sigma_d*h_eta*gamma*func_dU_hys` (L143-148) | ½·σ_d·h_η·γ 일치 | **PASS** |
| 5 | 폭 $w_j=n_jRT/F$ (eq:wbase, L714) | `func_w`: `n*R*T/F` (L74-75)·`_width`/`_n_factor` (L294-306) | nRT/F·'n'>'w'>1 역산 일치 | **PASS**(수치: n=1→25.7mV) |
| 6 | 평형 점유 $\xi_\eq=1/(1+\exp[-\sigma_d(V-U^d)/w])$ (eq:xieq, L770) | `func_ksi_eq`: `np.where(z>=0,...)` (L94-97) | σ_d 부호·오버플로 분기 동일 | **PASS** |
| 7 | 평형 peak $Q_j\xi_\eq(1-\xi_\eq)/w$ (eq:eqpeak, L1185) | `ksi_eq*(1-ksi_eq)/w` (L388·486) | 방향 불변·÷w 일치 | **PASS**(면적 DC=1) |
| 8 | 컷 affinity $\mathcal A=\min(z_\mathrm{cut}n_jRT, A_\mathrm{cap}RT)$ (eq:Acut, L1428) | `A=min(z_cut*n_safe*R*T, A_cap*R*T)` (L353) | σ_d 를 크기서 뺌(원본 버그 정정) 일치 | **PASS** |
| 9 | 전달계수 $\chi_d$: 방전 χ/충전 1−χ (eq:chid, L1441) | `func_chi_d`: `chi if sigma_d>=0 else 1-chi` (L158-163) | 합-1 거울 일치 | **PASS** |
| 10 | 유효장벽 $\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ (eq:dHeff, L1450) | `func_dH_a_eff`: `dH_a-chi_d*Omega` (L152-155) | −χ_d·Ω 일치 | **PASS**(수치: 48000−3000=45000) |
| 11 | 용량축 $L_q=\frac{T_*}{T}\frac{e^{(\Delta H_a^\eff-T\Delta S_a)/RT}}{1+e^{-\mathcal A/RT}}e^{-\chi_d\mathcal A/RT}$, $T_*=|I|h/(Q_\cell k_B)$ (eq:Lqfull, L1467) | `func_L_q`: `ln(T_attempt/T)-ln(1+e^{-A/RT})+dG_a/RT-x*A/RT` (L100-107) | 4항 로그·T_attempt=T_* 일치 | **PASS** |
| 12 | 전압축 $L_V=|dV/dq|_{q_a}L_q$ (eq:LV, L1480) | `abs(dVdq_qa)*L_q` (L369) | 절댓값·환산 일치 | **PASS** |
| 13 | 지수기억 이산 저역통과 $\xi_\mathrm{lag,i}=\rho\xi_\mathrm{lag,i-1}+(1-\rho)\xi_\eq$, $\rho=e^{-\Delta_\mathrm{grid}/L_V}$ (eq:lowpass, L1526) | `_causal_lowpass`: lfilter `[1-ρ]/[1,-ρ]` or 루프 (L110-128) | 계수·초기상태 일치 | **PASS** |
| 14 | peak_shape $=(\xi_\eq-\xi_\mathrm{lag})/L_V$ (eq:peakshape, L1565)·분기 스위치 $L_V<\nu\Delta_\mathrm{grid}$ (eq:branch, L1576) | `(ksi_eq-occ_lagged)/lag_len_V` (L497)·`min_lag_grid_steps*grid_step` 게이트 (L484) | ν=2·문턱 일치 | **PASS** |
| 15 | 충전 격자 역전 `lowpass(ξ[::-1])[::-1]` (eq:reversal, L1594) | `_causal_lowpass(ksi_arr[::-1],...)[::-1]` (L495) | σ_d<0 역전 일치 | **PASS** |
| 16 | 합산 $\frac{dQ}{dV}=C_\bg+\sum_jQ_j[\text{peak\_shape}_j]$ (eq:sum, L1649) | `dqdv_work += tr['Q']*peak_shape`·`np.interp` (L499·501) | 선형합·역보간 일치 | **PASS** |
| 17 | LCO 전자엔트로피 골 $\Delta S_{e,j}^\mathrm{mol}=-\tfrac{\pi^2}{3}R(k_BT/e_V)(g_\max/\Delta x_\mathrm{MIT})\sigma(1-\sigma)$ (eq:dSegate+eq:dSemolar+eq:gunit, L1082·L1018·L1027) | `func_dSe_molar`: `-(π²/3)*R*(kB*T/EV_TO_J)*(g_max_eV/dx_MIT)*gate` (L170-185) | leading −·÷e_V·R·k_B 몰당 일치 | **PASS**(수치: −45.66 ≈ Ch1 −46) |
| 18 | 전자비열·직접 두 경로 $S_e=\tfrac{\pi^2}{3}k_B^2Tg(E_F)$ (eq:Se L971·eq:Sedirect L983) | (유도 근거 — 코드는 미분형 eq:dSegate 만 구현; 상위식은 문건 유도) | 함수형 근거 성립 | **PASS**(코드는 골 미분형만 필요) |
| 19 | LCO ∂U/∂T=$\Delta S_\rxn^\mathrm{cat}/F$·MSMR 동형 f↔−σ_d (eq:lco-dUdT L474·eq:msmr L1739) | `LCOCathodeDQDV`(σ_d 뒤집기 없음, L641-671)·`func_U_j` 공용 | 부호 골격 흑연 동일 | **PASS** |
| 20 | config 봉우리내부 $+(R/F)\ln[\xi/(1-\xi)]$ (Ch2 eq:dVdT_config L236, Ch1 eq:lco-decomp 경유) | `entropy_coefficient`: `(R/F)*np.log(xi_c/(1-xi_c))` (L571) | Ch2 와 일치(Ch1 인라인 표기는 §2 갭2 참조) | **PASS**(Ch2 기준) |

### 1-B. 코드 → Ch1 (각 함수가 Ch1 식에 근거 있나)

| 코드 심볼(줄) | Ch1 근거(라벨) | 판정 |
|---|---|---|
| `func_w` (L74) | eq:wbase | 근거 O |
| `func_U_j` (L78) | eq:Uj | 근거 O |
| `func_U_j_hys` (L82, **死코드**) | eq:dUhys·eq:Ubranch 물리 동일(P1 확정 死) | 근거 O(단 Ch1 notation 은 func_dU_hys/func_U_branch 를 매핑 — 死 심볼엔 직접 앵커 없음, 정상) |
| `func_ksi_eq` (L94) | eq:xieq | 근거 O |
| `func_L_q` (L100) | eq:Lqfull | 근거 O |
| `_causal_lowpass` (L110) | eq:lowpass·eq:memory | 근거 O |
| `func_dU_hys`·`func_U_branch` (L133·143) | eq:dUhys·eq:Ubranch | 근거 O |
| `func_dH_a_eff` (L152) | eq:dHeff | 근거 O |
| `func_chi_d` (L158) | eq:chid | 근거 O |
| `func_dSe_molar`·`EV_TO_J` (L170·167) | eq:dSegate·eq:gunit | 근거 O |
| `_effective_dS_rxn`(seam) (L533·655) | eq:lco-decomp·sec:lco-code (ii) "한 줄 plug-in" | 근거 O(seam 은 아키텍처 — Ch1 서술과 정합) |
| `equilibrium` (L372) | eq:eqpeak·L1818 "히스 미반영 baseline" | 근거 O(히스 shift 미적용 — Ch1 정합) |
| `dqdv` (L392) | eq:hysmaster·전 N1~N9 | 근거 O |
| `curve`·`_direction_to_sigma` (L505·598) | eq:n0map | 근거 O |
| `LCOCathodeDQDV`·`LCO_MSMR_LIT` (L641·621) | eq:msmr·tab:lco-staging | **근거 O·이름 갭**(§2 갭1) |
| `entropy_coefficient`·`reversible_heat`·`irreversible_heat` (L544·578·588) | **Ch2** eq:weighted·eq:qrev (A조 범위 밖 — B조) | (B조 이관) |

**소결**: A조 범위 20식 전건 부호·단위·계수 정합. 死 `func_U_j_hys` 는 활성 `func_dU_hys`/`func_U_branch` 로 대체됐고 Ch1 도 활성 심볼만 매핑하므로 orphan 아님(死코드 보존은 P4 방침).

---

## 2. 확정 갭 (위치·무엇이·맞는 형태 — master 정정용)

### 갭1 [MEDIUM·확정] LCO 데이터셋 식별자 이름 불일치 — 최중대
- **무엇이**: Ch1 은 LCO 전이 초기값 리스트를 `LCO_STAGING_LIT` 로 지칭(4곳). 코드 실 심볼은 `LCO_MSMR_LIT`.
- **위치**: Ch1 L312("`LCO_STAGING_LIT` 로 둔다")·L322(tab:lco-staging caption "초기값 `LCO_STAGING_LIT`(3건...")·L1750(sec:lco-code (i) "`GRAPHITE_STAGING_LIT`→`LCO_STAGING_LIT`")·L1844(tab:nodemap N0' "`LCO_STAGING_LIT`(3 전이)"). 코드 L621 `LCO_MSMR_LIT = [...]`·L27-31 demo 도 `LCO_MSMR_LIT`.
- **맞는 형태**: 한쪽으로 통일. 코드 헤더·MSMR 동형 서술(코드 L615-618)이 "MSMR" 명명을 뒷받침하므로 **Ch1 4곳을 `LCO_MSMR_LIT` 로 통일**하는 편이 코드 변경 0(死코드·식별자 보존 방침 부합). 또는 코드를 `LCO_STAGING_LIT` 로 변경(단 demo_lco_heat.py L27-31 동반 수정 필요).
- **영향**: 물리·구조 무결. "문건만으로 재현" 실행 시 `AttributeError`. tier = 확정.

### 갭2 [MEDIUM·확정] 전자항 좌표매핑 x↔ξ 미구현 (Ch1 본문 서술 vs 코드 상수)
- **무엇이**: Ch1 sec:lco-code (ii)·"Ch2/P4 코드 구현 예고 (i) 좌표 매핑"(L1725-1729)은 전자항을 **$x=x(\xi_{\eq,1}(V))$ 매핑으로 V 격자 위에서** 평가한다고 서술("게이트 인자에 x=x(ξ_eq,1(V))를 대입해 V 격자 위에서 ΔS_e를 평가"). 코드는 `func_dSe_molar(tr['x_center'], T_ref, ...)` 로 **고정 상수 x_center=0.50** 에서 평가(L669)하고, T_ref=298.15 동결 상수 오프셋으로 seam 에 가산.
- **위치**: Ch1 L1725-1729(좌표매핑 서술)·L1752-1756(sec:lco-code (ii) plug-in). 코드 L655-671(`LCOCathodeDQDV._effective_dS_rxn`)·L666-670.
- **맞는 형태**: 두 방향 중 택1 — (a) Ch1 이 이미 이를 "★Ch2/P4 코드 구현 예고(두 설계 항목)"(L1724)·"다온도 round-trip 피팅 단계의 과제로 분리(P4 미구현, 라벨)"(코드 L664)로 **명시 defer** 했으므로, Ch1 sec:lco-code (ii) 에 "현 P4 구현은 x_center 상수 동결(단일-기준 근사), x↔ξ 매핑은 다온도 round-trip 단계"라는 현상태 라벨을 1문장 보강해 본문 서술과 코드 현상태를 명시 정합. (b) 또는 코드에 x↔ξ_eq,1(V) 매핑 구현(P4 이월 다온도 과제 — 범위상 지금 아님).
- **영향**: 단일온도·단일조성 대표값에선 무결(P4 gate PASS). 다조성 dQ/dV 곡선상 전자골의 x-의존 위치가 상수로 고정됨. tier = 확정(단 Ch1 이 defer 라벨 보유 → HIGH 아님).

### 갭3 [LOW·확정·P4 이월] x_MIT 값 불일치 (Ch1 0.85 vs 코드 0.50)
- **무엇이**: Ch1 eq:ggate(L1070)·정당화 (ii)(L1098)는 $x_\mathrm{MIT}\approx0.85$(MIT 2상역 x≈0.75-0.94 중앙). 코드 `LCO_MSMR_LIT` T1 전이는 `'x_MIT': 0.50, 'x_center': 0.50`(L632).
- **위치**: Ch1 L1070·L1098·L1146(그림). 코드 L631-632. P4 result §11 이월 명시("x_MIT=0.50 tier-C placeholder ... Ch1 anchor x_MIT≈0.85·플래토 x≈0.75-0.94와 불일치(내부 정합이나 문서)").
- **맞는 형태**: round-trip 피팅 단계서 물리값(≈0.85)으로 정정. 현재는 **tier-C placeholder 라벨 확인만** — 코드 L619-620 이 "tier-C 시연 기본값 — round-trip 피팅 前 placeholder(실측 신뢰값 아님)"로 라벨 보유하므로 label 정합은 성립(§3 참조). 문서-문서(코드 주석 vs Ch1 anchor) 수치 불일치만 잔존.
- **영향**: 시연 dQ/dV 정상(전자골이 T1 구간 내 위치). 신뢰값 아님. tier = 확정(P4 이월, 정정은 피팅 단계).

### 갭4 [LOW·확정] tab:nodemap N1 줄번호 오기
- **무엇이**: Ch1 tab:nodemap(L1832) N1 행이 분극식을 `dqdv L408` 로 지시. 코드 실제 분극 줄 = L430(`V_n = V_in - sigma_d*I_abs*self.Rn`). L408 은 dqdv docstring 내부(가드 서술).
- **위치**: Ch1 L1832. 코드 L430.
- **맞는 형태**: Ch1 tab:nodemap N1 코드식별자를 `dqdv L430` 으로 정정(또는 줄번호 제거·`dqdv` 만).
- **영향**: 미미(참조 편의). tier = 확정.

---

## 3. 공통 산출 — 3대 무결 + P4 이월 문서 정합

### 3-A. 3대 무결 최종 확인 (A조 범위)
1. **물리 배경 정확** — Ch1 유도 원천(Gibbs→평형조건 eq:eqcond → eq:Uj / 격자기체 이중웰→spinodal eq:spinodal→eq:dUhys / Eyring detailed balance eq:db→logistic eq:xieq / 지연 ODE eq:memory→eq:lowpass / Sommerfeld eq:Se·eq:Sedirect 2경로 교차검증)이 결과박스로 단계적 수렴. 부호 사슬 sec:signcheck S1~S8 + R1~R5 self-test 전건 PASS. **무결 확정**.
2. **코드 정확** — §1 매핑 20식 전건 부호·단위·계수 정합. 수치 재산출 6종(func_dSe_molar −45.66·gr U(298) 4전이·LCO U(298) 3전이·func_w 25.7mV·func_dU_hys 86.7mV·func_dH_a_eff 45000) Ch1 검증값 일치. seam base `_effective_dS_rxn(tr) is tr['dS_rxn']` = True (흑연 byte 0-diff 보장). **무결 확정**.
3. **사용자 의도 반영** — "흑연 forward 교과서가 LCO 양극까지 한 틀로(파라미터 교체+전자항 1항)" 통합 의도가 Ch1 sec:lco-map·sec:lco-code 서술과 코드 `LCOCathodeDQDV` 상속(override=`_effective_dS_rxn`만, σ_d 뒤집기 없음)에 일관 반영. "모든 인자 입력 노출·하드코딩 0" 의도 = tab:inputs(L1773-1799) ↔ 생성자/전이dict 키 전수 대응. **무결 확정**.

### 3-B. P4 이월 4항 문서 정합·라벨 확인
| P4 이월(result §11) | Ch1·코드 라벨 상태 | 판정 |
|---|---|---|
| x_MIT=0.50 tier-C placeholder | 코드 L619-620·L675 "tier-C 시연·placeholder·신뢰값 아님" 라벨 O / Ch1 anchor 0.85 (갭3) | **라벨 O·수치 불일치 잔존**(갭3) |
| 다온도 T² 곡률(Sommerfeld T-스케일·eq:U1T2 ½=a_e/2F) | 코드 L663-664 "다온도 round-trip 피팅 과제로 분리(P4 미구현, 라벨)" O / Ch1 L1049-1061 eq:U1T2 유도·L1724 "P4 코드 구현 예고" defer O | **라벨 정합 O**(단일-기준 동결 근사 명시) |
| LCO 시연 파라미터 tier-C | 코드 L619-620 라벨 O / Ch1 L315-317·L494 "신뢰값 아니라 초기값·tier 병기·피팅 override" O | **라벨 정합 O** |
| 비가역 3분해(I²R+Iη_ct+Iη_diff) | 코드 L588-596 "lumped만·3분해는 Ch2 boxed 부재·근거 미발견 옵션 분리" (Ch2 범위 = B조) | **A조 범위 밖(B조)** |

**소결**: P4 이월 4항 중 3항 라벨 정합 확인(코드·Ch1 양쪽 defer 라벨 보유). x_MIT 수치만 code주석↔Ch1 anchor 불일치(갭3). 비가역 3분해는 Ch2/B조 이관.

---

## 4. 근거 미발견/추정 (4-tier 하위)

### 추정1 [추정] Ch1 eq:lco-decomp config 항 부호 인라인 표기 (Ch1 outlier)
- Ch1 L1698 은 config 봉우리내부 항을 "$R\ln[(1-\xi)/\xi]$ 가 ... 따라 나온다"로 인라인 표기. 이는 부호상 $-R\ln[\xi/(1-\xi)]$ 와 등가.
- 그러나 **Ch2 eq:dVdT_config(L236)·eq:dSconfig(L226-227)** 는 $\partial S_\config/\partial\theta|_{\theta=1-\xi}=-R\ln[(1-\xi)/\xi]=+R\ln[\xi/(1-\xi)]$ 로 명시 정합하고(Ch2 L241-242), **코드 L571** `(R/F)*log(xi_c/(1-xi_c))` = $+(R/F)\ln[\xi/(1-\xi)]$ 로 Ch2·부호 일치.
- **판정(추정)**: Ch1 L1698 인라인의 argument `(1-ξ)/ξ` 가 부분몰 config 엔트로피 $\partial S_\config/\partial\theta$(=−R ln[θ/(1−θ)], θ=1−ξ ⇒ −R ln[(1−ξ)/ξ])를 leading −없이 적어, ∂U/∂T 로 들어갈 때의 부호(+R ln[ξ/(1−ξ)])와 표면상 반대로 읽힐 소지. Ch1 은 "config 엔트로피의 부분몰 형태"를 서술 중이고 ∂U/∂T 항으로 옮길 때 부호가 맞물림을 Ch2 가 명시하므로 **물리 오류는 아니나 Ch1 인라인 단독으로는 부호 방향이 모호**. master 판단 권장 — Ch1 L1698 을 Ch2·코드와 동형인 `$+R\ln[\xi/(1-\xi)]$`(∂U/∂T 기준) 또는 leading − 명시(`$-R\ln[\xi/(1-\xi)]$` = S_config 미분 기준)로 통일하면 삼자(Ch1·Ch2·코드) 표기 일치. **근거미발견 아님(Ch2 로 해소됨) — Ch1 인라인 표기 정밀화 제안 등급.**

### 추정2 [확정·결함 아님] z_cut 서술 code→Ch1 정밀도 비대칭
- 코드 docstring L239 는 z_cut 을 "ξ_eq 5%" 로 적음(P1 확정: 부정확 — 실제는 정규화 미분 ξ(1−ξ)/0.25 의 5%). **Ch1 L1424-1425 는 정확** — "점유 ξ_eq 자체가 아니라 미분 기준; logistic 미분 종의 5% 폭". 곧 **Ch1 이 코드 주석보다 정밀**. code↔Ch1 실식(A=min(z_cut·nRT,...))은 정합(§1 #8 PASS). **결함 아님** — 코드 docstring 정밀화는 P1 이 이미 보고(코드 개정 후보). Ch1 정정 불요.

---

## 5. 5줄 요약

1. **조**: A조 = code↔Ch1 상호 충실도. 핵심 물리식 양방향 20식 전건 부호·단위·계수 정합(수치 재산출 6종 Ch1 검증값 일치), CRIT/HIGH 0.
2. **확정 갭 수**: 4건 (갭1 식별자 `LCO_STAGING_LIT`↔`LCO_MSMR_LIT` [MEDIUM] · 갭2 전자항 x↔ξ 매핑 미구현 vs Ch1 본문 [MEDIUM·defer라벨] · 갭3 x_MIT 0.85↔0.50 [LOW·P4이월] · 갭4 tab:nodemap N1 L408→L430 오기 [LOW]).
3. **최중대 갭**: 갭1 — Ch1 4곳(L312·L322·L1750·L1844)이 코드 미존재 심볼 `LCO_STAGING_LIT` 지시 → "문건만으로 재현" 즉시 실패(물리·구조는 무결).
4. **정정 목록(master용)**: 갭1=Ch1 4곳 `LCO_MSMR_LIT` 통일(코드변경0 권장) / 갭2=Ch1 sec:lco-code (ii) 현상태 라벨 1문장 보강(x_center 동결 근사, 매핑은 다온도 단계) / 갭3=피팅 단계 x_MIT≈0.85 정정(현 tier-C 라벨 O) / 갭4=Ch1 tab:nodemap N1 `dqdv L430` / [추정] Ch1 L1698 config 부호 표기 Ch2·코드와 통일.
5. **리스크**: 4갭 전부 LOW~MEDIUM·물리 무결(P4 gate PASS 승계). 다온도·다조성 round-trip 피팅 단계로 갭2·갭3 실물리 정정 이월. Ch2 범위(entropy_coefficient·q_rev·비가역 3분해)는 B조 이관 — 본 A조 무판정.
