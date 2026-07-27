# Phase 057 사용자 의도·금지·결정 계보 복원 세부 계획

정본일: 2026-07-28
상위 계획:
`Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`
상위 Steps: 18–25
세부 Steps: 18.1–25.8

## Summary

이 phase는 v1.0.10–v1.0.25.2의 이론을 평가하기 전에,
사용자가 이 프로젝트를 어떤 방향으로 작성하길 원했는지를 원천 기록에서 복원한다.

최신 handover의 요약을 과거 전체의 의도로 간주하지 않는다.
plan, result, handover, change log, ledger, fitting/code guide와 machine JSON을
고유 Git blob 단위로 처음부터 끝까지 검독하고, 실제 commit diff와 연결한다.

문건 안의 주장을 다음 네 주체로 분리한다.

1. `USER_REQUIREMENT`: 사용자가 요구·승인·철회·정정한 사항.
2. `MODEL_PROPOSAL`: Fable, Opus, Claude, Codex 등이 제안한 사항.
3. `REVIEW_FINDING`: 검토 과정에서 발견되거나 주장된 결함.
4. `IMPLEMENTED_STATE`: 실제 파일과 코드 diff에 반영된 상태.

모델이 “사용자 지시”라고 적은 문장도 실제 선후 기록 또는 반복된 후속 승인으로
확인되기 전에는 `USER_REQUIREMENT`로 확정하지 않는다.

## Current Ground Truth

- Phase 055 gate: `PASS_P055_SOURCE_FREEZE`
- Phase 056 gate: `PASS_P056_COMPLETE_MANIFEST`
- 전체 범위: 1,520 paths, 862 unique blobs
- Phase 057의 최초 full-text 후보:
  `.md`, `.json`, `.txt`, `.html` 271 unique blobs, 57,795 lines
- 후보 구성:
  - Markdown 245 blobs / 29,331 lines
  - JSON 21 blobs / 24,030 lines
  - text 3 blobs / 377 lines
  - HTML 2 blobs / 4,057 lines
- 모든 후보의 현재 coverage 상태는 `UNREAD`.

57,795행 전체를 동일한 방식으로 읽지는 않는다.
서술 문건은 문장·표·수식·주석을 연속 행 범위로 전문 검독하고,
machine JSON은 모든 key/value를 순회하되 반복 배열은 schema, 길이,
각 항목 식별자와 값 범위를 별도 기계 검증한다.
어느 경우에도 파일 중간을 건너뛰고 앞뒤로 내용을 추정하지 않는다.

## Outputs

- `Codex/results/PHASE_057_USER_INTENT_READ_QUEUE.json`
- `Codex/results/PHASE_057_USER_INTENT_READ_COVERAGE.json`
- `Codex/results/PHASE_057_USER_INTENT_CONSTITUTION.md`
- `Codex/results/PHASE_057_DECISION_GENEALOGY.json`
- `Codex/results/PHASE_057_CLAIM_EVIDENCE_LEDGER.md`
- `Codex/results/PHASE_057_USER_INTENT_RECOVERY_RESULT.md`
- `Codex/results/ACTIVE_HANDOVER_V1010_V1025_2_REAUDIT.md` 갱신

중간 관찰은
`Codex/work/v1010_v1025_2_reaudit/phase057_notes/`에 저장할 수 있으나,
최종 판정은 result와 genealogy에만 둔다.

## Step 18 — 시간순 read queue 확정

### Step 18.1

Phase 056 coverage에서 `.md`, `.json`, `.txt`, `.html` 고유 blob을 추출한다.

### Step 18.2

각 blob의 모든 version path를 보존하고 최초 등장 version과 최초 등장 commit을 찾는다.

### Step 18.3

각 문건을 다음 category 중 하나로 분류한다.

- `PLAN`
- `HANDOVER`
- `RESULT`
- `EXECUTION_LEDGER`
- `CHANGE_LOG`
- `REFERENCE_LEDGER`
- `FITTING_GUIDE`
- `CODE_GUIDE`
- `DIRECTION_OR_AUDIT`
- `MACHINE_EVIDENCE`
- `OTHER_SUPPORT`

