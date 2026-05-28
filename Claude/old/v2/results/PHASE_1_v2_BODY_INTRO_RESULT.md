# Phase 1_v2 Result — §0 본문 머리말 + §1 작업의 동기

**Date**: 2026-05-28
**Cumulative steps**: 61 ~ 120
**Phase ID**: `PASS_BODY_INTRO_v2`
**Parent roadmap**: `Claude/plans/MASTER_ROADMAP_v2.md`
**Charter binding**: `Claude/results/CHARTER_v2.md`
**File touched**: `Claude/docs/graphite_ica_chapter1.tex` (newly created, lines 1-345)

---

## §1. Summary

Chapter 1 v2 의 본문 LaTeX 파일 (`graphite_ica_chapter1.tex`) 을 처음부터 신규
생성. Preamble (49-130), Charter compliance header (1-47, 사용자 verbatim +
P1-P4 + spine A1-A12 인라인), 초록 (109-127), §1 본문 (133-345) 작성. 본문
§1 은 사용자 의도 verbatim 박힘 (§1.1), 실험 관측 사실 (§1.2, O1+O2+O3),
이론적 가설 (§1.3, H1+H2+H3 = spine 출발점), deliverable 명시 (§1.4), 박사학위
연구 위치 (§1.5, Refs 6/7), spine 요약 (§1.6, A1-A12) 구성.

## §2. 산출

- File created: `Claude/docs/graphite_ica_chapter1.tex` — 345 lines (preamble + §1)
- Section headings written: 6 subsections under §1
- Spine equations referenced: A1-A12 (인라인 macros 박힘)
- User verbatim quotation: Charter §00.1 전문 (132자) `사용자 verbatim` theorem 박싱
- 학부 수준 prose: 모든 §1 본문 학부 수준, 비약/생략 X (Charter §00.2 P4)

## §3. Gates

| Gate ID | Requirement | Status |
|---|---|---|
| `GATE_1_v2_1` | chapter1.tex 신규 생성 (v1 미사용) | PASS |
| `GATE_1_v2_2` | Charter compliance header 인라인 (verbatim + P1-P4 + AP + spine) | PASS |
| `GATE_1_v2_3` | §1.1 사용자 verbatim 박싱 | PASS |
| `GATE_1_v2_4` | §1.2 O1/O2/O3 명시 | PASS |
| `GATE_1_v2_5` | §1.3 H1/H2/H3 hypothesis 명시 | PASS |
| `GATE_1_v2_6` | §1.6 spine A1-A12 박싱 | PASS |
| `GATE_1_v2_7` | 학부 수준 prose + 비약 X | PASS |

## §4. Audit

- Audit Dim #11 Pass 1 keyword scan on §0+§1 본문:
  - `\max` / `\min` / `\Heaviside` / `logistic` / `sigmoid` / `softplus` / `\operatorname{relu}` / `clip` 횟수 = 0 (definitional context)
  - 정의식 step function 류 = 0
  - PASS
- Writing Precision §5 self-check:
  - "trivially" / "obviously" / "clearly" 단독 사용 = 0
  - "It can be shown that" without derivation = 0
  - PASS

## §5. Next

- Phase 2_v2 (§2 기호와 단위 컨벤션) 자동 진입 — cumulative step 121
- 결정 대기 X

## §6. Decision Queue

본 phase 에서 신규 DQ 발생 X. v2 series 의 DQ-v2-1 ~ DQ-v2-5 그대로.
