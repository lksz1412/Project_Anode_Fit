# REVIEW_A — v7-10.tex 적대 재검수 (검수 sub, 리뷰 전용)

대상: `D:\Projects\Project_Anode_Fit\Claude\results\v7-10\v7-10.tex` (880행, Ch.1 체리픽 통합본)
기준: `...\v7-00_spine\Anode_Fit_v11_final.py` (707행, 코드·기본값 정본) · `...\v7-00_spine\v11_flowchart.md` (분극 정정본)
방식: 식·부호사슬 단위 청크 전문 정독 + 수치 재산출(python) + 병렬 적대 에이전트 1마리(유도 무비약 전담).
판정 원칙: 빈 통과 금지. 아래는 refute mandate 로 실제 적발한 결함이다.

---

## A. 확정 결함 {심각도 · 행/식 · 틀림 · 옳은형}

### D1. [HIGH] L_q 유도 무비약 — `1/(1+e^{−𝒜/RT})` 인자 미유도
- 위치: tex L536 (k_j 정의) → L572 ("forward 극한과 k_0=k_BT/h 를 식~eqref{eq:Lq} 에 넣으면 ... L_q 가 된다") → 식 eq:Lqfull (L575).
- 틀림: 본문이 k_j 를 **단일 forward 지수** `k_j ≈ k_0 exp[−(ΔG_a−χ𝒜)/RT]` 하나로만 정의(L536)하고, 이를 L_q=|I|/(Q_cell·k_j) 에 "넣으면 된다"고 단언한다. 그러나 그 대입은 `(T_*/T)·exp[(ΔH_a^eff−TΔS_a)/RT]·e^{−χ_d𝒜/RT}` 만 주고, eq:Lqfull(과 코드 func_L_q L96 `−log(1+exp(−A/RT))`)의 분모 `1/(1+e^{−𝒜/RT})` 는 **유도 단계 없이 등장**한다.
- 수치 증거(직접 재산출): 코드 L_q = 2.91193e−08, 단일-지수 k_j 로 얻은 L_q = 2.96527e−08, 비 = 0.98201 = **정확히 1/(1+e^{−𝒜/RT})**. 곧 코드/박스는 옳고, **본문 유도가 그 인자를 못 낳는다**. (순rate k_fwd−k_rev 라면 (1−e^{−𝒜/RT}) 가 나오지 (1+…) 가 아님 — 2-state 완화율 k_fwd+k_rev 전제가 누락.)
- 옳은형: k_j 를 `k_fwd/(1+e^{−𝒜/RT})` (정·역 합 형태의 포화 완화율)로 명시하거나, eq:Lq→eq:Lqfull 사이에 그 정규화 단계를 한 줄 추가. **박스식·코드 정합은 그대로 유지(수정 불요), 유도 다리만 보충.**
- 비고: eq:Lqfull → 코드 ln_Lq 4항 1:1 일치는 재검 PASS (T_*/T·+dG_a/RT[dG_a=ΔH_a^eff−TΔS_a, L342-346 확인]·−log(1+e^{−A/RT})·−χ_d A/RT). 결함은 오직 (1+e^{−A/RT}) **출처**.

### D2. [MEDIUM] logistic detailed-balance 유도에서 폭 다중도 n 소실
- 위치: tex L446-448 (유도 서술) → 박스 eq:xieq (L450), 폭 `w_j=n_jRT/F`.
- 틀림: 본문이 구동력 `𝒜=sF(V_n−U)` 와 Boltzmann 비 `e^{𝒜/RT}` 로 풀면 ξ_eq 가 닫힌다고 하나, 그 대수는 `w=RT/F`(곧 **n=1**)만 준다. 박스·코드(func_ksi_eq L86 `z=s(V−U)/func_w(T,n)`, func_w=nRT/F)는 `w=n_jRT/F` 인데, 다중도 n 이 유도 어디에도 들어오지 않는다.
- 옳은형: 구동력을 `𝒜=sF(V−U)/n_j` 로 두거나 Boltzmann 지수를 `𝒜/(n_jRT)` 로 적어야 `ξ_eq=logistic[s(V−U)/w], w=n_jRT/F` 가 닫힘. 박스/코드 정합, **유도 서술만 n 도입 보충**.

### D3. [LOW] z_cut=4.357 의 "ξ_eq 5% 컷" 라벨 오기 (개념 혼동)
- 위치: tex L541 "z_cut=4.357 이 ξ_eq 의 5% 컷에 대응" / 코드 주석 L216 "z_cut=4.357 = ξ_eq 5%".
- 틀림: z=4.357 → ξ_eq=0.9873 (곧 1−ξ=**1.27%**, 5% 아님). 실제로 5%인 것은 **미분** ξ(1−ξ)/0.25 = **정확히 0.05**. L540-541 의 다른 서술("원천 dξ_eq/dq 가 정점의 ~5%로 떨어지는 좌표")은 옳음 — 그 옆 괄호 라벨 "ξ_eq 의 5%"만 미분→점유 혼동.
- 옳은형: "ξ_eq 의 5% 컷" → "원천 미분 dξ_eq/dq 가 정점의 5%로 떨어지는 컷"(=ξ_eq(1−ξ_eq)/¼=5%). 본문 L540 표현과 통일. (코드 주석 L216 도 동일 오기지만 코드는 검수 범위 밖 — 본문만 정정 권고.)

