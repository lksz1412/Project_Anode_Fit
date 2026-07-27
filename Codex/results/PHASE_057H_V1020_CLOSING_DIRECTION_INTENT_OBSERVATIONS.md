# Phase 057H — v1.0.20 종결·피팅·Si/LCO 방향 사용자 의도 관찰

정본일: 2026-07-28
세부 Step: 19.4D
범위: 19 unique documents, 2,348 physical lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 묶음을 첫 행부터 끝 행까지 검독했다.

- 그림 경쟁 framing 6본과 좌표 원장 3본.
- P7 최종 Fable 검수, 그림 체리픽 판정, P8 마감 계획.
- v1.0.20 피팅 가이드와 Si/LCO 방향 보고.
- v1.0.21 후보인 대정준 전하 보존 유도 note 2본과
  Eyring TST 유도 note 2본.
- v1.0.20 최종 handover.

`coords.json`은 물리적으로 한 행이지만 29,088 byte인 JSON이므로
원시 한 행을 앞뒤만 보지 않았다. `jq`로 1,774개 표시 행으로 전개해
1–450, 451–900, 901–1350, 1351–1774의 네 연속 구간을 모두 읽었다.
`FRAMING_FO2.md`와 `DIRECTION_SI_LCO_REPORT.md`의 최초 일괄 출력에서
잘린 구간은 각각 41–104행과 32–50행을 별도로 다시 읽었다.

## Provisional Findings

### INTENT-PROV-0049 — 수식으로 만든 그림은 모델 거동 검산이지 외부 실험 검증이 아니다

그림 경쟁 여섯 창은 기존 그림 21본을 대조하고, 본문 식 또는
v1.0.20 코드로 좌표를 생성해 다음 공백을 메우려 했다.

- \(U_j(T)\) 중심 이동.
- \(L_V\)에 따른 peak 저하·꼬리·이웃 peak 겹침.
- \(\partial U_{\mathrm{oc}}/\partial T\)와 가역열 부호 교대.
- Einstein 진동 엔트로피와 electronic 항의 함수형 구분.
- 전체 합성 \(dQ/dV\), 히스테리시스 gap, TST/CNT 관련 도식.

좌표가 본문 표와 일치하고 LaTeX가 빌드되는지는 잘 검증됐다.
그러나 좌표의 근원은 대부분 같은 수식과 같은 초기 파라미터다.
따라서 이는 식-그림 내부 정합, 극한, 부호, 렌더 품질의 증거이지
흑연·LCO·Si 실험 데이터에 대한 외부 예측 검증이 아니다.

판정:

- 식-그림 수치 검산은 `PRESERVE`.
- 그림을 재료의 실제 크기·형상 증거로 쓰는 것은 `REJECT`.
- 최종 문건의 계산 그림은 “식의 예시 평가”, “문헌 데이터 대조”,
  “실측 적합 결과”를 캡션과 provenance에서 명확히 분리한다.

### INTENT-PROV-0050 — 단계별 역식별 사슬은 사용자 목표에 맞지만 수치 문턱은 권위가 아니다

`FITTING_GUIDE.md`는 저율 골격, 전류 차단 분극, rate-series 꼬리,
다온도 Arrhenius, 충·방전 gap, holdout의 S0–S5 사슬을 제안한다.
앞 단계의 결과를 다음 단계에서 동결하고, 동시에 열면 공선형이 되는
파라미터를 구분한 점은 사용자의 실험 직관과 잘 맞는다.

특히 다음 구분은 보존 가치가 크다.

- 평형 중심/면적/폭과 \(IR\) 분극을 먼저 분리.
- \(dV/dq|_{q_a}\)와 장벽을 동시에 자유화하지 않음.
- 정지·interruption·rate·temperature 데이터를 서로 다른
  식별 질문에 배정.
- 미사용 온도와 C-rate에서 holdout 검증.

반면 잔차 \(10^{-4}\), 용량 ±5%, \(A_{\mathrm{cap}}=4RT\),
“가시 꼬리 약 80 kJ/mol”, 각종 초기 범위는 특정 구현과
시연 파라미터에서 나온 운영값이다. 실험 오차모형·장비 분해능·
재료별 데이터로 재확정하지 않으면 물리 법칙이 아니다.

판정:

- 비순환 staged identification은 `PRESERVE`.
- 고정 수치 gate와 cap은 `EMPIRICAL_ONLY` 또는 `UNVERIFIED`.
- 최종 코드는 arbitrary clip/cap/soft threshold로 물리를 만들지 않고,
  필요 시 수치 안정화와 물리 경계를 별도 층으로 공개한다.

