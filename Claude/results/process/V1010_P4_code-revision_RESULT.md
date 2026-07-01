# P4 RESULT — 코드 개정: LCO 양극 + 발열 구현 (9종 경쟁-체리픽 · Serena)

> 마스터 §P4 · 계획 `../../plans/2026-07-03-v1010-P4-code-revision-plan.md`. 대상 `docs/v1.0.10/Anode_Fit_v1.0.10.py`. **순서 코드→문건→코드: 이론(Ch1·Ch2) 확정 후 그 이론 1:1 코드화.**

## 1. 범위·산출
흑연 음극 전용 코드를 **BDD 양·음극 dQ/dV 물리수식 피팅 함수**로 확장 — LCO 양극(MSMR 동형) + 가역 발열 q_rev + 전자 엔트로피(MIT). ★흑연 회귀 0-diff 절대 준수. 단일 .py = 공유 가변상태라 9종 = 설계 제안 드래프트, master만 Serena로 실편입.

## 2. 정독 커버리지 (master 직접, head→tail)
- 코드: func_U_j(L77-78, 선형 T)·equilibrium(L349-366)·dqdv(L369-479)·__init__(L220-258)·curve(L483-508)·GRAPHITE_STAGING_LIT(L531-560)·__main__. func_U_j 호출 = equilibrium L358·dqdv L436 확정.
- 이론: Ch1(sec:lco·eq:dSegate·eq:msmr·eq:gunit·eq:U1T2·L304-307 부호) · Ch2(eq:qrev·파생B 이중계산·eq:weighted·warnbox).
- 9 설계 드래프트 + 검토1 + P1 앵커.

## 3. 방법 = 9종 경쟁-체리픽 (Serena)
9 설계 드래프트(3S·3O·3C, 무통신) → 검토1(별세션, School A/B 판정) → 체리픽 설계 vN-10(master) → master Serena 실편입 + adversarial(별세션) + finalizer. 커밋 5회.

## 4. 드래프트 (커밋① 8525ed9)
9/9 완성(Codex stall 0). ★설계 3-3 분기: School A(zero-touch·0 replace)=O1·S2·S3 / School B(dqdv 항등 seam)=O2·O3·S1. 물리 만장일치(MSMR f↔−σ_d·q_rev T 한 번·이중계산 직교·÷e_V·면적 assert·byte 하네스·死코드 보존).

## 5. 검토1 (커밋② 826b6b0) — `V1010_P4_review1.md`
**School B(항등 seam) 승**: School A 독립클래스는 dqdv 오케스트레이션 루프(L431-477) 복제 불가피(DRY 붕괴)·O1 합성은 전자항 주입 논리실패. **★가장 약한 1곳(9종 전원 놓침): seam이 dqdv 단독이면 equilibrium·q_rev에서 LCO T1 전자항 누락 → 3경로 공유 헬퍼로 해소.** 물리 오류 3 적발: S1 T² 자동누적(½ 손실)·S3/C2/C3 LCO s=−1(Ch1 L304-307 위반)·O3 x↔ξ 역방향.

## 6. 체리픽 설계 vN-10 (커밋③ a9bd489) — `V1010_P4_design_v10.md`
골격: O2 seam+O3 하네스·O3 func_dSe_molar·O1 dUoc_dT·C3 T² 처리·S1 x=1−ξ·C1 tobytes+면적assert. 3경로 공유 seam·전자항 게이트 자체검산(−45.7 = Ch1 −46).

## 7. Serena 실편입 (커밋④ 88ba428 → 마감본)
| 심볼 | 방식 | 내용 |
|---|---|---|
| EV_TO_J·func_dSe_molar | insert_after func_chi_d | 전자엔트로피 게이트(−(π²/3)R(kB T/e_V)(g_max/dx)σ(1−σ), ÷e_V·부호<0·몰당 R kB) |
| _effective_dS_rxn(base) | insert_after curve | seam 항등(`return tr['dS_rxn']`) — 3경로 공유 |
| entropy_coefficient | insert_after curve | Ch2 가중식 ∂U/∂T = Σ w_j(ΔS_eff/F + config), dqdv 무가산/q_rev 가산 비대칭 |
| reversible_heat | insert_after curve | q_rev=−I·T·∂U/∂T [W] (T 한 번) |
| irreversible_heat | insert_after curve | lumped I(U_oc−V)(Ch2 유일 boxed), 3분해 옵션 라벨 |
| LCO_MSMR_LIT·LCOCathodeDQDV | insert_after 클래스 | tier-C 시연·상속(σ_d 뒤집기 없음), override=_effective_dS_rxn만 |
| equilibrium·dqdv seam | Edit 2줄 | func_U_j 인자 → self._effective_dS_rxn (byte 0-diff) |

