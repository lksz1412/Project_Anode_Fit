# FRAMING_FF3 — v1.0.20 그림/그래프 경쟁 저작 (창 FF3)

- 대상: `_sections/ch1_*.tex`(24) · `_sections/ch2_*.tex`(15) · `appendix_phase_separation.tex`
- 원본 무수정. 산출물은 본 폴더의 `fig_ff3_<n>_<주제>.tex` 완결 조각 + 컴파일 하네스.
- 프리앰블 확인 결과(사용 가능 tikz 라이브러리):
  - Ch1: `positioning, arrows.meta, calc, fit, backgrounds` (pgfplots 없음)
  - Ch2: `calc, arrows.meta, decorations.pathreplacing, positioning` (**backgrounds·fit 없음**)
  - Appendix: `arrows.meta, calc, backgrounds` (**positioning·fit 없음**)
  - → 조각별로 해당 문맥의 라이브러리만 사용. 곡선은 전부 `plot coordinates` 하드코딩(python 평가).

---

## 1단계 — 실태 조사

### 1-A. 기존 그림 전수 목록 (figure 환경 21개 = tikzpicture 21개)

| # | 파일 : 라벨 | 내용 | 역할 | 진단 |
|---|---|---|---|---|
| 1 | ch1_sec00 : `fig:spine` | N0–N9 계산 진행 박스 흐름도 | 문서 개관 | 양호 — 식 참조 연결·loop 브래킷까지 정보밀도 높음 |
| 2 | ch1_sec01 : `fig:staging` | staging 갤러리 채움(위) + 4전이 dQ/dV 峰 수치평가(아래) | "상전이=peak" 도입 | 양호 — 위/아래 축 스케일 차이를 캡션이 명시. 단 아래 峰은 w 폴백(0.020/…/0.012 V) 기준이라 실제 초기 상태(n=1, w=RT/F 균일 — §10)와 다른 폭 관행 |
| 3 | ch1_sec02a : `fig:sm-reservoir` | 계–저장조 에너지·입자 교환 상자도 | 대정준 구도 | 단순하지만 목적 부합 |
| 4 | ch1_sec02b : `fig:sm-gxi` | f(ξ)/RT 가족(Ω=0,1,2,2.5,3RT)+spinodal 점 | 볼록성 문턱 | 양호 — 식 그대로 수치 평가 |
| 5 | ch1_sec02b : `fig:sm-mu` | (μ−μ⁰)/RT 가족(Ω=0,2,4RT), vdW loop·spinodal | 비단조성 | 양호 |
| 6 | ch1_sec02b : `fig:sm-occ` | (a) θ(무차원, 3T) (b) ξ_eq·θ_eq(V, 3T) | 점유↔전기화학 결선 | 양호 |
| 7 | ch1_sec04 : `fig:doublewell` | 이중웰 g(ξ) 정성 개형 + g''<0 음영 | spinodal 불안정 띠 | 보통 — fig:sm-gxi 의 Ω=3RT 곡선의 정성 복제임을 캡션이 자인. 고유 정보는 음영 띠뿐 |
| 8 | ch1_sec04 : `fig:hysloop` | V_eq(ξ) 비단조(Ω=4RT)+과주행 굵은 경로+gap 치수 | gap 상한 유도 | 우수 — 정량 좌표·Maxwell 선·불안정 띠 |
| 9 | ch1_sec05 : `fig:barrier` | Eyring 반응좌표 (a)평형 (b)구동(χ 분할) | 속도식 출발점 | 양호 — 모형 퍼텐셜 수치 평가·장벽 치수 |
| 10 | ch1_sec05 : `fig:flux` | 정·역 플럭스 직선 교점(𝒜/RT=0,ln2,2ln2) | 정지점=logistic | 양호 |
| 11 | ch1_sec05 : `fig:logistic` | ξ_eq + 미분 종(3온도) 이중축·FWHM | 폭 w=nRT/F 의 의미 | 우수 |
| 12 | ch1_sec07 : `fig:widthbudget` | 폭 예산 waterfall(델타→②→②⊗③ 실제 합성곱→+①꼬리) | broadening 예산 | 우수 — 근사 한계까지 캡션에 명시 |
| 13 | ch1_sec07 : `fig:broadening` | (a)연속 고용체 종 (b)두-상 델타→치우친 종 | 폭 지위 대조 | 보통 — 곡선 좌표가 손그림(모식)인데 캡션에 개형/모식 표기가 없음(규범 B7 관점 약점). 정량 보완은 #12 가 이미 담당 |
| 14 | ch1_sec09 : `fig:relaxode` | 목표 ξ_eq vs 지연 ξ_lag + r 화살표 | 기억 적분 개념 | **부실** — 캡션 스스로 "도식 평가". 세로축 ξ 가 암묵적으로 0→2 스케일(진행률 0–1 규약과 시각 충돌·눈금 없음), 실제 식~(eq:lag) 적분 평가 아님. 문서 관행(실수치 평가)에 미달 |
| 15 | ch1_sec09 : `fig:reversal` | 방전/충전 peak shape 거울(실적분 수치) | 방향 반전 | 우수 |
| 16 | ch1_sec11 : `fig:lco-dirmap` | 라벨↔탈리튬화↔σ_d 슬롯 매핑 상자 | 방향 규약 | 양호 |
| 17 | ch1_sec15 : `fig:lco-electronic` | g(E_F,x) 게이트 + \|ΔS_e\| bump | MIT 게이트 | 보통 — y 축이 임의 스케일(게이트 높이 2.6 유닛), 본문 정량값(골 깊이 −46 J/(mol·K)·g_max=13 e/eV/atom)이 축에 없음. x 축은 x 감소 방향 재매핑이라 초독자 혼란 여지 |
| 18 | ch2_sec02 : `fig:occ_config` | (a) ⟨n⟩ logistic (b) S_config(θ) | 분포→엔트로피 | 양호 — 단 Ch2 조각 중 유일하게 TikZ 내장 수식 plot(domain) 사용(관행과 다름), 색상(파랑/빨강) 사용 |
| 19 | ch2_sec05 : `fig:blend` | 연속 블렌드 vs 계단(빨강) 모식 | 겹침 가중 개념 | **부실** — 캡션 자인: "모식 — 부호·하강 순서는 임의·흑연 실제 프로파일은 상승 방향". Ch2 의 중심 결과(실측급 비선형 ∂U_oc/∂T(x) 자동 생성·175점 수치검증·tab:qrev 부호 교대)를 받쳐 줄 **실 파라미터 곡선 그림이 문서 전체에 없음** |
| 20 | appendix : `fig:app-tangent` | f(ξ)/RT 현·공통접선·binodal/spinodal·영역 음영 | 공통접선 | 우수 |
| 21 | appendix : `fig:app-phasediag` | T/T_c–ξ binodal·spinodal 상평형 그림 | 종합 | 우수 |

