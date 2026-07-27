# v1.0.10–v1.0.25.2 전체 계보·사용자 의도 재감사 마스터 계획

정본일: 2026-07-28
작업 브랜치: `codex/lib-physics-endgame-v1025_2`
기준 커밋: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`
계획 범위: Phase 055–069, Steps 1–107

## Summary

이 계획의 목적은 새 이론 문건 또는 코드를 작성하기 전에
`Claude/docs/v1.0.10`부터 `Claude/docs/v1.0.25.2`까지의 전체 계보를
문건, 계획서, 결과서, handover, 코드, 시험, 그림, PDF, 데이터 산출물,
관련 Git 이력을 포함하여 다시 감사하는 것이다.

이번 감사에서는 최종 파일만 읽고 과거의 의도를 추정하지 않는다.
각 버전이 해결하려던 문제, 사용자의 요청 방향, 도입한 가정, 뒤에서 철회되거나
변형된 가정, 문건과 코드의 이탈, 실제 데이터 피팅에서 유지된 경험적 요소를
시간순으로 복원한다.

감사가 끝나기 전에는 새 이론의 채택식, 새 코드 구조, 재료별 기본값 또는
최종 목차를 확정하지 않는다. Phase 069의 착수 게이트를 통과한 뒤,
감사 결과를 입력으로 하는 별도의 이론·코드 완결 마스터 계획을 작성한다.

## Current Ground Truth

### 확인된 저장소 상태

- `main`의 최신 `4069cb3`은 v1.0.26 계열이며 이번 과학적 기준선에서 제외한다.
- v1.0.25.2의 두 후속 검토 계열은 공통 조상 `3b5fd05`에서 갈라져 있다.
  - Claude 검토 계열: `e3e1a63`
  - Codex 검토 계열: `11f9054`
- 현재 감사 브랜치는 어느 후속 계열도 정본으로 승격하지 않고
  공통 조상 `3b5fd05`에서 생성했다.
- v1.0.10–v1.0.25.2 범위에는 Git 기준 1,520개 파일과
  862개의 고유 blob이 있다.
- 확장자별 전체/고유 blob의 최초 집계는 다음과 같다.

| 유형 | 전체 파일 | 고유 blob |
|---|---:|---:|
| `.md` | 371 | 245 |
| `.tex` | 821 | 391 |
| `.py` | 129 | 84 |
| `.json` | 26 | 21 |
| `.txt` | 3 | 3 |
| `.html` | 6 | 2 |
| `.pdf` | 70 | 64 |
| `.png` | 85 | 49 |
| `.npz` | 8 | 2 |
| `.pyc` | 1 | 1 |

이 수치는 계획 수립 전 read-only 명령으로 얻은 최초 기준이며,
Phase 056에서 경로·blob·크기·행/페이지 수·생성물 관계를 포함한
정식 manifest로 다시 생성하고 검증한다.

### 잠정 사용자 방향성

다음 항목은 현재 대화와 이전 작업 맥락에서 확인한 잠정 기준이다.
Phase 057에서 실제 계획서, handover, 결과서, commit diff 및 원천 문건의
근거 위치와 연결하기 전에는 역사적 확정으로 표시하지 않는다.

1. 이론 문건은 코드 설명서가 아니라 물리·화학 이론서여야 한다.
2. 코드 언급은 이론 본문 밖의 지정된 구현 계약 문건에서만 허용한다.
3. 코드는 이론 문건에서 채택한 계산 가능한 식과 가정을 전부 반영해야 한다.
4. 외부 누적 용량 좌표 `q`, 재료 조성 좌표, 내부 전극전위와 관측 전압을
   혼동하지 않는다.
5. 전하 보존과 내부 전위 결정이 ICA/DVA 계산의 중심이어야 한다.
6. 저온과 유한전류에서의 dQ/dV 피크 저하·이동·브로드닝을
   열역학, 상전이, 반응속도, 수송, 이질성 및 관측 과정으로 분해한다.
7. 전류를 근거 없이 활성화 장벽의 독립 경험변수로 직접 삽입하지 않는다.
8. 임의 cap, clip, softplus, 근거 없는 threshold 및 사후 Gaussian 폭넓힘을
   물리 모델로 승격하지 않는다.
9. 경험적 피팅 성공과 물리적 상 또는 재료 성분의 식별을 구분한다.
10. 실험으로 식별되지 않은 graphite/LCO/Si 수치를 기본값으로 승격하지 않는다.
11. v1.0.26은 정본 또는 과학적 권위로 사용하지 않는다.

### 아직 확정되지 않은 사항

- 각 방향성이 처음 등장한 정확한 버전, 문장, 사용자 피드백 및 commit.
- v1.0.10 이전 문건에서 v1.0.10으로 승계된 가정의 출처.
- 같은 경로가 여러 버전에 복사됐으나 실제 내용이 달라진 지점.
- PDF와 대응 `.tex`의 정확한 생성 관계 및 빌드 시점.
- 기존 gate가 검증한 범위와 검증하지 못한 범위.
- v1.0.25.2 후속 두 검토 계열에서 채택 가능한 판단.

## Phase Range

| Phase | Steps | 이름 | 핵심 산출물 |
|---|---:|---|---|
| 055 | 1–8 | 기준선·보존 경계 확정 | source-freeze result, branch map |
| 056 | 9–17 | 전체 파일 manifest와 중복 지도 | source manifest, read queue |
| 057 | 18–25 | 사용자 의도·금지·결정 계보 복원 | intent constitution, decision genealogy |
| 058 | 26–32 | v1.0.10–v1.0.13 재감사 | lineage report A |
| 059 | 33–39 | v1.0.14–v1.0.18.2 재감사 | lineage report B |
| 060 | 40–45 | v1.0.19 재감사 | lineage report C |
| 061 | 46–51 | v1.0.20 재감사 | lineage report D |
| 062 | 52–57 | v1.0.21 재감사 | lineage report E |
| 063 | 58–63 | v1.0.22 재감사 | lineage report F |
| 064 | 64–69 | v1.0.23 재감사 | lineage report G |
| 065 | 70–75 | v1.0.24–v1.0.24.1 재감사 | lineage report H |
| 066 | 76–81 | v1.0.25–v1.0.25.2 재감사 | lineage report I |
| 067 | 82–90 | 코드·시험·피팅 계보 교차감사 | code-history report, behavior matrix |
| 068 | 91–98 | 기존 Codex/Claude 검토 재판정 | fork adjudication report |
| 069 | 99–107 | 전체 종합·새 작업 착수 게이트 | canonical audit, launch decision |

## Non-goals

- Phase 055–069 중 기존 Claude 문건, 코드, PDF, 이미지 또는 데이터 파일을
  수정하거나 덮어쓰지 않는다.
- 감사 완료 전 새 이론 본문, 새 재료 모델 또는 생산 코드를 작성하지 않는다.
- v1.0.26A/B를 정본 후보로 검토하지 않는다. 필요 시 반례 자료로만 별도 표시한다.
- 파일명이 최신이라는 이유로 과학적으로 우월하다고 판정하지 않는다.
- 과거 gate의 `PASS`를 새로운 물리 검증의 `PASS`로 자동 승계하지 않는다.
- 동일 blob을 여러 번 읽는 행위를 전수 검독으로 부풀리지 않는다.
- 서로 다른 blob을 “거의 같은 버전”이라는 이유로 생략하지 않는다.
- 관련 논문을 초록, 검색 요약 또는 2차 인용만으로 확정하지 않는다.
- `main`, Claude 후속 브랜치, 기존 Codex 검토 브랜치에 merge하지 않는다.

## Files Created by This Audit

- `Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`
- `Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.json`
- `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
- `Codex/results/PHASE_055_SOURCE_FREEZE_RESULT.md`
- `Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json`
- `Codex/results/PHASE_056_V1010_V1025_2_READ_COVERAGE.json`
- `Codex/results/PHASE_057_USER_INTENT_CONSTITUTION.md`
- `Codex/results/PHASE_057_DECISION_GENEALOGY.json`
- `Codex/results/PHASE_058_066_LINEAGE_REPORT_<A-I>.md`
- `Codex/results/PHASE_067_CODE_HISTORY_AND_BEHAVIOR_REPORT.md`
- `Codex/results/PHASE_068_FORK_ADJUDICATION_REPORT.md`
- `Codex/results/PHASE_069_CANONICAL_REAUDIT_AND_LAUNCH_GATE.md`
- `Codex/results/ACTIVE_HANDOVER_V1010_V1025_2_REAUDIT.md`

