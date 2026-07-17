# SI_ENTROPY_UP — Si(·Si 합금) 음극 엔트로피/∂U/∂T 실측 문헌 재조사 (v1.0.22 R4 승급 조사 창, D22-4)

> 스펙 원전 = 마스터 승급 지시 축 3: Si(또는 Si 합금) 음극의 엔트로피/∂U/∂T 실측 — 검색어 변형(entropy profile, entropimetry, thermodynamics of lithiation of silicon, partial molar entropy Li-Si) 포괄 시도. 진짜 없으면 "부재 확증(탐색 경로 기록)"으로 종결 — 이것도 유효한 결과.
> 저비용 창(R4) 원 상태: `comp_R4/SI_ENTROPY.md` = **0건("WebSearch 기반 Si 엔트로피 1차 실측 문헌 없음")** — DIRECTION_SI_LCO_REPORT §2 계보 H 의 "미확보" 판정을 그대로 계승·종결.
> **결론 선반영**: 본 승급 창은 저비용 창의 "부재" 판정을 **뒤집는다** — 검색어를 dV/dT·엔트로피 계수·entropimetry·isothermal microcalorimetry·MSMR 엔트로피/엔탈피·고체 열용량 등으로 확장하자 **6건의 실측/계산 1차 문헌**이 확인됨. "진짜 없으면 부재 확증"의 대우: 있었고, 저비용 창의 검색어 폭이 좁았던 것이 원인.
> **규칙 승계**: 기억 서지 절대 금지·웹 실검증분만·검증 실패 항목은 목록 미등재.
> tier 범례: **A** = 1차 문헌·정량 내용 본 세션에서 독립 확인 · **B** = DOI·서지 확인 완료이나 정량 내용 일부만 접근(추가 대조 필요)

---

## 검증 문헌 표

