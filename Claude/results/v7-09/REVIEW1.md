# REVIEW1 — v7-09.tex 적대 검수 (검수 sub, v7-09)

> 대상: `Claude/results/v7-09/v7-09.tex` (555행, 전문 정독 head→tail).
> 기준: `v7-00_spine/Anode_Fit_v11_final.py`(707행)·`v11_flowchart.md`·`AUTHOR_BRIEF.md` 전문 정독.
> 역할: 리뷰 전용 — 어떤 파일도 수정·커밋하지 않음. 본 .md 1개만 생성.

---

## A. 확정 결함 {심각도 · 행 · 무엇이 틀렸나 · 옳은 형}

### CRIT-1 — N3 폭이 점유율을 "계산"한다는 절 제목·도입의 spine 노드 오배치
- 심각도: **HIGH** (CRIT 아님 — 부호는 맞음, spine 노드 라벨이 어긋남)
- 행: §3 제목 L215 `폭과 평형 점유율` + L94 그림 `n4\\width`, L95 `n5\\ksi_eq` / L97 `n8\\lowpass`.
- 틀림: flowchart 의 노드 번호와 문건 절(N0–N9)·그림 박스 라벨이 **불일치**. flowchart 는
  N2=평형중심, **N3=히스테리시스 분기**, **N4=폭**, **N5=평형점유 ξ_eq**, **N6=평형 peak**,
  N7=L_V, N8=인과꼬리, N9=합산. 그런데 본 문건은 §3=폭·점유율, §4=평형 peak, §5=히스,
  §6=L_V, §7=인과꼬리, §8=합산으로 재배열했다. AUTHOR_BRIEF §3 은 "순서 고정"이되
  히스(N3)를 평형 peak 뒤(브리프 절6)로 옮기는 것을 **명시 허용**(brief 절5→6 순서)하므로
  절 재배열 자체는 위반 아님. 그러나 **그림(fig:spine)의 박스 텍스트가 flowchart 의 N-번호를
  그대로 베껴** `n4=width n5=ksi_eq n6=peak n7=L_V n8=lowpass n9=sum` 로 찍혀 있어,
  본문 절 번호(N3=폭·점유, N4=peak, N5=히스, N6=L_V, N7=꼬리, N8=합산, N9=역보간)와
  **번호가 어긋난다**. 독자가 그림의 n5(ksi_eq)를 본문 §5(히스)로 오인.
- 옳은 형: fig:spine 의 노드 텍스트를 본문 절 번호 체계(N0=inputs … N9=interp)에 맞추거나,
  최소한 캡션에서 "그림 노드 번호 = flowchart 원번호, 본문 절 번호와 다름"을 명시.

### HIGH-2 — §6 L_q 박스(eq:Lq)에서 `−χ_d A` 항이 ln 식과 폐형에서 **이중 계상 위험 표기**
- 심각도: **MEDIUM**
- 행: eq:lnLq L379–383, eq:Lq L384–389.
- 검증: v11 L96 `ln_Lq = log(T_attempt/T) − log(1+exp(−A/RT)) + dG_a/(RT) − x·A/(RT)`, x=chi_d.
  문건 폐형 eq:Lq 는 `exp[(ΔG_a^eff − χ_d A)/RT]·(1+exp[−A/RT])^{−1}` — 지수 안에 `−χ_d A` 정확히 1회,
  prefactor 에 `(1+e^{−A/RT})^{−1}` 정확히 1회. **이중 계상 아님 — 정합 PASS**. (적대 검산 결과 무결.)
  → 잠정 의심 철회. 결함 아님.

### HIGH-3 — §6 본문 "∂lnL_q/∂V<0" 명제의 **유도 누락** (G-follow 비약)
- 심각도: **HIGH**
- 행: L401 `식 eq:lnLq 에서 V 가 커져 cutoff affinity 가 커지면 −χ_dA/(RT) 항이 작용해 ln L_q 가 감소`.
- 틀림: 본문은 "A 가 V 와 함께 커진다"를 **전제 없이 선언**한다. 그러나 eq:Acut(L358) 의
  `A=min(z_cut|n|RT, A_cap RT)` 는 **V 에 의존하지 않는 상수**(전이당 고정)다. v11 L335 도
  `A = min(z_cut·n_safe·RT, A_cap·RT)` — V_work 미포함. 즉 코드에서 A 는 V 무관 상수이고,
  L_q 는 전이당 1회 산출(L462–464, T_rep·대표 n). 따라서 "V 가 커지면 A 가 커진다"는 **코드와 모순**.
  flowchart 부호규약 L89 `∂lnL_q/∂V<0` 는 v5 의 연속 affinity(A=sF(OCV−U)) 맥락의 잔재이며,
  v11 은 그 연속식을 컷 상수 A 로 대체(L326–331 주석이 명시)했다. 본 문건은 그 대체를 §6 에서
  설명하고도(L356–360) L401 에서 옛 연속 서술을 끌고와 **자기모순**.
