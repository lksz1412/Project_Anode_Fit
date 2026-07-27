# Phase 057BI 충돌 해소·사용자 방향 헌법 결과

정본일: 2026-07-28  
대상 단계: Phase 057 Steps 24.1–24.5

## 판정

`PASS_P057_CONFLICT_RESOLUTION`

22개 방향성 decision과 20개 금지·철회·보류 계보를 시간순으로 대조해
현재 사용자 방향 헌법을 작성했다. 이 헌법은 이론 정본이 아니라
후속 감사와 endgame 작업의 변경 통제 기준이다.

## 주요 충돌 해소

| 과거 결정 | 현재 해소 |
|---|---|
| 문건–코드 유기성을 위해 본문에 code map 포함 | 과학 내용의 100% 충실성은 보존, 구현 정보는 companion으로 이동 |
| v1.0.25 code-first 후 문건 cascade | 현재 theory→contract→code 방향이 supersede |
| v1.0.25 국소 patch 범위 | 당시 이력으로 보존, 현재 endgame 전면 감사 범위를 제한하지 않음 |
| theory regsol / fitting logistic 병치 | 역사적 실용 결정으로 보존, 최종 100% closure로는 불충분 |
| 7-gallery skew default | 철회, empirical opt-in만 보존 |
| bit-exact legacy 우선 | legacy gate로 분리, 새 physics/default gate를 막지 않음 |
| cap/clamp를 수치 안전과 혼용 | invalid input rejection만 보존, silent value shaping은 거부 |
| file name 불변 | 과거 release 결정으로 보존, 새 과학 architecture의 절대 제약 아님 |
| fit 우세를 phase evidence로 사용 | calibration signal과 phase identification을 분리 |
| LCO/Si placeholder와 seed | dataset-specific seed로 강등, material default 권위 제거 |

## 완전 대체와 범위 축소

완전 대체:

- code-first authority
- 7-gallery default
- theory manuscript 내부 구현 정보
- arbitrary silent cap/clip/clamp
- v1.0.26 authority

범위 축소:

- skew/gallery basis → empirical observation candidate
- regular-solution → theory/rederivation candidate
- legacy bit-exact → legacy regression 범위
- R²/BIC → calibration ranking 범위
- 과거 “완결” → 해당 phase가 실제 검사한 범위
- v1.0.25 국소 patch → 역사적 작업 범위

## 산출물

`Codex/results/PHASE_057_USER_INTENT_CONSTITUTION.md`

헌법은 기준선, 문건 성격, 좌표, 물리 계층, 핵심 현상, 재료별 책임,
열역학–경험식 경계, 데이터·검증, 수치 원칙, theory–code 100% 반영,
작업 기록, 미확정 영역과 변경 조건을 명시한다.

## 다음 단계

Phase 057 Step 25에서 coverage, actor, evidence, conflict, 잠정 방향 11개와
헌법을 적대 검증한다. PASS 전에는 이 헌법을 새 이론의 과학적 정본으로
승격하지 않는다.
