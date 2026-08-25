#!/usr/bin/env python3
"""Independently validate Phase 059 Step 39.3 conformance artifacts."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "b73652bb131d2772be483c4b1730aa8f3161baf5"
CODE_PATH = "Codex/results/PHASE_059_CODE_BEHAVIOR_MATRIX.json"
TEST_PATH = "Codex/results/PHASE_059_TEST_DEMO_CLAIM_MATRIX.json"
MAIN_PATH = "Codex/results/PHASE_059_FOUR_AXIS_CONFORMANCE_MATRIX.json"
BUILDER_PATH = "Codex/work/v1014_v1018_2_phase059/build_phase059_four_axis_conformance.py"
SEMANTIC_ONTOLOGY_ID = "P059-SEMANTIC-CONCEPT-ONTOLOGY-V1"
LINK_MATRIX_PATH_BY_CLASS = {
    "CODE": CODE_PATH,
    "TEST_RUNTIME": TEST_PATH,
    "STORED_ARTIFACT": TEST_PATH,
}
AXIS_ROLE_BY_CLASS = {
    "CODE": "DIRECT_STATIC_BEHAVIOR_EVIDENCE",
    "TEST_RUNTIME": "DIRECT_TEST_RUNTIME_OR_PROBE_EVIDENCE",
    "STORED_ARTIFACT": "DIRECT_CANONICAL_STORED_ARTIFACT_EVIDENCE",
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
ALLOWED_APPLICABILITY = {"DIRECT", "RELATED_NOT_DIRECT", "NOT_APPLICABLE"}
ADJUDICATION_BOUNDARY = (
    "This decision states only whether one frozen production finding is directly applicable "
    "to one frozen theory claim; it does not establish external material validity."
)
AXIS_KEYS = {"axis", "state", "evidence_links", "boundary"}
LINK_KEYS = {"evidence_class", "evidence_id", "matrix_path", "source_artifact_path", "source_field", "source_index", "source_record_sha256", "role", "basis"}
ROW_KEYS = {"claim_id", "theory_claim_sha256", "theory_axis", "production_axis", "test_runtime_axis", "stored_artifact_axis", "conformance_status", "decision_basis", "authority_boundary", "code_impact", "blocker_routes", "blocker_route_basis"}
ADJUDICATION_KEYS = {"adjudication_id", "code_finding_id", "applicability", "shared_contract_ids", "direct_contract_ids", "theory_relation_ids", "claim_basis_sha256", "code_basis_sha256", "claim_semantic_scope_sha256", "code_semantic_scope_sha256", "semantic_audit_method", "pair_graph_audit", "na_pair_grounding_id", "comparison", "basis", "authority_boundary"}
CLAIM_LEDGER_KEYS = {"claim_id", "claim_sha256", "claim_semantic_scope", "evidence_contract_ids", "evidence_relation_ids", "code_finding_adjudications", "direct_code_evidence_ids", "direct_code_relation_count", "authority_boundary"}
COMPARISON_KEYS = {"claim_quantity_or_dependency", "finding_affected_quantity_or_path", "overlap_or_dependency_path", "classification_reason", "exclusion_boundary"}
CLAIM_SCOPE_KEYS = {"claim_id", "claim_kind", "family", "labels", "contract_topics", "required_actions", "derivation_status", "code_impact_assessment", "source_anchor_refs", "source_relation_texts", "claim_quantity_or_dependency", "dependency_direction", "required_evidence_or_action", "non_goal", "semantic_concepts"}
FINDING_SCOPE_KEYS = {"code_finding_id", "title", "claim", "consequence", "required_action", "contract_ids", "source_evidence", "actual_production_behavior", "finding_affected_quantity_or_path", "non_adjudicated_quantities", "semantic_concepts"}
NA_GROUNDING_KEYS = {"grounding_id", "pair_id", "claim_id", "code_finding_id", "grounding_group_id", "grounding_group_sha256", "examined_claim_anchors", "examined_claim_quantities", "examined_finding_anchors", "examined_finding_behavior", "pair_graph_audit_id", "pair_graph_audit_sha256", "executed_quantity_intersection", "dependency_reachability", "contradiction_finding", "nonconnection_certificate", "conclusion_specific_rationale", "exclusion_boundary", "review_checks", "shared_contract_candidates", "claim_scope_sha256", "code_scope_sha256", "structural_signature_basis", "structural_signature_sha256", "reasoning_signature_sha256", "authority_boundary", "grounding_sha256"}
NA_GROUP_KEYS = {"grounding_group_id", "claim_primary_concept", "finding_behavior_concept", "incident_ontology_edges", "grouping_basis", "grounding_group_sha256", "member_pair_ids", "member_count"}
PAIR_GRAPH_AUDIT_KEYS = {"pair_graph_audit_id", "pair_id", "classification_derivation", "claim_graph", "finding_graph", "cross_domain_bridges", "traversal_result", "structural_signature_basis", "structural_signature_sha256", "authority_boundary", "pair_graph_audit_sha256"}
BRIDGE_KEYS = {"bridge_id", "pair_id", "kind", "source_node", "target_node", "path", "matched_scientific_concept", "shared_executed_quantity_node", "scientific_basis", "claim_anchor_sha256", "finding_anchor_sha256", "authority_boundary", "bridge_sha256"}

EXPECTED_CLAIM_SEMANTIC_TUPLE_SHA256 = {
    "P059-TCL-001": "acb28561a9fdd7a200f6abde215633b6fa083ab6f6f9da81694f1dc46ba208a5", "P059-TCL-002": "26102b88736e2df596aaab2e6d79586da3551075f3782f5096c86d9bf24c2d7f", "P059-TCL-003": "fbb2d3108f32f96f2b7979859e6868050a79478be9484945c4967b3baeb03f5a", "P059-TCL-004": "3a129623c617bef495a3e99ac64e047a6d3d6219d44fa22732d8e353587410c1", "P059-TCL-005": "49e11e97cedc8d23d79a9ec2958949a6303d94f23e7b71c910d8efc305c21add",
    "P059-TCL-009": "266473992ea768e9785106dd741f7e82e9626de64f08c690ef9df869173e31fc", "P059-TCL-010": "2de0fb69f68a0b32933d3ca9aa1ff865354f6abceffff1aa649c0b2f836439a7", "P059-TCL-011": "d9ed8c694931aea800409efa9be1fe612e1393cf003100a868c8c2b448262bba", "P059-TCL-023": "8de8bcb65ea69eef91b94178bbe28e5176570b4e909caade86688f8dedd9fa0f", "P059-TCL-025": "7140037685044226270dfb895c5adb492bc06e9ca92affcd3497945b297e1c23",
    "P059-TCL-026": "09a65f3ed8bbeedea11ff740554ca7ae8c0d02d228b8460f3b4c8943334ae4a9", "P059-TCL-030": "7cb83b02f57355785f0e24f6cd21fbc72cdedceb44682d73214cf045dfc0f79d", "P059-TCL-033": "f72fcc9d7ba45bce24d67a9c36ec7d021df237caf54c26cd107fe9d87a5361d3", "P059-TCL-034": "aa888a59674dc32a82988bdfa8baef5395203302bff47bf64aba18fa2d55ea4f", "P059-TCL-035": "db8eb8386b0c3f3e6a15c4e20d8debd4a5cc38523d22cbb151dd793dbd843486",
    "P059-TCL-037": "6a619737c344e259a7c8211fec223217c6eae7ce480ad79a6180ddc0055fc501", "P059-TCL-039": "a2ef39011981619ab9fa6b799ea01834ca59c405517e45c7d655f49ac0a39bee", "P059-TCL-048": "6db6d730f289b0a877b744f02da1a88c0983c07257836f45e97c5f5695b7f7ee", "P059-TCL-050": "f19c3aee2d569827338a58897921d99f24d6493bf68977628e2db2d5557d2afc", "P059-TCL-053": "fd9b4b03fa23628ce35e17b79089200469fa69e3ec950a65958084f651d59e88",
    "P059-TCL-055": "2e6d55ec65013b896d37355c8788034a408dfdf4aba7c74f0551cca6e67a731c", "P059-TCL-056": "b13834efeff7853f01e85dd42ce2eccb07fb86efd99a13465c6fb2cf88cd1aeb", "P059-TCL-060": "7eec6f0d8a3346c95da58657886c4c15210ebb6f65badce5712e66de011a4fd0", "P059-TCL-061": "fc3802557effa0e0dbb2e104ec51254736fec56534e3845824635cdd72c82bd8", "P059-TCL-066": "3e90ac9c034979828a03e56814880e7bcaf7788b9379761129289b41d0e477c8",
    "P059-TCL-069": "f1f45f3db532de47c2dd6fe8691c1b356ad32e7f7335bc09dc3f0c5e0b0c5206", "P059-TCL-073": "e962819ee185fb89b8c789d4437a3d9265c50f3653dc14ddea2b8191ab540643", "P059-TCL-081": "68e1842abe19131ebf75c1261418bc0c4144809f074f450db869b91394e8d6d8", "P059-TCL-083": "ad4b02224ae4720629369fbd642aadc985b92c05facb0e0b95ac74c40ce8e438", "P059-TCL-084": "2099dc4689f4db1965755cbc709194e6a11181fcd266119ec4aaeca170dc172c",
    "P059-TCL-100": "c836cadc909ab37b23d8810666d841cb2d1de32bd76d8271eac28b20b90c81db", "P059-TCL-108": "5e0e9df9da8c3a42502bfd73354b3f7263bbe4c43da126b0bbd62e77cc070995", "P059-TCL-113": "5d6b28d7b02b5556f765644a2f9f5facb05c86c4e7b23c48b09afcde8ef49fe6", "P059-TCL-140": "4485490a7d4f1bc39d521d1f31e9a8fccacc1ab912cd5c589ec5ee9c6edb1e00", "P059-TCL-151": "d57810d2b2086bd8e105e4a95b5dcfb30ee735d9caf647ab7609b21f9fcb9b82",
    "P059-TCL-153": "2e55c341869ccb98535d65ca7e6d5a374babfa6c7c7105186559e9e25f05af46", "P059-TCL-155": "e91bd656a0533e8f3f947ac3c60af279647536de334b740e93a5792f712dbbb3", "P059-TCL-157": "f719522aec1e247a9e835cb74a54c671e9c9fe91c446e81ce63f9f413b8f8cbe", "P059-TCL-159": "691af84d975c1bbda466a1bfdc0b4acb7676e8a054c3ef2c86741d80f0133f3b", "P059-TCL-160": "964277a97d84fe77c5a519c7f47a9b571c57cc0edcdd376e57017e92b921bf92",
    "P059-TCL-164": "e17d5946e074bfe30df9b3ccef998977b783371d2ff0dc9f395b4d8b573bdd4e", "P059-TCL-165": "74d73c4dbe9281236854fc2329cec67b2b9367f7029d79020211f1eaa458398a", "P059-TCL-166": "cff48bda1a2f98b64dcaaea22e97c78a33021ce90464a289dc6711c8fc45faf0", "P059-TCL-167": "407c26ef3116b8e1f102f877b0f6db0c73e47fae98b47480bf517c7ce8acc42e", "P059-TCL-168": "84fcab3738c63a0a2dd78e1478376c83614e877653a6303e286e6806de9cd125",
    "P059-TCL-169": "562910945990426e0efe6c4c6589daffac690694c838e1e0139bf82afa09e2a7", "P059-TCL-172": "949bd783e7aef163ab357bfb5a46c1590369463de4ed5330800a0c6617a18a3c", "P059-TCL-173": "c6b7686032ebffde9f6f06d0f1b37ec258deeaa5e6c6dbf69137977ee06f820e", "P059-TCL-176": "9522477eb2a9263f7fe84db6fb6e54861633fe6b79fb28a39ea4e32ef6cb99f7", "P059-TCL-179": "8f0b25fe25f0c9f2a198a8b37554ae9299c89e6c4849d2de50b7084d5fb592f4", "P059-TCL-182": "adcb08522c02e9810c4f1c6e52d2141e6ee27e656f5bbd4456e5c193a4eb6870",
}
EXPECTED_FINDING_SEMANTIC_TUPLE_SHA256 = {
    "P059-CODE-001": "043d88818ab0360ec7581cb652ad06d6c09f468cb8d350cdfe9033bd1b3c5edb", "P059-CODE-002": "088e1792e9ef78abf7c408e97358803d883b5e96a5637fd641e367c0be7e5536", "P059-CODE-003": "cc9adda78c07871aab1b362d4b953dd88a0104a9eebd459f02e35e47da543330", "P059-CODE-004": "9633515cae489ae42647adbaa4311fecaf57edaa7890dd613068822d88904ce7", "P059-CODE-005": "489f947747f420232452cb7e33285a82168712e5bec0d43baaa3a21f2b405261", "P059-CODE-006": "4c20d8eb83b3fb697a669846683c1fc80d003f0ca13bed9a8848b2368907df5c", "P059-CODE-007": "885b99c1140824e3ebaeb1a6482756da5f2969d4ede72de74eb386db6b9c1afc", "P059-CODE-008": "e44252b06eb7b7392f4f7f67a6043827d67306507d2d286eceec3f9d970c4582", "P059-CODE-009": "74df8de24fadb9f9796788f92797e1e0f00a7afe4b52c4a7440330d2632ea1a6", "P059-CODE-010": "3d8b79588e7de0b1150aa2091e25d3d71b65138a1ef430640f69fe179b4fe09a", "P059-CODE-011": "3eb9f2a737c96539cdefc95e012904bb9eedf8c25b98839e317022326186b8f7", "P059-CODE-012": "c9cc4e5379314e335af626a1332747c07af98d97906ebf7eb617e4bad3c7151a", "P059-CODE-013": "9fe8bb4c75ed1dd33159fd40c8841d6d6c372a104deb3951239b9dc6e2e9d31d",
}


# Independent review oracle. Shared contract IDs only nominate candidates; this
# smaller map records exact equation/finding semantic joins.
EXPECTED_DIRECT_CODE: dict[str, list[str]] = {
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
EXPECTED_RELATED_CODE = {
    ("P059-TCL-004", "P059-CODE-007"), ("P059-TCL-004", "P059-CODE-010"), ("P059-TCL-004", "P059-CODE-013"),
    ("P059-TCL-026", "P059-CODE-001"), ("P059-TCL-026", "P059-CODE-003"), ("P059-TCL-026", "P059-CODE-005"),
    ("P059-TCL-030", "P059-CODE-001"), ("P059-TCL-030", "P059-CODE-003"),
    ("P059-TCL-034", "P059-CODE-009"), ("P059-TCL-034", "P059-CODE-013"), ("P059-TCL-035", "P059-CODE-002"),
    ("P059-TCL-037", "P059-CODE-009"), ("P059-TCL-037", "P059-CODE-010"), ("P059-TCL-037", "P059-CODE-013"), ("P059-TCL-048", "P059-CODE-002"),
    ("P059-TCL-050", "P059-CODE-007"), ("P059-TCL-053", "P059-CODE-007"),
    ("P059-TCL-055", "P059-CODE-002"), ("P059-TCL-155", "P059-CODE-002"), ("P059-TCL-060", "P059-CODE-010"),
    ("P059-TCL-066", "P059-CODE-004"), ("P059-TCL-066", "P059-CODE-006"),
    ("P059-TCL-069", "P059-CODE-001"), ("P059-TCL-069", "P059-CODE-004"), ("P059-TCL-069", "P059-CODE-005"),
    ("P059-TCL-069", "P059-CODE-006"), ("P059-TCL-069", "P059-CODE-008"),
    ("P059-TCL-073", "P059-CODE-009"), ("P059-TCL-073", "P059-CODE-013"),
    ("P059-TCL-081", "P059-CODE-009"), ("P059-TCL-081", "P059-CODE-010"), ("P059-TCL-081", "P059-CODE-013"),
    ("P059-TCL-083", "P059-CODE-009"),
    ("P059-TCL-113", "P059-CODE-001"), ("P059-TCL-113", "P059-CODE-004"), ("P059-TCL-113", "P059-CODE-005"),
    ("P059-TCL-113", "P059-CODE-006"), ("P059-TCL-113", "P059-CODE-008"),
    ("P059-TCL-157", "P059-CODE-007"), ("P059-TCL-159", "P059-CODE-009"),
    ("P059-TCL-164", "P059-CODE-009"), ("P059-TCL-164", "P059-CODE-010"), ("P059-TCL-164", "P059-CODE-013"),
    ("P059-TCL-172", "P059-CODE-002"), ("P059-TCL-172", "P059-CODE-003"), ("P059-TCL-172", "P059-CODE-007"),
    ("P059-TCL-172", "P059-CODE-009"), ("P059-TCL-172", "P059-CODE-010"), ("P059-TCL-172", "P059-CODE-013"),
    ("P059-TCL-173", "P059-CODE-002"), ("P059-TCL-173", "P059-CODE-003"), ("P059-TCL-173", "P059-CODE-007"),
    ("P059-TCL-173", "P059-CODE-009"), ("P059-TCL-173", "P059-CODE-010"), ("P059-TCL-173", "P059-CODE-013"),
    ("P059-TCL-179", "P059-CODE-007"), ("P059-TCL-179", "P059-CODE-009"), ("P059-TCL-179", "P059-CODE-010"), ("P059-TCL-179", "P059-CODE-013"),
    ("P059-TCL-182", "P059-CODE-007"), ("P059-TCL-182", "P059-CODE-009"), ("P059-TCL-182", "P059-CODE-010"), ("P059-TCL-182", "P059-CODE-013"),
}
ORACLE_CLAIM_PRIMARY_CONCEPT: dict[str, str] = {
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

ORACLE_DIRECT_REQUIREMENT_CLAIMS: dict[str, tuple[str, ...]] = {
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

ORACLE_DEPENDENCY_TARGET_CLAIMS: dict[str, tuple[str, ...]] = {
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

ORACLE_FINDING_ONTOLOGY_SCOPE: dict[str, dict[str, Any]] = {
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

def oracle_claim_ontology_scope(claim_id: str) -> dict[str, Any]:
    return {
        "primary_concept": ORACLE_CLAIM_PRIMARY_CONCEPT[claim_id],
        "direct_requirements": [concept for concept, members in ORACLE_DIRECT_REQUIREMENT_CLAIMS.items() if claim_id in members],
        "dependency_targets": [concept for concept, members in ORACLE_DEPENDENCY_TARGET_CLAIMS.items() if claim_id in members],
    }


ORACLE_ONTOLOGY_EDGES = [
    [scope["behavior"], concept]
    for scope in ORACLE_FINDING_ONTOLOGY_SCOPE.values()
    for concept in scope["violates"] + scope["emits"]
]


EXPECTED_STATUS = {
    "P059-TCL-001": "MISALIGNED", "P059-TCL-003": "MISALIGNED",
    "P059-TCL-005": "ABSENT", "P059-TCL-025": "MISALIGNED", "P059-TCL-026": "MISALIGNED",
    "P059-TCL-030": "MISALIGNED", "P059-TCL-033": "MISALIGNED", "P059-TCL-034": "MISALIGNED", "P059-TCL-039": "PARTIAL",
    "P059-TCL-056": "MISALIGNED", "P059-TCL-066": "MISALIGNED", "P059-TCL-069": "MISALIGNED",
    "P059-TCL-073": "MISALIGNED", "P059-TCL-083": "MISALIGNED",
    "P059-TCL-084": "ABSENT", "P059-TCL-100": "MISALIGNED", "P059-TCL-108": "MISALIGNED",
    "P059-TCL-113": "MISALIGNED", "P059-TCL-151": "MISALIGNED", "P059-TCL-153": "MISALIGNED",
    "P059-TCL-159": "PARTIAL", "P059-TCL-160": "PARTIAL", "P059-TCL-164": "MISALIGNED",
    "P059-TCL-165": "MISALIGNED", "P059-TCL-166": "PARTIAL", "P059-TCL-167": "PARTIAL",
    "P059-TCL-168": "MISALIGNED", "P059-TCL-169": "PARTIAL", "P059-TCL-176": "MISALIGNED",
}
EXPECTED_TEST: dict[str, list[str]] = {
    "P059-TCL-001": ["P059-TD-012", "UNT-001"], "P059-TCL-003": ["P059-TD-011", "P059-TD-012", "WID-004"],
    "P059-TCL-005": ["P059-TD-013", "LCO-003"], "P059-TCL-025": ["P059-TD-012", "KIN-001"],
    "P059-TCL-026": ["P059-TD-012", "ORD-002"], "P059-TCL-030": ["P059-TD-012", "CUR-001", "CUR-002", "MEM-002"],
    "P059-TCL-033": ["P059-TD-007", "P059-TD-013", "LCO-001"], "P059-TCL-034": ["P059-TD-007", "P059-TD-013", "LCO-001"],
    "P059-TCL-039": ["P059-TD-003", "P059-TD-009", "MEM-002"], "P059-TCL-056": ["P059-TD-007", "P059-TD-013", "LCO-001"],
    "P059-TCL-066": ["P059-TD-012", "KIN-001"], "P059-TCL-069": ["P059-TD-012", "ORD-002"],
    "P059-TCL-073": ["P059-TD-007", "P059-TD-013", "LCO-001"], "P059-TCL-081": ["P059-TD-007", "P059-TD-013", "LCO-001"],
    "P059-TCL-083": ["P059-TD-007", "P059-TD-013", "LCO-001"], "P059-TCL-084": ["P059-TD-013", "LCO-003"],
    "P059-TCL-100": ["P059-TD-007", "P059-TD-013", "LCO-001"], "P059-TCL-108": ["P059-TD-012", "UNT-001"],
    "P059-TCL-113": ["P059-TD-012", "ORD-002"], "P059-TCL-151": ["P059-TD-012", "UNT-001"],
    "P059-TCL-153": ["P059-TD-011", "P059-TD-012", "WID-004"],
    "P059-TCL-159": ["P059-TD-011", "VIB-001", "VIB-002", "VIB-004"], "P059-TCL-160": ["P059-TD-012", "VIB-003", "VIB-004"],
    "P059-TCL-164": ["P059-TD-011", "P059-TD-012", "WID-004"], "P059-TCL-165": ["P059-TD-011", "P059-TD-012", "WID-004"],
    "P059-TCL-166": ["P059-TD-011", "VIB-001", "VIB-002", "VIB-004"], "P059-TCL-167": ["P059-TD-011", "VIB-001", "VIB-002", "VIB-004"],
    "P059-TCL-168": ["P059-TD-011", "P059-TD-012", "WID-004"], "P059-TCL-169": ["P059-TD-011", "WID-002", "WID-004"],
    "P059-TCL-176": ["P059-TD-011", "P059-TD-012", "WID-004"], "P059-TCL-179": ["P059-TD-011", "P059-TD-012", "WID-004"],
}
EXPECTED_ARTIFACT: dict[str, list[str]] = {
    "P059-TCL-001": ["GOLD-005"], "P059-TCL-003": ["GOLD-005"],
    "P059-TCL-005": ["IMG-059-05"], "P059-TCL-025": ["GOLD-005"], "P059-TCL-026": ["GOLD-005"],
    "P059-TCL-030": ["GOLD-005"], "P059-TCL-033": ["GOLD-005", "IMG-059-05"],
    "P059-TCL-034": ["GOLD-005", "IMG-059-05"], "P059-TCL-039": ["GOLD-006"],
    "P059-TCL-056": ["GOLD-005", "IMG-059-05"], "P059-TCL-066": ["GOLD-005"],
    "P059-TCL-069": ["GOLD-005"], "P059-TCL-073": ["GOLD-005", "IMG-059-05"],
    "P059-TCL-081": ["GOLD-005", "IMG-059-05"], "P059-TCL-083": ["GOLD-005", "IMG-059-05"],
    "P059-TCL-084": ["GOLD-005", "IMG-059-05"], "P059-TCL-100": ["GOLD-005", "IMG-059-05"],
    "P059-TCL-108": ["GOLD-005"], "P059-TCL-113": ["GOLD-005"], "P059-TCL-151": ["GOLD-005"],
    "P059-TCL-153": ["GOLD-005"], "P059-TCL-159": ["GOLD-004", "GOLD-005"],
    "P059-TCL-160": ["GOLD-004", "GOLD-005"], "P059-TCL-164": ["GOLD-005"], "P059-TCL-165": ["GOLD-005"],
    "P059-TCL-166": ["GOLD-004", "GOLD-005"], "P059-TCL-167": ["GOLD-004", "GOLD-005"],
    "P059-TCL-168": ["GOLD-005"], "P059-TCL-169": ["GOLD-004", "GOLD-005"],
    "P059-TCL-176": ["GOLD-005"], "P059-TCL-179": ["GOLD-005"],
}
EXPECTED_BLOCKERS: dict[str, list[str]] = {
    "P059-TCL-001": ["RB-01"], "P059-TCL-003": ["RB-04", "NS-04"],
    "P059-TCL-005": ["NS-03", "ED-02"], "P059-TCL-025": ["RB-05", "P059-BD-NEW-005"],
    "P059-TCL-026": ["RB-01", "RB-06", "RB-08"], "P059-TCL-030": ["RB-01", "RB-05", "RB-06", "RB-08"],
    "P059-TCL-033": ["RB-09", "NS-03"], "P059-TCL-034": ["RB-09", "NS-03", "ED-02"],
    "P059-TCL-039": ["CF-03", "RB-07"], "P059-TCL-056": ["RB-09", "NS-03"],
    "P059-TCL-066": ["RB-05", "P059-BD-NEW-005"], "P059-TCL-069": ["RB-08"],
    "P059-TCL-073": ["RB-09", "NS-03"], "P059-TCL-081": ["RB-09", "NS-03"],
    "P059-TCL-083": ["RB-09", "NS-03"], "P059-TCL-084": ["NS-03", "ED-02"],
    "P059-TCL-100": ["RB-09", "NS-03"], "P059-TCL-108": ["RB-01"],
    "P059-TCL-113": ["RB-08"], "P059-TCL-151": ["RB-01"], "P059-TCL-153": ["RB-04", "RB-10"],
    "P059-TCL-159": ["RB-11", "P059-BD-NEW-001", "P059-BD-NEW-002"],
    "P059-TCL-160": ["RB-11", "P059-BD-NEW-001", "P059-BD-NEW-002"],
    "P059-TCL-164": ["RB-04", "RB-10"], "P059-TCL-165": ["RB-04", "RB-10"],
    "P059-TCL-166": ["RB-11", "P059-BD-NEW-001", "P059-BD-NEW-002"],
    "P059-TCL-167": ["RB-11", "P059-BD-NEW-001", "P059-BD-NEW-002"],
    "P059-TCL-168": ["RB-04", "RB-10"], "P059-TCL-169": ["RB-04", "NS-04"],
    "P059-TCL-176": ["RB-04", "RB-10"], "P059-TCL-179": ["RB-04", "RB-10"],
}
HIGH_RISK_EXPECTED: dict[str, dict[str, Any]] = {
    "P059-F4-HR-001": {"claims": ["P059-TCL-025", "P059-TCL-026", "P059-TCL-030", "P059-TCL-066"], "evidence": [("CODE", "P059-CODE-008"), ("TEST_RUNTIME", "MEM-002"), ("STORED_ARTIFACT", "IMG-059-05")]},
    "P059-F4-HR-002": {"claims": ["P059-TCL-026", "P059-TCL-030", "P059-TCL-069", "P059-TCL-113"], "evidence": [("CODE", "P059-CODE-002"), ("CODE", "P059-CODE-003"), ("TEST_RUNTIME", "P059-TD-012"), ("TEST_RUNTIME", "ORD-002")]},
    "P059-F4-HR-003": {"claims": ["P059-TCL-026", "P059-TCL-030"], "evidence": [("CODE", "P059-CODE-004"), ("TEST_RUNTIME", "P059-TD-012"), ("TEST_RUNTIME", "CUR-002")]},
    "P059-F4-HR-004": {"claims": ["P059-TCL-001", "P059-TCL-026", "P059-TCL-030", "P059-TCL-108", "P059-TCL-151"], "evidence": [("CODE", "P059-CODE-006"), ("TEST_RUNTIME", "P059-TD-012"), ("TEST_RUNTIME", "UNT-001")]},
    "P059-F4-HR-005": {"claims": ["P059-TCL-003", "P059-TCL-153", "P059-TCL-164", "P059-TCL-165", "P059-TCL-168", "P059-TCL-169", "P059-TCL-176", "P059-TCL-179"], "evidence": [("CODE", "P059-CODE-007"), ("TEST_RUNTIME", "P059-TD-011"), ("TEST_RUNTIME", "P059-TD-012"), ("TEST_RUNTIME", "WID-004")]},
    "P059-F4-HR-006": {"claims": ["P059-TCL-005", "P059-TCL-033", "P059-TCL-034", "P059-TCL-056", "P059-TCL-073", "P059-TCL-081", "P059-TCL-083", "P059-TCL-084", "P059-TCL-100"], "evidence": [("CODE", "P059-CODE-010"), ("CODE", "P059-CODE-011"), ("TEST_RUNTIME", "P059-TD-007"), ("TEST_RUNTIME", "P059-TD-013"), ("TEST_RUNTIME", "LCO-001"), ("TEST_RUNTIME", "LCO-003"), ("STORED_ARTIFACT", "IMG-059-05")]},
    "P059-F4-HR-007": {"claims": ["P059-TCL-073", "P059-TCL-083", "P059-TCL-159", "P059-TCL-160", "P059-TCL-166", "P059-TCL-167"], "evidence": [("CODE", "P059-CODE-009"), ("CODE", "P059-CODE-013"), ("TEST_RUNTIME", "P059-TD-011"), ("TEST_RUNTIME", "P059-TD-012"), ("TEST_RUNTIME", "VIB-003"), ("TEST_RUNTIME", "VIB-004"), ("STORED_ARTIFACT", "GOLD-004"), ("STORED_ARTIFACT", "GOLD-005")]},
    "P059-F4-HR-008": {"claims": [], "evidence": [("TEST_RUNTIME", "P059-TD-013"), ("STORED_ARTIFACT", "IMG-059-05")]},
    "P059-F4-HR-009": {"claims": [], "evidence": [("TEST_RUNTIME", "P059-TD-013"), ("STORED_ARTIFACT", "GOLD-005")]},
    "P059-F4-HR-010": {"claims": [], "evidence": [("TEST_RUNTIME", "P059-TD-004"), ("TEST_RUNTIME", "P059-TD-005"), ("TEST_RUNTIME", "P059-TD-015"), ("STORED_ARTIFACT", "GOLD-003"), ("STORED_ARTIFACT", "GOLD-006")]},
    "P059-F4-HR-011": {"claims": [], "evidence": [("STORED_ARTIFACT", "PDF-059-03"), ("STORED_ARTIFACT", "IMG-059-03"), ("STORED_ARTIFACT", "P059-ART-GENE-PDF-OCC-007"), ("STORED_ARTIFACT", "P059-ART-GENE-IMAGE-OCC-015")]},
}

EXPECTED_CODE_SEMANTIC_SHA256 = "d2a27f8146251e1b2ff8287b06a2ad9a978b2b237babcffed929aaccda019f59"
EXPECTED_TEST_SEMANTIC_SHA256 = "463fd04d77005b361aa6fe23b8212fdfa7e6746c241e4c14f030c2c335c14f49"
EXPECTED_MAIN_SEMANTIC_SHA256 = "05c01c27056de951e724ded7ef9f4a123726f240279cf324cd243cea867d5852"


class ValidationFailure(RuntimeError):
    pass


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


def expected_semantic_ontology_ref() -> dict[str, Any]:
    return {
        "ontology_id": SEMANTIC_ONTOLOGY_ID,
        "directed_edge_count": len(ORACLE_ONTOLOGY_EDGES),
        "directed_edges_sha256": object_sha256(ORACLE_ONTOLOGY_EDGES),
    }


def certificate_basis_from_certificate(certificate: dict[str, Any]) -> dict[str, Any]:
    return {field: certificate[field] for field in CERTIFICATE_BASIS_FIELDS}


def expected_review_check_manifest(
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
    if PurePosixPath(path).as_posix() != path or "\\" in path:
        raise ValidationFailure(f"non-POSIX path: {path}")
    run = subprocess.run(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if run.returncode:
        raise ValidationFailure(f"missing baseline Git blob: {path}")
    return run.stdout


def load_source(path: str) -> Any:
    return json.loads(git_blob(path).decode("utf-8"))


def recursive_node_count(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + sum(recursive_node_count(v) for v in value.values())
    if isinstance(value, list):
        return 1 + sum(recursive_node_count(v) for v in value)
    return 1


def expected_input_coverage() -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_PATHS:
        blob = git_blob(path)
        text = blob.decode("utf-8")
        is_json = path.endswith(".json")
        parsed = json.loads(text) if is_json else None
        rows.append({"path": path, "line_count": len(text.splitlines()), "read_range": f"1-{len(text.splitlines())}", "parse_mode": "FULL_JSON_RECURSIVE" if is_json else "FULL_TEXT_1_TO_EOF", "recursive_node_count": recursive_node_count(parsed) if is_json else None, "git_blob_sha256": hashlib.sha256(blob).hexdigest(), "hash_basis": f"Git blob bytes at {BASELINE}"})
    return rows


def input_corpus_sha256(rows: list[dict[str, Any]]) -> str:
    return object_sha256(rows)


def semantic_sha256(document: dict[str, Any]) -> str:
    candidate = copy.deepcopy(document)
    candidate["determinism"]["semantic_sha256"] = ""
    return object_sha256(candidate)


def seal(document: dict[str, Any]) -> None:
    document["determinism"]["semantic_sha256"] = ""
    document["determinism"]["semantic_sha256"] = semantic_sha256(document)


def canonical_record(record_id: str, kind: str, evidence_class: str, path: str, field: str, idx: int, original: Any) -> dict[str, Any]:
    return {"record_id": record_id, "record_kind": kind, "evidence_class": evidence_class, "source_artifact_path": path, "source_field": field, "source_index": idx, "original_record": original, "original_record_sha256": object_sha256(original)}


def expected_code_records() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    index, diff = load_source(INPUT_PATHS[3]), load_source(INPUT_PATHS[4])
    records = []
    for idx, item in enumerate(index["modules"]): records.append(canonical_record(f"P059-CODE-MODULE-{idx + 1:03d}", "PRODUCTION_MODULE", "CODE", INPUT_PATHS[3], "modules", idx, item))
    for idx, item in enumerate(index["review"]["findings"]): records.append(canonical_record(item["id"], "PRODUCTION_FINDING", "CODE", INPUT_PATHS[3], "review.findings", idx, item))
    for idx, item in enumerate(diff["comparisons"]): records.append(canonical_record(f"P059-CODE-DIFF-{idx + 1:03d}", "PRODUCTION_DIFF", "CODE", INPUT_PATHS[4], "comparisons", idx, item))
    for idx, item in enumerate(diff["copy_forward"]): records.append(canonical_record(f"P059-CODE-COPY-{idx + 1:03d}", "PRODUCTION_COPY_FORWARD", "CODE", INPUT_PATHS[4], "copy_forward", idx, item))
    return records, {"production_code_index": index, "production_code_diff": diff}


def expected_test_and_artifact_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    matrix, runtime, probes = load_source(INPUT_PATHS[6]), load_source(INPUT_PATHS[8]), load_source(INPUT_PATHS[10])
    golden, genealogy, pdf, image = load_source(INPUT_PATHS[12]), load_source(INPUT_PATHS[14]), load_source(INPUT_PATHS[16]), load_source(INPUT_PATHS[18])
    tests: list[dict[str, Any]] = []
    artifacts: list[dict[str, Any]] = []
    for idx, item in enumerate(matrix["records"]): tests.append(canonical_record(f"P059-TD-SOURCE-{idx + 1:03d}", "TEST_DEMO_SOURCE", "TEST_RUNTIME", INPUT_PATHS[6], "records", idx, item))
    for idx, item in enumerate(matrix["findings"]): tests.append(canonical_record(item["id"], "TEST_DEMO_FINDING", "TEST_RUNTIME", INPUT_PATHS[6], "findings", idx, item))
    for idx, item in enumerate(runtime["runs"]): tests.append(canonical_record(f"P059-RUNTIME-{idx + 1:03d}", "ISOLATED_RUNTIME_RUN", "TEST_RUNTIME", INPUT_PATHS[8], "runs", idx, item))
    for idx, item in enumerate(probes["probes"]): tests.append(canonical_record(item["probe_id"], "INDEPENDENT_PROBE", "TEST_RUNTIME", INPUT_PATHS[10], "probes", idx, item))
    for idx, item in enumerate(golden["findings"]): artifacts.append(canonical_record(item["finding_id"], "GOLDEN_FINDING", "STORED_ARTIFACT", INPUT_PATHS[12], "findings", idx, item))
    genealogy_specs = [
        ("pdf_occurrences", "P059-ART-GENE-PDF-OCC", "GENEALOGY_PDF_OCCURRENCE"),
        ("pdf_byte_content_groups", "P059-ART-GENE-PDF-BYTE-GROUP", "GENEALOGY_PDF_BYTE_GROUP"),
        ("pdf_rendered_content_groups", "P059-ART-GENE-PDF-RENDER-GROUP", "GENEALOGY_PDF_RENDER_GROUP"),
        ("image_occurrences", "P059-ART-GENE-IMAGE-OCC", "GENEALOGY_IMAGE_OCCURRENCE"),
        ("image_content_groups", "P059-ART-GENE-IMAGE-GROUP", "GENEALOGY_IMAGE_GROUP"),
        ("golden_occurrences", "P059-ART-GENE-GOLD-OCC", "GENEALOGY_GOLDEN_OCCURRENCE"),
        ("golden_content_groups", "P059-ART-GENE-GOLD-GROUP", "GENEALOGY_GOLDEN_GROUP"),
    ]
    for field, prefix, kind in genealogy_specs:
        for idx, item in enumerate(genealogy[field]): artifacts.append(canonical_record(f"{prefix}-{idx + 1:03d}", kind, "STORED_ARTIFACT", INPUT_PATHS[14], field, idx, item))
    for idx, item in enumerate(pdf["documents"]): artifacts.append(canonical_record(f"P059-ART-PDF-DOC-{idx + 1:03d}", "PDF_VISUAL_DOCUMENT", "STORED_ARTIFACT", INPUT_PATHS[16], "documents", idx, item))
    for idx, item in enumerate(pdf["full_resolution_targets"]): artifacts.append(canonical_record(f"P059-ART-PDF-TARGET-{idx + 1:03d}", "PDF_VISUAL_TARGET", "STORED_ARTIFACT", INPUT_PATHS[16], "full_resolution_targets", idx, item))
    for idx, item in enumerate(pdf["findings"]): artifacts.append(canonical_record(item["id"], "PDF_VISUAL_FINDING", "STORED_ARTIFACT", INPUT_PATHS[16], "findings", idx, item))
    for idx, item in enumerate(image["images"]): artifacts.append(canonical_record(f"P059-ART-IMAGE-{idx + 1:03d}", "IMAGE_AUDIT_IMAGE", "STORED_ARTIFACT", INPUT_PATHS[18], "images", idx, item))
    for idx, item in enumerate(image["findings"]): artifacts.append(canonical_record(item["id"], "IMAGE_AUDIT_FINDING", "STORED_ARTIFACT", INPUT_PATHS[18], "findings", idx, item))
    snapshots = {"test_runtime": {"test_demo_assertion_matrix": matrix, "isolated_runtime_results": runtime, "independent_code_probes": probes}, "stored_artifact": {"golden_npz_audit": golden, "artifact_genealogy": genealogy, "pdf_visual_review": pdf, "image_audit": image}}
    return tests, artifacts, snapshots


def validate_source_line_evidence(record: dict[str, Any]) -> None:
    for evidence in record["original_record"].get("source_evidence", []):
        lines = git_blob(evidence["path"]).decode("utf-8").splitlines()
        line = evidence["line"]
        if not isinstance(line, int) or not 1 <= line <= len(lines): raise ValidationFailure(f"{record['record_id']} invalid source line")
        actual = lines[line - 1]
        if actual != evidence["source_line"] or evidence["needle"] not in actual: raise ValidationFailure(f"{record['record_id']} source line/needle mismatch")


def validate_occurrence_blob(record: dict[str, Any]) -> None:
    original = record["original_record"]
    path, sha = original.get("path") or original.get("representative_path"), original.get("sha256")
    if path and sha and (record["record_kind"].endswith("OCCURRENCE") or record["record_kind"] in {"PDF_VISUAL_DOCUMENT", "IMAGE_AUDIT_IMAGE"}):
        if hashlib.sha256(git_blob(path)).hexdigest() != sha: raise ValidationFailure(f"{record['record_id']} stored artifact blob hash mismatch")


def validate_common(document: dict[str, Any], expected_status: str, semantic_lock: str) -> None:
    if document.get("baseline_commit") != BASELINE: raise ValidationFailure("baseline_commit mismatch")
    if document.get("status") != expected_status: raise ValidationFailure("status mismatch")
    coverage = expected_input_coverage()
    if document.get("input_coverage") != coverage: raise ValidationFailure("input coverage ordered path/hash/line/parse contract mismatch")
    if document.get("input_corpus_sha256") != input_corpus_sha256(coverage): raise ValidationFailure("input corpus SHA-256 mismatch")
    actual_semantic = semantic_sha256(document)
    if document.get("determinism", {}).get("semantic_sha256") != actual_semantic: raise ValidationFailure("semantic SHA-256 self-check mismatch")
    if not semantic_lock: raise ValidationFailure("validator semantic lock is not frozen")
    if actual_semantic != semantic_lock: raise ValidationFailure("frozen canonical semantic SHA-256 lock mismatch")


def validate_review_completeness(code: dict[str, Any], test: dict[str, Any], main: dict[str, Any]) -> None:
    failures = []
    builder_text = (ROOT / BUILDER_PATH).read_text(encoding="utf-8")
    if "import validate_phase059_four_axis_conformance" in builder_text: failures.append("P1-3 builder imports validator substantive truth")
    # SIXTH review RED: pair membership or the absence of a pair-ID bridge must
    # never be the scientific decision oracle.  This source check deliberately
    # runs before the semantic lock so a resealed complement table is rejected.
    if "NA_CODE_MEMBERSHIP" in builder_text:
        failures.append("P1-SIXTH complement hardcoding: builder contains NA_CODE_MEMBERSHIP")
    if "CROSS_DOMAIN_BRIDGE_KIND.get(pair" in builder_text:
        failures.append("P1-SIXTH result hardcoding: pair-ID bridge presence determines traversal")
    ledger = main.get("applicable_claim_code_adjudications")
    if not isinstance(ledger, list) or len(ledger) != 51: failures.append("P1-1 missing 51-claim direct-code adjudication ledger")
    ledger_by_claim = {entry.get("claim_id"): entry for entry in ledger or [] if isinstance(entry, dict)}
    for claim_id, code_id, expected in [
        ("P059-TCL-073", "P059-CODE-013", "RELATED_NOT_DIRECT"),
        ("P059-TCL-081", "P059-CODE-010", "RELATED_NOT_DIRECT"),
        ("P059-TCL-179", "P059-CODE-007", "RELATED_NOT_DIRECT"),
        ("P059-TCL-037", "P059-CODE-013", "RELATED_NOT_DIRECT"),
        ("P059-TCL-069", "P059-CODE-005", "RELATED_NOT_DIRECT"),
        ("P059-TCL-113", "P059-CODE-005", "RELATED_NOT_DIRECT"),
        ("P059-TCL-155", "P059-CODE-002", "RELATED_NOT_DIRECT"),
        ("P059-TCL-172", "P059-CODE-003", "RELATED_NOT_DIRECT"),
        ("P059-TCL-173", "P059-CODE-003", "RELATED_NOT_DIRECT"),
        ("P059-TCL-034", "P059-CODE-009", "RELATED_NOT_DIRECT"),
        ("P059-TCL-037", "P059-CODE-009", "RELATED_NOT_DIRECT"),
        ("P059-TCL-073", "P059-CODE-009", "RELATED_NOT_DIRECT"),
        ("P059-TCL-081", "P059-CODE-009", "RELATED_NOT_DIRECT"),
        ("P059-TCL-083", "P059-CODE-009", "RELATED_NOT_DIRECT"),
        ("P059-TCL-164", "P059-CODE-009", "RELATED_NOT_DIRECT"),
        ("P059-TCL-172", "P059-CODE-009", "RELATED_NOT_DIRECT"),
        ("P059-TCL-173", "P059-CODE-009", "RELATED_NOT_DIRECT"),
        ("P059-TCL-179", "P059-CODE-009", "RELATED_NOT_DIRECT"),
        ("P059-TCL-182", "P059-CODE-009", "RELATED_NOT_DIRECT"),
        ("P059-TCL-172", "P059-CODE-010", "RELATED_NOT_DIRECT"),
        ("P059-TCL-173", "P059-CODE-010", "RELATED_NOT_DIRECT"),
        ("P059-TCL-172", "P059-CODE-013", "RELATED_NOT_DIRECT"),
        ("P059-TCL-173", "P059-CODE-013", "RELATED_NOT_DIRECT"),
    ]:
        decision = next((item for item in ledger_by_claim.get(claim_id, {}).get("code_finding_adjudications", []) if item.get("code_finding_id") == code_id), {})
        if decision.get("applicability") != expected:
            failures.append(f"P1-1 semantic correction requires {claim_id}<->{code_id}={expected}")
    if any("comparison" not in item for entry in ledger or [] for item in entry.get("code_finding_adjudications", [])):
        failures.append("P1-2 missing structured pair comparison substance")
    if any("claim_quantity_or_dependency" not in entry.get("claim_semantic_scope", {}) for entry in ledger or []):
        failures.append("P1-2 missing substantive claim semantic scope")
    code_scopes = main.get("semantic_cross_audit", {}).get("code_finding_semantic_scopes", [])
    if any("actual_production_behavior" not in scope for scope in code_scopes):
        failures.append("P1-2 missing substantive finding semantic scope")
    na_decisions = [
        item
        for entry in ledger or []
        for item in entry.get("code_finding_adjudications", [])
        if item.get("applicability") == "NOT_APPLICABLE"
    ]
    legacy_signatures = {
        (
            item.get("comparison", {}).get("overlap_or_dependency_path", "").startswith("NO SOURCE-GROUNDED PATH:"),
            "Those anchors identify neither a shared executed/contradicted quantity nor an upstream/downstream dependency"
            in item.get("comparison", {}).get("classification_reason", ""),
            item.get("comparison", {}).get("exclusion_boundary", "").startswith("Do not use this finding to adjudicate"),
        )
        for item in na_decisions
    }
    if len(na_decisions) == 575 and legacy_signatures == {(True, True, True)}:
        failures.append("P1-NA all 575 NOT_APPLICABLE decisions share one legacy structural template signature")
    na_groundings = main.get("semantic_cross_audit", {}).get("na_pair_groundings")
    if not isinstance(na_groundings, list) or len(na_groundings) != 558:
        failures.append("P1-NA missing 558-entry pair-level semantic grounding ledger/oracle")
    if any("na_pair_grounding_id" not in item for item in na_decisions):
        failures.append("P1-NA decisions do not reverse-link pair-specific groundings")
    cross_audit = main.get("semantic_cross_audit", {})
    if not isinstance(cross_audit.get("semantic_concept_ontology"), dict):
        failures.append("P1-SIXTH source-grounded semantic concept ontology is absent")
    if na_groundings and any("nonconnection_certificate" not in grounding for grounding in na_groundings):
        failures.append("P1-SIXTH machine-auditable exact-pair nonconnection certificate is absent")
    normalization = cross_audit.get("na_normalization_audit", {})
    for key in ("distinct_semantic_proof_structure_count", "distinct_normalized_rationale_structure_count", "distinct_normalized_exclusion_structure_count"):
        if normalization.get(key) != 558:
            failures.append(f"P1-SIXTH normalized semantic diversity is not 558/558: {key}={normalization.get(key)}")
    legacy_rationale_phrase = "Executable pair traversal found intersection="
    legacy_exclusion_phrase = "This pair-specific exclusion is bounded to"
    if len(na_groundings or []) == 558 and all(legacy_rationale_phrase in grounding.get("conclusion_specific_rationale", "") for grounding in na_groundings):
        failures.append("P1-SIXTH normalized rationale skeleton is shared by all 558 NA pairs")
    if len(na_groundings or []) == 558 and all(legacy_exclusion_phrase in grounding.get("exclusion_boundary", "") for grounding in na_groundings):
        failures.append("P1-SIXTH normalized exclusion skeleton is shared by all 558 NA pairs")
    tcl155_code002 = next((item for item in ledger_by_claim.get("P059-TCL-155", {}).get("code_finding_adjudications", []) if item.get("code_finding_id") == "P059-CODE-002"), {})
    if tcl155_code002.get("applicability") != "RELATED_NOT_DIRECT":
        failures.append("P1-graph TCL155<->CODE002 chronology bridge is misclassified as NOT_APPLICABLE")
    if na_decisions and all(
        item.get("pair_graph_audit") is None
        and grounding.get("executed_quantity_intersection", {}).get("result") == "NONE"
        and grounding.get("dependency_reachability", {}).get("result") == "NONE"
        and grounding.get("contradiction_finding", {}).get("result") == "NONE"
        for item, grounding in zip(na_decisions, na_groundings or [])
    ):
        failures.append("P1-graph all NA NONE results are stored without executable pair graph traversal")
    if not main.get("semantic_cross_audit", {}).get("cross_domain_bridge_oracle"):
        failures.append("P1-graph missing source-grounded cross-domain bridge oracle")
    exact_substance_count = 0
    scopes = {entry.get("claim_id"): entry.get("claim_semantic_scope", {}) for entry in ledger or []}
    finding_scopes = {scope.get("code_finding_id"): scope for scope in code_scopes}
    for grounding in na_groundings or []:
        claim_scope = scopes.get(grounding.get("claim_id"), {})
        finding_scope = finding_scopes.get(grounding.get("code_finding_id"), {})
        rationale = grounding.get("conclusion_specific_rationale", "")
        required_texts = [
            claim_scope.get("claim_quantity_or_dependency", ""), claim_scope.get("dependency_direction", ""), claim_scope.get("non_goal", ""),
            finding_scope.get("actual_production_behavior", ""), finding_scope.get("finding_affected_quantity_or_path", ""), finding_scope.get("non_adjudicated_quantities", ""),
        ]
        if all(text and text in rationale for text in required_texts):
            exact_substance_count += 1
    if len(na_groundings or []) == 558 and exact_substance_count != 558:
        failures.append(f"P1-NA exact claim/finding semantic substance appears in {exact_substance_count}/558 rationales")
    if any(
        "structural_signature_basis" not in grounding
        or any(field not in grounding.get("nonconnection_certificate", {}) for field in CERTIFICATE_BASIS_FIELDS)
        for grounding in na_groundings or []
    ):
        failures.append("P1-signature structural/certificate signature basis is absent and cannot be recomputed")
    rows = {x.get("claim_id"): x for x in main.get("rows", [])}
    for claim_id, code_id in [
        ("P059-TCL-084", "P059-CODE-011"),
        ("P059-TCL-030", "P059-CODE-006"),
        ("P059-TCL-033", "P059-CODE-010"),
        ("P059-TCL-056", "P059-CODE-010"),
        ("P059-TCL-066", "P059-CODE-005"),
    ]:
        links = rows.get(claim_id, {}).get("production_axis", {}).get("evidence_links", [])
        if code_id not in [x.get("evidence_id") for x in links]: failures.append(f"P1-1 missing direct link {claim_id}<->{code_id}")
    lco = next((x for x in main.get("high_risk_findings", []) if x.get("finding_id") == "P059-F4-HR-006"), {})
    missing_lco = [claim_id for claim_id in ("P059-TCL-033", "P059-TCL-056", "P059-TCL-081", "P059-TCL-084") if claim_id not in lco.get("claim_ids", [])]
    if missing_lco: failures.append("P1-1 LCO high-risk omits " + ",".join(missing_lco))
    if not isinstance(test.get("artifact_records"), list): failures.append("P1-2 missing canonical stored-artifact record universe")
    if any("evidence_ids" in finding for finding in main.get("high_risk_findings", [])): failures.append("P1-2 high-risk evidence uses bare IDs instead of anchored links")
    if failures: raise ValidationFailure("review completeness RED: " + "; ".join(failures))


def validate_code(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    expected, snapshots = expected_code_records()
    if document.get("source_snapshots") != snapshots or document.get("records") != expected: raise ValidationFailure("canonical code records/snapshots mismatch")
    ids = [x["record_id"] for x in expected]
    if len(ids) != len(set(ids)): raise ValidationFailure("canonical code record IDs are not unique")
    counts = Counter(x["record_kind"] for x in expected)
    expected_counts = {"production_modules": counts["PRODUCTION_MODULE"], "production_findings": counts["PRODUCTION_FINDING"], "production_diffs": counts["PRODUCTION_DIFF"], "production_copy_forward": counts["PRODUCTION_COPY_FORWARD"], "canonical_records": len(expected), "invalid_source_anchors": 0}
    if document.get("counts") != expected_counts: raise ValidationFailure("code count reconciliation mismatch")
    for record in expected:
        validate_source_line_evidence(record)
        if record["record_kind"] == "PRODUCTION_MODULE":
            original = record["original_record"]
            blob = git_blob(original["representative_path"])
            if hashlib.sha256(blob).hexdigest() != original["sha256"] or len(blob.decode("utf-8").splitlines()) != original["line_count"]: raise ValidationFailure(f"{record['record_id']} production source hash/line mismatch")
    validate_common(document, "PASS_P059_CODE_BEHAVIOR_MATRIX", EXPECTED_CODE_SEMANTIC_SHA256)
    return {x["record_id"]: x for x in expected}


def validate_test(document: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    tests, artifacts, snapshots = expected_test_and_artifact_records()
    if document.get("source_snapshots") != snapshots: raise ValidationFailure("test/artifact source snapshots are lossy or tampered")
    if document.get("test_runtime_records") != tests: raise ValidationFailure("canonical test/runtime records mismatch")
    if document.get("artifact_records") != artifacts: raise ValidationFailure("canonical stored-artifact records mismatch")
    all_ids = [x["record_id"] for x in tests + artifacts]
    if len(all_ids) != len(set(all_ids)): raise ValidationFailure("test/artifact canonical record IDs are not unique")
    tc = Counter(x["record_kind"] for x in tests)
    ac = Counter(x["record_kind"] for x in artifacts)
    expected_counts = {
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
    if document.get("counts") != expected_counts: raise ValidationFailure("test/artifact count reconciliation mismatch")
    for record in tests + artifacts:
        validate_source_line_evidence(record); validate_occurrence_blob(record)
        if record["record_kind"] == "TEST_DEMO_SOURCE":
            original = record["original_record"]; blob = git_blob(original["representative_path"])
            if hashlib.sha256(blob).hexdigest() != original["sha256"] or len(blob.decode("utf-8").splitlines()) != original["line_count"]: raise ValidationFailure(f"{record['record_id']} test source hash/line mismatch")
    validate_common(document, "PASS_P059_TEST_DEMO_CLAIM_MATRIX", EXPECTED_TEST_SEMANTIC_SHA256)
    return ({x["record_id"]: x for x in tests}, {x["record_id"]: x for x in artifacts})


def link_ids(axis: dict[str, Any]) -> list[str]:
    return [x["evidence_id"] for x in axis["evidence_links"]]


def expected_link_basis(source: dict[str, Any]) -> str:
    original = source["original_record"]
    return (
        original.get("claim")
        or original.get("interpretation")
        or original.get("title")
        or f"Exact frozen {source['record_kind']} record at "
        f"{source['source_field']}[{source['source_index']}]."
    )


def validate_link(
    link: Any,
    expected_class: str,
    universe: dict[str, dict[str, Any]],
    expected_role: str,
) -> None:
    if not isinstance(link, dict) or set(link) != LINK_KEYS: raise ValidationFailure(f"{expected_class} evidence-link schema mismatch")
    evidence_id = link["evidence_id"]
    if evidence_id not in universe: raise ValidationFailure(f"{expected_class} invalid evidence ID")
    source = universe[evidence_id]
    if link["evidence_class"] != expected_class or source["evidence_class"] != expected_class: raise ValidationFailure(f"{expected_class} evidence class mismatch")
    if link["source_artifact_path"] != source["source_artifact_path"] or link["source_field"] != source["source_field"] or link["source_index"] != source["source_index"]: raise ValidationFailure(f"{expected_class} evidence source anchor mismatch")
    if link["source_record_sha256"] != source["original_record_sha256"]: raise ValidationFailure(f"{expected_class} evidence record hash mismatch")
    expected_metadata = {
        "matrix_path": LINK_MATRIX_PATH_BY_CLASS[expected_class],
        "role": expected_role,
        "basis": expected_link_basis(source),
    }
    actual_metadata = {key: link[key] for key in expected_metadata}
    if actual_metadata != expected_metadata:
        raise ValidationFailure(f"{expected_class} evidence role/basis/path exact reconstruction mismatch")


def validate_axis(axis: Any, expected_axis: str, expected_class: str, universe: dict[str, dict[str, Any]]) -> None:
    if not isinstance(axis, dict) or set(axis) != AXIS_KEYS: raise ValidationFailure(f"{expected_axis} axis schema mismatch")
    if axis["axis"] != expected_axis or not axis["boundary"].strip(): raise ValidationFailure(f"{expected_axis} axis identity/boundary mismatch")
    links = axis["evidence_links"]
    if axis["state"] not in {"PRESENT", "NO_DIRECT_EVIDENCE"} or (axis["state"] == "PRESENT") != bool(links): raise ValidationFailure(f"{expected_axis} state/evidence mismatch")
    ids = []
    for link in links:
        validate_link(link, expected_class, universe, AXIS_ROLE_BY_CLASS[expected_class])
        ids.append(link["evidence_id"])
    if len(ids) != len(set(ids)): raise ValidationFailure(f"{expected_axis} duplicate evidence link")


def claim_contract_relation_ids(claim: dict[str, Any], contract_ids: list[str]) -> list[str]:
    relations = []
    for evidence in claim["applicable_contract_evidence"]:
        if evidence["contract_id"] in contract_ids: relations.extend(evidence["direct_claim_relation_ids"])
    return list(dict.fromkeys(relations))


def expected_claim_semantic_scope(claim: dict[str, Any]) -> dict[str, Any]:
    topics = sorted({evidence["topic"] for evidence in claim["applicable_contract_evidence"]})
    actions = list(dict.fromkeys(evidence["required_action"] for evidence in claim["applicable_contract_evidence"]))
    anchors = claim["source_anchors"]
    if not anchors:
        anchors = [
            source
            for evidence in claim["applicable_contract_evidence"]
            for source in evidence["all_contract_evidence"]
        ]
    refs: list[dict[str, Any]] = []
    for anchor in anchors:
        ref = {
            "path": anchor["path"],
            "line_start": anchor["line_start"],
            "line_end": anchor["line_end"],
            "label": anchor.get("label") or ",".join(anchor.get("labels", [])) or None,
            "source_excerpt_sha256": hashlib.sha256(anchor["source_excerpt"].encode("utf-8")).hexdigest(),
        }
        if ref not in refs:
            refs.append(ref)
    return {
        "claim_id": claim["claim_id"],
        "claim_kind": claim["claim_kind"],
        "family": claim["family"],
        "labels": claim["labels"],
        "contract_topics": topics,
        "required_actions": actions,
        "derivation_status": claim["derivation_audit"]["status"],
        "code_impact_assessment": claim["code_impact"]["assessment"],
        "source_anchor_refs": refs,
        "source_relation_texts": list(dict.fromkeys(anchor["source_excerpt"] for anchor in anchors)),
        "required_evidence_or_action": actions,
        "semantic_concepts": oracle_claim_ontology_scope(claim["claim_id"]),
    }


def expected_code_semantic_scope(finding: dict[str, Any]) -> dict[str, Any]:
    return {
        "code_finding_id": finding["id"],
        "title": finding["title"],
        "claim": finding["claim"],
        "consequence": finding["consequence"],
        "required_action": finding["required_action"],
        "contract_ids": finding["contract_ids"],
        "source_evidence": finding["source_evidence"],
        "actual_production_behavior": finding["claim"],
        "semantic_concepts": {
            "behavior": ORACLE_FINDING_ONTOLOGY_SCOPE[finding["id"]]["behavior"],
            "violates": list(ORACLE_FINDING_ONTOLOGY_SCOPE[finding["id"]]["violates"]),
            "emits": list(ORACLE_FINDING_ONTOLOGY_SCOPE[finding["id"]]["emits"]),
        },
    }


def validator_directed_path(edges: list[list[str]], source: str, target: str) -> list[str]:
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


def validator_reachable_nodes(edges: list[list[str]], source: str) -> list[str]:
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


def validate_pair_graph_audit(graph: Any, claim_scope: dict[str, Any], code_scope: dict[str, Any]) -> str:
    claim_id, code_id = claim_scope["claim_id"], code_scope["code_finding_id"]
    pair_id = f"{claim_id}->{code_id}"
    if not isinstance(graph, dict) or set(graph) != PAIR_GRAPH_AUDIT_KEYS:
        raise ValidationFailure(f"{pair_id} pair graph schema mismatch")
    if graph["pair_graph_audit_id"] != f"P059-PAIR-GRAPH-{claim_id[-3:]}-{code_id[-3:]}" or graph["pair_id"] != pair_id:
        raise ValidationFailure(f"{pair_id} pair graph identity mismatch")
    if graph["classification_derivation"] != "ONTOLOGY_INTERSECTION_CONTRADICTION_AND_DIRECTED_REACHABILITY":
        raise ValidationFailure(f"{pair_id} classification is hardcoded instead of ontology-derived")
    claim_concepts = oracle_claim_ontology_scope(claim_id)
    finding_concepts = ORACLE_FINDING_ONTOLOGY_SCOPE[code_id]
    direct_matches = sorted(set(claim_concepts["direct_requirements"]) & set(finding_concepts["violates"]))
    dependency_paths = [validator_directed_path(ORACLE_ONTOLOGY_EDGES, finding_concepts["behavior"], target) for target in claim_concepts["dependency_targets"]]
    dependency_paths = [path for path in dependency_paths if path]
    if direct_matches:
        expected_class, bridge_kind = "DIRECT", "DIRECT_CONTRADICTION"
        bridge_path, matched = [finding_concepts["behavior"], direct_matches[0]], direct_matches[0]
    elif dependency_paths:
        expected_class, bridge_kind = "RELATED_NOT_DIRECT", "RELATED_DEPENDENCY"
        bridge_path, matched = dependency_paths[0], dependency_paths[0][-1]
    else:
        expected_class, bridge_kind, bridge_path, matched = "NOT_APPLICABLE", "", [], None
    expected_claim_nodes = [claim_concepts["primary_concept"]] + claim_concepts["direct_requirements"] + claim_concepts["dependency_targets"]
    expected_claim_edges = [[claim_concepts["primary_concept"], concept] for concept in claim_concepts["direct_requirements"] + claim_concepts["dependency_targets"] if concept != claim_concepts["primary_concept"]]
    expected_finding_nodes = [finding_concepts["behavior"]] + list(finding_concepts["violates"]) + list(finding_concepts["emits"])
    expected_finding_edges = [edge for edge in ORACLE_ONTOLOGY_EDGES if edge[0] == finding_concepts["behavior"]]
    if graph["claim_graph"] != {"nodes": expected_claim_nodes, "directed_edges": expected_claim_edges, "executed_quantity_nodes": claim_concepts["direct_requirements"]}:
        raise ValidationFailure(f"{pair_id} claim concept graph mismatch")
    if graph["finding_graph"] != {"nodes": expected_finding_nodes, "directed_edges": expected_finding_edges, "executed_quantity_nodes": list(finding_concepts["violates"])}:
        raise ValidationFailure(f"{pair_id} finding concept graph mismatch")
    contradiction_evidence = [{"scientific_requirement": concept, "finding_behavior": finding_concepts["behavior"], "contradiction_edge": [finding_concepts["behavior"], concept]} for concept in direct_matches]
    expected_traversal = {"executed_quantity_intersection": direct_matches, "bridge_paths": dependency_paths, "contradiction_evidence": contradiction_evidence, "reachable_concepts": validator_reachable_nodes(ORACLE_ONTOLOGY_EDGES, finding_concepts["behavior"]), "computed_classification": expected_class}
    if graph["traversal_result"] != expected_traversal:
        raise ValidationFailure(f"{pair_id} independent ontology traversal result mismatch")
    bridges = graph["cross_domain_bridges"]
    if expected_class == "NOT_APPLICABLE":
        if bridges:
            raise ValidationFailure(f"{pair_id} NA graph contains an unsupported concept bridge")
    else:
        if not isinstance(bridges, list) or len(bridges) != 1 or set(bridges[0]) != BRIDGE_KEYS:
            raise ValidationFailure(f"{pair_id} concept-derived bridge schema/count mismatch")
        bridge = bridges[0]
        if bridge["pair_id"] != pair_id or bridge["kind"] != bridge_kind or bridge["path"] != bridge_path or bridge["source_node"] != bridge_path[0] or bridge["target_node"] != bridge_path[-1] or bridge["matched_scientific_concept"] != matched:
            raise ValidationFailure(f"{pair_id} bridge path/concept mismatch")
        if bridge["shared_executed_quantity_node"] != (matched if expected_class == "DIRECT" else None) or len(bridge["scientific_basis"].strip()) < 80:
            raise ValidationFailure(f"{pair_id} bridge scientific basis mismatch")
        if bridge["claim_anchor_sha256"] != [item["source_excerpt_sha256"] for item in claim_scope["source_anchor_refs"]] or bridge["finding_anchor_sha256"] != [hashlib.sha256(item["source_line"].encode("utf-8")).hexdigest() for item in code_scope["source_evidence"]] or bridge["authority_boundary"] != ADJUDICATION_BOUNDARY:
            raise ValidationFailure(f"{pair_id} bridge source/authority mismatch")
        payload = dict(bridge); stored = payload.pop("bridge_sha256")
        if stored != object_sha256(payload):
            raise ValidationFailure(f"{pair_id} bridge hash mismatch")
    normalized_finding_concepts = {"behavior": finding_concepts["behavior"], "violates": list(finding_concepts["violates"]), "emits": list(finding_concepts["emits"])}
    expected_structural = {
        "claim_concepts": claim_concepts,
        "finding_concepts": normalized_finding_concepts,
        "semantic_ontology_ref": expected_semantic_ontology_ref(),
        "direct_matches": direct_matches,
        "dependency_paths": dependency_paths,
    }
    if graph["structural_signature_basis"] != expected_structural or graph["structural_signature_sha256"] != object_sha256(expected_structural):
        raise ValidationFailure(f"{pair_id} graph structural basis/hash mismatch")
    if graph["authority_boundary"] != ADJUDICATION_BOUNDARY:
        raise ValidationFailure(f"{pair_id} graph authority boundary mismatch")
    payload = dict(graph); stored = payload.pop("pair_graph_audit_sha256")
    if stored != object_sha256(payload):
        raise ValidationFailure(f"{pair_id} pair graph audit hash mismatch")
    return expected_class


def validate_na_grounding_universe(
    main: dict[str, Any],
    ledger: list[dict[str, Any]],
    code_scopes: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    cross = main.get("semantic_cross_audit", {})
    groundings = cross.get("na_pair_groundings")
    groups = cross.get("na_grounding_groups")
    if not isinstance(groundings, list) or len(groundings) != 558 or not isinstance(groups, list):
        raise ValidationFailure("NA ontology grounding/group universe count mismatch")
    claim_scopes = {entry["claim_id"]: entry["claim_semantic_scope"] for entry in ledger}
    code_scope_by_id = {scope["code_finding_id"]: scope for scope in code_scopes}
    decision_by_pair = {
        f"{entry['claim_id']}->{decision['code_finding_id']}": decision
        for entry in ledger for decision in entry["code_finding_adjudications"]
    }
    expected_pairs = []
    for claim_id in claim_scopes:
        claim_concepts = oracle_claim_ontology_scope(claim_id)
        for code_id in code_scope_by_id:
            finding_concepts = ORACLE_FINDING_ONTOLOGY_SCOPE[code_id]
            direct = set(claim_concepts["direct_requirements"]) & set(finding_concepts["violates"])
            paths = [validator_directed_path(ORACLE_ONTOLOGY_EDGES, finding_concepts["behavior"], target) for target in claim_concepts["dependency_targets"]]
            if not direct and not any(paths):
                expected_pairs.append(f"{claim_id}->{code_id}")
    if [item.get("pair_id") for item in groundings] != expected_pairs or len(set(expected_pairs)) != 558:
        raise ValidationFailure("NA membership is not independently reconstructed from ontology cuts")

    expected_groups: list[dict[str, Any]] = []
    for grounding, pair_id in zip(groundings, expected_pairs):
        if not isinstance(grounding, dict) or set(grounding) != NA_GROUNDING_KEYS:
            raise ValidationFailure(f"{pair_id} NA grounding schema mismatch")
        claim_id, code_id = pair_id.split("->")
        claim_scope, code_scope = claim_scopes[claim_id], code_scope_by_id[code_id]
        claim_concepts = oracle_claim_ontology_scope(claim_id)
        finding_concepts = ORACLE_FINDING_ONTOLOGY_SCOPE[code_id]
        graph = decision_by_pair[pair_id]["pair_graph_audit"]
        if validate_pair_graph_audit(graph, claim_scope, code_scope) != "NOT_APPLICABLE":
            raise ValidationFailure(f"{pair_id} NA grounding has a reachable ontology path")
        if grounding["grounding_id"] != f"P059-NA-GROUND-{claim_id[-3:]}-{code_id[-3:]}" or grounding["claim_id"] != claim_id or grounding["code_finding_id"] != code_id:
            raise ValidationFailure(f"{pair_id} NA grounding identity mismatch")
        primary, behavior = claim_concepts["primary_concept"], finding_concepts["behavior"]
        group_rule = {
            "grounding_group_id": f"P059-NA-CONCEPT-{primary}__{behavior}",
            "claim_primary_concept": primary,
            "finding_behavior_concept": behavior,
            "incident_ontology_edges": [edge for edge in ORACLE_ONTOLOGY_EDGES if edge[0] == behavior or edge[1] == primary],
            "grouping_basis": "Exact scientific claim concept crossed with exact observed production behavior; IDs and source hashes are not grouping inputs.",
        }
        if grounding["grounding_group_id"] != group_rule["grounding_group_id"] or grounding["grounding_group_sha256"] != object_sha256(group_rule):
            raise ValidationFailure(f"{pair_id} NA concept group identity/hash mismatch")
        finding_refs = [{"path": item["path"], "line": item["line"], "source_line_sha256": hashlib.sha256(item["source_line"].encode("utf-8")).hexdigest()} for item in code_scope["source_evidence"]]
        claim_predicates = claim_concepts["direct_requirements"] or [primary]
        finding_predicates = list(finding_concepts["violates"]) or [behavior]
        direct_predicates = [
            {"claim_concept": claim_concept, "finding_concept": finding_concept, "same_scientific_concept": claim_concept == finding_concept, "contradiction_edge_present": [behavior, claim_concept] in ORACLE_ONTOLOGY_EDGES and claim_concept in finding_concepts["violates"]}
            for claim_concept in claim_predicates for finding_concept in finding_predicates
        ]
        dependency_targets = claim_concepts["dependency_targets"] or [primary]
        dependency_predicates = []
        for target in dependency_targets:
            path = validator_directed_path(ORACLE_ONTOLOGY_EDGES, behavior, target)
            dependency_predicates.append({"source_behavior_concept": behavior, "claim_target_concept": target, "path": path, "reachable": bool(path)})
        closure = validator_reachable_nodes(ORACLE_ONTOLOGY_EDGES, behavior)
        cut_evidence = []
        for target in dependency_targets:
            incoming = [edge for edge in ORACLE_ONTOLOGY_EDGES if edge[1] == target]
            reached_predecessors = [left for left, _ in incoming if left in closure]
            cut_evidence.append({
                "claim_target_concept": target,
                "target_absent_from_reachable_closure": target not in closure,
                "incoming_ontology_edges": incoming,
                "reached_predecessors": reached_predecessors,
                "blocking_cut": f"No audited ontology edge leaves {behavior} toward {target}." if not incoming else f"Only {sorted({left for left, _ in incoming})} feed {target}; none belongs to this finding's reachable closure.",
            })
        certificate_basis = {
            "claim_primary_concept": primary,
            "claim_direct_requirements": claim_concepts["direct_requirements"],
            "claim_dependency_targets": claim_concepts["dependency_targets"],
            "finding_behavior_concept": behavior,
            "finding_violated_requirements": list(finding_concepts["violates"]),
            "finding_dependency_outputs": list(finding_concepts["emits"]),
            "evaluated_direct_predicates": direct_predicates,
            "evaluated_dependency_predicates": dependency_predicates,
            "reachable_concepts": closure,
            "cut_evidence": cut_evidence,
            "contradiction_count": 0,
            "computed_conclusion": "NOT_APPLICABLE",
        }
        expected_certificate = {
            **certificate_basis,
            "claim_source_refs": claim_scope["source_anchor_refs"],
            "finding_source_refs": finding_refs,
            "claim_scope_sha256": object_sha256(claim_scope),
            "code_scope_sha256": object_sha256(code_scope),
            "authority_boundary": ADJUDICATION_BOUNDARY,
            "semantic_proof_signature_sha256": object_sha256(certificate_basis),
        }
        expected_certificate["certificate_sha256"] = object_sha256(expected_certificate)
        if grounding["nonconnection_certificate"] != expected_certificate:
            raise ValidationFailure(f"{pair_id} exact-pair nonconnection certificate mismatch")
        if any(item["same_scientific_concept"] or item["contradiction_edge_present"] for item in direct_predicates) or any(item["reachable"] for item in dependency_predicates):
            raise ValidationFailure(f"{pair_id} NA certificate contains a contradiction or reachable dependency")
        if grounding["examined_claim_anchors"] != claim_scope["source_anchor_refs"] or grounding["examined_finding_anchors"] != finding_refs or grounding["examined_finding_behavior"] != code_scope["actual_production_behavior"]:
            raise ValidationFailure(f"{pair_id} NA source grounding mismatch")
        expected_quantities = [claim_scope["claim_quantity_or_dependency"], claim_scope["dependency_direction"], primary] + claim_concepts["direct_requirements"] + claim_concepts["dependency_targets"]
        if grounding["examined_claim_quantities"] != expected_quantities:
            raise ValidationFailure(f"{pair_id} examined scientific quantities mismatch")
        if grounding["pair_graph_audit_id"] != graph["pair_graph_audit_id"] or grounding["pair_graph_audit_sha256"] != graph["pair_graph_audit_sha256"]:
            raise ValidationFailure(f"{pair_id} NA pair graph reverse link mismatch")
        expected_intersection = {"result": "NONE", "claim_nodes": claim_concepts["direct_requirements"], "finding_nodes": list(finding_concepts["violates"]), "common_executed_nodes": [], "finding": "Exact ontology requirement intersection is empty."}
        expected_dependency = {"result": "NONE", "claim_edges": graph["claim_graph"]["directed_edges"], "finding_edges": graph["finding_graph"]["directed_edges"], "cross_domain_bridges": [], "paths": [], "finding": "Independent directed traversal reaches no claim dependency target; see nonconnection_certificate.cut_evidence."}
        expected_contradiction = {"result": "NONE", "claim_assertion": claim_scope["claim_quantity_or_dependency"], "observed_behavior": code_scope["actual_production_behavior"], "evidence": [], "finding": "Every stored direct predicate is false."}
        if grounding["executed_quantity_intersection"] != expected_intersection or grounding["dependency_reachability"] != expected_dependency or grounding["contradiction_finding"] != expected_contradiction:
            raise ValidationFailure(f"{pair_id} NA predicate summary mismatch")
        required_substance = [primary, behavior, claim_scope["claim_quantity_or_dependency"], claim_scope["dependency_direction"], claim_scope["non_goal"], code_scope["actual_production_behavior"], code_scope["finding_affected_quantity_or_path"], code_scope["non_adjudicated_quantities"]]
        if any(text not in grounding["conclusion_specific_rationale"] for text in required_substance):
            raise ValidationFailure(f"{pair_id} NA rationale omits exact scientific substance")
        if primary not in grounding["exclusion_boundary"] or behavior not in grounding["exclusion_boundary"] or claim_scope["non_goal"] not in grounding["exclusion_boundary"] or code_scope["non_adjudicated_quantities"] not in grounding["exclusion_boundary"]:
            raise ValidationFailure(f"{pair_id} NA exclusion omits exact cut/authority substance")
        structural_basis = {
            "claim_concept_cardinality": {key: len(value) if isinstance(value, list) else 1 for key, value in claim_concepts.items()},
            "finding_concept_cardinality": {"violates": len(finding_concepts["violates"]), "emits": len(finding_concepts["emits"])},
            "direct_predicate_truth_vector": [item["same_scientific_concept"] or item["contradiction_edge_present"] for item in direct_predicates],
            "dependency_reachability_truth_vector": [item["reachable"] for item in dependency_predicates],
            "cut_cardinality": len(cut_evidence),
        }
        if grounding["structural_signature_basis"] != structural_basis or grounding["structural_signature_sha256"] != object_sha256(structural_basis):
            raise ValidationFailure(f"{pair_id} NA structural proof basis/hash mismatch")
        if grounding["reasoning_signature_sha256"] != object_sha256(certificate_basis):
            raise ValidationFailure(f"{pair_id} NA normalized semantic proof basis/hash mismatch")
        expected_checks = expected_review_check_manifest(
            claim_scope["source_anchor_refs"],
            finding_refs,
            direct_predicates,
            dependency_predicates,
            cut_evidence,
        )
        if grounding["review_checks"] != expected_checks or grounding["shared_contract_candidates"] != decision_by_pair[pair_id]["shared_contract_ids"] or grounding["claim_scope_sha256"] != object_sha256(claim_scope) or grounding["code_scope_sha256"] != object_sha256(code_scope) or grounding["authority_boundary"] != ADJUDICATION_BOUNDARY:
            raise ValidationFailure(f"{pair_id} NA review/source/authority fields mismatch")
        payload = dict(grounding); stored = payload.pop("grounding_sha256")
        if stored != object_sha256(payload):
            raise ValidationFailure(f"{pair_id} NA grounding hash mismatch")
        expected_groups.append({**group_rule, "grounding_group_sha256": object_sha256(group_rule), "member_pair_ids": [pair_id], "member_count": 1})

    if groups != expected_groups or len(groups) != 558:
        raise ValidationFailure("NA scientific concept group ledger/reverse membership mismatch")
    if any(set(group) != NA_GROUP_KEYS for group in groups):
        raise ValidationFailure("NA scientific concept group schema mismatch")
    structural_count = len({item["structural_signature_sha256"] for item in groundings})
    proof_count = len({item["nonconnection_certificate"]["semantic_proof_signature_sha256"] for item in groundings})
    if structural_count != 84 or proof_count != 558:
        raise ValidationFailure(f"NA proof diversity mismatch: structural={structural_count} semantic={proof_count}")
    return ({item["pair_id"]: item for item in groundings}, groundings, groups)


def validate_claim_semantic_scope(scope: Any, claim: dict[str, Any]) -> None:
    claim_id = claim["claim_id"]
    if not isinstance(scope, dict) or set(scope) != CLAIM_SCOPE_KEYS:
        raise ValidationFailure(f"{claim_id} substantive claim semantic scope schema mismatch")
    expected_source = expected_claim_semantic_scope(claim)
    for key, value in expected_source.items():
        if scope.get(key) != value:
            raise ValidationFailure(f"{claim_id} claim semantic scope source identity mismatch: {key}")
    semantic_tuple = (scope["claim_quantity_or_dependency"], scope["dependency_direction"], scope["non_goal"])
    if object_sha256(semantic_tuple) != EXPECTED_CLAIM_SEMANTIC_TUPLE_SHA256[claim_id]:
        raise ValidationFailure(f"{claim_id} claim quantity/dependency/non-goal semantic oracle mismatch")
    if any(not isinstance(value, str) or len(value.strip()) < 24 for value in semantic_tuple):
        raise ValidationFailure(f"{claim_id} claim semantic substance is blank or generic")


def validate_finding_semantic_scope(scope: Any, finding: dict[str, Any]) -> None:
    finding_id = finding["id"]
    if not isinstance(scope, dict) or set(scope) != FINDING_SCOPE_KEYS:
        raise ValidationFailure(f"{finding_id} substantive finding semantic scope schema mismatch")
    expected_source = expected_code_semantic_scope(finding)
    for key, value in expected_source.items():
        if scope.get(key) != value:
            raise ValidationFailure(f"{finding_id} finding semantic scope source identity mismatch: {key}")
    semantic_tuple = (scope["finding_affected_quantity_or_path"], scope["non_adjudicated_quantities"])
    if object_sha256(semantic_tuple) != EXPECTED_FINDING_SEMANTIC_TUPLE_SHA256[finding_id]:
        raise ValidationFailure(f"{finding_id} finding path/non-adjudicated semantic oracle mismatch")
    if any(not isinstance(value, str) or len(value.strip()) < 24 for value in semantic_tuple):
        raise ValidationFailure(f"{finding_id} finding semantic substance is blank or generic")


def expected_semantic_cross_audit(ledger: list[dict[str, Any]], code_findings: list[dict[str, Any]], code_scopes: list[dict[str, Any]], na_groundings: list[dict[str, Any]], na_groups: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = [decision for entry in ledger for decision in entry["code_finding_adjudications"]]
    graph_audits = [decision["pair_graph_audit"] for decision in decisions]
    bridge_oracle = [bridge for graph in graph_audits for bridge in graph["cross_domain_bridges"]]
    claim_scope_by_id = {entry["claim_id"]: entry["claim_semantic_scope"] for entry in ledger}
    code_scope_by_id = {scope["code_finding_id"]: scope for scope in code_scopes}
    ontology_nodes = []
    for claim_id, concept in ORACLE_CLAIM_PRIMARY_CONCEPT.items():
        ontology_nodes.append({"concept": concept, "kind": "CLAIM_PRIMARY_QUANTITY_OR_DEPENDENCY", "definition": claim_scope_by_id[claim_id]["claim_quantity_or_dependency"], "source_claim_ids": [claim_id]})
    for concept, members in ORACLE_DIRECT_REQUIREMENT_CLAIMS.items():
        ontology_nodes.append({"concept": concept, "kind": "DIRECT_SCIENTIFIC_REQUIREMENT", "definition": concept.replace("_", " "), "source_claim_ids": list(members)})
    for concept, members in ORACLE_DEPENDENCY_TARGET_CLAIMS.items():
        ontology_nodes.append({"concept": concept, "kind": "UPSTREAM_OR_DOWNSTREAM_DEPENDENCY_TARGET", "definition": concept.replace("_", " "), "source_claim_ids": list(members)})
    for code_id, scope in ORACLE_FINDING_ONTOLOGY_SCOPE.items():
        ontology_nodes.append({"concept": scope["behavior"], "kind": "OBSERVED_PRODUCTION_BEHAVIOR", "definition": code_scope_by_id[code_id]["finding_affected_quantity_or_path"], "source_code_finding_ids": [code_id]})
    proof_bases = [
        certificate_basis_from_certificate(grounding["nonconnection_certificate"])
        for grounding in na_groundings
    ]
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
        "distinct_semantic_proof_structure_count": len({object_sha256(basis) for basis in proof_bases}),
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
            **expected_semantic_ontology_ref(),
            "classification_method": "DIRECT from requirement/violation intersection; RELATED_NOT_DIRECT from directed behavior-to-claim-target reachability; NOT_APPLICABLE only from an empty intersection, no contradiction, and an explicit reachability cut.",
            "nodes": ontology_nodes,
            "directed_edges": ORACLE_ONTOLOGY_EDGES,
            "claim_memberships": [{"claim_id": claim_id, **oracle_claim_ontology_scope(claim_id)} for claim_id in ORACLE_CLAIM_PRIMARY_CONCEPT],
            "finding_memberships": [{"code_finding_id": code_id, "behavior": scope["behavior"], "violates": list(scope["violates"]), "emits": list(scope["emits"])} for code_id, scope in ORACLE_FINDING_ONTOLOGY_SCOPE.items()],
            "authority_boundary": ADJUDICATION_BOUNDARY,
        },
        "na_grounding_groups": na_groups,
        "na_pair_groundings": na_groundings,
        "na_normalization_audit": normalization_audit,
        "cross_domain_bridge_oracle": bridge_oracle,
        "claim_count": len(ledger),
        "code_finding_count": len(code_findings),
        "pair_count": len(decisions),
        "classification_counts": dict(sorted(Counter(decision["applicability"] for decision in decisions).items())),
        "shared_contract_candidate_pairs": sum(bool(decision["shared_contract_ids"]) for decision in decisions),
        "nonshared_direct_or_related_pairs": [
            f"{entry['claim_id']}->{decision['code_finding_id']}"
            for entry in ledger
            for decision in entry["code_finding_adjudications"]
            if decision["applicability"] != "NOT_APPLICABLE" and not decision["shared_contract_ids"]
        ],
        "pair_specific_basis_count": len({decision["basis"] for decision in decisions}),
        "structured_comparison_count": len(decisions),
        "na_pair_grounding_count": len(na_groundings),
        "na_grounding_group_count": len(na_groups),
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


def validate_adjudication_ledger(main: dict[str, Any], claims: list[dict[str, Any]], code_findings: list[dict[str, Any]]) -> dict[str, list[str]]:
    applicable = [claim for claim in claims if claim["evidence_contract_ids"]]
    ledger = main.get("applicable_claim_code_adjudications")
    if not isinstance(ledger, list) or len(ledger) != 51: raise ValidationFailure("51 applicable theory claims are not adjudicated exactly once")
    if [x.get("claim_id") for x in ledger] != [x["claim_id"] for x in applicable]: raise ValidationFailure("applicable claim adjudication ledger dropped/duplicated/reordered")
    code_ids = [x["id"] for x in code_findings]
    code_scopes = main.get("semantic_cross_audit", {}).get("code_finding_semantic_scopes")
    if not isinstance(code_scopes, list) or len(code_scopes) != 13:
        raise ValidationFailure("13 substantive code-finding semantic scopes are not preserved")
    for scope, finding in zip(code_scopes, code_findings):
        validate_finding_semantic_scope(scope, finding)
    code_scope_by_id = {scope["code_finding_id"]: scope for scope in code_scopes}
    grounding_by_pair, na_groundings, na_groups = validate_na_grounding_universe(main, ledger, code_scopes)
    direct_by_claim: dict[str, list[str]] = {}; decision_counts: Counter[str] = Counter(); graph_audits = []; bridge_oracle = []
    for entry, claim in zip(ledger, applicable):
        if set(entry) != CLAIM_LEDGER_KEYS: raise ValidationFailure(f"{claim['claim_id']} adjudication ledger schema mismatch")
        if entry["claim_sha256"] != object_sha256(claim) or entry["evidence_contract_ids"] != claim["evidence_contract_ids"] or entry["evidence_relation_ids"] != claim["evidence_relation_ids"]: raise ValidationFailure(f"{claim['claim_id']} adjudication theory identity mismatch")
        claim_scope = entry["claim_semantic_scope"]
        validate_claim_semantic_scope(claim_scope, claim)
        decisions = entry["code_finding_adjudications"]
        if not isinstance(decisions, list) or [x.get("code_finding_id") for x in decisions] != code_ids: raise ValidationFailure(f"{claim['claim_id']} must adjudicate all 13 code findings in order")
        expected_direct = EXPECTED_DIRECT_CODE.get(claim["claim_id"], []); actual_direct = []
        for index, (decision, finding) in enumerate(zip(decisions, code_findings), start=1):
            if set(decision) != ADJUDICATION_KEYS: raise ValidationFailure(f"{claim['claim_id']} code adjudication schema mismatch")
            expected_id = f"P059-F4-ADJ-{claim['claim_id'][-3:]}-{index:02d}"
            if decision["adjudication_id"] != expected_id: raise ValidationFailure(f"{claim['claim_id']} nondeterministic adjudication ID")
            shared = sorted(set(claim["evidence_contract_ids"]) & set(finding["contract_ids"]))
            if decision["shared_contract_ids"] != shared: raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} shared-contract reconstruction mismatch")
            pair = (claim["claim_id"], finding["id"])
            expected_app = "DIRECT" if finding["id"] in expected_direct else ("RELATED_NOT_DIRECT" if pair in EXPECTED_RELATED_CODE else "NOT_APPLICABLE")
            if decision["applicability"] != expected_app or expected_app not in ALLOWED_APPLICABILITY: raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} substantive applicability mismatch")
            expected_contracts = shared if expected_app == "DIRECT" else []
            if decision["direct_contract_ids"] != expected_contracts: raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} direct-contract mismatch")
            expected_relations = claim_contract_relation_ids(claim, expected_contracts)
            if expected_app == "DIRECT" and not expected_contracts: expected_relations = claim["evidence_relation_ids"]
            if decision["theory_relation_ids"] != expected_relations: raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} theory-relation evidence mismatch")
            claim_basis = {"claim_id": claim["claim_id"], "labels": claim["labels"], "contracts": claim["evidence_contract_ids"], "relations": claim["evidence_relation_ids"], "code_impact": claim["code_impact"]}
            if decision["claim_basis_sha256"] != object_sha256(claim_basis) or decision["code_basis_sha256"] != object_sha256(finding): raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} adjudication basis hash mismatch")
            code_scope = code_scope_by_id[finding["id"]]
            if decision["claim_semantic_scope_sha256"] != object_sha256(claim_scope) or decision["code_semantic_scope_sha256"] != object_sha256(code_scope): raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} semantic scope hash mismatch")
            graph_classification = validate_pair_graph_audit(decision["pair_graph_audit"], claim_scope, code_scope)
            if graph_classification != expected_app or graph_classification != decision["applicability"]:
                raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} graph traversal/classification reconciliation mismatch")
            graph_audits.append(decision["pair_graph_audit"]); bridge_oracle.extend(decision["pair_graph_audit"]["cross_domain_bridges"])
            if decision["semantic_audit_method"] != "FULL_EQUATION_PROSE_DERIVATION_CODE_IMPACT_X_FINDING_CROSS_AUDIT": raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} semantic audit method mismatch")
            prefix = f"Semantic audit {claim['claim_id']}->{finding['id']}: "
            comparison = decision["comparison"]
            if not isinstance(comparison, dict) or set(comparison) != COMPARISON_KEYS:
                raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} structured comparison schema mismatch")
            if expected_app == "NOT_APPLICABLE":
                grounding = grounding_by_pair[f"{claim['claim_id']}->{finding['id']}"]
                if decision["na_pair_grounding_id"] != grounding["grounding_id"]:
                    raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} NA grounding reverse-link mismatch")
                expected_comparison = {
                    "claim_quantity_or_dependency": claim_scope["claim_quantity_or_dependency"],
                    "finding_affected_quantity_or_path": code_scope["finding_affected_quantity_or_path"],
                    "overlap_or_dependency_path": grounding["dependency_reachability"]["finding"],
                    "classification_reason": grounding["conclusion_specific_rationale"],
                    "exclusion_boundary": grounding["exclusion_boundary"],
                }
            else:
                if decision["na_pair_grounding_id"] is not None:
                    raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} non-NA decision has a grounding reverse-link")
                reason = comparison.get("classification_reason")
                if not isinstance(reason, str) or len(reason.strip()) < 80 or reason.lower() in {"direct", "related", "not applicable", "generic boilerplate"}:
                    raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} non-NA scientific comparison is blank or generic")
                affected = code_scope["finding_affected_quantity_or_path"]
                excluded = code_scope["non_adjudicated_quantities"]
                if expected_app == "DIRECT":
                    overlap = f"DIRECT executed/contradicted path: {reason}"
                    boundary = f"Direct only to {affected}; it does not adjudicate {excluded}. Claim boundary: {claim_scope['non_goal']}"
                else:
                    overlap = f"BOUNDED upstream/downstream dependency: {reason}"
                    boundary = f"Related context only: the finding can alter an input or prerequisite but does not adjudicate {claim_scope['claim_quantity_or_dependency']}. It also excludes {excluded}."
                expected_comparison = {"claim_quantity_or_dependency": claim_scope["claim_quantity_or_dependency"], "finding_affected_quantity_or_path": affected, "overlap_or_dependency_path": overlap, "classification_reason": reason, "exclusion_boundary": boundary}
            if comparison != expected_comparison:
                raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} substantive pair comparison mismatch")
            if decision["basis"] != prefix + comparison["classification_reason"]:
                raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} pair basis/comparison mismatch")
            if not decision["basis"].strip() or "external material validity" not in decision["authority_boundary"].lower(): raise ValidationFailure(f"{claim['claim_id']}->{finding['id']} adjudication rationale/authority missing")
            if expected_app == "DIRECT": actual_direct.append(finding["id"])
            decision_counts[expected_app] += 1
        if actual_direct != expected_direct or entry["direct_code_evidence_ids"] != expected_direct or entry["direct_code_relation_count"] != len(expected_direct): raise ValidationFailure(f"{claim['claim_id']} direct-code reverse membership mismatch")
        if "external material validity" not in entry["authority_boundary"].lower(): raise ValidationFailure(f"{claim['claim_id']} adjudication authority boundary missing")
        direct_by_claim[claim["claim_id"]] = expected_direct
    if decision_counts != Counter({"DIRECT": 42, "RELATED_NOT_DIRECT": 63, "NOT_APPLICABLE": 558}): raise ValidationFailure("663 adjudication decisions do not reconcile 42/63/558")
    if len(graph_audits) != 663 or len({graph["pair_id"] for graph in graph_audits}) != 663:
        raise ValidationFailure("independently reconstructed pair graph ledger is incomplete")
    if bridge_oracle != main.get("semantic_cross_audit", {}).get("cross_domain_bridge_oracle") or len(bridge_oracle) != 105:
        raise ValidationFailure("concept-derived bridge oracle membership/count mismatch")
    if main.get("semantic_cross_audit") != expected_semantic_cross_audit(ledger, code_findings, code_scopes, na_groundings, na_groups): raise ValidationFailure("51x13 semantic cross-audit coverage/method mismatch")
    if len({decision["basis"] for entry in ledger for decision in entry["code_finding_adjudications"]}) != 663: raise ValidationFailure("pair-specific semantic bases are duplicated")
    return direct_by_claim


def validate_main(document: dict[str, Any], code_records: dict[str, dict[str, Any]], test_records: dict[str, dict[str, Any]], artifact_records: dict[str, dict[str, Any]]) -> None:
    if document.get("schema_version") != 7:
        raise ValidationFailure("four-axis schema version must be 7 for content-addressed ontology/certificate audit")
    theory = load_source(INPUT_PATHS[0]); claims = theory["claims"]
    code_findings = load_source(INPUT_PATHS[3])["review"]["findings"]
    direct_by_claim = validate_adjudication_ledger(document, claims, code_findings)
    rows = document.get("rows")
    if not isinstance(rows, list) or len(rows) != 185: raise ValidationFailure("four-axis row count must be exactly 185")
    expected_claim_ids = [x["claim_id"] for x in claims]; actual_claim_ids = [x.get("claim_id") for x in rows]
    if actual_claim_ids != expected_claim_ids or len(actual_claim_ids) != len(set(actual_claim_ids)): raise ValidationFailure("theory rows dropped, duplicated, orphaned, or reordered")
    routes: dict[str, list[str]] = {cid: [] for cid in expected_claim_ids}
    for route in theory["contract_routes"]: routes[route["claim_id"]].append(route["contract_id"])
    statuses: Counter[str] = Counter(); occurrence_ids: list[str] = []; relation_ids: list[str] = []
    for row, claim in zip(rows, claims):
        claim_id = claim["claim_id"]
        if set(row) != ROW_KEYS or row["theory_claim_sha256"] != object_sha256(claim): raise ValidationFailure(f"{claim_id} four-axis row schema/hash mismatch")
        expected_theory_axis = {
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
        if row["theory_axis"] != expected_theory_axis: raise ValidationFailure(f"{claim_id} governing/evidence theory relation mismatch")
        occurrence_ids.extend(row["theory_axis"]["mapped_occurrence_ids"]); relation_ids.extend(row["theory_axis"]["evidence_relation_ids"])
        validate_axis(row["production_axis"], "PRODUCTION_BEHAVIOR", "CODE", code_records)
        validate_axis(row["test_runtime_axis"], "RELEASE_TEST_DEMO_RUNTIME", "TEST_RUNTIME", test_records)
        validate_axis(row["stored_artifact_axis"], "STORED_ARTIFACT", "STORED_ARTIFACT", artifact_records)
        expected_code = direct_by_claim.get(claim_id, []); expected_test = EXPECTED_TEST.get(claim_id, []); expected_artifact = EXPECTED_ARTIFACT.get(claim_id, [])
        if link_ids(row["production_axis"]) != expected_code: raise ValidationFailure(f"{claim_id} production evidence mapping mismatch")
        if link_ids(row["test_runtime_axis"]) != expected_test: raise ValidationFailure(f"{claim_id} test/runtime evidence mapping mismatch")
        if link_ids(row["stored_artifact_axis"]) != expected_artifact: raise ValidationFailure(f"{claim_id} stored-artifact evidence mapping mismatch")
        expected_status = EXPECTED_STATUS.get(claim_id, "UNVERIFIED")
        if row["conformance_status"] != expected_status or expected_status not in ALLOWED_STATUSES: raise ValidationFailure(f"{claim_id} conformance status mismatch")
        expected_blockers = EXPECTED_BLOCKERS.get(claim_id, ["P059-BD-NEW-003"] if not claim["evidence_contract_ids"] else [])
        if row["blocker_routes"] != expected_blockers: raise ValidationFailure(f"{claim_id} blocker route mismatch")
        if not row["decision_basis"].strip() or not row["blocker_route_basis"].strip() or "external material validity" not in row["authority_boundary"].lower(): raise ValidationFailure(f"{claim_id} rationale/authority boundary missing")
        if row["code_impact"] != claim["code_impact"]: raise ValidationFailure(f"{claim_id} code impact mismatch")
        if not claim["evidence_contract_ids"] and row["conformance_status"] == "ALIGNED": raise ValidationFailure(f"{claim_id} unjustified ALIGNED for uncontracted claim")
        statuses[expected_status] += 1
    expected_occurrences = [occ for claim in claims for occ in claim["mapped_occurrence_ids"]]
    if occurrence_ids != expected_occurrences or len(occurrence_ids) != 973 or len(set(occurrence_ids)) != 973: raise ValidationFailure("973 theory occurrences are not routed exactly once")
    expected_relations = [rel for claim in claims for rel in claim["evidence_relation_ids"]]
    if relation_ids != expected_relations or len(relation_ids) != 80 or len(set(relation_ids)) != 80: raise ValidationFailure("80 contract evidence relations are not preserved exactly once")
    findings = document.get("high_risk_findings")
    if not isinstance(findings, list) or [x.get("finding_id") for x in findings] != list(HIGH_RISK_EXPECTED): raise ValidationFailure("high-risk finding IDs/order mismatch")
    universes = {"CODE": code_records, "TEST_RUNTIME": test_records, "STORED_ARTIFACT": artifact_records}
    for finding in findings:
        fid = finding["finding_id"]
        if set(finding) != {"finding_id", "topic", "claim_ids", "evidence_links", "finding", "authority_boundary"}: raise ValidationFailure(f"{fid} high-risk schema contains bare evidence IDs")
        expected = HIGH_RISK_EXPECTED[fid]
        if finding["claim_ids"] != expected["claims"]: raise ValidationFailure(f"{fid} claim boundary mismatch")
        actual_refs = []
        for link in finding["evidence_links"]:
            evidence_class = link.get("evidence_class")
            if evidence_class not in universes: raise ValidationFailure(f"{fid} noncanonical evidence class")
            validate_link(
                link,
                evidence_class,
                universes[evidence_class],
                "HIGH_RISK_STRUCTURED_EVIDENCE",
            )
            actual_refs.append((evidence_class, link["evidence_id"]))
        if actual_refs != expected["evidence"]: raise ValidationFailure(f"{fid} structured evidence mapping mismatch")
        if any(cid not in expected_claim_ids for cid in finding["claim_ids"]): raise ValidationFailure(f"{fid} invalid theory claim reference")
        if not finding["finding"].strip() or not finding["authority_boundary"].strip(): raise ValidationFailure(f"{fid} missing finding/authority boundary")
    lco, si = findings[5], findings[7]
    if any(claim_id not in lco["claim_ids"] for claim_id in ("P059-TCL-033", "P059-TCL-056", "P059-TCL-081", "P059-TCL-084")) or "298.15 K" not in lco["finding"] or "high-voltage" not in lco["finding"]: raise ValidationFailure("LCO claim coverage/freeze/high-voltage boundary mismatch")
    if "audited test/demo" not in si["finding"] or "audited images" not in si["finding"] or "does not establish production-code absence" not in si["authority_boundary"]: raise ValidationFailure("Si/blend evidence boundary overstates linked scope")
    if "joint low-temperature/finite-current" not in findings[0]["finding"]: raise ValidationFailure("low-temperature finite-current boundary mismatch")
    if "initial state" not in findings[1]["finding"] or "sorting" not in findings[1]["finding"]: raise ValidationFailure("chronology/initial-history boundary mismatch")
    if "public experimental" not in findings[8]["finding"] or "external material validity" not in findings[8]["authority_boundary"]: raise ValidationFailure("public-data boundary mismatch")
    expected_counts = {
        "theory_claims": 185,
        "theory_occurrences": 973,
        "governing_contract_routes": 38,
        "contract_evidence_relations": 80,
        "applicable_theory_claims": 51,
        "code_finding_adjudications": 663,
        "direct_code_relations": 42,
        "related_not_direct_code_decisions": 63,
        "not_applicable_code_decisions": 558,
        "na_pair_groundings": 558,
        "na_grounding_groups": 558,
        "na_structural_signatures": 84,
        "na_reasoning_signatures": 558,
        "pair_graph_audits": 663,
        "cross_domain_bridges": 105,
        "code_canonical_records": len(code_records),
        "test_runtime_canonical_records": len(test_records),
        "artifact_canonical_records": len(artifact_records),
        "row_orphans": 0,
        "row_duplicates": 0,
        "invalid_evidence_paths_or_anchors": 0,
        "missing_authority_boundaries": 0,
        "status_counts": {
            status: statuses.get(status, 0)
            for status in sorted(ALLOWED_STATUSES)
        },
        "high_risk_findings": len(HIGH_RISK_EXPECTED),
    }
    if document.get("counts") != expected_counts: raise ValidationFailure("four-axis count/status reconciliation mismatch")
    validate_common(document, "PASS_P059_FOUR_AXIS_CONFORMANCE_MATRIX", EXPECTED_MAIN_SEMANTIC_SHA256)


def load_output(path: str) -> dict[str, Any]:
    target = ROOT / path
    if not target.is_file(): raise ValidationFailure(f"missing artifact: {path}")
    try: return json.loads(target.read_bytes())
    except (UnicodeDecodeError, json.JSONDecodeError) as exc: raise ValidationFailure(f"invalid JSON artifact: {path}: {exc}") from exc


def validate_documents(code: dict[str, Any], test: dict[str, Any], main: dict[str, Any]) -> None:
    validate_review_completeness(code, test, main)
    code_records = validate_code(code)
    test_records, artifact_records = validate_test(test)
    validate_main(main, code_records, test_records, artifact_records)


def validate_paths(code_path: str = CODE_PATH, test_path: str = TEST_PATH, main_path: str = MAIN_PATH) -> None:
    validate_documents(load_output(code_path), load_output(test_path), load_output(main_path))


def find_row(main: dict[str, Any], claim_id: str) -> dict[str, Any]:
    return next(x for x in main["rows"] if x["claim_id"] == claim_id)


def find_ledger(main: dict[str, Any], claim_id: str) -> dict[str, Any]:
    return next(x for x in main["applicable_claim_code_adjudications"] if x["claim_id"] == claim_id)


def find_decision(main: dict[str, Any], claim_id: str, code_id: str) -> dict[str, Any]:
    return next(x for x in find_ledger(main, claim_id)["code_finding_adjudications"] if x["code_finding_id"] == code_id)


def drop_adjudication_direct_link(main: dict[str, Any], claim_id: str, code_id: str) -> None:
    entry = find_ledger(main, claim_id)
    decision = next(x for x in entry["code_finding_adjudications"] if x["code_finding_id"] == code_id)
    decision["applicability"] = "NOT_APPLICABLE"; decision["direct_contract_ids"] = []; decision["theory_relation_ids"] = []
    entry["direct_code_evidence_ids"].remove(code_id); entry["direct_code_relation_count"] -= 1
    row = find_row(main, claim_id)
    row["production_axis"]["evidence_links"] = [x for x in row["production_axis"]["evidence_links"] if x["evidence_id"] != code_id]


def run_negative_probes() -> None:
    base_code, base_test, base_main = load_output(CODE_PATH), load_output(TEST_PATH), load_output(MAIN_PATH)
    def bare_artifact(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        link = find_row(m, "P059-TCL-084")["stored_artifact_axis"]["evidence_links"][0]
        find_row(m, "P059-TCL-084")["stored_artifact_axis"]["evidence_links"] = [{"evidence_id": link["evidence_id"]}]
    def drop_artifact_record(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        t["artifact_records"] = [x for x in t["artifact_records"] if x["record_id"] != "IMG-059-05"]
    def drop_lco_claim(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None: m["high_risk_findings"][5]["claim_ids"].remove("P059-TCL-084")
    def reseal_grounding(grounding: dict[str, Any]) -> None:
        grounding.pop("grounding_sha256", None)
        grounding["grounding_sha256"] = object_sha256(grounding)
    def reseal_graph(graph: dict[str, Any]) -> None:
        graph.pop("pair_graph_audit_sha256", None)
        graph["pair_graph_audit_sha256"] = object_sha256(graph)
    def swap_na_groundings(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        items = m["semantic_cross_audit"]["na_pair_groundings"]
        items[0], items[1] = items[1], items[0]
    def swap_na_grounding_payload(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        first, second = m["semantic_cross_audit"]["na_pair_groundings"][:2]
        identity = {key: first[key] for key in ("grounding_id", "pair_id", "claim_id", "code_finding_id")}
        first.clear(); first.update(copy.deepcopy(second)); first.update(identity)
        reseal_grounding(first)
    def generic_na_grounding(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        grounding = m["semantic_cross_audit"]["na_pair_groundings"][0]
        grounding["conclusion_specific_rationale"] = "Generic template: no overlap, no dependency, no contradiction."
        reseal_grounding(grounding)
    def tamper_na_group(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        group = m["semantic_cross_audit"]["na_grounding_groups"][0]
        group["grouping_basis"] = "generic dependency absence"
        rule = {key: value for key, value in group.items() if key not in {"grounding_group_sha256", "member_pair_ids", "member_count"}}
        group["grounding_group_sha256"] = object_sha256(rule)
    def tamper_na_source_anchor(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        grounding = m["semantic_cross_audit"]["na_pair_groundings"][0]
        grounding["examined_claim_anchors"][0]["line_start"] += 1
        reseal_grounding(grounding)
    def tcl155_back_to_na(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        find_decision(m, "P059-TCL-155", "P059-CODE-002")["applicability"] = "NOT_APPLICABLE"
    def remove_tcl155_bridge(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        graph = find_decision(m, "P059-TCL-155", "P059-CODE-002")["pair_graph_audit"]
        graph["cross_domain_bridges"] = []; reseal_graph(graph)
    def add_bridge_to_na(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        graph = find_decision(m, "P059-TCL-001", "P059-CODE-001")["pair_graph_audit"]
        graph["cross_domain_bridges"] = copy.deepcopy(find_decision(m, "P059-TCL-155", "P059-CODE-002")["pair_graph_audit"]["cross_domain_bridges"])
        reseal_graph(graph)
    def hardcode_none_on_reachable(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        graph = find_decision(m, "P059-TCL-155", "P059-CODE-002")["pair_graph_audit"]
        graph["traversal_result"] = {"executed_quantity_intersection": [], "bridge_paths": [], "contradiction_evidence": [], "computed_classification": "NOT_APPLICABLE"}; reseal_graph(graph)
    def delete_grounding_rationale_field(m: dict[str, Any], basis_key: str) -> None:
        grounding = m["semantic_cross_audit"]["na_pair_groundings"][0]
        claim_scope = find_ledger(m, grounding["claim_id"])["claim_semantic_scope"]
        code_scope = next(item for item in m["semantic_cross_audit"]["code_finding_semantic_scopes"] if item["code_finding_id"] == grounding["code_finding_id"])
        exact = {
            "claim_quantity_or_dependency": claim_scope["claim_quantity_or_dependency"],
            "finding_behavior": code_scope["actual_production_behavior"],
            "claim_non_goal": claim_scope["non_goal"],
            "finding_non_adjudicated_scope": code_scope["non_adjudicated_quantities"],
        }[basis_key]
        grounding["conclusion_specific_rationale"] = grounding["conclusion_specific_rationale"].replace(exact, "")
        reseal_grounding(grounding)
    def tamper_graph_edge(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        graph = find_decision(m, "P059-TCL-155", "P059-CODE-002")["pair_graph_audit"]
        graph["claim_graph"]["directed_edges"][0][1] = "TAMPERED_NODE"; reseal_graph(graph)
    def tamper_signature_basis(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        grounding = m["semantic_cross_audit"]["na_pair_groundings"][0]
        grounding["structural_signature_basis"]["cut_cardinality"] = 999
        grounding["structural_signature_sha256"] = object_sha256(grounding["structural_signature_basis"]); reseal_grounding(grounding)
    def collapse_same_group_rationale(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        groundings = m["semantic_cross_audit"]["na_pair_groundings"]
        first, second = groundings[0], groundings[1]
        first["nonconnection_certificate"] = copy.deepcopy(second["nonconnection_certificate"])
        reseal_grounding(first)
    def falsify_semantic_cut(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        grounding = m["semantic_cross_audit"]["na_pair_groundings"][0]
        certificate = grounding["nonconnection_certificate"]
        certificate["cut_evidence"][0]["target_absent_from_reachable_closure"] = False
        certificate["semantic_proof_signature_sha256"] = object_sha256(
            certificate_basis_from_certificate(certificate)
        )
        certificate.pop("certificate_sha256", None); certificate["certificate_sha256"] = object_sha256(certificate)
        grounding["reasoning_signature_sha256"] = certificate["semantic_proof_signature_sha256"]
        reseal_grounding(grounding)
    def collapse_all_na_explanations(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        for grounding in m["semantic_cross_audit"]["na_pair_groundings"]:
            grounding["conclusion_specific_rationale"] = "One common skeleton claims no intersection, path, or contradiction for every pair."
            reseal_grounding(grounding)
    def add_ontology_relation(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        m["semantic_cross_audit"]["semantic_concept_ontology"]["directed_edges"].append(["pointwise_causal_memory_without_work_grid", "regular_solution_binodal"])
    def remove_ontology_relation(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        m["semantic_cross_audit"]["semantic_concept_ontology"]["directed_edges"].pop(0)
    def hardcode_classification(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        graph = find_decision(m, "P059-TCL-001", "P059-CODE-001")["pair_graph_audit"]
        graph["classification_derivation"] = "PAIR_MEMBERSHIP_COMPLEMENT"
        reseal_graph(graph)
    def restore_na_complement(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        m["semantic_cross_audit"]["semantic_concept_ontology"]["classification_membership_source"] = "NA_CODE_MEMBERSHIP"
    def tamper_ontology_ref(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        graph = find_decision(m, "P059-TCL-001", "P059-CODE-001")["pair_graph_audit"]
        graph["structural_signature_basis"]["semantic_ontology_ref"]["directed_edges_sha256"] = "0" * 64
        graph["structural_signature_sha256"] = object_sha256(graph["structural_signature_basis"])
        reseal_graph(graph)
    def tamper_review_manifest(c: dict[str, Any], t: dict[str, Any], m: dict[str, Any]) -> None:
        grounding = m["semantic_cross_audit"]["na_pair_groundings"][0]
        grounding["review_checks"]["checks"][0]["evidence_sha256"] = "0" * 64
        grounding["review_checks"]["checks_sha256"] = object_sha256(grounding["review_checks"]["checks"])
        reseal_grounding(grounding)
    mutations: list[tuple[str, Callable[[dict[str, Any], dict[str, Any], dict[str, Any]], None]]] = [
        ("drop_theory_row", lambda c, t, m: m["rows"].pop()),
        ("duplicate_theory_row", lambda c, t, m: m["rows"].append(copy.deepcopy(m["rows"][0]))),
        ("orphan_claim_id", lambda c, t, m: m["rows"][0].update(claim_id="P059-TCL-999")),
        ("drop_applicable_claim_ledger", lambda c, t, m: m["applicable_claim_code_adjudications"].pop()),
        ("drop_tcl084_code011", lambda c, t, m: drop_adjudication_direct_link(m, "P059-TCL-084", "P059-CODE-011")),
        ("drop_tcl030_code006", lambda c, t, m: drop_adjudication_direct_link(m, "P059-TCL-030", "P059-CODE-006")),
        ("drop_tcl033_code010", lambda c, t, m: drop_adjudication_direct_link(m, "P059-TCL-033", "P059-CODE-010")),
        ("drop_tcl056_code010", lambda c, t, m: drop_adjudication_direct_link(m, "P059-TCL-056", "P059-CODE-010")),
        ("drop_tcl066_code005", lambda c, t, m: drop_adjudication_direct_link(m, "P059-TCL-066", "P059-CODE-005")),
        ("tcl073_code013_back_to_direct", lambda c, t, m: next(x for x in find_ledger(m, "P059-TCL-073")["code_finding_adjudications"] if x["code_finding_id"] == "P059-CODE-013").update(applicability="DIRECT")),
        ("tcl081_code010_back_to_direct", lambda c, t, m: next(x for x in find_ledger(m, "P059-TCL-081")["code_finding_adjudications"] if x["code_finding_id"] == "P059-CODE-010").update(applicability="DIRECT")),
        ("tcl179_code007_back_to_direct", lambda c, t, m: next(x for x in find_ledger(m, "P059-TCL-179")["code_finding_adjudications"] if x["code_finding_id"] == "P059-CODE-007").update(applicability="DIRECT")),
        ("tcl037_code013_back_to_na", lambda c, t, m: next(x for x in find_ledger(m, "P059-TCL-037")["code_finding_adjudications"] if x["code_finding_id"] == "P059-CODE-013").update(applicability="NOT_APPLICABLE")),
        ("tcl069_code005_back_to_na", lambda c, t, m: next(x for x in find_ledger(m, "P059-TCL-069")["code_finding_adjudications"] if x["code_finding_id"] == "P059-CODE-005").update(applicability="NOT_APPLICABLE")),
        ("tcl113_code005_back_to_na", lambda c, t, m: next(x for x in find_ledger(m, "P059-TCL-113")["code_finding_adjudications"] if x["code_finding_id"] == "P059-CODE-005").update(applicability="NOT_APPLICABLE")),
        ("drop_lco_high_risk_tcl084", drop_lco_claim),
        ("drop_lco_high_risk_tcl033", lambda c, t, m: m["high_risk_findings"][5]["claim_ids"].remove("P059-TCL-033")),
        ("drop_lco_high_risk_tcl056", lambda c, t, m: m["high_risk_findings"][5]["claim_ids"].remove("P059-TCL-056")),
        ("drop_lco_high_risk_tcl081", lambda c, t, m: m["high_risk_findings"][5]["claim_ids"].remove("P059-TCL-081")),
        ("semantic_claim_scope_tamper", lambda c, t, m: m["semantic_cross_audit"]["claim_semantic_scopes"][0].update(contract_topics=[])),
        ("claim_semantic_variable_tamper", lambda c, t, m: find_ledger(m, "P059-TCL-001")["claim_semantic_scope"].update(claim_quantity_or_dependency="generic quantity")),
        ("claim_semantic_dependency_tamper", lambda c, t, m: find_ledger(m, "P059-TCL-001")["claim_semantic_scope"].update(dependency_direction="generic dependency")),
        ("finding_scope_behavior_tamper", lambda c, t, m: m["semantic_cross_audit"]["code_finding_semantic_scopes"][0].update(actual_production_behavior="generic behavior")),
        ("finding_scope_action_tamper", lambda c, t, m: m["semantic_cross_audit"]["code_finding_semantic_scopes"][0].update(required_action="generic action")),
        ("semantic_method_tamper", lambda c, t, m: find_ledger(m, "P059-TCL-001")["code_finding_adjudications"][0].update(semantic_audit_method="CONTRACT_JOIN")),
        ("na_basis_boilerplate", lambda c, t, m: find_ledger(m, "P059-TCL-001")["code_finding_adjudications"][0].update(basis="not applicable")),
        ("na_comparison_generic_boilerplate", lambda c, t, m: find_ledger(m, "P059-TCL-001")["code_finding_adjudications"][0].update(comparison={"claim_quantity_or_dependency": "quantity", "finding_affected_quantity_or_path": "path", "overlap_or_dependency_path": "none", "classification_reason": "not applicable", "exclusion_boundary": "none"})),
        ("na_overlap_dependency_boundary_delete", lambda c, t, m: find_ledger(m, "P059-TCL-001")["code_finding_adjudications"][0]["comparison"].update(overlap_or_dependency_path="", exclusion_boundary="")),
        ("na_pair_grounding_swap", swap_na_groundings),
        ("na_pair_grounding_payload_swap_resealed", swap_na_grounding_payload),
        ("na_pair_grounding_generic_resealed", generic_na_grounding),
        ("na_grounding_group_tamper_resealed", tamper_na_group),
        ("na_grounding_source_anchor_tamper_resealed", tamper_na_source_anchor),
        ("na_grounding_reverse_link_tamper", lambda c, t, m: find_ledger(m, "P059-TCL-001")["code_finding_adjudications"][0].update(na_pair_grounding_id="P059-NA-GROUND-999-999")),
        ("tcl155_code002_back_to_na", tcl155_back_to_na),
        ("cross_domain_bridge_removal", remove_tcl155_bridge),
        ("cross_domain_bridge_addition_to_na", add_bridge_to_na),
        ("hardcoded_none_with_reachable_graph", hardcode_none_on_reachable),
        ("na_exact_quantity_delete", lambda c, t, m: delete_grounding_rationale_field(m, "claim_quantity_or_dependency")),
        ("na_exact_behavior_delete", lambda c, t, m: delete_grounding_rationale_field(m, "finding_behavior")),
        ("na_exact_non_goal_delete", lambda c, t, m: delete_grounding_rationale_field(m, "claim_non_goal")),
        ("na_exact_non_adjudicated_delete", lambda c, t, m: delete_grounding_rationale_field(m, "finding_non_adjudicated_scope")),
        ("pair_graph_edge_tamper", tamper_graph_edge),
        ("na_signature_basis_tamper", tamper_signature_basis),
        ("same_group_rationale_collapse", collapse_same_group_rationale),
        ("na_semantic_cut_falsified_resealed", falsify_semantic_cut),
        ("all_na_common_skeleton", collapse_all_na_explanations),
        ("ontology_relation_addition", add_ontology_relation),
        ("ontology_relation_removal", remove_ontology_relation),
        ("pair_ontology_content_ref_tamper", tamper_ontology_ref),
        ("na_review_manifest_hash_tamper", tamper_review_manifest),
        ("hardcoded_pair_classification", hardcode_classification),
        ("restore_na_membership_complement", restore_na_complement),
        ("artifact_link_bare_id", bare_artifact),
        ("drop_artifact_canonical_record", drop_artifact_record),
        ("governing_relation_tamper", lambda c, t, m: find_row(m, "P059-TCL-069")["theory_axis"]["governing_contract_ids"].clear()),
        ("evidence_relation_tamper", lambda c, t, m: find_row(m, "P059-TCL-069")["theory_axis"]["evidence_relation_ids"].pop()),
        ("code_link_falsify", lambda c, t, m: find_row(m, "P059-TCL-025")["production_axis"]["evidence_links"][0].update(evidence_id="P059-CODE-999")),
        ("test_link_role_falsify", lambda c, t, m: find_row(m, "P059-TCL-025")["test_runtime_axis"]["evidence_links"][0].update(role="")),
        ("link_matrix_path_plausible_nonempty_wrong", lambda c, t, m: find_row(m, "P059-TCL-001")["production_axis"]["evidence_links"][0].update(matrix_path="Codex/results/PHASE_059_TEST_DEMO_CLAIM_MATRIX.json")),
        ("link_role_plausible_nonempty_wrong", lambda c, t, m: find_row(m, "P059-TCL-001")["production_axis"]["evidence_links"][0].update(role="RELATED_STATIC_BEHAVIOR_EVIDENCE")),
        ("link_basis_plausible_nonempty_wrong", lambda c, t, m: find_row(m, "P059-TCL-001")["production_axis"]["evidence_links"][0].update(basis="Plausible but noncanonical production finding summary.")),
        ("artifact_anchor_falsify", lambda c, t, m: find_row(m, "P059-TCL-025")["stored_artifact_axis"]["evidence_links"][0].update(source_index=999)),
        ("artifact_hash_falsify", lambda c, t, m: find_row(m, "P059-TCL-025")["stored_artifact_axis"]["evidence_links"][0].update(source_record_sha256="0" * 64)),
        ("illegal_status", lambda c, t, m: m["rows"][0].update(conformance_status="PASS")),
        ("unjustified_aligned", lambda c, t, m: m["rows"][5].update(conformance_status="ALIGNED")),
        ("tcl081_status_back_to_misaligned", lambda c, t, m: find_row(m, "P059-TCL-081").update(conformance_status="MISALIGNED")),
        ("tcl179_status_back_to_misaligned", lambda c, t, m: find_row(m, "P059-TCL-179").update(conformance_status="MISALIGNED")),
        ("remove_authority", lambda c, t, m: m["rows"][0].update(authority_boundary="")),
        ("low_temp_boundary_tamper", lambda c, t, m: m["high_risk_findings"][0].update(finding="temperature checked")),
        ("chronology_boundary_tamper", lambda c, t, m: m["high_risk_findings"][1].update(finding="chronology complete")),
        ("lco_boundary_tamper", lambda c, t, m: m["high_risk_findings"][5].update(finding="LCO complete")),
        ("si_boundary_overclaim", lambda c, t, m: m["high_risk_findings"][7].update(authority_boundary="production-code absence established")),
        ("public_data_boundary_tamper", lambda c, t, m: m["high_risk_findings"][8].update(authority_boundary="validated")),
        ("count_tamper", lambda c, t, m: m["counts"].update(theory_claims=184)),
        ("baseline_tamper", lambda c, t, m: m.update(baseline_commit="0" * 40)),
        ("corpus_tamper", lambda c, t, m: m.update(input_corpus_sha256="0" * 64)),
        ("coverage_tamper", lambda c, t, m: m["input_coverage"].pop()),
        ("drop_code_record", lambda c, t, m: c["records"].pop()),
        ("drop_test_record", lambda c, t, m: t["test_runtime_records"].pop()),
        ("auxiliary_main_mismatch", lambda c, t, m: c["records"][4]["original_record"].update(title="tampered")),
        ("semantic_hash_tamper", lambda c, t, m: m["determinism"].update(semantic_sha256="0" * 64)),
    ]
    rejected = 0
    for name, mutate in mutations:
        code, test, main = copy.deepcopy(base_code), copy.deepcopy(base_test), copy.deepcopy(base_main)
        mutate(code, test, main)
        if name != "semantic_hash_tamper": seal(code); seal(test); seal(main)
        try: validate_documents(code, test, main)
        except ValidationFailure as exc: rejected += 1; print(f"{name}: REJECTED ({exc})")
        else: raise ValidationFailure(f"{name}: UNEXPECTED_PASS")
    print(f"PASS_NEGATIVE_MUTATION_PROBES rejected={rejected}")


def run_focused_evidence_link_probes() -> None:
    """Reject plausible nonempty link metadata without using document locks."""
    code = load_output(CODE_PATH)
    main = load_output(MAIN_PATH)
    universe = {record["record_id"]: record for record in code["records"]}
    canonical = copy.deepcopy(find_row(main, "P059-TCL-001")["production_axis"]["evidence_links"][0])
    mutations = {
        "matrix_path": "records[0]",
        "role": "Plausible but wrong production-evidence role.",
        "basis": "Plausible but wrong canonical-record interpretation.",
    }
    accepted = []
    for field, wrong_value in mutations.items():
        link = copy.deepcopy(canonical)
        link[field] = wrong_value
        try:
            validate_link(link, "CODE", universe, AXIS_ROLE_BY_CLASS["CODE"])
        except ValidationFailure:
            continue
        accepted.append(field)
    if accepted:
        raise ValidationFailure("FOCUSED_EVIDENCE_LINK_RED accepted plausible nonempty wrong fields: " + ",".join(accepted))
    print("PASS_FOCUSED_EVIDENCE_LINK_PROBES rejected=3 before_semantic_lock=true")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--run-focused-evidence-link-probes", action="store_true")
    args = parser.parse_args()
    try:
        if args.run_focused_evidence_link_probes:
            run_focused_evidence_link_probes()
            return 0
        validate_paths()
        if args.run_negative_probes: run_negative_probes()
    except ValidationFailure as exc:
        print(f"FAIL_P059_STEP_039_3_FOUR_AXIS_CONFORMANCE: {exc}", file=sys.stderr); return 1
    print("PASS_P059_STEP_039_3_FOUR_AXIS_CONFORMANCE rows=185 code_records=21 test_runtime_records=103 artifact_records=152 adjudications=663")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
