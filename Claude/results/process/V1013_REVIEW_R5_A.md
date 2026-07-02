# V1.0.13 P5 검수 라운드 5 — 검수자 A (참조·라벨 단위 청크 스킴)

- 대상: `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` 전문 2,936줄 (전 구간 정독: 1–440 / 440–860 / 860–1280 / 1280–1700 / 1700–2120 / 2120–2539 / 2539–2936)
- 교차 대상: `graphite_ica_ch2_v1.0.13.tex` L100–260 (Ch1 이 문자열로 언급하는 라벨 4건 원문 대조)
- 방법: ① 스크래치패드 파이썬 스크립트(`ref_audit.py`)로 전 `\label` 정의·전 `\eqref/\ref/\pageref` 사용·`\cite`/`\bibitem` 기계 추출(주석 제거 후) → dangling/orphan/중복/전방참조 전수 목록화 ② 전문 정독하며 각 참조 사용처의 서술 ↔ 대상 원문 의미 대조 ③ Ch2 문자열 라벨·서지 전수 대조 ④ 전방 참조 최종 스윕 ⑤ 렌즈 ⑧(R4 수정분 참조 5항목) 개별 재검
- 규율: 검수 의견만 — tex/코드 무수정. 모든 지적에 줄 번호·원문 인용 병기.

---

## A. 기계 감사 결과 (스크립트 전수)

| 항목 | 값 |
|---|---|
| Ch1 `\label` 정의 | 163개 (중복 정의 **0**) |
| Ch1 `\eqref`/`\ref`/`\pageref` 사용 | **536건** |
| dangling(정의 없는 참조) | **0** (`\pageref{LastPage}` 1건은 `lastpage` 패키지 제공 — L68 로드 확인, 정상) |
| orphan(참조 0 라벨) | 23개 (하단 F. coverage 참조 — 결함 아님, 목록 보고) |
| `\cite` 키 | 20종(사용 37회) — `\bibitem` 20건과 **양방향 전수 일치**(누락 0·서지 orphan 0) |
| Part 0 이동 편입 라벨(주석 L308 선언: eq:partfn·eq:fermifn·eq:mu·eq:gxi) | 원위치 정의 삭제 완료 — 중복 0 기계 확인 |

---

## B. 지적 사항

### B-1. [HIGH] L2847 — tab:nodemap 의 `\_delith\_is\_discharge` 포인터가 딴 절(sec:lco-code)을 가리킴

- **위치**: L2847 (표 tab:nodemap, N0′ 보강 행)
- **원문**: `(N0$'$ 보강: \code{\_delith\_is\_discharge} 셀 라벨$\to$탈리튬화 부호 환산 = \S\ref{sec:lco-code})`
- **무엇이**: `_delith_is_discharge` 의 실제 서술 위치는 **sec:lco-code(L2635–2758)가 아니라** L2815 `\subsection{facade 와 전체 진행 한눈에}`(라벨 없는 L2760 `\section{전체 입력 인자와 기본값 — 피팅 준비}` 소속) 안의 L2817–2819 이다:
  > "LCO 서브클래스는 전극 인지 플래그(`\code{\_delith\_is\_discharge}`$=$False)로 셀 라벨을 탈리튬화 부호로 자동 환산한다 — `\code{'charge'}`$\mapsto\sigma_d{=}+1$(식~\eqref{eq:lco-sigmaslot})"
- **근거**: grep 전수 — `_delith_is_discharge` 출현은 L2818(서술)·L2847(포인터) 단 2곳. sec:lco-code 본문(2635–2758)에는 부재. 같은 표의 병렬 행 L2840 "(N6 보강: … = \S\ref{sec:broadening}…)" 은 정확히 서술 위치를 가리키는 패턴이므로, 이 행만 딴 절을 가리킨다. v1.0.13 재구조화(facade 소절이 sec:lco-code 밖으로 이동)에서 포인터 미갱신으로 추정 — 이 라운드의 주 사냥감(존재하지만 딴 대상을 가리키는 참조)에 정확히 해당. keybox 6단계 (6)이 "색인은 표~tab:nodemap"으로 독자를 이 표에 보내므로 오도 효과가 증폭된다.
- **수정안**: L2815 소절에 `\label{sec:facade}`(또는 유사) 신설 후 L2847 을 `= \S\ref{sec:facade}` 로 교체. (라벨 신설을 피하려면 문구를 "= 본문 『facade 와 전체 진행 한눈에』 소절" 로.)

