# Phase Planning Operations Guide

정본일: 2026-05-27
적용 위치: `D:\Projects\Project_Anode_Fit\Codex`

이 문건은 Codex가 `Project_Anode_Fit`에서 계획서를 세우고, 실행하고, 결과를 저장하고, 검수하는 운영 방식을 정리한 지침이다. 기준은 `D:\Projects\RO_SkillDict\5_skill_dictionary`에서 확인한 계획서/phase ledger/result/handover 관례이며, 이 프로젝트의 LaTeX 문건·논문·수식 검독 업무에 맞게 줄여 적용한다.

## 0. AGENTS.md와 이 문건의 분담

`D:\Projects\Project_Anode_Fit\Codex\AGENTS.md`에는 프로젝트 작업 중 항상 지켜야 하는 원칙을 둔다.

- Codex/Claude 작업 경계, 원본 자료 보호, Git 경계.
- 원천 파일 전문 검독, 읽은 범위 기록, 추측 보강 금지.
- `확정`, `근거 미발견`, `추정`, `미검증` 분리 보고.
- 검증하지 않은 내용을 PASS 또는 완료로 보고하지 않는 원칙.
- 변수명, 기호, 라벨, 식 번호, 한글 표현, Chapter/ver 명칭 이력 보존.
- 기존 문건 덮어쓰기 금지와 추가 개선 후보 보고 원칙.

이 운영지침에는 계획서와 phase 산출물을 작성, 실행, 저장, 검수하는 방법을 둔다.

- `Codex\plans`와 `Codex\results` 저장 위치와 파일명 규칙.
- 계획서 section, phase range, cumulative step numbering.
- `plan saved -> execution -> result saved -> validation -> ledger update` 실행 루프.
- phase result 문건 양식, ledger row 양식, gate 설계 원칙.
- audit pass, read coverage, decision queue, `근거 미발견` 기록 방식.
- Anode dQ/dV 문건 전용 검수 항목과 작업 시작 체크리스트.

## 1. 계획서가 필요한 경우

다음 중 하나라도 해당하면 본격 작업 전에 계획서를 먼저 저장한다.

- `.tex`, PDF, 논문, 수식 전개를 실제로 검독하고 재구성하는 작업
- 여러 원천 파일을 대조해야 하는 작업
- Chapter 1~5처럼 phase나 장 구조가 있는 장기 작업
- 피팅 절차, 수치해법, self-consistent equation, integral equation처럼 논리 전개가 복잡한 작업
- 사용자가 `계획서`, `정본`, `검수`, `인계`, `phase`, `장기 작업`을 언급한 작업
- Codex와 Claude 결과를 나중에 비교·통합해야 하는 작업

간단한 상태 확인, 단일 명령 출력, 단순 질문 답변에는 별도 계획서를 만들지 않아도 된다. 다만 사용자가 계획서를 요구하면 반드시 문서로 저장한다.

## 2. 저장 위치와 파일명

운영 지침과 실제 계획서는 `Codex\plans` 아래에 둔다.

- 실제 계획서: `D:\Projects\Project_Anode_Fit\Codex\plans\YYYY-MM-DD-<topic>-plan.md`
- 계획서 companion JSON: `D:\Projects\Project_Anode_Fit\Codex\plans\YYYY-MM-DD-<topic>-plan.json`
- phase 결과 문건: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_<phase-id>_<topic>_RESULT.md`
- phase 결과 companion JSON: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_<phase-id>_<topic>_RESULT.json`
- ledger 또는 execution index: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_<range>_EXECUTION_LEDGER.md`
- handover: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_<phase-id>_<topic>_HANDOVER.md`

파일명에는 반드시 날짜, phase 번호 또는 phase 범위, 주제를 넣는다. 파일 목록만 봐도 작업 순서와 복구 지점을 알 수 있어야 한다.

## 3. 계획서 작성 전 확인 순서

계획서 자체를 쓰기 전에 다음을 먼저 확인한다.

1. 활성 프로젝트와 작업 폴더가 `D:\Projects\Project_Anode_Fit\Codex`인지 확인한다.
2. 사용자가 지정한 원천 파일, 참고 파일, PDF, 이미지, 기존 문건 목록을 확정한다.
3. 각 원천 파일의 경로, 파일 크기, 행 수 또는 페이지 수를 확인한다.
4. 전문 검독이 필요한 파일과 샘플/구조 확인만 필요한 파일을 구분한다.
5. 기존 계획서, phase 결과서, ledger, handover가 있는지 확인한다.
6. 이어받는 작업이면 직전 ledger의 `Next Step`과 마지막 gate를 확인한다.
7. 아직 읽지 않은 범위는 `미검독`으로 표시하고, 추정으로 채우지 않는다.

