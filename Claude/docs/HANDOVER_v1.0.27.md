# HANDOVER_v1.0.27 — v1.0.27 arc 인계(진행 중 판 · 매 Step/Phase 종료·중단 시 갱신)

> 최종 갱신 = 2026-09-11 · master Fable 5.1 · 상태 = **Phase 1.1 Step 1 — 검수 R5 확정결함 1(stem 인용 `KNOWN_DEFECTS`) 반영한 iter_6 적용 · 계획서 v5.6(흑연 우선 재배열·모델 경계 편입) · 검수 R6 진행 중**(R6·R7 연속 0 이면 수렴). 후임 master·서브세션은 이 문서 → 마스터 플랜 → 최신 `Step <N>` → 최신 Result 순으로 읽고 이어받는다. "기억으로는" 금지 — 아래 path:line 을 실물로 연다.

## 1. 사용자 지시(원문 요지 · 상세 = 마스터 플랜 §Summary·Decisions Required 확정표)

- 과제: Claude 측 전 이력(RB→v1.0.26)을 파악하고 현행 v1.0.25/.1(+v1.0.26 A/B)을 검토해 열역학·동역학 관점의 수식 연구 진보 = 새 버전 **v1.0.27** 저작. 기준 6개(수식만으로 80~90% 이해·대학원 교재 형식·리뷰 논문급 서지·타전공 석박사 청중·일반→특수 사다리·사용자 방법론 절대 준수).
- 확정 결정 DR-1~23 + 신규 2(통계역학 전체 = Ch1 후반부 부록 D 교과서급 · 독자 참여형 섹션 X) = 마스터 플랜 `Claude/plans/2026-09-02-v2-master-plan.md` Decisions Required 확정표.
- 2026-09-05 지적: **동시 에이전트 ≤3**(병렬 허가 ≠ 대규모 fan-out) — 계획서 v5.5 · `memory/feedback-parallel-cap.md`.
- 2026-09-11 결정(계획서 v5.6 에 편입 완료 — Phase Range 재배열 블록 · Interfaces 「모델」 · Correction History v5.6): ① **흑연 우선 완성** — Ch1 PDF 를 먼저 내놓고 LCO·Si·코드는 뒤로(2.2 Step 19 · 2.3 Step 22 · 3.3 Step 43 · 4.6~4.8 · 챕터 7 이연) ② **모델 경계** — 챕터 1·2(등록부·진단 = 기존 문서 판정) = 지금처럼 Fable(작업·검수·master) · 기계 산출(배정표 정렬·카운트)만 Sonnet 4.6 + 자체검수 · 챕터 3 설계 = Opus 5.0 작업 sub(Step 단위) + Fable 검수 · 챕터 4·5·6 = Opus 4.8 저작 + Fable 검수(확정결함 2회 연속 절만 Fable 저작 승격) ③ 기록 = Step/Phase 종료마다 Step 파일·Result·Ledger·본 인계 갱신(사용자 2026-09-11 "후임 세션이 참고할 수 있게").

## 2. 현재까지 요약

- 마스터 플랜 v5.2 GO(2026-09-03) → Phase 1.1 Step 1(OUT-INV 인벤토리) 착수. 작업 sub 산출(iter_1) → 검수 R1(확정결함 1: 등재 누락) → iter_2 → R2(확정결함 1: 정책 미기계적용) → iter_3/3b(「추가 발견」 정책 (a)(b)(b′)(c) 확정 + 잔여 0 스크립트 증명) → R3(확정결함 0) → iter_4 → R4(Workflow · 확정결함 1: 정책 (b) 토크나이저 결함) → iter_5(토큰 정규화·`CODE_w_check.md` 등재) → **R5 실행 중**(run `wf_5f60ae3f-2d2` · 캐시 39 + 재실행 9). 수렴 조건 = 연속 2R 확정결함 0 → R5·R6.
- OUT-INV = `Claude/results/V1027_HISTORY_INVENTORY.md`(1,736행 · 등재 739 파일·111,130줄 · §10 = master 처분·정정 이력) · 증거 = `Claude/results/handoffs/v1027-phase-1.1-inventory/`(brief · audit_checklist r1~r4 · iter_1 TSV/work_log/audit_log/gen_outinv.ps1 · iter_2 audit_log_r2 · iter_3 policy_check(iter_5 최종판)/audit_log_r3 · iter_4 audit_log_r4).
- 계획서 사실 정정 v5.3·v5.4·v5.5(Correction History) — 골격·Step·게이트 불변.
- Step 2 brief 선작성 = `Claude/results/handoffs/v1027-phase-1.1-reading/brief.md`(모델 경계 결정 반영 전 — 디스패치 전 갱신 필요: 정렬·청크 = Sonnet 4.6 기계 산출 + 자체검수, 판정 열은 OUT-INV 전사).

## 3. 미완료·다음 순서

1. R6(iter_6 regression + PC (b-1)/(b-2) 독립 재현 · 동시 ≤3) → 0 이면 R7 → 연속 2R 수렴 → 검토·정정 commit → Step 1 파일 확정.
2. (완료) 계획서 v5.6 편입 · OUT-INV iter_6(740/111,160 · §10.7) · PC iter_6 스냅샷 판.
3. Step 2 정독 배정표(brief 갱신 후 디스패치) → 게이트 1.1 → `PHASE_1.1_V1027_INV_RESULT.md`+`.json` → `PHASE_1-7_V1027_EXECUTION_LEDGER.md` 생성 → push.
4. Phase 1.2~1.5 → 2.x(Ch1 몫) → 3.x → 4.0~4.5 → 5·6(Ch1) → **Ch1 PDF** → 이연분.

## 4. 주의

- `Codex/` 무접근(읽기 포함) · 동결 폴더(`docs/v1.0.24*`·`v1.0.25*`·`v1.0.26A/B`) 무수정 · 문건 본문 코드 언급 0 · tier 표기 0 · 독자 참여형 섹션 0 · 학술 용어 영어 원어.
- 검수 sub 반환이 한도(429)로 죽으면 침묵 흡수 금지 — Workflow 는 같은 run id 로 재개(스크립트 무수정 · 캐시 prefix 유지).
- 병렬 = 동시 ≤3. N×M 구조는 항목 순차.
- OUT-INV·계획서 수정은 정확 일치·건수 검증 스크립트(스크래치패드 `patch_*.py` 방식)로만 — 통째 Write 금지 · 수정 전 wip commit(복원 지점).
- policy_check 토큰화 = `[A-Za-z0-9_.-]` 만(괄호 제외) — R4 결함 재발 금지.

## 5. 인계 chain

- 이전 arc 인계: `Claude/docs/v1.0.25.1/results/HANDOVER_v25.md` · 판독 시드 `Claude/results/handoffs/2026-09-02-v2-master-plan/wf/R1~R7` · `review_master.md`.
- 본 arc 기록: Step 파일 `Claude/results/Step <N> — <제목>.md`(현재 Step 1) · Result `Claude/results/PHASE_<id>_V1027_<topic>_RESULT.md`(+json) · Ledger `Claude/results/PHASE_1-7_V1027_EXECUTION_LEDGER.md`(1.1 종료 시 생성) · commit `72a0477`→`cbc1d7c`→`731a94e`→`6bf32c9`→`b3a57bd`→`f3600f5`(모두 wip 복원 지점 · push 는 Phase 종료 시).
