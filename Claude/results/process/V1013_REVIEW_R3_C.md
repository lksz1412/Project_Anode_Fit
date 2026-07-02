# V1.0.13 P5 검수 라운드 3 — 검수자 C (식·유도 단위 청크)

- 대상: `graphite_ica_ch1_v1.0.13.tex` Part II (L1790–2912 정독; 담당 공식 범위 sec:lco-intro L1810~끝, nodemap·facade·signcheck 포함) + `graphite_ica_ch2_v1.0.13.tex` 전문(L1–793) + `Anode_Fit_v1.0.13.py` 전문(L1–881)
- 청크 스킴: **식·유도 단위** — 담당 구간 전 번호식·boxed 식을 원문에 기대지 않고 독립 재유도 후 원문 대조. 재계산 가능한 수치는 전수 재계산(독립 스크립트 실행 포함 — 산출 로그는 본문에 인라인, 원본 tex/py 무수정).
- 등급: [MEDIUM] 수정 권고 / [LOW] 선택적 / [PASS] 재유도 일치(오적발 방지 기록)

---

## A. 지적 사항

### [MEDIUM] M1 — Ch2 L607–625 (파생 D): 분기 부호 ±↔ch/dis 대응이 Ch1 eq:Ubranch 와 어긋나는 자연 독해를 허용
- **무엇이**: L608 "분기별 전이 중심을 $U_j^{(d)}=U_j\pm\tfrac12\Delta U_j^\hys$ (방향 $d=$ ch/dis)로 두면" — 수학 표기 관례상 ±의 위치 대응은 (+↔ch, −↔dis)로 읽힌다.
- **근거(재유도)**: Ch1 eq:Ubranch(L2153–2158) $U_j^{\,d}=U_j+\tfrac12\sigma_d h_\eta\gamma\,\Delta U^\hys$, eq:lco-sigmaslot(L1892–1898) 탈리튬화=+1. 흑연 라벨에서 방전=탈리튬화이므로 **dis=+½(위 가지), ch=−½(아래 가지)** — Ch1 L2165–2168 "탈리튬화 $+\tfrac12$ 위·리튬화 $-\tfrac12$ 아래"와 동일. 따라서 positional 독해(ch↔+)는 Ch1 과 반대다. 파생 D 는 명시적으로 "흑연 OCV"(L607) 문맥이라 Ch1 라벨이 기본 프레임인데, 어느 라벨 층위인지·어느 가지가 +인지 미지정. §2.6 의 ★라벨 층위 주의(L690–693)는 파생 D 이후에야 나온다. 아울러 Ch2 식은 Ch1 의 $\gamma_j h_{\eta,j}$ 축소 인자를 생략한 $\gamma h=1$ 특수형임도 무표기.
- **영향**: boxed 결과 eq:hys_rev(L618–620)는 두 가지 평균이라 ± 교환에 불변 → 산출 불변. 그러나 eq:hys_branch(L610–613)를 분기별로 구현하는 독자는 $g_j^{(\mathrm{ch})}/g_j^{(\mathrm{dis})}$ 를 반대 중심에 붙이게 된다(문건 자체가 "★최우선 결함 클래스"로 선언한 부호 사슬 항목).
- **수정안**: $U_j^{(d)}=U_j+\tfrac12\sigma_d\,h_{\eta,j}\gamma_j\,\Delta U_j^\hys$ (Ch1 eq:Ubranch 그대로, $\sigma_d$=탈리튬화 부호 — 흑연 라벨 dis=+½/ch=−½) 로 바꿔 적거나, 최소한 "(dis: $+\tfrac12$, ch: $-\tfrac12$ — 흑연 라벨)" 괄호를 병기.

