#!/usr/bin/env python3
"""Build the deterministic Phase 061 Step 47 process-authority matrix."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image
from pypdf import PdfReader


INPUT_COMMIT = "4c951f390c63f11f1c5a03cc47c7e3bce32926de"
BASELINE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
TOPOLOGY_PATH = Path("Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json")
TOPOLOGY_SHA256_LF = "0af27968b7896d2b5d462be6c9e1143e4e3985ffdd028b7f9f19a33924f9903c"
DEFAULT_OUTPUT = Path("Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json")
ALLOWED_AUTHORITY_CLASSES = (
    "USER_REQUIREMENT",
    "PLAN_INTENT",
    "PROCESS_SELF_ASSESSMENT",
    "INTERNAL_REVIEW",
    "COMPETING_DRAFT",
    "ADOPTED_RELEASE_SOURCE",
    "STRUCTURAL_WITNESS",
    "EXTERNAL_SCIENTIFIC_UNVERIFIED",
)

OBSERVATION_FILES = (
    "Codex/results/PHASE_057E_V1020_FOUNDATION_INTENT_OBSERVATIONS.md",
    "Codex/results/PHASE_057F_V1020_P2_P6_INTENT_OBSERVATIONS.md",
    "Codex/results/PHASE_057G_V1020_P7_REVIEW_DIRECTION_OBSERVATIONS.md",
    "Codex/results/PHASE_057H_V1020_CLOSING_DIRECTION_INTENT_OBSERVATIONS.md",
    "Codex/results/PHASE_057I_V1020_SNAPSHOT_LINEAGE_OBSERVATIONS.md",
)

CLAIM_CLASS_IDS = {
    "USER_REQUIREMENT": {26, 27, 28, 29, 30, 36, 47, 51},
    "PLAN_INTENT": {33, 48},
    "PROCESS_SELF_ASSESSMENT": {32, 37, 38, 45, 56},
    "INTERNAL_REVIEW": {34, 39, 40, 41, 42, 43, 44, 49, 57, 58},
    "COMPETING_DRAFT": {46, 52, 54, 55},
    "ADOPTED_RELEASE_SOURCE": {50},
    "EXTERNAL_SCIENTIFIC_UNVERIFIED": {31, 35, 53, 59},
    "STRUCTURAL_WITNESS": {60, 61, 62, 63, 64, 65},
}

CLASS_CEILINGS = {
    "USER_REQUIREMENT": "RECORDED_SECOND_ORDER_REQUIREMENT_ONLY_ORIGINAL_USER_TRANSCRIPT_GROUND_NOT_FOUND",
    "PLAN_INTENT": "PLAN_INTENT_ONLY",
    "PROCESS_SELF_ASSESSMENT": "INTERNAL_PROCESS_ONLY",
    "INTERNAL_REVIEW": "INTERNAL_REVIEW_ONLY",
    "COMPETING_DRAFT": "COMPETING_NOT_ADOPTED",
    "ADOPTED_RELEASE_SOURCE": "RELEASE_CONTENT_ONLY",
    "STRUCTURAL_WITNESS": "STRUCTURE_LINEAGE_ONLY",
    "EXTERNAL_SCIENTIFIC_UNVERIFIED": "EXTERNAL_SCIENCE_UNVERIFIED",
}

PLAN = "Claude/docs/v1.0.20/plans/"
RESULT = "Claude/docs/v1.0.20/results/"
SECTION = "Claude/docs/v1.0.20/_sections/"
RELEASE = "Claude/docs/v1.0.20/"

ALLOWED_CLAIM_TYPES = (
    "user_requirement",
    "plan",
    "self_review",
    "multi_review",
    "adoption",
    "completion",
    "scientific",
    "structural",
)

USER_REQUIREMENT_CLAIMS = frozenset({26, 27, 28, 29, 30, 36, 47, 51})

SNAPSHOT_PATHS = {
    "baseline": RESULT + "snapshot_v1019_baseline.json",
    "final": RESULT + "snapshot_v1020_final.json",
    "p0": RESULT + "snapshot_v1020_p0.json",
    "p2": RESULT + "snapshot_v1020_p2.json",
    "p3": RESULT + "snapshot_v1020_p3.json",
    "p4": RESULT + "snapshot_v1020_p4.json",
    "p5": RESULT + "snapshot_v1020_p5.json",
    "p6": RESULT + "snapshot_v1020_p6.json",
    "p7": RESULT + "snapshot_v1020_p7.json",
    "p7b": RESULT + "snapshot_v1020_p7b.json",
}

PLAN_ANCHOR_RANGES = {
    0: (20, 33),
    1: (18, 30),
    2: (24, 37),
    3: (18, 33),
    4: (15, 28),
    5: (15, 26),
    6: (15, 26),
    7: (15, 28),
    8: (15, 25),
}

OBSERVATION_RANGES = {
    26: (OBSERVATION_FILES[0], 25, 40), 27: (OBSERVATION_FILES[0], 41, 56),
    28: (OBSERVATION_FILES[0], 57, 73), 29: (OBSERVATION_FILES[0], 74, 87),
    30: (OBSERVATION_FILES[0], 88, 100), 31: (OBSERVATION_FILES[0], 101, 115),
    32: (OBSERVATION_FILES[0], 116, 130), 33: (OBSERVATION_FILES[0], 131, 155),
    34: (OBSERVATION_FILES[1], 24, 38), 35: (OBSERVATION_FILES[1], 39, 58),
    36: (OBSERVATION_FILES[1], 59, 70), 37: (OBSERVATION_FILES[1], 71, 87),
    38: (OBSERVATION_FILES[1], 88, 105), 39: (OBSERVATION_FILES[1], 106, 121),
    40: (OBSERVATION_FILES[2], 26, 45), 41: (OBSERVATION_FILES[2], 46, 62),
    42: (OBSERVATION_FILES[2], 63, 84), 43: (OBSERVATION_FILES[2], 85, 105),
    44: (OBSERVATION_FILES[2], 106, 125), 45: (OBSERVATION_FILES[2], 126, 142),
    46: (OBSERVATION_FILES[2], 143, 168), 47: (OBSERVATION_FILES[2], 169, 190),
    48: (OBSERVATION_FILES[2], 191, 208), 49: (OBSERVATION_FILES[3], 27, 49),
    50: (OBSERVATION_FILES[3], 50, 76), 51: (OBSERVATION_FILES[3], 77, 93),
    52: (OBSERVATION_FILES[3], 94, 122), 53: (OBSERVATION_FILES[3], 123, 144),
    54: (OBSERVATION_FILES[3], 145, 177), 55: (OBSERVATION_FILES[3], 178, 209),
    56: (OBSERVATION_FILES[3], 210, 227), 57: (OBSERVATION_FILES[3], 228, 244),
    58: (OBSERVATION_FILES[3], 245, 262), 59: (OBSERVATION_FILES[3], 263, 277),
    60: (OBSERVATION_FILES[4], 40, 52), 61: (OBSERVATION_FILES[4], 54, 84),
    62: (OBSERVATION_FILES[4], 86, 104), 63: (OBSERVATION_FILES[4], 106, 118),
    64: (OBSERVATION_FILES[4], 120, 141), 65: (OBSERVATION_FILES[4], 143, 159),
}

# Each curated source tuple is (path, first line, last line, evidentiary status).
CLAIM_SPECS: dict[int, dict[str, Any]] = {
    26: {
        "claim_type": "user_requirement",
        "primary": (PLAN + "2026-07-16-v1020-master-plan.md", 13, 31),
        "evidence": ((PLAN + "2026-07-16-v1020-master-plan.md", 37, 54, "RECORDED_REQUIREMENT"),),
        "expected": "Frozen user requirements defining undergraduate traceability and review-paper depth.",
        "gap": "Original conversational utterance is outside the frozen 232-source corpus.",
    },
    27: {
        "claim_type": "user_requirement",
        "primary": (PLAN + "2026-07-16-v1020-master-plan.md", 17, 17),
        "evidence": ((PLAN + "2026-07-16-v1020-master-plan.md", 48, 54, "RECORDED_REQUIREMENT_AND_GATE"), (SECTION + "ch1_sec02a_part0.tex", 132, 169, "ADOPTED_DERIVATION")),
        "expected": "Requirement plus adopted bare-site derivation before q(T) extension.",
        "gap": "No external adjudication of the derivation's physical correctness.",
    },
    28: {
        "claim_type": "user_requirement",
        "primary": (PLAN + "2026-07-16-v1020-master-plan.md", 25, 25),
        "evidence": ((RESULT + "V1020_REFERENCE_LEDGER.md", 1, 4, "INTERNAL_REFERENCE_POLICY"), (RESULT + "RESULT_P1_references.md", 22, 30, "SELF_REPORTED_VERIFICATION")),
        "expected": "Claim-level primary-source support, not DOI presence alone.",
        "gap": "Primary papers were not independently re-read in Step 47.",
    },
    29: {
        "claim_type": "user_requirement",
        "primary": (PLAN + "2026-07-16-v1020-master-plan.md", 31, 31),
        "evidence": ((PLAN + "2026-07-16-v1020-master-plan.md", 44, 44, "RECORDED_WORKFLOW"), (RESULT + "V1020_EXECUTION_LEDGER.md", 8, 16, "RECOVERY_LEDGER")),
        "expected": "Persistent plan, step log, result and ledger recovery chain.",
        "gap": "Recovery usability after context loss was not experimentally exercised here.",
    },
    30: {
        "claim_type": "user_requirement",
        "primary": (PLAN + "2026-07-16-v1020-master-plan.md", 29, 29),
        "evidence": ((PLAN + "2026-07-16-v1020-master-plan.md", 89, 90, "SCOPE_GUARD"), (RELEASE + "FITTING_GUIDE.md", 1, 5, "PACKAGE_COMPANION_ONLY")),
        "expected": "Theory body independent of implementation, with implementation confined to allowed surfaces.",
        "gap": "Rendered body was not re-scanned for every possible implementation reference in Step 47.",
    },
    31: {
        "claim_type": "scientific",
        "primary": (RESULT + "V1020_REFLEDGER_DRAFT_existing.md", 17, 18),
        "evidence": ((RESULT + "V1020_CHANGE_LOG.md", 10, 17, "CORRECTION_RECORD"), (RESULT + "V1020_REFERENCE_LEDGER.md", 10, 18, "CORRECTED_INTERNAL_LEDGER")),
        "expected": "Publisher/DOI metadata and primary-paper content supporting each cited proposition.",
        "gap": "Step 47 did not re-query DOI registries or re-read primary papers.",
        "contradictions": ("P061-CON-005", "P061-CON-006", "P061-CON-007"),
    },
    32: {
        "claim_type": "structural",
        "primary": (RESULT + "RESULT_P0_setup.md", 22, 33),
        "evidence": ((RESULT + "STEP_LOG_P0.md", 21, 23, "SELF_REPORTED_EXECUTION"), (RESULT + "tools_check_structure.py", 118, 132, "STRUCTURAL_CHECK_IMPLEMENTATION")),
        "expected": "Fresh execution logs establish only build, regression and structural properties.",
        "gap": "No fresh Step 47 execution; no material or experimental truth follows from these gates.",
    },
    33: {
        "claim_type": "plan",
        "primary": (PLAN + "2026-07-16-v1020-master-plan.md", 84, 90),
        "evidence": ((RESULT + "V1020_KICKOFF_SURVEY_history.md", 19, 25, "RECORDED_DEFERRAL"),),
        "expected": "Explicit non-goals and deferred physics items.",
        "gap": "Deferred items remain open rather than scientifically resolved.",
    },
    34: {
        "claim_type": "self_review",
        "primary": (PLAN + "PLAN_P3_graphite.md", 25, 29),
        "evidence": ((RESULT + "STEP_LOG_P3.md", 7, 9, "PLAN_REJECTED_AFTER_FULL_READ"), (RESULT + "RESULT_P3_graphite.md", 3, 4, "REJECTION_RECORDED")),
        "expected": "Full-read physical diagnosis can reject a planned KWW attribution.",
        "gap": "The rejection is internally reasoned and not an external scientific review.",
        "contradictions": ("P061-CON-001",),
    },
    35: {
        "claim_type": "scientific",
        "primary": (RESULT + "comp_P4_mitbg/AUTHOR_BRIEF.md", 12, 18),
        "evidence": ((RESULT + "RESULT_P4_lco.md", 3, 4, "PROCESS_REPORTED_ADOPTION"), (SECTION + "ch1_sec15_lcoelec.tex", 38, 52, "ADOPTED_THEORY_TEXT")),
        "expected": "Primary literature and derivation distinguish microscopic Mott mechanism from a phenomenological gate.",
        "gap": "Primary-paper support and material-specific truth remain independently unverified.",
        "contradictions": ("P061-CON-002",),
    },
    36: {
        "claim_type": "user_requirement",
        "primary": (RESULT + "STEP_LOG_P7.md", 63, 66),
        "evidence": ((RESULT + "V1020_CHANGE_LOG.md", 38, 40, "RECORDED_USER_DIRECTIVE"),),
        "expected": "Recorded decision removes historical self-reference from reader-facing theory.",
        "gap": "Original user utterance is not in the frozen source corpus.",
        "contradictions": ("P061-CON-003",),
    },
    37: {
        "claim_type": "completion",
        "primary": (RELEASE + "HANDOVER_v1.0.20.md", 1, 7),
        "evidence": ((RELEASE + "HANDOVER_v1.0.20.md", 59, 66, "RECORDED_VERSION_SEPARATION"),),
        "expected": "Frozen handover separates the quality-correction release from later expansion work.",
        "gap": "This is a process/version-lineage decision, not scientific closure.",
        "contradictions": ("P061-CON-003",),
    },
    38: {
        "claim_type": "self_review",
        "primary": (RESULT + "RESULT_P4_lco.md", 23, 28),
        "evidence": ((PLAN + "2026-07-16-v1020-master-plan.md", 53, 54, "GATE_POLICY"), (RESULT + "RESULT_P7_review.md", 4, 10, "LATER_INTERNAL_REVIEW")),
        "expected": "Equation-diff invariance plus independent physical re-derivation and primary-source checks.",
        "gap": "Internal review does not independently establish experimental or external scientific validity.",
        "contradictions": ("P061-CON-002",),
    },
    39: {
        "claim_type": "multi_review",
        "primary": (PLAN + "PLAN_P7_review.md", 4, 4),
        "evidence": ((RESULT + "RESULT_P7_review.md", 4, 10, "MULTI_REVIEW_SELF_REPORT"), (RESULT + "STEP_LOG_P7.md", 40, 46, "REVIEW_SCOPE_HISTORY")),
        "expected": "Independent reviews generate refutations and internally triaged findings.",
        "gap": "Reviewer agreement cannot promote claims to experimental or primary-source truth.",
        "contradictions": ("P061-CON-004",),
    },
}

CLAIM_SPECS.update({
    40: {
        "claim_type": "scientific",
        "primary": (RESULT + "comp_P7_review/REVIEW_CH2_C2F3.md", 21, 28),
        "evidence": ((SECTION + "ch2_sec00_intro.tex", 19, 22, "ADOPTED_CORRECTION"), (RESULT + "V1020_CHANGE_LOG.md", 33, 35, "ERRATUM_RECORD")),
        "expected": "Algebraic convex-mixture argument showing sign crossing but not boundary spikes from constant transition entropies.",
        "gap": "The internal derivation was not externally peer reviewed or experimentally tested.",
        "adoption": ((SECTION + "ch2_sec00_intro.tex", 19, 22),),
    },
    41: {
        "claim_type": "scientific",
        "primary": (RESULT + "comp_P7_review/REVIEW_O1.md", 43, 52),
        "evidence": ((SECTION + "ch1_sec02a_part0.tex", 242, 255, "ADOPTED_UNIT_CLARIFICATION"), (RESULT + "comp_P7_review/REVIEW_FINAL_FABLE.md", 15, 16, "FINAL_INTERNAL_REVIEW")),
        "expected": "Equation-level dimensional consistency between per-particle kBT and molar RT conventions.",
        "gap": "Internal dimensional audit only; no external scientific authority is inferred.",
    },
    42: {
        "claim_type": "scientific",
        "primary": (RESULT + "comp_P7_review/REVIEW_O2.md", 32, 32),
        "evidence": ((RESULT + "comp_P7_review/REVIEW_O2.md", 98, 102, "INTERNAL_REVIEW_DETAIL"), (RELEASE + "FITTING_GUIDE.md", 37, 51, "ADOPTED_CONDITIONAL_MODEL_RULE"), (RESULT + "CODE_IMPL_REPORT.md", 110, 121, "SELF_REPORTED_NUMERIC_GATE")),
        "expected": "Multi-temperature experimental identification of intrinsic width, disorder width and two-phase temperature law.",
        "gap": "Two-phase T-law and independent width components remain experimentally open.",
    },
    43: {
        "claim_type": "scientific",
        "primary": (RESULT + "comp_P7_review/REVIEW_O3.md", 99, 102),
        "evidence": ((RESULT + "comp_P7_review/REVIEW_O3.md", 157, 168, "CLAIM_SCOPE_CHECK"), (RESULT + "comp_P7_review/REVIEW_FINAL_FABLE.md", 21, 22, "FINAL_INTERNAL_REVIEW"), (SECTION + "ch1_sec15_lcoelec.tex", 240, 242, "ADOPTED_RESCOPE")),
        "expected": "Primary-paper scope must directly support the electronic/MIT proposition attributed to it.",
        "gap": "Primary paper was not independently re-read in Step 47; the adopted text is only internally scoped.",
    },
    44: {
        "claim_type": "multi_review",
        "primary": (RESULT + "RESULT_P7_review.md", 4, 10),
        "evidence": ((RESULT + "comp_P7_review/REVIEW_FINAL_FABLE.md", 43, 58, "FINAL_INTERNAL_CONVERGENCE"), (RESULT + "comp_P7_review/TRIAGE_P7.md", 1, 20, "INTERNAL_TRIAGE")),
        "expected": "Multi-review convergence supports internal consistency and bounded defect disposition.",
        "gap": "Consensus remains internal and cannot certify experimental or literature truth.",
        "contradictions": ("P061-CON-004",),
    },
    45: {
        "claim_type": "completion",
        "primary": (RESULT + "CODE_IMPL_REPORT.md", 41, 53),
        "evidence": ((RESULT + "CODE_IMPL_REPORT.md", 69, 75, "SELF_REPORTED_G1"), (RESULT + "CODE_IMPL_REPORT.md", 110, 121, "SELF_REPORTED_175_POINT_GATE"), (RELEASE + "test_gates_v1020.py", 1, 20, "TEST_SOURCE_NOT_FRESHLY_EXECUTED")),
        "expected": "Fresh execution against an independently frozen oracle would establish regression behavior only.",
        "gap": "Step 47 did not freshly execute code; reported gates do not establish new physics or experimental validity.",
    },
    46: {
        "claim_type": "plan",
        "primary": (RESULT + "DIRECTION_STATMECH_REPORT.md", 1, 3),
        "evidence": ((RESULT + "DIRECTION_GENERAL_REPORT.md", 1, 8, "READ_ONLY_CANDIDATE_REPORT"), (RESULT + "DIRECTION_STATMECH_REPORT.md", 329, 354, "GO_GATED_CANDIDATES")),
        "expected": "Explicit user adoption plus later release-text incorporation is required for candidate promotion.",
        "gap": "Candidate reports remain external-science-unverified planning material in this matrix.",
        "contradictions": ("P061-CON-009",),
    },
    47: {
        "claim_type": "user_requirement",
        "primary": (PLAN + "2026-07-16-v1020-master-plan.md", 27, 31),
        "evidence": ((RELEASE + "FITTING_GUIDE.md", 3, 5, "PACKAGE_COMPANION_CONTRACT"), (RESULT + "DIRECTION_GENERAL_REPORT.md", 18, 21, "INTERNAL_STRUCTURE_REVIEW")),
        "expected": "Recorded requirement combines self-contained textbook exposition, review depth and a separate fitting workflow.",
        "gap": "Satisfaction is a process assessment; no reader study or external review was conducted.",
    },
    48: {
        "claim_type": "plan",
        "primary": (RESULT + "DIRECTION_STATMECH_REPORT.md", 329, 354),
        "evidence": ((RESULT + "DIRECTION_SI_LCO_REPORT.md", 216, 236, "FUTURE_PHASE_SKETCH"), (RELEASE + "FITTING_GUIDE.md", 33, 33, "OPEN_DATA_DEPENDENCY")),
        "expected": "Prioritization is closed only after required experimental data and user adoption are available.",
        "gap": "Experimental closure and several user/data decisions remain open.",
        "contradictions": ("P061-CON-009",),
    },
    49: {
        "claim_type": "structural",
        "primary": (RESULT + "FIGS_PICK_JUDGMENT.md", 35, 100),
        "evidence": ((RESULT + "FIGS_PICK_JUDGMENT.md", 125, 131, "MODEL_INTERNAL_ATTESTATION"),),
        "expected": "Figures can verify equations against model anchors but require external data for experimental validation.",
        "gap": "No experimental comparison and no adopted release placement exist.",
        "adoption_state": "NOT_ADOPTED",
    },
    50: {
        "claim_type": "adoption",
        "primary": (RELEASE + "FITTING_GUIDE.md", 72, 90),
        "evidence": ((RELEASE + "FITTING_GUIDE.md", 63, 68, "ADOPTED_STAGED_PROCEDURE"), (RESULT + "CODE_IMPL_REPORT.md", 77, 121, "SELF_REPORTED_NUMERIC_CHECK")),
        "expected": "Adopted non-circular S0-S5 identification sequence, with numerical thresholds separately validated against data.",
        "gap": "The procedure is adopted; numeric thresholds and identifiability remain experimentally unverified.",
        "adoption": ((RELEASE + "FITTING_GUIDE.md", 72, 90),),
    },
    51: {
        "claim_type": "user_requirement",
        "primary": (PLAN + "2026-07-16-v1020-master-plan.md", 29, 29),
        "evidence": ((PLAN + "PLAN_P8_closing.md", 3, 13, "CLOSING_SCOPE"), (RELEASE + "HANDOVER_v1.0.20.md", 28, 29, "IMPLEMENTATION_SURFACE")),
        "expected": "Theory-body implementation references remain prohibited except in explicitly allowed companion or appendix surfaces.",
        "gap": "This matrix did not perform a new exhaustive rendered-body lexical audit.",
    },
    52: {
        "claim_type": "scientific",
        "primary": (RESULT + "DIRECTION_SI_LCO_REPORT.md", 120, 145),
        "evidence": ((RESULT + "DIRECTION_SI_LCO_REPORT.md", 242, 259, "PRELIMINARY_ARCHITECTURE_RECOMMENDATION"), (RELEASE + "HANDOVER_v1.0.20.md", 41, 44, "LATER_USER_DECISION")),
        "expected": "Chemo-mechanical primary theory and material data are required before silicon can share graphite/LCO authority.",
        "gap": "Chemo-mechanics theory, plastic dissipation and Si entropy support remain unverified or missing.",
        "adoption_state": "NOT_ADOPTED",
        "contradictions": ("P061-CON-009",),
    },
})

CONTRADICTION_SPECS = {
    "P061-CON-001": {
        "kind": "P3_KWW_PLAN_REJECTED",
        "status": "RESOLVED_BY_REJECTION",
        "description": "The P3 plan proposed KWW attribution; full reading found an exponential kernel and rejected the step.",
        "anchors": ((PLAN + "PLAN_P3_graphite.md", 25, 29, "PLANNED"), (RESULT + "STEP_LOG_P3.md", 7, 9, "REJECTED"), (RESULT + "RESULT_P3_graphite.md", 3, 4, "RESULT_RECORDED")),
    },
    "P061-CON-002": {
        "kind": "P4_SCOPE_NARROWED_AFTER_FULL_READ",
        "status": "RESOLVED_BY_NARROWER_ADOPTION",
        "description": "The P4 plan anticipated broad derivation work; full reading narrowed adopted work to the missing background bridge while preserving existing derivations.",
        "anchors": ((PLAN + "PLAN_P4_lco.md", 19, 23, "PLANNED_BROAD_SCOPE"), (RESULT + "RESULT_P4_lco.md", 3, 4, "NARROWED_RESULT"), (RESULT + "RESULT_P4_lco.md", 34, 36, "UNCHANGED_DERIVATIONS")),
    },
    "P061-CON-003": {
        "kind": "P6_DECISION_SUPERSEDED_IN_P7",
        "status": "RESOLVED_BY_LATER_USER_DIRECTIVE",
        "description": "P6 left historical title framing unchanged; the later P7 user directive removed reader-facing history markers.",
        "anchors": ((RESULT + "RESULT_P6_convention.md", 37, 41, "P6_PRESERVED"), (RESULT + "STEP_LOG_P7.md", 63, 66, "P7_SUPERSESSION"), (RESULT + "V1020_CHANGE_LOG.md", 38, 40, "EXECUTED_CHANGE")),
    },
    "P061-CON-004": {
        "kind": "P7_REVIEW_COUNT_DRIFT_4_10_11",
        "status": "UNRESOLVED_COUNTING_TAXONOMY_DRIFT",
        "description": "The plan says four review windows, the execution history expanded/restarted them, and the result reports eleven review documents.",
        "anchors": ((PLAN + "PLAN_P7_review.md", 4, 4, "PLANNED_FOUR"), (RESULT + "STEP_LOG_P7.md", 4, 15, "EXPANDED_AND_RESTARTED"), (RESULT + "RESULT_P7_review.md", 4, 10, "REPORTED_ELEVEN")),
    },
    "P061-CON-005": {
        "kind": "P1_BIB_EDIT_PLAN_CHANGED",
        "status": "RESOLVED_BY_RECORDED_PLAN_CHANGE",
        "description": "P1 declared bibliography edits out of scope, but its result records eight direct corrections.",
        "anchors": ((PLAN + "PLAN_P1_references.md", 12, 16, "BIB_EDIT_PROHIBITED"), (RESULT + "RESULT_P1_references.md", 15, 16, "BIB_EDIT_EXECUTED")),
    },
    "P061-CON-006": {
        "kind": "REFERENCE_LEDGER_HEADER_12_ACTUAL_14",
        "status": "OPEN_STALE_COUNT",
        "description": "The final reference ledger labels section B as twelve new keys but contains fourteen after two later Q3 additions.",
        "anchors": ((RESULT + "V1020_REFERENCE_LEDGER.md", 21, 38, "HEADER_AND_FOURTEEN_ROWS"),),
    },
    "P061-CON-007": {
        "kind": "CANDIDATE_DRAFT_COUNT_9_10_12",
        "status": "OPEN_STALE_COUNT",
        "description": "The candidate draft describes nine proposed keys, its table reports ten primary candidates, and its total reports twelve including auxiliary originals.",
        "anchors": ((RESULT + "V1020_REFLEDGER_DRAFT_candidates.md", 4, 18, "NINE_TEN_TWELVE_COUNTS"),),
    },
    "P061-CON-008": {
        "kind": "P8_DEDICATED_FILES_ABSENT_WITH_SUBSTITUTE_CLOSURE",
        "status": "PASS_WITH_CONCERNS_SUBSTITUTE_ONLY",
        "description": "P8 has no dedicated result or step log; the ledger and handover are substitute closure evidence.",
        "anchors": ((PLAN + "PLAN_P8_closing.md", 15, 25, "PLANNED_STEPS"), (RESULT + "V1020_EXECUTION_LEDGER.md", 16, 16, "LEDGER_CLOSURE"), (RELEASE + "HANDOVER_v1.0.20.md", 21, 29, "HANDOVER_SUBSTITUTE")),
        "missing_routes": (RESULT + "RESULT_P8*.md", RESULT + "STEP_LOG_P8*.md"),
    },
    "P061-CON-009": {
        "kind": "RESULT_P7_STALE_DIRECTION_STATUS",
        "status": "SUPERSEDED_BY_HANDOVER_DECISIONS",
        "description": "RESULT_P7 still says direction choices await GO, while the later handover records adopted user decisions including independent Chapter 3.",
        "anchors": ((RESULT + "RESULT_P7_review.md", 38, 45, "GO_STILL_PENDING"), (RELEASE + "HANDOVER_v1.0.20.md", 31, 44, "LATER_DECISIONS")),
    },
    "P061-CON-010": {
        "kind": "HANDOVER_GROUND_NOT_FOUND_NONE_OVERBROAD",
        "status": "OPEN_OVERBROAD_ATTESTATION",
        "description": "The handover states no ground-not-found items although P8 dedicated files and multiple scientific/data dependencies are absent.",
        "anchors": ((RELEASE + "HANDOVER_v1.0.20.md", 46, 50, "OVERBROAD_NONE"), (RELEASE + "FITTING_GUIDE.md", 21, 33, "LCO_PARAMETER_GAP"), (RESULT + "DIRECTION_SI_LCO_REPORT.md", 203, 208, "SCIENTIFIC_GAPS")),
        "missing_routes": (RESULT + "RESULT_P8*.md", RESULT + "STEP_LOG_P8*.md"),
    },
}

CLAIM_SPECS.update({
    53: {
        "claim_type": "scientific",
        "primary": (RESULT + "DIRECTION_SI_LCO_REPORT.md", 149, 174),
        "evidence": ((RESULT + "DIRECTION_SI_LCO_REPORT.md", 203, 208, "EXPLICIT_OPEN_SCIENCE_GAPS"), (RELEASE + "FITTING_GUIDE.md", 21, 33, "ADOPTED_TIER_CEILING")),
        "expected": "Material-specific high-voltage and multi-temperature LCO data with primary-paper support.",
        "gap": "LCO tier-2/3 anchors, multi-temperature T restoration and charge-order support remain open.",
    },
    54: {
        "claim_type": "scientific",
        "primary": (RESULT + "comp_Q2_gcbalance/NOTE_q2o1.md", 1, 24),
        "evidence": ((RESULT + "comp_Q2_gcbalance/draft_q2f1.tex", 1, 25, "COMPETING_DRAFT"), (RESULT + "DIRECTION_STATMECH_REPORT.md", 24, 48, "CANDIDATE_DERIVATION_SKETCH")),
        "expected": "Adopted derivation with explicit inter-class coupling assumptions and independent scientific review.",
        "gap": "The independent-site-class factorization changes hidden physics and remains a non-adopted candidate assumption.",
        "adoption_state": "NOT_ADOPTED",
    },
    55: {
        "claim_type": "scientific",
        "primary": (RESULT + "comp_Q3_tst/NOTE_q3f1.md", 1, 24),
        "evidence": ((RESULT + "comp_Q3_tst/draft_q3f1.tex", 1, 25, "COMPETING_DRAFT"), (RESULT + "DIRECTION_STATMECH_REPORT.md", 77, 120, "CANDIDATE_DERIVATION_SKETCH")),
        "expected": "Adopted TST derivation retaining the temperature dependence of activation entropy and prefactor.",
        "gap": "The candidate is not adopted and its temperature-law simplifications remain unverified.",
        "adoption_state": "NOT_ADOPTED",
    },
    56: {
        "claim_type": "completion",
        "primary": (RELEASE + "HANDOVER_v1.0.20.md", 1, 7),
        "evidence": ((RELEASE + "HANDOVER_v1.0.20.md", 21, 29, "INTERNAL_RELEASE_SUMMARY"), (RESULT + "V1020_EXECUTION_LEDGER.md", 16, 16, "P8_INTERNAL_GATE")),
        "expected": "Frozen release closure with explicit separation of quality correction from future physics expansion.",
        "gap": "Closure is process-bounded and does not certify scientific or experimental completeness.",
        "contradictions": ("P061-CON-008",),
    },
    57: {
        "claim_type": "multi_review",
        "primary": (RESULT + "FIGS_PICK_JUDGMENT.md", 95, 100),
        "evidence": ((RESULT + "FIGS_PICK_JUDGMENT.md", 125, 131, "EXPLICIT_NONVALIDATION"), (RELEASE + "FITTING_GUIDE.md", 21, 33, "MISSING_LCO_PARAMETERS")),
        "expected": "Measured LCO transition parameters before plotting quantitative three-peak curves.",
        "gap": "Q_j^cat and Omega_j^cat are unassigned; withholding the curve is the bounded valid decision.",
        "adoption_state": "NOT_ADOPTED",
        "contradictions": ("P061-CON-010",),
    },
    58: {
        "claim_type": "self_review",
        "primary": (RESULT + "comp_P7_review/REVIEW_FINAL_FABLE.md", 88, 90),
        "evidence": ((RESULT + "RESULT_P7_review.md", 4, 10, "INTERNAL_REVIEW_RESULT"), (RELEASE + "HANDOVER_v1.0.20.md", 46, 50, "CLOSING_ATTESTATION_WITH_LIMITS")),
        "expected": "H=0 and green build establish only the reviewed scopes and tested properties.",
        "gap": "No external peer review, primary-source replay or experimental validation follows from the green gates.",
    },
    59: {
        "claim_type": "scientific",
        "primary": (RESULT + "DIRECTION_SI_LCO_REPORT.md", 1, 4),
        "evidence": ((RESULT + "DIRECTION_SI_LCO_REPORT.md", 180, 208, "NEW_RESEARCH_LEDGER_CANDIDATES"), (RESULT + "V1020_REFERENCE_LEDGER.md", 37, 38, "PRIOR_INTERNAL_LEDGER_ENTRIES")),
        "expected": "Each new proposition requires a fresh primary-source/DOI support audit scoped to that proposition.",
        "gap": "Past web-verification labels do not establish present claim support; several fields and sources remain explicitly unverified.",
        "contradictions": ("P061-CON-006", "P061-CON-010"),
    },
    60: {
        "claim_type": "structural",
        "primary": (RELEASE + "HANDOVER_v1.0.20.md", 21, 26),
        "evidence": ((RESULT + "snapshot_v1019_baseline.json", 1, 1120, "STRICT_PARSED_FROZEN_BASELINE_STRUCTURE"), (RESULT + "snapshot_v1020_p0.json", 1, 1120, "STRICT_PARSED_FROZEN_P0_STRUCTURE")),
        "expected": "Baseline and P0 structural snapshots demonstrate version carry-forward only.",
        "gap": "Snapshots do not certify physical, chemical or experimental validity.",
    },
    61: {
        "claim_type": "adoption",
        "primary": (RESULT + "V1020_CHANGE_LOG.md", 39, 40),
        "evidence": ((SECTION + "ch1_sec02a_part0.tex", 132, 195, "ADOPTED_FIVE_EQUATION_ASSETS"), (SECTION + "ch1_sec15_lcoelec.tex", 38, 50, "ADOPTED_LCO_MOTT_EQUATION"), (RESULT + "snapshot_v1020_p0.json", 1, 1120, "STRICT_PARSED_P0_STRUCTURE"), (RESULT + "snapshot_v1020_p2.json", 1, 1139, "STRICT_PARSED_P2_STRUCTURE"), (RESULT + "snapshot_v1020_p7.json", 1, 1148, "STRICT_PARSED_P7_STRUCTURE"), (RESULT + "snapshot_v1020_p7b.json", 1, 1166, "STRICT_PARSED_P7B_STRUCTURE")),
        "expected": "Six release equations must be present in adopted chapter sources with bounded topology edges.",
        "gap": "Presence and derivation text do not independently establish scientific correctness.",
        "adoption": ((SECTION + "ch1_sec02a_part0.tex", 132, 195), (SECTION + "ch1_sec15_lcoelec.tex", 39, 46)),
    },
    62: {
        "claim_type": "structural",
        "primary": (RESULT + "comp_P7_review/REVIEW_FINAL_FABLE.md", 52, 53),
        "evidence": ((RESULT + "snapshot_v1020_p6.json", 967, 970, "P6_MOVED_KEY_SLICE"), (RESULT + "snapshot_v1020_p6.json", 1112, 1125, "P6_MOVED_KEYS_SLICE"), (RESULT + "snapshot_v1020_p7.json", 967, 970, "P7_MOVED_KEY_SLICE"), (RESULT + "snapshot_v1020_p7.json", 1112, 1125, "P7_MOVED_KEYS_SLICE")),
        "expected": "Hash-level comparison must distinguish a moved unlabeled block from substantive content change.",
        "gap": "Line-addressed unlabeled blocks remain topology evidence, not scientific validation.",
    },
    63: {
        "claim_type": "structural",
        "primary": (RESULT + "snapshot_v1020_final.json", 1166, 1175),
        "evidence": ((RESULT + "snapshot_v1020_final.json", 1166, 1175, "FINAL_FIRST_APPENDIX_BASELINE"),),
        "expected": "Final snapshot confirms exactly one appendix root; the exact eight pre-final v1.0.20 snapshot occurrences would be required for phase genealogy.",
        "gap": "The appendix root is absent from p0, p2, p3, p4, p5, p6, p7 and p7b; final is its first frozen snapshot occurrence.",
        "status": "CONFIRMED_WITH_GROUND_NOT_FOUND_SUBCLAIM",
        "contradictions": ("P061-CON-008", "P061-CON-010"),
    },
    64: {
        "claim_type": "structural",
        "primary": (RESULT + "tools_check_structure.py", 4, 6),
        "evidence": ((RESULT + "tools_check_structure.py", 118, 132, "STRUCTURAL_CHECK_LOGIC"), (RESULT + "RESULT_P0_setup.md", 27, 33, "SELF_REPORTED_GATE")),
        "expected": "Structural checker output covers labels, references, environments, equation hashes and tracked assets only.",
        "gap": "Equation validity, material truth, figure validity and experiments are outside the checker's authority.",
    },
    65: {
        "claim_type": "completion",
        "primary": (RELEASE + "HANDOVER_v1.0.20.md", 1, 7),
        "evidence": ((RESULT + "CODE_IMPL_REPORT.md", 41, 53, "SELF_REPORTED_MATCHED_IMPLEMENTATION"), (RESULT + "snapshot_v1019_baseline.json", 1, 1120, "STRICT_PARSED_BASELINE_STRUCTURE"), (RESULT + "snapshot_v1020_final.json", 1, 1299, "STRICT_PARSED_FINAL_STRUCTURE")),
        "expected": "Machine lineage limits v1.0.20 to a quality-correction release with future physics explicitly deferred.",
        "gap": "The lineage proves process/version relation only, not scientific completion.",
        "contradictions": ("P061-CON-008",),
    },
})


class BuildError(RuntimeError):
    """Raised when the frozen source contract cannot be reconstructed."""


def _reject_constant(value: str) -> None:
    raise BuildError(f"NONFINITE_JSON:{value}")


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise BuildError(f"DUPLICATE_JSON_KEY:{key}")
        result[key] = value
    return result


def strict_load_bytes(data: bytes) -> Any:
    return json.loads(
        data.decode("utf-8-sig"),
        object_pairs_hook=_object_pairs,
        parse_constant=_reject_constant,
    )


def _stable_stderr(data: bytes) -> str:
    return data.decode("utf-8", errors="replace").strip().replace("\r\n", "\n").replace("\r", "\n")


def _run_git_bytes(repo: Path, args: list[str], diagnostic: str) -> bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        raise BuildError(
            f"GIT_COMMAND_FAILED:{diagnostic}:returncode={proc.returncode}:"
            f"stderr={json.dumps(_stable_stderr(proc.stderr), ensure_ascii=True)}"
        )
    return proc.stdout


def _git_is_ancestor(repo: Path, ancestor: str, descendant: str, diagnostic: str) -> bool:
    proc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=repo,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    raise BuildError(
        f"GIT_COMMAND_FAILED:{diagnostic}:returncode={proc.returncode}:"
        f"stderr={json.dumps(_stable_stderr(proc.stderr), ensure_ascii=True)}"
    )


def git_blob(repo: Path, commit: str, path: str) -> bytes:
    tree = subprocess.run(
        ["git", "ls-tree", "--full-tree", "-z", commit, "--", path],
        cwd=repo,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if tree.returncode:
        raise BuildError(
            f"GIT_COMMAND_FAILED:LS_TREE:{commit}:{path}:returncode={tree.returncode}:"
            f"stderr={json.dumps(_stable_stderr(tree.stderr), ensure_ascii=True)}"
        )
    if not tree.stdout:
        raise BuildError(f"FROZEN_SOURCE_MISSING:{commit}:{path}")
    records = [record for record in tree.stdout.split(b"\0") if record]
    if len(records) != 1 or b"\t" not in records[0]:
        raise BuildError(f"FROZEN_SOURCE_TREE_CARDINALITY:{commit}:{path}:{len(records)}")
    metadata, actual_path_bytes = records[0].split(b"\t", 1)
    fields = metadata.decode("ascii", errors="strict").split()
    actual_path = actual_path_bytes.decode("utf-8", errors="strict")
    if len(fields) != 3 or fields[1] != "blob" or actual_path != path:
        raise BuildError(f"FROZEN_SOURCE_NOT_BLOB:{commit}:{path}")
    return _run_git_bytes(
        repo,
        ["cat-file", "blob", fields[2]],
        f"CAT_FILE:{commit}:{path}:{fields[2]}",
    )


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lf_bytes(data: bytes) -> bytes:
    return data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _walk_finite(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _walk_finite(key)
            _walk_finite(item)
    elif isinstance(value, list):
        for item in value:
            _walk_finite(item)
    elif isinstance(value, float) and not math.isfinite(value):
        raise BuildError("NONFINITE_JSON")


def _json_traversal_stats(value: Any) -> dict[str, int]:
    stats = {"nodes": 0, "max_depth": 0}

    def visit(item: Any, depth: int) -> None:
        stats["nodes"] += 1
        stats["max_depth"] = max(stats["max_depth"], depth)
        if isinstance(item, dict):
            for key, child in item.items():
                if not isinstance(key, str):
                    raise BuildError("JSON_KEY_NOT_STRING")
                visit(child, depth + 1)
        elif isinstance(item, list):
            for child in item:
                visit(child, depth + 1)
        elif isinstance(item, float) and not math.isfinite(item):
            raise BuildError("NONFINITE_JSON")
        elif item is not None and not isinstance(item, (str, int, float, bool)):
            raise BuildError(f"JSON_VALUE_TYPE:{type(item).__name__}")

    visit(value, 0)
    return stats


def _git_blob_batch(repo: Path, commit: str, paths: list[str]) -> dict[str, bytes]:
    proc = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None and proc.stdout is not None
    result: dict[str, bytes] = {}
    try:
        for path in paths:
            proc.stdin.write(f"{commit}:{path}\n".encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("ascii", errors="strict").rstrip("\n")
            fields = header.split()
            if len(fields) == 2 and fields[1] == "missing":
                raise BuildError(f"FROZEN_SOURCE_MISSING:{path}")
            if len(fields) != 3 or fields[1] != "blob":
                raise BuildError(f"FROZEN_SOURCE_NOT_BLOB:{path}:{header}")
            size = int(fields[2])
            data = proc.stdout.read(size)
            terminator = proc.stdout.read(1)
            if len(data) != size or terminator != b"\n":
                raise BuildError(f"FROZEN_SOURCE_TRUNCATED:{path}")
            result[path] = data
    finally:
        proc.stdin.close()
        proc.wait(timeout=30)
    if proc.returncode:
        stderr = b"" if proc.stderr is None else proc.stderr.read()
        raise BuildError(f"GIT_CAT_FILE_FAILED:{stderr.decode(errors='replace')}")
    return result


def _source_authority(row: dict[str, Any]) -> str:
    group = row["derived_authority_group"]
    basename = row["basename"]
    path = row["path"]
    if group == "FINAL_RELEASE_SURFACE":
        if basename == "HANDOVER_v1.0.20.md":
            return "PROCESS_SELF_ASSESSMENT"
        if row["extension"] in {"pdf", "png"}:
            return "STRUCTURAL_WITNESS"
        if basename == "appendix_phase_separation.tex":
            return "COMPETING_DRAFT"
        return "ADOPTED_RELEASE_SOURCE"
    if group == "PLAN_P0_P8":
        return "PLAN_INTENT"
    if group in {"STRUCTURAL_SNAPSHOT", "STRUCTURE_TOOL", "TEST_GATE"}:
        return "STRUCTURAL_WITNESS"
    if group == "CORE_PROCESS_RESULT":
        if basename == "V1020_STYLE_RUBRIC.md":
            return "PLAN_INTENT"
        external_ledgers = {
            "V1020_REFERENCE_LEDGER.md",
            "V1020_REFLEDGER_DRAFT_candidates.md",
            "V1020_REFLEDGER_DRAFT_existing.md",
            "V1020_P1_CITATION_BASELINE.md",
        }
        if basename in external_ledgers:
            return "EXTERNAL_SCIENTIFIC_UNVERIFIED"
        if basename == "FIGS_PICK_JUDGMENT.md":
            return "INTERNAL_REVIEW"
        if basename.startswith("DIRECTION_"):
            return "EXTERNAL_SCIENTIFIC_UNVERIFIED"
        if basename == "INTERCHAPTER_REPORT.md":
            return "INTERNAL_REVIEW"
        return "PROCESS_SELF_ASSESSMENT"
    if group == "COMPETITIVE_CANDIDATE_REVIEW":
        if row["extension"] in {"pdf", "png"} or row["manifest_role"] in {
            "figure",
            "generated_document",
        }:
            return "STRUCTURAL_WITNESS"
        if basename == "AUTHOR_BRIEF.md":
            return "PLAN_INTENT"
        if basename == "INTERCHAPTER_REPORT.md":
            return "INTERNAL_REVIEW"
        review_markers = ("/REVIEW_", "/TRIAGE_", "/PICK_JUDGMENT")
        return "INTERNAL_REVIEW" if any(marker in path for marker in review_markers) else "COMPETING_DRAFT"
    raise BuildError(f"SOURCE_AUTHORITY_UNROUTED:{row['source_id']}:{group}")


def _validate_topology(
    repo: Path, topology: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, bytes], dict[str, Any]]:
    if topology.get("baseline_commit") != BASELINE_COMMIT:
        raise BuildError("TOPOLOGY_BASELINE_MISMATCH")
    sources = topology.get("sources")
    if not isinstance(sources, list) or len(sources) != 232:
        raise BuildError("TOPOLOGY_SOURCE_COUNT")
    paths = [row.get("path") for row in sources]
    if any(not isinstance(path, str) for path in paths) or len(set(paths)) != 232:
        raise BuildError("TOPOLOGY_SOURCE_PATH_IDENTITY")
    if [row.get("manifest_index_v1020") for row in sources] != list(range(1, 233)):
        raise BuildError("TOPOLOGY_MANIFEST_INDEX")
    source_ids = [row.get("source_id") for row in sources]
    if source_ids != [f"P061-SRC-{index:04d}" for index in range(1, 233)]:
        raise BuildError("TOPOLOGY_SOURCE_ID")
    expected_path_hash = sha256(("\n".join(sorted(paths)) + "\n").encode("utf-8"))
    if topology.get("path_set_sha256") != expected_path_hash:
        raise BuildError("TOPOLOGY_PATH_SET_HASH")
    blobs = _git_blob_batch(repo, BASELINE_COMMIT, paths)
    text_extent_records: list[dict[str, Any]] = []
    strict_json_records: list[dict[str, Any]] = []
    pdf_extent_records: list[dict[str, Any]] = []
    image_extent_records: list[dict[str, Any]] = []
    for row in sources:
        path = row["path"]
        data = blobs[path]
        blob_id = blob_sha1(data)
        if blob_id != row["blob_sha1"]:
            raise BuildError(f"SOURCE_BLOB_MISMATCH:{row['source_id']}")
        if sha256(data) != row["sha256"] or len(data) != row["size_bytes"]:
            raise BuildError(f"SOURCE_CONTENT_MISMATCH:{row['source_id']}")
        mode = row["review_mode"]
        extent = row["manifest_extent"]
        if mode == "FULL_TEXT":
            if set(extent) != {"encoding_check", "lines"} or extent["encoding_check"] != "utf-8":
                raise BuildError(f"SOURCE_TEXT_EXTENT_SCHEMA:{row['source_id']}")
            try:
                data.decode("utf-8", errors="strict")
            except UnicodeDecodeError as exc:
                raise BuildError(f"SOURCE_UTF8_DECODE:{row['source_id']}:{exc.start}") from None
            observed_lines = len(data.splitlines())
            if observed_lines != extent["lines"]:
                raise BuildError(f"SOURCE_LINE_EXTENT_MISMATCH:{row['source_id']}")
            text_extent_records.append(
                {
                    "source_id": row["source_id"],
                    "path": path,
                    "blob_sha1": row["blob_sha1"],
                    "sha256": row["sha256"],
                    "manifest_extent": extent,
                    "observed_extent": {"encoding_check": "utf-8", "lines": observed_lines},
                    "validation_status": "PASS_FULL_TEXT_EXTENT",
                }
            )
            if row["extension"] == "json":
                parsed = strict_load_bytes(data)
                _walk_finite(parsed)
                traversal = _json_traversal_stats(parsed)
                strict_json_records.append(
                    {
                        "source_id": row["source_id"],
                        "path": path,
                        "blob_sha1": row["blob_sha1"],
                        "sha256": row["sha256"],
                        "manifest_extent": extent,
                        "traversal": traversal,
                        "validation_status": "PASS_STRICT_DUPLICATE_NONFINITE_FULL_TRAVERSAL",
                    }
                )
        elif mode == "FULL_PDF":
            if set(extent) != {"encrypted", "pages"}:
                raise BuildError(f"SOURCE_PDF_EXTENT_SCHEMA:{row['source_id']}")
            try:
                reader = PdfReader(io.BytesIO(data), strict=True)
                observed_extent = {
                    "encrypted": bool(reader.is_encrypted),
                    "pages": len(reader.pages),
                }
            except Exception as exc:
                raise BuildError(
                    f"SOURCE_PDF_READ_FAILED:{row['source_id']}:{type(exc).__name__}"
                ) from None
            if observed_extent != extent:
                raise BuildError(f"SOURCE_PDF_EXTENT_MISMATCH:{row['source_id']}")
            pdf_extent_records.append(
                {
                    "source_id": row["source_id"],
                    "path": path,
                    "blob_sha1": row["blob_sha1"],
                    "sha256": row["sha256"],
                    "manifest_extent": extent,
                    "observed_extent": observed_extent,
                    "validation_status": "PASS_PDF_STRICT_METADATA_EXTENT",
                }
            )
        elif mode == "FULL_IMAGE":
            if set(extent) != {"format", "frames", "height", "mode", "width"}:
                raise BuildError(f"SOURCE_IMAGE_EXTENT_SCHEMA:{row['source_id']}")
            try:
                with Image.open(io.BytesIO(data)) as image:
                    image.load()
                    observed_extent = {
                        "format": image.format,
                        "frames": getattr(image, "n_frames", 1),
                        "height": image.height,
                        "mode": image.mode,
                        "width": image.width,
                    }
            except Exception as exc:
                raise BuildError(
                    f"SOURCE_IMAGE_READ_FAILED:{row['source_id']}:{type(exc).__name__}"
                ) from None
            if observed_extent != extent:
                raise BuildError(f"SOURCE_IMAGE_EXTENT_MISMATCH:{row['source_id']}")
            image_extent_records.append(
                {
                    "source_id": row["source_id"],
                    "path": path,
                    "blob_sha1": row["blob_sha1"],
                    "sha256": row["sha256"],
                    "manifest_extent": extent,
                    "observed_extent": observed_extent,
                    "validation_status": "PASS_IMAGE_PIXEL_METADATA_EXTENT",
                }
            )
        else:
            raise BuildError(f"SOURCE_REVIEW_MODE:{row['source_id']}:{mode}")
    if len({row["blob_sha1"] for row in sources}) != 231:
        raise BuildError("TOPOLOGY_UNIQUE_BLOB_COUNT")
    duplicate = topology.get("duplicates")
    expected_duplicate_paths = {
        "Claude/docs/v1.0.20/results/snapshot_v1020_p5.json",
        "Claude/docs/v1.0.20/results/snapshot_v1020_p6.json",
    }
    if (
        not isinstance(duplicate, list)
        or len(duplicate) != 1
        or duplicate[0].get("blob_sha1") != "8dfea239d1787582c6c37c41fe6d06f7b204d72b"
        or set(duplicate[0].get("paths", [])) != expected_duplicate_paths
    ):
        raise BuildError("TOPOLOGY_DUPLICATE_GROUP")
    counts = {
        "full_text_extents_validated": len(text_extent_records),
        "strict_json_files_validated": len(strict_json_records),
        "strict_json_nodes_traversed": sum(row["traversal"]["nodes"] for row in strict_json_records),
        "pdf_extents_validated": len(pdf_extent_records),
        "pdf_pages_validated": sum(row["observed_extent"]["pages"] for row in pdf_extent_records),
        "image_extents_validated": len(image_extent_records),
    }
    if counts["full_text_extents_validated"] != 195:
        raise BuildError("FULL_TEXT_VALIDATION_COUNT")
    if counts["strict_json_files_validated"] != 11:
        raise BuildError("STRICT_JSON_VALIDATION_COUNT")
    if counts["pdf_extents_validated"] != 14 or counts["pdf_pages_validated"] != 130:
        raise BuildError("PDF_VALIDATION_COUNT")
    if counts["image_extents_validated"] != 23:
        raise BuildError("IMAGE_VALIDATION_COUNT")
    validation = {
        "input_commit": BASELINE_COMMIT,
        "authority_ceiling": "FROZEN_BYTES_AND_METADATA_EXTENT_ONLY_NO_VISUAL_OR_SCIENTIFIC_PROMOTION",
        "counts": counts,
        "text_extent_records": text_extent_records,
        "strict_json_records": strict_json_records,
        "pdf_extent_records": pdf_extent_records,
        "image_extent_records": image_extent_records,
        "external_scientific_truth": False,
        "visual_truth_promoted": False,
        "validation_status": "PASS_FROZEN_232_SOURCE_EXTENT_AND_STRICT_JSON_VALIDATION",
    }
    return sources, blobs, validation


def _line_slice(data: bytes, line_start: int, line_end: int) -> bytes:
    lines = lf_bytes(data).decode("utf-8").splitlines()
    if not (1 <= line_start <= line_end <= len(lines)):
        raise BuildError(f"SLICE_RANGE_INVALID:{line_start}:{line_end}:{len(lines)}")
    return ("\n".join(lines[line_start - 1 : line_end]) + "\n").encode("utf-8")


def _release_inclusion_edges(
    sources: list[dict[str, Any]], blobs: dict[str, bytes]
) -> dict[str, dict[str, Any]]:
    by_path = {row["path"]: row for row in sources}
    roots = (
        "Claude/docs/v1.0.20/graphite_ica_ch1_v1.0.20.tex",
        "Claude/docs/v1.0.20/graphite_ica_ch2_v1.0.20.tex",
    )
    edges: dict[str, dict[str, Any]] = {}
    for root in roots:
        root_row = by_path.get(root)
        if root_row is None:
            raise BuildError(f"RELEASE_ROOT_MISSING:{root}")
        for line_number, line in enumerate(lf_bytes(blobs[root]).decode("utf-8").splitlines(), start=1):
            match = re.fullmatch(r"\\input\{([^}]+)\}", line.strip())
            if match is None:
                continue
            child = f"Claude/docs/v1.0.20/{match.group(1)}"
            if not child.endswith(".tex"):
                child += ".tex"
            if child not in by_path or child in edges:
                raise BuildError(f"RELEASE_INCLUDE_INVALID:{root}:{line_number}:{child}")
            edges[child] = {
                "topology_type": "INCLUDED_RELEASE_SECTION",
                "parent_root_source_id": root_row["source_id"],
                "parent_root_path": root,
                "input_line_start": line_number,
                "input_line_end": line_number,
                "input_slice_sha256_lf": sha256(_line_slice(blobs[root], line_number, line_number)),
            }
    return edges


def _source_routes(
    sources: list[dict[str, Any]], blobs: dict[str, bytes]
) -> list[dict[str, Any]]:
    inclusion_edges = _release_inclusion_edges(sources, blobs)
    direct_roots = {
        "Claude/docs/v1.0.20/graphite_ica_ch1_v1.0.20.tex",
        "Claude/docs/v1.0.20/graphite_ica_ch2_v1.0.20.tex",
    }
    package_companions = {
        "Claude/docs/v1.0.20/Anode_Fit_v1.0.20.py",
        "Claude/docs/v1.0.20/FITTING_GUIDE.md",
    }
    routes: list[dict[str, Any]] = []
    for row in sources:
        authority_class = _source_authority(row)
        if authority_class not in ALLOWED_AUTHORITY_CLASSES:
            raise BuildError(f"SOURCE_AUTHORITY_INVALID:{row['source_id']}")
        adoption_topology: dict[str, Any] | None = None
        if authority_class == "ADOPTED_RELEASE_SOURCE":
            if row["path"] in direct_roots:
                adoption_topology = {"topology_type": "DIRECT_RELEASE_ROOT"}
            elif row["path"] in package_companions:
                adoption_topology = {"topology_type": "PACKAGE_COMPANION_ROOT"}
            elif row["path"] in inclusion_edges:
                adoption_topology = inclusion_edges[row["path"]]
            else:
                raise BuildError(f"ADOPTED_RELEASE_ORPHAN:{row['source_id']}:{row['path']}")
        routes.append(
            {
                "source_id": row["source_id"],
                "manifest_index_v1020": row["manifest_index_v1020"],
                "path": row["path"],
                "blob_sha1": row["blob_sha1"],
                "sha256": row["sha256"],
                "review_mode": row["review_mode"],
                "manifest_extent": row["manifest_extent"],
                "source_authority_class": authority_class,
                "exact_one_class": True,
                "adoption_topology": adoption_topology,
                "evidence_route": (
                    f"{row['source_id']} -> frozen Git blob {row['blob_sha1']} -> "
                    f"{authority_class} ceiling"
                ),
                "authority_ceiling": CLASS_CEILINGS[authority_class],
                "external_scientific_truth": False,
                "scientific_authority_promoted": False,
            }
        )
    return routes


def _claim_class(number: int) -> str:
    matches = [name for name, numbers in CLAIM_CLASS_IDS.items() if number in numbers]
    if len(matches) != 1:
        raise BuildError(f"CLAIM_CLASS_CARDINALITY:{number}:{matches}")
    return matches[0]


def _resolve_selectors(
    selectors: tuple[str, ...], routes: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    for selector in selectors:
        if selector.startswith("contains:"):
            needle = selector.removeprefix("contains:")
            matches = [route for route in routes if needle in route["path"]]
        elif selector.startswith("path:"):
            wanted = selector.removeprefix("path:")
            matches = [route for route in routes if route["path"] == wanted]
        else:
            matches = [route for route in routes if route["path"].rsplit("/", 1)[-1] == selector]
        if not matches:
            raise BuildError(f"EVIDENCE_SELECTOR_UNRESOLVED:{selector}")
        for route in matches:
            selected[route["source_id"]] = route
    return sorted(selected.values(), key=lambda route: route["manifest_index_v1020"])


def _route_by_path(routes: list[dict[str, Any]], path: str) -> dict[str, Any]:
    matches = [route for route in routes if route["path"] == path]
    if len(matches) != 1:
        raise BuildError(f"FROZEN_ROUTE_CARDINALITY:{path}:{len(matches)}")
    return matches[0]


def _evidence_record(
    routes: list[dict[str, Any]],
    source_blobs: dict[str, bytes],
    path: str,
    line_start: int,
    line_end: int,
    status: str,
) -> dict[str, Any]:
    route = _route_by_path(routes, path)
    sliced = _line_slice(source_blobs[path], line_start, line_end)
    return {
        "source_id": route["source_id"],
        "path": path,
        "input_commit": BASELINE_COMMIT,
        "blob_sha1": route["blob_sha1"],
        "sha256": route["sha256"],
        "line_start": line_start,
        "line_end": line_end,
        "slice_sha256_lf": sha256(sliced),
        "evidence_status": status,
        "source_authority_class": route["source_authority_class"],
    }


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _snapshot_input(
    routes: list[dict[str, Any]], source_blobs: dict[str, bytes], alias: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    path = SNAPSHOT_PATHS[alias]
    route = _route_by_path(routes, path)
    data = source_blobs[path]
    parsed = strict_load_bytes(data)
    _walk_finite(parsed)
    if not isinstance(parsed, dict) or len(parsed) not in {2, 3}:
        raise BuildError(f"SNAPSHOT_ROOT_SCHEMA:{alias}")
    for root_name, chapter in parsed.items():
        if not isinstance(root_name, str) or not isinstance(chapter, dict):
            raise BuildError(f"SNAPSHOT_ROOT_TYPE:{alias}")
        if set(chapter) != {"labels", "eqblocks", "asset_unique", "bibitems"}:
            raise BuildError(f"SNAPSHOT_CHAPTER_FIELDS:{alias}:{root_name}")
        if (
            not isinstance(chapter["labels"], list)
            or any(not isinstance(item, str) for item in chapter["labels"])
            or len(chapter["labels"]) != len(set(chapter["labels"]))
            or not isinstance(chapter["bibitems"], list)
            or any(not isinstance(item, str) for item in chapter["bibitems"])
            or len(chapter["bibitems"]) != len(set(chapter["bibitems"]))
            or not isinstance(chapter["asset_unique"], int)
            or isinstance(chapter["asset_unique"], bool)
            or not isinstance(chapter["eqblocks"], dict)
        ):
            raise BuildError(f"SNAPSHOT_CHAPTER_TYPE:{alias}:{root_name}")
        for key, block in chapter["eqblocks"].items():
            if (
                not isinstance(key, str)
                or not isinstance(block, dict)
                or set(block) != {"hash", "boxed", "file"}
                or not isinstance(block["hash"], str)
                or not isinstance(block["boxed"], bool)
                or not isinstance(block["file"], str)
            ):
                raise BuildError(f"SNAPSHOT_EQBLOCK_SCHEMA:{alias}:{root_name}:{key}")
    line_count = len(data.splitlines())
    return parsed, _evidence_record(
        routes,
        source_blobs,
        path,
        1,
        line_count,
        "STRICT_PARSED_COMPLETE_SNAPSHOT_INPUT",
    )


def _snapshot_chapter(snapshot: dict[str, Any], chapter_number: int) -> dict[str, Any]:
    marker = f"_ch{chapter_number}_"
    matches = [value for key, value in snapshot.items() if marker in key]
    if len(matches) != 1:
        raise BuildError(f"SNAPSHOT_CHAPTER_CARDINALITY:{chapter_number}:{len(matches)}")
    return matches[0]


def _chapter_projection(chapter: dict[str, Any]) -> dict[str, Any]:
    eqblocks = [
        {
            "identifier": identifier,
            "hash": block["hash"],
            "boxed": block["boxed"],
            "file": block["file"],
        }
        for identifier, block in sorted(chapter["eqblocks"].items())
    ]
    return {
        "labels": sorted(chapter["labels"]),
        "eqblocks": eqblocks,
        "asset_unique": chapter["asset_unique"],
        "bibitems": sorted(chapter["bibitems"]),
    }


def _document_projection(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "ch1": _chapter_projection(_snapshot_chapter(snapshot, 1)),
        "ch2": _chapter_projection(_snapshot_chapter(snapshot, 2)),
    }


def _projection_with_sha(value: Any) -> dict[str, Any]:
    return {"projection": value, "projection_sha256": sha256(_canonical_json_bytes(value))}


def _eqblock_map(chapter_projection: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["identifier"]: {
            "hash": item["hash"],
            "boxed": item["boxed"],
            "file": item["file"],
        }
        for item in chapter_projection["eqblocks"]
    }


def _eqblock_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_map = _eqblock_map(before)
    after_map = _eqblock_map(after)
    return {
        "added": [
            {"identifier": key, **after_map[key]} for key in sorted(set(after_map) - set(before_map))
        ],
        "removed": [
            {"identifier": key, **before_map[key]} for key in sorted(set(before_map) - set(after_map))
        ],
        "changed": [
            {"identifier": key, "before": before_map[key], "after": after_map[key]}
            for key in sorted(set(before_map) & set(after_map))
            if before_map[key] != after_map[key]
        ],
    }


def _sorted_substantive_eqblocks(chapter_projection: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        (
            {"hash": item["hash"], "boxed": item["boxed"], "file": item["file"]}
            for item in chapter_projection["eqblocks"]
        ),
        key=lambda item: (item["hash"], item["boxed"], item["file"]),
    )


def _set_delta(before: list[str], after: list[str]) -> dict[str, Any]:
    return {
        "count_before": len(before),
        "count_after": len(after),
        "count_delta": len(after) - len(before),
        "added": sorted(set(after) - set(before)),
        "removed": sorted(set(before) - set(after)),
    }


def _build_snapshot_machine_comparisons(
    routes: list[dict[str, Any]], source_blobs: dict[str, bytes]
) -> list[dict[str, Any]]:
    snapshots: dict[str, dict[str, Any]] = {}
    inputs: dict[str, dict[str, Any]] = {}
    for alias in SNAPSHOT_PATHS:
        snapshots[alias], inputs[alias] = _snapshot_input(routes, source_blobs, alias)
    projections = {alias: _document_projection(snapshot) for alias, snapshot in snapshots.items()}

    baseline_projection = projections["baseline"]
    p0_projection = projections["p0"]
    carry_equal = baseline_projection == p0_projection
    if not carry_equal:
        raise BuildError("SNAPSHOT_0060_PROJECTION_MISMATCH")
    comparison_0060 = {
        "comparison_id": "P061-SNAP-CMP-0060",
        "claim_intent_ids": ["INTENT-PROV-0060"],
        "comparison_kind": "BASELINE_TO_P0_COMPLETE_STRUCTURE_EQUALITY",
        "inputs": [inputs["baseline"], inputs["p0"]],
        "before": _projection_with_sha(baseline_projection),
        "after": _projection_with_sha(p0_projection),
        "exact_equal": carry_equal,
        "asserted_result": "EXACT_EQUAL",
        "authority_ceiling": "STRUCTURE_LINEAGE_ONLY",
        "external_scientific_truth": False,
    }

    expected_bare = {
        "eq:sm-bare": {"hash": "89e15eaa3c66", "boxed": True, "file": "ch1_sec02a_part0.tex"},
        "eq:sm-baremid": {"hash": "ef6644a8eb30", "boxed": False, "file": "ch1_sec02a_part0.tex"},
        "eq:sm-baresum": {"hash": "bc43ee3bcfc6", "boxed": False, "file": "ch1_sec02a_part0.tex"},
    }
    p0_ch1 = projections["p0"]["ch1"]
    p2_ch1 = projections["p2"]["ch1"]
    bare_delta = _eqblock_delta(p0_ch1, p2_ch1)
    actual_bare = {
        item["identifier"]: {key: item[key] for key in ("hash", "boxed", "file")}
        for item in bare_delta["added"]
    }
    if actual_bare != expected_bare or bare_delta["removed"] or bare_delta["changed"]:
        raise BuildError("SNAPSHOT_0061_BARE_TRANSITION_MISMATCH")
    comparison_0061_a = {
        "comparison_id": "P061-SNAP-CMP-0061-A",
        "claim_intent_ids": ["INTENT-PROV-0061"],
        "comparison_kind": "P0_TO_P2_CH1_BARE_SITE_THREE_EQUATIONS",
        "inputs": [inputs["p0"], inputs["p2"]],
        "before": _projection_with_sha(p0_ch1),
        "after": _projection_with_sha(p2_ch1),
        "exact_diff": bare_delta,
        "expected_added": [
            {"identifier": key, **expected_bare[key]} for key in sorted(expected_bare)
        ],
        "asserted_result": "EXACT_THREE_ADDED_NO_REMOVED_OR_CHANGED",
        "authority_ceiling": "STRUCTURE_LINEAGE_ONLY",
        "external_scientific_truth": False,
    }

    expected_later = {
        "eq:lco-mottcrit": {"hash": "1f15a2d56414", "boxed": False, "file": "ch1_sec15_lcoelec.tex"},
        "eq:sm-exch": {"hash": "8518ea77fc55", "boxed": False, "file": "ch1_sec02a_part0.tex"},
        "eq:sm-fdbe": {"hash": "7fe9ef50a5d9", "boxed": False, "file": "ch1_sec02a_part0.tex"},
    }
    p7_ch1 = projections["p7"]["ch1"]
    p7b_ch1 = projections["p7b"]["ch1"]
    later_delta = _eqblock_delta(p7_ch1, p7b_ch1)
    actual_later = {
        item["identifier"]: {key: item[key] for key in ("hash", "boxed", "file")}
        for item in later_delta["added"]
    }
    if actual_later != expected_later or later_delta["removed"] or later_delta["changed"]:
        raise BuildError("SNAPSHOT_0061_LATER_TRANSITION_MISMATCH")
    comparison_0061_b = {
        "comparison_id": "P061-SNAP-CMP-0061-B",
        "claim_intent_ids": ["INTENT-PROV-0061"],
        "comparison_kind": "P7_TO_P7B_CH1_EXCHANGE_FDBE_MOTT_THREE_EQUATIONS",
        "inputs": [inputs["p7"], inputs["p7b"]],
        "before": _projection_with_sha(p7_ch1),
        "after": _projection_with_sha(p7b_ch1),
        "exact_diff": later_delta,
        "expected_added": [
            {"identifier": key, **expected_later[key]} for key in sorted(expected_later)
        ],
        "asserted_result": "EXACT_THREE_ADDED_NO_REMOVED_OR_CHANGED",
        "authority_ceiling": "STRUCTURE_LINEAGE_ONLY",
        "external_scientific_truth": False,
    }

    p6_ch2 = projections["p6"]["ch2"]
    p7_ch2 = projections["p7"]["ch2"]
    move_delta = _eqblock_delta(p6_ch2, p7_ch2)
    expected_moves = {
        "ch2_sec00_intro.tex:44": "ch2_sec00_intro.tex:45",
        "ch2_sec08_synthesis.tex:49": "ch2_sec08_synthesis.tex:52",
        "ch2_sec08_synthesis.tex:78": "ch2_sec08_synthesis.tex:81",
        "ch2_sec08_synthesis.tex:96": "ch2_sec08_synthesis.tex:99",
    }
    removed_map = {
        item["identifier"]: {key: item[key] for key in ("hash", "boxed", "file")}
        for item in move_delta["removed"]
    }
    added_map = {
        item["identifier"]: {key: item[key] for key in ("hash", "boxed", "file")}
        for item in move_delta["added"]
    }
    moves = [
        {
            "before_identifier": old_key,
            "after_identifier": new_key,
            "before": removed_map.get(old_key),
            "after": added_map.get(new_key),
            "content_equal": removed_map.get(old_key) == added_map.get(new_key),
        }
        for old_key, new_key in sorted(expected_moves.items())
    ]
    if (
        set(removed_map) != set(expected_moves)
        or set(added_map) != set(expected_moves.values())
        or move_delta["changed"]
        or not all(move["content_equal"] for move in moves)
    ):
        raise BuildError("SNAPSHOT_0062_MOVE_RECONSTRUCTION_MISMATCH")
    comparison_0062 = {
        "comparison_id": "P061-SNAP-CMP-0062",
        "claim_intent_ids": ["INTENT-PROV-0062"],
        "comparison_kind": "P6_TO_P7_CH2_FOUR_LINE_ADDRESSED_KEY_MOVES",
        "inputs": [inputs["p6"], inputs["p7"]],
        "before": _projection_with_sha(p6_ch2),
        "after": _projection_with_sha(p7_ch2),
        "exact_diff": move_delta,
        "exact_moves": moves,
        "asserted_result": "FOUR_KEYS_MOVED_WITH_EQUAL_HASH_BOXED_FILE_VALUES",
        "authority_ceiling": "STRUCTURE_LINEAGE_ONLY",
        "external_scientific_truth": False,
    }

    appendix_root = "appendix_phase_separation.tex"
    prefinal_aliases = ("p0", "p2", "p3", "p4", "p5", "p6", "p7", "p7b")
    prefinal_roots = {
        alias: sorted(snapshots[alias]) for alias in prefinal_aliases
    }
    final_roots = sorted(snapshots["final"])
    prefinal_appendix_occurrences = {
        alias: [root for root in roots if root == appendix_root]
        for alias, roots in prefinal_roots.items()
    }
    final_appendix_occurrences = [root for root in final_roots if root == appendix_root]
    if any(prefinal_appendix_occurrences.values()):
        raise BuildError("SNAPSHOT_0063_PREFINAL_APPENDIX_FALSE_ABSENCE")
    if final_appendix_occurrences != [appendix_root] or len(final_roots) != 3:
        raise BuildError("SNAPSHOT_0063_FINAL_ROOT_MISMATCH")
    root_genealogy_projection = {
        "prefinal_roots": prefinal_roots,
        "prefinal_appendix_occurrences": prefinal_appendix_occurrences,
        "final_roots": final_roots,
        "final_appendix_occurrences": final_appendix_occurrences,
    }
    comparison_0063 = {
        "comparison_id": "P061-SNAP-CMP-0063",
        "claim_intent_ids": ["INTENT-PROV-0063"],
        "comparison_kind": "EXACT_EIGHT_PREFINAL_APPENDIX_ABSENCE_AND_FINAL_SINGLE_ROOT_PRESENCE",
        "inputs": [inputs[alias] for alias in (*prefinal_aliases, "final")],
        "root_genealogy": _projection_with_sha(root_genealogy_projection),
        "prefinal_snapshot_aliases": list(prefinal_aliases),
        "prefinal_appendix_root_occurrences": 0,
        "final_appendix_root_occurrences": 1,
        "asserted_result": "PREFINAL_GROUND_NOT_FOUND_FINAL_FIRST_OCCURRENCE_CONFIRMED",
        "authority_ceiling": "STRUCTURE_LINEAGE_ONLY",
        "external_scientific_truth": False,
    }

    final_projection = projections["final"]
    ch1_before = baseline_projection["ch1"]
    ch1_after = final_projection["ch1"]
    ch2_before = baseline_projection["ch2"]
    ch2_after = final_projection["ch2"]
    ch1_eq_delta = _eqblock_delta(ch1_before, ch1_after)
    ch2_eq_delta = _eqblock_delta(ch2_before, ch2_after)
    ch2_substantive_before = _sorted_substantive_eqblocks(ch2_before)
    ch2_substantive_after = _sorted_substantive_eqblocks(ch2_after)
    final_delta = {
        "ch1": {
            "labels": _set_delta(ch1_before["labels"], ch1_after["labels"]),
            "eqblock_count_before": len(ch1_before["eqblocks"]),
            "eqblock_count_after": len(ch1_after["eqblocks"]),
            "eqblock_count_delta": len(ch1_after["eqblocks"]) - len(ch1_before["eqblocks"]),
            "eqblock_exact_diff": ch1_eq_delta,
            "bibitems": _set_delta(ch1_before["bibitems"], ch1_after["bibitems"]),
            "asset_unique_before": ch1_before["asset_unique"],
            "asset_unique_after": ch1_after["asset_unique"],
            "asset_unique_unchanged": ch1_before["asset_unique"] == ch1_after["asset_unique"],
        },
        "ch2": {
            "labels": _set_delta(ch2_before["labels"], ch2_after["labels"]),
            "eqblock_count_before": len(ch2_before["eqblocks"]),
            "eqblock_count_after": len(ch2_after["eqblocks"]),
            "eqblock_count_delta": len(ch2_after["eqblocks"]) - len(ch2_before["eqblocks"]),
            "eqblock_exact_diff": ch2_eq_delta,
            "substantive_eqblocks_before": _projection_with_sha(ch2_substantive_before),
            "substantive_eqblocks_after": _projection_with_sha(ch2_substantive_after),
            "substantive_eqblocks_equal": ch2_substantive_before == ch2_substantive_after,
            "bibitems": _set_delta(ch2_before["bibitems"], ch2_after["bibitems"]),
            "asset_unique_before": ch2_before["asset_unique"],
            "asset_unique_after": ch2_after["asset_unique"],
            "asset_unique_unchanged": ch2_before["asset_unique"] == ch2_after["asset_unique"],
        },
    }
    expected_ch1_labels = {
        "eq:lco-mottcrit", "eq:sm-bare", "eq:sm-baremid", "eq:sm-baresum", "eq:sm-exch", "eq:sm-fdbe"
    }
    if (
        final_delta["ch1"]["labels"]["count_delta"] != 6
        or set(final_delta["ch1"]["labels"]["added"]) != expected_ch1_labels
        or final_delta["ch1"]["labels"]["removed"]
        or final_delta["ch1"]["eqblock_count_delta"] != 6
        or final_delta["ch1"]["bibitems"]["count_delta"] != 8
        or final_delta["ch1"]["asset_unique_before"] != 336
        or not final_delta["ch1"]["asset_unique_unchanged"]
        or final_delta["ch2"]["labels"]["count_delta"] != 0
        or final_delta["ch2"]["eqblock_count_delta"] != 0
        or not final_delta["ch2"]["substantive_eqblocks_equal"]
        or final_delta["ch2"]["bibitems"]["count_delta"] != 2
        or final_delta["ch2"]["asset_unique_before"] != 21
        or not final_delta["ch2"]["asset_unique_unchanged"]
    ):
        raise BuildError("SNAPSHOT_0065_RELEASE_DELTA_MISMATCH")
    comparison_0065 = {
        "comparison_id": "P061-SNAP-CMP-0065",
        "claim_intent_ids": ["INTENT-PROV-0065"],
        "comparison_kind": "BASELINE_TO_FINAL_CHAPTER_STRUCTURE_DELTA",
        "inputs": [inputs["baseline"], inputs["final"]],
        "before": _projection_with_sha(baseline_projection),
        "after": _projection_with_sha(final_projection),
        "exact_delta": final_delta,
        "asserted_result": "CH1_PLUS_6_LABELS_6_EQBLOCKS_8_BIB_ASSET336_CH2_0_LABELS_0_SUBSTANTIVE_EQBLOCKS_2_BIB_ASSET21",
        "authority_ceiling": "STRUCTURE_LINEAGE_ONLY",
        "external_scientific_truth": False,
    }
    result = [
        comparison_0060,
        comparison_0061_a,
        comparison_0061_b,
        comparison_0062,
        comparison_0063,
        comparison_0065,
    ]
    if [row["comparison_id"] for row in result] != [
        "P061-SNAP-CMP-0060",
        "P061-SNAP-CMP-0061-A",
        "P061-SNAP-CMP-0061-B",
        "P061-SNAP-CMP-0062",
        "P061-SNAP-CMP-0063",
        "P061-SNAP-CMP-0065",
    ]:
        raise BuildError("SNAPSHOT_COMPARISON_IDENTITY")
    return result


def _observation_record(
    number: int, observation_blobs: dict[str, bytes]
) -> tuple[dict[str, Any], str]:
    path, line_start, line_end = OBSERVATION_RANGES[number]
    data = observation_blobs[path]
    sliced = _line_slice(data, line_start, line_end)
    first = sliced.decode("utf-8").splitlines()[0]
    match = re.fullmatch(rf"### INTENT-PROV-{number:04d} — (.+)", first)
    if match is None:
        raise BuildError(f"OBSERVATION_RANGE_HEADING:{number}:{first}")
    return (
        {
            "path": path,
            "input_commit": INPUT_COMMIT,
            "blob_sha1": blob_sha1(data),
            "line_start": line_start,
            "line_end": line_end,
            "slice_sha256_lf": sha256(sliced),
            "status": "PROVISIONAL_OBSERVATION_ONLY_NOT_EVIDENCE",
        },
        match.group(1),
    )


def _build_contradictions(
    routes: list[dict[str, Any]], source_blobs: dict[str, bytes]
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for contradiction_id in sorted(CONTRADICTION_SPECS):
        spec = CONTRADICTION_SPECS[contradiction_id]
        anchors = [
            _evidence_record(routes, source_blobs, path, start, end, status)
            for path, start, end, status in spec["anchors"]
        ]
        result.append(
            {
                "contradiction_id": contradiction_id,
                "kind": spec["kind"],
                "status": spec["status"],
                "description": spec["description"],
                "anchors": anchors,
                "missing_routes": list(spec.get("missing_routes", ())),
                "external_scientific_truth": False,
            }
        )
    return result


def _parse_claims(
    routes: list[dict[str, Any]],
    source_blobs: dict[str, bytes],
    observation_blobs: dict[str, bytes],
    contradiction_ids: set[str],
) -> list[dict[str, Any]]:
    if set(CLAIM_SPECS) != set(range(26, 66)):
        raise BuildError(f"CLAIM_SPEC_SET:{sorted(CLAIM_SPECS)}")
    claims: list[dict[str, Any]] = []
    for number in range(26, 66):
        spec = CLAIM_SPECS[number]
        claim_type = spec["claim_type"]
        if claim_type not in ALLOWED_CLAIM_TYPES:
            raise BuildError(f"CLAIM_TYPE_INVALID:{number}:{claim_type}")
        observation, title = _observation_record(number, observation_blobs)
        claim_class = _claim_class(number)
        primary_path, primary_start, primary_end = spec["primary"]
        claimant = _evidence_record(
            routes,
            source_blobs,
            primary_path,
            primary_start,
            primary_end,
            "FROZEN_PRIMARY_CLAIMANT",
        )
        if number in USER_REQUIREMENT_CLAIMS:
            claimant["evidence_status"] = (
                "FROZEN_SECOND_ORDER_REQUIREMENT_RECORD_NOT_ORIGINAL_USER_TRANSCRIPT"
            )
        actual_evidence = [
            _evidence_record(routes, source_blobs, path, start, end, status)
            for path, start, end, status in spec["evidence"]
        ]
        attached = tuple(spec.get("contradictions", ()))
        if not set(attached).issubset(contradiction_ids):
            raise BuildError(f"CLAIM_CONTRADICTION_ORPHAN:{number}:{attached}")

        adoption_targets = []
        for path, start, end in spec.get("adoption", ()):
            target = _evidence_record(
                routes, source_blobs, path, start, end, "ADOPTED_RELEASE_TARGET"
            )
            if target["source_authority_class"] != "ADOPTED_RELEASE_SOURCE":
                raise BuildError(f"ADOPTION_TARGET_AUTHORITY:{number}:{path}")
            adoption_targets.append(target)
        if adoption_targets:
            adoption_state = "PRESENT"
            adoption_edge: dict[str, Any] | None = {
                "edge_type": "PROCESS_CLAIM_TO_ADOPTED_RELEASE_SOURCE",
                "targets": adoption_targets,
            }
        else:
            adoption_state = spec.get(
                "adoption_state",
                "NOT_ADOPTED" if claim_class == "COMPETING_DRAFT" else "NOT_APPLICABLE",
            )
            adoption_edge = None

        if "status" in spec:
            status = spec["status"]
        elif number == 42:
            status = "OPEN_EXPERIMENTAL_CLOSURE"
        elif number == 50:
            status = "CONFIRMED_ADOPTED_PROCEDURE_NUMERIC_GATES_UNVERIFIED"
        elif number == 61:
            status = "CONFIRMED_ADOPTED_RELEASE_PRESENCE"
        elif claim_class == "EXTERNAL_SCIENTIFIC_UNVERIFIED":
            status = "UNVERIFIED"
        elif adoption_state == "NOT_ADOPTED":
            status = "PROVISIONAL_NOT_ADOPTED" if claim_class == "COMPETING_DRAFT" else "CONFIRMED_NOT_ADOPTED"
        else:
            status = "CONFIRMED_WITHIN_AUTHORITY_CEILING"

        if number in {28, 31, 43, 53, 59}:
            target_phase, target_step = 71, None
        elif number in {42, 45, 50}:
            target_phase, target_step = 67, None
        elif number in {46, 48, 52, 54, 55}:
            target_phase, target_step = 62, None
        elif number >= 60:
            target_phase, target_step = 61, "48"
        elif number in {39, 44, 49, 57, 58}:
            target_phase, target_step = 61, "50"
        else:
            target_phase, target_step = 61, "47"
        authority_ceiling = CLASS_CEILINGS[claim_class]
        if number == 42:
            authority_ceiling = "INTERNAL_REVIEW_ONLY_OPEN_TWO_PHASE_T_LAW"
        elif number == 50:
            authority_ceiling = "ADOPTED_STAGED_IDENTIFICATION_ONLY_NUMERIC_GATES_UNVERIFIED"
        machine_comparison_ids = {
            60: ["P061-SNAP-CMP-0060"],
            61: ["P061-SNAP-CMP-0061-A", "P061-SNAP-CMP-0061-B"],
            62: ["P061-SNAP-CMP-0062"],
            63: ["P061-SNAP-CMP-0063"],
            65: ["P061-SNAP-CMP-0065"],
        }.get(number, [])

        claims.append(
            {
                "claim_id": f"P061-PROC-{number:04d}",
                "intent_id": f"INTENT-PROV-{number:04d}",
                "provisional_observation": observation,
                "claimant": claimant,
                "object": {"kind": "CURATED_PROCESS_OR_SCIENCE_CLAIM", "title": title},
                "claim_type": claim_type,
                "expected_evidence": {
                    "semantic_standard": spec["expected"],
                    "minimum_actual_anchors": len(spec["evidence"]),
                    "external_primary_required_for_scientific_truth": claim_type == "scientific",
                    "original_independent_user_transcript_required_for_first_order_requirement_authority": number in USER_REQUIREMENT_CLAIMS,
                },
                "actual_evidence": actual_evidence,
                "evidence_route_ids": sorted({item["source_id"] for item in actual_evidence}),
                "evidence_gap": {
                    "status": "OPEN_AUTHORITY_CEILING",
                    "description": spec["gap"],
                    "original_independent_user_transcript": (
                        "GROUND_NOT_FOUND_IN_FROZEN_232_SOURCE_CORPUS"
                        if number in USER_REQUIREMENT_CLAIMS
                        else "NOT_APPLICABLE"
                    ),
                    "frozen_plan_or_process_record_role": (
                        "SECOND_ORDER_REQUIREMENT_EVIDENCE_ONLY_NO_PROMOTION"
                        if number in USER_REQUIREMENT_CLAIMS
                        else "NOT_APPLICABLE"
                    ),
                },
                "machine_comparison_ids": machine_comparison_ids,
                "adoption_edge_state": adoption_state,
                "adoption_edge": adoption_edge,
                "contradiction_ids": list(attached),
                "contradiction": (
                    None
                    if not attached
                    else {"exact_table_reference": True, "contradiction_ids": list(attached)}
                ),
                "claim_authority_class": claim_class,
                "authority_ceiling": authority_ceiling,
                "status": status,
                "components": (
                    {
                        "final_first_occurrence": {
                            "status": "CONFIRMED",
                            "evidence": actual_evidence[0],
                            "machine_comparison_id": "P061-SNAP-CMP-0063",
                            "exact_appendix_root_occurrences": 1,
                        },
                        "prefinal_genealogy": {
                            "status": "GROUND_NOT_FOUND",
                            "exact_snapshot_occurrences": [
                                SNAPSHOT_PATHS[alias]
                                for alias in ("p0", "p2", "p3", "p4", "p5", "p6", "p7", "p7b")
                            ],
                            "exact_appendix_root_occurrences": 0,
                            "machine_comparison_id": "P061-SNAP-CMP-0063",
                        },
                    }
                    if number == 63
                    else None
                ),
                "target_phase": target_phase,
                "target_step": target_step,
                "external_scientific_truth": False,
                "scientific_authority_promoted": False,
            }
        )
    if {claim["claim_type"] for claim in claims} != set(ALLOWED_CLAIM_TYPES):
        raise BuildError("CLAIM_TYPE_COVERAGE")
    return claims


def _phase_table(
    routes: list[dict[str, Any]], source_blobs: dict[str, bytes]
) -> list[dict[str, Any]]:
    rows = (
        (0, "1-10", "1-10", "PLAN_P0_setup.md", "RESULT_P0_setup.md", "STEP_LOG_P0.md", "PASS_P0_SETUP", "ALIGNED"),
        (1, "11-22", "11-22", "PLAN_P1_references.md", "RESULT_P1_references.md", "STEP_LOG_P1.md", "PASS_P1_REFERENCE_LEDGER", "PLAN_CHANGED_BIB_EDIT"),
        (2, "23-32", "23-32", "PLAN_P2_part0.md", "RESULT_P2_part0.md", "STEP_LOG_P2.md", "PASS_P2_PART0", "ALIGNED"),
        (3, "33-44", "33-44 (Step 39 rejected)", "PLAN_P3_graphite.md", "RESULT_P3_graphite.md", "STEP_LOG_P3.md", "PASS_P3_GRAPHITE", "KWW_STEP_REJECTED"),
        (4, "45-62", "45-62 (competition repeated)", "PLAN_P4_lco.md", "RESULT_P4_lco.md", "STEP_LOG_P4.md", "PASS_P4_LCO", "SCOPE_NARROWED_AFTER_FULL_READ"),
        (5, "63-72", "63-72 (environment rebuilt once)", "PLAN_P5_ch2.md", "RESULT_P5_ch2.md", "STEP_LOG_P5.md", "PASS_P5_CH2", "ALIGNED_DISTINCT_P5_SNAPSHOT_OCCURRENCE"),
        (6, "73-80", "73-80", "PLAN_P6_convention.md", "RESULT_P6_convention.md", "STEP_LOG_P6.md", "PASS_P6_CONVENTION", "PARTLY_SUPERSEDED_BY_P7_USER_DIRECTIVE"),
        (7, "81-90", "81-90 (two interruptions and restarts)", "PLAN_P7_review.md", "RESULT_P7_review.md", "STEP_LOG_P7.md", "PASS_P7_REVIEW", "REVIEW_COUNT_DRIFT_4_10_11"),
        (8, "91-98", "91-98 (one cap interruption and restart)", "PLAN_P8_closing.md", None, None, "PASS_P8_CLOSING", "DEDICATED_RESULT_AND_LOG_GROUND_NOT_FOUND_HANDOVER_SUBSTITUTE"),
    )
    table: list[dict[str, Any]] = []
    for phase, planned, actual, plan_name, result_name, log_name, gate, relation in rows:
        plan_path = PLAN + plan_name
        plan_route = _route_by_path(routes, plan_path)
        plan_start, plan_end = PLAN_ANCHOR_RANGES[phase]
        result_path = None if result_name is None else RESULT + result_name
        log_path = None if log_name is None else RESULT + log_name
        result_route = None if result_path is None else _route_by_path(routes, result_path)
        log_route = None if log_path is None else _route_by_path(routes, log_path)
        table.append(
            {
                "phase": f"P{phase}",
                "planned_steps": planned,
                "actual_steps": actual,
                "gate": gate,
                "plan": {"path": plan_path, "source_id": plan_route["source_id"]},
                "plan_anchor": _evidence_record(
                    routes,
                    source_blobs,
                    plan_path,
                    plan_start,
                    plan_end,
                    "BOUNDED_PHASE_PLAN_STEPS_ANCHOR",
                ),
                "result": None if result_route is None else {"path": result_path, "source_id": result_route["source_id"]},
                "step_log": None if log_route is None else {"path": log_path, "source_id": log_route["source_id"]},
                "ledger_anchor": _evidence_record(
                    routes,
                    source_blobs,
                    RESULT + "V1020_EXECUTION_LEDGER.md",
                    phase + 8,
                    phase + 8,
                    "EXACT_PHASE_LEDGER_ROW",
                ),
                "relation": relation,
                "process_status": "PROCESS_REPORTED_PASS_WITH_CONCERNS",
                "completion_authority_ceiling": "INTERNAL_PROCESS_ONLY",
                "external_scientific_truth": False,
                "dedicated_result_path_state": "GROUND_NOT_FOUND" if phase == 8 else "PRESENT",
                "dedicated_step_log_path_state": "GROUND_NOT_FOUND" if phase == 8 else "PRESENT",
                "substitute_result": (
                    {
                        "path": RELEASE + "HANDOVER_v1.0.20.md",
                        "source_id": _route_by_path(routes, RELEASE + "HANDOVER_v1.0.20.md")["source_id"],
                        "line_start": 21,
                        "line_end": 29,
                        "slice_sha256_lf": sha256(_line_slice(source_blobs[RELEASE + "HANDOVER_v1.0.20.md"], 21, 29)),
                    }
                    if phase == 8
                    else None
                ),
            }
        )
    if any(
        (row["plan_anchor"]["line_start"], row["plan_anchor"]["line_end"])
        != PLAN_ANCHOR_RANGES[index]
        or not row["plan_anchor"]["slice_sha256_lf"]
        for index, row in enumerate(table)
    ):
        raise BuildError("PHASE_PLAN_ANCHOR_MISMATCH")
    p8 = table[8]
    if (
        p8["phase"] != "P8"
        or p8["plan_anchor"]["path"] != PLAN + "PLAN_P8_closing.md"
        or p8["plan_anchor"]["line_start"] != 15
        or p8["plan_anchor"]["line_end"] != 25
        or not p8["plan_anchor"]["slice_sha256_lf"]
    ):
        raise BuildError("P8_PLAN_ANCHOR_MISMATCH")
    return table


def _historical_boundaries(repo: Path, routes: list[dict[str, Any]]) -> dict[str, Any]:
    p5 = "730fc4087c7534aaa46433016ae98a1cc3d97c21"
    p6 = "8df0864d9522ec6fab29c52a473659f02ac195b6"
    p8_build = "ba41c9052e9b177268ef65e115dda500d0af3856"
    p8_close = "c70bcb6f4e2ca0eba6f1b9cfbb0cff7c2f88d862"
    parent = _run_git_bytes(
        repo, ["rev-parse", f"{p6}^"], "P5_P6_PARENT_REV_PARSE"
    ).decode("ascii", errors="strict").strip()
    if parent != p5:
        raise BuildError("P5_P6_PARENT_MISMATCH")
    changed = _run_git_bytes(
        repo,
        ["diff", "--name-only", p5, p6, "--", "Claude/docs/v1.0.20"],
        "P5_P6_DIFF",
    ).decode("utf-8", errors="strict").splitlines()
    changed_tex = sorted(path for path in changed if path.endswith(".tex"))
    expected_tex = sorted(
        [
            "Claude/docs/v1.0.20/_sections/ch1_appB_codemap.tex",
            "Claude/docs/v1.0.20/_sections/ch1_sec00_intro.tex",
            "Claude/docs/v1.0.20/appendix_phase_separation.tex",
        ]
    )
    if changed_tex != expected_tex:
        raise BuildError(f"P5_P6_SOURCE_DELTA:{changed_tex}")
    close_parent = _run_git_bytes(
        repo, ["rev-parse", f"{p8_close}^"], "P8_CLOSE_PARENT_REV_PARSE"
    ).decode("ascii", errors="strict").strip()
    if close_parent != p8_build:
        raise BuildError("P8_CLOSE_PARENT_MISMATCH")
    if not _git_is_ancestor(repo, p8_close, BASELINE_COMMIT, "P8_BASELINE_ANCESTRY"):
        raise BuildError("P8_CLOSE_NOT_IN_BASELINE")
    p8_chain = [
        "66e3510d67162dd6bd88158557f96621cbedbbcf",
        "c8853c83d79f22059e07c2a548759da6e8310d2d",
        "eb2cd1a32471a40de5511ed159aedf8272792a8a",
        "a0ae6b41e80983940e13851467a07b47e76531f6",
        "1e6c610f11682d87a416957b1cf65b4c8df53697",
        p8_build,
        p8_close,
    ]
    for previous, current in zip(p8_chain, p8_chain[1:]):
        actual_parent = _run_git_bytes(
            repo, ["rev-parse", f"{current}^"], f"P8_CHAIN_PARENT:{current}"
        ).decode("ascii", errors="strict").strip()
        if actual_parent != previous:
            raise BuildError(f"P8_CHAIN_PARENT_MISMATCH:{current}:{actual_parent}")
    p5_route = _resolve_selectors(("snapshot_v1020_p5.json",), routes)[0]
    p6_route = _resolve_selectors(("snapshot_v1020_p6.json",), routes)[0]
    return {
        "p5_p6": {
            "p5_commit": p5,
            "p6_commit": p6,
            "direct_parent": True,
            "snapshot_occurrences_distinct": True,
            "snapshot_blob_identical": p5_route["blob_sha1"] == p6_route["blob_sha1"],
            "snapshot_blob_sha1": p5_route["blob_sha1"],
            "snapshot_sha256": p5_route["sha256"],
            "actual_source_tree_identical": False,
            "changed_tex_paths": changed_tex,
            "authority_ceiling": "CAPTURED_STRUCTURE_ONLY",
        },
        "p8": {
            "build_commit": p8_build,
            "closing_commit": p8_close,
            "closing_parent_verified": True,
            "closing_in_frozen_baseline_ancestry": True,
            "dedicated_result_path_state": "GROUND_NOT_FOUND",
            "dedicated_step_log_path_state": "GROUND_NOT_FOUND",
            "substitute_result_path": "Claude/docs/v1.0.20/HANDOVER_v1.0.20.md",
            "completion_evidence_state": "CONFIRMED_INTERNAL_WITH_HANDOVER_LEDGER_GIT",
            "complete_commit_chain": p8_chain,
            "complete_commit_chain_parent_verified": True,
            "authority_ceiling": "INTERNAL_PROCESS_ONLY",
        },
    }


def build(repo: Path) -> dict[str, Any]:
    topology_bytes = git_blob(repo, INPUT_COMMIT, TOPOLOGY_PATH.as_posix())
    normalized_topology = lf_bytes(topology_bytes)
    if sha256(normalized_topology) != TOPOLOGY_SHA256_LF:
        raise BuildError("TOPOLOGY_FROZEN_HASH_MISMATCH")
    topology = strict_load_bytes(topology_bytes)
    _walk_finite(topology)
    if not isinstance(topology, dict):
        raise BuildError("TOPOLOGY_NOT_OBJECT")
    sources, source_blobs, frozen_source_validation = _validate_topology(repo, topology)
    routes = _source_routes(sources, source_blobs)
    snapshot_machine_comparisons = _build_snapshot_machine_comparisons(
        routes, source_blobs
    )
    observation_blobs = {
        relative: git_blob(repo, INPUT_COMMIT, relative) for relative in OBSERVATION_FILES
    }
    contradictions = _build_contradictions(routes, source_blobs)
    claims = _parse_claims(
        routes,
        source_blobs,
        observation_blobs,
        {row["contradiction_id"] for row in contradictions},
    )
    phase_table = _phase_table(routes, source_blobs)
    boundaries = _historical_boundaries(repo, routes)
    routed_classes = {route["source_authority_class"] for route in routes}
    claim_classes = {claim["claim_authority_class"] for claim in claims}
    if routed_classes | claim_classes != set(ALLOWED_AUTHORITY_CLASSES):
        raise BuildError("AUTHORITY_CLASS_COVERAGE")
    if any(claim["scientific_authority_promoted"] for claim in claims):
        raise BuildError("CLAIM_SCIENCE_PROMOTION")
    if any(route["scientific_authority_promoted"] for route in routes):
        raise BuildError("SOURCE_SCIENCE_PROMOTION")
    route_ids = {route["source_id"] for route in routes}
    for claim in claims:
        if not claim["evidence_route_ids"]:
            raise BuildError(f"CLAIM_EVIDENCE_EMPTY:{claim['claim_id']}")
        if not set(claim["evidence_route_ids"]).issubset(route_ids):
            raise BuildError(f"CLAIM_EVIDENCE_ORPHAN:{claim['claim_id']}")
        if claim["claimant"]["source_id"] not in route_ids:
            raise BuildError(f"CLAIMANT_ORPHAN:{claim['claim_id']}")
        if claim["claimant"]["line_start"] < 1 or not claim["claimant"]["slice_sha256_lf"]:
            raise BuildError(f"CLAIMANT_RANGE_OR_HASH:{claim['claim_id']}")
        if any(not item["slice_sha256_lf"] for item in claim["actual_evidence"]):
            raise BuildError(f"EVIDENCE_SLICE_HASH:{claim['claim_id']}")

    by_intent = {claim["intent_id"]: claim for claim in claims}
    referenced_contradictions = {
        contradiction_id
        for claim in claims
        for contradiction_id in claim["contradiction_ids"]
    }
    if referenced_contradictions != {row["contradiction_id"] for row in contradictions}:
        raise BuildError("CONTRADICTION_ATTACHMENT_COVERAGE")
    if sum(claim["adoption_edge_state"] == "PRESENT" for claim in claims) != 3:
        raise BuildError("CLAIM_ADOPTION_COUNT")
    if by_intent["INTENT-PROV-0036"]["adoption_edge"] is not None or by_intent["INTENT-PROV-0037"]["adoption_edge"] is not None:
        raise BuildError("INVALID_PROCESS_ADOPTION_EDGE")
    if len(by_intent["INTENT-PROV-0061"]["adoption_edge"]["targets"]) != 2:
        raise BuildError("CLAIM_0061_ADOPTION_TARGETS")
    if {
        (target["path"], target["line_start"], target["line_end"])
        for target in by_intent["INTENT-PROV-0061"]["adoption_edge"]["targets"]
    } != {
        (SECTION + "ch1_sec02a_part0.tex", 132, 195),
        (SECTION + "ch1_sec15_lcoelec.tex", 39, 46),
    }:
        raise BuildError("CLAIM_0061_ADOPTION_TARGET_MISMATCH")
    if by_intent["INTENT-PROV-0063"]["status"] != "CONFIRMED_WITH_GROUND_NOT_FOUND_SUBCLAIM":
        raise BuildError("CLAIM_0063_COMPONENT_STATUS")
    if [
        (item["path"], item["line_start"], item["line_end"])
        for item in by_intent["INTENT-PROV-0062"]["actual_evidence"]
    ] != [
        (SNAPSHOT_PATHS["p6"], 967, 970),
        (SNAPSHOT_PATHS["p6"], 1112, 1125),
        (SNAPSHOT_PATHS["p7"], 967, 970),
        (SNAPSHOT_PATHS["p7"], 1112, 1125),
    ]:
        raise BuildError("CLAIM_0062_EVIDENCE_RANGE_MISMATCH")
    machine_ids = {
        row["comparison_id"] for row in snapshot_machine_comparisons
    }
    referenced_machine_ids = {
        comparison_id
        for claim in claims
        for comparison_id in claim["machine_comparison_ids"]
    }
    if referenced_machine_ids != machine_ids:
        raise BuildError("SNAPSHOT_COMPARISON_CLAIM_COVERAGE")
    user_claims = [
        claim for claim in claims if claim["claim_authority_class"] == "USER_REQUIREMENT"
    ]
    if len(user_claims) != 8 or {
        int(claim["intent_id"].rsplit("-", 1)[-1]) for claim in user_claims
    } != USER_REQUIREMENT_CLAIMS:
        raise BuildError("USER_REQUIREMENT_CLAIM_IDENTITY")
    if any(
        claim["claimant"]["evidence_status"]
        != "FROZEN_SECOND_ORDER_REQUIREMENT_RECORD_NOT_ORIGINAL_USER_TRANSCRIPT"
        or claim["evidence_gap"]["original_independent_user_transcript"]
        != "GROUND_NOT_FOUND_IN_FROZEN_232_SOURCE_CORPUS"
        or claim["evidence_gap"]["frozen_plan_or_process_record_role"]
        != "SECOND_ORDER_REQUIREMENT_EVIDENCE_ONLY_NO_PROMOTION"
        or claim["authority_ceiling"]
        != "RECORDED_SECOND_ORDER_REQUIREMENT_ONLY_ORIGINAL_USER_TRANSCRIPT_GROUND_NOT_FOUND"
        for claim in user_claims
    ):
        raise BuildError("USER_REQUIREMENT_TRANSCRIPT_CEILING")

    direction_routes = [route for route in routes if "/DIRECTION_" in route["path"]]
    if not direction_routes or any(route["source_authority_class"] != "EXTERNAL_SCIENTIFIC_UNVERIFIED" for route in direction_routes):
        raise BuildError("DIRECTION_SOURCE_ROUTE")
    author_briefs = [route for route in routes if route["path"].endswith("/AUTHOR_BRIEF.md")]
    if len(author_briefs) != 2 or any(route["source_authority_class"] != "PLAN_INTENT" for route in author_briefs):
        raise BuildError("AUTHOR_BRIEF_SOURCE_ROUTE")
    interchapter = [route for route in routes if route["path"].endswith("/INTERCHAPTER_REPORT.md")]
    if len(interchapter) != 1 or interchapter[0]["source_authority_class"] != "INTERNAL_REVIEW":
        raise BuildError("INTERCHAPTER_SOURCE_ROUTE")
    adopted = [route for route in routes if route["source_authority_class"] == "ADOPTED_RELEASE_SOURCE"]
    if any(route["adoption_topology"] is None for route in adopted):
        raise BuildError("ADOPTED_RELEASE_TOPOLOGY_MISSING")

    basenames = {route["path"].rsplit("/", 1)[-1] for route in routes}
    if any(name.startswith("RESULT_P8") or name.startswith("STEP_LOG_P8") for name in basenames):
        raise BuildError("P8_DEDICATED_SURFACE_FALSE_PRESENT")
    ground_not_found = [
        {
            "ground_id": "P061-GNF-001",
            "object": "dedicated Phase P8 result path",
            "expected_pattern": "Claude/docs/v1.0.20/results/RESULT_P8*.md",
            "status": "GROUND_NOT_FOUND",
            "substitute_evidence": "Claude/docs/v1.0.20/HANDOVER_v1.0.20.md",
            "target_phase": 61,
            "target_step": "47",
        },
        {
            "ground_id": "P061-GNF-002",
            "object": "dedicated Phase P8 step log path",
            "expected_pattern": "Claude/docs/v1.0.20/results/STEP_LOG_P8*.md",
            "status": "GROUND_NOT_FOUND",
            "substitute_evidence": "Claude/docs/v1.0.20/results/V1020_EXECUTION_LEDGER.md",
            "target_phase": 61,
            "target_step": "47",
        },
        {
            "ground_id": "P061-GNF-003",
            "object": "appendix root in the exact eight pre-final v1.0.20 snapshot occurrences",
            "expected_pattern": "appendix_phase_separation.tex root in p0, p2, p3, p4, p5, p6, p7 or p7b",
            "status": "GROUND_NOT_FOUND",
            "substitute_evidence": "P061-SNAP-CMP-0063 confirms zero pre-final occurrences and one final first occurrence",
            "target_phase": 61,
            "target_step": "48",
        },
        {
            "ground_id": "P061-GNF-004",
            "object": "adoption edge for standalone appendix_phase_separation.tex",
            "expected_pattern": "adopted release root input edge",
            "status": "GROUND_NOT_FOUND",
            "substitute_evidence": "standalone appendix remains COMPETING_DRAFT",
            "target_phase": 62,
            "target_step": None,
        },
        {
            "ground_id": "P061-GNF-005",
            "object": "adoption edge for packaged PNG outputs",
            "expected_pattern": "release-text figure inclusion anchor",
            "status": "GROUND_NOT_FOUND",
            "substitute_evidence": "packaged PNGs remain STRUCTURAL_WITNESS",
            "target_phase": 62,
            "target_step": None,
        },
        {
            "ground_id": "P061-GNF-006",
            "object": "adoption edge for competitive candidates and rendered outputs",
            "expected_pattern": "explicit adopted release source target",
            "status": "GROUND_NOT_FOUND",
            "substitute_evidence": "candidate and review corpus remains non-adopted or structural",
            "target_phase": 62,
            "target_step": None,
        },
        {
            "ground_id": "P061-GNF-007",
            "object": "original independent user transcript for eight USER_REQUIREMENT claims",
            "expected_pattern": "first-order user utterance transcript independent of frozen plan/process records",
            "status": "GROUND_NOT_FOUND",
            "substitute_evidence": "frozen plans and process records are second-order requirement evidence only",
            "affected_intent_ids": [
                f"INTENT-PROV-{number:04d}" for number in sorted(USER_REQUIREMENT_CLAIMS)
            ],
            "promotion_prohibited": True,
            "target_phase": 61,
            "target_step": "47",
        },
    ]
    unverified_queue = [
        {
            "queue_id": "P061-UNV-001",
            "object": "primary DOI and claim-level literature support",
            "status": "UNVERIFIED",
            "required_evidence": "fresh primary-paper read and DOI metadata check for each proposition",
            "target_phase": 71,
        },
        {
            "queue_id": "P061-UNV-002",
            "object": "material-specific and experimental truth",
            "status": "UNVERIFIED",
            "required_evidence": "traceable experimental datasets and material conditions",
            "target_phase": 71,
        },
        {
            "queue_id": "P061-UNV-003",
            "object": "runtime build and code self-report",
            "status": "UNVERIFIED_FRESH_EXECUTION_NOT_RUN",
            "required_evidence": "fresh isolated build/test execution against frozen oracles",
            "target_phase": 67,
        },
        {
            "queue_id": "P061-UNV-004",
            "object": "equation and derivation validity",
            "status": "UNVERIFIED_EXTERNAL",
            "required_evidence": "independent re-derivation and primary-theory review",
            "target_phase": 71,
        },
        {
            "queue_id": "P061-UNV-005",
            "object": "figure numerical and experimental validity",
            "status": "UNVERIFIED",
            "required_evidence": "source-data recreation and experiment/model comparison",
            "target_phase": 67,
        },
        {
            "queue_id": "P061-UNV-006",
            "object": "two-phase temperature law and LCO data gaps",
            "status": "UNVERIFIED",
            "required_evidence": "multi-temperature width, OCV, entropy and tier-2/3 measurements",
            "target_phase": 67,
        },
        {
            "queue_id": "P061-UNV-007",
            "object": "Q2 Q3 and direction-report adoption",
            "status": "NOT_ADOPTED",
            "required_evidence": "approved plan, final derivation, release-text target and adoption edge",
            "target_phase": 62,
        },
        {
            "queue_id": "P061-UNV-008",
            "object": "standalone appendix adoption debt",
            "status": "GROUND_NOT_FOUND",
            "required_evidence": "explicit decision and root inclusion edge",
            "target_phase": 62,
        },
        {
            "queue_id": "P061-UNV-009",
            "object": "packaged PNG adoption debt",
            "status": "GROUND_NOT_FOUND",
            "required_evidence": "release-text figure inclusion anchors and captions",
            "target_phase": 62,
        },
        {
            "queue_id": "P061-UNV-010",
            "object": "competitive candidate adoption debt",
            "status": "GROUND_NOT_FOUND",
            "required_evidence": "curated target slices in adopted release sources",
            "target_phase": 62,
        },
        {
            "queue_id": "P061-UNV-011",
            "object": "original independent user transcript for recorded USER_REQUIREMENT claims",
            "status": "GROUND_NOT_FOUND",
            "required_evidence": "independent first-order user utterance transcript; frozen plans remain second-order evidence",
            "target_phase": 61,
        },
    ]
    if len(ground_not_found) != 7 or ground_not_found[-1]["ground_id"] != "P061-GNF-007":
        raise BuildError("USER_TRANSCRIPT_GNF_ROW")
    if len(unverified_queue) != 11 or unverified_queue[-1]["queue_id"] != "P061-UNV-011":
        raise BuildError("USER_TRANSCRIPT_UNVERIFIED_QUEUE")
    source_class_counts = dict(sorted(Counter(route["source_authority_class"] for route in routes).items()))
    claim_class_counts = dict(sorted(Counter(claim["claim_authority_class"] for claim in claims).items()))
    observation_inputs = []
    for relative in OBSERVATION_FILES:
        data = observation_blobs[relative]
        observation_inputs.append(
            {
                "path": relative,
                "input_commit": INPUT_COMMIT,
                "blob_sha1": blob_sha1(data),
                "sha256_lf_normalized": sha256(lf_bytes(data)),
                "lines": len(data.splitlines()),
                "status": "PROVISIONAL_INPUT_ONLY",
            }
        )
    builder_bytes = Path(__file__).read_bytes()
    required_negative_controls = [
        "DUPLICATE_JSON_KEY",
        "NONFINITE_JSON",
        "INPUT_COMMIT_MISMATCH",
        "TOPOLOGY_FROZEN_HASH_MISMATCH",
        "OBSERVATION_BLOB_MISMATCH",
        "OBSERVATION_RANGE_OR_SLICE_HASH_MISMATCH",
        "MISSING_TOP_FIELD",
        "EXTRA_TOP_FIELD",
        "SOURCE_ROUTE_MISSING",
        "SOURCE_ROUTE_DUPLICATE",
        "SOURCE_ROUTE_ORPHAN",
        "SOURCE_BLOB_MISMATCH",
        "SOURCE_LINE_EXTENT_MISMATCH",
        "PDF_EXTENT_TAMPER",
        "IMAGE_EXTENT_TAMPER",
        "JSON_STRICT_PARSE_TAMPER",
        "SOURCE_AUTHORITY_CLASS_MULTIPLE",
        "SOURCE_AUTHORITY_ROUTE_MISMATCH",
        "ADOPTED_RELEASE_TOPOLOGY_MISSING",
        "ADOPTED_TEX_ORPHAN",
        "DIRECTION_SOURCE_PROMOTED",
        "AUTHOR_BRIEF_NOT_PLAN",
        "INTERCHAPTER_NOT_REVIEW",
        "CLAIM_MISSING",
        "CLAIM_DUPLICATE",
        "CLAIMANT_RANGE_INVALID",
        "CLAIMANT_SLICE_HASH_MISMATCH",
        "CLAIM_TYPE_NOT_SEMANTIC",
        "CLAIM_AUTHORITY_CLASS_INVALID",
        "CLAIM_EVIDENCE_EMPTY",
        "CLAIM_EVIDENCE_ORPHAN",
        "CLAIM_EVIDENCE_RANGE_OR_STATUS_INVALID",
        "CLAIM_EVIDENCE_SLICE_HASH_MISMATCH",
        "CLAIM_EXPECTED_EVIDENCE_OR_GAP_MISSING",
        "CIRCULAR_SELF_CERTIFICATION",
        "ADOPTION_EDGE_REQUIRED_MISSING",
        "ADOPTION_EDGE_SELF_REFERENCE",
        "ADOPTION_EDGE_PROCESS_TARGET",
        "CLAIM_0036_0037_INVALID_ADOPTION",
        "CLAIM_0049_0057_FALSE_ADOPTION",
        "CLAIM_0050_ADOPTION_MISSING",
        "CLAIM_0061_ADOPTION_TARGET_MISMATCH",
        "PLAN_TO_SCIENCE_PROMOTION",
        "REVIEW_TO_PRIMARY_PROMOTION",
        "SNAPSHOT_TO_PHYSICAL_VALIDITY",
        "STRUCTURE_PROJECTION_TAMPER",
        "STRUCTURE_DELTA_TAMPER",
        "TEST_PASS_TO_EXPERIMENT",
        "BIBLIOGRAPHY_PRESENCE_TO_PRIMARY_SUPPORT",
        "P5_P6_OCCURRENCE_COLLAPSE",
        "P5_P6_SNAPSHOT_TO_SOURCE_EQUALITY",
        "UNLABELED_MOVE_AS_ADD_DELETE",
        "APPENDIX_PREFINAL_HISTORY_FALSE",
        "PREFINAL_APPENDIX_FALSE_ABSENCE",
        "SNAPSHOT_0063_INPUT_MISSING",
        "SNAPSHOT_0063_PREFINAL_ROOT_MISMATCH",
        "SNAPSHOT_0063_FINAL_ROOT_MISMATCH",
        "SNAPSHOT_0063_PROJECTION_TAMPER",
        "P8_DEDICATED_RESULT_FALSE_PRESENT",
        "P8_DEDICATED_LOG_FALSE_PRESENT",
        "P8_TOTAL_EVIDENCE_FALSE_GNF",
        "P8_INTERNAL_PASS_TO_SCIENCE",
        "STATUS_CONFIRMED_WITH_GNF_EVIDENCE",
        "CONTRADICTED_WITH_NULL_CONTRADICTION",
        "CONTRADICTION_ROW_MISSING",
        "CONTRADICTION_ANCHOR_HASH_MISMATCH",
        "CONTRADICTION_ATTACHMENT_ORPHAN",
        "PHASE_TABLE_ROW_MISSING",
        "PHASE_TABLE_LEDGER_ANCHOR_MISMATCH",
        "PHASE_TABLE_GATE_OR_STEP_MISMATCH",
        "P8_COMMIT_CHAIN_MISMATCH",
        "USER_TRANSCRIPT_FALSE_PRESENT",
        "P8_PLAN_ANCHOR_MISMATCH",
        "UNVERIFIED_QUEUE_MISSING",
        "EXTERNAL_TRUTH_TRUE",
        "GATE_NOT_PASS_WITH_CONCERNS",
        "TARGET_MISSING",
        "DETERMINISM_MISMATCH",
    ]
    required_review_negatives = {
        "STRUCTURE_PROJECTION_TAMPER",
        "STRUCTURE_DELTA_TAMPER",
        "USER_TRANSCRIPT_FALSE_PRESENT",
        "P8_PLAN_ANCHOR_MISMATCH",
        "PDF_EXTENT_TAMPER",
        "IMAGE_EXTENT_TAMPER",
        "JSON_STRICT_PARSE_TAMPER",
        "PREFINAL_APPENDIX_FALSE_ABSENCE",
        "SNAPSHOT_0063_INPUT_MISSING",
        "SNAPSHOT_0063_PREFINAL_ROOT_MISMATCH",
        "SNAPSHOT_0063_FINAL_ROOT_MISMATCH",
        "SNAPSHOT_0063_PROJECTION_TAMPER",
    }
    if (
        len(required_negative_controls) != len(set(required_negative_controls))
        or not required_review_negatives.issubset(required_negative_controls)
    ):
        raise BuildError("REQUIRED_NEGATIVE_CONTROL_SET")
    return {
        "artifact_kind": "PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX",
        "schema_version": 1,
        "phase": 61,
        "step": "47",
        "status": "PASS_WITH_CONCERNS",
        "gate": "PASS_WITH_CONCERNS",
        "generated_date": "2026-08-26",
        "input_commit": INPUT_COMMIT,
        "baseline_commit": BASELINE_COMMIT,
        "topology": {
            "path": TOPOLOGY_PATH.as_posix(),
            "input_commit": INPUT_COMMIT,
            "blob_sha1": blob_sha1(topology_bytes),
            "sha256_lf_normalized": sha256(normalized_topology),
            "path_set_sha256": topology["path_set_sha256"],
            "path_blob_set_sha256": topology["path_blob_set_sha256"],
            "sources": 232,
            "unique_blobs": 231,
            "full_frozen_blob_validation": True,
        },
        "builder": {
            "path": "Codex/work/v1020_phase061/build_phase061_step47_process_authority.py",
            "sha256_lf_normalized": sha256(lf_bytes(builder_bytes)),
            "production_modules_imported_or_executed": False,
        },
        "authority_classes": list(ALLOWED_AUTHORITY_CLASSES),
        "authority_policy": {
            "source_and_claim_authority_separate": True,
            "exactly_one_class_per_source": True,
            "exactly_one_class_per_claim": True,
            "external_scientific_truth_promoted": False,
            "process_or_review_can_self_certify_science": False,
            "snapshot_or_build_can_certify_physical_validity": False,
            "original_independent_user_transcript_available": False,
            "original_independent_user_transcript_status": "GROUND_NOT_FOUND_IN_FROZEN_232_SOURCE_CORPUS",
            "frozen_plan_and_process_requirement_records": "SECOND_ORDER_EVIDENCE_ONLY",
            "recorded_requirement_promoted_to_first_order_user_transcript": False,
        },
        "observation_inputs": observation_inputs,
        "frozen_source_validation": frozen_source_validation,
        "source_routes": routes,
        "process_source_ids": [
            route["source_id"]
            for route in routes
            if route["source_authority_class"]
            in {"PLAN_INTENT", "PROCESS_SELF_ASSESSMENT", "INTERNAL_REVIEW", "COMPETING_DRAFT", "EXTERNAL_SCIENTIFIC_UNVERIFIED"}
        ],
        "claims": claims,
        "snapshot_machine_comparisons": snapshot_machine_comparisons,
        "contradictions": contradictions,
        "phase_table": phase_table,
        "ground_not_found": ground_not_found,
        "unverified_queue": unverified_queue,
        "boundaries": boundaries,
        "required_negative_controls": required_negative_controls,
        "counts": {
            "source_routes": len(routes),
            "claims": len(claims),
            "snapshot_machine_comparisons": len(snapshot_machine_comparisons),
            "full_text_extents_validated": frozen_source_validation["counts"]["full_text_extents_validated"],
            "strict_json_files_validated": frozen_source_validation["counts"]["strict_json_files_validated"],
            "pdf_extents_validated": frozen_source_validation["counts"]["pdf_extents_validated"],
            "pdf_pages_validated": frozen_source_validation["counts"]["pdf_pages_validated"],
            "image_extents_validated": frozen_source_validation["counts"]["image_extents_validated"],
            "claim_first": claims[0]["intent_id"],
            "claim_last": claims[-1]["intent_id"],
            "phase_rows": len(phase_table),
            "contradictions": len(contradictions),
            "ground_not_found": len(ground_not_found),
            "unverified_queue": len(unverified_queue),
            "adoption_edges_present": sum(claim["adoption_edge_state"] == "PRESENT" for claim in claims),
            "source_authority_classes": source_class_counts,
            "claim_authority_classes": claim_class_counts,
            "external_truth_true": 0,
            "scientific_promotions_true": 0,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    repo = args.repo.resolve()
    payload = build(repo)
    output = args.output if args.output.is_absolute() else repo / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
