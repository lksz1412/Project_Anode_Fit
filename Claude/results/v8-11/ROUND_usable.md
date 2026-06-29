# ROUND_usable — v8-11 G-derive(가독·유도) · G-usable(재현) 통독 검수

검수 sub(리뷰 전용). 대상 = `v8-11/v8-11.tex`(1210줄, 서론→N9→부호검산 전문 통독).
기준 = `v7-00_spine/Anode_Fit_v11_final.py`(707줄) 정독 · `v7-11/v7-11.tex`(890줄) 배치 대조.
방식 = 절 단위 청크 순차 통독(처음→끝 따라 읽으며 막힘·재현불가 적발). refute mandate·빈 통과 금지.

수치 load-bearing 항은 직접 재산출 검증(아래 [검증완료] 표기):
R1 u=0.766·ΔU_hys=86.7 mV / R2 Ω=2RT→0 / N2 U(298)=0.0853 V / spinodal→artanh 닫힌식 = V_eq 직접차 86.7 mV 일치 / RT/F=25.7 mV / z_cut=4.357 → logistic 미분 정확히 0.05(5%컷). 전부 본문 수치와 일치.

---

## 1. G-derive 막힘 — 11식 유도를 학부생이 앞 식만으로 따라가나

11개 결과 박스 유도를 (a)출발→(b)연산→(c)중간식→(d)박스 4-step 으로 전수 추적. 결론 = **치명적 비약 0**. 비약·미정의·중복으로 학부생이 멈출 수 있는 지점은 아래 LOW 5건뿐(전부 "막혀서 못 따라감"이 아니라 "한 번 더 짚었으면" 수준).

### 따라가짐 PASS (막힘 없음) — 핵심 유도
- **eq:vn(분극)**: (a)V_app=V_n+σ|I|R_n 출발 → (b)이항 → (c)eq:vnmid → (d)박스. v7-11 은 박스만, v8-11 은 출발식 eq:vapppol 신설. 매끈. [PASS]
- **eq:Uj(평형중심)**: G≡H−TS, μ≡∂G/∂n 정의부터 → 전기화학 평형 eq:eqbalance → 상수 덩이 sFU 흡수 eq:eqcond(ΔG=−sFU) → ΔG=ΔH−TΔS 대입 → 박스. 통계역학 다리(eq:gibbsdef·eq:mudef·eq:eqbalance) 신설로 v7-11 의 "전자 항이 −FV 로 들어오므로" 압축이 완전 해소. [PASS]
- **eq:dUhys(spinodal→artanh)**: 격자기체 ḡ(θ) Stirling → μ eq:mu → g(ξ) eq:gxi → g''(ξ) eq:gpp → spinodal 근 eq:spinodal → V_eq(ξ) eq:Veq → spinodal 대입 eq:hyssub → 극대−극소 차 eq:hysdiff → 박스. 두 로그 부호상쇄·−4·artanh 변환까지 둘째 줄에 명시. **가장 긴 유도인데 한 칸도 안 빠짐.** [검증완료: 닫힌식=직접차 86.7mV] [PASS]
- **eq:Ubranch(분기중심)**: 두 spinodal 평균=U_j(eq:hyssym, 로그합·(1−2ξ)합 둘 다 0) → γ·h_η 한 자유도 → 박스. [PASS]
- **eq:xieq(logistic)**: Eyring k=k0 e^{−ΔGa/RT} → 비대칭 장벽 r±(eq:bv) → 비 취해 detailed balance eq:db(χ 상쇄) → 운동방정식 dξ/dt=k(ξ_eq−ξ) → 정지점 logit eq:logisticsolve → 박스. detailed balance 가 "χ+(1−χ)=1 합-1 강제 결과"임을 명시. [PASS]
- **eq:eqpeak(평형 peak)**: 전하보존 Q_cell q=Q_bg+ΣQ_jξ_j 를 q 미분 → 종 항등식 eq:belliden(ξ(1−ξ)) → 연쇄율 dz/dV=σ/w → 박스. v7-11 압축본보다 보존식 미분 단계가 전개됨. [PASS]
- **eq:Lq(용량축 길이)**: 운동방정식을 dq/dt=|I|/Q_cell 로 나눠 → 지연변수 r_j → eq:Lqmid → L_q=|I|/(Q_cell k_j) 박스. 이어 k_j=r+(1+e^{−A/RT}) 분해(eq:kuniv)까지. [PASS]
- **eq:dHeff(유효장벽)**: 합-1 → χ_d 방향선택 eq:chid → 깊은 꼬리 −Ω(1−2ξ)→+Ω 흡수 → 박스. [PASS]
- **eq:Lqfull(L_q 평가)**: eq:kuniv+Eyring prefactor 를 eq:Lq 에 대입 → eq:Lqmid2 → T_* 묶기 → 박스 + 코드 ln_Lq 4항 1:1 대응. [PASS]
- **eq:LV·eq:peakshape·eq:lowpass·eq:reversal·eq:sum**: 적분인자 eq:intfactor → 일반해 eq:memory → 이산 저역통과 eq:lowpass → peak_shape eq:peakshape → 분기 eq:branch → 충전 역전 eq:reversal → 합산 eq:sum. 인과 합성곱·격자역전 모두 동기 서술 충분. [PASS]

