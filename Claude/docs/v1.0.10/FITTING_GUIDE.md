# Anode_Fit v1.0.10 — 피팅 추천 가이드 (모델 ↔ 데이터)

> `Anode_Fit_v1.0.10.py`(흑연 음극 + LCO 양극 MSMR + 가역 발열)를 실측 dQ/dV·엔트로피 계수에 피팅하는 워크플로. 파라미터 tier·round-trip 절차·초기값/경계·수렴 판정. 이론 근거 = Ch1(dQ/dV·LCO)·Ch2(발열). ★흑연 회귀 0-diff 는 피팅 전 과정 불변(LCO 편입이 흑연 경로 무섭동).

## 1. 파라미터 tier 표

| tier | parameter | scope | 초기값 | 하한 | 상한 | 제약 | 필요 데이터 | release |
|---|---|---|---|---|---|---|---|---|
| 1 (peak 골격) | U_j **또는** (ΔH_rxn, ΔS_rxn) | 전극 공통 | 표 초기값 | — | — | U_j 순서보존 | 저율 등온 dQ/dV | 확정 |
| 1 | n_j (폭 = nRT/F) | 공통 | 1.0 | >0 | ~4 | n>0 | 봉우리 폭 | 확정 |
| 1 | Q_j | 공통 | 표 | >0 | — | ΣQ_j = Q_total(정규화) | 용량 | 확정 |
| 1 | Cbg | 공통 | 0 | — | — | — | baseline | 확정 |
| 2 (히스·비대칭) | Ω | 공통 | 표 | >2RT(≈4958@298K) | — | Ω>2RT(spinodal) | 충·방전 pair | 피팅 |
| 2 | γ | 공통 | 0 | 0 | 1 | γ∈[0,1] | 충·방전 gap | 피팅 |
| 2 | χ | 공통 | 0.5 | 0 | 1 | χ∈[0,1] | 방향 비대칭 | 피팅 |
| 2 | Rn | 공통 | 0 | ≥0 | — | — | 분극 이동 | 피팅 |
| 3 (동역학 꼬리) | dH_a | 공통 | 표 | >0 | — | — | rate-series | 피팅 |
| 3 | dVdq_qa | 공통 | 0.30 | >0 | — | ★누락=silent 꼬리 off | rate-series | 피팅 |
| 4 (다온도) | dS_rxn, dS_a | 공통 | 표 | — | — | 부호 문헌일치 | 다온도 | 피팅 |
| — | g_max_eV, x_MIT, dx_MIT | **LCO 전자항** | 13/0.50/0.05(tier-C) | x_MIT 물리 anchor≈0.85 | | ΔS_e 골≈−46 J/mol·K | 엔트로피 계수 | ★피팅 정정 |

가드: 코드 `_finite_pos`/`_finite_nonneg` 가 T·I·Q_cell·dict 값의 유한·부호를 fail-fast. bound(n>0·χ∈[0,1]·dVdq_qa>0·dx_MIT>0)는 fitting wrapper 스키마에서 별도 강제.

## 2. Round-trip 절차 (5-Phase, 과식별 회피 = tier 단계 개방)
- **Phase A — peak 골격**(저율 등온): tier-1(U_j 또는 ΔH/ΔS·n·Q·Cbg)만 개방. `equilibrium()` 또는 저율 `dqdv()`로 봉우리 위치·폭·면적 맞춤. 게이트: ΣQ_j∈[0.95,1.05]Q_total·U_j 순서.
- **Phase B — 히스·비대칭**(충·방전 pair): tier-2(Ω·γ·χ·Rn) 개방, tier-1 고정. 충전/방전 곡선 gap·분극 이동.
- **Phase C — 동역학 꼬리**(rate-series): tier-3(dH_a·dVdq_qa) 개방. **L_V 직접 fit 과 물리 dH_a/dVdq_qa/χ fit 동시개방 금지**(과식별) — 물리 경로 우선, L_V 직접은 초벌 우회만.
- **Phase D — 다온도·LCO 전자항**: tier-4(dS_rxn·dS_a) + LCO 전자항(g_max·x_MIT·dx) 개방. `entropy_coefficient()`·`reversible_heat()`를 다온도 엔트로피 계수에 맞춤. ★**전자항 dict 를 T1=MIT(최고 x·최저 V) 로 재정렬**(Ch1 tab:lco-staging, 현 시연은 중간 dict). ★다온도 시 `func_dSe_molar` 의 T 인자 전달로 Sommerfeld T-스케일 복원(현 T_ref 동결 근사 해제)·eq:U1T2 center-T_ref 별도적분(½=a_e/2F) 구현.
- **Phase E — 검증**(holdout): 미사용 T·C-rate 에서 예측 vs 실측. **흑연 0-diff 회귀 assert**(LCO 편입 후에도 흑연 불변).

## 3. 수렴·물리제약 판정
- 잔차 ΣΔ²/N < 1e-4 (정규화 dQ/dV).
- ΣQ_j ∈ [0.95, 1.05]·Q_total (면적보존).
- U_j 순서 보존 · 다온도 ΔS 부호 문헌 일치.
- **흑연 회귀 0-diff**: `test_regression_graphite.py verify` = 13/13 np.array_equal PASS (피팅·LCO 편입이 흑연 경로 불변).

## 4. 그래프 suite (검증·복원)
기존: `plot_dqdv.py`(흑연 4패널)·`demo_lco_heat.py`(흑연/LCO dQdV+q_rev) = PASS. 신규 validation suite `graph_suite_p5.py`:
- **V1** 흑연+LCO dQ/dV 나란히 — MSMR 동형, 두 전극 한 프레임.
- **V2** round-trip 복원 parity(입력 ΔS → forward U_j(T) → 회귀 ΔŜ, y=x) — ★FD round-trip 수치 무결 가드(ΔS↔∂U/∂T 정의 정합; 잡음 데이터 통계적 식별성 증명 아님).
- **V3** q_rev(V) 흡·발열 교대(ΔS 부호전환 음영) — eq:qrev 부호규약.
- **V4** ∂U/∂T 완전식 vs 단순식 vs FD — 파생 A 수치검증(config 항·완전식≈FD).
- **V5** 온도의존 peak 이동(258–318K) — U_j(T)=ΔS/F 이동.
- **V6** 전자항 골 ΔS_e(x) (x_MIT=0.50 vs 0.85 오버레이) — eq:dSegate·x_MIT 불일치 실증.
- **V7** 다온도 T² 곡률(선형 기준선 + eq:U1T2 예상곡률) — ★현 동결근사=선형, 다온도 피팅 구현 후 유효(오도 방지 주의).
- **V9** 면적보존 회귀(∫dQdV dV vs Q_j) — eq:eqpeak 면적=Q.
