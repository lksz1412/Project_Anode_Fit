# jpcc2021_firstprinciples_vib_config

**저자·연도·venue·DOI**: "Thermodynamic Analysis of Li-Intercalated Graphite by First-Principles Calculations with Vibrational and Configurational Contributions," *J. Phys. Chem. C* 2021, 125(51), 27891–27900. DOI 10.1021/acs.jpcc.1c08992.

**축**: A4 (Li-graphite staging 열역학·DFT) — ΔS 의 config↔vib 분해 이론 근거.

## 핵심 방법
LixC6 의 형성 자유에너지 ΔG 를 first-principles DFT 로 계산하되, **vibrational free energy(phonon 계산)**와 **configurational entropy** 두 성분을 명시 분해해 상안정성·staging 을 해석. Reynier 의 실험적 config(저-x)↔vib(고-x) 해석을 이론적으로 뒷받침.

## 지배식 (verbatim 기호)
- ΔG_form(x,T) = ΔE_DFT + F_vib(T) − T·S_config (성분 분해; 정확 식번호는 본문 미정독).
- (전위 엔트로피 계수 식은 본 논문 주제 아님 — config/vib 자유에너지 성분이 핵심.)

## 정량값 (DFT)
- vibrational free energy + configurational entropy 기여 합 = **< −20 meV/LixC6 for 0 ≤ x ≤ 1/3** (저-x 영역; 작지만 무시 못 할 크기).
- (상세 phonon·상도 수치는 본문/SI 미정독.)

## 타당·한계
- 타당: Reynier 의 config(저-x 양 ΔS)↔vib(고-x 음 ΔS) 이분 해석의 **제1원리 검증** — 우리 ΔS(x) 부호 물리에 이론 신뢰도 부여.
- 한계: 0 K DFT + harmonic phonon 근사, 유한온도 anharmonic·전자 엔트로피 제한적; staging 상도 DFT 자체 한계(interlayer vdW, ref 1607.05658 도 신뢰성 논의). 절대 ΔS(x) 전체 곡선보다 저-x(≤1/3) 위주.

## 우리 의도 관련성
- ΔS(x) 의 **성분 기원(config vs vib)**을 이론으로 고정 → 우리 다온도 dQ/dV 피팅이 산출할 ΔS(x) 부호반전을 "측정 잡음 아닌 물리"로 해석할 근거. 직접 정량 공급원은 아니고 해석·정당화 anchor.

## 정독 범위
- **검색-snippet(WebSearch, abstract 수치 <−20 meV/LixC6)** — full-text 미정독(ACS 유료). ★tier 강등.

## tier
- config/vib 분해 개념·<−20 meV/LixC6(0≤x≤1/3): **추정**(abstract 수치, 본문 미정독).
- 상세 식·상도: **미검증**.

## Decision-queue
1. 우리에 직접 정량이 필요한지 — 본 논문은 해석 anchor 성격. master 가 ΔS 부호 물리 서술의 인용으로만 쓸지 정량까지 끌지 결정.
2. DFT 상도 신뢰성 한계(1607.05658)와 함께 인용할지.
