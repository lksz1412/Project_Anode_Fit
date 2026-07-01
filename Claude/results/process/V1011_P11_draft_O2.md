# V1011 Phase 1.1 — LCO 수식화 드래프트 (ID = O2, Opus)

> 대상 = `docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex` 의 `sec:lco-center`(L470–513)·`sec:lco-hys`(L684–708).
> 산출 = 이 두 절을 흑연 forward 절((a)출발식→(b)적용연산→(c)중간식≥1→(d)박스)처럼 수식-주도로 재작성하는 **supplement 드래프트**.
> ★드래프트만 — tex/코드 편입은 master. 아래 재작성안은 삽입 위치·재작성 수식 사슬·원 줄글 대비·논리 감사 결과를 절별로 담는다.
> 물리·결과식·부호·수치 원칙 불변(줄글→수식, 전개 형식만). 신규 개념(ρ(U_app)/PSD·ρ_G·새 물리) 도입 없음. `sec:lco-map`·`sec:lco-Se`·`sec:lco-gate`·N7–9·전자엔트로피 절 미접촉.

---

## 정독 근거 (줄·식 인용, 추정 없음)

- **흑연 forward 정답 예시 (재작성의 형식·부호 기준)**
  - `sec:center` L405–468: eq:eqcond(L433–437, $\Delta G_j=-sFU_j$)·eq:Uj(L452–454)·∂U/∂T 다리(L457–459, Gibbs 항등식 $\partial\Delta G/\partial T=-\Delta S$ + $\Delta G=-FU$).
  - `sec:hys` L515–682: μ(θ) eq:mu(L531–534) → g(ξ) eq:gxi(L537–540) → g″ eq:gpp(L544–547) → spinodal eq:spinodal(L550–554) → V_eq eq:Veq(L587–590) → 대입 eq:hyssub(L596–601) → 차 eq:hysdiff(L604–611) → 박스 eq:dUhys(L614–619). 이 8-식 사슬이 (a)→(d) 정답 밀도.
- **재작성 대상 (줄글 회귀 확정)**
  - `sec:lco-center` L470–513: 전극무관 논증 단정(L471–476)·∂U_j/∂T 괄호 전보체(L477–482). `V1010_LCO_STYLE_REPORT.md` §1 center 행 HIGH×2.
  - `sec:lco-hys` L684–708: order-disorder·MIT·도핑 "같은 틀 그대로 적용" 서술 3회, Ω_j 대입 중간식 전무. STYLE_REPORT §1 hys 행 HIGH×3.
- **SPEC·calibration**
  - `AUTHOR_BRIEF.md`: ∂U/∂T=ΔS/F 부호 흑연 1:1(L22)·config+vib+elec 분해(L36)·단전극 dφ/dT≈+0.83 mV/K[tier B](L38).
  - `R1_broadening.md` D7(L49): "LCO T1·T2·T3 두-상도 해당" — 흑연 two-phase=2(LiC₁₂·LiC₆)와 별개로 **LCO 세 전이 전부 two-phase(Ω_j>2RT)**. tex L686·L707·L1209 와 정합(pure-LCO Ω_j = 피팅 초기값).

---

# A. sec:lco-center 재작성안 (양극 ∂U_j/∂T)

**삽입 위치.** L470 subsection 헤더 직후 ~ L488(검산 박스 L490 직전)까지의 줄글(L471–488)을 아래 (a)→(d) 수식 사슬로 대체. **L490–509 검산 박스(`verifybox`)·L511–512 다리 문장은 그대로 보존** — 검산 박스는 이미 수치 검산·단전극/전셀 혼동 가드·전자항 공존이 잘 서술돼 있어 손대지 않는다(과수정 경계).

## A-①  전극무관 논증 — 단정 비약 → eq:eqcond 재유도 대입

원 줄글(L471–476)은 "식 eq:Uj 는 유도에 전극 가정이 없다 … 평형 조건 eq:eqcond 에서 곧장 나오므로 LCO 양극에도 그대로 성립한다"를 **단정**한다. 흑연 forward `sec:center`(L422–454)의 유도를 되짚으면 이 단정이 실제로 어느 단계에서 전극무관인지 보이므로, 그 대입을 명시한다.

