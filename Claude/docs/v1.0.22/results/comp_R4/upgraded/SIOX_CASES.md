# SIOX_CASES — SiOₓ 음극 실측 문헌 (v1.0.22 R4 승급 조사 창, D22-4)

> 스펙 원전 = 마스터 승급 지시 축 1: SiOₓ 음극 — 전위 곡선 개형·평균 전위·1차 비가역(Li 실리케이트 형성)·히스테리시스 — 실측 1차 문헌(doi 검증).
> 저비용 창(R4) 원 상태: `comp_R4/SI_CASES.md` 케이스 2 = **0건("WebSearch 검증 대기 중")** — 미확보로 종결.
> **규칙 승계**: 기억 서지 절대 금지·웹 실검증분만·검증 실패 항목은 목록 미등재(탐색 경로만 하단에 기록).
> tier 범례: **A** = 1차 문헌·정량 내용 본 세션에서 독립 확인(WebFetch/Semantic Scholar 초록 또는 WebSearch 직접 인용) · **B** = DOI·서지 Crossref 확인 완료이나 정량 내용은 초록 elided/미접근(제목·주제 계열로만 위치 확인)

---

## 검증 문헌 표

| # | 특징 | 검증 문헌 | DOI | tier | 대표 수치(원문 확인) |
|---|---|---|---|---|---|
| 1 | **SiO 화학구조·리튬 실리케이트 최초 동정(XPS)** | Miyachi, Yamamoto, Kawai, Ohta, Shirakata (2005), "Analysis of SiO Anodes for Lithium-Ion Batteries," *J. Electrochem. Soc.* **152**(10), A2089–A2091 | 10.1149/1.2013210 | A | Cu 박막 위 증착 SiO 를 증착 직후·1차 충전 후·방전 후 3단계 XPS 분석. 완전충전 상태에도 Si 일부가 산화 상태로 잔존 — **리튬 실리케이트가 형성되어 부피변화 완충재 역할**을 함을 최초로 규명(SiOₓ 축의 원류 문헌). |
| 2 | **SiO–탄소 복합 음극 반응기구** | Yamada, Inaba, Ueda, Matsumoto, Iwasaki, Ohzuku (2012), "Reaction Mechanism of 'SiO'-Carbon Composite-Negative Electrode for High-Capacity Lithium-Ion Batteries," *J. Electrochem. Soc.* **159**(10), A1630–A1635 | 10.1149/2.018210jes | B | 서지 Crossref 확인 완료(저자 6인·권호·페이지 확정). **주의**: 초록 필드가 publisher 측에서 elided — 본 세션에서 정량값(생성 전위·상 분율)은 독립 재확인하지 못함. 검색 클러스터 상 Li₄SiO₄·Li₂O 생성 전위 논의의 위치는 확인되나 그 수치를 본 논문에 직접 귀속시키지 않음(과잉 귀속 방지). |
| 3 | **비정질 LiₓSi 경로 확증(operando NMR) · 히스테리시스 저감 기구** | Kitada, Pecher, Magusin, Groh, Weatherup, Grey (2019), "Unraveling the Reaction Mechanisms of SiO Anodes for Li-Ion Batteries by Combining in Situ ⁷Li and ex Situ ⁷Li/²⁹Si Solid-State NMR Spectroscopy," *J. Am. Chem. Soc.* **141**(17), 7014–7027 | 10.1021/jacs.9b01589 | A | **금속성 LiₓSi 상이 x=3.4–3.5 조성에서 비정질 SiO 리튬화 시 형성** — 결정질 Li–Si 상 특유의 히스테리시스 없이 **연속적 비정질 LiₓSi 형성/분해**로 진행(이산 상전이 아님). SiOₓ 히스테리시스가 결정질 Si 대비 저감되는 물리적 근거를 NMR로 직접 제시. |
| 4 | **SiO 용량·용량감쇠 기구·이론용량** | Zhang, Qin, Liu, Liu, Ren, Jansen, Lu (2018), "Capacity Fading Mechanism and Improvement of Cycling Stability of the SiO Anode for Lithium-Ion Batteries," *J. Electrochem. Soc.* **165**(10), A2102–A2107 | 10.1149/2.0431810jes | A | **SiO 이론용량 1710 mAh/g**. 주요 용량손실은 **초기 수 사이클에 집중**되고 이후 완만화 — 입자 내부 계면결함 제거·열처리로 안정성 개선 가능. 순수 Si 대비 SiO 의 상대적 안정성을 확인. |
| 5 | **1차 비가역 정량화(ICE) · 리튬 실리케이트 저감 전략** | Yom, Hwang, Cho, Yoon (2016), "Improvement of irreversible behavior of SiO anodes for lithium ion batteries by a solid state reaction at high temperature," *J. Power Sources* **311**, 159–166 | 10.1016/j.jpowsour.2016.02.025 | A | **미처리 SiO 초기 쿨롱효율(ICE) = 58.52%** — Li 분말과 고온 고상반응 처리 시 **82.12%** 로 개선. 1차 비가역 용량의 정량적 크기(1차 리튬화 시 소비되는 Li 중 ~40% 가 실리케이트/Li₂O 형성에 불가역 소모)를 직접 수치화한 문헌. |

