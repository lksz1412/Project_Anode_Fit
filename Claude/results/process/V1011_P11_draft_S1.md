# V1011 Phase 1.1 — LCO 수식화 드래프트 (S1·Sonnet)

> 대상: `docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex` 의 `sec:lco-center`(L470-513, 표제 줄 포함 실측 L470-509)·
> `sec:lco-hys`(L684-708). tex/코드 수정 없음 — 이 문건은 삽입 제안 supplement 다. 정독 완료: 대상 두 절 전문,
> 흑연 forward 대응 절 `sec:pol`(L351-402)·`sec:center`(L404-468, `eq:gibbsdef`~`eq:Uj`)·`sec:hys`(L515-654,
> `eq:mu`~`eq:Ubranch`)·`sec:width`(L710-857, `eq:wbase`)·`sec:broadening`(L1218-1352, two-phase calibration
> 원문·`eq:ensavg`)·`sec:lco-peak`(L1204-1216)·`sec:lco-decomp`(L1690-1727)·`sec:lco-code`(L1740-1765) 전문. SPEC
> `AUTHOR_BRIEF.md`(v9-00) 전문·`R1_broadening.md` 전문·`V1010_LCO_STYLE_REPORT.md` 전문.

---

## 0. 선행 사실 확인 (근거 대조 — 작업 전제)

두 절을 재작성하기 전에, base 프롬프트가 언급한 대입 대상이 실제로 문서 안에 존재하는지 확인했다.

