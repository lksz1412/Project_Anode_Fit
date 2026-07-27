# v1.0.25.2 Physics--Implementation Conformance Matrix

## Scope

이 문서는 물리 정본과 구현의 대응을 기록하는 허용된 implementation
ledger다. manuscript 본문에는 이 표의 symbol, file, test, version 정보를
옮기지 않는다.

Status:

- `CONFORMING`: 물리식과 구현 및 검증이 일치
- `PARTIAL`: 제한된 범위에서만 일치하거나 검증이 불완전
- `DIVERGENT`: 물리 계약과 구현이 다름
- `NOT IMPLEMENTED`: 문건에 있으나 구현 없음
- `EMPIRICAL ONLY`: 경험식으로만 유효
- `THEORY ONLY`: 구현 정본이 아닌 이론 대안

Frozen implementation source:

`Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py`
SHA-256
`eaa019f6a2f73d9274fbeea6211fa645d1e734ae98e490efbd473196f4a12746`.

## Matrix

| Physics ID | Physical statement | Validity domain | Implementation symbol/evidence | Test or invariant | Status | Required action |
|---|---|---|---|---|---|---|
| PHY-001 | 하나의 고정 state orientation, signed storage coefficient \(a_j\), dataset-level observation sign | charge/discharge trajectory and signed/magnitude ICA | `dqdv(..., s)` uses branch sign in `func_dxi_eq`; lines 721--753, 789--803; positive profile \(Q\) does not encode signed chemical storage | same-state reversal and observation-sign round trip absent | `DIVERGENT` | branch마다 logistic orientation을 뒤집는 현 계약을 고정-state trajectory로 재설계; \(a_j,s_j,\epsilon_{\rm obs}\)를 분리하고 magnitude preprocessing은 sign inference에 사용 금지 |
| PHY-002 | \(V_{\rm app},V_n,V_{\rm drive},V_{\rm eq}\) 분리 | polarized curve | `V_n=V_app-sigma_d I Rn`, lines 742--743; no independent drive state | zero-R limit; candidate affinity audit | `PARTIAL` | drive potential이 별도이면 명시 입력/식으로 분리; 아니면 \(V_{\rm drive}=V_n\) 적용범위 선언 |
| PHY-003 | monotonic curve와 time trajectory 분리 | causal memory | 현 API는 trajectory solver가 아니라 direction-based `np.argsort`를 쓰는 curve API, lines 746--756 | nonmonotonic input rejection/history test absent | `PARTIAL` | curve는 strict monotonic validation; 별도 trajectory API는 acquisition order 보존 |
| PHY-004 | measurement baseline, signed chemical storage와 observation sign/magnitude map 분리 | equilibrium/observation | `Cbg` is directly added, lines 758--762 and 853--855; archived preprocessing takes a positive magnitude profile | background area and units only; no signed-capacity round trip | `PARTIAL` | 이름/문건에서 observation baseline로 제한하거나 chemical state/free energy 추가; dataset sign transform을 provenance로 저장 |
| PHY-005 | \(z_j\)와 width 독립 | all electrochemical transitions | no explicit reaction \(z_j\); code documents `n`/`w` as width multiplicity rather than electron count, lines 491--546 | no stoichiometry invariant | `PARTIAL` | reaction stoichiometry를 별도 immutable field로 추가; candidate manuscript의 width-derived electron number 금지 |
| PHY-006 | ideal logistic is bounded thermodynamic baseline | independent-site, \(\alpha=1\) | `func_ksi_eq`, lines 145--148 | finite output but runtime warnings | `PARTIAL` | stable indexed evaluation; effective-\(w\) profile은 thermodynamic ideal profile과 분리 |
| PHY-007 | skew derivative is positive empirical area-preserving profile with \(A_j\ge0\), distinct from signed \(a_j\) | static magnitude/observation curve representation only | `func_dxi_eq`, lines 151--172 implements the area-preserving formula, but the same cumulative shape is reused by physical-state paths | G-alpha2 area and G-alpha3 smoothness PASS; direct formula max diff \(1.42\times10^{-14}\) | `PARTIAL` | dedicated empirical profile로 격리; cumulative shape를 chemical state/entropy로 재사용하거나 positive area에서 reaction orientation을 추론하지 않기 |
| PHY-008 | regular solution is theory/reference until solver adoption | nonideal equilibrium | production equilibrium comments explicitly use logistic single kernel, lines 685--696 | no production regular-solution branch | `THEORY ONLY` | manuscript에서 adopted kernel처럼 쓰지 않기; 별도 solver 전까지 theory module |
| PHY-009 | thermodynamic width, static broadening, lag separate | temperature/rate series | `w`/`n`, `alpha`, `L_V` are separate inputs; warning for alpha+L_V, lines 455--468 | only pairwise degeneracy warning tested | `PARTIAL` | `w`의 thermodynamic vs frozen-empirical profile을 type-level로 구분 |
| PHY-010 | charge balance is primary coupling | implicit OCV | `solve_U_oc`, lines 987--1072; blend pooled balance, lines 1674--1680; \(\alpha\ne1\) empirical cumulative shape is reused as physical capacity state | legacy round trip and blend capacity tests PASS | `PARTIAL` | background chemical storage가 빠져 있음을 명시; physical state와 empirical cumulative profile 분리; empirical 14 fit에는 이 해석을 소급하지 않기 |
| PHY-011 | inverse denominator failure is model inadmissibility | monotonic inverse | no direct implementation of Codex candidate denominator | no test | `NOT IMPLEMENTED` | 새 EOS에서 sign/admissibility gate로 구현; data deletion로 처리 금지 |
| PHY-012 | physical host blend와 generic 14-fit 분리 | blend | `BlendedAnodeDQDV` rescales Si by \(f_{\rm Si}\), lines 1648--1680; accepted fit builds one generic 14-list; finite-rate path sends the same external \(I/Q\) to both hosts | 두 경로는 구조적으로 별개이나 accepted empirical preset 없음; same blend data에서 default 7+7의 \(f_{\rm Si}\)와 code `Cbg` observation baseline만 재적합하면 \(R^2=-1.6132\), stored direct14는 0.9996494; 목적함수가 달라 우열 비교는 아님; \(f_{\rm Si}=0\) and capacity bookkeeping gates PASS | `PARTIAL` | `EmpiricalSkewProfile`와 `PhysicalHostBlend`를 명시적 profile로 노출; additive finite-rate path는 explicit approximation opt-in; raw-capacity normalization basis 명시 |
| PHY-013 | material closures remain modules | graphite/LCO/Si | host composition and LCO subclass exist | material evidence not verified by generic gates | `PARTIAL` | common core와 material module 경계를 새 manuscript 및 code layout에서 고정 |
| PHY-014 | rate sum controls mobility, ratio controls target | kinetic model | production uses one relaxation length rather than explicit \(J^+=r^+(1-\xi)\), \(J^-=r^-\xi\) | Level-A curve only | `NOT IMPLEMENTED` | Chapter 3 Level-B는 theory until forward/backward implementation; state-dependent rates use implicit stationary root |
| PHY-015 | \(k_0=(k_BT/h)\kappa(T)\) | Eyring interpretation | `func_L_q` effectively fixes transmission factor through formula, lines 177--193 | no independent \(\kappa\) test | `PARTIAL` | \(\kappa\)를 입력/unknown nuisance로 명시; activation entropy identifiability 제한 |
| PHY-016 | physical Eyring rate uses \({\rm s}^{-1}\) | physical profile | `curve` accepts \(1/{\rm h}\), lines 858--888, then SI \(h/k_B\) is used; lines 183--186 wrongly frame the correction as enthalpy-only | same physical rate produces L-ratio 3600; exact fixed-\(\Delta H_a\) intercept shift is \(\Delta S_a^{phys}-\Delta S_a^{legacy}=-R\ln3600=-68.081\) J mol\(^{-1}\) K\(^{-1}\); 20.298 kJ/mol is 298.15 K apparent offset only if \(\Delta S_a\) is fixed | `DIVERGENT` | SI profile에서 `/3600`; current behavior는 named legacy compatibility profile; 다온도 fit은 entropy/intercept convention으로 기록 |
| PHY-017 | causal memory needs explicit prehistory/initial state | monotonic single branch | `_causal_pad`, lines 196--227; five-\(L\) approximation | G-window PASS; residual \(e^{-5}=0.0067379\); duplicate first step gives zero pad | `PARTIAL` | finite tolerance 문구, supplied initial state/prehistory API, duplicate-step validation |
| PHY-018 | normalized spectrum and residual amplitude separate | distributed relaxation | no production distribution; Codex Chapter 1 candidate mixes roles | no normalization test | `NOT IMPLEMENTED` | 새 spectrum interface 전에 measure/amplitude notation부터 수정 |
| PHY-019 | fixed-state, fixed-charge, path derivatives distinct | temperature | `entropy_coefficient_x` uses implicit OCV; `dqdv` accepts \(T(V)\) but uses mean \(T\) for selected effects | fixed-\(x\) FD PASS only on legacy transitions | `PARTIAL` | fixed-\(q\) equilibrium path와 trajectory \(T(t)\) solver 분리 |
| PHY-020 | \(U=-\Delta_rG/(zF)\), same-forward-reaction \(I=zF\dot n>0\), generation-positive reversible heat is \(-IT U_T\) | declared reaction/current/control-volume convention | `reversible_heat`, lines 973--984; `reversible_heat_x`, lines 1103--1114 | same-implementation \(+60.8\) mV display regression PASS; independent reaction-sign/energy round trip 없음 | `PARTIAL` | written reaction→\(U,I,\Delta S,\dot Q\) 독립 test 후에만 현 코드 부호 보존 판정; candidate의 `+IT U_T` 수정; control-volume scope 추가 |
| PHY-021 | OCV/transition entropy bases need full closure | equilibrium temperature derivative | weighted `entropy_coefficient`, lines 902--971 reuses \(\alpha\ne1\) empirical cumulative shape in a thermodynamic derivative | selected legacy FD round trip PASS | `PARTIAL` | keyless/default 수정; state-dependent config term 재유도; empirical \(\alpha\)는 entropy path에서 제거 unless independently derived |
| PHY-022 | irreversible production is local flux times conjugate affinity; terminal lumping is bounded | local network or one-path terminal polarization | `irreversible_heat`, lines 1116--1124 implements \(I(U_{\rm oc}-V)\) with no sign/domain guard; no local network production | no \(I(U_{\rm oc}-V)\ge0\) guard, rest/internal-relaxation test or nonnegative network test | `PARTIAL` | terminal formula는 signed one-path domain으로 제한; rest/hidden storage와 double count 금지; local law는 explicit \(J^\pm\), \(Q^{SI}\)[C], positive-flux domain과 \(z\)로 구현 |
| PHY-023 | relaxation heat double counting 금지 | rest/thermal model | no integrated energy balance | no energy-closure test | `NOT IMPLEMENTED` | integrated EOS/DAE에서 reversible/stored/dissipated energy closure 추가 |
| PHY-024 | rejected thermal-tail mirror must not enter production | thermal relaxation | rejected candidate formula is absent from production code | absence check | `CONFORMING` | 현 부재 보존; fresh energy/power derivation과 acceptance gate 전에는 구현 금지 |
| PHY-025 | hysteresis belongs to landscape/target/mobility, not state reversal | branch model | center shift from `Omega,gamma`; direction also flips logistic | branch thermodynamic-cycle test absent | `DIVERGENT` | fixed state orientation + branch free energy/target state로 재작성 |
| PHY-026 | local vs global detailed balance distinct | metastable branch | no explicit Level-B detailed balance model | none | `NOT IMPLEMENTED` | terminology and tests added with forward/backward model |
| PHY-027 | loop area is loss only for closed state cycle | cyclic data | no cycle-state closure | none | `NOT IMPLEMENTED` | cycle endpoint/internal-state and side-reaction guards |
| PHY-028 | surviving stored-8dp empirical reference and production entry point are distinct | accepted blend-labeled data/window, protocol unknown | external stored-8dp vector/hashes exist; builder rounded `best` and omitted `pred`; no dedicated production preset | stored-8dp reconstruction \(R^2=0.9996494179\); original optimizer reproduction unavailable | `PARTIAL` | preserve external empirical reference and provenance gap; add dedicated entry point separately; future fits persist full optimizer state |
| PHY-029 | fit success does not assign mechanism | all fits | generic `GraphiteAnodeDischargeDQDV` can consume the stored 14-component list | fit metric only | `EMPIRICAL ONLY` | UI/docs label as generic empirical blend fit; no host/phase inference |
| PHY-030 | evidence grades travel with parameters | all materials | lines 1372--1388 call graphite7 opt-in/alpha-absent/5-of-7 upper-bound hits, while lines 1393--1399 contain alpha, lines 1431--1432 make 7+7 default, and stored-8dp graphite has no value exactly equal to the alpha upper bound; original active-set status is unavailable | no machine-readable provenance gate | `DIVERGENT` | profile schema에 source/evidence/identified/boundary-proximity/active-set-evidence fields 추가; designated implementation table을 artifact에서 생성 |
| PHY-031 | manuscript body physics-only; code 언급은 지정 section에만 허용 | manuscript | current release에는 지정 code appendix가 있고, 후보 본문 일부에는 symbol/workflow가 누출됨 | forbidden-term gate scans a much narrower phrase set | `PARTIAL` | 지정 implementation appendix 경계는 보존; file/commit/test/work-log는 외부 ledger로 두고 physics body 누출만 차단 |
| PHY-032 | every behavior traces to physics ID | implementation governance | no stable physics-ID mapping | present document is first matrix | `PARTIAL` | repairs and tests reference PHY IDs |

