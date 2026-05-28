# Project_Anode_Fit Codex 작업 지침

정본일: 2026-05-27

이 문서는 `D:\Projects\Project_Anode_Fit\Codex`에서 Codex가 작업할 때 적용하는 프로젝트 로컬 정본이다. 상위 전역 지침과 함께 적용하되, 이 파일은 Codex 전용 작업 폴더의 경계와 기록 방식을 정한다.

## 1. 활성 프로젝트와 작업 경계

- 활성 프로젝트는 `D:\Projects\Project_Anode_Fit`이다.
- Codex의 기본 작업 위치는 `D:\Projects\Project_Anode_Fit\Codex`이다.
- Claude 병행 작업 영역인 `D:\Projects\Project_Anode_Fit\Claude`는 사용자가 명시하지 않으면 수정하지 않는다.
- 사용자 원천 자료가 있는 임시 다운로드 폴더와 `_local_only` 성격의 PDF/사진 자료는 분석 원천으로만 다루고, 사용자가 명시하지 않으면 원본을 덮어쓰지 않는다.
- Codex 계획서는 `Codex\plans` 아래에 두고, 산출물·phase 결과·검수 결과·ledger·handover는 `Codex\results` 아래에 둔다. 보조 작업 파일은 필요 시 `Codex\work` 아래에 둔다.

## 2. 현재 프로젝트 목표

- 목표는 리튬이온전지 흑연 음극의 ICA(dQ/dV)와 DVA(dV/dQ)를 열역학적/동역학적으로 설명하고 피팅 가능한 문건 및 방법론으로 정리하는 것이다.
- 현재 큰 방향은 기존 `graphite_ica_dynamic_ver5.tex` 안의 ver.1~ver.5 적층 구조를 Chapter 1~5 구조로 재해석하는 것이다.
- Chapter 1은 `graphite_ica_charge_balance_ver1_rechecked2.tex`의 전하 보존식 기반 내부 전위 결정 흐름을 기준으로 재구성한다.
- Chapter 1에 남은 self-consistent 되먹임 변수 문제는 사용자의 JCP 147(14) 144111 (2017) 논문 및 그 논문의 ref. 6, 7 방법론을 실제 확인한 뒤 반영한다.
- Chapter 2~5는 Chapter 1의 기준식이 확정된 뒤 발열, 반응속도론, 통합 상태방정식, 히스테리시스 계층으로 적층한다.

## 3. 작업 시작 절차

1. 사용자 지시가 조사, 계획, 문건 검독, LaTeX 수정, 수식 검증, 피팅 알고리즘 설계 중 무엇인지 먼저 확정한다.
2. 작업 대상 파일과 읽을 원천 파일 목록을 먼저 확정한다.
3. 이어받는 작업이면 `Codex\results`의 직전 result, ledger, handover를 먼저 열어 이전 결정, 실제 완료 범위, 미검증 항목, 다음 단계 조건을 확인한다.
4. 사용자가 명시한 `.tex`, PDF, 문건은 처음부터 끝까지 실제로 읽는다. 긴 파일은 행 또는 페이지 범위를 나누고 읽은 범위를 기록한다.
5. 섹션 검색, `rg`, 일부 샘플, 빌드 성공만으로 전문 검독을 대체하지 않는다.
6. 판단 보고 시 `확정`, `근거 미발견`, `추정`, `미검증`을 분리한다.
7. 수식이나 물리적 가정은 원천 파일의 어느 절/식/문장에 근거하는지 남긴다.

## 4. 계획서와 페이즈 기록 운영

