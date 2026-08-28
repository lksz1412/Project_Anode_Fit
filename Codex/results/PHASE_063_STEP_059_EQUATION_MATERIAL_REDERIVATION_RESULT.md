# Phase 063 Step 059 — v1.0.22 Equation/Material Rederivation Result

상태: `PASS_WITH_CONCERNS`

Precommit Gate: `PASS_P063_STEP59_EQUATION_MATERIAL_REDERIVATION_WITH_CONCERNS`

Postcommit terminal: `PENDING_AT_PRECOMMIT_BY_DESIGN`

Gate 의미: 내부 수식·가정·부호·차원·극한·material scope의 재유도와 correction routing 완료. External truth 또는 canonical adoption PASS가 아니다.

정본일: 2026-08-29

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

예정 parent: `2ccee1af3a59a3a1e5c9fe7192e4f916c454521a`

## 1. 목적과 권위 경계

Step 59는 frozen v1.0.22에 나타나는 열역학·통계역학·재료·유한전류·열 수식을 독립 재유도하여 model layer, 가정, 차원, 부호, 극한과 material scope를 판정한다. 이 단계는 source 내부 식의 대수·수치·논리 경계만 확립하며 external scientific/material/experimental truth, primary-literature truth, canonical equation 채택, 실제 code/runtime conformance 또는 final manuscript readiness를 승인하지 않는다.

외부 원문 권위가 필요한 claim은 Step 60과 Phase 071로 `UNVERIFIED_EXTERNAL` 또는 `GROUND_NOT_FOUND` 상태를 유지한 채 전달한다. Frozen `Claude/**`는 수정하지 않는다.

## 2. 복구와 진입 조건

- master plan `1–665`와 Phase 063 detailed plan `1–681`을 현재 HEAD에서 전문 재독했다.
- 직전 Step 58 result, 두 execution ledger와 active handover를 현재본 기준으로 재확인했다.
- Step 58 exact-eight commit `2ccee1af3a59a3a1e5c9fe7192e4f916c454521a`은 local HEAD/upstream/live origin과 일치한다.
- Python 3.12/3.14 `PASS_P063_STEP58_PERSISTENCE`, negative `47/47`, determinism `2/2`를 확인했다.
- protected branch `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`, main `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`, `Claude/**` diff 0을 확인했다.

## 3. 계획 범위

### Task 59A — thermodynamic/statistical-mechanical layers

- independent-site grand partition, logistic, susceptibility와 fluctuation identity.
- regular-solution free energy, implicit response, spinodal/binodal/Maxwell와 metastability.
- equilibrium peak, observation convolution, empirical line shape와 finite-current memory의 operator 분리.
- TST partition ratio, prefactor, activation enthalpy/entropy/heat capacity와 temperature derivative.

### Task 59B — graphite/LCO/Si/blend material equations

- terminal/electrode/host potential, lithiation direction, composition coordinate의 공통 sign ledger.
- common-potential blend charge balance, sufficient unique-root 조건, host-specific capacity sum.
- external Si mass fraction에서 active/capacity fraction으로의 Faraday/capacity-basis 변환.
- Larché–Cahn stress–potential shift의 부호·차원과 plastic/path-history closure 부재.
- LCO local electronic/order/free-energy closure와 frozen global electronic entropy offset의 구분.

### Task 59C — finite-current and thermal checks

- C-rate `h^-1`→`s^-1`, lag scale 3,600배와 `RT ln 3600` barrier shift.
- arbitrary cut/cap/frozen-local approximation과 full local kinetics의 구분.
- configurational/vibrational/electronic entropy, reversible heat, hysteretic dissipation와 temperature-dependent width의 분리.
- symbolic, finite-difference, dimensional, limiting-case와 named mutation controls.

## 4. Exact-seven 산출물

