# Phase 059 theory contract review

This is a source-linked audit contract, not the final theory manuscript and not
a code-conformance or external-validity verdict.

| ID | Topic | Symbols | Disposition | Closure state | Source anchors |
|---|---|---|---|---|---|
| P059-CON-001 | coordinates | V_app, V_n, R_n, sigma_d, |I| | EMPIRICAL_ONLY | PARTIAL_OBSERVATION_LAYER | graphite_ica_ch1_v1.0.18.2.tex:968 (eq:vn); graphite_ica_ch1_v1.0.18.2.tex:219 (eq:n0map) |
| P059-CON-002 | coordinates | q, Q, Q_cell | CORRECT | OPEN_UNIT_AND_ORIENTATION_CONTRACT | graphite_ica_ch1_v1.0.18.2.tex:1555; graphite_ica_ch1_v1.0.18.2.tex:244 |
| P059-CON-003 | coordinates | c_rate, |I|, Q_cell | CORRECT | OPEN_DIMENSIONAL_BLOCKER | graphite_ica_ch1_v1.0.18.2.tex:219 (eq:n0map); graphite_ica_ch1_v1.0.18.2.tex:221 |
| P059-CON-004 | coordinates | theta, xi | PRESERVE | CLOSED_DEFINITION_NEEDS_ELECTRODE_MAP | graphite_ica_ch1_v1.0.18.2.tex:227; graphite_ica_ch1_v1.0.18.2.tex:524 (eq:fermifn) |
| P059-CON-005 | coordinates | sigma_d, s | CORRECT | OPEN_EQUILIBRIUM_DIRECTION_CONTAMINATION | graphite_ica_ch1_v1.0.18.2.tex:1331 (eq:xieq); graphite_ica_ch1_v1.0.18.2.tex:242 |
| P059-CON-006 | phase_separation | g(xi), Omega, T_c | PRESERVE | CLOSED_WITHIN_SYMMETRIC_REGULAR_SOLUTION | graphite_ica_ch1_v1.0.18.2.tex:665 (eq:gxi); graphite_ica_ch1_v1.0.18.2.tex:677 (eq:sm-thresh) |
| P059-CON-007 | phase_separation | xi_b, xi_s, mu_A, mu_B | PRESERVE | THEORY_ONLY_NOT_PRODUCTION_CLOSURE | appendix_phase_separation.tex:215 (eq:app-binodal); appendix_phase_separation.tex:248 (eq:app-spinodal) |
| P059-CON-008 | phase_separation | Delta U_hys, gamma_j, h_eta,j | EMPIRICAL_ONLY | OPEN_METASTABLE_DYNAMICS | graphite_ica_ch1_v1.0.18.2.tex:1161 (eq:dUhys); graphite_ica_ch1_v1.0.18.2.tex:1182 (eq:Ubranch) |
| P059-CON-009 | phase_separation | f, kappa, M, R(k) | PRESERVE | THEORY_ONLY_DIMENSIONALLY_REPAIRED | appendix_phase_separation.tex:435 (eq:app-ch-F); appendix_phase_separation.tex:446 (eq:app-ch-R); appendix_phase_separation.tex:440 |
| P059-CON-010 | phase_separation | two-phase plateau, production bell kernel | THEORY_ONLY | OPEN_PRODUCTION_TWO_PHASE_CLOSURE | appendix_phase_separation.tex:475; graphite_ica_ch1_v1.0.18.2.tex:1860 |
| P059-CON-011 | width | w_j, n_j, R, T, F | CORRECT | OPEN_ROLE_SPLIT | graphite_ica_ch1_v1.0.18.2.tex:1269 (eq:wbase); graphite_ica_ch2_v1.0.18.2.tex:167 (eq:logistic) |
| P059-CON-012 | width | n_j | EMPIRICAL_ONLY | OPEN_MICROSCOPIC_MEANING | graphite_ica_ch1_v1.0.18.2.tex:1269 (eq:wbase); graphite_ica_ch1_v1.0.18.2.tex:1274 |
| P059-CON-013 | width | w_two_phase, rho_U | EMPIRICAL_ONLY | PRESERVE_AS_OBSERVATION_HYPOTHESIS | graphite_ica_ch1_v1.0.18.2.tex:1860; graphite_ica_ch1_v1.0.18.2.tex:1660 (eq:ensavg) |
| P059-CON-014 | width | Q_j, dQ/dV, w_j | PRESERVE | CLOSED_KERNEL_IDENTITY | graphite_ica_ch1_v1.0.18.2.tex:1564 (eq:belliden); graphite_ica_ch1_v1.0.18.2.tex:1575 (eq:eqpeak) |
| P059-CON-015 | width | w_j, partial S_config/partial theta | CORRECT | OPEN_TWO_PHASE_SEMANTIC_CONTRADICTION | graphite_ica_ch2_v1.0.18.2.tex:247 (eq:dSconfig); graphite_ica_ch2_v1.0.18.2.tex:257 (eq:dVdT_config); graphite_ica_ch2_v1.0.18.2.tex:263 |
| P059-CON-016 | memory | k_j, L_q, |I|, Q_cell | CORRECT | OPEN_RATE_SCALE_AND_QCELL_UNITS | graphite_ica_ch1_v1.0.18.2.tex:1894 (eq:Lq); graphite_ica_ch1_v1.0.18.2.tex:1902 (eq:kuniv) |
| P059-CON-017 | memory | L_V, L_q, dV/dq | EMPIRICAL_ONLY | OPEN_NONMONOTONE_AND_LOCAL_MAP | graphite_ica_ch1_v1.0.18.2.tex:1970 (eq:LV); graphite_ica_ch1_v1.0.18.2.tex:1966 |
| P059-CON-018 | memory | xi_lag, L_V | PRESERVE | CLOSED_MATHEMATICS_OPEN_PROTOCOL_CONTRACT | graphite_ica_ch1_v1.0.18.2.tex:2045 (eq:lag); graphite_ica_ch1_v1.0.18.2.tex:2164 (eq:reversal) |
| P059-CON-019 | memory | xi_lag(V_0), history boundary | CORRECT | OPEN_INITIAL_HISTORY | graphite_ica_ch1_v1.0.18.2.tex:2045 (eq:lag); graphite_ica_ch1_v1.0.18.2.tex:977; graphite_ica_ch1_v1.0.18.2.tex:978 |
| P059-CON-020 | memory | A, z_cut, A_cap, Delta H_a_eff | REJECT | OPEN_LOCAL_BARRIER_CONTRADICTION | graphite_ica_ch1_v1.0.18.2.tex:1916 (eq:Acut); graphite_ica_ch1_v1.0.18.2.tex:1972 |
| P059-CON-021 | memory | L_V_direct, |I| | CORRECT | OPEN_ZERO_CURRENT_LIMIT | graphite_ica_ch1_v1.0.18.2.tex:1894 (eq:Lq); graphite_ica_ch1_v1.0.18.2.tex:1978 |
| P059-CON-022 | n_of_T | n_j(T), n_0, n_1, T_ref | EMPIRICAL_ONLY | OPEN_IDENTIFIABILITY_AND_EXTRAPOLATION | graphite_ica_ch1_v1.0.18.2.tex:1272; graphite_ica_ch2_v1.0.18.2.tex:555 |
| P059-CON-023 | n_of_T | partial w_j/partial T, n_j(T) | PRESERVE | CLOSED_ALGEBRA_OPEN_PHYSICAL_ROLE | graphite_ica_ch2_v1.0.18.2.tex:559 (eq:dwdT-nT); graphite_ica_ch1_v1.0.18.2.tex:1273 |
| P059-CON-024 | n_of_T | n_j(T), Delta S_rxn, theta_E, electronic entropy | UNVERIFIED | OPEN_PARAMETER_IDENTIFIABILITY | graphite_ica_ch2_v1.0.18.2.tex:563 |
| P059-CON-025 | entropy_heat | U_j(T), Delta H_rxn, Delta S_rxn, F | PRESERVE | CLOSED_CONVENTION_NEEDS_MATERIAL_REFERENCE | graphite_ica_ch1_v1.0.18.2.tex:1047 (eq:Uj); graphite_ica_ch1_v1.0.18.2.tex:2513 (eq:lco-dUdT) |
| P059-CON-026 | entropy_heat | S_config, partial S_config/partial theta | PRESERVE | CLOSED_IDEAL_LIMIT_ONLY | graphite_ica_ch2_v1.0.18.2.tex:234 (eq:Sconfig); graphite_ica_ch2_v1.0.18.2.tex:247 (eq:dSconfig) |
| P059-CON-027 | entropy_heat | g_j(V), dU/dT_weighted | EMPIRICAL_ONLY | OPEN_THERMODYNAMIC_INTERPRETATION | graphite_ica_ch2_v1.0.18.2.tex:571 (eq:weighted); graphite_ica_ch2_v1.0.18.2.tex:515 |
| P059-CON-028 | entropy_heat | hysteresis branch mean, dU/dT | CORRECT | OPEN_METASTABLE_SYMMETRY_ASSUMPTION | graphite_ica_ch2_v1.0.18.2.tex:690 (eq:hys_branch); graphite_ica_ch2_v1.0.18.2.tex:697 (eq:hys_rev) |
| P059-CON-029 | entropy_heat | q_rev, I, T, dU_oc/dT | PRESERVE | CLOSED_FORMULA_OPEN_SIGN_MAPPING | graphite_ica_ch2_v1.0.18.2.tex:764 (eq:qrev); graphite_ica_ch2_v1.0.18.2.tex:797 (eq:complete) |
| P059-CON-030 | einstein_vibration | S_vib, theta_E, u=theta_E/T | PRESERVE | CLOSED_SINGLE_OSCILLATOR_ONLY | graphite_ica_ch2_v1.0.18.2.tex:420 (eq:Svib-einstein); graphite_ica_ch2_v1.0.18.2.tex:428 |
| P059-CON-031 | einstein_vibration | Delta S_vib(T), Delta U_vib(T), T_ref | PRESERVE | CLOSED_INTERNAL_ROUND_TRIP | graphite_ica_ch2_v1.0.18.2.tex:435 (eq:dSvib); graphite_ica_ch2_v1.0.18.2.tex:449 (eq:dUvib) |
| P059-CON-032 | einstein_vibration | Delta phonon DOS, mode multiplicity, theta_E,j | CORRECT | OPEN_REACTION_QUANTITY_DEFINITION | graphite_ica_ch2_v1.0.18.2.tex:414; graphite_ica_ch2_v1.0.18.2.tex:391 (eq:Svib_mode) |
| P059-CON-033 | lco_electronic | U_T1, U_T2, U_T3, U_T4 | CORRECT | OPEN_USER_GOAL_HIGH_VOLTAGE_LCO | graphite_ica_ch1_v1.0.18.2.tex:2333; graphite_ica_ch1_v1.0.18.2.tex:2362 |
| P059-CON-034 | lco_electronic | g(E_F,x), S_e | PRESERVE | CLOSED_LIMIT_OPEN_TRANSITION_REGION | graphite_ica_ch1_v1.0.18.2.tex:2759 (eq:Se); graphite_ica_ch1_v1.0.18.2.tex:2816 (eq:gunit) |
| P059-CON-035 | lco_electronic | g_gate(E_F,x), x_MIT, Delta x_MIT | EMPIRICAL_ONLY | OPEN_PRIMARY_DATA_AND_CATEGORY_ERROR | graphite_ica_ch1_v1.0.18.2.tex:2861 (eq:ggate); graphite_ica_ch1_v1.0.18.2.tex:2789 |
| P059-CON-036 | lco_electronic | x(V), xi_eq,1(V), U_1(x,T) | CORRECT | OPEN_FIXED_POINT_AND_CHAIN_RULE | graphite_ica_ch1_v1.0.18.2.tex:3170 (eq:lco-xmap); graphite_ica_ch1_v1.0.18.2.tex:3193 (eq:lco-U1V); graphite_ica_ch1_v1.0.18.2.tex:3200 |
| P059-CON-037 | lco_electronic | Omega_doped, lambda_dop, delta U_dop | EMPIRICAL_ONLY | OPEN_DOPED_MATERIAL_VALIDATION | graphite_ica_ch1_v1.0.18.2.tex:2709 (eq:lco-dope); graphite_ica_ch1_v1.0.18.2.tex:2701 |
| P059-CON-038 | lco_electronic | Delta S_config, Delta S_vib, Delta S_e, U_1(T) | CORRECT | OPEN_COUPLING_AND_CODE_CONFORMANCE | graphite_ica_ch1_v1.0.18.2.tex:3064 (eq:lco-decomp); graphite_ica_ch1_v1.0.18.2.tex:2846 (eq:U1T2); graphite_ica_ch1_v1.0.18.2.tex:3071 |

