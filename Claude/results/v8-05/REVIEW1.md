# REVIEW1 — v8-05.tex 적대 검수 (검수 sub, 리뷰 전용)

대상: `Claude/results/v8-05/v8-05.tex` (1140행, 전문 정독 1–1140).
기준 정독: `Anode_Fit_v11_final.py`(L60–484 핵심 함수·dqdv), `v11_flowchart.md`, `AUTHOR_BRIEF_v8.md`, `KNOWN_DEFECTS.md`(전수 대조).
판정 자세: refute mandate·가장 약한 1곳·빈 통과 금지.

---

## 1. 확정 결함 (증거 동반)

### ★C1 (CRITICAL) — D-PEAK 미수정·verbatim 상속
KNOWN_DEFECTS ★D-PEAK 가 **그대로 살아 있다.** v8-05 L889–890:
> "$L_V$ 가 작으면 $\rho\to0$ 이라 $\xi_\mathrm{lag}\to$ 한 칸 뒤처진 $\xi_\eq$ 가 되어, 식~\eqref{eq:peakshape} 가 이산 미분 $\to\dd\xi_\eq/\dd V$ 의 종으로 환원된다"

이는 수학적으로 **틀림**(KNOWN_DEFECTS L6–10): $\xi_{lag,i}=\rho\xi_{lag,i-1}+(1-\rho)\xi_{eq,i}$ 에서 $L_V\to0\Rightarrow\rho\to0\Rightarrow\xi_{lag,i}\to\xi_{eq,i}$(**같은 칸**, 한 칸 뒤처진 게 아님) $\Rightarrow$ peak $\to0$ (종 아님). 종 환원은 **반대 극한 $L_V\gg\Delta_{grid}$**($\rho\to1$)에서 성립. 작은 $L_V$ 평형 회복은 *코드의 eq:branch 스위치*(L466 `lag_len_V < min_lag·grid_step → ξ_eq(1−ξ_eq)/w`)가 담당 — 매끈한 극한 아님. v8-05 는 eq:branch(L892–900)를 *별도로* 옳게 적었으나, 바로 위 prose 가 틀린 "매끈한 종 환원"을 그대로 주장 → 자기 본문 내 모순. **v8-04 자체 감사가 선적발한 ★최우선 결함을 v8-05 가 수정 안 함.**

### C2 (HIGH) — D-VEQ forward-defer 순환 부분 잔존
eq:Veq(L449)의 다리 $g_j'(\xi)=sF(V_\eq-U_j)$ 가 L441–447 에서 평형조건 eq:eqcond 인용으로 정당화되나, eq:eqcond(§3 L337) 자체는 비배치 자유에너지 기준이고 $g'(\xi)$(배치 몫 포함)와의 연결은 §6 detailed balance(eq:stationary, L601)에 가서야 닫힌다. KNOWN_DEFECTS D-VEQ 가 요구한 "inline 1줄(stationary $RT\ln[\xi/(1-\xi)]=\mathcal A$ 합류)"이 §4(eq:Veq 위치)에 없음 — §6 forward-defer 순환 완전 해소 안 됨. (§6 에서 사후 닫히므로 C1 보다 경미.)

### C3 (MEDIUM) — fig 캡션 일부 "v7-11 유래"인데 데이터 신규 의심·중복 미해소
KNOWN_DEFECTS fig:overshoot 지적(fig:hysloop 와 곡선 byte 동일·분기 라벨 뒤바뀜)은 v8-05 에 fig:overshoot 자체가 **부재**(제거됨)라 직접 적용 X — 단 fig:hysloop(L512–538) 1개만 남아 중복은 해소. 잔여: eq:eyring(eq:bv 의 Eyring $k_0=k_BT/h$, L759)·bazant2013·dreyer2010 가 본문에서 미인용(thebibliography 에만 존재, LOW).

---

## 2. KNOWN_DEFECTS 보유표 (v8-05)

| 결함 | 등급 | v8-05 상태 | 증거 |
|---|---|---|---|
| ★D-PEAK | CRITICAL | **보유(verbatim)** | L889–890 틀린 종 환원 prose |
| D-VEQ | HIGH | 부분 보유 | eq:Veq(L449) §6 forward-defer, §4 inline 다리 없음 |
| D-DHEFF | — | **수정됨** | eq:bv(L580)→eq:db→eq:kuniv(L759 $r^+=k_0e^{-(\Delta G_a-\chi A)/RT}$) 중간식 보유 |
| D-WEFF | — | **수정됨** | eq:isoslope(L562) $4RT-2\Omega$ 중간식 + $4Fw^\eff$ 다리(L566) 보유 |
| D-UBR | — | **수정됨(현상학 명시)** | L487–497 "spinodal 대칭+방향별 한 자유도 $\gamma$" ansatz 명시 |
| D-VN | LOW | 보유(자명) | eq:vn(L266) 이항 1줄(KNOWN_DEFECTS 도 minor·자명 인정) |
| fig:overshoot 중복 | — | **해소(그림 제거)** | fig:hysloop 단독 |
| eyring/bazant/dreyer 미인용 | LOW | 보유 | 본문 \cite 없음 |

→ **9종 중 핵심 ★D-PEAK 미수정**, D-VEQ 부분만. D-DHEFF/D-WEFF/D-UBR 3종은 유도 복원 양호.

