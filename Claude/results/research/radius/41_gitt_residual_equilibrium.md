# 축 H — GITT 비-델타 잔여 폭의 평형 수준 기원

> 리튬이온전지 흑연 음극 dQ/dV(ICA) staging peak. 선행 조사: 실측 종모양의 상당부분이 유한 전류 과전압(η, kinetic). 반론: η는 전류 의존이라 GITT(근평형, I→0)에서 사라져야 하고, 그러면 peak이 델타(또는 내재 RT/F 폭)로 수렴해야 한다. 그런데 실측 GITT/OCP dQ/dV도 델타가 아니다 → 평형 수준 잔여 폭이 실재하는가?
>
> 작성자 sub(축 H 전담). web search 1차 문헌 검증. 종합·verdict·타 축은 master 전담.

---

## 소절 1 — GITT/준평형(quasi-OCV) 흑연 peak이 실제로 유한 폭인가, 그 폭은 얼마인가

**핵심 정량 결론**

1. **흑연 OCV plateau는 완벽히 평탄하지 않다.** 흑연의 준평형 OCP는 단일 평탄역이 아니라 staging에 대응하는 **다중 plateau**(상온 LixC6 기준 약 85 mV·120 mV·210 mV 부근 3 plateau)이며, plateau 사이 전이구간은 유한 기울기(non-zero dV/dx)를 갖는다. 약 120 mV plateau가 LiC18→LiC12, 약 85 mV plateau가 LiC12→LiC6(stage-2→stage-1)에 해당한다 (IOPscience JES 2.1251802jes, BioLogic GITT App Note, LiionDB arXiv:2110.09879).

2. **C-rate를 낮추면 peak이 좁아지나, 0으로 수렴하지 않는다.** C/100 측정에서 staging peak은 더 sharp 해지지만 **여전히 유한 폭**을 유지한다(Frontiers/arXiv:2303.07088 DVA). 즉 전류 의존 성분(η, kinetic)은 C-rate↓에서 줄지만, peak 폭이 0(델타)으로 가지 않고 **유한 잔여 폭에서 포화**한다 — 이것이 본 축의 핵심 관찰.

3. **잔여 평형 수준 폭의 규모**: stage-2→stage-1 전이 구간에서 lithiation/delithiation 사이 **잔여 hysteresis ≈ 10 mV** 가 T=57°C·저율에서도 잔존(Mercer 2021, JMCA, D0TA10403E). dV/dQ(DVA) plateau의 finite slope 및 dQ/dV peak의 finite width의 평형 수준 하한이 이 10 mV scale과 같은 차수.

**판정(소절1)**: GITT/준평형 흑연 dQ/dV·dV/dQ peak은 **확정적으로 유한 폭**이다. OCV plateau는 완벽 평탄이 아니라 전이구간에 non-zero dV/dx가 있고, 저율로 갈수록 peak이 좁아지나 ~10 mV scale 잔여 폭에서 포화한다.

---

## 소절 2 — 그 평형 잔여 폭의 확립된 원인

### (a) 내재 전이 폭 (이상적 흑연도 완벽한 델타가 아님)

- **유한 RT/F 폭**: 격자가스/평균장(regular-solution) 모형에서 단상 solid-solution 구간의 dQ/dV는 ~RT/F(상온 ≈ 25.7 mV) scale의 내재 폭을 가지며, 상호작용 파라미터 Ω(in-plane + interlayer)가 plateau의 비-평탄도를 결정한다. lattice-gas 모형은 in-plane·out-of-plane 상호작용으로 staging을 재현하며 OCV에 step-like + 임계농도 비해석적(non-analytic) feature를 만든다 (OSTI 20001074; ScienceDirect S0167273800005798 lattice-gas; ACS Omega 2020 first-principles staging).
- **단상 solid-solution 꼬리**: 흑연 lithiation 초기 dilute stage(1L solid-solution)는 두-상 plateau가 아니라 연속적 단상이며, 이 구간 dQ/dV는 본질적으로 broad(델타가 아님). plateau 양끝(전이 시작/끝)에서 단상→2상 경계의 solid-solution 꼬리가 peak에 유한 폭 기여.
- **★ 정적 무질서(static disorder)에 의한 pseudo-continuous 전이 (2025 신규)**: operando 광학현미경 + random-field Ising 모형. 흑연 단입자는 dilute stage에서 **avalanche-like** (de)intercalation(수 μm 영역이 수 초 내 전이)을 보이고, 이 avalanche는 흑연의 **static disorder**에 기인해 stage 간 전이를 **pseudo-continuous**(델타가 아닌 유한 폭)로 만든다 → 전기화학 프로파일·온도 의존성을 설명 (arXiv:2509.21047, 2025). 이것은 (a)와 (c)의 가교: 무질서가 내재적으로 전이를 broad하게 만든다.

