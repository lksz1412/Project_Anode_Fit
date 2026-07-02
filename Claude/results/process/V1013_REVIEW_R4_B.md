# V1.0.13 P5 검수 라운드 4 — 검수자 B (라인·부호 창)

- 대상: `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` L1001–1920 (N3 히스테리시스 ~ N9 합산·tab:staging·Part II 도입)
- 코드 대조: `Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py`
- 청크 스킴: ~80줄 라인·부호 창 12개 (아래 coverage 선언). 창마다 ±부호·지수 부호·첨자·부등호·분모/분자 위치 전수 점검 + 수치 재계산.
- 역할 경계: 검수 의견만 — tex/코드 수정 없음. 모든 지적에 줄 번호·원문 인용.

---

## 지적 사항

### B4-1 [HIGH] L1855–1856 — LCO σ_d 괄호 라벨이 eq:lco-sigmaslot 과 정면 모순

- **위치**: L1854–1856 (sec:lco-map "양극 부호 규약" 문단) vs L1911–1912 (eq:lco-sigmaslot)·L1920–1921 (item (a)).
- **무엇이**: L1855–1856 원문 — "방전($\sigma_d=+1$)은 LCO 입장에서 \emph{리튬화}(Li$^+$ 가 LCO 로 들어와 Co$^{4+}\!\to$Co$^{3+}$ 환원, $x$ 증가, 전위 하강)이고, 충전($\sigma_d=-1$)은 \emph{탈리튬화}($x$ 감소, 전위 상승)이다." 즉 LCO 방전에 $\sigma_d=+1$, 충전에 $\sigma_d=-1$ 을 배정한다.
- **근거**: 같은 범위의 확정 규약 박스 L1911–1912 — "$\sigma_d=+1\ \Leftrightarrow\ $탈리튬화(산화, $\xi:0\!\to\!1$, 전위 상승 진행): 흑연 하프셀 --- 방전$\mapsto+1$, \textbf{LCO 하프셀 --- 충전$\mapsto+1$}". L1920–1921 도 "흑연 방전과 LCO 충전이 같은 부호로 성립". L1859 도 "LCO 양극에서 충전(탈리튬화)이 $\xi:0\!\to\!1$ 의 주 진행 방향". 코드도 동일: `Anode_Fit_v1.0.13.py` L671 "(충전 곡선↦s=+1 — Ch1 sec:lco-direction 방향 규약, eq:lco-sigmaslot)", L685–686 `_delith_is_discharge: bool = False`(curve() 가 LCO 의 셀 라벨을 뒤집어 탈리튬화 부호로 환산). 결정적으로 코드 docstring L667–669 는 같은 문장을 쓰되 **한정어를 갖고 있다**: "방전 σ_d=+1 은 LCO 엔 리튬화이며 ∂U_j/∂T=ΔS_rxn/F 의 부호 관계가 흑연과 같으므로 σ_d 를 뒤집지 않는다 — **단 이는 평형·∂U/∂T 경로 한정이다**." tex L1854–1858 에는 이 한정어가 없어, 독자가 L1855 의 배정을 방향 의존 작용처(분극·분기·꼬리)에 그대로 쓰면 분기 부호가 뒤집힌다 — 리튬화 가지가 위로 가서 L1922–1925 의 "탈리튬화 봉우리가 높은 전위 쪽" 불변과 모순.
- **수정안**: (i) L1855–1856 의 두 괄호 "($\sigma_d=+1$)"·"($\sigma_d=-1$)" 를 삭제하고 화학 서술만 남기거나, (ii) 코드 docstring 의 한정어를 이식 — 예: "…이다(단 이 방전$\mapsto\sigma_d{=}+1$ 라벨 읽기는 평형·$\partial U/\partial T$ 경로 한정이며, 방향 의존 작용처의 $\sigma_d$ 슬롯 배정은 \S\ref{sec:lco-direction} 의 탈리튬화 규약 --- LCO 충전$\mapsto+1$ --- 을 따른다)".

