#!/usr/bin/env python3
"""Validate Phase 061 Step 50 review/artifact evidence and checkpoint."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "b52435504b527d911b51470268e3879824bd6362"
EXPECTED_SUBJECT = "audit(phase061): adjudicate v1020 review artifacts"
EXPECTED_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
EXPECTED_PROTECTED = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
EXPECTED_MAIN = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"

BUILDER = REPO / "Codex/work/v1020_phase061/audit_phase061_step50_review_artifacts.py"
MATRIX = REPO / "Codex/results/PHASE_061_V1020_REVIEW_ARTIFACT_MATRIX.json"
VISUAL = REPO / "Codex/results/PHASE_061_V1020_VISUAL_READ_ATTESTATION.json"
RESULT = REPO / "Codex/results/PHASE_061_STEP_050_REVIEW_ARTIFACT_RESULT.md"
TOPOLOGY = REPO / "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json"
READ_ATTESTATION = REPO / "Codex/results/PHASE_061_V1020_READ_ATTESTATION.json"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

EXACT_EIGHT = (
    BUILDER.relative_to(REPO).as_posix(),
    Path(__file__).relative_to(REPO).as_posix(),
    MATRIX.relative_to(REPO).as_posix(),
    VISUAL.relative_to(REPO).as_posix(),
    RESULT.relative_to(REPO).as_posix(),
    ACTIVE_LEDGER.relative_to(REPO).as_posix(),
    PARENT_LEDGER.relative_to(REPO).as_posix(),
    HANDOVER.relative_to(REPO).as_posix(),
)

EXPECTED_MATRIX_KEYS = {
    "schema_version", "artifact_kind", "generated_date", "phase", "step",
    "baseline_commit", "status", "gate", "authority_boundary", "input_artifacts",
    "full_read_records", "adopted_source_references", "competitive_source_records",
    "content_adoption_edges", "p7_review_triage", "figure_candidates",
    "candidate_render_edges", "figure_genealogy_routes", "review_count_claims", "visual_attestation",
    "review_findings", "ground_not_found", "unverified_queue", "counts",
    "required_negative_controls", "builder",
}

EXPECTED_NEGATIVE_MANIFEST = (
    "SKIPPED_IMAGE_OCCURRENCE", "MISSING_PDF_PAGE", "FALSE_V1020_FIGURE_ADOPTION",
    "REVIEW_COUNT_INFLATION", "GENERATED_AS_EXPERIMENT", "VISUAL_PASS_AS_NUMERIC_VALIDITY",
    "DROPPED_COMPETITIVE_SOURCE", "FIGURE_CANDIDATE_COUNT", "CANDIDATE_RENDER_COUNT",
    "BROKEN_GENEALOGY_ROUTE", "Q2_Q3_FALSE_ADOPTION", "CONTENT_ADOPTION_WITHOUT_JUDGMENT",
    "PACKAGED_PNG_FALSE_INCLUDE", "GROUND_NOT_FOUND_REMOVED", "UNVERIFIED_REMOVED",
    "EXTERNAL_PROMOTION", "STRICT_JSON_DUPLICATE_KEY", "STRICT_JSON_NONFINITE",
    "PERSISTED_REBUILD_MISMATCH", "TWO_RUN_MISMATCH",
)
EXPECTED_GENEALOGY_STATES: dict[str, tuple[str, str, str]] = {
    **{f"FF1-{number}": ("UNVERIFIED", "UNVERIFIED", "P061-STEP50-GNF-007") for number in range(1, 8)},
    **{f"FF2-{number}": ("GNF", "UNVERIFIED", "P061-STEP50-GNF-005") for number in range(1, 6)},
    **{f"FF3-{number}": ("UNVERIFIED", "UNVERIFIED", "P061-STEP50-GNF-007") for number in range(1, 8)},
    **{f"FO1-{number}": ("GNF", "GNF", "P061-STEP50-GNF-007") for number in range(1, 5)},
    **{f"FO2-{number}": ("GNF", "GNF", "P061-STEP50-GNF-007") for number in range(1, 5)},
    **{f"FO3-{number}": ("PARTIAL", "PARTIAL", "P061-STEP50-GNF-007") for number in range(1, 5)},
}
EXPECTED_GENEALOGY_STATES["FF1-2"] = ("PARTIAL", "PARTIAL", "P061-STEP50-GNF-003")
EXPECTED_GENEALOGY_STATES["FF3-2"] = ("PARTIAL", "PARTIAL", "P061-STEP50-GNF-006")
EXPECTED_GENEALOGY_STATES["FF3-7"] = ("CONTRADICTED", "CONTRADICTED", "P061-STEP50-GNF-007")

# Filled from the final builder outputs.  Each top-level semantic section is
# pinned independently so a mutation receives a local identity diagnostic.
EXPECTED_MATRIX_SECTION_SHA: dict[str, str] = {
    "adopted_source_references": "829682b538a8fb731736aa83d6834a7712c59d013cfc7a537899e9679a96ccca",
    "artifact_kind": "6fdd166cac2b24a3c5e5de0d69deaccd156fcd0db313798ed3fe55c126db76c4",
    "authority_boundary": "6b5c8983a34914a106a2611158eb07cf534cdccadcd465b3fff2d01172e6cb9b",
    "baseline_commit": "31cf6635c1edae29e4d3773115b4f48391f0fd253a5077126173e1d1571aa805",
    "builder": "fa4a4a2b4e185dadee87bd59e0a8af601a975ee785ac901f7c3906215d4f1254",
    "candidate_render_edges": "76c005fc66f92bad4025c0e09950a5abb4e169e8bc272f314c437f79e0bcb5ae",
    "competitive_source_records": "a2ad4303d680db2a688a92c60d019481fffcafec63e2efa11e690ea687aa407f",
    "content_adoption_edges": "1d3cb95caaf678af72218b8da265825ba04450c44c1e95a3988b7b13521c175b",
    "counts": "00dabf81c9dee7d3baa1a5b136b8f52f9b331030d7f8150f8fac0d9779953741",
    "figure_candidates": "e9c7c7edd9754da3d3ca70ebcf9bc0ad9702f78f72814e2b80ee8651e1ff899e",
    "figure_genealogy_routes": "3ef935f9bdea753981e3bb01b29101e8837016516c7a48c96fbbe789704a115d",
    "full_read_records": "33c88da1a7e103917bb3bc1c9acd947c75a9a1f171e86fa7e463173d3d5ac075",
    "gate": "dff7a42158530ea5ac412b96b319a62e2f3aa7e96794e02089f14ab3ff41d0cf",
    "generated_date": "3c5c024bfbf28f2278009c954a814591dce05aa69520636f18dac76cf6b8089c",
    "ground_not_found": "253c8e17d38084699d232b5c9451035a232807a2fced1a69812efe44237f1370",
    "input_artifacts": "f4f743eb5e9d297cba4fd9d3e2a4cc443cb9113a83ea2e9d33b80a49e12e55f3",
    "p7_review_triage": "5dccddd89872a4861f8379804435a05e3c412e1ea4647c75df98706373ffd53e",
    "phase": "2a62cf402cd3396aa00f55f892f4545f308f74d01c8caa0f2837b1982f821595",
    "required_negative_controls": "cd33fce1b7b7e911bc3e82f687345849c7591466c81a75746b03d80691693e16",
    "review_count_claims": "2078f0a1c6451b54adafe4d2e95b5c1432d01bbd081b679bd904ae622665faad",
    "review_findings": "f9749392e59d7a49fb2a44052f072e3c9b6f80a990d8e51f7fd89bc47a933b6e",
    "schema_version": "9527f63c90435298923228633f5f53d97abff9f9187fa05fedcf361d3b0068b3",
    "status": "648df5ee863de7ed2225a908d0684c0c3070febe00c54b05ad03dce6291ab07a",
    "step": "7ea9844ae84eccbf55e8330640865e36c43521e45a1baec24233327aab7e6595",
    "unverified_queue": "c00b7a16f66f430e95de44696c46824103d5db660daa0f5d519c941d09a06760",
    "visual_attestation": "1755045ef8b5e8e32efc450153d6cac100e3231603747e32ed3275bcf8a4eec5",
}
EXPECTED_VISUAL_SECTION_SHA: dict[str, str] = {
    "artifact_kind": "1276f8497b1f20a7de7751d1f0990b9b2090c7b3762248463c81060a07f0c1cf",
    "authority_boundary": "7504aebcc23f67df1f0e8fc500f7f24f316af00f913919d934a6151a8bf2de47",
    "baseline_commit": "31cf6635c1edae29e4d3773115b4f48391f0fd253a5077126173e1d1571aa805",
    "counts": "325276bdc5afce05df267c0f0c8d7e9ea736fdb65574fc38df1e749e59897ff7",
    "generated_date": "3c5c024bfbf28f2278009c954a814591dce05aa69520636f18dac76cf6b8089c",
    "image_occurrences": "e15dfc9c8d628630bf9789a3d98df01282b177a426bb3fc6871e12b43cfe1270",
    "method": "c3d69243124cfd759abf6ece7ba77a3e678b1c67bcbad55cac3a2c1334d1934c",
    "pdf_occurrences": "708e9689f3a3060cff09350a27a4bf0a450097f55846b8ed900f8bf6b7eaebe7",
    "phase": "2a62cf402cd3396aa00f55f892f4545f308f74d01c8caa0f2837b1982f821595",
    "schema_version": "f3f7f1692237278576c65146ec85288abdc3c1a479b8ed9dc9c96433e18960db",
    "status": "648df5ee863de7ed2225a908d0684c0c3070febe00c54b05ad03dce6291ab07a",
    "step": "7ea9844ae84eccbf55e8330640865e36c43521e45a1baec24233327aab7e6595",
}
EXPECTED_BUILDER_AST_SHA = "f36384c8ac6928ebabe32196cb3a16306f1e32bd1c54376662cecc62513241ca"
EXPECTED_VISUAL_KEYS = {
    "schema_version", "artifact_kind", "generated_date", "phase", "step",
    "baseline_commit", "status", "authority_boundary", "method", "image_occurrences",
    "pdf_occurrences", "counts",
}


class ValidationError(RuntimeError):
    pass


def reject_constant(value: str) -> None:
    raise ValidationError(f"nonfinite JSON constant: {value}")


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValidationError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_json(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_pairs,
        parse_constant=reject_constant,
    )


def canonical_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def semantic_sha(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def run_git(*args: str, check: bool = True) -> str:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", check=False, timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationError(f"git {' '.join(args)} timed out") from exc
    if check and proc.returncode != 0:
        raise ValidationError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def walk_finite(value: Any) -> int:
    count = 1
    if isinstance(value, float) and not math.isfinite(value):
        raise ValidationError("nonfinite value in object")
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValidationError("non-string JSON key")
            count += walk_finite(child)
    elif isinstance(value, list):
        for child in value:
            count += walk_finite(child)
    elif value is not None and not isinstance(value, (str, int, float, bool)):
        raise ValidationError(f"unsupported JSON type {type(value).__name__}")
    return count


def canonical_ast_node(node: Any) -> Any:
    if isinstance(node, ast.AST):
        return {
            "type": type(node).__name__,
            "fields": [[field, canonical_ast_node(getattr(node, field))] for field in node._fields],
        }
    if isinstance(node, list):
        return [canonical_ast_node(item) for item in node]
    if isinstance(node, bytes):
        return {"type": "bytes", "hex": node.hex()}
    if isinstance(node, (str, int, float, complex, bool)) or node is None:
        return node
    raise ValidationError(f"unsupported AST value {type(node).__name__}")


def builder_security_diagnostics() -> list[str]:
    diagnostics: list[str] = []
    source = BUILDER.read_text(encoding="utf-8")
    tree = ast.parse(source)
    allowed = {
        "argparse", "hashlib", "json", "math", "re", "subprocess", "sys",
        "collections", "pathlib", "typing", "__future__",
    }
    imports: set[str] = set()
    subprocess_calls: list[ast.Call] = []
    banned_calls = {"eval", "exec", "compile", "__import__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add((node.module or "").split(".")[0])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in banned_calls:
                diagnostics.append("BUILDER_SECURITY")
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if node.func.value.id == "subprocess" and node.func.attr == "run":
                    subprocess_calls.append(node)
    if imports - allowed:
        diagnostics.append("BUILDER_SECURITY")
    if len(subprocess_calls) != 1:
        diagnostics.append("BUILDER_SUBPROCESS_CONTRACT")
    else:
        call = subprocess_calls[0]
        if not call.args or not isinstance(call.args[0], (ast.List, ast.Tuple)):
            diagnostics.append("BUILDER_SUBPROCESS_CONTRACT")
        else:
            values = [elt.value for elt in call.args[0].elts if isinstance(elt, ast.Constant)]
            if values != ["git", "cat-file", "--batch"]:
                diagnostics.append("BUILDER_SUBPROCESS_CONTRACT")
    if semantic_sha(canonical_ast_node(tree)) != EXPECTED_BUILDER_AST_SHA:
        diagnostics.append("BUILDER_AST")
    return sorted(set(diagnostics))


def section_identity_diagnostics(matrix: dict[str, Any], visual: dict[str, Any]) -> list[str]:
    diagnostics: list[str] = []
    if set(EXPECTED_MATRIX_SECTION_SHA) != set(EXPECTED_MATRIX_KEYS):
        diagnostics.append("PINNED_MATRIX_SCHEMA")
    else:
        for key in sorted(EXPECTED_MATRIX_KEYS):
            if semantic_sha(matrix.get(key)) != EXPECTED_MATRIX_SECTION_SHA[key]:
                diagnostics.append(f"MATRIX_{key.upper()}_IDENTITY")
    if set(EXPECTED_VISUAL_SECTION_SHA) != set(EXPECTED_VISUAL_KEYS):
        diagnostics.append("PINNED_VISUAL_SCHEMA")
    else:
        for key in sorted(EXPECTED_VISUAL_KEYS):
            if semantic_sha(visual.get(key)) != EXPECTED_VISUAL_SECTION_SHA[key]:
                diagnostics.append(f"VISUAL_{key.upper()}_IDENTITY")
    return sorted(set(diagnostics))


def provenance_diagnostics(matrix: dict[str, Any]) -> list[str]:
    diagnostics: list[str] = []
    expected_inputs = {
        path.relative_to(REPO).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (TOPOLOGY, READ_ATTESTATION,
                     REPO / "Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json",
                     REPO / "Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json",
                     REPO / "Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json")
    }
    found_inputs = {row.get("path"): row.get("sha256") for row in matrix.get("input_artifacts", [])}
    if found_inputs != expected_inputs:
        diagnostics.append("INPUT_ARTIFACT_IDENTITY")
    builder = matrix.get("builder", {})
    builder_sha_lf = hashlib.sha256(BUILDER.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    if (
        builder.get("path") != BUILDER.relative_to(REPO).as_posix()
        or builder.get("sha256_lf") != builder_sha_lf
        or builder.get("historical_production_imported") is not False
        or builder.get("historical_renderer_executed") is not False
        or builder.get("git_subprocess_contract")
        != "single git cat-file --batch invocation for selected frozen text, image, and PDF blobs"
    ):
        diagnostics.append("BUILDER_IDENTITY")
    return sorted(set(diagnostics))


def validate_content(matrix: dict[str, Any], visual: dict[str, Any]) -> list[str]:
    diagnostics: list[str] = []
    if set(matrix) != EXPECTED_MATRIX_KEYS or set(visual) != EXPECTED_VISUAL_KEYS:
        diagnostics.append("TOP_LEVEL_SCHEMA")
    if matrix.get("baseline_commit") != BASELINE or visual.get("baseline_commit") != BASELINE:
        diagnostics.append("BASELINE_IDENTITY")
    if matrix.get("phase") != 61 or matrix.get("step") != 50 or visual.get("phase") != 61 or visual.get("step") != 50:
        diagnostics.append("PHASE_STEP_IDENTITY")

    counts = matrix.get("counts", {})
    if counts.get("topology_sources") != 232:
        diagnostics.append("TOPOLOGY_SOURCE_COVERAGE")
    competitive = matrix.get("competitive_source_records", [])
    competitive_ids = [row.get("source_id") for row in competitive]
    competitive_indices = [row.get("manifest_index") for row in competitive]
    if len(competitive) != 126 or len(set(competitive_ids)) != 126 or sorted(competitive_indices) != list(range(95, 221)):
        diagnostics.append("COMPETITIVE_SOURCE_COVERAGE")
    if counts.get("competitive_occurrences") != len(competitive) or counts.get("competitive_text_sources") != 97:
        diagnostics.append("COMPETITIVE_SOURCE_COVERAGE")

    full_reads = matrix.get("full_read_records", [])
    if len(full_reads) != 104 or counts.get("full_read_source_union") != 104:
        diagnostics.append("FULL_READ_SOURCE_COVERAGE")
    if any(row.get("full_read_state") != "FULL_TEXT_1_TO_EOF" for row in full_reads):
        diagnostics.append("FULL_READ_SOURCE_COVERAGE")
    if len({row.get("source_id") for row in full_reads}) != len(full_reads):
        diagnostics.append("FULL_READ_SOURCE_COVERAGE")
    if len(matrix.get("adopted_source_references", [])) != 43:
        diagnostics.append("ADOPTED_SOURCE_REFERENCE_COVERAGE")

    content_edges = matrix.get("content_adoption_edges", [])
    if len(content_edges) != 7 or counts.get("content_adoption_edges") != 7:
        diagnostics.append("CONTENT_ADOPTION_EDGE_COVERAGE")
    for row in content_edges:
        if not row.get("judgment") or not row.get("target") or row.get("external_scientific_truth") is not False:
            diagnostics.append("CONTENT_ADOPTION_EDGE_COVERAGE")
            break

    triage = matrix.get("p7_review_triage", [])
    if [row.get("triage_id") for row in triage] != [f"T-{number:02d}" for number in range(1, 19)]:
        diagnostics.append("P7_TRIAGE_COVERAGE")
    if counts.get("p7_adopted_triage_rows") != 18:
        diagnostics.append("P7_TRIAGE_COVERAGE")

    candidates = matrix.get("figure_candidates", [])
    candidate_ids = [row.get("candidate_id") for row in candidates]
    if len(candidates) != 31 or len(set(candidate_ids)) != 31 or counts.get("figure_candidates") != 31:
        diagnostics.append("FIGURE_CANDIDATE_COVERAGE")
    if any(row.get("v1020_adopted_figure") is not False or row.get("v1020_tex_include_edge") is not None or row.get("v1020_generated_release_pdf_page_edge") is not None for row in candidates):
        diagnostics.append("FALSE_V1020_FIGURE_ADOPTION")
    if any(row.get("experimental_evidence_state") != "NOT_EVIDENCE" for row in candidates):
        diagnostics.append("GENERATED_AS_EXPERIMENT")
    render_edges = matrix.get("candidate_render_edges", [])
    if len(render_edges) != 31 or counts.get("candidate_render_edges") != 31:
        diagnostics.append("CANDIDATE_RENDER_EDGE_COVERAGE")
    render_candidate_ids = [row.get("candidate", {}).get("source_id") for row in render_edges]
    figure_source_ids = [row.get("candidate_source", {}).get("source_id") for row in candidates]
    if sorted(render_candidate_ids) != sorted(figure_source_ids):
        diagnostics.append("CANDIDATE_RENDER_EDGE_COVERAGE")
    if any(not row.get("harness") or not row.get("rendered_pdf") for row in render_edges):
        diagnostics.append("CANDIDATE_RENDER_EDGE_COVERAGE")

    genealogy = matrix.get("figure_genealogy_routes", [])
    genealogy_ids = [row.get("route_id") for row in genealogy]
    genealogy_candidate_ids = [row.get("candidate_id") for row in genealogy]
    if (
        len(genealogy) != 31 or len(set(genealogy_ids)) != 31
        or sorted(genealogy_candidate_ids) != sorted(candidate_ids)
        or counts.get("figure_genealogy_routes") != 31
    ):
        diagnostics.append("FIGURE_GENEALOGY_COVERAGE")
    for row in genealogy:
        if (
            not row.get("source_model_or_claim_records")
            or not row.get("candidate") or not row.get("renderer_harness")
            or not row.get("competitive_rendered_pdf") or not row.get("consolidated_judgment")
            or row.get("review_vote_records") != []
            or row.get("v1020_adopted_figure") is not None
            or row.get("v1020_tex_include") is not None
            or row.get("v1020_release_pdf_page") is not None
            or not row.get("missing_edges")
        ):
            diagnostics.append("FIGURE_GENEALOGY_COVERAGE")
            break
    candidate_by_id = {row.get("candidate_id"): row for row in candidates}
    render_by_candidate_source = {
        row.get("candidate", {}).get("source_id"): row for row in render_edges
    }
    if set(genealogy_candidate_ids) != set(EXPECTED_GENEALOGY_STATES):
        diagnostics.append("FIGURE_GENEALOGY_SEMANTICS")
    for row in genealogy:
        candidate_id = row.get("candidate_id")
        if candidate_id not in EXPECTED_GENEALOGY_STATES:
            continue
        expected_data, expected_generation, expected_route = EXPECTED_GENEALOGY_STATES[candidate_id]
        candidate_row = candidate_by_id.get(candidate_id, {})
        candidate_source = candidate_row.get("candidate_source", {})
        render_row = render_by_candidate_source.get(candidate_source.get("source_id"), {})
        data_records = row.get("source_data_records", [])
        generation_records = row.get("generation_records", [])
        model_records = row.get("source_model_or_claim_records", [])
        missing = row.get("missing_edges", [])
        if (
            row.get("candidate") != candidate_source
            or row.get("renderer_harness") != render_row.get("harness")
            or row.get("competitive_rendered_pdf") != render_row.get("rendered_pdf")
            or row.get("candidate_specific_data_link_state") != expected_data
            or row.get("candidate_specific_generation_link_state") != expected_generation
            or any(
                item.get("candidate_link_state") != "CONFIRMED"
                or item.get("relation_scope") != "FAMILY_COMPETITION_CONTEXT_NOT_NUMERIC_PROVENANCE"
                for item in model_records
            )
            or any(
                item.get("candidate_link_state") != expected_data
                or item.get("route") != expected_route
                or item.get("relation_scope") != "FAMILY_DATA_CONTEXT_CANDIDATE_LINK_ADJUDICATED_SEPARATELY"
                for item in data_records
            )
            or any(
                item.get("candidate_link_state") != expected_generation
                or item.get("route") != expected_route
                or item.get("relation_scope") != "FAMILY_GENERATION_CONTEXT_CANDIDATE_LINK_ADJUDICATED_SEPARATELY"
                for item in generation_records
            )
            or not any(item.get("route") == expected_route for item in missing)
        ):
            diagnostics.append("FIGURE_GENEALOGY_SEMANTICS")
            break

    q2q3 = [row for row in competitive if row.get("family") in {"comp_Q2_gcbalance", "comp_Q3_tst"}]
    if len(q2q3) != 16 or any(row.get("v1020_adoption_state") != "FORWARD_CANDIDATE_V1021_NOT_V1020" for row in q2q3):
        diagnostics.append("Q2_Q3_FALSE_ADOPTION")
    if counts.get("v1020_packaged_png_include_edges") != 0:
        diagnostics.append("PACKAGED_PNG_FALSE_INCLUDE")

    review_claims = matrix.get("review_count_claims", [])
    if [row.get("values") for row in review_claims] != [[4], [11], [6], [12]]:
        diagnostics.append("REVIEW_COUNT_INFLATION")
    expected_breakdown = {
        "chapter1_O_windows": 3, "chapter2_O_and_F_windows": 6,
        "partial_prior_F1": 1, "stream3_interchapter_report": 1,
    }
    if (
        len(review_claims) != 4 or review_claims[1].get("breakdown") != expected_breakdown
        or sum(expected_breakdown.values()) != 11
        or review_claims[1].get("separate_final_fable_pass") != 1
    ):
        diagnostics.append("REVIEW_COUNT_INFLATION")

    findings = matrix.get("review_findings", [])
    finding_ids = [row.get("id") for row in findings]
    if (
        len(findings) != 14 or len(set(finding_ids)) != 14
        or sum(row.get("priority") == "P1" for row in findings) != 3
        or sum(row.get("priority") == "P2" for row in findings) != 11
        or any(not row.get("finding") or not row.get("authority") for row in findings)
    ):
        diagnostics.append("REVIEW_FINDING_COVERAGE")

    images = visual.get("image_occurrences", [])
    image_ids = [row.get("source_id") for row in images]
    if len(images) != 23 or len(set(image_ids)) != 23 or visual.get("counts", {}).get("image_occurrences") != 23:
        diagnostics.append("IMAGE_OCCURRENCE_COVERAGE")
    if any(row.get("original_resolution_inspected") is not True or row.get("review_state") != "HUMAN_ORIGINAL_RESOLUTION_FULL" for row in images):
        diagnostics.append("IMAGE_OCCURRENCE_COVERAGE")
    if any(row.get("experimental_evidence_state") != "NOT_EVIDENCE" for row in images):
        diagnostics.append("GENERATED_AS_EXPERIMENT")
    if any(row.get("numeric_reproduction_state") != "UNVERIFIED_BY_VISUAL_REVIEW" for row in images):
        diagnostics.append("VISUAL_PASS_AS_NUMERIC_VALIDITY")

    pdfs = visual.get("pdf_occurrences", [])
    pages = [page for pdf in pdfs for page in pdf.get("pages", [])]
    if len(pdfs) != 14 or len({row.get("source_id") for row in pdfs}) != 14:
        diagnostics.append("PDF_OCCURRENCE_COVERAGE")
    if len(pages) != 130 or len({row.get("page_identity") for row in pages}) != 130 or visual.get("counts", {}).get("pdf_pages") != 130:
        diagnostics.append("PDF_PAGE_COVERAGE")
    if any(pdf.get("pages_expected") != pdf.get("pages_observed") or pdf.get("pages_observed") != len(pdf.get("pages", [])) for pdf in pdfs):
        diagnostics.append("PDF_PAGE_COVERAGE")
    if any(page.get("experimental_evidence_state") != "NOT_EVIDENCE" for page in pages):
        diagnostics.append("GENERATED_AS_EXPERIMENT")
    if any(page.get("numeric_reproduction_state") != "UNVERIFIED_BY_VISUAL_REVIEW" for page in pages):
        diagnostics.append("VISUAL_PASS_AS_NUMERIC_VALIDITY")
    if visual.get("counts", {}).get("blank_pages") != 0 or visual.get("counts", {}).get("render_failures") != 0:
        diagnostics.append("VISUAL_COMPLETENESS")

    if matrix.get("visual_attestation", {}).get("semantic_sha256") != semantic_sha(visual):
        diagnostics.append("VISUAL_MATRIX_LINK")
    boundary = matrix.get("authority_boundary", {})
    visual_boundary = visual.get("authority_boundary", {})
    if boundary.get("numerical_reproduction") is not False or boundary.get("material_or_experimental_validity") is not False:
        diagnostics.append("EVIDENCE_PROMOTION")
    if visual_boundary.get("numerical_validity") is not False or visual_boundary.get("experimental_evidence") is not False:
        diagnostics.append("EVIDENCE_PROMOTION")
    if counts.get("external_scientific_promotions") != 0 or counts.get("experimental_evidence_promotions") != 0:
        diagnostics.append("EVIDENCE_PROMOTION")
    if visual.get("counts", {}).get("numeric_validity_promotions") != 0 or visual.get("counts", {}).get("experimental_evidence_promotions") != 0:
        diagnostics.append("EVIDENCE_PROMOTION")
    if len(matrix.get("ground_not_found", [])) != 11:
        diagnostics.append("GROUND_NOT_FOUND_COVERAGE")
    if len(matrix.get("unverified_queue", [])) != 7:
        diagnostics.append("UNVERIFIED_QUEUE_COVERAGE")
    if tuple(matrix.get("required_negative_controls", [])) != EXPECTED_NEGATIVE_MANIFEST:
        diagnostics.append("NEGATIVE_MANIFEST")
    return sorted(set(diagnostics))


def strict_json_controls() -> list[str]:
    failures: list[str] = []
    for name, raw in {"duplicate": '{"a":1,"a":2}', "nonfinite": '{"a":NaN}'}.items():
        try:
            json.loads(raw, object_pairs_hook=reject_pairs, parse_constant=reject_constant)
        except ValidationError:
            continue
        failures.append(name)
    return failures


def negative_controls(matrix: dict[str, Any], visual: dict[str, Any]) -> list[tuple[str, list[str]]]:
    probes: list[tuple[str, dict[str, Any], dict[str, Any], str]] = []

    def fresh() -> tuple[dict[str, Any], dict[str, Any]]:
        return copy.deepcopy(matrix), copy.deepcopy(visual)

    m, v = fresh(); v["image_occurrences"].pop(); probes.append(("SKIPPED_IMAGE_OCCURRENCE", m, v, "IMAGE_OCCURRENCE_COVERAGE"))
    m, v = fresh(); v["pdf_occurrences"][0]["pages"].pop(); probes.append(("MISSING_PDF_PAGE", m, v, "PDF_PAGE_COVERAGE"))
    m, v = fresh(); m["figure_candidates"][0]["v1020_adopted_figure"] = True; probes.append(("FALSE_V1020_FIGURE_ADOPTION", m, v, "FALSE_V1020_FIGURE_ADOPTION"))
    m, v = fresh(); m["review_count_claims"][0]["values"] = [99]; probes.append(("REVIEW_COUNT_INFLATION", m, v, "REVIEW_COUNT_INFLATION"))
    m, v = fresh(); v["image_occurrences"][0]["experimental_evidence_state"] = "VALIDATED"; probes.append(("GENERATED_AS_EXPERIMENT", m, v, "GENERATED_AS_EXPERIMENT"))
    m, v = fresh(); v["pdf_occurrences"][0]["pages"][0]["numeric_reproduction_state"] = "VALIDATED"; probes.append(("VISUAL_PASS_AS_NUMERIC_VALIDITY", m, v, "VISUAL_PASS_AS_NUMERIC_VALIDITY"))
    m, v = fresh(); m["competitive_source_records"].pop(0); probes.append(("DROPPED_COMPETITIVE_SOURCE", m, v, "COMPETITIVE_SOURCE_COVERAGE"))
    m, v = fresh(); m["counts"]["figure_candidates"] = 30; probes.append(("FIGURE_CANDIDATE_COUNT", m, v, "FIGURE_CANDIDATE_COVERAGE"))
    m, v = fresh(); m["counts"]["candidate_render_edges"] = 30; probes.append(("CANDIDATE_RENDER_COUNT", m, v, "CANDIDATE_RENDER_EDGE_COVERAGE"))
    m, v = fresh(); m["figure_genealogy_routes"][0]["candidate_specific_data_link_state"] = "CONFIRMED"; probes.append(("BROKEN_GENEALOGY_ROUTE", m, v, "FIGURE_GENEALOGY_SEMANTICS"))
    m, v = fresh(); next(row for row in m["competitive_source_records"] if row["family"] == "comp_Q2_gcbalance")["v1020_adoption_state"] = "ADOPTED"; probes.append(("Q2_Q3_FALSE_ADOPTION", m, v, "Q2_Q3_FALSE_ADOPTION"))
    m, v = fresh(); m["content_adoption_edges"][0]["judgment"] = None; probes.append(("CONTENT_ADOPTION_WITHOUT_JUDGMENT", m, v, "CONTENT_ADOPTION_EDGE_COVERAGE"))
    m, v = fresh(); m["counts"]["v1020_packaged_png_include_edges"] = 1; probes.append(("PACKAGED_PNG_FALSE_INCLUDE", m, v, "PACKAGED_PNG_FALSE_INCLUDE"))
    m, v = fresh(); m["ground_not_found"].pop(); probes.append(("GROUND_NOT_FOUND_REMOVED", m, v, "GROUND_NOT_FOUND_COVERAGE"))
    m, v = fresh(); m["unverified_queue"].pop(); probes.append(("UNVERIFIED_REMOVED", m, v, "UNVERIFIED_QUEUE_COVERAGE"))
    m, v = fresh(); m["authority_boundary"]["numerical_reproduction"] = True; probes.append(("EXTERNAL_PROMOTION", m, v, "EVIDENCE_PROMOTION"))

    failures: list[tuple[str, list[str]]] = []
    for name, mutated_matrix, mutated_visual, expected in probes:
        mutated_matrix["visual_attestation"]["semantic_sha256"] = semantic_sha(mutated_visual)
        diagnostics = validate_content(mutated_matrix, mutated_visual)
        if diagnostics != [expected]:
            failures.append((name, diagnostics))
    return failures


def determinism_check() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="p061_step50_") as tmp:
        tmp_path = Path(tmp)
        outputs: list[tuple[bytes, bytes]] = []
        for run in range(2):
            matrix_out = tmp_path / f"matrix_{run}.json"
            visual_out = tmp_path / f"visual_{run}.json"
            proc = subprocess.run(
                [sys.executable, str(BUILDER), "--matrix-out", str(matrix_out), "--visual-out", str(visual_out)],
                cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                encoding="utf-8", errors="replace", check=False, timeout=120,
            )
            if proc.returncode != 0:
                failures.append(f"builder_run_{run}:{proc.stderr.strip()}")
                continue
            outputs.append((matrix_out.read_bytes(), visual_out.read_bytes()))
        if len(outputs) == 2:
            if outputs[0] != outputs[1]:
                failures.append("two_run_mismatch")
            if outputs[0][0] != MATRIX.read_bytes() or outputs[0][1] != VISUAL.read_bytes():
                failures.append("persisted_mismatch")
    return failures


def changed_paths() -> set[str]:
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain=v1", "-z"], cwd=REPO,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            encoding="utf-8", errors="replace", check=False, timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationError("git status --porcelain=v1 -z timed out") from exc
    if proc.returncode != 0:
        raise ValidationError(f"git status failed: {proc.stderr.strip()}")
    status = proc.stdout
    if not status:
        return set()
    entries = status.split("\x00")
    paths: set[str] = set()
    index = 0
    while index < len(entries) and entries[index]:
        entry = entries[index]
        code = entry[:2]
        paths.add(entry[3:].replace("\\", "/"))
        if "R" in code or "C" in code:
            index += 1
            if index < len(entries) and entries[index]:
                paths.add(entries[index].replace("\\", "/"))
        index += 1
    return paths


def nul_paths(*git_args: str) -> set[str]:
    raw = run_git(*git_args)
    return {path.replace("\\", "/") for path in raw.split("\x00") if path}


def live_remote_tip(branch: str) -> str:
    fields = run_git("ls-remote", "--heads", "origin", branch).split()
    return fields[0] if fields else ""


def precommit_checks() -> list[str]:
    diagnostics: list[str] = []
    if changed_paths() != set(EXACT_EIGHT):
        diagnostics.append("EXACT_EIGHT_DIRT")
    if nul_paths("diff", "--cached", "--name-only", "-z") != set(EXACT_EIGHT):
        diagnostics.append("EXACT_EIGHT_STAGED")
    diff_check = subprocess.run(
        ["git", "diff", "--check"], cwd=REPO,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=30,
    )
    if diff_check.returncode != 0:
        diagnostics.append("GIT_DIFF_CHECK")
    cached_diff_check = subprocess.run(
        ["git", "diff", "--cached", "--check"], cwd=REPO,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=30,
    )
    if cached_diff_check.returncode != 0:
        diagnostics.append("GIT_CACHED_DIFF_CHECK")
    if run_git("rev-parse", "HEAD") != EXPECTED_PARENT:
        diagnostics.append("PRECOMMIT_PARENT")
    if run_git("branch", "--show-current") != EXPECTED_BRANCH:
        diagnostics.append("ACTIVE_BRANCH_IDENTITY")
    if run_git("rev-parse", "--abbrev-ref", "@{u}") != f"origin/{EXPECTED_BRANCH}":
        diagnostics.append("ACTIVE_UPSTREAM_IDENTITY")
    if (
        run_git("rev-parse", "origin/codex/lib-physics-endgame-v1025_2") != EXPECTED_PROTECTED
        or live_remote_tip("codex/lib-physics-endgame-v1025_2") != EXPECTED_PROTECTED
    ):
        diagnostics.append("PROTECTED_BRANCH_DRIFT")
    if run_git("rev-parse", "origin/main") != EXPECTED_MAIN or live_remote_tip("main") != EXPECTED_MAIN:
        diagnostics.append("MAIN_BRANCH_DRIFT")
    result_text = RESULT.read_text(encoding="utf-8") if RESULT.is_file() else ""
    for token in ("PASS_WITH_CONCERNS_P061_STEP50_REVIEW_ARTIFACTS", EXPECTED_SUBJECT, "PENDING_AT_PRECOMMIT_BY_DESIGN"):
        if token not in result_text:
            diagnostics.append("RESULT_CONTRACT")
            break
    active_text = ACTIVE_LEDGER.read_text(encoding="utf-8") if ACTIVE_LEDGER.is_file() else ""
    parent_text = PARENT_LEDGER.read_text(encoding="utf-8") if PARENT_LEDGER.is_file() else ""
    handover_text = HANDOVER.read_text(encoding="utf-8") if HANDOVER.is_file() else ""
    if not all(token in active_text for token in ("Step 50", "PASS_WITH_CONCERNS_P061_STEP50_REVIEW_ARTIFACTS", "PENDING_AT_PRECOMMIT_BY_DESIGN")):
        diagnostics.append("ACTIVE_LEDGER_CONTRACT")
    if not all(token in parent_text for token in ("Steps 46–50", "PASS_WITH_CONCERNS_P061_STEP50_REVIEW_ARTIFACTS", "PENDING_AT_PRECOMMIT_BY_DESIGN")):
        diagnostics.append("PARENT_LEDGER_CONTRACT")
    if not all(token in handover_text for token in ("Phase 061 Step 50", "PASS_WITH_CONCERNS_P061_STEP50_REVIEW_ARTIFACTS", "PENDING_AT_PRECOMMIT_BY_DESIGN")):
        diagnostics.append("HANDOVER_CONTRACT")
    return sorted(set(diagnostics))


def persistence_checks() -> list[str]:
    diagnostics: list[str] = []
    head = run_git("rev-parse", "HEAD")
    if run_git("rev-parse", "HEAD^") != EXPECTED_PARENT:
        diagnostics.append("PERSISTENCE_PARENT")
    if run_git("show", "-s", "--format=%s", "HEAD") != EXPECTED_SUBJECT:
        diagnostics.append("PERSISTENCE_SUBJECT")
    files = set(run_git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines())
    if files != set(EXACT_EIGHT):
        diagnostics.append("PERSISTENCE_EXACT_EIGHT")
    if changed_paths():
        diagnostics.append("PERSISTENCE_DIRTY")
    upstream = run_git("rev-parse", "@{u}")
    live = live_remote_tip(EXPECTED_BRANCH)
    if not (head == upstream == live):
        diagnostics.append("PERSISTENCE_REMOTE")
    if run_git("branch", "--show-current") != EXPECTED_BRANCH or run_git("rev-parse", "--abbrev-ref", "@{u}") != f"origin/{EXPECTED_BRANCH}":
        diagnostics.append("ACTIVE_BRANCH_IDENTITY")
    if (
        run_git("rev-parse", "origin/codex/lib-physics-endgame-v1025_2") != EXPECTED_PROTECTED
        or live_remote_tip("codex/lib-physics-endgame-v1025_2") != EXPECTED_PROTECTED
    ):
        diagnostics.append("PROTECTED_BRANCH_DRIFT")
    if run_git("rev-parse", "origin/main") != EXPECTED_MAIN or live_remote_tip("main") != EXPECTED_MAIN:
        diagnostics.append("MAIN_BRANCH_DRIFT")
    if run_git("diff", "--name-only", "origin/codex/lib-physics-endgame-v1025_2...HEAD", "--", "Claude"):
        diagnostics.append("CLAUDE_TRACKED_DRIFT")
    if run_git("ls-files", "--others", "--exclude-standard", "--", "Claude"):
        diagnostics.append("CLAUDE_UNTRACKED_DRIFT")
    return sorted(set(diagnostics))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--persistence", action="store_true")
    args = parser.parse_args(argv)

    required = (BUILDER, MATRIX, VISUAL)
    missing = [path.relative_to(REPO).as_posix() for path in required if not path.is_file()]
    if missing:
        for path in missing:
            print(f"STEP50_MISSING_ARTIFACT {path}")
        print(f"FAIL_P061_STEP50_REVIEW_ARTIFACTS 0/{len(required)}")
        return 1
    try:
        matrix = load_json(MATRIX)
        visual = load_json(VISUAL)
        nodes = walk_finite(matrix) + walk_finite(visual)
        diagnostics = sorted(set(
            validate_content(matrix, visual)
            + section_identity_diagnostics(matrix, visual)
            + provenance_diagnostics(matrix)
            + builder_security_diagnostics()
        ))
        if diagnostics:
            for diagnostic in diagnostics:
                print(f"STEP50_{diagnostic}")
            print("FAIL_P061_STEP50_REVIEW_ARTIFACTS")
            return 1
        strict_failures = strict_json_controls()
        if strict_failures:
            print(f"STEP50_STRICT_JSON_FAILURES {strict_failures}")
            return 1
        if args.run_negative_probes:
            negative_failures = negative_controls(matrix, visual)
            if negative_failures:
                for name, found in negative_failures:
                    print(f"STEP50_NEGATIVE_FAILURE {name} {found}")
                return 1
            print("PASS_P061_STEP50_NEGATIVE_CONTROLS 16/16")
        if args.determinism_check:
            deterministic_failures = determinism_check()
            if deterministic_failures:
                print(f"STEP50_DETERMINISM_FAILURES {deterministic_failures}")
                return 1
            print("PASS_P061_STEP50_DETERMINISM 2/2")
        if args.persistence:
            persistence = persistence_checks()
            if persistence:
                for diagnostic in persistence:
                    print(f"STEP50_{diagnostic}")
                return 1
            print("PASS_P061_STEP50_PERSISTENCE")
        elif not args.content_only:
            required_precommit = (RESULT, ACTIVE_LEDGER, PARENT_LEDGER, HANDOVER)
            missing_precommit = [path.relative_to(REPO).as_posix() for path in required_precommit if not path.is_file()]
            if missing_precommit:
                for path in missing_precommit:
                    print(f"STEP50_MISSING_ARTIFACT {path}")
                return 1
            precommit = precommit_checks()
            if precommit:
                for diagnostic in precommit:
                    print(f"STEP50_{diagnostic}")
                return 1
            print("PASS_P061_STEP50_PRECOMMIT")
        print(f"PASS_P061_STEP50_REVIEW_ARTIFACTS nodes={nodes} competitive=126 figures=31 images=23 pdf=14/130")
        print("PASS_WITH_CONCERNS_P061_STEP50_REVIEW_ARTIFACTS")
        return 0
    except (ValidationError, OSError, UnicodeError, ValueError, KeyError, TypeError, IndexError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL_P061_STEP50_VALIDATOR {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
