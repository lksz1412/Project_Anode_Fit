# Anode Fit — Situational Assessment Plan

작성일: 2026-05-27
작성자: Claude (Project_Anode_Fit Claude 측)
양식: [[feedback_plan_template_11sections]] (Codex `Codex/plans/phase_planning_operations_guide.md §4` 와 정합)

## Summary

ver5 마스터 (5-chapter 통합본) + ver1_rechecked2 (Chapter 1 재작성판) + 사용자 본인 JCP 2017 논문 (ref. 6, 7 적분식 해법) 세 축을 통합해 다음 3가지를 확정한다.

1. ver5 의 Chapter 1 ~ Chapter 5 구조 의도 파악 (ver.1 ~ ver.5 의 사실상 Chapter 명 재해석)
2. ver1_rechecked2 의 self-consistent 되먹임 변수가 정확히 어느 식·어느 변수에서 발생하는지 진단
3. JCP ref. 6, 7 의 self-consistent integral equation 해법을 본 graphite dQ/dV 문제의 되먹임 해결에 적용하는 안의 1차 스케치

본 계획서는 **상황 파악 단계 (Phase A ~ D)** 에 한정한다. Chapter 1 본문의 본격 LaTeX 디벨롭은 본 계획서 범위 외 — 본 계획서 종료 후 별도 후속 계획서 (`Claude/plans/<date>-chapter1-rebuild-plan.md`) 로 진입.

## Current Ground Truth

### 확정 (4-tier "확정")

- `Claude/docs/graphite_ica_dynamic_ver5.tex` = 1974 줄. `\section{ver.1 기본식}` ~ `\section{ver.5 의 목적과 적층 규칙}` 5개 블록.
  - Chapter 1 (ver.1 기본식) 영역: 줄 46 ~ 약 526
  - Chapter 2 (ver.2 발열): 줄 527 ~ 855
  - Chapter 3 (ver.3 반응속도론): 줄 856 ~ 1125
  - Chapter 4 (ver.4 통합): 줄 1126 ~ 1522
  - Chapter 5 (ver.5 히스테리시스): 줄 1523 ~ 끝
  - 근거: 본 세션 grep 결과 `\section|\subsection` 패턴 매칭 (앞 100개 결과까지 확인. 줄 1500 이후의 세부 subsection 은 미확인 — Phase A 에서 전수 확인)
- `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` = 495 줄. 제목 = "graphite ICA charge balance dynamic ver1 rechecked". Chapter 1 재작성판. 전하 보존식 기반 내부 전위 결정 흐름.
  - 근거: 본 세션 grep 결과 `\section` 14개 (문서 목적/원칙, 기호 컨벤션, 전하 보존식 등)
- `Claude/_local_only/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` = 2.07 MB. 사용자 본인 논문.

### 사용자 진술 (4-tier "추정" — Phase D 에서 검증)

- JCP 논문의 ref. 6, 7 이 self-consistent integral equation 해법 포함 (Phase D Step 14~16 에서 본문·서지 정독으로 확정 또는 근거 미발견 으로 이동)

### 직전 gate

없음 (본 phase 가 본 프로젝트 첫 작업 phase. Phase 0 (Assess) 는 이전 셋업 단계에서 완료 — repo 셋업 / 폴더 표준 / 글로벌 메모리 정합)

### 미확인 사항 (Decision Queue 또는 Phase 내 해결 대상)

- ChatGPT 가 ver1_rechecked2 작업 진입 직전 범했던 "큰 논리 오류" 의 구체 정체 (DQ1)
- JCP 논문의 총 페이지 수 (Phase D Step 14 시작 시 확인)
- ver1_rechecked2 의 self-consistent loop 의 구체 위치·변수 (Phase B 에서 진단)
- ver5 의 Chapter 2 ~ 5 에서 Chapter 1 으로 역참조되는 식 있는지 (Phase A Step 3 에서 인계 chain 추적)

## Phase Range

