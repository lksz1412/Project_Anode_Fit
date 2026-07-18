# Phase V0 — 착수·검증설계·코드 T/I/V 확인 Result

## Summary
v1.0.24 반쪽셀 곡선 생성기 완성도 검증의 설계를 확정하고, 코드의 T/I/V 의존 구현 범위를 실측 확인했다. 검증 매트릭스(4온도×GITT/3율)와 브로드닝 3출처 분리 매핑을 정식화. 코드는 ①(L_V, I·T)·②(w=nRT/F, T)를 예측하나 ③(σ_η 앙상블 산포)은 별도 예측 없이 w_j에 흡수(문건 규정 정합).

## Step Range
Cumulative **1–4** (신 캠페인 v1.0.24 착수).

## Inputs
- `plans/2026-07-18-v1024-completeness-validation-plan.md`(검증 설계).
- `docs/v1.0.23/Anode_Fit_v1.0.23.py`: `func_L_q`(L105–112)·`func_w`(L91–94)·`_n_factor`(L360–381).
- `docs/v1.0.23/_sections/ch1_sec07_broadening.tex`(브로드닝 3출처·폭예산·스코프).

## Files Created
- `results/V1024_EXECUTION_LEDGER.md`·`results/PHASE_V0_RESULT.md`·`results/comp_v24/`(폴더).

## Files Updated
- (없음 — 설계·확인 phase)

## Read Coverage
- `func_L_q`·`func_w`·`_n_factor` 전문. `ch1_sec07_broadening.tex` 전문(직전 세션).

## Execution Evidence
코드 T/I/V 의존 grep·정독 결과:
- **I(전류)**: `func_L_q` `T_attempt=|I|/Q_cell·h/kB` → `L_V∝|I|` (① 꼬리 전류의존 구현).
- **T(온도)**: `func_w=nRT/F`(② T선형) + `func_L_q` Arrhenius `dG_a/RT·−x·A/RT`(① 활성화 T의존) + `_n_factor` `n(T)=n+n_T1(T−T_ref)`(폭 잔여 T의존, 기본 n_T1=0).
- **σ_η(③ 앙상블 산포)**: grep 무 → **코드 미예측**. 문건대로 `w_j`가 ②⊗③ 흡수 → ③은 피팅 초과폭으로만 들어감.

## Validation
| 게이트(V0) | 판정 | 근거 |
|---|---|---|
| 검증 매트릭스 확정 | PASS | 4온도(15/23/35/45)×{GITT,0.05,0.1,0.2C} |
| 조건↔출처 매핑 | PASS | GITT=②③·(율−GITT)=①∝\|I\|·4온도=T의존(계획서 GT) |
| 코드 T/I/V 범위 확정 | PASS | ①②·n(T) 구현·③ σ_η 미예측(w_j 흡수) 확인 |

## Gate
**PASS.** 검증 설계·코드 범위 확정. V1(공개데이터) 진입.

## Confirmed Non-Changes
- 코드·문건 무수정(설계·확인만). v1.0.23 불가침.

## Open Issues / Decision Queue
- **[V2 시험 대상]** 폭 T-스케일 예측 = ② nRT/F. 실측 초과분이 ③ σ_η. σ_η의 T-의존은 코드가 n_T1 fudge 외 예측 못함 — V2서 실측 대조.
- **[V1 진행중]** 공개데이터 확보(리서치 2창).

## Next
V1 — 공개데이터 조사(흑연/LCO 반쪽셀). 다음 cumulative step = **5**.
