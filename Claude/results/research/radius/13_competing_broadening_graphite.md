# 조사 카드 D — dQ/dV peak 넓어짐·비대칭의 경쟁 기작 + 흑연 마이크론 정량

> 축 D (배정 1개 축). 작업 = web search(WebSearch/WebFetch) 1차 문헌 검증 + 본 카드 1개.
> 경계 준수: 본 축만. 종합·verdict·다른 카드 금지(master 전담). 모델/코드/메모리 수정 없음.
> 작성 sub. 허위 attribution 금지 — abstract-only/snippet-only 출처는 본문에 tier 강등·명시.
> 작성일 2026-06-30. 검색 기준 시점 = 질문 시점(2026-06).

---

## 0. 핵심 질문 (재진술)

흑연 음극 코인 하프셀 dQ/dV(ICA)에서 staging 전이 peak이 **치우친(비대칭) 종모양**으로 넓어진다.
사용자 가설 = 이 치우침/넓어짐의 주요 원인이 **입자 반경 분포**(반경에 따라 전이전위 `U_j`가 입자간 분포 → 평형 전위 이질성으로 환산).
본 축의 임무 = 같은 치우침을 만들 수 있는 **경쟁 기작**(kinetic·접촉저항·조성 이질성·온도·입경)을 1차 문헌으로 정량 조사해, 사용자 가설과 **분리 가능한 식별 신호**를 찾는다.

**조사 카드 schema**: `주장 | 근거문헌(저자·연도·DOI) | 식별신호/정량값(값·단위·조건) | 흑연 적용성 | 타당/한계 | 사용자 가설과의 관계(경쟁/보완) | 정독범위 | tier`
tier ∈ {확정, 근거미발견, 추정, 미검증}.

> **정독범위 표기 규약**: ScienceDirect 본문은 WebFetch 403(차단)되어 검색 엔진 요약(snippet)만 확보 → "snippet" 표기·tier 강등. PMC·arXiv·IOP·Frontiers·RSC는 본문/abstract 페이지 WebFetch 성공 → "abstract+요약" 또는 "본문요약" 표기. arXiv PDF 2건(2005.04983, 1211.0027)은 PDF 바이너리 디코드 실패 → abstract 페이지 또는 snippet 기반.

---

## 1. dQ/dV / DVA peak을 넓히거나 비대칭으로 치우치게 만드는 기작들 + 각 식별 신호

### (a) 동역학 / 유한 전류 분극 · diffusion limitation · overpotential ★가장 강한 경쟁 기작

| 항목 | 내용 |
|---|---|
| **주장** | 유한 전류에서 발생하는 분극(overpotential)·고상 확산 한계가 dQ/dV peak을 (i) 충/방전 방향으로 비대칭 이동(charge→고전압, discharge→저전압), (ii) peak 높이 감소·폭 증가시킨다. 전류↑이면 식별 가능 peak 수가 줄어든다. |
| **근거문헌** | Fly & Lin (정확 저자 미확정), "Rate dependency of incremental capacity analysis (dQ/dV) as a diagnostic tool for lithium-ion batteries", *J. Energy Storage* (2019), DOI 10.1016/j.est.2019.100812 (S2352152X19308175). **[snippet only]** |
| **식별신호/정량값** | C-rate↑ → peak less pronounced·고전압 shift·broadening. C/6 초과에서 식별 peak 수 급감(특히 노화셀: 200 cycle 후 1C charge에서 1개 vs C/24에서 5개). 의사평형(pseudo-equilibrium) 조건 = **C/20 이하**에서 정보 최대. |
| **흑연 적용성** | 직접(흑연 음극 포함 풀셀·하프셀 ICA 대상). |
| **타당/한계** | 타당 — C-rate 의존성이 명확한 식별 신호. 한계: 본 출처 본문 미정독(403), 저자·정확 수치 일부 snippet 의존. |
| **가설과의 관계** | **경쟁(강)**. 저율로 갈수록 peak이 좁아지고 대칭에 가까워지면 치우침의 상당부분이 kinetic(반경분포 아님)이라는 신호. |
| tier | **추정→확정 경계** (현상 자체는 다수 출처 교차확인되어 확정, snippet 의존 수치는 추정) |

보강 정량 (kinetic 분극의 mV 규모, 본문요약 확보):

