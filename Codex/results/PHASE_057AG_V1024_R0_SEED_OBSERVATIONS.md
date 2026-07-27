# Phase 057AG — v1.0.24.1 archive·R0·seed 관찰

정본일: 2026-07-28
세부 Step: 19.8A
범위: 4 unique documents, 157 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `ARCHIVE_NOTE.md`
- `results/PHASE_R0_RESULT.md`
- `results/V1024_REFLECT_EXECUTION_LEDGER.md`
- `results/REFLECT_SEED_TABLE.md`

네 문건을 첫 행부터 마지막 행까지 전량 검독했다.

## Provisional Findings

### INTENT-PROV-0228 — v1.0.24.1은 사용자 편집 피드백을 반영한 동결 스냅샷이지 새 과학 정본이 아니다

archive note는 v1.0.24.1을 v1.0.24의 F-01–F-11, 어조 강화,
별표 제거를 거친 frozen snapshot으로 규정한다. 물리 골격,
수식, 라벨, 코드 로직은 바꾸지 않았고 폴더명만 `.1`이며
내부 파일명은 v1.0.24를 유지한다.

판정:

- 이 provenance와 동결 경계는 `PRESERVE`.
- v1.0.24.1이라는 번호만으로 과학 내용이 v1.0.24보다
  검증됐다고 보지 않는다.
- 후속 판정은 v1.0.24 물리 변경과 v1.0.24.1 편집 변경을
  분리한다.

### INTENT-PROV-0229 — R0는 v1.0.23을 bit-exact 복제했으므로 기존 결함도 모두 상속했다

R0의 목표는 v1.0.23을 버전 문자열만 바꿔 복제하고 빌드,
구조, 기존 게이트를 통과하는 것이었다. 이는 clean baseline과
delta 추적에는 적절하다.

그러나 v1.0.23에서 확인된 C-rate 단위, 기본 동역학 휴면,
Si/Si-C 미완결, LCO 공통-kernel 과잉공유도 그대로 복제된다.

판정:

- baseline parity는 `LINEAGE_PRESERVE`.
- R0 PASS를 물리 acceptance로 읽는 것은 `REJECT`.
- v1.0.24의 가치는 R1/R2 이후 실제 delta로만 판정한다.

### INTENT-PROV-0230 — C-rate 3,600배 오류를 인정했지만 bit-exact 우선 대응은 물리 교정이 아니다

seed table은 정확히 다음 문제를 기록한다.

`c_rate[1/h]`와 `k_0[1/s]`를 섞어 `func_L_q`에 3,600배
불일치가 생겼고, `dH_a` 물리해석이 약 20 kJ/mol 이동한다.

하지만 반영 목표를 “주석+환산상수, 곡선 bit-exact,
기존 tier-C 장벽에 흡수”로 잡았다. 단위 오류가 적합 파라미터에
흡수되어 곡선이 맞는다는 것은 structural non-identifiability의
증거이지 단위계가 옳다는 뜻이 아니다.

판정:

- 결함 발견과 영향량은 `PRESERVE`.
- 기존 곡선 bit-exact를 유지하는 대응은 최종 물리 correction으로
  `REJECT`.
- SI 일관식으로 교정하고 장벽·prefactor를 다시 식별해야 한다.

### INTENT-PROV-0231 — Si 정칙용액 방향은 후보로 유용하지만 seed의 “실측·무근거 0” 표현은 과하다

seed는 a-Si를 `Omega<2RT` 단일상 Frumkin/regular-solution
kernel로 두고 logistic 대비 적합 개선을 제시한다. sharp
two-phase보다 넓은 고용체 응답이라는 방향은 검토 가치가 있다.

그러나 근거의 중심은 기존 peak 폭을 모델 단위 `RT/F`로
환산한 값과 내부 ablation이다. `delta` cap의 바닥
`0.2RT 지향`, 물질별 Omega 시드, feature 수는 독립 실험으로
확정된 상수가 아니다.