필요한 생성 스크립트와 중간 기계 산출물은
`Codex/work/v1010_v1025_2_reaudit/` 아래에만 둔다.

## Phase 055 — 기준선·보존 경계 확정

### Steps 1–8

1. 기준 커밋, 현재 브랜치, 원격 branch tip, 공통 조상을 기록한다.
2. 기존 작업 트리의 사용자 변경과 새 감사 worktree가 분리됐는지 확인한다.
3. v1.0.26 제외 규칙과 v1.0.25.2 기준선의 의미를 명시한다.
4. Claude 후속 2개 commit과 Codex 후속 5개 commit을 별도 입력 계보로 등록한다.
5. `Codex/AGENTS.md`와 phase 운영 지침의 전문 읽기 범위를 기록한다.
6. 기존 Codex 결과서의 마지막 phase 번호와 새 phase 번호의 연결을 설명한다.
7. source-freeze 결과서와 최초 ledger row를 작성한다.
8. Git 상태, JSON/Markdown 경로 및 branch 보호 조건을 검증한다.

### Gate

`PASS_P055_SOURCE_FREEZE`는 기준 commit과 세 입력 계보가 해시로 고정되고,
기존 작업 트리의 변경이 감사 worktree에 존재하지 않으며,
수정 금지 경계가 결과서에 기록된 경우에만 부여한다.

