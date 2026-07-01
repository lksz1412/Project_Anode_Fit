# V1.0.11 Phase 1.1 — LCO 수식화 supplement 드래프트 (ID = O1, Opus)

> 대상 = `docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex` 의 두 절 — `sec:lco-center`(L470–513)·`sec:lco-hys`(L684–708).
> 목표 = 현재 줄글 결론("같은 틀 그대로 적용"·괄호 전보체)을 흑연 forward 절(`sec:pol` L351+·`sec:center` L405+·`sec:hys` L515+)과 같은 **(a)출발식→(b)적용연산→(c)중간식≥1→(d)박스** 사슬로 재작성.
> ★드래프트만 — tex/코드 수정 X(편입은 master). 물리·결과식·부호·수치 원칙 불변(전개 형식만 줄글→수식). 유도의 논리 소당성을 감사(물리 인과·부호·차원·극한·detailed balance)하고, 진짜 논리 결함이면 근거와 함께 지적·수정안 제시.
> 근거 = 흑연 forward 정답(`eq:Uj` L453·`eq:eqcond` L433·`eq:Ujmid` L448·`eq:mu` L532·`eq:gpp` L545·`eq:spinodal` L551·`eq:dUhys` L616·`eq:Ubranch` L635)·`V1010_LCO_STYLE_REPORT.md` §1·`AUTHOR_BRIEF.md`·`R1_broadening.md`(★two-phase calibration)·`tab:lco-staging`(L319–342).
> 작성 = 2026-07-02. 무통신 독립 작성. 허위 attribution 없음.

---

## 0. 전체 요지 (감사 결론 먼저)

두 절 모두 **물리·부호·결과는 옳다** — 흑연 forward 의 정답 식(`eq:Uj`·`eq:dUhys`·`eq:Ubranch`)이 LCO 에 그대로 적용된다는 결론 자체는 정확하다. 결함은 **논리 오류가 아니라 유도 밀도(G-derive) 위반**이다: 두 절이 "같은 틀 그대로 적용"·괄호 전보체로 닫혀, 흑연 forward 가 매 결과식마다 보여 준 (a)→(d) 사슬과 **중간식이 빠졌다**. 따라서 본 supplement 는 물리를 바꾸지 않고 **빠진 중간식을 채우는** 재작성이다.

단 두 곳에서 **논리 소당성 감사가 실제 보완을 요구**한다(오류는 아니고, 비약 제거 = 논증의 소당성 강화):

- **감사 A1 (center, 전극무관 논증)**: 현 L471–476 은 "유도에 전극 가정이 없다 → LCO 에도 성립"을 **단정**한다. 이 단정 자체는 참이나, *왜* 전극 가정이 없는지를 `eq:eqcond`→`eq:Uj` 유도 사슬에서 **어느 단계도 전극 종을 특정하지 않음**을 짚어 대입식으로 회수해야 비약이 제거된다. (★base §산출 ② 는 "`eq:n0map` 대입 식으로"라 지시했으나 — `eq:n0map`(L201)은 방향부호·전류 환산 매핑이라 전극무관 **논증의 근거가 아니다**. 전극무관성의 실제 소스는 `eq:eqcond`의 삽입-반쪽반응 평형 조건이다. §2.2 D-CENTER-2 에서 근거와 함께 정정 제안한다.)
- **감사 A2 (hys, two-phase calibration)**: 현 L684–708 은 "세 전이 모두 상분리 대응"이라 쓰나(L687), `R1_broadening.md` calibration 은 **어느 전이가 정규용액 two-phase 인지**를 Ω 초기값 = 거친 추정으로 명시할 것을 요구한다. LCO 는 흑연(LiC₁₂·LiC₆ 두 전이만 two-phase)과 달리 **세 전이 전부 관측상 2상 공존역**이라 흑연과 대칭이 아니다 — 이 비대칭을 명시하지 않으면 흑연 절의 "two-phase = 2개" 메시지와 혼동된다(`R1` D7). §3.4 에서 처리.

가장 약했던 원 줄글 = **`sec:lco-hys` L684–708 전체** (3회 "같은 틀 적용" 서술, spinodal 대입 중간식 0, Ω_j 값(0.47/1.49)을 언급만 하고 `eq:spinodal`·`eq:dUhys` 에 넣은 식이 전무 — `V1010_LCO_STYLE_REPORT` HIGH×3).