| Phase | 이름 | Cumulative Steps |
|---|---|---:|
| **A** | ver5 마스터 전문 정독 + 챕터 구조 매핑 | 1 ~ 6 |
| **B** | ver1_rechecked2 전문 정독 + 되먹임 구조 진단 | 7 ~ 10 |
| **C** | Chapter 1 (ver5) ↔ rechecked2 매핑표 + 되먹임 진단 통합 | 11 ~ 13 |
| **D** | JCP 논문 ref. 6, 7 정독 + 본 문제 적용 안 스케치 | 14 ~ 18 |

Chapter 1 본문 디벨롭 (Phase E~) 은 본 계획서 범위 외 — Step 19 부터 신규 계획서에서 이어 진행 (DQ3 사용자 결정 필요).

## Non-goals

본 계획서가 **하지 않는** 것:

- Chapter 1 본문의 LaTeX 디벨롭 (별도 후속 계획서)
- Chapter 2 ~ 5 본문의 수정·재작성
- Codex 측 산출물 (`Codex/results/` 등) read · 비교 (P2 정합 — 양 모델 산출물 독립성 보존)
- 사진 55장 OCR (다른 작업용 — 5-27 사용자 확정)
- ChatGPT 의 "큰 논리 오류" 정체 추정 (사용자 답변 대기 — DQ1)
- LaTeX 빌드 (정독·진단 단계라 빌드 미요)
- 원천 `.tex` · PDF · 임시저장소 원본 수정 (P2 + [[feedback_document_protection_addendum_pattern]] 정합)
- ref. 6, 7 외 다른 ref 의 정독 (본 작업과 직결되지 않으면 보류)

## Implementation Changes

### 신규 생성 (Claude/results/)

- `Claude/results/PHASE_A_ver5_master_structure_RESULT.md`
- `Claude/results/PHASE_B_ver1_rechecked_feedback_diagnosis_RESULT.md`
- `Claude/results/PHASE_C_chapter1_mapping_and_feedback_note_RESULT.md`
- `Claude/results/PHASE_D_jcp_ref6_7_methodology_RESULT.md`
- `Claude/results/PHASE_A_D_EXECUTION_LEDGER.md` ([[feedback_phase_execution_loop]] 12 컬럼 양식)

각 RESULT 는 [[feedback_phase_execution_loop]] 의 11항목 양식 준수.

### 수정 (Claude/docs/)

없음 (본 계획서 = 정독·진단 only).

### 신규 생성 (Claude/plans/)

본 계획서 자체. 후속 계획서는 본 계획서 종료 후 별도.

## Phase A — ver5 마스터 전문 정독 + 챕터 구조 매핑

**Steps:**

1. ver5.tex 줄 1 ~ 1000 전수 정독 (`Read offset=1 limit=1000`) — Chapter 1 + Chapter 2 전반 cover
2. ver5.tex 줄 1001 ~ 1974 전수 정독 (`Read offset=1001 limit=1000`) — Chapter 3 / 4 / 5 cover
3. 각 챕터 끝의 `\section{ver.N 으로 전달되는 기준식}` 절 (있는 만큼) 본문 전체 인용 추출 — 인계 chain 확정
4. 챕터 1 ~ 5 각각의 골격 요약 작성 (Summary 2 ~ 3 줄 + 핵심 식 번호 목록 + 핵심 변수 목록)
5. **챕터 1 상세** (rechecked2 와 매핑 대상이라 더 깊게): `\subsection` 트리 + 각 subsection 의 정의식 식 번호 · 핵심 변수 추출
6. `PHASE_A_ver5_master_structure_RESULT.md` 작성 ([[feedback_phase_execution_loop]] 11항목)
   - Read Coverage: 줄 1 ~ 1974 전수 (PASS)
   - 산출물: 챕터 골격표 + 인계 chain 표

**Gate (Phase A):**

- `GATE_A1`: ver5.tex 줄 1 ~ 1974 전체 read 했고 Result 의 `Read Coverage` 에 분할 호출 내역 (offset/limit 페어) 기록
- `GATE_A2`: Chapter 1 ~ 5 각각의 `시작 줄 ~ 끝 줄` 범위 + 헤더 (`\section{...}`) 전체 목록 확정
- `GATE_A3`: `ver.N 으로 전달되는 기준식` 절 전수 추출 (각 챕터에 1 개씩 = 4 개 예상 — Chapter 5 는 마지막이라 없을 수 있음)
- `GATE_A4`: Chapter 1 의 `\subsection` 트리 전수 추출 (Phase C 매핑 대상)

