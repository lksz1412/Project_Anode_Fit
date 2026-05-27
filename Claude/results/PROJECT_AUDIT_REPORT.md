# Project_Anode_Fit — Phase A~D 종합 Audit 보고서

작성일: 2026-05-27
작성자: Claude (Project_Anode_Fit Claude 측)
근거: Phase A~D 4 commit (`0944119` `2c8a72b` `99f7876` `0641cb8`) + 본 세션 대화 로그
양식: 사용자 요청 5-27 verbatim — "내가 파악한 것 / 잘된 것 / 부족한 것 / 잘못된 것 / 해결안"
관련 메모리: [[feedback_phase_audit_workflow]] · [[feedback_confirmed_items_policy]] · [[feedback_document_protection_addendum_pattern]]

---

## 1. 파악한 것 (What I Understood)

### 1.1 ver5.tex 마스터의 5 챕터 적층 구조

`Claude/docs/graphite_ica_dynamic_ver5.tex` (1974 줄) 는 현재 `\section{ver.1 ...}` ~ `\section{ver.5 ...}` 5 블록 = **사실상 Chapter 1 ~ Chapter 5**. 골격:

- **Chapter 1 (ver.1 기본식, 19§/21subsec)**: spine = `ΔG_eff,j → k_j → dξ_j/dt → ξ_j(q) → dξ_j/dq → dQ/dV, dV/dQ`. 핵심 변수 `V_n`, `V_{n,OCV}`, `V_{n,app}`, `ξ_j`, `k_j`, `R_n`. **V_{n,OCV}(q,T) 는 외부 함수 lookup**.
- **Chapter 2 (ver.2 발열, 13§)**: ver.1 의 `dξ_j/dq` 를 그대로 받아 발열 항을 **basis expansion** (열역학 항등식 아닌, 피팅용 reduced-order) 으로 적층. 가역열 / 비가역열 분리.
- **Chapter 3 (ver.3 반응속도론, 11§)**: `A_j` 를 단순 전위 보조에서 BV 과전압으로 일반화. **"평형 진행률 (ξ_{j,eq}) 은 OCV 기준 / 동역학 속도 (k_j) 는 apparent·과전압 기준" 분리 원칙** 강조 (중복 반영 금지 경고).
- **Chapter 4 (ver.4 통합, 14§)**: ver.1+2+3 의 식을 변경 없이 받아 통합 상태방정식·관측방정식·계산 절차로 묶음. 신규 수식 X, 절차 통합 only.
- **Chapter 5 (ver.5 히스테리시스, 16§)**: branch index `p ∈ {chg, dis}` 추가. 4 성분 분해 (저항성 / 동적 지연 / 구조 기억 / 열적). 기존 ξ_j 정의 변경 X.

**인계 chain 4 건**: `\section{ver.N 으로 전달되는 기준식}` (line 485 / 812 / 1066 / 1468). Chapter 5 는 terminal.

### 1.2 ver1_rechecked2 의 재정의 의도

`Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` (495 줄, 14§/14subsec) 는 Chapter 1 의 **재작성판**. 핵심 변경:

| 영역 | ver5 Ch1 | ver1_rechecked2 |
|---|---|---|
| **spine** | `ΔG_eff → k → dξ/dt → dξ/dq → dQ/dV` | **`Q_ext=Q_cell·q → 전하 보존식 → V_n → V_{n,app} → dQ/dV`** |
| **V_{n,OCV}** | 외부 함수 lookup | **전하 보존식의 implicit 해** (`Q_cell·q = Q_bg(V_n,T) + Σ Q_{j,tot} ξ_j` 의 V_n 의 root) |
| **전위 3 종 분리** | V_n ≡ V_{n,OCV}, V_{n,app}=V_n+IR | **V_n (내부) / V_{n,app} (관측) / V_{n,drive} (속도 구동) 3 종** |
| **Q_bg 역할** | 단순 배경 용량 | **잔류 chemical capacitance** — V_n 결정 자유도 |
| **기타 신규** | 부재 | 해 존재 조건, Q_bg slope floor (ε_Q), softplus 양수 장벽 (ε_G), 단조성 제약, 휴지 처리, 초기 조건 정합, 단위 (Q_cell 쿨롱) 명시, 장벽 분포 support g≥0 |

