# BLEND_UP — 흑연/Si 블렌드(Si 5~30%) dQ/dV·전위 프로파일 실측·모델링 문헌 재조사 (v1.0.22 R4 승급 조사 창, D22-4)

> 스펙 원전 = 마스터 승급 지시 축 4: 흑연/Si 블렌드(Si 5~30%) dQ/dV·전위 프로파일 실측 또는 모델링 문헌(blended electrode model, composite anode graphite silicon dQ/dV) — R5 공통-μ 대정준·R6 f_Si 토글이 쓸 정렬 데이터.
> 저비용 창(R4) 원 상태: `comp_R4/BLEND_ALIGN.md` = **0건("WebSearch 기반 Gr-Si 블렌드 실측 dQ/dV 없음")** — D25 사용자 결정(시연/데이터/공백 모드) 대기로 종결.
> **결론 선반영**: 본 승급 창은 저비용 창의 "부재" 판정을 **뒤집는다** — 이론(MSMR 확장)·실측(f_Si 스윕 dQ/dV)·상용 스케일(150 Ah 프리즘 셀) 3방향에서 **8건**이 확인됨. D25 는 "(C) 공백 선언"이 아니라 "(B) 데이터 모드"를 뒷받침할 근거가 확보됨.
> **규칙 승계**: 기억 서지 절대 금지·웹 실검증분만·검증 실패 항목은 목록 미등재.
> tier 범례: **A** = 1차 문헌·정량 내용 본 세션에서 독립 확인 · **B** = DOI·서지 확인 완료이나 정량 내용 일부만 접근

---

## 검증 문헌 표 — (가) 이론·모델링 (R5 공통-μ 대정준의 직접 다리)

| # | 특징 | 검증 문헌 | DOI | tier | 대표 수치(원문 확인) |
|---|---|---|---|---|---|
| 1 | **SiO/흑연 블렌드 — MSMR 골격 기반 축소모델(perturbation theory), Verbrugge 동일 저자 계보** | Tu, Dao, Verbrugge, Koch (2024), "Mathematical Model for a Lithium-Ion Battery with a SiO/Graphite Blended Electrode Based on a Reduced Order Model Derived Using Perturbation Theory," *J. Electrochem. Soc.* **171**(5), 050539 | 10.1149/1945-7111/ad4823 | A | **두 host(SiO·흑연)를 multi-site multi-reaction(MSMR) 골격으로 명시 정식화**. 각 host 마다 별도 비선형 편미분방정식(비가역 열역학 — 화학퍼텐셜 구배가 구동력)을 세우고, 단일입자모형(SPM)을 leading order 로 삼아 섭동으로 보정하는 축소모형(ROM). **저자 Mark W. Verbrugge = 기존 원장 verbrugge_lisi2016/2015(N9 전하보존 Si 실증 앵커)와 동일 인물** — 흑연·LCO·Si 단일 host 골격을 블렌드로 일반화하는 **가장 직접적인 이론 다리**. |
| 2 | **Si/흑연 복합 연속체 모델 — OCV 곡선 차이에 따른 반응전류 host 간 전환** | Ai, Kirkaldy, Jiang, Offer, Wang, Wu (2022), "A composite electrode model for lithium-ion batteries with silicon/graphite negative electrodes," *J. Power Sources* **527**, 231142 | 10.1016/j.jpowsour.2022.231142 | A | 연속체 수준 모델이 **전압 히스테리시스를 재현**하고 흑연·Si 간 상호작용을 시연. **높은 SoC 에서는 흑연이 반응전류의 대부분을 담당**하다가, **깊은 방전(low SoC)으로 갈수록 급격히 Si 상으로 전환** — 이는 **서로 다른 OCV 곡선·질량분율·교환전류밀도**의 결과. 고율에서는 관통-두께 방향 불균일(집전체측 Si 반응 집중 vs 분리막측 흑연 집중)도 시연. **"공통 전위에서 두 host 가 정말 동시반응하는가"(R5 이론의 핵심 전제)에 대한 정량적 반례/조건부 답** — 실제로는 SoC 구간별로 우세 host 가 전환되며 완전 동시반응이 아님을 모델이 보임. |

## 검증 문헌 표 — (나) 실측 dQ/dV·전위 정렬 (f_Si 5~30% 스윕)

