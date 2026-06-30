# 조사 카드 F — 입자 크기 의존 *동역학적(kinetic)* 분산이 dQ/dV 종모양을 만드는가

> 축 F (배정 1개 축). 작업 = web search(WebSearch/WebFetch) 1차 문헌 검증 + 본 카드 1개.
> 경계 준수: 본 축만. 종합·verdict·다른 카드 금지(master 전담). 모델/코드/메모리 수정 없음.
> 작성 sub. 허위 attribution 금지 — abstract-only/snippet-only 출처는 본문에 tier 강등·명시.
> 작성일 2026-06-30. 검색 기준 시점 = 질문 시점(2026-06).

---

## 0. 핵심 질문 (재진술 — 검증할 사용자 신가설)

흑연 음극 dQ/dV(ICA) staging peak이 실측에서 **치우친 종모양**으로 넓어진다. 입자 반경의 *열역학적*
전위 shift(Gibbs–Thomson)는 마이크론 흑연에서 ~0.01 mV로 무시 가능함이 선행 축에서 확인됨.
사용자는 이와 **별개의 동역학적(kinetic) 기작**을 제시한다 (축 F = 본 카드의 검증 대상):

> 고정 셀 전류가 크기 다른 입자들에 분배 → 국소 전류밀도·고상확산 timescale **τ ∝ r²/D** 가 입자마다
> 다름 → 작은 입자는 빨리 평형 도달(낮은 과전압), 큰 입자는 지연(높은 과전압) → 같은 인가 전위에서
> 입자들이 서로 다른 국소 SOC → 거시 전이가 전압 구간에 퍼짐 → dQ/dV broadening. 이는 **C-rate에
> 비례·저율서 소멸하는 동역학(apparent-U) 분산**이다.

본 축 임무 = 이 신가설을 (1) 다입자/SPM+PSD 모델, (2) operando 비균질 lithiation, (3) C-rate·PSD폭·D
정량 스케일 3 갈래로 1차 문헌 검증.

**카드 schema**: `주장 | 근거(저자·연도·DOI/URL) | 지배식/무차원수/정량값 | 흑연 적용성 | 타당/한계 |
사용자 신가설 지지/반박 | 정독범위 | tier`. DOI 필수. 추정 mV는 tier=추정+계산근거. abstract-only 명시.
tier ∈ {확정, 근거미발견, 추정, 미검증}.

> **정독범위 규약**: Wiley 본문(Röder 2016) = HTTP 402(paywall) → 검색 엔진 요약(snippet)만 → tier 강등.
> arXiv PDF(2006.12208) = 바이너리 디코드 실패 → **abstract 페이지(arxiv.org/abs) WebFetch 성공 → abstract
> verbatim 확보**. PMC(Nat. Commun. PMC10449918; GITT PMC8397968) = 본문 WebFetch 성공 → "본문요약".
> IOPscience(Farkhondeh JES) = abstract/snippet. 사용자 신가설 지지/반박 판정은 master 아닌 본 sub의 축내 1차 평가.

---

## 1. 다입자 모델(MPM)/SPM+PSD에서 입자 크기 분포가 *동역학적으로* 전압/dQ/dV를 퍼뜨리는가

### (a) ★ 핵심: bimodal PSD → double plateau (전적으로 bimodality 때문) — SIAM/Chapman 군

