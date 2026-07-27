# Phase 057AC — v1.0.23 P2·P3 관찰

정본일: 2026-07-28
세부 Step: 19.7C
범위: 2 unique documents, 216 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `results/PHASE_P2_RESULT.md`
- `results/PHASE_P3_RESULT.md`

두 결과 문건을 첫 행부터 마지막 행까지 전량 읽었다. 이 batch는
부록 E의 수학적 저작과 그 식을 옮긴 선택적 코드 경로의 내부
정합을 판정한다. 공개 LIB 데이터 설명력과 물질별 물리 closure의
타당성은 이 두 문건의 게이트로 검증되지 않는다.

## Provisional Findings

### INTENT-PROV-0199 — 부록 E는 선택적 수학 연구노트이지 물질모델의 완결 closure가 아니다

P2는 비선형 Volterra lag 문제, 동결 0차 기준, 첫 Picard/ratio
보정, 국소 유효성 지표, voltage-domain 전달함수를 하나의
부록으로 정리했다. 앞선 P1에서 확인한 수식을 대체로 정확히
전사했고, 본문에는 포인터만 두어 기존 서사를 보존했다.

그러나 핵심 상태 의존성

`L_V(xi)=L_V^0 exp[g_eff(1-xi)]`

및

`g_eff=2 chi_d Omega/(RT)`

은 독립적인 전이상태 유도나 물질별 실험 식별로 닫힌 법칙이
아니다. 선택한 surrogate constitutive law 안에서 자기일관성을
개선하는 방법이다.

판정:

- Picard 1회와 동결극한의 수학은 `THEORY_ONLY`.
- 흑연·Si·LCO의 보편 closure 또는 검증된 상전이 장벽으로
  승격하지 않는다.
- 최종 문건에 남기려면 유도 범위, 식별 가능성, 실패 조건을
  물리 서사 안에서 다시 세워야 한다.

### INTENT-PROV-0200 — P3 코드는 가정된 근사를 충실히 옮겼지만 시험은 자기정합·합성 검산이다

P3는 `_causal_memory_ratio`, `_lag_ratio_geff`,
`lag_ratio_correction`, `transfer_apparent_from_equilibrium`을
추가했다. 보고된 G-E1–E5는 다음을 보인다.

- `g_eff=0`에서 동결 경로를 회수한다.
- 옵션 off에서 기존 출력이 bit-exact다.
- 같은 synthetic constitutive law의 fixed point에 대해 첫
  Picard iterate가 0차보다 가깝다.
- FFT 전달함수와 같은 동결 convolution이 수치적으로 일치한다.
- 수동 `L_V=0.006`, `L_V/w=0.3` 조건에서 옵션이 실제 작동한다.

이는 구현의 내부 수학 정합을 지지한다. 하지만 참값 자체를
동일한 가정으로 생성했으므로 실험 또는 독립 물리 검증은 아니다.
특히 `max|on-off|=0.94`는 작동성만 증명하며, 변화량의 물리적
합리성을 증명하지 않는다.

판정:

- “선택한 1차 closure의 구현 일치”는 `PRESERVE`.
- “실제 전극의 자기일관 lag가 검증됐다”는 `REJECT`.
- 이후에는 synthetic unit test, 수치 수렴 test, 공개 데이터
  예측 test를 서로 다른 gate로 둔다.

### INTENT-PROV-0201 — 기본 off 보존은 회귀 안전성이지 기존 물리의 교정이 아니다

P3는 `lag_ratio_correction=False`를 기본값으로 두고 기존
v1.0.19 계열 출력을 bit-exact로 보존했다. 이는 신규 선택지가
기존 결과를 몰래 바꾸지 않았다는 좋은 회귀 증거다.

반대로 기본 경로에는 앞선 재감사에서 발견한 C-rate 시간단위
3,600배 문제와 그에 연결된 `L_V/w`, 유효장벽 식별 문제가
그대로 남는다. “기본값에서 휴면이므로 안전하다”는 설명도 그
단위 문제가 교정되기 전에는 성립하지 않는다.

판정:

- 회귀 보존은 `PRESERVE`.
- 이를 v1.0.23 물리모델의 개선 또는 검증으로 읽는 것은
  `REJECT`.
- 시간단위 교정 후 기존·ratio 두 경로를 모두 재식별한다.

### INTENT-PROV-0202 — 전달함수는 전압축 평활 항등이며 기기·동역학 응답으로 자동 승격되지 않는다

