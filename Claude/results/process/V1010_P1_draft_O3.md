# Anode_Fit v1.0.10 — P1 분석 경쟁 드래프트 **O3**

> 대상: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` (흑연 음극 dQ/dV, 703줄)
> 근거 문건: `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` (식 라벨 인용)
> 산출: ① 플로우차트 맵(물리식+줄번호) ② 조건 audit(충족도·결함·흑연 전용) ③ 피팅 파라미터 인벤토리
> 검산: z_cut·dU_hys·L_q·dH_eff·면적보존 numerically 독립 검증(아래 §0).
> 표기: [확정]=코드·식 직접근거 / [추정] / [근거 미발견]. 코드 수정·commit 없음(분석 전용).

---

## §0. 독립 수치 검산 (작성 전 사전 확인 — 추측 배제용)

| 항목 | 코드/식 주장 | 독립 계산 | 판정 |
|---|---|---|---|
| z_cut=4.357 의미 | 도입부 docstring(L218) "ξ_eq 5%" / tex(L1369-70) "미분 dξ/dq 의 5%" | ξ_eq(z=4.357)=**1.27%**, ξ(1−ξ)/0.25=**5.00%** | **tex 가 정확** — "5%"는 점유가 아니라 **미분**(ξ(1−ξ))의 5%. **docstring(L218) 문구 부정확** (→audit C1) |
| ΔU_hys(Ω=12000,298K) | 자체검증 L644·L1819 "86.7 mV" | u=0.766, ΔU_hys=**86.69 mV** | [확정] 일치 |
| ΔU_hys(Ω≤2RT) | L85·L137 분기 0 | Ω=2RT(=4957.6) → u=0, gap=**0** | [확정] 일치 |
| A 컷(n=1, 기본) | A=min(z_cut·n·RT, A_cap·RT) (L331) | z_cut·RT=**4.357RT** > A_cap=**4.0RT** → 항상 **4.0RT 로 capped** | [확정]·주목: **n=1 데이터셋에서 z_cut 은 절대 binding 안 됨** (→audit D4) |
| L_q(dH_a=44k,I=0.1,χ=0.5) | func_L_q (L100-107) | =1.094e-07 → L_V=*0.30=**3.28e-08** | [확정] 유한·양수 |
| ΔH_a^eff 부호 | dH_a−χ_d·Ω (L155) | χ=0.5 → 방·충 χ_d 동일 0.5 → dH_eff 동일 39000 | [확정]·주목: **χ=0.5 면 충방전 비대칭 0** (→audit D5) |
| 면적보존 (평형) | ∫Q·ξ(1−ξ)/w dV = Q | 수치적분 = **1.000000** | [확정] area-conserving |
| 면적보존 (꼬리) | ∫(ξ_eq−ξ_lag)/L_V dV ≈ Q | 수치적분 = **0.99986** (격자 이산오차) | [확정] DC/면적 보존 (1.0.10 핵심 수정의 목적) |

---

## §1. ★ 플로우차트 맵 — 입력→equilibrium / dqdv→curve

### 1-A. 데이터 흐름 (최상위)

```
[입력] GRAPHITE_STAGING_LIT(L531-560) ─┐
       사용자 transitions dict          ├─→ __init__(L221-259)
       생성자 스칼라(x,Rn,Cbg,chi,…)    ┘    │ 가드(_finite류 L167-188)
                                              │ seed_L_V 산출(_build_seed_L_V L262-269)
                                              ▼
        ┌──────────────────────────────────────────────────────┐
        │  equilibrium(V_n,T)  L350-367   [|I|→0 평형 기준선]   │
        │  dqdv(V_app,T,I_abs,Q_cell,s)  L370-480  [관측 곡선]  │
        │  curve(...)  L483-508  [실험조건 facade → dqdv 재사용]│
        └──────────────────────────────────────────────────────┘