---

## 1. 재작성 원칙 (흑연 forward 대조에서 도출)

흑연 forward 의 세 정답 절이 공유하는 골격을 LCO 재적용에 그대로 옮긴다:

| 흑연 forward 정답 | 사슬 패턴 | LCO 재적용에서 바뀌는 것 |
|---|---|---|
| `sec:center`(L442–461): `eq:Uj` 유도 | (a) $\Delta G_j=\Delta H-T\Delta S$ → (b) `eq:eqcond` 대입 → (c) `eq:Ujmid` 이항 → (d) `eq:Uj` 박스 | 입력 $(\Delta H,\Delta S)$ 의 **값**만. 식·부호 1:1 |
| `sec:hys`(L523–641): `eq:mu`→`eq:gpp`→`eq:spinodal`→`eq:dUhys`→`eq:Ubranch` | (a) 격자기체 $\mu$ → (b) $\xi$ 변환 → (c) $g''$ → (d) spinodal → gap → 분기중심 | $\Omega_j$ 의 **값**만(LCO 상전이가 정함). 사슬 형태 불변 |

★핵심 규율 = **점프 0**. 흑연 `eq:Uj` 유도가 $\partial U_j/\partial T=\Delta S/F$ 를 Gibbs 항등식 $\partial\Delta G/\partial T=-\Delta S$ 와 `eq:eqcond`의 $\Delta G=-FU$ 를 **잇는 한 문장**으로 못박았듯(L458–459), LCO center 도 같은 다리를 완결 문장으로 놓는다.

---

## 2. `sec:lco-center` 재작성 (삽입 위치 = L470–513 교체)

### 2.1 원 줄글 대비 — 무엇이 빠졌나

원문(L471–488)의 흐름:
- L471–476: "`eq:Uj` 는 전극 가정이 없다 → LCO 에도 성립. 바뀌는 건 입력 값뿐" — **단정**(중간식 0).
- L477–482: `eq:lco-dUdT`($\partial U_j/\partial T=\Delta S^\mathrm{cat}_{\rxn,j}/F$)를 "식~`eq:Uj` 의 $T$ 미분"이라 **괄호 전보체**로 제시 — Gibbs 항등식 다리 문장 없음.

빠진 것 = (i) 전극무관성을 `eq:eqcond`→`eq:Uj` 각 단계가 전극 종을 특정하지 않음을 **대입으로** 보인 식, (ii) `eq:lco-dUdT` 를 `eq:Uj` 에서 **미분으로 유도**한 (a)→(d) 사슬. 흑연 `sec:center`(L442–461)은 둘 다 갖췄으므로, LCO 절이 흑연 forward 밀도에 못 미친다(`V1010_LCO_STYLE_REPORT` HIGH×2).

### 2.2 논리 감사

- **D-CENTER-1 (무결)**: $\partial U_j/\partial T=\Delta S^\mathrm{cat}_{\rxn,j}/F$ 는 `eq:Uj` 의 정직한 $T$ 미분이며 부호·차원 정합($\Delta S$ [J mol⁻¹ K⁻¹] / F [C mol⁻¹] = [V K⁻¹]). 흑연과 1:1. **논리 결함 없음** — 유도 밀도만 보완.
- **D-CENTER-2 (비약 제거, base §산출 ② 정정 포함)**: 전극무관 논증의 근거는 **`eq:eqcond`**(L433, 삽입 반쪽반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}$ 의 평형 조건)이지 `eq:n0map`(방향부호 매핑)이 아니다. `eq:eqcond`→`eq:Ujmid`→`eq:Uj` 세 단계 중 **어느 것도 "흑연"·"음극"을 입력으로 쓰지 않고** 오직 반쪽반응의 $(\Delta H_\rxn,\Delta S_\rxn)$ 와 $s$ 만 쓴다 — 이것이 전극무관성의 **식 차원 근거**다. base 지시의 `eq:n0map` 은 mismatch 로 판단하여 `eq:eqcond` 로 대체(근거: `eq:n0map`(L197–201)은 $\sigma_d$·$|I|$ 환산일 뿐 $U_j$ 유도에 등장하지 않음; 전극무관성은 평형 조건 `eq:eqcond` 에서만 나온다). ★이는 물리 변경이 아니라 **올바른 앵커 식으로의 교정**이다.

### 2.3 재작성 수식 사슬

