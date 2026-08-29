# Phase 064 Step 66 Ratio/Transfer Rederivation Result

정본일: 2026-08-29

Status: `PASS_PENDING_PERSISTENCE_WITH_CORRECTIONS`

Gate: `PASS_P064_STEP66_REDERIVATION`

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

Expected parent: `5fb19384e3df7a73c96fcf26e8f599b42c331ae7`

Expected subject: `audit(phase064): rederive v1023 ratio transfer closure`

Postcommit persistence terminal: `PASS_P064_STEP66_PERSISTENCE`

Phase ceiling after this Step: `CONDITIONAL_P064`

## 1. 결론

Step 66은 JCP 147/Ref. 6의 Fredholm ratio/reference chain과 v1.0.23의 graphite lag를 독립 재유도했다. 두 문제는 literal identity가 아니다. 전자에서 후자로 이전 가능한 것은 ``미지 의존성을 고립하고 동일 경계·극한을 만족하는 가해 reference로 치환한 뒤 근사 오차를 검증한다''는 설계 원리뿐이다.

Graphite 식은 protocol을 따라 증가하는 유향 전압좌표 `x`에서 causal nonlinear Volterra equation이며 같은 좌표에서 1계 local ordinary differential equation (ODE)과 동치다. 단, v1.0.23이 ``참 문제''라고 부른 상태의존 `kappa(xi)`는 full kinetics를 복원한 exact law가 아니라 interaction-dependent forward exponential 한 항만 복원하고 나머지를 동결한 reduced feedback hypothesis다. 이번 Step은 이 권위 경계를 정정한다.

또한 다음 load-bearing 오류·과장을 정정했다.

- JCP 147 Eq. 38의 angular factor는 `exp(K*sigma*mu)`다. Step 65 ASCII semantic projection의 `exp(K*r*mu)`는 오기이며 PDF crop/raw identity는 정상이다.
- `epsilon = g*Delta xi_support`는 dimensionless local leading-order indicator이지 그 자체가 rigorous global contraction constant 또는 ``안전 증명서''가 아니다.
- `H(omega_x)=1/(1+i*omega_x*L0)`에서 `omega_x`의 단위는 `V^-1`이다. sweep-rate model 없이 time, electrochemical impedance spectroscopy (EIS), instrument response로 승격할 수 없다.
- C-rate `[h^-1]`를 Eyring rate `[s^-1]`와 결합할 때 `1/3600`이 필요하다. 현재 frozen runtime은 kinetics와 current/capacity unit contract를 분리하지 않아 `L_q`, `L_V`, `L_V/w`를 같은 실제 C-rate에서 3600배 크게 만들 수 있다.
- 따라서 `0.1 <= L_V/w <= 0.6`은 synthetic dimensionless test window로만 남고, ``중간전류'' 또는 특정 C-rate window라는 물리 라벨은 재산정 전 승인하지 않는다.

## 2. 복구 및 저장소 경계

