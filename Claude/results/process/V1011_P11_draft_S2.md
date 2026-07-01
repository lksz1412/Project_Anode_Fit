# V1011 Phase 1.1 — LCO 수식화 드래프트 (S2/Sonnet)

> 독립 작성. tex/코드 수정 없음 — 편입은 master 판단. 대상: `docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex`
> `sec:lco-center`(L470-513) · `sec:lco-hys`(L684-708, N3 절 내부) 두 절의 줄글 결론을 흑연 forward 식
> (a)출발→(b)연산→(c)중간식→(d)박스 사슬로 재작성. 물리·결과식·부호·수치는 **불변** — 전개 형식만 바꾼다.
> 각 항목에 논리 감사(무결 or 결함+근거)를 병기한다.

---

## 0. 정독 확인 (근거 없는 작업 금지)

전문 정독한 범위와 그 안에서 이번 작업에 실제로 쓴 지점:

- `graphite_ica_ch1_v1.0.11.tex` L1-120(전문·매크로), L180-350(N0 표기·`eq:n0map`·`sec:lco-map`),
  L350-932(N1 분극 → N2 평형중심 `sec:center`/`sec:lco-center` → N3 히스 `sec:hys`/`sec:lco-hys` →
  N4/N5 폭·`sec:width`/`sec:dist`), L933-950(N5+ 전자엔트로피 도입부, 손대지 않음 확인용),
  L1195-1240(`sec:lco-peak`·`sec:broadening` 도입, 인접 경계 확인용), L1685-1765(`sec:lco-decomp`·
  `sec:lco-code`, 전방 참조 대상 확인용).
- `results/process/V1010_LCO_STYLE_REPORT.md` 전문 — 표1의 "필요한 수식 사슬" 컬럼이 이 드래프트의
  산출 명세.
- `results/builds/v9/v9-00_spine/AUTHOR_BRIEF.md` 전문 — LCO 전이표(T1/T2/T3 tier A Xia)·전자 엔트로피
  파생·ΔS 분해·G-derive/G-follow/G-usable 렌즈.
- `results/builds/ch1v10/review1/R1_broadening.md` 전문 — two-phase calibration(그래파이트 4건 중 2건만
  LiC₁₂·LiC₆), Ω 초기값="거친 추정" 명시 요건, size 절제 원칙.

핵심 사전 확인 사항(추정 방지):
1. **LCO Ω_j 수치는 문건 어디에도 없다** (`\Omega_j` 전수 grep, L235/517-741/1209-1232 전부 확인) —
   있는 것은 config 엔트로피 초기값(T2 ≈0.47, T3 ≈1.49 J/K·mol, Motohashi tier A)과 정성 서술
   "LCO 세 전이 모두 Ω_j>2RT 두-상"(L686-687, L1209)뿐이다. 따라서 아래 (c) LCO-hys 사슬은 **Ω_j를
   기호로 유지**하고 대입은 구조적(문턱 부등식 확인)까지만 하며, 수치 대입을 지어내지 않는다.
