# V1.0.13 P5 검수 라운드 5 — 검수자 C (참조·라벨·경계 단위, Ch2 + 챕터 간)

- 대상: `Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex` 전문(797줄) + `graphite_ica_ch1_v1.0.13.tex`(2771줄, 대조 구역 표적 정독) + `Anode_Fit_v1.0.13.py`(라벨 문자열 전수)
- 방법: 스크래치패드 스크립트로 \label/\ref/\eqref/\cite/\bibitem 기계 전수 추출 → dangling·orphan·중복 판정 → 각 참조의 서술-대상 의미 대조 → 챕터 간·py 문자열 라벨 전수 재대조 → 절 경계·float·R4 수정분 렌즈 ⑧ 재검.
- ★검수 의견만 — tex/코드 무수정. 모든 지적에 줄 번호·원문 인용 병기. 보고 4-tier(확정/근거 미발견/추정/미검증) 표기.

---

## A. 지적 사항

### [C-1][MEDIUM][확정] §2.4 도입 열거가 (A)(B)(D)만 — 파생 C 누락 + C 내용의 포인터가 자기 절을 우회

- 위치: Ch2 L455–459 (§\ref{sec:mixing} 도입) ↔ L578 (파생 C 소절 실재)
- 무엇: 절 도입 로드맵이 파생 3건만 예고하는데 절 본문은 파생 4건(A·B·C·D)을 담는다. C 의 내용(폭 w 지위)은 무명 괄호문으로만 언급되고, 그 "지위 못 박기"의 포인터가 자기 소절(파생 C, \S\ref{ssec:weff})이 아니라 \S\ref{sec:revheat} 종합식으로 간다.
- 근거(원문):
  - L455–457: "이 절은 (A) 겹침 가중식을 음함수 미분으로 닫고 수치로 검증하며, (B) 이중계산을 분리하고, (D) 히스테리시스 분기별 $\partial U/\partial T$ 를 / 가역/비가역으로 어떻게 가르는지를 닫힌식으로 다룬다."
  - L457–459(이어지는 괄호문): "(이상 격자기체의 폭 $w=RT/F$ 는 단상 평형 예측이지만, … 그 \emph{지위}는 \S\ref{sec:revheat} 종합식에서 못 박고, 폭의 \emph{기원}은 Chapter 1 broadening 절이 다룬다.)"
  - L578: "\subsection{파생 C — 폭 $w$ 의 지위: 단상 평형 예측 vs.\ 두-상 현상학적 피팅 폭}\label{ssec:weff}" — 그리고 그 소절 자신이 L593–594 에서 "본 장은 그 결과만 받아 $w_j$ 의 \emph{지위}를 못 박는다"고 선언.
- 진단: v5 개정 때 구 파생 C(w_eff 축소식)를 제거하면서(헤더 주석 L9–14) 도입 열거가 (A)(B)(D)로 재작성됐고, 이후 신 파생 C(폭 지위)가 같은 자리에 들어왔는데 도입이 재동기화되지 않은 잔재로 판단(추정 — 경위는 추정, 불일치 자체는 확정).
- 수정안: 도입을 "(A) …, (B) …, (C) 폭 $w_j$ 의 이중지위를 못 박고(\S\ref{ssec:weff}), (D) …" 4-항 열거로 재동기화. 괄호문 포인터는 \S\ref{ssec:weff}(1차) + \S\ref{sec:revheat}(종합식 재확인, 2차) 순으로.

### [C-2][MINOR][확정] procedurebox 5단계의 config 항 계수 — eq:single_config 인용인데 $n_j$ 탈락

- 위치: Ch2 L758–759 ↔ L567 (eq:single_config)
- 무엇: 절차 박스가 식~\eqref{eq:single_config} "의" 분포 config 항을 인용하며 계수를 $(R/F)$ 로 적음. 인용 대상 식의 계수는 $(n_jR/F)$.
- 근거(원문):
  - L758–759: "식~\eqref{eq:single_config} 의 분포 config 항 $(R/F)\ln[\xi_j/(1-\xi_j)]$ 가 자동으로 채우며"
  - L567(eq:single_config): "$\frac{\partial U_\oc}{\partial T}(x)\;\approx\;\frac{\Delta S_{\rxn,j}}{F}\;+\;\frac{n_jR}{F}\ln\!\frac{\xi_j}{1-\xi_j}$"
  - 방증: py L561–562 도 같은 계수를 R2 에서 정정했음을 기록 — "★config 항 계수 = ∂w_j/∂T = n_j·R/F (v1.0.13 R2 정정 — 구판은 R/F 로 n_j=1 특수형…)". Ch2 L259 는 R/F 를 "자리당 $n_j{=}1$ 서식"으로 명시 구분하고 있으므로, 일반 절차를 서술하는 procedurebox 에서 특수 서식으로 인용하면 층위가 흐려짐.
