# REVIEW_CH2_C2O1 — 독립 검수 (검수자 C2O1)

- 대상: v1.0.20 Chapter 2 청크 (_sections/ch2_*.tex) + appendix_phase_separation.tex
- 구본 대조: v1.0.19 동명 파일 (read-only)
- 검수 3축: ① 신본 자체 결함 · ② v1.0.19 대비 regression · ③ 신설 다리 물리·서지 정확성
- 렌즈: G-follow · G-usable · G-derive + refute 시도 + 최약점 지목
- 심각도: H=물리·수식 오류/오귀속 · M=유도 비약·정합 결손·regression · L=표기·문장·일관성
- 상태: 진행 중 (파일별 정독 완료 시 append)

---

## 발견 목록

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| C2O1-01 | ch2_preamble.tex:35 | L | ③ | `\newtheorem*{bgbox}{배경}` 가 Ch2 preamble 에 신설(B-003)됐으나 Ch2 본문 어느 절에서도 `\begin{bgbox}` 미사용(grep 전건 확인). Ch2 sec03:8-9 는 Ch1 §2 의 bgbox 를 후방 참조만 하고 자체 bgbox 를 만들지 않음. | grep bgbox → ch2_preamble:35 단독 매치. CHANGE_LOG B-003 = "양 preamble 신설(자족 블록·부록 이동 가능 설계)". | 결함 아님 판정 가능(공유 렌더 정합+장래 대비 의도적). 다만 현 시점 Ch2 미사용임을 인지 — 유지 무방. |
| C2O1-02 | ch2_sec00_intro.tex:41 | L | ① | 본문에 "이 통계열역학 사슬은 v5 계보가 규정한 골격이며" — 자기 버전 이력 서술. STYLE_RUBRIC A2[D1] "자기 개정 이력·버전 서술 금지(본문)". | RUBRIC A2. 구본 동일(regression 아님). G3 에서 유사 사례("(재작성)" 꼬리)를 P6 D1 검토 후보로만 유보. | D1 관점 후보(pre-existing). P6 스윕 미포함 — 사용자 판단 대기 항목으로 인지. 자산 주석 [C-1] 은 지적 대상 아님. |
| C2O1-03 | ch2_sec04_einstein.tex:61-63 | L | ① | ΔF_vib(T)≡RT ln(1−e^{−θ_E/T}) 를 "모드 자유에너지 편차"로 명명하나, 실제로는 단일 Einstein 모드의 (영점 제외) 절대 자유에너지이며 "편차(deviation from T_ref)"가 아님. 정작 편차량은 뒤의 ΔF_vib(T)−ΔF_vib(T_ref). ΔS_vib/ΔU_vib 의 Δ(=기준편차)와 ΔF_vib 의 Δ(=vib 몫)가 의미가 다름. | 66행 S_vib=−∂ΔF_vib/∂T 로 eq:Svib-einstein 정확 회복 확인 → 물리 무영향. 구본 동일(regression 아님). | G-follow 상 Δ 이중용법이 학부생 혼동 소지. 물리 중립·pre-existing — 표현 후보로만 인지. |
| C2O1-04 | ch2_sec01_partition.tex:85 · ch2_sec05_mixing.tex:165,167 | L | ① | 두-상 전이 압축표기 "$2\mathrm{L}\!\to\!2\cdot2\!\to\!1$" 에서 중간 "$2\cdot2$" 가 "2L→2"·"2→1" 두 전이의 경계인지 곱(2·2=4)인지 시각적으로 모호. | 문맥상 "2L→2" 및 "2→1" 두 두-상 전이 나열임이 확정(sec05:170 "어느 전이가 실제로 두-상 plateau"). 구본 동일(regression 아님). | "$2\mathrm{L}\to2$, $2\to1$" 또는 "및" 구분자 권고. pre-existing 가독 L. |
| C2O1-05 | ch2_sec08_synthesis.tex:126 (tab:qrev x̄=0.75 행) | L | ① | 표시된 ∂U_oc/∂T=+0.044 mV/K 로 재계산 시 ΔS=F·0.044e−3=+4.245→+4.2, Q̇/I=−298.15·0.044e−3=−13.12→−13.1 이나, 표는 ΔS=+4.3·Q̇/I=−13.2. x̄=0.50 도 Q̇/I 표시 +26.6 vs 재계산 +26.5. | 세 열이 full-precision ∂U/∂T≈+0.0443 에서 동시 화해(96485·0.0443e−3=+4.27→+4.3, −298.15·0.0443e−3=−13.2). 중간열만 3자리로 반올림된 표시-정밀도 문제. 구본 동일(regression 아님)·물리 오류 아님. | G-usable(표시값 재현) 상 학부생이 표기값으로 재계산 시 ~0.1 mV 어긋남. ∂U/∂T 4자리 표기 또는 "표시 반올림" 각주 권고. |

