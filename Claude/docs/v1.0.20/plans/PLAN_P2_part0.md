# Phase P2 세부 계획서 — Ch1 Part 0: 양자통계 배경 + q(T) 정통 유도 선행 재배열 (Steps 23–32)

## Summary
F-1(페르미온/보손 배경)·F-2(교수 감수: 원문식 선행) 를 Ch1 Part 0 에 반영한다. 핵심 = §2.2(단일 삽입 자리) 를 [원형(내부 자유도 없는 2-상태) 유도·박스 → 배경 bgbox(페르미온/보손/FD·BE) → 확장(q(T)) 유도·박스 → 원형 회수 검산] 의 D7 2단 구조로 재배열 — **Ch2 §2.1 의 기존 순서(정통 선행)와 챕터 간 정합**. 신규 콘텐츠는 경쟁 저작(N=4: Opus×3+Fable×1, 병렬 허용)으로 생산, master(Fable) 체리픽 통합.

## Current Ground Truth
- 대상 전문 정독 완료(이번 세션): sec00(1–91)·sec01(1–205)·sec02a(1–268)·sec02b(1–329). q(T) 첫 등장 = sec02a eq:partfn(L125–130) — 원형 단계 없음. FD 동형 가드 = eq:fermifn verifybox(L172–185). 페르미온/보손 배경 부재(전 문건 한글 "페르미온" 1회 뿐).
- 원장 발효: 인용 가능 = V1 키만(P2 소관 후보: hill1960·fowler1939·mcquarrie1976·mckinnon1983·[배경 보조] ashcroftmermin1976).
- 무인용 배정: U1(sec01:91 staging 초기값 — 인용 전방 배치)·U12(sec01:170 — 기각 후보 확정 처리).

## Phase Range
P2 단독(Steps 23–32).

## Non-goals
sec02b·sec03 이후 내용 변경 X(접합 확인만). 기존 라벨·최종 식·수치·자산 앵커 변경 X. 물리 확장 X(배경·재배열·중간식 노출만).

## Implementation Changes
- `_sections/ch1_preamble.tex`: bgbox 환경 신설(+ch2_preamble 동시 — P5 대비).
- `_sections/ch1_sec02a_part0.tex`: §2.2 소절 교체(경쟁 통합본 — 원형→bgbox→확장), 나머지 소절 불변.
- `_sections/ch1_sec01_n0n1.tex`: U1 인용 부여(tab:staging 참조부).
- 경쟁 산출 보존: `results/comp_P2_part0/`(AUTHOR_BRIEF·draft_o1/o2/o3/f1.tex·PICK_JUDGMENT.md).
- CHANGE_LOG: B-001(2단 재배열)·B-002(배경 bgbox)·B-003(bgbox 환경) 사전 등재.

## Phase P2 Steps
| Step | 내용 | Gate |
|---|---|---|
| 23 | 본 계획서 저장 + CHANGE_LOG 사전 등재(B-001~003) | 파일·등재 |
| 24 | 대상 정독 확인(Read Coverage 인계 — 세션 내 전문 정독 4파일) + 편집부 재정독 | RESULT 기재 |
| 25 | bgbox 환경 정의(ch1·ch2 preamble) + 빌드 스모크 | 빌드 GREEN |
| 26 | 경쟁 브리프 작성(원문 소절·rubric·원장 발췌·보존 체크리스트·산출 형식) | 브리프 완비 |
| 27 | ★경쟁 초안 4본(Opus×3+Fable×1, **병렬**) → draft 파일 4본 | 4본 존재·각 보존 체크 자기보고 |
| 28 | master 교차검토(보존 체크리스트 대조·오류 표)·체리픽 통합 → sec02a 반영 | PICK_JUDGMENT 기록 |
| 29 | U1 인용 부여·U12 기각 확정(baseline 기입) | baseline 갱신 |
| 30 | 빌드 3-pass + 구조 diff(신규 eqblock/라벨 ↔ CHANGE_LOG 1:1) | GREEN·diff 대응 |
| 31 | 후방 정합: sec02b·sec03 접합부(eq:fermifn·eq:sm-epstilde 참조처)·Ch2 §2.1 서술("Part 0 가 자세히 세웠다") 정합 재확인 | 대조 기록 |
| 32 | STEP_LOG·RESULT·ledger·커밋 | 해시 |

## Implementation Interfaces
- 경쟁 산출 = §2.2 소절 대체 블록(`\subsection{단일 삽입 자리...}` 부터 `\subsection{$M$ 개의 독립 자리` 직전까지)의 완결 tex. 시작·끝 마커 주석 필수.
- 보존 체크리스트(브리프 §C — 전 초안 의무): 가정 1/2·미시상태 온전 기술·eq:partfn/eq:sm-occmid/eq:sm-epstilde/eq:fermifn/eq:sm-flucres/eq:sm-sint 라벨·최종형 불변·q(T)↔용량 q 각주·조화 우물 q 고전/양자형·★FD 동형 가드·요동-응답·ε̃ 하류 두 갈래 단락·Ch2 참조 문구.
- 체리픽 규칙: Fable 초안 가중 3·이식 금지 = 검토가 잡은 오류·베이스 1본 + graft.

## Test Plan
빌드 3-pass(err0·undef0)·구조 diff(eqblocks 추가분만·삭제 0·기존 해시 불변 확인 — B-001 재배열로 §2.2 내 기존 블록 이동은 해시 불변이어야 함)·자산 앵커 수 불변·페이지 증가 예상(62→63±1).

## Assumptions
경쟁 초안이 전부 부적합하면 master 직접 작성으로 폴백(브리프 기준). U12 기각 = 사용자 확인 불요(모델 부호 서술 — 4-tier 확정 근거 기재).

## Correction History
(초판)
