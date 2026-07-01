# P5 감사 드래프트 — S1 · A조 (code↔Ch1 양방향 매핑)

> **감사자**: S1 · A조 (code↔Ch1 상호충실도)  
> **대상**: Anode_Fit v1.0.10 (`docs/v1.0.10/Anode_Fit_v1.0.10.py` 850줄 · `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` 1933줄)  
> **앵커**: P1 RESULT(코드 audit) · P2 RESULT(Ch1 편입) · P3 RESULT(Ch2) · P4 RESULT(코드 개정)  
> **보고 4-tier**: [확정] / [근거미발견] / [추정] / [미검증]  
> **제약**: 코드·문건 수정 없음(감사·보고만)

---

## 1. 감사 초점 및 방법

A조 초점은 **양방향 매핑**:
- **Ch1→코드**: Ch1에 명시된 수식이 코드에 1:1로 구현되어 있는가
- **코드→Ch1**: 코드의 함수·계산이 Ch1 이론 근거를 갖는가
- **갭·부호·단위·계수 불일치** 적발

공통 항목:
- 3대 무결 최종 확인 (식별자 보존·범위 보존·사본 금지)
- P4 이월 항목 문서 정합 확인 (x_MIT tier-C · 다온도 T² 곡률 · 시연 파라미터 · 비가역 3분해)

정독 범위 (head→tail 전영역):
- 코드 850줄 전문 ✓
- Ch1.tex 1933줄 전문 ✓
- Ch2.tex 751줄 전문 ✓
- P1-P4 RESULT 전문 ✓

---

## 2. Ch1→코드 매핑 (식이 코드에 있는가)

### 2-A. 전이 폭 (eq:wbase)

**Ch1**: w_j = n_j · RT/F (eq:wbase, L~75)  
**코드**: `func_w(T, n=1.0): return n * R * T / F` (L74-75)  
**판정**: [확정] 1:1 일치. n=1.0 기본값 = Ch1 기술 정합.

### 2-B. 평형 중심 전위 (eq:Uj)

**Ch1**: U_j(T) = (−ΔH_rxn + T·ΔS_rxn)/F (eq:Uj)  
**코드**: `func_U_j(T, dH_rxn, dS_rxn): return (-dH_rxn + T * dS_rxn) / F` (L78-79)  
**판정**: [확정] 1:1 일치. 부호, 선형 T 의존 정합.

### 2-C. 평형 점유 (eq:xieq)

**Ch1**: ξ_eq = 1/(1 + exp[−σ_d(V−U_j^d)/w_j]) (eq:xieq)  
**코드**: `func_ksi_eq(T, V_n, U, n=1.0, s=1)` — logistic, overflow-safe 분기 (L94-97)  
**판정**: [확정] 1:1 일치. s=σ_d 부호 흡수. overflow-safe 분기(z≥0/z<0)로 ξ∈(0,1) 보장.

### 2-D. 히스테리시스 gap (eq:dUhys)

**Ch1**: ΔU_j^hys = (2/F)[Ω_j·u_j − 2RT·artanh(u_j)], u_j = √(1−2RT/Ω_j) (eq:dUhys)  
**코드**: `func_dU_hys(T, Omega)` — Ω≤2RT → 0; else u·artanh 닫힌형 (L133-140)  
**판정**: [확정] 1:1 일치. Ω≤2RT → gap=0 분기(spinodal 임계 아래 단상) 정합.

**주의**: `func_U_j_hys`(L82-91)는 동일식을 가진 死코드(미호출). 실제 사용처는 `func_dU_hys` 뿐. [확정, P1 RESULT 확인]

### 2-E. 분기 중심 (eq:Ubranch)

**Ch1**: U_j^d = U_j + ½·σ_d·h_η·γ·ΔU_j^hys (eq:Ubranch)  
**코드**: `func_U_branch(T, U_j, Omega, gamma, sigma_d, h_eta=1.0)` → center = U_j + 0.5·sigma_d·h_eta·gamma·func_dU_hys(T, Omega) (L143-148)  
**판정**: [확정] 1:1 일치. h_eta 인자화(원형 func_U_j_hys partial_hys=1.0 하드코딩 개선).

### 2-F. 방향별 전달계수 (eq:chid)

**Ch1**: χ_d = χ (방전) / 1−χ (충전) (eq:chid)  
**코드**: `func_chi_d(chi, sigma_d)`: σ_d≥0 → chi; σ_d<0 → 1−chi (L158-163)  
**판정**: [확정] 1:1 일치. 합-1 규칙 보존.