## Confirmed concrete defects

### C-001 — Eager stable-logistic branch

Evidence:

- source lines 145--148
- current-source probe produced two overflow warnings and one invalid-divide
  warning on nominal gallery inputs

Repair:

- allocate output
- evaluate \(z\ge0\) and \(z<0\) slices separately
- add scalar/array and warnings-as-errors tests

Acceptance:

- finite output
- no runtime warning for finite valid inputs
- numerical equivalence within a declared tolerance

### C-002 — Keyless width derivative mismatch

Evidence:

- `_n_factor` default 1, lines 491--511
- `_width` therefore \(RT/F\), lines 523--531
- `_dwdT` returns zero whenever `n` is absent, lines 534--546

Probe at 298.15 K:

- finite-difference \(dw/dT=8.61688345\times10^{-5}\) V/K
- reported \(dw/dT=0\)
- fixed-\(x\) \(dU_{\rm oc}/dT=-9.46661405\times10^{-5}\) V/K
- reported entropy coefficient \(=0\)

Repair decision:

- no-key profile must choose one contract:
  thermal ideal (`n=1`, nonzero derivative) or frozen empirical (`w=w_ref`,
  zero derivative)
- implicit mixed contract is forbidden

### C-003 — Accepted fitted observation baselines are not consumed