### B4-2 [MEDIUM] L1074 fig:hysloop — 곡선 내부 좌표가 eq:Veq(Ω=4RT) 참값에서 이탈

- **위치**: L1074 (tikz plot coordinates), 캡션 L1088 "비단조 평형 전위 $V_\eq(\xi)$(식~\eqref{eq:Veq}, $\Omega_j=4RT$)".
- **무엇이**: $y=\ln[\xi/(1-\xi)]+4(1-2\xi)$ 로 전수 재계산하면 —
  - $(0.4, 0.47)$·$(0.6, -0.47)$: 참값 $\pm0.3945$ (오차 $+0.075$, 봉우리 참값 1.066 의 7%);
  - $(0.2, 0.99)$·$(0.8, -0.99)$: 참값 $\pm1.0137$ (오차 $-0.024$);
  - $(0.05, 0.62)$·$(0.95, -0.62)$: 참값 $\pm0.6556$ (오차 $-0.036$).
  - 정확한 점(검증 PASS): spinodal $(0.1464, \pm1.066)$(참값 $u=0.70711$, $y=1.06568$ — ΔU 화살표 폭 $2\times1.066$ 도 닫힌꼴 $2[4u-2\,\mathrm{artanh}\,u]=2.13137$ 과 정합), $(0.1, 1.00)$, $(0.3, 0.75)$, $(0.5, 0)$, $(0.02, -0.05)$, $(0.08, 0.92)$ 및 그 거울점.
- **근거**: 캡션이 식·Ω 값을 명시하므로 좌표는 그 식의 값이어야 한다. R2 에서 fig:logistic 실선을 같은 이유로 4dp 참값으로 교체한 전례와 비대칭.
- **수정안**: $(0.05,0.6556)$ $(0.2,1.0137)$ $(0.4,0.3945)$ $(0.6,-0.3945)$ $(0.8,-1.0137)$ $(0.95,-0.6556)$ 로 교체 (fig:logistic 4dp 방식).

### B4-3 [LOW] L1355–1357 — "4L↔3L 전이" 한 라벨을 표의 두 행(4→3·3→2L)에 대응

- **위치**: L1355–1357 원문 — "dilute$\to$stage4 영역과 4L$\leftrightarrow$3L 전이(표~\ref{tab:staging} 의 $4\!\to\!3\cdot3\!\to\!2\mathrm L$ 행에 해당; …)". 동일 축약 L1125 "dilute$\to$stage4$\cdot$4L$\leftrightarrow$3L", L1463 "(dilute$\cdot$4L--3L)".
- **무엇이**: 문헌 L-명명으로 표의 두 solid-solution 행은 각각 $4\mathrm L\!\to\!3\mathrm L$(행 4→3)과 $3\mathrm L\!\to\!2\mathrm L$(행 3→2L) — 전이 **둘**이다. "4L↔3L 전이" 단수 라벨이 두 행을 받는 현재 문구는 R3 삽입 명명 해설("표의 정수 행 라벨과 같은 전이다")로도 남는 잔여 부정합.
- **근거**: tab:staging (L1809–1810) 행 라벨 "4→3"·"3→2L"; L1356–1357 의 L-명명 해설 자체.
- **수정안**: "4L$\to$3L$\cdot$3L$\to$2L 전이(표의 $4\!\to\!3\cdot3\!\to\!2\mathrm L$ 행)" 로 복수화 (L1125·L1463 도 동일 손질).

### B4-4 [LOW] L1272 — "그 분포의 변곡(spinodal)" 은 대상 객체가 어긋난 표현

