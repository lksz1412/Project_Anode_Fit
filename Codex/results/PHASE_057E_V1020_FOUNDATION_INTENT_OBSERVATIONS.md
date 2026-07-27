# Phase 057E — v1.0.20 foundation 사용자 의도 관찰

정본일: 2026-07-28
세부 Step: 19.4A
범위: 16 unique documents, 885 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 묶음을 첫 행부터 끝 행까지 검독했다.

- master plan 1본: 207행.
- kickoff survey 2본: 126행.
- P0 plan/result/step/change/ledger/style 6본: 237행.
- P1 plan/citation baseline/drafts/result/step/reference ledger 7본: 315행.

최초 master plan·survey 일괄 출력이 중간에서 truncation되어
master plan을 1–70, 71–140, 141–207행으로 다시 나눠 읽고,
두 survey도 독립 범위로 다시 읽었다.
P0 일괄 출력에서는 change log 중간이 잘려 1–43행을 별도로 다시 읽었다.
따라서 이 batch의 885행 전부가 연속 범위 검독으로 복구됐다.

## Provisional Findings

### INTENT-PROV-0026 — 독자 수준과 깊이의 이중 요구

`2026-07-16-v1020-master-plan.md:13-33`은 사용자 피드백을
F-1–F-10으로 보존한다.
특히 F-7은 이공계 교과서 양식, 학부 수준 독자의 자립 추적 가능성,
리뷰 논문 수준의 물리·화학 깊이를 동시에 요구한다.
F-1은 통계역학의 순서와 구성은 좋지만 페르미온·보손의 배경 설명이
빠졌다고 지적한다.
F-3·F-4는 히스테리시스 이후와 LCO를 핵심 난점으로 지목한다.

`V1020_STYLE_RUBRIC.md:5-44`는 이를 완결 명제, 절간 다리,
출발식→연산→중간식→결과식, 극한·부호 검산, 새 기호 즉시 정의,
보편식 선행의 형태로 구체화한다.

판정: 강한 `USER_REQUIREMENT`, `PRESERVE`.

### INTENT-PROV-0027 — 정통 이론을 먼저 닫고 확장을 분리

master plan `:17,39,48-54`의 F-2/D7은 지도교수 감수에서 나온
직접 처방을 기록한다.
표준 Fermi–Dirac 또는 2상태 유도를 먼저 완결한 뒤,
\(q(T)\), 상호작용항, 현상학 인자를 별도 단계로 추가하고,
확장을 끄면 표준 원형이 회수됨을 보여야 한다.

change log `:18-22,39-40`은 이 원칙으로
\(\Xi_1^0\) 원형과 \(q(T)\) 확장을 분리하고,
교환대칭·FD/BE·Mott 판별을 수식화한 이력을 기록한다.

판정: `USER_REQUIREMENT`, `PRESERVE`.
최종 문건에서는 “표준 이론”, “재료 특화 확장”, “현상학적 폐쇄”를
같은 식의 일부처럼 섞지 말고 층별로 표시해야 한다.

### INTENT-PROV-0028 — 인용은 존재 확인만이 아니라 주장-근거 연결

master plan `:25,41,51,107-111`은 다음을 요구한다.

- 인용 전 온라인 실재 검증.
- 저자·연도·저널·권·쪽·DOI 대조.
- 문헌 결과만 떼어 쓰지 않고 선행 이론에서 해당 결과까지 연결.
- 원장에 없는 키와 기억 기반 서지 금지.
- 검증 실패 시 대체 1차 문헌을 찾고, 실패하면 주장 완화 또는 공백 공개.

P1 기록은 기존 42항목을 전수 대조하고,
무인용 문헌성 주장 U1–U12를 파일·행 좌표로 관리했다.

판정: `USER_REQUIREMENT`, `PRESERVE`.
다만 2026-07-16 당시 Crossref/웹 대조 결과는 최종 문헌조사 단계에서
현재 출판사 원문과 다시 검증해야 한다.

### INTENT-PROV-0029 — 계획·스텝 이력은 과학 복구 장치

master plan `:29-33,44,152-159`은
마스터 계획→phase 세부 계획→각 step 즉시 이력→phase result→ledger의
연쇄를 사용자 방식으로 명시한다.
목적은 단순 행정 기록이 아니라 auto-compaction 뒤 임의 추론과
환각을 막는 복구 위키다.
담당 문건 전문 정독과 phase 말 후방 정합 검토도 필수다.

P0/P1 plan과 step log는 이 구조를 실제로 사용했다.

판정: `USER_REQUIREMENT`, `PRESERVE`.
현재 Phase 055–069 운영 구조의 직접 선행 근거다.

### INTENT-PROV-0030 — 이론 본문은 독립 교재, 구현은 외부 계약

