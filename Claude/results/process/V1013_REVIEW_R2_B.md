# V1013 REVIEW — Round 2, 검수자 B (청크 스킴: 절 단위)

- **대상**: `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` — **Ch1 Part II 전체(L1809 sec:lco-intro ~ sec:lco-code L2733) + 전체 입력 인자(L2735–)·facade(L2790–)·signcheck(L2830–EOF L2910)**
- **★렌즈 ⑧ 최우선**: R1 수정 8개 지점의 새 결함(지정 목록 전건 판정 — 하단 §⑧ 판정표) + 압축 적용부 p1(lco-center·lco-hys)·p2(lco-electronic·lco-peak)·p3(lco-decomp·lco-code·signcheck·dist)의 문장 병합 비약·문법 잔결함 스캔.
- **검증 보조**: `Anode_Fit_v1.0.13.py`(생성자·curve·seam·LCO 클래스·`__main__` 표적 정독), Ch2 파생 B 존재 grep, 컴파일 log(2026-07-03 03:41 — tex 최종 수정 직후) 참조 무결 확인.
- **원칙**: refute mandate — 유도 재유도·수치 재계산·코드 원문 대조. 지적만, tex/코드 수정 0건.

---

## 지적 사항 (등급순)

### [HIGH-1] L2034 — eq:lco-decomp→§ 강등이 만든 **중복 참조 렌더 훼손** (렌즈 ⑧ 직격)
- **원문**: "$\Delta S_{\rxn,j}^\mathrm{cat}$ 는 `\S\ref{sec:lco-decomp}(\S\ref{sec:lco-decomp} 의 분해식)에서` config$\cdot$vib$\cdot$전자 세 성분으로 분해된다."
- **무엇이**: 같은 절 참조가 괄호 밖·안에 이중으로 찍혀 PDF 에 "§X.X(§X.X 의 분해식)에서"로 렌더된다 — 원문의 "식~\eqref{eq:lco-decomp}" 강등 시 괄호 안만 바꿔야 할 것을 본문·괄호 양쪽에 치환한 잔재.
- **수정안**: "\S\ref{sec:lco-decomp} 의 분해식에서 config$\cdot$vib$\cdot$전자 세 성분으로 분해된다." (괄호 삭제)

### [HIGH-2] L2045–2046 — 같은 강등 계열의 **"§ 의 § 의" 중복** (렌즈 ⑧ 직격)
- **원문**: "전자항 $\propto T'$ 를 실제 적분한 닫힌 특수형이 `\S\ref{sec:lco-Se} 의` ⏎ `\S\ref{sec:lco-Se} 의 $T^2$ 곡률식($\tfrac12(T^2-T_\mathrm{ref}^2)$ 곡률)다.`"
- **무엇이**: "…특수형이 §Y 의 §Y 의 $T^2$ 곡률식…다"로 렌더 — eq:U1T2 전방 참조(R1 C-08(a)) 강등 시 행 걸침 이중 삽입.
- **수정안**: "…닫힌 특수형이 \S\ref{sec:lco-Se} 의 $T^2$ 곡률식($\tfrac12(T^2-T_\mathrm{ref}^2)$)이다." (한쪽 삭제; 겸사 "곡률식(…곡률)" 중복도 정리)

