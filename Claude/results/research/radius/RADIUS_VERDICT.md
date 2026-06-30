# RADIUS_VERDICT — dQ/dV peak 형상 → U_j 분포 → 활물질 반경 분포 추산: 타당성 판정

> 대상: `Claude/results/v8-11/v8-11.tex`(Ch1 유도확장) + `versions/v11_final.py` 모델 위의 *해석 가설*.
> 근거: 4축 1차 문헌 조사(`10`·`11`·`12`·`13`) + 종합(`20_synthesis.md`). master 직접 정독·삼각검증.
> 보고 4-tier: 확정 / 근거미발견 / 추정 / 미검증. 작성 2026-06-30.

---

## 1. 한 줄 판정
**부분 타당·조건부.** 사용자의 *물리적 직관*(단일입자 1차전이 = 델타, ensemble 평균이 그것을 퍼뜨림)은 표준 열역학으로 **맞다**. 그러나 **"U_j 분포 = 반경 분포(반경만 의존)"라는 핵심 고리는 전형 마이크론 흑연(r≈2.5–10 µm)에서 정량적으로 무효**(반경→U_j 결합이 실측 peak 폭보다 ~1000배 작음)이고, **역변환은 ill-posed**이며, 실측 치우침은 **반경 분포보다 동역학적 분극이 지배**한다. ∴ *지금 형태대로(마이크론 흑연·반경 단독·직접 deconvolution)는 성립하지 않는다.* 단 **나노 활물질 + 근평형 측정 + 다른 broadening 공제 + 정규화/형태가정 + 독립 PSD 대조**라는 조건을 모두 갖추면 *부분적으로* 의미를 가질 수 있다.

---

## 2. 고리별 답 (사용자 추정의 단계 그대로)

### (L1) "Ω≥2RT면 단일 입자 dQ/dV는 유사 델타" — **맞다(평형 극한). [확정]**
- 정규용액 격자기체에서 Ω>2RT 면 자유에너지가 이중웰 → 평형 등온선 V_eq(ξ) 비단조(van der Waals loop). 참 평형은 **Maxwell 공통접선 작도**로 loop 을 수평 plateau(공존 전위)로 대체 → V(q) 평탄 → `dq/dV→∞` → **dQ/dV = 한 전위의 Dirac 델타**. 사용자 전제와 정합.
- ★단서 1: 모델의 `w_eff=(RT/F)(1−Ω/2RT)` 는 *매끈 등온선 근사*라 진짜 델타가 아니라 floor(0.05·RT/F≈**1.3 mV**) 클립 극협 종을 준다. 참 델타는 Maxwell 평형이고, 기본 설정은 `use_w_eff=False`(기본폭 `nRT/F`≈25.7 mV).
- ★단서 2: **고전류(Tafel)에서는 spinodal 이 사라져 단일 입자가 *균질* 충전**(델타 아님) — Bai·Cogswell·Bazant, *Nano Lett.* 11, 4890 (2011), 10.1021/nl202764f. 즉 "단일입자=항상 델타"는 근평형 극한 전용.
- ★단서 3: 흑연 전이가 모두 1차는 아니다 — **4L–3L 등은 solid-solution(연속)**. 가설은 *전이별로* 분리 적용해야 한다.

### (L2) "종모양 = 단일입자 델타 ⊛ U_j 분포(통계역학적 형상)" — **개념은 실재하나 유일 원인 아님. [추정]**
- 다입자 열역학에서 비단조 단일입자 화학퍼텐셜은 **입자 순차 충전(particle-by-particle)** 으로 거시 plateau 를 만든다 — Dreyer et al., *Nat. Mater.* 9, 448 (2010), 10.1038/nmat2730. 즉 "ensemble 평균이 단일입자 형상을 퍼뜨린다"는 그림 자체는 **foundational 하게 옳다**.
- ★그러나 결정적 반례: Dreyer 의 plateau 는 *동일* 입자(분포 없음)에서도 순차성만으로 생긴다 → **종폭이 반드시 U_j *분포* 때문이 아니다.** "델타 ⊛ 분포 = 흑연 종모양"을 직접 분해·검증한 1차문헌은 **근거미발견**.
- ★입자 *상호작용*이 있으면 사상이 깨진다: electro-autocatalysis 는 분포 없는 단일상에서도 가짜 plateau 를 만들고(Park·Chueh·Bazant, *Nat. Mater.* 20, 991 (2021), 10.1038/s41563-021-00936-1), 흑연은 avalanche 형 상관 전이로 분포 정보를 왜곡한다(Han·Grey·Rao, arXiv:2509.21047, 2025, preprint·미검증). ∴ **"ensemble 평균 = 정적 U_j 분포의 1:1 반영"은 입자 독립·근평형 극한에서만** 성립.

