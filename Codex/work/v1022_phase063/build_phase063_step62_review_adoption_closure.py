#!/usr/bin/env python3
"""Build deterministic Phase 063 Step 62 review/adoption/build/state evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import posixpath
import re
import subprocess
from collections import Counter
from typing import Any


REPO = pathlib.Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PARENT = "89bd7c7c27a827ec2322db25fe9e2634874c2f9d"
MATRIX = "Codex/results/PHASE_063_V1022_REVIEW_ADOPTION_CLOSURE_MATRIX.json"
RESULT = "Codex/results/PHASE_063_STEP_062_REVIEW_ADOPTION_CLOSURE_RESULT.md"
GATE = "PASS_P063_STEP62_REVIEW_ADOPTION_CLOSURE_WITH_CONCERNS"
SENTINEL = "P063_STEP62_RESULT_FIRST_PRECOMMIT"


FAMILY_RANGES = (
    (77, 80, "COMP_AUD"),
    (81, 103, "FR_REPORT_A01_A23"),
    (104, 111, "FR_CONTROL_TRIAGE_EXEC"),
    (112, 116, "R2_A_SEAMS"),
    (117, 119, "R2_CONTROL"),
    (120, 130, "R2_B_BRIDGES"),
    (131, 131, "R2_CONTROL"),
    (132, 134, "R2_C_STATMECH"),
    (135, 137, "R3_CONTROL"),
    (138, 140, "R3_D_SEAMS"),
    (141, 148, "R3_E_BRIDGES"),
    (149, 155, "R4_SURVEY"),
    (156, 159, "R4_UPGRADED"),
    (160, 161, "R5_CONTROL"),
    (162, 168, "R5_W1"),
    (169, 175, "R5_W2"),
    (176, 182, "R5_W3"),
    (183, 183, "COMP_R6"),
    (184, 187, "COMP_R7"),
    (188, 188, "COMP_R8"),
    (189, 191, "COMP_RV"),
    (192, 196, "COMP_SM2"),
    (197, 201, "COMP_V23"),
)
FAMILY_DECISIONS = {
    "COMP_AUD": "REVIEW_FINDINGS_PARTIAL_SOURCE_CORRECTION_C056",
    "FR_REPORT_A01_A23": "PARTIAL_ADOPTION_H_AND_CORRECTION_M_ONLY",
    "FR_CONTROL_TRIAGE_EXEC": "DECISION_EXECUTION_AND_DEFER_RECORD",
    "R2_A_SEAMS": "PARTIAL_ADOPTION_WITH_PRESERVED_ALTERNATIVES",
    "R2_CONTROL": "CHERRYPICK_DECISION_AND_BRIEF_CONTROL",
    "R2_B_BRIDGES": "PARTIAL_ADOPTION_WITH_MERGE_AND_TRIM",
    "R2_C_STATMECH": "PARTIAL_ADOPTION_CLT_BOX_AND_CNT_LINK",
    "R3_CONTROL": "CHERRYPICK_DECISION_AND_BRIEF_CONTROL",
    "R3_D_SEAMS": "PARTIAL_ADOPTION",
    "R3_E_BRIDGES": "PARTIAL_ADOPTION_FOUR_BRIDGES_L5_UNVERIFIED",
    "R4_SURVEY": "LITERATURE_EVIDENCE_USED_NO_WHOLESALE_SOURCE_ADOPTION",
    "R4_UPGRADED": "LITERATURE_EVIDENCE_USED_NO_WHOLESALE_SOURCE_ADOPTION",
    "R5_CONTROL": "SECTION_LEVEL_CHERRYPICK_DECISION",
    "R5_W1": "PARTIAL_SECTION_ADOPTION",
    "R5_W2": "PARTIAL_SECTION_ADOPTION",
    "R5_W3": "PARTIAL_SECTION_ADOPTION",
    "COMP_R6": "HISTORICAL_SELF_REPORT_WITH_SEPARATE_CODE_PATCH",
    "COMP_R7": "PARTIAL_FIGURE_ADOPTION_REVIEWER_VOTE_GROUND_NOT_FOUND",
    "COMP_R8": "HISTORICAL_EXECUTION_RECORD_WITH_SKIP_SET",
    "COMP_RV": "PARTIAL_REVIEW_CORRECTION_ROUTE",
    "COMP_SM2": "PARTIAL_ADOPTION_REVIEWER_VOTE_GROUND_NOT_FOUND",
    "COMP_V23": "NOT_ADOPTED_IN_FROZEN_V1022_REVIEWER_VOTE_GROUND_NOT_FOUND",
}

# Full-text P-Z adjudication, cross-checked against frozen final source and commits.
_FINDING_STATE_GROUPS = {
    "RESOLVED_IN_V1022": {131, 141, 145, 146, 147, 158, 160, 165},
    "OPEN": {101, 103, 104, 111, 114, 115, 118, 119, 126, 127, 130, 133, 134, 135, 136, 137, 138, 139, 142, 148, 150, 151, 153, 155, 156, 157, 159, 161, 162, 163, 166, 167, 168, 169, 170, 171, 172, 177, 179, 183, 184, 185, 186, 190, 191},
    "SUPERSEDED": {108, 180},
    "HISTORICAL_ONLY": {96, 97, 98, 99, 100, 102, 105, 106, 107, 109, 110, 113, 116, 117, 124, 125, 140, 143, 144, 154, 164, 174, 175, 176, 178, 181, 182, 187, 188, 189},
    "UNVERIFIED": {112, 120, 121, 122, 123, 128, 129, 132, 149, 152, 173},
}
FINDING_STATES = {
    number: state
    for state, numbers in _FINDING_STATE_GROUPS.items()
    for number in numbers
}
CURRENT_STATE_EVIDENCE = {
    101: [("P063-SRC-0048", 8, 8, "5eab7ad2a40780bb8481f1d6301c75dcea1845b4"), ("P063-SRC-0051", 78, 84, "5eab7ad2a40780bb8481f1d6301c75dcea1845b4")],
    127: [("P063-SRC-0051", 78, 84, "5eab7ad2a40780bb8481f1d6301c75dcea1845b4")],
    131: [("P063-SRC-0050", 55, 65, "72522563ebdf9040f8cb55ca4b6bdf1eabd0a898")],
    136: [("P063-SRC-0051", 78, 84, "5eab7ad2a40780bb8481f1d6301c75dcea1845b4")],
    141: [("P063-SRC-0010", 388, 409, "8637c56df7f0bed1ef0149963a500764aa00fab7"), ("P063-SRC-0014", 38, 76, "730fcb1857cd5d650372b70050780f8f32c672a8"), ("P063-SRC-0039", 75, 95, "8637c56df7f0bed1ef0149963a500764aa00fab7")],
    145: [("P063-SRC-0010", 309, 316, "92213f94ca986ce90616a6b3d5fe3a0cce995ff0")],
    146: [("P063-SRC-0013", 112, 116, "b1a985c27912f354744986e310a98b3f1982336d")],
    147: [("P063-SRC-0014", 38, 76, "730fcb1857cd5d650372b70050780f8f32c672a8")],
    158: [("P063-SRC-0016", 24, 35, "70fd87ffc918e26b7cddf0d15ea7b6edb5667203"), ("P063-SRC-0016", 64, 85, "70fd87ffc918e26b7cddf0d15ea7b6edb5667203")],
    160: [("P063-SRC-0036", 51, 58, "1519c64f9c9b2ba104dc39947b8a3ad1ad7c7f2c")],
    165: [("P063-SRC-0023", 350, 387, "5d2f60ffef02d191b32418d6e7d8acd029ac62e7")],
    169: [("P063-SRC-0048", 8, 8, "5eab7ad2a40780bb8481f1d6301c75dcea1845b4"), ("P063-SRC-0051", 78, 84, "5eab7ad2a40780bb8481f1d6301c75dcea1845b4")],
    183: [("P063-SRC-0001", 1083, 1087, "e40c29064cbd459ab20fc32731397f11931ab552"), ("P063-SRC-0001", 1297, 1319, "e40c29064cbd459ab20fc32731397f11931ab552"), ("P063-SRC-0053", 55, 60, "72522563ebdf9040f8cb55ca4b6bdf1eabd0a898")],
    184: [("P063-SRC-0001", 990, 1024, "e40c29064cbd459ab20fc32731397f11931ab552"), ("P063-SRC-0001", 1149, 1157, "e40c29064cbd459ab20fc32731397f11931ab552"), ("P063-SRC-0050", 113, 150, "72522563ebdf9040f8cb55ca4b6bdf1eabd0a898")],
    186: [("P063-SRC-0050", 138, 153, "6c13a4ea182612c7103142ea1db2f75f7c82bcc9"), ("P063-SRC-0051", 205, 222, "6c13a4ea182612c7103142ea1db2f75f7c82bcc9")],
}
ADOPTION_ROUTES: list[dict[str, Any]] = [
    {
        "route_id": "P063-S62-ADOPT-000",
        "finding_ids": ["INTENT-PROV-0101", "INTENT-PROV-0127", "INTENT-PROV-0136", "INTENT-PROV-0165", "INTENT-PROV-0169"],
        "review_sources": ["P063-SRC-0077", "P063-SRC-0078", "P063-SRC-0079", "P063-SRC-0080"],
        "proposal_sources": [],
        "decision_sources": [],
        "patch_commits": ["5eab7ad2a40780bb8481f1d6301c75dcea1845b4"],
        "final_source_edges": [],
        "infer_final_source_edges": True,
        "decision": "PARTIAL_C056_SOURCE_CORRECTION_WITHOUT_SEPARATE_DIRECT_DECISION_RECORD",
        "decision_evidence_state": "GROUND_NOT_FOUND_REPOSITORY_REPORTED_ONLY",
        "verification_only_sources": ["P063-SRC-0080"],
        "authority_ceiling": "INTERNAL_REVIEW_PATCH_AND_BUILD_VERIFICATION_ONLY",
    },
    {
        "route_id": "P063-S62-ADOPT-001",
        "finding_ids": ["INTENT-PROV-0101", "INTENT-PROV-0127", "INTENT-PROV-0136", "INTENT-PROV-0169"],
        "proposal_sources": ["P063-SRC-0101"],
        "decision_sources": [],
        "patch_commits": ["5667879b9973e3ff77fba2af43550270e2f80919", "68b396e22821d935431b49ec54707fc693ff171d", "5eab7ad2a40780bb8481f1d6301c75dcea1845b4"],
        "final_source_edges": [
            {"source_id": "P063-SRC-0047", "path": "Claude/docs/v1.0.22/_sections/ch3v22_notation.tex"},
            {"source_id": "P063-SRC-0048", "path": "Claude/docs/v1.0.22/_sections/ch3v22_sec00_intro.tex"},
            {"source_id": "P063-SRC-0050", "path": "Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex"},
            {"source_id": "P063-SRC-0051", "path": "Claude/docs/v1.0.22/_sections/ch3v22_sec03_blend.tex"},
            {"source_id": "P063-SRC-0053", "path": "Claude/docs/v1.0.22/_sections/ch3v22_sec05_code.tex"},
        ],
        "decision": "SOURCE_PATCH_EXISTS_WITH_LATE_SCOPE_CORRECTION_DIRECT_USER_DECISION_NOT_RECOVERED",
        "decision_evidence_state": "GROUND_NOT_FOUND_REPOSITORY_REPORTED_ONLY",
        "authority_ceiling": "INTERNAL_SOURCE_ADOPTION_ONLY",
    },
    {
        "route_id": "P063-S62-ADOPT-002",
        "finding_ids": ["INTENT-PROV-0131"],
        "proposal_sources": ["P063-SRC-0172"],
        "decision_sources": ["P063-SRC-0161"],
        "patch_commits": ["72522563ebdf9040f8cb55ca4b6bdf1eabd0a898"],
        "final_source_edges": [{"source_id": "P063-SRC-0050", "path": "Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex"}],
        "decision": "ADOPTED_AS_FIRST_CYCLE_IRREVERSIBLE_CASE_PROPERTY_SEPARATE_FROM_EQUILIBRIUM_TRANSITION_LIST",
        "decision_evidence_state": "DIRECT",
        "authority_ceiling": "INTERNAL_SOURCE_ADOPTION_WITH_LITERATURE_QUANTITY_CEILING",
    },
    {
        "route_id": "P063-S62-ADOPT-003",
        "finding_ids": ["INTENT-PROV-0141", "INTENT-PROV-0147"],
        "proposal_sources": ["P063-SRC-0192", "P063-SRC-0193", "P063-SRC-0194"],
        "review_sources": ["P063-SRC-0195", "P063-SRC-0196"],
        "decision_sources": [],
        "patch_commits": ["8637c56df7f0bed1ef0149963a500764aa00fab7", "730fcb1857cd5d650372b70050780f8f32c672a8"],
        "final_source_edges": [
            {"source_id": "P063-SRC-0010", "path": "Claude/docs/v1.0.22/_sections/ch1_sec02b_part0.tex"},
            {"source_id": "P063-SRC-0014", "path": "Claude/docs/v1.0.22/_sections/ch1_sec06_eqpeak.tex"},
            {"source_id": "P063-SRC-0039", "path": "Claude/docs/v1.0.22/_sections/ch2_sec07_revheat.tex"},
        ],
        "decision": "SOURCE_PATCH_EXISTS_AND_LATE_GUARD_CORRECTED_REVIEWER_DECISION_GROUND_NOT_FOUND",
        "decision_evidence_state": "GROUND_NOT_FOUND",
        "authority_ceiling": "INTERNAL_DERIVATION_ONLY",
        "reviewer_vote_state": "GROUND_NOT_FOUND_NO_INDIVIDUAL_VOTE",
    },
    {
        "route_id": "P063-S62-ADOPT-004",
        "finding_ids": ["INTENT-PROV-0146"],
        "proposal_sources": ["P063-SRC-0086"],
        "decision_sources": ["P063-SRC-0109"],
        "patch_commits": ["b1a985c27912f354744986e310a98b3f1982336d"],
        "final_source_edges": [{"source_id": "P063-SRC-0013", "path": "Claude/docs/v1.0.22/_sections/ch1_sec05_width.tex"}],
        "decision": "ADOPTED_TST_CLASSICAL_LIMIT_CORRECTION",
        "decision_evidence_state": "DIRECT",
        "authority_ceiling": "INTERNAL_DERIVATION_ONLY",
    },
    {
        "route_id": "P063-S62-ADOPT-005",
        "finding_ids": ["INTENT-PROV-0158"],
        "proposal_sources": ["P063-SRC-0089"],
        "decision_sources": ["P063-SRC-0109"],
        "patch_commits": ["70fd87ffc918e26b7cddf0d15ea7b6edb5667203"],
        "final_source_edges": [{"source_id": "P063-SRC-0016", "path": "Claude/docs/v1.0.22/_sections/ch1_sec08_lag.tex"}],
        "decision": "ADOPTED_BARRIER_ACCOUNTING_CORRECTION",
        "decision_evidence_state": "DIRECT",
        "authority_ceiling": "INTERNAL_DERIVATION_ONLY",
    },
    {
        "route_id": "P063-S62-ADOPT-006",
        "finding_ids": ["INTENT-PROV-0165"],
        "proposal_sources": ["P063-SRC-0097", "P063-SRC-0099"],
        "decision_sources": ["P063-SRC-0109"],
        "patch_commits": ["5d2f60ffef02d191b32418d6e7d8acd029ac62e7", "5eab7ad2a40780bb8481f1d6301c75dcea1845b4"],
        "final_source_edges": [{"source_id": "P063-SRC-0023", "path": "Claude/docs/v1.0.22/_sections/ch1_sec15_lcoelec.tex"}],
        "decision": "ADOPTED_LCO_COORDINATE_CORRECTION",
        "decision_evidence_state": "DIRECT",
        "authority_ceiling": "INTERNAL_DERIVATION_AND_FROZEN_IMPLEMENTATION_CONCORDANCE",
    },
    {
        "route_id": "P063-S62-ADOPT-007",
        "finding_ids": ["INTENT-PROV-0186"],
        "proposal_sources": ["P063-SRC-0184", "P063-SRC-0185", "P063-SRC-0186", "P063-SRC-0187"],
        "change_record_sources": ["P063-SRC-0074"],
        "decision_sources": [],
        "patch_commits": ["6c13a4ea182612c7103142ea1db2f75f7c82bcc9"],
        "final_source_edges": [
            {"source_id": "P063-SRC-0050", "path": "Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex"},
            {"source_id": "P063-SRC-0051", "path": "Claude/docs/v1.0.22/_sections/ch3v22_sec03_blend.tex"},
        ],
        "decision": "SOURCE_PATCH_EXISTS_AS_SCHEMATIC_INTERNAL_CODE_PROJECTION_NOT_EXPERIMENT_REVIEWER_DECISION_GROUND_NOT_FOUND",
        "decision_evidence_state": "GROUND_NOT_FOUND",
        "authority_ceiling": "INTERNAL_VISUAL_REGRESSION_ONLY",
        "reviewer_vote_state": "GROUND_NOT_FOUND_NO_INDIVIDUAL_VOTE",
    },
    {
        "route_id": "P063-S62-ADOPT-008",
        "finding_ids": ["INTENT-PROV-0145"],
        "proposal_sources": ["P063-SRC-0083"],
        "decision_sources": ["P063-SRC-0105", "P063-SRC-0110"],
        "patch_commits": ["92213f94ca986ce90616a6b3d5fe3a0cce995ff0"],
        "final_source_edges": [{"source_id": "P063-SRC-0010", "path": "Claude/docs/v1.0.22/_sections/ch1_sec02b_part0.tex"}],
        "decision": "ADOPTED_MEAN_FIELD_VERSUS_INDEPENDENT_SITE_FORM_BOUNDARY",
        "decision_evidence_state": "DIRECT",
        "authority_ceiling": "INTERNAL_DERIVATION_ONLY",
    },
    {
        "route_id": "P063-S62-ADOPT-009",
        "finding_ids": ["INTENT-PROV-0160"],
        "proposal_sources": ["P063-SRC-0092", "P063-SRC-0093"],
        "decision_sources": ["P063-SRC-0109"],
        "patch_commits": ["1519c64f9c9b2ba104dc39947b8a3ad1ad7c7f2c"],
        "final_source_edges": [{"source_id": "P063-SRC-0036", "path": "Claude/docs/v1.0.22/_sections/ch2_sec04_einstein.tex"}],
        "decision": "ADOPTED_ONE_MODE_SCOPE_AND_SIGNED_GENERALIZATION_BOUNDARY",
        "decision_evidence_state": "DIRECT",
        "authority_ceiling": "INTERNAL_DERIVATION_ONLY",
    },
    {
        "route_id": "P063-S62-CHAIN-008",
        "finding_ids": [f"INTENT-PROV-{number:04d}" for number in (144, 154, 164, 176, 177, 178, 179, 180, 181, 182)],
        "proposal_sources": [f"P063-SRC-{number:04d}" for number in range(81, 104)],
        "decision_sources": [f"P063-SRC-{number:04d}" for number in range(104, 112)],
        "patch_commits": [
            "0fdb15b9ced589bbca57d980347c61c6acf8b662", "640aa7c7bc75b6e0ba8758a7a3ff420b2a7bda4d",
            "7f9d0db7ce5fd2d8158d951a95c74ff86de25534", "730fcb1857cd5d650372b70050780f8f32c672a8",
            "70fd87ffc918e26b7cddf0d15ea7b6edb5667203", "1519c64f9c9b2ba104dc39947b8a3ad1ad7c7f2c",
            "b1a985c27912f354744986e310a98b3f1982336d", "bba778811ce2092b43b253abfdfd0538f2b2c754",
            "5d2f60ffef02d191b32418d6e7d8acd029ac62e7", "50bbb172169ff1fa75de275c2e721fc9831e684d",
            "9fecfa9f25bb6c04f4cdb81d2e8ace8fcea4ca5c", "92213f94ca986ce90616a6b3d5fe3a0cce995ff0",
            "d183deffee5ede0ae480d909d5ddcd5bc6fc7cee",
            "b3e1cc72e73b3ee3fa1fa777f826ee87efe7472e", "5667879b9973e3ff77fba2af43550270e2f80919",
        ],
        "final_source_edges": [],
        "infer_final_source_edges": True,
        "decision": "PARTIAL_ADOPTION_H29_AND_CORRECTION_M41_DEFER_M158_L_APPROX120_SKIP13",
        "authority_ceiling": "INTERNAL_PATCH_AND_PROCESS_ACCOUNTING_ONLY",
    },
    {
        "route_id": "P063-S62-CHAIN-009",
        "finding_ids": [f"INTENT-PROV-{number:04d}" for number in range(111, 118)],
        "proposal_sources": [f"P063-SRC-{number:04d}" for number in range(112, 135)],
        "decision_sources": ["P063-SRC-0131"],
        "patch_commits": ["2a16148eddcde3617d387efe866282fb2f0a3222"],
        "final_source_edges": [],
        "infer_final_source_edges": True,
        "decision": "PARTIAL_ADOPTION_CLT_BOX_CNT_LINK_EIGHT_BRIDGES_WITH_MERGE_TRIM_AND_REJECTION",
        "authority_ceiling": "INTERNAL_SOURCE_ADOPTION_PRIMARY_EQUATIONS_PARTLY_UNVERIFIED",
    },
    {
        "route_id": "P063-S62-CHAIN-010",
        "finding_ids": [f"INTENT-PROV-{number:04d}" for number in range(118, 125)],
        "proposal_sources": [f"P063-SRC-{number:04d}" for number in range(135, 149)],
        "decision_sources": ["P063-SRC-0137"],
        "patch_commits": ["f33918d3bea6f57ef434a5612f1fb5b7166fc764"],
        "final_source_edges": [],
        "infer_final_source_edges": True,
        "decision": "PARTIAL_ADOPTION_FOUR_LCO_BRIDGES_L5_VALUES_REMAIN_TIER_C_UNVERIFIED",
        "authority_ceiling": "INTERNAL_SOURCE_ADOPTION_PRIMARY_QUANTITIES_UNVERIFIED",
    },
    {
        "route_id": "P063-S62-CHAIN-011",
        "finding_ids": [f"INTENT-PROV-{number:04d}" for number in range(125, 134)],
        "proposal_sources": [f"P063-SRC-{number:04d}" for number in range(149, 160)],
        "decision_sources": ["P063-SRC-0161", "P063-SRC-0076"],
        "patch_commits": ["72522563ebdf9040f8cb55ca4b6bdf1eabd0a898"],
        "final_source_edges": [],
        "infer_final_source_edges": True,
        "decision": "EVIDENCE_SEEDS_PARTIALLY_USED_WITHOUT_DATASET_OR_MATERIAL_TRUTH_PROMOTION",
        "authority_ceiling": "LITERATURE_CANDIDATE_AND_INTERNAL_SOURCE_ONLY",
    },
    {
        "route_id": "P063-S62-CHAIN-012",
        "finding_ids": [f"INTENT-PROV-{number:04d}" for number in range(134, 140)],
        "proposal_sources": [f"P063-SRC-{number:04d}" for number in range(160, 183)],
        "decision_sources": ["P063-SRC-0161"],
        "patch_commits": ["72522563ebdf9040f8cb55ca4b6bdf1eabd0a898"],
        "final_source_edges": [],
        "infer_final_source_edges": True,
        "decision": "SECTION_LEVEL_CHERRYPICK_W3_W2_W1_PLUS_W3_W1_W3_WITH_REMAINDER_NONADOPTED",
        "authority_ceiling": "INTERNAL_SOURCE_ADOPTION_ONLY",
    },
    {
        "route_id": "P063-S62-CHAIN-013",
        "finding_ids": ["INTENT-PROV-0183", "INTENT-PROV-0184", "INTENT-PROV-0185"],
        "proposal_sources": ["P063-SRC-0183"],
        "decision_sources": ["P063-SRC-0075"],
        "patch_commits": ["e40c29064cbd459ab20fc32731397f11931ab552"],
        "final_source_edges": [],
        "infer_final_source_edges": True,
        "decision": "IMPLEMENTED_TO_FROZEN_SPEC_WITH_OPEN_FINITE_RATE_AND_MATERIAL_BOUNDARIES",
        "authority_ceiling": "FROZEN_IMPLEMENTATION_ONLY",
    },
    {
        "route_id": "P063-S62-CHAIN-014",
        "finding_ids": ["INTENT-PROV-0140", "INTENT-PROV-0142"],
        "proposal_sources": ["P063-SRC-0189", "P063-SRC-0190", "P063-SRC-0191"],
        "decision_sources": ["P063-SRC-0074"],
        "patch_commits": ["3db9b5d2aa80f75378a7fa66f84ad3d59c3e9ce4"],
        "final_source_edges": [],
        "infer_final_source_edges": True,
        "decision": "PARTIAL_REVIEW_CORRECTIONS_WITH_REMAINDER_ROUTED",
        "authority_ceiling": "INTERNAL_REVIEW_AND_SOURCE_PATCH_ONLY",
    },
    {
        "route_id": "P063-S62-CHAIN-014B",
        "finding_ids": ["INTENT-PROV-0188"],
        "status_sources": ["P063-SRC-0188"],
        "proposal_sources": [],
        "decision_sources": [],
        "patch_commits": ["f816385dd6055ef2f4afc18b9812f902f6ee9389"],
        "final_source_edges": [],
        "infer_final_source_edges": True,
        "decision": "EXECUTION_STATUS_REPORTS_FOURTEEN_PATCHED_SIX_PRE_RESOLVED_TWENTY_ONE_SKIPPED_WITHOUT_SEPARATE_DIRECT_DECISION_RECORD",
        "decision_evidence_state": "GROUND_NOT_FOUND_REPOSITORY_REPORTED_ONLY",
        "authority_ceiling": "INTERNAL_STATUS_AND_SOURCE_PATCH_ONLY",
    },
    {
        "route_id": "P063-S62-CHAIN-015",
        "finding_ids": ["INTENT-PROV-0188", "INTENT-PROV-0189"],
        "proposal_sources": [f"P063-SRC-{number:04d}" for number in range(197, 202)],
        "decision_sources": [],
        "patch_commits": [],
        "final_source_edges": [],
        "decision": "NOT_ADOPTED_IN_FROZEN_V1022",
        "authority_ceiling": "PROPOSAL_SURVEY_ONLY",
        "reviewer_vote_state": "GROUND_NOT_FOUND_NO_INDIVIDUAL_VOTE",
    },
]
BUILD_ROWS: list[dict[str, Any]] = [
    {
        "driver": "appendix_phase_separation.tex", "root_source_id": "P063-SRC-0056", "root_blob": "4e17bf01a5a1eb71476e6112d6a26b96861b17f5", "pdf_source_id": "P063-SRC-0055",
        "engine": "MiKTeX-XeTeX 4.16 (MiKTeX 25.12)", "passes": 3, "exit_codes": [0, 0, 0], "expected_pages": 8, "built_pages": 8, "frozen_pages": 8,
        "undefined_refs": 0, "undefined_citations": 0, "multiply_defined_labels": [], "missing_glyphs": [],
        "frozen_pdf_sha256": "8d89cdf9fb803c7a06c6fbcf2c59899162705baf30a93b601ca0bebaacbce7aa", "built_pdf_sha256": "8f6699b369cce5e89b4dad4501a6a06afe58ce8c122054a2cf0aae3bcec7b725", "raw_pdf_equal": False,
        "text_sha256": "09294bbeb06765ce332e547be60615cba1c5d14ca8f1fd5b970ff12f712cd0bd", "text_equal": True, "text_pages_equal": "8/8", "render_exact": "8/8", "render_diff_pages": [],
    },
    {
        "driver": "ch1_graphite_v1.0.22.tex", "root_source_id": "P063-SRC-0058", "root_blob": "c67f8aab1e71aa708864c0603f737a844d3daf45", "pdf_source_id": "P063-SRC-0057",
        "engine": "MiKTeX-XeTeX 4.16 (MiKTeX 25.12)", "passes": 3, "exit_codes": [0, 0, 0], "expected_pages": 83, "built_pages": 83, "frozen_pages": 83,
        "undefined_refs": 0, "undefined_citations": 0, "multiply_defined_labels": ["swiderska2019", "LastPage"], "missing_glyphs": [],
        "frozen_pdf_sha256": "f4068a043dbaa712d462fd4cb3e8288d8e1d3a5bd02c13e5cfb0aa8bce17daa0", "built_pdf_sha256": "79d791a8f79e652031bbfefbf7ce66907e668bfd8fe529d0f6aa0832bd98d9e8", "raw_pdf_equal": False,
        "text_sha256": "2cf7f3bdf7c07d56491c2911e6fecdf8bf6d5abdbc18b530f6f3f925ee3fce0d", "text_equal": True, "text_pages_equal": "83/83", "render_exact": "80/83", "render_diff_pages": [39, 64, 83],
    },
    {
        "driver": "ch2_lco_v1.0.22.tex", "root_source_id": "P063-SRC-0060", "root_blob": "7c31f2d7b22b32b99acdd7852d914fe435331cfb", "pdf_source_id": "P063-SRC-0059",
        "engine": "MiKTeX-XeTeX 4.16 (MiKTeX 25.12)", "passes": 3, "exit_codes": [0, 0, 0], "expected_pages": 25, "built_pages": 25, "frozen_pages": 25,
        "undefined_refs": 0, "undefined_citations": 0, "multiply_defined_labels": ["swiderska2019", "LastPage"], "missing_glyphs": [],
        "frozen_pdf_sha256": "799812d0e43e3359eefb3a6fc575c665572f04eb48848340e28be59662d3ad9f", "built_pdf_sha256": "af1fe3bcf0c90d556aced5158503c8f90c8348556262fa9247773a504370f265", "raw_pdf_equal": False,
        "text_sha256": "00d5f9e30f72540eb323413f34a397010176b2beb3e0cadb87da94ba3d7994cb", "text_equal": True, "text_pages_equal": "25/25", "render_exact": "22/25", "render_diff_pages": [5, 14, 15],
    },
    {
        "driver": "ch3_si_v1.0.22.tex", "root_source_id": "P063-SRC-0062", "root_blob": "5810298ed59229f2b2410bc98da6be8e2a873b73", "pdf_source_id": "P063-SRC-0061",
        "engine": "MiKTeX-XeTeX 4.16 (MiKTeX 25.12)", "passes": 3, "exit_codes": [0, 0, 0], "expected_pages": 17, "built_pages": 17, "frozen_pages": 17,
        "undefined_refs": 0, "undefined_citations": 0, "multiply_defined_labels": ["swiderska2019", "LastPage"],
        "missing_glyphs": [{"char": "μ", "count": 2, "log_lines": [1226, 1227], "source_path": "Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex", "source_blob": "ea88ed0730bb8cbc5f48cd3cacc42fab93f88ded", "source_lines": [70, 73], "pdf_page": 7, "frozen_and_built_loss": True}],
        "frozen_pdf_sha256": "8c9da9fbc6e5f4567b01f994988e16ca84ea78365f0c8ea8056934a22d2f03fb", "built_pdf_sha256": "2dc3e9f78bb6b7c5a40160fdaad337814d2c82f2dd44ff98a38f26310994f695", "raw_pdf_equal": False,
        "text_sha256": "3fd66b145d2654a5662d853094710e6fa6aec0012aa3f11ce23e51fba06b451f", "text_equal": True, "text_pages_equal": "17/17", "render_exact": "15/17", "render_diff_pages": [5, 13],
    },
]
BUILD_EXECUTION: dict[str, Any] = {
    "host_environment": {
        "os": "Microsoft Windows NT 10.0.26200.0",
        "powershell": "7.6.5",
        "git": "2.53.0.windows.2",
        "xelatex": "MiKTeX-XeTeX 4.16 (MiKTeX 25.12)",
        "poppler": "26.05.0",
        "render_dpi": 96,
        "pixel_decoder": "Pillow RGB exact comparison",
    },
    "materialization_algorithm": [
        "git ls-tree -rz --full-tree <baseline> -- Claude/docs/v1.0.22",
        "for each manifest entry: git cat-file blob <oid> > exact relative path bytes",
        "verify every materialized path SHA-1 against its Git object before build",
    ],
    "working_directory": "<external-temp>/Claude/docs/v1.0.22",
    "driver_order": [row["driver"] for row in BUILD_ROWS],
    "run_order": [
        {"round": round_number, "driver": row["driver"]}
        for round_number in range(1, 4)
        for row in BUILD_ROWS
    ],
    "build_command_argv": ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "<driver>"],
    "page_count_command_argv": ["pdfinfo", "<pdf>"],
    "text_command_argv": ["pdftotext", "-layout", "<pdf>", "-"],
    "page_text_command_argv": ["pdftotext", "-layout", "-f", "<page>", "-l", "<page>", "<pdf>", "-"],
    "render_command_argv": ["pdftoppm", "-png", "-r", "96", "<pdf>", "<output-prefix>"],
    "cleanup_required": True,
    "frozen_producer": "xdvipdfmx (20220710)",
    "frozen_pdf_version": "1.5",
    "rebuilt_producer": "MiKTeX-dvipdfmx (20250413)",
    "rebuilt_pdf_version": "1.7",
}
BUILD_LOG_DIAGNOSTICS: list[dict[str, Any]] = [
    {
        "driver": "appendix_phase_separation.tex",
        "log_sha256": "183700cb4a40d92e1b31b4f444af52d181b21ce152a63cdba74b58e8dabe21f2",
        "log_lines": 1033,
        "multiply_defined_label_log_lines": [],
        "missing_character_log_lines": [],
        "overfull_hbox_log_lines": [],
        "overfull_vbox_log_lines": [],
        "infinite_glue_log_lines": [],
        "font_shape_summary_log_lines": [1018],
    },
    {
        "driver": "ch1_graphite_v1.0.22.tex",
        "log_sha256": "ced48fbb49b8f7e9e53c4fe80301d99c5b13832c710ffd4307aac43984ccded4",
        "log_lines": 2035,
        "multiply_defined_label_log_lines": [929, 932],
        "missing_character_log_lines": [],
        "overfull_hbox_log_lines": [1139, 1482, 1525, 1590, 1650, 1751, 1886, 1891, 1902, 1946],
        "overfull_vbox_log_lines": [],
        "infinite_glue_log_lines": [1144, 1146, 1881, 1913, 1954],
        "font_shape_summary_log_lines": [2018],
    },
    {
        "driver": "ch2_lco_v1.0.22.tex",
        "log_sha256": "29f64af94a3ebb6b6fe8ea83b866b82832b5bb592658f1f4d4defce6b1755732",
        "log_lines": 1376,
        "multiply_defined_label_log_lines": [930, 933],
        "missing_character_log_lines": [],
        "overfull_hbox_log_lines": [1256, 1275, 1280],
        "overfull_vbox_log_lines": [],
        "infinite_glue_log_lines": [],
        "font_shape_summary_log_lines": [1359],
    },
    {
        "driver": "ch3_si_v1.0.22.tex",
        "log_sha256": "01ff62a8290e2a6306c5b1428d3d4c7ab4b5d254f0a3b13406e485fefd5733f4",
        "log_lines": 1346,
        "multiply_defined_label_log_lines": [931, 935],
        "missing_character_log_lines": [1226, 1227],
        "overfull_hbox_log_lines": [1199, 1204, 1209],
        "overfull_vbox_log_lines": [1246],
        "infinite_glue_log_lines": [],
        "font_shape_summary_log_lines": [1329],
    },
]
RENDER_DIFFERENCES: list[dict[str, Any]] = [
    {"driver": "ch1_graphite_v1.0.22.tex", "page": 39, "width": 794, "height": 1123, "changed_pixels": 722, "total_pixels": 891662, "changed_pixel_fraction": 0.0008097238639753629, "changed_pixel_percent": 0.08097238639753629, "bbox": [244, 888, 552, 906], "frozen_png_sha256": "e4b6c20d3d7432b79261cc4107eba3386667b2c65cf5191de501ddd3a6680adb", "built_png_sha256": "30f7f472394c8afc62b85d0e7264c77a26728f53dd341b46e628b8441ebb4918"},
    {"driver": "ch1_graphite_v1.0.22.tex", "page": 64, "width": 794, "height": 1123, "changed_pixels": 56, "total_pixels": 891662, "changed_pixel_fraction": 6.28040670119395e-05, "changed_pixel_percent": 0.00628040670119395, "bbox": [599, 1017, 611, 1028], "frozen_png_sha256": "24b6392804c7c38faccbf785787da51e09d3e5a9339a50f17ad4f7e91a5e8bd7", "built_png_sha256": "02ff2795f1bff90df7941e4bd960f8a0ad5fd47c8cf8be5a5962bbea4dd6fa41"},
    {"driver": "ch1_graphite_v1.0.22.tex", "page": 83, "width": 794, "height": 1123, "changed_pixels": 247, "total_pixels": 891662, "changed_pixel_fraction": 0.00027701079557051887, "changed_pixel_percent": 0.027701079557051887, "bbox": [427, 427, 630, 442], "frozen_png_sha256": "1d8b2d20bf7c473ba02901126308f711ef80586751b4811ac1d03cdf07c8e7e7", "built_png_sha256": "f953a5e3311a352edf4eb26f8513a6592b3e235405aa31e5afce50e3fb7b8b03"},
    {"driver": "ch2_lco_v1.0.22.tex", "page": 5, "width": 794, "height": 1123, "changed_pixels": 573, "total_pixels": 891662, "changed_pixel_fraction": 0.0006426201856757381, "changed_pixel_percent": 0.06426201856757381, "bbox": [282, 516, 555, 650], "frozen_png_sha256": "e1bab8666aec2bcfc3e1a0aa2d8f816b69f868f5e4bfc1eb011e86a58d5edbc5", "built_png_sha256": "0a5471364883b471dbc53bd9b83025fa3be7fc0e6f2ca805da64a399c58c91d6"},
    {"driver": "ch2_lco_v1.0.22.tex", "page": 14, "width": 794, "height": 1123, "changed_pixels": 352, "total_pixels": 891662, "changed_pixel_fraction": 0.00039476842121790543, "changed_pixel_percent": 0.03947684212179054, "bbox": [177, 300, 588, 315], "frozen_png_sha256": "a1bee1505be2b63fa3e82f6036e07c142669543156d68e7ca61b6a79f646a43f", "built_png_sha256": "44ed922fd95cda612c686fb8fbf2a66d73b7f7785a46d60baa1f678e76320f1e"},
    {"driver": "ch2_lco_v1.0.22.tex", "page": 15, "width": 794, "height": 1123, "changed_pixels": 422, "total_pixels": 891662, "changed_pixel_fraction": 0.0004732735049828298, "changed_pixel_percent": 0.04732735049828298, "bbox": [214, 322, 669, 337], "frozen_png_sha256": "36b85034def3d200df0454788e790ada81f11794fd34b27219389208b59e9543", "built_png_sha256": "98fb53b0e2383ccd73f76405022d710b4588bcdeddc05e50c40599f5930ce926"},
    {"driver": "ch3_si_v1.0.22.tex", "page": 5, "width": 794, "height": 1123, "changed_pixels": 379, "total_pixels": 891662, "changed_pixel_fraction": 0.00042504895352723344, "changed_pixel_percent": 0.042504895352723344, "bbox": [196, 516, 613, 530], "frozen_png_sha256": "2de2113428365859890793f641da515cc3d5230d969b178bdda85a926d7e1e49", "built_png_sha256": "abfe29cbaa1b91c0f91903b3c86ca7892b8f917997d26ac8a4eb2b0ad0c43317"},
    {"driver": "ch3_si_v1.0.22.tex", "page": 13, "width": 794, "height": 1123, "changed_pixels": 239, "total_pixels": 891662, "changed_pixel_fraction": 0.00026803878599738465, "changed_pixel_percent": 0.026803878599738467, "bbox": [175, 718, 711, 732], "frozen_png_sha256": "1ff46d60f407779efbd4fad5ef1fbd08b66b31d9c076fce2451826fc0227e6d4", "built_png_sha256": "ae25dd87bb2683442756840f9d5d49a2ab49ede142f74b7e4be77b754eb2e49f"},
]
V1022_PREFIX = "Claude/docs/v1.0.22/"
V1022_BUILD_DRIVERS = [
    f"{V1022_PREFIX}appendix_phase_separation.tex",
    f"{V1022_PREFIX}ch1_graphite_v1.0.22.tex",
    f"{V1022_PREFIX}ch2_lco_v1.0.22.tex",
    f"{V1022_PREFIX}ch3_si_v1.0.22.tex",
]
IMPLEMENTATION_APPENDIX_ALLOWLIST = [
    f"{V1022_PREFIX}_sections/ch1_appB_codemap.tex",
    f"{V1022_PREFIX}_sections/ch2_appB_codemap.tex",
]
CH3_MAIN_IMPLEMENTATION_SECTION = f"{V1022_PREFIX}_sections/ch3v22_sec05_code.tex"
FITTING_GUIDE = f"{V1022_PREFIX}FITTING_GUIDE.md"
NONRENDERING_COMMAND_RE = re.compile(
    r"\\(?:label|ref|pageref|eqref|autoref|cref|Cref|input|include)\*?"
    r"(?:\[[^\]]*\])?\{[^{}]*\}"
)
CODE_SCAN_PATTERNS = [
    ("ENGLISH_CODE_OR_COMMAND", re.compile(r"(?i)(?<![A-Za-z])code(?![A-Za-z])")),
    ("LATEX_TEXTTT_COMMAND", re.compile(r"\\texttt\s*\{")),
    ("PYTHON_FILE_SUFFIX", re.compile(r"(?i)\.py\b")),
    ("API_WORD", re.compile(r"(?i)(?<![A-Za-z])API(?![A-Za-z])")),
    ("KOREAN_CODE", re.compile("코드")),
    ("KOREAN_IMPLEMENTATION", re.compile("구현")),
    ("DEFAULT_WORD", re.compile(r"(?i)(?<![A-Za-z])default(?![A-Za-z])")),
]
STATE_CHRONOLOGY = [
    {
        "commit": "720fb0566fdc5743192854f497d1f679ffc1b423",
        "event": "R9_CLOSEOUT_DOCUMENTS",
        "authority": "STATE_DOCUMENT_AS_OF_EVENT",
    },
    {
        "commit": "68b396e22821d935431b49ec54707fc693ff171d",
        "event": "C055_USER_DECISIONS_COMPLETED",
        "authority": "SOURCE_PATCH_AND_CHANGE_RECORD",
    },
    {
        "commit": "fb30c9085825c914027e41a0b08898750e1b0620",
        "event": "C055_RESIDUAL_PROSE_REPAIR",
        "authority": "SOURCE_PATCH",
    },
    {
        "commit": "2f56b8935f09db84609a25597578159bd19fdf7b",
        "event": "HANDOVER_LATER_TOUCH",
        "authority": "STATE_DOCUMENT_LATER_TOUCH_NOT_GLOBAL_REFRESH",
    },
    {
        "commit": "957930a9b75e4a673782fe27751788414ac11f0e",
        "event": "THREE_PDF_REBUILD_AFTER_C055",
        "authority": "GENERATED_BUILD_WITNESS",
    },
    {
        "commit": "f431e1acda8c78fbd78390ae285aa79421a26669",
        "event": "AUD2_G2_OVERCLAIM_DETECTED",
        "authority": "REVIEW_FINDING_ONLY",
    },
    {
        "commit": "5eab7ad2a40780bb8481f1d6301c75dcea1845b4",
        "event": "C056_CORRECTIONS_AND_PDF_REBUILD",
        "authority": "SOURCE_PATCH_CHANGE_EXECUTION_AND_BUILD_WITNESS",
    },
    {
        "commit": BASELINE,
        "event": "FROZEN_MANIFEST_BASELINE",
        "authority": "FROZEN_SOURCE_UNIVERSE",
    },
]
STATE_CONFLICTS: list[dict[str, Any]] = [
    {
        "conflict_id": "P063-S62-STATE-001",
        "topic": "C055_TITLE",
        "stale_claims": [{"path": "Claude/docs/v1.0.22/results/MERGE_READINESS.md", "lines": [165, 166], "claim": "PENDING_USER_DECISION"}],
        "current_evidence": [
            {"path": "Claude/docs/v1.0.22/_sections/ch1_sec11_lcointro.tex", "lines": [2, 8], "commit": "68b396e22821d935431b49ec54707fc693ff171d"},
            {"path": "Claude/docs/v1.0.22/results/V1022_CHANGE_LOG.md", "lines": [48, 48], "commit": "68b396e22821d935431b49ec54707fc693ff171d"},
        ],
        "current_state": "RESOLVED_IN_V1022",
        "stale_disposition": "SUPERSEDED",
    },
    {
        "conflict_id": "P063-S62-STATE-002",
        "topic": "C055_MOYASSARI",
        "stale_claims": [
            {"path": "Claude/docs/v1.0.22/results/MERGE_READINESS.md", "lines": [168, 169], "claim": "ABSENT_AND_PENDING"},
            {"path": "Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md", "lines": [143, 143], "claim": "CONDITIONAL_FUTURE_ADOPTION"},
        ],
        "current_evidence": [
            {"path": "Claude/docs/v1.0.22/_sections/ch3v22_bib.tex", "lines": [39, 39], "commit": "68b396e22821d935431b49ec54707fc693ff171d"},
            {"path": "Claude/docs/v1.0.22/results/V1022_REFERENCE_LEDGER.md", "lines": [30, 30], "commit": "68b396e22821d935431b49ec54707fc693ff171d"},
            {"path": "Claude/docs/v1.0.22/results/V1022_CHANGE_LOG.md", "lines": [48, 48], "commit": "68b396e22821d935431b49ec54707fc693ff171d"},
            {"path": "Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md", "lines": [97, 97], "commit": "68b396e22821d935431b49ec54707fc693ff171d"},
        ],
        "current_state": "RESOLVED_IN_V1022",
        "stale_disposition": "SUPERSEDED",
    },
    {
        "conflict_id": "P063-S62-STATE-003",
        "topic": "C056_G2_SCOPE",
        "stale_claims": [
            {"path": "Claude/docs/v1.0.22/results/V1022_CHANGE_LOG.md", "lines": [48, 48], "claim": "ZERO_TO_THIRTY_CONTINUOUS_COVERAGE"},
            {"path": "Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md", "lines": [97, 97], "claim": "ZERO_TO_THIRTY_CONTINUOUS_COVERAGE"},
            {"path": "Claude/docs/v1.0.22/results/V1022_REFERENCE_LEDGER.md", "lines": [30, 30], "claim": "PATH_B_FULL_COVERAGE"},
        ],
        "current_evidence": [
            {"path": "Claude/docs/v1.0.22/_sections/ch3v22_sec05_code.tex", "lines": [45, 45], "commit": "5eab7ad2a40780bb8481f1d6301c75dcea1845b4"},
            {"path": "Claude/docs/v1.0.22/results/V1022_CHANGE_LOG.md", "lines": [49, 49], "commit": "5eab7ad2a40780bb8481f1d6301c75dcea1845b4"},
        ],
        "current_state": "RESOLVED_IN_V1022_WITH_CORRECTED_SCOPE",
        "stale_disposition": "SUPERSEDED",
    },
    {
        "conflict_id": "P063-S62-STATE-004",
        "topic": "C056_COORDINATE",
        "stale_claims": [{"path": "Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md", "lines": [16, 16], "claim": "F_SI_ZERO_TO_THIRTY_PERCENT"}],
        "current_evidence": [{"path": "Claude/docs/v1.0.22/_sections/ch3v22_sec00_intro.tex", "lines": [8, 8], "commit": "5eab7ad2a40780bb8481f1d6301c75dcea1845b4"}],
        "current_state": "RESOLVED_IN_V1022_MASS_FRACTION_EXTERNAL_CAPACITY_FRACTION_INTERNAL",
        "stale_disposition": "SUPERSEDED",
    },
    {
        "conflict_id": "P063-S62-STATE-005",
        "topic": "R9_STATUS",
        "stale_claims": [
            {"path": "Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md", "lines": [23, 23], "claim": "R9_IN_PROGRESS"},
            {"path": "Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md", "lines": [43, 43], "claim": "R9_IN_PROGRESS"},
            {"path": "Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md", "lines": [147, 147], "claim": "R9_DRAFT"},
        ],
        "current_evidence": [
            {"path": "Claude/docs/v1.0.22/results/V1022_EXECUTION_LEDGER.md", "lines": [23, 23], "commit": "720fb0566fdc5743192854f497d1f679ffc1b423"},
            {"path": "Claude/docs/v1.0.22/results/V1022_EXECUTION_LEDGER.md", "lines": [24, 24], "commit": "5eab7ad2a40780bb8481f1d6301c75dcea1845b4"},
        ],
        "current_state": "R9_AND_AUD_COMPLETED_AS_PROCESS_STATES",
        "stale_disposition": "SUPERSEDED",
    },
    {
        "conflict_id": "P063-S62-STATE-006",
        "topic": "INDEX_AS_OF_BOUNDARY",
        "stale_claims": [
            {"path": "Claude/docs/v1.0.22/results/INDEX_v1022.md", "lines": [4, 5], "claim": "FINAL_INDEX"},
            {"path": "Claude/docs/v1.0.22/results/INDEX_v1022.md", "lines": [13, 23], "claim": "R0_TO_R8_ONLY"},
            {"path": "Claude/docs/v1.0.22/results/INDEX_v1022.md", "lines": [142, 146], "claim": "RESULT_COUNT_INCLUDES_LOCAL_PYC"},
        ],
        "current_evidence": [{"path": "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json", "lines": [], "commit": PARENT}],
        "current_state": "HISTORICAL_AS_OF_R9_NOT_FROZEN_MANIFEST_INDEX",
        "stale_disposition": "HISTORICAL_ONLY",
    },
    {
        "conflict_id": "P063-S62-STATE-007",
        "topic": "MERGE_BUILD_POLICY",
        "stale_claims": [{"path": "Claude/plans/2026-07-17-v1022-master-plan.md", "lines": [15, 95], "claim": "TEST_MERGE"}],
        "current_evidence": [{"path": "Claude/plans/2026-07-17-v1022-master-plan.md", "lines": [3, 99], "commit": BASELINE}],
        "current_state": "MERGE_BUILD_FORBIDDEN",
        "stale_disposition": "RESOLVED_BY_INTRA_DOCUMENT_CORRECTION",
    },
    {
        "conflict_id": "P063-S62-STATE-008",
        "topic": "MASTER_PLAN_REVISION_LABEL",
        "stale_claims": [{"path": "Claude/plans/2026-07-17-v1022-master-plan.md", "lines": [1, 3], "claim": "REVISION_V2"}],
        "current_evidence": [{"path": "Claude/plans/2026-07-17-v1022-master-plan.md", "lines": [1, 99], "commit": BASELINE}],
        "current_state": "CONFLICTED_REVISION_LABEL_USE_EXACT_PATH_AND_BLOB",
        "stale_disposition": "UNVERIFIED_LABEL",
    },
    {
        "conflict_id": "P063-S62-STATE-009",
        "topic": "MERGE_READINESS_STATUS",
        "stale_claims": [{"path": "Claude/docs/v1.0.22/results/MERGE_READINESS.md", "lines": [1, 204], "claim": "MASTER_CONFIRMED_AND_DRAFT_SIMULTANEOUSLY"}],
        "current_evidence": [{"path": "Claude/docs/v1.0.22/results/V1022_EXECUTION_LEDGER.md", "lines": [23, 23], "commit": "720fb0566fdc5743192854f497d1f679ffc1b423"}],
        "current_state": "HISTORICAL_R9_AS_OF_720FB056_NOT_CURRENT_FINAL_AUTHORITY",
        "stale_disposition": "HISTORICAL_ONLY",
    },
    {
        "conflict_id": "P063-S62-STATE-010",
        "topic": "AUDIT_SCOPE_CEILING",
        "stale_claims": [{"path": "Claude/docs/v1.0.22/results/AUDIT_LINEAGE_v19_v22.md", "lines": [7, 7], "claim": "ALL_UNLOGGED_LOSS_OR_CHANGE_ZERO"}],
        "current_evidence": [{"path": "Claude/docs/v1.0.22/results/AUDIT_LINEAGE_v19_v22.md", "lines": [33, 59], "commit": "704e8da60e956c31cc714cd067a2403dbc957abf"}],
        "current_state": "INTERNAL_AUDIT_SELF_REPORT_WITH_EXPLICIT_PROSE_SCOPE_CEILING",
        "stale_disposition": "SCOPE_LIMITED_NOT_EXTERNAL_TRUTH",
    },
    {
        "conflict_id": "P063-S62-STATE-011",
        "topic": "MERGE_PROCEDURE_COUNT",
        "stale_claims": [{"path": "Claude/docs/v1.0.22/results/V1022_EXECUTION_LEDGER.md", "lines": [23, 23], "claim": "FIVE_STEPS"}],
        "current_evidence": [{"path": "Claude/docs/v1.0.22/results/MERGE_READINESS.md", "lines": [138, 150], "commit": "720fb0566fdc5743192854f497d1f679ffc1b423"}],
        "current_state": "SOURCE_ENUMERATED_FOUR_STEPS",
        "stale_disposition": "SUPERSEDED_OR_ERRONEOUS_SUMMARY",
    },
]


def run_git(*args: str, text: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
        errors="strict" if text else None,
        timeout=60,
        check=True,
    )
    return proc.stdout


def git_bytes(commit: str, path: str) -> bytes:
    return run_git("show", f"{commit}:{path}", text=False)  # type: ignore[return-value]


def identity(commit: str, path: str) -> dict[str, Any]:
    raw = git_bytes(commit, path)
    return {
        "path": path,
        "commit": commit,
        "git_blob": str(run_git("rev-parse", f"{commit}:{path}")).strip(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }


def line_evidence(
    commit: str,
    path: str,
    start: int,
    end: int,
    evidence_role: str,
    source_id: str | None = None,
) -> dict[str, Any]:
    raw = git_bytes(commit, path)
    lines = raw.splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        raise RuntimeError(f"invalid evidence span: {commit}:{path}:{start}-{end}/{len(lines)}")
    selected = b"".join(lines[start - 1 : end])
    row: dict[str, Any] = {
        "path": path,
        "commit": commit,
        "git_blob": str(run_git("rev-parse", f"{commit}:{path}")).strip(),
        "lines": [start, end],
        "slice_sha256": hashlib.sha256(selected).hexdigest(),
        "evidence_role": evidence_role,
    }
    if source_id is not None:
        row["source_id"] = source_id
    return row


def strict_load(path: pathlib.Path) -> Any:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs)


def traversal_count(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + len(value) + sum(traversal_count(item) for item in value.values())
    if isinstance(value, list):
        return 1 + sum(traversal_count(item) for item in value)
    return 1


def family_id(source_id: str) -> str:
    number = int(source_id.rsplit("-", 1)[1])
    matches = [name for start, end, name in FAMILY_RANGES if start <= number <= end]
    if len(matches) != 1:
        raise RuntimeError(f"family route mismatch: {source_id} -> {matches}")
    return matches[0]


def canonical(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        + "\n"
    ).encode("utf-8")


def evidence_link(path: str, schema: str | int | None = None, gate: str | None = None) -> dict[str, Any]:
    row = identity(PARENT, path)
    if path.endswith(".json"):
        parsed = json.loads(git_bytes(PARENT, path))
        row["traversal"] = traversal_count(parsed)
    if schema is not None:
        row["schema"] = schema
    if gate is not None:
        row["gate"] = gate
    return row


def split_latex_comment(line: str) -> tuple[str, str]:
    """Split at the first unescaped percent sign without changing source bytes."""
    for index, char in enumerate(line):
        if char != "%":
            continue
        backslashes = len(line[:index]) - len(line[:index].rstrip("\\"))
        if backslashes % 2 == 0:
            return line[:index], line[index + 1 :]
    return line, ""


def rendered_scan_text(line: str) -> str:
    """Remove arguments that TeX consumes as non-rendered identifiers/paths."""
    current = line
    while True:
        updated = NONRENDERING_COMMAND_RE.sub("", current)
        if updated == current:
            return current
        current = updated


def code_token_matches(text: str) -> list[dict[str, Any]]:
    matches = [
        {
            "token_class": token_class,
            "start_column": match.start() + 1,
            "end_column": match.end(),
            "token": match.group(0),
        }
        for token_class, pattern in CODE_SCAN_PATTERNS
        for match in pattern.finditer(text)
    ]
    return sorted(matches, key=lambda row: (row["start_column"], row["end_column"], row["token_class"]))


def reachable_tex_inventory() -> list[dict[str, Any]]:
    queue = list(V1022_BUILD_DRIVERS)
    seen: set[str] = set()
    while queue:
        path = queue.pop(0)
        if path in seen:
            continue
        raw = git_bytes(BASELINE, path)
        seen.add(path)
        text = raw.decode("utf-8-sig")
        for match in re.finditer(r"\\(?:input|include)\s*\{([^}]+)\}", text):
            target = match.group(1)
            if not target.endswith(".tex"):
                target += ".tex"
            resolved = posixpath.normpath(f"{V1022_PREFIX}{target}")
            if not resolved.startswith(V1022_PREFIX) or resolved.startswith(f"{V1022_PREFIX}../"):
                raise RuntimeError(f"unsafe TeX dependency: {path} -> {target}")
            if resolved not in seen:
                queue.append(resolved)
    rows = []
    for path in sorted(seen):
        raw = git_bytes(BASELINE, path)
        rows.append(
            {
                "path": path,
                "blob_sha1": str(run_git("rev-parse", f"{BASELINE}:{path}")).strip(),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
                "physical_lines": len(raw.decode("utf-8-sig").splitlines()),
            }
        )
    if len(rows) != 53:
        raise RuntimeError(f"reachable TeX denominator drift: {len(rows)}")
    return rows


def code_surface_class(path: str, rendered_state: str) -> tuple[str, str, bool, str]:
    if rendered_state == "COMMENT":
        if path in IMPLEMENTATION_APPENDIX_ALLOWLIST:
            return "IMPLEMENTATION_APPENDIX_COMMENTS", "NONRENDERED_COMMENT_HISTORY", False, "NONRENDERED_COMMENT"
        if "preamble" in pathlib.PurePosixPath(path).name or path in V1022_BUILD_DRIVERS:
            return "PREAMBLE_OR_DRIVER_COMMENTS", "NONRENDERED_COMMENT_HISTORY", False, "NONRENDERED_COMMENT"
        return "PHYSICS_SOURCE_COMMENTS", "NONRENDERED_COMMENT_HISTORY", False, "NONRENDERED_COMMENT"
    if path == FITTING_GUIDE:
        return "FITTING_GUIDE", "SEPARATE_GUIDE_NOT_PHYSICS_MANUSCRIPT", False, "GUIDE_ONLY"
    if path in IMPLEMENTATION_APPENDIX_ALLOWLIST:
        return "IMPLEMENTATION_APPENDIX_RENDERED", "ALLOWLISTED_DEDICATED_IMPLEMENTATION_SURFACE", False, "DEDICATED_IMPLEMENTATION_APPENDIX"
    if path == CH3_MAIN_IMPLEMENTATION_SECTION:
        return "IMPLEMENTATION_MAIN_BODY_RELOCATION_REQUIRED", "FORBIDDEN_MAIN_BODY_IMPLEMENTATION_SECTION_OPEN", True, "IMPLEMENTATION_MAIN_BODY_RELOCATION_REQUIRED"
    name = pathlib.PurePosixPath(path).name
    if name.endswith("_bib.tex"):
        return "BIBLIOGRAPHY", "BIBLIOGRAPHIC_TOKEN_ONLY", False, "BIBLIOGRAPHY_ONLY"
    if "preamble" in name:
        return "PREAMBLE_NONRENDERED", "NONRENDERED_CONTROL", False, "NONRENDERED_CONTROL"
    return "PHYSICS_MAIN_BODY_RENDERED", "FORBIDDEN_BY_TARGET_MANUSCRIPT_POLICY_OPEN", True, "IMPLEMENTATION_OR_CODE_PROSE"


def scan_code_mentions() -> dict[str, Any]:
    reachable = reachable_tex_inventory()
    rows: list[dict[str, Any]] = []
    for source in reachable:
        path = source["path"]
        text = git_bytes(BASELINE, path).decode("utf-8-sig")
        for line_number, raw_line in enumerate(text.splitlines(), 1):
            rendered, comment = split_latex_comment(raw_line)
            for rendered_state, scan_text in (
                ("RENDERED", rendered_scan_text(rendered)),
                ("COMMENT", comment),
            ):
                matches = code_token_matches(scan_text)
                if not matches:
                    continue
                surface, disposition, actionable, manual_class = code_surface_class(path, rendered_state)
                rows.append(
                    {
                        "path": path,
                        "blob_sha1": source["blob_sha1"],
                        "line": line_number,
                        "rendered_state": rendered_state,
                        "surface_class": surface,
                        "manual_class": manual_class,
                        "actionable": actionable,
                        "disposition": disposition,
                        "occurrences": len(matches),
                        "token_classes": sorted({match["token_class"] for match in matches}),
                        "token_matches": matches,
                        "source_line_sha256": hashlib.sha256(raw_line.encode("utf-8")).hexdigest(),
                        "scan_text_sha256": hashlib.sha256(scan_text.encode("utf-8")).hexdigest(),
                    }
                )
    guide_raw = git_bytes(BASELINE, FITTING_GUIDE)
    guide_blob = str(run_git("rev-parse", f"{BASELINE}:{FITTING_GUIDE}")).strip()
    for line_number, line in enumerate(guide_raw.decode("utf-8-sig").splitlines(), 1):
        matches = code_token_matches(line)
        if not matches:
            continue
        surface, disposition, actionable, manual_class = code_surface_class(FITTING_GUIDE, "RENDERED")
        rows.append(
            {
                "path": FITTING_GUIDE,
                "blob_sha1": guide_blob,
                "line": line_number,
                "rendered_state": "RENDERED",
                "surface_class": surface,
                "manual_class": manual_class,
                "actionable": actionable,
                "disposition": disposition,
                "occurrences": len(matches),
                "token_classes": sorted({match["token_class"] for match in matches}),
                "token_matches": matches,
                "source_line_sha256": hashlib.sha256(line.encode("utf-8")).hexdigest(),
                "scan_text_sha256": hashlib.sha256(line.encode("utf-8")).hexdigest(),
            }
        )
    rows.sort(key=lambda row: (row["path"], row["line"], row["rendered_state"]))
    classes = []
    for class_name in sorted({row["surface_class"] for row in rows}):
        selected = [row for row in rows if row["surface_class"] == class_name]
        classes.append(
            {
                "class": class_name,
                "line_rows": len(selected),
                "occurrences": sum(row["occurrences"] for row in selected),
                "actionable_line_rows": sum(bool(row["actionable"]) for row in selected),
                "actionable_occurrences": sum(row["occurrences"] for row in selected if row["actionable"]),
                "disposition": selected[0]["disposition"],
            }
        )
    main_rows = [row for row in rows if row["surface_class"] in {"PHYSICS_MAIN_BODY_RENDERED", "IMPLEMENTATION_MAIN_BODY_RELOCATION_REQUIRED"}]
    actionable_rows = [row for row in main_rows if row["actionable"]]
    manual_counts = []
    for class_name in sorted({row["manual_class"] for row in main_rows}):
        selected = [row for row in main_rows if row["manual_class"] == class_name]
        manual_counts.append(
            {"class": class_name, "line_rows": len(selected), "occurrences": sum(row["occurrences"] for row in selected)}
        )
    implementation_path_counts = []
    for path in [*IMPLEMENTATION_APPENDIX_ALLOWLIST, CH3_MAIN_IMPLEMENTATION_SECTION]:
        selected = [row for row in rows if row["path"] == path and row["rendered_state"] == "RENDERED"]
        implementation_path_counts.append(
            {
                "path": path,
                "surface_class": selected[0]["surface_class"],
                "line_rows": len(selected),
                "occurrences": sum(row["occurrences"] for row in selected),
            }
        )
    return {
        "scan_contract": {
            "baseline_commit": BASELINE,
            "pattern_regexes": {name: pattern.pattern for name, pattern in CODE_SCAN_PATTERNS},
            "comments_split_at_first_unescaped_percent": True,
            "nonrendering_command_argument_regex": NONRENDERING_COMMAND_RE.pattern,
            "comments_stripped_for_rendered_scan": True,
            "reachable_tex_files": len(reachable),
            "guide_scanned_separately": True,
            "occurrence_definition": "ONE_REGEX_MATCH; OVERLAPPING_PATTERN_CLASSES_ARE_SEPARATE_OCCURRENCES",
        },
        "reachable_tex_inventory": reachable,
        "implementation_allowlist_exact_paths": IMPLEMENTATION_APPENDIX_ALLOWLIST,
        "misclassified_previous_surface": {
            "path": CH3_MAIN_IMPLEMENTATION_SECTION,
            "root_driver": f"{V1022_PREFIX}ch3_si_v1.0.22.tex",
            "root_input_line": 27,
            "appendix_command_before_input": False,
            "corrected_class": "IMPLEMENTATION_MAIN_BODY_RELOCATION_REQUIRED",
        },
        "classes": classes,
        "implementation_path_counts": implementation_path_counts,
        "occurrence_rows": rows,
        "physics_main_body_manual_refinement": {
            "candidate_line_rows": len(main_rows),
            "candidate_occurrences": sum(row["occurrences"] for row in main_rows),
            "mutually_exclusive_classes": manual_counts,
            "actionable_line_rows": len(actionable_rows),
            "actionable_occurrences": sum(row["occurrences"] for row in actionable_rows),
            "false_positive_line_rows": len(main_rows) - len(actionable_rows),
            "false_positive_occurrences": sum(row["occurrences"] for row in main_rows if not row["actionable"]),
        },
        "policy_pass": not actionable_rows,
        "external_scientific_authority": False,
        "owner": "Phase 078 scholarly-body implementation-reference removal",
        "acceptance_criterion": "Zero rendered code/API/implementation mentions outside the two exact dedicated implementation appendix paths.",
    }


def normalized_source_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def patch_final_survival(commit: str, path: str) -> dict[str, Any]:
    diff_raw = run_git("show", "--format=", "--unified=0", commit, "--", path, text=False)
    assert isinstance(diff_raw, bytes)
    diff_text = diff_raw.decode("utf-8", errors="replace")
    additions: list[dict[str, Any]] = []
    new_line: int | None = None
    for raw_line in diff_text.splitlines():
        if raw_line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", raw_line)
            if not match:
                raise RuntimeError(f"unparsed patch hunk: {commit}:{path}:{raw_line}")
            new_line = int(match.group(1))
            continue
        if new_line is None or raw_line.startswith(("diff --git", "index ", "--- ", "+++ ")):
            continue
        if raw_line.startswith("+"):
            value = raw_line[1:]
            normalized = normalized_source_line(value)
            if normalized:
                additions.append(
                    {
                        "patch_new_line": new_line,
                        "normalized_sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
                    }
                )
            new_line += 1
        elif raw_line.startswith("-"):
            continue
        elif raw_line.startswith(" "):
            new_line += 1
    final_lines = git_bytes(BASELINE, path).decode("utf-8-sig").splitlines()
    final_index: dict[str, list[int]] = {}
    for line_number, line in enumerate(final_lines, 1):
        normalized = normalized_source_line(line)
        if normalized:
            final_index.setdefault(hashlib.sha256(normalized.encode("utf-8")).hexdigest(), []).append(line_number)
    survivors = [
        row | {"frozen_final_line_numbers": final_index[row["normalized_sha256"]]}
        for row in additions
        if row["normalized_sha256"] in final_index
    ]
    return {
        "commit": commit,
        "path": path,
        "patch_sha256": hashlib.sha256(diff_raw).hexdigest(),
        "added_nonblank_lines": len(additions),
        "surviving_added_lines": len(survivors),
        "survivors": survivors,
        "final_presence": bool(survivors),
    }


def direct_finding_projection(
    finding: str,
    route: dict[str, Any],
    enriched_edges: list[dict[str, Any]],
    source_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    number = int(finding.rsplit("-", 1)[1])
    direct_edges: list[dict[str, Any]] = []
    edge_by_source = {edge["source_id"]: edge for edge in enriched_edges}
    proposal_line_index: dict[str, list[dict[str, Any]]] = {}
    for proposal_source_id in route["proposal_sources"]:
        proposal_source = source_by_id[proposal_source_id]
        proposal_lines = git_bytes(BASELINE, proposal_source["path"]).decode("utf-8-sig").splitlines()
        for line_number, line in enumerate(proposal_lines, 1):
            normalized = normalized_source_line(line)
            if not normalized:
                continue
            normalized_sha256 = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
            proposal_line_index.setdefault(normalized_sha256, []).append(
                {
                    "source_id": proposal_source_id,
                    "path": proposal_source["path"],
                    "blob_sha1": proposal_source["blob_sha1"],
                    "line": line_number,
                    "normalized_sha256": normalized_sha256,
                }
            )
    for source_id, start, end, patch_commit in CURRENT_STATE_EVIDENCE.get(number, []):
        if source_id not in edge_by_source or patch_commit not in route["patch_commits"]:
            continue
        final_lines = git_bytes(BASELINE, edge_by_source[source_id]["path"]).decode("utf-8-sig").splitlines()
        slice_hashes = {
            hashlib.sha256(normalized_source_line(line).encode("utf-8")).hexdigest()
            for line in final_lines[start - 1 : end]
            if normalized_source_line(line)
        }
        patch_rows = [
            row
            for row in edge_by_source[source_id]["patch_final_survival"]
            if row["commit"] == patch_commit
        ]
        survivor_lines = sorted(
            {
                line_number
                for patch_row in patch_rows
                for survivor in patch_row["survivors"]
                if survivor["normalized_sha256"] in slice_hashes
                for line_number in survivor["frozen_final_line_numbers"]
                if start <= line_number <= end
            }
        )
        if not survivor_lines:
            continue
        surviving_patch_content = sorted(
            {
                (
                    survivor["normalized_sha256"],
                    tuple(
                        line_number
                        for line_number in survivor["frozen_final_line_numbers"]
                        if start <= line_number <= end
                    ),
                )
                for patch_row in patch_rows
                for survivor in patch_row["survivors"]
                if survivor["normalized_sha256"] in slice_hashes
                and any(start <= line_number <= end for line_number in survivor["frozen_final_line_numbers"])
            }
        )
        proposal_content_evidence = sorted(
            {
                (
                    proposal_row["source_id"],
                    proposal_row["path"],
                    proposal_row["blob_sha1"],
                    proposal_row["line"],
                    proposal_row["normalized_sha256"],
                )
                for normalized_sha256, _ in surviving_patch_content
                for proposal_row in proposal_line_index.get(normalized_sha256, [])
            }
        )
        proposal_edge = bool(proposal_content_evidence)
        direct_edges.append(
            {
                "source_id": source_id,
                "path": edge_by_source[source_id]["path"],
                "patch_commit": patch_commit,
                "final_start_line": start,
                "final_end_line": end,
                "final_slice_sha256": hashlib.sha256(
                    "\n".join(final_lines[start - 1 : end]).encode("utf-8")
                ).hexdigest(),
                "surviving_patch_line_numbers": survivor_lines,
                "surviving_patch_content": [
                    {
                        "normalized_sha256": normalized_sha256,
                        "frozen_final_line_numbers": list(line_numbers),
                    }
                    for normalized_sha256, line_numbers in surviving_patch_content
                ],
                "proposal_content_evidence": [
                    {
                        "source_id": proposal_source_id,
                        "path": proposal_path,
                        "blob_sha1": proposal_blob_sha1,
                        "line": proposal_line,
                        "normalized_sha256": normalized_sha256,
                    }
                    for proposal_source_id, proposal_path, proposal_blob_sha1, proposal_line, normalized_sha256
                    in proposal_content_evidence
                ],
                "patch_to_final_current_state_edge": True,
                "proposal_to_patch_to_final_content_edge": proposal_edge,
                "content_edge_type": (
                    "PROPOSAL_PATCH_FINAL_CONTENT_EDGE"
                    if proposal_edge
                    else "PATCH_TO_FINAL_CURRENT_STATE_EDGE"
                ),
            }
        )
    if not direct_edges:
        return None
    return {
        "finding_id": finding,
        "proposal_sources": route["proposal_sources"],
        "review_sources": route.get("review_sources", []),
        "decision_sources": route["decision_sources"],
        "decision_evidence_state": route["decision_evidence_state"],
        "final_source_edges": direct_edges,
        "patch_to_final_current_state_edge": True,
        "proposal_to_patch_to_final_content_edge": any(
            edge["proposal_to_patch_to_final_content_edge"] for edge in direct_edges
        ),
        "external_truth": False,
    }


def build_artifact() -> dict[str, Any]:
    if len(FINDING_STATES) != 96:
        raise RuntimeError(f"finding adjudication incomplete: {len(FINDING_STATES)}/96")
    code_mention_boundary = scan_code_mentions()
    if not ADOPTION_ROUTES or len(BUILD_ROWS) != 4 or not code_mention_boundary or not STATE_CONFLICTS:
        raise RuntimeError("review/build/state adjudication constants incomplete")
    state_conflicts = json.loads(json.dumps(STATE_CONFLICTS, ensure_ascii=False))
    for conflict in state_conflicts:
        for role_key in ("stale_claims", "current_evidence"):
            enriched_anchors = []
            for anchor in conflict[role_key]:
                commit = anchor.get("commit", BASELINE)
                raw = git_bytes(commit, anchor["path"])
                identity_fields: dict[str, Any] = {
                    "commit": commit,
                    "git_blob": str(run_git("rev-parse", f"{commit}:{anchor['path']}")).strip(),
                    "source_sha256": hashlib.sha256(raw).hexdigest(),
                    "source_bytes": len(raw),
                }
                if anchor["lines"]:
                    start, end = anchor["lines"]
                    source_lines = raw.splitlines(keepends=True)
                    identity_fields["slice_sha256"] = hashlib.sha256(b"".join(source_lines[start - 1 : end])).hexdigest()
                else:
                    identity_fields["slice_sha256"] = None
                enriched_anchors.append(anchor | identity_fields)
            conflict[role_key] = enriched_anchors

    topology = strict_load(REPO / "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json")
    provisional = strict_load(REPO / "Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json")
    source_by_id = {row["source_id"]: row for row in topology["sources"]}
    source_by_path = {row["path"]: row for row in topology["sources"]}
    competing = [row for row in topology["sources"] if row["partition"] == "COMPETING_REVIEW_CANDIDATE"]
    if len(competing) != 125:
        raise RuntimeError(f"competing denominator drift: {len(competing)}")

    occurrence_rows: list[dict[str, Any]] = []
    for row in competing:
        occurrence_rows.append(
            {
                "source_id": row["source_id"],
                "family_id": family_id(row["source_id"]),
                "path": row["path"],
                "blob_sha1": row["blob_sha1"],
                "sha256": row["sha256"],
                "bytes": row["extent"]["bytes"],
                "physical_lines": row["extent"]["lines"],
                "nonblank_lines": row["extent"]["nonblank_lines"],
                "process_role": row["process_authority_subtype"],
                "authority_ceiling": "PROPOSAL_REVIEW_DECISION_OR_STATUS_EVIDENCE_ONLY",
                "final_adoption_authority": False,
            }
        )
    occurrence_rows.sort(key=lambda row: row["source_id"])

    adoption_routes: list[dict[str, Any]] = []
    final_paths = {
        row["path"]
        for row in topology["sources"]
        if row["partition"] == "FINAL_RELEASE_SURFACE" and not row["path"].endswith(".pdf")
    }
    for raw_route in ADOPTION_ROUTES:
        route = json.loads(json.dumps(raw_route, ensure_ascii=False))
        source_role_keys = (
            "task_brief_sources",
            "proposal_sources",
            "review_sources",
            "status_sources",
            "decision_sources",
            "change_record_sources",
        )
        declared_source_ids = sorted(
            {
                source_id
                for role_key in source_role_keys
                for source_id in route.get(role_key, [])
            }
        )
        for source_id in declared_source_ids:
            if source_id not in source_by_id:
                raise RuntimeError(f"unknown typed occurrence source: {route['route_id']} -> {source_id}")
        typed_key = {
            "T_TASK_OR_BRIEF": "task_brief_sources",
            "C_CANDIDATE_PROPOSAL_OR_DRAFT": "proposal_sources",
            "R_REVIEW_OR_SURVEY": "review_sources",
            "D_DECISION_TRIAGE_OR_EXECUTION_RECORD": "decision_sources",
            "S_SELF_REPORT_OR_STATUS": "status_sources",
        }
        for role_key in source_role_keys:
            route.pop(role_key, None)
        for role_key in typed_key.values():
            route[role_key] = []
        for source_id in declared_source_ids:
            source = source_by_id[source_id]
            subtype = source.get("process_authority_subtype")
            if subtype is None and source["partition"] == "STATUS_MACHINE_PROCESS":
                subtype = "S_SELF_REPORT_OR_STATUS"
            if subtype not in typed_key:
                raise RuntimeError(
                    f"unsupported typed occurrence role: {route['route_id']} -> {source_id}/{subtype}"
                )
            route[typed_key[subtype]].append(source_id)
        route["typed_occurrence_sources"] = [
            {
                "source_id": source_id,
                "process_role": (
                    source_by_id[source_id].get("process_authority_subtype")
                    or "S_SELF_REPORT_OR_STATUS"
                ),
                "path": source_by_id[source_id]["path"],
            }
            for source_id in declared_source_ids
        ]
        route.setdefault(
            "decision_evidence_state",
            "DIRECT" if route["decision_sources"] else "GROUND_NOT_FOUND",
        )
        for role_key in ("verification_only_sources",):
            for source_id in route.get(role_key, []):
                if source_id not in source_by_id:
                    raise RuntimeError(f"unknown {role_key} source: {route['route_id']} -> {source_id}")
        related_findings = route.pop("finding_ids")
        route["related_finding_ids"] = related_findings
        route["external_truth"] = False
        patch_rows: list[dict[str, Any]] = []
        inferred: set[str] = set()
        for commit in route["patch_commits"]:
            changed = str(
                run_git("diff-tree", "--no-commit-id", "--name-only", "-r", commit, "--", "Claude/docs/v1.0.22")
            ).splitlines()
            patch_rows.append(
                {
                    "commit": commit,
                    "subject": str(run_git("show", "-s", "--format=%s", commit)).rstrip("\r\n"),
                    "changed_paths": changed,
                }
            )
            inferred.update(path for path in changed if path in final_paths)
        if route.pop("infer_final_source_edges", False):
            route["final_source_edges"] = [
                {"source_id": source_by_path[path]["source_id"], "path": path}
                for path in sorted(inferred)
            ]
        enriched_edges: list[dict[str, Any]] = []
        for edge in route["final_source_edges"]:
            source = source_by_id[edge["source_id"]]
            if source["path"] != edge["path"] or source["partition"] != "FINAL_RELEASE_SURFACE":
                raise RuntimeError(f"invalid final-source edge: {edge}")
            if edge["path"] not in inferred:
                raise RuntimeError(
                    f"final-source edge lacks patch changed-path evidence: {route['route_id']} -> {edge['path']}"
                )
            survival = [
                patch_final_survival(commit, edge["path"])
                for commit in route["patch_commits"]
                if edge["path"] in next(row["changed_paths"] for row in patch_rows if row["commit"] == commit)
            ]
            final_presence = any(row["final_presence"] for row in survival)
            enriched_edges.append(
                edge
                | {
                    "blob_sha1": source["blob_sha1"],
                    "sha256": source["sha256"],
                    "patch_final_survival": survival,
                    "final_presence_state": "PATCH_ADDITION_SURVIVES_IN_FROZEN_FINAL" if final_presence else "PATCH_ADDITION_ABSENT_FROM_FROZEN_FINAL",
                    "final_adoption_authority": final_presence,
                    "external_truth": False,
                }
            )
        route["final_source_edges"] = enriched_edges
        route["patch_evidence"] = patch_rows
        projections = [
            projection
            for finding in related_findings
            if (projection := direct_finding_projection(finding, route, enriched_edges, source_by_id)) is not None
        ]
        route["finding_projections"] = projections
        route["finding_ids"] = [row["finding_id"] for row in projections]
        route["finding_edge_authority"] = any(
            row["proposal_to_patch_to_final_content_edge"] for row in projections
        )
        route["finding_patch_final_current_state_authority"] = bool(projections)
        if route["decision_evidence_state"].startswith("GROUND_NOT_FOUND"):
            inspected = [
                {
                    "source_id": row["source_id"],
                    "path": row["path"],
                    "blob_sha1": row["blob_sha1"],
                    "sha256": row["sha256"],
                }
                for row in occurrence_rows
            ]
            route["ground_not_found"] = {
                "searched_universe": "ALL_125_COMPETING_REVIEWER_CANDIDATE_OCCURRENCES_FULL_TEXT",
                "inspected_source_count": len(inspected),
                "inspected_sources_sha256": hashlib.sha256(canonical(inspected)).hexdigest(),
                "query": [
                    route["route_id"],
                    route["decision"],
                    *related_findings,
                    "direct user adoption decision",
                    "reviewer vote",
                ],
                "source_context": declared_source_ids,
                "owner": "Phase 063 Step 63.1 source disposition; user decision if direct adoption authority is required",
                "result": "NO_INDEPENDENT_DIRECT_DECISION_OR_REVIEWER_VOTE_RECOVERED",
            }
        else:
            route["ground_not_found"] = None
        adoption_routes.append(route)

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in occurrence_rows:
        grouped.setdefault(row["family_id"], []).append(row)
    family_rows = [
        {
            "family_id": name,
            "occurrence_count": len(rows),
            "source_ids": [row["source_id"] for row in rows],
            "paths": [row["path"] for row in rows],
            "physical_lines": sum(row["physical_lines"] for row in rows),
            "nonblank_lines": sum(row["nonblank_lines"] for row in rows),
            "bytes": sum(row["bytes"] for row in rows),
            "authority_ceiling": "FAMILY_GROUPING_ONLY_NO_ADOPTION_INFERENCE",
            "family_decision": FAMILY_DECISIONS[name],
        }
        for name, rows in sorted(grouped.items())
    ]

    records = {
        row["claim_id"]: row
        for row in provisional["records"]
        if 96 <= row["numeric_id"] <= 191
    }
    routes = {row["finding_id"]: row for row in topology["phase057_finding_routes"]}
    observations = {row["path"]: row for row in topology["phase057_observation_inputs"]}
    patch_ceiling_ids = {100, 116, 118, 124, 172}
    finding_rows: list[dict[str, Any]] = []
    for number in range(96, 192):
        finding = f"INTENT-PROV-{number:04d}"
        source = records[finding]
        route = routes[finding]
        state = FINDING_STATES[number]
        candidate_ids = route["candidate_v1022_source_ids"]
        proposal_ids = [
            item
            for item in candidate_ids
            if source_by_id[item]["partition"] == "COMPETING_REVIEW_CANDIDATE"
        ]
        linked_projections = [
            (adoption_route, projection)
            for adoption_route in adoption_routes
            for projection in adoption_route["finding_projections"]
            if projection["finding_id"] == finding
        ]
        observation = observations[source["source_path"]]
        state_evidence = [
            line_evidence(
                PARENT,
                source["source_path"],
                source["source_lines"][0],
                source["source_lines"][1],
                "PHASE057_FULLTEXT_ADJUDICATION_INPUT",
            )
            | {
                "observation_id": observation["observation_id"],
                "source_block_sha256": source["source_block_sha256"],
                "worktree_sha256_attested_by_step58": observation["sha256"],
            }
        ]
        for source_id, start, end, commit in CURRENT_STATE_EVIDENCE.get(number, []):
            final_source = source_by_id[source_id]
            state_evidence.append(
                line_evidence(
                    BASELINE,
                    final_source["path"],
                    start,
                    end,
                    "FROZEN_FINAL_SOURCE_CURRENT_STATE",
                    source_id,
                )
                | {"patch_commit": commit, "final_blob_sha1": final_source["blob_sha1"]}
            )
        criterion = source["body"].split("판정:", 1)[-1].strip()
        if not criterion:
            criterion = "Preserve this row as unresolved until the named owner supplies direct source or external evidence."
        finding_rows.append(
            {
                "finding_id": finding,
                "numeric_id": number,
                "title": source["title"],
                "source_path": source["source_path"],
                "source_lines": source["source_lines"],
                "source_block_sha256": source["source_block_sha256"],
                "referenced_actor": source["referenced_actor"],
                "actor_confidence": source["actor_confidence"],
                "candidate_source_routes": candidate_ids,
                "proposal_sources": proposal_ids,
                "proposal_families": sorted({family_id(item) for item in proposal_ids}),
                "decision_routes": [row["route_id"] for row, _ in linked_projections],
                "decision_sources": sorted(
                    {
                        source_id
                        for _, projection in linked_projections
                        for source_id in projection["decision_sources"]
                    }
                ),
                "final_source_edges": sorted(
                    {
                        edge["source_id"]
                        for _, projection in linked_projections
                        for edge in projection["final_source_edges"]
                    }
                ),
                "final_source_paths": sorted(
                    {
                        edge["path"]
                        for _, projection in linked_projections
                        for edge in projection["final_source_edges"]
                    }
                ),
                "patch_final_current_state_edges": [
                    {"route_id": route_row["route_id"]} | edge
                    for route_row, projection in linked_projections
                    for edge in projection["final_source_edges"]
                ],
                "proposal_patch_final_content_edges": [
                    {"route_id": route_row["route_id"]} | edge
                    for route_row, projection in linked_projections
                    for edge in projection["final_source_edges"]
                    if edge["proposal_to_patch_to_final_content_edge"]
                ],
                "build_page_edges": [],
                "state": state,
                "state_basis": (
                    "DIRECT_PROPOSAL_PATCH_FINAL_CONTENT_EDGE"
                    if any(
                        edge["proposal_to_patch_to_final_content_edge"]
                        for _, projection in linked_projections
                        for edge in projection["final_source_edges"]
                    )
                    else (
                        "DIRECT_PATCH_FINAL_CURRENT_STATE_EDGE_WITHOUT_PROPOSAL_CONTENT_MATCH"
                        if linked_projections
                        else (
                            "DIRECT_FINAL_SOURCE_STATE_WITHOUT_SURVIVING_PROPOSAL_PATCH_EDGE"
                            if number in CURRENT_STATE_EVIDENCE
                            else "PHASE057_FULLTEXT_OBSERVATION_WITHOUT_SYNTHETIC_ADOPTION_EDGE"
                        )
                    )
                ),
                "evidence_state": "DIRECT" if linked_projections or number not in CURRENT_STATE_EVIDENCE else "PARTIAL_DIRECT_FINAL_STATE_PATCH_EDGE_GROUND_NOT_FOUND",
                "state_evidence": state_evidence,
                "patch_confirmation_required": number in patch_ceiling_ids,
                "searched_universe": None,
                "query": None,
                "external_truth": False,
                "owner": "Phase 063 Step 63.1 disposition; Phase 071+ external truth",
                "acceptance_criterion": criterion,
            }
        )

    status_sources = [
        {
            "source_id": row["source_id"],
            "path": row["path"],
            "blob_sha1": row["blob_sha1"],
            "sha256": row["sha256"],
            "first_add_commit": row["first_add_commit"],
            "last_touch_commit": row["last_touch_commit"],
            "last_touch_subject": row["last_touch_subject"],
            "authority_ceiling": "STATE_SELF_REPORT_OR_MACHINE_PROCESS_ONLY",
        }
        for row in topology["sources"]
        if row["partition"] == "STATUS_MACHINE_PROCESS"
    ]

    family_counts = {row["family_id"]: row["occurrence_count"] for row in family_rows}
    state_counts = Counter(row["state"] for row in finding_rows)
    return {
        "schema": "P063_STEP62_REVIEW_ADOPTION_CLOSURE_V1",
        "phase": 63,
        "step": 62,
        "input_commit": PARENT,
        "frozen_baseline": BASELINE,
        "result_first": {"sentinel": SENTINEL, "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN"},
        "evidence_links": {
            "step58_topology": evidence_link("Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json", 1, "PASS_P063_STEP58_SOURCE_PROCESS_TOPOLOGY"),
            "step58_read_attestation": evidence_link("Codex/results/PHASE_063_V1022_READ_ATTESTATION.json", 1),
            "phase057_findings": evidence_link("Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json", 1),
            "step59_equations": evidence_link("Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json", 1, "PASS_P063_STEP59_EQUATION_MATERIAL_REDERIVATION_WITH_CONCERNS"),
            "step60_literature": evidence_link("Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json", 1, "PASS_P063_STEP60_LITERATURE_SCOPE_WITH_CONCERNS"),
            "step61_code": evidence_link("Codex/results/PHASE_063_V1022_CODE_DELTA_MATRIX.json", 1),
        },
        "competing_occurrences": occurrence_rows,
        "proposal_families": family_rows,
        "adoption_routes": adoption_routes,
        "finding_adjudications": finding_rows,
        "build_audit": {
            "materialization": "FROZEN_GIT_RAW_BLOB_BYTES_IN_EXTERNAL_TEMP_DIRECTORY",
            "raw_blob_materialization_verified": "204/204",
            "non_pdf_git_object_identity_before_build": "200/200",
            "non_pdf_git_object_identity_after_build": "200/200",
            "drivers": 4,
            "passes_per_driver": 3,
            "runs_exit_zero": "12/12",
            "build_execution": BUILD_EXECUTION,
            "rows": BUILD_ROWS,
            "built_pdf_sha256_authority": "WITNESS_RUN_ONLY_NOT_REPLAY_INVARIANT; PDF_METADATA_DEPENDS_ON_BUILD_TIME",
            "log_diagnostics": BUILD_LOG_DIAGNOSTICS,
            "log_sha256_authority": "WITNESS_RUN_ONLY_NOT_REPLAY_INVARIANT; TRANSCRIPT_INCLUDES_RUN_METADATA",
            "frozen_pdf_page_total": 133,
            "page_text_equal": "133/133",
            "render_exact": "125/133",
            "render_difference_pages": 8,
            "render_differences": RENDER_DIFFERENCES,
            "external_scientific_authority": False,
        },
        "code_mention_boundary": code_mention_boundary,
        "state_chronology": {
            "status_sources": status_sources,
            "commit_chronology": STATE_CHRONOLOGY,
            "conflicts": state_conflicts,
            "precedence_rule": "FINAL_SOURCE_AND_COMMIT_CHRONOLOGY_OUTRANK_STALE_SELF_REPORT",
        },
        "counts": {
            "competing_occurrences": len(occurrence_rows),
            "proposal_families": len(family_rows),
            "competing_physical_lines": sum(row["physical_lines"] for row in occurrence_rows),
            "competing_nonblank_lines": sum(row["nonblank_lines"] for row in occurrence_rows),
            "competing_bytes": sum(row["bytes"] for row in occurrence_rows),
            "family_occurrences": family_counts,
            "finding_adjudications": len(finding_rows),
            "finding_states": dict(sorted(state_counts.items())),
            "adoption_routes": len(adoption_routes),
            "build_drivers": len(BUILD_ROWS),
            "state_conflicts": len(state_conflicts),
        },
        "authority": {
            "proposal_as_adoption": False,
            "review_as_adoption": False,
            "cherrypick_as_source_patch": False,
            "build_as_science": False,
            "external_scientific": False,
            "primary_literature": False,
            "material": False,
            "experimental": False,
            "canonical": False,
            "final_release": False,
            "publication": False,
        },
        "gate": GATE,
    }


def result_text(artifact: dict[str, Any], matrix_sha256: str) -> str:
    counts = artifact["counts"]
    states = counts["finding_states"]
    pages = "/".join(str(row["built_pages"]) for row in artifact["build_audit"]["rows"])
    code = artifact["code_mention_boundary"]
    refinement = code["physics_main_body_manual_refinement"]
    code_classes = {row["class"]: row for row in code["classes"]}
    direct_finding_rows = sum(bool(row["decision_routes"]) for row in artifact["finding_adjudications"])
    proposal_finding_rows = sum(bool(row["proposal_patch_final_content_edges"]) for row in artifact["finding_adjudications"])
    resolved_direct_rows = sum(
        row["state"] == "RESOLVED_IN_V1022" and bool(row["decision_routes"])
        for row in artifact["finding_adjudications"]
    )
    resolved_rows = states["RESOLVED_IN_V1022"]
    return f"""# Phase 063 Step 62 Review, Adoption, Build and State Closure Result

