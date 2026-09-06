#!/usr/bin/env python3
"""Validate Phase 068 Step 91 Claude-fork full-read evidence.

This validator is intentionally self-contained.  It reconstructs the fixed Git
topology and all source-byte identities without importing the companion builder.
JSON collection is a single-process, result-first/two-JSON-last transaction.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Iterable


SCHEMA_INVENTORY = "P068-STEP91-CLAUDE-DIFF-1"
SCHEMA_ATTESTATION = "P068-STEP91-FULL-READ-1"
EXPECTED_PARENT = "d54d1a2b2378369cbeaef757309b3ed629491d2c"
EXPECTED_PARENT_PARENT = "0371387f582fb63f5c3858d7e6905ed83eee885f"
EXPECTED_PARENT_SUBJECT = "docs(phase068): plan claude codex fork adjudication"
EXPECTED_SUBJECT = "audit(phase068): read claude fork history"
CONTENT_TERMINAL = "PASS_P068_STEP91_CLAUDE_FORK_READ"
PERSISTENCE_TERMINAL = "PASS_P068_STEP91_PERSISTENCE"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
ACTIVE_REMOTE_REF = "refs/remotes/origin/" + ACTIVE_BRANCH
ACTIVE_LIVE_REF = "refs/heads/" + ACTIVE_BRANCH
ACTIVE_UPSTREAM = "origin/" + ACTIVE_BRANCH
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
PROTECTED_LOCAL_REF = "refs/heads/" + PROTECTED_BRANCH
PROTECTED_REMOTE_REF = "refs/remotes/origin/" + PROTECTED_BRANCH
PROTECTED_LIVE_REF = "refs/heads/" + PROTECTED_BRANCH
MAIN_TIP = "f0c381bd6dc315ac75cbffa93dd86ce83a37949b"
MAIN_LOCAL_REF = "refs/heads/main"
MAIN_REMOTE_REF = "refs/remotes/origin/main"
MAIN_LIVE_REF = "refs/heads/main"
CLAUDE_REMOTE_REF = "refs/remotes/origin/claude/version-1026-regsol-review-kl88j7"
CLAUDE_LIVE_REF = "refs/heads/claude/version-1026-regsol-review-kl88j7"
CLAUDE_LOCAL_REF = "refs/heads/claude/version-1026-regsol-review-kl88j7"
CODEX_FORK_TIP = "11f90544865dd179739ca5bc5062b28c1078e504"
CODEX_FORK_REMOTE_REF = "refs/remotes/origin/codex/v1025_2-physics-conformance"
CODEX_FORK_LIVE_REF = "refs/heads/codex/v1025_2-physics-conformance"
CODEX_FORK_LOCAL_REF = "refs/heads/codex/v1025_2-physics-conformance"
BASE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
CLAUDE_COMMITS = (
    "2802395dd03e6cabe3e981bddddbba139e3963bc",
    "e3e1a634f34b711aa4803fd190fe9120f1755f13",
)
CLAUDE_TIP = CLAUDE_COMMITS[-1]
EXPECTED_PARENTS = {
    CLAUDE_COMMITS[0]: (BASE,),
    CLAUDE_COMMITS[1]: (CLAUDE_COMMITS[0],),
}
EXPECTED_SUBJECTS = {
    CLAUDE_COMMITS[0]: "fix(v1.0.25.2): 문턱 근방 스케일링 각주 오류 정정 — Codex 교차검증 수용 (U13)",
    CLAUDE_COMMITS[1]: "docs(v1.0.25.2): 핸드오버 갱신 — Codex 11f9054 대조 상태 + U13 오류 기록",
}

BUILDER = "Codex/work/v1025_phase068/build_phase068_step91.py"
VALIDATOR = "Codex/work/v1025_phase068/validate_phase068_step91.py"
INVENTORY = "Codex/results/PHASE_068_CLAUDE_FORK_DIFF_INVENTORY.json"
ATTESTATION = "Codex/results/PHASE_068_CLAUDE_FORK_FULL_READ_ATTESTATION.json"
RESULT = "Codex/results/PHASE_068_STEP_091_CLAUDE_FORK_REVIEW_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
EXACT_EIGHT = (
    BUILDER,
    VALIDATOR,
    INVENTORY,
    ATTESTATION,
    RESULT,
    PARENT_LEDGER,
    ACTIVE_LEDGER,
    HANDOVER,
)
GIT_ORDERED_EIGHT = tuple(sorted(EXACT_EIGHT))
PRE_JSON_SIX = (BUILDER, VALIDATOR, RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)
EXPECTED_STATUS = {
    BUILDER: "A",
    VALIDATOR: "A",
    INVENTORY: "A",
    ATTESTATION: "A",
    RESULT: "A",
    PARENT_LEDGER: "M",
    ACTIVE_LEDGER: "M",
    HANDOVER: "M",
}
EXPECTED_MODES = {path: "100644" for path in EXACT_EIGHT}
EXPECTED_OLD_MODES = {path: ("000000" if EXPECTED_STATUS[path] == "A" else "100644") for path in EXACT_EIGHT}

ARCHIVE_PATH = "Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md"
TEX_PATH = "Claude/docs/v1.0.25.2/_sections/ch3v22_sec02b_sifr.tex"
HANDOVER_PATH = "Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md"
EXPECTED_EDGES = (
    {
        "parent": BASE,
        "commit": CLAUDE_COMMITS[0],
        "paths": (
            (ARCHIVE_PATH, "M", "100644", "100644", "537d2a25326116067a079a978dcd1f272a75ed7b", "6b2cdd9e16ca99d26b0879d28a30b3322d43015e"),
            (TEX_PATH, "M", "100644", "100644", "ea762ff015f47e03b79e99f051deae5ddef44f9c", "05f1d84713017dde303f56ca7004b61aa0496979"),
        ),
    },
    {
        "parent": CLAUDE_COMMITS[0],
        "commit": CLAUDE_COMMITS[1],
        "paths": (
            (HANDOVER_PATH, "M", "100644", "100644", "7aa93a497eb660d40fbfea43f47960aed750c661", "b763605ab233303e93d25cf0843851b4c96beef7"),
        ),
    },
)
EXPECTED_BLOBS = {
    "537d2a25326116067a079a978dcd1f272a75ed7b": (30245, "00c89fb5a3078ff5b53a797e061fd5a80c9ef305d123aa1d77acd151b816d35d", 381),
    "6b2cdd9e16ca99d26b0879d28a30b3322d43015e": (32409, "e95c6090a94091960f81350f31fb64684d8301344f0428c189f28cf2a00c01e7", 406),
    "ea762ff015f47e03b79e99f051deae5ddef44f9c": (26835, "0444633ca12ce1212a2a98f4378db1a6d6d33e92f6856b767447e54b52c4d13a", 253),
    "05f1d84713017dde303f56ca7004b61aa0496979": (27406, "b0d00c44fa3d0097753ea056cfe08851e703d67e593eae148d6b133bdaa25179", 258),
    "7aa93a497eb660d40fbfea43f47960aed750c661": (10087, "76f6565912f7fdbadb501c665f0e8969948e28c257af6b7ac9bd116a6015ee49", 175),
    "b763605ab233303e93d25cf0843851b4c96beef7": (14150, "603e5fdaf90072a229338c17b92b7da7efcd3764863c3a285c6d68c366907b70", 219),
}

ARCHIVE_NEW = "6b2cdd9e16ca99d26b0879d28a30b3322d43015e"
TEX_OLD = "ea762ff015f47e03b79e99f051deae5ddef44f9c"
TEX_NEW = "05f1d84713017dde303f56ca7004b61aa0496979"
HANDOVER_OLD = "7aa93a497eb660d40fbfea43f47960aed750c661"
HANDOVER_NEW = "b763605ab233303e93d25cf0843851b4c96beef7"


def _claim_def(
    number: int,
    assertion_key: str,
    normalized_proposition: str,
    domain: str,
    sources: tuple[tuple[str, str, str, int, int], ...],
    *,
    self_report_status: str,
    truth_status: str,
    owner: str,
    route: str,
    assumptions: tuple[str, ...] = (),
    quantity_unit_sign_basis: dict[str, Any] | None = None,
    refuting_evidence_ids: tuple[str, ...] = (),
    authority_ceiling: str = "SOURCE_TEXT_PROVENANCE_ONLY",
) -> dict[str, Any]:
    claim_id = f"C91-{number:02d}"
    return {
        "id": claim_id,
        "assertion_key": assertion_key,
        "normalized_proposition": normalized_proposition,
        "domain": domain,
        "assumptions": assumptions,
        "quantity_unit_sign_basis": quantity_unit_sign_basis,
        "self_report_status": self_report_status,
        "truth_status": truth_status,
        "supporting_evidence_ids": tuple(f"{claim_id}-SRC-{index:02d}" for index in range(1, len(sources) + 1)),
        "refuting_evidence_ids": refuting_evidence_ids,
        "authority_ceiling": authority_ceiling,
        "owner": owner,
        "route": route,
        "sources": sources,
    }


def _q(value: str, unit: str, sign_convention: str, basis: str) -> dict[str, str]:
    return {"value": value, "unit": unit, "sign_convention": sign_convention, "basis": basis}


# C91-01..98 are atomic propositions extracted from the two commits, three
# changed-path edges, and all claim-bearing source occurrences. A pointer is
# (kind, object, path, line_start, line_end); raw-diff line values are symbolic.
CLAIM_DEFS = (
    _claim_def(1, "commit_280_identity", "The first reviewed commit is the fixed 2802395 object with the fixed parent and subject.", "repository_topology", (("commit_object", CLAUDE_COMMITS[0], "", 1, 4), ("commit_message", CLAUDE_COMMITS[0], "", 1, 1)), self_report_status="NOT_SELF_REPORT_GIT_DERIVED", truth_status="VERIFIED_REPOSITORY_OBJECT", owner="STEP91_REPOSITORY_AUDIT", route="CLOSED_STEP91", authority_ceiling="REPOSITORY_OBJECT_IDENTITY"),
    _claim_def(2, "commit_e3_identity", "The second reviewed commit is the fixed e3e1a63 object with the fixed parent and subject.", "repository_topology", (("commit_object", CLAUDE_COMMITS[1], "", 1, 4), ("commit_message", CLAUDE_COMMITS[1], "", 1, 1)), self_report_status="NOT_SELF_REPORT_GIT_DERIVED", truth_status="VERIFIED_REPOSITORY_OBJECT", owner="STEP91_REPOSITORY_AUDIT", route="CLOSED_STEP91", authority_ceiling="REPOSITORY_OBJECT_IDENTITY"),
    _claim_def(3, "archive_edge_change", "The first edge modifies ARCHIVE_NOTE with the fixed modes and blob identities.", "repository_tree_edge", (("raw_diff_record", CLAUDE_COMMITS[0], ARCHIVE_PATH, 1, 1),), self_report_status="NOT_SELF_REPORT_GIT_DERIVED", truth_status="VERIFIED_TREE_EDGE", owner="STEP91_REPOSITORY_AUDIT", route="CLOSED_STEP91", authority_ceiling="REPOSITORY_TREE_IDENTITY"),
    _claim_def(4, "tex_edge_change", "The first edge modifies the Si Frumkin TeX section with the fixed modes and blob identities.", "repository_tree_edge", (("raw_diff_record", CLAUDE_COMMITS[0], TEX_PATH, 2, 2),), self_report_status="NOT_SELF_REPORT_GIT_DERIVED", truth_status="VERIFIED_TREE_EDGE", owner="STEP91_REPOSITORY_AUDIT", route="CLOSED_STEP91", authority_ceiling="REPOSITORY_TREE_IDENTITY"),
    _claim_def(5, "handover_edge_change", "The second edge modifies the Claude handover with the fixed modes and blob identities.", "repository_tree_edge", (("raw_diff_record", CLAUDE_COMMITS[1], HANDOVER_PATH, 1, 1),), self_report_status="NOT_SELF_REPORT_GIT_DERIVED", truth_status="VERIFIED_TREE_EDGE", owner="STEP91_REPOSITORY_AUDIT", route="CLOSED_STEP91", authority_ceiling="REPOSITORY_TREE_IDENTITY"),
    _claim_def(6, "net_three_modified_paths", "The base-to-tip net diff contains exactly the same three modified paths.", "repository_topology", (("raw_diff_net", CLAUDE_TIP, "", 1, 3),), self_report_status="NOT_SELF_REPORT_GIT_DERIVED", truth_status="VERIFIED_TREE_TOPOLOGY", owner="STEP91_REPOSITORY_AUDIT", route="CLOSED_STEP91", authority_ceiling="REPOSITORY_TREE_IDENTITY"),
    _claim_def(7, "old_tex_value_continuity", "The superseded TeX said the broadened curve value is continuous across the threshold.", "historical_scientific_text", (("blob", TEX_OLD, TEX_PATH, 216, 219),), self_report_status="SOURCE_AUTHOR_ASSERTION", truth_status="HISTORICAL_TEXT_ONLY_NOT_SCIENTIFIC_TRUTH", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("broadening has already been applied",), refuting_evidence_ids=("C91-16",)),
    _claim_def(8, "old_tex_derivative_divergence", "The superseded TeX said square-root gap closure makes the Omega derivative diverge and the slope discontinuous.", "historical_scientific_text", (("blob", TEX_OLD, TEX_PATH, 217, 219),), self_report_status="SOURCE_AUTHOR_ASSERTION", truth_status="HISTORICAL_TEXT_ONLY_REPORTED_AS_ERROR", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("theta_a opens with square-root threshold scaling", "gap weight alone controls the full response difference"), refuting_evidence_ids=("C91-12", "C91-14", "C91-15", "C91-16")),
    _claim_def(9, "theta_a_sqrt_opening", "The coexistence composition theta_a opens with square-root scaling near the threshold.", "regular_solution_threshold_scaling", (("commit_message", CLAUDE_COMMITS[0], "", 14, 14), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 394, 394), ("blob", TEX_NEW, TEX_PATH, 217, 219)), self_report_status="SOURCE_AUTHOR_ASSERTION", truth_status="UNVERIFIED_SCIENTIFIC_PROPOSITION", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("epsilon is distance from Omega/(2RT)=1",)),
    _claim_def(10, "gap_weight_sqrt_closure", "The gap weight closes proportionally to square-root epsilon near the threshold.", "regular_solution_threshold_scaling", (("commit_message", CLAUDE_COMMITS[0], "", 14, 14), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 394, 395), ("blob", TEX_NEW, TEX_PATH, 218, 220), ("commit_message", CLAUDE_COMMITS[1], "", 9, 9), ("blob", HANDOVER_NEW, HANDOVER_PATH, 125, 127)), self_report_status="SOURCE_AUTHOR_ASSERTION", truth_status="UNVERIFIED_SCIENTIFIC_PROPOSITION", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("epsilon is nonnegative distance from threshold",), quantity_unit_sign_basis=_q("proportional to sqrt(epsilon)", "dimensionless weight", "nonnegative above threshold", "source asymptotic statement")),
    _claim_def(11, "two_solid_solution_terms_equal_weight_loss", "At threshold the two solid-solution terms lose equal weight.", "regular_solution_cancellation", (("commit_message", CLAUDE_COMMITS[0], "", 15, 15), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 395, 395), ("blob", TEX_NEW, TEX_PATH, 219, 220), ("blob", HANDOVER_NEW, HANDOVER_PATH, 127, 127)), self_report_status="SOURCE_AUTHOR_ASSERTION", truth_status="UNVERIFIED_SCIENTIFIC_PROPOSITION", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("the response decomposition and weights use the same normalization",)),
    _claim_def(12, "leading_sqrt_terms_cancel", "The equal weight losses cancel the leading square-root order.", "regular_solution_cancellation", (("commit_message", CLAUDE_COMMITS[0], "", 15, 15), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 395, 396), ("blob", TEX_NEW, TEX_PATH, 219, 220), ("commit_message", CLAUDE_COMMITS[1], "", 9, 9), ("blob", HANDOVER_NEW, HANDOVER_PATH, 127, 127)), self_report_status="SOURCE_AUTHOR_ASSERTION", truth_status="UNVERIFIED_SCIENTIFIC_PROPOSITION", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("both cancelling terms are expanded on a common basis",)),
    _claim_def(13, "ratio_5_90_invariant", "The reported maximum response difference divided by epsilon is 5.90 and invariant from epsilon 1e-3 through 1e-5.", "numerical_crosscheck", (("commit_message", CLAUDE_COMMITS[0], "", 10, 11), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 392, 392), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 405, 405), ("blob", TEX_NEW, TEX_PATH, 221, 222), ("commit_message", CLAUDE_COMMITS[1], "", 9, 9), ("blob", HANDOVER_NEW, HANDOVER_PATH, 124, 126)), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("the same response normalization is used at every epsilon",), quantity_unit_sign_basis=_q("5.90 for epsilon=1e-3..1e-5", "reported max|Delta|/epsilon", "absolute magnitude", "unattached source crosscheck")),
    _claim_def(14, "response_difference_linear", "The response difference is O(epsilon), not O(sqrt(epsilon)).", "regular_solution_threshold_scaling", (("commit_message", CLAUDE_COMMITS[0], "", 11, 15), ("commit_message", CLAUDE_COMMITS[0], "", 20, 21), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 392, 396), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 400, 401), ("blob", TEX_NEW, TEX_PATH, 219, 222), ("commit_message", CLAUDE_COMMITS[1], "", 9, 9), ("blob", HANDOVER_NEW, HANDOVER_PATH, 125, 127), ("blob", HANDOVER_NEW, HANDOVER_PATH, 133, 133), ("blob", HANDOVER_NEW, HANDOVER_PATH, 157, 157)), self_report_status="SOURCE_AUTHOR_ASSERTION", truth_status="UNVERIFIED_SCIENTIFIC_PROPOSITION", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("the leading square-root terms cancel",)),
    _claim_def(15, "omega_derivative_finite", "The derivative of the broadened response with respect to Omega is finite at threshold.", "regular_solution_differentiability", (("commit_message", CLAUDE_COMMITS[0], "", 11, 16), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 396, 397), ("blob", TEX_NEW, TEX_PATH, 222, 223), ("commit_message", CLAUDE_COMMITS[1], "", 9, 9), ("blob", HANDOVER_NEW, HANDOVER_PATH, 125, 128)), self_report_status="SOURCE_AUTHOR_ASSERTION", truth_status="UNVERIFIED_SCIENTIFIC_PROPOSITION", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("the O(epsilon) statement holds with a finite limiting coefficient",)),
    _claim_def(16, "omega_c1_equal_slopes", "The broadened response is C1 in Omega, with value and first derivative continuous across threshold.", "regular_solution_differentiability", (("commit_message", CLAUDE_COMMITS[0], "", 16, 16), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 396, 397), ("blob", TEX_NEW, TEX_PATH, 222, 223), ("commit_message", CLAUDE_COMMITS[1], "", 9, 9), ("blob", HANDOVER_NEW, HANDOVER_PATH, 126, 128)), self_report_status="SOURCE_AUTHOR_ASSERTION", truth_status="UNDECIDED_REQUIRES_LIMIT_AND_ONE_SIDED_DERIVATIVES", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("both one-sided derivatives exist", "both one-sided derivative limits are equal"), refuting_evidence_ids=("C91-08",)),
    _claim_def(17, "area_error_precision", "The crosscheck reported window-integrated area error 7.8e-16, rounded to 8e-16 in the TeX.", "numerical_crosscheck", (("commit_message", CLAUDE_COMMITS[0], "", 8, 8), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 390, 390), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 404, 405), ("blob", TEX_NEW, TEX_PATH, 221, 222), ("commit_message", CLAUDE_COMMITS[1], "", 10, 10), ("blob", HANDOVER_NEW, HANDOVER_PATH, 130, 131)), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("window, grid, normalization, and Q definition match across reports",), quantity_unit_sign_basis=_q("7.8e-16; rounded 8e-16", "reported area error", "absolute error", "unattached source crosscheck")),
    _claim_def(18, "subcritical_gap_zero", "The crosscheck reported exactly zero gap weight below Omega=2RT.", "numerical_crosscheck", (("commit_message", CLAUDE_COMMITS[0], "", 9, 9), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 391, 391), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 404, 405), ("blob", TEX_NEW, TEX_PATH, 222, 224), ("commit_message", CLAUDE_COMMITS[1], "", 10, 10), ("blob", HANDOVER_NEW, HANDOVER_PATH, 130, 131)), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("the tested implementation matches the stated equation",), quantity_unit_sign_basis=_q("0.0", "dimensionless gap weight", "nonnegative", "reported Omega<2RT crosscheck")),
    _claim_def(19, "u9_raw_deltas", "The earlier U9 table reportedly contained max absolute differences 5.764e-2, 5.698e-3, and 5.488e-4.", "historical_numerical_record", (("commit_message", CLAUDE_COMMITS[0], "", 20, 20), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 399, 400)), self_report_status="SOURCE_SELF_REPORT_NO_UPSTREAM_TABLE_POINTER", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", quantity_unit_sign_basis=_q("5.764e-2 / 5.698e-3 / 5.488e-4", "reported max|Delta|", "absolute magnitude", "U9 table as restated")),
    _claim_def(20, "u9_normalized_ratios", "Dividing the three U9 differences by their stated epsilons reportedly gives 57.6, 57.0, and 54.9.", "historical_numerical_record", (("commit_message", CLAUDE_COMMITS[0], "", 20, 21), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 399, 401), ("blob", HANDOVER_NEW, HANDOVER_PATH, 133, 134)), self_report_status="SOURCE_SELF_REPORT_NO_UPSTREAM_TABLE_POINTER", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("the corresponding epsilons are known and correctly paired",), quantity_unit_sign_basis=_q("57.6 / 57.0 / 54.9", "reported max|Delta|/epsilon", "absolute magnitude", "U9 table as restated")),
    _claim_def(21, "gap_weight_scaling_transfer_error", "The old conclusion arose by transferring square-root gap-weight scaling to the full response difference.", "error_provenance", (("commit_message", CLAUDE_COMMITS[0], "", 17, 17), ("commit_message", CLAUDE_COMMITS[0], "", 21, 21), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 397, 397), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 400, 401), ("blob", TEX_NEW, TEX_PATH, 223, 224), ("blob", HANDOVER_NEW, HANDOVER_PATH, 133, 134), ("blob", HANDOVER_NEW, HANDOVER_PATH, 157, 157)), self_report_status="SOURCE_AUTHOR_RETROSPECTIVE", truth_status="UNVERIFIED_CAUSAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94"),
    _claim_def(22, "numbers_generated_not_read", "The author characterized the error as generating numerical evidence without reading it through.", "workflow_retrospective", (("commit_message", CLAUDE_COMMITS[0], "", 22, 22), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 402, 402), ("blob", HANDOVER_NEW, HANDOVER_PATH, 133, 134), ("blob", HANDOVER_NEW, HANDOVER_PATH, 159, 160)), self_report_status="SOURCE_AUTHOR_RETROSPECTIVE", truth_status="UNVERIFIED_WORKFLOW_SELF_REPORT", owner="STEP91_PROVENANCE_AUDIT", route="RECORDED_NOT_ADJUDICATED"),
    _claim_def(23, "codex_11f_merged_3b5", "The Codex conformance branch at 11f9054 reportedly merged Claude baseline 3b5fd05.", "cross_branch_topology_self_report", (("commit_message", CLAUDE_COMMITS[0], "", 3, 4), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 385, 385), ("commit_message", CLAUDE_COMMITS[1], "", 3, 4), ("blob", HANDOVER_NEW, HANDOVER_PATH, 67, 68), ("blob", HANDOVER_NEW, HANDOVER_PATH, 219, 219)), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_UNTIL_CODEX_FORK_TOPOLOGY_READ", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(24, "phase054_script_independent_recalculation", "phase054_regsol_crosscheck.py reportedly independently recalculated eq:sifr-twophase.", "cross_branch_numerical_provenance", (("commit_message", CLAUDE_COMMITS[0], "", 4, 4), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 385, 386), ("blob", HANDOVER_NEW, HANDOVER_PATH, 73, 73)), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_UNTIL_CODEX_FORK_FULL_READ", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92_THEN_STEP94"),
    _claim_def(25, "old_threshold_footnote_identified_wrong", "The source authors specifically classify the prior threshold derivative-divergence footnote as wrong.", "correction_provenance", (("commit_message", CLAUDE_COMMITS[0], "", 1, 1), ("commit_message", CLAUDE_COMMITS[0], "", 5, 5), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 383, 383), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 386, 386), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 392, 392), ("commit_message", CLAUDE_COMMITS[1], "", 1, 1), ("commit_message", CLAUDE_COMMITS[1], "", 8, 8), ("blob", HANDOVER_NEW, HANDOVER_PATH, 47, 47), ("blob", HANDOVER_NEW, HANDOVER_PATH, 122, 122), ("blob", HANDOVER_NEW, HANDOVER_PATH, 124, 124)), self_report_status="SOURCE_AUTHOR_CORRECTION", truth_status="VERIFIED_CORRECTION_STATEMENT_SCIENCE_UNVERIFIED", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94"),
    _claim_def(26, "codex_finding_fully_accepted", "Claude recorded full acceptance of the Codex finding.", "correction_provenance", (("commit_message", CLAUDE_COMMITS[0], "", 1, 1), ("commit_message", CLAUDE_COMMITS[0], "", 5, 5), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 406, 406), ("blob", HANDOVER_NEW, HANDOVER_PATH, 47, 47)), self_report_status="SOURCE_AUTHOR_CORRECTION", truth_status="VERIFIED_ACCEPTANCE_STATEMENT_ONLY", owner="STEP91_PROVENANCE_AUDIT", route="CLOSED_STEP91"),
    _claim_def(27, "tex_footnote_patch_action", "The first commit says it corrected the TeX footnote to state cancellation and linear scaling.", "repository_change_intent", (("commit_message", CLAUDE_COMMITS[0], "", 1, 1), ("commit_message", CLAUDE_COMMITS[0], "", 24, 25), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 404, 405), ("commit_message", CLAUDE_COMMITS[1], "", 8, 8), ("blob", HANDOVER_NEW, HANDOVER_PATH, 47, 47), ("blob", HANDOVER_NEW, HANDOVER_PATH, 128, 128), ("raw_diff_record", CLAUDE_COMMITS[0], TEX_PATH, 2, 2)), self_report_status="SOURCE_ACTION_CLAIM_WITH_TREE_EDGE", truth_status="VERIFIED_PATH_CHANGED_CONTENT_MEANING_UNADJUDICATED", owner="STEP91_PROVENANCE_AUDIT", route="STEP91_CHANGE_STEP94_CONTENT"),
    _claim_def(28, "archive_u13_added", "The first commit says it created ARCHIVE_NOTE entry U13.", "repository_change_intent", (("commit_message", CLAUDE_COMMITS[0], "", 26, 26), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 383, 406), ("raw_diff_record", CLAUDE_COMMITS[0], ARCHIVE_PATH, 1, 1)), self_report_status="SOURCE_ACTION_CLAIM_WITH_TREE_EDGE", truth_status="VERIFIED_RECORD_EXISTS_CONTENT_UNADJUDICATED", owner="STEP91_PROVENANCE_AUDIT", route="STEP91_RECORD_STEP94_CONTENT"),
    _claim_def(29, "commit_structure_check_pass", "The first commit message reports STRUCTURE_CHECK PASS.", "build_validation_self_report", (("commit_message", CLAUDE_COMMITS[0], "", 26, 26),), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_BUILD_SELF_REPORT", owner="STEP96_BUILD_GATE", route="STEP96"),
    _claim_def(30, "history_3b5_handover_rewrite", "The updated handover history labels 3b5fd05 as the final handover rewrite.", "document_history", (("blob", HANDOVER_NEW, HANDOVER_PATH, 46, 46),), self_report_status="DOCUMENT_HISTORY_SELF_REPORT", truth_status="UNVERIFIED_HISTORY_ROW", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(31, "history_280_u13_correction", "The updated handover history labels 2802395 as the U13 threshold-scaling correction accepting Codex crosscheck.", "document_history", (("blob", HANDOVER_NEW, HANDOVER_PATH, 47, 47),), self_report_status="DOCUMENT_HISTORY_SELF_REPORT", truth_status="VERIFIED_ROW_EXISTS_SCIENCE_UNADJUDICATED", owner="STEP91_PROVENANCE_AUDIT", route="STEP91_RECORD_STEP94_CONTENT"),
    _claim_def(32, "codex_branch_outputs_four_docs_three_probes", "The Codex branch reportedly produced four new documents and three probes.", "cross_branch_inventory_self_report", (("commit_message", CLAUDE_COMMITS[1], "", 3, 5), ("blob", HANDOVER_NEW, HANDOVER_PATH, 67, 78)), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_UNTIL_CODEX_FORK_FULL_READ", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92", quantity_unit_sign_basis=_q("4 documents + 3 probes", "artifacts", "not applicable", "handover inventory")),
    _claim_def(33, "only_regsol_crosscheck_reviewed", "Of those Codex outputs, only the regular-solution crosscheck was reportedly reviewed.", "cross_branch_review_status", (("commit_message", CLAUDE_COMMITS[1], "", 4, 5), ("blob", HANDOVER_NEW, HANDOVER_PATH, 68, 78)), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_REVIEW_STATUS", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(34, "regsol_review_triggered_u13", "The reviewed regular-solution crosscheck reportedly triggered U13.", "correction_provenance", (("blob", HANDOVER_NEW, HANDOVER_PATH, 73, 73),), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_CAUSAL_SELF_REPORT", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92_THEN_STEP94"),
    _claim_def(35, "phase054_addendum_unreviewed", "The Phase 054 lineage review addendum was marked unreviewed.", "cross_branch_review_status", (("blob", HANDOVER_NEW, HANDOVER_PATH, 74, 74),), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_REVIEW_STATUS", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(36, "alignment_matrix_unreviewed", "The latest-release alignment matrix was marked unreviewed.", "cross_branch_review_status", (("blob", HANDOVER_NEW, HANDOVER_PATH, 75, 75),), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_REVIEW_STATUS", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(37, "alignment_matrix_may_answer_p1", "The alignment matrix was said to potentially answer the P1 gallery-to-staging assignment question.", "cross_branch_decision_support", (("commit_message", CLAUDE_COMMITS[1], "", 6, 6), ("blob", HANDOVER_NEW, HANDOVER_PATH, 75, 80), ("blob", HANDOVER_NEW, HANDOVER_PATH, 198, 199)), self_report_status="SOURCE_HYPOTHESIS", truth_status="UNVERIFIED_DECISION_SUPPORT_HYPOTHESIS", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(38, "correction_handover_unreviewed", "The conformance-branch correction handover was marked unreviewed.", "cross_branch_review_status", (("blob", HANDOVER_NEW, HANDOVER_PATH, 76, 76),), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_REVIEW_STATUS", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(39, "ledger_probe_manifest_unreviewed", "The Phase 054 ledger, source probes, and source-freeze manifest were marked unreviewed.", "cross_branch_review_status", (("blob", HANDOVER_NEW, HANDOVER_PATH, 77, 77),), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_REVIEW_STATUS", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(40, "package_manuscript_pdf_unreviewed", "The earlier conformance package, manuscript, and PDF totaling 26,385 lines were marked unreviewed.", "cross_branch_review_status", (("blob", HANDOVER_NEW, HANDOVER_PATH, 78, 78),), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_REVIEW_STATUS", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92", quantity_unit_sign_basis=_q("26385", "reported lines", "not applicable", "handover inventory")),
    _claim_def(41, "prior_baseline_issue_reported_resolved", "The handover reports the prior defective-baseline concern as resolved by merge.", "cross_branch_issue_status", (("commit_message", CLAUDE_COMMITS[1], "", 7, 7), ("blob", HANDOVER_NEW, HANDOVER_PATH, 82, 82)), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_ISSUE_STATUS", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(42, "prior_handover_mismatch_reported_resolved", "The handover reports the prior handover self-report mismatch as resolved by a correction document.", "cross_branch_issue_status", (("commit_message", CLAUDE_COMMITS[1], "", 7, 7), ("blob", HANDOVER_NEW, HANDOVER_PATH, 82, 83)), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_ISSUE_STATUS", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(43, "prior_crosscheck_absence_reported_resolved", "The handover reports the prior lack of eq:sifr-twophase crosscheck as resolved.", "cross_branch_issue_status", (("commit_message", CLAUDE_COMMITS[1], "", 7, 7), ("blob", HANDOVER_NEW, HANDOVER_PATH, 83, 83)), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_ISSUE_STATUS", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92_THEN_STEP94"),
    _claim_def(44, "conformance_name_hides_scope", "The handover assesses the conformance branch name as hiding the scale of the work and marks that naming concern unresolved.", "lineage_governance", (("commit_message", CLAUDE_COMMITS[1], "", 7, 7), ("blob", HANDOVER_NEW, HANDOVER_PATH, 84, 85)), self_report_status="SOURCE_AUTHOR_ASSESSMENT", truth_status="UNVERIFIED_GOVERNANCE_ASSESSMENT", owner="STEP95_LINEAGE_DECISION", route="STEP95"),
    _claim_def(45, "workflow_ratio_table_rule", "The updated workflow rule requires explicit scaling-ratio tables before choosing a scaling law.", "workflow_rule", (("commit_message", CLAUDE_COMMITS[1], "", 11, 12), ("blob", HANDOVER_NEW, HANDOVER_PATH, 157, 160)), self_report_status="SOURCE_NORMATIVE_RULE", truth_status="VERIFIED_RULE_TEXT_EXISTS", owner="STEP91_PROVENANCE_AUDIT", route="APPLY_STEPS94_TO97"),
    _claim_def(46, "legacy_gates_green_vector", "The handover reports all listed legacy gate groups GREEN.", "build_validation_self_report", (("blob", HANDOVER_NEW, HANDOVER_PATH, 187, 190),), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_BUILD_SELF_REPORT", owner="STEP96_BUILD_GATE", route="STEP96"),
    _claim_def(47, "handover_structure_check_pass", "The handover reports STRUCTURE_CHECK PASS.", "build_validation_self_report", (("blob", HANDOVER_NEW, HANDOVER_PATH, 189, 190),), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_BUILD_SELF_REPORT", owner="STEP96_BUILD_GATE", route="STEP96"),
    _claim_def(48, "handover_numerical_checks_three_of_three", "The handover reports three of three eq:sifr-twophase numerical checks passing.", "numerical_validation_self_report", (("blob", HANDOVER_NEW, HANDOVER_PATH, 190, 190),), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", quantity_unit_sign_basis=_q("3/3", "reported checks", "not applicable", "handover validation summary")),
    _claim_def(49, "default_path_temperature_dependence_0_5252", "The handover reports restoration of default-path temperature dependence magnitude 0.5252.", "model_validation_self_report", (("blob", HANDOVER_NEW, HANDOVER_PATH, 191, 191),), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP93_CODEX_MODEL_AUDIT", route="STEP93", quantity_unit_sign_basis=_q("0.5252", "reported max|Delta|", "absolute magnitude", "288 K to 308 K default-path comparison")),
    _claim_def(50, "nan_inf_zero", "The handover reports zero NaN or infinity outputs.", "model_validation_self_report", (("blob", HANDOVER_NEW, HANDOVER_PATH, 191, 191),), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_BUILD_SELF_REPORT", owner="STEP96_BUILD_GATE", route="STEP96", quantity_unit_sign_basis=_q("0", "NaN/Inf occurrences", "count", "handover validation summary")),
    _claim_def(51, "xelatex_three_pass_not_run", "The handover says the XeLaTeX three-pass build was not run.", "build_status", (("blob", HANDOVER_NEW, HANDOVER_PATH, 192, 192),), self_report_status="SOURCE_SELF_REPORT", truth_status="OPEN_BUILD_REQUIREMENT", owner="STEP96_BUILD_GATE", route="STEP96", quantity_unit_sign_basis=_q("3", "XeLaTeX passes", "required but unexecuted", "handover build requirement")),
    _claim_def(52, "handover_six_position_queue_exists", "The handover contains a six-position next-session queue.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 196, 206),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN", quantity_unit_sign_basis=_q("6", "queue positions", "ordered", "Claude handover")),
    _claim_def(53, "current_codex_comparison_branch_location", "The handover locates the current Codex comparison branch at origin/codex/v1025_2-physics-conformance tip 11f9054.", "cross_branch_location", (("blob", HANDOVER_NEW, HANDOVER_PATH, 219, 219),), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_UNTIL_CODEX_FORK_TOPOLOGY_READ", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(54, "older_codex_audit_location", "The handover scopes the older Codex scientific audit to v1.0.10 through v1.0.23 and locates it on origin/codex-local-audit-20260720.", "cross_branch_location", (("blob", HANDOVER_NEW, HANDOVER_PATH, 218, 218),), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_LOCATION_SELF_REPORT", owner="STEP95_LINEAGE_DECISION", route="STEP95"),
    _claim_def(55, "handover_queue_reordered_p0_first", "The second commit reports reordering the work queue so that P0 comes first.", "repository_change_intent", (("commit_message", CLAUDE_COMMITS[1], "", 13, 13), ("blob", HANDOVER_NEW, HANDOVER_PATH, 198, 198), ("raw_diff_record", CLAUDE_COMMITS[1], HANDOVER_PATH, 1, 1)), self_report_status="SOURCE_ACTION_CLAIM_WITH_TREE_EDGE", truth_status="VERIFIED_PATH_CHANGED_CONTENT_MEANING_UNADJUDICATED", owner="STEP91_PROVENANCE_AUDIT", route="STEP91_RECORD_STEPS92_TO97_CONTENT"),
    _claim_def(56, "stale_archive_u1_u12_header", "The updated handover header still routes readers to ARCHIVE_NOTE U1 through U12 although U13 is present.", "document_routing_defect", (("blob", HANDOVER_NEW, HANDOVER_PATH, 3, 4), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 383, 383)), self_report_status="NOT_SELF_REPORT_TEXTUAL_COMPARISON", truth_status="VERIFIED_TEXTUAL_ROUTING_MISMATCH", owner="STEP97_RELEASE_INTEGRITY", route="STEP97"),
    _claim_def(57, "tex_theory_asset_not_adopted", "The corrected equation remains a theory-layer asset outside the adopted post-v1.0.25 path.", "manuscript_authority_status", (("blob", TEX_NEW, TEX_PATH, 231, 234),), self_report_status="DOCUMENT_AUTHORITY_STATEMENT", truth_status="VERIFIED_STATUS_TEXT_EXISTS_ADOPTION_NOT_INFERRED", owner="STEP95_LINEAGE_DECISION", route="STEP95"),
    _claim_def(58, "codex_review_classified_p0_blocking", "The updated handover classifies review of the Codex comparison outputs as P0, highest priority, and blocking.", "workflow_priority", (("commit_message", CLAUDE_COMMITS[1], "", 3, 5), ("blob", HANDOVER_NEW, HANDOVER_PATH, 63, 69)), self_report_status="SOURCE_NORMATIVE_PRIORITY", truth_status="VERIFIED_PRIORITY_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(59, "p1_removed_from_highest_priority", "The updated handover removes P1's former highest-priority label after inserting P0 ahead of it.", "workflow_priority_change", (("blob", HANDOVER_OLD, HANDOVER_PATH, 63, 63), ("commit_message", CLAUDE_COMMITS[1], "", 13, 13), ("blob", HANDOVER_NEW, HANDOVER_PATH, 87, 87)), self_report_status="NOT_SELF_REPORT_TEXTUAL_COMPARISON", truth_status="VERIFIED_TEXTUAL_PRIORITY_CHANGE_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(60, "u13_layout_recheck_required", "The updated handover requires the lengthened U13 footnote layout to be checked during the three-pass XeLaTeX build.", "build_requirement", (("blob", HANDOVER_NEW, HANDOVER_PATH, 198, 200),), self_report_status="SOURCE_NORMATIVE_REQUIREMENT", truth_status="OPEN_BUILD_REQUIREMENT", owner="STEP96_BUILD_GATE", route="STEP96"),
    _claim_def(61, "prior_area_selfcheck_basis", "The prior area self-check reported error 1e-4 and the handover characterizes its basis as a finite window and coarse grid.", "historical_numerical_record", (("commit_message", CLAUDE_COMMITS[0], "", 8, 8), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 390, 390), ("commit_message", CLAUDE_COMMITS[1], "", 10, 10), ("blob", HANDOVER_NEW, HANDOVER_PATH, 130, 131)), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("the area-error definition and normalization are the historical self-check's own basis",), quantity_unit_sign_basis=_q("1e-4", "reported area error", "absolute error", "prior finite-window/coarse-grid self-check")),
    _claim_def(62, "area_crosscheck_reported_stricter", "The source authors characterize the 7.8e-16 crosscheck as much stricter or higher precision than the prior 1e-4 self-check.", "numerical_comparison_self_report", (("commit_message", CLAUDE_COMMITS[0], "", 8, 8), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 390, 390), ("commit_message", CLAUDE_COMMITS[1], "", 10, 10), ("blob", HANDOVER_NEW, HANDOVER_PATH, 130, 131)), self_report_status="SOURCE_AUTHOR_NUMERICAL_COMPARISON", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("both values measure the same area-error quantity under comparable normalization",), quantity_unit_sign_basis=_q("7.8e-16 versus 1e-4", "reported area error", "smaller reported magnitude called stricter", "source-authored comparison; bases not independently reconciled")),
    _claim_def(63, "workflow_failure_same_root_as_section4", "The authors say that producing but not reading the numerical evidence has the same root as Section 4's failure to verify what could be verified.", "workflow_retrospective", (("commit_message", CLAUDE_COMMITS[0], "", 22, 22), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 402, 402), ("blob", HANDOVER_NEW, HANDOVER_PATH, 133, 134), ("blob", HANDOVER_NEW, HANDOVER_PATH, 159, 160)), self_report_status="SOURCE_AUTHOR_RETROSPECTIVE", truth_status="UNVERIFIED_CAUSAL_SELF_REPORT", owner="STEP91_PROVENANCE_AUDIT", route="RECORDED_NOT_ADJUDICATED"),
    _claim_def(64, "workflow_cancellation_pair_rule", "The updated workflow rule requires all cancelling term pairs in a composite expression to be counted together.", "workflow_rule", (("commit_message", CLAUDE_COMMITS[1], "", 11, 12), ("blob", TEX_NEW, TEX_PATH, 223, 224), ("blob", HANDOVER_NEW, HANDOVER_PATH, 157, 160)), self_report_status="SOURCE_NORMATIVE_RULE", truth_status="VERIFIED_RULE_TEXT_EXISTS", owner="STEP91_PROVENANCE_AUDIT", route="APPLY_STEPS94_TO97"),
    _claim_def(65, "workflow_read_outputs_to_end_rule", "The updated workflow rule requires produced numerical outputs to be read through to the end before a conclusion is written.", "workflow_rule", (("commit_message", CLAUDE_COMMITS[1], "", 11, 12), ("blob", HANDOVER_NEW, HANDOVER_PATH, 157, 160)), self_report_status="SOURCE_NORMATIVE_RULE", truth_status="VERIFIED_RULE_TEXT_EXISTS", owner="STEP91_PROVENANCE_AUDIT", route="APPLY_STEPS94_TO97"),
    _claim_def(66, "phase054_addendum_reported_line_count", "The handover reports that the Phase 054 latest-lineage review addendum contains 372 lines.", "cross_branch_inventory_self_report", (("blob", HANDOVER_NEW, HANDOVER_PATH, 74, 74),), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_INVENTORY_SELF_REPORT", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92", quantity_unit_sign_basis=_q("372", "reported lines", "count", "handover inventory")),
    _claim_def(67, "four_prior_findings_baseline", "The handover states that its four previously submitted Codex-branch findings were assessed against baseline 2abf019.", "cross_branch_issue_baseline", (("blob", HANDOVER_NEW, HANDOVER_PATH, 82, 85),), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_BASELINE_SELF_REPORT", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92"),
    _claim_def(68, "area_claim_confirmed_higher_precision", "The authors say the area-conservation claim was one of the remaining claims confirmed by the crosscheck at higher precision.", "numerical_validation_self_report", (("commit_message", CLAUDE_COMMITS[1], "", 10, 10), ("blob", HANDOVER_NEW, HANDOVER_PATH, 130, 131)), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("the phrase 'remaining two claims' refers to the preceding area and subcritical-gap claims",)),
    _claim_def(69, "window_area_equals_q_confirmation", "The crosscheck reports that the window-integrated area equals Q.", "numerical_crosscheck", (("commit_message", CLAUDE_COMMITS[0], "", 8, 8), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 390, 390)), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("the reported finite integration window and normalization define the same Q",), quantity_unit_sign_basis=_q("area = Q", "capacity over the reported window", "equality claim", "unattached source crosscheck")),
    _claim_def(70, "u9_ratios_interpreted_linear", "The authors say the U9 ratios 57.6, 57.0, and 54.9 already displayed linear scaling.", "historical_numerical_interpretation", (("commit_message", CLAUDE_COMMITS[0], "", 20, 21), ("blob", ARCHIVE_NEW, ARCHIVE_PATH, 400, 401), ("blob", HANDOVER_NEW, HANDOVER_PATH, 133, 133), ("blob", HANDOVER_NEW, HANDOVER_PATH, 157, 157)), self_report_status="SOURCE_AUTHOR_RETROSPECTIVE", truth_status="UNVERIFIED_CAUSAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("the stated epsilon pairing and normalization are correct",), quantity_unit_sign_basis=_q("57.6 / 57.0 / 54.9", "reported max|Delta|/epsilon", "called approximately invariant", "unattached U9 table retrospective")),
    _claim_def(71, "comparison_tip_reported_date", "The handover dates comparison-branch tip 11f9054 to 2026-07-27.", "cross_branch_date_self_report", (("blob", HANDOVER_NEW, HANDOVER_PATH, 67, 67),), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_DATE_SELF_REPORT", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92", quantity_unit_sign_basis=_q("2026-07-27", "ISO calendar date", "not applicable", "handover source-only date")),
    _claim_def(72, "claude_baseline_includes_u11_u12", "The source says baseline 3b5fd05 includes U11 and U12.", "cross_branch_baseline_self_report", (("commit_message", CLAUDE_COMMITS[1], "", 4, 4), ("blob", HANDOVER_NEW, HANDOVER_PATH, 68, 68)), self_report_status="SOURCE_SELF_REPORT", truth_status="UNVERIFIED_BASELINE_SELF_REPORT", owner="STEP92_CODEX_FORK_AUDIT", route="STEP92", quantity_unit_sign_basis=_q("3b5fd05", "Git abbreviation", "not applicable", "source-labeled U11/U12 baseline")),
    _claim_def(73, "p4_correction_record_created", "The second commit creates a P4 resolved-error record preserving the threshold-error correction history.", "repository_change_intent", (("commit_message", CLAUDE_COMMITS[1], "", 8, 8), ("blob", HANDOVER_NEW, HANDOVER_PATH, 122, 122)), self_report_status="SOURCE_ACTION_CLAIM_WITH_TREE_EDGE", truth_status="VERIFIED_RECORD_EXISTS_CONTENT_UNADJUDICATED", owner="STEP91_PROVENANCE_AUDIT", route="STEP91_RECORD_STEP94_CONTENT"),
    _claim_def(74, "parallel_physics_rewrite_scope", "The handover characterizes the branch work as a parallel physics implementation rewrite with a separate manuscript and PDF, not merely a conformance check.", "cross_branch_scope_assessment", (("blob", HANDOVER_NEW, HANDOVER_PATH, 84, 85),), self_report_status="SOURCE_AUTHOR_ASSESSMENT", truth_status="UNVERIFIED_SCOPE_ASSESSMENT", owner="STEP95_LINEAGE_DECISION", route="STEP93_THEN_STEP95"),
    _claim_def(75, "additional_lineage_not_exposed", "The handover says that the parallel work creates an additional lineage not exposed by the branch name.", "lineage_governance", (("blob", HANDOVER_NEW, HANDOVER_PATH, 85, 85),), self_report_status="SOURCE_AUTHOR_ASSESSMENT", truth_status="UNVERIFIED_LINEAGE_ASSESSMENT", owner="STEP95_LINEAGE_DECISION", route="STEP95"),
    _claim_def(76, "lineage_decision_assigned_to_user", "The handover assigns the additional-lineage disposition decision to the user.", "lineage_governance", (("blob", HANDOVER_NEW, HANDOVER_PATH, 85, 85),), self_report_status="SOURCE_GOVERNANCE_ALLOCATION", truth_status="PENDING_USER_DECISION", owner="USER_DECISION", route="STEP95_THEN_USER_DECISION"),
    _claim_def(77, "p1_thermodynamic_input_unresolved", "The P1 thermodynamic-input issue remains labeled unresolved across the handover update.", "workflow_priority_change", (("blob", HANDOVER_OLD, HANDOVER_PATH, 63, 63), ("blob", HANDOVER_NEW, HANDOVER_PATH, 87, 87)), self_report_status="NOT_SELF_REPORT_TEXTUAL_COMPARISON", truth_status="VERIFIED_UNRESOLVED_LABEL", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(78, "alignment_matrix_named_first_work", "The handover names alignment-matrix review as the next session's first work.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 80, 80),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(79, "queue_one_review_codex_outputs", "Queue position 1 requires review of the Codex 11f9054 outputs.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 198, 198),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(80, "queue_one_alignment_matrix_first", "Within queue position 1, the alignment matrix is first.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 198, 198),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(81, "queue_one_addendum_second", "Within queue position 1, the Phase 054 addendum follows the alignment matrix.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 198, 199),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(82, "queue_one_conformance_model_third", "Within queue position 1, conformance_model follows the Phase 054 addendum.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 199, 199),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(83, "queue_two_xelatex_three_pdfs", "Queue position 2 requires a three-pass XeLaTeX build and committing three PDFs.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 200, 200),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(84, "queue_three_gallery_assignment_confirmation", "Queue position 3 requires user confirmation of the gallery-cluster-to-staging assignment.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 201, 201),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(85, "queue_three_populate_thermodynamic_fields", "After that confirmation, dH_rxn, dS_rxn, and n are to be populated in the seed.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 201, 201),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(86, "queue_three_restore_skew7_default", "The default is then to be restored to 7-skew.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 201, 202),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(87, "queue_three_add_temperature_gate", "A gate measuring default-path temperature dependence is then to be added.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 202, 202),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(88, "queue_four_blend_normalization_first", "Queue position 4 requires the Codex P0-4 blend-normalization comparison first.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 203, 203),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(89, "queue_four_remaining_p0_order", "Within queue position 4, P0-2, P0-3, and P0-5 follow P0-4.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 203, 203),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(90, "queue_five_omega_qualifier", "Queue position 5 requires one model-family qualifier sentence for the Omega anchor.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 204, 204),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(91, "queue_six_n7_skew_regsol", "Residual queue work includes N7, a skew-regular-solution N=7 item.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 205, 205),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(92, "queue_six_n8_equilibrium_data", "Residual queue work includes N8, equilibrium-data GITT or pOCV plus hold.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 205, 205),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(93, "queue_six_n9_bootstrap_ci", "Residual queue work includes N9, bootstrap confidence intervals.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 205, 205),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(94, "queue_six_c4_source_journal", "Residual queue work includes C-4, source-journal to M4 resolution.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 205, 206),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(95, "queue_six_d_trap_record", "Residual queue work includes D, the trap record in Chapter 2 Appendix A.", "workflow_queue", (("blob", HANDOVER_NEW, HANDOVER_PATH, 206, 206),), self_report_status="SOURCE_NORMATIVE_QUEUE", truth_status="VERIFIED_QUEUE_TEXT_EXISTS_NOT_CURRENT_AUTHORITY", owner="PHASE068_MASTER_PLAN", route="SUPERSEDED_BY_CURRENT_PHASE_PLAN"),
    _claim_def(96, "history_rows_appended", "The second commit reports appending two commit rows to the handover history table.", "repository_change_intent", (("commit_message", CLAUDE_COMMITS[1], "", 13, 13), ("blob", HANDOVER_NEW, HANDOVER_PATH, 46, 47), ("raw_diff_record", CLAUDE_COMMITS[1], HANDOVER_PATH, 1, 1)), self_report_status="SOURCE_ACTION_CLAIM_WITH_TREE_EDGE", truth_status="VERIFIED_PATH_CHANGED_CONTENT_MEANING_UNADJUDICATED", owner="STEP91_PROVENANCE_AUDIT", route="CLOSED_STEP91", quantity_unit_sign_basis=_q("2", "history rows", "appended", "second-commit self-report plus changed path")),
    _claim_def(97, "comparison_branch_location_added", "The second commit reports adding the current comparison branch to the handover location map.", "repository_change_intent", (("commit_message", CLAUDE_COMMITS[1], "", 13, 13), ("blob", HANDOVER_NEW, HANDOVER_PATH, 219, 219), ("raw_diff_record", CLAUDE_COMMITS[1], HANDOVER_PATH, 1, 1)), self_report_status="SOURCE_ACTION_CLAIM_WITH_TREE_EDGE", truth_status="VERIFIED_PATH_CHANGED_CONTENT_MEANING_UNADJUDICATED", owner="STEP91_PROVENANCE_AUDIT", route="STEP92"),
    _claim_def(98, "subcritical_gap_claim_confirmed_higher_precision", "The authors say the zero-subcritical-gap claim was the other remaining claim confirmed by the crosscheck at higher precision.", "numerical_validation_self_report", (("commit_message", CLAUDE_COMMITS[1], "", 10, 10), ("blob", HANDOVER_NEW, HANDOVER_PATH, 130, 131)), self_report_status="SOURCE_SELF_REPORT_NO_TRANSCRIPT", truth_status="UNVERIFIED_NUMERICAL_SELF_REPORT", owner="STEP94_SCIENTIFIC_ADJUDICATION", route="STEP94", assumptions=("the phrase 'remaining two claims' refers to the preceding area and subcritical-gap claims",)),
)

SUPPLEMENTAL_CLAIM_UNITS = (
    ("S91-01", "commit_message", CLAUDE_COMMITS[1], "", 3, 13, "restates_branch_u13_and_workflow_claims", ("C91-10", "C91-12", "C91-13", "C91-14", "C91-15", "C91-16", "C91-17", "C91-18", "C91-23", "C91-25", "C91-27", "C91-32", "C91-33", "C91-37", "C91-41", "C91-42", "C91-43", "C91-44", "C91-45", "C91-55", "C91-58", "C91-59", "C91-61", "C91-62", "C91-64", "C91-65", "C91-68", "C91-72", "C91-73", "C91-96", "C91-97", "C91-98")),
    ("S91-02", "blob", HANDOVER_NEW, HANDOVER_PATH, 46, 47, "history_rows", ("C91-25", "C91-26", "C91-27", "C91-30", "C91-31", "C91-96")),
    ("S91-03", "blob", HANDOVER_NEW, HANDOVER_PATH, 122, 134, "u13_restatement", ("C91-10", "C91-11", "C91-12", "C91-13", "C91-14", "C91-15", "C91-16", "C91-17", "C91-18", "C91-20", "C91-21", "C91-22", "C91-25", "C91-27", "C91-61", "C91-62", "C91-63", "C91-68", "C91-70", "C91-73", "C91-98")),
    ("S91-04", "blob", HANDOVER_NEW, HANDOVER_PATH, 157, 160, "workflow_restatement", ("C91-14", "C91-21", "C91-22", "C91-45", "C91-63", "C91-64", "C91-65", "C91-70")),
    ("S91-05", "blob", HANDOVER_NEW, HANDOVER_PATH, 187, 192, "self_reported_check_summary", ("C91-46", "C91-47", "C91-48", "C91-49", "C91-50", "C91-51")),
    ("S91-06", "blob", HANDOVER_NEW, HANDOVER_PATH, 196, 206, "planned_next_order", ("C91-37", "C91-52", "C91-55", "C91-60", "C91-79", "C91-80", "C91-81", "C91-82", "C91-83", "C91-84", "C91-85", "C91-86", "C91-87", "C91-88", "C91-89", "C91-90", "C91-91", "C91-92", "C91-93", "C91-94", "C91-95")),
    ("S91-07", "blob", HANDOVER_NEW, HANDOVER_PATH, 218, 219, "branch_location_status", ("C91-23", "C91-53", "C91-54", "C91-97")),
    ("S91-08", "blob", HANDOVER_NEW, HANDOVER_PATH, 63, 85, "p0_inventory_and_prior_finding_baseline", ("C91-23", "C91-24", "C91-32", "C91-33", "C91-34", "C91-35", "C91-36", "C91-37", "C91-38", "C91-39", "C91-40", "C91-41", "C91-42", "C91-43", "C91-44", "C91-58", "C91-66", "C91-67", "C91-71", "C91-72", "C91-74", "C91-75", "C91-76", "C91-78")),
)

KNOWN_FINDINGS = (
    {"id": "F91-P1-01", "severity": "P1", "claim_ids": ["C91-13", "C91-14", "C91-15", "C91-16"], "statement": "Finite sampled difference quotients alone do not establish C1 continuity; Step 94 must derive the limit and both one-sided derivatives."},
    {"id": "F91-P1-02", "severity": "P1", "claim_ids": ["C91-13", "C91-20"], "statement": "The reported 5.90 and 57.x ratios have unresolved normalization/provenance and must not be equated before Step 94."},
    {"id": "F91-P2-01", "severity": "P2", "claim_ids": ["C91-56"], "statement": "The handover header still routes ARCHIVE_NOTE U1-U12 although U13 now exists."},
    {"id": "F91-P2-02", "severity": "P2", "claim_ids": ["C91-29", "C91-47", "C91-48"], "statement": "STRUCTURE_CHECK and three-of-three checks are self-reports without transcripts in the two reviewed commits."},
)

MAX_JSON_BYTES = 4_000_000
MAX_JSON_DEPTH = 24
MAX_JSON_NODES = 50_000
CLAIM_COUNT = 98
SUPPLEMENTAL_CLAIM_UNIT_COUNT = 8
HEX40 = re.compile(r"^[0-9a-f]{40}$")
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
PRECOMMIT_MARKER = "P068_STEP91_CLAUDE_FORK_READ_PRECOMMIT"
PENDING_MARKER = "PENDING_AT_PRECOMMIT_BY_DESIGN"
COLLECT_LOCK = "Codex/results/.phase068_step91_collect.lock"
COLLECTOR_SCHEMA = "P068-STEP91-TWO-JSON-WRITER-1"
NEGATIVE_CONTROL_CATALOG = {
    "strict_json": tuple(f"N91-J{index:02d}" for index in range(1, 13)),
    "git_argv": tuple(f"N91-G{index:02d}" for index in range(1, 17)),
    "source_policy": tuple(f"N91-S{index:02d}" for index in range(1, 65)),
    "human_controls": tuple(f"N91-H{index:02d}" for index in range(1, 11)),
    "payload_contract": tuple(f"N91-P{index:02d}" for index in range(1, 30)),
}
EXPECTED_SOURCE_SEAL_SHA256 = {
    "builder": "c555ebfe2f40dd382248b2356efb7ae0f4c63b3f4f5da30f8db2e936fe0eac36",
    "validator": "359f92e3ff61f492a96d661f36bc221e3c7e456d7bf01a2f17c6650c8a875db1",
}


class ValidationError(RuntimeError):
    """A stable validation failure with a machine-readable code."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def fail(code: str, detail: str = "") -> None:
    raise ValidationError(code, detail)


