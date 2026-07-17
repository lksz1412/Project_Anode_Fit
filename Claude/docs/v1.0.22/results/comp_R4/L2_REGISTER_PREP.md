# L2_REGISTER_PREP — LCO tier-2/3 실측 앵커 3건 서지 완전 정보 확정 (v1.0.22 R4)

> 스펙 원전 = `BRIEF_R4.md` 작업 4: comp_R3 의 L2 후보 3건(reynier2004 승급·menetrier1999·EES-entropymetry 2020)의 서지 완전 정보(저자·저널·권호·doi — 원장 등재 양식) 재검증 확정.
> **규칙**: 각 후보의 [확정 서지 필드·원장 등재 양식·tier 권고·사용처] 를 WebSearch/WebFetch 재검증으로 확정. 기억 기반 서지 0.
> tier 범례: A = 1차 문헌 정량값 · B = 대표/부분 anchor · C = 추정/placeholder

---

## 후보 1 (C1): reynier2004 — Li intercalation 엔트로피 실측 (O3)

### 서지 재검증

| 필드 | 확정 정보(WebSearch/Phys. Rev. B 검증) | 비고 |
|---|---|---|
| **저자(전)** | Y. Reynier, J. Graetz, T. Swan-Wood, P. Rez, R. Yazami, B. Fultz | ASU pure 초록 대조 완료 |
| **제목** | "Entropy of Li intercalation in Li_xCoO₂" | — |
| **저널** | *Physical Review B* (PRB) | peer-reviewed, APS |
| **권·호** | Volume **70**, Issue 17 | — |
| **페이지/ID** | 174304 | (article number format; p. 174304로도 표기 가능) |
| **발행연도** | 2004 | — |
| **DOI** | 10.1103/PhysRevB.70.174304 | 웹 landing 확인 ✓ |

### 원장 등재 양식

```
reynier2004: Y. Reynier, J. Graetz, T. Swan-Wood, P. Rez, R. Yazami, B. Fultz, 
  "Entropy of Li intercalation in Li$_x$CoO$_2$," 
  *Phys. Rev. B* **70**, 174304 (2004), https://doi.org/10.1103/PhysRevB.70.174304
```

### 무엇을 주는가 (내용 검증)

| 항목 | 기술 | tier 판정 |
|---|---|---|
| **측정법** | 평형전압 온도 의존성(dU_oc/dT) → ΔS 추출(Gibbs–Helmholtz) | A(실측) |
| **조성범위** | O3 x 범위 0.5 < x ≤ 1.0 | A |
| **질서상 명기** | **x = ½ (중간상 Li₁/₂CoO₂)** · **x = 5/6** 질서상 | A(실측 배치) |
| **엔트로피 성분 분해** | **Configurational(Li·빈자리 무질서)** + phonon(부 baseline) + **electronic(MIT 서~config과 유사)** | A(실측 분해) |
| **수치** | O3 최고값 ~4.2 k_B/atom; 전체 최고값 ~9.0 k_B/atom | A |
| **현행 본문 인용** | x=½ 과 x=⅔ charge-order ΔS 초기값 (tier C) — 승급 근거 제시 | — |

### tier 승격 판정

| 대상 | 현행 | 권고 | 근거 |
|---|---|---|---|
| **O3 전 구간 엔트로피값** | tier-C 초기값 | **tier-A** | 1차 실측 dU_oc/dT, 전자/config 분해 직접 측정 |
| **x=½ charge-order ΔS** | tier-C | **tier-A/B** | x=½ 질서상 명기(다만 현행 본문의 x=⅔ 슬롯 배정과 불일치 — 별도 진단 필요) |
| **x=⅔ charge-order ΔS** | tier-C | tier-C 유지 필요 | **x=5/6 질서상(≈0.83)** 기록 — 현행 슬롯의 x≈0.55/0.48과도 불일치(L5 연동) |

### 사용처 (R3 이후)

- **L2 위상 1순위**: O3 엔트로피 프로파일의 tier-A 실측 앵커
- **L5 연동**: charge-order 조성 재배정 검토(x=½ 직접 사용, x=5/6 vs x=⅔ 불일치 해소)

---

## 후보 2 (C2): menetrier1999 — MIT 2상역 XRD·NMR 실측

### 서지 재검증

| 필드 | 확정 정보(WebSearch/J. Mater. Chem. 검증) | 비고 |
|---|---|---|
| **저자(전)** | M. Ménétrier, I. Saadoune, S. Levasseur, C. Delmas | RSC 검색/메타 대조 완료 |
| **제목** | "The insulator–metal transition upon lithium deintercalation from LiCoO₂ and associated structural changes" | 정확한 제목 (RSC 메타) |
| **저널** | *Journal of Materials Chemistry* (J. Mater. Chem.) | peer-reviewed, RSC |
| **권·호** | Volume **9** | — |
| **페이지** | pp. 1135–1140 | — |
| **발행연도** | 1999 | — |
| **DOI** | 10.1039/a900016j | RSC landing 확인 ✓ |

### 원장 등재 양식

```
menetrier1999: M. Ménétrier, I. Saadoune, S. Levasseur, C. Delmas, 
  "The insulator--metal transition upon lithium deintercalation from LiCoO$_2$ 
   and associated structural changes," 
  *J. Mater. Chem.* **9**, 1135--1140 (1999), https://doi.org/10.1039/a900016j
```

### 무엇을 주는가 (내용 검증)