| 항목 | 내용 |
|---|---|
| **주장** | SPM 을 **입자 크기 분포(PSD)** 로 확장하면 unimodal PSD 의 **spread 가 cell dynamics(전압 곡선)에 영향**을 주고, **bimodal PSD 는 double-particle model(DPM)로 잘 근사되어 실측 double-plateau 를 재현 — 이 double feature 가 "전적으로 bimodality 때문(entirely due to bimodality)"**. narrow PSD 에 대해 asymptotic 으로 **SPM 보정항**을 유도. |
| **근거문헌** | Kirk, T. L., Evans, J., Please, C. P., Chapman, S. J. (2022), "Modeling Electrode Heterogeneity in Lithium-Ion Batteries: Unimodal and Bimodal Particle-Size Distributions", *SIAM J. Appl. Math.* 82(2). DOI **10.1137/20M1344305** (arXiv:2006.12208). |
| **지배식/정량값** | PSD 를 SPM 에 도입 → unimodal: spread 가 클수록 곡선 변형 + effective radius 선택 문제 / narrow PSD 에 대한 asymptotic **correction to SPM** / bimodal: **DPM 1쌍이 double-plateau 재현**. (검증 chemistry = LFP, abstract verbatim 확보. 무차원수 명시값은 abstract 미기재 → 본문 미정독.) |
| **흑연 적용성** | 모델은 chemistry-무관(임의 OCV 곡선). abstract 검증 예시는 **LFP** (강한 phase-separating). 흑연 staging 에 직접 적용한 figure 는 본 검색 미확보. |
| **타당/한계** | 타당 — "PSD 분포가 feature 를 퍼뜨리고/쪼갠다"의 **수학적 정식화 + 실측 재현**을 1급 학술지에 제시. 한계: ① abstract 만 정독(본문 402/디코드 실패) ② 검증이 LFP — 흑연 staging peak 의 mV 폭 정량은 본 출처 직접 미제공 ③ LFP double-plateau 는 평형 OCV 의 비단조성도 관여 가능(순수 kinetic 아님). |
| **신가설 지지/반박** | **지지(강·구조적)**. "입자 크기 분포가 전압 feature 를 퍼뜨리고 bimodal 이면 둘로 쪼갠다"는 사용자 신가설의 핵심 메커니즘을 직접 모델링·실측 재현. 단 이 출처만으로는 *kinetic vs thermo* 분리가 약함(아래 (b)·소절3에서 보강). |
| 정독범위 | arxiv.org/abs/2006.12208v2 **abstract verbatim** + 검색요약. 본문 미정독. |
| tier | **확정**(double-plateau←bimodality 명제·SPM보정 존재는 abstract 확정) / 흑연 kinetic 분리 = 추정 |

### (b) ★ 흑연 직접: PSD heterogeneity → 입자별 국소 전류밀도·과전압·반응속도 차이 — Röder 2016

| 항목 | 내용 |
|---|---|
| **주장** | 흑연 전극에 입자 크기 분포를 주면 **입자마다 국소 전류밀도가 달라지고, heterogeneity 가 uneven surface overpotential 과 reaction rate 를 유발**한다. 즉 같은 셀 전류에서 크기별로 충전 거동이 갈린다. |
| **근거문헌** | Röder, F., Sonntag, S., Schröder, D., Krewer, U. (2016), "Simulating the Impact of Particle Size Distribution on the Performance of Graphite Electrodes in Lithium-Ion Batteries", *Energy Technology* 4(12), 1588–1597. DOI **10.1002/ente.201600232**. |
| **지배식/정량값** | "mathematical electrode model with distributed particle size … identifies **different local current densities** and charging behavior of particles … heterogeneity provokes **uneven surface overpotentials and reaction rates**." (정량 mV·C-rate 표 = Wiley 본문 402 → snippet only, 수치 미확보.) |
| **흑연 적용성** | **직접**(graphite 전극 전용 모델 연구). |
| **타당/한계** | 타당 — 사용자 신가설의 "크기→국소전류→과전압 분산" 사슬을 흑연에서 명시적으로 모델링. 한계: 본문 paywall, peak 폭의 mV 정량·C-rate 의존 곡선 직접 미정독(snippet). |
| **신가설 지지/반박** | **지지(직접)**. 흑연에서 PSD→국소전류밀도·과전압 분산을 1차 문헌이 확인 = 신가설의 동역학 사슬 1단계 입증. |
| 정독범위 | Wiley 본문 402 → 검색요약(snippet). abstract 수준. |
| tier | **확정**(현상·방향) / mV 정량 = 근거미발견 |

