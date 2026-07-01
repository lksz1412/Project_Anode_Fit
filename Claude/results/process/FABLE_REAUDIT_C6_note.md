# FABLE 재검 챕터3 — 코드 적합성 감사 C-6

- **역할**: 감사 sub (파일 수정 없음, 노트 1개 산출)
- **대상**: `Claude/docs/v1.0.11/Anode_Fit_v1.0.11.py` (852줄, head→tail 전문 정독) ↔ `graphite_ica_ch1_v1.0.11.tex` (1938줄) · `graphite_ica_ch2_v1.0.11.tex` (751줄)
- **방법**: 양방향 전수 매핑 + 파이썬 직접 실행 실측 (numpy 2.x 환경, 자체 self-test + 독립 검산 2종)
- **렌즈**: 서술 순응 금지·실행 우선·이전 판정(0-diff·seam) 재확인·refute·최약점·빈통과금지
- **판정 요약**: 확정 결함 0. 물리·부호·차원 전부 정합. 문건O/코드X 4건은 전부 **명시 선언된 후속과제(deferred)**, 불일치 1건은 **명시 라벨된 tier-C placeholder**. 별건 버전 라벨 위생 경고 1건.

주의: `git status`상 실행 실측은 물리 byte-identical(v1.0.11=문건 가독성 보강판, 코드는 내부 1.0.10 유지)이므로 코드 자기검증은 파일명 v1.0.11 / 내부 라벨 1.0.10 동일 산출물에 대한 것.

---

## 1. 식 → 구현 매핑 (문건 결과박스 전수)

### 1-A. Ch1 결과박스 (17식, boxed 전수)

| 문건 식 (eq: 라벨, 줄) | 수식 | 코드 심볼 | 코드 줄 | 판정 |
|---|---|---|---|---|
| eq:vn (373) | V_n=V_app−σ_d\|I\|R_n | `dqdv` 분극 | L430 | 정합 |
| eq:Uj (453) | U_j=(−ΔH_rxn+TΔS_rxn)/F | `func_U_j` | L78-79 | 정합 |
| eq:dUhys (615) | ΔU_hys=(2/F)[Ωu−2RT·artanh u], u=√(1−2RT/Ω) | `func_dU_hys` / 원형 `func_U_j_hys` | L133-140 / L82-91 | 정합 (양식 동일) |
| eq:Ubranch (635) | U_j^d=U_j+½σ_d h_η γ ΔU_hys | `func_U_branch` | L143-148 | 정합 |
| eq:xieq (775) | ξ_eq=1/(1+exp[−σ_d(V−U^d)/w]) | `func_ksi_eq` (z≥0/z<0 오버플로 분기) | L94-97 | 정합 |
| eq:eqpeak (1190) | (dQ/dV)^eq_j=Q_j ξ(1−ξ)/w | `equilibrium`·`dqdv` peak_shape | L388 / L486 | 정합 |
| eq:chid (1446) | χ_d=χ(방전)/1−χ(충전) | `func_chi_d` | L158-163 | 정합 |
| eq:dHeff (1455) | ΔH_a^eff=ΔH_a−χ_d·Ω | `func_dH_a_eff` | L152-155 | 정합 |
| eq:Acut (1433) | A=min(z_cut·n_j·RT, A_cap·RT) | `_resolve_lag_length` | L353 | 정합 |
| eq:Lqfull (1472) | L_q=(T*/T)·e^{(ΔH_eff−TΔS_a)/RT}/(1+e^{−A/RT})·e^{−χ_d A/RT} | `func_L_q` (ln 형) | L100-107 | 정합 (로그 전개 항별 일치) |
| eq:LV (1485) | L_V=\|dV/dq\|_qa·L_q | `_resolve_lag_length` 반환 | L369 | 정합 |
| eq:lowpass (1531) | ξ_lag,i=ρξ_lag,i−1+(1−ρ)ξ_eq,i, ρ=e^{−Δg/L_V} | `_causal_lowpass` (lfilter/폴백) | L110-128 | 정합 |
| eq:peakshape (1570) | peak_shape=(ξ_eq−ξ_lag)/L_V | `dqdv` | L497 | 정합 |
| eq:branch (1581) | L_V<νΔg → 평형 종, 그 외 꼬리 | `dqdv` 분기 | L484-497 | 정합 (ν=min_lag_grid_steps=2) |
| eq:reversal (1600) | 충전 격자 역전 ξ[::-1]…[::-1] | `dqdv` 충전 분기 | L495 | 정합 |
| eq:sum (1654) | dQ/dV=C_bg+Σ_j Q_j[peak] | `dqdv` 누적+interp | L449-501 | 정합 |
| eq:dSegate (1087) / eq:dSemolar (1023) | ΔS_e=−(π²/3)R(k_BT/e_V)(g_max/Δx)σ(1−σ) | `func_dSe_molar` | L170-185 | 정합 |

