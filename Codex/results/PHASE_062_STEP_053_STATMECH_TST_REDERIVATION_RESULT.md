# Phase 062 Step 053 — v1.0.21 대정준 전하 보존·TST 재유도 결과

## 판정

- 상태: `PASS_WITH_CONCERNS`
- Precommit Gate: `PASS_P062_STEP53_STATMECH_TST_REDERIVATION`
- Postcommit terminal: `PENDING_AT_PRECOMMIT_BY_DESIGN`
- 범위: frozen v1.0.21 Q2/Q3 내부 수식·가정·교차참조의 독립 재유도와 조건 경계.
- 외부 권위: `UNVERIFIED_EXTERNAL`; external scientific/material/experimental truth 및 primary-reference proposition support는 모두 false.
- `Claude/**` 수정: 0.

## 입력과 전문 검독

- frozen baseline `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`; Q2 `1635bc97fb7bd9c3fabc720e91bf09e5ba31798f`; Q3 `c7420915dfae8ef076319737bddcc532a86d9505`.
- 최종 release text/process 파일 `9/9`개, `1425`행을 1–EOF 직접 검독했다.
- Q2/Q3 load-bearing source span `14`개는 원문 전체·행 범위·Git blob·SHA-256으로 고정했다.
- Q2/Q3 snapshot strict traversal nodes `2285`; snapshot은 구조 diff evidence일 뿐 과학 truth가 아니다.

## Q2 — 다클래스 대정준 재유도

부호를 먼저 고정한다: `mu_molar(V)=mu0_molar-sF(V-U)`. `s=+1`이면 `dmu/dV=-F`, `xi=1-theta`이므로 전위가 오를수록 추출 진행률이 증가한다.

독립 hard-core 자리에서는 `Xi_1j=1+exp[-(eps_j-mu)/(RT)]`, `Xi=product_j Xi_1j^Mj`, `theta_j=[1+exp((eps_j-mu)/(RT))]^-1`, `<N>=sum Mj theta_j`가 이어진다. 한 자리당 한 전자를 전제로 `Qj=(F/NA)Mj`를 쓰면 `sum Qj xi_j=Q xbar`가 된다.

molar chemical potential 기준 응답은 `d<N>/dmu=Var(N)/(RT)`이고, 전위 residual 미분은 `sF/(RT) sum Qj theta_j(1-theta_j)`다. 따라서 비음이 아니라 **양의 분산**이 strict monotonicity의 필요조건이다. 존재성은 별도이며, 유한 전위 구간에서는 목표가 endpoint image 안에 있어야 한다. Source의 blanket `>0`·unique-root solver 계약은 이 조건들을 빠뜨려 `CORRECT`다.

- multiclass root `-0.040328287409` V, residual `-1.110e-16`.
- analytic/finite-difference derivative error `5.678e-11`.
- `N_p=1` closed/numeric inverse error `6.939e-18` V.
- coupled two-site variance-response error `5.094e-14`, while independent-product mean error `1.957e-01`.
- zero weight, duplicate energy, saturation, finite domain, degeneracy, coupled class and nonconvex branch는 각각 존재/유일성 축을 분리해 machine artifact에 고정했다.
- interacting self-consistent mean field의 감도는 Bernoulli 분산합과 달라 `평균장 수준에서 정확`이라는 문구를 교정해야 한다.
- `Qj=(F/NA)Mj`는 C 기준이다. Ah는 `/3600`, normalized capacity는 `Qj/Qcell`을 명시해야 하며, 단순 constraint inversion과 Legendre-Fenchel potential duality도 분리해야 한다.
- Q2 추가 display는 snapshot의 labeled 4개가 아니라 unnumbered capacity identity를 포함한 5개다.

## Q3 — TST 재유도와 교정

현재 source의 single-site pseudo-first-order 범위(`[s^-1]`)에서, 일관된 표준상태의 무차원 `K_dagger`와 transmission coefficient를 유지한 식은 `k=kappa(kBT/h)K_dagger exp[-DeltaE0/(RT)]`이다. Source 식은 `kappa=1`, classical separable reaction coordinate, no recrossing/tunneling인 특수형이다.

`L(T)=ln K_dagger(T)`라 두면 `DeltaG=DeltaE0-RTL`, `DeltaS=-DeltaE0'+RL+RT L'`, `DeltaH=DeltaE0-T DeltaE0'+RT^2 L'`, `DeltaCp=-T DeltaE0''+R(2T L'+T^2 L'')`이다. 그러므로 source의 `DeltaS=R ln(q-dagger/qR)`는 energy-zero derivative와 partition-ratio derivative가 모두 0일 때만 회수된다.

