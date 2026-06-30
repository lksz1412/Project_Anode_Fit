# 30 — Round 2 Scope: "델타가 종모양이 되는 진짜 원인은 무엇인가" (apparent-U 분포의 기원)

> Round 1(`RADIUS_VERDICT.md`) 결론: 반경→U_j 의 *열역학적* 결합은 마이크론 흑연서 무효(0.01–0.05 mV ≪ peak 폭). 사용자 재질문: "그럼 델타가 종모양 되는 건 뭐냐? 동일 C-rate라도 입자 크기에 따라 차오르는 SOC가 달라져 생기는 종모양 퍼짐인가? U_j 분포인 건 확실한데 그 원인을 모르겠다."
> Round 2 = **종모양의 진짜 기원** 규명 + 사용자 신가설(크기 의존 *kinetic* 분산) 집중 조사. R1 문건 덮어쓰기 X(addendum).

## ★master 재구성 (조사 전 개념 정리 — tier: 확정(모델·열역학 논리))
사용자가 "U_j 분포는 확실"이라 했으나, **종모양이 되려면 분포가 *필수*는 아니다.** 델타→종모양 경로는 최소 3계층이 있고, 이를 구분해야 "원인"이 잡힌다.

**계층 1 — 분포 없이도 종모양 (단일 입자만으로):**
- (1a) **내재 평형 폭**: 전이가 *강한* 1차(Ω≫2RT)가 아니면 단일 입자 dQ/dV 는 애초에 델타가 아니라 logistic 미분 종 `Q·ξ(1−ξ)/w`, 폭 `w=nRT/F`(n=1·298K → 25.7 mV, FWHM≈3.5w≈90 mV; n<1이면 좁아짐). ★실측 peak 폭(수십 mV)이 nRT/F 규모와 같은 자리수 — **델타 전제는 Ω>2RT 강1차 전이에만 성립**하고, 흑연 전이 일부(4L–3L 등)는 solid-solution이라 단일 입자가 *이미 종*이다. → "델타여야 하는데 종"이라는 출발 자체가 전이별로 다름.
- (1b) **단일 입자 유한율속 꼬리**: Ω>2RT 라도 유한 전류면 점유가 평형을 못 따라가 `(ξ_eq−ξ_lag)/L_V`(모델 N7/N8)로 **한 입자에서 비대칭 종**이 나온다. 분포 불요. C-rate 의존.
- (1c) **순차충전**(Dreyer): 동일 입자라도 ensemble 순차성으로 거시 plateau/종.

**계층 2 — apparent-U(겉보기 전이전위) 분포 (분포가 있다면, 그 정체):**
- 관측 peak 전위 V_peak = U_j(평형, ★GITT상 입자 무관 상수) + η(과전압). **분포하는 것은 평형 U_j 가 아니라 η.** 즉 사용자가 본 "U_j 분포"는 십중팔구 **apparent-U = U_j + η 의 분포**이고, 그 정체는 η(과전압)의 입자간 분산이다.
- η 분산의 원인: **(2a) ★크기 의존 kinetic 분산**(사용자 신가설 — 동일 셀 전류가 크기 다른 입자에 분배되며 국소 전류밀도·확산시간 τ∝r²/D 차이 → 큰 입자 더 지연 → apparent-U 퍼짐), (2b) 접촉저항·전류분포 이질, (2c) 두께방향 SOC 구배, (2d) 형태학·배향 이질.

**계층 3 — 참 열역학적 U_j 분포:** 마이크론 흑연선 ~0(R1). 나노/조성이질만 유의.

## ★Round 2 핵심 가설 재정식 (사용자 신가설을 정확히)
"종모양 = 크기 의존 SOC 차오름 차이" = **계층 2a**. 검증 명제:
> 동일 인가 C-rate에서, 입자 반경 분포 → (국소 전류밀도·확산 timescale τ∝r²/D 분포) → 입자별 과전압 η·국소 SOC 분포 → apparent 전이전위 분포 → dQ/dV 종모양 broadening. **이는 C-rate에 비례·저율서 소멸하는 *동역학* 효과**(R1의 열역학 1/r shift와 전혀 다른 채널).

이게 맞다면 사용자의 원래 "반경 분포 추산" 발상은 *열역학*이 아니라 *동역학* 경로로 부활 가능 — 단 추출되는 건 평형 U 분포가 아니라 "kinetic 분산 분포"이고 C-rate·D·형태학과 얽힘.

## Round 2 연구질문 (3축)
- **E** (계층1): 분포 *없이* 단일 입자만으로 델타가 종이 되는가 — 내재 폭 nRT/F·유한율속 꼬리·순차충전. 흑연 전이별 1차/연속 성격. → "분포가 필수인가?" 판정.
- **F** (계층2a·★사용자 신가설): 동일 C-rate·크기 분포 → kinetic 분산 → apparent-U 종모양. SPM→MPM, PSD as kinetic input, τ∝r²/D, non-uniform utilization/reaction, current distribution. 정량(broadening mV vs C-rate·PSD폭)·C-rate 스케일·문헌 선례.
- **G** (계층2 전체·식별): apparent-U 분포의 원인 전수 분류·순위 + **식별·분해 방법**(C-rate 의존성·GITT 잔여·온도·두께·단일입자 대조) + Ch1 모델(단일 유효입자+L_V)에 무엇을 더해야 이 분포가 들어오나.

## 검색 키워드(신규 초점)
"multi-particle model graphite particle size kinetic broadening dQ/dV", "single particle model distribution of particle sizes voltage", "non-uniform lithiation particle size current distribution electrode", "resistive reactant / mosaic kinetic", "particle size distribution overpotential intercalation simulation", "graphite staging two-phase vs solid solution order of transition", "apparent open circuit potential overpotential distribution electrode", "GITT residual peak width near equilibrium graphite".