본 Phase C 매핑표 47 행: **유지 6 / 신규 추가 8 / 삭제 후보 8 / 재정의 25**.

### 1.3 self-consistent 되먹임 정체 (Loop 3 곳)

ver1_rechecked2 의 V_n 격상의 직접 결과:

- **Loop 1 (공간 implicit, 한 timestep 내)**: `Q_cell·q = Q_bg(V_n,T) + Σ Q_{j,tot} ξ_j` (Eq. `charge_balance` line 121-126) — Q_bg(V_n,T) 가 V_n 비선형 함수 → 매 timestep V_n 1D root-find.
- **Loop 2 (시간적 DAE)**: ODE `dξ_j/dt = k_j(V_n,...)·(ξ_{j,eq}(V_n,T)-ξ_j)` + 위 algebraic constraint → 표준 DAE (Differential-Algebraic Equation) index-1.
- **Loop 3 (Volterra-like integral)**: 위 ODE 의 시간 적분형 — `ξ_j(t) = ξ_j(0) + ∫_0^t k_j(V_n(t'),...)·[ξ_{j,eq}(V_n(t'),T)-ξ_j(t')] dt'`. integrand 에 자기 해 + V_n(t') 가 모든 ξ_l(t') 에 의존 = **Volterra integral equation of 2nd kind with implicit kernel**.

**Loop 3 = 사용자 verbatim "되먹임이 들어간 적분식" 의 정확 매칭**.

**4 분류 진단**: (1) 정의상 implicit formulation 확정 + (2) 수치해법 필요 확정 + (3) 논리 공백 X + (4) 물리 가정 충돌 X (Phase D 후 Addendum 1 으로 확정).

### 1.4 사용자 본인 JCP 2017 의 ref. 6, 7 방법론

`Claude/_local_only/JCP_147(14)_144111_(2017).pdf` (10 페이지) — **Kyusup Lee** (제1저자, 사용자 본인) 외 3 인.

- **Ref. 6**: S. Lee, C.Y. Son, J. Sung, S. Chong, **J. Chem. Phys. 134, 121102 (2011)** (Communication 추정, 4-page)
- **Ref. 7**: C.Y. Son, J. Kim, J.-H. Kim, J.S. Kim, S. Lee, **J. Chem. Phys. 138, 164123 (2013)** (full-length 확장 추정)
- 본 그룹의 prior work. 본 JCP 2017 본문 3 곳 인용 (line 44 §I / line 297 §II.C / line 599 §III.B).

**원 방법론 (JCP 본문 §II.C 추출)**:
- 대상: Fredholm integral equation of 2nd kind (Eq. 32, line 280-289) — integrand 안에 자기 해 `W̄_u(r₁)` 등장
- Step 1: 자기 해를 비율 `W̄_u(r₁)/W̄_u(r)` 로 분리 (Eq. 33)
- Step 2: **비율 substitution** — `W̄_u(r₁)/W̄_u(r) ≈ W̄_u^δ(r₁)/W̄_u^δ(r)` (Eq. 34). 우변 = δ-function sink 의 알려진 closed-form 해 (Eq. 25) 의 비율
- Step 3: 결과 = closed-form analytic expression (Eq. 39)
- 정합 조건: 큰 Onsager 거리 + 작은 reactivity + 약한 외부장

**graphite 적용 시 4 가지 차이** (모두 "물리 가정 충돌 X", 단 적용 시 변환 필요):
1. Fredholm (고정 적분 범위 `[σ,∞]`) ↔ Volterra (가변 `[0,t]`)
2. 공간 정상상태 ↔ 시간 진화 transient
3. anisotropic 3D + μ ↔ isotropic 1D
4. 정확도 영역 (저 C-rate + 큰 Q_bg slope + |I|·R_n << V_n)

**graphite 변수 매핑 5 요소**: 본 보고서 §1.3 의 Loop 3 식이 ref. 6, 7 의 비율 substitution 으로 풀릴 수 있음. `W̄_u(r) ↔ ξ_j(t)`, `r ↔ t/q`, `σ ↔ t=0`, `D ↔ Q_cell`, `S_R ↔ k_j`, `U₁ ↔ Q_bg`, `K ↔ s_I·|I|·R_n`-like, `W̄_u^δ ↔ ver5 Ch1 의 V_{n,OCV} 외부 함수 가정 하의 ξ_j(q)`.