2. **LCO의 "two-phase" 계열**: 그래파이트는 4 전이 중 2개(LiC₁₂·LiC₆)만 Ω>2RT, 나머지 2개는
   solid-solution(Ω≤2RT)로 피팅될 것으로 기대된다(L738-741, R1_broadening.md calibration). LCO는
   이와 달리 **세 전이(T1 MIT·T2·T3 order-disorder) 전부가 Ω_j>2RT 두-상**이라고 이미 명시돼 있다
   (L686-687 "LCO 에서 Ω_j>2RT 의 상분리(따라서 2상 plateau·히스테리시스)를 낳는 자리는 표의 세 전이
   모두에 대응", L1209 "LCO 의 세 전이도 모두 Ω_j>2RT 의 두-상"). 이 드래프트는 이 기존 calibration을
   뒤집지 않고, sec:lco-hys 안에서 그 근거(문턱 부등식 자체)를 수식으로 보이는 데 그친다.

---

## 1. sec:lco-center (L470-513) 재작성안

### 1.1 원 줄글 (현재, 요지)

- L471-476: "*식~\eqref{eq:Uj} 는 유도에 전극 가정이 없다 — 평형 조건 식~\eqref{eq:eqcond}에서 곧장
  나오므로 LCO 양극에도 그대로 성립한다.*" → 단정 비약. 흑연 유도(§sec:center)가 어디서 전극-무관성을
  얻는지 **식으로 짚지 않고** 결론만 말한다.
- L477-482: "*온도 의존도 같은 미분이다: ∂U_j/∂T = ΔS_rxn,j^cat/F (식 eq:Uj 의 T 미분, 전극 불문).*" →
  괄호 안에 "Gibbs 항등식과 잇는 것과 같다"는 다리가 흑연 쪽 §sec:center 말미(L458-459)에는 있지만,
  LCO 쪽은 그 다리를 **재현하지 않고 결과만** 적는다. 미분 자체가 눈앞에서 일어나지 않는다(점프).

V1010_LCO_STYLE_REPORT.md 표의 요구: "ΔG=−sFU→∂U/∂T=ΔS/F 다리 문장 + (a→d)", "전극무관 논증을
eq:n0map 대입 식으로(단정 비약 제거)".

### 1.2 논리 소당성 감사 — 원 논증이 실제로 유효한가

**감사 결과: 결론(전극무관성)은 참이나, 그 근거 제시가 생략(비약)이지 결함은 아니다.** 검증:

식~\eqref{eq:eqcond}($\Delta G_j=-sFU_j$)와 식~\eqref{eq:Ujmid}--\eqref{eq:Uj}의 유도 경로(§sec:center
(a)(b)(c)(d))를 다시 추적하면, 전극 고유량이 들어오는 지점은 오직 **입력값** $(\Delta H_{\rxn,j},
\Delta S_{\rxn,j})$뿐이다 — 유도 중 어느 단계도 "이 반응이 흑연이다"라는 가정을 쓰지 않는다(Gibbs 정의
eq:gibbsdef, 화학퍼텐셜 정의 eq:mudef, 전기화학평형 eq:eqbalance 모두 반응 종에 무관한 일반 열역학
항등식이다). 따라서 "유도에 전극 가정이 없다"는 원문의 주장은 **참**이며 물리적으로 건전하다 — 수정할
결함이 아니라, 그 참임을 **어느 단계에서 확인되는지 식으로 짚지 않은 서술 결핍**이다. 아래 재작성은
이 결핍만 메운다(물리·결론 불변).

### 1.3 재작성 수식 사슬

**삽입 위치**: L470-482 (부제 "LCO 평형 중심과 ∂U_j/∂T — 양극 부호" 첫 두 단락, `\begin{verifybox}`
이전까지). L483 이후(전자항 관련 forward-ref, config/vib/elec 분해 언급)는 그대로 유지.

---

**(a) 출발 — 흑연 유도의 전극-의존 지점 특정.**
§sec:center의 평형 조건 유도(식~\eqref{eq:eqcond})를 다시 적으면

$$
\mu_\mathrm{Li}(\theta_\eq) = \mu^0 - sF(V-U), \qquad \Delta G_j = -sF\,U_j,
$$

이고, 이 등식이 서는 데 쓰인 것은 (i) Gibbs 정의 $G\equiv H-TS$(식~\eqref{eq:gibbsdef}), (ii) 화학퍼텐셜
정의 $\mu\equiv\partial G/\partial n|_{T,P}$(식~\eqref{eq:mudef}), (iii) 전기화학 평형 조건
$\tilde\mu_{\mathrm{Li}^+}+\tilde\mu_{e^-}=\tilde\mu_\mathrm{Li}$(식~\eqref{eq:eqbalance}) 셋뿐이다.
이 셋 중 어느 것도 흑연 삽입 반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_\text{(흑연)}$의
$[\,]$(빈 격자자리)가 무엇인지 지정하지 않는다 — LCO 삽입 반응
$\mathrm{Li}^++e^-+\mathrm{Li}_{1-x}\mathrm{CoO_2}\rightleftharpoons\mathrm{Li}_{1-x+\delta}\mathrm{CoO_2}$로
바꿔 써도 (i)(ii)(iii) 전개는 기호 하나 바뀌지 않는다 — 자리 $[\,]$가 흑연 층간 갤러리든 LCO 팔면체
자리든, $\delta G=[\tilde\mu_\mathrm{Li}-\tilde\mu_{\mathrm{Li}^+}-\tilde\mu_{e^-}]\,\dd n=0$라는 조건문
자체는 반응물 정체와 무관한 일반 평형 조건이기 때문이다.

**(b) 연산 — 전극 고유량이 들어오는 유일한 자리 확인.**
식~\eqref{eq:Ujmid}의 $\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}=-FU_j$를 다시 보면, 좌변의
$(\Delta H_{\rxn,j},\Delta S_{\rxn,j})$가 유일하게 물질 고유 정보를 담은 자리다 — 이들은 (i)(ii)(iii)의
유도 과정에서 오지 않고, "이 반응이 무엇인가"(흑연 삽입 vs LCO 삽입)라는 **입력**에서 온다. 대수적으로,
같은 식 $U_j=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F$ (식~\eqref{eq:Uj})에 위첨자를 달아 전극별로
구분하면

