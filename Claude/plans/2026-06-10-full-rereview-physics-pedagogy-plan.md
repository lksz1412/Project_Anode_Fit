# Ch1·Ch3·Ch4 전면 재검토 — 절별 재작업 수준 (물리 논리 + 교과서 해설) + 10회 재검토 Plan

## Summary
박사님 지시(6-10, 모델 교체 직후): 지금까지의 작업 방식 그대로 **처음부터 전면 재검토**. 대상 = 활성 3개 챕터(`graphite_ica_ch1.tex` 병합 단일 챕터 / `ch3` 발열 / `ch4` 반응속도론). 방식 = **절별·챕터별 재작업 수준** — 각 절을 (a) **전문 생략 없이 정독**(왜곡·누락 대비), (b) **수식 전개의 물리적 논리 결함 파악·수정**, (c) **교과서 수준으로 더 쉽게 설명하기 위한 해설 타당성 검토**(어려운 개념은 비유가 아니라 전제가 되는 쉬운 개념부터 단계적 전개 — 글로벌 지침 §3; 해설 추가 시 앞 도입·뒤 사용 완결, orphan 0). **절대 금지: 기존 본문을 그대로 두고(복붙) "검토 완료" 처리** — 무수정 절도 절별 result 에 "왜 무수정인지" 정독 근거를 남겨야 PASS. 본작업 1회 후 **동일 방식 10회 재검토**, 매 라운드 종료마다 커밋+푸쉬. 박사님 출근으로 실시간 피드백 불가 → **본 계획서 승인(GO) 후 전 작업 무중단 자율 진행**(팝업 0, 질문은 완료 보고 시점에 일괄).

## Current Ground Truth
- 원천(전문 정독 대상): `Claude/docs/graphite_ica_ch1.tex` **1626행/18절/34p** · `graphite_ica_ch3.tex` **479행/11절/9p** · `graphite_ica_ch4.tex` **323행/8절/6p**. 전부 빌드 0/0(overfull 0·undefined 0), 직전 커밋 `246022a`(10-round 논리검수 완료, ~50건→3건 수렴).
- 의존 트리: **Ch1(병합: 평형·동역학·히스) → Ch3(발열)·Ch4(반속)**. Ch3/Ch4 는 Ch1 식번호를 텍스트로 인계(현재 .aux 대조 일치: relax 1.20·eyring 1.21·Lq 1.23·affinity 1.27·bv 1.28·db 1.29·ΔU_hys 1.48·U_center 1.49 등). **Ch1 에 식이 추가/삭제되면 Ch3/Ch4 재매핑 의무.**
- 직전까지의 검수는 **논리 결함 중심**(부호·정의역·식별성·내부모순). **이번에 새로 들어가는 렌즈 = 교과서 해설 타당성**(독자가 따라올 수 있는 단계 전개인가) — 이 렌즈로는 아직 한 번도 체계 검수한 적 없음(미검독 영역).
- 작업트리: ch3/ch4 pdf 재빌드 변경분(무해) + 무관한 staged 삭제 다수(아카이브 정리 흔적) — **후자는 절대 커밋에 포함하지 않음**(명시 스테이징만).
- 통제 문건: 글로벌 `~/.claude/CLAUDE.md` + 프로젝트 `CLAUDE.md`(P1~P5; V_n/V_app/V_drive/V_OCV 일관 등 검수 7항목) + ★메모리(절별 루프·복붙 금지·댕글링 금지·단일문건 규율·GO 후 연속·auto commit+push). **매 챕터 시작 전 프로젝트 CLAUDE.md + ★메모리 재확인, 매 절 시작 전 Implementation Interfaces 의 절별 체크리스트 적용**(박사님 6-10 지시 반영).

## Phase Range
| Phase | 이름 | Steps | 산출 |
|---|---|---:|---|
| 1.1 | Ch1 사전점검(지침·메모리 재확인, 절 목록·기준선) | 1–3 | 체크리스트 확정 |
| 1.2 | Ch1 PART A 절별 재작업(서론~겹침, 11절) | 4–14 | 절별 수정+빌드 |
| 1.3 | Ch1 PART B/C 절별 재작업(DVA~검증, 7절) | 15–21 | 절별 수정+빌드 |
| 1.4 | Ch1 챕터 게이트(빌드·인계 재매핑·result·커밋푸쉬) | 22–24 | RESULT+커밋 |
| 3.1 | Ch3 사전점검(+Ch1 변경분 인계 대조) | 25 | 〃 |
| 3.2 | Ch3 절별 재작업(서론~종합식, 11절) | 26–36 | 〃 |
| 3.3 | Ch3 챕터 게이트 | 37–38 | RESULT+커밋 |
| 4.1 | Ch4 사전점검(+인계 대조) | 39 | 〃 |
| 4.2 | Ch4 절별 재작업(8절) | 40–47 | 〃 |
| 4.3 | Ch4 챕터 게이트 | 48–49 | RESULT+커밋 |
| R.1~R.10 | 재검토 10회(각 라운드 = 3챕터 절별 전문 정독 재검수→수정→빌드→**커밋+푸쉬**) | 50–69 | 라운드별 ledger+커밋 10개 |

