#!/usr/bin/env python3
"""Validate the Phase 060 Step 41 process-authority matrix."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "Codex/results/PHASE_060_V1019_PROCESS_INTENT_MATRIX.json"
BUILDER = ROOT / "Codex/work/v1019_phase060/build_phase060_step41_process_authority.py"
EXPECTED_SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_SPEC_FINGERPRINTS = {
    "PROCESS_SOURCES": "9859a847943c09dea411651c73762e26c3674f6c13ea64f7420241379d4a487d",
    "RELEASE_SOURCES": "22992eb79bd839c01040c13ed7d1434e9103de62cabf805805477125e6f5a503",
    "WITNESS_SOURCES": "2da5e5fc7fbff8ae02b1a675ebfd544139acef84bf6d3469c6737f25a6866b96",
    "COMMIT_EVENTS": "ba775d3f26c463b390bf8cbcebe9167a3ee23a3e46bc9b10748a54b510a013c0",
    "CLAIM_SPECS": "6d891ae8e4f47f39f97d2854022a7893edb14eec72ee03c741a0e53bf5f6082f",
    "CH2_DEFECT_CORRECTION_SPECS": "199f576115ae05fb15bec4f0422ced8d62115f7a38c46abeb0d4a67ea40462c8",
    "CONTRADICTION_SPECS": "86cc25061c8fd8ba60e2ec6f06a19330724ce28b99f4a82a8e6683c8ae9b8d5e",
    "UNRESOLVED_SPECS": "cc4dc5b10fe1f693d70be7373e3d5a4645a23a010c5ba8f8d724b16e3dc656bf",
}
EXPECTED_AUTHORITY_POLICY = {
    "allowed_claim_types": [
        "USER_REQUIREMENT",
        "PROCESS_EVIDENCE",
        "SELF_ASSERTION",
        "SCIENTIFIC_CLAIM",
        "RUNTIME_CLAIM",
        "UNVERIFIED",
    ],
    "rules": [
        "Commit chronology and process checklists establish PROCESS_EVIDENCE only.",
        "Scientific/runtime completion requires independent release-source evidence and independent execution or rederivation.",
        "Asset presence or preservation assertions do not establish physical validity or citation truth.",
        "Contradictions are preserved and routed; latest-file and majority preference are forbidden.",
        "The bounded continuity scan cannot establish general physical validity.",
    ],
}
EXPECTED_AUTHORITY_DECISIONS = [
    {"decision_id": "AUT-001", "decision": "ACCEPT_PROCESS_CHRONOLOGY", "scope": "Named stages, recorded reviewer roles, checklists, defect registers, correction records, and verified commit existence only."},
    {"decision_id": "AUT-002", "decision": "NO_SCIENTIFIC_PROMOTION", "scope": "All physical validity, derivation correctness, material claims, and citation truth remain Step 44/Phase 071 work."},
    {"decision_id": "AUT-003", "decision": "NO_RUNTIME_PROMOTION", "scope": "Code behavior, tests, stored/fresh artifacts, and continuity require Step 42 and document-to-reachable-code Step 43."},
    {"decision_id": "AUT-004", "decision": "ASSET_PRESENCE_NOT_VALIDITY", "scope": "336 and 133 are process checklist identities; their presence/preservation assertions are not independent physical or citation validation."},
    {"decision_id": "AUT-005", "decision": "PRESERVE_CONTRADICTIONS", "scope": "All six recorded authority conflicts retain both positions and explicit downstream routes."},
]
EXPECTED_AUTHORITY_BOUNDARIES = {
    "PROCESS_INPUT": "Process prose is evidence of recorded intent/activity only.",
    "RELEASE_INPUT": "Release text is an independent release-source witness, not automatic scientific/runtime truth.",
    "CARRIED_STEP40_WITNESS": "Step 40 full-read witness used only to preserve an explicit authority contradiction.",
}
GENERATION_METADATA_KEYS = frozenset(
    {"builder", "source_commit", "volatile_timestamp", "ordering", "encoding", "line_metric"}
)
AUTHORITY_POLICY_KEYS = frozenset({"allowed_claim_types", "rules"})
SOURCE_SUMMARY_KEYS = frozenset(
    {
        "process",
        "release",
        "carried_step40_witness",
        "mandatory_full_read_files",
        "mandatory_full_read_physical_lines",
    }
)
SOURCE_SUMMARY_GROUP_KEYS = frozenset({"files", "physical_lines", "nonblank_lines"})
SOURCE_RECORD_KEYS = frozenset(
    {
        "path",
        "group",
        "git_blob_sha1",
        "sha256",
        "size_bytes",
        "physical_lines",
        "nonblank_lines",
        "read_coverage",
        "coverage_status",
        "authority_boundary",
    }
)
READ_COVERAGE_KEYS = frozenset({"start_line", "end_line"})
ANCHOR_KEYS = frozenset({"path", "start_line", "end_line", "anchor_text_sha256", "excerpt"})
CLAIM_RECORD_KEYS = frozenset(
    {"claim_id", "claim_type", "topic", "claim", "authority_decision", "anchors", "independent_release_evidence"}
)
INDEPENDENT_RELEASE_EVIDENCE_KEYS = frozenset({"anchor_count", "status"})
DEFECT_CORRECTION_RECORD_KEYS = frozenset(
    {
        "obligation_id",
        "defect_id",
        "defect_summary",
        "prescribed_correction",
        "reviewer_attribution",
        "claim_type",
        "authority_decision",
        "defect_evidence",
        "prescribed_correction_evidence",
        "reviewer_evidence",
        "completion_assertion",
        "completion_evidence",
    }
)
CHRONOLOGY_RECORD_KEYS = frozenset(
    {"event_id", "stage", "commit", "subject", "purpose", "claim_type", "scientific_truth", "runtime_truth", "anchors"}
)
CONTRADICTION_RECORD_KEYS = frozenset(
    {"contradiction_id", "title", "status", "route", "adjudication", "positions"}
)
CONTRADICTION_POSITION_KEYS = frozenset({"position", "anchors"})
UNRESOLVED_RECORD_KEYS = frozenset({"unresolved_id", "item", "route", "anchors"})
AUTHORITY_DECISION_KEYS = frozenset({"decision_id", "decision", "scope"})
GATE_SUMMARY_KEYS = frozenset(
    {
        "source_orphans",
        "source_orphan_count",
        "defect_correction_orphans",
        "defect_correction_orphan_count",
        "unresolved_obligation_orphans",
        "unresolved_obligation_orphan_count",
        "contradiction_obligation_orphans",
        "contradiction_obligation_orphan_count",
        "duplicate_claim_identity_count",
        "unsupported_authority_promotions",
        "unsupported_authority_promotion_count",
        "contradiction_unrouted",
        "contradiction_unrouted_count",
        "scientific_claims_promoted",
        "runtime_claims_promoted",
        "next_step",
    }
)
NON_PROMOTING_COMPLETION_DECISIONS = {
    "NOT_PROMOTED_STEP42",
    "NOT_PROMOTED_STEP43",
    "NOT_PROMOTED_STEP44",
    "HISTORICAL_CORRECTION_PROCESS_ONLY",
}
CH2_UNION_PATH = "Claude/results/process/V1019_CH2_UNION_DEFECTS.md"
PROCESS_LEDGER_PATH = "Claude/results/process/V1019_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Claude/docs/v1.0.19/HANDOVER_v1.0.19.md"
CH1_UNION_PATH = "Claude/results/process/V1019_UNION_DEFECTS.md"
REQUIRED_CH2_DEFECT_CORRECTION_OBLIGATIONS = [
    {"obligation_id": "DCR-CU-02", "defect_id": "CU-2", "defect_summary": "The union records a site-versus-molar mixed intermediate expression and an unstated chemical-potential cancellation.", "prescribed_correction": "Delete the mixed intermediate expression, or rewrite it with numerator and denominator multiplied by N_A while explicitly showing N_A epsilon_0 minus mu equals mu_0 minus mu equals sF(V-U_j) over RT.", "source_anchor": (CH2_UNION_PATH, 20, 21), "reviewer_attribution": ["W1-2", "W10-2"], "completion_anchor": (PROCESS_LEDGER_PATH, 53, 53)},
    {"obligation_id": "DCR-CU-03", "defect_id": "CU-3", "defect_summary": "The union records literal Ch1 internal label names printed as prose across Ch2.", "prescribed_correction": "Replace prose references of the form 'equation eq:XXX' with descriptive Chapter 1 section-and-equation wording while retaining Ch2-local eqref references.", "source_anchor": (CH2_UNION_PATH, 23, 24), "reviewer_attribution": ["W3-1", "W9 관련"], "completion_anchor": (PROCESS_LEDGER_PATH, 53, 53)},
    {"obligation_id": "DCR-CU-04", "defect_id": "CU-4", "defect_summary": "The union records the Ch2-local eq:Se label colliding with the Ch1 eq:Se label.", "prescribed_correction": "Rename the Ch2-local label, for example to eq:Se-ch2, and add the collision to Appendix A or separate the two references with a footnote.", "source_anchor": (CH2_UNION_PATH, 26, 27), "reviewer_attribution": ["W9-1"], "completion_anchor": (PROCESS_LEDGER_PATH, 53, 53)},
    {"obligation_id": "DCR-CU-05", "defect_id": "CU-5", "defect_summary": "The union records tension between 'sum' wording and an underbrace that labels the unsigned raw entropy term as reversible heat.", "prescribed_correction": "Move the minus sign into the underbraced reversible-heat term, or replace 'sum' with wording that explicitly denotes a signed combination.", "source_anchor": (CH2_UNION_PATH, 29, 30), "reviewer_attribution": ["W6-1"], "completion_anchor": (PROCESS_LEDGER_PATH, 53, 53)},
    {"obligation_id": "DCR-CU-06", "defect_id": "CU-6", "defect_summary": "The union records duplicate transition prose at the end of section 2.6 and start of section 2.7.", "prescribed_correction": "Make the section 2.6 ending a local close and leave the forward transition solely to the section 2.7 opening.", "source_anchor": (CH2_UNION_PATH, 32, 33), "reviewer_attribution": ["W6-2"], "completion_anchor": (PROCESS_LEDGER_PATH, 53, 53)},
    {"obligation_id": "DCR-CU-07", "defect_id": "CU-7", "defect_summary": "The union records an Appendix A 'common error' claim absent from its cited source section and therefore inconsistent with the appendix's pure-republication rule.", "prescribed_correction": "Correct the basis to ssec:sconfig/ssec:dvdt and add the claimed warning to the body, or narrow the appendix wording to a statement already present in the body.", "source_anchor": (CH2_UNION_PATH, 35, 36), "reviewer_attribution": ["W8-1"], "completion_anchor": (PROCESS_LEDGER_PATH, 53, 53)},
    {"obligation_id": "DCR-CU-08", "defect_id": "CU-8", "defect_summary": "The union records an overgeneralized analogy between the Ch1 and Ch2 entropy skeletons.", "prescribed_correction": "Qualify the analogy as limited to configurational centering and distribution separation.", "source_anchor": (CH2_UNION_PATH, 39, 39), "reviewer_attribution": ["W2-1"], "completion_anchor": (PROCESS_LEDGER_PATH, 53, 53)},
    {"obligation_id": "DCR-CU-09", "defect_id": "CU-9", "defect_summary": "The union records an ambiguous singular 'next section' transition spanning two following sections.", "prescribed_correction": "Name both following sections explicitly.", "source_anchor": (CH2_UNION_PATH, 40, 40), "reviewer_attribution": ["W3-2"], "completion_anchor": (PROCESS_LEDGER_PATH, 53, 53)},
    {"obligation_id": "DCR-CU-10", "defect_id": "CU-10", "defect_summary": "The union records that eq:weighted lacks its derivation-A marker.", "prescribed_correction": "Add the derivation-A marker to the title or equivalent heading.", "source_anchor": (CH2_UNION_PATH, 41, 41), "reviewer_attribution": ["W5-1"], "completion_anchor": (PROCESS_LEDGER_PATH, 53, 53)},
    {"obligation_id": "DCR-CU-11", "defect_id": "CU-11", "defect_summary": "The union records that all initial Omega values exceed the two-phase threshold while the prose identifies a specific two-phase transition.", "prescribed_correction": "State that the initial Omega values all exceed 2RT and that transition-specific two-phase identification depends on measured plateau/staging literature and the Ch1 A-106 post-fit basis.", "source_anchor": (CH2_UNION_PATH, 42, 42), "reviewer_attribution": ["W10-1"], "completion_anchor": (PROCESS_LEDGER_PATH, 53, 53)},
]
REQUIRED_UNRESOLVED_OBLIGATIONS = [
    {"unresolved_id": "UNR-001", "route": "STEP43_DOCUMENT_TO_REACHABLE_CODE", "anchors": [("Claude/docs/v1.0.19/FITTING_GUIDE.md", 61, 66), (HANDOVER_PATH, 26, 27)]},
    {"unresolved_id": "UNR-002", "route": "STEP43_DOCUMENT_TO_REACHABLE_CODE", "anchors": [(HANDOVER_PATH, 34, 35)]},
    {"unresolved_id": "UNR-003", "route": "STEP44_PHYSICS_REDERIVATION_AND_PHASE071_REFERENCE_TRUTH", "anchors": [("Claude/docs/v1.0.19/FITTING_GUIDE.md", 21, 31), (HANDOVER_PATH, 34, 35)]},
    {"unresolved_id": "UNR-004", "route": "STEP43_DOCUMENT_TO_REACHABLE_CODE", "anchors": [("Claude/docs/v1.0.19/_sections/ch1_appB_codemap.tex", 4, 16), ("Claude/docs/v1.0.19/_sections/ch2_appB_codemap.tex", 7, 22)]},
    {"unresolved_id": "UNR-005", "route": "STEP42_RUNTIME_AND_ARTIFACT_AUDIT", "anchors": [("Claude/docs/v1.0.19/samples/continuity_scan_report.txt", 13, 15), ("Claude/results/process/V1019_CONTINUITY_JUDGMENT.md", 15, 37)]},
    {"unresolved_id": "UNR-006", "route": "STEP44_PHYSICS_REDERIVATION_AND_PHASE071_REFERENCE_TRUTH", "anchors": [(CH1_UNION_PATH, 5, 8), (CH2_UNION_PATH, 5, 8)]},
    {"unresolved_id": "UNR-007", "route": "USER_DECISION_LATER_PHASE", "anchors": [(HANDOVER_PATH, 34, 38), ("Claude/results/process/V1019_FINAL_REVIEW_UNION.md", 47, 49)]},
    {"unresolved_id": "UNR-008", "route": "STEP45_1_CLAIM_DEFECT_DISPOSITION", "anchors": [(HANDOVER_PATH, 36, 36), (CH1_UNION_PATH, 54, 55)]},
    {"unresolved_id": "UNR-009", "route": "STEP45_1_CLAIM_DEFECT_DISPOSITION", "anchors": [(HANDOVER_PATH, 37, 37), (CH1_UNION_PATH, 57, 60)]},
    {"unresolved_id": "UNR-010", "route": "STEP45_1_CLAIM_DEFECT_DISPOSITION", "anchors": [(HANDOVER_PATH, 38, 38)]},
    {"unresolved_id": "UNR-011", "route": "STEP45_1_CLAIM_DEFECT_DISPOSITION_AND_PHASE071_072_REFERENCE_DATA_TRUTH", "anchors": [(HANDOVER_PATH, 38, 38)]},
]
EXPECTED_UNRESOLVED_ITEM_TEXT = {
    "UNR-001": "Multi-temperature LCO electronic temperature restoration is unimplemented.",
    "UNR-002": "Total heat irreversible q_irr decomposition remains future work.",
    "UNR-003": "LCO tier-2/3 Omega and activation-energy measured anchors are not found.",
    "UNR-004": "The actual reachable code must adjudicate current implementation versus future requirement wording.",
    "UNR-005": "Continuity output requires independent rerun and broader runtime/artifact inspection.",
    "UNR-006": "Physical derivations and claimed zero-error outcomes require independent rederivation; literature and DOI truth remain separate.",
    "UNR-007": "Standalone appendix integration remains a user decision.",
    "UNR-008": "Whether broadening should receive N6a/N6b sublabels remains an optional naming decision.",
    "UNR-009": "The W2-2 sec:center-eqcond/Uj labels remain harmless orphans with reverse-reference wiring or pruning deferred.",
    "UNR-010": "Future-physics proposals 2 through 5 remain externally delegated and measurement-pending.",
    "UNR-011": "The v1.0.16 physics-data obligation remains externally delegated and measurement-pending.",
}
REQUIRED_CONTRADICTION_OBLIGATIONS = [
    {"contradiction_id": "CTR-001", "route": ["STEP42_RUNTIME_AND_ARTIFACT_AUDIT", "STEP43_DOCUMENT_TO_REACHABLE_CODE"], "position_names": ["COMPLETED", "FUTURE_REQUIREMENT_NOT_CURRENT_IMPLEMENTATION"], "position_anchors": [[("Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.tex", 6, 7), (HANDOVER_PATH, 26, 27)], [("Claude/docs/v1.0.19/_sections/ch2_appB_codemap.tex", 7, 10)]]},
    {"contradiction_id": "CTR-002", "route": ["STEP42_RUNTIME_AND_ARTIFACT_AUDIT", "STEP43_DOCUMENT_TO_REACHABLE_CODE"], "position_names": ["BROAD_CODE_COMPLETION", "LCO_T_RESTORATION_AND_TOTAL_HEAT_UNRESOLVED"], "position_anchors": [[(HANDOVER_PATH, 26, 27)], [("Claude/docs/v1.0.19/FITTING_GUIDE.md", 61, 66), (HANDOVER_PATH, 34, 35)]]},
    {"contradiction_id": "CTR-003", "route": ["STEP42_RUNTIME_AND_ARTIFACT_AUDIT", "STEP44_PHYSICS_REDERIVATION"], "position_names": ["GENERAL_NO_REREVIEW_NEEDED", "BOUNDED_GRIDS_AND_THRESHOLD_ONLY"], "position_anchors": [[("Claude/results/process/V1019_CONTINUITY_JUDGMENT.md", 15, 37)], [("Claude/docs/v1.0.19/samples/continuity_scan_report.txt", 13, 15), ("Claude/docs/v1.0.19/samples/continuity_scan_report.txt", 17, 129)]]},
    {"contradiction_id": "CTR-004", "route": ["STEP44_PHYSICS_REDERIVATION"], "position_names": ["ZERO_CRITICAL_PHYSICAL_ERRORS", "CU1_PHYSICAL_SIGN_ERROR_RECORDED"], "position_anchors": [[("Claude/results/process/V1019_FINAL_REVIEW_UNION.md", 5, 7)], [(CH2_UNION_PATH, 5, 8), (CH2_UNION_PATH, 17, 18)]]},
    {"contradiction_id": "CTR-005", "route": ["STEP45_1_CLAIM_DEFECT_DISPOSITION"], "position_names": ["HEADLINE_HIGH3_MED8_LOWMED3_LOW9_NOTE1", "ENUMERATED_HIGH3_MED7_LOWMED3_LOW10_NOTE1"], "position_anchors": [[(CH1_UNION_PATH, 5, 8), (PROCESS_LEDGER_PATH, 47, 47)], [(CH1_UNION_PATH, 19, 55)]]},
    {"contradiction_id": "CTR-006", "route": ["STEP45_1_CLAIM_DEFECT_DISPOSITION"], "position_names": ["HEADLINE_HIGH1_MED6_LOW_UNSLOTTED", "ENUMERATED_HIGH1_MED5_LOWMED1_LOW4"], "position_anchors": [[(CH2_UNION_PATH, 5, 8), (PROCESS_LEDGER_PATH, 52, 52), (HANDOVER_PATH, 7, 7), (HANDOVER_PATH, 22, 22)], [(CH2_UNION_PATH, 17, 42), (PROCESS_LEDGER_PATH, 52, 52)]]},
]


class DuplicateKeyError(ValueError):
    pass


class NonFiniteNumberError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_nonfinite_number(value: str) -> None:
    raise NonFiniteNumberError(f"non-finite JSON number: {value}")


def strict_json_loads(payload: str) -> Any:
    return json.loads(
        payload,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_nonfinite_number,
    )


def load_builder_module() -> Any:
    spec = importlib.util.spec_from_file_location("phase060_step41_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load builder module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git_bytes(blob_sha1: str) -> bytes:
    proc = subprocess.run(
        ["git", "cat-file", "blob", blob_sha1],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout


def git_path_blob(source_commit: str, path: str) -> str:
    proc = subprocess.run(
        ["git", "rev-parse", f"{source_commit}:{path}"],
        cwd=ROOT,
        check=True,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout.strip()


def git_commit_subject(commit: str) -> str:
    proc = subprocess.run(
        ["git", "show", "-s", "--format=%s", commit],
        cwd=ROOT,
        check=True,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout.strip()


def expected_anchor(path: str, start: int, end: int, lines_by_path: dict[str, list[str]]) -> dict[str, Any]:
    selected = "\n".join(lines_by_path[path][start - 1 : end])
    excerpt = selected.replace("\t", " ")
    if len(excerpt) > 240:
        excerpt = excerpt[:237] + "..."
    return {
        "path": path,
        "start_line": start,
        "end_line": end,
        "anchor_text_sha256": hashlib.sha256(selected.encode("utf-8")).hexdigest(),
        "excerpt": excerpt,
    }


def expected_anchors(specs: list[tuple[str, int, int]], lines_by_path: dict[str, list[str]]) -> list[dict[str, Any]]:
    return [expected_anchor(path, start, end, lines_by_path) for path, start, end in specs]


def add_error(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def require_exact_keys(
    errors: list[str], value: Any, expected_keys: frozenset[str], context: str
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{context} must be an object")
        return False
    add_error(errors, set(value) == expected_keys, f"{context} key schema mismatch")
    return True


def validate_anchor_keys(errors: list[str], value: Any, context: str) -> None:
    if not isinstance(value, list):
        errors.append(f"{context} must be a list")
        return
    for index, anchor_item in enumerate(value):
        require_exact_keys(errors, anchor_item, ANCHOR_KEYS, f"{context}[{index}]")


def semantic_fingerprint(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def extract_severity_counts(
    lines: list[str],
    pattern: str,
    severity_aliases: dict[str, str],
) -> tuple[list[int], dict[str, int]]:
    identities: list[int] = []
    counts: dict[str, int] = {}
    compiled = re.compile(pattern)
    for line in lines:
        match = compiled.search(line.replace("*", ""))
        if match is None:
            continue
        identities.append(int(match.group(1)))
        severity = severity_aliases.get(match.group(2), match.group(2))
        counts[severity] = counts.get(severity, 0) + 1
    return identities, counts


def validate_data(data: Any, module: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["artifact root must be an object"]

    expected_top_level_keys = {
        "schema_version",
        "phase",
        "step",
        "generation_metadata",
        "authority_policy",
        "source_summary",
        "sources",
        "chronology",
        "claims",
        "defect_correction_records",
        "contradictions",
        "unresolved_queue",
        "authority_decisions",
        "gate_summary",
    }
    add_error(errors, set(data) == expected_top_level_keys, "top-level schema keys mismatch")
    add_error(errors, module.SOURCE_COMMIT == EXPECTED_SOURCE_COMMIT, "builder SOURCE_COMMIT semantic contract mismatch")
    for name, expected_fingerprint in EXPECTED_SPEC_FINGERPRINTS.items():
        add_error(
            errors,
            semantic_fingerprint(getattr(module, name)) == expected_fingerprint,
            f"builder {name} semantic contract mismatch",
        )

    add_error(errors, data.get("schema_version") == "phase060-step41-process-authority-v1", "schema_version mismatch")
    add_error(errors, type(data.get("phase")) is int and data.get("phase") == 60, "phase mismatch")
    add_error(errors, type(data.get("step")) is int and data.get("step") == 41, "step mismatch")
    metadata = data.get("generation_metadata")
    add_error(errors, isinstance(metadata, dict), "generation_metadata missing")
    if isinstance(metadata, dict):
        require_exact_keys(errors, metadata, GENERATION_METADATA_KEYS, "generation_metadata")
        expected_metadata = {
            "builder": "Codex/work/v1019_phase060/build_phase060_step41_process_authority.py",
            "source_commit": EXPECTED_SOURCE_COMMIT,
            "volatile_timestamp": None,
            "ordering": "declared source/claim/chronology order; JSON keys sorted",
            "encoding": "UTF-8",
            "line_metric": "Python splitlines over frozen Git blob bytes",
        }
        add_error(errors, metadata == expected_metadata, "generation_metadata mismatch")

    policy = data.get("authority_policy")
    allowed_types = {
        "USER_REQUIREMENT",
        "PROCESS_EVIDENCE",
        "SELF_ASSERTION",
        "SCIENTIFIC_CLAIM",
        "RUNTIME_CLAIM",
        "UNVERIFIED",
    }
    require_exact_keys(errors, policy, AUTHORITY_POLICY_KEYS, "authority_policy")
    add_error(errors, policy == EXPECTED_AUTHORITY_POLICY, "authority_policy mismatch")

    expected_source_specs: list[tuple[str, str, str, int, int, int, str]] = []
    for group, specs in (
        ("PROCESS_INPUT", module.PROCESS_SOURCES),
        ("RELEASE_INPUT", module.RELEASE_SOURCES),
        ("CARRIED_STEP40_WITNESS", module.WITNESS_SOURCES),
    ):
        for path, blob, sha256, physical, nonblank, size_bytes in specs:
            expected_source_specs.append((path, blob, sha256, physical, nonblank, size_bytes, group))

    source_records = data.get("sources")
    add_error(errors, isinstance(source_records, list), "sources must be a list")
    if not isinstance(source_records, list):
        source_records = []
    actual_source_paths = [record.get("path") for record in source_records if isinstance(record, dict)]
    expected_source_paths = [spec[0] for spec in expected_source_specs]
    add_error(errors, actual_source_paths == expected_source_paths, "sources: path order/set mismatch")
    add_error(errors, len(actual_source_paths) == len(set(actual_source_paths)), "sources: duplicate path identities")

    lines_by_path: dict[str, list[str]] = {}
    expected_record_by_path: dict[str, dict[str, Any]] = {}
    for path, blob, sha256, physical, nonblank, size_bytes, group in expected_source_specs:
        worktree_path = ROOT / Path(path)
        add_error(errors, worktree_path.is_file(), f"missing source: {path}")
        try:
            committed_blob = git_path_blob(EXPECTED_SOURCE_COMMIT, path)
            payload = git_bytes(blob)
            lines = payload.decode("utf-8").splitlines()
        except Exception as exc:  # pragma: no cover - diagnostic boundary
            errors.append(f"cannot read frozen source {path}: {exc}")
            committed_blob = ""
            lines = []
            payload = b""
        lines_by_path[path] = lines
        add_error(errors, committed_blob == blob, f"source contract {path}.source_commit_path_blob")
        add_error(errors, hashlib.sha256(payload).hexdigest() == sha256, f"source contract {path}.sha256")
        add_error(errors, len(payload) == size_bytes, f"source contract {path}.size_bytes")
        add_error(errors, len(lines) == physical, f"source contract {path}.physical_lines")
        add_error(errors, sum(1 for line in lines if line.strip()) == nonblank, f"source contract {path}.nonblank_lines")
        expected_record_by_path[path] = {
            "path": path,
            "group": group,
            "git_blob_sha1": blob,
            "sha256": sha256,
            "size_bytes": size_bytes,
            "physical_lines": physical,
            "nonblank_lines": nonblank,
            "read_coverage": [{"start_line": 1, "end_line": physical}],
            "coverage_status": "READ_FULL",
            "authority_boundary": EXPECTED_AUTHORITY_BOUNDARIES[group],
        }

    ch1_severity_ids, ch1_severity_counts = extract_severity_counts(
        lines_by_path[CH1_UNION_PATH],
        r"\[U-(\d+)\]\s+(LOW-MED|HIGH|MED|LOW|NOTE)",
        {},
    )
    add_error(errors, ch1_severity_ids == list(range(1, 25)), "Ch1 detailed severity identities mismatch")
    add_error(
        errors,
        ch1_severity_counts == {"HIGH": 3, "MED": 7, "LOW-MED": 3, "LOW": 10, "NOTE": 1},
        "Ch1 detailed severity enumeration mismatch",
    )
    ch2_severity_ids, ch2_severity_counts = extract_severity_counts(
        lines_by_path[CH2_UNION_PATH],
        r"CU-(\d+)\s+\[(LOW-MED|HIGH|MEDIUM|LOW)",
        {"MEDIUM": "MED"},
    )
    add_error(errors, ch2_severity_ids == list(range(1, 12)), "Ch2 detailed severity identities mismatch")
    add_error(
        errors,
        ch2_severity_counts == {"HIGH": 1, "MED": 5, "LOW-MED": 1, "LOW": 4},
        "Ch2 detailed severity enumeration mismatch",
    )

    for record in source_records:
        if not isinstance(record, dict):
            errors.append("sources: non-object record")
            continue
        require_exact_keys(errors, record, SOURCE_RECORD_KEYS, "sources record")
        path = record.get("path")
        read_coverage = record.get("read_coverage")
        if not isinstance(read_coverage, list):
            errors.append(f"sources[{path}].read_coverage must be a list")
        else:
            for index, coverage in enumerate(read_coverage):
                require_exact_keys(
                    errors,
                    coverage,
                    READ_COVERAGE_KEYS,
                    f"sources[{path}].read_coverage[{index}]",
                )
        expected = expected_record_by_path.get(path)
        if expected is None:
            continue
        for key, value in expected.items():
            add_error(errors, record.get(key) == value, f"sources[{path}].{key} mismatch")

    source_summary = data.get("source_summary")
    expected_summary = {
        "process": {"files": 11, "physical_lines": 1028, "nonblank_lines": 889},
        "release": {"files": 5, "physical_lines": 550, "nonblank_lines": 480},
        "carried_step40_witness": {"files": 1, "physical_lines": 37, "nonblank_lines": 34},
        "mandatory_full_read_files": 16,
        "mandatory_full_read_physical_lines": 1578,
    }
    if require_exact_keys(errors, source_summary, SOURCE_SUMMARY_KEYS, "source_summary"):
        for group_name in ("process", "release", "carried_step40_witness"):
            require_exact_keys(
                errors,
                source_summary.get(group_name),
                SOURCE_SUMMARY_GROUP_KEYS,
                f"source_summary.{group_name}",
            )
    add_error(errors, source_summary == expected_summary, "source_summary mismatch")

    claims = data.get("claims")
    add_error(errors, isinstance(claims, list), "claims must be a list")
    if not isinstance(claims, list):
        claims = []
    claim_ids = [claim.get("claim_id") for claim in claims if isinstance(claim, dict)]
    add_error(errors, len(claim_ids) == len(set(claim_ids)), "duplicate claim identities")
    expected_claim_ids = [spec["claim_id"] for spec in module.CLAIM_SPECS]
    add_error(errors, claim_ids == expected_claim_ids, "claim identity/order mismatch")
    expected_claim_by_id = {spec["claim_id"]: spec for spec in module.CLAIM_SPECS}
    release_paths = {spec[0] for spec in module.RELEASE_SOURCES}
    unsupported_promotions: list[str] = []
    referenced_paths: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("claim record must be an object")
            continue
        claim_id = claim.get("claim_id")
        require_exact_keys(errors, claim, CLAIM_RECORD_KEYS, f"claims[{claim_id}]")
        validate_anchor_keys(errors, claim.get("anchors"), f"claims[{claim_id}].anchors")
        require_exact_keys(
            errors,
            claim.get("independent_release_evidence"),
            INDEPENDENT_RELEASE_EVIDENCE_KEYS,
            f"claims[{claim_id}].independent_release_evidence",
        )
        spec = expected_claim_by_id.get(claim_id)
        if spec is None:
            continue
        for key in ("claim_type", "topic", "claim", "authority_decision"):
            add_error(errors, claim.get(key) == spec[key], f"claims[{claim_id}].{key} mismatch")
        add_error(errors, claim.get("claim_type") in allowed_types, f"claims[{claim_id}] disallowed claim type")
        expected_anchor_list = expected_anchors(spec["anchors"], lines_by_path)
        add_error(errors, claim.get("anchors") == expected_anchor_list, f"claims[{claim_id}].anchors mismatch")
        for item in claim.get("anchors", []):
            if isinstance(item, dict) and isinstance(item.get("path"), str):
                referenced_paths.add(item["path"])
        release_count = sum(1 for item in expected_anchor_list if item["path"] in release_paths)
        expected_release = {
            "anchor_count": release_count,
            "status": "PRESENT_BUT_NOT_INDEPENDENTLY_EXECUTED" if release_count else "ABSENT",
        }
        add_error(errors, claim.get("independent_release_evidence") == expected_release, f"claims[{claim_id}].independent_release_evidence mismatch")
        if (
            claim.get("claim_type") in {"SCIENTIFIC_CLAIM", "RUNTIME_CLAIM"}
            and claim.get("authority_decision") not in NON_PROMOTING_COMPLETION_DECISIONS
        ):
            unsupported_promotions.append(str(claim_id))
            if release_count == 0:
                errors.append(f"unsupported authority promotion without release evidence: {claim_id}")

    defect_corrections = data.get("defect_correction_records")
    add_error(errors, isinstance(defect_corrections, list), "defect_correction_records must be a list")
    if not isinstance(defect_corrections, list):
        defect_corrections = []
    defect_correction_ids = [
        item.get("obligation_id") for item in defect_corrections if isinstance(item, dict)
    ]
    required_defect_correction_ids = [
        item["obligation_id"] for item in REQUIRED_CH2_DEFECT_CORRECTION_OBLIGATIONS
    ]
    add_error(
        errors,
        defect_correction_ids == required_defect_correction_ids,
        "defect/correction obligation identities mismatch",
    )
    required_defect_by_id = {
        item["obligation_id"]: item for item in REQUIRED_CH2_DEFECT_CORRECTION_OBLIGATIONS
    }
    for item in defect_corrections:
        if not isinstance(item, dict):
            errors.append("defect/correction obligation must be an object")
            continue
        obligation_id = item.get("obligation_id")
        require_exact_keys(
            errors,
            item,
            DEFECT_CORRECTION_RECORD_KEYS,
            f"defect/correction[{obligation_id}]",
        )
        for evidence_name in (
            "defect_evidence",
            "prescribed_correction_evidence",
            "reviewer_evidence",
            "completion_evidence",
        ):
            require_exact_keys(
                errors,
                item.get(evidence_name),
                ANCHOR_KEYS,
                f"defect/correction[{obligation_id}].{evidence_name}",
            )
        obligation = required_defect_by_id.get(obligation_id)
        if obligation is None:
            continue
        add_error(errors, item.get("defect_id") == obligation["defect_id"], f"defect/correction[{obligation_id}].defect_id mismatch")
        add_error(errors, item.get("claim_type") == "PROCESS_EVIDENCE", f"defect/correction[{obligation_id}] authority mismatch")
        add_error(errors, item.get("authority_decision") == "PROCESS_ONLY_NOT_SCIENTIFIC_OR_RUNTIME_PROOF", f"defect/correction[{obligation_id}].authority_decision mismatch")
        add_error(errors, item.get("reviewer_attribution") == obligation["reviewer_attribution"], f"defect/correction[{obligation_id}].reviewer_attribution mismatch")
        add_error(errors, item.get("defect_summary") == obligation["defect_summary"], f"defect/correction[{obligation_id}].defect_summary mismatch")
        add_error(errors, item.get("prescribed_correction") == obligation["prescribed_correction"], f"defect/correction[{obligation_id}].prescribed_correction mismatch")
        add_error(errors, item.get("completion_assertion") == "The process ledger asserts that C-P4 incorporated CU-1 through CU-11 with zero rejections.", f"defect/correction[{obligation_id}].completion_assertion mismatch")
        source_anchor = expected_anchor(*obligation["source_anchor"], lines_by_path)
        completion_anchor = expected_anchor(*obligation["completion_anchor"], lines_by_path)
        add_error(errors, item.get("defect_evidence") == source_anchor, f"defect/correction[{obligation_id}].defect_evidence mismatch")
        add_error(errors, item.get("prescribed_correction_evidence") == source_anchor, f"defect/correction[{obligation_id}].prescribed_correction_evidence mismatch")
        add_error(errors, item.get("reviewer_evidence") == source_anchor, f"defect/correction[{obligation_id}].reviewer_evidence mismatch")
        add_error(errors, item.get("completion_evidence") == completion_anchor, f"defect/correction[{obligation_id}].completion_evidence mismatch")
        referenced_paths.add(source_anchor["path"])
        referenced_paths.add(completion_anchor["path"])

    chronology = data.get("chronology")
    add_error(errors, isinstance(chronology, list), "chronology must be a list")
    if not isinstance(chronology, list):
        chronology = []
    chronology_ids = [item.get("event_id") for item in chronology if isinstance(item, dict)]
    expected_chronology_ids = [event[0] for event in module.COMMIT_EVENTS]
    add_error(errors, chronology_ids == expected_chronology_ids, "chronology identity/order mismatch")
    for item, spec in zip(chronology, module.COMMIT_EVENTS):
        if not isinstance(item, dict):
            errors.append("chronology record must be an object")
            continue
        event_id, stage, commit, purpose, anchor_specs = spec
        require_exact_keys(errors, item, CHRONOLOGY_RECORD_KEYS, f"chronology[{event_id}]")
        validate_anchor_keys(errors, item.get("anchors"), f"chronology[{event_id}].anchors")
        add_error(errors, item.get("event_id") == event_id, f"chronology[{event_id}].event_id mismatch")
        add_error(errors, item.get("stage") == stage, f"chronology[{event_id}].stage mismatch")
        add_error(errors, item.get("commit") == commit, f"chronology[{event_id}].commit mismatch")
        try:
            committed_subject = git_commit_subject(commit)
        except Exception as exc:  # pragma: no cover - diagnostic boundary
            errors.append(f"chronology[{event_id}] cannot resolve commit: {exc}")
            committed_subject = ""
        add_error(errors, item.get("subject") == committed_subject, f"chronology[{event_id}].subject mismatch")
        add_error(errors, item.get("purpose") == purpose, f"chronology[{event_id}].purpose mismatch")
        add_error(errors, item.get("claim_type") == "PROCESS_EVIDENCE", f"chronology[{event_id}] authority mismatch")
        add_error(errors, item.get("scientific_truth") is False and item.get("runtime_truth") is False, f"chronology[{event_id}] truth promotion")
        add_error(errors, item.get("anchors") == expected_anchors(anchor_specs, lines_by_path), f"chronology[{event_id}].anchors mismatch")
        for anchor_item in item.get("anchors", []):
            if isinstance(anchor_item, dict) and isinstance(anchor_item.get("path"), str):
                referenced_paths.add(anchor_item["path"])

    contradictions = data.get("contradictions")
    add_error(errors, isinstance(contradictions, list), "contradictions must be a list")
    if not isinstance(contradictions, list):
        contradictions = []
    contradiction_ids = [item.get("contradiction_id") for item in contradictions if isinstance(item, dict)]
    expected_contradiction_ids = [spec["contradiction_id"] for spec in module.CONTRADICTION_SPECS]
    add_error(errors, contradiction_ids == expected_contradiction_ids, "contradiction identity/order mismatch")
    required_contradiction_ids = [
        item["contradiction_id"] for item in REQUIRED_CONTRADICTION_OBLIGATIONS
    ]
    add_error(
        errors,
        contradiction_ids == required_contradiction_ids,
        "contradiction obligation identities mismatch",
    )
    contradiction_unrouted: list[str] = []
    for item, spec in zip(contradictions, module.CONTRADICTION_SPECS):
        if not isinstance(item, dict):
            errors.append("contradiction record must be an object")
            continue
        contradiction_id = spec["contradiction_id"]
        require_exact_keys(
            errors,
            item,
            CONTRADICTION_RECORD_KEYS,
            f"contradictions[{contradiction_id}]",
        )
        positions_value = item.get("positions")
        if not isinstance(positions_value, list):
            errors.append(f"contradictions[{contradiction_id}].positions must be a list")
        else:
            for position_index, position_value in enumerate(positions_value):
                context = f"contradictions[{contradiction_id}].positions[{position_index}]"
                if require_exact_keys(
                    errors,
                    position_value,
                    CONTRADICTION_POSITION_KEYS,
                    context,
                ):
                    validate_anchor_keys(errors, position_value.get("anchors"), f"{context}.anchors")
        for key in ("contradiction_id", "title", "status", "route", "adjudication"):
            add_error(errors, item.get(key) == spec[key], f"contradictions[{contradiction_id}].{key} mismatch")
        if not item.get("route"):
            contradiction_unrouted.append(contradiction_id)
        expected_positions = []
        for position in spec["positions"]:
            expected_positions.append({"position": position["position"], "anchors": expected_anchors(position["anchors"], lines_by_path)})
        add_error(errors, item.get("positions") == expected_positions, f"contradictions[{contradiction_id}].positions mismatch")
        for position in item.get("positions", []):
            for anchor_item in position.get("anchors", []):
                if isinstance(anchor_item, dict) and isinstance(anchor_item.get("path"), str):
                    referenced_paths.add(anchor_item["path"])

    contradiction_by_id = {
        item.get("contradiction_id"): item for item in contradictions if isinstance(item, dict)
    }
    for obligation in REQUIRED_CONTRADICTION_OBLIGATIONS:
        contradiction_id = obligation["contradiction_id"]
        item = contradiction_by_id.get(contradiction_id)
        if item is None:
            continue
        add_error(errors, item.get("route") == obligation["route"], f"contradiction obligation[{contradiction_id}].route mismatch")
        positions = item.get("positions", [])
        add_error(errors, len(positions) == len(obligation["position_anchors"]), f"contradiction obligation[{contradiction_id}].position count mismatch")
        for index, anchor_specs in enumerate(obligation["position_anchors"]):
            if index >= len(positions) or not isinstance(positions[index], dict):
                continue
            add_error(
                errors,
                positions[index].get("position") == obligation["position_names"][index],
                f"contradiction obligation[{contradiction_id}].position[{index}] name mismatch",
            )
            add_error(
                errors,
                positions[index].get("anchors") == expected_anchors(anchor_specs, lines_by_path),
                f"contradiction obligation[{contradiction_id}].position[{index}] anchors mismatch",
            )

    unresolved = data.get("unresolved_queue")
    add_error(errors, isinstance(unresolved, list), "unresolved_queue must be a list")
    if not isinstance(unresolved, list):
        unresolved = []
    unresolved_ids = [item.get("unresolved_id") for item in unresolved if isinstance(item, dict)]
    expected_unresolved_ids = [spec["unresolved_id"] for spec in module.UNRESOLVED_SPECS]
    add_error(errors, unresolved_ids == expected_unresolved_ids, "unresolved identity/order mismatch")
    required_unresolved_ids = [item["unresolved_id"] for item in REQUIRED_UNRESOLVED_OBLIGATIONS]
    add_error(
        errors,
        unresolved_ids == required_unresolved_ids,
        "unresolved obligation identities mismatch",
    )
    for item, spec in zip(unresolved, module.UNRESOLVED_SPECS):
        if not isinstance(item, dict):
            errors.append("unresolved record must be an object")
            continue
        unresolved_id = spec["unresolved_id"]
        require_exact_keys(errors, item, UNRESOLVED_RECORD_KEYS, f"unresolved[{unresolved_id}]")
        validate_anchor_keys(errors, item.get("anchors"), f"unresolved[{unresolved_id}].anchors")
        for key in ("unresolved_id", "item", "route"):
            add_error(errors, item.get(key) == spec[key], f"unresolved[{unresolved_id}].{key} mismatch")
        add_error(errors, item.get("anchors") == expected_anchors(spec["anchors"], lines_by_path), f"unresolved[{unresolved_id}].anchors mismatch")
        for anchor_item in item.get("anchors", []):
            if isinstance(anchor_item, dict) and isinstance(anchor_item.get("path"), str):
                referenced_paths.add(anchor_item["path"])

    unresolved_by_id = {
        item.get("unresolved_id"): item for item in unresolved if isinstance(item, dict)
    }
    for obligation in REQUIRED_UNRESOLVED_OBLIGATIONS:
        unresolved_id = obligation["unresolved_id"]
        item = unresolved_by_id.get(unresolved_id)
        if item is None:
            continue
        add_error(errors, item.get("item") == EXPECTED_UNRESOLVED_ITEM_TEXT[unresolved_id], f"unresolved obligation[{unresolved_id}].item mismatch")
        add_error(errors, item.get("route") == obligation["route"], f"unresolved obligation[{unresolved_id}].route mismatch")
        add_error(
            errors,
            item.get("anchors") == expected_anchors(obligation["anchors"], lines_by_path),
            f"unresolved obligation[{unresolved_id}].anchors mismatch",
        )

    authority_decisions = data.get("authority_decisions")
    add_error(errors, isinstance(authority_decisions, list), "authority_decisions must be a list")
    if isinstance(authority_decisions, list):
        for index, decision in enumerate(authority_decisions):
            require_exact_keys(
                errors,
                decision,
                AUTHORITY_DECISION_KEYS,
                f"authority_decisions[{index}]",
            )
    add_error(errors, authority_decisions == EXPECTED_AUTHORITY_DECISIONS, "authority_decisions mismatch")
    aut005_scope = ""
    if isinstance(authority_decisions, list):
        aut005 = next(
            (
                item
                for item in authority_decisions
                if isinstance(item, dict) and item.get("decision_id") == "AUT-005"
            ),
            None,
        )
        if isinstance(aut005, dict):
            aut005_scope = str(aut005.get("scope", ""))
    scope_match = re.fullmatch(
        r"All (\w+) recorded authority conflicts retain both positions and explicit downstream routes\.",
        aut005_scope,
    )
    scope_count = {"six": 6}.get(scope_match.group(1)) if scope_match else None
    add_error(
        errors,
        scope_count == len(REQUIRED_CONTRADICTION_OBLIGATIONS) == len(contradictions),
        "AUT-005 scope count does not match contradiction obligation manifest",
    )

    mandatory_paths = {spec[0] for spec in module.PROCESS_SOURCES + module.RELEASE_SOURCES}
    source_orphans = sorted(mandatory_paths - referenced_paths)
    defect_correction_orphans = sorted(set(required_defect_correction_ids) - set(defect_correction_ids))
    unresolved_obligation_orphans = sorted(set(required_unresolved_ids) - set(unresolved_ids))
    contradiction_obligation_orphans = sorted(set(required_contradiction_ids) - set(contradiction_ids))
    duplicate_claim_count = len(claim_ids) - len(set(claim_ids))
    gate_summary = data.get("gate_summary")
    expected_gate_summary = {
        "source_orphans": source_orphans,
        "source_orphan_count": len(source_orphans),
        "defect_correction_orphans": defect_correction_orphans,
        "defect_correction_orphan_count": len(defect_correction_orphans),
        "unresolved_obligation_orphans": unresolved_obligation_orphans,
        "unresolved_obligation_orphan_count": len(unresolved_obligation_orphans),
        "contradiction_obligation_orphans": contradiction_obligation_orphans,
        "contradiction_obligation_orphan_count": len(contradiction_obligation_orphans),
        "duplicate_claim_identity_count": duplicate_claim_count,
        "unsupported_authority_promotions": unsupported_promotions,
        "unsupported_authority_promotion_count": len(unsupported_promotions),
        "contradiction_unrouted": contradiction_unrouted,
        "contradiction_unrouted_count": len(contradiction_unrouted),
        "scientific_claims_promoted": 0,
        "runtime_claims_promoted": 0,
        "next_step": 42,
    }
    require_exact_keys(errors, gate_summary, GATE_SUMMARY_KEYS, "gate_summary")
    add_error(errors, gate_summary == expected_gate_summary, "gate_summary mismatch")
    add_error(errors, not source_orphans, f"source/process orphans: {source_orphans}")
    add_error(errors, not defect_correction_orphans, f"defect/correction obligation orphans: {defect_correction_orphans}")
    add_error(errors, not unresolved_obligation_orphans, f"unresolved obligation orphans: {unresolved_obligation_orphans}")
    add_error(errors, not contradiction_obligation_orphans, f"contradiction obligation orphans: {contradiction_obligation_orphans}")
    add_error(errors, not unsupported_promotions, f"unsupported authority promotions: {unsupported_promotions}")
    add_error(errors, not contradiction_unrouted, f"unrouted contradictions: {contradiction_unrouted}")

    return errors


def run_negative_mutations(data: dict[str, Any], module: Any) -> list[str]:
    failures: list[str] = []

    def expect(name: str, mutated: dict[str, Any], needle: str) -> None:
        errors = validate_data(mutated, module)
        if not any(needle in error for error in errors):
            failures.append(f"{name}: expected diagnostic containing {needle!r}, got {errors!r}")
        else:
            print(f"{name}: PASS_EXPECTED_FAILURE diagnostic={needle}")

    mutated = copy.deepcopy(data)
    mutated["sources"][0]["path"] += ".mutated"
    expect("altered_source_path", mutated, "sources: path order/set mismatch")

    mutated = copy.deepcopy(data)
    mutated["sources"][0]["sha256"] = "0" * 64
    expect("altered_source_hash", mutated, ".sha256 mismatch")

    mutated = copy.deepcopy(data)
    mutated["sources"][0]["read_coverage"][0]["end_line"] -= 1
    expect("skipped_source_line", mutated, ".read_coverage mismatch")

    mutated = copy.deepcopy(data)
    mutated["sources"].pop()
    expect("missing_source_record", mutated, "sources: path order/set mismatch")

    mutated = copy.deepcopy(data)
    mutated["claims"].append(copy.deepcopy(mutated["claims"][0]))
    expect("duplicate_claim_identity", mutated, "duplicate claim identities")

    mutated = copy.deepcopy(data)
    mutated["claims"][0]["unexpected_quality_field"] = "must be rejected"
    expect("extra_claim_field", mutated, "claims[CLM-001] key schema mismatch")

    mutated = copy.deepcopy(data)
    mutated["sources"][0]["authority_boundary"] = "Arbitrary nonempty text that implies scientific authority."
    expect(
        "misleading_source_authority_boundary",
        mutated,
        ".authority_boundary mismatch",
    )

    mutated = copy.deepcopy(data)
    target = next(claim for claim in mutated["claims"] if claim["claim_type"] == "SCIENTIFIC_CLAIM")
    target["authority_decision"] = "PROMOTED_COMPLETE"
    expect("unsupported_authority_promotion", mutated, "unsupported authority promotion")

    mutated = copy.deepcopy(data)
    mutated["contradictions"][0]["route"] = []
    expect("unrouted_contradiction", mutated, "unrouted contradictions")

    mutated = copy.deepcopy(data)
    mutated["defect_correction_records"] = [
        item for item in mutated["defect_correction_records"] if item["obligation_id"] != "DCR-CU-05"
    ]
    expect("missing_cu_defect_correction", mutated, "defect/correction obligation identities mismatch")

    mutated = copy.deepcopy(data)
    mutated["unresolved_queue"] = [
        item for item in mutated["unresolved_queue"] if item["unresolved_id"] != "UNR-009"
    ]
    expect("missing_unresolved_obligation", mutated, "unresolved obligation identities mismatch")

    mutated = copy.deepcopy(data)
    mutated["contradictions"] = [
        item for item in mutated["contradictions"] if item["contradiction_id"] != "CTR-005"
    ]
    expect("missing_severity_contradiction", mutated, "contradiction obligation identities mismatch")

    mutated = copy.deepcopy(data)
    aut005 = next(
        item for item in mutated["authority_decisions"] if item["decision_id"] == "AUT-005"
    )
    aut005["scope"] = "All four recorded authority conflicts retain both positions and explicit downstream routes."
    expect(
        "stale_authority_conflict_count",
        mutated,
        "AUT-005 scope count does not match contradiction obligation manifest",
    )

    try:
        strict_json_loads('{"duplicate": 1, "duplicate": 2}')
    except DuplicateKeyError:
        print("duplicate_json_key: PASS_EXPECTED_FAILURE diagnostic=duplicate key")
    else:
        failures.append("duplicate_json_key: strict parser accepted duplicate keys")

    return failures


def deterministic_regeneration(artifact_bytes: bytes) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="p060_step41_") as temp_dir:
        output = Path(temp_dir) / "matrix.json"
        proc = subprocess.run(
            [sys.executable, str(BUILDER), "--output", str(output)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode != 0:
            return [f"builder regeneration failed exit={proc.returncode}: {proc.stderr.strip()}"]
        regenerated = output.read_bytes()
        if regenerated != artifact_bytes:
            return [
                "builder regeneration bytes mismatch "
                f"stored={hashlib.sha256(artifact_bytes).hexdigest()} regenerated={hashlib.sha256(regenerated).hexdigest()}"
            ]
        print(f"PASS_BUILDER_REGENERATION {hashlib.sha256(regenerated).hexdigest()}")
    return []


def main() -> int:
    if not ARTIFACT.is_file():
        print("FAIL missing_artifact: Codex/results/PHASE_060_V1019_PROCESS_INTENT_MATRIX.json")
        print("FAIL_P060_STEP41_PROCESS_AUTHORITY 0/1")
        return 2
    try:
        artifact_bytes = ARTIFACT.read_bytes()
        data = strict_json_loads(artifact_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, DuplicateKeyError, NonFiniteNumberError) as exc:
        print(f"FAIL invalid_artifact_json: {exc}")
        print("FAIL_P060_STEP41_PROCESS_AUTHORITY 0/1")
        return 1

    module = load_builder_module()
    errors = validate_data(data, module)
    errors.extend(deterministic_regeneration(artifact_bytes))
    if not errors:
        errors.extend(run_negative_mutations(data, module))
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print("FAIL_P060_STEP41_PROCESS_AUTHORITY 0/1")
        return 1

    def walk(value: Any, depth: int = 0) -> tuple[int, int, int]:
        value_nodes = 1
        key_nodes = 0
        max_depth = depth
        if isinstance(value, dict):
            key_nodes += len(value)
            for child in value.values():
                child_values, child_keys, child_depth = walk(child, depth + 1)
                value_nodes += child_values
                key_nodes += child_keys
                max_depth = max(max_depth, child_depth)
        elif isinstance(value, list):
            for child in value:
                child_values, child_keys, child_depth = walk(child, depth + 1)
                value_nodes += child_values
                key_nodes += child_keys
                max_depth = max(max_depth, child_depth)
        return value_nodes, key_nodes, max_depth

    value_nodes, key_nodes, max_depth = walk(data)
    print("PASS_SOURCE_CONTRACT process=11/1028/889 release=5/550/480 witness=1/37/34")
    print("PASS_AUTHORITY_GATES orphans=0 promotions=0 contradictions_unrouted=0")
    print("PASS_SEVERITY_ENUMERATION ch1=3/7/3/10/1 ch2=1/5/1/4")
    print("PASS_OBLIGATION_COMPLETENESS defect_corrections=10 unresolved=11 contradictions=6")
    print("PASS_NEGATIVE_MUTATIONS 14/14")
    print(
        "PASS_STRICT_JSON "
        f"lines={len(artifact_bytes.decode('utf-8').splitlines())} value_nodes={value_nodes} "
        f"key_nodes={key_nodes} total_nodes={value_nodes + key_nodes} max_depth={max_depth} duplicate_keys=0"
    )
    print("PASS_P060_STEP41_PROCESS_AUTHORITY 1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