### Stop Condition

공통 조상이 바뀌었거나 원격 tip이 예상과 다르거나,
감사 worktree에 출처 불명의 변경이 있으면 즉시 중단한다.

## Phase 056 — 전체 파일 manifest와 중복 지도

### Steps 9–17

9. v1.0.10–v1.0.25.2의 모든 tracked path와 blob hash를 추출한다.
10. 버전, 확장자, 파일 크기, text/binary, 코드/문건/계획/결과/그림/데이터 역할을 분류한다.
11. text 파일의 전체 행 수와 안정적인 내용 hash를 기록한다.
12. PDF의 페이지 수, 대응 `.tex` 후보, 생성·복제 관계를 기록한다.
13. PNG의 해상도·색상 모드·blob 중복 관계를 기록한다.
14. NPZ의 key, dtype, shape와 비파괴 통계 요약을 기록한다.
15. 동일 blob의 모든 경로를 하나의 dedup group으로 연결한다.
16. 각 고유 blob에 `FULL_TEXT`, `FULL_PDF`, `FULL_IMAGE`, `BINARY_INTROSPECTION`,
    `GENERATED_ONLY` 중 검독 방식을 배정한다.
17. 전체 path 수, 고유 blob 수, 분류 합계가 서로 일치하는지 검증한다.

### Gate

`PASS_P056_COMPLETE_MANIFEST`는 1,520개 기준 path가 빠짐없이 manifest에 있고,
각 path가 한 개의 blob group과 검독 방식에 연결되며,
집계 합이 기준선과 일치할 때만 부여한다.

### Stop Condition

추적되지 않는 외부 include, 깨진 symlink, source가 없는 중요 PDF/데이터,
또는 manifest에 넣을 수 없는 파일이 발견되면 누락 원인을 해결할 때까지 중단한다.

## Phase 057 — 사용자 의도·금지·결정 계보 복원

### Steps 18–25

18. v1.0.10–v1.0.25.2의 plan, result, handover, change log, ledger를 시간순 read queue로 정렬한다.
19. 각 고유 문건 blob을 처음부터 끝까지 읽고 실제 행 범위를 coverage에 기록한다.
20. commit message와 해당 commit의 실제 diff를 연결해 작업 주장과 실변경을 대조한다.
21. 사용자 요청, 모델 제안, 검토 의견, 사용자 승인·철회·정정을 서로 다른 주체로 분리한다.
22. 변수·부호·좌표·장 구조·문체·코드 언급 경계·피팅 목표의 결정 계보를 작성한다.
23. 임의 근사, 금지된 편의항, 보류된 물리, 데이터 없는 기본값을 별도 폐기 계보로 작성한다.
24. 결정마다 최초 근거, 후속 수정, 현재 상태와 충돌 항목을 기록한다.
25. 잠정 방향성 11개를 `확정`, `부분 확정`, `철회`, `근거 미발견`으로 재판정한다.

### Gate

`PASS_P057_INTENT_RECOVERY`는 현재 방향성의 각 항목이 최소 하나의
원천 문장 또는 실제 diff와 연결되고, 상충하는 지시는 시간순으로 해소되며,
근거가 없는 항목은 확정 목록에서 제외될 때만 부여한다.

