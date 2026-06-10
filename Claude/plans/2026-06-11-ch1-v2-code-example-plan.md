# Ch1 v2 — 예시 구현 절(§1.17) 추가 Plan (V.E)

## Summary
사용자 /goal: "저 문건만 보고 추가 지식 없이 파이썬으로 피팅 식을 세울 수 있나? 가능하면 제대로 된 예시 코드를 **마지막 절로 추가**. 피팅 자체는 사용자가 하므로 **피팅 근사식(모델 함수)** 이 핵심. 필요한 보완은 동일 방법론·작업 순서로. **검수·수정·내용 추가 10회**, 하는 김에 **완전성·물리적 논리 문제점 검토**까지. 전문 생략 없이 읽고 진행."
답은 "예" — §1.15 가 사양이고 R13/R17 round-trip 이 실증. 본 plan 은 그 실증을 문건 본문(§1.17)으로 승격: M1–M6 의 파이썬 직역(주석에 식 번호 1:1) + 단계 회귀 골격 + round-trip 사용 예. 코드는 수록 전 **실행 검증 의무**(문건 밖 가정 0).

## Current Ground Truth
- 본문 1,680행/35p/식 (1.1)–(1.38)/0-0-0, HEAD d6531e8. 전문 재정독 완료(이번 세션, 4분할 전 구간).
- 실증 자산: `results/TBR_R17_roundtrip/`(준평형 S1+S5 PASS), `results/V2_R13_roundtrip/`(꼬리 경로 χ·(1−r_a) PASS).
- 식 번호 확정: eq:logistic=1.11, eq:hysdU=1.34, eq:hyscenter=1.35, eq:master=1.37, eq:hysmaster=1.38 (aux 대조).
- cumulative step 시작 = 151.

## Phase Range
| Phase | 이름 | Steps | 산출 |
|---|---|---|---|
| E.0 | 계획·ledger | 151 | 본 계획서 |
| E.1 | 예시 코드 작성+실행 검증 | 152 | `results/V2_E_codeexample/` |
| E.2 | §1.17 절 작성(절 단위 루프) | 153 | 절 커밋 |
| E.R | 검수·수정·추가 10회(완전성·물리 렌즈 포함, Codex 병행 1회+) | 154–163 | ROUNDS_RESULT 추가 |

## §1.17 절 설계
- 제목: "예시 구현 — 모델 함수에서 round-trip 까지" (마지막 절, §16 뒤·참고문헌 앞).
- 소절 1: 모델 함수(M1–M6 직역, 주석=식 번호) — dU_hys(1.34)/xi_eq(1.11꼴)/ln_Lq(M3=1.27 역)/L_V·r_a(M4)/합산(1.38)/측정축 복귀. numpy 만 사용.
- 소절 2: 단계 회귀의 골격 — S1 잔차 함수(다-peak 동시 회귀의 모델), S3/S4 는 선형 회귀 한 줄임을 명시. 최소화 루틴은 임의의 가중 LSQ(피팅은 독자 몫 — 사용자 명시).
- 소절 3: 사용 예와 검증 — round-trip 실증 수치 요지((7) 규정의 실행), 코드-문건 대응표(함수↔식·M·S).
- 게이트: 수록 코드와 실행 파일이 **동일 텍스트**(diff 0), 실행 PASS 로그 아카이브, 빌드 0/0/0, 코드 줄 폭 ≤72자.

## Non-goals
- scipy 의존·전체 파이프라인 재현(골격은 §15 모듈 순서 참조로 충분). 원본·v1 불가침. ch3/ch4 무수정. 분량 억지 증가 금지.

## Implementation Changes
- 신규: 본 계획서 · `results/V2_E_codeexample/{graphite_ica_model.py, run_log.txt}` · §1.17(tex). ledger·ROUNDS_RESULT 추가.

## Gates
- E.1: 실행 PASS(모델 평가 + 미니 round-trip 1건 — S1 3량 회복 오차 한계 명시).
- E.2: 빌드 0/0/0, 수록=실행 파일 diff 0, 식 번호 인용 전수 일치.
- E.R: 라운드당 [검수→수정→빌드→기록→커밋·푸쉬] × 10, 렌즈에 ①코드-식 1:1 ②실행 재검증 ③**전 문건 완전성(orphan·도입/사용)** ④**물리 논리 적대** ⑤prose ⑥시각 ⑦Codex 적대 병행 포함.

## Test Plan
- python 실행 로그(assert 합격 기준 내장), xelatex 2-pass 광역 grep, 수록-실행 diff, PDF 시각(코드 절 페이지).

## Assumptions
- "마지막 절" = 참고문헌 앞 \section (TOC 포함). "10회" = E.R 라운드 수 하한.

## Decisions Required
- 없음(/goal GO — 무중단).

## Correction History
- (초판) 2026-06-11 /goal 직후 작성.