### [MEDIUM] M2 — Ch1 fig:lco-electronic (L2432–2462): 그림 내 라벨 3건이 본문 부호·좌표 규약과 모순
- **무엇이/근거(좌표 검산)**:
  1. **축 화살표 (L2436)**: `{Li content $x$ (delithiation $\leftarrow$)}`. tick 매핑(L2438)은 plot-x 0→라벨 1.0, plot-x 1→라벨 0.0 — 즉 x 는 **오른쪽으로 감소**하고 탈리튬화(x↓)는 **오른쪽 진행**이다. 소스 주석 L2435 도 "`delithiation -> `"로 오른쪽을 명시 — 렌더 라벨 ←는 저자 주석·tick 배치 모두와 모순(리튬화 방향을 가리킴).
  2. **y축 라벨 (L2437)·노드 (L2449)**: "$\Delta S_e\propto-\partial g/\partial x$", "$\Delta S_e(x)$ bump" — 본문 ★부호 규약(L2335–2345, eq:dSe)은 **삽입 기준 $\Delta S_e=+\partial S_e/\partial x<0$** 이고, 그려진 양의 종은 $|\Delta S_e|\propto-\partial g/\partial x>0$ 이다. 캡션(L2455–2456)은 절댓값 기호를 정확히 붙였으나 축 라벨·노드는 절댓값 없이 $\Delta S_e$ 를 양의 종으로 지칭 → 그림만 보면 부호 규약과 반대로 읽힌다.
  3. **"insulator ($x\!\approx\!1$)" 노드 (L2445)**: plot-x 0.62 에 배치 — tick 매핑상 $x\approx0.38$(금속 측) 위치다. 절연체 영역은 plot-x 0~0.1(x≈1, 왼쪽).
- **수정안**: ① `$\rightarrow$` 로 정정(또는 "delithiation: $x\downarrow$, 오른쪽 진행" 문구). ② 축 라벨·노드를 $|\Delta S_e|$ 로. ③ 노드를 plot-x ≤0.1 부근으로 이동(공간이 좁으면 화살표 지시).

### [MEDIUM] M3 — Ch1 eq:lco-configsplit (L2556–2563)·eq:lco-slots (L2565–2573): 혼합 분포항의 $n_j$ 일반화 미전파 (R2 수정의 잔여 대칭 자리)
- **무엇이**: eq:lco-configsplit 의 혼합 분포항은 $R\ln[\xi_j/(1-\xi_j)]$ 인데 underbrace 부기가 "— $w_j(T)=n_jRT/F$ 서식이 자동 생성"이라 붙어 있다.
- **근거(재유도)**: $w_j=n_jRT/F$ 서식이 생성하는 항은 $\partial w_j/\partial T=n_jR/F$ 에서 $n_jR\ln[\xi_j/(1-\xi_j)]$ 다(Ch2 eq:dxidT L481–490 재유도와 동일: $\partial\xi_j/\partial T|_U=-g_j\partial U_j/\partial T-g_j(n_jR/F)z_j$). R2 는 Ch2 쪽 4곳(eq:dxidT·keybox L715·eq:single_config L564·코드 `entropy_coefficient` L587 `config=(n_j*R/F)*log(...)`)을 $n_jR/F$ 로 정합했고, Ch2 eq:dVdT_config(L255)에는 "자리당 $n_j{=}1$ 서식 — 전이별 일반형은 $n_jR/F$" 한정어를 달았다. Ch1 의 이 대응 자리(순수 격자기체 결과 $R\ln$ 자체는 물리로 옳음)는 한정어도 $n_j$ 도 없어, $n_j\ne1$ 피팅 시 "w 가 담는 항"과 계수가 어긋난다. eq:lco-slots 첫 행 "혼합 분포항은 $w_j$ 가 담음 — 재기입 금지"도 같은 주의 필요.
- **수정안**: Ch2 와 동일한 한정어 "(자리당 $n_j{=}1$; 일반형은 $n_jR\ln[\xi_j/(1-\xi_j)]$, Ch2 eq:dxidT)" 병기, 또는 항을 $n_jR\ln$ 으로 일반화.