### B-2. [MED] L2486 — "\S\ref{sec:sum} 의 ΔS_rxn^cat 분해" : 분해는 sec:sum 에 없음(sec:lco-decomp 소관)

- **위치**: L2486
- **원문**: "이 전자항이 \S\ref{sec:sum} 의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 분해에서 셋째 성분으로 plug-in 되며(흑연은 이 자리가 0)"
- **무엇이**: sec:sum(L1781 "합산과 역보간 (N9)")에는 $\Delta S_{\rxn,j}^\mathrm{cat}$ 도 그 "분해"도 없다(eq:sum 은 $C_\bg+\sum Q_j[\cdot]$, 표는 흑연 tab:staging). "config+vib+electronic 셋째 성분" 분해의 실제 위치는 **sec:lco-decomp**(L2553 `\subsection{LCO $\Delta S_{\rxn,j}^\mathrm{cat}$ 분해 — config + vib + electronic}`, 분해 박스 eq:lco-decomp L2597–2602 — 셋째 성분 = $\Delta S_{e,j}^{\,\mathrm{mol}}$ ✓ "셋째 성분" 서술과 정합).
- **근거(반박 검토 포함)**: sec:lco-decomp 서두 L2554 도 "합산식~\eqref{eq:sum} 의 $\Delta S_{\rxn,j}$" 라는 축약을 쓰지만 곧바로 "평형 중심 $U_j(T)$ 를 통해" 로 사슬을 명시해 자기해명한다. L2486 은 그 해명 없이 "\S\ref{sec:sum} 의 …분해" 로 적어, 독자가 sec:sum 에서 분해식을 찾게 만든다. (저자 의도가 '합산에 들어가는 ΔS' 축약이었다면 오적발 가능성 있음 — 다만 어느 해석이든 포인터 교체가 순개선.)
- **수정안**: `\S\ref{sec:sum}` → `\S\ref{sec:lco-decomp}` 로 교체, 또는 "합산식~\eqref{eq:sum} 에 $U_j(T)$ 를 통해 들어가는 $\Delta S_{\rxn,j}^\mathrm{cat}$ 의 분해(\S\ref{sec:lco-decomp})에서 셋째 성분으로 plug-in" 으로 사슬 명시.

### B-3. [MED] L1380 — "$L_V\propto|I|$ — \S\ref{sec:tail}" : 해당 관계의 수립 위치는 sec:lag

- **위치**: L1379–1380
- **원문**: "C-rate 가 오를수록 심해지고 $|I|\!\to\!0$ 에서 \emph{소멸}한다($L_V\propto|I|$ — \S\ref{sec:tail}; Fly 등\cite{fly2020})."
- **무엇이**: $L_V\propto|I|$ 는 sec:lag 에서 수립된다 — L1623–1624: "한편 $|I|$ 의존은 동결 뒤에도 살아 있다 — $L_q\propto|I|$($T_*\propto|I|$)라 $|I|\to0$ 에서 $L_V\to0$, 다음 절의 꼬리가 사라지고". 부호 회귀 R3(L2894)도 "식~\eqref{eq:LV} 의 $L_V\propto|I|\to0$" 으로 sec:lag 의 식을 가리켜 일관된다. 같은 문장 앞부분(L1378)은 올바르게 "\S\ref{sec:lag}--\S\ref{sec:tail}" 쌍을 쓰고 있어 이 괄호만 어긋난다.
- **근거(반박 검토)**: 대시가 "소멸한다"(꼬리 소멸 자체 = sec:tail 의 eq:branch 스위치)에 걸린다고 읽으면 방어 가능 — 오적발 가능성 표시. 그러나 괄호의 주어는 비례 관계 $L_V\propto|I|$ 이므로 sec:lag(또는 식 병기)가 정확하다.
- **수정안**: "($L_V\propto|I|$ — \S\ref{sec:lag}, 식~\eqref{eq:Lqfull}·\eqref{eq:LV}; Fly 등\cite{fly2020})".

### B-4. [LOW] L1508 — fig:broadening 캡션 "\S\ref{sec:tail} 의 $L_V$"

- **원문**: "① \emph{전류가 켜는} 유한율속 비대칭 꼬리(…과전압 $\eta(t)$, \S\ref{sec:tail} 의 $L_V$, $|I|\!\to\!0$ 소멸)"
- **무엇이**: $L_V$ 는 sec:lag 의 표제 주제("동역학 지연 길이 $L_V$ (N7)")이고 sec:tail 은 그것을 쓰는 절. 본문 L1378 의 표기("\S\ref{sec:lag}--\S\ref{sec:tail} 의 동역학 지연 길이 $L_{V,j}$ 와 인과 꼬리")와 정합하도록 병기가 정확.
- **수정안**: "\S\ref{sec:lag}--\S\ref{sec:tail} 의 $L_V$".