| 항목 | 내용 |
|---|---|
| **주장** | 흑연에서 Li⁺ intercalation 속도를 한 자릿수(0.05C→0.5C) 올리면 셀 분극이 **약 70 mV** 증가. 고율에서 단일상 Stage II 대신 Stage I–IV 이질적 공존. |
| **근거문헌** | Weng, S. *et al.* (2023), "Kinetic Limits of Graphite Anode for Fast-Charging Lithium-Ion Batteries", *Nano-Micro Letters* 15, 215. DOI 10.1007/s40820-023-01183-6. PMC10516836. **[본문요약]** |
| **식별신호/정량값** | 0.05C→0.5C 분극 **+70 mV**. Li⁺ 화학확산계수 D = 2.64×10⁻¹⁰ ~ 19.87×10⁻¹⁰ cm²/s(lithiation 상태 의존). 10 µm 입자 표면→중심 확산 ~7.89 min(≈7.6C 상당). 박전극(<10 µm 입자) = 계면 Li⁺ 확산 율속, 후막 = 전극 수송 율속. |
| **흑연 적용성** | 직접. |
| **타당/한계** | 타당, 정량 명확. 한계: 70 mV는 전체 셀 분극(개별 staging peak 폭 기여 분해는 아님). |
| **가설과의 관계** | **경쟁(강)**. 70 mV 분극은 staging plateau 간격(0.085~0.22 V) 대비 무시 못 할 규모 → kinetic이 peak 위치·폭에 큰 기여. |
| tier | **확정** |

### (b) 입자간 접촉저항 / 전류 분포 이질성

| 항목 | 내용 |
|---|---|
| **주장** | 집전체–활물질 gap 편차로 인한 접촉저항 분포, 입자간 저항 분포가 유효 분극을 입자별로 다르게 만들어 feature를 넓힌다(DRT에서 별도 peak로 분리됨). |
| **근거문헌** | (DRT 일반) Illig/Schmidt 계열 및 리뷰들. 모델로 직접 검증: **Farkhondeh, M., Pritzker, M., Fowler, M., Delacourt, C. (2017)**, "Mesoscopic modeling of a LiFePO4 electrode: experimental validation…", *J. Electrochem. Soc.* 164(11), E3040–E3053; 및 Farkhondeh *et al.* (2014) *PCCP* 16(41), 22555. **[snippet only]** — mesoscopic 모델 = "non-monotonic 평형전위 + **resistance distribution**" 단위 다수로 전극 구성. |
| **식별신호/정량값** | DRT에서 접촉저항 = 고주파 semicircle(저항+용량 병렬). resistance distribution을 모델에 명시적으로 넣으면 GITT/연속 응답이 재현됨(Farkhondeh). 정량 mV 폭 기여는 본 검색에서 미확보. |
| **흑연 적용성** | Farkhondeh 모델은 LFP/graphite 셀 대상(graphite 측 직접 언급은 LFP 중심). DRT는 흑연 음극 광범위 적용. |
| **타당/한계** | 타당하나 흑연 dQ/dV 폭에 대한 **직접 정량 mV 기여 미발견**. resistance distribution이 broadening을 만든다는 것은 모델 구조상 성립. |
| **가설과의 관계** | **경쟁**. 단, 저항 분포는 **kinetic(전류 의존)** → 저율에서 사라져야 함. 반경 분포의 평형 이질성과 식별 가능(C-rate 의존성 차이). |
| tier | **추정** (모델 구조는 확정적이나 흑연 dQ/dV 정량 폭은 근거미발견) |

### (c) 조성 / SOC 이질성 · 전극 두께 방향 불균일

| 항목 | 내용 |
|---|---|
| **주장** | 후막·고율에서 집전체–분리막 방향 Li 조성 구배 발생 → 전극 내 여러 영역이 서로 다른 SOC·staging에 동시 존재 → feature 넓어짐. **평탄 OCV plateau 구간에서 이질성 최대.** |
| **근거문헌** | ① (모델) Maire/Touzin 계열, "Lithiation heterogeneities of graphite according to C-rate and mass-loading: A model study", *Electrochim. Acta* (2018) (S0013468618307229). **[snippet only]** ② (실험·모델) **Tardif, S. *et al.* (2020)**, "Contribution of X-ray experiments and modeling to the understanding of the heterogeneous lithiation of graphite electrodes", arXiv:2005.04983, DOI 10.48550/arXiv.2005.04983. **[abstract 페이지 요약; PDF 디코드 실패]** |
| **식별신호/정량값** | "평형전위 곡선이 두께 방향 intercalation 이질성을 강하게 지배하며, **평탄 평형전위 영역의 SOC에서 이질성 최대**"(Maire snippet). Tardif: 80 µm 전극에서 synchrotron XRD로 LiₓC₆ 상의 순차 형성·"homogeneous↔heterogeneous 분포 교대" 관찰; **LiC₆/LiC₁₂ 전이에서 (de)insertion kinetics 크게 감소**. 고stoichiometry에서는 예측보다 균질. 정량 mV는 미확보. |
| **흑연 적용성** | 직접(흑연 전극 전용 연구). |
| **타당/한계** | 타당. 한계: 후막·고율 조건에 강하게 의존 — **박전극·저율 코인셀에서는 기여 작아짐**. |
| **가설과의 관계** | **경쟁**. 두께 구배는 전극 설계·전류 의존 → 박전극 저율로 줄임으로써 반경 분포(입자 내재 성질)와 분리 가능. |
| tier | **추정** (현상 확정, 코인셀 정량 기여는 조건 의존·근거미발견) |

