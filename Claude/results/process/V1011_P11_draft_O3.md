# V1.0.11 Phase 1.1 — LCO 수식화 supplement 드래프트 (ID: **O3**, Opus)

> 대상 = `docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex` 의 `sec:lco-center`(L470–512, 양극 $\partial U_j/\partial T$)·`sec:lco-hys`(L684–707, order–disorder/MIT 정규용액). 두 절이 현재 줄글 결론("같은 틀 그대로 적용"·괄호 전보체)으로 닫혀 있어, 흑연 forward 절(`sec:pol` L351+·`sec:center` L405+·`sec:hys` L515+)의 **(a)출발식→(b)적용연산→(c)중간식≥1→(d)박스** 사슬로 재작성하는 supplement.
> ★드래프트만. tex/코드 수정 X(편입은 master). 물리·결과식·부호·수치 원칙 불변(줄글→수식, 전개 형식만). 신규 개념(ρ(U_app)/PSD convolution·ρ_G·새 물리) 도입 0. 손대지 않는 절: `sec:lco-map`·`sec:lco-Se`·`sec:lco-gate`·N7–9·전자엔트로피 절.
> 참조 정독 근거: 대상 tex 전문(해당 두 절 + 흑연 forward 4절 + `eq:n0map` L197·`eq:eqcond` L433·`eq:Uj` L453·`tab:lco-staging` L330·`sec:lco-electronic` L933·`eq:U1T2` L1060·`eq:msmr` L1744) / `V1010_LCO_STYLE_REPORT.md` §1 center·hys 행 / `AUTHOR_BRIEF.md`(∂U/∂T=ΔS/F·전이표·전자항 부호) / `R1_broadening.md`(two-phase = LiC₁₂·LiC₆ 2개 calibration·Ω 초기값=거친 추정).

---

## 0. 요지 (5-tier 앞당김)

- **center**: 전극무관 논증을 `eq:n0map`·`eq:eqcond` 대입 사슬로, $\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$ 를 Gibbs 항등식 다리 완결 문장 + (a→d)로 재작성. 물리·부호·수치 **불변**(흑연 `sec:center` L458–459 의 다리를 LCO 절에 명시 이식만).
- **hys**: 흑연 `sec:hys` 의 $\mu(\theta)\!\to\!g''\!\to\!\xi_s^\pm\!\to\!\Delta U_j^\hys=(2/F)[\Omega_j u_j-2RT\,\mathrm{artanh}\,u_j]$ 사슬을 LCO $\Omega_j$(T2·T3 order–disorder·T1 MIT)로 **실제 대입한 중간식**으로. "같은 틀 적용" 3회(order-disorder·MIT·도핑) 각각 LCO-특화 대입 유도.
- **★논리 결함 발견 여부**: 두 절의 물리·부호·결과식은 **무결**(잘못된 유도 아님). 단 **정합 명시 결함 2건**을 근거와 함께 지적·보완안 제시 — (i) center 절의 "$+80$ J/(mol·K)$>0$ 이면 $\partial U/\partial T>0$" 검산이 `sec:lco-map`(L304–309)의 **LCO 방전=리튬화·전위 하강** 부호 규약과 어느 좌표(삽입 vs 탈리튬화)에서 성립하는지 미명시 → 좌표 고정 문장 필요, (ii) hys 절의 two-phase calibration 이 `R1_broadening.md` 의 "흑연 two-phase = LiC₁₂·LiC₆ 2개" 와 **어느 LCO 전이가 정규용액 two-phase 인지** 대응만 서술하고 spinodal 문턱 $\Omega_j>2RT$ 대입 중간식이 없음 → 아래 (b)(c) 사슬이 그 공백을 메움.
- **물리 불변 확인**: 결과식($U_j$·$\partial U_j/\partial T$·$\Delta U_j^\hys$·spinodal), 부호(양극 $U$ 높음·$\Delta U_j^\hys\ge0$·전자항 소수 음의 보정), 수치(+0.83 mV/K·+80 J/mol·K·0.47/1.49 J/K·mol·$x_\mathrm{MIT}\approx0.85$) 전부 원문 그대로 사용 — **변경 0**.
- **가장 약했던 원 줄글**: `sec:lco-hys` L684–701 의 "같은 정규용액 틀 그대로 적용"·"식~\eqref{eq:dUhys}·\eqref{eq:Ubranch} 를 그대로 받는다" 서술 — LCO $\Omega_j$ 를 spinodal·gap 식에 넣은 중간식이 **한 줄도 없어** G-derive(점프 0) 최대 위반 지점.

---

# A. `sec:lco-center` 재작성

## A.0 삽입 위치

- **삽입 위치**: `sec:lco-center` 전체(L470–512)를 아래 A.1(전극무관 논증)·A.2(온도 미분)·A.3(부호 검산 verifybox 유지)로 재편. verifybox(L490–509)는 **수치·부호 내용 불변**으로 두되, 앞에 좌표 고정 한 문장(A.2 말미)을 삽입. 도입 문장(L470–475)은 A.1 의 (a)→(d)로 대체.