### INTENT-PROV-0051 — 이론 본문은 자립하고 코드 정보는 허용 구역에만 둔다는 결정이 확인된다

P8 계획과 handover는 v1.0.20을 과거 버전을 몰라도 읽히는
자립 교재로 만들고, 본문 코드 언급을 금지한다고 다시 명시한다.
코드명·함수·회귀값은 `FITTING_GUIDE`, code-map 성격의 부록,
구현 보고와 handover에만 남겼다.

이는 사용자의 최신 제약과 일치한다.

1. 이론 문건의 본문은 물리·화학 논리만으로 완결한다.
2. 코드는 문건을 근거로 1:1 구현하되 본문이 코드를 설명하지 않는다.
3. 구현 계약·시험·버전 이력은 별도 companion 문건에서 추적한다.

판정: `USER_REQUIREMENT`, `PRESERVE`.
후속 통합에서 기존 code-map 부록의 위치와 노출 범위는
이 최신 원칙으로 다시 판정한다.

### INTENT-PROV-0052 — Si는 흑연식을 그대로 늘리는 문제가 아니라 chemo-mechanics가 필요한 별도 계보다

`DIRECTION_SI_LCO_REPORT.md`는 흑연 N0–N9 사슬을 Si에 대조해
전하 보존 합산(N9), 방향·전류 조건(N0), 유효 logistic 합과
유한율속 기억 구조 일부는 살아남는다고 보았다.
반면 상온 비정질 Si의 경사 전위, 약 300% 부피 변화,
응력-전위 결합, 소성 소산, 입자 크기 의존 때문에
N1/N2/N4/N6/N7은 재해석되고 N3 히스테리시스에는
새 기계 물리가 필요하다고 판정했다.

이 구분은 중요하다.

- logistic 합은 Si의 미시 격자 자리 증명이 아니라 유효 표현일 수 있다.
- 수백 mV Si 히스테리시스를 흑연 정규용액 gap만으로 설명하면 안 된다.
- 흑연에서 작아 배제한 particle-size channel이 Si에서는 지배적일 수 있다.
- graphite+Si 혼합전극은 단순 peak 합만이 아니라
  두 active material의 전하 분배·응력·경로 의존을 함께 닫아야 한다.

초기 보고는 “예비 부록 후 독립 Chapter 3”을 권고했고,
최종 handover의 사용자 결정 D21-3은 **Si 독립 Chapter 3**으로
후행 확정했다. 따라서 후행 결정이 선행 권고를 supersede한다.

판정:

- N9 전하 보존의 전극-중립 골격은 `PRESERVE` 후보.
- 고정자리 lattice-gas 미시 해석의 Si 직접 이식은 `REJECT`.
- chemo-mechanical 자유에너지와 소산 법칙이 닫히기 전
  Si 이론 완결 선언은 `UNVERIFIED`.

### INTENT-PROV-0053 — LCO는 골격이 있다고 해도 도핑 고전압·다온도 데이터로 닫히지 않았다

Si/LCO 보고와 피팅 가이드는 v1.0.20의 LCO 경로에
다음 한계를 직접 기록한다.

- `LCO_MSMR_LIT`의 전이량과 전자항은 tier-C 시연값.
- LCO의 \(\Omega_j^{\mathrm{cat}}\), 활성화 장벽 등은
  신뢰할 문헌 anchor가 없어 미배정.
- electronic entropy의 온도 의존은 \(T_{\mathrm{ref}}\) 동결 근사이고,
  문건이 말하는 \(T^2\) 중심 곡률의 다온도 구현은 미완료.
- LCO 3-peak 그림도 \(Q_j^{\mathrm{cat}}\), \(\Omega_j^{\mathrm{cat}}\)
  발명 위험 때문에 모든 창이 보류했다.
- 도핑으로 고전압 안정화된 LCO의 실제 OCV/dQdV/entropy/rate 자료를
  fit한 기록은 없다.

판정:

- 전극-중립 열역학/전하 보존 골격은 `PRESERVE` 후보.
- v1.0.20 LCO 수치는 `THEORY_ONLY` 또는 tier-C illustration.
- 최종 LCO 코드는 공개된 도핑 고전압 데이터와 조성·온도·율속 조건을
  대조하기 전 기본 상수나 권위값을 갖지 않는다.

### INTENT-PROV-0054 — 대정준 전하 보존 초안은 유용하지만 독립 자리 클래스 가정이 숨은 물리를 바꾼다

