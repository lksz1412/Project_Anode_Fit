# Phase P1 — 조건검수 게이트 (lag ratio 보정식 재유도·타당성 부등식) Result

## Summary

사용자 논문(JCP 147 144111)의 Fredholm-2종 ratio 닫힘 기법을 문건 자기일관 구조에 접목 가능한지 **집행(부록 E 저작) 전 정식 검증**했다. 판정: 문건 자기일관 3종 중 **동역학 lag(II)에만** 성립. lag 의 참 문제는 `L_V=L_V(ξ)` 비선형 자기일관(제2종 **Volterra**, 인과·Markov)이고, 문건이 이미 쓰는 **동결 0차**(선형 합성곱)가 논문의 "가해 기준문제(δ-싱크)"에 대응한다. 논문 Eq.34 철학(미지량→비→가해기준 치환)을 Volterra 위에 이식해 **1차 ratio 닫힌형** 도출·검증 완료. 마스터 독립 재유도(수치)로 COND_AUDIT 예비분석의 모든 정량 주장을 재현. **셀링포인트 부분 강등**: lag 참 문제가 값싼 O(N) 전진 ODE라 "계산 절감/수치 루프 대체"는 성립 안 함 → "분석적 1차 닫힘 + 타당성 증명서 + 사용자 방법 자기 인용/시연"으로 재프레이밍.

## Step Range

Cumulative **Step 4 – Step 8** (P0 = 1–3 완료 승계).
- Step 4: II lag Volterra→ratio 형식 재유도 (1차 보정식 도출)
- Step 5: 타당성 부등식 `ε≡2χ_d(Ω/RT)Δξ_supp≪1` 도출 + 논문 (i)(ii)(iii) 1:1 대응
- Step 6: 동결극한 회수 증명 (L_V=const → 0차 정확 회수)
- Step 7: Ref.6·7 원문 확보 여부 판단 + 서지 검증
- Step 8: COND_AUDIT.md 정식화 + 마스터 검산 게이트 + 본 Result + ledger

## Inputs

- `docs/v1.0.23/_sections/ch1_sec08_lag.tex` (L1–145, 전문) — eq:Lqmid/eq:Lq/eq:kuniv/eq:Acut/eq:chid/eq:dHeff/eq:Lqfull/eq:LV.
- `docs/v1.0.23/Anode_Fit_v1.0.23.py` — `func_L_q`(L97–104)·`_causal_memory_pointwise`(L107–135)·`_resolve_lag_length`(L404–448)·상단 docstring(L38–74) 동결 근거.
- `jcp_extract.txt` — 방법 구조(L296–297 Fredholm-2·ratio Eqs.37·38)·서지(L711–714 Ref.6·7).
- `docs/v1.0.23/results/comp_v23/COND_AUDIT.md` (L1–302, 전문) — P1 예비 분석(sub-agent 산출).
- `Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md` — P1 gate 정의.

## Files Created

- `docs/v1.0.23/results/PHASE_P1_RESULT.md` (본 문건) — P1 phase-loop 결과 기록(11항 양식).
- `scratchpad/p1_ratio_check.py` — 마스터 독립 재유도 수치 검산(동결회수·차수·ε 예측). 예비 COND_AUDIT 의 `cond_audit_verify.py` 와 **독립 구현**으로 교차 확인.
- (선행·sub-agent) `docs/v1.0.23/results/comp_v23/COND_AUDIT.md` — 조건검수 정본(10절·P3-5 5항·게이트 판정). 본 P1 에서 마스터 검산으로 **정식 승인**.

## Files Updated

- `docs/v1.0.23/results/V1023_EXECUTION_LEDGER.md` — P1 row 추가(Step 4–8·CONDITIONAL PASS·Next=9).
- (본문·코드 무수정 — Confirmed Non-Changes 참조)

## Read Coverage

