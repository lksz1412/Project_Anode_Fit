# FRAMING_FF2 — v1.0.20 그림/그래프 경쟁 저작 (창 FF2)

- 대상: `_sections/ch1_*.tex`(24) · `_sections/ch2_*.tex`(15) · `appendix_phase_separation.tex`
- 원본 수정 없음. 산출물은 본 폴더(`results/comp_P7_figs/FF2/`) 한정.
- 규약: pgfplots 미로드 확인 → plot coordinates 방식. 곡선 좌표는 python 수치 평가 후 하드코딩.

---

## 1단계 — 실태 조사

### 1.1 preamble 가용 자원 (구현 제약 확정)

| 문서 | tikz 라이브러리 | 비고 |
|---|---|---|
| ch1 (`ch1_preamble.tex`) | `positioning, arrows.meta, calc, fit, backgrounds` | pgfplots 없음. 그림은 전부 그레이스케일 관행 |
| ch2 (`ch2_preamble.tex`) | `calc, arrows.meta, decorations.pathreplacing, positioning` | pgfplots 없음. **backgrounds 없음** (ch2 조각에서 `on background layer` 사용 금지). 기존 그림에 blue/red 사용 관행 있음 |
| appendix (자체 preamble) | `arrows.meta, calc, backgrounds` | 독립 컴파일 |

### 1.2 기존 그림 전수 목록 (21건) + 진단

기호: [정량]=식 그대로의 수치 평가 명시, [개형]=정성/모식 선언 있음, [무표기]=수치/모식 지위 선언 없음(rubric B7 위반 소지).

| # | 파일:라벨 | 내용/역할 | 진단 |
|---|---|---|---|
| 1 | ch1_sec00 `fig:spine` | 계산 진행 N0→N9 흐름도 | 양호. 노드↔식 매핑 포함, 정보 밀도 적정 |
| 2 | ch1_sec01 `fig:staging` | staging 갤러리 도식(위)+실제 dQ/dV 4-peak(아래)[정량] | 양호. 범주축/전위축 비정렬 주의문까지 있음 |
| 3 | ch1_sec02a `fig:sm-reservoir` | grand canonical 계·저장조 상자 도식 | **저밀도**: 상자 2 + 화살 2 뿐. Gibbs 인자 지수 구조·두 교환 채널의 결과(Boltzmann vs Gibbs)가 그림에 없음. 개선 후보(하위) |
| 4 | ch1_sec02b `fig:sm-gxi` | f(ξ)/RT 가족 Ω=0…3RT [정량] | 양호. spinodal 점 표기 |
| 5 | ch1_sec02b `fig:sm-mu` | μ(θ) 가족 0/2RT/4RT [정량] | 양호. van der Waals loop·±1.066 |
| 6 | ch1_sec02b `fig:sm-occ` | (a) θ(ε−μ) 3온도 (b) ξ_eq(V)·θ_eq(V) [정량] | 양호 |
| 7 | ch1_sec04 `fig:doublewell` | 이중웰 g(ξ) Ω=3RT [개형 선언] | 정성 곡선이지만 fig:sm-gxi 로 교차 참조되어 허용 수준. 재설계 우선순위 낮음 |
| 8 | ch1_sec04 `fig:hysloop` | 비단조 V_eq(ξ)·과주행·gap 2.131RT/F [정량] | 우수. 단 **gap 의 Ω(또는 T) 의존 — 문턱·임계 소멸·Taylor 함정·도핑 축소 — 는 어느 그림에도 없음** → 신규 후보 |
| 9 | ch1_sec05 `fig:barrier` | Eyring 활성화 장벽 (a)평형 (b)구동 [정량(모형 퍼텐셜)] | 양호 |
| 10 | ch1_sec05 `fig:flux` | 정·역 플럭스 교점 → ξ_eq [정량] | 양호 |
| 11 | ch1_sec05 `fig:logistic` | ξ_eq+미분 종 3온도, FWHM [정량] | 우수 |
| 12 | ch1_sec07 `fig:widthbudget` | 폭 예산 waterfall(delta→②→②⊗③→+①) [정량, 실제 합성곱] | 우수. 근사 한계까지 캡션에 명시 |
| 13 | ch1_sec07 `fig:broadening` | (a)연속 고용체 vs (b)두-상 broadening [무표기] | **좌표 임의 스케치인데 캡션에 개형/모식 선언이 없음**(B7). 정보 자체는 fig:widthbudget 과 부분 중복. 재설계 후보(중위) |
| 14 | ch1_sec09 `fig:relaxode` | 목표 ξ_eq vs 지연 ξ_lag, r 정의 [캡션에 '도식 평가' 명시] | 도식 지위 선언은 있으나 실측식 평가 아님. fig:reversal 이 정량을 담당하므로 우선순위 중하 |
| 15 | ch1_sec09 `fig:reversal` | 방전/충전 인과 꼬리 거울(peak shape 수치 적분) [정량] | 우수. 단 **L_V 크기 변화(온도·전류 의존)가 peak 를 어떻게 바꾸는지, 꼬리가 이웃 peak 와 겹치는 관측 핵심은 그림 없음** → 신규 후보 |
| 16 | ch1_sec11 `fig:lco-dirmap` | 충방전 라벨↔탈리튬화↔σ_d 슬롯 도식 | 양호(규약 그림) |
| 17 | ch1_sec15 `fig:lco-electronic` | g(E_F,x) 게이트 + \|ΔS_e\| bump [정량(게이트 식 평가)] | 대체로 양호. 단 y 축 눈금 없음(‘g_max’ 한 점만), **전자항의 관측 신호(∂U/∂T 의 T-선형, U(T) 의 T² 곡률·고온 외삽 하락)는 그림 없음** → 신규 후보 |
| 18 | ch2_sec02 `fig:occ_config` | (a) ⟨n⟩ logistic (b) S_config(θ) | 보통. (b)에서 본문이 강조하는 **부분몰 ∂S_config/∂θ=−R ln[θ/(1−θ)] 의 ±∞ 발산이 곡선으로 없음**(텍스트 화살표 주석뿐) → 재설계 후보 |
| 19 | ch2_sec05 `fig:blend` | 연속 블렌드 vs 계단 [모식 선언 있음] | 모식 지위는 명시. 그러나 파생 A 의 **수치 검증(175점)·실제 4-전이 프로파일(−16→−5→0→+29 상승·부호 교대)이 그림으로 없음** — 장 전체의 실계산 곡선 부재가 최대 공백 → 신규 후보(최상위) |
| 20 | appendix `fig:app-tangent` | 공통접선·binodal·spinodal [정량] | 우수 |
| 21 | appendix `fig:app-phasediag` | binodal/spinodal 상평형도 [정량] | 우수 |

