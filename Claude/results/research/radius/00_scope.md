# 00 — Scope·연구질문·검색전략·전제 1차 판정

> 대상 모델: `Claude/results/v8-11/v8-11.tex`(Ch1 유도확장 최종) + `versions/v11_final.py`. master 정독 완료.
> 본 조사 = 모델 위 *해석 가설*(peak 형상→U_j 분포→반경 분포)의 타당성·조건 판정. 모델 수정 X.

## 검증 대상 가설 (사용자)
Ω≥2RT 일 때 단일 입자 dQ/dV peak 은 (유사) 델타여야 하나, 실측 코인 하프셀은 **치우친 종모양**. ∴ 종모양 = 단일입자 델타가 **U_j(전이 중심 전위) 분포**로 퍼진 통계역학적 형상. 흑연 입자 = 구형 가정, **U_j 분포가 오직 반경에만 의존**한다고 보면 **peak 형상 = U_j 분포 = 반경 분포** → 역변환으로 반경 분포 추산.

## 연구질문 6축
1. (전제) 단일 입자 Ω>2RT → dQ/dV 델타/극협? (1차 상전이 평형 형상·single-particle 실험)
2. (ensemble) U_j 분포 다입자계 → 매끈·치우친 평균 dQ/dV? (many-particle/mosaic/domino — 입자 독립 vs 상호작용)
3. (결합) 입자 **반경** → 전이 전위 U_j 이동? 기작(Gibbs–Thomson·strain·miscibility-gap 억제·표면재구성)·부호·크기. LiFePO4 나노 vs **흑연 마이크론** 정량.
4. (역문제) "peak→U_j 분포→반경 분포" 역변환 성립조건·유일성·deconvolution.
5. (선례) dQ/dV·DVA·GITT·EIS·relaxation → 입자크기분포 추출 선례·정확도·함정. OCV=site-energy DOS 해석.
6. (경쟁·정량) 흑연 마이크론 실측 치우침 = 반경분포 vs kinetic dispersion·접촉저항·조성이질성·온도 중 무엇? 분리 가능성.

## 검색전략
- DB: Google Scholar·CrossRef·arXiv·publisher(Nature·ACS·Elsevier·ECS·Wiley). 리뷰=진입점 → 1차 인용 추적.
- 포함: peer-review 1차·실측/이론 정량. 제외: 비-Li graphite·전고체·full-cell 부반응(경계 표시만).
- 쿼리 예: "particle size distribution dQ/dV graphite", "Gibbs-Thomson intercalation potential particle size", "many-particle model hysteresis insertion electrode Dreyer", "size-dependent phase diagram LiFePO4 Cogswell Bazant", "differential voltage analysis particle size", "single particle electrochemistry graphite staging", "lattice gas intercalation isotherm site energy distribution".

## 전제 1차 판정 (master, 모델·기초 열역학 — 문헌 보강 = 서브A) — tier: 확정(논리/모델)
- eq:Veq `V_eq(ξ)=U_j+(RT/sF)ln[ξ/(1−ξ)]+(Ω/sF)(1−2ξ)` 는 Ω>2RT 에서 **비단조**(local max @ξ_s⁻, local min @ξ_s⁺ = spinodal, eq:spinodal). 
- 참 평형(공통접선/Maxwell 작도)은 비단조 구간을 **수평 plateau**(공존 전위)로 대체 → V(q) 평탄 → `dq/dV→∞` → **단일·평형 입자 dQ/dV = Dirac 델타**(전이 용량 전부가 한 전위에서). ∴ **사용자 전제는 평형/mean-field 수준에서 성립**.
- 단서: (i) 모델 `w_eff`(eq:weff)는 *매끈 등온선 근사*라 진짜 델타가 아닌 floor(0.05·RT/F≈1.3 mV) 클립 극협 종 — 참 델타는 Maxwell 평형. (ii) 실제 단일 입자는 계면·kinetic 으로 유한 폭 가능(서브A 실험 확인). (iii) 기본 `use_w_eff=False`라 모델 기본 종폭은 `nRT/F`(25.7 mV) — Ω narrowing 미적용 상태.
- ★경쟁 경고: Ch1 모델은 실측 치우침을 **kinetic 꼬리**(N7/N8 `(ξ_eq−ξ_lag)/L_V`, 유한 전류 lag)로 *이미* 설명. 사용자 radius-분포 가설은 이와 **경쟁/보완** — Phase2 에서 분리 판정 필수.
