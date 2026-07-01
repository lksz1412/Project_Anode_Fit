# V1011 Phase 1.1 — LCO 수식화 드래프트 (ID = S3, Sonnet)

> 대상: `Claude/docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex` — sec:lco-center(L470-513, 섹션 실경계) · sec:lco-hys(L684-708, 섹션 실경계; 지시 범위 L684-932는 다음 sec:width/sec:dist 그림까지 포함하는 정독 여유값으로, 실제 재작성 대상은 sec:lco-hys 본문 L684-708). tex/코드 미수정 — 드래프트만. 근거 줄번호는 전부 위 tex 파일 기준.

---

## 0. 정독 확인 (근거)

- 흑연 forward 대조표본: sec:center §"$G,\mu$ 와 평형 조건 — 유도"(L411-440, (a)(b)(c)(d) 라벨), §"$U_j(T)$ — 온도 환산"(L442-461, (a)(b)(c)(d) 라벨) — 이것이 sec:lco-center 가 따라야 할 밀도.
- sec:hys §"상호작용이 평형을 비트는 곳"(L523-557, (a)(b)(c)(d)) · §"gap 의 닫힌 꼴"(L584-623, (a)(b)(c)(d)) · §"방향별 분기 중심"(L625-641, (a)(b)(c)(d)) — sec:lco-hys 가 따라야 할 밀도.
- sec:lco-center 원문 L470-513, sec:lco-hys 원문 L684-708 전문.
- V1010_LCO_STYLE_REPORT.md §1 필요한 수식 사슬 컬럼(L11-12).
- AUTHOR_BRIEF(v9) G-derive·부호·LCO 확정값(전이표 T1/T2/T3, config ΔS 0.47/1.49 J/K·mol, tier 구분).
- R1_broadening.md calibration: 흑연 two-phase = LiC₁₂·LiC₆ 2개만(dilute·4L-3L은 solid-solution). **LCO는 이와 별개 계**임을 확인 — tex 본문 L1209("LCO 의 세 전이도 모두 $\Omega_j>2RT$ 의 두-상")·L1211이 이미 T1·T2·T3 전부 two-phase로 명시. 이 값을 sec:lco-hys 재작성에 그대로 정합시킴(신규 판정 아님, 기존 확정 재사용).
- sec:lco-decomp(L1690-1727, eq:lco-decomp) — config 슬롯 = 봉우리 *중심 표준값* $\Delta S_j^0$(로그 몫과 별개), Ω_j(상호작용 에너지, 엔탈피성)와는 다른 양임을 확인(아래 §2 논리 감사에서 이 구분을 활용).

---

## 1. sec:lco-center 재작성안

### 1.1 삽입 위치
L470-513 (`\subsection{LCO 평형 중심과 $\partial U_j/\partial T$ — 양극 부호}\label{sec:lco-center}` 전체) 교체. 앞뒤(L468 코드박스 끝, L514 다음 섹션 도입)는 불변.

### 1.2 원 줄글 대비 — 무엇이 산문이었나
- L471-476: "유도에 전극 가정이 없다 ... 그대로 성립한다"가 **결론만 서술** — eq:eqcond 가 어디서 전극 비의존성을 얻는지 식으로 짚지 않음(단정 비약).
- L477-482: $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ 를 "식~eq:Uj 의 $T$ 미분"이라 괄호 안에 압축 — 미분 연산 자체(좌변 미분 vs Gibbs 항등식 경유 이중 확인)가 본문에 없음. 흑연 본문(L458)도 이 관계를 괄호로 언급하지만, 그건 이미 본문(L442-455)에서 $U_j$ 를 (a)→(d)로 완전히 유도한 *뒤*의 부가 언급이라 괜찮다 — LCO 절은 그 앞 단계(왜 이 관계가 전극 불문인가) 자체가 유도 없이 결론으로 시작한다는 점이 다르다.

### 1.3 재작성 수식 사슬

**① 전극무관 논증 — 단정 비약 제거, eq:n0map·eq:eqcond 대입으로**