## A.1 전극무관 논증 — 단정 비약 제거 (eq:n0map·eq:eqcond 대입)

**원 줄글 (L471–476, 대비)**:
> 식~\eqref{eq:Uj} 의 $U_j(T)=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F$ 는 *유도에 전극 가정이 없다* — 평형 조건 식~\eqref{eq:eqcond}($\Delta G_j=-FU_j$)에서 곧장 나오므로 LCO 양극에도 그대로 성립한다. LCO 에 적용할 때 바뀌는 것은 입력 $(\Delta H_{\rxn,j},\Delta S_{\rxn,j})$ 의 *값*뿐이고 …

→ "전극 가정이 없다"가 **단정**으로 던져지고(어느 식 단계가 전극-중립인지 대입으로 보이지 않음), 흑연 `sec:pol`·`sec:center` 의 (a)→(d) 밀도에 못 미친다(`V1010_LCO_STYLE_REPORT` §1 center 행 HIGH×2: "전극무관 논증 단정 비약").

**재작성 수식 사슬 (a→d)**:

> **(a) 출발 — 전극-중립 골격의 세 진입.** `sec:center`(식~\eqref{eq:Uj})의 유도를 되짚으면, 세 다리 어디에도 "흑연"이 들어가지 않는다: (i) 실험조건 매핑 식~\eqref{eq:n0map} 의 방향 부호·전류 환산 $\sigma_d=\pm1$, $|I|=\text{c\_rate}\cdot Q_\cell$ 는 삽입형 전극이면 종류 불문이고, (ii) 전기화학 평형 조건 식~\eqref{eq:eqcond}
> $$\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U),\qquad \Delta G_j=-sF\,U_j$$
> 은 삽입 반쪽반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$ 의 전기화학 평형에서 나오며 host 가 흑연인지 LCO 인지에 무관하다(host 정보는 $\mu^0$·$\Delta G_j$ 의 *값*에만 들어간다), (iii) 비배치 몫 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 은 열역학 항등식이라 재료-중립이다.
>
> **(b) 연산 — host 라벨을 값으로 격리.** 위 세 다리에서 host 의존을 모으면, 유일한 host 입력은 $(\Delta H_{\rxn,j},\Delta S_{\rxn,j})$ 한 쌍뿐이다. 식~\eqref{eq:eqcond} 의 $\Delta G_j=-sFU_j$ 에 비배치 몫을 대입하면
> $$\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}=-F\,U_j\quad(s=+1),$$
> 이 관계에서 $F$·$T$·$s$ 는 보편 상수·규약이고 host 는 $(\Delta H_{\rxn,j},\Delta S_{\rxn,j})$ 로만 진입한다.
>
> **(c) 중간식 — LCO 상첨자로 값만 교체.** 흑연↔LCO 의 차이를 상첨자 $\mathrm{cat}$(cathode)로 명시하면, 같은 식이 값만 바뀐 채 성립한다:
> $$\boxed{\;U_j^\mathrm{cat}(T)=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\,\Delta S_{\rxn,j}^\mathrm{cat}}{F}\;}
> \qquad(\text{식~\eqref{eq:Uj} 와 동일 꼴, host 입력만 교체}).$$
>
> **(d) 결론 — 값의 부호로 높은 중심.** LCO 양극의 높은 중심($\sim$3.9–4.2 V)은 이 식의 분자 $-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 크게 양(LCO 삽입 반응의 큰 음의 $\Delta H_\rxn$)인 데서 온다 — 흑연의 $\sim$0.1 V 와 *같은 식, 다른 입력*이다. 곧 "전극 가정이 없다"는 단정이 아니라, (a)의 세 다리가 전부 host-중립이고 host 가 (b)에서 값 두 개로만 격리된다는 대입으로 **회수**된다.

**논리 감사 (center A.1)**: 무결. 원 줄글의 결론("식·부호 관계는 흑연과 1:1, 값만 다름")은 정확하며, 재작성은 그 결론을 `eq:n0map`→`eq:eqcond`→`eq:Uj` 대입 사슬로 *유도*했을 뿐 물리를 바꾸지 않는다. 상첨자 $\mathrm{cat}$ 은 `tab:lco-staging`·`eq:lco-dUdT`·`eq:lco-decomp` 에서 이미 쓰이는 표기라 신규 도입 아님.

## A.2 온도 의존 $\partial U_j/\partial T$ — Gibbs 항등식 다리 (전보체 → 완결 문장)

**원 줄글 (L477–482, 대비)**:
> 온도 의존도 같은 미분이다:
> $$\frac{\partial U_j}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}\qquad(\text{식~\eqref{eq:Uj} 의 }T\text{ 미분, 전극 불문}).$$