- 사용자가 `계획서`라고 말하면 단순 체크리스트가 아니라 실행 기준 문서를 뜻한다.
- 새 계획서는 본격 작업 전에 먼저 저장한다. 대화로만 계획을 말하고 장기 작업을 시작하지 않는다.
- 계획서는 기본적으로 `Codex\plans\YYYY-MM-DD-<topic>-plan.md`에 저장한다.
- 구조화된 실행 메타데이터가 필요하면 같은 이름의 `.json` companion을 함께 둔다.
- phase 결과 문건은 `Codex\results\PHASE_<phase-id>_<topic>_RESULT.md` 형태를 우선 사용한다.
- 장기 작업에는 phase ledger 또는 execution index를 유지한다. ledger에는 최소한 `Phase`, `Plan Steps`, `Status`, `Canonical Report`, `Machine Artifact`, `Gate Result`, `Next Step`에 해당하는 항목을 둔다.
- 계획서의 phase와 step은 최대 한계나 고정 족쇄가 아니라 `최소 수행 기준선`이다. 작업 중 논리 검증, 원천 대조, 수식 전개, 문헌 확인이 더 필요하다고 판단되면 phase, subphase, step, audit pass, repair loop를 추가할 수 있다.
- phase/step을 추가한 경우에는 원래 계획의 어느 phase 뒤에 왜 추가했는지, 추가 산출물 경로, 새 gate, 다음 step을 ledger와 해당 result 문건에 기록한다.
- 기존 계획서, 결과서, handover는 사용자가 명시하지 않으면 덮어쓰지 않는다. 정정은 새 addendum, supersession, correction 문건으로 남긴다.
- handover를 만들 때는 상단에 이전 plan, result, ledger, handover chain을 누적 기록한다. 각 항목에는 경로, phase 또는 step 범위, gate 상태, 다음 단계 조건을 함께 남긴다.
- 작업 재개 시 `지난 세션이 했다`가 아니라 저장된 원문 기록을 직접 확인한 범위만 근거로 삼는다. 확인하지 못한 항목은 `근거 미발견` 또는 `미검증`으로 남긴다.
- 컨텍스트 압축, 세션 재개, 모델 교체, 긴 작업 중단 이후에는 기억이나 요약만으로 이어가지 않는다. 활성 계획서를 먼저 열고, 그 계획서의 phase/result/ledger 경로를 따라 필요한 과거 phase 문건을 직접 확인한 뒤 작업한다.
- phase 결과 문건을 저장하는 이유는 사용자 보고용만이 아니다. 컴팩션 이후 훼손된 기억이나 불완전한 요약에 의존해 환각성 판단을 하지 않도록, 다음 작업자가 원문 기록을 다시 열어 정확히 이어가기 위한 복구 지점이다.
- 컴팩션 이후 특정 판단, 수식, 읽은 범위, gate 결과가 필요하면 해당 phase result와 ledger를 찾아 직접 확인한다. 확인하지 않은 내용을 과거에 완료된 사실처럼 취급하지 않는다.

## 5. 계획서 기본 형식

계획서는 가능한 한 다음 순서를 따른다.

1. 제목
2. `Summary`
3. `Current Ground Truth` 또는 baseline
4. `Phase Range`
5. `Non-goals` 또는 scope guard
6. `Implementation Changes` 또는 생성/수정 파일 목록
7. phase별 세부 section
8. `Implementation Interfaces` 또는 문건/수식/데이터 구조 예시
9. `Test Plan` 또는 검증 계획
10. `Assumptions`
11. 필요 시 `Correction History`

추가 규칙:

- `Phase Range`에는 포함되는 phase 번호, phase 이름, step 범위를 먼저 나열한다.
- phase 본문은 `## Phase N — <phase name>` 형식을 우선 사용한다.
- step 번호는 phase마다 1부터 다시 시작하지 않는다. 하나의 계획 안에서는 전체 phase를 관통해 단조 증가시킨다.
- 각 phase에는 산출물, Gate, 중단 조건, 다음 phase 진입 조건을 둔다.
- 계획서에는 목표, 배경, 적용 범위, 읽을 원천 파일, 생성/수정할 파일, 단계별 작업, 검증 게이트, 사용자 결정 경계, 금지 사항을 빠짐없이 쓴다.

## 6. 실행과 검수 루프

기본 루프는 다음 순서다.

1. plan saved
2. execution
3. result saved
4. validation
5. ledger update

phase 결과 문건에는 다음을 남긴다.

- 실제 입력 파일
- 실제 읽은 범위
- 생성/수정 파일
- 실행 명령
- 검증 결과
- 확정된 판단
- `근거 미발견`과 미해결 사항
- decision queue
- 다음 phase 진입 조건

검수 원칙:

