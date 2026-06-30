# ROUND_usable — v7-11.tex G-follow / G-usable 통독 검수

검수 sub(리뷰 전용). 대상 = `v7-11/v7-11.tex`(890행) 서론→N9→부호검산 전문.
기준(정독) = `v7-00_spine/Anode_Fit_v11_final.py`(707행). 절 단위 청크 통독,
refute mandate·가장 약한 1곳·빈 통과 금지. 수치 주장은 직접 재산출로 검증.

판정 요약: **재현(G-usable) 닫힘 = YES** (6단계 박스 + tab:inputs + tab:staging + tab:nodemap
만으로 v11 곡선 코드 끝까지 작성 가능). **G-follow 절단(막힘) = 0** (학부생이 앞 식+본문만으로
따라감). 잔존 결함 = LOW 1건(코드박스 반올림 표기 0.0855 vs 0.0853) + INFO 2건.

---

## 1. G-follow 막힘 목록 (전제 없는 등장·비약·미정의 기호)

통독 결과 **읽기를 끊는 막힘(blocker) = 0건.** 각 절이 앞 식만으로 닫히는지 절별 확인:

- 서론·N0(§1.1) PASS — σ_d/|I|/V_n/ξ_j/Q_j 전부 도입 자리에서 정의, 기호표(longtable)가
  본문 등장 전에 깔림. 그림 spine 이 절 순서=노드 순서를 미리 고정.
- N1 분극(§1.2) PASS — V_app→V_n 부호 논증(방전 측정>내부)이 식 eq:vn 전에 말로 닫힘.
  작업 격자 V_work(eq:vwork)도 "꼬리 여유" 동기 제시 후 식.
- N2 중심(§1.3) PASS — G,μ→평형조건(eq:eqcond)→U_j(eq:Uj) 사슬이 한 절 안에서 연속.
  ΔG=−sFU 부호 핵심을 명시.
- N3 히스(§1.4) PASS — g(ξ)(eq:gxi)→2계미분→spinodal(eq:spinodal)→gap(eq:dUhys)→
  분기중심(eq:Ubranch)→center(eq:center) 단계가 끊김 없이 이어짐. artanh 전개 각주.
  fig:hysloop 가 과주행 그림으로 직관 보강.
- N4·N5 폭/점유(§1.5) PASS — eq:wbase(기본 폭) → eq:weff(옵션) → ξ_eq(eq:xieq).
  ★보완된 두 다리(line 463: "n_j 는 eq:wbase 의 w=n_jRT/F 로 분모에 들어간다",
  V_work 평가전위 회수)가 logistic 분모의 n_j 출처와 평가격자 혼동을 정확히 막음.
- N6 평형peak(§1.6) PASS — 보존식 미분 → 종 항등식 dξ/dz=ξ(1−ξ) → 연쇄율 dz/dV=σ_d/w
  → eq:eqpeak. 위치·순높이 Q/(4w)·면적 Q 세 양을 한 식에서 읽어줌.
- N7 지연(§1.7) PASS — 보편 1계식(eq:Lq) → 컷 affinity(eq:Acut) → χ_d(eq:chid) →
  ΔH_a^eff(eq:dHeff) → L_q(eq:Lqfull) → L_V(eq:LV). 정·역 합 k=k⁺(1+e^{−A/RT})가
  분모 1/(1+e^{−A/RT})의 출처임을 §1.7.4 첫 줄에서 명시(★보완 다리, line 546·582).
- N8 꼬리(§1.8) PASS — 지수기억 일반해 → 이산 점화식(eq:lowpass) → peak_shape(eq:peakshape)
  → 분기(eq:branch) → ★충전 격자역전(eq:reversal). 역전의 인과(미래 기억 금지) 논증이
  식 전에 옴. fig:reversal 좌우 패널.
- N9 합산(§1.9) + 부호검산(§1.10) PASS — eq:sum, S1–S8 체크리스트, R1–R4 수치 회귀.

미정의 기호 잔존: **없음.** k_0=k_BT/h, T_*, q_a, T_rep 모두 등장 자리에서 정의.

---

## 2. G-usable 닫힘 여부 (재현 코드 끝까지 작성 가능한가 / 빠진 것)

**닫힘 = YES.** 6단계 박스(keybox, line 791-799) + tab:staging(line 723) +
tab:inputs(line 751) + tab:nodemap(line 807)을 직접 따라 L_q/L_V를 손으로 재산출한 결과,
코드값과 동일 경로로 닫힘(아래 검증). 닫히지 않은 식·빠진 인자 = 없음.

