# P2 — broadening + w 이중지위 통합 설계 (Ch1 v10 broadening 절 명세)

> 사용자 결정 baked: 다입자/PSD 모델 X(D3·radius "의미없음") · w_eff 제거(D2) · v9→v10 통합(D1). broadening 은 *설명(텍스트)*으로만 복원, 모델 확장 0.
> 근거: `research/radius/{ORIGIN,RADIUS,BAND}_VERDICT.md`·`DOCS_say_about_distribution.md`(v4/v5 verbatim). tier 병기.

## 0. 복원 핵심 (v8/v9 가 덜어낸 것)
v3/v4/v5 가 가졌고 v8/v9 가 0건으로 만든 **"평형 델타 vs 실측 종, w=현상학적 피팅 폭"** 축을 *올바른 물리*로 복원. **단, v4/v5 의 다입자/ρ_G 모델 기계장치는 안 가져온다**(D3) — *설명*만.

## 1. broadening 절 내용 (Ch1 v10 신규 절, 평형 peak §sec:peak 부근)

### (a) 전이별 출발 — 애초에 델타인 전이만 문제 [확정]
- **dilute→stage4·4L↔3L = solid-solution**(plateau 없음) → 단일 입자 평형 dQ/dV 가 **이미 폭 ~nRT/F 의 종**(Frumkin/정규용액; Levi&Aurbach 1999, 10.1016/S0013-4686(99)00202-9). broadening 불요.
- **2L→2(LiC₁₂)·2→1(LiC₆) = two-phase plateau(Ω>2RT)** → 평형 단일 입자는 **델타에 가까움**. → **"왜 델타가 아니고 종?" 은 이 두 전이에만 해당.**

### (b) two-phase 델타가 실측 유한 종이 되는 까닭 — 동역학·내재·★집합 통계역학 [확정]
평형 *단일 입자*가 아니라, *측정 조건 + 입자 집합*이 폭을 만든다(전부 평형 U_j 분포 아님):
1. **유한율속 비대칭 꼬리**: 단일 입자라도 유한 전류면 표면 SOC 가 평형을 앞서/뒤처져 과전압 η(SOC) 가 변하며 peak 을 한쪽으로 밀고 꼬리를 늘인다 = 모델의 `(ξ_eq−ξ_lag)/L_V`(N7/N8). C-rate↑ 심화·평형(C→0) 소멸. (Fly 2020, 10.1016/j.est.2019.101329)
2. **내재 RT/F 폭**: 평탄역 양끝 단상 꼬리·정렬 폭이 ~26 mV floor.
3. ★**집합 다입자 통계역학** [★사용자 요구 = 반영]: 전극은 N 입자 *앙상블*이고, 입자마다 **전이전위·배리어가 분포** $\rho(U_j)$ 를 이룬다(결정성·흑연화도·turbostratic 무질서·국소 환경 = ★**비-크기** heterogeneity; Dahn 1995, 10.1126/science.270.5236.590, $x_\max=1-P$). two-phase 의 단일입자 평형은 델타지만, **앙상블 통계평균** $\langle\dd Q/\dd V\rangle=\int\rho(U_j)\,\delta\text{-류 응답}\,\dd U_j$ 가 유한 종으로 번진다(Dreyer 다입자 순차전환, 10.1038/nmat2730). ρ→δ 면 단일 델타 환원. → ★**forward 통계평균만**(역산 X). 
→ ★**그러므로 two-phase 전이의 폭 $w_j$ 는 평형 예측($nRT/F$)이 아니라 (1)(2)(3) broadening 이 정하는 *현상학적 자유 피팅 폭*이다.** (v8 이 덜어낸 핵심 — apparent-U = U_j + η, 분포하는 건 η + 앙상블 ρ(U_j).)

### (c) 무엇을 *하지 않는가* — ★범위·경고 (★사이즈만 제외)
- ★**파티클 *사이즈* 효과는 빼라**(사용자 명시): 입자 크기 kinetic 분산 τ∝r²·반경→U_j·PSD convolution 크기분산 — *전부 제외*(radius 조사 결론 = 크기각도 의미없음·반경→평형U 마이크론서 ~0.01mV·Cogswell-Bazant 2012 임계 22nm). 집합 통계역학(b-3)은 *전이전위 분포*(비-크기)로 다룬다, 크기 분포로 다루지 않는다.
- **dQ/dV→ρ(U_j) 역산 안 한다**(forward 통계평균만, ill-posed 1종 Fredholm). 평형 U_j 중심은 GITT 상 입자 무관 상수(분포는 ρ 폭으로 *작게*).
- **dQ/dV→분포 역산 = ill-posed(forward-only)**: 다입자/PSD convolution 모델은 만들지 않는다(D3, radius 조사 결론 = 추출 의미없음). 입자 heterogeneity 는 현상학적 $w$ 에 흡수되는 것으로만 언급(별도 모델·추출 X).

## 2. w 이중지위 (Ch1 본문 N4/N5 폭 절 보강)
- **단상(Ω<2RT)**: $w=nRT/F$ = 검증 가능한 평형 예측(등온선 폭).
- **두-상(Ω>2RT, ★우리 staging 4개 전부)**: $w$ = **현상학적 자유 피팅 폭**(평형 아님, broadening 이 정함). 피팅 대상 파라미터.
- 명시 문장 1개로 두 지위 구분.

## 3. w_eff 제거 (D2)
- 현 Ch1 (해당 시)·Ch2 v4 §C 의 **$w_\eff(\Omega)$ "상호작용이 종을 좁힘→델타" 절 제거**: two-phase 실측은 *종*이지 델타가 아니다(narrowing 은 반대 방향). 종폭은 §1(b) broadening·현상학적 w 가 설명.
- 코드 `use_w_eff` = 면적보존 깨진 버그 → v12 제거(P7). 문서도 w_eff 자취 0.

## 4. Ch1 v10 통합 명세 (전부 때려박기, D1)
v10 = 현 v9(흑연 forward + LCO 전자 엔트로피 + ξ_eq 분포 + 통계역학) **보존** + 추가:
- ★**broadening 절**(§1: 전이별·현상학적 w·범위 경고)
- ★**w 이중지위**(§2)
- ★**w_eff 제거**(§3, 있으면)
- 기존 LCO/전자엔트로피/분포/부호 **불변**.

## Gate (P2)
broadening 절 내용·전이별 구분·현상학적 w·★다입자 모델 0·범위 경고·w 이중지위·w_eff 제거 사유 확정. radius DOI grounded·4-tier. → P3 Ch1 v10 spine·AUTHOR_BRIEF.