### 1-B. 그림이 없어 이해가 어려운 절/개념 공백

| 코드 | 위치 | 공백 내용 | 절실도 |
|---|---|---|---|
| G-A | Ch1 §3 (N2) | U_j(T) 온도 이동 — 4전이 기울기 ΔS/F 의 부호·크기 차이(+0.301…−0.166 mV/K)가 수치로만 존재 | 중 |
| G-B | Ch1 §8 (N7) | **L_V 의 정량 거동** — 서론 관측("저온·고율일수록 꼬리가 길어짐")을 닫는 노드인데 그림 0. eq:Lqfull 의 (T, ΔH_a, \|I\|) 의존과 §10 의 "가시적 꼬리 ≈ 80 kJ/mol 급" 문턱이 시각화 안 됨 | **상** |
| G-C | Ch1 §4·§13 | **ΔU^hys 닫힌꼴(eq:dUhys)의 거동** — Ω≤2RT 에서 gap=0, T→T_c 에서 (T_c−T)^{3/2} 연속 소멸, 도핑 억제(eq:lco-dope)까지 같은 식인데 곡선 없음 | **상** |
| G-D | Ch1 §10 (N9) | **최종 합산 곡선** — eq:sum 의 산출물(배경+4峰 전체 dQ/dV)이 문서 어디에도 없음(fig:staging 하단은 개별 峰·§1 위치·다른 폭 관행). 온도를 바꿀 때 峰들이 서로 다른 방향으로 움직이는 것(ΔS 부호)도 미시각화 | **상** |
| G-E | Ch1 §12–16 | LCO 3峰 곡선 — 단 Q_j^cat 미배정(표에 용량 열 없음)이라 임의 수치 창작 위험 → 보류 | 하 |
| G-F | Ch1 §15·Ch2 §2.4 | 식별 신호 — 전자항 T² 곡률 vs Einstein 로그 곡률 vs 선형 | 중 |
| G-G | Ch2 §2.5–2.8 | **실 파라미터 ∂U_oc/∂T(x̄) 전 구간 프로파일** — 완전식(eq:complete) vs 단순식(eq:weighted), 4단계 ΔS⁰/F 레벨, 부호 교대(tab:qrev 5점)가 표·문장으로만 존재. fig:blend(모식)의 자리 | **상** |
| G-H | Appendix §A.6 | 핵생성 장벽 ΔG(r) 곡선(표면 +r² vs 부피 −r³, r*·ΔG*) — 텍스트 전용 | 중 |
| G-I | Ch2 §2.4 | S_vib(T;θ_E) 닫힌형·두 극한(고전 로그/저온 동결)·ΔU_vib 편차의 수치(−3.74/0/+3.70/+9.14 μV/K) | 중 |

