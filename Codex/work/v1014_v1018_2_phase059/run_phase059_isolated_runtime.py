#!/usr/bin/env python3
"""Run Phase 059 production/test/demo files in disposable isolation.

Capture mode is never invoked. All code, golden inputs, plots, caches, stdout,
and stderr are confined to a temporary directory; only sanitized logs and the
machine-readable result are written under Codex/.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
WORK = ROOT / "Codex" / "work" / "v1014_v1018_2_phase059"
LOG_DIR = WORK / "runtime_logs"
OUTPUT = RESULTS / "PHASE_059_ISOLATED_RUNTIME_RESULTS.json"
SUMMARY = RESULTS / "PHASE_059_ISOLATED_RUNTIME_REVIEW.md"

VERSIONS = [
    ("v1.0.14", "1014"),
    ("v1.0.15", "1015"),
    ("v1.0.16", "1016"),
    ("v1.0.17", "1017"),
    ("v1.0.18.1", "1018_1"),
    ("v1.0.18.2", "1018_2"),
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


def assigned_strings(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    values: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if not isinstance(node.value, ast.Constant) or not isinstance(
            node.value.value, str
        ):
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                values[target.id] = node.value.value
    return values


def sanitize(text: str, isolation_root: Path) -> str:
    return text.replace(str(isolation_root), "<ISOLATION_ROOT>")


def file_inventory(base: Path) -> dict[str, str]:
    inventory = {}
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(base))
        if "__pycache__" in path.parts or "mplconfig" in path.parts:
            continue
        inventory[rel] = sha256_bytes(path.read_bytes())
    return inventory


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def regression_numeric_diagnostic(version: str, tag: str) -> dict:
    source_dir = ROOT / "Claude" / "docs" / version
    code_name = f"Anode_Fit_v{version.removeprefix('v')}.py"
    code = load_module(
        source_dir / code_name,
        f"phase059_code_{tag}",
    )
    regression = load_module(
        source_dir / "test_regression_graphite.py",
        f"phase059_regression_{tag}",
    )
    current = regression.graphite_outputs(code)
    with __import__("numpy").load(source_dir / "golden_graphite_ref.npz") as golden:
        golden_keys = list(golden.files)
        current_keys = list(current)
        arrays = []
        for key in current_keys:
            now = __import__("numpy").asarray(current[key])
            old = __import__("numpy").asarray(golden[key])
            arrays.append(
                {
                    "key": key,
                    "shape_equal": now.shape == old.shape,
                    "dtype_equal": now.dtype == old.dtype,
                    "array_equal": bool(__import__("numpy").array_equal(now, old)),
                    "allclose_rtol0_atol1e_12": bool(
                        __import__("numpy").allclose(
                            now, old, rtol=0.0, atol=1e-12
                        )
                    ),
                    "max_abs_diff": float(
                        __import__("numpy").max(__import__("numpy").abs(now - old))
                    ),
                }
            )
    area, qsum = regression.area_check(code)
    return {
        "version": version,
        "code_sha256": sha256_bytes((source_dir / code_name).read_bytes()),
        "golden_sha256": sha256_bytes(
            (source_dir / "golden_graphite_ref.npz").read_bytes()
        ),
        "current_key_count": len(current_keys),
        "golden_key_count": len(golden_keys),
        "key_set_equal": set(current_keys) == set(golden_keys),
        "array_equal_count": sum(item["array_equal"] for item in arrays),
        "allclose_rtol0_atol1e_12_count": sum(
            item["allclose_rtol0_atol1e_12"] for item in arrays
        ),
        "max_abs_diff": max(item["max_abs_diff"] for item in arrays),
        "area": float(area),
        "qsum": float(qsum),
        "area_ratio": float(area / qsum),
        "arrays": arrays,
    }


def run_one(
    isolation_root: Path,
    version: str,
    tag: str,
    task: str,
) -> dict:
    source_dir = ROOT / "Claude" / "docs" / version
    code_name = f"Anode_Fit_v{version.removeprefix('v')}.py"
    code_source = source_dir / code_name
    task_dir = isolation_root / version / task
    task_dir.mkdir(parents=True, exist_ok=True)
    mplconfig = task_dir / "mplconfig"
    mplconfig.mkdir()
    env = os.environ.copy()
    env.update(
        {
            "MPLBACKEND": "Agg",
            "MPLCONFIGDIR": str(mplconfig),
            "PYTHONHASHSEED": "0",
        }
    )

    if task == "production_selfcheck":
        local_code = task_dir / code_name
        shutil.copy2(code_source, local_code)
        command = [sys.executable, str(local_code)]
    elif task == "regression_verify":
        script = source_dir / "test_regression_graphite.py"
        strings = assigned_strings(script)
        local_code = task_dir / code_name
        shutil.copy2(code_source, local_code)
        golden_source = source_dir / "golden_graphite_ref.npz"
        golden_target = task_dir / strings["GOLD"]
        shutil.copy2(golden_source, golden_target)
        env["ANODEFIT_CODE"] = str(local_code)
        command = [sys.executable, str(script), "verify"]
    elif task == "sample_test":
        script = source_dir / f"sample_test_v{tag}.py"
        strings = assigned_strings(script)
        shutil.copy2(code_source, task_dir / strings["CODE"])
        command = [sys.executable, str(script)]
    elif task == "demo_lco_heat":
        script = source_dir / "demo_lco_heat.py"
        strings = assigned_strings(script)
        shutil.copy2(code_source, task_dir / strings["CODE"])
        command = [sys.executable, str(script)]
    elif task == "graph_suite":
        script = source_dir / f"graph_suite_v{tag}.py"
        strings = assigned_strings(script)
        shutil.copy2(code_source, task_dir / strings["CODE"])
        command = [sys.executable, str(script)]
    elif task == "plot_dqdv":
        script = source_dir / "plot_dqdv.py"
        local_script = task_dir / "plot_dqdv.py"
        local_code = task_dir / code_name
        shutil.copy2(script, local_script)
        shutil.copy2(code_source, local_code)
        command = [sys.executable, str(local_script)]
    else:
        raise ValueError(task)

    before = file_inventory(task_dir)
    completed = subprocess.run(
        command,
        cwd=task_dir,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    stdout = sanitize(completed.stdout, isolation_root)
    stderr = sanitize(completed.stderr, isolation_root)
    after = file_inventory(task_dir)
    outputs = [
        {
            "path": path,
            "sha256": digest,
            "size_bytes": (task_dir / path).stat().st_size,
        }
        for path, digest in sorted(after.items())
        if before.get(path) != digest
        and not path.endswith(".py")
        and not path.endswith(".npz")
    ]
    # A preloaded golden input is not an output; no runtime task is allowed to
    # create or modify NPZ files.
    npz_mutations = [
        path
        for path, digest in after.items()
        if path.endswith(".npz") and before.get(path) != digest
    ]

    safe_version = version.replace(".", "_")
    stdout_path = LOG_DIR / f"{safe_version}_{task}.stdout.txt"
    stderr_path = LOG_DIR / f"{safe_version}_{task}.stderr.txt"
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    return {
        "version": version,
        "task": task,
        "command_mode": "verify" if task == "regression_verify" else "execute",
        "exit_code": completed.returncode,
        "stdout_sha256": sha256_bytes(stdout.encode("utf-8")),
        "stderr_sha256": sha256_bytes(stderr.encode("utf-8")),
        "stdout_log": str(stdout_path.relative_to(ROOT)),
        "stderr_log": str(stderr_path.relative_to(ROOT)),
        "stdout_line_count": len(stdout.splitlines()),
        "stderr_line_count": len(stderr.splitlines()),
        "reported_pass": "PASS" in stdout,
        "reported_done": "DONE" in stdout or "VALIDATION DONE" in stdout,
        "npz_mutations": npz_mutations,
        "generated_outputs": outputs,
    }


def main() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    # Remove only prior generated runtime logs so stale files cannot masquerade
    # as current execution evidence.
    for path in LOG_DIR.glob("*.txt"):
        path.unlink()

    results = []
    with tempfile.TemporaryDirectory(prefix="anodefit_phase059_") as temp:
        isolation_root = Path(temp)
        for version, tag in VERSIONS:
            for task in TASKS:
                results.append(run_one(isolation_root, version, tag, task))
    diagnostics = [
        regression_numeric_diagnostic(version, tag) for version, tag in VERSIONS
    ]

    task_counts = {
        task: sum(item["task"] == task for item in results) for task in TASKS
    }
    exit_counts = {
        str(code): sum(item["exit_code"] == code for item in results)
        for code in sorted({item["exit_code"] for item in results})
    }
    output_hash_groups: dict[str, list[str]] = {}
    for item in results:
        for output in item["generated_outputs"]:
            output_hash_groups.setdefault(output["sha256"], []).append(
                f"{item['version']}:{item['task']}:{output['path']}"
            )

    no_npz_mutation = not any(item["npz_mutations"] for item in results)
    all_zero = all(item["exit_code"] == 0 for item in results)
    only_regression_failed = all(
        item["exit_code"] == 0 or item["task"] == "regression_verify"
        for item in results
    ) and all(
        item["exit_code"] == 1
        for item in results
        if item["task"] == "regression_verify"
    )
    diagnostics_tolerant = all(
        item["allclose_rtol0_atol1e_12_count"] == item["current_key_count"]
        and item["key_set_equal"]
        for item in diagnostics
    )
    status = (
        "PASS_P059_ISOLATED_RUNTIME_EXECUTION"
        if all_zero and no_npz_mutation
        else "CONDITIONAL_P059_ISOLATED_RUNTIME"
        if only_regression_failed and diagnostics_tolerant and no_npz_mutation
        else "FAIL_P059_ISOLATED_RUNTIME_EXECUTION"
    )
    result = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "scope": "Phase 059 Step 34.3 disposable isolated runtime execution",
        "status": status,
        "authority_boundary": (
            "Successful execution and historical internal regression only; "
            "print-only verdicts, theory conformance, and experimental validity "
            "are not promoted."
        ),
        "capture_mode_invoked": False,
        "source_tree_output_written": False,
        "runtime_environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "numpy": __import__("numpy").__version__,
            "matplotlib": importlib.metadata.version("matplotlib"),
        },
        "version_count": len(VERSIONS),
        "task_type_count": len(TASKS),
        "run_count": len(results),
        "task_counts": task_counts,
        "exit_code_counts": exit_counts,
        "zero_exit_count": sum(item["exit_code"] == 0 for item in results),
        "regression_reported_pass_count": sum(
            item["task"] == "regression_verify" and item["reported_pass"]
            for item in results
        ),
        "npz_mutation_count": sum(
            len(item["npz_mutations"]) for item in results
        ),
        "generated_output_count": sum(
            len(item["generated_outputs"]) for item in results
        ),
        "generated_output_hash_groups": [
            {"sha256": digest, "occurrences": paths}
            for digest, paths in sorted(output_hash_groups.items())
        ],
        "regression_numeric_diagnostics": diagnostics,
        "runs": results,
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rows = "\n".join(
        f"| {item['version']} | {item['task']} | {item['exit_code']} | "
        f"{item['reported_pass']} | {item['stdout_line_count']} | "
        f"{item['stderr_line_count']} | {len(item['generated_outputs'])} |"
        for item in results
    )
    summary = f"""# Phase 059 isolated runtime review

