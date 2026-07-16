# FRAMING_FO2 — v1.0.20 그림/그래프 경쟁 저작 (창 FO2)

> 대상: `Claude/docs/v1.0.20/_sections/ch1_*.tex`·`ch2_*.tex`·`appendix_phase_separation.tex`
> 유일 쓰기 영역: `results/comp_P7_figs/FO2/`. 문서 원본 수정 없음. 다른 창 폴더·`comp_P7_review/` 미열람.
> 사용 가능 패키지(전수 확인): **pgfplots 없음** → `\draw plot coordinates{...}` 방식만.
> - ch1 preamble tikz 라이브러리: `positioning, arrows.meta, calc, fit, backgrounds`
> - ch2 preamble tikz 라이브러리: `calc, arrows.meta, decorations.pathreplacing, positioning`
> - 두 장 공통 안전 집합: `calc, arrows.meta, positioning` (내 구현은 이 공통 집합 + `Latex`/`Stealth` 화살촉만 사용 → 양장 어디든 배치 가능)

---

## 1단계 — 실태 조사 (전수 목록 + 부실 진단)

### 1-A. 기존 그림 전수 목록 (tikzpicture 기반 21개; 표/longtable 캡션 제외)

| # | 파일 | 라벨 | 내용 | 역할(어느 식/절) | 정보밀도 | 부실 진단 |
|---|------|------|------|------------------|:--------:|-----------|
| 1 | ch1_sec00_intro | `fig:spine` | N0~N9 계산 진행 순서도(flowchart) | 서론 계산 골격 | 중 | 양호. 개념 지도. 곡선 산출과 무관한 구조도 |
| 2 | ch1_sec01_n0n1 | `fig:staging` | staging 갤러리 채움 도식(위) + 실제 dQ/dV 4-peak(아래, eq:eqpeak 초기값) | N9 합산·관측 지문 | 높음 | 매우 충실. 갤러리+실좌표 peak 병치 |
| 3 | ch1_sec02a_part0 | `fig:sm-reservoir` | grand canonical 저장조 모식 | Part0 앙상블 | 낮음 | 단순 모식(정당). 개선 불요 |
| 4 | ch1_sec02b_part0 | `fig:sm-gxi` | 정규용액 섞임 몫 f(ξ)/RT | Part0 평균장 | 중 | 양호(수치 평가) |
| 5 | ch1_sec02b_part0 | `fig:sm-mu` | 격자기체 화학퍼텐셜 μ(θ) | Part0 평균장 | 중 | 양호 |
| 6 | ch1_sec02b_part0 | `fig:sm-occ` | (a) θ vs (ε−μ)/kT 3온도 (b) ξ_eq(V)·θ_eq(V) 3온도 | eq:fermifn·logistic | 매우 높음 | 매우 충실 |
| 7 | ch1_sec04_hys | `fig:doublewell` | 격자기체 자유에너지 이중웰(개형) | eq:gxi·spinodal | 중 | **개형** 명시. 정성 곡선(수치판=fig:sm-gxi) |
| 8 | ch1_sec04_hys | `fig:hysloop` | 비단조 V_eq(ξ), Ω=4RT, 과주행·gap | eq:Veq·dUhys | 매우 높음 | 매우 충실 |
| 9 | ch1_sec05_width | `fig:barrier` | Eyring 활성화 지형 (a)평형 (b)구동 | eq:bv·db | 높음 | 충실 |
| 10 | ch1_sec05_width | `fig:flux` | 정·역 플럭스 교점 → ξ_eq(3 affinity) | eq:logisticsolve | 높음 | 충실 |
| 11 | ch1_sec05_width | `fig:logistic` | ξ_eq + 미분 종(dual axis) 3온도 | eq:xieq·belliden | 매우 높음 | 매우 충실 |
| 12 | ch1_sec07_broadening | `fig:widthbudget` | 폭 예산 waterfall 4단계 | eq:widthbudget | 매우 높음 | 매우 충실 |
| 13 | ch1_sec07_broadening | `fig:broadening` | (a)고용체 종 (b)두-상 델타→종 | eq:eqpeak·ensavg | 높음 | 양호 |
| 14 | ch1_sec09_tail | `fig:relaxode` | 지연 완화: 목표/지연/차 | eq:lag·peakshape | 중 | **도식**(schematic) 좌표. 정량화 여지 |
| 15 | ch1_sec09_tail | `fig:reversal` | 인과 꼬리 방향 방전/충전 거울 | eq:reversal | 매우 높음 | 매우 충실(수치) |
| 16 | ch1_sec11_lcointro | `fig:lco-dirmap` | 충·방전 라벨↔탈리튬화 방향 | LCO 방향 규약 | 중 | 양호(개념도) |
| 17 | ch1_sec15_lcoelec | `fig:lco-electronic` | MIT-logistic 게이트 g(E_F,x)+|ΔS_e| bump | eq:ggate·dSegate | 높음 | 충실 |
| 18 | ch2_sec02_config | `fig:occ_config` | (a)점유 logistic (b)S_config(θ) | eq:occ·Sconfig | 높음 | 양호 |
| 19 | ch2_sec05_mixing | `fig:blend` | 겹침 가중 연속 블렌드 vs 계단 | eq:weighted | 중 | **모식**·좌표 임의(sigmoid). 실좌표化 여지 |
| 20 | appendix | `fig:app-tangent` | 혼합 자유에너지 공통접선 3구성 | eq:app-fxi | 매우 높음 | 매우 충실 |
| 21 | appendix | `fig:app-phasediag` | binodal/spinodal 상평형도 | eq:app-binodal | 매우 높음 | 매우 충실 |

