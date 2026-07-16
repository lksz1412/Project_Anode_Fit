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

---

## 2단계 — 프레이밍 (창 소관: 우선순위 top 6 자체 확정)

> 선정 원칙: (a) 독자 이해 기여(공백>재설계), (b) 문서 중심식·장 도착점 우선, (c) 식 그대로의 수치 평가로
> 물리 무결 보장 가능한 것, (d) 기존 그림과 중복 최소. 아래 6건 확정, 상위 4건 구현.

### [1] (신규·구현) 합성 관측 dQ/dV — N9 → `fig:cand-fo3-1`
- **무엇**: 배경 pedestal + 네 전이 봉우리(얇은 회색) + 그 합(굵은 실선 = 실제 관측 곡선)을 한 $V_n$ 축에.
- **왜**: 문서가 최종 산출하는 식~(eq:sum) $\dd Q/\dd V=C_\bg+\sum_j Q_j[\text{peak}]_j$ 의 **결과 곡선** 자체가
  전무했다. fig:staging 은 봉우리를 분리해 보일 뿐 합성·배경·겹침이 없어, 서론 "관측"의 peak 겹침을
  독자가 그림으로 못 본다. 이 그림이 "한 곡선을 그린다"는 문서 목표의 도착 이미지다.
- **스케치**: 가로 $V_n$[V] 0.03–0.26(증가=우), 세로 $\dd Q/\dd V$[Q_cell/V] 0–13. 얇은 회색 4곡선 + 굵은
  합성 1곡선 + 점선 배경. 주석=전이명·겹침 shoulder 화살표·방전 방향. 대조=fig:staging(분리) ↔ 본 그림(합성).
  크기 ~9×5 cm.

### [2] (신규·구현) 가역 발열 부호 교대 q_rev/I(x̄) — Ch2 §2.8 → `fig:cand-fo3-2`
- **무엇**: $\dot Q_\rev/I=-T\,\partial U_\oc/\partial T$ 를 탈리튬화 분율 $\bar x$ 에 대해. 발열/흡열 영역 음영 +
  부호 반전점 + tab:qrev 5점 마커.
- **왜**: Chapter 2 의 **도착점**(저-x̄ 발열→고-x̄ 흡열, "한 종합식이 스스로 부호를 뒤집음")이 표 tab:qrev
  로만 존재했다. 식~(eq:qrev)·(eq:implicit)의 귀결을 곡선으로 보이면 "외부 스위치 없이 분포만으로 교대"가 한눈에.
- **스케치**: 가로 $\bar x$ 0–1, 세로 $\dot Q_\rev/I$[mV] −100..+112, 0선 파선. 발열/흡열 배경 음영 2단, 반전점
  $\bar x\!\approx\!0.68$ 표시, 5점 정확 마커(표와 대조). 크기 ~8×5 cm.

### [3] (신규·구현) 단일 평형 peak 해부도 — N6 중심식 → `fig:cand-fo3-3`
- **무엇**: 종 하나에 위치=$U_j^d$, 순높이=$Q_j/(4w_j)$, 배경차감 면적=$Q_j$(음영), FWHM=$3.53w_j$ 를 주석.
- **왜**: 문서 **중심식** (eq:eqpeak)이 "한 식에서 세 양을 읽는다"고 말하나, 세 양을 한 종에 모은 그림이 없다
  (fig:logistic 은 $\dd\xi/\dd V$ 모양인자·FWHM 만, $Q_j$ 스케일·면적=$Q_j$ 미표시).
- **스케치**: 가로 $(V-U_j^d)/w_j$ −5..5, 세로 $\dd Q/\dd V$. 종+면적 음영+높이 파선+FWHM 치수선+중심 점선.
  크기 ~10×4 cm.

### [4] (신규·구현) 평형 중심의 온도 의존 U_j(T) — N2 → `fig:cand-fo3-4`
- **무엇**: 네 전이 $U_j(T)=(-\Delta H_\rxn+T\Delta S_\rxn)/F$ 직선, 기울기=$\Delta S_{\rxn,j}/F$ 의 부호차.
- **왜**: §3 전체에 그림 0. $\partial U_j/\partial T=\Delta S/F$ 의 **부호가 전이마다 달라** 중심이 오르내리는
  것(4→3 상승, 2→1 하강)이 텍스트에만 있어, "다온도마다 U_j 재독" 논거의 시각 근거가 없었다.
- **스케치**: 가로 $T$[K] 268–328, 세로 $U_j$[mV] 75–225(끊음). 직선 4개 + 우측 전이명 + 기울기 범례 박스 +
  기준 등온선. 크기 ~9×5 cm.

### [5] (신규·미구현 후보) V_app vs V_n 분극·충방전 거울 — N1
- **무엇/왜**: 두 전위 $V_\app=V_n+\sigma_d|I|R_n$(eq:vn)의 구분과, IR 분극이 peak 을 방전(+)·충전(−)으로 미는
  거울 관계. P3 검수 #1(전위 기호 구분)의 시각 보강. **스케치**: 같은 평형 peak 을 $V_\app$·$V_n$ 두 좌표에
  나란히, 분극 shift 화살표+충방전 거울. (구현 보류 — 상위 4건 우선.)

### [6] (신규·미구현 후보) 국소 봉우리 가중 Q_j g_j(x̄) — Ch2 tab:worked
- **무엇/왜**: 한 SOC에서 "어느 봉우리가 활성"인지(겹침 가중 분모 $\sum Q_jg_j$)의 막대/곡선. 단 [2]의 음함수
  기계와 물리가 겹쳐 우선순위 하위. (구현 보류.)

