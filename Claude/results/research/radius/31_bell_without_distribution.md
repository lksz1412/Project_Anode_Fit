# 축 E — 종모양 dQ/dV가 입자간 U_j 분포 *없이* 생기는 경로 검증

> 검증 대상 명제(사용자 믿음): "단일 입자 평형 dQ/dV는 델타여야 하는데 실측은 종모양 →
> 반드시 입자간 전이전위 U_j 분포 때문이다."
> 임무: **분포가 없어도 델타가 종모양이 되는 경로**가 1차 문헌에 있는지 검증해
> "종모양 = U_j 분포 필수"가 필연 결론인지 반박/한정한다.
> 작성: research sub (축 E). 종합·verdict는 master 전담. 본 카드는 축 E 한정.

---

## 소절 1 — 내재 평형 폭: 단일 입자 평형 dQ/dV는 *애초에* 델타가 아닐 수 있다

핵심 물리. 사용자의 "단일 입자 = 델타" 전제는 **전이가 강한 1차(strong first-order,
Ω≫2RT)일 때만** 성립한다. 평형 단일 입자의 dQ/dV는 등온선(occupancy x vs 전위 E)의
기울기 dx/dE이고, 이는 mean-field 정규용액(regular solution) = **Frumkin intercalation
isotherm**으로 기술된다. Frumkin 상호작용 파라미터 g(또는 Ω/RT)가:

- **g = 0 (Langmuir 극한, 상호작용 없음)**: dx/dE = logistic 미분 형태. peak 반치폭
  ~ 3.5·(nRT/F) ≈ 90 mV(n=1, 298K) 수준의 **본래 종모양**. 델타가 전혀 아니다.
- **0 < g < 4 (인력 있으나 임계 미만, Ω < 2RT)**: peak이 좁아지고 높아지지만 여전히
  **유한 폭 종모양**. 단일 상(solid solution) 안에서 연속 전이.
- **g ≥ 4 (Ω ≥ 2RT, 임계 초과)**: dx/dE가 발산 → 상분리(miscibility gap) →
  Maxwell plateau → 평형 dQ/dV가 **델타에 수렴**. 사용자가 가정한 그림은 *이 경우에만*.

따라서 "단일 입자 평형 = 델타"는 **모든 전이가 강한 1차라는 숨은 가정**에 의존한다.
연속(solid-solution) 전이거나 약한 1차이면 단일 입자조차 본래 폭 ~nRT/F의 종을 낸다.

### 흑연 staging: 어느 전이가 1차(델타 후보)이고 어느 게 본래 종인가

문헌 합의(아래 카드 1d/1e):
- **dilute 영역 → stage 4 (저 x, x≲0.04~0.08)**: **dilute solid solution**.
  매우 낮은 점유에서 OCV가 급강하하는 **연속(solid-solution)** 거동. plateau 아님 →
  단일 입자도 본래 **종모양**(분포 불필요). 사용자 명제가 가장 약해지는 구간.
