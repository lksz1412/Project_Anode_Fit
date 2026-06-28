# REVIEW2 — v7-02b.tex 적대 검수2 (검수 sub, review-only)

대상: `Claude/results/v7-02/v7-02b.tex` (875행, 14p, build PASS)
정본: `Anode_Fit_v11_final.py`(706행) · `v11_flowchart.md`(분극 2026-06-29 정정본) · `AUTHOR_BRIEF.md`
방식: REVIEW1 5결함(CRIT-1·HIGH-2·HIGH-3·MED-4·LOW-5) 반영 검증 + 식·부호사슬 단위청크 전문정독 + 코드 1:1 + 산술 재검산 + 빌드로그. refute·가장약한1곳·빈통과금지.

---

## ① 보완 반영 검증 (REVIEW1 결함별)

- **CRIT-1 (𝒜 이중정의 → ∂lnL_q/∂V 유도 모순) — FIXED.** grep 전수: 모든 `\mathcal{A}`(L159·174·510·513·517·522·523·527·549·550·557·574·757)가 컷점 상수(V_n 무의존) 의미로 통일. 구동력은 L416 `σ_d F(V_n−U_j^d)`로 풀어써 기호 분리. 오류 등식 §7 verifybox는 `∂L_q/∂V=0`(L574–576, 코드 L463 per-tr 1회 산출 근거)로 재작성 — 코드 정합.
- **MED-4 (𝒜 과적재·기호표 누락) — FIXED.** §5 eq:stationary에서 𝒜 제거(L417–420), 기호사전(L159)엔 컷형만 등재 — 이제 본문 사용과 사전 1:1.
- **HIGH-2 (방전 peak "낮은 전위" 부호역전) — FIXED·정합.** verifybox §2 L216–219: V_n=V_app−|I|R_n<V_app → peak@V_n=U_j^d → V_app=U_j^d+|I|R_n>U_j^d → "**높은** 전위" ✓. eq:interp(L718 V_app=V_n+σ_d|I|R_n) 및 flowchart 정정본(L88 "방전 측정 V_app가 평형 V_n보다 높다")과 일치. 박스 내부 모순 없음.
- **LOW-5 (산술 20347 표기) — 미수정(잔존).** L276 여전히 `8647`/`20347`(정확 8646.35/20346.35). 결론 0.2109 V는 정합(재검산 0.21088). NOTE급 표기정밀도만 — 무해.
- **HIGH-3 (eq:stationary→eq:xieq, n인자/RT→n_jRT 중간식 누락) — ★미수정(NEW 회귀, 아래 ②).** NOTEb 보완목록(1~4)에 HIGH-3 부재 — 침묵 누락.

검증 대상 3보완(𝒜 통일·verifybox peak 부호·의존성 표): **3/3 모두 정확 반영.**

## ② 신규 회귀 / 적발 (가장 약한 1곳 우선)

- **★HIGH-3 잔존 (가장 약한 1곳·G-follow 직격).** L415–416: "전위-구동력 `σ_d F(V_n−U_j^d)`를 폭 `w_j`로 묶어 쓰면" → eq:stationary(L419) 지수 `σ_d(V_n−U_j^d)/w_j`. 차원상 에너지(J/mol)를 `F·w_j=n_jRT`로 나눠야 무차원 지수가 나오는데("`w_j`로 묶어"가 아니라 `F w_j`로), `F(V_n−U)/(F w_j)=(V_n−U)/w_j` 또는 `=σ_d F(V_n−U)/(n_jRT)` 중간식 1줄이 여전히 부재. REVIEW1 HIGH-3 "옳은 형: 중간식 1줄 추가"가 미이행. n=1 기본값에서만 수치 일치. BRIEF §4(산문-only 유도단계 명시 중간식 승격) 위반 — REVIEW1 대비 **무변화**(악화는 아니나 미해결).
- **MED 신규 (eq:bv χ vs χ_d 다리 끊김).** L522–523 eq:bv는 `χ𝒜`/`(1−χ)𝒜`로 χ(무방향) 사용, 그러나 §7.2(L529–543)에서 χ_d(방전 χ/충전 1−χ)로 분기하고 eq:lnLq(L550)는 `χ_d𝒜/RT`를 씀. eq:bv→eq:lnLq 사이 "방전이면 χ_d=χ라 r_j^+가 율속"이라는 χ→χ_d 연결 문장이 약함(L532는 율속만 언급, χ=χ_d 등치는 암묵). G-follow 경미 비약 — 식 부호는 정합(방전서 χ_d=χ로 eq:bv와 일치).
- **부호 사슬 8항 신규 flip·orphan·다리끊김: 적발 0.** eq:reverse(L630–633)=코드 L474–477 1:1, eq:closed(L699)=L481, eq:hyscenter(L327)=func_U_branch L138 ±½σ_d 정확. 모든 figure(\ref) 사용, 신규 orphan 없음.
- **빌드:** `!` 에러 0, Overfull 0, Underfull badness 10000 ×2(L756·L758 의존성표 셀 — v7-02와 동수, 무회귀·cosmetic), 폰트 italic fallback 경고(kotex 상시·무해), 14p 출력.