**(a) 출발 — 전극을 고르지 않은 두 다리.**
흑연 평형 조건 eq:eqcond 는 전기화학 평형 $\tilde\mu_{\mathrm{Li}^+}+\tilde\mu_{e^-}=\tilde\mu_\mathrm{Li}$(eq:eqbalance, L427)에서 나왔고, 이 균형식은 삽입 반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$ 의 host 가 흑연인지 LCO인지 **묻지 않는다** — host 종의 화학 정체는 상수 덩이 $\mu^0$ 에만 들어가고 전위 의존은 전자항 $\tilde\mu_{e^-}=\mu_{e^-}^0-FV$ 하나뿐이다. 따라서 host 를 양극으로 바꿔도 다리는
$$
\Delta G_j=-sF\,U_j\qquad(\text{eq:eqcond, host 불문}),\qquad
\Delta G_j=\Delta H_{\rxn,j}^{\mathrm{cat}}-T\,\Delta S_{\rxn,j}^{\mathrm{cat}}
$$
두 개가 그대로다.

**(b) 적용 — 두 다리를 같은 자리에서 잇는다.**
흑연 eq:Ujmid(L446–449)와 똑같이 두 표현을 등치한다 — 바뀌는 것은 입력 위첨자 $(\cdot)^\mathrm{cat}$ 뿐이다:
$$
\Delta H_{\rxn,j}^{\mathrm{cat}}-T\,\Delta S_{\rxn,j}^{\mathrm{cat}}=-F\,U_j\qquad(s=+1).
$$

**(c) 중간식 — $U_j$ 로 이항.**
$$
U_j(T)=-\frac{\Delta H_{\rxn,j}^{\mathrm{cat}}-T\,\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}
=\frac{-\Delta H_{\rxn,j}^{\mathrm{cat}}+T\,\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}.
$$
이 식은 흑연 eq:Uj 와 **문자 하나 다르지 않고**(위첨자만 `cat`), 대입 자리(eq:eqcond)가 host 불문이라는 (a)의 관찰이 곧 "전극무관"의 내용이다. LCO 양극의 높은 중심($\sim$3.9–4.2 V)은 삽입 반응의 큰 음의 $\Delta H_{\rxn}^{\mathrm{cat}}$(분자 $-\Delta H_{\rxn}^{\mathrm{cat}}$ 가 크게 양)에서 오고, 흑연의 $\sim$0.1 V 와 같은 식·다른 입력이다.

**(d) 박스 — 양극 평형 중심.**
$$
\boxed{\;U_j^{\mathrm{cat}}(T)=\frac{-\Delta H_{\rxn,j}^{\mathrm{cat}}+T\,\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}\;}
\qquad(\text{eq:Uj 의 host}=\text{LCO 특수화, eq:eqcond 가 host 불문}).
$$

**원 줄글 대비.** L471–476의 "유도에 전극 가정이 없다 … 그대로 성립한다"(단정)를, eq:eqbalance→eq:eqcond 가 host 종을 $\mu^0$ 상수로만 흡수한다는 (a)의 관찰 + (b)(c) 대입으로 대체 — 단정을 **대입 식으로 회수**했다. 물리·부호·결과식 불변(위첨자 `cat` 부기만 추가).

## A-②  ∂U_j/∂T — 괄호 전보체 → Gibbs 항등식 다리 완결 문장

원 줄글(L477–482)은 "온도 의존도 같은 미분이다"라는 한 줄 뒤 곧장 eq:lco-dUdT($\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$)를 놓고 "(식 eq:Uj 의 $T$ 미분, 전극 불문)"이라는 **괄호 전보체**로 닫는다. 흑연 forward `sec:center` L457–459 는 이미 이 미분을 **Gibbs 항등식 다리**로 완결 문장화했으므로(그러나 그 다리는 흑연 절에만 있고 LCO 절엔 옮겨오지 않았다), 같은 다리를 완결 문장으로 옮긴다.

