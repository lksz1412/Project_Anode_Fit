#!/usr/bin/env python3
"""Generate the Phase 059 Step 38.5 future-physics roadmap disposition."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json"
ROADMAP = "Claude/docs/v1.0.18.2/ROADMAP_future_physics.md"
BASELINE_COMMIT = "1cf955ba347218676a73bdae0a9eb8add8e1581a"
CODE = "Claude/docs/v1.0.18.2/Anode_Fit_v1.0.18.2.py"
TEST_REVIEW = "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_REVIEW.md"
TEST_MATRIX = "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json"
THEORY_REVIEW = "Codex/results/PHASE_059_THEORY_CONTRACT_REVIEW.md"
THEORY_MATRIX = "Codex/results/PHASE_059_THEORY_CONTRACT_MATRIX.json"
CODE_REVIEW = "Codex/results/PHASE_059_PRODUCTION_CODE_REVIEW.md"
CODE_INDEX = "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json"
PS_REVIEW = "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_REVIEW.md"
PS_AUDIT = "Codex/results/PHASE_059_V1014_PHASE_SEPARATION_AUDIT.json"
KIN_REVIEW = "Codex/results/PHASE_059_V1014_KINETICS_REVIEW.md"
KIN_AUDIT = "Codex/results/PHASE_059_V1014_KINETICS_AUDIT.json"
NT_REVIEW = "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_REVIEW.md"
NT_AUDIT = "Codex/results/PHASE_059_V1016_NT_WIDTH_LAW_AUDIT.json"
IDENT_REVIEW = "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_REVIEW.md"
IDENT_AUDIT = "Codex/results/PHASE_059_V1016_JOINT_IDENTIFIABILITY_AUDIT.json"
EIN_REVIEW = "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_REVIEW.md"
EIN_AUDIT = "Codex/results/PHASE_059_V1018_2_EINSTEIN_THEORY_AUDIT.json"
EIN_FP_REVIEW = "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_REVIEW.md"
EIN_FP_AUDIT = "Codex/results/PHASE_059_V1018_2_EINSTEIN_FULLPATH_AUDIT.json"

INPUT_PATHS = [
    ROADMAP,
    "Claude/docs/v1.0.18.2/HANDOVER_v1.0.18.2.md",
    "Claude/docs/v1.0.18.2/FITTING_GUIDE.md",
    CODE,
    "Claude/docs/v1.0.18.2/test_regression_graphite.py",
    "Claude/docs/v1.0.18.2/sample_test_v1018_2.py",
    "Claude/docs/v1.0.18.2/graph_suite_v1018_2.py",
    THEORY_REVIEW,
    THEORY_MATRIX,
    CODE_REVIEW,
    CODE_INDEX,
    TEST_REVIEW,
    TEST_MATRIX,
    PS_REVIEW,
    PS_AUDIT,
    KIN_REVIEW,
    KIN_AUDIT,
    NT_REVIEW,
    NT_AUDIT,
    IDENT_REVIEW,
    IDENT_AUDIT,
    EIN_REVIEW,
    EIN_AUDIT,
    EIN_FP_REVIEW,
    EIN_FP_AUDIT,
    "Codex/plans/2026-08-25-phase059-resume-closure-detailed-plan.md",
]
TOPIC_BY_ITEM_ID = {
    "P059-RM-001": "other",
    "P059-RM-002": "interaction",
    "P059-RM-003": "phase_field",
    "P059-RM-004": "transport",
    "P059-RM-005": "particle_size",
    "P059-RM-006": "data",
    "P059-RM-007": "data",
    "P059-RM-008": "data",
    "P059-RM-009": "data",
    "P059-RM-010": "data",
    "P059-RM-011": "other",
    "P059-RM-012": "data",
}


def git_blob(path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def evidence(path: str, anchor: str, finding: str) -> dict[str, str]:
    return {"path": path, "anchor": anchor, "finding": finding}


def roadmap_text(lines: list[str], specification: str) -> str:
    selected: list[str] = []
    for part in specification.split(","):
        bounds = part.strip().split("-", 1)
        start = int(bounds[0])
        end = int(bounds[1]) if len(bounds) == 2 else start
        selected.extend(lines[start - 1 : end])
    return "\n".join(selected)


def recursive_node_count(value: Any) -> int:
    """Traverse every parsed JSON node so full semantic parse is auditable."""
    if isinstance(value, dict):
        return 1 + sum(recursive_node_count(key) + recursive_node_count(child) for key, child in value.items())
    if isinstance(value, list):
        return 1 + sum(recursive_node_count(child) for child in value)
    return 1


def item(
    roadmap_lines: list[str],
    item_id: str,
    source_lines: str,
    atomic_topic: str,
    primary_classification: str,
    secondary_status: list[str],
    theory_evidence: list[dict[str, str]],
    code_evidence: list[dict[str, str]],
    test_evidence: list[dict[str, str]],
    artifact_evidence: list[dict[str, str]],
    data_prerequisites: list[str],
    literature_prerequisites: list[str],
    acceptance_criterion: str,
    authority_boundary: str,
) -> dict[str, Any]:
    return {
        "item_id": item_id,
        "source_path": ROADMAP,
        "source_lines": source_lines,
        "source_text": roadmap_text(roadmap_lines, source_lines),
        "topic": TOPIC_BY_ITEM_ID[item_id],
        "atomic_topic": atomic_topic,
        "primary_classification": primary_classification,
        "secondary_status": secondary_status,
        "theory_evidence": theory_evidence,
        "code_evidence": code_evidence,
        "test_evidence": test_evidence,
        "artifact_evidence": artifact_evidence,
        "data_prerequisites": data_prerequisites,
        "literature_prerequisites": literature_prerequisites,
        "acceptance_criterion": acceptance_criterion,
        "authority_boundary": authority_boundary,
    }


def build_items(roadmap_lines: list[str]) -> list[dict[str, Any]]:
    missing_headline_tests = [
        evidence(
            TEST_REVIEW,
            "P059-TD-011; lines 36-37",
            "The complete release harness inventory contains no n_T1 or theta_E activation.",
        ),
        evidence(
            TEST_MATRIX,
            "finding P059-TD-011",
            "Machine evidence records both headline post-v1.0.15 feature tokens as missing.",
        ),
    ]
    no_external_data = evidence(
        TEST_REVIEW,
        "P059-TD-013; lines 38 and 55-56",
        "No public experimental dataset is loaded by the release tests or demos.",
    )

    return [
        item(
            roadmap_lines,
            "P059-RM-001",
            "3, 10",
            "einstein_vibration",
            "IMPLEMENTED",
            [
                "PARTIAL",
                "DORMANT",
                "INTERNAL_CAPABILITY_ONLY",
                "UNVALIDATED",
                "PUBLIC_PARAMETER_CONTRACT_OPEN",
                "PERSISTENT_TEST_MISSING",
            ],
            [
                evidence(THEORY_REVIEW, "P059-CON-030..032; lines 37-39", "One-mode algebra and reference round-trip are preserved, but a reaction-spectrum definition is open."),
                evidence(EIN_REVIEW, "lines 9-41", "Independent rederivation passes the single-oscillator algebra while rejecting material/reaction-spectrum authority."),
            ],
            [
                evidence(CODE, "lines 341-383, 449-459, 545, 621-678", "Einstein helpers feed the public equilibrium, dQ/dV, entropy, and reversible-heat paths."),
                evidence(CODE_REVIEW, "P059-CODE-009 and P059-CODE-013; lines 31 and 35", "The capability is dormant in defaults and the positive Tref guard is incomplete."),
            ],
            missing_headline_tests,
            [
                evidence(EIN_AUDIT, "findings EIN-001..EIN-012; summary", "Algebra and reference round-trip pass; general reaction spectrum and material validation fail."),
                evidence(EIN_FP_AUDIT, "validation, findings FP-001..FP-012", "Active full-path conformance passes, while U-only silent ignore, Tref guard, and persistent regression fail."),
            ],
            [
                "At least three controlled temperatures spanning the Einstein-curvature window, preferably on both sides of Tref, on the same specimen and state definition.",
                "Quasi-equilibrium or rest-qualified OCV/entropy data with temperature, SOC/composition, protocol, replicate uncertainty, voltage resolution, and thermal equilibration metadata.",
                "Independent phonon or heat-capacity constraints sufficient to distinguish vibrational curvature from electronic, width, and baseline terms.",
            ],
            [
                "Reaction-resolved product-minus-reactant phonon spectra or a cited signed mode-amplitude reduction; the existing one absolute oscillator is insufficient.",
                "Primary-source support for any material theta_E or mode multiplicity; theta_E=700 K remains a capability demonstration only.",
            ],
            "Reject or define theta_E on U-only transitions, enforce theta_E_Tref>0, add persistent absent/active scalar-array/derivative/heat tests, define reaction-resolved signed spectral amplitude, and pass held-out multi-temperature material validation with uncertainty.",
            "IMPLEMENTED means a callable production path exists. It does not establish default activation, a complete public parameter contract, persistent release coverage, reaction-spectrum completeness, or graphite/LCO material validity.",
        ),
        item(
            roadmap_lines,
            "P059-RM-002",
            "18-23",
            "interaction_composition",
            "NEW_SCOPE",
            ["PRODUCTION_ABSENT", "CONSTANT_OMEGA_ONLY", "HIGH_INTRUSION", "DATA_DEPENDENT", "LITERATURE_DFT_REQUIRED"],
            [
                evidence(THEORY_REVIEW, "P059-CON-006 and P059-CON-007; lines 13-14", "The frozen theory closes only the symmetric constant-Omega regular-solution baseline."),
                evidence(THEORY_MATRIX, "records P059-CON-006 and P059-CON-007", "The machine contract limits closed forms to a symmetric regular solution and theory-only phase closure."),
            ],
            [
                evidence(CODE, "lines 138-152, 550-554, 804-833", "Production reads one scalar Omega per transition and has no Omega(xi) or sublattice law."),
                evidence(CODE_INDEX, "v1.0.18.2 module public API and datasets", "The complete production inventory exposes scalar Omega parameters only."),
            ],
            [
                evidence(TEST_REVIEW, "P059-TD-012 and P059-TD-013; lines 37-38", "Critical new physics branches and public experimental data are absent from the release harnesses."),
            ],
            [
                evidence(CODE_REVIEW, "lines 19-35", "The production finding inventory contains no composition-dependent interaction capability."),
                evidence(PS_AUDIT, "findings PS-059-01..PS-059-10", "The preserved phase-separation asset is the symmetric regular-solution baseline, not a nonuniform interaction law."),
            ],
            [
                "Composition-resolved equilibrium and metastable voltage data across all graphite staging intervals and LCO T2/T3, with temperature, rate, rest/equilibrium, specimen, phase identity, and voltage-resolution metadata.",
                "Matched nonuniform staging/LCO symmetry observations or first-principles ordering energies capable of constraining Omega0, Omega1, and any sublattice parameters.",
            ],
            [
                "Primary literature or DFT establishing the composition dependence and symmetry form of the interaction energy for each material; no Omega1 value may be inferred from the roadmap prose.",
                "A source-backed mapping from graphite layer interactions and LCO Li-vacancy ordering to the chosen free-energy variables.",
            ],
            "Derive a dimensionally and symmetrically defined Omega(xi) or sublattice free energy, implement it through equilibrium/spinodal/hysteresis paths, add limiting tests recovering constant Omega, and validate nonuniform staging/LCO asymmetry on independent composition-resolved data.",
            "The current constant-Omega theory/code does not count as implementation of Omega(xi). This classification neither selects the proposed linear law nor validates a material interaction parameter.",
        ),
        item(
            roadmap_lines,
            "P059-RM-003",
            "25-29",
            "phase_field_hysteresis",
            "THEORY_ONLY",
            [
                "THEORY_BASELINE_PRESENT",
                "DIMENSIONAL_FORM_REPAIRED_IN_V1018_2",
                "PRODUCTION_ABSENT",
                "QUANTITATIVE_CLOSURE_NEW_SCOPE",
                "MOBILITY_BC_ELASTICITY_COARSE_GRAINING_OPEN",
            ],
            [
                evidence(THEORY_REVIEW, "P059-CON-008..010; lines 15-17", "Gamma hysteresis remains empirical; Cahn-Hilliard exists as a theory-only dimensional baseline without production closure."),
                evidence(PS_REVIEW, "lines 9-18 and 39-112", "The historical derivation rederives algebra but requires dimensional, mobility, boundary-condition, elasticity, and solid-electrode boundaries."),
            ],
            [
                evidence(CODE, "lines 138-152 and 549-554", "Production consumes gamma as a scalar input to the branch shift; it does not derive gamma from Cahn-Hilliard or nucleation physics."),
                evidence(CODE_INDEX, "v1.0.18.2 module functions and transition keys", "The complete API inventory has no kappa, mobility, boundary-condition, phase-field, or gamma-derivation solver."),
            ],
            [
                evidence(TEST_REVIEW, "P059-TD-012; lines 37 and 51-54", "No release gate covers a phase-field/gamma derivation; major physics branches remain untested."),
            ],
            [
                evidence(PS_AUDIT, "canonical_repair_contract; findings PS-059-03..PS-059-10", "Quantitative use requires units, flux/mobility, boundaries, elasticity scope, and nucleation assumptions."),
                evidence(THEORY_MATRIX, "records P059-CON-008..P059-CON-010", "The machine contracts distinguish empirical gamma, theory-only CH, and open production two-phase closure."),
            ],
            [
                "Time-resolved phase evolution and charge/discharge hysteresis loops versus temperature, current/rate, rest history, particle size, specimen geometry, and microstructure.",
                "Independent interfacial energy, gradient coefficient, mobility/diffusivity, molar/site density, elastic constants, coherent strain, surface wetting, nucleation-site, and boundary-condition evidence.",
            ],
            [
                "Primary sources supporting the dimensional phase-field functional, solid coherency/elastic boundary, nucleation regime, and the coarse-graining from phase fields to an observed gamma_j and L_V.",
            ],
            "Close units, mobility, boundary conditions, elasticity and surface/nucleation assumptions; derive an explicit coarse-graining from the phase-field solution to gamma_j and hysteresis/L_V; implement conservation/dissipation tests and validate against rate-temperature-size-resolved hysteresis data.",
            "THEORY_ONLY recognizes a frozen analytical baseline, not a production solver or quantitative gamma_j prediction. Promoting the baseline and fitting material parameters remains NEW_SCOPE.",
        ),
        item(
            roadmap_lines,
            "P059-RM-004",
            "31-35",
            "kinetics_transport",
            "NEW_SCOPE",
            ["TRANSPORT_SOLVER_ABSENT", "LUMPED_RN_ONLY", "SIMPLE_RELAXATION_ONLY", "DATA_DEPENDENT", "CURRENT_BALANCE_OPEN"],
            [
                evidence(THEORY_REVIEW, "P059-CON-001, P059-CON-016..021", "Existing theory is a lumped polarization and reduced causal-memory model with open current, local-affinity, unit, and protocol contracts."),
                evidence(KIN_REVIEW, "lines 104-118 and KIN-059-04..KIN-059-20", "A mechanistic extension must close local affinity, charge transfer, diffusion/porous transport, current conservation, and terminal voltage."),
            ],
            [
                evidence(CODE, "lines 511-512 and 695-701", "Production subtracts lumped I*Rn and explicitly leaves irreversible heat decomposition as a future task."),
                evidence(CODE_REVIEW, "P059-CODE-006 and P059-CODE-008; lines 28 and 30", "Current conversion and local-temperature kinetics are not closed, and no transport solver is reported."),
            ],
            [
                evidence(TEST_REVIEW, "P059-TD-012 and P059-TD-013; lines 37-38", "The release harness has no transport/current-balance branch coverage and no measured dataset."),
            ],
            [
                evidence(KIN_AUDIT, "findings KIN-059-03..KIN-059-20; repair_contract", "The voltage-grid relaxation is not a galvanostatic Butler-Volmer/Nernst-Planck forward model."),
                no_external_data,
            ],
            [
                "Electrochemical impedance spectroscopy over SOC/composition and temperature with frequency range, perturbation amplitude, geometry, porosity/tortuosity, electrolyte, and replicate uncertainty.",
                "Matched multi-rate and concentration/activity series with rest/GITT or current-interruption segments sufficient to separate charge transfer, electrolyte/solid transport, ohmic loss, and equilibrium Nernst shifts.",
            ],
            [
                "Primary transport/charge-transfer constitutive sources defining activities, transference, concentrated-solution assumptions, exchange current, boundary conditions, and the reduction to any Warburg or limiting-current approximation.",
            ],
            "Implement signed current balance and terminal-voltage closure with Butler-Volmer and concentration/activity transport, recover the lumped/equilibrium limits analytically, pass conservation/entropy-production/grid-convergence tests, and validate separated Rct/transport/Nernst contributions against held-out EIS and rate data.",
            "The existing Rn shift and first-order lag are reduced empirical capabilities, not a Butler-Volmer plus Nernst-Planck implementation and not evidence that kinetic and thermodynamic tails are separated.",
        ),
        item(
            roadmap_lines,
            "P059-RM-005",
            "37-41",
            "particle_size",
            "NEW_SCOPE",
            ["QUALITATIVE_THEORY_BASELINE_ONLY", "QUANTITATIVE_CONVOLUTION_ABSENT", "NANOSCALE_UNVALIDATED", "DATA_DEPENDENT", "ILL_POSED_INVERSION_BOUNDARY"],
            [
                evidence(THEORY_REVIEW, "P059-CON-013; line 20", "The preserved width/heterogeneity identity is empirical observation-level theory, not a quantitative particle-size law."),
                evidence(THEORY_MATRIX, "record P059-CON-013", "A normalized apparent-potential distribution is only a preserved observation hypothesis requiring microstructural inference."),
            ],
            [
                evidence(CODE_INDEX, "all four production modules: public_api, functions, datasets", "The complete production inventory contains no PSD, radius distribution, Gibbs-Thomson, or finite-N convolution path."),
            ],
            [
                evidence(TEST_MATRIX, "all 30 records: feature_tokens and model_calls", "The complete test/demo inventory contains no PSD/nanoscale activation or quantitative particle-size gate."),
            ],
            [
                evidence(CODE_REVIEW, "lines 8-17 and 19-35", "The production lineage inventory records no particle-size implementation."),
                no_external_data,
            ],
            [
                "Measured number-, area-, and volume-weighted particle-size distributions for the actual graphite, Si, and LCO specimens, including agglomeration, morphology, uncertainty, and resolution limits.",
                "Surface/interfacial energy, molar volume, phase/coherency state, particle geometry, finite-site/finite-N evidence, and size-resolved equilibrium/ICA data across temperature and rate.",
            ],
            [
                "Primary support for the chosen Gibbs-Thomson sign/prefactor and its solid-electrode assumptions, plus the finite-N staging law and convolution measure.",
                "A source-backed reason that the selected effective-radius distribution is observable; unconstrained rho(U_app) inversion remains prohibited.",
            ],
            "Define a normalized measured-PSD forward convolution with surface/interfacial-energy and molar-volume units, recover the micron/infinite-N limits, preserve capacity, quantify resolution and ill-posedness, and validate held-out size-resolved nano-electrode curves.",
            "A qualitative identity and micron-scale exclusion estimate do not implement quantitative PSD convolution and do not justify extrapolation to nano Si or LCO.",
        ),
        item(
            roadmap_lines,
            "P059-RM-006",
            "46",
            "n_of_T_diagnostic",
            "NEW_SCOPE",
            ["PRODUCTION_CAPABILITY_PRESENT", "EMPIRICAL_ONLY", "PERSISTENT_TEST_MISSING", "DATA_TASK_UNEXECUTED", "IDENTIFIABILITY_CONDITIONAL"],
            [
                evidence(THEORY_REVIEW, "P059-CON-022..024; lines 29-31", "n(T) is an empirical width law with open extrapolation and joint-identifiability authority."),
                evidence(NT_REVIEW, "lines 9-30 and 51-69", "The opt-in product rule works, but the law is empirical, correlated, and lacks persistent release coverage."),
            ],
            [
                evidence(CODE, "lines 294-339 and 672-678", "Production can evaluate n(T), w(T), and dwdT on opt-in transitions."),
                evidence(CODE_REVIEW, "P059-CODE-007; line 29", "The no-n/no-w default width and derivative contract remains inconsistent."),
            ],
            missing_headline_tests,
            [
                evidence(NT_AUDIT, "mathematical_contract, persistent_test_coverage, findings, summary", "Capability conformance passes opt-in, while positivity, default conformance, persistent regression, and microscopic authority fail."),
                evidence(IDENT_AUDIT, "rank_analyses.n0_n1_single_temperature; minimum_evidence_contract.width_nt", "One temperature has rank 1/2; multiple temperatures and uncertainty/positivity constraints are required."),
            ],
            [
                "Per-transition peak widths at multiple measured temperatures, preferably on both sides of Tref, using the same specimen, direction, low-rate/rest-qualified protocol, voltage resolution, replicate uncertainty, and peak-overlap treatment.",
                "Held-out temperatures and domain-wide n(T)>0 bounds, with profile likelihood or equivalent uncertainty analysis for n1.",
            ],
            [
                "Literature is needed only to assign a microscopic interpretation; until then n(T) must remain an empirical width ratio rather than a multiplicity or phase mechanism.",
            ],
            "Execute the per-temperature diagnostic, demonstrate stable per-transition n estimates and uncertainty across held-out temperatures, enforce positivity on the full fitted domain, distinguish constant-n/constant-w/n(T), and add persistent n_T1 regression tests.",
            "The n(T) calculation is implemented, but the roadmap item is the unexecuted real-data diagnostic. Capability does not make the data task IMPLEMENTED or material-validated.",
        ),
        item(
            roadmap_lines,
            "P059-RM-007",
            "46",
            "two_phase_width_temperature",
            "NEW_SCOPE",
            ["THEORY_OBSERVATION_HYPOTHESIS", "PRODUCTION_MECHANISM_ABSENT", "DATA_TASK_UNEXECUTED", "SEMANTIC_ROLE_OPEN", "UNVALIDATED"],
            [
                evidence(THEORY_REVIEW, "P059-CON-010, P059-CON-013, P059-CON-015; lines 17, 20, 22", "The two-phase bell width is phenomenological and conflicts with an automatic ideal-configurational interpretation."),
                evidence(NT_REVIEW, "lines 25-30 and 71-76", "n(T) cannot be promoted to a phase-separation mechanism without identifying the width source."),
            ],
            [
                evidence(CODE, "lines 317-339 and 469-585", "Production supplies generic transition width and dwdT machinery but no distinct two-phase temperature-width mechanism."),
                evidence(CODE_INDEX, "v1.0.18.2 transition keys and public API", "No typed two-phase PSD/phase-field/heterogeneity width component exists."),
            ],
            [
                evidence(TEST_REVIEW, "P059-TD-011..P059-TD-013; lines 36-38", "No n(T), two-phase-mechanism, or public-data gate exists."),
            ],
            [
                evidence(NT_AUDIT, "finding two_phase_interpretation", "The audit explicitly forbids promoting n(T) to a phase mechanism."),
                evidence(THEORY_MATRIX, "records P059-CON-010, P059-CON-013, P059-CON-015", "Two-phase closure and the semantic role of width remain open."),
            ],
            [
                "Two-phase transition widths at multiple temperatures under quasi-equilibrium/rest-qualified protocols, with the same specimen, rate, direction, cycling history, voltage resolution, and uncertainty.",
                "Independent particle-size/heterogeneity, phase fraction, coherency, and instrument-resolution evidence needed to separate thermal, ensemble, kinetic, and observation broadening.",
            ],
            [
                "Primary support for the mechanism assigned to two-phase width; an ideal lattice-gas nRT/F identity cannot be reused by notation alone.",
            ],
            "Measure and model the two-phase width-temperature law with a distinct typed width component, demonstrate capacity conservation and mechanism discrimination, and validate held-out temperatures after separating heterogeneity, kinetics, phase-field, and measurement resolution.",
            "Generic n(T) and a phenomenological bell do not complete the roadmap's two-phase real-data diagnosis or establish a thermodynamic entropy interpretation.",
        ),
        item(
            roadmap_lines,
            "P059-RM-008",
            "47",
            "lco_omega_dha",
            "NEW_SCOPE",
            ["GENERIC_SCHEMA_CAPABILITY", "LCO_DEFAULT_VALUES_ABSENT", "DATA_TASK_UNEXECUTED", "MATERIAL_SCOPE_OPEN", "UNVALIDATED"],
            [
                evidence(THEORY_REVIEW, "P059-CON-033 and P059-CON-037; lines 40 and 44", "High-voltage/doped LCO and material parameter validation remain open."),
                evidence(KIN_REVIEW, "KIN-059-07, KIN-059-08, KIN-059-17; lines 140-141 and 150", "Migration barriers cannot be equated directly to mesoscopic transformation dH_a, and multi-T/multi-rate data are required."),
            ],
            [
                evidence(CODE, "lines 228-235 and 728-764", "The generic transition schema accepts optional Omega/dH_a, but actual LCO_MSMR_LIT entries omit both and line 764 states that they are unassigned."),
                evidence(CODE_REVIEW, "P059-CODE-011; line 33", "Doped high-voltage LCO scope is absent from defaults."),
            ],
            [no_external_data],
            [
                evidence(KIN_AUDIT, "findings KIN-059-07, KIN-059-08, KIN-059-17", "The kinetic barrier requires mesoscale coarse-graining and multi-temperature/rate relaxation evidence."),
                evidence(CODE_INDEX, "v1.0.18.2 public method transition_keys versus datasets.LCO_MSMR_LIT.transition_key_sets", "Generic methods recognize Omega/dH_a, while every actual LCO default key set omits both."),
            ],
            [
                "Composition-, phase-, and dopant-resolved LCO equilibrium/hysteresis and relaxation data with temperature, rate, rest/GITT, EIS/current-interruption, particle/electrode geometry, and uncertainty.",
                "A protocol that distinguishes homogeneous interaction Omega from transport, nucleation/phase-boundary motion, and mesoscopic activation dH_a.",
            ],
            [
                "Primary material-specific literature for LCO Omega and activation quantities, including reaction/state definition, composition/voltage range, dopant, units, and whether a value is microscopic migration or mesoscale relaxation.",
            ],
            "Replace placeholders only after source-backed parameter definitions and real-data estimation; demonstrate cross-temperature/rate recovery, uncertainty, and held-out validation for the target LCO material and voltage window.",
            "Generic schema support for Omega and dH_a is not an assigned LCO value. Actual LCO defaults omit both, so there is no real-constant, doped/high-voltage, or unique-mechanism authority.",
        ),
        item(
            roadmap_lines,
            "P059-RM-009",
            "47",
            "lco_electronic_temperature",
            "NEW_SCOPE",
            ["THEORY_BASELINE_PRESENT", "PRODUCTION_FROZEN_AT_298_15K", "T_SQUARED_LAW_ABSENT", "DATA_TASK_UNEXECUTED", "UNVALIDATED"],
            [
                evidence(THEORY_REVIEW, "P059-CON-034, P059-CON-036, P059-CON-038; lines 41, 43, 45", "Sommerfeld theory is bounded, while composition feedback, T-squared integration, and code conformance remain open."),
                evidence(IDENT_REVIEW, "lines 25-30 and 41-46", "The frozen LCO electronic gate is rank 1/4 and cannot be separated without composition-resolved multi-temperature priors."),
            ],
            [
                evidence(CODE, "lines 780-797", "The LCO electronic entropy seam evaluates the gate at a hard-coded 298.15 K reference."),
                evidence(CODE_REVIEW, "P059-CODE-010; line 32", "The claimed electronic temperature scale and T-squared center shift are absent in production."),
            ],
            [
                evidence(TEST_REVIEW, "P059-TD-008 and P059-TD-013; lines 33 and 38", "Graph-suite electronic checks are print-only and no public data are loaded."),
            ],
            [
                evidence(IDENT_AUDIT, "rank_analyses.lco_frozen_gate; findings lco_gate_current_code and lco_base_entropy", "The frozen gate is structurally rank deficient for the requested electronic parameters."),
                evidence(CODE_INDEX, "review finding P059-CODE-010", "Static code evidence confirms the hard-coded electronic reference temperature."),
            ],
            [
                "Composition-resolved LCO OCV/entropy or calorimetry at at least three well-separated temperatures, with the same specimen, equilibrium/rest protocol, SOC mapping, resolution, replicate uncertainty, and held-out temperatures.",
                "Independent electronic heat-capacity/DOS and phase-coexistence evidence sufficient to separate baseline, vibrational, configurational, and electronic curvature.",
            ],
            [
                "Primary support for the Sommerfeld/smooth-DOS validity range and the reaction-specific Li-reference entropy through the MIT; transition-region extrapolation requires direct evidence.",
            ],
            "Implement composition- and temperature-resolved electronic free energy with the correct reaction/reference and derivatives, recover the T-squared limit where justified, add numeric failure gates, and validate curvature on held-out multi-temperature LCO data.",
            "A theory equation and a frozen 298.15 K offset do not implement or validate the roadmap's multi-temperature T-squared/electronic data task.",
        ),
        item(
            roadmap_lines,
            "P059-RM-010",
            "47",
            "lco_composition_gate",
            "NEW_SCOPE",
            ["PRODUCTION_CAPABILITY_PRESENT", "PLACEHOLDER_CONSTANTS", "FROZEN_COMPOSITION_GATE", "DATA_TASK_UNEXECUTED", "JOINTLY_NONIDENTIFIABLE", "UNVALIDATED"],
            [
                evidence(THEORY_REVIEW, "P059-CON-035 and P059-CON-036; lines 42-43", "The g(EF,x) logistic is empirical and the x(V,T) fixed-point/chain-rule closure is open."),
                evidence(IDENT_REVIEW, "lines 25-30 and 41-46", "The current frozen evaluation cannot jointly identify g_max, x_MIT, gate width, and base entropy."),
            ],
            [
                evidence(CODE, "lines 174-190, 728-750, 780-797", "A logistic gate exists with placeholder g_max/x_MIT/dx_MIT values but is frozen at x_center and 298.15 K."),
                evidence(CODE_REVIEW, "P059-CODE-010 and P059-CODE-011; lines 32-33", "Composition-temperature coupling and target high-voltage material scope are absent."),
            ],
            [
                evidence(TEST_REVIEW, "P059-TD-007, P059-TD-008, P059-TD-013; lines 32-33 and 38", "LCO/electronic demos are print-only and have no external-data authority."),
            ],
            [
                evidence(IDENT_AUDIT, "rank_analyses.lco_frozen_gate and scenario_matrix", "The present gate has rank 1/4; composition-resolved nonfrozen data and priors are mandatory."),
                evidence(THEORY_MATRIX, "records P059-CON-035 and P059-CON-036", "The machine contracts mark the gate empirical and fixed-point/chain-rule closure open."),
            ],
            [
                "Composition-resolved x(V,T), DOS/electronic entropy or heat-capacity observations through the MIT, with dopant/material identity, phase state, equilibrium/rest, temperature, voltage resolution, and uncertainty.",
                "Independent measurements or priors that separate g_max, x_MIT, dx_MIT, base reaction entropy, phase coexistence, and vibrational curvature.",
            ],
            [
                "Primary composition-resolved DOS/entropy sources for the target LCO chemistry; endpoint values cannot authorize an invented continuous logistic curve.",
            ],
            "Replace the frozen placeholder with a source- and data-constrained x(V,T) model, solve its implicit coupling and chain rule, demonstrate parameter rank/uncertainty, and pass held-out composition-temperature material validation.",
            "The public gate function is a capability seam only. It does not make g_max/x_MIT measured constants or close composition feedback and material validity.",
        ),
        item(
            roadmap_lines,
            "P059-RM-011",
            "48",
            "bibliography",
            "NEW_SCOPE",
            ["RESIDUAL_RECHECK_INCOMPLETE", "SOURCE_IDENTITIES_NOT_ENUMERATED", "GROUND_NOT_FOUND", "NO_SCIENTIFIC_COMPLETION_AUTHORITY"],
            [
                evidence(THEORY_REVIEW, "lines 1-4", "The theory-contract review explicitly excludes final theory canon and external validity; it is not a bibliography truth audit."),
            ],
            [
                evidence(CODE_REVIEW, "lines 1-4", "The production-code review excludes theory conformance and experimental validity and provides no bibliography closure."),
            ],
            [
                evidence(TEST_REVIEW, "lines 1-5", "The test/demo review is a static assertion inventory, not literature verification."),
            ],
            [
                evidence(THEORY_MATRIX, "authority_boundary", "The machine theory artifact explicitly excludes literature verification."),
                evidence(EIN_AUDIT, "primary_scope_source", "One Einstein scope source is recorded, but it cannot close the roadmap's unspecified residual bibliography set."),
            ],
            [
                "A version-pinned bibliography inventory and atomic claim-to-citation map; no experimental dataset is required for the metadata audit itself.",
                "The exact seven author corrections, two DOI corrections, and every residual reference must be enumerated before closure can be tested.",
            ],
            [
                "For every residual item: publisher/DOI-resolver metadata and, for load-bearing claims, the primary full text with exact page/section/equation support.",
                "Author, title, journal, year, volume/issue, pages/article number, DOI, correction/retraction state, and claim-variable mapping must agree.",
            ],
            "Enumerate the corrected and residual bibliography records, verify metadata and load-bearing claims against primary sources, produce zero unresolved identity/DOI conflicts, and retain any inaccessible full text as explicitly unverified rather than inferred.",
            "The roadmap's statement that some corrections were completed is not accepted as authority. The mandatory corpus does not identify the residual records, so their completion status remains ground-not-found.",
        ),
        item(
            roadmap_lines,
            "P059-RM-012",
            "49",
            "joint_identifiability",
            "NEW_SCOPE",
            ["CAPABILITY_SEAMS_PRESENT", "IDENTIFIABILITY_FAIL", "PERSISTENT_TEST_MISSING", "DATA_TASK_UNEXECUTED", "LCO_ELECTRONIC_FROZEN", "UNVALIDATED"],
            [
                evidence(THEORY_REVIEW, "P059-CON-024; lines 31 and 65-66", "No demonstrated joint identifiability exists for n(T), reaction entropy, vibrational, and electronic terms."),
                evidence(IDENT_REVIEW, "lines 9-30 and 32-50", "The requested joint opening is rank deficient without multi-temperature/rate data and independent priors."),
            ],
            [
                evidence(CODE, "lines 621-678 and 780-797", "Vibrational, width-derivative, and electronic seams can add numerically, but the LCO electronic term is frozen and defaults omit theta_E/n_T1."),
                evidence(CODE_REVIEW, "P059-CODE-010 and P059-CODE-013; lines 32 and 35", "The electronic temperature law is frozen and Einstein capability is dormant."),
            ],
            missing_headline_tests,
            [
                evidence(IDENT_AUDIT, "rank_analyses, scenario_matrix, minimum_evidence_contract, summary", "Single-T n has rank 1/2; activation retains an exact null; the LCO gate has rank 1/4; requested joint identification fails."),
                evidence(EIN_FP_AUDIT, "release_test_coverage and validation", "No persistent release test activates Einstein, and full-path conformance is not material validation."),
            ],
            [
                "At least three temperatures spanning both sides of Tref and the relevant vibrational/electronic curvature window, with a rate series at each temperature, same specimens, equilibrium/rest control, replicates, measurement resolution, and held-out conditions.",
                "Independent quasi-equilibrium dV/dq or fixed prefactor, current-interruption/transport diagnostics, composition-resolved x(V,T), phonon/heat-capacity priors, DOS/phase priors, and uncertainty/covariance estimates.",
            ],
            [
                "Primary reaction-specific vibrational and electronic sources, plus a justified functional form and parameter prior for each component; three temperature points alone are necessary but not sufficient.",
            ],
            "Add a joint forward model and durable tests, demonstrate full-rank or explicitly constrained parameterization, pass synthetic recovery with noise/model discrepancy, profile-likelihood/covariance and held-out multi-temperature/rate material validation, and keep unresolved null directions frozen.",
            "Additive code seams and an internal round-trip do not establish joint statistical identifiability. The current LCO electronic T term is frozen, and the roadmap's three-temperature wording is not sufficient evidence by itself.",
        ),
    ]


def build_artifact() -> dict[str, Any]:
    blobs = {path: git_blob(path) for path in INPUT_PATHS}
    parsed_json: dict[str, Any] = {}
    for path, blob in blobs.items():
        text = blob.decode("utf-8")
        if path.endswith(".json"):
            parsed_json[path] = json.loads(text)

    roadmap_lines = blobs[ROADMAP].decode("utf-8").splitlines()
    items = build_items(roadmap_lines)
    primary_counts = Counter(entry["primary_classification"] for entry in items)
    coverage = []
    for path in INPUT_PATHS:
        row: dict[str, Any] = {
            "path": path,
            "line_count": len(blobs[path].decode("utf-8").splitlines()),
            "read_range": f"1-{len(blobs[path].decode('utf-8').splitlines())}",
            "full_read": True,
            "hash_basis": "Git blob bytes at HEAD",
            "git_blob_sha256": hashlib.sha256(blobs[path]).hexdigest(),
        }
        if path in parsed_json:
            parsed = parsed_json[path]
            row["json_parse"] = {
                "valid": True,
                "top_level_keys": list(parsed) if isinstance(parsed, dict) else [],
                "recursive_node_count": recursive_node_count(parsed),
            }
        coverage.append(row)

    artifact: dict[str, Any] = {
        "schema_version": 1,
        "phase": 59,
        "step": "38.5",
        "generated_date": "2026-08-25",
        "baseline_commit": BASELINE_COMMIT,
        "status": "PASS_P059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION",
        "scope": "Atomic disposition of all five future-physics proposals and seven atomic v1.0.16 carryover tasks in the frozen v1.0.18.2 roadmap.",
        "authority_boundary": "This is an internal source/theory/code/test/artifact disposition. It does not select canonical future theory, repair production defects, verify uninspected literature, or establish graphite, LCO, Si, blend, temperature, rate, or particle-size material validity.",
        "rules_and_definitions": {
            "IMPLEMENTED": "A real calculation is reachable through a public production behavior. This does not imply default activation, complete parameter contracts, persistent test coverage, or material validation.",
            "THEORY_ONLY": "A theory/derivation baseline exists, but the corresponding quantitative public production closure does not.",
            "NEW_SCOPE": "The frozen corpus lacks the requested closure, or the atomic item is an unexecuted data/literature/identifiability task even if reusable capability seams exist.",
            "secondary_status_rule": "Partial, dormant, empirical, placeholder, untested, unvalidated, and data-dependent states qualify but never replace the one primary classification.",
            "roadmap_authority_rule": "Roadmap and handover self-reports are source claims only; dispositions are controlled by Phase 059 theory, production-code, test/demo, and independent audit evidence.",
            "path_and_hash_rule": "Repository paths use POSIX separators and input integrity is SHA-256 over Git blob bytes at HEAD, independent of checkout CRLF conversion.",
        },
        "counts": {
            "total_items": len(items),
            "proposal_items": 5,
            "carryover_atomic_items": 7,
            "primary_classifications": {
                "IMPLEMENTED": primary_counts["IMPLEMENTED"],
                "NEW_SCOPE": primary_counts["NEW_SCOPE"],
                "THEORY_ONLY": primary_counts["THEORY_ONLY"],
            },
            "input_files": len(coverage),
            "input_lines": sum(row["line_count"] for row in coverage),
        },
        "input_coverage": coverage,
        "items": items,
        "adjudication_summary": {
            "confirmed": [
                "Einstein vibration is a real but dormant/partial public-path production capability.",
                "Production Omega is a per-transition scalar, not Omega(xi).",
                "Cahn-Hilliard is a theory baseline; gamma remains an empirical production input.",
                "Production polarization is lumped Rn/simple relaxation, not Butler-Volmer plus Nernst-Planck transport.",
                "No quantitative PSD/nanoscale convolution exists in the frozen production/test corpus.",
                "n(T) calculation capability exists, but its real-data diagnostic and persistent release coverage do not.",
                "LCO electronic production behavior is frozen at 298.15 K; generic Omega/dH_a schema exists, but actual LCO defaults omit both and provide no measured authority.",
                "Joint theta_E/n/electronic identification fails under the current evidence contract.",
            ],
            "unresolved": [
                "Reaction-resolved vibrational amplitude/spectrum, U-only semantics, Tref guard, persistent tests, and material validation.",
                "All quantitative/data/literature closures represented by P059-RM-002 through P059-RM-012.",
            ],
            "ground_not_found": [
                "The exact residual bibliography records behind roadmap line 48 are not enumerated in the mandatory Step 38.5 corpus.",
                "No measured/public dataset is loaded by the audited release tests/demos.",
                "No evidence in the mandatory corpus validates theta_E=700 K, Omega/dH_a, g_max/x_MIT, gamma, mobility, interfacial energy, or PSD as target-material constants.",
            ],
        },
        "unresolved_items": [
            {"item_id": entry["item_id"], "reason": entry["acceptance_criterion"]}
            for entry in items
        ],
        "validator_summary": {
            "expected_banner": "PASS_P059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION",
            "tdd_red": "Validator was executed before this artifact existed and failed with the required missing-artifact diagnostic; exact command/output belongs to the human result.",
            "required_final_checks": [
                "validator exit 0",
                "generator twice with identical artifact SHA-256",
                "python -m json.tool parse",
                "git diff --check",
                "git diff -- Claude is empty",
            ],
        },
        "determinism": {
            "serialization": "UTF-8, LF, json.dumps(sort_keys=True, indent=2, ensure_ascii=False)",
            "semantic_hash_basis": "Canonical compact JSON with determinism.semantic_sha256 replaced by an empty string",
            "semantic_sha256": "",
        },
    }
    canonical = json.dumps(
        artifact, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    artifact["determinism"]["semantic_sha256"] = hashlib.sha256(canonical).hexdigest()
    return artifact


def main() -> int:
    artifact = build_artifact()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(artifact, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    payload_hash = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(
        "PASS_P059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_AUDIT "
        f"items={artifact['counts']['total_items']} "
        f"inputs={artifact['counts']['input_files']} "
        f"artifact_sha256={payload_hash}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