### [LOW] L1 — LCO dict ΔH 재보정 수치의 상수 불일치: F=96485.332 로 역산된 값 vs 코드 F=96485.0
- **무엇이**: `LCO_MSMR_LIT` dict1 `dH_rxn=-391017.4`, dict2 `-375555.7`.
- **근거(산술 재계산, T=298.15)**: dict1 유효 $\Delta S=+6.0+\Delta S_e(-45.678262)=-39.678262$ (재계산: $\Delta S_e=-\tfrac{\pi^2}{3}R\tfrac{k_BT}{e_V}\tfrac{13}{0.05}\cdot\tfrac14=-45.6783$ — dict 주석 −45.678 정합·Ch1 "≈−46"(L2067·L2428, T=300 K 기준 −45.96) 정합).
  - $\Delta H=T\Delta S_\mathrm{eff}-F\,U$: **F=96485.332** → dict1 −391017.4, dict2 −375555.7 — **소수 첫째 자리까지 정확 재현**. **F=96485.0(코드 상수 L67)** → −391016.1 / −375554.4.
  - 따라서 코드 자체 상수로 순전파하면 $U(298.15)=3.930013/3.880013$ V (**+13.2/+13.5 μV**). dict3(−391360.0)은 어느 F 로도 정확 역산되지 않고(코드 F 기준 −391360.5) $U=4.049994$ V(−5.7 μV).
- **영향**: 폭 25.7 mV 대비 5×10⁻⁴ 수준 — 물리 무해. 다만 "ΔH = T_ref·ΔS_eff − F·U"(dict1 주석)·"U 세 값 … 목표 전위에 정합"(Ch1 L1862–1867) 선언과 코드 상수 사이의 자기일관성 흠.
- **수정안**: 코드 F 로 재역산(−391016.1/−375554.4/−391360.5) 또는 dict 주석에 "역산 상수 F=96485.332(CODATA)" 명기.

### [LOW] L2 — (범위 경계) Ch1 L1800–1801 "U(298) 정합 … 표의 U 와 일치": 4→3 전이만 3자리 반올림 불일치
- **근거(재계산)**: $U=( -\Delta H+298.15\,\Delta S)/F$: 4→3 (−11700, +29) → **0.21088 V → 반올림 0.211 ≠ 0.210** (0.88 mV). 3→2L 0.13992→0.140 ✓, 2L→2 0.12032→0.120 ✓, 2→1 0.08529→0.085 ✓. 코드 `__main__` print 도 "U(298)=0.211 (target 0.210)"로 출력된다(assert 아님).
- **수정안**: ΔH≈−11785 J/mol 로 정합화, 표를 0.211 로, 또는 "일치"→"≈1 mV 내 정합" 완화. (표 자체는 Part I 소속 — 검산 가능 문장 L1800 이 담당 경계에 걸림.)

### [LOW] L3 — Ch2 L255: R2 삽입 한정어가 만든 신규 전방 수식 참조 (렌즈 ⑧)
- **무엇이**: §2.2 eq:dVdT_config 내 "(… 전이별 일반형은 $n_jR/F$, 식~\eqref{eq:dxidT})" — eq:dxidT 는 §2.4(L489)에 정의. 전방 표지("후술" 등) 없는 식 번호 전방 참조.
- **수정안**: "식~\eqref{eq:dxidT}(후술, \S\ref{ssec:overlap})" 형태로 전방 표지 병기.

### [LOW] L4 — Ch2 srcbox L509–531 (파생 A 수치검증): 0.18/0.21/0.14 가 그리드 스팬 의존 수치인데 x̄ 범위 미명시
- **근거(독립 재현)**: 4-전이 흑연 파라미터로 음함수 $\sum Q_j\xi_j(U_\oc,T)=Q\bar x$ 를 풀어 FD($T$=292.15/298.15)·단순식·완전식을 재계산: **완전식−FD 최대 1×10⁻⁴ mV/K — "표시 정밀도(≲10⁻² mV/K) 일치·절대오차≈0" 주장 독립 PASS**. 반면 config 항(=단순식 잔차)의 극값은 그리드 끝점에서 로그적으로 커져 스팬에 민감: 175점 균일 그리드에서 $\bar x\in[0.02,0.98]$→[−0.309,+0.206], $[0.01,0.99]$→[−0.370,+0.264], $[0.005,0.995]$→[−0.430,+0.323] mV/K. 문건의 [−0.21,+0.14]·실측 0.18 은 대략 $\bar x\in[\sim0.04,\sim0.98]$ 급 스팬에 해당 — "0.18 은 극값 미샘플, 해석 상한 0.21" 해명은 **그 스팬 내에서** 내적 정합이나, 스팬이 명시되지 않아 제3자 재현이 닫히지 않는다(내부자료 \cite{numverif2026} 의존). 부수: srcbox L528 "~0.3 mV/K 급"은 재현 범위와 자릿수 정합.
- **수정안**: srcbox 에 x̄ 그리드 범위·간격(끝점 포함 여부) 1줄 명시.

