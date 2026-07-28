# Phase 059 v1.0.18.2 Einstein full-path 감사

정본일: 2026-07-28

판정: `CONDITIONAL_P059_V1018_2_EINSTEIN_ABSENT_KEY_AND_ACTIVE_FULLPATH_CONFORMANCE_PASS_BUT_PARAMETER_CONTRACT_AND_PERSISTENT_REGRESSION_FAIL`

## 결론

theta_E가 없을 때 v1.0.18.1과 equilibrium, 등온/비등온 dQdV,
entropy coefficient, reversible heat가 모두 exact 동일했다.
theta_E=700 K 활성 branch도 중심 전위, 중심의 finite-difference
기울기, entropy coefficient와 -I*T*dU/dT 열 항등식이 같은
자유에너지 경로로 닫혔다.

그러나 public parameter contract는 닫히지 않았다. dH_rxn/dS_rxn이
없는 U-only transition에 theta_E를 넣으면 private helper는 nonzero
보정을 계산하지만 equilibrium과 entropy public path는 이를 조용히
무시한다. theta_E_Tref도 finite만 검사하고 양수 조건을 강제하지
않아 0 또는 음수에서 깨끗한 fail-fast가 없다.

배포 test_regression_graphite.py, sample_test, graph_suite에는 theta_E와
_vib 호출이 각각 0건이다. handover의 round-trip은 현재 배포
regression harness에서 재현·보존되는 test authority가 아니다.

따라서 구현 capability의 내부 정합은 보존하지만, 실제 사용 전에는
U-only 조합 reject 또는 명시 의미 부여, Tref>0 guard, absent/active
scalar-array/derivative/heat 회귀시험이 필요하다. 이 결과도 material
fit validation은 아니다.

## 다음 단계

Step 38.5에서 ROADMAP_future_physics의 항목을 implemented,
theory-only, new-scope와 data prerequisite로 전건 분류한다.

원본 `Claude/`, `main`은 수정하지 않았다.