Gate: `{GATE}`

Terminal: `{GATE}`

Result-first sentinel: `{SENTINEL}`

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

## Reconciled prerequisite

- Step 61 exact-eight containing commit: `{PARENT}`.
- Step 61 persistence terminal: `PASS_P063_STEP61_PERSISTENCE`.

## Closure result

- matrix SHA-256: `{matrix_sha256}`.
- competing/reviewer/candidate occurrence: `{counts['competing_occurrences']}/125`, families `{counts['proposal_families']}/22`, physical/nonblank lines `{counts['competing_physical_lines']:,}/{counts['competing_nonblank_lines']:,}`, bytes `{counts['competing_bytes']:,}`.
- Phase 057 finding adjudication: `{counts['finding_adjudications']}/96`; state counts `{json.dumps(states, ensure_ascii=False, sort_keys=True)}`.
- proposal-family chronology routes: `{counts['adoption_routes']}`; direct decisions are distinguished from `GROUND_NOT_FOUND`, and actual patch/final-source evidence is recorded separately. Proposal/reviewer/cherry-pick records alone never establish adoption.
- clean build: drivers `4/4`, passes `12/12`, pages `{pages}`, total `133`; current frozen PDF page counts are compared independently.
- state conflicts: `{counts['state_conflicts']}`; final source and commit chronology outrank stale status prose, which remains preserved as superseded evidence.
- external scientific/primary-literature/material/experimental/canonical/final-release/publication authority: `false/false/false/false/false/false/false`.

