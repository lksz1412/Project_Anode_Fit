#!/usr/bin/env python3
"""Generate source-linked Phase 059 symbol/unit/sign/assumption contracts."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
INDEX_PATH = RESULTS / "PHASE_059_THEORY_SOURCE_INDEX.json"
OUTPUT = RESULTS / "PHASE_059_THEORY_CONTRACT_MATRIX.json"
SUMMARY = RESULTS / "PHASE_059_THEORY_CONTRACT_REVIEW.md"

CH1 = "Claude/docs/v1.0.18.2/graphite_ica_ch1_v1.0.18.2.tex"
CH2 = "Claude/docs/v1.0.18.2/graphite_ica_ch2_v1.0.18.2.tex"
APP = "Claude/docs/v1.0.18.2/appendix_phase_separation.tex"

ALLOWED_DISPOSITIONS = {
    "PRESERVE",
    "CORRECT",
    "EMPIRICAL_ONLY",
    "THEORY_ONLY",
    "REJECT",
    "UNVERIFIED",
}


def eq(path: str, label: str) -> dict:
    return {"kind": "equation_or_label", "path": path, "label": label}


def prose(path: str, pattern: str) -> dict:
    return {"kind": "prose_regex", "path": path, "pattern": pattern}


CONTRACTS = [
    {
        "id": "P059-CON-001",
        "topic": "coordinates",
        "symbols": ["V_app", "V_n", "R_n", "sigma_d", "|I|"],
        "quantity": "measured terminal voltage and a lumped polarization-corrected model voltage",
        "unit": "V; R_n in ohm; |I| in A",
        "sign_or_orientation": "V_n = V_app - sigma_d |I| R_n",
        "assumptions": [
            "One constant resistance represents all modeled polarization.",
            "Electrode identity and protocol sign are supplied separately.",
        ],
        "source_claim": "The internal evaluation voltage is obtained by a direction-signed lumped ohmic subtraction.",
        "disposition": "EMPIRICAL_ONLY",
        "closure_state": "PARTIAL_OBSERVATION_LAYER",
        "required_action": "Keep this in the observation layer and split electrolyte, solid, and interfacial potentials in any mechanistic extension.",
        "evidence_specs": [eq(CH1, "eq:vn"), eq(CH1, "eq:n0map")],
    },
    {
        "id": "P059-CON-002",
        "topic": "coordinates",
        "symbols": ["q", "Q", "Q_cell"],
        "quantity": "normalized accumulated charge coordinate q = Q/Q_cell",
        "unit": "q dimensionless; Q and Q_cell on one explicit charge/capacity basis",
        "sign_or_orientation": "The orientation of increasing q must be fixed independently of charge/discharge labels.",
        "assumptions": [
            "Q and Q_cell use the same basis.",
            "The mapping from q to material stoichiometry is electrode specific.",
        ],
        "source_claim": "Charge conservation is written on a normalized trajectory coordinate.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_UNIT_AND_ORIENTATION_CONTRACT",
        "required_action": "Define separate variables for coulombs, ampere-hours, normalized capacity, and host stoichiometry.",
        "evidence_specs": [
            prose(CH1, r"Q_\\cell q=Q_\\bg"),
            prose(CH1, r"Q_\\cell.*C\(또는 A"),
        ],
    },
    {
        "id": "P059-CON-003",
        "topic": "coordinates",
        "symbols": ["c_rate", "|I|", "Q_cell"],
        "quantity": "conversion from C-rate and capacity to current magnitude",
        "unit": "c_rate in h^-1, Q_cell in Ah gives A; Q_cell in C requires division by 3600 s/h",
        "sign_or_orientation": "|I| is nonnegative; direction is not carried by its sign",
        "assumptions": ["Capacity and time units are explicitly compatible."],
        "source_claim": "|I| = c_rate Q_cell, with prose allowing Q_cell in C or Ah.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_DIMENSIONAL_BLOCKER",
        "required_action": "Make Ah the facade capacity unit or require SI coulombs with an explicit 3600 conversion.",
        "evidence_specs": [eq(CH1, "eq:n0map"), prose(CH1, r"c\\_rate 는 시간 역수")],
    },
    {
        "id": "P059-CON-004",
        "topic": "coordinates",
        "symbols": ["theta", "xi"],
        "quantity": "Li-site occupancy theta and delithiation progress xi = 1-theta",
        "unit": "dimensionless",
        "sign_or_orientation": "Increasing xi means delithiation; increasing theta means lithiation.",
        "assumptions": ["A transition can be represented by one scalar progress variable."],
        "source_claim": "Occupancy and progress are complementary coordinates.",
        "disposition": "PRESERVE",
        "closure_state": "CLOSED_DEFINITION_NEEDS_ELECTRODE_MAP",
        "required_action": "Preserve one global state orientation and map protocol direction only in the observation/trajectory layer.",
        "evidence_specs": [prose(CH1, r"\\theta_j=1-\\xi_j"), eq(CH1, "eq:fermifn")],
    },
    {
        "id": "P059-CON-005",
        "topic": "coordinates",
        "symbols": ["sigma_d", "s"],
        "quantity": "protocol traversal sign sigma_d versus fixed thermodynamic reaction-orientation sign s",
        "unit": "dimensionless signs",
        "sign_or_orientation": "sigma_d changes with protocol; s is fixed after defining the reference reaction.",
        "assumptions": ["Equilibrium state is independent of protocol direction."],
        "source_claim": "The sources distinguish a protocol sign from a fixed derivation sign but still place sigma_d in the equilibrium logistic.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_EQUILIBRIUM_DIRECTION_CONTAMINATION",
        "required_action": "Remove protocol direction from the equilibrium occupancy and use it only to traverse a fixed equilibrium relation or a metastable kinetic state.",
        "evidence_specs": [eq(CH1, "eq:xieq"), prose(CH1, r"유도 전용 고정 부호")],
    },
    {
        "id": "P059-CON-006",
        "topic": "phase_separation",
        "symbols": ["g(xi)", "Omega", "T_c"],
        "quantity": "symmetric regular-solution molar free energy and its mean-field critical condition",
        "unit": "g and Omega in J mol^-1; T and T_c in K",
        "sign_or_orientation": "Omega > 0 penalizes mixing; Omega > 2RT produces nonconvexity.",
        "assumptions": ["Symmetric Bragg-Williams mean field.", "One conserved composition coordinate."],
        "source_claim": "The homogeneous free energy loses convexity at Omega = 2RT.",
        "disposition": "PRESERVE",
        "closure_state": "CLOSED_WITHIN_SYMMETRIC_REGULAR_SOLUTION",
        "required_action": "Keep the criterion only for the stated symmetric mean-field model and do not treat fitted Omega as a universal material constant.",
        "evidence_specs": [eq(CH1, "eq:gxi"), eq(CH1, "eq:sm-thresh")],
    },
    {
        "id": "P059-CON-007",
        "topic": "phase_separation",
        "symbols": ["xi_b", "xi_s", "mu_A", "mu_B"],
        "quantity": "binodal coexistence compositions and spinodal local-stability limits",
        "unit": "compositions dimensionless; chemical potentials J mol^-1",
        "sign_or_orientation": "Binodal is a global common-tangent condition; spinodal is f''=0.",
        "assumptions": ["Symmetric regular solution for the displayed closed forms."],
        "source_claim": "The appendix correctly separates coexistence from loss of local stability.",
        "disposition": "PRESERVE",
        "closure_state": "THEORY_ONLY_NOT_PRODUCTION_CLOSURE",
        "required_action": "Use the binodal for equilibrium phase fractions and the spinodal only for metastability limits.",
        "evidence_specs": [eq(APP, "eq:app-binodal"), eq(APP, "eq:app-spinodal")],
    },
    {
        "id": "P059-CON-008",
        "topic": "phase_separation",
        "symbols": ["Delta U_hys", "gamma_j", "h_eta,j"],
        "quantity": "spinodal overdrive voltage span and empirical branch scaling",
        "unit": "Delta U_hys in V; gamma_j and h_eta,j dimensionless",
        "sign_or_orientation": "The modeled discharge center is shifted above the charge center under the chosen convention.",
        "assumptions": [
            "Metastable traversal reaches a scaled fraction of a mean-field spinodal span.",
            "Partial cycling is represented by a static scalar.",
        ],
        "source_claim": "A closed spinodal gap is reduced by empirical factors to create branch centers.",
        "disposition": "EMPIRICAL_ONLY",
        "closure_state": "OPEN_METASTABLE_DYNAMICS",
        "required_action": "Replace static branch factors with an internal-state kinetic model or label them strictly phenomenological.",
        "evidence_specs": [eq(CH1, "eq:dUhys"), eq(CH1, "eq:Ubranch")],
    },
    {
        "id": "P059-CON-009",
        "topic": "phase_separation",
        "symbols": ["f", "kappa", "M", "R(k)"],
        "quantity": "Cahn-Hilliard volumetric free-energy functional and linear growth rate",
        "unit": "f J m^-3; kappa J m^-1; M m^5 J^-1 s^-1; R(k) s^-1",
        "sign_or_orientation": "R(k)>0 denotes growth of an unstable Fourier mode.",
        "assumptions": ["Conserved order parameter.", "Constant mobility.", "Small-amplitude linearization."],
        "source_claim": "v1.0.17 repairs the earlier molar/volumetric dimensional ambiguity.",
        "disposition": "PRESERVE",
        "closure_state": "THEORY_ONLY_DIMENSIONALLY_REPAIRED",
        "required_action": "Keep volumetric and molar free-energy symbols distinct and supply material kappa and M before quantitative use.",
        "evidence_specs": [eq(APP, "eq:app-ch-F"), eq(APP, "eq:app-ch-R"), prose(APP, r"부피 밀도")],
    },
    {
        "id": "P059-CON-010",
        "topic": "phase_separation",
        "symbols": ["two-phase plateau", "production bell kernel"],
        "quantity": "relationship between equilibrium convexification and measured finite-width dQ/dV peaks",
        "unit": "plateau potential V; dQ/dV charge per V",
        "sign_or_orientation": "Equilibrium common tangent fixes a plateau potential but not a measured peak width.",
        "assumptions": ["Instrument, heterogeneity, finite size, and kinetics may broaden an equilibrium singularity."],
        "source_claim": "The appendix explicitly leaves finite peak width to a separate broadening model.",
        "disposition": "THEORY_ONLY",
        "closure_state": "OPEN_PRODUCTION_TWO_PHASE_CLOSURE",
        "required_action": "Connect convexified phase fractions to an observation kernel without reusing ideal-solution configurational entropy by notation alone.",
        "evidence_specs": [prose(APP, r"봉우리의 유한"), prose(CH1, r"w_j.*phenomenological")],
    },
    {
        "id": "P059-CON-011",
        "topic": "width",
        "symbols": ["w_j", "n_j", "R", "T", "F"],
        "quantity": "logistic voltage scale",
        "unit": "w_j in V; n_j dimensionless",
        "sign_or_orientation": "w_j must be strictly positive.",
        "assumptions": ["Ideal independent-site logistic when w_j = n_j RT/F is given a thermodynamic interpretation."],
        "source_claim": "All transitions share the numerical form w_j = n_j RT/F.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_ROLE_SPLIT",
        "required_action": "Use separate symbols for ideal thermal width and empirical ensemble/two-phase width.",
        "evidence_specs": [eq(CH1, "eq:wbase"), eq(CH2, "eq:logistic")],
    },
    {
        "id": "P059-CON-012",
        "topic": "width",
        "symbols": ["n_j"],
        "quantity": "dimensionless empirical width ratio",
        "unit": "dimensionless",
        "sign_or_orientation": "n_j > 0",
        "assumptions": ["It may absorb degeneracy, heterogeneity, or unresolved interactions but is not an electron number."],
        "source_claim": "The text calls n_j a multiplicity while fitting it as a free width factor.",
        "disposition": "EMPIRICAL_ONLY",
        "closure_state": "OPEN_MICROSCOPIC_MEANING",
        "required_action": "Rename it as an empirical width ratio unless a partition-function derivation and identifiability test support a microscopic meaning.",
        "evidence_specs": [eq(CH1, "eq:wbase"), prose(CH1, r"폭을.*피팅")],
    },
    {
        "id": "P059-CON-013",
        "topic": "width",
        "symbols": ["w_two_phase", "rho_U"],
        "quantity": "distribution of apparent transition potentials for a broadened two-phase event",
        "unit": "width in V; rho_U in V^-1",
        "sign_or_orientation": "Distribution is nonnegative and normalized.",
        "assumptions": ["Finite width is observational/ensemble broadening, not ideal homogeneous mixing."],
        "source_claim": "The two-phase bell is explicitly phenomenological.",
        "disposition": "EMPIRICAL_ONLY",
        "closure_state": "PRESERVE_AS_OBSERVATION_HYPOTHESIS",
        "required_action": "Give this width its own symbol and infer a normalized heterogeneity kernel from data or microstructure.",
        "evidence_specs": [prose(CH1, r"two-phase.*near-delta"), eq(CH1, "eq:ensavg")],
    },
    {
        "id": "P059-CON-014",
        "topic": "width",
        "symbols": ["Q_j", "dQ/dV", "w_j"],
        "quantity": "area-normalized logistic derivative peak",
        "unit": "Q_j charge; dQ/dV charge V^-1",
        "sign_or_orientation": "Peak magnitude is nonnegative; integral over the full voltage domain equals Q_j.",
        "assumptions": ["Infinite or sufficiently wide integration domain.", "Positive width."],
        "source_claim": "The logistic derivative conserves transition capacity.",
        "disposition": "PRESERVE",
        "closure_state": "CLOSED_KERNEL_IDENTITY",
        "required_action": "Retain area conservation as a mandatory numerical gate for every broadened and kinetic kernel.",
        "evidence_specs": [eq(CH1, "eq:belliden"), eq(CH1, "eq:eqpeak")],
    },
    {
        "id": "P059-CON-015",
        "topic": "width",
        "symbols": ["w_j", "partial S_config/partial theta"],
        "quantity": "thermal logistic slope versus configurational partial entropy",
        "unit": "w_j V; partial entropy J mol^-1 K^-1",
        "sign_or_orientation": "For the ideal lattice gas, R ln[xi/(1-xi)] changes sign at xi=1/2.",
        "assumptions": ["The width is the ideal-site thermal width, not a phenomenological two-phase distribution."],
        "source_claim": "Ch2 reads the temperature derivative of w=nRT/F as a configurational entropy contribution.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_TWO_PHASE_SEMANTIC_CONTRADICTION",
        "required_action": "Apply the configurational term only to a derived homogeneous occupancy model and not automatically to empirical two-phase widths.",
        "evidence_specs": [eq(CH2, "eq:dSconfig"), eq(CH2, "eq:dVdT_config"), prose(CH2, r"logistic 폭.*이미 부분몰")],
    },
    {
        "id": "P059-CON-016",
        "topic": "memory",
        "symbols": ["k_j", "L_q", "|I|", "Q_cell"],
        "quantity": "first-order relaxation rate and lag length in normalized capacity",
        "unit": "k_j s^-1; L_q dimensionless if |I|/Q_cell is s^-1",
        "sign_or_orientation": "L_q > 0",
        "assumptions": ["One exponential relaxation mode.", "Time and capacity units are consistent."],
        "source_claim": "L_q = |I|/(Q_cell k_j).",
        "disposition": "CORRECT",
        "closure_state": "OPEN_RATE_SCALE_AND_QCELL_UNITS",
        "required_action": "Define the time basis explicitly and replace the universal molecular prefactor with a calibrated coarse-grained rate model.",
        "evidence_specs": [eq(CH1, "eq:Lq"), eq(CH1, "eq:kuniv")],
    },
    {
        "id": "P059-CON-017",
        "topic": "memory",
        "symbols": ["L_V", "L_q", "dV/dq"],
        "quantity": "voltage-domain image of a lag length",
        "unit": "L_V in V",
        "sign_or_orientation": "L_V is a positive length; traversal direction belongs in the causal integral limits.",
        "assumptions": ["A local monotone mapping V(q) exists."],
        "source_claim": "L_V = L_q |dV/dq| at a representative condition.",
        "disposition": "EMPIRICAL_ONLY",
        "closure_state": "OPEN_NONMONOTONE_AND_LOCAL_MAP",
        "required_action": "Evolve the state in time or capacity and project to voltage afterward; do not reconstruct history by sorting voltage.",
        "evidence_specs": [eq(CH1, "eq:LV"), prose(CH1, r"컷점 OCV 기울기")],
    },
    {
        "id": "P059-CON-018",
        "topic": "memory",
        "symbols": ["xi_lag", "L_V"],
        "quantity": "normalized one-sided exponential causal memory integral",
        "unit": "xi_lag dimensionless; kernel V^-1",
        "sign_or_orientation": "The past lies toward lower V for one monotone traversal and toward higher V for the reverse traversal.",
        "assumptions": ["Constant L_V over the integral.", "Monotone voltage trajectory.", "Specified infinite-past boundary."],
        "source_claim": "The continuous integral and its reverse-direction mirror are mathematically normalized.",
        "disposition": "PRESERVE",
        "closure_state": "CLOSED_MATHEMATICS_OPEN_PROTOCOL_CONTRACT",
        "required_action": "Preserve the normalized kernel but state initial history and traversal as explicit inputs.",
        "evidence_specs": [eq(CH1, "eq:lag"), eq(CH1, "eq:reversal")],
    },
    {
        "id": "P059-CON-019",
        "topic": "memory",
        "symbols": ["xi_lag(V_0)", "history boundary"],
        "quantity": "initial condition and pre-window history of the lagged state",
        "unit": "dimensionless",
        "sign_or_orientation": "Initial state must correspond to the actual prior protocol.",
        "assumptions": ["The theoretical -infinity/+infinity boundary can be approximated by the observed finite window."],
        "source_claim": "The theory uses an infinite-past integral and does not define a finite-window experimental initial-state contract.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_INITIAL_HISTORY",
        "required_action": "Add an explicit initial state or preconditioning segment and test finite-window convergence.",
        "evidence_specs": [eq(CH1, "eq:lag"), prose(CH1, r"\$u\\to-\\infty"), prose(CH1, r"\$u\\to\+\\infty")],
    },
    {
        "id": "P059-CON-020",
        "topic": "memory",
        "symbols": ["A", "z_cut", "A_cap", "Delta H_a_eff"],
        "quantity": "reaction affinity used to modify an activation barrier",
        "unit": "A and Delta H_a_eff in J mol^-1",
        "sign_or_orientation": "Positive forward affinity lowers the forward barrier under the chosen convention.",
        "assumptions": ["A tail-cut affinity can represent local driving."],
        "source_claim": "The source freezes A=min(z_cut nRT,A_cap RT) per transition, so the realized local voltage derivative is zero.",
        "disposition": "REJECT",
        "closure_state": "OPEN_LOCAL_BARRIER_CONTRADICTION",
        "required_action": "Use a local thermodynamic affinity derived from electrochemical potentials and a rate law satisfying detailed balance.",
        "evidence_specs": [eq(CH1, "eq:Acut"), prose(CH1, r"실현되는.*미분은")],
    },
    {
        "id": "P059-CON-021",
        "topic": "memory",
        "symbols": ["L_V_direct", "|I|"],
        "quantity": "direct empirical voltage-lag override",
        "unit": "V",
        "sign_or_orientation": "Must vanish as |I| approaches zero for a unique equilibrium curve.",
        "assumptions": ["A direct override is allowed independently of current in the historical model."],
        "source_claim": "The physical derivation gives L_q proportional to |I|, but the fit architecture also permits an independent L_V.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_ZERO_CURRENT_LIMIT",
        "required_action": "Parameterize empirical lag as an explicit function with L_V(0,T,state)=0 and test the limit.",
        "evidence_specs": [eq(CH1, "eq:Lq"), prose(CH1, r"L_V.*직접")],
    },
    {
        "id": "P059-CON-022",
        "topic": "n_of_T",
        "symbols": ["n_j(T)", "n_0", "n_1", "T_ref"],
        "quantity": "minimal empirical temperature dependence of a width ratio",
        "unit": "n dimensionless; n_1 K^-1",
        "sign_or_orientation": "n_j(T) > 0 over the fitted temperature window",
        "assumptions": ["A linear form is adequate only within a bounded calibration window."],
        "source_claim": "n(T) is introduced as an optional data-decided residual width law.",
        "disposition": "EMPIRICAL_ONLY",
        "closure_state": "OPEN_IDENTIFIABILITY_AND_EXTRAPOLATION",
        "required_action": "Use only after per-temperature diagnostics and enforce positivity plus bounded extrapolation.",
        "evidence_specs": [prose(CH1, r"온도 함수.*n_j\(T\)"), prose(CH2, r"잔여 폭.*n_j\(T\)")],
    },
    {
        "id": "P059-CON-023",
        "topic": "n_of_T",
        "symbols": ["partial w_j/partial T", "n_j(T)"],
        "quantity": "temperature derivative of w_j=n_j(T)RT/F",
        "unit": "V K^-1",
        "sign_or_orientation": "Sign depends on n_j(T)+T n_j'(T).",
        "assumptions": ["The same n(T) defines both width and its derivative."],
        "source_claim": "The product-rule derivative is algebraically correct.",
        "disposition": "PRESERVE",
        "closure_state": "CLOSED_ALGEBRA_OPEN_PHYSICAL_ROLE",
        "required_action": "Keep one parameter source for w and dw/dT and separate empirical-width derivatives from configurational entropy.",
        "evidence_specs": [eq(CH2, "eq:dwdT-nT"), prose(CH1, r"\\partial w_j/\\partial T")],
    },
    {
        "id": "P059-CON-024",
        "topic": "n_of_T",
        "symbols": ["n_j(T)", "Delta S_rxn", "theta_E", "electronic entropy"],
        "quantity": "separability of multiple temperature-dependent peak mechanisms",
        "unit": "mixed parameters with explicit SI units",
        "sign_or_orientation": "Each mechanism can shift or reshape a peak with different signs.",
        "assumptions": ["At least three temperatures and enough independent observables are available."],
        "source_claim": "The source says data decide the scope but provides no identifiability proof.",
        "disposition": "UNVERIFIED",
        "closure_state": "OPEN_PARAMETER_IDENTIFIABILITY",
        "required_action": "Use profile likelihood/Fisher-rank and held-out temperatures before enabling n(T), vibrational, and electronic terms together.",
        "evidence_specs": [prose(CH2, r"피팅하는 스코프는 데이터가 정한다")],
    },
    {
        "id": "P059-CON-025",
        "topic": "entropy_heat",
        "symbols": ["U_j(T)", "Delta H_rxn", "Delta S_rxn", "F"],
        "quantity": "equilibrium insertion-reaction potential and entropy coefficient",
        "unit": "U V; Delta H J mol^-1; Delta S J mol^-1 K^-1",
        "sign_or_orientation": "For the stated insertion convention, U=(-Delta H+T Delta S)/F and dU/dT=Delta S/F.",
        "assumptions": ["Reference reaction and electron number are fixed.", "Pressure work is negligible."],
        "source_claim": "The center-temperature sign chain is internally consistent under its reaction convention.",
        "disposition": "PRESERVE",
        "closure_state": "CLOSED_CONVENTION_NEEDS_MATERIAL_REFERENCE",
        "required_action": "State the half-reaction for every electrode and never compare cumulative formation enthalpy with differential reaction enthalpy.",
        "evidence_specs": [eq(CH1, "eq:Uj"), eq(CH1, "eq:lco-dUdT")],
    },
    {
        "id": "P059-CON-026",
        "topic": "entropy_heat",
        "symbols": ["S_config", "partial S_config/partial theta"],
        "quantity": "ideal binary-site configurational entropy and its partial-molar derivative",
        "unit": "J mol^-1 K^-1",
        "sign_or_orientation": "The derivative changes sign at half occupancy and diverges at ideal endpoints.",
        "assumptions": ["Independent equivalent sites.", "Homogeneous single phase.", "Thermodynamic-limit ideal mixing."],
        "source_claim": "The configurational formula is correct for the ideal lattice gas.",
        "disposition": "PRESERVE",
        "closure_state": "CLOSED_IDEAL_LIMIT_ONLY",
        "required_action": "Replace endpoint divergences and two-phase regions with the appropriate interacting/convexified chemical potential.",
        "evidence_specs": [eq(CH2, "eq:Sconfig"), eq(CH2, "eq:dSconfig")],
    },
    {
        "id": "P059-CON-027",
        "topic": "entropy_heat",
        "symbols": ["g_j(V)", "dU/dT_weighted"],
        "quantity": "peak-amplitude-weighted apparent entropy coefficient in overlapping transitions",
        "unit": "V K^-1",
        "sign_or_orientation": "Weights are nonnegative and normalized where total peak amplitude is nonzero.",
        "assumptions": ["Independent additive transition peaks.", "A local apparent coefficient is meaningful under overlap."],
        "source_claim": "The weighted formula is an observation-level blend, not a unique thermodynamic partial molar entropy.",
        "disposition": "EMPIRICAL_ONLY",
        "closure_state": "OPEN_THERMODYNAMIC_INTERPRETATION",
        "required_action": "Label the result as an apparent overlap-weighted coefficient and validate against independently measured entropy.",
        "evidence_specs": [eq(CH2, "eq:weighted"), prose(CH2, r"겹침 가중")],
    },
    {
        "id": "P059-CON-028",
        "topic": "entropy_heat",
        "symbols": ["hysteresis branch mean", "dU/dT"],
        "quantity": "average of charge/discharge branch derivatives",
        "unit": "V K^-1",
        "sign_or_orientation": "Arithmetic branch averaging cancels only symmetric branch contributions.",
        "assumptions": ["Charge and discharge branches are symmetric around a thermodynamic center."],
        "source_claim": "The source treats branch averaging as entropy recovery.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_METASTABLE_SYMMETRY_ASSUMPTION",
        "required_action": "Use equilibrium or relaxation-derived OCV for entropy; treat branch averaging as a tested approximation.",
        "evidence_specs": [eq(CH2, "eq:hys_branch"), eq(CH2, "eq:hys_rev")],
    },
    {
        "id": "P059-CON-029",
        "topic": "entropy_heat",
        "symbols": ["q_rev", "I", "T", "dU_oc/dT"],
        "quantity": "reversible heat rate",
        "unit": "W",
        "sign_or_orientation": "q_rev = -I T dU_oc/dT under the stated cell-current convention.",
        "assumptions": ["Current sign and electrode/full-cell voltage convention are explicit.", "Temperature is absolute K."],
        "source_claim": "The reversible-heat identity is standard but electrode and cell current labels must not be mixed.",
        "disposition": "PRESERVE",
        "closure_state": "CLOSED_FORMULA_OPEN_SIGN_MAPPING",
        "required_action": "Provide a half-cell/full-cell sign table and test heat signs against calorimetry.",
        "evidence_specs": [eq(CH2, "eq:qrev"), eq(CH2, "eq:complete")],
    },
    {
        "id": "P059-CON-030",
        "topic": "einstein_vibration",
        "symbols": ["S_vib", "theta_E", "u=theta_E/T"],
        "quantity": "entropy of one molar Einstein oscillator mode",
        "unit": "J mol^-1 K^-1",
        "sign_or_orientation": "S_vib >= 0, tends to zero as T approaches zero, and grows logarithmically in the classical high-T limit.",
        "assumptions": ["One harmonic mode with fixed frequency.", "No anharmonicity or mode coupling."],
        "source_claim": "The single-mode entropy expression and limits are internally correct.",
        "disposition": "PRESERVE",
        "closure_state": "CLOSED_SINGLE_OSCILLATOR_ONLY",
        "required_action": "Retain as a basis function, not yet as an insertion-reaction entropy.",
        "evidence_specs": [eq(CH2, "eq:Svib-einstein"), prose(CH2, r"저온.*S_\\vib\\to0")],
    },
    {
        "id": "P059-CON-031",
        "topic": "einstein_vibration",
        "symbols": ["Delta S_vib(T)", "Delta U_vib(T)", "T_ref"],
        "quantity": "reference-subtracted vibrational entropy and voltage correction",
        "unit": "Delta S J mol^-1 K^-1; Delta U V",
        "sign_or_orientation": "Both corrections are zero at T_ref by construction.",
        "assumptions": ["The same oscillator defines free energy and entropy.", "Reference constants are absorbed into baseline center parameters."],
        "source_claim": "The derivative of the reference-subtracted voltage correction matches the entropy correction.",
        "disposition": "PRESERVE",
        "closure_state": "CLOSED_INTERNAL_ROUND_TRIP",
        "required_action": "Keep the round-trip gate while adding reaction-spectrum amplitudes and positive reference-temperature validation.",
        "evidence_specs": [eq(CH2, "eq:dSvib"), eq(CH2, "eq:dUvib")],
    },
    {
        "id": "P059-CON-032",
        "topic": "einstein_vibration",
        "symbols": ["Delta phonon DOS", "mode multiplicity", "theta_E,j"],
        "quantity": "vibrational contribution to an insertion reaction",
        "unit": "J mol_reaction^-1 K^-1",
        "sign_or_orientation": "Sign follows product-minus-reactant spectrum and stoichiometry, not an absolute oscillator entropy.",
        "assumptions": ["Reaction entropy is a difference between host states and all participating phases."],
        "source_claim": "The historical term uses one unit-amplitude absolute oscillator and does not define product/reactant spectral differences.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_REACTION_QUANTITY_DEFINITION",
        "required_action": "Introduce weighted product-minus-reactant phonon spectra or fitted signed mode amplitudes constrained by DFT/calorimetry.",
        "evidence_specs": [prose(CH2, r"전 모드 합을 대표 진동수 하나로 접고"), eq(CH2, "eq:Svib_mode")],
    },
    {
        "id": "P059-CON-033",
        "topic": "lco_electronic",
        "symbols": ["U_T1", "U_T2", "U_T3", "U_T4"],
        "quantity": "LCO transition centers and declared voltage scope",
        "unit": "V vs Li/Li+",
        "sign_or_orientation": "Increasing cathode potential corresponds to delithiation on charge.",
        "assumptions": ["The modeled O3 window ends below the O3-to-H1-3 high-voltage event."],
        "source_claim": "The document places the approximately 4.55 V transition explicitly outside scope.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_USER_GOAL_HIGH_VOLTAGE_LCO",
        "required_action": "Add a separately validated doped high-voltage LCO phase/oxygen-redox model and public data before claiming the requested scope.",
        "evidence_specs": [prose(CH1, r"4\.55.*O3.*H1-3"), prose(CH1, r"고전압, 범위 밖")],
    },
    {
        "id": "P059-CON-034",
        "topic": "lco_electronic",
        "symbols": ["g(E_F,x)", "S_e"],
        "quantity": "Sommerfeld electronic entropy from the Fermi-level density of states",
        "unit": "g states J^-1 atom^-1 or states eV^-1 atom^-1 with explicit conversion; S_e J mol^-1 K^-1",
        "sign_or_orientation": "Absolute electronic entropy is nonnegative; reaction partial entropy may have either sign.",
        "assumptions": ["Degenerate electrons.", "DOS smooth over k_B T near E_F.", "Normalization per atom is explicit."],
        "source_claim": "The Sommerfeld formula and eV-to-J conversion are valid within the metallic smooth-DOS limit.",
        "disposition": "PRESERVE",
        "closure_state": "CLOSED_LIMIT_OPEN_TRANSITION_REGION",
        "required_action": "Use electronic-structure or measured heat-capacity data through the MIT where the smooth-DOS assumption fails.",
        "evidence_specs": [eq(CH1, "eq:Se"), eq(CH1, "eq:gunit")],
    },
    {
        "id": "P059-CON-035",
        "topic": "lco_electronic",
        "symbols": ["g_gate(E_F,x)", "x_MIT", "Delta x_MIT"],
        "quantity": "empirical composition gate for the DOS across the MIT",
        "unit": "g in states eV^-1 atom^-1; x dimensionless",
        "sign_or_orientation": "Gate orientation must match metallic versus insulating composition sides.",
        "assumptions": ["A logistic in composition approximates an unknown continuous DOS curve."],
        "source_claim": "The source admits the continuous g(E_F,x) curve is absent from primary literature and fills it with a logistic hypothesis.",
        "disposition": "EMPIRICAL_ONLY",
        "closure_state": "OPEN_PRIMARY_DATA_AND_CATEGORY_ERROR",
        "required_action": "Do not justify the composition gate by resemblance to a Fermi occupation; calibrate it to DOS/entropy data and propagate uncertainty.",
        "evidence_specs": [eq(CH1, "eq:ggate"), prose(CH1, r"연속 곡선.*1차 문헌")],
    },
    {
        "id": "P059-CON-036",
        "topic": "lco_electronic",
        "symbols": ["x(V)", "xi_eq,1(V)", "U_1(x,T)"],
        "quantity": "mapping from voltage-domain transition progress to LCO stoichiometry and electronic center feedback",
        "unit": "x and xi dimensionless; U V",
        "sign_or_orientation": "Delithiation lowers x while the selected progress coordinate increases.",
        "assumptions": ["The first transition progress provides a valid local stoichiometry map.", "A fixed point is unique and stable."],
        "source_claim": "The precise theory is implicit because x depends on xi, xi on U, and U on electronic entropy at x.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_FIXED_POINT_AND_CHAIN_RULE",
        "required_action": "Solve the implicit state equation and include dU/dV in dxi/dV; validate uniqueness and branch stability.",
        "evidence_specs": [eq(CH1, "eq:lco-xmap"), eq(CH1, "eq:lco-U1V"), prose(CH1, r"고정점 구조")],
    },
    {
        "id": "P059-CON-037",
        "topic": "lco_electronic",
        "symbols": ["Omega_doped", "lambda_dop", "delta U_dop"],
        "quantity": "doping-induced suppression of ordering/hysteresis and independent center shift",
        "unit": "Omega J mol^-1; lambda dimensionless; center shift V",
        "sign_or_orientation": "Reducing Omega closes the symmetric mean-field gap; center shift is a separate signed parameter.",
        "assumptions": ["Doping effects can be reduced to Omega scaling plus an independent center shift."],
        "source_claim": "The document labels quantitative doping shift as literature gap G3.",
        "disposition": "EMPIRICAL_ONLY",
        "closure_state": "OPEN_DOPED_MATERIAL_VALIDATION",
        "required_action": "Fit dopant-specific parameters to public high-voltage datasets with chemistry, concentration, cycling, and temperature metadata.",
        "evidence_specs": [eq(CH1, "eq:lco-dope"), prose(CH1, r"갭 G3")],
    },
    {
        "id": "P059-CON-038",
        "topic": "lco_electronic",
        "symbols": ["Delta S_config", "Delta S_vib", "Delta S_e", "U_1(T)"],
        "quantity": "decomposition of LCO insertion entropy and electronic T-squared center shift",
        "unit": "entropy terms J mol^-1 K^-1; U V",
        "sign_or_orientation": "The insertion-reaction convention controls signs; a term linear in T in entropy integrates to one-half times T squared in voltage.",
        "assumptions": [
            "Config, vibrational, and electronic partition functions factorize to leading order.",
            "The electronic entropy is locally linear in T.",
        ],
        "source_claim": "The additive decomposition and one-half integration factor are algebraically sound, but config-electronic coupling is neglected.",
        "disposition": "CORRECT",
        "closure_state": "OPEN_COUPLING_AND_CODE_CONFORMANCE",
        "required_action": "Test factorization, define reaction-resolved vibrational terms, and implement the same composition and temperature dependence in code.",
        "evidence_specs": [eq(CH1, "eq:lco-decomp"), eq(CH1, "eq:U1T2"), prose(CH1, r"교차항.*0")],
    },
]


def compact(text: str, limit: int = 500) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    return value if len(value) <= limit else value[: limit - 1] + "…"


def source_excerpt(path: str, line_start: int, line_end: int) -> str:
    lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
    start = max(line_start - 2, 0)
    end = min(line_end + 1, len(lines))
    return compact("\n".join(lines[start:end]))


def resolve_evidence(spec: dict, index: dict) -> dict:
    path = spec["path"]
    if spec["kind"] == "equation_or_label":
        label = spec["label"]
        candidates = [
            item
            for item in index["labels"]
            if item["path"] == path and item["label"] == label
        ]
        if len(candidates) != 1:
            raise SystemExit(
                f"label resolution failed: path={path} label={label} "
                f"count={len(candidates)}"
            )
        match = candidates[0]
        return {
            "kind": spec["kind"],
            "path": path,
            "label": label,
            "line_start": match["line"],
            "line_end": match["line"],
            "source_excerpt": source_excerpt(path, match["line"], match["line"]),
        }
    if spec["kind"] == "prose_regex":
        pattern = re.compile(spec["pattern"])
        lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
        matches = [number for number, line in enumerate(lines, 1) if pattern.search(line)]
        if not matches:
            raise SystemExit(
                f"prose evidence not found: path={path} pattern={spec['pattern']}"
            )
        line = matches[0]
        return {
            "kind": spec["kind"],
            "path": path,
            "pattern": spec["pattern"],
            "match_count": len(matches),
            "line_start": line,
            "line_end": line,
            "source_excerpt": source_excerpt(path, line, line),
        }
    raise ValueError(f"unknown evidence kind: {spec['kind']}")


def main() -> None:
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    records = []
    for contract in CONTRACTS:
        if contract["disposition"] not in ALLOWED_DISPOSITIONS:
            raise SystemExit(f"invalid disposition: {contract['id']}")
        record = {
            key: value for key, value in contract.items() if key != "evidence_specs"
        }
        record["evidence"] = [
            resolve_evidence(spec, index) for spec in contract["evidence_specs"]
        ]
        records.append(record)

    topic_counts = Counter(record["topic"] for record in records)
    disposition_counts = Counter(record["disposition"] for record in records)
    closure_counts = Counter(record["closure_state"] for record in records)
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "scope": (
            "Phase 059 Step 33.4 source-linked symbol, unit, sign/orientation, "
            "and assumption contracts"
        ),
        "status": "PASS_P059_THEORY_CONTRACT_EXTRACTION",
        "authority_boundary": (
            "Audit contracts and provisional dispositions, not final theory canon, "
            "code conformance, literature verification, or material validation."
        ),
        "allowed_dispositions": sorted(ALLOWED_DISPOSITIONS),
        "record_count": len(records),
        "topic_counts": dict(sorted(topic_counts.items())),
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "closure_state_counts": dict(sorted(closure_counts.items())),
        "rules": [
            "One symbol denotes one physical quantity within a derivation.",
            "Units and reference reactions are part of the public contract.",
            "Protocol direction does not define equilibrium state.",
            "Empirical observation kernels are not equilibrium thermodynamics.",
            "A reference-subtracted correction is not a reaction quantity until product/reactant states and weights are defined.",
            "Theory-body prose remains physics/chemistry only; implementation traceability belongs in separate conformance artifacts.",
        ],
        "records": records,
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    rows = []
    for record in records:
        evidence = "; ".join(
            f"{Path(item['path']).name}:{item['line_start']}"
            + (f" ({item['label']})" if "label" in item else "")
            for item in record["evidence"]
        )
        rows.append(
            f"| {record['id']} | {record['topic']} | "
            f"{', '.join(record['symbols'])} | {record['disposition']} | "
            f"{record['closure_state']} | {evidence} |"
        )
    summary = """# Phase 059 theory contract review

This is a source-linked audit contract, not the final theory manuscript and not
a code-conformance or external-validity verdict.

| ID | Topic | Symbols | Disposition | Closure state | Source anchors |
|---|---|---|---|---|---|
{rows}

## Counts

- records: {record_count}
- topics: {topic_counts}
- dispositions: {disposition_counts}

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
""".format(
        rows="\n".join(rows),
        record_count=len(records),
        topic_counts=json.dumps(dict(sorted(topic_counts.items())), ensure_ascii=False),
        disposition_counts=json.dumps(
            dict(sorted(disposition_counts.items())), ensure_ascii=False
        ),
    )
    SUMMARY.write_text(summary, encoding="utf-8")
    print(
        "PASS_P059_THEORY_CONTRACT_EXTRACTION "
        f"records={len(records)} topics={len(topic_counts)}"
    )


if __name__ == "__main__":
    main()
