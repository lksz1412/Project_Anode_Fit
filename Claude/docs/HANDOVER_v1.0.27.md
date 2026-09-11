# HANDOVER_v1.0.27 — v1.0.27 arc 인계(진행 중 판 · 매 Step/Phase 종료·중단 시 갱신)

> 최종 갱신 = 2026-09-11 · master Fable 5.1 · 상태 = **Phase 1.1 Step 1 — 검수 R5 확정결함 1(stem 인용 `KNOWN_DEFECTS`) 반영한 iter_6 적용 · 계획서 v5.6(흑연 우선 재배열·모델 경계)·v5.7(발췌독 원칙·R6 단독 수렴 예외)·v5.8(읽기 범위 실행 규칙) ·v5.9(R6 반영) · **검수 R6 확정결함 0 → Step 1 수렴(사용자 예외) · iter_7 정정 완료 · 다음 = Step 2 디스패치**. 후임 master·서브세션은 이 문서 → 마스터 플랜 → 최신 `Step <N>` → 최신 Result 순으로 읽고 이어받는다. "기억으로는" 금지 — 아래 path:line 을 실물로 연다.

## 1. 사용자 지시(원문 요지 · 상세 = 마스터 플랜 §Summary·Decisions Required 확정표)

- 과제: Claude 측 전 이력(RB→v1.0.26)을 파악하고 현행 v1.0.25/.1(+v1.0.26 A/B)을 검토해 열역학·동역학 관점의 수식 연구 진보 = 새 버전 **v1.0.27** 저작. 기준 6개(수식만으로 80~90% 이해·대학원 교재 형식·리뷰 논문급 서지·타전공 석박사 청중·일반→특수 사다리·사용자 방법론 절대 준수).
- 확정 결정 DR-1~23 + 신규 2(통계역학 전체 = Ch1 후반부 부록 D 교과서급 · 독자 참여형 섹션 X) = 마스터 플랜 `Claude/plans/2026-09-02-v2-master-plan.md` Decisions Required 확정표.
- 2026-09-05 지적: **동시 에이전트 ≤3**(병렬 허가 ≠ 대규모 fan-out) — 계획서 v5.5 · `memory/feedback-parallel-cap.md`.
- 2026-09-11 결정(계획서 v5.6 에 편입 완료 — Phase Range 재배열 블록 · Interfaces 「모델」 · Correction History v5.6): ① **흑연 우선 완성** — Ch1 PDF 를 먼저 내놓고 LCO·Si·코드는 뒤로(2.2 Step 19 · 2.3 Step 22 · 3.3 Step 43 · 4.6~4.8 · 챕터 7 이연) ② **모델 경계** — 챕터 1·2(등록부·진단 = 기존 문서 판정) = 지금처럼 Fable(작업·검수·master) · 기계 산출(배정표 정렬·카운트)만 Sonnet 4.6 + 자체검수 · 챕터 3 설계 = Opus 5.0 작업 sub(Step 단위) + Fable 검수 · 챕터 4·5·6 = Opus 4.8 저작 + Fable 검수(확정결함 2회 연속 절만 Fable 저작 승격) ③ 기록 = Step/Phase 종료마다 Step 파일·Result·Ledger·본 인계 갱신(사용자 2026-09-11 "후임 세션이 참고할 수 있게").

## 2. 현재까지 요약

- 마스터 플랜 v5.2 GO(2026-09-03) → Phase 1.1 Step 1(OUT-INV 인벤토리) 착수. 작업 sub 산출(iter_1) → 검수 R1(확정결함 1: 등재 누락) → iter_2 → R2(확정결함 1: 정책 미기계적용) → iter_3/3b(「추가 발견」 정책 (a)(b)(b′)(c) 확정 + 잔여 0 스크립트 증명) → R3(확정결함 0) → iter_4 → R4(Workflow · 확정결함 1: 정책 (b) 토크나이저 결함) → iter_5(토큰 정규화·`CODE_w_check.md` 등재) → R5(Workflow · 확정결함 1: (b) 정의 > 기계 규칙 — 확장자 없는 stem 인용 `KNOWN_DEFECTS`) → iter_6(`KNOWN_DEFECTS.md` 등재 · (b-1) 확장자 토큰 + (b-2) stem 스윕 이원화 · 경계 `(?![A-Za-z0-9_])` · PC 스냅샷 기록) → R6(Workflow · **확정결함 0** · 경미 5 · 제안 4) → iter_7(경미·제안 반영 · §10.8 · 계획서 v5.9) → **Step 1 수렴**(계획서 v5.7 사용자 예외 = R6 단독 0).
- OUT-INV = `Claude/results/V1027_HISTORY_INVENTORY.md`(1,757행 · 등재 740 파일·111,160줄 · §10 = master 처분·정정 이력 §10.1~10.7) · 증거 = `Claude/results/handoffs/v1027-phase-1.1-inventory/`(brief · audit_checklist r1~r4 · iter_1 TSV/work_log/audit_log/gen_outinv.ps1 · iter_2 audit_log_r2 · iter_3 policy_check(iter_6 최종판 · 스냅샷 기록)/audit_log_r3 · iter_4 audit_log_r4 · iter_5 audit_log_r5).
- 계획서 정정 v5.3·v5.4·v5.5(사실 정정)·v5.6(사용자 재결정 편입 — 흑연 우선 재배열·모델 경계·Assumptions 11 740/111,160)·v5.7(발췌독 원칙·R6 단독 수렴 예외)·v5.8(읽기 범위 실행 규칙)·v5.9(R6 반영·Step 1 수렴 선언) — 골격·Step·게이트 삭제 없음.
- Step 2 brief 선작성 = `Claude/results/handoffs/v1027-phase-1.1-reading/brief.md`(모델 경계 결정 반영 전 — 디스패치 전 갱신 필요: 정렬·청크 = Sonnet 4.6 기계 산출 + 자체검수, 판정 열은 OUT-INV 전사).