## Inputs and actual review coverage

- Recovery controls read: `Codex/AGENTS.md`, the Phase 063 detailed plan, Step 61 result, both execution ledgers, and active handover.
- Primary machine inputs replayed from Step 61 parent `{PARENT}`: Step 58 topology/read attestation, Phase 057 provisional finding ledger, Step 59 equation/material matrix, Step 60 literature/scope matrix, and Step 61 code matrix.
- Competing/reviewer/candidate corpus: `125/125` source occurrences, `17,072/17,072` physical lines and `13,926/13,926` nonblank lines. The original occurrence identities are retained even when grouped into 22 families.
- Phase 057 P--Z observation files: `11/11` files, `1..EOF`; all 96 consecutive records `INTENT-PROV-0096`--`0191` were re-adjudicated.
- Frozen build universe: manifest `204/204` Git objects. Raw `git cat-file blob` bytes matched `204/204`; all non-PDF inputs matched their Git objects before and after build `200/200`.

## Proposal, review, decision, patch, and source closure

- The 125 competing occurrences remain typed as task/brief `8`, candidate/proposal `58`, review/survey `46`, decision/triage/execution `9`, and self-report/status `4`.
- Nineteen family chronology routes cover all 125 competing occurrences. Each route retains typed occurrence edges separately from patch commits and final-source paths.
- Finding-level patch-to-final current-state edges are present only where an exact patch-added nonblank line survives inside an attested frozen-final source slice: `{direct_finding_rows}` rows total, including all `{resolved_direct_rows}/{resolved_rows}` `RESOLVED_IN_V1022` rows. Only `{proposal_finding_rows}` of those rows also have an exact normalized-content intersection with a typed candidate/proposal source; every other edge is explicitly classified `PATCH_TO_FINAL_CURRENT_STATE_EDGE`, never promoted to proposal adoption.
- Each final-source route stores patch hunk SHA-256, added-line hashes, frozen-final line locations and presence/absence state. A same-path patch without surviving content is not current-state evidence, and a surviving patch line without exact typed-proposal content evidence is not proposal adoption authority.
- COMP_AUD, the late FR A21 source correction, R7, R6, RV, R8, and v1.0.23 survey paths do not have a recovered independent decision/reviewer vote where the repository lacks one; their decision evidence remains `GROUND_NOT_FOUND` or repository-reported only.
- The 96 current states are `HISTORICAL_ONLY={states['HISTORICAL_ONLY']}`, `OPEN={states['OPEN']}`, `RESOLVED_IN_V1022={states['RESOLVED_IN_V1022']}`, `SUPERSEDED={states['SUPERSEDED']}`, `UNVERIFIED={states['UNVERIFIED']}`. Findings 101, 127, 136 and 169 remain `OPEN` because the mixed mass-fraction/external-capacity-fraction criterion is not fully satisfied; finding 186 remains `OPEN` because its required quantitative panel is still a placeholder. Every row retains the Phase 057 direct observation span; 15 rows additionally retain frozen final-source evidence, and five implemented-state claims retain a patch-confirmation ceiling.