### (c) 보강: many-particle 모델 — 저율 unit-by-unit, 고율 parallel(분산) — Farkhondeh 군

| 항목 | 내용 |
|---|---|
| **주장** | non-monotonic 평형전위 + **resistance distribution** 을 가진 다수 mesoscopic unit 으로 전극 구성 시, lithiation 이 **저 C-rate 에선 unit-by-unit 순차, 고 C-rate 에선 mixed sequential-parallel** 로 진행 — 즉 분산(broadening)이 **C-rate 와 함께 켜진다**. |
| **근거문헌** | Farkhondeh, M., Pritzker, M., Fowler, M., Delacourt, C. (2017), "Mesoscopic Modeling of a LiFePO4 Electrode: Experimental Validation under Continuous and Intermittent Operating Conditions", *J. Electrochem. Soc.* 164(11), E3040–E3053. DOI **10.1149/2.0211706jes**. (관련: Farkhondeh et al. 2014, *PCCP* 16(41), 22555, DOI 10.1039/C4CP03530E.) |
| **지배식/정량값** | "lithiation proceeds **unit-by-unit … at low C-rates** but by a **mixed sequential-parallel order at high rates** … outcome of the interplay between the non-equilibrium single-phase lithiation … and the **non-uniform resistance distribution**." (resistance distribution 은 크기-상관 — 작은 입자 저저항·먼저 충전.) |
| **흑연 적용성** | 모델 검증 chemistry = LFP/graphite 셀. resistance/non-monotonic-U 단위 분산 프레임워크는 흑연 staging 에 이식 가능(직접 흑연 figure 는 LFP 중심). |
| **타당/한계** | 타당 — **C-rate 가 분산을 켜고 끈다**는 신가설 검증 신호를 모델로 직접 제시. 한계: LFP 중심, 흑연 dQ/dV mV 폭 직접 미제공, 본문 미정독(IOP snippet). |
| **신가설 지지/반박** | **지지(강)**. "저율=순차(좁음)·고율=병렬(분산)"은 사용자 신가설의 "**저율서 소멸**" 검증 신호와 정확히 일치. |
| 정독범위 | IOPscience abstract/검색요약(snippet). |
| tier | **추정→확정 경계**(저율순차/고율병렬 명제는 다출처 교차확인=확정, 흑연 정량=추정) |

---

## 2. operando 비균질 lithiation — 작은 입자 먼저, 큰 입자 지연 (흑연 직접·실험)

### (d) ★ operando microscopy + phase-field: τ ∝ r², ~7 µm 전환 직경, C-rate 의존

| 항목 | 내용 |
|---|---|
| **주장** | operando 광학 현미경 + 3D phase-field 로 흑연 입자 lithiation 을 직접 관찰 — **입자 크기가 intercalation mechanism 을 결정**하며 "**고상확산 시간상수가 반경의 제곱(τ ∝ r²)**". 작은 입자 = intercalation-wave(kinetic 지배·빠름), 큰 입자 = shrinking-core(수송 지배·지연·코어 미충전). 전환 직경 **~7 µm**. |
| **근거문헌** | Yang, Y. *et al.* (2023), "Multiscale dynamics of charging and plating in graphite electrodes coupling operando microscopy and phase-field modelling", *Nature Communications* 14, 5050. PMC10449918. DOI **10.1038/s41467-023-40574-6**. |
| **지배식/정량값** | "the time constant for solid-state diffusion **squares with the radius**" / "transition between intercalation wave … and shrinking core … observed to be **~7 µm**" / "When the lithiation current is **doubled (4 mA cm⁻²)**, it introduces a **marked intra-particle SOC heterogeneity**" / 저율 **0.05C** 에선 phase boundary 가 입자를 가로지르는 동일 intercalation-wave(균질) / C-rate: 0.05C, 1C, 2C, 3C / 입자 ~7–20 µm / 가소(plating) 핵생성 장벽 **20 mV**. |
| **흑연 적용성** | **직접**(graphite 음극 operando 실험). |
| **타당/한계** | 타당(★) — 사용자 신가설의 **모든 사슬 단계**(τ∝r² → 작은 입자 빠름·큰 입자 지연 → 국소 SOC 이질 → **C-rate 의존, 저율서 균질화**)를 흑연에서 직접 영상 확인. 한계: 본 논문 초점은 plating onset/intra-particle 이질 — *입자간* SOC 분산을 **dQ/dV peak 폭(mV)** 으로 환산한 정량은 본문에 직접 표로 없음(연결은 본 카드 추론). |
| **신가설 지지/반박** | **지지(최강·실험)**. τ∝r²·작은입자선충전·큰입자지연·C-rate켜짐·저율소멸을 흑연 operando 로 직접 입증. |
| 정독범위 | PMC10449918 **본문요약**(WebFetch 성공, verbatim 인용 확보). |
| tier | **확정**(τ∝r²·~7µm·C-rate 의존·저율균질은 본문 확정) / dQ/dV mV 폭 환산 = 추정 |

