# 조사 카드 — 축 B: 입자 반경 → 전이/평형 전위 결합 기작·부호·크기

> 작업: 학술 조사 sub (4세션 분업). 배정 축 = B (입자 반경이 삽입 전극의 평형/전이 전위를 이동시키는 물리 기작·부호·정량 규모, 흑연 마이크론 입자 적용성).
> 종합·verdict·타 축 카드는 master 전담. 본 카드는 축 B 단일.
> 작성일 2026-06-30. 모든 tier·DOI 명시. 1차 문헌 web search 검증.

---

## 배경 가설 (사용자)

흑연 staging 전이 j 는 전이 전위 U_j 에 dQ/dV peak 을 낸다. **입자(구형 가정) 반경 r 이 U_j 를 결정**한다면, U_j 분포 = 반경 분포가 되어 dQ/dV peak 형상 → 입자 반경 분포 역산 가능. 본 축은 이 가설의 **사활 전제** — "반경 r → 전이 전위 U_j 사상이 실제로 존재하고, 그 크기가 실측 peak 폭(수십 mV)을 설명할 규모인가" — 를 1차 문헌으로 검증.

---

## §1. 입자 크기가 삽입 전극 평형/전이 전위를 이동시키는 물리 기작

크기 의존 전위 shift 의 후보 기작은 세 갈래로, 모두 **표면/계면 항이 부피 대비 커지는 1/r 스케일**에서 발생한다.

### (a) Gibbs–Thomson / 표면에너지 효과

곡률 있는 입자는 표면적/부피 비가 1/r 로 커져, Gibbs–Thomson 관계로 화학퍼텐셜이 이동한다. 표준형:

  Δμ = 2 γ V_m / r   →   전위 환산 ΔV = − Δμ / (zF) = − 2 γ V_m / (z F r)

- γ = 표면(계면) 에너지 [J/m²], V_m = molar volume [m³/mol], r = 입자 반경, z = 전자수, F = Faraday.
- **부호**: 작은 입자일수록 화학퍼텐셜이 올라가 → 삽입 반응(Li 환원 삽입)의 평형 전위는 일반적으로 작은 입자에서 **낮아지는 방향**(탈리튬화 기준 phase 안정성 감소). 단 부호는 어느 상(빈/찬)이 표면에너지가 큰가에 의존하며 재료별로 다를 수 있음(surface wetting 부호 의존).
- 출처: Gibbs–Thomson의 Δμ = 2γV_m/R 형태는 핵생성·Ostwald ripening 표준식 (arXiv cond-mat/9605142, "The Gibbs–Thomson formula at small island sizes"); 전극 적용은 아래 §2의 LiFePO4 phase-field 문헌과 Ag 합금 음극 Gibbs–Thomson 연구(ACS Appl. Energy Mater. 2022, DOI 10.1021/acsaem.1c04127).

### (b) Coherency / elastic strain energy 의 크기 의존

이상(二相) 공존 입자에서 두 상의 lattice misfit 이 만드는 coherency strain energy 가 자유에너지에 더해져 **miscibility gap(고용 한계)을 좁히고**, 임계 크기 이하에서 gap 을 완전히 닫는다(2상 → 단상 solid-solution).

- LiFePO4: Cogswell & Bazant, *ACS Nano* 6 (2012) 2215, DOI **10.1021/nn204177u**. γ ≈ **39 mJ/m²**(미세구조 micrograph 로 37 mJ/m² 추정), coherency strain 으로 **임계 입자 크기 ≈ 22 nm 에서 miscibility gap 소멸**, 실온 coherent 고용 한계 0.09 < x < 0.91. plateau 가 평탄 대신 **upward-sloping** 으로 기울어짐(= 전위가 조성에 따라 이동).
- 선행: Meethong, Huang, Carter, Chiang, *Electrochem. Solid-State Lett.* 10 (2007) A134, DOI **10.1149/1.2710960** ("Size-Dependent Lithium Miscibility Gap in Nanoscale Li₁₋ₓFePO₄"). 크기 감소 → free energy of mixing 수정(표면에너지+표면응력 + coherency stress) → gap 폭 감소. (원문 paywall — 수치는 Cogswell-Bazant 로 교차.)

### (c) 표면 재구성 / surface phase / 비화학량론

표면 wetting(표면이 특정 상으로 젖음)·표면 재구성·표면 비화학량론이 작은 입자에서 평형 조성·전위 profile 을 바꿈. LiFePO4 3D 나노입자에서 surface wetting + coherency strain 이 miscibility gap closure·계면 형태·상 미세구조를 지배(Cogswell & Bazant 류, *ACS Nano* 9 (2015) 7591, DOI **10.1021/acsnano.5b02555**).