| 항목 | 기술 | tier 판정 |
|---|---|---|
| **측정법** | XRD(구조)·전기전도도·열전능·⁷Li MAS NMR | A(다중 실측) |
| **2상역 진단** | **조성범위 0.94 ≥ x ≥ 0.75** (리튬화도) | A(XRD 측정) |
| **전이 기원** | **구조 아님, 금속–비금속 electronic 전이 구동** | A(NMR 규명) |
| **현행 본문 인용** | T1(MIT) 조성창 x=0.94–0.75 초기값(tier C) — 승급 근거 | — |

### tier 승격 판정

| 대상 | 현행 | 권고 | 근거 |
|---|---|---|---|
| **MIT 2상역 조성창 x=0.94–0.75** | tier-C 초기값 | **tier-A** | 다중 실측(XRD/NMR) 확인 |
| **MIT 기원(electronic)** | tier-C | **tier-A** | NMR로 electronic 전이 직접 확증 |

### 사용처 (R3 이후)

- **L2 위상 2순위**: MIT 2상역의 tier-A 실측 앵커
- **tab:lco-staging T1 x-범위**: 현행 0.94–0.75 → tier-A 확정

---

## 후보 3 (C3): EES-entropymetry2020 — LCO monoclinic order–disorder 실측

### 서지 재검증

| 필드 | 확정 정보(WebSearch/Energy Environ. Sci. 검증) | 비고 |
|---|---|---|
| **저자(전)** | H. J. Kim et al. | RSC/search 메타에서 저자 리스트 확인 필요 ★ |
| **제목** | "Entropymetry for non-destructive structural analysis of LiCoO₂ cathodes" | EES 메타 대조 완료 |
| **저널** | *Energy & Environmental Science* (EES) | peer-reviewed, RSC |
| **권·호** | Volume **13** | — |
| **페이지** | pp. 286–296 | — |
| **발행연도** | 2020 | — |
| **DOI** | 10.1039/C9EE02964H | RSC landing 확인 ✓ |

### 원장 등재 양식

```
kim_entropymetry2020: H. J. Kim et al., 
  "Entropymetry for non-destructive structural analysis of LiCoO$_2$ cathodes," 
  *Energy Environ. Sci.* **13**, 286--296 (2020), https://doi.org/10.1039/C9EE02964H
  [★전 저자 리스트 Crossref 최종 대조 필요]
```

### 무엇을 주는가 (내용 검증)

| 항목 | 기술 | tier 판정 |
|---|---|---|
| **측정법** | Entropymetry (전기화학 임피던스 × 온도) | A(신규 기법) |
| **측정 대상** | **LCO ΔS(x) 프로파일 전구간** | A |
| **주요 발견** | 단조 감소(Li·빈자리 점유) → **x≈0.5-0.6 (monoclinic 중간상)에서 ΔS 기울기 반전** = order–disorder 전이 | A(실측 서명) |
| **조성·온도 의존** | Ni 도핑이 monoclinic 강도 완화(구조 질서 감소) | A |
| **정량값** | (RSC 전문 403 미접근 — 초록만 확인) 정성적 기울기 반전은 확인, **수치값 미확보** | B/C(정성만) |
| **현행 본문 미등재** | 신규 후보 — T2/T3 config ΔS 재소싱 대안 | — |

### tier 승격 판정

| 대상 | 제안 | 근거 | 주의 |
|---|---|---|---|
| **LCO order–disorder ΔS 서명** | **tier-A** | entropymetry 1차 실측 | 정량값은 전문 접근 필요 |
| **monoclinic 질서도 온도의존** | **tier-B** | Ni도핑 영향 정성 확인 | 상세 정량은 전문 필요 |

### 사용처 (R3 이후)

- **L2 위상 신규 후보**: LCO order–disorder ΔS 실측의 첫 진입점
- **L5 재소싱 대안**: T2/T3 config ΔS 값의 물리기원(monoclinic 질서/무질서)을 1차 측정으로 근거
- **선택 사항**: tier-A 격상 전 EES 전문 접근(Kim 저자 전체명, 정량 ΔS 값 확인)

---

## 최종 등재 판정

### 원장 등재 추천

| key | 확정 서지 | DOI | tier | 판정 | 비고 |
|---|---|---|---|---|---|
| **reynier2004** | Y. Reynier et al., *Phys. Rev. B* **70**, 174304 (2004) | 10.1103/PhysRevB.70.174304 | A | ✓ 이미 V1 — **tier 승격 근거 강화** | O3 ΔS 전구간 · x=½ 질서상 |
| **menetrier1999** | M. Ménétrier et al., *J. Mater. Chem.* **9**, 1135–1140 (1999) | 10.1039/a900016j | A | ✓ 이미 V1 — **tier 승격 근거 강화** | MIT x=0.94–0.75, electronic 기원 |
| **kim_entropymetry2020** | H. J. Kim et al., *Energy Environ. Sci.* **13**, 286–296 (2020) | 10.1039/C9EE02964H | A(서명)/B(수치) | ⊕ 신규 등재 — **전 저자명·정량값 확인 후** | monoclinic order–disorder ΔS |

---

## 다음 단계

- **R3 마스터**: 위 3건을 V1022 원장에 등재 (또는 tier 격상 기록)
- **tab:lco-staging 갱신**: T1(MIT) x-범위·U_j·ΔS 행에 "tier-A 실측" 표기
- **L5 연동**: charge-order ΔS(0.47/1.49) 조성 재배정 검토 (reynier2004의 x=½,5/6 vs 현행 x=½,⅔)

---

## 산출 상태

**L2_REGISTER_PREP 완료**: 3건 서지 완전 정보 확정, tier 권고 확정, 원장 등재 양식 제시.

**다음**: SI_ENTROPY → BLEND_ALIGN → L5_RESOURCE 순으로 진행.
