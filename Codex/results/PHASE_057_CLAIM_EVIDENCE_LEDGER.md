# Phase 057 claim–evidence ledger

정본일: 2026-07-28  
Gate: `PASS_P057_INTENT_RECOVERY`

## Canonical evidence chain

| Layer | Canonical artifact | Count / role |
|---|---|---|
| Source queue | `PHASE_057_USER_INTENT_READ_QUEUE.json` | 271 documents, 57,795 lines, 341 chunks |
| Read coverage | `PHASE_057_USER_INTENT_READ_COVERAGE.json` | 271/271 READ, 57,795/57,795 lines |
| Git document genealogy | `PHASE_057_GIT_DOCUMENT_GENEALOGY.json` | 271 blobs, 406 paths, 673 events |
| Commit claim matrix | `PHASE_057_COMMIT_CLAIM_MATRIX.json` | 229 commits, 2,381 changed-file events |
| Completion candidates | `PHASE_057_COMPLETION_AUTHORITY_CLAIMS.json` | 3,487 candidate locations |
| Completion adjudication | `PHASE_057_COMPLETION_CLAIM_ADJUDICATION.json` | 3,487/3,487 disposed |
| Decision effectivity | `PHASE_057_DECISION_EFFECTIVITY_TIMELINE.json` | copy-forward, withdrawal, active states |
| Provisional findings | `PHASE_057_PROVISIONAL_FINDING_LEDGER.json` | INTENT-PROV-0001–0404 |
| Current user direction | `PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md` | 17 direct-current directions |
| Decision genealogy | `PHASE_057_DECISION_GENEALOGY.json` | 22 decisions, 72 evidence links |
| Rejection/deferment | `PHASE_057_REJECTION_DEFERMENT_GENEALOGY.json` | 20 entries, 118 references |
| Constitution | `PHASE_057_USER_INTENT_CONSTITUTION.md` | audit constitution, not theory canon |
| Final validator | `PHASE_057_INTENT_RECOVERY_VALIDATION.json` | 30/30 checks PASS |

## Evidence authority order

1. current direct user instruction
2. original source path/blob and actual Git patch
3. independently rerun machine evidence
4. repository-reported user direction with repeated later corroboration
5. model proposal or review finding
6. result/handover/commit subject self-report

낮은 등급의 evidence가 높은 등급과 충돌하면 높은 등급을 우선하되,
과거 기록은 삭제하지 않고 superseded 상태로 남긴다.

## Completion claim disposition

- non-positive context: 407
- positive assertions: 3,080
  - `CONFIRMED`: 3
  - `OVERCLAIMED`: 4
  - `PARTIAL`: 961
  - `UNVERIFIED`: 2,112

세 `CONFIRMED` 위치는 모두 v1.0.25.2가 최신 기준선이라는 같은 사실을
반복한다. 이를 세 개의 독립 검증으로 세지 않는다.

## Phase boundary

Phase 057은 사용자 방향과 과거 결정의 권위·효력을 복원했다.
각 버전의 이론식, code behavior, PDF/image와 fit의 물리적 옳고 그름은
Phase 058–067에서 독립 검증한다. 따라서 이 ledger의 `PRESERVE`는
과거 구현을 그대로 채택한다는 뜻이 아니다.