직접 재현 검증(tex 식만 사용, 코드 미참조):
- U(298) 4건: eq:Uj 로 0.2109/0.1399/0.1203/0.0853 → tab:staging 의 0.210/0.140/0.120/0.085
  와 정합(✔ U 폴백=열역학 환산 목표 일치 주장 line 743 참).
- 히스 R1: Ω=12000,γ=1 → u=0.7661, ΔU_hys=86.69 mV → 본문 "u=0.766, 86.7 mV"(line 863) 정확.
- 히스 문턱 R2: Ω=2RT=4957.6 J/mol → u=0, ΔU_hys=0 → 본문 4958 J/mol·0.0 mV(line 866) 정확.
- z_cut=4.357 → ξ_eq 미분 ξ(1−ξ)/0.25 = 0.0500 (정확히 5%) → 본문 "미분 5% 컷"
  표기(line 552, ★보완: "점유 자체 아니라 미분 기준" 명시)와 정합. ✔
- L_q 끝까지: eq:Acut(A=min(z_cut·n·RT, A_cap·RT), 2→1 에서 cap 9915<10800 binding) →
  eq:dHeff(ΔH_a^eff=40000−0.5·13000) → eq:Lqfull → eq:LV(×|dVdq_qa|=0.30) 로
  L_q=7.92e-9, L_V=2.37e-9 산출 — tex 식 체인만으로 닫힘. ✔

기본 폭 참조(eq:wbase) 정확성:
- eq:wbase: w_j=n_jRT/F. 코드 func_w = n*R*T/F 동일. ✔
- eq:xieq logistic 분모가 w_j(=eq:wbase)임을 line 463 에서 명시 — eq:wbase 참조 일치. ✔
- 'w' 직접 주면 n=wF/RT 역산(_n_factor, line 446·192) — tab:inputs line 763 "w 또는 n"
  도 정합. ✔
- eq:weff 는 (RT/F)(1−Ω/2RT) (n 없음) — 코드 func_w_eff(line 144) 와 동일(n 미포함).
  본문 line 453 "기본은 w=n_jRT/F, narrowing 은 명시 켤 때만" 으로 두 폭 구분 정확.
  → INFO(아래 I-2): n 처리가 base 와 eff 에서 다른 점은 코드 충실 재현이나 학부생 첫 독해
  시 미세 혼동 여지(정합성 결함 아님).

전 인자 망라(tab:inputs) 점검 — 코드 생성자 시그니처(line 220-231)와 1:1 대조:
- 전이 dict 키: U/(dH_rxn,dS_rxn), w/n, Q, Omega, gamma, h_eta, dH_a/dS_a, dVdq_qa,
  L_V, z_cut, A_cap_RT, use_w_eff, use_dH_eff — **전부 표에 있음.**
- 생성자: x/chi, chi_split, Rn, Cbg, use_dH_eff, use_w_eff, z_cut, A_cap_RT,
  w_eff_floor_frac, grid_pad_lo/hi, n_work_min, min_lag_grid_steps, v_span_floor,
  seed_T/I/Q_cell — **전부 표에 있음**(v_span_floor·seed 까지 line 779-780).
- 호출: V_app,T,c_rate/I_abs,Q_cell,direction — 표에 있음.
- 빠진 인자 = **0건.** (tab:staging 의 staging 폭 폴백 0.020/0.016/0.014/0.012 도 line 742
  에 명시.)

초기값(tab:staging) 닫힘: 4 전이 × (U, ΔH_rxn, ΔS_rxn, Q, Ω, ΔH_a, |dV/dq|) 전부 수록,
+ 본문 line 742 가 w 폴백·n=1·ΔS_a=0 보충 → transitions dict 완전 구성 가능. ✔

초기값(tab:staging) 대 코드 GRAPHITE_STAGING_LIT(line 535-564) 전수 대조: 7열 4행 전부 일치
(ΔH_rxn −11700/−13500/−13100/−13000, ΔS_rxn +29/0/−5/−16, Q 0.10/0.12/0.25/0.50,
Ω 6000/8000/10000/13000, ΔH_a 48000/46000/44000/40000, dVdq 0.30 ×4). ✔ 0 오류.

---

## 3. 절 도입/마무리 다리 · 체리픽(graft) 이음새

- 절간 다리 PASS: 각 절 끝이 다음 절을 호명("다음 절은 …로 들어간다" line 297·337·402·478·528).
  N5 끝(line 478)→N6, N6 끝(line 527)→N7 자연 연결.
