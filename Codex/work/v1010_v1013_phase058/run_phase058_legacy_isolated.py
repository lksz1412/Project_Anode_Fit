#!/usr/bin/env python3
"""Run Phase 058 legacy tests/demos from disposable directories.

Every source is copied byte-for-byte to a fresh temporary directory.  Windows
path literals are reproduced as Linux filenames where needed, so the source is
not patched.  Repository hashes are checked before and after execution.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Codex" / "results" / "PHASE_058_LEGACY_ISOLATED_EXECUTION.json"
TIMEOUT_SECONDS = 120

CASES = [
    ("Claude/docs/v1.0.10/sample_test_v1010.py", "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py", []),
    ("Claude/docs/v1.0.10/test_regression_graphite.py", "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py", ["verify"]),
    ("Claude/docs/v1.0.12/sample_test_v1012.py", "Claude/docs/v1.0.12/Anode_Fit_v1.0.12.py", []),
    ("Claude/docs/v1.0.13/sample_test_v1013.py", "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py", []),
    ("Claude/docs/v1.0.13/test_regression_graphite.py", "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py", ["verify"]),
    ("Claude/docs/v1.0.10/demo_lco_heat.py", "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py", []),
    ("Claude/docs/v1.0.10/graph_suite_p5.py", "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py", []),
    ("Claude/docs/v1.0.10/plot_dqdv.py", "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py", []),
    ("Claude/docs/v1.0.13/demo_lco_heat.py", "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py", []),
    ("Claude/docs/v1.0.13/graph_suite_v1013.py", "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py", []),
    ("Claude/docs/v1.0.13/plot_dqdv.py", "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py", []),
]
V1013_GOLD = ROOT / "Claude/docs/v1.0.13/golden_graphite_ref.npz"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def top_level_strings(source: str) -> dict[str, str]:
    tree = ast.parse(source)
    values: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name) or target.id not in {"CODE", "OUT", "GOLD"}:
                continue
            try:
                value = ast.literal_eval(node.value)
            except Exception:
                value = None
            if isinstance(value, str):
                values[target.id] = value
    # v1.0.13 regression wraps CODE in os.environ.get, but GOLD is plain.
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "get"
            and len(node.args) >= 2
        ):
            try:
                key = ast.literal_eval(node.args[0])
                default = ast.literal_eval(node.args[1])
            except Exception:
                continue
            if key == "ANODEFIT_CODE" and isinstance(default, str):
                values["CODE"] = default
    return values


def generated_inventory(directory: Path, inputs: set[str]) -> list[dict]:
    records = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        relative = str(path.relative_to(directory))
        if relative in inputs or relative.startswith(".mplconfig/"):
            continue
        records.append(
            {
                "path": relative,
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return records


def reported_max_abs_diff(stdout: str) -> float | None:
    values = [
        float(value)
        for value in re.findall(r"max_abs_diff=([0-9.]+e[+-][0-9]+)", stdout)
    ]
    return max(values) if values else None


def classify(path: str, returncode: int, stdout: str, stderr: str) -> str:
    if returncode == 0:
        if "test_regression_graphite.py" in path:
            return "PASS_INTERNAL_BIT_EXACT_ONLY"
        return "EXECUTED_REPORT_ONLY"
    if "test_regression_graphite.py" in path and (
        "No such file or directory" in stderr or "FileNotFoundError" in stderr
    ):
        return "BLOCKED_MISSING_FROZEN_GOLDEN"
    if "No such file or directory" in stderr or "FileNotFoundError" in stderr:
        return "BLOCKED_FROZEN_PATH"
    if "ModuleNotFoundError" in stderr or "ImportError" in stderr:
        return "BLOCKED_DEPENDENCY"
    if (
        "test_regression_graphite.py" in path
        and "GRAPHITE 0-DIFF: FAIL" in stdout
        and reported_max_abs_diff(stdout) is not None
    ):
        return "FAIL_BIT_EXACT_GOLDEN_FLOAT_DRIFT"
    return "EXECUTION_FAILURE"


def run_case(script_rel: str, model_rel: str, arguments: list[str]) -> dict:
    script_source = (ROOT / script_rel).read_text(encoding="utf-8")
    path_literals = top_level_strings(script_source)
    with tempfile.TemporaryDirectory(prefix="phase058-") as tmp:
        sandbox = Path(tmp)
        script_copy = sandbox / Path(script_rel).name
        model_copy = sandbox / Path(model_rel).name
        shutil.copy2(ROOT / script_rel, script_copy)
        shutil.copy2(ROOT / model_rel, model_copy)
        inputs = {script_copy.name, model_copy.name}

        code_literal = path_literals.get("CODE")
        if code_literal:
            code_alias = sandbox / code_literal
            shutil.copy2(ROOT / model_rel, code_alias)
            inputs.add(code_literal)

        gold_literal = path_literals.get("GOLD")
        if gold_literal and "v1.0.13/test_regression_graphite.py" in script_rel:
            gold_alias = sandbox / gold_literal
            shutil.copy2(V1013_GOLD, gold_alias)
            inputs.add(gold_literal)

        environment = os.environ.copy()
        mpl_config = sandbox / ".mplconfig"
        mpl_config.mkdir()
        environment.update(
            {
                "MPLBACKEND": "Agg",
                "MPLCONFIGDIR": str(mpl_config),
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONHASHSEED": "0",
                "ANODEFIT_CODE": str(model_copy),
            }
        )
        try:
            completed = subprocess.run(
                [sys.executable, script_copy.name, *arguments],
                cwd=sandbox,
                env=environment,
                text=True,
                capture_output=True,
                timeout=TIMEOUT_SECONDS,
                check=False,
            )
            returncode = completed.returncode
            stdout = completed.stdout
            stderr = completed.stderr
            timed_out = False
        except subprocess.TimeoutExpired as error:
            returncode = 124
            stdout = error.stdout or ""
            stderr = error.stderr or ""
            timed_out = True
        stdout = stdout.replace(str(sandbox), "<TEMP>")
        stderr = stderr.replace(str(sandbox), "<TEMP>")
        return {
            "script": script_rel,
            "model": model_rel,
            "arguments": arguments,
            "source_execution_mode": "BYTE_IDENTICAL_TEMP_COPY",
            "timeout_seconds": TIMEOUT_SECONDS,
            "timed_out": timed_out,
            "returncode": returncode,
            "classification": "BLOCKED_TIMEOUT"
            if timed_out
            else classify(script_rel, returncode, stdout, stderr),
            "reported_max_abs_diff": reported_max_abs_diff(stdout),
            "stdout": stdout,
            "stderr": stderr,
            "path_literals": path_literals,
            "generated_files": generated_inventory(sandbox, inputs),
        }


def main() -> None:
    protected = sorted(
        {str(ROOT / script) for script, _, _ in CASES}
        | {str(ROOT / model) for _, model, _ in CASES}
        | {str(V1013_GOLD)}
    )
    before = {path: sha256(Path(path)) for path in protected}
    results = [run_case(*case) for case in CASES]
    after = {path: sha256(Path(path)) for path in protected}
    unchanged = before == after
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "execution_isolation": {
            "temporary_directories": True,
            "repository_sources_executed_in_place": False,
            "repository_source_hashes_unchanged": unchanged,
            "protected_source_sha256_before": before,
            "protected_source_sha256_after": after,
        },
        "case_count": len(results),
        "classification_counts": {
            label: sum(result["classification"] == label for result in results)
            for label in sorted({result["classification"] for result in results})
        },
        "results": results,
        "interpretation_rule": "Execution success means the legacy artifact ran in isolation; it is not a physical-validity verdict.",
        "validation": {
            "all_cases_disposed": len(results) == len(CASES),
            "sources_unchanged": unchanged,
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