1. **`eq:n0map` 는 문서에 존재하지 않는다.** `grep`으로 전체 tex 를 확인한 결과 `n0map` 문자열은 0건이다. base
   프롬프트 §산출 ②의 "전극무관 논증을 eq:n0map 대입 식으로"는 실제 라벨을 지칭하지 못한다 — 아마 `eq:eqcond`
   (평형 조건, L433-437) 또는 `eq:Uj`(L452-455)를 가리킨 것으로 보인다. 아래 재작성은 실제 존재하는
   `eq:eqcond`→`eq:Uj`→`eq:lco-dUdT` 사슬로 이 논증을 식으로 만든다(근거: L471-476 이 이미 "$\Delta G_j=-FU_j$
   에서 곧장 나온다"고 텍스트로 말하고 있어, 이 문장이 가리키는 식은 `eq:eqcond`).
2. **LCO 의 수치 $\Omega_j$ 는 문서 어디에도 없다.** `Omega`·`0.47`·`1.49` 로 전수 검색한 결과, 표
   `tab:lco-staging`(L336-337)과 `sec:lco-decomp`(L1735)에 있는 $0.47/1.49$ J/(mol·K) 는 **$\Delta S_j^0$(config
   엔트로피)** 값이지 $\Omega_j$(정규용액 상호작용 에너지, 단위 J/mol) 가 아니다 — 서로 다른 물리량이다. `sec:lco-code`
   (L1756)는 `LCO_MSMR_LIT` dict 가 $\Omega$ 키를 가진다고만 말하고 수치는 주지 않는다. 즉 **LCO $\Omega_j$ 의 실제
   수치 대입은 현재 근거 미발견(1차 문헌에 없음, tier 표시 필요)**이다. 아래 (T2·T3)·(T1) 재작성은 이 갭을 숨기지
   않고 — 흑연처럼 수치 하나를 넣는 대신 **기호 $\Omega_j$ 로 대입한 사슬**을 완결하고, "수치는 round-trip 피팅 전
   미정(tier 표시)"임을 명시한다. 이것이 사용자 원칙 ①("물리·결과식·부호 불변, 신규 개념 도입 금지")과 ③("손대지
   말 것: N7-9·전자엔트로피")을 지키면서 근거 없는 수치를 지어내지 않는 유일한 방법이다.

---

## 1. `sec:lco-center` 재작성안 — LCO 평형 중심과 $\partial U_j/\partial T$

### 1.1 삽입 위치
L470-509 전체 교체(표제 `\subsection{LCO 평형 중심과 $\partial U_j/\partial T$ — 양극 부호}\label{sec:lco-center}`
유지, `\begin{verifybox}...\end{verifybox}`(L490-509)는 원문 그대로 보존 — 검산 박스는 이미 수식·수치 사슬이라
현재도 양호하다. 교체 대상은 L471-489 의 줄글 서론 + 반복 서술 부분뿐이다.

### 1.2 원 줄글 (L471-489) 요지
- L471-476: "$U_j(T)$ 는 유도에 전극 가정이 없다 — 평형 조건 식~eqcond 에서 곧장 나오므로 LCO 에도 그대로 성립한다"
  — **단정 비약**: "곧장 나온다"는 서술만 있고, $\Delta G_j=-sFU_j$(전극 무관 도출, `eq:eqcond`)에서 실제로
  대입해 확인하는 식이 없다.
- L477-489: $\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$ 를 "식~Uj 의 $T$ 미분(전극 불문)"이라 괄호
  하나로 처리(`eq:lco-dUdT`, L478-482)하고, 그 뒤 곧바로 수치 스케일(+80 J/(mol·K)) 서술로 넘어간다 — **미분 다리
  자체가 괄호 전보체**다(사용자 지적 그대로).

### 1.3 재작성 수식 사슬

**① 전극무관 논증 — 단정에서 대입 확인으로.**

\textbf{(a) 출발 — 흑연 유도의 전극 의존 지점 점검.} 식~\eqref{eq:eqcond} 의 평형 조건
$$\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U),\qquad \Delta G_j=-sFU_j$$
은 그 유도(L422-437)의 어느 단계에서도 흑연 고유 물질 상수(격자 상수·층간 거리 등)를 쓰지 않았다 — 들어간 것은
(i) 삽입 반응의 일반형 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$, (ii) 전자의 전하수
$z=-1$, (iii) 방전 부호 규약 $s=+1$ 뿐이다. 이 세 입력은 host 가 흑연이든 LCO 든 삽입형 전극이면 공통이다.

\textbf{(b) 적용 연산 — host 를 흑연에서 LCO 로 치환.} 식~\eqref{eq:eqcond} 의 좌변 유도(L422-430)를 다시 쓰되
반응식만 LCO 삽입 반응으로 바꾼다:
$$\mathrm{Li}^++e^-+\mathrm{Li}_{1-x}\mathrm{CoO_2}\;\rightleftharpoons\;\mathrm{Li}_{1-x+\Delta x}\mathrm{CoO_2}$$
— 이 반응도 (i)(ii)(iii) 을 그대로 만족한다(전자수 $z=-1$ 불변, $s=+1$ 규약 불변). 따라서 평형 조건의 대수적 형태
$\tilde\mu_{\mathrm{Li}^+}+\tilde\mu_{e^-}=\tilde\mu_\mathrm{Li}$(식~\eqref{eq:eqbalance})가 치환 후에도 같은 꼴로
성립하고, $-FV$ 항의 계수도 동일하므로 상수 묶음 정의 $sFU\equiv$(비배치 몫)도 같은 자리에서 반복된다.

\textbf{(c) 중간식 — 결과 재확인.} (b)의 치환을 끝까지 밀면 식~\eqref{eq:eqcond}·\eqref{eq:Uj}가 기호 그대로
재도출된다:
$$U_j^\mathrm{cat}(T)=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\,\Delta S_{\rxn,j}^\mathrm{cat}}{F}$$
— 위첨자 cat 만 붙었을 뿐 함수형은 `eq:Uj` 와 항등하다.

\textbf{(d) 박스 — 전극무관 명제의 확인 완료.}
$$\boxed{\;U_j^\mathrm{cat}(T)=\dfrac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\Delta S_{\rxn,j}^\mathrm{cat}}{F}\;,\quad\text{(b)의 host 치환으로 }U_j(T)\text{ 와 동일 함수형 확인}.}$$
바뀐 것은 입력 값 $(\Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat})$ 뿐이다 — 양극의 높은 중심
($\sim$3.9–4.2 V)은 이 식에서 분자 $-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 흑연보다 훨씬 크게 양이라는 **입력 값**의
차이이지, 식의 형태 차이가 아니다.