- 옳은 형: L401 을 삭제하거나 "v11 에서 A 는 컷 상수라 L_q 는 V 에 직접 의존하지 않는다; 전위 의존은
  ξ_eq·occ_lagged 차이로 들어간다"로 정정. (AUTHOR_BRIEF §8-6 의 ∂lnL_q/∂V<0 체크는 v5 연속식 기준
  — v11 컷 상수 모델엔 부적용임을 NOTE 에 적었어야 함.)

### HIGH-4 — G-usable 미달: 곡선 재현에 필요한 수치 인자 표가 **불완전**
- 심각도: **HIGH**
- 행: L199–211 staging 표.
- 틀림: 표가 `U,w,Q,Omega,dH_rxn,dS_rxn` 6열만 싣고 **동역학 인자 전부 누락**:
  `dH_a`(48000/46000/44000/40000), `dVdq_qa`(0.30), `dS_a`(0). 이들 없이는 §6–§7 의 L_q·L_V·꼬리를
  **재현 불가**(G-usable 정면 위반). 또 생성자 기본값(z_cut=4.357, A_cap_RT=4.0, x=χ=0.5, Rn,
  min_lag_grid_steps=2.0, n_work_min=2048, grid_pad_lo/hi=0.15, w_eff_floor_frac=0.05, v_span_floor)
  중 **어느 것도 수치로 명시 안 됨** — 본문은 식별자만 부르고 값을 안 준다. AUTHOR_BRIEF §4 G-usable
  "z_cut·창·초기값·진행이 닫혀야"·"GRAPHITE_STAGING_LIT 초기값·각 인자 의미 표 포함"을 **명시 위반**.
- 옳은 형: staging 표에 dH_a·dS_a·dVdq_qa 열 추가 + 생성자 기본 인자값 표(또는 본문 수치) 1개 신설.

### MED-5 — eq:facade(L77–82) I_abs 분기의 변수명 충돌
- 심각도: **LOW**
- 행: L79 `\texttt{I\_abs}, & \texttt{I\_abs} 가 주어질 때`.
- 틀림: 좌변 수학기호 I_abs(=|I|)와 코드 키워드 인자 `I_abs`(curve 의 Optional)를 같은 글리프로 써서
  자기참조처럼 보인다. v11 L507–511 은 `if I_abs is None: I_use=c_rate·Q_cell else I_use=I_abs`.
  의미는 맞으나 표기상 `I_{abs}= I\_abs` 가 동어반복으로 읽힘.
- 옳은 형: 코드 인자는 `\texttt{I\_abs}_{\mathrm{arg}}` 등으로 구분.

### MED-6 — §0 본문 "q=Q/Q_cell 환산" 누락
- 심각도: **MEDIUM**
- 행: §0 (sec:n0, L118–148) 전체.
- 틀림: AUTHOR_BRIEF §3-1·flowchart N0 은 `q=Q/Q_cell` 환산을 N0 도입 항목으로 요구. 본 문건은
  Q_cell 을 입력 집합 eq:n0input 에 넣되 **q=Q/Q_cell 정의식·역할(L_q→무차원, T_attempt 의 I/Q_cell)을
  본문에서 명시 안 함**. eq:Tattempt(L377) 에서 I_abs/Q_cell 이 불쑥 등장(앞 도입 없음 = orphan 직전).
- 옳은 형: §0 에 q=Q/Q_cell 한 줄 도입 후 §6 에서 사용.

---

## B. 강점 3 · 약점 3 (가장 약한 1)

**강점**
1. 부호 4개소(분극·logistic·분기중심·충전 격자역전)를 keybox(L550–552)로 명확히 닫음 — §8 부호 핵심 8항 중 부호 자체는 전부 v11 정합.
2. eq:closedcode(L493–500)의 "or 는 수학적 자유선택이 아니라 코드 branch" 명시 — peak_shape 2-branch 의 코드 충실도 높음(v11 L466–479 정확 반영).
3. 충전 격자역전(eq:chglowpass L435–438 `[L(ξ[::-1])][::-1]`)을 v11 L477 과 1:1, 비인과 방지 근거까지 서술 — N8 핵심 정확.