ROOT = Path(__file__).resolve().parents[3]


def validate_git_argv(
    args: list[str],
    *,
    authorized_oids: tuple[str, ...] = (),
    authorized_pairs: tuple[tuple[str, str], ...] = (),
) -> None:
    """Fail closed unless a Git invocation has one declared read-only shape."""
    if type(args) is not list or not args or any(type(x) is not str or any(c in x for c in "\x00\r\n") for x in args):
        fail("E_GIT_ARG", repr(args))
    if type(authorized_oids) is not tuple or type(authorized_pairs) is not tuple or any(
        type(value) is not str or not HEX40.fullmatch(value) for value in authorized_oids
    ) or any(
        type(pair) is not tuple
        or len(pair) != 2
        or any(type(value) is not str or not HEX40.fullmatch(value) for value in pair)
        for pair in authorized_pairs
    ):
        fail("E_GIT_AUTHORIZATION", repr((authorized_oids, authorized_pairs)))
    command = args[0]
    fixed_object_oids = {EXPECTED_PARENT, BASE, *CLAUDE_COMMITS, *EXPECTED_BLOBS}
    allowed_object_oids = fixed_object_oids | set(authorized_oids)
    fixed_pairs = {
        (BASE, CLAUDE_COMMITS[0]),
        (CLAUDE_COMMITS[0], CLAUDE_COMMITS[1]),
        (BASE, CLAUDE_TIP),
    }
    allowed_pairs = fixed_pairs | set(authorized_pairs)
    if command == "branch":
        valid = args == ["branch", "--show-current"]
    elif command == "remote":
        valid = args == ["remote", "get-url", "origin"]
    elif command == "status":
        valid = args == ["status", "--porcelain=v1", "-z", "--untracked-files=all"]
    elif command == "rev-parse":
        valid = args in (
            ["rev-parse", "HEAD"],
            ["rev-parse", "@{upstream}"],
            ["rev-parse", "--abbrev-ref", "@{upstream}"],
            ["rev-parse", ACTIVE_REMOTE_REF],
            ["rev-parse", PROTECTED_LOCAL_REF],
            ["rev-parse", PROTECTED_REMOTE_REF],
            ["rev-parse", MAIN_LOCAL_REF],
            ["rev-parse", MAIN_REMOTE_REF],
            ["rev-parse", CLAUDE_LOCAL_REF],
            ["rev-parse", CLAUDE_REMOTE_REF],
            ["rev-parse", CODEX_FORK_LOCAL_REF],
            ["rev-parse", CODEX_FORK_REMOTE_REF],
        )
    elif command == "show-ref":
        valid = len(args) == 4 and args[:3] == ["show-ref", "--verify", "--quiet"] and args[3] in {
            PROTECTED_LOCAL_REF,
            MAIN_LOCAL_REF,
            CLAUDE_LOCAL_REF,
            CODEX_FORK_LOCAL_REF,
        }
    elif command == "cat-file":
        valid = len(args) == 3 and args[1] in {"-t", "commit", "blob"} and args[2] in allowed_object_oids
    elif command == "merge-base":
        valid = args == ["merge-base", BASE, CLAUDE_TIP]
    elif command == "rev-list":
        valid = args == ["rev-list", "--reverse", f"{BASE}..{CLAUDE_TIP}"]
    elif command == "diff-tree":
        valid = (
            len(args) == 7
            and args[1:5] == ["--no-commit-id", "--raw", "-z", "-r"]
            and (args[5], args[6]) in allowed_pairs
        )
    elif command == "diff":
        valid = args == ["diff", "--quiet"] or (
            len(args) == 6
            and args[1:5] == ["--cached", "--raw", "-z", "--abbrev=40"]
            and args[5] == EXPECTED_PARENT
        ) or args == ["diff", "--cached", "--name-status", "-z", EXPECTED_PARENT, "--"] or (
            len(args) == 6
            and args[1:3] == ["--name-status", "-z"]
            and (args[3], args[4]) in allowed_pairs
            and args[5] == "--"
        )
    elif command == "ls-files":
        valid = args == ["ls-files", "--stage", "-z", "--", *EXACT_EIGHT]
    elif command == "ls-tree":
        valid = (
            len(args) == 5
            and args[1] == "-z"
            and args[2] in authorized_oids
            and args[3] == "--"
            and args[4] in EXACT_EIGHT
        )
    elif command == "ls-remote":
        valid = args == ["ls-remote", "--exit-code", "origin", args[3]] if len(args) == 4 else False
        valid = bool(valid and args[3] in {
            ACTIVE_LIVE_REF,
            PROTECTED_LIVE_REF,
            MAIN_LIVE_REF,
            CLAUDE_LIVE_REF,
            CODEX_FORK_LIVE_REF,
        })
    else:
        fail("E_GIT_SUBCOMMAND", repr(args))
    if not valid:
        fail("E_GIT_ARGV_SHAPE", repr(args))