### (d) 온도 영향

| 항목 | 내용 |
|---|---|
| **주장** | 저온은 Li 고상 확산↓·분극↑ → staging 전이가 둔화·여러 stage 공존·peak 둔화/넓어짐. 고온은 peak이 더 선명·잘 분리됨. |
| **근거문헌** | ① Senyshyn 계열, "Low-temperature performance of Li-ion batteries: The behavior of lithiated graphite", *J. Power Sources* (2015) (S0378775315002311) **[snippet only]**. ② (개념) dQ/dV 실무 가이드(lipowergroup) **[비1차, tier 강등]**. |
| **식별신호/정량값** | 230–320 K: 250 K 이하 lithiated graphite 상 불안정, LiC₁₂→graphite 전이 급변. 저온 율속 한계 = 흑연 음극의 낮은 Li 확산. "고온에서 process 더 선명·peak 더 잘 분리." 정량 mV/폭 미확보. |
| **흑연 적용성** | 직접. |
| **타당/한계** | 타당(정성). 한계: 상온 고정 코인셀 실험에는 변수 아님 — 온도를 통제하면 제거되는 기작. |
| **가설과의 관계** | **경쟁(약, 통제 가능)**. 상온 고정 시 무관 → 반경 분포 분리에 직접 방해 안 됨. |
| tier | **추정** |

### (e) 입자 크기 분포 자체 (= 사용자 가설의 직접 대상)

| 항목 | 내용 |
|---|---|
| **주장** | 입경이 작아질수록 **overpotential 증가**(특히 최소 입경 전극). 큰 입자는 확산거리↑로 율속 불리. 분포가 넓으면(d90/d10↑) 입자별 응답 시간 상수 분산. |
| **근거문헌** | ① **Jeschull, F. *et al.* (2020)**, "Graphite Particle-Size Induced Morphological and Performance Changes…", *J. Electrochem. Soc.* 167(10), 100535, DOI 10.1149/1945-7111/ab9b9a **[본문요약]**. ② 입경·overpotential snippet (MDPI Materials 2023, 16, 6896; ResearchGate ultra-thin-layer 386313026) **[snippet only]**. |
| **식별신호/정량값** | "입경↓ → overpotential↑, 최소 입경 전극에서 특히"(snippet). Jeschull: dQ/dE peak 이동은 **사이클에 따른 hysteresis 증가**이며 **입경 자체가 평형전위를 바꾼다는 정량 mV 근거는 제시 안 함**; 형태학(void) 요인이 성능 지배, 대입자(d90 48.4 µm)도 소입자(d90 6.5 µm)와 성능 비등. |
| **흑연 적용성** | 직접. |
| **타당/한계** | 핵심 한계: 문헌은 입경 효과를 **kinetic overpotential·형태학**으로 귀속하며, **반경→평형 전위 U_j 이동(thermodynamic)**의 직접 정량 근거는 미발견. |
| **가설과의 관계** | **사용자 가설의 핵심 검증점**. 문헌 다수는 입경을 kinetic 변수로 취급 → "반경 분포 = 평형 이질성"이라는 사용자 가정은 **추가 입증 필요**. |
| tier | **근거미발견** (반경→평형전위 분포 환산의 1차 정량 근거 미확보) |

---

## 2. ★C-rate / GITT(near-equilibrium) 의존성 — 치우침이 kinetic인지 평형 이질성인지 가르는 시험