### (e) 보강: 저율=sharp peak / 고율=broadening (quasi-equilibrium 상실) — ICA 일반

| 항목 | 내용 |
|---|---|
| **주장** | 저 방전율에선 well-defined·sharp dQ/dV peak(2상 평형 반영), 율 ↑ 이면 **peak broadening** — 전이가 더 넓은 전압 구간에 걸쳐 발생(고전류서 평형 상실·확산 제약). SPM 은 **<1C 정도 저율에서만** 신뢰. |
| **근거문헌** | (현상 일반·다출처 교차) 예: Generalised SPM 유도 — Marquis, S. G. *et al.* / Brosa Planella *et al.* 계열, arXiv:1907.09410 ("Generalised single particle models for high-rate operation … systematic derivation and validation"); ICA 율의존 일반론(검색요약). |
| **지배식/정량값** | 저율 sharp ↔ 고율 broaden(전압 구간 확대). "basic SPM reliably reproduces … provided rates are relatively low (**less than 1C**)". (출처별 DOI: arXiv:1907.09410.) |
| **흑연 적용성** | 흑연 포함 일반(2상/phase-separating 전극 ICA). |
| **타당/한계** | 타당 — 신가설의 "**저율서 소멸**" 핵심 검증 신호를 ICA 현상론으로 뒷받침. 한계: 이 broadening 의 일부는 *입자내* 확산·전극 수송 등 PSD 무관 kinetic 도 포함(PSD 분산만의 기여 분리는 별도). |
| **신가설 지지/반박** | **지지(검증신호)**. C-rate↑→broaden, C-rate↓→sharpen 은 신가설이 예측하는 동역학 분산의 서명과 일치. 단 PSD-기인 vs 일반 kinetic 의 분리는 추가 필요. |
| 정독범위 | arXiv 검색요약 + ICA 율의존 검색요약(snippet). |
| tier | **확정**(저율sharp/고율broaden 현상) / PSD-only 기여 분리 = 근거미발견 |

---

## 3. 정량·C-rate 스케일 — τ ∝ r²/D, D, 무차원수, apparent-U 분산 mV 추정

### (f) 흑연 Li 고상확산계수 D (GITT)