- 검증하지 않은 내용을 PASS로 쓰지 않는다.
- 수식 전개는 차원, 부호, 독립변수, implicit/self-consistent 의존성, 피팅 식별성을 따로 검수한다.
- PDF ref. 6, 7 방법론은 실제 서지와 본문 맥락을 확인하기 전에는 반영 완료로 보고하지 않는다.
- 되먹임 적분식 문제는 `정의상 implicit system`, `수치해법 필요`, `논리 공백`, `물리 가정 충돌` 중 무엇인지 분리한다.
- long-running 작업은 phase boundary마다 결과서와 handover를 만든다.

## 7. 문헌과 수식 취급

- 논문, PDF, LaTeX 원천은 추측으로 보강하지 않는다.
- 외부 논문이나 공식 문헌이 필요한 경우 DOI, 논문 링크, 공식 문서 링크를 함께 기록한다.
- 사용자의 논문에서 ref. 6, 7을 가져올 때는 다음을 분리한다.
  - 해당 ref.의 정확한 서지 정보
  - 사용자 논문 본문에서 그 ref.가 쓰인 위치
  - 원 방법론의 수학적 구조
  - 현재 graphite dQ/dV 문제에 대응되는 변수 매핑
  - 그대로 가져오면 안 되는 물리적 가정
- 수식은 LaTeX 깨짐, 기호 중복, 독립변수 혼동, 단위 불일치를 검수한 뒤 보고한다.
- PDF나 이미지 기반 자료에서 OCR이 필요한 경우 OCR 텍스트만 신뢰하지 않는다. 원문 이미지, 수식 의미, 변수 대응, 단위, 그림/표 캡션, 본문 맥락을 함께 대조한다.
- OCR로 추출한 식이나 표는 `확정`, `판독 불확실`, `근거 미발견`을 분리하고, 판독 불확실한 기호를 추정으로 보정하지 않는다.

## 8. 이름과 구조 보존

- 기존 변수명, 함수명, 기호, 라벨, 식 번호, 한글 표현은 사용자가 바꾸라고 하지 않으면 임의 변경하지 않는다.
- `ver.1`~`ver.5`는 기존 파일명/본문 이력으로 남아 있을 수 있지만, 새 구조 제안에서는 Chapter 1~5로 재해석한다.
- Chapter 1 기준식이 확정되기 전에는 Chapter 2~5의 전달식 정합성을 완료로 보고하지 않는다.
- 추가 개선 후보는 실제 수정하지 말고 `추가 후보`로 보고한다.
- LaTeX 본문에는 작업 날짜, phase, step, audit, commit hash 같은 단순 변경 이력을 넣지 않는다.
- 문건 본문에는 논문 내용, 수식 의미, 독자가 이해해야 할 해석만 남긴다. 작업 이력과 검수 판단은 `Codex\results`의 result, ledger, audit, handover에 기록한다.

## 9. Git과 병행 작업

- Claude 작업 영역과 Codex 작업 영역의 산출물을 섞지 않는다.
- 서브 에이전트나 병렬 검수는 역할, 읽을 파일/범위, 금지 사항, 보고 형식을 명확히 지정한 경우에만 완료 처리한다.
- 서브 에이전트 결과는 Codex가 최종 통합한다. 서로 충돌하는 판단, 미확인 근거, 범위 밖 제안은 단순 병합하지 말고 `확정`, `미결`, `근거 미발견`, `추가 후보`로 분류한다.
- 서브 에이전트는 Claude 폴더, 원본 임시 폴더, 사용자 논문/PDF 원본, 기존 결과 문건을 사용자 지시 없이 수정하지 않는다.
- 사용자가 명시하지 않으면 push, merge, Claude 폴더 수정은 하지 않는다.
- Codex 폴더 내 변경도 사용자가 commit을 요청하기 전에는 자동 commit하지 않는다.
- 변경 전후에는 가능하면 `git status`로 범위를 확인하되, 사용자나 Claude가 만든 변경을 되돌리지 않는다.

## 10. 참고한 운영 관례

이 지침은 `D:\Projects\RO_SkillDict\5_skill_dictionary`의 운영 방식을 참고해 만들었다. 확인한 대표 문건은 다음과 같다.