## Phase 058 — v1.0.10–v1.0.13 재감사

### Steps 26–32

26. 각 버전의 고유 이론 `.tex`와 `.md`를 전문 검독한다.
27. 대응 코드와 시험의 고유 blob을 전문 검독한다.
28. PDF 전 페이지 및 고유 그림을 검독하고 source와 불일치를 기록한다.
29. v1.0.10의 출발 문제, 관측량, 전하 보존, 열·LCO 확장의 실제 범위를 복원한다.
30. v1.0.11–v1.0.12에서 철회·교정된 판단을 확인한다.
31. v1.0.13의 통계역학 재작성과 다회 검수의 실효 범위를 검증한다.
32. 물리·수식·문체·코드 정합 항목을 판정표로 닫는다.

### Gate

`PASS_P058_LINEAGE_A`는 모든 고유 source blob과 PDF/image queue가 완료되고,
버전별 변화가 commit diff와 일치할 때만 부여한다.

## Phase 059 — v1.0.14–v1.0.18.2 재감사

### Steps 33–39

33. 각 버전의 고유 이론·계획·결과 문건을 전문 검독한다.
34. 코드·시험·샘플·golden artifact를 전문 검독 또는 비파괴 조사한다.
35. v1.0.14의 코드 언급 분리, 부호 검산 및 상분리 부록을 재판정한다.
36. v1.0.15의 전압 격자 제거와 trajectory/기억 적분 변화를 검증한다.
37. v1.0.16–v1.0.17의 폭 온도의존과 사용자 리뷰 반영 계보를 검증한다.
38. v1.0.18.1–v1.0.18.2의 Einstein/열물리 확장과 적용 범위를 검증한다.
39. 유지·정정·폐기·이론전용 항목을 판정표로 닫는다.

### Gate

`PASS_P059_LINEAGE_B`는 각 변화가 문건–코드–시험–이력의 네 축에서
대조되고 미검증 항목이 PASS에서 제외될 때만 부여한다.

## Phase 060 — v1.0.19 재감사

### Steps 40–45

40. Ch1/Ch2 master와 모든 고유 section 파일을 전문 검독한다.
41. 재작성 계획, Fable 검수 결과, handover와 code map을 전문 검독한다.
42. `Anode_Fit_v1.0.19.py`, demo, suite, roundtrip, regression을 전문 검독한다.
43. doc-leads 전환이 실제로 코드의 물리 흐름까지 반영됐는지 검증한다.
44. 암묵적 전하수지, 온도·전류 처리, LCO/graphite 관측 경로를 재유도한다.
45. v1.0.19의 채택 가능 핵심과 잔존 결함을 닫는다.

### Gate

`PASS_P060_LINEAGE_C`는 section include 전개 순서 전체와 코드 호출 흐름 전체가
coverage에 기록되고 식별성·단위·부호 검증이 완료될 때만 부여한다.

## Phase 061 — v1.0.20 재감사

### Steps 46–51

46. master plan P0–P8, 모든 phase plan/result/step log를 전문 검독한다.
47. 방향 보고서, style rubric, reference ledger와 경쟁 초안의 역할을 분리한다.
48. 최종 master와 section의 v1.0.19 대비 실제 차이를 검증한다.
49. 문헌 인용과 배경 증축이 계산식의 권위를 부당하게 확장했는지 확인한다.
50. 그림 경쟁·다중 검수의 실질적 과학 검증 범위를 판정한다.
51. v1.0.20의 보존·정정·폐기 항목을 닫는다.

### Gate

`PASS_P061_LINEAGE_D`는 232개 path가 manifest 방식으로 모두 처분되고,
초안과 채택본을 혼동하지 않을 때만 부여한다.

## Phase 062 — v1.0.21 재감사

### Steps 52–57

52. Q0–Q8 계획·결과·handover·ledger를 전문 검독한다.
53. 다클래스 grand-canonical 전하수지와 TST 배경을 원식부터 재유도한다.
54. LCO 심화 및 Si 예비 지도의 문헌·단위·적용 범위를 검증한다.
55. 코드가 v1.0.20/19와 실질적으로 달라졌는지 blob 및 동작으로 대조한다.
56. 추가 서술과 실제 새 물리 폐쇄를 분리한다.
57. v1.0.21의 보존·정정·폐기 항목을 닫는다.

