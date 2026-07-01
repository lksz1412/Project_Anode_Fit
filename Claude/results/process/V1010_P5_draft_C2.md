# Anode_Fit v1.0.10 P5 감사 드래프트 C2

> 조: B조(code↔Ch2 상호충실도)  
> 범위: 감사 의견만. 코드/문건 수정 없음.  
> 판정 기준: Ch2 발열 식 ↔ `Anode_Fit_v1.0.10.py` 양방향 매핑, T 한 번, 이중계산 직교, 부호, 차원, 하프셀 스코프, P4 이월 라벨.

## 1. Read Coverage

- base 프롬프트: `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/p5_audit_base.txt` 19줄 전문 정독. `__ID__=C2`, `__GROUP__=B조(code↔Ch2 상호충실도)` 적용.
- 프로젝트 지침: `D:/Projects/Project_Anode_Fit/Codex/AGENTS.md` 전문 확인.
- 코드: `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py` head→tail 정독. 핵심 발열 구현: `func_dSe_molar` L170-185, `_effective_dS_rxn` L533-542/L655-671, `entropy_coefficient` L544-576, `reversible_heat` L578-586, `irreversible_heat` L588-596, `LCO_MSMR_LIT` L621-638.
- Ch1: `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` head→tail 정독. B조 관련 참조: LCO 전자항 `eq:dSegate` L1081-1087, `eq:gunit` L1026-1029, `eq:U1T2` L1054-1056, LCO 분해/코드 예고 L1685-1760.
- Ch2: `Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex` head→tail 정독. 핵심 식: 하프셀 warnbox L102-107, 파생 B 이중계산 L293-309/L524-536, `eq:weighted` L470-474, 히스 분기 평균 L570-592, `eq:qrev` L642-646, 종합식 L668-684, 한계/갭 L687-697.
- 앵커 결과: `V1010_P1_code-audit_RESULT.md`, `V1010_P2_ch1_RESULT.md`, `V1010_P3_ch2_RESULT.md`, `V1010_P4_code-revision_RESULT.md` 전문 확인. P4 이월 L53-57 확인.

## 2. Executive Finding

대부분의 Ch2 발열 핵심식은 코드에 직접 대응한다. 특히 `q_rev=-I*T*dU/dT`는 코드에서 T를 한 번만 곱하고, `entropy_coefficient`는 Ch2 완전식의 `dS_eff/F + (R/F)log(xi/(1-xi))` 구조를 그대로 구현한다. 또한 dQ/dV 경로에는 config 항을 더하지 않고 q_rev 경로에만 더해 파생 B의 이중계산 금지를 지킨다.

확정 갭은 2건이다.

1. Ch2 히스테리시스 가역열 분기 평균식 `eq:hys_rev`가 코드 발열 인터페이스에 구현되어 있지 않다. `entropy_coefficient`/`reversible_heat`는 방향 또는 분기 중심을 받지 않고 unbranched equilibrium weights만 사용한다.
2. Ch1/Ch2가 LCO MIT 전자 엔트로피를 조성 의존 게이트로 설명하지만, 코드의 LCO q_rev 경로는 `x_center`와 `T_ref=298.15`에서 동결한 상수 오프셋만 더한다. P4에서 의도적으로 라벨링한 단일-기준 근사이나, Ch2의 “ΔS(x)” 완전 발열 곡선과는 아직 불완전 대응이다.

## 3. Ch2 → Code Mapping

