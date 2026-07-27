# Phase 057L — v1.0.21 Q2/Q3 구조 관찰

정본일: 2026-07-28
세부 Step: 19.5C
범위: 2 unique documents, 2,680 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 두 JSON을 각각 400행 이하의 연속 구간으로 나누어
첫 행부터 끝 행까지 검독했다.

- `snapshot_v1021_q2.json`, 1,324행.
- `snapshot_v1021_q3.json`, 1,356행.

동봉된 구조 diff 도구로 Q0→Q2와 Q2→Q3도 다시 계산했다.

## Provisional Findings

### INTENT-PROV-0078 — Q2의 기계상 변경은 다클래스 식 네 개다

Q0→Q2 diff는 Ch1에만 다음을 추가한다.

- section label `sec:sm-mc`.
- `eq:sm-mc-factor`
- `eq:sm-mc-occ`
- boxed `eq:sm-mc-balance`
- `eq:sm-mc-fluc`

기존 equation hash 변경·삭제는 0이고,
Ch2와 phase-separation appendix의 label/eqblock/bib/asset 변화도 0이다.

판정:

- 다클래스 자리의 factorization, occupation, charge balance,
  fluctuation response를 한 묶음으로 추가했다는 변경 대장과 일치한다.
- Ch2 연결은 구조상 새 식이 아니라 산문 연결이었다는 기록과도 일치한다.
- 이후 물리 감사에서는 이 네 식의 클래스 독립성,
  공통 reservoir potential, 정규화와 용량 가중,
  유일근 조건을 실제 본문에서 검산해야 한다.

### INTENT-PROV-0079 — Q2는 물질상 식별 모델이 아니라 통계역학 반전 골격이다

snapshot이 보여 주는 새 label은 모두 `sm-mc` 통계역학 블록에 있고,
graphite/LCO/Si 전용 상 label이나 실험 데이터 자산은 추가되지 않았다.
asset count는 Ch1 336, Ch2 21로 그대로다.

판정:

- 전하 보존 하에서 여러 site class의 공통 전위를 푸는 골격은
  피팅의 상태 제약으로 검토할 가치가 있다.
- 그러나 각 class를 흑연 stage, LCO 상, Si 상으로 곧바로 읽는 것은
  이 구조 증거가 지지하지 않는다.
- 물질별 해석은 별도 자유에너지·상변태·구조·분광/전기화학 증거가
  있어야 한다.

### INTENT-PROV-0080 — Q3의 기계상 변경은 TST 배경 식 다섯 개다

Q2→Q3 diff는 Ch1 `ch1_sec05_width.tex`에만 다음을 추가한다.

- `eq:tst-qrc`
- `eq:tst-freq`
- `eq:tst-rate`
- `eq:tst-dG`
- boxed `eq:tst-box`

Ch1 서지는 `glasstone1941`, `laidlerking1983` 두 건 증가했다.
기존 식 hash 변경·삭제, Ch2/appendix 변화, asset 증가는 없다.

판정:

- TST prefactor와 활성화 자유에너지의 이론 배경을 보강했다는
  계보는 `PRESERVE`.
- 이 추가만으로 전류·전극전위·온도에 따른 장벽 이동이나
  dQ/dV peak lowering/broadening의 동역학이 완성됐다고 볼 수 없다.

### INTENT-PROV-0081 — TST 배경과 실제 LIB 비평형 장벽 모델을 분리해야 한다

당시 통제 문건은 준평형과 재교차 무시를 TST 전제로 적고,
`ΔS_a = R ln(q‡/q_R)`를 Part 0의 엔트로피 연산과 연결했다.
구조 snapshot은 해당 식의 존재만 확인한다.

후속 검산 항목:

1. `ΔG_a(T,\phi,x,\text{state})`의 독립변수와 표준상태.
2. transmission coefficient와 recrossing의 처리.
3. activation entropy의 일반적 온도 의존성.
4. 전류가 장벽 자체를 바꾸는 경우와 overpotential이 구동력을
   바꾸는 경우의 구분.
5. 단일 TST rate를 분포·핵생성·성장·상경계 이동과 연결하는 과정.

판정:

- TST 교과 배경은 보존 후보.
- 이를 곧바로 peak 폭의 실험 법칙으로 사용하는 것은 `UNVERIFIED`.

### INTENT-PROV-0082 — Q2/Q3에는 새 실험 검증 자산이 없다

Q0, Q2, Q3의 asset count는 모두
Ch1 336, Ch2 21, appendix 0으로 동일하다.

판정:

- Q2/Q3는 이론·설명 확장이다.
- 공개 실험 데이터와의 독립 적합 또는 예측 검증을 수행한 phase로
  해석하는 것은 `REJECT`.
- 해당 검증은 최종 문헌·데이터 phase에서 새로 설계한다.

## Evidence Limits

1. snapshot은 식 문자열 hash를 주며 실제 유도 산문을 주지 않는다.
2. 새 식의 단위·부호·경계조건은 아직 검산하지 않았다.
3. 기존 식 hash 불변은 기존 식의 정확성을 뜻하지 않는다.
4. 코드 함수 변경이 불필요했다는 Q8 판정은 이 snapshot이 증명하지 않는다.

## Coverage Status

- 이 batch의 2문건, 2,680행은 `READ`.
- 누적 coverage 반영은 batch JSON 적용 후 110문건, 22,595행이다.
- v1.0.21 잔여는 6 snapshot, 8,232행이다.

## Next

Step 19.5D:
Q4/Q5-navigation snapshot 2문건, 2,727행을 전문 검독해
그림 5건과 임시 항법 인프라의 실제 구조 변화를 확인한다.