> **(a) 출발 — 평형 조건의 유도 경로 재확인.** 식~\eqref{eq:eqcond} $\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U)$, $\Delta G_j=-sFU_j$ 는 \S\ref{sec:center}(a)(b)(c)에서 (i) 전기화학 퍼텐셜 균형 $\tilde\mu_{\mathrm{Li}^+}+\tilde\mu_{e^-}=\tilde\mu_\mathrm{Li}$(식~\eqref{eq:eqbalance}), (ii) 전자항의 전위 의존 $\tilde\mu_{e^-}=\mu_{e^-}^0-FV$ 만으로 닫혔다. 이 두 입력 중 어디에도 "흑연"이라는 물질 고유 항이 들어가지 않는다 — $\tilde\mu_{e^-}=\mu_{e^-}^0-FV$ 는 전자 1개가 전위 $V$ 를 가로지를 때의 일 $-FV$ 이며 이는 전극 재질과 무관한 정전기 일이다(전극 정보는 오직 화학종의 표준 퍼텐셜 $\mu^0,\mu_{e^-}^0$ 값 안에 있고, 이는 애초부터 식~\eqref{eq:eqcond} 우변의 상수 $U_j$ 자리로 흡수된 항이다).
>
> **(b) 적용 연산 — 삽입 반응을 LCO 종으로 바꿔 같은 유도를 재확인.** LCO 삽입 반응은 $\mathrm{Li}^++e^-+\square_\mathrm{LCO}\rightleftharpoons\mathrm{Li}_{(\mathrm{LCO})}$(공석 $\square_\mathrm{LCO}$ 에 흡착)로, 화학종 이름만 바뀌고 반응의 항 구조(전기화학 퍼텐셜 균형 + 전자항의 $-FV$)는 흑연 반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{흑연})}$(L424)과 동형이다. 식~\eqref{eq:eqbalance}$\to$\eqref{eq:eqcond} 유도를 이 LCO 반응에 대해 다시 밟아도 같은 좌표($\theta,V$)와 같은 상수 정의($sFU\equiv$ 전위 무관 상수 덩이)로 닫히므로,
> \begin{equation}
> \mu_\mathrm{Li}^\mathrm{cat}(\theta_\eq)=\mu^{0,\mathrm{cat}}-sF(V-U_j^\mathrm{cat}),\qquad \Delta G_j^\mathrm{cat}=-sFU_j^\mathrm{cat}
> \label{eq:lco-eqcond}
> \end{equation}
> 형태가 흑연과 나란히 성립한다(부호 $s=+1$ 규약 동일 — \S\ref{sec:lco-map} 의 방전=리튬화 재확인과 정합).
>
> **(c) 중간식 — $U_j^\mathrm{cat}(T)$ 도 같은 온도 환산.** 식~\eqref{eq:lco-eqcond} 에 식~\eqref{eq:Ujmid} 의 유도(즉 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 대입 후 $U_j$ 로 이항)를 그대로 반복하면
> \begin{equation}
> U_j^\mathrm{cat}(T)=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\,\Delta S_{\rxn,j}^\mathrm{cat}}{F}
> \label{eq:lco-Uj}
> \end{equation}
> — 식~\eqref{eq:Uj} 와 *같은 함수형*, 입력만 $(\Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat})$.
>
> **(d) 박스 — 값의 차이만 명시.**
> \begin{equation}
> \boxed{\;U_j^\mathrm{cat}(T)=\dfrac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\,\Delta S_{\rxn,j}^\mathrm{cat}}{F}\;,\qquad\text{함수형 }=\text{ 식~\eqref{eq:Uj}, 입력만 다름.}}
> \label{eq:lco-Ujbox}
> \end{equation}
> 양극 영역의 높은 중심($\sim$3.9--4.2 V)은 LCO 삽입 반응의 큰 음의 $\Delta H_{\rxn,j}^\mathrm{cat}$(분자 $-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 크게 양)에서 온다 — 흑연의 $\sim$0.1 V 와 *같은 식, 다른 입력값*이라는 원문 결론(L474-475)은 이 유도로 근거가 채워진다.

**② $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ — 괄호 전보체를 완결 다리로**