- graft 인자표(§1.9.1 tab:staging, §1.9.2 tab:inputs) 이음새 PASS: line 719-721 이
  "이 표가 있어 이 문건만으로 재현 가능"으로 N9 합산식(eq:sum) 직후에 자연 삽입. 앞(eq:sum
  보존식)과 뒤(facade §1.9.3)와 매끄럽게 이어짐 — 인자표가 떠 있지 않고 재현가능성 주장에
  묶임.
- tab:nodemap(§1.9.3) 이 절 순서=노드 순서를 닫아 facade 까지 회수. 이음새 결함 0.

---

## 4. 새 유도 문장(F1/F2/F3 보완) 읽기 흐름 점검

v7-11 헤더(line 4-5)가 명시한 보완 다리 3건이 흐름을 끊는지 점검:
- F1 = eq:wbase 기본 폭 번호식(line 441-444): PASS. N4 첫 식으로 자연 도입, 이후 eq:xieq·
  tab·nodemap 이 \eqref 로 참조 — orphan 아님(앞 도입·뒤 사용).
- F2 = L_q 분모 1/(1+e^{−A/RT}) 정·역 합 유도(line 546·582): PASS. §1.7.1 끝과 §1.7.4
  첫 줄에 "정·역 합 k=k⁺(1+e^{−A/RT}) … 분모가 여기서 온다"로 삽입 — 한 문장 다리,
  eq:Lqfull 분모 출처를 닫고 흐름 단절 없음.
- F3 = logistic 폭 다중도 n_j 전파 + z_cut 미분 5% + spinodal 부호순(line 463·552·368):
  PASS. n_j 전파는 eq:xieq 직후 한 절(line 463), 5% 는 컷 정의 괄호(line 552), 부호순은
  eq:dUhys 유도 줄(line 368) — 모두 기존 문장에 흡수, 새 문단 비대 없음.

새 문장이 만든 비약·중복 = 없음.

---

## 5. 잔존 결함 (심각도·행)

| # | 심각도 | 행 | 내용 |
|---|--------|-----|------|
| D1 | LOW | line 333-334 | codebox: "(13000−298.15×16)/96485 ≈ **0.0855** V" — 실제 산출 = **0.0853** V (반올림 표기 오류). 목표 0.085 와의 정합 주장 자체는 유효(0.0853→0.085)하므로 재현·부호 비차단. 0.0855→0.0853 정정 권고. |
| I-1 | INFO | line 524 | eq:eqpeak 순높이 "Q_j/(4w_j)" — ξ=½에서 ξ(1−ξ)=¼ 라 정확. (검증 통과, 기록용.) |
| I-2 | INFO | line 449·453·463 | 기본 폭은 w=n_jRT/F(n 포함), 옵션 w_eff=(RT/F)(1−Ω/2RT)(n 미포함). 코드 충실 재현이나, use_w_eff 켤 때 n_j 가 폭에서 빠지는 점은 본문에 명시되지 않음(코드 _width line 287 도 w_eff 분기서 n 미사용). 학부생 첫 독해 시 미세 혼동 여지 — 한 줄 각주 권고(결함 아님, 개선 제안). |

부호 사슬(S1–S8·R1–R4) 통독: 코드 부호와 8/8 정합(V_n=V_app−σ_d|I|R_n, ξ_eq σ_d 부호,
peak 양수·방향불변, ΔU_hys≥0·방전+/충전−, χ_d 합1, A 크기 방향무관·χ_d 가 방향, 충전 격자역전).
R1–R4 수치 전건 재산출 일치. 부호 결함 = 0.

---

## 6. 반환 6줄

1. G-follow 막힘 수 = **0** (서론→N9→부호검산 전 절 앞 식만으로 따라감, 미정의 기호 0).
2. G-usable 닫힘 = **YES** — 6단계 박스+tab:inputs+tab:staging+tab:nodemap 으로 L_q/L_V
   끝까지 직접 재산출 성공, 빠진 인자 0(생성자·dict·호출 인자 코드와 1:1).
3. 기본 폭 참조 eq:wbase(w=n_jRT/F) 정확, eq:xieq 분모 n_j 출처 명시·코드 func_w 정합.
4. graft 인자표·F1/F2/F3 새 유도 이음새 매끄러움(앞 도입·뒤 사용, orphan 0, 흐름 단절 0).
5. 잔존 결함 = LOW 1(line 333-334 codebox 0.0855→0.0853 반올림 오타, 재현·부호 비차단)
   + INFO 2(순높이 검증통과·w_eff n 처리 각주 제안).
6. **가장 약한 1곳 = line 333-334 codebox U(298) 표기 0.0855** (실제 0.0853) — 유일한
   수치 오타. 영향 LOW(목표 0.085 정합 유지)이나 falsifiable 수치라 정정 권고.