### Gate

`PASS_P062_LINEAGE_E`는 TST partition-ratio의 온도의존,
전하수지 유일성 및 LCO/Si 스코프가 재검증될 때만 부여한다.

## Phase 063 — v1.0.22 재감사

### Steps 58–63

58. R0 이후 모든 계획·결과·lineage audit·handover를 전문 검독한다.
59. 3장 재편의 모든 include와 cross-reference를 실제 순서로 전문 검독한다.
60. graphite, LCO, Si/blend의 공통전위 평형식을 재유도한다.
61. blend의 용량·질량 기준과 equilibrium additivity 한계를 검증한다.
62. Si 값의 근거등급, 히스테리시스 및 finite-rate 비가산성 공백을 확인한다.
63. v1.0.22의 보존·정정·폐기 항목을 닫는다.

### Gate

`PASS_P063_LINEAGE_F`는 재편 전후 내용 손실, 공통전위 폐쇄,
재료별 증거등급이 모두 확인될 때만 부여한다.

## Phase 064 — v1.0.23 재감사

### Steps 64–69

64. P1–P5 계획·결과·handover·reference ledger를 전문 검독한다.
65. JCP147 본문과 ref. 6, 7의 정확한 서지와 수학 구조를 원문으로 확인한다.
66. ratio closure/transfer-function 도입식과 적용 대상을 재유도한다.
67. algebraic charge-balance root와 lag Volterra 문제의 적용 경계를 검증한다.
68. synthetic/Picard/transfer gate와 실제 실험 검증의 차이를 판정한다.
69. v1.0.23의 보존·정정·폐기 항목을 닫는다.

### Gate

`PASS_P064_LINEAGE_G`는 ref. 6, 7을 원문에서 확인하고,
도입법의 변수 매핑·적용 불가 가정·실제 계산 이득이 모두 검증될 때만 부여한다.

## Phase 065 — v1.0.24–v1.0.24.1 재감사

### Steps 70–75

70. 모든 고유 이론·계획·결과·handover를 전문 검독한다.
71. 코드와 profile/default 체계의 변경을 전문 검독한다.
72. skew peak 및 material decomposition의 기원과 해석 범위를 추적한다.
73. default/legacy gate가 어떤 초기화 경로를 실제 검증하는지 확인한다.
74. 문건·코드·가이드의 stale 설명과 동작 불일치를 식별한다.
75. v1.0.24/24.1의 보존·정정·폐기 항목을 닫는다.

### Gate

`PASS_P065_LINEAGE_H`는 fresh-import, explicit profile, legacy restoration을
각각 독립 경로로 시험하고 결과를 분리할 때만 부여한다.

## Phase 066 — v1.0.25–v1.0.25.2 재감사

### Steps 76–81

76. 모든 고유 문건·계획·결과·handover를 전문 검독한다.
77. skew derivative와 direct14 피팅의 수학·수치·데이터 흐름을 재현한다.
78. 저장된 8-digit vector와 원 optimizer state의 차이를 확인한다.
79. direct14의 경험적 성공과 재료 상분해 해석을 분리한다.
80. 4+2, 7+7 및 기타 profile/default 상태와 온도의존을 검증한다.
81. v1.0.25.2의 채택 기준선과 잔존 결함을 닫는다.

### Gate

`PASS_P066_LINEAGE_I`는 실제 피팅 재현, default/fresh-import 검증,
경험적·물리적 권위 분리가 완료될 때만 부여한다.

## Phase 067 — 코드·시험·피팅 계보 교차감사

### Steps 82–90

82. 버전별 Python 고유 blob 전체를 모듈·함수·상태·입출력 기준으로 전문 검독한다.
83. 전압, 전류, 용량, 조성, 온도 좌표의 실제 코드 흐름을 추적한다.
84. 전하수지 root, lag/trajectory, kinetics, heat, observation 순서를 call graph로 만든다.
85. mutable global/default/profile 및 import-time side effect를 추적한다.
86. 모든 test/demo/golden artifact가 실제로 검증한 행위를 기록한다.
87. C-rate/초, 에너지, 엔트로피, 열 및 capacity-basis 단위를 수치 검산한다.
88. overflow, clipping, 정렬, padding 및 numerical fallback이 물리를 바꾸는지 확인한다.
89. 실제 데이터 피팅 경로와 synthetic/demo 경로를 분리한다.
90. 이론식–코드–시험–데이터의 4방향 conformance matrix를 만든다.