step 번호는 phase·챕터 무관 단조 누적(1→69).

## Non-goals
- **삭제·덮어쓰기 금지**(박사님 명시): 파일 삭제 X, 기존 results/plans/handover/`old/`/`Archive_*` 덮어쓰기 X(정정은 Addendum 별도 문건), `Codex/` read/write X. 작업트리의 기존 staged 삭제들 커밋 포함 X.
- 절 삭제·장 구조 재편 X(추가·수정만). 확정 물리 발명 X — 수정은 근거(재유도·극한·차원·반례) 있는 결함과 해설 보강만.
- **Workflow 도구 X**(ultracode 기본값보다 상시 지시 우선), **AskUserQuestion/EnterPlanMode 등 팝업 X**. 멀티에이전트 필요 시 Agent 도구만.
- 챕터 통째 배치 Write/Edit X(절 단위). 절마다 사용자 확인 X(GO 후 끝까지 연속).
- 인계 식번호·라벨 임의 변경 X(식 추가 시에만 라벨 기준 재매핑).

## Implementation Changes
- 수정: `Claude/docs/graphite_ica_ch1.tex`(+pdf) · `graphite_ica_ch3.tex`(+pdf) · `graphite_ica_ch4.tex`(+pdf).
- 신규: 본 계획서 · `Claude/results/PHASE_FRR_EXECUTION_LEDGER.md`(12-col) · `PHASE_FRR_ch1_RESULT.md` · `PHASE_FRR_ch3_RESULT.md` · `PHASE_FRR_ch4_RESULT.md`(각 11항목, Read Coverage 행범위 명시) · `PHASE_FRR_ROUNDS_RESULT.md`(R.1~R.10 라운드별 append — 본 세션 신규 문건이라 append 는 덮어쓰기 아님).
- 기존 문건 무수정(보호): 이전 PHASE_* results/ledgers, 이전 plans.

## Phase 1.1 — Ch1 사전점검
- **Step 1.** 프로젝트 CLAUDE.md(P1~P5)·★메모리(절별루프·복붙금지·댕글링·단일문건·의존트리) 재확인, 절별 체크리스트(Implementation Interfaces) 확정. **Step 2.** ch1 18절 목록·행범위 추출, ledger 골격 생성. **Step 3.** 기준 빌드(0/0)·.aux 인계 번호 스냅샷.
- Gate G1.1: 체크리스트·ledger·스냅샷 존재(파일로 확인 가능).

## Phase 1.2 / 1.3 — Ch1 절별 재작업 (PART A: 서론·기호·전하보존·평형peak·정규용액·동역학·유효배리어·통계·분포·종합·겹침 / PART B·C: DVA·분기·분기dQdV·분극·부분cycle·master·검증)
- 각 절(= 한 step) 공통 루프: ① 해당 절 **전문 정독**(head→tail, 행범위 기록) → ② **물리 논리**: 모든 유도 손 재유도·부호/차원/극한/정의역 검산, 결함은 수정 → ③ **해설 타당성**: 단계 비약(전제 없이 결론) 지점 식별, "전제 개념→단계 전개" 해설 보강(비유 의존 X, 분량 패딩 X — 모든 추가는 앞 도입·뒤 사용 확인) → ④ 절 단위 빌드(2-pass) → ⑤ 앞 절·(Ch3/4 작업 시 Ch1) 정합 확인 → ⑥ ledger 행 + 절별 기록(수정 요지 또는 **무수정 사유**). 다음 절로 자동 진행(중단 없음).
- Gate G1.2/G1.3: 전 절 ledger 에 정독 행범위 + 수정/무수정 근거 기록(빈 칸 0), 빌드 0/0.

## Phase 1.4 — Ch1 챕터 게이트
- **Step 22.** 전체 2-pass 빌드, overfull/undefined 0, 단일문건 규율 grep(인계 recap/transmit/결론 절 0). **Step 23.** .aux 인계 번호 스냅샷 대조 — 변동 시 Ch3/Ch4 본문 재매핑(플레이스홀더 방식)+재빌드 undef 0. **Step 24.** `PHASE_FRR_ch1_RESULT.md`(11항목) 저장 → 명시 스테이징 커밋+푸쉬.
- Gate G1.4: result 존재 + 커밋 해시 기록. (result 저장 없이 Ch3 진입 금지.)

## Phase 3.1~3.3 — Ch3(발열) / Phase 4.1~4.3 — Ch4(반속)
- Ch1 과 동일 루프. 추가 점검: Ch1 인계 식번호 텍스트 전수 대조(P3-6), 발열 3분해(q_rev/q_hys/q_pol)·반속 detailed balance 의 Ch1 정합, V_n/V_app/V_drive 표기 일관(P3-1). 각 챕터 종료 시 result+커밋푸쉬.