> **(a) 출발 — 두 개의 독립 경로.** $\partial U_j^\mathrm{cat}/\partial T$ 를 확인하는 데는 두 경로가 있고 서로 검산한다: 경로 1(직접 미분) — 식~\eqref{eq:lco-Ujbox} 를 $T$ 로 바로 미분. 경로 2(Gibbs 항등식 경유) — $\Delta G_j=-FU_j$(식~\eqref{eq:eqcond}, $s=+1$)와 Gibbs 자유에너지의 온도 미분 항등식 $\partial(\Delta G_j)/\partial T=-\Delta S_{\rxn,j}$(식~\eqref{eq:gibbsdef} $G\equiv H-TS$ 를 $T$ 로 미분하면 $\partial G/\partial T=\partial H/\partial T-S-T\partial S/\partial T$; 반응차 $\Delta$에서 $H,S$ 를 $T$ 무관 상수로 두는 표준 근사(반응 엔탈피·엔트로피 자체가 이 온도창에서 상수, \S\ref{sec:center} 도입 전제와 동일) 아래 $\partial\Delta H/\partial T\approx0$ 이라 $\partial\Delta G/\partial T=-\Delta S$ 로 닫힘).
>
> **(b) 적용 연산 — 경로 2 를 식으로.** $\Delta G_j=-FU_j$ 의 양변을 $T$ 로 미분하면
> \begin{equation}
> \frac{\partial(\Delta G_j)}{\partial T}=-F\frac{\partial U_j}{\partial T}
> \quad\text{그리고}\quad
> \frac{\partial(\Delta G_j)}{\partial T}=-\Delta S_{\rxn,j}
> \label{eq:lco-gibbschain}
> \end{equation}
> 두 우변을 잇는다.
>
> **(c) 중간식 — 두 경로 일치 확인.**
> \begin{equation}
> -F\frac{\partial U_j}{\partial T}=-\Delta S_{\rxn,j}
> \quad\Longrightarrow\quad
> \frac{\partial U_j}{\partial T}=\frac{\Delta S_{\rxn,j}}{F}
> \label{eq:lco-dUdTmid}
> \end{equation}
> — 이는 식~\eqref{eq:lco-Ujbox} 를 직접 $T$ 미분한 값 $\partial U_j^\mathrm{cat}/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$(경로 1)와 정확히 일치한다(교차검증, $\Delta H$ 항은 $T$ 미분에서 소거).
>
> **(d) 박스.**
> \begin{equation}
> \boxed{\;\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}\;,}
> \label{eq:lco-dUdT-box}
> \end{equation}
> 전극 불문(경로 1·2 어디에도 흑연/LCO 구분 항이 없음). 이하 원문 L482-508(대표 스케일 검산·단전극 대 전셀 혼동 금지·전자항과의 부호 공존)은 **변경 없음** — 이미 수식·검산 박스(verifybox, L490-509) 형태로 잘 서 있고, 위 (a)-(d) 다리가 그 앞에 서면 verifybox 의 "식~\eqref{eq:lco-dUdT} 에 역대입" 문장이 지금보다 훨씬 근거 있게 읽힌다.

### 1.4 논리 감사 결과 — **무결**
- 물리 인과: 전기화학 퍼텐셜 균형(L422-429)의 항 구조는 화학종 이름에 의존하지 않음 — 결론(L471-476)이 옳다. 재작성은 이를 "왜 옳은가"를 eq:eqbalance 재적용으로 보였을 뿐, 물리·부호·결과식 변경 없음.
- 부호: $\partial U/\partial T=\Delta S/F$ 는 흑연·LCO 모두 같은 부호 관계 — 재작성 (a)-(d) 양쪽 경로 모두 이 부호를 재확인하며 불변.
- 차원: $[\Delta S_{\rxn}/F]=$ J/(mol·K) / (C/mol) = V/K, $[\partial U/\partial T]=$ V/K — 일치.
- 극한: $\Delta H_{\rxn}\to0$ 이면 $U_j\to T\Delta S_{\rxn}/F$(순엔트로피 기원) — 원문·재작성 모두 이 극한을 별도로 안 다루나 결과식 형태상 자명해 추가 서술 불필요(과잉 확장 자제).
- **발견한 결함 없음** — 원 결론(전극무관·미분관계)은 물리적으로 옳고, 문제는 순수히 "결론까지 가는 사슬 부재"였다. 위 ①②가 그 사슬을 흑연 sec:center 와 같은 (a)(b)(c)(d) 밀도로 채운다.

---

## 2. sec:lco-hys 재작성안

