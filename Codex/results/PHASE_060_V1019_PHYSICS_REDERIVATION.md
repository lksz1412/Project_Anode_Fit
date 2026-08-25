# Phase 060 v1.0.19 독립 물리 재유도

상태: `PASS_WITH_CONCERNS`

권위 경계: 이 문서는 동결된 v1.0.19 source model의 내부 수식 정합, 차원, 부호, 극한과 구현 영향을 감사한다. 외부 문헌 진실성·재료 타당성·정본 채택을 확정하지 않는다.

## 1. 범위와 방법

- frozen source commit: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`
- 전문 검독: 31/31 files, 4544/4544 physical lines
- production implementation import/call: `false`
- 독립 경로: 직접 대수, 차원 분석, bisection, central finite difference, quadrature/convolution, free-energy round trip

## 2. 규약 동결

| ID | 기호 | 정의 | 단위 | 충돌 |
|---|---|---|---|---|
| `SYM-Q` | Q, Q_cell | absolute or normalized charge and cell capacity | C or Ah, but one timebase | CONFLICT-SIGNED-ICA |
| `SYM-X` | x, xbar | Li fraction x and delithiation fraction xbar=1-x | 1 | CONFLICT-X-XBAR |
| `SYM-XI` | xi_j, theta_j | delithiation progress and occupied fraction theta=1-xi | 1 | 없음 |
| `SYM-SIGMA` | sigma_d | Ch1 half-cell direction: discharge/delithiation +1, charge/lithiation -1 | 1 | CONFLICT-DISCHARGE-LABEL |
| `SYM-I` | I | Bernardi signed cell current, I>0 cell discharge | A | CONFLICT-DISCHARGE-LABEL |
| `SYM-VAPP` | V_app | measured half-cell voltage | V | 없음 |
| `SYM-VN` | V_n | internal voltage after ohmic correction | V | 없음 |
| `SYM-U` | U_j, U_oc | transition center and implicit equilibrium observation voltage | V | 없음 |
| `SYM-W` | w_j, n_j | logistic voltage scale and dimensionless thermal multiplicity | V; 1 | CONFLICT-WIDTH-STATE |
| `SYM-BG` | C_bg, Q_bg | background differential capacity and its unspecified primitive | charge/V; charge | CONFLICT-BACKGROUND-PRIMITIVE |
| `SYM-T` | T, T_rep | pointwise temperature and representative mean used by selected paths | K | CONFLICT-POINTWISE-REPRESENTATIVE-T |
| `SYM-HEAT` | qdot_rev | signed reversible heat into the declared cell control volume | W | CONFLICT-CONTROL-VOLUME |

## 3. 지배 잔차와 관측 변환

배경이 없는 branch-free 특수형에서 탈리튬화 분율 $\bar x=1-x$를 쓰면

\[F(U;\bar x,T)=\sum_j Q_j\,\xi_j(U,T)-Q\bar x=0,\qquad Q=\sum_jQ_j.\]

미분 가능하고 $F_U\ne0$인 국소 branch에서만

\[\frac{\mathrm dU}{\mathrm dQ}=-\frac{F_Q}{F_U},\qquad F_Q=-1,\qquad \frac{\mathrm dQ}{\mathrm dU}=F_U=\sum_jQ_jg_j.\]

따라서 $F_U\to0$에서는 DVA가 발산하고 전역 유일성은 보장되지 않는다. $C_\mathrm{bg}$가 0이 아니면 $Q_\mathrm{bg}$의 primitive와 기준 상수가 추가로 필요하다.

고정 $\bar x$에서 온도 미분하면

\[\left.\frac{\partial U}{\partial T}\right|_{\bar x}=-\frac{\sum_jQ_j(\partial\xi_j/\partial T)_U}{\sum_jQ_j(\partial\xi_j/\partial U)_T},\]

이며 $w_j=n_j(T)RT/F$인 경우 $\partial_Tw_j=(R/F)(n_j+Tn'_j)$가 반드시 들어간다. 직접 입력한 frozen $w_j$에는 같은 config 항을 자동 적용할 수 없다.

## 4. Check 판정

| Check | Family | Result | Derivation | Implementation | 핵심 판정 |
|---|---|---|---|---|---|
| `P060-PHY-001` | CONVENTION | `CONDITIONAL` | `BOUNDED` | `PARTIAL` | Both formulae are internally usable, but the same word discharge denotes opposite graphite reaction directions. |
| `P060-PHY-002` | THERMODYNAMIC_CENTER | `PASS` | `CLOSED` | `ALIGNED` | The stated center law follows from the declared reaction convention. |
| `P060-PHY-003` | EQUILIBRIUM_OBSERVATION | `FAIL` | `CLOSED` | `MISALIGNED` | Independent quadrature reproduces the positive magnitude, but the source silently relabels that magnitude as signed dQ/dV on charge. |
| `P060-PHY-004` | CHARGE_BALANCE | `PASS` | `CLOSED` | `PARTIAL` | The four-transition source fixture has a bracketed monotone root and reproduces the worked point. |
| `P060-PHY-005` | CHARGE_BALANCE | `CONDITIONAL` | `BOUNDED` | `ABSENT` | The source does not define the background primitive or its charge offset for the implicit composition solve. |
| `P060-PHY-006` | IMPLICIT_SENSITIVITY | `PASS` | `CLOSED` | `PARTIAL` | Analytic and independent charge finite differences agree within tolerance. |
| `P060-PHY-007` | UNIQUENESS | `CONDITIONAL` | `BOUNDED` | `PARTIAL` | The worked bisection root does not prove uniqueness for every admitted model path. |
| `P060-PHY-008` | WIDTH_THERMAL | `FAIL` | `CONFLICTING` | `MISALIGNED` | The no-n/no-w implementation has w=RT/F but reports dw/dT=0; the complete-input list also omits the required thermal-width state. |
| `P060-PHY-009` | HYSTERESIS | `CONDITIONAL` | `BOUNDED` | `PARTIAL` | The algebraic spinodal result closes, but gamma*h_eta and the use of a spinodal upper bound as observed hysteresis are not independently derived. |
| `P060-PHY-010` | KINETIC_LAG | `FAIL` | `CONFLICTING` | `MISALIGNED` | The source explicitly acknowledges a factor-3600 alternative while the runtime convention uses the unconverted numeric c-rate; the numerical seed lag is not dimensionally unique. |
| `P060-PHY-011` | CAUSAL_MEMORY | `PASS` | `CLOSED` | `PARTIAL` | Independent discrete convolution confirms normalization, positivity, mirroring and the small-lag limit within discretization tolerance. |
| `P060-PHY-012` | PROTOCOL_STATE | `FAIL` | `NOT_DERIVABLE` | `ABSENT` | The source closes two separate monotone sweep directions, not a stateful rest/reversal/finite-window protocol. |
| `P060-PHY-013` | THERMAL_MIXING | `CONDITIONAL` | `BOUNDED` | `PARTIAL` | The independent four-transition finite difference matches the complete expression only under w=RT/F; direct frozen width requires a different expression. |
| `P060-PHY-014` | EINSTEIN | `PASS` | `CLOSED` | `PARTIAL` | Independent free-energy finite differences reproduce Delta S_vib/F and the source's four illustrative slopes. |
| `P060-PHY-015` | LCO_ELECTRONIC | `FAIL` | `CLOSED` | `MISALIGNED` | The independent unit and T^2 round trip closes, but the reachable implementation freezes the electronic contribution at x_center and 298.15 K and therefore lacks the source T^2 path. |
| `P060-PHY-016` | REVERSIBLE_HEAT | `CONDITIONAL` | `BOUNDED` | `PARTIAL` | The numerical worked sign is reproduced, but half-cell/full-cell and Ch1 direction labels require an explicit assembly map. |
| `P060-PHY-017` | HYSTERESIS_HEAT | `CONDITIONAL` | `BOUNDED` | `ABSENT` | The source states a linearized branch-average rule, while no explicit reachable branch-average implementation exists. |
| `P060-PHY-018` | MATERIAL_PATH | `CONDITIONAL` | `BOUNDED` | `PARTIAL` | The half-cell forms are separable; the v1.0.19 source does not close the final full-cell composition path. |
| `P060-PHY-019` | BROADENING | `UNVERIFIED` | `NOT_DERIVABLE` | `PARTIAL` | No production ensemble calculator or source-grounded inverse-identification law closes the width budget. |
| `P060-PHY-020` | PARAMETER_AUTHORITY | `UNVERIFIED` | `NOT_DERIVABLE` | `NOT_APPLICABLE` | Several numbers are explicitly fit-only or ground-not-found; cited items remain source-cited-unverified until Phase 071. |
| `P060-PHY-021` | IDENTIFIABILITY | `CONDITIONAL` | `BOUNDED` | `PARTIAL` | Single-condition curves identify combinations such as L_V, gamma*h_eta*gap, and gmax/delta_x rather than every primitive parameter. |
| `P060-PHY-022` | HYSTERESIS | `FAIL` | `CONFLICTING` | `UNVERIFIED` | Two source sections make incompatible zero-current claims unless an unstated gamma->0 condition is imposed. |

## 5. 독립 수치 probe

- four-transition root: $U_{oc}=74.349724$ mV at $\bar x=0.25$, $T=298.15$ K.
- $dQ/dU=6.176820556$ $Q_\mathrm{cell}$/V, analytic $dU/dQ=0.161895589$ V/$Q_\mathrm{cell}$, finite-difference error `8.672e-11`.
- complete $\partial U/\partial T=-0.203949$ mV/K, finite-difference error `5.025e-15` V/K; $\dot Q_\mathrm{rev}/I=60.807459$ mV.
- lag timebase: unconverted/canonical ratio = `3600.0`.
- Einstein round-trip max error = `4.109e-16` V/K.
- LCO electronic gate-center $\Delta S_e=-45.964250$ J/(mol K), $T^2$ round-trip error `1.266e-14` V/K.

이 probe들은 source equation의 내부 대수·수치 왕복만 검증한다. 실험 또는 문헌 진실성은 검증하지 않는다.

## 6. Parameter authority

| ID | Parameters | Disposition |
|---|---|---|
| `PAR-GRA-U` | four graphite U values | `SOURCE_CITED_TIER_B_OR_C_NOT_PRIMARY_VERIFIED` |
| `PAR-GRA-DS` | four graphite DeltaS values | `SOURCE_CITED_RANGE_OR_PROFILE_NOT_TRANSITION_SPECIFIC_TRUTH` |
| `PAR-GRA-KIN` | Omega, DeltaH_a, dVdq | `FIT_INITIAL_OR_TREND_ONLY_GROUND_NOT_FOUND_TRANSITION_SPECIFIC` |
| `PAR-HYS` | gamma, h_eta | `EMPIRICAL_FIT_ONLY` |
| `PAR-EINSTEIN` | theta_E=700 K illustration | `ILLUSTRATIVE_OR_DATA_DRIVEN_NOT_MATERIAL_DEFAULT` |
| `PAR-LCO-DOS` | gmax=13 states/eV/atom | `SOURCE_CITED_SINGLE_ENDPOINT_NOT_PRIMARY_VERIFIED_HERE` |
| `PAR-LCO-GATE` | x_MIT=0.85, delta_x_MIT=0.05, continuous logistic gate | `SOURCE_CITED_RANGE_PLUS_MODEL_ASSUMPTION_FIT_ONLY` |
| `PAR-LCO-THERMAL` | transition-specific config/vib/electronic baselines | `TIER_C_INITIAL_OR_UNVERIFIED_PENDING_ROUNDTRIP` |

## 7. 구조적 식별성

- `ID-HS`: 관측 조합 `-DeltaH+T DeltaS`; 분리 미확정 `DeltaH, DeltaS`; 필요 근거: three or more calibrated temperatures or independent calorimetry.
- `ID-HYS`: 관측 조합 `gamma*h_eta*DeltaU_hys(Omega,T)`; 분리 미확정 `gamma, h_eta, Omega`; 필요 근거: full-cycle and partial-cycle bidirectional data over temperature.
- `ID-LAG`: 관측 조합 `L_V=|dV/dq|*(|I|/Qcell)/k`; 분리 미확정 `dH_a, dS_a, chi, Omega, dVdq`; 필요 근거: multi-rate, multi-temperature and independent OCV slope.
- `ID-CAP`: 관측 조합 `Q_j/Q_total with Q_bg offset`; 분리 미확정 `Q_j absolute scale, Q_bg integration constant, xbar offset`; 필요 근거: absolute capacity and reference composition.
- `ID-WIDTH`: 관측 조합 `observed width from intrinsic+lag+ensemble`; 분리 미확정 `n or w, L_V, ensemble rho(U)`; 필요 근거: multi-rate and multi-temperature ensemble-resolved data.
- `ID-LCO-GATE`: 관측 조합 `gmax/delta_x at the gate center`; 분리 미확정 `gmax, delta_x, x_MIT`; 필요 근거: independent endpoint DOS plus composition-resolved transition data.
- `ID-VIB-ELEC`: 관측 조합 `local temperature slope over two points`; 분리 미확정 `theta_E, electronic slope`; 필요 근거: at least three temperatures spanning useful curvature.

## 8. Findings

- `P060-PHY-P1-001` `P1`: The lag seed uses an h^-1 c-rate beside s^-1 Eyring kinetics without one canonical conversion; the two numeric readings differ by 3600. 처분: Step 45.1 CORRECT route; Phase 076 must freeze a timebase.
- `P060-PHY-P1-002` `P1`: C_bg defines dQ_bg/dV but no Q_bg primitive, reference charge, or inclusion in the composition residual is specified. 처분: Step 45.1 CORRECT route; Phase 074 must define the background charge state.
- `P060-PHY-P1-003` `P1`: The worked monotone bisection does not prove a unique root for admitted plateau, phase-separated, background, or history-dependent paths. 처분: Step 45.1 preserve as conditional; Phase 075/076 must close branch selection.
- `P060-PHY-P1-004` `P1`: The default thermal width is RT/F but the implementation derivative is zero, and the complete-expression input list omits n(T) or dw/dT. 처분: Step 45.1 CORRECT route; retain Step 43 MISALIGNED finding.
- `P060-PHY-P1-005` `P1`: The static monotone convolution has no explicit state for rest, finite-window initialization, or mid-protocol reversal. 처분: Step 45.1 CORRECT/NEW_SCOPE route; Phase 076 state equation.
- `P060-PHY-P1-006` `P1`: The source's LCO electronic entropy requires x,V,T dependence and T-squared center curvature, whereas the reachable path freezes x_center and 298.15 K. 처분: Step 45.1 CORRECT route; Phase 078 evidence-gated LCO closure.
- `P060-PHY-P1-007` `P1`: The reversible charge/discharge branch-average path is absent and the source identity is exact only to linear order in a small hysteresis gap. 처분: Step 45.1 THEORY_ONLY/CORRECT route; Phase 081 heat closure.
- `P060-PHY-P1-008` `P1`: Ch1 half-cell discharge and Bernardi cell discharge are opposite graphite reaction directions; electrode/full-cell heat signs need an explicit map. 처분: Step 45.1 preserve as sign blocker; Phase 074/081.
- `P060-PHY-P1-009` `P1`: Transition-specific Graphite kinetic/interaction numbers and continuous LCO gate parameters lack primary-source authority or are explicitly fit-only. 처분: Keep UNVERIFIED; Phase 071/072 authority and data gates.
- `P060-PHY-P1-010` `P1`: The three broadening mechanisms are not closed by a forward ensemble calculator or identifiable inverse law. 처분: Step 45.1 THEORY_ONLY/NEW_SCOPE; Phase 077/081.
- `P060-PHY-P1-011` `P1`: The source uses dQ/dV for both the signed derivative of a progress-increasing charge coordinate and its positive ICA magnitude, which disagree on charge. 처분: Step 45.1 CORRECT route; freeze separate signed-derivative and positive-magnitude observables.
- `P060-PHY-P1-012` `P1`: The source says nonzero hysteresis survives I->0 in one section but declares the zero-current baseline direction-invariant in another without gamma->0. 처분: Step 45.1 source-conflict route; do not promote either baseline as canonical before resolution.
- `P060-PHY-P2-001` `P2`: Only gamma*h_eta*DeltaU_hys is observed in the branch shift; its factors are not separately identified. 처분: Identifiability carry-forward.
- `P060-PHY-P2-002` `P2`: A direct L_V bypass and the kinetic product cannot identify dH_a, dS_a, chi, Omega and dV/dq separately at one condition. 처분: Multi-rate/multi-temperature carry-forward.
- `P060-PHY-P2-003` `P2`: At one temperature, Delta H and Delta S enter the center only through -DeltaH+TDeltaS. 처분: Require multi-temperature center data.
- `P060-PHY-P2-004` `P2`: Capacity scaling and an unfixed background-charge offset can trade against composition normalization. 처분: Require an absolute charge/reference-state contract.
- `P060-PHY-P2-005` `P2`: Two temperatures constrain only a local slope; Einstein curvature and a linear electronic term need at least three informative temperatures. 처분: Phase 081 experimental design.
- `P060-PHY-P2-006` `P2`: At the LCO gate center, amplitude is proportional to gmax/delta_x; endpoint and width evidence are needed to separate them. 처분: Phase 071/072/078 carry-forward.
- `P060-PHY-P2-007` `P2`: ICA/DVA reciprocity is local and fails as a finite number when F_U approaches zero. 처분: Preserve singular-domain diagnostics.
- `P060-PHY-P2-008` `P2`: The source's complete synthesis lists w but consumes n or dw/dT, so arbitrary direct-width thermal behavior is under-specified. 처분: Correct the future input contract before adoption.

## 9. 판정 경계

- check 결과: PASS 5, FAIL 6, CONDITIONAL 9, UNVERIFIED 2, NOT_APPLICABLE 0.
- findings: P0 0, P1 12, P2 8.
- Step 44 gate는 감사 coverage와 독립 재유도 완료를 뜻하는 `PASS_WITH_CONCERNS`다. FAIL/CONDITIONAL/UNVERIFIED row를 수리·외부 검증 완료로 승격하지 않는다.
- 다음 단위는 Step 45.1 claim/defect/carry-forward disposition이다.