**중단 조건:**

- 줄 800 초과 길이의 단일 LaTeX 환경 (예: 거대 `align*` 블록) 발견 → 분할 read 추가 필요. 사용자에게 진척 보고 후 계속.

**다음 phase 진입 조건:** GATE_A1 ~ A4 모두 PASS.

## Phase B — ver1_rechecked2 전문 정독 + 되먹임 구조 진단

**Steps:**

7. ver1_rechecked2.tex 줄 1 ~ 495 전수 정독 (`Read` 단일 호출, 2000 limit 안)
8. 변수 의존성 추출: `V_n` / `V_{n,app}` / `V_{n,drive}` / `V_{n,OCV}` / `xi_j` / `q` / `I` / `Q_bg` / `T` 등의 정의식 · 의존 변수 매핑 (P3-1 검수 항목 정합)
9. **Self-consistent loop 식별**: 어느 변수가 어느 식에서 자기 자신 (또는 자기와 연쇄 연결된 변수) 으로 되먹여지는지 dependency graph 또는 의존 표로 표시 (P3-3 정합)
10. `PHASE_B_ver1_rechecked_feedback_diagnosis_RESULT.md` 작성
    - Read Coverage: 줄 1 ~ 495 전수 (PASS)
    - 산출물: 변수 의존성 표 + self-consistent loop 위치 + 4 분류 추정 (P3-4 정합)

**Gate (Phase B):**

- `GATE_B1`: ver1_rechecked2.tex 줄 1 ~ 495 전체 read 했고 Read Coverage 기록
- `GATE_B2`: 변수 의존성 표 작성 (변수 × 정의식 식 번호 × 의존 변수 × 자기참조 여부 컬럼)
- `GATE_B3`: self-consistent loop 위치 표시 (어느 식·어느 변수)
- `GATE_B4`: loop 4 분류 진단 (`정의상 implicit formulation` / `수치해법 필요` / `논리 공백` / `물리 가정 충돌`) — 본 phase 에선 "추정" 표기 OK (확정은 Phase D 후)

**중단 조건:** 본문에 정의되지 않은 변수가 본문 전개에 사용되면 "근거 미발견" 으로 표기 후 계속 진행.

**다음 phase 진입 조건:** GATE_B1 ~ B4 모두 PASS.

## Phase C — Chapter 1 (ver5) ↔ rechecked2 매핑표 + 되먹임 진단 통합

**Steps:**

11. Phase A 의 Chapter 1 `\subsection` 트리 ↔ Phase B 의 rechecked2 `\subsection` 트리 매핑표 작성 (3 열: ver5 Ch1 section / rechecked2 section / 디벨롭 방향)
12. 매핑 항목 분류: **유지** (양쪽 같음) / **신규 추가** (rechecked2 에만) / **삭제 후보** (ver5 Ch1 에만, 그러나 rechecked2 가 같은 의도를 다른 방식으로 표현) / **재정의** (양쪽 다 있지만 의미 변경) / **보류** (사용자 결정 필요)
13. `PHASE_C_chapter1_mapping_and_feedback_note_RESULT.md` 작성 — 매핑표 + Phase B 되먹임 진단 통합. **사용자 검수 요청 (Decision Gate)** 명시.

**Gate (Phase C):**

- `GATE_C1`: 매핑표 행 수 = `max(ver5 Ch1 subsection 수, rechecked2 subsection 수)` 이상 (양쪽 합집합)
- `GATE_C2`: 모든 행에 디벨롭 방향 라벨 (유지 / 신규 추가 / 삭제 후보 / 재정의 / 보류) 부여
- `GATE_C3`: 보류 라벨 행은 사용자 결정 대기 사유 명시 (Decision Queue 항목 추가)
- `GATE_C4` (Decision Gate): 사용자에게 매핑표 보고 + "방향 OK" 또는 수정 지시 회수

**다음 phase 진입 조건:** GATE_C4 PASS (사용자 승인). 미승인 시 매핑표 수정 후 재보고.

## Phase D — JCP 논문 ref. 6, 7 정독 + 본 문제 적용 안 스케치