---

## 3단계 — 구현 (실제 TikZ 4건 + 컴파일 검증)

### 구현 목록 (모두 `\begin{figure}..\end{figure}` 완결 조각, 라벨 `fig:cand-fo3-*` — 기존 라벨과 무충돌)

| 파일 | 라벨 | 대상 절(배치 제안) | 좌표 성격 | 사용 라이브러리 |
|------|------|-------------------|-----------|-----------------|
| `fig_fo3_1_composite_dqdv.tex` | `fig:cand-fo3-1` | §10 sec:sum, eq:sum 박스 직후 | 식 그대로 수치 평가(python) | arrows.meta (ch1) |
| `fig_fo3_2_qrev_signflip.tex` | `fig:cand-fo3-2` | §2.8 sec:synthesis, tab:qrev 인접 | 식 그대로 수치 평가(음함수 해, python) | arrows.meta (ch2) |
| `fig_fo3_3_peak_anatomy.tex` | `fig:cand-fo3-3` | §6 sec:eqpeak, eq:eqpeak 박스 직후 | 식 그대로 수치 평가(python) | arrows.meta (ch1) |
| `fig_fo3_4_center_UjT.tex` | `fig:cand-fo3-4` | §3 sec:center, eq:Uj 박스 직후 | 식 그대로 수치 평가(python) | arrows.meta (ch1) |

- 좌표 provenance: `gen_coords.py`(검증)·`emit_tikz.py`(좌표 출력)·`coords.json`. 모두 본 폴더 내.
- 캡션 규범 준수: 4건 모두 "좌표는 식 그대로의 수치 평가" 명시, 배경 pedestal 은 "예시 상수" 명시(rubric B7),
  한국어 완결 문장, 자기 버전 이력 언급 없음.

### 물리 무결 검증 (물리 가드)
- **CAND-2**: 음함수 $\sum_j Q_j\xi_{\eq,j}(U_\oc,T)=Q\bar x$ 를 python 이분법으로 풀고 중앙차분한 결과가
  표~tab:qrev **5점(0.10/0.25/0.50/0.75/0.90) 전부와 정확 일치**(U_oc·∂U/∂T·ΔS·q_rev 네 열 모두). 부호
  반전점 $\bar x{=}0.680$. 규약(eq:qrev, $+$=발열, 방전 $I>0$) 준수.
- **CAND-1**: 봉우리 순높이 $Q_j/(4w_j)$ = 1.25/1.875/4.46/10.42 로 fig:staging 의 peak 좌표(1.247/1.875/4.442/
  10.399)와 일치. 방전 $\sigma_d{=}+1$, 종 $\ge0$ 방향 불변.
- **CAND-3**: 종 $\xi(1-\xi)$ 정점 $\tfrac14$·FWHM $2\ln(3{+}2\sqrt2)w{=}3.5255w$ 해석식과 일치.
- **CAND-4**: 기울기 $\Delta S_{\rxn,j}/F$ = +0.301/0/−0.052/−0.166 mV/K, 부호=ΔS 부호. 단위 mV·K 정합.
- 새 물리 주장 없음. 기존 그림 정보 요소 유실 없음(신규 4건 모두 공백 채움).

### 컴파일 검증 (의무)
- 하네스 `_harness.tex` = `\documentclass{article}` + kotex + amsmath류 + graphicx + tikz(라이브러리 합집합
  `positioning,arrows.meta,calc,fit,backgrounds,decorations.pathreplacing`) + 사용 매크로 정의. 4조각 `\input`.
- 명령: `xelatex -interaction=nonstopmode -halt-on-error _harness.tex`
- 결과: **EXIT=0, 4 pages, 오류 0**(`^!`/Error/Fatal/Undefined control/Overfull/Dimension 전무).
  잔여 경고는 하네스에 실제 라벨이 없어 생기는 `\eqref`/`\ref` 미해결(`??`)뿐 — 비치명적이며 본문 `\input` 시 해소.
- 렌더 시각 검수(pymupdf 120 dpi) 후 라벨 겹침 3건(Fig1 합성 라벨, Fig2 x̄축 제목, Fig4 "2→1"↔"T[K]")
  수정·재컴파일(EXIT=0)·재검 완료. 최종 4건 모두 곡선 이탈·라벨 충돌 없음.

### 본문 배치 제안 (문서 원본 미수정 — 제안만)
- `fig:cand-fo3-1` → §10 (`ch1_sec10_sum.tex`) 식~(eq:sum) 박스 직후. fig:staging 의 짝(분리↔합성).
- `fig:cand-fo3-2` → §2.8 (`ch2_sec08_synthesis.tex`) 표~(tab:qrev) 직전 또는 직후.
- `fig:cand-fo3-3` → §6 (`ch1_sec06_eqpeak.tex`) 식~(eq:eqpeak) 박스 직후.
- `fig:cand-fo3-4` → §3 (`ch1_sec03_center.tex`) 식~(eq:Uj) 박스 직후(현재 §3 그림 0).

### 남은 개선 후보 (미구현 — 실제 수정 안 함)
- [5] V_app vs V_n 거울(N1), [6] 국소 봉우리 가중(Ch2). 기존 그림 재설계 후보: `fig:relaxode`(도식→인과적분
  수치 승격), `fig:lco-electronic`(게이트 개형→eq:ggate 정확 수치). 모두 우선순위 하위로 보고만.
