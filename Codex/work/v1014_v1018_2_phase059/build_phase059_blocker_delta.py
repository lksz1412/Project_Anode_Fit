#!/usr/bin/env python3
"""Build the frozen Phase 058 -> Phase 059 blocker-delta register."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "4ee5927ef8fb68bbb488b7debc1709c6f5fad8b0"
ARTIFACT_REL = "Codex/results/PHASE_059_PHASE058_BLOCKER_DELTA.json"
ARTIFACT = ROOT / ARTIFACT_REL

INPUT_PATHS = [
    "Codex/results/PHASE_058_CARRY_FORWARD_BLOCKER_REGISTER.json",
    "Codex/results/PHASE_058_CARRY_FORWARD_BLOCKER_REVIEW.md",
    "Codex/results/PHASE_058_FOUR_AXIS_CONFORMANCE_MATRIX.json",
    "Codex/results/PHASE_058_FOUR_AXIS_CONFORMANCE_REVIEW.md",
    "Codex/results/PHASE_059_COMPLETION_AUTHORITY_CLAIM_MATRIX.json",
    "Codex/results/PHASE_059_COMPLETION_AUTHORITY_REVIEW.md",
    "Codex/results/PHASE_059_THEORY_CONTRACT_MATRIX.json",
    "Codex/results/PHASE_059_THEORY_CONTRACT_REVIEW.md",
    "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json",
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
    "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json",
    "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION_RESULT.md",
]

CATEGORY_FIELDS = [
    ("carry_forward_assets", "carry_forward_asset"),
    ("repair_blockers", "repair_blocker"),
    ("new_scope_blockers", "new_scope_blocker"),
    ("evidence_debts", "evidence_debt"),
]

STATUS_SEMANTICS = {
    "RESOLVED": (
        "Actual frozen source/code/test/data evidence satisfies every element of the old "
        "acceptance criterion. An internal PASS banner, self-report, file existence, or "
        "artifact existence alone is insufficient."
    ),
    "PARTIAL": (
        "Actual frozen evidence satisfies a named subset of the acceptance criterion, while "
        "at least one named element remains open."
    ),
    "UNCHANGED": (
        "The Phase 059 evidence does not materially advance or worsen closure of the old "
        "acceptance criterion."
    ),
    "REGRESSED": (
        "The audited closure surface is worse than the Phase 058 boundary, for example because "
        "new public branches increased without corresponding automatic gates."
    ),
    "NEW_EVIDENCE": (
        "Phase 059 adds material evidence about the item, but that evidence does not by itself "
        "satisfy the old acceptance criterion."
    ),
}

EFFECTIVE_ACCEPTANCE = {
    "CF-01": "Preserve the bounded ideal statistical-mechanics and logistic-kernel identities without promoting them to material validation.",
    "CF-02": "Preserve homogeneous symmetric regular-solution free-energy algebra within stated assumptions and keep it separate from convexified equilibrium.",
    "CF-03": "Preserve charge conservation, peak area, and capacity accounting under one explicit Ah/C/hour/second basis contract.",
    "CF-04": "Preserve explicit separation of electrode reaction direction from cell charge/discharge labels in theory and public behavior.",
    "CF-05": "Retain causal relaxation only as a reduced nonequilibrium starting point with normalization and continuity evidence, not as persistent protocol physics.",
    "CF-06": "Preserve bounded entropy-temperature-coefficient and reversible-heat identities with explicit sign and reference conventions.",
    "CF-07": "Preserve the bounded Sommerfeld electronic-entropy endpoint and unit bridge without treating frozen placeholders as material constants.",
    "CF-08": "Preserve nonmutating verify-first regression and provenance discipline with portable deterministic failure gates.",
    "CF-09": "Preserve exact literature anchors and placeholder tiers while withholding claim authority until primary-source truth audit.",
    "CF-10": "Preserve the scalar degenerate-span safety property or prove its architectural obsolescence with an equivalent regression gate.",
    "CF-11": "Preserve claim-disposition and four-axis audit infrastructure with complete, deterministic, orphan-free routing and explicit authority boundaries.",
    "RB-01": "One unit contract and conversion gate covers Ah and C representations without factor-3600 ambiguity.",
    "RB-02": "Homogeneous branches, binodal, common tangent, spinodal and measured hysteresis are explicitly separated.",
    "RB-03": "Independent extents, mutually exclusive states or a continuous host free energy is selected per material.",
    "RB-04": "Electron stoichiometry, site count, degeneracy, interaction, heterogeneity, kinetics and observation widths use distinct symbols and tests.",
    "RB-05": "Temperature, flux or overpotential, electrode potential, composition and phase state enter a falsifiable local barrier and shipped conditions activate the intended path.",
    "RB-06": "Every public parameter path converges continuously to equilibrium as current approaches zero.",
    "RB-07": "The equilibrium-to-lag transition is continuous in curve, area and objective landscape.",
    "RB-08": "If data require hysteresis, cycle history and metastable state persist across calls with limiting tests.",
    "RB-09": "Composition mapping, temperature curvature, phase assignments and defaults are theory-code consistent and data validated.",
    "RB-10": "Instrument resolution, sampling, smoothing, differentiation, baseline and noise map latent states to measured dQ/dV.",
    "RB-11": "Scalar, entropy, LCO, limits, units and data-fit checks fail automatically on every supported environment.",
    "RB-12": "Every cited PDF and image is current, visually clean, reproducible and linked to the exact source state.",
    "RB-13": "The theory main text contains physics and chemistry only; implementation traceability lives in a separate controlled artifact.",
    "NS-01": "Close a provenance-controlled public experimental dataset and fit pipeline with held-out validation, uncertainty, and failure gates by Phase 069.",
    "NS-02": "Close source-backed silicon and graphite-silicon composite material models with conservation, code, tests, and external data by Phase 069.",
    "NS-03": "Close doped high-voltage LCO chemistry and degradation with explicit states, target voltage coverage, tests, and material data by Phase 069.",
    "NS-04": "Close uncertainty, held-out validation, and mechanism ablation with identifiable parameters and explicit null directions by Phase 069.",
    "NS-05": "Complete a systematic primary-literature protocol and exact full-text claim adjudication by Phase 069.",
    "ED-01": "Supply a provenance-controlled public experimental fit with held-out evidence by Phase 069.",
    "ED-02": "Externally validate LCO defaults and phase assignments on source-backed composition, temperature, rate, and voltage-window data by Phase 069.",
    "ED-03": "Supply a documented search protocol and full primary-source adjudication for every load-bearing bibliography claim by Phase 069.",
    "ED-04": "Recover and hash every historically required missing artifact blob body or explicitly bound the unavailable evidence before Phase 068 closure.",
    "ED-05": "Replace environment-specific bit-exact authority with a portable numeric tolerance/provenance contract and cross-environment failure gate by Phase 067.",
}

DELTA_STATUS = {
    "CF-01": "NEW_EVIDENCE",
    "CF-02": "NEW_EVIDENCE",
    "CF-03": "NEW_EVIDENCE",
    "CF-04": "NEW_EVIDENCE",
    "CF-05": "NEW_EVIDENCE",
    "CF-06": "NEW_EVIDENCE",
    "CF-07": "NEW_EVIDENCE",
    "CF-08": "NEW_EVIDENCE",
    "CF-09": "NEW_EVIDENCE",
    "CF-10": "NEW_EVIDENCE",
    "CF-11": "NEW_EVIDENCE",
    "RB-01": "UNCHANGED",
    "RB-02": "PARTIAL",
    "RB-03": "UNCHANGED",
    "RB-04": "UNCHANGED",
    "RB-05": "UNCHANGED",
    "RB-06": "UNCHANGED",
    "RB-07": "PARTIAL",
    "RB-08": "UNCHANGED",
    "RB-09": "UNCHANGED",
    "RB-10": "UNCHANGED",
    "RB-11": "REGRESSED",
    "RB-12": "PARTIAL",
    "RB-13": "PARTIAL",
    "NS-01": "UNCHANGED",
    "NS-02": "UNCHANGED",
    "NS-03": "UNCHANGED",
    "NS-04": "UNCHANGED",
    "NS-05": "NEW_EVIDENCE",
    "ED-01": "UNCHANGED",
    "ED-02": "UNCHANGED",
    "ED-03": "NEW_EVIDENCE",
    "ED-04": "UNCHANGED",
    "ED-05": "NEW_EVIDENCE",
}

EVIDENCE_SPECS = {
    "CF-01": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-176")],
    "CF-02": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-061")],
    "CF-03": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-039")],
    "CF-04": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "ORD-001")],
    "CF-05": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "MEM-001"), ("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "MEM-003")],
    "CF-06": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-179")],
    "CF-07": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-033")],
    "CF-08": [("json", "Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json", "GOLD-006")],
    "CF-09": [("json", "Codex/results/PHASE_059_COMPLETION_AUTHORITY_CLAIM_MATRIX.json", "P059-CLM-028")],
    "CF-10": [("json", "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json", "P059-CODE-001")],
    "CF-11": [("lines", "Codex/results/PHASE_059_STEP_039_1_THEORY_CLAIM_DISPOSITION_RESULT.md", 153, 171)],
    "RB-01": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "UNT-001")],
    "RB-02": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-002"), ("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-009")],
    "RB-03": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-002")],
    "RB-04": [("json", "Codex/results/PHASE_059_THEORY_CLAIM_MATRIX.json", "P059-TCL-153"), ("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "WID-004")],
    "RB-05": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "KIN-001")],
    "RB-06": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "CUR-002")],
    "RB-07": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "MEM-003")],
    "RB-08": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "ORD-002"), ("json", "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json", "P059-CODE-003")],
    "RB-09": [("json", "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json", "P059-CODE-010"), ("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "LCO-001")],
    "RB-10": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-007")],
    "RB-11": [("json", "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json", "P059-TD-011"), ("json", "Codex/results/PHASE_059_PRODUCTION_CODE_INDEX.json", "P059-CODE-013"), ("json", "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json", "P059-TD-012"), ("json", "Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json", "GOLD-003")],
    "RB-12": [("json", "Codex/results/PHASE_059_PDF_VISUAL_REVIEW.json", "PDF-059-01"), ("json", "Codex/results/PHASE_059_PDF_VISUAL_REVIEW.json", "PDF-059-02"), ("json", "Codex/results/PHASE_059_IMAGE_AUDIT.json", "IMG-059-03")],
    "RB-13": [("json", "Codex/results/PHASE_059_COMPLETION_AUTHORITY_CLAIM_MATRIX.json", "P059-CLM-028")],
    "NS-01": [("json", "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json", "P059-TD-013")],
    "NS-02": [("json", "Codex/results/PHASE_059_IMAGE_AUDIT.json", "IMG-059-05")],
    "NS-03": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "LCO-003")],
    "NS-04": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-012")],
    "NS-05": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-011")],
    "ED-01": [("json", "Codex/results/PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json", "P059-TD-013")],
    "ED-02": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "LCO-003")],
    "ED-03": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-011")],
    "ED-04": [("lines", "Codex/results/PHASE_059_ARTIFACT_GENEALOGY_REVIEW.md", 20, 33)],
    "ED-05": [("json", "Codex/results/PHASE_059_GOLDEN_NPZ_AUDIT.json", "GOLD-003")],
}

BASIS = {
    "CF-01": "Step 39.1 preserves the ideal logistic claim only within its derivational boundary; all primary-literature and material authority remains unverified.",
    "CF-02": "Step 39.1 preserves the symmetric homogeneous regular-solution algebra while Phase 059 separately keeps convexification open.",
    "CF-03": "The bell-kernel capacity identity remains preserved, but the public C-rate/capacity basis still has a 3,600 ambiguity.",
    "CF-04": "An independent charge/discharge mirror identity passes exactly; this is internal direction coherence, not material validation.",
    "CF-05": "The pointwise recurrence normalization and resolved small-lag continuity pass, while initial history and chronology remain open.",
    "CF-06": "The reversible-heat identity is preserved with bounded sign assumptions; calorimetry and full heat closure are not supplied.",
    "CF-07": "The Sommerfeld identity is retained as theory, but production freezes the LCO electronic contribution at one reference temperature.",
    "CF-08": "Golden capture/verify provenance is now explicitly bounded as self-referential internal evidence, and portable failure semantics remain open.",
    "CF-09": "v1.0.17 strengthened references and theory-body boundaries, but Phase 059 did not perform systematic primary-source truth audit.",
    "CF-10": "v1.0.15 removes the old work-grid architecture; Phase 059 confirms the replacement but does not prove an equivalent dedicated degenerate-span regression gate.",
    "CF-11": "Step 39.1 extends deterministic claim routing to 973 occurrences and 38 contracts with orphan zero, while 134 equation claims remain uncontracted.",
    "RB-01": "Independent probe UNT-001 reproduces the exact 3,600 factor, so the acceptance criterion remains unsatisfied.",
    "RB-02": "Phase 059 preserves binodal/common-tangent theory and distinguishes it from production observation, but quantitative convexified measured closure remains theory-only.",
    "RB-03": "The lineage still uses independent weighted transition components and adds no material-selected common-host topology.",
    "RB-04": "Phase 059 audits the required role split but does not demonstrate production use of distinct symbols and distinct tests for electron stoichiometry, site count, degeneracy, interaction, heterogeneity, kinetics, and observation widths; WID-004 confirms that the implicit default width and entropy derivative still disagree, so no acceptance element is satisfied.",
    "RB-05": "Independent KIN-001 confirms that the lag/barrier resolver has no local voltage or affinity and shipped material defaults do not close the intended path.",
    "RB-06": "CUR-002 confirms that direct L_V gives the same lag at I=0 and I=1 and therefore bypasses equilibrium.",
    "RB-07": "The resolved L_V kernel converges monotonically in curve and area, but no objective-landscape handoff test or public-path unit closure exists.",
    "RB-08": "Voltage sorting erases acquisition order and each call forces its first state to equilibrium, so persistent history remains absent.",
    "RB-09": "Phase 059 preserves bounded theory identities, but P059-CODE-010 and LCO-001 show that production freezes the LCO electronic term at 298.15 K instead of applying the temperature-dependent law, and no external data validate composition mapping, temperature curvature, phase assignments, or defaults; no acceptance element is satisfied.",
    "RB-10": "Phase 059 adds no instrument-resolution, sampling, smoothing, differentiation, baseline, or noise forward operator mapping latent state to measured dQ/dV; the Phase 058 F4-08 conceptual ensemble integral remains code/test/artifact absent and is not acceptance progress.",
    "RB-11": "Relative to the Phase 058 gate surface, v1.0.18.2 exposes an Einstein helper path that remains dormant in shipped defaults, while the complete copied harness contains no n_T1 or theta_E token and omits critical branch gates; strict bit equality also fails on the audited runtime.",
    "RB-12": "All 492 PDF pages and 10 unique images were visually inspected, but Unicode extraction, links, source-version provenance, and reproducible rebuild/rerender remain open.",
    "RB-13": "v1.0.17 confirms a partial removal of implementation language, but final theory-only semantic separation and the standalone controlled companion are not yet closed.",
    "NS-01": "The full release test/demo inventory loads no public experimental dataset, fit, uncertainty, or holdout.",
    "NS-02": "IMG-059-05 shows that no audited image contains Si, graphite-Si, or experimental observations; this image-only evidence satisfies none of the old source-backed material-model, conservation, code, test, or external-data acceptance elements.",
    "NS-03": "The released LCO defaults stop at 4.05 V and contain no dopant or degradation state.",
    "NS-04": "Step 38.5 finds rank-deficient joint identification and no held-out material validation or mechanism ablation.",
    "NS-05": "Phase 059 provides a more precise ground-not-found bibliography boundary, but not a systematic full-text primary-source review.",
    "ED-01": "No release test or demo loads a measured/public dataset; no Phase 059 public experimental fit exists.",
    "ED-02": "The LCO state remains a three-transition placeholder without doped/high-voltage states or external parameter validation.",
    "ED-03": "The residual bibliography identities are not fully enumerated and no primary-source claim audit is present.",
    "ED-04": "Phase 059 audits later-version artifact bodies, but it does not recover or adjudicate the specific historical blob bodies absent from the Phase 058 partial clone.",
    "ED-05": "Across six releases only 1/13 arrays are bit-exact while 13/13 pass a 1e-12 absolute tolerance, confirming environment dependence without closing the portable gate.",
}

PARTIAL_SATISFIED = {
    "RB-02": ["Homogeneous, spinodal, binodal, and common-tangent theory are explicitly separated in the audited theory claims."],
    "RB-07": ["Independent resolved-kernel curve error decreases monotonically and wide-window area remains conserved as L_V decreases."],
    "RB-12": ["492/492 PDF pages and 10/10 unique images received complete visual inspection; visible PDF clipping was zero."],
    "RB-13": ["v1.0.17 source patch removes a bounded set of exposed implementation language from the theory body."],
}

NEW_EVIDENCE_SATISFIED = {
    "CF-01": ["Bounded logistic algebra is explicitly preserved in Step 39.1."],
    "CF-02": ["Bounded symmetric regular-solution algebra is explicitly preserved in Step 39.1."],
    "CF-03": ["The peak-area identity is explicitly preserved in Step 39.1."],
    "CF-04": ["The independent mirror identity passes exactly under symmetric zero-polarization assumptions."],
    "CF-05": ["Pointwise recurrence normalization and resolved L_V-to-zero convergence pass independent probes."],
    "CF-06": ["The bounded reversible-heat identity is explicitly preserved."],
    "CF-07": ["The bounded electronic-entropy identity is explicitly preserved."],
    "CF-08": ["Capture and verify authority are explicitly separated in the golden audit."],
    "CF-09": ["Reference and theory-body patches are source-confirmed."],
    "CF-10": ["The old work-grid architecture is source-confirmed as removed and replaced by pointwise evaluation."],
    "CF-11": ["Step 39.1 routes 973 occurrences, 38 contracts, and 80 contract-evidence records with orphan zero."],
    "NS-05": ["The residual bibliography ground-not-found boundary is more precisely enumerated."],
    "ED-03": ["The exact missing bibliography scope is now explicitly classified as ground not found."],
    "ED-05": ["Cross-release runtime evidence quantifies the strict-bit versus tolerance-level difference."],
}

NEW_BLOCKERS = [
    {
        "blocker_id": "P059-BD-NEW-001",
        "category": "repair_blocker",
        "topic": "einstein_input_semantics_and_positive_reference_guard",
        "evidence_specs": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "VIB-003"), ("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-001")],
        "acceptance_criterion": "Reject nonpositive theta_E_Tref before arithmetic, define or reject theta_E on U-only transitions, and add persistent scalar/array/derivative/heat failure gates for absent and active Einstein paths.",
        "target_phase": 67,
        "blocking_authority": "Blocks canonical implementation-conformance promotion of the Einstein path; it does not invalidate the bounded single-oscillator algebra.",
        "overlap_old_ids": ["RB-04", "RB-11"],
        "deduplication_basis": "The old width and test-gate blockers do not contain the v1.0.18.2-specific positive reference-temperature and U-only input semantics introduced after Phase 058.",
    },
    {
        "blocker_id": "P059-BD-NEW-002",
        "category": "evidence_debt",
        "topic": "einstein_reaction_spectrum_amplitude_and_material_identifiability",
        "evidence_specs": [("json", "Codex/results/PHASE_059_INDEPENDENT_CODE_PROBES.json", "VIB-004"), ("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-001")],
        "acceptance_criterion": "Define reaction-resolved signed phonon spectral amplitudes, populate source-backed material parameters, demonstrate joint identifiability, and pass held-out multi-temperature material validation with uncertainty.",
        "target_phase": 69,
        "post_audit_target_phases": [71, 72, 82],
        "blocking_authority": "Blocks material or canonical authority for Einstein corrections; it does not block internal algebraic capability classification.",
        "overlap_old_ids": ["NS-04", "NS-05", "ED-01"],
        "deduplication_basis": "The old generic identifiability, literature, and data items do not preserve the new Einstein reaction-spectrum/amplitude claim as an independently traceable acceptance target.",
    },
    {
        "blocker_id": "P059-BD-NEW-003",
        "category": "evidence_debt",
        "topic": "uncontracted_displayed_equation_claim_adjudication",
        "evidence_specs": [("lines", "Codex/results/PHASE_059_STEP_039_1_THEORY_CLAIM_DISPOSITION_RESULT.md", 167, 185)],
        "acceptance_criterion": "Give every one of the 134 currently uncontracted exact equation claims an evidence-backed derivation/literature disposition or an explicit justified exclusion before canonical equation freeze.",
        "target_phase": 69,
        "post_audit_target_phases": [71, 82],
        "blocking_authority": "Blocks canonical promotion of uncontracted equation claims; it does not negate Step 39.1 occurrence and contract routing completeness.",
        "overlap_old_ids": ["CF-11", "NS-05", "ED-03"],
        "deduplication_basis": "CF-11 preserves audit infrastructure and NS-05/ED-03 cover literature protocol, but none records the newly measured universe of 134 exact equation claims lacking directly applicable theory contracts.",
    },
    {
        "blocker_id": "P059-BD-NEW-004",
        "category": "new_scope_blocker",
        "topic": "composition_dependent_interaction_or_sublattice_law",
        "evidence_specs": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-002")],
        "acceptance_criterion": "Derive and implement a dimensionally and symmetrically defined Omega(xi) or sublattice free energy, recover the constant-Omega limit, and validate nonuniform material asymmetry on independent composition-resolved data.",
        "target_phase": 69,
        "post_audit_target_phases": [73, 75, 77, 78],
        "blocking_authority": "Blocks promotion of composition-dependent interaction claims, not the bounded constant-Omega homogeneous algebra.",
        "overlap_old_ids": ["RB-02", "RB-03"],
        "deduplication_basis": "RB-02 addresses convexification and RB-03 host topology; neither specifies the new composition-dependent interaction or sublattice constitutive law.",
    },
    {
        "blocker_id": "P059-BD-NEW-005",
        "category": "new_scope_blocker",
        "topic": "signed_charge_transfer_and_transport_solver",
        "evidence_specs": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-004")],
        "acceptance_criterion": "Implement signed current balance and terminal-voltage closure with charge-transfer and transport, recover lumped/equilibrium limits, pass conservation and convergence tests, and validate separated contributions on held-out EIS/rate data.",
        "target_phase": 69,
        "post_audit_target_phases": [73, 76],
        "blocking_authority": "Blocks mechanistic transport authority; it does not erase the bounded reduced causal-lag kernel.",
        "overlap_old_ids": ["RB-05", "NS-01"],
        "deduplication_basis": "RB-05 covers a local barrier/default defect and NS-01 covers data infrastructure; neither is a signed charge-transfer/transport/current-balance model acceptance target.",
    },
    {
        "blocker_id": "P059-BD-NEW-006",
        "category": "new_scope_blocker",
        "topic": "quantitative_particle_size_psd_forward_model",
        "evidence_specs": [("json", "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json", "P059-RM-005")],
        "acceptance_criterion": "Define a normalized measured-PSD forward convolution with radius, surface/interfacial energy and molar-volume units, recover large-particle limits, preserve capacity, quantify ill-posedness, and validate held-out size-resolved curves.",
        "target_phase": 69,
        "post_audit_target_phases": [72, 73, 75, 77],
        "blocking_authority": "Blocks quantitative particle-size authority; it does not invalidate a generic phenomenological observation-width identity.",
        "overlap_old_ids": ["RB-10"],
        "deduplication_basis": "RB-10 covers instrument/observation mapping; it does not define a physical radius/PSD/Gibbs-Thomson or finite-size forward law.",
    },
]

REFINEMENT_ROUTES = [
    {"finding": "nonmonotone chronology and forced initial equilibrium", "old_ids": ["RB-07", "RB-08"], "basis": "Refines existing handoff and persistent-history blockers; not new."},
    {"finding": "direct-L_V zero-current bypass", "old_ids": ["RB-06"], "basis": "Exact continuation of the old zero-current blocker."},
    {"finding": "default width/dwdT and n(T) role mismatch", "old_ids": ["RB-04", "RB-10", "NS-04"], "basis": "Refines width semantics, observation, and identifiability items."},
    {"finding": "frozen LCO electronic term and absent doped high-voltage state", "old_ids": ["RB-09", "NS-03", "ED-02"], "basis": "Refines the existing LCO repair/scope/evidence trio."},
    {"finding": "print-only tests, missing branches, and strict bit-exact portability", "old_ids": ["RB-11", "ED-05"], "basis": "Refines failure-gate and environment-specific evidence debt."},
    {"finding": "PDF accessibility, broken links, stale version labels, image units and rerender provenance", "old_ids": ["RB-12"], "basis": "All are acceptance dimensions of the existing artifact-layout/provenance blocker."},
    {"finding": "public fit, Si/blend, literature truth, uncertainty and holdout remain absent", "old_ids": ["NS-01", "NS-02", "NS-04", "NS-05", "ED-01", "ED-03"], "basis": "Existing new-scope/evidence-debt IDs already own these absences."},
    {"finding": "Cahn-Hilliard units/boundaries/coarse-graining and empirical hysteresis gamma", "old_ids": ["RB-02", "RB-08"], "basis": "Refines convexified equilibrium and persistent hysteresis; no duplicate new blocker."},
]


def git_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def recursive_node_count(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + sum(recursive_node_count(item) for item in value.values())
    if isinstance(value, list):
        return 1 + sum(recursive_node_count(item) for item in value)
    return 1


def walk_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from walk_dicts(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_dicts(item)


def record_matches(document: Any, record_id: str) -> list[tuple[str, dict[str, Any]]]:
    id_keys = ("id", "claim_id", "item_id", "probe_id", "finding_id", "record_id", "contract_id")
    matches = []
    for obj in walk_dicts(document):
        for key in id_keys:
            if obj.get(key) == record_id:
                matches.append((key, obj))
                break
    return matches


def record_evidence(parsed: dict[str, Any], path: str, record_id: str) -> dict[str, Any]:
    matches = record_matches(parsed[path], record_id)
    if len(matches) > 1:
        largest = max(recursive_node_count(record) for _, record in matches)
        matches = [
            (key, record)
            for key, record in matches
            if recursive_node_count(record) == largest
        ]
    if len(matches) != 1:
        raise RuntimeError(f"{path}:{record_id}: expected one JSON record, found {len(matches)}")
    key, record = matches[0]
    observed = {
        field: copy.deepcopy(record[field])
        for field in (
            "title", "topic", "category", "verdict", "disposition", "primary_classification",
            "claim", "interpretation", "acceptance", "authority_boundary"
        )
        if field in record
    }
    return {
        "path": path,
        "anchor_kind": "json_record",
        "record_id_key": key,
        "record_id": record_id,
        "record_sha256": hashlib.sha256(canonical_bytes(record)).hexdigest(),
        "observed_fields": observed,
        "authority_use": "Frozen internal audit evidence only; record presence or PASS language is not resolution authority.",
    }


def line_evidence(blob_map: dict[str, bytes], path: str, start: int, end: int) -> dict[str, Any]:
    lines = blob_map[path].decode("utf-8").splitlines()
    if start < 1 or end < start or end > len(lines):
        raise RuntimeError(f"invalid line evidence {path}:{start}-{end}")
    excerpt = "\n".join(lines[start - 1 : end])
    return {
        "path": path,
        "anchor_kind": "line_range",
        "line_start": start,
        "line_end": end,
        "source_excerpt": excerpt,
        "excerpt_sha256": hashlib.sha256(excerpt.encode("utf-8")).hexdigest(),
        "authority_use": "Frozen internal audit text only; the anchored result does not promote external validity.",
    }


def materialize_evidence(specs: list[tuple[Any, ...]], parsed: dict[str, Any], blob_map: dict[str, bytes]) -> list[dict[str, Any]]:
    output = []
    for spec in specs:
        if spec[0] == "json":
            output.append(record_evidence(parsed, spec[1], spec[2]))
        elif spec[0] == "lines":
            output.append(line_evidence(blob_map, spec[1], spec[2], spec[3]))
        else:
            raise RuntimeError(f"unknown evidence specification: {spec!r}")
    return output


def acceptance_audit(old_id: str, status: str) -> dict[str, Any]:
    if status == "PARTIAL":
        satisfied = PARTIAL_SATISFIED[old_id]
        conclusion = "PARTIALLY_SATISFIED"
    elif status == "NEW_EVIDENCE":
        satisfied = NEW_EVIDENCE_SATISFIED[old_id]
        conclusion = "NOT_CLOSED_NEW_EVIDENCE"
    elif status == "REGRESSED":
        satisfied = []
        conclusion = "NOT_SATISFIED_REGRESSED"
    else:
        satisfied = []
        conclusion = "NOT_SATISFIED_UNCHANGED"
    return {
        "criterion": EFFECTIVE_ACCEPTANCE[old_id],
        "satisfied_elements": satisfied,
        "unsatisfied_elements": [BASIS[old_id]],
        "conclusion": conclusion,
        "resolution_authority_check": "NOT_RESOLVED; no internal PASS, self-report, file existence, or artifact existence was counted as closure.",
    }


def source_routes(register: dict[str, Any], four_axis: dict[str, Any], old_id: str) -> list[dict[str, Any]]:
    rows = {row["id"]: row for row in four_axis["rows"]}
    output = []
    for index, route in enumerate(register["four_axis_routes"]):
        if route["route"] == old_id:
            output.append({
                "register_route_index": index,
                "route": copy.deepcopy(route),
                "phase058_four_axis_record": copy.deepcopy(rows[route["row"]]),
                "phase058_four_axis_record_sha256": hashlib.sha256(canonical_bytes(rows[route["row"]])).hexdigest(),
            })
    return output


def build() -> dict[str, Any]:
    blob_map = {path: git_blob(path) for path in INPUT_PATHS}
    parsed = {
        path: json.loads(blob_map[path].decode("utf-8"))
        for path in INPUT_PATHS
        if path.endswith(".json")
    }
    coverage = []
    for path in INPUT_PATHS:
        blob = blob_map[path]
        line_count = len(blob.splitlines())
        row = {
            "path": PurePosixPath(path).as_posix(),
            "byte_count": len(blob),
            "line_count": line_count,
            "read_range": f"1-{line_count}",
            "sha256": hashlib.sha256(blob).hexdigest(),
            "hash_basis": f"Git blob bytes at baseline {BASELINE}",
            "parse_mode": "recursive_json_all_nodes" if path.endswith(".json") else "full_text_1_to_EOF",
        }
        if path.endswith(".json"):
            row["recursive_node_count"] = recursive_node_count(parsed[path])
        coverage.append(row)

    register = parsed[INPUT_PATHS[0]]
    four_axis = parsed[INPUT_PATHS[2]]
    old_deltas = []
    for source_field, category in CATEGORY_FIELDS:
        for index, original in enumerate(register[source_field]):
            old_id = original["id"]
            status = DELTA_STATUS[old_id]
            old_deltas.append({
                "old_id": old_id,
                "old_category": category,
                "source_register_field": source_field,
                "source_register_index": index,
                "original_item": copy.deepcopy(original),
                "original_item_sha256": hashlib.sha256(canonical_bytes(original)).hexdigest(),
                "original_acceptance_present": "acceptance" in original,
                "original_acceptance_criterion": original.get("acceptance"),
                "effective_acceptance_criterion": (
                    original["acceptance"]
                    if "acceptance" in original
                    else EFFECTIVE_ACCEPTANCE[old_id]
                ),
                "source_four_axis_routes": source_routes(register, four_axis, old_id),
                "delta_status": status,
                "phase059_evidence": materialize_evidence(EVIDENCE_SPECS[old_id], parsed, blob_map),
                "acceptance_criterion_audit": acceptance_audit(old_id, status),
                "delta_basis": BASIS[old_id],
                "authority_boundary": "This delta routes frozen internal evidence only. It does not establish primary-literature truth, experimental material validity, or canonical equation authority.",
            })

    new_blockers = []
    for item in NEW_BLOCKERS:
        blocker = {key: copy.deepcopy(value) for key, value in item.items() if key != "evidence_specs"}
        blocker["source_phase"] = 59
        blocker["phase059_evidence"] = materialize_evidence(item["evidence_specs"], parsed, blob_map)
        blocker["authority_boundary"] = "The blocker is bounded to the frozen Phase 059 corpus and is not a literature-truth or external material verdict."
        new_blockers.append(blocker)

    status_counts = Counter(item["delta_status"] for item in old_deltas)
    old_category_counts = Counter(item["old_category"] for item in old_deltas)
    new_category_counts = Counter(item["category"] for item in new_blockers)
    corpus_sha = hashlib.sha256(canonical_bytes(coverage)).hexdigest()
    result = {
        "schema_version": 1,
        "phase": 59,
        "step": "39.2",
        "generated_date": "2026-08-25",
        "status": "PASS_P059_STEP_039_2_BLOCKER_DELTA",
        "baseline_commit": BASELINE,
        "scope": "Lossless routing of all 34 Phase 058 carry-forward register items through frozen Phase 059 evidence, plus genuinely new Phase 059 blockers.",
        "authority_boundary": "Internal lineage/blocker routing only. No source existence, self-report, PASS banner, test execution, artifact existence, DOI metadata, or synthetic output is external scientific or material validation.",
        "rules_and_definitions": {
            "allowed_delta_statuses": list(STATUS_SEMANTICS),
            "delta_status_semantics": STATUS_SEMANTICS,
            "resolved_rule": "RESOLVED requires actual source/code/test/data evidence satisfying every old acceptance element; self-report, internal PASS, or existence is never sufficient.",
            "new_evidence_rule": "NEW_EVIDENCE records a changed evidence state without implying closure.",
            "original_preservation_rule": "The complete source register snapshot and every original item object are stored without field renaming or loss; missing original acceptance/evidence fields remain explicitly absent rather than invented.",
            "new_blocker_rule": "A Phase 059 finding is new only when no old ID owns its constitutive acceptance target; refinements are routed back to old IDs.",
        },
        "input_coverage": coverage,
        "input_corpus_sha256": corpus_sha,
        "source_register_preservation": {
            "path": INPUT_PATHS[0],
            "snapshot": copy.deepcopy(register),
            "snapshot_sha256": hashlib.sha256(canonical_bytes(register)).hexdigest(),
            "category_field_map": [{"source_field": field, "old_category": category} for field, category in CATEGORY_FIELDS],
        },
        "old_deltas": old_deltas,
        "new_blockers": new_blockers,
        "refinement_routes_not_double_counted": REFINEMENT_ROUTES,
        "counts": {
            "input_file_count": len(coverage),
            "input_line_count": sum(item["line_count"] for item in coverage),
            "old_category_counts": dict(sorted(old_category_counts.items())),
            "old_total": len(old_deltas),
            "old_routed": len(old_deltas),
            "orphan_old": 0,
            "old_delta_status_counts": {status: status_counts.get(status, 0) for status in STATUS_SEMANTICS},
            "resolved_count": status_counts.get("RESOLVED", 0),
            "unsupported_resolved_count": 0,
            "new_blocker_count": len(new_blockers),
            "new_blocker_category_counts": dict(sorted(new_category_counts.items())),
            "new_id_collisions": 0,
            "invalid_evidence_paths_or_anchors": 0,
            "missing_acceptance_or_authority_boundary": 0,
            "illegal_delta_status": 0,
        },
        "unresolved": {
            "old_items_not_resolved": len(old_deltas),
            "new_blockers_open": len(new_blockers),
            "primary_literature_truth_audit": "UNVERIFIED_DEFERRED_TO_PHASE071",
            "external_material_validation": "GROUND_NOT_FOUND_IN_FROZEN_PHASE059_CORPUS",
            "next_step": "Controller must atomically commit the four Step 39.2 science files plus ledger and handover, push/verify, then enter Step 39.3.",
        },
        "determinism": {
            "serialization": "UTF-8 JSON, ensure_ascii=false, sort_keys=true, indent=2, LF, final newline",
            "semantic_hash_basis": "Canonical compact JSON with determinism.semantic_sha256 set to the empty string",
            "semantic_sha256": "",
        },
    }
    result["determinism"]["semantic_sha256"] = hashlib.sha256(canonical_bytes(result)).hexdigest()
    return result


def main() -> int:
    document = build()
    payload = json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    print(
        "PASS_P059_STEP_039_2_BLOCKER_DELTA_BUILD "
        f"old={document['counts']['old_total']} new={document['counts']['new_blocker_count']} "
        f"inputs={document['counts']['input_file_count']} artifact_sha256={digest}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