판정:

- regular-solution single-phase 후보는 `THEORY_CANDIDATE`.
- `0.2RT` cap/floor와 fit-derived seed는 `EMPIRICAL_ONLY`.
- arbitrary cap을 최종 물리 기본값으로 승격하지 않는다.

### INTENT-PROV-0232 — graphite·LCO feature 증가는 구조 가설과 곡선 분해를 구분해야 한다

seed는 graphite 5-feature staging, stage-2L pair, LCO 전이별
Omega를 추가하며 내부 R² 개선과 문헌 표지를 근거로 든다.
이는 관찰 peak를 더 세밀하게 설명하는 후보 분해다.

하지만 feature 수가 늘면 적합 자유도만으로도 R²가 상승할 수
있다. 특히 LCO의 high-voltage dopant 안정화와 전이별 물리
식별은 이 seed table에서 검증되지 않았다.

판정:

- 문헌이 지지하는 phase/feature 후보는 `PRESERVE_AS_HYPOTHESIS`.
- feature count와 entropy/Omega 수치를 확정 기본값으로 두는
  것은 `UNVERIFIED`.
- information criterion, held-out 조건, 독립 structural
  measurement와 함께 판정한다.

### INTENT-PROV-0233 — 사용자 편집 방향은 중립적 전문문체와 코드 경계로 복원된다

archive note에 남은 사용자 피드백 결과는 다음과 같다.

- 은유·의인·구어를 중립화한다.
- 별표 같은 강조 marker를 본문에서 제거한다.
- 기호 충돌과 식 설명을 명료화한다.
- 코드 언급은 당시 규칙상 부록에만 둔다.
- 조판과 장별 서사 균형을 교정한다.

현재 사용자는 경계를 더 엄격히 하여 이론 문건에는 물리·화학만
두고 코드 내용을 배제하라고 했다.

판정:

- 중립적 대학원 교재 문체, 명료한 기호, 장 균형은
  `USER_DIRECTION_PRESERVE`.
- “코드=부록 전용”은 최신 지시로 `SUPERSEDE`하며,
  코드 지도는 별도 companion에 둔다.
- 상세성은 장식적 표지 수가 아니라 유도·가정·한계·문헌
  설명의 충분성으로 확보한다.

### INTENT-PROV-0234 — 토글 기본값이 최초 구현에서 사양과 달랐던 이력은 code drift 경고다

실행 원장은 LCO electronic-entropy 토글이 seed/brief의
기본 OFF 사양에서 벗어났고, 사용자 지적 뒤 R5-1에서 다시
OFF로 고쳤다고 기록한다.

판정:

- 사용자 지적과 교정 이력은 `PRESERVE`.
- 문건 사양이 있어도 코드 기본값이 이탈할 수 있으므로 최종
  conformance는 prose review만으로 충분하지 않다.
- default value, unit, branch gate를 machine-readable contract와
  test로 고정한다.

### INTENT-PROV-0235 — Ref.6·7 서지 완성은 내용 검증과 별개다

seed table에서 Ref.6과 Ref.7의 제목·DOI가 채워졌다. 이는
v1.0.23의 bibliographic gap을 닫는다.

판정:

- 서지 식별자는 `BIBLIOGRAPHICALLY_VERIFIED`.
- 원 논문의 식·가정·오차범위가 graphite lag 접목을 지지하는지는
  `CONTENT_UNVERIFIED`.
- 최종 문헌 phase에서 원문을 직접 대조한다.

## Coverage Status

- 이 batch의 4문건, 157행은 `READ`.
- 누적 coverage 반영 후 목표는 234문건, 49,029행이다.
- 전체 Phase 057 잔여 목표는 37문건, 8,766행이다.

## Next

Step 19.8B:
author brief·cherrypick·W1–W3 5문건 388행을 전문 검독한다.
