# Phase 057AP — v1.0.25 data addendum 관찰

정본일: 2026-07-28
세부 Step: 19.8J
범위: 1 unique document, 291 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `Claude/docs/v1.0.25.1/results/V1025_DATA_ADDENDUM.md`

1–160, 161–291의 연속 범위로 나눠 첫 행부터 마지막 행까지
전량 검독했다.

## Provisional Findings

### INTENT-PROV-0302 — addendum/supersession 기록 규약은 최종 계보 관리에 적합하다

문건은 v1.0.24 결과를 덮어쓰지 않고, 후속 측정이 뒤집은
파일·절·문장을 지목해 v1.0.25 판정으로 supersede한다.
또 작성자가 직접 실행한 확인과 마스터 세션 수치를 분리한다.

판정:

- 이 원본 보존, 조준 supersession, 측정 주체 표시 규약은
  `PRESERVE_AND_GENERALIZE`.
- 최종 작업 이력에는 claim ID, source blob, 실행 주체, 실행
  artifact, superseded-by를 machine-readable하게 둔다.

### INTENT-PROV-0303 — SINTEF graphite와 silicon CSV의 protocol 혼용 정정은 중요하다

레포 `gr.csv`는 `gr_A/p-ocv`, `si.csv`는
`si_Dhold/p-ocvhold`로 매핑되며, 점수와 V/Q 값 대조를 통해
독립 확인됐다고 기록한다. 그러므로 두 곡선을 동일 측정 조건의
재료 비교로 읽을 수 없다.

판정:

- protocol label 정정은 `PRESERVE`.
- `sigr.csv`의 원자료 key·protocol은 여전히 `UNVERIFIED`.
- 이후 모든 dataset row에는 cell, electrode, protocol, hold,
  rate, temperature, direction, cycle, extraction rule을
  필수 metadata로 둔다.

### INTENT-PROV-0304 — `p-ocvhold` 개선을 비평형 잔여에만 귀속한 주장은 통제 수준을 재확인해야 한다

7-transition fit에서 graphite `p-ocv` R² 0.9770,
`p-ocvhold` R² 0.9945를 보고 protocol만 바꾼 대조라고
서술한다. 그러나 이 addendum만으로는 같은 물리 cell의 동일
trajectory에 hold 유무만 바꾼 paired experiment인지 확인되지
않는다.

판정:

- hold가 더 평형에 가까운 곡선을 줄 가능성은
  `PHYSICALLY_PLAUSIBLE`.
- 개선분 전부를 비평형 잔여에 귀속하는 인과 주장은
  `UNVERIFIED`.
- raw metadata, paired-cell 구조, 전처리, uncertainty를
  Phase 067과 문헌·데이터 감사에서 확인한다.

### INTENT-PROV-0305 — regular-solution 이득의 부호 역전은 confounding 증거이지 보편적 기각 증거는 아니다

전이 수가 낮을 때 @3 순효과 +0.97 %p, graphite 7 +
Si 7일 때 −0.53 %p가 보고된다. 이는 kernel 이득이 basis
resolution과 강하게 얽혀 있음을 보여준다. 문건 자체도
v1.0.24와 v1.0.25의 cell·기준 구성이 다르고 다중-cell
확인이 없다고 명시한다.

판정:

- “@3 채택 근거 철회”는 `PRESERVE`.
- “regular-solution 물리가 불필요하다”는 보편 결론은
  `REJECT_AS_UNPROVEN`.
- 후보 free-energy model은 전이 수, cell, protocol을 통제한
  nested/held-out 비교로 다시 판정한다.

### INTENT-PROV-0306 — `Omega`를 kernel과 분리해 유지하면 fit과 상 판정이 서로 검증하지 못한다

regular-solution dQ/dV kernel은 삭제됐지만 `Omega`는
hysteresis gap, activation barrier, `Omega/RT` 상성격 판정에
남는다. logistic equilibrium이 `Omega`에서 파생되지 않으면
curve fit의 성공은 `Omega/RT` phase classification을
직접 지지하지 않는다.

판정:

- 동일 free-energy/chemical-potential closure에서 equilibrium,
  susceptibility, hysteresis, barrier modulation을 연결한다.
- 그 연결이 없는 `Omega`는 mechanism parameter가 아니라
  별도 empirical descriptor로 낮춘다.

### INTENT-PROV-0307 — 비상수 background 관찰은 유효하지만 “재료 거동” 단정은 이르다

0.3–0.9 V에서 background가 0.433에서 0.032로 감소하고
4 cell·2 protocol에서 같은 방향이라고 보고한다. 그러나
background는 unresolved broad transitions, side reaction,
normalization, differentiation, windowing의 영향을 함께 받을
수 있다.

판정:

- 상수 background의 전역적 부적합은 `PRESERVE`.
- 감소분의 물리 원인은 `UNRESOLVED`.
- background를 편의 상수나 광폭 peak 하나로 대체하기 전에
  measurement/preprocessing model과 broad thermodynamic
  population을 분리한다.