| # | 특징 | 검증 문헌 | DOI | tier | 대표 수치(원문 확인) |
|---|---|---|---|---|---|
| 1 | **Si-C 음극 엔트로피 계수 — SoC·열화 의존 정량** | Böhm, Zintel, Ganninger, Jäger, Markus, Henriques (2024), "Exploring the Impact of State of Charge and Aging on the Entropy Coefficient of Silicon–Carbon Anodes," *Energies* **17**(22), 5790 | 10.3390/en17225790 | A | 엔트로피 계수(∂U/∂T) **전 구간 음(negative) 부호 유지**: 100% SoH 에서 **−40 ~ −95 μV/K**, 노화 후(71–80% SoH) **−45 ~ −105 μV/K**. SoC 의존: 95%→90% SoC 급락(~−70→−95 μV/K), 45–90% 구간 평탄, ~10% SoC 에서 ~−40 μV/K 로 회복. **흑연 대비 "더 균일"(흑연 특유의 급격한 피크·변동이 없음)** — 흑연 골격 N4/N6(peak 문법)의 Si 대응 재해석(§3 tab:simap N2/N6 판정)에 직접 정합. |
| 2 | **Si 반쪽전지 — 등온 열량측정(isothermal microcalorimetry)으로 가역열(엔트로피) 성분 직접 분리** | Arnot, Allcorn, Harrison (2021), "Effect of Temperature and FEC on Silicon Anode Heat Generation Measured by Isothermal Microcalorimetry," *J. Electrochem. Soc.* **168**(11), 110536 | 10.1149/1945-7111/ac315c | A | C/10 순환에서 총 발열을 **옴열(분극)·가역열(엔트로피)·기생반응열** 3성분으로 분리 — **가역열(엔트로피) 성분이 세 성분 중 가장 작음**(옴열이 지배)을 정량 열량측정으로 직접 확인. FEC 첨가 시 기생반응 엔탈피는 오히려 **증가**하나 저항 성장은 억제. 순수 Si 전극(합금 아님)에서의 **직접 열량측정 기반 엔트로피 성분 분리** — dV/dT 간접법이 아닌 독립 측정 경로. |
| 3 | **NCA/Gr-SiOₓ 완전지 엔트로피 프로파일링 — Si·흑연 성분 분리 서명** | Wojtala, Zülke, Burrell, Nagarathinam, Li, Hoster, Howey, Mercer (2022), "Entropy Profiling for the Diagnosis of NCA/Gr-SiOₓ Li-Ion Battery Health," *J. Electrochem. Soc.* **169**(10), 100527 | 10.1149/1945-7111/ac87d1 | A | 완전지(NCA/Gr-SiOₓ)이나 **엔트로피 프로파일에서 흑연·Si 기여를 성분 분리**: 흑연 성분은 방전 중 엔트로피 변화가 **입자 균열과 연동해 감소**, Si 성분은 순환에 따라 충전 중 엔트로피 변화가 **부피변화와 연동해 증가**. Gr-Si 혼합 전극의 엔트로피 이력(hysteresis)이 순환 열화에 따라 증가 — **BLEND_UP.md 축과 직접 접점**(엔트로피 성분 분리 = f_Si 분해 가능성의 실측 증거). |
| 4 | **MSMR 골격의 반응별 엔트로피·엔탈피 정량 분해 방법론** | Garrick, Koch, Choi, Du, Adeyinka, Staser, Choe (2024), "Quantifying the Entropy and Enthalpy of Insertion Materials for Battery Applications Via the Multi-Species, Multi-Reaction Model," *J. Electrochem. Soc.* **171**(2), 023502 | 10.1149/1945-7111/ad1d27 | B | **주의(과잉귀속 방지)**: 본 논문 자체의 확인된 초록은 **NMC811/흑연 파우치 셀**을 대상으로 하며 Si 는 초록에 명시되지 않음(HTFDA 방법·다기능 열량계로 실측 → MSMR 확장 모델로 반응(gallery site)별 엔트로피 분해). **Si 데이터 직접 제공 아님** — 그러나 기존 원장의 verbrugge_lisi2016(Li-Si MSMR speciation, N9 최강 자산)과 **같은 MSMR 계열**이라, "반응별 엔트로피 분해" 방법론이 Si 다반응 계에도 원리상 이식 가능함을 시사하는 **방법론적 다리**로만 인용(정량값 아님). |
| 5 | **Si 반쪽전지 — 온도 의존 열발생·용량, 저온 이상 엔트로피 신호** | Böhm, Bracht, Kallfa, Markus, Henriques (2025), "Temperature-Dependent Thermal Effects and Capacity Characteristics of Silicon Anodes in Lithium-Ion Batteries," *J. Electrochem. Soc.* **172**(5), 050537 | 10.1149/1945-7111/adda7a | A | **나노-Si 45 wt% 반쪽전지**, 15–60 °C 4개 온도점, 12개 코인셀·초기/25사이클 후 열량측정+ICA. 고온일수록 용량 증가·발열 감소(우호적). **상온 이하에서 Si 특유 열유속 서명과 다른 추가 발열 피크**(탈리튬화 시)가 새로 관측 — 저온 영역에서 엔트로피/열 거동이 상온과 질적으로 달라짐을 시사(정성 신규 발견, 정량 ΔS(T) 표는 원문 대조 필요). |
| 6 | **Li–Si 화합물(고상) 절대 엔트로피·열용량 — 2~873 K** | Thomas, Abdel-Hafiez, Gruber, Hüttl, Seidel, Wolter, Büchner, Kortus, Mertens (2013), "The heat capacity and entropy of lithium silicides over the temperature range from (2 to 873) K," *J. Chem. Thermodynamics* **64**, 205–225 | 10.1016/j.jct.2013.05.018 | B | 서지 Crossref 확인 완료. **주의(성격 상이)**: 이 문헌은 **operando 전기화학 dV/dT 가 아니라 고상 리튬실리사이드 화합물(Li₁₂Si₇ 등)의 단열/시차주사 열량측정**으로 절대 엔트로피 S°(T)·열용량 C_p(T) 를 구함 — N2(평형 참조)의 열역학 앵커로는 유효하나 **"음극 엔트로피 실측"(전지 맥락 dU/dT)과는 측정 맥락이 다름**을 명시. 본문 §1 S1(Wen–Huggins 1981, 고온 상도표)과 같은 계열의 **고상 열역학 보완 자산**으로 위치시킴(정량 재확인은 원문 대조 필요 → tier B). |

