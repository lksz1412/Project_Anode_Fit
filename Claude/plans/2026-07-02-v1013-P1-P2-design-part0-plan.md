# v1.0.13 P1–P2 세부계획 (설계 확정 + Part 0 신설 + 흑연부 재배열 + 코드 루프 A)

> 마스터 = `2026-07-02-v1013-restructure-master-plan.md` rev.4 (Steps 1–20 구간). 우선순위: ①물리 ②비약 ③수식-주도.

## Summary
P1.1 설계 4산출물(구조맵·용어표·산문예산·CODE_MAP) → P2.1 Part 0 N=6 경쟁(+Part II 도입 동시 경쟁·figure 포함)+Fable 체리픽 → P2.2 흑연부 재배열·압축(master 절별 루핑) → P2.3 코드 루프 A. 병렬 설계: P1 측정 3 sub 와 P2.1 작성 6 sub 는 상호 독립이라 동시 발진(작성은 P1 산출물에 의존하지 않음 — 교훈 카드·범위는 프롬프트에 자족).

## Current Ground Truth
- docs/v1.0.13/ 증판 완료·버전 패치·회귀 하네스 교정(진짜 verify 13/13 PASS — ledger 정정 기록 참조).
- Ch1 = 2364줄급(v1.0.12 최종 + 사본), LCO 산재 7지점(마스터 Ground Truth), Ch2 = 769줄급.
- 작성 대상 원문 범위: Part 0 원천 = Ch1 sec:width~sec:dist(L918–1139)·Ch2 eq:Z1 절(L120–175) / Part II 도입 원천 = sec:lco-map(L301–355)·lco-hys 분기 부호 문단·lco-peak 방향 규약 문단.

## Phase Range
마스터 Steps 1–20. 1.1(S1–5)·2.1(S6–11)·2.2(S12–17)·2.3(S18–20).

## Non-goals
마스터 Non-goals 승계. 이 세부계획 구간에서는 Part II 이동(S21+)·용어 전수 치환(S31+)은 하지 않음(설계표만).

## Implementation Changes
`V1013_STRUCTURE_MAP.md`·`V1013_TERMS_POLICY.md`·`V1013_PROSE_BUDGET.md`·`V1013_CODE_MAP.md`·`V1013_P21_draft_{F1,F2,S1,S2,C1,C2}.md`·`V1013_P21_map.md`(체리픽)·Ch1 Part 0/Part I 편입판·코드 주석 동기.

## Phase 1.1 (S1–5)
S1 구조맵 = master(이동표·참조 영향— aux 실측). S2 용어표·S3 산문예산·S4 CODE_MAP = sub 3기(Sonnet) 병렬, master 삼각검증. S5 gate: 4산출물·orphan 0.

## Phase 2.1 (S6–11)
S6 원천 정독(각 drafter 자체 수행). S7–S9 = N=6 발진(F1·F2 Fable / S1·S2 Sonnet / C1·C2 Codex — Codex 는 s1(Part 0)→s2(Part II 도입+figure) 스텝별 구동·폴링 감시). S10 체리픽(Fable sub·가중3·figure 매트릭스 포함) → master 재유도 검증. S11 gate.

## Phase 2.2 (S12–17)
master 절별 루핑: Part 0 편입(sec:center 前) → N4/N5 재접속(Part 0 참조로 유도 중복 제거) → LCO 절 추출·후방 이동(내용 불변 이동 먼저) → 흑연 각 절 산문 압축. 중간 빌드.

## Phase 2.3 (S18–20)
CODE_MAP 흑연 구간 양방향 갱신·주석 동기·회귀 13/13 불변 gate.

## Implementation Interfaces
마스터 Interfaces 승계(교훈 카드 7항·figure 양식·CODE_MAP 양식).

## Test Plan
중간 빌드 0-err·회귀 verify 13/13·수치 grep·lco-* 전방 참조 0(S17)·드래프트 물리 자기검수 필수.

## Assumptions
Part 0 배치 = 서론(sec:intro류) 뒤·sec:notation 앞 또는 직후 — 체리픽 시 확정. 산문 예산 수치 = S3 실측 후 이 파일에 추기.

## 산문 예산 확정 (S3 실측 후 추기, 2026-07-02 — 기본값 권한으로 채택)
- 실측: 흑연 본체 386문장/48식(8.04) · LCO 253문장/44식(5.75) · Ch2 230문장/27식(8.52). **LCO 밀도는 오히려 낮음 — "말 많음"의 실체 = 구조(흑연 식 재확인 서술·산재 배치)** → Part II 재조립에서 도입 일원화·mapping 표화로 감축.
- 목표: LCO 10절 개별 ≥35%(253→161, 혼합 −36%) · `sec:broadening` −35%(59문장/1식 최대 outlier — 집합 통계역학 서사는 유지하되 수식·표로 전환) · `sec:revheat` −20% · `ssec:weff` −15% · `sec:signcheck` −10%(감사 기능 보존) · 기타 흑연 절 = 다리 1–2문장 원칙 적용(강제율 없음).
- 근거·상세 = `results/process/V1013_PROSE_BUDGET.md`(재현 스크립트 포함).

## Correction History
- 초판(GO 직후). 병렬 설계(P1 측정 ∥ P2.1 작성) 명시.
