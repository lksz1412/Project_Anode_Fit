# Phase 057AQ — v1.0.25 cascade TODO·change ledger 관찰

정본일: 2026-07-28
세부 Step: 19.8K
범위: 2 unique documents, 339 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

- `Claude/docs/v1.0.25.1/results/V1025_DOC_CASCADE_TODO.md`
- `Claude/docs/v1.0.25.1/results/V1025_CHANGE_LEDGER.md`

두 문건을 첫 행부터 마지막 행까지 전량 검독했다. 계획 초안,
실제 집행, 사용자 결정, 집행자 재량, 검증 시점을 구분했다.

## Provisional Findings

### INTENT-PROV-0314 — v1.0.25의 집행 순서는 현재 사용자 원칙과 반대였다

cascade TODO는 “코드 측 이미 완결, 문건이 정합해야 할 코드
거동”을 기준으로 LaTeX를 후행 편집했다. 즉 구현이 먼저
결정되고 theory prose가 그 구현을 설명하는 code-first
cascade였다.

판정:

- 이 실행 순서는 `SUPERSEDE`.
- 새 정본은 문헌·가정·free energy·관측량·동역학을 먼저
  승인하고, 그 뒤 implementation specification과 코드를
  파생한다.
- 회귀 때문에 이론을 구부리지 않고, legacy 호환은 별도
  compatibility layer로 격리한다.

### INTENT-PROV-0315 — 이론 본문에 코드 이름과 gate를 삽입한 방식은 폐기한다

지시서는 Ch1/Ch2/Ch3 본문과 각주에 `func_dxi_eq`,
`_causal_pad`, `use_si_constants`, line number, bit-exact,
gate 이름을 넣도록 했다. 이는 현재 확정된 “문건은 물리·화학
논리만” 원칙과 충돌한다.

판정:

- 해당 code references는 최종 이론 문건에서 `REJECT`.
- 수식–구현–시험 mapping은 별도 conformance companion과
  machine-readable matrix에만 둔다.
- 이론 본문은 구현 상태가 아니라 물리적 채택 지위와 적용
  범위만 설명한다.

### INTENT-PROV-0316 — additive-only·boxed 식 보존 규칙이 과학적 정본성보다 우선하면 안 된다

당시 지시는 기존 식·label·boxed 삭제 금지와 additive-only를
강하게 요구했고, 코드에서 삭제된 Frumkin kernel도 analytic
record로 본문에 보존했다. 사실이 아니게 된 문장 하나만 예외로
삭제했다.

판정:

- history 보존에는 유용하지만 canonical textbook의 기준으로는
  `SUPERSEDE`.
- 검토 가치가 있는 비채택 이론은 명시적 “대안 모델과 기각
  근거” 절 또는 별도 review appendix로 이동한다.
- label 안정성보다 식의 진실성, 채택 지위, 독자 혼동 방지가
  우선이다.

### INTENT-PROV-0317 — skew `alpha`는 면적을 보존하지만 전이 중심의 의미를 바꾼다

`xi_eq=sigma^alpha`는 단조성과 총 면적을 보존한다. 그러나
`alpha != 1`이면 peak apex가 `U + sigma_d w ln(alpha)`로
이동하고, `V=U`에서 진행률도 `2^{-alpha}`다. 따라서 기존
`U`를 peak center, half-completion voltage, thermodynamic
transition voltage로 동시에 부를 수 없다.

판정:

- 정규화 kernel 수학은 `PRESERVE_FOR_REVIEW`.
- `U`, median potential, mode/apex, free-energy crossing의
  정의를 분리한다.
- 조성 비대칭 free energy에서 유도하지 못하면 `alpha`는
  empirical observation-shape parameter이며 canonical
  thermodynamic center를 바꾸지 못한다.

### INTENT-PROV-0318 — alpha의 물리적 동기는 유도보다 앞서 붙은 상태다

TODO는 order–disorder entropy step과 composition-dependent
`Omega(x)`를 skew의 동기로 제시하지만, `sigma^alpha`가 해당
free energy에서 유도된다는 증명은 없다.

판정:

- 이 설명은 `PLAUSIBILITY_ONLY`.
- microscopic mechanism을 암시하는 prose로 empirical kernel을
  물리화하지 않는다.
- 채택하려면 자유에너지 또는 확률분포에서 유도하고 다중
  rate·temperature 데이터로 kinetic asymmetry와 식별한다.

### INTENT-PROV-0319 — causal pad는 필요한 경계조건 수정이지만 고정 truncation·cap은 물리 상수가 아니다

`-infinity` 이력 적분을 근사하기 위해 `5 L_V` pad,
간격 `<=L_V/20`, 최대 4000점이 도입됐다. 이는 window-start
artifact를 크게 줄였지만 `5 L_V`는 유한 절단이며 tail
잔여가 `exp(-5)` 수준이고 4000점 cap은 해상도 의존 실패
가능성을 남긴다.

판정:

- causal history를 평가창 밖까지 확장하는 원리는 `PRESERVE`.
- 5, 20, 4000을 물리 상수처럼 고정하는 것은
  `REJECT_AS_UNDERIVED`.
- tolerance-controlled quadrature/convolution, adaptive domain,
  explicit convergence error와 failure를 사용한다.

### INTENT-PROV-0320 — legacy bit-exact가 SI 상수의 기본 적용을 막은 결정은 재설계가 필요하다

v1.0.25는 CODATA 계열 `R_SI`, `F_SI`를 추가했지만 기존
golden output을 한 bit도 바꾸지 않기 위해 비-SI legacy 값을
기본으로 유지했다.

판정:

- 회귀 차이를 공개한 점은 `PRESERVE`.
- 새 scientific canonical mode는 권위 있는 상수를 기본으로
  하고, legacy bit-exact는 명시적 compatibility mode로 둔다.
- 표시 반올림이 아니라 raw value, unit, constant set ID를
  검증한다.

### INTENT-PROV-0321 — FWHM 정정은 유용하지만 채택 모델 밖의 유도로 남아 있다

`lambda=1-Omega/(2RT)`에 대해 중심 높이 scale과 FWHM을
분리하고, FWHM closed form과 `lambda^(3/2)` 점근을 추가했다.
이는 선행 “한 식으로 연속화” 오류를 고친 중요한 수학 자산이다.
그러나 regular-solution dQ/dV는 생산 경로에서 삭제됐다.

판정:

- 식은 Phase 065·문헌 감사에서 독립 재유도한다.
- 맞다면 review/theory asset으로 보존하되, 채택 구현의 설명처럼
  쓰지 않는다.
- two-phase singularity의 유한 폭은 equilibrium, material
  heterogeneity, kinetics, instrument broadening으로 분리한다.

### INTENT-PROV-0322 — 문건·코드 감사 30/30은 물리 타당성 검증이 아니다

change ledger는 신규 수치와 거동의 구현 재현 30/30을 보고하지만,
그 검사는 문건 주장과 코드 출력의 일치다. 자유에너지의 타당성,
parameter identifiability, external predictive validity를
보증하지 않는다.

판정:

- conformance evidence는 `PRESERVE`.
- physics verification, numerical verification, software
  regression, data validation을 별도 gate family로 둔다.

### INTENT-PROV-0323 — 검증 뒤 동시 편집이 계속되어 당시 PASS snapshot이 최종 source를 보증하지 않는다

ledger는 02:06 이전 structure/strict/doc-code 검사를 실행한 뒤
02:17까지 여러 `_sections`가 계속 수정됐고, 줄 수가 +250에서
+257로 변했다고 기록한다. 작성 sub-session도 gate 결과를
재실행하지 않고 인용했다.

판정:

- 당시 PASS는 해당 시점 snapshot에만 유효하다.
- 최종 workflow는 source freeze commit 후 검증하고, 검증 뒤
  변경 시 gate를 자동 무효화한다.
- commit SHA, artifact hash, test environment가 없는 PASS
  문구를 acceptance authority로 쓰지 않는다.

### INTENT-PROV-0324 — 누락된 gate와 축소 편집 범위는 후속 모순 가능성을 남겼다

금지 표현 재도입을 검사할 `G-금지`가 구현되지 않았고,
causal-pad 설명과 background 정정은 지시된 여러 절 중 일부에만
집약됐다. 당시 ledger도 관련 절의 모순 재검을 권고한다.

판정:

- Phase 065에서 실제 LaTeX 전역 서술을 교차검사한다.
- 문자열 금지만이 아니라 claim registry와 semantic
  conformance test로 금지·supersession을 관리한다.

### INTENT-PROV-0325 — 파일명 유지 결정은 사용자 의도로 확정돼 있다

DG-2에서 사용자는 내부 파일명을 매 version마다 바꾸지 말고
문서의 version 표시만 갱신하라고 결정했다.

판정:

- 기존 계보 해석에서는 `PRESERVE`.
- 새 endgame artifact 명명은 별도 계획에서 결정하되, 불필요한
  rename churn과 cross-reference 파손을 피한다.

## Direction Recovered

이 batch가 보여주는 최종 방향은 다음처럼 정리된다.

1. 기존 작업의 정직한 계획–실집행 원장은 살린다.
2. code-first cascade는 theory-first derivation으로 뒤집는다.
3. 이론 문건과 conformance companion을 물리적으로 분리한다.
4. 회귀 호환성과 과학 정본을 같은 default로 타협하지 않는다.
5. validation은 반드시 freeze commit을 대상으로 재실행한다.
6. fitting kernel의 수학적 편의에 microscopic 이름을 먼저
   붙이지 않는다.

## Coverage Status

- 이 batch의 2문건, 339행은 `READ`.
- 누적 coverage 반영 후 목표는 261문건, 51,870행이다.
- 전체 Phase 057 잔여 목표는 10문건, 5,925행이다.

## Next

Step 19.8L:
T13/T14 report 1문건 487행을 연속 구간으로 나눠 전문 검독한다.