- **위치**: L1271–1272 원문 — "자기무모순 분포가 된다 — 그 비단조성이 \S\ref{sec:hys} 의 히스이고, 그 분포의 변곡(spinodal)이 식~\eqref{eq:spinodal} 이다."
- **무엇이**: spinodal 은 자유에너지 $g(\xi)$ 의 변곡점($g''=0$ — L985 에서는 옳게 "변곡점 $\xi_s^\pm$" 로 $g$ 에 귀속)이고, **분포(등온선 $\xi(V)$) 쪽에서는 변곡이 아니라 접힘(수직 접선, $\dd\xi/\dd V\to\infty$)** 이다. "분포의 변곡" 은 다른 객체의 성질을 옮겨 붙인 서술.
- **근거**: eq:spinodal 유도(L959, $g''=0$)·L985 의 올바른 용법과의 자체 비교.
- **수정안**: "그 분포가 접히는 점(자유에너지 $g$ 의 변곡, spinodal)이 식~\eqref{eq:spinodal} 이다" 류로 객체를 바로잡기.

### B4-5 [NOTE] L1194 fig:barrier(b) — driven 곡선 가장자리 점 4개가 균일 기울임 곡선에서 이탈 (도식 한정)

- **위치**: L1194 coordinates. 내부 점 $(1.5,0.188)$ $(2,0.463)$ $(2.5,0.737)$ $(3,0.825)$ $(3.5,0.649)$ $(4,0.288)$ $(4.5,-0.074)$ $(5,-0.250)$ 은 기울임 $-0.0875(x-1)$ 을 정확히 따르나(전수 재계산 PASS), $(0,0.550)$ $(0.5,0.232)$(기울임 미적용) $(5.5,-0.118)$(참 $-0.162$) $(6,0.200)$(참 $0.1125$) 는 벗어난다.
- **근거**: 물리 치수는 전부 정확 — $\Delta G_a=0.9$, $A=0.35$, $\chi A=0.175$(정점 $1.0\to0.825$), 정방향 장벽 $0.725=\Delta G_a-\chi A$, 역방향 $1.075=\Delta G_a+(1-\chi)A$. 부호 방향(전위↑⇒정방향 장벽↓) 일치. 캡션에 좌표 정밀성 주장 없음 — 미관 항목.
- **수정안**: 선택 사항(가장자리 4점을 기울임 곡선 값으로 교체하면 곡선 굴곡 매끈).

### B4-6 [NOTE] L1718–1719 — 닫힌꼴 점프의 "높이" 판은 $L_V\ll w$ 영역 전제 (실무상 무해)

- **위치**: L1718–1719 원문 — "그 크기는 격자에 무관하게 $\nu$ 만의 닫힌 함수 $1-(1/\nu)\big/\!\big(e^{1/\nu}-1\big)$ (중심 peak 높이$\cdot$전이 면적 둘 다)".
- **무엇이**: 면적 판은 임의 $L_V$ 에서 정확(재유도: $r_i=\rho r_{i-1}+\rho\Delta\xi_i \Rightarrow \sum r_i=\tfrac{\rho}{1-\rho}$, 면적$=\tfrac{1}{\nu}\tfrac{1}{e^{1/\nu}-1}$). 높이 판은 $r_i\approx\xi'\,\Delta\,\rho/(1-\rho)$ 근사, 곧 $L_V\ll w$(완만 변화) 전제에서 같은 인자 — 기본 설정(grid $\sim2\times10^{-4}$ V, 문턱 $L_V=2\Delta\sim4\times10^{-4}$ V $\ll w\sim0.026$ V)에서 성립하므로 진술은 실질 참. 한정어 한 구가 있으면 완전.
- **수정안**: 선택 사항 — "(문턱 $L_V\ll w_j$ 인 기본 격자 영역에서)" 부가.

### B4-7 [INFO] 코드 쪽 라벨 표기가 tex 라벨과 상이 (tex 결함 아님 — 유지보수 참고)