---

## 축 소결

- **전위 곡선 개형**: 문헌 1·3 이 정성적으로 확인 — 결정질 Si 의 이산 상전이(Li₁₅Si₄ 등)와 달리 SiOₓ 는 **비정질 LiₓSi 의 연속 형성/분해**(문헌 3, NMR 직접 관측)로 경사 전위 특성이 더 강화됨.
- **1차 비가역(리튬 실리케이트 형성)**: 문헌 1(정성·기구)·5(정량, ICE 58.52%→82.12%)가 상보적으로 확보 — SI_CASES.md 원 상태의 "0건"을 명확히 해소.
- **히스테리시스**: 문헌 3 이 유일한 직접 증거(정성 — "결정질 특유 히스테리시스 없음"). **절대 mV 수치는 본 세션에서 미확보** — 아래 탐색 경로 참조.
- **평균 전위**: 개별 논문에서 명시적 평균전위 수치(V)를 독립 재확인하지 못함 — 문헌 4 는 이론용량만 확정. **정직 공백으로 남김**(아래 탐색 경로 참조).

## 탐색 경로 (검증 실패·미확보 — 기록용, 목록 미등재)

- "SiOₓ 평균 전위 0.2–0.4 V" 류 수치는 다수 2차 리뷰(예: *J. Alloys Compd.* 계열 리뷰)에서 반복 언급되나, 본 세션에서 해당 특정 리뷰 논문의 DOI 를 Crossref 로 3회 시도(제목 일치 검색·ScienceDirect PII 역추적)했으나 **정확한 DOI 확정 실패**(ScienceDirect 직접 fetch 403·Crossref bibliographic query 무매치) — 리뷰 자체는 미등재.
- SiOₓ 히스테리시스의 **절대 mV 크기**를 독립 문헌(순수 SiOₓ, 블렌드 아님)으로 특정하는 시도 — 검색된 후보(예: SiOₓ/graphite 블렌드 딜라토메트리 계열)는 모두 **블렌드 맥락**이라 BLEND_UP.md 로 귀속(교차 오염 방지). 순수 SiOₓ 단독 히스테리시스 mV 수치의 1차 문헌은 이번 세션에서 미확보.
- ScienceDirect·IOPscience 초록 페이지는 이번 세션에서 대부분 403(직접 차단) — Crossref API·Semantic Scholar API 경유로 우회했으며, 우회 불가 항목(문헌 2 정량값 등)은 tier B 로 표기하고 과잉 귀속을 피함.

## R5/R6 대응 매핑

**R5** Ch3 SiOₓ 케이스 절의 전위 개형(문헌 1·3)·1차 비가역 초기값(문헌 5, ICE 58.5%→tier-A 시연값)·용량(문헌 4, 1710 mAh/g)을 공급 — 히스테리시스는 "결정질 대비 저감" 정성 서술까지만(절대값 tier-C 유지 또는 공백 선언). **R6** `BlendedAnodeDQDV` Si 케이스 셋의 SiOₓ 서브케이스 파라미터(이론용량 1710 mAh/g·ICE 초기값)로 직접 사용 가능.