$$
U_j^{\mathrm{an}}(T)=\frac{-\Delta H_{\rxn,j}^{\mathrm{an}}+T\Delta S_{\rxn,j}^{\mathrm{an}}}{F},
\qquad
U_j^{\mathrm{cat}}(T)=\frac{-\Delta H_{\rxn,j}^{\mathrm{cat}}+T\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}
$$

— **같은 함수형**(같은 $F$-분모, 같은 부호 구조), **다른 인자값**뿐이다. 이것이 "유도에 전극 가정이
없다"는 서술의 식으로 확인된 형태다.

**(c) 중간식 — 부호·크기 비교로 값의 차이를 특정.**
$U_j^\mathrm{cat}\sim3.9$--$4.2$ V(양극, 표~\ref{tab:lco-staging})와 $U_j^\mathrm{an}\sim0.085$--$0.21$ V
(음극, 표~\ref{tab:staging})의 차는 함수형이 아니라 $-\Delta H_{\rxn,j}$ 크기에서 온다: LCO 삽입 반응이
흑연 삽입보다 발열이 훨씬 크므로($-\Delta H_{\rxn,j}^\mathrm{cat}\gg-\Delta H_{\rxn,j}^\mathrm{an}>0$)
분자가 커져 $U_j^\mathrm{cat}\gg U_j^\mathrm{an}$가 된다 — 식~\eqref{eq:Uj}를 $T\to0$ 극한(가장 단순한
검산)에 두면 $U_j\to-\Delta H_{\rxn,j}/F$로 순수히 엔탈피 항만 남아 이 크기 비교가 그대로 보존됨을
확인할 수 있다.

**(d) 박스 — 전극-무관 함수형.**
$$
\boxed{\;U_j^{\,e}(T)=\frac{-\Delta H_{\rxn,j}^{\,e}+T\,\Delta S_{\rxn,j}^{\,e}}{F}\;,\qquad e\in\{\mathrm{an,cat}\}\;}
$$
— 식~\eqref{eq:Uj}와 동일한 식에 전극 위첨자 $e$만 단 것. 유도 경로(a)(b)(c)가 이 위첨자를 어디에도
요구하지 않았다는 것 자체가 "전극-무관"의 수식적 의미다.

**온도 미분 다리 — Gibbs 항등식과 잇기(L477-482 보완).**

**(a) 출발.** Gibbs 항등식 $\left(\dfrac{\partial \Delta G}{\partial T}\right)_P=-\Delta S$(임의의 반응
자유에너지에 대해 항상 성립하는 열역학 항등식, Maxwell 관계에서 옴).

**(b) 연산 — 식~\eqref{eq:eqcond}의 $\Delta G_j=-sFU_j$($s=+1$)를 온도로 미분.**
좌변은 Gibbs 항등식으로 $\partial\Delta G_j/\partial T=-\Delta S_{\rxn,j}$, 우변은 $U_j$가 유일한
$T$-의존 변수이므로 $\partial(-FU_j)/\partial T=-F\,\partial U_j/\partial T$.

**(c) 중간식 — 두 표현을 등치.**
$$
-\Delta S_{\rxn,j}=-F\,\frac{\partial U_j}{\partial T}
\quad\Longrightarrow\quad
\frac{\partial U_j}{\partial T}=\frac{\Delta S_{\rxn,j}}{F}.
$$
(직접 미분 검산: 식~\eqref{eq:Uj}의 $U_j=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F$를 $T$로 미분하면
$\Delta H_{\rxn,j}$가 $T$-상수라 $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ — 두 경로가 일치한다,
이는 Gibbs 항등식과 식~\eqref{eq:Uj}가 서로 **정합**(하나가 다른 하나에서 나온 것이 아니라 같은
열역학 구조의 두 얼굴)함을 보이는 교차검산이다.)

**(d) 박스 — 전극 위첨자 부착(LCO 대입).**
$$
\boxed{\;\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}\;}
\label{eq:lco-dUdT-derived}
$$
— (b)(c)의 유도 경로 어디에도 "$e=\mathrm{an}$"이 요구되지 않았으므로 $e=\mathrm{cat}$로 바로 대입
가능하다. 이것이 원문 식~\eqref{eq:lco-dUdT}와 **동일한 식**이며, 이 사슬은 그 식이 "괄호 전보체"가
아니라 Gibbs 항등식에서 두 줄 만에 나옴을 보인다.

### 1.4 원 줄글 대비

| 항목 | 원문(L470-482) | 재작성 |
|---|---|---|
| 전극무관 논증 | "유도에 전극 가정이 없다"(결론만) | (a)(b)(c)(d): 유도 3원칙(Gibbs 정의·화학퍼텐셜 정의·전기화학평형)이 반응종 무관 항등식임을 명시 확인 → 위첨자 부착 함수형 박스 |
| ∂U_j/∂T 다리 | "식 eq:Uj 의 T 미분, 전극 불문"(괄호 전보체) | Gibbs 항등식 (a)→대입 (b)→등치 (c)→박스 (d), 직접미분 교차검산 포함 |
| 물리·부호·수치 | — | 전부 불변(같은 결과식, 같은 부호, 같은 $\partial U_j/\partial T = \Delta S_{\rxn,j}/F$) |