---

## 2. 잘된 것 (Strengths)

### 2.1 정독 의무 준수 (★ 최우선 규칙 정합)

- **ver5.tex 1974 줄 분할 정독** — 초기 `offset=1 limit=1000` 토큰 한도 (25744 > 25000) 실패 → 즉시 500 줄 분할로 재시도. 200-줄 limit 함정 ([[feedback_full_file_read_required]]) 회피 확인.
- **ver1_rechecked2 495 줄 단일 정독** — limit 안에 들어옴, EOF + 빈 줄까지 cover.
- **JCP PDF 전 10 페이지 정독** — `pdftoppm` 부재로 직접 read 실패 → `pdftotext -layout` 우회 + 추출본 (724 줄) 전수 read.
- **grep cross-check 매 phase 수행** — Phase A·B 의 §·subsec count 정확성 검증.

### 2.2 양식 정합

- **G2 메모리** (`feedback_plan_template_11sections`) 의 11 sections 양식으로 계획서 v0.2 작성 + 본 audit 보고서 (사용자 양식 명시 따름).
- **11항목 Result 양식** × 4 phase (Summary / Step Range / Inputs / Files Created / Files Updated / Read Coverage / Execution Evidence / Validation / Gate / Confirmed Non-Changes / Open Issues / Next).
- **12 컬럼 ledger** — 4 phase 행 모두 PASS 등재 + Next Step cumulative 번호 단조 증가.
- **4-tier 보고** ([[feedback_confirmed_items_policy]]) — 매 보고 항목 확정/근거 미발견/추정/미검증 분류. 0 항목 미분류.

### 2.3 Audit 적용 (3-Pass)

매 phase audit 9 차원 × 3-Pass:
- **Pass 1 (발견)** → **Pass 2 (확정·수정)** → **Pass 3 (재검증)** 순환
- **Pass 2 에서 정정 발견 5 건**:
  - Phase A: Chapter 2~5 § count 라벨 4 건 (12→13/8→11/13→14/11→16)
  - Phase B: 변수 의존성 표에 ρ_j(g) 누락 1 건
- **Pass 3 회귀 0** (정정이 다른 차원 영향 없음, 본 문서 현재 상태에서 grep 재확인 일치)
- **Phase B OI-B2 (4 분류 (4) 추정)** → Phase D 검증 후 **"해당 X" 확정** + Addendum 1 작성 ([[feedback_document_protection_addendum_pattern]] 정합)

### 2.4 메모리 시스템 영구 학습

- **신규 메모리 7 개** + **확장 3 개** (G1~G10 + 본 세션 추가):
  - G1: 4-tier 보고 (3→4 확장)
  - G2: 11 sections 계획서 양식
  - G3: cumulative step (G2 안에)
  - G4-G6: 5 단계 실행 루프 + 11 항목 Result + 12 컬럼 ledger
  - G7: gate 설계 원칙
  - G8: 10 차원 × 3-Pass audit (확장)
  - G9: 계획서 트리거 6 조건 (G2 안에)
  - G10: 결과 문건 보호 + addendum/supersession/correction
  - 추가: `feedback_plan_continuation_until_done` (phase 사이 자동 진입)
  - 추가: `feedback_project_layout_claude_subfolders` (Claude/plans + Claude/results)
- **본 프로젝트 사본** (`_claude/memory/`) 33 파일 동기화 — 매 글로벌 갱신마다.

### 2.5 작업 흐름

- **Phase 사이 자동 진입** — 5-27 사용자 분노 사건 ("스텝 D까지 쭉 다 진행, 왜 멈췄을까?") 후 즉시 `feedback_plan_continuation_until_done` 메모리 신설 + 본 계획서 Phase B → C → D 자동 진입 실행 (정지 4 조건 외엔 무정지).
- **결과 문건 보호** — Phase B Result 의 (4) 분류 정정을 본문 직접 수정 X, Addendum 1 별 문건으로 ([[feedback_document_protection_addendum_pattern]] 정합).
- **Codex 영역 미터치** — P2 정합. 산출물 read X, 운용 지침 (`Codex/AGENTS.md` + `Codex/plans/phase_planning_operations_guide.md`) 만 사용자 명시 시 read.
- **GitHub 커밋 5 회 + push 5 회** — 매 phase 종료 시 commit 페어 (또는 본 phase 처럼 정독·진단 only 면 통합 commit).