---

## §2. ★정량 규모 비교 — 나노 LiFePO4 vs 마이크론 흑연 (1/r 스케일)

### LiFePO4 나노입자 (~20–100 nm) 의 크기 효과 규모

- **임계 크기 ≈ 22 nm** 에서 miscibility gap 이 닫힘 (Cogswell & Bazant, DOI 10.1021/nn204177u). 즉 크기 효과가 상도(phase diagram)를 정성적으로 바꾸는 것은 **나노 영역(수십 nm)에 한정**.
- γ = 39 mJ/m², LiFePO4 V_m ≈ 4.4×10⁻⁵ m³/mol, z=1.
- Gibbs–Thomson 전위 shift 추정 (r = 22 nm = 2.2×10⁻⁸ m):
  ΔV = 2 γ V_m /(zF r) = 2 × 0.039 × 4.4e-5 / (1 × 96485 × 2.2e-8)
     ≈ 3.43e-6 / 2.12e-3 ≈ **1.6 mV** (r=22 nm) 정도. **[tier=추정]**
  → 표면에너지 단독 항만으로는 22 nm 에서도 ~1–2 mV 수준; gap closure 의 큰 효과는 주로 **coherency strain**(elastic) 항에서 옴. 즉 LiFePO4에서 "크게 보이는" 크기 효과의 본질은 표면에너지가 아니라 strain·표면 wetting 의 협동.

### 동일 기작을 마이크론 흑연(5–20 µm, r ≈ 2.5–10 µm)에 적용 → 1/r 로 축소

표면에너지(Gibbs–Thomson) 항은 1/r 이므로, 나노(22 nm)→마이크론(r=5 µm) 으로 가면 r 비 ≈ 5e-6 / 2.2e-8 ≈ **227 배** → shift 도 1/227 로 축소.

- 흑연 추정(γ 가정 필요): 흑연 basal/edge 표면에너지는 이방성 크나, 보수적으로 γ ~ 0.1–1 J/m², V_m(graphite, C 기준) ≈ 5.3×10⁻⁶ m³/mol, r = 5 µm = 5×10⁻⁶ m, z=1:
  γ=0.5 J/m² 가정 시 ΔV = 2 × 0.5 × 5.3e-6 /(96485 × 5e-6) ≈ 5.3e-6 / 0.48 ≈ **1.1×10⁻² mV ≈ 0.01 mV**. **[tier=추정]**
  γ=1 J/m² 라도 ~0.02 mV. r=10 µm 이면 절반.
- **판정(정량)**: 마이크론 흑연에서 Gibbs–Thomson 표면에너지 전위 shift 는 **~0.01–0.05 mV 규모**로, 실측 dQ/dV peak 폭(수십 mV, 전형 10–50 mV)보다 **3 자리수(≈1000배) 작다**. → 표면에너지 기작으로는 peak 폭을 **전혀 설명 못 함**. coherency strain 도 r 이 µm 면 입자 전체가 incoherent 분리(전위·균열로 strain 완화) 가능해 크기 의존이 사라지는 영역. **[tier=추정, 단 1/r 스케일링은 확정 물리]**

> ★핵심: 크기→전위 결합은 **나노(<~50 nm)에서만 유의(mV~수mV)**하고, 마이크론 흑연에서는 1/r 로 사실상 소멸(<0.1 mV). 실측 dQ/dV peak 폭(수십 mV)은 입자 크기 분포가 아니라 **본질적 staging 열역학(2상 plateau 폭·온도(kT)·전이 자유에너지) + 동역학적 분극·입자간 불균일** 에서 옴.

---

## §3. 흑연 특이성 — staging 전이 전위의 입자 크기 의존, r→U_j 단조성

### 직접 측정/계산 문헌