Evidence:

- declared values at lines 1433--1435
- constructor default `Cbg=0.0`, lines 1601--1605
- hosts receive only caller `Cbg`, lines 1668--1672

Repair:

- empirical profiles own their fitted observation baseline explicitly
- physical host blend requires an explicit electrode observation-baseline
  contract distinct from chemical background storage
- do not silently sum graphite and Si standalone fitted observation baselines

### C-004 — Invalid `si_case` accepted on current default path

Evidence:

- validation occurs only in the `DEFAULT_SI_TRANSITIONS is None` branch,
  lines 1617--1626
- probe accepted `not-a-real-case`

Repair:

- either remove `si_case` when an explicit/default profile makes it irrelevant,
  or validate it unconditionally when supplied

### C-005 — Nonfinite lag becomes equilibrium silently

Evidence:

- `_resolve_lag_length`, lines 661--664, maps nonfinite \(L_q\) to 0
- `dqdv`, lines 820--827, maps nonfinite/zero/unresolved length to equilibrium

Repair:

- evaluate \(L_q\) in log domain
- distinguish physical \(L\to0\), grid-unresolved \(L\), overflow \(L\to\infty\),
  and invalid parameter
- fail or warn explicitly according to a named profile

### C-006 — Mutable global transition and physical-constant profiles