---

## 2단계 — 프레이밍 (우선순위 top 7)

> 각 항목: [무엇 → 왜(어느 식/개념) → 설계 스케치]. F1–F5 구현 확정, F6·F7 여유 시 구현.

**F1. (신규·최우선, Ch2) 실 파라미터 ∂U_oc/∂T(x̄) 프로파일 — `fig:cand-ff3-1`**
- 무엇: Ch1 4-전이 staging 초기값(U_j(T)=(−ΔH+TΔS)/F 정합값·Q_j·ΔS⁰_j·w=RT/F, n=1)으로 전하 보존 음함수 eq:implicit 를 풀어 완전식 eq:complete 의 ∂U_oc/∂T(x̄) 를 전 구간(x̄=0.02–0.98) 수치 평가. 단순식(중심값 가중 eq:weighted) 곡선을 함께 겹침. 4개 ΔS⁰_j/F 레벨 점선 + "계단(오답)" 대비선 유지(fig:blend 정보요소 계승) + tab:qrev 5점 마킹 + 부호 교대(발열↔흡열) 영역 표기.
- 왜: Ch2 의 중심 주장 — "전이당 상수 ΔS⁰ + 분포만으로 측정급 비선형이 자동 생성된다"(§2.5 파생 A·수치검증 srcbox·§2.8 tab:qrev) — 를 받치는 실곡선 그림이 전무. fig:blend 는 모식이고 방향까지 실제와 반대라고 캡션이 자인. 이 한 장이 eq:weighted·eq:complete·eq:single_config·tab:qrev 를 한 축 위에 통합.
- 스케치: 가로 x̄(0→1, 탈리튬화), 세로 ∂U_oc/∂T [mV/K] (−0.45…+0.45). 굵은 실선=완전식, 회색 실선=단순식, 점선 수평 4개=ΔS⁰_j/F(+0.301/0/−0.052/−0.166), 빨간 파선=계단(비중 지배 전이 스위칭), 검은 점 5개=tab:qrev 행, y=0 기준선과 발열/흡열 라벨. Ch2 라이브러리만 사용(backgrounds 금지 → 음영 대신 기준선·라벨).