- 수정안: L758 을 "$(n_jR/F)\ln[\xi_j/(1-\xi_j)]$" 로 (또는 "$(R/F)$($n_j{=}1$ 서식; 일반형 $n_jR/F$)" 병기로) 정정.

### [C-3][MINOR][확정] py 주석의 `sec:lco` 문자열 3곳 — Ch1 에 그런 라벨 없음 (dangling 문자열 포인터)

- 위치: `Anode_Fit_v1.0.13.py` L169, L631, L663
- 무엇: 주석이 "Ch1 sec:lco" 를 가리키나 Ch1 라벨 163종 전수에 `sec:lco` 는 없음(실재는 `sec:lco-intro`(L1830)·`sec:lco-map`(L1837)·`sec:lco-code`(L2635) 등 접미사형뿐).
- 근거(원문):
  - py L169: "# ===== LCO 양극 확장: 전자 엔트로피(MIT) — Ch1 sec:lco, eq:dSegate ============="
  - py L631: "# ===== LCO 양극 MSMR 시연 데이터셋 — Ch1 sec:lco =============================="
  - py L663: `"""LCO 양극 dQ/dV — MSMR 동형(Ch1 sec:lco: X_j↔Q_j, …)`
- 참고: R4 현행화 대상 13종(eq:vn·eq:Uj·eq:dUhys·eq:Ubranch·eq:wbase·eq:xieq·eq:eqpeak·eq:belliden·eq:chid·eq:Lqfull·eq:LV·eq:peakshape·eq:sum)은 전부 실재·의미 일치(§B 참조) — 이 3곳은 그 목록 밖의 잔존.
- 수정안: 내용상 L169·L663 은 `sec:lco-intro`(Part II 총괄) 또는 세부 절(`sec:lco-Se`/`sec:lco-code`)로, L631 은 `sec:lco-code`(MSMR)로 특정.

### [C-4][LOW][확정] py L558 "(eq:weighted 완전식)" — eq:weighted 는 Ch2 명시 '단순식' 라벨

- 위치: py L558 ↔ Ch2 L496–499, L717–721
- 근거(원문): py L558 `"""가역 엔트로피 계수 ∂U_oc/∂T(x) [V/K] — Ch2 가중식(eq:weighted 완전식).` ↔ Ch2 L496 boxed 식 자체가 "$\frac{\partial U_\oc}{\partial T}(x)\Big|_{\text{단순식}}$" 로 표기·L513 "식~\eqref{eq:weighted} 의 \emph{단순식}". 완전식은 라벨 없는 §2.6 keybox 박스(L717–721).
- 판단: 구현식(py L560)은 완전식이 맞고 eq:weighted 의 가중 구조 확장이므로 오독 위험은 낮으나, 라벨-의미가 어긋나는 문자열 참조(이번 라운드 사냥감 유형). 수정안: "(Ch2 eq:weighted 의 완전식 확장 — §2.6 keybox 종합식)" 류로 정밀화.

### [C-5][LOW][확정] Ch1 L420 "Ch2 표기와 맞추어 같은 글자 $Z$" — Ch2 의 해당 식 표기는 $Z_1$

- 근거(원문): Ch1 L419–420: "Chapter 2 의 단일 자리 분배함수(그 문건 식 (eq:Z1))와 같은 식이다. … Ch2 표기와 맞추어 같은 글자 $Z$ 로 적는다." ↔ Ch2 L126–128(eq:Z1): "$Z_1 \;=\; \sum_{n=0,1} e^{-\beta(\varepsilon_0-\mu)\,n}$". Ch2 의 서(L91)만 prose 로 "분배함수 $Z$".
- 판단: 식-대-식 대응(1+e^{−βΔμ})은 정확 일치[확정]. "같은 글자" 주장만 아첨자 하나 어긋남. 수정안(택1): Ch1 쪽 "같은 글자 $Z$($=$Ch2 의 $Z_1$)" 병기, 또는 방치 가능한 수준.