### 2.1 삽입 위치
L684-708 (`\subsection{LCO order--disorder 와 MIT 2상역 — 같은 정규용액 틀}\label{sec:lco-hys}` 전체) 교체. 앞(L682-683 그림 hysloop 끝) · 뒤(L709 다음 섹션 sec:width 도입) 불변.

### 2.2 원 줄글 대비 — 무엇이 산문이었나
- L685-687: "그대로 적용된다" — 흑연 sec:hys 의 $\mu(\theta)\to g''\to$spinodal$\to\Delta U_\hys$ 사슬을 LCO 표기로 다시 밟지 않고 결론만 선언.
- L689-694(T2·T3): "정규용액의 $\Omega>0$ ... 상분리의 LCO 사례다"라고만 하고, $\Omega_j>2RT$ 조건·spinodal 식·$\Delta U_\hys$ 박스를 T2/T3 첨자로 재대입한 중간식이 없음("같은 틀 적용" 서술 1회).
- L696-701(T1): "이 구간 역시 식~eq:dUhys·eq:Ubranch 의 spinodal gap·분기 중심을 그대로 받는다"— 재적용 문장뿐, T1 첨자 대입 부재("같은 틀 적용" 서술 2회).
- L703-707(도핑): "$\Omega_j$ 를 $2RT$ 쪽으로 낮춰"라는 정성 서술만 있고, 이것이 식~\eqref{eq:dUhys}·\eqref{eq:xieq} 를 통해 $\Delta U_\hys\downarrow$·$w$(broadening 측)에 어떻게 전파되는지 사슬이 없음("같은 틀 적용" 서술 3회).

### 2.3 재작성 수식 사슬

**① T2·T3 order-disorder — $\mu(\theta)\to g''\to$spinodal$\to\Delta U_\hys$ 사슬을 LCO 첨자로**

