# plans/ INDEX (MOC) — 계획서 항해 진입점

> 컴팩션 복구·항해용. **현재 활성 마스터부터 읽는다.** 과거 계획은 시대별 그룹으로 묶음(날짜순 파일명 = 1차 정렬). result/ledger 는 `../results/process/`.

## ★ 현재 활성 (v1.0.10 교재 증판본 — 코드↔문건 동기화)
| 파일 | 역할 | 상태 |
|---|---|---|
| **2026-07-01-v1010-code-doc-sync-bdd-fitting-plan.md** | ★**MASTER** — 순차 6-페이즈(1 코드 → 2+3 Ch1 → 4 Ch2 → 5 코드개정 → 6 최종점검). LCO·발열 코드구현=P4. | GO 대기 |
| 2026-07-01-graph-verify-code-doc-unify-v1010-plan.md | (완료) 코드 정상 종개형 검증 + 1.0.10 버전 통일 | done |
| 2026-06-30-rework-broadening-restore-weff-fix-reorg-plan.md | (완료) broadening 복원·w_eff 제거·구조 재정리 | done |
- 실행 ledger·result: `../results/process/V1010_EXECUTION_LEDGER.md`, `V1010_P{n}_*_RESULT.md`, `GRAPH_VERIFY_RESULT.md`, `PHASE_REWORK_RESULT.md`.

## 마스터/로드맵 (역대)
- `MASTER_ROADMAP_v3.md` · `MASTER_ROADMAP_CH2_v1.md` · `2026-06-22-ch1-v5-comprehensive-rereview-MASTER.md` · `2026-06-22-ch1-v6-flowchart-reassembly-MASTER.md`

## 역사 계획 (시대별 그룹 — 날짜순)
- **05-29~05-30 통합·재유도 기획**: consolidation-roadmap·intent-gap-diagnosis·undergrad-rederivation-rebuild.
- **06-01~06-03 Ch1 자기완결·논리사슬 재구축**: self-contained·blank-page-clean-spine·FINAL-logical-chain·intersection-bridge·peak-physics-derivation·rerevision(2·signs).
- **06-06~06-08 Ch1 교과서형·레지스터 + Ch2 신설(반속/발열/히스 기획)**: register-revision·sec6/sec8-10·textbook-form / ch2-5-rebuild·ch2-deep·ch2-textbook-overhaul·NEW-ch2-kinetics·NEW-ch2-hysteresis·connective-masterequation. (⚠️이때 Ch3=발열 4장 기획 = 이후 supersede)
- **06-09~06-13 통합·깊이확장·Ch1 v2~v4 패스**: integration-completeness·ch3-heat-build·merge-single-chapter·textbook-depth / ch1 v2(blank/rewrite/proofread/tone/figures)·v3(equation-selfcontained/w4/x-pass)·v4(stacking-redo).
- **06-17~06-22 Ch1 v5/v6 + v5RR 라운드**: v5-equation-driven·v5RR(R0~R3)·v6-flowchart.
- **06-29~06-30 Ch1 v7/v8 9x9x1x1 + v9 LCO·Ch2 v4 2track + 조사**: v7-codeflow·v8-derivation-expanded·ch1v9-LCO-ch2v4-mixing-2track·ch2-reversible-heat-survey·radius-distribution-survey.
- **06-30~07-01 rework·v1.0.10**: (위 ★현재 활성 참조).

## 규약 (지침 — [[feedback_plan_template_11sections]]·[[feedback_phase_execution_loop]])
- 마스터 계획 + 페이즈별 세부 계획 = **plans/ 에만** 차곡차곡. 페이즈마다 **result** 를 results/process 에 저장(다음 페이즈 전제·컴팩션 복구점), **ledger** 갱신. 문서 추가 시 같은 턴에 본 INDEX 갱신.
