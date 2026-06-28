# REVIEW2 — v7-09b.tex 적대 재검수 (검수 sub, 검토2)

> 대상: `Claude/results/v7-09/v7-09b.tex` (660행, 전문 정독 head→tail — 식·부호사슬 단위 청크).
> 기준: `v7-00_spine/Anode_Fit_v11_final.py`(707행)·`v11_flowchart.md`(분극 정정본)·`AUTHOR_BRIEF.md` 전문 정독.
> 비교 baseline: `REVIEW1.md`(v7-09 검수, 20/30). v7-09b = 그 보완본(대폭 증보: logistic·spinodal·L_q 유도 신규 추가).
> 역할: 리뷰 전용 — 어떤 파일도 수정·커밋하지 않음. 본 .md 1개만 생성.
> 검산 도구: μ_mix 적분 vs 폐형, staging 표 vs 코드, logistic 수치, 병렬 적대 에이전트 2(logistic/히스 · L_q/꼬리).

---

## ① REVIEW1 결함 보완 반영 점검 (6건 + 유도누락 1)

| REVIEW1 항목 | 심각도 | v7-09b 반영 위치 | 판정 |
|---|---|---|---|
| HIGH-1 fig:spine 노드번호↔절번호 불일치 | HIGH | L89–98: 각 박스에 `Sec NN` 2차 라벨 추가(N3/hys→Sec N5, N4/width→Sec N3, N5/ksi→Sec N3, N6/peak→Sec N4, N7/L_V→Sec N6, N8/lowpass→Sec N7, N9/sum→Sec N8–N9). 절 번호 매핑 **전수 정확**. | **FIXED** |
| HIGH-3 ∂lnL_q/∂V<0 자기모순(컷상수 A) | HIGH | L501–507: A_j=전이당 컷 상수 명시 + eq:Lqflat `∂lnL_q/∂V=0 within plateau`(L502–505) + L507 단조성을 "물리적 동기"로 강등("미분을 실시간 평가 안 함, L_q piecewise-flat 상수"). 잔여 V-의존 주장 없음. | **FIXED** |
| HIGH-4 G-usable: 동역학 인자·생성자 기본값 표 부재 | HIGH | (a) staging 표 L235–245 에 `dH_a·dVdq_qa·dS_a` 3열 추가 — 코드 GRAPHITE_STAGING_LIT 와 9열 **전수 일치**(자체 대조 검산). (b) 생성자 기본값 표 L158–181 신설(z_cut 4.357·A_cap_RT 4.0·min_lag 2.0·n_work_min 2048·grid_pad 0.15·w_eff_floor 0.05·v_span_floor·seed_* 등 14행). | **FIXED** |
| 유도누락(logistic·spinodal·L_q 코드전사) | HIGH | logistic = μ-equality+FD 유사성으로 유도(L252–266); spinodal ΔU_hys = double-well g(ξ)→μ_mix→g″=0→폐형(L353–377); L_q = τ 완화식→q축 Green 함수 적분(L433–452). 3대 유도 모두 신규 추가. | **FIXED**(단 ★새 회귀 1, ②참조) |
| MED-6 N0 q=Q/Q_cell 미도입(orphan 직전) | MED | eq:qdef L131–134: `q=Q/Q_cell`·`q̇=I_abs/Q_cell` 도입 + L_q·C-rate 환산 연결 명시. eq:Tattempt 의 I/Q_cell orphan 해소. | **FIXED** |
| MED-5 eq:facade I_abs 글리프 충돌 | LOW | L77–82 미변경 — 수학기호 I_abs 와 코드 인자 `I_abs` 동일 글리프 잔존. 의미는 정합(코드 L507–511), 표기상 동어반복. LOW 라 비차단. | **미반영(LOW)** |

**소계**: 차단성(HIGH) 4건 + 유도누락 = **전부 반영**. LOW 1건만 잔존(비차단).

---

## ② ★신규 회귀 (대폭 증보분 — 신규 식의 부호·유도·orphan 엄격 검수)