## 3. 미완료·다음 순서

1. (완료) R6 확정결함 0 → Step 1 수렴 · iter_7 정정 · 검토·정정 commit.
2. (완료) 계획서 v5.6 편입 · OUT-INV iter_6(740/111,160 · §10.7) · PC iter_6 스냅샷 판.
3. Step 2 정독 배정표(brief 갱신 후 디스패치) → 게이트 1.1 → `PHASE_1.1_V1027_INV_RESULT.md`+`.json` → `PHASE_1-7_V1027_EXECUTION_LEDGER.md` 생성 → push.
4. Phase 1.2~1.5 → 2.x(Ch1 몫) → 3.x → 4.0~4.5 → 5·6(Ch1) → **Ch1 PDF** → 이연분.

## 4. 주의

- `Codex/` 무접근(읽기 포함) · 동결 폴더(`docs/v1.0.24*`·`v1.0.25*`·`v1.0.26A/B`) 무수정 · 문건 본문 코드 언급 0 · tier 표기 0 · 독자 참여형 섹션 0 · 학술 용어 영어 원어.
- 검수 sub 반환이 한도(429)로 죽으면 침묵 흡수 금지 — Workflow 는 같은 run id 로 재개(스크립트 무수정 · 캐시 prefix 유지).
- 병렬 = 동시 ≤3. N×M 구조는 항목 순차.
- **검수 라운드 읽기 범위 실행 규칙(v5.8 · 사용자 2026-09-11 "매번 42번 이상씩 전문을 검토할 필요가 있어?")** — ① **1R 렌즈만 전문 정독**(≤250행 창 · 전 영역 cover · 창 경계 기록). ② **2R 이후 렌즈 = 발췌독**: 읽기 범위 = 직전 iter 처분표(§10.x)의 변경 지점 + 직전 라운드 발견의 반영 위치 + 그 문맥 ±30행. 프롬프트에 "파일 전체 Read 금지" 를 명시하고 coverage 표에 발췌 창만 적는다. ③ **반박자(refuter)** = 발견이 인용한 path:line 과 그 앞뒤 ±20행만 연다 · 파일 전체 Read 금지 · **인원 = 확정결함 후보만 3인, 경미·제안 후보는 1인**(발견 수가 10 을 넘으면 반박 총량이 라운드 비용을 지배한다). ④ **기계 검사는 매 라운드 전건 재실행**(카운트·Test-Path·hash 표기 파싱·policy_check (a)(c)/(b-1)/(b-2)·합계) — 발췌독이 못 보는 영역은 스크립트가 본다. ⑤ 동시 에이전트 ≤3 유지 · 발견 순차. ⑥ 위 규칙은 Workflow 스크립트 템플릿(렌즈·반박자 프롬프트)에 박아 두고 이후 모든 Step 의 검수 라운드에 그대로 쓴다 — 한 라운드 = 렌즈 2 + 반박 ≤(확정 후보×3 + 나머지×1) + 통합 1.
- 수렴 예외(Step 1 한정 · 사용자 2026-09-11): R6 단독 확정결함 0 → 다음 Step(계획서 v5.7). 반복 라운드 = 발췌독(v5.7·v5.8).
- OUT-INV·계획서 수정은 정확 일치·건수 검증 스크립트(스크래치패드 `patch_*.py` 방식)로만 — 통째 Write 금지 · 수정 전 wip commit(복원 지점).
- policy_check (b) 검사 = (b-1) 확장자 토큰(문자 집합 `[A-Za-z0-9_.-]` · 종료 경계 `(?![A-Za-z0-9_])`) + (b-2) 확장자 없는 stem 스윕 · 통제 문서 최종 편집 뒤 마지막에 재실행 · 머리에 5본 스냅샷 기록 — R4·R5 결함 재발 금지.

## 5. 인계 chain

- 이전 arc 인계: `Claude/docs/v1.0.25.1/results/HANDOVER_v25.md` · 판독 시드 `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R1~R7` · `review_master.md`.
- 본 arc 기록: Step 파일 `Claude/results/Step <N> — <제목>.md`(현재 Step 1) · Result `Claude/results/PHASE_<id>_V1027_<topic>_RESULT.md`(+json) · Ledger `Claude/results/PHASE_1-7_V1027_EXECUTION_LEDGER.md`(1.1 종료 시 생성) · commit `72a0477`→`cbc1d7c`→`731a94e`→`6bf32c9`→`b3a57bd`→`f3600f5`→`baccb49`→`81ec4e4`→`96d884b`(모두 wip 복원 지점 · push 는 Phase 종료 시).
