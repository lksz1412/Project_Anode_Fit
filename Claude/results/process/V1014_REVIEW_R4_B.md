# Anode_Fit v1.0.14 P4.1 R4 — 검수자 B(Sonnet) 보고서
## 렌즈: 그림·표 정합 (캡션↔tikz, 라벨 용어, 표↔본문 수치, 라벨 겹침, 좌표 자기주장 검산)

- 대상: `graphite_ica_ch1_v1.0.14.tex`(전 3235행, 그림 17종·표 8종), `graphite_ica_ch2_v1.0.14.tex`(전 782행, 그림 2종·표 2종), `appendix_phase_separation.tex`(전 486행, 그림 2종)
- 방법: 3개 파일 전문 정독(head→tail) + 그림당 대표 3점 이상 python 수치 검산(scipy 포함, `scipy.optimize.brentq`·`scipy.integrate.quad` 사용) + 표 수치 ↔ 본문 재계산 교차
- ★ 파일 수정 없음. 본 보고서 1개만 신규 작성.

---

## 1. 그림별 검사 결과 표 (Ch1, 17종)

| 그림 | 캡션 핵심 주장 | 검산 방법 | 판정 |
|---|---|---|---|
| fig:spine (L158) | 계산 진행 블록도, N0–N9 | 캡션 서술 vs 노드 나열 대조 | PASS |
| fig:staging (L272) | stage 4/3/2L/2/1 갤러리, U≈0.21/0.14/0.12/0.085V | tab:staging 값과 대조 | PASS (정확 일치) |
| fig:sm-reservoir (L399) | grand canonical 개념도 | 개념도, 수치 없음 | PASS |
| fig:sm-gxi (L636) | f(ξ)/RT 5곡선(Ω=0,1,2,2.5,3RT), spinodal ξ_s=0.2113/0.7887 | 공식 대입 수치검산(전 좌표) | PASS (완전 일치) |
| fig:sm-mu (L670) | μ(θ) 3곡선, spinodal θ_s=0.146/0.854, 값 ±1.066 | 공식 대입 수치검산 | PASS |
| fig:sm-occ (L786) | (a) θ 3온도 계단형 (b) ξ_eq(V), w=23.1/25.7/28.3mV | RT/F 계산 재확인 + 좌표 검산 | PASS |
| fig:doublewell (L1043) | g_j(ξ) 정성 곡선, Ω=3RT, spinodal 표시 | "정성 곡선"으로 명시 자기한정 — 캡션이 정확좌표는 sm-gxi 참조로 위임 | PASS |
| fig:hysloop (L1147) | V_eq(ξ) Ω=4RT, spinodal 1.0657/-1.0657 | 공식 대입(4dp 반올림 오차 <0.001) | PASS |
| fig:barrier (L1253) | 활성화 장벽 개형도 | 정성도, 수치주장 없음 | PASS |
| fig:flux (L1289) | 정지점 교차 ξ_eq=2/3, 1/2 | 대수 확인(2(1-ξ)=ξ→ξ=2/3) | PASS |
| fig:logistic (L1361) | ξ_eq·ξ(1-ξ) 종, 최대 0.25→스케일3배=0.75 | 스케일 배율 확인 | PASS |
| **fig:widthbudget (L1538, R2 갱신)** | ②내재 bell, ②⊗③ 합성 σ_η=1.25σ_int→1.6w_j, ①수치적분(L_V=1.5w_j) | **3개 곡선 전체 python 재현** — 아래 §3 | **PASS (강한 확증)** |
| fig:broadening (L1649) | (a)단상 종 (b)두-상 델타→종, ①②③ 라벨 | 정성 스케치, \S 인용 정합 확인 | PASS |
| fig:relaxode (L1829) | ξ_eq/ξ_lag 완화, "peak shape" 라벨 | **본문 peak\_shape 식별자와 대조** | **LOW 결함 — §4 참조** |
| fig:reversal (L1907) | 방전/충전 꼬리 방향 거울 | 정성, 캡션 "peak\_shape" 용어 확인(일치) | PASS |
| fig:lco-dirmap (L2116) | σ_d 슬롯 배정 블록도 | 식~eq:lco-sigmaslot 대조 | PASS |
| fig:lco-electronic (L2617) | MIT-logistic 게이트 g(x), ΔS_e bump | **곡선 전체 python 재현**(g_max=13·x_MIT=0.85·Δx=0.05) | **PASS (강한 확증)** |

## 2. 표별 검사 결과 (Ch1 8종 + Ch2 2종)