### NEW-1 — eq:mueqraw → eq:logitsolve **n_j² 대수 오류** (HIGH, 신규 유도)
- 행: eq:mueqraw L253–257, eq:logitsolve L260–264.
- 틀림: eq:mueqraw 의 전기화학항이 `−n_j F σ_d V_n`, 기준 `Δμ_j^0=n_j F σ_d U_j`(L259). μ_occ=μ_vac 풀면
  `RT ln(ξ/(1−ξ)) = n_j F σ_d(V_n−U_j)` → `ln(ξ/(1−ξ)) = σ_d(V_n−U_j)/(RT/(n_j F))`.
  그런데 eq:logitsolve 는 분모를 `n_j RT/F`(=w_j)로 적었다. 올바른 분모는 `RT/(n_j F)` — **n_j² 만큼 어긋남**.
- 근거: 코드 `func_ksi_eq` `z=s*(V_n−U)/func_w`, `func_w=n*R*T/F` → z=σ_d(V_n−U)F/(nRT). 이 분모(nRT/F)가 나오려면
  eq:mueqraw 의 전기화학항 계수는 **n_j 가 아니라 1**(단위 사이트당 1전자)여야 한다. 즉 항을 `−F σ_d V_n`, `Δμ_j^0=F σ_d U_j`
  로 고쳐야 RT ln(...)=F σ_d(V_n−U_j) → ln(...)=σ_d(V_n−U_j)/(RT/F), 그리고 w=nRT/F 정의(다중도가 폭에 흡수)와
  정합. 현 형은 다중도를 **분자(전기화학항)에 한 번 + 분모(w)에 또 한 번** 넣어 이중 계상.
- 영향: 최종 박스식 eq:ksieq(L294–298)·w 정의(L281)는 코드 정합(결과는 맞음). **유도 중간 두 식만 틀림** —
  REVIEW1 이 "logistic 유도 전무"를 HIGH 로 지적해 새로 넣은 바로 그 유도가 G-follow 독자를 오도. 신규 회귀.
- 옳은 형: eq:mueqraw 의 `n_jF σ_d V_n → F σ_d V_n`, L259 `Δμ_j^0=n_jF σ_d U_j → F σ_d U_j`. (또는 다중도를
  명시적으로 "폭에 흡수되는 effective 인자"로 한 줄 각주 — 단 현 표기는 그 설명 없이 어긋남.)

### NEW-2 — h_{η,j} orphan (MED, 신규/증보)
- 행: eq:Ubranch L392·eq:center L398·fig:hys L412·keybox L657 에서 `h_{η,j}`(부분 cycle 인자) 사용,
  **본문 정의 없음**. 코드 docstring(func_U_branch L134·생성자 L205)은 "부분 cycle 인자, 기본 1.0"으로 명시하나
  .tex 본문은 도입 0. 히스 절이 대폭 증보됐는데 이 기호만 전제 없이 등장 → 완결성 orphan.
- 옳은 형: §N5 도입부에 "h_η = 부분 cycle 인자(완전 cycle 1.0), 코드 `h_eta` key" 한 줄.

### NEW-3 — eq:Lqintegral↔eq:lowpass "같은 kernel" 표현 과장 (LOW)
- 행: L448–452. 연속 Green 함수 적분이 "균일 격자에서 같은 kernel 의 지수 재귀로 구현"(L452)이라 하나,
  코드 `_causal_lowpass`(L100–118)는 `y_0=x_0` zero-order-hold seed — 선단(leading edge)에서 연속형과 다름.
  수치 정합은 i≥1 정상 재귀에서만 정확. 결함은 아니나 "exact same" 뉘앙스가 경계조건을 가린다.
- 옳은 형: "연속형은 i≥1 정상 재귀, y_0=x_0 는 인과 seed" 한 줄 단서.

### 검산 PASS (신규 유도 중 무결 확인)
- spinodal ΔU_hys 폐형 eq:dUhysderive/eq:dUhys: μ_mix 적분 vs 폐형 **수치 전수 일치**(Ω=6000~13000, 오차<1e-9). 부호 ξ_−<½<ξ_+ → gap≥0 정확.
- g(ξ)→μ_mix(eq:mumix)→g″=0(eq:spinodalsolve) 대수 무결. ξ_±=(1±u)/2, u=√(1−2RT/Ω) 정확.
- eq:lnLq/eq:Lq: 코드 L96 5개항 부호·prefactor `Ih/(Q_cell kB T)`·`(1+e^{−A/RT})^{−1}`·`exp[(ΔG_eff−χ_dA)/RT]` 전수 일치.
- eq:dxidv/eq:absdxidv: dξ/dz=ξ(1−ξ)·dz/dV=σ_d/w 정확. eq:Acut=코드 L335 일치. eq:chglowpass/eq:tailpeak=코드 L477/479 일치.
- staging 표 9열 = 코드 4전이 전수 일치, U(298) 자기정합(0.211/0.140/0.120/0.085).
- (참고) 코드 L216 주석 `z_cut=4.357=ξ_eq 5%` 는 실제 logistic(4.357)=1.27%로 코드 주석이 틀리나, .tex 표(L172)는 중립 라벨("cutoff affinity multiplier")이라 **문건엔 미전파** — 문건 무결.