## Clean build and page genealogy

- Four frozen drivers were raw-blob materialized and built in an external disposable directory with XeLaTeX three times each: `12/12` runs exited zero. The matrix preserves exact run order, argv, OS/PowerShell/Git/XeTeX/Poppler versions, producer/PDF versions and cleanup contract.
- Page counts are `{pages}` and total `133/133`. Extracted page text is equal for `133/133` frozen/built page pairs.
- Raw PDF bytes differ because the frozen producer is older `xdvipdfmx`/PDF 1.5 and the current producer is MiKTeX `dvipdfmx`/PDF 1.7; rebuilt-PDF SHA-256 values are witness-run identities, not cross-time invariants because PDF metadata includes build time. Render comparison is exact for `125/133`; the eight differing pages are Ch1 `39,64,83`, Ch2 `5,14,15`, and Ch3 `5,13`. Per-page pixel counts, bounding boxes and PNG SHA-256 values are preserved; the maximum changed-pixel fraction is `0.08097238639753629%`. Direct visual inspection found no content or layout difference.
- Undefined reference and citation diagnostics are `0/0` for every driver. The appendix has no multiply-defined labels. Ch1--Ch3 each report multiply-defined `swiderska2019` and `LastPage` labels at exact stored log lines; all four witness logs retain SHA-256 and diagnostic line ledgers, while transcript hashes are explicitly non-invariant across run metadata.
- The rebuilt Ch3 log emits two missing literal Greek `μ` diagnostics at log lines `1226/1227`, sourced from `_sections/ch3v22_sec02_cases.tex:70,73` on PDF page 7. Direct page-text and visual inspection confirms the same two replacement characters in both frozen and rebuilt PDFs; this remains a downstream manuscript/PDF repair item.

