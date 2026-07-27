# Phase 057W — v1.0.22 FR A09–A16 심층검토 관찰

정본일: 2026-07-28
세부 Step: 19.6H
범위: 8 unique documents, 2,644 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 FR A09–A16 심층 검토 보고서를 첫 행부터 끝 행까지 검독했다.
400행을 넘는 보고서는 연속 구간으로 나누어 읽었고, 병렬 출력이
잘린 A12·A13은 더 작은 구간으로 다시 전량 확인했다.

- `results/comp_FR/A09_REVIEW.md`
- `results/comp_FR/A10_REVIEW.md`
- `results/comp_FR/A11_REVIEW.md`
- `results/comp_FR/A12_REVIEW.md`
- `results/comp_FR/A13_REVIEW.md`
- `results/comp_FR/A14_REVIEW.md`
- `results/comp_FR/A15_REVIEW.md`
- `results/comp_FR/A16_REVIEW.md`

## Provisional Findings

### INTENT-PROV-0156 — 유한전류 tail의 적분 수학과 물리 closure를 분리해야 한다

A09가 검산한 지수 memory convolution, 충·방전 방향 반전, 부분적분
항등식과 영전류 극한은 내부 수학으로는 상당히 견고하다. 그러나
해석적 닫힌형을 얻기 위해 다음을 동시에 고정했다.

- logistic 응답의 5% 지점에 해당하는 `z_cut=4.357`.
- 실현 구동력의 상한 `A_cap=4RT`.
- cut 이후의 `A_j`, `L_q`, Jacobian을 국소 상수로 동결.
- q축 cut이라고 설명하면서 실제 계산은 전위축에서 수행.
- microscopic Eyring prefactor를 cell-scale relaxation에 직접 사용.

이 값과 동결은 상전이 장벽에서 유도된 보편 상수가 아니라 선택된
수치·관측 closure다. 특히 `A_cap=4RT`를 “안전한 물리 상한”으로
승격하면 사용자가 금지한 임의 cap을 이론으로 위장하게 된다.

판정:

- causal memory integral과 방향 반전은 `PRESERVE`.
- 5% cut, `4RT` cap, frozen-`L_q`는 `EMPIRICAL_ONLY`.
- 최종 이론 문건의 보편 법칙 또는 생산 코드의 무조건 기본값으로
  두는 것은 `REJECT`.
- full local kinetics와 frozen analytic observation kernel을 서로
  다른 근사 단계로 명명하고 각각 별도 검증한다.

### INTENT-PROV-0157 — C-rate의 시간 단위 오류는 장벽 파라미터로 흡수되는 구조적 결함이다

A10은 당시 계산이 C/10을 `|I|/Q_cell=0.1`로 넣어 C-rate의 숫자를
사실상 `s^-1`처럼 사용했음을 드러냈다. 물리적 C/10은
`0.1 h^-1 = 2.78e-5 s^-1`이므로 lag length는 약 3,600배 달라진다.

이 차이는 단순 표시 오차가 아니다. Eyring 지수와 곱해진 모델에서는
동일한 곡선을 맞추며

`RT ln(3600) ≈ 20.3 kJ mol^-1` at 298 K

가 activation free energy 또는 activation entropy 쪽으로 이동할 수
있다. 따라서 “실데이터 피팅이 된다”는 사실은 이 단위 결함을
반증하지 못한다. 오히려 fitted barrier가 단위·prefactor 오류를
보상했을 가능성을 검증해야 한다.

판정:

- C-rate는 입력 경계에서 `h^-1` 또는 무차원 C-rate로 명시하고,
  kinetics 내부에서는 SI `s^-1`로 한 번만 변환한다.
- 기존 barrier 값은 단위 교정 전 물질 고유값으로 승격하지 않고
  `UNVERIFIED`로 둔다.
- time-unit invariance와 `RT ln 3600` 재매개 가능성을 회귀 gate로
  추가한다.

### INTENT-PROV-0158 — barrier 식의 `Omega` 회계가 문건과 코드에서 다르게 읽힌다

A09는 보편식의 산문·식이 `A_j`에 이미
`-Omega(1-2xi)`를 포함하면서, 다시
`Delta G_eff = Delta G - chi Omega`를 사용해 `chi Omega`를 두 번
차감하는 것으로 읽힌다고 지적했다. 당시 코드 경로는 ideal/frozen
구동력과 effective barrier를 조합해 한 번만 적용한다.