→ 결과식은 옳으나 "식~\eqref{eq:Uj} 의 $T$ 미분, 전극 불문"이 **괄호 전보체**로 다리를 삼켰다(`V1010_LCO_STYLE_REPORT` §1: "Gibbs 항등식 다리 없이 괄호 전보체"). 흑연 `sec:center` L458–459 에는 다리("Gibbs 항등식 $\partial\Delta G/\partial T=-\Delta S$ 와 $\Delta G=-FU$ 를 잇는 것과 같다")가 완결 문장으로 있으나 LCO 절엔 이식되지 않았다.

**재작성 수식 사슬 (a→d)**:

> **(a) 출발 — 두 항등식.** 온도 의존은 두 항등식을 잇는다: 평형 조건 식~\eqref{eq:eqcond} 의 $\Delta G_j=-FU_j$ 와, Gibbs 자유에너지 정의 식~\eqref{eq:gibbsdef}($G\equiv H-TS$)의 온도 미분이 주는 Gibbs–Helmholtz 항등식
> $$\left.\frac{\partial \Delta G_j}{\partial T}\right|_P=-\Delta S_{\rxn,j}.$$
> **(b) 연산 — 두 식을 $T$ 로 미분해 연결.** $\Delta G_j=-FU_j$ 의 양변을 $T$ 로 미분하면 $\partial\Delta G_j/\partial T=-F\,\partial U_j/\partial T$ 이고, 이를 (a)의 Gibbs–Helmholtz 우변과 등치하면
> $$-F\,\frac{\partial U_j}{\partial T}=-\Delta S_{\rxn,j}^\mathrm{cat}.$$
> **(c) 중간식 — $\partial U_j/\partial T$ 로 정리.** 양변을 $-F$ 로 나누면
> $$\frac{\partial U_j}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.$$
> **(d) 박스 — 전극-중립 관계식.**
> $$\boxed{\;\frac{\partial U_j}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}\;}
> \qquad(\text{식~\eqref{eq:lco-dUdT}; Gibbs–Helmholtz + }\Delta G=-FU\text{, host 불문}).$$
> 이 다리는 흑연 `sec:center`(식~\eqref{eq:Uj} 아래)의 것과 *글자 그대로 같은 두 항등식*이며, LCO 에서 바뀌는 것은 우변의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 값뿐이다 — 흑연 전이별 $+29/0/-5/-16$ J/(mol·K)(표~\ref{tab:staging})와 값은 다르나 관계식은 동일하다.

**★좌표 고정 문장 (A.2 말미 삽입 — 정합 결함 (i) 보완)**:

> **(부호 좌표 고정.)** 식~\eqref{eq:lco-dUdT} 의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 는 반쪽반응을 *삽입 방향*(Li$^+$ 가 host 로 들어옴)으로 적은 반응 엔트로피다 — 흑연 표~\ref{tab:staging} 의 부호 규약(삽입 기준 음의 $\Delta S_\rxn$)과 동일 좌표다. `sec:lco-map`(위)에서 LCO 방전($\sigma_d=+1$)은 host 관점 *리튬화*(삽입)이므로, 아래 검산의 $\partial U/\partial T$ 부호는 이 삽입 좌표에서 읽는다. 단전극 potentiometric $\dd\phi/\dd T$ 는 관례상 반쪽전지 전위의 온도 계수로 보고되므로(부호는 측정 규약 의존), 아래 verifybox 는 그 대표 스케일을 삽입-반응 $\Delta S_{\rxn}^\mathrm{cat}$ 로 환산해 *크기·부호 sanity* 만 확인한다.

**논리 감사 (center A.2)**: 무결 + 정합 보완 1건. 결과식·부호·수치 불변. **정합 결함 (i)**: 원 verifybox(L491–494)는 "$\dd\phi/\dd T\approx+0.83$ mV/K → $\Delta S_{\rxn}^\mathrm{cat}\approx+80$ J/(mol·K)$>0$ → $\partial U/\partial T>0$" 를 적는데, `sec:lco-map`(L304–305)은 LCO 방전=리튬화=전위 하강이라 규정한다. 두 서술이 **다른 좌표**(단전극 potentiometric 규약 vs 삽입-반응 좌표)에서 읽히므로 **모순은 아니나**, 어느 좌표에서 부호를 읽는지 원문이 명시하지 않아 독자 오독 여지가 있다(부호 사슬 G-follow 저하). 위 좌표 고정 문장이 이를 못박는다 — 물리·수치는 그대로 두고 **읽는 좌표만 명시**한다. verifybox 본문(L495–508, 단전극 vs 전셀 혼동 금지·전자항 공존)은 **수정 없이 유지**(이미 삽입-기준으로 정합).

---

# B. `sec:lco-hys` 재작성

## B.0 삽입 위치

