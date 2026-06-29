# reynier2003_entropy_enthalpy

**저자·연도·venue·DOI**: Y. Reynier, R. Yazami, B. Fultz, "The entropy and enthalpy of lithium intercalation into graphite," *J. Power Sources* 119–121, 850–855, 2003. PII S0378775303002854.

**축**: A1 (엔트로피 계수 측정·흑연 프로파일) — ★ΔS(x)·ΔH(x) 실측 정전.

## 핵심 방법
graphite 반쪽셀 OCV 를 여러 온도에서 측정 → **개회로전위의 온도 의존**에서 인터칼레이션의 부분몰 ΔS·ΔH 를 x(LixC6) 함수로 추출. (OCV(T) slope→ΔS, 적합→ΔH.) Raman·선행 inelastic neutron scattering 으로 vibrational 기원 해석 보강.

## 지배식 (verbatim 기호 — tier 주의)
- ΔS_intercalation = F·(∂E_eq/∂T)  (= nF·dU/dT, n=1; MSMR Part I Eq.27 와 정합, +부호).
- ΔH = ΔG + TΔS = −F·E_eq + T·F·(∂E_eq/∂T).
- (논문은 OCV(T) 직접 측정·미분; 위 관계는 표준 정전, MSMR Part I 카드로 부호 확정.)

## 정량값 (graphite, LixC6)
- ΔS(x) **부호 거동**(정성·강확정): x<0.2(~0.25) → **ΔS 크고 양(+)**, configurational entropy(entropy of mixing) 지배. x>0.2(~0.25) → **ΔS 음(−)**, vibrational 기여 지배(2차 성분).
- 고-x 에서 stage compound 형성과 결부된 **두 plateau**(stage 2→1 등).
- ΔH(x): **모든 x 에서 음(−)**, x 증가할수록 덜 음(less negative). stage-2(LiC12)→stage-1(LiC6) 형성 시 ΔH 덜 음 = **고-x Li–Li 반발**(Chem.Mater.2015 ΔH 역전과 정합).
- ※ 구체 dE/dT(mV/K)·ΔS(J/mol/K) 절대 수치는 본 추출(검색)에서 미확보 — 본문/그림 정독 필요(MSMR Part II 흑연 +3~4 mV/K @low-x, ~0.2 부호반전이 정량 교차참조).

## 타당·한계
- 타당: 흑연 ΔS(x)·ΔH(x) 의 **원천 실측 표준**(~다수 후속 인용·MSMR Part I/II 가 reference 로 사용). configurational↔vibrational 물리 해석 확립.
- 한계: 절대 수치는 셀·흑연 종류 의존; 히스테리시스(특히 region II)는 후속(Allart 2018·JPS 2018 hysteresis)이 더 정량. 본 추출은 abstract+2차 일치 기반(절대값 미확보).

## 우리 의도 관련성
- 가역발열 사슬의 **ΔS(x) 물리·부호 anchor**: 다온도 dQ/dV → ∂U_j/∂T=ΔS_j/F 가 재현해야 할 타깃 프로파일(저-x 양수→x≈0.25 부호반전→고-x 음수·plateau). Bernardi 가역항의 부호(저-SOC 흡열 vs 고-SOC 발열)를 결정하는 물리.
- ΔH(x) 단조(덜 음) = 우리 ΔH 성분 sanity.

## 정독 범위
- **검색-snippet(WebSearch 복수 일치) + abstract** — 부호·물리 거동 강확정. **절대 수치(mV/K, J/mol/K)·그림값은 미확보**(ScienceDirect 유료, full-text 미정독). ★tier 강등.

## tier
- ΔS(x)·ΔH(x) **부호·정성 거동**: **확정에 준함**(복수 독립 출처 일치 + MSMR Part II 정량 정합).
- 절대 수치(dE/dT, ΔS, ΔH 값): **미검증**(본문 미정독) — master 정독 또는 Caltech open thesis(6nmrn-e2m11, 403)·academia PDF 로 보강 권장.

## Decision-queue
1. ★ 절대 수치 확보: dE/dT(mV/K) 및 ΔS(J/mol/K) vs x 표/그림 — master 또는 후속 sub 가 full-text/그림 정독으로 채울 것(현재 정성만).
2. region II 히스테리시스가 ΔS 측정에 주는 불확실성 — 히스 카드(JPS 2018)·Allart 2018 과 통합해 master 판단.
