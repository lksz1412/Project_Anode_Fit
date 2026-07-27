# Phase 057 사용자 의도·금지·결정 계보 복원 최종 결과

정본일: 2026-07-28  
기준 commit: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`  
대상: v1.0.10–v1.0.25.2

## 최종 판정

`PASS_P057_INTENT_RECOVERY`

Phase 057의 30개 최종 검증 항목이 모두 통과했다.
이 PASS는 사용자 방향 복원이 완료됐다는 뜻이며,
v1.0.10–v1.0.25.2의 물리·코드가 과학적으로 모두 옳다는 뜻은 아니다.

## 완결성

- full-text queue: 271/271 unique documents
- physical lines: 57,795/57,795
- contiguous chunks: 341/341
- occurrence paths: 406
- Git path events: 673
- commits: 229
- full patch file events: 2,381
- provisional findings: 404/404, ID gap 0
- completion/authority candidates: 3,487/3,487 disposed
- canonical decisions: 22
- decision evidence links: 72 path+line+commit
- rejection/deferment entries: 20
- current direct user directions: 17
- final machine checks: 30/30

## 잠정 방향 11개 재판정

| ID | 잠정 방향 | 최종 판정 | 연결 결정 |
|---|---|---|---|
| 1 | 이론 문건은 물리·화학 이론서 | 확정 | DEC-005–007 |
| 2 | 코드 언급은 theory 밖 구현 계약에만 | 확정 | DEC-007 |
| 3 | code는 채택 theory를 전부 반영 | 확정 | DEC-008, 022 |
| 4 | q·조성·내부전위·관측전압 분리 | 확정 | DEC-010 |
| 5 | 전하 보존과 내부전위가 ICA/DVA 중심 | 확정 | DEC-011 |
| 6 | 저온·유한전류 peak 변화를 물리 계층별 분해 | 확정 | DEC-013, 015 |
| 7 | 전류를 근거 없는 독립 barrier 변수로 넣지 않음 | 확정 | DEC-014 |
| 8 | arbitrary cap/clip/softplus/threshold 금지 | 확정 | DEC-021 |
| 9 | fit 성공과 phase/material identification 분리 | 확정 | DEC-018, 019 |
| 10 | 미식별 재료 수치를 default로 승격하지 않음 | 확정 | DEC-012, 017 |
| 11 | v1.0.26을 과학 권위로 사용하지 않음 | 확정 | DEC-002 |

모든 항목은 현재 사용자의 직접 재확인과 repository evidence에 연결됐다.

## 복원된 가장 중요한 방향

1. theory manuscript는 physics/chemistry only다.
2. 구현 추적성은 별도 companion에서 유지한다.
3. authority는 theory → implementation contract → code다.
4. 실제 fitting 성공분은 버리지 않지만 물리적 지위를 과장하지 않는다.
5. 최종 model은 material free energy → kinetics/transport →
   observation의 연결 계층이어야 한다.
6. 저온·유한전류 peak lowering/broadening과 T–I–U barrier가
   최상위 acceptance 현상이다.
7. doped high-voltage LCO, graphite, Si, blend의 공개
   multi-temperature/multi-rate validation이 필수다.
8. arbitrary numerical guard와 data-free default는 금지한다.
9. legacy regression, conformance와 physical validity를 분리한다.
10. phase plan, step history, ledger, handover, commit/push로
    compaction 이후에도 복구 가능하게 한다.

## 과거 계보에서 확정된 경고

- 7-gallery default는 온도 의존을 소거해 철회됐다.
- gate가 legacy를 먼저 복원해 결함 default를 보지 못했다.
- v1.0.25.2의 최종 default는 legacy4이고 skew7은 opt-in이다.
- skew α는 면적을 보존하지만 center, width, susceptibility,
  entropy를 보존하지 않는다.
- regsol equilibrium code 삭제 뒤 Ω 역할이 단절됐다.
- C-rate 3,600배, blend normalization과 capacity denominator가
  code-audit blocker다.
- doc–code 30/30은 같은 물리 오류의 양쪽 복제를 배제하지 못한다.
- protocol/specimen confounding과 naive BIC는 외부 validation이 아니다.
- theory lineage에 code token과 code map이 남아 있다.
- doped high-voltage LCO와 핵심 다온도·다전류 현상은 아직 검증되지 않았다.

## JSON 예외 처분

21개 `.json` 문건 중 20개는 scalar/key traversal을 완료했다.
`snapshot_v1024_R0.json`은 JSON이 아니라 37-byte plain-text pointer다.
이를 실패를 숨기지 않고 `MISLABELED_POINTER`로 처분했다.

## 정본 산출물

- 사용자 방향 헌법:
  `Codex/results/PHASE_057_USER_INTENT_CONSTITUTION.md`
- 방향 결정 계보:
  `Codex/results/PHASE_057_DECISION_GENEALOGY.json`
- 폐기·보류 계보:
  `Codex/results/PHASE_057_REJECTION_DEFERMENT_GENEALOGY.json`
- claim–evidence ledger:
  `Codex/results/PHASE_057_CLAIM_EVIDENCE_LEDGER.md`
- 최종 validation:
  `Codex/results/PHASE_057_INTENT_RECOVERY_VALIDATION.json`

## 다음 phase

Phase 058은 v1.0.10–v1.0.13의 이론 `.tex`, code, tests,
PDF와 images를 이 헌법과 독립 물리 검산으로 재감사한다.
Phase 058 착수 전에 별도 detailed plan을 저장한다.

새 이론 본문과 production code는 아직 작성하지 않는다.
