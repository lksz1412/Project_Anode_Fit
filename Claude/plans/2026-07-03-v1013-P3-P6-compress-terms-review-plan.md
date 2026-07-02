# v1.0.13 P3–P6 세부계획 (압축 마감·용어 전수·Fable 10회 검수·마감)

> 마스터 = `2026-07-02-v1013-restructure-master-plan.md` rev.4 (Steps 21–45). 우선순위 ①물리 ②비약 ③수식-주도. GO 기집행 중(사용자 부재·자율 완주).

## Summary
P3.1 잔여(압축 p1 적용)·P3.2 완료분 정리 → P4.1 용어·약자 전수(TERMS_POLICY 27+18)·overfull 전수 → P5.1 Fable 단독 10회 가변-청크 검수(수렴=연속 2R 확정결함 0) → P6.1 가이드·샘플·result·ledger·INDEX·HANDOVER.

## Current Ground Truth
- 완료 커밋: 8c4f21e(Part 0+C-1)·4b9480f(Part II 통합)·4f1ab12(루프 A/B)·377b5e6(압축 p2/p3+overfull+FD+Ch2 정합). Ch1 50p·Ch2 14p 0-err.
- 진행 중 sub: p1(lco-center·hys 압축 — 64k 한도 1회 중단 후 분할 저장 재개)·p4(Ch2 revheat·weff).
- 압축 처분 기록: p3 signcheck 콜론계 8건 기각(절감 0.7%·문안 미제시) / p3 목표 미달 절들은 "신규 유도·물리 민감부 보존" 근거 인정(우선순위 ①).
- 루프 B 의도 변경: LCO demo dS_eff·q_rev 전후 대조 커밋 메시지 기록. sample_test_v1013.py 는 T1 재정렬 반영 재실행 필요(P6).

## Phase Range
| Phase | Steps | 내용 |
|---|---|---|
| 3.1잔여 | 21–26 | p1 수신·적용(lco-center·hys) — 물리 보존 선언 검증 후 적용기/수동 |
| 4.1 | 31–34 | TERMS_POLICY 전수 적용(문맥 정독 치환·수식/코드/서지 금지구역 준수)·약자 첫 출현 병기·overfull>10pt 0 |
| 5.1 | 35–40 | 검수 설계(청크·렌즈 로테이션 표) → R1–R10(Fable 병렬 agent, refute·최약 1곳·빈 통과 금지, coverage missing=0) → 라운드별 master 삼각검증·수정·커밋 |
| 6.1 | 41–45 | p4 적용(Ch2)·FITTING_GUIDE 참조 갱신·sample 재실행(glyph 0)·최종 게이트·result·ledger·INDEX·HANDOVER·커밋+푸쉬 |

## Non-goals
물리 결과식·verify10/C-1 판정 변경 X·코드 동작 추가 변경 X(루프 B 완료분 동결)·Ch2 대개편 X.

## P5 검수 설계(확정)
- 라운드 스킴 로테이션: R1 통독(Part 0→II 순차 3분할)·R2 절 단위(신설·이동 절 전담)·R3 식·유도 단위(박스 30 재유도)·R4 라인 단위(부호·첨자 — 무작위 창 6)·R5 도메인=참조·라벨·경계·R6 도메인=수식-주도·산문 예산·R7 도메인=용어·약자 일관·R8 figure(캡션-본문-좌표 3자·TikZ 렌더)·R9 상호충실도(CODE_MAP·가이드·코드 주석)·R10 직전 수정의 새 결함 + 잔여 flag 소거. 수렴 후에도 최소 10R 완주.
- 각 라운드 3–4 Fable agent 병렬(청크 전담 분할), master 삼각검증 후 직접 수정, `V1013_REVIEW_R{n}.md` 기록, 라운드별 커밋.
- 렌즈: ①물리 불변·재유도 ②비약 ③구조(전방 참조 0) ④수식-주도 ⑤용어 ⑥상호충실도 ⑦시각 ⑧신규 결함.

## Test Plan
마스터 Test Plan 승계 + 라운드별: 수정분 빌드 0-err·부호 sweep·회귀 13/13.

## Assumptions
p1 적용 후 lco-center·hys 문장수 재실측으로 LCO 감축 회계 마감(미달 시 잔여는 R6 라운드가 처리 — 강제 재압축은 물리 보존과 충돌 시 하지 않음).

## Correction History
- 초판(P3 진행 중 작성 — P1-P2 세부계획의 후속).
