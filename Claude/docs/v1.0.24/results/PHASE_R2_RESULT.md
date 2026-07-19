# Phase R2 — 코드 반영 (@3·@5·LCO토글·#1) Result

## Summary
`Anode_Fit_v1.0.24.py` 에 시드표(R0) 사양대로 4개 반영을 additive·bit-exact 폴백으로 구현: @3 정칙용액(Frumkin) 커널·@5 XRD 5-feature staging·LCO 전자항 on/off 토글·#1 C-rate/Eyring 단위계약. 기존 게이트 bit-exact 전부 PASS + 신규 반영 게이트 4/4 PASS + 곡선 물리 타당성(매끈·단일봉·토글) 시각 확인.

## Step Range
cumulative R-step 5–9.

## Inputs
- `Anode_Fit_v1.0.24.py`(R0 복제분), `REFLECT_SEED_TABLE.md`(사양).
- 검증 근거: `comp_v24/{regsol_si,ablation,lco_ablation,T_SPLIT_FINDING,regsol2,LCO_DIAGNOSIS,CODEX_REVIEW_VERIFICATION}`.

## Files Created / Updated
- 수정 `Anode_Fit_v1.0.24.py`:
  - `func_L_q`(L105): #1 단위계약 주석(값 무변경·bit-exact).
  - 신규 `_regsol_binodal_xa`·`_regsol_dqdv`·`_REGSOL_XG`(func_ksi_eq 뒤): @3 Frumkin 커널(self-contained numpy, scipy 무).
  - `equilibrium()` 루프: `kernel=='regsol'` 분기(로지스틱 기본=bit-exact).
  - 신규 상수 `GRAPHITE_STAGING_XRD_v1024`(5-feature, GRAPHITE_STAGING_LIT 뒤): @5.
  - `LCOCathodeDQDV.__init__`(신규)+`_effective_dS_rxn`(플래그): 전자항 토글.
- 신규 `test_gates_v1024_reflect.py`(반영 게이트 4종)·`results/v1024_reflect_curves.py`·`results/reflect_curves.png`.

## Read Coverage
- `Anode_Fit_v1.0.24.py`: func_w/func_U_j/func_ksi_eq/func_L_q(L91-135) 전독·equilibrium(L536-560) 전독·_effective_dS_rxn base(L716-725)·LCO class(L985-1030) 전독·GRAPHITE_STAGING_LIT/LCO_MSMR_LIT 전독·구성자 시그니처(test_gates L83-114) 확인.

## Execution Evidence
- import OK: `_regsol_dqdv`·`GRAPHITE_STAGING_XRD_v1024`·LCO `include_electronic_entropy` 존재.
- **기존 게이트 bit-exact 보존**: `test_gates_v1024.py` → G1 PASS(module max|d|=**0.0e+00**·golden 4.3e-15·bit-exact=True)·G2·G3·n(T)·R6 BLEND(G1/G2/G3/coverage) 전 PASS. selfconsistent 5/5 ALL PASS.
- **신규 반영 게이트** `test_gates_v1024_reflect.py` → **ALL PASS (4/4)**:
  - G-R1 @5: 전이 5·유한·비음·stage-2L 분리기울기 **0.301 mV/℃**(Dahn 0.30 정합)·sep 25℃16→45℃22mV.
  - G-R2 토글: 기본=ON max|Δ|=0.0(bit-exact)·OFF@298 U(T_ref)보존 max|Δ|=0.0·OFF@318 ∂U/∂T차 max|Δ|=0.66(>0).
  - G-R3 @3: 유한·비음·면적=1.001·prominent 봉=**1**(단일 broad·매끈).
  - G-R4 #1: func_L_q 정상·값 무변경.
- 곡선 물리 타당성 `reflect_curves.png`: @5 매끈 T-의존·@3 단일 broad 매끈·LCO 토글 298 ON=OFF 동일·318 분기.

## Validation
- PASS_R2_CODE: (1)기존 bit-exact 3종(G1·4전이폴백·selfconsistent) 유지 [확정] (2)@3/@5/토글/#1 신규 게이트 4/4 [확정] (3)곡선 연속·매끈·단일봉·미분가능 [확정] (4)신규 의존성 0(numpy만) [확정].

## Gate
**PASS_R2_CODE = PASS.**

## Confirmed Non-Changes
- 기본 경로(로지스틱 MSMR·4전이 GRAPHITE_STAGING_LIT·LCO 전자항 ON) 전부 v1.0.23 bit-exact. `func_L_q` 수치 무변경(주석만). dqdv() 유한율속 경로에 @3 커널 미개입(equilibrium 한정 — 유한율속 regsol 은 추가 후보). 블렌드 f_Si=0 흑연 회수 bit-exact 유지.

## Open Issues / Decision Queue
- 유한율속 `dqdv()` 에 regsol 커널 확장 = 추가 후보(현재 equilibrium 한정). 근거 미발견 아님·의도적 스코프.
- R1 문건 저작(9창) 병행 진행 중 — 완료 시 체리픽·통합·PHASE_R1_RESULT.

## Next
R1 문건 통합(9창 체리픽) → R3 검증·통합검수 → R4 마감. 다음 cumulative step 10.