```

### 1-B. 모듈 레벨 물리 함수 (사용자 원형 보존 = L73-128 / 보완 = L132-188)

| 함수 | 줄 | 물리식 (tex 라벨) | 역할 |
|---|---|---|---|
| `func_w(T,n)` | L74-75 | w = nRT/F (eq:weff 비-eff 부분) | 전이 폭 [V] |
| `func_U_j(T,dH,dS)` | L78-79 | U_j = (−ΔH_rxn + TΔS_rxn)/F (func_U_j) | 평형 중심 [V] (열역학 환산) |
| `func_U_j_hys(...)` | L82-91 | U + ½·s·partial·γ·ΔU_hys; ΔU_hys=(2/F)[Ωu−2RT·artanh u], u=√(1−2RT/Ω) (eq:hysdU) | 히스 분기 중심 (원형; **partial_hys=1.0 하드코딩** L90) |
| `func_ksi_eq(T,V_n,U,n,s)` | L94-97 | z=s(V_n−U)/w; ξ=logistic(z) (overflow-safe np.where 분기) (func_ksi_eq) | 평형 점유 ξ_eq |
| `func_L_q(...)` | L100-107 | ln L_q = ln(T*/T) − ln(1+e^{−A/RT}) + ΔG_a/RT − χ·A/RT; T*=(I/Q_cell)h/k_B (eq:Lqfull). **I≤0 → −inf**(L102-103) | 지연 길이(용량축) [무차원 q] |
| `_causal_lowpass(src,Δ,L)` | L110-128 | ρ=e^{−Δ/L}; 1차 IIR 저역통과(scipy.lfilter, except→파이썬 루프 fallback). **L≤0 or 비유한 → 원신호 copy**(L113-114) | 인과 지수기억(eq:memory 합성곱 이산형) |
| `func_dU_hys(T,Ω)` | L133-140 | ΔU_hys (eq:hysdU) — func_U_j_hys 내부와 동일식 추출 | gap 헬퍼 |
| `func_U_branch(T,U,Ω,γ,σ_d,h_η)` | L143-148 | U + ½·σ_d·h_η·γ·ΔU_hys (eq:hyscenter) — **partial_hys 를 h_eta 로 인자화** | 분기 중심 헬퍼 |
| `func_dH_a_eff(dH_a,Ω,χ_d)` | L152-155 | ΔH_a^eff = ΔH_a − χ_d·Ω (eq:dHeff) | 유효 장벽 |
| `func_chi_d(χ,σ_d)` | L158-163 | χ_d = χ(방전 σ_d≥0) / 1−χ(충전) (eq:chid 합-1) | 방향별 전달계수(기본 규칙, 주입 교체 가능) |
| `_finite/_finite_pos/_finite_nonneg` | L167-188 | 유한/양수/비음수 가드 → ValueError | fail-fast 입력 검증 |

### 1-C. `equilibrium()` (L350-367) — **평형 peak, 방향 불변**

```
T 가드(_finite_pos L352) → V=asarray
baseline = Cbg(V) if callable else full(Cbg)   (L354-356)
for tr in transitions:                          (L358)
   U_j = func_U_j(T,dH_rxn,dS_rxn) if (dH_rxn&dS_rxn) else tr['U']   (L359-362)
   n_j = _n_factor(tr,T)   (L363)   ;   w = _width(tr,T)=func_w   (L364)
   ksi_eq = func_ksi_eq(T,V,U_j,n_j)   (L365)   ← s 인자 미전달 = 기본 s=+1
   dqdv += tr['Q'] * ksi_eq*(1−ksi_eq)/w        (L366)  ★ eq:eqpeak
