# Phase 059 isolated runtime review

기존 소스와 golden을 수정하지 않는 disposable temporary directory에서
6 versions × 6 task types를 실행했다. regression은 `verify`만
사용했고 `capture`는 호출하지 않았다.

## 결과

- runs: 36
- zero exit: 30
- regression PASS banners: 0
- NPZ mutations: 0
- generated non-input outputs: 24
- exact golden arrays per version: 1/13, 1/13, 1/13, 1/13, 1/13, 1/13
- tolerant arrays (`rtol=0`, `atol=1e-12`) per version: 13/13, 13/13, 13/13, 13/13, 13/13, 13/13
- maximum absolute golden difference: 4.330e-15
- regression area ratio range: 0.936308–0.936308

| Version | Task | Exit | PASS banner | stdout lines | stderr lines | Outputs |
|---|---|---:|---|---:|---:|---:|
| v1.0.14 | production_selfcheck | 0 | False | 42 | 0 | 0 |
| v1.0.14 | regression_verify | 1 | False | 15 | 0 | 0 |
| v1.0.14 | sample_test | 0 | False | 6 | 0 | 1 |
| v1.0.14 | demo_lco_heat | 0 | False | 17 | 0 | 1 |
| v1.0.14 | graph_suite | 0 | False | 20 | 603 | 1 |
| v1.0.14 | plot_dqdv | 0 | False | 5 | 0 | 1 |
| v1.0.15 | production_selfcheck | 0 | False | 42 | 0 | 0 |
| v1.0.15 | regression_verify | 1 | False | 15 | 0 | 0 |
| v1.0.15 | sample_test | 0 | False | 6 | 0 | 1 |
| v1.0.15 | demo_lco_heat | 0 | False | 17 | 0 | 1 |
| v1.0.15 | graph_suite | 0 | False | 20 | 603 | 1 |
| v1.0.15 | plot_dqdv | 0 | False | 5 | 0 | 1 |
| v1.0.16 | production_selfcheck | 0 | False | 42 | 0 | 0 |
| v1.0.16 | regression_verify | 1 | False | 15 | 0 | 0 |
| v1.0.16 | sample_test | 0 | False | 6 | 0 | 1 |
| v1.0.16 | demo_lco_heat | 0 | False | 17 | 0 | 1 |
| v1.0.16 | graph_suite | 0 | False | 20 | 603 | 1 |
| v1.0.16 | plot_dqdv | 0 | False | 5 | 0 | 1 |
| v1.0.17 | production_selfcheck | 0 | False | 42 | 0 | 0 |
| v1.0.17 | regression_verify | 1 | False | 15 | 0 | 0 |
| v1.0.17 | sample_test | 0 | False | 6 | 0 | 1 |
| v1.0.17 | demo_lco_heat | 0 | False | 17 | 0 | 1 |
| v1.0.17 | graph_suite | 0 | False | 20 | 603 | 1 |
| v1.0.17 | plot_dqdv | 0 | False | 5 | 0 | 1 |
| v1.0.18.1 | production_selfcheck | 0 | False | 42 | 0 | 0 |
| v1.0.18.1 | regression_verify | 1 | False | 15 | 0 | 0 |
| v1.0.18.1 | sample_test | 0 | False | 6 | 0 | 1 |
| v1.0.18.1 | demo_lco_heat | 0 | False | 17 | 0 | 1 |
| v1.0.18.1 | graph_suite | 0 | False | 20 | 603 | 1 |
| v1.0.18.1 | plot_dqdv | 0 | False | 5 | 0 | 1 |
| v1.0.18.2 | production_selfcheck | 0 | False | 42 | 0 | 0 |
| v1.0.18.2 | regression_verify | 1 | False | 15 | 0 | 0 |
| v1.0.18.2 | sample_test | 0 | False | 6 | 0 | 1 |
| v1.0.18.2 | demo_lco_heat | 0 | False | 17 | 0 | 1 |
| v1.0.18.2 | graph_suite | 0 | False | 20 | 603 | 1 |
| v1.0.18.2 | plot_dqdv | 0 | False | 5 | 0 | 1 |

## 증거 한계

1. zero exit는 실행 가능성만 뜻한다.
2. regression PASS는 각 version의 저장 golden과 current-output
   bit equality만 뜻한다. 현재 환경에서는 1/13 array만 exact이고
   전 배열이 `atol=1e-12` 안에서 일치해 strict gate의 환경
   비이식성을 확인했다.
3. sample/demo/graph/plot의 DONE 또는 VALIDATION 문구는 Step 34.2
   판정대로 print-only다.
4. regression이 출력한 유한전압창 area ratio는 0.9363으로
   가이드의 0.95 하한보다 낮지만 exit 판정에 포함되지 않는다.
5. 이 실행은 `n_T1`, `theta_E`, nonmonotone history, direct
   `L_V` zero-current, unit conversion 또는 measured data를 새로
   검증하지 않는다.

Gate: `CONDITIONAL_P059_ISOLATED_RUNTIME`.