### (b) ★ GITT가 *참* 평형이 아닐 가능성 — I→0에서도 잔존하는 hysteresis/metastable

이 소절이 본 축의 가장 강한 발견.

- **Dreyer 류 thermodynamic hysteresis (I→0 잔존)**: 다입자(many-particle) 저장계에서 단입자 chemical potential이 비단조(non-monotone)이면 particle-by-particle 충·방전이 일어나, **충·방전 전압 gap이 전류→0 극한에서도 사라지지 않는다**(thermodynamically stable hysteresis). "the hysteresis ... seems not to disappear as the current vanishes"; "apparent equilibria"가 다수 존재 (Dreyer et al. 2010, Nat. Mater. 9, 448–453, nmat2730; Dreyer et al. Continuum Mech. Thermodyn. 2010, 10.1007/s00161-010-0178-1). LiFePO4가 원형 사례이나 **상분리/staging 물질 일반에 적용** — 흑연 staging도 이 부류.
- **흑연 특이적 metastable carbon stacking hysteresis**: 흑연 delithiation 시 metastable AAAA stacking이 평형 AABB/AB로 즉시 가지 않고 x<0.5까지 retained. 잔류 interlayer Li가 stacking 에너지 지형을 바꿔 **시간 척도 수 시간~수 일에도 변화 없는 metastable 상태**가 존재 → 측정 OCV는 history-dependent이며 "must be considered a distinct quantity" from true equilibrium. **잔여 hysteresis ≈ 10 mV가 T=57°C에서도 잔존** (Mercer et al. 2021, JMCA 9, 492–504, D0TA10403E). 즉 GITT의 휴지구간(수 시간)으로도 이 metastability는 풀리지 않아, GITT OCP가 *참* 평형이 아닐 수 있다.

### (c) 진짜 평형 물질 이질성 (material heterogeneity)

- 실제 흑연 전극은 입자별 결정성·표면·결함·입자크기 분포가 있어, 입자마다 약간 다른 전이 전위를 가져 ensemble dQ/dV가 broaden. 단입자 avalanche가 입자 간 비동기적으로 일어나면(상기 arXiv:2509.21047 intraparticle 공간 이질성·시간 패턴) 전극 수준 평균이 추가로 broad. 단, 이것은 *전극 수준* 이질성이며 *단입자/단결정* 내재 폭(a)과는 분리해야 한다.

---

## 소절 3 — 분해: 잔여 폭 중 (내재 전이폭) vs (미평형/잔류 히스) vs (물질 이질성) 구분 연구

- **(a) vs (b) 분리**: Mercer 2021은 측정 OCV hysteresis를 **enthalpy/entropy 항(평형 열역학) + metastable stacking(미평형)** 으로 분해, ~10 mV 순(net) hysteresis가 enthalpy/entropy(평형 기원) 부분이고, 추가 hysteresis가 stacking metastability(미평형) 부분임을 구분 → **(a)와 (b)를 명시적으로 분리한 1차 사례**.
- **(a)·(c) 가교를 정량화한 연구**: arXiv:2509.21047(2025)은 random-field Ising로 **static disorder가 stage 전이를 pseudo-continuous로 broaden**시킴을 정량화 — 내재 전이폭(a)과 무질서/이질성(c)을 한 모형으로 연결. 단 단입자 내재 폭 vs 전극 ensemble 폭의 명시적 분해는 abstract 수준에서 단정 불가(tier 강등).
- **(b)와 GITT 평형성 직접 반증**: OCV 모형은 thermodynamically consistent 해야 한다는 비판(JPCL 3c03129, 2024)은 measured OCV를 평형으로 등치하면 안 됨을 뒷받침. → "GITT=참 평형" 전제 자체가 1차 문헌에서 의심받음.
- **명시적 3-way(내재 폭 / 미평형 / 이질성) 정량 분해를 단일 논문에서 다 한 사례는 본 조사 범위에서 미발견**(tier: 근거 미발견). Mercer(a/b 분리) + RFIM(a/c 연결)을 합쳐야 함.