## Scholarly-body code-mention boundary

- Reachable TeX: `53` files; the fitting guide is scanned separately.
- The previous opaque aggregate was replaced by a row-level replay ledger: `{refinement['candidate_line_rows']}` rendered main-manuscript rows / `{refinement['candidate_occurrences']}` regex occurrences, with path, Git blob, line, exact token class/column, rendered/comment state and source/scan hashes for every row.
- Chapter 3 §3.5 is not an appendix: it is input at `ch3_si_v1.0.22.tex:27` before the bibliography and without a preceding `\\appendix`. It is therefore classified `IMPLEMENTATION_MAIN_BODY_RELOCATION_REQUIRED` at `{code_classes['IMPLEMENTATION_MAIN_BODY_RELOCATION_REQUIRED']['line_rows']}/{code_classes['IMPLEMENTATION_MAIN_BODY_RELOCATION_REQUIRED']['occurrences']}`, not allowlisted.
- Actionable future-policy blockers are `{refinement['actionable_line_rows']}` rows / `{refinement['actionable_occurrences']}` occurrences. Frozen v1.0.22 is not edited here. The only exact allowlisted implementation appendices are Ch1/Ch2, totaling `{code_classes['IMPLEMENTATION_APPENDIX_RENDERED']['line_rows']}/{code_classes['IMPLEMENTATION_APPENDIX_RENDERED']['occurrences']}`; guide `{code_classes['FITTING_GUIDE']['line_rows']}/{code_classes['FITTING_GUIDE']['occurrences']}`. Bibliography, preamble and comments stay separate.

