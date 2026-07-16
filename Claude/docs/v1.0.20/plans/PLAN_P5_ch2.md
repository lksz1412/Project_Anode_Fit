# Phase P5 세부 계획서 — Ch2: 정통 유도 정합·배경 연결·Ch1 정합 (Steps 63–72)

## Summary
Ch2 전 절 전문 정독 후: ①D7/D3 점검(§2.1 은 이미 정통 선행 — P0 확인; §2.3 BE/FD 닫힌형의 중간식 노출 후보) ②Ch1 신설 배경(페르미온/보손 bgbox)과의 분업·서술형 참조 연결 ③U9·U10 처리(ch2_bib 에 dahn1991·ohzuku1993 등재 필요) ④Ch1 v1.0.20 변경과 교차참조 정합 확인. master 직접(소규모 편집 — 대형 유도 신설 없음 예상; 정독 후 재판정).

## Current Ground Truth
정독 완료: sec00(68)·sec01(144)·sec03(95). 미정독: sec02(188)·sec04(115)·sec05(240)·sec06(52)·sec07(58)·sec08(144)·sec09(43)·sec10(25)·appA(74)·appB(69). U9(sec05:168–169)·U10(sec02:9, low). Ch1 골격·라벨 불변이므로 Ch2 의 리터럴 교차참조는 유효 예상(확인 필요).

## Phase Range
P5 단독(Steps 63–72).

## Non-goals
물리 모델·수치·라벨 변경 X. appB(코드 요구명세) 내용 변경 X(P8 소관 버전 표기 제외). 대형 재구성 X.

## Phase P5 Steps
| Step | 내용 | Gate |
|---|---|---|
| 63 | 본 계획서 저장 | 파일 |
| 64–66 | sec02·04·05 / sec06~10 / appA·appB 전문 정독 + 보강 지도 | Read Coverage |
| 67 | 보강 지도 확정(D7/D3 대상·배경 연결 위치·U9/U10) — CHANGE_LOG 사전 등재(필요분) | 지도 |
| 68 | 편집: §2.3 배경 연결(Ch1 배경 박스 서술형 참조)·D3 중간식(판정 시)·U9(+ch2_bib 등재)·U10 | 편집 완료 |
| 69 | 빌드 3-pass + 구조 + diff | GREEN·1:1 |
| 70 | 후방 정합: Ch1↔Ch2 교차참조(절 번호·기호 Ξ₁·q(T)·eq:Se-ch2)·rubric | 대조 기록 |
| 71 | baseline 기입·STEP_LOG·RESULT·ledger | 기록 |
| 72 | 커밋+푸시 | 해시 |

## Test Plan
빌드 err0·cite↔bib 정합(신규 키 등재+인용 동시)·eqblocks diff ↔ CHANGE_LOG 1:1·자산 앵커(Ch2 21태그) 보존.

## Assumptions
D3 중간식 삽입은 물리 불변 보강(수식 블록 추가 가능 — B-00x 사전 등재 후). 경쟁 불요 판정 유지(정독 후 뒤집히면 Correction).

## Correction History
- (Step 69) **빌드 환경 재구축 1건**: 컨테이너 재생성(작업 볼륨 유지·루트 FS 초기화)으로 P0 설치분 중 `texlive-fonts-recommended`(hyperref xetex 드라이버의 pzdr.tfm 소속) 소실 → Ch2 3-pass가 preamble 에서 전패("No pages of output"). apt 재설치 후 Ch1 65p·Ch2 25p 재현(err0·undef0) — 문건·계획 내용 변경 없음, 환경 사건만 기록.