> **① $\partial U_j/\partial T$ 양극 — `eq:Uj` 미분 다리 (a→d)**

**(a) 출발 — 전극무관 평형 중심.** 평형 중심 `eq:Uj`
$$U_j(T)=\frac{-\Delta H_{\rxn,j}+T\,\Delta S_{\rxn,j}}{F}$$
는 삽입 반쪽반응의 평형 조건 `eq:eqcond`($\Delta G_j=-sFU_j$)와 반응 자유에너지 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 두 입력만으로 닫힌다. 이 두 입력 어디에도 "흑연"·"음극"이라는 전극 종은 들어가지 않는다 — 반쪽반응의 $(\Delta H_{\rxn,j},\Delta S_{\rxn,j})$ 와 방전 규약 $s=+1$ 만이 식을 정한다.

**(b) 연산 — 전극무관성을 대입으로.** 따라서 LCO 양극에 적용할 때 바뀌는 것은 입력 값뿐이다. `eq:eqcond` 의 평형 조건을 양극 반쪽반응 $\mathrm{Li}^++e^-+[\,]_\mathrm{cat}\rightleftharpoons\mathrm{Li}_\mathrm{(LCO)}$ 에 그대로 써서 상첨자 cat 을 달면
$$\Delta G_j^\mathrm{cat}=\Delta H_{\rxn,j}^\mathrm{cat}-T\,\Delta S_{\rxn,j}^\mathrm{cat}\;\overset{\text{eq:eqcond}}{=}\;-sF\,U_j^\mathrm{cat},$$
곧 흑연에서 쓴 것과 **글자 그대로 같은 식에 상첨자만** 바뀐다(전극 종이 유도 단계에 없었다는 §2.2 D-CENTER-2 의 대입 확인).

**(c) 중간식 — $U_j^\mathrm{cat}$ 이항 후 $T$ 미분.** `eq:Ujmid` 처럼 이항하면 $U_j^\mathrm{cat}(T)=(-\Delta H_{\rxn,j}^\mathrm{cat}+T\Delta S_{\rxn,j}^\mathrm{cat})/F$ 이고, 이를 $T$ 로 미분하면 $\Delta H^\mathrm{cat}$ 은 $T$ 무관, $T\Delta S^\mathrm{cat}$ 의 $T$ 미분이 $\Delta S^\mathrm{cat}$ 이라
$$\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\partial}{\partial T}\!\left[\frac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\Delta S_{\rxn,j}^\mathrm{cat}}{F}\right]=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.$$
이 미분은 Gibbs 항등식 $\partial\Delta G/\partial T=-\Delta S$ 와 `eq:eqcond` 의 $\Delta G=-FU$ 를 잇는 것과 동치다 — 흑연 `sec:center`(L458–459)이 이미 놓은 다리이고, 전극을 바꿔도 그 다리는 그대로 선다.

**(d) 박스 — 양극 $\partial U/\partial T$.** (현 `eq:lco-dUdT` 그대로, 유도가 그 앞에 놓임)
$$\boxed{\;\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}\qquad(\text{eq:Uj 의 }T\text{ 미분, 전극 불문})\;}$$
관계식은 흑연과 동일한 형태이고, **값**만 전이별 $\Delta S_{\rxn,j}^\mathrm{cat}$(§`sec:lco-decomp` 의 config·vib·elec 합, `eq:lco-decomp`)이 정한다.

> **② 전극무관 논증을 대입식으로 (단정 비약 제거)**

원 L471–476 의 "유도에 전극 가정이 없다"는 단정을, **평형 조건 자체의 대입**으로 회수한다. `eq:eqcond` 의 삽입 평형은 임의의 삽입형 전극 $M$ 에 대해
$$\tilde\mu_{\mathrm{Li}^+}+\tilde\mu_{e^-}=\tilde\mu_{\mathrm{Li}(M)}\;\Longrightarrow\;\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U_j),$$
로 닫히는데, 이 유도(흑연 `sec:center` L422–437)에서 전극 $M$ 은 **좌변 $\tilde\mu_{\mathrm{Li}(M)}$ 의 기준 상태로만** 들어가 우변의 상수 덩이 $U_j$ 에 흡수된다. 곧 $M=$ 흑연이든 $M=$ LCO 든 **식의 형태와 부호 관계는 불변**이고, 바뀌는 것은 $U_j$ 안의 수치(그리고 그 온도 미분 $\Delta S_{\rxn,j}^\mathrm{cat}/F$)뿐이다. LCO 양극의 높은 중심($\sim$3.9–4.2 V)은 삽입 반응의 큰 음의 $\Delta H_\rxn^\mathrm{cat}$(분자 $-\Delta H_\rxn^\mathrm{cat}$ 가 크게 양)에서 오며 — 흑연 $\sim$0.1 V 와 **같은 식, 다른 입력**이라는 결론이 이제 단정이 아니라 대입으로 회수된다.

