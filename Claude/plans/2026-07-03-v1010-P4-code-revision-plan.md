# P4 세부 스텝 계획 — 코드 개정: LCO 양극 + 발열 구현 (9종 경쟁-체리픽 · Serena)

> 마스터 §P4. result = `results/process/V1010_P4_code-revision_RESULT.md`. 대상 = `docs/v1.0.10/Anode_Fit_v1.0.10.py`(614줄, 흑연 음극 전용). 앵커 = P1 result(플로우차트·조건 audit·파라미터 인벤토리)·Ch1(LCO MSMR·직접엔트로피 eq:Sedirect·sec:lco)·Ch2(발열 q_rev·이중계산 직교·전자엔트로피). **Serena 필수**(replace_symbol_body·insert_after_symbol). **순서 코드→문건→코드: 이론(Ch1·Ch2) 확정 완료 → 이제 그 이론 1:1 코드화.**

## P4 목표 (사용자 의도)
코드를 **BDD 양·음극 dQ/dV 물리수식 기반 피팅 함수**로 확장 — 흑연 음극(기존) + **LCO 양극**(MSMR 동형) + **가역 발열** q_rev. 흑연 회귀 0-diff 절대.

## 현 코드 구조 (Serena 실측)
- 모듈함수 14: func_w·func_U_j·func_U_j_hys(死)·func_ksi_eq·func_L_q·_causal_lowpass(DC=1)·func_dU_hys·func_U_branch·func_dH_a_eff·func_chi_d + _finite류.
- 클래스 `GraphiteAnodeDischargeDQDV`(11메서드): __init__·_build_seed_L_V·_n_factor('n'>'w'>1)·_width·_chi_d·_chi_and_dH_eff·_resolve_lag_length·equilibrium·dqdv·curve·_direction_to_sigma.
- 상수 R·F·GRAPHITE_STAGING_LIT·V·U298·I.

## P4 산출물 (확장 코드 + 회귀)
1. **LCO 양극 dQ/dV**: MSMR 동형(X_j↔Q_j, U_j⁰↔U_j^d, ω_j↔w_j, f↔−σ_d, Ch1 sec:lco) — 신규 클래스 `LCOCathodeDQDV`(또는 일반화 base) — 양극 부호·MIT g(E_F) 급변 electronic 항.
2. **가역 발열 q_rev**: `q_rev=−IT·∂U/∂T=−(IT/F)ΔS(x)`(Ch2 eq:qrev) — 신규 메서드/함수. dS_e(전자엔트로피, LCO는 x-의존) + 비가역 3분해(I²R+Iη_ct+Iη_diff) 옵션. **이중계산 직교**(중심 ΔS⁰_j에 config 재가산 금지).
3. **흑연 회귀 0-diff**: 기존 GraphiteAnodeDischargeDQDV 출력 byte 불변(확장이 흑연 경로 무섭동) — 회귀 하네스.
4. **면적 보존**: _causal_lowpass DC gain=1 유지·확장 경로도 면적 보존.
5. 품질 = 마스터 §2 + 코드 소유권(식별자·정수코드 보존)·범위(지정 외 임의수정 X).

## 9종 경쟁-체리픽 (단일 .py = 공유 가변상태 → 9종 = **설계 제안 드래프트**, master만 Serena로 실편입)
- **Step 1 — 9 설계 드래프트**(3S·3O·3C, 독립): 현 코드 + P1 result + Ch1(sec:lco·eq:Sedirect) + Ch2(eq:qrev·직교) 정독 → **구현 설계 제안**(클래스 구조·함수 시그니처·삽입 위치·흑연 회귀 가드·발열 수식 매핑·LCO MSMR 매핑) → `V1010_P4_draft_<id>.md`. **드래프트만, .py 수정 절대 X**. **커밋①**.
- **Step 2 — 검토1(별세션)** + 보완: 9 설계 교차검증(물리 1:1·흑연 회귀 안전·이중계산 직교·부호·면적보존·소유권). refute+가장약한1곳. **커밋②**.
- **Step 3 — master 체리픽**(설계 vN-10): 통합 설계(Serena 편입 레시피·심볼별 replace/insert). **커밋③**.
- **Step 4 — master Serena 실편입** + adversarial(별세션) + finalizer: master가 **.py 실제 확장(Serena)** → 흑연 회귀 0-diff 검증 + 그래프 생성 → `V1010_P4_code-revision_RESULT.md`. **커밋④**.

## Gate (P4 종료)
- 흑연 회귀 0-diff(기존 커브 byte 일치) · LCO 양극 dQ/dV 정상 개형 · 발열 q_rev 이론 1:1(T 한 번·부호·이중계산 직교) · 면적보존 DC=1 · 식별자/정수코드 보존 · import/실행 무오류 · 그래프 suite 생성.

## 주의
- **Serena 필수**(심볼 도구, 텍스트 치환 X)·검수=작업과 다른 세션·commit master 전용·추정 금지(코드·Ch1·Ch2 줄 근거).
- 코드 소유권: 사용자 식별자·대소문자·정수/문자열 코드 절대 보존. 지정 범위 외 임의수정 X(대체 필요 시 묻고 GO).
- 死코드 func_U_j_hys 처리는 P1 판정 따름(제거 아닌 보존, 사용자 GO 전까지).
- 이중계산 직교: 중심 표준값 ΔS⁰_j(config=0) ⊥ config 분포항 R ln[ξ/(1−ξ)] — 구현 시 분리.
