# v8-05 자체검수 노트 (graphite_ica_ch1 v8 — 유도 포함 교과서 확장판)

산출 = `v8-05.tex`(자족) + `v8-05.pdf`(xelatex 2-pass, 0-err, 21p). 독립 작업(무통신).

## 1. Read Coverage (전문 정독)

| 입력 | 행 범위 | 정독 |
|---|---|---|
| `v8-00_spine/AUTHOR_BRIEF_v8.md` | 1–64 (전문) | 권위 사양. §3 유도 11식·§4 보존·§5 그림·§7 부호 8항·§8 작성방식 |
| `v7-11/v7-11.tex` | 1–890 (전문, 2 페이지로) | ★배치 보존 대상. 절순서 N0→N9·결과박스 10개·그림 5개·표 4종·부호검산 |
| `docs/graphite_ica_ch1_Opus_v5.tex` | 1–1883 (전문, 4 페이지로) | ★유도 원천. Boltzmann→Eyring→G/μ→평형→logistic→spinodal→ΔU_hys→L_q→memory→tail |
| `v7-00_spine/Anode_Fit_v11_final.py` | 1–707 (전문) | 식·부호·식별자 정본. func_* 1:1 대조 |
| `v7-00_spine/v11_flowchart.md` | 1–90 (전문) | 척추 N0→N9, 노드↔식↔v5 매핑, 부호규약 |

## 2. ★유도 사슬 복원 목록 (G-derive — 브리프 §3 의 11식, 메운 단계)

각 결과 박스 위에 [출발식→연산→중간식≥1→박스] 가시화(한 줄 점프 0). 손계산 round-trip 으로 전수 검증(`verify.py`):