**(a) 출발 — Gibbs 항등식.**
등압에서 반응 자유에너지의 온도 미분은 반응 엔트로피의 음수다:
$$
\frac{\partial(\Delta G_j)}{\partial T}\Big|_P=-\Delta S_{\rxn,j}^{\mathrm{cat}}\qquad(\text{Gibbs 항등식}).
$$

**(b) 적용 — eq:eqcond 의 $\Delta G_j=-FU_j$ 를 좌변에 대입.**
$s=+1$ 에서 $\Delta G_j=-FU_j$(A-① (a)) 를 양변 미분하면 $\partial(\Delta G_j)/\partial T=-F\,\partial U_j/\partial T$ 이고, 이를 (a) 좌변에 넣는다:
$$
-F\,\frac{\partial U_j}{\partial T}=-\Delta S_{\rxn,j}^{\mathrm{cat}}.
$$

**(c) 중간식 — $-F$ 로 나눔.**
$$
\frac{\partial U_j}{\partial T}=\frac{\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}.
$$
같은 결과를 eq:Uj 를 직접 $T$ 미분해서도 얻는다 — $-\Delta H_{\rxn,j}^{\mathrm{cat}}$ 는 $T$ 무관, $T\,\Delta S_{\rxn,j}^{\mathrm{cat}}$ 의 미분이 $\Delta S_{\rxn,j}^{\mathrm{cat}}$ 이므로 $\partial U_j/\partial T=\Delta S_{\rxn,j}^{\mathrm{cat}}/F$. 두 경로가 같은 값에 닿는 것이 흑연 L458 의 "Gibbs 항등식과 eq:eqcond 를 잇는 것과 같다"의 내용이며, 이 이중 경로 자체가 전극무관(어느 경로도 host 정보를 쓰지 않는다)의 재확인이다.

**(d) 박스 — 양극 온도 계수.**
$$
\boxed{\;\frac{\partial U_j^{\mathrm{cat}}}{\partial T}=\frac{\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}\;}
\qquad(\text{eq:lco-dUdT; 흑연과 부호까지 1:1, 값만 }\Delta S_{\rxn,j}^{\mathrm{cat}}).
$$
LCO 의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 는 `sec:lco-decomp`(eq:lco-decomp)에서 config·vib·전자 세 성분으로 분해되며, 여기서는 부호·크기 sanity 만 확인한다 — 이 (d) 박스 뒤에 원 L483–488(대표 스케일 $\dd\phi/\dd T\approx+0.83$ mV/K → $\Delta S_\rxn\approx+80$ J/(mol·K)[tier B], 흑연 전이별 $+29/0/-5/-16$ 과 값은 다르나 관계식 동일)과 L490–509 검산 박스를 **그대로 이어붙인다**(그 서술은 이미 완결).

**원 줄글 대비.** L477–482의 괄호 전보체 "(식 eq:Uj 의 $T$ 미분, 전극 불문)"을, Gibbs 항등식(a)→eq:eqcond 대입(b)→나눗셈(c)의 완결 문장 사슬 + eq:Uj 직접 미분의 이중 경로로 대체. 물리·부호·결과식 불변(eq:lco-dUdT 그대로 재유도).

---

# B. sec:lco-hys 재작성안 (order-disorder·MIT·도핑)

**삽입 위치.** L684 subsection 헤더 직후 ~ L707(L708 절 종료 직전)까지의 줄글 세 문단(L685–708: order-disorder·MIT·도핑 "같은 틀 그대로 적용" 서술 3회)을 아래 (B-0 다리) + (B-① order-disorder) + (B-② MIT) + (B-③ 도핑) 수식-주도 대입 사슬로 대체. `sec:hys`(L515–682, 흑연 정답 사슬)은 **미접촉**(LCO 절이 그 결과식을 대입만 함).

## B-0  LCO calibration 선언 — 어느 전이가 정규용액 two-phase인가 (★base 요구)