1. `Codex/work/v1022_phase063/build_phase063_step59_equation_material_rederivation.py`.
2. `Codex/work/v1022_phase063/validate_phase063_step59.py`.
3. `Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json`.
4. 이 result.
5. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`.
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`.
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`.

예정 subject: `audit(phase063): rederive v1022 equation material`

## 5. 독립 재유도 evidence

<!-- P063_STEP59_DERIVATION_EVIDENCE_BEGIN -->
```json
{
  "evidence_id": "P063-STEP59-INDEPENDENT-REDERIVATION",
  "evidence_date": "2026-08-29",
  "external_truth_state": "UNVERIFIED_EXTERNAL",
  "authority_ceiling": "INTERNAL_DERIVATION_ONLY",
  "negative_claim_guards": {
    "independent_site_not_mean_field": true,
    "spinodal_not_binodal": true,
    "equilibrium_not_observation": true,
    "common_potential_not_equal_current": true,
    "mass_fraction_not_capacity_fraction": true,
    "larche_cahn_reversible_not_hysteresis_closure": true,
    "lco_global_offset_not_local_closure": true,
    "c_rate_requires_divide_3600": true,
    "tst_temperature_derivatives_retained": true,
    "reversible_heat_not_hysteretic_dissipation": true
  },
  "derivation_rows": [
    {
      "derivation_id": "P063-DER-001",
      "topic": "independent-site grand partition and logistic occupancy",
      "formula": "Xi=product_j[1+exp(-(epsilon_j-mu)/(RT))]^M_j; theta_j=[1+exp((epsilon_j-mu)/(RT))]^-1",
      "assumptions": ["finite positive T", "hard-core one-particle sites", "independent classes", "common molar chemical potential"],
      "dimensions": "epsilon, mu and RT are J/mol; exponent is dimensionless",
      "limits": "T->0 gives a step away from degeneracy; T->infinity gives half occupancy for finite energy difference",
      "disposition": "PRESERVE_CONDITIONAL",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Step 60 external authority; Phase 075 canonical equation",
      "source_evidence": [{"source_id":"P063-SRC-0009","path":"Claude/docs/v1.0.22/_sections/ch1_sec02a_part0.tex","git_blob":"98dbb903773340600c4d72d8c680d35328147157","line_intervals":[[73,81],[126,155]]}]
    },
    {
      "derivation_id": "P063-DER-002",
      "topic": "fluctuation response and strictness",
      "formula": "d<N>/dmu=Var(N)/(RT); independent sites give Var(N)=sum_j M_j theta_j(1-theta_j)",
      "assumptions": ["equilibrium differentiation", "independent-site variance sum only in the independent layer"],
      "dimensions": "molar-energy response has units mol/J in the normalized counting convention",
      "limits": "strict response requires positive weighted variance; root existence separately requires the target in the endpoint image",
      "disposition": "PRESERVE_CONDITIONAL",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 075",
      "source_evidence": [{"source_id":"P063-SRC-0009","path":"Claude/docs/v1.0.22/_sections/ch1_sec02a_part0.tex","git_blob":"98dbb903773340600c4d72d8c680d35328147157","line_intervals":[[305,314]]},{"source_id":"P063-SRC-0010","path":"Claude/docs/v1.0.22/_sections/ch1_sec02b_part0.tex","git_blob":"e9c17ce0e2b23e85843f70bfc8e6132e5154ae69","line_intervals":[[301,376]]}]
    },
    {
      "derivation_id": "P063-DER-003",
      "topic": "self-consistent regular-solution response",
      "formula": "d xi/dD=xi(1-xi)/[RT-2 Omega xi(1-xi)]",
      "assumptions": ["scalar symmetric regular solution", "locally selected branch"],
      "dimensions": "D, RT and Omega are J/mol; response is mol/J",
      "limits": "diverges at the spinodal and changes sign on the unstable branch; it is not the independent Bernoulli response",
      "disposition": "CORRECT",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 075/082",
      "source_evidence": [{"source_id":"P063-SRC-0010","path":"Claude/docs/v1.0.22/_sections/ch1_sec02b_part0.tex","git_blob":"e9c17ce0e2b23e85843f70bfc8e6132e5154ae69","line_intervals":[[211,216],[301,316]]}]
    },
    {
      "derivation_id": "P063-DER-004",
      "topic": "regular-solution spinodal",
      "formula": "g=RT[x ln x+(1-x)ln(1-x)]+Omega x(1-x); x_s=(1+-sqrt(1-2RT/Omega))/2",
      "assumptions": ["symmetric scalar regular solution", "Omega>2RT for two real spinodal roots"],
      "dimensions": "g and Omega are J/mol",
      "limits": "critical point is Omega=2RT at x=1/2",
      "disposition": "PRESERVE",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 075/078",
      "source_evidence": [{"source_id":"P063-SRC-0012","path":"Claude/docs/v1.0.22/_sections/ch1_sec04_hys.tex","git_blob":"9113881f850be737938f9b36aebfc95dd5731d48","line_intervals":[[25,39]]}]
    },
    {
      "derivation_id": "P063-DER-005",
      "topic": "binodal, common tangent and Maxwell construction",
      "formula": "mu(x_b^-)=mu(x_b^+)=mu_star; [g(x_b^+)-g(x_b^-)]/(x_b^+-x_b^-)=mu_star; integral(mu-mu_star)dx=0",
      "assumptions": ["equilibrium coexistence", "convexification of the homogeneous free energy"],
      "dimensions": "chemical potential and common-tangent slope are J/mol",
      "limits": "binodal differs from spinodal; the intervening homogeneous branches are metastable",
      "disposition": "PRESERVE",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 075/082",
      "source_evidence": [{"source_id":"P063-SRC-0056","path":"Claude/docs/v1.0.22/appendix_phase_separation.tex","git_blob":"4e17bf01a5a1eb71476e6112d6a26b96861b17f5","line_intervals":[[169,278],[360,390]]}]
    },
    {
      "derivation_id": "P063-DER-006",
      "topic": "regular-solution demixing is not LCO superstructure ordering",
      "formula": "g_second(1/2)=4RT-2Omega<0 when Omega>2RT",
      "assumptions": ["single scalar composition coordinate"],
      "dimensions": "curvature is J/mol per squared composition",
      "limits": "the midpoint is a maximum, so an ordered x=1/2 minimum requires an additional sublattice/order parameter",
      "disposition": "REJECT",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 078/082",
      "source_evidence": [{"source_id":"P063-SRC-0033","path":"Claude/docs/v1.0.22/_sections/ch2_sec01_partition.tex","git_blob":"380388bdf75b8b6b5b19aa667efa221a945b8eb5","line_intervals":[[114,137]]},{"source_id":"P063-SRC-0021","path":"Claude/docs/v1.0.22/_sections/ch1_sec13_lcohys.tex","git_blob":"9eac9dc326aaea977867a7f263e8f7458543e34d","line_intervals":[[108,166]]}]
    },
    {
      "derivation_id": "P063-DER-007",
      "topic": "equilibrium logistic dQ/dV kernel",
      "formula": "d xi/dV=xi(1-xi)/w; ideal w=RT/F; peak=1/(4w); FWHM=4 acosh(sqrt(2)) w",
      "assumptions": ["equilibrium", "normalized full-domain response", "one-electron voltage coupling"],
      "dimensions": "kernel is 1/V and capacity-weighted response is C/V",
      "limits": "full-domain area is one before capacity weighting",
      "disposition": "PRESERVE_CONDITIONAL",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 075",
      "source_evidence": [{"source_id":"P063-SRC-0014","path":"Claude/docs/v1.0.22/_sections/ch1_sec06_eqpeak.tex","git_blob":"4f96ebdd20e80601086c4aa0ddb8c3a653a9095f","line_intervals":[[8,76]]}]
    },
    {
      "derivation_id": "P063-DER-008",
      "topic": "static observation convolution",
      "formula": "y_obs(V)=integral rho(U)y_eq(V-U)dU",
      "assumptions": ["normalized static kernel", "shift-invariant independent observation broadening"],
      "dimensions": "rho has reciprocal-voltage units",
      "limits": "variance adds only for normalized independent finite-variance kernels; FWHM quadrature is not general",
      "disposition": "PRESERVE_CONDITIONAL",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 075/082",
      "source_evidence": [{"source_id":"P063-SRC-0015","path":"Claude/docs/v1.0.22/_sections/ch1_sec07_broadening.tex","git_blob":"21ac77670f2d70540b77007ff9cc8008a7599e68","line_intervals":[[103,176]]}]
    },
    {
      "derivation_id": "P063-DER-009",
      "topic": "causal finite-current memory",
      "formula": "K_L(deltaV)=exp(-deltaV/L_V)/L_V for deltaV>=0; response=K_L convolved with equilibrium derivative",
      "assumptions": ["linear first-order relaxation", "constant frozen L_V per transition"],
      "dimensions": "K_L is 1/V and L_V is V",
      "limits": "L_V->0 recovers the equilibrium response; it is not a symmetric observation convolution",
      "disposition": "PRESERVE_CONDITIONAL",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 076",
      "source_evidence": [{"source_id":"P063-SRC-0017","path":"Claude/docs/v1.0.22/_sections/ch1_sec09_tail.tex","git_blob":"490139d35601c8d83da6d567bcdcf2ac97619d1c","line_intervals":[[10,65],[96,191]]}]
    },
    {
      "derivation_id": "P063-DER-010",
      "topic": "general transition-state rate",
      "formula": "k=kappa(k_B T/h)K_dagger exp[-DeltaE0/(RT)]",
      "assumptions": ["dimensionless standard-state partition ratio", "quasi-equilibrium transition state", "explicit transmission coefficient"],
      "dimensions": "k_B T/h is 1/s and all exponential arguments are dimensionless",
      "limits": "source is the kappa=1 classical separable special case; the one-sided flux moment must not be named a conditional positive-speed mean",
      "disposition": "CORRECT",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 076/082",
      "source_evidence": [{"source_id":"P063-SRC-0013","path":"Claude/docs/v1.0.22/_sections/ch1_sec05_width.tex","git_blob":"684bb74a2ffb811d128cbf667045e991915158a3","line_intervals":[[52,89]]}]
    },
    {
      "derivation_id": "P063-DER-011",
      "topic": "activation entropy, enthalpy and heat capacity",
      "formula": "DeltaS=-DeltaE0_prime+R L+RT L_prime; DeltaH=DeltaE0-T DeltaE0_prime+RT^2 L_prime; DeltaCp=-T DeltaE0_second+R(2T L_prime+T^2 L_second)",
      "assumptions": ["same standard-state energy zero", "differentiable DeltaE0(T) and L(T)=ln K_dagger(T)"],
      "dimensions": "DeltaS and DeltaCp are J/(mol K); DeltaH is J/mol",
      "limits": "DeltaS=R ln K_dagger only when both omitted derivative contributions vanish",
      "disposition": "CORRECT",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 076/082",
      "source_evidence": [{"source_id":"P063-SRC-0013","path":"Claude/docs/v1.0.22/_sections/ch1_sec05_width.tex","git_blob":"684bb74a2ffb811d128cbf667045e991915158a3","line_intervals":[[91,104]]}]
    },
    {
      "derivation_id": "P063-DER-012",
      "topic": "high-temperature TST limit",
      "formula": "K_dagger proportional to T^-1 cancels the explicit T in k_B T/h; K_dagger=1 leaves a T prefactor",
      "assumptions": ["classical harmonic high-temperature power counting"],
      "dimensions": "partition ratio is dimensionless",
      "limits": "K_dagger=1 is not constant-prefactor pure Arrhenius",
      "disposition": "CORRECT",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 076/082",
      "source_evidence": [{"source_id":"P063-SRC-0013","path":"Claude/docs/v1.0.22/_sections/ch1_sec05_width.tex","git_blob":"684bb74a2ffb811d128cbf667045e991915158a3","line_intervals":[[109,119]]}]
    },
    {
      "derivation_id": "P063-DER-013",
      "topic": "fixed delithiation coordinate and branch direction",
      "formula": "xi_del=1-theta increases with V; x_LCO=x_hi-(x_hi-x_lo)xi_del; a reverse-path progress coordinate must be separate",
      "assumptions": ["xi_del is a physical composition coordinate rather than path progress"],
      "dimensions": "all composition coordinates are dimensionless",
      "limits": "multiplying the equilibrium logistic argument by branch sign reverses composition on the charge branch",
      "disposition": "CORRECT",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 074/078/082",
      "source_evidence": [{"source_id":"P063-SRC-0008","path":"Claude/docs/v1.0.22/_sections/ch1_sec01_n0n1.tex","git_blob":"9648c33e724f4bb762924ff20ba775ec568d4bf0","line_intervals":[[24,35]]},{"source_id":"P063-SRC-0013","path":"Claude/docs/v1.0.22/_sections/ch1_sec05_width.tex","git_blob":"684bb74a2ffb811d128cbf667045e991915158a3","line_intervals":[[278,297]]},{"source_id":"P063-SRC-0025","path":"Claude/docs/v1.0.22/_sections/ch1_sec17_msmr.tex","git_blob":"90bc83050a0ea7f707e015a20cb441289d0d0e9c","line_intervals":[[120,127]]}]
    },
    {
      "derivation_id": "P063-DER-014",
      "topic": "common-potential blend charge balance",
      "formula": "G(U)=sum_hj Q_hj xi_hj(U,T)-Q xbar=0; Q=sum_hj Q_hj",
      "assumptions": ["equilibrium common electrochemical potential", "positive capacity weights", "continuous host responses"],
      "dimensions": "G and Q are C on a physical capacity basis",
      "limits": "unique root is sufficient under positive aggregate derivative and endpoint bracketing; common potential does not mean equal host current",
      "disposition": "PRESERVE_CONDITIONAL",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 075/080",
      "source_evidence": [{"source_id":"P063-SRC-0051","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec03_blend.tex","git_blob":"4966fa1ffbe31364b3b87ba387cd4d439cf658a5","line_intervals":[[17,114]]}]
    },
    {
      "derivation_id": "P063-DER-015",
      "topic": "mass fraction to reversible capacity fraction",
      "formula": "f_Si=m_Si q_Si u_Si/[m_Si q_Si u_Si+m_G q_G u_G]",
      "assumptions": ["same cycle and direction basis", "explicit active-mass denominator", "ICE or retention applied exactly once"],
      "dimensions": "mass times specific capacity yields capacity; f_Si is dimensionless",
      "limits": "1-m_Si equals graphite only on a two-active-material mass basis without binder, carbon or other active mass",
      "disposition": "CORRECT",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Step 60C; Phase 080; Step 61 from_wt contract",
      "source_evidence": [{"source_id":"P063-SRC-0047","path":"Claude/docs/v1.0.22/_sections/ch3v22_notation.tex","git_blob":"87aa209d66ec2a71b165a58d6e25819eeb7ba80a","line_intervals":[[24,36]]},{"source_id":"P063-SRC-0050","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex","git_blob":"ea88ed0730bb8cbc5f48cd3cacc42fab93f88ded","line_intervals":[[15,78]]},{"source_id":"P063-SRC-0051","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec03_blend.tex","git_blob":"4966fa1ffbe31364b3b87ba387cd4d439cf658a5","line_intervals":[[61,89],[209,222]]}]
    },
    {
      "derivation_id": "P063-DER-016",
      "topic": "Larché-Cahn stress-potential shift",
      "formula": "mu_host=mu0-vbar sigma_h; V=V0+(vbar/F)sigma_h",
      "assumptions": ["tension-positive hydrostatic stress", "positive insertion partial molar volume", "linear reversible coupling"],
      "dimensions": "vbar sigma is J/mol and vbar/F is V/Pa",
      "limits": "compression raises host chemical potential and lowers voltage in this convention",
      "disposition": "PRESERVE_CONDITIONAL",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 079",
      "source_evidence": [{"source_id":"P063-SRC-0052","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec04_mech.tex","git_blob":"b4c331374a7c03f5de26353cb0655e2c7c21f1dc","line_intervals":[[15,60]]}]
    },
    {
      "derivation_id": "P063-DER-017",
      "topic": "mechanical branch gap and missing history closure",
      "formula": "DeltaV_mech=(vbar/F)(sigma_dis-sigma_chg) only under constant-vbar same-state comparison",
      "assumptions": ["same composition and temperature", "branch stresses supplied by a separate constitutive model"],
      "dimensions": "DeltaV_mech is V",
      "limits": "single-valued reversible stress-composition coupling produces no closed-cycle hysteresis; plastic flow, hardening, damage and history are ground-not-found",
      "disposition": "UNRESOLVED",
      "external_support": "GROUND_NOT_FOUND",
      "owner": "Phase 079 and later material dynamics",
      "source_evidence": [{"source_id":"P063-SRC-0052","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec04_mech.tex","git_blob":"b4c331374a7c03f5de26353cb0655e2c7c21f1dc","line_intervals":[[49,105]]}]
    },
    {
      "derivation_id": "P063-DER-018",
      "topic": "finite-current blend host-current allocation",
      "formula": "i_graphite+i_Si=I_electrode with host-specific OCV, overpotential, exchange current, area, transport and state equations",
      "assumptions": ["finite-rate operation"],
      "dimensions": "all current terms use one declared A or normalized-rate basis",
      "limits": "equilibrium capacity-weighted response does not close host current partition or nonadditive local dynamics",
      "disposition": "UNRESOLVED",
      "external_support": "GROUND_NOT_FOUND",
      "owner": "Phase 080 and later material dynamics",
      "source_evidence": [{"source_id":"P063-SRC-0051","path":"Claude/docs/v1.0.22/_sections/ch3v22_sec03_blend.tex","git_blob":"4966fa1ffbe31364b3b87ba387cd4d439cf658a5","line_intervals":[[229,273]]}]
    },
    {
      "derivation_id": "P063-DER-019",
      "topic": "C-rate conversion and lag length",
      "formula": "nu_q=|I|/Q_cell=C_rate_per_hour/3600; L_q=nu_q/k; L_V=abs(dV/dq)L_q",
      "assumptions": ["k is in 1/s", "Q_cell and current share a physical or consistently normalized basis"],
      "dimensions": "nu_q and k are 1/s; L_q is dimensionless; L_V is V",
      "limits": "using the h^-1 numerical value directly makes lag 3600 times too large",
      "disposition": "CORRECT",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Step 61 static/runtime correction; Phase 076",
      "source_evidence": [{"source_id":"P063-SRC-0016","path":"Claude/docs/v1.0.22/_sections/ch1_sec08_lag.tex","git_blob":"52f175b0d769c7a8b932183ef454042a8c9c01eb","line_intervals":[[10,31],[99,140]]},{"source_id":"P063-SRC-0018","path":"Claude/docs/v1.0.22/_sections/ch1_sec10_sum.tex","git_blob":"10ab70e2e4a99cc72b122c75922bc178041b1923","line_intervals":[[54,59]]}]
    },
    {
      "derivation_id": "P063-DER-020",
      "topic": "equivalent barrier shift from the C-rate seam",
      "formula": "Delta barrier=RT ln(3600)=20.2994 kJ/mol at 298.15 K",
      "assumptions": ["Arrhenius dependence k=A exp(-barrier/RT)", "same observed lag and prefactor"],
      "dimensions": "RT ln(3600) is J/mol",
      "limits": "correcting to 1/s lowers fitted k by 3600 and therefore raises the inferred barrier by RT ln(3600)",
      "disposition": "CORRECT",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Step 61 runtime delta",
      "source_evidence": [{"source_id":"P063-SRC-0016","path":"Claude/docs/v1.0.22/_sections/ch1_sec08_lag.tex","git_blob":"52f175b0d769c7a8b932183ef454042a8c9c01eb","line_intervals":[[99,118]]},{"source_id":"P063-SRC-0018","path":"Claude/docs/v1.0.22/_sections/ch1_sec10_sum.tex","git_blob":"10ab70e2e4a99cc72b122c75922bc178041b1923","line_intervals":[[54,59]]}]
    },
    {
      "derivation_id": "P063-DER-021",
      "topic": "cut/cap control",
      "formula": "z_cut=2 acosh(p^-1/2); A=RT min(z_cut n,A_cap)",
      "assumptions": ["logistic derivative cut", "empirical finite cap"],
      "dimensions": "affinity is J/mol",
      "limits": "p=0.05 gives z_cut=4.35654, but A_cap=4 gives an effective derivative fraction sech(2)^2=0.07065",
      "disposition": "PRESERVE_CONDITIONAL",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 076",
      "source_evidence": [{"source_id":"P063-SRC-0016","path":"Claude/docs/v1.0.22/_sections/ch1_sec08_lag.tex","git_blob":"52f175b0d769c7a8b932183ef454042a8c9c01eb","line_intervals":[[37,54]]}]
    },
    {
      "derivation_id": "P063-DER-022",
      "topic": "frozen-local versus full local kinetics",
      "formula": "frozen model has partial_V ln L_q=0 per transition; full local model requires A_d(V,xi,state) and k(V,xi,T,state)",
      "assumptions": ["one frozen evaluation at the tail cut for the current model"],
      "dimensions": "log derivative is 1/V",
      "limits": "a finite-cut deep-tail substitution is a hybrid heuristic and cannot be promoted to full local kinetics",
      "disposition": "PRESERVE_CONDITIONAL",
      "external_support": "GROUND_NOT_FOUND",
      "owner": "Phase 076/080",
      "source_evidence": [{"source_id":"P063-SRC-0016","path":"Claude/docs/v1.0.22/_sections/ch1_sec08_lag.tex","git_blob":"52f175b0d769c7a8b932183ef454042a8c9c01eb","line_intervals":[[99,140]]}]
    },
    {
      "derivation_id": "P063-DER-023",
      "topic": "reversible and irreversible heat",
      "formula": "Qdot_rev=-I T dUoc/dT; Qdot_irr=I(Uoc-V)>=0 under the declared signed cell-current convention",
      "assumptions": ["I>0 cell discharge", "low-rate uniform concentration", "phase heat already represented in equilibrium Uoc where claimed"],
      "dimensions": "A times V is W",
      "limits": "half-cell charge/discharge labels must not replace signed cell current; high-rate mixing and spatial heat may require residual terms",
      "disposition": "PRESERVE_CONDITIONAL",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 074/077",
      "source_evidence": [{"source_id":"P063-SRC-0039","path":"Claude/docs/v1.0.22/_sections/ch2_sec07_revheat.tex","git_blob":"0bc5e966688c49428e4856c7b289b0038f830f67","line_intervals":[[10,25],[47,94]]}]
    },
    {
      "derivation_id": "P063-DER-024",
      "topic": "hysteretic dissipation and branch thermal derivative",
      "formula": "E_hys=closed_integral V dQ; branch dU/dT includes (sigma_d/2)d[h_eta gamma DeltaU_hys]/dT",
      "assumptions": ["same cycle coordinate and signed-current convention", "no double counting with terminal overpotential heat"],
      "dimensions": "closed V dQ integral is J; I times hysteretic overpotential is W",
      "limits": "I DeltaU_hys without an absolute-current or signed-overpotential convention can become negative on charge; constant-gap approximations are not general",
      "disposition": "CORRECT",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Phase 074/077/078",
      "source_evidence": [{"source_id":"P063-SRC-0021","path":"Claude/docs/v1.0.22/_sections/ch1_sec13_lcohys.tex","git_blob":"9eac9dc326aaea977867a7f263e8f7458543e34d","line_intervals":[[80,95]]},{"source_id":"P063-SRC-0037","path":"Claude/docs/v1.0.22/_sections/ch2_sec05_mixing.tex","git_blob":"b7d1650418c2734854378e0a1ca5cac8fc5790d3","line_intervals":[[196,227]]},{"source_id":"P063-SRC-0039","path":"Claude/docs/v1.0.22/_sections/ch2_sec07_revheat.tex","git_blob":"0bc5e966688c49428e4856c7b289b0038f830f67","line_intervals":[[16,22],[47,52]]}]
    },
    {
      "derivation_id": "P063-DER-025",
      "topic": "LCO local electronic closure versus frozen global offset",
      "formula": "local model DeltaS_e(x,T) and its T integral are distinct from a constant evaluated at x_MIT,T_ref and applied to the full T1 transition",
      "assumptions": ["model-layer identity is preserved"],
      "dimensions": "entropy is J/(mol K), integrated free-energy contribution is J/mol, voltage shift is V",
      "limits": "the frozen constant approximation cannot establish composition locality or T-squared curvature; the reported -91 mV effect changes under T_ref reanchoring",
      "disposition": "CORRECT",
      "external_support": "UNVERIFIED_EXTERNAL",
      "owner": "Step 60; Phase 078/082",
      "source_evidence": [{"source_id":"P063-SRC-0023","path":"Claude/docs/v1.0.22/_sections/ch1_sec15_lcoelec.tex","git_blob":"2a41d8aaf965b18131eea68e5a77d8b7f536f44a","line_intervals":[[113,265],[340,390]]},{"source_id":"P063-SRC-0025","path":"Claude/docs/v1.0.22/_sections/ch1_sec17_msmr.tex","git_blob":"90bc83050a0ea7f707e015a20cb441289d0d0e9c","line_intervals":[[120,159]]}]
    }
  ],
  "sign_ledger": [
    {"sign_id":"P063-SIGN-001","quantity":"V versus Li","definition":"mu_host-mu_metal=-F V","consequence":"higher V lowers host Li chemical potential","adjudicated":true},
    {"sign_id":"P063-SIGN-002","quantity":"theta and xi_del","definition":"theta is Li occupancy; xi_del=1-theta is fixed delithiation fraction","consequence":"xi_del increases with V independent of path direction","adjudicated":true},
    {"sign_id":"P063-SIGN-003","quantity":"LCO x","definition":"x=x_hi-(x_hi-x_lo)xi_del","consequence":"x decreases during delithiation","adjudicated":true},
    {"sign_id":"P063-SIGN-004","quantity":"sigma_d","definition":"+1 oxidation/delithiation path; -1 reduction/lithiation path","consequence":"branch label may shift centers but must not redefine physical composition","adjudicated":true},
    {"sign_id":"P063-SIGN-005","quantity":"Bernardi I","definition":"I>0 is cell discharge in the thermal balance","consequence":"it is a separate signed-current convention and is not sigma_d","adjudicated":true},
    {"sign_id":"P063-SIGN-006","quantity":"hydrostatic stress","definition":"tension positive; mu_host=mu0-vbar sigma_h","consequence":"compression with vbar>0 raises mu_host and lowers V","adjudicated":true}
  ],
  "operator_ledger": [
    {"operator_id":"P063-OP-001","name":"equilibrium free-energy response","input":"state,T,V","output":"theta,xi,Uoc,dQ/dV equilibrium","collapsed_with":[]},
    {"operator_id":"P063-OP-002","name":"phase convexification","input":"nonconvex homogeneous free energy","output":"binodal,common tangent,phase fraction","collapsed_with":[]},
    {"operator_id":"P063-OP-003","name":"static observation convolution","input":"equilibrium response and normalized static kernel","output":"symmetrically broadened observation","collapsed_with":[]},
    {"operator_id":"P063-OP-004","name":"empirical line shape","input":"fit parameters","output":"phenomenological response","collapsed_with":[]},
    {"operator_id":"P063-OP-005","name":"causal finite-current memory","input":"equilibrium response and directed relaxation kernel","output":"path-dependent lag/tail","collapsed_with":[]},
    {"operator_id":"P063-OP-006","name":"thermal and dissipative response","input":"dUeq/dT,signed current,terminal overpotential,path","output":"reversible heat plus nonnegative dissipation","collapsed_with":[]}
  ],
  "material_scope_ledger": [
    {"material_id":"P063-MAT-001","material":"graphite","claim":"independent logistic and regular-solution kernels are model layers, not complete staging microphysics","scope_state":"CONDITIONAL"},
    {"material_id":"P063-MAT-002","material":"LCO","claim":"scalar demixing does not derive x=1/2 ordered-superstructure stability","scope_state":"DERIVED_INTERNAL"},
    {"material_id":"P063-MAT-003","material":"LCO electronic","claim":"local electronic free energy and frozen T1-wide offset remain distinct approximations","scope_state":"CONDITIONAL"},
    {"material_id":"P063-MAT-004","material":"elemental Si, SiOx and Si-C","claim":"capacity, ICE, utilization, cycle and active-mass bases are not yet common","scope_state":"UNVERIFIED_EXTERNAL"},
    {"material_id":"P063-MAT-005","material":"Si mechanics","claim":"reversible stress shift exists but path-dependent plastic/damage closure is absent","scope_state":"GROUND_NOT_FOUND"},
    {"material_id":"P063-MAT-006","material":"graphite-Si blend","claim":"equilibrium common-potential balance exists but finite-current host allocation is absent","scope_state":"GROUND_NOT_FOUND"}
  ],
  "review_attestations": [
    {"review_id":"P063-REV-59A","role":"thermodynamic/statistical-mechanical independent rederivation","read_scope":"19 frozen TeX files, 4564 lines, each 1-EOF with blob identity; prior Step53 result 1-96 and JSON strict traversal 956 nodes","result":"PASS_WITH_CONCERNS","finding_summary":{"P0":0,"P1":4,"P2":4}},
    {"review_id":"P063-REV-59B","role":"graphite/LCO sign and material review","read_scope":"Ch1 sec00-18 and Ch2 sec00-10 relevant roots/appendix all 1-EOF; Phase057 R/S/T and Phase062 Step54 result/matrix","result":"FAIL_FINDINGS_ROUTED","finding_summary":{"P0":0,"P1":4,"P2":4}},
    {"review_id":"P063-REV-59BC","role":"Si/blend/mechanics/finite-current/thermal review","read_scope":"Ch3 root and sections, AppD, phase-separation appendix, lag/tail/sum/reversible heat all 1-EOF; four Phase057 observation documents 1-EOF; targeted static code spans only","result":"FAIL_FINDINGS_ROUTED","finding_summary":{"P0":4,"P1":5,"P2":2}}
  ],
  "findings": [
    {"finding_id":"P063-S59-F001","priority":"P0","status":"OPEN_ROUTED","summary":"C-rate h^-1 numerical value enters an s^-1 kinetic path without division by 3600, overstates lag by 3600 and shifts an equivalent fitted barrier by RT ln 3600.","owner":"Step 61 and Phase 076","external_truth_validated":false},
    {"finding_id":"P063-S59-F002","priority":"P0","status":"OPEN_ROUTED","summary":"Si mass-to-capacity conversion mixes theoretical, first-charge and reversible capacity bases and leaves active-mass/ICE/utilization semantics unresolved.","owner":"Step 60C, Step 61 and Phase 080","external_truth_validated":false},
    {"finding_id":"P063-S59-F003","priority":"P0","status":"OPEN_ROUTED","summary":"The reversible Larché-Cahn voltage shift is derived, but no path-dependent plastic/damage constitutive law closes Si hysteresis prediction.","owner":"Phase 079","external_truth_validated":false},
    {"finding_id":"P063-S59-F004","priority":"P0","status":"OPEN_ROUTED","summary":"The finite-current blend path does not solve host current partition, so equilibrium weighted addition cannot support a production finite-rate claim.","owner":"Phase 080 and later dynamics","external_truth_validated":false},
    {"finding_id":"P063-S59-F005","priority":"P1","status":"OPEN_ROUTED","summary":"The general activation-entropy expression omits temperature derivatives of the energy zero and transition-state partition ratio.","owner":"Phase 076/082","external_truth_validated":false},
    {"finding_id":"P063-S59-F006","priority":"P1","status":"OPEN_ROUTED","summary":"Independent-product and Bernoulli-response results are overextended to self-consistent mean field.","owner":"Phase 075/082","external_truth_validated":false},
    {"finding_id":"P063-S59-F007","priority":"P1","status":"OPEN_ROUTED","summary":"The one-sided Maxwell flux moment is mislabeled as the conditional positive-speed mean; the two differ by factor two.","owner":"Phase 076/082","external_truth_validated":false},
    {"finding_id":"P063-S59-F008","priority":"P1","status":"OPEN_ROUTED","summary":"K_dagger=1 is called pure Arrhenius even though the Eyring prefactor remains proportional to temperature.","owner":"Phase 076/082","external_truth_validated":false},
    {"finding_id":"P063-S59-F009","priority":"P1","status":"OPEN_ROUTED","summary":"A fixed delithiation composition coordinate is complemented on the reverse branch, reversing the LCO composition/MIT map.","owner":"Phase 074/078/082","external_truth_validated":false},
    {"finding_id":"P063-S59-F010","priority":"P1","status":"OPEN_ROUTED","summary":"Positive-Omega scalar regular-solution demixing is incorrectly promoted to stability of an x=1/2 ordered LCO superstructure.","owner":"Phase 078/082","external_truth_validated":false},
    {"finding_id":"P063-S59-F011","priority":"P1","status":"OPEN_ROUTED","summary":"The branch thermal coefficient omits the explicit temperature derivative of the hysteresis-gap term.","owner":"Phase 074/077/078","external_truth_validated":false},
    {"finding_id":"P063-S59-F012","priority":"P1","status":"OPEN_ROUTED","summary":"The LCO +0.83 mV/K and derived entropy retain an unresolved electrode/reaction basis and sign conflict.","owner":"Step 60 and Phase 071/074/078","external_truth_validated":false},
    {"finding_id":"P063-S59-F013","priority":"P2","status":"OPEN_ROUTED","summary":"Numerical constraint inversion is described as a Legendre transform without separating the thermodynamic potential transformation.","owner":"Phase 075/082","external_truth_validated":false},
    {"finding_id":"P063-S59-F014","priority":"P2","status":"OPEN_ROUTED","summary":"Capacity identities omit C versus Ah versus normalized basis and one load-bearing identity remains an unnumbered display.","owner":"Phase 074/082","external_truth_validated":false},
    {"finding_id":"P063-S59-F015","priority":"P2","status":"OPEN_ROUTED","summary":"The general TST row needs an explicit dimensionless standard state and transmission coefficient.","owner":"Phase 076/082","external_truth_validated":false},
    {"finding_id":"P063-S59-F016","priority":"P2","status":"OPEN_ROUTED","summary":"A signed I times positive hysteresis gap can imply negative dissipation on charge and risks double counting terminal overpotential heat.","owner":"Phase 074/077","external_truth_validated":false},
    {"finding_id":"P063-S59-F017","priority":"P2","status":"OPEN_ROUTED","summary":"The frozen T1-wide LCO electronic offset is not the local composition- and temperature-dependent electronic free-energy closure.","owner":"Phase 078/082","external_truth_validated":false},
    {"finding_id":"P063-S59-F018","priority":"P2","status":"OPEN_ROUTED","summary":"Strict temperature independence of configurational entropy at fixed composition is limited to the ideal independent-site layer.","owner":"Phase 075/078","external_truth_validated":false},
    {"finding_id":"P063-S59-F019","priority":"P2","status":"OPEN_ROUTED","summary":"The g(E_F)=13 LCO claim remains model-inferred rather than an externally verified direct endpoint.","owner":"Step 60 and Phase 078","external_truth_validated":false},
    {"finding_id":"P063-S59-F020","priority":"P2","status":"OPEN_ROUTED","summary":"The default affinity cap implements an approximately 7.07 percent derivative cut while nearby wording continues to call it a 5 percent cut.","owner":"Phase 076/082","external_truth_validated":false}
  ]
}
```
<!-- P063_STEP59_DERIVATION_EVIDENCE_END -->

## 6. 핵심 판정

### 6.1 전체 수식 분모와 model layer

- Step 58 topology의 네 root에서 도달하는 TeX `53`개를 frozen blob으로 다시 고정했다.
- 외부 display equation `231`개(`equation/align/...` 환경 `205`, bracket display `26`)를 source ID, blob, 1-based line interval, body SHA-256와 함께 전수 inventory한다.
- 독립 자리, self-consistent mean field, equilibrium two-phase convexification, static observation convolution, empirical line shape, causal finite-current memory, thermal/dissipative response를 서로 다른 operator로 유지했다.
- Phase 057의 관련 provisional finding `55`개는 원 record identity를 그대로 보존하고 `RETAINED_PROVISIONAL_NOT_PROMOTED`로 route한다.

### 6.2 P0 네 건

1. `C_rate [h^-1]` 숫자가 `k [s^-1]`와 결합할 때 `/3600`이 누락된다. 같은 물리 장벽에서 `L_q`, `L_V`는 3,600배 과대이며 298.15 K의 등가 장벽 보정은 `RT ln 3600 = 20.2994 kJ/mol`이다.
2. `m_Si→f_Si` 대수는 같은 capacity basis에서만 맞다. 현재 원소 Si/SiOx/Si-C 값은 theoretical, first-charge, reversible, ICE/utilization과 active-mass denominator가 섞여 production 정량 입력으로 승인할 수 없다.
3. Larché–Cahn 가역 전위 이동의 부호와 차원은 맞지만 `sigma_h(theta,history)` 탄소성·damage 구성식이 없어 Si hysteresis prediction은 닫히지 않는다.
4. 평형 common-potential blend balance는 보존되지만 유한전류의 `i_gr+i_Si=I`와 host별 kinetic/transport closure가 없어 finite-rate additive output을 완결 모델로 볼 수 없다.

### 6.3 추가 교정

- `xi_del=1-theta`를 고정 조성좌표로 두면서 reverse branch에서 여집합을 취하면 LCO `x(xi)`가 뒤집힌다. 조성좌표와 path-progress 좌표를 분리해야 한다.
- `Omega>2RT`인 scalar regular solution의 `x=1/2`는 `g''<0`인 maximum이다. 이는 miscibility gap을 만들지만 LCO ordered superstructure의 안정성을 유도하지 않는다.
- 일반 TST의 `DeltaS`, `DeltaH`, `DeltaCp`에는 `DeltaE0(T)`와 `ln K_dagger(T)`의 온도 미분이 남는다.
- branch `dU/dT`에는 temperature-dependent hysteresis gap의 명시적 미분이 필요하며, reversible heat와 hysteretic dissipation을 합치지 않는다.
- LCO local electronic free energy와 frozen `(x_MIT,T_ref)` T1-wide offset은 별도 모델이다.

## 7. 독립 계산과 검증 기준

- grand-canonical variance response, regular-solution spinodal/binodal/Maxwell, logistic peak/FWHM, TST entropy/enthalpy/heat-capacity, blend root, C-rate/barrier와 stress-voltage dimensions를 builder가 독립 재계산한다.
- `Omega=3RT` probe는 binodal과 spinodal을 분리하고 Maxwell equal-area residual을 수치 적분한다.
- central finite difference는 grand-canonical response, equilibrium peak, TST entropy/heat-capacity와 blend derivative에 사용한다.
- source 식은 frozen production module을 import/execute하지 않고 Git object에서만 읽는다. Code/runtime conformance는 Step 61 소관이다.
- named semantic mutation, strict JSON, builder determinism, exact-seven staged/persistence와 protected/main/Claude guard를 Python 3.12/3.14에서 통과해야 한다.

## 8. 검증 상태

- result-first checkpoint: 작성 완료.
- machine artifact: `365,949` bytes, strict traversal `11,231` nodes로 생성 완료.
- validator missing-artifact RED: 초기 skeleton의 missing-artifact failure를 확인했고, 현재 validator는 `FAIL_P063_STEP59: E_ARTIFACT_MISSING: Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json`으로 명시 진단한다.
- Python 3.12/3.14 content diagnostics: artifact diagnostic `0`, live result↔artifact evidence parity, frozen source/equation replay와 Phase 057 exact record/ID-set PASS, named singleton semantic negative `44/44`, strict JSON negative `5/5`, determinism `2/2`.
- 독립 Task 59A/59B/59C review: 실제 source 전문 범위와 blob을 갖춘 세 보고를 통합 완료. 최종 exact-seven SPEC/QUALITY re-review는 control document hash 고정 후 실행 대기.
- stage/commit/push/persistence: 미실행.

## 9. 다음 조건

이 evidence에서 machine artifact를 결정론적으로 재구성하고 두 Python runtime의 content/negative/determinism gate를 통과한다. 그 뒤 두 ledger와 handover를 Step 59 recovery state로 갱신하고, 모든 named negative가 singleton diagnostic으로 거부되며 최종 독립 SPEC/QUALITY review가 통과할 때만 exact seven을 stage한다.
