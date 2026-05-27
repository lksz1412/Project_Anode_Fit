# Phase 0_v2 — Foundation (Charter v2 audit + Spine lock) Phase-Level Plan

**Date**: 2026-05-28
**Parent roadmap**: `Claude/plans/MASTER_ROADMAP_v2.md`
**Charter binding**: `Claude/results/CHARTER_v2.md`
**Cumulative step range**: **1 ~ 60** (minimum baseline per `feedback_step_granularity_flexibility`; expansion OK)

---

## §1. Summary

본 Phase 0_v2 는 v2 series 의 governance foundation 을 확정. 산출 = Charter v2 의 self-audit + Master Roadmap v2 의 self-consistency 점검 + v1 산출 이동 확인 + spine A1-A12 lock 확인 + 본 phase Result md/json 저장.

본 phase 는 **LaTeX 본문 작성 X**, **governance only**. Phase 1_v2 (§0+§1 머리말+작업 동기) 가 본 phase PASS 후 진입.

## §2. Inputs (Read 대상)

- `Claude/results/CHARTER_v2.md` (835 줄, 12 sections + §00 사용자 verbatim)
- `Claude/plans/MASTER_ROADMAP_v2.md` (272+ 줄, 22 sections + §0 사용자 verbatim)
- `Claude/results/EXECUTION_LEDGER_v2.md` (17-row ledger)
- `Claude/_claude/memory/MEMORY.md` (인덱스)
- `Claude/_claude/memory/feedback_phase_result_anti_compaction_hallucination.md` (신규)
- `Claude/_claude/memory/feedback_step_granularity_flexibility.md` (신규)

## §3. Steps (cumulative 1 ~ 60, 최소 기준)

1. Save this Phase 0_v2 plan — **DONE**.
2. Confirm `Claude/old/` 에 v1 산출 35 파일 이동 완료 (commit `e3c0ab5` 의 git rename log).
3. Confirm Charter v2 의 §00 (사용자 verbatim) 박힘 — `head -100 CHARTER_v2.md` 으로 확인.
4. Confirm Master Roadmap v2 의 §0 (사용자 verbatim) 박힘 — `head -100 MASTER_ROADMAP_v2.md` 으로 확인.
5. Confirm spine A1-A12 가 Charter v2 §2 에 lock 됨.
6. Confirm DEC-1 ~ DEC-8 명시 (Charter §10).
7. Confirm DQ-v2-1 ~ DQ-v2-5 등재 (Charter §11).
8. Confirm Master Roadmap v2 §2 의 17 phase × 1220 step.
9. Audit Charter v2 self-consistency:
   - 9a. §00 사용자 verbatim 과 §1 Objective 정합.
   - 9b. §2 spine A1-A12 와 §8 variable inventory 정합.
   - 9c. §3 anti-pattern + §6 Dim #11 정합.
   - 9d. §00.6 (step 유연성) + §00.7 (컴팩션 복구) + §00.8 (Ralph Wiggum) 의 메모리 cross-reference 존재.
10. Audit Master Roadmap v2 self-consistency:
    - 10a. §0 사용자 verbatim 과 §1 Objective 정합.
    - 10b. §2 phase 목록과 §3-§18 의 각 phase 본문 정합.
    - 10c. §19 Test Plan 의 T-v2-1~T-v2-11 과 phase deliverable 정합.
11. Audit Dim #11 Pass 1 keyword scan on CHARTER_v2 + MASTER_ROADMAP_v2:
    - 11a. `\max`, `\min`, `\Heaviside`, logistic, sigmoid 등 anti-pattern keyword in definitional contexts (목표: 0 FAIL).
    - 11b. erf, discrete N_p 는 OK-derived (v2 재분류) — 발견 시 분류 명시.
12. Audit §5 Writing Precision Standard self-application on CHARTER_v2 + MASTER_ROADMAP_v2:
    - 12a. "trivially", "obviously", "clearly" 단독 사용 (목표: 0).
    - 12b. "It can be shown that" without derivation (목표: 0).