원 줄글 L685–687 은 "그 가정이 서는 LCO 양극에도 그대로 적용된다 — Ω_j 의 값만 LCO 상전이가 정한다 … 세 전이 모두에 대응한다"를 서술만 한다. base 프롬프트 요구("★two-phase = LiC 계열 아닌 LCO는 어느 전이가 정규용액 two-phase인지 명시")에 따라, **흑연과 LCO 의 two-phase 카운트가 다름**을 못박는 한 문장을 먼저 놓는다.

- **흑연**: 표 tab:staging 네 전이 중 피팅 후 two-phase(Ω_j>2RT 유지)는 $2\mathrm L\!\to\!2$($\mathrm{LiC_{12}}$)·$2\!\to\!1$($\mathrm{LiC_6}$) **두 개만**이고, dilute→stage4·$4\mathrm L\!\leftrightarrow\!3\mathrm L$ 은 solid-solution(Ω_j<2RT)이다(`sec:width` L738–741·R1_broadening calibration).
- **LCO**: 세 전이 T1(MIT)·T2·T3(order-disorder) 이 **전부 two-phase**(Ω_j>2RT)다(tex L686·L707·L1209·R1_broadening D7 L49). 곧 LCO 하프셀은 solid-solution 전이가 없이 세 전이 모두 spinodal 문턱을 넘는 상분리다 — 이것이 흑연(4 중 2)과 LCO(3 중 3)의 calibration 차이다.

$$
\underbrace{\{\,2\mathrm L\!\to\!2,\ 2\!\to\!1\,\}}_{\text{흑연 two-phase (4 중 2)}}
\quad\longleftrightarrow\quad
\underbrace{\{\,\text{T1(MIT)},\ \text{T2, T3(order-disorder)}\,\}}_{\text{LCO two-phase (3 중 3)}}\ :\ \Omega_j>2RT.
$$

pure-LCO 의 $\Omega_j$ 는(흑연 $\Omega_j$ 초기값이 그러하듯) 신뢰값 아닌 **피팅 초기값**이므로 아래 대입은 수치가 아니라 $\Omega_j>2RT$ 문턱을 넘긴 **기호** $\Omega_j$ 로 전개한다(허위 정밀 금지).

## B-①  (T2·T3) order-disorder — 정규용액 Ω_j 실제 대입

**(a) 출발 — LCO order-disorder 를 격자기체로.**
$x\approx0.5$ 부근 $\mathrm{Li}_x\mathrm{CoO_2}$ 의 점유 리튬/빈자리 교대 정렬(monoclinic 초격자)은 "동등한 자리에 리튬이 차고 빈다"는 `sec:hys` 가정을 만족하는 상분리다. 흑연 eq:gxi(L537–540)의 자유에너지를 그대로 받되 상호작용을 LCO order-disorder 값 $\Omega_{\mathrm{od}}$ 로 특수화한다:
$$
g_j(\xi)=g_j^0+RT\big[\xi\ln\xi+(1-\xi)\ln(1-\xi)\big]+\Omega_{\mathrm{od}}\,\xi(1-\xi),
\qquad \Omega_{\mathrm{od}}>0\ (\text{동종 이웃 인력, 이중웰}).
$$

**(b) 적용 — 두 번 미분해 spinodal 근.**
흑연 eq:gpp(L544–547)·eq:spinodal(L550–554)에 $\Omega_j\to\Omega_{\mathrm{od}}$ 를 넣으면
$$
g_j''(\xi)=\frac{RT}{\xi(1-\xi)}-2\Omega_{\mathrm{od}},
\qquad
\xi_{s,j}^\pm=\tfrac12\big(1\pm u_{\mathrm{od}}\big),\quad
u_{\mathrm{od}}\equiv\sqrt{1-\frac{2RT}{\Omega_{\mathrm{od}}}}\ \ (\Omega_{\mathrm{od}}>2RT).
$$

**(c) 중간식 — LCO order-disorder 분기 gap.**
흑연 eq:hysdiff(L604–611)의 극대−극소 차에 $u_j\to u_{\mathrm{od}}$·$\Omega_j\to\Omega_{\mathrm{od}}$ 를 대입한다:
$$
\Delta U_{\mathrm{od}}^\hys
=V_{\eq}(\xi_{s}^-)-V_{\eq}(\xi_{s}^+)
=\frac{2}{F}\Big[\Omega_{\mathrm{od}}\,u_{\mathrm{od}}-2RT\,\mathrm{artanh}\,u_{\mathrm{od}}\Big].
$$

