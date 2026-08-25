#!/usr/bin/env python3
"""Validate the Phase 059 Step 39.4 carry-forward register independently."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from functools import lru_cache
from typing import Any


BASELINE = "8d7be538c586e41a373b769d0949e0c65916b4ef"
ARTIFACT = pathlib.Path("Codex/results/PHASE_059_CARRY_FORWARD_REGISTER.json")
ROADMAP_PATH = "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION.json"
DELTA_PATH = "Codex/results/PHASE_059_PHASE058_BLOCKER_DELTA.json"
FOUR_AXIS_PATH = "Codex/results/PHASE_059_FOUR_AXIS_CONFORMANCE_MATRIX.json"
INPUT_PATHS = (
    "Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md",
    "Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md",
    "Codex/plans/2026-08-25-phase059-resume-closure-detailed-plan.md",
    ROADMAP_PATH,
    "Codex/results/PHASE_059_STEP_038_5_FUTURE_PHYSICS_ROADMAP_DISPOSITION_RESULT.md",
    DELTA_PATH,
    "Codex/results/PHASE_059_STEP_039_2_BLOCKER_DELTA_RESULT.md",
    FOUR_AXIS_PATH,
    "Codex/results/PHASE_059_STEP_039_3_FOUR_AXIS_CONFORMANCE_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)
ALLOWED_CATEGORIES = {
    "PRESERVED_ASSET",
    "REPAIR_BLOCKER",
    "NEW_SCOPE_BLOCKER",
    "EVIDENCE_DEBT",
}
ALLOWED_DOMAINS = {
    "INTERNAL_CONFORMANCE",
    "EXTERNAL_VALIDITY",
    "MIXED_INTERNAL_EXTERNAL",
}
TOP_LEVEL_KEYS = {
    "schema_version", "phase", "step", "generated_date", "status", "baseline_commit",
    "scope", "authority_boundary", "input_coverage", "input_corpus_sha256",
    "rules_and_definitions", "source_reconciliation", "four_axis_boundary", "items",
    "counts", "unresolved", "determinism",
}
ITEM_KEYS = {
    "carry_forward_id", "source_route", "category", "category_mapping_basis",
    "category_mapping_basis_sha256", "status", "open_state", "acceptance_criterion",
    "original_target_fields", "target_phase", "target_horizon", "activation_gate",
    "target_basis", "target_phase_context", "schedule_reconciliation", "blocking_authority",
    "validity_domain", "authority_boundary", "phase059_evidence_state", "source_evidence",
    "source_evidence_sha256", "overlap_or_refinement_links", "four_axis_high_risk_links",
    "non_double_count_basis",
}
OVERLAP_LINK_KEYS = {"related_source_id", "relation_type", "basis"}
HIGH_RISK_LINK_KEYS = {"finding_id", "source_artifact_path", "finding_record_sha256", "relevance_basis"}
FOUR_AXIS_BOUNDARY_KEYS = {
    "source_artifact_path", "status_counts", "direct_related_not_applicable",
    "high_risk_findings", "high_risk_findings_sha256", "external_truth_authority",
    "authority_boundary",
}
DETERMINISM_KEYS = {"serialization", "hash_basis", "semantic_sha256"}
EXPECTED_SCOPE = "Losslessly route 12 Step 38.5 roadmap identities and 34+6 Step 39.2 identities into mutually exclusive future carry-forward categories."
EXPECTED_TOP_AUTHORITY = "This register is internal routing authority only. It does not establish primary-literature truth, external material validity, parameter identifiability, public-data validation, or completed repairs."
EXPECTED_RULES = {
    "categories": {
        "PRESERVED_ASSET": "Non-blocking bounded asset retained with an explicit preservation criterion; never presented as validated or resolved.",
        "REPAIR_BLOCKER": "Existing internal behavior or contract requires correction and acceptance evidence.",
        "NEW_SCOPE_BLOCKER": "Proposed constitutive/material/model scope is absent and cannot be promoted without its acceptance package.",
        "EVIDENCE_DEBT": "Claim authority is blocked by missing literature, data, provenance, identifiability, or validation evidence.",
    },
    "category_exclusivity": "Each of 52 source identities receives exactly one category; category arrays or overlaps are prohibited.",
    "source_routing": "Direct one-source-to-one-row routing is used; no scientifically distinct acceptance criterion is consolidated.",
    "resolution_rule": "No OPEN item is RESOLVED or VALIDATED. Internal PASS, file existence, artifact existence, or self-report is not acceptance closure.",
    "target_rule": "Targets 60-69 are pre-freeze closure/audit gates. Targets 70-90 are inactive unless Phase 069 returns GO or CONDITIONAL_GO.",
    "authority_rule": "Four-axis internal conformance and relation partitions do not establish external material or literature truth.",
}
EXPECTED_UNRESOLVED = {
    "pre_freeze": "All non-asset targets in Phases 060-069 remain open until exact acceptance evidence closes them.",
    "post_gate": "All Phase 070-090 targets are inactive unless Phase 069 returns GO or CONDITIONAL_GO.",
    "external_validity": "No primary-literature truth, public material fit, held-out external validation, or parameter-identifiability closure is established.",
    "next_step": "Controller review, ledger/handover update, six-file atomic commit/push/remote verification, then Step 39.5.",
}
EXPECTED_DETERMINISM_STATIC = {
    "serialization": "UTF-8, LF, ensure_ascii=False, sort_keys=True, indent=2",
    "hash_basis": "Canonical JSON with determinism.semantic_sha256 set to the empty string",
}


ROADMAP_CATEGORY = {
    "P059-RM-001": "REPAIR_BLOCKER",
    "P059-RM-002": "NEW_SCOPE_BLOCKER",
    "P059-RM-003": "NEW_SCOPE_BLOCKER",
    "P059-RM-004": "NEW_SCOPE_BLOCKER",
    "P059-RM-005": "NEW_SCOPE_BLOCKER",
    "P059-RM-006": "EVIDENCE_DEBT",
    "P059-RM-007": "NEW_SCOPE_BLOCKER",
    "P059-RM-008": "EVIDENCE_DEBT",
    "P059-RM-009": "NEW_SCOPE_BLOCKER",
    "P059-RM-010": "NEW_SCOPE_BLOCKER",
    "P059-RM-011": "EVIDENCE_DEBT",
    "P059-RM-012": "NEW_SCOPE_BLOCKER",
}
ROADMAP_CATEGORY_BASIS = {
    "P059-RM-001": "A callable Einstein correction already exists, so the open U-only semantics, positive theta_E_Tref guard, persistent activation tests, and branch behavior are corrections to existing behavior; reaction-spectrum and material evidence remain separately linked debts.",
    "P059-RM-002": "Production has only transition-constant Omega; composition-dependent Omega(xi) or a sublattice free energy, its symmetry and limiting law, and composition-resolved validation are a genuinely new constitutive scope.",
    "P059-RM-003": "The frozen analytical Cahn-Hilliard baseline is theory-only; mobility, boundary conditions, elasticity, nucleation, conservation, and coarse-graining to hysteresis require a new production-physics scope rather than a repair to an existing solver.",
    "P059-RM-004": "Existing Rn and first-order lag are reduced empirical behavior, not a signed Butler-Volmer/Nernst-Planck current-balance solver; the requested transport and charge-transfer closure is genuinely new constitutive scope.",
    "P059-RM-005": "A qualitative broadening identity exists, but normalized measured-PSD/radius convolution, Gibbs-Thomson units, capacity limits, and size-resolved validation are absent new particle-size physics.",
    "P059-RM-006": "The n(T) calculation seam exists; what is missing is execution on controlled multi-temperature observations with uncertainty, positivity, held-out temperatures, and persistent evidence, so the obligation is evidence debt rather than new algebra.",
    "P059-RM-007": "A phenomenological width exists, but a distinct typed two-phase width component that separates heterogeneity, kinetics, phase-field, and instrument resolution is absent and therefore a new constitutive/observation scope.",
    "P059-RM-008": "Generic Omega and dH_a keys exist, while source-backed LCO values, estimation protocol, uncertainty, and cross-temperature/rate held-out recovery are missing; the blocker is material evidence debt, not permission to invent constants.",
    "P059-RM-009": "Production freezes one electronic offset at 298.15 K; a composition- and temperature-resolved electronic free-energy law with derivatives, limits, and LCO validation is a new material constitutive scope.",
    "P059-RM-010": "A placeholder composition gate exists, but an implicit source-constrained x(V,T) model, chain rule, rank, and uncertainty closure do not; that missing feedback law is new inference/material scope.",
    "P059-RM-011": "The residual bibliography identities and load-bearing full-text anchors are not present in the frozen corpus; the open obligation is evidence debt and no DOI or claim support may be inferred.",
    "P059-RM-012": "Additive seams do not constitute a joint forward/inference model; full-rank or constrained recovery, null-direction accounting, uncertainty, ablation, and held-out validation are a genuinely new inference scope.",
}
TARGET_PHASE = {
    "P059-RM-001": 67,
    "P059-RM-002": 75,
    "P059-RM-003": 75,
    "P059-RM-004": 76,
    "P059-RM-005": 75,
    "P059-RM-006": 86,
    "P059-RM-007": 75,
    "P059-RM-008": 86,
    "P059-RM-009": 78,
    "P059-RM-010": 78,
    "P059-RM-011": 71,
    "P059-RM-012": 81,
    "CF-01": 65, "CF-02": 65, "CF-03": 67, "CF-04": 67,
    "CF-05": 67, "CF-06": 65, "CF-07": 65, "CF-08": 67,
    "CF-09": 66, "CF-10": 67, "CF-11": 69,
    "RB-01": 67, "RB-02": 65, "RB-03": 65, "RB-04": 67,
    "RB-05": 67, "RB-06": 67, "RB-07": 67, "RB-08": 67,
    "RB-09": 67, "RB-10": 67, "RB-11": 67, "RB-12": 68,
    "RB-13": 68,
    "NS-01": 86, "NS-02": 80, "NS-03": 78, "NS-04": 81,
    "NS-05": 71,
    "ED-01": 86, "ED-02": 86, "ED-03": 71, "ED-04": 68,
    "ED-05": 67,
    "P059-BD-NEW-001": 67, "P059-BD-NEW-002": 86,
    "P059-BD-NEW-003": 82, "P059-BD-NEW-004": 75,
    "P059-BD-NEW-005": 76, "P059-BD-NEW-006": 75,
}
TARGET_PHASE_BASIS = {
    65: "Phase 065 owns the v1.0.24-v1.0.24.1 lineage re-audit: full-read every unique theory/plan/result/handover, code and profile/default change, trace skew peak and material decomposition, test fresh-import, explicit-profile and legacy-restoration gates, then close preserve/correct/reject dispositions.",
    66: "Phase 066 owns the v1.0.25-v1.0.25.2 lineage re-audit: reproduce skew derivative and direct14 fitting, compare the stored 8-digit vector with optimizer state, separate empirical success from physical/material authority, and verify profile/default and temperature dependence including fresh-import/default behavior.",
    67: "Phase 067 is the code/test/fitting cross-audit that must close or explicitly retain this internal implementation, limit, unit, runtime, or harness obligation.",
    68: "Phase 068 is the fork/artifact adjudication gate for historical evidence, render provenance, and theory/code artifact separation.",
    69: "Phase 069 is the canonical audit synthesis and GO/CONDITIONAL_GO/NO_GO decision gate for this bounded audit-infrastructure obligation.",
    71: "Phase 071 is the primary-literature review phase; exact source identity and claim support remain unverified until that phase.",
    72: "Phase 072 is the data-acquisition phase for the specified material, protocol, temperature, composition, rate, and uncertainty evidence.",
    75: "Phase 075 is the equilibrium/phase-separation phase for the proposed interaction, phase-field, width, or particle-size constitutive law and its limits.",
    76: "Phase 076 is the kinetics/hysteresis phase for causal state, charge-transfer, transport, and history-dependent closure.",
    78: "Phase 078 is the LCO material-model phase for electronic, composition-gate, doped/high-voltage, and phase-state closure.",
    80: "Phase 080 is the blend-coupling phase; Phase 079 Si prerequisites must exist before graphite-Si composite closure is adjudicated.",
    81: "Phase 081 is the inference/uncertainty phase for rank, null directions, recovery, ablation, and held-out design.",
    82: "Phase 082 is the equation-freeze phase; every uncontracted equation claim must be supported or explicitly excluded before freeze.",
    86: "Phase 086 is the external-data validation phase for public fit, held-out material evidence, portability, and parameter-validity claims.",
}
TARGET_CONTEXT = {
    "P059-RM-003": {"prerequisite_phases": [71, 72, 73, 74], "related_downstream_phases": [76]},
    "P059-RM-006": {"prerequisite_phases": [67, 72], "related_downstream_phases": []},
    "P059-RM-008": {"prerequisite_phases": [71, 72, 78], "related_downstream_phases": []},
    "NS-02": {"prerequisite_phases": [79], "related_downstream_phases": []},
}
SCHEDULE_RECONCILIATION_IDS = {
    "NS-01", "NS-02", "NS-03", "NS-04", "NS-05",
    "ED-01", "ED-02", "ED-03",
    "P059-BD-NEW-002", "P059-BD-NEW-003", "P059-BD-NEW-004",
    "P059-BD-NEW-005", "P059-BD-NEW-006",
}
MIXED_DOMAIN = {
    "P059-RM-001", "P059-RM-002", "P059-RM-003", "P059-RM-004",
    "P059-RM-005", "P059-RM-006", "P059-RM-007", "P059-RM-009", "P059-RM-010",
    "P059-RM-012", "RB-02", "RB-03", "RB-05", "RB-09", "RB-10",
    "NS-02", "NS-03", "NS-04", "P059-BD-NEW-004",
    "P059-BD-NEW-005", "P059-BD-NEW-006",
}
EXTERNAL_DOMAIN = {
    "P059-RM-008", "P059-RM-011", "NS-01", "NS-05",
    "ED-01", "ED-02", "ED-03", "P059-BD-NEW-002", "P059-BD-NEW-003",
}


EXPECTED_OVERLAP_EDGES = {
    frozenset(pair)
    for pair in (
        ("P059-RM-001", "P059-BD-NEW-001"), ("P059-RM-001", "P059-BD-NEW-002"),
        ("P059-RM-001", "RB-11"), ("P059-RM-002", "P059-BD-NEW-004"),
        ("P059-RM-003", "RB-02"), ("P059-RM-003", "RB-03"),
        ("P059-RM-004", "P059-BD-NEW-005"), ("P059-RM-004", "RB-05"),
        ("P059-RM-005", "P059-BD-NEW-006"), ("P059-RM-005", "RB-10"),
        ("P059-RM-006", "RB-04"), ("P059-RM-006", "NS-04"),
        ("P059-RM-007", "RB-04"), ("P059-RM-007", "RB-10"),
        ("P059-RM-008", "ED-02"), ("P059-RM-008", "NS-03"),
        ("P059-RM-009", "RB-09"), ("P059-RM-009", "ED-02"),
        ("P059-RM-010", "RB-09"), ("P059-RM-010", "ED-02"),
        ("P059-RM-010", "NS-04"), ("P059-RM-011", "NS-05"),
        ("P059-RM-011", "ED-03"), ("P059-RM-012", "NS-04"),
        ("P059-RM-012", "P059-BD-NEW-002"), ("P059-RM-012", "ED-01"),
        ("P059-BD-NEW-001", "RB-04"), ("P059-BD-NEW-001", "RB-11"),
        ("P059-BD-NEW-002", "NS-04"), ("P059-BD-NEW-002", "NS-05"),
        ("P059-BD-NEW-002", "ED-01"), ("P059-BD-NEW-003", "CF-11"),
        ("P059-BD-NEW-003", "NS-05"), ("P059-BD-NEW-003", "ED-03"),
        ("P059-BD-NEW-004", "RB-02"), ("P059-BD-NEW-004", "RB-03"),
        ("P059-BD-NEW-005", "RB-05"), ("P059-BD-NEW-005", "NS-01"),
        ("P059-BD-NEW-006", "RB-10"),
        ("P059-RM-002", "RB-02"), ("P059-RM-002", "RB-03"),
        ("P059-RM-004", "RB-06"), ("P059-BD-NEW-005", "RB-06"),
        ("P059-RM-008", "RB-09"), ("P059-RM-011", "CF-09"),
    )
}
EXPECTED_OVERLAP_BASIS = {
    frozenset(("P059-RM-001", "P059-BD-NEW-001")): "The roadmap Einstein capability and NEW-001 share the active input path, but NEW-001 owns the narrower U-only and positive-reference guard contract while RM-001 retains the full capability acceptance.",
    frozenset(("P059-RM-001", "P059-BD-NEW-002")): "Both routes concern Einstein corrections; RM-001 owns callable-path semantics and tests, whereas NEW-002 owns reaction-resolved spectra, material parameters, identifiability, and held-out evidence.",
    frozenset(("P059-RM-001", "RB-11")): "The optional Einstein branch enlarges the branch-complete gate surface audited by RB-11, but capability existence and portable automatic failure coverage are distinct acceptance criteria.",
    frozenset(("P059-RM-002", "P059-BD-NEW-004")): "Both source records require composition-dependent interaction or sublattice physics; the roadmap proposal identity and the later constitutive blocker remain separately traceable.",
    frozenset(("P059-RM-003", "RB-02")): "Cahn-Hilliard phase-field closure depends on correctly separating homogeneous, spinodal, binodal, common-tangent, and measured branches, while RB-02 does not by itself supply mobility or coarse-graining.",
    frozenset(("P059-RM-003", "RB-03")): "A phase-field host state constrains transition topology, but choosing independent extents versus a common host does not itself derive gradient dynamics, nucleation, or observed hysteresis.",
    frozenset(("P059-RM-004", "P059-BD-NEW-005")): "Both records route the absent signed charge-transfer/transport solver; separate source identities preserve the roadmap proposal and the Phase 059 acceptance package without double closure.",
    frozenset(("P059-RM-004", "RB-05")): "The full transport solver needs a falsifiable local affinity/barrier law, while RB-05 can be repaired without claiming that Butler-Volmer and Nernst-Planck transport are implemented.",
    frozenset(("P059-RM-005", "P059-BD-NEW-006")): "Both records require a normalized radius/PSD forward law; the roadmap particle-size proposal and the later exact units/limits/capacity blocker remain distinct source obligations.",
    frozenset(("P059-RM-005", "RB-10")): "Physical PSD and Gibbs-Thomson broadening feed the measured line shape, whereas RB-10 separately owns instrument resolution, sampling, smoothing, differentiation, baseline, and noise.",
    frozenset(("P059-RM-006", "RB-04")): "Per-temperature n inference depends on unambiguous width, site-count, degeneracy, and entropy symbols/tests, but collecting n(T) evidence does not repair production semantic conflation.",
    frozenset(("P059-RM-006", "NS-04")): "The n(T) diagnostic needs uncertainty and held-out rank evidence, while NS-04 owns the broader joint-identifiability and mechanism-ablation obligation.",
    frozenset(("P059-RM-007", "RB-04")): "A typed two-phase width law requires the semantic role split audited by RB-04, but RB-04 does not create the missing two-phase constitutive component or data validation.",
    frozenset(("P059-RM-007", "RB-10")): "Two-phase physical broadening and the observation operator both affect measured width, but latent mechanism and instrument/differentiation mapping remain separate acceptance layers.",
    frozenset(("P059-RM-008", "ED-02")): "Source-backed LCO Omega/dH_a estimation is part of external LCO default validation, while ED-02 also covers phase assignments, composition, rate, temperature, and voltage window.",
    frozenset(("P059-RM-008", "NS-03")): "LCO interaction/barrier parameters may depend on dopant and high-voltage chemistry, but parameter estimation does not supply the missing chemical/degradation states owned by NS-03.",
    frozenset(("P059-RM-009", "RB-09")): "The roadmap temperature-dependent electronic law is directly affected by RB-09's frozen 298.15 K production behavior, while full held-out material validation remains broader than that repair.",
    frozenset(("P059-RM-009", "ED-02")): "Temperature-resolved electronic curvature is one component of externally validating LCO defaults and phase assignments; neither route closes the other by existence.",
    frozenset(("P059-RM-010", "RB-09")): "The implicit x(V,T) gate is required for theory-code-consistent LCO composition mapping, whereas RB-09 additionally covers electronic curvature, phase assignments, and defaults.",
    frozenset(("P059-RM-010", "ED-02")): "Composition-gate constants and feedback require external LCO evidence, but ED-02 retains the wider material/default/phase validation criterion.",
    frozenset(("P059-RM-010", "NS-04")): "The gate parameters are rank-deficient within joint inference, while NS-04 owns uncertainty, holdout, ablation, and all explicit null directions across mechanisms.",
    frozenset(("P059-RM-011", "NS-05")): "The residual bibliography identities are inputs to systematic primary-literature review, but enumerating them and completing full-text claim adjudication are distinct acceptance stages.",
    frozenset(("P059-RM-011", "ED-03")): "Roadmap residual-reference identity overlaps the missing search protocol and load-bearing full-text evidence, without allowing metadata existence to close claim support.",
    frozenset(("P059-RM-012", "NS-04")): "Both routes require joint identifiability, uncertainty, null-direction, ablation, and held-out evidence; the roadmap multi-temperature seam remains a separate source identity.",
    frozenset(("P059-RM-012", "P059-BD-NEW-002")): "Joint theta_E/n/electronic inference includes the Einstein material-spectrum debt, while NEW-002 is reaction-vibration-specific and RM-012 spans the full joint model.",
    frozenset(("P059-RM-012", "ED-01")): "Held-out joint recovery requires a public experimental fit surface, but ED-01's provenance-controlled public fit does not establish parameter rank or mechanism separation.",
    frozenset(("P059-BD-NEW-001", "RB-04")): "Einstein input semantics add a typed thermal path and persistent tests to the broader symbol/width/entropy separation audit, but do not resolve every RB-04 semantic role.",
    frozenset(("P059-BD-NEW-001", "RB-11")): "NEW-001's guard and active/absent branch tests are a concrete subset of RB-11's portable branch-complete automatic failure gates.",
    frozenset(("P059-BD-NEW-002", "NS-04")): "Reaction-spectrum parameters participate in joint identifiability and uncertainty, while NS-04 also covers non-vibrational mechanisms and ablation.",
    frozenset(("P059-BD-NEW-002", "NS-05")): "Material-specific phonon and reaction-spectrum authority requires primary-source review, but literature truth alone does not provide calibration or held-out validation.",
    frozenset(("P059-BD-NEW-002", "ED-01")): "Einstein material validation needs public multi-temperature observations, while ED-01 retains the general provenance-controlled fit and holdout pipeline.",
    frozenset(("P059-BD-NEW-003", "CF-11")): "The 134 uncontracted claims are a measured gap in the claim-routing infrastructure preserved by CF-11, but infrastructure completeness does not adjudicate those claims.",
    frozenset(("P059-BD-NEW-003", "NS-05")): "Uncontracted equations may require primary literature, while NS-05 owns the systematic protocol across all load-bearing claims rather than only 134 equations.",
    frozenset(("P059-BD-NEW-003", "ED-03")): "Exact equation disposition depends on search/full-text claim evidence, but ED-03 is not limited to the equation subset and cannot be closed by routing counts.",
    frozenset(("P059-BD-NEW-004", "RB-02")): "Composition-dependent interaction changes nonconvex equilibrium and phase boundaries, while RB-02 separately enforces branch/binodal/common-tangent/measured-hysteresis separation.",
    frozenset(("P059-BD-NEW-004", "RB-03")): "A sublattice or Omega(xi) law may encode common-host topology, but topology selection alone does not derive or validate the new interaction law.",
    frozenset(("P059-BD-NEW-005", "RB-05")): "The signed transport solver consumes local affinity/barrier physics; repairing the local barrier does not create current balance, transport conservation, or EIS validation.",
    frozenset(("P059-BD-NEW-005", "NS-01")): "Transport separation requires provenance-controlled EIS/rate data and holdout infrastructure, while NS-01 covers the broader public experimental fit pipeline.",
    frozenset(("P059-BD-NEW-006", "RB-10")): "The physical radius/PSD forward model feeds latent-to-measured broadening, whereas RB-10 owns the downstream instrument and differentiation observation operator.",
    frozenset(("P059-RM-002", "RB-02")): "Composition-dependent Omega or sublattice free energy changes convexification, binodal, spinodal, and common-tangent structure, so RM-002 depends on RB-02's phase-equilibrium distinctions without being reduced to them.",
    frozenset(("P059-RM-002", "RB-03")): "The proposed sublattice asymmetry is a candidate common-host topology, while RB-03 requires a material-specific topology choice and RM-002 additionally requires a constitutive law and data.",
    frozenset(("P059-RM-004", "RB-06")): "A signed charge-transfer/transport solver must analytically recover equilibrium as current approaches zero; RB-06 owns that public zero-current limit across existing parameter paths.",
    frozenset(("P059-BD-NEW-005", "RB-06")): "NEW-005's current-balance solver acceptance explicitly includes the equilibrium/lumped limit, making RB-06's continuous I-to-zero contract a required but non-sufficient subset.",
    frozenset(("P059-RM-008", "RB-09")): "Estimating LCO Omega/dH_a requires theory-code-consistent composition, temperature, phase, and default semantics from RB-09 before material constants can carry authority.",
    frozenset(("P059-RM-011", "CF-09")): "RM-011's residual bibliography audit extends CF-09's preserved exact anchors and placeholder tiers; preservation of citation structure does not verify remaining metadata or load-bearing claims.",
}
EXPECTED_HIGH_RISK_ROUTES = {
    "P059-F4-HR-001": {"P059-RM-004", "RB-05", "P059-BD-NEW-005"},
    "P059-F4-HR-002": {"CF-05", "RB-08"},
    "P059-F4-HR-003": {"RB-06", "P059-RM-004", "P059-BD-NEW-005"},
    "P059-F4-HR-004": {"CF-03", "RB-01"},
    "P059-F4-HR-005": {"RB-04", "P059-RM-006", "P059-RM-007"},
    "P059-F4-HR-006": {"RB-09", "NS-03", "ED-02", "P059-RM-008", "P059-RM-009", "P059-RM-010"},
    "P059-F4-HR-007": {"RB-11", "P059-BD-NEW-001", "P059-BD-NEW-002", "P059-RM-001"},
    "P059-F4-HR-008": {"NS-02"},
    "P059-F4-HR-009": {"NS-01", "ED-01", "NS-04", "P059-RM-012"},
    "P059-F4-HR-010": {"CF-08", "RB-11", "ED-05"},
    "P059-F4-HR-011": {"RB-12", "ED-04"},
}
EXPECTED_HIGH_RISK_BASIS = {
    ("P059-F4-HR-001", "P059-RM-004"): "The roadmap transport solver must retain local temperature/current semantics; the finding shows production collapses local T(V) before lag/affinity evaluation and provides no joint low-T/current validation.",
    ("P059-F4-HR-001", "RB-05"): "RB-05 requires a falsifiable local barrier driven by temperature, flux/overpotential, potential, composition, and phase; the finding identifies the exact local-state collapse that keeps it open.",
    ("P059-F4-HR-001", "P059-BD-NEW-005"): "The new signed current-balance/transport solver must evaluate local affinity and transport at local T/current; the low-temperature finite-current finding is therefore a direct design boundary, not material validation.",
    ("P059-F4-HR-002", "CF-05"): "CF-05 preserves causal relaxation only as a reduced starting point; voltage sorting and forced equilibrium initialization define the chronology/history boundary that preservation must not overstate.",
    ("P059-F4-HR-002", "RB-08"): "RB-08 explicitly requires persistent cycle history and metastable state; sorting and forced first-state equilibrium are the internal defects that prevent its acceptance.",
    ("P059-F4-HR-003", "RB-06"): "RB-06 owns continuous equilibrium recovery as current approaches zero; direct L_V precedence produces identical I=0/I=1 behavior and directly violates that contract.",
    ("P059-F4-HR-003", "P059-RM-004"): "The proposed signed transport/current-balance solver must recover the equilibrium limit; the direct-L_V bypass is an existing limit defect that the new solver cannot inherit.",
    ("P059-F4-HR-003", "P059-BD-NEW-005"): "NEW-005 requires analytic lumped/equilibrium limits; the reproduced direct-L_V zero-current violation is a required regression boundary for its future solver.",
    ("P059-F4-HR-004", "CF-03"): "CF-03 preserves peak area and capacity only under one explicit unit basis; the factor-3,600 current/lag discrepancy bounds that preservation.",
    ("P059-F4-HR-004", "RB-01"): "RB-01 is the exact Ah/C/hour/second conversion blocker reproduced by the factor-3,600 probe and absent release gate.",
    ("P059-F4-HR-005", "RB-04"): "RB-04 requires distinct width and entropy roles/tests; production's default thermal width with zero entropy derivative is the exact semantic inconsistency.",
    ("P059-F4-HR-005", "P059-RM-006"): "Per-temperature n inference cannot carry authority while the same default transition has incompatible observable and entropy temperature laws and no persistent n_T1 gate.",
    ("P059-F4-HR-005", "P059-RM-007"): "A two-phase width law must be separated from the inconsistent default width/dwdT path before mechanism or temperature evidence can be interpreted.",
    ("P059-F4-HR-006", "RB-09"): "RB-09 owns LCO composition/temperature/default consistency; the 298.15 K freeze, missing implicit coupling, and limited defaults are its exact internal boundary.",
    ("P059-F4-HR-006", "NS-03"): "NS-03 requires doped high-voltage LCO states and degradation coverage; the audited defaults end near 4.05 V without dopant/state descriptors.",
    ("P059-F4-HR-006", "ED-02"): "ED-02 requires external validation of LCO defaults and phases; print-only synthetic evidence and absent high-voltage coverage cannot supply that authority.",
    ("P059-F4-HR-006", "P059-RM-008"): "LCO Omega/dH_a estimation cannot proceed from generic keys while defaults lack values, high-voltage/dopant state, and measured multi-T/rate evidence.",
    ("P059-F4-HR-006", "P059-RM-009"): "The roadmap T-dependent electronic law is contradicted by the production 298.15 K freeze and missing temperature-resolved material evidence.",
    ("P059-F4-HR-006", "P059-RM-010"): "The roadmap composition gate needs implicit x(V,T) feedback; the finding records a frozen center/placeholder path with no source-backed composition-temperature closure.",
    ("P059-F4-HR-007", "RB-11"): "RB-11's portable branch gates must cover the dormant Einstein branch, nonpositive reference temperature, active/absent defaults, derivatives, and heat path.",
    ("P059-F4-HR-007", "P059-BD-NEW-001"): "NEW-001 directly owns positive theta_E_Tref, U-only semantics, and persistent active/absent Einstein failure gates exposed by this finding.",
    ("P059-F4-HR-007", "P059-BD-NEW-002"): "NEW-002 owns the reaction-specific spectrum/amplitude and material validation absent from the internally consistent but dormant Einstein capability.",
    ("P059-F4-HR-007", "P059-RM-001"): "RM-001 is callable but dormant and unvalidated; the finding precisely bounds IMPLEMENTED to internal capability rather than material authority.",
    ("P059-F4-HR-008", "NS-02"): "NS-02 is limited to the audited absence of Si/blend claims in the 185-claim universe, public data loading in tests/demos, and Si/blend images; no wider code/data absence is inferred.",
    ("P059-F4-HR-009", "NS-01"): "NS-01 requires a provenance-controlled public fit pipeline; audited release inputs are synthetic and therefore do not satisfy its dataset/holdout acceptance.",
    ("P059-F4-HR-009", "ED-01"): "ED-01 is the direct public-fit evidence debt: no measured dataset load, fit, or held-out artifact exists in the frozen suite.",
    ("P059-F4-HR-009", "NS-04"): "Uncertainty, ablation, and joint identifiability cannot be validated without measured/public fit and held-out observations, which the finding shows are absent.",
    ("P059-F4-HR-009", "P059-RM-012"): "The joint inference roadmap item needs real multi-temperature/rate holdout evidence; synthetic golden arrays cannot establish rank or material recovery.",
    ("P059-F4-HR-010", "CF-08"): "CF-08 preserves verify-not-capture discipline; self-capture, nonportable paths, extra-key tolerance, and runtime-sensitive strict equality define the unresolved boundary.",
    ("P059-F4-HR-010", "RB-11"): "RB-11's cross-environment failure gates cannot rely on a self-referential golden whose strict equality is runtime-sensitive and key set is not exact.",
    ("P059-F4-HR-010", "ED-05"): "ED-05 owns the portable tolerance/provenance contract quantified by 1/13 bit-exact versus 13/13 at atol=1e-12.",
    ("P059-F4-HR-011", "RB-12"): "RB-12 requires every PDF/image to be current and source-linked; stale v1.0.15 labeling and copied image filenames are exact provenance defects.",
    ("P059-F4-HR-011", "ED-04"): "ED-04 concerns historical artifact evidence; the genealogy finding provides bounded later lineage evidence but does not recover missing historical blob bodies.",
}


class ValidationFailure(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ValidationFailure(message)


def require_dict_exact_keys(value: Any, expected_keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{label} must be an object")
    actual_keys = set(value)
    if actual_keys != expected_keys:
        fail(f"{label} key-set mismatch: missing={sorted(expected_keys - actual_keys)} extra={sorted(actual_keys - expected_keys)}")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{label} must be an array")
    return value


def strict_json_loads(text: str, label: str) -> Any:
    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(text, object_pairs_hook=reject_duplicate_keys)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {label}: {exc}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def require_exact_json(actual: Any, expected: Any, label: str) -> None:
    """Compare JSON values without Python's bool/int/float equality coercions."""
    if type(expected) is int and type(actual) is not int:
        fail(f"{label} must be a JSON integer, got {type(actual).__name__}")
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            fail(f"{label} must be an object")
        for key, expected_value in expected.items():
            if key not in actual:
                fail(f"{label} missing exact field: {key}")
            require_exact_json(actual[key], expected_value, f"{label}.{key}")
    elif isinstance(expected, list):
        if not isinstance(actual, list):
            fail(f"{label} must be an array")
        if len(actual) != len(expected):
            fail(f"{label} length mismatch")
        for index, (actual_value, expected_value) in enumerate(zip(actual, expected, strict=True)):
            require_exact_json(actual_value, expected_value, f"{label}[{index}]")
    if canonical_bytes(actual) != canonical_bytes(expected):
        fail(f"{label} exact JSON semantic mismatch")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def recursive_nodes(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + sum(recursive_nodes(v) for v in value.values())
    if isinstance(value, list):
        return 1 + sum(recursive_nodes(v) for v in value)
    return 1


@lru_cache(maxsize=None)
def git_blob(path: str) -> bytes:
    try:
        return subprocess.check_output(["git", "show", f"{BASELINE}:{path}"], stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        fail(f"missing frozen Git blob {path}: {exc.stderr.decode(errors='replace').strip()}")


@lru_cache(maxsize=None)
def load_json_blob(path: str) -> Any:
    try:
        return strict_json_loads(git_blob(path).decode("utf-8"), path)
    except UnicodeDecodeError as exc:
        fail(f"invalid frozen JSON {path}: {exc}")


def expected_input_coverage() -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_PATHS:
        blob = git_blob(path)
        is_json = path.endswith(".json")
        parsed = strict_json_loads(blob.decode("utf-8"), path) if is_json else None
        rows.append({
            "path": path,
            "read_range": f"1-{blob.count(bytes([10]))}",
            "line_count": blob.count(bytes([10])),
            "byte_count": len(blob),
            "git_blob_sha256": hashlib.sha256(blob).hexdigest(),
            "hash_basis": f"Git blob bytes at {BASELINE}",
            "parse_mode": "UTF-8 strict duplicate-key-rejecting json.loads plus full recursive traversal" if is_json else "UTF-8 text 1..EOF",
            "recursive_node_count": recursive_nodes(parsed) if is_json else 0,
        })
    return rows


def source_universe() -> tuple[list[tuple[str, str, int, str, dict[str, Any]]], dict[str, Any]]:
    roadmap = load_json_blob(ROADMAP_PATH)
    delta = load_json_blob(DELTA_PATH)
    four_axis = load_json_blob(FOUR_AXIS_PATH)
    if len(roadmap.get("items", [])) != 12:
        fail("frozen roadmap universe is not 12 items")
    if len(delta.get("old_deltas", [])) != 34 or len(delta.get("new_blockers", [])) != 6:
        fail("frozen blocker-delta universe is not 34 old plus 6 new")
    if len(four_axis.get("high_risk_findings", [])) != 11:
        fail("frozen four-axis high-risk universe is not 11")
    records: list[tuple[str, str, int, str, dict[str, Any]]] = []
    for index, row in enumerate(roadmap["items"]):
        records.append((ROADMAP_PATH, "items", index, row["item_id"], row))
    for index, row in enumerate(delta["old_deltas"]):
        records.append((DELTA_PATH, "old_deltas", index, row["old_id"], row))
    for index, row in enumerate(delta["new_blockers"]):
        records.append((DELTA_PATH, "new_blockers", index, row["blocker_id"], row))
    return records, four_axis


def expected_category(source_id: str, row: dict[str, Any], collection: str) -> str:
    if collection == "items":
        return ROADMAP_CATEGORY[source_id]
    category = row["old_category"] if collection == "old_deltas" else row["category"]
    mapping = {
        "carry_forward_asset": "PRESERVED_ASSET",
        "repair_blocker": "REPAIR_BLOCKER",
        "new_scope_blocker": "NEW_SCOPE_BLOCKER",
        "evidence_debt": "EVIDENCE_DEBT",
    }
    return mapping[category]


def expected_category_basis(source_id: str, row: dict[str, Any], collection: str, category: str) -> str:
    if collection == "items":
        return ROADMAP_CATEGORY_BASIS[source_id]
    source_category = row["old_category"] if collection == "old_deltas" else row["category"]
    return (
        f"Lossless Step 39.2 category mapping: {source_category} -> {category}; "
        "the frozen source category and original target fields remain verbatim in source_route.source_record."
    )


def expected_domain(source_id: str) -> str:
    if source_id in MIXED_DOMAIN:
        return "MIXED_INTERNAL_EXTERNAL"
    if source_id in EXTERNAL_DOMAIN:
        return "EXTERNAL_VALIDITY"
    return "INTERNAL_CONFORMANCE"


def expected_carry_id(source_id: str) -> str:
    if source_id.startswith("P059-RM-"):
        return source_id.replace("P059-RM-", "P059-CFR-RM-")
    if source_id.startswith("P059-BD-NEW-"):
        return source_id.replace("P059-BD-NEW-", "P059-CFR-BD-NEW-")
    return f"P059-CFR-{source_id}"


def expected_acceptance(row: dict[str, Any], collection: str) -> str:
    if collection == "items":
        return row["acceptance_criterion"]
    if collection == "old_deltas":
        return row["effective_acceptance_criterion"]
    return row["acceptance_criterion"]


def expected_original_targets(row: dict[str, Any], collection: str) -> dict[str, Any]:
    if collection == "old_deltas":
        original = row["original_item"]
        return {key: original[key] for key in ("target_phases", "target_phase", "resolve_by_phase") if key in original}
    if collection == "new_blockers":
        return {key: row[key] for key in ("target_phase", "post_audit_target_phases") if key in row}
    return {}


def normalized_scientific_basis(value: str) -> str:
    normalized = value.lower()
    normalized = re.sub(r"p059-[a-z0-9-]+", "<id>", normalized)
    normalized = re.sub(r"\b(implemented|theory_only|new_scope|repair_blocker|new_scope_blocker|evidence_debt)\b", "<class>", normalized)
    normalized = re.sub(r"\b\d+(?:\.\d+)?\b", "<n>", normalized)
    return " ".join(normalized.split())


def expected_target_basis(source_id: str, row: dict[str, Any], collection: str, target: int) -> str:
    special = {
        "P059-RM-003": "P075 is the primary owner because Cahn-Hilliard gradient energy, mobility, boundary conditions, elasticity and nucleation are equilibrium/phase-field closure; P076 is only a downstream kinetics consumer.",
        "P059-RM-006": "P067 owns internal n(T)>0 enforcement, default conformance and persistent n_T1 regression gates; P072 supplies data provenance and feasibility; P086 owns substantive real-data n(T) estimation, cross-temperature recovery, uncertainty and held-out validation.",
        "P059-RM-008": "P071/P072/P078 supply literature, data feasibility and LCO model prerequisites; P086 owns source-backed Omega/dH_a estimation, cross-temperature/rate recovery, uncertainty and held-out validation.",
        "CF-01": "P065 must verify whether v1.0.24/24.1 unique theory preserved or altered the bounded ideal logistic identity across fresh/default/profile paths.",
        "CF-02": "P065 must trace the v1.0.24/24.1 regular-solution and material-decomposition lineage before preserving homogeneous algebra.",
        "CF-06": "P065 must re-audit v1.0.24/24.1 entropy/heat theory and profile/default behavior before preserving sign-bounded identities.",
        "CF-07": "P065 must re-audit the v1.0.24/24.1 electronic-entropy/material-decomposition lineage without promoting placeholders.",
        "RB-02": "P065 must determine whether v1.0.24/24.1 skew/material decomposition conflated homogeneous, spinodal, binodal and measured branches.",
        "RB-03": "P065 must re-audit v1.0.24/24.1 profile/default transition topology and material-decomposition authority.",
        "CF-09": "P066 must inspect v1.0.25/25.2 unique documents, direct14 empirical success and physical-authority language while preserving exact source tiers.",
    }
    rationale = special.get(source_id)
    if rationale is None:
        acceptance = expected_acceptance(row, collection)
        rationale = f"This phase owns {source_id} because its exact routed acceptance is: {acceptance} Passing the phase gate does not itself close the item."
    return f"{TARGET_PHASE_BASIS[target]} {rationale}"


def expected_target_context(source_id: str) -> dict[str, list[int]]:
    return TARGET_CONTEXT.get(source_id, {"prerequisite_phases": [], "related_downstream_phases": []})


def expected_schedule_reconciliation(source_id: str, row: dict[str, Any], collection: str) -> dict[str, Any]:
    if source_id not in SCHEDULE_RECONCILIATION_IDS:
        return {"applicability": "NOT_REQUIRED_NO_LEGACY_PHASE069_SUBSTANTIVE_TARGET"}
    original_targets = expected_original_targets(row, collection)
    post_targets = original_targets.get("post_audit_target_phases", [])
    selected = TARGET_PHASE[source_id]
    if post_targets:
        post_role = (
            "PRESERVED_PREREQUISITE_OR_INTERMEDIATE_PHASES; selected successor is among them"
            if selected in post_targets
            else "PRESERVED_PREREQUISITE_OR_INTERMEDIATE_PHASES; P086 adds the missing external-validation execution owner"
        )
    else:
        post_role = "NOT_PRESENT_IN_FROZEN_SOURCE"
    return {
        "applicability": "REQUIRED_LEGACY_PHASE069_OR_NEW_BLOCKER_SCHEDULE",
        "legacy_acceptance_criterion": expected_acceptance(row, collection),
        "legacy_target_fields": original_targets,
        "phase059_temporal_state": "CURRENT_PHASE_059_NOT_MISSED",
        "phase069_role": "AUDIT_SYNTHESIS_AND_GO_ACTIVATION_DECISION_ONLY",
        "substantive_acceptance_state": "OPEN_UNCHANGED_BY_SCHEDULE_RECONCILIATION",
        "successor_execution_target_phase": selected,
        "successor_target_supersession": "NEW_MASTER_POST_GATE_EXECUTION_OWNER_SUPERSEDES_LEGACY_PHASE069_SUBSTANTIVE_DEADLINE",
        "activation_condition": "PHASE_069_GO_OR_CONDITIONAL_GO_REQUIRED",
        "source_post_audit_target_phases_role": post_role,
    }


def expected_evidence_state(row: dict[str, Any], collection: str) -> dict[str, Any]:
    if collection == "items":
        return {
            "source_step": "38.5",
            "primary_classification": row["primary_classification"],
            "secondary_status": row["secondary_status"],
            "closure_interpretation": "SOURCE_DISPOSITION_PRESERVED_ACCEPTANCE_REMAINS_OPEN",
        }
    if collection == "old_deltas":
        return {
            "source_step": "39.2",
            "delta_status": row["delta_status"],
            "acceptance_audit_conclusion": row["acceptance_criterion_audit"]["conclusion"],
            "closure_interpretation": "NOT_RESOLVED",
        }
    return {
        "source_step": "39.2",
        "delta_status": "NEW_OPEN_BLOCKER",
        "closure_interpretation": "NOT_RESOLVED",
    }


def expected_blocking_authority(category: str) -> str:
    if category == "PRESERVED_ASSET":
        return "NON_BLOCKING_PRESERVATION_AUTHORITY"
    if category == "REPAIR_BLOCKER":
        return "Blocks internal canonical conformance until the exact acceptance criterion is satisfied; it does not establish an external material verdict."
    if category == "NEW_SCOPE_BLOCKER":
        return "Blocks promotion of this proposed scope into the canonical model; it does not invalidate the bounded existing model."
    return "Blocks canonical or material claim authority that depends on the missing evidence; it does not invalidate an internal calculation by existence alone."


def expected_authority_boundary(category: str, domain: str) -> str:
    if category == "PRESERVED_ASSET":
        return "This is a preserved internal audit/theory/code asset. Preservation does not establish external material validity, literature truth, parameter validity, or acceptance closure."
    return (
        f"This {domain} route is OPEN. Frozen source evidence and internal conformance findings do not establish external material validity, "
        "primary-literature truth, parameter identifiability, or acceptance closure."
    )


def expected_overlap_basis(source_id: str, other: str) -> str:
    return EXPECTED_OVERLAP_BASIS[frozenset((source_id, other))]


def expected_high_risk_basis(finding: dict[str, Any], source_id: str) -> str:
    return EXPECTED_HIGH_RISK_BASIS[(finding["finding_id"], source_id)]


def expected_source_evidence(row: dict[str, Any], collection: str) -> list[dict[str, Any]]:
    expected: list[dict[str, Any]] = []
    if collection == "items":
        for field in ("theory_evidence", "code_evidence", "test_evidence", "artifact_evidence"):
            for record in row[field]:
                expected.append({
                    "evidence_role": field,
                    "evidence_object_sha256": object_sha(record),
                    "evidence": record,
                })
    elif collection == "old_deltas":
        for record in row["phase059_evidence"]:
            expected.append({
                "evidence_role": "phase059_evidence",
                "evidence_object_sha256": object_sha(record),
                "evidence": record,
            })
        for record in row["source_four_axis_routes"]:
            expected.append({
                "evidence_role": "source_four_axis_routes",
                "evidence_object_sha256": object_sha(record),
                "evidence": record,
            })
    else:
        for record in row["phase059_evidence"]:
            expected.append({
                "evidence_role": "phase059_evidence",
                "evidence_object_sha256": object_sha(record),
                "evidence": record,
            })
    return expected


def validate_underlying_evidence(evidence: dict[str, Any]) -> None:
    path = evidence.get("path")
    if not isinstance(path, str) or "\\" in path or not path:
        fail("invalid or non-POSIX underlying evidence path")
    blob = git_blob(path)
    if "record_id" in evidence:
        document = strict_json_loads(blob.decode("utf-8"), path)
        key = evidence["record_id_key"]
        wanted = evidence["record_id"]
        matches: list[dict[str, Any]] = []
        def walk(value: Any) -> None:
            if isinstance(value, dict):
                if value.get(key) == wanted:
                    matches.append(value)
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        walk(document)
        if not any(object_sha(match) == evidence["record_sha256"] for match in matches):
            fail(f"underlying JSON record/hash not found: {path}:{wanted}")
    elif "line_start" in evidence:
        lines = blob.decode("utf-8").splitlines()
        start, end = evidence["line_start"], evidence["line_end"]
        excerpt = "\n".join(lines[start - 1:end])
        if excerpt != evidence["source_excerpt"] or hashlib.sha256(excerpt.encode()).hexdigest() != evidence["excerpt_sha256"]:
            fail(f"underlying line-range evidence mismatch: {path}:{start}-{end}")


def semantic_sha(document: dict[str, Any]) -> str:
    candidate = copy.deepcopy(document)
    candidate["determinism"]["semantic_sha256"] = ""
    return hashlib.sha256(canonical_bytes(candidate)).hexdigest()


def validate_document(document: dict[str, Any]) -> None:
    document = require_dict_exact_keys(document, TOP_LEVEL_KEYS, "document")
    require_exact_json(document.get("schema_version"), 1, "schema_version")
    require_exact_json(document.get("phase"), 59, "phase")
    require_exact_json(document.get("step"), "39.4", "step")
    require_exact_json(document.get("generated_date"), "2026-08-25", "generated_date")
    require_exact_json(document.get("baseline_commit"), BASELINE, "baseline_commit")
    require_exact_json(
        document.get("status"),
        "PASS_P059_STEP_039_4_CARRY_FORWARD_REGISTER",
        "status",
    )
    require_exact_json(document.get("scope"), EXPECTED_SCOPE, "scope")
    require_exact_json(document.get("authority_boundary"), EXPECTED_TOP_AUTHORITY, "authority_boundary")
    rules = require_dict_exact_keys(document.get("rules_and_definitions"), set(EXPECTED_RULES), "rules_and_definitions")
    require_dict_exact_keys(rules.get("categories"), set(EXPECTED_RULES["categories"]), "rules_and_definitions.categories")
    require_exact_json(rules, EXPECTED_RULES, "rules_and_definitions")
    unresolved = require_dict_exact_keys(document.get("unresolved"), set(EXPECTED_UNRESOLVED), "unresolved")
    require_exact_json(unresolved, EXPECTED_UNRESOLVED, "unresolved")
    determinism = require_dict_exact_keys(document.get("determinism"), DETERMINISM_KEYS, "determinism")
    require_exact_json(
        {key: determinism.get(key) for key in EXPECTED_DETERMINISM_STATIC},
        EXPECTED_DETERMINISM_STATIC,
        "determinism.static",
    )
    require_list(document.get("input_coverage"), "input_coverage")
    coverage = expected_input_coverage()
    require_exact_json(document.get("input_coverage"), coverage, "input_coverage")
    require_exact_json(document.get("input_corpus_sha256"), object_sha(coverage), "input_corpus_sha256")

    source_records, four_axis = source_universe()
    source_by_id = {source_id: (path, collection, index, row) for path, collection, index, source_id, row in source_records}
    if len(source_by_id) != 52:
        fail("source identity collision in frozen universe")
    items = require_list(document.get("items"), "items")
    if len(items) != 52:
        fail("carry-forward item total must be exactly 52")
    source_ids: list[Any] = []
    for index, item in enumerate(items):
        require_dict_exact_keys(item, ITEM_KEYS, f"items[{index}]")
        route = require_dict_exact_keys(
            item.get("source_route"),
            {
                "source_artifact_path", "source_collection", "source_index", "source_id",
                "source_phase", "source_record_sha256", "source_record", "reverse_link_key",
            },
            f"items[{index}].source_route",
        )
        source_ids.append(route.get("source_id"))
    expected_order = [record[3] for record in source_records]
    if source_ids != expected_order or len(set(source_ids)) != 52:
        fail("source loss, duplication, orphan, or ordering mismatch")
    carry_ids = [item.get("carry_forward_id") for item in items]
    if carry_ids != [expected_carry_id(source_id) for source_id in expected_order] or len(set(carry_ids)) != 52:
        fail("carry-forward stable ID mismatch or collision")

    categories = Counter()
    targets = Counter()
    domains = Counter()
    statuses = Counter()
    observed_edges: set[frozenset[str]] = set()
    observed_hr: dict[str, set[str]] = defaultdict(set)
    roadmap_basis_signatures: list[str] = []
    high_risk_by_id = {row["finding_id"]: row for row in four_axis["high_risk_findings"]}
    for item in items:
        route = require_dict_exact_keys(
            item.get("source_route"),
            {
                "source_artifact_path", "source_collection", "source_index", "source_id",
                "source_phase", "source_record_sha256", "source_record", "reverse_link_key",
            },
            "item.source_route",
        )
        source_id = route.get("source_id")
        path, collection, index, source_row = source_by_id[source_id]
        expected_route = {
            "source_artifact_path": path,
            "source_collection": collection,
            "source_index": index,
            "source_id": source_id,
            "source_phase": 58 if collection == "old_deltas" else 59,
            "source_record_sha256": object_sha(source_row),
            "source_record": source_row,
            "reverse_link_key": f"{path}#{collection}[{index}]/{source_id}",
        }
        require_exact_json(route, expected_route, f"{source_id}.source_route")
        require_exact_json(
            route.get("source_record_sha256"),
            object_sha(route.get("source_record")),
            f"{source_id}.source_route.source_record_sha256",
        )
        category = item.get("category")
        if not isinstance(category, str) or category not in ALLOWED_CATEGORIES or category != expected_category(source_id, source_row, collection):
            fail(f"{source_id} category overlap or mapping mismatch")
        if item.get("category_mapping_basis") != expected_category_basis(source_id, source_row, collection, category):
            fail(f"{source_id} category mapping basis mismatch")
        if item.get("category_mapping_basis_sha256") != hashlib.sha256(item["category_mapping_basis"].encode("utf-8")).hexdigest():
            fail(f"{source_id} category mapping basis hash mismatch")
        if collection == "items":
            roadmap_basis_signatures.append(normalized_scientific_basis(item["category_mapping_basis"]))
        if item.get("acceptance_criterion") != expected_acceptance(source_row, collection) or not item["acceptance_criterion"].strip():
            fail(f"{source_id} acceptance criterion loss/tamper")
        require_dict_exact_keys(
            item.get("original_target_fields"),
            set(expected_original_targets(source_row, collection)),
            f"{source_id}.original_target_fields",
        )
        require_exact_json(
            item.get("original_target_fields"),
            expected_original_targets(source_row, collection),
            f"{source_id}.original_target_fields",
        )
        target = item.get("target_phase")
        if type(target) is not int:
            fail(f"{source_id} target_phase must be a JSON integer")
        if target != TARGET_PHASE[source_id] or not (60 <= target <= 90):
            fail(f"{source_id} invalid or scientifically misrouted target phase")
        horizon = "PRE_FREEZE_060_069" if target <= 69 else "POST_GATE_070_090"
        gate = "NOT_APPLICABLE" if target <= 69 else "PHASE_069_GO_OR_CONDITIONAL_GO_REQUIRED"
        if item.get("target_horizon") != horizon or item.get("activation_gate") != gate:
            fail(f"{source_id} target horizon/gate mismatch")
        if item.get("target_basis") != expected_target_basis(source_id, source_row, collection, target):
            fail(f"{source_id} target basis mismatch")
        require_dict_exact_keys(
            item.get("target_phase_context"),
            {"prerequisite_phases", "related_downstream_phases"},
            f"{source_id}.target_phase_context",
        )
        require_exact_json(
            item.get("target_phase_context"),
            expected_target_context(source_id),
            f"{source_id}.target_phase_context",
        )
        expected_schedule = expected_schedule_reconciliation(source_id, source_row, collection)
        require_dict_exact_keys(item.get("schedule_reconciliation"), set(expected_schedule), f"{source_id}.schedule_reconciliation")
        require_exact_json(
            item.get("schedule_reconciliation"),
            expected_schedule,
            f"{source_id}.schedule_reconciliation",
        )
        domain = expected_domain(source_id)
        if item.get("validity_domain") != domain or domain not in ALLOWED_DOMAINS:
            fail(f"{source_id} internal/external validity-domain mismatch")
        if item.get("blocking_authority") != expected_blocking_authority(category):
            fail(f"{source_id} blocking-authority mismatch")
        if item.get("authority_boundary") != expected_authority_boundary(category, domain):
            fail(f"{source_id} authority-boundary mismatch")
        expected_state = expected_evidence_state(source_row, collection)
        require_dict_exact_keys(item.get("phase059_evidence_state"), set(expected_state), f"{source_id}.phase059_evidence_state")
        require_exact_json(
            item.get("phase059_evidence_state"),
            expected_state,
            f"{source_id}.phase059_evidence_state",
        )
        expected_non_double = (
            "This row owns exactly one frozen source identity. overlap_or_refinement_links disclose related acceptance surfaces; "
            "they do not consolidate source membership or transfer resolution, category, target, evidence, or authority."
        )
        if item.get("non_double_count_basis") != expected_non_double:
            fail(f"{source_id} non-double-count basis mismatch")
        status = item.get("status")
        open_state = item.get("open_state")
        if category == "PRESERVED_ASSET":
            if status != "PRESERVED_ACTIVE" or open_state != "NON_BLOCKING_ASSET":
                fail(f"{source_id} preserved asset presented as open/resolved/validated")
            if item.get("blocking_authority") != "NON_BLOCKING_PRESERVATION_AUTHORITY":
                fail(f"{source_id} preserved asset has blocking authority")
        else:
            if status != "OPEN" or open_state != "OPEN_ACCEPTANCE_NOT_SATISFIED":
                fail(f"{source_id} open item presented as resolved/validated")
            if "external" in item["authority_boundary"].lower() and "not" not in item["authority_boundary"].lower():
                fail(f"{source_id} possible external-validity authority inflation")
        source_evidence = require_list(item.get("source_evidence"), f"{source_id}.source_evidence")
        expected_evidence = expected_source_evidence(source_row, collection)
        require_exact_json(item.get("source_evidence"), expected_evidence, f"{source_id}.source_evidence")
        require_exact_json(
            item.get("source_evidence_sha256"),
            object_sha(source_evidence),
            f"{source_id}.source_evidence_sha256",
        )
        for evidence_index, evidence_wrapper in enumerate(source_evidence):
            require_dict_exact_keys(
                evidence_wrapper,
                {"evidence_role", "evidence_object_sha256", "evidence"},
                f"{source_id}.source_evidence[{evidence_index}]",
            )
            evidence = evidence_wrapper["evidence"]
            if not isinstance(evidence, dict):
                fail(f"{source_id} source evidence payload must be an object")
            require_exact_json(
                evidence_wrapper.get("evidence_object_sha256"),
                object_sha(evidence),
                f"{source_id}.source_evidence[{evidence_index}].evidence_object_sha256",
            )
            if "path" in evidence and (not evidence["path"] or "\\" in evidence["path"]):
                fail(f"{source_id} invalid source evidence path")
            if "path" in evidence:
                git_blob(evidence["path"])
                if "record_id" in evidence or "line_start" in evidence:
                    validate_underlying_evidence(evidence)
        overlap_links = require_list(item.get("overlap_or_refinement_links"), f"{source_id}.overlap_or_refinement_links")
        for link_index, link in enumerate(overlap_links):
            require_dict_exact_keys(link, OVERLAP_LINK_KEYS, f"{source_id}.overlap_or_refinement_links[{link_index}]")
            other = link.get("related_source_id")
            if not isinstance(other, str) or not other:
                fail(f"{source_id} overlap related_source_id must be a nonempty string")
            edge = frozenset((source_id, other))
            if len(edge) != 2 or edge not in EXPECTED_OVERLAP_EDGES:
                fail(f"{source_id} invalid overlap/refinement link")
            if (
                link.get("relation_type") != "OVERLAPPING_ACCEPTANCE_NOT_CONSOLIDATED"
                or link.get("basis") != expected_overlap_basis(source_id, other)
            ):
                fail(f"{source_id} lossy overlap/refinement link")
            observed_edges.add(edge)
        high_risk_links = require_list(item.get("four_axis_high_risk_links"), f"{source_id}.four_axis_high_risk_links")
        for link_index, link in enumerate(high_risk_links):
            require_dict_exact_keys(link, HIGH_RISK_LINK_KEYS, f"{source_id}.four_axis_high_risk_links[{link_index}]")
            finding_id = link.get("finding_id")
            if not isinstance(finding_id, str) or not finding_id:
                fail(f"{source_id} high-risk finding_id must be a nonempty string")
            if finding_id not in high_risk_by_id:
                fail(f"{source_id} invalid four-axis finding link")
            finding = high_risk_by_id[finding_id]
            if link.get("finding_record_sha256") != object_sha(finding) or link.get("source_artifact_path") != FOUR_AXIS_PATH:
                fail(f"{source_id} four-axis finding hash/path mismatch")
            if link.get("relevance_basis") != expected_high_risk_basis(finding, source_id):
                fail(f"{source_id} missing four-axis relevance basis")
            observed_hr[finding_id].add(source_id)
        categories[category] += 1
        targets[target] += 1
        domains[domain] += 1
        statuses[status] += 1

    if len(roadmap_basis_signatures) != 12 or len(set(roadmap_basis_signatures)) != 12:
        fail("roadmap category bases collapse to a generic normalized template")

    if observed_edges != EXPECTED_OVERLAP_EDGES:
        fail("overlap/refinement universe has missing or extra edges")
    for edge in EXPECTED_OVERLAP_EDGES:
        a, b = tuple(edge)
        a_links = {link["related_source_id"] for link in items[expected_order.index(a)]["overlap_or_refinement_links"]}
        b_links = {link["related_source_id"] for link in items[expected_order.index(b)]["overlap_or_refinement_links"]}
        if b not in a_links or a not in b_links:
            fail("overlap/refinement reverse membership mismatch")
    if dict(observed_hr) != EXPECTED_HIGH_RISK_ROUTES:
        fail("four-axis high-risk reverse routing mismatch")
    for finding in four_axis["high_risk_findings"]:
        for evidence in finding["evidence_links"]:
            path = evidence["source_artifact_path"]
            source = load_json_blob(path)
            collection: Any = source
            for field_part in evidence["source_field"].split("."):
                collection = collection[field_part]
            record = collection[evidence["source_index"]]
            if object_sha(record) != evidence["source_record_sha256"]:
                fail(f"four-axis underlying record mismatch: {finding['finding_id']}")

    expected_counts = {
        "source_roadmap_items": 12,
        "source_step39_2_old_deltas": 34,
        "source_step39_2_new_blockers": 6,
        "source_total": 52,
        "routed_total": 52,
        "source_orphans": 0,
        "source_duplicates": 0,
        "category_counts": dict(sorted(categories.items())),
        "target_phase_counts": {str(k): v for k, v in sorted(targets.items())},
        "target_horizon_counts": {
            "POST_GATE_070_090": sum(v for k, v in targets.items() if k >= 70),
            "PRE_FREEZE_060_069": sum(v for k, v in targets.items() if k <= 69),
        },
        "validity_domain_counts": dict(sorted(domains.items())),
        "status_counts": dict(sorted(statuses.items())),
        "overlap_edges": len(EXPECTED_OVERLAP_EDGES),
        "overlap_directed_memberships": len(EXPECTED_OVERLAP_EDGES) * 2,
        "four_axis_high_risk_findings": 11,
        "four_axis_high_risk_route_memberships": sum(len(v) for v in EXPECTED_HIGH_RISK_ROUTES.values()),
        "roadmap_category_basis_normalized_signatures": 12,
        "schedule_reconciliations_required": len(SCHEDULE_RECONCILIATION_IDS),
        "schedule_reconciliations_missing": 0,
        "external_material_truth_validated": 0,
        "invalid_target_phase": 0,
        "missing_acceptance_criterion": 0,
        "missing_authority_boundary": 0,
        "missing_source_or_reverse_link": 0,
        "open_items_presented_resolved": 0,
    }
    require_dict_exact_keys(document.get("counts"), set(expected_counts), "counts")
    require_exact_json(document.get("counts"), expected_counts, "counts")
    expected_source_reconciliation = {
        "ordered_source_ids": expected_order,
        "source_membership_sha256": object_sha(expected_order),
        "roadmap": {"path": ROADMAP_PATH, "collection": "items", "count": 12},
        "step39_2_old": {"path": DELTA_PATH, "collection": "old_deltas", "count": 34},
        "step39_2_new": {"path": DELTA_PATH, "collection": "new_blockers", "count": 6},
        "routing_method": "52 direct rows; overlap/refinement edges are disclosure-only and do not consume a second source membership.",
    }
    require_dict_exact_keys(
        document.get("source_reconciliation"),
        set(expected_source_reconciliation),
        "source_reconciliation",
    )
    require_exact_json(
        document.get("source_reconciliation"),
        expected_source_reconciliation,
        "source_reconciliation",
    )
    four_axis_boundary = require_dict_exact_keys(
        document.get("four_axis_boundary"),
        FOUR_AXIS_BOUNDARY_KEYS,
        "four_axis_boundary",
    )
    require_dict_exact_keys(four_axis_boundary.get("status_counts"), set(four_axis["counts"]["status_counts"]), "four_axis_boundary.status_counts")
    require_dict_exact_keys(
        four_axis_boundary.get("direct_related_not_applicable"),
        {"DIRECT", "RELATED_NOT_DIRECT", "NOT_APPLICABLE"},
        "four_axis_boundary.direct_related_not_applicable",
    )
    require_list(four_axis_boundary.get("high_risk_findings"), "four_axis_boundary.high_risk_findings")
    require_exact_json(
        four_axis_boundary.get("status_counts"),
        four_axis["counts"]["status_counts"],
        "four_axis_boundary.status_counts",
    )
    require_exact_json(
        four_axis_boundary.get("high_risk_findings"),
        four_axis["high_risk_findings"],
        "four_axis_boundary.high_risk_findings",
    )
    require_exact_json(
        four_axis_boundary.get("high_risk_findings_sha256"),
        object_sha(four_axis_boundary.get("high_risk_findings")),
        "four_axis_boundary.high_risk_findings_sha256",
    )
    require_exact_json(
        four_axis_boundary.get("source_artifact_path"),
        FOUR_AXIS_PATH,
        "four_axis_boundary.source_artifact_path",
    )
    require_exact_json(
        four_axis_boundary.get("authority_boundary"),
        four_axis["authority_boundary"],
        "four_axis_boundary.authority_boundary",
    )
    require_exact_json(
        four_axis_boundary.get("direct_related_not_applicable"),
        {"DIRECT": 42, "RELATED_NOT_DIRECT": 63, "NOT_APPLICABLE": 558},
        "four_axis_boundary.direct_related_not_applicable",
    )
    require_exact_json(
        four_axis_boundary.get("external_truth_authority"),
        "NOT_ESTABLISHED",
        "four_axis_boundary.external_truth_authority",
    )
    require_exact_json(
        document.get("determinism", {}).get("semantic_sha256"),
        semantic_sha(document),
        "determinism.semantic_sha256",
    )


def seal(document: dict[str, Any]) -> None:
    document["determinism"]["semantic_sha256"] = ""
    document["determinism"]["semantic_sha256"] = semantic_sha(document)


def run_negative_probes(base: dict[str, Any]) -> tuple[int, float]:
    mutations: list[tuple[str, Any]] = [
        ("drop_source", lambda d: d["items"].pop()),
        ("duplicate_source", lambda d: d["items"].append(copy.deepcopy(d["items"][0]))),
        ("orphan_source_id", lambda d: d["items"][0]["source_route"].update(source_id="MISSING")),
        ("source_record_tamper", lambda d: d["items"][0]["source_route"]["source_record"].update(topic="fake")),
        ("source_record_hash_tamper", lambda d: d["items"][0]["source_route"].update(source_record_sha256="0" * 64)),
        ("reverse_link_tamper", lambda d: d["items"][0]["source_route"].update(reverse_link_key="fake")),
        ("illegal_category", lambda d: d["items"][0].update(category="OPEN_BLOCKER")),
        ("category_overlap", lambda d: d["items"][0].update(category=["PRESERVED_ASSET", "EVIDENCE_DEBT"])),
        ("category_basis_tamper", lambda d: d["items"][0].update(category_mapping_basis="plausible but wrong mapping basis")),
        ("category_basis_hash_tamper", lambda d: d["items"][0].update(category_mapping_basis_sha256="0" * 64)),
        (
            "roadmap_category_generic_collapse",
            lambda d: [
                item.update(
                    category_mapping_basis="Generic source classification is routed without item-specific scientific reasoning.",
                    category_mapping_basis_sha256=hashlib.sha256(
                        b"Generic source classification is routed without item-specific scientific reasoning."
                    ).hexdigest(),
                )
                for item in d["items"]
                if item["source_route"]["source_collection"] == "items"
            ],
        ),
        ("blank_acceptance", lambda d: d["items"][0].update(acceptance_criterion="")),
        ("original_target_tamper", lambda d: next(i for i in d["items"] if i["source_route"]["source_collection"] == "old_deltas").update(original_target_fields={})),
        ("past_target", lambda d: d["items"][0].update(target_phase=59)),
        ("wrong_target", lambda d: d["items"][0].update(target_phase=90)),
        ("rm003_wrong_primary_target", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-003").update(target_phase=76)),
        ("rm006_wrong_evidence_target", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-006").update(target_phase=72)),
        ("rm008_wrong_evidence_target", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-008").update(target_phase=72)),
        ("phase065_basis_generic", lambda d: next(i for i in d["items"] if i["target_phase"] == 65).update(target_basis="Phase 065 performs a generic earlier-version audit.")),
        ("phase066_basis_generic", lambda d: next(i for i in d["items"] if i["target_phase"] == 66).update(target_basis="Phase 066 performs a generic later-version audit.")),
        ("rm006_p072_prerequisite_drop", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-006").update(target_phase_context={"prerequisite_phases": [], "related_downstream_phases": []})),
        ("rm006_p067_prerequisite_drop", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-006").update(target_phase_context={"prerequisite_phases": [72], "related_downstream_phases": []})),
        ("post_gate_removed", lambda d: next(i for i in d["items"] if i["target_phase"] >= 70).update(activation_gate="NOT_APPLICABLE")),
        ("blank_target_basis", lambda d: d["items"][0].update(target_basis="")),
        ("schedule_required_drop", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "NS-01").update(schedule_reconciliation={"applicability": "NOT_REQUIRED_NO_LEGACY_PHASE069_SUBSTANTIVE_TARGET"})),
        ("schedule_legacy_acceptance_tamper", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "NS-01")["schedule_reconciliation"].update(legacy_acceptance_criterion="plausible but wrong acceptance")),
        ("schedule_false_missed", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "NS-02")["schedule_reconciliation"].update(phase059_temporal_state="MISSED_DEADLINE")),
        ("schedule_phase069_execution_owner", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "ED-01")["schedule_reconciliation"].update(phase069_role="SUBSTANTIVE_EXECUTION_OWNER")),
        ("schedule_successor_tamper", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-BD-NEW-002")["schedule_reconciliation"].update(successor_execution_target_phase=72)),
        ("schedule_activation_tamper", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-BD-NEW-005")["schedule_reconciliation"].update(activation_condition="PHASE_069_GO_ONLY")),
        ("schedule_post_audit_role_tamper", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-BD-NEW-002")["schedule_reconciliation"].update(source_post_audit_target_phases_role="P086_PRESENT_IN_FROZEN_SOURCE")),
        ("blank_authority", lambda d: d["items"][0].update(authority_boundary="")),
        ("external_overclaim", lambda d: next(i for i in d["items"] if i["validity_domain"] == "EXTERNAL_VALIDITY").update(authority_boundary="External validity established")),
        ("preserved_marked_open", lambda d: next(i for i in d["items"] if i["category"] == "PRESERVED_ASSET").update(status="OPEN")),
        ("preserved_blocking", lambda d: next(i for i in d["items"] if i["category"] == "PRESERVED_ASSET").update(blocking_authority="BLOCKS_RELEASE")),
        ("open_marked_resolved", lambda d: next(i for i in d["items"] if i["category"] != "PRESERVED_ASSET").update(status="RESOLVED")),
        ("domain_tamper", lambda d: d["items"][0].update(validity_domain="EXTERNAL_VALIDITY")),
        ("rm006_external_only_domain", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-006").update(validity_domain="EXTERNAL_VALIDITY")),
        ("overlap_drop", lambda d: next(i for i in d["items"] if i["overlap_or_refinement_links"])["overlap_or_refinement_links"].pop()),
        ("overlap_extra", lambda d: d["items"][0]["overlap_or_refinement_links"].append({"related_source_id":"RB-13","relation_type":"OVERLAPPING_ACCEPTANCE_NOT_CONSOLIDATED","basis":"fake"})),
        ("overlap_basis_tamper", lambda d: next(i for i in d["items"] if i["overlap_or_refinement_links"])["overlap_or_refinement_links"][0].update(basis="plausible but wrong overlap basis")),
        ("overlap_rm002_rb02_drop", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-002")["overlap_or_refinement_links"].__setitem__(slice(None), [x for x in next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-002")["overlap_or_refinement_links"] if x["related_source_id"] != "RB-02"])),
        ("overlap_rm004_rb06_drop", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-004")["overlap_or_refinement_links"].__setitem__(slice(None), [x for x in next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-004")["overlap_or_refinement_links"] if x["related_source_id"] != "RB-06"])),
        ("overlap_new005_rb06_drop", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-BD-NEW-005")["overlap_or_refinement_links"].__setitem__(slice(None), [x for x in next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-BD-NEW-005")["overlap_or_refinement_links"] if x["related_source_id"] != "RB-06"])),
        ("overlap_rm008_rb09_drop", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-008")["overlap_or_refinement_links"].__setitem__(slice(None), [x for x in next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-008")["overlap_or_refinement_links"] if x["related_source_id"] != "RB-09"])),
        ("overlap_rm011_cf09_drop", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-011")["overlap_or_refinement_links"].__setitem__(slice(None), [x for x in next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-011")["overlap_or_refinement_links"] if x["related_source_id"] != "CF-09"])),
        ("overlap_generic_basis", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-008")["overlap_or_refinement_links"][0].update(basis="These records overlap but remain distinct.")),
        ("high_risk_drop", lambda d: next(i for i in d["items"] if i["four_axis_high_risk_links"])["four_axis_high_risk_links"].pop()),
        ("high_risk_hash_tamper", lambda d: next(i for i in d["items"] if i["four_axis_high_risk_links"])["four_axis_high_risk_links"][0].update(finding_record_sha256="0" * 64)),
        ("high_risk_new005_hr001_drop", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-BD-NEW-005")["four_axis_high_risk_links"].__setitem__(slice(None), [x for x in next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-BD-NEW-005")["four_axis_high_risk_links"] if x["finding_id"] != "P059-F4-HR-001"])),
        ("high_risk_rm004_hr003_drop", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-004")["four_axis_high_risk_links"].__setitem__(slice(None), [x for x in next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-004")["four_axis_high_risk_links"] if x["finding_id"] != "P059-F4-HR-003"])),
        ("high_risk_new005_hr003_drop", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-BD-NEW-005")["four_axis_high_risk_links"].__setitem__(slice(None), [x for x in next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-BD-NEW-005")["four_axis_high_risk_links"] if x["finding_id"] != "P059-F4-HR-003"])),
        ("high_risk_basis_generic", lambda d: next(i for i in d["items"] if i["source_route"]["source_id"] == "P059-RM-004")["four_axis_high_risk_links"][0].update(relevance_basis="This is a generic high-risk relation.")),
        ("input_drop", lambda d: d["input_coverage"].pop()),
        ("input_hash_tamper", lambda d: d["input_coverage"][0].update(git_blob_sha256="0" * 64)),
        ("baseline_tamper", lambda d: d.update(baseline_commit="0" * 40)),
        ("corpus_hash_tamper", lambda d: d.update(input_corpus_sha256="0" * 64)),
        ("count_tamper", lambda d: d["counts"].update(routed_total=51)),
        ("schema_version_bool", lambda d: d.update(schema_version=True)),
        ("count_source_orphans_bool", lambda d: d["counts"].update(source_orphans=False)),
        ("source_route_source_index_bool", lambda d: d["items"][0]["source_route"].update(source_index=False)),
        (
            "source_record_register_index_bool",
            lambda d: d["items"][12]["source_route"]["source_record"].update(source_register_index=False),
        ),
        (
            "evidence_register_route_index_bool",
            lambda d: d["items"][15]["source_evidence"][1]["evidence"].update(register_route_index=True),
        ),
        ("schema_version_float", lambda d: d.update(schema_version=1.0)),
        ("count_routed_total_float", lambda d: d["counts"].update(routed_total=52.0)),
        ("source_route_source_index_float", lambda d: d["items"][0]["source_route"].update(source_index=0.0)),
        ("scope_authority_overclaim", lambda d: d.update(scope="External material validity ESTABLISHED")),
        ("top_authority_overclaim", lambda d: d.update(authority_boundary="Primary literature and external material validity ESTABLISHED")),
        ("rules_authority_overclaim", lambda d: d["rules_and_definitions"].update(authority_rule="Internal PASS establishes external material truth.")),
        ("unresolved_external_overclaim", lambda d: d["unresolved"].update(external_validity="External material validation ESTABLISHED.")),
        ("unknown_top_established_key", lambda d: d.update(external_truth="ESTABLISHED")),
        ("unknown_item_established_key", lambda d: d["items"][0].update(external_truth="ESTABLISHED")),
        ("unknown_four_axis_established_key", lambda d: d["four_axis_boundary"].update(material_truth="ESTABLISHED")),
        ("unknown_overlap_established_key", lambda d: next(i for i in d["items"] if i["overlap_or_refinement_links"])["overlap_or_refinement_links"][0].update(shared_truth="ESTABLISHED")),
        ("unknown_high_risk_established_key", lambda d: next(i for i in d["items"] if i["four_axis_high_risk_links"])["four_axis_high_risk_links"][0].update(external_truth="ESTABLISHED")),
        ("unknown_rules_established_key", lambda d: d["rules_and_definitions"].update(external_truth="ESTABLISHED")),
        ("malformed_scalar_item", lambda d: d["items"].__setitem__(0, "scalar item")),
        ("malformed_overlap_none", lambda d: next(i for i in d["items"] if i["overlap_or_refinement_links"]).update(overlap_or_refinement_links=None)),
        ("malformed_high_risk_none", lambda d: next(i for i in d["items"] if i["four_axis_high_risk_links"]).update(four_axis_high_risk_links=None)),
        ("malformed_four_axis_string", lambda d: d.update(four_axis_boundary="ESTABLISHED")),
        ("malformed_overlap_related_id_list", lambda d: next(i for i in d["items"] if i["overlap_or_refinement_links"])["overlap_or_refinement_links"][0].update(related_source_id=[])),
        ("malformed_high_risk_finding_id_list", lambda d: next(i for i in d["items"] if i["four_axis_high_risk_links"])["four_axis_high_risk_links"][0].update(finding_id=[])),
        ("four_axis_overclaim", lambda d: d["four_axis_boundary"].update(external_truth_authority="ESTABLISHED")),
        ("four_axis_partition_tamper", lambda d: d["four_axis_boundary"]["direct_related_not_applicable"].update(DIRECT=43)),
        ("evidence_hash_tamper", lambda d: d["items"][0].update(source_evidence_sha256="0" * 64)),
        ("source_evidence_drop_resealed", lambda d: (d["items"][0]["source_evidence"].pop(), d["items"][0].update(source_evidence_sha256=object_sha(d["items"][0]["source_evidence"])))),
        ("evidence_state_tamper", lambda d: d["items"][0]["phase059_evidence_state"].update(closure_interpretation="RESOLVED")),
        ("semantic_hash_tamper", lambda d: None),
    ]
    started = time.perf_counter()
    rejected = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        seal(candidate)
        if name == "semantic_hash_tamper":
            candidate["determinism"]["semantic_sha256"] = "0" * 64
        try:
            validate_document(candidate)
        except ValidationFailure as exc:
            print(f"{name}: REJECTED ({exc})")
            rejected += 1
        else:
            fail(f"negative mutation unexpectedly passed: {name}")
    raw = json.dumps(base, ensure_ascii=False, sort_keys=True)
    raw = raw.replace("{", '{"schema_version":999,', 1)
    try:
        strict_json_loads(raw, "raw_duplicate_json_key_probe")
    except ValidationFailure as exc:
        print(f"raw_duplicate_json_key: REJECTED ({exc})")
        rejected += 1
    else:
        fail("negative raw duplicate-key mutation unexpectedly passed")
    return rejected, time.perf_counter() - started