### Gate

`PASS_P067_CODE_HISTORY`는 모든 고유 Python blob과 시험 경로가 coverage에 있고,
검증되지 않은 코드를 정상 동작으로 간주하지 않을 때만 부여한다.

## Phase 068 — 기존 Codex/Claude 검토 재판정

### Steps 91–98

91. 공통 조상 이후 Claude 고유 2개 commit의 전체 diff와 산출물을 전문 검독한다.
92. 공통 조상 이후 Codex 고유 5개 commit의 전체 diff와 산출물을 전문 검독한다.
93. 기존 Phase 044 및 Phase 054의 source coverage와 판단 근거를 재검증한다.
94. U13 regular-solution correction과 후속 오류 기록을 독립 재유도한다.
95. 병행 `conformance_model`의 이론 권위, 구현 가치, 중복 계보 위험을 판정한다.
96. 두 fork의 주장 충돌을 원문·수식·실행 결과로 재판정한다.
97. `ADOPT`, `REWRITE`, `REFERENCE_ONLY`, `REJECT`, `UNVERIFIED`로 분류한다.
98. 어떤 commit도 통째로 cherry-pick하지 않고 파일/논점별 채택안을 확정한다.

### Gate

`PASS_P068_FORK_ADJUDICATION`은 양쪽 고유 diff가 전부 coverage에 있고,
자기보고와 실제 Git 상태의 불일치까지 판정됐을 때만 부여한다.

## Phase 069 — 전체 종합·새 작업 착수 게이트

### Steps 99–107

99. Phase 057–068의 결정·결함·보존 항목을 하나의 canonical audit로 통합한다.
100. 사용자 목표를 관측–열역학–동역학–전기화학–재료–피팅 순서로 다시 정식화한다.
101. 이론 본문에 남길 내용과 외부 구현 계약으로 이동할 내용을 확정한다.
102. empirical, reduced-physics, production-physics 모델 계층을 분리한다.
103. graphite, high-voltage doped LCO, Si, graphite+Si별 데이터 요구량과 식별 가능성을 확정한다.
104. 공개 데이터만으로 검증 가능한 주장과 사용자 데이터가 필요한 주장을 분리한다.
105. 새 이론·코드 완결 계획의 입력 요구사항과 선행 문헌 조사 목록을 확정한다.
106. read coverage, manifest, ledger, open issue 및 모든 phase gate를 재검증한다.
107. `GO`, `CONDITIONAL_GO`, `NO_GO` 중 하나로 새 작업 착수 여부를 판정한다.

### Gate

`PASS_P069_REAUDIT_COMPLETE`는 다음이 모두 충족될 때만 부여한다.

- 1,520개 path가 manifest에서 처분됨.
- 862개 기준 고유 blob 또는 Phase 056에서 정정된 고유 blob 전부가 검독됨.
- 모든 고유 text source가 첫 행부터 끝 행까지 coverage에 기록됨.
- 모든 고유 PDF가 전 페이지 검독되고 source 관계가 확인됨.
- 모든 고유 그림이 시각 검독됨.
- 모든 데이터/binary artifact가 비파괴 조사됨.
- 관련 commit의 실제 diff가 모두 검독됨.
- 사용자 의도 계보와 현재 채택 방향이 원천 근거로 연결됨.
- 미검증·근거 미발견 항목이 PASS 주장과 분리됨.
- 기존 이론 및 코드는 아직 수정되지 않음.

## Read-Coverage Interface

각 manifest 항목은 최소한 다음 필드를 가진다.

```json
{
  "path": "Claude/docs/v1.0.XX/...",
  "version": "v1.0.XX",
  "blob_sha": "...",
  "dedup_group": "...",
  "role": "theory|plan|result|handover|code|test|figure|data|generated",
  "review_mode": "FULL_TEXT|FULL_PDF|FULL_IMAGE|BINARY_INTROSPECTION|GENERATED_ONLY",
  "extent": {"lines": 0, "pages": 0},
  "status": "UNREAD|IN_PROGRESS|READ|VERIFIED",
  "coverage": [],
  "review_evidence": [],
  "notes": []
}
```