```
- **물리 핵심**: peak = Q_j·ξ(1−ξ)/w = Q_j·|dξ_eq/dV| (대칭 logistic 종, 폭 w, **면적=Q_j**[§0]). **충방전·히스·동역학 전혀 없음** — |I|→0 기준선.
- 히스 분기 중심 미적용(center=U_j 그대로), L_V·꼬리 없음. ★dqdv 와의 차이의 출발점.

### 1-D. `dqdv()` (L370-480) — **관측 곡선, 방향·동역학·히스 전부**

```
σ_d = +1 if s≥0 else −1   (L388)
가드: I_abs(_finite_nonneg), Q_cell(_finite_pos)   (L391-392)
V_in 가드(비어있음·비유한)   (L394-400)
T_input: 스칼라 등온 or V_app 길이 배열=비등온 T(V); 유한·>0 가드   (L402-405)
─ 분극: V_n = V_in − σ_d·I_abs·Rn                  (L408)  ★ eq:hysmaster
─ 작업격자: V_work = linspace(v_lo−pad_lo·span, v_hi+pad_hi·span, n_work)  (L410-416)
            n_work = max(n_work_min, V_n.size*2);  grid_step=V_work[1]−[0]
─ T_work: 배열이면 V_n 정렬 후 np.interp, 아니면 등온 상수   (L418-424)
─ T_rep = mean(T_work)  (L426)  ;  dqdv_work = Cbg baseline  (L427-429)
for tr in transitions:                              (L431)
   U_j = func_U_j(T_work,…) [배열] or tr['U']        (L433-436)
   ★히스 분기중심:                                   (L441-450)
      Ω,γ,h_η = tr.get(...)
      if γ≠0 and Ω>0:
         hys_shift = func_U_branch(T_rep,U_j=0,Ω,γ,σ_d,h_η)   (L447)  ★ eq:hyscenter
         center = U_j + hys_shift            ← σ_d 로 방·충 반대 이동
      else: center = U_j
   n_j=_n_factor(tr,T_work) ; w=_width(tr,T_work)    (L452-453)
   ksi_eq = func_ksi_eq(T_work,V_work,center,n_j,σ_d)  (L455) ← center·σ_d 둘 다 방향
   ─ 지연길이(전이당 상수, 대표 T_rep·n_rep):          (L458-460)
      lag_len_V = _resolve_lag_length(tr,T_rep,I_abs,Q_cell,n_rep,σ_d)
   ─ 분기 스위치:                                     (L462-475)  ★ eq:branch
      if (비유한 lag) or lag < min_lag_grid_steps·grid_step:
          peak_shape = ksi_eq*(1−ksi_eq)/w           ★ 평형 종 직접(eq:eqpeak)
      else:
          σ_d≥0: occ_lagged = _causal_lowpass(ksi, Δ, L_V)            (L471)
          σ_d<0: occ_lagged = _causal_lowpass(ksi[::−1],…)[::−1]      (L473) ★격자역전 eq:reversal
          peak_shape = (ksi_eq − occ_lagged)/lag_len_V               (L475) ★ eq:peakshape
   dqdv_work += tr['Q'] * peak_shape                  (L477)
