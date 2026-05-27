# Project_Anode_Fit — Claude 측 프로젝트 한정 지침

> 본 파일은 글로벌 `~/.claude/CLAUDE.md` 의 "프로젝트 진입 시 우선 정독" 대상.
> Codex 측 거울 = `Codex/AGENTS.md` (양 모델 작동 정합).
> 글로벌 지침과 메모리는 본 프로젝트 한정 조항에 우선해 적용한다.

---

## P1. 프로젝트 목표

리튬이온전지 흑연 음극의 ICA (dQ/dV) · DVA (dV/dQ) 를 **열역학적 / 동역학적** 으로 설명하고 피팅 가능한 문건 및 방법론으로 정리한다.

현재 구조:
- 기존 `Claude/docs/graphite_ica_dynamic_ver5.tex` 안의 `ver.1` ~ `ver.5` 적층 구조를 **Chapter 1 ~ Chapter 5** 구조로 재해석.
- **Chapter 1** = `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` 의 **전하 보존식 기반 내부 전위 결정 흐름** 을 기준으로 재구성.
- Chapter 1 의 self-consistent 되먹임 변수 문제는 **사용자 본인 논문 JCP 147 (14) 144111 (2017)** 의 **ref. 6, 7** 방법론을 **실제 확인한 뒤** 반영.
- Chapter 2 ~ 5 는 Chapter 1 기준식 확정 후 발열 · 반응속도론 · 통합 상태방정식 · 히스테리시스 계층으로 적층.

## P2. 작업 경계 (Claude · Codex 병행)

- 활성 프로젝트 = `D:\Projects\Project_Anode_Fit`
- Claude 기본 작업 위치 = `D:\Projects\Project_Anode_Fit\Claude`
- Codex 작업 영역 = `D:\Projects\Project_Anode_Fit\Codex` — **사용자가 명시 안 하면 read 도 write 도 하지 말 것**
  - 예외: 사용자가 명시적으로 read 요청한 Codex 측 **운용 지침 문건** (`Codex/AGENTS.md`, `Codex/plans/phase_planning_operations_guide.md` 등) 은 read OK. **산출물 (tex 디벨롭 결과 등) 은 read 금지** — 양 모델 독립 산출물 비교 무결성 보존.
- 사용자 원천 자료 (임시저장소 폴더, `_local_only/` 의 PDF·사진) 는 **분석 원천으로만**. 사용자가 명시 안 하면 원본 덮어쓰기 X.
- Claude 계획서 = `Claude/plans/YYYY-MM-DD-<topic>-plan.md` ([[feedback_plan_template_11sections]] 양식)
- Claude 산출물·phase 결과·ledger·handover = `Claude/results/` ([[feedback_phase_execution_loop]] 양식)
- 보조 작업 파일 = `Claude/work/` (필요 시 신설)

## P3. 본 프로젝트 전용 검수 7 항목

LaTeX 문건 작업 phase gate 에 다음 항목을 포함한다 ([[feedback_gate_design_principle]] 의 좋은 Gate 양식으로 작성):

1. `V_n`, `V_{n,app}`, `V_{n,drive}`, `V_{n,OCV}` 의 구분이 본문 전체에서 일관되게 유지되는가
2. 전하 보존식이 **내부 전위를 결정하는 중심식** 으로 유지되는가 (단순히 OCV 에서 읽는 흐름으로 회귀 X)
3. `xi_j`, `Q_bg`, `dQ/dV`, `dV/dQ` 의 순환 의존성 (self-consistent loop) 이 **어느 식·어느 변수** 에서 생기는지 dependency graph 또는 표로 표시됐는가
4. 위 순환 의존성이 **`정의상 implicit formulation` / `수치해법 필요` / `논리 공백` / `물리 가정 충돌`** 4 분류 중 무엇인지 분리 진단됐는가
5. ref. 6, 7 방법론을 가져올 때 다음 4 항목이 별도 sub-section 으로 기록됐는가:
   - ref. 의 정확한 서지 정보
   - 사용자 논문 본문에서 ref. 가 쓰인 위치 (page · paragraph)
   - 원 방법론의 수학적 구조
   - 본 graphite dQ/dV 문제에 대응되는 변수 매핑
   - 그대로 가져오면 안 되는 **물리적 가정 차이**