## Counts

- records: 38
- topics: {"coordinates": 5, "einstein_vibration": 3, "entropy_heat": 5, "lco_electronic": 6, "memory": 6, "n_of_T": 3, "phase_separation": 5, "width": 5}
- dispositions: {"CORRECT": 13, "EMPIRICAL_ONLY": 9, "PRESERVE": 13, "REJECT": 1, "THEORY_ONLY": 1, "UNVERIFIED": 1}

## Highest-impact open contracts

1. `P059-CON-003`: C-rate × capacity has no single unit contract when
   `Q_cell` is allowed to mean either coulombs or ampere-hours.
2. `P059-CON-005`: protocol direction remains inside the historical equilibrium
   logistic even though equilibrium occupancy should be path independent.
3. `P059-CON-010` and `P059-CON-015`: the two-phase width is phenomenological
   while the same numerical width is read as ideal configurational entropy.
4. `P059-CON-020`: the stated local barrier dependence is frozen into a
   transition-level cut affinity, eliminating realized local voltage dependence.
5. `P059-CON-021`: a direct voltage-lag override needs an explicit
   zero-current limit.
6. `P059-CON-024`: n(T), reaction entropy, vibrational, and electronic
   temperature terms have no demonstrated joint identifiability.
7. `P059-CON-032`: one absolute Einstein oscillator is not yet an
   insertion-reaction vibrational entropy.
8. `P059-CON-033`–`P059-CON-038`: the requested doped high-voltage LCO scope,
   implicit composition/electronic feedback, and material validation remain open.

Gate: `PASS_P059_THEORY_CONTRACT_EXTRACTION`.
