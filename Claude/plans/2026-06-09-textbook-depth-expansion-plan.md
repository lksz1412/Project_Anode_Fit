# 교과서 깊이 보강 계획 — Ch1 §8~§11 + Ch2 전반 (PHASE_CM 이어 Phase 4·5)

## Summary
박사님 지적(6-09): 대학 교재 볼륨·깊이 기준에 못 미친다. (1) **Ch1 §1~§7은 충분, §8 이후(종합·겹침·종합모델식·검증반증)가 부실** → 각 절을 한 개념마다 \emph{직관→전 단계 유도→worked example→해석}으로 풀어 교과서 깊이로. (2) **Ch2 전체가 이해 난해** → 직관 선행·중간단계 보강·전개 명료화로 \emph{읽고 따라갈 수 있게} 재서술하며 볼륨도 교재 수준으로. 기존 정확 유도·식 보존, 추가는 진짜 설명(패딩·disclaimer 적층 금지). 대상: `graphite_ica_ch1.tex`(§8~§11), `graphite_ica_ch2.tex`(전반).

## Current Ground Truth
- Ch1 21p(§1~§11, 절번호 1.x). §1~§7 박사님 "충분" 판정. §8 종합·§9 겹침·§10 종합모델식(sec:master)·§11 검증반증 = 보강 대상.
- Ch2 11p(§1~§11, 절번호 2.x). 직전 Phase 3 보강 후에도 "전체 난해" → 절별 이해 가능성(직관·단계) 보강.
- 핵심 유도·수치 손검·Codex 검증 완료(MAJOR 0). 직전 커밋 d1925d0.
- 이전 ledger Next=done(3.9). 본 계획 cumulative step 91부터.

## Phase Range
| Phase | 이름 | Steps | 대상 |
|---|---|---:|---|
| 4.1 | Ch1 §8 종합 심화 | 91–95 | sec:synth |
| 4.2 | Ch1 §9 다중전이 겹침 심화 | 96–99 | sec:overlap |
| 4.3 | Ch1 §10 종합모델식 심화 | 100–103 | sec:master |
| 4.4 | Ch1 §11 검증·반증 심화 | 104–107 | sec:falsify |
| 4.5 | Ch1 빌드·Codex·커밋 | 108–110 | Ch1 |
| 5.1 | Ch2 §서론·§1·§2 이해 보강 | 111–115 | 서론·notation·hys_bg |
| 5.2 | Ch2 §3·§4·§5 clarity 심화 | 116–120 | decomp·spinodal·branch |
| 5.3 | Ch2 §6·§7·§8 clarity 심화 | 121–125 | dQdV·pol·memory |
| 5.4 | Ch2 §9·§10·§11 clarity 심화 | 126–130 | param·fit·master |
| 5.5 | Ch2 빌드·Codex·커밋 | 131–133 | Ch2 |

## Non-goals
- 정확성 확인 유도·식·라벨·식번호 변경 금지(신규만 add). §1~§7(Ch1) 본체 재작성 금지(박사님 "충분").
- 패딩·동어반복·disclaimer 적층·메타발언 금지 — 교과서 prose(직관·예제·해석)로만 볼륨.
- Ch2 단일문건 규율 유지(§1 Chapter-1 언급 0, 인계/전달/결론 절 X). Ch1만 기반.
- 챕터 통째 배치 작성 금지 — 절 단위. Codex/·Archive·zip 미혼입.

## Implementation Changes
- 수정: `graphite_ica_ch1.tex`(§8~§11), `graphite_ica_ch2.tex`(절별). 빌드 pdf 재생성.
- Result: `PHASE_TXB_ch1_RESULT.md`·`PHASE_TXB_ch2_RESULT.md`. Ledger: `PHASE_CM_EXECUTION_LEDGER.md` 에 Phase 4·5 행.

## Phase 4.1 — Ch1 §8 종합 심화
- **Steps 91–95.** §8(종합)에: (a) 닫힌식 조립을 \emph{말로} 단계별 안내(평형 rise + 지연 꼬리가 한 곡선이 되는 그림), (b) 3$\times$3 표 \emph{각 칸의 물리 기전}을 본문 단락으로 풀이(부호·우세조건의 why), (c) \emph{worked example}: 한 전이의 전곡선을 대표 파라미터로 그려보는 수치 산출(peak 높이·FWHM·꼬리 길이), (d) 식별 S1–S4 의 공선형 해소를 더 또렷이.
- **Gate G4.1:** §8에 (조립 안내·3×3 기전 단락·worked example 수치·S1–S4 명료화) 추가 grep; 수치 손검; 빌드 clean·overfull 0.