- **stage 4L ↔ 3L 전이**: 문헌이 **plateau가 없다(연속/약한 전이)**고 명시
  (RSC D0TA12607A: "phase transformation ... characterized by a plateau ... except for
  4L–3L transition"). → 본래 종모양, 분포 불필요.
- **stage 2L → stage 2 (LiC12), stage 2 → stage 1 (LiC6)**: **two-phase plateau
  (강한 1차)**. dx/dE=0(plateau) → 평형 단일 입자 dQ/dV는 **델타에 가깝다**.
  여기서는 실측 종모양이 *내재 폭만으로는* 설명 안 됨 → 분포 또는 유한율속(소절2) 필요.

즉 흑연은 **전이별로 갈린다**: 저 x·4L-3L = 본래 종(분포 불필요), LiC12·LiC6 = 본래
델타(broadening 원인 별도 필요). "전 구간이 델타"라는 전제는 흑연 실제에 부분적으로만 맞다.

---

## 소절 2 — 단일 입자 유한율속 broadening/skew: 입자 하나라도 넓어진다

평형이 아니라 **유한 전류**면, 입자 *하나*만으로도 dQ/dV peak이 넓어지고 비대칭이 된다.
배경 forward 모델의 lag 꼬리 `(ξ_eq − ξ_lag)/L_V`가 바로 이 단일 입자 효과다.

- **고상확산 한계**: 표면 점유가 평형을 앞서가/뒤처져(surface crowding) 전이가 더 넓은
  전위 범위에 펼쳐짐 → peak broadening. C-rate↑일수록 심화(카드 2a).
- **비대칭(skew)**: overpotential + 확산 구배로 충·방전 feature가 비대칭·중첩 →
  꼬리 한쪽으로 늘어남(카드 2a, 2b).
- 이 모두는 **입자 개수와 무관**(단일 입자에서도 발생). 따라서 종모양 폭의 *일부*는
  분포 없이 율속만으로 설명 가능. 단, **평형 극한(C/100→0)에서는 이 항이 사라진다** →
  강한 1차 전이의 평형 델타를 유한 폭으로 만드는 데는 율속만으론 불충분(평형으로 가면
  다시 델타로 수렴). 즉 소절2는 **동역학적 broadening**이지 평형 종모양의 설명은 아님.

---

## 소절 3 — Dreyer 순차충전: 분포 *없이도* 거시 plateau/종이 나오는 결정적 경로

가장 강한 반증. **Dreyer et al. (Nature Mater. 2010)** 다입자 모델 + 후속
**Katrašnik·Gaberšček et al. (J. Electrochem. Soc. 2022/arXiv:2201.04940)**:

- 메커니즘의 본질은 **단일 입자 화학퍼텐셜의 비단조성(non-monotone μ(x) = 비볼록 자유에너지)**.
  입자들이 리튬을 교환하며 전체 자유에너지를 최소화 → **particle-by-particle(순차) 충전** →
  거시적으로 **plateau / apparent equilibrium** 출현.
- **결정적 포인트(분포 필수성 직접 반박)**: arXiv:2201.04940 THEORY 절 명시 —
  *"In the idealised case, the intraparticle phase separated state represents an ensemble
  of particles all of which are split uniformly into two phases ... if the DOD is 0.5.
  In a more realistic situation, where a distribution of particle properties ... is taken
  into account, one may **expect a distribution** ..."*
  → **이상화(분포 0) 케이스가 이미 거시 거동을 낸다**; 입자 물성 분포는 *현실 보정*이지
  메커니즘 발생의 *필요조건이 아니다*. 비단조 μ(x) 하나가 1차 원인.
- 또한 같은 논문: *"extremely small currents ... is not true for phase separating
  materials, which exhibit a hysteretic behaviour even at extremely small currents"* —
  비단조 μ의 퍼텐셜 장벽이 **전류→0에서도** 평형에서 벗어난 상태를 강제. 즉 거시 종/plateau·
  히스테리시스가 **율속(소절2)·분포(명제) 둘 다 없어도** 비단조 단일입자 열역학에서 발생.

단, **한정**: Dreyer 경로가 내는 거시 신호는 *plateau/델타형*(상분리 강조)이지, 그 자체가
"종모양 broadening"을 직접 만들진 않는다. 종모양 폭은 (a) 소절1의 내재 평형 폭(연속 전이),
(b) 소절2의 유한율속, (c) 명제의 입자간 U_j 분포 — 세 경로의 **합성**. Dreyer는 "분포가
plateau의 필요조건이 아님"을 증명함으로써 **명제의 '반드시'를 깨는** 역할이 핵심.

---

## 카드 (schema: 주장 | 근거 | 지배식/정량 | 흑연 적용성 | 타당/한계 | 명제와의 관계 | 정독범위 | tier)

**카드 1a — Frumkin/정규용액 등온선이 단일 입자 dx/dE 폭을 결정**
- 주장: 단일 입자 평형 dQ/dV(=dx/dE)는 상호작용 g<4면 본래 유한폭 종, g≥4(Ω≥2RT)면
  델타. "단일=델타"는 강한 1차에서만.
- 근거: Levi & Aurbach, *Electrochim. Acta* 45 (1999) 167–185.
  DOI 10.1016/S0013-4686(99)00202-9.
- 지배식/정량: Frumkin = 정규용액 mean-field; g=0 Langmuir 극한 peak FWHM ~3.5·nRT/F
  ≈90 mV(298K,n=1); 임계 g=4 ↔ Ω=2RT에서 dx/dE 발산(상분리 개시).
- 흑연 적용성: 흑연 음극이 논문 예시 host. 직접 적용.
- 타당/한계: 타당(표준 이론). mean-field 근사 한계(staging 장거리 질서 단순화).
- 명제와의 관계: **반박/한정** — 연속·약한 전이면 분포 없이 종모양. 명제의 "단일=델타"
  전제를 g<4 영역에서 무효화.
- 정독범위: abstract + 검색 추출(full 본문 미접근). tier 강등 반영.
- tier: 확정(이론은 교과서 표준; 정량 90 mV는 표준 유도값=확정, 논문 verbatim은 미검증).

**카드 1d — 흑연 dilute 영역은 solid solution(연속), plateau 아님**
- 주장: 저 x(dilute stage) 영역은 연속 solid solution → 단일 입자도 본래 종.
- 근거: McEldrew/관련 dilute-occupation 모델, *Electrochim. Acta* (2019)
  "Transitions of lithium occupation in graphite ... dilute lithium occupation limit",
  DOI 10.1016/j.electacta.2019.134791(검색 식별; full 미접근→tier 강등).
  보강: MIT in-situ optical (dspace 1721.1/110917) — dilute에서 OCV 급강하 후 plateau로.
- 지배식/정량: 매우 낮은 점유에서 dE/dx 급경사(연속), plateau는 x>~0.25부터.
- 흑연 적용성: 직접(흑연 전용 논문).
- 타당/한계: 타당. 정확한 경계 x값은 자료별 편차.
- 명제와의 관계: **반박** — 흑연 일부 구간은 본래 연속 → 분포 불필요 종모양.
- 정독범위: abstract/검색. tier 강등.
- tier: 근거미발견→추정(DOI 식별했으나 full 정독 못함; 연속성 자체는 다출처 일치=확정에 근접).

**카드 1e — 4L–3L 전이는 plateau 없음(연속/약한), 나머지 staging은 two-phase plateau**
- 주장: 4L↔3L = plateau 없음(종 후보); 2L→2(LiC12), 2→1(LiC6) = two-phase
  plateau(평형 델타 후보).
- 근거: RSC *J. Mater. Chem. A* (2021) potassium/lithium staging 비교,
  DOI 10.1039/D0TA12607A (verbatim: "characterized by a plateau ... except for 4L–3L
  transition"). 보강: IOPscience 모델 DOI 10.1149/2.1251802jes (LiC6↔LiC12 x=0.5
  "constant potential"=plateau).
- 지배식/정량: plateau 구간 dE/dx≈0(델타); 4L-3L·dilute는 dE/dx≠0(종).
- 흑연 적용성: 직접.
- 타당/한계: 타당. 2L·3 stage 존재 여부는 자료 간 이견(IOP 논문은 LiC18·LiC27 미관측).
- 명제와의 관계: **한정** — 흑연은 전이별로 갈림. 강한 1차 구간(LiC12·LiC6)에서는
  명제(분포 또는 율속 필요)가 살아있음.
- 정독범위: abstract + WebFetch 추출(IOP). tier 표기.
- tier: 확정(4L-3L plateau 부재·LiC6/12 plateau는 다출처 일치).

**카드 2a — 유한율속 단일 입자 broadening/skew (C-rate 의존)**
- 주장: 단일 입자 하나라도 고상확산 한계로 dQ/dV peak이 C-rate↑에 따라 넓어지고 비대칭.
- 근거: 단일 graphite 입자 연구 ScienceDirect S254243512030619X; broadening 일반론
  (LFP dQ/dV 분석 자료). 정량 DOI 단일 미특정 → tier 강등.
- 지배식/정량: peak FWHM ∝ f(C-rate, D_s); 평형(C→0)에서 broadening→0.
- 흑연 적용성: single graphite particle 직접.
- 타당/한계: 타당하나 **평형 극한에서 소멸** → 평형 델타 설명엔 부적합(동역학 전용).
- 명제와의 관계: **부분 반박** — 분포 없이도 폭 일부 설명. 단 평형 종모양은 설명 못함.
- 정독범위: abstract/검색. tier 강등.
- tier: 추정(broadening 현상 자체는 확정, 단일입자 정량 C-rate 곡선은 미검증).

**카드 3 — Dreyer 순차충전: 비단조 μ(x)가 분포 없이 거시 plateau/히스테리시스 (★최강)**
- 주장: 동일(분포 0) 다입자라도 비단조 화학퍼텐셜이면 순차충전 → 거시 plateau/apparent
  equilibrium. 분포는 메커니즘 필요조건 아님.
- 근거: ① **Dreyer, Jamnik, Guhlke, Huth, Moskon, Gaberšček, *Nat. Mater.* 9 (2010)
  448–453, DOI 10.1038/nmat2730** (PMID 20383130). ② Katrašnik, Moškon, Zelič, Mele,
  Ruiz-Zepeda, Gaberšček, arXiv:2201.04940 (→ J. Electrochem. Soc. 2022).
- 지배식/정량: F_TOT = Σ_l ∫ f_l(x_l)dV 최소화, q=(1/N)Σx_l 제약; 비단조 μ(x)=비볼록 f(x);
  "idealised case ... particles all split uniformly ... DOD 0.5"(분포 0 케이스가 이미 작동);
  "hysteretic behaviour even at extremely small currents"(율속 0에서도).
- 흑연 적용성: 모델은 LFP 중심이나 **모든 phase-separating host(비볼록 f)에 일반**;
  흑연 staging plateau에 동일 논리 적용 가능(흑연 LiC12·LiC6 강한 1차 구간).
- 타당/한계: 타당(seminal). 한계: 거시 신호가 plateau/델타형이지 "종모양 broadening"을
  직접 만들진 않음 → 종 폭은 소절1·2와 합성.
- 명제와의 관계: **직접 반박** — "분포가 plateau의 *반드시*"라는 필연성을 깸.
  (단 "종모양"을 직접 산출하진 않으므로 명제의 *형태*(델타→종) 설명은 소절1·2가 보완.)
- 정독범위: arXiv:2201.04940 **본문 6쪽 full 정독(PDF Read)** + Nat.Mater. abstract/서지.
  THEORY 절·Fig.2(비단조 μ, 비볼록 F) verbatim 확인.
- tier: **확정** (비단조 μ 메커니즘·분포 비필수성은 본문 직접 인용으로 확인).

---

## 이 축 요약

**"U_j 분포가 종모양의 필수 원인인가"에 대한 판정: 아니다(명제는 과도 일반화).**
종모양은 분포 없이도 최소 두 독립 경로로 발생한다 —
(1) **내재 평형 폭**: 전이가 강한 1차가 아니면(흑연의 dilute 영역·4L–3L 전이) 단일 입자
평형 dQ/dV가 *애초에* 폭 ~nRT/F의 종(Frumkin/정규용액 dx/dE);
(2) **유한율속 broadening/skew**: 단일 입자 하나라도 고상확산 한계로 peak이 넓어지고
비대칭(단, 평형 극한에서 소멸 → 동역학 전용);
(3) **Dreyer 순차충전(비단조 μ)**: 동일 입자(분포 0)라도 거시 plateau/히스테리시스를
내며, "분포가 필요조건"임을 직접 반박.

**흑연 전이별 1차/연속 판정:**
- dilute→stage4, **4L↔3L = 연속/약한(plateau 없음)** → 본래 종, 분포 불필요.
- **2L→stage2(LiC12), stage2→stage1(LiC6) = two-phase plateau(강한 1차)** →
  평형 단일 입자는 델타에 가까움 → 여기서 실측 종모양은 (분포) 또는 (유한율속) 또는
  (Dreyer 순차) 중 하나 이상이 필요. 명제는 *이 구간에 한해서만* 부분적으로 정당.

**가장 강한 DOI: 10.1038/nmat2730** (Dreyer et al., Nature Materials 2010) —
비단조 화학퍼텐셜 단독으로 분포 없이 거시 plateau/순차충전을 산출, "분포 필수" 명제를
직접 반박. 보강 full-text 근거 = arXiv:2201.04940(Katrašnik·Gaberšček, 본문 정독).
내재 평형 폭 anchor = 10.1016/S0013-4686(99)00202-9 (Frumkin, Levi & Aurbach).

**열린 문제:**
- 흑연 LiC12·LiC6 강한 1차 구간에서 실측 종모양 폭의 *정량 분해*(분포 vs 유한율속 vs
  Dreyer 순차 기여 비율)는 미해결 — 평형 OCV(C/100) 측정으로 율속 기여 제거 후 잔여 폭이
  분포인지 Dreyer형 apparent-equilibrium인지 분리 필요.
- 2L·stage3 존재/연속성 여부 자료 간 이견(IOP 10.1149/2.1251802jes는 LiC18/LiC27 미관측)
  → 어느 전이가 진짜 강한 1차인지 흑연 등급·온도 의존성 확인 필요.
- Dreyer 비단조 μ가 "종모양 폭"을 직접 산출하는지(단순 plateau가 아니라) — 순차충전
  ensemble의 dQ/dV가 분포 입력 없이 유한폭 종을 내는지는 본 축 자료로 미확정(추정).