- `ch1_sec08_lag.tex` — **전문 검독**(L1–145, 본 세션 재독).
- `Anode_Fit_v1.0.23.py` — **부분 검독**: lag 관련 함수 3종 + 상단 docstring(L38–74·97–135·404–448). 그 외 클래스(전하보존·블렌드)는 P1 스코프 밖(미검독).
- `jcp_extract.txt` — **부분 검독**: 방법 구조·서지 grep 확인(L45·296–297·600·711–714). 전문 정독은 직전 세션 완료(요약 승계).
- `COND_AUDIT.md` — **전문 검독**(L1–302).
- 논문 원문(JCP147 PDF 본문 page/para) — **미접근**(추출 텍스트만). Ref.6·7 원문 — **미소장**.

## Execution Evidence

**(1) 마스터 독립 재유도 수치 검산** `scratchpad/p1_ratio_check.py` (상태의존 모델 `L_V(ξ)=L_V0·exp[2χ_d(Ω/RT)(1−ξ)]`, ξ=1 동결서 ρ=1; 참해=비선형 후진Euler+국소Picard·0차=동결선형·1차=기준궤적 위 변계수선형):

```
  Ω/RT          ε        err_0        err_1  err1/err0     err0/ε
  0.00 0.0000e+00   0.0000e+00   0.0000e+00     0.0000 0.0000e+00
  0.25 3.1250e-02   1.8475e-02   5.6061e-04     0.0303 5.9120e-01
  0.50 6.2500e-02   4.0686e-02   2.7750e-03     0.0682 6.5098e-01
  1.00 1.2500e-01   9.9361e-02   1.6794e-02     0.1690 7.9489e-01
  2.00 2.5000e-01   2.9023e-01   1.3527e-01     0.4661 1.1609e+00

[차수 스케일링: ε 반감(L0 반감) 시]
         ε        err_0        err_1      e0비      e1비
2.5000e-01   1.6030e-01   3.8358e-02    0.000    0.000
1.2500e-01   9.9361e-02   1.6794e-02    1.613    2.284
6.2500e-02   5.3975e-02   5.4501e-03    1.841    3.081
3.1250e-02   2.7349e-02   1.4702e-03    1.974    3.707
```

- **동결회수**: Ω/RT=0 → err_0=err_1=0.0 (machine-exact).
- **차수**: ε 반감 시 err_0비→2(**1차 O(ε)**), err_1비→4(**2차 O(ε²)**) — 보정항 1차 획득.
- **ε 예측**: err_0/ε≈0.6–0.8(O(1) 상수), ε=0.25(≪1 아님)서 err1/err0=0.47 → 제어 붕괴(warnbox).

**(2) COND_AUDIT 예비 검산** `cond_audit_verify.py`(독립 스크립트)와 정량 일치: 동결회수 ‖r₁−r₀‖=1.06×10⁻⁸(이산화 바닥)·err0~g^1.32/err1~g^2.59·Picard 수축률=ε(0.073→0.101, 0.276→0.432, 0.840→0.883)·전달함수 H=1/(1+iωL_V) FFT rel err 5.47×10⁻⁹·fig:reversal(+1.01w,0.196) 재현. → **두 독립 구현이 동일 결론**.

**(3) 서지 grounding** (`jcp_extract.txt` L711–714, 원문 참조목록 직접 인용):
```
6S. Lee, C. Y. Son, J. Sung, and S. Chong, J. Chem. Phys. 134, 121102 (2011)
7C. Y. Son, J. Kim, J.-H. Kim, J. S. Kim, and S. Lee, J. Chem. Phys. 138, 164123 (2013)
```
L296–297: "Fredholm integral equation of the second kind … ratio W̄_u(r₁)/W̄_u(r) is given by Eqs. (37) and (38)". → 서지·방법 **날조 아님**(원문 직접 확인).

## Validation

