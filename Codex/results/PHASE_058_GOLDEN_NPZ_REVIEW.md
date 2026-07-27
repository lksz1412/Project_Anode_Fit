# Phase 058 golden NPZ 전수 감사

정본일: 2026-07-28  
대상: `Claude/docs/v1.0.13/golden_graphite_ref.npz`  
기계 결과: `Codex/results/PHASE_058_GOLDEN_NPZ_AUDIT.json`

## 전수 처분

107,324-byte NPZ의 13개 key를 모두 `allow_pickle=False`로 읽고,
v1.0.13 production code와 regression harness가 지정한 동일 호출로
재생성한 array를 전건 비교했다.

| 결과 | 수 |
|---|---:|
| key/shape/dtype 확인 | 13/13 |
| golden과 current 모두 finite | 13/13 |
| bit-exact | 1/13 (`V`) |
| bit-exact 실패 | 12/13 |
| `rtol=atol=1e-12` allclose | 13/13 |
| 전체 최대 절대차 | \(2.665\times10^{-15}\) |

production source와 NPZ의 실행 전후 hash는 동일했다.

## 무엇을 보존하는가

이 NPZ는 다음의 output continuity reference로는 유용하다.

- 0.03–0.34 V, 1000-point input grid
- 298.15 K equilibrium output
- 방전·충전 방향별 0.02, 0.2, 1.0 A output
- 258.15, 298.15, 318.15 K output
- 288.15–308.15 K의 \(T(V)\) output
- high-level `curve(direction="discharge", c_rate=0.2)` output

현재 환경의 12개 수치 output은 golden과 \(10^{-15}\) 수준에서만
다르므로, 적절한 tolerance 아래에서 같은 numerical family를
재현한다고 볼 수 있다.

## 무엇을 보존하지 않는가

이 NPZ에는 다음이 없다.

- raw 또는 processed experimental dQ/dV
- graphite/LCO/Si material identity와 specimen metadata
- 온도 안정화, current protocol, voltage calibration, smoothing metadata
- fitted parameter vector, optimizer state, bounds, seed, covariance
- train/validation split와 holdout metric
- Python/NumPy/BLAS/CPU provenance

따라서 이 파일을 “저장된 fit”, “원 optimizer state 재현” 또는
“실험 검증 결과”로 읽으면 안 된다. 정확한 지위는
`DERIVED_MODEL_OUTPUT_SNAPSHOT`이다.

## bit-exact gate 판정

`np.array_equal` gate는 현재 환경에서 12/13 FAIL이다.
차이가 \(10^{-15}\)로 작아 물리 차이는 아니지만, gate 정의상 실패다.
이는 단일 bitwise gate가 다음 서로 다른 문제를 혼합한다는 뜻이다.

1. runtime/platform provenance
2. 허용 가능한 floating-point drift
3. algorithmic regression
4. physical validity

후속 체계는 bitwise gate를 재현 환경 내부 provenance용으로만 제한하고,
수치 tolerance·물리 invariant·실험 holdout gate를 별도로 둬야 한다.

## Step 27.5 결론

13/13 array를 처분했고 NPZ의 권위 경계를 닫았다.
v1.0.10은 대응 golden이 저장소에 없어 과거 0-diff gate 자체를
재현할 수 없고, v1.0.13 golden은 tolerance continuity는 통과하지만
bit-exact gate는 실패한다.

이로써 Step 27의 code/test/demo/data 감사가 완료됐다. 다음은 Step 28의
PDF 8개 215 pages와 image 8개 전수 렌더·시각 검독이다.