부속: eq:ggate(1074) g(E_F,x) 게이트 = `func_dSe_molar` 내부 σ(1−σ) 항으로 **접혀 구현**(닫힌식 dSegate가 게이트 미분을 이미 포함) → 정합(folded). eq:lco-decomp(1695) ΔS_cat=config+vib+elec = LCO `_effective_dS_rxn` seam(L657-673) → 정합.

### 1-B. Ch2 결과박스 (가중식·q_rev·이중계산 직교)

| 문건 식 (줄) | 수식 | 코드 심볼 | 코드 줄 | 판정 |
|---|---|---|---|---|
| eq:logistic (151) | θ_eq/ξ_eq=1/(1+exp[∓(V−U_j)/w]) | `func_ksi_eq` | L94-97 | 정합 (Ch1 종의 통계역학 기원) |
| eq:weighted (471) 단순식 | ∂U/∂T=ΣQ_j g_j(ΔS_j/F)/ΣQ_j g_j | `entropy_coefficient` 첫 항 | L575 | 정합 |
| use-this 종합식 (672) 완전식 | +봉우리내부 (R/F)ln[ξ/(1−ξ)] config 항 포함 | `entropy_coefficient` | L544-578 | 정합 (독립 재구현 대조 오차 1e-19) |
| eq:qrev (645) | q_rev=−I·T·∂U/∂T=−(IT/F)ΔS | `reversible_heat` (T 한 번) | L580-588 | 정합 (T² 없음, 실측 diff 0) |
| eq:qrev (643) 첫 항 | q_irr=I(U_oc−V)≥0 lumped | `irreversible_heat` | L590-598 | 정합 (lumped만; 3분해는 양측 모두 boxed 없음) |
| eq:hys_rev (582) | ∂U^rev/∂T=½(∂U^ch/∂T+∂U^dis/∂T) | `entropy_coefficient` (평형중심 U_j 사용) | L564 | 정합 (γ대칭 자동 근사; γ 무관 실증) |
| 이중계산 직교 (warnbox 293 / decomp 1707) | config(중심표준값)+elec(MIT 골) 슬롯 분리 | seam 중심표준값 + config는 logistic w가 담음 | L573,L657-673 | 정합 (Z=Z_cfg·Z_elec 직교, 중심서 config=0) |

---

## 2. 구현 → 식 역매핑 (근거 없는 창작 색출)

**모듈 공개 함수 11 + 가드 3 + 클래스 메서드 16 — 전수 문건 근거 보유. 코드O/문건X(orphan 창작) = 0건.**

