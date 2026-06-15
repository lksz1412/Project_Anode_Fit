# PHASE PYFUNC RESULT — Anode_Fit Python 함수화 + 풀셀 분해 피팅

**계획**: `Claude/plans/2026-06-16-anode-fit-python-functionalization-plan.md`
**산출물 위치**: `Claude/results/anode_fit_python/`
**일자**: 2026-06-16
**대상 셀**: LCO 기반 핸드폰용 파우치 셀 (흑연 음극 / LCO 양극) — 사용자 명시

## 1. 지시 (요지)

Anode_Fit 문건의 식을 **추적 가능한 Python 함수**로 함수화. 함수마다 ① 문건 몇번식(또는 몇번식
조합) ② 적용 가정·근사 ③ x축 V/Q 를 상세 주석. 11-section 계획서부터 최종 Python 함수까지.

## 2. 산출물

| 파일 | 내용 |
|---|---|
| `anode_fit_lib.py` (25KB) | 추적 모듈. Primitive(7)+모델(3)+V↔Q(2)+풀셀(3)+피팅(3) 함수, 전 함수 4항 docstring(출처식·조합·가정·V/Q축) |
| `test_anode_fit_lib.py` | T2~T4 수치검산. **ALL PASS** |
| `roundtrip_fullcell.py` | T5 LCO/흑연 풀셀 분해 round-trip. **PASS** |
| `TRACE_TABLE.md` | 함수↔식번호↔조합↔가정↔V/Q축 추적표 + 식별성 발견 6항 |

## 3. 식 번호 매핑 (aux 권위 추출)

핵심 fitting 식: (1.27) ξ_eq · (1.50) bell · (1.54)+(1.64)+(1.68)→(1.69) lnL_q · (1.63) tail ·
(1.79) simplefit(종+꼬리) · (1.82) total(다전이 합) · (1.88) dU_hys · (1.91) 분기중심 ·
(1.94) master · (1.96) hysmaster · (1.42)/(1.47) 전하보존·관측식(V↔Q 적분).

## 4. 검증 결과 (4-tier: 확정)

- **T2 함수 수치검산**: bell 정점=Q/4w (1.51) ✓ · dU_hys(25℃,4RT)=54.76mV≈54.8 (1.88) ✓ ·
  종+꼬리 면적=Q (1.80) ✓.
- **T3 V↔Q 일관**: d/dV ∫dQdV ≈ dQdV (rel<2e-4) ✓ · invert∘QV≈id (<0.05mV) ✓.
- **T4 풀셀 환원**: 평탄 대극 극한서 단일전극 회복 ✓.
- **T5 풀셀 분해 round-trip(LCO/흑연)**: 음극 3 peak ±8mV·면적 ±0.013, 양극 3 peak ±8mV·
  면적 ±0.013, off_ct ±0.013, **재구성 V_FC RMSE 0.64mV (≪ 잡음 3mV)**. PASS.

## 5. 식별성 발견 (실증된 가정·한계 — TRACE_TABLE §6)

1. **loading–Q_j 공선형** (§1.11) → load=1 고정.
2. **dV/dQ rugged landscape**(sharp LCO peak) → coarse-to-fine(평활 V → dV/dQ).
3. **절대 offset ~1% softness** (§1.12 비유일성) — 정직 보고.
4. **비순환 staging 필수** = 사용자 "RMSE3/4/더 많은 단계" 의 grounded 근거.

## 6. Read Coverage

- 정독: 정본 §1.7~§1.12·§1.15·§1.17(eqpeak/lag/potbranch/tempbranch/synth/overlap/master/code) +
  aux 식매핑 전수 + BDD `BatteryData_Matching`(99_Backend.py 858–1185) + 기존 §1.17 코드·round-trip.
- 미정독(범위 밖): §1.13·§1.14 히스테리시스 본문 상세(함수는 (1.88)/(1.91)만 사용, 충분).

## 7. 미완·다음

- [선택] BDD 슬롯-인(신규 클래스, 백엔드 무변경) — 별도 GO.
- [선택] §1.17 본문(.tex)에 풀셀 매칭 코드 예시 절 추가 — 별도 결정(정본 본문 수정 = 사용자 승인).
- 꼬리(r_a, L_V) 자유 피팅 경로의 풀셀 round-trip — 현 round-trip 은 준평형(r_a=0). 확장 가능.

## 8. 상태

함수화 + 추적 + round-trip 실증 **완료**. 정본 .tex 본문 **무수정**(보존). BDD 백엔드 **무수정**(보존).