### [HIGH-3] L2375–2376 — 부호 주석의 기호 오기: $\partial\sigma/\partial x$ 는 **양수**인데 "$<0$" 로 주석 (★부호 1급 클래스, prose) — ★가장 약한 1곳
- **원문**: "식~\eqref{eq:dSe} 에 넣으면 삽입 기준 $\Delta S_e(x)\propto\partial\sigma/\partial x<0$(탈리튬화 방출 $|\Delta S_e|\propto-\partial\sigma/\partial x>0$)가 MIT 부근의 국소 골…"
- **근거(재유도)**: 게이트 정의(식 eq:ggate, L2370)는 $\sigma\!\big((x-x_\mathrm{MIT})/\Delta x_\mathrm{MIT}\big)$ — $x$ 의 **증가함수**라 $\partial\sigma/\partial x=\sigma'/\Delta x_\mathrm{MIT}>0$ 이고, 음이 되는 것은 $g=g_{\max}[1-\sigma]$ 의 미분 $\partial g/\partial x=-\tfrac{g_{\max}}{\Delta x_\mathrm{MIT}}\sigma(1-\sigma)<0$ 쪽이다. 곧 문면의 두 부등호 주석("$\partial\sigma/\partial x<0$"·"$-\partial\sigma/\partial x>0$")은 표기된 도함수에 대해 **둘 다 거짓**이며, 같은 문서의 정확한 서술 — L2381–2382 "$\partial g/\partial x=-\frac{g_{\max}}{\Delta x_\mathrm{MIT}}\sigma(1-\sigma)<0$", 그림 캡션 L2454 "$|\Delta S_e|\propto-\partial g/\partial x>0$", L2342 "파선이 이 양의 방출량 $-\partial g/\partial x$" — 와 문서 내 충돌한다. $\sigma$ 가 있어야 할 자리에 $g$ 가(정확히는 그 반대로) 뒤바뀐 오기.
- **하류 안전성**: display·박스 식(eq:dSe·eq:dSegate·eq:dSemolar·eq:lco-SeV)과 코드(`func_dSe_molar` L188, leading `−`)는 전건 정합 — 훼손은 이 prose 한 문장뿐.
- **오적발 자기표시**: "∝ 를 음의 비례상수 포함으로 읽으면 첫 절은 구제 가능"하나, 그 읽기로는 둘째 절($|\Delta S_e|\propto-\partial\sigma/\partial x$)이 다시 음의 상수를 요구해 한 문장 안에서 규약이 뒤집힌다 — 어느 고정 규약으로도 두 절이 동시에 성립하지 않아 유지.
- **수정안**: "$\Delta S_e(x)\propto\partial g/\partial x<0$(탈리튬화 방출 $|\Delta S_e|\propto-\partial g/\partial x>0$)".

### [MED-4] L2060–2061·L2322 — 강등 문안의 이중 속격 "…의 분해식 의 …" (렌즈 ⑧, 문법)
- **원문(2곳)**: L2060–2061 "표~\ref{tab:lco-staging}$\cdot$\S\ref{sec:lco-decomp} 의 분해식 ⏎ 의 초기값을 데이터로 피팅해" / L2322 "가 \S\ref{sec:lco-decomp} 의 분해식 의 $\Delta S_{e,j}$ 자리에 들어가는".
- **무엇이**: "§X **의** 분해식 **의** Y" — 속격 조사가 연쇄되고 둘째 "의"가 개행으로 앞말과 띄어져("분해식 의") 조사 띄어쓰기 오류로 렌더된다. eq 참조("식~\eqref{…} 의 Y")를 기계 치환한 잔재.
- **수정안**: "…\S\ref{sec:lco-decomp} 분해식의 초기값을…" / "…\S\ref{sec:lco-decomp} 분해식의 $\Delta S_{e,j}$ 자리에…".

### [MED-5] L2261 — "$\S$\ref{sec:hys} 의 $S_\mathrm{mix}$" — 소재 오귀속 (G-follow)
- **원문**: "($-k_B\sum[f\ln f+(1-f)\ln(1-f)]$, 식~\eqref{eq:fd} 를 자리당 점유로 본 \S\ref{sec:hys} 의 $S_\mathrm{mix}$ 와 같은 꼴)"
- **근거**: $S_\mathrm{mix}$ 의 정의는 Part 0 \S sm-lattice 의 식 eq:sm-Smix(L466)이고, 기호 $S_\mathrm{mix}$ 는 문서 전체에서 L466·469·488·515·785·793(전부 Part 0)과 이 자리에만 등장한다(전수 grep) — \S hys(N3) 본문엔 없다. 독자를 \S hys 로 보내면 못 찾는다.
- **수정안**: "…\S\ref{sec:sm-lattice} 의 $S_\mathrm{mix}$(식~\eqref{eq:sm-Smix}) 와 같은 꼴". (동계열 관찰 — L2074 "\S\ref{sec:hys} 의 …식~\eqref{eq:mu} 와 …식~\eqref{eq:gxi}"도 두 라벨의 정의는 Part 0 \S sm-mf 다; 다만 \S hys 가 그 식들의 회수·적용처라 절반은 방어 가능 — 하향 관찰로만 기록.)