### 1.5 sec:lco-center 논리 감사 결과

**무결.** 원문의 결론(전극무관성, 온도 미분 관계식)은 물리적으로 옳고, 흑연 유도 경로를 다시 추적한
결과 어느 단계도 전극 고유 가정을 쓰지 않음을 확인했다(위 (a)(b)). 발견된 것은 "논리 결함"이 아니라
"논증 생략"이며, 재작성은 그 생략을 메우는 것으로 충분하다 — 물리·부호·결과식 변경 0.

한 가지 주의점(결함은 아니나 재작성 시 명시 필요): 원문 verifybox(L490-509)의 $\Delta S_\rxn^\mathrm{cat}
\approx+80$ J/(mol·K) 수치는 **단일전극 전체 계수의 대표 스케일**이지 전이별 정밀값이 아니라고 이미
스스로 tier 병기하고 있다(L498-500) — 이 절제된 태도는 재작성에서도 보존해야 하며, 위 (c)에서 나는
숫자를 새로 만들지 않고 기존 verifybox를 그대로 남겨 이 절제를 훼손하지 않는다.

---

## 2. sec:lco-hys (L684-708) 재작성안

### 2.1 원 줄글 (현재, 요지)

- L685-687: "*§sec:hys 의 격자기체·정규용액 틀은 '동등한 자리에 리튬이 차고 빈다'는 가정만 쓰므로, 그
  가정이 서는 LCO 양극에도 그대로 적용된다 — Ω_j 의 값만 LCO 의 상전이가 정한다.*" → 적용 선언, 대입
  중간식 없음.
- L689-694 (T2·T3 order-disorder): "*한 쌍 전이가 식 eq:spinodal 의 spinodal 문턱 Ω_j>2RT 를 넘어 두 개의
  좁은 peak 로 갈라진다.*" → 문턱을 "넘는다"고 서술만 하고, $\xi_{s,j}^\pm$·$\Delta U_j^\hys$ 로 이어지는
  대입 사슬이 없다.
- L696-701 (T1 MIT): "*이 구간 역시 식 eq:dUhys·eq:Ubranch 의 spinodal gap·분기 중심을 그대로 받는다.*"
  → 같은 패턴, 대입 없음.
- L703-707 (도핑): "*정규용액 틀에서 이는 Ω_j 를 2RT 쪽으로 낮춰...*" → 정성 서술.

이것이 V1010_LCO_STYLE_REPORT.md가 지적한 "같은 틀 적용" 3회 반복(order-disorder·MIT·도핑) 및 "Ω_j
(0.47/1.49) spinodal 대입 중간식 전무"다.

### 2.2 논리 소당성 감사 — 원 논증이 실제로 유효한가

**두 가지를 구분해서 감사한다.**

**(A) "같은 정규용액 틀이 LCO에 적용된다"는 구조적 주장 — 무결.** §sec:hys의 유도(식~\eqref{eq:mu}
→ \eqref{eq:gxi} → \eqref{eq:gpp} → \eqref{eq:spinodal} → \eqref{eq:hysdiff} → \eqref{eq:dUhys} →
\eqref{eq:Ubranch})는 "격자기체 자리에 리튬이 차고 빈다"는 가정, 즉 이항 점유($\theta$ 또는 $1-\theta$)와
평균장 상호작용 $\Omega\theta(1-\theta)$ 가정만 쓴다 — 이 가정은 LCO의 팔면체 리튬 자리에도 문자 그대로
성립한다(리튬이 들어가거나 비거나 둘 중 하나, 이웃 자리와의 평균장 상호작용). 따라서 구조적 적용
가능성 자체는 옳다.

**(B) LCO 세 전이 모두가 Ω_j>2RT를 만족한다는 정량 주장 — 검증 불가(수치 부재), 단 결함은 아님.**
"T2·T3 가 spinodal 문턱을 넘어 두 개의 좁은 peak 로 갈라진다"(L692)는 서술은 **경험적 관찰**(order-disorder
전이가 실제로 좁은 두 봉우리로 나타남, Motohashi tier A)에 기반한 것이지, $\Omega_j$의 문헌 수치를
문턱 부등식에 대입해 검증된 것이 아니다 — 그런 $\Omega_j$ 수치 자체가 문건 어디에도 없다(§0 확인).
이것은 **논리 결함이 아니라 데이터 공백**이다: 결론(T2·T3가 두-상)은 관찰과 일치하고, 상분리를 낳는
메커니즘(문턱 부등식)도 §sec:hys에서 이미 검증되었으므로, 남은 것은 "$\Omega_j$가 몇 J/mol인지"라는
피팅 대상 수치일 뿐 논증의 인과 사슬 자체는 무결이다. 재작성은 이 부등식 자체를 명시적으로 다시
쓰되(§0에서 확인했듯) 수치를 지어내지 않는다.