---

## 3. 강점 3 · 약점 3

강점: ① 부호 8항 v11 1:1 완전 일치(아래 §5) + S1–S8 전수 검산절 + R1–R4 falsifiable 수치 회귀(L1107–1126) — G-usable 1급. ② D-DHEFF·D-WEFF·D-UBR 유도 사슬을 중간식과 함께 복원(eq:isoslope·eq:bv·ansatz 명시) — 브리프 §3 G-derive 충실. ③ 배치(N0→N9 절 순서·결과 박스·표 4종·식별자) v7-11 보존, 코드 식별자 전수 정합(L412/L335/L466–479 등).

약점: ① **★D-PEAK 미수정** — 검토1 단계가 잡아야 할 최우선 결함이 본문에 verbatim 잔존(C1). 체리픽/최종이 반드시 고쳐야 함. ② D-VEQ §4 inline 다리 누락(C2). ③ eq:Acut 의 $z_{cut}=4.357$ 가 "$\dd\xi_\eq/\dd q$ 의 5% 컷"(L791)이라 했으나 5%↔4.357 의 수치 연결(어느 미분의 5%인지 계산)은 미제시 — G-derive 한 칸 점프(MINOR).

---

## 4. 차원 점수 (합 /35)

| 차원 | 점수 | 근거 |
|---|---|---|
| G-derive(유도 완결성) | 3/5 | D-DHEFF/WEFF/UBR 복원 양호하나 ★D-PEAK 틀린 유도 잔존·z_cut 점프 |
| 배치 보존 | 5/5 | N0–N9·박스·표·식별자 v7-11 1:1 |
| 부호 8항 v11 1:1 | 5/5 | 전수 일치(§5) |
| G-follow(따라가짐) | 4/5 | 절 도입/마무리 다리 양호·forward-defer 1곳 |
| G-usable(사용성) | 5/5 | 6단계 재현 박스+R1–R4 수치+입력표 완비 |
| 완결성(orphan) | 4/5 | \ref 정합·미인용 3건(LOW) |
| 그림 | 4/5 | 영어 ASCII 준수·fig:overshoot 중복 제거·신규 다수, fig 데이터 검증은 정성 |
| **합** | **30/35** | |

(★D-PEAK 1건이 G-derive 를 끌어내림 — 정확성 외 모든 축은 우수.)

---

## 5. 부호 8항 검산 (v11 코드 대조 — 전수 PASS)

| # | 항 | v8-05 | v11 코드 | 일치 |
|---|---|---|---|---|
| 1 | $U_j=(-\Delta H+T\Delta S)/F$ | eq:Uj L351 | func_U_j L69 | ✓ |
| 2 | $\xi_\eq=$logistic$[\sigma_d(V-U)/w]$ 방전 V↑→ξ↑ | eq:xieq L609 | func_ksi_eq L86–87 | ✓ |
| 3 | $d\xi/dV$ peak 양수·방향불변 | eq:eqpeak L711 | L468/L370 | ✓ |
| 4 | $\Delta U_\hys\ge0$·$\Omega\le2RT\to0$·분기 $\pm\tfrac12\sigma_d$ | eq:dUhys L474·Ubranch L490 | func_dU_hys L127–130·func_U_branch L138 | ✓ |
| 5 | $\chi_d$ 충전 $1-\chi$·$\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ | eq:chid L807·dHeff L816 | func_chi_d L160·func_dH_a_eff L152 | ✓ |
| 6 | $\partial\ln L_q/\partial V$ 컷상수→운영 0(부등식=동기) | L844–849·S6 L1097 | A=const L335·func_L_q L96 | ✓ (flowchart 부등식과 정합 처리) |
| 7 | 꼬리 충전 격자역전·충전 dQ/dV 방전거울 양수 | eq:reversal L910 | L474–477 `[::-1]…[::-1]` | ✓ |
| 8 | $V_n=V_\app-\sigma_d|I|R_n$ 방전 측정>내부 | eq:vn L268·L272 | L412 | ✓ (flowchart 2026-06-29 정정과 일치) |

부호 8항 **전수 PASS** — 부호 결함 0.

---

## 6. 체리픽 적합도 (엄격)

**조건부 강후보 — 단 ★D-PEAK 수정 전엔 최종 불가.**
- 부호 8항 1:1·배치 보존·G-usable·D-DHEFF/WEFF/UBR 유도 복원은 9종 중 상위로 추정(타 v8 미대조이나 자체 기준 우수).
- 그러나 **검토1 단계가 잡아야 할 ★최우선 D-PEAK 가 본문에 verbatim 잔존**(C1)은 체리픽 *그대로 채택* 차단 사유. KNOWN_DEFECTS L22 "체리픽·최종은 D-PEAK 전부 수정한 유도로"를 v8-05 가 충족 못 함.
- 권고: v8-05 의 §8 인과꼬리 절(L880–900) **C1 수정**(틀린 종 환원 prose 삭제 → (a) 연속 정당화는 $L_V\gtrsim\Delta_{grid}$, (b) 작은 $L_V$ 평형 회복은 eq:branch 스위치로 명시) + C2 inline 다리 추가 시 → **최종서 1순위 베이스 후보**로 승급 가능. 현 상태 점수 30/35(C1 -3, C2/C3 -2).