### INTENT-PROV-0308 — raw R² 비교만으로 전이 수·skew의 물리 필요성을 판정할 수 없다

흑연 5→7→9 transition과 skew에서 R²가 증가하고, silicon은
7→8에서 소폭 하락한다. 그러나 parameter 수, optimizer
variance, correlated residual, held-out error가 함께 보고되지
않았다.

판정:

- 수치 fit 가능성은 `PRESERVE_AS_CALIBRATION`.
- “7에서 포화”, “skew가 물리적으로 필요”, “9 transition이
  정당”이라는 결론은 `UNVERIFIED`.
- likelihood, noise model, information criterion, profile
  likelihood와 조건·cell holdout을 함께 쓴다.

### INTENT-PROV-0309 — 고정 전위 fit 악화는 전위 물리의 기각이 아니다

@4 U 고정이 graphite 반쪽셀에서 R²를 0.93215로 낮춘다.
이는 고정값·gauge·protocol·cell transfer가 맞지 않음을 보일
수 있지만, 평형 전위가 물리적으로 자유 parameter라는 뜻은
아니다.

판정:

- 이 dataset에서 해당 고정값의 부적합은 `PRESERVE`.
- 문헌 전위 prior와 실험 reference/gauge 변환을 분리해
  hierarchical uncertainty로 처리한다.

### INTENT-PROV-0310 — `gallery != phase`는 핵심 원칙이지만 basis 증가는 자동으로 물리적이지 않다

추가 center가 기존 peak 근처에 붙고 검출 peak 수가 prominence
threshold에 따라 달라진다는 관찰은 dQ/dV component 수를
thermodynamic phase 수로 읽으면 안 된다는 점을 뒷받침한다.

판정:

- 상 판정은 구조·열역학 근거에 위임한다는 원칙은
  `PRESERVE`.
- near-degenerate logistic component는 같은 상의 형상 표현일
  수 있지만, 곧바로 물리 gallery의 증거가 되지는 않는다.
- 최종 문건은 phase, stage, gallery, transition, basis
  component, detected peak를 서로 다른 용어로 정의한다.

### INTENT-PROV-0311 — graphite two-phase count는 addendum 내부에서도 미해결이다

A7은 staging transition 4개와 물리 two-phase 2개를 쓰지만,
보존된 선행 문건에는 “two-phase 4개” 표현도 있다. addendum은
이를 마스터 판단 사안으로 남긴다.

판정:

- Dahn 1991 전문과 후속 in-situ 구조 문헌을 직접 확인할
  때까지 `UNVERIFIED`.
- 숫자 하나를 seed comment나 abstract에서 가져와 정본으로
  승격하지 않는다.

### INTENT-PROV-0312 — 핵심 수치의 재현 provenance가 현재 끊겨 있다

신규 CSV 8종은 당시 session scratch에만 있었고, A2·A4–A7
수치의 재현 script가 repo에 등재되지 않았으며, 일부 gate는
작성 세션이 재실행하지 않았다. 따라서 서술된 수치와 결과
artifact만으로는 현재 독립 재현할 수 없다.

판정:

- 해당 결과는 `REPORTED_NOT_REPRODUCIBLE`로 유지한다.
- source checksum, immutable raw data 또는 fetch recipe,
  environment lock, extraction script, fit config, seed,
  optimizer trace, output table이 복구되기 전 validation
  authority로 사용하지 않는다.

### INTENT-PROV-0313 — 이 addendum은 연구의 핵심 온도·전류·고전압 범위를 검증하지 않는다

여기 기록된 주된 결과는 RT, C/50, half-cell pOCV 계열이며
doped high-voltage LCO, 다중 온도, 정전류에 따른 peak
저하·broadening, 온도·전류·전위 의존 barrier의 검증은 없다.

판정:

- equilibrium-shape calibration 자산으로 제한한다.
- 사용자가 시작점으로 제시한 현상은 이후 multi-condition
  validation matrix의 최상위 acceptance gate로 둔다.

## Direction Recovered

이 문건에서 복원되는 사용자 의도는 “수치가 좋아 보이면 채택”이
아니다.

1. 과거 기록은 보존하되 잘못된 주장은 출처와 범위를 지정해
   supersede한다.
2. protocol·cell·전처리가 다른 data를 같은 조건으로 묶지 않는다.
3. gallery 표현력과 thermodynamic phase 실재를 분리한다.
4. 채택 식, 물리 파라미터, 데이터 판정은 재현 가능한 artifact로
   연결한다.
5. single-condition R²는 출발점이지 최종 물리 검증이 아니다.

## Coverage Status

- 이 batch의 1문건, 291행은 `READ`.
- 누적 coverage 반영 후 목표는 259문건, 51,531행이다.
- 전체 Phase 057 잔여 목표는 12문건, 6,264행이다.

## Next

Step 19.8K:
document cascade TODO와 change ledger 2문건 339행을 전문
검독한다.