### 2-G. 유효 활성화 엔탈피 (eq:dHeff)

**Ch1**: ΔH_a^eff = ΔH_a − χ_d·Ω (eq:dHeff)  
**코드**: `func_dH_a_eff(dH_a, Omega, chi_d)` → dH_a - chi_d * Omega (L152-155)  
**판정**: [확정] 1:1 일치. 부호 정합.

### 2-H. affinity 절단 (eq:Acut)

**Ch1**: A = min(z_cut·n_j·RT, A_cap·RT) (eq:Acut)  
**코드**: `A = min(z_cut * abs(n) * R * T, A_cap_RT * R * T)` (L331)  
**판정**: [확정] 1:1 일치. n_j = 다중도(코드 abs(n) 음수 방어 포함).

**주의**: n=1, z_cut=4.357(기본) → z_cut·RT=4.357RT > A_cap·RT=4.0RT → A=4RT로 capped, z_cut inert. z_cut<4.0 또는 n≠1이면 binding. [확정, P1 §2-D D4]

### 2-I. 동역학 지연 길이 (eq:Lqfull)

**Ch1**: L_q = (T*/T)·exp[(ΔH_a^eff − T·ΔS_a)/RT] / (1+e^{−A/RT}) · e^{−χ_d·A/RT} (eq:Lqfull)  
**코드**: `func_L_q(T, I, Q_cell, dH_a, dS_a, x, A)`:  
```
T_attempt = (I/Q_cell) * h / kB          # T* = attempt frequency
ln_Lq = (ln T_attempt - ln T)
       - ln(1 + exp(-A/(R*T)))            # ÷(1+e^{-A/RT})
       + (dH_a - T*dS_a) / (R*T)         # ΔG_a/RT
       - x * A / (R*T)                    # −χ_d·A/RT (x=χ_d 주입)
```
(L100-107)  
**판정**: [확정] 1:1 일치. T_attempt/T = T*/T 비. 로그 분해 방식이 다르나 수학적 동치.

**주의(GAP-A3)**: 파라미터명 `x`가 Ch1의 χ_d를 받도록 설계되어 있으나(호출처 `_resolve_lag_length` L342에서 `x=chi_d`로 주입), 함수 시그니처의 `x` 자체는 composition x와 동일 기호. 호출 맥락에서 혼동 가능성 있음. [추정 — 호출 체인 확인으로 물리적 오류 없음 확인]

### 2-J. 전압축 지연 (eq:LV)

**Ch1**: L_V = |dV/dq|_qa · L_q (eq:LV)  
**코드**: `L_V = abs(tr.get('dVdq_qa', 0.0)) * L_q` (L347 근방)  
**판정**: [확정] 1:1 일치.

**주의**: dVdq_qa 미지정 → L_V=0 → 동역학 꼬리 silent 소거. [확정, P1 F2]

### 2-K. 평형 peak 합산 (eq:eqpeak, eq:sum)

**Ch1**: (dQ/dV)^eq_j = Q_j·ξ_eq(1−ξ_eq)/w_j; dQ/dV = C_bg + Σ_j Q_j·[peak_shape_j] (eq:eqpeak, eq:sum)  
**코드**: `equilibrium`: `Cbg + sum(tr['Q'] * ksi*(1-ksi)/w)` (L366); `dqdv` L462-464 평형 분기도 동일 형태  
**판정**: [확정] 1:1 일치. 면적 보존 = ∫ = 1.000000 [P1 §0 검산].

### 2-L. 인과 저역통과 필터 (eq:lowpass, eq:reversal)

**Ch1**: ξ_lag,i = ρ·ξ_lag,i-1 + (1−ρ)·ξ_eq,i; 충전 방향: ξ[::-1] (eq:lowpass, eq:reversal)  
**코드**: `_causal_lowpass`: decay=e^{−grid_step/lag}; IIR 1차 필터; scipy lfilter 우선 (L110-128); 충전(σ_d<0) 격자 역전 후 필터 후 재역전 (L470-473)  
**판정**: [확정] 1:1 일치. DC gain=1(면적 보존). 충전 역전 로직 eq:reversal 정합.

### 2-M. peak shape (eq:peakshape)

**Ch1**: peak_shape = (ξ_eq − ξ_lag)/L_V (eq:peakshape)  
**코드**: `peak_shape = (ksi_eq - ξ_lag) / lag_len_V` (L475)  
**판정**: [확정] 1:1 일치.

