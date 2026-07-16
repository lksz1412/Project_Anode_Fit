# Phase P3 세부 계획서 — Ch1 흑연 본론 §3–§10: 중간다리·서지 (Steps 33–44)

## Summary
F-3(히스테리시스 이후 신규 개념 과다·중간다리 부족) 해소: §4 히스(문헌 계보 다리·γ_j/h_η 지위)·§7 broadening(U3)·§9 꼬리(KWW/기억 커널 계보 — 현재 인용 0)·§10(U4)·§5(q(T) 재등장 D7 정합). master 직접 편집(국소 보강 — 경쟁 불요), 신규 인용은 원장 V1 키만(dreyer2011·williamswatts1970·kohlrausch1854 bib 등재).

## Current Ground Truth
sec04 전문 정독 완료(기획 세션). sec03/05/06/07/08/09/10 미정독 → Steps 34–36. 무인용 배정: U2(sec04:125)·U3(sec07:25)·U4(sec10:28). 0-cite 절: sec03·06·08·09. 원장 V1 대기 키: dreyer2011·williamswatts1970·kohlrausch1854·safran1980(선택).

## Phase Range
P3 단독(Steps 33–44).

## Non-goals
수식·수치·라벨 변경 X(다리 문장·인용·소폭 서술 보강만 — 물리 불변). LCO(§11+) X. 경쟁 저작 X(국소 편집).

## Implementation Changes
ch1_sec04(다리·U2)·ch1_sec07(U3)·ch1_sec09(KWW 계보 다리)·ch1_sec10(U4 완화)·(필요시) ch1_sec05 소폭·ch1_bib(+3 서지추가 C-010~012)·CITATION_BASELINE(U2~U4 처리)·CHANGE_LOG(서지추가)·STEP_LOG_P3·RESULT_P3.

## Phase P3 Steps
| Step | 내용 | Gate |
|---|---|---|
| 33 | 본 계획서 저장 | 파일 |
| 34 | sec03·sec05·sec06 전문 정독(D7 대상·다리 필요처 표기) | Read Coverage |
| 35 | sec07·sec08 전문 정독 | 〃 |
| 36 | sec09·sec10 전문 정독 | 〃 |
| 37 | §4 보강: dreyer2010 재인용(U2)+dreyer2011 등재·인용(many-particle 계보 다리)·준안정 가지/과주행 도입 문장·γ_j·h_η 지위 보강 | 편집 완료 |
| 38 | §7 보강: U3(dahn1991 인용) + 개념 다리 점검 | 〃 |
| 39 | §9 보강: KWW 계보 다리(kohlrausch1854·williamswatts1970 등재·인용) | 〃 |
| 40 | §10: U4(편차 주장 완화 또는 근거) | 〃 |
| 41 | §5: q(T) 재등장부 D7 정합 점검(원형 참조 연결) + 기타 정독 중 표기 다리 | 〃 |
| 42 | 빌드 3-pass + 구조 체커 + 스냅샷 diff(변경=서지추가·다리 문장뿐 — eqblocks ~0 기대) | GREEN·diff 대응 |
| 43 | 후방 정합: P2 신설(원형/bgbox) 용어와 §3–10 접속·전이 문구 확인 | 대조 기록 |
| 44 | STEP_LOG·RESULT·ledger·커밋 | 해시 |

## Implementation Interfaces
D8 다리 양식(rubric D3′): [무엇인가 1–3문장 → 문헌 계보(V1 인용) → 본 문건 역할]. 수식 블록 신설 없음(eqblocks diff 0 목표).

## Test Plan
빌드 err0/undef0·cite↔bib 정합(신규 3키 등재·인용 동시)·eqblocks diff ~0/−0·자산 336 보존·U2~U4 처리 기입.

## Assumptions
U4 는 근거 문헌 부재 시 완화 서술로(허위 정밀 금지). safran1980 은 필요해지면 사용(기본 미사용).

## Correction History
(초판)