**② $\partial U_j/\partial T$ — 미분 다리 완결.**

\textbf{(a) 출발 — 식~\eqref{eq:Uj}(또는 위 (d) 박스)를 $T$ 로 미분.} host 에 무관하게
$$U_j(T)=\frac{-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j}}{F}$$
에서 $\Delta H_{\rxn,j},\Delta S_{\rxn,j}$ 는 (근사적으로) $T$ 에 무관한 상수이므로, $T$ 미분은 $T\Delta S_{\rxn,j}/F$
항만 남긴다:
$$\frac{\partial U_j}{\partial T}=\frac{\Delta S_{\rxn,j}}{F}.$$

\textbf{(b) 연산 — Gibbs 항등식과의 일치 확인(독립 경로).} 이 결과가 우연이 아님을 Gibbs 항등식으로 교차 검증한다.
자유에너지 전미분 $\dd G=-S\dd T+V\dd P+\mu\dd n$(등압)에서 $\big(\partial G/\partial T\big)_{P,n}=-S$이고, 반응
자유에너지에도 같은 관계 $\big(\partial\Delta G_j/\partial T\big)_P=-\Delta S_{\rxn,j}$가 성립한다. 식~\eqref{eq:eqcond}
의 $\Delta G_j=-FU_j$($s=1$)를 이 관계에 대입하면
$$\frac{\partial(-FU_j)}{\partial T}=-\Delta S_{\rxn,j}\quad\Longrightarrow\quad \frac{\partial U_j}{\partial T}=\frac{\Delta S_{\rxn,j}}{F}$$
— (a)의 직접 미분과 **독립적으로 같은 식에 도달**한다(하나는 $U_j(T)$ 의 명시적 함수형을 미분, 다른 하나는 Gibbs
항등식을 경유 — 두 경로가 일치하는 것이 이 관계가 임의 대수 조작이 아니라 열역학 항등식임을 보증한다).

\textbf{(c) 중간식 — cat 위첨자 부착(LCO 특화 대입).} ①의 host 치환 논증을 그대로 적용하면
$$\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.$$

\textbf{(d) 박스.}
$$\boxed{\;\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}\;.}$$
(식 번호는 편입 시 기존 `eq:lco-dUdT` 를 그대로 쓴다 — 결과식 불변, 유도만 (a)(b) 두 경로로 보강.)

이후 L483-509(부호·크기 sanity, verifybox)는 원문 유지 — 이미 수치 대입("$\Delta S_\rxn\approx+80$ J/(mol·K)")과
검산이 있는 부분이라 수식화 대상이 아니다.

### 1.4 논리 감사 결과 — `sec:lco-center`

- **G-derive**: (a)(b)(c)(d) 전 단계에 점프 없음. ①은 host 치환의 "무엇이 바뀌고 무엇이 안 바뀌는지"를 (i)(ii)(iii)
  세 입력으로 명시해 "곧장 나온다"는 단정을 검증 가능한 단계로 바꿨다.
- **부호 사슬**: $\Delta G_j=-sFU_j$ 에서 $s=+1$(방전 규약) 그대로 사용 — LCO 도 리튬화가 방전이므로 부호 규약
  전환 없음(L304-305 의 "방전=LCO 리튬화" 규약과 정합). $\partial U/\partial T=\Delta S/F$ 관계의 부호는 흑연·LCO
  동일 — 값의 부호만 다르다(흑연 $\Delta S_\rxn$ 은 전이별 $\pm$, LCO 는 verifybox 스케일에서 $+80$).
- **물리 소당성**: 두 독립 경로(직접 미분 vs Gibbs 항등식 경유)가 같은 결과에 도달 — 이는 결함 발견이 아니라
  **원 결과가 열역학적으로 견고함의 확인**이다. 극한 확인: $\Delta S_\rxn\to0$ 이면 $\partial U/\partial T\to0$(중심이
  온도에 안 움직임) — 물리적으로 타당(엔트로피 변화 없는 반응은 온도로 전위가 안 밀린다).