| 표 | 핵심 수치 | 대조 대상 | 판정 |
|---|---|---|---|
| tab:staging (L1961) | U/ΔH_rxn/ΔS_rxn 4행 | U(298)=(-ΔH+298.15ΔS)/F 재계산, 전 행 ±1mV 이내 | PASS |
| tab:lco-staging (L2045) | U_j~3.90/4.05/4.17-20V, 시연값 3.930/3.880/4.050 | 코드(`Anode_Fit_v1.0.14.py` L660-677) 대조 — 캡션이 "별개, round-trip 대상"으로 명시 | PASS (자기한정 정확) |
| tab:nodemap (L2946) | N0–N9, N0'/N2'/N5+/N9' | 식 번호 → 본문 정의 대조 전수 | PASS |
| tab:signcheck-S (L2989) | S1–S8 정성 검산 | 각 행 근거식 재확인 | PASS |
| tab:signcheck-R (L3025) | R1–R6 수치, u=0.766·86.7mV·+80J/(mol·K) 등 | **python 재계산**(§3) | PASS |
| tab:symcode (L3080) | 기호↔코드 식별자 | 본문 기호 정의와 대조 | PASS |
| tab:inputs (L3117) | z_cut=4.357, min_lag_grid_steps=2.0, v_span_floor=1e-6 | 본문 eq:Acut(L1727)·eq:branch ν=2(L1883)·L927 스팬 하한 서술과 대조 | PASS (완전 일치) |
| tab:nodecode (L3157) | 노드↔구현 식별자 | tab:nodemap과 1:1 대조 | PASS |
| tab:ds (Ch2, L341) | ΔS⁰_j = +29/0/-5/-16 | Ch1 tab:staging ΔS_rxn과 대조 | PASS (정확 일치) |
| tab:limits (Ch2, L637) | 6개 극한·코너 | 본문 각 절 서술과 대조 | PASS |

## 3. 수치 검산 상세 (그림당 대표 3점 이상, python)

**fig:widthbudget (가장 중요 — R2 갱신 대상)**: 세 곡선을 모두 독립 재현.
- ② 내재곡선(s=1): `1/(4·cosh²(z/2))` — 19개 좌표 전부 4자리 일치.
- ②⊗③ 합성곡선(파선): 캡션이 "같은 함수족이면" 전제를 명시했으므로, 동일 함수를 s=1.6으로 재척도(`1/(4s·cosh²(z/2s))`)했더니 19개 좌표 전부 일치 — 이는 실제 convolution이 아니라 "분산 매칭 + 동일 함수족 가정"의 해석적 근사이며, **캡션 스스로 "같은 함수족이면"이라고 조건부로 밝혀 두어 과장 없음**.
- ① 지수꼬리 포함 곡선(굵은 실선): 캡션이 "수치 적분"이라 주장 — `scipy.integrate.quad`로 s=1.6 곡선과 단측 지수커널(L=1.5)의 실제 convolution을 수행, 21개 좌표 전부 diff=0.0000 — **"수치 적분" 주장이 문자 그대로 참**임을 확인(가장 엄격한 확인 대상이 가장 강하게 통과).

**fig:lco-electronic**: g(E_F,x) 로지스틱 게이트(g_max=2.6 스케일·중심 x_MIT=0.85→tikz축 xx=0.15·폭 Δx=0.05) 10개 좌표 전부 일치; ΔS_e bump(∝σ(1-σ), 진폭 5.4배) 5개 좌표 전부 일치.

**tab:signcheck-R 재계산**: R1 Ω=12000, γ=1 → u=0.7661(일치), ΔU_hys=86.68mV(표기 86.7 일치). R2 Ω=2RT=4957.6≈4958(일치). R6 dφ/dT=0.83mV/K → ΔS=96485×0.83e-3=80.08 J/(mol·K)(표기 +80 일치), 30K 창 Δ U=24.9mV(표기 +25mV 일치).

**appendix fig:app-tangent / fig:app-phasediag (A.2, 4점 정정 검증)**: binodal `brentq`로 직접 근을 구해 ξ_b=0.070720/0.929280(표기 0.0707/0.9293 일치), f(ξ_b)/RT=-0.058341(표기 -0.0583 일치); spinodal ξ_s=0.211325/0.788675(표기 0.2113/0.7887 일치), f=-0.015707(표기 -0.0157 일치). 상평형도의 binodal 곡선(`2(1-2ξ)/ln[(1-ξ)/ξ]`)·spinodal 곡선(`4ξ(1-ξ)`) 각 12점 전부 일치, Ω=3RT 등온선의 네 교점이 fig:app-tangent와 동일 값으로 재확인됨 — **"4점 정정 후 곡선 매끈함" 요청 사항 충족, 결함 없음**.

## 4. 결함 목록 (심각도순, refute 생존분만)