### [MED-6] L2095–2096 ↔ L2100–2101 — '초기값' 이중 의미 충돌이 **같은 문단 안에** 잔존 (R1 C-16 수정의 적용 누락 — 렌즈 ⑧ 인접)
- **원문**: L2095–2097 "LCO 는 **pure-LCO 초기값에서** T1(MIT)$\cdot$T2$\cdot$T3 세 전이 전부가 같은 문턱 $\Omega_j^\mathrm{cat}>2RT$ 를 넘는 상분리 후보다" ↔ 4줄 뒤 L2100–2101 "표~\ref{tab:lco-staging} 는 LCO $\Omega_j^\mathrm{cat}$ 의 수치 열을 싣지 않으며(흑연 표~\ref{tab:staging} 와 달리 **초기값 미배정**)".
- **근거**: 같은 단어 '초기값'이 4줄 간격으로 "문헌 물리 기대"와 "수치 기본값" 두 층위로 쓰여 "미배정인데 $>2RT$?"의 오독 경로가 열린다 — R1 C-16 이 지적한 바로 그 충돌이며, 수정은 L2517("pure-LCO **문헌 물리에서**")에만 적용되고 이 문단(원지적의 L2093–2095 짝)은 남았다.
- **수정안**: L2095 "pure-LCO 초기값에서" → "pure-LCO 문헌 물리에서" (L2517 과 동일 어휘로 통일).

### [MED-7] tab:nodemap LCO 4행(L2820–2824) — 코드 식별자 열이 실재 식별자를 안 씀 (렌즈 ⑥)
- **무엇이**: N5$+$ 행의 식별자 열 = "$\Delta S_e$ plug-in(전자항)", N9$'$ 행 = "MSMR 동형 \eqref{eq:msmr}"(코드 식별자가 아님). 실제 코드에는 `func_dSe_molar`(py L173)·seam `_effective_dS_rxn`(py L545/L684)·`LCOCathodeDQDV`(py L658)가 실재한다.
- **근거**: 표의 선언된 목적이 "노드 $\leftrightarrow$ 식 $\leftrightarrow$ 코드 식별자 매핑"이고 흑연 N0–N9 행은 전부 실식별자를 적는다 — LCO 행만 관념 라벨로 느슨해 상호충실도 표가 반쪽이다. (R1 C-04 의 "N0$'$ 행에 전극 인지 플래그 반영 권장"도 미적용 — facade 본문 문장으로만 반영됨.)
- **수정안**: N5$+$ 식별자 열 → "\code{func\_dSe\_molar}, seam \code{\_effective\_dS\_rxn}"; N9$'$ → "\code{LCOCathodeDQDV}(\code{\_delith\_is\_discharge}$=$False)" 류.

### [LOW-8] L2343 — "분해식(\S\ref{sec:lco-decomp} 분해식)이" — 괄호 안 '분해식' 중복 (렌즈 ⑧). → "분해식(\S\ref{sec:lco-decomp})이".

### [LOW-9] L2329–2331 — 신설 게이트 기호 예고 괄호(⑧ 지정)의 표기: "게이트 파라미터 $g_{\max}\cdot x_\mathrm{MIT}\cdot\Delta x_\mathrm{MIT}$" — 수식 모드 $\cdot$ 나열이 세 파라미터의 **곱**으로 읽힌다. 문서 관례는 튜플 "$(g_{\max},x_\mathrm{MIT},\Delta x_\mathrm{MIT})$"(L2374·L2728). → 쉼표 튜플로.

### [LOW-10] L2605 — "(구현식은 \S\ref{sec:lco-code} 식~\eqref{eq:lco-xmap})" — eq:lco-xmap 정의(L2683–2685)보다 앞선 수식 라벨 전방 참조(렌즈 ③ 규약 위반; 절 참조 병기로 완화돼 있어 LOW). → "(구현식은 \S\ref{sec:lco-code})"로 충분.

