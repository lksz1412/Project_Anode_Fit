# REVIEW1 — v7-06.tex 적대 검수 (검수 sub, 리뷰 전용)

대상: `v7-06/v7-06.tex` (785행, 전문 정독 head→tail). 판정 기준: `Anode_Fit_v11_final.py`(706행)·`v11_flowchart.md`·`AUTHOR_BRIEF.md` 전문 정독.
척추: §서론 spine TikZ + 9개 \section 이 N0–N9 순서 일치 확인. 수치 claim(U(298) 4건·z_cut 5%·dU_hys≥0)은 Python 직접 검산으로 PASS.

---

## A. 확정 결함 {심각도 · 행 · 무엇이 틀렸나 · 옳은 형}

| # | 심각도 | 행 | 틀린 내용 | 옳은 형 |
|---|---|---|---|---|
| D1 | **HIGH** | 578–579, 765–766(S6) | S6 `∂ln L_q/∂V<0` 를 부호 사슬 \checkmark 항목으로 제시. 그러나 코드 `A=min(z_cut·n·RT, A_cap·RT)`(L335)·`dH_a^eff`·`dS_a` 전부 V 무의존 → `func_L_q`(L96) 의 L_q 는 V 에 대해 **상수**. 실현 미분은 `=0`, `<0` 아님. 문건 스스로 "L_q 는…상수로 동결"(531), "전이당 상수…1회 평가"(587·461) 라 적어 **자기 모순**. | S6 은 "꼬리 컷점 **선택의 물리 동기**(컷을 더 깊은 affinity 로 잡을수록 짧아짐)"로 격하·표기. 곡선-실현 V-미분 아님을 명시. \checkmark 무근거. |
| D2 | **MED** | 447 (eq:xieq 박스 주석) | 박스 주석이 호출을 `func_ksi_eq(T, V_n, U, n, s)`·`z=s(V_n−U)/w` 로 적음. 실제 코드(L459)는 `func_ksi_eq(T_work, V_work, center, ...)` — 인자는 **V_work**(패딩 작업격자)·**center**(분기중심). | 2번째 인자를 `V_work`, 중심을 `center`(=U_j^d) 로. 본문은 §sec:pol·keybox 에서 V_work 를 세웠으므로 부호 논리는 무사하나, 박스만 보고 재현하면 그리드 패딩·분기중심을 놓침(G-usable). |
| D3 | **MED** | 573 (eq:Lqfull 직후) | "`func_L_q` 가…`dG_a=ΔH_a^eff−T·ΔS_a`" 라 단언. 코드 L95 는 `dG_a = dH_a − T*dS_a`(인자명 **dH_a**, eff 아님). eff 가 되는 건 호출자(L346)가 `dH_a_use` 를 넘기기 때문. | "`func_L_q` 의 `dH_a` 인자에는 호출 측이 이미 `dH_a_use(=ΔH_a^eff)` 를 넘긴다"는 한 문장 추가. 직접 호출 시 raw dH_a 넣으면 장벽 틀림(G-usable 함정). |

부호 8항 자체의 부호 방향은 전부 코드와 일치(아래 §C). D1 은 S6 의 *부호 부등호 자체*가 아니라 *코드 실현 여부* 결함(부호 방향 ✓, 그러나 "곡선에서 실현되는 사슬 항"이라는 지위가 거짓).

## B. 강점 3 · 약점 3

**강점**: (1) 척추 N0→N9 가 \section 9개와 정확히 1:1, spine TikZ·tab:nodemap 이 노드↔식↔코드식별자 닫음(완결성 우수). (2) eq:Lqfull 4개 항이 코드 L96 ln_Lq 와 항별 동형(T*/T·−ln(1+e^{−A/RT})·+dG_a/RT·−χ_d A/RT) — 검산 PASS. (3) 그림 4종 전부 신규 TikZ·내부 영어 ASCII·전부 \ref 사용(orphan 0), 각 그림이 앞 식 동기·뒤 본문 사용.