### (L3) "U_j 분포 = 입자 반경 분포(구형·반경만 의존)" — **★마이크론 흑연에서 불성립. [핵심 결함]**
- 반경이 전이 전위를 이동시키는 **기작은 실재**(Gibbs–Thomson 표면에너지 ΔV=−2γV_m/zFr, coherency elastic strain) — 단 둘 다 **1/r(또는 더 빠르게)** 작아진다. [확정: 기작]
- ★정량(축B 직접 계산, tier=추정·단 1/r 스케일 확정): r≈5 µm, γ≈0.5–1 J/m², V_m≈5.3×10⁻⁶ m³/mol → **ΔV ≈ 0.01–0.05 mV**. 실측 peak 폭(수십 mV)의 **약 1/1000**. γ 가정에 robust(2배 키워도 결론 불변).
- 큰 크기 효과(miscibility-gap 닫힘)는 **나노에서만**: LiFePO₄ 임계 반경 ≈ **22 nm**(Cogswell & Bazant, *ACS Nano* 6, 2215 (2012), 10.1021/nn204177u, γ≈39 mJ/m²). 마이크론 흑연은 적용 영역 밖.
- 흑연 staging 전위의 *평형* 입경 의존을 직접 보고한 문헌 **근거미발견** — 흑연 "particle size effect" 문헌은 전부 **kinetic/형태학**(Jeschull 2020 10.1149/1945-7111/ab9b9a; Weng 2023 10.1007/s40820-023-01183-6). GITT QOCP 는 staging 전위를 **입자 무관 상수**(0.22/0.12/0.08 V, Park 2021 10.3390/ma14164683)로 측정.
- ∴ 마이크론에서 r→U_j 사상은 **사실상 평탄**(반경이 바뀌어도 U_j 무감) → 그 분포를 peak 에서 읽어낼 신호가 애초에 없다.

### (L4) "peak → 분포 역변환(deconvolution)" — **ill-posed. [확정]**
- `peak = 단일입자 커널 ⊛ 분포` 는 **1종 Fredholm 적분방정식** = DRT(distribution of relaxation times)와 동형. DRT 가 1차 문헌에서 "intrinsically ill-posed, requires Tikhonov regularization" 로 명시됨. ∴ forward(분포→peak)만 well-posed, **역방향은 정규화/형태가정 없이는 비유일·불안정**(작은 노이즈→해 진동). 서로 다른 분포가 거의 같은 곡선을 줌(identifiability, arXiv:1702.02471).
- **dQ/dV(전압영역)에서 PSD 를 직접 역변환한 1차 선례 근거미발견** — 사용자 발상은 *신규 시도*. 가장 가까운 선례는 EIS diffusion-impedance(Song & Bazant 2012, arXiv:1205.6539)이고 그조차 **lognormal 형태가정 + forward-fit**.

### (L5) "반경 분포 추산" — **현 조건에선 불가. [확정: 부정]**
- L3(사상 평탄) × L4(ill-posed) × L2(다원인 중첩)의 합성 결과. 특히 실측 치우침은 **유한 전류 kinetic 분극**(0.05→0.5C 에서 ~70 mV, staging 간격과 동급; Weng 2023)이 지배 → 반경 분포 신호는 그 아래 묻힌다.

---

## 3. 어떤 조건이면 "맞는 말"이 되는가 (성립 조건 — 동시 충족 필요)
1. **근평형 측정**: GITT 또는 C/20–C/100 으로 동역학 꼬리(모델 N7/N8 lag)·분극을 제거. polarization compensation 으로 잔여 shift 확인. → 잔여 폭만이 *평형 이질성*의 상한.
2. **나노 활물질**: 반경→U_j 결합이 유의(mV~수mV)·단조가 되려면 **r ≲ 50–100 nm** 영역. 전형 마이크론 흑연은 부적격(박리 흑연·few-layer·나노 음극이라면 재검토).
3. **입자 독립 전이**: autocatalysis/avalanche(상관) 부재 — 흑연에선 의심스러우므로 operando 로 독립성 점검.
4. **반경이 U_j 이질성의 지배 원인**: 조성·표면상·접촉저항·국소 환경 이질성을 *공제*한 뒤 잔여를 반경에 귀속(전제이지 기정사실 아님).
5. **단일 격리 전이**: 인접 staging peak 과 중첩 없는 전이 1개. 단일입자 커널(델타 vs 유한폭) 사전 확정.
6. **정규화 + 형태가정 + 독립 검증**: non-parametric 직접 deconvolution 대신 Tikhonov/MaxEnt + lognormal 등 parametric, 그리고 **SEM 단면·레이저 회절 PSD 와 cross-validate** 전까지 미검증 처리.