### [LOW-11] L1374 — broadening ③ 소절 heading 의 scope 라벨 반 층위 과잉 (⑧ 지정 항목의 잔여)
- **무엇이**: heading "③ 집합 다입자 통계역학(앙상블 몫) — 흑연 두-상($\mathrm{LiC_{12}}\cdot\mathrm{LiC_6}$)에 한함" 인데, 본문 L1378–1379·keybox L1455–1456 은 "LCO 는 일반 $\eta$ 분포(iii-b)로만 다룬다" — iii-b 는 ③ 의 하위 층이라 heading 의 무조건 "한함"이 본문과 반 층위 어긋난다(keybox·캡션의 새 문안 "흑연-특정 구조 무질서 **근거**는 흑연 두-상 한정"은 정확 — R1 HIGH-1 의 본 모순은 해소됨).
- **수정안**: heading → "③ 집합 다입자 통계역학(앙상블 몫) — 구조 무질서 근거는 흑연 두-상 한정".

### [LOW-12] L2599 — "(갭 G1$\cdot$G2$\cdot$G4)" — G2 만 정의(L2300 "G$n$ 은 …일련번호")되고 G1$\cdot$G4 는(그리고 G3 도) 본문 어디에도 개별 도입이 없다 — 고아 일련번호. → 이 자리에서 대응을 풀어 "(연속 $\Delta S(x)$=G1, $g(E_F,x)$=G2, 도핑 shift=G4)"로 명시하거나 G-목록 각주 신설.

### [LOW-13] L2582·L2587 — "★이중계산 금지(B)" 의 태그 "(B)" 가 Ch1 안에서 무정의 — 실체는 Ch2 파생 B(Ch2 L558 subsection; 코드 docstring py L563 "Ch2 파생 B" 명시)로 확인되나 Ch1 단독 독자에게 고아 라벨. → "★이중계산 금지(Ch2 파생 B)" 병기.

### [LOW-14] L2253–2259 — p2 압축부 문법: 미완결 연결어미
- **원문**: "…LCO 의 전도 전자도 에너지 준위 $E$ 를 Fermi--Dirac 분포로 **점유하며**($E_F$=Fermi 준위): [식 eq:fd] **입자 0/1 배타 점유라는 구조가** …같다"
- **무엇이**: "-하며"가 display 식 뒤로 이어지지 않고 새 문장이 시작돼 첫 문장이 미완결로 끊긴다(병합·재배치 잔재). → "점유한다($E_F$=Fermi 준위):".

### [LOW-15] L2303–2306 — p2 압축부 주술 호응: "forward 모델이 …쓰는 **양은** 삽입 반응 엔트로피로 — 흑연의 …round-trip 으로 맞추는 바로 그 **슬롯(…)이며**" — 주어 '양'이 술어 '슬롯이며'와 호응하지 않는다(양$\ne$슬롯). → "…쓰는 **자리는** …바로 그 슬롯이며" 또는 "쓰는 양은 삽입 반응 엔트로피다 — 그 슬롯은 …".

### [LOW-16] L2728–2729 — 술어 미완 명사문: "$g(E_F,x)$ 는 식~\eqref{eq:ggate} 의 게이트로, 초기값 3개$(\dots)$ 를 피팅 인자로 **노출.**" — enumerate 항목 말미가 동사 없이 끊김(p3 압축 잔재). → "노출한다."

### [LOW-17] L2337 — "reynier\cite{reynier2004} 의 O3 총 부분몰" — 저자명 소문자(타처 L2594 "Reynier"). → 대문자.

### [LOW-18] Motohashi tier C 하향 괄호(⑧ 지정)의 잔여 2건 — 괄호 자체(L2185–2187)는 내용 정확·문장 흐름 유지(PASS)이나:
  (i) **표-본문 비대칭**: tab:lco-staging T3 행(L1874)의 "config($\approx$1.49 J/K\,mol)"에는 하향 표시가 없다 — 표만 읽는 독자는 그 슬롯 배정이 tier C 로 내려간 것을 모른다. → 표 각주 포인터 또는 "†(배정 tier C, \S\ref{sec:lco-hys})" 반영.
  (ii) **경계 기준 미명시**: 0.47 anchor 의 $x{=}\tfrac12$ 도 T2 창($x\approx0.55$) 밖(0.05 이탈)인데 하향은 $x{=}\tfrac23$(0.11+ 이탈)만 — 어느 이탈부터 하향인지 기준이 없다. 부수: 표 단위 "J/K\,mol" vs 본문 "J/(mol\,K)" 표기 혼재.