**약점**: (1=가장 약함) **D1/S6** — 부호 사슬 전수 검산표가 코드에서 실현 안 되는 항목에 \checkmark 를 부여해 "전건 정합·부호 결함 0"(771) 결론의 신뢰를 깎음. (2) D2 박스 인자명 V_n↔V_work 혼동 — 문건 G-usable 핵심 박스에서 발생. (3) D3 `dH_a` vs `dH_a_eff` 암묵 전제 — 직접 재현 독자 함정.

## C. 부호 8항 PASS/FAIL + 근거

| 항 | 판정 | 근거 |
|---|---|---|
| S1 `U_j=(−ΔH+TΔS)/F`, ΔG=−FU | **PASS** | eq:Uj(310) = func_U_j(L69). U(298) 4건 Python 검산 일치(0.211/0.140/0.120/0.085). ΔH<0 흡열 아님 서술 정확. |
| S2 `ξ_eq=logistic[σ_d(V−U)/w]` 방전 V↑→ξ↑ | **PASS**(주석 D2) | 부호 방향 = func_ksi_eq(L86–87) 일치. 단 박스 인자명 V_n→V_work 정정 필요(D2). |
| S3 `dξ/dV=σ_d ξ(1−ξ)/w`, peak 양수·방향불변 | **PASS** | eq:eqpeak(499). equilibrium()(L369) s=+1·raw U_j 고정인데 peak ξ(1−ξ)/w 가 s-불변이라 "충방전 불변·히스 미반영"(722) 정확. |
| S4 `ΔU_hys≥0`, Ω≤2RT→0; 중심 ±½σ_d | **PASS** | eq:dUhys(361)=func_dU_hys(L130). Ω=4RT→+54.8 mV≥0, Ω=2RT→0 Python 검산. U^dis>U^chg 정합. |
| S5 `χ_d`: 방전 χ/충전 1−χ; ΔH_a^eff=ΔH_a−χ_dΩ | **PASS** | eq:chid(549)=func_chi_d(L160), eq:dHeff(556)=func_dH_a_eff(L152). |
| S6 `∂ln L_q/∂V<0` | **FAIL (D1, HIGH)** | 코드 A·L_q V-무의존 상수(L335·463) → 실현 미분 0. \checkmark 무근거·자기 모순. |
| S7 충전 격자 역전 `ξ[::-1]…[::-1]`; 충전=방전 거울 | **PASS** | eq:reversal(634)=코드 L477 일치. |
| S8 `V_n=V_app−σ_d|I|R_n` | **PASS** | eq:vn(258)=코드 L412 일치. |

**부호 FAIL = S6 1건(D1, HIGH).** 나머지 7항 PASS.

## D. 차원 점수 (6 × 5 = /30)

| 차원 | 점수 | 사유 |
|---|---|---|
| 척추 N0→N9 순서·노드 커버 | 5/5 | 9 \section ↔ N0–N9 정확, tab:nodemap·spine 완결. |
| 부호 사슬(8항 코드 대조) | **3/5** | 7항 PASS·1항(S6) FAIL + 자기모순, "결함 0" 과잉 결론. |
| G-follow(따라가짐) | 4/5 | 절 도입·다리 충실. 단 S6 "V↑→A↑"가 코드 frozen-A 와 단절돼 따라가던 독자 혼란. |
| G-usable(재현) | 4/5 | tab:staging 초기값·z_cut·창 닫음. 단 D2(V_work)·D3(dH_a_eff) 박스 함정. |
| 완결성(orphan) | 5/5 | \ref/\eqref 93건 모두 정의 대응, eq:Lq(N8 인용) 포함 orphan 0. 그림·표 전부 본문 참조. |
| 형식(수식주도·전보체·다리) | 5/5 | 보편식 먼저·극한 코너케이스(Ω≤2RT,|I|→0), 절 도입/마무리 다리, 박스 식별자 1:1. |
| **합계** | **26/30** | |

---

## 반환 요약
합 26/30. CRIT 0 · HIGH 1(D1=S6) · MED 2(D2 박스 V_n↔V_work, D3 dH_a vs dH_a_eff). 부호 FAIL = **S6 1건**(`∂lnL_q/∂V<0` 가 코드 frozen-A 상수와 모순 → 실현 미분 0). 가장 약한 1곳 = **S6**: 부호 전수 검산표가 코드 미실현 항에 \checkmark 부여, "부호 결함 0" 결론의 신뢰 훼손.