- active branch: `codex/anode-fit-v1025_2-canonical-completion`.
- Step 65 commit: `5fb19384e3df7a73c96fcf26e8f599b42c331ae7`.
- Step 65 subject: `audit(phase064): bound v1023 literature authority`.
- Step 65 persistence: Python 3.12/3.14 `PASS_P064_STEP65_PERSISTENCE`.
- protected branch local/tracking/live: `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`.
- main tracking/live: `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`.
- frozen source baseline: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`.
- `Claude/**` tracked/staged/untracked mutation: `0/0/0`.

## 3. 실제 확인 입력과 범위

Controller는 master plan `1–665`, Phase 064 detailed plan `1–586`, Step 65 result `1–254`를 재독했다. Step 66 직접 수식 입력은 다음과 같다.

| Path | Frozen blob | Read coverage |
|---|---|---:|
| `Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md` | `ce4b17399f8d7318b4053134959ab77f9038d313` | `1–225` |
| `Claude/docs/v1.0.23/_sections/ch1_appE_selfconsistent.tex` | `b0e246c7bd31c63134137066d31a6032d4d190d7` | `1–212` |
| `Claude/docs/v1.0.23/_sections/ch1_sec08_lag.tex` | `15cd3c78f37dea9a1b942108d01df3db62101a6f` | `1–145` |
| `Claude/docs/v1.0.23/_sections/ch1_sec09_tail.tex` | `490139d35601c8d83da6d567bcdcf2ac97619d1c` | `1–245` |
| `Claude/docs/v1.0.23/_sections/ch1_sec10_sum.tex` | machine evidence에서 고정 | `1–170` |
| `Claude/docs/v1.0.23/results/comp_v23/COND_AUDIT.md` | `3c840b4a67b9c8b134c76c984efe34fba9271915` | `1–301` |
| `Claude/docs/v1.0.23/results/comp_v23/p1_ratio_check.py` | `b3b62159919fce6d4c4665b234d74456fa0fcf10` | `1–68` |
| `Claude/docs/v1.0.23/test_gates_v1023_selfconsistent.py` | machine evidence에서 고정 | `1–128` |

`Anode_Fit_v1.0.23.py`는 controller가 `105–210`, `450–535`, `630–710`을 직접 재독했고 independent reviewers가 lag/current/transfer 소비 경로를 확대 검독했다. frozen source 전체 `1–1585`는 Step 64에서 이미 전문 검독됐으며 이번 Step은 targeted rederivation coverage를 별도로 기록한다.

JCP 147 VOR `10/10`과 Ref. 6 VOR `4/4`의 전문 검독 권위, raw hash, page/equation anchors는 Step 65 machine artifacts를 입력으로 사용했다. Controller는 JCP PDF page 5를 다시 추출·대조했고 independent reader는 Eq. 38 crop을 원문 확대 재확인했다. Ref. 7 원문은 계속 `GROUND_NOT_FOUND`이며 추정으로 보완하지 않았다.

## 4. Fredholm source chain 독립 재유도

JCP 147의 공간은 `r in [sigma,infinity)`, `mu in [-1,1]`이고 대상은 ultimate survival probability다. `Wbar_u(r) -> 1` as `r -> infinity`, contact에서 zero radial derivative가 경계다. Eqs. 19–20은 direction-resolved survival을 orientation average로 치환하는 critical approximations다.

`a(r1)=r1^2 Lambda(r1) exp[-U1(r1)]`라 두면 Eq. 32는 그 근사계 안에서

```text
W(r) = 1
 - chi(sigma/r)/(D*sigma) * integral_[sigma,r] a(r1) W(r1) dr1
 - 1/(D*sigma) * integral_[r,infinity] chi(sigma/r1) a(r1) W(r1) dr1.
```

첫 구간 `[sigma,r]`에서는 `chi(sigma/r)`가 관측점에 고정되고, 둘째 `[r,infinity]`에서는 `chi(sigma/r1)`가 적분점에 따라 변한다. 같은 fixed semi-infinite domain의 contact-side와 infinity-side를 함께 결합하므로 causal triangular kernel이 아니며 `r,r1` 교환 대칭도 아니다.

`W(r) != 0`에서 Eq. 32를 `W(r)`로 나누면 Eq. 33 inverse-bracket form이 된다. 이는 Eqs. 19–20 근사계 내부의 exact algebraic rearrangement일 뿐이다. Eq. 34에서

```text
W(r1)/W(r) ~= W_delta(r1)/W_delta(r)
```

로 바꾸는 순간 reference-ratio approximation이 들어간다. Eqs. 35–36은 long-range sink와 contact delta sink의 Boltzmann-weighted integrated reactivity를 맞춰 `kappa(mu)`를 정하고, Eq. 37은 solvable contact reference ratio, Eq. 38은

```text
Lambda_rx = 4*pi*exp[U1(sigma)] * integral_0^infinity r^2 exp[-U1(r)]
            * (1/2) integral_-1^1 exp[K*sigma*mu] S_R(r,mu) dmu dr
```

를 정의한다. Eq. 39는 이 reference ratio를 Eq. 33에 대입한 approximate closed result다.

Ref. 6 Eqs. 9–12도 transformed radial fixed domain에서 exact Fredholm/rearrangement chain을 유지한 뒤 미지 propagator ratio를 solvable reference ratio로 바꾸는 시점에 근사가 들어간다. leading Eq. 13은 small-Laplace-variable limit에서 exact하다는 원 논문의 범위를 graphite에 이전하지 않는다.

## 5. Graphite reduced Volterra model 재유도

충·방전 모두에서 protocol을 따라 증가하는 유향 전압좌표를 `x`로 둔다. 방전 convention은 `x=V`, 거울 충전 convention은 `x=-V`다. `r=xi_eq-xi`, `sigma_x=d xi_eq/dx`, `kappa=1/L_V`라 두면 선택된 reduced feedback model은

```text
dr/dx = sigma_x(x) - kappa(xi_eq(x)-r(x))*r(x),
r(x0) = r_initial.
```

같은 initial condition에서 integrating factor를 쓰면 정확히 동치인 causal nonlinear Volterra form은

```text
r(x) = r_initial*exp[-integral_x0^x kappa(xi(v)) dv]
     + integral_x0^x sigma_x(u)
       * exp[-integral_u^x kappa(xi(v)) dv] du,
xi(v) = xi_eq(v)-r(v).
```

`x0 -> -infinity`, `r` bounded, `kappa >= kappa_min > 0`일 때만 initial term을 0으로 보내는 remote-past form이 정당하다. finite measurement window에서는 initial state를 버릴 수 없다.

v1.0.23의 selected reduced law는

```text
L(xi)=L0*exp[g*(1-xi)],
kappa(xi)=kappa0*exp[-g*(1-xi)],
g=2*chi_d*Omega/(R*T).
```

이 식 아래에서 ODE–Volterra equivalence는 exact다. 그러나 이 `L(xi)` 자체는 full forward/reverse rate, ideal-voltage dependence, cut rule과 voltage/capacity slope를 모두 복원한 law가 아니다. 따라서 `REDUCED_FEEDBACK_HYPOTHESIS`로 분류한다.

Frozen reference는 `kappa0=1/L0`:

```text
r0' = sigma_x-kappa0*r0,
r0(x) = r_initial*exp[-(x-x0)/L0]
      + integral_x0^x sigma_x(u) exp[-(x-u)/L0] du,
xi0=xi_eq-r0.
```

Volterra operator를 `T`라 하면 첫 reference-trajectory/Picard iterate는

```text
r1=T[r0],
r1' = sigma_x-kappa(xi0)*r1,
xi0=xi_eq-r0.
```

이다. 이 `r1`은 JCP solution ratio와 같은 객체가 아니며, Eq. 34가 graphite 식을 증명한 것도 아니다. Eq. 34는 reference substitution 설계에 동기를 제공했을 뿐이다. `g=0`이면 `kappa=kappa0`여서 동일 initial condition에서 `r=r1=r0`가 exact하다.

## 6. 수축성과 타당성

remote-past/zero-initial operator에서 `kappa >= kappa_min > 0`, `|partial kappa/partial xi| <= K_kappa`, `||sigma_x||_infinity < infinity`라 하면 Volterra operator에 대해

```text
||T[r]-T[s]||_infinity
 <= q_sufficient ||r-s||_infinity,
q_sufficient = ||sigma_x||_infinity*K_kappa/kappa_min^2.
```

따라서 `q_sufficient < 1`은 실제 sufficient contraction condition이다. 모든 인자의 단위를 쓰면 `[sigma_x]=V^-1`, `[K_kappa]=V^-1`, `[kappa_min]=V^-1`이므로 `q_sufficient`는 dimensionless다.

약한 local modulation에서 `K_kappa ~= g*kappa0`, `kappa_min ~= kappa0`, logistic `||sigma_x||_infinity=1/(4w)`를 쓰면

```text
q_local ~= g*L0/(4w) = g*Delta xi_support,
Delta xi_support ~= L0/(4w).
```

가 된다. 기존 `epsilon`은 이 local leading-order estimate로만 유지한다. 제한된 synthetic cases에서 error ratio와 상관된다는 사실은 global theorem, universal `epsilon=0.5` threshold 또는 JCP 세 조건과의 primary-source 1:1 identity를 만들지 않는다.

## 7. Voltage-coordinate transfer identity

Frozen equation `L0*d xi_lag/dx + xi_lag = xi_eq`와 Fourier convention

```text
f_hat(omega_x)=integral f(x) exp[-i*omega_x*x] dx
```

에서

```text
H(omega_x)=xi_lag_hat/xi_eq_hat=1/(1+i*omega_x*L0).
```

`[omega_x]=V^-1`, `[L0]=V`, `H`는 dimensionless다. 이는 infinite/adequately extended directed-voltage domain의 linear frozen filter identity다. finite discrete Fourier transform은 circular convolution이므로 padding/initial-condition/window contract 없이 causal convolution과 같지 않다.

시간 변환에는 별도 sweep rate `nu=dx/dt`가 필요해 `tau=L0/|nu|`가 된다. 이 protocol-specific change of variable은 EIS, instrument transfer function 또는 electrochemical relaxation mechanism의 외부 권위를 제공하지 않는다.

## 8. C-rate/timebase 정정

`q=Q/Q_cell`을 dimensionless capacity fraction, `C_h`를 `[h^-1]`, `t_s`를 seconds로 두면

```text
dq/dt_s = C_h/3600.
```

`Q_cell`이 ampere-hour (Ah), current가 ampere (A)면 `I_A=C_h*Q_Ah`이지만 normalized rate는 `I_A/(3600*Q_Ah)`다. `Q_cell`이 coulomb (C)이면 normalized rate는 `I_A/Q_C`다. Eyring `k`가 `[s^-1]`일 때

```text
L_q = (dq/dt_s)/k,
L_V = |dV/dq|*L_q.
```

따라서 current `[A]`와 normalized rate `[s^-1]`를 서로 다른 quantity로 전달해야 한다. IR term에는 current가, kinetics에는 normalized rate가 필요하다. 기존 단일 `I,Q_cell` contract는 Ah 경로와 coulomb 경로를 동시에 만족시키지 못한다.

같은 실제 C-rate에서 legacy `L_q`, `L_V`, `L_V/w`는 corrected value의 3600배다. 같은 dimensionless `L_V/w`를 회복하려면 다른 인자가 같을 때 rate가 3600배 필요하다. barrier로 보상하려면 298.15 K에서 `R*T*ln(3600)=20.30 kJ/mol`가 추가로 필요하다. 그러므로 기존의 `middle-current`, `C-rate~1`, `80 kJ/mol visible-tail` 물리 숫자는 재산정 전 승인하지 않는다.

## 9. 계산 경로와 benchmark 권위

Frozen, first-ratio/Picard, converged Picard는 같은 directed grid에서 각각 one pass, frozen plus one correction pass, frozen plus multiple correction passes다. fixed iteration count에서 모두 `O(N)`이며 first ratio output은 first Picard iterate와 동일하다.

Independent disposable benchmark는 Windows 11 build 26200, Python 3.14.4, NumPy 2.5.0, `N=8000`, `x=[-0.15,0.35] V`, `w=0.02 V`, `L0=0.006 V`에서 수행했다. reference는 external/material truth가 아니라 frozen operator의 sup-delta `<=1e-13` converged fixed point다.

| `g_eff` | frozen ms | ratio ms | converged Picard ms / iterations | ratio/frozen | Picard/ratio | relative L2 lag error frozen -> ratio |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 4.0579 | 8.9484 | 50.3639 / 10 | 2.205 | 5.628 | 0.0118446 -> 0.000462266 |
| 1.0 | 4.0579 | 8.7944 | 59.6905 / 12 | 2.167 | 6.787 | 0.0290647 -> 0.00292961 |
| 2.0 | 4.0579 | 8.6916 | 87.6683 / 18 | 2.142 | 10.087 | 0.0918681 -> 0.0282658 |

판정은 comparator-dependent다. ratio는 frozen보다 느려 benefit이 음(-), first Picard와는 동일해 algorithmic benefit이 0, converged Picard보다는 빠르지만 근사오차가 남아 조건부 양(+)이다. local nonlinear ODE는 다른 one-pass integration도 가능하므로 이 synthetic implementation timing을 generic speedup으로 승격하지 않는다.

## 10. Result-first Human Evidence

아래 strict JSON block은 source self-report를 채택한 것이 아니라 controller와 독립 readers의 원문·수식·단위·runtime 검독을 기계 artifact에 전달하는 입력이다.

<!-- P064_STEP66_HUMAN_EVIDENCE_BEGIN -->
```json
{
  "authority_ceiling": "CONDITIONAL_P064_REF7_GNF_AND_FROZEN_DEFECTS_OPEN",
  "benchmark": {
    "authority": "INTERNAL_SYNTHETIC_RUNTIME_OBSERVATION_ONLY",
    "comparator_conclusion": {"ratio_vs_converged_picard": "POSITIVE_WITH_APPROXIMATION_ERROR", "ratio_vs_first_picard": "ZERO_IDENTICAL_OUTPUT", "ratio_vs_frozen": "NEGATIVE_SLOWER"},
    "environment": {"architecture": "AMD64", "numpy": "2.5.0", "os": "Windows 11 build 26200", "python": "3.14.4"},
    "input": {"L0_V": 0.006, "N": 8000, "center_V": 0.1, "convergence_sup_delta": 1e-13, "domain_V": [-0.15, 0.35], "w_V": 0.02},
    "rows": [
      {"g_eff": 0.5, "frozen_ms": 4.0579, "ratio_ms": 8.9484, "picard_ms": 50.3639, "picard_iterations": 10, "ratio_over_frozen": 2.205, "picard_over_ratio": 5.628, "lag_relative_l2_frozen": 0.0118446, "lag_relative_l2_ratio": 0.000462266, "peak_relative_l2_frozen": 0.0502759, "peak_relative_l2_ratio": 0.00263474, "ratio_equals_picard1": true},
      {"g_eff": 1.0, "frozen_ms": 4.0579, "ratio_ms": 8.7944, "picard_ms": 59.6905, "picard_iterations": 12, "ratio_over_frozen": 2.167, "picard_over_ratio": 6.787, "lag_relative_l2_frozen": 0.0290647, "lag_relative_l2_ratio": 0.00292961, "peak_relative_l2_frozen": 0.124001, "peak_relative_l2_ratio": 0.0169777, "ratio_equals_picard1": true},
      {"g_eff": 2.0, "frozen_ms": 4.0579, "ratio_ms": 8.6916, "picard_ms": 87.6683, "picard_iterations": 18, "ratio_over_frozen": 2.142, "picard_over_ratio": 10.087, "lag_relative_l2_frozen": 0.0918681, "lag_relative_l2_ratio": 0.0282658, "peak_relative_l2_frozen": 0.379598, "peak_relative_l2_ratio": 0.162313, "ratio_equals_picard1": true}
    ]
  },
  "contraction": {"global_scope": "REMOTE_PAST_OR_ZERO_INITIAL_TERM", "global_sufficient": "q=norm_sigma_infinity*K_kappa/kappa_min^2<1", "global_units": "(V^-1)*(V^-1)/(V^-1)^2=1", "local_indicator": "epsilon_local=g*L0/(4*w)", "local_status": "LEADING_ORDER_HEURISTIC_NOT_GLOBAL_THEOREM"},
  "corrections": [
    {"id": "P064-S66-CORR-001", "severity": "P0", "finding": "C-rate h^-1 and Eyring s^-1 are mixed; current and normalized rate contracts conflict", "disposition": "CORRECT_DERIVATION_AND_ROUTE_RUNTIME", "owner": "Phase 064 Step 67"},
    {"id": "P064-S66-CORR-002", "severity": "P1", "finding": "Step65 Eq38 semantic projection wrote exp(K*r*mu), original is exp(K*sigma*mu)", "disposition": "SUPERSEDE_SEMANTIC_PROJECTION_KEEP_PDF_CROP", "owner": "Phase 064 Step 66"},
    {"id": "P064-S66-CORR-003", "severity": "P1", "finding": "selected kappa(xi) was called the true full kinetics", "disposition": "DEMOTE_TO_REDUCED_FEEDBACK_HYPOTHESIS", "owner": "Phase 064 Step 66"},
    {"id": "P064-S66-CORR-004", "severity": "P1", "finding": "epsilon_local was promoted to a rigorous safety proof and universal threshold", "disposition": "REPLACE_WITH_GLOBAL_SUFFICIENT_BOUND_AND_LOCAL_HEURISTIC", "owner": "Phase 064 Step 66"},
    {"id": "P064-S66-CORR-005", "severity": "P1", "finding": "JCP applicability conditions were mapped 1:1 to graphite without primary-source authority", "disposition": "DEMOTE_TO_INTERNAL_ANALOGY", "owner": "Phase 064 Step 66"},
    {"id": "P064-S66-CORR-006", "severity": "P1", "finding": "voltage-coordinate omega was promoted to time EIS or instrument response", "disposition": "BOUND_TO_DIRECTED_VOLTAGE_COORDINATE", "owner": "Phase 064 Step 66"},
    {"id": "P064-S66-CORR-007", "severity": "P1", "finding": "unpadded FFT is circular and uniform-grid contract is not enforced", "disposition": "ROUTE_CODE_RUNTIME_BOUNDARY", "owner": "Phase 064 Step 67"},
    {"id": "P064-S66-CORR-008", "severity": "P1", "finding": "dimensionless L0/w window was labeled a physical middle-current window", "disposition": "RETAIN_DIMENSIONLESS_REJECT_CURRENT_LABEL", "owner": "Phase 064 Step 66"},
    {"id": "P064-S66-CORR-009", "severity": "P2", "finding": "declared scratchpad cond_audit_verify.py is absent from frozen evidence", "disposition": "GROUND_NOT_FOUND_ROUTE_VALIDATION_AUTHORITY", "owner": "Phase 064 Step 68"},
    {"id": "P064-S66-CORR-010", "severity": "P2", "finding": "p1_ratio_check default CP949 output exits after numeric work", "disposition": "REQUIRE_UTF8_INVOCATION", "owner": "Phase 064 Step 67"},
    {"id": "P064-S66-CORR-011", "severity": "P2", "finding": "tail illustration plots xi up to 2 despite normalized 0 to 1 state", "disposition": "ROUTE_SOURCE_DISPOSITION", "owner": "Phase 064 Step 69.1"}
  ],
  "evidence_date": "2026-08-29",
  "evidence_id": "P064-HUMAN-REDERIVATION-STEP66-001",
  "expected_parent": "5fb19384e3df7a73c96fcf26e8f599b42c331ae7",
  "expected_subject": "audit(phase064): rederive v1023 ratio transfer closure",
  "fredholm": {"eq32_status": "EXACT_WITHIN_EQ19_EQ20_APPROXIMATED_SYSTEM", "eq33_status": "EXACT_REARRANGEMENT_REQUIRES_NONZERO_W", "eq34_status": "REFERENCE_RATIO_APPROXIMATION", "eq38_angular_factor": "exp(K*sigma*mu)", "eq39_status": "APPROXIMATE_CLOSED_RESULT", "kernel_direction": "FIXED_DOMAIN_TWO_SIDED_NONCAUSAL", "radial_domains": [["sigma", "r"], ["r", "infinity"]]},
  "gate": "PASS_P064_STEP66_REDERIVATION",
  "ground_not_found": ["Ref7 original full text and equation chain", "scratchpad/cond_audit_verify.py", "primary-source proof of JCP-to-graphite variable mapping"],
  "readers": [
    {"reader": "controller", "scope": "master/phase/Step65 recovery; targeted frozen derivation sources; JCP page5; integration"},
    {"reader": "Kierkegaard", "scope": "JCP147 10/10; Ref6 4/4; Fredholm equation/boundary reconstruction"},
    {"reader": "Leibniz", "scope": "Volterra/ODE/contraction/transfer rederivation and adversarial source review"},
    {"reader": "Singer", "scope": "C-rate/timebase contract, frozen runtime probes and disposable benchmark"}
  ],
  "reduced_volterra": {"coordinate": "x increases along protocol; x=V discharge, x=-V mirrored charge", "frozen_limit": "g=0 implies r=r1=r0 with same initial condition", "initial_condition": "finite x0 term required unless remote-past decay assumptions hold", "model_authority": "REDUCED_FEEDBACK_HYPOTHESIS", "picard1": "r1=T[r0]", "problem_class": "NONLINEAR_CAUSAL_VOLTERRA_EQUIVALENT_TO_LOCAL_FIRST_ORDER_ODE"},
  "ref7_status": "GROUND_NOT_FOUND_NO_INFERENCE",
  "source_mutation_count": 0,
  "timebase": {"Ah_contract": "dq/dt_s=I_A/(3600*Q_Ah)=C_h/3600", "coulomb_contract": "dq/dt_s=I_A/Q_C", "legacy_overestimate_factor": 3600, "required_separation": ["current_A_for_IR", "normalized_rate_s^-1_for_kinetics"], "status": "CORRECTED_DERIVATION_FROZEN_RUNTIME_OPEN"},
  "transfer": {"fourier_convention": "fhat(omega_x)=integral f(x)*exp(-i*omega_x*x)dx", "formula": "H=1/(1+i*omega_x*L0)", "omega_units": "V^-1", "prohibited_promotions": ["TIME_WITHOUT_SWEEP_RATE", "EIS", "INSTRUMENT_RESPONSE"], "status": "VOLTAGE_COORDINATE_ONLY"}
}
```
<!-- P064_STEP66_HUMAN_EVIDENCE_END -->

## 11. 확정·미결·근거 미발견

### 확정

- JCP 147 Eq. 32/33/34/35–39의 exact/approximate boundary와 Eq. 38 `K*sigma*mu` 정정.
- Ref. 6 ratio/reference design principle의 원 문제 한정 권위.
- directed-voltage reduced ODE와 nonlinear Volterra의 조건부 exact equivalence.
- frozen `r0`, first Picard/reference trajectory `r1`, same-initial-condition frozen limit.
- rigorous sufficient contraction bound와 local `epsilon`의 더 낮은 권위.
- voltage-coordinate transfer identity의 단위와 Fourier convention.
- C-rate/Ah/C/s unit contract 및 factor 3600.
- comparator-dependent benchmark와 generic speedup 금지.

### 미결

- frozen runtime의 current/rate interface 실제 수리와 전체 consumer 영향: Step 67.
- circular FFT, nonuniform-grid rejection, finite-window initial-state behavior: Step 67.
- synthetic/internal gate의 최종 authority 분류: Step 68.
- correction owner들의 lossless disposition/carry: Step 69.1.

### 근거 미발견

- Ref. 7 original full-text equation chain.
- JCP/Ref. 6이 graphite mapping 또는 current regime를 직접 지지한다는 primary-source evidence.
- v1.0.23이 선언한 `scratchpad/cond_audit_verify.py` frozen artifact.

## 12. 검증 결과

- result-first human evidence: saved before builder and machine artifact.
- builder normal plus Python 3.12/3.14 check-only reconstruction: `PASS`; source `9/9`, corrections `11/11`, benchmark cases `4/4`; JSON-last same-directory temporary write, flush/fsync, atomic replace and cleanup used.
- Python 3.12/3.14 artifact validator: `PASS_P064_STEP66_REDERIVATION`.
- named semantic controls `36/36`, strict JSON duplicate/nonfinite/overflow/truncation controls `7/7`, full artifact traversal `733`, source contracts `9/9`, correction rows `11/11`, deterministic reconstructions `2/2`.
- independent final scientific, builder/validator adversarial and record/Git-boundary reviews: each P0/P1/P2=`0/0/0`.
- exact-seven staged/Git boundary: `PENDING`.
- postcommit persistence: `PENDING_AT_PRECOMMIT_BY_DESIGN`.

## 13. 다음 단계 조건

Step 66의 exact-seven commit/push 뒤 Python 3.12/3.14 `PASS_P064_STEP66_PERSISTENCE`가 확인되어야 Step 67로 진입한다. Step 67은 algebraic root와 causal Volterra를 분리하고, 이번 Step이 OPEN으로 넘긴 current/rate interface, circular FFT, nonuniform grid, finite-window initial state와 runtime portability를 frozen code/runtime boundary에서 판정한다.