### 1.3 그림이 없어 이해가 어려운 절/개념 공백

| 공백 | 위치 | 왜 그림이 필요한가 |
|---|---|---|
| G-A. **실계산 ∂U_oc/∂T(x̄) 곡선 (완전식 vs 단순식)** | ch2 §2.5(파생 A·B)·§2.8(종합식·tab:qrev) | 장의 중심 주장 "상수+분포만으로 측정급 비선형 자동 생성"이 수치 서술(175점 검증·계산 예제·5점 표)로만 존재. 연속 블렌드·config 발산·부호 교대를 실제 staging 파라미터 곡선으로 보여야 표·예제가 한눈에 닫힘 |
| G-B. **가역 발열 Q̇_rev/I(x̄) 의 SOC 흡·발열 교대** | ch2 §2.7–2.8(tab:qrev) | 표의 5점(+91.5…−64.9 mV)이 곡선 없이 나열됨. 발열→흡열 반전점 시각화가 Bernardi 출구의 핵심 |
| G-C. **히스 gap ΔU^hys 의 문턱 곡선** | ch1 §4.2(eq:dUhys·Taylor 함정)·§13(eq:lco-dope 도핑) | 문턱 Ω=2RT 에서 0, u³ 양수 소멸, 상수 대입 시 음수 오답, 도핑 축소 — 전부 장문의 텍스트로만 존재. gap(Ω) 한 곡선이 세 문단을 동시에 닫음 |
| G-D. **L_V 성장에 따른 peak 변형·이웃 peak 겹침** | ch1 §8(N7 — 그림 0건)·§9·서론 관측 | 서론 관측의 핵심("저온·고율일수록 꼬리가 길어져 다음 peak 와 겹침")이 어느 그림에도 없음. fig:reversal 은 L_V=1.5w 한 값·단일 전이뿐 |
| G-E. **전자항 U_1(T) 의 T² 곡률 식별 신호** | ch1 §15(eq:U1T2)·§12(Kirchhoff)·§17(동결 근사) | "고온 외삽이 선형 외삽보다 낮아진다"는 식별 신호와 (기저 선형/동결 선형/적분형 T²) 세 모델 층위가 그림 없이 서술만 존재 |
| G-F. **Einstein S_vib(T;θ_E) 닫힌형과 두 극한 + ΔU_vib 강제 영점** | ch2 §2.4(그림 0건) | 신설 절 전체가 무그림. 고전 로그 극한·저온 동결·T_ref 강제 영점(−3.74/0/+3.70/+9.14 μV/K)·electronic(∝T) 과의 함수형 분리가 곡선으로 필요 |
| G-G. U_j(T) 4-전이 직선(중심의 온도 이동) | ch1 §3 | ΔS 부호가 기울기를 정하는 것 — 보조적(우선순위 하) |
| G-H. ΔS 삼분해 슬롯의 x-프로파일 | ch1 §14 | 표·수식으로 대체 가능 — 보조적(우선순위 하) |