> **(a) 출발 — 같은 격자기체 가정, LCO 자리.** \S\ref{sec:hys}(L523-534)의 $\mu(\theta)=\mu^0+RT\ln[\theta/(1-\theta)]+\Omega(1-2\theta)$(식~\eqref{eq:mu})는 "동등한 자리에 리튬이 차고 빈다"는 가정만 쓴다 — 흑연 격자기체 유도(경우의 수 $W$, Stirling 근사, 평균장 초과에너지 $\Omega\theta(1-\theta)$)가 서는 전제는 LCO 의 리튬 자리에도 문자 그대로 성립한다(자리 동등성은 결정 대칭이 주는 가정이지 흑연 특이 가정이 아님). 따라서 T2($x\!\approx\!0.55$)·T3($x\!\approx\!0.48$) 전이에 첨자 $j\in\{\mathrm{T2,T3}\}$ 를 달아 그대로 쓴다:
> \begin{equation}
> \mu_\mathrm{Li}^\mathrm{cat}(\theta_j)=\mu^{0,\mathrm{cat}}+RT\ln\frac{\theta_j}{1-\theta_j}+\Omega_j^\mathrm{cat}(1-2\theta_j),\qquad j\in\{\mathrm{T2,T3}\}.
> \label{eq:lco-mu}
> \end{equation}
>
> **(b) 적용 연산 — $g_j''$, spinodal 문턱을 LCO 첨자로 재대입.** \S\ref{sec:hys}(a)(c)(d)(L535-557)의 $g_j(\xi)\to g_j''(\xi)=RT/[\xi(1-\xi)]-2\Omega_j$(식~\eqref{eq:gpp})와 spinodal 근 $\xi_{s,j}^\pm=\tfrac12(1\pm u_j)$, $u_j=\sqrt{1-2RT/\Omega_j}$(식~\eqref{eq:spinodal})는 유도 과정에 전이 고유 정보를 쓰지 않으므로(오직 $\Omega_j$ 값 하나로만 전이가 들어온다) $j=\mathrm{T2,T3}$ 에 대해 형태 그대로 성립한다:
> \begin{equation}
> g_{\mathrm{T2}}''(\xi)=\frac{RT}{\xi(1-\xi)}-2\Omega_{\mathrm{T2}},\qquad
> g_{\mathrm{T3}}''(\xi)=\frac{RT}{\xi(1-\xi)}-2\Omega_{\mathrm{T3}},
> \label{eq:lco-gpp}
> \end{equation}
> 문턱 조건 $\Omega_{\mathrm{T2}}>2RT$, $\Omega_{\mathrm{T3}}>2RT$ 가 각각 성립해야 두 전이가 상분리(spinodal 실근, 이중웰)로 관측된 hex$\to$monoclinic·monoclinic$\to$hex 좁은 두 peak 를 낳는다 — 이 조건이 "정규용액의 $\Omega>0$ 이 만드는 이중웰"(원문 L690-691)의 정량 근거다.
>
> **(c) 중간식 — 분기 gap $\Delta U_\hys$ 를 T2·T3 로.** 식~\eqref{eq:dUhys} $\Delta U_j^\hys=(2/F)[\Omega_j u_j-2RT\,\mathrm{artanh}\,u_j]$ 유도(두 spinodal 점에서 평형전위 차, L584-619)는 $\Omega_j$ 가 문턱을 넘는 임의 전이에 대해 성립하는 일반식이므로
> \begin{equation}
> \Delta U_{\mathrm{T2}}^\hys=\frac{2}{F}\big[\Omega_{\mathrm{T2}}u_{\mathrm{T2}}-2RT\,\mathrm{artanh}\,u_{\mathrm{T2}}\big],\qquad
> \Delta U_{\mathrm{T3}}^\hys=\frac{2}{F}\big[\Omega_{\mathrm{T3}}u_{\mathrm{T3}}-2RT\,\mathrm{artanh}\,u_{\mathrm{T3}}\big].
> \label{eq:lco-dUhys-t2t3}
> \end{equation}
>
> **(d) 박스 — 분기 중심과 config 엔트로피 출처 연결.**
> \begin{equation}
> \boxed{\;U_j^{\mathrm{cat},d}=U_j^\mathrm{cat}+\tfrac12\sigma_d h_{\eta,j}\gamma_j\,\Delta U_j^\hys,\qquad j\in\{\mathrm{T2,T3}\}\;}
> \label{eq:lco-Ubranch-t2t3}
> \end{equation}
> (식~\eqref{eq:Ubranch} 형태 그대로, LCO 첨자). T2·T3 의 정렬 charge-order 엔트로피 변화($\approx$0.47 J/(mol·K)@$x{=}\tfrac12$, $\approx$1.49 J/(mol·K)@$x{=}\tfrac23$[tier A, Motohashi\cite{motohashi2009}])는 이 $\Omega_j^\mathrm{cat}$(상호작용 *에너지*)가 아니라 표~\ref{tab:lco-staging}·식~\eqref{eq:lco-decomp} 의 $\Delta S_j^\mathrm{config}$(엔트로피 *중심표준값*) 자리로 들어간다 — **두 양은 같은 상전이의 서로 다른 열역학 계수**(하나는 $g_j$ 의 $\Omega_j\xi(1-\xi)$ 항의 에너지 계수, 하나는 $\mu^0$ 근방 로그 몫의 표준 엔트로피 계수)라는 점을 여기서 명시한다(§2.5 논리 감사 참조 — 1차 문헌에 $\Omega_j^\mathrm{cat}$ 자체의 수치는 없음, 갭으로 남김).

**② T1 MIT — 같은 사슬을 T1 첨자로, 전자 자유도 분리 명시**

