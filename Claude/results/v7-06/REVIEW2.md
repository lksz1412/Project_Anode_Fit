# REVIEW2 — v7-06b.tex 적대 검수2 (검수 sub, 리뷰 전용)

대상: `v7-06/v7-06b.tex` (819행, 전문 정독 head→tail). 기준: `Anode_Fit_v11_final.py`(707행)·`v11_flowchart.md`(분극 정정본)·`AUTHOR_BRIEF.md` 전문 정독.
임무: ① 보완 4건(REVIEW1 의 D1/D2/D3 + ∂lnL_q 자기모순) 반영 검증 ② ★새 회귀 적발 ③ 재점수/30 ④ 부호 8항 재판정.
수치 claim(R1–R4·U(298)·z_cut 5%)은 Python 독립 재산출로 검증.

---

## ① 보완 반영 검증 {결함 · 위치 · 코드 대조 · 판정}

| 보완 | 위치 | 코드 대조 | 판정 |
|---|---|---|---|
| **D1/S6 ∂lnL_q/∂V<0 자기모순** | 584–591(§7 부호의 핵심) + 776–779(S6) + R4(800–802) | `A=min(z_cut·n·RT, A_cap·RT)`(L335)·`_resolve_lag_length`(L307–351)에 **V 인자 없음** → L_q 는 전이당 스칼라. 본문이 "운영상 실현 미분 ∂lnL_q/∂V=0(전이당 한 스칼라)" + "부등식 <0 은 컷 규칙의 *물리적 동기*(국소 구동력 A=σ_dF(V_n−U) 로 두면 V↑→A↑→장벽↓→L_q↓)" 로 분리 서술. \|I\| 의존(L_q∝\|I\|→0)은 동결 뒤에도 살아 평형 환원함을 별도 명시. | **반영 완료**. 자기모순 해소. S6 \checkmark 근거 회복(미실현 항에 부여한 \checkmark → "물리적 동기 + 실현 0" 으로 정확화). |
| **D2 박스 V_n→V_work** | 447·451(§5 codebox) + 162–164(§1 규약 박스) | 코드 L459 `func_ksi_eq(T_work, V_work, center, n_j, sigma_d)` 와 박스 인자 1:1. §1 박스는 격자 무관 일반형 `[σ_d(V−U)/w]` 로 중립화(forward-ref 회피). | **반영 완료**. 박스만 보고 재현해도 V_work·center 안 놓침. |
| **D3 dH_a vs dH_a_eff 전제** | 576–579(§7 eq:Lqfull 직후) | 코드 `_chi_and_dH_eff`(L302–303): `use_dH_eff=True` 일 때만 ΔH_a−χ_dΩ, False 면 dH_a_use=ΔH_a. 본문 "식 ΔH_a^eff 는 func_L_q 의 dH_a 인자 dH_a_use 이고 use_dH_eff=True 일 때만 eq:dHeff 와 같다 — 꺼지면 그대로 ΔH_a" 추가. | **반영 완료**. 직접 호출 함정 제거. |
| **§10 부호-감사 절 유지** | 760–805(sec:signcheck) | S1–S8 전수 + 신규 verifybox(R1–R4). | **유지·강화**. |

**수치 재산출(Python, T=298.15):** R1 dU_hys=86.686 mV(문건 86.7), u=0.76607(문건 0.766), 2RT=4957.6(문건 4958) — **일치**. R2 Ω=2RT=4957.6 J/mol→u=0→dU=0 — 일치. z_cut=4.357→ξ_eq=0.9873, bell/peak=ξ(1−ξ)/0.25=0.0500 — "5% 컷" 정확. U(298) 4건=0.2109/0.1399/0.1203/0.0853(목표 0.210/0.140/0.120/0.085) — 일치.

## ② ★ 신규 회귀 (보완 4건이 들인 새 결함)

**보완 4건 + verifybox 가 들인 신규 회귀 = 0.** 정정은 전부 국소(박스 인자·1줄 전제·S6 재서술·신규 박스)이며 절 순서·spine·preamble 불변. \eqref 추가분(eq:vwork·dHeff·Lqfull·dUhys·Ubranch·branch·eqpeak·LV) 전부 기존 라벨 → undefined 0. verifybox env=L36 정의됨. 부호 단조성 진술 불변.

**refute / 가장 약한 1곳 — 빈 통과 거부:**