## Phase 4.2 — Ch1 §9 다중전이 겹침 심화
- **Steps 96–99.** §9에: 겹침의 물리(왜 고율·저온서 융합), deconvolution 비유일성의 직관, $N_p$ 전이 합산 worked example(두 인접 peak 융합 조건 수치), OCV-anchored forward 절차 단계화.
- **Gate G4.2:** §9 보강 요소 존재; 융합 조건 수치 손검; 빌드 clean.

## Phase 4.3 — Ch1 §10 종합모델식 심화
- **Steps 100–103.** §10(sec:master)에: 단계별 피팅 walkthrough(데이터→S1→…→예측을 한 예제로 관통), 전곡선 재구성 예제, 예측 검증 방법.
- **Gate G4.3:** §10 walkthrough·예제 존재; 빌드 clean.

## Phase 4.4 — Ch1 §11 검증·반증 심화
- **Steps 104–107.** §11에: 반증 가능 지문의 물리, 경쟁 기전(확산·접촉·전하전달) 각각의 구별 진단을 표/단락으로 상술, GITT/EIS 진단 절차.
- **Gate G4.4:** §11 진단 상술·경쟁기전 구별 존재; 빌드 clean.

## Phase 4.5 — Ch1 빌드·Codex·커밋
- **Steps 108–110.** 2-pass 빌드 overfull 0·undefined 0; Codex foreground(보강분 물리·수치·정합, MAJOR 0); result+ledger; ch1 tex+pdf 커밋·푸쉬.
- **Gate G4.5:** 빌드 0/0; Codex MAJOR 0(시정 후); git 해시.

## Phase 5.1–5.4 — Ch2 절별 이해 보강
- **Steps 111–130.** 각 절: \emph{직관 선행}(무엇을 왜 하는지 한두 문장 먼저) → 압축된 전개를 \emph{중간 단계}로 풀기 → 필요 시 작은 예제·비유 → 절 끝 한 줄 정리. 난해 지점(부호 반전·spinodal·분기·파라미터화)을 특히 또렷이. 단일문건 규율·식 보존.
- **Gate G5.x:** 각 절 직관·중간단계 추가 grep; 식·라벨 보존; 빌드 clean.

## Phase 5.5 — Ch2 빌드·Codex·커밋
- **Steps 131–133.** 2-pass 빌드 0/0; Codex foreground(clarity 보강이 물리 왜곡 0·정합); result+ledger; ch2 tex+pdf 커밋·푸쉬.
- **Gate G5.5:** 빌드 0/0; Codex MAJOR 0; git 해시.

## Implementation Interfaces
- 보강 prose = (물리적 질문/직관 → 전 단계 유도 → worked example/비유 → 해석/정리). 별행 수식, 인라인 cramming 금지.
- worked example = 대표 수치 대입 → 산출 → 관측 규모와 대조.
- Result 11항목·Ledger 12-col.

## Test Plan
- 빌드 2-pass: overfull 0, undefined 0, 페이지 수 기록(목표 Ch1 §8~ 실질 증가, Ch2 ≥16p).
- 추가식·예제 수치 손검. 라벨 보존 grep. 단일문건 규율 grep(Ch2). Codex foreground 각 챕터 1회.

## Assumptions
- A1: worked example 대표값은 규모 예시(실측 아님) 명시.
- A2: "교과서 깊이" = 직관·중간단계·예제·해석을 충분히 — 물리가 요구하는 만큼(인위 분량 X).
- A3: §1~§7(Ch1)은 박사님 "충분" 판정 존중, 손대지 않음.

## Correction History
- 2026-06-09 v1: 작성. 박사님 "대학 교재 볼륨·깊이 기준, Ch1 §8 이후 부실·Ch2 난해" 수용. PHASE_CM(1~3) 이어 Phase 4(Ch1 후반)·5(Ch2 전반), cumulative step 91부터. "쭉 이어서 진행" → 저장 후 Phase 4.1→5.5 연속.