### D4. [LOW] 두 spinodal 끝점 부호 약칭 "(1−2ξ)=∓u" 표기
- 위치: tex L363 "$(1-2\xi)=\mp u_j$".
- 틀림: 순서 (ξ_s^−, ξ_s^+)=(½(1−u), ½(1+u)) 에서 (1−2ξ) 는 각각 (+u, −u) = "±u"(상단 +). 본문 ∓ 는 부호 순서가 뒤집힘. (박스 eq:dUhys 자체는 정확 — 재유도·수치 모두 PASS, 순전히 prose 약칭.)
- 옳은형: "(1−2ξ)=±u" 또는 "극대에서 +u, 극소에서 −u".

---

## B. 가장 약한 3곳 (refute — 빈 통과 금지)

1. **eq:Lqfull 유도 다리 (D1, 최약)**: 박스·코드가 옳다는 사실이 "유도가 옳다"를 가리고 있었음. 단일 지수 k_j → 분모 (1+e^{−A/RT}) 미생성을 수치(비 0.98201)로 못박음. **이 문건의 한 핵심 주장("이 문건만 보고 코드 재현")이 가장 위태로운 자리** — 독자가 L536 k_j 로 L_q 를 짜면 1.8% 어긋난 꼬리를 얻는다.
2. **logistic n 소실 (D2)**: detailed-balance 한 줄이 n=1 만 닫는데 박스는 n_jRT/F. 부호는 맞아 S2 검산을 통과하지만, "수식이 논리를 운반"하는 본 문건 기조에서 운반 사슬 한 칸이 비어 있음.
3. **부호 검산 §sec:signcheck 의 S6 자기참조(L837-840)**: "운영상 실현 미분 ∂lnL_q/∂V=0" 이라 부등식 <0 을 "동기로만 성립"이라 변호 — 논리적으로 자기무모순이나, **검산이 검산 대상을 스스로 재정의**해 빠져나가는 구조라 가장 공격받기 쉬운 부호 항. (결함으로 확정하진 않음: 동결+컷규칙 정당화가 일관 — 단 가장 약한 통과.)

---

## C. 부호 사슬 8항 PASS/FAIL (v11 코드 1:1 재대조)

| # | 항목 | 코드 대조 | 판정 |
|---|------|-----------|------|
| S1 | U_j=(−ΔH+TΔS)/F, ΔG=−FU | func_U_j L69 `(-dH_rxn+T*dS_rxn)/F`; ΔH<0→중심↑ | **PASS** |
| S2 | ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ | func_ksi_eq L86 `z=s*(V_n−U)/func_w` | **PASS**(유도 다리 D2 별건) |
| S3 | dξ/dV=σ_d ξ(1−ξ)/w, peak |·|≥0 방향불변 | L468 `ksi_eq*(1-ksi_eq)/w`, ξ(1−ξ)≥0 | **PASS** |
| S4 | ΔU_hys≥0/±, Ω≤2RT→0, 분기 ±½σ_d | func_dU_hys L127-130, func_U_branch L138 `0.5*sigma_d*h_eta*gamma*dU`; U_dis>U_chg | **PASS** (수치 86.69mV/u=0.766 일치) |
| S5 | χ_d 충전 1−χ, ΔH_a^eff=ΔH_a−χ_d·Ω | func_chi_d L160 `chi if s>=0 else 1-chi`; func_dH_a_eff L152 | **PASS** |
| S6 | ∂lnL_q/∂V 컷상수 동기(실현=0) | _resolve_lag_length 컷 A=min(...) L335, 전이당 스칼라 | **PASS**(B-3 최약 통과) |
| S7 | 꼬리 충전 격자역전 ξ[::-1]…[::-1] | L477 `_causal_lowpass(ksi_arr[::-1],…)[::-1]` | **PASS** |
| S8 | 분극 V_n=V_app−σ_d|I|R_n, 방전 측정>내부 | dqdv L412 `V_in - sigma_d*I_abs*self.Rn`; flowchart L88 정정본과 정합 | **PASS** |

**부호 8항: 8/8 PASS — 숨은 flip·자기모순 0.** (S2 는 부호 PASS, 유도 무비약은 D2 로 분리 계상.)

---

## D. 인자표·재현 박스·staging 표 검증

