# Phase 057B — v1.0.10–v1.0.13 사용자 의도 관찰

정본일: 2026-07-28
세부 Step: 19.1
범위: 7 unique documents, 445 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 고유 blob을 첫 행부터 끝 행까지 검독했다.

| 경로 | 범위 |
|---|---:|
| `Claude/docs/v1.0.10/FITTING_GUIDE.md` | 1–46 |
| `Claude/docs/v1.0.10/HANDOVER_v1.0.11.md` | 1–78 |
| `Claude/docs/v1.0.10/V1010_PROBLEM_REPORT.md` | 1–55 |
| `Claude/docs/v1.0.10/V1010_HANDOVER_INTEGRITY_REPORT.md` | 1–45 |
| `Claude/docs/v1.0.12/FITTING_GUIDE.md` | 1–98 |
| `Claude/docs/v1.0.13/FITTING_GUIDE.md` | 1–99 |
| `Claude/docs/v1.0.13/HANDOVER_v1.0.13.md` | 1–24 |

첫 일괄 출력은 중간 truncation이 발생했다.
누락된 `V1010_PROBLEM_REPORT`, `V1010_HANDOVER_INTEGRITY_REPORT`,
v1.0.12 `FITTING_GUIDE`는 각각 별도 호출로 1행부터 EOF까지 다시 읽었다.
truncated 출력만으로 coverage를 완료 처리하지 않았다.

## Provisional Findings

### INTENT-PROV-0001 — 물리·화학 논리의 전개 무결성

`V1010_HANDOVER_INTEGRITY_REPORT.md:3`은 프로젝트의 첫 축을
물리·화학 논리를 전개 과정까지 비약 없이 이론적으로 무결한 식으로 만드는 것으로
기록한다.

`HANDOVER_v1.0.13.md:8`에는 사용자의 GO가 더 직접적으로 남아 있다.
물리·화학 전개 중 문제를 발견하면 수정하며 진행하고,
우선순위를 물리 논리 결함 제거, 논리 비약 제거, 수식 중심 구성 순으로 둔다.

판정: `USER_REQUIREMENT` 후보, 현재 `PRESERVE` 잠정.

### INTENT-PROV-0002 — 교재 수준의 추종 가능성과 수식 중심 서술

`V1010_HANDOVER_INTEGRITY_REPORT.md:3`은 학부 지식만 가진 타전공
석·박사 독자가 따라올 수 있는 교과서성을 두 번째 축으로 기록한다.

`HANDOVER_v1.0.13.md:5-8`은 다음 사용자 지적을 기록한다.

- 흑연 논리를 마친 뒤 LCO를 배치해 중간 혼합을 피할 것.
- 산문이 과도하며 수식만 읽어도 대부분 이해될 정도로 수식 중심성을 회복할 것.
- 통계역학 논의를 출발부터 자세히 제공하되 양자역학은 불필요함.
- 약어와 전문용어를 독자가 알 수 있게 소개할 것.
- 수식 전개에 필요한 개념은 당시 코드에 없더라도 설명할 것.

판정: `USER_REQUIREMENT` 후보.
단, 당시의 “흑연 후 LCO”라는 장 배치는 후속 3장 재편에서 변경됐을 수 있으므로
구조 자체는 `UNVERIFIED`, 서술 원칙은 `PRESERVE` 잠정이다.

### INTENT-PROV-0003 — v1.0.10 R1 철회는 사용자 요구가 아닌 검토 판정

`V1010_PROBLEM_REPORT.md:13-18`은 처음에 Nernstian 폭으로 두-상
near-delta를 만들 수 없다는 구조 결함을 주장했다.
같은 문건의 정정 배너와
`V1010_HANDOVER_INTEGRITY_REPORT.md:17-20`,
`HANDOVER_v1.0.11.md:4,10-14,27-32,76-78`은 이 판단을 철회하고
실제 PSD/convolution 재도입을 금지했다.

이것은 당시 검토자들의 `REVIEW_FINDING`과 `MODEL_PROPOSAL` 충돌이다.
현재 확인 범위에는 사용자가 해당 물리 판단을 독립적으로 확정한 직접 근거가 없다.

판정:

- “R1은 오판이었다”를 현재 사용자 방향으로 자동 승계하지 않음.
- “PSD/convolution은 금지”도 현재 사용자 헌법으로 자동 승계하지 않음.
- Phase 058–059에서 원 이론·코드·사용자 피드백과 다시 대조할 `UNVERIFIED`.

### INTENT-PROV-0004 — 순차 식별과 과식별 회피

v1.0.10, v1.0.12, v1.0.13 `FITTING_GUIDE`는 공통적으로
저율 평형 peak → 충·방전 pair → rate-series → multi-temperature →
holdout의 순서로 parameter tier를 연다.

v1.0.12/13의 S0–S5는 다음을 추가한다.

- GITT relaxation으로 활성화/수송 지배를 먼저 판정.
- 저율 OCV/dQdV로 중심·폭·면적·background 식별.
- current interruption으로 lumped resistance 식별.
- rate tail로 전위 민감도 식별.
- multi-temperature로 활성화 엔탈피 식별.
- rate별 charge/discharge gap으로 hysteresis 성분 식별.

