# Phase 057AR — v1.0.25 T13/T14 집행 보고 관찰

정본일: 2026-07-28
세부 Step: 19.8L
범위: 1 unique document, 487 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `Claude/docs/v1.0.25.1/results/V1025_T13_T14_REPORT.md`

1–240, 241–487의 연속 범위로 나눠 첫 행부터 마지막 행까지
전량 검독했다.

## Provisional Findings

### INTENT-PROV-0326 — version 표시만 바꾸고 식별자·파일명을 유지한 것은 사용자 결정이다

T14는 master TeX 세 파일의 사람이 읽는 version 문자열만
v1.0.25로 바꾸고 filename, input path, external-document key를
유지했다. 이는 DG-2 사용자 결정을 직접 기록한다.

판정:

- 계보 사실로 `PRESERVE`.
- 파일명 token과 문서의 과학적 version을 혼동하지 않는다.
- 최종 artifact는 불필요한 rename 없이 stable identifier와
  semantic release metadata를 분리한다.

### INTENT-PROV-0327 — “protocol만 바꾼 대조”라는 A2 해석은 파일 key 증거와 맞지 않는다

보고서가 열거한 Zenodo key에서 graphite p-ocv와 p-ocvhold는
서로 다른 specimen UUID를 가진 별도 파일이다. 날짜가 겹치는
쌍은 있어도 동일 cell에서 hold만 on/off한 paired trajectory라는
증거가 아니다.

판정:

- p-ocvhold fit이 더 높았다는 관찰값은 `PRESERVE_AS_REPORTED`.
- 개선분을 protocol 효과 또는 비평형 잔여에만 귀속한 인과
  주장은 `REJECT_AS_UNCONTROLLED`.
- 같은 electrode의 paired protocol이 없으면 cell random
  effect를 둔 계층 비교와 충분한 replicate를 요구한다.

### INTENT-PROV-0328 — protocol source mapping은 강하지만 재현 package는 보존되지 않았다

`gr.csv`와 `si.csv`는 각 후보 중 유일하게 길이가 일치하고
저장 반올림 폭 내에서 값이 맞아 각각 gr_A, si_Dhold로
판정됐다. 하지만 원 parquet/JSON과 `verify_protocol.py`는
session scratch에만 있었고 checksum·fetch script가 repo에
남지 않았다.

판정:

- mapping은 `HIGH_CONFIDENCE_REPORTED`.
- 독립 재현 authority는 `INCOMPLETE`.
- Zenodo record/version, exact file key, checksum, transform
  script와 output을 보존해야 한다.

### INTENT-PROV-0329 — 실행 보고서 자체도 이동 중인 source snapshot을 기록했다

보고서 첫 표는 자기 줄 수를 484로 적지만 최종 physical line은
487이다. structure check도 master가 `_sections`를 편집 중인
01:52 snapshot에서 실행됐고, 당시 `eq:skewpeak`가 아직 검사
대상이 아니었다.

판정:

- 그 PASS는 최종 v1.0.25 source 검증이 아니다.
- 보고서 생성 중 self-count와 검증 결과는 freeze commit 이후
  다시 만들어야 한다.
- 최종 workflow는 동시 편집이 끝난 immutable commit에만
  acceptance status를 부여한다.

### INTENT-PROV-0330 — 변경 최소성은 높지만 stale title 보존은 독자 정직성을 해친다

ARCHIVE_NOTE의 기존 40줄과 “v1.0.24.1 동결 아카이브” 표제를
삭제하지 않고 v1.0.25 정정 절을 하단에 붙였다. 과거 주장을
보존하려는 의도는 좋지만 폴더 첫 문장이 현재 지위와 어긋난다.

판정:

- historical source는 수정하지 않고 보존한다.
- canonical index와 release note는 현재 지위를 첫 화면에서
  정확히 밝혀야 한다.
- “삭제 금지”를 misleading heading 보존보다 우선하지 않는다.

### INTENT-PROV-0331 — master 파일에서 code 문자열이 없다는 검사는 이론 문건의 코드 배제를 보증하지 않는다

세 master TeX에서 `Anode_Fit` 문자열이 0회인 것은 확인됐지만,
입력 목록에는 Ch1/Ch2 code map appendix와 Ch3 code section이
포함돼 있다. master wrapper만 grep한 검사는 합성 문서 내용의
코드 배제를 보증하지 않는다.

판정:

- 최종 이론 문건은 transitive input 전체를 대상으로 code
  reference audit를 수행한다.
- implementation material은 별도 companion으로 이동한다.

### INTENT-PROV-0332 — 수치 출처 표시와 미측정 표기는 좋은 정직성 자산이다

보고서는 master가 준 수치, sub-session이 직접 확인한 사실,
미측정 항목을 명시적으로 구분하고, 서로 다른 ablation
조건의 순위 역전을 같은 실험처럼 쓰지 않는다.

판정:

- attribution과 `미측정` 표기 관행은
  `PRESERVE_AND_FORMALIZE`.
- 단, “직접 확인”에는 실행 script·input hash·commit SHA가
  함께 있어야 한다.

### INTENT-PROV-0333 — 구조 검사와 실제 build는 역할이 다르다는 경계는 정확하다

TeX tool 부재를 확인하고 build를 했다고 주장하지 않았으며,
structure check가 조판·문법·page layout을 대체하지 못한다고
밝혔다.

판정:

- 검증 범위의 정직한 제한은 `PRESERVE`.
- v1.0.25.1 이후 실제 XeLaTeX build 증거와 chronology를
  따로 대조한다.

### INTENT-PROV-0334 — 핵심 과학 공백은 보고서 말미에도 열린 채 남아 있다

raw data 영구보존, 재현 script, graphite phase count,
regsol 철회의 다중-cell 통계, 독립 gate 재실행이 U6–U10으로
남았다. 또한 이 작업은 high-voltage doped LCO나 온도·전류
series를 다루지 않았다.

판정:

- v1.0.25 T13/T14는 provenance 정정 phase이지 모델 validation
  완료가 아니다.
- 이 미해결 항목을 이후 version의 완료 문구가 실제로 닫았는지
  추적한다.

## Direction Recovered

1. 원본 version을 보존하면서 새 판정은 후속 기록으로 남긴다.
2. 파일명 안정성과 표시 version을 분리한다.
3. 실행 주체와 미실행 항목을 정직하게 표시한다.
4. 앞으로는 scratch 증거를 남기지 말고 재현 package로 승격한다.
5. protocol 효과와 cell 차이를 분리하지 않은 인과 해석은 금지한다.
6. wrapper grep이 아니라 합성된 이론 문건 전체에 코드 배제 gate를
   적용한다.

## Coverage Status

- 이 batch의 1문건, 487행은 `READ`.
- 누적 coverage 반영 후 목표는 262문건, 52,357행이다.
- 전체 Phase 057 잔여 목표는 9문건, 5,438행이다.

## Next

Step 19.8M:
v1.0.25 document edit report 1문건 312행을 전문 검독한다.
