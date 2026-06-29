# allart2018_potentiometric_model

**저자·연도·venue·DOI**: D. Allart, M. Montaru, H. Gualous, "Model of Lithium Intercalation into Graphite by Potentiometric Analysis with Equilibrium and Entropy Change Curves of Graphite Electrode," *J. Electrochem. Soc.* 2018. DOI 10.1149/2.1251802jes.

**축**: A1 (엔트로피 계수 측정·흑연 프로파일) — ★전극분리 ΔS(x) 정량값 + 히스테리시스.

## 핵심 방법
graphite 전극 potentiometric 측정으로 **평형전위 곡선 + 엔트로피 변화 곡선**을 충·방전 모두에서 측정. dE_OCV/dT 에서 ΔS(x) 산출, region II 의 큰 히스테리시스를 staging 모델(혼합 stacking LiC24)로 해석.

## 지배식 (verbatim 기호)
- **ΔS = nF·(∂E_OCV/∂T)**, "the derivative dE_OCV/dT is directly proportional to the entropy variation." (+부호, n=전자수, F=Faraday. MSMR Part I Eq.27 와 정합.)

## 정량값 (graphite 전극, 0–40°C 5°C 스텝, C/10, 20°C 기준)
- Region IV (0.08 ≤ x ≤ 0.17): **ΔS = +29 J/mol/K @ x=0.08** (LiC72 dilute, 양수 peak — Reynier 저-x 양 ΔS·MSMR +3~4 mV/K 와 정합).
- Region II (0.25 ≤ x ≤ 0.5): ΔS ≈ −15 ~ 0 J/mol/K, **큰 히스테리시스**.
- Region I (x > 0.5): ΔS ≈ −5 ~ −16 J/mol/K (LiC6↔LiC12 전이).
- 부호반전: 저-x 양(+29)→고-x 음(−) = Reynier x≈0.25 부호반전과 정합.

## 히스테리시스
- "high hysteresis in 0.1 ≤ x ≤ 0.3" (≈region II): 충/방전 엔트로피 시그니처 상이 → 인터칼/디인터칼 시 Li 배열 compactness 차이.
- staging 모델: 혼합 stacking **LiC24** — 리튬화 시 stage 4–2(주로 stage4), 탈리튬화 시 stage 2–4(주로 stage2). stage 3 미관측·LiC18(x=0.33)/LiC27(x=0.22) 형성 부정, LiC24 가능성 제시.

## 프로토콜
- 온도 사이클 0–40°C, 5°C 스텝, 각 30분. 2% SOC 마다 측정(Δx≈0.012). 평형기준 dE_OCV/dt ≤ 0.1 mV/h. C/10.

## 타당·한계
- 타당: **전극 단위 ΔS(x) 절대 수치(J/mol/K)** 제공(우리에 직접 유용), 충·방전 분리, region 별 분해, 평형기준 명시.
- 한계: region II 히스테리시스로 ΔS 측정 자체에 경로의존 불확실성(→ JPS 2018 hysteresis 카드 연결); staging 모델은 제안(LiC24)으로 논쟁 여지; coin/단셀.

## 우리 의도 관련성
- **정량 anchor #1(전극 ΔS in J/mol/K)**: 우리 다온도 dQ/dV → ∂U_j/∂T=ΔS_j/F 가 재현해야 할 region 별 ΔS 절대값(+29@저x, −5~−16@고x). Bernardi 가역항에 직접 대입 스케일.
- MSMR Part I 이 흑연 6갤러리 reference 로 본 논문(Allart) 사용 → 우리 MSMR 적합의 ground-truth 후보.
- 히스테리시스 region II = 우리 가역/비가역 경계(Q6) 직접 데이터.

## 정독 범위
- **full-text(IOP HTML 본문, WebFetch 구조화 추출)** — 식·region별 ΔS 값·히스테리시스·staging 모델·protocol 본문 확보. 단 region 경계 x값·부호는 추출 판독이라 정밀 그래프값은 master 원도 확인 권장.

## tier
- 식(ΔS=nF dE/dT)·protocol·히스테리시스 존재: **확정에 준함**(IOP 본문).
- 정량값(+29, −5~−16 J/mol/K, region 경계): **확정에 준함**(본문 추출) — 정밀 자릿수·region 경계는 master 원도/표 확인 권장(추출 판독).

## Decision-queue
1. region 별 ΔS 절대값·x 경계 정밀화 — master 원논문 그림/표 직접.
2. LiC24 staging 모델을 우리 Ch1 전이 정의와 어떻게 매핑할지 — master(Ch1 대조 영역).
3. region II 히스테리시스 ΔS 불확실성 정량 — JPS 2018 hysteresis 카드와 통합.