- **논리 결함 여부**: **무결**. 원 줄글의 결론(전극무관·미분 관계)은 옳다 — 문제는 그 결론에 이르는 **다리가
  생략**된 것이었지 결론 자체의 오류가 아니다. 따라서 이 절은 "결함 수정"이 아니라 "다리 보완"에 해당한다.
- **G-usable 확인**: 위 사슬만으로 독자가 임의 host 의 $U_j(T)$ 를 $(\Delta H_{\rxn,j},\Delta S_{\rxn,j})$ 로부터
  직접 산출 가능(AUTHOR_BRIEF 의 "이 문건으로 LCO ∂U/∂T 산출 가능" 요건 충족).

---

## 2. `sec:lco-hys` 재작성안 — LCO order-disorder/MIT 정규용액

### 2.1 삽입 위치
L684-708 전체 교체(표제 `\subsection{LCO order--disorder 와 MIT 2상역 — 같은 정규용액 틀}\label{sec:lco-hys}` 유지).

### 2.2 원 줄글 요지 (사용자 지적과 일치 확인)
- L685-687: "같은 정규용액 틀이 그대로 적용된다" — 적용 선언 1회째.
- L689-694: (T2·T3) "$\Omega>0$ 이 만드는 상분리의 LCO 사례" — 적용 선언 2회째, 수치는 config 엔트로피
  ($0.47$/$1.49$ J/K·mol)만 인용하고 $\Omega_j$ 대입 없음.
- L696-701: (T1 MIT) "이 구간 역시 식~dUhys·Ubranch 의 spinodal gap·분기 중심을 그대로 받는다" — 적용 선언 3회째.
- L703-707: (도핑) "$\Omega_j$ 를 $2RT$ 쪽으로 낮춰" — 정성 서술.

세 번의 "그대로 적용/그대로 받는다"가 실제 대입 중간식 없이 반복된다는 사용자 지적이 본문 대조로 확인된다.

### 2.3 재작성 수식 사슬

**서론 (변경 없음, L685-688 유지)** — 격자기체 가정이 전극 무관임을 다시 서술하는 도입 문장은 정상이므로 보존.

**(T2·T3) order-disorder — $\Omega_j$ 대입 사슬.**

\textbf{(a) 출발 — 흑연 사슬 재호출.} \S\ref{sec:hys} 에서 세운 사슬은 식~\eqref{eq:mu}(격자기체 $\mu(\theta)$)
→ 식~\eqref{eq:gxi}($g_j(\xi)$) → 식~\eqref{eq:gpp}($g_j''$) → 식~\eqref{eq:spinodal}($\xi_{s,j}^\pm$) →
식~\eqref{eq:dUhys}($\Delta U_j^\hys$) → 식~\eqref{eq:Ubranch}($U_j^{\,d}$) 로 닫혔다. 이 사슬의 유일한 전이별
입력은 상호작용 에너지 $\Omega_j$ 하나다(다른 전부는 $T,R,F$ 등 보편 상수). LCO T2·T3 전이에 이 사슬을 적용한다는
것은 **$\Omega_j$ 자리에 $\Omega_j^{T2},\Omega_j^{T3}$(order-disorder 상호작용 에너지)를 대입해 같은 다섯 식을
다시 읽는 것**이다.

\textbf{(b) 적용 연산 — 대입.} 식~\eqref{eq:spinodal}에 $\Omega_j\to\Omega_j^{T2}$(또는 $T3$)를 대입하면
$$\xi_{s,T2}^\pm=\tfrac12\big(1\pm u_{T2}\big),\qquad u_{T2}=\sqrt{1-\frac{2RT}{\Omega_j^{T2}}}\qquad(\Omega_j^{T2}>2RT),$$
T3 도 동형으로 $u_{T3}=\sqrt{1-2RT/\Omega_j^{T3}}$. 식~\eqref{eq:dUhys}에 같은 대입을 넣으면
$$\Delta U_{T2}^\hys=\frac{2}{F}\Big[\Omega_j^{T2}u_{T2}-2RT\,\mathrm{artanh}\,u_{T2}\Big],\qquad
\Delta U_{T3}^\hys=\frac{2}{F}\Big[\Omega_j^{T3}u_{T3}-2RT\,\mathrm{artanh}\,u_{T3}\Big].$$

