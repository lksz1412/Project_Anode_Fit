# Anode Fit — Chapter 1 Rebuild from Scratch Plan

작성일: 2026-05-27
작성자: Claude (Project_Anode_Fit Claude 측)
양식: [[feedback_plan_template_11sections]] (Codex `Codex/plans/phase_planning_operations_guide.md §4` 정합)
선행: `Claude/plans/2026-05-27-anode-fit-situational-assessment-plan.md` (Phase A~D, Steps 1-18) + `Claude/results/PROJECT_AUDIT_REPORT.md`

## Summary

신 **Chapter 1 (전하 보존식 기반 흑연 음극 ICA/DVA 동역학 기본식)** 본문을 **처음부터 새로 작성**.

사용자 5-27 verbatim:
> "기존의 것을 고치는 쪽이 아닌 기존의 것을 참고만 하고 전체를 다시 처음부터 작성하는 것을 요청한다."

따라서:
- ver5 Ch1 (`Claude/docs/graphite_ica_dynamic_ver5.tex` line 46-526) 본문 직접 수정 X
- ver1_rechecked2 (`Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` line 1-495) 본문 직접 수정 X
- 두 원본은 **참고 자료** 로만 사용. 새 .tex 파일 신설 (`Claude/docs/graphite_ica_chapter1_v0.1.tex`)
- 본 audit 보고서 (`PROJECT_AUDIT_REPORT.md`) 의 §3 부족 + §4 잘못 + §5 해결안을 흡수해 신 본문에 반영
- 핵심 신규: **§16 — Ref. 6, 7 의 비율 substitution 기법을 graphite 의 self-consistent loop (Phase B 의 Loop 3) 에 적용** 단원 신설

본 계획서 범위는 **Chapter 1 한정**. Chapter 2~5 본문 작성은 별도 후속 계획서.

## Current Ground Truth

### 입력 자산 (확정)

- **원본 참고** (수정 X):
  - `Claude/docs/graphite_ica_dynamic_ver5.tex` (1974 줄, 5 chapter 마스터)
  - `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` (495 줄, Chapter 1 재작성판)
  - `Claude/_local_only/JCP_147(14)_144111_(2017)...pdf` (10 페이지, 사용자 본인 논문)
  - `Claude/_local_only/jcp_extract.txt` (724 줄, pdftotext 추출본)
- **본 audit 산출물**:
  - `Claude/results/PROJECT_AUDIT_REPORT.md` (본 계획서 직전 작성)
  - `Claude/results/PHASE_A_ver5_master_structure_RESULT.md` (Chapter 1 의 21 subsec 트리)
  - `Claude/results/PHASE_B_ver1_rechecked_feedback_diagnosis_RESULT.md` (+ Addendum 1) — Loop 1/2/3 + 변수 의존성 23 행 + 4 분류
  - `Claude/results/PHASE_C_chapter1_mapping_and_feedback_note_RESULT.md` — 47 매핑 행 (유지 6 / 신규 8 / 삭제 후보 8 / 재정의 25)
  - `Claude/results/PHASE_D_jcp_ref6_7_methodology_RESULT.md` — ref. 6, 7 의 비율 substitution 방법론 + 5 요소 매핑 + 4 차이

### 직전 gate

- Phase D = `PASS_JCP_REF6_7_METHODOLOGY` (commit `0641cb8`)
- Phase A~D 모두 PASS, cumulative Steps 1-18 종료

### 미확인 사항 (Phase E 진입 시 또는 진입 후 해결)

- ref. 6, 7 의 정확 LaTeX 식 (특히 Eq. 32, 33, 34, 37, 39) — pdftotext 깨짐, 사용자 의뢰 권장 (OI-D3)
- ref. 6, 7 의 DOI (OI-D2) — 외부 검색 또는 사용자 의뢰
- ref. 7 의 분리 기여 (OI-D1) — 사용자 의뢰 또는 ref. 7 직접 정독 별 phase
- "저 C-rate + 큰 Q_bg slope" 의 정량 영역 (OI-D4) — graphite 실험 데이터 또는 시뮬레이션
- GATE_C4 사용자 매핑표 검수 (Phase C, 사전 GO 면제로 보류)
- DQ1 (ChatGPT 의 "큰 논리 오류" 정체) — 사용자 답변 회수 권장

### 사전 결정 (본 계획서 자체가 답인 항목)

