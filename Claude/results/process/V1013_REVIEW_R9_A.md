# V1013 REVIEW — Round 9, 검수자 A (코드 인용 단위 청크)

- 대상: `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` (전문 2,933줄, Read 줄번호 기준) ↔ `Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py` (전문 883줄)
- 청크 스킴: **코드 인용 하나씩** [tex 인용 원문 ↔ py 실제 원문 verbatim 대조 → 동작 서술 대조]. R2~R8 동안 py 6회 수정 이력 반영, **최종 py 기준 전수 재대조**.
- 보조 대조: py 가 인용하는 Ch2 라벨은 `graphite_ica_ch2_v1.0.13.tex` 를 grep+해당 절 부분 정독으로 확인(eq:weighted L486·eq:hys_rev L610·eq:qrev L676·§2.6=sec:revheat 6번째 \section·keybox 종합식 L699-705).
- 역할 준수: 검수 의견만 — tex/py 무수정. 모든 지적에 양쪽 줄 번호·원문 병기.

---

## 1. 지적 사항

### F1 [LOW] py 내부 use_w_eff 제거 시점 라벨 모순 ("v12" stale)
- **위치**: py L312 (`_width` docstring) ↔ py L4·L8 (헤더) ↔ tex L24-25 (계보 주석)
- **무엇이**: py L312 `"(use_w_eff 경로는 ξ_eq 폭·분모 불일치로 면적보존 깨지는 버그 — v12에서 제거.)"` 가 py L4 계보 `"v11_final → use_w_eff 제거 → 1.0.10 → 1.0.12 → 1.0.13"` 및 L8 `"[1.0.10 변경] use_w_eff 경로 제거"` 와 모순. 계보상 제거는 1.0.10 진입 시점이고 "v12" 라는 판본은 계보에 없다(1.0.12 는 제거 이후).
- **근거**: tex 헤더 L24-25 도 "w_eff 완전제거" 를 v10-10(→1.0.10) 블록에 기록.
- **수정안**: py L312 를 "…버그 — 1.0.10에서 제거." 로 현행화.

### F2 [LOW] py 헤더 [근거 문건] L_q 요약식에서 −TΔS_a 항 누락
- **위치**: py L48-49 ↔ py L108-109 (`func_L_q`) ↔ tex L1599-1609 (eq:Lqfull)
- **무엇이**: py L48 `"L_q = (|I|h/Q_cell kB T)·e^{(ΔH_a^eff−χ_d A)/RT}/(1+e^{−A/RT})"` — 구현은 `dG_a = dH_a - T * dS_a` (py L108) 로 −TΔS_a 를 포함하고, tex eq:Lqfull 도 `exp[(ΔH_a^eff−TΔS_a)/RT]` 를 명시. 헤더 요약식만 dS_a=0 특수형인데 무표기.
- **근거**: 헤더 블록 서두가 "본 구현이 따르는 식" 이라 자구 정합 기대치가 있는 자리.
- **수정안**: 지수를 `(ΔH_a^eff−TΔS_a−χ_d A)/RT` 로 고치거나 "(dS_a=0 형)" 병기.

### F3 [LOW] LCO 데이터셋 머리 주석 "방전 σ_d=+1(LCO 리튬화)" — 슬롯 규약 한정어 누락
- **위치**: py L633-634 (`LCO_MSMR_LIT` 머리) ↔ tex L1916-1921 (eq:lco-sigmaslot) ↔ py L667-671 (LCO 클래스 docstring)
- **무엇이**: py L633-634 `"방전 σ_d=+1(LCO 리튬화)·부호 골격 흑연 동일(Ch1 Part II sec:lco-map·sec:lco-direction)"`. eq:lco-sigmaslot 은 "σ_d=+1 ⇔ 탈리튬화 ⇔ LCO 하프셀 충전↦+1" 이므로, 이 문장을 자구대로 읽으면 σ_d=+1 슬롯에 리튬화가 배정된 듯 규약과 충돌. 실제 의도(클래스 docstring L667-671)는 "방전 σ_d=+1 은 LCO 엔 리튬화이며 … σ_d 를 뒤집지 않는다 — **단 이는 평형·∂U/∂T 경로 한정**" 인데, 데이터셋 주석엔 이 한정어가 없다. v1.0.13 루프 B 이후 `curve(direction='discharge')` 는 LCO 에서 σ_d=−1 로 환산되므로(_delith_is_discharge=False, py L531-535) 무한정 문장은 curve 경로와도 어긋나게 읽힌다.
- **수정안**: py L633-634 에 "(평형·∂U/∂T 경로 한정 — 방향 작용처의 슬롯은 탈리튬화=+1, eq:lco-sigmaslot; curve 라벨은 자동 환산)" 병기.