- temperature-dependent ratio probe: source entropy `0.000000` vs corrected `6.894325` J mol^-1 K^-1.
- entropy finite-difference error `3.479e-10`; heat-capacity error `8.617e-10`.
- omitting `kappa=0.37` changes the rate by factor `2.702703`.
- source의 `sqrt(kBT/(2*pi*m))`는 조건부 양의 속도 평균이 아니라 one-sided flux moment다. 조건부 평균/flux-moment 비는 `2.0`이다.
- classical harmonic high-T에서 reduced transition state가 안정 모드 하나 적으면 `K_dagger proportional to T^-1`이고 `(kBT/h)K_dagger`의 T 거듭제곱이 상쇄된다. 반대로 `K_dagger=1`은 Eyring prefactor의 T 인자를 남기므로 일반적인 constant-prefactor pure Arrhenius가 아니다.
- equilibrium TST background does not derive electrode overpotential/current, recrossing, nucleation/growth, phase-boundary motion, barrier distributions or measured dQ/dV width.

## 주장별 판정

| Claim | Derivation state | Source disposition | External support |
|---|---|---|---|
| `P062-S53-GC-001` | `CONDITIONAL_ASSUMPTIONS` | `PRESERVE` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-002` | `CONFIRMED_INTERNAL_DERIVATION` | `PRESERVE` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-003` | `CONFIRMED_INTERNAL_DERIVATION` | `PRESERVE` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-004` | `CONFIRMED_INTERNAL_DERIVATION` | `PRESERVE` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-005` | `CONFIRMED_INTERNAL_DERIVATION` | `PRESERVE` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-006` | `CONDITIONAL_ASSUMPTIONS` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-007` | `CONFLICTING` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-008` | `NOT_DERIVED` | `UNVERIFIED` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-009` | `CONFIRMED_INTERNAL_DERIVATION` | `PRESERVE` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-010` | `NOT_DERIVED` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-011` | `NOT_DERIVED` | `REJECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-012` | `CONFLICTING` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-013` | `CONDITIONAL_ASSUMPTIONS` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-GC-014` | `CONFLICTING` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-001` | `CONDITIONAL_ASSUMPTIONS` | `PRESERVE` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-002` | `CONDITIONAL_ASSUMPTIONS` | `PRESERVE` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-003` | `CONFLICTING` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-004` | `CONDITIONAL_ASSUMPTIONS` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-005` | `CONDITIONAL_ASSUMPTIONS` | `PRESERVE` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-006` | `CONFLICTING` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-007` | `CONFLICTING` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-008` | `NOT_DERIVED` | `UNVERIFIED` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-009` | `NOT_DERIVED` | `UNVERIFIED` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-010` | `NOT_DERIVED` | `REJECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-011` | `CONFLICTING` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-012` | `CONFLICTING` | `CORRECT` | `UNVERIFIED_EXTERNAL` |
| `P062-S53-TST-013` | `CONFLICTING` | `CORRECT` | `UNVERIFIED_EXTERNAL` |

## Findings and routing

- P0 `0`; P1 `5`; P2 `5`.
- P1: 일반 활성화 엔트로피 식의 온도 미분항 누락, self-consistent mean-field에 대한 독립 Bernoulli 증명의 과잉 확장, 조건이 빠진 blanket unique-root solver 계약, Maxwell flux-moment 오명명, high-T/순수 Arrhenius 극한 과장을 `CORRECT`로 라우팅한다.
- P2: Legendre 용어, capacity basis, unnumbered Q2 equation denominator, standard-state/`kappa`, equilibrium TST→electrode/peak-width 권위 승격을 각각 교정·차단한다.
- 발견된 오류는 frozen `Claude/**`에 직접 고치지 않았고 후속 canonical theory/manuscript 단계의 명시적 correction route로 남긴다.

## 검증과 다음 단계

- 독립 대수, exact coupled-state enumeration, bisection, central finite difference, analytic limiting cases를 사용했다.
- required negative controls: wrong sign, missing weight, variance-zero uniqueness, hidden interaction, constant-ratio misuse, omitted `kappa`, state-free electrode barrier, TST-to-width promotion.
- machine artifact SHA-256: `934be5273a91578b712d3ab44ef96eebb4cf7645973ec101b4e233b49426de16`.
- 실행 명령: `py -3.12 Codex/work/v1021_phase062/validate_phase062_step53.py --content-only --run-negative-probes --determinism-check`; 같은 명령을 `py -3.14`로도 실행했다.
- 두 런타임 모두 content Gate, negative controls `36/36`, Markdown negative controls `9/9`, builder-policy negative controls `11/11`, builder CRLF portability `1/1`, determinism `2/2`, symbolic checks `15/15`, numeric checks `20/20`, strict JSON traversal `956` nodes/depth `5`를 통과했다.
- exact-seven 예정 subject: `audit(phase062): rederive v1021 statmech tst`.
- Step 54는 이 exact-seven commit의 push 및 `PASS_P062_STEP53_PERSISTENCE` 확인 후에만 시작한다.