- **삽입 위치**: `sec:lco-hys`(L684–707) 전체. 도입 문장(L684–687)은 B.1(공통 대입 준비)로, "(T2·T3) order–disorder"(L689–694)는 B.2 로, "(T1) MIT 2상역"(L696–701)은 B.3 으로, "도핑 보정"(L703–707)은 B.4 로 재작성. 흑연 `sec:hys` 의 결과식(식~\eqref{eq:mu}·\eqref{eq:gxi}·\eqref{eq:gpp}·\eqref{eq:spinodal}·\eqref{eq:dUhys}·\eqref{eq:Ubranch})은 **재유도하지 않고 참조·대입만**(중복 유도 금지) — LCO 파라미터를 그 식에 넣은 중간식을 새로 적는다.

## B.1 공통 대입 준비 — 정규용액 틀의 host-중립 진입 + two-phase calibration

**원 줄글 (L684–687, 대비)**:
> \S\ref{sec:hys} 의 격자기체·정규용액 틀은 "동등한 자리에 리튬이 차고 빈다"는 가정만 쓰므로, 그 가정이 서는 LCO 양극에도 그대로 적용된다 — $\Omega_j$ 의 *값*만 LCO 의 상전이가 정한다. … 세 전이 모두에 대응한다.

→ "그대로 적용된다"가 대입 없이 서술로 닫힘. 어느 LCO 전이가 spinodal 문턱 $\Omega_j>2RT$ 를 넘는지(=정규용액 two-phase)가 흑연 calibration(`R1_broadening.md`: two-phase=LiC₁₂·LiC₆ 2개)과 **명시 대응 없이** "세 전이 모두"로 뭉뚱그려짐 → 정합 결함 (ii).

**재작성 수식 사슬 (a→b)**:

> **(a) 출발 — host-중립 대입점.** `sec:hys` 의 격자기체 화학퍼텐셜 식~\eqref{eq:mu}
> $$\mu_\mathrm{Li}(\theta)=\mu^0+RT\ln\frac{\theta}{1-\theta}+\Omega_j(1-2\theta)$$
> 은 "동등한 자리에 Li 가 차고 빈다"는 가정 하나만 쓴다. 이 가정이 서는 host 라면 흑연·LCO 무관하게 성립하므로, LCO 세 전이 각각에 대해 유일한 host 입력은 상호작용 $\Omega_j$(및 폭 $n_j$·중심 $U_j$)의 *값*이다 — 식~\eqref{eq:mu}→\eqref{eq:gpp}→\eqref{eq:spinodal}→\eqref{eq:dUhys}→\eqref{eq:Ubranch} 사슬 전체가 host-중립 골격이고, LCO 는 $\Omega_j$ 를 갈아 끼운다.
>
> **(b) two-phase calibration — 어느 전이가 정규용액 two-phase 인가.** spinodal 문턱은 식~\eqref{eq:spinodal} 의 실수 조건 $\Omega_j>2RT$($2RT\approx4958$ J/mol @298 K)다. 흑연에서 이 문턱을 *피팅 후* 유지하는 것은 강한 1차 전이 LiC₁₂·LiC₆ 2개뿐이고, dilute→stage4·4L↔3L 은 연속 고용체라 $\Omega_j<2RT$ 로 내려간다(\S\ref{sec:width} 이중지위·\S\ref{sec:broadening}(a)). LCO 는 이 대응을 다음처럼 받는다:
> $$\begin{cases}
> \text{T2·T3 order--disorder}: & \Omega_j>2RT\ \Rightarrow\ \text{정규용액 two-phase(초격자 상분리)},\\
> \text{T1 MIT 2상역}: & \Omega_j>2RT\ \Rightarrow\ \text{구조 two-phase(전자항은 별도)},\\
> \text{(연속 고용체 구간)}: & \Omega_j\le2RT\ \Rightarrow\ \text{단상(히스 없음)}.
> \end{cases}$$
> 곧 흑연의 "two-phase = 2개(LiC₁₂·LiC₆)" calibration 이 LCO 에선 "two-phase = T1·T2·T3 의 상분리 구간"으로 *host 별로 다른 전이 집합*에 대응하며, 문턱 판정 식 $\Omega_j>2RT$ 자체는 동일하다(`R1_broadening.md` D7: LCO 두-상 확장은 흑연 2개와 별개로 정확). 아래 각 전이는 이 문턱을 넘는 것으로 두고 $\Omega_j$ 를 대입한다.

**논리 감사 (hys B.1)**: 무결 + 정합 보완 1건. **정합 결함 (ii)**: 원문 L686–687 은 "세 전이 모두에 대응한다"까지만 서술하고, 흑연 two-phase=2개 calibration 과의 **대응 표**·spinodal 문턱 대입이 없었다. 위 (b)가 문턱 식 $\Omega_j>2RT$ 를 각 LCO 전이에 명시 대응시켜 공백을 메운다 — 물리(문턱·two-phase 판정)는 흑연과 동일, LCO 전이 집합만 다름. 신규 개념 0.