| # | 심각도 | 행 | 내용 | 비고 |
|---|---|---|---|---|
| N1 | **LOW** | 587–589(§7), 778(S6) | "국소 구동력 A=σ_dF(V_n−U)" 로 단조성을 논증. 그러나 코드의 컷 affinity 는 **n·RT 스케일**(A=z_cut·nRT) 이고 여기 쓴 σ_dF(V_n−U) 는 §5 eq:xieq 유도의 *logistic 구동력*(442행)이다. 둘은 차원은 같으나 *다른 양*(전자=컷 동결 전, 후자=평형 점유용). "장벽↓" 단조 동기는 옳으나, 동일 기호 𝒜 를 두 맥락에 써 G-follow 독자가 "컷 A 가 곧 σ_dF(V_n−U)" 로 오독할 여지. **새 회귀 아님**(D1 정정이 도입했으나 물리 진술 자체는 옳음) → 정정 권고지 결함 아님. |
| N2 | **LOW(pre-existing, 비-회귀)** | 433–436(eq:weff) | w_eff=(RT/F)(1−Ω/2RT) 는 Ω>2RT 에서 **음수**(검산: Ω=6000→−5.4 mV, Ω=13000→−41.7 mV). 본문 "Ω→2RT 에서 0 으로 가므로 floor 클립" 은 Ω→2RT⁺ 근방만 맞고, staging 기본값(Ω=6000~13000≫2RT)에선 음수→floor 로 강제 클립됨. 코드 `func_w_eff`(L141–146) `np.maximum(w_eff, floor)` 가 정확히 이 음수를 막음(코드는 옳음). **boforse 가 안 건드린 초본 잔존 항목** → 신규 회귀 아님. use_w_eff 기본 False 라 곡선 미사용·§10 감사 범위 밖. |

N1·N2 모두 boforse 라운드가 **들인** 결함이 아니다. 신규 회귀는 0.

## ③ 부호 8항 재판정 (코드 v11 대조)

| 항 | 판정 | 근거(행) |
|---|---|---|
| S1 U_j=(−ΔH+TΔS)/F, ΔG=−FU | PASS | eq:Uj(310)=func_U_j(L69). U(298) 4건 재산출 일치. |
| S2 ξ_eq=logistic[σ_d(V−U)/w] 방전 V↑→ξ↑ | **PASS(D2 정정 반영)** | 박스 인자 V_work·center 정정(447·451)=L459. 단조성 불변. |
| S3 dξ/dV=σ_d ξ(1−ξ)/w peak 양수 | PASS | eq:eqpeak(498–502)=L468·L370. 방향 불변. |
| S4 ΔU_hys≥0, Ω≤2RT→0; ±½σ_d | PASS | eq:dUhys(361)=func_dU_hys(L130). R1=+86.7·R2=0 재산출. U^dis>U^chg. |
| S5 χ_d 방전χ/충전1−χ; ΔH_a^eff=ΔH_a−χ_dΩ | **PASS(D3 보강)** | eq:chid(551)=L160, eq:dHeff(559)=L152. use_dH_eff 분기 명시(576–579). |
| S6 ∂lnL_q/∂V<0 | **PASS(D1 정정)** | 실현 미분=0(A 컷상수 L335·V 무인자 L307) + 부등식=물리 동기. 본문과 무모순(584–591·776–779·R4). 자기모순 해소. |
| S7 충전 격자역전 ξ[::-1]…[::-1]; 충전=방전 거울 | PASS | eq:reversal(644–645)=L477. peak_shape>0. |
| S8 V_n=V_app−σ_d\|I\|R_n | PASS | eq:vn(258)=L412. flowchart 정정본(분극 부호 88행) 정합 — 방전 측정>내부, 본문 262행 일치. |

**부호 결함 0** (S6 FAIL → 정정 PASS). 신규 R1–R4 회귀 self-test 도 수치 재산출 전건 일치.

## ④ 재점수 (6 × 5 = /30)

| 차원 | v7-06 | v7-06b | 변동 사유 |
|---|---|---|---|
| 척추 N0→N9 | 5/5 | **5/5** | spine·tab:nodemap 불변. |
| 부호 사슬(8항) | 3/5 | **5/5** | S6 자기모순 해소+\checkmark 근거 회복, verifybox R1–R4 falsifiable 고정으로 회귀 가드. "결함 0" 결론 신뢰 복원. |
| G-follow | 4/5 | **5/5** | S6 "V↑→A↑" 단절 해소(실현 0 vs 동기 분리), 독자 혼란 제거. (N1 동일기호 오독 여지 −0 미만, 감점 안 함.) |
| G-usable | 4/5 | **5/5** | D2(V_work·center 박스)·D3(dH_a_use 전제) 함정 제거 → 박스 직접 재현 가능. |
| 완결성(orphan) | 5/5 | **5/5** | \eqref 추가분 전부 정의 대응, undefined 0. |
| 형식 | 5/5 | **5/5** | 보편식 먼저·다리·1:1 박스 불변, verifybox 형식 정합. |
| **합계** | **26/30** | **30/30** | |

---

## 반환 요약
합 **30/30**(v7-06b, ↑26 from v7-06). 보완 4건(D1 ∂lnL_q 자기모순·D2 V_work·D3 dH_a_eff·§10 유지) **전부 코드 대조 반영 확인**. R1–R4·U(298)·z_cut 5% **Python 독립 재산출 일치**. **신규 회귀 0**(N1·N2 는 boforse 미도입 — N1=동일기호 𝒜 오독 여지 LOW, N2=eq:weff 음수→floor pre-existing·곡선 미사용). 부호 8항 전건 PASS(S6 FAIL→정정 PASS), CRIT/HIGH/MED 0. 가장 약한 1곳 = N1(컷 affinity 𝒜 와 logistic 구동력 σ_dF(V−U) 동일기호 — 물리 옳으나 표기 분리 권고).