### B-5. [LOW] L1576 — "(식~\eqref{eq:mu} 의 $\Omega(1-2\xi)$)" : 좌표 불일치(원문은 $\Omega(1-2\theta)$)

- **원문**: "구동력에 평균장 $\mu$ 의 상호작용 몫(식~\eqref{eq:mu} 의 $\Omega(1-2\xi)$)을 마저 실으면 $\mathcal A_j=sF(V-U_j)-\Omega_j(1-2\xi_j)$ 다"
- **무엇이**: eq:mu(L529)의 문면은 "$\mu_\mathrm{Li}(\theta)=\mu^0+RT\ln\frac{\theta}{1-\theta}+\Omega_j\,(1-2\theta)$" — $\theta$ 좌표다. $\theta=1-\xi$ 에서 $(1-2\theta)=-(1-2\xi)$ 로 **부호가 뒤집히므로**, "식 eq:mu 의 $\Omega(1-2\xi)$" 는 문면과 어긋난다. $\xi$ 좌표의 $\Omega_j(1-2\xi)$ 는 L995 의 $g_j'(\xi)$ 전개(비라벨)·식 eq:Veq 에 있다. 유효 장벽 유도는 부호가 생명인 자리(★최우선 결함 클래스 인접)라 인용 좌표를 정확히 하는 편이 안전하다(물리 결론 자체는 기존 라운드 검증 완료 — 여기 지적은 인용 정합만).
- **수정안**: "(식~\eqref{eq:Veq} 의 상호작용 몫 — $\xi$ 좌표의 $\Omega_j(1-2\xi)$)" 또는 "(식~\eqref{eq:mu} 의 상호작용 몫을 $\xi$ 좌표로 옮긴 $\Omega(1-2\xi)$)".

### B-6. [LOW] L2605·L2610 — "★이중계산 금지(B)" 의 짝 "(A)" 부재(고아 열거자)

- **원문**: L2605 "★이중계산 금지(B) — 식~\eqref{eq:lco-decomp} 의 $\Delta S_j^\mathrm{config}$ 자리에는 …" / L2610 "★이중계산 금지(B)(config엔 중심값만, elec엔 게이트 골만)"
- **무엇이**: 문서 전체 grep 에서 "이중계산 금지(A)" 또는 짝이 되는 "(A)" 항목이 부재. 독자가 (A)를 찾게 만드는 dangling 내부 열거자다. (외부 감사 항목 ID 계승일 가능성 — 오적발 가능성 표시 — 이라도 본문 내 해소 불가는 동일.)
- **수정안**: "(B)" 삭제, 또는 첫 출현(L2605)에 "(B — 이중계산 금지 가드의 두 번째 항; (A)는 ~)" 식으로 유래 명시.

### B-7. [LOW] 자기 절 참조 2건 — 렌더링이 자기 자신을 가리킴

- L1107 (sec:width 내부): "아래 \S\ref{sec:width} logistic 유도의 중심 기울기…" → "§1.6 안에서 '아래 §1.6'" 으로 렌더링. 실제 대상은 같은 절의 다음 소절(L1135 "평형 진행률 $\xi_\eq$ — logistic 의 유도").
- L1618 (sec:lag 내부): "($\S\ref{sec:lag}$ 의 동결)" — 자기 절 참조. 실제 대상은 같은 절 앞 소절(L1552 "$L_q$ 는 전이당 한 점…\emph{상수로 동결}").
- **수정안**: 각각 "아래 소절의 logistic 유도" / "(앞 소절의 동결)" 평문화, 또는 소절 라벨 신설.

### B-8. [LOW] fig:spine 캡션 L188 — "본 문건의 절 번호가 이 노드 순서다" : Part 0 삽입 후 1:1 아님

- **원문**: L188 "본 문건의 절 번호가 이 노드 순서다."
- **무엇이**: v1.0.13 은 N0(=\S1.1 sec:notation)과 N1(=\S1.3 sec:pol) 사이에 Part 0(\S1.2 sec:sm-found)이 신설되어, "절 번호 = 노드 순서" 매핑이 더는 성립하지 않는다(노드 k ↔ 절 1.(k+1) 로 읽으면 어긋남). 노드 **순서**는 절 순서를 따르므로(단조) tab:nodemap 캡션 L2827 "본 문건 절 순서 $=$ 이 노드 순서" 는 유지 가능하나, spine 캡션의 "번호" 는 재구조화 잔재다.
- **수정안**: "본 문건의 절 \emph{순서}가 이 노드 순서를 따른다(통계역학 기초 \S\ref{sec:sm-found} 는 N0 뒤에 삽입된 기초 절)".