### F4 [LOW] tab:lco-staging 캡션의 "코드 시연값 별개" 선언이 U 값만 커버 — ΔS 불일치 무언급
- **위치**: tex L1886-1891 (tab:lco-staging 캡션) ↔ tex L1897-1899 (표 ΔS 열) ↔ py L648·L653·L657 (dS_rxn +6.0/−4.0/−2.0)
- **무엇이**: 캡션은 "코드 LCO_MSMR_LIT 시연값(U=3.930/3.880/4.050 V; …)은 tier-C 시연 초기값으로, **U 세 값은** 본 표의 물리 anchor 와 별개라 round-trip 피팅으로 정합한다" 라고 U 만 명시. 표의 ΔS 초기값(T2 config≈0.47, T3≈1.49 J/(mol K), 양수)과 코드 시연 dS_rxn(−4.0/−2.0, 음수)은 부호까지 다른데 별개성 선언에 포함되지 않아, 코드 dS_rxn 을 표 anchor 정합값으로 오독할 여지.
- **수정안**: 캡션 문구를 "U·ΔS_rxn 시연값은 … 별개라" 로 확장(1어절 수정).

### F5 [INFO] 인용 자구 미세 불일치 2건 (동작 동일 — verbatim 아님)
- **위치**: tex L1796 ↔ py L506; tex L1345 ↔ py L493
- **무엇이**: ① tex `"코드는 \code{dqdv\_work += tr['Q'] * peak\_shape} 로 누적하고"` — py 원문은 `dqdv_work = dqdv_work + tr['Q'] * peak_shape` (+= 미사용, 비변조 대입). ② tex `\code{peak\_shape = ksi\_eq * (1 - ksi\_eq) / w}` — py 는 `(1.0 - ksi_eq)`. 수치·동작 완전 동일, 인용 표기 관례 수준.
- **수정안**(선택): ① 을 `dqdv_work = dqdv_work + …` 로 자구 일치시키거나 "누적한다(비변조 대입)" 로 서술화.

### F6 [INFO] 하드코딩 상수 2건 vs "내부 하드코딩 상수는 없다" 원칙 문구
- **위치**: py L220-222 (클래스 docstring 원칙) ↔ py L701 (`T_ref = 298.15`, LCO `_effective_dS_rxn`) · py L574 (`eps = 1e-12`, `entropy_coefficient`) ↔ tex tab:inputs L2756-2793 (T_ref 행 없음)
- **무엇이**: 원칙 문구 "커브식의 모든 기호 = 코드 입력 … 내부 하드코딩 상수는 없다" 와 달리 T_ref(물리 기준온도)·eps(수치 가드)가 인자 미노출. tex 는 동결 근사 자체는 명시(L2726-2729·tab:lco-staging 캡션)하므로 서술-코드 동작 정합은 유지 — 원칙 문구와의 긴장만.
- **수정안**(선택): T_ref 인자 노출 또는 원칙 문구에 "(LCO T_ref 동결·수치 eps 제외)" 예외 명시 + tab:inputs 에 T_ref 행.

