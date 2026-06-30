# REVIEW1 — v7-02.tex 적대 검수 (검수 sub, review-only)

대상: `Claude/results/v7-02/v7-02.tex` (863행, 14p, build PASS: 에러0·undefined0·overfull0)
정본: `Anode_Fit_v11_final.py` (706행) · `v11_flowchart.md` (N0–N9) · `AUTHOR_BRIEF.md`
검수 방식: master 직접 전문 정독(4파일) + 부호 8항 v11 1:1 대조 + 산술 재검산 + 빌드로그.

---

## A. 확정 결함 (심각도 · 행 · 무엇이 틀렸나 · 옳은 형)

### CRIT-1 — 𝒜 기호 이중 정의 → ∂lnL_q/∂V 부호 유도가 코드·자기식과 모순  (HIGH→CRIT: 부호체크 6항 직격)
- 행: eq:affinity L504 vs verifybox L564–566 (관련 N7 전체 §7, eq:lnLq L539)
- 틀림: L504 는 `𝒜 = min(z_cut·n_j·RT, A_cap·RT)` 로 **V 무관 상수**(코드 L335 와 1:1, 그리고 코드 L463 에서 L_q 는 전이당 T_rep 로 1회 산출 = **V_n 의존 전혀 없음**). 그런데 L565 는 같은 𝒜 를 `σ_d F(V_n−U_j^d)` 로 **재정의**해 `∂lnL_q/∂V_n = −χ_d σ_d F/RT < 0` 을 "유도". 두 𝒜 정의가 상호모순이고, v11 구현 기준으로는 ∂lnL_q/∂V_n = 0.
- 옳은 형: 𝒜(컷 affinity, 상수)와 구동력(σ_d F(V_n−U) — §6 L416 의 𝒜_j)을 **다른 기호로 분리**하라. ∂lnL_q/∂V<0 은 "코드의 per-transition L_q 가 실은 V 무관(전이당 1회)"임을 명시한 뒤, 연속극한의 정성 경향으로만 서술하거나, 컷점 q_a 가 V 따라 이동하는 경로 의존으로 재유도. 현재 박스의 등식 유도는 폐기.

### HIGH-2 — verifybox 물리 결론 오류: "방전 ICA peak 가 OCV peak 보다 낮은 전위"
- 행: L213–214 (분극 §, eq:vn L183 / eq:interp 복귀식 L706 과 충돌)
- 틀림: V_n=V_app−|I|R_n(방전) → V_app>V_n 까지는 맞으나, L483 역보간 후 L706 `V_app=V_n+σ_d|I|R_n` 이므로 **측정 peak 위치 V_app = U_j^d + |I|R_n > U_j^d** — 즉 방전 측정 peak 는 평형중심보다 **높은** V_app 에 온다. L214 "낮은 전위에 나타나는 이유" 는 정반대. "V_n<V_app"(상태변수 비교)을 "peak 가 낮은 전위"(측정축 위치)로 비약한 혼동.
- 옳은 형: "방전 측정 peak 는 OCV peak 보다 +|I|R_n 만큼 **높은** V_app 에 나타난다"(eq:interp 와 정합).

### HIGH-3 — ξ_eq 유도 비약(G-follow): RT → w_j 전이에서 n 인자 소실
- 행: L411–420 (eq:stationary → eq:xieq)
- 틀림: eq:stationary 지수는 `𝒜_j/RT` (𝒜_j=σ_d F(V_n−U)). eq:xieq 지수는 `σ_d(V_n−U)/w_j = σ_d F(V_n−U)/(n_j RT) = 𝒜_j/(n_j RT)`. "구동력을 폭 w_j 로 묶으면" 한 문장으로 RT→n_jRT 치환(=n 인자 도입)을 건너뜀. n=1 기본값에서만 수치 일치. BRIEF §4 "산문-only 유도단계 명시 중간식 승격" 위반.
- 옳은 형: 폭 척도 정의 `w_j=n_jRT/F` 를 명시 대입하는 중간식 1줄 추가(𝒜_j/(n_jRT)=σ_d(V_n−U)/w_j).

### MED-4 — 𝒜 기호 과적재(전역 일관성)
- 행: L416(𝒜_j=σ_d F(V_n−U_j^d), N5) vs L504(𝒜=상수 컷, N7)
- 틀림: 동일 기호 𝒜 가 §6 에선 V 의존 구동력, §7 에선 V 무관 컷 상한. 독자가 같은 양으로 오인(CRIT-1 의 뿌리). 기호사전(L152–159)엔 𝒜=컷형만 등재.
- 옳은 형: 둘 중 하나를 𝒜_drive / 𝒜_cut 식으로 구분, 기호표 반영.

### LOW-5 — 산술 표기 흠(결론은 정합)
- 행: L270–271. 298.15×29.0 = 8646.35 인데 본문 8647 로 반올림 후 합 20347 표기(정확 20346.35). 최종 0.2109 V 는 정합. 미세 표기 정밀도만.