- **위치**: py L137 "eq:hysdU"(tex 는 eq:dUhys), L148·L474 "eq:hyscenter"(eq:Ubranch), L162·L315·L324 "eq:chisum"(eq:chid), L335 "eq:tail"(eq:LV), L503 "eq:closed"(eq:peakshape), L405·L436 "eq:hysmaster"(eq:vn).
- **무엇이/근거**: tex 본문의 코드 대응 서술은 전부 함수 동작 기준으로 정합(아래 검증 목록) — 어긋난 것은 코드 주석의 라벨 문자열뿐. 향후 grep 기반 상호참조 시 헛발 위험.
- **수정안**: 범위 밖(코드) — v12 정리 시 라벨 통일 권고만 기록.

---

## 검증 PASS 목록 (부호·수치 전수 재계산 근거)

**부호·항등식**: eq:hyssub 대입 $(1\pm u)/(1\mp u)$·$\mp u$ ✓; eq:hysdiff 로그 차 $=-4\,\mathrm{artanh}\,u$ ✓; eq:dUhys $\ge0$(양수성 $u-(1-u^2)\mathrm{artanh}\,u=+\tfrac23u^3+O(u^5)$) ✓; Taylor $\to\tfrac{8RT}{3F}u^3$·$u^3\propto(T_c-T)^{3/2}$·$T_c=\Omega/2R$ ✓; eq:bv→eq:db $\chi$ 상쇄 ✓; eq:logisticsolve·eq:xieq·signbox(방전 $V\!\uparrow\Rightarrow\xi\!\uparrow$) ✓; 분포 관점 $\langle n\rangle=1/(1+e^{+\beta\Delta\mu})$·여집합 $\xi=1-\langle n\rangle$·$\Delta\mu=+sF(V-U)$ ✓; $\Delta\mu$ 에 $-\Omega(1-2\xi)$ 가산 ↔ eq:Veq $+\Omega(1-2\xi)$ 자기무모순 ✓; eq:belliden ✓; eq:eqpeak 높이 $Q/4w$·면적 $Q$ ✓; eq:Lqmid·eq:Lq·eq:kuniv·eq:Lqfull 지수 부호 ✓; eq:dHeff 의 $-\chi_d\Omega$(방전 $\xi\to1$·충전 $\xi\to0$ 모두 $+\Omega$ 흡수) ✓; eq:chid ✓; eq:memory 인과 커널·eq:lowpass ✓; 충전 격자 역전·꼬리 방향(방전 高$V$/충전 低$V$) ✓; eq:sum ✓; Part II item (a)(b) 부호 ✓.

**수치**: fig:logistic 26좌표 4dp 전수 재계산 — 전부 정확 (예: $z{=}{-}3$: $3/(1{+}e^3){=}0.1423$; $z{=}{\pm}2.5$ 미분: $0.2103$) ✓; $z_\mathrm{cut}$: $\xi(1-\xi){=}0.0125\Rightarrow z{=}\ln(0.98734/0.012660){=}4.3567\to4.357$ ✓; $\nu$ 닫힌꼴: $\nu{=}2$: $22.93\%$(면적 $0.7707$)·$\nu{=}8$: $6.12\%$·$\nu{=}10$: $4.92\%$·점근 $1/(2\nu)$ ✓; $RT/F{=}25.69$ mV·$2RT{=}4958$ J/mol ✓; $U(298)$ 4행 전수: $0.210875$/$0.139918$/$0.120321$/$0.085294$ V — 표값 대비 $+0.88$/$-0.08$/$+0.32$/$+0.29$ mV, 전부 $\pm1$ mV 내·"0.2109 표시 자리수 경계" 정확 ✓; fig:hysloop spinodal $u{=}0.70711$·$y{=}1.0657$·ΔU 화살표 $2.131$ ✓; fig:flux $\xi_\eq{=}2/3$(검정)·$1/2$(회색) ✓; fig:barrier 장벽 치수 $0.725/1.075/0.175$ ✓.