**(d) 박스 — 두 개 좁은 peak 의 분기.**
$$
\boxed{\;\Delta U_{\mathrm{od}}^\hys=\frac{2}{F}\Big[\Omega_{\mathrm{od}}\,u_{\mathrm{od}}-2RT\,\mathrm{artanh}\,u_{\mathrm{od}}\Big],\quad
u_{\mathrm{od}}=\sqrt{1-\frac{2RT}{\Omega_{\mathrm{od}}}}\;}
$$
한 쌍 전이(T2 $\sim$4.05 V hex→monoclinic, T3 $\sim$4.17 V monoclinic→hex)가 $\Omega_{\mathrm{od}}>2RT$ 로 spinodal 문턱을 넘어 두 개의 좁은 peak 로 갈라지고, 각 전이의 방향별 분기 중심은 흑연 eq:Ubranch(L634–637)를 그대로 받아
$U_j^{\,d}=U_j+\tfrac12\sigma_d h_{\eta,j}\gamma_j\,\Delta U_{\mathrm{od}}^\hys$ 다.

**★config ΔS 와 Ω 의 구분(이중계산·혼동 가드).** 정렬의 charge-order 엔트로피 변화($\approx0.47$ J/K·mol@$x{=}\tfrac12$·$\approx1.49$ J/K·mol@$x{=}\tfrac23$[tier A, Motohashi])는 **config $\Delta S$**(eq:lco-decomp 의 config 슬롯·tab:lco-staging 출처)이지, 위 정규용액 상호작용 $\Omega_{\mathrm{od}}$ 가 **아니다** — 둘은 서로 다른 양이다($\Delta S$ 는 엔트로피, $\Omega$ 는 상호작용 에너지). 따라서 재작성 시 "Motohashi 0.47/1.49 → $\Omega_{\mathrm{od}}$" 식의 다리를 놓아선 안 되고, $\Omega_{\mathrm{od}}$ 는 히스 gap 을 정하는 별도 피팅 파라미터로 둔다. (이 구분은 원 줄글에도 암묵적이나 명시가 없어 오독 여지가 있었음 — 아래 논리 감사 참조.)

## B-②  (T1) MIT 2상역 — spinodal gap 대입 + 전자 자유도 분리

**(a) 출발 — MIT plateau 를 격자기체 config 로.**
$x\approx0.75$–0.94 절연체→금속 천이(MIT, plateau $\sim$3.9 V)의 **구조적 2상 공존**은 order-disorder 와 같은 격자기체 config 자유도로 적는다 — 상호작용을 MIT 값 $\Omega_{\mathrm{MIT}}$ 로 특수화:
$$
g_1(\xi)=g_1^0+RT\big[\xi\ln\xi+(1-\xi)\ln(1-\xi)\big]+\Omega_{\mathrm{MIT}}\,\xi(1-\xi),\qquad \Omega_{\mathrm{MIT}}>2RT.
$$

**(b) 적용 — spinodal·gap 대입.**
B-①과 같은 대입으로
$$
u_{\mathrm{MIT}}=\sqrt{1-\frac{2RT}{\Omega_{\mathrm{MIT}}}},\qquad
\Delta U_{\mathrm{MIT}}^\hys=\frac{2}{F}\Big[\Omega_{\mathrm{MIT}}\,u_{\mathrm{MIT}}-2RT\,\mathrm{artanh}\,u_{\mathrm{MIT}}\Big].
$$

**(c) 중간식 — 분기 중심.**
$$
U_1^{\,d}=U_1+\tfrac12\,\sigma_d\,h_{\eta,1}\,\gamma_1\,\Delta U_{\mathrm{MIT}}^\hys\qquad(\text{eq:Ubranch, }j{=}\text{T1 특수화}).
$$

