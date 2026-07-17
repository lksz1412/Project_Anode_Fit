# SIC_CASES — Si–C 복합 음극 실측 문헌 (v1.0.22 R4 승급 조사 창, D22-4)

> 스펙 원전 = 마스터 승급 지시 축 2: Si–C 복합(사용자 확정 케이스, D22-3) — 상용급 Si–C 복합 음극의 전위·용량·순환 곡선 실측 문헌.
> 저비용 창(R4) 원 상태: `comp_R4/SI_CASES.md` 케이스 3 = **0건("WebSearch 검증 대기 중")** — 미확보로 종결.
> **규칙 승계**: 기억 서지 절대 금지·웹 실검증분만·검증 실패 항목은 목록 미등재.
> tier 범례: **A** = 1차 문헌·정량 내용 본 세션에서 독립 확인 · **B** = DOI·서지 확인 완료이나 정량 내용 일부만 접근

---

## 검증 문헌 표

| # | 특징 | 검증 문헌 | DOI | tier | 대표 수치(원문 확인) |
|---|---|---|---|---|---|
| 1 | **상용(산업)급 원료 Si 기반 Si-C 복합 — 전위·용량·순환 전체 특성화** | Andersen, Foss, Voje, Tronstad, Mokkelbost, Vullum, Ulvestad, Kirkengen, Mæhlen (2019), "Silicon-Carbon composite anodes from industrial battery grade silicon," *Scientific Reports* **9**, 14814 | 10.1038/s41598-019-51324-4 | A | Si 원료 = **Elkem Silgrain® 라인(수력야금 리칭 공정)의 산업용 배터리급 실리콘** — 조성 Si:흑연:CMC:카본블랙 = **60:15:10:15**(질량비). 전위: 저-밀링 시료 **~0.1 V 뚜렷한 평탄역**, 고-밀링 시료는 **0.3–0.1 V 완만 경사**(나노화 거동). **평균 탈리튬화 전위 ~0.4 V**. 1차 방전/충전 용량 **3801/3117 mAh/g**, **초기 쿨롱효율 82%**. 용량제한 순환(1000 mAh/g, FEC 첨가·CMC/SBR 이중 바인더) 시 **1200 사이클 이상 안정**. **본 축의 "사용자 확정 케이스(D22-3)" 요건에 가장 직접 부합하는 1차 문헌.** |
| 2 | **저-Si 함량(10 wt%) Si/흑연 복합 — 전위 피크 분리·순환 안정성** | Naboka, Yim, Abu-Lebdeh (2021), "Practical Approach to Enhance Compatibility in Silicon/Graphite Composites to Enable High-Capacity Li-Ion Battery Anodes," *ACS Omega* **6**(4), 2644–2654 | 10.1021/acsomega.0c04811 | A | Si **10 wt%** + 흑연/카본Super P/바인더. 리튬화 피크 **~0.2, 0.1, 0.07 V**(흑연 기여), 탈리튬화 **~0.11, 0.16, 0.23 V**(흑연) + Si 별도 피크 — dQ/dV 상 Si·흑연 피크가 **분리 관측**됨(전위 중첩 정도 판단 근거). 개질 복합 **565 mAh/g, 100사이클 95% 유지**(저부하 2.8–3.2 mg/cm²) / 개질 최우수(25EC/gr) **99% 유지 @100사이클**(고부하 6.6 mg/cm², 471 mAh/g급). 미개질 대비 ICE **49.6%→82.9–83.3%** 로 개선. |
| 3 | **산업 폐실리콘 기반 다중스케일 탄소-집적 Si 음극 — 실사용 조건 순환** | Lee, Hong, Kim, Park, Kim, Kang, Kim, Lee, Son, Cho, Kim, Woo, Lee, Kang (2025), "Multiscale Carbon-Integrated Silicon Anode for Stable Cycling Under Practical Lithium-Ion Battery Conditions," *Advanced Energy Materials*, DOI 게재 | 10.1002/aenm.202504250 | B | 서지 Crossref 확인 완료(저자 14인·2025). **산업 폐실리콘(industrial waste silicon)**을 원료로 탄소 구조 통합, 상용 흑연 음극과 병용하는 실사용(practical) 조건 순환 안정성을 목표로 함(제목·초록 상 확인). **주의**: 정량 수치(용량·ICE·사이클수)는 본 세션에서 페이월로 독립 재확인하지 못함 — tier B 로 표기, 향후 원문 대조 필요. |

---

## 축 소결

- **상용급 요건(사용자 확정 D22-3) 충족**: 문헌 1(Andersen 2019)이 원료 단계부터 "industrial battery grade"(Elkem 산업 공정)를 명시한 **가장 직접적인 부합 사례** — 전위 개형·평균 전위·1차 용량·ICE·장기 순환(1200+ 사이클)까지 전 항목 정량 확보.
- **저-Si 함량 비교 자산**: 문헌 2(Naboka 2021)는 Si 10 wt% 로 BLEND_UP.md 축(f_Si 5~30%)과도 접점 — dQ/dV 상 Si·흑연 피크 분리 관측이 R5 "공통-μ 검증"에 직접 참고자료.
- **미완**: 문헌 3 은 서지만 확정, 정량값은 tier B 유지(추가 원문 대조 필요 — R3/R5 소관).

## 탐색 경로 (검증 실패·미확보 — 기록용, 목록 미등재)

- "6500 mAh/g 초고용량 Si-C" 계열(arXiv 프리프린트 경유 발견)은 학술지 정식 게재 여부·상용성 근거가 이번 세션에서 불명확 — Si-C 축이 요구하는 "상용급" 요건에 부합한다고 판단하기엔 근거 부족으로 제외.
- Beattie·Magasinski·Yushin 등 Si-C 복합 고전 계열은 이번 세션에서 별도 WebSearch 를 하지 않음(이미 확보된 3건이 상용급 요건·정량성 면에서 우선순위가 높다고 판단해 시간 배분) — 후속 세션에서 추가 조사 여지 있음(미착수, 실패 아님).

## R5/R6 대응 매핑

**R5** Ch3 Si–C 복합 케이스(사용자 확정, D22-3) 절의 1차 실측 앵커로 문헌 1(Andersen2019)을 대표례로, 문헌 2(Naboka2021)를 저-Si 함량 보조례로 사용 — 전위 개형·평균전위 0.4V·ICE 82%·1200사이클 안정성이 tier-A 초기값. **R6** `BlendedAnodeDQDV` Si 케이스 셋의 Si-C 서브케이스 파라미터(조성비 60:15:10:15, 평균 탈리튬화 전위 0.4V)로 직접 사용 가능.