### 2.4 검산 verifybox — 존치 (재작성 X, 손대지 말 것)

원 L490–509 의 verifybox(대표 $\mathrm{d}\phi/\mathrm{d}T\approx+0.83$ mV/K → $\Delta S_\rxn^\mathrm{cat}\approx+80$ J/(mol K) 역대입 검산, 단전극 vs 전셀 혼동 경고, 전자항 부호 공존)는 **이미 수식-검산 형태**이고 `V1010_LCO_STYLE_REPORT` 가 손대지 말 절로 분류하지 않았으나 정상 밀도다 — 유지. 위 (a)→(d) 사슬은 그 verifybox **앞**(L488과 L490 사이)에 놓여, 검산이 유도된 관계식을 역대입하는 순서가 된다(orphan 0: 앞에서 `eq:lco-dUdT` 유도 → 뒤 verifybox 가 그 식에 역대입).

### 2.5 center 논리 감사 결과

**무결(물리·부호·수치 불변).** 결함 = 유도 밀도뿐. 보완 = (i) `eq:lco-dUdT` 를 `eq:Uj` 미분 (a)→(d) 사슬로, (ii) 전극무관 단정을 `eq:eqcond` 대입으로 회수. ★한 가지 **앵커 정정**: base 지시의 `eq:n0map` → `eq:eqcond`(근거 §2.2 D-CENTER-2). 물리 결과 완전 불변.

---

## 3. `sec:lco-hys` 재작성 (삽입 위치 = L684–708 교체)

### 3.1 원 줄글 대비 — 무엇이 빠졌나

원문(L684–708)은 흑연 `sec:hys`(L515–641)의 완전한 사슬 `eq:mu`→`eq:gpp`→`eq:spinodal`→`eq:dUhys`→`eq:Ubranch` 을 **한 번도 LCO 파라미터로 재전개하지 않고**, 세 문단(order-disorder·MIT·도핑)에서 각각 "같은 정규용액 틀 그대로 적용"이라고 **서술만** 한다:
- L689–694 (T2·T3 order-disorder): $\Omega>0$ 이 이중웰을 만든다고 말하나, `eq:gpp`·`eq:spinodal` 에 LCO $\Omega_j$ 를 넣은 중간식 0. Motohashi 값(0.47/1.49 J/K mol)은 **엔트로피** 값인데 $\Omega_j$(상호작용 에너지)와의 연결이 서술로만 암시됨.
- L696–701 (T1 MIT): "`eq:dUhys`·`eq:Ubranch` 를 그대로 받는다"고만 함. spinodal gap 을 MIT 조성폭에 대입한 식 0.
- L703–707 (도핑): "$\Omega_j$ 를 $2RT$ 쪽으로 낮춘다"고 서술하나, 그 낮춤이 `eq:dUhys` 의 gap 을 얼마나 줄이는지 극한식($\Omega_j\to2RT^+$) 미제시.

→ `V1010_LCO_STYLE_REPORT` HIGH×3. 가장 약한 절.

### 3.2 논리 감사