---

## 파일별 커버리지 증빙

### ch2_preamble.tex (전문 정독 완료, 52행)
- 구본 대비: 버전 스탬프 v1.0.19→v1.0.20(주석 2·3행, pdftitle 27행, lhead 29행)·`\newtheorem*{bgbox}{배경}`(35행) 신설. 물리 무관.
- 매크로(\kB·\vib·\config·\eff 등) 정합, `\theequation`·`\thesection` = 2.N prefix 정상.
- refute: bgbox 미사용(C2O1-01) 외 결함 없음. 최약점 = bgbox 미사용(정합상 무해).

### ch2_sec00_intro.tex (전문 정독 완료, 68행)
- 구본 대비 무변경(diff 공백).
- 물리 검산: 사슬 박스(44-52행) Z→⟨n⟩→S=−R∑p ln p→∂U/∂T=ΔS/F→Q̇_rev 정합. Q̇_rev=−IT∂U_oc/∂T=−(IT/F)ΔS(x)(26행) 부호·환산 정합.
- 교차참조: Ch1 §3(8행 평형 중심 전위)·§15(61행 LCO 전자 엔트로피) — 후술 Ch1 대조에서 확인.
- refute: 물리·수식 결함 없음. 최약점 = "v5 계보" 자기버전 서술(C2O1-02).

### ch2_sec01_partition.tex (전문 정독 완료, 144행)
- 구본 대비 무변경(diff 공백).
- 물리 재검산(전 식 손검산): eq:Z1 Ξ₁=1+e^{−β(ε0−μ)}·eq:occ ⟨n⟩=1/(1+e^{β(ε0−μ)})(분자분모 나눗셈 정합)·eq:logistic θ_eq/ξ_eq 지수부호(고V→θ→0→ξ→1)·eq:Vxi Nernst·eq:BW·eq:Veq_BW(∂g/∂θ=RT ln[θ/(1−θ)]+Ω(1−2θ) 정합)·eq:slope_BW(θ=½ 에서 (2Ω−4RT)/F, 임계 Ω=2RT) 전건 정합.
- s_int=k_B ∂(T ln q)/∂T 선도항 +k_B ln q(45-46행) 정합.
- 교차참조: Ch1 §1(σ_d 각주)·§2 Part0(Ξ₁·ε̃·섞임·자리당 S)·§4(spinodal)·§5(logistic 종) — Ch1 대조 예정.
- refute: 부호 여집합 오류 각주(58-61행)·이중지위 keybox 논리 일관. 결함 없음. 최약점 = keybox 두-상 표기 "2L→2·2→1"(85행) 압축 표기(가독 L급, 정의 명확하여 미로그).

### ch2_sec02_config.tex (전문 정독 완료, 188행)
- 구본 대비: 9행 U10 참조 `(\S\ref{ssec:litverif})` 부여만. ssec:litverif = 132행 "문헌 검증" 소절 실재 → 전방참조 타겟 정확. CITATION_BASELINE U10 처리와 정합.
- 물리 재검산: eq:Sconfig·eq:dSconfig(∂S/∂θ=−R ln[θ/(1−θ)], 상수 ±1 상쇄)·eq:dVdT_config(둘째항 (R/F)ln[ξ/(1−ξ)] = (1/F)∂S_config/∂θ|_{θ=1−ξ}) 정합. 부호 3분기(56-64행) ξ→1:+∞·ξ→0:−∞·ξ=½:0 정합.
- ΔH⁰_j=−FU_j+FT ∂U_j/∂T 검산: U_j=(−ΔH+TΔS)/F 대입 시 =ΔH_rxn,j 로 항등(176-177행) 정합.
- MCMB 단위 각주(138-140행) [미검증]: +29 J/mol·K ⇒ +0.30 mV/K(29/96485=0.30) 산술 정합, +3~4 mV/K 자릿수 차 정직 노출 — 판정 맥락상 정직 공백(결함 아님).
- 교차참조: Ch1 §14(삼분해·슬롯, 128행).
- refute: tab:ds 4→3 행 +29@x=0.08(창 끝, config 겹침) 등치의 약함은 본문이 명시 hedge(143-145·167-169행) — 은닉 결함 아님. 최약점 = 그 경계 등치(disclosed).