### [C-6][LOW][확정] Ch2 orphan 라벨 4건 — 본문·챕터 간·py 어디서도 참조 없음

- ssec:logistic(L142)·eq:slope_BW(L219)·eq:Svib_mode(L388)·ssec:hys(L609). 컴파일 무해하나, 특히 ssec:hys(파생 D)는 본문이 "파생 D" 이름으로만 지시(L456, L739–740, L774)하고 \S\ref 참조가 0회 — 파생 C 가 \S\ref{ssec:weff} 로 5회(L176, L532, L657, L668, L726) 참조되는 것과 비대칭. 수정안: 파생 D 언급 1곳 이상(예: L739 "파생 D 는")에 \S\ref{ssec:hys} 부착, 나머지는 유지 또는 라벨 제거 판단은 저자 몫.

### [C-7][LOW][확정] keybox L169–170 의 폭 서식 포인터가 1차 등장 위치를 건너뜀

- 근거(원문): L169–170: "(자리당 $n_j{=}1$ 기준; 전이별 유효 폭 서식 $w_j=n_jRT/F$ 는 \S\ref{sec:revheat}$\cdot$코드 \texttt{func\_w})". Ch2 안에서 $w_j(T)=n_jRT/F$ 의 첫 실체 등장은 파생 A 의 L482–483("폭 $w_j(T)=n_jRT/F$ 의 명시적 온도 의존") — \S\ref{ssec:overlap}. sec:revheat 키박스에는 "평형 예측 $nRT/F$"(L725)로만 재등장.
- 수정안: 포인터를 "\S\ref{ssec:overlap} 식~\eqref{eq:dxidT}$\cdot$\S\ref{sec:revheat}$\cdot$코드 func\_w" 로.

### [C-8][LOW][확정] "eq~\eqref{…}" 표기 2곳 — 문서 전반의 "식~\eqref{…}" 와 불일치

- L722–723: "Ch1 의 $\xi_j(V,T)$(eq~\eqref{eq:logistic})" / L730: "이 식은 eq~\eqref{eq:single_config} 로 환원된다". 나머지 전부(약 30곳)는 "식~\eqref{…}". 수정안: "식~\eqref{…}" 통일.

### [C-9][LOW][확정] py L608 "(warnbox·eq:qrev 는 lumped 만 제시)" — Ch2 에서 q_irr lumped 를 제시하는 박스는 warnbox 가 아님

- 근거(원문): py L608–609: "★3분해(I²R_n + I·η_ct + I·η_diff)는 Ch2 에 boxed 식이 없다(warnbox·eq:qrev 는 / lumped 만 제시)". Ch2 쪽 실제: lumped 첫 항은 eq:qrev(L687–690) 본문 + ★라벨 층위 주의 문단(L694–697, 박스 아님) + srcbox(L698–701, 부호 규약). Ch2 의 warnbox 3곳(L103 범위·L313 이중계산·L600 폭)은 q_irr 을 다루지 않음. "3분해 boxed 식 없음" 주장 자체는 정확[확정]. 수정안: "warnbox" → "srcbox" 또는 "eq:qrev 주변 prose".

### [C-10][관찰] 폭 w 지위 서술의 5중 반복 / §2.1 도입의 BW 소절 미예고 / tab:ds x-범위 출처

- (i) w 지위 recap 이 keybox L167–184·L223–224·L457–459·파생 C L578–607·keybox L724–726 의 5곳에서 반복 — 각기 포인터 형식이라 규정 위반은 아니나 밀도 높음(이전 라운드 유지 결정으로 보임 — 재론 아님, 기록만).
- (ii) §2.1 도입(L117–120)은 "분배함수→점유 분포→logistic 기원"만 예고하고 ssec:BW(다자리 평균장, L196)는 미예고 — C-1 과 같은 유형이나 경미.
- (iii) tab:ds 의 "x 범위" 열(0.08–0.16/0.16–0.25/0.25–0.50/0.50–1.00)은 Ch1 tab:staging 의 Q 분율 누적(0.10/0.22/0.47/0.97)과 1:1 이 아님 — 각주(L360–363)가 경계 불일치를 이미 선언하고 있어 미결함 처리[확정]. 기록만.