**총평**: Chapter 1(그림 17개 중 12개가 tikz)과 appendix는 이미 **수치 평가 좌표·다중 주석·대조 요소**를 갖춘 고밀도 그림이 많다. 반면 **Chapter 2 는 그림이 단 2개**(occ_config, blend)뿐이고 그중 blend 는 모식·임의좌표다. 곧 **부실의 무게중심은 Chapter 2 의 그림 공백**과 소수의 모식(blend·relaxode·doublewell)에 있다.

### 1-B. 그림 공백 목록 (그림이 없어 이해가 어려운 핵심 절/개념)

| 공백 | 파일(절) | 왜 그림이 필요한가 | 산출 좌표 근거 |
|------|----------|--------------------|----------------|
| **G1. 가역 발열 SOC 부호 교대** | ch2_sec07_revheat·ch2_sec08_synthesis (§2.7·§2.8) | Chapter 2 의 **최종 도착 결과**(한 종합식이 SOC 축에서 흡/발열 부호를 스스로 뒤집음). 표 tab:qrev(5점)만 있고 **그림 0** | 모델 `entropy_coefficient_x`·`reversible_heat_x` — 5점 문건값과 **bit 일치 확인** |
| **G2. 평형 중심 U_j(T) 선형** | ch1_sec03_center (§3, N2) | eq:Uj `U_j=(−ΔH+TΔS)/F` 의 **온도 선형·기울기=ΔS/F 부호**가 그림 0. 다온도 피팅에서 중심 이동의 근거 | eq:Uj + tab:staging 4전이 — 정확 선형 |
| **G3. Einstein S_vib(T;θ_E)** | ch2_sec04_einstein (§2.4) | eq:Svib-einstein 닫힌형·두 극한(고온 log·저온 0)이 그림 0. 준양자 영역 개념 | eq:Svib-einstein 직접 평가; S_vib(298.15;700)=2.898 확인 |
| **G4. vib vs electronic 식별** | ch2_sec04_einstein·ch2_sec03_vibel (§2.4·§2.3) | "vib=강제영점+곡률 vs electronic=∝T 선형·무영점"이라는 **다온도 곡률 피팅 분리 논거**가 그림 0. 2점이 왜 부족한지 | eq:dUvib 기울기 — 문건 −3.74/0/+3.70/+9.14 μV/K **일치 확인** |
| G5. ΔS(x) 세 분포 분해 | ch2_sec03_vibel (§2.3) | config 발산 + vib 음 baseline + 중심 = 측정 ΔS(x)의 부호 구조 원천 | G1 의 complete/simple 분리로 부분 커버 |
| G6. N1 분극 V_n | ch1_sec01 (§pol) | eq:vn 측정→내부 전위, 충·방전 부호 | (기존 fig:spine 이 부분 언급) |

---

## 2단계 — 프레이밍 (창 소관 우선순위 top 7)

> 원칙: (i) **공백 우선**(Chapter 2 무게중심) (ii) 물리 안전(본문 식 수치 평가·부호/극한/단위 일치·새 물리 금지)
> (iii) 기존 고밀도 그림과 **중복 회피** (iv) 실좌표 하드코딩 가능성.

