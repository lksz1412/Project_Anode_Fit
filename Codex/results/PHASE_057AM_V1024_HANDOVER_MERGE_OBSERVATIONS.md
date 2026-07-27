# Phase 057AM — v1.0.24 handover·index·merge 관찰

정본일: 2026-07-28
세부 Step: 19.8G
범위: 3 unique documents, 210 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `results/HANDOVER_v24.md`
- `results/INDEX_v24.md`
- `results/MERGE_READINESS_v24.md`

세 문건을 첫 행부터 마지막 행까지 전량 검독했다. R4 뒤 공개
데이터 fitting, 전수 감사, 6-gallery 추가, 사용자 FB0–FB9가
사후 addendum으로 누적됐다는 시점을 구분했다.

## Provisional Findings

### INTENT-PROV-0275 — SINTEF 공개 데이터 fit은 보존할 중요한 경험적 성과다

handover/index는 SINTEF Zenodo 20086298 pOCV 데이터에 실제
코드 경로를 적용해 다음 적합도를 보고한다.

- graphite 5-feature: `0.9525 → 0.9731`.
- Si regular solution: `0.9944`.
- graphite+Si blend: `0.9848`.
- LCO: `0.94–0.9999` 범위.

이는 단순 synthetic test보다 강한 경험적 증거이며, 사용자가
“실제 데이터 피팅은 된다”고 확인한 내용과 정합한다.

판정:

- 공개 데이터 calibration 성공은 `PRESERVE`.
- dataset extraction, objective, parameter count/bounds,
  train/validation split, residual structure는 원 fit artifact와
  코드에서 재현한다.
- in-sample R²를 물리 유일성 또는 조건 외 예측으로 승격하지
  않는다.

### INTENT-PROV-0276 — v1.0.24 코드에는 binodal/Maxwell 처리가 있었으므로 직접 구현 감사가 필요하다

R2 요약만 보면 homogeneous kernel만 보였지만, R4 후 감사는
`_regsol_binodal_xa`가 `Omega>2RT`에서 Maxwell coexistence를
처리한다고 명시한다. 따라서 앞선 “두-상 처리가 전혀 없다”는
가능성은 코드 직접 검토 전 확정할 수 없다.

판정:

- binodal implementation의 존재는 `IMPLEMENTED_CLAIM`.
- 공존 조성, gap capacity, solid-solution wings, 임계 연속,
  normalization을 Phase 067에서 직접 검산한다.
- v1.0.25.2 kernel comparison과 수치 결과를 최고 우선 대조로
  둔다.

### INTENT-PROV-0277 — 문건을 코드에 맞춰 고친 순서는 사용자의 최종 권위 방향과 반대다

handover는 Si warnbox가 `Omega>2RT`를 kernel 범위 밖이라
썼지만 코드가 이미 Maxwell branch를 처리하므로 문건을 코드에
맞춰 정정했다고 기록한다.

과거 산출물의 불일치를 닫는 실무 조치로는 이해할 수 있다.
하지만 사용자의 최종 원칙은 물리·화학 문건이 근거가 되고
코드가 이를 100% 반영하는 것이다.

판정:

- 불일치를 숨기지 않고 교정한 이력은 `PRESERVE`.
- 최종 workflow에서는 physics derivation → numerical
  specification → code → conformance test의 권위 방향을 고정한다.
- 코드에 있는 기능을 정당화하려고 사후 이론을 쓰지 않는다.

### INTENT-PROV-0278 — regsol capacity `+0.063%` 버그의 발견·교정은 좋은 conservation gate 사례다

R4 후 전수 감사는 `_regsol_dqdv`의 discrete weight 때문에
용량이 0.063% 초과한 문제를 찾고 `wi=Q/xg.size`로 고쳐
면적 1.000000을 재검증했다.

판정:

- 이 결함과 교정은 `PRESERVE`.
- 각 transition과 전체 electrode에 대해
  `integral dQ/dV dV = Q`를 grid·temperature·parameter
  sweep 전 범위에서 gate로 일반화한다.