- 흑연 staging 전이 전위의 **입자 크기 의존을 직접 보고한 평형 열역학 문헌은 근거 미발견**. 검색된 흑연 "particle size effect" 문헌은 모두 **kinetic / heterogeneity / rate capability** 효과:
  - "Understanding particle size effect on fast-charging behavior of graphite anode using ultra-thin-layer electrodes" (ResearchGate 386313026) — fast-charging·rate, 평형 전위 shift 아님.
  - "Kinetic Limits of Graphite Anode for Fast-Charging" (PMC10516836, Nano-Micro Lett. 2023, DOI 10.1007/s40820-023-01183-6) — 입자 크기 <10 µm 시 계면 확산·수송이 율속; 동역학.
  - "Multiscale dynamics of charging and plating in graphite" (Nat. Commun. 2023, DOI 10.1038/s41467-023-40574-6) — 입자 단위 lithiation 불균일이 크기·형상·배향·표면·C-rate 에 의존(동역학·heterogeneity). 평형 U_j 이동 아님.
  - dQ/dV peak shift 가 보고될 때 그 원인은 **온도(0/−20 °C 에서 저전위로 이동, kinetic+entropic), C-rate, 분극** — 입자 크기 평형 효과 아님 (ACS Electrochem. 2024, DOI 10.1021/acselectrochem.4c00079).

### 흑연의 LiFePO4 대비 차이 (크기 효과를 더 약하게 만드는 요인)

- 흑연은 **층상·이방성**: lithiation 은 c-축 갤러리 팽창(stage)으로 일어나며, ab-plane 내 2D 도메인. 표면에너지·strain 이 LiFePO4(3D olivine, 강한 1D 채널 misfit)와 질적으로 다름.
- 흑연 입자는 마이크론급이고 stage 전이 misfit strain 은 박리·전위로 완화되기 쉬워 coherency strain 의 크기 의존이 약함.
- 따라서 LiFePO4 의 "나노에서 gap 닫힘" 같은 극적 크기 효과를 흑연 마이크론에 그대로 이식할 근거 없음.

### r → U_j 사상의 단조성(역변환 가능성)

- 가설이 성립하려면 r → U_j 가 **단조(monotonic)**여야 역산 가능. §1(a) Gibbs–Thomson 은 형식상 U_j ∝ 1/r 로 단조이긴 하나(크기↑ → shift↓ 단조), §2 에서 본 대로 **마이크론에서 기울기가 0 에 수렴**(shift<0.1 mV) → 사실상 평탄(r 변화에 U_j 무감) → **역변환 불능(ill-posed)**. peak 폭이 크기 분포 정보를 담지 못함.
- 또한 실제 peak 폭은 staging 2상 plateau 의 본질적 폭 + kT 열적 broadening + 동역학 분극이 지배하므로, 설령 미세한 1/r shift 가 있어도 이 큰 배경에 묻혀 **분리 불가**. **[tier=추정/근거미발견 — 흑연 직접 데이터 부재]**

---

## 조사 카드 (schema)

| # | 주장 | 근거문헌(저자·연도·DOI/URL) | 지배식/정량값 | 흑연 적용성 | 타당/한계 | 사용자 가설 관련성 | 정독범위 | tier |
|---|------|------|------|------|------|------|------|------|
| B1 | 입자 크기는 Gibbs–Thomson 으로 평형 화학퍼텐셜·전위를 1/r 로 이동 | Gibbs–Thomson 표준 (arXiv cond-mat/9605142); 전극 적용 Ag 음극 ACS Appl. Energy Mater. 2022, DOI 10.1021/acsaem.1c04127 | Δμ=2γV_m/r, ΔV=−2γV_m/(zFr) | 기작은 보편, 크기는 1/r | 부호는 표면 wetting 의존 | 결합 존재는 확정, 크기가 관건 | 검색 요약 + 식 유도 | 확정(기작), 추정(부호) |
| B2 | LiFePO4 나노입자에서 coherency strain 이 miscibility gap 좁히고 ≈22 nm 에서 닫음 | Cogswell & Bazant, ACS Nano 6(2012)2215, DOI 10.1021/nn204177u | γ≈39 mJ/m², 임계 r≈22 nm, 0.09<x<0.91, plateau upward-slope | LiFePO4 한정, 흑연 ≠ | 큰 크기 효과는 strain 항이 주도(표면에너지 단독은 ~1–2 mV) | 흑연엔 직접 이식 불가 근거 | ar5iv 전문 발췌 정독 | 확정 |
| B3 | 크기-의존 miscibility gap 의 선행 정립 | Meethong, Huang, Carter, Chiang, ESSL 10(2007)A134, DOI 10.1149/1.2710960 | gap 폭 = f(표면에너지+표면응력+coherency stress) | LiFePO4 | 원문 paywall, B2 로 교차검증 | 크기 효과 = 나노 현상 | 초록·인용 요약(원문 미접근) | 추정(수치), 확정(존재) |
| B4 | ★마이크론 흑연(r≈5 µm)의 Gibbs–Thomson 전위 shift ≈ 0.01–0.05 mV | B1 식 + γ~0.5–1 J/m², V_m≈5.3e-6 m³/mol 가정 | ΔV≈2×0.5×5.3e-6/(96485×5e-6)≈0.011 mV | ★직접 대상 | γ 가정 의존, 그러나 1/r 스케일은 확정 → 결론 robust | ★실측 peak 폭(수십 mV)보다 ~10³배 작음 → 가설 부정 | 식 직접 계산 | 추정(값), 확정(1/r 스케일) |
| B5 | 흑연 "particle size effect" 문헌은 평형 전위 shift 아님, 모두 kinetic/heterogeneity | Nano-Micro Lett. 2023 DOI 10.1007/s40820-023-01183-6; Nat.Commun. 2023 DOI 10.1038/s41467-023-40574-6; ACS Electrochem. 2024 DOI 10.1021/acselectrochem.4c00079 | <10 µm 시 계면확산 율속; dQ/dV shift = 온도·C-rate 원인 | 흑연 직접 | 크기→평형 U_j 이동 직접 보고 부재 | r→U_j 평형 사상 근거 미발견 | 검색 요약 정독 | 확정(kinetic), 근거미발견(평형 size shift) |
| B6 | r→U_j 사상이 마이크론에서 사실상 평탄 → 역변환 ill-posed | B4 + staging 본질 plateau·kT broadening | shift<0.1 mV ≪ peak 폭 수십 mV | 흑연 | 흑연 직접 데이터 부재 | ★peak 폭이 크기 분포 정보 담지 못함 | 식+논리 | 추정 |