| Gate (계획서 P1) | 판정 | 근거 (4-tier) |
|---|---|---|
| **(a)** 1차 ratio 보정식이 동결극한서 0차 정확 회수 | **PASS** | [확인] 수치 err_0=err_1=0.0(Ω=0)·COND_AUDIT 1.06×10⁻⁸. 해석: δκ≡0→R≡1→r₁=r₀. |
| **(b)** 타당성 부등식 ↔ 논문 (i)(ii)(iii) 1:1 대응 | **PASS** | [확인] COND_AUDIT §4.2 매핑표(i↔소섭동 δκ·ii↔L_0 지배·iii↔단거리 핵 L_V/w). ε=Picard 수축률 수치 확증. |
| **(c)** 마스터 재유도 검산 (P3-5 의무 5항) | **PASS** | [확인] 독립 재구현이 차수 이득·수축률·동결회수 재현. P3-5 5항 = COND_AUDIT §9(①서지[확인] ②논문내위치[원문-간접·page/para 미확정] ③수학구조 ④변수매핑 ⑤물리가정차). |
| **중단 조건** (재유도 검산 불통과) | **미발동** | 검산 통과 → 본체 유지(교육예시 강등 불필요). |

**4-tier 주의**: ②(논문 내 사용 위치)의 page·paragraph 는 **원문-간접**(추출 텍스트 기반, PDF 본문 위치 직접 미확정) — [근거 미발견]으로 표기, D4(JCP147 자족 기술)로 진행.

## Gate

**CONDITIONAL PASS.** 재유도·게이트 (a)(b)(c) 전부 PASS. 부록 E 저작(P2) 진입 허가 — **단 조건부**:
1. 셀링포인트 재프레이밍 준수(§7.2): "계산 절감/수치 루프 대체" 문구 **금지**, "분석적 1차 닫힘 + 타당성 증명서 + 사용자 방법 시연"으로만.
2. 적용 불가(I·III 대수근) 부록 E 서두 명시(§8 문안).
3. ②(논문 내 위치) page/para 는 원문 확보 시 확정(미확보 시 [원문-간접] 명기).

## Confirmed Non-Changes

- **`.tex` 본문·`.py` 코드 무수정** — P1 은 검수·유도·검산 phase(분석만). 저작은 P2, 코드는 P3.
- **v1.0.22 무접근** — 완결 문건(read-only 기준선).
- **본문 챕터 무개입** — 부록 E 는 P2, 본문 포인터도 P2. P1 은 문건 파일 변경 0.
- **기존 게이트 스크립트 무변경** — `test_gates_v1023.py` 손대지 않음(P3 에서 신옵션 게이트 추가 예정).

## Open Issues / Decision Queue

- **[근거 미발견]** Ref.6·7 원문 미소장 → P3-5 ②의 page/para 직접 확정 불가. **D4 기본값**(JCP147 자족 기술)으로 진행. 사용자 원문 제공 시 확정.
- **[결정 반영됨]** 셀링포인트 부분 강등(계산 절감 철회) — 사용자 승인 불요(정직 정정), 부록 E 문안에 반영.
- **[다음 phase 전 확인]** P2 부록 E 를 ch1_graphite 부록군에 편입 시 xr 교차참조·페이지 예산 회귀 없음 확인(P2 재빌드 게이트).

## Next

**P2 — 부록 E 저작 (Step 9–15) 진입 허가.** 다음 cumulative step = **9**.
진입 조건: 위 Gate 3개 조건부 항목을 P2 저작에 반영. P2 Step 9 = 부록 E 골격(E.1 lag Volterra 자기일관+동결0차 / E.2 Fredholm ratio 닫힘+P3-5 5항+warnbox / E.3 Laplace 전달함수 / E.4 코드 대응 지도).

<!-- 자산(P1_RESULT): [P1-01 lag=비선형Volterra(Markov)·논문Fredholm-2와 종다름·II만 정합] [P1-02 동결0차=δ싱크 가해기준] [P1-03 1차ratio 닫힌형·게이트a 동결회수 machine-exact] [P1-04 ε=2χd(Ω/RT)Δξsupp=Picard수축률·(i)(ii)(iii)1:1] [P1-05 마스터 독립재유도=COND_AUDIT 재현(err0 O(ε)/err1 O(ε²))] [P1-06 서지 원문직접 grounding·날조0] [P1-07 강등:계산절감 철회→분석닫힘+증명서] [P1-08 CONDITIONAL PASS→P2 Step9] -->
