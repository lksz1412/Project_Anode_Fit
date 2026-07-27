# Phase 057BD 완료·권위·불변·정합 선언 판정 결과

정본일: 2026-07-28  
대상 단계: Phase 057 Step 20.4  
기준 커밋: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`

## 판정

`PASS_P057_COMPLETION_CLAIM_ADJUDICATION`

이 판정은 3,487개 후보의 처분이 빠짐없이 기록됐다는 뜻이다.
과거 문건의 `PASS`를 현재 과학적 PASS로 승계한다는 뜻이 아니다.
뒤의 버전별 물리·코드 재감사에서 새로운 독립 증거가 나오면
`PARTIAL`과 `UNVERIFIED`는 근거를 남기고 승격 또는 강등할 수 있다.

## 판정 정책

1. 먼저 부정·제한, 미래 계획·gate 정의, 인용·stale 논평을
   긍정 주장 모집단에서 제외했다.
2. 긍정 주장은 `CONFIRMED`, `OVERCLAIMED`, `PARTIAL`,
   `UNVERIFIED` 네 상태 중 하나를 반드시 받는다.
3. 같은 commit에 코드·이론·시험이 모두 있어도 서로 독립된 검증이
   아니므로 자동 판정의 상한은 `PARTIAL`이다.
4. result나 commit subject의 자기보고만 있으면 `UNVERIFIED`가 기본이다.
5. `CONFIRMED`와 `OVERCLAIMED` 수동 판정은 이번 전문 검독에서 저장한
   구체 근거가 있을 때만 허용했다.

이 정책은 “증거가 없으므로 거짓”이라고 단정하지 않는다. 반대로
“기록에 PASS라고 쓰였으므로 참”이라고도 단정하지 않는다.

## 전체 처분

| 처분 | 위치 수 |
|---|---:|
| 전체 후보 | 3,487 |
| 긍정 주장 | 3,080 |
| 부정·제한 문맥 | 339 |
| 계획·통과조건 | 27 |
| 인용·stale·자기보고 논평 | 41 |

긍정 주장 3,080개의 네 상태 합은 정확히 3,080이다.

| 판정 상태 | 위치 수 | 의미 |
|---|---:|---|
| `CONFIRMED` | 3 | 현재 독립 근거로 확인 |
| `OVERCLAIMED` | 4 | 표현 범위가 증거·현재 상태를 초과 |
| `PARTIAL` | 961 | 일부 실행·patch 증거는 있으나 선언 전체는 미입증 |
| `UNVERIFIED` | 2,112 | 독립 증거가 없거나 요구 증거 축이 부족 |

`CONFIRMED` 3건은 독립된 세 사실이 아니라 같은 현재 권위 사실의
세 원문 위치다. 즉 v1.0.25.2가 이번 작업의 최신 과학 기준선이라는
사실을 `ARCHIVE_NOTE` 한 곳과 최종 handover 두 곳에서 확인한 것이다.

## 직접 확정한 과장 선언

### 1. v1.0.25.2 안의 stale 최신 제목

`Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md:1`은 복제된 제목에서
v1.0.25.1을 “현행 최신”으로 부른다. 같은 파일 후반, 최종 handover,
현재 Git 기준선 및 사용자 재확인은 v1.0.25.2를 최신으로 둔다.

판정: `OVERCLAIMED / STALE_AUTHORITY_LABEL`

### 2. “확정 구성의 코드 반영 완결”

`Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md:230`의 제목은 최종 기본 경로가
legacy4이고 skew7은 opt-in isothermal 표현이라는 사실, 그리고 정칙용액
이론과 logistic 평형 구현의 단절을 포괄하지 못한다.

판정: `OVERCLAIMED / IMPLEMENTATION_COMPLETION_TOO_BROAD`

### 3. 이론 문건의 코드 이야기 배제 완료

`Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md:25`는 이관 완료를
선언하지만 실제 이론 계열의 본문·부록·각주에는 함수명, key, gate,
bit-exact 및 code map이 남아 있다.

판정: `OVERCLAIMED / THEORY_CODE_BOUNDARY_VIOLATED`

### 4. Ω 적합으로 흑연 두-상 marginal 확정

`KERNEL_COMPARISON_REPORT_v1025_2.html:228`은 패배한 regsol 적합에서
얻은 Ω/RT를 두-상 판정으로 이전한다. 네 값 중 하나는 임계값 아래이고,
불확도·전이 대응·다온도 transfer가 검증되지 않았다. winning skew basis나
독립 XRD 상 판정으로 이전할 수 없다.

판정: `OVERCLAIMED / LOSING_FIT_TRANSFERRED_TO_PHASE_CLAIM`

## `PARTIAL`의 대표 의미

- 나열된 v1.0.25.2 gate의 실행 기록은 있으나 legacy 복원이 당시 결함
  기본 경로를 검사하지 못했다.
- doc–code 30/30은 같은 식·상수의 복제를 보이지만 같은 물리 오류가
  양쪽에 복제됐을 가능성과 외부 데이터 타당성을 배제하지 못한다.
- build/PDF, machine JSON 또는 test 파일이 같은 commit에 있어도
  final source에 대한 재실행 여부와 검증 범위를 별도로 확인해야 한다.
- bit-exact와 무변경은 비교 대상, 정규화, 허용오차 및 호출 경로가
  고정돼야만 의미가 있다.

## 핵심 해석

과거 이력에는 실행 흔적이 매우 많지만, 3,080개 긍정 선언 중 현재
독립 근거로 곧바로 확정할 수 있는 위치는 최신 기준선 표기 3곳뿐이다.
이는 과거 작업이 전부 실패했다는 뜻이 아니라, 결과서와 gate가 주로
자기 정의한 범위의 기계 정합을 증명했고 사용자가 지금 요구하는
물리적 완결성·외부 타당성·이론–코드 단일 논리까지 독립 증명하지는
않았다는 뜻이다.

따라서 이후 감사에서는 “완결판”이라는 버전 이름을 출발 증거로 쓰지
않는다. 각 식의 유도, 제한 극한, 코드 소비 경로, 공개 데이터의
out-of-sample 설명력을 다시 검증한다.

## 기계 산출물과 재현성

- 판정기:
  `Codex/work/v1010_v1025_2_reaudit/adjudicate_phase057_completion_claims.py`
- 전건 판정:
  `Codex/results/PHASE_057_COMPLETION_CLAIM_ADJUDICATION.json`
- JSON 크기: 5,380,133 bytes
- 연속 두 번 생성한 SHA-256:
  `345889abcc34675607e2d59f17721fe4e316721183914a8cd7bf3cb247920c96`

검증 조건:

- 3,487/3,487 candidate ID 순서·연결 보존
- 3,080/3,080 긍정 주장에 네 상태 중 하나 부여
- 407/407 비긍정 후보에 null status와 제외 사유 부여
- status 합과 긍정 주장 수 일치
- exact-blob commit과 실제 patch scope 연결
- provisional finding ID 연결

## 다음 단계

Phase 057 Step 20.5에서 merge, copy-forward, revert, 후속 수정으로
같은 선언의 효력이 어떻게 달라졌는지를 기록한다. 특히 v1.0.25.1의
stale handover, v1.0.25.2의 7-gallery 기본값 도입과 legacy4 복구,
gate가 실제로 본 경로와 보지 못한 경로를 시간축에 배치한다.