### [NOTE-19] L2169 — "(T2$\cdot$T3) order--disorder(OD)" 재병기 잔존(첫 병기는 이동된 L2082 — ⑧ 지정 항목 자체는 PASS). 무해 중복이나 첫-출현-병기 원칙상 L2169 는 "OD"만으로 족하다. (동류: MSMR 병기가 L1844–1845·L1968–1969·L2612–2613 세 번.)

### [NOTE-20] 용어 '방출' (L2335·L2341–2342·캡션 L2454–2455) — 탈리튬화 시 전극 전자계 엔트로피는 $0\to1.1\,k_B$/atom 으로 **증가**하는데 이를 일관되게 "방출되는 전자 엔트로피"로 부른다. 수식·부호·적분 항등은 전건 정합하나, '방출'은 열 언어(발열)와 연상 충돌해 Ch2 가역열($\Delta S>0$ 방전 흡열) 독해와 이어 읽을 때 오독 여지 — "켜지는/드러나는 전자 엔트로피" 계열 검토 권장. 순수 용어 관찰(물리 훼손 아님).

### [NOTE-21] $g_{\max}$ 단위 표기 혼재 — "e/eV/atom"(L2298·L2366) vs "e/eV"(eq:ggate 박스 L2371·L2398·캡션 L2453). 자리당 정규화 병기 통일 권장.

### [NOTE-22] L1912–1913 — "(…세 작용처 중 실질 활성이 분극뿐임은 \S\ref{sec:lco-hys} 의 two-phase calibration 지위 그대로다)" — 해당 문단(L2099–2102)은 $\Omega$ 미배정$\to$분기 비활성만 다루고 **꼬리**(동역학 키 미배정) 비활성은 다루지 않는다 — 포인터가 3 작용처 중 2/3 만 커버(코드 docstring py L667–668 은 "Omega·dH_a 미배정으로 분기·꼬리 비활성" 완전 서술). 반 문장 보강 여지.

### [관찰 — R1 지적의 미적용 잔존 확인 (재론 아님, 회귀 추적 기록)]
- fig:logistic 파선 좌표 표류(R1 B MED-5): 현행 L1286 좌표 그대로 — 재검산 결과 동일($z{=}0$ 에서 $9\times$, $z{=}1$ 9.14, $z{=}2$ 9.49, $z{=}3$ 10.04, $z{=}4$ 11.95$\times$ — 상수배 아님). 마스터 보류 판단이면 무시.
- R1 C-18(fig:lco-electronic 캡션의 $0.18\,k_B$ 병치) 현행 L2457 유지 — NOTE 급 보류로 간주.

---

## ⑧ 지정 항목 판정표 (R1 수정 지점 전건)