master plan `:27-31`의 F-8은 Ch1·Ch2·코드를 동기화된 한 세트로 두되,
문건이 코드에 영향을 주는 `doc-leads` 방향과 본문 코드 언급 금지를
동시에 요구한다. 참고와 appendix만 예외다.

style rubric `:7-10`은 버전 이력, 작업 라벨, 코드 함수명,
방어적 자기고백을 본문에서 제거한다.
change log `:39`는 사용자 지시를
“과거 이력 무관, 이 문서만 보고 이해되는 교과서”로 보존한다.

판정: `USER_REQUIREMENT`, `PRESERVE`.

### INTENT-PROV-0031 — v1.0.20의 서지 정정은 중요한 경고 사례

`V1020_REFLEDGER_DRAFT_existing.md:17-18,42-43`과
change log `:10-17`은 기존 참고문헌에서 다음 오류를 찾았다.

- `ml2024`: DOI와 article number가 실재하는 다른 논문을 가리킴.
- `leviaurbach1999`: 1997 논문 제목과 1999 리뷰의 서지·DOI가 혼합됨.
- 여러 제목 절단, 아티클번호·페이지 누락, MSMR 표기 불일치.

이는 DOI 문자열이 resolve된다는 사실만으로 인용이 옳다고 할 수 없고,
제목·저자·쪽·본문 주장까지 대조해야 함을 보여준다.

판정: 운영 교훈 `PRESERVE`.
과거 원장의 `V1`도 최종판에서는 primary-source 재대조가 필요하다.

### INTENT-PROV-0032 — 구조·회귀 gate의 권위 범위

P0 result/step log는 TeX 빌드, label/cite 구조,
자산 앵커, snapshot 동일성과 코드 회귀 편차를 검증한다.
이들은 복제 무결성, 수치 안정성과 문서 조립 상태를 증명한다.

그러나 master plan `:84-91`은 v1.0.20에서 새 물리와 코드 기능 변경을
범위 밖으로 고정했고, ledger도 대부분 기존 eqblock 보존을 gate로 삼았다.

판정:

- 편집·구조·회귀 보존 증거는 `INTERNAL_CONSISTENCY`.
- 재료 물리 또는 공개 실험 데이터 설명력의 검증 증거는 아님.
- 해당 gate를 과학 완결로 승격하는 것은 `REJECT`.

### INTENT-PROV-0033 — v1.0.20은 의도적으로 물리 완결을 다음 판에 이월

master plan `:64,84-90,202-207` 및 kickoff history `:19-25`는
LCO tier-2/3 실측값, 다온도 전자항 복원, 비가역열 3분해,
\(\Omega(\xi)\), Cahn–Hilliard, Butler–Volmer, PSD를 범위 밖에 둔다.

correction history `:205-207`은 사용자 후속 지시로 다음을
v1.0.21 작업 재료로 이월했다고 기록한다.

- 대정준 전하보존.
- Eyring transition-state theory.
- LCO 확장.
- silicon 이론 접목.
- 일반 확장 후보와 새 그림.

마지막에는 실측 데이터 부재로 확인·피팅을 회사에서 수행할 예정이라고
명시한다.

판정:

- v1.0.20은 설명·서지 정련판으로 `PRESERVE`.
- 현재 목표인 LCO/graphite/Si/graphite+Si 실데이터 물리 완결판의
  종점으로 보는 것은 `REJECT`.
- 이월 항목은 v1.0.21 이후 계보에서 채택·왜곡·누락 여부를 추적한다.

## Conflicts to Carry Forward

1. v1.0.19를 “전체적으로 제대로”라고 한 당시 사용자 평가는
   v1.0.20 증판 착수 승인이지, 현재 재감사에서 과학 오류를 면제하는
   영구 판정이 아니다.
2. “기존 물리 불변”과 “오류 발견 시 수정” 규칙이 동시에 존재한다.
   최종 기준은 근거 있는 오류 정정을 허용하되 변경 원장을 남기는 것이다.
3. Crossref 확인은 서지 식별에 유용하지만, 문헌의 물리 주장을
   지지하는 정확한 본문 위치까지 검증하지는 않는다.
4. 문건 asset 보존과 과학적 진실 보존은 동일하지 않다.
5. v1.0.20의 새 background 식이 교과서 표준이라는 자기 보고는
   Phase 061 및 최종 문헌감사에서 직접 재유도·원전 대조해야 한다.

## Coverage Status

- 이 batch의 16문건은 `READ`.
- 누적 Phase 057 coverage: 38문건, 2,343행.
- v1.0.20 잔여: 65문건, 16,156행.
- 아직 Phase 057 최종 `VERIFIED`가 아니다.

## Next

Step 19.4B:
P2 Part 0, P3 graphite, P4 LCO, P5 Ch2, P6 convention의
plan/result/step/competition judgment 21문건, 815행을 전문 검독한다.