def run_git(
    args: list[str],
    *,
    authorized_oids: tuple[str, ...] = (),
    authorized_pairs: tuple[tuple[str, str], ...] = (),
) -> subprocess.CompletedProcess[bytes]:
    validate_git_argv(args, authorized_oids=authorized_oids, authorized_pairs=authorized_pairs)
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=300,
        shell=False,
    )


def git_bytes(
    args: list[str],
    *,
    authorized_oids: tuple[str, ...] = (),
    authorized_pairs: tuple[tuple[str, str], ...] = (),
) -> bytes:
    proc = run_git(args, authorized_oids=authorized_oids, authorized_pairs=authorized_pairs)
    if proc.returncode:
        fail("E_GIT", f"git {args!r}: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout


def git_returncode(args: list[str], accepted: tuple[int, ...]) -> int:
    proc = run_git(args)
    if proc.returncode not in accepted:
        fail("E_GIT_RETURN_CODE", f"git {args!r}: {proc.returncode}")
    return proc.returncode


def git_text(
    args: list[str],
    *,
    authorized_oids: tuple[str, ...] = (),
    authorized_pairs: tuple[tuple[str, str], ...] = (),
) -> str:
    return git_bytes(args, authorized_oids=authorized_oids, authorized_pairs=authorized_pairs).decode("utf-8", "strict").rstrip("\n")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def physical_line_count(raw: bytes) -> int:
    return 0 if not raw else raw.count(b"\n") + (0 if raw.endswith(b"\n") else 1)


def lf_normalize(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def split_lines(raw: bytes) -> list[str]:
    return raw.decode("utf-8", "strict").splitlines()


def line_span(raw: bytes, start: int, end: int) -> str:
    lines = split_lines(raw)
    if start < 1 or end < start or end > len(lines):
        fail("E_POINTER_RANGE", f"{start}-{end}/{len(lines)}")
    return "\n".join(lines[start - 1 : end])


def canonical_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic_sha(obj: dict[str, Any]) -> str:
    clone = dict(obj)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def _reject_constant(value: str) -> None:
    fail("E_JSON_NONFINITE", value)


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            fail("E_JSON_DUPLICATE_KEY", key)
        out[key] = value
    return out


def _shape(root: Any) -> tuple[int, int]:
    nodes = 0
    max_depth = 0
    stack = [(root, 1)]
    while stack:
        value, depth = stack.pop()
        nodes += 1
        max_depth = max(max_depth, depth)
        if nodes > MAX_JSON_NODES:
            fail("E_JSON_NODE_LIMIT", str(nodes))
        if depth > MAX_JSON_DEPTH:
            fail("E_JSON_DEPTH", str(depth))
        if isinstance(value, dict):
            stack.extend((v, depth + 1) for v in value.values())
        elif isinstance(value, list):
            stack.extend((v, depth + 1) for v in value)
        elif isinstance(value, float) and not math.isfinite(value):
            fail("E_JSON_NONFINITE", repr(value))
        elif isinstance(value, str) and len(value) > 1_000_000:
            fail("E_JSON_STRING_LIMIT", str(len(value)))
    return nodes, max_depth


def strict_load(raw: bytes) -> dict[str, Any]:
    if len(raw) > MAX_JSON_BYTES:
        fail("E_JSON_SIZE", str(len(raw)))
    if raw.startswith(b"\xef\xbb\xbf"):
        fail("E_JSON_BOM")
    if b"\r" in raw or not raw.endswith(b"\n") or raw.count(b"\n") != 1:
        fail("E_JSON_PHYSICAL_FORM")
    try:
        text = raw.decode("utf-8", "strict")
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_reject_constant)
    except ValidationError:
        raise
    except Exception as exc:
        fail("E_JSON_PARSE", str(exc))
    if not isinstance(value, dict):
        fail("E_JSON_ROOT", str(type(value)))
    _shape(value)
    if canonical_bytes(value) != raw:
        fail("E_JSON_NONCANONICAL")
    if value.get("semantic_sha256") != semantic_sha(value):
        fail("E_JSON_SEMANTIC_SHA")
    return value


def line_byte_interval(raw: bytes, start: int, end: int) -> list[int]:
    lines = raw.splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        fail("E_POINTER_RANGE", f"{start}-{end}/{len(lines)}")
    begin = sum(len(x) for x in lines[: start - 1])
    finish = sum(len(x) for x in lines[:end])
    return [begin, finish]


def ensure_object(oid: str, kind: str, *, authorized_oids: tuple[str, ...] = ()) -> None:
    if not HEX40.fullmatch(oid):
        fail("E_OID_FORM", oid)
    actual = git_text(["cat-file", "-t", oid], authorized_oids=authorized_oids)
    if actual != kind:
        fail("E_OBJECT_TYPE", f"{oid}: {actual} != {kind}")


def parse_commit(oid: str, *, authorized_oids: tuple[str, ...] = ()) -> tuple[dict[str, Any], bytes]:
    ensure_object(oid, "commit", authorized_oids=authorized_oids)
    raw = git_bytes(["cat-file", "commit", oid], authorized_oids=authorized_oids)
    recomputed_oid = hashlib.sha1(b"commit " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
    if recomputed_oid != oid:
        fail("E_COMMIT_OID", oid)
    header, separator, message = raw.partition(b"\n\n")
    if separator != b"\n\n" or not message:
        fail("E_COMMIT_FORM", oid)
    header_lines = header.decode("utf-8", "strict").splitlines()
    tree = next((line[5:] for line in header_lines if line.startswith("tree ")), "")
    parents = [line[7:] for line in header_lines if line.startswith("parent ")]
    author = next((line[7:] for line in header_lines if line.startswith("author ")), "")
    committer = next((line[10:] for line in header_lines if line.startswith("committer ")), "")
    message_lines = split_lines(message)
    if not message_lines:
        fail("E_COMMIT_MESSAGE", oid)
    record = {
        "oid": oid,
        "tree": tree,
        "parents": parents,
        "subject": message_lines[0],
        "author": author,
        "committer": committer,
        "raw_bytes": len(raw),
        "raw_sha256": sha256(raw),
        "git_oid_recomputed": recomputed_oid,
        "raw_lines": physical_line_count(raw),
        "message_offset": len(header) + 2,
        "message_bytes": len(message),
        "message_sha256": sha256(message),
        "message_lines": physical_line_count(message),
        "message_final_lf": message.endswith(b"\n"),
        "coverage": {"byte_start": 0, "byte_end": len(raw), "line_start": 1, "line_end": physical_line_count(raw), "status": "READ_FULL"},
        "signature_status": "PRESENT_NOT_AUTHENTICATED" if b"\ngpgsig " in b"\n" + header else "ABSENT",
    }
    return record, message


def parse_raw_diff(
    parent: str,
    child: str,
    allowed_status: tuple[str, ...] = ("M",),
    *,
    authorized_pairs: tuple[tuple[str, str], ...] = (),
) -> tuple[list[dict[str, str]], bytes]:
    raw = git_bytes(
        ["diff-tree", "--no-commit-id", "--raw", "-z", "-r", parent, child],
        authorized_pairs=authorized_pairs,
    )
    chunks = raw.split(b"\x00")
    if chunks and chunks[-1] == b"":
        chunks.pop()
    if len(chunks) % 2:
        fail("E_DIFF_FORM", f"{parent}..{child}")
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    offset = 0
    for index in range(0, len(chunks), 2):
        meta_raw, path_raw = chunks[index], chunks[index + 1]
        meta = meta_raw.decode("ascii", "strict")
        path = path_raw.decode("utf-8", "strict")
        fields = meta.split(" ")
        if len(fields) != 5 or not fields[0].startswith(":"):
            fail("E_DIFF_META", meta)
        status = fields[4]
        if status not in allowed_status:
            fail("E_DIFF_STATUS", f"{path}: {status}")
        if path in seen:
            fail("E_DIFF_DUPLICATE", path)
        seen.add(path)
        record_end = offset + len(meta_raw) + 1 + len(path_raw) + 1
        out.append(
            {
                "path": path,
                "status": status,
                "old_mode": fields[0][1:],
                "new_mode": fields[1],
                "old_blob": fields[2],
                "new_blob": fields[3],
                "raw_byte_start": str(offset),
                "raw_byte_end": str(record_end),
            }
        )
        offset = record_end
    if offset != len(raw):
        fail("E_DIFF_COVERAGE", f"{offset}/{len(raw)}")
    return out, raw


def expected_edge_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    edges: list[dict[str, Any]] = []
    occurrences: list[dict[str, Any]] = []
    for edge_index, expected in enumerate(EXPECTED_EDGES, 1):
        records, raw = parse_raw_diff(expected["parent"], expected["commit"])
        compact = [
            (r["path"], r["status"], r["old_mode"], r["new_mode"], r["old_blob"], r["new_blob"])
            for r in records
        ]
        if tuple(compact) != expected["paths"]:
            fail("E_EDGE_SET", f"edge {edge_index}: {compact!r}")
        if len(records) != (2 if edge_index == 1 else 1):
            fail("E_EDGE_COUNT", f"edge {edge_index}: {len(records)}")
        edge = {
            "index": edge_index,
            "parent": expected["parent"],
            "commit": expected["commit"],
            "path_count": len(records),
            "raw_diff_bytes": len(raw),
            "raw_diff_sha256": sha256(raw),
            "raw_diff_coverage": {"byte_start": 0, "byte_end": len(raw), "status": "READ_FULL"},
            "changes": records,
        }
        edges.append(edge)
        for record in records:
            for side in ("old", "new"):
                occurrences.append(
                    {
                        "edge_index": edge_index,
                        "commit": expected["commit"],
                        "path": record["path"],
                        "side": side,
                        "mode": record[f"{side}_mode"],
                        "blob": record[f"{side}_blob"],
                    }
                )
    return edges, occurrences


def expected_blob_records(occurrences: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = sorted({item["blob"] for item in occurrences})
    if set(seen) != set(EXPECTED_BLOBS):
        fail("E_BLOB_SET", repr(seen))
    out: list[dict[str, Any]] = []
    for oid in seen:
        ensure_object(oid, "blob")
        raw = git_bytes(["cat-file", "blob", oid])
        expected_bytes, expected_sha, expected_lines = EXPECTED_BLOBS[oid]
        if (len(raw), sha256(raw), physical_line_count(raw)) != (expected_bytes, expected_sha, expected_lines):
            fail("E_BLOB_IDENTITY", oid)
        # Recompute the Git blob object id, so an object-store lookup is not the only check.
        recomputed_oid = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
        if recomputed_oid != oid:
            fail("E_BLOB_OID", oid)
        raw.decode("utf-8", "strict")
        lf = lf_normalize(raw)
        out.append(
            {
                "oid": oid,
                "media_type": "text/x-tex" if any(x["path"] == TEX_PATH and x["blob"] == oid for x in occurrences) else "text/markdown",
                "encoding": "utf-8",
                "raw_bytes": len(raw),
                "raw_sha256": sha256(raw),
                "raw_lines": physical_line_count(raw),
                "raw_final_lf": raw.endswith(b"\n"),
                "raw_cr_bytes": raw.count(b"\r"),
                "lf_bytes": len(lf),
                "lf_sha256": sha256(lf),
                "lf_lines": physical_line_count(lf),
                "coverage": {"byte_start": 0, "byte_end": len(raw), "line_start": 1, "line_end": physical_line_count(raw), "status": "READ_FULL"},
                "git_oid_recomputed": recomputed_oid,
            }
        )
    return out


def claim_pointer(kind: str, oid: str, path: str, start: int, end: int) -> dict[str, Any]:
    if kind == "blob":
        raw = git_bytes(["cat-file", "blob", oid])
        interval = line_byte_interval(raw, start, end)
        excerpt_raw = raw[interval[0] : interval[1]]
    elif kind == "commit_message":
        _, raw = parse_commit(oid)
        interval = line_byte_interval(raw, start, end)
        excerpt_raw = raw[interval[0] : interval[1]]
    elif kind == "commit_object":
        ensure_object(oid, "commit")
        raw = git_bytes(["cat-file", "commit", oid])
        interval = line_byte_interval(raw, start, end)
        excerpt_raw = raw[interval[0] : interval[1]]
    elif kind == "raw_diff_record":
        parent = EXPECTED_PARENTS[oid][0]
        records, raw = parse_raw_diff(parent, oid)
        matches = [item for item in records if item["path"] == path]
        if len(matches) != 1:
            fail("E_CLAIM_DIFF_POINTER", f"{oid}:{path}")
        interval = [int(matches[0]["raw_byte_start"]), int(matches[0]["raw_byte_end"])]
        excerpt_raw = raw[interval[0] : interval[1]]
    elif kind == "raw_diff_net":
        records, raw = parse_raw_diff(BASE, CLAUDE_TIP)
        if len(records) != 3:
            fail("E_CLAIM_NET_POINTER", str(len(records)))
        interval = [0, len(raw)]
        excerpt_raw = raw
    else:
        fail("E_CLAIM_KIND", kind)
    try:
        excerpt = excerpt_raw.decode("utf-8", "strict").replace("\x00", "\\0")
    except UnicodeDecodeError:
        excerpt = excerpt_raw.hex()
    full_source = interval == [0, len(raw)]
    return {
        "source_kind": kind,
        "source_oid": oid,
        "path": path or None,
        "line_start": start if kind in {"blob", "commit_message", "commit_object"} else None,
        "line_end": end if kind in {"blob", "commit_message", "commit_object"} else None,
        "byte_start": interval[0],
        "byte_end": interval[1],
        "source_bytes_sha256": sha256(excerpt_raw),
        "source_text": excerpt,
        "coverage_status": "FULL_SOURCE" if full_source else "EXACT_SLICE_OF_FULLY_READ_SOURCE",
    }


def expected_claim_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for definition in CLAIM_DEFS:
        pointers = []
        for evidence_id, spec in zip(definition["supporting_evidence_ids"], definition["sources"], strict=True):
            pointer = claim_pointer(*spec)
            pointer["evidence_id"] = evidence_id
            pointers.append(pointer)
        records.append(
            {
                "id": definition["id"],
                "assertion_key": definition["assertion_key"],
                "normalized_proposition": definition["normalized_proposition"],
                "domain": definition["domain"],
                "assumptions": list(definition["assumptions"]),
                "quantity_unit_sign_basis": definition["quantity_unit_sign_basis"],
                "claimant_surfaces": pointers,
                "self_report_status": definition["self_report_status"],
                "truth_status": definition["truth_status"],
                "supporting_evidence_ids": list(definition["supporting_evidence_ids"]),
                "refuting_evidence_ids": list(definition["refuting_evidence_ids"]),
                "authority_ceiling": definition["authority_ceiling"],
                "owner": definition["owner"],
                "scientific_truth_promoted": False,
                "source_self_report_is_not_truth": True,
                "route": definition["route"],
            }
        )
    if [x["id"] for x in records] != [f"C91-{i:02d}" for i in range(1, CLAIM_COUNT + 1)]:
        fail("E_CLAIM_IDS")
    return records


def supplemental_claim_records() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for unit_id, kind, oid, path, start, end, purpose, claim_ids in SUPPLEMENTAL_CLAIM_UNITS:
        out.append(
            {
                "id": unit_id,
                "purpose": purpose,
                "truth_status": "SOURCE_UNIT_ONLY_NOT_ADJUDICATED",
                "scientific_truth_promoted": False,
                "claim_ids": list(claim_ids),
                "source": claim_pointer(kind, oid, path, start, end),
            }
        )
    return out


def exhaustive_supplemental_claim_ids(
    kind: str, oid: str, path: str, start: int, end: int
) -> list[str]:
    """Return every claim pointer overlapping one fixed supplemental source unit."""
    return [
        definition["id"]
        for definition in CLAIM_DEFS
        if any(
            source_kind == kind
            and source_oid == oid
            and source_path == path
            and not (source_end < start or source_start > end)
            for source_kind, source_oid, source_path, source_start, source_end in definition["sources"]
        )
    ]


def file_identity(path: str) -> dict[str, Any]:
    target = ROOT / path
    if not target.is_file():
        fail("E_INPUT_MISSING", path)
    raw = target.read_bytes()
    return {"path": path, "bytes": len(raw), "sha256": sha256(raw), "physical_lines": physical_line_count(raw)}


def build_payload_objects() -> tuple[dict[str, Any], dict[str, Any]]:
    """Reconstruct both payloads from fixed Git objects and frozen pre-JSON files."""
    merge_base = git_text(["merge-base", BASE, CLAUDE_TIP])
    if merge_base != BASE:
        fail("E_MERGE_BASE", merge_base)
    commit_set = git_text(["rev-list", "--reverse", f"{BASE}..{CLAUDE_TIP}"]).splitlines()
    if commit_set != list(CLAUDE_COMMITS):
        fail("E_COMMIT_SET", repr(commit_set))
    commits: list[dict[str, Any]] = []
    message_map: dict[str, bytes] = {}
    for oid in CLAUDE_COMMITS:
        record, message = parse_commit(oid)
        if tuple(record["parents"]) != EXPECTED_PARENTS[oid] or record["subject"] != EXPECTED_SUBJECTS[oid]:
            fail("E_COMMIT_METADATA", oid)
        commits.append(record)
        message_map[oid] = message
    edges, occurrences = expected_edge_records()
    net, net_raw = parse_raw_diff(BASE, CLAUDE_TIP)
    expected_net = sorted([row for edge in EXPECTED_EDGES for row in edge["paths"]], key=lambda x: x[0])
    actual_net = sorted(
        [(r["path"], r["status"], r["old_mode"], r["new_mode"], r["old_blob"], r["new_blob"]) for r in net],
        key=lambda x: x[0],
    )
    if actual_net != expected_net or len(net) != 3:
        fail("E_NET_SET", repr(actual_net))
    blobs = expected_blob_records(occurrences)
    claims = expected_claim_records()
    supplemental = supplemental_claim_records()
    pre_json = [file_identity(path) for path in PRE_JSON_SIX]
    evidence_basis = {
        "base": BASE,
        "tip": CLAUDE_TIP,
        "commit_oids": list(CLAUDE_COMMITS),
        "edge_raw_sha256": [edge["raw_diff_sha256"] for edge in edges],
        "net_raw_sha256": sha256(net_raw),
        "blob_raw_sha256": [item["raw_sha256"] for item in blobs],
        "claim_source_sha256": [source["source_bytes_sha256"] for item in claims for source in item["claimant_surfaces"]],
        "supplemental_source_sha256": [item["source"]["source_bytes_sha256"] for item in supplemental],
    }
    evidence_set_sha = sha256(canonical_bytes(evidence_basis))
    inventory: dict[str, Any] = {
        "schema": SCHEMA_INVENTORY,
        "authority": "AUDIT_INVENTORY_ONLY_NO_SCIENTIFIC_ADJUDICATION",
        "expected_parent": EXPECTED_PARENT,
        "branch": ACTIVE_BRANCH,
        "claude_ref": CLAUDE_LIVE_REF,
        "base": BASE,
        "tip": CLAUDE_TIP,
        "merge_base": merge_base,
        "commit_count": 2,
        "commits": commits,
        "edge_count": 2,
        "edges": edges,
        "edge_path_counts": [2, 1],
        "net_path_count": 3,
        "net_changes": net,
        "net_raw_diff_bytes": len(net_raw),
        "net_raw_diff_sha256": sha256(net_raw),
        "net_raw_diff_coverage": {"byte_start": 0, "byte_end": len(net_raw), "status": "READ_FULL"},
        "claim_count": len(claims),
        "claim_source_pointer_count": sum(len(item["claimant_surfaces"]) for item in claims),
        "claims": claims,
        "supplemental_claim_units": supplemental,
        "findings": list(KNOWN_FINDINGS),
        "u13_disposition": "UNDECIDED_ROUTE_STEP94",
        "scientific_truth_promotions": 0,
        "negative_control_catalog": {key: list(value) for key, value in NEGATIVE_CONTROL_CATALOG.items()},
        "negative_control_count": sum(len(value) for value in NEGATIVE_CONTROL_CATALOG.values()),
        "pre_json_file_identities": pre_json,
        "attestation_path": ATTESTATION,
        "evidence_set_sha256": evidence_set_sha,
        "content_terminal": CONTENT_TERMINAL,
    }
    inventory["semantic_sha256"] = semantic_sha(inventory)
    inventory_raw = canonical_bytes(inventory)
    attestation: dict[str, Any] = {
        "schema": SCHEMA_ATTESTATION,
        "authority": "BYTE_COVERAGE_ATTESTATION_ONLY_NO_SCIENTIFIC_ADJUDICATION",
        "expected_parent": EXPECTED_PARENT,
        "base": BASE,
        "tip": CLAUDE_TIP,
        "commit_object_count": len(commits),
        "commit_objects": commits,
        "commit_message_occurrences": [
            {
                "oid": oid,
                "byte_start": 0,
                "byte_end": len(message_map[oid]),
                "line_start": 1,
                "line_end": physical_line_count(message_map[oid]),
                "raw_sha256": sha256(message_map[oid]),
                "status": "READ_FULL",
            }
            for oid in CLAUDE_COMMITS
        ],
        "edge_count": len(edges),
        "edge_path_event_count": sum(edge["path_count"] for edge in edges),
        "blob_side_occurrence_count": len(occurrences),
        "unique_blob_count": len(blobs),
        "blob_occurrences": occurrences,
        "unique_blobs": blobs,
        "coverage_gaps": [],
        "binary_or_pdf_objects": [],
        "negative_control_count": sum(len(value) for value in NEGATIVE_CONTROL_CATALOG.values()),
        "negative_control_case_ids": [case_id for value in NEGATIVE_CONTROL_CATALOG.values() for case_id in value],
        "claim_count": len(claims),
        "claim_source_pointer_count": sum(len(item["claimant_surfaces"]) for item in claims),
        "claim_ids": [item["id"] for item in claims],
        "supplemental_claim_unit_count": len(supplemental),
        "supplemental_claim_unit_ids": [item["id"] for item in supplemental],
        "evidence_set_sha256": evidence_set_sha,
        "inventory_path": INVENTORY,
        "inventory_bytes": len(inventory_raw),
        "inventory_sha256": sha256(inventory_raw),
        "pre_json_file_identities": pre_json,
        "u13_disposition": "UNDECIDED_ROUTE_STEP94",
        "content_terminal": CONTENT_TERMINAL,
    }
    attestation["semantic_sha256"] = semantic_sha(attestation)
    validate_payload_contract(inventory, attestation)
    return inventory, attestation


def validate_payload_contract(inventory: dict[str, Any], attestation: dict[str, Any]) -> None:
    inventory_fields = {
        "schema", "authority", "expected_parent", "branch", "claude_ref", "base", "tip", "merge_base",
        "commit_count", "commits", "edge_count", "edges", "edge_path_counts", "net_path_count", "net_changes",
        "net_raw_diff_bytes", "net_raw_diff_sha256", "net_raw_diff_coverage", "claim_count",
        "claim_source_pointer_count", "claims", "supplemental_claim_units", "findings", "u13_disposition",
        "scientific_truth_promotions", "negative_control_catalog", "negative_control_count", "pre_json_file_identities", "attestation_path", "evidence_set_sha256",
        "content_terminal", "semantic_sha256",
    }
    attestation_fields = {
        "schema", "authority", "expected_parent", "base", "tip", "commit_object_count", "commit_objects",
        "commit_message_occurrences", "edge_count", "edge_path_event_count", "blob_side_occurrence_count",
        "unique_blob_count", "blob_occurrences", "unique_blobs", "coverage_gaps", "binary_or_pdf_objects",
        "negative_control_count", "negative_control_case_ids",
        "claim_count", "claim_source_pointer_count", "claim_ids", "supplemental_claim_unit_count",
        "supplemental_claim_unit_ids", "evidence_set_sha256", "inventory_path", "inventory_bytes",
        "inventory_sha256", "pre_json_file_identities", "u13_disposition", "content_terminal", "semantic_sha256",
    }
    if set(inventory) != inventory_fields or set(attestation) != attestation_fields:
        fail("E_CONTRACT_TOP_LEVEL_FIELDS")
    if inventory["schema"] != SCHEMA_INVENTORY or attestation["schema"] != SCHEMA_ATTESTATION:
        fail("E_CONTRACT_SCHEMA")
    if inventory["expected_parent"] != EXPECTED_PARENT or attestation["expected_parent"] != EXPECTED_PARENT:
        fail("E_CONTRACT_PARENT_CERTIFICATE")
    commits = inventory.get("commits")
    if not isinstance(commits, list) or inventory.get("commit_count") != 2 or len(commits) != 2:
        fail("E_CONTRACT_COMMIT_COUNT")
    if [item.get("oid") for item in commits] != list(CLAUDE_COMMITS):
        fail("E_CONTRACT_COMMIT_IDENTITY")
    if [tuple(item.get("parents", ())) for item in commits] != [EXPECTED_PARENTS[oid] for oid in CLAUDE_COMMITS]:
        fail("E_CONTRACT_COMMIT_PARENT")
    if [item.get("subject") for item in commits] != [EXPECTED_SUBJECTS[oid] for oid in CLAUDE_COMMITS]:
        fail("E_CONTRACT_COMMIT_SUBJECT")
    edges = inventory.get("edges")
    if not isinstance(edges, list) or inventory.get("edge_count") != 2 or len(edges) != 2 or inventory.get("edge_path_counts") != [2, 1]:
        fail("E_CONTRACT_EDGE_COUNT")
    for index, (edge, expected) in enumerate(zip(edges, EXPECTED_EDGES, strict=True), 1):
        if edge.get("index") != index or edge.get("parent") != expected["parent"] or edge.get("commit") != expected["commit"]:
            fail("E_CONTRACT_EDGE_IDENTITY", str(index))
        changes = edge.get("changes")
        if not isinstance(changes, list) or edge.get("path_count") != len(expected["paths"]) or len(changes) != len(expected["paths"]):
            fail("E_CONTRACT_EDGE_PATH_COUNT", str(index))
        actual = [(item.get("path"), item.get("status"), item.get("old_mode"), item.get("new_mode"), item.get("old_blob"), item.get("new_blob")) for item in changes]
        if [row[0] for row in actual] != [row[0] for row in expected["paths"]]:
            fail("E_CONTRACT_EDGE_PATH", str(index))
        if [row[1] for row in actual] != [row[1] for row in expected["paths"]]:
            fail("E_CONTRACT_EDGE_STATUS", str(index))
        if [(row[2], row[3]) for row in actual] != [(row[2], row[3]) for row in expected["paths"]]:
            fail("E_CONTRACT_EDGE_MODE", str(index))
        if [(row[4], row[5]) for row in actual] != [(row[4], row[5]) for row in expected["paths"]]:
            fail("E_CONTRACT_EDGE_BLOB", str(index))
    expected_net = sorted([row for edge in EXPECTED_EDGES for row in edge["paths"]], key=lambda row: row[0])
    net = inventory.get("net_changes")
    if not isinstance(net, list) or inventory.get("net_path_count") != 3 or len(net) != 3:
        fail("E_CONTRACT_NET_COUNT")
    actual_net = [(item.get("path"), item.get("status"), item.get("old_mode"), item.get("new_mode"), item.get("old_blob"), item.get("new_blob")) for item in net]
    if actual_net != expected_net:
        fail("E_CONTRACT_NET_TOPOLOGY")
    blobs = attestation.get("unique_blobs")
    if not isinstance(blobs, list) or attestation.get("unique_blob_count") != 6 or len(blobs) != 6:
        fail("E_CONTRACT_BLOB_COUNT")
    if {item.get("oid") for item in blobs} != set(EXPECTED_BLOBS):
        fail("E_CONTRACT_BLOB_IDENTITY")
    for blob in blobs:
        coverage = blob.get("coverage")
        if not isinstance(coverage, dict) or coverage.get("byte_start") != 0 or coverage.get("byte_end") != blob.get("raw_bytes") or coverage.get("line_start") != 1 or coverage.get("line_end") != blob.get("raw_lines") or coverage.get("status") != "READ_FULL":
            fail("E_CONTRACT_BLOB_COVERAGE", str(blob.get("oid")))
    claims = inventory.get("claims")
    expected_ids = [f"C91-{index:02d}" for index in range(1, CLAIM_COUNT + 1)]
    if not isinstance(claims, list) or inventory.get("claim_count") != CLAIM_COUNT or len(claims) != CLAIM_COUNT:
        fail("E_CONTRACT_CLAIM_COUNT")
    if [item.get("id") for item in claims] != expected_ids or len({item.get("id") for item in claims}) != CLAIM_COUNT:
        fail("E_CONTRACT_CLAIM_IDS")
    claim_fields = {
        "id", "assertion_key", "normalized_proposition", "domain", "assumptions", "quantity_unit_sign_basis",
        "claimant_surfaces", "self_report_status", "truth_status", "supporting_evidence_ids",
        "refuting_evidence_ids", "authority_ceiling", "owner", "scientific_truth_promoted",
        "source_self_report_is_not_truth", "route",
    }
    pointer_fields = {
        "evidence_id", "source_kind", "source_oid", "path", "line_start", "line_end", "byte_start",
        "byte_end", "source_bytes_sha256", "source_text", "coverage_status",
    }
    evidence_ids: list[str] = []
    for claim_index, claim in enumerate(claims):
        if set(claim) != claim_fields:
            fail("E_CONTRACT_CLAIM_FIELDS", str(claim.get("id")))
        if claim.get("scientific_truth_promoted") is not False or claim.get("source_self_report_is_not_truth") is not True:
            fail("E_CONTRACT_AUTHORITY_PROMOTION", str(claim.get("id")))
        surfaces = claim.get("claimant_surfaces")
        if not isinstance(surfaces, list) or not surfaces:
            fail("E_CONTRACT_CLAIM_SURFACES", str(claim.get("id")))
        if any(set(pointer) != pointer_fields for pointer in surfaces):
            fail("E_CONTRACT_POINTER_FIELDS", str(claim.get("id")))
        surface_ids = [pointer.get("evidence_id") for pointer in surfaces]
        if surface_ids != claim.get("supporting_evidence_ids"):
            fail("E_CONTRACT_EVIDENCE_LINK", str(claim.get("id")))
        if any(pointer.get("coverage_status") not in {"FULL_SOURCE", "EXACT_SLICE_OF_FULLY_READ_SOURCE"} for pointer in surfaces):
            fail("E_CONTRACT_POINTER_COVERAGE", str(claim.get("id")))
        if any(ref not in expected_ids for ref in claim.get("refuting_evidence_ids", [])):
            fail("E_CONTRACT_REFUTING_LINK", str(claim.get("id")))
        definition = CLAIM_DEFS[claim_index]
        expected_metadata = {
            "id": definition["id"],
            "assertion_key": definition["assertion_key"],
            "normalized_proposition": definition["normalized_proposition"],
            "domain": definition["domain"],
            "assumptions": list(definition["assumptions"]),
            "quantity_unit_sign_basis": definition["quantity_unit_sign_basis"],
            "self_report_status": definition["self_report_status"],
            "truth_status": definition["truth_status"],
            "supporting_evidence_ids": list(definition["supporting_evidence_ids"]),
            "refuting_evidence_ids": list(definition["refuting_evidence_ids"]),
            "authority_ceiling": definition["authority_ceiling"],
            "owner": definition["owner"],
            "route": definition["route"],
        }
        if any(claim.get(key) != value for key, value in expected_metadata.items()):
            fail("E_CONTRACT_CLAIM_METADATA", str(claim.get("id")))
        for pointer, spec, evidence_id in zip(surfaces, definition["sources"], definition["supporting_evidence_ids"], strict=True):
            kind, oid, path, start, end = spec
            expected_pointer_identity = {
                "evidence_id": evidence_id,
                "source_kind": kind,
                "source_oid": oid,
                "path": path or None,
                "line_start": start if kind in {"blob", "commit_message", "commit_object"} else None,
                "line_end": end if kind in {"blob", "commit_message", "commit_object"} else None,
            }
            if any(pointer.get(key) != value for key, value in expected_pointer_identity.items()):
                fail("E_CONTRACT_POINTER_IDENTITY", str(claim.get("id")))
        evidence_ids.extend(surface_ids)
    if len(evidence_ids) != len(set(evidence_ids)):
        fail("E_CONTRACT_EVIDENCE_DUPLICATE")
    if inventory.get("claim_source_pointer_count") != len(evidence_ids):
        fail("E_CONTRACT_CLAIM_POINTER_DENOMINATOR")
    c1 = claims[15]
    if c1.get("id") != "C91-16" or c1.get("owner") != "STEP94_SCIENTIFIC_ADJUDICATION" or c1.get("route") != "STEP94" or c1.get("truth_status") != "UNDECIDED_REQUIRES_LIMIT_AND_ONE_SIDED_DERIVATIVES":
        fail("E_CONTRACT_C1_ROUTE")
    supplemental = inventory.get("supplemental_claim_units")
    if not isinstance(supplemental, list) or [item.get("id") for item in supplemental] != [f"S91-{index:02d}" for index in range(1, SUPPLEMENTAL_CLAIM_UNIT_COUNT + 1)]:
        fail("E_CONTRACT_SUPPLEMENTAL_IDS")
    if any(not item.get("claim_ids") or any(claim_id not in expected_ids for claim_id in item.get("claim_ids", [])) for item in supplemental):
        fail("E_CONTRACT_SUPPLEMENTAL_LINK")
    for item, unit in zip(supplemental, SUPPLEMENTAL_CLAIM_UNITS, strict=True):
        _, kind, oid, path, start, end, _, _ = unit
        if item.get("claim_ids") != exhaustive_supplemental_claim_ids(kind, oid, path, start, end):
            fail("E_CONTRACT_SUPPLEMENTAL_EXHAUSTIVE", str(item.get("id")))
    finding_ids = [item.get("id") for item in inventory.get("findings", [])]
    if finding_ids != ["F91-P1-01", "F91-P1-02", "F91-P2-01", "F91-P2-02"]:
        fail("E_CONTRACT_FINDINGS")
    if inventory.get("u13_disposition") != "UNDECIDED_ROUTE_STEP94" or inventory.get("scientific_truth_promotions") != 0:
        fail("E_CONTRACT_U13_AUTHORITY")
    expected_catalog = {key: list(value) for key, value in NEGATIVE_CONTROL_CATALOG.items()}
    flattened_controls = [case_id for value in NEGATIVE_CONTROL_CATALOG.values() for case_id in value]
    if inventory.get("negative_control_catalog") != expected_catalog or inventory.get("negative_control_count") != len(flattened_controls):
        fail("E_CONTRACT_NEGATIVE_CONTROL_CATALOG")
    pointer_count = len(evidence_ids)
    if (
        attestation.get("commit_object_count") != 2
        or attestation.get("edge_count") != 2
        or attestation.get("edge_path_event_count") != 3
        or attestation.get("blob_side_occurrence_count") != 6
        or attestation.get("claim_count") != CLAIM_COUNT
        or attestation.get("claim_source_pointer_count") != pointer_count
        or attestation.get("claim_ids") != expected_ids
        or attestation.get("negative_control_count") != len(flattened_controls)
        or attestation.get("negative_control_case_ids") != flattened_controls
    ):
        fail("E_CONTRACT_ATTESTATION_DENOMINATORS")
    if attestation.get("coverage_gaps") != [] or attestation.get("binary_or_pdf_objects") != []:
        fail("E_CONTRACT_COVERAGE_GAPS")
    if inventory.get("evidence_set_sha256") != attestation.get("evidence_set_sha256"):
        fail("E_CONTRACT_EVIDENCE_BINDING")
    if inventory.get("content_terminal") != CONTENT_TERMINAL or attestation.get("content_terminal") != CONTENT_TERMINAL:
        fail("E_CONTRACT_TERMINAL")


def read_text_file(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        fail("E_OUTPUT_MISSING", path)
    try:
        return target.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail("E_TEXT_UTF8", f"{path}: {exc}")


def require_tokens(path: str, tokens: Iterable[str]) -> str:
    text = read_text_file(path)
    for token in tokens:
        if token not in text:
            fail("E_CONTROL_TOKEN", f"{path}: {token}")
    return text


def require_exact_prefixed_line(text: str, path: str, prefix: str, expected: str) -> None:
    matches = [line for line in text.splitlines() if line.startswith(prefix)]
    if matches != [expected]:
        fail("E_CONTROL_EXACT_LINE", f"{path}: {prefix!r}")


def parse_markdown_row(line: str, path: str) -> tuple[str, ...]:
    if not line.startswith("|") or not line.endswith("|"):
        fail("E_CONTROL_ROW_FORM", path)
    cells = tuple(cell.strip() for cell in line[1:-1].split("|"))
    if not cells or any(cell == "" for cell in cells):
        fail("E_CONTROL_ROW_FORM", path)
    return cells


def require_exact_markdown_row(text: str, path: str, prefix: str, expected: tuple[str, ...]) -> None:
    matches = [line for line in text.splitlines() if line.startswith(prefix)]
    if len(matches) != 1 or parse_markdown_row(matches[0], path) != expected:
        fail("E_CONTROL_ROW_EXACT", f"{path}: {prefix!r}")


def require_exact_section(text: str, path: str, heading: str, expected_body: str, next_heading: str) -> None:
    lines = text.splitlines()
    indexes = [index for index, line in enumerate(lines) if line == heading]
    if len(indexes) != 1:
        fail("E_CONTROL_SECTION_EXACT", f"{path}: {heading!r}")
    start = indexes[0]
    next_indexes = [index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")]
    if not next_indexes or lines[next_indexes[0]] != next_heading:
        fail("E_CONTROL_SECTION_EXACT", f"{path}: {heading!r} next")
    if lines[start:next_indexes[0]] != [heading, "", expected_body, ""]:
        fail("E_CONTROL_SECTION_EXACT", f"{path}: {heading!r} body")


def validate_human_control_texts(result: str, parent: str, active: str, handover: str) -> None:
    claim_range = f"C91-01..C91-{CLAIM_COUNT:02d}"
    pointer_count = sum(len(definition["sources"]) for definition in CLAIM_DEFS)
    negative_count = sum(len(case_ids) for case_ids in NEGATIVE_CONTROL_CATALOG.values())
    summary_counts = f"2/2/2+1/3/6/{CLAIM_COUNT}/{pointer_count}/{negative_count}"
    result_fields = (
        ("Status: ", "Status: `PASS_PENDING_PERSISTENCE`"),
        ("Selected Gate: ", f"Selected Gate: `{CONTENT_TERMINAL}`"),
        ("Persistence terminal: ", f"Persistence terminal: `{PERSISTENCE_TERMINAL}`"),
        ("Containing commit: ", f"Containing commit: `{PENDING_MARKER}`"),
        ("Current-state marker: ", f"Current-state marker: `{PRECOMMIT_MARKER}`"),
        ("Expected parent: ", f"Expected parent: `{EXPECTED_PARENT}`"),
        ("Expected subject: ", f"Expected subject: `{EXPECTED_SUBJECT}`"),
        ("Next cumulative Step: ", "Next cumulative Step: `Step 92`"),
    )
    for prefix, expected in result_fields:
        require_exact_prefixed_line(result, RESULT, prefix, expected)
    for token in (
            BASE,
            CLAUDE_COMMITS[0],
            CLAUDE_COMMITS[1],
            "2/1",
            "net 3",
            "6",
            "C91-01",
            f"C91-{CLAIM_COUNT:02d}",
            "UNDECIDED_ROUTE_STEP94",
            "scientific truth promotions: 0",
            "F91-P1-01",
            "F91-P1-02",
            "F91-P2-01",
            "F91-P2-02",
            INVENTORY,
            ATTESTATION,
        ):
        if token not in result:
            fail("E_CONTROL_TOKEN", f"{RESULT}: {token!r}")
    last = next((line.strip() for line in reversed(result.splitlines()) if line.strip()), "")
    if last != CONTENT_TERMINAL:
        fail("E_RESULT_TERMINAL", last)
    parent_cells = (
        "068",
        "91–98",
        "plan activation persisted; Step 91 content fixed pending persistence; Steps 92–98 pending",
        "fork",
        "기존 Codex/Claude 검토 재판정",
        "PASS_PENDING_PERSISTENCE",
        "`Codex/plans/2026-09-07-phase068-claude-codex-fork-adjudication-detailed-plan.md`",
        f"activation `Codex/results/PHASE_068_PLAN_ACTIVATION_RESULT.md`; current `{RESULT}`",
        f"activation validator/JSON retained; current `{BUILDER}`, `{VALIDATOR}`, `{INVENTORY}`, `{ATTESTATION}`; exact-eight `A/A/A/A/A/M/M/M`, all `100644`",
        f"activation exact-seven commit `{EXPECTED_PARENT}`, parent `0371387f582fb63f5c3858d7e6905ed83eee885f`, pushed/live/clean with dual `PASS_P068_PLAN_ACTIVATION_PERSISTENCE`; Step 91 selected `{CONTENT_TERMINAL}` under `{PRECOMMIT_MARKER}`, expected parent `{EXPECTED_PARENT}`, subject `{EXPECTED_SUBJECT}`, containing commit `{PENDING_MARKER}`, reserved terminal `{PERSISTENCE_TERMINAL}`; commits/edges/path-counts/net/blobs/claims/pointers/negative controls `{summary_counts}`, register `{claim_range}`; U13 `UNDECIDED_ROUTE_STEP94`, scientific promotions 0",
        "Step 91 review, dual staged validation, commit/push/live/clean and dual persistence, then Step 92",
    )
    active_cells = (
        "068",
        "91–98",
        "plan activation persisted; Step 91 content fixed pending persistence; Steps 92–98 pending",
        "fork adjudication",
        "PASS_PENDING_PERSISTENCE",
        "`Codex/plans/2026-09-07-phase068-claude-codex-fork-adjudication-detailed-plan.md`",
        f"activation `Codex/results/PHASE_068_PLAN_ACTIVATION_RESULT.md`; current `{RESULT}`",
        f"activation evidence retained; current `{BUILDER}`, `{VALIDATOR}`, `{INVENTORY}`, `{ATTESTATION}`; exact-eight `A/A/A/A/A/M/M/M`, all `100644`",
        f"activation commit `{EXPECTED_PARENT}` pushed/live/clean with dual `PASS_P068_PLAN_ACTIVATION_PERSISTENCE`; Step 91 selected `{CONTENT_TERMINAL}`, marker `{PRECOMMIT_MARKER}`, expected parent `{EXPECTED_PARENT}`, subject `{EXPECTED_SUBJECT}`, containing commit `{PENDING_MARKER}`, reserved terminal `{PERSISTENCE_TERMINAL}`; commits/edges/path-counts/net/blobs/claims/pointers/negative controls `{summary_counts}`, register `{claim_range}`; U13 `UNDECIDED_ROUTE_STEP94`, scientific promotions 0",
        "dual Step 91 persistence, then Step 92",
    )
    marker_line = f"Current-state marker: `{PRECOMMIT_MARKER}`"
    require_exact_prefixed_line(parent, PARENT_LEDGER, "Current-state marker: ", marker_line)
    require_exact_markdown_row(parent, PARENT_LEDGER, "| 068 |", parent_cells)
    require_exact_prefixed_line(active, ACTIVE_LEDGER, "Current-state marker: ", marker_line)
    require_exact_markdown_row(active, ACTIVE_LEDGER, "| 068 |", active_cells)
    handover_20 = f"20. 현재 Phase 상태: Phase 067 Steps 82–90.2 complete and persisted at selected `CONDITIONAL_P067`; Phase 068 plan activation exact-seven commit `{EXPECTED_PARENT}` is pushed/live/clean with dual `PASS_P068_PLAN_ACTIVATION_PERSISTENCE`; Step 91 holds selected `{CONTENT_TERMINAL}` / `PASS_PENDING_PERSISTENCE` under `{PRECOMMIT_MARKER}`; Step 92 is blocked until dual Step 91 persistence"
    handover_21 = f"21. 현재 result: `{RESULT}`; activation result `Codex/results/PHASE_068_PLAN_ACTIVATION_RESULT.md` and plan `Codex/plans/2026-09-07-phase068-claude-codex-fork-adjudication-detailed-plan.md` retained as canonical history"
    handover_22 = f"22. 현재 machine evidence: `{BUILDER}`; `{VALIDATOR}`; JSON-last `{INVENTORY}`; JSON-last `{ATTESTATION}`; expected parent `{EXPECTED_PARENT}`; subject `{EXPECTED_SUBJECT}`; Gate `{CONTENT_TERMINAL}`; containing commit `{PENDING_MARKER}`; reserved terminal `{PERSISTENCE_TERMINAL}`; counts `2/2/2+1/net 3/6/{claim_range}/{pointer_count} pointers/{negative_count} named negatives`; U13 `UNDECIDED_ROUTE_STEP94`; scientific truth promotions: 0; Step 92 blocked until persistence"
    handover_recovery = f"- Step 91 recovery coverage is complete for frozen Claude topology: commits `2`, parent edges `2`, edge path events `2/1`, net paths `3`, and `6` unique before/after UTF-8 blobs read from byte 0 through EOF without gaps. Claim register `{claim_range}` has `{pointer_count}` exact claimant-surface pointers; {SUPPLEMENTAL_CLAIM_UNIT_COUNT} supplemental units map complete source ranges back to those claims; `{negative_count}` named negative controls are declared. U13 is a self-reported proposition under `UNDECIDED_ROUTE_STEP94`; no PDF/binary occurred, no source was modified, and scientific truth promotions: 0."
    require_exact_prefixed_line(handover, HANDOVER, "Current-state marker: ", marker_line)
    require_exact_prefixed_line(handover, HANDOVER, "20. 현재 Phase 상태:", handover_20)
    require_exact_prefixed_line(handover, HANDOVER, "21. 현재 result:", handover_21)
    require_exact_prefixed_line(handover, HANDOVER, "22. 현재 machine evidence:", handover_22)
    require_exact_prefixed_line(
        handover,
        HANDOVER,
        "- Step 91 recovery coverage is complete for frozen Claude topology:",
        handover_recovery,
    )
    handover_step_cells = (
        "Phase 068 Step 91",
        "Claude two-commit/two-edge/three-path full read",
        f"result `{RESULT}`; machine `{BUILDER}`, `{VALIDATOR}`, `{INVENTORY}`, `{ATTESTATION}`; selected `{CONTENT_TERMINAL}` / `PASS_PENDING_PERSISTENCE`; exact-eight `A/A/A/A/A/M/M/M`, all `100644`; marker `{PRECOMMIT_MARKER}`; expected parent `{EXPECTED_PARENT}`; subject `{EXPECTED_SUBJECT}`; containing commit `{PENDING_MARKER}`; reserved `{PERSISTENCE_TERMINAL}`; commits/edges/path-counts/net/blobs/claims/pointers/negative controls `{summary_counts}`, register `{claim_range}`; U13 `UNDECIDED_ROUTE_STEP94`; scientific promotions 0",
        "dual persistence, then Step 92",
    )
    require_exact_markdown_row(handover, HANDOVER, "| Phase 068 Step 91 |", handover_step_cells)
    exact_next_action = f"Keep `{BUILDER}`, `{VALIDATOR}`, `{RESULT}`, both ledgers and this handover frozen first. Generate `{INVENTORY}` and `{ATTESTATION}` last. Obtain Python 3.12/3.14 `{CONTENT_TERMINAL}`, deterministic bytes `2/2`, and independent P0/P1/P2=`0/0/0`; stage only exact-eight `A/A/A/A/A/M/M/M`, all modes `100644`, and obtain dual staged validation. Commit with subject `{EXPECTED_SUBJECT}` and parent `{EXPECTED_PARENT}`, push, verify local/upstream/tracking/live origin equality with protected/main/frozen tips unchanged and a clean tree, then require dual `{PERSISTENCE_TERMINAL}`. Execute Step 92 only after that terminal. Current marker is `{PRECOMMIT_MARKER}`, containing commit is `{PENDING_MARKER}`, activation terminal `PASS_P068_PLAN_ACTIVATION_PERSISTENCE` is fixed, U13 remains `UNDECIDED_ROUTE_STEP94`, and scientific truth promotions: 0."
    require_exact_section(
        handover,
        HANDOVER,
        "## Exact Next Action",
        exact_next_action,
        "## Hard-stop Reminder",
    )


def validate_human_controls() -> None:
    validate_human_control_texts(
        read_text_file(RESULT),
        read_text_file(PARENT_LEDGER),
        read_text_file(ACTIVE_LEDGER),
        read_text_file(HANDOVER),
    )


def status_entries() -> dict[str, str]:
    raw = git_bytes(["status", "--porcelain=v1", "-z", "--untracked-files=all"])
    fields = raw.split(b"\x00")
    if fields and fields[-1] == b"":
        fields.pop()
    out: dict[str, str] = {}
    for field in fields:
        if len(field) < 4:
            fail("E_STATUS_FORM", repr(field))
        xy = field[:2].decode("ascii", "strict")
        path = field[3:].decode("utf-8", "strict")
        if "R" in xy or "C" in xy:
            fail("E_STATUS_RENAME", f"{xy} {path}")
        if path in out:
            fail("E_STATUS_DUPLICATE", path)
        out[path] = xy
    return out


def validate_status(expected_paths: Iterable[str], phase: str, ignored_untracked: Iterable[str] = ()) -> None:
    expected_set = set(expected_paths)
    actual = status_entries()
    for ignored in ignored_untracked:
        if actual.pop(ignored, None) != "??":
            fail("E_STATUS_LOCK", ignored)
    if set(actual) != expected_set:
        fail("E_STATUS_PATH_SET", f"{phase}: expected={sorted(expected_set)!r}, actual={sorted(actual)!r}")
    for path in expected_paths:
        expected = EXPECTED_STATUS[path]
        xy = actual[path]
        if phase in {"pre_json", "content"}:
            wanted = "??" if expected == "A" else " M"
        elif phase == "staged":
            wanted = expected + " "
        else:
            fail("E_STATUS_PHASE", phase)
        if xy != wanted:
            fail("E_STATUS_CODE", f"{path}: {xy!r} != {wanted!r}")


def validate_local_boundary_refs(active_expected: str) -> None:
    if git_text(["branch", "--show-current"]) != ACTIVE_BRANCH:
        fail("E_BRANCH")
    if git_text(["rev-parse", "--abbrev-ref", "@{upstream}"]) != ACTIVE_UPSTREAM:
        fail("E_UPSTREAM_NAME")
    if git_text(["rev-parse", "HEAD"]) != active_expected:
        fail("E_HEAD", git_text(["rev-parse", "HEAD"]))
    if git_text(["rev-parse", "@{upstream}"]) != active_expected or git_text(["rev-parse", ACTIVE_REMOTE_REF]) != active_expected:
        fail("E_ACTIVE_TRACKING_REF")
    if git_text(["rev-parse", PROTECTED_LOCAL_REF]) != PROTECTED_TIP:
        fail("E_PROTECTED_LOCAL_REF")
    fixed_tracking = (
        (PROTECTED_REMOTE_REF, PROTECTED_TIP),
        (MAIN_REMOTE_REF, MAIN_TIP),
        (CLAUDE_REMOTE_REF, CLAUDE_TIP),
        (CODEX_FORK_REMOTE_REF, CODEX_FORK_TIP),
    )
    for ref, expected in fixed_tracking:
        if git_text(["rev-parse", ref]) != expected:
            fail("E_FIXED_TRACKING_REF", ref)
    optional_local = (
        (MAIN_LOCAL_REF, MAIN_TIP),
        (CLAUDE_LOCAL_REF, CLAUDE_TIP),
        (CODEX_FORK_LOCAL_REF, CODEX_FORK_TIP),
    )
    for ref, expected in optional_local:
        exists = git_returncode(["show-ref", "--verify", "--quiet", ref], (0, 1)) == 0
        if exists and git_text(["rev-parse", ref]) != expected:
            fail("E_OPTIONAL_LOCAL_REF", ref)
    if git_text(["remote", "get-url", "origin"]) != ORIGIN_URL:
        fail("E_ORIGIN")


def validate_live_boundary_refs(active_expected: str) -> None:
    fixed_live = (
        (ACTIVE_LIVE_REF, active_expected),
        (PROTECTED_LIVE_REF, PROTECTED_TIP),
        (MAIN_LIVE_REF, MAIN_TIP),
        (CLAUDE_LIVE_REF, CLAUDE_TIP),
        (CODEX_FORK_LIVE_REF, CODEX_FORK_TIP),
    )
    for ref, expected in fixed_live:
        if exact_live_ref(ref) != expected:
            fail("E_FIXED_LIVE_REF", ref)


def validate_current_branch_and_parent() -> None:
    validate_local_boundary_refs(EXPECTED_PARENT)
    parent, _ = parse_commit(EXPECTED_PARENT)
    if tuple(parent["parents"]) != (EXPECTED_PARENT_PARENT,) or parent["subject"] != EXPECTED_PARENT_SUBJECT:
        fail("E_PREDECESSOR_CERTIFICATE")
    validate_live_boundary_refs(EXPECTED_PARENT)


def validate_json_payloads(read_from_commit: str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    if read_from_commit is None:
        inventory_raw = (ROOT / INVENTORY).read_bytes() if (ROOT / INVENTORY).is_file() else fail("E_OUTPUT_MISSING", INVENTORY)
        attestation_raw = (ROOT / ATTESTATION).read_bytes() if (ROOT / ATTESTATION).is_file() else fail("E_OUTPUT_MISSING", ATTESTATION)
    else:
        inventory_raw = committed_path_bytes(read_from_commit, INVENTORY)
        attestation_raw = committed_path_bytes(read_from_commit, ATTESTATION)
    inventory = strict_load(inventory_raw)
    attestation = strict_load(attestation_raw)
    expected_inventory_raw, expected_attestation_raw = deterministic_payload_pair()
    expected_inventory = strict_load(expected_inventory_raw)
    expected_attestation = strict_load(expected_attestation_raw)
    if inventory != expected_inventory or inventory_raw != expected_inventory_raw:
        fail("E_INVENTORY_RECONSTRUCTION")
    if attestation != expected_attestation or attestation_raw != expected_attestation_raw:
        fail("E_ATTESTATION_RECONSTRUCTION")
    if attestation.get("inventory_sha256") != sha256(inventory_raw) or attestation.get("inventory_bytes") != len(inventory_raw):
        fail("E_JSON_CROSS_BINDING")
    if inventory.get("evidence_set_sha256") != attestation.get("evidence_set_sha256"):
        fail("E_EVIDENCE_BINDING")
    return inventory, attestation


def _dotted_name(node: ast.AST) -> str:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
    return ".".join(reversed(parts))


def source_seal_sha256(text: str, role: str) -> str:
    """Hash exact normalized source text; exclude only the validator seal values."""
    if role not in {"builder", "validator"}:
        fail("E_SOURCE_ROLE", role)
    normalized = text
    if role == "validator":
        lines = text.splitlines()
        starts = [index for index, line in enumerate(lines) if line == "EXPECTED_SOURCE_SEAL_SHA256 = {"]
        if len(starts) != 1:
            fail("E_SOURCE_SEAL_DECLARATION", f"validator:{len(starts)}")
        start = starts[0]
        ends = [index for index in range(start + 1, len(lines)) if lines[index] == "}"]
        if not ends:
            fail("E_SOURCE_SEAL_DECLARATION", "validator:unterminated")
        end = ends[0]
        lines[start : end + 1] = ["EXPECTED_SOURCE_SEAL_SHA256 = <NORMALIZED_SOURCE_SEAL>"]
        normalized = "\n".join(lines) + ("\n" if text.endswith(("\n", "\r")) else "")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def validate_source_seal(text: str, role: str) -> None:
    actual = source_seal_sha256(text, role)
    expected = EXPECTED_SOURCE_SEAL_SHA256.get(role)
    if actual != expected:
        fail("E_SOURCE_EXACT_SEAL", f"{role}:{actual}")


def validate_source_policy(text: str, role: str) -> None:
    """Statically reject dynamic execution, arbitrary I/O, and undeclared imports."""
    if role not in {"builder", "validator"}:
        fail("E_SOURCE_ROLE", role)
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        fail("E_SOURCE_PARSE", f"{role}:{exc.lineno}:{exc.msg}")
    allowed_plain_imports = {
        "builder": {("argparse", None), ("sys", None), ("validate_phase068_step91", "contract")},
        "validator": {
            ("argparse", None),
            ("ast", None),
            ("copy", None),
            ("hashlib", None),
            ("json", None),
            ("math", None),
            ("os", None),
            ("re", None),
            ("subprocess", None),
            ("sys", None),
            ("tempfile", None),
        },
    }[role]
    allowed_from_imports = {
        "builder": {("__future__", (("annotations", None),))},
        "validator": {
            ("__future__", (("annotations", None),)),
            ("pathlib", (("Path", None),)),
            ("typing", (("Any", None), ("Iterable", None))),
        },
    }[role]
    allowed_module_attributes = {
        "builder": {
            "argparse.ArgumentParser", "argparse.Namespace", "sys.argv", "sys.dont_write_bytecode", "sys.stderr",
            "contract.ATTESTATION", "contract.COLLECTOR_SCHEMA", "contract.EXACT_EIGHT", "contract.EXPECTED_PARENT",
            "contract.EXPECTED_STATUS", "contract.EXPECTED_STATUS.values", "contract.INVENTORY", "contract.ValidationError",
            "contract.build_payload_objects", "contract.canonical_bytes", "contract.collect_payloads",
            "contract.deterministic_payload_pair", "contract.fail", "contract.run_self_tests", "contract.sha256",
            "contract.strict_load", "contract.validate_pre_json",
        },
        "validator": {
            "argparse.ArgumentParser", "argparse.Namespace", "ast.AST", "ast.Assign", "ast.AsyncFunctionDef",
            "ast.Attribute", "ast.Call", "ast.ClassDef", "ast.Constant", "ast.ExceptHandler", "ast.FunctionDef",
            "ast.DictComp", "ast.GeneratorExp", "ast.Import", "ast.ImportFrom", "ast.Lambda", "ast.List",
            "ast.ListComp", "ast.Load", "ast.Name", "ast.SetComp", "ast.Starred", "ast.arg",
            "ast.iter_child_nodes", "ast.parse",
            "ast.walk", "copy.deepcopy", "hashlib.sha1", "hashlib.sha256", "json.dumps", "json.loads",
            "math.isfinite", "os.O_CREAT", "os.O_EXCL", "os.O_WRONLY", "os.close", "os.fdopen", "os.fsync",
            "os.getpid", "os.link", "os.open", "os.write", "re.compile", "subprocess.CompletedProcess",
            "subprocess.PIPE", "subprocess.run", "sys.argv", "sys.stderr", "tempfile.TemporaryDirectory",
            "tempfile.mkstemp",
        },
    }[role]
    module_roots = {item.split(".", 1)[0] for item in allowed_module_attributes}
    protected_bindings = module_roots | ({"Path", "Any", "Iterable"} if role == "validator" else set())
    forbidden_modules = {"builtins", "ctypes", "ftplib", "http", "importlib", "requests", "shutil", "socket", "ssl", "urllib"}
    forbidden_callable_names = {"eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr", "globals", "locals", "vars", "open", "input", "breakpoint"}
    sensitive_attributes = {
        "subprocess.run", "subprocess.Popen", "subprocess.call", "subprocess.check_call", "subprocess.check_output",
        "os.system", "os.popen", "os.spawnl", "os.spawnv", "os.execv", "os.execve", "os.open", "os.write",
        "os.link", "os.replace", "os.rename", "os.renames", "os.remove", "os.mkdir", "os.makedirs", "os.rmdir",
        "os.removedirs", "tempfile.mkstemp", "tempfile.TemporaryDirectory",
    }
    parents: dict[int, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[id(child)] = parent
    owners: dict[int, str] = {}
    for top in ast.walk(tree):
        if isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for node in ast.walk(top):
                owners[id(node)] = top.name
    dynamic_scope_ids: set[int] = set()
    for scope in ast.walk(tree):
        if isinstance(scope, (ast.Lambda, ast.GeneratorExp, ast.ListComp, ast.SetComp, ast.DictComp)):
            dynamic_scope_ids.update(id(node) for node in ast.walk(scope))
    privileged_call_owners = {
        "run_git": {"git_bytes", "git_returncode"},
        "_external_temp_collection": {"deterministic_payload_pair"},
        "_write_payload_temp": {"_external_temp_collection", "collect_payloads"},
        "_safe_unlink_payload": {"_external_temp_collection", "collect_payloads"},
        "collect_payloads": {"main"},
    }
    for node in ast.walk(tree):
        owner = owners.get(id(node), "<module>")
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in forbidden_modules or (alias.name, alias.asname) not in allowed_plain_imports:
                    fail("E_SOURCE_IMPORT", f"{role}:{alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            root = module.split(".", 1)[0]
            imported = tuple((alias.name, alias.asname) for alias in node.names)
            if root in forbidden_modules or (module, imported) not in allowed_from_imports:
                fail("E_SOURCE_IMPORT", f"{role}:{module}")
        elif isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load) and node.id in protected_bindings:
            fail("E_SOURCE_MODULE_REBIND", f"{role}:{owner}:{node.id}")
        elif isinstance(node, ast.arg) and node.arg in protected_bindings:
            fail("E_SOURCE_MODULE_REBIND", f"{role}:{owner}:{node.arg}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in protected_bindings:
            fail("E_SOURCE_MODULE_REBIND", f"{role}:{owner}:{node.name}")
        elif isinstance(node, ast.ExceptHandler) and node.name in protected_bindings:
            fail("E_SOURCE_MODULE_REBIND", f"{role}:{owner}:{node.name}")
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id in forbidden_callable_names or (node.id.startswith("__") and node.id not in {"__file__", "__name__"}):
                fail("E_SOURCE_DYNAMIC_NAME", f"{role}:{owner}:{node.id}")
            if node.id in privileged_call_owners:
                parent = parents.get(id(node))
                if not isinstance(parent, ast.Call) or parent.func is not node:
                    fail("E_SOURCE_PRIVILEGED_TRANSPORT", f"{role}:{owner}:{node.id}")
                if owner not in privileged_call_owners[node.id]:
                    fail("E_SOURCE_PRIVILEGED_CALL", f"{role}:{owner}:{node.id}")
                if id(node) in dynamic_scope_ids:
                    fail("E_SOURCE_DYNAMIC_SCOPE", f"{role}:{owner}:{node.id}")
            if node.id in module_roots:
                parent = parents.get(id(node))
                if not isinstance(parent, ast.Attribute) or parent.value is not node:
                    fail("E_SOURCE_CALLABLE_TRANSPORT", f"{role}:{owner}:{node.id}")
                dotted = _dotted_name(parent)
                if dotted not in allowed_module_attributes:
                    fail("E_SOURCE_MODULE_API", f"{role}:{owner}:{dotted}")
        elif isinstance(node, ast.Attribute):
            dotted = _dotted_name(node)
            frame_attribute = node.attr in {"gi_frame", "ag_frame", "cr_frame", "tb_frame"} or node.attr.startswith("f_")
            if (node.attr.startswith("_") and not (node.attr == "__init__" and owner == "__init__")) or frame_attribute:
                fail("E_SOURCE_DUNDER_LOOKUP", f"{role}:{owner}:{node.attr}")
            root = dotted.split(".", 1)[0]
            if root in module_roots and dotted not in allowed_module_attributes:
                fail("E_SOURCE_MODULE_API", f"{role}:{owner}:{dotted}")
            allowed_module_store = role == "builder" and dotted == "sys.dont_write_bytecode"
            if not isinstance(node.ctx, ast.Load) and root in module_roots and not allowed_module_store:
                fail("E_SOURCE_MODULE_REBIND", f"{role}:{owner}:{dotted}")
            parent = parents.get(id(node))
            direct_callee = isinstance(parent, ast.Call) and parent.func is node
            allowed_os_constant = owner == "collect_payloads" and dotted in {"os.O_CREAT", "os.O_EXCL", "os.O_WRONLY"}
            allowed_subprocess_value = dotted in {"subprocess.CompletedProcess", "subprocess.PIPE"}
            if (dotted.startswith("os.") or dotted.startswith("tempfile.")) and not direct_callee and not allowed_os_constant:
                fail("E_SOURCE_CALLABLE_TRANSPORT", f"{role}:{owner}:{dotted}")
            if dotted.startswith("subprocess.") and not direct_callee and not allowed_subprocess_value:
                fail("E_SOURCE_CALLABLE_TRANSPORT", f"{role}:{owner}:{dotted}")
            if dotted.startswith("sys.") and dotted not in {"sys.argv", "sys.dont_write_bytecode", "sys.stderr"}:
                fail("E_SOURCE_DYNAMIC_LOOKUP", f"{role}:{owner}:{dotted}")
            if dotted == "sys.modules":
                fail("E_SOURCE_DYNAMIC_LOOKUP", f"{role}:{owner}:{dotted}")
            if dotted in sensitive_attributes:
                if not direct_callee:
                    fail("E_SOURCE_CALLABLE_TRANSPORT", f"{role}:{owner}:{dotted}")
            if node.attr in {"open", "write", "writelines", "truncate", "flush", "write_bytes", "write_text", "unlink", "rename", "replace", "copy", "copy_into", "move", "move_into", "chmod", "lchmod", "mkdir", "rmdir", "touch", "symlink_to", "hardlink_to", "link_to"}:
                if not direct_callee:
                    fail("E_SOURCE_CALLABLE_TRANSPORT", f"{role}:{owner}:{dotted}")
        elif isinstance(node, ast.Call):
            dotted = _dotted_name(node.func)
            leaf = dotted.rsplit(".", 1)[-1]
            if id(node) in dynamic_scope_ids and (dotted.startswith(("os.", "subprocess.", "tempfile.")) or leaf in privileged_call_owners):
                fail("E_SOURCE_DYNAMIC_SCOPE", f"{role}:{owner}:{dotted}")
            if dotted in forbidden_callable_names:
                fail("E_SOURCE_DYNAMIC_CALL", f"{role}:{owner}:{dotted}")
            if leaf in {"write_bytes", "write_text", "rename", "copy", "copy_into", "move", "move_into", "chmod", "lchmod", "mkdir", "rmdir", "touch", "symlink_to", "hardlink_to", "link_to"}:
                fail("E_SOURCE_FILE_MUTATION", f"{role}:{owner}:{dotted}")
            if leaf == "open" and not (owner == "collect_payloads" and dotted == "os.open"):
                fail("E_SOURCE_FILE_MUTATION", f"{role}:{owner}:{dotted}")
            if leaf in {"writelines", "truncate"} and not dotted.startswith("os."):
                fail("E_SOURCE_FILE_MUTATION", f"{role}:{owner}:{dotted}")
            if leaf == "flush" and owner != "_write_payload_temp":
                fail("E_SOURCE_FILE_MUTATION", f"{role}:{owner}:{dotted}")
            if leaf == "replace":
                constant_args = tuple(arg.value for arg in node.args if isinstance(arg, ast.Constant))
                allowed_replace = (
                    not node.keywords
                    and len(node.args) == 2
                    and len(constant_args) == 2
                    and (
                        (owner == "lf_normalize" and constant_args in ((b"\r\n", b"\n"), (b"\r", b"\n")))
                        or (owner == "claim_pointer" and constant_args == ("\x00", "\\0"))
                    )
                )
                if not allowed_replace:
                    fail("E_SOURCE_FILE_MUTATION", f"{role}:{owner}:{dotted}")
            if dotted in {"os.replace", "os.rename", "os.renames", "os.remove", "os.mkdir", "os.makedirs", "os.rmdir", "os.removedirs"}:
                fail("E_SOURCE_FILE_MUTATION", f"{role}:{owner}:{dotted}")
            if leaf == "unlink" and owner not in {"_write_payload_temp", "_safe_unlink_payload", "collect_payloads"}:
                fail("E_SOURCE_FILE_MUTATION", f"{role}:{owner}:{dotted}")
            if leaf == "write" and not (owner == "_write_payload_temp" and dotted != "os.write") and not (owner == "collect_payloads" and dotted == "os.write"):
                fail("E_SOURCE_FILE_MUTATION", f"{role}:{owner}:{dotted}")
            if dotted.startswith("subprocess."):
                if role != "validator" or dotted != "subprocess.run" or owner != "run_git":
                    fail("E_SOURCE_PROCESS", f"{role}:{owner}:{dotted}")
                keywords = {keyword.arg: keyword.value for keyword in node.keywords if keyword.arg is not None}
                if set(keywords) != {"cwd", "check", "stdout", "stderr", "timeout", "shell"}:
                    fail("E_SOURCE_PROCESS_SHAPE", "keywords")
                if not isinstance(keywords["shell"], ast.Constant) or keywords["shell"].value is not False:
                    fail("E_SOURCE_PROCESS_SHELL")
                if len(node.args) != 1 or not isinstance(node.args[0], ast.List):
                    fail("E_SOURCE_PROCESS_SHAPE", "argv")
                argv_elts = node.args[0].elts
                if (
                    len(argv_elts) != 2
                    or not isinstance(argv_elts[0], ast.Constant)
                    or argv_elts[0].value != "git"
                    or not isinstance(argv_elts[1], ast.Starred)
                    or not isinstance(argv_elts[1].value, ast.Name)
                    or argv_elts[1].value.id != "args"
                ):
                    fail("E_SOURCE_PROCESS_SHAPE", "git argv")
            if dotted in {"os.system", "os.popen", "os.spawnl", "os.spawnv", "os.execv", "os.execve"}:
                fail("E_SOURCE_PROCESS", f"{role}:{owner}:{dotted}")
            allowed_os_calls = {
                "_write_payload_temp": {"os.fdopen", "os.fsync"},
                "collect_payloads": {"os.open", "os.write", "os.getpid", "os.fsync", "os.link", "os.close"},
            }
            if dotted.startswith("os.") and dotted not in allowed_os_calls.get(owner, set()):
                fail("E_SOURCE_OS_API", f"{role}:{owner}:{dotted}")
            allowed_tempfile_calls = {
                "_write_payload_temp": {"tempfile.mkstemp"},
                "_external_temp_collection": {"tempfile.TemporaryDirectory"},
            }
            if dotted.startswith("tempfile.") and dotted not in allowed_tempfile_calls.get(owner, set()):
                fail("E_SOURCE_TEMP_API", f"{role}:{owner}:{dotted}")
    if role == "builder":
        if any(_dotted_name(node.func).startswith(("subprocess.", "os.", "tempfile.")) for node in ast.walk(tree) if isinstance(node, ast.Call)):
            fail("E_BUILDER_PROCESS_OR_IO")
        privileged_names = {"run_git", "_external_temp_collection", "_write_payload_temp", "_safe_unlink_payload", "collect_payloads"}
        if any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in privileged_names for node in ast.walk(tree)):
            fail("E_SOURCE_PRIVILEGED_DEF_CARDINALITY", "builder")
    else:
        privileged_names = ("run_git", "_external_temp_collection", "_write_payload_temp", "_safe_unlink_payload", "collect_payloads")
        privileged_defs: dict[str, ast.FunctionDef] = {}
        for name in privileged_names:
            matches = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
            if len(matches) != 1:
                fail("E_SOURCE_PRIVILEGED_DEF_CARDINALITY", f"{name}:{len(matches)}")
            if not isinstance(matches[0], ast.FunctionDef) or matches[0] not in tree.body:
                fail("E_SOURCE_PRIVILEGED_DEF_SCOPE", name)
            privileged_defs[name] = matches[0]
        calls = [_dotted_name(node.func) for node in ast.walk(privileged_defs["run_git"]) if isinstance(node, ast.Call)]
        if not calls or calls[0] != "validate_git_argv" or calls.count("subprocess.run") != 1:
            fail("E_SOURCE_RUN_GIT_GATE", repr(calls))
    marker = "WRITER_SCHEMA" if role == "builder" else "EXPECTED_SOURCE_SEAL_SHA256"
    full_source = any(
        isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == marker for target in node.targets)
        for node in tree.body
    )
    if full_source:
        actual_plain_imports = [
            (alias.name, alias.asname)
            for node in tree.body
            if isinstance(node, ast.Import)
            for alias in node.names
        ]
        actual_from_imports = [
            (node.module or "", tuple((alias.name, alias.asname) for alias in node.names))
            for node in tree.body
            if isinstance(node, ast.ImportFrom)
        ]
        actual_module_attributes = {
            _dotted_name(node)
            for node in ast.walk(tree)
            if isinstance(node, ast.Attribute) and _dotted_name(node).split(".", 1)[0] in module_roots
        }
        if len(actual_plain_imports) != len(allowed_plain_imports) or set(actual_plain_imports) != allowed_plain_imports:
            fail("E_SOURCE_IMPORT_INVENTORY", role)
        if len(actual_from_imports) != len(allowed_from_imports) or set(actual_from_imports) != allowed_from_imports:
            fail("E_SOURCE_IMPORT_INVENTORY", role)
        if actual_module_attributes != allowed_module_attributes:
            fail("E_SOURCE_MODULE_API_INVENTORY", f"{role}:{sorted(actual_module_attributes ^ allowed_module_attributes)!r}")
        validate_source_seal(text, role)


def validate_source_guard() -> None:
    builder_text = read_text_file(BUILDER)
    validator_text = read_text_file(VALIDATOR)
    validate_source_policy(builder_text, "builder")
    validate_source_policy(validator_text, "validator")
    validate_source_seal(builder_text, "builder")
    validate_source_seal(validator_text, "validator")


def collect_lock_allowlist(lock_held: bool) -> tuple[str, ...]:
    """Permit only the live builder's own lock during its in-lock checks."""
    return (COLLECT_LOCK,) if lock_held else ()


def validate_content(lock_held: bool = False) -> None:
    # Output absence is deliberately the first RED gate used before implementation.
    for path in EXACT_EIGHT:
        if not (ROOT / path).is_file():
            fail("E_OUTPUT_MISSING", path)
    validate_current_branch_and_parent()
    validate_status(EXACT_EIGHT, "content", collect_lock_allowlist(lock_held))
    validate_source_guard()
    validate_human_controls()
    validate_json_payloads()


def validate_pre_json(lock_held: bool = False) -> None:
    for path in PRE_JSON_SIX:
        if not (ROOT / path).is_file():
            fail("E_INPUT_MISSING", path)
    for path in (INVENTORY, ATTESTATION):
        if (ROOT / path).exists():
            fail("E_REFUSE_OVERWRITE", path)
    validate_current_branch_and_parent()
    validate_status(PRE_JSON_SIX, "pre_json", collect_lock_allowlist(lock_held))
    validate_source_guard()
    validate_human_controls()


def _external_temp_collection() -> tuple[bytes, bytes]:
    """Build, serialize, fsync, and reread one pair outside the repository."""
    objects = build_payload_objects()
    raws = tuple(canonical_bytes(item) for item in objects)
    with tempfile.TemporaryDirectory(prefix="p068-step91-") as directory:
        external_root = Path(directory).resolve()
        try:
            external_root.relative_to(ROOT.resolve())
        except ValueError:
            pass
        else:
            fail("E_EXTERNAL_TEMP_INSIDE_REPOSITORY", str(external_root))
        inventory_temp = _write_payload_temp(external_root / "inventory.json", raws[0])
        attestation_temp = _write_payload_temp(external_root / "attestation.json", raws[1])
        reread = (inventory_temp.read_bytes(), attestation_temp.read_bytes())
        _safe_unlink_payload(inventory_temp, raws[0])
        _safe_unlink_payload(attestation_temp, raws[1])
    if reread != raws:
        fail("E_EXTERNAL_TEMP_REREAD")
    if strict_load(reread[0]) != objects[0] or strict_load(reread[1]) != objects[1]:
        fail("E_PAYLOAD_ROUNDTRIP")
    if objects[1]["inventory_sha256"] != sha256(reread[0]):
        fail("E_PAYLOAD_CROSS_BINDING")
    return reread


def deterministic_payload_pair() -> tuple[bytes, bytes]:
    first = _external_temp_collection()
    second = _external_temp_collection()
    if first != second:
        fail("E_PAYLOAD_NONDETERMINISTIC")
    if strict_load(first[0]) != strict_load(second[0]) or strict_load(first[1]) != strict_load(second[1]):
        fail("E_PAYLOAD_SEMANTIC_NONDETERMINISM")
    return first[0], first[1]


def _write_payload_temp(destination: Path, raw: bytes) -> Path:
    descriptor, name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temp = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        if temp.read_bytes() != raw:
            fail("E_COLLECT_TEMP_VERIFY", destination.as_posix())
        return temp
    except BaseException:
        temp.unlink(missing_ok=True)
        raise


def _safe_unlink_payload(path: Path, expected_raw: bytes) -> None:
    if path.is_file() and path.read_bytes() == expected_raw:
        path.unlink()


def collect_payloads() -> tuple[bytes, bytes]:
    """Atomically publish the exact JSON pair after result/control freeze."""
    lock = ROOT / COLLECT_LOCK
    inventory_path = ROOT / INVENTORY
    attestation_path = ROOT / ATTESTATION
    descriptor: int | None = None
    inventory_temp: Path | None = None
    attestation_temp: Path | None = None
    inventory_raw = b""
    attestation_raw = b""
    inventory_published = False
    attestation_published = False
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.write(descriptor, f"pid={os.getpid()} schema={COLLECTOR_SCHEMA}\n".encode("ascii"))
        os.fsync(descriptor)
        validate_pre_json(lock_held=True)
        inventory_raw, attestation_raw = deterministic_payload_pair()
        validate_pre_json(lock_held=True)
        inventory_temp = _write_payload_temp(inventory_path, inventory_raw)
        attestation_temp = _write_payload_temp(attestation_path, attestation_raw)
        try:
            os.link(inventory_temp, inventory_path)
        except FileExistsError:
            fail("E_REFUSE_OVERWRITE_RACE", INVENTORY)
        except OSError as exc:
            fail("E_ATOMIC_LINK", f"{INVENTORY}: {exc}")
        inventory_published = True
        inventory_temp.unlink()
        inventory_temp = None
        try:
            os.link(attestation_temp, attestation_path)
        except FileExistsError:
            fail("E_REFUSE_OVERWRITE_RACE", ATTESTATION)
        except OSError as exc:
            fail("E_ATOMIC_LINK", f"{ATTESTATION}: {exc}")
        attestation_published = True
        attestation_temp.unlink()
        attestation_temp = None
        validate_content(lock_held=True)
        return inventory_raw, attestation_raw
    except FileExistsError:
        fail("E_COLLECT_LOCKED", COLLECT_LOCK)
    except BaseException:
        if attestation_published:
            _safe_unlink_payload(attestation_path, attestation_raw)
        if inventory_published:
            _safe_unlink_payload(inventory_path, inventory_raw)
        raise
    finally:
        if inventory_temp is not None:
            inventory_temp.unlink(missing_ok=True)
        if attestation_temp is not None:
            attestation_temp.unlink(missing_ok=True)
        if descriptor is not None:
            os.close(descriptor)
            lock.unlink(missing_ok=True)


def validate_staged() -> None:
    validate_content_files_present()
    validate_current_branch_and_parent()
    validate_status(EXACT_EIGHT, "staged")
    if git_returncode(["diff", "--quiet"], (0, 1)) != 0:
        fail("E_UNSTAGED_DIFF")
    raw = git_bytes(["diff", "--cached", "--raw", "-z", "--abbrev=40", EXPECTED_PARENT])
    records = parse_index_raw_diff(raw)
    if [item["path"] for item in records] != list(GIT_ORDERED_EIGHT):
        fail("E_STAGED_PATH_ORDER", repr([item["path"] for item in records]))
    for item in records:
        path = item["path"]
        expected = (EXPECTED_STATUS[path], EXPECTED_OLD_MODES[path], EXPECTED_MODES[path])
        actual = (item["status"], item["old_mode"], item["new_mode"])
        if actual != expected:
            fail("E_STAGED_MODE_STATUS", f"{path}: {actual!r} != {expected!r}")
    name_status = parse_name_status(git_bytes(["diff", "--cached", "--name-status", "-z", EXPECTED_PARENT, "--"]))
    expected_name_status = [(EXPECTED_STATUS[path], path) for path in GIT_ORDERED_EIGHT]
    if name_status != expected_name_status:
        fail("E_STAGED_NAME_STATUS_ORDER", repr(name_status))
    stage_records = parse_ls_files_stage(git_bytes(["ls-files", "--stage", "-z", "--", *EXACT_EIGHT]))
    if [item["path"] for item in stage_records] != list(GIT_ORDERED_EIGHT):
        fail("E_STAGE_PATH_ORDER", repr([item["path"] for item in stage_records]))
    raw_by_path = {item["path"]: item for item in records}
    for item in stage_records:
        path = item["path"]
        worktree = (ROOT / path).read_bytes()
        worktree_blob = hashlib.sha1(b"blob " + str(len(worktree)).encode("ascii") + b"\x00" + worktree).hexdigest()
        if item["mode"] != "100644" or item["stage"] != "0":
            fail("E_STAGE_MODE_NUMBER", f"{path}: {item!r}")
        if item["blob"] != raw_by_path[path]["new_blob"] or item["blob"] != worktree_blob:
            fail("E_STAGE_BLOB_BINDING", path)
    validate_source_guard()
    validate_human_controls()
    validate_json_payloads()


def validate_content_files_present() -> None:
    for path in EXACT_EIGHT:
        if not (ROOT / path).is_file():
            fail("E_OUTPUT_MISSING", path)


def parse_index_raw_diff(raw: bytes) -> list[dict[str, str]]:
    chunks = raw.split(b"\x00")
    if chunks and chunks[-1] == b"":
        chunks.pop()
    if len(chunks) % 2:
        fail("E_INDEX_DIFF_FORM")
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for i in range(0, len(chunks), 2):
        meta = chunks[i].decode("ascii", "strict").split(" ")
        path = chunks[i + 1].decode("utf-8", "strict")
        if len(meta) != 5 or not meta[0].startswith(":"):
            fail("E_INDEX_META")
        if path in seen:
            fail("E_INDEX_DUPLICATE", path)
        seen.add(path)
        out.append(
            {
                "path": path,
                "status": meta[4],
                "old_mode": meta[0][1:],
                "new_mode": meta[1],
                "old_blob": meta[2],
                "new_blob": meta[3],
            }
        )
    return out


def parse_name_status(raw: bytes) -> list[tuple[str, str]]:
    chunks = raw.split(b"\x00")
    if chunks and chunks[-1] == b"":
        chunks.pop()
    if len(chunks) % 2:
        fail("E_NAME_STATUS_FORM")
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for index in range(0, len(chunks), 2):
        status = chunks[index].decode("ascii", "strict")
        path = chunks[index + 1].decode("utf-8", "strict")
        if status not in {"A", "M"}:
            fail("E_NAME_STATUS_CODE", f"{status}:{path}")
        if path in seen:
            fail("E_NAME_STATUS_DUPLICATE", path)
        seen.add(path)
        out.append((status, path))
    return out


def parse_ls_files_stage(raw: bytes) -> list[dict[str, str]]:
    chunks = raw.split(b"\x00")
    if chunks and chunks[-1] == b"":
        chunks.pop()
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for chunk in chunks:
        meta_raw, separator, path_raw = chunk.partition(b"\t")
        if separator != b"\t":
            fail("E_STAGE_FORM")
        meta = meta_raw.decode("ascii", "strict").split(" ")
        path = path_raw.decode("utf-8", "strict")
        if len(meta) != 3 or meta[0] != "100644" or not HEX40.fullmatch(meta[1]) or meta[2] != "0":
            fail("E_STAGE_META", meta_raw.decode("ascii", "replace"))
        if path in seen:
            fail("E_STAGE_DUPLICATE", path)
        seen.add(path)
        out.append({"mode": meta[0], "blob": meta[1], "stage": meta[2], "path": path})
    return out


def committed_path_bytes(commit: str, path: str) -> bytes:
    if not HEX40.fullmatch(commit) or path not in EXACT_EIGHT:
        fail("E_COMMITTED_PATH_ARG", f"{commit}:{path}")
    raw = git_bytes(["ls-tree", "-z", commit, "--", path], authorized_oids=(commit,))
    if not raw.endswith(b"\x00"):
        fail("E_LS_TREE", path)
    meta, listed = raw[:-1].split(b"\t", 1)
    if listed.decode("utf-8", "strict") != path:
        fail("E_LS_TREE_PATH", path)
    parts = meta.decode("ascii", "strict").split(" ")
    if len(parts) != 3 or parts[0] != "100644" or parts[1] != "blob" or not HEX40.fullmatch(parts[2]):
        fail("E_LS_TREE_META", meta.decode("ascii", "replace"))
    return git_bytes(["cat-file", "blob", parts[2]], authorized_oids=(parts[2],))


def exact_live_ref(ref: str) -> str:
    if ref not in {
        ACTIVE_LIVE_REF,
        PROTECTED_LIVE_REF,
        MAIN_LIVE_REF,
        CLAUDE_LIVE_REF,
        CODEX_FORK_LIVE_REF,
    }:
        fail("E_LIVE_REF_ALLOWLIST", ref)
    raw = git_bytes(["ls-remote", "--exit-code", "origin", ref])
    lines = raw.decode("ascii", "strict").splitlines()
    if len(lines) != 1:
        fail("E_LIVE_REF_COUNT", f"{ref}: {len(lines)}")
    fields = lines[0].split("\t")
    if len(fields) != 2 or fields[1] != ref or not HEX40.fullmatch(fields[0]):
        fail("E_LIVE_REF_FORM", lines[0])
    return fields[0]


def validate_persistence(expected_commit: str) -> None:
    if not HEX40.fullmatch(expected_commit):
        fail("E_EXPECTED_COMMIT_FORM", expected_commit)
    ensure_object(expected_commit, "commit", authorized_oids=(expected_commit,))
    validate_local_boundary_refs(expected_commit)
    if status_entries():
        fail("E_PERSISTENCE_DIRTY", repr(status_entries()))
    record, _ = parse_commit(expected_commit, authorized_oids=(expected_commit,))
    if tuple(record["parents"]) != (EXPECTED_PARENT,) or record["subject"] != EXPECTED_SUBJECT:
        fail("E_PERSISTENCE_COMMIT")
    records, _ = parse_raw_diff(
        EXPECTED_PARENT,
        expected_commit,
        ("A", "M"),
        authorized_pairs=((EXPECTED_PARENT, expected_commit),),
    )
    if [item["path"] for item in records] != list(GIT_ORDERED_EIGHT):
        fail("E_PERSISTENCE_PATH_ORDER", repr([item["path"] for item in records]))
    for item in records:
        path = item["path"]
        if (
            item["status"] != EXPECTED_STATUS[path]
            or item["old_mode"] != EXPECTED_OLD_MODES[path]
            or item["new_mode"] != EXPECTED_MODES[path]
        ):
            fail("E_PERSISTENCE_STATUS_MODE", item["path"])
    name_status = parse_name_status(
        git_bytes(
            ["diff", "--name-status", "-z", EXPECTED_PARENT, expected_commit, "--"],
            authorized_pairs=((EXPECTED_PARENT, expected_commit),),
        )
    )
    expected_name_status = [(EXPECTED_STATUS[path], path) for path in GIT_ORDERED_EIGHT]
    if name_status != expected_name_status:
        fail("E_PERSISTENCE_NAME_STATUS_ORDER", repr(name_status))
    # Compare committed control bytes with clean worktree before reconstruction.
    for path in EXACT_EIGHT:
        if committed_path_bytes(expected_commit, path) != (ROOT / path).read_bytes():
            fail("E_PERSISTENCE_WORKTREE_BINDING", path)
    validate_source_guard()
    validate_human_controls()
    inventory, _ = validate_json_payloads(expected_commit)
    result = committed_path_bytes(expected_commit, RESULT).decode("utf-8", "strict")
    if next((line.strip() for line in reversed(result.splitlines()) if line.strip()), "") != CONTENT_TERMINAL:
        fail("E_COMMITTED_RESULT_TERMINAL")
    if inventory.get("content_terminal") != CONTENT_TERMINAL:
        fail("E_COMMITTED_JSON_TERMINAL")
    # Network is last and is restricted to the five fixed refs after local preauthorization.
    validate_live_boundary_refs(expected_commit)


def _strict_failure(raw: bytes, expected_code: str) -> None:
    try:
        strict_load(raw)
    except ValidationError as exc:
        if exc.code != expected_code:
            fail("E_SELFTEST_CODE", f"{exc.code} != {expected_code}")
    else:
        fail("E_SELFTEST_ACCEPTED", expected_code)


def _source_policy_failure(source: str, role: str, expected_code: str, case_id: str) -> None:
    try:
        validate_source_policy(source, role)
    except ValidationError as exc:
        if exc.code != expected_code:
            fail("E_SELFTEST_SOURCE_POLICY_CODE", f"{case_id}: {exc.code} != {expected_code}")
    else:
        fail("E_SELFTEST_SOURCE_POLICY_ACCEPTED", f"{case_id}: {expected_code}")


def _human_failure(texts: tuple[str, str, str, str], expected_code: str, case_id: str) -> None:
    try:
        validate_human_control_texts(*texts)
    except ValidationError as exc:
        if exc.code != expected_code:
            fail("E_SELFTEST_HUMAN_CODE", f"{case_id}: {exc.code} != {expected_code}")
    else:
        fail("E_SELFTEST_HUMAN_ACCEPTED", f"{case_id}: {expected_code}")


def _contract_failure(inventory: dict[str, Any], attestation: dict[str, Any], expected_code: str, case_id: str) -> None:
    try:
        validate_payload_contract(inventory, attestation)
    except ValidationError as exc:
        if exc.code != expected_code:
            fail("E_SELFTEST_CONTRACT_CODE", f"{case_id}: {exc.code} != {expected_code}")
    else:
        fail("E_SELFTEST_CONTRACT_ACCEPTED", f"{case_id}: {expected_code}")


def _parser_failure(parser: Any, raw: bytes, expected_code: str, case_id: str) -> None:
    try:
        parser(raw)
    except ValidationError as exc:
        if exc.code != expected_code:
            fail("E_SELFTEST_PARSER_CODE", f"{case_id}: {exc.code} != {expected_code}")
    else:
        fail("E_SELFTEST_PARSER_ACCEPTED", f"{case_id}: {expected_code}")


def run_self_tests() -> int:
    tests = 0
    executed_negative_ids: list[str] = []
    sample: dict[str, Any] = {"schema": "T", "value": [1, "한글", True, None]}
    sample["semantic_sha256"] = semantic_sha(sample)
    raw = canonical_bytes(sample)
    if strict_load(raw) != sample:
        fail("E_SELFTEST_BASELINE")
    tests += 1
    cases = (
        ("N91-J01", b'{"a":1,"a":2}\n', "E_JSON_DUPLICATE_KEY"),
        ("N91-J02", b'{"x":NaN}\n', "E_JSON_NONFINITE"),
        ("N91-J03", b'{"x":Infinity}\n', "E_JSON_NONFINITE"),
        ("N91-J04", b'\xef\xbb\xbf{}\n', "E_JSON_BOM"),
        ("N91-J05", b'{}', "E_JSON_PHYSICAL_FORM"),
        ("N91-J06", b'{}\r\n', "E_JSON_PHYSICAL_FORM"),
        ("N91-J07", b'{}\n\n', "E_JSON_PHYSICAL_FORM"),
        ("N91-J08", b'[]\n', "E_JSON_ROOT"),
        ("N91-J09", b'{broken}\n', "E_JSON_PARSE"),
        ("N91-J10", b'{"semantic_sha256":"0"}\n', "E_JSON_SEMANTIC_SHA"),
        ("N91-J11", b'{"b":1,"a":2}\n', "E_JSON_NONCANONICAL"),
    )
    for case_id, bad, code in cases:
        _strict_failure(bad, code)
        executed_negative_ids.append(case_id)
        tests += 1
    deep: Any = 0
    for _ in range(MAX_JSON_DEPTH + 2):
        deep = [deep]
    deep_obj = {"x": deep}
    deep_obj["semantic_sha256"] = semantic_sha(deep_obj)
    _strict_failure(canonical_bytes(deep_obj), "E_JSON_DEPTH")
    executed_negative_ids.append("N91-J12")
    tests += 1
    # In-memory mutation REDs for canonical/semantic/cross-contract primitives.
    mutated = raw[:1] + b" " + raw[1:]
    _strict_failure(mutated, "E_JSON_NONCANONICAL")
    tests += 1
    if sha256(b"a") == sha256(b"b"):
        fail("E_SELFTEST_HASH")
    tests += 1
    if physical_line_count(b"a\n") != 1 or physical_line_count(b"a") != 1 or physical_line_count(b"") != 0:
        fail("E_SELFTEST_LINES")
    tests += 1
    if lf_normalize(b"a\r\nb\rc\n") != b"a\nb\nc\n":
        fail("E_SELFTEST_LF")
    tests += 1
    if not HEX40.fullmatch("a" * 40) or HEX40.fullmatch("-" + "a" * 39):
        fail("E_SELFTEST_OID")
    tests += 1
    if len(CLAIM_DEFS) != CLAIM_COUNT or len(SUPPLEMENTAL_CLAIM_UNITS) != SUPPLEMENTAL_CLAIM_UNIT_COUNT:
        fail("E_SELFTEST_CLAIMS")
    tests += 1
    if [x["id"] for x in CLAIM_DEFS] != [f"C91-{i:02d}" for i in range(1, CLAIM_COUNT + 1)]:
        fail("E_SELFTEST_CLAIM_IDS")
    tests += 1
    if len(EXACT_EIGHT) != 8 or list(EXPECTED_STATUS.values()) != ["A", "A", "A", "A", "A", "M", "M", "M"]:
        fail("E_SELFTEST_OUTPUTS")
    tests += 1
    if set(x["severity"] for x in KNOWN_FINDINGS) != {"P1", "P2"}:
        fail("E_SELFTEST_FINDINGS")
    tests += 1
    if collect_lock_allowlist(False) != () or collect_lock_allowlist(True) != (COLLECT_LOCK,):
        fail("E_SELFTEST_COLLECT_LOCK_ALLOWLIST")
    tests += 1
    allowed_git_shapes = (
        ["status", "--porcelain=v1", "-z", "--untracked-files=all"],
        ["cat-file", "-t", EXPECTED_PARENT],
        ["cat-file", "commit", EXPECTED_PARENT],
        ["cat-file", "blob", ARCHIVE_NEW],
        ["diff-tree", "--no-commit-id", "--raw", "-z", "-r", BASE, CLAUDE_COMMITS[0]],
        ["diff", "--cached", "--raw", "-z", "--abbrev=40", EXPECTED_PARENT],
        ["diff", "--cached", "--name-status", "-z", EXPECTED_PARENT, "--"],
        ["ls-files", "--stage", "-z", "--", *EXACT_EIGHT],
        ["ls-remote", "--exit-code", "origin", ACTIVE_LIVE_REF],
    )
    for argv in allowed_git_shapes:
        validate_git_argv(argv)
    tests += 1
    rejected_git_shapes = (
        ("N91-G01", ["status"]),
        ("N91-G02", ["cat-file", "blob", "-" + "a" * 39]),
        ("N91-G03", ["diff-tree", "--output=escape", "a" * 40]),
        ("N91-G04", ["ls-remote", "--exit-code", "origin", "refs/heads/not-allowlisted"]),
        ("N91-G05", ["checkout", MAIN_LIVE_REF]),
        ("N91-G06", ["ls-files", "--stage", "-z", "--", *EXACT_EIGHT[:-1], "undeclared"]),
        ("N91-G07", ["cat-file", "blob", "a" * 40]),
        ("N91-G08", ["diff-tree", "--no-commit-id", "--raw", "-z", "-r", "a" * 40, "b" * 40]),
        ("N91-G09", ["diff", "--name-status", "-z", "a" * 40, "b" * 40, "--"]),
        ("N91-G10", ["ls-tree", "-z", "a" * 40, "--", EXACT_EIGHT[0]]),
        ("N91-G11", ["diff", "--cached", "--raw", "-z", EXPECTED_PARENT]),
    )
    for case_id, argv in rejected_git_shapes:
        try:
            validate_git_argv(argv)
        except ValidationError as exc:
            if exc.code not in {"E_GIT_ARGV_SHAPE", "E_GIT_SUBCOMMAND"}:
                fail("E_SELFTEST_GIT_REJECT_CODE", exc.code)
        else:
            fail("E_SELFTEST_GIT_ACCEPTED", repr(argv))
        executed_negative_ids.append(case_id)
    tests += 1
    class ForgedStr(str):
        def __eq__(self, other: object) -> bool:
            disguises = {
                "-c": "diff",
                "alias.x=!echo blocked": "--cached",
                "x": "--raw",
                "ignored": "-z",
                "ignored2": EXPECTED_PARENT,
            }
            return disguises.get(str(self), str(self)) == other

    forged_argv = [
        ForgedStr("-c"),
        ForgedStr("alias.x=!echo blocked"),
        ForgedStr("x"),
        ForgedStr("ignored"),
        ForgedStr("ignored2"),
    ]
    try:
        validate_git_argv(forged_argv)
    except ValidationError as exc:
        if exc.code != "E_GIT_ARG":
            fail("E_SELFTEST_GIT_REJECT_CODE", f"N91-G12:{exc.code}")
    else:
        fail("E_SELFTEST_GIT_ACCEPTED", "N91-G12")
    executed_negative_ids.append("N91-G12")
    tests += 1
    try:
        validate_git_argv(["cat-file", "blob", ARCHIVE_NEW], authorized_oids=[])
    except ValidationError as exc:
        if exc.code != "E_GIT_AUTHORIZATION":
            fail("E_SELFTEST_GIT_REJECT_CODE", f"N91-G13:{exc.code}")
    else:
        fail("E_SELFTEST_GIT_ACCEPTED", "N91-G13")
    executed_negative_ids.append("N91-G13")
    tests += 1
    duplicate_path = EXACT_EIGHT[0].encode("utf-8")
    index_record = b":000000 100644 " + b"0" * 40 + b" " + b"1" * 40 + b" A\x00" + duplicate_path + b"\x00"
    name_record = b"A\x00" + duplicate_path + b"\x00"
    stage_record = b"100644 " + b"1" * 40 + b" 0\t" + duplicate_path + b"\x00"
    parser_cases = (
        ("N91-G14", parse_index_raw_diff, index_record + index_record, "E_INDEX_DUPLICATE"),
        ("N91-G15", parse_name_status, name_record + name_record, "E_NAME_STATUS_DUPLICATE"),
        ("N91-G16", parse_ls_files_stage, stage_record + stage_record, "E_STAGE_DUPLICATE"),
    )
    for case_id, parser, bad, code in parser_cases:
        _parser_failure(parser, bad, code, case_id)
        executed_negative_ids.append(case_id)
        tests += 1
    source_policy_cases = (
        ("N91-S01", "import subprocess as sp\nsp.run(['git','status'])\n", "validator", "E_SOURCE_IMPORT"),
        ("N91-S02", "from subprocess import Popen as p\np([])\n", "validator", "E_SOURCE_IMPORT"),
        ("N91-S03", "import subprocess\nrunner = subprocess.run\nrunner([])\n", "validator", "E_SOURCE_CALLABLE_TRANSPORT"),
        ("N91-S04", "loader = __import__\nloader('os')\n", "validator", "E_SOURCE_DYNAMIC_NAME"),
        ("N91-S05", "import os\ndef f():\n    os.system('x')\n", "validator", "E_SOURCE_PROCESS"),
        ("N91-S06", "from pathlib import Path\nPath('x').write_text('y')\n", "validator", "E_SOURCE_FILE_MUTATION"),
        ("N91-S07", "from pathlib import Path\nPath('x').unlink()\n", "validator", "E_SOURCE_FILE_MUTATION"),
        ("N91-S08", "import subprocess\ndef f(args):\n    subprocess.run(['git', *args])\n", "validator", "E_SOURCE_PROCESS"),
        ("N91-S09", "import socket\n", "validator", "E_SOURCE_IMPORT"),
        ("N91-S10", "x = object().__dict__\n", "validator", "E_SOURCE_DUNDER_LOOKUP"),
        ("N91-S11", "open('x')\n", "validator", "E_SOURCE_DYNAMIC_CALL"),
    )
    for case_id, source, role, code in source_policy_cases:
        _source_policy_failure(source, role, code, case_id)
        executed_negative_ids.append(case_id)
        tests += 1
    shell_escape = """import subprocess\ndef run_git(args):\n    validate_git_argv(args)\n    return subprocess.run([\"git\", *args], cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300, shell=True)\n"""
    _source_policy_failure(shell_escape, "validator", "E_SOURCE_PROCESS_SHELL", "N91-S12")
    executed_negative_ids.append("N91-S12")
    tests += 1
    _source_policy_failure("from pathlib import Path\nwriter = Path.write_text\nwriter(None, 'x')\n", "validator", "E_SOURCE_CALLABLE_TRANSPORT", "N91-S13")
    executed_negative_ids.append("N91-S13")
    tests += 1
    additional_source_policy_cases = (
        ("N91-S14", "Path('x').replace('y')\n", "E_SOURCE_FILE_MUTATION"),
        ("N91-S15", "Path('x').chmod(0o777)\n", "E_SOURCE_FILE_MUTATION"),
        ("N91-S16", "Path('x').link_to('y')\n", "E_SOURCE_FILE_MUTATION"),
        ("N91-S17", "Path('x').lchmod(0o777)\n", "E_SOURCE_FILE_MUTATION"),
        ("N91-S18", "move = Path.replace\n", "E_SOURCE_CALLABLE_TRANSPORT"),
        ("N91-S19", "def run_git():\n    pass\ndef run_git():\n    pass\n", "E_SOURCE_PRIVILEGED_DEF_CARDINALITY"),
        (
            "N91-S20",
            "def run_git():\n    pass\ndef _external_temp_collection():\n    pass\ndef _write_payload_temp():\n    pass\ndef _safe_unlink_payload():\n    pass\ndef _safe_unlink_payload():\n    pass\ndef collect_payloads():\n    pass\n",
            "E_SOURCE_PRIVILEGED_DEF_CARDINALITY",
        ),
        (
            "N91-S21",
            "def run_git():\n    pass\ndef _external_temp_collection():\n    pass\ndef _write_payload_temp():\n    pass\ndef _safe_unlink_payload():\n    pass\ndef outer():\n    def collect_payloads():\n        pass\n",
            "E_SOURCE_PRIVILEGED_DEF_SCOPE",
        ),
        (
            "N91-S22",
            "def run_git():\n    pass\ndef _external_temp_collection():\n    pass\nasync def _write_payload_temp():\n    pass\ndef _safe_unlink_payload():\n    pass\ndef collect_payloads():\n    pass\n",
            "E_SOURCE_PRIVILEGED_DEF_SCOPE",
        ),
        ("N91-S23", "import tempfile\ntempfile.NamedTemporaryFile(delete=False)\n", "E_SOURCE_TEMP_API"),
        ("N91-S24", "import os\nos.truncate('x', 0)\n", "E_SOURCE_OS_API"),
        ("N91-S25", "import os\ntruncator = os.truncate\n", "E_SOURCE_MODULE_API"),
        ("N91-S26", "import subprocess\nrunner = subprocess.getoutput\nrunner('echo unsafe')\n", "E_SOURCE_MODULE_API"),
        (
            "N91-S27",
            "from pathlib import Path\nopener = Path.open\nhandle = opener(Path('x'), 'w')\nhandle.writelines(['unsafe'])\n",
            "E_SOURCE_CALLABLE_TRANSPORT",
        ),
        ("N91-S28", "import sys\nmodule = sys.modules['os']\nmodule.system('echo unsafe')\n", "E_SOURCE_MODULE_API"),
        ("N91-S29", "import subprocess\nrunner = vars(subprocess)['getoutput']\nrunner('echo unsafe')\n", "E_SOURCE_DYNAMIC_CALL"),
        ("N91-S30", "import os\nmodule = os\nmodule.system('echo unsafe')\n", "E_SOURCE_CALLABLE_TRANSPORT"),
        ("N91-S31", "import subprocess\nmodule = subprocess\nmodule.getoutput('echo unsafe')\n", "E_SOURCE_CALLABLE_TRANSPORT"),
        ("N91-S32", "import tempfile\nmodule = tempfile\nmodule.NamedTemporaryFile(delete=False)\n", "E_SOURCE_CALLABLE_TRANSPORT"),
        ("N91-S33", "handle.writelines(['unsafe'])\n", "E_SOURCE_FILE_MUTATION"),
        ("N91-S34", "opener = __builtins__['open']\nopener('unsafe.txt', 'w')\n", "E_SOURCE_DYNAMIC_NAME"),
        ("N91-S35", "handle.truncate(0)\n", "E_SOURCE_FILE_MUTATION"),
        ("N91-S36", "handle.flush()\n", "E_SOURCE_FILE_MUTATION"),
        ("N91-S37", "import sys\nframe = sys._getframe()\nmodule = frame.f_globals['os']\nmodule.system('echo unsafe')\n", "E_SOURCE_DUNDER_LOOKUP"),
        ("N91-S38", "import argparse\nargparse._os.system('echo blocked')\n", "E_SOURCE_MODULE_API"),
        ("N91-S39", "from argparse import FileType\nFileType('w')('blocked')\n", "E_SOURCE_IMPORT"),
        ("N91-S40", "import argparse\nargparse.FileType('w')('blocked')\n", "E_SOURCE_MODULE_API"),
        ("N91-S41", "from argparse import _os\n_os.system('echo blocked')\n", "E_SOURCE_IMPORT"),
        ("N91-S42", "import pathlib\npathlib.os.system('echo blocked')\n", "E_SOURCE_IMPORT"),
        ("N91-S43", "import ast\nast.sys.modules['os'].system('echo blocked')\n", "E_SOURCE_MODULE_API"),
        ("N91-S44", "import os\ndef collect_payloads():\n    os = Path\n", "E_SOURCE_MODULE_REBIND"),
        ("N91-S45", "_write_payload_temp(Path('blocked'), b'x')\n", "E_SOURCE_PRIVILEGED_CALL"),
        ("N91-S46", "writer = _write_payload_temp\nwriter(Path('blocked'), b'x')\n", "E_SOURCE_PRIVILEGED_TRANSPORT"),
        ("N91-S47", "_safe_unlink_payload(Path('blocked'), b'')\n", "E_SOURCE_PRIVILEGED_CALL"),
        ("N91-S48", "Path('src').copy('dst')\n", "E_SOURCE_FILE_MUTATION"),
        ("N91-S49", "Path('src').copy_into('dst')\n", "E_SOURCE_FILE_MUTATION"),
        ("N91-S50", "Path('src').move('dst')\n", "E_SOURCE_FILE_MUTATION"),
        ("N91-S51", "Path('src').move_into('dst')\n", "E_SOURCE_FILE_MUTATION"),
        ("N91-S52", "Path('blocked')._delete()\n", "E_SOURCE_DUNDER_LOOKUP"),
        ("N91-S53", "frame = (x for x in ()).gi_frame\nmodule = frame.f_globals['os']\nmodule.system('echo blocked')\n", "E_SOURCE_DUNDER_LOOKUP"),
    )
    for case_id, source, code in additional_source_policy_cases:
        _source_policy_failure(source, "validator", code, case_id)
        executed_negative_ids.append(case_id)
        tests += 1
    followup_source_policy_cases = (
        (
            "N91-S54",
            "import validate_phase068_step91 as contract\ncontract.os.system('echo blocked')\n",
            "builder",
            "E_SOURCE_MODULE_API",
        ),
        (
            "N91-S55",
            "import validate_phase068_step91 as contract\nmodule = contract\n",
            "builder",
            "E_SOURCE_CALLABLE_TRANSPORT",
        ),
        (
            "N91-S56",
            "import os\ndef collect_payloads():\n    deferred = lambda: os.open('blocked', os.O_CREAT | os.O_WRONLY, 0o600)\n",
            "validator",
            "E_SOURCE_DYNAMIC_SCOPE",
        ),
        ("N91-S57", "Path('blocked').open('w')\n", "validator", "E_SOURCE_DYNAMIC_CALL"),
        ("N91-S58", "def f(os):\n    pass\n", "validator", "E_SOURCE_MODULE_REBIND"),
    )
    for case_id, source, role, code in followup_source_policy_cases:
        _source_policy_failure(source, role, code, case_id)
        executed_negative_ids.append(case_id)
        tests += 1

    def tamper_first(source: str, old: str, new: str) -> str:
        head, separator, tail = source.partition(old)
        if not separator:
            fail("E_SELFTEST_SOURCE_SEAL_FIXTURE", old)
        return head + new + tail

    validator_source = read_text_file(VALIDATOR)
    builder_source = read_text_file(BUILDER)
    source_seal_cases = (
        (
            "N91-S59",
            tamper_first(
                validator_source,
                "descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)",
                "descriptor = os.open(ROOT / 'blocked', os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)",
            ),
            "validator",
        ),
        (
            "N91-S60",
            tamper_first(
                validator_source,
                "    validate_git_argv(args, authorized_oids=authorized_oids, authorized_pairs=authorized_pairs)\n    return subprocess.run(",
                "    validate_git_argv(args, authorized_oids=authorized_oids, authorized_pairs=authorized_pairs)\n    args[0] = 'checkout'\n    return subprocess.run(",
            ),
            "validator",
        ),
        (
            "N91-S61",
            tamper_first(
                validator_source,
                "def validate_source_guard() -> None:\n",
                "def validate_source_guard() -> None:\n    print(Path('C:/blocked').read_text(encoding='utf-8'))\n",
            ),
            "validator",
        ),
        (
            "N91-S62",
            tamper_first(
                builder_source,
                'WRITER_SCHEMA = "P068-STEP91-TWO-JSON-WRITER-1"',
                'WRITER_SCHEMA = "P068-STEP91-TWO-JSON-WRITER-2"',
            ),
            "builder",
        ),
        (
            "N91-S63",
            tamper_first(validator_source, "        dir=destination.parent,", "        dir=ROOT,"),
            "validator",
        ),
        (
            "N91-S64",
            tamper_first(
                validator_source,
                "            os.link(inventory_temp, inventory_path)",
                "            os.link(ROOT / 'blocked', inventory_path)",
            ),
            "validator",
        ),
    )
    for case_id, source, role in source_seal_cases:
        _source_policy_failure(source, role, "E_SOURCE_EXACT_SEAL", case_id)
        executed_negative_ids.append(case_id)
        tests += 1
    pristine_human = (
        read_text_file(RESULT),
        read_text_file(PARENT_LEDGER),
        read_text_file(ACTIVE_LEDGER),
        read_text_file(HANDOVER),
    )
    validate_human_control_texts(*pristine_human)

    def mutate_prefixed(text: str, prefix: str, replacement: Any) -> str:
        lines = text.splitlines()
        indexes = [index for index, line in enumerate(lines) if line.startswith(prefix)]
        if len(indexes) != 1:
            fail("E_SELFTEST_HUMAN_FIXTURE", f"{prefix!r}:{len(indexes)}")
        lines[indexes[0]] = replacement(lines[indexes[0]])
        return "\n".join(lines) + ("\n" if text.endswith("\n") else "")

    def replace_once_fixture(text: str, old: str, new: str) -> str:
        head, separator, tail = text.partition(old)
        if not separator or old in tail:
            fail("E_SELFTEST_HUMAN_FIXTURE", old)
        return head + new + tail

    human_cases: list[tuple[str, tuple[str, str, str, str], str]] = []
    result_bad_status = mutate_prefixed(
        pristine_human[0],
        "Status: ",
        lambda _: "Status: `FAIL`; superseded expected=`PASS_PENDING_PERSISTENCE`",
    )
    human_cases.append(("N91-H01", (result_bad_status, *pristine_human[1:]), "E_CONTROL_EXACT_LINE"))
    handover_duplicate_recovery = mutate_prefixed(
        pristine_human[3],
        "- Step 91 recovery coverage is complete for frozen Claude topology:",
        lambda line: (
            "- Step 91 recovery coverage is complete for frozen Claude topology: commits `2`, parent edges `2`, edge path events `2/1`, net paths `3`, and `6` unique before/after UTF-8 blobs read from byte 0 through EOF without gaps. Claim register `C91-01..C91-60` has `139` exact claimant-surface pointers; seven supplemental units map complete source ranges back to those claims; `62` named negative controls are declared. U13 is a self-reported proposition under `UNDECIDED_ROUTE_STEP94`; no PDF/binary occurred, no source was modified, and scientific truth promotions: 0.\n"
            + line
        ),
    )
    human_cases.append(("N91-H02", (*pristine_human[:3], handover_duplicate_recovery), "E_CONTROL_EXACT_LINE"))
    parent_bad_row = mutate_prefixed(
        pristine_human[1],
        "| 068 |",
        lambda line: replace_once_fixture(
            replace_once_fixture(line, "| PASS_PENDING_PERSISTENCE |", "| FAIL |"),
            "| Step 91 review,",
            "| expected PASS_PENDING_PERSISTENCE; Step 91 review,",
        ),
    )
    human_cases.append(("N91-H03", (pristine_human[0], parent_bad_row, pristine_human[2], pristine_human[3]), "E_CONTROL_ROW_EXACT"))
    active_bad_row = mutate_prefixed(
        pristine_human[2],
        "| 068 |",
        lambda line: replace_once_fixture(
            replace_once_fixture(line, "| PASS_PENDING_PERSISTENCE |", "| FAIL |"),
            "| dual Step 91",
            "| expected PASS_PENDING_PERSISTENCE; dual Step 91",
        ),
    )
    human_cases.append(("N91-H04", (pristine_human[0], pristine_human[1], active_bad_row, pristine_human[3]), "E_CONTROL_ROW_EXACT"))
    handover_bad_20 = mutate_prefixed(
        pristine_human[3],
        "20. 현재 Phase 상태:",
        lambda line: replace_once_fixture(line, "Step 91 holds selected", "Step 91 FAIL; expected Step 91 holds selected"),
    )
    human_cases.append(("N91-H05", (*pristine_human[:3], handover_bad_20), "E_CONTROL_EXACT_LINE"))
    handover_bad_21 = mutate_prefixed(
        pristine_human[3],
        "21. 현재 result:",
        lambda line: replace_once_fixture(line, RESULT, "wrong/result.md") + f"; expected `{RESULT}`",
    )
    human_cases.append(("N91-H06", (*pristine_human[:3], handover_bad_21), "E_CONTROL_EXACT_LINE"))
    handover_bad_22 = mutate_prefixed(
        pristine_human[3],
        "22. 현재 machine evidence:",
        lambda line: replace_once_fixture(line, BUILDER, "wrong/builder.py") + f"; expected `{BUILDER}`",
    )
    human_cases.append(("N91-H07", (*pristine_human[:3], handover_bad_22), "E_CONTROL_EXACT_LINE"))
    handover_bad_row = mutate_prefixed(
        pristine_human[3],
        "| Phase 068 Step 91 |",
        lambda line: replace_once_fixture(line, "| dual persistence, then Step 92 |", "| FAIL; expected dual persistence, then Step 92 |"),
    )
    human_cases.append(("N91-H08", (*pristine_human[:3], handover_bad_row), "E_CONTROL_ROW_EXACT"))
    handover_bad_next = mutate_prefixed(
        pristine_human[3],
        "Keep `Codex/work/v1025_phase068/build_phase068_step91.py`",
        lambda line: "STOP. " + line,
    )
    human_cases.append(("N91-H09", (*pristine_human[:3], handover_bad_next), "E_CONTROL_SECTION_EXACT"))
    duplicate_section = replace_once_fixture(
        pristine_human[3],
        "## Hard-stop Reminder",
        "## Exact Next Action\n\nDUPLICATE\n\n## Hard-stop Reminder",
    )
    human_cases.append(("N91-H10", (*pristine_human[:3], duplicate_section), "E_CONTROL_SECTION_EXACT"))
    for case_id, texts, code in human_cases:
        _human_failure(texts, code, case_id)
        executed_negative_ids.append(case_id)
        tests += 1
    validate_human_control_texts(*pristine_human)
    base_inventory, base_attestation = build_payload_objects()
    pristine_payload_bytes = (canonical_bytes(base_inventory), canonical_bytes(base_attestation))
    contract_cases = 0

    def run_contract_negative(inventory: dict[str, Any], attestation: dict[str, Any], expected_code: str) -> None:
        nonlocal contract_cases
        case_id = NEGATIVE_CONTROL_CATALOG["payload_contract"][contract_cases]
        _contract_failure(inventory, attestation, expected_code, case_id)
        executed_negative_ids.append(case_id)
        contract_cases += 1

    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["unknown"] = True
    run_contract_negative(inventory, attestation, "E_CONTRACT_TOP_LEVEL_FIELDS")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["commits"].pop()
    run_contract_negative(inventory, attestation, "E_CONTRACT_COMMIT_COUNT")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["commits"][0]["oid"] = "0" * 40
    run_contract_negative(inventory, attestation, "E_CONTRACT_COMMIT_IDENTITY")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["commits"][0]["parents"] = ["0" * 40]
    run_contract_negative(inventory, attestation, "E_CONTRACT_COMMIT_PARENT")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["commits"][0]["subject"] = "changed"
    run_contract_negative(inventory, attestation, "E_CONTRACT_COMMIT_SUBJECT")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["edges"][0]["path_count"] = 1
    run_contract_negative(inventory, attestation, "E_CONTRACT_EDGE_PATH_COUNT")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["edges"][0]["changes"][0]["path"] = "wrong"
    run_contract_negative(inventory, attestation, "E_CONTRACT_EDGE_PATH")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["edges"][0]["changes"][0]["status"] = "A"
    run_contract_negative(inventory, attestation, "E_CONTRACT_EDGE_STATUS")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["edges"][0]["changes"][0]["old_mode"] = "100755"
    run_contract_negative(inventory, attestation, "E_CONTRACT_EDGE_MODE")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["edges"][0]["changes"][0]["old_blob"] = "0" * 40
    run_contract_negative(inventory, attestation, "E_CONTRACT_EDGE_BLOB")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["net_path_count"] = 2
    run_contract_negative(inventory, attestation, "E_CONTRACT_NET_COUNT")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["net_changes"][0]["path"] = "wrong"
    run_contract_negative(inventory, attestation, "E_CONTRACT_NET_TOPOLOGY")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    attestation["unique_blobs"][0]["coverage"]["byte_end"] -= 1
    run_contract_negative(inventory, attestation, "E_CONTRACT_BLOB_COVERAGE")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["claim_count"] = 59
    run_contract_negative(inventory, attestation, "E_CONTRACT_CLAIM_COUNT")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["claims"][1]["id"] = "C91-01"
    run_contract_negative(inventory, attestation, "E_CONTRACT_CLAIM_IDS")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["claims"][0].pop("domain")
    run_contract_negative(inventory, attestation, "E_CONTRACT_CLAIM_FIELDS")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["claims"][0]["claimant_surfaces"].clear()
    run_contract_negative(inventory, attestation, "E_CONTRACT_CLAIM_SURFACES")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["claims"][0]["scientific_truth_promoted"] = True
    run_contract_negative(inventory, attestation, "E_CONTRACT_AUTHORITY_PROMOTION")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["claims"][12]["truth_status"] = "VERIFIED_SCIENTIFIC_TRUTH"
    run_contract_negative(inventory, attestation, "E_CONTRACT_CLAIM_METADATA")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["claims"][0]["supporting_evidence_ids"] = ["wrong"]
    run_contract_negative(inventory, attestation, "E_CONTRACT_EVIDENCE_LINK")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["claim_source_pointer_count"] -= 1
    run_contract_negative(inventory, attestation, "E_CONTRACT_CLAIM_POINTER_DENOMINATOR")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["claims"][15]["owner"] = "STEP91_REPOSITORY_AUDIT"
    run_contract_negative(inventory, attestation, "E_CONTRACT_CLAIM_METADATA")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["supplemental_claim_units"][0]["claim_ids"] = ["C91-99"]
    run_contract_negative(inventory, attestation, "E_CONTRACT_SUPPLEMENTAL_LINK")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["supplemental_claim_units"][0]["claim_ids"].pop()
    run_contract_negative(inventory, attestation, "E_CONTRACT_SUPPLEMENTAL_EXHAUSTIVE")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["u13_disposition"] = "CONFIRMED"
    run_contract_negative(inventory, attestation, "E_CONTRACT_U13_AUTHORITY")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    attestation["edge_path_event_count"] = 6
    run_contract_negative(inventory, attestation, "E_CONTRACT_ATTESTATION_DENOMINATORS")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    attestation["coverage_gaps"] = ["gap"]
    run_contract_negative(inventory, attestation, "E_CONTRACT_COVERAGE_GAPS")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    attestation["evidence_set_sha256"] = "0" * 64
    run_contract_negative(inventory, attestation, "E_CONTRACT_EVIDENCE_BINDING")
    inventory, attestation = copy.deepcopy((base_inventory, base_attestation))
    inventory["content_terminal"] = "FAIL"
    run_contract_negative(inventory, attestation, "E_CONTRACT_TERMINAL")
    validate_payload_contract(base_inventory, base_attestation)
    if pristine_payload_bytes != (canonical_bytes(base_inventory), canonical_bytes(base_attestation)):
        fail("E_SELFTEST_MUTATION_RESTORE")
    expected_negative_ids = [case_id for value in NEGATIVE_CONTROL_CATALOG.values() for case_id in value]
    if executed_negative_ids != expected_negative_ids:
        fail("E_SELFTEST_NEGATIVE_REACHABILITY", repr(executed_negative_ids))
    tests += contract_cases
    print(f"PASS_P068_STEP91_SELF_TESTS {tests}")
    return tests


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--collect", action="store_true")
    modes.add_argument("--content-only", action="store_true")
    modes.add_argument("--verify-staged", action="store_true")
    modes.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args(argv)
    has_expected_commit = args.expected_commit is not None
    if args.verify_persistence != has_expected_commit:
        parser.error("--expected-commit is required only with --verify-persistence")
    if args.verify_persistence and args.expected_commit == "":
        parser.error("--expected-commit must not be empty")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        tests = run_self_tests()
        if args.collect:
            inventory_raw, attestation_raw = collect_payloads()
            print(
                f"{CONTENT_TERMINAL} collect=JSON_LAST result_first=true "
                f"inventory_bytes={len(inventory_raw)} inventory_sha256={sha256(inventory_raw)} "
                f"attestation_bytes={len(attestation_raw)} attestation_sha256={sha256(attestation_raw)} "
                f"self_tests={tests}"
            )
            return 0
        if args.content_only:
            validate_content()
            print(f"{CONTENT_TERMINAL} self_tests={tests}")
        elif args.verify_staged:
            validate_staged()
            print(f"{CONTENT_TERMINAL} staged=exact-eight self_tests={tests}")
        else:
            validate_persistence(args.expected_commit)
            print(f"{PERSISTENCE_TERMINAL} commit={args.expected_commit} self_tests={tests}")
        return 0
    except ValidationError as exc:
        print(f"FAIL_P068_STEP91 {exc.code} {exc.detail}".rstrip(), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