| # | 지정 항목 | 판정 | 근거 |
|---|---|---|---|
| 1 | tab:lco-staging 캡션 현행화(L1858–1866) | **PASS** | 코드 py L636–655 대조: $U{=}3.930/3.880/4.050$ ✓, T1 dict `electronic:True`·`x_MIT:0.85`·`g_max_eV:13.0`·`dx_MIT:0.05` ✓, "v1.0.13 재정렬 완료" ✓(py L640–641 루프 B 주석), $T_\mathrm{ref}$ 동결 상수 오프셋 ✓(py L688–698), $T^2$ 곡률 § 참조 강등 ✓. 문안·문법 결함 없음 |
| 2 | Motohashi tier C 하향 괄호(L2184–2187) | PASS(본문) / 잔여 **LOW-18** | 값 tier A 유지 + $x{=}\tfrac23$ 슬롯 배정만 tier C — 내용 정확, 주술 호응 유지. 표 미반영·경계 기준 미명시 잔여 |
| 3 | OD 병기 위치 | **PASS** / NOTE-19 | 첫 출현 = eq:lco-J(L2079), 병기 직후 L2082 "(OD $=$ order--disorder)" ✓; L2169 재병기 중복만 잔존 |
| 4 | eq:lco-decomp→§ 강등 6곳 | **FAIL 4곳** | 전방 eq 참조 자체는 0 으로 소거 ✓(전 참조 L2586·2605·2697·2824 = 정의 후). 그러나 강등 문안이 **HIGH-1**(L2034 중복)·**HIGH-2**(L2045–2046 중복, eq:U1T2 계열)·**MED-4**(L2060·L2322 이중 속격)·**LOW-8**(L2343 중복) 유발 |
| 5 | facade 전극 인지 신설 문장(L2792–2795) | **PASS** | py L530–535(`sigma_d = -sigma_d` when `not _delith_is_discharge`)·L682(`False`)·L672("저수준 dqdv(s=...) 물리 부호 직접")·L542(`dqdv(..., s=sigma_d)` 시그니처) 전건 일치. 'charge'$\mapsto$`_direction_to_sigma`$=-1\to$flip$\to+1$ ✓ |
| 6 | self-test R1–R5 재서술(L2857–2859) | **PASS** | `__main__` 대조: R1=py L813–822($\Omega{=}12000,\gamma{=}1$) ✓·R2=py L835–836($\Omega{=}2RT$) ✓·R3=py L838–841($\gamma{=}0$, $|I|{=}10^{-6}$) ✓ — "R1–R3 은 같은 양의 수기 재산출, R4 컷 규칙 정의 검사, R5 극한 논증" 이 실물과 정확히 대응; "다섯 항"(L2858)↔"다섯 회귀 항"(L2881) 수사 정합(R1 C-05 해소) |
| 7 | 게이트 기호 예고 괄호(L2330–2331) | PASS(내용) / **LOW-9**(표기) | "정의는 다음 소절 \S lco-gate 가 닫는다 — 여기서는 닫힌꼴 예고" — C-08(c) 해소 ✓; 괄호 안 $\cdot$ 나열 표기만 결함 |
| 8 | broadening scope 문안(keybox L1454–1456·캡션 L1494–1495) | PASS(본 모순 해소) / **LOW-11**(heading) | "흑연-특정 구조 무질서 **근거**는 흑연 두-상 한정 — LCO 는 일반 $\eta$ 산포로만" — eq:ensavg 를 흑연 전용이라 하던 R1 모순 소거 ✓; ③ heading 의 "한함"만 반 층위 잔존 |

---

## 재유도·검산 통과 기록 (오적발 방지용 명시)