- `D:\Projects\RO_SkillDict\AGENTS.md`
- `D:\Projects\RO_SkillDict\docs\codex_plans\2026-05-16-modern-kro-effect-system-plan-v3-canonical.md`
- `D:\Projects\RO_SkillDict\docs\codex_plans\2026-05-19-modern-kro-effect-system-foundation-first-master-roadmap.md`
- `D:\Projects\RO_SkillDict\docs\PHASE_EXT5D_PHASE161_180_SOURCE_REVIEW_EXECUTION_LEDGER.md`
- `D:\Projects\RO_SkillDict\docs\PHASE_EXT5D_PHASE162_PACKAGE003_SOURCE_REVIEW_OBSERVATIONS_PLAN.md`
- `D:\Projects\RO_SkillDict\docs\PHASE_EXT5D_PHASE162_PACKAGE003_SOURCE_REVIEW_OBSERVATIONS_RESULT.md`
- `D:\Projects\RO_SkillDict\docs\PHASE_EXT5D_PHASE180_PRE_RUNTIME_HANDOVER.md`
- `D:\Projects\RO_SkillDict\docs\PHASE_EXT5E_PHASE184_187_POST_REAUDIT_PLAN.md`
- `D:\Projects\RO_SkillDict\docs\PHASE_EXT5E_PHASE186_POST_REAUDIT_PASS3_REPAIR_VERIFICATION_PLAN.md`
- `D:\Projects\RO_SkillDict\docs\PHASE_EXT5E_PHASE186_POST_REAUDIT_PASS3_REPAIR_VERIFICATION_RESULT.md`
- `D:\Projects\RO_SkillDict\docs\PHASE_EXT5E_PHASE188_200_DECISION_EVIDENCE_LEDGER.md`
- `D:\Projects\RO_SkillDict\docs\PHASE_EXT5E_PHASE194_VALIDATOR_TDD_PREPARATION_PLAN.md`
- `D:\Projects\RO_SkillDict\docs\PHASE_EXT5E_PHASE194_VALIDATOR_TDD_PREPARATION_RESULT.md`

## 11. AGENTS와 운영지침의 분담

`AGENTS.md`에는 프로젝트 작업 중 항상 지켜야 하는 원칙을 둔다.

- Codex와 Claude의 작업 경계, 원본 임시 폴더와 사용자 논문/PDF 보호 원칙.
- 원천 `.tex`, PDF, 논문, 문건의 전문 검독 원칙과 읽은 범위 기록 의무.
- 세션 시작/재개/인계 시 `Codex\results`의 원문 기록을 직접 확인한 뒤 이어가는 원칙.
- 판단 보고 시 `확정`, `근거 미발견`, `추정`, `미검증`을 분리하는 원칙.
- 검증하지 않은 내용을 PASS 또는 완료로 보고하지 않는 원칙.
- 기존 변수명, 기호, 라벨, 식 번호, 한글 표현, Chapter/ver 명칭 이력을 임의 변경하지 않는 원칙.
- LaTeX 본문에 단순 작업 이력과 phase 라벨을 인라인으로 남기지 않는 원칙.
- 서브 에이전트와 병렬 검수의 역할, 범위, 금지 사항, 최종 통합 책임 원칙.
- PDF/이미지 OCR 판독 시 수식 의미와 본문 맥락까지 대조하는 프로젝트 전용 원칙.
- 사용자 승인 없이 기존 문건, Claude 작업물, 원본 자료를 덮어쓰지 않는 원칙.
- 추가 개선 후보는 실제 수정하지 않고 `추가 후보`로 보고하는 원칙.
- Git, commit, push, merge, 병행 작업 폴더 수정 경계.

`Codex\plans\phase_planning_operations_guide.md`에는 계획서와 phase 산출물을 어떻게 작성, 실행, 저장, 검수할지에 관한 절차를 둔다.

- `Codex\plans`와 `Codex\results` 저장 위치와 파일명 규칙.
- 계획서 기본 section, phase range, cumulative step numbering.
- `plan saved -> execution -> result saved -> validation -> ledger update` 실행 루프.
- phase result 문건, ledger row, gate, audit pass 양식.
- 읽은 범위, `근거 미발견`, decision queue, 검증 evidence를 결과 문건에 남기는 방법.
- Anode dQ/dV 문건 전용 gate 항목과 작업 시작 체크리스트.