- **D-HYS-1 (무결)**: "격자기체·정규용액 틀은 '동등한 자리에 리튬이 차고 빈다'는 가정만 쓰므로 LCO 에도 적용"(L685)은 정확 — `eq:mu`~`eq:dUhys` 유도(흑연 L524–623)는 자리 등가성만 가정하고 전극 종을 특정하지 않는다. LCO order-disorder(리튬/빈자리 정렬)·MIT(2상 공존)는 모두 이 가정을 만족한다. **논리 결함 없음.**
- **D-HYS-2 (차원·부호 감사, 무결)**: $\Omega_j$ [J/mol] 는 상호작용 에너지, Motohashi 의 0.47/1.49 J/(mol K) 는 **엔트로피** — 둘은 다른 양이다. 원문은 후자를 "config 주도 $\Delta S$ 의 출처"(L693–694)로 옳게 쓰나, 독자가 "$\Omega_j=0.47$?"로 오독할 여지가 있다. **오류는 아니나** 재작성에서 $\Omega_j$(spinodal 문턱 $>2RT\approx4958$ J/mol@298K)와 charge-order $\Delta S^0_j$(중심 표준값)를 **명시 분리**한다(비약 제거).
- **D-HYS-3 (two-phase calibration, base §산출 ★ 요구)**: 흑연은 dilute·4L-3L = solid-solution($\Omega<2RT$), LiC₁₂·LiC₆ 두 전이만 two-phase($\Omega>2RT$)다(`R1_broadening.md`·`sec:width` L738–741). LCO 는 이와 **비대칭**: 세 전이(T1 MIT·T2·T3) **전부** 관측상 2상 공존역이다(L687·`tab:lco-staging` 성격 열). 이 비대칭을 명시하지 않으면 흑연 절의 "two-phase = 2개" 메시지와 충돌한다(`R1` D7 주의). ★따라서 재작성은 **"LCO 는 세 전이 전부 two-phase, 단 $\Omega_j$ 초기값은 거친 추정이고 도핑·피팅으로 갈린다"**를 명시(calibration 요건). **논리 결함 아님 — 명시 누락**이므로 보완.

### 3.3 재작성 수식 사슬 — 도입 문단 (L685–688 교체)

**LCO 상전이를 정규용액 $\Omega_j$ 로.** §`sec:hys` 의 사슬 `eq:mu`→`eq:gpp`→`eq:spinodal`→`eq:dUhys`→`eq:Ubranch` 은 "동등한 자리에 리튬이 차고 빈다"는 가정만 쓰므로(§3.2 D-HYS-1), 그 가정이 서는 LCO 양극에 **$\Omega_j$ 의 값만 갈아** 그대로 적용된다. LCO 에서 이 값을 정하는 것은 표 `tab:lco-staging` 의 세 상전이이며, 흑연(two-phase = LiC₁₂·LiC₆ 두 전이만)과 달리 **세 전이 전부** 관측상 2상 공존역이라($x{\approx}0.5$ order-disorder 한 쌍 + $x{\approx}0.75$–0.94 MIT), 셋 다 초기값에서 spinodal 문턱 $\Omega_j>2RT$($2RT\approx4958$ J/mol@298 K)를 넘는 쪽에 놓인다 — 단 이 $\Omega_j$ 는 신뢰값이 아니라 **거친 초기 추정**이고, 도핑·피팅으로 override 되어 전이별로 갈린다(pure-LCO $\Omega_j$ = 초기값, 도핑에 따른 폭·shift = 우리 데이터 피팅; 흑연 `GRAPHITE_STAGING_LIT` 철학 그대로).

> ★D-HYS-3 명시: 흑연은 **두 전이만** two-phase(dilute·4L-3L = solid-solution), LCO 는 **세 전이 전부** two-phase — 이 비대칭이 두 전극의 spinodal 계상 차이다. 흑연 `sec:width` 의 "two-phase = 2개" 메시지가 LCO 로 흐려지지 않게 문장 경계를 둔다(`R1` D7).

### 3.4 재작성 수식 사슬 — (T2·T3) order-disorder (L689–694 교체)

**(a) 출발 — order-disorder 를 $\Omega_j>0$ 으로.** $x\approx0.5$ 부근에서 $\mathrm{Li}_x\mathrm{CoO_2}$ 는 점유 리튬과 빈자리가 교대로 정렬하는 monoclinic 초격자(질서상)를 이룬다 — 동종 이웃 인력이 가운데를 위로 미는 정규용액 $\Omega_j>0$(흑연 `eq:gxi` 의 이중웰 씨앗)의 LCO 사례다. 이 정렬을 낳는 상호작용을 $\Omega_{T2},\Omega_{T3}$ 로 둔다.

**(b) 연산 — `eq:gpp` 의 곡률에 LCO $\Omega_j$ 대입.** 흑연 `eq:gpp`
$$g_j''(\xi)=\frac{RT}{\xi(1-\xi)}-2\Omega_j$$
에 $j\in\{T2,T3\}$ 를 넣으면, 두 order-disorder 전이 각각이 자기 $\Omega_j$ 로 이중웰 곡률을 갖는다. 상분리(따라서 좁은 2상 peak)의 문턱은 $g_j''<0$ 구간이 생기는 조건 $\Omega_j>2RT$ 이다.