### [LOW] L5 — Ch1 L2717: "≈0.48 mV/K" 반올림
- **근거**: $|\Delta S_e^{\rm mol}|/F=45.6783/96485=0.4734$ mV/K → 2유효자리 **0.47**. (×30 K=14.2 mV — "≈14 mV"는 유지.)
- **수정안**: 0.47 로.

### [LOW] L6 — Ch1 L2119: "$\Omega\le2RT$ 이면 $u$ 가 실수가 아니라" — 등호점 부정확
- **근거**: $u=\sqrt{1-2RT/\Omega}$ 는 $\Omega=2RT$ 에서 $u=0$ 실수(gap=0, R2 검산 항목과 동일 연속 극한). 허수는 $\Omega<2RT$ 에서만. 식 (2119 조건 명기)·코드(`Omega <= two_RT → 0`) 분기는 옳음 — prose 만.
- **수정안**: "$\Omega<2RT$ 면 허수, 등호에서 $u=0$ (gap 0 연속)".

### [LOW] L7 — 용어 첫 출현 병기 잔재 (Ch2)
- SOC: 첫 출현 L78(서) 미병기, 병기는 L336. MIT: 첫 출현 L327 미병기, 병기는 L427–428. (Ch1 Part II 는 MIT L1848·MSMR L1845·SOC L2059·DFT L1802 모두 첫 출현 병기 ✓.)
- **수정안**: L78·L327 에 병기 이동.

### [LOW] L8 — Ch2 fig:blend (L533–558): 개형이 본 장 흑연 사례와 역방향 + 캡션 좌표 표기 혼용
- **근거**: 축은 $\bar x$(delithiation, 우향 진행). 흑연 프로파일은 탈리튬화 진행에서 $\Delta S^0$ 가 −16→−5→0→+29 로 **상승**하는데, 개형은 $+\Delta S^0_j\to-\Delta S^0_{j+1}$ **하강** 블렌드로 그려짐 — 일반 모식도라 수학적 오류는 아니나 본문 유일 사례와 반대 방향. 캡션·본문(L501, L556)은 "$x$ 가 넘어갈 때"로 축 좌표 $\bar x$ 와 기호 혼용(★좌표 주의 L462–463 이 "고정 $\bar x$=고정 $x$"를 선언해 치명은 아님).
- **수정안**: 캡션에 "(모식 — 흑연 실제 프로파일은 상승 방향, 표~\ref{tab:ds})" 1구 병기 또는 개형 반전; 캡션 "$x$"→"$\bar x$".