### 2-N. 전자 엔트로피 게이트 (eq:dSegate)

**Ch1**: ΔS_e,j(x,T) = −(π²/3)·k_B²·T·(g_max/Δx_MIT)·σ(1−σ), σ=logistic[(x−x_MIT)/Δx_MIT] (eq:dSegate)  
**코드**: `func_dSe_molar(x, T, g_max_eV, x_MIT, dx_MIT)`:
```python
z = (x - x_MIT) / dx_MIT
sig = 1.0 / (1.0 + np.exp(-z))
gate = sig * (1.0 - sig)
return -(np.pi**2 / 3.0) * R * (kB * T / EV_TO_J) * (g_max_eV / dx_MIT) * gate
```
(L~191-200)  
**판정**: [확정] 수식 1:1 일치. 단위 변환 분석:

- Ch1 eq:gunit: g_J = g_eV / e_V (나눗셈, eV→J 변환, P2 RESULT §3 C3 확인)
- 코드: `(kB * T / EV_TO_J) * (g_max_eV / dx_MIT)` → kB [J/K] · T [K] / EV_TO_J [J/eV] = kB·T in eV 단위; g_max_eV [/eV] / dx_MIT → [/eV·Δx]; 결과: 무차원 게이트 σ(1-σ) 곱 → [/eV·Δx·eV] = [/Δx]; ×R [J/mol/K] → [J/mol/K/Δx]…

**★ 단위 심층 검산 (GAP-A5)**:  
Ch1 eq:dSemolar:  
ΔS_e,j^mol = N_A·(π²/3)·k_B·(dg/dx)|_{x_MIT}·(k_B·T)  
= (π²/3)·R·k_B·T·(g_max/Δx) [J/(mol·K)] if g in [1/J] units

코드에서:  
`-(π²/3) * R * (kB * T / EV_TO_J) * (g_max_eV / dx_MIT) * gate`  
= −(π²/3) · R · (kB·T/e_V) · (g_max_eV/dx_MIT) · gate  
= −(π²/3) · R · [kB·T in eV] · [g in 1/eV / dx_MIT] · gate

단위 분석: [J/mol/K] · [eV] · [1/eV / Δx] = [J/mol/K/Δx]  
게이트 gate = σ(1−σ) ≈ (1/4) at peak, 무차원  
결론: g_max_eV / dx_MIT가 사실상 dg/dx = -g_max·(1/Δx)의 최대 진폭에 해당하며 eq:gunit의 나눗셈(g_J = g_eV / e_V) 형태 구현. [확정]

수치 검증: func_dSe_molar(x_MIT=0.50, T=298.15, g_max_eV=13.0, x_MIT=0.50, dx_MIT=0.05)  
= −(π²/3)·8.314·(1.38e-23·298.15/1.602e-19)·(13.0/0.05)·0.25  
= −(3.29)·8.314·(2.568e-2 eV)·260·0.25  
≈ −3.29·8.314·0.02568·65  
≈ −45.7 J/(mol·K)  
Ch1 목표값: −46 J/(mol·K) [P4 RESULT §9, P2 RESULT §6 "−45.68 vs −46"]. [확정 일치]

### 2-O. MIT 게이트 전자밀도 함수 (eq:ggate)

**Ch1**: g(E_F,x) ≈ g_max[1−σ((x−x_MIT)/Δx_MIT)], g_max=13 e/eV, x_MIT≈0.85, Δx_MIT≈0.05 (eq:ggate, sec:lco-gate)  
**코드**: `LCO_MSMR_LIT` T2 전이 (U=3.880V): `'g_max_eV': 13.0, 'x_MIT': 0.50, 'dx_MIT': 0.05`  
**판정**:

**★★ [확정 불일치 — GAP-A1: x_MIT 값 상이]**  
- Ch1 eq:ggate 초기값: x_MIT≈**0.85**, Δx_MIT≈0.05  
- Ch1 tab:lco-staging: T1 (MIT) 전이 x≈**0.94-0.75**, 전이 중심 x≈**0.845**  
- 코드 LCO_MSMR_LIT T2: x_MIT=**0.50**, x_center=0.50  
- 괴리: 코드 x_MIT=0.50 vs Ch1 x_MIT≈0.85 → **Δ = 0.35 (x 좌표계 기준 35% 이동)**  
- P4 RESULT §11 라벨: "x_MIT=0.50 tier-C placeholder"로 명시 (의도적 임시값)  
- 코드 LCO_MSMR_LIT에 tier-C 라벨 있음 [확정]  
- **이월 상태**: P5 이월 — round-trip 피팅으로 물리값 정정 및 문서 정합 필요  