6. Chapter 1 기준식이 Chapter 2 ~ 5 전달식 (`ver.N 으로 전달되는 기준식` 절) 과 충돌하지 않는가
7. `ver.1` ~ `ver.5` 라는 **역사적 명칭** 과 `Chapter 1` ~ `Chapter 5` 라는 **새 구조 명칭** 을 혼동하지 않는가 (작업 보고에서 둘 다 쓸 때 명시적으로 매핑)

## P4. 본 프로젝트 시작 체크리스트 (계획서 작성 전)

매 phase 계획서 작성 전 다음 확인:

- [ ] 활성 작업 폴더가 `D:\Projects\Project_Anode_Fit\Claude` 인가
- [ ] 원천 파일 목록 (이번 phase 에서 read 할 파일) 이 확정됐는가
- [ ] 전문 검독 대상 vs 부분 확인 대상이 분리됐는가
- [ ] 기존 계획서 (`Claude/plans/`) / ledger (`Claude/results/PHASE_*_EXECUTION_LEDGER.md`) / handover 존재 여부 확인했는가
- [ ] cumulative step 번호 시작점을 정했는가 (이전 ledger 의 `Next Step` 참조)
- [ ] 중단 조건 + 사용자 결정 경계 명시했는가
- [ ] 검증 명령 또는 검수 방법이 실제 실행 가능하게 쓰였는가
- [ ] 결과 문건과 ledger 저장 위치 정했는가

## P5. 이름 · 구조 보존 (본 프로젝트 한정)

- 기존 변수명 · 함수명 · 기호 · 라벨 · 식 번호 · 한글 표현은 사용자가 바꾸라고 하지 않으면 **임의 변경 X** ([[feedback_user_code_conventions]] 본 프로젝트 적용)
- `ver.1` ~ `ver.5` 는 기존 파일명 · 본문 이력으로 남아 있음 → **새 구조 제안에서는 Chapter 1 ~ Chapter 5 로 재해석**
- 단 본문에 등장하는 `ver.N으로 전달되는 기준식` 등 절 제목은 그대로 보존 (역사적 인계 chain 표시)
- Chapter 1 기준식이 확정되기 전에는 Chapter 2 ~ 5 의 전달식 정합성을 **완료** 로 보고 X
- 추가 개선 후보는 **실제 수정하지 말고** `추가 후보` 로 보고

## 관련 글로벌 메모리 (자동 적용)

본 프로젝트는 다음 글로벌 메모리를 그대로 따른다. `_claude/memory/` 에 사본 존재.

- [[feedback_session_start_protocol]] · [[feedback_full_file_read_required]] · [[feedback_planning_vs_execution]]
- [[feedback_project_layout_claude_subfolders]] (Claude/plans + Claude/results)
- [[feedback_plan_template_11sections]] (계획서 11 sections 양식)
- [[feedback_phase_execution_loop]] (5단계 루프 + Result 11항목 + Ledger 12 컬럼)
- [[feedback_gate_design_principle]] (확인 가능한 조건 의무)
- [[feedback_phase_audit_workflow]] (10차원 × 3-Pass)
- [[feedback_confirmed_items_policy]] (보고 4-tier)
- [[feedback_document_protection_addendum_pattern]] (결과 문건 보호)
- [[feedback_decision_request_clarity]] · [[feedback_interaction_style]]

## Codex 측 거울 (참고)

- `Codex/AGENTS.md` — Codex 가 항상 지키는 원칙 (본 P1~P5 와 정합)
- `Codex/plans/phase_planning_operations_guide.md` — Codex 의 계획서·실행·검수 운영지침 (글로벌 메모리 G2~G10 과 정합)

양 문건은 Codex 운용용이며 Claude 가 직접 따를 필요는 없다. **운용 방식 (계획서 양식 · 실행 루프 · gate · result 양식 등) 은 본 CLAUDE.md + 글로벌 메모리로 동일 수준 유지** — Claude · Codex 산출물이 동등 양식으로 비교 가능해야 한다는 5-27 사용자 의도 반영.