**(d) 박스 — 두 몫 분리(config regular-solution + 전자 자유도).**
$$
\boxed{\;\underbrace{\Delta U_{\mathrm{MIT}}^\hys=\tfrac{2}{F}\big[\Omega_{\mathrm{MIT}}u_{\mathrm{MIT}}-2RT\,\mathrm{artanh}\,u_{\mathrm{MIT}}\big]}_{\text{구조적 2상역: 정규용액 틀(이 절)}}
\ \|\ 
\underbrace{\Delta S_{e,1}(x,T)}_{\text{전자 자유도: 별도 항(sec:lco-electronic)}}\;}
$$
MIT 에는 격자기체 config 만으로 닫히지 않는 **전자 자유도**(전도 전자 상태밀도 변화)가 있어 엔트로피에 흑연엔 없는 항 $\Delta S_{e,1}$ 이 하나 더 붙는다 — 그러나 그 항은 $U_1(T)$ 의 중심(eq:lco-decomp)에 들어가고, **히스 gap** $\Delta U_{\mathrm{MIT}}^\hys$ 은 config 상호작용 $\Omega_{\mathrm{MIT}}$ 만으로 정해진다(구조적 2상역은 정규용액 틀로, 전자 자유도는 별도 항으로 — 이중계산 방지의 출발). 이 분리가 원 L698–701 의 "두 몫을 분리한다는 점만 못박는다"를 **박스 한 줄로 못박은 것**이다.

## B-③  도핑 보정 — Ω_j 를 2RT 쪽으로 낮추는 대입

**(a) 출발 — 비-redox 치환의 상전이 억제.**
Al³⁺/Mg²⁺ 비-redox 치환은 Co redox·전자항을 보존하되 order-disorder·MIT 상전이를 **억제**한다. 정규용액 틀에서 상전이 강도는 $\Omega_j$ 가 문턱 $2RT$ 위로 얼마나 떨어져 있느냐로 재는 양이므로, 도핑은 $\Omega_j$ 를 $2RT$ 쪽으로 낮추는 것으로 들어온다:
$$
\Omega_j^{\text{doped}}=\Omega_j^{\text{pure}}-\delta\Omega(\text{도핑}),\qquad \Omega_j^{\text{doped}}\to 2RT^+.
$$

**(b) 적용 — $u_j$·gap 의 문턱 극한.**
$\Omega_j\to2RT^+$ 이면 $u_j=\sqrt{1-2RT/\Omega_j}\to0$ 이고, 흑연 L621–623 의 Taylor 전개($\mathrm{artanh}\,u=u+u^3/3+\cdots$)로
$$
\Delta U_j^\hys=\frac{2}{F}\big[\Omega_j u_j-2RT\,\mathrm{artanh}\,u_j\big]
\ \xrightarrow{\ u_j\to0\ }\ \frac{8RT}{3F}\,u_j^3\to0.
$$

**(c) 중간식 — 히스 소멸·평탄역 풀림.**
곧 도핑이 $\Omega_j$ 를 $2RT$ 로 낮출수록 spinodal gap $\Delta U_j^\hys$ 와 히스가 $u_j^3\propto(T_{c,j}-T)^{3/2}$ 규모로 매끄럽게 줄고($T_{c,j}=\Omega_j/2R$), 평탄역이 풀려 그만큼 `sec:broadening` 의 broadening 폭이 더 큰 몫을 차지한다(peak smear·$U_j$ 미세 shift).

**(d) 박스 — 초기값·피팅 규약.**
$$
\boxed{\;\Omega_j^{\text{pure}}\ (\text{tab:lco-staging 초기값})\ \xrightarrow{\ \text{도핑}\ }\ \Omega_j^{\text{doped}}=\Omega_j^{\text{pure}}-\delta\Omega\ \ (\to 2RT^+ \Rightarrow \Delta U_j^\hys\to0)\;}
$$
흑연 `GRAPHITE_STAGING_LIT` 의 $\Omega_j$ 가 초기값이고 폭이 피팅 대상이었듯, pure-LCO 의 $\Omega_j$ 가 초기값이고 도핑에 따른 폭·shift($\delta\Omega$)는 우리 데이터로 피팅한다(원 L703–707 을 문턱 극한 대입으로 수식화).

