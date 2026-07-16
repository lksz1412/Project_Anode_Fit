# FRAMING_FO3 — v1.0.20 그림/그래프 경쟁 저작 (창 FO3)

> 독립·무통신 창. 대상 = `_sections/ch1_*.tex`(24) · `_sections/ch2_*.tex`(15) · `appendix_phase_separation.tex`.
> 유일 쓰기 영역 = 본 폴더. 문서 원본 수정 금지. 언어 = 한국어.
> preamble 확인 결과: **pgfplots 없음** → `plot[smooth] coordinates{...}`(python 평가 하드코딩) 또는 인라인 함수 방식만 사용.
>  - ch1 tikz 라이브러리 = `positioning, arrows.meta, calc, fit, backgrounds`
>  - ch2 tikz 라이브러리 = `calc, arrows.meta, decorations.pathreplacing, positioning`
>  - 공통 = kotex(한글), D2Coding, amsmath/amssymb/mathtools/bm. `\resizebox`(graphicx: hyperref 등 경유 로드됨 — 기존 fig:widthbudget·sm-occ·sm-mu 가 사용).

---

## 1단계 — 실태 조사 (전수 목록 + 부실 진단 + 공백)

### 1-A. 기존 그림(TikZ) 전수 목록 — 21건

| # | 파일 | 라벨 | 내용 / 역할 | 좌표 성격 | 품질 진단 |
|---|------|------|------------|-----------|-----------|
| 1 | ch1_sec00_intro | `fig:spine` | 계산 진행 spine(N0→N9 노드 flowchart) | 도식(노드) | 상. 문서 전체 지도. 정보밀도 높음 |
| 2 | ch1_sec01_n0n1 | `fig:staging` | 흑연 staging 갤러리 채움(위) + 4전이 dQ/dV peak(아래, eq:eqpeak 초기값) | 위=범주 도식 / 아래=식 수치평가 | 상. 단 4 peak을 **분리** 표시(합성·배경 없음) |
| 3 | ch1_sec02a_part0 | `fig:sm-reservoir` | grand canonical 저장조 모식 | 개념 도식 | 중상. 개념 전달용 |
| 4 | ch1_sec02b_part0 | `fig:sm-gxi` | 정규용액 f(ξ)/RT 섞임 몫 | 식 수치평가 | 상 |
| 5 | ch1_sec02b_part0 | `fig:sm-mu` | 격자기체 화학퍼텐셜 μ(θ) | 식 수치평가 | 상 |
| 6 | ch1_sec02b_part0 | `fig:sm-occ` | 단일자리 점유 재매개변수화 (a)θ(ε−μ) (b)ξ_eq(V) 3온도 | 식 수치평가 | 상 |
| 7 | ch1_sec04_hys | `fig:doublewell` | 이중웰 g(ξ) 개형 + spinodal 띠 | 개형(정성) | 중상. 명시적 "개형" |
| 8 | ch1_sec04_hys | `fig:hysloop` | 비단조 V_eq(ξ) 과주행·spinodal·gap | 식 수치평가 | 상(최상급). 정량 |
| 9 | ch1_sec05_width | `fig:barrier` | Eyring 활성화 장벽 (a)평형 (b)구동 | 모형퍼텐셜 수치평가 | 상. 정량 |
| 10 | ch1_sec05_width | `fig:flux` | 정·역 플럭스 교점=정지점 ξ_eq | 식 수치평가 | 상 |
| 11 | ch1_sec05_width | `fig:logistic` | ξ_eq + 미분 종(dξ/dV) 3온도, FWHM=3.53w | 식 수치평가 | 상. 단 dξ/dV(모양인자)이지 dQ/dV(=Q·모양) 아님 |
| 12 | ch1_sec07_broadening | `fig:widthbudget` | broadening 폭예산 waterfall 4단계 | 실제 합성곱 수치 | 상(최상급) |
| 13 | ch1_sec07_broadening | `fig:broadening` | (a)고용체 종 (b)두-상 델타→종 | 도식(개형) | 중상. 개형이나 캡션 "개형" 미명시 |
| 14 | ch1_sec09_tail | `fig:relaxode` | 지연 완화 ξ_eq/ξ_lag/r | **도식**(자인정) | 중. 유일하게 "도식 평가" — 정량화 여지 |
| 15 | ch1_sec09_tail | `fig:reversal` | 인과 꼬리 방향 (a)방전 (b)충전 거울 | 식 수치평가 | 상(최상급) |
| 16 | ch1_sec11_lcointro | `fig:lco-dirmap` | 충방전 라벨↔탈리튬화 방향 슬롯 | 개념 도식 | 중상 |
| 17 | ch1_sec15_lcoelec | `fig:lco-electronic` | LCO MIT-logistic 게이트 g(E_F,x) + |ΔS_e| bump | 손튜닝 개형 | 중. 좌표 근사(개형 미명시) |
| 18 | ch2_sec02_config | `fig:occ_config` | (a)점유분포⟨n⟩ (b)config 엔트로피 S_config(θ) | 인라인 함수 | 상 |
| 19 | ch2_sec05_mixing | `fig:blend` | 연속 블렌드 vs 계단(오답) | **모식**(자인정) | 중상. 부호·순서 임의 명시 |
| 20 | appendix | `fig:app-tangent` | 공통접선 상분리 3구성(안정/준안정/불안정) | 식 수치평가 | 상 |
| 21 | appendix | `fig:app-phasediag` | 상평형 그림 binodal/spinodal + 임계점 | 식 수치평가 | 상 |