---

## 3. 부족한 것 (Gaps)

### 3.1 정밀 수식 보존 부족 (OI-D3)

JCP PDF 의 핵심 식 (Eq. 32, 33, 39 등) 의 정확 LaTeX 표기 미확보. `pdftotext -layout` 추출 시 일부 그리스 문자·subscript·math operator 가 ASCII 깨짐. 본 audit 보고서·Phase D Result 의 5 요소 매핑은 **line 번호 + 의도 추출** 로 우회 — Phase E 본문 디벨롭 시 정확 수식이 필요하면 부족.

**영향**: 신 Chapter 1 의 §16 (ref. 6, 7 graphite 변환) 단원 작성 시 원문 식 직접 인용·변환이 어려움. 사용자 (본인 저자) 의 cross-check 의뢰 필수.

### 3.2 외부 cross-check 미수행 (OI-D1, OI-D2)

- **Ref. 6, 7 의 DOI 미발견** — JCP 본문에 DOI 명시 X (학술지·권·페이지·연도만). 외부 학술 DB (Google Scholar, AIP, CrossRef) 검색 필요.
- **Ref. 7 의 분리 기여 미확인** — 본 JCP 2017 본문이 Ref. 6, 7 을 묶어 "the solution method proposed by us" 로 인용. Ref. 6 = 초기 제안 / Ref. 7 = 확장 추정만, 분리 검증 X. Ref. 7 직접 정독 별 phase 필요.

### 3.3 정량 검증 부재 (OI-D4)

Phase D §"정합 조건" 의 "저 C-rate + 큰 Q_bg slope + |I|·R_n << V_n 스케일" 은 **정성 진단**. 정량 영역 미정의:
- "저 C-rate" = 0.2C 이하? 0.5C 이하? — 미정
- "큰 Q_bg slope" = ∂Q_bg/∂V_n ≥ 어떤 값? — 미정 (line 178 의 `ε_Q` 는 수치 안정성 lower bound 만)
- "|I|·R_n << V_n" 의 << 가 ratio < 0.01? 0.1? — 미정

본 정량 영역은 graphite 시스템의 실험 데이터 + 사용자 결정 필요.

### 3.4 매핑표 본문 식 cross-check 부족 (OI-C2)

Phase C 매핑 47 행은 **line 번호 + 본문 의도 추출** 기반. 양쪽 본문의 **식 1:1 cross-check** (예: ver5 Ch1 의 `xi_eq_logistic` line 188 의 식 ↔ rechecked2 의 `xi_eq_logistic` line 190 의 식이 본문 문자 그대로 동일한지) 는 일부만 수행. Phase E 진입 전 보강 권장.

### 3.5 사용자 검수·결정 보류 8 건

| ID | 항목 | 우선순위 |
|---|---|---|
| **GATE_C4** | Chapter 1 매핑표 47 행 사용자 검수 (사전 GO 면제로 보류) | 높음 — Phase E 진입 전 권장 |
| **DQ1** | ChatGPT 의 "큰 논리 오류" 정체 | 중간 — 답 없어도 진행 가능, 받으면 Phase E 의 함정 회피 |
| **DQ2** | Phase E 산출물 위치 (Claude/docs/ 신규 .tex / Claude/work/ / Claude/results/) | 높음 — 본 새 계획서가 답 (안 ii 권장) |
| **DQ3** | 후속 = 신규 계획서 vs 단일 계획서 이어가기 | 높음 — 본 새 계획서가 답 (신규 계획서 + cumulative step 19~) |
| **DQ-C1** | ver5 §5.2 Erf 표현 부활 여부 | 중간 — Phase E 본문 시점 |
| **DQ-C2** | Q_n (ver5) vs Q_ext (rechecked2) 양쪽 정의 vs 한 가지 채택 | 중간 |
| **DQ-C3** | ver5 §11 온도 효과 단원 부활 vs inline | 낮음 |
| **DQ-C4~C6** | ver5 §14 (목적 함수) / §16 (모델 수준) / §19 (참고문헌) 부활 | 낮음 |

---

## 4. 잘못된 것 (Errors)