**원 줄글 대비(B 전체).** L685–708의 order-disorder·MIT·도핑 "같은 정규용액 틀 그대로 적용" 서술 3회를, 각각 흑연 eq:gxi→eq:gpp→eq:spinodal→eq:dUhys 사슬에 LCO Ω_j($\Omega_{\mathrm{od}}$·$\Omega_{\mathrm{MIT}}$·$\Omega_j^{\text{doped}}$)를 **실제 대입한 중간식**으로 대체 — spinodal 대입 중간식이 전무하던 것을 (a)→(d)로 채웠다. two-phase calibration(흑연 4 중 2 ↔ LCO 3 중 3)을 B-0 로 명시. 물리·부호·결과식 불변(흑연 결과식 재대입, 새 물리 없음).

---

# C. 논리 감사 결과 (물리 인과·부호·차원·극한·detailed balance)

> base 요구: 단순 기계적 변환이 아니라 각 유도의 논리 소당성을 감사. 아래는 진짜 논리 결함(비약이 아닌 오류)만 tier 로 분류.

## C-1  center — 무결(물리·부호·결과식 불변)

- **전극무관 논증(A-①)**: eq:eqbalance(L427)가 host 종을 $\mu^0$ 상수로만 흡수한다는 관찰은 정확하다 — 삽입 반응식의 host 는 전위 의존항($\tilde\mu_{e^-}=\mu_{e^-}^0-FV$)에 들어가지 않으므로 eq:eqcond·eq:Uj 가 host 불문으로 성립한다. **원 단정은 결함이 아니라 유도 다리 생략(비약)**이다 — 대입 식으로 회수하면 무결. 물리 결함 없음.
- **∂U/∂T 부호(A-②)**: $\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$ 는 (i) Gibbs 항등식+eq:eqcond, (ii) eq:Uj 직접 미분 두 경로가 같은 값에 닿아 흑연과 **부호까지 1:1**(AUTHOR_BRIEF L22 요구 충족). 대표 $\Delta S_\rxn\approx+80$ J/(mol·K)>0 → $\partial U/\partial T>0$(중심이 온도에 오름)은 검산 박스 L491–500 과 정합. **차원 검산**: $[\Delta S/F]=(\text{J·mol}^{-1}\text{K}^{-1})/(\text{C·mol}^{-1})=\text{J·C}^{-1}\text{K}^{-1}=\text{V/K}$ ✓.
- **전자항 공존**: 검산 박스 L501–508 이 이미 "전체 계수 $+80$ vs T1 전자항 음수(한 성분)는 모순 아님"을 잘 서술 — 손대지 않음(과수정 경계). **결함 없음.**

## C-2  hys — 무결 + ★혼동 가드 1건(오류 아님, 명시 권고)

- **two-phase 적용의 소당성**: order-disorder(초격자)·MIT(plateau) 는 실제 miscibility gap / 상분리이므로 정규용액 이중웰($\Omega_j>2RT$) 적용은 물리적으로 정당하다. LCO 세 전이 전부 two-phase 는 tex L686·L707·L1209·R1_broadening D7 과 정합 — **결함 없음**(물리 불변).
- **극한 검산**: 도핑 $\Omega_j\to2RT^+ \Rightarrow u_j\to0 \Rightarrow \Delta U_j^\hys\to\frac{8RT}{3F}u_j^3\to0$ 은 흑연 L621–623 의 연속 소멸과 동형 — 임계온도 $T_{c,j}=\Omega_j/2R$ 에서 매끄럽게 사라짐. **부호**: 극대>극소라 $\Delta U_j^\hys\ge0$, 방전 $\sigma_d=+1$ 이 중심을 $+$쪽(eq:Ubranch L639–640) — 흑연 부호 사슬 그대로. ✓
- **★[MED, 오류 아님 — 명시 권고] config ΔS vs 상호작용 Ω 혼동 여지**: 원 L689–694 는 order-disorder 문단에서 "정규용액 $\Omega>0$ 이 만드는 상분리"와 "charge-order 엔트로피 변화 0.47/1.49 J/K·mol"을 **연달아** 놓는다. 두 양은 물리적으로 다르다 — $\Omega_{\mathrm{od}}$(상호작용 에너지, 히스 gap 을 정함)와 config $\Delta S$(엔트로피, tab:lco-staging 의 중심 표준값). 원문은 "$\Delta S$ 의 출처"라고만 해 직접 등치는 하지 않았으므로 **논리 오류는 아니다**. 다만 수식화하며 "Motohashi $\Delta S$ → $\Omega_{\mathrm{od}}$" 다리를 잘못 놓으면 신규 오류가 생기므로, B-① (d) 의 ★가드 문장으로 **두 양의 분리를 명시**할 것을 권고한다. (이중계산 금지(B) 규칙 eq:lco-decomp L1704 와 같은 성격의 분리.)
- **차원 검산**: $[\Omega_j u_j/F]=(\text{J/mol})/(\text{C/mol})=\text{V}$, $[2RT\,\mathrm{artanh}\,u_j/F]=\text{V}$ → $\Delta U_j^\hys$ 단위 V ✓. artanh 인자 $u_j$ 는 무차원 ✓.