死코드 func_U_j_hys·통계열역학 본체 불가침. 식별자·정수코드·시그니처 보존.

## 8. Adversarial (별세션, refute) — 1-6 정상·7 해소·3 수정
- **항목 1-6 정상 확정**(코드+식+실행 삼각검증): 흑연 0-diff(seam base `is tr['dS_rxn']` True·maxdiff 0.0)·seam 3경로 일관·func_dSe_molar 물리(−45.68 손수 재현)·q_rev T 한 번(`q−(−I·T·dUdT)`=0.0)·이중계산 직교(dict 미오염)·σ_d 불변(base `is` True).
- **★항목 7(가장 약한 1곳) = factor-2**: dSe(T)∝T를 func_U_j의 T·ΔS에 넣어 평형peak U_j(T)와 entropy_coefficient가 factor-2 불일치(eq:U1T2 a_e/2F vs a_e/F). 단일온도 정합·설계 defer됐으나 다온도서 조용히 틀림. → **master 마감서 해소: LCO override의 dSe를 T_ref=298.15 동결 상수 오프셋으로 변경** → dS_eff T-무관·U_j(T) 선형·세 경로 factor-2 없이 일관. Sommerfeld T-스케일·½ 인자는 다온도 피팅 과제로 inline 라벨.
- **항목 3 수정**: demo/test 스크립트 cp949 크래시 → `sys.stdout.reconfigure(utf-8)` 콘솔-safe.
- 허위적발 0 확인.

## 9. 검증
- **흑연 0-diff**: 13/13 배열 np.array_equal bit 완전일치 PASS(LCO override 동결 변경 후에도 유지)·면적 ratio 0.936308 동일. py_compile OK·__main__ 무오류.
- **LCO dQ/dV**: finite·피크 3.92·4.04(3.880↔3.930 근접 블렌드, Ch1 "연속 블렌드" 정합).
- **전자엔트로피**: func_dSe_molar(x_MIT)=−45.68(Ch1 −46), 창밖 −0.451≈0. seam 전자전이 dS_eff=−49.68=−4+(−45.68) 3경로 일치.
- **q_rev**: 흑연 range[−0.216,0.105]W·LCO[−0.099,0.258]W(전자전이 발열 서명), T 한 번. 그래프 3종(figs/P4_lco_heat_validation.png).

## 10. Gate (P4 종료) — PASS
흑연 회귀 0-diff ✓ · LCO 양극 dQ/dV 정상 개형 ✓ · 발열 q_rev 이론 1:1(T 한 번·부호·이중계산 직교) ✓ · 면적보존 DC=1 ✓ · 식별자/정수코드/死코드 보존 ✓ · import/실행 무오류 ✓ · 그래프 suite ✓ · CRIT/HIGH 0(항목7 마감 해소·3 수정) ✓.

## 11. P5 이월 (최종 점검)
- **x_MIT=0.50 tier-C placeholder**: Ch1 eq:ggate anchor x_MIT≈0.85·플래토 x≈0.75-0.94와 불일치(내부 정합이나 문서). round-trip 피팅 단계서 물리값 정정·문서 정합.
- **다온도 T² 곡률**: 전자전이 U_j(T)의 Sommerfeld T-스케일·eq:U1T2 center-T_ref 별도적분(½=a_e/2F) 미구현(단일-기준 동결 근사). 다온도 round-trip 피팅서 구현.
- **LCO 시연 파라미터**: tier-C 기본값 → 실측/round-trip 피팅으로 신뢰값화.
- **비가역 3분해**: lumped만 구현, I²R+Iη_ct+Iη_diff 개별 분해는 율의존 피팅 과제(Ch2 boxed 부재).
- 그래프·문건 상호충실도·완성도 9종 최종 점검(P5).