판정:

- interaction contribution을 equilibrium chemical potential,
  metastable driving force, activation barrier lowering 중 어느
  슬롯에 넣는지 자유에너지 도식에서 먼저 정한다.
- 같은 `Omega` 기여를 state function과 barrier closure에 이중
  계상하지 않는다는 식별 규칙을 둔다.
- 현 문건의 universal equation은 코드와 1:1 대응한다고 볼 수 없어
  `CORRECT`.

### INTENT-PROV-0159 — 열역학 좌표와 표준상태의 다리가 아직 완결되지 않았다

A11은 분배함수·logistic·Bragg–Williams 대수 자체는 대부분
재유도에 통과했지만, 그 사이의 물리 명명이 흔들림을 찾았다.

- `epsilon_0-mu`를 level energy라고 부르는 오서술.
- chemical potential과 electrochemical potential의 혼용.
- 혼합 자유에너지 `g(theta)`에서 선형 표준상태 항 `mu^0 theta`를
  생략한 채 `U_j`가 갑자기 등장하는 유도 비약.
- 충·방전의 전류 부호와 화학적 삽입 방향을 늦게 정의하는 구조.
- 모든 초기 `Omega_j>2RT`인데 phase label이 그 조건으로부터
  유도된 것처럼 읽히는 분류.

판정:

- neutral-Li chemical potential, charged-species electrochemical
  potential, electrode potential, cell terminal voltage를 층별로
  정의한다.
- `mu^0`, `U_j`, mixing/interactions의 기준 자유에너지 관계를
  Legendre 변환과 평형 조건으로 연결한다.
- 실험 staging label과 regular-solution stability classification을
  별도 열로 둔다.

### INTENT-PROV-0160 — 엔트로피 장은 유용하지만 단일 Einstein mode를 물질 법칙으로 쓰면 안 된다

A12·A13은 configurational, vibrational, electronic entropy를
분리하려는 방향과 다수의 수학식을 재검산했다. 보존할 핵심은
다음이다.

- `partial S_vib / partial ln omega = -C_mode` 관계.
- configurational entropy의 logistic 특수형.
- 자유에너지 적분과 엔트로피 미분의 round-trip.
- 전자 엔트로피의 Sommerfeld 한계.

그러나 현 단일 Einstein closure는 반응 전후 모드 집합의 차를
“알짜 +1 모드, 진폭 R”로 접어 놓았다. 그 결과

- 고전극한에서 잔여가 상쇄되지 않고 오히려 커진다.
- `partial Delta S_vib / partial T`의 부호가 항상 양으로 고정된다.
- 경화형 또는 음의 `Delta C_p` 잔여를 표현하지 못한다.
- electronic 항과의 식별 근거는 기준온도 영점이 아니라 매우 작은
  곡률뿐인데, 보고서 재계산상 신호가 약 `0.06–0.08 microV/K`다.

또한 “리튬화하면 일반적으로 `Delta S_e<0`”라는 문장은 부호를
결정하는 `partial g(E_F)/partial x`의 물질 의존성을 지운다.

판정:

- 단일 Einstein mode는 `EMPIRICAL_ONLY` 축약으로 한정한다.
- 물리 정본은 reactant/product phonon DOS 차 또는 부호·모드수까지
  식별되는 reduced basis에서 시작한다.
- vibrational/electronic 분리는 최소 3온도점이라는 형식 조건뿐
  아니라 필요한 정밀도와 identifiability를 함께 명시한다.

### INTENT-PROV-0161 — 폭의 열적 서식과 히스테리시스의 온도 의존은 서로 독립 검증 대상이다

A13–A15는 완전식의 configurational 항이
`partial w_j/partial T`에서 생긴다는 점을 확인했다. 따라서
`w_j=n_jRT/F`를 가정한 완전식과 실측 폭이 온도에 거의 무관한
경우의 단순식은 같은 데이터에 다른 엔트로피 계수를 준다. 당시
예제의 차이는 약 `0.3 mV/K` 규모다.

동시에 hysteresis branch 식은 `Delta U_hys`를 기준온도에서
동결해야만 제시된 형태가 된다. regular-solution spinodal gap을
그대로 온도에 살리면 각 branch에
`±(1/2) partial Delta U_hys/partial T`가 추가되며, 보고서 예제에서는
약 `0.15 mV/K`로 반응 엔트로피와 같은 자릿수다.