---

## 2단계 — 프레이밍 (우선순위 top 7)

선정 기준: (i) 문서 핵심 주장(관측·파생·식별 신호)의 시각 공백 크기, (ii) 절 단위 그림 0건 여부, (iii) 본문 수치 anchor 로 검산 가능한 실평가 곡선인가.

### FF2-1. [신규·최상위] 실계산 ∂U_oc/∂T(x̄) + 가역 발열 Q̇_rev/I(x̄) — 2패널 (G-A+G-B)
- **무엇을**: Chapter 1 staging 4-전이 파라미터(표 tab:staging 의 ΔH·ΔS·Q, w=RT/F, 298.15 K)로 전하 보존 음함수를 풀어 얻은 (a) ∂U_oc/∂T(x̄) — 완전식(eq:complete, 실선)과 단순식(eq:weighted, 파선), 전이별 수준선 ΔS⁰_j/F, tab:qrev 5점 anchor — 과 (b) Q̇_rev/I=−T·∂U_oc/∂T — 발열/흡열 영역과 부호 반전점.
- **왜**: 파생 A(연속 블렌드)·파생 B(config 항 = 완전−단순 잔차)·§2.8 계산 예제(−0.204/−0.134 mV/K)·tab:qrev(부호 교대)를 한 그림이 전부 실증. ch2 의 유일한 곡선 그림(fig:blend)이 모식에 머무는 공백을 해소.
- **설계**: 가로 x̄∈[0.05,0.95]. (a) 좌축 mV/K(−0.45…+0.45), 완전식 blue 실선(기존 fig:blend 관행)·단순식 black 파선·수준선 dotted(+0.301/0/−0.052/−0.166)·anchor 5점(●, tab:qrev 값)·0선. (b) 좌축 mV(−100…+120), 곡선 실선·anchor 5점·+발열/−흡열 라벨. 캡션: 좌표는 식 그대로의 수치 평가, w 열적 서식 전제(단순식이 보수 기준) 한정 재인용.
- **배치 제안**: ch2 §2.8 표 tab:qrev 옆(§ssec:qrevtab).

### FF2-2. [신규] 히스테리시스 gap ΔU^hys 의 문턱·임계 소멸·Taylor 함정·도핑 (G-C)
- **무엇을**: ΔU^hys(Ω)=(2/F)[Ωu−2RT artanh u] vs Ω/RT (298.15 K). 정확 곡선 + 문턱 근방 양수 점근 (8RT/3F)u³ + 상수-대입 오답 −(4RT/3F)u³(음수, '함정' 표기) + 흑연 4-전이 초기값 Ω 위치 표식 + 도핑 화살표(Ω→2RT⁺ ⇒ gap→0).
- **왜**: §4.2 의 boxed gap·★Taylor 함정 문단·§13 의 eq:lco-dope 가 전부 텍스트. Ω=4RT 에서 54.8 mV(fig:hysloop 와 동일값)로 기존 그림과 정합 검산까지 됨.
- **설계**: x=Ω/RT 0…5.6, y=gap[mV] −15…110. 회색 음영 Ω≤2RT(gap=0 구간), 정확 곡선 thick, 점근 dashed, 함정 dotted(0 아래), 표식 4점(6.2/28.3/56.0/102.7 mV), γ_j 축소 안내 화살표. 그레이스케일(ch1 관행).
- **배치 제안**: ch1 §4.2 식 eq:dUhys 아래(또는 §13.5 도핑 절에서 재참조).

