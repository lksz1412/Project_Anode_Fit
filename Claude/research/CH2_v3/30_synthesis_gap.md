# Ch2 v3 — 종합·삼각검증·갭·의도 매핑 (Phase 3.1)

> master CORE. 추출카드·정합표 종합. ★사슬(dQ/dV(T) → ∂U/∂T → 가역 발열) 각 고리의 문헌 커버맵 + 4-tier.

## 1. 합의 (다출처 일치 = 확정준함)
- **정전 식**: $\Delta G=-nFE_\eq$, $\Delta S=+nF\,\partial E_\eq/\partial T$, $\Delta H=-nFE_\eq+nFT\,\partial E_\eq/\partial T$, 가역 발열 $\dot Q_\mathrm{rev}=-I\,T\,\partial U/\partial T$. [Bernardi 1985 · Newman · MSMR Part I Eq.27/28 — 삼각]
- **흑연 ΔS(x) 정성·정량**: 저x 양수(configurational)→고x 음수(vibrational), +29 @x=0.08, −5~−16 @x>0.5; stage2→1(x=0.5) 이상. [Allart 2018 full-text · Reynier 2003 · MSMR Part II · Chem.Mater./JPC C 정성 — 삼각]
- **가역열 SOC 의존·부호 가변**: ∂U/∂T 부호가 SOC 따라 바뀌어 흡열/발열 교대. [Standardised 2024 · MSMR · 종설 — 삼각]
- **★Ch1 정합**: Ch1 ΔS_rxn(+29→0→−5→−16) = Allart 전극 ΔS 정량 일치(+29·−16 정확). Ch1 U_j(T) 구조가 ∂U_j/∂T=ΔS_rxn,j/F 를 *이미* 내장. [Phase 2.2]

## 2. ★의도 사슬 커버맵 (각 고리의 문헌 근거)
| 고리 | 내용 | 문헌 근거 | tier |
|---|---|---|---|
| ① | $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ | 정전(Newman·MSMR Eq.27)·Ch1 내장 | 확정준함 |
| ② | 다온도 **dQ/dV** 피팅 → 전이별 $U_j(T)$ → 기울기 → $\Delta S_{\rxn,j}(x)$ | ★*부분 근거*: MSMR 은 OCV(T)/반응별 $dU_j^0/dT$ 추정(직접 선례) · Electrochim.Acta 2019 는 dQ/dV+entropy→부분몰 ΔS(우리와 가장 근접 prototype, 단 식 미확보·dilute 한정) · entropy spectroscopy. **dQ/dV(T) peak-shift 로 ∂U/∂T 직접 추출**의 *명시 선례는 약함* = 본 작업의 기여/공백 | 추정(방법 grounded·정량 선례 부분) |
| ③ | $\Delta S(x)$ → $\dot Q_\mathrm{rev}=-I\,T\,\partial U/\partial T$ | Bernardi · Standardised 2024 · calorimetry 검증 | 확정준함 |
**결론**: 사슬 ①③ 확정, ②가 *핵심 기여 지점*(MSMR 가 OCV(T) 로 하는 것을 Ch1 dQ/dV 모델 다온도 피팅으로 — 선례는 MSMR 가 template, dQ/dV 직접경로는 신규성). 지난 연구의 "미진"이 바로 ② — 이제 MSMR template + Allart 검증값 + Bernardi 로 근거화 가능.

## 3. 논쟁·함정 (정직)
- ★**ΔS_rxn vs ΔS_a 혼동 금지(Q8)**: 반응(평형) 엔트로피 $\Delta S_{\rxn}=F\,\partial U/\partial T$(가역 발열의 원천) ≠ 활성화 엔트로피 $\Delta S_a$(Eyring prefactor, Ch1 꼬리 동역학). MSMR Part I 이 둘을 별개로 다룸. Ch2 는 *반응 엔트로피*만이 가역 발열에 들어감을 명시.
- ★**히스테리시스 하 "가역" 경계(Q6)**: OCV 가 history-dependent(metastable stacking, JPS 2018·JMCA 2021) → 단일 ∂U/∂T 가 경로의존·측정 불확실. 가역 발열은 *평형(또는 충방전 평균) ∂U/∂T* 로 정의하고, 히스/과전압발 entropy production σ≥0 은 *비가역열*로 분리. JPS 2018 가 측정 불확실도 경고(정량 미확보=갭).
- **DFT 신뢰성**: 절대 ΔH 는 interlayer 상호작용 기술 난점(JPC C·arXiv DFT). 정성·분해(config/vib)는 유효, 절대값은 실험 우선.
- **dQ/dV 피팅 함정**: 평활(과평활→폭 편향)·peak 분해·노이즈·저율 준평형 전제. MSMR 가 연속함수·저차 다항으로 과적합 억제 권고.
- **ΔH 기준**: 형성(cumulative) vs 전이별(differential) — 환산 전 등치 금지.

## 4. 공백 (Ch2 초안서 "미확보"로 정직 표기 / 후속 정독 대상)
1. Electrochim.Acta 2019 본문 식(Bragg–Williams 확장)·절대 ΔS/ΔH — 403 미확보. *방법은 grounded, 식은 갭*.
2. Reynier 2003 절대 dE/dT(mV/K)·ΔS(J/mol/K) vs x 곡선 — 부호·정성만.
3. JPS 2018 히스 entropy 불확실도 정량(±, 최적 protocol).
4. Chem.Mater.2015 ΔS_form·455K→298K 환산 정당성.
5. dQ/dV(T)→∂U/∂T 직접경로 정확도 실증(우리 기여 — 후속 실데이터 단계).

## 5. Gate (Phase 3.1)
PASS — 합의/논쟁/공백 분류·★사슬 커버맵(①③ 확정·② 기여지점)·삼각검증·함정(ΔS_rxn vs ΔS_a·히스 가역경계)·4-tier. → Phase 4.1 Ch2 v3 초안.