> **(a) 출발.** T1($x\!\approx\!0.75$--$0.94$)의 절연체$\to$금속 전위 plateau($\sim$3.9 V)도 "리튬이 두 자리(절연체상 조성·금속상 조성)에 나뉘어 앉는" 격자기체로 볼 수 있으므로, 식~\eqref{eq:mu}$\to$\eqref{eq:gpp} 유도가 $j=\mathrm{T1}$ 에도 그대로 선다:
> \begin{equation}
> g_{\mathrm{T1}}''(\xi)=\frac{RT}{\xi(1-\xi)}-2\Omega_{\mathrm{T1}},\qquad \Omega_{\mathrm{T1}}>2RT\ \text{(2상 공존의 문턱)}.
> \label{eq:lco-gpp-t1}
> \end{equation}
>
> **(b) 적용 연산 — 분기 gap.**
> \begin{equation}
> \Delta U_{\mathrm{T1}}^\hys=\frac{2}{F}\big[\Omega_{\mathrm{T1}}u_{\mathrm{T1}}-2RT\,\mathrm{artanh}\,u_{\mathrm{T1}}\big],\qquad u_{\mathrm{T1}}=\sqrt{1-\frac{2RT}{\Omega_{\mathrm{T1}}}}.
> \label{eq:lco-dUhys-t1}
> \end{equation}
>
> **(c) 중간식 — 분기 중심.**
> \begin{equation}
> U_{\mathrm{T1}}^{\mathrm{cat},d}=U_{\mathrm{T1}}^\mathrm{cat}+\tfrac12\sigma_d h_{\eta,\mathrm{T1}}\gamma_{\mathrm{T1}}\,\Delta U_{\mathrm{T1}}^\hys.
> \label{eq:lco-Ubranch-t1}
> \end{equation}
>
> **(d) 박스 — 이중계산 경계(무엇이 이 사슬에 들어오지 않는지).**
> \begin{equation}
> \boxed{\;\text{식~\eqref{eq:lco-gpp-t1}--\eqref{eq:lco-Ubranch-t1} 의 } \Omega_{\mathrm{T1}},\ g_{\mathrm{T1}}''\ \text{은 리튬 \emph{배치} 자유도만 — 전자(전도전자) 자유도는 별도.}}
> \end{equation}
> 이 구조적(배치) 2상 자유에너지 $g_{\mathrm{T1}}(\xi)$ 는 전도 전자의 상태밀도 변화(전자 자유도)를 담지 않는다 — 두 자유도가 \S\ref{sec:lco-decomp}(가법성 정당화, L1707-1715)에서 "근사적으로 직교"(즉 $Z=Z_\mathrm{config}\cdot Z_\mathrm{elec}$)로 다뤄지는 것과 정합하도록, 여기서 $\Omega_{\mathrm{T1}}$·$g_{\mathrm{T1}}''$ 는 config 슬롯 전용임을 명시한다(원문 L699-701 "두 몫을 분리한다는 점만 못박는다"의 수식 근거).

**③ 도핑 보정 — $\Omega_j\downarrow$ 가 $\Delta U_\hys\downarrow$·broadening$\uparrow$ 로 전파되는 사슬**

> **(a) 출발.** Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 격자기체 자유에너지의 상호작용 계수 $\Omega_j$ 를 낮춘다(치환 이온이 리튬-리튬 이웃 인력의 협동성을 흐트림 — 물리적으로 다결정 무질서가 유효 배위를 어지럽혀 평균장 $\Omega$ 를 줄이는 표준 정규용액 도핑 효과).
>
> **(b) 적용 연산 — $u_j$ 를 통한 전파.** 식~\eqref{eq:spinodal} $u_j=\sqrt{1-2RT/\Omega_j}$ 에서 $\Omega_j\downarrow$(단 $\Omega_j>2RT$ 유지)이면 $2RT/\Omega_j\uparrow \Rightarrow u_j\downarrow$.
>
> **(c) 중간식 — $\Delta U_\hys$ 로 전파.** 식~\eqref{eq:dUhys} 는 $u_j\to0$ 극한에서 $\Delta U_j^\hys\to\frac{8RT}{3F}u_j^3\to0$(L621-623 이미 유도된 극한)이므로, $\Omega_j\downarrow\Rightarrow u_j\downarrow\Rightarrow\Delta U_j^\hys\downarrow$ — 도핑이 분기 gap 을 줄인다는 원문 결론이 이 극한식으로 직접 닫힌다.
>
> **(d) 박스 — broadening 쪽 전파(경계 명시).**
> \begin{equation}
> \boxed{\;\Omega_j\ \text{(도핑)}\downarrow\ \Longrightarrow\ u_j\downarrow\ \Longrightarrow\ \Delta U_j^\hys\downarrow\ \text{(식~\eqref{eq:dUhys})}\;,}
> \end{equation}
> 단 $\Omega_j$ 가 여전히 $2RT$ 를 넘는 한(원문 L705 "$2RT$ 쪽으로 낮춰"— 문턱을 넘어선다는 뜻이 아니라 접근한다는 뜻, 재확인) 폭 $w_j$ 는 \S\ref{sec:width} 이중지위의 **두-상 측**(broadening 이 정하는 현상학적 피팅 폭)에 남는다 — $\Omega_j$ 감소가 폭 자체를 식~\eqref{eq:wbase} 로 직접 넓히는 것이 아니라(그 식은 단상측 평형 예측), 분기 gap 축소를 통해 두 branch 가 더 가까이 겹쳐 \S\ref{sec:broadening} 의 broadening 이 차지하는 실효 몫을 키운다는 *간접* 경로다(원문 L705 "broadening 폭이 더 큰 몫을 차지한다"의 정확한 의미 — peak 를 smear 하는 것은 $w_j$ 확대가 아니라 분기 gap 축소로 인한 겹침).