### FF2-3. [신규] 지연 길이 L_V 가 peak 를 바꾸는 방식 — 꼬리 성장과 이웃 peak 겹침 (G-D)
- **무엇을**: (a) 단일 전이 peak shape (ξ_eq−ξ_lag)/L_V 를 L_V/w=0(평형 종)·0.75·1.5·3 에서 — 정점 하락·중심 이동·꼬리 연장. (b) 두 전이(간격 6w, 동일 Q)의 합성 곡선을 L_V=0.3w vs 3w 에서 — 꼬리가 이웃 peak 와 겹쳐 골이 메워지는 것.
- **왜**: 서론 '관측'의 셋째 축(C-rate·저온 → 꼬리 연장·겹침)이 그림 부재. §8(N7)은 그림 0건. L_V∝\|I\|·Arrhenius(T) 인과는 §8 식으로, 그 결과 모양은 본 그림으로 분업.
- **설계**: (a) x=(V−U)/w −6…10, y=peak[1/w] 0…0.27, 평형 종 dotted(정점 0.25), L 별 실선/파선(정점 좌표 주석: fig:reversal 의 (+1.01w, 0.196) 재현 포함). (b) x −5…14, 두 성분 thin + 합 thick, L 두 경우 대비, "L_V↑ ⇒ 겹침" 주석. 인과 기억 적분의 점별 수치 평가(방전 분기).
- **배치 제안**: ch1 §9 fig:reversal 다음(또는 §8 끝).

### FF2-4. [신규] LCO 전자항의 U_1(T) — T² 곡률 식별 신호 (G-E)
- **무엇을**: U_1(T)−U_1(T_ref) [mV] vs T(268…348 K) 세 층위 — (i) 기저 선형(전자항 없음, ΔS_0=+80 J/mol K 대표 스케일), (ii) 현행 동결 근사(선형, 기울기 (ΔS_0+ΔS_e(T_ref))/F), (iii) 적분형 T²(eq:U1T2, a_e=−0.1532 J/mol K² — 게이트 중심 닫힌식 그대로). 고온에서 (iii)<(i) 하락 gap 주석 = "식별 신호".
- **왜**: §15 ★T² 누적계수 문단·§12 Kirchhoff 적분형·§17 동결 근사의 3-층위가 서술로만 존재. 다온도 피팅 설계의 핵심 신호.
- **설계**: x=T[K] 268…348(T_ref=298.15 수직 점선), y=ΔU[mV] −30…+45. (i) dotted, (ii) dashed, (iii) thick 실선. 끝점 기울기 주석(0.403/0.276 mV/K). 그레이스케일.
- **배치 제안**: ch1 §15 식 eq:U1T2 아래.

### FF2-5. [신규] Einstein 진동 엔트로피 닫힌형과 중심 이동의 강제 영점 (G-F)
- **무엇을**: (a) S_vib(T;θ_E)/R vs T/θ_E — 닫힌형(eq:Svib-einstein), 고전 극한 1+ln(T/θ_E) dashed, 저온 동결 →0; θ_E=700 K·298 K 작동점 표식. (b) ∂ΔU_vib/∂T [μV/K] vs T — θ_E=500/700/900 K 가족, T_ref 강제 영점, 본문 4수치(−3.74/0/+3.70/+9.14 μV/K@700 K) 점 anchor.
- **왜**: 신설 절 §2.4 가 그림 0건. electronic(∝T·영점 없음)과의 함수형 분리(3온도점 필요)가 (b)의 시각 대상.
- **설계**: (a) x 0…1.6, y 0…1.7; (b) x 260…360 K, y −8…+12 μV/K, 0선·T_ref 점선. ch2 관행 색(주 곡선 blue 허용).
- **배치 제안**: ch2 §2.4.3(수치·식별 소절) 옆.

### FF2-6. [재설계] ch2 `fig:occ_config` — 부분몰 발산 패널 추가
- **무엇을**: 기존 (a) ⟨n⟩·(b) S_config 를 유지(정보 유실 금지)하고 (c) ∂S_config/∂θ=−R ln[θ/(1−θ)] 곡선(±∞ 발산·중심 0)을 추가한 3패널.
- **왜**: 본문 §2.2 의 중심 결과가 부분몰 형태(eq:dSconfig)인데 그림엔 화살표 주석뿐.
- **설계**: (c) x=θ 0…1, y ±4R 클립, 중심 0 교차·양끝 발산 주석, 발산 방향 규약(ξ 좌표 읽기) 캡션 명시.