| Ch2 항목 | Ch2 근거 | 코드 근거 | 판정 |
|---|---:|---:|---|
| 하프셀 스코프 | Ch2 L102-107 | 전극 클래스별 메서드, 전셀 합성 함수 없음 | 확정 PASS |
| `eq:weighted` 중심 가중 | Ch2 L470-474 | `entropy_coefficient` L544-576, `Qg=Q*g`, `num/den` | 확정 PASS |
| 완전식 config 항 | Ch2 L480-482, L668-684 | `config=(R/F)log(xi/(1-xi))` L571, `dS_eff/F+config` L573 | 확정 PASS |
| 파생 B 이중계산 금지 | Ch2 L293-309, L524-536 | dQ/dV는 `func_U_j(...dS_eff...)`만, config 무가산 L456; q_rev 경로만 config 가산 L571-573 | 확정 PASS |
| `eq:qrev` | Ch2 L642-646 | `return -float(I) * T * entropy_coefficient(...)` L585-586 | 확정 PASS |
| T 한 번 | Ch2 L642-646, P3 L20/L47 | `dUdT`가 이미 V/K, `reversible_heat`에서 `T` 1회 곱 L580-586 | 확정 PASS |
| 부호 규약 | Ch2 L651-653, L658-664 | docstring L580-584 및 식 L586 | 확정 PASS |
| 비가역 lumped | Ch2 L642-649 | `irreversible_heat = I*(U_oc-V)` L588-596 | 확정 PASS, 인터페이스 리스크 있음 |
| 비가역 3분해 | P4 이월 L57, Ch2 boxed 부재 | 코드 docstring L592-594가 “lumped만” 라벨 | 확정 PASS |
| 히스 분기 평균 | Ch2 L570-592 | `entropy_coefficient`가 `sigma_d`, `gamma`, branch center를 받지 않음 L544-576 | 확정 GAP-1 |
| LCO MIT ΔS_e(x,T) 게이트 | Ch1 L1081-1087, Ch2 L406-408/L631-632 | `func_dSe_molar`는 x 인자 지원 L170-185이나 LCO override는 `x_center`, `T_ref` 고정 L659-670 | 확정 GAP-2 / P4 이월 라벨 |

## 4. Code → Ch2 Mapping

| 코드 메서드 | 코드 위치 | Ch2/Ch1 근거 | 판정 |
|---|---:|---|---|
| `_effective_dS_rxn` base | L533-542 | Ch2 중심 표준값 `ΔS^0_j` 입력, 파생 B 중심값 정의 L294-306 | 확정 PASS |
| `entropy_coefficient` | L544-576 | Ch2 `eq:weighted` + 완전식 L470-482, L668-684 | 확정 PASS |
| `reversible_heat` | L578-586 | Ch2 `eq:qrev` L642-646 | 확정 PASS |
| `irreversible_heat` | L588-596 | Ch2 `I(U_oc-V)` L642-649 | 확정 PASS |
| `LCOCathodeDQDV._effective_dS_rxn` | L655-671 | Ch1 `eq:dSegate`, `eq:gunit`, P4 factor-2 해소 라벨 | 부분 PASS: 단일-기준 근사로 라벨됨 |
| `func_dSe_molar` | L170-185 | Ch1 `eq:dSegate`, `eq:gunit` | 확정 PASS: 중심값 검산 `-45.678 J/(mol K)` |

코드에 “Ch2 근거가 없는 새 발열 메서드”는 발견하지 못했다. `irreversible_heat`의 3분해 부재도 코드가 새 기능을 주장하는 것이 아니라, Ch2 boxed 식 부재를 근거로 lumped만 둔다고 명시한다.

## 5. Confirmed Gaps

### GAP-1 — Ch2 히스테리시스 가역열 분기 평균식 미구현

- 위치: Ch2 `eq:hys_branch`/`eq:hys_rev` L570-592, 코드 `entropy_coefficient` L544-576, `reversible_heat` L578-586.
- 무엇이 맞지 않나: Ch2는 히스테리시스가 있을 때 분기별 `g_j^{(d)}`로 `∂U_oc^{(d)}/∂T`를 계산하고, 가역 발열에는 `1/2(ch+dis)` 평균을 넣는다고 한다. 코드의 `entropy_coefficient`는 방향 인자, 분기 중심 `U_j^d`, `gamma`, `Omega`를 받지 않으며, unbranched `U_j`에서 `xi`와 `g`를 계산한다.
- 영향: `gamma=0` 또는 단일 고립 전이에서는 사실상 차이가 사라질 수 있다. 그러나 여러 전이가 겹치고 히스 분기 이동이 있으면 Ch2의 branch-weight 평균과 코드 unbranched weight가 달라진다. 독립 수치 확인에서 2전이 합성 예시의 최대 차이는 `6.45e-06 V/K`였다.
- 맞는 형태: master 정정은 둘 중 하나다. (A) 코드에 `entropy_coefficient(..., hys_mode='none|branch_avg', direction=...)` 같은 분기 평균 경로를 추가한다. (B) 문건/코드 docstring에 현재 발열 구현은 “히스 branch 평균 미적용, unbranched equilibrium heat coefficient”라고 범위를 낮춘다.
- 분류: 확정.