**F2. (신규, Ch1 §8) 지연 길이 지도 log₁₀L_V(ΔH_a; T) — `fig:cand-ff3-2`**
- 무엇: eq:Lqfull·eq:LV 를 기본값(χ=0.5, ΔS_a=0, 𝒜=A_cap RT=4RT, n=1, \|dV/dq\|=0.30 V, C/10, Q_cell=1 정규화 — §10 c-rate 숫자 규약)으로 평가한 log₁₀ L_V vs ΔH_a 직선 3개(T=268/298/328 K) + 가시성 문턱 L_V=w=RT/F 수평선 + 교차점(≈70/78/86 kJ/mol) + 표~tab:staging 초기값 ΔH_a(40–48 kJ/mol) 창 표시 + "×20 (C/10→2C): +1.3 decade" 수직 화살표(L_V∝\|I\|).
- 왜: 서론의 관측 (a)온도 (b)C-rate 가 꼬리로 들어오는 자리가 N7 인데 그림이 없다. §10 의 두 정량 서술 — "초기값에서 L_V=10⁻¹⁰–10⁻⁸ V 로 평형 종 전용" · "가시적 꼬리에는 ΔH_a≈80 kJ/mol 급 필요" — 가 이 지도에서 눈으로 확인된다(지수 함수라 로그 축이 유일하게 정보를 살림).
- 스케치: 가로 ΔH_a 20–100 kJ/mol, 세로 log₁₀(L_V/V) −12…0. 반대수에서 eq:Lqfull 은 직선(기울기 1/(RT ln10)) — 저온일수록 가파름. 문턱선 위 = 꼬리 가시 영역 라벨. Ch1 라이브러리만.

**F3. (신규, Ch1 §10) 합산 곡선 — 배경+4峰 전체 dQ/dV, 두 온도 — `fig:cand-ff3-3`**
- 무엇: eq:sum 을 초기 상태 그대로(평형 종 전용: L_V→0·γ=0·R_n=0, w_j=RT/F 균일, C_bg=0.05 Q_cell/V 상수 예시) 268.15 K 와 328.15 K 에서 전 구간 평가해 겹침. 개별 전이 기여(298 K 가늘게)와 총합(굵게)을 함께. 각 峰 중심의 온도 이동 화살표(4→3: +0.301 mV/K → 오른쪽 / 2→1: −0.166 mV/K → 왼쪽)와 U_j(T) 산식 주석.
- 왜: 문서의 도착점("이 문건만 보고 같은 곡선을 재현")인 eq:sum 의 산출물 전체 곡선이 없다. 동시에 N2(중심 온도 이동·ΔS 부호별 반대 방향)·N4(폭 ∝T)·N9(배경 위 선형 누적)를 한 장에 통합 — G-A 공백도 흡수.
- 스케치: 가로 V 0.03–0.28 V, 세로 dQ/dV [Q_cell/V] 0–5.5. 실선=268 K 총합, 파선=328 K 총합, 얇은 회색=298 K 전이별 기여+배경 수평선. 중심 이동 화살표 2개(부호 반대 강조). Ch1 라이브러리만.

**F4. (재설계, Ch1 §9 `fig:relaxode`) 기억 적분의 실수치 완화 — `fig:cand-ff3-4`**
- 무엇: 기존 도식을 실제 수치로 재설계 — 목표 ξ_eq(q)=logistic(폭 w_q=0.35, 중심 q=1.2), ξ_lag(q)=eq:lag 의 인과 기억 적분(L_q=0.4)을 python 정적분으로 평가해 하드코딩. 원 그림의 정보 요소 전부 보존(목표 파선·지연 실선·차 r 화살표·수직 점선·"peak shape=(ξ_eq−ξ_lag)/L_V" 주석) + 추가: ξ∈[0,1] 실축 눈금, 지수 커널 e^{−(q−u)/L_q} 스케치(평가점 1.8 아래 음영)로 "길이 L_q 만큼의 최근 과거만 기억"을 시각화, r 최대점 좌표.
- 왜: 유일하게 기억 적분(eq:lag)을 설명하는 그림이 "도식 평가"이고 세로축이 암묵 0→2 라 진행률 규약(0–1)과 시각 충돌. 문서 관행(실수치 평가·rubric B7)에 맞춰 승격.
- 스케치: 가로 q 0–3.4, 세로 ξ 0–1(눈금 0/0.5/1). 커널 음영은 backgrounds 레이어. Ch1 라이브러리만.