### ch2_sec03_vibel.tex (전문 정독 완료, 101행)
- 구본 대비: 8-9행 Ch1 §2 배경박스 후방참조 1문장 신설 · 17-21행 B-005 중간식 인라인 신설. 표시식 eq:Svib_mode(22-25행)·라벨·최종식 불변 확인.
- **B-005 손 재유도(전 단계 검산 — 핵심 과제)**: f_k=k_B T ln(1−e^{−βℏω}), S=−∂f_k/∂T.
  (1) 곱규칙: ∂_T(k_B T)·ln(·)=k_B ln(1−e^{−βℏω}) → S 부호반전 후 −k_B ln(1−e^{−βℏω}) [로그 항].
  (2) β=1/k_BT 연쇄율: k_B T·∂_T ln(1−e^{−βℏω}) = −(ℏω/T)·[e^{−βℏω}/(1−e^{−βℏω})] = −(ℏω/T)n_k → S 후 +(ℏω/T)n_k = +k_B βℏω n_k [점유 항], ∵ e^{−βℏω}/(1−e^{−βℏω})=1/(e^{βℏω}−1)=n_k 및 ℏω/T=k_B βℏω.
  ⇒ 중간식 S=−k_B ln(1−e^{−βℏω})+k_B βℏω n_k **정확**.
  (3) 항등식1 1−e^{−βℏω}=1/(1+n): n=1/(e^{βℏω}−1)⇒e^{βℏω}=(1+n)/n⇒e^{−βℏω}=n/(1+n)⇒1−e^{−βℏω}=1/(1+n) **정확**.
  (4) 항등식2 βℏω=ln[(1+n)/n]: e^{βℏω}=(1+n)/n 로그 **정확**.
  (5) 대입: −k_B ln[1/(1+n)]+k_B n ln[(1+n)/n]=k_B ln(1+n)+k_B n ln(1+n)−k_B n ln n=k_B[(1+n)ln(1+n)−n ln n]=eq:Svib_mode **정확**.
  ⇒ 전 5단계 부호·대수 정합. B-005 결함 없음(강한 양성 검증).
- electronic: eq:Se_start·Sommerfeld ∫(−∂f/∂E)(E−E_F)²dE=(π²/3)(k_BT)²·C_e=(π²/3)k_B²T g(E_F)·S_e=∫C_e/T'dT'=(π²/3)k_B²T g(E_F)(=γT=C_e) 정합. 차원검산 k_B²T g→k_B(66행) 정합.
- 교차참조: Ch1 §2(배경박스, 분업 대조 예정)·§8·§9(활성화 S)·§13·§15(eq:Se 별개). eq:Se-ch2(61행) vs Ch1 eq:Se 라벨 회피 = appA:67 각주로 명시.
- refute: msmr_partI(91행) "활성화 S 는 비가역 지배·가역 발열 미포함" 인용은 다소 느슨하나 pre-existing·원장 V1 승인. 최약점 = 그 인용 적합성(pre-existing, 미로그).

### ch2_sec04_einstein.tex (전문 정독 완료, 115행)
- 구본 대비 무변경(diff 공백).
- 물리·수치 재검산: 단일모드 항등식 (1+n)ln(1+n)−n ln n=−ln(1−e^{−u})+u/(e^u−1) 손검산 정합(1+n=e^u/(e^u−1) 경유). eq:Svib-einstein·고온극한 R[1+ln(T/θ_E)](−ln u+u/2 와 1−u/2 상쇄)·저온극한 0 정합. round-trip: ΔF_vib=RT ln(1−e^{−θ_E/T}), S_vib=−∂ΔF_vib/∂T 로 eq:Svib-einstein 회복·eq:dUvib 및 ∂ΔU_vib/∂T=ΔS_vib/F 정합. Bernardi 관계 ∂U/∂T=ΔS/F(∂ΔG/∂T=−ΔS 로 ΔC_p 무관) 정합.
- **수치 4점 손 재계산**(θ_E=700K, T_ref=298.15): ΔS_vib(T)/F=[S_vib(T)−S_vib(T_ref)]/F, R/F=86.17 µV/K. T=278.15/298.15/318.15/348.15 → −3.742/0/+3.694/+9.132 µV/K, 본문 −3.74/0/+3.70/+9.14 와 정합(반올림).
- 교차참조: Ch1 §4 spinodal 근 u_j=√(1−2RT/Ω_j) 동명 별개 각주(20-22행). appA 함정표 연동.
- refute: 물리·수치 결함 없음. 최약점 = ΔF_vib 의 "편차" 명명(C2O1-03, 물리 중립).