**한 가지 실제 개선 여지(비약 아닌 표현 정밀화)**: 원문 L696 "MIT 2상역"이라는 표현이 order-disorder
(T2·T3)와 같은 $g_j(\xi)$ 이중웰 틀을 쓴다고 말하지만, MIT는 전자 자유도가 얽힌 상전이라 격자기체 단독
그림이 근사임을 원문도 스스로 명시한다(L698-701, "전자 자유도가 있어 엔트로피에 항이 하나 더 붙는다").
이 구분은 원문이 이미 정확히 하고 있으므로 결함이 아니라 — 재작성에서 이 경계를 유지하는 것이 핵심
과제다(§sec:lco-electronic을 침범하지 않음).

### 2.3 재작성 수식 사슬

**삽입 위치**: L684-707 (부제 "LCO order-disorder 와 MIT 2상역 — 같은 정규용액 틀" 전체, `\S\ref{sec:lco-hys}`
라벨이 붙은 첫 문단부터 "도핑 보정" 문단 끝까지). 다음 절 N4(`sec:width`, L709~)는 그대로 유지.

---

#### (i) 공통 대입 — LCO 격자기체 사슬 (T2·T3·T1 전부에 선행)

**(a) 출발 — §sec:hys 자유에너지를 LCO 리튬 자리로.** 식~\eqref{eq:gxi}의 $g_j(\xi)=g_j^0+RT[\xi\ln\xi+
(1-\xi)\ln(1-\xi)]+\Omega_j\xi(1-\xi)$는 "자리 하나에 리튬이 있거나 없거나"라는 이항 격자기체 가정만
쓴다. LCO $\mathrm{Li}_x\mathrm{CoO_2}$의 팔면체 리튬 자리도 이 가정을 문자 그대로 만족하므로(자리당
점유 0 또는 1), 전이 인덱스 $j\in\{\mathrm{T1,T2,T3}\}$(표~\ref{tab:lco-staging})를 달아 그대로 쓴다:
$$
g_j^\mathrm{cat}(\xi)=g_j^{0,\mathrm{cat}}+RT\big[\xi\ln\xi+(1-\xi)\ln(1-\xi)\big]+\Omega_j^\mathrm{cat}\,\xi(1-\xi).
$$

**(b) 연산 — 문턱 부등식에 표~\ref{tab:lco-staging}의 정성 정보 대입.** 식~\eqref{eq:spinodal}의
문턱 조건 $\Omega_j>2RT$를 $j=$T2($\sim$4.05 V, hex→monoclinic)·T3($\sim$4.17 V, monoclinic→hex)에
적용하면, Motohashi tier A 관측(각 전이가 실측에서 **좁은 두 봉우리**로 갈라짐, 곧 상분리 plateau가
실재함)이 바로 $\Omega_{j}^\mathrm{cat}>2RT$의 **경험적 증거**다 — 상분리가 관찰되었다는 것 자체가
$g_j''(\xi)$가 어딘가에서 음이 됨(식~\eqref{eq:gpp})을 뜻하고, 그것이 문턱 부등식의 정의이기 때문이다
(역으로 문턱 미만이면 $g_j''\ge0$ 전 구간이라 단일 극소 = 연속 고용체가 되어 두 봉우리로 갈라질 수
없다 — 대우 논증).

**(c) 중간식 — spinodal 자리와 gap을 T2·T3에 부착.**
$$
\xi_{s,j}^\pm=\tfrac12(1\pm u_j),\qquad u_j=\sqrt{1-\frac{2RT}{\Omega_j^\mathrm{cat}}}\qquad(j=\mathrm{T2,T3}),
$$
$$
\Delta U_j^{\hys,\mathrm{cat}}=\frac{2}{F}\Big[\Omega_j^\mathrm{cat}\,u_j-2RT\,\mathrm{artanh}\,u_j\Big]\qquad(j=\mathrm{T2,T3})
$$
— 식~\eqref{eq:spinodal}·\eqref{eq:dUhys}에 위첨자만 단 것(유도 경로가 전극을 가정하지 않으므로 §1.3
(a)(b)와 같은 논리로 정당).