**(c) 중간식 — `eq:spinodal` 의 spinodal 을 LCO 전이에.** $g_j''=0$ 의 근으로(흑연 `eq:spinodal`)
$$\xi_{s,j}^\pm=\tfrac12(1\pm u_j),\qquad u_j=\sqrt{1-\frac{2RT}{\Omega_j}}\quad(j\in\{T2,T3\}),$$
곧 $\Omega_{T2},\Omega_{T3}>2RT$ 인 한 T2($\sim$4.05 V, hex$\to$monoclinic)·T3($\sim$4.17 V, monoclinic$\to$hex) 각각이 두 spinodal 끝점 사이 불안정 구간을 가져 **두 개의 좁은 peak** 로 갈라진다.

**(d) 박스 — order-disorder gap.** 흑연 `eq:dUhys` 를 두 전이에 그대로 써서
$$\boxed{\;\Delta U_j^\hys=\frac{2}{F}\Big[\Omega_j\,u_j-2RT\,\mathrm{artanh}\,u_j\Big],\quad u_j=\sqrt{1-\frac{2RT}{\Omega_j}}\quad(j\in\{T2,T3\})\;}$$
order-disorder 의 큰 $\Omega_j$ 가 $u_j$ 를 1 쪽으로 밀어 gap 을 키우므로, T2·T3 의 충방전 분기가 흑연 staging 보다 크다(`sec:lco-peak` L1211 서술과 정합).

**★$\Omega_j$ 와 $\Delta S^0_j$ 분리(D-HYS-2 비약 제거).** 정렬의 charge-order 엔트로피 변화 $\Delta S^0_j\approx0.47$ J/(mol K)@$x{=}\tfrac12$·$\approx1.49$ J/(mol K)@$x{=}\tfrac23$[tier A, Motohashi]는 표 `tab:lco-staging` 의 config **중심 표준값**($\Delta S^\mathrm{config}_j$, `eq:lco-decomp` 의 첫 슬롯)의 출처이지, spinodal 문턱을 정하는 상호작용 에너지 $\Omega_j$[J/mol]와는 **다른 양**이다 — 전자는 봉우리 중심 표준값(logistic 이 담음, `sec:lco-decomp` ★이중계산 금지 B), 후자는 이중웰 곡률(`eq:gpp`)을 정하는 문턱 파라미터다. 둘은 같은 order-disorder 물리의 서로 다른 계상이다.

### 3.5 재작성 수식 사슬 — (T1) MIT 2상역 (L696–701 교체)

**(a) 출발 — MIT plateau 를 $\Omega_{T1}>2RT$ 로.** $x\approx0.75$–0.94 의 절연체$\to$금속 천이(MIT)도 2상 공존역이다(전위 plateau $\sim$3.9 V). 격자기체 config 자유도만 보면 이 plateau 역시 정규용액 상분리이므로 $\Omega_{T1}>2RT$ 로 둔다.

**(b) 연산 — `eq:spinodal`·`eq:dUhys` 를 T1 에 대입.** 흑연 사슬을 $j=T1$ 에 그대로 써서
$$u_{T1}=\sqrt{1-\frac{2RT}{\Omega_{T1}}},\qquad \Delta U_{T1}^\hys=\frac{2}{F}\Big[\Omega_{T1}u_{T1}-2RT\,\mathrm{artanh}\,u_{T1}\Big],$$
곧 MIT plateau 의 spinodal gap 이 흑연 two-phase 전이(LiC₁₂·LiC₆)와 **같은 닫힌식**으로 적힌다.

**(c) 중간식 — 분기 중심 `eq:Ubranch` 에.** 방향별 분기 중심(흑연 `eq:Ubranch`)
$$U_{T1}^{\,d}=U_{T1}+\tfrac12\,\sigma_d\,h_{\eta,T1}\,\gamma_{T1}\,\Delta U_{T1}^\hys$$
로 MIT plateau 의 충방전 히스가 $\Delta U_{T1}^\hys$·$\gamma_{T1}$ 로 적힌다 — 곧 LCO MIT 도 흑연과 같은 분기 식을 받는다.

