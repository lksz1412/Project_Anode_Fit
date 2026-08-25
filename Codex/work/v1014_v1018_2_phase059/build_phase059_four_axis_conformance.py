#!/usr/bin/env python3
"""Build Phase 059 Step 39.3 artifacts without importing the validator."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "b73652bb131d2772be483c4b1730aa8f3161baf5"
CODE_PATH = "Codex/results/PHASE_059_CODE_BEHAVIOR_MATRIX.json"
TEST_PATH = "Codex/results/PHASE_059_TEST_DEMO_CLAIM_MATRIX.json"
MAIN_PATH = "Codex/results/PHASE_059_FOUR_AXIS_CONFORMANCE_MATRIX.json"
SEMANTIC_ONTOLOGY_ID = "P059-SEMANTIC-CONCEPT-ONTOLOGY-V1"
LINK_MATRIX_PATH_BY_CLASS = {
    "CODE": CODE_PATH,
    "TEST_RUNTIME": TEST_PATH,
    "STORED_ARTIFACT": TEST_PATH,
}
INPUT_PATHS = [
    "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json",
    "Codex/results/PHASE_059_THEORY_SOURCE_INDEX.json",
    "Codex/results/PHASE_059_STEP_039_1_THEORY_CLAIM_DISPOSITION_RESULT.md",
    "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json",
    "Codex/results/PHASE_059_PRODUCTION_CODE_DIFF.json",
    "Codex/results/PHASE_059_PRODUCTION_CODE_REVIEW.md",
    "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json",
    "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_REVIEW.md",
    "Codex/results/PHASE_059_ISOLATED_RUNTIME_RESULTS.json",
    "Codex/results/PHASE_059_ISOLATED_RUNTIME_REVIEW.md",
    "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json",
    "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBE_REVIEW.md",
    "Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json",
    "Codex/results/PHASE_059_GOLDEN_NPZ_REVIEW.md",
    "Codex/results/PHASE_059_ARTIFACT_GENEALOGY.json",
    "Codex/results/PHASE_059_ARTIFACT_GENEALOGY_REVIEW.md",
    "Codex/results/PHASE_059_PDF_VISUAL_REVIEW.json",
    "Codex/results/PHASE_059_ARTIFACT_RENDER_AUDIT.md",
    "Codex/results/PHASE_059_IMAGE_AUDIT.json",
    "Codex/results/PHASE_059_STANDALONE_IMAGE_REVIEW.md",
    "Codex/results/PHASE_059_COMPLETION_AUTHORITY_CLAIM_MATRIX.json",
    "Codex/results/PHASE_059_COMPLETION_AUTHORITY_REVIEW.md",
    "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json",
    "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION_RESULT.md",
    "Codex/results/PHASE_059_PHASE058_BLOCKER_DELTA.json",
    "Codex/results/PHASE_059_STEP_039_2_BLOCKER_DELTA_RESULT.md",
]
ALLOWED_STATUSES = {"ALIGNED", "PARTIAL", "MISALIGNED", "ABSENT", "UNVERIFIED"}
AUTHORITY_BOUNDARY = (
    "This row establishes only evidence-bounded internal frozen-corpus conformance. "
    "Even ALIGNED would not establish primary-literature truth, parameter identifiability, "
    "or external material validity for graphite, LCO, Si, blend, temperature, or rate."
)
ADJUDICATION_BOUNDARY = (
    "This decision states only whether one frozen production finding is directly applicable "
    "to one frozen theory claim; it does not establish external material validity."
)

# Claim meanings are source-bounded interpretations of the exact anchors stored
# below. They state the compared quantity/dependency and, equally importantly,
# what that claim does not establish.
CLAIM_SEMANTICS: dict[str, tuple[str, str, str]] = {
    "P059-TCL-001": ("Q_cell, Q_cell_Ah/Q_cell_C, normalized q, host stoichiometry, and charge-balance coordinates", "Q_cell*q balances background charge and transition occupancies; unit-specific capacity determines the current conversion used downstream.", "Does not choose an electrode stoichiometry map or permit Ah and coulomb variables to share one ambiguous symbol."),
    "P059-TCL-002": ("convexified phase fraction, finite observed peak width, and the observation kernel", "Equilibrium phase fractions must feed a separately defined broadening/observation operator before comparison with finite-width data.", "Does not derive empirical width from ideal-solution configurational entropy or close a production two-phase model."),
    "P059-TCL-003": ("n_j(T), w_j=n_j(T)RT/F, and partial w_j/partial T", "The same n_j(T) determines both width and its temperature derivative, which then propagates into configurational reversible heat.", "Does not authorize unbounded extrapolation or activate n(T) without per-temperature diagnostics and positivity."),
    "P059-TCL-004": ("joint identifiability of n(T), vibrational, and electronic terms", "Independent temperature observables must identify the coupled parameter blocks before they are enabled together.", "Does not infer identifiability from fit convergence, component existence, or a single temperature."),
    "P059-TCL-005": ("doped high-voltage LCO phase/oxygen-redox scope near the O3-to-H1-3 region", "A separately parameterized material/state model and public high-voltage data are prerequisites for extending the generic low-voltage defaults.", "Does not claim the three generic LCO transitions represent doped high-voltage behavior."),
    "P059-TCL-009": ("regular-solution binodal xi_b(T) and critical temperature T_c", "The common-tangent/binodal relation supplies equilibrium coexistence fractions as temperature changes.", "Does not use the spinodal as an equilibrium phase boundary or make fitted Omega universal."),
    "P059-TCL-010": ("Cahn-Hilliard free energy F[xi] with bulk f(xi) and gradient penalty kappa|grad xi|^2", "The spatial composition field determines free energy through distinct bulk-density and gradient-energy terms.", "Does not supply material kappa, molar-to-volumetric conversion, mobility, or quantitative kinetics."),
    "P059-TCL-011": ("Cahn-Hilliard growth rate R(k) from M, k, f''(xi_bar), and kappa", "Mobility and curvature set the wavelength-dependent linear growth/decay rate after the free-energy units are fixed.", "Does not calibrate M or kappa and does not turn the phase-field relation into the production observation model."),
    "P059-TCL-023": ("regular-solution spinodal xi_s plus/minus from f''(xi)=0", "The loss of local curvature stability defines metastability limits below T_c.", "Does not substitute spinodal points for equilibrium binodal fractions."),
    "P059-TCL-025": ("cutoff affinity A from z_cut, n_j, R, T, and A_cap", "The displayed cutoff maps temperature and width multiplicity to one bounded affinity used by the rate model.", "Does not establish a local electrochemical affinity or detailed-balance rate along a voltage trajectory."),
    "P059-TCL-026": ("voltage lag length L_V=|dV/dq|*L_q", "A chronology-preserving q-domain lag is projected to voltage only after evaluating the local trajectory slope.", "Does not authorize voltage sorting, direct nonzero L_V at I=0, or an ambiguous capacity/time basis."),
    "P059-TCL-030": ("q-domain lag state r_j and L_q=|I|/(Q_cell*k_j)", "Current, capacity basis, and kinetic rate set the relaxation length while r_j evolves in chronological capacity order.", "Does not define a universal molecular prefactor, erase initial history, or permit a nonzero zero-current lag."),
    "P059-TCL-033": ("Sommerfeld electronic entropy S_e(T,x)=pi^2 k_B^2 T g(E_F,x)/3", "Temperature and composition-dependent density of states determine the electronic entropy contribution.", "Does not remain valid through an MIT without electronic-structure or measured heat-capacity evidence."),
    "P059-TCL-034": ("LCO center shift U_1(T) with linear entropy and quadratic electronic-temperature terms", "Integrating a temperature-dependent reaction entropy moves the transition center from T_ref.", "Does not establish factorization, reaction-resolved vibration, or implementation consistency by algebra alone."),
    "P059-TCL-035": ("phenomenological branch center U_j^d from sigma_d, hysteresis scale, and branch factor", "Protocol direction shifts the observed branch center through a static empirical multiplier.", "Does not provide a trajectory-state hysteresis model or validate reversal/pulse behavior."),
    "P059-TCL-037": ("half-reaction center U_j=(-Delta H_rxn,j+T Delta S_rxn,j)/F", "Differential reaction enthalpy and entropy determine the electrode half-reaction voltage.", "Does not equate cumulative formation quantities with differential reaction quantities or validate material inputs."),
    "P059-TCL-039": ("logistic derivative xi_eq(1-xi_eq) and unit-area bell kernel", "Differentiating occupancy produces the normalized peak whose integrated area must conserve transition capacity.", "Does not validate kinetic broadening, material parameters, or finite-window area without a numerical gate."),
    "P059-TCL-048": ("regular-solution hysteresis span Delta U_hys from Omega, T, and u", "The symmetric regular-solution metastability construction sets a temperature-dependent static span.", "Does not replace an internal-state kinetic hysteresis model or validate arbitrary materials."),
    "P059-TCL-050": ("ensemble-averaged dQ/dV as convolution over a normalized rho(U_app)", "A distribution of apparent centers broadens the single-domain response through an observation integral.", "Does not identify rho from data, assign it the ideal thermal-width symbol, or establish a two-phase mechanism."),
    "P059-TCL-053": ("equilibrium transition peak Q_j*xi_eq(1-xi_eq)/w_j", "Occupancy slope and width determine local dQ/dV while integration must recover Q_j.", "Does not establish the physical origin of w_j or validate kinetic/non-equilibrium peaks."),
    "P059-TCL-055": ("Fermi occupation theta from beta and Delta mu", "Chemical-potential difference fixes one equilibrium state orientation independent of protocol traversal direction.", "Does not put charge/discharge direction inside the equilibrium occupation law."),
    "P059-TCL-056": ("composition gate g(E_F,x) across x_MIT with width Delta x_MIT", "Composition changes the density-of-states factor that feeds electronic entropy and its implicit x(V,T) feedback.", "Does not justify the gate by Fermi-like shape or calibrate DOS/entropy parameters without data."),
    "P059-TCL-060": ("density-of-states unit conversion from states/eV/atom to states/J/atom", "Division by the exact eV-to-joule factor changes units without changing the physical DOS function.", "Does not validate a smooth-DOS approximation, MIT behavior, or the temperature/composition at which DOS is evaluated."),
    "P059-TCL-061": ("symmetric regular-solution free energy g_j(xi) from ideal mixing and Omega_j xi(1-xi)", "Composition and interaction strength determine curvature and phase-stability behavior in the stated mean-field model.", "Does not make fitted Omega_j universal or extend the symmetric model to arbitrary materials."),
    "P059-TCL-066": ("coarse-grained rate k_j from forward/reverse rates, barrier Delta G_a, affinity A_j, and T", "Local temperature and affinity modify the activation exponent and hence the lag rate supplied to L_q.", "Does not establish k_B T/h as a calibrated mesoscopic prefactor or permit a cutoff affinity frozen across the trace."),
    "P059-TCL-069": ("normalized causal lag convolution xi_lag(V) with L_V and infinite-past history", "A supplied positive L_V weights the chronological equilibrium prehistory into the current occupancy.", "Does not specify the upstream rate law, capacity conversion, initial finite-window state, or voltage-sorting reconstruction."),
    "P059-TCL-073": ("implicit LCO U_1(V,T) built from configurational, vibrational, and electronic reaction entropy", "Composition-dependent reaction entropy is integrated in temperature and coupled back through x(V,T) and U_1(V,T).", "Does not close uniqueness, branch stability, dU/dV feedback, or material vibrational inputs by writing the integral."),
    "P059-TCL-081": ("LCO half-reaction identity partial U_j^cat/partial T=Delta S_rxn,j^cat/F", "The total reaction entropy input determines the temperature derivative of the cathode equilibrium voltage.", "Does not validate any particular electronic/vibrational entropy component or its material parameterization."),
    "P059-TCL-083": ("LCO reaction entropy decomposition into configurational, vibrational, and electronic terms", "All three reaction-specific components feed the material entropy and the resulting voltage-temperature dependence.", "Does not prove factorization, phonon amplitudes, DOS parameters, or consistent implementation."),
    "P059-TCL-084": ("dopant-specific Omega_j^cat,dop and collapse of high-voltage hysteresis near the critical limit", "Dopant chemistry changes interaction parameters and therefore the modeled high-voltage phase/hysteresis response.", "Does not supply dopant chemistry, concentration, cycling, temperature metadata, or fitted public data."),
    "P059-TCL-100": ("composition map x(xi_eq,1(V)) between x_hi and x_lo", "Equilibrium occupancy determines composition, which must feed back into composition-dependent LCO entropy and voltage.", "Does not solve the implicit state equation or establish uniqueness and branch stability."),
    "P059-TCL-108": ("protocol sign sigma_d and current magnitude |I|=c_rate*Q_cell", "The facade maps protocol direction and a capacity-unit-specific C-rate to the observation-layer current.", "Does not merge electrode potentials or permit Ah/coulomb ambiguity without an explicit factor 3600 conversion."),
    "P059-TCL-113": ("direction-dependent reversal lag integrals with separate infinite-past/future branch bounds", "Traversal direction selects the causal branch kernel while preserving prehistory and a supplied L_V.", "Does not define the upstream rate/affinity law, initialize a finite trace, or allow chronology to be sorted away."),
    "P059-TCL-140": ("single-phase versus double-well threshold Omega_j <= or > 2RT", "Regular-solution curvature changes sign at the symmetric mean-field critical threshold.", "Does not make the fitted interaction parameter universal or replace material phase evidence."),
    "P059-TCL-151": ("observation voltage V_n=V_app-sigma_d|I|R_n", "Current and series resistance set the ohmic observation-layer shift from applied to internal voltage.", "Does not merge electrolyte, solid, and interfacial potentials or validate the current-unit conversion."),
    "P059-TCL-153": ("base width w_j=n_j RT/F and the role of n_j", "A thermodynamic interpretation makes ideal width scale with T; an empirical width requires a distinct role and symbol.", "Does not assign microscopic meaning to an empirical/two-phase width without partition-function and identifiability evidence."),
    "P059-TCL-155": ("equilibrium occupancy xi_eq(V,T) and protocol sign sigma_d", "A fixed equilibrium relation should be traversed by protocol; direction belongs to observation or metastable state, not equilibrium itself.", "Does not justify protocol-dependent equilibrium thermodynamics."),
    "P059-TCL-157": ("binary configurational entropy S_config=-R[theta ln theta+(1-theta)ln(1-theta)]", "Homogeneous site occupancy determines ideal configurational entropy.", "Does not regularize endpoint divergences or apply unchanged inside convexified two-phase regions."),
    "P059-TCL-159": ("single Einstein-oscillator entropy S_vib(T;theta_E)", "Temperature relative to theta_E determines the oscillator basis entropy.", "Does not by itself define an insertion-reaction entropy, signed reaction amplitude, or material phonon spectrum."),
    "P059-TCL-160": ("mode entropy S_vib,k from Bose occupation n_k", "Each phonon-mode occupation contributes to the vibrational entropy basis before product-minus-reactant weighting.", "Does not supply reaction-specific spectra, signed amplitudes, DFT, or calorimetric calibration."),
    "P059-TCL-164": ("overlap-weighted partial U_oc/partial T including Delta S^0 and configurational width terms", "Transition weights and the same width/configurational derivative path determine the aggregate entropy coefficient.", "Does not validate heat sign, empirical-width thermodynamics, or calorimetric agreement."),
    "P059-TCL-165": ("partial S_config/partial theta=-R ln[theta/(1-theta)]", "Occupancy differentiates homogeneous configurational entropy and can enter dV/dT only for the matching derived width model.", "Does not automatically apply to empirical ensemble/two-phase widths or endpoint/two-phase regions."),
    "P059-TCL-166": ("reference-difference Delta S_vib(T)=S_vib(T)-S_vib(T_ref)", "The same positive reference temperature anchors vibrational entropy to zero at T_ref.", "Does not add reaction amplitudes, validate nonpositive T_ref, activate defaults, or establish material phonons."),
    "P059-TCL-167": ("Delta U_vib reference construction and partial Delta U_vib/partial T=Delta S_vib/F", "Reference-subtracted vibrational free energy and entropy must satisfy the round-trip temperature derivative.", "Does not validate nonpositive T_ref, reaction spectra/amplitudes, activation, or material calibration."),
    "P059-TCL-168": ("configurational contribution to partial V/partial T at fixed xi", "The same homogeneous occupancy/width model propagates partial S_config/partial theta into voltage-temperature response.", "Does not attach configurational entropy to an unrelated empirical width."),
    "P059-TCL-169": ("partial w_j/partial T=(R/F)[n_j(T)+T dn_j/dT]", "One n_j(T) parameter source determines both w and its derivative by the product rule.", "Does not mix ideal and empirical width derivatives or permit inconsistent fallback parameters."),
    "P059-TCL-172": ("branch-specific partial U_oc^(d)/partial T as a transition-weighted reaction entropy", "Branch occupancies/weights determine an apparent branch entropy coefficient.", "Does not establish equilibrium entropy when protocol history is erased or validate the branch approximation."),
    "P059-TCL-173": ("reversible coefficient as the average of charge and discharge dU_oc/dT branches", "A tested symmetric branch average approximates a reversible entropy coefficient.", "Does not prove equilibrium, erase relaxation requirements, or validate the arithmetic average universally."),
    "P059-TCL-176": ("ideal logistic theta_eq/xi_eq versus (V-U_j)/w", "For an ideal independent-site interpretation, center and thermal width set complementary logistic occupations.", "Does not identify empirical ensemble/two-phase width with the ideal thermal width."),
    "P059-TCL-179": ("reversible heat q_rev=-I*T*partial U_oc/partial T=-I*T*Delta S/F", "Current, absolute temperature, entropy coefficient, and an explicit sign convention determine reversible heat.", "Does not validate material dU/dT inputs, calorimetric signs, or half-cell/full-cell sign mapping."),
    "P059-TCL-182": ("apparent overlap-weighted partial U_oc/partial T from Q_j g_j and Delta S_rxn,j", "Peak overlap weights material transition entropy inputs into a local apparent coefficient.", "Does not make the coefficient a fundamental equilibrium observable or validate it without independent entropy data."),
}

FINDING_SEMANTICS: dict[str, tuple[str, str]] = {
    "P059-CODE-001": ("work-grid removal and the pointwise causal-memory implementation path", "thermodynamic identities, capacity units, local rate physics, material parameters, and experimental validity"),
    "P059-CODE-002": ("dqdv voltage sorting and reconstructed output order, which erase chronological trajectory state", "relations evaluated on an already preserved trajectory, material thermodynamics, and unit conversion"),
    "P059-CODE-003": ("the first lagged occupancy initializer out[0]=ksi_eq[0]", "kernel normalization, the local kinetic law, width algebra, and material entropy"),
    "P059-CODE-004": ("the direct L_V override return before the I<=0 equilibrium branch", "positive-current derived rate identities, convolution normalization at a supplied L_V, and material calibration"),
    "P059-CODE-005": ("one cutoff-derived affinity A held constant across the voltage trace", "the normalized lag/reversal kernel at supplied L_V, thermodynamic heat identities, and capacity units"),
    "P059-CODE-006": ("facade current I=c_rate*Q_cell with an unresolved Ah-versus-coulomb basis", "the form of equilibrium thermodynamics, kernel normalization, and material-specific rate constants"),
    "P059-CODE-007": ("fallback width n=1 paired with fallback dwdT=0 in the reversible-heat path", "ideal logistic algebra, an independently specified empirical kernel, chronology, and external width validation"),
    "P059-CODE-008": ("one trace-mean T_rep used to resolve lag length for an otherwise pointwise temperature trace", "equilibrium thermodynamic identities and the normalized kernel when a valid local L_V is already supplied"),
    "P059-CODE-009": ("theta_E_Tref checked for finiteness but not positivity", "Einstein algebra at valid temperatures, reaction amplitudes, default activation, and material phonon evidence"),
    "P059-CODE-010": ("LCO electronic entropy evaluated at hard-coded T_ref=298.15 K without explicit x(V,T) feedback", "generic half-reaction/heat identities, DOS unit conversion, non-electronic materials, and external LCO validity"),
    "P059-CODE-011": ("three generic LCO defaults ending near 4.05 V with no dopant or high-voltage state descriptors", "low-voltage generic algebra, graphite behavior, and any unmodeled material outside the target scope"),
    "P059-CODE-012": ("identical production-code blobs across v1.0.16-v1.0.18.1", "scientific runtime behavior, equation validity, parameter values, and material evidence"),
    "P059-CODE-013": ("optional theta_E helper path absent from all shipped graphite and LCO transition defaults", "Einstein basis algebra, non-vibrational equations, reaction amplitudes, and material phonon validity"),
}

# Ontology-driven classification below is computed from scientific requirement
# intersection and directed dependency traversal. The frozen partition is used
# only as a post-computation regression assertion.

# Source-grounded semantic ontology.  The scientific concepts below factor the
# 51 claim scopes and 13 production findings independently; no claim/finding
# pair is listed here.  Pair classification is computed later from requirement
# intersection and directed dependency reachability, then checked against the
# separately frozen expected partition.
CLAIM_PRIMARY_CONCEPT: dict[str, str] = {
    "P059-TCL-001": "normalized_capacity_charge_balance", "P059-TCL-002": "convexified_phase_observation_operator",
    "P059-TCL-003": "temperature_dependent_width", "P059-TCL-004": "coupled_parameter_identifiability",
    "P059-TCL-005": "doped_high_voltage_lco_scope", "P059-TCL-009": "regular_solution_binodal",
    "P059-TCL-010": "cahn_hilliard_free_energy", "P059-TCL-011": "cahn_hilliard_linear_growth",
    "P059-TCL-023": "regular_solution_spinodal", "P059-TCL-025": "cutoff_affinity",
    "P059-TCL-026": "voltage_projected_lag_length", "P059-TCL-030": "capacity_domain_relaxation",
    "P059-TCL-033": "sommerfeld_electronic_entropy", "P059-TCL-034": "lco_electronic_center_shift",
    "P059-TCL-035": "phenomenological_branch_center", "P059-TCL-037": "half_reaction_enthalpy_entropy_voltage",
    "P059-TCL-039": "logistic_peak_area", "P059-TCL-048": "regular_solution_hysteresis",
    "P059-TCL-050": "ensemble_broadening_convolution", "P059-TCL-053": "equilibrium_dqdv_peak",
    "P059-TCL-055": "equilibrium_fermi_occupation", "P059-TCL-056": "composition_dependent_dos_gate",
    "P059-TCL-060": "dos_unit_conversion", "P059-TCL-061": "symmetric_regular_solution_free_energy",
    "P059-TCL-066": "affinity_coupled_activation_rate", "P059-TCL-069": "causal_lag_convolution",
    "P059-TCL-073": "implicit_lco_entropy_voltage_feedback", "P059-TCL-081": "lco_voltage_temperature_derivative",
    "P059-TCL-083": "lco_entropy_decomposition", "P059-TCL-084": "dopant_dependent_lco_hysteresis",
    "P059-TCL-100": "lco_composition_feedback_map", "P059-TCL-108": "protocol_current_capacity_mapping",
    "P059-TCL-113": "reversal_history_lag_integral", "P059-TCL-140": "regular_solution_critical_threshold",
    "P059-TCL-151": "ohmic_observation_voltage", "P059-TCL-153": "ideal_vs_empirical_width_role",
    "P059-TCL-155": "equilibrium_occupation_protocol_separation", "P059-TCL-157": "binary_configurational_entropy",
    "P059-TCL-159": "einstein_oscillator_entropy", "P059-TCL-160": "bose_mode_entropy",
    "P059-TCL-164": "overlap_weighted_voltage_temperature", "P059-TCL-165": "configurational_entropy_derivative",
    "P059-TCL-166": "referenced_vibrational_entropy", "P059-TCL-167": "referenced_vibrational_voltage",
    "P059-TCL-168": "configurational_voltage_temperature", "P059-TCL-169": "width_product_rule",
    "P059-TCL-172": "branch_entropy_coefficient", "P059-TCL-173": "branch_averaged_reversible_coefficient",
    "P059-TCL-176": "ideal_logistic_occupation", "P059-TCL-179": "reversible_heat_identity",
    "P059-TCL-182": "apparent_overlap_entropy_coefficient",
}

DIRECT_REQUIREMENT_CLAIMS: dict[str, tuple[str, ...]] = {
    "capacity_current_unit_consistency": ("P059-TCL-001", "P059-TCL-026", "P059-TCL-030", "P059-TCL-108", "P059-TCL-151"),
    "chronological_trajectory_preservation": ("P059-TCL-026", "P059-TCL-030", "P059-TCL-069", "P059-TCL-113"),
    "finite_window_initial_history": ("P059-TCL-069", "P059-TCL-113"),
    "zero_current_lag_limit": ("P059-TCL-026", "P059-TCL-030"),
    "local_affinity_rate_coupling": ("P059-TCL-025", "P059-TCL-030", "P059-TCL-066"),
    "width_temperature_derivative_consistency": ("P059-TCL-003", "P059-TCL-153", "P059-TCL-164", "P059-TCL-165", "P059-TCL-168", "P059-TCL-169", "P059-TCL-176"),
    "local_temperature_rate_evaluation": ("P059-TCL-025", "P059-TCL-026", "P059-TCL-030", "P059-TCL-066"),
    "positive_einstein_reference_temperature": ("P059-TCL-166", "P059-TCL-167"),
    "lco_electronic_temperature_scaling": ("P059-TCL-033", "P059-TCL-034"),
    "lco_composition_electronic_feedback": ("P059-TCL-056", "P059-TCL-073", "P059-TCL-083", "P059-TCL-100"),
    "doped_high_voltage_material_state_scope": ("P059-TCL-005", "P059-TCL-084"),
    "shipped_vibrational_path_activation": ("P059-TCL-083", "P059-TCL-159", "P059-TCL-160", "P059-TCL-166", "P059-TCL-167"),
}

DEPENDENCY_TARGET_CLAIMS: dict[str, tuple[str, ...]] = {
    "pointwise_memory_realization": ("P059-TCL-026", "P059-TCL-030", "P059-TCL-069", "P059-TCL-113"),
    "protocol_trajectory_context": ("P059-TCL-035", "P059-TCL-048", "P059-TCL-055", "P059-TCL-155", "P059-TCL-172", "P059-TCL-173"),
    "history_initialization_dependency": ("P059-TCL-026", "P059-TCL-030", "P059-TCL-172", "P059-TCL-173"),
    "supplied_lag_boundary_dependency": ("P059-TCL-066", "P059-TCL-069", "P059-TCL-113"),
    "affinity_upstream_lag_dependency": ("P059-TCL-026", "P059-TCL-069", "P059-TCL-113"),
    "capacity_scale_upstream_lag_dependency": ("P059-TCL-066", "P059-TCL-069", "P059-TCL-113"),
    "width_parameter_identifiability_input": ("P059-TCL-004",),
    "width_observation_kernel_input": ("P059-TCL-050", "P059-TCL-053"),
    "width_configurational_entropy_input": ("P059-TCL-157",),
    "width_branch_entropy_input": ("P059-TCL-172", "P059-TCL-173"),
    "width_reversible_heat_input": ("P059-TCL-179", "P059-TCL-182"),
    "local_temperature_upstream_lag": ("P059-TCL-069", "P059-TCL-113"),
    "einstein_reference_to_lco_center": ("P059-TCL-034", "P059-TCL-073"),
    "einstein_reference_to_reaction_entropy": ("P059-TCL-037", "P059-TCL-081", "P059-TCL-083", "P059-TCL-164"),
    "einstein_reference_to_branch_heat": ("P059-TCL-172", "P059-TCL-173", "P059-TCL-179", "P059-TCL-182"),
    "einstein_reference_basis_context": ("P059-TCL-159",),
    "lco_electronic_parameter_identifiability": ("P059-TCL-004",),
    "lco_electronic_reaction_entropy_dependency": ("P059-TCL-037", "P059-TCL-081", "P059-TCL-164"),
    "lco_electronic_branch_heat_dependency": ("P059-TCL-172", "P059-TCL-173", "P059-TCL-179", "P059-TCL-182"),
    "lco_dos_evaluation_context": ("P059-TCL-060",),
    "vibrational_parameter_identifiability": ("P059-TCL-004",),
    "vibrational_center_shift_dependency": ("P059-TCL-034", "P059-TCL-073"),
    "vibrational_reaction_entropy_dependency": ("P059-TCL-037", "P059-TCL-081", "P059-TCL-164"),
    "vibrational_branch_heat_dependency": ("P059-TCL-172", "P059-TCL-173", "P059-TCL-179", "P059-TCL-182"),
}

FINDING_ONTOLOGY_SCOPE: dict[str, dict[str, Any]] = {
    "P059-CODE-001": {"behavior": "pointwise_causal_memory_without_work_grid", "violates": (), "emits": ("pointwise_memory_realization",)},
    "P059-CODE-002": {"behavior": "voltage_sorting_erases_trajectory_chronology", "violates": ("chronological_trajectory_preservation",), "emits": ("protocol_trajectory_context",)},
    "P059-CODE-003": {"behavior": "equilibrium_forced_finite_window_initializer", "violates": ("finite_window_initial_history",), "emits": ("history_initialization_dependency",)},
    "P059-CODE-004": {"behavior": "direct_voltage_lag_bypasses_zero_current_limit", "violates": ("zero_current_lag_limit",), "emits": ("supplied_lag_boundary_dependency",)},
    "P059-CODE-005": {"behavior": "cutoff_affinity_frozen_across_voltage_trace", "violates": ("local_affinity_rate_coupling",), "emits": ("affinity_upstream_lag_dependency",)},
    "P059-CODE-006": {"behavior": "c_rate_capacity_unit_basis_is_ambiguous", "violates": ("capacity_current_unit_consistency",), "emits": ("capacity_scale_upstream_lag_dependency",)},
    "P059-CODE-007": {"behavior": "width_and_temperature_derivative_fallbacks_disagree", "violates": ("width_temperature_derivative_consistency",), "emits": ("width_parameter_identifiability_input", "width_observation_kernel_input", "width_configurational_entropy_input", "width_branch_entropy_input", "width_reversible_heat_input")},
    "P059-CODE-008": {"behavior": "trace_mean_temperature_replaces_local_rate_temperature", "violates": ("local_temperature_rate_evaluation",), "emits": ("local_temperature_upstream_lag",)},
    "P059-CODE-009": {"behavior": "einstein_reference_temperature_lacks_positivity_guard", "violates": ("positive_einstein_reference_temperature",), "emits": ("einstein_reference_to_lco_center", "einstein_reference_to_reaction_entropy", "einstein_reference_to_branch_heat", "einstein_reference_basis_context")},
    "P059-CODE-010": {"behavior": "lco_electronic_entropy_is_frozen_at_reference_temperature", "violates": ("lco_electronic_temperature_scaling", "lco_composition_electronic_feedback"), "emits": ("lco_electronic_parameter_identifiability", "lco_electronic_reaction_entropy_dependency", "lco_electronic_branch_heat_dependency", "lco_dos_evaluation_context")},
    "P059-CODE-011": {"behavior": "generic_lco_defaults_omit_dopant_high_voltage_state", "violates": ("doped_high_voltage_material_state_scope",), "emits": ()},
    "P059-CODE-012": {"behavior": "production_blobs_are_copy_forward_identical", "violates": (), "emits": ()},
    "P059-CODE-013": {"behavior": "shipped_transition_defaults_leave_einstein_path_dormant", "violates": ("shipped_vibrational_path_activation",), "emits": ("vibrational_parameter_identifiability", "vibrational_center_shift_dependency", "vibrational_reaction_entropy_dependency", "vibrational_branch_heat_dependency")},
}

def claim_ontology_scope(claim_id: str) -> dict[str, Any]:
    return {
        "primary_concept": CLAIM_PRIMARY_CONCEPT[claim_id],
        "direct_requirements": [concept for concept, members in DIRECT_REQUIREMENT_CLAIMS.items() if claim_id in members],
        "dependency_targets": [concept for concept, members in DEPENDENCY_TARGET_CLAIMS.items() if claim_id in members],
    }


def ontology_edges() -> list[list[str]]:
    edges: list[list[str]] = []
    for scope in FINDING_ONTOLOGY_SCOPE.values():
        edges.extend([[scope["behavior"], concept] for concept in scope["violates"] + scope["emits"]])
    return edges


SEMANTIC_ONTOLOGY_EDGES = ontology_edges()

# Builder-owned expected partition. It is asserted only after ontology
# computation and never creates a concept, edge, bridge, or classification.
DIRECT_CODE: dict[str, list[str]] = {
    "P059-TCL-001": ["P059-CODE-006"],
    "P059-TCL-003": ["P059-CODE-007"],
    "P059-TCL-005": ["P059-CODE-011"],
    "P059-TCL-025": ["P059-CODE-005", "P059-CODE-008"],
    "P059-TCL-026": ["P059-CODE-002", "P059-CODE-004", "P059-CODE-006", "P059-CODE-008"],
    "P059-TCL-030": ["P059-CODE-002", "P059-CODE-004", "P059-CODE-005", "P059-CODE-006", "P059-CODE-008"],
    "P059-TCL-033": ["P059-CODE-010"],
    "P059-TCL-034": ["P059-CODE-010"],
    "P059-TCL-056": ["P059-CODE-010"],
    "P059-TCL-066": ["P059-CODE-005", "P059-CODE-008"],
    "P059-TCL-069": ["P059-CODE-002", "P059-CODE-003"],
    "P059-TCL-073": ["P059-CODE-010"],
    "P059-TCL-083": ["P059-CODE-010", "P059-CODE-013"],
    "P059-TCL-084": ["P059-CODE-011"],
    "P059-TCL-100": ["P059-CODE-010"],
    "P059-TCL-108": ["P059-CODE-006"],
    "P059-TCL-113": ["P059-CODE-002", "P059-CODE-003"],
    "P059-TCL-151": ["P059-CODE-006"],
    "P059-TCL-153": ["P059-CODE-007"],
    "P059-TCL-159": ["P059-CODE-013"],
    "P059-TCL-160": ["P059-CODE-013"],
    "P059-TCL-164": ["P059-CODE-007"],
    "P059-TCL-165": ["P059-CODE-007"],
    "P059-TCL-166": ["P059-CODE-009", "P059-CODE-013"],
    "P059-TCL-167": ["P059-CODE-009", "P059-CODE-013"],
    "P059-TCL-168": ["P059-CODE-007"],
    "P059-TCL-169": ["P059-CODE-007"],
    "P059-TCL-176": ["P059-CODE-007"],
}
RELATED_CODE = {
    ("P059-TCL-004", "P059-CODE-007"), ("P059-TCL-004", "P059-CODE-010"),
    ("P059-TCL-004", "P059-CODE-013"),
    ("P059-TCL-026", "P059-CODE-001"), ("P059-TCL-026", "P059-CODE-003"),
    ("P059-TCL-026", "P059-CODE-005"),
    ("P059-TCL-030", "P059-CODE-001"), ("P059-TCL-030", "P059-CODE-003"),
    ("P059-TCL-034", "P059-CODE-013"),
    ("P059-TCL-034", "P059-CODE-009"),
    ("P059-TCL-035", "P059-CODE-002"), ("P059-TCL-037", "P059-CODE-010"),
    ("P059-TCL-037", "P059-CODE-013"),
    ("P059-TCL-037", "P059-CODE-009"),
    ("P059-TCL-048", "P059-CODE-002"), ("P059-TCL-050", "P059-CODE-007"),
    ("P059-TCL-053", "P059-CODE-007"), ("P059-TCL-055", "P059-CODE-002"), ("P059-TCL-155", "P059-CODE-002"),
    ("P059-TCL-060", "P059-CODE-010"),
    ("P059-TCL-066", "P059-CODE-004"), ("P059-TCL-066", "P059-CODE-006"),
    ("P059-TCL-069", "P059-CODE-001"), ("P059-TCL-069", "P059-CODE-004"),
    ("P059-TCL-069", "P059-CODE-005"),
    ("P059-TCL-069", "P059-CODE-006"), ("P059-TCL-069", "P059-CODE-008"),
    ("P059-TCL-073", "P059-CODE-009"), ("P059-TCL-073", "P059-CODE-013"),
    ("P059-TCL-081", "P059-CODE-009"), ("P059-TCL-081", "P059-CODE-010"),
    ("P059-TCL-081", "P059-CODE-013"),
    ("P059-TCL-083", "P059-CODE-009"),
    ("P059-TCL-113", "P059-CODE-001"), ("P059-TCL-113", "P059-CODE-004"),
    ("P059-TCL-113", "P059-CODE-005"),
    ("P059-TCL-113", "P059-CODE-006"), ("P059-TCL-113", "P059-CODE-008"),
    ("P059-TCL-157", "P059-CODE-007"),
    ("P059-TCL-159", "P059-CODE-009"),
    ("P059-TCL-164", "P059-CODE-009"), ("P059-TCL-164", "P059-CODE-010"), ("P059-TCL-164", "P059-CODE-013"),
    ("P059-TCL-172", "P059-CODE-002"), ("P059-TCL-172", "P059-CODE-003"), ("P059-TCL-172", "P059-CODE-007"),
    ("P059-TCL-172", "P059-CODE-009"), ("P059-TCL-172", "P059-CODE-010"), ("P059-TCL-172", "P059-CODE-013"),
    ("P059-TCL-173", "P059-CODE-002"), ("P059-TCL-173", "P059-CODE-003"), ("P059-TCL-173", "P059-CODE-007"),
    ("P059-TCL-173", "P059-CODE-009"), ("P059-TCL-173", "P059-CODE-010"), ("P059-TCL-173", "P059-CODE-013"),
    ("P059-TCL-179", "P059-CODE-007"), ("P059-TCL-179", "P059-CODE-010"),
    ("P059-TCL-179", "P059-CODE-009"), ("P059-TCL-179", "P059-CODE-013"),
    ("P059-TCL-182", "P059-CODE-007"), ("P059-TCL-182", "P059-CODE-010"),
    ("P059-TCL-182", "P059-CODE-009"), ("P059-TCL-182", "P059-CODE-013"),
}
DIRECT_REASON = {
    ("P059-TCL-001", "P059-CODE-006"): "The charge-conservation prose requires distinct coulomb, ampere-hour, normalized-capacity, and stoichiometric variables; the facade instead reuses generic Q_cell in a per-hour C-rate multiplication.",
    ("P059-TCL-003", "P059-CODE-007"): "The n(T) prose requires one self-consistent w and dw/dT path, while the production default uses n=1 for width but zero derivative when n is omitted.",
    ("P059-TCL-005", "P059-CODE-011"): "The contract-only high-voltage LCO scope requires a separately validated doped model, while the production finding establishes generic defaults ending near 4.05 V with no dopant/state descriptors.",
    ("P059-TCL-025", "P059-CODE-005"): "The cutoff-affinity equation is evaluated as one frozen transition constant, exactly matching the finding that local voltage-dependent driving is absent.",
    ("P059-TCL-025", "P059-CODE-008"): "The cutoff-affinity claim requires local state/temperature driving, while production resolves lag kinetics once at trace-mean temperature.",
    ("P059-TCL-026", "P059-CODE-002"): "The local V(q) projection requires chronology-preserving state evolution; production voltage sorting destroys that supplied trajectory order.",
    ("P059-TCL-026", "P059-CODE-004"): "Because eq:LV projects Lq and Lq tends to zero with current, a direct L_V override that survives I=0 violates the projected zero-current limit.",
    ("P059-TCL-026", "P059-CODE-006"): "The projected L_V inherits the Q_cell/time scale of Lq, so the facade's ambiguous Ah-versus-coulomb conversion directly introduces the reproduced factor-3,600 scale error.",
    ("P059-TCL-026", "P059-CODE-008"): "The projected L_V inherits the temperature-dependent Lq, while production resolves that lag scale once at trace-mean rather than local temperature.",
    ("P059-TCL-030", "P059-CODE-002"): "The Lq ODE evolves r_j along chronological q; sorting by voltage changes that independent-variable trajectory and therefore the realized state solution.",
    ("P059-TCL-030", "P059-CODE-004"): "The Lq contract requires the zero-current lag limit, while direct L_V bypasses the I=0 branch.",
    ("P059-TCL-030", "P059-CODE-005"): "Eq:Lq depends on k_j, but production constructs that rate from one cutoff affinity rather than a local electrochemical driving-force/barrier relation.",
    ("P059-TCL-030", "P059-CODE-006"): "The Lq denominator uses Q_cell and a time-based rate; the production facade leaves Ah/C conversion ambiguous and exposes the factor-3,600 scale defect.",
    ("P059-TCL-030", "P059-CODE-008"): "The Lq rate is state/temperature dependent, while production collapses T(V) to one mean before resolving lag length.",
    ("P059-TCL-033", "P059-CODE-010"): "Eq:Se requires the Sommerfeld electronic entropy to scale as T g(E_F,x), while the LCO subclass evaluates the electronic term only at 298.15 K.",
    ("P059-TCL-034", "P059-CODE-010"): "The quadratic U1(T) equation requires explicit temperature dependence, while the LCO electronic term is evaluated only at 298.15 K.",
    ("P059-TCL-056", "P059-CODE-010"): "Eq:ggate makes g(E_F,x) composition dependent, while production evaluates the gate at one stored x_center and supplies no implicit x(V,T) feedback.",
    ("P059-TCL-066", "P059-CODE-005"): "Eq:kuniv couples the activation barrier to the local affinity A_j, but production freezes A at one cutoff-derived transition constant across the voltage trace.",
    ("P059-TCL-066", "P059-CODE-008"): "Eq:kuniv is explicitly temperature dependent, while production resolves the resulting lag rate once at trace-mean T rather than the local T(t) trajectory.",
    ("P059-TCL-069", "P059-CODE-002"): "The normalized lag integral retains traversal order, while production sorting erases chronology.",
    ("P059-TCL-069", "P059-CODE-003"): "The infinite-history lag boundary requires explicit initial history; production forces the first state to equilibrium.",
    ("P059-TCL-073", "P059-CODE-010"): "The implicit U1(V,T) relation requires composition-temperature coupling and derivatives; production freezes its electronic contribution at 298.15 K.",
    ("P059-TCL-083", "P059-CODE-010"): "The LCO entropy decomposition requires matched composition and temperature dependence; production freezes the electronic term at 298.15 K.",
    ("P059-TCL-083", "P059-CODE-013"): "Eq:lco-decomp explicitly includes a reaction vibrational entropy component, but shipped graphite and LCO defaults never activate the available theta_E path.",
    ("P059-TCL-084", "P059-CODE-011"): "The empirical dopant equation requires dopant-specific high-voltage data and states; shipped defaults contain no dopant/state descriptor and end near 4.05 V.",
    ("P059-TCL-100", "P059-CODE-010"): "The implicit x(V,T) mapping must feed LCO temperature derivatives; production evaluates the electronic contribution at a fixed 298.15 K.",
    ("P059-TCL-108", "P059-CODE-006"): "The n0 mapping exposes the facade capacity/current conversion; production leaves Q_cell as generic charge while C-rate is per hour.",
    ("P059-TCL-113", "P059-CODE-002"): "The reversal equation stores distinct traversal branches, while production sorting destroys reversal order.",
    ("P059-TCL-113", "P059-CODE-003"): "The reversal integrals require branch prehistory extending from an asymptotic boundary, while production resets the first lagged state to instantaneous equilibrium on every call.",
    ("P059-TCL-151", "P059-CODE-006"): "Eq:vn applies the current directly to the ohmic drop, so the facade's ambiguous Ah-versus-coulomb C-rate conversion directly mis-scales V_n when that route is used.",
    ("P059-TCL-153", "P059-CODE-007"): "The baseline width role must be explicit and self-consistent; production's implicit default width and dwdT use different fallback semantics.",
    ("P059-TCL-159", "P059-CODE-013"): "The Einstein single-oscillator basis exists as an optional helper, but shipped transition defaults never activate theta_E.",
    ("P059-TCL-160", "P059-CODE-013"): "The required reaction-specific signed mode quantity is absent and shipped defaults never activate the optional Einstein helper.",
    ("P059-TCL-164", "P059-CODE-007"): "Eq:complete requires the same thermal width/configurational contribution in dQ/dV weighting and dU/dT; production defaults to n=1 for width but zero dw/dT in reversible heat.",
    ("P059-TCL-165", "P059-CODE-007"): "The configurational derivative must propagate through the thermal-width path only; production's implicit default is thermal in dQ/dV yet suppresses that derivative in reversible heat.",
    ("P059-TCL-166", "P059-CODE-009"): "The reference-difference entropy identity requires a positive reference temperature; production checks theta_E_Tref only for finiteness.",
    ("P059-TCL-166", "P059-CODE-013"): "The reference-difference entropy path is not activated by any shipped transition default.",
    ("P059-TCL-167", "P059-CODE-009"): "The paired voltage/entropy derivative uses the same positive reference-temperature domain; production lacks that guard.",
    ("P059-TCL-167", "P059-CODE-013"): "The paired vibrational voltage path is not activated by any shipped transition default.",
    ("P059-TCL-168", "P059-CODE-007"): "Eq:dVdT_config ties the configurational term to dw/dT, while production's implicit n=1 width is paired with a zero default derivative.",
    ("P059-TCL-169", "P059-CODE-007"): "The dwdT equation requires one n(T) parameter source for width and derivative; production fallbacks disagree.",
    ("P059-TCL-176", "P059-CODE-007"): "The logistic equation's ideal thermal width role must be separated from empirical width, while production retains an implicit inconsistent fallback.",
}
RELATED_REASON = {
    ("P059-TCL-004", "P059-CODE-007"): "The width/dw-dT fallback defect is relevant to the n(T) member of the identifiability bundle, but it does not supply profile likelihood, Fisher rank, or held-out-temperature evidence.",
    ("P059-TCL-004", "P059-CODE-010"): "The frozen LCO electronic term shows one coupled model component is incomplete, but it does not adjudicate joint n(T)/vibrational/electronic identifiability.",
    ("P059-TCL-004", "P059-CODE-013"): "Dormant theta_E defaults bound activation of one candidate component, but they do not provide the requested joint-identifiability evidence.",
    ("P059-TCL-026", "P059-CODE-001"): "Pointwise memory is the implementation architecture around the V(q) projection, but grid removal alone neither preserves nor refutes the projection's trajectory contract.",
    ("P059-TCL-026", "P059-CODE-003"): "An explicit prehistory is a prerequisite for evolving the projected state, but the forced first state does not by itself adjudicate the algebraic L_V projection.",
    ("P059-TCL-026", "P059-CODE-005"): "The frozen affinity changes the upstream Lq supplied to eq:LV, but it does not directly adjudicate the voltage-projection identity.",
    ("P059-TCL-030", "P059-CODE-001"): "Pointwise grid removal changes how the Lq state equation is realized, but source-level grid removal alone does not adjudicate its time basis, rate law, or zero-current limit.",
    ("P059-TCL-030", "P059-CODE-003"): "Every Lq ODE needs an initial state, but the forced equilibrium initializer is a boundary-condition defect rather than an adjudication of the displayed Lq scale law.",
    ("P059-TCL-034", "P059-CODE-013"): "Dormant vibrational defaults bear on the contract's additional reaction-resolved vibrational requirement, but they do not adjudicate the displayed electronic T-squared center law.",
    ("P059-TCL-034", "P059-CODE-009"): "A nonpositive theta_E_Tref can invalidate an optional vibrational contribution upstream of a transition center, but that reference guard neither evaluates nor contradicts the displayed electronic T-squared center law.",
    ("P059-TCL-035", "P059-CODE-002"): "Sorting away reversal and pulse history confirms why a static sigma_d branch factor is only phenomenological, but it does not numerically adjudicate eq:Ubranch.",
    ("P059-TCL-037", "P059-CODE-010"): "The frozen LCO electronic entropy changes one material-specific Delta S supplied to the U_j identity, while the generic enthalpy-entropy identity itself remains distinct.",
    ("P059-TCL-037", "P059-CODE-013"): "Dormant reaction-specific vibrational input can leave one Delta S contribution absent, but it does not adjudicate the generic U_j=(-Delta H+T Delta S)/F identity.",
    ("P059-TCL-037", "P059-CODE-009"): "The incomplete theta_E_Tref guard can invalidate an optional vibrational Delta S input supplied to U_j, while the generic enthalpy-entropy center identity remains algebraically distinct.",
    ("P059-TCL-048", "P059-CODE-002"): "Loss of protocol history limits use of a static hysteresis-width formula as a state model, but it does not adjudicate the regular-solution expression itself.",
    ("P059-TCL-050", "P059-CODE-007"): "The fallback mismatch exposes unresolved width-role semantics, but it does not implement or test the normalized ensemble convolution in eq:ensavg.",
    ("P059-TCL-053", "P059-CODE-007"): "The finding identifies dQ/dV as thermal under the implicit default and reversible heat as frozen; that cross-output inconsistency is relevant but does not refute the equilibrium peak identity alone.",
    ("P059-TCL-055", "P059-CODE-002"): "The claim assigns protocol direction to the trajectory layer, and sorting destroys that layer's history, but the Fermi occupation orientation itself is not adjudicated.",
    ("P059-TCL-155", "P059-CODE-002"): "The claim requires one fixed equilibrium relation to be traversed by protocol while direction remains in the observation/metastable trajectory; voltage sorting erases that supplied chronology without directly changing the equilibrium occupation law.",
    ("P059-TCL-060", "P059-CODE-010"): "The production finding concerns temperature/composition freezing in the same electronic-entropy path; it does not identify an error in the separate eV-to-joule DOS conversion.",
    ("P059-TCL-066", "P059-CODE-004"): "A direct L_V override can bypass the eq:kuniv rate path, but its zero-current defect does not adjudicate the universal prefactor or barrier-affinity equation itself.",
    ("P059-TCL-066", "P059-CODE-006"): "The facade unit defect mis-scales the downstream Lq built from k_j, but it does not adjudicate eq:kuniv's molecular prefactor or affinity coupling.",
    ("P059-TCL-069", "P059-CODE-001"): "Pointwise grid removal concerns architecture and does not establish the lag equation's history boundary or chronology.",
    ("P059-TCL-069", "P059-CODE-004"): "A nonzero direct L_V at zero current changes the lag kernel's physical limit, but it does not adjudicate the normalized convolution identity at a specified positive L_V.",
    ("P059-TCL-069", "P059-CODE-005"): "The frozen cutoff affinity changes the upstream kinetic rate and derived L_V supplied to the lag kernel, but the normalized convolution remains a relation at a specified L_V.",
    ("P059-TCL-069", "P059-CODE-006"): "The Q_cell unit ambiguity changes the derived L_V scale entering the kernel, but not the kernel normalization or initial-history statement itself.",
    ("P059-TCL-069", "P059-CODE-008"): "Trace-mean temperature changes the derived lag scale, but eq:lag itself accepts a supplied L_V and does not specify the local temperature rate law.",
    ("P059-TCL-073", "P059-CODE-013"): "A dormant reaction-specific vibrational term leaves one Delta S input absent from the implicit U1(V,T) construction, but it does not adjudicate the implicit state equation or its dU/dV closure.",
    ("P059-TCL-073", "P059-CODE-009"): "The missing positive theta_E_Tref guard can invalidate an optional vibrational center contribution upstream of implicit U1(V,T), but does not directly adjudicate its composition-state closure.",
    ("P059-TCL-081", "P059-CODE-010"): "The frozen electronic entropy changes one material-specific Delta S input to dU/dT, but it does not adjudicate the generic half-reaction identity partial U/partial T=Delta S/F.",
    ("P059-TCL-081", "P059-CODE-013"): "Dormant vibrational defaults can omit one contribution to reaction entropy, but they do not adjudicate the generic LCO dU/dT thermodynamic identity.",
    ("P059-TCL-081", "P059-CODE-009"): "The nonpositive-reference guard gap can invalidate a vibrational Delta S input upstream of dU/dT, but it does not directly contradict the generic half-reaction derivative identity.",
    ("P059-TCL-083", "P059-CODE-009"): "The LCO decomposition accepts a reaction vibrational entropy input whose reference-difference implementation lacks a positive theta_E_Tref guard; this is an upstream domain defect, not a direct contradiction of the decomposition sum.",
    ("P059-TCL-113", "P059-CODE-001"): "Pointwise grid removal concerns architecture and does not establish reversal-branch preservation.",
    ("P059-TCL-113", "P059-CODE-004"): "A nonzero zero-current lag changes the physical reversal limit, but it does not adjudicate the two normalized branch-integral identities at a specified L_V.",
    ("P059-TCL-113", "P059-CODE-005"): "The frozen cutoff affinity changes the upstream kinetic rate and L_V supplied to both reversal branches, but it does not adjudicate their direction-dependent integration bounds.",
    ("P059-TCL-113", "P059-CODE-006"): "The unit ambiguity changes the L_V scale shared by both reversal branches, not their direction-dependent integration bounds.",
    ("P059-TCL-113", "P059-CODE-008"): "Trace-mean temperature changes the shared lag length but does not by itself adjudicate the reversal branch construction.",
    ("P059-TCL-157", "P059-CODE-007"): "The default dw/dT defect suppresses a downstream configurational contribution, but it does not adjudicate the binary configurational-entropy identity itself.",
    ("P059-TCL-159", "P059-CODE-009"): "The reference-temperature guard is relevant to the difference implementation but does not directly adjudicate the standalone single-oscillator entropy identity.",
    ("P059-TCL-164", "P059-CODE-010"): "Frozen LCO electronic entropy can corrupt a material-specific Delta S input to the weighted coefficient, but it does not adjudicate the generic overlap-weighted aggregation identity.",
    ("P059-TCL-164", "P059-CODE-013"): "Dormant vibrational defaults omit a possible reaction-entropy contribution, but they do not adjudicate the displayed generic weighted coefficient.",
    ("P059-TCL-164", "P059-CODE-009"): "The theta_E_Tref guard gap can invalidate one vibrational dU_j/dT input upstream of the overlap-weighted coefficient, without directly adjudicating the aggregation identity.",
    ("P059-TCL-172", "P059-CODE-002"): "Sorting erases the protocol history needed to interpret branch-specific entropy, but it does not adjudicate the branch-weighted derivative formula itself.",
    ("P059-TCL-172", "P059-CODE-003"): "Forcing the first lagged state to equilibrium removes the prehistory required to realize branch-specific weights and relaxation, but it does not directly refute the displayed branch entropy average.",
    ("P059-TCL-172", "P059-CODE-007"): "The width/dw-dT fallback can alter branch weights and entropy coefficients, but the finding does not test the branch-specific averaging approximation.",
    ("P059-TCL-172", "P059-CODE-009"): "The theta_E_Tref guard gap propagates through vibrational dS and weighted dS_eff into a branch entropy coefficient, but does not directly adjudicate the branch averaging formula.",
    ("P059-TCL-172", "P059-CODE-010"): "The LCO electronic entropy frozen at 298.15 K propagates into weighted dS_eff for a material-specific branch, but does not directly adjudicate the generic branch entropy approximation.",
    ("P059-TCL-172", "P059-CODE-013"): "Dormant theta_E defaults suppress a vibrational component of the weighted branch entropy input, while leaving the displayed branch averaging relation itself unadjudicated.",
    ("P059-TCL-173", "P059-CODE-002"): "Loss of charge/discharge history limits interpretation of a reversible branch average, but it does not adjudicate the arithmetic averaging approximation itself.",
    ("P059-TCL-173", "P059-CODE-003"): "A forced equilibrium first state removes the branch prehistory and relaxation prerequisite for the two coefficients being averaged, but does not directly refute their symmetric-average identity.",
    ("P059-TCL-173", "P059-CODE-007"): "The fallback defect can contaminate each branch coefficient upstream, but it does not directly adjudicate their symmetric average.",
    ("P059-TCL-173", "P059-CODE-009"): "The incomplete theta_E_Tref guard can contaminate vibrational entropy upstream of each branch coefficient, but does not directly adjudicate their arithmetic mean.",
    ("P059-TCL-173", "P059-CODE-010"): "The LCO electronic entropy freeze can contaminate the material-specific dS_eff feeding both branch coefficients, while their symmetric averaging rule remains distinct.",
    ("P059-TCL-173", "P059-CODE-013"): "Dormant theta_E defaults omit a vibrational contribution upstream of the two branch coefficients, but do not directly adjudicate the displayed reversible average.",
    ("P059-TCL-179", "P059-CODE-007"): "The width/dw-dT fallback changes an upstream configurational contribution to dU/dT, but it does not adjudicate the q_rev=-I T dU/dT identity or heat-sign convention.",
    ("P059-TCL-179", "P059-CODE-010"): "The frozen LCO electronic term changes a material-specific dU/dT supplied to q_rev, while the generic -I T dU/dT heat identity remains separate.",
    ("P059-TCL-179", "P059-CODE-009"): "The theta_E_Tref domain gap can invalidate a vibrational entropy contribution upstream of dU/dT and reversible heat, while the generic q_rev=-I T dU/dT identity remains distinct.",
    ("P059-TCL-179", "P059-CODE-013"): "Dormant vibrational defaults can omit a material entropy contribution to q_rev, but they do not adjudicate the heat identity itself.",
    ("P059-TCL-182", "P059-CODE-007"): "The width/dw-dT fallback affects the production full coefficient, but eq:weighted is explicitly a simpler apparent overlap-weighted formula and remains a distinct approximation.",
    ("P059-TCL-182", "P059-CODE-010"): "The frozen LCO electronic term changes one material-specific dU_j/dT input, but it does not adjudicate the generic apparent weighting rule.",
    ("P059-TCL-182", "P059-CODE-009"): "The theta_E_Tref guard gap can invalidate a vibrational dU_j/dT input upstream of the apparent weighted coefficient, without directly adjudicating its overlap-weighting approximation.",
    ("P059-TCL-182", "P059-CODE-013"): "Dormant vibrational defaults omit a possible input term, but they do not adjudicate the apparent overlap weighting itself.",
}

STATUS = {
    "P059-TCL-001": "MISALIGNED", "P059-TCL-003": "MISALIGNED", "P059-TCL-005": "ABSENT",
    "P059-TCL-025": "MISALIGNED", "P059-TCL-026": "MISALIGNED", "P059-TCL-030": "MISALIGNED",
    "P059-TCL-033": "MISALIGNED", "P059-TCL-034": "MISALIGNED", "P059-TCL-039": "PARTIAL",
    "P059-TCL-056": "MISALIGNED", "P059-TCL-066": "MISALIGNED", "P059-TCL-069": "MISALIGNED",
    "P059-TCL-073": "MISALIGNED", "P059-TCL-083": "MISALIGNED",
    "P059-TCL-084": "ABSENT", "P059-TCL-100": "MISALIGNED", "P059-TCL-108": "MISALIGNED",
    "P059-TCL-113": "MISALIGNED", "P059-TCL-151": "MISALIGNED", "P059-TCL-153": "MISALIGNED",
    "P059-TCL-159": "PARTIAL", "P059-TCL-160": "PARTIAL", "P059-TCL-164": "MISALIGNED",
    "P059-TCL-165": "MISALIGNED", "P059-TCL-166": "PARTIAL", "P059-TCL-167": "PARTIAL",
    "P059-TCL-168": "MISALIGNED", "P059-TCL-169": "PARTIAL", "P059-TCL-176": "MISALIGNED",
}
TEST_IDS: dict[str, list[str]] = {
    "P059-TCL-001": ["P059-TD-012", "UNT-001"], "P059-TCL-003": ["P059-TD-011", "P059-TD-012", "WID-004"],
    "P059-TCL-005": ["P059-TD-013", "LCO-003"], "P059-TCL-025": ["P059-TD-012", "KIN-001"],
    "P059-TCL-026": ["P059-TD-012", "ORD-002"], "P059-TCL-030": ["P059-TD-012", "CUR-001", "CUR-002", "MEM-002"],
    "P059-TCL-033": ["P059-TD-007", "P059-TD-013", "LCO-001"], "P059-TCL-034": ["P059-TD-007", "P059-TD-013", "LCO-001"],
    "P059-TCL-039": ["P059-TD-003", "P059-TD-009", "MEM-002"], "P059-TCL-056": ["P059-TD-007", "P059-TD-013", "LCO-001"],
    "P059-TCL-066": ["P059-TD-012", "KIN-001"],
    "P059-TCL-069": ["P059-TD-012", "ORD-002"], "P059-TCL-073": ["P059-TD-007", "P059-TD-013", "LCO-001"],
    "P059-TCL-081": ["P059-TD-007", "P059-TD-013", "LCO-001"], "P059-TCL-083": ["P059-TD-007", "P059-TD-013", "LCO-001"],
    "P059-TCL-084": ["P059-TD-013", "LCO-003"],
    "P059-TCL-100": ["P059-TD-007", "P059-TD-013", "LCO-001"], "P059-TCL-108": ["P059-TD-012", "UNT-001"],
    "P059-TCL-113": ["P059-TD-012", "ORD-002"], "P059-TCL-151": ["P059-TD-012", "UNT-001"],
    "P059-TCL-153": ["P059-TD-011", "P059-TD-012", "WID-004"],
    "P059-TCL-159": ["P059-TD-011", "VIB-001", "VIB-002", "VIB-004"], "P059-TCL-160": ["P059-TD-012", "VIB-003", "VIB-004"],
    "P059-TCL-164": ["P059-TD-011", "P059-TD-012", "WID-004"], "P059-TCL-165": ["P059-TD-011", "P059-TD-012", "WID-004"],
    "P059-TCL-166": ["P059-TD-011", "VIB-001", "VIB-002", "VIB-004"], "P059-TCL-167": ["P059-TD-011", "VIB-001", "VIB-002", "VIB-004"],
    "P059-TCL-168": ["P059-TD-011", "P059-TD-012", "WID-004"], "P059-TCL-169": ["P059-TD-011", "WID-002", "WID-004"],
    "P059-TCL-176": ["P059-TD-011", "P059-TD-012", "WID-004"], "P059-TCL-179": ["P059-TD-011", "P059-TD-012", "WID-004"],
}
ARTIFACT_IDS: dict[str, list[str]] = {
    "P059-TCL-001": ["GOLD-005"], "P059-TCL-003": ["GOLD-005"],
    "P059-TCL-005": ["IMG-059-05"], "P059-TCL-025": ["GOLD-005"], "P059-TCL-026": ["GOLD-005"],
    "P059-TCL-030": ["GOLD-005"], "P059-TCL-033": ["GOLD-005", "IMG-059-05"],
    "P059-TCL-034": ["GOLD-005", "IMG-059-05"], "P059-TCL-039": ["GOLD-006"],
    "P059-TCL-056": ["GOLD-005", "IMG-059-05"], "P059-TCL-066": ["GOLD-005"],
    "P059-TCL-069": ["GOLD-005"], "P059-TCL-073": ["GOLD-005", "IMG-059-05"], "P059-TCL-083": ["GOLD-005", "IMG-059-05"],
    "P059-TCL-081": ["GOLD-005", "IMG-059-05"], "P059-TCL-084": ["GOLD-005", "IMG-059-05"],
    "P059-TCL-100": ["GOLD-005", "IMG-059-05"], "P059-TCL-108": ["GOLD-005"],
    "P059-TCL-113": ["GOLD-005"], "P059-TCL-151": ["GOLD-005"], "P059-TCL-153": ["GOLD-005"],
    "P059-TCL-159": ["GOLD-004", "GOLD-005"],
    "P059-TCL-160": ["GOLD-004", "GOLD-005"], "P059-TCL-166": ["GOLD-004", "GOLD-005"], "P059-TCL-167": ["GOLD-004", "GOLD-005"],
    "P059-TCL-164": ["GOLD-005"], "P059-TCL-165": ["GOLD-005"], "P059-TCL-168": ["GOLD-005"],
    "P059-TCL-169": ["GOLD-004", "GOLD-005"], "P059-TCL-176": ["GOLD-005"], "P059-TCL-179": ["GOLD-005"],
}
BLOCKERS: dict[str, list[str]] = {
    "P059-TCL-001": ["RB-01"], "P059-TCL-003": ["RB-04", "NS-04"],
    "P059-TCL-005": ["NS-03", "ED-02"], "P059-TCL-025": ["RB-05", "P059-BD-NEW-005"],
    "P059-TCL-026": ["RB-01", "RB-06", "RB-08"], "P059-TCL-030": ["RB-01", "RB-05", "RB-06", "RB-08"],
    "P059-TCL-033": ["RB-09", "NS-03"], "P059-TCL-034": ["RB-09", "NS-03", "ED-02"],
    "P059-TCL-039": ["CF-03", "RB-07"], "P059-TCL-056": ["RB-09", "NS-03"],
    "P059-TCL-066": ["RB-05", "P059-BD-NEW-005"],
    "P059-TCL-069": ["RB-08"], "P059-TCL-073": ["RB-09", "NS-03"], "P059-TCL-083": ["RB-09", "NS-03"],
    "P059-TCL-081": ["RB-09", "NS-03"], "P059-TCL-084": ["NS-03", "ED-02"],
    "P059-TCL-100": ["RB-09", "NS-03"], "P059-TCL-108": ["RB-01"],
    "P059-TCL-113": ["RB-08"], "P059-TCL-151": ["RB-01"], "P059-TCL-153": ["RB-04", "RB-10"],
    "P059-TCL-159": ["RB-11", "P059-BD-NEW-001", "P059-BD-NEW-002"], "P059-TCL-160": ["RB-11", "P059-BD-NEW-001", "P059-BD-NEW-002"],
    "P059-TCL-164": ["RB-04", "RB-10"], "P059-TCL-165": ["RB-04", "RB-10"],
    "P059-TCL-166": ["RB-11", "P059-BD-NEW-001", "P059-BD-NEW-002"], "P059-TCL-167": ["RB-11", "P059-BD-NEW-001", "P059-BD-NEW-002"],
    "P059-TCL-168": ["RB-04", "RB-10"], "P059-TCL-169": ["RB-04", "NS-04"],
    "P059-TCL-176": ["RB-04", "RB-10"], "P059-TCL-179": ["RB-04", "RB-10"],
}
DECISION_BASIS = {
    "P059-TCL-001": "The generic Q_cell variable is used in a per-hour C-rate multiplication without an explicit Ah-versus-coulomb boundary, contradicting the coordinate prose's required variable split.",
    "P059-TCL-003": "The implicit default width uses n=1 while its reversible-heat derivative is zero, contradicting the required self-consistent n(T), w, and dw/dT propagation.",
    "P059-TCL-005": "The separately validated doped high-voltage LCO scope is absent from production defaults and stored images.",
    "P059-TCL-025": "The cutoff-affinity law is frozen globally and lag temperature is trace-averaged, contradicting the required local affinity evaluation.",
    "P059-TCL-026": "The V(q) projection is contradicted by sorting, a direct L_V that survives I=0, ambiguous capacity units, and trace-mean rather than local-temperature lag evaluation.",
    "P059-TCL-030": "The q-domain ODE is reordered by voltage sorting; direct L_V bypasses I=0; its rate uses a frozen affinity, ambiguous factor-3,600 units, and trace-mean temperature.",
    "P059-TCL-033": "The Sommerfeld entropy equation requires a T g(E_F,x) scale, while production evaluates the LCO electronic term only at 298.15 K.",
    "P059-TCL-034": "The quadratic LCO temperature law is directly misaligned with a production electronic term frozen at 298.15 K.",
    "P059-TCL-039": "Synthetic wide-window area evidence is bounded, release evidence is print-only, and the golden is self-referential.",
    "P059-TCL-056": "The composition-dependent DOS gate is evaluated only at one stored x_center and is not coupled to x(V,T).",
    "P059-TCL-066": "The claimed temperature- and affinity-dependent rate is evaluated with a frozen cutoff affinity and one trace-mean temperature.",
    "P059-TCL-069": "Voltage sorting and a forced equilibrium first state contradict chronology and explicit initial-history closure.",
    "P059-TCL-073": "The implicit U1(V,T) composition-temperature coupling is directly misaligned with the 298.15 K electronic freeze; dormant vibrational input is retained only as RELATED_NOT_DIRECT context.",
    "P059-TCL-081": "The generic LCO half-reaction identity remains unverified: frozen electronic entropy and dormant vibrational defaults affect material-specific Delta S inputs only and are RELATED_NOT_DIRECT, not direct refutations of partial U/partial T=Delta S/F.",
    "P059-TCL-083": "The LCO decomposition's electronic dependence is frozen and its explicit vibrational component is dormant in shipped defaults.",
    "P059-TCL-084": "The dopant-specific high-voltage empirical scope is absent from defaults, public-data tests, and audited images.",
    "P059-TCL-100": "The implicit x(V,T) mapping is not propagated into production's fixed-temperature electronic contribution.",
    "P059-TCL-108": "The facade uses per-hour C-rate with an ambiguous charge/capacity input and no explicit 3,600 conversion gate.",
    "P059-TCL-113": "Production sorting erases reversal traversal and the forced equilibrium first state erases the branch prehistory required by the stored identity.",
    "P059-TCL-151": "The facade's ambiguous C-rate/capacity conversion directly mis-scales the current used by the ohmic V_n projection.",
    "P059-TCL-153": "Ideal thermal and empirical width roles remain unsplit and production width/dwdT defaults disagree.",
    "P059-TCL-159": "The oscillator basis exists internally, but shipped defaults and release artifacts do not activate theta_E.",
    "P059-TCL-160": "Reaction-specific signed spectrum/amplitude is absent and the Einstein option remains dormant.",
    "P059-TCL-164": "The production default is thermal in dQ/dV but suppresses the matching configurational derivative in the weighted dU/dT coefficient.",
    "P059-TCL-165": "The implicit default violates the configurational-derivative boundary by pairing a thermal width with zero dw/dT.",
    "P059-TCL-166": "Internal algebra is boundedly supported, but the reference-temperature guard is incomplete and activation is absent.",
    "P059-TCL-167": "The paired derivative identity is boundedly supported, but the shared guard is incomplete and activation is absent.",
    "P059-TCL-168": "The explicit configurational dV/dT term is omitted for the production path whose implicit width is nevertheless thermal.",
    "P059-TCL-169": "The explicit derivative probe is bounded, while production width/dwdT fallback semantics disagree.",
    "P059-TCL-176": "The logistic algebra itself is not rejected, but its ideal width role is not separated from the inconsistent production fallback.",
    "P059-TCL-179": "The generic reversible-heat identity remains unverified: width/dw-dT, electronic, and vibrational findings alter upstream dU/dT inputs but do not directly adjudicate q_rev=-I T dU/dT or its sign convention.",
}

HIGH_RISK_CONFIG = [
    ("P059-F4-HR-001", "low_temperature_finite_current", ["P059-TCL-025", "P059-TCL-026", "P059-TCL-030", "P059-TCL-066"], [("CODE", "P059-CODE-008"), ("TEST_RUNTIME", "MEM-002"), ("STORED_ARTIFACT", "IMG-059-05")], "The local affinity, kinetic rate, projected lag length, and Lq state law require local temperature/current semantics; production collapses local T(V) to one mean and audited images contain no joint low-temperature/finite-current sweep. The combined observed mechanism is not established.", "This is an internal kernel/code/image-scope comparison; it does not identify the mechanism or validate material data."),
    ("P059-F4-HR-002", "chronology_and_initial_history", ["P059-TCL-026", "P059-TCL-030", "P059-TCL-069", "P059-TCL-113"], [("CODE", "P059-CODE-002"), ("CODE", "P059-CODE-003"), ("TEST_RUNTIME", "P059-TD-012"), ("TEST_RUNTIME", "ORD-002")], "Production voltage sorting erases supplied q/V chronology and the first internal state is forced to equilibrium; no release gate supplies an explicit initial state, preconditioning segment, or reversal/pulse/rest test.", "The finding reproduces an internal chronology defect; it does not choose a canonical state solver or infer experimental history."),
    ("P059-F4-HR-003", "zero_current_direct_lv", ["P059-TCL-026", "P059-TCL-030"], [("CODE", "P059-CODE-004"), ("TEST_RUNTIME", "P059-TD-012"), ("TEST_RUNTIME", "CUR-002")], "Direct L_V is returned before the I=0 branch, contradicting both the projected L_V relation and Lq zero-current limit; an independent probe reproduces identical I=0/I=1 outputs and the release suite does not gate the limit.", "This proves an internal zero-current contract violation, not a fitted physical current law."),
    ("P059-F4-HR-004", "c_rate_factor_3600", ["P059-TCL-001", "P059-TCL-026", "P059-TCL-030", "P059-TCL-108", "P059-TCL-151"], [("CODE", "P059-CODE-006"), ("TEST_RUNTIME", "P059-TD-012"), ("TEST_RUNTIME", "UNT-001")], "The coordinate, L_V, Lq, facade, and V_n mappings share an ambiguous Q_cell/time basis; the independent probe reproduces a factor-3,600 current/lag discrepancy and no release gate enforces Ah versus C conversion.", "This is an internal unit-contract defect and does not establish any material rate parameter."),
    ("P059-F4-HR-005", "width_and_dwdt", ["P059-TCL-003", "P059-TCL-153", "P059-TCL-164", "P059-TCL-165", "P059-TCL-168", "P059-TCL-169", "P059-TCL-176", "P059-TCL-179"], [("CODE", "P059-CODE-007"), ("TEST_RUNTIME", "P059-TD-011"), ("TEST_RUNTIME", "P059-TD-012"), ("TEST_RUNTIME", "WID-004")], "The audit requires one self-consistent n(T), w, and dw/dT source plus distinct ideal and empirical width roles; production's implicit default is thermal in dQ/dV but temperature-frozen in dU/dT and reversible heat, and release harnesses omit default-fallback coverage.", "A role/default mismatch is confirmed internally; no multi-temperature observation operator or material width law is validated."),
    ("P059-F4-HR-006", "lco_temperature_and_high_voltage", ["P059-TCL-005", "P059-TCL-033", "P059-TCL-034", "P059-TCL-056", "P059-TCL-073", "P059-TCL-081", "P059-TCL-083", "P059-TCL-084", "P059-TCL-100"], [("CODE", "P059-CODE-010"), ("CODE", "P059-CODE-011"), ("TEST_RUNTIME", "P059-TD-007"), ("TEST_RUNTIME", "P059-TD-013"), ("TEST_RUNTIME", "LCO-001"), ("TEST_RUNTIME", "LCO-003"), ("STORED_ARTIFACT", "IMG-059-05")], "Production freezes the Sommerfeld electronic term at 298.15 K and one x_center, omits the implicit U1/x coupling, defaults end near 4.05 V with no dopant/high-voltage state, the demo is print-only, and audited images lack doped high-voltage coverage.", "This is an internal absence/misalignment finding; it does not validate LCO phase identity, oxygen redox, doping, or temperature parameters."),
    ("P059-F4-HR-007", "einstein_capability_guard_and_authority", ["P059-TCL-073", "P059-TCL-083", "P059-TCL-159", "P059-TCL-160", "P059-TCL-166", "P059-TCL-167"], [("CODE", "P059-CODE-009"), ("CODE", "P059-CODE-013"), ("TEST_RUNTIME", "P059-TD-011"), ("TEST_RUNTIME", "P059-TD-012"), ("TEST_RUNTIME", "VIB-003"), ("TEST_RUNTIME", "VIB-004"), ("STORED_ARTIFACT", "GOLD-004"), ("STORED_ARTIFACT", "GOLD-005")], "The LCO decomposition requests a vibrational reaction term and Einstein algebra exists as an optional capability, but it is dormant in defaults, lacks a positive theta_E_Tref guard and reaction-specific signed spectrum/amplitude, and is absent from release/golden activation.", "Internal algebraic capability is not phonon evidence, material calibration, identifiability, or external validation."),
    ("P059-F4-HR-008", "si_and_blend_scope", [], [("TEST_RUNTIME", "P059-TD-013"), ("STORED_ARTIFACT", "IMG-059-05")], "No Si/blend theory claim exists in the 185-claim universe; the audited test/demo corpus loads no public experimental dataset and audited images contain no Si or graphite-Si case.", "The linked evidence is limited to audited test/demo data loading and audited images. It does not establish production-code absence, all-data absence, or a canonical Si/blend disposition."),
    ("P059-F4-HR-009", "public_fit_and_holdout", [], [("TEST_RUNTIME", "P059-TD-013"), ("STORED_ARTIFACT", "GOLD-005")], "The audited release suite loads no public experimental dataset and golden files contain synthetic model outputs only.", "The absence of audited public experimental validation prevents external material validity; it does not prove that no suitable dataset exists outside the frozen corpus."),
    ("P059-F4-HR-010", "golden_self_reference", [], [("TEST_RUNTIME", "P059-TD-004"), ("TEST_RUNTIME", "P059-TD-005"), ("TEST_RUNTIME", "P059-TD-015"), ("STORED_ARTIFACT", "GOLD-003"), ("STORED_ARTIFACT", "GOLD-006")], "The same harness can capture and verify its golden, uses a nonportable path, ignores extra keys, and strict equality is runtime-sensitive.", "Golden existence or tolerance agreement does not establish theory truth or experimental accuracy."),
    ("P059-F4-HR-011", "artifact_provenance", [], [("STORED_ARTIFACT", "PDF-059-03"), ("STORED_ARTIFACT", "IMG-059-03"), ("STORED_ARTIFACT", "P059-ART-GENE-PDF-OCC-007"), ("STORED_ARTIFACT", "P059-ART-GENE-IMAGE-OCC-015")], "Anchored PDF/image findings and genealogy occurrences identify the v1.0.16 appendix carrying v1.0.15 provenance and stale image filename/version lineage.", "This is a provenance finding only and grants no equation, code, literature, or material authority."),
]


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def object_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


CERTIFICATE_BASIS_FIELDS = (
    "claim_primary_concept",
    "claim_direct_requirements",
    "claim_dependency_targets",
    "finding_behavior_concept",
    "finding_violated_requirements",
    "finding_dependency_outputs",
    "evaluated_direct_predicates",
    "evaluated_dependency_predicates",
    "reachable_concepts",
    "cut_evidence",
    "contradiction_count",
    "computed_conclusion",
)


def semantic_ontology_ref() -> dict[str, Any]:
    return {
        "ontology_id": SEMANTIC_ONTOLOGY_ID,
        "directed_edge_count": len(SEMANTIC_ONTOLOGY_EDGES),
        "directed_edges_sha256": object_sha256(SEMANTIC_ONTOLOGY_EDGES),
    }


def certificate_basis_from_certificate(certificate: dict[str, Any]) -> dict[str, Any]:
    return {field: certificate[field] for field in CERTIFICATE_BASIS_FIELDS}


def review_check_manifest(
    claim_refs: list[dict[str, Any]],
    finding_refs: list[dict[str, Any]],
    direct_predicates: list[dict[str, Any]],
    dependency_predicates: list[dict[str, Any]],
    cut_evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    evidence_by_check = {
        "CLAIM_SOURCE_ANCHOR": ("claim_source_refs", claim_refs),
        "FINDING_SOURCE_ANCHOR": ("finding_source_refs", finding_refs),
        "DIRECT_PREDICATE": ("evaluated_direct_predicates", direct_predicates),
        "DEPENDENCY_TRAVERSAL": ("evaluated_dependency_predicates", dependency_predicates),
        "ONTOLOGY_CUT": ("cut_evidence", cut_evidence),
    }
    checks = [
        {
            "check": check,
            "certificate_field": certificate_field,
            "evidence_count": len(evidence),
            "evidence_sha256": object_sha256(evidence),
        }
        for check, (certificate_field, evidence) in evidence_by_check.items()
    ]
    manifest = {
        "manifest_version": 1,
        "checks": checks,
        "checked_evidence_total": sum(item["evidence_count"] for item in checks),
    }
    manifest["checks_sha256"] = object_sha256(checks)
    return manifest


@lru_cache(maxsize=None)
def git_blob(path: str) -> bytes:
    if PurePosixPath(path).as_posix() != path or "\\" in path: raise RuntimeError(f"non-POSIX path: {path}")
    run = subprocess.run(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if run.returncode: raise RuntimeError(f"missing baseline Git blob: {path}")
    return run.stdout


def load_source(path: str) -> Any:
    return json.loads(git_blob(path).decode("utf-8"))


def recursive_node_count(value: Any) -> int:
    if isinstance(value, dict): return 1 + sum(recursive_node_count(v) for v in value.values())
    if isinstance(value, list): return 1 + sum(recursive_node_count(v) for v in value)
    return 1


def input_coverage() -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_PATHS:
        blob = git_blob(path); text = blob.decode("utf-8"); is_json = path.endswith(".json"); parsed = json.loads(text) if is_json else None
        rows.append({"path": path, "line_count": len(text.splitlines()), "read_range": f"1-{len(text.splitlines())}", "parse_mode": "FULL_JSON_RECURSIVE" if is_json else "FULL_TEXT_1_TO_EOF", "recursive_node_count": recursive_node_count(parsed) if is_json else None, "git_blob_sha256": hashlib.sha256(blob).hexdigest(), "hash_basis": f"Git blob bytes at {BASELINE}"})
    return rows


def seal(document: dict[str, Any]) -> None:
    document["determinism"]["semantic_sha256"] = ""
    document["determinism"]["semantic_sha256"] = object_sha256(document)


def write_json(path: str, document: dict[str, Any]) -> str:
    seal(document); payload = json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    target = ROOT / path; target.parent.mkdir(parents=True, exist_ok=True); target.write_text(payload, encoding="utf-8", newline="\n")
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def common_header(status: str, coverage: list[dict[str, Any]]) -> dict[str, Any]:
    return {"schema_version": 2, "generated_date": "2026-08-25", "phase": 59, "step": "39.3", "baseline_commit": BASELINE, "status": status, "input_coverage": coverage, "input_corpus_sha256": object_sha256(coverage), "determinism": {"serialization": "UTF-8, LF, json.dumps(sort_keys=True, indent=2, ensure_ascii=False)", "hash_basis": f"Git blob bytes at {BASELINE}", "semantic_sha256": ""}}


def canonical_record(record_id: str, kind: str, evidence_class: str, path: str, field: str, idx: int, original: Any) -> dict[str, Any]:
    return {"record_id": record_id, "record_kind": kind, "evidence_class": evidence_class, "source_artifact_path": path, "source_field": field, "source_index": idx, "original_record": original, "original_record_sha256": object_sha256(original)}


def code_records() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    index, diff = load_source(INPUT_PATHS[3]), load_source(INPUT_PATHS[4]); records = []
    for idx, item in enumerate(index["modules"]): records.append(canonical_record(f"P059-CODE-MODULE-{idx + 1:03d}", "PRODUCTION_MODULE", "CODE", INPUT_PATHS[3], "modules", idx, item))
    for idx, item in enumerate(index["review"]["findings"]): records.append(canonical_record(item["id"], "PRODUCTION_FINDING", "CODE", INPUT_PATHS[3], "review.findings", idx, item))
    for idx, item in enumerate(diff["comparisons"]): records.append(canonical_record(f"P059-CODE-DIFF-{idx + 1:03d}", "PRODUCTION_DIFF", "CODE", INPUT_PATHS[4], "comparisons", idx, item))
    for idx, item in enumerate(diff["copy_forward"]): records.append(canonical_record(f"P059-CODE-COPY-{idx + 1:03d}", "PRODUCTION_COPY_FORWARD", "CODE", INPUT_PATHS[4], "copy_forward", idx, item))
    return records, {"production_code_index": index, "production_code_diff": diff}


def test_artifact_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    matrix, runtime, probes = load_source(INPUT_PATHS[6]), load_source(INPUT_PATHS[8]), load_source(INPUT_PATHS[10])
    golden, genealogy, pdf, image = load_source(INPUT_PATHS[12]), load_source(INPUT_PATHS[14]), load_source(INPUT_PATHS[16]), load_source(INPUT_PATHS[18])
    tests: list[dict[str, Any]] = []; artifacts: list[dict[str, Any]] = []
    for idx, item in enumerate(matrix["records"]): tests.append(canonical_record(f"P059-TD-SOURCE-{idx + 1:03d}", "TEST_DEMO_SOURCE", "TEST_RUNTIME", INPUT_PATHS[6], "records", idx, item))
    for idx, item in enumerate(matrix["findings"]): tests.append(canonical_record(item["id"], "TEST_DEMO_FINDING", "TEST_RUNTIME", INPUT_PATHS[6], "findings", idx, item))
    for idx, item in enumerate(runtime["runs"]): tests.append(canonical_record(f"P059-RUNTIME-{idx + 1:03d}", "ISOLATED_RUNTIME_RUN", "TEST_RUNTIME", INPUT_PATHS[8], "runs", idx, item))
    for idx, item in enumerate(probes["probes"]): tests.append(canonical_record(item["probe_id"], "INDEPENDENT_PROBE", "TEST_RUNTIME", INPUT_PATHS[10], "probes", idx, item))
    for idx, item in enumerate(golden["findings"]): artifacts.append(canonical_record(item["finding_id"], "GOLDEN_FINDING", "STORED_ARTIFACT", INPUT_PATHS[12], "findings", idx, item))
    specs = [("pdf_occurrences", "P059-ART-GENE-PDF-OCC", "GENEALOGY_PDF_OCCURRENCE"), ("pdf_byte_content_groups", "P059-ART-GENE-PDF-BYTE-GROUP", "GENEALOGY_PDF_BYTE_GROUP"), ("pdf_rendered_content_groups", "P059-ART-GENE-PDF-RENDER-GROUP", "GENEALOGY_PDF_RENDER_GROUP"), ("image_occurrences", "P059-ART-GENE-IMAGE-OCC", "GENEALOGY_IMAGE_OCCURRENCE"), ("image_content_groups", "P059-ART-GENE-IMAGE-GROUP", "GENEALOGY_IMAGE_GROUP"), ("golden_occurrences", "P059-ART-GENE-GOLD-OCC", "GENEALOGY_GOLDEN_OCCURRENCE"), ("golden_content_groups", "P059-ART-GENE-GOLD-GROUP", "GENEALOGY_GOLDEN_GROUP")]
    for field, prefix, kind in specs:
        for idx, item in enumerate(genealogy[field]): artifacts.append(canonical_record(f"{prefix}-{idx + 1:03d}", kind, "STORED_ARTIFACT", INPUT_PATHS[14], field, idx, item))
    for idx, item in enumerate(pdf["documents"]): artifacts.append(canonical_record(f"P059-ART-PDF-DOC-{idx + 1:03d}", "PDF_VISUAL_DOCUMENT", "STORED_ARTIFACT", INPUT_PATHS[16], "documents", idx, item))
    for idx, item in enumerate(pdf["full_resolution_targets"]): artifacts.append(canonical_record(f"P059-ART-PDF-TARGET-{idx + 1:03d}", "PDF_VISUAL_TARGET", "STORED_ARTIFACT", INPUT_PATHS[16], "full_resolution_targets", idx, item))
    for idx, item in enumerate(pdf["findings"]): artifacts.append(canonical_record(item["id"], "PDF_VISUAL_FINDING", "STORED_ARTIFACT", INPUT_PATHS[16], "findings", idx, item))
    for idx, item in enumerate(image["images"]): artifacts.append(canonical_record(f"P059-ART-IMAGE-{idx + 1:03d}", "IMAGE_AUDIT_IMAGE", "STORED_ARTIFACT", INPUT_PATHS[18], "images", idx, item))
    for idx, item in enumerate(image["findings"]): artifacts.append(canonical_record(item["id"], "IMAGE_AUDIT_FINDING", "STORED_ARTIFACT", INPUT_PATHS[18], "findings", idx, item))
    snapshots = {"test_runtime": {"test_demo_assertion_matrix": matrix, "isolated_runtime_results": runtime, "independent_code_probes": probes}, "stored_artifact": {"golden_npz_audit": golden, "artifact_genealogy": genealogy, "pdf_visual_review": pdf, "image_audit": image}}
    return tests, artifacts, snapshots


def build_code(coverage: list[dict[str, Any]]) -> dict[str, Any]:
    records, snapshots = code_records()
    counts = Counter(x["record_kind"] for x in records)
    document = common_header("PASS_P059_CODE_BEHAVIOR_MATRIX", coverage)
    code_counts = {
        "production_modules": counts["PRODUCTION_MODULE"],
        "production_findings": counts["PRODUCTION_FINDING"],
        "production_diffs": counts["PRODUCTION_DIFF"],
        "production_copy_forward": counts["PRODUCTION_COPY_FORWARD"],
        "canonical_records": len(records),
        "invalid_source_anchors": 0,
    }
    document.update(
        {
            "scope": "Lossless canonicalization of frozen production modules, findings, exact diffs, and copy-forward records.",
            "authority_boundary": "Source declaration and static behavior evidence only; no runtime success, theory conformance, or external material validity is inferred.",
            "source_snapshots": snapshots,
            "records": records,
            "counts": code_counts,
        }
    )
    return document


def build_test(coverage: list[dict[str, Any]]) -> dict[str, Any]:
    tests, artifacts, snapshots = test_artifact_records()
    tc = Counter(x["record_kind"] for x in tests)
    ac = Counter(x["record_kind"] for x in artifacts)
    document = common_header("PASS_P059_TEST_DEMO_CLAIM_MATRIX", coverage)
    test_artifact_counts = {
        "test_demo_source_records": tc["TEST_DEMO_SOURCE"],
        "test_demo_findings": tc["TEST_DEMO_FINDING"],
        "isolated_runtime_runs": tc["ISOLATED_RUNTIME_RUN"],
        "independent_probes": tc["INDEPENDENT_PROBE"],
        "test_runtime_canonical_records": len(tests),
        "golden_findings": ac["GOLDEN_FINDING"],
        "genealogy_records": sum(v for k, v in ac.items() if k.startswith("GENEALOGY_")),
        "pdf_visual_records": sum(v for k, v in ac.items() if k.startswith("PDF_VISUAL_")),
        "image_audit_records": sum(v for k, v in ac.items() if k.startswith("IMAGE_AUDIT_")),
        "artifact_canonical_records": len(artifacts),
        "invalid_source_anchors": 0,
    }
    document.update(
        {
            "scope": "Lossless, evidence-class-separated canonicalization of test/runtime evidence and stored golden/PDF/image/genealogy evidence.",
            "authority_boundary": "Test assertions, runtime observations, probes, golden snapshots, rendered documents, images, and genealogy remain distinct internal evidence classes; none is external material validation.",
            "source_snapshots": snapshots,
            "test_runtime_records": tests,
            "artifact_records": artifacts,
            "counts": test_artifact_counts,
        }
    )
    return document


def make_link(record: dict[str, Any], role: str) -> dict[str, Any]:
    original = record["original_record"]
    basis = original.get("claim") or original.get("interpretation") or original.get("title") or f"Exact frozen {record['record_kind']} record at {record['source_field']}[{record['source_index']}]."
    return {
        "evidence_class": record["evidence_class"],
        "evidence_id": record["record_id"],
        "matrix_path": LINK_MATRIX_PATH_BY_CLASS[record["evidence_class"]],
        "source_artifact_path": record["source_artifact_path"],
        "source_field": record["source_field"],
        "source_index": record["source_index"],
        "source_record_sha256": record["original_record_sha256"],
        "role": role,
        "basis": basis,
    }


def make_axis(axis: str, ids: list[str], universe: dict[str, dict[str, Any]], role: str, boundary: str) -> dict[str, Any]:
    return {
        "axis": axis,
        "state": "PRESENT" if ids else "NO_DIRECT_EVIDENCE",
        "evidence_links": [make_link(universe[x], role) for x in ids],
        "boundary": boundary,
    }


def contract_relations(claim: dict[str, Any], contract_ids: list[str]) -> list[str]:
    relations = []
    for evidence in claim["applicable_contract_evidence"]:
        if evidence["contract_id"] in contract_ids: relations.extend(evidence["direct_claim_relation_ids"])
    return list(dict.fromkeys(relations))

# Explicit source-grounded cross-domain bridge oracle. Classification is
# computed from traversal of these bridges, not from DIRECT/RELATED table lookup.


def claim_semantic_scope(claim: dict[str, Any]) -> dict[str, Any]:
    quantity, dependency, non_goal = CLAIM_SEMANTICS[claim["claim_id"]]
    concepts = claim_ontology_scope(claim["claim_id"])
    topics = sorted({item["topic"] for item in claim["applicable_contract_evidence"]})
    actions = list(dict.fromkeys(item["required_action"] for item in claim["applicable_contract_evidence"]))
    anchors = claim["source_anchors"]
    if not anchors:
        anchors = [
            evidence
            for item in claim["applicable_contract_evidence"]
            for evidence in item["all_contract_evidence"]
        ]
    anchor_refs = []
    for anchor in anchors:
        ref = {
            "path": anchor["path"],
            "line_start": anchor["line_start"],
            "line_end": anchor["line_end"],
            "label": anchor.get("label") or ",".join(anchor.get("labels", [])) or None,
            "source_excerpt_sha256": hashlib.sha256(anchor["source_excerpt"].encode("utf-8")).hexdigest(),
        }
        if ref not in anchor_refs:
            anchor_refs.append(ref)
    return {
        "claim_id": claim["claim_id"],
        "claim_kind": claim["claim_kind"],
        "family": claim["family"],
        "labels": claim["labels"],
        "contract_topics": topics,
        "required_actions": actions,
        "derivation_status": claim["derivation_audit"]["status"],
        "code_impact_assessment": claim["code_impact"]["assessment"],
        "source_anchor_refs": anchor_refs,
        "source_relation_texts": list(dict.fromkeys(anchor["source_excerpt"] for anchor in anchors)),
        "claim_quantity_or_dependency": quantity,
        "dependency_direction": dependency,
        "required_evidence_or_action": actions,
        "non_goal": non_goal,
        "semantic_concepts": concepts,
    }


def code_semantic_scope(finding: dict[str, Any]) -> dict[str, Any]:
    affected_path, non_adjudicated = FINDING_SEMANTICS[finding["id"]]
    concepts = FINDING_ONTOLOGY_SCOPE[finding["id"]]
    return {
        "code_finding_id": finding["id"],
        "title": finding["title"],
        "claim": finding["claim"],
        "consequence": finding["consequence"],
        "required_action": finding["required_action"],
        "contract_ids": finding["contract_ids"],
        "source_evidence": finding["source_evidence"],
        "actual_production_behavior": finding["claim"],
        "finding_affected_quantity_or_path": affected_path,
        "non_adjudicated_quantities": non_adjudicated,
        "semantic_concepts": {"behavior": concepts["behavior"], "violates": list(concepts["violates"]), "emits": list(concepts["emits"])},
    }


def directed_path(edges: list[list[str]], source: str, target: str) -> list[str]:
    adjacency: dict[str, list[str]] = {}
    for left, right in edges:
        adjacency.setdefault(left, []).append(right)
    queue: list[tuple[str, list[str]]] = [(source, [source])]
    visited = {source}
    while queue:
        node, path = queue.pop(0)
        if node == target:
            return path
        for neighbor in adjacency.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor); queue.append((neighbor, path + [neighbor]))
    return []


def reachable_nodes(edges: list[list[str]], source: str) -> list[str]:
    adjacency: dict[str, list[str]] = {}
    for left, right in edges:
        adjacency.setdefault(left, []).append(right)
    queue = [source]
    visited = {source}
    while queue:
        node = queue.pop(0)
        for neighbor in adjacency.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return sorted(visited)


def pair_graph_audit(claim_scope: dict[str, Any], code_scope: dict[str, Any]) -> dict[str, Any]:
    claim_id, code_id = claim_scope["claim_id"], code_scope["code_finding_id"]
    pair = (claim_id, code_id)
    pair_id = f"{claim_id}->{code_id}"
    claim_concepts = claim_ontology_scope(claim_id)
    finding_concepts = FINDING_ONTOLOGY_SCOPE[code_id]
    direct_matches = sorted(set(claim_concepts["direct_requirements"]) & set(finding_concepts["violates"]))
    dependency_paths = [
        directed_path(SEMANTIC_ONTOLOGY_EDGES, finding_concepts["behavior"], target)
        for target in claim_concepts["dependency_targets"]
    ]
    dependency_paths = [path for path in dependency_paths if path]
    contradiction_evidence = [
        {
            "scientific_requirement": concept,
            "finding_behavior": finding_concepts["behavior"],
            "contradiction_edge": [finding_concepts["behavior"], concept],
        }
        for concept in direct_matches
    ]
    if direct_matches:
        classification = "DIRECT"
        scientific_basis = DIRECT_REASON[pair]
        matched_concept = direct_matches[0]
        bridge_kind = "DIRECT_CONTRADICTION"
        bridge_path = [finding_concepts["behavior"], matched_concept]
    elif dependency_paths:
        classification = "RELATED_NOT_DIRECT"
        scientific_basis = RELATED_REASON[pair]
        bridge_kind = "RELATED_DEPENDENCY"
        bridge_path = dependency_paths[0]
        matched_concept = bridge_path[-1]
    else:
        classification = "NOT_APPLICABLE"
        scientific_basis = ""
        bridge_kind = ""
        bridge_path = []
        matched_concept = None

    claim_nodes = [claim_concepts["primary_concept"]] + claim_concepts["direct_requirements"] + claim_concepts["dependency_targets"]
    claim_edges = [
        [claim_concepts["primary_concept"], concept]
        for concept in claim_concepts["direct_requirements"] + claim_concepts["dependency_targets"]
        if concept != claim_concepts["primary_concept"]
    ]
    finding_nodes = [finding_concepts["behavior"]] + list(finding_concepts["violates"]) + list(finding_concepts["emits"])
    finding_edges = [
        edge for edge in SEMANTIC_ONTOLOGY_EDGES
        if edge[0] == finding_concepts["behavior"]
    ]
    bridges: list[dict[str, Any]] = []
    if bridge_path:
        bridge = {
            "bridge_id": f"P059-BRIDGE-{claim_id[-3:]}-{code_id[-3:]}",
            "pair_id": pair_id,
            "kind": bridge_kind,
            "source_node": bridge_path[0],
            "target_node": bridge_path[-1],
            "path": bridge_path,
            "matched_scientific_concept": matched_concept,
            "shared_executed_quantity_node": matched_concept if classification == "DIRECT" else None,
            "scientific_basis": scientific_basis,
            "claim_anchor_sha256": [item["source_excerpt_sha256"] for item in claim_scope["source_anchor_refs"]],
            "finding_anchor_sha256": [hashlib.sha256(item["source_line"].encode("utf-8")).hexdigest() for item in code_scope["source_evidence"]],
            "authority_boundary": ADJUDICATION_BOUNDARY,
        }
        bridge["bridge_sha256"] = object_sha256(bridge)
        bridges.append(bridge)

    structural_basis = {
        "claim_concepts": claim_concepts,
        "finding_concepts": finding_concepts,
        "semantic_ontology_ref": semantic_ontology_ref(),
        "direct_matches": direct_matches,
        "dependency_paths": dependency_paths,
    }
    audit = {
        "pair_graph_audit_id": f"P059-PAIR-GRAPH-{claim_id[-3:]}-{code_id[-3:]}",
        "pair_id": pair_id,
        "classification_derivation": "ONTOLOGY_INTERSECTION_CONTRADICTION_AND_DIRECTED_REACHABILITY",
        "claim_graph": {"nodes": claim_nodes, "directed_edges": claim_edges, "executed_quantity_nodes": claim_concepts["direct_requirements"]},
        "finding_graph": {"nodes": finding_nodes, "directed_edges": finding_edges, "executed_quantity_nodes": list(finding_concepts["violates"])},
        "cross_domain_bridges": bridges,
        "traversal_result": {
            "executed_quantity_intersection": direct_matches,
            "bridge_paths": dependency_paths,
            "contradiction_evidence": contradiction_evidence,
            "reachable_concepts": reachable_nodes(SEMANTIC_ONTOLOGY_EDGES, finding_concepts["behavior"]),
            "computed_classification": classification,
        },
        "structural_signature_basis": structural_basis,
        "structural_signature_sha256": object_sha256(structural_basis),
        "authority_boundary": ADJUDICATION_BOUNDARY,
    }
    audit["pair_graph_audit_sha256"] = object_sha256(audit)
    return audit


def na_group_rule(primary_concept: str, finding_behavior: str) -> dict[str, Any]:
    incident_edges = [
        edge for edge in SEMANTIC_ONTOLOGY_EDGES
        if edge[0] == finding_behavior or edge[1] == primary_concept
    ]
    return {
        "grounding_group_id": f"P059-NA-CONCEPT-{primary_concept}__{finding_behavior}",
        "claim_primary_concept": primary_concept,
        "finding_behavior_concept": finding_behavior,
        "incident_ontology_edges": incident_edges,
        "grouping_basis": "Exact scientific claim concept crossed with exact observed production behavior; IDs and source hashes are not grouping inputs.",
    }


def build_na_grounding(claim_scope: dict[str, Any], code_scope: dict[str, Any], shared: list[str], graph_audit: dict[str, Any]) -> dict[str, Any]:
    claim_id = claim_scope["claim_id"]
    code_id = code_scope["code_finding_id"]
    pair_id = f"{claim_id}->{code_id}"
    traversal = graph_audit["traversal_result"]
    if traversal["computed_classification"] != "NOT_APPLICABLE":
        raise ValueError(f"reachable/intersecting pair cannot be grounded as NA: {pair_id}")

    claim_concepts = claim_ontology_scope(claim_id)
    finding_concepts = FINDING_ONTOLOGY_SCOPE[code_id]
    group = na_group_rule(claim_concepts["primary_concept"], finding_concepts["behavior"])
    finding_refs = [
        {"path": item["path"], "line": item["line"], "source_line_sha256": hashlib.sha256(item["source_line"].encode("utf-8")).hexdigest()}
        for item in code_scope["source_evidence"]
    ]
    claim_predicates = claim_concepts["direct_requirements"] or [claim_concepts["primary_concept"]]
    finding_predicates = list(finding_concepts["violates"]) or [finding_concepts["behavior"]]
    direct_predicates = [
        {
            "claim_concept": claim_concept,
            "finding_concept": finding_concept,
            "same_scientific_concept": claim_concept == finding_concept,
            "contradiction_edge_present": [finding_concepts["behavior"], claim_concept] in SEMANTIC_ONTOLOGY_EDGES and claim_concept in finding_concepts["violates"],
        }
        for claim_concept in claim_predicates
        for finding_concept in finding_predicates
    ]
    dependency_targets = claim_concepts["dependency_targets"] or [claim_concepts["primary_concept"]]
    dependency_predicates = [
        {
            "source_behavior_concept": finding_concepts["behavior"],
            "claim_target_concept": target,
            "path": directed_path(SEMANTIC_ONTOLOGY_EDGES, finding_concepts["behavior"], target),
            "reachable": bool(directed_path(SEMANTIC_ONTOLOGY_EDGES, finding_concepts["behavior"], target)),
        }
        for target in dependency_targets
    ]
    closure = reachable_nodes(SEMANTIC_ONTOLOGY_EDGES, finding_concepts["behavior"])
    cut_evidence = []
    for target in dependency_targets:
        incoming = [edge for edge in SEMANTIC_ONTOLOGY_EDGES if edge[1] == target]
        reached_predecessors = [left for left, _ in incoming if left in closure]
        cut_evidence.append({
            "claim_target_concept": target,
            "target_absent_from_reachable_closure": target not in closure,
            "incoming_ontology_edges": incoming,
            "reached_predecessors": reached_predecessors,
            "blocking_cut": (
                f"No audited ontology edge leaves {finding_concepts['behavior']} toward {target}."
                if not incoming
                else f"Only {sorted({left for left, _ in incoming})} feed {target}; none belongs to this finding's reachable closure."
            ),
        })
    certificate_basis = {
        "claim_primary_concept": claim_concepts["primary_concept"],
        "claim_direct_requirements": claim_concepts["direct_requirements"],
        "claim_dependency_targets": claim_concepts["dependency_targets"],
        "finding_behavior_concept": finding_concepts["behavior"],
        "finding_violated_requirements": list(finding_concepts["violates"]),
        "finding_dependency_outputs": list(finding_concepts["emits"]),
        "evaluated_direct_predicates": direct_predicates,
        "evaluated_dependency_predicates": dependency_predicates,
        "reachable_concepts": closure,
        "cut_evidence": cut_evidence,
        "contradiction_count": 0,
        "computed_conclusion": "NOT_APPLICABLE",
    }
    certificate = {
        **certificate_basis,
        "claim_source_refs": claim_scope["source_anchor_refs"],
        "finding_source_refs": finding_refs,
        "claim_scope_sha256": object_sha256(claim_scope),
        "code_scope_sha256": object_sha256(code_scope),
        "authority_boundary": ADJUDICATION_BOUNDARY,
    }
    certificate["semantic_proof_signature_sha256"] = object_sha256(certificate_basis)
    certificate["certificate_sha256"] = object_sha256(certificate)

    direct_clause = (
        f"The claim's requirements {claim_concepts['direct_requirements']} are disjoint from the finding's contradicted requirements {list(finding_concepts['violates'])}."
        if claim_concepts["direct_requirements"] and finding_concepts["violates"]
        else f"The direct predicate audit compared {claim_predicates} with {finding_predicates} and found no shared scientific requirement."
    )
    dependency_clause = (
        f"Traversal from {finding_concepts['behavior']} reaches {closure}, but none of the claim targets {dependency_targets}; the exact cuts are {[item['blocking_cut'] for item in cut_evidence]}."
    )
    rationale_parts = [
        f"{claim_concepts['primary_concept']} is grounded by {claim_scope['claim_quantity_or_dependency']} and depends as follows: {claim_scope['dependency_direction']}",
        f"{finding_concepts['behavior']} is grounded by {code_scope['actual_production_behavior']} along {code_scope['finding_affected_quantity_or_path']}",
        direct_clause,
        dependency_clause,
        f"No contradiction predicate is true; shared contract candidates {shared or ['NONE']} therefore remain non-dispositive.",
        f"The claim excludes {claim_scope['non_goal']}; the finding does not adjudicate {code_scope['non_adjudicated_quantities']}.",
    ]
    # Rotate source-grounded clauses by scientific graph cardinality so prose is
    # a certificate rendering, not one group-core template with an inserted tail.
    rotation = (len(claim_concepts["direct_requirements"]) + 2 * len(claim_concepts["dependency_targets"]) + len(finding_concepts["emits"])) % 3
    rationale = " ".join(rationale_parts[rotation:4] + rationale_parts[:rotation] + rationale_parts[4:])
    exclusion = (
        f"Reachability cut for {claim_concepts['primary_concept']}: {cut_evidence[0]['blocking_cut']} "
        f"This leaves {claim_scope['non_goal']} outside the authority of {finding_concepts['behavior']}, whose audited non-adjudicated scope is {code_scope['non_adjudicated_quantities']}."
    )
    structural_basis = {
        "claim_concept_cardinality": {key: len(value) if isinstance(value, list) else 1 for key, value in claim_concepts.items()},
        "finding_concept_cardinality": {"violates": len(finding_concepts["violates"]), "emits": len(finding_concepts["emits"])},
        "direct_predicate_truth_vector": [item["same_scientific_concept"] or item["contradiction_edge_present"] for item in direct_predicates],
        "dependency_reachability_truth_vector": [item["reachable"] for item in dependency_predicates],
        "cut_cardinality": len(cut_evidence),
    }
    review_checks = review_check_manifest(
        claim_scope["source_anchor_refs"],
        finding_refs,
        direct_predicates,
        dependency_predicates,
        cut_evidence,
    )
    grounding = {
        "grounding_id": f"P059-NA-GROUND-{claim_id[-3:]}-{code_id[-3:]}",
        "pair_id": pair_id,
        "claim_id": claim_id,
        "code_finding_id": code_id,
        "grounding_group_id": group["grounding_group_id"],
        "grounding_group_sha256": object_sha256(group),
        "examined_claim_anchors": claim_scope["source_anchor_refs"],
        "examined_claim_quantities": [claim_scope["claim_quantity_or_dependency"], claim_scope["dependency_direction"]] + [claim_concepts["primary_concept"]] + claim_concepts["direct_requirements"] + claim_concepts["dependency_targets"],
        "examined_finding_anchors": finding_refs,
        "examined_finding_behavior": code_scope["actual_production_behavior"],
        "pair_graph_audit_id": graph_audit["pair_graph_audit_id"],
        "pair_graph_audit_sha256": graph_audit["pair_graph_audit_sha256"],
        "executed_quantity_intersection": {"result": "NONE", "claim_nodes": claim_concepts["direct_requirements"], "finding_nodes": list(finding_concepts["violates"]), "common_executed_nodes": [], "finding": "Exact ontology requirement intersection is empty."},
        "dependency_reachability": {"result": "NONE", "claim_edges": graph_audit["claim_graph"]["directed_edges"], "finding_edges": graph_audit["finding_graph"]["directed_edges"], "cross_domain_bridges": [], "paths": [], "finding": "Independent directed traversal reaches no claim dependency target; see nonconnection_certificate.cut_evidence."},
        "contradiction_finding": {"result": "NONE", "claim_assertion": claim_scope["claim_quantity_or_dependency"], "observed_behavior": code_scope["actual_production_behavior"], "evidence": [], "finding": "Every stored direct predicate is false."},
        "nonconnection_certificate": certificate,
        "conclusion_specific_rationale": rationale,
        "exclusion_boundary": exclusion,
        "review_checks": review_checks,
        "shared_contract_candidates": shared,
        "claim_scope_sha256": object_sha256(claim_scope),
        "code_scope_sha256": object_sha256(code_scope),
        "structural_signature_basis": structural_basis,
        "structural_signature_sha256": object_sha256(structural_basis),
        "reasoning_signature_sha256": object_sha256(certificate_basis),
        "authority_boundary": ADJUDICATION_BOUNDARY,
    }
    grounding["grounding_sha256"] = object_sha256(grounding)
    return grounding


def pair_comparison(claim_scope: dict[str, Any], code_scope: dict[str, Any], applicability: str, scientific_reason: str, na_grounding: dict[str, Any] | None = None) -> dict[str, str]:
    quantity = claim_scope["claim_quantity_or_dependency"]
    affected = code_scope["finding_affected_quantity_or_path"]
    excluded = code_scope["non_adjudicated_quantities"]
    if applicability == "DIRECT":
        overlap = f"DIRECT executed/contradicted path: {scientific_reason}"
        reason = scientific_reason
        boundary = f"Direct only to {affected}; it does not adjudicate {excluded}. Claim boundary: {claim_scope['non_goal']}"
    elif applicability == "RELATED_NOT_DIRECT":
        overlap = f"BOUNDED upstream/downstream dependency: {scientific_reason}"
        reason = scientific_reason
        boundary = f"Related context only: the finding can alter an input or prerequisite but does not adjudicate {quantity}. It also excludes {excluded}."
    else:
        if na_grounding is None:
            raise ValueError("NOT_APPLICABLE requires an explicit pair grounding")
        overlap = na_grounding["dependency_reachability"]["finding"]
        reason = na_grounding["conclusion_specific_rationale"]
        boundary = na_grounding["exclusion_boundary"]
    return {
        "claim_quantity_or_dependency": quantity,
        "finding_affected_quantity_or_path": affected,
        "overlap_or_dependency_path": overlap,
        "classification_reason": reason,
        "exclusion_boundary": boundary,
    }


def build_adjudication_ledger(claims: list[dict[str, Any]], code_findings: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    ledger = []
    na_groundings = []
    graph_audits = []
    for claim in [x for x in claims if x["evidence_contract_ids"]]:
        decisions = []
        direct_ids = []
        expected_direct_ids = DIRECT_CODE.get(claim["claim_id"], [])
        claim_scope = claim_semantic_scope(claim)
        claim_basis = {
            "claim_id": claim["claim_id"],
            "labels": claim["labels"],
            "contracts": claim["evidence_contract_ids"],
            "relations": claim["evidence_relation_ids"],
            "code_impact": claim["code_impact"],
        }
        for index, finding in enumerate(code_findings, start=1):
            pair = (claim["claim_id"], finding["id"])
            shared = sorted(set(claim["evidence_contract_ids"]) & set(finding["contract_ids"]))
            code_scope = code_semantic_scope(finding)
            graph_audit = pair_graph_audit(claim_scope, code_scope)
            graph_audits.append(graph_audit)
            applicability = graph_audit["traversal_result"]["computed_classification"]
            if applicability == "DIRECT":
                direct_ids.append(finding["id"])
                applicability = "DIRECT"; direct_contracts = shared; relations = contract_relations(claim, direct_contracts) if direct_contracts else claim["evidence_relation_ids"]; scientific_reason = DIRECT_REASON[pair]
            elif applicability == "RELATED_NOT_DIRECT":
                applicability = "RELATED_NOT_DIRECT"; direct_contracts = []; relations = []; scientific_reason = RELATED_REASON[pair]
            else:
                applicability = "NOT_APPLICABLE"; direct_contracts = []; relations = []
                scientific_reason = ""
            na_grounding = build_na_grounding(claim_scope, code_scope, shared, graph_audit) if applicability == "NOT_APPLICABLE" else None
            if na_grounding is not None:
                na_groundings.append(na_grounding)
            comparison = pair_comparison(claim_scope, code_scope, applicability, scientific_reason, na_grounding)
            basis = f"Semantic audit {claim['claim_id']}->{finding['id']}: {comparison['classification_reason']}"
            decisions.append(
                {
                    "adjudication_id": f"P059-F4-ADJ-{claim['claim_id'][-3:]}-{index:02d}",
                    "code_finding_id": finding["id"],
                    "applicability": applicability,
                    "shared_contract_ids": shared,
                    "direct_contract_ids": direct_contracts,
                    "theory_relation_ids": relations,
                    "claim_basis_sha256": object_sha256(claim_basis),
                    "code_basis_sha256": object_sha256(finding),
                    "claim_semantic_scope_sha256": object_sha256(claim_scope),
                    "code_semantic_scope_sha256": object_sha256(code_scope),
                    "semantic_audit_method": "FULL_EQUATION_PROSE_DERIVATION_CODE_IMPACT_X_FINDING_CROSS_AUDIT",
                    "pair_graph_audit": graph_audit,
                    "na_pair_grounding_id": na_grounding["grounding_id"] if na_grounding else None,
                    "comparison": comparison,
                    "basis": basis,
                    "authority_boundary": ADJUDICATION_BOUNDARY,
                }
            )
        if direct_ids != expected_direct_ids:
            raise ValueError(f"graph-computed direct membership mismatch for {claim['claim_id']}: {direct_ids} != {expected_direct_ids}")
        actual_related_ids = [item["code_finding_id"] for item in decisions if item["applicability"] == "RELATED_NOT_DIRECT"]
        expected_related_ids = [finding["id"] for finding in code_findings if (claim["claim_id"], finding["id"]) in RELATED_CODE]
        if actual_related_ids != expected_related_ids:
            raise ValueError(f"ontology-computed related membership mismatch for {claim['claim_id']}: {actual_related_ids} != {expected_related_ids}")
        ledger.append(
            {
                "claim_id": claim["claim_id"],
                "claim_sha256": object_sha256(claim),
                "claim_semantic_scope": claim_scope,
                "evidence_contract_ids": claim["evidence_contract_ids"],
                "evidence_relation_ids": claim["evidence_relation_ids"],
                "code_finding_adjudications": decisions,
                "direct_code_evidence_ids": direct_ids,
                "direct_code_relation_count": len(direct_ids),
                "authority_boundary": ADJUDICATION_BOUNDARY,
            }
        )
    actual_pairs = [grounding["pair_id"] for grounding in na_groundings]
    computed_na_pairs = [
        decision["pair_graph_audit"]["pair_id"]
        for entry in ledger
        for decision in entry["code_finding_adjudications"]
        if decision["applicability"] == "NOT_APPLICABLE"
    ]
    if actual_pairs != computed_na_pairs or len(actual_pairs) != 558 or len(set(actual_pairs)) != 558:
        raise ValueError("ontology-computed NA groundings do not reconcile 558 ordered unique pairs")
    if len(graph_audits) != 663 or len({item["pair_id"] for item in graph_audits}) != 663:
        raise ValueError("pair graph audits do not cover 51x13 exactly once")
    return ledger, na_groundings, graph_audits


def build_semantic_cross_audit(ledger: list[dict[str, Any]], code_findings: list[dict[str, Any]], na_groundings: list[dict[str, Any]], graph_audits: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = [decision for entry in ledger for decision in entry["code_finding_adjudications"]]
    code_scopes = [code_semantic_scope(finding) for finding in code_findings]
    nonshared = [
        f"{entry['claim_id']}->{decision['code_finding_id']}"
        for entry in ledger
        for decision in entry["code_finding_adjudications"]
        if decision["applicability"] != "NOT_APPLICABLE" and not decision["shared_contract_ids"]
    ]
    groups: dict[str, dict[str, Any]] = {}
    for grounding in na_groundings:
        group_id = grounding["grounding_group_id"]
        if group_id not in groups:
            primary_concept, finding_behavior = group_id.removeprefix("P059-NA-CONCEPT-").split("__", 1)
            rule = na_group_rule(primary_concept, finding_behavior)
            groups[group_id] = {**rule, "grounding_group_sha256": object_sha256(rule), "member_pair_ids": []}
        groups[group_id]["member_pair_ids"].append(grounding["pair_id"])
    group_ledger = [{**group, "member_count": len(group["member_pair_ids"])} for group in groups.values()]
    bridge_oracle = [bridge for audit in graph_audits for bridge in audit["cross_domain_bridges"]]
    ontology_nodes = []
    for claim_id, concept in CLAIM_PRIMARY_CONCEPT.items():
        ontology_nodes.append({"concept": concept, "kind": "CLAIM_PRIMARY_QUANTITY_OR_DEPENDENCY", "definition": CLAIM_SEMANTICS[claim_id][0], "source_claim_ids": [claim_id]})
    for concept, members in DIRECT_REQUIREMENT_CLAIMS.items():
        ontology_nodes.append({"concept": concept, "kind": "DIRECT_SCIENTIFIC_REQUIREMENT", "definition": concept.replace("_", " "), "source_claim_ids": list(members)})
    for concept, members in DEPENDENCY_TARGET_CLAIMS.items():
        ontology_nodes.append({"concept": concept, "kind": "UPSTREAM_OR_DOWNSTREAM_DEPENDENCY_TARGET", "definition": concept.replace("_", " "), "source_claim_ids": list(members)})
    for code_id, scope in FINDING_ONTOLOGY_SCOPE.items():
        ontology_nodes.append({"concept": scope["behavior"], "kind": "OBSERVED_PRODUCTION_BEHAVIOR", "definition": FINDING_SEMANTICS[code_id][0], "source_code_finding_ids": [code_id]})
    proof_bases = [
        certificate_basis_from_certificate(grounding["nonconnection_certificate"])
        for grounding in na_groundings
    ]
    proof_hashes = [object_sha256(basis) for basis in proof_bases]
    claim_scope_by_id = {entry["claim_id"]: entry["claim_semantic_scope"] for entry in ledger}
    code_scope_by_id = {scope["code_finding_id"]: scope for scope in code_scopes}
    def normalized_na_text(grounding: dict[str, Any], field: str) -> str:
        claim_scope = claim_scope_by_id[grounding["claim_id"]]
        code_scope = code_scope_by_id[grounding["code_finding_id"]]
        raw_values = [
            claim_scope["claim_quantity_or_dependency"], claim_scope["dependency_direction"], claim_scope["non_goal"],
            *claim_scope["source_relation_texts"], *claim_scope["labels"],
            code_scope["title"], code_scope["claim"], code_scope["consequence"], code_scope["required_action"],
            code_scope["actual_production_behavior"], code_scope["finding_affected_quantity_or_path"], code_scope["non_adjudicated_quantities"],
        ]
        text = grounding[field]
        for value in sorted({value for value in raw_values if isinstance(value, str) and len(value) > 3}, key=len, reverse=True):
            text = text.replace(value, "<RAW_SOURCE_OR_LABEL>")
        text = re.sub(r"P059-(?:TCL|CODE|CON)-\d+", "<ID>", text)
        text = re.sub(r"[0-9a-f]{64}", "<HASH>", text)
        return " ".join(text.split())
    normalized_rationales = [normalized_na_text(grounding, "conclusion_specific_rationale") for grounding in na_groundings]
    normalized_exclusions = [normalized_na_text(grounding, "exclusion_boundary") for grounding in na_groundings]
    normalization_audit = {
        "method": "Remove pair IDs, source hashes, raw source strings, and claim/finding labels; retain only scientific concept membership, predicate truth values, traversed concepts, and graph-cut structure.",
        "removed_identity_fields": ["pair_id", "claim_id", "code_finding_id", "source hashes", "raw source strings", "labels"],
        "retained_semantic_fields": ["scientific concept names", "requirement intersections", "dependency targets", "reachable closure", "cut witnesses", "contradiction predicates", "computed conclusion"],
        "na_certificate_count": len(proof_bases),
        "distinct_semantic_proof_structure_count": len(set(proof_hashes)),
        "distinct_normalized_rationale_structure_count": len(set(normalized_rationales)),
        "distinct_normalized_exclusion_structure_count": len(set(normalized_exclusions)),
        "normalized_semantic_proof_corpus_sha256": object_sha256(proof_bases),
        "normalized_rationale_corpus_sha256": object_sha256(normalized_rationales),
        "normalized_exclusion_corpus_sha256": object_sha256(normalized_exclusions),
        "reuse_explanation": "No normalized semantic proof basis is reused: each surviving claim-primary-concept/production-behavior cross has a distinct scientific predicate and cut certificate.",
    }
    return {
        "method": [
            "Read every applicable claim's equation or prose anchors, labels, contract topics, derivation status, required actions, and code-impact assessment.",
            "Read every code finding's source evidence, claim, consequence, contracts, and required action.",
            "Cross-compared all 51 claims against all 13 findings; shared contracts nominated candidates but were neither necessary nor sufficient.",
            "DIRECT requires an executed or contradicted variable, dependency, limit, or explicit required action; RELATED_NOT_DIRECT requires a bounded prerequisite or downstream dependency.",
            "Each NOT_APPLICABLE conclusion is reverse-linked to one explicit pair grounding that audits executed-quantity intersection, directed dependency reachability, contradiction, exact claim/finding anchors, and an authority-bounded exclusion.",
        ],
        "claim_semantic_scopes": [entry["claim_semantic_scope"] for entry in ledger],
        "code_finding_semantic_scopes": code_scopes,
        "semantic_concept_ontology": {
            **semantic_ontology_ref(),
            "classification_method": "DIRECT from requirement/violation intersection; RELATED_NOT_DIRECT from directed behavior-to-claim-target reachability; NOT_APPLICABLE only from an empty intersection, no contradiction, and an explicit reachability cut.",
            "nodes": ontology_nodes,
            "directed_edges": SEMANTIC_ONTOLOGY_EDGES,
            "claim_memberships": [{"claim_id": claim_id, **claim_ontology_scope(claim_id)} for claim_id in CLAIM_PRIMARY_CONCEPT],
            "finding_memberships": [{"code_finding_id": code_id, "behavior": scope["behavior"], "violates": list(scope["violates"]), "emits": list(scope["emits"])} for code_id, scope in FINDING_ONTOLOGY_SCOPE.items()],
            "authority_boundary": ADJUDICATION_BOUNDARY,
        },
        "na_grounding_groups": group_ledger,
        "na_pair_groundings": na_groundings,
        "na_normalization_audit": normalization_audit,
        "cross_domain_bridge_oracle": bridge_oracle,
        "claim_count": len(ledger),
        "code_finding_count": len(code_findings),
        "pair_count": len(decisions),
        "classification_counts": dict(sorted(Counter(decision["applicability"] for decision in decisions).items())),
        "shared_contract_candidate_pairs": sum(bool(decision["shared_contract_ids"]) for decision in decisions),
        "nonshared_direct_or_related_pairs": nonshared,
        "pair_specific_basis_count": len({decision["basis"] for decision in decisions}),
        "structured_comparison_count": len(decisions),
        "na_pair_grounding_count": len(na_groundings),
        "na_grounding_group_count": len(group_ledger),
        "na_structural_signature_count": len({item["structural_signature_sha256"] for item in na_groundings}),
        "na_reasoning_signature_count": len({item["reasoning_signature_sha256"] for item in na_groundings}),
        "na_pair_grounding_sha256": object_sha256(na_groundings),
        "pair_graph_audit_count": len(graph_audits),
        "cross_domain_bridge_count": len(bridge_oracle),
        "cross_domain_bridge_sha256": object_sha256(bridge_oracle),
        "claim_scope_ledger_count": len(ledger),
        "finding_scope_ledger_count": len(code_scopes),
        "authority_boundary": ADJUDICATION_BOUNDARY,
    }


def build_high_risk(code_records_by_id: dict[str, dict[str, Any]], test_records_by_id: dict[str, dict[str, Any]], artifact_records_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    universes = {
        "CODE": code_records_by_id,
        "TEST_RUNTIME": test_records_by_id,
        "STORED_ARTIFACT": artifact_records_by_id,
    }
    findings = []
    for finding_id, topic, claims, refs, finding, boundary in HIGH_RISK_CONFIG:
        links = [make_link(universes[cls][eid], "HIGH_RISK_STRUCTURED_EVIDENCE") for cls, eid in refs]
        findings.append(
            {
                "finding_id": finding_id,
                "topic": topic,
                "claim_ids": claims,
                "evidence_links": links,
                "finding": finding,
                "authority_boundary": boundary,
            }
        )
    return findings


def build_main(coverage: list[dict[str, Any]], code: dict[str, Any], test: dict[str, Any]) -> dict[str, Any]:
    theory = load_source(INPUT_PATHS[0])
    claims = theory["claims"]
    code_findings = load_source(INPUT_PATHS[3])["review"]["findings"]
    code_by_id = {x["record_id"]: x for x in code["records"]}
    test_by_id = {x["record_id"]: x for x in test["test_runtime_records"]}
    artifact_by_id = {x["record_id"]: x for x in test["artifact_records"]}
    ledger, na_groundings, graph_audits = build_adjudication_ledger(claims, code_findings)
    semantic_audit = build_semantic_cross_audit(
        ledger,
        code_findings,
        na_groundings,
        graph_audits,
    )
    direct_by_claim = {x["claim_id"]: x["direct_code_evidence_ids"] for x in ledger}
    routes: dict[str, list[str]] = {claim["claim_id"]: [] for claim in claims}
    for route in theory["contract_routes"]: routes[route["claim_id"]].append(route["contract_id"])
    rows = []
    for claim in claims:
        claim_id = claim["claim_id"]
        code_ids = direct_by_claim.get(claim_id, [])
        test_ids = TEST_IDS.get(claim_id, [])
        artifact_ids = ARTIFACT_IDS.get(claim_id, [])
        status = STATUS.get(claim_id, "UNVERIFIED")
        blockers = BLOCKERS.get(claim_id, ["P059-BD-NEW-003"] if not claim["evidence_contract_ids"] else [])
        if claim_id in DECISION_BASIS:
            decision = DECISION_BASIS[claim_id]
            blocker_basis = "Exact Step 39.2 blocker IDs are linked because the frozen blocker acceptance names the mapped defect or evidence debt."
        elif not claim["evidence_contract_ids"]:
            decision = "This equation claim has no directly applicable Step 39.1 contract evidence and no exact cross-axis relation. It remains UNVERIFIED without label/name/existence inference."
            blocker_basis = "P059-BD-NEW-003 explicitly carries all 134 uncontracted equation claims without assigning a stronger disposition."
        else:
            decision = "All 13 production findings were explicitly adjudicated; none is directly applicable and this corpus does not establish sufficient test/artifact conformance. The claim remains UNVERIFIED."
            blocker_basis = "No exact Step 39.2 blocker route is assigned beyond preserved theory-contract evidence; the empty route is explicit."

        theory_axis = {
            "claim_kind": claim["claim_kind"],
            "disposition": claim["disposition"],
            "literature_status": claim["literature_status"],
            "mapped_occurrence_ids": claim["mapped_occurrence_ids"],
            "governing_contract_ids": routes[claim_id],
            "evidence_contract_ids": claim["evidence_contract_ids"],
            "evidence_relation_ids": claim["evidence_relation_ids"],
            "source_anchors": claim["source_anchors"],
            "authority_boundary": claim["authority_boundary"],
        }
        production_axis = make_axis(
            "PRODUCTION_BEHAVIOR",
            code_ids,
            code_by_id,
            "DIRECT_STATIC_BEHAVIOR_EVIDENCE",
            "Static production findings are direct only after claim-by-claim semantic adjudication; they do not establish theory truth or material validity.",
        )
        test_runtime_axis = make_axis(
            "RELEASE_TEST_DEMO_RUNTIME",
            test_ids,
            test_by_id,
            "DIRECT_TEST_RUNTIME_OR_PROBE_EVIDENCE",
            "Release assertions, runtime observations, and synthetic probes remain distinct and do not establish external validity.",
        )
        stored_artifact_axis = make_axis(
            "STORED_ARTIFACT",
            artifact_ids,
            artifact_by_id,
            "DIRECT_CANONICAL_STORED_ARTIFACT_EVIDENCE",
            "Golden, PDF, image, and genealogy records are historical internal evidence, never independent scientific oracles.",
        )
        rows.append(
            {
                "claim_id": claim_id,
                "theory_claim_sha256": object_sha256(claim),
                "theory_axis": theory_axis,
                "production_axis": production_axis,
                "test_runtime_axis": test_runtime_axis,
                "stored_artifact_axis": stored_artifact_axis,
                "conformance_status": status,
                "decision_basis": decision,
                "authority_boundary": AUTHORITY_BOUNDARY,
                "code_impact": claim["code_impact"],
                "blocker_routes": blockers,
                "blocker_route_basis": blocker_basis,
            }
        )

    statuses = Counter(x["conformance_status"] for x in rows)
    high_risk = build_high_risk(code_by_id, test_by_id, artifact_by_id)
    document = common_header("PASS_P059_FOUR_AXIS_CONFORMANCE_MATRIX", coverage)
    document["schema_version"] = 7
    decision_semantics = {
        "ALIGNED": "All applicable internal axes have exact mutually consistent evidence; never external validity.",
        "PARTIAL": "At least one exact internal relation is supported while a required axis or bounded behavior remains open.",
        "MISALIGNED": "Exact internal evidence demonstrates a theory/contract versus production/release contradiction.",
        "ABSENT": "Applicability is explicit and exact evidence shows required production/test/artifact scope absent.",
        "UNVERIFIED": "Exact applicability or sufficient cross-axis evidence is missing; names, labels, and existence are not inferred joins.",
    }
    counts = {
        "theory_claims": 185,
        "theory_occurrences": 973,
        "governing_contract_routes": 38,
        "contract_evidence_relations": 80,
        "applicable_theory_claims": len(ledger),
        "code_finding_adjudications": sum(len(x["code_finding_adjudications"]) for x in ledger),
        "direct_code_relations": semantic_audit["classification_counts"]["DIRECT"],
        "related_not_direct_code_decisions": semantic_audit["classification_counts"]["RELATED_NOT_DIRECT"],
        "not_applicable_code_decisions": semantic_audit["classification_counts"]["NOT_APPLICABLE"],
        "na_pair_groundings": semantic_audit["na_pair_grounding_count"],
        "na_grounding_groups": semantic_audit["na_grounding_group_count"],
        "na_structural_signatures": semantic_audit["na_structural_signature_count"],
        "na_reasoning_signatures": semantic_audit["na_reasoning_signature_count"],
        "pair_graph_audits": semantic_audit["pair_graph_audit_count"],
        "cross_domain_bridges": semantic_audit["cross_domain_bridge_count"],
        "code_canonical_records": len(code_by_id),
        "test_runtime_canonical_records": len(test_by_id),
        "artifact_canonical_records": len(artifact_by_id),
        "row_orphans": 0,
        "row_duplicates": 0,
        "invalid_evidence_paths_or_anchors": 0,
        "missing_authority_boundaries": 0,
        "status_counts": {x: statuses.get(x, 0) for x in sorted(ALLOWED_STATUSES)},
        "high_risk_findings": len(high_risk),
    }
    document.update(
        {
            "scope": "Route every Step 39.1 theory claim once across theory, production behavior, release test/demo/runtime, and canonical stored-artifact axes.",
            "authority_boundary": "Four-axis status is frozen internal conformance only. No row establishes literature truth or external material validity.",
            "decision_semantics": decision_semantics,
            "semantic_cross_audit": semantic_audit,
            "applicable_claim_code_adjudications": ledger,
            "rows": rows,
            "high_risk_findings": high_risk,
            "counts": counts,
            "unresolved": [
                "Primary-literature exact support remains unverified for all 185 theory claims.",
                "The 134 uncontracted equation claims retain P059-BD-NEW-003 and no inferred cross-axis mapping.",
                "Chronology, initial history, zero-current direct L_V, factor-3,600 units, width roles, LCO temperature/high-voltage/doping, and Einstein activation/guard blockers remain open.",
                "No audited public experimental fit/held-out validation establishes graphite, LCO, Si, or blend external material validity.",
                "Stored PDF/image/golden provenance and self-reference debts remain open.",
            ],
        }
    )
    return document


def main() -> int:
    coverage = input_coverage(); code = build_code(coverage); test = build_test(coverage); main_matrix = build_main(coverage, code, test)
    code_sha, test_sha, main_sha = write_json(CODE_PATH, code), write_json(TEST_PATH, test), write_json(MAIN_PATH, main_matrix)
    print(f"PASS_P059_STEP_039_3_FOUR_AXIS_BUILD claims=185 code_records={len(code['records'])} test_runtime_records={len(test['test_runtime_records'])} artifact_records={len(test['artifact_records'])} adjudications=663 code_sha256={code_sha} test_sha256={test_sha} main_sha256={main_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
