# Phase 057N — v1.0.21 Q5/Q5b 구조 관찰

정본일: 2026-07-28
세부 Step: 19.5E
범위: 2 unique documents, 2,740 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 두 JSON을 각각 400행 이하의 연속 구간으로 나누어
첫 행부터 끝 행까지 검독했다.

- `snapshot_v1021_q5.json`, 1,369행.
- `snapshot_v1021_q5b.json`, 1,371행.

Q5-navigation→Q5와 Q5→Q5b 구조 diff도 다시 계산했다.

## Provisional Findings

### INTENT-PROV-0087 — Q5는 계산 예제와 로드맵 label 세 개만 추가했다

Q5-navigation→Q5 diff는 Ch1에 다음을 추가한다.

- `sec:sum-worked`
- `ssec:nav-roadmap`
- `tab:navroadmap`

equation block, bibliography, asset, Ch2, appendix 변화는 0이다.
당시 change log는 끝-대-끝 계산 예제 안에 무번호 display 식 3개를
의도적으로 equation-block 체계 밖에 두었다고 기록한다.

판정:

- 대학원 교재형 문건에 완결 계산 예제를 두는 방향은 `PRESERVE`.
- 그러나 결과를 만드는 무번호 식이 구조 snapshot과 equation register의
  감시 밖에 있는 설계는 `CORRECT`.
- 최종 문건에서는 계산에 사용되는 모든 load-bearing 식에
  안정 label, 단위, 입력값 출처, 반올림 규칙을 부여한다.

### INTENT-PROV-0088 — Q5b의 기계상 변화는 측정 원리 서지 두 건뿐이다

Q5→Q5b diff는 Ch1 bibliography에만 다음을 추가한다.

- `weppner_huggins1977`
- `baek_pilon2022`

label, equation block, asset, Ch2, appendix 변화는 0이다.
통제 문건상 산문 bgbox는 GITT, entropic potential,
reversible heat/calorimetry의 원리 대응을 추가했다.

판정:

- 준평형 OCV, 전위의 온도계수, 가역열을 서로 교차 검증하는
  실험 방향은 사용자의 연구 목적과 직접 맞아 `PRESERVE`.
- 기법 상세와 모델식이 동일하다고 혼동하지 않는 scope guard도 보존한다.
- 최종 문헌 조사에서는 리뷰 한 편에 의존하지 않고
  GITT 원전·재료별 1차 실험·열량계 자료를 함께 확인한다.

### INTENT-PROV-0089 — Q5 구조 PASS는 계산 예제의 수치 정확성을 보장하지 않는다

Q5 snapshot에는 `sec:sum-worked`의 존재만 보이고,
예제의 무번호 식과 숫자는 equation hash로 캡처되지 않는다.
당시 기록은 네 좌표가 Python과 손계산에 일치한다고 적었지만
snapshot 자체는 그 값을 보존하지 않는다.

판정:

- 예제 검증은 실제 TeX 값, 독립 계산, 코드 실행을 삼자 대조해야 한다.
- 표시 반올림값을 재입력하지 않는 규칙은 보존하되,
  숨은 정밀도와 단위 변환을 machine-readable fixture로 남겨야 한다.
- “구조 diff 1:1”만으로 예제 재현성을 선언하지 않는다.

### INTENT-PROV-0090 — 측정 원리 배경은 검증 설계의 출발점이지 데이터 검증이 아니다

Q5b에서 새 asset은 0이고 equation도 0이다.
따라서 측정 원리를 설명했다는 사실과 실제 데이터를 사용했다는 사실은
분명히 다르다.

최종 검증 설계에 요구할 연결:

1. relaxation/GITT로 얻은 준평형 전위.
2. 저율 및 정전류 ICA의 peak 위치·높이·폭.
3. 온도별 entropic coefficient.
4. calorimetric reversible/irreversible heat.
5. 필요 시 reference electrode/half-cell로 분리한 전극 기여.

판정:

- 이 다중 관측량 교차 제약을 최종 모델 식별성 gate로 발전시킨다.

## Coverage Status

- 이 batch의 2문건, 2,740행은 `READ`.
- 누적 coverage 반영은 batch JSON 적용 후 114문건, 28,062행이다.
- v1.0.21 잔여는 Q6/Q7 2 snapshot, 2,765행이다.

## Next

Step 19.5F:
Q6/Q7 snapshot 2문건, 2,765행을 전문 검독해
LCO 시연과 Si bridgehead의 최종 v1.0.21 구조를 확인한다.