## ③ 재점수 (6×5 = /30)

| 차원 | v7-02 | v7-02b | 근거 |
|---|---|---|---|
| 1 spine N0–N9 정합 | 5 | 5 | 순서·노드 완전, figure 정확 |
| 2 부호 사슬 정확 | 3 | **5** | CRIT-1·HIGH-2 정정 → 8항 전건 PASS(아래 ④). ∂L_q/∂V=0 코드정합·peak 측정위치 정합 |
| 3 G-follow | 3 | **3** | HIGH-3 n인자 비약 잔존 + eq:bv χ→χ_d 다리약함(MED신규) → 미상승 |
| 4 G-usable(재현·STAGING) | 5 | 5 | §11 닫힌 재현·초기값표·Optuna·round-trip, STAGING_LIT 정합 |
| 5 완결성 orphan | 4 | **5** | 𝒜 기호 사전 등재·본문 1:1(MED-4 해소), figure \ref 전수 사용 |
| 6 형식(수식주도·전보체·다리·figure) | 4 | 4 | 양호, build 무결, L276 산술표기·괄호동격 경미 잔존 |
| **합** | **24** | **27/30** | +3 (부호 +2·orphan +1; G-follow 정체) |

## ④ 부호 8항 PASS/FAIL (코드 v11 1:1 재대조)

1. U_j(T)=(−ΔH+TΔS)/F (ΔG=−FU, ΔH<0 발열) — **PASS** (eq:Uj L244=func_U_j L68; 재검산 U1=0.2109·U2=0.140 ✓)
2. ξ_eq=logistic[σ_d(V_n−U)/w], 방전 V↑→ξ↑ — **PASS** (eq:xieq L424=func_ksi_eq L84; 결과식 부호 정합. *유도 경로 HIGH-3 비약은 G-follow 흠, 부호는 무오류*)
3. dξ/dV=σ_d ξ(1−ξ)/w → peak 양수·방향불변 — **PASS** (eq:dxidV L452, eq:eqpeak L473 방향불변)
4. ΔU_hys≥0·Ω≤2RT→0·분기중심 ±½σ_d — **PASS** (eq:hysdU L314=func_dU_hys L123; eq:hyscenter L327=func_U_branch L138; 산술 54.9mV 재검산 ✓)
5. χ_d 방전χ/충전1−χ·ΔH_a^eff=ΔH_a−χ_dΩ — **PASS** (eq:chid L534=func_chi_d L155; eq:dHeff L539=func_dH_a_eff L149)
6. ∂lnL_q/∂V (=0, 𝒜 상수) — **PASS (b에서 FAIL→정정)** (L513–517·574–576 코드 L463 per-tr 1회 근거; eq:lnLq L549–550=func_L_q L96 항별일치 T_*·−ln(1+e^{−A/RT})·dG_a/RT·−χ_dA/RT)
7. 충전 격자역전 ξ[::-1]…[::-1]·충전 dQ/dV=방전 거울(양수) — **PASS** (eq:reverse L630–633=코드 L474–477)
8. 분극 V_n=V_app−σ_d|I|R_n·방전 peak>OCV peak — **PASS (b에서 verifybox FAIL→정정)** (eq:vn L186=L412; verifybox §2 L216–219 측정peak 高 정합)

부호 요약: **8 PASS / 0 FAIL** (v7-02 6P/2F → b에서 6·8항 정정 완료). 잔존은 부호결함 아닌 G-follow(HIGH-3·eq:bv) 흠.