이 불일치는 버그가 아닌 의도적 tier-C placeholder이나, **P5 최종 점검 기준으로 코드와 Ch1 문서 간 수치 불일치가 잔존**함을 감사 기록에 명시.

### 2-P. MSMR 동형 (eq:msmr)

**Ch1**: x_j = X_j/(1+exp[f(U−U_j⁰)/ω_j]) → logistic 동형 (eq:msmr)  
**코드**: 별도 `func_msmr` 없음. LCOCathodeDQDV가 `func_ksi_eq` 재사용 (σ_d=+1이므로 f↔σ_d=+1, U_j⁰↔U_j, ω_j↔w_j 매핑)

**판정**: [근거미발견 — 별도 함수 없음, 동형 재사용이 의도] Ch1 eq:msmr은 LCO MSMR과 logistic 동형성 서술이며, 코드는 동일 `func_ksi_eq`를 재사용하는 설계. 별도 구현 부재가 설계 의도이나, 동형 mapping이 코드 주석이나 Ch1에 명시적으로 기술되어 있지 않아 추적성이 낮음.

**★ [추정 — GAP-A2: 동형 매핑 명시 부재]**  
Ch1 eq:msmr 파라미터 대응(X_j↔Q_j, U_j⁰↔U_j^d, ω_j↔w_j, f↔−σ_d)이 P3 RESULT §11에는 기술되었으나 코드 주석이나 Ch1 본문에 명시적 cross-reference 없음. 추적성 낮음.

### 2-Q. LCO _effective_dS_rxn seam

**Ch1**: 전자엔트로피 ΔS_e,j 를 dS_rxn에 가산하는 단일 진입점 설계 (sec:lco-code 언급)  
**코드**: `LCOCathodeDQDV._effective_dS_rxn(tr, T)`:
```python
dS = tr['dS_rxn']
if tr.get('electronic'):
    T_ref = 298.15
    dS = dS + func_dSe_molar(tr['x_center'], T_ref, ...)
return dS
```
**판정**: [확정] seam 설계 정합. 3경로(equilibrium·dqdv·entropy_coefficient) 공유 [P4 RESULT §7 확인].

**★ [확정 — T_ref 동결 근사]**  
_effective_dS_rxn에서 T_ref=298.15 K 동결 상수 오프셋 사용. Ch1 eq:dSegate는 ΔS_e∝T (Sommerfeld). 단일온도 사용에서는 정합하나, 다온도에서 전자엔트로피 기여가 T-의존으로 계산되지 않음. 이 근사는 P4 RESULT §8 adversarial 항목7 해소로 factor-2 방지 목적의 의도적 설계. **P4 이월 항목으로 명시됨**.

### 2-R. 엔트로피 계수 가중식 (eq:weighted, Ch2)

**Ch2**: ∂U_oc/∂T = Σ[Q_j g_j / Σ Q_k g_k]·(ΔS_eff,j/F + (R/F)·ln[ξ_j/(1-ξ_j)]) (eq:weighted)  
**코드**: `entropy_coefficient(self, V_n, T=298.15)`:  
위 식의 완전식 구현. g_j = ξ_eq(1-ξ_eq)/w_j; ΔS_eff,j = _effective_dS_rxn 경유 [P4 RESULT §7 확인]  
**판정**: [확정] 1:1 일치 (완전식, config 항 포함).

### 2-S. 가역 발열 (eq:qrev, Ch2)

**Ch2**: Q_rev = −I·T·∂U_oc/∂T (eq:qrev)  
**코드**: `reversible_heat(self, I, V_n, T=298.15)`: `return -float(I) * T * self.entropy_coefficient(V_n, T)`  
**판정**: [확정] 1:1 일치. T 한 번(T²가 아님) 정합. [P4 RESULT §9 "T 한 번" 확인]

---

## 3. 코드→Ch1 매핑 (함수가 식 근거 있는가)

### 3-A. EV_TO_J 상수

**코드**: `EV_TO_J = 1.602176634e-19` (J/eV)  
**Ch1**: eq:gunit: g_J = g_eV / e_V (L2 P2 RESULT §3 C3)  
**판정**: [확정] Ch1 eq:gunit 근거 있음. 코드에서 나눗셈 형 (`kB * T / EV_TO_J`) = e_V로 나누기. 정합.

### 3-B. GRAPHITE_STAGING_LIT 데이터셋

