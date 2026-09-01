# Phase 066 Step 077 — Skew Derivative and Direct14 Fit Reproduction Result

정본일: 2026-09-01

계획: `Codex/plans/2026-09-01-phase066-v1025-v1025_2-lineage-detailed-plan.md`

입력 기준선: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`

선행 persistence: Step 76 exact-eight commit
`38e00020906e3a024e493c214c1a99a6f8ab07d2`, Python 3.12/3.14
`PASS_P066_STEP76_PERSISTENCE`

## 1. 판정

선택 Gate는
`CONDITIONAL_P066_STEP77_FIT_REPLAY_WITH_NONCONVERGED_SELECTED_TRIAL_AND_UNSEALED_PROCESS_LOGS`다.

이 조건부 판정은 frozen repository-derived `sigr.csv`를 실제 Direct14 입력으로 사용하여,
원 driver의 전처리·57-parameter contract·난수 진행 상태·12-start bounded least-squares
경로를 Python 3.12와 Python 3.14에서 각각 한 번 실행했고 두 런타임이 동일한 최량
곡선을 반환했다는 뜻이다. 다만 두 runtime에서 선택된 최저-cost trial 11은 모두
`max_nfev=6000`에서 `success=false`, `status=0`으로 끝났으므로 이 Gate는 optimizer
수렴 성공을 뜻하지 않는다. 저장된 8자리 벡터 자체의 ordered exact reproduction도
실패했으므로 exact historical optimizer-state reproduction을 뜻하지 않는다.

## 2. 실제 읽은 입력과 범위

- `Claude/results/comp_v24/sintef_data/sigr.csv`: 1–16,736행 전행·전셀 numeric traversal.
- `Claude/results/comp_v24/sintef_data/SOURCES.md`: 1–25행.
- `Claude/results/comp_v26_data/build_two_versions.py`: 1–223행.
- `Claude/results/comp_v26_data/test_skew_regsol_v2.py`: 1–300행.
- `Claude/results/comp_v26_data/bdd_dqdv.py`: 1–177행.
- `Claude/results/comp_v26_data/test_gallery_vs_regsol.py`: 1–251행.
- `Claude/results/comp_v26_data/out_versions/summary_versions.json`: 1–873행 strict parse와
  `C_skew/blend` 57-vector 직접 대조.
- `Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json`: 1–101행.
- Phase 057 AO–AW 관찰 문건 9개, v1.0.25/25.1/25.2의 skew 함수·release gate 관련
  범위, Phase 066 Step 77 계획 계약을 직접 재확인했다.

## 3. 수학 재유도

방향 \(s\in\{-1,+1\}\), \(w>0\), \(\alpha>0\)에 대해

\[
z=\frac{s(V-U)}{w},\qquad
\sigma=\frac{1}{1+e^{-z}},\qquad
\xi=\sigma^{\alpha}
\]

이고 chain rule은

\[
\frac{d\xi}{dV}
=s\frac{\alpha}{w}\sigma^{\alpha}(1-\sigma).
\]

따라서 Direct14의 양의 profile은 \(s=+1\)에서

\[
k(V)=\frac{dQ}{dV}
=Q\frac{\alpha}{w}\sigma^{\alpha}(1-\sigma)
\]

이다. 일반 방향에서는 이 식은 \(Q\lvert d\xi/dV\rvert\)이다. Frozen `func_dxi_eq`가 반환하는
양의 값도 \(s=-1\)에서는 signed derivative가 아니라 magnitude이므로, docstring의
`dξ/dV` 표기는 그 방향에서 엄밀하지 않다.

\(s=+1\)에서는 치환 \(d\xi=(d\xi/dV)dV\)로, \(s=-1\)에서는 역적분한계
또는 \(\lvert d\xi\rvert=\lvert d\xi/dV\rvert dV\)로 양의 profile의 무한 구간
면적은 \(Q\)이고, 정점은

\[
\sigma_\star=\frac{\alpha}{\alpha+1},\qquad
V_\star=U+s\,w\ln\alpha
\]

이다. 그러므로 \(U\)는 skew peak가 아니라 underlying logistic midpoint이며,
\(\alpha=1\)일 때만 정점과 일치한다. Profile slope는

\[
\frac{dk}{dV}=\frac{s}{w}k\{\alpha-(\alpha+1)\sigma\}
\]

이다. 수치검산은 \(\alpha=0.15,0.25,0.5,1,2,4,8\)에 대해 normalization 최대 오차
`4.441e-16`, 방향 포함 중앙차분 최대 상대오차 `8.749e-7`, 반사 오차
`1.3322676295501878e-15`,
\(\alpha=1\) 회수 오차 `0`을 얻었다.

Direct14 helper는 \(z\)를 `[-350,350]`으로 clip하여 overflow를 막는다. 다만 clip 밖에서
clipped coordinate는 상수인데 helper profile은 음의 포화측에서 미소한 양수이므로,
전 실수축에서 helper가 clipped coordinate의 exact derivative라는 주장은 하지 않는다.
Release의 `np.where` piecewise 식도 최종 선택값은 finite이나 양 branch를 eager evaluation해
극단 입력에서 선택되지 않은 exponential의 overflow warning을 낼 수 있다.

## 4. Raw input와 전처리

- 실제 fit 입력: `sigr.csv`, Git blob
  `4b06fefa1bb81de842386c95fbba5bdd431602d4`, SHA-256
  `e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6`.
- 컬럼: `V_vs_Li` [V versus Li/Li+], `Q_mAh` [mAh]. 용량 basis는 질량 정규화가
  없는 absolute mAh다.
- 16,735 numeric rows, malformed/nonfinite 0, Q unique 16,735.
- 전처리: stable Q sort → duplicate Q first V → increasing isotonic V(Q) →
  0.060–0.700 V, 0.5 mV grid → right-continuous cumulative Q difference →
  positive finite longest contiguous interval → direct/reciprocal Savitzky–Golay ensemble
  ratios 0.01/0.02/0.03, polynomial order 3 → 1,280 points.
- 처리 배열 SHA-256: V
  `6c7ca15d7b9eaf80561d2d2d834856c9b3076f31f6d7e4e6ce304ddb266020b4`, D
  `713c1de666d84e29edd55fbaab5b6321bfe505fb25cfe03c0b727a88bce743ce`.
- 데이터 면적: `3.4451462421322883 mAh`.
- `SOURCES.md`는 이 자료를 graphite+Si blend half-cell, pOCV, C/50, 약 25 °C로 선언한다.
  이 구분의 machine status는 `SOURCE_DECLARED_BUT_EXACT_BINDING_GROUND_NOT_FOUND`다.
  그러나 exact original Zenodo parquet key/checksum, specimen UUID·composition binding,
  정확한 protocol과 extraction cryptographic binding은 repository에서 `GROUND_NOT_FOUND`다.
  따라서 이 CSV를 original experimental parquet라고 부르지 않는다.

## 5. Optimizer contract와 실제 실행

- Parameter order: `[U×14, w×14, Q×14, alpha×14, bg]`, 57개 전부 free.
- Bounds: U=processed V 범위, `w=[1e-4,0.12]`, `Q=[1e-9,10A]`,
  `alpha=[0.15,8]`, bg=`[min(0,Dmin),Dmax]`.
- Objective: unweighted `model(V)-D` residual.
- Solver source-explicit options: bounds와 `max_nfev=6000`; historical SciPy version과
  source가 생략한 resolved defaults는 `GROUND_NOT_FOUND`다.
- 세 U seed 전략 × 각 4 restarts. Driver RNG는 `default_rng(23)`이지만 Direct14 전에
  8개 fit이 1,908 uniform scalars를 소비한다. Direct14 자체는 513개를 소비한다.
- Reconstructed 12-start matrix SHA-256:
  `3d5c9a7b04cfbd4a6773d9d45d64f46cb342b9adadc790960cc9264d71122ead`.

실행 결과:

| Runtime | NumPy / SciPy | Calls / converged | Best | Cost | R² | BIC |
|---|---|---:|---:|---:|---:|---:|
| Python 3.12.10 | 2.3.5 / 1.17.1 | 12 / 9 | 11 (비수렴) | 11.2870552249079 | 0.999649399285802 | −4760.58585278818 |
| Python 3.14.4 | 2.5.2 / 1.17.1 | 12 / 9 | 11 (비수렴) | 11.2870552249079 | 0.999649399285802 | −4760.58585278818 |

trial 11을 포함한 3개 trial은 `max_nfev` 경계였지만 finite bounded vector를 반환했다.
Frozen driver와 동일하게 12개 반환 cost의 최소값을 선택했으나, `runtime_success=false`와
`selected_trial_converged=false`로 기록해 이 수치 일치를 수렴 성공으로 승격하지 않았다.

Runtime record SHA-256은 Python 3.12
`279df24f1d7758dd35b5c217696d3c41557dba772d62eccb83148c4aae857a61`, Python 3.14
`2d271429355cf9a33424246d5216092b0230e125dff3d5571266c61de288aa3d`다.

실행 명령 형태는 다음과 같다. `<TEMP>`는 OS temporary root 아래의 disposable path다.

```text
py -3.12 -B -X utf8 Codex/work/v1025_phase066/build_phase066_step77.py fit --runtime-label python3.12 --output <TEMP>/p066_step77_py312.json
PYTHONPATH=<TEMP>/p066_py314_deps py -3.14 -B -X utf8 Codex/work/v1025_phase066/build_phase066_step77.py fit --runtime-label python3.14 --output <TEMP>/p066_step77_py314.json
py -3.12 -B -X utf8 Codex/work/v1025_phase066/build_phase066_step77.py collect --runtime312 <TEMP>/p066_step77_py312.json --runtime314 <TEMP>/p066_step77_py314.json
py -3.12 -B -X utf8 Codex/work/v1025_phase066/validate_phase066_step77.py
PYTHONPATH=<TEMP>/p066_py314_deps py -3.14 -B -X utf8 Codex/work/v1025_phase066/validate_phase066_step77.py
```

## 6. Stored result 비교

저장 vector는 driver가 `r.x`를 8자리로 반올림한 57-vector다. Original full-precision
`r.x`, full-precision prediction, cost/status/nfev/Jacobian/gradient, historical runtime은
`GROUND_NOT_FOUND`다.

- 저장 vector 자체를 현재 frozen input에서 평가하면 보고된 R²/BIC/peak RMSE/valley RMSE/
  area/bg의 각 반올림 값을 전부 회수한다.
- 두 runtime prediction은 서로 bit-identical했다: max absolute difference `0`.
- 새 runtime 대 stored-vector curve RMSE: `0.0005229047404880496 mAh/V`.
- 새 runtime cost는 stored-vector 평가 cost보다 상대 `5.310664260083087e-05` 높다.
- Ordered parameter max absolute difference는 `1.2482043497025828`로 사전 tolerance
  `5e-8`을 넘었다. 따라서 `ordered_parameter_exact_reproduction=false`다.
- 하지만 사전 curve/cost/R² tolerance는 통과해 repository-derived CSV의 in-sample
  numerical fit은 재현됐다.

이는 nonconvex 57-parameter fit에서 비슷한 곡선을 내는 서로 다른 parameter vector가
존재한다는 직접 증거다. 어느 vector도 물질상, gallery, species 또는 독립 식별성 권위로
승격하지 않는다.

## 7. 생성·수정 파일

- `Codex/work/v1025_phase066/build_phase066_step77.py`
- `Codex/work/v1025_phase066/validate_phase066_step77.py`
- `Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json`
- `Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json`
- 본 결과 문건
- 두 execution ledger
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

`Claude/**`, protected branch와 `main`은 수정하지 않았다.

## 8. 검증과 다음 조건

Validator는 raw hash, frozen source anchors, preprocessing V/D digests, RNG advancement와
12-start matrix, 모든 trial vector/hash/bounds, best selection, stored vector/metrics,
runtime curve/cost/parameter 비교를 독립 계산한다. Named negative controls는 derivative sign,
normalization, parameter order, data hash, bound, objective, synthetic-as-raw,
failed-fit-as-reproduced, fabricated original state, material promotion, wrong gate,
runtime seal, nested unknown key, production clip, arbitrary Git argv, dynamic `getattr`, direct
subprocess 우회, filesystem write, undeclared network import, fabricated preprocessing step/unit/
runtime metric/trial diagnostic, subscript dispatch, path `.open`, write-target substitution의
26종이다.

현재 conditional content Gate는 선택됐고 선택 trial 비수렴과 original process 외부
stdout/stderr/exit 기록 부재를 ceiling으로 보존한다. exact-eight commit/push/persistence 전 상태는
`PASS_PENDING_PERSISTENCE`다. 다음 Step 78은 commit subject
`audit(phase066): reproduce skew direct14 fitting`과 Python 3.12/3.14
`PASS_P066_STEP77_PERSISTENCE`가 확인된 뒤에만 시작한다.