- 원형 보존 함수(불가침): `func_w`(eq:wbase)·`func_U_j`(eq:Uj)·`func_U_j_hys`(eq:dUhys+Ubranch)·`func_ksi_eq`(eq:xieq)·`func_L_q`(eq:Lqfull)·`_causal_lowpass`(eq:lowpass)·`GRAPHITE_STAGING_LIT`(tab:staging) — 근거 O.
- 보완 함수: `func_dU_hys`·`func_U_branch`·`func_dH_a_eff`·`func_chi_d`(각 eq: 라벨 주석과 일치) — 근거 O.
- LCO 확장: `func_dSe_molar`(eq:dSegate)·`LCO_MSMR_LIT`(tab:lco-staging)·`LCOCathodeDQDV._effective_dS_rxn`(eq:lco-decomp seam) — 근거 O.
- 클래스 인프라: `_n_factor`/`_width`(eq:wbase)·`_chi_d`/`_chi_and_dH_eff`(eq:chid+dHeff)·`_resolve_lag_length`(sec:lag 사슬)·`equilibrium`/`dqdv`(nodemap N0-N9)·`curve`(N0 facade)·`_direction_to_sigma`(eq:n0map)·`entropy_coefficient`/`reversible_heat`/`irreversible_heat`(Ch2)·`_effective_dS_rxn` seam(sec:lco-code)·`_build_seed_L_V`(tab:inputs seed_*, 진단용) — 근거 O.
- 가드 `_finite/_finite_pos/_finite_nonneg`: 설계항목 (B), tab:inputs 인자 범위 — 근거 O.
- 전체 인자 노출: tab:inputs(1778-1804)와 생성자/전이 dict 키가 1:1 (하드코딩 상수 0 주장 확인).

---

## 3. 실행 실측 (파이썬 직접 실행)

**self-test (`__main__`): overall OK = True.** 주요 계측값:

- **부호 사슬 8항 (S1–S8, sec:signcheck)** — 전항 실측/소스 확인 PASS:
  - S1 U(298): 0.211/0.140/0.120/0.085 V = 목표 정합. S2 ξ_eq: 방전 V↑→peak(neg=False). S3 peak 양수(neg=False 전조건). S4 히스: dU_hys=86.7 mV, dis−chg peak=+86.9 mV(기대 +86.7). S5 χ_d/ΔH_eff: chi_split 주입 differ=True. S6 A 컷상수(운영 미분 0). S7 충전 격자역전 neg=False. S8 V_n=V_app−σ_d\|I\|R_n(L430).
- **면적 보존**: ∫(equilibrium)dV = **0.97000** = ΣQ_j(0.10+0.12+0.25+0.50) **ratio 1.00000** — eq:eqpeak 면적=Q_j 정확.
- **극한**:
  - Ω→2RT: `func_dU_hys(2RT)`=0.0, Ω<2RT=0.0 (제곱근 NaN 영역 명시 분기).
  - \|I\|→0: `func_L_q(1e-9)`=1.09e-15→0, `func_L_q(0)`=−inf(가드); 방전/충전 곡선 diff 5.1e-15.
  - ΔS=0: dS_rxn=0에서 진중심 ξ=0.5 config=0 → ec = **0.000e+00** (정확).
- **전자 엔트로피 계수**: `func_dSe_molar`(x_MIT,298,g13,Δx0.05) = **−45.655 J/mol/K** (문건 검증값 −45.7~−46 정합), 해석식과 완전 일치 → **3중 단위 가드**(leading −, ÷e_V, 몰당 R·k_B) 실증.
- **q_rev 차원**: `reversible_heat` = −I·T·ec **정확 일치**(max diff 0.0) → T 한 번만(T² 없음). 부호: ΔS>0역(+29) ec>0(방전 흡열), ΔS<0역(−16) ec<0(발열) — Ch2 부호규약 정합.
- **Ch2 종합식 대조(최약점 검증)**: 코드 `entropy_coefficient` vs 독립 재구현(가중식 완전식) max diff = **1.08e-19** — Ch2 use-this 박스식 정확 구현.
- **이전 판정 재확인**: curve==dqdv max_diff **0.00e+00** / graphite seam `_effective_dS_rxn`==tr['dS_rxn'] **byte 0-diff** / per-tr override isolation **True** / guards **7/7**.
- **LCO seam**: U(298)=3.930/3.880/4.050 V 목표 정확 착지(dH_rxn이 ΔS_e 흡수), 'electronic' 전이만 dS_eff 변경(tr1: −4→−49.678), 비전자 전이 불변; LCO vs graphite-base diff 2.87(seam 활성).

