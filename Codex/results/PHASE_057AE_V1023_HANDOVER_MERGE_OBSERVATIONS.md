# Phase 057AE — v1.0.23 handover·index·merge 관찰

정본일: 2026-07-28
세부 Step: 19.7E
범위: 3 unique documents, 138 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `results/HANDOVER_v23.md`
- `results/INDEX_v23.md`
- `results/MERGE_READINESS_v23.md`

세 문건을 첫 행부터 마지막 행까지 전량 검독했다. 이 batch는
v1.0.23이 스스로 규정한 정체성, 완료 범위, 열린 항목, 다음
방향을 복원한다.

## Provisional Findings

### INTENT-PROV-0213 — v1.0.23의 실제 정체성은 검증된 재료모델 갱신이 아니라 선택적 방법 시연이다

handover가 가장 정직하게 적은 핵심은 다음이다.

- 사용자 JCP의 Fredholm 문제를 literal하게 이식하지 않았다.
- lag는 이미 O(N)인 Volterra/Markov 문제라 계산 절감도 없다.
- Fredholm ratio의 “미지 비를 기준 비로 치환”하는 철학만
  첫 Picard 근사로 옮겼다.
- 옵션은 기본 off이며, 기존 산출을 바꾸지 않는다.

따라서 v1.0.23의 과학적 기여는 조건부 수학 시연과 근사
진단이지, graphite/LCO/Si 데이터 설명력의 새 검증이 아니다.

판정:

- 이 좁은 정체성은 `PRESERVE`.
- “v1.0.23이 v1.0.22의 물리를 완결했다”는 해석은 `REJECT`.
- endgame에서는 이 자산을 본체 필수항이 아니라 후보 closure
  라이브러리로 재평가한다.

### INTENT-PROV-0214 — 식별성 작업을 건너뛴 채 물리 closure를 확정할 수 없다

P4 Fisher 정보기하는 사용자 별도 승인 항목이라 미실행됐고,
handover도 이를 열린 항목으로 남겼다. Fisher 정보 하나가
식별성을 완전히 해결하지는 않지만, 최소한 v1.0.23은
`chi_d`, `Omega`, 장벽, `L_V`, peak width 사이의 상관과
조건별 식별 가능성을 체계적으로 검사하지 않았다.

판정:

- P4 미실행은 계보상 `SKIPPED`, 실패가 아니다.
- 그러나 식별성 미검증 상태에서 상태 의존 barrier를 물질
  물리로 확정하는 것은 `REJECT`.
- 최종 계획에는 structural identifiability, sensitivity,
  profile likelihood/posterior correlation, 조건 외 검증을
  포함한다.

### INTENT-PROV-0215 — 곡선 QA가 열린 상태였으므로 merge readiness는 과학적 acceptance가 아니다

handover는 “양 버전 샘플 이미지 QA”를 다음 작업으로 남겼다.
검사항목도 전이 경계, 미해상 가드 전환, ratio 경로 kink,
연속·매끄러움·미분가능성으로 구체적이다. 그럼에도 같은 시점의
merge 문건은 병합 준비 완료를 선언했다.

판정:

- 소프트웨어 패키징 관점의 `MERGE_READY`는 당시 기록으로
  보존한다.
- curve morphology와 differentiability가 미검증이므로
  fitting-ready 또는 science-ready 판정은 `UNVERIFIED`.
- 최종 gate는 대표곡선 시각 QA뿐 아니라 수치 미분 연속성,
  switch-point 좌우극한, 적분면적, peak-tracking까지 자동화한다.

### INTENT-PROV-0216 — “중간 전류 실이득창”은 단위 교정과 데이터 근거 전에는 물리 명제가 아니다

handover와 merge 문건은 `0.1≲L_V/w≲0.6`을 중간 전류
실이득창이라 부르고, 기본 흑연은 휴면이라고 적었다. 그러나
이 범위는 synthetic sweep에서 정한 수치 근사 유효창이며,
당시 `L_V`에는 C-rate의 3,600배 시간단위 문제가 남아 있었다.

판정:

- 무차원 solver-regime으로서의 범위는 `NUMERICAL_ONLY`.
- 실제 C-rate의 “중간 전류”와의 대응은 `UNVERIFIED`.
- 단위 교정, 실제 전위폭 `w`, 속도상수 `k(T,U,x)`의
  독립 식별 후 물질별로 다시 계산한다.

### INTENT-PROV-0217 — 인계문건은 미확정 서지와 독립 초안을 명확히 남겼다

INDEX는 `appendix_phase_separation.tex`가 어느 master에도
편입되지 않은 standalone 초안임을 표시했고, handover는
Ref.6·7 원문 제목·DOI를 미확정으로 남겼다. 숨기지 않은
상태 표시는 보존할 가치가 있다.

판정:

- standalone 상분리 초안은 최종 정본의 일부로 자동 간주하지
  않는다.
- Ref.6·7은 원문 대조 전 `CONTENT_UNVERIFIED`.
- 최종 합성 시 “존재”, “편입”, “검증”, “채택” 상태를 서로
  다른 열로 관리한다.

### INTENT-PROV-0218 — forward 이론과 inverse fitting의 분리 원칙은 유지하되 연결 계약이 필요하다

handover는 v1.0.24 역문제(Tikhonov/Bayesian deconvolution)를
forward 문건과 scope 분리할 후보로 적었다. 이는 관측 해석과
물리 생성모델을 혼동하지 않게 하는 좋은 방향이다.

다만 최종 목표는 실제 공개 데이터를 설명하는 fitting
코드이므로 완전한 단절도 곤란하다. forward model의 상태·단위·
관측연산자와 inverse model의 parameter/prior/noise model 사이에
명시적 계약이 필요하다.

판정:

- 문건 내 물리와 inverse algorithm 설명의 분리는 `PRESERVE`.
- 별도 implementation companion에서 forward → observation →
  likelihood → inference의 추적 계약을 둔다.
- 적합 성공을 물리 진실로 오독하지 않도록 calibration과
  validation 결과를 분리한다.

## Direction Recovered

v1.0.23 인계에서 확인되는 사용자 방향은 “고등수학을 많이
넣는 것” 자체가 아니다. 사용자가 제공한 방법을 적용하기 전에
문제의 종과 적용 조건을 확인하고, 적용 불가능하면 솔직히
범위를 줄이며, 실제 곡선과 코드가 이론을 따르는지를 검증하는
것이다.

최종 작업에서는 이 원칙을 더 엄격하게 적용한다.

- 수학은 필요성과 관측 가능한 결과가 있을 때만 채택한다.
- 내부 구현 PASS와 실제 데이터 설명 PASS를 분리한다.
- 이론 문건의 코드 대응 부록은 별도 companion으로 이동한다.
- 미완·미편입·미확정 자산을 정본처럼 승계하지 않는다.

## Coverage Status

- 이 batch의 3문건, 138행은 `READ`.
- 누적 coverage 반영 후 목표는 228문건, 48,638행이다.
- v1.0.23 잔여 목표는 2문건, 234행이다.

## Next

Step 19.7F:
curve QA와 code guide 2문건 234행을 전문 검독하고 v1.0.23
intent queue를 닫는다.
