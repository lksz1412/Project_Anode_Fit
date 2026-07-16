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

## 2단계 — 프레이밍 (아래 append)
## 3단계 — 구현 (아래 append)