### ch2_sec05_mixing.tex (전문 정독 완료, 240행)
- 구본 대비: 168-169행 U9 = footnote 내 두-상 지목 근거 문장에 `\cite{dahn1991,ohzuku1993}` 부여만.
- **U9 축③ 정합 확인**: 주장="실측 plateau·staging 문헌의 상평형". dahn1991="Phase diagram of Li_xC6"(흑연 상도표)·ohzuku1993="Formation of Li-Graphite Intercalation Compounds"(staging 형성) — 둘 다 주장 직접 뒷받침. CITATION_BASELINE U9 처리(C-017·C-018 신규등재)와 정합.
- 물리 재검산: eq:implicit_diff(음함수미분)·eq:gj(∂ξ/∂U=ξ(1−ξ)/w)·eq:dxidT(두 조각, z_j=(U−U_j)/w_j=ln[ξ/(1−ξ)])·eq:dwdT-nT(곱미분)·eq:weighted(g_j 상쇄→중심값 가중)·eq:single_config(n_jR/F, sec02 일반형)·eq:hys_rev(분기 평균) 전건 정합. 2RT≈4957 J/mol@298.15 정합(2×8.314×298.15=4957.2).
- 교차확인: fig:blend 캡션 −16→−5→0→+29(탈리튬화 상승)이 tab:ds(+29→0→−5→−16, x 오름차순)와 방향 일관.
- 수치검증 박스(175점·0.18/0.21·[−0.21,+0.14]·0.35 mV/K)는 numverif2026(내부자료, 검증대상 아님)·전제 hedge(자기일관성이지 실측검증 아님) 명시.
- g 4종 충돌 주의(39-41행)·narrowing 식 재도입 금지(187행)·가역/비가역 분리 warnbox 논리 일관.
- 교차참조: Ch1 §2(g_j(ξ), 39행)·§7(broadening, 177행)·§4(분기 중심식 γ_j h_{η,j}=1, 196행).
- refute: 수치검증이 내부자료 의존이나 disclosed. 최약점 = 두-상 압축표기(C2O1-04).

### ch2_sec06_limits.tex (전문 정독 완료, 52행)
- 구본 대비 무변경(diff 공백).
- tab:limits 6코너 전건 정합: ξ→1 config→+∞·ξ→0 config→−∞·ξ=½ =ΔS/F(config=0)·Ω→2RT 상분리·단일봉우리 eq:weighted 환원·고온 k_BT~E_F 에서 Sommerfeld 정량 부적용(정성만) 정직 노출.
- keybox "ΔS_rxn,j 전이당 상수" 근사 판정(중심+분포로 측정급·예외 LCO MIT)이 파생 B/§2.3 elec 예외와 정합.
- refute: 결함 없음. 최약점 = 고온 코너(k_BT~E_F)가 전지 온도역에서 도달불가한 학술적 극한(형식적 유효성 점검일 뿐, 결함 아님).

### ch2_sec07_revheat.tex (전문 정독 완료, 58행)
- 구본 대비 무변경(diff 공백).
- 물리 재검산: eq:qrev Bernardi 분해 Q̇=I(U_oc−V)+(−IT∂U_oc/∂T), Q̇_irr≥0(방전 V<U_oc)·Q̇_rev=−IT∂U/∂T=−(IT/F)ΔS 정합. srcbox ΔG=−FU_oc·ΔS=−∂ΔG/∂T=+F∂U_oc/∂T 정합. 부호해석(방전 I>0: ΔS>0→흡열/ΔS<0→발열)·SOC 흡발열 교대·2→1 발열 전건 정합.
- 라벨층위 warnbox(방전=Bernardi 리튬화 vs Ch1 탈리튬화 σ_d=+1, 같은 단어 반대 방향, 부호는 I로 읽음) — 정확·중요.
- refute: 결함 없음. 최약점 = 라벨 충돌(본문이 스스로 "부호 최대 어긋남 자리"로 명시·정확 처리).

