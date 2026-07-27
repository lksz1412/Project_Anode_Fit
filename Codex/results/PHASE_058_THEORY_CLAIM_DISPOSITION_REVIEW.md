# Phase 058 v1.0.10–v1.0.13 이론 주장 전건 처분

정본일: 2026-07-28  
대상: Phase 058 Step 32.1  
source inventory:
`Codex/results/PHASE_058_THEORY_EQUATION_CLAIM_MATRIX.json`  
최종 처분:
`Codex/results/PHASE_058_THEORY_CLAIM_DISPOSITIONS.json`  
분류기:
`Codex/work/v1010_v1013_phase058/classify_phase058_equations.py`  
검산기:
`Codex/work/v1010_v1013_phase058/validate_phase058_theory_claim_dispositions.py`

## 결론

v1.0.10, v1.0.12, v1.0.13의 theory source 6개에 있는 displayed
equation 323건, unique label 132개를 모두 다음 일곱 상태 중
하나로 처분했다.

| 상태 | 수 |
|---|---:|
| `PRESERVE` | 145 |
| `CORRECT` | 35 |
| `SUPERSEDE` | 29 |
| `EMPIRICAL_ONLY` | 29 |
| `THEORY_ONLY` | 66 |
| `REJECT` | 6 |
| `UNVERIFIED` | 13 |
| **합계** | **323** |

미배정은 0이다. 최종 판정은

`ALL_323_THEORY_EQUATION_OCCURRENCES_ARE_DISPOSED_WITH_LATEST_CORRECTIONS_NOT_MISTAKEN_FOR_EXTERNAL_VALIDATION`

이다.

이 수치는 식의 “정답률”이 아니다. 같은 식이 세 version에 반복되면
occurrence도 세 번 센다. 목적은 역사적 source 각 위치가 다음
정본에 어떤 권위로 넘어가는지 누락 없이 결정하는 것이다.

## 1. 결정 상태의 의미

### `PRESERVE`

명시한 적용 범위에서 수학·물리 항등식을 유지한다.

대표 자산:

- 이상 grand-canonical partition과 occupancy
- ideal Nernst/logistic
- regular-solution 자유에너지와 homogeneous curvature
- 전하 보존과 ideal peak 면적·높이
- \(G=H-TS\), \(\partial U/\partial T=\Delta S/F\)의 sign
  contract
- configurational, vibrational, Sommerfeld endpoint 식
- reversible heat identity
- LCO charge를 cathode delithiation에 연결하는 direction slot

`PRESERVE`는 material parameter나 public-data 적합까지 승인한다는
뜻이 아니다.

### `CORRECT`

핵심 구조는 쓸 수 있지만 scope, sign, phase topology, width
semantics 또는 material interpretation을 고쳐야 한다.

대표:

- nonideal branch에서 logistic을 보편 평형식으로 쓰는 것
- spinodal voltage difference를 measured hysteresis gap으로 읽는 것
- 다중 transition 단순합을 common-host topology로 읽는 것
- arbitrary \(n_j\)의 entropy/config identity
- LCO–MSMR mapping의 함수형 동형과 물리량 동일성 혼동
- implicit entropy weighting의 extent·width 전제

### `SUPERSEDE`

과거 식을 나중 version이 실제로 바꿨을 때 과거 occurrence를
정본 후보에서 제외한다.

- v1.0.10→v1.0.12 changed labels 4개
- v1.0.10/v1.0.12→v1.0.13 changed labels 15개

총 29 occurrences다. 최신식이 있다고 해서 외부 검증된 것은
아니며, 최신식 자체는 다시 다른 여섯 상태 중 하나를 받는다.

### `EMPIRICAL_ONLY`

데이터를 표현할 수는 있지만 미시적 정체를 부여하지 않는다.

대표:

- \(w=nRT/F\)의 arbitrary \(n\)
- cut affinity
- grid prescription
- branch-center 축소 인자
- \(\Delta H_a-\chi\Omega\) barrier correction
- MIT composition-logistic gate
- \(x\leftrightarrow\xi\) 선형 mapping

### `THEORY_ONLY`

수학적 reduced model 또는 후보식이지만 실행·실험 폐쇄가 없다.

대표:

- causal relaxation length와 memory kernel
- finite-current peak-shape candidate
- ensemble forward broadening integral
- LCO regular-solution 후보
- entropy component factorization
- \(g(E_F,x)\)가 주어졌을 때의 electronic correction path

### `REJECT`

그대로는 허용할 수 없다.

대표:

- coulomb capacity와 h\(^{-1}\) C-rate를 factor 3600 없이
  \(I=c_\mathrm{rate}Q\)로 잇는 계약
- 불연속 numerical branch handoff를 물리 폐쇄로 읽는 것

### `UNVERIFIED`

재료별 귀속 또는 외부 유효성 증거가 없다.

대표:

- LCO three-transition default
- LCO dopant correction
- LCO peak parameterization
- material-specific \(\Omega\), entropy slot과 phase assignment

## 2. version별 의미

| version | Preserve | Correct | Supersede | Empirical | Theory-only | Reject | Unverified |
|---|---:|---:|---:|---:|---:|---:|---:|
| v1.0.10 | 35 | 8 | 14 | 7 | 16 | 2 | 0 |
| v1.0.12 | 40 | 11 | 15 | 10 | 24 | 2 | 6 |
| v1.0.13 | 70 | 16 | 0 | 12 | 26 | 2 | 7 |

v1.0.13에서 보존 수가 늘어난 것은 Part 0의 이상 통계역학 식이
추가됐기 때문이다. 동시에 `CORRECT`, `EMPIRICAL_ONLY`,
`THEORY_ONLY`, `UNVERIFIED`가 63건이다. 그러므로 최신식 수의
증가를 물리 완결로 읽을 수 없다.

## 3. 핵심 label의 판정

| label | 판정 | 이유 |
|---|---|---|
| `eq:n0map` | `REJECT` | C-rate–coulomb 계약의 factor 3600 누락 |
| `eq:wbase` | `EMPIRICAL_ONLY` | \(n\)은 유도된 다중도가 아님 |
| `eq:xieq` | `CORRECT` | ideal/phenomenological 범위와 평형 방향 분리 필요 |
| `eq:dUhys` | `CORRECT` | spinodal 차와 평형·측정 hysteresis는 다름 |
| `eq:branch` | `REJECT` | 불연속 numerical handoff |
| `eq:ggate` | `EMPIRICAL_ONLY` | energy Fermi 점유가 composition gate를 유도하지 않음 |
| `eq:lco-dope` | `UNVERIFIED` | doped high-voltage LCO 화학 검증 부재 |
| `eq:U1T2` | `PRESERVE` | \(T\)-선형 entropy 적분의 \(1/2\) 계수는 유효 |
| `eq:qrev` | `PRESERVE` | 명시적 current/electrode sign 계약 아래 유효 |
| `eq:lco-sigmaslot` | `PRESERVE` | cell label과 electrode delithiation 분리 |

## 4. 정본 승계 원칙

새 문건은 `PRESERVE` 식을 복사하는 것으로 시작하지 않는다.

1. 같은 claim의 역사적 중복을 한 정본 식으로 합친다.
2. `PRESERVE`의 적용 범위를 식 바로 앞에 쓴다.
3. `CORRECT`는 수정 유도와 limit test를 통과해야 들어간다.
4. `EMPIRICAL_ONLY`는 미시 명칭을 붙이지 않고 observation/fitting
   layer에 둔다.
5. `THEORY_ONLY`는 구현·실험 gate가 생길 때까지 후보로 표시한다.
6. `UNVERIFIED` default는 재료 상수로 승격하지 않는다.
7. `REJECT`와 `SUPERSEDE` 식은 새 본문에 재도입하지 않는다.

## 5. 재현성

원본 323 equation row의 순서에 대해

```text
equation_id|decision
```

을 연결한 SHA-256은

`50016c639b06ceb4e5be417fbf35a5cf321b4e300eb1f6955b93ca691742f415`

다. Source matrix의 행이 바뀌거나 결정 규칙이 달라지면 gate가
실패한다. 32/32 checks가 통과했다.

## 6. 다음 단계

Step 32.2는 식의 물리 판정과 별개로 다음 네 축을 맞댄다.

1. theory가 주장했는가
2. production code가 구현했는가
3. test가 failure gate로 검사했는가
4. PDF/image/data artifact가 같은 상태에서 생성됐는가

각 축의 PASS가 무엇을 검사하지 않았는지도 함께 기록한다.