위 6개가 모두 서면 가설은 "전이 전위 이질성 분포 추출"로서 의미를 갖고, *반경이 그 이질성의 지배 원인일 때에 한해* 반경 분포로 해석 가능. 마이크론 흑연 코인셀 통상 측정은 1·2·4를 만족하지 못한다.

---

## 4. 한계·반례 요약
- **정량 갭(치명적)**: 마이크론 흑연 반경→U_j ≈ 0.01–0.05 mV ≪ peak 폭(수십 mV). [축B]
- **다원인 중첩**: 치우침 = (kinetic 분극 지배) + (순차충전) + (재료 내재 비대칭, Weng/Siegel 2023) + (전극 전위 불균일, Cell Rep. Phys. Sci. 2023 "PSD 아님") + (잔여 평형 이질성). 반경은 마지막 항의 일부에 불과. [축C·D]
- **모델 자체의 설명**: Ch1 v8-11 은 동일 치우침을 *kinetic 꼬리*(N7/N8)로 이미 설명 — 사용자 가설은 이와 경쟁하며, 마이크론에선 kinetic 가설이 정량 우위.
- **역문제 비유일**: 같은 peak 을 여러 분포·여러 기작이 재현 → 반경 분포 유일 산출 불가. [축C]
- **반증 아님**: 위는 "마이크론 흑연·반경 단독·직접 역변환" 형태의 *무효* 판정이지, 나노/근평형 변형까지 부정하는 것은 아님(해당 직접 데이터는 근거미발견 = 열린 문제).

---

## 5. 실측·후속 권고 (가설을 *시험*하려면)
1. **C-rate 사다리 + GITT**: C/2→C/100 으로 peak 폭·비대칭의 C-rate 의존성을 측정. 저율로 갈수록 좁아지면 치우침은 kinetic; C/100·GITT 에서 *남는 잔여 폭*이 평형 이질성(반경 포함)의 상한 — 이 상한이 ~mV 미만이면 반경 가설은 정량적으로 닫힘.
2. **독립 PSD 동시 측정**: 동일 전극 SEM 단면/레이저 회절 PSD ↔ dQ/dV 잔여 폭 상관 검정. 무상관이면 반경 기여 기각.
3. **단일 입자 실측**: single-particle microelectrode dQ/dV 폭 vs 다입자 폭 차이 = ensemble 분포 기여의 직접 상한.
4. **나노/박편 흑연 대조**: few-layer·나노 흑연에서 staging 전위 입경 의존을 직접 측정(L3 의 나노 한정 변형 검증) — 현재 문헌 공백.
5. **모델 측**: 만약 분포 효과를 모델에 넣으려면, 반경 단독이 아니라 *일반 U_j 이질성 분포*(원인 불문)를 평형 peak 에 합성곱하는 항으로 도입하고, kinetic 꼬리와 **식별 가능하도록** C-rate 의존성을 구속조건으로 둘 것. (※ 구현은 본 조사 범위 밖 — 교수님 검토 후.)

---

## 6. 핵심 근거 DOI
- 단일입자 1차전이·고전류 균질: Bai·Cogswell·Bazant, *Nano Lett.* 2011, **10.1021/nl202764f**.
- 다입자 순차충전 plateau: Dreyer et al., *Nat. Mater.* 2010, **10.1038/nmat2730**.
- 입자 상호작용 인공물: Park·Chueh·Bazant, *Nat. Mater.* 2021, **10.1038/s41563-021-00936-1**; Han·Grey·Rao, **arXiv:2509.21047**(preprint).
- 크기-의존 상도(나노 한정): Cogswell & Bazant, *ACS Nano* 2012, **10.1021/nn204177u**; Meethong et al., *ESSL* 2007, 10.1149/1.2710960.
- 역문제 선례·ill-posedness: Song & Bazant 2012, **arXiv:1205.6539**; DRT Tikhonov(1종 Fredholm) 문헌군; identifiability **arXiv:1702.02471**; PSD forward Kirk et al. 2022, 10.1137/20M1344305.
- broadening≠PSD: Cell Rep. Phys. Sci. 2023, S2666-3864(23)00096-6.
- kinetic 분극·분리신호: Weng 2023, **10.1007/s40820-023-01183-6**; GITT 평형 plateau Park 2021, **10.3390/ma14164683**; 재료내재 비대칭 Weng/Siegel 2023, 10.3389/fenrg.2023.1087269.
- 해석틀(OCV=자리에너지 분포): McKinnon & Haering lattice-gas; Frumkin isotherm(Levi & Aurbach).

> abstract/snippet-only 출처(Nature/Springer 본문·ScienceDirect 403)는 각 카드에 tier 강등 표기. 핵심 정량(반경 0.01–0.05 mV 계산·Weng 70 mV·Park GITT·Cogswell 22 nm)은 본문/계산으로 검증됨.