### LOW — fig:relaxode 라벨 용어 불일치 (그림 내 라벨 vs 본문 식별자)
- **위치**: `graphite_ica_ch1_v1.0.14.tex` L1845
- **원문**: `\node[font=\scriptsize] at (1.1,2.15) {peak shape $=(\xi_\eq-\xi_\mathrm{lag})/L_V$};`
- **문제**: tikz 노드 텍스트가 "peak shape"(공백)로 적혀 있으나, 바로 아래 박스식 eq:peakshape(L1861 `\text{peak\_shape}=...`)와 eq:branch(L1873–1878, 두 곳 모두 `\text{peak\_shape}`)는 밑줄(`\_`) 있는 코드 식별자형 "peak\_shape"를 쓴다. 같은 문건의 다른 그림 fig:reversal 캡션(L1934 `peak\_shape with tail`)과 표 tab:nodecode N6행(L3172 `peak_shape = ksi_eq*(1-ksi_eq)/w`)도 전부 밑줄형으로 일관되어 있어, fig:relaxode의 tikz 라벨만 유일하게 이탈한다.
- **refute 시도**: "그림 내 자연어 설명이니 공백이 의도된 스타일일 수 있다"는 반론을 검토했으나, 같은 문건의 다른 3곳(박스식 2곳 + fig:reversal 캡션 + 표 1곳=4곳)이 전부 밑줄형으로 통일되어 있어 이 반론은 기각됨 — 유일한 이탈점으로 생존.
- **정정 제안**: L1845의 `peak shape`를 `peak\_shape`로 교체(1자 수정, 물리·수치 영향 없음).

### 결함 없음(추가 발견 안 됨)
- 좌표 겹침(라벨-곡선 충돌, 렌즈④): 전 17개 그림의 라벨 y-좌표를 인접 곡선값과 대조 — fig:app-tangent 영역 라벨(안정/준안정/불안정, y=0.068)이 곡선 최댓값(0.0569)보다 위에 위치해 여유 확보, fig:sm-occ (b)의 θ_eq/ξ_eq 라벨도 두 곡선 사이 공백에 위치. 겹침 결함 없음.
- γ 기호 재사용 혼동(분기 축소인자 γ_j vs 계면에너지 γ): 두 용법이 쓰이는 절이 서로 멀리 떨어져 있고(§sec:hys ↔ §sec:broadening(c)-(i)), 후자 도입부(L1585)에서 "분기 축소 인자 γ_j와 무관한 별개 기호"라고 명시적으로 disclaim — 어느 그림 라벨도 두 의미를 혼용하지 않음. 결함 없음.
- σ_int·σ_η 정의(R3 이후 신규 기호): 본문 정의(L1528 σ_int≡πn_jRT/(√3F), L1518 σ_η)와 그림 라벨(L1552 σ_η=1.25σ_int) 완전 일치. 결함 없음.
- tab:lco-staging 시연값(3.930/3.880/4.050V)과 표 U_j열(~3.90/~4.05/~4.17-20V) 수치 불일치는 캡션이 "별개, round-trip 대상"이라 명시적으로 disclaim하고 있어 결함 아님(코드 `Anode_Fit_v1.0.14.py` L660-677과 정확 대조 확인).

## 5. Ch2·Appendix 교차 확인
- tab:ds의 ΔS⁰_j(+29/0/-5/-16)가 Ch1 tab:staging의 ΔS_rxn과 정확 일치 — 두 챕터 간 데이터 정합 확인.
- fig:blend(Ch2 L529)는 캡션이 스스로 "모식 — 부호·하강 순서는 임의"라 선언, 실제 흑연 프로파일 방향(탈리튬화 시 -16→-5→0→+29 상승)과 그림의 임의 스케치 방향이 다른 것은 의도된 것으로 확인(결함 아님).
- appendix ξ 좌표 배향 경고(L6-8, L55-61: 부록 ξ=본문 θ, 여집합 관계)가 fig:app-tangent·fig:app-phasediag 어디에도 이 여집합 혼동 없이 일관 적용됨을 확인.

## 6. 결론
그림 21종(Ch1 17 + Ch2 2 + App 2)·표 10종(Ch1 8 + Ch2 2) 전수 검사 결과 CRITICAL/HIGH 결함 0건, MEDIUM 0건, **LOW 1건**(fig:relaxode "peak shape"→"peak\_shape" 통일 누락). "좌표는 식 그대로의 수치 평가" 자기주장이 있는 모든 그림(sm-gxi, sm-mu, sm-occ, widthbudget, lco-electronic, app-tangent, app-phasediag)이 python 재계산으로 확증되었고, 특히 R2 갱신 대상인 fig:widthbudget의 "수치 적분" 주장은 실제 convolution 수치검증으로 문자 그대로 참임을 확인했다.