### FF2-7. [재설계] ch1 `fig:broadening` — 모식 지위 선언 + 정량화(예비)
- **무엇을**: (b) 두-상 패널의 실선을 실제 ②⊗③+① 수치 곡선(fig:widthbudget 의 최종 단계와 동일 파라미터)으로 교체하거나, 최소한 캡션에 개형(모식) 선언을 추가.
- **왜**: 유일하게 수치/모식 지위 선언이 없는 곡선 그림(B7).

**구현 선정(최소 4 이상)**: FF2-1 · FF2-2 · FF2-3 · FF2-4 · FF2-5 의 5건을 실제 TikZ 로 구현한다(FF2-6·7 은 프레이밍만 — 기존 그림 교체는 본문 수정을 동반하므로 경쟁 창 산출물로는 신규 조각 우선).

---

## 3단계 — 구현·검증 기록

### 3.1 구현 목록 (5건, 전건 완결 `\begin{figure}…\end{figure}` 조각)

| 파일 | 라벨 | 대상 장 | 내용 | 본문 제안 배치 위치 |
|---|---|---|---|---|
| `fig_ff2_1_ch2_dudt_blend.tex` | `fig:cand-ff2-1` | ch2 | (a) ∂U_oc/∂T(x̄) 완전식 vs 단순식 + 수준선 + tab:qrev 5점 (b) Q̇_rev/I(x̄) 부호 교대 | ch2 §2.8 `\subsection{SOC 부호 교대}`(tab:qrev 옆) — §2.5 fig:blend 은 모식으로 존치, 본 그림이 실계산을 담당 |
| `fig_ff2_2_ch1_hysgap.tex` | `fig:cand-ff2-2` | ch1 | ΔU^hys(Ω/RT) 문턱 곡선 + u³ 점근 + 상수-대입 오답(Taylor 함정) + staging 4점 + 도핑 극한 + RT/F 보조축 | ch1 §4.2 식 eq:dUhys 바로 아래(§13.5 도핑 절에서 재참조) |
| `fig_ff2_3_ch1_tail_overlap.tex` | `fig:cand-ff2-3` | ch1 | (a) peak shape 의 L_V/w=0·0.75·1.5·3 가족(정점·이동·꼬리) (b) 두 전이 합성의 겹침(골/정점 0.38→0.83) | ch1 §9 fig:reversal 다음(또는 §8 말미) — 서론 '관측' 셋째 축의 시각화 |
| `fig_ff2_4_ch1_u1_curvature.tex` | `fig:cand-ff2-4` | ch1 | (a) U_1(T) 기저 선형 vs 적분형 T² 곡률(−25.7 mV 식별 gap) (b) ∂U_1/∂T 기울기 공간(상수 vs 선형, 동결 근사 접점) | ch1 §15 식 eq:U1T2 아래 |
| `fig_ff2_5_ch2_einstein.tex` | `fig:cand-ff2-5` | ch2 | (a) S_vib(T;θ_E)/R 닫힌형 + 고전 극한 + 저온 동결 + 700 K 작동점 (b) ∂ΔU_vib/∂T 의 T_ref 강제 영점(θ_E=500/700/900 K) + 본문 4수치 anchor | ch2 §2.4.3(수치·식별 소절) |

### 3.2 좌표 산출과 물리 검산 (python — `ff2_compute_coords.py`, 전 좌표 하드코딩 근거)

상수: R=8.314462618, F=96485.33212, T=298.15 K (본문 수치 관행과 동일 자릿수 재현 확인).