**(d) 박스 — T2·T3 분기 중심.**
$$
\boxed{\;U_j^{\mathrm{cat},d}=U_j^\mathrm{cat}+\tfrac12\,\sigma_d\,h_{\eta,j}\,\gamma_j\,\Delta U_j^{\hys,\mathrm{cat}}\;,\qquad j\in\{\mathrm{T2,T3}\}\;}
$$
— 식~\eqref{eq:Ubranch}와 동형. $\Omega_j^\mathrm{cat}$의 수치는 문헌에 없으므로(§0) 이 사슬은 구조를
확정하되 **피팅 대상**으로 남긴다(흑연 $\Omega_j$ 초기값이 "거친 추정"이었던 것과 동일한 지위,
R1_broadening.md calibration).

#### (ii) T1 MIT — 같은 사슬 + 전자 자유도 경계 명시

**(a) 출발.** T1($\sim$3.90 V, $x\approx0.94$--$0.75$, insulator→metal)도 리튬 자리 점유 관점에서는
(i)과 같은 이항 격자기체이므로 같은 식이 선다:
$$
g_\mathrm{T1}^\mathrm{cat}(\xi)=g_\mathrm{T1}^{0,\mathrm{cat}}+RT[\xi\ln\xi+(1-\xi)\ln(1-\xi)]+\Omega_\mathrm{T1}^\mathrm{cat}\,\xi(1-\xi).
$$

**(b) 연산 — 문턱 부등식과 "구조 몫만" 경계 명시.** T1의 실측 plateau($\sim$3.9 V 부근 2상 공존,
L696)가 T2·T3와 같은 논리로 $\Omega_\mathrm{T1}^\mathrm{cat}>2RT$의 경험적 증거다. 단, 이 문턱 부등식이
포착하는 것은 리튬 자리 점유의 **구조적**(config) 상호작용 몫뿐이다 — MIT의 전자 자유도(전도전자
상태밀도 $g(E_F)$ 켜짐)는 $g_j(\xi)$에 들어 있지 않고, 그 몫은 §sec:lco-electronic의 별도 항
$\Delta S_{e,j}$로 붙는다(식~\eqref{eq:lco-decomp}).

**(c) 중간식 — T1 spinodal·gap(구조 몫).**
$$
\xi_{s,\mathrm{T1}}^\pm=\tfrac12(1\pm u_\mathrm{T1}),\quad u_\mathrm{T1}=\sqrt{1-\frac{2RT}{\Omega_\mathrm{T1}^\mathrm{cat}}},
\qquad
\Delta U_\mathrm{T1}^{\hys,\mathrm{cat}}=\frac{2}{F}\Big[\Omega_\mathrm{T1}^\mathrm{cat}u_\mathrm{T1}-2RT\,\mathrm{artanh}\,u_\mathrm{T1}\Big].
$$

**(d) 박스 — T1 분기 중심(구조 몫 + 전자 몫의 분리 명시).**
$$
\boxed{\;U_\mathrm{T1}^{\mathrm{cat},d}=U_\mathrm{T1}^\mathrm{cat}+\tfrac12\,\sigma_d\,h_{\eta,\mathrm{T1}}\,\gamma_\mathrm{T1}\,\Delta U_\mathrm{T1}^{\hys,\mathrm{cat}}\;,}
$$
여기서 $U_\mathrm{T1}^\mathrm{cat}=U_\mathrm{T1}^\mathrm{cat}(T)$ 자체가 식~\eqref{eq:Uj}를 통해
$\Delta S_{\rxn,\mathrm{T1}}^\mathrm{cat}=\Delta S^\mathrm{config}+\Delta S^\mathrm{vib}+\Delta S_{e,\mathrm{T1}}$
(식~\eqref{eq:lco-decomp})를 담고 있다 — 곧 **전자 자유도는 격자기체 $g_j(\xi)$ 상호작용 몫 $\Omega_j$에
들어가지 않고, 중심 $U_j$ 쪽 엔트로피 분해에 들어간다**. 이 사슬은 "MIT 2상역은 정규용액 틀로, 전자
자유도는 별도 항으로"(원문 L700-701)라는 이중계산 방지 원칙을 (a)-(d) 대입으로 명시적으로 확인한다 —
$\Omega_j$ 문턱식과 $\Delta S_{e,j}$ 분해식이 서로 다른 슬롯(각각 $g_j(\xi)$의 상호작용 계수, $U_j(T)$의
엔트로피 성분)에 산다는 구조가 사슬 자체에서 드러난다.

#### (iii) 도핑 보정 — 문턱 부등식 위의 이동으로 재기술

**(a) 출발.** 도핑(Al³⁺/Mg²⁺ 비-redox 치환)이 상전이를 억제한다는 관측(원문 L703-704)을, 정규용액
파라미터의 변화로 옮긴다: 도핑 농도를 $\delta$라 하면 $\Omega_j^\mathrm{cat}=\Omega_j^\mathrm{cat}(\delta)$이고
관측은 $\dd\Omega_j^\mathrm{cat}/\dd\delta<0$(도핑이 늘수록 $\Omega$가 줄어듦)이다.