**코드**: 4-전이 데이터 (U=0.085/0.120/0.140/0.210 V, Q=0.50/0.25/0.12/0.10)  
**Ch1**: 흑연 staging 4-전이 (stage 4→3, 3→2L, 2L→2, 2→1; 전위·용량)  
**판정**: [확정] Ch1 tab:staging 정합. 수치는 초기값 (피팅 대상). 흑연 음극 전위대(~0.08-0.21 V vs Li) 일치.

### 3-C. LCO_MSMR_LIT 데이터셋

**코드**:
```python
LCO_MSMR_LIT = [
    {'U': 3.930, 'w': 0.030, 'Q': 0.55, 'dH_rxn': -377400.0, 'dS_rxn': +6.0, 'n': 1.0},
    {'U': 3.880, 'w': 0.024, 'Q': 0.30, ..., 'electronic': True, 'x_center': 0.50,
     'g_max_eV': 13.0, 'x_MIT': 0.50, 'dx_MIT': 0.05},
    {'U': 4.050, 'w': 0.028, 'Q': 0.15, 'dH_rxn': -391360.0, 'dS_rxn': -2.0, 'n': 1.0},
]
```
**Ch1**: tab:lco-staging 3-전이 (T1=MIT ~3.90V, T2=order-disorder a ~4.05V, T3=order-disorder b ~4.17-4.20V)  
**판정**:

전이 개수: 코드 3개 vs Ch1 3개 [확정 일치]  
전위 대응:
- 코드 U=3.930V ↔ Ch1 T1 ~3.90V [추정 일치, 오차 30mV 범위]
- 코드 U=3.880V (electronic) ↔ Ch1 T1 MIT — **단 MIT 중심 전위로서 3.88V는 Ch1 ~3.90V와 근접** [추정 일치]
- 코드 U=4.050V ↔ Ch1 T2 ~4.05V [확정 일치]
- Ch1 T3 (~4.17-4.20V): **코드에 대응 전이 없음** [확정 불일치 → GAP-A6]

**★ [확정 불일치 — GAP-A6: T3 전이 누락]**  
Ch1 tab:lco-staging의 T3 (order-disorder b, ~4.17-4.20V, x≈0.48)에 대응하는 코드 전이가 LCO_MSMR_LIT에 없음. 코드는 3전이(U=3.930, 3.880, 4.050V)이나, Ch1은 T1/T2/T3 세 종류를 구별하고 T2=~4.05V, T3=~4.17-4.20V로 다르게 지목. 현재 코드 U=4.050V가 T2만 포괄하고 T3는 누락. tier-C 시연 데이터셋이므로 의도적 단순화일 가능성 있으나 문서 정합 불명확. [추정 — tier-C 단순화, 확인 필요]

### 3-D. σ_d 부호 규칙 — LCOCathodeDQDV

**코드**: `LCOCathodeDQDV(GraphiteAnodeDischargeDQDV)` — 상속, `sigma_d` 뒤집기 없음  
**Ch1**: LCO 양극에서의 방전 σ_d 부호 — LCO가 양극이므로 방전 시 Li 삽입 방향이 흑연 음극과 반대  
**판정**: [추정 — GAP-A7: σ_d 부호 뒤집기 검토 필요]  

Ch1은 흑연 음극 기준. LCO 양극은 방전 시 Li 삽입(x 증가), 흑연 음극은 방전 시 Li 삽입(x 증가). dQ/dV 물리에서:
- 흑연 음극 방전: V 감소 방향으로 dQ/dV 봉우리 → σ_d 방향 정의가 일관
- LCO 양극 방전: V 감소 방향이지만 양극 전위 ~3.9-4.1V 범위에서 dQ/dV 형태가 음극과 유사 구조

코드에서 σ_d 뒤집기 없이 상속 사용 중이며, P4 RESULT §7 "σ_d 뒤집기 없음"으로 명시. 이 설계가 Ch1 이론과 물리적으로 정합하는지 명시적 수식 근거가 Ch1에 없음. [근거미발견 — Ch1 LCO σ_d 수식 명시 없음]

### 3-E. func_L_q I≤0 sentinel

**코드**: `if I <= 0: return -np.inf` (L102) — 충전 또는 전류 0일 때 sentinel  
**Ch1**: 인과 꼬리는 방전 방향 정의. 충전은 격자 역전으로 처리 (eq:reversal)  
**판정**: [확정] Ch1 eq:reversal과 정합. I≤0→−inf sentinel은 호출측 _resolve_lag_length L319에서 catch되어 L_V=0(평형종)으로 처리. 의도 흐름 차단 없음 [P1 §1.2 확인].