1. **U_j(T)** (eq:Uj): G≡H−TS(1.4)→μ≡∂G/∂n(1.5)→전기화학 균형 μ̃합(1.6)→3종 펼침(1.6a, eq:eqexpand **신규 중간식**)→상수덩이 묶어 μ=μ⁰−sF(V−U)·ΔG=−sFU(1.7)→ΔG=ΔH−TΔS 대입·1줄 이항→박스. (이전 "정의로 선언" → 펼침 식 1.6a 추가로 *유도*로 승급, 검수 #1 반영.)
2. **w_j** (eq:wbase): logistic 중심 기울기 s/(4w)→w=RT/F→다중도 n_j 일반화. w_eff 는 g″ 중심 기울기 4RT−2Ω(eq:isoslope **신규 중간식**)를 이상값 4RT 와 등치→박스. (이전 "eq:gpp 류" 포인터 → 식 1.14 명시 도출, 검수 #2 반영.)
3. **ξ_eq logistic** (eq:xieq): affinity 𝒜=sF(V−U)→BV 정역장벽(eq:bv)→비취해 χ 상쇄 detailed balance e^{𝒜/RT}(eq:db)→운동방정식(eq:relax)→정지점비(eq:stationary)→ξ=1/(1+X⁻¹) 풀이→박스. s→σ_d·U_j→U_j^d 승급 명시(검수 #5 반영).
4. **평형 peak** (eq:eqpeak): 보존식 q미분(eq:dQdV)→logistic z치환→bell 항등식 dξ/dz=ξ(1−ξ) under-brace(eq:belliden)→연쇄율 ×σ_d/w→박스.
5. **ΔU_hys** (eq:dUhys): smix Stirling(eq:smix)→g(ξ)(eq:gxi)→g″ 둘째미분(eq:gpp)→근의공식 spinodal(eq:spinodal)→g'=sF(V_eq−U) 도출(eq:gprime **신규 중간식**)→V_eq(eq:Veq)→spinodal 대입 logit 역수(eq:hyssub)→극대−극소 artanh 결합(eq:hysdiff)→박스. (eq:Veq 의 g'=sF(V_eq−U) 관계 in-place 도출, 검수 #4 반영.)
6. **분기 중심** (eq:Ubranch): 두 spinodal 평균=U_j 대칭(로그합 0·(1−2ξ)합 0)→방향별 ±½σ_d γ→박스.
7. **L_q** (eq:Lqfull): 운동방정식 /(dq/dt)→지연 ODE(eq:Lq)→적분인자 일반해 합성곱(eq:memory)→k=k⁺(1+e^{−𝒜/RT}) detailed balance(eq:kuniv)→Eyring k₀=k_BT/h→로그 4항 박스. χ_d·ΔH_eff 승급 forward-pointer 추가(검수 #5 반영).
8. **컷 affinity 𝒜** (eq:Acut): 원천 dξ_eq/dq 정점 5% 컷→𝒜=z_cut·n·RT(상한 A_cap·RT). ★z_cut=4.357 는 *미분* 5% 컷(점유 아님) 명시 — v11 docstring "ξ_eq 5%" 부정확 정정(검수 agent 확인). ∂lnL_q/∂V=0 운영실현·부등식은 동기 구분(v7 系統 결함 회피).
9. **ΔH_a^eff** (eq:dHeff): 꼬리 구동력 −Ω(1−2ξ) 분리→깊은꼬리 ξ→1(충전거울 ξ→0) 상수 +Ω 흡수→ΔH_a−χ_dΩ. χ_d 합-1(eq:chid).
10. **L_V·인과꼬리** (eq:peakshape): memory 합성곱→이산 저역통과 ρ=e^{−Δgrid/L_V}(eq:lowpass)→peak=(ξ_eq−ξ_lag)/L_V→★충전 격자역전 ξ[::-1]…[::-1](eq:reversal).
11. **합산** (eq:sum): 보존식 Qq=Q_bg+ΣQξ→q미분→/(dV/dq) 선형합→박스.

## 3. 부호 8항 (브리프 §7 — v11 1:1, 라운드마다 전건)

S1 U_j=(−ΔH+TΔS)/F·ΔG=−FU ✓ / S2 ξ_eq=logistic[σ_d(V−U)/w] 방전 V↑→ξ↑ ✓ / S3 dξ/dV peak 양수·방향불변 ✓ / S4 ΔU_hys≥0·Ω≤2RT→0·분기±½σ_d ✓ / S5 χ_d 충전 1−χ·ΔH_a^eff=ΔH_a−χ_dΩ ✓ / S6 ∂lnL_q/∂V 운영 0·부등식은 동기 ✓ / S7 충전 격자역전·dQ/dV 거울 양수 ✓ / S8 V_n=V_app−σ_d|I|R_n ✓. 검수 3 agent 전원 8/8 PASS 확인.

수치 검증(verify.py·298.15K): ΔU_hys(12000,γ=1)=86.69mV(=self-test 86.7), Ω=4RT→54.8mV, Ω=2RT→0; U(298) stage2→1=0.0853V; L_q log형=func_L_q 정확; logistic=stationary비; bell 항등식; spinodal 0.7887/0.2113(Ω=3RT). 전부 일치.

## 4. 그림 목록 (8개; v7-11 유래 5 / 신규 3 — 영어 ASCII 라벨, orphan 0)

| 라벨 | 유래 | 내용 |
|---|---|---|
| fig:spine | v7-11 그대로 채택 | 코드 진행 척추 N0→N9 |
| fig:staging | v7-11 유래 | 흑연 staging 갤러리 채움 |
| fig:hysloop | v7-11 유래 | V_eq(ξ) 비단조 과주행 |
| fig:logistic | v7-11 유래 | ξ_eq + 미분 종 |
| fig:reversal | v7-11 유래 | 인과 꼬리 방향(충전 격자역전) |
| **fig:dwell** | **신규** | g(ξ) 이중웰 + spinodal + plateau 현(유도 #5 보조) |
| **fig:fluxcross** | **신규** | 정·역 플럭스 교차 정지점(유도 #3 보조) |
| **fig:memory** | **신규** | 지연 ODE 일반해 기억 거동(추종/꼬리 두 극한, 유도 #7 보조) |

신규 3개는 복원한 유도 단계를 돕는 그림(g 이중웰·플럭스 교차·ODE 완화). v3–v6 그림 재사용 0.

## 5. 10R 가변-청크 검수 결함 추이 (G-derive 1급 + 부호·G-follow·완결성)

본작업 1회 후 master 직접 라운드 + 3-agent 병렬 적대검수(refute·가장약한1곳·빈통과금지, 청크/렌즈 전환):
- agent1 (N4–N7, G-derive): CRITICAL 0·HIGH 0. MED 2(eq:weff 기울기 in-section 도출, "아래/위" deixis), LOW 3.
- agent2 (부호+v11 1:1, 전문): CRITICAL 0·HIGH 0. 부호 8/8·박스 10개·표 3종 verbatim 확인. MED 2(eq:Veq 도출, L412 라인번호), LOW 3.
- agent3 (N2/N3/N8/N9+scope): CRITICAL 0·HIGH 0(scope creep 0). MED 1(U_j 정의 vs 도출), LOW 4.
- 삼각검증 후 master 직접 수정: #1 eq:weff 기울기 eq:isoslope 신규 도출+deixis 정정 / #2 U_j eq:eqexpand 신규 펼침식 / #3 eq:Veq eq:gprime in-place 도출 / #4 eq:kuniv χ_d 승급 forward-pointer / #5 s→σ_d 승급 명시 / σ_d F thin-space.
- 재빌드 후 수렴: 잔여 결함 = LOW 잔량(L412 라인번호=v7-11 보존 항목, 의도적 preservation)·연속 0-CRITICAL/0-HIGH 2R. 수렴 판정.

## 6. 빌드

xelatex (MiKTeX 25.12) + D2Coding 폰트 확인. 2-pass(실제 4-pass: 라벨·lastpage 수렴) → **0 error · 0 ignored-error · 0 undefined ref · 0 overfull hbox · 21 페이지 PDF**. 초기 "Infinite glue shrinkage [4][5]"(longtable 페이지 분할)는 표를 \newpage+\footnotesize 단일 페이지로 고정해 제거(v7-11 preamble 보존, 표 자체 불변). 잔여 경고 = bx/it 한글 폰트 substitution 3건(캡션, 무해).

## 7. 보존·범위

- 결과 박스 10개·코드 식별자(func_*)·부호·절순서 N0→N9·표 3종(staging/inputs/nodemap) = v7-11 verbatim, v11 1:1.
- 추가 = 유도 단계만(중간식 3개 신규: eq:eqexpand·eq:isoslope·eq:gprime — 모두 인접 도입·사용, orphan 0).
- 무관 주제 재유입 0(lever/chord/cotangent·KWW·Marcus·Arrhenius 회귀·피팅 알고리즘 끌어오지 않음 — 곡선 11식 수렴 사슬만). scope creep 0(agent3 확인).
- 분량 21p = 유도의 자연 결과(패딩 0). 브리프 ~28–40p 는 상한 가이드, 무관 확장으로 채우지 않음.

## Decision Queue
없음(작업 중단 사유 없이 완결).