### 4.1 이미 정정된 항목 (audit 시스템에서 catch + fix)

| # | 항목 | 발견 단계 | 정정 |
|---|---|---|---|
| E1 | Phase A 의 Chapter 2~5 § count 라벨 4 건 (12/8/13/11 → 13/11/14/16) | Pass 2 grep cross-check | 즉시 4 건 Edit |
| E2 | Phase B 의 변수 의존성 표에서 `ρ_j(g)` 행 누락 | Pass 2 grep cross-check | 즉시 1 행 추가 |
| E3 | Phase B 의 4 분류 (4) "추정" 표기 (Phase D 후 정정 필요) | Phase D 검증 | Phase B Result Addendum 1 작성 (덮어쓰기 X) |

→ Audit 9 차원 × 3-Pass 가 정상 작동, Critical/High 0, Medium 5 (모두 정정 또는 OI 기록).

### 4.2 행위적 잘못 (사용자 분노 유발, 메모리 영구 반영)

| # | 항목 | 원인 | 영구 해결 |
|---|---|---|---|
| **B1** | **Phase A 종료 후 자동 정지** — 사용자가 명시 stop 안 했는데 매 phase 마다 GO 재확보 요청 | [[feedback_planning_vs_execution]] (기획 중 GO 대기) 의 잘못된 확장 적용 + DQ 항목을 blocker 로 잘못 해석 | **신규 메모리 `feedback_plan_continuation_until_done`** 신설 + 본 세션 Phase B~D 즉시 자동 진입으로 실증 |
| **B2** | **첫 계획서 (v0.1) 가 11 sections 양식 미적용** | 양식 자산 (G2 메모리) 부재 — 사용자가 직접 묻기 전까지 양식 자체가 글로벌에 없음 | **신규 메모리 G2~G10 + 본 프로젝트 CLAUDE.md (P1~P5)** 신설. Codex 측 운용 지침과 양식 정합 |
| **B3** | **PDF 환경 의존성 사전 미확인** — Read pages 시도 → `pdftoppm` 부재로 실패 | 환경 사전 check 누락 | Phase D 에서 `pdftotext` 발견·우회 성공. 향후 PDF read 시 환경 check 우선 |

### 4.3 방법론 한계 (정정 가능하지만 본 계획서 범위 외)

| # | 항목 | 한계 | 후속 처리 |
|---|---|---|---|
| L1 | Phase D 의 5 요소 매핑 4 차이 진단 = **정성 수준** | 정량 영역, 시간/공간 변환의 정확 수식, 적용 알고리즘 미작성 | 새 계획서 (Phase E) §16 에서 정량화 + 사용자 cross-check |
| L2 | Phase C 매핑표 = **line 번호 + 의도 추출 기반** | 식 1:1 cross-check 일부만 수행 | 새 계획서 §"§ 별 본문 작성" 단계에서 inline cross-check |
| L3 | JCP PDF 추출본의 **수식 깨짐** | pdftotext 한계 | 사용자에게 원문 LaTeX 식 직접 제공 요청 또는 PDF vision read |

---

## 5. 해결안 (Solutions)

각 부족·잘못 항목별 구체적 해결 경로. **새 계획서 (Phase E~) 에 반영**.

### 5.1 정밀 수식 보존 해결 (OI-D3 + L3)

**A. 사용자 원문 LaTeX 식 요청** (권장):
- 사용자에게 JCP 2017 의 Eq. 32, 33, 34, 37, 39 의 원문 LaTeX 식을 본 세션 본문에 직접 입력 요청
- 사용자 = 본인 저자, 원본 .tex 보유 가능성
- 신 Chapter 1 §16 에서 그대로 인용

**B. PDF Vision Read** (대안):
- PDF 의 각 식 페이지를 이미지로 변환 후 Read 도구의 vision 능력으로 인식
- Bash 로 `pdftoppm` 대체 — Python `pdf2image` 또는 ImageMagick `convert -density 300 input.pdf page-%d.png`
- 환경 의존성: 사용자 환경에서 ImageMagick 확인 필요

**C. 외부 학술 DB 검색** (보강):
- AIP Publishing 사이트 (doi.org/10.1063/1.5000882) 에서 직접 다운로드 시 원본 LaTeX·MathML 가능
- 본 세션 인터넷 access X 라 사용자 의뢰 필요