---

## B. 검산 PASS 기록 (렌즈 ⑧ — R4 수정분 + 물리 불변)

R4 수정분 4건 전수 재검 — 모두 PASS:
1. L259–262 "…식~\eqref{eq:dxidT}; $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ 를 첫 항으로 쓰고…" — 괄호 짝 1쌍 정확, 세미콜론 2개 병렬 유효, 부호 검산 $-R\ln[(1-\xi)/\xi]=+R\ln[\xi/(1-\xi)]$ 수학적으로 옳음.
2. L630–631 "…$\propto I\,\Delta U^\hys$ 의 소산율(한 사이클당 $\propto Q_\mathrm{cycle}\,\Delta U^\hys$ 의 entropy production 소산열)…" — 차원(율=W, 사이클당=J) 정합·괄호 짝·문법 정상.
3. L523–527 srcbox 'n' 키 한정 — py 대조 실증: `_n_factor`(py L301–307)가 'n' 우선, 'w' 단독이면 현재 T 로 $n=wF/RT$ 역산 → `_width`=`func_w(T,n)`=w 상수 = **T-동결 폭** ✓; 'n' 보유 시 $w=nRT/F$ 열적 서식 ✓; "검증 데이터셋은 전 전이 해당" ↔ py 헤더 L10 "GRAPHITE_STAGING_LIT 는 'n':1.0 보유" ✓.
4. 파생 D $+\tfrac12\sigma_d$ 2곳(L611·L627) — 두 식 동일 표기, Ch1 eq:Ubranch(L1049) $U_j^{\,d}=U_j+\tfrac12\sigma_d h_{\eta,j}\gamma_j\Delta U_j^\hys$ 의 $\gamma_jh_{\eta,j}{=}1$ 특수형 정확(곱 순서 차이는 무해), 가지 방향(dis $+\tfrac12$ 위/ch $-\tfrac12$ 아래) ↔ Ch1 L1053–1054 "$U_j^{\dis}>U_j^{\chg}$" 일치.

물리 불변 확인(챕터 간 같은 값·같은 식 전수 — 전부 일치, 상이점 0):
- $U_j(T)=(-\Delta H+T\Delta S)/F$: Ch2 L71 = Ch1 eq:Uj(L914) ✓
- $\Delta S^0_j$ 4값 $+29/0/-5/-16$: Ch2 tab:ds = Ch1 tab:staging(L1812–1815) ✓; ΔH(2→1) $-13.0$ kJ/mol = 표 $-13000$ J/mol ✓(검산 $-FU+T\Delta S=-12971$ J/mol)
- 임계 $\Omega_c=2RT$: Ch2 eq:slope_BW·tab:limits = Ch1 eq:sm-thresh(L547–550) ✓; 두-상 전이 = 2L→2·2→1 두 건: Ch2 L172–173·L585 = Ch1 헤더 L23 "two-phase=LiC₁₂·LiC₆ 2개만" ✓
- logistic 부호: Ch2 eq:logistic($\xi_\eq=1/(1+e^{-(V-U_j)/w})$) = Ch1 eq:sm-logistic(L672–674, s=+1)·eq:logisticsolve·eq:xieq ✓ — Ch1 L1267 "부호까지 동일" 주장 실측 확인
- 분극식: Ch2 L751 = Ch1 eq:vn(L831) $V_n=V_\app-\sigma_d|I|R_n$ ✓; σ_d 작용처 셋(분극·분기·꼬리): Ch2 각주 L149–150 = Ch1 L209·L1911–1912 ✓; s=+1 유도 전용: Ch2 L148–151 = Ch1 L657–658 ✓
- 가역열 부호: Ch2 L705–706(방전 I>0, ΔS>0→흡열) = py L599 ✓; 서 L85 = eq:qrev ✓; 단위 환산 $+29$ J/(mol K) ⇒ $0.30$ mV/K 산술 ✓($29/96485=3.0\times10^{-4}$)

