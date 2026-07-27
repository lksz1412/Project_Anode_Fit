#!/usr/bin/env python3
"""Validate the Phase 059 production-code source index and exact diffs."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
INDEX = RESULTS / "PHASE_059_PRODUCTION_CODE_INDEX.json"
DIFF = RESULTS / "PHASE_059_PRODUCTION_CODE_DIFF.json"
REVIEW = RESULTS / "PHASE_059_PRODUCTION_CODE_REVIEW.md"
QUEUE = RESULTS / "PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json"
CONTRACTS = RESULTS / "PHASE_059_THEORY_CONTRACT_MATRIX.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def main() -> None:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    diff = json.loads(DIFF.read_text(encoding="utf-8"))
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    contracts = json.loads(CONTRACTS.read_text(encoding="utf-8"))
    modules = index["modules"]
    findings = index["review"]["findings"]
    by_finding = {item["id"]: item for item in findings}
    contract_ids = {item["id"] for item in contracts["records"]}
    queue_code = {
        item["representative_path"]: item
        for item in queue["records"]
        if item["role"] == "code"
    }

    checks: list[tuple[str, bool]] = []
    checks.append(("review exists", REVIEW.is_file()))
    checks.append(
        ("index gate exact", index["status"] == "PASS_P059_PRODUCTION_CODE_INDEX")
    )
    checks.append(
        (
            "diff gate exact",
            diff["status"] == "PASS_P059_PRODUCTION_CODE_EXACT_DIFF",
        )
    )
    checks.append(("unique blob count", index["unique_blob_count"] == 4))
    checks.append(("occurrence path count", index["occurrence_path_count"] == 6))
    checks.append(("total line count", index["total_line_count"] == 3704))
    checks.append(("module count", len(modules) == 4))
    checks.append(("comparison count", diff["comparison_count"] == 3))
    checks.append(("finding count", index["review"]["finding_count"] == 13))
    checks.append(("finding ids unique", len(by_finding) == 13))
    checks.append(
        (
            "finding ids exact sequence",
            [item["id"] for item in findings]
            == [f"P059-CODE-{number:03d}" for number in range(1, 14)],
        )
    )

    module_source_exact = True
    module_ast_exact = True
    queue_link_exact = True
    api_constructor_present = True
    for module in modules:
        path = ROOT / module["representative_path"]
        raw = path.read_bytes()
        lines = raw.decode("utf-8").splitlines()
        module_source_exact &= (
            module["sha256"] == sha256_bytes(raw)
            and module["byte_count"] == len(raw)
            and module["line_count"] == len(lines)
        )
        tree = ast.parse(raw.decode("utf-8"), filename=str(path))
        function_names = set()
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_names.add(node.name)
            elif isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        function_names.add(f"{node.name}.{child.name}")
        module_ast_exact &= function_names == {
            item["qualified_name"] for item in module["functions"]
        }
        queue_item = queue_code[module["representative_path"]]
        queue_link_exact &= (
            module["git_blob_sha"] == queue_item["blob_sha"]
            and module["occurrence_paths"] == queue_item["occurrence_paths"]
        )
        api_constructor_present &= any(
            item["qualified_name"] == "GraphiteAnodeDischargeDQDV.__init__"
            for item in module["public_api"]
        )
    checks.append(("module source hashes exact", module_source_exact))
    checks.append(("module AST function sets exact", module_ast_exact))
    checks.append(("queue blob and occurrence links exact", queue_link_exact))
    checks.append(("constructor included in API", api_constructor_present))

    patch_exact = True
    endpoints_exact = True
    datasets_unchanged = True
    for item in diff["comparisons"]:
        patch = (ROOT / item["exact_unified_diff"]).read_bytes()
        patch_exact &= item["exact_unified_diff_sha256"] == sha256_bytes(patch)
        endpoints_exact &= (
            item["old_blob_sha"]
            == queue_code[item["old_path"]]["blob_sha"]
            and item["new_blob_sha"]
            == queue_code[item["new_path"]]["blob_sha"]
        )
        datasets_unchanged &= (
            item["dataset_hashes_old"] == item["dataset_hashes_new"]
        )
    checks.append(("exact patch hashes", patch_exact))
    checks.append(("diff endpoint blobs exact", endpoints_exact))
    checks.append(("default datasets unchanged across comparisons", datasets_unchanged))

    copy = diff["copy_forward"][0]
    checks.append(
        (
            "v16 v17 v181 copy lineage exact",
            copy["occurrence_paths"]
            == [
                "Claude/docs/v1.0.16/Anode_Fit_v1.0.16.py",
                "Claude/docs/v1.0.17/Anode_Fit_v1.0.17.py",
                "Claude/docs/v1.0.18.1/Anode_Fit_v1.0.18.1.py",
            ],
        )
    )
    checks.append(
        (
            "pointwise helper lineage exact",
            diff["comparisons"][0]["functions_added"]
            == ["_causal_memory_pointwise"]
            and set(diff["comparisons"][0]["functions_removed"])
            == {"_causal_lowpass", "func_U_j_hys"},
        )
    )
    checks.append(
        (
            "nT helper lineage exact",
            diff["comparisons"][1]["functions_added"]
            == ["GraphiteAnodeDischargeDQDV._dwdT"],
        )
    )
    checks.append(
        (
            "Einstein helper lineage exact",
            set(diff["comparisons"][2]["functions_added"])
            == {
                "GraphiteAnodeDischargeDQDV._S_vib",
                "GraphiteAnodeDischargeDQDV._vib_dS",
                "GraphiteAnodeDischargeDQDV._vib_dU",
                "GraphiteAnodeDischargeDQDV._vib_theta",
            },
        )
    )

    anchors_exact = True
    contract_links_exact = True
    for item in findings:
        for evidence in item["source_evidence"]:
            line = (
                (ROOT / evidence["path"])
                .read_text(encoding="utf-8")
                .splitlines()[evidence["line"] - 1]
            )
            anchors_exact &= (
                line == evidence["source_line"]
                and evidence["needle"] in evidence["source_line"]
            )
        contract_links_exact &= set(item["contract_ids"]).issubset(contract_ids)
    checks.append(("finding anchors exact", anchors_exact))
    checks.append(("finding contract links exact", contract_links_exact))
    checks.append(
        (
            "critical blocker count",
            index["review"]["severity_counts"]["CRITICAL"] == 5,
        )
    )
    checks.append(
        (
            "trajectory blocker retained",
            by_finding["P059-CODE-002"]["severity"] == "CRITICAL"
            and by_finding["P059-CODE-002"]["disposition"] == "CORRECT",
        )
    )
    checks.append(
        (
            "local barrier rejected",
            by_finding["P059-CODE-005"]["disposition"] == "REJECT",
        )
    )
    checks.append(
        (
            "unit blocker retained",
            by_finding["P059-CODE-006"]["severity"] == "CRITICAL",
        )
    )
    checks.append(
        (
            "dwdT mismatch retained",
            by_finding["P059-CODE-007"]["disposition"] == "CORRECT",
        )
    )
    checks.append(
        (
            "high-voltage gap retained",
            by_finding["P059-CODE-011"]["severity"] == "CRITICAL",
        )
    )
    checks.append(
        (
            "Einstein capability bounded",
            by_finding["P059-CODE-013"]["disposition"]
            == "INTERNAL_CAPABILITY_ONLY",
        )
    )

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}")
    if failed:
        raise SystemExit(f"PHASE 059 CODE INDEX FAIL: {failed}")
    print(
        "PASS_P059_PRODUCTION_CODE_INDEX_AND_DIFF "
        f"checks={len(checks)}/{len(checks)} modules=4 findings=13"
    )


if __name__ == "__main__":
    main()
