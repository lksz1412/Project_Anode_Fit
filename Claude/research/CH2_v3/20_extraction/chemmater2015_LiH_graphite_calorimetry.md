# chemmater2015_LiH_graphite_calorimetry

**저자·연도·venue·DOI**: "Intercalation Compounds from LiH and Graphite: Relative Stability of Metastable Stages and Thermodynamic Stability of Dilute Stage Id," *Chem. Mater.* 2015. DOI 10.1021/acs.chemmater.5b00235.

**축**: A4 (Li-graphite staging 열역학·실험 calorimetry) — 형성 ΔH 절댓값 anchor.

## 핵심 방법
LiH + graphite 분말을 400–550°C, dynamic vacuum 에서 가열해 staged Li-GIC 합성, 직접 calorimetry(455 K)로 형성 엔탈피 측정 + powder XRD·Raman 으로 stage 동정. 준안정 stage 상대 안정성·dilute stage Id 열역학 안정성 규명.

## 지배식 (verbatim 기호)
정량 calorimetry 논문(평형식 유도보다 측정값 중심). 형성반응 ΔH_form (per mol Li) 직접 측정. (전위 엔트로피 계수 식은 본 논문 범위 아님.)

## 정량값 (직접 측정)
- **형성 엔탈피 ΔH_form (455 K, per mol Li)**:
  - LiC6 (stage I): **−13.9 ± 1.2 kJ/mol Li**
  - LiC12 (stage II): **−24.8 ± 1.0 kJ/mol Li**  (※ stage II 가 더 음수 = 고-x 에서 Li–Li 반발로 stage I 가 덜 안정 ↔ Reynier ΔH 경향과 정합).
- 동정된 stages: I(LiC6, Aα), IIa(Li0.5C6, AαA), IIb(Li~0.33C6, AαABβB), III(Li~0.22C6, AαAB), IV(Li~0.167C6), dilute Id.
- (3D→2D) 상전이: LiC6 T=711±5 K, ΔH_ph.tr=1.1±0.3 kJ/mol Li; LiC12 T=472±5 K, ΔH_ph.tr=1.45±0.2 kJ/mol Li.

## 타당·한계
- 타당: 형성 ΔH 의 직접 calorimetric 절댓값(드묾) — 전기화학 ΔH 측정의 독립 검증 anchor.
- 한계: 고온(455 K) 측정값 → 상온 전기화학 셀 ΔH 와 직접 동일시 X(온도 보정·상 차이 유의). LiH 경로 합성 = 전기화학 lithiation 과 경로 다름(준안정 stage 강조). ΔS 직접값은 본 추출에서 미확인(주로 ΔH·상전이).

## 우리 의도 관련성
- 가역발열 사슬의 **ΔH 절댓값 sanity anchor**: 우리 dQ/dV 피팅이 산출할 전이별 ΔH(=−FU+TΔS 의 ΔH 성분) 크기 스케일(수십 kJ/mol Li) 검증.
- stage I vs II 의 ΔH 역전(II 더 음수)은 고-x Li–Li 반발의 열역학 증거 → ΔS(x) 부호반전(Reynier)과 같은 물리의 엔탈피측 표현.

## 정독 범위
- **검색-snippet(WebSearch, ACS abstract+요약 수치)** — 정량값(ΔH_form, 상전이 T·ΔH)은 snippet 에 명시. 본문 full-text 직접 정독 X(ACS 유료).

## tier
- ΔH_form 값(−13.9±1.2, −24.8±1.0 kJ/mol Li): **추정→확정에 준함**(abstract 수치 직접 인용, 본문 미정독). ★tier 강등 명시.
- ΔS 값: **미검증/미확인**(본 추출에서 ΔS 정량 미확보).

## Decision-queue
1. 본 논문에 ΔS_form 정량이 있는지 — master full-text 확인(있다면 강력한 독립 anchor).
2. 455 K 값→상온 환산 필요성·정당성 — master 판단(우리 셀 온도 범위와 차이 큼).