**코드 대조 (Anode_Fit_v1.0.13.py)**: func_dU_hys(L136–143)·func_U_branch(L146–151, h_eta 포함)·eq:center 분기조건 `gamma != 0.0 and Omega > 0.0`(L473)·hys_shift=func_U_branch(T_rep,0,…)(L476)·func_ksi_eq 오버플로 분기(L100)·V_work 호출(L484)·_n_factor 'n'우선→'w'역산→1(L301–307; L1384–1386 "'n' 제거해야 'w' 활성" 정합)·equilibrium 이 $U_j$ 중심·분기 없음(L387–395; R3 한정 문구 정합)·func_chi_d(L166)·func_dH_a_eff(L158)·func_L_q 로그형+$T_*$(L107–109)·resolver 가드 'L_V' 직접/I≤0·dH_a 부재→0(L342–349)·A=min(z_cut·n·RT, A_cap·RT)(L360)·비유한 L_q→0(L372–373)·|dVdq_qa|·L_q(L376)·_causal_lowpass lfilter zi=ρx₀→y₀=x₀·루프 y₀=x₀(L121–128; R3 초기조건 문구 정합)·L_V≤0/비유한→원신호(L116–117)·분기 스위치 ν=2 기본+isfinite(L257, L491)·충전 [::-1] 필터 [::-1](L502)·누적+np.interp+스칼라 반환(L506–509) — 전부 tex 서술과 일치. tab:staging ↔ GRAPHITE_STAGING_LIT(L711–740) 32개 값 + w 폴백 0.020/0.016/0.014/0.012·n=1·dS_a=0 전수 일치. LCO_MSMR_LIT 시연값 U=3.930/3.880/4.050·T1 dict x_MIT=0.85(L646–649) — tex L1879–1880 주장과 일치.

**직전 R1–R3 수정분(렌즈 ⑧, 담당 구간 10건)**: ① eq:belliden 전방참조 해소(L1118 — \S 참조만, \eqref 첫 사용 L1342 는 정의 후) ✓ ② eq:xieq 여집합 동치 문구(L1161–1162, 문법·물리 정합) ✓ ③ equilibrium 가역 기준선 한정(L1337–1339, 코드 정합) ✓ ④ 4L 명명 문구(L1356–1357 — 존재·문법 OK, 잔여 부정합은 B4-3) ✓/△ ⑤ ① 문단 eqref 제거(L1373–1377) ✓ ⑥ fig:logistic 4dp 좌표(전수 재계산 PASS) ✓ ⑦ affinity 확장 브리지(L1573–1575, 부호 사슬 정합) ✓ ⑧ lowpass 초기조건(L1661–1662, 코드 정합) ✓ ⑨ fig:relaxode 캡션 한정어·ν 정량(L1684–1687·L1716–1724 — 닫힌꼴·6.1%·4.9% 재계산 PASS, 미세 한정어는 B4-6) ✓ ⑩ U(298) ±1 mV 정합(L1817–1818, 4행 재계산 PASS) ✓.

---

## 가장 약한 1곳

**B4-1 (L1855–1856)** — 같은 Part II 도입 안에서 LCO $\sigma_d$ 배정이 두 문단에서 반대로 적혀 있다. 부호 규약은 이 장의 척추이고, eq:lco-sigmaslot 이 아무리 옳아도 먼저 읽히는 L1855 가 반대 배정을 무경고로 주므로 방향 의존 작용처(분극·분기·꼬리) 구현을 그르칠 수 있는 유일한 실질 위험 지점이다.

## 물리 불변 확인