**(d) 박스 — config 와 전자 자유도의 분리(이중계산 방지 출발).** MIT 에는 격자기체 config 만으로 닫히지 않는 **전자 자유도**(전도 전자 상태밀도 변화)가 있어, 엔트로피에 흑연엔 없는 항이 하나 더 붙는다(`sec:lco-electronic` 의 $\Delta S_{e,j}$, `eq:dSe`·`eq:dSemolar`). 재작성은 이를 **두 몫으로 분리**해 못박는다:
$$\boxed{\;\text{MIT 의 구조적 2상역}\to\text{정규용액 }\Omega_{T1}\text{(위 (a)–(c))},\qquad\text{전자 자유도}\to\Delta S_{e,T1}\text{(별도 항, }\propto T\text{)}\;}$$
config 슬롯(`eq:lco-decomp`)에는 봉우리 중심 표준값만, elec 슬롯에는 MIT 게이트 골만 들어가 각 항이 자기 자유도의 몫만 채운다 — 같은 엔트로피를 두 번 세지 않는다(`sec:lco-decomp` ★가법성·무이중계산). 여기서는 그 분리의 출발점만 못박고, 전자항 유도는 `sec:lco-electronic` 이 잇는다(orphan 0: 뒤 절이 이 분리를 받아 전개).

### 3.6 재작성 수식 사슬 — 도핑 보정 (L703–707 교체)

**(a) 출발 — 비-redox 치환의 상전이 억제.** Al³⁺/Mg²⁺ 비-redox 치환은 Co redox 와 전자항을 보존하되 order-disorder·MIT 상전이를 **억제**한다. 정규용액 틀에서 이는 상호작용 $\Omega_j$ 를 낮추는 것으로 들어온다.

**(b) 연산 — $\Omega_j\downarrow$ 가 gap 에 미치는 효과.** `eq:dUhys` 의 gap 은 $u_j=\sqrt{1-2RT/\Omega_j}$ 를 통해 $\Omega_j$ 에 단조 증가한다. 도핑이 $\Omega_j$ 를 문턱 $2RT$ 쪽으로 낮추면 $u_j\to0$ 이라, 극한식(흑연 `eq:dUhys` 아래 Taylor)
$$\Delta U_j^\hys\;\xrightarrow{\;\Omega_j\to 2RT^+\;}\;\frac{8RT}{3F}\,u_j^3\to0\qquad(u_j^3\propto(T_{c,j}-T)^{3/2},\ T_{c,j}=\Omega_j/2R)$$
로 spinodal gap·히스가 매끄럽게 줄고 평탄역이 풀린다.

**(c) 중간식 — 풀린 몫이 broadening 으로.** $\Omega_j$ 가 $2RT$ 로 가까워질수록 상분리가 약해지므로 `eq:dUhys` 의 gap 이 담던 날카로움이 `sec:broadening` 의 broadening 폭으로 넘어간다(폭 $w_j$ 의 이중지위: two-phase 에선 현상학적 피팅 폭, `sec:width` L732–733). 곧 도핑은 두 방향으로 들어온다 — (i) peak 를 smear(폭↑), (ii) $U_j$ 를 미세 shift.

**(d) 박스 — 도핑 = 초기값에서 피팅으로.** 흑연 `GRAPHITE_STAGING_LIT` 가 초기값이고 폭이 피팅 대상이었듯,
$$\boxed{\;\text{pure-LCO }\Omega_j\ (\text{초기값},\ >2RT)\ \xrightarrow{\ \text{도핑}\ }\ \Omega_j\downarrow\ (\to 2RT\text{ 쪽})\ \Rightarrow\ \Delta U_j^\hys\downarrow,\ w_j\uparrow,\ U_j\ \text{shift}\;(\text{우리 데이터 피팅})\;}$$

### 3.7 hys 논리 감사 결과

**무결(물리·부호·수치 불변).** 세 결함은 전부 **유도 밀도(G-derive) 미달**이지 논리 오류가 아니다. 보완 = (i) order-disorder·MIT·도핑 세 문단을 각각 `eq:gpp`→`eq:spinodal`→`eq:dUhys`(→`eq:Ubranch`) 대입 사슬로, (ii) two-phase calibration 명시(D-HYS-3: LCO 세 전이 전부 two-phase, $\Omega_j$ 거친 초기값·피팅으로 갈림 — `R1` 요건), (iii) $\Omega_j$(문턱) vs $\Delta S^0_j$(중심 표준값) 분리(D-HYS-2 비약 제거). 물리·결과식·부호 완전 불변.