**F5. (신규, Ch1 §4↔§13 공용) 히스 gap 닫힌꼴의 거동 — `fig:cand-ff3-5`**
- 무엇: eq:dUhys 2패널. (a) T=298.15 K 고정, ΔU^hys vs Ω(0–14 kJ/mol): 문턱 2RT≈4.958 kJ/mol 에서 0 으로 연속 발아((Ω−2RT)^{3/2} — Taylor 박스의 양수 소멸), 표~tab:staging 초기값 Ω=6/8/10/13 kJ/mol 4점 마킹(6.2/23.6/50.4/102.7 mV). (b) Ω 고정 3곡선(6/8/13 kJ/mol), ΔU^hys vs T(250–800 K): 각자 T_c=Ω/2R 에서 (T_c−T)^{3/2} 로 소멸 — 도핑 억제(eq:lco-dope: Ω↓ ⇒ 같은 T 에서 gap↓)와 온도 상승에 의한 히스 축소가 한 그림.
- 왜: gap 의 닫힌꼴은 Ch1 §4 의 핵심 박스이자 LCO §13(eq:lco-dUhys·eq:lco-dope)이 재사용하는 구조식인데 함수 거동 곡선이 없다. "Ω≤2RT 면 정확히 0" 분기·임계 연속성·γ_j 가 깎는 상한이라는 지위가 한눈에 들어옴.
- 스케치: (a) 가로 Ω [kJ/mol], 세로 ΔU^hys [mV](0–110), 문턱 수직 점선+음영 없음. (b) 가로 T [K], 세로 [mV], T_c 3점 마킹. Ch1 라이브러리만.

**F6. (신규·여유 시, Ch2 §2.4) Einstein 진동 보정 — `fig:cand-ff3-6`**
- 무엇: (a) S_vib(T;θ_E=700 K)/R 닫힌형(eq:Svib-einstein, 50–1000 K) + 고전 극한 R[1+ln(T/θ_E)] 파선 + 저온 동결. (b) ∂ΔU_vib/∂T=ΔS_vib(T)/F [μV/K] (268–348 K): 본문 4수치(−3.74/0/+3.70/+9.14) 점 마킹, T_ref 강제 영점 표시, 전자항 형(선형 ∝T, 영점 없음) 대비선.
- 왜: §2.4 는 수치는 있는데 곡선이 없고, 식별 논거(3온도점 필요)가 함수형 비교인데 시각 부재(G-F·G-I).
- 스케치: 2패널 나란히. Ch2 라이브러리만.

**F7. (신규·여유 시, Appendix §A.6) 고전 핵생성 장벽 — `fig:cand-ff3-7`**
- 무엇: 무차원 ΔG(r)/ΔG* = 3(r/r*)²−2(r/r*)³ 곡선 + 표면항 +3(r/r*)² · 부피항 −2(r/r*)³ 가는 곡선 + (r*, ΔG*) 마킹.
- 왜: §A.6 이 핵생성 vs spinodal 분해를 텍스트로만 설명(G-H). 준안정 영역의 "유한 요동 필요"가 이 곡선 하나로 선명해짐.
- 스케치: 가로 r/r* 0–1.6, 세로 ΔG/ΔG* −1…1.1. Appendix 라이브러리만(arrows.meta·calc·backgrounds).

### 라벨·배치 계획
| 조각 | 라벨 | 제안 배치 |
|---|---|---|
| fig_ff3_1_dUdT_profile.tex | fig:cand-ff3-1 | Ch2 §2.5 fig:blend 자리 대체 또는 §2.8 tab:qrev 직후(권장: §2.8) |
| fig_ff3_2_LV_map.tex | fig:cand-ff3-2 | Ch1 §8.4 (eq:LV 박스 뒤) |
| fig_ff3_3_sum_curve.tex | fig:cand-ff3-3 | Ch1 §10 표~tab:staging 뒤 |
| fig_ff3_4_relaxode.tex | fig:cand-ff3-4 | Ch1 §9.1 기존 fig:relaxode 대체 |
| fig_ff3_5_hysgap.tex | fig:cand-ff3-5 | Ch1 §4.2 eq:dUhys 뒤(§13 에서 재참조 가능) |
| fig_ff3_6_einstein.tex | fig:cand-ff3-6 | Ch2 §2.4.3 |
| fig_ff3_7_nucleation.tex | fig:cand-ff3-7 | Appendix §A.6.1 |

(3단계 기록은 구현·컴파일 후 append)
