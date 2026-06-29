# msmr_partII_entropy_2024

**저자·연도·venue·DOI**: "MSMR Temperature Dependence Part II: Entropy Coefficient for MCMB Graphite," *J. Electrochem. Soc.* 2024. DOI 10.1149/1945-7111/ad70d9.

**축**: A5 (파라미터 추정·MSMR) — 우리 다전이 dQ/dV 피팅에 **가장 근접한 방법론**.

## 핵심 방법
MSMR(Multi-Species Multi-Reaction) 프레임워크로 흑연 평형전위를 다수 갤러리(반응 j)의 합으로 표현하고, **각 반응의 표준전위 U_j⁰(및 X_j, ω_j)의 온도 의존성**으로 엔트로피 계수 ∂U/∂T 를 파라미터화. 5개 갤러리(j=1..5)로 MCMB 흑연 적합. C/50 저속 OCV + 3-step potentiometric 엔트로피 측정으로 검증.

## 지배식 (verbatim 기호)
- 총 리튬화(Eq. A·6): x = Σ_j X_j · x_j, with
  x_j = (1+ω_j)·exp[(U−U_j⁰)F/RT] / { 1 + (1+ω_j)·exp[(U−U_j⁰)F/RT] }
- 미분전압/용량(Eq. A·7): dQ/dU = Σ_j (X_j F/RT)·x_j(1−x_j)·(…)  → NDVS(정규화 미분전압) peak = 개별 반응 식별. **= 우리 dQ/dV 다전이 peak 의 모델 등가물.**
- 온도 의존(Eq.5): f(T)=A T⁴+B T³+C T²+E; (Eq.6) df/dT=4A T³+3B T²+2C T. 각 파라미터 U_j⁰(T),X_j(T),ω_j(T)에 적용.
- 엔트로피 계수 정의: "the temperature derivative of the equilibrium potential of the active material" = ∂U/∂T. 반응별 기여 ∂U_j⁰/∂T.

## 정량값 (MCMB graphite, 15–35°C, C/50)
- 전위 엔트로피 계수 ∂U/∂T(potentiometric, Fig.1):
  - 저-SOC(~0.08 lithiation): **+3 ~ +4 mV/K (양수 peak)**.
  - ~0.2 SOC 부근: **양→음 전이**(부호 바뀜).
  - ~0.6 SOC: 뚜렷한 전이; 1.0(완전리튬화) 향해 약간 감소.
- 반응별 ∂U_j⁰/∂T @25°C (Table IV):
  - j1 = +1.388 mV/K, j2 = +0.011, j3 = −0.142, j4 = −0.218, j5 = −0.015 mV/K.
- 적합: 온도별(15,20,25,30,35°C) MSMR 파라미터를 OCV-vs-SOC 오차 최소화로 추정 후 다항 온도함수 적합.

## 타당·한계
- 타당: 우리 의도(다전이별 ∂U_j/∂T 분리)와 방법 동형. NDVS=dQ/dV 등가, 반응별 엔트로피 계수 직접 산출.
- 한계(저자 명시): "흑연은 시뮬레이션 가장 어려운 재료 중 하나"; staging 비평활성을 작은 ω_j(가파른 plateau)로 매끄럽게 못 잡음 → 엔트로피 계수 근사에 **진동(oscillation)** 발생, "model-based virtual engineering 엔 불충분"할 수 있음. 저속 OCV 만으론 정확도 부족. ~52% SOC wiggle(데이터 3점), >70% SOC slope 불일치(예측 증가 vs 측정 감소, 평균은 일치), 60% 전이 위치 약간 어긋남. 권고: ω_j 큰(부드러운 전이) 재료에서 더 robust.

## 우리 의도 관련성
- **핵심 anchor**: dQ/dV(=dQ/dU) 다전이 peak ↔ MSMR 반응 j ↔ 반응별 엔트로피 계수 ∂U_j⁰/∂T 의 **완성된 사슬을 흑연에 대해 실증**. 우리는 동일 구조로 다온도 dQ/dV 피팅 → ∂U_j/∂T=ΔS_rxn,j/F → 가역발열을 구성 가능.
- 정량적 sanity check: 저-SOC +3~4 mV/K 양수, ~0.2 SOC 부호반전 = Reynier 2003 와 정성 일치(교차검증 가능).
- 한계가 곧 우리 주의점: 가파른 staging 전이를 작은 ω 로 표현 시 엔트로피 진동 → 피팅 정규화·검증 필요.

## 정독 범위
- **full-text(IOP HTML 본문, WebFetch 구조화 추출)** — 식(A·6,A·7,5,6)·Table IV 반응별 값·Fig.1 정성·한계 모두 본문 확보.

## tier
- 식·방법·한계: **확정에 준함**(IOP 본문).
- 정량값(±3~4 mV/K, 반응별 dU_j⁰/dT): **확정에 준함**(Table IV/Fig.1 본문) — 단 Fig.1 peak 값(+3~4 mV/K)은 추출 판독값이라 정밀 자릿수는 master 원도 확인 권장.

## Decision-queue
1. Fig.1 의 저-SOC +3~4 mV/K 정확값·전이 SOC 위치 — master 원논문 그래프/표로 정밀화.
2. 우리 흑연 dQ/dV 피팅에 MSMR 반응 수(여기 5개)를 그대로 쓸지, Ch1 전이 정의와 매핑할지 — master 결정(Ch1 대조는 master 영역).
3. Part I(ad1d27)의 일반 ΔS·ΔH 정량법과 본 Part II 흑연 적용의 정합 — 별도 카드와 대조.