### ch2_sec08_synthesis.tex (전문 정독 완료, 144행)
- 구본 대비 무변경(diff 공백).
- **가중평균 산술 직접 재계산(과제)**: [중심+config] = {−0.157,−0.220,−0.206,−0.203}(tab:worked 각 행 합 정합). 비중가중 0.753(−0.203)+0.193(−0.206)+0.051(−0.220)+0.003(−0.157)=−0.20431≈**−0.204** 정합. 단순식 0.753(−0.166)+0.193(−0.052)+0.051(0)+0.003(+0.301)=−0.1341≈**−0.134**·config 몫 =−0.0702≈**−0.070** 정합.
- tab:worked 전 셀 손검산: w=RT/F=25.69 mV·g_j=ξ(1−ξ)/w(9.30/4.77/2.61/0.19)·ΔS⁰/F(−0.166/−0.052/0/+0.301=ΔS⁰/96485)·config=(R/F)ln[ξ/(1−ξ)](R/F=0.08617 mV/K) 전건 정합. 비중 합=1.000.
- (e): ΔS=F·(−0.204e−3)=−19.68≈−19.7·Q̇/I=−298.15·(−0.204e−3)=+60.82≈+60.8 mV 정합. tab:qrev 5행 ΔS=F∂U/∂T·Q̇=−T∂U/∂T 내부정합(U_oc 43.5→195.2 mV 탈리튬화 상승 정합).
- refute: tab:qrev 중간열 표시반올림(C2O1-05)이 유일. 최약점 = 그 표시-정밀도.

### ch2_sec09_method.tex (전문 정독 완료, 43행)
- 구본 대비 무변경(diff 공백).
- procedurebox 5단계 정합: 저율 다온도 dQ/dV·분극분리(Ch1 §1 V_n=V_app−σ_d|I|R_n, 16행)·동시피팅=MSMR(Multi-Species, Multi-Reaction, Ch1 §17, 20행)·ΔS⁰_j=F dU_j/dT+Allart 대조·봉우리내부 자동. ΔS⁰_j=F dU_j/dT 는 ∂U_j/∂T=ΔS_rxn,j/F 와 정합.
- 정직한 한계 5항(시뮬 자기일관성≠실측·히스 경로의존 범위밖·Ω(T) 미확보·elec 흑연소수·전셀 범위밖) 헌법 ② 정직 노출.
- 교차참조: Ch1 §1(V_n)·§17(MSMR). MSMR 풀네임 원장 C4 일치.
- refute: 결함 없음. 최약점 = MSMR 대응 주장(msmr_partI/II 인용, 적정).

### ch2_sec10_closing.tex (전문 정독 완료, 25행)
- 구본 대비 무변경(diff 공백).
- 4파생 역할 요약·6코너·"상수+분포" 자기일관·계산예제(<0.001 µV/K)·5점 부호교대·가역발열 수미상관 — 본문과 전건 정합(신규 내용 없음).
- 교차참조: Ch1 logistic(8행)·§7(broadening, 13행).
- refute: 요약절, 본문과 불일치 없음. 최약점 = 없음(순 요약).

### ch2_appA_traps.tex (전문 정독 완료, 74행)
- 구본 대비 무변경(diff 공백).
- 함정표 12항 전부 본문 근거절과 정합: s vs σ_d(ssec:logistic)·θ/ξ·θ/θ_E·x̄/x·g 4종·F_vib/F·u_j/x·u_j vs Ch1 §4 spinodal 근(별개)·방전(I>0) 라벨·ΔS/ΔS_a·ΔS_vib(T)/∂S_vib/∂x·S_e 라벨(eq:Se-ch2 vs Ch1 §15 eq:Se).
- 42행 "F_vib=몰당 Helmholtz(ΔF_vib=RT ln(1−e^{−θ_E/T}))" — C2O1-03 과 연동(ΔF_vib=F_vib 로 취급, sec04 "편차" 명명이 loose 임을 재확인).
- 교차참조: Ch1 §4 spinodal u_j·§15 eq:Se(동명 별개 명시) — Ch1 대조 예정.
- refute: 결함 없음. 최약점 = F_vib/ΔF_vib 명명 loose(C2O1-03 로 로그됨).