---

## B. 강점 3 · 약점 3

강점:
1. 코드 1:1 대응이 촘촘(L번호·함수명 박스 인용 다수: L412/L68/L84/L133/L155/L149/L474–477/L481/L483). G-usable 높음 — §11 재현 지침+초기값표+Optuna 범위로 닫힘.
2. 부호 8항 중 핵심 6항(U_j·ξ_eq·dξ/dV·ΔU_hys±·χ_d/ΔH_eff·충전 격자역전·분극식)이 v11 과 부호·계수까지 정확. eq:lnLq 가 func_L_q(L90–97)와 항별 완전 일치(T_*·−ln(1+e^{−A/RT})·dG_a/RT·−χ_dA/RT).
3. 척추 N0→N9 순서·노드 100% 커버, 절 도입(앞 절 받은 것)·마무리(다음 절 다리) 규범 충실. 빌드 무결함(14p).

약점:
1. (가장 약한 1곳) **N7 동역학 §의 𝒜 처리** — 컷 affinity(상수)와 구동력(V 의존)을 한 기호로 뭉개 CRIT-1(∂lnL_q/∂V 유도 모순)·MED-4·HIGH-3 이 모두 이 영역에서 파생. 검수 적대 타깃 1순위.
2. 평형 점유 유도가 detailed-balance 정지점→logistic 으로 가는 길에 n 인자·w_j 치환을 산문으로 처리(HIGH-3).
3. 분극 verifybox 의 측정축 vs 상태변수 혼동(HIGH-2) — 물리 결론이 뒤집힘.

---

## C. 차원 점수 (6 × 5 = /30)

| 차원 | 점수 | 근거 |
|---|---|---|
| 1 spine N0–N9 정합 | 5 | 순서·노드 완전 커버, 절↔노드 1:1, 흐름도 figure 정확 |
| 2 부호 사슬 정확 | 3 | 8항 중 6항 PASS, 2항(∂lnL_q/∂V·peak 측정위치) FAIL — 핵심 클래스 |
| 3 G-follow(따라가짐) | 3 | ξ_eq n-인자 비약·𝒜 과적재로 중간 단계 추적 곤란 |
| 4 G-usable(재현·STAGING) | 5 | §11 닫힌 재현 지침·초기값표·Optuna 범위·round-trip, STAGING_LIT L535–564 정합 |
| 5 완결성 orphan | 4 | 도입/마무리 규범 충실, 모든 figure \ref 사용. 𝒜 기호만 사전 누락(MED-4) |
| 6 형식(수식주도·전보체·절다리·figure) | 4 | 수식주도·절다리 양호, figure 영어 ASCII·\caption 한글 규범 준수, build 무결. 괄호 동격 일부 잔존 경미 |
| **합** | **24/30** | |

---

## D. 부호 8항 PASS / FAIL (코드 v11 대조)

1. U_j(T)=(−ΔH+TΔS)/F — **PASS** (eq:Uj L239 = func_U_j L68–69, 부호·F 일치; ΔH<0 발열 서술 정확)
2. ξ_eq=logistic[σ_d(V_n−U)/w], 방전 V↑→ξ↑ — **PASS** (eq:xieq L419 = func_ksi_eq L84–87; 방향 서술 정확. *유도 경로는 HIGH-3 비약이나 결과식 부호는 정합*)
3. dξ/dV=σ_d ξ(1−ξ)/w → peak 양수·방향불변 — **PASS** (eq:dxidV L447, eq:eqpeak L461 방향불변 명시)
4. ΔU_hys≥0·Ω≤2RT→0·분기중심 ±½σ_d — **PASS** (eq:hysdU L309·L313 명시분기 = func_dU_hys L123–130; eq:hyscenter L322 = func_U_branch L138; 방전 +/충전 − 정확. 산술 54.9mV 재검산 정합)
5. χ_d 방전χ/충전1−χ·ΔH_a^eff=ΔH_a−χ_dΩ — **PASS** (eq:chid L524=func_chi_d L155–160; eq:dHeff L529=func_dH_a_eff L149)
6. ∂lnL_q/∂V<0 — **FAIL** (CRIT-1: 𝒜 재정의로 유도, 코드 L463 기준 per-transition L_q 는 V 무관 → 등식 유도 모순. 정성 경향만 참)
7. 충전 격자역전 ξ[::-1]…[::-1]·충전 dQ/dV=방전 거울(양수) — **PASS** (eq:reverse L617–623 = 코드 L474–477 1:1; 비물리 dQ/dV<0 회피 서술 정확)
8. 분극 V_n=V_app−σ_d|I|R_n — **PASS** (eq:vn L183 = 코드 L412; 단, 같은 절 verifybox L213–214 측정 peak 위치 결론은 HIGH-2 오류)

부호 요약: **6 PASS / 2 FAIL**(6항 CRIT, 8항은 식 PASS·동반 verifybox 결론 HIGH-2 오류).
