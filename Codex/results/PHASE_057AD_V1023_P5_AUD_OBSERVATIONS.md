# Phase 057AD — v1.0.23 P5·독립 AUD 관찰

정본일: 2026-07-28
세부 Step: 19.7D
범위: 2 unique documents, 160 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `results/PHASE_P5_RESULT.md`
- `results/comp_v23/AUD_REPORT_v23.md`

두 문건을 첫 행부터 마지막 행까지 전량 검독했다. 여기서
“독립 감사”는 v1.0.23 작업 당시의 내부 분담 감사라는 뜻이다.
본 재감사의 독립적인 외부 문헌·실험 검증과 동일시하지 않는다.

## Provisional Findings

### INTENT-PROV-0206 — P5는 전사·회귀 감사를 잘했지만 “물리 전부 정합”으로 범위를 과장했다

P5의 강한 증거는 다음에 한정된다.

- 문건 식과 코드 식의 부호·계수·분모 대조.
- v1.0.22 대비 additive parity.
- 기존 기본 경로의 bit-exact 회귀.
- 내부 예제와 합성 게이트의 재현.
- 문건 빌드·라벨·인용 구조의 무결성.

이는 implementation conformance와 문서 품질 감사로 가치가 있다.
그러나 공개 실험 데이터, 독립 물성, 단위 전파, 매개변수
식별성, 물질별 예측을 gate로 삼지 않았다. 그럼에도 결론은
“물리·수식·코드·게이트·서지 견고”로 확대됐다.

판정:

- 식–코드 전사 정합과 회귀 결과는 `PRESERVE`.
- “물리 전부 정합”, “양 버전 견고”라는 포괄 결론은
  `SUPERSEDE`.
- 최종 감사에서는 `DERIVATION`, `IMPLEMENTATION`,
  `NUMERICS`, `EXPERIMENT`, `LITERATURE` gate를 분리한다.

### INTENT-PROV-0207 — 알려진 3,600배 단위 결함을 놓친 “치명 0”은 acceptance 기준으로 무효다

v1.0.22–v1.0.23 기본 경로의 `L_q=|I|/(Q_cell k)`에는 C-rate의
`h^-1` 수치를 시간축 `s`와 혼용한 3,600배 문제가 후속
재감사에서 확인됐다. 이 오류는 `L_V`, 휴면 판정, 그리고
barrier fit에 직접 전파된다.

P5는 동일 코드·게이트의 bit-exact 보존을 PASS 근거로 썼기
때문에, 기존 동작이 정확히 보존될수록 이 물리 단위 오류도
정확히 보존된다. P5/AUD에는 이 결함을 잡는 차원·단위 gate가
없다.

판정:

- 당시 정의한 좁은 audit scope 안의 “치명 0”은 이력 사실로
  보존한다.
- v1.0.23 전체 acceptance 또는 최신 물리 기준의 “치명 0”은
  `REJECT`.
- 단위 수정 전의 휴면·barrier·C-rate 수치는 정량 권위로
  사용하지 않는다.

### INTENT-PROV-0208 — 같은 이론식에서 `g_eff`를 다시 얻은 것은 대수 검산이지 독립 물리 유도가 아니다

AUD는 §8의 `k_univ`와 `dH_eff`에서

`partial ln L_V / partial xi = -2 chi_d Omega/(RT)`

를 다시 얻고 “독립 재유도·양방향 정확”이라 했다. 이는
같은 이론 가정에서 부호와 계수를 다시 계산한 대수적 독립성은
가진다. 그러나 전이상태 자유에너지나 화학퍼텐셜에서
`2 chi_d Omega(1-xi)`를 새로 도출한 것이 아니며, 독립 실험이나
외부 이론으로 closure를 검증한 것도 아니다.

판정:

- 부호·계수 검산은 `PRESERVE`.
- “독립 물리 유도”라는 해석은 `SUPERSEDE`.
- 최종 문건은 열역학 상호작용항과 kinetic activation barrier의
  역할을 별도 원리에서 유도하고 중복 회계를 검사한다.

### INTENT-PROV-0209 — additive parity는 새 기능의 격리를 증명하지만 기준선의 진실성을 증명하지 않는다