| 항목 | 내용 |
|---|---|
| **주장** | 저율로 갈수록 peak이 좁아지고 대칭에 가까워진다. 의사평형 조건(C/20 이하 또는 GITT)에서 정보 최대·feature 최선명. C/100에서 staging peak이 선명·추가 2L peak 출현. |
| **근거문헌** | est.2019 (S2352152X19308175) **[snippet]**; DVA rate-capability (S3050914925000652) **[snippet]**; Weng/Siegel/Stefanopoulou (2023) *Front. Energy Res.* 11, 1087269, DOI 10.3389/fenrg.2023.1087269 **[본문요약]**. |
| **식별신호/정량값** | 의사평형 = **C/20 이하**. C/100에서 peak 선명·discharge에 2L staging peak 추가 출현. polarization compensation(current interrupt)로 고율 ICA의 peak voltage shift 최소화 가능 → shift가 polarization(kinetic) 기원임을 역증명. |
| **GITT 평형 데이터** | Park *et al.* (2021) *Materials* 14(16), 4683, DOI 10.3390/ma14164683 **[본문요약]**: QOCP staging plateau **≈0.22 V, 0.12 V, 0.08 V (vs Li/Li⁺)** = LiC₇₂→LiC₃₆→LiC₁₂→LiC₆. D = 1×10⁻¹¹ ~ 4×10⁻¹⁰ cm²/s. 즉 **평형 전위는 입자 무관 thermodynamic 상수로 측정됨** — staging 전이전위가 입경에 따라 분포한다는 직접 증거는 이 GITT 데이터엔 없음. |
| **중요 nuance** | Weng/Siegel(2023): **"charge-discharge asymmetry exists at the material level"** — stage 2 전이 feature가 lithiation 방향에서 더 sharp·높음. 즉 비대칭의 **일부는 재료 내재(intrinsic, kinetic 아님)** — 전부를 kinetic으로도, 전부를 반경으로도 귀속 불가. |
| **타당/한계** | 강한 식별 시험. GITT/저율에서 **남는 잔여 폭** = 평형 이질성(반경 분포 포함)의 **상한**. |
| **가설과의 관계** | **결정적 분리 신호**. 저율·GITT에서 peak이 대칭·선명해지면 치우침은 주로 kinetic. 잔여 폭이 남으면 그 상한 안에서만 반경 분포 논의 가능. |
| tier | **확정**(C-rate/GITT 의존성·평형 plateau 값), **추정**(material-level 비대칭의 정확한 기원 분해) |

---

## 3. ★정량: 전형 흑연 음극에서 각 기작의 peak 폭 기여 mV 규모 비교

전제: 입자 5–20 µm, 표준 코인 하프셀, 0.05–1C.

| 비교 항목 | mV 규모 | 출처 | tier |
|---|---|---|---|
| staging plateau 간격(thermodynamic 기준자) | 0.22 / 0.12 / 0.08 V plateau; stage 2→1 전이 **≈65–85 mV**, 1L-4L-3L-2L **≈90 mV**, dense stage 2-1 **≈76 mV** | Park 2021 (10.3390/ma14164683); shrinking-annuli arXiv:1211.0027 snippet; RSC D2TA02420A snippet | 확정(plateau)/추정(전이 mV) |
| **kinetic 분극** (0.05C→0.5C) | **≈70 mV** (셀 전체) | Weng 2023 (10.1007/s40820-023-01183-6) | 확정 |
| Si 12→15 wt% 분극 급증(비교 척도) | <12 wt% ΔV<0.003 V → 15 wt% 급증 | aenm.202505674 snippet | 추정 |
| **반경 분포 → 평형 전위 이질성** 환산 규모 | **정량 mV 미발견** | — | **근거미발견** |
| 입경↓ → overpotential↑ | 정성("최소 입경에서 특히"), 정량 mV 미확보 | MDPI 6896 snippet; Jeschull 2020 | 근거미발견 |
| 두께 방향 SOC 구배(후막·고율) | 평탄 plateau SOC에서 최대(정성) | Maire/Touzin 2018; Tardif 2020 | 추정 |

**핵심 정량 대비**: kinetic 분극 ~70 mV(0.05C→0.5C)는 staging 전이 간격(65–90 mV)과 **동급 규모** → 유한 전류에서 kinetic이 peak 위치·폭을 staging 자체만큼 흔든다. 반면 **반경 분포가 평형 전위 이질성으로 환산되는 mV 규모는 1차 문헌에서 미확보** → 사용자 가설의 정량적 무게를 현재 근거로 확정 불가.

---

## 경쟁기작 매트릭스