**Steps:**

14. JCP PDF 정독 (분할 `Read pages="..."` — 총 페이지 수 시작 시 확인 후 10p 단위 분할)
15. 본문에서 ref. 6, 7 인용 위치 (page · paragraph) 확인 + 인용 맥락의 수식 · 전개 추출
16. Reference 리스트에서 ref. 6, 7 의 정확한 서지 정보 (DOI / 저자 / 학술지 / 권 · 호 · 페이지 / 연도) 확보
17. ref. 6, 7 의 원 방법론 (self-consistent integral equation 해법) 의 **수학적 구조** 요약 (해법 종류 = Picard iteration / Banach fixed-point / Volterra integral 등 중 어느 것인지, 또는 그 외)
18. 본 graphite dQ/dV 문제 (Phase B 진단된 되먹임 변수) ↔ ref. 6, 7 방법론의 변수 매핑 5 요소 작성 → `PHASE_D_jcp_ref6_7_methodology_RESULT.md` (P3-5 정합)

**Gate (Phase D):**

- `GATE_D1`: JCP 본문 전체 페이지 정독, Read Coverage 에 페이지 범위 기록 (예: pages 1-5, 6-10, ..., 14411-1 끝까지)
- `GATE_D2`: ref. 6, 7 의 본문 내 인용 위치 (page · paragraph) 명시
- `GATE_D3`: ref. 6, 7 의 서지 정보 5 항목 (저자 / 학술지 / 권 · 호 / 페이지 / 연도, 가능 시 DOI) 명시
- `GATE_D4`: 5 요소 매핑 (서지 / 본문 위치 / 원 방법론 / 변수 매핑 / 물리 가정 차이) 작성 (P3-5)

**중단 조건:** ref. 6, 7 이 사용자 진술 (self-consistent integral equation 해법) 과 실제 다르면 "추정 → 근거 미발견 또는 다른 분류" 로 정정 후 사용자에게 보고.

**다음 phase 진입 조건:** 본 phase 가 본 계획서 마지막 phase. 종료 후 종합 보고 + 후속 계획서 (Phase E ~) 작성 여부 사용자 결정 (DQ2, DQ3).

## Implementation Interfaces

각 phase 산출물의 표 양식. 실행 시 이 양식 그대로 따른다.

### Phase A — 챕터 골격표 양식

```markdown
| Chapter | ver.N 명칭 | 줄 범위 | `\section` 헤더 수 | `\subsection` 수 | 핵심 변수 | ver.N 으로 전달되는 기준식 절 위치 |
|---|---|---:|---:|---:|---|---|
| 1 | ver.1 기본식 | 46 ~ 526 | N | M | xi_j, V_n, ... | line 485 (예) |
```

### Phase B — 변수 의존성 표 양식

```markdown
| 변수 | 정의식 (식 번호 또는 line) | 의존 변수 | 자기참조? | 4-tier 분류 |
|---|---|---|---|---|
| V_n | Eq. (3) line 132 | xi_j, q, T | 예 (xi_j 의존) | 추정 |
```

### Phase C — Chapter 1 매핑표 양식

```markdown
| ver5 Ch1 subsection (헤더 + 라인) | rechecked2 subsection (헤더 + 라인) | 디벨롭 방향 | 비고 |
|---|---|---|---|
| §3.1 기호 정의 (line 92) | §2.1 기본 좌표 (line 68) | 유지 (rechecked 가 더 명확) | rechecked2 가 우선 |
| §6.1 전위 보조 구동력 (line 212) | (없음) | 보류 (사용자 결정) | rechecked2 의 전하 보존식 흐름에서 필요한지 |
```

### Phase D — ref. 6, 7 매핑 5 요소 양식

```markdown
## Ref. N — <짧은 식별 라벨>

- **서지**: 저자 (연도). 제목. 학술지 vol(no), pp. DOI: ...
- **인용 위치 (JCP 본문)**: page P, paragraph para — 인용 맥락 (Eq. (X) 위·아래 등)
- **원 방법론 수학 구조**: <self-consistent integral equation 형태 + 해법 종류>
- **본 문제 변수 매핑**:
  | ref. N 원 변수 | 본 문제 (ver1_rechecked2) 대응 변수 |
  |---|---|
  | ψ(r) | V_n(q, T) |
  | ρ(r) | xi_j(q, T) |
  | ... | ... |
- **물리 가정 차이**: <원 ref 가정 vs 본 문제 가정 — 그대로 가져오면 안 되는 항목>
```