### G-derive LOW 막힘 (5건, 심각도 LOW — 따라감은 됨)

- **[LOW] L741(eq:weff 유도 — w^eff 중심기울기 매칭)**: "sF dV_eq/dξ|_{1/2}=4RT−2Ω 와 4Fw^eff 를 같다고 풀면(s 부호 양변 공통 상쇄)"가 한 줄로 압축. dV_eq/dξ|_{1/2} 가 어떻게 (4RT−2Ω)/(sF) 가 되는지(eq:Veq 를 ξ=1/2 에서 미분)와, ideal logistic 중심기울기가 왜 4Fw^eff 인지(eq:eqpeak 의 1/(4w) 와의 연결)는 독자가 직접 채워야 함. eq:dUhys 같은 4-step 전개가 아닌 유일한 결과식. **막힘이라기보다 11식 중 유일하게 (a)~(c) 단계가 inline 1줄로 눌린 곳** — 학부생이 "4Fw^eff 의 4 가 어디서?"에서 잠깐 멈출 수 있음. (단 w^eff 는 use_w_eff 기본 False 옵션이라 재현 필수경로는 아님.)

- **[LOW] L799–801(z_cut=4.357 의 출처)**: "logistic 미분 종의 5% 폭이 중심에서 ±z_cut·RT/F 규모라 A=z_cut·n_jRT". 4.357 이라는 정밀값이 미분 5% 컷에 대응함은 [검증완료: 정확히 0.05] 사실이나, 본문은 z_cut 을 풀어 유도하지 않고 "선택값"으로 선언. 독자가 4.357 을 스스로 도출하려면 e^{−z}/(1+e^{−z})²=0.05·(1/4) 를 풀어야 하는데 그 방정식이 본문에 없음. tab:inputs·tab:nodemap 에 기본값으로 박혀 있어 재현엔 지장 없음(G-usable PASS). G-derive 로만 LOW.

- **[LOW] L743 "면적=Q_j(∫₀¹dξ=1, eq:belliden 의 종이 dξ_eq 의 치환적분)"**: 치환적분 논리가 압축. ∫(dξ/dV)dV=∫dξ=1 인 이유(적분변수 치환)는 한 박자 생각 필요하나 표준. LOW.

- **[LOW] L605 "k_j≡r⁺+r⁻"의 등장**: dξ/dt=r⁺(1−ξ)−r⁻ξ=k_j(ξ_eq−ξ) 로 적을 때 k_j=r⁺+r⁻ 임이 괄호 안 정의로만 주어지고, r⁺(1−ξ)−r⁻ξ 가 (r⁺+r⁻)(ξ_eq−ξ) 로 묶이는 대수(ξ_eq=r⁺/(r⁺+r⁻))는 생략. eq:logisticsolve 의 ξ_eq/(1−ξ_eq)=e^{A/RT} 와 정합하나 그 인수분해 한 줄이 없음. 따라감 LOW.

- **[LOW] ∂lnL_q/∂V 반복(과제 명시 점검 대상)**: ∂lnL_q/∂V=0(실현)·<0(동기)이 **L858–864 본문 + S6(L1161) + R4(L1185) + fig 캡션 논의** 로 4회 등장. 중복은 사실이나 각 출현이 다른 역할(본문 유도/부호검산 체크리스트/회귀 self-test 수치못박기)이라 **불필요 중복 아님 — 정당한 cross-reference**. 단 R4 와 S6 의 문장이 거의 동일 표현이라 한쪽이 약간 redundant 하게 읽힘. 심각도 LOW(설계상 의도된 반복).

