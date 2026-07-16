# Phase P7 세부 계획서 — 통합 검수: 4창 union·교차합의 triage·최종 Fable 패스 + 서지 3자 정합 (Steps 81–90)

## Summary
사용자 확정안(D-9 축소 대체): **검수 4창 = Opus×3 + Fable×1**(병렬 — 체리피킹 케이스 허용 범위), 창별 담당 청크 + 공통 3축(신본 결함 / v1.0.19 regression / 신설 다리 물리·서지) → master(Fable) union 취합 → **교차합의 triage**(≥2창 공통 = 채택 후보 / 단독 = master 재정독·재유도 확정 후에만) → master 수정 → **최종 Fable 검수 패스**(다른 청크 스킴·수정 회귀 1급) → 연속 2R 신규 0 까지. 병행: master 직접 **서지 3자 정합**(cite↔bib↔원장 스크립트 전수 + appendix [A1]~[A5] 온라인 검증 — P6 발견 큐).

## Current Ground Truth
P0~P6 PASS. 빌드 65/25/8p GREEN·diff 이력 전건 CHANGE_LOG 1:1·무인용 U1~U12 전건 처리. 신설 다리 목록 = P2(§2.2 2단+bgbox)·P3(§4 계보·U2~U4)·P4(§15.1 MIT bgbox·§13/§17 계보·U5~U8/U11)·P5(Ch2 U9/U10·§2.3 다리·B-005)·P6(표면 3묶음). 원본 v1.0.19 = `../v1.0.19/`(불가침 — read 만). appendix 서지 5건 원장 밖(P6 발견).

## Phase Range
P7 단독(Steps 81–90).

## Non-goals
대형 재구성 X. 창의 실수정 X(read-only 검수 — 수정은 master 만). 원장 밖 신규 인용 추가 X(필요 시 원장 등재 선행). Codex/ 접근 X.

## Phase P7 Steps
| Step | 내용 | Gate |
|---|---|---|
| 81 | 본 계획서 저장·검수 브리프 확정 | 파일 |
| 82 | 4창 병렬 기동(O1=Ch1 §0~5 / O2=Ch1 §6~10+부록 / O3=Ch1 §11~18 / F1=Ch2 전체+appendix) — 조기 저장·완주 마커 | 기동 4 |
| 83 | (병행) master 서지 3자 정합 스크립트 전수(cite↔bib↔원장) | 0 불일치 |
| 84 | (병행) appendix [A1]~[A5] 온라인 검증·원장 등재 | 5/5 판정 |
| 85 | 4창 완주 수합(생존 규칙: ≥3 완주 + 커버리지 결손 시 master 직접 보충) | 커버리지 |
| 86 | union 취합·교차합의 triage(Fable 가중 3·단독 지적은 재정독/재유도 확정) | 전건 판정 |
| 87 | master 수정 집행(채택분 — CHANGE_LOG 사전 등재 규칙 준수) | 편집 |
| 88 | 최종 Fable 검수 패스(다른 청크 스킴 — 수정 회귀 1급) + 필요 시 재라운드 | 연속 신규 0 |
| 89 | 빌드+구조+diff(p7)·무인용 재확인 | GREEN·1:1 |
| 90 | STEP_LOG·RESULT·ledger·커밋 | 기록·해시 |

## Test Plan
3자 정합 = 스크립트(전 cite 키 → bib 존재 → 원장 V1 존재) 0 불일치. 창 커버리지 = 담당 파일 전문 정독 확인(REVIEW 파일의 파일별 언급). union 전건 = 발견 각각 [채택/기각+근거] 기록. 빌드 err0·diff ↔ CHANGE_LOG 1:1.

## Assumptions
창 사고(API 오류·유실) 시 P4 선례 준용: 생존 ≥3 + Fable 결과 확보(최종 Fable 패스가 Fable 몫 겸임 가능) 면 진행, 결손 청크는 master 직접 검수로 보충. 검수 창 출력은 파일 조기 저장으로 유실 최소화.

## Correction History
(초판)