---

## 4. 삽입 위치 요약 (master 편입용)

| 절 | 삽입/교체 줄 | 재작성 내용 | 원 줄글 대비 | 감사 |
|---|---|---|---|---|
| `sec:lco-center` | L471–488 교체(verifybox L490–509 존치) | ① `eq:lco-dUdT` = `eq:Uj` $T$-미분 (a)→(d) 사슬 + ② 전극무관 논증을 `eq:eqcond` 대입식으로 | 단정 비약(L471–476)·괄호 전보체(L477–482) → 중간식 채움 | 무결. ★앵커 정정 `eq:n0map`→`eq:eqcond`(D-CENTER-2) |
| `sec:lco-hys` 도입 | L685–688 교체 | LCO 세 전이 $\Omega_j$ 로, two-phase calibration 명시 | "같은 틀 적용" 서술 → calibration 명시 | 무결(D-HYS-3 명시 보완) |
| `sec:lco-hys` T2·T3 | L689–694 교체 | `eq:gpp`→`eq:spinodal`→`eq:dUhys` 대입 (a)→(d) + $\Omega$/$\Delta S^0$ 분리 | spinodal 대입 중간식 0 → 채움 | 무결(D-HYS-2 비약 제거) |
| `sec:lco-hys` T1 MIT | L696–701 교체 | `eq:spinodal`·`eq:dUhys`·`eq:Ubranch` T1 대입 + config/전자 분리 박스 | "그대로 받는다" → 대입 사슬 | 무결 |
| `sec:lco-hys` 도핑 | L703–707 교체 | $\Omega_j\downarrow$→gap 극한($\Omega\to2RT^+$)→broadening | "낮춘다" 서술 → 극한식 | 무결 |

**손대지 말 것(확인)**: `sec:lco-map`(L295–349)·`sec:lco-Se`/`sec:lco-electronic`(L933+)·`sec:lco-gate`(L1068+)·N7-9·전자엔트로피 절·verifybox(L490–509). 신규 개념(ρ(U_app)·PSD convolution·ρ_G) 도입 0.

---

## 5. 5줄 요약

1. **center 수식화 핵심** — `eq:lco-dUdT`($\partial U_j^\mathrm{cat}/\partial T=\Delta S^\mathrm{cat}_{\rxn,j}/F$)를 `eq:Uj` 의 $T$-미분 (a)→(d) 사슬로 유도하고, 전극무관 논증을 `eq:eqcond`(삽입 평형 조건, 전극 종 미특정) 대입으로 회수해 L471–476 의 단정 비약을 제거.
2. **hys 수식화 핵심** — order-disorder(T2·T3)·MIT(T1)·도핑 세 문단을 각각 흑연 `eq:gpp`→`eq:spinodal`→`eq:dUhys`(→`eq:Ubranch`)에 LCO $\Omega_j$ 를 실제 대입한 (a)→(d) 중간식으로 재전개, 도핑은 $\Omega_j\to2RT^+$ 극한식으로.
3. **논리 결함 발견 여부** — 진짜 논리 오류 **0건**. 세 곳은 비약 제거(D-CENTER-2 `eq:n0map`→`eq:eqcond` 앵커 정정·D-HYS-2 $\Omega_j$ vs $\Delta S^0_j$ 분리·D-HYS-3 two-phase calibration 명시)로, 모두 유도 밀도·명시 누락이지 물리·부호 오류가 아님.
4. **물리 불변 확인** — 결과식(`eq:Uj`·`eq:dUhys`·`eq:Ubranch`)·부호(양극 U 높음·$\partial U/\partial T=\Delta S/F$ 흑연 1:1·$\Delta U^\hys\ge0$)·수치(Motohashi 0.47/1.49·$2RT\approx4958$ J/mol·$\Delta S^\mathrm{cat}\approx+80$)·차원 전부 불변. 전개 형식만 줄글→수식.
5. **가장 약했던 원 줄글** — `sec:lco-hys` L684–708(3회 "같은 정규용액 틀 그대로 적용" 서술, spinodal 대입 중간식 전무, Ω_j 값 언급만·`eq:spinodal`/`eq:dUhys` 대입 0 — `V1010_LCO_STYLE_REPORT` HIGH×3, center HIGH×2 보다 무거움).