## 4. 계획서 기본 구조

계획서는 다음 순서를 기본으로 한다.

```markdown
# <Project/Topic> Plan

## Summary

## Current Ground Truth

## Phase Range

## Non-goals

## Implementation Changes

## Phase N — <phase name>

## Implementation Interfaces

## Test Plan

## Assumptions

## Correction History
```

각 section에 들어갈 내용은 다음과 같다.

- `Summary`: 목표, 왜 이 작업을 하는지, 이번 계획이 어디까지 다루는지 쓴다.
- `Current Ground Truth`: 현재 확인된 사실, 원천 파일, 기존 결정, 직전 gate, 미확인 사항을 분리한다.
- `Phase Range`: 모든 phase 번호, 이름, step 범위를 먼저 표로 제시한다.
- `Non-goals`: 이번 작업에서 하지 않을 것, 손대면 안 되는 파일, 사용자 승인 전 금지 사항을 명시한다.
- `Implementation Changes`: 생성/수정할 문서, working copy, 분석 산출물, companion JSON, ledger를 나열한다.
- phase별 본문: 각 phase의 step, 입력, 산출물, gate, 중단 조건, 다음 phase 조건을 쓴다.
- `Implementation Interfaces`: 수식, 데이터 구조, 표 양식, ledger row, 결과 문건 양식 등 실행자가 그대로 따라야 할 인터페이스를 둔다.
- `Test Plan`: LaTeX 빌드, 수식 검수, JSON parse, 문헌 대조, 읽은 범위 대조, 논리 의존성 검수 등 실제 검증 방법을 쓴다.
- `Assumptions`: 아직 확정되지 않았지만 계획 수립을 위해 임시로 둔 가정을 표시한다.
- `Correction History`: 이전 계획에서 무엇을 정정했는지 쓴다.

## 5. Step 번호와 phase 번호

- 하나의 계획서 안에서는 step 번호를 phase마다 1부터 다시 시작하지 않는다.
- Phase A가 Steps 1-12라면 Phase B는 Step 13부터 시작한다.
- 기존 작업을 이어받는 경우 직전 ledger 또는 결과 문건의 `Next Step`을 확인한 뒤 다음 번호부터 시작한다.
- phase 번호, step 범위, 결과 파일명, ledger의 `Plan Steps`가 서로 맞아야 한다.
- 맞지 않으면 phase 완료로 보고하지 말고 먼저 정정 문건이나 ledger correction을 남긴다.

## 6. 실행 루프

기본 실행 루프는 다음 순서다.

```text
plan saved -> execution -> result saved -> validation -> ledger update
```

각 phase는 이 루프를 독립적으로 닫아야 한다.

- `plan saved`: phase plan markdown과 필요 시 JSON을 저장한다.
- `execution`: 계획서의 step 순서대로 수행한다.
- `result saved`: 실제 수행 범위와 결과를 별도 result 문건에 기록한다.
- `validation`: 계획서에서 정의한 gate를 실제 명령, 수식 검수, 문헌 대조, 읽은 범위 대조로 확인한다. 확인하지 못한 항목은 `근거 미발견` 또는 `미검증`으로 남기고 PASS에 포함하지 않는다.
- `ledger update`: phase 상태, gate, result path, machine artifact, next step을 ledger에 반영한다.

## 7. Phase 결과 문건 양식

phase 결과 문건에는 최소한 다음 항목을 둔다.

```markdown
# Phase N — <topic> Result

## Summary

## Step Range

## Inputs

## Files Created

## Files Updated

## Read Coverage

## Execution Evidence

## Validation

## Gate

## Confirmed Non-Changes

## Open Issues / Decision Queue

## Next
```

특히 `Read Coverage`에는 실제 읽은 파일과 행/페이지 범위를 적는다. 전문 검독하지 않은 파일은 `부분 검독` 또는 `미검독`으로 남긴다.
`Open Issues / Decision Queue`에는 `근거 미발견`, 사용자 결정 필요 항목, 다음 phase 전에 확인해야 할 문헌/수식/원천 대조를 분리해서 적는다.

## 8. Ledger row 양식

장기 작업에는 다음 형태의 ledger를 둔다.