### GAP-2 — LCO MIT 전자 엔트로피의 조성 의존 게이트가 q_rev 경로에서 상수 오프셋으로 축약됨

- 위치: Ch1 `eq:dSegate` L1081-1087, `eq:U1T2` L1054-1056, LCO 코드 예고 L1724-1729, 코드 `func_dSe_molar` L170-185, `LCOCathodeDQDV._effective_dS_rxn` L655-671, P4 RESULT L40/L54-L55.
- 무엇이 맞지 않나: 문건은 LCO MIT 전자항을 `ΔS_e(x,T)` 게이트로 둔다. 코드의 순수 함수는 x 인자를 받지만, 실제 LCO 클래스는 `tr['x_center']`와 `T_ref=298.15`에서 한 번 평가한 값을 `dS_rxn`에 상수 오프셋으로 더한다. 따라서 q_rev 곡선에서 MIT 전자항의 전압/SOC 의존 골은 구현되지 않는다.
- 영향: P4에서 factor-2 문제를 피하려고 단일-기준 동결 근사를 선택한 것은 확인된다. 그러나 Ch2의 `ΔS(x)` 완전 발열 관점에서는 LCO 전자항의 위치별 q_rev signature가 단순화된다. `x_MIT=0.50` tier-C placeholder와 Ch1 anchor `x_MIT≈0.85` 불일치도 같은 이월 묶음이다.
- 맞는 형태: master 정정은 (A) 현재 코드를 “단일온도/단일중심 LCO heat demo”로 명확히 라벨하거나, (B) round-trip 단계에서 `x↔xi_eq,1(V)` 매핑과 `eq:U1T2`의 `1/2` 적분계수를 포함한 다온도 구현으로 승격해야 한다.
- 분류: 확정. 단, P4에서 이월 라벨은 이미 존재하므로 신규 미라벨 결함은 아니다.

## 6. Risks / Non-Gap Notes

### RISK-1 — `irreversible_heat`의 `q_irr≥0`은 입력 부호 관례에 의존

- 위치: 코드 L588-596, Ch2 L642-649.
- 코드 식 자체는 Ch2 lumped 식 `I(U_oc-V)`와 일치한다. 다만 메서드는 `I>0 방전`, `U_oc>=V` 같은 Ch2 부호 조건을 검사하지 않는다. 잘못된 방향 부호나 전압 순서를 넣으면 docstring의 `≥0`이 보장되지 않는다.
- 분류: 리스크. 공식 gap으로 세지 않음.

### RISK-2 — `entropy_coefficient`의 독립변수는 SOC x가 아니라 전압 격자 `V_n`

- 위치: Ch2 종합식 L681-683은 주어진 SOC x에서 `U_oc(x,T)`를 풀어 `xi_j`를 되먹이는 절차를 설명한다. 코드 L544-576은 이미 주어진 전압 격자에서 `xi_j(V,T)`를 평가한다.
- 해석: dQ/dV 곡선 위의 전압축 발열 profile을 계산하는 사용법이면 정합한다. SOC 입력 API를 기대하면 별도 implicit solver가 없다.
- 분류: 리스크/인터페이스 범위. 공식 gap으로 세지 않음.

## 7. T 한 번 / 차원 / 부호 재검산