---

## 카드 (schema: 주장 | 근거 | 지배식/정량값 | 흑연 적용성 | 타당/한계 | 판정 관련성 | 정독범위 | tier)

| # | 주장 | 근거(저자·연도·DOI) | 지배식/정량값(폭 mV·조건) | 흑연 적용성 | 타당/한계 | "GITT 비-델타=평형 이질성"인가 판정 관련성 | 정독범위 | tier |
|---|------|------|------|------|------|------|------|------|
| H1 | 흑연 준평형 OCP는 단일 평탄역이 아닌 다중 plateau(~85·120·210 mV)이며 전이구간에 non-zero dV/dx | IOPscience JES 10.1149/2.1251802jes; BioLogic GITT App Note 1; LiionDB arXiv:2110.09879 (2021) | 3 plateau; LiC18→12≈120 mV, LiC12→6(stage2→1)≈85 mV | 직접(LixC6) | 타당. plateau 정확값은 정의·온도 의존 | 평형 OCV가 완벽 평탄이 아님을 확정 → 잔여 폭 실재의 토대 | abstract+검색요약 | 확정 |
| H2 | C/100 등 저율에서 staging peak이 sharp해지나 유한 폭에서 포화(델타로 수렴 X) | Frontiers/arXiv:2303.07088 (DVA, 2023) | C/100서 low-SOC peak sharper, 여전히 유한 | 직접 | 타당. 정확한 포화 폭값은 abstract서 단정 X | η(전류 의존)는 줄지만 잔여 폭 남음 → 본 축 핵심 관찰 직접 지지 | abstract | 확정 |
| H3 | 흑연 lithiation/delithiation 잔여 hysteresis ≈10 mV가 T=57°C·저율서도 잔존; metastable AAAA stacking 기원; 측정 OCV는 참 평형과 distinct | Mercer, Peng, Soares, Hoster, Kramer 2021, JMCA 9, 492–504, 10.1039/D0TA10403E | net hysteresis ≈10 mV (0.25<x<0.5); metastable 상태 수 시간~수 일 무변화 | 직접 | 강함(full HTML 정독). 10 mV는 hysteresis(충방전 gap)지 단방향 peak 폭은 아님—구분 필요 | ★(b) GITT가 참 평형 아닐 수 있음 + 평형 기원(enthalpy/entropy)과 미평형 stacking을 분리 | full(HTML) | 확정 |
| H4 | 다입자 비단조 chemical potential → 충방전 전압 gap이 I→0서도 사라지지 않음(thermodynamic hysteresis) | Dreyer, Jamnik et al. 2010, Nat. Mater. 9, 448–453, 10.1038/nmat2730; Continuum Mech. Thermodyn. 10.1007/s00161-010-0178-1 | voltage gap ≠0 at vanishing current; "apparent equilibria" 다수 | 간접(LiFePO4 원형, 상분리/staging 일반) | 강한 이론. 흑연 직접 측정 아님 → 흑연 적용은 유추 | ★(b) "GITT(I→0)면 평형" 전제의 이론적 반증—gap이 평형 수준서 잔존 | abstract+검색요약 | 추정(흑연 직접성) |
| H5 | static disorder가 stage 전이를 pseudo-continuous로 broaden; 단입자 avalanche-like 전이 | arXiv:2509.21047 (2025, operando + RFIM) | avalanche μm/수초; disorder→pseudo-continuous 전이폭 | 직접(흑연 단입자) | 신규·강함. 동료심사 전(arXiv) → tier 강등 | (a)내재폭과 (c)무질서/이질성을 한 모형서 연결; 델타 아님의 구조적 기원 | abstract | 미검증(preprint) |
| H6 | regular-solution/lattice-gas: in-plane+interlayer 상호작용 Ω가 OCV 비-평탄도·내재 전이폭 결정; 단상구간 ~RT/F scale | OSTI 20001074; ScienceDirect S0167273800005798; ACS Omega 2020 (D0... staging) | dQ/dV 내재 폭 ~RT/F≈25.7 mV scale (상온, 단상) | 직접(이론) | 타당. 구체 Ω·mV는 모형·파라미터 의존 | (a)내재 전이폭—이상적 흑연도 델타 아님의 열역학 근거 | abstract+검색요약 | 추정(정량값) |
| H7 | OCV 모형은 thermodynamically consistent해야—measured OCV를 평형과 등치 금지 | JPCL 10.1021/acs.jpclett.3c03129 (2024) | (정성) | 직접(방법론) | 타당 | (b)지지: GITT OCP=참 평형 가정 자체 의심 | 검색요약 | 추정 |

