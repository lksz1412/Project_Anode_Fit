# standardised_potentiometric_2024

**저자·연도·venue·DOI**: "A Standardised Potentiometric Method for the Effective Parameterisation of Reversible Heating in a Lithium-Ion Cell," *J. Electrochem. Soc.* 2024. DOI 10.1149/1945-7111/ad4918. (셀: LG Chem M50LT, NMC/graphite-SiO_y 21700.)

**축**: A2 (가역 발열·측정 표준 protocol).

## 핵심 방법
가역 발열 파라미터(엔트로피 계수 ∂U/∂T)를 SOC 전 구간에서 효율적으로 측정하는 **표준 potentiometric protocol**("T35-T0" 법) 제시. 큰 온도 스텝(ΔT=35°C, 35→0°C 하강)을 써서 ΔU 신호를 키우고 상대 불확도를 낮춤. 전통법 >60일 → 7.4일로 단축.

## 지배식 (verbatim 기호)
- 가역 발열: **Q̇_rev = −I·T·(∂U/∂T)** (I>0 방전; ∂U/∂T<0 ⇒ Q̇_rev>0 발열). ← Bernardi 형태 동일.
- 엔트로피 계수↔ΔS: 추출본은 **∂U/∂T = −ΔS/(nF)** 로 출력(Gibbs–Helmholtz). ※부호 주의: 표준 정의(dE_eq/dT=+ΔS/nF)와 상충 — 추출 부호 오류 의심, Decision-queue. n=전자수, F=96485 C/mol, ΔS in J/mol/K.

## 정량값 (셀=full NMC/graphite-SiO_y, 전극분리값 아님)
- 0–20% SOC: |∂U/∂T| ~ 0.3–0.5 mV/K (최대 절댓값 구간; graphite 저-SOC staging 기여).
- 20–100% SOC: −0.1 ~ +0.1 mV/K (작은 계수, 측정 노이즈 큼).
- 문헌 비교(Table II): 0–20% 최대 0.3–0.62 mV/K; 20–100% 최대 0.1–0.12 mV/K.
- 불확도: 4셀 평균 std.dev. 3.13 µV/K, 최악 32% SOC 에서 9.93 µV/K. 고|∂U/∂T| 구간 상대불확도 ≈3.3%.
- 프로토콜(Table VI): 35°C 6h rest → 0°C 2h rest(스텝) → 0.1C −4%SOC 방전 → 96%~8% SOC 4%씩 23스텝. 평형 기준 dV/dt<0.1 mV/hr.

## 타당·한계
- 타당: 큰 ΔT 로 신호/노이즈 개선, PKP(방전후 완화)·PTP(열평형후 완화) 오차원 명시·완화, 셀간 재현성 정량.
- 한계: full cell(전극 분리 ΔS 직접 X), M50LT 특화(LFP·solid-state 미검증), 선형 ∂U/∂T(35°C 구간 상수) 가정, 1-D radial 열전도 근사, SOC>100%·<8% 적용 불가.

## 우리 의도 관련성
- Bernardi 가역항을 **실측 protocol** 로 잇는다: ∂U/∂T(SOC) 측정 방법·평형 기준(dV/dt<0.1 mV/hr)·온도 스텝 설계·불확도 정량은 우리 다온도 dQ/dV 피팅의 측정·검증 표준 참고.
- 단 이 논문은 dU/dT 를 직접 스텝-측정(우리는 dQ/dV(T) 피팅으로 ∂U_j/∂T 를 전이별로 추출) → 방법은 다르나 검증·크로스체크 anchor.

## 정독 범위
- **full-text(IOP HTML 본문, WebFetch 구조화 추출)** — 식·protocol·정량값·한계 표(Table II/VI)·불확도 모두 본문에서 확보. 단 ΔS 부호 1건 추출 의심.

## tier
- 식 형태·protocol·불확도: **확정에 준함**(IOP 본문 추출).
- 정량값(mV/K, SOC): **확정에 준함**(full cell 값임을 명시 — 전극분리 아님).
- ∂U/∂T=−ΔS/nF 부호: **미검증**(Bernardi 카드와 동일 부호 이슈).

## Decision-queue
1. ★ ΔS 부호(위 Bernardi #1 과 동일) — master 원문 확정.
2. 이 full-cell 값(0.3–0.5 mV/K @low SOC)을 graphite 전극 기여로 어디까지 귀속할지 — Reynier·MSMR 전극분리값과 대조해 master 판단.