**약점**
1. **(가장 약한 1곳) G-usable 미달(HIGH-4)**: 동역학 인자(dH_a·dVdq_qa·dS_a) 표 누락 + 생성자 기본값 전부 미명시 → "이 문건만으로 v11 재현" 불가. 브리프 최우선 요구(§4) 정면 미달.
2. ∂lnL_q/∂V 자기모순(HIGH-3): 컷 상수 A 를 도입하고도 V-의존 서술을 끌고와 모순.
3. fig:spine 노드번호 vs 본문 절번호 불일치(HIGH-1).

---

## C. 차원 점수 (6 차원 × 5점 = /30)

| 차원 | 점수 | 근거 |
|---|---:|---|
| 1. 구조·spine 정합 | 3/5 | 절 순서는 브리프 허용 범위, 그러나 fig:spine 노드번호 어긋남(HIGH-1)·N0 q환산 누락(MED-6). |
| 2. 물리·부호 사슬 | 4/5 | 부호 8항 전부 v11 정합. 감점 = ∂lnL_q/∂V 서술이 컷상수 모델과 모순(HIGH-3, 부호 아닌 단조성 주장). |
| 3. G-follow | 3/5 | logistic·분극은 따라가짐. A 의 V-의존 비약(HIGH-3)·q 미도입(MED-6)으로 §6 중간 끊김. |
| 4. G-usable(재현) | 2/5 | 동역학 인자·생성자 기본값 표 부재(HIGH-4). 식 사슬은 있으나 수치가 안 닫혀 코드 작성 불가. |
| 5. 완결성 orphan | 4/5 | 대부분 앞도입·뒤사용. I/Q_cell·q 가 도입 없이 §6 등장(경미 orphan). |
| 6. 그림·시각·형식 | 4/5 | 그림 전부 신규 TikZ·영어 ASCII·\ref 연결·절 다리 양호. 감점 = fig:spine 번호 혼동. |
| **합** | **20/30** | |

---

## D. 부호 8항 PASS/FAIL (v11 대조)

1. U_j(T)=(−ΔH+TΔS)/F — **PASS** (eq:Uj L184 = v11 L69).
2. ξ_eq=logistic[σ_d(V−U)/w] — **PASS** (eq:ksieq L244 = v11 L86–87, z 정의에 σ_d).
3. dξ/dV=σ_d ξ(1−ξ)/w, peak 양수 — **PASS** (eq:dxidv/absdxidv L277–279).
4. ΔU_hys≥0, Ω≤2RT→0; 분기 ±½σ_d h_η γ — **PASS** (eq:dUhys L303–312·eq:Ubranch L316 = v11 L123–138).
5. χ_d 방전 χ/충전 1−χ; ΔH_a^eff=ΔH_a−χ_dΩ — **PASS** (eq:chid L363·eq:dHeff L372 = v11 L160·L152).
6. ∂lnL_q/∂V<0 — **FAIL** (L401): v11 에서 A 는 V-무관 컷 상수(L335)·L_q 는 전이당 1회 산출 → "V↑→A↑→lnL_q↓" 서술이 코드와 모순. 식 자체(eq:lnLq/eq:Lq)는 v11 정합이나 **단조성 주장이 틀림**.
7. 충전 격자역전 ξ[::-1]…[::-1], 충전=방전 거울 — **PASS** (eq:chglowpass L435–438 = v11 L477).
8. 분극 V_n=V_app−σ_d|I|R_n — **PASS** (eq:polar L156 = v11 L412).

부호 8항: **7 PASS / 1 FAIL(6번)**.

---

## E. 분량 결함 여부 (가장 짧은 후보 점검)
- 곡선식 누락: **있음** — staging 동역학 인자(dH_a 등) 표 누락(HIGH-4)으로 L_q 수치 닫힘 결손.
- 유도 생략: logistic 의 통계역학(정규용액 μ)에서의 유도가 **전혀 없음**(브리프 §3-4 요구) — ξ_eq 를 "코드의 func_ksi_eq 그대로"(L242)로만 제시. ΔU_hys 의 spinodal 유래도 결과식만(eq:dUhys) 제시, 유도 0.
- → 분량 자체가 결함(브리프 "수식 주도 유도" 미달): logistic·spinodal·BV/Eyring(L_q) 어느 것도 *유도*되지 않고 코드식 전사. **HIGH 급 추가 약점**.
