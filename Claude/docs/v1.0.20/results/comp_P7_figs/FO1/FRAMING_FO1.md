# FRAMING_FO1 — v1.0.20 물리 교과서 그림/그래프 경쟁 저작 (창 FO1)

> 창 FO1 · 독립·무통신. 언어 한국어. 유일 쓰기 영역 = 본 폴더.
> 대상 = `Claude/docs/v1.0.20/_sections/ch1_*.tex`(24)·`ch2_*.tex`(15)·`appendix_phase_separation.tex`.
> 환경: xelatex + cjk-ko(kotex) 확인. pgfplots **미로드** → `\draw plot coordinates` 하드코딩 방식.
> preamble tikz 라이브러리: Ch1 = `positioning,arrows.meta,calc,fit,backgrounds`; Ch2 = `calc,arrows.meta,decorations.pathreplacing,positioning`.
> 좌표 산출: 문서 자체 참조 구현 `Anode_Fit_v1.0.20.py`(GRAPHITE_STAGING_LIT·func_U_j·solve_U_oc·entropy_coefficient_x·equilibrium·dqdv)를 python 으로 평가해 하드코딩(rubric B7 "식 그대로의 수치 평가").

---

## 1단계 — 실태 조사

### 1-A. 전 파일 그림 전수 목록 (21개 tikzpicture, figure 환경)