### B-9. [LOW] L2090–2092·L2612 — 표 내용과 서술의 부분 불일치 2건

- L2090–2092: "표~\ref{tab:lco-staging} 의 config$\cdot$vib 값은 \emph{전이별 부분몰} 성분" — tab:lco-staging(L1891–1901)의 $\Delta S$ 열에는 config 값(0.47/1.49)만 있고 **vib 수치는 없다**. → "표~\ref{tab:lco-staging} 의 config 값(및 \S\ref{sec:lco-decomp} 의 vib 슬롯)" 등으로 조정.
- L2612–2613: "vib … (흑연 표~\ref{tab:staging} 의 음의 $\Delta S_\rxn$ 에 대응)" — tab:staging 의 $\Delta S_\rxn$ 는 $+29/0/-5/-16$ 혼합 부호(음수는 하위 2행뿐). → "표~\ref{tab:staging} 하위 두 전이의 음의 $\Delta S_\rxn$" 등으로 한정.

### B-10. [NOTE] L2858 — "브리프 §7 의 부호 체크리스트" : 문서 외부 포인터

- **원문**: "브리프 §7 의 부호 체크리스트를 전건 확인한다"
- **무엇이**: "브리프"는 본 문건·Ch2 어디에도 없는 외부 작업지시문 참조 — 교과서 단독 독자는 해소 불가. 유래 표기 의도라면 각주로 지위(작성 지시문)를 명시하는 편이 깔끔.

### B-11. [NOTE] 기준온도 기호 이원화 — eq:U1T2 의 $T_0$ vs eq:lco-U1V·표 캡션의 $T_\mathrm{ref}$

- eq:U1T2(L2379, "기준온도 $T_0$")와 그 식을 "닫힌형"으로 인용하는 eq:lco-U1V(L2729, $T_\mathrm{ref}$)·L2066 적분·tab:lco-staging 캡션(L1887)이 같은 양을 두 기호로 적는다. 상호 참조 쌍(식 lco-U1V → 식 U1T2)을 오가는 독자가 $T_0=T_\mathrm{ref}$ 를 스스로 등치해야 한다. 한 기호로 통일 권고.

---

## C. 렌즈 ⑧ — R4 수정분 참조 5항목 개별 판정 (전부 PASS)

1. **L516–518 $\Omega^\mathrm{cat}$ 귀속 + \S\ref{sec:lco-hys} 신규 참조**: PASS — "Part II 의 $\Omega_j^\mathrm{cat}$(표 밖 — 피팅 배정 전제, \S\ref{sec:lco-hys})" ↔ sec:lco-hys L2123–2125 "표~tab:lco-staging 는 LCO $\Omega_j^\mathrm{cat}$ 의 수치 열을 싣지 않으며…미배정 시 구현은 $\Omega=0$ 폴백" 정확 정합. tab:staging 의 $\Omega_j$ 열 실재도 확인.
2. **G1·G2·G3 인라인 정의(L2622–2625)**: PASS — "G$n$ 일련번호의 선언은 G2 첫 정의 자리" ↔ 실제 첫 선언 L2323–2324 "(갭 G2 — G$n$ 은 본 문건이 추적하는 1차 문헌 공백의 일련번호)" 는 \S sec:lco-Se(2275–2386) 내부 — 병기된 "\S\ref{sec:lco-Se}" 와 위치 정합. G2 재언급 L2390 도 일관.
3. **fig:doublewell 캡션의 fig:sm-gxi 참조(L986–987)**: PASS — "수치 정확 좌표는 그림~\ref{fig:sm-gxi} 의 $\Omega=3RT$ 곡선" ↔ fig:sm-gxi 에 $\Omega=3RT$ 곡선·spinodal $\xi_s^\pm=0.2113/0.7887$ 실재. 수치 검산: $f(\xi_s)/RT=-0.01575$ — fig:sm-gxi 의 $-0.0157$ 정확(fig:doublewell 은 "정성 곡선" 선언이라 $-0.0155$ plot 무방). 역방향 참조(fig:sm-gxi 캡션 L587 "그 절의 이중웰 그림…확대")도 상호 정합.
4. **L1858–1861 슬롯 배정 포인터(\S\ref{sec:lco-direction})**: PASS — "탈리튬화 규약(LCO \emph{충전}$\mapsto\sigma_d{=}+1$)" ↔ eq:lco-sigmaslot(L1914–1919) "LCO 하프셀 --- 충전$\mapsto+1$" 문면 일치.
5. **(보조) L928 seam 포인터**: PASS — "LCO 전자항 plug-in 자리: \S\ref{sec:lco-code}" ↔ sec:lco-code 표제 "파라미터 교체 + 전자항 plug-in (H)" 정합.