## C-3  물리 불변 확인 (종합)

- 결과식: 재작성안의 모든 박스가 **기존 tex 식의 재유도·재대입**이다 — eq:Uj·eq:lco-dUdT(A), eq:dUhys·eq:Ubranch(B). 새 결과식·새 물리·새 파라미터 없음(base 원칙 1·2 충족). ρ(U_app)/PSD·ρ_G 미도입 ✓.
- 부호: ∂U/∂T=ΔS/F 흑연 1:1(A-②), $\Delta U_j^\hys\ge0$·방전 $+$쪽(B) — 8/8 부호 사슬 불변.
- 미접촉 범위: `sec:lco-map`·`sec:lco-Se`·`sec:lco-gate`·N7–9·전자엔트로피 절·검산 박스(L490–509)·`sec:hys` 흑연 사슬(L515–682) 전부 미변경 ✓.

---

## 5줄 요약

1. **center 수식화**: 전극무관 단정(L471–476)을 eq:eqbalance→eq:eqcond 가 host 를 $\mu^0$ 상수로만 흡수한다는 대입 사슬로, ∂U_j/∂T 괄호 전보체(L477–482)를 Gibbs 항등식 다리+eq:Uj 직접미분 이중 경로로 (a)→(d) 완결 — 검산 박스 L490–509 는 보존.
2. **hys 수식화**: order-disorder·MIT·도핑 "같은 틀 적용" 3회를 각각 흑연 μ→g″→spinodal→ΔU_hys 사슬에 LCO $\Omega_{\mathrm{od}}$·$\Omega_{\mathrm{MIT}}$·$\Omega_j^{\text{doped}}$ 를 실제 대입한 중간식으로 재작성, 도핑은 $\Omega_j\to2RT^+ \Rightarrow \Delta U_j^\hys\to\frac{8RT}{3F}u_j^3\to0$ 문턱 극한으로.
3. **calibration 명시(★base 요구)**: 흑연 two-phase = 4 중 2(LiC₁₂·LiC₆), **LCO two-phase = 3 중 3(T1 MIT·T2·T3 order-disorder 전부 $\Omega_j>2RT$)** — solid-solution 전이 없음(B-0).
4. **논리 결함 발견 여부**: 진짜 오류(비약 아닌 오류) **없음** — center·hys 모두 물리·부호·결과식 불변. 단 hys order-disorder 에서 config $\Delta S$(Motohashi 0.47/1.49)와 상호작용 $\Omega_{\mathrm{od}}$ 혼동 여지 1건[MED, 오류 아님]을 B-① (d) 가드로 명시 권고.
5. **가장 약했던 원 줄글**: `sec:lco-hys`(L685–708) — order-disorder·MIT·도핑 세 문단이 spinodal 대입 중간식 **전무**한 채 "같은 틀 그대로 적용"으로만 닫혀 흑연 sec:hys 8-식 사슬 대비 밀도가 가장 낮았다(HIGH×3, center 의 HIGH×2 보다 결손 큼).
```
