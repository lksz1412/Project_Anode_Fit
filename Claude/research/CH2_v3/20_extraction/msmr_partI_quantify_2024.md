# msmr_partI_quantify_2024

**저자·연도·venue·DOI**: "Quantifying Entropy and Enthalpy of Insertion Materials via MSMR," *J. Electrochem. Soc.* 2024. DOI 10.1149/1945-7111/ad1d27. (Part I; Part II=ad70d9 흑연 적용.)

**축**: A5 (파라미터 추정·MSMR) — ★우리 다전이 ΔS·ΔH 정량 공식의 일반 틀.

## 핵심 방법
MSMR 갤러리(반응 j)별 평형전위와 그 **온도 의존성**으로부터 부분몰 엔트로피 ΔS·엔탈피 ΔH 를 stoichiometry 함수로 폐형 유도. half-cell OCV 최소자승 적합 + 셀-레벨 엔트로피 계수 측정(HTFDA, ±10°C 섭동)으로 온도 미분 추정. NMC811(4갤러리)·graphite(6갤러리, Allart et al. 참조) 검증.

## 지배식 (verbatim 기호 — ★ 우리 핵심 관계의 출처)
- 갤러리 전위(Eq.4, quasi-Nernstian): U_j = U_j⁰ + (RT/F)ω_j ln[ X_j(1−x_j) / (x_j(X_j−x_j)) ].
- **엔트로피 계수(Eq.22): dU/dT = (1/F)(ΔS/n).**  ⇒ (Eq.27) **ΔS = nF·dU/dT.**  ← **부호 = 양(+).** (Bernardi/Standardised 카드의 −부호 의심을 해소: 표준은 +ΔS/nF.)
- **엔탈피(Eq.28): ΔH = U·nF − T·nF·(dU/dT) = ΔG + TΔS** (ΔG=−nFU).
- 점유율 온도미분(Eq.20): dx_j/dT|_U 폐형(staging plateau 의 온도 이동).
- 총 엔트로피 계수(Eq.9): dU/dT = (1/(dx/dU))·(dx/dT). 갤러리별(Eq.23): dU_j/dT|_x = U_j⁰' + (RT/(ω_j F))ω_j' + (RT/F)ln[x_j(X_j−x_j)/((1−x_j)X_j)]·ω_j'.

## 정량값
- graphite: Allart et al.[42] 엔트로피 데이터 기준, **6 갤러리** 모델(Part II 의 5 와 차이 — master 대조).
- NMC811: 4 갤러리; 엔트로피 계수 peak @ x≈0.22,0.40,0.61,0.88; ΔH 크기 ~kJ/mol 규모(U·nF−T·nF·dU/dT 재구성).
- (흑연 절대 ΔS 값은 Part II/Reynier 카드 참조 — 본 카드는 일반식·NMC 예시 중심.)

## 타당·한계
- 타당: ∂U/∂T↔ΔS↔ΔH 의 **부호·폐형 완비**(Eq.22/27/28) — 우리 사슬의 수식 권위. dQ/dU(NDVS)=dQ/dV 와 직접 연결.
- 한계(저자 명시): 25°C 단일 분석, MSMR 파라미터·미분의 함수형 미정의; 예측 유효 "20% SOC 이상"(8–16% offset); 파라미터 온도의존 상수 가정(향후 과제). 목적함수가 평형전위 충실도에 100× 가중(엔트로피 오차 후순위) → 엔트로피 적합 정확도 한계.

## 우리 의도 관련성
- **수식 정전**: ΔS=nF·dU/dT(+부호), ΔH=nFU−T·nF·dU/dT 를 명시적으로 제공 → ∂U_j/∂T=ΔS_rxn,j/F(전이별, n=1)와 정확 일치. Bernardi 가역항에 바로 투입 가능한 ΔS_j 의 정의·산출법.
- dQ/dU(Eq. Part II A·7)=우리 dQ/dV; Eq.23 = 반응별 엔트로피 계수 분해 = 다전이 피팅 목표량.

## 정독 범위
- **full-text(IOP HTML 본문, WebFetch 구조화 추출)** — Eq.4,9,20,22,23,27,28·적합법·한계 본문 확보.

## tier
- 식(Eq.22/27/28 등)·부호: **확정에 준함**(IOP 본문, 부호 +ΔS/nF 명시). ← Bernardi/Standardised 부호 이슈를 **해소하는 1급 증거**.
- graphite 6갤러리 등 정량: **확정에 준함**(본문) — 단 Part II 5갤러리와 수 불일치는 master 대조 필요.

## Decision-queue
1. ★ 부호 확정 완료: ΔS=+nF·dU/dT (Eq.22/27). Bernardi·Standardised 카드의 −부호는 추출 오류로 판정 — master 최종 승인.
2. graphite 갤러리 수: Part I=6 vs Part II=5 불일치 — master 두 논문 본문 대조해 우리 Ch1 전이 매핑 결정.
3. 목적함수 100× 평형 가중이 우리 다온도 동시적합에도 권장되는지 — master 방법 설계 시 반영.