\textbf{(c) 중간식 — 분기 중심.} 식~\eqref{eq:Ubranch}에 위 두 gap 을 넣으면 T2·T3 각각의 방향별 분기 중심이 닫힌다:
$$U_{T2}^{\,d}=U_{T2}+\tfrac12\sigma_d h_{\eta,T2}\gamma_{T2}\,\Delta U_{T2}^\hys,\qquad
U_{T3}^{\,d}=U_{T3}+\tfrac12\sigma_d h_{\eta,T3}\gamma_{T3}\,\Delta U_{T3}^\hys.$$

\textbf{(d) 박스 — LCO T2·T3 대입 완결.}
$$\boxed{\;U_{Tk}^{\,d}=U_{Tk}+\tfrac12\sigma_d h_{\eta,Tk}\gamma_{Tk}\,\frac{2}{F}\Big[\Omega_j^{Tk}u_{Tk}-2RT\,\mathrm{artanh}\,u_{Tk}\Big],\quad k\in\{T2,T3\},\quad u_{Tk}=\sqrt{1-\tfrac{2RT}{\Omega_j^{Tk}}}\;.}$$

★**수치 갭 명시(허위 정밀 금지)**: 위 사슬은 $\Omega_j^{T2},\Omega_j^{T3}$ 를 대수 기호로 닫았을 뿐, 그 **수치는
현재 1차 문헌에 없다**(표~\ref{tab:lco-staging}·L1735 은 $\Omega_j$ 가 아니라 config 엔트로피 $\Delta S_j^0\approx
0.47/1.49$ J/(mol·K) 만 제공 — 서로 다른 물리량이다, \S0.2 확인). 코드 dict `LCO_MSMR_LIT` 은 $\Omega$ 키를 갖는
구조이나(L1756) 초기 수치는 round-trip 피팅 전 tier-C 추정으로 남는다 — 흑연이 `GRAPHITE_STAGING_LIT` 의 $\Omega_j$
초기값을 피팅으로 override 하는 것과 동일한 절차가 LCO 에도 필요하다는 점을 이 사슬이 명시적으로 드러낸다(원
줄글은 이 갭을 "그대로 적용된다"는 문장 뒤로 숨겼다 — 사슬을 실제로 쓰면 갭이 드러난다).