1. **몰당 게이트 골 수치 사슬**: $-\tfrac{\pi^2}{3}R\,\tfrac{k_BT}{e_V}\,\tfrac{g_{\max}}{\Delta x_\mathrm{MIT}}\cdot\tfrac14$ = $3.2899{\times}8.314{\times}0.02585{\times}260{\times}0.25=45.96$ → $-46$ J/(mol K)@300 K ✓(L2065·L2427); 298.15 K 재계산 $-45.68$ ✓ = 코드 주석 $-45.678$(py L638)·docstring $-45.7$(py L182). $+80-46\approx+34>0$ ✓; $0.83$ mV/K${\times}F=80.1$ ✓; 30 K 창 $+25$ mV ✓; 되먹임 $46/F{\times}30\,\mathrm K=14.3$ mV ✓(L2716–2717).
2. **LCO_MSMR_LIT $U(298)$ 역산(seam 포함)**: T1 $(391017.4+298.15\times(6.0-45.68))/96485=3.9300$ ✓(전자항 흡수 재보정 주석 py L638–639 정합), dict2 $(375555.7-1192.6)/96485=3.8800$ ✓, dict3 $(391360.0-596.3)/96485=4.0500$ ✓ — 캡션 시연값 3건 전건 재현.
3. **Sommerfeld 이중 경로**: $C_e=\tfrac{\pi^2}{3}k_B^2Tg(E_F)$ ✓, $S_e=\int C_e/T'\dd T'$ ✓; 직접 경로 $\int s(\zeta)\dd\zeta=\pi^2/3$ ✓ → eq:Se$\equiv$eq:Sedirect ✓. 끝점 $S_e/k_B=3.29{\times}0.0259{\times}13=1.11$ ✓; 게이트 적분 방출$=g_{\max}$ 전 스윙과 항등 ✓; $1/e_V^2\approx3.9{\times}10^{37}$ ✓; eq:U1T2 적분 $\tfrac12$ 인자 ✓(음의 곡률→고온 외삽 하향 ✓).
4. **정규용액 대입형**: eq:lco-gpp·lco-spinodal·lco-Veq·$\Delta U^{\hys,\mathrm{cat}}$·대칭 평균$=U_j^\mathrm{cat}$·Taylor $\tfrac{8RT}{3F}u^3$ 전건 흑연식과 대수 동일 재유도 ✓. self-test R1 수치 $u=\sqrt{1-4958.4/12000}=0.766$, $\Delta U^\hys=2[12000{\times}0.766-4958.4{\times}1.0107]/F=86.7$ mV ✓.
5. **MSMR 사전**: eq:msmr→eq:lco-msmrnorm 나눗셈 ✓; eq:lco-comp 여집합 항등식 재유도 ✓; 진행률↔진행률·점유↔점유 두 pairing 모두 $f=+\sigma_d$ 유일해 ✓, 직접 등치 시 $f=-\sigma_d$ 서술 ✓; eq:lco-msmrpeak $|f|=1$·$\theta(1-\theta)=\xi(1-\xi)$ ✓.
6. **eq:lco-xmap**: $\xi{=}0\mapsto0.94$, $\xi{=}1\mapsto0.75$, $x_\mathrm{MIT}{=}0.85$ 창 내부 ✓; 고정점 구조 서술 ✓(현행 동결 구현은 무순환 — 코드 `x_center` 상수 평가 py L698 정합).
7. **tab:inputs 전 행**: 생성자(py L250–260) 대조 — `x` 0.5·`Rn` 0·`Cbg` 0·`chi` None→x·`chi_split` `func_chi_d`·`use_dH_eff` True·`z_cut` 4.357·`A_cap_RT` 4.0·`grid_pad` 0.15/0.15·`n_work_min` 2048·`min_lag_grid_steps` 2.0·`v_span_floor` 1e-6·`seed` 298.15/0.1/1.0 — 전건 일치 ✓; per-transition override(z_cut) 실증 테스트 py L863–875 존재 ✓.
8. **facade·equilibrium**: `curve`→`dqdv(V_app,T,I_use,Q_cell,s=σ_d)` ✓(py L542); `equilibrium` 은 $U_j$(분기 중심 아님)·$\sigma_d$ 무인자 — "충방전 불변·히스 미반영" 서술 ✓(py L379–396). keybox 6단계(L2781–2787)의 라벨 사슬·분기 문턱 $\nu{=}2$ ✓.
9. **signcheck S1–S8·R1–R5**: 전 항 재확인 ✓ — S6/R4 의 "동결 vs 부등식" 정합 서술 일관, R5 의 $0/0$ 비환원·분기 스위치 논증 재유도 ✓(연속 항등식 $(\xi_\eq-\xi_\mathrm{lag})/L_V=\dd\xi_\mathrm{lag}/\dd V$).
10. **구조**: 컴파일 log(문서 최종 수정 03:41:02 직후 03:41:26) 에 undefined/multiply-defined reference 0건(폰트 경고만) — 청크 내 전 \ref/\eqref 해소 확인. '천이' 잔재 0건 ✓. fig:lco-dirmap 노드-캡션 정합(방전/충전↦$\pm1$ 음영 slotP 배치) ✓.

---

## 말미 종합

**가장 약한 1곳**: **[HIGH-3] L2375–2376** — ★부호 1급 클래스(전자항 부호 규약)의 본문 한가운데서 도함수 기호가 $g\to\sigma$ 로 뒤바뀌어, 문면을 그대로 따라가는 독자가 "$\partial\sigma/\partial x<0$"라는 거짓 부등식을 얻는 유일한 자리. 같은 문서의 박스식·캡션·코드와 정면 충돌하므로 한 줄 치환으로 닫힌다.

