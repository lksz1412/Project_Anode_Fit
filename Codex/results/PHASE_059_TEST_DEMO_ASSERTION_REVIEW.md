# Phase 059 test/demo assertion review

12 test blobs와 18 demo blobs 전부의 assertion, comparison, exit,
golden read/write, figure output, import path와 feature token을 AST로
검사했다. 이 단계는 정적 test-evidence 감사이며 runtime 결과가 아니다.

## 구조

- files: 30 (test 12, demo 18)
- lines: 3372
- Python `assert`: 0
- version/path 문자열을 정규화하면 5 logic families × 각 6 releases다.

| Family | Files | Assert | Exit calls | array_equal | Golden writes | Figure writes |
|---|---:|---:|---:|---:|---:|---:|
| demo_lco_heat | 6 | 0 | 0 | 0 | 0 | 6 |
| graph_suite | 6 | 0 | 0 | 0 | 0 | 6 |
| plot_dqdv | 6 | 0 | 0 | 0 | 0 | 6 |
| regression | 6 | 0 | 12 | 6 | 6 | 0 |
| sample_test | 6 | 0 | 0 | 0 | 0 | 6 |

## 판정

| ID | Evidence class | Disposition | Finding | Source anchors |
|---|---|---|---|---|
| P059-TD-001 | STATIC_TEST_STRUCTURE | CONFIRMED | All thirty files contain zero Python assert statements | test_regression_graphite.py:55 |
| P059-TD-002 | INTERNAL_REGRESSION | INTERNAL_ONLY | Regression verify enforces bit equality on generated arrays | test_regression_graphite.py:72; test_regression_graphite.py:82 |
| P059-TD-003 | PRINT_ONLY_NUMERIC | OVERCLAIM_RISK | Area conservation is printed but not gated | test_regression_graphite.py:79; test_regression_graphite.py:80 |
| P059-TD-004 | MUTATING_TEST_MODE | CONTROL_REQUIRED | Capture mode overwrites the golden baseline | test_regression_graphite.py:61; test_regression_graphite.py:62 |
| P059-TD-005 | PORTABILITY | CORRECT | Golden path is hard-coded while only code path is overridable | test_regression_graphite.py:15; test_regression_graphite.py:17 |
| P059-TD-006 | PRINT_ONLY_VISUALIZATION | NOT_A_GATE | Sample tests are report-only visualizations | sample_test_v1018_2.py:106; sample_test_v1018_2.py:124 |
| P059-TD-007 | PRINT_ONLY_VISUALIZATION | NOT_A_GATE | LCO heat demo has no numeric failure condition | demo_lco_heat.py:22; demo_lco_heat.py:73 |
| P059-TD-008 | PRINT_ONLY_NUMERIC | NOT_A_GATE | Graph suite finite, parity, area, and dictionary checks are print-only | graph_suite_v1018_2.py:137; graph_suite_v1018_2.py:140; graph_suite_v1018_2.py:145 |
| P059-TD-009 | PRINT_ONLY_NUMERIC | NOT_A_GATE | Shape and area verdict in plot_dqdv is print-only | plot_dqdv.py:130; plot_dqdv.py:131 |
| P059-TD-010 | NORMALIZED_LINEAGE | COPY_FORWARD | Thirty versioned blobs reduce to five unchanged logic families | graph_suite_v1018_2.py:6 |
| P059-TD-011 | BRANCH_COVERAGE | MISSING | No harness activates n_T1 or theta_E | graph_suite_v1018_2.py:17 |
| P059-TD-012 | BRANCH_COVERAGE | MISSING | Critical production-code branches are untested | test_regression_graphite.py:25 |
| P059-TD-013 | EXTERNAL_VALIDITY | ABSENT | No public experimental dataset is loaded | test_regression_graphite.py:27; sample_test_v1018_2.py:43 |
| P059-TD-014 | AUTHORITY_LANGUAGE | OVERCLAIMED | PASS, DONE, and VALIDATION labels exceed enforced evidence | test_regression_graphite.py:81; demo_lco_heat.py:73; graph_suite_v1018_2.py:145 |
| P059-TD-015 | INTERNAL_REGRESSION | PARTIAL | Regression comparison ignores extra golden arrays | test_regression_graphite.py:71 |

## 핵심 결론

1. 실제 실패를 강제하는 것은 regression verify의 current-output
   array별 `np.array_equal`뿐이다. 이는 내부 baseline 보존이다.
2. regression의 area ratio는 출력만 하고 exit 상태에 반영하지
   않는다. capture는 golden을 덮어쓰므로 통제 없이 실행하면 안 된다.
3. sample, demo, graph suite, plot의 finite/parity/area/shape/expected
   값은 모두 출력 또는 그림일 뿐 gate가 아니다.
4. 30 versioned blobs는 5개 logic family의 경로/버전 복사다.
   `n_T1`과 `theta_E`를 활성화하는 표준 test/demo는 하나도 없다.
5. nonmonotone chronology, initial history, direct `L_V`의 $I=0$
   limit, default width derivative, C-rate unit, Einstein Tref와
   high-voltage doped LCO branch도 검사하지 않는다.
6. measured/public dataset을 읽는 경로가 없으므로 이 suite는
   external validity를 전혀 부여하지 않는다.

Gate: `PASS_P059_TEST_DEMO_ASSERTION_INVENTORY`.