| 그림 | 평가한 식 | 본문 anchor 재현 (검산 결과) |
|---|---|---|
| FF2-1 | eq:implicit(이분법 풀이)→eq:complete·eq:weighted·eq:qrev; U_j 는 표 tab:staging 의 (ΔH,ΔS) 로 eq:Uj 평가 | tab:qrev 5행 **전부 일치**: ∂U/∂T=−0.307/−0.204/−0.089/+0.044/+0.218 mV/K, Q̇/I=+91.5/+60.8/+26.6/−13.2/−64.9 mV, U_oc=43.5/74.3~74.4/109.0/148.8/195.2 mV; 계산 예제 완전식 −0.204·단순식 −0.134 mV/K 일치. 부호 반전 x̄≈0.681 |
| FF2-2 | eq:dUhys(+u³ 점근·오답 −(4RT/3F)u³) | gap(4RT)=54.76 mV = fig:hysloop 의 2.131 RT/F(54.8 mV) 일치; staging Ω 초기값 4점 gap=6.23/28.31/56.00/102.78 mV |
| FF2-3 | eq:lag·eq:peakshape 점별 적분(t∈[0,40], n=4000 사다리꼴) | L_V=1.5w 정점 (+1.01w, 0.1955) = fig:reversal 과 일치; 신규 값 0.227@+0.62w(0.75w)·0.149@+1.50w(3w); 합성 골/정점 0.377→0.832 |
| FF2-4 | eq:U1T2; a_e=−(π²/3)R(k_B/e_V)(g_max/Δx)·¼=−0.15321 J/(mol K²) | a_e·T_ref=−45.7≈−46 J/(mol K)(본문 §15 게이트 골 깊이 재현); 348 K 곡률 gap −25.66 mV; 동결 근사 대비 −1.99 mV=(a_e/2F)(50 K)² |
| FF2-5 | eq:Svib-einstein·eq:dUvib | θ_E=700 K 에서 ∂ΔU_vib/∂T = **−3.74/0/+3.70/+9.14 μV/K** — 본문 §2.4.3 의 네 수치 그대로 재현 |

물리 가드 확인: 전 곡선이 본문 식·부호·극한과 일치(gap≥0·문턱 아래 0, peak shape≥0·면적 보존, S_vib≥0·저온 0, ΔS_e<0 삽입 기준). 새 물리 주장 없음 — FF2-3(b) 의 두-전이 파라미터(간격 6w·같은 Q)와 FF2-4 의 ΔS_0=+80(대표 스케일)은 캡션에 입력값으로 명시. 기존 그림 정보 유실 없음(전건 신규 조각).

### 3.3 컴파일 검증 (오류 0 확인)

- 하네스: `harness_ff2_ch1.tex`(article+kotex+amsmath+tikz[positioning,arrows.meta,calc,fit,backgrounds]+ch1 매크로), `harness_ff2_ch2.tex`(동일 구성, tikz[calc,arrows.meta,decorations.pathreplacing,positioning]+ch2 매크로) — 각 장 preamble 라이브러리 그대로, pgfplots 불사용(plot coordinates 방식).
- 명령: `xelatex -interaction=nonstopmode harness_ff2_ch1.tex` / `…ch2.tex`
- 결과: **양쪽 exit 0 · 오류(`^!`) 0건 · overfull hbox 0건** (`harness_ff2_ch1.log`·`harness_ff2_ch2.log` 보존). 렌더 PDF(`harness_ff2_ch1.pdf`·`harness_ff2_ch2.pdf`)를 페이지 단위로 검수해 라벨 충돌 7건(범례 겹침·축 제목 겹침·주석-곡선 교차)을 수정 후 재컴파일 확인.
- 잔여 경고: 조각이 본문 라벨(eq:complete 등)을 참조하므로 하네스 단독 컴파일에서는 `??`(undefined reference 경고 — 오류 아님) — 본문 `\input` 편입 시 자동 해소. kotex 기본 폰트의 이탤릭 대체 경고 1건은 본문 빌드와 동일한 무해 경고.

### 3.4 산출물 일람

- `FRAMING_FF2.md` (본 문서) · `ff2_compute_coords.py` (좌표 산출·검산 스크립트)
- 조각 5건: `fig_ff2_1_ch2_dudt_blend.tex` ~ `fig_ff2_5_ch2_einstein.tex` (라벨 `fig:cand-ff2-1`~`-5`, 기존 라벨과 충돌 없음 — 기존 문서에 `fig:cand-*` 계열 부재 확인)
- 하네스·검증 산출: `harness_ff2_ch1.tex/.pdf/.log/.aux` · `harness_ff2_ch2.tex/.pdf/.log/.aux`
- 문서 원본 수정: **없음** (쓰기는 본 폴더 한정)

**최종 집계: 프레이밍 7건(FF2-1~7) · 구현 5건(FF2-1~5) · 컴파일 전건 통과(오류 0).**