### F7 [INFO] py `reversible_heat` 의 "방전 I>0" — Ch2 가 경고한 라벨 층위 무주석
- **위치**: py L599 ↔ Ch2 tex L680-683
- **무엇이**: py docstring `"방전 I>0: ΔS>0(∂U/∂T>0) → q_rev<0 흡열"`. Ch2 는 같은 자리에서 "★라벨 층위 주의 — Bernardi 관례의 방전(I>0)=흑연 하프셀 리튬화, Ch1 방전 라벨과 **반대 화학 방향**" 을 명시 경고. py 는 "(Ch2 부호규약)" 포인터만 있고 한정어가 없어 Ch1 σ_d=+1(탈리튬화) 방전과 혼동 소지.
- **수정안**: docstring 에 "(Bernardi 셀-수지 라벨 — Ch1 σ_d 방전 라벨과 별개, Ch2 라벨 층위 주의 참조)" 한 줄 병기.

---

## 2. 전수 대조 PASS 확정 목록 (요지)

**codebox 2/2**: ① N2 (tex L932-939) — `if 'dH_rxn' in tr and 'dS_rxn' in tr` = py L462 자구 일치, seam `_effective_dS_rxn` 경유 명시 = py L463 정합, stage 2→1 검산 (13000−298.15×16)/96485=0.08529→0.0853 ✓. ② N7 (tex L1631-1636) — n_safe=|n_j| (py L357)·`_chi_and_dH_eff` (py L367)·`func_L_q(...,x=chi_d,A=A)` (py L371 위치인자 정합)·`|dVdq_qa|*L_q` (py L376)·전이당 상수 T_rep·n_rep 1회 평가 (py L486-489) 전부 ✓.

**주요 인용/동작 서술 30+건 ✓**: V_n 식 (tex L842=py L437 verbatim) · 작업격자 패딩 0.15/n_work=max(2048,2·len)/v_span_floor 1e-6/T_rep=mean(T_work) (tex L851-859=py L439-455) · func_U_j `(-dH_rxn+T*dS_rxn)/F` (tex L925=py L80) · func_dU_hys `(2/F)*(Omega*u−2RT·arctanh u)`·Ω≤2RT→0 (tex L973·L1041=py L136-143) · func_U_branch `U_j+0.5*sigma_d*h_eta*gamma*…` (tex L1059-1060=py L151) · hys_shift=func_U_branch(T_rep,0,…), 조건 γ≠0∧Ω>0 (tex L1064-1069=py L473-477) · func_w `n*R*T/F`·'w'→n 역산·'n' 우선(tex L1120-1121·L1395-1397=py L75-76·L301-307) · func_ksi_eq `np.where(z>=0,…)` 오버플로 분기 (tex L1178-1179=py L99-100) · 호출 `func_ksi_eq(T_work,V_work,center,n_j,sigma_d)` (tex L1180-1182=py L484) · 평형 peak `ksi_eq*(1-ksi_eq)/w`·equilibrium=U_j 중심 무분기·s=1 (tex L1345-1348=py L379-396·L493) · A=min(z_cut·n_safe·RT, A_cap·RT), z_cut 4.357=미분 종 5% 컷(수치 재검산: ξ(1−ξ)=0.0125 ⇔ z=4.357 ✓), A_cap 4.0 (tex L1563-1567=py L255·L360) · func_chi_d σ_d≥0→χ/else 1−χ (tex L1576-1580=py L166) · use_dH_eff 분기·per-tr override (tex L1592-1593·L1613-1616=py L322-329·L368) · func_L_q ln 사슬·T_attempt=(I/Q_cell)h/kB=T_* (tex L1611-1613=py L107-109) · L_V override/I≤0/dH_a 부재→0 (tex L1628-1629=py L342-349) · lfilter 계수 [1−ρ]/[1,−ρ]·zi 초기화 ξ_lag,0=ξ_eq,0·fallback 점화식·L_V≤0/비유한→원신호 (tex L1667-1669=py L113-131) · peak_shape=(ksi_eq−occ_lagged)/lag_len_V (tex L1706=py L504) · 분기 스위치 L_V<ν·Δ_grid(ν=2)∨비유한 (tex L1713-1722=py L257·L491) · 충전 격자 역전 `[::-1]…[::-1]` (tex L1737-1744=py L499-502) · 합산·np.interp 역보간·스칼라 첫 성분 반환 (tex L1796-1798=py L506-509) · curve facade: `_direction_to_sigma`·|I|=c_rate·Q_cell·I_abs 우선·LCO 라벨 플립 'charge'→+1 (tex L2811-2815=py L530-542·L686) · ν=2 점프 23%·ν=8 6.1%·ν=10 4.9% 수치 재계산 ✓ (tex L1725-1727).