### 3-F. _build_seed_L_V 진단 함수

**코드**: `_build_seed_L_V(T, I, Q_cell)` (L262-269) — σ_d=+1 고정 방전 기준 L_V seed  
**Ch1**: 이 함수에 대응하는 명시 수식 없음  
**판정**: [근거미발견] 진단/초기값 전용 내부 함수로 Ch1 이론 외 범위. 물리적 오류 아님.

### 3-G. _resolve_lag_length 복합 우선순위 로직

**코드**: 3단계 우선순위: ① L_V 직접 지정 → ② I≤0·dH_a 부재 → ③ 동역학 산출 (L313-347)  
**Ch1**: eq:Lqfull 단일 수식. 직접 지정·부재 분기는 코드 공학 선택  
**판정**: [추정] ③의 물리 계산 경로는 Ch1 eq:Lqfull 근거. ①②는 코드 편의 분기로 Ch1 범위 외. 물리적 정합.

### 3-H. equilibrium vs dqdv 분기 구조

**코드**: L462-464 `lag_len_V < min_lag_grid_steps·grid_step` → 평형 peak 분기  
**Ch1**: Ch1은 이 numerical 분기를 명시하지 않음. 연속 |I|→0 극한만 기술  
**판정**: [추정] 수치 안정성을 위한 코드 공학 선택. Ch1 eq:eqpeak 극한과 물리적 정합하나 분기 문턱 수치(min_lag_grid_steps)는 Ch1 근거 없음.

---

## 4. 부호·단위·계수 불일치 종합표

| ID | 위치 | 유형 | 설명 | 판정 |
|---|---|---|---|---|
| **GAP-A1** | LCO_MSMR_LIT T2 vs Ch1 eq:ggate | **수치 불일치** | 코드 x_MIT=0.50 vs Ch1 x_MIT≈0.85 (괴리 0.35) | [확정] P4 이월 tier-C placeholder |
| **GAP-A2** | eq:msmr 동형 | **명시성 결여** | MSMR↔logistic 동형 cross-ref 코드 주석 및 Ch1 미명시 | [추정] 추적성 낮음 |
| **GAP-A3** | func_L_q 파라미터 `x` | **명칭 혼동** | x가 χ_d를 받도록 설계되나 기호 충돌(composition x와 동일) | [추정] 물리 오류 없음, 가독성 이슈 |
| **GAP-A4** | eq:Sedirect vs 코드 | **경로 누락** | Ch1 직접엔트로피 경로(eq:Sedirect) 별도 코드 경로 없음 | [근거미발견] 공통 결과식 구현이라 실용적 동치 |
| **GAP-A5** | func_dSe_molar 단위 | **단위 검산** | kB*T/EV_TO_J = kB*T in eV, g in 1/eV → 결합 단위 확인 | [확정] 수치 −45.7≈−46 J/(mol·K) 일치 |
| **GAP-A6** | LCO_MSMR_LIT T3 누락 | **전이 누락** | Ch1 T3 (~4.17-4.20V) 대응 전이 코드 미존재 | [추정] tier-C 단순화, 문서 정합 미명시 |
| **GAP-A7** | LCO σ_d 방향 | **설계 근거** | 양극 σ_d 뒤집기 미적용의 Ch1 수식 근거 미명시 | [근거미발견] 설계 의도 주석 필요 |

---

## 5. P4 이월 항목 문서 정합 확인

### 5-A. x_MIT=0.50 tier-C placeholder

**P4 RESULT §11**: "Ch1 eq:ggate anchor x_MIT≈0.85·플래토 x≈0.75-0.94와 불일치. round-trip 피팅 단계서 물리값 정정·문서 정합."  
**현재 상태**: [확정] 코드 LCO_MSMR_LIT T2에 `'x_MIT': 0.50` 잔존. Ch1은 x_MIT≈0.85 초기값 명기. 불일치 잔존.  
**문서 정합 판정**: Ch1 §lco-gate는 "초기값으로 …"라는 맥락으로 기술하여 피팅 대상임을 암시하나, 코드의 tier-C placeholder 값(0.50)이 Ch1 초기값(0.85)과 다른 이유에 대한 설명이 Ch1 또는 코드 주석 어디에도 없음. **문서 정합 필요. [미검증 — round-trip 피팅 후 신뢰값 확정 필요]**