13. Confirm 본 phase result 파일 위치: `Claude/results/PHASE_0_v2_FOUNDATION_RESULT.md` + `.json`.
14. Confirm ledger 행 갱신 위치: `Claude/results/EXECUTION_LEDGER_v2.md`.
15. Write Phase 0_v2 Result md (Steps 16-50 의 audit 결과 본문).
16-50. Audit 결과 본문 작성 (각 step 의 발견 사항 → Result md 의 §"Audit" 섹션).
51. Write Phase 0_v2 Result json (machine-readable).
52. Validate Result json parses (`python -m json.tool`).
53. Update ledger Phase 0_v2 row from IN_PROGRESS → PASS.
54. Commit + push.
55. Confirm push success.
56. Mark Phase 0_v2 PASS, Gate `PASS_FOUNDATION_v2`.
57. Record next-step entry for Phase 1_v2 (cumulative step 61).
58. Confirm 본 phase 에서 LaTeX 본문 작성 X (governance only).
59. Confirm 본 phase 에서 `Claude/docs/` 의 어떤 파일도 modify/create 안 함.
60. End Phase 0_v2 boundary.

**Expansion note** (`feedback_step_granularity_flexibility`): 위 60 step 은 최소 기준점. Audit Pass 1+2+3 (Ralph Wiggum loop) 진행 중 추가 검토 필요 시 step 늘려서 확장 OK. 본 phase 의 Actual Steps 칸은 실제 사용 step 수로 갱신.

## §4. Gates

- `GATE_0_v2_1`: Charter v2 9 sections + §00 (5 sub) + §00.6-§00.8 (3 sub) 존재.
- `GATE_0_v2_2`: Master Roadmap v2 22 sections + §0 (5 sub) + §0.6-§0.8 (3 sub) 존재.
- `GATE_0_v2_3`: v1 산출 35 파일 모두 `Claude/old/` 이동 확인 (git log).
- `GATE_0_v2_4`: Charter v2 + Master Roadmap v2 self-consistency audit PASS (Step 9-10).
- `GATE_0_v2_5`: Audit Dim #11 Pass 1 on governance docs PASS (0 FAIL).
- `GATE_0_v2_6`: §5 Writing Precision Standard 적용 (Step 12) PASS.
- `GATE_0_v2_7`: 신규 메모리 2 개 (`anti_compaction_hallucination` + `step_granularity_flexibility`) 글로벌 + 프로젝트 사본 동기화 확인.
- `GATE_0_v2_8`: Phase 0_v2 Result md + json + ledger 갱신 + commit 완료.

## §5. Test Plan

- T-0_v2-1: 모든 Step 1-60 완료 (또는 확장된 actual step 까지).
- T-0_v2-2: 8 Gates 모두 PASS.
- T-0_v2-3: `Claude/docs/` 에 chapter1 v1 / v2 파일 부재 (v2 본문은 Phase 1_v2 부터).
- T-0_v2-4: Phase 1_v2 entry path clear.

## §6. Assumptions

- A-0_v2-1. 사용자 GO 사인 ("작업 ㄱㄱ", 2026-05-28) 이 Phase 0_v2 entry 의 GO.
- A-0_v2-2. DEC-2 (V_n = V_{n,OCV} 외부 lookup) 기본 유지, DQ-v2-1 추후 사용자 명시 시 변경.
- A-0_v2-3. v2 series cumulative step = 1 부터 (DEC-6). v1 series 와 무관.

## §7. Decision Queue (this phase)

- 새 DQ 없음. v2 series 의 기존 DQ-v2-1 ~ DQ-v2-5 만.

## §8. Sprint Contract

- [ ] Steps 1-60 (또는 확장) 완료.
- [ ] Gates 1-8 PASS.
- [ ] Ralph Wiggum loop Pass 3 PASS.
- [ ] Commit + push + ledger update.
- [ ] Phase 1_v2 entry clear.