### ch2_appB_codemap.tex (전문 정독 완료, 69행)
- 구본 대비 무변경(diff 공백).
- **회귀 기준값 sec08 문자 일치 확인(과제)**: entropy_coefficient_x(0.25)=−0.204(단순식 −0.134·config −0.070)·U_oc=74.4 mV·round-trip −0.204(<0.001 µV/K)·ΔS=−19.7·Q̇/I=+60.8 mV·5점(−0.307/−0.204/−0.089/+0.044/+0.218, +91.5/+60.8/+26.6/−13.2/−64.9)·175점 — 전건 sec08/tab:qrev 와 문자 일치.
- doc-leads 프레이밍(문건 권위·코드 이후 개정)·하위호환 bit-exact(θ_E 미지정)·입력규약(s=+1·두-상 자유폭) 정합. 함수명 부록 B 전용(rubric A5 준수).
- refute: 결함 없음. 최약점 = tab:qrev 값 승계라 C2O1-05 표시반올림이 appB:48-49 에도 전파(동일 원천, 별건 아님).

### ch2_bib.tex (전문 정독 완료, 27행)
- 구본 대비: 헤더 14→16 bibitem 정정 · dahn1991·ohzuku1993 신규(C-017/018) · msmr_partI 023502(C-005) · msmr_partII 제목전문+103505(C-006) · hysteresis2018 179–184(C-007). 전부 CHANGE_LOG·REFERENCE_LEDGER 정합.
- 카운트 실측: 외부 15 + numverif2026 내부 1 = 16 정확. 신규 dahn1991·ohzuku1993 모두 sec05:169 U9 에서 실인용(orphan 없음). 전 15 외부키 본문 인용처 존재 확인.
- dahn1991(PRB 44, 9170, 1991·DOI 10.1103/PhysRevB.44.9170)·ohzuku1993(JES 140, 2490, 1993·DOI 10.1149/1.2220849·제목 전문) 원장 문자 일치. ch1_bib 3자 정합은 Ch1 대조에서 확인 예정.
- refute: 서지 오류 없음. 최약점 = ch1_bib 문자일치 미확인(다음 단계).

### appendix_phase_separation.tex (전문 정독 완료, 497행)
- 구본 대비: (1) 3·39행 버전 스탬프 v1.0.19→v1.0.20 각주 갱신 · (2) P6 표기 정규 용액→정규용액·격자 기체→격자기체 8건(44·69·104·163·210·245·352·380행) · (3) 494행 [A5] Ch.~17--18→**Ch.~18--19**(C-019). 내용 미개정.
- **P6 표기 주변 문장 훼손 점검**: 8건 전부 단어 내부 공백 제거만이며 주술·수식·인접어 훼손 없음(문장 완결성 유지).
- **C-019 확인**: [A5](494행) "Ch.~18--19 (Cahn--Hilliard 선형화·핵생성 이론)" — CHANGE_LOG C-019(Ch.18 spinodal/CH·Ch.19 nucleation)·원장 [A5] 정합. 본문 인용 [A5] 2곳(403·439행)은 장번호 무표기 → 무변경 정합. [A1]-[A4] 원장 문자 정합([A1] sentence-case 서지재량 허용 명시).
- **물리 전건 손검산**: app-Smix(Stirling)·app-Umix(Δw 상쇄)·app-fxi·app-chord·app-lever·공통접선 app-ct·화학퍼텐셜 절편 μ_A=t(0)/μ_B=t(1)·binodal(Ω=3RT: ξ_b=0.0707 검산·f/RT=−0.0583)·spinodal ξ_s=½(1±u), u=√(1−2RT/Ω)(§4.1 정합·0.2113/0.7887·f/RT=−0.0157)·요동 ½f''δ²·Maxwell app-maxwell·CNT r*·ΔG*=16πγ³/3Δg_v²·Cahn-Hilliard R(k)=−Mk²[f''+2κk²]·k_m=k_c/√2·차원([κ]=J/m,[M]=m⁵J⁻¹s⁻¹) 전건 정합.
- 그림 2종(fig:app-tangent·fig:app-phasediag) 좌표값이 식 평가와 일치(binodal/spinodal 곡선·네 교점).
- 기호 배향 각주(ξ_appendix=θ_body, 여집합) 명시 — 본문과 정합.
- 본문 절참조 §2(Part0)·§4.1(spinodal)·§4.2(히스 gap)·§7(broadening) — Ch1 대조 예정.
- refute: 결함 없음. 최약점 = Cahn-Hilliard 절에서 f 를 몰당→부피밀도로 재해석(442행 disclosed)하는 단위-맥락 전환(G-follow 속도방지턱, 명시되어 결함 아님).

---

## Ch1 교차 정합 축 (Ch1 신본 대조 — 전건 통과)