`H(omega)=1/(1+i omega L_V)`는 전압축에서 지수 kernel
convolution을 Fourier/Laplace 표현으로 옮긴 것이다. G-E4도
동일한 frozen convolution과 FFT 표현의 일치를 검사한다.

이 `omega`를 시간 각주파수, EIS 응답, 계측기 전달함수 또는
동적 감수율로 읽으려면 전압 sweep와 시간의 사상, 전류·전위
동역학, 초기·경계조건이 추가로 필요하다. 또한 P3 결과만으로는
helper가 생산 `dqdv` 경로의 독립적인 물리 응답을 구성한다고
볼 수 없다.

판정:

- 전압축 convolution의 변환 표현은 `PRESERVE`.
- 실험 장비 또는 실제 시간응답 해석은 `UNVERIFIED`.
- 최종 문건에서는 frequency-response 언어를 쓰기 전에 독립
  유도를 제공하거나 전압영역 계산 도구로 한정한다.

### INTENT-PROV-0203 — 코드 대응표의 본문계 편입은 사용자의 최종 문건 경계와 충돌한다

P2 당시 규칙은 “본문 코드 언급 0, 부록 E.6 예외”였고 이
범위에서는 자체 PASS를 선언했다. 그러나 현재 사용자 방향은
이론 문건에는 물리·화학 논리만 두고, 코드는 그 문건을 100%
반영하는 별도 산출물로 관리하는 것이다.

판정:

- 부록 E.6의 함수명·플래그·코드 지도는 최종 이론 문건에서
  분리한다.
- 식–코드 추적표 자체는 버리지 않고 별도 implementation
  conformance companion의 기계검증 가능한 계약으로 옮긴다.
- 문건과 코드를 분리하되 양방향 equation ID–symbol–unit–
  function–test 매핑을 유지한다.

### INTENT-PROV-0204 — 상호작용항의 회계와 부호는 후속 코드 계보 감사 전 확정할 수 없다

P2/P3은

`kappa=kappa_0 exp[-2 chi_d (Omega/RT)(1-xi)]`

와 그 역수인 `L_V`의 지수형을 서로 맞췄다. 그러나 이
`Omega`가 평형 자유에너지, 전이상태 장벽, `dH_eff`, 또는
다른 상호작용 보정에 이미 들어가는 항과 중복되는지는 이
두 결과 문건이 전 계보를 따라 증명하지 않는다.

판정:

- 수식과 신규 함수 사이의 부호·역수 관계는
  `IMPLEMENTATION_CONSISTENT`.
- 열역학적 `Omega`와 kinetic barrier contribution의 분할은
  `UNVERIFIED`.
- Phase 067 코드 역사에서 자유에너지·화학퍼텐셜·장벽·lag
  각 경로의 `Omega` 회계를 항별로 추적한다.

### INTENT-PROV-0205 — 미확인 원문을 넣은 서지는 최종 권위가 될 수 없다

P2는 사용자 JCP 논문과 Ref.6·7을 참고문헌에 추가했으나,
동시에 Ref.6·7 제목·DOI와 원문 대조가 완료되지 않았다고
명시했다. 미확정 사실을 표시한 정직성은 보존하되, 그 상태로
수식의 문헌 권위를 완결했다고 볼 수 없다.

판정:

- 현재 서지 연결은 `PARTIALLY_VERIFIED`.
- 최종 문헌 조사에서 원 논문의 식, 변수 정의, 문제의 종,
  가정, 오차주장을 직접 대조한다.
- 원문 미확인 항목은 인용문헌 목록과 근거 행렬에서 별도
  상태로 유지한다.

## Endgame Consequence

부록 E 계열을 그대로 최종본으로 승격하지 않는다. 유용한 핵은
첫 Picard 근사와 전압축 convolution의 수학이다. 최종 작업에서는
다음 순서로 재판정한다.

1. C-rate와 모든 시간·전압축 단위를 먼저 교정한다.
2. `L_V(xi,T,I,U)`의 물리 유도와 식별 가능성을 다시 세운다.
3. 열역학 상호작용과 kinetic barrier의 중복 회계를 제거한다.
4. 공개 실험 데이터에 대한 out-of-sample 조건 예측으로
   closure의 필요성을 시험한다.
5. 코드 지도는 이론 문건이 아닌 별도 conformance companion에
   둔다.

## Coverage Status

- 이 batch의 2문건, 216행은 `READ`.
- 누적 coverage 반영 후 목표는 223문건, 48,340행이다.
- v1.0.23 잔여 목표는 7문건, 532행이다.

## Next

Step 19.7D:
P5 마감 결과와 독립 AUD 2문건 160행을 전문 검독한다.