**(b) 연산 — 문턱까지의 거리에 대입.** 식~\eqref{eq:spinodal}의 $u_j=\sqrt{1-2RT/\Omega_j^\mathrm{cat}}$에
$\Omega_j^\mathrm{cat}(\delta)\downarrow$를 대입하면 $u_j(\delta)\downarrow$(제곱근 안 $2RT/\Omega_j$가
커져 $u_j$가 작아짐), $\Omega_j^\mathrm{cat}(\delta)\to2RT^+$에서 $u_j\to0$.

**(c) 중간식 — gap의 도핑 의존.** 식~\eqref{eq:dUhys}에 그대로 대입하면
$$
\Delta U_j^{\hys,\mathrm{cat}}(\delta)=\frac{2}{F}\Big[\Omega_j^\mathrm{cat}(\delta)\,u_j(\delta)-2RT\,\mathrm{artanh}\,u_j(\delta)\Big]\ \xrightarrow{\delta\uparrow}\ 0
$$
— §sec:hys L621-623에서 이미 확립한 $\Omega_j\to2RT^+$ 연속 소멸 극한($\Delta U_j^\hys\to\frac{8RT}{3F}u_j^3\to0$)을
그대로 재사용한 것이며, 이것이 "히스가 준다"의 수식적 의미다.

**(d) 박스 — 도핑에 따른 폭 재분배.** $\Omega_j^\mathrm{cat}(\delta)\to2RT^+$에서 식~\eqref{eq:wbase}
이중지위 논증(§sec:width L728-743)에 의해 그 전이는 "두-상"(현상학적 피팅 폭) 쪽에서 "단상에 가까운"
쪽으로 넘어가려는 경향을 보인다 — 곧
$$
\boxed{\;\Omega_j^\mathrm{cat}(\delta)\downarrow \ \Rightarrow\ \Delta U_j^{\hys,\mathrm{cat}}(\delta)\downarrow,\ u_j(\delta)\downarrow \ \Rightarrow\ \text{broadening(\S\ref{sec:broadening}) 폭 비중 상대적 증가.}\;}
$$
이는 원문 L704-705 "spinodal gap·히스가 줄고 평탄역이 풀려, broadening 폭이 더 큰 몫을 차지한다"를
그대로 수식화한 것 — 정성 결론 불변, 대입 경로만 명시.

### 2.4 원 줄글 대비

| 항목 | 원문(L684-707) | 재작성 |
|---|---|---|
| 총론("같은 틀 적용") | 1회 선언 | (i) 공통 대입 사슬로 $g_j(\xi)$→spinodal→gap→분기중심까지 4단 |
| T2·T3 order-disorder | "spinodal 문턱을 넘어 갈라진다"(서술) | (i)(b) 대우 논증(관측된 두-봉우리 ⟺ $\Omega_j>2RT$) + (c)(d) 중간식·박스 |
| T1 MIT | "그대로 받는다"(서술) | (ii)(a)-(d) 동일 사슬 + 전자몫과의 슬롯 분리 명시(이중계산 방지 구조 확인) |
| 도핑 | "$\Omega_j$를 낮춰...폭이 큰 몫"(서술) | (iii)(a)-(d) $\delta$-의존 $\Omega_j(\delta)$→$u_j(\delta)$→gap(δ)→극한 재사용 박스 |
| Ω_j 수치 | 없음(원문도 수치 대입 안 함) | 수치 대입 없음(문헌 부재, §0 확인) — **지어내지 않음**, 구조만 명시하고 피팅 대상으로 명기 |

### 2.5 sec:lco-hys 논리 감사 결과

**무결 (데이터 공백은 별도 명기, 결함 아님).** 구조적 적용 가능성(A)은 §sec:hys 유도가 실제로 전극
비의존임을 확인해 무결. 정량 주장(B, "세 전이 모두 Ω_j>2RT")은 수치 검증이 아니라 관측(좁은 두-봉우리
plateau 실재) → 대우 논증(§2.3 (i)(b))으로 뒷받침되며, 이는 §0에서 이미 확정한 사전 지식(LCO Ω_j
수치가 문헌에 없음)과 모순되지 않는다 — 재작성은 이 공백을 감추지 않고 "피팅 대상"으로 명기했다
(R1_broadening.md의 "코드 Ω 초기값=거친 추정" calibration 정신과 정합).