---

## 이 축 요약 (master 인계용)

**규모**: GITT/준평형 흑연 staging peak은 **확정적으로 유한 폭**이다(델타 아님). OCV plateau는 완벽 평탄이 아니라 전이구간에 non-zero dV/dx가 있고, 저율(C/100)로 갈수록 peak이 좁아지나 0으로 수렴하지 않고 포화한다. 평형 수준 잔여 척도는 **~10 mV(stage-2→1 hysteresis)** 및 **단상구간 ~RT/F≈25.7 mV** 차수.

**지배 원인 — 셋 다 실재하나 비중·DOL 차이**:
- **(b) 미평형/잔류 hysteresis가 가장 강하게 입증됨**. ① Dreyer thermodynamic hysteresis: 다입자 비단조 μ로 충방전 gap이 **I→0서도 잔존**(Nat. Mater. 2010, 10.1038/nmat2730) — "GITT가 I→0이니 평형"이라는 전제를 이론적으로 직접 반증. ② 흑연 특이 metastable AAAA stacking: 수 시간~수 일 무변화, **≈10 mV가 57°C서도 잔존**(Mercer 2021, 10.1039/D0TA10403E, full 정독) — GITT 휴지로도 안 풀리는 미평형. **→ GITT 비-델타의 핵심 주범은 "GITT가 참 평형이 아님(b)"**.
- **(a) 내재 전이폭**: regular-solution/lattice-gas의 Ω·RT/F가 이상적 흑연도 델타 아니게 함(H6), static disorder가 pseudo-continuous 전이 유발(H5, 2025 preprint). 내재 폭은 실재하나 정량 분해는 abstract 수준.
- **(c) 물질 이질성**: 전극 ensemble broadening. 실재하나 단입자 내재폭(a)과 분리 필요. (b)·(c)는 입자 간 비동기 avalanche로 일부 연결.

**가장 강한 DOL(Degree of Literature)**:
1. **H3 Mercer 2021 (10.1039/D0TA10403E)** — full HTML 정독, 흑연 직접, ~10 mV 정량, 평형(enthalpy/entropy) vs 미평형(stacking) **명시적 분리**. 본 축 최강 근거.
2. **H4 Dreyer 2010 (10.1038/nmat2730)** — I→0 hysteresis 잔존의 이론적 권위(흑연 직접성은 유추라 tier 추정).

**'평형 이질성 실재' 판정**: 흑연 GITT 비-델타 peak의 잔여 폭은 **순수 평형 물질 이질성(c)만으로 설명되지 않는다**. 1차 문헌의 무게중심은 **(b) GITT/OCP가 참 열역학 평형이 아님**(I→0서도 잔존하는 thermodynamic + metastable-stacking hysteresis)에 있고, 여기에 **(a) 내재 전이폭**이 더해진다. 즉 "η가 GITT서 사라지면 델타로 수렴해야 한다"는 논증의 빈틈은 **GITT 자체가 델타를 줄 만큼의 참 평형이 아니라는 것** — η(전류 과전압)와는 다른, I→0에서도 남는 평형 수준 hysteresis/metastability + 내재 RT/F·Ω 폭이 잔여 폭을 만든다.

**열린 문제**:
- 단일 논문에서 **(내재 단입자 폭) vs (미평형 metastability) vs (전극 ensemble 이질성) 3-way 정량 분해**는 미발견(근거 미발견 tier). Mercer(a/b 분리)+RFIM(a/c 연결) 합성 필요.
- GITT 휴지시간을 충분히 늘리면(수 일) metastable stacking이 풀려 폭이 더 좁아지는지 — 즉 (b) 중 "느린 완화"와 "진정 thermodynamic gap"의 분리는 미검증.
- H5(2025)는 preprint(미검증) — 동료심사본 추적 필요.

**tier 분포**: 확정 3(H1·H2·H3) / 추정 3(H4 흑연직접성·H6 정량값·H7) / 미검증 1(H5 preprint) / 3-way 정량분해는 근거 미발견.