판정:

- `w(T)`의 열적, 동결, 데이터 기반 서식을 경쟁 hypothesis로 둔다.
- reversible entropic coefficient는 branch 평균/평형 경로와
  hysteretic dissipation을 분리한 뒤 추정한다.
- `eq:weighted` 단순식과 config 포함 완전식을 서로 포함한다고
  서술한 A14의 오귀속은 `CORRECT`.
- spinodal gap의 온도 미분을 버린 branch 식을 보편 열역학식으로
  쓰지 않는다.

### INTENT-PROV-0162 — 내부 round-trip과 실험 검증을 같은 PASS로 부르면 안 된다

A14–A16은 부호, 표 좌표, 유일근, finite difference, 코드 회귀를
꼼꼼히 재계산했다. 이 자산은 보존 가치가 높다. 그러나 예제 입력은
문헌 스케일에 맞춰 정한 값이며, 같은 입력으로 생성한 곡선과
미분식을 다시 대조한 것은 독립적인 실험 검증이 아니다.

특히:

- `Delta S_j` 입력을 같은 문헌 프로파일에 대조한 것은 일부가
  traceability이지 out-of-sample validation이 아니다.
- `standardised2024`는 calorimetry 직접 관측 논문이 아니라
  potentiometric entropy-coefficient protocol이다.
- `numverif2026`과 175점 일치는 self-consistency regression이다.
- 실제 data fit, protocol transfer, held-out temperature/rate,
  calorimetry 교차검증은 남아 있다.

판정:

- algebra/unit/limit/round-trip/code regression은
  `INTERNAL_VERIFICATION`.
- parameter provenance, same-data reproduction, held-out prediction,
  cross-modal validation을 별도 tier로 둔다.
- “측정급 곡선”이라는 표현은 실제 데이터와 불확실도 gate 전에는
  사용하지 않는다.

### INTENT-PROV-0163 — 코드 대응 부록은 필요하지만 물리 본문과 다른 정본이어야 한다

A16은 코드맵에서 실재하지 않는 `T_work` 식별자, 오래된 v1.0.19
anchor, 병합 후 거짓이 된 “함수명은 이 부록에만”이라는 문장,
열특성 진입점 입력 누락을 찾았다. 동시에 `z_cut`, `A_cap_RT`,
`use_dH_eff`가 기본값으로 표에 고정돼 있었다.

판정:

- 식별자·API·default·solver tolerance·bit-exact 회귀는
  implementation concordance에 둔다.
- physics manuscript에는 코드 함수명과 기본값을 두지 않는다.
- 모든 default는 `physical constant`, `measured input`,
  `literature prior`, `fit initial value`, `numerical guard`,
  `disabled optional closure`로 분류한다.
- 임의 cut/cap은 기본 활성화하지 않고, 필요 시 데이터·수치 오차
  연구와 함께 명시적으로 opt-in한다.

### INTENT-PROV-0164 — A09–A16의 수정안을 그대로 적용하지 않는다

이번 묶음은 실제 결함을 다수 찾았지만 일부 제안은 문장을 더
붙여 기존 closure를 정당화하는 방식이다. 예를 들어 임의 cap의
“안전성” 설명, single-mode 진폭 추가, spinodal gap 동결 관례,
폭의 열적 서식 유지가 그렇다.

판정:

- 재계산 로그와 결함 위치는 `PRESERVE`.
- 제안 LaTeX는 `UNVERIFIED` 후보이며 기계 적용하지 않는다.
- 최종 채택은 first-principles consistency, literature evidence,
  parameter identifiability, experimental falsifiability,
  code-theory concordance를 모두 통과해야 한다.

## Coverage Status

- 이 batch의 8문건, 2,644행은 `READ`.
- 누적 coverage 반영 후 목표는 187문건, 42,443행이다.
- v1.0.22 잔여 목표는 30문건, 5,239행이다.

## Next

Step 19.6I:
FR A17–A19 및 A21–A23 심층 review 6문건 2,894행을 전문 검독해
LCO, Si, SiO_x, Si–C/blend 물리와 최종 심층 검토의 잔여 판정을
복원한다.