## State-document conflict closure

- Eight chronology events reconstruct R9, C-055, later handover/build/audits, C-056 and the frozen baseline.
- Eleven conflict rows cover stale C-055/C-056 status, R9 state, historical index boundary, merge/build policy, revision label, merge readiness, audit ceiling, and four-versus-five merge-procedure count.
- Source paths and commit chronology outrank stale status prose. Superseded prose is retained as historical evidence rather than deleted.

## Validation executed

```text
python -m py_compile Codex/work/v1022_phase063/build_phase063_step62_review_adoption_closure.py Codex/work/v1022_phase063/validate_phase063_step62.py
python -B Codex/work/v1022_phase063/build_phase063_step62_review_adoption_closure.py
python -B Codex/work/v1022_phase063/validate_phase063_step62.py --content-only
python -B Codex/work/v1022_phase063/validate_phase063_step62.py --verify-build-replay --run-negative-probes --determinism-check
```

Independent build replay uses this durable sequence in a fresh disposable directory:

```text
git ls-tree -rz --full-tree 3b5fd059ed09cdcdde38668c399cb35b8afbcca9 -- Claude/docs/v1.0.22
git cat-file blob <oid> > <external-temp>/<exact-relative-path>
xelatex -interaction=nonstopmode -halt-on-error -file-line-error <driver>    # rounds 1..3, four drivers in stored order
pdfinfo <pdf>
pdftotext -layout [-f <page> -l <page>] <pdf> -
pdftoppm -png -r 96 <pdf> <output-prefix>
```

