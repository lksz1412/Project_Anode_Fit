# bernardi1985_energy_balance

**저자·연도·venue·DOI**: D. Bernardi, E. Pawlikowski, J. Newman, "A General Energy Balance for Battery Systems," *J. Electrochem. Soc.* 132(1), 5–12, 1985. DOI 10.1149/1.2113792.

**축**: A2 (가역 발열·Bernardi·열모델) — 본 사슬의 ★정전(canonical anchor).

## 핵심 방법
전지 시스템 전체에 대한 일반 에너지 수지(energy balance)를 1열역학 1법칙에서 유도. 온도 변화의 기여를 (i) 전기화학 반응(가역 엔트로피항), (ii) 상변화, (iii) 혼합(mixing) 효과, (iv) Joule(저항)열 네 항으로 완전·일반 형태로 분해. 실무에서 가장 널리 쓰이는 단순화 형태(균일 온도·단일 반응·혼합·상변화 무시)로 축약된다.

## 지배식 (verbatim 기호 — tier 주의)
단순화된(일반에 널리 인용되는) 발열률:

  Q̇ = I (U − V) − I · T · (∂U/∂T)

- 1항 I(U−V) = 비가역(과전압/분극·저항) 발열 ≥ 0.
- 2항 −I·T·(∂U/∂T) = **가역(엔트로피) 발열**. 등가로 Q̇_rev = −I·T·(dU_OCV/dT).
- 부호 규약: I > 0 = 방전(discharge), U = open-circuit(평형) 전위, V = 셀 전압, T = 절대온도(K).
- **엔트로피 계수** ∂U/∂T(= dU_OCV/dT) ↔ 반응 엔트로피 관계: **∂U/∂T = ΔS/(nF)** (Gibbs–Helmholtz; ΔG=−nFU, ΔS=−∂ΔG/∂T ⇒ ∂U/∂T = ΔS/nF). n=이동 전자수, F=Faraday 상수, ΔS=반응 엔트로피.
  - ※ 우리 의도의 핵심 연결고리. **부호 주의**: 본 카드 작성 중 자동추출 도구(source #8 표준법 논문)가 동일 관계를 `∂U/∂T = −ΔS/(nF)` 로 출력했으나, 이는 추출 부호 오류로 의심된다(표준 정의 ΔG=−nFE_eq ⇒ dE_eq/dT=+ΔS/nF, Reynier 2003·Newman 교과서와 일치). Decision-queue 에 등록.

## 정량값
원논문은 정량 측정값 제시 X(이론 정전). 정량은 후속 측정 문헌(Reynier·MSMR 등)에서.

## 타당·한계
- 타당: 가장 일반적인 전지 에너지 수지 유도, ~1800+ 피인용의 표준. Bernardi 본인이 "측정 가능한 셀 특성 기반으로 가역 발열률을 요약"(2차 인용).
- 한계: 단순화 형태는 균일 온도·혼합/상변화 무시·단일 평균 OCV 가정. 다전이(multi-stage)·국부 비균일을 직접 다루지 않음 → 우리는 전이별 ΔS_j 를 별도 측정/피팅으로 공급해야 함.

## 우리 의도 관련성
가역 발열 사슬의 **종점 식**을 제공: Q̇_rev = −I·T·∂U/∂T. dQ/dV 다온도 피팅 → ∂U_j/∂T = ΔS_rxn,j/F(전이별) → 본 식에 대입 → 전이별 가역 발열. 즉 Ch1 평형식과 발열 모델을 잇는 정전 다리.

## 정독 범위
- **검색-snippet + 2차 verbatim(source #8 표준법 논문 본문에서 식 형태·기호 확인)**. 원논문 full-text 직접 정독 X(IOP/scispace 403, arXiv 인용본 PDF 텍스트 미파싱).
- 식 형태 Q̇=I(U−V)−I·T·∂U/∂T 와 ∂U/∂T=ΔS/nF 는 복수 독립 2차 출처 일치로 **확정에 준함**. 단 부호 1건 미해소.

## tier
- 식 형태(Q̇=I(U−V)−IT∂U/∂T): **추정→확정에 준함**(복수 2차 일치, 원문 직접 X).
- ∂U/∂T=ΔS/nF 부호: **미검증**(2차 1건이 −부호 출력, 표준과 상충 — Decision-queue).
- 정량값: 해당 없음.

## Decision-queue
1. ★ ∂U/∂T = +ΔS/(nF) vs −ΔS/(nF) 부호 — 원논문 또는 Newman 교과서 직접 정독으로 master 가 확정 요(우리 발열 부호 전체에 영향).
2. 원논문 Eq. 번호·"mixing/phase change" 항의 정확한 형태가 우리에 필요한지(현재는 불필요로 보임) master 판단.