### tab:inputs (L750-772) — 전 기본값 코드 1:1
모든 칸 일치(코드 __init__ L220-231 + GRAPHITE_STAGING_LIT):
z_cut 4.357 ✓ · A_cap_RT 4.0 ✓ · use_w_eff False ✓ · use_dH_eff True ✓ · x/chi 0.5 ✓ · chi_split func_chi_d ✓ · Rn 0.0 ✓ · Cbg 0.0 ✓ · w_eff_floor_frac 0.05 ✓ · grid_pad_lo/hi 0.15 ✓ · n_work_min 2048 ✓ · min_lag_grid_steps 2.0 ✓ · v_span_floor 1e−6 ✓ · seed_T/I/Q_cell 298.15/0.1/1.0 ✓ · h_eta 1.0 ✓ · dS_a 0 ✓ · Omega/gamma 0,0 ✓ · n 1 ✓ · dVdq_qa 0 ✓.
**인자표 오류 = 없음(0 칸).** 단 D3(z_cut 라벨)·D5(아래) 주의.

- **D5. [LOW] tab:inputs 식 참조 오기 (L753)**: `w 또는 n` 행이 `(eqref{eq:weff})` 를 가리키나, 기본 폭은 `w_j=n_jRT/F`(eq:Uj 인접 본문 식, 정확히는 eq 폭정의)이고 eq:weff(L439)는 **옵션 w^eff** 전용. nodemap 표(L810)는 N4 를 옳게 eq:weff 로 묶되 func_w/func_w_eff 둘 다 적음. 기본 폭 식(w=nRT/F)에 별도 라벨이 없어 tab:inputs 가 옵션식으로 잘못 가리킴. → 기본 폭식 라벨 신설 후 참조 교정 권고(경미).

### 6단계 재현 박스 (keybox L781-789) — 식 참조 검증
(1)~(6) 단계 식 참조 모두 정합: n0map·vn·vwork(1·2) / Uj·center·weff·xieq(3) / Acut·chid·dHeff·Lqfull·LV(4) / eqpeak·peakshape·reversal, `L_V<2Δ_grid` 문턱(5, =min_lag_grid_steps 2.0 코드 L466) / sum 역보간(6). **6단계 식 참조 오류 = 없음.** (단 (3)의 weff 참조가 D5 와 동일 — 기본 폭 라벨 부재.)

### tab:staging (L719-730) — GRAPHITE_STAGING_LIT 대조
| stage | U | ΔH_rxn | ΔS_rxn | Q | Ω | ΔH_a | dVdq_qa | 판정 |
|---|---|---|---|---|---|---|---|---|
| 4→3 | 0.210 | −11700 | +29.0 | 0.10 | 6000 | 48000 | 0.30 | ✓ |
| 3→2L | 0.140 | −13500 | 0.0 | 0.12 | 8000 | 46000 | 0.30 | ✓ |
| 2L→2 | 0.120 | −13100 | −5.0 | 0.25 | 10000 | 44000 | 0.30 | ✓ |
| 2→1 | 0.085 | −13000 | −16.0 | 0.50 | 13000 | 40000 | 0.30 | ✓ |
코드 L535-563 와 전 칸 일치. U(298) 재산출: 0.2109/0.1399/0.1203/0.0853 V — 표 목표 U 와 모두 정합. **staging 표 오류 = 없음.**
(주: dH_a/dS_a 는 표 캡션 범위 밖이라 미수록 정상. 폭 w 폴백 0.020/0.016/0.014/0.012 은 본문 L732 에 별도 서술 — 코드 일치.)

---

## E. 극한 재검 (refute mandate 3)
- Ω≤2RT → ΔU_hys=0: 코드 L75/func_dU_hys L127 명시분기 ✓, 2RT=4957.6 J/mol(본문 4958 ✓), 연속(u→0) ✓.
- |I|→0 평형환원: L_V∝|I|(T_*∝|I|) → 0, L_V<2Δ_grid 분기 → eq:eqpeak 평형종, σ_d 불변 ✓.
- γ=0: center=U_j(L453 else), 분기 소멸 ✓.
모두 PASS.

---

## F. v7-11 보완 권고 (우선순위)
1. **(D1, 必)** eq:Lq→eq:Lqfull 사이 1줄: k_j 를 정·역 합 완화율 `k=k_fwd(1+e^{−𝒜/RT})^{-1}` 로 명시하거나 정규화 단계 삽입. 박스·코드는 불변.
2. **(D2, 권)** logistic 유도 서술에 다중도 n 도입(구동력/n 또는 Boltzmann 지수 𝒜/(nRT)). 박스 불변.
3. **(D3, 권)** L541 "ξ_eq 의 5% 컷" → "원천 미분 5% 컷"(L540 표현과 통일).
4. **(D5, 경)** 기본 폭식 `w=nRT/F` 라벨 신설, tab:inputs L753·keybox(3) 참조를 eq:weff(옵션) 에서 기본식으로 교정.
5. **(D4, 경)** L363 "(1−2ξ)=∓u" → "±u".
모두 **유도 서술·라벨 교정**이며 박스 결과식·코드 정합·부호 8항은 손대지 않는다(회귀 위험 0).

---
**총평**: 박스 결과식·코드 정합·부호 8항·인자표·staging·6단계 재현은 모두 PASS(수치 못박음 완료). 결함은 **유도 무비약 2건(D1 HIGH·D2 MEDIUM)** + 라벨/표기 3건(D3·D4·D5 LOW). 한 번에 OK 아님 — v7-11 에서 D1·D2 다리 보충 필수.