### [LOW] L9 — 단위·기호 미세 불일치 2건
- (i) $g_{\max}$ 단위 접미: L2299 "13 e/eV/atom" vs eq:ggate 박스 L2372·fig 캡션 L2454 "13 e/eV" — eq:gunit(L2326)은 states/J/**atom**. /atom 접미 일관화 권고(문건 스스로 경고한 $N_A$ 혼동 예방).
- (ii) Ch2 L162 "$\beta F=1/w$": $\beta=1/k_BT$ 로는 $N_A$ 배 어긋남 — 몰 단위 $\beta_{\rm mol}=1/RT$ 임을 문맥이 암시하나 기호가 그대로. "$(1/RT)F=1/w$" 로 명시 권고.

---

## B. PASS 기록 (재유도·삼각 대조 일치 — 오적발 방지)

- **P1 eq:lco-sigmaslot 3작용처 부호 사슬 (L1892–1912)**: (a) 분극 $V_n=V_\app-\sigma_d|I|R_n$: $\sigma_d=+1$(산화)→$V_\app>V_n$ ✓ 흑연 방전·LCO 충전 동일 부호. (b) 분기 $+\tfrac12$ 위 = 탈리튬화 봉우리 고전위 ✓. (c) 꼬리 $\sigma_d=-1$ 격자 역전 ✓. **코드 삼각**: `_delith_is_discharge=True/False` + `curve()` 라벨 환산(L530–535) — 흑연 'discharge'→+1(무반전), LCO 'charge'→−1→반전→+1 = eq:lco-sigmaslot 'charge'↦+1 ✓. **수치 확인**: `LCOCathodeDQDV.curve(direction='charge') ≡ dqdv(s=+1)` 최대차 0.0. fig:lco-dirmap(L1927–1967) 노드·화살표 배선 4경로 전부 정확, 좌표(헤더 xshift 상쇄 ±24mm) 정상.
- **P2 MSMR 동형 사슬 (L2617–2671)**: eq:msmr→정규화(여집합 대수 $1-\frac{1}{1+e^{+a}}=\frac{1}{1+e^{-a}}$ ✓)→eq:lco-comp(지수 부호 반전 ✓)→eq:lco-msmrmap($f=+\sigma_d$ 는 진행률↔진행률 pairing 의 유일해 ✓; $f=F/RT$ 폭 흡수 재모수화 정합 ✓)→eq:lco-msmrpeak($|f|=1$, $|\dd\theta/\dd U|=\theta(1-\theta)/\omega$ 재유도 ✓).
- **P3 전자항 차원·부호 (L2309–2345)**: eq:dSe 자리당 [J/K]; eq:dSemolar $N_Ak_B^2=Rk_B$ → [J/(mol·K)] 도착 ✓; eq:gunit 나눗셈 방향 ✓($e_V$ 곱하면 $1/e_V^2\approx4\times10^{37}$배 — 배수 표기도 검산 일치); 삽입 $x\!\uparrow$→금속→절연체→$\partial g/\partial x<0$→$\Delta S_e<0$ ✓; 게이트 방향(σ(z), x=1 에서 g≈0·x=0.75 에서 ≈0.88g_max) ✓; **★R2 정정부 L2376 "$\propto\partial g/\partial x<0$" 확인** — 정정 유지, 잔여 $\partial\sigma/\partial x$ 없음. eq:dSegate 닫힌식(연쇄율 $\sigma'/\Delta x$) ✓. 코드 `func_dSe_molar` 와 식 1:1, 골 깊이 재계산 **−45.678262** = dict 주석 −45.678 = Ch1 −46 반올림 ✓.
- **P4 $T^2$ 곡률 (L2351–2363, eq:U1T2)**: $\int_{T_0}^{T}a_eT'\dd T'=\tfrac{a_e}{2}(T^2-T_0^2)$ 재적분 ✓, $a_e$ 정의(J/(mol·K²))·부호 ✓; eq:lco-U1V 적분형과 정합, 동결 구현의 선형 $U(T)$ 서술(L2710–2714)=코드 seam(T_ref=298.15 상수 오프셋) 정확 대응 ✓. 되먹임 상한 0.47 mV/K×30 K=14.2 mV ≲ w₁(25.7 mV) ✓(L5 반올림 제외).
- **P5 이중계산 가드 (eq:lco-slots L2565–2573·eq:lco-mit L2206–2212)**: gap⇐Ω(J/mol)와 $\partial U/\partial T$⇐ΔS(J/(mol·K))는 다른 슬롯·다른 차원 ✓; config 는 중심 표준값만(혼합항은 w 몫) — Ch2 파생 B 와 문구·부호 일치 ✓; $\partial S_\config/\partial\theta|_{\theta=1-\xi}=+R\ln[\xi/(1-\xi)]$ 부호 전환 재유도 ✓(M3 의 $n_j$ 계수만 예외).
- **P6 eq:lco-decomp (L2575–2580)**: 세 성분 차원 동일 ✓; 분배함수 인수분해→로그 가법→부분몰 가법 사슬 ✓; $S_\mathrm{mix}$ **Part 0 §sec:sm-lattice 귀속(L2262) — R2 정정 유지 확인** ✓.
- **P7 Ch2 eq:dxidT 독립 재유도 (L481–490)**: $a_j=(U-U_j(T))/w_j(T)$ 전미분 → $-g_j\partial U_j/\partial T-g_j(n_jR/F)z_j$, $z_j=(U-U_j)/w_j=\ln[\xi/(1-\xi)]$ ✓. **계수 $n_jR/F$ 4곳 전수 일치**: 본문 L506–507·keybox L715·eq:single_config L564·코드 `entropy_coefficient` L587 (구현식 `(n_j*R/F)*np.log(xi_c/(1-xi_c))`) ✓. eq:dVdT_config "자리당 n_j=1 서식" 한정어(L255) 정합 ✓(전방 참조만 L3). 고정-ξ 경로와 음함수 경로의 단일 전이 극한 합치 ✓. 코드 `entropy_coefficient` vs 수기 완전식 최대차 5.6×10⁻¹⁷ mV/K(비트 수준) ✓.
- **P8 x̄≡1−x 전파 (Ch2)**: 선언 L462–463; L469(고정 x̄=고정 x)·L503–504($Q\partial\bar x/\partial U$)·fig:blend 축 L537·keybox L723–725 — 잔여 누락 없음 ✓(캡션 기호 혼용만 L8).
- **P9 eq:muV+각주 (Ch2 L143–151)**: Ch1 L1985 "$\mu_\mathrm{Li}=\mu^0-sF(V-U)$, $\Delta G_j=-sFU_j$($s{=}+1$)"(L2000)와 자구 일치 ✓; 각주의 여집합 함정 서술 = Ch1 eq:lco-comp 와 동일 물리 ✓; $V\!\uparrow\Rightarrow\mu\!\downarrow\Rightarrow\theta\!\downarrow$ 재유도 ✓. (eq:sm-eqcond 원문은 Part 0 — 담당 범위 밖, Part II 인용부로 삼각.)
- **P10 Bernardi 라벨 층위 (Ch2 L679–708)**: 하프셀 자발 방전 = 흑연 리튬화(양극이 흑연) 재검 ✓; $\Delta S=+F\partial U_\oc/\partial T$ 항등식 ✓; 저-x 리튬화 ΔS>0→흡열, stage 2→1 ΔS=−16→발열 — Bernardi 라벨 내 자기일관 ✓, Ch1 라벨(방전=탈리튬화)과의 충돌은 L690–693 이 명시 분리 ✓. 코드 `reversible_heat`(−I·T·∂U/∂T, T 1회) ✓ `irreversible_heat` lumped ✓.
- **P11 FD 약자 분리**: "Fermi--Dirac--Sommerfeld"(L655·767) vs 유한차분 "$^\mathrm{num}$"(L511, 병기 "finite difference") — 약자 충돌·잔재 0 ✓.
- **P12 수치 전수 재계산**: R1 히스 $u=0.7661$·$\Delta U^\hys=86.69$ mV(주장 0.766/86.7 ✓); $2RT=4957.6$→"4958" ✓; $F\times0.83$ mV/K$=80.08$→"≈+80" ✓; $+80-46\approx+34$ ✓; 30 K→24.9 mV→"≈+25" ✓; $1.1\,k_B$ 재계산 1.1056 ✓; 골 −45.96@300 K→"−46" ✓; $1/\Delta x=20$ ✓; $k_BT/E_F\approx0.03$ ✓; MCMB 29/F=0.30 mV/K ✓; $\Delta H^0=-FU+FT\partial U/\partial T=-12.97$ kJ/mol→"−13.0" ✓; Ch2 BE 모드 엔트로피 eq:Svib_mode $-\partial f_k/\partial T$ 항등 재유도 ✓; Sommerfeld $\int s(\zeta)\dd\zeta=\pi^2/3$ 두 경로 합치 ✓; eq:lco-dope Taylor $(8RT/3F)u^3$ 재전개 ✓; spinodal $\xi(1-\xi)=RT/2\Omega$·대칭 평균=U 재유도 ✓; eq:Veq_BW(θ)↔eq:lco-Veq(ξ) 좌표 변환 합치(★H-1 정정부 무결) ✓; "전이 경계 3곳"(L517·L556) = 4전이−1 ✓; 표시 정밀도 서술(≲10⁻² mV/K vs 수 μV/K) 내적 정합 ✓.
- **P13 직전 수정부 무결**: R1 overfull 분할 eq:lco-plugin(L2720–2728) — 분할 후 사슬 x(ξ)→ΔS_e→U₁→U₁^d→ξ→dQ/dV 등가·화살표 식번호 정확 ✓. hotfix 1(nodemap N0 행 $ 균형 L2809) ✓. hotfix 2(N0′ multicolumn 별도 행 L2822–2823, 4열 스팬) ✓. §중복 해소부: sec:lco-direction↔sec:lco-hys ★분기 부호↔sec:lco-peak ★방향 슬롯 — 재유도 중복 없이 참조 위임 구조 ✓.
- **P14 상호충실도 전수 (문건↔코드)**: GRAPHITE_STAGING_LIT 4×(U/w/Q/Ω/ΔH/ΔS/ΔH_a/dVdq/n/dS_a) = Ch1 표 L1792–1802 전항 일치 ✓; LCO_MSMR_LIT(U 3.930/3.880/4.050·x_MIT 0.85·g_max 13·Δx 0.05·Ω/γ/dH_a 미배정→분기·꼬리 비활성) = Ch1 L1862–1867·L2101–2105·L1913 선언 일치 ✓; tab:inputs 기본값(z_cut 4.357·A_cap 4.0·pad 0.15·2048·2.0·1e-6·seed 298.15/0.1/1.0·h_eta 1.0·Ω,γ=0·dS_a=0·use_dH_eff True) = 생성자·dict get 기본값 전수 일치 ✓; nodemap 코드 식별자 13종 실재 ✓; x-매핑(eq:lco-xmap)·T² 다온도는 "round-trip 단계 과제" 선언(L1865–1867·L2710–2714)과 코드 동결 구현(x_center 상수·T_ref 동결) 정확 대응 — 문건이 코드 상태를 과장 없이 기술 ✓.

---

## C. 가장 약한 1곳

**M1 (Ch2 파생 D L608 의 ± ↔ ch/dis 무명시 대응).** 이 문건군의 1급 방어선(부호 사슬 — Ch1 이 "★최우선 결함 클래스"로 자기 선언)에서 유일하게 부호 배정이 독자 추론에 맡겨진 자리이며, 자연 독해(positional)가 Ch1 eq:Ubranch·eq:lco-sigmaslot 과 반대다. boxed 평균(eq:hys_rev)은 불변이라 잠복성이 높다 — 종형 불변으로 잠복하는 여집합 함정(Ch2 각주)과 동형의 잠복 구조.

## D. 물리 불변 확인

- 평형 종 $\xi(1-\xi)$ 의 여집합($\sigma_d$ 반전) 불변 — 식(eq:lco-comp)·코드(`func_ksi_eq` 안정형)·수치(|I|→0 dis/chg 일치) 3중 확인.
- 면적 보존 $\int(\dd Q/\dd V)^{\eq}_j\dd V=Q_j$, 최대 $Q_j/4w_j$ — eq:lco-peakobs 재유도 일치.
- $\Delta U^\hys\ge0$·$\Omega\le2RT\to0$ 연속(Taylor $u^3$)·분기 중심 $U_j$ 대칭 — 재유도·코드 분기 일치.
- $\Delta S_e<0$(삽입 기준)·$\propto T$·게이트 적분 $=S_e$(metal 끝점) 항등 — 부호·크기·차원 3중 검산 통과.
- 동결 구현의 $U(T)$ 선형성·세 산출 경로(equilibrium/dqdv/entropy_coefficient)의 seam 단일화 — 코드 구조 확인.

## E. Coverage 선언

- **Ch1**: L1790–2912 전 줄 정독(담당 공식 시점 L1810 이전 L1790–1809 는 경계 문맥으로 포함 — L2 는 경계 지적으로 명기). 재유도한 번호식/boxed 식 전수: eq:lco-sigmaslot·lco-n0sub·lco-dUdT(2경로)·lco-J·lco-gxi·lco-gpp·lco-spinodal·lco-Veq·(ΔU_hys 무번호 유도·대칭 평균)·lco-dUhys·lco-Ubranch·(T2/T3·T1 대입 무번호)·lco-mit·lco-dope·fd·Se·Sedirect·dSe·dSemolar·gunit·U1T2·ggate·dSegate·lco-charge·lco-belliden·lco-peakobs·lco-eqpeak·lco-Zfact·lco-Sadd·lco-configsplit·lco-slots·lco-decomp·msmr·lco-msmrnorm·lco-comp·lco-msmrmap·lco-msmrpeak·lco-xmap·lco-SeV·lco-U1V·lco-plugin + 표 3종(tab:lco-staging·tab:inputs·tab:nodemap) + 그림 2종 TikZ 좌표 검산(fig:lco-dirmap·fig:lco-electronic) + signcheck S1–S8·R1–R5. 미검증 잔여: Part I/Part 0 식 라벨 실체(eq:center·eq:vwork 등 — 범위 밖, 참조 일관성만 확인)·문헌 인용값 원문(tier 병기 존중).
- **Ch2**: L1–793 전 줄 정독. 재유도: 서 boxed 사슬·Z1·occ·muV·logistic·Vxi·BW·Veq_BW·slope_BW·Sconfig·dSconfig·dVdT_config·Svib_mode·Se·implicit·implicit_diff·gj·dxidT·weighted·single_config·hys_branch·hys_rev·qrev·종합식 keybox + 표 2종·그림 2종(fig:occ_config 곡선 수식 검산·fig:blend) + 극한 6코너.
- **코드**: L1–881 전 줄 정독. 대조 함수/데이터 전수(P14 목록) + 독립 실행 재현(스크래치패드, 원본 무수정): dSe −45.678262·LCO U(298) 3건·흑연 U(298) 4건·FD vs 단순/완전(3개 그리드×175점)·entropy_coefficient 비트 대조·hys 86.69 mV·curve 라벨 환산 0-diff.
- **재계산 수치 전수 목록**: −45.6783·−391017.4/−375555.7/−391360.0(역산 포함)·3.930/3.880/4.050·0.210/0.140/0.120/0.085·86.7 mV·0.766·4958·+80·+34·+25 mV·1.1 k_B·−46·0.48(→0.47)·14 mV·20배·0.03·0.30 mV/K·−13.0 kJ/mol·0.18/0.21/0.14(스팬 의존 확인)·10⁻² mV/K·3곳·(8RT/3F)u³·4×10³⁷.

## F. 5줄 요약 (오적발 자기표시)

1. 치명(부호·물리 붕괴)급 결함 0 — 담당 전 식 재유도 일치, FD≡완전식 등 핵심 수치 주장 독립 재현 PASS.
2. [MEDIUM] 3건: 파생 D ±↔ch/dis 무명시(Ch1 과 역독해 허용, ★가장 약한 1곳)·fig:lco-electronic 라벨 3건(축 화살표 ← 오류 확정 — 소스 주석과 모순)·Ch1 configsplit $n_j$ 미전파(R2 대칭 자리).
3. [LOW] 9건: LCO ΔH 가 F=96485.332 역산(코드 F 와 +13 μV — **재계산으로 기원 확정, 추정 아님**)·흑연 4→3 U(298)=0.211(경계)·전방 참조·검증 그리드 스팬 미명시·0.48/등호점/용어병기/fig:blend 방향/단위 접미.
4. 오적발 주의 자기표시: 파생 A 재현의 극값 차이는 그리드 스팬 의존임을 확인했으므로 문건 [−0.21,+0.14] 자체를 오류로 단정하지 않음(L4 는 재현성 명시 요구); Ch1 L1838 "방전(σ_d=+1)=LCO 리튬화"는 L1916 층위 구분으로 이미 해소된 사안이라 지적하지 않음; 내 검증 스크립트의 초기 bisection 버그(첫 실행 181 mV/K)는 내 오류로 식별·수정 후 재실행함.
5. 수정 우선순위 제안: M1 → M2(i) → M3 → L1·L2 (나머지는 편집 라운드 일괄).