**G-derive 막힘 총계: 치명(HIGH/CRIT) 0, LOW 5. 11식 모두 학부생이 앞 식만으로 따라갈 수 있음 — 유일한 약점은 eq:weff 의 1줄 압축.**

---

## 2. G-usable 닫힘 — 6단계 박스 + 3표만으로 v11 곡선 재현 가능?

### 닫힘 = YES (재현 경로 완결)

6단계 박스(L1105–1113)를 tab:staging(L1037)·tab:inputs(L1065)·tab:nodemap(L1121)과 함께 따라가며 각 단계 입력의 출처를 추적:

- **(1) transitions**: tab:staging 4건 = U/ΔH_rxn/ΔS_rxn/Q/Ω/ΔH_a/dVdq_qa 전부 수치 제공. + L1056 "w 폴백 0.020/0.016/0.014/0.012, n=1, ΔS_a=0" 본문 명시. → 코드 GRAPHITE_STAGING_LIT 와 1:1 대조 [검증: 값·부호 전부 일치].
- **(2) σ_d·|I|·T·R_n → V_n(eq:vn)·V_work(eq:vwork)**: 패딩 0.15·n_work=max(2048,2|V_n|) 명시. R_n 기본 0(tab:inputs). [닫힘]
- **(3) U_j(eq:Uj)→center(eq:center)→w_j(eq:wbase)→ξ_eq(eq:xieq)**: center 분기조건(γ≠0 & Ω>0) eq:center 에 명시. ξ_eq 평가전위가 V_work 임을 L624 에서 못박음. [닫힘]
- **(4) A(eq:Acut)→χ_d,ΔH_a^eff(eq:chid,dHeff)→L_q(eq:Lqfull)→L_V(eq:LV)**: 전이당 상수(T_rep·n_rep) 명시. χ 기본 0.5. [닫힘]
- **(5) peak_shape 분기**: L_V<2Δ_grid(ν=min_lag_grid_steps=2) → 평형종 eq:eqpeak, else 꼬리 eq:peakshape + 충전 역전 eq:reversal. [닫힘]
- **(6) ΣQ_j 합산 + np.interp 역보간 eq:sum**. [닫힘]

tab:inputs 가 **전 인자 + 기본값**을 전이키/생성자/호출 3구획으로 전수 노출 → 코드 `__init__` 시그너처(x=0.5, Rn=0, Cbg=0, z_cut=4.357, A_cap_RT=4.0, w_eff_floor_frac=0.05, grid_pad=0.15, n_work_min=2048, min_lag_grid_steps=2.0, v_span_floor=1e-6, seed_T/I/Q_cell=298.15/0.1/1.0) 와 대조 → **누락 인자 0, 기본값 오류 0** [검증완료: 코드 L220–231 1:1].

### G-usable 잔존 결함

- **[LOW] grid_pad_lo/hi 비대칭 코멘트 vs 동일값**: 본문 L307·tab:inputs 는 p_lo=p_hi=0.15(대칭). 코드 L418 코멘트는 "저전위쪽 더 넓게"라 적었으나 실제 기본값은 둘 다 0.15(대칭). 문건은 0.15 동일로 정확히 적었으므로 **문건 결함 아님**(코드 코멘트가 부정확한 것). 재현 영향 0. 참고로만 기록.
- **[LOW] dVdq_qa 기본 0 → L_V=0 함정**: tab:inputs 에서 dVdq_qa 기본 0. 재현 시 사용자가 staging 표(0.30)를 안 넣고 빈 dict 로 가면 L_V=0(꼬리 소멸)되는데, 이 의존(eq:LV 가 0 곱)이 6단계 박스에는 명시 안 됨. tab:staging 에 0.30 이 있어 표대로 하면 정상이나, "기본 0 이면 꼬리 없음"경고가 본문 L865("dH_a 키 없으면 L_V=0")에는 있고 dVdq_qa=0 케이스는 암묵. 재현 LOW.

**G-usable 닫힘: YES. 6단계+3표로 v11 곡선 재현 코드 작성 가능, 닫히지 않은 식·빠진 인자 0. 잔존 LOW 2건(둘 다 재현 차단 아님).**

---

## 3. 배치 보존 — v7-11 결과박스·식별자·부호·표 변형/누락 0 (유도만 추가)