Q2 note 두 본은
\[
\Xi=\prod_j\Xi_{1,j}^{M_j},\qquad
\langle N\rangle=\sum_jM_j\theta_j
\]
에서
\(\sum_jQ_j\xi_j=Q\bar{x}\)를 유도하고,
\(\partial\langle N\rangle/\partial\mu=\beta\operatorname{var}N>0\)로
OCV 음함수의 유일근을 설명하려 했다.

전하 보존 자체와 안정 평형의 양의 감수율은 중요한 연결이다.
그러나 초안의 상세 식별에는 다음 가정이 들어간다.

- 서로 다른 staging 전이를 독립 자리 클래스처럼 인수분해.
- \(Q_j/Q=M_j/M_{\mathrm{tot}}\)로 동일 자리 전하를 대응.
- 상관이 없는 Bernoulli 합으로
  \(\operatorname{var}N=\sum_jM_j\theta_j(1-\theta_j)\) 사용.
- 평균장 \(\Omega_j\), 순차 staging, 상공존의 상관을 별도 취급하지 않음.

따라서 전하 보존식의 보편성과 이 특정 독립-class 미시 유도는
동일한 권위를 갖지 않는다. 상분리/상관이 있는 계에서 fluctuation
formula는 전체 공분산을 포함해야 하며, 안정 평형 가지와
비안정 평균장 loop도 분리해야 한다.

판정:

- 전하 보존과 안정 평형 단조성 연결은 `PRESERVE` 후보.
- 독립-class product를 graphite staging의 정통 미시 기원으로
  확정하는 것은 `UNVERIFIED`.
- v1.0.21 초안이라는 지위를 유지하고 후대 채택 여부를 다시 추적한다.

### INTENT-PROV-0055 — TST 초안은 표준 배경을 보강하지만 활성화 엔트로피의 온도 의존을 축약하면 안 된다

Q3 note 두 본은 반응좌표의 1차원 통과 flux에서
\(k_BT/h\)를 유도하고,
\[
k=\frac{k_BT}{h}\frac{q^\ddagger}{q_R}
  e^{-\Delta E_0/RT}
 =\frac{k_BT}{h}e^{\Delta S_a/R}e^{-\Delta H_a/RT}
\]
로 연결한다. \(\Delta S_a\)와 평형 반응 엔트로피
\(\Delta S_{\mathrm{rxn}}\)을 분리하고, 터널링·재교차·변분 TST가
범위 밖임을 밝힌 것은 적절하다.

다만 일반식은
\[
\Delta S_a
=R\frac{\partial}{\partial T}
 \left[T\ln(q^\ddagger/q_R)\right]
\]
이며, 단순한 \(R\ln(q^\ddagger/q_R)\)는 분배함수 비의 잔여
온도 의존을 무시하거나 별도 엔탈피 항에 일관되게 배분한 경우의
제한된 읽기다. 두 note 중 q3f1은 이 조건을 더 정확히 기록했고,
q3o2의 축약은 그대로 정본화하면 안 된다.

판정:

- \(k_BT/h\), 상태합 비, 활성화 엔트로피의 미시 연결은
  `THEORY_ONLY` 후보.
- 활성화 엔트로피를 온도 독립 prefactor 상수로 고정하는 것은
  데이터와 모드 분배함수 검증 전 `UNVERIFIED`.
- 이 문건들은 경쟁 초안이며 v1.0.20 정본에 채택된 내용이 아니다.

### INTENT-PROV-0056 — v1.0.20의 실제 계보 지위는 “품질 정정판”이다

최종 handover는 v1.0.20을 v1.0.19 대비 품질 정정·보강판으로
정의하고, 생산 코드의 물리·수치가 v1.0.19와 동일하며
헤더만 갱신됐다고 기록한다. 확장 항목은 모두 v1.0.21로 분리했고,
실측 데이터 부재 때문에 실제 피팅은 회사에서 수행하기로 했다고
명시한다.

따라서 v1.0.20에서 다음 표현은 허용되지 않는다.

- 새로운 graphite/LCO 물리 구현판.
- 공개 실험 데이터로 검증된 완성 모델.
- Si 또는 도핑 고전압 LCO까지 닫힌 통합 이론.

판정: 계보상 `PRESERVE`.
후대 문건이 v1.0.20의 내부 gate를 경험적 권위로 소급 사용하는지
v1.0.21 이후에서 감사한다.

### INTENT-PROV-0057 — 그림 선정의 가장 좋은 결정은 값이 없는 LCO 곡선을 만들지 않은 것이다

