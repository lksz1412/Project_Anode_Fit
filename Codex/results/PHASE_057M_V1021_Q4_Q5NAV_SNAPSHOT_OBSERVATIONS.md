# Phase 057M — v1.0.21 Q4/Q5 항법 구조 관찰

정본일: 2026-07-28
세부 Step: 19.5D
범위: 2 unique documents, 2,727 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 두 JSON을 각각 400행 이하의 연속 구간으로 나누어
첫 행부터 끝 행까지 검독했다.

- `snapshot_v1021_q4.json`, 1,361행.
- `snapshot_v1021_q5nav.json`, 1,366행.

Q3→Q4와 Q4→Q5-navigation의 구조 diff도 다시 계산했다.

## Provisional Findings

### INTENT-PROV-0083 — Q4는 식 변경 없이 그림 label 다섯 개만 추가했다

Q3→Q4 diff:

- Ch1: `fig:UjT`, `fig:hysgap`, `fig:sumcurve`.
- Ch2: `fig:qrevsoc`, `fig:svibid`.
- equation 추가·삭제·hash 변경 0.
- bibliography 변화 0.
- appendix 변화 0.

판정:

- 당시 “A급 그림 5건만 보수적으로 반영”했다는 변경 대장과
  정확히 일치한다.
- 그림이 기존 식의 결과를 설명하는 교육 자산일 수는 있으나,
  새 물리식이나 새 실험 검증으로 세지 않는다.

### INTENT-PROV-0084 — 그림 label 추가와 외부 데이터 검증은 무관하다

Q3와 Q4의 `asset_unique`는
Ch1 336, Ch2 21로 동일하다. 새 그림은 문건 내부 벡터/TikZ 자산처럼
구조 체커가 외부 asset 증가로 세지 않는 형태다.

판정:

- 모델 내부 곡선, 제한 거동, 부호·형상 설명 그림으로 취급한다.
- 실제 LCO/graphite/Si 데이터 점, 오차막대, 데이터 DOI,
  train/validation 분할이 없으면 empirical validation으로
  승격하지 않는다.
- 최종 문건 그림은 “이론 개념도”, “모델 예측”, “실험 대조”를
  시각적으로 명확히 구분해야 한다.

### INTENT-PROV-0085 — Q5 항법은 새 물리가 아닌 임시 색인 계층이다

Q4→Q5-navigation diff는 Ch1에만 다음 label을 추가한다.

- `sec:appendix-nav`
- `ssec:nav-map`
- `ssec:nav-symbols`
- `fig:navmap`
- `tab:navsymbols`

equation, bibliography, Ch2, phase-separation appendix의 구조 변화는 0이다.

판정:

- 식 의존성 지도와 기호 충돌 해소라는 교육적 목적은 유효하다.
- 그러나 당시 handover에서 v1.0.22 제거가 이미 확정된 임시 이원판이다.
- 최종 문건에는 별도 항법판을 부활시키기보다
  단일 정본의 장별 기호표·선행조건·연결 문단으로 기능만 흡수하는
  방향을 우선 검토한다.

### INTENT-PROV-0086 — snapshot은 항법 토글의 실제 무영향성을 증명하지 않는다

Q5-navigation snapshot은 체커가 항법 부록을 함께 스캔한 결과다.
따라서 다음 자기주장은 이 JSON 하나로는 증명되지 않는다.

- 기본판 PDF가 byte/content 관점에서 불변인지.
- 토글이 equation numbering과 페이지 참조에 미치는 영향.
- 적용판과 미적용판 사이에 조건부 산문 외 숨은 차이가 없는지.

판정:

- 이원 빌드의 존재와 추가 label은 `STRUCTURAL_EVIDENCE`.
- 기능이 후속 철회됐으므로 최종 이론·코드 방향 결정에는
  제거 계보를 우선한다.

## Coverage Status

- 이 batch의 2문건, 2,727행은 `READ`.
- 누적 coverage 반영은 batch JSON 적용 후 112문건, 25,322행이다.
- v1.0.21 잔여는 4 snapshot, 5,505행이다.

## Next

Step 19.5E:
Q5/Q5b snapshot 2문건, 2,740행을 전문 검독해
끝-대-끝 예제·로드맵·측정 원리 보강의 실제 구조 변화를 확인한다.