### Ledger 양식

`Claude/results/PHASE_A_D_EXECUTION_LEDGER.md` 는 [[feedback_phase_execution_loop]] §3 의 12 컬럼 표 양식 그대로.

## Test Plan

본 계획서의 산출물을 검증하는 방법. 각 phase 의 Gate 가 본 Test Plan 의 항목을 실제로 만족시키는지 [[feedback_gate_design_principle]] 의 "확인 가능한 조건" 양식으로 확인.

| # | 검증 항목 | 방법 | 통과 기준 |
|---|---|---|---|
| T1 | Read Coverage 대조 | 각 Result 의 `Read Coverage` 항목과 실제 파일 줄/페이지 수 cross-check | Sum(분할 read 의 limit) ≥ 파일 총 줄 수. 미달이면 미검독 영역 명시 |
| T2 | 변수 의존성 표 무모순 | Phase B 의 표가 ver1_rechecked2 본문에 등장하는 모든 주요 변수를 포함 | grep 으로 변수 출현 횟수 ≥ 1 인 변수 모두 표에 존재 |
| T3 | 챕터 인계 chain 무손실 | Phase A 의 `ver.N 으로 전달되는 기준식` 절 추출 결과 ↔ ver5 본문의 해당 절 전문 | diff 무결 (인용한 본문 = 원문) |
| T4 | ref. 6, 7 서지 신뢰성 | Phase D 의 서지 정보가 DOI 또는 학술지 권·호·페이지 정보로 외부 학술 DB 에서 1:1 매칭 | web 검색 OK. 매칭 안 되면 "근거 미발견" |
| T5 | 4-tier 분류 일관성 | 모든 Result 의 보고 항목이 확정 / 근거 미발견 / 추정 / 미검증 중 하나로 분류 | 분류 없는 항목 0 개 |
| T6 | 매핑표 합집합 cover | Phase C 매핑표 행 수 ≥ ver5 Ch1 subsection 수 + rechecked2 subsection 수 - 공통 항목 수 | 누락 행 0 개 |

## Assumptions

- **A1**. ver5 의 `\section{ver.N ...}` 헤더가 Chapter N 으로 재해석된다는 사용자 의도 (5-27 사용자 진술 — 본 세션 시작 메시지)
- **A2**. ver1_rechecked2 = ver5 Chapter 1 의 재작성판이며, ChatGPT 가 범한 "큰 논리 오류" 후 사용자가 처음부터 다시 시작한 판본 (5-27 사용자 진술)
- **A3**. `Claude/_local_only/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf` 가 사용자 본인 저자 논문 (5-27 사용자 진술)
- **A4**. JCP 논문의 ref. 6, 7 이 self-consistent integral equation 해법 포함 (5-27 사용자 진술 — Phase D Step 15 ~ 17 에서 검증. 검증 후 확정 또는 근거 미발견)
- **A5**. Phase E 이후 Chapter 1 본문 디벨롭은 별도 계획서 — 본 계획서 범위 외 (DQ2, DQ3 사용자 결정 후 시작)
- **A6**. 사진 55장은 본 작업과 무관 (5-27 사용자 확정)
- **A7**. Codex 측 산출물 read 안 함 — 운용 지침 (`Codex/AGENTS.md`, `Codex/plans/phase_planning_operations_guide.md`) 은 사용자가 명시 요청한 경우에만 read (P2 + 본 세션 이전 read 가 이에 해당)

## Correction History

- **2026-05-27 v0.1** (대화 본문판): 11 sections 양식 적용 안 한 초기 계획서. ver5/ver1 정독 순서 + JCP ref 6,7 적용 큰 흐름만 제시. Sprint Contract (Success Criteria + QA Tier) 미적용.
- **2026-05-27 v0.2** (본 문건): G2 메모리 [[feedback_plan_template_11sections]] 의 11 sections 양식으로 재작성. cumulative step (1 ~ 18) 적용. 각 Phase 별 `Gate_<X><N>` 식별자 부여. Implementation Interfaces 에 표 양식 명시. Test Plan 에 6 검증 항목 명시. v0.1 의 큰 흐름은 유지 — 본문 구조만 양식 정합.