\textbf{★two-phase calibration 명시(사용자 요구 사항).} \S\ref{sec:broadening}(a)(L1226-1237)의 calibration —
"흑연 4 staging 전이 중 실제 2상(=$\Omega_j>2RT$ 유지)은 $2\mathrm L\to2$($\mathrm{LiC_{12}}$)·$2\to1$
($\mathrm{LiC_6}$) 둘뿐이고, dilute$\to$stage4·$4\mathrm L\leftrightarrow3\mathrm L$ 은 피팅 후 $\Omega_j<2RT$
로 내려가 solid-solution 이 될 것으로 기대된다" — 를 LCO 에 옮기면: **LCO 세 전이(T1 MIT·T2·T3 order-disorder)는
전부 실측 전위 plateau 를 보이는 1차 상전이**이므로(L313-314 "코인 하프셀은 세 전이를 남긴다"·L689-696 각 전이의
결정학적 상변화 서술 — hex↔monoclinic 초격자·절연체↔금속), 흑연과 달리 **셋 다 계산 결과가 아니라 실험적으로
이미 2상(plateau)으로 관측된 전이**다. 곧 LCO 의 "어느 전이가 정규용액 two-phase 인가"의 calibration 은 흑연처럼
피팅으로 갈리는 것이 아니라 **입력 단계에서 이미 셋 다 $\Omega_j>2RT$ 로 고정**된다(L1209 "LCO 의 세 전이도 모두
$\Omega_j>2RT$ 의 두-상"과 정합). 흑연의 "4개 중 2개만 진짜 two-phase" 라는 구분이 LCO 에는 **적용되지 않는다** —
LCO 는 세 전이 전부가 그 구분에서 "2상" 쪽에 속한다(전이 개수 자체가 다르고, 넷 중 갈라지는 흑연과 달리 LCO 는
애초에 골라낸 세 전이가 전부 1차상전이이기 때문). 이 차이를 명시하지 않으면 독자가 흑연의 "4개 중 2개" 비율을
LCO 에 유추 적용하는 오독이 생길 수 있다.

**(T1) MIT 2상역 — 같은 사슬 + 전자 자유도 분리 명시.**

\textbf{(a) 출발.} T1 MIT 도 (T2·T3)와 같은 격자기체 상분리 사슬을 따르므로, $\Omega_j\to\Omega_j^{T1}$(MIT
config 상호작용) 대입으로 동일하게 닫힌다:
$$u_{T1}=\sqrt{1-\frac{2RT}{\Omega_j^{T1}}},\qquad \Delta U_{T1}^\hys=\frac{2}{F}\Big[\Omega_j^{T1}u_{T1}-2RT\,\mathrm{artanh}\,u_{T1}\Big],\qquad \Omega_j^{T1}>2RT.$$

\textbf{(b) 연산 — 분기 중심.}
$$U_{T1}^{\,d}=U_{T1}+\tfrac12\sigma_d h_{\eta,T1}\gamma_{T1}\,\Delta U_{T1}^\hys.$$

\textbf{(c) 중간식 — 이 사슬이 담지 \emph{않는} 것.} 식 (a)(b)의 $\Delta U_{T1}^\hys,U_{T1}^{\,d}$ 는 **config
자유도(리튬 자리 점유 배열)만의 spinodal gap** 이다. MIT 는 여기에 더해 전도 전자의 상태밀도 변화(전자 자유도)가
있으나, 그 항은 이 정규용액 사슬 \emph{안}에 있지 않다 — \S\ref{sec:lco-electronic}·\S\ref{sec:lco-decomp}
(식~\eqref{eq:lco-decomp})의 별도 슬롯 $\Delta S_{e,1}$ 로 들어가며, 그 슬롯은 $U_{T1}(T)$ 의 **평형 중심**(분기
전, \S\ref{sec:lco-center})에 더해지지 이 히스테리시스 gap $\Delta U_{T1}^\hys$ 식에는 나타나지 않는다.

\textbf{(d) 박스 — 두 몫의 경계 명시.}
$$\boxed{\;U_{T1}^{\,d}=\underbrace{U_{T1}+\tfrac12\sigma_d h_{\eta,T1}\gamma_{T1}\,\Delta U_{T1}^\hys(\Omega_j^{T1})}_{\text{config 자유도(이 절, spinodal gap)}}\;,\qquad U_{T1}=U_{T1}(T;\Delta S_{\rxn,1}^\mathrm{cat}=\Delta S^\mathrm{config}_1+\Delta S^\mathrm{vib}_1+\Delta S_{e,1})\;.}$$
즉 전자 엔트로피 $\Delta S_{e,1}$ 는 $U_{T1}$ 자체(분기 이전 평형 중심, 식~\eqref{eq:lco-decomp})의 입력에 들어가고,
$\Delta U_{T1}^\hys$ 는 그 위에 얹히는 별도의 config 전용 gap 이다 — 이 경계가 sec:lco-decomp 의 "이중계산 방지(B)"
규칙과 정확히 같은 경계선이며(원 줄글 L700-701 "구조적 2상역은 정규용액 틀로, 전자 자유도는 별도 항으로"가 말하려던
바를 식으로 명시한 것), 이 재작성은 그 서술을 대체하지 않고 식으로 뒷받침한다.

**도핑 보정 — 정성 서술을 $\Omega_j$ 이동으로 수식화.**

원 줄글(L703-707)은 이미 "$\Omega_j$ 를 $2RT$ 쪽으로 낮춘다"는 방향은 정확히 말하고 있으나 정량화가 없다. 최소
수식 다리를 추가한다.

\textbf{(a) 출발.} 도핑 전(pure-LCO) 상호작용 에너지를 $\Omega_j^{(0)}$, 도핑 후를 $\Omega_j^\mathrm{dop}$ 라 하면
도핑 억제 효과는
$$\Omega_j^\mathrm{dop}=\Omega_j^{(0)}-\delta\Omega_j(c_\mathrm{dop}),\qquad \delta\Omega_j\ge0,$$
로 적을 수 있다($c_\mathrm{dop}$ = Al/Mg 치환 분율, $\delta\Omega_j$ 는 억제 크기 — 함수형은 미정, tier C).
\textbf{(b) 연산 — spinodal gap 으로 전파.} 식~\eqref{eq:dUhys}에 $\Omega_j\to\Omega_j^\mathrm{dop}$ 를 넣으면
$u_j^\mathrm{dop}=\sqrt{1-2RT/\Omega_j^\mathrm{dop}}<u_j^{(0)}$(같은 $T$ 에서 $\Omega$ 가 작을수록 $u$ 가 작다),
따라서 $\Delta U_j^{\hys,\mathrm{dop}}<\Delta U_j^{\hys,(0)}$ — gap 감소가 정량적으로 뒤따른다. \textbf{(c) 중간식
— 문턱 접근.} $\Omega_j^\mathrm{dop}\to2RT^+$ 이면 \S\ref{sec:hys}(d) 의 극한식(Taylor 전개, L622-623)이 그대로
적용되어 $\Delta U_j^{\hys,\mathrm{dop}}\to\frac{8RT}{3F}(u_j^\mathrm{dop})^3\to0$ — 히스가 매끄럽게 사라진다.
\textbf{(d) 박스 — 도핑 극한과 폭 이관.}
$$\boxed{\;\Omega_j^\mathrm{dop}\downarrow 2RT\;\Longrightarrow\;\Delta U_j^\hys\downarrow0\;(\text{동일 식~\eqref{eq:dUhys}, 입력만 이동})\;,}$$
$\Omega_j^\mathrm{dop}$ 이 $2RT$ 에 가까워질수록(문턱 접근) 코드 분기(`if Omega<=2RT: return 0.0`, L556-557)의
문턱을 넘나들 수 있고, 그러면 그 전이는 \S\ref{sec:width} 의 폭 이중지위에서 **둘째(현상학적 broadening) 지위에서
첫째(평형 예측) 지위로 이동**한다 — 이는 원 줄글이 말한 "polaron peak 를 smear 하고 $U_j$ 를 shift"의 정량적
근거(gap 자체가 좁아지고, 그 경계 근처에서는 폭 지위 전환까지 가능하다는 것)이다.

### 2.4 논리 감사 결과 — `sec:lco-hys`

- **G-derive**: (T2·T3)·(T1)·도핑 세 블록 모두 (a)→(b)→(c)→(d) 완결. 흑연 사슬의 다섯 식(`eq:mu`~`eq:Ubranch`)에
  기호 대입만 했으므로 물리·부호·형태는 원문과 항등(불변 원칙 ① 충족) — 새 물리·새 개념(예: ρ 분포, PSD)는
  도입하지 않음(원칙 ②).
- **부호 사슬**: $\Omega_j>2RT$ 문턱·$u_j$ 실수 조건·$\Delta U_j^\hys\ge0$·$\sigma_d$ 방향 부호 전부 흑연과 1:1
  유지(위첨자 T1/T2/T3 만 부착) — 부호 반전·계수 변경 없음.
- **물리 소당성 — 진짜 결함 발견**: 원 줄글 3회 반복된 "같은 틀 그대로 적용된다"는 서술 자체는 **정성적으로는
  옳다**(격자기체 가정이 전극 물질에 의존하지 않는다는 것은 사실). 다만 실제로 사슬을 끝까지 대입해보면(위 (T2·T3)
  박스) **LCO 의 $\Omega_j$ 수치가 문서 어디에도 없다**는 것이 드러난다 — 이것은 원 서술의 "논리 오류"가 아니라
  "생략으로 가려진 데이터 갭"이다(§0.2). 사용자가 지적한 "논리 소당성 감사" 기준으로 분류하면: 이는 비약(스타일
  문제)이지 오류(물리적으로 틀린 명제)는 아니다 — "그대로 적용된다"는 명제 자체는 참이며, 수식화 과정에서 갭이
  드러났을 뿐 결과식이 틀린 것은 아니다.
- **two-phase calibration 불일치 소지 확인**: 원 줄글 L686-687("$\Omega_j$ 의 값만 LCO 의 상전이가 정한다")과
  L1209(broadening 절, "LCO 의 세 전이도 모두 $\Omega_j>2RT$")은 **서로 모순되지 않는다** — 하나는 sec:lco-hys
  에서 정성적 개괄, 다른 하나는 sec:broadening 에서 확정 진술이다. 다만 sec:lco-hys 본문에는 "흑연은 4개 중
  2개만 two-phase인데 LCO 는 3개 다 two-phase"라는 **대비가 명시돼 있지 않아** 독자가 흑연 calibration
  비율(4개 중 2개)을 LCO 에 그대로 유추할 위험이 있다 — 이것도 물리 오류는 아니고 **누락으로 인한 오독 소지**다.
  위 재작성의 "★two-phase calibration 명시" 문단이 이 갭을 닫는다.
- **결론**: **논리 결함 없음(무결)**. 발견된 것은 (i) 수치 갭(1차 문헌 부재, tier 로 해결) (ii) 대비 누락(오독
  소지, 문장 추가로 해결) 두 가지이며, 둘 다 "비약"이지 "오류"가 아니다. 원 결과식·부호·물리는 완전히 보존된다.

---

## 3. 요약 — 5줄

1. **center**: "전극무관 곧장 나온다" 단정을 host-치환 (a)→(d) 사슬로, $\partial U/\partial T=\Delta S/F$ 를
   직접미분+Gibbs 항등식 두 독립 경로로 검증하는 사슬로 재작성 — 결과식 `eq:lco-dUdT` 불변.
2. **hys**: 흑연 5식 사슬(`eq:mu`→`eq:Ubranch`)을 T1/T2/T3 각각에 $\Omega_j^{Tk}$ 기호 대입한 (a)→(d) 사슬로,
   MIT 는 config-전자 두 슬롯 경계를 박스로 명시, 도핑은 $\Omega_j^\mathrm{dop}\to2RT$ 극한 사슬로 정량화.
3. **논리 결함**: 발견 안 됨(원 결론·부호·결과식 전부 참이고 보존됨). 발견된 것은 두 갭 — (i) LCO $\Omega_j$
   수치 1차 문헌 부재(tier-C, round-trip 피팅 전제로 명시) (ii) "흑연 4개 중 2개만 two-phase" 대비가 LCO 절
   본문에 없어 오독 소지(대비 문장 추가로 해결) — 둘 다 결함이 아니라 누락.
4. **물리 불변 확인**: $\Omega_j>2RT$ 문턱·$u_j$ 정의·$\Delta U_j^\hys$ 부호·$U_j^{\,d}$ 방향 부호·전자-config
   가법성 경계 전부 원문과 항등. 신규 물리·신규 개념(ρ 분포·PSD·새 상호작용 항) 도입 없음.
5. **가장 약했던 원 줄글**: sec:lco-hys 의 (T2·T3) 블록(L689-694) — "같은 틀 적용"이라 선언만 하고 $\Omega_j$
   수치도 대입 중간식도 전혀 없어, 사슬을 실제로 펼쳐보기 전까지는 수치 갭(§0.2)이 숨어 있었다. center 의
   L477-482(미분 다리 괄호 전보체)가 근소한 차이로 그다음.