---

## ③ 재점수 (6 차원 × 5 = /30) — REVIEW1 대비

| 차원 | v7-09(R1) | v7-09b(R2) | 근거 |
|---|---:|---:|---|
| 1. 구조·spine 정합 | 3 | **5** | fig:spine 2차 라벨로 HIGH-1 해소·절매핑 전수 정확. q 도입(MED-6) 완료. |
| 2. 물리·부호 사슬 | 4 | **4** | 부호 8항 전부 PASS(④). ∂lnL_q/∂V 모순(HIGH-3) 정정. 감점 = NEW-1 logistic 유도 n_j² 대수오류(부호 아닌 다중도 배치). |
| 3. G-follow | 3 | **4** | logistic·spinodal·L_q 유도 신규로 따라가짐 대폭 향상. 감점 = NEW-1 중간식이 독자 오도 + h_η orphan(NEW-2). |
| 4. G-usable(재현) | 2 | **5** | 생성자 기본값 표 + 동역학 인자 3열(코드 전수 일치) → "이 문건만으로 v11 재현" 닫힘. HIGH-4 완전 해소. |
| 5. 완결성 orphan | 4 | **4** | q·I/Q_cell orphan 해소. 감점 = h_η 미정의(NEW-2) 신규 orphan. |
| 6. 그림·시각·형식 | 4 | **5** | 그림 6종 신규 TikZ·영어 ASCII·\ref·절다리 양호. fig:spine 혼동 해소. 빌드 11p 에러 0. |
| **합** | **20** | **27/30** | +7. 차단성 보완 전부 반영, 신규 회귀 1 HIGH(국소 유도 대수)·1 MED(orphan)만 잔존. |

**판정**: 보완 성공(20→27). 잔여 차단 후보 = **NEW-1**(logistic 유도 2식 대수정정) 1건. NEW-2(h_η) 권고. 정정은 국소 2~3행, 최종 박스식·부호사슬은 무손상.

---

## ④ 부호 8항 PASS/FAIL (v11 대조)

1. U_j(T)=(−ΔH+TΔS)/F — **PASS** (eq:Uj L218 = 코드 L69).
2. ξ_eq=logistic[σ_d(V−center)/w] — **PASS(결과식)** (eq:ksieq L294–298, z 정의에 σ_d = 코드 L86). ※유도 중간 eq:logitsolve 분모 n_j² 오류(NEW-1) — 부호 아닌 다중도 배치 결함, 최종식은 정합.
3. dξ/dV=σ_d ξ(1−ξ)/w, peak 양수 — **PASS** (eq:dxidv L328·eq:absdxidv L330).
4. ΔU_hys≥0, Ω≤2RT→0; 분기중심 +½σ_d h_η γ — **PASS** (eq:dUhys L380–388·eq:Ubranch L392 = 코드 L123–138; μ_mix 적분 검산 일치). ※h_η 본문 미정의(NEW-2, 부호는 정합).
5. χ_d 방전 χ/충전 1−χ; ΔH_a^eff=ΔH_a−χ_dΩ — **PASS** (eq:chid L461–466·eq:dHeff L470 = 코드 L160·L152).
6. ∂lnL_q/∂V — **PASS(정정 확인)** (eq:Lqflat L502–505 `=0 within plateau` + L507 단조성 동기로 강등; REVIEW1 FAIL 해소).
7. 충전 격자역전 ξ[::-1]…[::-1], 충전=방전 거울 — **PASS** (eq:chglowpass L541–544 = 코드 L477).
8. 분극 V_n=V_app−σ_d|I|R_n — **PASS** (eq:polar L189–191 = 코드 L412; 방전 anodic 양 과전압 서술 = flowchart 정정본 L88 정합).

부호 8항: **8 PASS** (6번 정정 확인). 부호 자체는 전건 v11 정합 — 잔여 결함 NEW-1 은 부호가 아닌 유도 중간식 다중도 대수, NEW-2 는 orphan.
