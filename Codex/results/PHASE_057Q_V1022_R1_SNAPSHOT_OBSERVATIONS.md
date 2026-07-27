# Phase 057Q — v1.0.22 R1 구조 snapshot 관찰

정본일: 2026-07-28
세부 Step: 19.6B
범위: 1 unique document, 1,391 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

`Claude/docs/v1.0.22/results/snapshot_v1022_r1.json`을 다음 연속 구간으로
나누어 첫 행부터 마지막 행까지 검독했다.

- lines 1–350
- lines 351–700
- lines 701–1,050
- lines 1,051–1,391

그 뒤 `snapshot_v1021_q7.json`과 label, equation block hash,
bibliography key 및 master별 자산 수를 대조했다.

## Provisional Findings

### INTENT-PROV-0106 — R1은 식의 개정이 아니라 물질 책임의 재배치였다

전역 비교 결과는 다음과 같다.

| 항목 | v1.0.21 Q7 | v1.0.22 R1 | 차이 |
|---|---:|---:|---|
| 고유 label | 355 | 348 | navigation label 7개 제거 |
| equation block | 188 | 188 | 추가 0, 제거 0, hash 변경 0 |
| bibliography key | 66 | 66 | 추가 0, 제거 0 |
| master별 `asset_unique` 합 | 357 | 357 | 총수 보존 |

구체적으로 기존 Ch1에 있던 LCO equation block 41개가 새 Ch2로
이동했고, 기존 Ch2에 있던 열역학·혼합·가역열 equation block
32개가 새 Ch1로 이동했다. 식 이름과 hash는 모두 동일하다.

판정:

- R1은 새 물리식의 제안이나 수정으로 해석하지 않는다.
- 공통 graphite/열 골격과 LCO 고유항을 분리한
  구조적 provenance로 `PRESERVE`.
- 식 hash 보존은 산문 의미·물리 정당성·코드 정합성을 보증하지 않는다.

### INTENT-PROV-0107 — 제거된 것은 임시 navigation 표지층뿐이다

v1.0.21 Q7 대비 사라진 label은 다음 7개뿐이다.

- `fig:navmap`
- `sec:appendix-nav`
- `ssec:nav-map`
- `ssec:nav-roadmap`
- `ssec:nav-symbols`
- `tab:navroadmap`
- `tab:navsymbols`

이에 대응하는 equation block 제거는 없다.

판정:

- v1.0.21의 임시 항법판을 최종 이론 자산으로 승격하지 않고
  장 구조 자체로 대체하려는 방향은 `PRESERVE`.
- 항법판 제거만으로 독자가 공통항과 재료 고유항의 연결을 실제로
  따라갈 수 있는지는 이후 원고 전문에서 별도 판정한다.

### INTENT-PROV-0108 — R1 시점 Ch3 Si는 이론장이 아니라 자리표시자다

R1 snapshot의 `ch3_si_v1.0.22.tex`은 다음만 가진다.

- 7 labels.
- 0 equation blocks.
- 0 assets.
- 14 bibliography keys.

labels도 `si-anchor`, `si-facts`, `si-gap`, `si-map`,
`si-partial`, `tab:simap`처럼 조사·공백·지도 성격이다.

판정:

- R1 시점에는 Si/SiO_x/Si–C/blend의 독립 수식 체계가 없다.
- 이 snapshot을 근거로 v1.0.22 전체가 Si 물리를 이미 완성했다고
  서술하는 것은 `REJECT`.
- 후속 R4–R6에서 실제로 추가된 식·코드·제약을 분리해 추적한다.

### INTENT-PROV-0109 — phase-separation appendix는 bit-identical 보존됐다

`appendix_phase_separation.tex`은 양 snapshot에서 모두 다음과 같다.

- 30 labels.
- 19 equation blocks.
- 0 assets.
- 0 bibliography keys.
- equation block 이름과 hash 변경 0.

판정:

- R1 재편이 phase-separation 부록을 손상하지 않았다는
  구조 증거로 `PRESERVE`.
- 그러나 binodal/spinodal/Maxwell/CNT/Cahn–Hilliard 식의 물리적
  완전성은 후속 전문 및 독립 재유도 없이는 승인하지 않는다.

### INTENT-PROV-0110 — snapshot gate의 권위 범위는 구조 보존까지다

snapshot은 label, 식 block hash, master별 자산 수와 bibliography key를
추적하는 데 강하지만 다음을 직접 검증하지 않는다.

- 산문에서 식의 전제와 적용 범위를 왜곡했는가.
- 동일 식이 올바른 물리로 해석되는가.
- 재배치 뒤 교차참조가 교육적으로 충분한가.
- 코드가 그 식을 정확히 구현하는가.
- 실제 온도·전류·조성 데이터에 설명력을 갖는가.

판정:

- “R1에서 식·서지 자산의 미로그 손실 없음”은 구조 gate로 보존한다.
- 이를 과학적 정합성이나 실험 검증 PASS로 확대하는 것은 `REJECT`.
- 이후 Phase 063·067에서 산문, 식 재유도, 코드 및 데이터 gate를
  각각 독립 수행한다.

## Coverage Status

- 이 batch의 1문건, 1,391행은 `READ`.
- 누적 coverage 반영 후 목표는 124문건, 32,695행이다.
- v1.0.22 잔여 목표는 93문건, 14,987행이다.

## Next

Step 19.6C:
R2 Ch1 completion 경쟁 brief·seam·bridge·removal 12문건 811행을
전문 검독해 후보안, 채택안, 제거안과 구조 gate를 구분한다.