- $U^{\dis}>U^{\chg}$: L1051(흑연)·L1922–1925(LCO 탈리튬화 가지 위) — 유지 ✓ (단 B4-1 의 라벨 모순이 문구 층위에서 이를 위협).
- $\Delta U_j^\hys\ge0$·$\Omega>2RT$ 문턱·$u_j=\sqrt{1-2RT/\Omega}$ — 유지 ✓.
- peak 양수성(평형 종 $\xi(1-\xi)/w\ge0$·꼬리 $(\xi_\eq-\xi_\mathrm{lag})/L_V>0$ 진행 방향) — 유지 ✓.
- 전위↑⇒배리어↓⇒꼬리↓(L1616–1620)·$|I|\to0\Rightarrow L_V\to0\Rightarrow$ 평형 환원 — 유지 ✓.
- $\sigma_d$ 슬롯 물리 내용 = 탈리튬화(eq:lco-sigmaslot ↔ 코드 `_delith_is_discharge` 환산) — 코드 층위 유지 ✓, tex 층위 예외 1건 = B4-1.

## Coverage 선언 (창 분할, missing = 0)

| 창 | 줄 범위 | 내용 |
|---|---|---|
| W1 | 1001–1080 | eq:hyssub·hysdiff·dUhys·Ubranch·center, fig:hysloop 좌표 |
| W2 | 1081–1160 | 폭 이중지위, eq:bv·db·logisticsolve |
| W3 | 1161–1240 | eq:xieq·코드 호출, fig:barrier·fig:flux 좌표 |
| W4 | 1241–1320 | signbox, sec:dist 분포 관점, fig:logistic 좌표, eq:belliden 전반 |
| W5 | 1321–1400 | eq:eqpeak, sec:broadening (a)(b)①② |
| W6 | 1401–1480 | ③(iii-a/b)·eq:ensavg·(c)금지 3항·keybox |
| W7 | 1481–1560 | fig:broadening, sec:lag 도입, eq:Lqmid·Lq·kuniv·Acut |
| W8 | 1561–1640 | eq:chid·dHeff·Lqfull·LV·codebox, sec:tail 도입 |
| W9 | 1641–1720 | eq:intfactor·memory·lowpass, fig:relaxode, eq:peakshape·branch |
| W10 | 1721–1800 | ν 정량 각주, 충전 격자 역전, fig:reversal, eq:sum, tab:staging 머리 |
| W11 | 1801–1880 | tab:staging 값·U(298) 정합, Part II 도입·양극 부호 문단, tab:lco-staging |
| W12 | 1881–1920 | LCO 표 잔여, eq:lco-sigmaslot, item (a)(b) 전반 |

경계 의존 확인용 범위 밖 정독: L985–1001(eq:Veq — W1 대입의 전제), 코드 L60–190·280–570·630–750.

## 5줄 요약 (오적발 자기표시)

1. HIGH 1건: L1855–1856 LCO $\sigma_d$ 괄호 라벨이 eq:lco-sigmaslot(L1911–1912)·item (a)와 정반대 — 코드 docstring 의 "평형·∂U/∂T 경로 한정" 한정어가 tex 에 누락된 것이 원인(확정, 원문 인용 완비).
2. MEDIUM 1건: fig:hysloop 내부 좌표 3쌍이 eq:Veq(Ω=4RT) 참값에서 최대 +0.075 이탈(재계산 근거 확정) — 단 spinodal·중심·ΔU 치수는 정확하므로 "도식 자유도로 의도된 근사" 라는 반론 여지는 남음(그 경우 LOW 강등 타당).
3. LOW 2건(4L 명명 잔여 부정합·"분포의 변곡" 객체 어긋남)은 문구 층위 — 오적발 가능성 낮으나 어느 쪽도 물리 값은 불변.
4. R1–R3 수정분 10건 전부 존재·정합 재확인, fig:logistic 26좌표·ν 닫힌꼴·z_cut·U(298) 4행 등 수치 전수 재계산 PASS — 여기서 새 결함 0.
5. 자기 반박(refute mandate): B4-6·B4-5 는 결함이라기보다 한정어·미관 수준임을 명시(NOTE 강등 완료); B4-1 만은 두 원문이 상호 배타라 오적발일 수 없다.