판정: 과식별 회피에 유효한 `MODEL_PROPOSAL`.
사용자 요구로 확정하지 않으며 후속 버전에서 유지·수정 여부를 확인한다.

### INTENT-PROV-0005 — 합성 회귀와 실제 데이터 검증은 다르다

세 `FITTING_GUIDE`는 FD parity, golden regression과 면적 보존을 검증하지만,
동시에 실제 미사용 온도·C-rate holdout을 최종 검증으로 둔다.
v1.0.10 guide `:40`, v1.0.12 guide `:92`, v1.0.13 guide `:92`는
수치 round-trip이 잡음 데이터의 통계적 식별성을 증명하지 않는다고 경고한다.

판정: `PRESERVE` 후보.
과거 synthetic gate의 PASS를 실제 물리 검증으로 승격하지 않아야 한다.

### INTENT-PROV-0006 — 문건과 코드의 상호 유기성

`HANDOVER_v1.0.13.md:6-8`은 사용자가
문건–코드–문건–코드의 상호 유기 루프를 요구했고,
코드 flow의 이론 배경과 문건 수식의 코드 반영 중 어느 한쪽만 작성하는 것을
금지했다고 기록한다.

당시에는 문건에 코드 연결 내용을 적극적으로 포함했다.
현재 사용자의 “이론 본문은 코드 언급 배제, 외부 지정 절에서만 연결” 요구는
이 상호충실성 목표를 유지하면서 표현 위치를 더 엄격히 분리한 후속 결정으로
보인다. 정확한 supersession 위치는 후속 기록에서 확인해야 한다.

판정: 상호충실성은 `PRESERVE`, 본문 내 코드 언급 방식은 `UNVERIFIED`.

### INTENT-PROV-0007 — 검수 횟수보다 실제 재검증이 우선

`V1010_PROBLEM_REPORT.md`와 `V1010_HANDOVER_INTEGRITY_REPORT.md`는
같은 대규모 다중 검수 체계가 R1에 대해 서로 반대 결론을 냈음을 기록한다.
코드 실행을 추가한 후 초기 CRIT 판정이 철회됐다.

판정: “10회 검수” 자체는 과학적 gate가 아니다.
원식 재유도, 코드 실행, 실제 출력과 원천 기록 대조를 분리해야 한다.
이는 `REVIEW_FINDING`이며 후속 전체 계보에서 재검증한다.

### INTENT-PROV-0008 — 전극 라벨과 물리 방향의 분리

v1.0.12 `FITTING_GUIDE.md:5-11`은 탈리튬화를 `+1`로 직접 입력하도록 설명했다.
v1.0.13 `FITTING_GUIDE.md:5-11`은 electrode-aware wrapper를 도입하여
LCO charge label을 내부 탈리튬화 `+1`로 환산하도록 정정했다.

판정: 물리 방향과 셀 라벨을 분리한다는 원칙은 `PRESERVE` 후보.
구체 API 및 부호 대응은 `IMPLEMENTED_STATE`이며 Phase 058/067에서 검증한다.

### INTENT-PROV-0009 — v1.0.13은 실제 데이터 폐쇄가 아니었다

`HANDOVER_v1.0.13.md:17-18`은 계획 범위의 미완료가 없다고 쓰면서도
실데이터 round-trip 소관으로 다음 네 항목을 의도적으로 이월했다.

- multi-temperature \(T^2\) freeze 해제
- LCO \(\Omega^{cat}\), \(dH_a\) 배정
- numerical lag threshold 상향과 golden rebaseline
- LCO x-mapping 순환 수치 확인

판정: v1.0.13의 “완주”는 문건·내부 gate의 계획 범위 완료이지,
실험 기반 물리 모델 완료를 뜻하지 않는다.

## Conflicts to Carry Forward

1. 두-상 near-delta와 관측 broadening을 한 현상학적 폭에 흡수할지,
   equilibrium kernel과 population/transport broadening으로 분리할지.
2. radius/PSD 역산의 ill-posedness와 forward PSD integration의 구분.
3. \(\Omega>2RT\)를 모든 transition fit의 하한으로 둘 수 있는지.
4. `w=nRT/F`의 물리적 역할과 fitted apparent width의 역할.
5. v1.0.12→v1.0.13 LCO direction correction이 저수준·wrapper 전 경로에
   실제 반영됐는지.
6. synthetic regression과 real-data validation의 경계가 이후 버전에서
   흐려졌는지.

## Coverage Status

- 이 batch의 7문건은 `READ`.
- 아직 Phase 057 최종 `VERIFIED`가 아니다.
- 후속 문건 및 실제 Git diff와 충돌 대조가 끝난 뒤에만
  claim을 현재 사용자 방향 헌법으로 승격한다.

## Next

Step 19.2:
v1.0.14–v1.0.18.2에서 처음 등장한 고유 intent 문건을 전문 검독한다.
