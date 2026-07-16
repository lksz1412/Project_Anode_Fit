# Phase P1 세부 계획서 — 서지 원장: 전수 실재 검증·무인용 확정·후보 문헌 (Steps 11–22)

## Summary
이후 전 phase 의 인용 규칙("원장 V1 키만 인용 가능")의 기반인 REFERENCE_LEDGER 를 구축한다: ①기존 42건(ch1 28+ch2 14) 온라인 실재 검증 ②무인용 문헌성 주장 최종 목록 ③보강(D8 다리)용 신규 후보 문헌 사전 검증.

## Current Ground Truth
킥오프 조사 ① §2–3(인용 실태·무인용 12곳 후보). 웹 검증 가동 확인(P0). bib 원문 = `v1.0.20/_sections/ch1_bib.tex`·`ch2_bib.tex`.

## Phase Range
P1 단독(Steps 11–22). 마스터 §4.

## Non-goals
본문 편집 X(인용 부여·정정은 P2~P5 소관). bib 파일 수정 X(정정안만 원장에 기록 — 반영은 담당 phase). 신규 인용 문헌의 본문 배치 X.

## Implementation Changes
신규: `results/V1020_P1_CITATION_BASELINE.md`(무인용 최종 목록)·`results/V1020_REFLEDGER_DRAFT_existing.md`·`results/V1020_REFLEDGER_DRAFT_candidates.md`(sub-agent 초안 2본)·`results/V1020_REFERENCE_LEDGER.md`(master 확정본)·STEP_LOG_P1·RESULT_P1.

## Phase P1 Steps
| Step | 내용 | Gate |
|---|---|---|
| 11 | 본 계획서 저장 | 파일 |
| 12 | 무인용 주장 어간 확장 재스캔(스크립트) + 킥오프 목록 병합 → CITATION_BASELINE 확정 | 목록에 파일:행·주장·필요 문헌 유형 전건 |
| 13–15 | 기존 42건 실재 검증 — sub-agent 1(동기·단독): bib 원문 정독 → 항목별 WebSearch/WebFetch(DOI resolve) → 저자·연도·제목·저널·권·페이지·DOI 필드 대조 → V1/V2/FAIL + 근거 URL → 초안 파일 write | 42/42 판정, 미판정 0 |
| 16 | master spot-check: 초안 중 5건 직접 재검증(무작위+FAIL 전건) — agent 자기보고 불신뢰 규율 | 재검증 일치 |
| 17–18 | 신규 후보 검증 — sub-agent 2(동기·단독): D8 개념별 후보(Mott/Imada MIT·Marianetti Mott-LCO·Van der Ven LCO 상도표·MSMR 원 논문·KWW/Williams-Watts·Ashcroft-Mermin·Safran staging·기타) 정확 서지 확정 → 초안 write | 개념별 ≥1 V1 또는 Gn 명시 |
| 19 | master 원장 확정 조립(V1020_REFERENCE_LEDGER.md — 양식: key·전체 서지·DOI·검증 근거·판정·사용/예정 위치·비고) + spot-check 2건 | 원장 완성 |
| 20 | baseline↔원장 정합(무인용 각 항목에 해소 수단[기존 키/신규 키/완화/Gn] 배정) | 전 항목 배정 |
| 21 | STEP_LOG_P1·RESULT_P1·ledger 갱신 | 기록 완결 |
| 22 | 커밋+푸시 | 해시 |

## Implementation Interfaces
원장 행: `| key | 서지(저자·연도·제목·저널·권·쪽) | DOI | 검증(방법·URL·대조 필드) | 판정 V1/V2/FAIL | 사용 위치(현행)/예정(P2~P5) | 비고 |`

## Test Plan
sub-agent 산출을 master 가 spot-check(≥5건+FAIL 전건). DOI 는 resolve 확인. 판정 기준: V1 = 1차 출처(발행사/DOI 메타)에서 전 필드 일치 / V2 = 2차 출처만 / FAIL = 필드 불일치·실재 불확인(정정안 필수).

## Assumptions
sub-agent 는 단독·동기 실행(병렬 금지 — 체리피킹 아님). 웹 간헐 차단 시 재시도 후 잔여는 미판정으로 두고 STOP 보고.

## Correction History
(초판)