절 번호 매핑 확인(ch1 신본 \section 순서): §1 n0n1 · §2 part0(2a/2b) · §3 center · §4 hys(4.1 spinodal=sec:hys-spinodal · 4.2 gap=sec:hys-gap · 4.3 branch) · §5 width · §6 eqpeak · §7 broadening(7.2 세 출처) · §8 lag · §9 tail · §10 sum · §11~§17 LCO · §18 inputs. → Ch2 리터럴 참조(§1·§2·§3·§4·§5·§7·§8·§9·§13·§14·§15·§17) 전건 절번호·내용 대응.

| 대조 항목 | Ch2 측 | Ch1 신본 측 | 판정 |
|---|---|---|---|
| bgbox 분업(sec03 서두) | sec03:8-9 "Chapter 1 §2 배경박스(페르미온·보손과 양자 통계)가 정리" | ch1_sec02a:171-188 `\begin{bgbox}` 제목 "페르미온·보손과 양자 통계", 교환대칭·스핀-통계·FD/BE 수록, 186행에 포논 BE/전자 FD forward 다리 | ✅분업 성립(제목 문자 일치·내용이 미룬 배경 실제 포함·양방향 다리) |
| Ξ₁ 표기 | sec01 eq:Z1 Ξ₁=1+e^{−β(ε₀−μ)}, sec01:39 "Ch1 §2와 통일 표기" | ch1_sec02a:130/152 Ξ₁⁰=1+e^{−β(ε₀−μ)}·199/216-217 "(eq:Z1)도 같은 기호 Ξ₁로 통일" | ✅통일(내부자유도 흡수 시 ε₀→ε̃로 Ch1 Ξ₁=Ch2 Ξ₁) |
| q(T)→ε̃ 정의 | sec01:42-43 ε̃=ε₀−k_BT ln q(T) | ch1_sec02a:232 ε̃(T)≡ε₀−k_BT ln q(T) | ✅문자 일치(자리당 S=k_B ∂(T ln q)/∂T 도 sec01:45 ↔ ch1:277-280 일치) |
| eq:Se vs eq:Se-ch2 별개 | sec03:60 `\label{eq:Se-ch2}` S_e=(π²/3)k_B²T g(E_F) | ch1_sec15:82 `\label{eq:Se}` S_e=(π²/3)k_B²T g(E_F,x) | ✅동명 별개 라벨(공식 동일·별도 컴파일)·appA:67 각주 정확·Ch1 §15 sec:lco-Se 유도(Sommerfeld 적분·C_e 적분)가 sec03 상술처와 일치 |
| u_j 동명 별개(spinodal 근) | sec04:21·appA:51 "Ch1 §4 spinodal 근 u_j=√(1−2RT/Ω_j)" | ch1_sec04:35/104 u_j≡√(1−2RT/Ω_j) (§4.1 sec:hys-spinodal) | ✅문자 일치·appendix §4.1 참조도 정합 |
| dahn1991 3자 정합 | ch2_bib:9 | ch1_bib:5 (동일: PRB 44, 9170, 1991·DOI 10.1103/PhysRevB.44.9170) | ✅ch1_bib·ch2_bib·원장 문자 완전 일치(C-017) |
| ohzuku1993 3자 정합 | ch2_bib:10 | ch1_bib:6 (동일: JES 140, 2490, 1993·DOI 10.1149/1.2220849·제목 전문) | ✅ch1_bib·ch2_bib·원장 문자 완전 일치(C-018) |
| 삼분해·슬롯(§14) | sec02:128 "Ch1 §14 반응 엔트로피 삼분해·슬롯 규칙" | ch1_sec14 §14 "반응 엔트로피 삼분해와 슬롯 규칙" | ✅제목·내용 대응 |
| broadening 세 출처(§7) | sec05:177 "Ch1 §7 broadening 세 출처" | ch1_sec07 §7·§7.2 sec:broadening-sources "broadening 의 세 출처" | ✅대응 |
| appendix 본문 절참조 | §2·§4.1·§4.2·§7 | §2 part0·§4.1 spinodal·§4.2 gap·§7 broadening | ✅전건 대응 |