---

## D. 전방 참조 최종 스윕 (수식·그림 한정)

**전방 `\eqref`(수식) 4건 — 무표지 잔여 0 확인**:
- L1687→eq:peakshape@1701: "바로 아래 \S 의 식~\eqref{eq:peakshape}" — "바로 아래" 표지 ✓
- L1689→eq:branch@1717: "아래 식~\eqref{eq:branch}" — "아래" 표지 ✓
- L2629→eq:lco-xmap@2708: "(구현식은 \S\ref{sec:lco-code} 식~\eqref{eq:lco-xmap})" — "아래/후술" 낱말은 없으나 후속 절 명시 포인터 동반 = 실질 완화(경계 사례로 기록만)
- L2648→eq:lco-msmrmap@2676: "정식 대응은 아래 식~\eqref{eq:lco-msmrmap}" — "아래" 표지 ✓

**전방 `\ref` 그림 19건**: 전부 같은 절 내 float 배치(원천 정의가 수~150줄 뒤; fig:spine·fig:staging·fig:sm-* 5·fig:doublewell·fig:hysloop·fig:barrier·fig:flux·fig:logistic·fig:broadening·fig:relaxode·fig:reversal·fig:lco-dirmap·fig:lco-electronic) — LaTeX float 표준 관행·전부 해당 절 본문이 도입 서술 동반. **결함 0**. 표(tab:staging 원거리 4건 등)는 이번 스윕 범위 밖(수식·그림 한정)이며 L517 은 "본론" 표지 동반.

→ R3·R4 의 6건 해소 후 **무표지 전방 수식·그림 참조 잔여 = 0** 기계 재확인 완료.

---

## E. Ch2 문자열 라벨·서지 대조

**Ch2 라벨 괄호 문자열 4건 — 전건 실재·의미 정합(PASS)**:
| Ch1 위치 | 문자열 | Ch2 정의 | 의미 대조 |
|---|---|---|---|
| L419 | (eq:Z1) "단일 자리 분배함수" | L126–128: $Z_1=1+e^{-\beta(\varepsilon_0-\mu)}$ | Ch1 eq:partfn 과 동형 ✓ |
| L667 | (eq:muV) "같은 관계" | L144–146: $\mu=\mu^0-sF(V-U_j)$ | Ch1 eq:sm-eqcond 와 동일 관계·같은 $s$ 규약 ✓ |
| L794 | (eq:Vxi) "같은 결론을 발열 관점에서 재사용" | L188–190: $V(\xi)=U_j+\frac{RT}{F}\ln\frac{\xi}{1-\xi}$ | Ch1 eq:sm-nernst($s{=}+1$)와 동일 ✓ |
| L1267 | (eq:logistic) "부호까지 동일" | L156–159: $\xi_\eq=1/(1+e^{-(V-U_j)/w})$ | Ch1 eq:logisticsolve·eq:xieq 와 부호 일치 ✓ |

**서지**: `\cite` 20키 ↔ `\bibitem` 20건 양방향 전수 일치, orphan 0. 각 인용처 의미도 대조(dreyer2010=히스 기원, eyring1935=속도식, bazant2013=전하전달, leviaurbach1999=내재 폭, fly2020=율속 ICA, dahn1995=무질서 용량한계, park2021=GITT OCP, xia2007=LCO 3전이, reynier2004=엔트로피, motohashi2009=g(E_F)·전자상도, menetrier1999·reimers1992=MIT, swiderska2019=+0.83 mV/K, msmr2024=MSMR, ml2024=config 단독 불가, rsc2021=staging 비교) — 전건 적정.

---

## F. Coverage 선언