| 항목 | 내용 |
|---|---|
| **주장** | 흑연 내 Li 화학확산계수 D 는 lithiation 상태(x in Li_xC₆)에 따라 **~10⁻¹¹ ~ 4×10⁻¹⁰ cm²/s** 범위, staging plateau 부근서 **~1–2×10⁻¹⁰ cm²/s**. |
| **근거문헌** | (GITT) PMC8397968, "Investigation of Lithium Ion Diffusion of Graphite Anode by the Galvanostatic Intermittent Titration Technique" (2021). 보강: Weng et al. 2023, *Nano-Micro Lett.* 15, 215, DOI 10.1007/s40820-023-01183-6 (D = 2.64~19.87×10⁻¹⁰ cm²/s, 축 D 카드 기확보). |
| **지배식/정량값** | x<0.16: ~10⁻¹¹ / 0.16–0.2: ~2×10⁻¹⁰ / 0.2–0.25: ~8×10⁻¹¹ / 0.25–0.5: ~2×10⁻¹⁰ / x≥0.5: ~10⁻¹⁰ cm²/s. 전체 1×10⁻¹¹ ~ 4×10⁻¹⁰ cm²/s. |
| **흑연 적용성** | **직접**. |
| **타당/한계** | 타당(τ 계산 입력 확보). 한계: GITT D 는 방법·전극 의존 산포 큼(문헌 10⁻¹³~10⁻¹⁰까지). |
| **신가설 지지/반박** | **지지(입력)**. 아래 τ 추정의 D 입력 제공. |
| 정독범위 | PMC8397968 본문요약(WebFetch 성공). |
| tier | **확정**(D 범위) |

### (g) ★ τ ∝ r²/D 추정 + apparent-U 분산 mV 규모 [tier=추정, 계산근거 명시]

| 항목 | 내용 |
|---|---|
| **주장(추정)** | 같은 인가 전류에서 입자별 확산 timescale **τ = r²/D** 가 크기 제곱으로 벌어져, PSD 폭(d10~d90)에 비례하는 국소 SOC 분산 → apparent-U 분산을 만든다. 마이크론 흑연에서 그 규모는 **수 mV ~ 수십 mV** 로 추정(C-rate 비례·저율 0). |
| **계산근거(본 sub 직접 산정)** | D = 1×10⁻¹⁰ cm²/s = 1×10⁻¹⁴ m²/s 가정. r=5 µm(직경10µm): τ = r²/D = (5×10⁻⁶)²/1×10⁻¹⁴ = 2.5×10⁻¹¹/1×10⁻¹⁴ ≈ **2500 s ≈ 42 min**. r=10 µm(직경20µm): τ = (10×10⁻⁶)²/1×10⁻¹⁴ = 1×10⁻¹⁰/1×10⁻¹⁴ ≈ **10⁴ s ≈ 2.8 h**. → 직경 2배 차이 입자 사이 **τ 4배 차이**. C/2(2 h 만방)에서 작은입자(τ≈42min)는 추종·큰입자(τ≈2.8h)는 확산 율속 → 둘은 같은 시각에 서로 다른 국소 SOC. 무차원 비교: 방전 timescale t_dis = 1/C-rate × 3600 s, **Damköhler/Biot 류 비 τ/t_dis = (r²/D)·C-rate** — 작은입자 ≪1(평형), 큰입자 ~O(1)(지연). dV/dQ slope(staging plateau 0.085~0.22 V 구간) × ΔSOC_dispersion 로 apparent-U mV 환산 → ΔSOC ~ 수 % 면 수~수십 mV. |
| **무차원수** | **τ/t_dis = (r²/D)·(C-rate/3600 s⁻¹)** (Damköhler/Biot 유사). C-rate→0 이면 모든 입자 τ/t_dis→0 → 분산→0(**저율 소멸, 신가설 핵심 예측**). PSD 폭(r_max²/r_min² = (d90/d10)²) 이 분산 배율. |
| **흑연 적용성** | 직접(흑연 D·µm 입경 사용). |
| **타당/한계** | 추정 — τ∝r²·C-rate 의존은 (d) operando 로 확정, **mV 환산은 본 sub 의 order-of-magnitude 계산**(특정 실측 mV 표 미발견). ΔSOC→mV 변환은 국소 dV/dQ 와 PSD 형상에 민감. |
| **신가설 지지/반박** | **지지(정량 골격)**. 무차원수 τ/t_dis=(r²/D)·C-rate 가 신가설의 "C-rate 비례·저율 소멸"을 닫힌 형태로 표현. 절대 mV 는 미검증. |
| 정독범위 | 본 sub 직접 산정(입력 D=축 F (f)·Weng; τ∝r²=(d) Nat.Commun.). |
| tier | **추정**(계산근거 명시) — 절대 mV 규모는 미검증 |