`FIGS_PICK_JUDGMENT.md`는 기존 고품질 그림을 대부분 보존하고,
공백을 채우며, 물리 범위를 벗어난 `fig:relaxode`만 교체하자는
보수 원칙을 채택했다. 특히 LCO 3-peak 후보는
\(Q_j^{\mathrm{cat}}\), \(\Omega_j^{\mathrm{cat}}\)가 없어서
모든 창이 독립적으로 보류했다.

이 결정은 사용자의 방향에 부합한다.

- 설명의 친절함을 위해 그림은 늘릴 수 있다.
- 그러나 “그럴듯한 완성 그림”을 위해 미확정 상수나 상 배정을
  발명하지 않는다.
- 모델 시연과 실험 관측을 명시적으로 구분한다.

판정: 증거가 없는 수치 그림 보류 원칙을 `PRESERVE`.

### INTENT-PROV-0058 — “H=0”과 빌드 green은 범위가 제한된 마감 판정이다

`REVIEW_FINAL_FABLE.md`는 20개 수정 지점과 주변 회귀를 검사해
고·중 위험 결함 0, 저위험 3건을 보고했다. 동시에
폭 keybox의 “셋을 한꺼번에 흡수”라는 문구가
\(L_V\)와 유효 폭의 역할을 다시 섞는 최약점이라고 남겼다.

최종 handover의 H=0, err=0, 구조 PASS는 이 정해진 검수 범위 안의
결과다. 실제 데이터 판별력, 미채택 Q2/Q3 초안, Si 기계 물리,
도핑 LCO 실증까지 통과했다는 뜻은 아니다.

판정:

- 수정 회귀·빌드 결과는 `PRESERVE`.
- 범위를 제거한 “물리 오류 0” 일반화는 `REJECT`.
- 최종 감사에서는 각 PASS가 무엇을 증명하고 무엇을 증명하지 않는지
  acceptance matrix에 함께 적는다.

### INTENT-PROV-0059 — 과거 “웹 검증 완료” 표기는 새 문헌조사를 대체하지 않는다

Si/LCO 보고는 17개 Si 문헌의 DOI를 웹 검색으로 확인했다고 기록했다.
그러나 같은 문건이 저자·쪽수 미확인 필드와
Larché–Cahn, 소성 소산, Si 부분몰 엔트로피의 미확보를 남겼고,
보고서의 링크·검색 확인만으로 각 load-bearing 정량 주장의
원문 조건, 시료, 온도, 전극 형상, 측정법까지 재현되지는 않는다.

판정:

- 과거 보고서는 후보 문헌 지도와 provenance로 `PRESERVE`.
- 최종 review급 문헌조사에서는 원문/보충자료/데이터를 다시 열고,
  claim–source–condition을 새 원장에 기록한다.
- 과거의 “검증 완료” 문구를 그대로 권위로 승계하지 않는다.

## Conflicts to Carry Forward

1. staged fitting의 좋은 식별 논리와 임의 수치 cap/gate를 분리해야 한다.
2. 독립 자리 클래스 대정준 유도와 순차 staging/상관/상분리의
   실제 통계역학을 재판정해야 한다.
3. TST에서 \(\Delta S_a\)의 일반 온도 의존과 상수 prefactor 근사를
   명시적으로 분리해야 한다.
4. LCO electronic 항의 \(T_{\mathrm{ref}}\) 동결 구현과
   문건의 \(T^2\) 예측 사이의 불일치를 후대 버전에서 추적해야 한다.
5. Si의 전하 보존 골격 재사용과 기계 히스테리시스 새 물리를
   서로 다른 모듈·검증 gate로 구성해야 한다.
6. 최종 독립 Chapter 3 결정이 언제 실제 이론·코드로 구현됐는지
   v1.0.21 이후에서 확인해야 한다.
7. 내부 수식 그림, synthetic round-trip, 공개 실험 fit을
   서로 다른 증거 등급으로 유지해야 한다.

## Coverage Status

- 이 batch의 19문건은 `READ`.
- 누적 Phase 057 coverage: 94문건, 8,073행.
- v1.0.20 잔여: 9문건, 10,426행.
- 아직 Phase 057 최종 `VERIFIED`가 아니다.

## Next

Step 19.4E:
v1.0.20의 baseline/P0/P2/P3/P4/P5/P7/P7b/final snapshot
9문건 10,426행을 전문 검독하고, 구조 변화가 증명하는 것과
과학적으로 증명하지 못하는 것을 분리한다.