## Success Criteria (Sprint Contract)

> governance `~/.claude/governance/03-phase-workflow.md` §"Sprint Contract (A2)" 정합

- [ ] **Phase A 종료**: GATE_A1 ~ A4 PASS. ver5.tex 1 ~ 1974 줄 전수 정독 + 챕터 골격표 + 인계 chain 표
- [ ] **Phase B 종료**: GATE_B1 ~ B4 PASS. ver1_rechecked2.tex 1 ~ 495 줄 전수 정독 + 변수 의존성 표 + self-consistent loop 위치 + 4 분류 추정
- [ ] **Phase C 종료**: GATE_C1 ~ C4 PASS. Chapter 1 매핑표 + 사용자 검수 통과 (Decision Gate)
- [ ] **Phase D 종료**: GATE_D1 ~ D4 PASS. JCP 본문 전수 정독 + ref. 6, 7 서지·본문 위치·원 방법론·변수 매핑·물리 가정 차이 5 요소 완비
- [ ] **종합**: Decision Queue (DQ1 ~ DQ3) 사용자 답변 회수 또는 보류 사유 명시 + 후속 계획서 (Phase E ~) 진입 결정 사용자 답변 회수

## QA Tier (Sprint Contract)

> governance `~/.claude/governance/03-phase-workflow.md` §"Sprint Contract (A2)" 정합

- [ ] Quick (Critical / High 만)
- [x] **Standard** (+ Medium) ← 기본값 + 본 작업에 적합
- [ ] Exhaustive (전체, Cosmetic 포함)

근거: 본 계획서는 정독·진단 중심 (Phase A ~ D 모두 read coverage 와 4-tier 분류가 핵심). Quick (Critical/High 만) 으로는 Medium 의 미검독 영역 누락 위험. Exhaustive (Cosmetic 까지) 까지는 디벨롭 단계가 아니라 불필요.

## Decision Queue (사용자 결정 대기)

- **DQ1**: ChatGPT 가 ver1_rechecked2 작업 진입 직전 범했던 "큰 논리 오류" 의 구체 정체. Phase B 정독 시 같은 함정에 빠지지 않기 위해 사용자 진술 권장. 확보 안 되면 Phase B 의 self-consistent loop 진단을 사용자에게 추가 검증 받기.
- **DQ2**: 본 계획서 종료 후 Chapter 1 본문 디벨롭 진입 시 산출물 위치
  - 안 (i): `Claude/results/PHASE_E_..._RESULT.md` 안에 본문 + 메타 같이
  - 안 (ii): `Claude/docs/graphite_ica_chapter1_v0.1.tex` 신설 (P5 의 원본 .tex 보존 정합)
  - 안 (iii): `Claude/work/chapter1_rebuild/` 작업 폴더 안에 진행 후 안정화 시 `Claude/docs/` 로 이동
  - **추천**: 안 (ii) 또는 (iii)
- **DQ3**: cumulative step 1 ~ 18 의 본 계획서 종료 후 Phase E ~ 의 step 시작 번호 = 19. 단일 계획서로 이어갈지 신규 계획서로 분리할지
  - G3 정합: 단일 계획서 이어가기 = step 번호 단조 증가 (Phase E 가 step 19 부터)
  - 다만 본 계획서가 상황 파악, 후속이 본문 디벨롭이라 의미 단위가 다름 → **신규 계획서 + cumulative step 19 ~ 이어받기** 권장

---

## 메타

- 본 계획서는 [[feedback_planning_vs_execution]] 준수 — 사용자 GO 사인 후 Phase A Step 1 진입.
- 본 계획서 자체의 commit + push 는 사용자 검수 후 진행 (현재 staging 안 함).
- Codex 측 거울 계획서가 `Codex/plans/` 에 별도 존재할 수 있음 — 본 Claude 계획서와 독립 (P2 + [[feedback_document_protection_addendum_pattern]] 정합).