| 기작 | 식별신호 (kinetic이면 전류 의존) | 흑연 정량규모 | 대표 문헌(DOI) | 반경가설과 분리가능성 |
|---|---|---|---|---|
| (a) 분극·확산한계 | **C-rate↑ → broaden·고전압 shift; 저율 C/20↓서 좁아짐** | ~70 mV(0.05→0.5C); C/6 초과 peak 소실 | Weng 10.1007/s40820-023-01183-6; est.2019 | **높음** — 저율/GITT서 사라지면 kinetic |
| (b) 접촉저항·전류분포 이질 | 전류 의존; DRT 고주파 peak | 모델로 broadening 재현, mV 미확보 | Farkhondeh JES 164 E3040 | 높음(전류 의존, 저율서 감소) |
| (c) SOC·두께 이질 | 후막·고율 의존; 평탄 plateau SOC서 최대 | 정성(80 µm 전극); 코인셀 mV 미확보 | Tardif arXiv:2005.04983; Maire 2018 | 높음(박전극·저율로 제거) |
| (d) 온도 | 저온서 broaden; 상온 고정 시 무관 | 정성; <250 K 상 불안정 | Senyshyn 2015 (S0378775315002311) | 통제로 제거 |
| (e) 입경(분포) | **약한 전류 의존 + 형태학**; 입경↓ overpotential↑ | overpotential 정성, **평형 U_j 이동 mV 미발견** | Jeschull 10.1149/1945-7111/ab9b9a | **이것이 가설 본체** — 단 kinetic으로 귀속되는 경향 |
| (★기준) staging 평형 plateau | 전류 무관(GITT QOCP) | 0.22/0.12/0.08 V; 전이 65–90 mV | Park 10.3390/ma14164683 | — (분리의 기준자) |

---

## 이 축 요약 · 치우침의 지배 기작 판정 · 열린 문제

**이 축 요약.** dQ/dV staging peak의 넓어짐·비대칭을 만들 수 있는 경쟁 기작 5종을 1차 문헌으로 조사했다. (a) 유한 전류 분극·확산 한계가 가장 강력하고 정량이 명확한 경쟁 기작이며(0.05C→0.5C에서 셀 분극 **~70 mV** 증가, C/6 초과서 peak 식별 수 급감, 의사평형 = C/20 이하), 이는 staging 전이 간격(65–90 mV)과 **동급 mV 규모**다. (b) 접촉저항/전류분포 이질, (c) 두께 방향 SOC 구배(후막·고율, 평탄 plateau SOC서 최대), (d) 온도(저온 broaden)는 모두 **전류 또는 전극설계·온도 의존** — 저율·박전극·상온 통제로 줄거나 사라진다. (e) 입자 크기 효과는 문헌 다수가 **kinetic overpotential·형태학**으로 귀속하며, **반경→평형 전위 U_j 분포(thermodynamic 이질성)**로 환산되는 1차 정량 근거는 본 검색에서 **미발견**.

**치우침의 지배 기작 판정 (kinetic vs radius).**
- **유한 전류 실측(코인셀 통상 C/10~1C)에서는 kinetic(분극·확산 한계)이 비대칭/넓어짐을 지배**한다고 볼 근거가 가장 강하다. 결정적 분리 신호 = **C-rate 의존성**: 저율(C/20 이하)·GITT로 갈수록 peak이 좁아지고 대칭에 가까워지며(C/100에서 staging peak 선명·추가 2L peak 출현), polarization compensation(current interrupt)으로 고율 peak shift를 제거할 수 있다는 사실이 shift의 kinetic 기원을 역증명한다.
- **반경 분포(사용자 가설)는 GITT/저율에서 남는 "잔여 폭"의 상한 안에서만** 정당화된다. 단 GITT QOCP는 staging 평형 전위를 입자 무관 thermodynamic 상수(0.22/0.12/0.08 V)로 측정하며, 반경이 이 전위를 입자별로 분포시킨다는 직접 증거는 확보되지 않았다 → **사용자 가설은 현재 1차 문헌상 정량적으로 미입증**(반증은 아님).
- **중요 nuance(보완 가능성)**: Weng/Siegel/Stefanopoulou(2023)는 charge-discharge 비대칭이 **"material level"에 내재**한다고 명시(stage 2 feature가 lithiation 방향서 더 sharp) — 비대칭의 일부는 kinetic도 반경도 아닌 **재료 내재**일 수 있다. 즉 치우침은 단일 기작이 아니라 (kinetic 지배 + 재료 내재 비대칭 + 잔여 평형 이질성)의 중첩일 개연성.