## Phase R.1~R.10 — 재검토 10회
- 각 라운드(= 2 steps: 검수·수정 / 검증·커밋푸쉬): 3챕터를 절 그룹으로 나눠 **전문 정독 재검수**(Agent 병렬, 각 그룹 head→tail, 간결 확정결함만·빈통과 금지·refute) — 렌즈 = 물리 논리 + 해설 타당성 + **직전 라운드 수정이 들인 새 결함**. master 가 적발 건 삼각검증 후 직접 수정 → 3챕터 빌드 0/0 → ledger 라운드 행 + `PHASE_FRR_ROUNDS_RESULT.md` append → **커밋+푸쉬**. 라운드 간 무중단.
- 수렴해도 10회 모두 수행(박사님 명시 횟수). 후반 라운드는 "남은 확정 결함 없음(수렴)" 보고도 유효하나 전문 정독 후에만.
- Gate G-R.k: 라운드 커밋 해시 + 결함 수 기록.

## Implementation Interfaces
- **절별 체크리스트**(매 절 적용): (1) 전문 정독 행범위 기록 (2) 유도 손검(부호·차원·극한·정의역) (3) V_n/V_app/V_drive/V_OCV 구분 (4) 해설: 새 개념이 전제 없이 등장하는가 → 전제부터 단계 전개로 보강 (5) 추가분 앞 도입·뒤 사용(orphan 0) (6) 단일문건 규율(타 챕터 recap/transmit 0) (7) 인계 식번호 보존 (8) 수정/무수정 사유 한 줄.
- Ledger 12-col 표준. Result 11항목 표준(Read Coverage 필수). 커밋: 내 작업물만 명시 스테이징(`git add <경로들>`), attribution 없음, 매 커밋 즉시 push(`rb-rebuild-2026-05-30`).
- 해설 보강 문체: 본문 한글 prose + 학술 용어 영어 원어, 비유 금지·전제 개념 단계 전개, 수식 깨짐 빌드로 확인.
- 식 추가 시 번호 재매핑 절차: 구 .aux 스냅샷 ↔ 신 .aux 라벨 대조 → Ch3/Ch4 `(1.x)` 텍스트 플레이스홀더 치환 → 재빌드 undef 0.

## Test Plan
- 절/챕터/라운드 단위 `xelatex -interaction=nonstopmode -halt-on-error` 2-pass — overfull 0·undefined 0(확인 가능 출력 인용).
- .aux 인계 번호 전수 대조(ch1 스냅샷 ↔ ch3/ch4 본문 grep) — 식별자별 일치 기록.
- 규율 grep: 본문 "Chapter"·"앞 장"(병합 후 ch1 은 단일 장) recap·transmit 표현 0, 인라인 변경이력 라벨 0.
- 정독 증명: 각 절 result/ledger 에 행범위. 무수정 절도 행범위+사유 필수(복붙-완료 방지 gate).
- 해설 보강 검증: 추가 단락마다 (앞 도입 위치, 뒤 사용 위치) 쌍 기록 — 한쪽이라도 없으면 trim.
- 라운드 검증: 결함 수 추이 기록(수렴 곡선), 각 라운드 커밋 해시.

## Assumptions
- A1: 대상 = ch1+ch3+ch4 전부("챕터별" 지시의 포괄 해석; ch3/ch4 는 해설 렌즈 미적용 상태라 포함이 안전).
- A2: "삭제·덮어쓰기 금지"는 파일·기존 결과문건 차원 — .tex 본문의 결함 수정·해설 보강(Edit)은 승인된 작업 범위(박사님 "그 외 작업 권한 승인"). 단 기존 정확 문장의 불필요한 재서술은 안 함(증분 수정).
- A3: 10회 재검토의 "동일한 방식" = 절별 전문 정독 루프(R8 식 fresh 적대검수 포함). Codex 적대검수는 박사님 명시 호출 없으므로 본 계획에선 Agent 검수로 수행(허용돼 있으나 횟수·비용 자율 판단).
- A4: 작업 중 중대 구조 결정(절 신설 필요 등)이 나오면 — 신설은 수행하되(추가는 허용) Open Issues 에 근거 기록, 삭제성 결정은 보류 후 완료 보고에 질문.

## Decisions Required
- 없음 — 본 계획서 GO 만 필요. GO 후 Phase 1.1→R.10 까지 무중단 자율 진행(정지 5조건: Decision Gate/새 의존성/FAIL gate/사용자 stop/통제문서 모순→더 제한적 채택). 질문은 완료 보고에 일괄.

## Correction History
- 2026-06-10 신규. 직전 10-round 논리검수(`PHASE_LOGIC_REVIEW_10ROUNDS.md`, ~50→3 수렴)와 구분: 이번은 (1) 모델 교체 후 전면 fresh 재검, (2) **해설 타당성(교과서 접근성) 렌즈 신설**, (3) ch3/ch4 포함 전 챕터, (4) 복붙-완료 금지 gate(무수정 사유 의무) 명문화, (5) 본작업+10회 재검토 각 커밋푸쉬.