긴 파일은 연속된 범위로 나누어 읽되 `coverage`의 합집합이
`1..EOF` 또는 `1..last_page`를 정확히 덮어야 한다.
중간 범위가 비면 자동 gate 실패로 처리한다.

## Decision Interface

각 과학·문체·구조 결정은 다음 상태 중 하나만 가진다.

- `PRESERVE`: 현재 방향의 정본으로 보존.
- `CORRECT`: 핵심은 보존하되 수식·단위·표현을 고쳐야 함.
- `SUPERSEDE`: 뒤의 근거 있는 결정으로 대체됨.
- `EMPIRICAL_ONLY`: 피팅·관측 모델로만 허용하며 물리적 실체로 해석하지 않음.
- `THEORY_ONLY`: 이론적 배경 또는 선택 모델이며 생산 구현 권위는 없음.
- `REJECT`: 물리 충돌, 근거 부족 또는 사용자 철회로 폐기.
- `UNVERIFIED`: 근거 부족으로 현재 판정 불가.

각 결정에는 최초 도입 위치, 사용자 반응, 후속 변경, 현재 판정,
문헌 근거 및 코드 영향을 연결한다.

## Validation Plan

### Manifest and coverage

- Git tree path count와 manifest path count 비교.
- blob hash별 dedup group 완전성 검사.
- 확장자·role·review mode 합계 검사.
- text line coverage의 gap/overlap 검사.
- PDF page coverage의 gap 검사.
- JSON parse 및 schema 필수 필드 검사.

### Document and equation review

- include graph 순서대로 `.tex` 전문 검독.
- 식별된 모든 식에 대해 차원, 부호, 독립변수, 경계조건, 극한 검증.
- 동일 기호의 버전간 의미 변경 추적.
- 부분미분, 전미분, 고정 조건과 trajectory derivative 구분.
- 본문 주장과 인용 문헌의 실제 지원 범위 대조.

### Code and numerical review

- 고유 Python blob 전문 검독.
- fresh import와 explicit profile 초기화 분리 시험.
- 정적 call graph와 동적 probe 대조.
- synthetic gate와 real-data fitting 경로 분리.
- 단위·부호·보존·인과성·overflow·수렴 검증.
- stored fit artifact의 재현성과 해석 가능성 분리.

### Git history review

- commit message와 실제 patch 일치 여부 확인.
- merge commit의 각 parent 대비 차이 확인.
- 삭제·rename·복제·되돌림 추적.
- 계획상 완료와 실제 committed artifact의 일치 확인.

## Compaction and Session-Recovery Protocol

작업 재개 시 다음 순서를 강제한다.

1. `git status --short --branch`와 현재 commit을 확인한다.
2. 이 마스터 계획을 처음부터 끝까지 다시 읽는다.
3. execution ledger에서 마지막 `PASS`와 첫 `PENDING`을 확인한다.
4. `ACTIVE_HANDOVER`와 해당 phase result를 전문 재독한다.
5. source manifest와 read coverage에서 마지막 완료 범위를 확인한다.
6. 마지막 phase gate를 재실행한다.
7. 기록과 작업 트리가 일치할 때만 다음 미검독 범위로 진행한다.

대화 요약이나 모델 기억은 진행 증거로 사용하지 않는다.

## Assumptions

- 기준 commit `3b5fd05`의 tracked tree는 v1.0.25.2 공통 기준선의 재현 가능한 입력이다.
- 최초 1,520 path/862 unique blob 집계는 Phase 056에서 정정될 수 있다.
- 동일 Git blob은 byte-identical하므로 한 번의 전문 검독 결과를 모든 경로에 연결할 수 있다.
- PDF가 `.tex`에서 생성됐더라도 PDF 전 페이지의 시각·레이아웃 검독은 별도로 필요하다.
- 외부 논문 원문 접근이 불가능하면 해당 의존 phase는 `CONDITIONAL` 또는 `BLOCKED`로 남긴다.

## Correction History

- 2026-07-28: 이전 최신본 중심 검토안을 대체하고 감사 범위를
  v1.0.10–v1.0.25.2 전체 계보로 확장했다.
- 2026-07-28: 사용자 의도 복원을 버전 내용 감사보다 앞선 Phase 057로 이동했다.
- 2026-07-28: 파일명 기준이 아니라 path–blob manifest와 전 범위 coverage를
  완료 조건으로 채택했다.