### Step 18.4

서술 문건은 최대 400행의 연속 chunk로 나눈다.
문단·표·수식이 chunk 경계에서 갈리면 범위를 겹쳐 다시 읽되,
coverage 완료 판정은 중복을 제거한 합집합으로 한다.

### Step 18.5

JSON은 전체 key path, 배열 길이, 식별자와 값 범위를 순회하는 검증 항목을 만든다.
사람이 해석해야 하는 문자열 필드는 별도 연속 텍스트 packet으로 만든다.

### Step 18.6

read queue의 파일 수, blob 수, 행 수 합계를 Phase 056 manifest와 대조한다.

## Step 19 — 원천 문건 전문 검독

### Step 19.1

v1.0.10–v1.0.13의 queue를 시간순으로 전문 검독한다.

### Step 19.2

v1.0.14–v1.0.18.2의 queue를 시간순으로 전문 검독한다.

### Step 19.3

v1.0.19의 queue를 시간순으로 전문 검독한다.

### Step 19.4

v1.0.20의 queue를 계획→step log→result→handover 순서로 전문 검독한다.
경쟁 초안과 최종 채택 판단을 분리한다.

### Step 19.5

v1.0.21의 queue를 전문 검독한다.

### Step 19.6

v1.0.22의 queue를 R0부터 최종 handover까지 전문 검독한다.

### Step 19.7

v1.0.23의 queue를 전문 검독한다.

### Step 19.8

v1.0.24–v1.0.25.2의 queue를 전문 검독한다.

### Step 19.9

HTML guide와 machine JSON을 전 범위 검독·순회한다.

### Step 19.10

모든 chunk의 coverage gap과 EOF 도달을 검증한다.

## Step 20 — 작업 주장과 실제 Git diff 대조

### Step 20.1

각 문건 blob의 최초 도입 commit과 후속 수정 commit을 연결한다.

### Step 20.2

commit message가 주장한 변경과 실제 patch의 대상·범위를 비교한다.

### Step 20.3

`완료`, `PASS`, `전건`, `정본`, `무변경`, `코드 정합` 표현을 별도 추출한다.

### Step 20.4

각 완료 주장을 `CONFIRMED`, `OVERCLAIMED`, `PARTIAL`, `UNVERIFIED`로 판정한다.

### Step 20.5

merge, copy-forward, revert 및 후속 수정으로 효력이 달라진 결정을 기록한다.

## Step 21 — 발화 주체와 승인 상태 분리

### Step 21.1

`USER_REQUIREMENT`, `MODEL_PROPOSAL`, `REVIEW_FINDING`, `IMPLEMENTED_STATE`를 분리한다.

### Step 21.2

사용자 요구로 확인되는 항목에 최초 근거와 마지막 재확인 근거를 연결한다.

### Step 21.3

모델 제안이 사용자 승인 없이 구현된 사례를 분리한다.

### Step 21.4

사용자가 문제를 제기했으나 해결 완료 근거가 없는 항목을 `OPEN_USER_CONCERN`으로 둔다.

### Step 21.5

사용자 정정 후 과거 표현이 문건·코드에 남은 stale 항목을 식별한다.

## Step 22 — 방향성 결정 계보 작성

### Step 22.1

프로젝트 목표와 관측 출발점을 복원한다.

### Step 22.2

문건의 독자 수준, 상세도, 장간 연결 및 이론–코드 경계를 복원한다.

### Step 22.3

`q`, 조성 좌표, 전압, 전류, 온도, 충·방전 branch와 미분 규약을 복원한다.

### Step 22.4

전하 보존, 평형, 동역학, 열, 히스테리시스, 재료 혼합의 계층 순서를 복원한다.

### Step 22.5

피팅, 식별성, 데이터 요구량과 검증 조건을 복원한다.

### Step 22.6

각 결정에 `PRESERVE`, `CORRECT`, `SUPERSEDE`, `EMPIRICAL_ONLY`,
`THEORY_ONLY`, `REJECT`, `UNVERIFIED` 중 하나를 부여한다.