| # | 특징 | 검증 문헌 | DOI | tier | 대표 수치(원문 확인) |
|---|---|---|---|---|---|
| 3 | **Si 5–20 wt% 상용 흑연 블렌드 — 용량·ICE·f_Si 최적점** | Gautam, Mishra, Bhawana, Kalwar, Dwivedi, Yadav, Mitra (2024), "Relationship between Silicon Percentage in Graphite Anode to Achieve High-Energy-Density Lithium-Ion Batteries," *ACS Appl. Mater. Interfaces* **16**(35), 45809–45820 | 10.1021/acsami.4c10178 | A | **상용 흑연에 Si 5–20 wt%** 스윕. Si 10%→15%(Si15Gr75) 로 늘리면 1차 리튬화/탈리튬화 용량이 각 **+16.8%/+16.0%** 증가. **Si15Gr75 ICE ≈ 82.9%**(순수 흑연과 거의 동등) — **f_Si 최적점**으로 제시. 0.5C 에서 **215사이클 후 용량 60% 유지**. 상용 NMC622 완전지에서 0.1–0.5C 전 구간 성능 확인. **본 브리프의 f_Si 5~30% 범위에 정확히 부합하는 스윕 실측.** |
| 4 | **Si 0–20 wt% 블렌드 — 두께변화(딜라토메트리)·용량손실 상관** | Moyassari, Roth, Kücher, Chang, Hou, Spingler, Jossen (2022), "The Role of Silicon in Silicon-Graphite Composite Electrodes Regarding Specific Capacity, Cycle Stability, and Expansion," *J. Electrochem. Soc.* **169**(1), 010504 | 10.1149/1945-7111/ac4545 | A | Si **0–20 wt%** 스윕, in-situ 딜라토메트리 + 코인셀 전기화학 동시 측정. 초기 두께변화는 Si 함량과 상관되나 **순환 중 안정화**. **Si 함량과 용량손실은 상관되나, 두께변화와 용량손실률 사이엔 뚜렷한 상관 없음**(구분되는 두 열화축) — R5 의 "용량 배분의 f_Si 의존" 요구에 직접 실측 정합. |
| 5 | **Si 30 wt% 고함량 블렌드 — decoupled blend cell 로 Si·흑연 기여 분리** | Chatzogiannakis, Ghilescu, Giannadaki, Cabello, Casas-Cabanas, Palacín (2025), "Decoupling Silicon and Graphite Contribution in High-Silicon Content Composite Electrodes," *Batteries & Supercaps* **8**(10), e202500104 | 10.1002/batt.202500104 | A | **Si 30 wt%**(브리프 상한) 블렌드를 "decoupled blend cell" 기법으로 분리 측정 — **혼합 전극 거동이 두 성분의 단순합이 아님(비가산적)**을 확인. **탈리튬화 시 Si·흑연 간 유효 C-rate 격차가 특히 큼** — 공통-μ 가정의 "이상적 동시반응"과의 편차를 정량 시사. 저-Si 함량 근사용 Si/Gr–Gr 대안 셀 구성도 병행 제시. |
| 6 | **SiOₓ/흑연 블렌드 — SiOₓ 분율에 선형 비례하는 히스테리시스 에너지손실** | Zhan, Jin, Stapf, Meyer, Birke, Fill (2026), "Unraveling the vertical expansion and hysteresis in SiOx/graphite composite electrodes via in-situ dilatometry and cracking origins via X-ray diffraction and scanning electron microscopy," *J. Energy Storage* **154**, 121227 | 10.1016/j.est.2026.121227 | A | 활물질 총 로딩 고정·SiOₓ 분율만 가변, C/20 딜라토메트리 + DV/IC 분석. **SiOₓ 함량에 거의 선형 비례하는 두께변화**, **히스테리시스 유발 에너지손실도 SiOₓ 함량에 선형 비례**. **"겹치는 리튬화 전위(overlapping lithiation potentials)"에서 SiOₓ–흑연 계면에 양방향 Li⁺ 확산이 균열을 유발** — R5 공통-μ 가정의 물리적 근거(전위 중첩 구간 존재)와 그 대가(계면 균열)를 동시에 실측 제시. |
| 7 | **150 Ah 상용 각형 셀 — SiO/흑연 복합 음극 (탈)리튬화 불균일** | Zhang, Qian, Shi, Zhao, Zhang, Qi, Wang, Lu (2024), "Unveiling the (de)lithiation heterogeneity of SiO/Graphite composite anodes in a 150 Ah high-energy-density Li-ion prismatic cell," *J. Power Sources* **611**, 234754 | 10.1016/j.jpowsour.2024.234754 | B | 서지 Crossref 확인 완료(저자 8인). **상용 규격(150 Ah 각형 고에너지밀도 셀)**의 SiO/흑연 복합 음극에서 (탈)리튬화 불균일을 규명(제목 확인) — **상용 스케일 실증**으로 R5/R6 의 "회사 제출" 지향과 접점 큼. **주의**: 초록 필드 elided, 정량 수치는 본 세션에서 독립 재확인 못함 — tier B, 원문 대조 필요. |
| 8 | **Si-흑연 블렌드 전극의 엔트로피 해석 — 성분별 신호 분리(SI_ENTROPY_UP 축과 교차)** | Mertin, Wycisk, Richter, Oldenburger, Hofmann, Luetje, Manz, Luu, Wieck, Birke (2023), "Interpreting the entropy of silicon–graphite blended electrodes," *J. Energy Storage* **64**, 107118 | 10.1016/j.est.2023.107118 | B | 서지 Crossref 확인 완료(저자 10인). 제목 상 Si-흑연 블렌드 전극의 엔트로피(∂U/∂T) 신호를 성분별로 해석 — SI_ENTROPY_UP.md 문헌 3(Wojtala2022, NCA/Gr-SiOₓ 엔트로피 성분분리)과 같은 문제의식. **주의**: 초록 elided, 정량 수치 미확보 — tier B. **엔트로피 축과 블렌드 축의 교차 자산**으로 양쪽에 각주 필요. |