- **라벨 총수**: 163 (Ch1) / **중복 정의**: 0 / **dangling 참조**: 0 (LastPage 는 패키지 제공)
- **참조 사용 총수**: 536 (\eqref+\ref+\pageref; \cite 별도 37)
- **의미 대조한 참조 수**: 536건 전수 — 전문 정독 중 각 사용처 문맥 ↔ 대상 원문(줄 단위) 대조. 서술이 대상 내용을 규정하는 참조(「식 X 의 logistic」·「표 Y 의 행」류) 약 460건은 개별 판정, 단순 병기 나열(keybox 사다리·표 식 열·codebox 사슬)도 대상 실재·식 정체 확인. 수치 동반 참조는 재계산 검산(아래 물리 불변).
- **orphan 라벨 23건** (결함 아님 — 참조 0 기록): sec:sm-found·sec:sm-site·sec:lco-why(절 3) / eq:sm-occmid·eq:sm-factor·eq:sm-mf·eq:sm-gtheta·eq:sm-emu·eq:sm-mubridge·eq:Lqmid·eq:Lqmid2·eq:intfactor·eq:lco-gpp·eq:lco-spinodal·eq:lco-Veq·eq:lco-mit·eq:lco-dope·eq:Sedirect·eq:lco-peakobs·eq:lco-slots·eq:lco-msmrnorm·eq:lco-msmrpeak·eq:lco-plugin(식 20). 이 중 boxed 결과식(eq:lco-mit·eq:lco-plugin 등)은 참조 없이도 자체 완결이라 무해.
- **전방 참조**: 수식 4(전부 완화)·그림 19(전부 같은 절 float) — 무표지 잔여 0.
- **Ch2 대조**: 문자열 라벨 4/4 PASS·서지 20/20 PASS.

**물리 불변 확인**: 본 라운드 지적은 전부 포인터·문구 정합(참조 대상 교정)이며 **물리식·부호·수치 변경 제안 0**. 정독 중 수치 재검산 전건 통과 — R1 히스 86.7 mV($u=0.766$)·문턱 $2RT=4958$ J/mol·$\nu$ 점프 $1-(1/\nu)/(e^{1/\nu}-1)$: 22.9%(ν=2)/6.1%(8)/4.9%(10)·표 tab:staging $U(298)$ round-trip 4행(0.2109/0.1399/0.1203/0.0853 V, ±1 mV)·$w=RT/F$ 23.1/25.7/28.3 mV·게이트 골 −46 J/(mol K)·되먹임 상한 0.477 mV/K×30 K≈14 mV·spinodal $f/RT=-0.0157$ — 전부 문서 기재값과 일치.

---

## G. 가장 약한 1곳

**L2847 tab:nodemap 의 `_delith_is_discharge` → \S\ref{sec:lco-code} 포인터(B-1)**. 이 표는 keybox "(6) … 색인은 표~tab:nodemap" 이 독자를 명시적으로 보내는 문서 공식 색인인데, 그 색인의 한 행이 재구조화 이전 위치(딴 절)를 가리킨다 — 이 라운드 청크 스킴(참조 전수 대조)이 아니면 통독으로 걸리기 어려운 종류이고, 색인 오류라 오도가 구조적으로 증폭된다.

---

## 5줄 요약 (오적발 자기표시)

1. HIGH 1건: L2847 색인표의 `_delith_is_discharge` 포인터가 sec:lco-code 를 가리키나 실서술은 L2818 facade 소절(딴 절) — grep 전수로 확정, 오적발 가능성 낮음.
2. MED 2건: L2486 "\S sec:sum 의 ΔS^cat 분해"(분해는 sec:lco-decomp 소관 — 축약 의도였다면 오적발 가능성 有)·L1380 "$L_V\propto|I|$ — \S sec:tail"(수립처는 sec:lag — 대시 귀속 해석에 따라 오적발 가능성 有).
3. LOW 6건: 캡션 $L_V$ 귀속(L1508)·eq:mu 인용 좌표 $\theta$/$\xi$ 불일치(L1576)·고아 열거자 "(B)"·자기 절 참조 2건·spine 캡션 "절 번호=노드"(Part 0 삽입 후 부정확)·표-서술 부분 불일치 2건(L2090 vib 값 부재·L2612 혼합 부호).
4. 기계 감사: 라벨 163·참조 536·dangling 0·중복 0·cite/bib 20:20 완전 일치·무표지 전방 수식/그림 참조 잔여 0(R3·R4 해소 확인)·Ch2 문자열 라벨 4/4 정합.
5. 렌즈 ⑧ R4 수정분 5항목 전부 PASS·물리 불변(수치 재검산 전건 일치, 물리 변경 제안 0) — 지적은 전부 포인터·문구 교정 범위.