def apply_cli_malformed_probe(document: dict[str, Any], probe: str) -> None:
    if probe == "scalar_item":
        document["items"][0] = "scalar item"
    elif probe == "overlap_none":
        next(item for item in document["items"] if item["overlap_or_refinement_links"])["overlap_or_refinement_links"] = None
    elif probe == "high_risk_none":
        next(item for item in document["items"] if item["four_axis_high_risk_links"])["four_axis_high_risk_links"] = None
    elif probe == "four_axis_string":
        document["four_axis_boundary"] = "ESTABLISHED"
    elif probe == "overlap_related_id_list":
        next(item for item in document["items"] if item["overlap_or_refinement_links"])["overlap_or_refinement_links"][0]["related_source_id"] = []
    elif probe == "high_risk_finding_id_list":
        next(item for item in document["items"] if item["four_axis_high_risk_links"])["four_axis_high_risk_links"][0]["finding_id"] = []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--artifact-path", type=pathlib.Path, default=ARTIFACT)
    parser.add_argument(
        "--cli-malformed-probe",
        choices=(
            "scalar_item", "overlap_none", "high_risk_none", "four_axis_string",
            "overlap_related_id_list", "high_risk_finding_id_list",
        ),
    )
    args = parser.parse_args()
    artifact_path = args.artifact_path
    if not artifact_path.exists():
        print(f"FAIL_P059_STEP_039_4_CARRY_FORWARD_REGISTER: missing artifact: {artifact_path.as_posix()}")
        return 1
    try:
        document = strict_json_loads(artifact_path.read_text(encoding="utf-8"), artifact_path.as_posix())
        if args.cli_malformed_probe:
            apply_cli_malformed_probe(document, args.cli_malformed_probe)
        validate_document(document)
        if args.run_negative_probes:
            rejected, elapsed = run_negative_probes(document)
            print(f"PASS_NEGATIVE_MUTATION_PROBES rejected={rejected} runtime_seconds={elapsed:.3f}")
    except (ValidationFailure, UnicodeDecodeError) as exc:
        print(f"FAIL_P059_STEP_039_4_CARRY_FORWARD_REGISTER: {exc}")
        return 1
    print("PASS_P059_STEP_039_4_CARRY_FORWARD_REGISTER items=52 sources=12+34+6 orphan=0 external_truth=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