dqdv_out = np.interp(V_n, V_work, dqdv_work)           (L479)  ← 작업격자→입력격자 보간
return scalar or array                                 (L480)
```

### 1-E. `_resolve_lag_length()` (L303-347) — L_V 동역학 산출

```
'L_V' 직접지정 있으면 → 유한·≥0 가드 후 그대로 (동역학 우회)   (L313-318)
I≤0 or 'dH_a' 키 부재 → 0 (평형 종, 꼬리 없음)                (L319-320)
n_safe=|n_j|; z_cut/A_cap = tr override or 전역                (L328-330)
A = min(z_cut·n_safe·RT, A_cap·RT)                             (L331)  ★ eq:Acut
(chi_d, dH_a_use) = _chi_and_dH_eff(dH_a,Ω,σ_d,tr override)    (L338-339) ★ eq:chid·dHeff
L_q = func_L_q(T,I,Q_cell, dH_a_use, dS_a, x=chi_d, A)         (L342)  ★ eq:Lqfull
비유한 L_q → 0                                                 (L343-344)
return |dVdq_qa| · L_q                                          (L347)  ★ eq:LV
```

### 1-F. `curve()` facade (L483-508) — 새 물리 없음

```
σ_d = _direction_to_sigma(direction)  (L501; 문자열/정수→±1, L510-524)
Q_cell 가드  (L502)
I_abs 미지정이면 |I| = c_rate·Q_cell, 지정이면 그대로  (L503-507)
return self.dqdv(V_app,T,I_use,Q_cell,s=σ_d)  (L508)  ← 내부 dqdv 재사용
```

### 1-G. ★ equilibrium vs dqdv 핵심 차이 (요청 명시 항목)

| 축 | `equilibrium` (L350) | `dqdv` (L370) |
|---|---|---|
| 물리 의미 | |I|→0 **평형 peak**(eq:eqpeak) | **관측 peak**(eq:hysmaster): 평형−지연 |
| peak 형태 | Q·ξ(1−ξ)/w (대칭 logistic 종) | Q·(ξ_eq−ξ_lag)/L_V (지연 꼬리) — 단, lag<2칸이면 평형 종으로 분기(eq:branch) |
| 중심 | U_j (히스 미적용) | center = U_j + ½σ_d h_η γ ΔU_hys (분기, **σ_d 로 방·충 갈림**) |
| 방향성 | **없음**(s 미전달=+1 고정) | σ_d 가 ① 분극 V_n ② 분기중심 ③ χ_d/ΔH_eff ④ 격자역전 4곳에 |
| 분극 | 없음(V_n 직접) | V_n = V_app − σ_d·I_abs·Rn |
| 동역학 | 없음 | L_V(T,I,Q_cell,A,χ_d,ΔH_eff) 꼬리 |
| 격자 | 입력 V 직접 | 패딩 작업격자 + 보간(꼬리 양끝 여유) |
| 관측되는 것 | 평형 분포(이상) | **꼬리·히스 포함 실측 dQ/dV** |

> **요청 핵심 답**: equilibrium 은 *평형 peak*(분포 자체, 방향 불변), dqdv 는 *관측 꼬리·히스*(완화 지연으로 평형이 늦게 따라오며 생기는 비대칭 꼬리 + 히스 분기 중심). dqdv 가 |I|→0(L_V→0)이면 분기 스위치(eq:branch)로 equilibrium 의 peak 형태로 환원되나, **center 에 히스 분기는 잔존**(γ>0 이면 |I|→0 에서도 충방전 peak 위치 갈림 — 자체검증 L637-646 이 이를 실증).

---

## §2. ★ 조건 audit — 충족도·결함·흑연 전용

### 2-A. 물리수식 충족도 [확정]

| 식 (tex) | 코드 구현 | 충족 |
|---|---|---|
| 분극 V_n=V_app−σ_d|I|R_n | L408 | ✔ |
| 평형중심 U_j=(−ΔH+TΔS)/F | func_U_j L79 | ✔ |
| 히스 gap ΔU_hys (artanh) | func_dU_hys L133-140 / func_U_j_hys L88-89 | ✔ (두 곳 동일식) |
| 분기중심 U^d=U+½σ_d h_η γ ΔU_hys | func_U_branch L148, 호출 L447 | ✔ |
| 폭 w=nRT/F | func_w L75 | ✔ (w_eff 제거됨 = 1.0.10 변경) |
| 평형점유 ξ_eq=logistic[s(V−U)/w] | func_ksi_eq L96-97 (overflow-safe) | ✔ |
| 평형 peak Q·ξ(1−ξ)/w | L366·L464 | ✔ (면적=Q 검산 §0) |
| χ_d 합-1 | func_chi_d L163 | ✔ |
| L_q (eq:Lqfull) | func_L_q L106 | ✔ (로그식 직접대응 §0) |
| ΔH_a^eff=ΔH_a−χ_d·Ω | func_dH_a_eff L155 | ✔ |
| 꼬리 인과기억(σ_d) | _causal_lowpass + 격자역전 L470-473 | ✔ |
| 합산 dQ/dV=C_bg+ΣQ_j[평형−꼬리] | L477·L427 | ✔ |

→ tex L51 의 closed-form 12개 식 **전부 코드에 매핑** [확정].

### 2-B. 부호·차원·극한 검산 [확정]

- **차원**: w=[V], U=[V], ξ 무차원, ξ(1−ξ)/w=[1/V], Q·[1/V]·[전하]=dQ/dV 차원 일치. L_q=T*/T·exp(…)=무차원(용량 분율), L_V=|dV/dq|·L_q=[V]. ✔
- **부호**: 분극 σ_d 방향(방전 V_n<V_app, 충전 >); 분기 σ_d 로 대칭 이동; χ_d 방전 χ/충전 1−χ. ✔
- **극한**:
  - Ω≤2RT → ΔU_hys=0 (NaN 영역 차단 L85/L137). ✔ 검산 §0.
  - |I|→0 → T*∝|I|→0 → L_V→0 → 분기 스위치로 평형 종. 자체검증 L662-665 (dis/chg diff~0). ✔
  - γ=0 → hys_shift=0 → center=U_j. ✔
  - T 배열(비등온) → T_work interp, U_j·w 배열 대응. ✔

### 2-C. 가드·死코드·시그널체인·면적보존 결함

| ID | 심각도 | 위치 | 내용 | 근거 |
|---|---|---|---|---|
| **C1** | LOW(문서) | L218 docstring | "z_cut … (기본 4.357 = ξ_eq 5%)" — **점유 5%가 아니라 미분(dξ/dq) 5%**(ξ_eq 자체는 1.27%). tex L1369-70 은 정확. **코드 docstring 만 부정확**. | §0 검산 |
| **C2** | LOW | L236 | `self.Cbg` 만 가드 면제("사용자 책임" 주석). callable Cbg 가 비유한 반환 시 출력 오염 가능(설계상 의도적). | 코드 주석 |
| **D4** | INFO | L331 | n=1 데이터셋(GRAPHITE_STAGING_LIT 전부 'n':1.0)에서 z_cut·RT=4.357RT > A_cap=4.0RT → **A 항상 4.0RT 로 capped, z_cut binding 안 됨**. z_cut override 는 n≠1 또는 z_cut<4.0 일 때만 효과. 자체검증 L687-698 은 z_cut=2.0(<4) 로 격리 확인 — 즉 의도된 동작이나 기본 데이터셋에선 inert. | §0 검산 + L691 |
| **D5** | INFO | L163·L298 | χ=0.5(기본 x=0.5)면 충방전 χ_d 동일(0.5) → ΔH_eff·L_q **충방전 비대칭 0**. 비대칭은 χ≠0.5 일 때만. 자체검증 L622-635 이 chi=0.5 + custom split(충전 0.3)으로 차이 실증. | §0 검산 |
| **D6** | INFO(死) | L210·L617 | `curve()` docstring 의 "sto" 편의 언급 있으나 sto→V 매핑은 사용자 책임(코드 내 q→V 변환 없음). 기능 부재 아님(설계 경계). | L617 주석 |
| **G1** | NOTE | L462-475 | **분기 스위치 진폭 불연속**: 문턱 L_V=ν·Δ_grid 에서 꼬리 분기 진폭과 평형 종 진폭(∝1/w)이 정확히 일치하도록 맞춰져 있지 **않음** → 작은 점프 가능. tex L1529-1533 이 명시적으로 인정(실용적 선택, ν↑로 완화). **버그 아님, 알려진 이산 모드 스위치**. | tex L1529 |
| **G2** | NOTE | L319 | `'dH_a'` 키 부재 → L_V=0(평형 종). 동역학 키 없는 전이는 자동 평형 처리 — 의도된 graceful fallback. | L319 주석 |

**死코드 판정**: [근거 미발견] 진짜 死코드(도달 불가) 없음. v11_final 재검수에서 死변수 U_j_rep 제거·func_U_branch 활성화 완료(헤더 L15-16). `func_U_j_hys`(L82) 는 모듈에 존재하나 클래스 내부는 func_U_branch 를 호출(L447) — func_U_j_hys 자체는 **클래스에서 미호출**(외부 API/하위호환용으로 보존, 死코드 아님 = 공개 함수). [추정]

**면적보존**: [확정] 평형(∫=1.000)·꼬리(∫=0.99986) 모두 보존. 1.0.10 변경(L7)이 use_w_eff 제거로 ξ_eq 폭과 분모 w 불일치(면적 깨짐 버그)를 바로잡은 것 — 헤더 주장과 수치 일치.

**시그널 체인**: σ_d 가 dqdv 진입(L388)→분극(L408)→분기중심(L447)→ksi_eq(L455)→_resolve_lag_length(L460)→χ_d/ΔH_eff(L338)→격자역전(L470-473) 까지 일관 전파. seed_L_V 는 σ_d=+1 고정(L268, 진단용). 끊김 [근거 미발견].

### 2-D. ★ 흑연 전용 (LCO·발열·전자엔트로피 부재) [확정]

- **LCO 부재**: 코드에 LCO/cobalt/order-disorder 항 없음. 단 tex L1145-1151 은 평형 peak 식이 전극 불문 LCO 에도 적용 가능하다고 명시 — **코드는 흑연 staging 데이터셋만 내장**(GRAPHITE_STAGING_LIT, stage 4→3/3→2L/2L→2/2→1). LCO 전용 항(큰 Ω order-disorder) 없음 = **흑연 음극 전용**. ✔
- **발열(thermal/self-heating) 부재**: T 는 외생 입력(등온 스칼라 or T(V) 프로파일 L402-424). 발열항·열생성·dT/dt 결합 **없음**. 비등온은 T(V) 프로파일을 사용자가 주입할 뿐 내부 열모델 아님. ✔
- **전자 엔트로피(electronic entropy) 부재**: ΔS_rxn(L78, 격자/구성 엔트로피, U_j 환산)·ΔS_a(L100, 활성화 엔트로피)만. 전자 상태밀도 기반 전자 엔트로피항 **없음**. ✔
- → 세 부재 모두 [확정]: 본 모델은 **흑연 음극 staging dQ/dV 의 평형+동역학 꼬리+히스** 전용. 양극(LCO)·열·전자구조 확장 없음.

---

## §3. ★ 피팅 파라미터 인벤토리

> "지배영역" = dQ/dV 곡선에서 그 파라미터가 주로 형태를 좌우하는 곳.
> 초기값 = GRAPHITE_STAGING_LIT(stage 2→1, 만충, L553-559) 기준 + 생성자 기본값.

| 기호 | 코드 키/인자 | 줄 | 역할 | 지배영역 | 초기값 | 자유/고정 |
|---|---|---|---|---|---|---|
| **n_j** | `'n'`(또는 'w' 역산) | L272-278 | 폭 다중도 w=nRT/F | peak **폭**(전이 전체) | 1.0 (전 stage) | 자유(폭 핸들; 'n' 우선, 없으면 'w'→n 역산, 없으면 1) |
| **U_j** | `'U'` 또는 (`dH_rxn`,`dS_rxn`) | L78,L360 | 평형 중심 | peak **위치**(V축) | 0.085 V (또는 ΔH=−13000,ΔS=−16) | 자유(열역학 환산 우선) |
| **Ω_j** | `'Omega'` | L441,L335 | 정규용액 상호작용 | 히스 **gap 크기** + ΔH_eff 보정 | 13000 J/mol | 자유(상분리·히스; Ω≤2RT 면 히스 0) |
| **dH_a** | `'dH_a'` | L333,L536… | 활성화 엔탈피 | **꼬리 길이 L_V**(exp 지수) | 40000 J/mol(만충)~48000(저SOC) | 자유(동역학; 키 부재 시 꼬리 0) |
| **χ** | 생성자 `chi`/`x` | L210,L237 | 전이상태 분율(전달계수 핸들) | 꼬리 **충방전 비대칭** | 0.5 (x 기본) | 자유(χ=0.5 면 비대칭 0; chi_split 규칙 교체 가능) |
| **L_V** | `'L_V'` (선택) | L209,L313 | 지연 길이 직접지정 | 꼬리 **길이**(동역학 우회) | 미지정(동역학 산출) | 자유·override(피팅/테스트용) |
| **z_cut** | `z_cut`/tr override | L226,L329 | 컷 affinity z=A/(nRT) | 꼬리 **시작점 구동력**(L_q) | 4.357 | **준고정**(n=1 에선 A_cap 에 capped, inert — D4) |
| **dVdq_qa** | `'dVdq_qa'` | L347,L536… | 컷점 OCV 기울기 |dV/dq| | L_q→**L_V 환산**(꼬리 진폭) | 0.30 V | 자유(fit; 부재 시 0=꼬리 0) |

**보조 파라미터(2차)**:

| 기호 | 키/인자 | 줄 | 역할 | 자유/고정 |
|---|---|---|---|---|
| Q_j | `'Q'` | L366,L477 | 전이 용량 가중(peak 면적) | 자유 (0.10/0.12/0.25/0.50) |
| dS_rxn | `'dS_rxn'` | L78 | U_j 온도의존(ΔS) | 자유 |
| dS_a | `'dS_a'` | L100,L334 | 활성화 엔트로피(L_q 온도) | 자유(기본 0) |
| γ_j | `'gamma'` | L442 | 히스 분기 축소인자(γ=1 spinodal 상한, 0 소멸) | 자유(기본 0=히스 off) |
| h_η | `'h_eta'` | L443 | 부분 cycle 인자 | 자유(기본 1.0) |
| A_cap_RT | `A_cap_RT`/override | L226,L330 | 컷 affinity 상한(RT 배수) | 준고정(기본 4.0) |
| Rn | 생성자 `Rn` | L235,L408 | 직렬저항(분극) | 자유(기본 0) |
| Cbg | 생성자 `Cbg` | L236 | 배경 dQ/dV(상수 or V함수) | 자유(기본 0) |
| use_dH_eff | 생성자/override | L225,L298 | ΔH_eff 보강 토글 | 고정 bool(기본 True) |
| s/σ_d | dqdv `s` | L375,L388 | 방향(±1) | 입력(피팅 아님) |

> **곡선 지배영역 요약**: U_j=peak 위치 / n_j(w)=peak 폭 / Q_j=peak 면적 / Ω_j·γ=히스 분기 / dH_a·dVdq_qa=꼬리 길이·진폭 / χ=꼬리 충방전 비대칭 / z_cut·A_cap=꼬리 시작 구동력(n=1 에선 사실상 A_cap 만). [확정 — 줄·식 근거]

---

## §4. 종합 판정

- 충족도: tex closed-form 12식 **전부 매핑**, 면적보존 수치 확인, 부호·차원·극한 일관. [확정]
- 결함: 진짜 버그·死코드 **없음**. LOW 1건(C1: docstring "ξ_eq 5%" 부정확 — 실은 미분 5%), 알려진 NOTE 2건(G1 분기 스위치 진폭 불연속 = tex 인정 / D4 z_cut n=1 inert / D5 χ=0.5 비대칭 0). 모두 설계상 의도이거나 문서 표현 문제.
- 흑연 전용: LCO·발열·전자엔트로피 3부재 [확정].
- 不확실: func_U_j_hys 클래스 미호출(공개 API 보존 추정) [추정]; 그 외 [근거 미발견] 항목 명시.