AUD는 v1.0.23이 v1.0.22의 공유 파일·공유 코드에 대해
byte-identical이고, 부록 E와 선택적 함수·플래그만 더해졌다고
판정했다. 이 계보 사실은 중요하다. v1.0.23의 새 문제가 어디에
국한되는지 추적할 수 있기 때문이다.

그러나 v1.0.22 자체에 있던 단위, SiOₓ placeholder, Si/Si-C
finite-rate closure, 열·엔트로피 누락까지 옳아지는 것은 아니다.

판정:

- additive parity는 `LINEAGE_PRESERVE`.
- “v1.0.22가 통과했으므로 공유부 물리는 통과”라는 추론은
  `REJECT`.
- 최종 계보표에는 “새 결함 유입”과 “기존 결함 상속”을 별도
  열로 둔다.

### INTENT-PROV-0210 — 수치 증거 과장을 찾아 고친 절차는 보존할 좋은 감사 패턴이다

P5는 부록 E의 다음 두 문장을 실제 커밋 스크립트로 다시
실행해 고쳤다.

- `g=0`의 약 `10^-8` 주장을 정확한 `0.0` 항등 회수로 수정.
- FFT의 약 `10^-9` 주장을 실제 G-E4 `3.96e-6`으로 수정.

또 G-E4 허용오차를 `5e-3`에서 `1e-4`로 좁혔다. 이는
scratchpad 결과와 재현 가능한 커밋 증거를 구분하고, 과장된
수치를 실제 실행값으로 낮춘 올바른 행위다.

판정:

- 이 증거 교정 절차와 수정치는 `PRESERVE`.
- 최종 프로젝트 전체에 `claim → committed reproducer →
  observed tolerance` 형식의 provenance gate를 일반화한다.
- 다만 이 수치들은 여전히 같은 모델의 수치 구현 검산이지
  실험 물리 검증은 아니다.

### INTENT-PROV-0211 — 서지 존재 확인과 인용 내용 검증을 구분하지 않아야 한다

AUD는 일부 DOI·제목의 존재와 사용자 논문의 서지를 확인한 뒤
“서지 무날조”라고 했다. 동시에 Ref.6·7은 제목·DOI·원문
확정이 남았다고 기록했다. 논문이 실재하는 것과 그 논문이
현재 식·가정·오차주장을 지지하는 것은 별개다.

판정:

- 확인된 제목·DOI의 존재는 `BIBLIOGRAPHICALLY_VERIFIED`.
- 원문 식과 적용범위를 대조하지 않은 이론 귀속은
  `CONTENT_UNVERIFIED`.
- 최종 review-level 문헌 행렬은
  `existence / full-text / equation / scope / claim support`를
  각각 기록한다.

### INTENT-PROV-0212 — 당시 “병합 준비 완료”는 프로젝트 완결 판정이 아니라 작업흐름 상태다

P5의 merge readiness는 문건 빌드, 회귀, 신규 게이트, 당시
범위의 발견사항 정정이 끝났다는 의미다. 사용자 최종 목표인
대학원 교재·리뷰 수준의 이론, 공개 LCO/graphite/Si 데이터
설명, 문건–코드 완전 정합을 충족했다는 의미는 아니다.

판정:

- v1.0.23 작업흐름의 역사적 `MERGE_READY`는 보존한다.
- 과학적 최신 정본 또는 endgame 후보 지위는 부여하지 않는다.
- v1.0.23은 유용한 수학·감사 자산을 제공하는 비정본 계보로
  두고, 후속 버전과 함께 재합성한다.

## Endgame Consequence

v1.0.23에서 가져갈 것은 식–코드 매핑 방식, additive parity,
재현수치 교정 절차다. 버릴 것은 내부 정합만으로 물리 검증을
선언하는 acceptance 논리다.

최종 conformance에는 최소 다음 다섯 축이 독립적으로 필요하다.

1. 방정식 유도와 단위의 물리 gate.
2. 문건 식–코드의 기계적 mapping gate.
3. 수치 수렴·보존·극한의 numerical gate.
4. 원문 문헌 claim-support gate.
5. 공개 데이터의 calibration/validation 분리와 조건 외 예측 gate.

## Coverage Status

- 이 batch의 2문건, 160행은 `READ`.
- 누적 coverage 반영 후 목표는 225문건, 48,500행이다.
- v1.0.23 잔여 목표는 5문건, 372행이다.

## Next

Step 19.7E:
handover·index·merge readiness 3문건 138행을 전문 검독한다.