**물리 불변 확인**: **PASS** — $f=+\sigma_d$(pairing 유일해, L2646–2655 재유도) · $\Delta\mu=+sF(V-U)$(L1248) · eq:lco-sigmaslot 방향 규약(코드 `_delith_is_discharge` 구현 일치) · 삽입 기준 $\Delta S_{e}<0$ 의 **모든 display·박스 식**(eq:dSe·dSegate·dSemolar·lco-SeV) · H-1 계열(eq:lco-Veq) · 이중계산 가드(eq:lco-mit·eq:lco-slots·$w_j$↔config 분포항) · signcheck S1–S8 전건 위반 0. HIGH-3 은 prose 부등호 주석의 기호 오기이지 박스식 훼손이 아님.

**Coverage 선언**: 담당 청크 **Ch1 L1800–2910(EOF) 연속 전문 정독**(할당 L1809–EOF + 경계 L1800–1808; Part II 도입 3소절·이동 6절·전체 입력 인자·facade·signcheck·참고문헌 포함, 생략 없음). ⑧·압축 스캔 표적 정독(청크 외): L1360–1500(broadening ③·keybox·fig:broadening — scope 문안 + R1 MED-5 좌표 재검산), L1236–1298(sec:dist p3-④ 압축부 + fig:logistic — 병합문 이상 없음, 좌표 표류 잔존 확인). grep 전수: sec:lco-decomp(9곳)·sec:lco-Se(6곳)·eq:lco-decomp/eq:U1T2(전방 참조 0)·OD·천이(0)·$S_\mathrm{mix}$(7곳)·갭 G$n$·"(B)". 코드 `Anode_Fit_v1.0.13.py`: L160–299·L379–397·L505–714·L743–879 정독(렌즈 ⑥ 필요 범위 — 전문 통독 아님). Ch2: 파생 B 존재 확인 grep 만(타 검수자 소관). 미정독: Ch1 L1–1235·L1501–1799 상세 본문(타 청크 소관 — 인터페이스 기호는 grep·R1 기록으로 대조).

**5줄 요약**:
1. ⑧ 지정 8항목 중 5건 PASS(캡션 현행화·OD 병기·facade 전극 인지·self-test 재서술·게이트 예고 — 코드 원문 대조까지 전건 일치), 1건 부분(PASS+잔여 LOW: Motohashi·broadening), **1계열 FAIL: eq:lco-decomp/U1T2 → § 강등이 중복 참조 2곳(HIGH-1·2)·이중 속격 2곳(MED-4)·괄호 중복 1곳(LOW-8)을 새로 만들었다** — 기계 치환의 문맥 미확인이 뿌리.
2. 신규 최대 결함 = HIGH-3(L2375–2376): 게이트 부호 문장에서 $\partial g/\partial x$ 가 $\partial\sigma/\partial x$ 로 오기돼 두 부등호 주석이 문면상 거짓 — ★부호 1급 prose, display 식·코드는 무훼손.
3. 압축부(p1·p2·p3) 스캔: 병합 비약은 없고 문법 잔결함 3건(미완결 연결어미 L2253·주술 호응 L2303·술어 미완 L2728)만 — 전부 LOW.
4. 상호충실도 강함: LCO_MSMR_LIT $U(298)$ 3건 seam 포함 역산 재현·게이트 골 $-45.68$ 코드-문건 수치 일치·tab:inputs 전 행 생성자 일치; 남은 갭은 tab:nodemap LCO 행의 식별자 미기재(MED-7)뿐.
5. 오적발 자기표시 — HIGH-3 은 "음의 비례상수 ∝" 독법으로 첫 절만은 구제 가능하나 둘째 절과 동시 성립 불가라 유지; MED-7 은 완결성 판단(표 목적 해석에 의존); NOTE-20 '방출'은 용어 취향 여지가 커 NOTE 로 한정; fig:logistic 좌표는 R1 기지적의 잔존 확인이지 신규 지적이 아니다.