## Step 23 — 금지·철회·보류 계보 작성

### Step 23.1

임의 cap, clip, threshold, softplus, 사후 smoothing과 기타 편의 근사를 추적한다.

### Step 23.2

근거 없는 재료 상수·default·host decomposition을 추적한다.

### Step 23.3

평형/동역학, 히스테리시스/분극, 내부전위/관측전압 혼동을 추적한다.

### Step 23.4

충전 해석, 발열, Si mechanics, LCO 도핑 등 시기상 보류됐다가 재도입된 항목을 추적한다.

### Step 23.5

철회된 논리가 후속 문건이나 코드에서 부활했는지 확인한다.

## Step 24 — 충돌 해소와 현재 사용자 방향 헌법

### Step 24.1

같은 주제의 상충 결정을 시간순으로 배열한다.

### Step 24.2

후속 결정이 이전 결정을 완전히 대체했는지, 적용 범위만 좁혔는지 판정한다.

### Step 24.3

사용자 결정과 물리적 사실이 충돌할 가능성이 있으면 둘을 분리해 기록한다.

### Step 24.4

현재 작업의 변경 불가 원칙과 사용자 결정이 필요한 경계를 작성한다.

### Step 24.5

`PHASE_057_USER_INTENT_CONSTITUTION.md`를 작성하되 아직 이론 정본으로 부르지 않는다.

## Step 25 — 검증과 gate

### Step 25.1

271개 고유 문건 후보와 57,795행의 전체 처분을 재검증한다.

### Step 25.2

모든 서술 문건의 line coverage에 gap이 없는지 확인한다.

### Step 25.3

모든 JSON의 key/value traversal 및 schema 검증 완료를 확인한다.

### Step 25.4

각 사용자 방향 결정에 원천 path, line, commit 중 최소 두 종류의 근거가 있는지 검사한다.

### Step 25.5

모델 제안을 사용자 요구로 잘못 승격한 항목이 없는지 적대 재검토한다.

### Step 25.6

잠정 사용자 방향성 11개를 최종 재판정한다.

### Step 25.7

result, genealogy, evidence ledger와 ACTIVE_HANDOVER를 저장한다.

### Step 25.8

`PASS_P057_INTENT_RECOVERY`, `CONDITIONAL_P057`, `FAIL_P057` 중 하나를 판정한다.

## Evidence Record

각 claim은 최소한 다음 구조를 사용한다.

```json
{
  "claim_id": "INTENT-0001",
  "topic": "document-code-boundary",
  "actor": "USER_REQUIREMENT",
  "statement": "...",
  "first_evidence": {
    "path": "...",
    "lines": [1, 10],
    "commit": "..."
  },
  "later_evidence": [],
  "conflicts": [],
  "current_status": "PRESERVE",
  "confidence": "CONFIRMED"
}
```

## Gate

`PASS_P057_INTENT_RECOVERY`는 다음이 모두 충족될 때만 부여한다.

- 271개 기준 고유 문건 후보가 모두 처분됨.
- line/key coverage gap이 없음.
- 사용자 요구와 모델 제안이 분리됨.
- 과거 `PASS` 주장이 실제 diff 및 산출물과 대조됨.
- 철회·금지·보류 항목의 후속 부활 여부가 확인됨.
- 현재 방향 헌법의 각 항목이 원천 근거와 연결됨.
- 근거가 없는 기억 기반 항목이 확정 목록에 없음.

## Stop Conditions

- manifest와 실제 Git tree가 달라짐.
- 파일 중간 범위를 읽을 수 없거나 decoding할 수 없음.
- commit history가 shallow하여 최초 도입 근거를 찾을 수 없음.
- 외부 원천이 필요한 결정을 내부 기록만으로 확정해야 하는 상황.
- 기존 원천 파일에 의도하지 않은 변경이 발견됨.

중단 시 추정으로 채우지 않고 `BLOCKED`와 정확한 미완료 범위를 기록한다.
