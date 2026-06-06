# Ch1 보완 (A.0–A.5) Execution Ledger

**Plan**: `Claude/plans/2026-06-06-ch1-sec6-statmech-accessibility-plan.md`
**대상**: `Claude/docs/graphite_ica_ch1.tex` (R.0~R.9 완료본; 879줄·19p)

| Phase | Planned Steps | Actual Steps | Block | Purpose | Status | Result | Validation | Gate | Next Step |
|---|---:|---:|---|---|---|---|---|---|---:|
| A.0 | 1–4 | 1–4 | design | §5끝~§6~§7 재정독 + eq#29/overflow 확정 + 신규 절 설계 + Decision | PASS | `PHASE_A0_design_RESULT.md` | eq#29=superpose(.aux) 확정; 신규 절 5도구 설계; Decision 권고값 확정 | PASS_A0_DESIGN | 5 |
| A.1 | 5–7 | 5–7 | eq-linebreak | eq:superpose(#29) 줄나눔 + overflow 교정 + 빌드 | PASS | `PHASE_A1_eq-linebreak_RESULT.md` | 모든 디스플레이식 overflow 0(eq:superpose·arrhenius·verifybox·equation* 분할); 내용 불변 | PASS_A1_EQ_LINEBREAK | 8 |
| A.2 | 8–11 | 8–11 | s1-5-light | §1~5 경량 검토(R.9 Codex CLEAN + A.1 레이아웃 content-preserving; 교차모델 §1~5 는 A.5 전영역 패스가 커버) | PASS | (A3-A5 result 내 기록) | A.5 Codex 전영역서 §1~5 회귀 0 확인 | PASS_A2_S1-5_LIGHT | 12 |
| A.3 | 12–18 | 12–18 | new-section | 신규 §6 통계 도구(5도구, 초년생) | PASS | `PHASE_A3-A5_statmech-section_RESULT.md` | Codex 신규 절 CLEAN(G-undergrad 포함); 도구1~5 수학 정확 | PASS_A3_NEW_SECTION | 19 |
| A.4 | 19–25 | 19–25 | dist-rewrite | §7 dist 가 도구1~4(eq:norm/wavg/varprop/jacobian) 인용·연결 | PASS | 〃 | §6↔§7 인용 4건 정합; §5→§6→§7 비약 0 | PASS_A4_DIST_LINK | 26 |
| A.5 | 26–30 | 26–30 | final-verify | 하류 정합 + Codex 교차모델 전영역 + 빌드 | PASS | 〃 | **Codex DOCUMENT CLEAN**; 참조 139·라벨 48 undefined/중복 0; clarity 2건 보강 | PASS_A5_FINAL | 완료 |

**Decision(확정, 권고값)**: D-newsection=신규 \section{통계의 도구} §5·§6 사이 삽입(dist→§7 자동) · D-eq29=eq:superpose aligned 2줄 · D-scope=§1~5 경량·§6+ 본격 · D-undergrad=G-undergrad 게이트.
**Anti-compaction(§X)**: 컴팩션·재개 직후 5단계 재정독 의무(G-recovery).