T1 MIT 관련 유일한 주의점: 원문이 이미 "정규용액 틀(config)"과 "전자 자유도(elec)"를 분리해 서술
(L698-701)하고 있었고, 재작성 (ii)(d)는 이를 **수식 슬롯**(각각 $\Omega_j$ vs $\Delta S_{e,j}$)으로
명시함으로써 이중계산 방지를 강화했을 뿐 새로운 주장을 추가하지 않았다 — sec:lco-electronic·
sec:lco-decomp의 기존 결론(eq:lco-decomp)을 침범하지 않고 순인용만 했다(원칙 3 "손대지 말 것" 준수
확인).

---

## 3. 신규 개념 도입 여부 점검 (원칙 2 준수 확인)

- $\rho(U_\app)$/PSD convolution/$\rho_G$ 모델: **도입 안 함**. broadening 앙상블 모델은 이 드래프트
  범위 밖(§sec:broadening 자체이며 sec:lco-center/hys가 아님)이고, 재작성 전체에서 언급하지 않았다.
- 새 물리량: `Ω_j^cat`, `U_j^cat`, `Δ S_{rxn,j}^cat` 등은 **기존 식에 위첨자 e/cat만 부착**한 표기이지
  신규 개념이 아니다(§sec:lco-map이 이미 이 표기 관례를 세워둔 것을 따름, L295-309).
  도핑 파라미터 $\delta$(§2.3 (iii))는 원문 L703-707 "우리 시료 도핑"을 정량화하기 위한 최소 표기이며,
  본문에 이미 있는 정성 주장("Ω_j를 낮춘다")을 수식 사슬로 잇는 데만 쓰고 새로운 물리 기작을 들여오지
  않는다.

---

## 4. 손대지 않은 절 확인

`sec:lco-map`(L295-349)·`sec:lco-Se`(L953-1067)·`sec:lco-gate`(L1068-1096)·N7-N9(동역학 꼬리~합산)·
전자엔트로피 절 전체 — 이번 재작성안에서 이 절들의 텍스트를 인용만 했고(전방 참조), 수정 대상으로
삼지 않았다. `sec:lco-decomp`(L1690-1727)·`sec:lco-peak`(L1204-1216)·`sec:lco-code`(L1740~)도 동일 —
이들은 V1010_LCO_STYLE_REPORT.md 표에서 이미 별도 항목(peak/decomp/plug-in/MSMR)으로 분류돼 있으며
이번 base 프롬프트(§목표)가 지정한 범위(sec:lco-center·sec:lco-hys)에 들지 않으므로 이 드래프트에서
다루지 않는다.

---

## 5. 요약 (5줄)

1. **sec:lco-center**: "전극무관"이라는 결론은 §sec:center 유도 3원칙(Gibbs 정의·화학퍼텐셜·전기화학평형)이
   반응종을 가정하지 않는다는 점을 (a)-(d)로 확인해 위첨자 부착 함수형으로 재작성했고, ∂U_j/∂T도 Gibbs
   항등식에서 두 줄(등치→박스)로 잇는 다리를 신설했다 — 결과식·부호·수치 불변.
2. **sec:lco-hys**: T2·T3(order-disorder)·T1(MIT)·도핑 세 서술 전부를 §sec:hys의 $g_j(\xi)$→spinodal→
   $\Delta U_j^\hys$→분기중심 사슬에 전이별 위첨자 대입으로 재작성했고, 도핑은 $\Omega_j(\delta)$ 의존
   극한으로 이었다.
3. **논리 결함 발견 여부**: 결함 없음 — 두 절 모두 "결론은 참이나 대입 과정이 생략된 논증"(비약이지
   오류 아님)이었다. 단 하나 남는 것은 LCO $\Omega_j$의 수치 부재(§0)이며, 이는 문헌 공백이지 문건의
   논리 결함이 아니므로 재작성에서 "피팅 대상"으로 명기하고 수치를 지어내지 않았다.
4. **물리 불변 확인**: 두 절의 최종 결과식(전극위첨자 부착 $U_j(T)$·$\partial U_j/\partial T=\Delta
   S_{\rxn,j}/F$·$\Delta U_j^\hys$·$U_j^d$)은 흑연 원식과 문자 그대로 동형이며 부호·극한(Ω→2RT⁺ 연속
   소멸, T→0 엔탈피 극한)도 그대로 재사용해 검증했다 — 새 물리·새 수치 도입 없음.
5. **가장 약했던 원 줄글**: sec:lco-hys의 "같은 정규용액 틀 그대로 적용된다"(L685-687) — 구조적으로는
   맞지만 세 전이(T2·T3·T1) 각각에 대한 문턱 부등식 대입이 전무해 V1010 리포트가 지적한 "Ω_j 대입
   중간식 전무"가 가장 두드러졌고, 이 드래프트의 (i)(ii) 사슬이 그 공백을 채우는 핵심 기여다.