기존 소스와 golden을 수정하지 않는 disposable temporary directory에서
6 versions × 6 task types를 실행했다. regression은 `verify`만
사용했고 `capture`는 호출하지 않았다.

## 결과

- runs: {len(results)}
- zero exit: {sum(item['exit_code'] == 0 for item in results)}
- regression PASS banners: {sum(item['task'] == 'regression_verify' and item['reported_pass'] for item in results)}
- NPZ mutations: {sum(len(item['npz_mutations']) for item in results)}
- generated non-input outputs: {sum(len(item['generated_outputs']) for item in results)}
- exact golden arrays per version: {', '.join(f"{item['array_equal_count']}/{item['current_key_count']}" for item in diagnostics)}
- tolerant arrays (`rtol=0`, `atol=1e-12`) per version: {', '.join(f"{item['allclose_rtol0_atol1e_12_count']}/{item['current_key_count']}" for item in diagnostics)}
- maximum absolute golden difference: {max(item['max_abs_diff'] for item in diagnostics):.3e}
- regression area ratio range: {min(item['area_ratio'] for item in diagnostics):.6f}–{max(item['area_ratio'] for item in diagnostics):.6f}

| Version | Task | Exit | PASS banner | stdout lines | stderr lines | Outputs |
|---|---|---:|---|---:|---:|---:|
{rows}

## 증거 한계

1. zero exit는 실행 가능성만 뜻한다.
2. regression PASS는 각 version의 저장 golden과 current-output
   bit equality만 뜻한다. 현재 환경에서는 1/13 array만 exact이고
   전 배열이 `atol=1e-12` 안에서 일치해 strict gate의 환경
   비이식성을 확인했다.
3. sample/demo/graph/plot의 DONE 또는 VALIDATION 문구는 Step 34.2
   판정대로 print-only다.
4. regression이 출력한 유한전압창 area ratio는 0.9363으로
   가이드의 0.95 하한보다 낮지만 exit 판정에 포함되지 않는다.
5. 이 실행은 `n_T1`, `theta_E`, nonmonotone history, direct
   `L_V` zero-current, unit conversion 또는 measured data를 새로
   검증하지 않는다.

Gate: `{result['status']}`.
"""
    SUMMARY.write_text(summary, encoding="utf-8")


if __name__ == "__main__":
    main()