---

## 축 소결 — "부재" 판정 기각

**저비용 창(R4)의 "0건 확보" 판정은 기각한다.** 검색어를 (a) "entropy coefficient"(직접 동의어), (b) "isothermal microcalorimetry"(독립 측정경로), (c) "entropy profiling / entropimetry"(완전지 성분분리), (d) "MSMR entropy enthalpy"(방법론), (e) "heat capacity lithium silicides"(고상 열역학)로 확장하자 **6건**(tier A 4·tier B 2)이 확인됨. 특히 문헌 1(Böhm2024)·문헌 2(Arnot2021)는 **Si(-C) 반쪽전지의 직접 엔트로피/가역열 실측**으로 DIRECTION_SI_LCO_REPORT §2 계보 H 가 요구한 "Si 부분몰 엔트로피/∂U/∂T 실측"에 정확히 부합한다.

**부호·크기 요약(문헌 1 기준, tier A)**: Si-C 음극 엔트로피 계수는 **전 SoC 구간 음(-)**, 크기 **40–105 μV/K**(흑연보다 절댓값은 유사~작은 범위이나 SoC 의존 곡선이 흑연보다 평탄) — 흑연 대비 "차이·부호"는 **부호는 SoC 대부분 구간에서 흑연과 같은 음(-)이나 곡선 형태(피크 유무)가 다르다**로 정리 가능(단, 흑연과의 직접 동시 비교 데이터는 문헌 1 초록 요약 수준 — 원문 그래프 대조는 R5 실집행 소관).

## 탐색 경로 (검증 실패·미확보 — 기록용, 목록 미등재)

- Chevrier 등의 "비정질 Si 엔트로피 혼합 예측(1회 부호반전 정성 예측)"은 여러 2차 문헌에서 **반복 인용된 정황은 확인**되나(Böhm2024 논문 계열 인용 패턴), 본 세션에서 **원 계산 논문의 정확한 서지(제목·연도·DOI)를 직접 특정하지 못함** — Chevrier & Dahn 2009(JES 156(6) A454, 이미 원장 chevrier_dahn2009 로 등재됨)과 별개의 논문일 가능성이 있어 **혼동 방지를 위해 미등재**(추가 검증 필요 시 R5/R3 소관).
- "partial molar entropy Li-Si" 정확 문구로 순수 전기화학적 반쪽전지 dV/dT 곡선(조성 함수 S(x) 전 구간)을 보고하는 문헌은 이번 세션에서 **직접 특정하지 못함** — 문헌 1·5(Böhm 계열)가 SoC 함수 엔트로피 계수를 주나 "Si-C"(탄소 포함) 명칭이며 순수 원소 Si 단독 조성함수 S(x) 표는 별도 확인 필요.
- Gemini/기타 고체상태 제일원리 계산 기반 Si 엔트로피 논문(예: DFT 진동 엔트로피)은 검색에서 산발적으로 노출됐으나(예: "Machine Learning for the Prediction of Thermodynamic Properties in Amorphous Silicon") 본 축이 요구하는 "실측"(experimental) 기준에 부합하는지 애매하여 — 계산 논문은 이번 라운드에서 제외(실측 우선 원칙).

## R5/R6 대응 매핑

**R5** Ch3 Si 열특성 소절(신설 시) ∂U/∂T 초기값을 문헌 1(Böhm2024, tier-A, −40~−95 μV/K)·문헌 2(Arnot2021, tier-A, 가역열 최소 성분)로 직접 공급 — 기존 D24("Si 엔트로피 미확보 시 처리방식") 결정 필요성 자체가 **해소**(생략/DFT근사/공백선언 선택지 중 하나를 고를 필요 없이 tier-A 실측 인용 가능). **R6** `entropy_coefficient` 계열 함수의 Si 케이스 파라미터(부호 음·크기 40–105 μV/K 범위)로 시연값 대체 가능.