Evidence:

- `use_legacy_4transition`, lines 1438--1450, mutates module defaults
- future transition instances depend on process-global call order
- an existing instance keeps its own transition list and corresponding
  `seed_L_V`; that transition toggle alone does not demonstrate a
  within-instance stale mismatch
- `use_si_constants`, lines 103--124, rebinds module-global \(R,F\)
- existing instances then use the new globals while their cached `seed_L_V`
  remains based on the old constants, as source line 108 acknowledges

Repair:

- immutable transition and physical-constant profile objects or explicit
  constructor presets
- tests must not modify process-global defaults
- add old-instance/new-instance invariants across profile selection

### C-007 — Stale inline profile/default contract

Evidence:

- source lines 1372--1388 say graphite7 is opt-in, legacy4 default is
  unchanged, and alpha keys are absent
- lines 1393--1399 contain alpha keys
- lines 1431--1432 set graphite7+Si7 as the module defaults
- the “5 of 7 alpha upper-bound hits” comment conflicts with the stored-8dp
  graphite maximum 7.99623012 and zero stored values exactly equal to the
  upper bound; original optimizer active-set status is unavailable

Repair:

- remove duplicated narrative state from inline comments
- generate the designated implementation profile table from one immutable,
  machine-readable profile artifact
- test default identity and separately record stored boundary proximity and
  optimizer active-set evidence

