# Fable 재검 — 챕터 0(준비)·챕터 1(이력 전수감사) 세부 계획서

> 마스터 = `2026-07-02-fable-reaudit-v12-master-plan.md`. 본 세부계획 = Phase 0.2(Steps 3-4) + 챕터 1 Phase 1.1-1.3(Steps 5-12). result = `Claude/results/process/FABLE_REAUDIT_P0_P1_RESULT.md`. 감사 산출 = `docs/Fable_점검/`. 브랜치 = main(phase 종료마다 커밋+푸쉬).

## Phase 0.2 — 준비 (Steps 3-4)
- Step 3: `docs/Fable_점검/` 폴더 생성.
- Step 4: 감사 대상 인벤토리 확정 — 버전별(Ch1 v3·v4·v5·v6·v7·v8·v9·v10·v1.0.10·v1.0.11 / Ch2 v3·v4·v5·v1.0.10 / 코드 v11_final·v1.0.10) tex·계획서·spine(AUTHOR_BRIEF·KNOWN_DEFECTS·FIX_LIST·CHERRYPICK_PLAN·REVIEW)·RESULT·핸드오버 전수 목록. gate = 누락 버전 0.

## Phase 1.1 — 버전×문건 매핑표 (Steps 5-6)
- Step 5: 인벤토리를 "버전 → (계획서 | 산출물 | 검수기록 | 핸드오버)" 매핑표로 정리(어느 버전이 어떤 계획 하에 만들어졌고 무엇으로 검수됐나).
- Step 6: 전환점(v3→v4 Fable→Opus 인수·v5→v6 RB 재구축·v7 배치·v8 유도확장·v9 LCO·v10 broadening 복원·v1.0.10 코드동기화·v1.0.11 수식화)별 핵심 질문 확정. gate = 매핑 완결·근거 경로 실재.

## Phase 1.2 — Fable 직접 정독 (Steps 7-10)
- Step 7: 기록류 정독(gap 채움) — v7 계획/결과·v6 RB 트랙(CHARTER·HANDOVER_RB 3종·LEDGER)·v5 전환 기록·PHASE_REWORK/2TRACK RESULT·v9/v10 CHERRYPICK_PLAN. (본 세션에서 이미 정독한 것 재사용: v8/v9/v10/ch2v4 BRIEF·KNOWN_DEFECTS·FIX_LIST·6-30 핸드오버·R1/R2 리뷰·PHASE_CH1v10.)
- Step 8: ★버전 tex 실물 대조 — 대용량(v3 200KB 등)은 위임 심층 분석(모델 분산, Fable 슬롯 포함) + master는 각 버전의 구조·대표 절 직접 표본 정독(CORE 판단). 전환마다 "무엇이 추가/삭제/왜곡됐나".
- Step 9: 버전 전환별 판정 — (이전 문제→개선 의도→달성→우수구조 보존) 4문 + 장점/단점/문제점.
- Step 10: 교차검증(기록 vs tex 실물 vs 이번 세션 인계검수 결과 삼각). gate = 전 전환 판정에 줄 근거.

## Phase 1.3 — 감사 문건 작성 (Steps 11-12)
- Step 11: `docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md` — 버전별 변경이력·장점·단점·문제점·전체 흐름 종합·v12 교훈.
- Step 12: 자체 검수(coverage·근거·4-tier) 후 result 저장·ledger·커밋+푸쉬. gate = 전 버전 커버·판정 줄근거·문건 완결.

## 산출·경로 규율
- 계획 = plans/ · step 이력 = results/process/FABLE_REAUDIT_P0_P1_RESULT.md · 감사 = docs/Fable_점검/ · 커밋+푸쉬 = phase 종료마다(main).
