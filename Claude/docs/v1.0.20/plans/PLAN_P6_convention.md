# Phase P6 세부 계획서 — 전역 컨벤션·용어·어조 통일 패스 (Steps 73–80)

## Summary
rubric(V1020_STYLE_RUBRIC) 기준 전 문건(Ch1 24 + Ch2 15 + appendix_phase_separation) 통일 스윕: ①C-계열 용어 대역표 grep 스윕(위반 목록 → 정정) ②A-계열 어조(메타발언·명령형·전보체) 스팟 스윕 + B7 캡션 점검 ③tab:notation 신설 기호(v1.0.20 신규 — Ξ₁⁰ 등) 등재 검토·반영 ④appendix 표면 정합(내용 불변) ⑤G1~G4 판정·처리. master 직접(표면 편집 — 수식·물리 불변).

## Current Ground Truth
P5 까지 수식 블록 변경 0(diff 근거)·자산 336/21 보존·빌드 65p/25p GREEN. G2 는 P1 C-008 로 기처리(헤더 36종 현행). G3 은 제목 보존 원칙(CLAUDE.md P5)과 rubric "사용자 판단 대기 가능" — 무변경+추가 후보 보고 예정. G1(부록 번호 방식)·G4(bib 키 개명)는 사실 확인 후 위험/이득 판정. tab:notation 위치·현행 등재 목록 미확인(Step 76 에서 확인).

## Phase Range
P6 단독(Steps 73–80).

## Non-goals
물리 모델·수식·수치·라벨·절 번호 변경 X. appendix 내용 재작성 X(용어 표면만). 문건 제목 변경 X(추가 후보 보고만). bib 키 개명 X(판정 기각 예상 — 근거 기록).

## Phase P6 Steps
| Step | 내용 | Gate |
|---|---|---|
| 73 | 본 계획서 저장 | 파일 |
| 74 | C-계열 용어 대역표 grep 스윕(전 파일·용어별 근거 기록) → 위반 정정 | 스윕 기록 |
| 75 | A-계열 어조·메타발언·명령형 스윕 + B7 캡션(개형/수치 평가 명시) 점검 | 스윕 기록 |
| 76 | tab:notation 확인 → v1.0.20 신설 기호 등재 판정·반영 | 전건 등재 |
| 77 | appendix_phase_separation 전문 정독 + 표면 정합 | Read Coverage |
| 78 | G1~G4 판정·처리(근거 기록) | 판정 기록 |
| 79 | 빌드 3-pass + 구조 + diff(스냅샷 p6) | GREEN·1:1 |
| 80 | STEP_LOG·RESULT·ledger·커밋 | 기록·해시 |

## Test Plan
빌드 err0·undef0·페이지수 기록. eqblocks diff ±0(표면 패스 — 수식 불변이 gate). 자산 336/21 보존. 용어 스윕은 grep 명령·매치 수·처리 결과를 STEP_LOG 에 기록(재현 가능).

## Assumptions
표면 정정은 CHANGE_LOG 등재 불요(D11′ — 수식·수치·부호 불닿음; 예외 발생 시 사전 등재 후 진행). tab:notation 등재도 표(산문) 행 추가라 eqblock 불변 예상 — 만약 tab:notation 이 수식 환경이면 B-00x 사전 등재로 전환.

## Correction History
(초판)
