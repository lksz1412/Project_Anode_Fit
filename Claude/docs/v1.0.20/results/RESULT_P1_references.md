# Phase P1 — 서지 원장 Result

## Summary
기존 서지 42건 전수 온라인 실재 검증(V1 36·V2 3·FAIL 2·내부 1) → 정정 8건(C-001~008) bib 반영, 무인용 문헌성 주장 U1–U12 확정·배정, 신규 후보 12키 검증 등재. **REFERENCE_LEDGER 발효: 이후 본문 인용은 원장 V1 키만.**

## Step Range
Steps 11–22 (계획 11–22 전건 수행 + 계획 정정 1건[bib 정정을 P1 직접 반영으로]).

## Inputs
`_sections/ch1_bib.tex`(1–38 전문)·`_sections/ch2_bib.tex`(1–26 전문)·킥오프 조사 ①·전 절 tex(어간 재스캔 — 기계 스캔).

## Files Created
V1020_REFLEDGER_DRAFT_existing.md(sub-agent)·V1020_REFLEDGER_DRAFT_candidates.md(sub-agent)·V1020_REFERENCE_LEDGER.md·V1020_P1_CITATION_BASELINE.md·STEP_LOG_P1.md·본 RESULT·plans/PLAN_P1_references.md.

## Files Updated
ch1_bib.tex(C-001~004·008: ml2024 DOI/저자·leviaurbach1999 제목·ohzuku1993 제목·msmr2024 표기·헤더 24→28) / ch2_bib.tex(C-005~007: 아티클번호 2·제목 전문·쪽수) / V1020_CHANGE_LOG.md(서지정정 8행).

## Read Coverage
- 전문: ch1_bib.tex(38행)·ch2_bib.tex(26행)·두 초안 보고서 전문·ch1_sec00(91)·ch1_sec01(205)[P2 선행 정독 겸].
- 기계 스캔: 전 절 tex(어간 매치 — 전문 정독 아님, 각 절 정독은 담당 phase).

## Execution Evidence
- 검증 방법: Crossref API·출판사·DOI resolve·서지 DB(초안 파일에 URL 전건 기록). master 직접 재검증 7건(존재·필드 일치): ml2024/leviaurbach1999/dreyer2010/bernardi1985/xia2007/marianetti2004/msmr_origin2017 — WebSearch 원문 결과 세션 기록.
- 정정 후 구조 검사: cite↔bib 정합 유지(키 무변경 — 필드만 정정).

## Validation
- Gate "42/42 판정·미판정 0": PASS. Gate "무인용 목록 좌표·배정 전건": PASS(U1–U12). Gate "후보 개념별 ≥1 V1": PASS(MIT·LCO 상도표·MSMR·KWW·Sommerfeld·many-particle 히스·staging 전부 V1 확보). Gate "spot-check": 7/7 일치.

## Gate
**PASS** (PASS_P1_REFERENCE_LEDGER)

## Confirmed Non-Changes
본문 절 파일 무변경(인용 부여는 P2~P5). 수식·라벨·자산 앵커 무변경. 신규 키의 bib 등재는 첫 인용 phase 에서(현재 원장만).

## Open Issues / Decision Queue
- safran1987 = V2 보류(Crossref 권 오기탁) — 필요 시 safran1980(V1) 우선 사용.
- ashcroftmermin1976 쪽수 인용 금지(장 수준만) — 실물 대조는 사용자 로컬 이월.
- numverif2026 의 코드 버전 문자열(v1.0.19) → P8 코드 bump 시 동반 갱신.

## Next
P2(Ch1 Part 0 — 배경+q(T) 2단, 경쟁 저작) 착수 — Step 23 부터.
