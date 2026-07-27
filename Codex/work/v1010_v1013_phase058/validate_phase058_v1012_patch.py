#!/usr/bin/env python3
"""Validate the v1.0.11 -> v1.0.12 patch adjudication."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
MATRIX = ROOT / "Codex/results/PHASE_058_V1012_PATCH_ADJUDICATION.json"
THEORY_DIFF = ROOT / "Codex/results/PHASE_058_THEORY_LINEAGE_DIFF.json"


class StripDocstrings(ast.NodeTransformer):
    """Remove docstrings while preserving executable AST."""

    def _strip(self, node):
        self.generic_visit(node)
        body = getattr(node, "body", None)
        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            node.body = body[1:]
        return node

    def visit_Module(self, node):
        return self._strip(node)

    def visit_FunctionDef(self, node):
        return self._strip(node)

    def visit_AsyncFunctionDef(self, node):
        return self._strip(node)

    def visit_ClassDef(self, node):
        return self._strip(node)


def executable_ast_hash(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    stripped = StripDocstrings().visit(tree)
    payload = ast.dump(stripped, include_attributes=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def numstat(old: Path, new: Path) -> tuple[int, int]:
    result = subprocess.run(
        ["git", "diff", "--no-index", "--numstat", "--", str(old), str(new)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr)
    if not result.stdout.strip():
        return 0, 0
    fields = result.stdout.strip().split("\t")
    return int(fields[0]), int(fields[1])


def load_module(path: Path, name: str):
    sys.dont_write_bytecode = True
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def representative_outputs(module) -> list[np.ndarray]:
    graphite_voltage = np.linspace(0.03, 0.34, 1400)
    lco_voltage = np.linspace(3.75, 4.15, 1200)
    graphite = module.GraphiteAnodeDischargeDQDV(
        module.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.0
    )
    lco = module.LCOCathodeDQDV(
        module.LCO_MSMR_LIT, x=0.5, Rn=0.01, Cbg=0.0
    )
    return [
        np.asarray(
            graphite.curve(
                graphite_voltage,
                direction="discharge",
                c_rate=0.2,
                Q_cell=1.0,
                T=298.15,
            )
        ),
        np.asarray(graphite.entropy_coefficient(graphite_voltage, 298.15)),
        np.asarray(
            lco.curve(
                lco_voltage,
                direction="charge",
                c_rate=0.2,
                Q_cell=1.0,
                T=298.15,
            )
        ),
        np.asarray(lco.entropy_coefficient(lco_voltage, 298.15)),
    ]


def main() -> int:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    theory_diff = json.loads(THEORY_DIFF.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}

    checks["schema"] = data["schema_version"] == "phase058-v1012-patch-adjudication-v1"
    checks["boundary"] = data["audit_boundary"] == "PATCH_CLASSIFICATION_NOT_THEORY_CANON"

    additions = 0
    deletions = 0
    changed = 0
    identical = 0
    for pair in data["file_pairs"]:
        old = ROOT / pair["old"]
        new = ROOT / pair["new"]
        pair_id = pair["role"]
        checks[f"files_exist:{pair_id}"] = old.is_file() and new.is_file()
        observed_added, observed_deleted = numstat(old, new)
        checks[f"numstat:{pair_id}"] = (
            observed_added == pair["added_lines"]
            and observed_deleted == pair["deleted_lines"]
        )
        is_equal = old.read_bytes() == new.read_bytes()
        checks[f"classification_equal:{pair_id}"] = (
            (pair["classification"] == "BYTE_IDENTICAL") == is_equal
        )
        additions += observed_added
        deletions += observed_deleted
        if is_equal:
            identical += 1
        else:
            changed += 1

    checks["file_pair_count"] = (
        len(data["file_pairs"]) == data["summary"]["file_pair_count"]
    )
    checks["changed_pair_count"] = changed == data["summary"]["changed_file_pair_count"]
    checks["identical_pair_count"] = (
        identical == data["summary"]["byte_identical_file_pair_count"]
    )
    checks["addition_total"] = additions == data["summary"]["added_lines"]
    checks["deletion_total"] = deletions == data["summary"]["deleted_lines"]

    code_pair = next(pair for pair in data["file_pairs"] if pair["role"] == "production_code")
    old_code = ROOT / code_pair["old"]
    new_code = ROOT / code_pair["new"]
    old_ast_hash = executable_ast_hash(old_code)
    new_ast_hash = executable_ast_hash(new_code)
    expected_ast_hash = data["executable_code_equivalence"][
        "docstring_stripped_ast_sha256"
    ]
    checks["executable_ast_equal"] = (
        old_ast_hash == expected_ast_hash == new_ast_hash
    )

    old_module = load_module(old_code, "phase058_v1011_patch_probe")
    new_module = load_module(new_code, "phase058_v1012_patch_probe")
    old_outputs = representative_outputs(old_module)
    new_outputs = representative_outputs(new_module)
    bit_equal = [np.array_equal(old, new) for old, new in zip(old_outputs, new_outputs)]
    max_difference = max(
        float(np.max(np.abs(old - new)))
        for old, new in zip(old_outputs, new_outputs)
    )
    checks["representative_case_count"] = (
        len(bit_equal)
        == len(data["executable_code_equivalence"]["representative_cases"])
    )
    checks["representative_outputs_bit_equal"] = (
        sum(bit_equal)
        == data["executable_code_equivalence"]["bit_identical_case_count"]
        == len(bit_equal)
    )
    checks["representative_max_difference"] = (
        max_difference
        == data["executable_code_equivalence"]["maximum_absolute_difference"]
        == 0.0
    )

    diff_by_id = {
        item["pair_id"]: item for item in theory_diff["comparisons"]
    }
    for chapter, pair_id in (
        ("chapter_1", "ch1_v1010_to_v1012"),
        ("chapter_2", "ch2_v1010_to_v1012"),
    ):
        expected = data["theory_diff"][chapter]
        equations = diff_by_id[pair_id]["labeled_equations"]
        checks[f"equations:{chapter}"] = (
            equations["old_count"] == expected["old_equations"]
            and equations["new_count"] == expected["new_equations"]
            and equations["unchanged_count"] == expected["unchanged_equations"]
            and equations["changed_count"] == expected["changed_equations"]
            and equations["added_count"] == expected["added_equations"]
            and equations["removed_count"] == expected["removed_equations"]
        )

    allowed_decisions = {
        "PRESERVE",
        "CORRECT",
        "SUPERSEDE",
        "EMPIRICAL_ONLY",
        "THEORY_ONLY",
        "REJECT",
        "UNVERIFIED",
    }
    claim_ids = [claim["id"] for claim in data["change_claims"]]
    checks["claim_ids_unique"] = len(claim_ids) == len(set(claim_ids))
    checks["claim_decisions_allowed"] = all(
        claim["decision"] in allowed_decisions for claim in data["change_claims"]
    )
    checks["claims_have_reasons"] = all(
        bool(claim["reason"].strip()) for claim in data["change_claims"]
    )

    failures = [name for name, passed in checks.items() if not passed]
    print(
        json.dumps(
            {
                "matrix": str(MATRIX.relative_to(ROOT)),
                "check_count": len(checks),
                "failures": failures,
                "file_pairs": len(data["file_pairs"]),
                "added_lines": additions,
                "deleted_lines": deletions,
                "executable_ast_hashes": [old_ast_hash, new_ast_hash],
                "representative_cases_bit_equal": bit_equal,
                "maximum_absolute_difference": max_difference,
                "gate": (
                    "PASS_P058_V1012_PATCH_ADJUDICATION"
                    if not failures
                    else "FAIL_P058_V1012_PATCH_ADJUDICATION"
                ),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