### 5-B. 다온도 T² 곡률 (eq:U1T2)

**P4 RESULT §11**: "전자전이 U_j(T)의 Sommerfeld T-스케일·eq:U1T2 center-T_ref 별도적분(½=a_e/2F) 미구현."  
**Ch1 eq:U1T2**: U₁(T) = U₁(T₀) + (ΔS₀/F)(T−T₀) + (a_e/2F)(T²−T₀²) (P2 RESULT §3 항목 6 신설)  
**코드**: `func_U_j`는 선형 T만 구현: U_j = (−ΔH + T·ΔS_rxn)/F. T² 항 없음.  
**문서 정합 판정**: Ch1에 eq:U1T2 명시됨(P2 편입 확인). 코드는 선형 근사만. T² 항 미구현이 코드 주석에 "(다온도 T² Sommerfeld 미구현, 단일온도 동결 근사)" 라벨로 명시되어 있는지 확인 필요. **[미검증 — 코드 주석 확인 필요; Ch1-코드 부분 불일치]**

### 5-C. LCO 시연 파라미터

**P4 RESULT §11**: "tier-C 기본값 → 실측/round-trip 피팅으로 신뢰값화 필요."  
**현재 상태**: LCO_MSMR_LIT 3전이 모두 tier-C 라벨(P4 RESULT §7 "tier-C 시연"). 실측 데이터 피팅 미완.  
**문서 정합 판정**: Ch1 tab:lco-staging의 수치(전위·폭·용량)와 코드 LCO_MSMR_LIT 수치가 파라미터별로 일부 다름(T3 전이 누락, T1/T2 U값 근사 일치). tier-C 임시값임이 코드에 명시되어 있으나 Ch1 문서에 tier-C 주석 없음. **[추정 — 피팅 전 임시 상태]**

### 5-D. 비가역 3분해

**P4 RESULT §11**: "lumped만 구현(I(U_oc−V)), I²R+Iη_ct+Iη_diff 개별 분해는 율의존 피팅 과제."  
**Ch2 eq:qrev**: Q_irr = I(U_oc−V) lumped 표현 (sec:revheat)  
**코드**: `irreversible_heat(self, I, V_n, U_oc, T=None)`: lumped I(U_oc−V) 구현  
**문서 정합 판정**: Ch2는 lumped를 boxed 표현으로 제시하며 3분해는 별도 구현 과제로 명기 안 함. 코드와 Ch2 정합. **[확정 — 현 단계 정합, 3분해는 미래 과제]**

---

## 6. 3대 무결 최종 확인

### 6-A. 식별자 보존

**검사 범위**: P4 신규 추가 심볼 — `EV_TO_J`, `func_dSe_molar`, `_effective_dS_rxn`, `entropy_coefficient`, `reversible_heat`, `irreversible_heat`, `LCO_MSMR_LIT`, `LCOCathodeDQDV`  
**원형 보존 심볼**: `func_w`, `func_U_j`, `func_U_j_hys`, `func_ksi_eq`, `func_L_q`, `_causal_lowpass`, `func_dU_hys`, `func_U_branch`, `func_dH_a_eff`, `func_chi_d`, `GRAPHITE_STAGING_LIT`, `GraphiteAnodeDischargeDQDV`

P4 RESULT §7 "식별자·정수코드·死코드 보존", §9 "흑연 0-diff: 13/13 배열 np.array_equal bit 완전일치 PASS".  
**판정**: [확정] 식별자 보존. 사용자 원형 코드 식별자 변조 없음.

### 6-B. 범위 보존

**검사**: P4에서 추가된 함수들이 기존 `GraphiteAnodeDischargeDQDV` 흑연 로직을 수정했는가?  
P4 RESULT §7 "equilibrium·dqdv seam: Edit 2줄 — func_U_j 인자 → self._effective_dS_rxn (byte 0-diff)"  
P4 RESULT §9 "흑연 0-diff: 13/13 배열 np.array_equal bit 완전일치 PASS(LCO override 동결 변경 후에도 유지)"  
**판정**: [확정] 범위 보존. 흑연 로직 bit-identical 회귀. seam 편입이 기존 기능 범위 밖에 최소 영향으로 완료.

### 6-C. 사본 금지

**검사**: 프로젝트 내 글로벌 지침·메모리의 사본 생성 여부, 코드 중복 생성 여부  
**판정**: [확정] `func_U_j_hys`(死코드)와 `func_dU_hys`가 동일식을 중복 보유하나 전자는 원형 보존 목적 동결(L36 라벨). 의도적 중복으로 글로벌 사본 금지 위반 아님. 문서 사본 생성 없음.