- **DQ2** (Phase E 산출물 위치): **`Claude/docs/graphite_ica_chapter1_v0.1.tex`** 신설 (원본 보존, P5 정합)
- **DQ3** (단일 vs 신규 계획서): **신규 계획서 + cumulative step 19~ 이어받기** (의미 단위 다름 — 상황 파악 vs 본문 작성)

## Phase Range

| Phase | 이름 | Cumulative Steps |
|---|---|---:|
| **E** | 신 Chapter 1 본문 작성 (LaTeX) | 19 ~ 30 |
| **F** | LaTeX 빌드 + 사용자 검수 + 정정 루프 | 31 ~ 35 |

Chapter 2~5 본문은 별 계획서 (cumulative step 36 ~). 본 계획서는 Chapter 1 한정.

## Non-goals

본 계획서가 **하지 않는** 것:

- ver5 Ch1 또는 ver1_rechecked2 의 **본문 직접 수정** (P5 + [[feedback_document_protection_addendum_pattern]] 정합 — 두 원본은 그대로 보존)
- Chapter 2 ~ 5 본문 작성 (별 후속 계획서)
- Ref. 7 직접 정독 (별 phase 필요 시)
- Ref. 6, 7 의 graphite 적용 알고리즘 의 **수치 구현** (예: Python solver 작성) — 본 계획서는 LaTeX 문건 작성만, 수치 구현은 Phase G (별 계획서)
- ref. 6, 7 의 정량 검증 (실험 데이터 또는 시뮬레이션 cross-check) — Phase G 또는 별 계획서
- Codex 측 산출물 read·통합 (P2 정합)
- 원천 .tex / PDF / 임시저장소 원본 수정

## Implementation Changes

### 신규 생성 (`Claude/docs/`)

- **`Claude/docs/graphite_ica_chapter1_v0.1.tex`** — 신 Chapter 1 본문 (★ 핵심 산출물)

### 신규 생성 (`Claude/results/`)

- `Claude/results/PHASE_E_chapter1_body_writing_RESULT.md`
- `Claude/results/PHASE_F_build_and_review_RESULT.md`
- `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md`

### 수정 (`Claude/docs/`)

- 없음 (ver5.tex, rechecked2.tex 모두 보존)

### 신규 생성 (`Claude/plans/`)

- 본 계획서 자체

## Phase E — 신 Chapter 1 본문 작성 (LaTeX)

**Steps:**

### Step 19 — 신 Chapter 1 의 spine 설계 + § 골격 확정

- ver5 Ch1 spine (`ΔG_eff → k_j → dξ/dt → dξ/dq → dQ/dV`) vs rechecked2 spine (`Q_ext = Q_cell·q → 전하 보존식 → V_n → V_{n,app} → dQ/dV`) 중 **rechecked2 spine 채택** (전하 보존식 중심 = 사용자 의도 = self-consistent loop 의 출발점)
- § 골격: Phase C 매핑 47 행 의 라벨 기반:
  - **유지 6**: 그대로 채택 (rechecked2 표현)
  - **신규 추가 8**: rechecked2 의 신규 모두 포함 (전하 보존식 §, 해 존재 조건, Q_bg slope floor, softplus, 단조성 제약, 휴지 처리, 초기 조건 정합, 단위 컨벤션)
  - **재정의 25**: rechecked2 우선 채택 (확장·명료화 방향)
  - **삭제 후보 8**: DQ-C1~C6 결과에 따라 — 본 계획서 가정으로 ver5 §14 (목적 함수) + §16 (모델 수준) + §19 (참고문헌) **부활** (사용 빈도 + 가치 평가), ver5 §5.2 (Erf) + §9.1 (Q_n) + §7.3 해석 + §11 (온도 효과 별 단원) **삭제 유지**
- §16 신설 — **★ Ref. 6, 7 의 비율 substitution 기법을 graphite Loop 3 에 적용** 단원
- 본 골격을 `PHASE_E_RESULT.md` §"§ 골격 설계" 로 기록

### Step 20 — §1 (문서의 목적과 원칙) + §2 (기호와 단위 컨벤션)