---

## 이 축 요약 (크기 의존 kinetic 분산이 종모양을 설명하는 정도·C-rate 스케일·정량·열린 문제)

**판정 — 사용자 신가설(축 F)은 1차 문헌으로 강하게 지지된다.** 열역학 Gibbs–Thomson 경로(선행 축, ~0.01 mV
무시 가능)와 달리, **동역학 경로는 마이크론 흑연에서 실재하고 규모가 충분하다**:

1. **메커니즘 사슬 전체가 흑연 operando 로 직접 확인됨** — Yang et al. 2023 Nat. Commun.(DOI
   10.1038/s41467-023-40574-6, **가장 강한 DOI**): "고상확산 시간상수가 반경의 제곱(τ∝r²)", 전환 직경 ~7 µm,
   작은 입자=intercalation-wave(빠름)·큰 입자=shrinking-core(지연·코어 미충전), 그리고 결정적으로 **0.05C 에선
   균질·전류 2배에선 marked SOC heterogeneity** = 신가설의 "**C-rate 비례·저율 소멸**" 검증 신호와 정확 일치.

2. **PSD→feature 분산/분할의 수학적 정식화 + 실측 재현** — Kirk·Evans·Please·Chapman 2022 SIAM(DOI
   10.1137/20M1344305): bimodal PSD 의 double-plateau 가 "**전적으로 bimodality 때문**", narrow PSD 의 SPM
   보정항 존재. 흑연 직접 정량은 Röder 2016(DOI 10.1002/ente.201600232): PSD→**국소 전류밀도·과전압·반응속도
   차이**. 저율순차/고율병렬은 Farkhondeh 2017(DOI 10.1149/2.0211706jes).

3. **C-rate 스케일·정량** — 지배 무차원수 **τ/t_dis = (r²/D)·C-rate** (Damköhler/Biot 류): C-rate→0 이면
   분산→0(저율 소멸), PSD 폭 (d90/d10)² 가 배율. D≈1×10⁻¹⁰ cm²/s(GITT, PMC8397968)로 10µm 입자 τ≈42 min,
   20µm 입자 τ≈2.8 h → **직경 2배=τ 4배**. apparent-U 분산 mV 규모는 **추정 수~수십 mV**(tier=추정,
   계산근거 본문 (g); 절대값 직접 실측 미발견).

**열린 문제**: (i) *입자간* SOC 분산을 dQ/dV **peak 폭(mV)** 으로 직접 환산한 흑연 실측 표는 미발견 — 절대
mV 는 추정에 머묾. (ii) bimodal double-plateau 직접 검증은 LFP(강 phase-separating); 흑연 staging 에서의
double-feature 직접 재현 figure 미확보. (iii) 이 kinetic 분산과 *순수 입자내* 확산 broadening(PSD 무관)의 분리
— **저율 측정(C/20 이하)이 식별 키**: 저율서도 남는 비대칭은 PSD-kinetic 이 아닌 평형/조성 기인(타 축 소관).

**가장 강한 DOI**: 10.1038/s41467-023-40574-6 (Yang et al. 2023, Nat. Commun. — τ∝r²·~7µm·C-rate 의존
operando 직접 입증). 보조: 10.1137/20M1344305 (PSD→double-plateau 정식화) · 10.1002/ente.201600232 (흑연 PSD 직접).

**정량 규모(추정)**: 무차원 τ/t_dis=(r²/D)·C-rate; 10↔20µm 입자 τ 4배 차; apparent-U 분산 **수~수십 mV(C-rate
비례, 저율 0)** — tier=추정, 절대 mV 실측 미확보.