```markdown
| Phase/Subphase | Planned Steps | Actual Steps | Block | Purpose | Status | Plan | Result | Machine Artifacts | Validation | Gate | Next Step |
|---|---:|---:|---|---|---|---|---|---|---|---|---:|
| Phase001 | 1-25 | 1-18 | setup | Source inventory and plan baseline | PASS | `plans/...md` | `results/...RESULT.md` | `results/...RESULT.json` | Read coverage PASS; JSON PASS | `PASS_SOURCE_INVENTORY` | 26 |
```

Ledger는 단순 진행표가 아니라 컨텍스트 압축, 세션 교체, Claude/Codex 비교, 나중의 재개를 위한 복구 지점이다.

## 9. Gate 설계 원칙

Gate는 `좋아 보임`이 아니라 확인 가능한 조건이어야 한다.

좋은 Gate 예:

- 지정된 `.tex` 파일 1행부터 끝행까지 읽었고 읽은 범위를 결과서에 기록했다.
- PDF에서 ref. 6, 7의 서지와 본문 사용 위치를 확인했다.
- self-consistent 변수 의존성을 dependency graph로 작성했고 순환 위치를 표시했다.
- Chapter 1에서 Chapter 2로 전달되는 기준식 목록을 원문 식 번호와 함께 대조했다.
- LaTeX 빌드 또는 최소 문법 검사를 실행했고 실패/성공을 기록했다.
- 결과 JSON 또는 ledger JSON이 parse된다.

나쁜 Gate 예:

- 내용이 적절해 보인다.
- 아마 맞다.
- 검색 결과상 문제 없어 보인다.
- 일부 섹션만 읽고 전체 구조를 안다고 가정한다.

## 10. 검수와 audit 방식

큰 작업에서는 세 단계 검수 루프를 쓴다.

1. Pass 1: 가능한 문제를 넓게 찾는다.
2. Pass 2: 발견 항목이 실제 문제인지 확인하고, 확인된 문제만 고친다.
3. Pass 3: 고친 문제가 실제로 해결됐는지 재검증한다.

수정이 필요한 경우:

- 이전 phase 문건은 덮어쓰지 않는다.
- 새 addendum, supersession, correction 문건을 만든다.
- 원천 `.tex`, PDF, Claude 작업물, 외부 임시 폴더 원본은 사용자 승인 없이 수정하지 않는다.

## 11. 이 프로젝트 전용 검수 항목

Anode dQ/dV 문건 작업에서는 다음 항목을 phase gate에 포함한다.

- `V_n`, `V_{n,app}`, `V_{n,drive}`, OCV의 구분이 유지되는가.
- 전하 보존식이 내부 전위를 결정하는 중심식으로 유지되는가.
- `xi_j`, `Q_bg`, `dQ/dV`, `dV/dQ`의 순환 의존성이 어디서 생기는지 표시됐는가.
- 순환 의존성이 implicit formulation인지, 수치해법이 필요한지, 논리 오류인지 분리됐는가.
- ref. 6, 7 방법론을 가져올 때 변수 매핑과 물리 가정 차이를 따로 기록했는가.
- Chapter 1 기준식이 Chapter 2~5 전달식과 충돌하지 않는가.
- `ver.1`~`ver.5`라는 역사적 명칭과 Chapter 1~5라는 새 구조 명칭을 혼동하지 않는가.

## 12. 금지 사항

- 계획서 없이 장기 검독이나 대규모 재작성에 들어가지 않는다.
- 읽지 않은 원문을 읽은 것처럼 보고하지 않는다.
- PDF ref. 6, 7을 확인하지 않고 방법론 반영 완료라고 쓰지 않는다.
- Claude 폴더나 원본 임시 폴더 파일을 사용자 지시 없이 수정하지 않는다.
- 기존 문건을 사용자 승인 없이 덮어쓰지 않는다.
- unresolved decision을 임의로 확정하지 않는다.
- 수식의 부호, 단위, 독립변수, boundary condition을 추측으로 맞추지 않는다.

## 13. 작업 시작 체크리스트

계획서를 쓰기 전 마지막으로 다음을 확인한다.

- [ ] 활성 작업 폴더가 `D:\Projects\Project_Anode_Fit\Codex`인가.
- [ ] 원천 파일 목록이 확정됐는가.
- [ ] 전문 검독 대상과 부분 확인 대상이 분리됐는가.
- [ ] 기존 계획서/ledger/handover 존재 여부를 확인했는가.
- [ ] phase 번호와 step 번호 시작점을 정했는가.
- [ ] 중단 조건과 사용자 결정 경계를 명시했는가.
- [ ] 검증 명령 또는 검수 방법이 실제 실행 가능하게 쓰였는가.
- [ ] 결과 문건과 ledger를 어디에 저장할지 정했는가.