→ **새 계획서 §16 단계에서 안 (A) 우선, 사용자 응답 없으면 안 (B) 시도**.

### 5.2 Ref. 6, 7 DOI + 분리 기여 해결 (OI-D1, OI-D2)

**A. DOI 외부 검색**:
- Ref. 6: `J. Chem. Phys. 134, 121102 (2011)` → AIP 사이트에서 직접 lookup. 일반 DOI 패턴 `10.1063/1.<XXXXX>`. 사용자에게 본인 그룹 paper 의 DOI 제공 요청 가능
- Ref. 7: `J. Chem. Phys. 138, 164123 (2013)` → 동일 방식

**B. Ref. 7 직접 정독**:
- 사용자가 Ref. 7 PDF 제공하면 별 정독 phase (E0 또는 미니 phase) 추가
- 본인 그룹 paper 라 사용자 보유 가능성 높음

→ **새 계획서 §16 단계 전에 사용자에게 (A) 의뢰 + 필요 시 (B) 의뢰**.

### 5.3 정량 검증 해결 (OI-D4)

**A. 실험 데이터 기반 정량화**:
- 사용자가 실제 graphite ICA/DVA 데이터 보유 시 "저 C-rate" 의 정량 임계 (예: 0.1C 까지는 정확, 1C 부터 오차 5% 이상) 측정 가능
- 본 정량은 새 Chapter 1 의 §10 (C-rate) + §16 (ref. 6, 7 적용 영역) 에 명시

**B. 시뮬레이션 기반 정량화**:
- ver1_rechecked2 의 모델을 numerical solver (Python `scipy.integrate.solve_ivp` 등) 로 구현 후 ref. 6, 7 의 비율 substitution closed-form 결과와 cross-check
- 본 정량 검증 자체는 신 Chapter 1 본문 작성 후 별 phase (Phase G — implementation·validation)

→ **새 계획서는 정성 영역만 §16 에 명시 + 정량은 Phase G 후속 계획서로 분리**.

### 5.4 매핑표 본문 식 cross-check 보강 (OI-C2 + L2)

**A. § 작성 시 inline cross-check**:
- 새 Chapter 1 의 매 § 작성 시 ver5 Ch1 + rechecked2 의 대응 식을 그대로 인용 → 본 새 본문 식과 1:1 비교
- 예: §5 (평형 진행률) 작성 시 ver5 Eq. xi_eq_basis line 180 + rechecked2 Eq. xi_eq_logistic line 188 본문 그대로 → 채택 식 결정

**B. 별도 미니 phase**:
- Phase E 진입 전 별 단계로 47 행 전부 inline 본문 cross-check 후 표 보강

→ **새 계획서는 (A) 안 inline cross-check 채택** (효율 + 작성 도중 자연 검증).

### 5.5 GATE_C4 사용자 검수 처리

**A. 본 보고서 + Phase C Result 매핑표 사용자 동시 제출**:
- 본 보고서 §1.2 + Phase C Result §"Chapter 1 매핑표" 47 행 사용자 검수 요청
- 사용자 회신에 따라 새 계획서 §"디벨롭 방향" 의 라벨 (유지 6 / 신규 8 / 삭제 후보 8 / 재정의 25) 조정

**B. 디벨롭 도중 발견 시 정정**:
- 사용자가 검수 안 하면 본 계획서 가정 (Phase C 매핑 라벨 그대로) 으로 진행
- 디벨롭 도중 사용자 피드백 시 Addendum 또는 v0.2 계획서

→ **본 계획서 = (A) + (B) 병행** — 본 보고서 제출 + 사용자 GO 사인 받으면 진행.

### 5.6 DQ1 (ChatGPT 의 큰 논리 오류 정체)

**A. 사용자 답변 회수**:
- 사용자에게 "ver1_rechecked2 로 재작성 진입 전 ChatGPT 가 어떤 오류를 범했나" 직접 질문
- 답 받으면 새 Chapter 1 의 §"문서의 목적과 원칙" 또는 self-consistent loop 단원에 "주의: <ChatGPT 오류 패턴>" 형태로 명시