**데이터셋 ✓**: tab:staging 4전이×7값 = GRAPHITE_STAGING_LIT (py L711-740) 전수 일치, U(298) 4건 재계산(0.2109/0.1399/0.1203/0.0853) = tex L1824 "±1 mV·4→3 만 0.2109" 정합, w 폴백 0.020/0.016/0.014/0.012 ✓. LCO_MSMR_LIT U 3.930/3.880/4.050·electronic/x_center/g_max_eV/x_MIT/dx_MIT = tab:lco-staging 캡션·tab:inputs LCO 행 ✓. dict dH 재역산 3건 독립 재계산: −391016.05/−375554.4/−391360.55 → py −391016.1/−375554.4/−391360.0 (T3 −0.55 J/mol 은 U(298) −6 μV 급, 표시 정밀도 아래) ✓. ΔS_e(x_MIT,298.15) 재계산 −45.679 = py 주석 −45.678·tex ≈−46 ✓.

**py→tex 라벨 58건 전수 실재 ✓**: ch1 26종(eq:vn·Uj·dUhys·Ubranch·wbase·xieq·eqpeak·belliden·chid·Lqfull·LV·dHeff·memory·peakshape·sum·gunit·dSegate·U1T2·lco-sigmaslot·lco-msmrmap, sec:lco-Se·lco-decomp·lco-code·lco-map·lco-direction, tab:lco-staging) + ch2 7종(eq:Z1 L129·muV L147·logistic L160·Vxi L183·weighted L486·hys_rev L610·qrev L676). py L558 "§2.6 keybox 종합식" = ch2 6번째 \section(sec:revheat) 의 keybox(L699-705) ✓ — `entropy_coefficient` 구현식(가중 [ΔS_eff/F+(n_j R/F)ln(ξ/(1−ξ))])과 1:1, config 계수 n_jR/F = ch2 eq:dxidT 의 ∂w_j/∂T ✓. reversible_heat −I·T·∂U/∂T(T 한 번) = ch2 eq:qrev ✓. irreversible_heat lumped-only 주장 = ch2 eq:qrev 주변 lumped 제시와 정합(3분해 boxed 식 부재 — 해당 절 부분 정독 기준) ✓.

**self-test(__main__) ✓**: R1 재계산 u=0.76608·ΔU_hys=86.69 mV = tex R1 "0.766·86.7 mV" = py hys 테스트 기대식 d(dis−chg)=+γ·dU_hys ✓ / R2 Ω=2RT=4957.6(tex "4958")→0 = py L839-840 ✓ / R3 γ=0·|I|=1e-6 dis≡chg = py L841-845 ✓ / 가드 7/7 목록·per-tr override 격리·facade max_diff<1e-12 — 문건 주장과 모순 없음.

**렌즈 ⑧ (R8 nodemap 신규 행) ✓**: N5+ `func_dSe_molar` — 물리식 열 N_A(π²/3)k_B²T·∂g/∂x = (π²/3)Rk_BT·∂g/∂x (N_Ak_B²=Rk_B) = eq:dSemolar 와 항등, 부호 <0(삽입)·식번호 eq:dSemolar·eq:ggate 정합, 구현(py L188)은 eq:dSegate×eq:gunit(나눗셈)×eq:dSemolar 합성형과 일치. N9' `_effective_dS_rxn` — eq:lco-decomp 의 elec plug-in seam, 세 경로 공유(equilibrium L389·dqdv L463·entropy_coefficient L577) ✓, 동결 T_ref 구현은 tex L2725-2729 현행 구현 선언과 정합.