- content/Git-evidence gate: `{GATE}`.
- strict traversal and exact negative-control totals are emitted by the validator and are not predeclared as evidence before execution.
- builder determinism and stored-output identity: `2/2`.
- staged exact-seven and postcommit persistence terminals remain pending until the result-first files are staged and committed.

## Confirmed, unresolved, and ground not found

### Confirmed

- All 125 competing occurrences, 22 families, 96 findings, four build drivers/133 pages and eleven state conflicts are accounted for without occurrence loss.
- Actual patch changed-path membership, patch-hunk hashes, surviving added-line hashes/locations, frozen final-source blob identity and evidence line-slice hashes are machine-checked.
- Internal build completeness does not establish scientific, material, experimental, primary-literature, canonical, final-release or publication authority.

### Unresolved

- `OPEN=45` and `UNVERIFIED=11` Phase 057 findings require Step 63.1 routing and later domain owners.
- The Ch3 `μ` glyph warnings, three chapter duplicate-label diagnostics and `{refinement['actionable_line_rows']}/{refinement['actionable_occurrences']}` actionable main-manuscript implementation mentions remain open.
- The eight raster-microdifference pages are internally page-text/visual equivalent but raw PDF reproducibility remains producer-environment dependent.

### Ground not found

- No individual reviewer vote was recovered for SM2, R7 or the v1.0.23 survey; no vote is synthesized.
- Several late source patches are supported by commit/source chronology and repository self-report, but no independent direct user-decision record was recovered; those routes retain the explicit authority ceiling.
- No exact source/citation/bibitem-to-PDF-page sidecar exists in the frozen release. This build audit proves driver/page closure, not a fabricated exact citation-page genealogy.

