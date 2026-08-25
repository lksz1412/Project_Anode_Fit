#!/usr/bin/env python3
"""Validate Phase 060 Step 42 runtime and stored-artifact evidence.

The validator is deliberately narrower than a scientific validator.  It checks
source identity, audit coverage, execution determinism, and the authority
boundaries recorded by Step 42.  It does not promote internal regression,
synthetic fitting, or visual agreement to experimental truth.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
RUNTIME_MATRIX = ROOT / "Codex/results/PHASE_060_V1019_CODE_TEST_RUNTIME_MATRIX.json"
ARTIFACT_AUDIT = ROOT / "Codex/results/PHASE_060_V1019_ARTIFACT_AUDIT.json"
AUDITOR = ROOT / "Codex/work/v1019_phase060/audit_phase060_step42_runtime_artifacts.py"
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()

CODE_LINES = {
    "Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py": 1151,
    "Claude/docs/v1.0.19/fit_roundtrip_demo.py": 368,
    "Claude/docs/v1.0.19/graph_suite_v1019.py": 150,
    "Claude/docs/v1.0.19/test_regression_v1019.py": 127,
}
RUNTIME_CASES = [
    "regression_verify",
    "regression_capture_guard",
    "fit_roundtrip",
    "graph_suite",
    "module_demo",
]
EXPECTED_EXITS = {
    "regression_verify": 0,
    "regression_capture_guard": 3,
    "fit_roundtrip": 0,
    "graph_suite": 0,
    "module_demo": 0,
}
PDF_PAGES = {
    "Claude/docs/v1.0.19/appendix_phase_separation.pdf": 8,
    "Claude/docs/v1.0.19/graphite_ica_ch1_v1.0.19.pdf": 62,
    "Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.pdf": 25,
}
EXPECTED_NPZ_SHA = "61b7f59b809417f46618039d1eecf5cc1aca9ed2d0202fcda7d909386c00d0c2"
EXPECTED_SNAPSHOT_SHA = "deb97711e6e7570a680421a4ce71a06eac581b8a0d8c8b3adfca9a132e45e14e"
EXPECTED_CLAIM_FINGERPRINT = "dc62069e834579c6f6ac6e8ee711fcdc1406d8a09a29b36e9f0275e27b932588"
EXPECTED_EDGE_FINGERPRINT = "eac13854a3b82d0baef8a60fd7a2d7ff606a322a1af4dc80a90dc67dca2a1e73"
EXPECTED_DEFINITION_FINGERPRINT = "f4dc07f5251465d14d6c56265aa105ac7d24e8f2650daa723c558e10acae7d99"
EXPECTED_SEMANTIC_FINGERPRINT = "5cd2bf92eda64253f51f0ac7ec4f9f0f037da853ac9701e76a0515cfa5ca8d3e"
EXPECTED_PDF_FINGERPRINT = "e4f3df8e10b3ae3d21f4073337ed4245f6d01e89e567dcb9ef96e1363fe02d4d"
EXPECTED_IMAGE_FINGERPRINT = "a20fe14ada6a3cddb3579a72d828777528ef939364be5f9c6a6c723f2acae0d1"
EXPECTED_NPZ_ARRAY_FINGERPRINT = "6348a5f375c422c790547472e733eae2b533a83c3b2ba25fa520bcaa160736bd"
EXPECTED_NPZ_MEMBER_FINGERPRINT = "e8bbc6e568ffa321af171e187b14857ea713dd267c2d82c8fbecb2c1f303777e"
EXPECTED_CROSS_VERSION_FINGERPRINT = "045809462960a5fcb74ae59102521d48b151090063d09403f4fb93827895c6b8"
EXPECTED_RUNTIME_CASE_FINGERPRINT = "a24bf673eda4bc6ad174049e1d33e93200c0ad5ba327ba31051ff82f11f2c7b7"
EXPECTED_FINDING_FINGERPRINT = "ee58bd952894884188c600116f0a91902fc15d773896681b8fe25175c9b504b7"
EXPECTED_MANUAL_ATTESTATION_FINGERPRINT = "01cc2a7405f923072b237fa6f0b61e38ba579b5eecd4c337669607881829ae89"
EXPECTED_IMPORT_FINGERPRINT = "bc5d284dd1465129b99d6434bd17187a3fb909eb79bf6009b37a41da3c58f92c"
EXPECTED_DETERMINISM_SCOPE = (
    "Byte-identical rebuild is required only under the recorded "
    "Python/dependency/Poppler platform; cross-toolchain byte portability is not claimed."
)


class DuplicateKeyError(ValueError):
    """Raised when a JSON object repeats a key."""


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate key: {key}")
        result[key] = value
    return result


def strict_json_load(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON number: {value}")
        ),
    )


def canonical_fingerprint(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def git_bytes(*args: str) -> bytes:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout


def raw_blob(path: str) -> bytes:
    return git_bytes("cat-file", "blob", f"{SOURCE_COMMIT}:{path}")


def actual_claude_status() -> list[str]:
    text = git_bytes("status", "--porcelain", "--", "Claude").decode(
        "utf-8", errors="replace"
    )
    return [line for line in text.splitlines() if line]


def check(condition: bool, code: str, errors: list[str]) -> None:
    if not condition:
        errors.append(code)


def validate_runtime(runtime: dict[str, Any], claude_status: list[str]) -> list[str]:
    errors: list[str] = []
    check(runtime.get("schema_version") == 1, "runtime.schema_version", errors)
    check(runtime.get("phase") == 60 and runtime.get("step") == 42, "runtime.phase_step", errors)
    check(runtime.get("source_commit") == SOURCE_COMMIT, "runtime.source_commit", errors)
    check(claude_status == [], "runtime.dirty_claude", errors)

    code_index = runtime.get("code_index", [])
    check(isinstance(code_index, list) and len(code_index) == 4, "runtime.code.files", errors)
    by_path = {item.get("path"): item for item in code_index if isinstance(item, dict)}
    check(set(by_path) == set(CODE_LINES), "runtime.code.paths", errors)
    for path, expected_lines in CODE_LINES.items():
        item = by_path.get(path, {})
        blob = raw_blob(path)
        check(item.get("physical_lines") == expected_lines, f"runtime.code.lines:{path}", errors)
        check(item.get("read_coverage") == [1, expected_lines], f"runtime.code.coverage:{path}", errors)
        check(item.get("syntax_parse") == "PASS", f"runtime.code.syntax:{path}", errors)
        check(item.get("git_blob_sha1") == hashlib.sha1(f"blob {len(blob)}\0".encode() + blob).hexdigest(), f"runtime.code.blob:{path}", errors)
        check(item.get("raw_git_blob_sha256") == hashlib.sha256(blob).hexdigest(), f"runtime.code.sha256:{path}", errors)
        check(item.get("assert_nodes") == [], f"runtime.code.assert_nodes:{path}", errors)
        definitions = item.get("definitions", [])
        check(all(set(record) >= {"kind", "qualified_name", "start_line", "end_line", "public_entry", "docstring", "signature", "state_writes", "explicit_raises", "exception_handlers", "return_lines", "branch_tests", "side_effect_calls"} for record in definitions), f"runtime.code.definition_contract:{path}", errors)
        check(all(isinstance(record.get("public_entry"), bool) for record in definitions), f"runtime.code.public_entry:{path}", errors)
        check(all(set(record.get("signature", {})) == {"parameters", "return_annotation"} for record in definitions), f"runtime.code.signature:{path}", errors)
        check(all(all(set(parameter) == {"name", "kind", "annotation", "default"} for parameter in record.get("signature", {}).get("parameters", [])) for record in definitions), f"runtime.code.parameters:{path}", errors)
        check(isinstance(item.get("module_and_class_state"), list), f"runtime.code.state_index:{path}", errors)
        semantics = item.get("path_semantics", [])
        check(all(set(record) == {"id", "path", "lines", "category", "inputs", "outputs", "state", "defaults", "errors", "fallbacks", "dormant_or_ignored", "side_effects"} for record in semantics), f"runtime.code.path_semantics_schema:{path}", errors)
        check(all(record.get("path") == path for record in semantics), f"runtime.code.path_semantics_path:{path}", errors)

    summary = runtime.get("code_summary", {})
    check(summary.get("files") == 4, "runtime.code_summary.files", errors)
    check(summary.get("physical_lines") == 1796, "runtime.code_summary.lines", errors)
    check(summary.get("assert_nodes") == 0, "runtime.code_summary.asserts", errors)
    check(summary.get("definitions") == sum(len(x.get("definitions", [])) for x in code_index), "runtime.code_summary.definitions", errors)
    check(summary.get("call_edges") == sum(len(x.get("call_edges", [])) for x in code_index), "runtime.code_summary.edges", errors)
    check(summary.get("public_entries") == 34, "runtime.code_summary.public_entries", errors)
    check(summary.get("module_and_class_state_records") == 112 == sum(len(x.get("module_and_class_state", [])) for x in code_index), "runtime.code_summary.state_records", errors)
    check(summary.get("path_semantic_records") == 8 == sum(len(x.get("path_semantics", [])) for x in code_index), "runtime.code_summary.path_semantics", errors)
    check(set(summary.get("semantic_fields", [])) >= {"public_entry", "signature.parameters", "signature.return_annotation", "state_writes", "explicit_raises", "exception_handlers", "side_effect_calls", "module_and_class_state", "path_semantics.inputs", "path_semantics.outputs", "path_semantics.defaults", "path_semantics.errors", "path_semantics.fallbacks", "path_semantics.dormant_or_ignored"}, "runtime.code_summary.semantic_fields", errors)

    definition_surface = [{x.get("path"): x.get("definitions")} for x in code_index]
    edge_surface = [{x.get("path"): x.get("call_edges")} for x in code_index]
    semantic_surface = [{x.get("path"): {"state":x.get("module_and_class_state"), "path_semantics":x.get("path_semantics")}} for x in code_index]
    import_surface = [{x.get("path"): x.get("imports")} for x in code_index]
    check(canonical_fingerprint(definition_surface) == EXPECTED_DEFINITION_FINGERPRINT, "runtime.definition_fingerprint", errors)
    check(canonical_fingerprint(edge_surface) == EXPECTED_EDGE_FINGERPRINT, "runtime.call_edge_fingerprint", errors)
    check(canonical_fingerprint(semantic_surface) == EXPECTED_SEMANTIC_FINGERPRINT, "runtime.semantic_index_fingerprint", errors)
    check(canonical_fingerprint(import_surface) == EXPECTED_IMPORT_FINGERPRINT, "runtime.import_fingerprint", errors)
    optional_imports = [
        (item.get("path"), record.get("module"), record.get("line"))
        for item in code_index
        for record in item.get("imports", [])
        if record.get("optional") is True
    ]
    check(
        optional_imports
        == [
            ("Claude/docs/v1.0.19/fit_roundtrip_demo.py", "scipy.optimize", 212),
            ("Claude/docs/v1.0.19/fit_roundtrip_demo.py", "matplotlib", 302),
            ("Claude/docs/v1.0.19/fit_roundtrip_demo.py", "matplotlib.pyplot", 304),
        ],
        "runtime.import_optional_contract",
        errors,
    )

    claims = runtime.get("claim_gate_index", [])
    claim_summary = runtime.get("claim_gate_summary", {})
    check(isinstance(claims, list) and len(claims) == 46, "runtime.claims.count", errors)
    ids = [item.get("id") for item in claims if isinstance(item, dict)]
    check(len(ids) == len(set(ids)) == 46, "runtime.claims.unique", errors)
    check(claim_summary.get("records") == 46 and claim_summary.get("ids") == ids, "runtime.claims.summary", errors)
    check(canonical_fingerprint(claims) == EXPECTED_CLAIM_FINGERPRINT, "runtime.claim_fingerprint", errors)

    run = runtime.get("runtime", {})
    passes = run.get("passes", [])
    check(run.get("pass_count") == 2 and len(passes) == 2, "runtime.passes.count", errors)
    check(run.get("byte_identical_records") is True, "runtime.passes.deterministic", errors)
    if len(passes) == 2:
        check(passes[0] == passes[1], "runtime.passes.byte_records", errors)
    for pass_no, record in enumerate(passes, start=1):
        cases = record.get("cases", [])
        case_ids = [case.get("case_id") for case in cases]
        check(case_ids == RUNTIME_CASES, f"runtime.pass{pass_no}.case_set", errors)
        check(canonical_fingerprint(cases) == EXPECTED_RUNTIME_CASE_FINGERPRINT, f"runtime.pass{pass_no}.case_fingerprint", errors)
        check(record.get("working_tree_claude_status_before") == [], f"runtime.pass{pass_no}.claude_before", errors)
        check(record.get("working_tree_claude_status_after") == [], f"runtime.pass{pass_no}.claude_after", errors)
        immutable = record.get("fixture_source_immutability", [])
        check(len(immutable) == 5, f"runtime.pass{pass_no}.immutability_count", errors)
        check(all(item.get("content_unchanged") is True and item.get("size_unchanged") is True and item.get("mtime_ns_unchanged") is True and item.get("mode_unchanged") is True and item.get("matches_frozen_blob") is True for item in immutable), f"runtime.pass{pass_no}.metadata_immutability", errors)
        check(all(item.get("before_sha256") == item.get("after_sha256") and item.get("before_size_bytes") == item.get("after_size_bytes") for item in immutable), f"runtime.pass{pass_no}.before_after_identity", errors)
        for case in cases:
            case_id = case.get("case_id")
            check(case.get("exit_code") == EXPECTED_EXITS.get(case_id), f"runtime.case.exit:{case_id}", errors)
            check(case.get("exit_matches_contract") is True, f"runtime.case.contract:{case_id}", errors)
            check(case.get("stderr_sha256") == EMPTY_SHA256 and case.get("stderr_size_bytes") == 0, f"runtime.case.stderr:{case_id}", errors)
            check(case.get("cwd") == "<SYSTEM_TEMP>/fixture/Claude/docs/v1.0.19", f"runtime.case.cwd:{case_id}", errors)

    semantic = run.get("semantic_summary", {})
    check(semantic.get("regression", {}).get("array_equal_passed") == 13, "runtime.semantic.regression", errors)
    check(semantic.get("regression", {}).get("gate_scope") == "array equality only", "runtime.semantic.regression_scope", errors)
    check(semantic.get("fit_roundtrip", {}).get("all_source_gates") is True, "runtime.semantic.fit", errors)
    check(semantic.get("fit_roundtrip", {}).get("experimental_validation") is False, "runtime.semantic.fit_authority", errors)
    check(semantic.get("graph_suite", {}).get("aggregate_exit_gate") is False, "runtime.semantic.graph_scope", errors)
    check(semantic.get("module_demo", {}).get("gate_scope") == "subset described by MAIN-15", "runtime.semantic.module_scope", errors)

    golden = runtime.get("golden_npz", {})
    arrays = golden.get("arrays", [])
    check(golden.get("allow_pickle") is False, "runtime.golden.allow_pickle", errors)
    check(golden.get("load_status") == "PASS", "runtime.golden.load", errors)
    check(golden.get("sha256") == EXPECTED_NPZ_SHA, "runtime.golden.sha256", errors)
    check(golden.get("array_count") == len(arrays) == 13, "runtime.golden.count", errors)
    check([x.get("order") for x in arrays] == list(range(13)), "runtime.golden.order", errors)
    check(all(x.get("shape") == [1000] and x.get("dtype") == "<f8" for x in arrays), "runtime.golden.shape_dtype", errors)
    check(all(x.get("finite_count") == 1000 and x.get("nan_count") == 0 and x.get("posinf_count") == 0 and x.get("neginf_count") == 0 for x in arrays), "runtime.golden.finite", errors)
    check(canonical_fingerprint(arrays) == EXPECTED_NPZ_ARRAY_FINGERPRINT, "runtime.golden.array_fingerprint", errors)
    members = golden.get("zip_members", [])
    check(len(members) == 13 and [item.get("order") for item in members] == list(range(13)), "runtime.golden.members", errors)
    check(all(item.get("date_time") == [1980, 1, 1, 0, 0, 0] for item in members), "runtime.golden.member_timestamps", errors)
    check(canonical_fingerprint(members) == EXPECTED_NPZ_MEMBER_FINGERPRINT, "runtime.golden.member_fingerprint", errors)
    capture = golden.get("fresh_capture", {})
    capture_passes = capture.get("passes", [])
    check(capture.get("pass_count") == 2 and len(capture_passes) == 2, "runtime.golden.capture_count", errors)
    check(capture.get("byte_identical_records") is True and len(capture_passes) == 2 and capture_passes[0] == capture_passes[1], "runtime.golden.capture_deterministic", errors)
    check(capture.get("stored_archive_byte_identical") is True and capture.get("stored_member_order_and_bytes_identical") is True, "runtime.golden.capture_identity", errors)
    for index, capture_pass in enumerate(capture_passes, start=1):
        capture_runtime = capture_pass.get("runtime", {})
        check(capture_runtime.get("exit_code") == 0 and capture_runtime.get("exit_matches_contract") is True, f"runtime.golden.capture{index}.exit", errors)
        check(capture_runtime.get("stderr_sha256") == EMPTY_SHA256 and capture_runtime.get("semantic_observations", {}).get("fresh_capture_array_count") == 13, f"runtime.golden.capture{index}.output", errors)
        check(capture_pass.get("archive_sha256") == EXPECTED_NPZ_SHA and capture_pass.get("zip_members") == members and capture_pass.get("source_code_unchanged") is True, f"runtime.golden.capture{index}.identity", errors)

    witness = runtime.get("v1020_snapshot_witness", {})
    check(witness.get("physical_lines") == 1120 and witness.get("read_coverage") == [1, 1120], "runtime.snapshot.coverage", errors)
    check(witness.get("strict_json") == "PASS", "runtime.snapshot.strict_json", errors)
    check(witness.get("raw_git_blob_sha256") == EXPECTED_SNAPSHOT_SHA, "runtime.snapshot.sha256", errors)
    check(witness.get("recursive_node_count") == 1583, "runtime.snapshot.nodes", errors)
    roots = witness.get("top_level_roots", [])
    check([(x.get("labels"), x.get("equation_blocks"), x.get("boxed_equation_blocks"), x.get("asset_unique"), x.get("bibitems")) for x in roots] == [(219, 122, 33, 336, 28), (69, 32, 10, 21, 14)], "runtime.snapshot.claims", errors)
    generator = witness.get("generator", {})
    check(generator.get("path") == "Claude/docs/v1.0.20/results/tools_check_structure.py" and generator.get("physical_lines") == 165 and generator.get("read_coverage") == [1, 165], "runtime.snapshot.generator", errors)
    regeneration = witness.get("regeneration", {})
    regeneration_passes = regeneration.get("passes", [])
    check(regeneration.get("pass_count") == 2 and len(regeneration_passes) == 2, "runtime.snapshot.regeneration_count", errors)
    check(regeneration.get("byte_identical_records") is True and len(regeneration_passes) == 2 and regeneration_passes[0] == regeneration_passes[1], "runtime.snapshot.regeneration_deterministic", errors)
    check(regeneration.get("object_equal_to_stored") is True and regeneration.get("normalized_byte_equal_to_raw_stored") is True, "runtime.snapshot.regeneration_identity", errors)
    check(all(item.get("exit_code") == 0 and item.get("strict_json") == "PASS" and item.get("tex_files") == 42 and item.get("source_inputs_unchanged") is True and item.get("object_equal_to_stored") is True and item.get("normalized_lf_sha256") == EXPECTED_SNAPSHOT_SHA for item in regeneration_passes), "runtime.snapshot.regeneration_passes", errors)

    check(runtime.get("finding_summary") == {"P0": 0, "P1": 6, "P2": 9}, "runtime.findings.summary", errors)
    findings = runtime.get("findings", {})
    check({key: len(findings.get(key, [])) for key in ("P0", "P1", "P2")} == {"P0": 0, "P1": 6, "P2": 9}, "runtime.findings.count", errors)
    check(canonical_fingerprint(findings) == EXPECTED_FINDING_FINGERPRINT, "runtime.findings.fingerprint", errors)
    check(runtime.get("generation", {}).get("determinism_scope") == EXPECTED_DETERMINISM_SCOPE, "runtime.generation.determinism_scope", errors)
    check(runtime.get("authority_policy", {}).get("scientific_truth", "").startswith("NOT_PROMOTED"), "runtime.authority.science", errors)
    return errors


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    check(artifact.get("schema_version") == 1, "artifact.schema_version", errors)
    check(artifact.get("phase") == 60 and artifact.get("step") == 42, "artifact.phase_step", errors)
    check(artifact.get("source_commit") == SOURCE_COMMIT, "artifact.source_commit", errors)

    pdfs = artifact.get("pdfs", [])
    by_path = {item.get("path"): item for item in pdfs if isinstance(item, dict)}
    check(set(by_path) == set(PDF_PAGES), "artifact.pdf.paths", errors)
    for path, expected in PDF_PAGES.items():
        item = by_path.get(path, {})
        pages = item.get("pages", [])
        check(item.get("page_count") == item.get("expected_page_count") == expected, f"artifact.pdf.count:{path}", errors)
        check(item.get("rendered_page_count") == len(pages) == expected, f"artifact.pdf.render_count:{path}", errors)
        check([page.get("page") for page in pages] == list(range(1, expected + 1)), f"artifact.pdf.sequence:{path}", errors)
        check(item.get("render_exit_code") == 0 and item.get("render_stderr_sha256") == EMPTY_SHA256, f"artifact.pdf.render:{path}", errors)
        check(all(page.get("width") == 1191 and page.get("height") == 1684 and page.get("mode") == "RGB" for page in pages), f"artifact.pdf.page_geometry:{path}", errors)
        blob = raw_blob(path)
        check(item.get("sha256") == hashlib.sha256(blob).hexdigest(), f"artifact.pdf.sha256:{path}", errors)
    summary = artifact.get("pdf_summary", {})
    check(summary == {"files": 3, "pages": 95, "rendered_pages": 95}, "artifact.pdf.summary", errors)
    check(canonical_fingerprint([(x.get("path"), x.get("sha256"), x.get("page_count")) for x in pdfs]) == EXPECTED_PDF_FINGERPRINT, "artifact.pdf.fingerprint", errors)

    images = artifact.get("images", [])
    check(len(images) == 13, "artifact.images.count", errors)
    check(len({item.get("git_blob_sha1") for item in images}) == 13, "artifact.images.unique", errors)
    check(len({item.get("path") for item in images}) == 13, "artifact.images.paths", errors)
    check(all(item.get("format") == "PNG" and item.get("frames") == 1 for item in images), "artifact.images.format", errors)
    check(all(item.get("provenance", {}).get("status") in {"DIRECT_GENERATOR", "DIRECT_TEX_SOURCE", "KERNEL_AND_BUILD_EVENT_ONLY", "GROUND_NOT_FOUND"} for item in images), "artifact.images.provenance", errors)
    check(artifact.get("image_summary") == {"occurrences": 13, "unique_blobs": 13}, "artifact.images.summary", errors)
    check(canonical_fingerprint([(x.get("path"), x.get("sha256"), x.get("width"), x.get("height")) for x in images]) == EXPECTED_IMAGE_FINGERPRINT, "artifact.images.fingerprint", errors)

    fresh = artifact.get("fresh_to_stored_comparisons", {})
    check(set(fresh) == {"fit_roundtrip", "graph_suite"}, "artifact.fresh.keys", errors)
    check(all(item.get("byte_identical") is True for item in fresh.values()), "artifact.fresh.identity", errors)
    cross = artifact.get("cross_version_witness", {})
    check(cross.get("byte_identical") is True and cross.get("review_authority_counted_again") is False, "artifact.cross_version", errors)
    comparisons = artifact.get("cross_version_comparisons", [])
    check(len(comparisons) == 3, "artifact.cross_version_comparison_count", errors)
    check([(item.get("differing_pixels"), item.get("difference_bbox_left_top_right_bottom_exclusive"), item.get("byte_identical")) for item in comparisons] == [(34, [1342, 645, 1347, 653], False), (39, [1341, 645, 1347, 653], False), (0, None, True)], "artifact.cross_version_pixel_diffs", errors)
    check(all(item.get("dimensions_equal") is True and item.get("authority_boundary") == "Pixel identity/difference is visual lineage evidence only." for item in comparisons), "artifact.cross_version_authority", errors)
    check(canonical_fingerprint(comparisons) == EXPECTED_CROSS_VERSION_FINGERPRINT, "artifact.cross_version_fingerprint", errors)

    manual = artifact.get("manual_visual_attestation", {})
    check(manual.get("status") == "DONE_WITH_CONCERNS", "artifact.manual.status", errors)
    check(manual.get("pdf_pages_reviewed") == 95, "artifact.manual.pdf_pages", errors)
    check(manual.get("unique_images_reviewed") == 13, "artifact.manual.images", errors)
    check(manual.get("finding_summary") == {"P0": 0, "P1": 0, "P2": 4}, "artifact.manual.findings", errors)
    pdf_records = manual.get("pdf_records", [])
    image_records = manual.get("image_records", [])
    check(len(pdf_records) == 3 and sum(item.get("pages_reviewed", 0) for item in pdf_records) == 95, "artifact.manual.pdf_records", errors)
    check(len(image_records) == 13 and len({item.get("path") for item in image_records}) == 13, "artifact.manual.image_records", errors)
    check(all(item.get("visual_status") in {"PASS", "CONCERN_CLIPPED_TITLE", "CONCERN_VERSION_LABEL", "CONCERN_PROVENANCE"} for item in image_records), "artifact.manual.image_status", errors)
    check(canonical_fingerprint(manual) == EXPECTED_MANUAL_ATTESTATION_FINGERPRINT, "artifact.manual.fingerprint", errors)
    policy = artifact.get("authority_policy", {})
    check(policy.get("scientific_truth") == "NOT_PROMOTED" and policy.get("experimental_validation") == "NOT_CLAIMED", "artifact.authority", errors)
    return errors


def assert_negative(label: str, runtime: dict[str, Any], artifact: dict[str, Any], mutate: Any, expected_fragment: str) -> None:
    bad_runtime = copy.deepcopy(runtime)
    bad_artifact = copy.deepcopy(artifact)
    dirty: list[str] = []
    mutate(bad_runtime, bad_artifact, dirty)
    errors = validate_runtime(bad_runtime, dirty) + validate_artifact(bad_artifact)
    if not any(expected_fragment in error for error in errors):
        raise AssertionError(f"negative {label} escaped expected={expected_fragment} errors={errors}")
    print(f"PASS_NEGATIVE {label} -> {expected_fragment}")


def deterministic_rebuild() -> None:
    with tempfile.TemporaryDirectory(prefix="phase060_step42_validate_") as tmp:
        temp_root = Path(tmp)
        runtime_out = temp_root / "runtime.json"
        artifact_out = temp_root / "artifact.json"
        proc = subprocess.run(
            [
                sys.executable,
                str(AUDITOR),
                "--runtime-output",
                str(runtime_out),
                "--artifact-output",
                str(artifact_out),
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode != 0:
            raise AssertionError(
                "deterministic rebuild failed: "
                + proc.stderr.decode("utf-8", errors="replace")
            )
        if runtime_out.read_bytes() != RUNTIME_MATRIX.read_bytes():
            raise AssertionError("deterministic runtime JSON byte mismatch")
        if artifact_out.read_bytes() != ARTIFACT_AUDIT.read_bytes():
            raise AssertionError("deterministic artifact JSON byte mismatch")
    print("PASS deterministic_rebuild byte_identical=2/2")


def main() -> int:
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (AUDITOR, RUNTIME_MATRIX, ARTIFACT_AUDIT)
        if not path.is_file()
    ]
    if missing:
        for path in missing:
            print(f"FAIL missing_artifact: {path}")
        print(f"FAIL_P060_STEP42_RUNTIME_ARTIFACTS 0/{len(missing)}")
        return 2

    try:
        runtime = strict_json_load(RUNTIME_MATRIX)
        artifact = strict_json_load(ARTIFACT_AUDIT)
        errors = validate_runtime(runtime, actual_claude_status()) + validate_artifact(artifact)
        if errors:
            for error in errors:
                print(f"FAIL {error}")
            print(f"FAIL_P060_STEP42_RUNTIME_ARTIFACTS 0/{len(errors)}")
            return 1

        assert_negative(
            "skipped_pdf_page",
            runtime,
            artifact,
            lambda _r, a, _d: a["pdfs"][0]["pages"].pop(),
            "artifact.pdf.render_count",
        )
        assert_negative(
            "altered_assertion_gate",
            runtime,
            artifact,
            lambda r, _a, _d: r["claim_gate_index"][0].__setitem__("gate", "GATED"),
            "runtime.claim_fingerprint",
        )
        assert_negative(
            "missing_call_edge",
            runtime,
            artifact,
            lambda r, _a, _d: r["code_index"][0]["call_edges"].pop(),
            "runtime.code_summary.edges",
        )
        assert_negative(
            "dirty_claude",
            runtime,
            artifact,
            lambda _r, _a, d: d.append(" M Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py"),
            "runtime.dirty_claude",
        )
        assert_negative(
            "extra_runtime_output",
            runtime,
            artifact,
            lambda r, _a, _d: r["runtime"]["passes"][0]["cases"][0].__setitem__("stdout_size_bytes", r["runtime"]["passes"][0]["cases"][0]["stdout_size_bytes"] + 1),
            "runtime.pass1.case_fingerprint",
        )
        assert_negative(
            "golden_mismatch",
            runtime,
            artifact,
            lambda r, _a, _d: r["golden_npz"].__setitem__("sha256", "0" * 64),
            "runtime.golden.sha256",
        )
        assert_negative(
            "missing_semantic_index",
            runtime,
            artifact,
            lambda r, _a, _d: r["code_index"][0]["path_semantics"].pop(),
            "runtime.code_summary.path_semantics",
        )
        assert_negative(
            "metadata_mutation",
            runtime,
            artifact,
            lambda r, _a, _d: r["runtime"]["passes"][0]["fixture_source_immutability"][0].__setitem__("mtime_ns_unchanged", False),
            "runtime.pass1.metadata_immutability",
        )
        assert_negative(
            "fresh_capture_mismatch",
            runtime,
            artifact,
            lambda r, _a, _d: r["golden_npz"]["fresh_capture"].__setitem__("stored_archive_byte_identical", False),
            "runtime.golden.capture_identity",
        )
        assert_negative(
            "snapshot_regeneration_mismatch",
            runtime,
            artifact,
            lambda r, _a, _d: r["v1020_snapshot_witness"]["regeneration"].__setitem__("object_equal_to_stored", False),
            "runtime.snapshot.regeneration_identity",
        )
        assert_negative(
            "pixel_diff_mismatch",
            runtime,
            artifact,
            lambda _r, a, _d: a["cross_version_comparisons"][0].__setitem__("differing_pixels", 35),
            "artifact.cross_version_pixel_diffs",
        )
        assert_negative(
            "fabricated_finding",
            runtime,
            artifact,
            lambda r, _a, _d: r["findings"]["P1"].__setitem__(0, "fabricated replacement"),
            "runtime.findings.fingerprint",
        )
        assert_negative(
            "altered_manual_attestation",
            runtime,
            artifact,
            lambda _r, a, _d: a["manual_visual_attestation"]["pdf_records"][0].__setitem__("note", ""),
            "artifact.manual.fingerprint",
        )
        assert_negative(
            "optional_import_mutation",
            runtime,
            artifact,
            lambda r, _a, _d: r["code_index"][1]["imports"][5].__setitem__("optional", False),
            "runtime.import_fingerprint",
        )
        deterministic_rebuild()
    except Exception as exc:
        print(f"FAIL exception: {type(exc).__name__}: {exc}")
        print("FAIL_P060_STEP42_RUNTIME_ARTIFACTS 0/1")
        return 1

    print("PASS strict_json duplicate_keys=0 nonfinite=0")
    print("PASS negative_mutations required=6/6 supplemental=8/8 total=14/14")
    print("PASS coverage code=4/4 lines=1796/1796 semantic_paths=8/8 claims=46/46 metadata=10/10 npz=13/13 fresh_capture=2/2 snapshot_regeneration=2/2 pdf=3/3 pages=95/95 images=13/13 pixel_comparisons=3/3")
    print("PASS authority runtime_bounded scientific_not_promoted experimental_not_claimed")
    print("PASS_P060_STEP42_RUNTIME_ARTIFACTS 42/42")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