### 2.4 ★two-phase calibration 명시 (지시 18번 요구)
LiC 계열(흑연)의 two-phase calibration(2L→2·2→1 두 전이만 $\Omega>2RT$, 4→3·dilute→4L 은 solid-solution 으로 피팅될 것으로 기대, R1_broadening.md·본문 L738-741)과 달리, **LCO 는 T1·T2·T3 세 전이 모두 $\Omega_j>2RT$ 의 two-phase**다 — 이는 이미 본문 sec:lco-peak(L1209 "LCO 의 세 전이도 모두 $\Omega_j>2RT$ 의 두-상") 에 확정 서술돼 있다. sec:lco-hys 재작성은 이 기존 확정과 정합해야 하므로, 위 ①②의 (a) 단계에서 "T1·T2·T3 세 전이 전부가 이 사슬의 적용 대상"이라는 점을 명시했다(config 값이 있는 T2·T3 만 다루고 T1 을 빠뜨리는 오류를 피함). LCO 는 흑연과 달리 하프셀 세 전이가 전부 강한 1차 상전이(MIT·두 order-disorder)라는 것이 물리적으로도 정합적이다 — 표~\ref{tab:lco-staging} 의 세 전이가 전부 "성격" 열에 상전이(insulator→metal, hex→monoclinic, monoclinic→hex)로 적혀 있어 solid-solution 후보가 애초에 없다.

### 2.5 논리 감사 결과 — **결함 1건 발견 및 수정안 (경계 명시로 해소, 결과식 불변)**

**감사 대상 1 — $\Omega_j$ 수치 대입 가능성.** 지시문은 "Ω_j(T2 order-disorder·T1 MIT)로 실제 대입한 중간식"을 요구한다. 원문·1차 문헌(Motohashi 2009) 어디에도 $\Omega_j^\mathrm{cat}$ 의 **수치**는 없다 — 문헌값은 config 엔트로피 $\Delta S_j^0$(0.47/1.49 J/(mol·K), 표~\ref{tab:lco-staging})뿐이고, 이는 $g_j(\xi)$ 의 로그 몫 표준값이지 $\Omega_j\xi(1-\xi)$ 항의 에너지 계수가 아니다(sec:lco-decomp 이 이 둘을 이미 슬롯으로 분리 — L1704-1706 이중계산 금지). **따라서 "Ω_j 에 숫자를 대입"은 물리적으로 불가능하고(1차 문헌 갭, 허위 정밀 금지 원칙 위배 소지) 시도해서는 안 된다.** 위 재작성 ①②는 이 갭을 얼버무리지 않고 **기호 대입**($\Omega_j\to\Omega_{\mathrm{T1}},\Omega_{\mathrm{T2}},\Omega_{\mathrm{T3}}$)까지만 하고, 박스 (d)에서 "이 $\Omega_j^\mathrm{cat}$ 수치는 갭(피팅 대상)"임을 명시했다 — 이것이 지시문 원칙 1("물리·결과식·부호·수치 원칙 불변")과 원칙 2(신규 개념 도입 금지) 양쪽을 지키는 유일한 정직한 해법이다. 만약 이 감사 없이 임의로 $\Omega_j$ 에 그럴듯한 숫자를 넣었다면 이것이 진짜 논리 결함(허위 정밀)이 됐을 것 — 원문은 애초에 이 함정을 피해 "그대로 적용"이라는 안전한 줄글로 남았던 것이고, 수식화가 이 안전판을 깨지 않도록 §2.3 박스에 갭 표시를 넣었다.

