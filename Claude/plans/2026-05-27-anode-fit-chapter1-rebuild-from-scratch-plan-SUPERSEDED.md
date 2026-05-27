# SUPERSESSION MARKER — Chapter 1 Rebuild Plan v0.1

작성일: 2026-05-27
양식: [[feedback_document_protection_addendum_pattern]] §"Supersession"

## Supersedes

- `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-from-scratch-plan.md` (v0.1, commit `a63378f`)
- **본문은 보존** (덮어쓰기 X). 향후 참조 기준 X.

## Superseded By

- `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md` (v0.2 마스터 로드맵)
- 입력 보고서: `Claude/results/PROJECT_AUDIT_REPORT_v0.2.md`

## Supersession Reason

사용자 5-27 critical 피드백 3 항목 (`PROJECT_AUDIT_REPORT_v0.2.md` §"사용자 5-27 critical 피드백"):

1. **계획서 수준 부족** — v0.1 (436 줄, 2 phase, 17 step) 가 RO_SkillDict codex 마스터 로드맵 (1763 줄, 16 phase, 1000+ step) 의 약 1/5 수준. v0.2 마스터 로드맵 (~1500+ 줄, 17 phase, ~1200 step) 으로 granularity 확장.
2. **Ref 6, 7 DOI 사용자 떠넘김** — v0.1 의 DQ-E2 가 잘못된 위임. v0.2 는 자기 외부 검색 (WebSearch / WebFetch) 후 `근거 미발견` 명시. DQ-G4 는 "사용자 직접 제공 옵션" 으로 재정의 (의뢰 아님).
3. **본질 진단 실패** — v0.1 의 Phase B self-consistent loop (Loop 1/2/3) 진단을 본질로 잘못 다룸. 실제 본질 = ver1~5 의 step function 가정 (사용자 verbatim "적분을 모 아니면 도 즉 스텝펑션의 형태"). v0.2 는 Charter (Phase E0) + 신 spine (continuous chemical potential, Phase E1) + Audit Dim #11 (system-fidelity) 도입으로 본질 처리.

## v0.1 의 본문 상태

- 파일 `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-from-scratch-plan.md` 는 변경되지 않음 (덮어쓰기 X).
- v0.1 의 Phase E (Steps 19-30) + Phase F (Steps 31-35) 구조는 v0.2 의 Phase E0-F5 로 재해석·확장.
- v0.1 의 A1~A13 가정은 v0.2 의 §"Assumptions" A1~A15 로 갱신 (A1 Phase C 매핑 라벨 채택 = v0.2 의 Charter 적용 후 일부 재검토 필요, A4-A9 의 DQ-C1~C6 결정은 v0.2 Phase E10 시점으로 이동).
- v0.1 의 DQ-E1~E6 는 v0.2 의 DQ-G1~G8 로 재정리 (E6 → G1, E1 → G2 통합, E2 → G4 재정의, E3 → A6/Phase F1, E4 → G2, E5 → G3).

## 향후 참조

- v0.1 본문이 필요한 경우 (이력 추적, audit 재검증 등) `Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-from-scratch-plan.md` 직접 참조 가능.
- **신 작업은 모두 v0.2 마스터 로드맵 기준**.

## Re-validation

- [[feedback_phase_audit_workflow]] Pass 3 재검증: 본 supersession 이 v0.1 의 다른 항목 (예: Phase A~D 의 4 RESULT 파일) 에 영향 X. Phase A~D ledger 도 무변. 회귀 없음.

## Ledger Update

- 본 supersession 의 사실 자체를 `Claude/results/PHASE_A_D_EXECUTION_LEDGER.md` Updates 표에 1 행 추가:
  - 2026-05-27 | v0.1 plan | superseded by v0.2 master roadmap (`Claude/plans/2026-05-27-anode-fit-chapter1-rebuild-master-roadmap.md`)
- v0.2 마스터 로드맵의 신규 Ledger 는 `Claude/results/PHASE_E_F_EXECUTION_LEDGER.md` 로 별도 (cumulative step 19-1220 cover).
