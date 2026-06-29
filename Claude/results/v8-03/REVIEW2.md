# REVIEW2 — v8-03b.tex 검토2 (검수 sub, v8-03b 단일 대상)

> 방법: 대상 전문 정독(1099행) + 기준 v11_final.py(706줄)·AUTHOR_BRIEF_v8.md·REVIEW1·NOTEb 전수 대조.
> 식·유도 단위 청크 정독 + master 직접 수치 재현(scratchpad: dpeak_test.py·dpeak_test2.py·selftest_num.py·weff_bridge.py).
> ★master 지시 핵심 = "D-PEAK 정정이 *옳은지 직접 검산*" — 수행: 이산 저역통과 (ξ_eq−ξ_lag)/L_V 를 L_V 변화로 실측.

---

## 1. 보완 5개 반영 점검 (REVIEW1 결함 → v8-03b 처리)

| # | 결함(REVIEW1) | v8-03b 위치 | 반영 판정 | 근거 |
|---|----------------|-------------|-----------|------|
| D-VEQ (H2) | eq:Veq forward-defer | 431-440 | **반영 O** | eq:gder(g'(ξ)) 추가 + sF(V_eq−U)=g'(ξ) 경유 inline. 대수 자체정합(eq:gder→eq:Veq 1:1). 순환 제거. |
| D-DHEFF (H1) | χ_d 계수 점프 | 805-815 | **부분 반영** | 방전 ξ→1·충전 ξ→0 깊은 꼬리 A_j→sF(V−U)+Ω 극한을 *명시*. 단 "Ω가 전진장벽 χ_dΩ 낮춤"의 χ_d 계수 자체는 여전히 BEP-split 손짓(`r⁺=k₀e^{−(ΔH_a−χ_d·A)/RT}`류 중간식 부재). 박스값 정확. |
| D-WEFF (H3) | 중심기울기 중간식 누락 | 596-603 | **반영했으나 ★새 오류** | g''|_{1/2}=4RT−2Ω(eq:gpp) 다리 추가됐으나 **곱 인자 오기**(아래 §2-N1). 박스 w_eff=(RT/F)(1−Ω/2RT)는 정확(func_w_eff L144 1:1). |
| orphan fig (H4) | fig:logistic·fig:reversal \ref 0 | 680, 916 | **반영 O** | 8 fig 전부 본문 \ref 정확히 1회(audit). dangling ref 0. |
| **D-PEAK (C1/C2)** | L_V→0 거짓 환원 | **886-901 / 1078-1081** | **★불완전·부분 역행**(아래 §5) | verifybox R3는 정정 정확(스위치 대체). 그러나 N8 본문은 *반대로 잘못된* 새 framing 도입. |

요지: D-VEQ·orphan = 깨끗 해결. D-DHEFF = 부분(박스 OK). D-WEFF = 박스 OK·다리 새 오류. **D-PEAK = R3는 옳으나 본문이 역행** — master 가설 적중.

---

## 2. ★신규 회귀 (v8-03→v8-03b 편집이 *새로* 만든 결함)

| 라벨 | 라인 | 결함 | 심각도 | 근거(수치) |
|------|------|------|--------|-----------|
| **N1 (D-WEFF 다리)** | **597-598** | "이상 기울기가 **(4RT−2Ω)/RT 배**로 줄어" — **인자 4배 오기**. 곡률비 g''(Ω)/g''(0)=(4RT−2Ω)/**(4RT)**=1−Ω/2RT 가 박스로 연결되는 정확한 인자. (4RT−2Ω)/RT 는 Ω=0 에서 **4**(=불변이어야 할 자리)·물리적 "감소 인자" 아님. | **HIGH(유도)** | weff_bridge.py: text_factor(Ω=0)=4.000 vs correct 1.000; w_eff/w_base=1−Ω/2RT. 박스는 정확, *다리만* 오류. |
| **N2 (D-PEAK 본문)** | **886-901** | N8 본문이 새로 도입한 framing 이 검증 물리와 **정반대**(§5 전개). (a)"L_V<νΔgrid 에서 한칸이동근사 유효→수렴", (b)"L_V→0 이라 peak→0 아니다…매끄럽게 이어진다", (c)"매끈 종 환원은 L_V≫Δgrid 가 아니라 **L_V≪Δgrid 에서** 연속". 세 주장 모두 거짓. | **CRITICAL** | dpeak_test.py: L_V≪Δgrid(ρ→0)서 tail/true_bell=**0.0005**(peak→0). L_V≫Δgrid(ρ→1)서 0.97(수렴). 정확히 *뒤집힘*. |
| N3 (자체모순) | 886-901 vs 1078-1081 | N8 본문(N2)과 verifybox R3 가 **상호 모순**: R3="스위치가 평형 종으로 *대체*"(옳음) vs 본문="분기 없이 연속 환원"(틀림). 같은 문건 두 곳이 반대 서술. | HIGH | 직접 대조. |

기타 비-회귀(유지): 부호 8항·4 모범 사슬·코드 1:1·표·그림 ASCII — 편집이 손상 안 함(§3·§4).

---

## 3. 부호 사슬 8항 (S1–S8, v11 코드 1:1 재확인)

| 항 | 명제 | 판정 | 근거 |
|----|------|------|------|
| S1 | U_j=(−ΔH+TΔS)/F, ΔG=−sFU | PASS | eq:Uj(331)↔func_U_j L69. U(298)=0.0853(selftest_num 검증). |
| S2 | ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ | PASS | eq:xieq(668)↔func_ksi_eq L86. |
| S3 | dξ/dV peak 양수·방향불변 | PASS | eq:eqpeak(727)↔L370/468. |
| S4 | ΔU_hys≥0/Ω≤2RT→0/분기±½σ_d | PASS | eq:dUhys(474)·eq:Ubranch(486)↔func_U_branch L138. selftest: u=0.766·86.69 mV·2RT→0. |
| S5 | χ_d 충전1−χ/ΔH_a^eff=ΔH_a−χ_dΩ | PASS | eq:chid(802)·eq:dHeff(811)↔func_chi_d L160·func_dH_a_eff L152. |
| S6 | ∂lnL_q/∂V: 컷상수→운영0(부등식=동기) | PASS | 834-837·S6(1061) 자기모순 0. |
| S7 | 꼬리 충전 격자역전/dQ/dV 방전거울(양수) | PASS | eq:reversal(913)↔L474-477 ξ[::-1]…[::-1]. |
| S8 | 분극 V_n=V_app−σ_d|I|R_n(방전 측정>내부) | PASS | eq:vn(254)↔L412. |

**부호 박스 결함 0/8 유지.** 단 *유도 다리* 부호 비정합은 잔존(M1): §3 eq:gder `+Ω(1−2ξ)` vs §4(582) ξ-규약 μ `−Ω(1−2ξ)` — 같은 ξ 에 Ω 부호 반대(g_j 와 ḡ 의 상호작용 부호 규약 상충). D-VEQ 보완이 이 상류 비정합은 **해결 못 함**(eq:gxi 의 +Ω 계승). 박스(eq:Veq)는 v7-11·정합, *다리*만 비정합 — REVIEW1 M1 수준 잔존(신규 아님).

---

## 4. ★D-PEAK 정정 정확성 (master 직접 검산 — 핵심)

**검산 방법**: 코드 L466-481 의 tail 분기 (ξ_eq−ξ_lag)/L_V 를 격자 고정·L_V 변화로 실측(_causal_lowpass 1:1 복제, lfilter zi=ρ·src[0]).

**실측 결과(dpeak_test.py, dgrid=5.0e-5, true_bell_max=9.731):**
| L_V/Δgrid | ρ=e^{−Δgrid/L_V} | tail_peak / true_bell |
|-----------|------------------|----------------------|
| 1000 | 0.999 | 0.715 |
| 40–100 | 0.975–0.99 | **0.986** (최대 근접) |
| 2.0 (스위치 경계) | 0.607 | 0.771 |
| 0.5 | 0.135 | 0.313 |
| **0.1 (L_V≪Δgrid)** | **0.000** | **0.0005** (peak→0!) |

**판정**:
- ★**N8 본문(886-901) framing 은 부정확 — master 가설 정확히 적중.** v8-03b 가 적은 ① "L_V→0 이라 peak→0 아니다" ② "L_V≪Δgrid 에서 매끄럽게 종으로 이어진다" ③ "eq:branch 는 수치불안정(분모≈0) 방지"는 **셋 다 검증과 반대**. 실측: L_V→0(ρ→0)에서 ξ_lag→ξ_eq(같은칸)→분자→0 → **peak→0**(ratio 0.0005). 분모 발산이 아니라 *분자 붕괴*가 본질. 평형 종 회복은 **L_V≫Δgrid(ρ→1)** 에서 일어남(반대 극한). 한칸이동근사 ξ_lag≈ξ_eq−L_V dξ/dV 는 1−ρ≈Δgrid/L_V 인 ρ→1=**L_V≫Δgrid** 전개(dpeak_test2: 검증). v8-03b 가 이를 "L_V<νΔgrid" 자리에 붙인 것은 regime **반전**.
- eq:branch 스위치의 실제 역할 = 작은 L_V 에서 *붕괴하는 이산 꼬리*를 해석적 평형 종 ξ_eq(1−ξ_eq)/w 로 **대체(substitute)**. 경계(L_V=2Δgrid)서 꼬리=평형의 77%로 *불연속*(매끈 X) — "연속 환원"이 아니라 "치환 가드"가 정확.
- ✓ **반면 verifybox R3(1078-1081)는 옳다**: "스위치가 평형 분기 선택→peak가 ξ_eq(1−ξ_eq)/w 로", "(정정) L_V→0 이 peak→0 아니다 — 스위치가 평형 종으로 *대체*". R3 의 "대체" 표현 = master 가 요구한 정확 framing.
- ∴ v8-03b 의 D-PEAK 정정은 **반쪽**: R3 는 고쳤으나 정작 N8 본문에 *새로운 틀린 설명*(regime 반전 + "분기 없이 연속")을 심어 같은 문건 내 자기모순(N3) + KNOWN_DEFECTS ★최우선 D-PEAK 가 형태만 바뀐 채 **잔존**. C1 의 핵심(작은 L_V 곡선 0 붕괴 → G-follow 파괴)은 미해결.

**수정 방향(권고, master 통합용)**: N8 본문 886-901 을 R3 와 일치시킴 — ① "(ξ_eq−ξ_lag)/L_V → dξ_eq/dV 종 환원은 **L_V≫Δgrid**(ρ→1) 에서" ② "L_V≲Δgrid 면 이산 꼬리가 0 으로 붕괴하므로 eq:branch 가 해석적 평형 종으로 **대체**(연속 환원 아님)" ③ "수치불안정" 표현 삭제→"이산 붕괴 가드". 박스 eq:branch/eq:eqpeak·R3 는 불변.

---

## 5. 차원 점수 (합 / 35)

| 차원 | v8-03(REVIEW1) | v8-03b | 비고 |
|------|----------------|--------|------|
| G-derive(유도 완결성) | 2.5 | **3.0** | D-VEQ 해결·D-DHEFF 극한 추가 +; D-WEFF 새 인자오기(N1) − |
| 배치 보존(v7-11) | 5 | 5 | 절순서·박스·식별자·표 불변 |
| 부호 8항(v11 1:1) | 5 | 5 | S1–S8 전건 PASS·박스 결함 0 |
| **D-PEAK 처리** | 1 | **2** | R3 정정 옳음(+1) vs N8 본문 regime 반전·자기모순(N2/N3) 신규 |
| G-follow | 3 | **2.5** | 본문 거짓 framing 이 작은-L_V 재현 *역방향* 오도(전보다 더 틀린 설명) |
| G-usable/완결성 | 4 | **4.5** | orphan 0 해결·keybox·nodemap 완결 |
| 그림 | 3.5 | **4** | orphan 2 해소·ASCII·dangling 0; spine 유래표기 1 누락 잔존(L1) |
| **합계** | **24** | **26 / 35** | +2(D-VEQ·orphan·부분 D-DHEFF) − D-PEAK 본문 역행 상쇄 |

빌드: xelatex 2-pass, LaTeX `!` error 0, 19p PDF, dangling ref 0(검증). 폰트 shape 경고 3건 = 무해.

---

## 6. master 삼각검증 노트
- D-PEAK: master 수치 재현(dpeak_test ×2) = REVIEW1 C1 와 삼각 일치(L_V≪Δgrid서 ratio 0.0005). v8-03b NOTEb(12-14·44행)의 자기서술 "수치 불안정 방지/매끄러운 연속 환원" = 실측과 반대 → 정정 자체가 부정확 확정.
- D-WEFF N1: master weff_bridge.py 독립 검산 — 박스 정확·다리 인자 4배 오기 확정. REVIEW1 H3(박스 정확) 계승 + 새 다리오기 추가.
- 모범 4사슬(spinodal·artanh·detailed balance·L_q 4항) 재검산 전건 일치(selftest_num: u=0.766·86.69 mV·artanh 항등 2.0215·U298=0.0853).