챕터 간 문자열 라벨 5건 전수: Ch1→Ch2 4건(eq:Z1 L419·eq:muV L667·eq:Vxi L794·eq:logistic L1267) 모두 Ch2 에 실재·의미 일치 ✓ / Ch2→Ch1 1건(eq:Ubranch L611) 실재·의미 일치 ✓. Ch2 의 서술형 Ch1 지시("Part 0"·"broadening 절"·"폭 이중지위"·"전자 엔트로피 절"·"단위 다리") 전부 Ch1 실체(L799 "Part 0 사다리"·sec:broadening·sec:width L1118·sec:lco-Se·L677–679) 확인 ✓.

py 라벨 문자열 59건 전수: Ch1 라벨 51건 실재+수식 의미 일치(R4 현행화 13종은 개별 식 대조 — eq:vn·eq:Uj·eq:dUhys·eq:Ubranch·eq:wbase·eq:xieq·eq:eqpeak·eq:belliden·eq:chid·eq:Lqfull·eq:LV·eq:peakshape·eq:sum 전부 Ch1 boxed 식과 문자 그대로 일치) ✓ / Ch2 라벨 5건(eq:weighted·eq:hys_rev·eq:qrev×3) 실재 ✓(정밀도 지적은 C-4) / 부재 3건 = C-3.

---

## C. 가장 약한 1곳

**C-1 (§2.4 도입 [A][B][D] 열거 — 파생 C 부재).** 이 장의 파생 A~D 는 챕터의 척추 구조인데, 로드맵이 4개 중 3개만 예고하고 C 의 소유권을 자기 소절이 아닌 §2.6 으로 넘긴다. 독자가 도입을 신뢰해 절을 따라가면(G-follow) 무예고 소절을 만나고, 맺음(L773 "파생 C")과도 어긋나는 유일한 지점이다.

## D. Coverage 선언

- Ch2 \label 38종(중복 0) / \ref·\eqref 89회·대상 34종 — dangling 0·orphan 4(C-6) / 의미 대조 89회 전수 수행, 불일치 = C-2 1건.
- \cite 29회(L198–199 다행 1건 포함)·14종 ↔ \bibitem 14종 — 상호 누락 0. 인용-서술 정합 스팟 확인(occupation2019 방법수준 한정·msmr_partII 단위 [미검증] 헤지·chemmater2015 abstract tier 등 선언 일치).
- 챕터 간 문자열 참조 총 5건(Ch1→Ch2 4 + Ch2→Ch1 1) — 전수 실재·의미 일치. Ch1 의 "Chapter 2/Ch2" 언급 문장 8곳 의미 대조 완료.
- py 라벨 문자열 59건 전수 — 실재 56·부재 3(C-3).
- 절 경계 8개 구획(서·§2.1~§2.6·맺음) 도입/마무리/고아 지시어/float 전수 — 결함 = C-1(+C-10 관찰). float 4건 전부 참조 보유·[t] 배치 정상.
- R4 수정분 렌즈 ⑧ 4건 — 전부 PASS. coverage missing = 0.
- 오적발 자기표시: 기계 추출 1차 판정 "bazant2013 미인용"은 내 스크립트의 줄단위 한계(L198 "\cite{huggins2009," + L199 "bazant2013}." 다행 걸침)로 인한 **오탐 — 원문 확인으로 철회**(이에 따라 cite 사용 수를 27→29 로 보정). 그 외 지적은 전부 원문 재확인 완료.

## E. 5줄 요약

1. 기계 전수: Ch2 라벨 38·참조 89·인용 14종 — dangling/미해결 인용 0, orphan 라벨 4(LOW).
2. 챕터 간 문자열 라벨 5건·py 라벨 문자열 59건 전수 대조 — py `sec:lco` 3곳만 부재(MINOR), 나머지 전부 실재·의미 일치.
3. 최중 지적 = §2.4 도입이 파생 (A)(B)(D)만 예고, 실재 소절은 A·B·C·D(MEDIUM, v5 개정 잔재 추정).
4. 수치·부호 불변(ΔS⁰ 4값·ΔH −13.0·Ω_c=2RT·σ_d 3작용처·logistic 부호·가역열 부호) 챕터 간 전부 일치 — 상이점 0.
5. R4 수정분 4건 렌즈 ⑧ 재검 전부 PASS; 오적발 1건(bazant2013)은 자기 검증으로 철회.