- `entropy_coefficient` 반환 단위: `dS_eff/F`는 `[J mol^-1 K^-1]/[C mol^-1]=V/K`, `config=(R/F)ln(...)`도 `V/K`, 가중 평균도 `V/K`.
- `reversible_heat`: `-I*T*dUdT` = `A*K*V/K = A*V = W`. 코드 L586에서 T는 한 번만 곱한다. 독립 실행 확인: `reversible_heat - (-I*T*entropy_coefficient)` 최대차 `0.0`.
- `q_rev` 부호: Ch2 L658-664와 코드 L580-584가 동일하다. 방전 `I>0`에서 `ΔS>0`이면 `q_rev<0` 흡열, `ΔS<0`이면 `q_rev>0` 발열.
- config 이중계산: dQ/dV 경로는 `dS_eff`로 중심 온도 이동만 반영하고, config 항은 `entropy_coefficient`에서만 명시 가산한다. Ch2 파생 B L293-309/L524-536과 정합한다.
- LCO 전자항 단위: `func_dSe_molar`는 `R*(kB*T/EV_TO_J)*(g_max/dx)`를 사용해 Ch1 `g_J=g_eV/e_V` 나눗셈형과 정합한다. 독립 실행 확인: `func_dSe_molar(0.5,298.15,13,0.5,0.05)=-45.678... J/(mol K)`.

## 8. P4 이월 항목 확인

| 이월 항목 | 근거 | B조 판정 |
|---|---|---|
| `x_MIT=0.50` tier-C placeholder | 코드 L632, P4 RESULT L54, Ch1 L1069-1071 | 확정 이월. GAP-2와 연결. |
| 다온도 T² 곡률 | Ch1 L1049-1058, 코드 L659-664, P4 RESULT L55 | 확정 이월. 코드가 `T_ref` 동결로 라벨. |
| LCO 시연 파라미터 | 코드 L619-L620, P4 RESULT L56 | 확정 이월. 신뢰값 아님 라벨 있음. |
| 비가역 3분해 | 코드 L592-L594, P4 RESULT L57 | 확정 이월. Ch2 boxed 부재 때문에 lumped만 구현. |

## 9. 3대 무결 최종 확인

- 물리 배경 정확: Ch2의 q_rev, weighted entropy coefficient, config 이중계산 분리, 하프셀 범위, lumped irreversible heat는 코드에 대체로 충실히 반영됐다. 히스테리시스 branch-average와 LCO MIT x-dependent heat signature는 완성 구현이 아니라 이월/범위 제한이다.
- 코드 정확: T² 오곱은 없음. `q_rev`는 T 한 번이고 차원은 W로 닫힌다. `dSe_molar`의 eV→J 나눗셈형도 맞다. `irreversible_heat`는 식은 맞지만 positivity는 호출 관례 의존이다.
- 사용자 의도 반영: P4 목적이 “흑연 0-diff + LCO/발열 확장”이었다는 점은 충족한다. P5 최종점검 관점에서는 위 2개 갭을 master 정정 큐에 올려야 빈 통과가 아니다.

## 10. Master 정정 목록

1. `entropy_coefficient`/`reversible_heat`의 범위 정정: Ch2 `eq:hys_rev`를 구현하지 않는 현재 상태를 명시하거나, branch-average 옵션을 구현한다.
2. LCO 전자 엔트로피 heat path 정정: 현재 `x_center`, `T_ref` 동결 근사를 명시 유지할지, Ch1의 `x↔xi_eq,1(V)` 매핑과 `eq:U1T2` 다온도 적분으로 승격할지 결정한다.
3. `irreversible_heat` doc/interface 정정 후보: `I>0 방전 및 U_oc>=V` 관례를 명시해 `q_irr≥0` 문구가 무조건 보장처럼 읽히지 않게 한다.

## 11. Final Classification

- 확정 PASS: q_rev 식, T 한 번, weighted 완전식, config 이중계산 직교, 하프셀 scope, lumped irreversible heat, 비가역 3분해 이월 라벨.
- 확정 GAP: 2건.
- 리스크: 2건.
- 근거 미발견: 코드 안에서 Ch2에 없는 별도 발열 기능을 주장하는 항목은 발견하지 못함.
- 미검증: 실제 실측 데이터 round-trip, full-cell 합성, 다온도 LCO T² 구현 성능.
