# electrochimacta2019_occupation_transitions

**저자·연도·venue·DOI**: "Transitions of lithium occupation in graphite: A physically informed model in the dilute lithium occupation limit supported by electrochemical and thermodynamic measurements," *Electrochim. Acta* 2019. PII S0013468619316457.

**축**: A3 (ICA/dQ-dV 열역학) — ★우리 의도(dQ/dV ↔ ΔS·ΔH)에 **방법·물리 가장 근접**.

## 핵심 방법
two-layer **Bragg–Williams** 모델을 dilute Li 점유(0<x<~0.1) 극한으로 확장: 저점유에서 **Li–substrate 상호작용 항이 점유에 따라 변한다**는 물리(통상 고정 가정과 대비)를 도입. **galvanostatic + dQ/dV 측정 + 엔트로피 프로파일링**으로 부분몰 ΔS·ΔH 를 측정·검증. dQ/dV peak(= 전위 plateau)을 부분몰 ΔS·ΔH 의 길항으로 설명.

## 지배식 (verbatim 기호 — 부분 abstract)
- 부분몰 Gibbs: Δḡ(x) = Δh̄(x) − T·Δs̄(x); 셀전위 U(x) = −Δḡ(x)/F (n=1). → **dQ/dV peak ↔ Δs̄·Δh̄ 길항** 으로 plateau 발생.
- Bragg–Williams: Δs̄ 에 configurational(mixing) 항 + Li–substrate 상호작용의 점유의존(저-x 비선형) 항. (정확 식형은 본문 미정독.)

## 정량값
- dilute 범위 0 < x < ~0.1 연구; **x ≈ 0.07 전위 plateau**(dQ/dV peak), x < 0.05 가파른 전위 변화.
- 구체 ΔS·ΔH 절대 수치는 본 추출(검색)에서 미확보 — 본문/그림 정독 필요(Allart 2018 의 region IV +29 J/mol/K @x=0.08 가 같은 저-x 영역의 정량 교차참조).

## 타당·한계
- 타당: **dQ/dV ↔ 부분몰 ΔS·ΔH 의 직접 연결을 명시적으로 모델링·측정**한 사실상 유일 후보(우리 사슬의 방법 prototype). 저-x plateau 의 미해명 feature 를 ΔS/ΔH 길항으로 설명.
- 한계: dilute limit(0<x<0.1)에 특화 — 고-x staging(stage 2↔1) 은 본 모델 범위 밖(저자도 별개 물리로 명시). 절대 수치 본 추출 미확보. 단셀·특정 흑연.

## 우리 의도 관련성
- **방법 prototype(최근접)**: "dQ/dV 측정 + 엔트로피 프로파일링 → 부분몰 ΔS·ΔH" 사슬을 흑연 실데이터로 시연. 우리 다온도 dQ/dV 피팅 → ΔS(x) 의 직접 선례. 전위 plateau=dQ/dV peak 의 ΔS·ΔH 길항 해석은 우리 전이별 ∂U_j/∂T 물리 해석의 틀.
- 단 dilute 영역 한정 → 고-x 는 Allart/Reynier/MSMR 로 보완.

## 정독 범위
- **검색-snippet(WebSearch 복수 + abstract)** — 방법(dQ/dV+entropy profiling)·물리(plateau@0.07, ΔS·ΔH 길항)·범위(0<x<0.1) 확보. **식 정확형·절대 수치 미확보**(ScienceDirect 유료, full-text·bohrium 미파싱). ★tier 강등.

## tier
- 방법(dQ/dV↔ΔS·ΔH)·물리(plateau@~0.07, ΔS·ΔH 길항, Bragg–Williams 확장): **추정→확정에 준함**(abstract·복수 검색 일치).
- 식 정확형·절대 ΔS/ΔH 수치: **미검증**(본문 미정독).

## Decision-queue
1. ★ 본문 식(Bragg–Williams 확장 항)·부분몰 ΔS/ΔH 절대값·그림 — master/sub full-text 정독으로 채울 것(우리 방법 prototype 이므로 정밀 확보 우선순위 높음).
2. dilute(0<x<0.1) 모델을 고-x staging 으로 어떻게 잇는지 — Allart/Reynier 와 통합(master).