## B.2 (T2·T3) order–disorder — Ω_j 를 spinodal·ΔU_hys 에 실제 대입

**원 줄글 (L689–694, 대비)**:
> $x\approx0.5$ 부근에서 … monoclinic 초격자(질서상)를 이룬다 — 이 정렬은 정규용액의 $\Omega>0$ … 이 만드는 상분리의 LCO 사례다. 한 쌍 전이(T2 $\sim$4.05 V, T3 $\sim$4.17 V)가 식~\eqref{eq:spinodal} 의 spinodal 문턱 $\Omega_j>2RT$ 를 넘어 두 개의 좁은 peak 로 갈라진다. 정렬의 charge-order 엔트로피 변화($\approx$0.47 J/K·mol@$x{=}\tfrac12$, $\approx$1.49 J/K·mol@$x{=}\tfrac23$)가 … config 주도 $\Delta S$ 의 출처다.

→ "$\Omega_j>2RT$ 를 넘어 두 peak 로 갈라진다"가 **결론만** 서술. spinodal 값 $\xi_{s,j}^\pm$·gap $\Delta U_j^\hys$ 를 LCO $\Omega_j$ 로 계산한 **중간식이 한 줄도 없다**(`V1010_LCO_STYLE_REPORT` §1 hys 행 HIGH×3: "Ω_j spinodal 대입 중간식 전무").

**재작성 수식 사슬 (a→d)**:

> **(a) 출발 — 정렬을 $\Omega_j>0$ 로.** $x\approx0.5$ 의 monoclinic 초격자(점유 Li 와 빈자리의 교대 정렬)는 동종 이웃 인력 $\Omega_j>0$ 이 가운데를 위로 미는 이중웰(식~\eqref{eq:gxi})의 LCO 사례다. 두 전이 $j\in\{\mathrm{T2},\mathrm{T3}\}$ 각각에 $\Omega_j$ 를 배정한다.
>
> **(b) 연산 — spinodal 값 대입.** 식~\eqref{eq:spinodal} 에 LCO $\Omega_j$ 를 넣으면 두 전이의 변곡점이
> $$u_j=\sqrt{1-\frac{2RT}{\Omega_j}},\qquad \xi_{s,j}^\pm=\tfrac12(1\pm u_j)\qquad(j=\mathrm{T2},\mathrm{T3};\ \Omega_j>2RT),$$
> 로 정해지고, 두-상 조건은 T2·T3 각각 $\Omega_{\mathrm{T2}},\Omega_{\mathrm{T3}}>2RT\approx4958$ J/mol(@298 K)이다.
>
> **(c) 중간식 — gap 을 LCO $\Omega_j$ 로.** 식~\eqref{eq:dUhys} 에 위 $u_j$ 를 대입하면 두 order–disorder 전이의 spinodal 상한 gap 이
> $$\Delta U_j^\hys=\frac{2}{F}\Big[\Omega_j\,u_j-2RT\,\mathrm{artanh}\,u_j\Big],\qquad j=\mathrm{T2},\mathrm{T3},$$
> 로 *같은 함수, 다른 $\Omega_j$* 로 두 개 나온다 — T2($\sim$4.05 V)·T3($\sim$4.17–4.20 V) 가 두 개의 좁은 peak 로 갈라지는 것이 이 두 gap 의 발현이다. 방향별 분기 중심은 식~\eqref{eq:Ubranch} 로 $U_j^{\,d}=U_j+\tfrac12\sigma_d h_{\eta,j}\gamma_j\Delta U_j^\hys$ 이며 $U_j^{\dis}>U_j^{\chg}$(방전 중심이 충전보다 높음)가 T2·T3 에도 그대로 성립한다.
>
> **(d) 박스 — config $\Delta S$ 의 출처 연결.** 이 정렬의 charge-order 엔트로피 변화가 표~\ref{tab:lco-staging} 의 config 주도 $\Delta S_{\rxn,j}^\mathrm{cat}$ 값이다:
> $$\Delta S^\mathrm{config}\approx0.47\ \text{J/K·mol}\ (x{=}\tfrac12,\ \text{T2}),\qquad
> \Delta S^\mathrm{config}\approx1.49\ \text{J/K·mol}\ (x{=}\tfrac23,\ \text{T3})\quad[\text{tier A}].$$
> 곧 T2·T3 는 전자항 off(표~\ref{tab:lco-staging}), config 단독으로 spinodal·gap·config $\Delta S$ 가 모두 흑연 two-phase 전이와 *같은 식*으로 닫힌다.

