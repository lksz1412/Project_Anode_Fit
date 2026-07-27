# Phase 058 legacy test·demo 격리 실행 결과

정본일: 2026-07-28  
기준 commit: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`  
기계 결과: `Codex/results/PHASE_058_LEGACY_ISOLATED_EXECUTION.json`

## 실행 경계

11개 unique test/demo source와 대응 production module을 byte-identical
상태로 임시 디렉터리에 복사해 실행했다. hardcoded Windows path도
원문을 patch하지 않고 임시 디렉터리의 Linux filename으로 재현했다.
`PYTHONDONTWRITEBYTECODE=1`, `MPLBACKEND=Agg`를 사용했고, 실행 전후
보호 source와 v1.0.13 golden NPZ의 SHA-256이 모두 동일했다.

따라서 이 결과는 원본을 건드리지 않은 frozen-artifact 실행 결과다.
다만 실행 성공은 물리 타당성 판정이 아니라는 경계를 유지한다.

## 처분

| 처분 | 수 | 의미 |
|---|---:|---|
| `EXECUTED_REPORT_ONLY` | 9 | 그림·콘솔 보고 생성, 물리 assertion 없음 |
| `BLOCKED_MISSING_FROZEN_GOLDEN` | 1 | v1.0.10 golden이 repo 밖 임시 경로에만 있어 verify 불가 |
| `FAIL_BIT_EXACT_GOLDEN_FLOAT_DRIFT` | 1 | v1.0.13 repo golden과 현재 재생성 array가 bit-exact 불일치 |

## 핵심 관찰

### v1.0.10 regression은 재현 자료가 불완전하다

`test_regression_graphite.py verify`는
`C:\Users\...\scratchpad\p4_golden.npz`를 요구하지만 해당 golden은
저장소에 없다. 현재 source로 새로 capture한 뒤 같은 source로 verify하면
자기 동일성만 확인하므로 과거 release gate 재현으로 세지 않았다.

### v1.0.13 bit-exact gate는 현재 환경에서 FAIL이다

repo의 `golden_graphite_ref.npz` 13개 array 중 `V`만 bit-exact였고
나머지 12개는 최대 절대차
\(2.665\times 10^{-15}\) 이내로 달랐다. 이는 물리적으로 큰 차이가
아니지만, gate가 `np.array_equal`이므로 공식 결과는 FAIL이다.
따라서 bit-exact golden을 Python/NumPy/platform을 넘는 물리 검증으로
사용할 수 없다. 이후 회귀는 다음을 분리해야 한다.

1. 재현 환경을 완전히 고정한 bitwise provenance gate
2. 단위와 conservation을 포함한 수치 허용오차 gate
3. 독립 해석해·극한·sign gate
4. public experiment와 holdout을 쓰는 physical-validation gate

### demo 출력이 드러낸 범위

- fitted `n=0.12`이면 graphite local maximum이 4개가 된다.
  이는 empirical peak flexibility를 확인할 뿐 폭의 물리 유도가 아니다.
- default `n=1`은 네 transition이 한 개의 broad maximum으로 합쳐진다.
- v1.0.10 graph suite의 제한 창 면적비는 0.9790이며,
  regression의 0.03–0.34 V 창 면적비는 0.936308이다.
  넓은 창에서 회복되는 kernel tail 면적과 실제 fitting window의
  capacity accounting을 구분해야 한다.
- v1.0.10 sample/demo의 LCO 전자 entropy depth는 약
  \(-45.68\ {\rm J\,mol^{-1}\,K^{-1}}\)로 출력되지만,
  이는 hardcoded model target의 재생이지 독립 실험 검증이 아니다.
- v1.0.13 `plot_dqdv.py`에서 default graphite discharge와 charge의
  peak maximum은 동일하게 7.350으로 출력됐다. default kinetic/hysteretic
  response가 사용자 핵심 현상을 검증하지 않는다는 source 감사와 부합한다.

## 판정

Step 27.3의 실행 처분은 완료했다. 11/11 case가 성공·실패·blocker 중
하나로 분류됐고 원본 source는 보존됐다. 그러나 legacy test suite의
물리 validation gate는 성립하지 않는다. 다음 Step 27.4에서 현재
implementation과 독립된 계산으로 conservation, sign, limits,
temperature/current behavior를 검산한다.