---

## 3. 가장 약한 1곳

**F3 — py L633-634 의 무한정 "방전 σ_d=+1(LCO 리튬화)"**. 부호 규약은 문건이 선언한 ★최우선 결함 클래스이고, 이 주석은 LCO 데이터셋 사용자가 가장 먼저 만나는 자리인데 eq:lco-sigmaslot(σ_d=+1=탈리튬화=LCO 충전) 와 자구 충돌로 읽힌다. 정합 정보(평형 경로 한정)는 8줄 아래 클래스 docstring 에만 있다 — 압축 주석 한 줄에 한정어를 병기하면 닫힌다.

## 4. 물리 불변 확인

지적 7건 전부 주석·캡션·docstring 층위 — 물리식·부호·수치·코드 동작 변경을 요구하는 항목 0. 부호 사슬 S1–S8(tex L2857-2875)·회귀 R1–R5 를 py 구현과 교차 재검산한 결과 모순 0: 분극 부호(py L437)·logistic 방향(py L99-100)·평형 종 방향 불변(py L493)·분기 ±½σ_d(py L151)·χ_d 합-1 거울(py L166)·A 컷 동결(py L360, min 밖 σ_d)·충전 격자 역전(py L502)·ΔU_hys≥0·Ω≤2RT→0(py L140-141) 전부 문건 주장과 일치.

## 5. Coverage 선언

- **codebox**: 2/2 (tex 전체 `\begin{codebox}` grep 결과 L932·L1631 뿐 — 전수).
- **코드 인용/동작 서술 단위**: 36 단위 대조(§2 목록) + 표 3종(tab:staging·tab:lco-staging·tab:inputs) 전 행 + nodemap 15행 + keybox 6단계 + signbox/verifybox R1–R5.
- **py 함수**: 모듈 함수 14(func_w·func_U_j·func_U_j_hys·func_ksi_eq·func_L_q·_causal_lowpass·func_dU_hys·func_U_branch·func_dH_a_eff·func_chi_d·func_dSe_molar·_finite·_finite_pos·_finite_nonneg) + Graphite 메서드 15 + LCO override 1 = 30 전수 정독, 데이터셋 2·__main__ 블록 포함 py 883줄 100%.
- **정독 범위**: tex 1–2933 전 구간(부분 Read 7회로 빈틈 없이 cover), py 1–883 전 구간. missing = 0.

## 6. 5줄 요약 (오적발 자기표시)

1. CRIT/HIGH 0 — 최종 py 기준 codebox 2건·인용 36단위·라벨 58건·데이터셋·self-test 전수 재대조 결과 물리·부호·수치 불일치 없음.
2. 확정 LOW 2건: F1(py L312 "v12에서 제거" stale — 계보상 1.0.10)·F2(py L48 L_q 요약식 −TΔS_a 누락 — 자구 대조로 확정).
3. LOW 2건은 해석 여지 있음: F3(py L633-634 부호 한정어 누락 — 클래스 docstring 이 정합 정보 보유, **이전 라운드가 의도적 압축으로 수용했을 가능성 → 오적발 여지 중**)·F4(tab:lco-staging 캡션 ΔS 별개성 무언급 — tier-C 우산으로 묵시 커버 가능 → 오적발 여지 중).
4. INFO 3건(F5 자구 +=·F6 T_ref/eps 하드코딩 vs 원칙 문구·F7 Bernardi 방전 라벨 무주석)은 수용/기각 자유 — 동작·물리 무영향 확정.
5. 가장 약한 1곳 = F3; 물리 불변 유지 — 본 라운드 수정 요구는 전부 주석·캡션 1줄 수준.
