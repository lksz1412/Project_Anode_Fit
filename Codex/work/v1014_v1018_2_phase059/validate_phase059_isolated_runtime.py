#!/usr/bin/env python3
"""Validate Phase 059 disposable runtime evidence and its authority boundary."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
OUTPUT = RESULTS / "PHASE_059_ISOLATED_RUNTIME_RESULTS.json"
SUMMARY = RESULTS / "PHASE_059_ISOLATED_RUNTIME_REVIEW.md"

VERSIONS = [
    "v1.0.14",
    "v1.0.15",
    "v1.0.16",
    "v1.0.17",
    "v1.0.18.1",
    "v1.0.18.2",
]
TASKS = [
    "production_selfcheck",
    "regression_verify",
    "sample_test",
    "demo_lco_heat",
    "graph_suite",
    "plot_dqdv",
]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def main() -> None:
    result = json.loads(OUTPUT.read_text(encoding="utf-8"))
    runs = result["runs"]
    diagnostics = result["regression_numeric_diagnostics"]
    checks: list[tuple[str, bool]] = []
    checks.append(("summary exists", SUMMARY.is_file()))
    checks.append(
        (
            "status conditional",
            result["status"] == "CONDITIONAL_P059_ISOLATED_RUNTIME",
        )
    )
    checks.append(("capture not invoked", result["capture_mode_invoked"] is False))
    checks.append(
        ("source output not written", result["source_tree_output_written"] is False)
    )
    checks.append(("version count", result["version_count"] == 6))
    checks.append(("task type count", result["task_type_count"] == 6))
    checks.append(("run count", result["run_count"] == len(runs) == 36))
    checks.append(
        (
            "version task cartesian product",
            {(item["version"], item["task"]) for item in runs}
            == {(version, task) for version in VERSIONS for task in TASKS},
        )
    )
    checks.append(("zero exit count", result["zero_exit_count"] == 30))
    checks.append(
        (
            "exit code counts",
            result["exit_code_counts"] == {"0": 30, "1": 6},
        )
    )
    checks.append(
        (
            "only regressions fail",
            all(
                item["exit_code"]
                == (1 if item["task"] == "regression_verify" else 0)
                for item in runs
            ),
        )
    )
    checks.append(
        (
            "no regression PASS banner",
            result["regression_reported_pass_count"] == 0
            and all(
                not item["reported_pass"]
                for item in runs
                if item["task"] == "regression_verify"
            ),
        )
    )
    checks.append(
        (
            "no npz mutation",
            result["npz_mutation_count"] == 0
            and all(not item["npz_mutations"] for item in runs),
        )
    )
    checks.append(
        (
            "twenty-four generated outputs",
            result["generated_output_count"] == 24
            and sum(len(item["generated_outputs"]) for item in runs) == 24,
        )
    )
    checks.append(
        (
            "visual tasks each output once",
            all(
                len(item["generated_outputs"])
                == (
                    1
                    if item["task"]
                    in {"sample_test", "demo_lco_heat", "graph_suite", "plot_dqdv"}
                    else 0
                )
                for item in runs
            ),
        )
    )

    logs_exact = True
    logs_sanitized = True
    for item in runs:
        for stream in ("stdout", "stderr"):
            path = ROOT / item[f"{stream}_log"]
            raw = path.read_bytes()
            text = raw.decode("utf-8")
            logs_exact &= (
                item[f"{stream}_sha256"] == sha256_bytes(raw)
                and item[f"{stream}_line_count"] == len(text.splitlines())
            )
            logs_sanitized &= "anodefit_phase059_" not in text
    checks.append(("runtime logs exact", logs_exact))
    checks.append(("temporary paths sanitized", logs_sanitized))
    checks.append(
        (
            "regression logs report failure",
            all(
                "GRAPHITE 0-DIFF: FAIL" in (
                    ROOT / item["stdout_log"]
                ).read_text(encoding="utf-8")
                for item in runs
                if item["task"] == "regression_verify"
            ),
        )
    )

    checks.append(("diagnostic count", len(diagnostics) == 6))
    checks.append(
        (
            "diagnostic versions exact",
            [item["version"] for item in diagnostics] == VERSIONS,
        )
    )
    checks.append(
        (
            "golden key sets exact",
            all(
                item["current_key_count"] == 13
                and item["golden_key_count"] == 13
                and item["key_set_equal"]
                for item in diagnostics
            ),
        )
    )
    checks.append(
        (
            "strict equality one of thirteen",
            all(item["array_equal_count"] == 1 for item in diagnostics),
        )
    )
    checks.append(
        (
            "tolerant equality thirteen of thirteen",
            all(
                item["allclose_rtol0_atol1e_12_count"] == 13
                for item in diagnostics
            ),
        )
    )
    checks.append(
        (
            "floating differences tiny",
            0.0 < max(item["max_abs_diff"] for item in diagnostics) < 5e-15,
        )
    )
    checks.append(
        (
            "area ratio below guide threshold",
            all(item["area_ratio"] < 0.95 for item in diagnostics)
            and all(item["area_ratio"] > 0.93 for item in diagnostics),
        )
    )
    checks.append(
        (
            "diagnostic source hashes exact",
            all(
                item["code_sha256"]
                == sha256_bytes(
                    (
                        ROOT
                        / "Claude"
                        / "docs"
                        / item["version"]
                        / f"Anode_Fit_v{item['version'].removeprefix('v')}.py"
                    ).read_bytes()
                )
                and item["golden_sha256"]
                == sha256_bytes(
                    (
                        ROOT
                        / "Claude"
                        / "docs"
                        / item["version"]
                        / "golden_graphite_ref.npz"
                    ).read_bytes()
                )
                for item in diagnostics
            ),
        )
    )
    checks.append(
        (
            "array diagnostic structure",
            all(
                len(item["arrays"]) == 13
                and all(array["shape_equal"] for array in item["arrays"])
                and all(array["dtype_equal"] for array in item["arrays"])
                for item in diagnostics
            ),
        )
    )
    checks.append(
        (
            "runtime environment recorded",
            all(
                result["runtime_environment"].get(key)
                for key in ("python", "implementation", "platform", "numpy", "matplotlib")
            ),
        )
    )

    claude_status = subprocess.run(
        ["git", "status", "--porcelain", "--", "Claude"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    checks.append(
        (
            "Claude source tree clean",
            claude_status.returncode == 0 and not claude_status.stdout.strip(),
        )
    )

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}")
    if failed:
        raise SystemExit(f"PHASE 059 ISOLATED RUNTIME FAIL: {failed}")
    print(
        "CONDITIONAL_P059_ISOLATED_RUNTIME_VALIDATED "
        f"checks={len(checks)}/{len(checks)} runs=36"
    )


if __name__ == "__main__":
    main()
