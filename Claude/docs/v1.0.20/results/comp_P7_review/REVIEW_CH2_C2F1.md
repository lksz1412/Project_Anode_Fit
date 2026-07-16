# REVIEW_CH2_C2F1 — v1.0.20 Ch2 + appendix 독립 검수 (검수자 C2F1)

> 검수 일시: 2026-07-16. 대상: `_sections/ch2_*.tex` 16종 + `appendix_phase_separation.tex`.
> 대조 구본: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.19/` 동명 파일 (read-only).
> 기준 문건: V1020_STYLE_RUBRIC.md · V1020_REFERENCE_LEDGER.md · V1020_CHANGE_LOG.md · V1020_P1_CITATION_BASELINE.md (4종 전문 정독 완료).
> 검수 3축: ① 신본 자체 결함 / ② v1.0.19 대비 regression / ③ 신설 다리(C-017·C-018·B-005·C-019·U9·U10) 물리·서지 정확성 + 교차 정합(Ch1 §N 리터럴 참조 전건).
> 다른 REVIEW_*.md 미열람 (독립성 준수).

## 발견 표 형식

| # | 위치(파일:행) | 심각도(H/M/L) | 축(①/②/③) | 발견 | 근거 | 제안 |

---
### ch2_sec00_intro.tex (전문 정독 완료, 68행)

- ② 구본 대비: `diff` 결과 **완전 동일** — regression 없음.
- ③ 교차 정합: L8 "Chapter 1 §3 의 평형 중심 전위" — Ch1 신본 절 번호 매핑(§3=ch1_sec03_center, TOC 1.3) 일치, 식 자체도 ch1_sec03:53 `\boxed{U_j(T)=(-\Delta H_{\rxn,j}+T\,\Delta S_{\rxn,j})/F}` 와 문자 일치. L61 "Chapter 1 §15" — §15=ch1_sec15_lcoelec(LCO 전자 엔트로피 항) 제목·내용 일치.
- ① refute 시도: L18–19 "SOC 에 따라 부호를 바꾸고($x$ 작을 때 양, 클 때 음)" — 이상 격자기체 $S_\config=-R\ln[\theta/(1-\theta)]$ 유래 $\partial U/\partial T$ 는 $\theta\to0$ 에서 $+$, $\theta\to1$ 에서 $-$ 로 정합(반박 실패 — 서술 옳음). L26 $\dot Q_\rev=-IT\,\partial U_\oc/\partial T$ 부호 규약은 §7 정독 시 재대조 예정.
- 발견: 없음 (컴파일 로그 미해결 참조 0 확인).

### ch2_sec01_partition.tex (전문 정독 완료, 144행)

- ② 구본 대비: `diff` 완전 동일 — regression 없음.
- ① 수식 재검산(전건 손 재유도): eq:Z1(Ξ₁=1+e^{−β(ε₀−μ)})·eq:occ(마지막 등식 분자분모 나눔 포함)·eq:logistic(θ/ξ 부호)·eq:Vxi(θ=1−ξ 대입 역산 일치)·eq:BW→eq:Veq_BW 미분(∂g/∂θ=RT ln[θ/(1−θ)]+Ω(1−2θ) → V_eq 부호 정확)·eq:slope_BW(θ=½ 에서 (2Ω−4RT)/F → 임계 Ω=2RT) — 전건 옳음. L74–76 단위 환산(βF=N_A/w ⟺ F/k_BT) 검산 일치. L47–49 고온 극한 S_vib→R[1+ln(T/θ_E)] 재유도 일치(1D 모드: −ln x + xn → 1+ln(T/θ_E), x=θ_E/T≪1).
- ③ 교차 정합(Ch1 리터럴 참조 4건): (i) L12–13·39–40 "Chapter 1 §2 Part 0" — §2=ch1_sec02a(TOC 1.2 "통계역학 기초 — 분배함수에서 Nernst 식까지 (Part 0)") 일치. Ξ₁ 표기: ch1_sec02a:215–217 이 "위 첨자 없는 Ξ₁=내부 자유도 포함 완전형, Chapter 2 의 eq:Z1 도 같은 기호로 통일" 선언 — Ch2 eq:Z1 은 형식상 bare 형이지만 ch2_sec01:43 "본 장 이하의 ε₀ 은 그 흡수를 마친 유효값(ε̃)으로 읽는다" 규약으로 Ch1 Ξ₁=1+q(T)e^{−β(ε₀−μ)}=1+e^{−β(ε̃−μ)} 와 동일 대상 — 정합 성립. ε̃ 정의 문자 일치: ch2_sec01:43 `\tilde\varepsilon=\varepsilon_0-\kB T\ln q(T)` ⟷ ch1_sec02a:232 `\tilde\varepsilon(T)\equiv\varepsilon_0-k_BT\ln q(T)` — 동일(매크로 \kB vs k_B 는 렌더 동일). s_int=k_B∂(T ln q)/∂T 도 ch1_sec02a:277–280 과 일치. (ii) L58–59 각주 "σ_d(Chapter 1 §1)" — ch1_sec01:11–14 σ_d 정의(방전 +1/충전 −1)·작용처 3곳 일치. (iii) L77–78 "Chapter 1 §5 의 logistic 평형 종 ξ_eq" — ch1_sec05 §제목·logistic 유도 일치. (iv) L133 "Chapter 1 §4 의 spinodal 조건과 같은 열역학" — ch1_sec04:35–38 Ω_j>2RT 문턱과 일치.
- refute 시도: L65–66 "N_Aε₀≡μ⁰" 처리 — ch1_sec02a:273–276 "μ⁰ 는 정확히 ε̃ 의 몰 환산 N_Aε̃" 과 대조하면 Ch2 는 ε₀ 를 유효값으로 읽는 규약(L43–44) 하에서 동일 진술 — 모순 아님(반박 실패).
- 발견: 없음.

### ch2_sec02_config.tex (전문 정독 완료, 188행)

- ② 구본 대비: diff 결과 변경 1건뿐 — L9 로드맵 문장에 `(\S\ref{ssec:litverif})` 병기. **U10 의도 변경과 1:1 대응**, 그 외 regression 없음.
- ③ U10 검증: 참조 라벨 `ssec:litverif` 는 L132 에 실재(§2.2 의 4번째 소절 = §2.2.4 — BASELINE 기재와 일치). 인용 실체(reynier2003·allart2018)는 L135–136 에 기존 존재 — U10 처리 기재("참조 부여, 인용 실체는 기존 인용")와 정확히 부합.
- ① 수식 재검산: eq:Sconfig ↔ eq:BW 둘째 항/(−T) 일치 검산 옳음. eq:dSconfig(±1 상쇄) 옳음. eq:dVdT_config — V(ξ) 의 T-미분 손 재유도: ∂V/∂T|_ξ = ΔS_rxn,j/F + (R/F)ln[ξ/(1−ξ)], 그리고 (1/F)∂S_config/∂θ|_{θ=1−ξ} = +(R/F)ln[ξ/(1−ξ)] — 부호 연결(L48 "+로 맞물린다") 정확. 부호 3분기(ξ→1: +∞ / ξ→0: −∞ / ξ=½: 0) 전건 옳음. L136 단위 환산(+29 J mol⁻¹K⁻¹ = +0.30 mV/K): 29/96485 = 0.3005 mV/K — 일치. L176–177 검산식 ΔH⁰_j=−FU_j+FT∂U_j/∂T: U_j 정의 역산으로 항등 성립, stage 2→1 수치(−16 J/mol/K, T=298, U_j=0.0853 V ⟹ −13.0 kJ/mol)가 Ch1 §3 예제값(−13000 J/mol)과 일치.
- ③ 교차 정합: L128 "Chapter 1 §14 의 반응 엔트로피 삼분해·슬롯 규칙" — ch1_sec14 제목·eq:lco-configsplit(중심 표준값 vs 내부 분포 분리) 실재, "config 중심/분포 분리에 한정한 대응" 한정 문구도 ch1_sec14 의 실제 범위와 정합.
- 확정 판정 존중: L138–140 MCMB 단위 [미검증] 각주는 정직 공백 관용(지적 제외).
- refute 시도: L59 "dilute 격자기체 모형이 같은 발산을 예측 \cite{occupation2019}" — occupation2019 는 원장 A 표 V1(ch2 무수정 군) 등재 키로 인용 자격 있음(반박 실패).
- 발견: 없음.

### ch2_sec03_vibel.tex (전문 정독 완료, 101행)

- ② 구본 대비: diff 결과 변경 2블록뿐 — (i) L8–9 페르미온/보손 배경 참조 1문장 신설, (ii) L17–21 B-005 중간식 인라인. 그 외 전 행 동일. CHANGE_LOG B-005 기재("표시 수식 블록·라벨·최종식 불변")와 정확히 일치 — eq:Svib_mode·eq:Se_start·eq:Se-ch2 라벨/식 불변 확인.
- ③ **B-005 손 재유도 검산(전 단계)**: f_k=k_BT ln(1−e^{−βℏω_k}) 에서 −∂f_k/∂T 를 처음부터 전개.
  - 곱 규칙 항: −k_B ln(1−e^{−βℏω}) — 본문 "곱의 규칙이 로그 항을" 귀속 정확.
  - 연쇄율 항: −k_BT·[∂ln(1−e^{−u})/∂u]·(du/dT), u=βℏω, du/dT=−u/T, ∂ln(1−e^{−u})/∂u=e^{−u}/(1−e^{−u})=n_k ⟹ +k_B βℏω n_k — 본문 "β=1/k_BT 를 지나는 연쇄율이 점유 항을" 귀속 정확.
  - 중간식 S=−k_B ln(1−e^{−βℏω})+k_B βℏω n_k — **일치**.
  - BE 항등식 2건: n_k=1/(e^{βℏω}−1) ⟹ e^{βℏω}=(1+n_k)/n_k ⟹ βℏω=ln[(1+n_k)/n_k] ✓; e^{−βℏω}=n_k/(1+n_k) ⟹ 1−e^{−βℏω}=1/(1+n_k) ✓ — 본문 2건 모두 옳음.
  - 대입: −k_B ln[1/(1+n_k)]+k_B n_k ln[(1+n_k)/n_k] = k_B[(1+n_k)ln(1+n_k)−n_k ln n_k] = eq:Svib_mode — **전 단계 옳음, 점프 없음**. B-005 는 물리 불변 보강으로 판정.
- ③ 배경 참조 1문장(L8–9) 분업 대조: ch1_sec02a:171–188 의 bgbox 실제 열람 — 박스 제목 "페르미온·보손과 양자 통계" 문자 일치, 내용(동일입자 교환 대칭·스핀–통계 정리·Pauli 배타·BE/FD 분포)이 Ch2 서두 1문장의 예고 항목과 1:1, bgbox 말미(ch1_sec02a:185–187)가 "진짜 양자 통계가 일하는 곳은 Chapter 2 — 포논 BE·전자 FD" forward 다리로 호응 — **분업 성립**.
- ③ 교차 정합: L64 "Chapter 1 §15 의 전자 엔트로피 유도가 상술" — ch1_sec15:61–93 에 [FD 정보 엔트로피 합 → Sommerfeld → C_e → S_e] 사슬 실재(주장 그대로). **eq:Se-ch2(Ch2 L61) vs eq:Se(ch1_sec15:82) 라벨 별개** 확인(자산 주석 C-65 의 충돌 회피 개명 이행). L89–90 "Chapter 1 §8·§9 활성화 엔트로피" — ch1_sec08:89–91 Eyring·ΔG_a^eff=ΔH_a^eff−TΔS_a 실재, 대응 정확. L76 "Chapter 1 §13·§15" — 두 절 제목(LCO order–disorder/MIT·LCO 전자 엔트로피) 일치.
- ① 수식 재검산: Sommerfeld 적분 ∫(−∂f/∂E)(E−E_F)²dE=(π²/3)(k_BT)² 표준값 일치, C_e=(π²/3)k_B²Tg(E_F)·S_e=∫C_e/T′dT′ 적분 옳음. eq:Se_start 차원(L66: k_B²Tg 알짜 차원 k_B) 옳음.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| C2F1-01 | ch2_sec03_vibel.tex:16 | L | ① | 단일 모드 "자유에너지" f_k=k_BT ln(1−e^{−βℏω_k}) 가 영점 에너지 ℏω/2 무언급 생략 — 모드 바닥 기준 에너지 규약이면 정확하나 규약 자체가 명시돼 있지 않음. Ch1 §2 Part 0(ch1_sec02a:288–292)은 같은 자리에서 "영점 에너지 인자는 온도 무관 상수" 가드를 명시하여 챕터 간 노출 수준 비대칭 | S=−∂f/∂T 에 ℏω/2 는 기여 0 이므로 결과 전부 불변(재유도로 확인). B-005 가 유도를 명시화한 뒤라 G-derive 렌즈에서 기준 규약 1구절 공백이 상대적으로 드러남. v1.0.19 에도 동일 문구(regression 아님) | f_k 직후 "(영점 에너지 ℏω_k/2 는 온도 무관이라 S 에 기여하지 않아 생략)" 반구절 부연 — 선택 사항 |

### ch2_sec04_einstein.tex (전문 정독 완료, 115행)

- ② 구본 대비: diff 완전 동일 — regression 없음.
- ③ 교차 정합(u_j 동명 별개 각주): L20–22 각주 "Chapter 1 §4 spinodal 근의 u_j=√(1−2RT/Ω_j) 와도 동명 별개" — ch1_sec04:35 `u_j\equiv\sqrt{1-\frac{2RT}{\Omega_j}}\ (\Omega_j>2RT)` 실재, 식 문자 일치. 각주 가드 정상 작동(rubric B5 부합).
- ① 수식 재검산(전건): (i) eq:Svib_mode→eq:Svib-einstein 항등식 (1+n)ln(1+n)−n ln n = −ln(1−e^{−u})+u n — B-005 검증 항등식 2건으로 재확인, "단일모드 특수화이지 새 근사가 아니다" 진술 옳음. (ii) 고전극한 전개: −ln(1−e^{−u})→−ln u+u/2, u/(e^u−1)→1−u/2, u/2 상쇄 → R[1+ln(T/θ_E)] — 손 전개 일치. (iii) 저온극한 S→0 옳음. (iv) ΔF_vib=RT ln(1−e^{−θ_E/T}) 의 −∂/∂T = S_vib 재유도 일치. (v) eq:dUvib 적분 사슬(∫ΔS dT′ 분해→ΔF 로 닫기→∂ΔU_vib/∂T=ΔS_vib/F) 손 재유도 전 단계 일치, T_ref 영점 자동 고정 논리 옳음. (vi) Bernardi/Kirchhoff 진술(∂U/∂T=ΔS(T)/F 는 T-의존 ΔS 에도 정확) — Gibbs–Helmholtz 로 항등 성립, 옳음.
- ① 수치 검산(Python 재계산): θ_E=700 K·T_ref=298.15 K, T=278.15/298.15/318.15/348.15 K ⟹ −3.738/0/+3.700/+9.138 μV/K — 본문 −3.74/0/+3.70/+9.14 와 반올림 자리까지 일치. 단위 환산 50→580 K·80→928(≈930) K·700 K≈60.3 meV — L23·L98 표기와 일치.
- refute 시도: L104 "2-온도 유한차분은 곡률과 선형을 합으로만 보아 축퇴" — ΔS_vib(선형+곡률)·S_e(순선형) 두 함수형이 국소 기울기 1개 자유도에 사영되면 비식별이라는 논리 — 옳음(반박 실패). 3온도점 필요 주장은 함수형 2개+영점 구속 관점에서 타당.
- 발견: 없음.

### ch2_sec05_mixing.tex (전문 정독 완료, 240행)

- ② 구본 대비: diff 결과 변경 1블록뿐 — L168–169 각주에 `\cite{dahn1991,ohzuku1993}` 삽입(줄바꿈 재배치 동반, 문장 무변). **U9·C-017·C-018 의도 변경과 1:1**, 그 외 regression 없음.
- ③ **U9 인용-주장 정합 검증**: 주장 = "2L→2·2→1 을 두-상으로 지목하는 근거는 문턱 부등식이 아니라 실측 plateau·staging 문헌의 상평형". (i) dahn1991 = PRB 44, 9170 (1991) "Phase diagram of Li_xC6" — 전기화학 실측 기반 Li_xC6 상도표·plateau·staging 논문으로 주장 내용과 정확 부합. (ii) ohzuku1993 = JES 140, 2490 (1993) 흑연 삽입 화합물 형성(XRD·stage 구조) — plateau·stage 실측 문헌으로 부합. (iii) 인용 위치 = 주장 직후(rubric E1 부합). (iv) 각주 내 수치 "2RT≈4957 J/mol": 2×8.314×298.15=4957.6 — 옳음. (v) "Chapter 1 의 초기값 Ω 는 네 전이 모두 임계 초과" — ch1_sec10 tab:staging Ω=6000/8000/10000/13000 J/mol 전건 >4957 — 옳음. (vi) "(Chapter 1 의 staging 초기값·post-fit 기준)" — tab:staging 의 anchor 출처가 실제로 dahn1991·ohzuku1993(ch1_sec10:25–28) — 삼각 정합.
- ① 수식 재검산(전건): eq:implicit 음함수 미분 사슬→eq:implicit_diff 옳음. eq:gj(∂ξ/∂U=ξ(1−ξ)/w) 옳음. eq:dxidT — a_j=(U−U_j(T))/w_j(T) 연쇄율 손 전개로 두 조각(−g_j∂U_j/∂T, −g_j(n_jR/F)z_j) 재현 — 옳음. eq:weighted 대입 사슬 옳음. 완전식 config 항 부호(+n_jRz_j/F) 옳음. eq:dwdT-nT 곱 미분 옳음. eq:single_config 는 sec02 eq:dVdT_config 의 n_j 일반화와 문자 정합. eq:hys_branch·eq:hys_rev — 분기 평균 논리·선형화 한정(ΔU^hys≪w_j) 서술 옳음(단일 전이 지배 시 z_j 는 x 고정이라 분기 무관 — 상쇄 정확, 겹침 구간은 1차 상쇄 — 본문 한정 그대로).
- ③ 교차 정합: L39 "Chapter 1 §2 의 조성 자유에너지 g_j(ξ)" — Ch1 TOC 1.2.4 g(ξ) 실재. L177 "Chapter 1 §7 의 broadening 절" — ch1_sec07(두-상 broadening, 세 출처 소절 TOC 1.7.2) 일치. L195–196 "Chapter 1 §4 의 분기 중심식에서 γ_jh_η,j=1 로 둔 특수형" — ch1_sec04:130 eq:Ubranch `U_j^d=U_j+½σ_d h_{η,j}γ_jΔU_j^hys` 실재, γ_jh_η,j=1 대입 시 Ch2 형태와 문자 일치, 방전=+½ 부호 방향(ch1_sec04:133–134 U_dis>U_ch)도 일치.
- ① 내부 수치 일관성 refute 시도: "그리드 실측 최대 0.18 vs 해석 상한 0.21 vs 구간 범위 [−0.21,+0.14]" — [−0.21,+0.14]를 해석 범위로, 0.18 을 그리드 샘플값으로 읽으면 0.18<0.21 로 자기일관(본문이 그 관계를 명시 서술) — 모순 아님(반박 실패). fig:blend 캡션 "−16→−5→0→+29 상승 방향" — tab:ds 값·탈리튬화 진행 순서(2→1 부터 4→3 까지)와 정합.
- 확정 판정 존중: "두-상"(전이 유형) 용어는 의미 분업 판정 유지 — 지적 제외.
- 발견: 없음.

### ch2_sec06_limits.tex (전문 정독 완료, 52행)

- ② 구본 대비: diff 완전 동일 — regression 없음.
- ① 표 tab:limits 6 코너 전건 대조: ξ→1/ξ→0/ξ=½ 은 sec02 부호 3분기와 일치, Ω→2RT 는 sec01 eq:slope_BW 와 일치, 단일 봉우리 환원은 eq:weighted→eq:single_config 포함 관계와 일치(직접 대입으로 재확인), 고온 코너는 Sommerfeld 축퇴 전제(k_BT≪E_F)의 적용 한계를 정직 명시 — 전건 옳음.
- refute 시도: keybox "상수 표준값+분포만으로 측정급 곡선" 주장 — sec05 수치 검증(완전식=유한차분 표시 정밀도 일치)이 근거로 실재하므로 과장 아님(반박 실패). LCO MIT 예외 한정도 sec03 ssec:elec 와 정합.
- 발견: 없음.

### ch2_sec07_revheat.tex (전문 정독 완료, 58행)

- ② 구본 대비: diff 완전 동일 — regression 없음.
- ① 부호 물리 재검산(sec00 L26 이월 검증 포함): eq:qrev — 하프셀(흑연 vs Li 금속)에서 셀 방전(I>0)=작동전극 리튬화, 리튬화 반응(Li+C6→LiC6)의 ΔG=−FU_oc ⟹ ΔS=+F∂U_oc/∂T(L35–37 srcbox 유도 옳음), 가역 흡수열 = TΔS·(I/F) ⟹ 발열률 Q̇_rev=−(IT/F)ΔS — **부호 사슬 전 단계 옳음**. ΔS>0 방전 시 흡열/ΔS<0 발열(L45–47) 물리 정합. sec00:26 의 동일식과 문자 일치 — 챕터 내 일관.
- ① 라벨 층위 경고(ssec:signlabel) 검증: "Bernardi 셀 방전=하프셀 리튬화" vs "Ch1 방전 라벨=탈리튬화(σ_d=+1)" — 실제로 반대 화학 방향이 맞으며(하프셀에서 흑연이 양극 역할), 전류 부호로 읽으라는 지침은 물리적으로 정확한 해소책. Q̇_irr=I(U_oc−V)≥0 은 (U_oc−V) 부호가 I 와 함께 뒤집혀 2법칙 강제 — 옳음.
- ③ 인용 정합: bernardi1985(원장 V1·ch2 무수정군)·newman·msmr_partI·standardised2024 전건 원장 등재 키.
- 발견: 없음.

### ch2_sec08_synthesis.tex (전문 정독 완료, 144행)

- ② 구본 대비: diff 완전 동일 — regression 없음.
- ① **수치 전건 독립 재계산(지시 항목)**: Chapter 1 tab:staging 입력(ΔH=−11700/−13500/−13100/−13000, ΔS⁰=+29/0/−5/−16, Q=0.10/0.12/0.25/0.50, U_j=(−ΔH+TΔS)/F 규약 — ch1_sec10:49 명시)에서 전하 보존 음함수를 직접 풀어 재현:
  - U_oc(x̄=0.25)=74.4 mV ✓ (주의: 표의 반올림 U_j=210/140/120/85 mV 를 쓰면 74.1 mV 로 0.3 mV 어긋남 — 문서 값은 Ch1 규약(열역학 입력에서 U_j 산출)을 따른 것으로 정합 확인).
  - tab:worked 전행: ξ_j=0.005/0.072/0.143/0.395 ✓ g_j=0.19/2.61/4.77/9.30 ✓ 비중=0.003/0.051/0.193/0.753 ✓ ΔS⁰_j/F=+0.301/0.000/−0.052/−0.166 ✓ config=−0.458/−0.220/−0.154/−0.037 ✓ (표시 자리 전부 일치).
  - ΣQ_jg_j=6.18 /V ✓, 2→1 비중 75% ✓.
  - **가중 평균 산술: 0.753(−0.203)+0.193(−0.206)+0.051(−0.220)+0.003(−0.157)=−0.20431 → −0.204 mV/K ✓** (괄호 값도 표의 [중심+config] 행합과 일치: −0.166−0.037=−0.203 등 전건 확인). 단순식 −0.134 ✓, config 몫 −0.070 ✓ (−0.204−(−0.134)=−0.070 정합).
  - round-trip: T±3 K 유한차분 = −0.2039 mV/K = 해석 완전식과 일치 ✓ (<0.001 μV/K 주장과 부합).
  - ΔS(0.25)=F×(−0.204 mV/K)=−19.7 J mol⁻¹K⁻¹ ✓, Q̇_rev/I=−T∂U/∂T=+60.8 mV ✓.
  - tab:qrev 5점 표 전건: U_oc=43.5/74.4/109.0/148.8/195.2 mV ✓, ∂U/∂T=−0.307/−0.204/−0.089/+0.044/+0.218 mV/K ✓, ΔS=−29.6/−19.7/−8.6/+4.3/+21.0 ✓, Q̇_rev/I=+91.5/+60.8/+26.6/−13.2/−64.9 mV ✓, 발열→흡열 부호 교대 ✓ — **25개 수치 전건 독립 재현**.
- ① eq:complete — sec05 완전식 유도와 문자 일치, 입력 사양(ΔS⁰_j 정의·w_j 이중지위·Einstein 확장 주입 자리) 전부 앞 절과 정합.
- ③ 교차 정합: L23–24 "Chapter 1 §5 의 평형 진행률에서 σ_d→s=+1·분기 shift 無로 둔 형" — ch1_sec01:29 ξ_eq=logistic[σ_d(V−U)/w] 와 eq:logistic 의 관계 서술 정확(σ_d=+1 대입 시 동형).
- refute 시도: L54 "가중 분모 ΣQ_jg_j=6.18 Q_cell/V 가 곧 그 점의 측정 dQ/dV" — d(Qx̄)/dU=ΣQ_jg_j 항등으로 옳음(반박 실패). tab:qrev 캡션의 경계행(x̄≈0.75) 부호 반전 가능 한정 — 단순식 값 재계산 시 +0.044→단순식으로는 상승( +0.070 급) 방향성 확인, 한정 서술 타당.
- 발견: 없음.

### ch2_sec09_method.tex (전문 정독 완료, 43행)

- ② 구본 대비: diff 완전 동일 — regression 없음.
- ③ 교차 정합: L16 "Chapter 1 §1 의 V_n=V_app−σ_d|I|R_n" — ch1_sec01:179 eq:vn `\boxed{V_n=V_\app-\sigma_d|I|R_n}` 과 문자 일치. L19–20 "MSMR(Multi-Species, Multi-Reaction) 절차(Chapter 1 §17)" — §17=ch1_sec17_msmr(MSMR 동형) 일치, 풀네임은 rubric C4·원장 확정 명칭("Multi-Species, Multi-Reaction", bakerverbrugge2018 명명 원전)과 일치.
- ① 절차 5단계 논리 검토: 저율 준평형→분극 분리→다온도 동시 피팅→ΔS⁰_j=F dU_j/dT→분포 항 자동 — 앞 절 결과와 전건 정합, 3온도점 요건(§2.4 연계)도 일관. 정직한 한계 5건은 Gn 관용(결함 아님) — 그 중 (1) "시뮬 자기일관성≠실측 검증" 구분은 sec05 srcbox 전제 명시와 동일 논조로 일관.
- 발견: 없음.

### ch2_sec10_closing.tex (전문 정독 완료, 25행)

- ② 구본 대비: diff 완전 동일 — regression 없음.
- ① 맺음 요약의 사실 정합: "수치 검증 완료(파생 A)"·"<0.001 μV/K 일치"·"다섯 SOC 표"·"저-x̄ 발열·고-x̄ 흡열" — 본문 실적과 전건 일치(sec08 재계산으로 이미 독립 확인). "broadening 기원은 Chapter 1 §7" 재확인 — 일치.
- 발견: 없음.

