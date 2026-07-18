# Phase P3 — 코드 적용 (ratio 보정·전달함수 옵션) Result

## Summary

부록 E(자기일관 해법)의 수식을 코드에 실제 적용했다. `Anode_Fit_v1.0.23.py` 에 (1) **1차 ratio 보정** 경로 `_causal_memory_ratio`(동결 0차 궤적 위 상태의존 국소 지연 길이 `L_V(V)=L_V⁰·exp[g_eff(1−ξ_lag0)]`, `g_eff=2χ_d·Ω/RT` via `_lag_ratio_geff`), (2) **전달함수** `transfer_apparent_from_equilibrium`(H(ω)=1/(1+iωL_V) 저역통과·FFT)을 추가하고, 생성자 플래그 `lag_ratio_correction`(기본 **False**)으로 dqdv 경로에 분기했다. **동결 경로 bit-exact 보존을 기존 게이트(G1: v1.0.19 golden·G3: 보정제거 변형)로 증명**(max|d|=0.0). 신규 게이트 모듈 `test_gates_v1023_selfconsistent.py`(G-E1~E5) 5/5 PASS 로 ratio 보정의 동결극한 회수·차수 이득·전달함수·liveness 검증. 부록 E.6 코드 지도를 실 함수명으로 갱신(수식↔코드 정합 확정).

## Step Range

Cumulative **Step 16 – Step 20** (P2 = 9–15 완료 승계).
- Step 16: `func_L_q`/lag 경로에 ratio 보정 옵션(`_causal_memory_ratio`·`_lag_ratio_geff`·`lag_ratio_correction` 플래그·기본 off)
- Step 17: `_causal_memory` 전달함수 경로(`transfer_apparent_from_equilibrium`, FFT)
- Step 18: 신 옵션 게이트 신설 + 동결 bit-exact 게이트(기존 게이트 재실행 exit0)
- Step 19: 코드↔부록 E.6 수식 정합(지도 실 함수명 갱신)
- Step 20: 본 Result + ledger + CHANGE_LOG

## Inputs

- `Anode_Fit_v1.0.23.py` — `func_L_q`(L97–104)·`_causal_memory_pointwise`(L107–135)·`_resolve_lag_length`(L404–448)·`_chi_and_dH_eff`(L394–401)·`__init__`(L254–294)·dqdv 호출부(L544–587) 전수 검독.
- `_sections/ch1_appE_selfconsistent.tex` — E.1~E.6 수식(구현 사양).
- `results/PHASE_P1_RESULT.md`·`comp_v23/COND_AUDIT.md` — 검증된 수식(κ·ε·H·동결회수).
- `test_gates_v1023.py` — 기존 게이트(bit-exact 증빙 도구).

## Files Created

- `test_gates_v1023_selfconsistent.py` — 자기일관 옵션 게이트 5종(G-E1 동결회수·G-E2 dqdv bit-exact·G-E3 차수이득 Picard·G-E4 전달함수·G-E5 liveness).

## Files Updated

- `Anode_Fit_v1.0.23.py`:
  - 신규 모듈 함수 `_causal_memory_ratio`(1차 ratio 보정) + `transfer_apparent_from_equilibrium`(전달함수 FFT).
  - `__init__` 키워드 `lag_ratio_correction: bool = False`(끝자리·positional 무영향) + `self.lag_ratio_correction`.
  - 신규 메서드 `_lag_ratio_geff`(g_eff=2χ_d·Ω/RT·use_dH_eff 게이트).
  - dqdv `elif self.lag_ratio_correction:` 분기(else=기존 동결 경로 무변경).
  - 헤더 주석 (E)(F) 항 추가(옵션 문서화).
- `_sections/ch1_appE_selfconsistent.tex` — E.6 표 3행을 실 함수명으로 갱신(`_causal_memory_ratio`·`_lag_ratio_geff`·`lag_ratio_correction`·`transfer_apparent_from_equilibrium`).

## Read Coverage

- `Anode_Fit_v1.0.23.py` — **부분 검독**: lag/dqdv/init/chi 관련 전 영역(L38–135·254–294·394–448·544–587) 전수. 그 외(LCO·블렌드 클래스 본체)는 P3 스코프 밖(미검독) — 단 __init__ 키워드 추가가 서브클래스에 미치는 영향은 게이트로 확인(G1/R6 exit0).
- `ch1_appE_selfconsistent.tex` — **전문**(직전 P2 저작분).

## Execution Evidence

**(1) 기존 게이트 — 동결 bit-exact 증명** (`test_gates_v1023.py`):
```
>>> SUMMARY: G1 PASS (module max|d|=0.0e+00, golden max|d|=4.3e-15, bit-exact=True) | G2 PASS | G3 PASS | n(T) PASS
>>> R6 BLEND (§3.5): R6-G1 PASS | R6-G2 PASS | R6-G3 PASS | coverage PASS   (exit=0)
```
→ `lag_ratio_correction=False`(기본) 에서 v1.0.19 골든·보정제거 변형과 **max|d|=0.0 bit-exact**. 서브클래스(LCO·블렌드) 무영향.