표(그림 아님, 참고): tab:notation·tab:staging·tab:ds·tab:worked·tab:qrev·tab:signcheck-S/R·tab:symcode·tab:nodemap·tab:nodecode 등.

### 1-B. 부실 진단 요약(정보밀도·주석·독자 이해·시각 품질)

- 전반: Chapter 1 그림은 대부분 **정량·고밀도·잘 주석됨**(관행: "좌표는 식 그대로의 수치 평가"/"개형"/"모식" 캡션 규범 준수). 시각 품질 양호.
- 상대적 약점(재설계 후보):
  - `fig:relaxode`(#14): 유일하게 좌표가 순수 "도식" — 실제 인과 기억 적분(eq:lag) 수치로 승격 가능(단, fig:reversal 이 이미 정량으로 겹치므로 우선순위 낮음).
  - `fig:lco-electronic`(#17): 게이트 곡선 좌표가 손튜닝 개형(식 eq:ggate 의 정확 수치평가 아님) — 정량화 여지. 단 LCO는 부차 전개.
  - `fig:broadening`(#13): 개형인데 캡션에 "개형/모식" 미표기(rubric B7 관점 경미).
- 재설계보다 **공백 채움의 독자 이해 기여가 더 큼**(아래 1-C). 기존 그림은 정보 요소 유실 위험이 있어 원칙적으로 보존, 신규 후보에 자원 집중.

### 1-C. 그림 공백 목록 — 그림이 없어 이해가 어려운 절/개념

| ID | 위치 | 공백 개념 | 왜 필요한가 |
|----|------|-----------|-------------|
| G1 | §10 sum (N9), eq:sum | **합성 관측 dQ/dV = C_bg + Σ_j Q_j[peak]** | 문서가 최종 산출하는 **바로 그 한 곡선**(배경 위 4 peak 합산·겹침)의 그림이 전무. fig:staging은 peak을 분리 표시할 뿐 합성·배경 없음. 서론 "관측"이 말한 peak 겹침도 미시각화 |
| G2 | §2.8 synthesis, tab:qrev + eq:qrev | **가역 발열 부호 교대 q_rev/I(x̄)** | Chapter 2 의 **도착점**(저-x̄ 발열→고-x̄ 흡열)이 표 tab:qrev 만 존재. 한 종합식이 SOC 축에서 스스로 부호를 뒤집는 거동의 시각화 공백 |
| G3 | §6 eqpeak (N6), eq:eqpeak | **단일 평형 peak 해부도**(위치=U_j^d, 순높이=Q_j/4w_j, 면적=Q_j, FWHM=3.53w) | 문서 **중심식**이 한 식에서 읽는 세 양을 하나의 주석 종에 모은 그림 부재. fig:logistic은 dξ/dV(모양인자)만, Q_j 스케일·면적=Q_j 미표시 |
| G4 | §3 center (N2), eq:Uj | **U_j(T) 온도 의존**(기울기=ΔS_rxn/F, 전이별 부호차) | §3 전체에 그림 0. ∂U_j/∂T=ΔS/F 의 부호가 전이마다 달라 중심이 오르내리는(4→3 상승, 2→1 하강) 그림이 없어 "다온도마다 U_j 재독" 논거가 텍스트에만 |
| G5 | §1 N1 (pol), eq:vn | **V_app vs V_n 분극·충방전 거울** | 두 전위 구분(P3 검수 #1)의 시각화 부재. IR 분극이 peak을 방전=+, 충전=− 로 미는 거울 관계 |
| G6 | §2.8 tab:worked | **국소 dQ/dV 봉우리 가중 Q_j g_j(x̄)** | 한 SOC에서 "어느 봉우리가 활성"인지(겹침 가중 분모) 시각화 — 단 G2 기계와 중복 |