---

## 7. 발견 요약 및 권고

### 7-1. 확정 불일치 (수정 권고)

| ID | 항목 | 심각도 | 권고 |
|---|---|---|---|
| GAP-A1 | x_MIT=0.50 vs Ch1 x_MIT≈0.85 | HIGH | round-trip 피팅 후 코드 값 정정 및 Ch1/코드 주석 동기화 |
| GAP-A6 | T3 전이 누락 (Ch1 ~4.17-4.20V) | MEDIUM | tier-C 시연용이면 Ch1 또는 코드 주석에 누락 사유 명기 |

### 7-2. 추정 이슈 (검토 권고)

| ID | 항목 | 심각도 | 권고 |
|---|---|---|---|
| GAP-A2 | MSMR↔logistic 동형 cross-ref 미명시 | LOW | 코드 LCOCathodeDQDV 클래스 docstring에 eq:msmr 참조 1줄 추가 |
| GAP-A3 | func_L_q 파라미터 `x`=χ_d 명칭 혼동 | LOW | docstring에 "x: transfer coefficient χ_d" 명기 |
| GAP-A7 | LCO σ_d 뒤집기 미적용 수식 근거 미명시 | MEDIUM | Ch1 또는 코드 주석에 양극 σ_d 관례 명기 |

### 7-3. 근거미발견 (비-오류)

| ID | 항목 | 설명 |
|---|---|---|
| GAP-A4 | eq:Sedirect 별도 코드 경로 없음 | 공통 결과식 구현으로 실용적 동치, 오류 아님 |

### 7-4. P4 이월 잔존

| 항목 | 현재 상태 |
|---|---|
| x_MIT tier-C | 코드 0.50 vs Ch1 0.85 — round-trip 피팅 전 임시. 이월 잔존 |
| 다온도 T² 곡률 | func_U_j 선형 근사만. eq:U1T2 T² 항 미구현. 이월 잔존 |
| LCO 시연 파라미터 | tier-C 임시값 전체. 신뢰값화 미완. 이월 잔존 |
| 비가역 3분해 | lumped만. Ch2 정합으로 현 단계 적절. 과제 잔존 |

### 7-5. 최종 무결 확인

| 항목 | 결과 |
|---|---|
| 전체 Ch1 수식 → 코드 매핑 | **20개 식 전수 매핑 완료. 불일치 2건(GAP-A1·A6 — P4 이월)** |
| 전체 코드 함수 → Ch1 근거 | **주요 함수 전수 Ch1 근거 있음. GAP-A3·A4·A7 보완 권고** |
| 부호·단위·계수 불일치 | **GAP-A5 수치 검증 확인(−45.7≈−46). 나머지 정합** |
| 3대 무결 | **전원 PASS** |
| P4 이월 문서 정합 | **4건 이월 잔존 확인, 현 단계 의도적** |

---

## 8. 결론

A조(code↔Ch1 상호충실도) 감사 기준으로:

- **Ch1→코드**: 수식 20개 전수 매핑. Ch1 제시 수식이 코드에 1:1로 구현됨. **단 x_MIT(GAP-A1)의 초기값 불일치가 잔존하며 P4 이월 tier-C 상태.**
- **코드→Ch1**: 주요 함수 전수 Ch1 근거 확인. MSMR 동형(GAP-A2), σ_d 방향 근거(GAP-A7)의 명시적 cross-reference 보완 권고.
- **갭·부호·단위·계수**: 수치적 불일치 없음(GAP-A5 수치 검증 통과). x_MIT 위치 불일치(GAP-A1)는 의도적 tier-C placeholder. T3 전이 누락(GAP-A6) 문서 정합 필요.
- **3대 무결**: 식별자·범위·사본 전원 PASS.
- **P4 이월**: 4건 전원 잔존 확인. 현 단계 의도적 미완으로 P5 최종 점검 기록에 명시.

**전체 판정**: 코드와 Ch1 이론의 상호충실도는 주요 물리 수식에서 **높음**. 잔존 갭(GAP-A1·A6)은 tier-C 임시 데이터의 한계이며 round-trip 피팅 후 정정 예정. 코드 추적성 개선(GAP-A2·A3·A7 docstring)은 낮은 우선순위 권고.

---

*감사자: S1 · A조(code↔Ch1 상호충실도) | 2026-07-01 | 코드·문건 수정 없음*
