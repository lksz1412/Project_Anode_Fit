# Phase 057K — v1.0.21 Q0 기준선 관찰

정본일: 2026-07-28
세부 Step: 19.5B
범위: 1 unique document, 1,299 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

`snapshot_v1021_q0.json` 1,299행을 네 연속 구간으로 나누어
첫 행부터 끝 행까지 검독했다.

## Provisional Findings

### INTENT-PROV-0075 — Q0는 v1.0.20 final의 구조적 이월이다

Q0의 세 캡처 대상은 다음과 같다.

| 대상 | labels | eqblocks | assets | bib |
|---|---:|---:|---:|---:|
| Ch1 | 225 | 128 | 336 | 36 |
| Ch2 | 69 | 32 | 21 | 16 |
| phase-separation appendix | 30 | 19 | 0 | 0 |

최상위 Ch1/Ch2 파일명을 제외하고 각 entry의 value를 정렬·직렬화한
SHA-256은 v1.0.20 final과 Q0가 모두
`0bbc3e55fdcb81535e81d43ec0c6b2d2af44c951e35434129e709d70ee4b769b`
로 일치했다.

판정:

- 당시 change log의 “복제·버전 표기만” 주장은 구조 필드 기준으로
  `PRESERVE`.
- v1.0.21의 새 자산은 Q0 이후 diff로만 센다.

### INTENT-PROV-0076 — Q0 기준선 자체가 코드 분리 재검토 대상을 포함한다

Q0 label 목록에는 다음 코드 전용 구조가 이미 존재한다.

- `sec:appendix-code`
- `sec:lco-code`
- `sec:lco-code-msmr`
- `sec:lco-code-plugin`
- `tab:nodecode`
- `tab:symcode`

판정:

- 이들은 v1.0.21에서 새로 생긴 것이 아니라 v1.0.20에서 이월됐다.
- 사용자가 허용한 “특정 절”에 해당하는지 최종 문건 아키텍처에서
  명시적으로 판정해야 한다.
- 코드 언급이 이 허용 구역을 넘어 본론 유도·시연에 침투했는지는
  실제 TeX 전문과 후속 버전 diff로 별도 검사한다.

### INTENT-PROV-0077 — 구조 기준선은 물리 검증 기준선이 아니다

Q0는 graphite/LCO의 열역학·히스테리시스·폭·lag·tail,
Ch2 엔트로피·가역열, phase-separation appendix에 걸친
label과 식 hash를 넓게 보존한다. 그러나 각 식의 문자열과 위치가
보존됐다는 사실만 확인한다.

판정:

- Q0는 이후 추가·삭제·변경을 추적하는 기계 기준선으로 `PRESERVE`.
- 다중 성분의 물리적 실재성, 온도·전류 의존 장벽,
  실제 dQ/dV peak 설명력, 코드 일치는 전혀 증명하지 않는다.
- Phase 062·067에서 내용·구현·데이터를 각각 다시 판정한다.

## Coverage Status

- 이 batch의 1문건, 1,299행은 `READ`.
- 누적 coverage 반영은 batch JSON 적용 후 108문건, 19,915행이다.
- v1.0.21 잔여는 8 snapshot, 10,912행이다.

## Next

Step 19.5C:
Q2/Q3 snapshot 2문건, 2,680행을 전문 검독해
다클래스 전하 보존·요동–응답과 TST 확장의 실제 구조 diff를 확인한다.