**가장 강한 DOI (분리 신호·정량 순).**
1. **Weng et al. 2023, *Nano-Micro Letters* 15:215, DOI 10.1007/s40820-023-01183-6** — kinetic 분극 ~70 mV 정량 + staging 이질 공존(가장 강한 kinetic 정량 근거).
2. **Park et al. 2021, *Materials* 14(16):4683, DOI 10.3390/ma14164683** — GITT QOCP staging 평형 plateau(0.22/0.12/0.08 V) = 분리의 기준자(평형 전위가 thermodynamic 상수임).
3. **est.2019, DOI 10.1016/j.est.2019.100812** (S2352152X19308175) — C-rate 의존성·C/20 의사평형(분리 시험의 직접 처방). *단 snippet only — master는 본문 정독으로 tier 승격 필요.*
4. **Weng/Siegel/Stefanopoulou 2023, *Front. Energy Res.* 11:1087269, DOI 10.3389/fenrg.2023.1087269** — material-level 내재 비대칭(보완 기작).

**열린 문제 (master·후속 축으로).**
1. **반경→평형 전위 이질성 mV 환산**: 사용자 가설의 핵심. 입자 반경 분포가 staging 전이전위 `U_j`를 입자간 어느 mV 폭으로 분포시키는지 정량한 1차 문헌 미발견 — 이론(elastic/coherency strain, surface energy, 표면-부피 비) 또는 단일입자 실측 문헌으로 별도 조사 필요.
2. **잔여 폭 분해**: GITT/C/100에서 남는 peak 폭 중 (입경 분포) vs (조성 이질) vs (재료 내재 비대칭) 비율을 분해한 실험 미확보.
3. **snippet 의존 출처 본문 정독**: est.2019, Maire/Touzin 2018, Senyshyn 2015, Farkhondeh 2017은 ScienceDirect 403으로 본문 미정독 — master가 정식 접근으로 수치·tier 승격 필요.
4. **단일 흑연 입자 실측**: "Interplay of Li intercalation and plating on a single graphite particle"(S254243512030619X) 등 단일입자 dQ/dV가 다입자 대비 얼마나 좁은지 = 반경 분포 기여의 직접 상한 실측 후보(본 축 미정독).

---

### 출처 목록 (본 축에서 실제 사용)

- Weng, S. et al. (2023) *Nano-Micro Letters* 15:215. DOI 10.1007/s40820-023-01183-6 — https://pmc.ncbi.nlm.nih.gov/articles/PMC10516836/ [본문요약]
- Park, J.H. et al. (2021) *Materials* 14(16):4683. DOI 10.3390/ma14164683 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8397968/ [본문요약]
- Tardif, S. et al. (2020) arXiv:2005.04983. DOI 10.48550/arXiv.2005.04983 — https://arxiv.org/abs/2005.04983 [abstract 페이지; PDF 디코드 실패]
- Jeschull, F. et al. (2020) *J. Electrochem. Soc.* 167(10):100535. DOI 10.1149/1945-7111/ab9b9a — https://iopscience.iop.org/article/10.1149/1945-7111/ab9b9a [본문요약]
- Weng, A., Siegel, J.B., Stefanopoulou, A. (2023) *Front. Energy Res.* 11:1087269. DOI 10.3389/fenrg.2023.1087269 — https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2023.1087269/full [본문요약]
- "Rate dependency of ICA (dQ/dV)…" (2019) *J. Energy Storage*. DOI 10.1016/j.est.2019.100812 — S2352152X19308175 [snippet only, ScienceDirect 403]
- Farkhondeh, M. et al. (2017) *J. Electrochem. Soc.* 164(11):E3040; (2014) *PCCP* 16(41):22555 [snippet only]
- "Lithiation heterogeneities of graphite according to C-rate and mass-loading" (2018) *Electrochim. Acta*. S0013468618307229 [snippet only]
- "Low-temperature performance… lithiated graphite" (2015) *J. Power Sources*. S0378775315002311 [snippet only]
- shrinking-annuli (thin-layer graphite) arXiv:1211.0027 [snippet only; PDF 디코드 실패]
- (비1차, 개념 보조) dQ/dV 실무 가이드 lipowergroup.com [tier 강등]

> abstract/snippet-only 출처는 본문 표에 명시·tier 강등 처리됨. master는 ScienceDirect 본문 접근으로 snippet 출처 수치를 검증·승격할 것.
