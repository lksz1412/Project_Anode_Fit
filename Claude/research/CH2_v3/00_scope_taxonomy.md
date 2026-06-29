# Ch2 v3 — 조사 범위·연구질문·6축 택소노미·검색전략 (Phase 0.1)

> plan = `Claude/plans/2026-06-30-ch2-reversible-heat-entropy-survey-plan.md`. ★백지(v2 미참고)·Ch1 v8-11 토대. master 직접 작성. 본 문서가 Phase 1 수집의 기준.

## 0. 목표 한 줄
Ch1(흑연 음극 dQ/dV forward 모델)의 평형 전위 $U_j(T)$ 로부터 **가역 발열·엔트로피 계수 ∂U/∂T·ΔS(x)** 를 정의·정량·추정하는 경로를, 1차 문헌으로 백지부터 근거화하고 Ch2 v3 초안의 토대를 만든다.

## 1. 연구질문 (Q1–Q8 — Phase 2~3 가 출처와 함께 답)
- **Q1 (측정 프로파일)**: 흑연 음극의 엔트로피 계수 $\partial U/\partial T(x)$ 와 부분몰 엔트로피 $\Delta S(x)$ 의 *측정된* 프로파일·범위·불확도·온도구간은? staging 과의 대응?
- **Q2 (staging 정량)**: stage 전이별(4→3→2L→2→1) 형성 엔탈피 $\Delta H$·엔트로피 $\Delta S$ 의 정량값·측정조건(전기화학 vs calorimetry vs DFT)·상호 일관성?
- **Q3 (가역 발열 정전)**: 전지 가역(엔트로피) 발열의 정의·Bernardi energy balance($\dot Q=I(U-V)-IT\,\partial U/\partial T$)·calorimetry 검증·부호 규약(흡열/발열)?
- **Q4 (추정 경로)**: 다온도 $dQ/dV$ (또는 OCV(T)) 로부터 $\partial U/\partial T$ / $\Delta S(x)$ 를 추출한 *실증 선례*·정확도·회귀/식별 방법(MSMR·system-ID)·함정(평활·peak 분해·노이즈)?
- **Q5 (엔트로피 분해)**: configurational(저x 양수) ↔ vibrational(고x 음수) 엔트로피 기여의 물리·모델식·문헌 근거?
- **Q6 (가역/비가역 경계)**: 히스테리시스·경로의존(우리 Ch1 의 분기·꼬리) 하에서 "가역 발열"의 정의 경계는? entropy production $\sigma\ge0$(비가역열)과의 분리?
- **Q7 (Ch1 정합)**: Ch1 `GRAPHITE_STAGING_LIT`(ΔH_rxn −11.7~−13 kJ/mol, ΔS_rxn +29~−16 J/mol/K, U 0.085~0.21 V)이 문헌값과 정합하는가? 단위·기준(per mol Li vs per transition vs per F) 정규화 후 부호·규모?
- **Q8 (개념 혼동 방지)**: 반응 엔트로피 $\Delta S_{\rxn}$(평형 ∂U/∂T) vs 활성화 엔트로피 $\Delta S_a$(Eyring prefactor 온도의존, Ch1 꼬리) 의 구분 — 문헌이 어떻게 다루나?

## 2. 6축 source taxonomy
| 축 | 범위 | 핵심 키워드 |
|---|---|---|
| **A1 엔트로피 계수 측정** | potentiometric·dynamic·calorimetric ∂U/∂T 측정법·흑연 프로파일 | entropy coefficient, dU/dT, potentiometric, partial molar entropy, LixC6 |
| **A2 가역 발열·열모델** | Bernardi balance·reversible/irreversible heat·calorimetry·전기-열 모델 | Bernardi heat generation, reversible entropic heat, calorimetry, dU/dT |
| **A3 ICA/dQ-dV 열역학** | dQ/dV peak↔상전이·부분몰 열역학·물리기반 occupation 모델 | incremental capacity, dQ/dV, phase transition entropy, staging |
| **A4 Li-graphite staging 열역학** | 실험(calorimetry·전기화학)·DFT 형성 ΔH/ΔS·상도 | LiC6 LiC12 enthalpy entropy, staging, DFT phase diagram, intercalation |
| **A5 파라미터 추정** | OCV(T) 회귀·MSMR·system-ID·다온도 피팅 | MSMR, entropy coefficient estimation, system identification, OCV temperature |
| **A6 교과서·리뷰 정전** | 전기화학 열역학 정전·리뷰 | Newman Electrochemical Systems, electrochemical thermodynamics, Huggins |

## 3. 검색 전략
- **DB**: Google Scholar·CrossRef·arXiv·publisher(IOP/JES·Elsevier·ACS·RSC·Wiley)·교과서(정전 확인).
- **쿼리**: 축별 키워드 × {graphite/anode, Li, entropy/heat, measurement/fitting}. 리뷰 우선 진입 → 1차 출처 추적(snowball: 인용·피인용).
- **포함**: 흑연 음극·Li intercalation·가역 발열/엔트로피 계수/∂U∂T·staging 열역학·추정 방법.
- **제외**: 무관 화학(타 음극·전고체·금속 Li 외)·순수 degradation only(열역학 무관)·비-peer 자료(블로그 등은 진입점만, 인용 X).
- **우선순위**: 1차 peer-review > 권위 리뷰 > 교과서 > preprint(arXiv, tier 표시) > 2차.

## 4. seed 문헌(2026-06-30 검색·*존재* 확인 — 정독·확장 대상, 아직 조사 결과 아님)
- A1/A3: Reynier&Yazami JPS 2003(S0378775303002854) · Potentiometric model JES 2018(10.1149/2.1251802jes) · JPS 2005 anomalies(S0378775305007500) · Entropy Profiles review(PMC12025376).
- A2: Standardised Potentiometric reversible heat JES 2024(10.1149/1945-7111/ad4918) · Reversible heat absorption arXiv 2107.00625 · Bernardi 1985(원전 확인 대상).
- A3: Transitions of Li occupation Electrochim.Acta 2019(S0013468619316457) · Differential Analysis Chem.Mater.2022(acs.chemmater.2c01976).
- A4: LiC6/LiC12 calorimetry Chem.Mater.2015(acs.chemmater.5b00235) · DFT vib+config JPC C 2021(acs.jpcc.1c08992) · DFT phase diagram arXiv 1607.05658.
- A5: MSMR entropy coeff JES 2024(10.1149/1945-7111/ad70d9) · System-ID JES 2025(10.1149/1945-7111/adfe1f) · Unifying Thermodynamics arXiv 2507.10677.
- A6: Newman&Thomas-Alyea *Electrochemical Systems*(정전).

## 5. Gate (Phase 0.1)
질문 8 · 6축 · 쿼리/기준 · seed 확정. → Phase 1.1(수집·선별, master + 서브1 순차).