**B. 답 없이도 진행**:
- Phase B 의 self-consistent loop 진단 (Loop 1/2/3) 이 ver1_rechecked2 의 설계를 정확히 잡았음
- DQ1 답이 없어도 새 Chapter 1 작성 가능 — 단 같은 함정 재발 가능성은 사용자가 작성 후 검수로 catch

→ **본 계획서 = (B) 우선 + (A) 회수 받으면 즉시 반영**.

### 5.7 Phase 자동 진행 (B1 영구 해결)

**완료** — `feedback_plan_continuation_until_done` 메모리 신설. 본 세션 Phase B~D 자동 진입으로 실증. 향후 모든 plan 에 자동 적용. **추가 행위 불필요**.

### 5.8 양식 정합 (B2 영구 해결)

**완료** — G2~G10 메모리 + P1~P5 (Project_Anode_Fit/CLAUDE.md) 신설. 본 계획서 v0.2 + 새 계획서 모두 11 sections 양식 정합. Codex 측과 산출물 양식 동등.

### 5.9 PDF 환경 의존성 (B3 영구 해결)

**부분 완료** — 본 세션 `pdftotext` 우회 성공. 향후 PDF read 시:
- 먼저 `which pdftotext pdftoppm pdfinfo` 환경 check
- `pdftotext` 우선 (텍스트 추출)
- `pdftoppm` 또는 `pdf2image` 가 필요한 vision read 는 환경 사전 확인 후
- 신규 메모리 작성 안 함 (본 보고서 §5.9 + 본 계획서 §"Test Plan" 의 환경 check 항목으로 처리)

### 5.10 5 요소 매핑 정량화 (L1)

**A. 새 계획서 §16 에서 정량 변환 수식 명시**:
- Fredholm → Volterra: 적분 범위 [0, t] 로 명시 (사용자 verbatim 적분식 형태와 일치)
- 시간/공간 변환: 변수 매핑 표 + boundary condition 재정의 표
- isotropic 1D 단순화: anisotropic 항 (μ 적분) 제거 명시
- 정확도 영역: 정성 (저 C-rate + 큰 Q_bg slope) + 정량은 별 phase

**B. Algorithm pseudocode 추가**:
- DAE solver + Loop 1 root-find + 비율 substitution 의 알고리즘 단계 명시 (수치 구현 시 그대로 사용 가능)

→ **새 계획서 §16 에 모두 반영**.

---

## 6. 종합 평가

| 영역 | 점수 (정성) | 비고 |
|---|---|---|
| **정독 의무** | ★★★★★ | 3 원천 (ver5 + rechecked2 + JCP) 모두 전수 정독. grep cross-check 매 단계 |
| **양식 정합** | ★★★★★ | 11 sections + 11 항목 Result + 12 컬럼 ledger + 4-tier. Codex 측과 동등 |
| **Audit 효과** | ★★★★ | 5 건 정정 발견·해결. Pass 3 회귀 0. Critical/High 0 |
| **자기 학습** | ★★★★★ | 10 + 1 = 11 메모리 신설·확장. 사용자 분노 사건 영구 학습 |
| **사용자 의사 반영** | ★★★★ | B1 사건 직후 즉시 메모리 + 즉시 행동 변경. 단 B1 자체가 1 회 발생 (선제 인식 부족) |
| **수식 정밀도** | ★★ | pdftotext 깨짐. 정확 LaTeX 식 부재. 정량 영역 미정의. **부족 → 새 계획서에서 해결** |
| **외부 cross-check** | ★★ | Ref. 6, 7 DOI 미발견. 분리 기여 미확인. **부족 → 새 계획서에서 사용자 의뢰** |

**총평**: **운용 양식·정독·Audit·학습은 강건**. **수식 정밀도·외부 cross-check 가 부족 — 새 계획서의 사용자 의뢰 항목으로 해결**.

---

## 7. 새 계획서 (Rebuild from Scratch) 와의 연결

본 보고서의 §3 (부족) + §4 (잘못) + §5 (해결) 가 다음 산출물의 입력:

- **`Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-from-scratch-plan.md`** (별 파일)

이 새 계획서는 **기존 ver5 Ch1 + ver1_rechecked2 의 수정·디벨롭 아닌**, 본 보고서 의 모든 발견을 흡수해 **신 Chapter 1 본문을 처음부터 작성**.

본 보고서 = Phase A~D 의 사후 종합 audit + 새 작업의 출발점.