**(2) 신규 자기일관 게이트** (`test_gates_v1023_selfconsistent.py`):
```
G-E1 동결회수(g_eff=0): max|x1-x0|=0.00e+00 (<1e-14), max|Lloc-L0|=0.0e+00  PASS
G-E2 dqdv bit-exact(g_eff=0): Ω부재 array_equal=True, use_dH_eff=False array_equal=True  PASS
G-E3 차수이득(코드 Picard·참=고정점):
   Ω/RT=0.0 ε=0.000e+00 err0=0.000e+00 err1=0.000e+00
   Ω/RT=1.0 ε=7.500e-02 err0=6.398e-02 err1=7.505e-03 err1/err0=0.117
   Ω/RT=2.0 ε=1.500e-01 err0=2.005e-01 err1=7.330e-02 err1/err0=0.366   PASS
G-E4 전달함수 H=1/(1+iωL_V) vs 동결합성곱: rel RMS=3.96e-06 (<5e-3)  PASS
G-E5 liveness(Ω>0·use_dH_eff): max|on-off|=9.400e-01 (>1e-6) finite=True  PASS
>>> SELF-CONSISTENT GATES: ALL PASS  (5/5)   (exit=0)
```

**(3) 문건 재빌드**(E.6 갱신 후): ch1 3-pass err0/undef0/**87p**(불변).

## Validation

| Gate (계획서 P3) | 판정 | 근거 |
|---|---|---|
| 기존 게이트 exit0 유지 | **PASS** | [확인] test_gates_v1023.py exit0·G1 max|d|=0.0. |
| 동결 off = 기존 bit-exact | **PASS** | [확인] G1(golden 4.3e-15·module 0.0)·G-E2(array_equal True 두 경로). |
| 신옵션 수렴 | **PASS** | [확인] G-E3 참=코드 자기일관 고정점(Picard)·err1<err0 전부·g=0 정확회수·수축률≈ε. |
| 전달함수 정합 | **PASS** | [확인] G-E4 rel RMS 3.96e-6(<5e-3). |
| 옵션 liveness(무작동 아님) | **PASS** | [확인] G-E5 max|on-off|=0.94(Ω>0 해상 regime). |
| 수식↔코드 1:1(E.6) | **PASS** | [확인] E.6 표 실 함수명 갱신·재빌드 GREEN. κ↔`_causal_memory_ratio`·g_eff↔`_lag_ratio_geff`·H↔`transfer_apparent_from_equilibrium`. |

**정직 명시**: G-E5 는 실이득 regime(L_V override 0.006=L_V/w 0.3)에서만 옵션이 작동함을 보인다. 기본 흑연 파라미터(c_rate~1)는 L_V~7.5e-7 로 미해상 가드→평형종 직행(COND_AUDIT §7 휴면)이라 ratio 무효과 — 이는 결함이 아니라 부록 E.4 warnbox 의 실이득창(0.1≲L_V/w≲0.6) 밖임을 코드가 그대로 반영한 것.

## Gate

**PASS.** ratio 보정·전달함수 옵션 구현·게이트·수식↔코드 정합 완료. 동결 경로 bit-exact 불변. P4(선택) 또는 P5(마감) 진입 가능.

## Confirmed Non-Changes

- **동결 0차 경로(`_causal_memory_pointwise`·else 분기) 무변경** — 기존 dqdv 산출 bit-exact.
- **기존 게이트 스크립트 무수정** — `test_gates_v1023.py` 그대로(신 게이트는 별 파일).
- **LCO·블렌드 클래스 본체 무수정** — __init__ 키워드는 상속되나 기본 off 라 무영향(R6 exit0 확인).
- **문건 본문 무개입** — 부록 E.6(부록 예외)만 갱신, 본문 무변경.
- **v1.0.22 무접근**.
- **사용자 식별자·기호 보존** — 신규 함수만 추가, 기존 이름 변경 0.

## Open Issues / Decision Queue

- **[결정 대기·D3]** P4(Tier2 Fisher 정보기하) 실행 여부 — 기본값 P3 후 별도 GO. 미승인 시 P5(마감) 직행.
- **[P5 대상]** 신 코드·부록 E 독립 적대적 검수(수식↔코드·게이트 견고성·프로젝트 검수 7항)는 P5 4창.
- **[근거 미발견·잔존]** Ref.6·7 제목·DOI 미확보(P2 이월).

## Next

**분기점.** D3 승인 시 **P4 (Step 21–24)**, 미승인/기본 시 **P5 마감 (Step 25–28)**. 다음 cumulative step = **21**(P4) 또는 **25**(P5). 기본값(D3=P3 후 별도 GO) → P5 마감 준비 대기 또는 사용자 지시.

<!-- 자산(P3_RESULT): [P3-01 _causal_memory_ratio 1차 보정·L_loc 상태의존] [P3-02 _lag_ratio_geff g_eff=2χdΩ/RT·use_dH_eff 게이트] [P3-03 transfer_apparent_from_equilibrium H=1/(1+iωL_V) FFT] [P3-04 lag_ratio_correction 플래그 기본off·bit-exact] [P3-05 기존게이트 G1 max|d|=0 bit-exact 증명] [P3-06 신게이트 5/5 PASS] [P3-07 E.6 수식↔코드 실함수명 정합] [P3-08 G-E5 실이득regime만 작동·휴면은 부록warnbox 반영] -->