**논리 감사 (hys B.2)**: 무결. 결과식(spinodal·gap·분기 중심)·부호($\Delta U_j^\hys\ge0$·$U_j^{\dis}>U_j^{\chg}$)·수치(0.47/1.49 J/K·mol·$\sim$4.05/4.17 V·$2RT\approx4958$ J/mol) 전부 원문 그대로. 재작성은 흑연 `sec:hys` 의 두 결과식(\eqref{eq:spinodal}·\eqref{eq:dUhys})에 LCO $\Omega_{\mathrm{T2}},\Omega_{\mathrm{T3}}$ 를 **대입한 중간식**을 새로 적었을 뿐이며, 흑연 식을 재유도하지 않는다(중복 유도 금지 준수). $\Omega_j$ 수치는 원문에 없어(피팅 대상 초기값) 기호로만 두었다 — 허위 정밀 금지(tier).

## B.3 (T1) MIT 2상역 — 구조 two-phase + 전자항 분리 (이중계산 방지)

**원 줄글 (L696–701, 대비)**:
> $x\approx0.75$–$0.94$ 의 절연체→금속 천이(MIT)도 2상 공존역이다 … 이 구간 역시 식~\eqref{eq:dUhys}·\eqref{eq:Ubranch} 의 spinodal gap·분기 중심을 *그대로 받는다* … 다만 MIT 에는 격자기체 config 만으로 닫히지 않는 *전자 자유도* … 가 있어, 엔트로피에 흑연엔 없는 항이 하나 더 붙는다 … 여기서는 "MIT 의 구조적 2상역은 정규용액 틀로, 전자 자유도는 별도 항으로" 두 몫을 분리한다는 점만 못박는다.

→ "그대로 받는다"가 대입 없이 서술. 구조 two-phase 의 $\Omega_{\mathrm{T1}}$ 대입식·전자항 분리의 **가산 식**이 없다(`V1010_LCO_STYLE_REPORT` §1: "order-disorder·MIT·도핑 '같은 틀 그대로 적용' 서술 3회").

**재작성 수식 사슬 (a→d)**:

> **(a) 출발 — MIT 의 두 자유도.** T1 MIT($x\approx0.75$–$0.94$, $\sim$3.9 V plateau)는 *구조* 상분리(격자기체 config)와 *전자* 자유도(전도 전자 상태밀도 변화)를 함께 갖는다. 히스테리시스를 낳는 것은 구조 몫이므로, 정규용액 틀은 config 상호작용 $\Omega_{\mathrm{T1}}$ 에만 건다.
>
> **(b) 연산 — 구조 몫에 $\Omega_{\mathrm{T1}}$ 대입.** T2·T3 와 같은 식으로, 구조 two-phase 의 spinodal·gap 이
> $$u_{\mathrm{T1}}=\sqrt{1-\frac{2RT}{\Omega_{\mathrm{T1}}}},\quad
> \Delta U_{\mathrm{T1}}^\hys=\frac{2}{F}\Big[\Omega_{\mathrm{T1}}u_{\mathrm{T1}}-2RT\,\mathrm{artanh}\,u_{\mathrm{T1}}\Big]\quad(\Omega_{\mathrm{T1}}>2RT),$$
> 로 닫히고, 분기 중심 $U_{\mathrm{T1}}^{\,d}=U_{\mathrm{T1}}+\tfrac12\sigma_d h_{\eta}\gamma_{\mathrm{T1}}\Delta U_{\mathrm{T1}}^\hys$(식~\eqref{eq:Ubranch})가 MIT plateau 의 충방전 히스를 적는다 — 여기까지 흑연·T2·T3 와 *완전히 같은 식*.
>
> **(c) 중간식 — 전자항을 별도 몫으로 가산(이중계산 방지).** MIT 고유의 전자 자유도는 히스가 아니라 *엔트로피*에 하나의 항을 더한다. 전이 엔트로피가 config·vib·elec 직교 가산(식~\eqref{eq:lco-decomp})이므로 T1 만
> $$\Delta S_{\rxn,\mathrm{T1}}^\mathrm{cat}(x,T)=\underbrace{\Delta S^\mathrm{config}_{\mathrm{T1}}+\Delta S^\mathrm{vib}_{\mathrm{T1}}}_{\text{구조·진동 (}T\text{-무관)}}+\underbrace{\Delta S_{e,\mathrm{T1}}(x,T)}_{\text{전자 (MIT 게이트, }\propto T)},$$
> 로 적고, 구조 히스(위 (b)의 $\Omega_{\mathrm{T1}}$)와 전자 엔트로피($\Delta S_e$, \S\ref{sec:lco-electronic})는 *서로 다른 몫*이라 겹치지 않는다 — config 상호작용은 히스·gap 을, 전자항은 $\partial U_1/\partial T$ 의 $T$-선형 성분(식~\eqref{eq:U1T2} 의 $T^2$ 곡률)을 각각 담당한다.
>
> **(d) 박스 — 두 몫 분리 원칙.**
> $$\boxed{\ \text{MIT 구조 2상역} \Rightarrow \Omega_{\mathrm{T1}}\ (\text{식~\eqref{eq:dUhys}·\eqref{eq:Ubranch} 히스}),\qquad
> \text{MIT 전자 자유도} \Rightarrow \Delta S_{e,\mathrm{T1}}\ (\text{식~\eqref{eq:lco-decomp} 별도 가산})\ }$$
> 이 분리가 이중계산 방지의 출발점이며, 전자항 부호는 삽입 기준 $\Delta S_{e,\mathrm{T1}}<0$(탈리튬화 방출 $|\Delta S_{e,\mathrm{T1}}|>0$, \S\ref{sec:lco-electronic})로 A.2 좌표와 일관한다.