| # | 파일 | 라벨 | 내용 | 역할 | 좌표 성격 |
|---|------|------|------|------|-----------|
| 1 | ch1_sec00_intro | `fig:spine` | 계산 진행 흐름도(N0→N9 노드·식 매핑, 파선=전이 루프) | 문서 전체 spine | 흐름도(도식) |
| 2 | ch1_sec01_n0n1 | `fig:staging` | 흑연 staging 갤러리 채움(위) + 대응 dQ/dV peak(아래, eq:eqpeak 초기값) | "상전이1=peak1" | 아래 패널 수치 |
| 3 | ch1_sec02a_part0 | `fig:sm-reservoir` | grand canonical 저장조 구도 | 대정준 개념 | 도식 |
| 4 | ch1_sec02b_part0 | `fig:sm-gxi` | 정규용액 f(ξ)/RT 가족(Ω=0…3RT) | 이중웰 문턱 | 수치 |
| 5 | ch1_sec02b_part0 | `fig:sm-mu` | 격자기체 μ(θ) 가족(van der Waals loop) | spinodal 씨앗 | 수치 |
| 6 | ch1_sec02b_part0 | `fig:sm-occ` | 점유의 전기화학 재매개변수화 (a)θ(무차원) (b)ξ_eq,θ_eq(V) | logistic 기원 | 수치 |
| 7 | ch1_sec04_hys | `fig:doublewell` | g_j(ξ) 이중웰(Ω=3RT)·불안정 띠 | spinodal 개념 | **정성 개형**(수치는 #4 참조) |
| 8 | ch1_sec04_hys | `fig:hysloop` | 비단조 V_eq(ξ)·과주행·spinodal·gap | 히스 gap 유도 | 수치 |
| 9 | ch1_sec05_width | `fig:barrier` | Eyring 활성화 장벽 (a)평형 (b)구동 | 속도식 출발 | 반응좌표 개형 |
| 10 | ch1_sec05_width | `fig:flux` | 정·역 플럭스 교점 = ξ_eq | detailed balance | 수치 |
| 11 | ch1_sec05_width | `fig:logistic` | ξ_eq와 미분 종의 온도의존(3T)·이중축 | 평형 종·폭 | 수치(고밀도) |
| 12 | ch1_sec07_broadening | `fig:widthbudget` | 폭 예산 waterfall(4단계, 실제 합성곱) | 두-상 broadening | 수치 |
| 13 | ch1_sec07_broadening | `fig:broadening` | (a)연속고용체 (b)두-상 델타→종 | 폭 지위 대조 | 개형 |
| 14 | ch1_sec09_tail | `fig:relaxode` | 지연 완화(target ξ_eq vs lagged ξ_lag) | 기억 적분 | **도식(비수치)** |
| 15 | ch1_sec09_tail | `fig:reversal` | 인과 꼬리 방향(방전·충전 거울) | 방향 반전 | 수치 |
| 16 | ch1_sec11_lcointro | `fig:lco-dirmap` | 충방전 라벨 ↔ 탈리튬화 방향 | LCO 규약 | 도식 |
| 17 | ch1_sec15_lcoelec | `fig:lco-electronic` | MIT-logistic 게이트 g(E_F,x)·\|ΔS_e\| bump | 전자 엔트로피 | 수치 개형 |
| 18 | ch2_sec02_config | `fig:occ_config` | (a)점유분포 (b)S_config(θ) | config 엔트로피 | 인라인 함수 plot |
| 19 | ch2_sec05_mixing | `fig:blend` | 연속 블렌드 vs 계단(빨간=틀림) | 겹침 가중 연속성 | 모식 |
| 20 | appendix | `fig:app-tangent` | f(ξ)/RT 공통접선·binodal·spinodal | 상분리 기하 | 수치 |
| 21 | appendix | `fig:app-phasediag` | 대칭 정규용액 상평형도(binodal/spinodal) | 온도축 상도표 | 수치 |

(표: `\begin{table}`·longtable 는 그림 아님 — 별도. tab:notation·tab:staging·tab:ds·tab:worked·tab:qrev·tab:signcheck-S/R·부록 codemap 표 등.)

### 1-B. 각 그림 부실 진단 (정보밀도·주석·독자기여·시각품질)

**총평**: 기존 21개 그림은 전반적으로 **고품질**이다. 대부분 (i) 실제 모델 식의 수치 평가 좌표, (ii) 캡션에 좌표 성격(식 평가/개형) 명시(B7 준수), (iii) 축·눈금·주석·범례가 촘촘하다. 따라서 FO1 의 무게중심은 "기존 그림 대수술"이 아니라 **그림이 아예 없는 개념 공백 채우기**에 둔다.

- 강함(수정 불요): #2 #4 #5 #6 #8 #10 #11 #12 #15 #17 #18 #20 #21 — 수치·주석 충실.
- 개념 도식(의도적, 유지): #1 #3 #9 #13 #16 #19 — 흐름도/개념 대조라 수치 불요.
- **약함(개형이라 정밀도 낮음, 재설계 후보)**:
  - #7 `fig:doublewell`: "정성 곡선"이라 명시. 수치 정확판(#4 Ω=3RT)이 이미 존재해 재설계 이득 작음 → 후보이나 우선순위 낮음.
  - #14 `fig:relaxode`: 좌표가 "도식 평가"(비수치). 같은 절 #15 `fig:reversal` 는 실제 기억 적분 수치인데, #14 만 도식이라 **정밀도 불균형**. 실제 eq:lag 적분으로 정확화 가능 → 재설계 후보.

### 1-C. 그림 공백 목록 (그림이 없어 이해가 어려운 절/개념)

| 공백 | 절 | 개념/식 | 왜 공백이 아픈가 |
|------|----|---------|------------------|
| **P-1** | ch1_sec03 (N2) | 평형 중심 `U_j(T)=(−ΔH+TΔS)/F` (eq:Uj) | 절 전체가 "중심이 T 에 선형 이동, 기울기 ΔS/F, 부호 갈림"을 말하나 **그림 0**. 다온도 피팅에서 U_j(T)를 온도마다 읽는 이유가 시각화 안 됨. |
| **P-2** | ch1_sec00·sec08 (N7) | 관측 3인자 중 **C-rate**: dQ/dV 가 \|I\|↑ 로 꼬리 늘고 낮아짐 (eq:LV, L_V∝\|I\|) | 서론 "관측"이 문서의 동기인데 **실제 예측 dQ/dV 를 C-rate 별로 겹쳐 보인 그림이 없다**. fig:widthbudget/reversal 은 조각(폭 예산·거울)만. |
| **P-3** | ch2_sec07·sec08 | 가역 발열 SOC **부호 교대**(발열→흡열) (eq:qrev·tab:qrev) | Chapter 2 의 도착 결론(한 종합식이 SOC 축에서 부호를 스스로 뒤집음)이 **표(tab:qrev)로만** 있고 그림 0. 영점 교차·교대가 그림이면 즉시 읽힘. |
| **P-4** | ch2_sec04 | Einstein 진동 `S_vib(T;θ_E)`·중심 이동 `∂ΔU_vib/∂T` (eq:Svib-einstein·eq:dUvib) | 절이 "T_ref 강제 영점 + 로그 곡률"로 electronic(∝T, 원점 통과 선형)과 **식별**된다고 주장하나 두 함수형을 대조한 그림 0 → "3온도점 필요" 논증이 그림 없이 어렵다. |
| P-5 | ch2_sec03·synthesis | 세 분포 ΔS(x) 합성(config +∞/−∞ · vib 음 baseline · electronic bump) | fig:occ_config(config)·fig:lco-electronic(elec)로 조각은 있으나 **합쳐진 ΔS(x)** 한 장 없음. P-3 과 부분 중복. |
| P-6 | ch1_sec06 (N6) | 평형 peak 세 읽기값: 위치=U_j^d·순높이=Q_j/(4w_j)·면적=Q_j (eq:eqpeak) | fig:logistic 이 종을 보이나 "위치·높이·면적" 세 양을 한 종에 주석한 그림은 없음. 우선순위 낮음(중복). |

---

## 2단계 — 프레이밍 (창 소관: 우선순위 top 7 확정)

기존 21개 그림이 이미 고품질이므로 **무게중심 = 개념 공백(신규) 6, 재설계 1**. 우선순위는 (i) 개념 공백의 크기, (ii) 본문 핵심 결론과의 직결성, (iii) 정확 수치 산출 가능성으로 매겼다. ★ = 실제 구현함.

### ★T1 (P-1) — 평형 중심 `U_j(T)` 의 온도 선형 이동  [→ ch1_sec03 §3]
- **무엇을 그리나**: 흑연 staging 4 전이의 `U_j(T)` 를 온도축(258–338 K)에 대해 그린 4 직선 + 각 기울기 `ΔS_rxn,j/F` 주석 + T_ref 값 읽기.
- **왜 이 그림인가**: §3 는 `U_j(T)=(−ΔH+TΔS)/F`(eq:Uj)와 `∂U_j/∂T=ΔS_rxn/F` 를 유도하나 **그림이 0**. 반응 엔트로피 부호가 중심 이동 방향을 가른다는 것(양=상승/영=수평/음=하강)과 "다온도 피팅이 온도마다 U_j 를 따로 읽어야 함"이 한 장에 보인다.
- **설계 스케치**: x=T[K], y=U_j[mV]. 4 직선(굵기/파선/회색으로 구분), T_ref=298.15 세로 강조 띠·점, 기울기 표 주석. 크기 ~7×4.5 cm.

### ★T2 (P-2) — peak 모양의 동역학 지연 `L_V` 가족 (C-rate 갈래)  [→ ch1_sec06 §6 또는 ch1_sec08 §8 말미]
- **무엇을 그리나**: eq:peakshape `(ξ_eq−ξ_lag)/L_V` 를 `L_V/w = 0(평형)·0.5·1.5·3.0` 넷으로 겹쳐, 정점 낮아짐 + 높은 V 꼬리 성장.
- **왜 이 그림인가**: 서론 "관측"의 **C-rate 갈래**(저율·고율에서 꼬리 길어져 겹침)를 실제 예측 곡선으로 보인 그림이 없다. 기본 파라미터에서 `seed_L_V≈1e−8 V`(꼬리 무시)이므로, 정직하게 **무차원 `L_V/w` 가족**으로 eq:peakshape·eq:tail-limit 의 L_V 의존을 시각화. fig:reversal(단일 L_V=1.5w, 방전·충전 거울)과 비중복.
- **설계 스케치**: x=(V−U_j^d)/w[−6..10 비대칭], y=peak[1/w]. L_V=0 점선(대칭 종)→굵은 실선(L_V=3) 진행, 정점 dot, 진행 화살표.

### ★T3 (P-3) — 가역 발열의 SOC 부호 교대 (Chapter 2 도착 결론)  [→ ch2_sec08 §2.8 tab:qrev 부근]
- **무엇을 그리나**: `∂U_oc/∂T(x̄)` 완전식(굵은 실선)·config 몫(파선), 우축 `Q̇_rev/I=−T∂U_oc/∂T`, 영점 교차(x̄₀≈0.68), 표 5 앵커점(+91.5…−64.9 mV), exo/endo 영역.
- **왜 이 그림인가**: Chapter 2 의 climax("한 종합식이 SOC 축에서 흡·발열 부호를 스스로 교대")가 **표(tab:qrev)로만** 존재. 영점 교차 그림이면 즉시 읽히고, config 발산이 고-x̄ upturn 을 끄는 것이 대조로 보인다.
- **설계 스케치**: x=x̄[0.05..0.95], 좌축 ∂U_oc/∂T[mV/K], 우축 Q̇/I[mV](=좌축×−298.15). endo 밴드 음영·영점선.

### ★T4 (P-4) — Einstein 진동 엔트로피와 electronic 식별  [→ ch2_sec04 §2.4]
- **무엇을 그리나**: (a) `S_vib(T;θ_E)/R`(eq:Svib-einstein) 곡선·두 극한, (b) `∂ΔU_vib/∂T`(eq:dUvib, T_ref 강제 영점+곡률) vs electronic ∝T(원점 통과 개형), 4 앵커점(−3.74/0/+3.70/+9.14 μV/K).
- **왜 이 그림인가**: §2.4 는 "T_ref 강제 영점 + 로그 곡률 vs 선형"으로 vib·electronic 이 **식별**되고 "3온도점 필요"라 주장하나 두 함수형 대조 그림이 0.
- **설계 스케치**: 2 패널. (a) x=T[K], y=S_vib/R. (b) x=T[K], y=∂ΔU_vib/∂T[μV/K], vib 실선·electronic 점쇄선.

### T5 (P-5) — 세 분포 합성 `ΔS(x)` (config+vib+electronic)  [프레이밍만]
- **무엇을**: `ΔS(x)=F∂U_oc/∂T` 총합 + config(양끝 ±∞ 발산)·vib(음 baseline)·electronic(LCO bump) 3 분해를 한 축에. **왜**: §2.3·종합식이 "세 분포의 합"을 말하나 합쳐진 ΔS(x) 한 장 없음(fig:occ_config·fig:lco-electronic 은 조각). **미구현 사유**: T3 와 부분 중복(ΔS=F∂U_oc/∂T)이라 T3 우선. 확장 시 T3 에 2 패널로 붙일 수 있음.

### T6 (R-1, 재설계) — `fig:relaxode`(§9)를 정성 도식 → 실제 기억 적분 수치로  [프레이밍만]
- **무엇을**: 현행 fig:relaxode 좌표는 "도식 평가"(비수치). 같은 절 fig:reversal 은 실제 eq:lag 적분 수치라 **정밀도 불균형**. eq:lag 를 수치 적분해 target ξ_eq·lagged ξ_lag·차 r 을 정확 좌표로 재설계(원 정보요소 유실 없이). **미구현 사유**: 원 그림이 이미 개념 전달에 충분하고 신규 공백(T1–T4) 이득이 더 커 후순위.

(P-6 평형 peak 세 읽기값은 fig:logistic 과 중복도 높아 top 에서 제외.)

---

## 3단계 — 구현 (실제 TikZ 4건)

| 파일 | 라벨 | 대상 배치 | 좌표 출처(정확) | 라이브러리 |
|------|------|-----------|------------------|------------|
| `fig_fo1_1_Uj_of_T.tex` | `fig:cand-fo1-1` | ch1_sec03 §3 (eq:Uj 박스 뒤, "수 mV 이동" 문단 근처) | `func_U_j`(GRAPHITE_STAGING_LIT) 식 그대로 | ch1 |
| `fig_fo1_2_crate_tail_family.tex` | `fig:cand-fo1-2` | ch1_sec06 §6 말미 또는 ch1_sec08 §8 말미 | eq:lag 인과 기억 적분 수치(방전, w=1) | ch1 |
| `fig_fo1_3_revheat_soc.tex` | `fig:cand-fo1-3` | ch2_sec08 §2.8 tab:qrev 직전/직후 | `solve_U_oc`→`entropy_coefficient_x`·`reversible_heat_x` | ch2 |
| `fig_fo1_4_vib_einstein.tex` | `fig:cand-fo1-4` | ch2_sec04 §2.4 (eq:dUvib 박스 뒤, 수치 문단 근처) | eq:Svib-einstein·eq:dUvib 닫힌형 수치 | ch2 |

**좌표 검증(문서 자체 구현과 일치)**:
- T1: U_j(298.15)=210.9/139.9/120.3/85.3 mV(2→1 은 본문 0.0853 V 와 일치), 기울기 +0.301/0/−0.052/−0.166 mV/K = ΔS_rxn,j/F.
- T2: L_V=1.5w 정점 0.1955@+1.0w = fig:reversal 의 0.196@+1.01w 와 일치(교차검증).
- T3: 5 앵커 U_oc=43.5/74.4/109.0/148.8/195.2 mV·Q̇_rev/I=+91.5/+60.8/+26.6/−13.2/−64.9 mV = tab:qrev 완전 일치. 완전식/단순식/config @x̄=0.25 = −0.204/−0.134/−0.070 mV/K 일치.
- T4: ∂ΔU_vib/∂T = −3.74/0/+3.70/+9.14 μV/K @278.15/298.15/318.15/348.15 K = 본문 §2.4 수치 일치.

**컴파일 검증**:
- 명령: `xelatex -interaction=nonstopmode -halt-on-error _harness.tex` (하네스 = `\documentclass{article}`+kotex+amsmath+tikz, 라이브러리 `positioning,arrows.meta,calc,fit,backgrounds,decorations.pathreplacing`; pgfplots 미사용).
- 1차: `fig_fo1_4` 의 `\\` 노드에 `align` 미지정 → "missing \item" 오류 1건. → 해당 노드에 `align=left` 추가.
- 최종(`compile_PASS.log`): **EXIT=0, 오류 0, `Output written on _harness.pdf (2 pages)`**. 4 그림 전건 렌더 확인(pg1.png=T1·T2·T3, pg2.png=T4). (미정의 `\eqref`/`\ref` 경고는 하네스 한정 — 실제 문서에서 라벨 해석되므로 오류 아님.)

**물리 가드 확인**: 전 그림 본문 식과 부호·극한·단위 일치, 새 물리 주장 없음.
- T1 기울기 ΔS/F 부호(발열 ΔH<0·양의 ΔS 상승) 일치. T2 방전 꼬리 높은 V·평형 종 정점 1/(4w)·면적 Q_j 보존. T3 ∂U_oc/∂T<0⇒Q̇_rev>0 발열(eq:qrev·I>0 방전). T4 저온 S_vib→0·T_ref 영점.

**본문 제안 배치**: 위 표 "대상 배치" 열. 라벨 `fig:cand-fo1-N` 은 기존 라벨과 무충돌(기존 = fig:spine/staging/sm-*/doublewell/hysloop/barrier/flux/logistic/widthbudget/broadening/relaxode/reversal/lco-*/occ_config/blend/app-*).

**구현 결과**: 프레이밍 **7건**(P-1~P-4·P-5·R-1·+P-6 검토제외 명시), 구현 **4건**, 컴파일 **전건 통과**.