---

## 축 소결 — "부재" 판정 기각, D25 재검토 근거

**저비용 창(R4)의 "0건 확보" 판정은 기각한다.** 8건(tier A 6·tier B 2) 확보 — 이론 2건(MSMR 확장 ROM·연속체 반응전환 모델)·실측 f_Si 스윕 3건(5–30 wt% 전 구간 커버)·SiOₓ 블렌드 히스테리시스 1건·상용 스케일 1건·엔트로피 교차 1건.

**공통-μ 가정에 대한 정직한 평가(R5 착수 판단에 중요)**:
- **부분 지지**: 문헌 6(Zhan2026)이 "겹치는 리튬화 전위(overlapping lithiation potentials)"를 명시적으로 실측 확인 — 두 host 가 공유하는 전위 구간이 실재함.
- **동시에 한계도 실측됨**: 문헌 2(Ai2022 모델)·문헌 5(Chatzogiannakis2025 실측) 모두 **SoC 구간별로 우세 반응 host 가 전환**되고 **혼합 거동이 두 성분 단순합이 아님(비가산적)**을 보임 — 순수 공통-μ 동시반응 가정은 **1차 근사이며 실측과 정성적 편차가 있음**을 R5 저작 시 명시해야 함(GS 계열 정직 공백 후보).
- **f_Si 스윕 초기값**: 문헌 3(Gautam2024, 5–20%)·문헌 4(Moyassari2022, 0–20%)·문헌 5(Chatzogiannakis2025, 30%)를 합치면 **브리프가 요구한 f_Si 0~30% 전 구간**이 실측으로 커버됨.

## 탐색 경로 (검증 실패·미확보 — 기록용, 목록 미등재)

- "그림 5본"급 dQ/dV overlay(흑연 단독·Si 단독·블렌드 f_Si=10/20/30% 를 한 그래프에 겹친 형태)를 **그대로 게재한 단일 문헌**은 이번 세션에서 특정하지 못함 — 위 문헌들이 각기 다른 측면(용량·두께·엔트로피·모델)을 다루므로, R5 저작 시 **복수 문헌의 수치를 조합**해 재구성해야 함(단일 문헌 인용으로 그림을 그리면 과잉귀속).
- 산업계(Tesla·CATL·BYD 등) 블렌드 제형 관련 자료는 BRIEF_R4/BLEND_ALIGN.md 원 조사에서도 "학술지 미등재·접근 불가"로 판단됐고, 본 승급 창에서도 재시도하지 않음(우선순위상 학술 1차 문헌을 우선 확보).
- 순수 원소 Si(SiOₓ 아님) + 흑연 블렌드의 dQ/dV 실측(문헌 2·3·4·5 는 각각 SiO 또는 상용 Si 계열 — "원소 Si 나노입자 + 흑연" 조합만 특정한 문헌)은 이번 세션에서 별도로 분리 확인하지 않음 — 문헌 3(Gautam2024)이 가장 근접(Si 자체, SiOₓ 아님)하나 원료 Si 의 형태(나노/마이크로) 명시는 재확인 필요.

## R5/R6 대응 매핑

**R5** "공통-μ 대정준" 이론 절의 서론 다리로 문헌 1(Tu–Verbrugge2024, MSMR ROM — 동일 저자계보 이론적 연속성)을 앵커로, 실측 f_Si 스윕 초기값으로 문헌 3·4·5(5/10/15/20/30 wt% 커버)를 사용 — 단 문헌 2·5·6 이 보이는 "비가산적·SoC별 host 전환" 실측 편차를 **GS 계열 정직 공백**(공통-μ = 1차 근사, 완전 동시반응 아님)으로 명시할 것을 권고. **R6** `BlendedAnodeDQDV(f_Si, si_case)` 게이트 검증(f_Si=0 bit-exact 이후 f_Si 스윕 연속성)의 대조 데이터로 문헌 3·4·5 의 f_Si-용량 곡선을 tier-A 초기값으로 직접 사용 가능.