**논리 감사 (hys B.3)**: 무결. 결과식·부호·수치 불변. 두 몫 분리(config→히스, elec→$\Delta S$)는 원문 L698–701 의 "두 몫을 분리한다"를 **가산 식**으로 명시한 것이며, 신규 물리 0(전자항 자체 유도는 `sec:lco-electronic` 소관이라 참조만). $\Delta S_e\propto T$·$T^2$ 곡률(식~\eqref{eq:U1T2})은 원문에 이미 있는 결과라 참조로 연결 — A.2·B.3 의 부호 좌표가 삽입-기준으로 일치함을 재확인.

## B.4 도핑 보정 — Ω_j 를 2RT 쪽으로 낮추는 대입

**원 줄글 (L703–707, 대비)**:
> Al³⁺/Mg²⁺ 비-redox 치환은 Co redox 와 전자항을 보존하되 order–disorder·MIT 상전이를 *억제*한다 — 정규용액 틀에서 이는 $\Omega_j$ 를 $2RT$ 쪽으로 낮춰 … peak 를 smear 하고 $U_j$ 를 미세 shift 시키는 것으로 들어온다. … pure-LCO 의 $\Omega_j$ 가 초기값이고 도핑에 따른 폭·shift 는 우리 데이터로 피팅한다.

→ "$\Omega_j$ 를 $2RT$ 쪽으로 낮춘다"가 방향 서술만. 문턱 접근이 gap·폭에 주는 정량 효과(극한)를 식으로 보이지 않음.

**재작성 수식 사슬 (a→d)**:

> **(a) 출발 — 도핑의 작용점.** Al³⁺/Mg²⁺ 비-redox 치환은 Co redox·전자항을 보존하므로 $\Delta S_e$·$U_j$ 의 큰 골격은 두고, order–disorder·MIT 상전이를 *억제*한다. 정규용액 틀에서 이 억제는 상호작용의 감소, 곧 $\Omega_j^\mathrm{dope}<\Omega_j^\mathrm{pure}$ 로 들어온다.
>
> **(b) 연산 — 문턱 접근의 gap 극한.** $\Omega_j$ 가 $2RT$ 로 내려가면 식~\eqref{eq:spinodal} 의 $u_j=\sqrt{1-2RT/\Omega_j}\to0^+$ 이고, 식~\eqref{eq:dUhys} 를 $u_j\!\to\!0$ 에서 Taylor 전개(원문 L622, $\mathrm{artanh}\,u=u+u^3/3+\cdots$)하면
> $$\Delta U_j^\hys\to\frac{8RT}{3F}\,u_j^3\to0,\qquad u_j^3\propto(T_{c,j}-T)^{3/2},\ \ T_{c,j}=\frac{\Omega_j}{2R}.$$
> **(c) 중간식 — 폭으로의 이전.** 히스 gap 이 줄면($\Delta U_j^\hys\to0$), 두-상 plateau 가 풀려 그 전이는 단상($\Omega_j\le2RT$) 쪽으로 이동한다 — \S\ref{sec:width} 이중지위에서 두-상의 *현상학적 피팅 폭*이 단상의 *평형 예측 폭* $w_j=n_jRT/F$ 로 바뀌고, `sec:broadening` 의 broadening 폭이 더 큰 몫을 차지한다(원문 L704–705 의 서술을 극한식으로 회수).
>
> **(d) 결론 — 초기값·피팅 규율.** pure-LCO $\Omega_j$ 가 초기값이고(허위 정밀 금지, tier), 도핑에 따른 $\Omega_j$ 감소분·$U_j$ shift·폭은 우리 데이터로 피팅한다 — 흑연 `GRAPHITE\_STAGING\_LIT`(초기값→피팅 override)와 동일 철학. 곧 도핑은 *새 항이 아니라 기존 $\Omega_j$ 의 값 이동*으로 들어온다(신규 개념 0).

**논리 감사 (hys B.4)**: 무결. $u_j\to0$ 극한·Taylor 계수($8RT/3F$)·$T_{c,j}=\Omega_j/2R$ 는 원문 흑연 `sec:hys` L621–623 에 이미 유도된 결과라 **재유도 없이 대입만**. 도핑이 $\Omega_j$ 값 이동으로 들어온다는 것은 원문 결론과 동일 — 극한식이 그 방향 서술을 정량 회수했을 뿐. 부호·물리 불변.