- 작은 면적 오류도 fitting에서 capacity parameter로 흡수될 수
  있으므로 “R²가 높다”는 이유로 무시하지 않는다.

### INTENT-PROV-0279 — 6-gallery는 해상도 basis이지 여섯 물리상이라는 뜻이 아니다

후반부에 6-gallery MSMR 상수가 opt-in으로 추가됐고, 문건도
gallery와 physical phase를 구분했다고 기록한다.

판정:

- basis-resolution과 phase count의 분리는 `PRESERVE`.
- 4/5/6 component 선택은 model selection 문제로 다루고,
  추가 component를 새 상 발견으로 해석하지 않는다.
- default 승격은 held-out likelihood와 parameter stability가
  지지할 때만 허용한다.

### INTENT-PROV-0280 — 단위 오류의 올바른 장벽 보정 부호는 기록됐지만 계산은 여전히 옛 gauge다

handover는

`dH_a_phys = dH_a + RT ln(3600) ≈ dH_a + 20.3 kJ/mol`

로 부호를 정정했다. 하지만 code value는 bit-exact로 그대로
두고 주석만 바꿨다.

판정:

- 장벽 gauge 변환식은 `PRESERVE`.
- v1.0.24 fitted barrier를 SI physical barrier로 직접 읽는 것은
  `REJECT`.
- 최종 fit에서는 SI rate law로 처음부터 재보정하고 uncertainty를
  보고한다.

### INTENT-PROV-0281 — 사용자 1차 정독 피드백은 최종 문체·경계의 직접 증거다

FB0–FB9는 다음 사용자 방향을 보여 준다.

- 본문 코드 함수명 제거, 당시에는 부록에 한정.
- 은유·의인·수필체·과도한 강조 marker 제거.
- 정의어와 기호 충돌 해소.
- 제목의 작업 N-tag와 자기-diff 언어 제거.
- LCO 장은 graphite 공통점보다 차이를 먼저 설명.
- overflow와 조판을 실제 페이지 단위로 검증.

판정:

- 이 방향은 `USER_DIRECTION_CONFIRMED`.
- 최신 지시에 따라 코드 내용은 부록에서도 분리해 별도
  implementation companion으로 이동한다.
- 최종 문건은 친절하고 상세하되 작업일지 말투가 아닌 전문
  교재·리뷰 register를 사용한다.

### INTENT-PROV-0282 — MERGE-READY 10/10은 calibration-ready에 가깝고 science-complete가 아니다

merge gate에는 build, structure, code regression, internal
derivation, 공개 pOCV fit이 포함돼 있다. 반면 다음을 잔여로
남겼다.

- finite-rate dQ/dV regular-solution 배선.
- stage-2L 다온도 정량.
- Ω point identification.
- LCO electronic entropy의 다온도 검증.
- doped high-voltage LCO.

판정:

- 당시 branch integration 상태는 `MERGE_READY_HISTORY`.
- 사용자 최종 목표의 `SCIENCE_COMPLETE`는 `REJECT`.

### INTENT-PROV-0283 — 공개 fit 성공은 최종 데이터 phase의 기준선을 제공한다

v1.0.24를 폐기하지 않고, 재현 가능한 공개 fit을 baseline으로
삼는다. 최종 모델은 최소한 이 적합 성능과 보존법칙을 유지하면서
다음 추가 예측을 해야 한다.

- 동일 전극의 온도 이동.
- 0-current 대비 finite-current peak suppression/broadening.
- charge/discharge 방향성.
- composition/dopant 변화.
- 조건 외 electrode/dataset transfer.

이 기준을 못 넘는 더 복잡한 이론은 채택하지 않는다.

## Coverage Status

- 이 batch의 3문건, 210행은 `READ`.
- 누적 coverage 반영 후 목표는 254문건, 50,578행이다.
- 전체 Phase 057 잔여 목표는 17문건, 7,217행이다.

## Next

Step 19.8H:
v1.0.24 Markdown code guide 1문건 374행을 전문 검독한다.