- §1: rechecked2 §1 (line 47-65) base + 본 audit 보고서 의 spine 표 추가 + DQ1 답 받으면 ChatGPT 오류 회피 주의 추가
- §2: rechecked2 §2 (line 67-107) 채택 — 기호 표 + 단위 컨벤션 (Q_cell 쿨롱) + 추가: ver5 Ch1 의 상세 변수 (ΔH, ΔS, ν_j, χ_j 등) 도 표에 포함 (재정의 분류 행 #3 의 통합)

### Step 21 — §3 (흑연 staging) + §4 (전하 보존식)

- §3: rechecked2 §3 (line 109-116) base + ver5 Ch1 의 effective transition 표 (line 140-150) 통합 (재정의 행 #6)
- §4 (★): rechecked2 §4 전체 (line 118-182) 채택 — 전하 보존식 + 평형 OCV + 총용량 정합 + 배경 용량 함수 수치 조건. **신 Chapter 1 의 중심 단원**

### Step 22 — §5 (평형 진행률) + §6 (상변이 속도식)

- §5: rechecked2 §5 (line 184-201) base + ver5 Ch1 의 logistic 식 본문 정합 cross-check (행 #15)
- §6: rechecked2 §6 전체 (line 203-266) 채택 — V_n / V_{n,app} / V_{n,drive} 3 종 분리 + softplus + 속도상수. **★ P3-1 검수 항목 정합**

### Step 23 — §7 (진행률 동역학) + §8 (장벽 분포)

- §7: rechecked2 §7 전체 (line 268-318) 채택 — 시간 영역 + q 좌표 (정전류만) + 휴지 처리 + 초기 조건 정합
- §8: rechecked2 §8 전체 (line 320-351) 채택 — 장벽 분포 support `g ≥ 0` + softplus

### Step 24 — §9 (ICA · DVA)

- §9.1 (내부 전위 미분): rechecked2 §9.1 (line 354-377) 채택 + 단조성 제약 (Eq. monotonic_constraint) 포함
- §9.2 (apparent 전위 미분): rechecked2 §9.2 (line 379-392) 채택
- §9.3 (ICA · DVA): rechecked2 §9.3 (line 394-412) 채택 — **`dQ_ext/dV_{n,app} = Q_cell / (dV_{n,app}/dq)`** 의 외부 전하 기준

### Step 25 — §10 (C-rate · 온도) + §11 (실용 피팅식 · EMG)

- §10: rechecked2 §10 (line 414-430) base + ver5 Ch1 의 C-rate 효과 2 경로 (line 367-375) 통합. 0.2C 기준 포함. **온도 효과는 별 § 아닌 inline 유지** (DQ-C3 답: rechecked2 방식)
- §11: rechecked2 §11 (line 432-437) + ver5 Ch1 의 EMG 식 (line 398) 통합. "초기값 / 비교용만" 명시

### Step 26 — §12 (피팅 절차) + §13 (목적 함수 · 정규화) + §14 (식별성 · 제약) + §15 (모델 수준)

- §12: rechecked2 §12 (line 439-460) base + ver5 Ch1 의 §13 피팅 절차 (line 420-427) 통합
- §13 (DQ-C4 답: 부활): ver5 Ch1 의 §14 목적 함수 (line 431-443) 채택 + 새 spine 에 맞춰 변수 갱신
- §14: rechecked2 §12 의 식별성 표 (line 449-460) + ver5 Ch1 의 §15 (line 446-468) 통합
- §15 (DQ-C5 답: 부활): ver5 Ch1 의 §16 모델 수준 Level 0~5 (line 470-483) 채택

### Step 27 — §16 (★ Ref. 6, 7 의 self-consistent loop 해법 적용) — **신 단원**

본 계획서의 **★ 핵심 신규 단원**. 본 audit 보고서 §1.4 + §5.10 의 정량화 + Phase D Result §"5 요소 매핑" 흡수.

세부 subsection:
- §16.1 — Self-consistent loop 의 정체 (Phase B 의 Loop 1/2/3 본문 인용 + Volterra integral 형태 명시)
- §16.2 — Ref. 6, 7 의 비율 substitution 기법 요약 (Fredholm 2nd kind / Eq. 32 → 33 → 34 → 39 의 단계)
  - 정확 LaTeX 식 사용자 의뢰 — **DQ-E1 (사용자 응답 대기)**
  - 사용자 응답 없으면 본 audit 의 line 번호 + 의도 추출 형태 유지
- §16.3 — graphite 변수 매핑 (5 요소 매핑 표 — Phase D Result §"5 요소 매핑" 의 변수 대응 표 그대로 채택)
- §16.4 — 4 가지 차이 (Fredholm/Volterra, 공간/시간, isotropy, 정확도 영역) 와 graphite 적용 시 변환
  - Fredholm → Volterra 변환 명시 (적분 범위 변경)
  - 시간/공간 변환 표 (r ↔ t, σ ↔ t=0, ∞ ↔ ∞ 또는 ∞ ↔ 종료 시간)
  - isotropic 1D 단순화 (anisotropic μ 항 제거)
  - 정확도 영역 (저 C-rate + 큰 Q_bg slope + |I|·R_n << V_n 스케일) — 정성, 정량은 후속 phase
- §16.5 — graphite 에 적용된 closed-form analytic expression (Volterra 변환 후의 새 Eq. 39 대응식)
- §16.6 — Algorithm pseudocode (DAE solver + Loop 1 root-find + 비율 substitution)
- §16.7 — 한계와 적용 영역 (저율·약한 분극 영역 정확, 고율·강한 분극 정확도 저하)

### Step 28 — §17 (ver.2 로 전달) + §18 (자기 검수)

- §17: rechecked2 §13 (line 462-470) 채택 — `dξ_j/dt` 우선 + 정전류 시 q 변환
- §18: 신 자기 검수 (16 항목 이상 — rechecked2 §14 의 13 항목 + 신규 §16 의 ref. 6, 7 적용 확인 + Loop 1/2/3 명시 + 4 차이 변환 확인)

### Step 29 — §19 (참고문헌) (DQ-C6 답: 부활)

- ver5 Ch1 의 §19 5 ref (line 518-523) 채택 + JCP 2017 본인 논문 추가 + Ref. 6, 7 추가 (사용자 DOI 의뢰 결과 반영 — 받으면 DOI 포함, 없으면 권/호/페이지만)

### Step 30 — 전체 본문 통합 + 일관성 점검

- 모든 § 통합 후 변수명·식 번호·내부 참조 (\ref, \eqref) 일관성 점검
- spine 식 (§1) ↔ 본문 식들 (§4, §5, §6, §7, §9, §16) 일관성
- ver.2 로 전달되는 기준식 (§17) 이 본문에서 정의된 모든 변수 사용 확인

**Gate (Phase E):**

- `GATE_E1` — 신 Chapter 1 본문 `Claude/docs/graphite_ica_chapter1_v0.1.tex` 작성 완료. § 골격 (Step 19) 의 모든 §·subsec cover
- `GATE_E2` — 본 audit 보고서 §3 부족 + §4 잘못 + §5 해결 모두 반영 확인 (특히 §16 신설, 변수 의존성 명시, 4-tier 분류 일관성)
- `GATE_E3` — Phase C 매핑표 47 행 의 디벨롭 방향 라벨 (유지 6 / 신규 8 / 삭제 후보 8 / 재정의 25) 모두 신 본문에 반영 (삭제 후보 중 부활 결정한 §14·§15·§19 도 포함)
- `GATE_E4` — 신 Chapter 1 의 인계 chain (`§17 ver.2 로 전달되는 기준식`) 의 식이 본 Chapter 1 본문 의 §4·§5·§7·§9·§16 식과 정합

**중단 조건:**

- 본문 작성 도중 Phase A~D 의 정독으로 cover 안 된 영역 발견 (예: Chapter 2~5 의 식이 신 Chapter 1 의 인계에 영향) → 사용자 보고 + 정정
- LaTeX 매크로 충돌 또는 정의되지 않은 변수 발견 → 본 phase 안에서 정의 추가

**다음 phase 진입 조건:** GATE_E1~E4 모두 PASS

## Phase F — LaTeX 빌드 + 사용자 검수 + 정정 루프

**Steps:**

### Step 31 — LaTeX 빌드 환경 확인 + 빌드 시도

- 환경 check: `which pdflatex xelatex lualatex; which kotex` (한글 문서)
- ver5.tex 의 preamble (line 1-44) 와 rechecked2.tex 의 preamble (line 1-36) 참조해 신 Chapter 1 의 preamble 작성
- 첫 빌드 시도 (`pdflatex graphite_ica_chapter1_v0.1.tex` + 한글 시 `xelatex` 또는 `lualatex`)

### Step 32 — 빌드 에러 정정 루프

- 빌드 에러 발생 시 즉시 정정 (LaTeX 문법 / 누락 매크로 / undefined ref)
- 최대 3 회 빌드 시도. 3 회 후에도 에러 시 사용자 의뢰
- 빌드 성공 시 PDF 출력 확인 (페이지 수 + § 헤더 + 식 렌더링)

### Step 33 — PDF 출력 사용자 검수 요청 (**★ Decision Gate**)

- 빌드 성공한 PDF 를 사용자에게 제출
- 사용자 검수 항목 권장:
  - 신 Chapter 1 의 spine 이 의도 정합
  - §16 (ref. 6, 7 적용) 의 수식 정확성 (사용자 = 본인 저자라 정확 cross-check 가능)
  - 변수 정의·기호 일관성
  - GATE_C4 (Phase C 매핑) 의 라벨 적합성 (유지/신규/삭제/재정의 결정 합당성)
  - DQ-C1~C6 의 본 계획서 가정 (§14·§15·§19 부활 / §5.2 Erf·§9.1 Q_n·§11 별 단원 삭제) 적합성
- **Decision Gate `GATE_F1`**: 사용자 검수 통과 또는 정정 지시 회수

### Step 34 — 사용자 피드백 반영 (정정 또는 v0.2)

- 사용자 정정 지시 받으면:
  - 경미한 정정 (식 오타·라벨 변경) → 본문 직접 정정 + commit
  - 본질적 정정 (§ 추가·구조 변경) → `Claude/docs/graphite_ica_chapter1_v0.2.tex` 신설 (v0.1 보존, [[feedback_document_protection_addendum_pattern]] 정합) 또는 `PHASE_E_RESULT_ADDENDUM_<n>.md` + 다음 빌드 phase
- 정정 후 Step 31~33 반복 (최대 3 라운드)

### Step 35 — 최종 commit + push

- 사용자 검수 통과 후 최종 commit
- 본 계획서 종료 + Chapter 2~5 후속 계획서 작성 여부 사용자 결정 회수

**Gate (Phase F):**

- `GATE_F1` (★ Decision Gate) — 사용자 PDF 검수 통과 또는 명시적 GO 사인
- `GATE_F2` — LaTeX 빌드 PASS (3 회 이내, 빌드 로그 무경고 권장)
- `GATE_F3` — 신 Chapter 1 의 PDF 출력 정합 (페이지 수 합리 + § 모두 렌더링 + 식 깨짐 X)

**다음 phase 진입 조건:** 본 계획서 마지막 phase. 종료 후 Chapter 2~5 후속 계획서 작성 사용자 결정 (별 계획서 또는 cumulative step 36~ 이어가기).

## Implementation Interfaces

### 신 Chapter 1 의 § 골격 (Step 19 결과 미리 명시)

```
신 Chapter 1 — 전하 보존식 기반 흑연 음극 ICA/DVA 동역학 기본식

§1   문서의 목적과 원칙 (spine 식 + ChatGPT 회피)
§2   기호와 단위 컨벤션
     §2.1 기호 정의 (확장 표 — rechecked2 11 + ver5 추가 변수)
     §2.2 단위 컨벤션 (Q_cell 쿨롱 + Ah→C 변환)
     §2.3 전류·전위 부호 conv. (s_I, s_{φ,j}, s_{ξ,j})
§3   흑연 staging 과 effective transition index
§4   ★ 전하 보존식: 내부 전위의 결정
     §4.1 전하 보존식 (Eq. charge_balance — 중심식)
     §4.2 평형 OCV 의 의미 (전하 보존식의 평형해)
     §4.3 총용량 정합 조건
     §4.4 배경 용량 함수의 수치 조건 (∂Q_bg/∂V_n ≥ ε_Q)
§5   평형 진행률 ξ_{j,eq}
     §5.1 Logistic 표현
     §5.2 평형 피크와 실제 피크 (mdframed note)
§6   상변이 속도식
     §6.1 V_n / V_{n,app} / V_{n,drive} 3 종 구분
     §6.2 유효 장벽 + 속도상수 + softplus regularization
§7   상변이 진행률 동역학
     §7.1 시간 영역 식 (dξ_j/dt = k_j(ξ_eq - ξ_j))
     §7.2 정전류 구간의 q 좌표 식
     §7.3 휴지 구간 처리 (|I|=0 시 V_n(t) relaxation)
     §7.4 초기 조건 + 전하 보존식 정합
§8   장벽 분포 동역학
     §8.1 장벽 분포 support g ≥ 0
     §8.2 장벽별 진행률 + softplus
     §8.3 분포 평균
§9   ICA 와 DVA 유도
     §9.1 내부 전위 미분 (dV_n/dq) + 단조성 제약
     §9.2 apparent 전위 미분 (dV_{n,app}/dq)
     §9.3 ICA = dQ_ext/dV_{n,app} = Q_cell / (dV_{n,app}/dq)
     §9.4 DVA = dV_{n,app}/dQ_ext
§10  C-rate 효과와 0.2C 기준식 (온도 효과 inline)
§11  실용 피팅식 (EMG) 과 동역학 모델의 관계
§12  피팅 절차 (단계별)
§13  목적 함수와 정규화
§14  식별성 및 제약
§15  모델 수준 선택표 (Level 0 ~ 5)
§16  ★ Ref. 6, 7 의 self-consistent loop 해법 적용 (신 단원)
     §16.1 Self-consistent loop 정체 (Loop 1/2/3)
     §16.2 Ref. 6, 7 비율 substitution 기법
     §16.3 graphite 변수 매핑
     §16.4 Fredholm/Volterra·공간/시간·isotropy·정확도 영역 4 차이
     §16.5 graphite closed-form analytic expression
     §16.6 Algorithm pseudocode
     §16.7 한계와 적용 영역
§17  ver.2 로 전달되는 기준식
§18  자기 검수 체크리스트 (16 항목+)
§19  참고문헌 (ver5 5 ref + JCP 2017 + Ref. 6 + Ref. 7)
```

**총: 19 §, 22 subsec, 그 중 §16 신규**.

### LaTeX 파일 구조

```latex
\documentclass[11pt,a4paper]{article}
% preamble — ver5.tex line 1-44 base, kotex / amsmath / mdframed 포함
% 신규 매크로 (rechecked2 의 \drive 등) 추가

\begin{document}
\title{전하 보존식 기반 흑연 음극의 ICA/DVA 동역학 기본식 (신 Chapter 1)}
\author{Project_Anode_Fit Claude 측}
\date{2026-05-27}
\maketitle

\tableofcontents
\newpage

\section{문서의 목적과 원칙}
...

% §1 ~ §19 본문

\end{document}
```

### 변수 매핑 표 양식 (§16.3)

```markdown
| JCP 2017 / Ref. 6, 7 변수 | graphite (신 Chapter 1) 대응 변수 | 비고 |
|---|---|---|
| W̄_u(r) | ξ_j(t) 또는 V_n(t) | 시간 진화 변수 |
| r | t (시간) 또는 q (방전 좌표) | 적분 변수 |
| σ (contact distance, BC) | t=0 (초기) 또는 q=0 | 시간 영역 boundary |
| D (diffusion coefficient) | Q_cell | dq/dt = |I|/Q_cell |
| S_R(r, μ) | k_j(V_n, q, T, I) | 속도상수 |
| U_1(r) | Q_bg(V_n, T) | chemical capacitance |
| K = eE/kT | s_I·|I|·R_n / (kT?-like) | 외부 전류 분극 |
| μ = cos θ | (graphite isotropic, 부재) | |
| Fredholm integral (Eq. 32) | Volterra integral (Loop 3) | 적분 범위 변환 |
| W̄_u^δ(r) (Eq. 25) | ver5 Ch1 의 V_{n,OCV} 외부 함수 가정 하의 ξ_j(q) | 비율 substitution 기준 해 |
```

### 4 가지 차이 변환 표 (§16.4)

```markdown
| 차이 | JCP/Ref.6,7 (원) | graphite (신 Chapter 1) | 변환 방법 |
|---|---|---|---|
| 1. 적분 범위 | Fredholm [σ, ∞] 고정 | Volterra [0, t] 가변 | 적분 변수 r → t 치환, BC 재정의 |
| 2. 시간성 | 공간 정상상태 (steady-state ultimate) | 시간 진화 (transient ξ_j(t)) | "ultimate" 개념 폐기, t→t 의 비율 substitution |
| 3. 차원성 | anisotropic 3D + μ 적분 | isotropic 1D radial | μ 적분 제거, anisotropic 항 (Kr·μ) 제거 |
| 4. 정확도 영역 | 큰 Onsager rc + 작은 σ + 약 K | 저 C-rate + 큰 ∂Q_bg/∂V_n + |I|·R_n << V_n | 정성 명시, 정량은 Phase G 후속 |
```

### Result 양식 (Step 30 종료 시)

[[feedback_phase_execution_loop]] §2 의 11 항목 양식. 추가:
- `Section Implementation Status` (§1 ~ §19 의 완료/부분/미작성 표)
- `Cross-reference Verification` (변수 의존성 + spine 식 vs 본문 식 cross-check 결과)

### Ledger 양식

[[feedback_phase_execution_loop]] §3 의 12 컬럼 양식. Phase E + F 각 행.

## Test Plan

| # | 검증 항목 | 방법 | 통과 기준 |
|---|---|---|---|
| **T1** | 신 Chapter 1 본문이 본 audit 보고서 §3 부족 모두 해결 | §3 의 5 항목 (3.1 ~ 3.5) 별 본문 cross-check | 5 항목 모두 본문 또는 §"한계와 후속" 에 명시 |
| **T2** | 신 Chapter 1 본문이 §4 잘못 모두 정정 | §4 의 9 항목 (E1~E3 + B1~B3 + L1~L3) 별 본문 cross-check | E1~E3 = 이미 정정 / B1~B3 = 메모리 영구 반영 / L1~L3 = 본문 §16 에 명시 |
| **T3** | Phase C 매핑표 47 행 의 디벨롭 방향 모두 신 본문에 반영 | 47 행 vs 신 본문 § 매핑 검증 | 47 행 = 본 § (유지 6) ∪ 본 § (신규 8) ∪ 본문 부재 (삭제 8 중 부활 결정 X 부분) ∪ 본 § (재정의 25) |
| **T4** | 신 §16 의 4 차이 변환 모두 명시 | §16.4 의 표 4 행 | 4 행 모두 변환 방법 명시 |
| **T5** | LaTeX 빌드 PASS | `pdflatex` 또는 `xelatex` 실행 | exit code 0 + PDF 출력 페이지 ≥ § 수 |
| **T6** | 변수 의존성 일관성 | 신 본문 의 변수 사용 vs §2 의 기호 표 | 모든 사용 변수가 §2 에 정의 |
| **T7** | spine 식 ↔ 본문 식 일관성 | §1 의 spine 식 의 변수 (Q_ext, Q_cell, q, Q_bg, V_n, ξ_j, V_{n,app}, dQ/dV, dV/dQ) ↔ 본문 §4·§5·§6·§7·§9 의 식 | 모든 spine 변수가 해당 본문 § 에서 정의 + 사용 |
| **T8** | 인계 chain (§17) ↔ 본문 식 일관성 | §17 의 ver.2 전달 식 ↔ 본 Chapter 1 본문 식 | §17 의 모든 식이 본문 어딘가에 정의 또는 유도 |
| **T9** | 4-tier 분류 일관성 | 신 Chapter 1 본문 의 모든 정의·식·가정 의 4-tier (확정/근거미발견/추정/미검증) | 0 항목 미분류 |
| **T10** | 사용자 검수 통과 (Decision Gate) | PDF 제출 + 사용자 회신 | 사용자 GO 사인 또는 명시 정정 지시 |

## Assumptions

- **A1.** Phase C 매핑표 의 5 분류 라벨 (유지 6 / 신규 8 / 삭제 후보 8 / 재정의 25) 그대로 사용. 사용자 GATE_C4 검수 결과 다르면 본 계획서 v0.2 또는 Addendum 으로 정정.
- **A2.** DQ2 (Phase E 산출물 위치) = `Claude/docs/graphite_ica_chapter1_v0.1.tex` 채택.
- **A3.** DQ3 (단일 vs 신규 계획서) = 신규 계획서 + cumulative step 19~. **본 계획서가 그 답**.
- **A4.** DQ-C1 (Erf 표현 부활) = 삭제 유지 (rechecked2 의 logistic 만 사용, 단순화 의도 존중)
- **A5.** DQ-C2 (Q_n vs Q_ext) = Q_ext 채택 (rechecked2 의 외부 전하 기준)
- **A6.** DQ-C3 (온도 효과 별 단원) = 삭제 유지 (rechecked2 의 inline 방식 채택)
- **A7.** DQ-C4 (목적 함수 부활) = **부활** (ver5 Ch1 §14 채택 — 피팅 필수 단원)
- **A8.** DQ-C5 (모델 수준 선택표 부활) = **부활** (ver5 Ch1 §16 채택 — 모델 선택 가이드)
- **A9.** DQ-C6 (참고문헌 부활) = **부활** (ver5 Ch1 §19 5 ref + JCP 2017 + Ref. 6, 7 추가)
- **A10.** 사용자 = JCP 2017 의 제1저자 Kyusup Lee (Phase D 확정). §16 의 ref. 6, 7 정확 수식 + DOI 제공 의뢰 가능.
- **A11.** DQ1 (ChatGPT 의 큰 논리 오류 정체) 사용자 답변 없어도 진행. Phase B 진단 (Loop 1/2/3) 이 정확하므로 본문 작성 가능. 답 받으면 §1 의 "주의" 항목에 inline 반영.
- **A12.** 빌드 환경 = pdflatex 또는 xelatex + kotex. ver5.tex 의 preamble 호환 환경 가정.
- **A13.** 본 계획서 범위 = Chapter 1 한정. Chapter 2~5 + 수치 구현 + 정량 검증 모두 별 후속 계획서.

## Correction History

- **v0.1** (본 문건, 2026-05-27): 신규 작성. Phase A~D 의 모든 발견 (`PROJECT_AUDIT_REPORT.md` §3 부족 + §4 잘못 + §5 해결) 흡수. 사용자 5-27 verbatim "기존 것을 참고만 하고 전체를 다시 처음부터 작성" 의도 정합.

## Success Criteria (Sprint Contract)

> governance `~/.claude/governance/03-phase-workflow.md` §"Sprint Contract (A2)" 정합

- [ ] **Phase E 종료**: `GATE_E1` ~ `GATE_E4` 모두 PASS. 신 `Claude/docs/graphite_ica_chapter1_v0.1.tex` 작성. § 골격 19 § + 22 subsec 모두 cover. §16 신단원 7 subsec 완비 (적어도 §16.1, §16.3, §16.4 는 사용자 의뢰 없이 본 audit 자산 만으로 작성 가능, §16.2·§16.5 는 사용자 의뢰 결과 대기 placeholder).
- [ ] **Phase F 종료**: `GATE_F1` ~ `GATE_F3` 모두 PASS. LaTeX 빌드 PASS + PDF 출력 + 사용자 검수 통과 (또는 정정 지시 반영 후 재검수 통과).
- [ ] **종합**: Test Plan T1 ~ T10 모두 PASS. 신 Chapter 1 본문이 본 audit 보고서 §3 부족 + §4 잘못 의 해결안 반영 완료.

## QA Tier (Sprint Contract)

- [ ] Quick (Critical / High 만)
- [x] **Standard** (+ Medium) ← 기본값
- [ ] Exhaustive (전체, Cosmetic 포함)

근거: 본 계획서는 본문 작성 + 빌드 + 사용자 검수 중심. Quick 으로는 §16 신단원의 완성도 부족 위험. Exhaustive 까지는 cosmetic (LaTeX 미세 조판, font 등) 미요.

## Decision Queue (사용자 결정 대기)

| ID | 항목 | 우선순위 | 비고 |
|---|---|---|---|
| **DQ-E1** | §16.2 의 ref. 6, 7 정확 LaTeX 식 (Eq. 32, 33, 34, 37, 39) — 사용자 (본인 저자) 원문 직접 제공? | **높음** | 제공 받으면 §16.2·§16.5 즉시 본문화. 없으면 line 번호 + 의도 추출 형태 (Phase D Result §"원 방법론") 유지 |
| **DQ-E2** | Ref. 6, 7 의 DOI — 사용자 직접 제공 또는 외부 검색 의뢰? | **중간** | §19 (참고문헌) 의 DOI 부분만 영향. 빌드 자체엔 무영향 |
| **DQ-E3** | 빌드 환경 — pdflatex / xelatex / lualatex 중 사용자 권장? kotex 또는 polyglossia? | **중간** | Phase F Step 31 환경 check 시 사용자 확인 |
| **DQ-E4** | 본 계획서 가정 A1~A13 중 사용자가 다르게 결정하고 싶은 항목? 특히 A1 (Phase C 매핑 라벨 그대로) | 중간 | 검수 후 본 계획서 v0.2 |
| **DQ-E5** | DQ1 (ChatGPT 의 큰 논리 오류 정체) — 본 계획서 진행 중 사용자 답변? | 낮음 | A11 적용 — 없어도 진행 |
| **DQ-E6** | 사용자가 본 계획서를 검수하고 GO 사인 줄지? 또는 본 계획서 v0.2 가 먼저 필요? | **★ 최우선** | 본 계획서 commit + push 후 사용자 결정 회수 |

## 메타

- 본 계획서는 [[feedback_planning_vs_execution]] 정합 — Phase E Step 19 진입은 **사용자 GO 사인 후**.
- 본 계획서 자체는 commit + push 진행 (산출물 제출).
- 사용자 GO 사인 받으면 [[feedback_plan_continuation_until_done]] 정합으로 Phase E → F 자동 진입 (매 phase 종료마다 GO 재확보 X). 다만 GATE_F1 (사용자 PDF 검수) 은 사용자 사전 GO 면제 명시 시 보류 표기 후 진행.
- Codex 측 거울 계획서가 `Codex/plans/` 에 별도 존재할 수 있음 — 본 Claude 계획서와 독립 (P2 정합).
