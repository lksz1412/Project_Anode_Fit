# hysteresis_entropy_uncertainty_2018

**저자·연도·venue·DOI**: "Uncertainties in entropy due to temperature path dependent voltage hysteresis in Li-ion cells," *J. Power Sources* 2018. PII S0378775318305287.

**축**: A-add (히스테리시스/가역경계, Q6) — ★엔트로피 측정 불확실성·가역 경계.

## 핵심 방법
potentiometric 엔트로피 측정에서 **온도 경로 의존(temperature path dependent) 전압 히스테리시스**가 ΔS 추정에 주는 불확실성을 정량. 1×2032 coin + 3×18650(NMC/NCA cathode, graphite anode) 셀로 다양한 온도 여기(excitation) 비교 → 최적 온도 여기 protocol 제안. (저자: 이 온도-경로 히스테리시스는 "기존 미보고".)

## 지배식 (verbatim 기호)
- 표준 ΔS = nF·(∂E_OCV/∂T) 전제. 핵심 기여는 식 신규보다 **측정 오차 모델**: dE/dT 추정이 온도 스텝 순서(가열 vs 냉각 경로)에 따라 달라짐 → ΔS 불확실성.
- 검증: "cell entropy changes from reversible heat agree excellently with those from temperature dependent OCV" (가역열법 ↔ OCV(T)법 정합 = Bernardi 가역항 ↔ ΔS 측정 일치 확인).

## 정량값
- 본 추출(검색)에서 구체 불확실도 수치(±%, µV/K)는 미확보 — 본문 정독 필요.
- 정성: 비선형 reaction entropy 거동, 온도 여기 설계가 ΔS 정확도 좌우; 최적 여기 protocol 제안.
- (관련 RSC D0TA10403E: graphite OCV 히스테리시스가 Li dynamics 만이 아니라 충/방전 phase succession 차이에서; **>50°C 에서도 잔류** — 순수 운동학적 완화 아님.)

## 타당·한계
- 타당: 우리 다온도 dQ/dV 피팅의 **핵심 위협(가역/비가역 경계)을 정면으로 정량**. 가역열법↔OCV(T)법 정합은 Bernardi 사슬의 실험 검증.
- 한계: full cell 중심(전극분리 아님); 구체 불확실도 수치 본 추출 미확보; graphite region II 특화 분석은 Allart/RSC 보강 필요.

## 우리 의도 관련성
- **가역성 경계(Q6) 직접 근거**: dQ/dV(T) 피팅으로 ∂U/∂T 추출 시, 온도 경로(가열/냉각)·히스테리시스 region(graphite region II, 0.1≤x≤0.3)에서 ΔS 가 경로의존 → 우리 ΔS(x)·가역발열 추정의 **불확실도 상한·측정 설계(온도 여기)** 근거.
- "가역열 ↔ OCV(T) 정합" = 우리가 OCV(T) 기반 ΔS 로 Bernardi 가역발열을 계산하는 것의 정당성.

## 정독 범위
- **검색-snippet(WebSearch + abstract) + 2차(RSC D0TA10403E 정성)** — 방법·정성·검증 확보. **구체 불확실도 수치 미확보**(ScienceDirect 유료, full-text 미정독). ★tier 강등.

## tier
- 방법·온도경로 히스테리시스 개념·가역열↔OCV 정합: **추정→확정에 준함**(abstract 명시).
- 정량 불확실도(±%, µV/K): **미검증**(본문 미정독).
- >50°C 잔류 히스테리시스: **추정**(2차 RSC, 별도 논문).

## Decision-queue
1. ★ 구체 불확실도 수치·최적 온도 여기 protocol — master/sub full-text 정독으로 채울 것(가역경계 정량의 핵심 공백).
2. graphite region II 히스테리시스가 우리 ΔS(x) 신뢰구간에 주는 정량 영향 — Allart 2018·RSC D0TA10403E 와 통합해 master 판단.
3. 우리 dQ/dV 피팅을 충/방전 분리할지(히스 회피) — master 방법 설계.