## Exact-seven checkpoint

1. `Codex/work/v1022_phase063/build_phase063_step62_review_adoption_closure.py`
2. `Codex/work/v1022_phase063/validate_phase063_step62.py`
3. `Codex/results/PHASE_063_V1022_REVIEW_ADOPTION_CLOSURE_MATRIX.json`
4. `Codex/results/PHASE_063_STEP_062_REVIEW_ADOPTION_CLOSURE_RESULT.md`
5. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md`
7. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

`Claude/**`, protected `codex/lib-physics-endgame-v1025_2`, and `main` remain unchanged.

## Persistence boundary

The exact-seven commit subject is `audit(phase063): close v1022 review adoption build`. Post-commit verification must emit `PASS_P063_STEP62_PERSISTENCE` before Step 63.1.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=pathlib.Path, default=REPO)
    parser.add_argument("--matrix", type=pathlib.Path)
    parser.add_argument("--result", type=pathlib.Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.repo.resolve() != REPO.resolve():
        raise SystemExit("repo mismatch")
    artifact = build_artifact()
    matrix_bytes = canonical(artifact)
    result_bytes = result_text(artifact, hashlib.sha256(matrix_bytes).hexdigest()).encode("utf-8")
    matrix = args.matrix or REPO / MATRIX
    result = args.result or REPO / RESULT
    if args.check:
        if matrix.read_bytes() != matrix_bytes or result.read_bytes() != result_bytes:
            raise SystemExit("stored output mismatch")
        print("PASS_P063_STEP62_BUILDER_CHECK")
        return 0
    result.parent.mkdir(parents=True, exist_ok=True)
    result.write_bytes(result_bytes)
    matrix.parent.mkdir(parents=True, exist_ok=True)
    matrix.write_bytes(matrix_bytes)
    print("PASS_P063_STEP62_BUILDER result-first")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