---

## C. 종합 논리 감사 (물리 소당성·부호·차원·극한·detailed balance)

| 항목 | 검산 | 결과 |
|---|---|---|
| **물리 인과** | center: host 라벨이 $(\Delta H,\Delta S)$ 값으로만 진입 / hys: 정렬·MIT 가 $\Omega_j>0$ 로 진입 | 무결 (인과 방향 원문과 일치) |
| **부호** | $\partial U_j/\partial T=\Delta S/F$(흑연 1:1) · $\Delta U_j^\hys\ge0$ · $U_j^{\dis}>U_j^{\chg}$ · $\Delta S_{e,\mathrm{T1}}<0$(삽입) | 무결. 단 center 검산의 부호 *읽는 좌표* 미명시 → A.2 좌표 고정 문장 보완(모순 아님, 명시 결함) |
| **차원** | $[\Delta S/F]=$ (J/mol·K)/(C/mol)$=$V/K ✓ · $[\Omega u/F]=$ (J/mol)/(C/mol)$=$V ✓ · $[2RT\,\mathrm{artanh}\,u/F]=$V ✓ | 무결 |
| **극한** | $\Omega_j\!\to\!2RT^+\Rightarrow\Delta U_j^\hys\!\to\!0$(연속) · $|I|\!\to\!0\Rightarrow V_n=V_\app$ · 도핑 $\Omega\!\downarrow\Rightarrow$ 히스 소멸 | 무결 (원문 극한과 일치) |
| **detailed balance** | hys 는 $g''=0$ spinodal 경로(자유에너지)로, `sec:width` 는 속도식 정지점(kinetic) 경로로 같은 $\xi_\eq$ 도달 — 두 절 무모순 | 무결 (본 supplement 는 hys 자유에너지 경로만 다룸, DB 경로 불변) |
| **이중계산** | MIT config(히스)와 elec($\Delta S$) 직교 가산 → 겹침 0 | 무결 (B.3 (c) 가산식이 명시) |

**정합 결함 2건 (오류 아닌 명시 공백)**:
1. center verifybox 부호 검산의 **읽는 좌표 미명시**(단전극 potentiometric vs 삽입-반응) → A.2 좌표 고정 문장으로 보완. 물리·수치 불변.
2. hys 도입의 **two-phase calibration 대응 공백**(흑연 2개 vs LCO 전이 집합) → B.1 (b) 문턱 대응식으로 보완. 문턱 판정 식 동일.

두 건 모두 **유도 오류가 아니라** 흑연 forward 의 정합 문장이 LCO 절에 이식되지 않아 생긴 명시 공백이며, 보완은 물리·결과식·부호·수치를 **바꾸지 않는다**.

---

## D. 5줄 요약

1. **center 수식화**: 전극무관 논증을 `eq:n0map`→`eq:eqcond`→`eq:Uj` 대입 사슬(A.1)로, $\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$ 를 Gibbs–Helmholtz + $\Delta G=-FU$ 다리 (a→d)(A.2)로 — 흑연 `sec:center` L458–459 의 다리를 LCO 절에 명시 이식.
2. **hys 수식화**: 흑연 $\mu(\theta)\!\to\!g''\!\to\!\xi_s^\pm\!\to\!\Delta U_j^\hys=(2/F)[\Omega_j u-2RT\,\mathrm{artanh}\,u]$ 사슬에 LCO $\Omega_j$(T2·T3 order–disorder·T1 MIT)를 **대입한 중간식**으로 "같은 틀 적용" 3회를 각각 유도(B.2·B.3·B.4), MIT 전자항은 별도 가산으로 이중계산 방지.
3. **논리 결함 발견**: 진짜 유도 오류 **0**. 정합 명시 결함 **2건**(center 부호 좌표 미명시·hys two-phase calibration 대응 공백) — 근거와 보완 문장 제시, 둘 다 물리 불변.
4. **물리 불변 확인**: 결과식($U_j$·$\partial U_j/\partial T$·spinodal·$\Delta U_j^\hys$)·부호·수치(+0.83 mV/K·+80 J/mol·K·0.47/1.49 J/K·mol·$x_\mathrm{MIT}\approx0.85$·$2RT\approx4958$ J/mol) 전부 원문 그대로, 신규 개념 0.
5. **가장 약했던 원 줄글**: `sec:lco-hys` L684–701 의 "같은 정규용액 틀 그대로 적용"·"식~\eqref{eq:dUhys}·\eqref{eq:Ubranch} 를 그대로 받는다" — LCO $\Omega_j$ 를 spinodal·gap 에 넣은 중간식이 한 줄도 없어 G-derive 최대 위반이었고, B.2·B.3 이 이를 대입 중간식으로 해소.