### C-008 — Lumped irreversible heat has no sign/domain contract

Evidence:

- `irreversible_heat`, lines 1116--1124, returns
  \(I(U_{\rm oc}-V)\)
- the docstring asserts nonnegativity, but the function does not validate the
  signed current/potential convention or resulting sign
- the API does not state that rest internal relaxation and hidden state-energy
  storage are outside the terminal lumped path

Repair:

- bind the formula to a written forward reaction/current convention
- reject or diagnose \(I(U_{\rm oc}-V)<0\) in the claimed dissipative domain
- keep terminal lumping, local network production and rest relaxation as
  separate, non-double-counted sources in an integrated energy balance

## Existing tests: coverage judgment

| Test | Observed result | Scientific reach |
|---|---|---|
| `test_gates_v1025.py` | 9/9 PASS | skew compatibility, area, smoothness, selected window behavior |
| `test_gates_v1024.py` | PASS | legacy 4-transition regression and selected blend invariants |
| Phase 044 probe | deterministic match | current defaults, thermodynamic round trip, rate units, causal edge, stored empirical-profile reconstruction |

Missing production-default gates:

- exact current default construction without legacy toggle
- current default backgrounds
- current default 7+7 curve snapshot
- accepted empirical profile entry point
- invalid case fail-fast
- keyless and explicit-\(w\) temperature round trip
- warnings-as-errors
- strict monotonic branch validation
- time-ordered reversal/rest trajectory
- per-point \(T\) versus local-constant approximation

## Repair order

1. Freeze the surviving stored-8dp empirical reference, then add its direct
   entry point.
2. Introduce explicit `empirical`, `physical-host`, and `legacy-compatible`
   profiles.
3. Fix stable logistic, parameter validation and background wiring.
4. Fix width-temperature contracts and SI rate units.
5. Split monotonic curve and trajectory APIs.
6. Implement integrated EOS/energy balance only after Chapter 2--5 physics
   corrections.

No production code is modified until these rows are accepted in the physics
ledger and manuscript architecture is fixed.