---

## 이 축 요약 · ★흑연 마이크론 정량 판정 · 열린 문제

**기작 존재(확정):** 입자 반경이 삽입 전극의 평형/전이 전위를 이동시키는 물리 기작은 실재한다 — Gibbs–Thomson 표면에너지(Δμ=2γV_m/r)와 coherency elastic strain energy. 둘 다 1/r(또는 더 빠른) 로 작아진다. 부호는 표면 wetting 에 의존.

**★흑연 마이크론 정량 판정(이 축의 결론):** **반경→U_j 결합은 마이크론 흑연(r≈2.5–10 µm)에서 실측 dQ/dV peak 폭(수십 mV)을 설명할 정량 규모가 아니다.**
- 표면에너지(Gibbs–Thomson) shift 는 마이크론에서 **~0.01–0.05 mV**(tier=추정; γ=0.5–1 J/m², V_m≈5.3e-6 m³/mol 가정, 식 ΔV=2γV_m/zFr 직접 계산) → peak 폭보다 **약 3 자리수(≈1000배) 작다.**
- 큰 크기 효과를 내는 coherency-strain 기반 miscibility-gap closure 는 **나노(LiFePO4 임계 ≈22 nm)에서만** 발생하는 현상이며(가장 강한 근거 = **Cogswell & Bazant, ACS Nano 6 (2012) 2215, DOI 10.1021/nn204177u**, γ≈39 mJ/m², 22 nm), 마이크론 흑연에는 적용 영역 밖.
- 흑연 staging 전이 전위의 입자 크기 평형 의존을 직접 보고한 문헌은 **근거 미발견**; 흑연 "particle size effect" 문헌은 전부 **동역학·heterogeneity·rate**(예: Nano-Micro Lett. 2023, DOI 10.1007/s40820-023-01183-6).
- 따라서 **r→U_j 사상은 마이크론에서 사실상 평탄(역변환 ill-posed)** → dQ/dV peak 형상으로 입자 반경 분포를 역산한다는 가설은 이 축에서 **부정적**. (실측 peak 폭은 staging 2상 plateau 의 본질 폭 + kT 열적 broadening + 동역학 분극이 지배.)

**열린 문제:**
1. 흑연 나노/박편(<100 nm 두께 박리 흑연·few-layer)에서 staging 전위의 크기 의존을 직접 측정한 데이터 — 본 검색에서 미발견. 존재한다면 가설의 나노 한정 변형은 검증 여지.
2. 흑연 표면에너지 γ(basal vs edge, Li 흡착 후) 실측값 — 본 추정은 γ~0.5–1 J/m² 가정. 정확 γ 확보 시 B4 추정 정밀화 가능(결론(≪peak 폭)은 γ 가정에 robust).
3. dQ/dV peak 폭을 결정하는 진짜 인자(staging plateau 본질 폭 vs 분극 vs 입자간 U 분포) 의 분해 — 이는 master 의 타 축(열역학 plateau·동역학 분극 축)과 교차 종합 필요.
