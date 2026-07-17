# L2_TIER_CANDIDATES — LCO tier 실측 앵커 후보 (v1.0.22 R3 · O-E)

> 스펙 원전 = `docs/v1.0.20/results/DIRECTION_SI_LCO_REPORT.md` §5 L2 행: "LCO tier-2/3 실측 앵커 강화 — 현행 LCO U_j/ΔS 는 tier-C 초기값(Xia/Reynier/Motohashi 경유 tier B). 1차 실측 OCV/엔트로피 앵커로 승격이 정직 문화에 부합."
> **규칙**: **웹 검증 성공분만** 후보 등재. 검증 실패 항목은 후보로도 올리지 않음(기억 서지 금지). **원장 등재·tab:lco-staging 갱신은 마스터 소관 — 본 문서는 후보 목록·검증 근거까지만.**
> tier 범례: A=1차 문헌 정량 확정값 · B=대표/부분 anchor 또는 2차 경유 · C=추정/placeholder.
> 현행 `tab:lco-staging`(sec11): 3 전이(T1 MIT ~3.90 V x0.94–0.75 · T2 od ~4.05 V x≈0.55 · T3 od ~4.17–4.20 V x≈0.48) — U_j·ΔS 값 tier-C 초기값(피팅 override 전제).

## 후보 표 (본 세션 WebSearch 검증분만)

| # | 서지 | DOI | 검증 근거(본 세션) | 무엇을 주는가(실측) | tab:lco-staging 승급 대상 행 | 원장 상태 |
|---|---|---|---|---|---|---|
| **C1** | Y. Reynier, J. Graetz, T. Swan-Wood, P. Rez, R. Yazami, B. Fultz, "Entropy of Li intercalation in Li$_x$CoO$_2$," *Phys. Rev. B* **70**, 174304 (2004) | 10.1103/PhysRevB.70.174304 | ASU pure 초록 대조: 평형전압 온도의존으로 ΔS(x) 실측(0.5<x≤1.0); config(Li·빈자리 무질서)가 O3 조성추세 대부분·phonon 음 baseline·**MIT 서 electronic≈config**; 척도 O3 max 4.2 k_B/atom·총 max 9.0 k_B/atom | **1차 실측 ΔS(x) 앵커**(dU_oc/dT) — 전자·config 분해 실측 | **T1(MIT) ΔS_rxn 슬롯**·O3 전 구간 ΔS: tier-C/B → **tier-A(측정)** | **이미 V1**(승급 근거 강화 후보) |
| **C2** | M. Ménétrier, I. Saadoune, S. Levasseur, C. Delmas, "The insulator--metal transition upon lithium deintercalation from LiCoO$_2$...," *J. Mater. Chem.* **9**, 1135--1140 (1999) | 10.1039/a900016j | RSC/search 대조: XRD+전기전도+열전능+$^7$Li MAS NMR 실측; **2상역 0.75≤x≤0.94** 는 구조 아닌 금속–비금속 전이가 구동 | MIT 2상역 조성창 1차 실측(x0.94–0.75) | **T1(MIT) x-범위 행**: 0.94–0.75 → **tier-A(측정)** | **이미 V1**(승급 근거 강화 후보) |
| **C3** | H. J. Kim 외, "Entropymetry for non-destructive structural analysis of LiCoO$_2$ cathodes," *Energy Environ. Sci.* **13**, 286--296 (2020) | 10.1039/C9EE02964H | RSC landing+search 대조: entropymetry 로 LCO ΔS 프로파일 실측 — 단조 감소(빈자리 점유)에서 **monoclinic 중간상(order–disorder)이 ΔS 기울기 반전**(제한된 배열·높은 질서); Ni 도핑이 질서 완화→monoclinic ΔS 진폭 감소 | **order–disorder(monoclinic) ΔS 서명 1차 실측** | **T2/T3(order–disorder) config ΔS 행**: tier-C → tier-A/B(측정) | **신규 후보**(현재 원장 미등재) |

## 검증 실패·제외 항목 (기억 서지 금지 — 후보 미등재)

| 항목 | 사유 |
|---|---|
| `ch2v22_bib.tex` reynier2004 비고의 "[동 그룹: *J. Electrochem. Soc.* **151**, A422 (2004)]" | 본 세션 검색으로 **별개 LCO 엔트로피 논문임을 확인 실패**(검색은 이 그룹의 JES/JPS 엔트로피 논문이 흑연 계열일 가능성 시사). LCO L2 후보로 미등재 — **마스터가 비고의 정확한 서지·대상물질 재확인 요망**. |
| "Operando monitoring the insulator-metal transition of LiCoO₂" (검색 표출) | 서지·측정 상세 미검증 → 제외. |
| C3 의 정확한 수치 ΔS 값 | RSC 전문 403(landing/초록만 확인) — 정성 서명(기울기 반전)은 확인, **정량값은 미확보** → 등재 시 마스터가 전문 대조 요. |

## 판정 요약

- **웹 검증 성공 후보 = 3건**(C1 reynier2004 · C2 menetrier1999 · C3 EES-entropymetry2020).
- **핵심 공백 = ΔS_rxn tier**: 현행 tab:lco-staging 의 U_j(전이 전압)는 이미 reimers1992/xia2007(V1, tier A/B)로 앵커돼 있으나 **ΔS_rxn 값이 tier-C 초기값** — 승급 실측 앵커는 **엔트로피 측정** 문헌이 핵.
  - T1(MIT)·O3 ΔS → **C1 reynier2004**(실측 dU/dT, electronic·config 분해)로 tier-A 승급 가능.
  - T2/T3(order–disorder) config ΔS → **C3 EES-entropymetry2020**(monoclinic ΔS 실측 서명)로 승급 가능 — **신규 등재 후보**.
  - T1 x-범위 → **C2 menetrier1999**(2상역 0.94–0.75 실측)로 tier-A 승급 가능.
- **주의**: C1·C2 는 이미 V1(등재는 tier 격상·사용처 추가 문제), C3 만 신규 서지. **등재·표 갱신은 마스터 소관**(본 후보 목록·검증 근거까지).
- **L5 연동**: C1(reynier2004)은 x=½·x=**5/6** 질서상을 명기 — 현행 charge-order 슬롯의 x=2/3 배정과 불일치(→ `L5_CHARGEORDER_CHECK.md`). C3 도 T2/T3 config ΔS 재소싱 대안.