### top 우선순위 및 설계 스케치

**P1 — 가역 발열 SOC 부호 교대 (G1) [구현]**
- 무엇: 2단 패널. (상) ∂U_oc/∂T(x̄) [mV/K] — 완전식(실선)·단순식/중심값만(파선), 영선·영점(x̄≈0.68). (하) Q̇_rev/I(x̄) [mV] — 발열(exo)/흡열(endo) 음영 2영역, 영점, tab:qrev 5점 마커.
- 왜: Chapter 2 §2.8 종합식(eq:complete)의 **도착 결과**를 한 장으로. "한 식이 부호를 스스로 뒤집는다"를 시각화. 완전식 vs 단순식 대조가 config 몫(문건이 강조하는 이중계산 분리)을 그대로 보여줌.
- 스케치: x̄ 0.08→0.92. 상단 y −0.33~+0.26 mV/K, 영선 강조. 하단 y −77~+98 mV, y=0 위=발열/아래=흡열 음영. 크기 ~폭 12cm×높이 9cm. 대조=완전/단순 2곡선·발열/흡열 2음영.

**P2 — 평형 중심 U_j(T) 선형 (G2) [구현]**
- 무엇: T[K] vs U_j[V], 4 staging 전이의 직선. 기울기=ΔS_rxn/F(4→3 우상향, 3→2L 수평, 2L→2·2→1 우하향). 298.15 K 앵커점 표시.
- 왜: eq:Uj 의 온도 의존을 **부호까지** 보여줌. ΔS>0(config 우세)→중심 상승, ΔS<0(vib 우세)→중심 하강. N2 이해 직접 기여.
- 스케치: T 260~340, U 0.078~0.225. 4직선+298K 수직 안내선+앵커점·기울기 라벨. ~11cm×7cm. 대조=서로 다른 기울기 부호.

**P3 — Einstein 진동 엔트로피 S_vib(T;θ_E) (G3) [구현]**
- 무엇: T[K] vs S_vib[J/mol/K], θ_E=700 K(실선)·400 K(파선) 두 곡선 + 고온 점근선 R[1+ln(T/θ_E)](점선) + 저온 S_vib→0.
- 왜: eq:Svib-einstein 닫힌형과 두 극한 검산을 시각화. "고온=동결 상수의 출처, 저온=바닥상태 얼어붙음" 개념.
- 스케치: T 60~740, S 0~13.5. 곡선 2개+점근선 2개. 저온 0 수렴·고온 곡선-점근 접근 주석. ~11cm×7.5cm. 대조=θ_E 두 값·닫힌형 vs 점근선.

**P4 — vib/electronic 식별 신호 (G4) [구현]**
- 무엇: T[K] vs ∂U/∂T [μV/K]. vib 편차 ∂ΔU_vib/∂T(실선, θ_E=700K, **T_ref=298.15 강제영점+곡률**, 실좌표) vs electronic ∝T(파선, **무영점 직선**, 개형). 4온도점(278/298/318/348) 마커.
- 왜: §2.4 "두 함수형을 다온도 곡률로 가른다·2점은 축퇴"의 논거를 그림으로. 강제영점+곡률 vs 직선의 대비.
- 스케치: T 270~348, y −5.3~+9.1 μV/K. 실선 곡선+파선 직선+T_ref 수직선+4마커. 2점 국소기울기 축퇴 주석. ~11cm×7cm. 대조=곡률 vs 선형·영점 유무.

**P5 — (추가 후보) `fig:blend` 재설계** — 현재 임의 sigmoid 모식을 겹침 가중 실좌표(∂U_oc/∂T 국소값 블렌드)로 교체. 원 정보요소(연속 vs 계단 대비) 보존 + 실좌표 추가. *구현 여력 시.*

**P6 — (추가 후보) `fig:relaxode` 정량화** — 도식 좌표를 eq:lag 기억적분 실좌표로. 단 fig:reversal 이 이미 정량판 제공 → 우선순위 낮음.

**P7 — (추가 후보) ΔS(x) 세 분포 분해 (G5)** — P1 상단 패널이 complete/simple 분리로 부분 커버하므로 독립 구현 순위 낮춤.

### 확정: **구현 대상 = P1·P2·P3·P4 (4건)**. 라벨 = `fig:cand-fo2-1..4`(기존 라벨 비충돌 확인: 기존은 fig:spine/staging/... 로 `cand-fo2-` prefix 없음).

---
