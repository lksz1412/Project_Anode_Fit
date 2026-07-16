# Phase P8 세부 계획서 — v1.0.20 마감 (Steps 91–98)

## Summary
v1.0.20 을 원본으로 동결 마감: 그림 경쟁 잔여(FF1~3) 수합 → 체리픽 판정문(자료 보존 — 반영은 v1.0.21 소관) → 최종 빌드·PDF 커밋 → 코드 판정(스트림 2 완료분 — matched 이월, ERRATA E-001 코드 영향 무 재확인) → FITTING_GUIDE 승계+버전 표기 → HANDOVER_v1.0.20(사용자 지시 전문 Chain·결정 이력·추가 후보·v1.0.21 이월 목록) → INDEX 2종 갱신 → 최종 커밋·푸시(PR 생성 금지).

## Current Ground Truth
P0~P7 전 PASS + B-008/B-009 반영(빌드 66/25/8p err0·diff 1:1·자산 336/21). 코드 Anode_Fit_v1.0.20.py = G1/G2/G3 PASS(변경 함수 0·헤더 이월)·test_gates_v1020.py exit 0. 그림 경쟁 FO1~3 완주(구현 12본)·FF1~3 진행 중. 방향성 보고서 3본(STATMECH·GENERAL·INTERCHAPTER) + TRIAGE·검수 11본 전부 커밋됨. 확장 전건 v1.0.21 이월(마스터플랜 v5).

## Phase Range
P8 단독(Steps 91–98). v1.0.20 종결 phase.

## Non-goals
확장 반영 X(v1.0.21 소관 — 통계역학 2건·LCO·Si·일반 확장·그림 신규 반영). 물리·수식 추가 변경 X. PR 생성 X.

## Phase P8 Steps
| Step | 내용 | Gate |
|---|---|---|
| 91 | 본 계획서 저장 | 파일 |
| 92 | FF1~3 수합(생존 규칙 ≥3·Fable≥1은 전체 6창 기준 기충족) → 그림 체리픽 판정문 FIGS_PICK_JUDGMENT.md(신규 vs 기존 비교 포함 — 사용자 기준) | 판정문 |
| 93 | 최종 빌드 3본 + 구조 + 스냅샷 final + diff(P7b→final ±0 확인) | GREEN |
| 94 | 코드 마감 판정: ERRATA 원장(E-001 무영향) ↔ matched 이월 재확인·게이트 재실행 | exit 0 |
| 95 | FITTING_GUIDE.md 승계(버전 표기)·PDF 3본 커밋 | 파일 |
| 96 | HANDOVER_v1.0.20.md(지시 전문 Chain·결정 이력·확정/근거미발견/추정/미검증 4-tier 요약·추가 후보 목록·v1.0.21 이월 목록) | 11항목 |
| 97 | docs/INDEX.md·Claude/plans/INDEX.md 갱신 | 갱신 |
| 98 | ledger P8 행·최종 커밋·푸시 | 해시 |

## Test Plan
최종 빌드 err0·undef0·페이지수 기록(66/25/8). 구조 PASS(자산 336/21·미인용 0·dup 0). 코드 게이트 재실행 exit 0. diff(P7b→final) ±0(마감 중 문서 무변경 증빙).

## Assumptions
FF 창 사고 시: 전체 6창 기준 생존 규칙 기충족(FO 3본 + Fable 조기 저장분) — 잔여분 수합 가능한 만큼으로 체리픽 진행(기록).

## Correction History
(초판)
