#!/usr/bin/env python3
"""Independently audit v1.0.14 LCO entropy, heat, sign, and doping claims."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
CH1 = ROOT / "Claude/docs/v1.0.14/graphite_ica_ch1_v1.0.14.tex"
CH2 = ROOT / "Claude/docs/v1.0.14/graphite_ica_ch2_v1.0.14.tex"
CODE = ROOT / "Claude/docs/v1.0.14/Anode_Fit_v1.0.14.py"
OUTPUT = ROOT / "Codex/results/PHASE_059_V1014_LCO_HEAT_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1014_LCO_HEAT_REVIEW.md"

F = 96485.33212
R = 8.31446261815324
KB = 1.380649e-23
EV_TO_J = 1.602176634e-19


PRIMARY_SOURCES = [
    {
        "id": "SWIDERSKA_MOCEK_2019",
        "title": (
            "Temperature coefficients of Li-ion battery single electrode "
            "potentials and related entropy changes - revisited"
        ),
        "doi": "10.1039/C8CP06638H",
        "url": "https://doi.org/10.1039/C8CP06638H",
        "verified_claim": (
            "The inferred intrinsic LCO single-electrode coefficient is "
            "+0.83 mV/K, whereas the measured isothermal Li|LCO half-cell "
            "voltage coefficient is -0.25 mV/K; the inferred Li-metal "
            "single-electrode coefficient is +1.03 mV/K."
        ),
        "audit_effect": (
            "The manuscript applies +0.83 mV/K to a half-cell voltage "
            "defined versus Li, which changes the sign and magnitude of "
            "the reaction-entropy anchor."
        ),
    },
    {
        "id": "MOTOHASHI_2009",
        "title": "Electronic phase diagram of the layered cobalt oxide system LixCoO2",
        "doi": "10.1103/PhysRevB.80.165114",
        "url": "https://doi.org/10.1103/PhysRevB.80.165114",
        "open_url": "https://arxiv.org/pdf/0909.3556",
        "verified_claim": (
            "D(E_F)=13 electrons/eV for CoO2 is calculated from a "
            "susceptibility difference under a Pauli-paramagnetic "
            "assumption. The paper does not state 13 e/eV/atom in the "
            "cited passage and reports a complex composition-dependent "
            "electronic phase diagram."
        ),
        "audit_effect": (
            "The manuscript's direct-measurement, per-atom, tier-A label "
            "and transfer of this x=0 endpoint to the x~0.85 MIT gate are "
            "not source-supported."
        ),
    },
    {
        "id": "MENETRIER_1999",
        "title": (
            "The insulator-metal transition upon lithium deintercalation "
            "from LiCoO2"
        ),
        "doi": "10.1039/A900016J",
        "url": "https://doi.org/10.1039/A900016J",
        "verified_claim": (
            "The 0.75<=x<=0.94 biphasic domain accompanies a gradual "
            "change from localized to delocalized electronic behavior; "
            "the metal-nonmetal transition is proposed as its driver."
        ),
        "audit_effect": (
            "This supports an electronic-transition mechanism and a "
            "two-phase interval, not the manuscript's unique smooth "
            "logistic DOS curve or its width."
        ),
    },
    {
        "id": "REYNIER_2004",
        "title": "Entropy of Li intercalation in LixCoO2",
        "doi": "10.1103/PhysRevB.70.174304",
        "url": "https://doi.org/10.1103/PhysRevB.70.174304",
        "open_url": "https://authors.library.caltech.edu/records/e9xj1-c1x65",
        "verified_claim": (
            "Equilibrated-voltage measurements cover 0.5<x<=1.0. "
            "Electronic entropy of lithiation is small in the O3 phase, "
            "while electronic and configurational changes are comparable "
            "for the metal-insulator transition."
        ),
        "audit_effect": (
            "Electronic entropy belongs in the candidate physics, but its "
            "measured profile is not validated by the x=0 endpoint gate."
        ),
    },
    {
        "id": "BERNARDI_1985",
        "title": "A General Energy Balance for Battery Systems",
        "doi": "10.1149/1.2113792",
        "url": "https://doi.org/10.1149/1.2113792",
        "verified_claim": (
            "The general cell energy balance contains electrochemical "
            "reaction, phase-change, mixing, and Joule-heating terms; "
            "reduced heat equations require explicit simplifications."
        ),
        "audit_effect": (
            "The reduced reversible/irreversible split may be preserved "
            "only with a signed-current convention and stated omitted terms."
        ),
    },
    {
        "id": "TEICHERT_SHOJAEI_2024",
        "title": (
            "Bridging scales with machine learning from first-principles "
            "statistical mechanics to phase-field computations for LixCoO2"
        ),
        "doi": "10.1016/j.jmps.2024.105726",
        "url": "https://doi.org/10.1016/j.jmps.2024.105726",
        "open_url": "https://arxiv.org/pdf/2302.08991",
        "verified_claim": (
            "The work models O3 order-disorder free energy and explicitly "
            "does not capture the metal-insulator plateau around x~0.7-0.9; "
            "strain and vibrational entropy are also excluded."
        ),
        "audit_effect": (
            "It does not validate the manuscript's logistic electronic "
            "entropy gate. The manuscript also cites article 105727, but "
            "the published article number and DOI are 105726."
        ),
    },
    {
        "id": "XIA_2024_DOPING",
        "title": (
            "Stabilizing 4.6 V LiCoO2 via Er and Mg trace doping at "
            "Li-site and Co-site respectively"
        ),
        "doi": "10.1002/smll.202311578",
        "url": "https://doi.org/10.1002/smll.202311578",
        "verified_claim": (
            "Mg at the Co site suppresses the ~4.2 V "
            "hexagonal-monoclinic transition but can worsen lattice-oxygen "
            "stability and the >4.45 V O3-to-H1-3 transition; Er at the Li "
            "site improves oxygen stability."
        ),
        "audit_effect": (
            "Doping is site- and mechanism-specific and cannot generally "
            "be represented only by lowering a scalar regular-solution "
            "Omega."
        ),
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_v1014_module():
    spec = importlib.util.spec_from_file_location("v1014_lco_heat_audit", CODE)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load v1.0.14 module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def first_line(text: str, marker: str) -> int:
    return next(
        index
        for index, line in enumerate(text.splitlines(), 1)
        if marker in line
    )


def source_contracts(ch1: str, ch2: str, code: str) -> dict:
    heat_start = code.find("def reversible_heat")
    heat_signature_end = code.find(") -> ScalarOrArray:", heat_start)
    heat_signature = code[heat_start:heat_signature_end]
    return {
        "line_counts": {
            "chapter_1": len(ch1.splitlines()),
            "chapter_2": len(ch2.splitlines()),
            "production_code": len(code.splitlines()),
        },
        "chapter_1_claim_lines": {
            "lco_center_identity": first_line(ch1, "\\label{eq:lco-dUdT}"),
            "doping_scalar_limit": first_line(ch1, "\\label{eq:lco-dope}"),
            "sommerfeld_entropy": first_line(ch1, "\\label{eq:Se}"),
            "molar_electronic_entropy": first_line(
                ch1, "\\label{eq:dSemolar}"
            ),
            "t_squared_center": first_line(ch1, "\\label{eq:U1T2}"),
            "mit_gate": first_line(ch1, "\\label{eq:ggate}"),
            "gate_entropy": first_line(ch1, "\\label{eq:dSegate}"),
            "plus_0p83_anchor": first_line(ch1, "0.83$ mV/K"),
            "dos_13_per_atom": first_line(ch1, "13$ e/eV/atom"),
            "wrong_ml_article_number": first_line(ch1, "105727"),
        },
        "chapter_2_claim_lines": {
            "sommerfeld_entropy": first_line(ch2, "\\label{eq:Se}"),
            "reversible_heat": first_line(ch2, "\\label{eq:qrev}"),
            "reaction_activation_entropy_split": first_line(
                ch2, "반응 엔트로피 vs 활성화 엔트로피"
            ),
        },
        "code_lines": {
            "gate_function": first_line(code, "def func_dSe_molar"),
            "reversible_heat": first_line(code, "def reversible_heat"),
            "irreversible_heat": first_line(code, "def irreversible_heat"),
            "t_ref_freeze": first_line(code, "T_ref = 298.15"),
            "x_center_freeze": first_line(
                code, "tr['x_center'], T_ref"
            ),
            "lco_data": first_line(code, "LCO_MSMR_LIT = ["),
        },
        "theory_high_voltage_t4_present": (
            "\\sim$4.55" in ch1 and "O3$\\to$H1-3" in ch1
        ),
        "theory_high_voltage_t4_scope": "OPTIONAL_OUT_OF_SCOPE",
        "code_has_doping_parameter": any(
            token in code
            for token in ("dopant", "doping", "Al_content", "Mg_content")
        ),
        "code_has_lco_omega": any(
            "'Omega'" in line
            for line in code.splitlines()[650:683]
        ),
        "code_has_composition_resolved_electronic_gate": (
            "tr['x_center'], T_ref" not in code
        ),
        "code_has_t_squared_lco_center": (
            "T**2" in code[code.find("class LCOCathodeDQDV") :]
            or "T * T" in code[code.find("class LCOCathodeDQDV") :]
        ),
        "heat_current_linked_to_curve_direction": (
            "direction" in heat_signature
        ),
    }


def numerical_rederivation(module) -> dict:
    temperature = 298.15
    intrinsic_lco_coefficient = 0.83e-3
    li_reference_coefficient = 1.03e-3
    measured_half_cell_coefficient = -0.25e-3
    difference_from_intrinsic_values = (
        intrinsic_lco_coefficient - li_reference_coefficient
    )

    g_max = 13.0
    x_mit = 0.85
    dx_mit = 0.05

    def sigmoid(z: float) -> float:
        return 1.0 / (1.0 + math.exp(-z))

    def gate_g(x: float) -> float:
        return g_max * (1.0 - sigmoid((x - x_mit) / dx_mit))

    endpoint_entropy_kb = (
        math.pi**2 / 3.0 * (KB * temperature / EV_TO_J) * g_max
    )
    gate_center_entropy = float(
        module.func_dSe_molar(
            x_mit, temperature, g_max, x_mit, dx_mit
        )
    )
    closed_gate_center_entropy = (
        -(math.pi**2 / 3.0)
        * R
        * (KB * temperature / EV_TO_J)
        * (g_max / dx_mit)
        * 0.25
    )
    gate_integrated_entropy_kb_x1_to_x0 = (
        math.pi**2
        / 3.0
        * (KB * temperature / EV_TO_J)
        * (gate_g(0.0) - gate_g(1.0))
    )

    electronic_transition = next(
        item for item in module.LCO_MSMR_LIT if item.get("electronic")
    )
    lco_model = module.LCOCathodeDQDV(
        module.LCO_MSMR_LIT, x=0.5, Rn=0.01, Cbg=0.0
    )
    temperature_grid = np.array([268.15, 298.15, 328.15])
    effective_entropy = np.array(
        [
            float(lco_model._effective_dS_rxn(electronic_transition, t))
            for t in temperature_grid
        ]
    )
    code_center = np.array(
        [
            float(
                module.func_U_j(
                    t,
                    electronic_transition["dH_rxn"],
                    lco_model._effective_dS_rxn(electronic_transition, t),
                )
            )
            for t in temperature_grid
        ]
    )
    code_second_difference = float(
        code_center[0] - 2.0 * code_center[1] + code_center[2]
    )
    a_e = gate_center_entropy / temperature
    theoretical_second_difference = float(
        a_e / F * (temperature_grid[2] - temperature_grid[1]) ** 2
    )

    theory_transition_centers = [3.90, 4.05, 4.17]
    code_transition_centers = [
        float(
            module.func_U_j(
                temperature,
                item["dH_rxn"],
                lco_model._effective_dS_rxn(item, temperature),
            )
        )
        for item in module.LCO_MSMR_LIT
    ]

    return {
        "temperature_K": temperature,
        "potential_reference_rederivation": {
            "intrinsic_lco_single_electrode_V_per_K": (
                intrinsic_lco_coefficient
            ),
            "li_metal_single_electrode_V_per_K": li_reference_coefficient,
            "intrinsic_difference_V_per_K": (
                difference_from_intrinsic_values
            ),
            "measured_isothermal_Li_LCO_half_cell_V_per_K": (
                measured_half_cell_coefficient
            ),
            "manuscript_intrinsic_entropy_J_per_mol_K": (
                F * intrinsic_lco_coefficient
            ),
            "measured_half_cell_entropy_J_per_mol_K": (
                F * measured_half_cell_coefficient
            ),
            "entropy_sign_reversal": (
                F * intrinsic_lco_coefficient
                * F
                * measured_half_cell_coefficient
                < 0
            ),
        },
        "sommerfeld_gate_rederivation": {
            "g_max_input_e_per_eV": g_max,
            "source_unit_promoted_to_per_atom_without_support": True,
            "endpoint_electronic_entropy_kB": endpoint_entropy_kb,
            "g_at_x_1_e_per_eV": gate_g(1.0),
            "g_at_x_0_e_per_eV": gate_g(0.0),
            "x_1_residual_fraction": gate_g(1.0) / g_max,
            "gate_center_dS_code_J_per_mol_K": gate_center_entropy,
            "gate_center_dS_closed_form_J_per_mol_K": (
                closed_gate_center_entropy
            ),
            "gate_integrated_entropy_x1_to_x0_kB": (
                gate_integrated_entropy_kb_x1_to_x0
            ),
            "gate_peak_scales_as_inverse_dx": True,
            "gate_area_tracks_endpoint_difference": True,
        },
        "theory_code_temperature_contract": {
            "temperature_grid_K": temperature_grid.tolist(),
            "code_effective_entropy_J_per_mol_K": (
                effective_entropy.tolist()
            ),
            "code_effective_entropy_temperature_invariant": bool(
                np.all(effective_entropy == effective_entropy[0])
            ),
            "code_T1_center_V": code_center.tolist(),
            "code_center_second_difference_V": code_second_difference,
            "theory_gate_a_e_J_per_mol_K2": a_e,
            "theory_expected_symmetric_second_difference_V": (
                theoretical_second_difference
            ),
            "theory_T_squared_curvature_implemented": (
                not math.isclose(
                    code_second_difference,
                    0.0,
                    rel_tol=0.0,
                    abs_tol=1.0e-14,
                )
            ),
        },
        "transition_map": {
            "theory_centers_V": theory_transition_centers,
            "code_centers_V_at_298p15K": code_transition_centers,
            "theory_max_center_V": max(theory_transition_centers),
            "code_max_center_V": max(code_transition_centers),
            "theory_code_centers_match": bool(
                np.allclose(
                    theory_transition_centers,
                    code_transition_centers,
                    rtol=0.0,
                    atol=0.01,
                )
            ),
            "code_center_above_4p15V_count": sum(
                center > 4.15 for center in code_transition_centers
            ),
            "doped_high_voltage_profile_present": False,
        },
        "heat_sign_contract": {
            "reaction_coordinate": (
                "I_lith>0 means the written lithiation/reduction reaction "
                "advances"
            ),
            "thermodynamic_identity": (
                "E_lith=-DeltaG_lith/F; "
                "dE_lith/dT=DeltaS_lith/F"
            ),
            "reversible_heat_generation": (
                "qdot_rev,gen=-I_lith*T*dE_lith/dT"
            ),
            "irreversible_heat_generation": (
                "qdot_irr,gen=I_ext*(E_oc-V_terminal) only under the "
                "matching discharge-positive cell convention; otherwise "
                "use overpotential times its conjugate signed current"
            ),
            "charge_discharge_labels_sufficient": False,
        },
    }


def canonical_repair_contract() -> dict:
    return {
        "potential_and_heat": [
            "Define the written lithiation reaction and I_lith before any sign.",
            "Distinguish intrinsic electrode potential phi from measured half-cell E=phi_working-phi_reference.",
            "Use dE/dT for the same reference system as the fitted voltage.",
            "Write qdot_rev,gen=-I_lith*T*dE/dT and derive every label mapping from I_lith.",
        ],
        "electronic_entropy": [
            "Preserve the Sommerfeld form only inside a verified metallic Fermi-liquid phase.",
            "Give DOS normalization explicitly: per formula unit, per Co, per Li site, or per atom; include spin convention.",
            "Treat the logistic g(E_F,x) curve and dx_MIT as empirical until composition-resolved data validate them.",
            "For a two-phase interval, use phase entropies, coexistence compositions, and the lever rule before any smooth observation convolution.",
            "Do not infer a local peak height from an endpoint DOS without uncertainty propagation.",
        ],
        "doping_and_high_voltage": [
            "Separate Li-site, Co-site, O-site, bulk, gradient, and surface modifications.",
            "Represent at least phase free energy, oxygen chemical stability, electronic structure, strain, transport, and interface reactions as distinct mechanisms.",
            "Do not map all doping effects to Omega; use Omega only for the specifically calibrated transition free-energy term.",
            "Require actual doped-LCO data and a >4.2 V voltage domain before claiming high-voltage coverage.",
        ],
        "theory_to_code": [
            "Implement composition-resolved dS_e(x,T) or remove that claim from the theory contract.",
            "Implement the integrated T-slope consistently, including T-squared curvature when dS_e is linear in T.",
            "Bind heat current sign to the same reaction coordinate used by the curve path.",
            "Make all material numbers explicit fit priors, never universal defaults.",
        ],
    }


def findings() -> list[dict]:
    return [
        {
            "id": "LH-059-01",
            "topic": "electrode_thermodynamic_identity",
            "disposition": "PRESERVE_WITH_EXPLICIT_REACTION_COORDINATE",
            "finding": (
                "For the written lithiation reaction, E=-DeltaG/F and "
                "dE/dT=DeltaS/F are correct."
            ),
            "defect": (
                "The reference electrode and reaction-current coordinate "
                "must be fixed before applying the identity."
            ),
        },
        {
            "id": "LH-059-02",
            "topic": "lco_temperature_coefficient_anchor",
            "disposition": "REJECT_REFERENCE_CONFLATION_AND_SIGN",
            "finding": (
                "The cited +0.83 mV/K is an inferred intrinsic LCO "
                "single-electrode coefficient."
            ),
            "defect": (
                "The manuscript applies it to U versus Li. The same primary "
                "paper reports -0.25 mV/K for the isothermal Li|LCO "
                "half-cell, reversing the entropy sign."
            ),
        },
        {
            "id": "LH-059-03",
            "topic": "direction_and_current_labels",
            "disposition": "CORRECT_TO_SIGNED_REACTION_CURRENT",
            "finding": (
                "The delithiation slot is internally mapped for curve "
                "generation."
            ),
            "defect": (
                "The heat API takes an unrelated signed I, while the same "
                "word discharge denotes opposite graphite chemical "
                "directions in the curve and heat prose."
            ),
        },
        {
            "id": "LH-059-04",
            "topic": "reversible_heat_identity",
            "disposition": "PRESERVE_WITH_SIGN_AND_OMITTED_TERM_BOUNDARY",
            "finding": (
                "qdot_rev=-I*T*dE/dT is correct for a matched "
                "discharge-positive cell convention."
            ),
            "defect": (
                "A half-electrode implementation must bind I to the written "
                "reaction, and the reduced equation must retain the "
                "mixing/phase-change omission boundary."
            ),
        },
        {
            "id": "LH-059-05",
            "topic": "sommerfeld_functional_form",
            "disposition": "PRESERVE_ONLY_IN_VERIFIED_METALLIC_REGIME",
            "finding": (
                "S_e=(pi^2/3)k_B^2*T*g(E_F) is the leading metallic "
                "Sommerfeld result with a declared DOS convention."
            ),
            "defect": (
                "It cannot be carried unchanged through a strongly "
                "composition-dependent first-order MIT without validating "
                "the Fermi-liquid and smooth-DOS assumptions."
            ),
        },
        {
            "id": "LH-059-06",
            "topic": "dos_13_anchor",
            "disposition": "REJECT_TIER_A_PER_ATOM_PROMOTION",
            "finding": (
                "Motohashi et al. infer 13 electrons/eV for CoO2 from "
                "susceptibility under a Pauli assumption."
            ),
            "defect": (
                "It is not stated as a direct 13 e/eV/atom measurement, "
                "and the x=0 endpoint does not validate a gate at x~0.85."
            ),
        },
        {
            "id": "LH-059-07",
            "topic": "mit_logistic_gate",
            "disposition": "EMPIRICAL_ONLY",
            "finding": (
                "The gate is smooth, differentiable, and its integrated "
                "entropy tracks the chosen endpoint difference."
            ),
            "defect": (
                "No cited primary source supplies the continuous g(E_F,x) "
                "or dx=0.05. The -46 J/(mol K) depth scales as 1/dx and is "
                "a model output, not a measured anchor."
            ),
        },
        {
            "id": "LH-059-08",
            "topic": "mit_two_phase_thermodynamics",
            "disposition": "CORRECT_TO_COEXISTENCE_AND_LEVER_RULE",
            "finding": (
                "Primary literature supports a 0.75<=x<=0.94 biphasic "
                "metal-insulator interval."
            ),
            "defect": (
                "A homogeneous smooth DOS derivative across that interval "
                "replaces phase coexistence by an unstated observation "
                "regularization."
            ),
        },
        {
            "id": "LH-059-09",
            "topic": "entropy_component_decomposition",
            "disposition": "PRESERVE_AS_CANDIDATE_WITH_COUPLING_RESIDUAL",
            "finding": (
                "Reynier et al. support configurational, phonon, and "
                "electronic contributions and comparable config/electronic "
                "changes at the MIT."
            ),
            "defect": (
                "The simple additive factorization neglects coupling and "
                "does not identify the proposed gate from measured entropy."
            ),
        },
        {
            "id": "LH-059-10",
            "topic": "temperature_integration",
            "disposition": "PRESERVE_THEORY_REJECT_IMPLEMENTATION_MATCH",
            "finding": (
                "If DeltaS_e=a_e*T at fixed composition, the integrated "
                "center contains a_e(T^2-T_ref^2)/(2F)."
            ),
            "defect": (
                "The code freezes both x and T at 298.15 K and produces "
                "zero T-squared curvature."
            ),
        },
        {
            "id": "LH-059-11",
            "topic": "composition_mapping",
            "disposition": "FAIL_THEORY_CODE_CONFORMANCE",
            "finding": (
                "The theory declares DeltaS_e(x,T) and a voltage-composition "
                "mapping."
            ),
            "defect": (
                "Production code evaluates the gate only at tr['x_center']; "
                "the electronic term is a constant offset across the peak."
            ),
        },
        {
            "id": "LH-059-12",
            "topic": "lco_transition_map",
            "disposition": "REJECT_AS_MATERIAL_SPECIFIC_MAPPING",
            "finding": (
                "The theory lists about 3.90, 4.05, and 4.17 V transitions."
            ),
            "defect": (
                "Code defaults produce about 3.93, 3.88, and 4.05 V, omit "
                "the 4.17 V transition, and are demonstration priors only."
            ),
        },
        {
            "id": "LH-059-13",
            "topic": "doping_mechanism",
            "disposition": "REJECT_SCALAR_OMEGA_ONLY_GENERALIZATION",
            "finding": (
                "Doping can alter phase transitions, so a calibrated Omega "
                "change may be one reduced contribution."
            ),
            "defect": (
                "Primary evidence shows site-specific and competing oxygen, "
                "structure, and electronic effects. LCO code has neither "
                "doping variables nor Omega values."
            ),
        },
        {
            "id": "LH-059-14",
            "topic": "doped_high_voltage_coverage",
            "disposition": "FAIL_SCOPE_ABSENT",
            "finding": (
                "The theory names an optional ~4.55 V O3-H1-3 transition."
            ),
            "defect": (
                "It is out of scope; the code has no center above 4.15 V "
                "and no doped-LCO experimental profile or fit path."
            ),
        },
        {
            "id": "LH-059-15",
            "topic": "ml2024_citation_support",
            "disposition": "CORRECT_CITATION_AND_REJECT_CLAIM_SUPPORT",
            "finding": (
                "The cited work provides a first-principles order-disorder "
                "free-energy/phase-field framework."
            ),
            "defect": (
                "The correct article/DOI is 105726, not 105727, and the "
                "paper explicitly does not capture the MIT plateau; it "
                "cannot validate the electronic gate."
            ),
        },
        {
            "id": "LH-059-16",
            "topic": "graphite_electronic_entropy",
            "disposition": "CORRECT_ABSENCE_TO_QUANTIFIED_NEGLECT",
            "finding": (
                "A small electronic contribution may be neglected in a "
                "bounded graphite fit."
            ),
            "defect": (
                "The categorical 'absent in graphite' wording is not a "
                "thermodynamic identity and needs a dataset-specific error "
                "bound."
            ),
        },
    ]


def report_text(result: dict) -> str:
    numeric = result["numerical_rederivation"]
    reference = numeric["potential_reference_rederivation"]
    gate = numeric["sommerfeld_gate_rederivation"]
    temp = numeric["theory_code_temperature_contract"]
    transitions = numeric["transition_map"]
    rows = [
        (
            f"| {item['id']} | {item['topic']} | "
            f"{item['disposition']} | {item['defect']} |"
        )
        for item in result["findings"]
    ]
    lines = [
        "# Phase 059 v1.0.14 LCO·열·부호 독립 재유도",
        "",
        "정본일: 2026-07-28",
        "",
        f"판정: `{result['status']}`",
        "",
        "## 결론",
        "",
        "전극 반응에 대해 `E=-DeltaG/F`, `dE/dT=DeltaS/F`와",
        "`q_rev,gen=-I_lith*T*dE/dT`의 열역학 골격은 보존한다.",
        "Sommerfeld 전자 엔트로피와 T-선형 엔트로피를 적분한 T² 중심",
        "곡률도 각각의 가정 안에서는 대수적으로 맞다.",
        "",
        "그러나 v1.0.14의 LCO 정량화와 구현 정합은 통과하지 못한다.",
        "가장 큰 오류는 +0.83 mV/K의 intrinsic single-electrode",
        "coefficient를 Li 기준 half-cell 전압 기울기로 사용한 것이다.",
        "인용 원 논문이 보고한 isothermal Li|LCO half-cell 값은",
        "-0.25 mV/K이므로 엔트로피 anchor의 부호가 뒤집힌다.",
        "",
        "## 전위 기준과 열 부호",
        "",
        "같은 Faraday 상수로 역산하면:",
        "",
        (
            f"- manuscript +0.83 mV/K -> "
            f"{reference['manuscript_intrinsic_entropy_J_per_mol_K']:.3f} "
            "J/(mol K)"
        ),
        (
            f"- measured Li|LCO -0.25 mV/K -> "
            f"{reference['measured_half_cell_entropy_J_per_mol_K']:.3f} "
            "J/(mol K)"
        ),
        (
            "- inferred intrinsic difference "
            f"(0.83-1.03) mV/K = "
            f"{reference['intrinsic_difference_V_per_K'] * 1e3:.3f} mV/K"
        ),
        "",
        "따라서 문건의 `+80 J/(mol K)` 검산은 문건이 실제로 피팅하는",
        "`V vs Li/Li+` 좌표의 검산이 아니다. 최종 문건은 intrinsic",
        "전극전위와 reference를 포함한 half-cell voltage를 분리해야 한다.",
        "열 부호도 charge/discharge 문자열이 아니라 삽입 반응 진행을 양으로",
        "정한 `I_lith`에 연결해야 한다.",
        "",
        "## 전자 엔트로피 gate",
        "",
        "금속상에서 다음 Sommerfeld 선도항은 보존한다:",
        "",
        "`S_e=(pi^2/3) k_B^2 T g(E_F)`.",
        "",
        "하지만 Motohashi 원문은 susceptibility 차이를 Pauli 성분으로",
        "가정해 CoO2에 대해 `13 electrons/eV`를 계산한다. 인용 구절은",
        "직접 DOS 측정도 아니고 `per atom`이라고 쓰지도 않는다. 더구나",
        "x=0 끝점을 x~0.85 MIT의 연속곡선 높이로 옮기는 근거가 없다.",
        "",
        (
            f"현재 gate는 298.15 K에서 endpoint S_e="
            f"{gate['endpoint_electronic_entropy_kB']:.4f} k_B, "
            f"중심 깊이={gate['gate_center_dS_code_J_per_mol_K']:.3f} "
            "J/(mol K)를 만든다."
        ),
        (
            f"x=1에서도 g={gate['g_at_x_1_e_per_eV']:.4f} e/eV "
            f"({100 * gate['x_1_residual_fraction']:.2f}% residual)다."
        ),
        "",
        "중심 깊이는 `1/dx_MIT`에 비례하므로 -46이라는 수치는",
        "`dx_MIT=0.05` 선택의 산출물이다. 원문들이 지지하는 것은",
        "0.75<=x<=0.94의 전자전이·2상역이지 이 유일한 smooth gate가",
        "아니다. 두-상 구간은 우선 두 상의 엔트로피, 공존 조성, lever",
        "rule로 닫고 실험 분해능이 필요할 때만 observation convolution을",
        "별도로 두어야 한다.",
        "",
        "## 이론과 코드",
        "",
        (
            "문건은 전자 엔트로피의 T-선형성과 "
            "`a_e(T^2-T_ref^2)/(2F)`를 유도하지만 코드는 "
            "`x_center`와 298.15 K에서 전자항을 동결한다."
        ),
        (
            f"268.15/298.15/328.15 K code center second difference는 "
            f"{temp['code_center_second_difference_V']:.3e} V, "
            f"이론 gate가 요구하는 값은 "
            f"{temp['theory_expected_symmetric_second_difference_V']:.3e} V다."
        ),
        "즉 조성 의존 gate와 T² 곡률은 둘 다 미구현이다.",
        "",
        (
            "이론 전이 중심은 "
            f"{transitions['theory_centers_V']} V, code는 "
            f"{[round(v, 6) for v in transitions['code_centers_V_at_298p15K']]} "
            "V다."
        ),
        "4.17 V 전이가 없고 4.15 V보다 높은 중심은 0개다. 도핑 변수,",
        "LCO Omega, 실제 doped high-voltage 데이터 경로도 없다.",
        "",
        "## 고전압 도핑",
        "",
        "도핑을 `Omega_pure -> Omega_dop` 하나로 줄이는 것은 정본 후보가",
        "될 수 없다. 2024년 Er/Mg LCO 1차 연구는 Mg의 Co-site 치환이",
        "~4.2 V 상전이를 억제하면서도 >4.45 V 산소 안정성을 악화시킬",
        "수 있고, Li-site Er은 산소 안정화를 담당함을 보인다. 즉 site,",
        "전자구조, 산소 화학, 정합변형, 수송, 표면반응을 분리해야 한다.",
        "",
        "## 문헌 정정",
        "",
        "v1.0.14의 `ml2024`는 article/DOI를 105727로 적었지만 실제는",
        "105726이다. 더 중요하게 그 논문은 MIT plateau를 포착하지",
        "못한다고 명시하므로 logistic electronic gate의 검증 근거가 아니다.",
        "",
        "## 직접 대조한 1차 문헌",
        "",
        "- [Swiderska-Mocek et al. 2019](https://doi.org/10.1039/C8CP06638H)",
        "- [Motohashi et al. 2009](https://doi.org/10.1103/PhysRevB.80.165114)",
        "- [Ménétrier et al. 1999](https://doi.org/10.1039/A900016J)",
        "- [Reynier et al. 2004](https://doi.org/10.1103/PhysRevB.70.174304)",
        "- [Bernardi et al. 1985](https://doi.org/10.1149/1.2113792)",
        "- [Shojaei et al. 2024](https://doi.org/10.1016/j.jmps.2024.105726)",
        "- [Xia et al. 2024](https://doi.org/10.1002/smll.202311578)",
        "",
        "## 판정표",
        "",
        "| ID | topic | disposition | blocker/debt |",
        "|---|---|---|---|",
        *rows,
        "",
        "## 다음 단계",
        "",
        "Step 36.4에서 v1.0.14의 kinetics/barrier/current broadening",
        "사슬을 독립 재유도하고, 저온×유한전류에서 peak suppression과",
        "broadening을 낼 수 있는지 theory-code joint limit로 판정한다.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    source_hashes_before = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in (CH1, CH2, CODE)
    }
    ch1 = CH1.read_text(encoding="utf-8")
    ch2 = CH2.read_text(encoding="utf-8")
    code = CODE.read_text(encoding="utf-8")
    module = load_v1014_module()
    finding_list = findings()
    result = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "scope": (
            "Phase 059 Step 36.3 independent LCO electronic entropy, "
            "electrode-reference sign, reversible heat, transition map, "
            "and doped high-voltage scope audit"
        ),
        "authority_boundary": (
            "Historical-document and implementation audit only; not a "
            "validated doped-LCO parameterization or final theory."
        ),
        "source_hashes_before": source_hashes_before,
        "source_contracts": source_contracts(ch1, ch2, code),
        "primary_source_checks": PRIMARY_SOURCES,
        "numerical_rederivation": numerical_rederivation(module),
        "canonical_repair_contract": canonical_repair_contract(),
        "findings": finding_list,
        "summary": {
            "finding_count": len(finding_list),
            "preserve_family_count": sum(
                item["disposition"].startswith("PRESERVE")
                for item in finding_list
            ),
            "correct_family_count": sum(
                item["disposition"].startswith("CORRECT")
                for item in finding_list
            ),
            "reject_family_count": sum(
                item["disposition"].startswith("REJECT")
                for item in finding_list
            ),
            "fail_family_count": sum(
                item["disposition"].startswith("FAIL")
                for item in finding_list
            ),
            "empirical_only_count": sum(
                item["disposition"] == "EMPIRICAL_ONLY"
                for item in finding_list
            ),
            "primary_source_count": len(PRIMARY_SOURCES),
            "half_cell_reference_closure_pass": False,
            "electronic_gate_external_validation_pass": False,
            "theory_code_electronic_conformance_pass": False,
            "doped_high_voltage_coverage_pass": False,
            "heat_identity_algebra_pass": True,
        },
        "status": (
            "CONDITIONAL_P059_V1014_LCO_HEAT_ALGEBRA_PRESERVED_WITH_"
            "REFERENCE_DOS_GATE_CODE_AND_DOPING_BLOCKERS"
        ),
        "next_action": (
            "Phase 059 Step 36.4 independently rederive the v1.0.14 "
            "kinetics/barrier/current-broadening chain and adjudicate the "
            "low-temperature finite-current joint limit."
        ),
    }
    source_hashes_after = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in (CH1, CH2, CODE)
    }
    result["source_hashes_after"] = source_hashes_after
    result["source_unchanged"] = source_hashes_after == source_hashes_before
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    REPORT.write_text(report_text(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "report": str(REPORT.relative_to(ROOT)),
                "status": result["status"],
                "summary": result["summary"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