## 담당 소관 항목 판정 요약 (C-017·C-018·B-005·C-019·U9·U10)
- **B-005**(sec03 중간식 인라인): 손 재유도 전 5단계 정합 — **정확**(발견 없음). 표시식·라벨·최종식 불변 확인.
- **C-017/C-018**(ch2_bib dahn1991·ohzuku1993): ch1_bib·원장 3자 문자 일치 — **정확**. sec05 U9 실인용.
- **C-019**(appendix [A5] Ch.18-19): 정정 반영·본문 [A5] 2곳 무변경 — **정확**.
- **U9**(sec05:168-169 dahn1991·ohzuku1993): 주장-문헌 정합(상도표·staging) — **정확**.
- **U10**(sec02:9 §ref:litverif): 전방참조 타겟(ssec:litverif 실재) — **정확**.

---

## REVIEW COMPLETE — 발견 총 5건 (H 0 / M 0 / L 5)

- 전문 정독 완료: 담당 청크 15개 파일(ch2_preamble·sec00~sec10·appA·appB·bib) + appendix_phase_separation.tex(497행). 커버리지 헤더로 파일별 증빙.
- 축① 신본 자체 결함: 물리·수식 오류 **0건**. B-005 중간식 손 재유도, sec08 가중평균(−0.204/−0.134/−0.070), sec04 Einstein 4온도점(−3.74/0/+3.70/+9.14), appendix binodal/spinodal/CNT/Cahn-Hilliard, ΔH⁰=−FU+FT∂U/∂T(2→1 −13.0 kJ/mol) 전건 재검산 정합. 발견 5건은 모두 표기·가독·표시정밀도 L급.
- 축② regression: **0건**. 구본(v1.0.19) 대비 의미 약화·자산 유실·수치 변화 없음. 변경은 CHANGE_LOG 의도 항목(U10 §2:9·B-005/배경참조 §3·U9 §5·bib C-005/006/007/017/018·preamble bgbox·appendix P6/C-019)에 정확히 1:1 대응.
- 축③ 신설 다리: **전건 정확**. bgbox 분업·U9 인용 정합·U10 전방참조·B-005 재유도·C-019 정정·dahn1991/ohzuku1993 3자 문자 일치·eq:Se-ch2 vs eq:Se 별개·u_j 동명 별개 각주 — 모두 검증 통과.
- 확정 판정 맥락 존중: 두-상/2상역 분업(P6)·Gn 선언·MCMB [미검증] 각주·appendix 관용·% 자산 주석 — 지적 대상에서 제외(반박 근거 없음).

발견 5건(전부 L, pre-existing·비-regression):
1. C2O1-01 ch2_preamble:35 — bgbox 정의 Ch2 미사용(B-003 정합상 무해).
2. C2O1-02 sec00:41 — "v5 계보" 자기버전 서술(D1 후보).
3. C2O1-03 sec04:61-63 — ΔF_vib "편차" 명명 loose(물리 중립).
4. C2O1-04 sec01:85·sec05:165-167 — 두-상 압축표기 "2L→2·2→1" 가독.
5. C2O1-05 sec08 tab:qrev x̄=0.75 — 중간열 표시반올림(재계산 시 ~0.1 mV 어긋남, appB 회귀표에 전파).

## 가장 약한 1곳

**sec08/appB 회귀 기준값의 헤드라인 "완전식 −0.204 mV/K"(지배 2→1 두-상 전이의 config 몫)가, 문건 스스로 [미검증]으로 선언한 열적 폭 서식 $w_j=n_jRT/F$ 에 조건부라는 점.** 파생 C(§2.5 ssec:weff)·파생 A srcbox·종합식 박스(§2.8)가 반복해 밝히듯, 두-상 전이 폭은 평형이 예측하는 양이 아니라 현상학적 자유 피팅이며, 실측 $w_j$ 가 $T$-동결에 가까우면 완전식↔단순식 우열이 ~0.3 mV/K 급으로 뒤집혀 config 몫(−0.070)의 부호적 지위가 흔들린다. 곧 doc-leads 코드 계약의 1급 회귀값 −0.204 는 "완전식"으로 제시되면서도 그 성립 근거가 자기-선언 미검증 가정 위에 있고, 보수적 바닥은 단순식 −0.134 다. 문건이 이 조건부를 warnbox 로 투명하게 노출하므로 **은닉 결함이 아니라 disclosed 조건부**이나, 검수 3축 중 가장 반박 가능성이 큰 지점이며 다온도 실데이터 round-trip 전까지 −0.204 를 확정 회귀값으로 굳히지 말 것을 지목한다. (개별 발견 중 가장 실무 영향이 큰 것은 C2O1-05 표시반올림 — 회귀표 재현 계약에 직접 닿음.)