**감사 대상 2 — 부호 사슬.** $\Delta U_j^\hys\ge0$(spinodal 상한), $U_j^{d}$ 방향 부호(방전 $+$, 충전 $-$) 모두 흑연 사슬 그대로 상속 — LCO 특이 부호 반전 없음(확인, 결함 아님).

**감사 대상 3 — 물리 소당성(T1 전자 자유도 분리).** 격자기체 유도(L524-534)의 전제는 "자리 점유 이진 변수"이고 T1 의 전자 자유도(전도전자 밴드 채움)는 이와 다른 자유도라 같은 $\Omega,\theta$ 로 뭉뚱그리면 이중계산 위험이 있다 — 이를 §2.3②(d)에서 명시적으로 분리해 sec:lco-decomp 의 직교성 논증과 다리를 놓았다(원문 L699-701 은 이 분리를 서술만 했고 수식 사슬 쪽에서 "이 사슬이 config 전용"이라는 명시가 없었던 것을 보완).

**감사 대상 4 — 극한.** $\Omega_j\to2RT^+$ 에서 $u_j\to0$, $\Delta U_j^\hys\to\frac{8RT}{3F}u_j^3\to0$(도핑 사슬 (c)에서 재사용) — 흑연 본문(L621-623)의 기존 유도를 그대로 인용, 재유도하지 않음(중복 방지, DRY).

**결론 — 원 물리·결과식·부호 전부 불변.** 발견한 것은 "$\Omega_j$ 수치화 유혹"이라는 잠재 함정이며, 이는 실제 저지르지 않고 갭으로 명시하는 것으로 해소했다(비약 제거이지 결과 변경이 아님).

---

## 3. 요약 (5줄)

1. **sec:lco-center**: "전극무관 논증"을 eq:eqbalance 재적용(반응 항 구조가 화학종명 무관)으로, "$\partial U/\partial T=\Delta S/F$"를 두 독립 경로(직접미분 vs Gibbs 항등식 경유) 교차검증으로 완결해 (a)→(d) 사슬 2건을 신설. 결과식·부호 불변, 기존 verifybox(L490-509)는 그대로 두고 앞에 다리만 놓음.
2. **sec:lco-hys**: 흑연 $\mu(\theta)\to g_j''\to$spinodal$\to\Delta U_\hys\to U_j^d$ 사슬을 T1(MIT)·T2·T3(order-disorder) 세 전이 첨자로 각각 재전개(3개 사슬)했고, 도핑 보정도 $\Omega_j\downarrow\to u_j\downarrow\to\Delta U_j^\hys\downarrow$ 극한식(L621-623 기존식 재사용)으로 닫았다. LCO calibration = T1·T2·T3 **세 전이 모두** $\Omega_j>2RT$(흑연의 "4개 중 2개만 two-phase"와 다른 계, 이미 L1209 확정 — 신규 판정 아님)임을 (a) 단계에 명시.
3. **논리 결함 발견 여부**: 1건 — "$\Omega_j$ 에 수치를 실제 대입"하라는 지시를 문자 그대로 이행하면 1차 문헌에 없는 수치를 지어내는 허위 정밀이 된다. 기호 대입까지만 하고 수치는 갭(round-trip 피팅 대상)으로 명시하는 것으로 해소 — 결과식·물리 변경 없이 잠재 함정만 회피.
4. **물리 불변 확인**: 두 절 모두 결과 박스(eq:lco-Ujbox, eq:lco-dUdT-box, eq:lco-Ubranch-t1/t2t3)가 흑연 대응식과 *형태 동일*(첨자·입력만 LCO); 부호(양극 U 높음, $\partial U/\partial T=\Delta S/F$ 흑연과 1:1, $\Delta U_\hys\ge0$)·차원·극한 전부 원문과 일치, 재작성으로 바뀐 수치·결론 0건.
5. **가장 약했던 원 줄글**: sec:lco-hys L689-694(T2·T3 "정규용액의 $\Omega>0$ ... LCO 사례다")— 세 "같은 틀 적용" 서술 중 유일하게 문헌 수치(config ΔS 0.47/1.49)가 바로 옆에 있는데도 그 수치가 $\Omega_j$ 자리로 들어가는 게 아니라는 구분 없이 병치돼 있어, 독자가 "이 수치를 spinodal 식에 넣으면 되겠다"고 오독할 위험이 가장 컸던 지점(감사 대상 1 로 해소).