v7-11(890줄) ↔ v8-11(1210줄) 대조. 증분 +320줄 = 전부 유도 다리·신규 그림 4개(barrier·doublewell·flux·relaxode)·검산 항 추가. **삭제·변형 0 확인:**

- **결과 박스 11식 전수 일치**: eq:vn / eq:Uj / eq:dUhys / eq:Ubranch / eq:xieq / eq:eqpeak / eq:LV(+eq:Lq) / eq:dHeff / eq:peakshape / eq:sum — 박스 내용·label·부호 모두 동일. [PASS]
- **식별자**: func_U_j·func_dU_hys·func_U_branch·func_ksi_eq·func_L_q·func_chi_d·func_dH_a_eff·func_w(_eff)·_causal_lowpass·_resolve_lag_length·GRAPHITE_STAGING_LIT — 전부 보존, 대소문자·언더바 일치. [PASS]
- **부호**: σ_d 규약·ΔG=−sFU·U^dis>U^chg·격자역전·peak 양수 8/8 동일. [PASS]
- **3표 보존**: tab:staging 4행 수치(0.210/−11700/+29.0/0.10/6000/48000/0.30 …) v7-11 과 자릿수까지 동일. tab:inputs·tab:nodemap 동일. [PASS]
- **9 그림**: v7-11 5개(spine·staging·hysloop·logistic·reversal) 보존(캡션에 "v7-11 유래/그대로 채택" 명기) + 신규 4개. fig:spine·fig:staging 캡션은 v7-11 "신규"→v8-11 "v7-11 유래"로 출처표기만 바뀜(내용 동일). [PASS]

**변형/누락 0. 유도만 순증.** 단 1건 차이:
- **부호검산 verifybox: v7-11 R1–R4(4항) → v8-11 R1–R5(5항)**. R5(꼬리 극한 D-PEAK 회귀) 추가. 이는 누락이 아니라 **증분 보강**(헤더 주석 L9 "D-PEAK2 보강" 정합). S 체크리스트는 양쪽 S1–S8 동일. [증분 — 결함 아님]

---

## 4. 절 도입/마무리 다리 · 체리픽 이음새

절간 bridge 전수 확인 — **끊김 0**:
- 서론→N0: "다음 절은…U_j(T)…G→μ→평형조건 다리부터"(L318) → N2 가 정확히 그 다리로 시작. [PASS]
- N1→N2, N2→N3("μ 에 상호작용 몫…"L387), N3→N4, N4→N6("이 종이 평형 peak"L700), N6→N7("L_V 세우고"L760), N7→N8, N8→N9, N9→부호검산. 모든 마무리 문장이 다음 절 첫 물리량을 예고. [PASS]
- 체리픽 이음새: v8-10 헤더(L7–11)가 "v7-11 유래 5 그림 + 신규 4"·"이식금지 회귀(v8-02/03 D-PEAK·D-WEFF ¼·v8-07 s_F orphan)" 명시. fig:relaxode 캡션(L925–930)이 D-PEAK 회귀(L_V→0 은 식 극한 아니라 분기 스위치)를 본문 L946–963·R5 와 삼중 정합 — **체리픽 봉합선이 오히려 가장 촘촘히 검증된 구간**. orphan(앞 도입 없는 등장) 0. [PASS]

---

## 종합

| 항목 | 결과 |
|---|---|
| G-derive 막힘 | 치명 0, LOW 5 (eq:weff 1줄압축이 최약) |
| G-usable 닫힘 | YES (누락인자 0·기본값오류 0·닫히지않은식 0) |
| 배치 보존 | 변형/누락 0 (유도+그림+R5 순증만) |
| 절 다리·이음새 | 끊김 0, orphan 0 |
| 수치 검증 | R1·R2·N2·spinodal→artanh·RT/F·z_cut 전부 본문 일치 |

**가장 약한 1곳**: eq:weff(L741) 유도 — 11식 중 유일하게 (a)~(c) 중간단계가 inline 1줄("4Fw^eff 와 같다고 풀면")로 눌려, "분모 4"와 "ideal logistic 중심기울기" 연결을 독자가 직접 채워야 함. 다른 10식은 4-step 전개인데 이 식만 비대칭. 단 use_w_eff 기본 False 옵션식이라 재현 필수경로 밖 → 심각도 LOW. 치명 결함은 전 구간 0.