---

## 4. 갭 분류

### [정합] — 주류
Ch1 17 + Ch2 7 = **24개 결과박스 전부 코드에 정확 매핑**, 실행 실측(면적·부호8·극한·차원·전자계수·종합식)이 물리 정합 확정. 코드O/문건X(orphan) = **0**.

### [문건O · 코드X] — 전부 **명시 선언된 후속과제**(결함 아님)
1. **eq:U1T2 (1060)** 전자항 T² 곡률(½=a_e/2F): 코드는 ΔS_e를 T_ref 동결 상수 오프셋으로 처리 → T² 곡률 없음. LCO 서브클래스 docstring(L665-666)·tab:lco-staging 캡션에 "P4 미구현, 다온도 round-trip 피팅 단계 과제"로 명시.
2. **좌표 매핑 x=x(ξ_eq,1(V)) (Ch1 §1730-1734 (i))**: 코드는 `x_center` 고정 스칼라 사용(전압격자 위 x-의존 아님) → 단일-기준 근사. 명시 선언(L665-666).
3. **eq:hys_branch (574)** 분기별 ∂U^(d)/∂T: 코드는 분기평균(eq:hys_rev)만 구현. `entropy_coefficient` docstring(L552-554) "비대칭 분기별 ∂U/∂T 미구현, Ch2 범위 밖 선언, 후속 과제" — γ 무관 실증(§3).
4. **eq:ensavg 앙상블 ρ(U_app) broadening convolution**: 코드는 단일 유효입자+L_V 구조, ρ는 현상학적 w에 흡수(forward-only). Ch1 broadening keybox(L1334-1352) 명시 배제(역산 금지·PSD 크기 convolution 미도입).

### [코드O · 문건X]
**없음.** 모든 공개 심볼이 문건 근거 보유(§2). 창작·문건밖 로직 미발견.

### [불일치] — 라벨된 placeholder (물리 결함 아님)
1. **LCO_MSMR_LIT 시연값**: 코드는 x_MIT=0.50, 'electronic'을 3.880 V **중간** 전이(tr1)에 배정. 문건 물리 anchor(tab:lco-staging)는 T1(MIT)~3.90 V·x_MIT≈0.85(최저전위)에 전자항. → tab:lco-staging 캡션(L325-329) + 코드 주석(L628-635)이 **tier-C placeholder**로 명시, round-trip 피팅 시 T1=MIT dict로 재정렬 선언. 물리 defect 아니라 시연 초기값 배치.
2. (참고, 양측 일관) q_irr 3분해(I²R+Iη_ct+Iη_diff): Ch2에 boxed 식 없음 → 코드도 lumped만, 주석에 정직 명기(L594-596). "neither/정직" 케이스.

### 별건 경고 (물리 아님 · 버전 위생)
- **버전 라벨 불일치**: 파일명 `Anode_Fit_v1.0.11.py`·`graphite_ica_ch1_v1.0.11.tex`이나 **내부 라벨·상호참조는 전부 "1.0.10"**(코드 L3, tex \date L100). 코드 [근거 문건] 포인터(L38)는 더 오래된 `graphite_ica_ch1_Opus_v6.tex`를 가리킴(stale). v1.0.11은 문건 가독성 보강판(broadening 다리·ρ(U_j)→ρ(U_app))이라 코드는 물리 byte-identical로 rev 안 됨 — 결과식 정합엔 영향 없으나 provenance 라벨 위생 권고(수정 범위 밖이라 보고만).

---

## 부록 — 실행 환경/재현
- 실행: `python Anode_Fit_v1.0.11.py` (self-test) + 검산 스크립트 2종(scratchpad `c6check.py`/`c6check2.py`).
- numpy 2.x: `np.trapz`→`np.trapezoid` 치환 필요(대상 코드 무관, 검산 스크립트 측 이슈).
- 대상 파일 무수정(감사 sub 원칙 준수).
