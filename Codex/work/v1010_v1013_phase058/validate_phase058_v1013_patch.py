#!/usr/bin/env python3
"""Validate the exact v1.0.12 to v1.0.13 patch adjudication."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
RESULT = ROOT / "Codex/results/PHASE_058_V1013_PATCH_ADJUDICATION.json"
GOLDEN_AUDIT = ROOT / "Codex/results/PHASE_058_GOLDEN_NPZ_AUDIT.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def patch_numstat(old: Path, new: Path) -> tuple[int, int]:
    process = subprocess.run(
        ["git", "diff", "--no-index", "--numstat", str(old), str(new)],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if process.returncode not in (0, 1):
        raise RuntimeError(process.stderr)
    line = process.stdout.strip().splitlines()[0]
    added, deleted, _ = line.split("\t", 2)
    return int(added), int(deleted)


def strip_docstrings(tree: ast.AST) -> ast.AST:
    for node in ast.walk(tree):
        if isinstance(
            node,
            (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef),
        ):
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                node.body = node.body[1:]
    return tree


def callable_fingerprints(path: Path) -> dict[str, str]:
    tree = strip_docstrings(ast.parse(path.read_text(encoding="utf-8")))
    result: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result[node.name] = hashlib.sha256(
                ast.dump(node, include_attributes=False).encode()
            ).hexdigest()
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    name = f"{node.name}.{child.name}"
                    result[name] = hashlib.sha256(
                        ast.dump(child, include_attributes=False).encode()
                    ).hexdigest()
    return result


EQUATION_PATTERN = re.compile(
    r"\\begin\{(equation|align|gather|multline)\*?\}"
    r"(.*?)"
    r"\\end\{\1\*?\}",
    re.DOTALL,
)


def equation_fingerprints(path: Path) -> dict[str, str]:
    source = path.read_text(encoding="utf-8")
    result: dict[str, str] = {}
    for _, body in EQUATION_PATTERN.findall(source):
        normalized = re.sub(r"\s+", " ", body).strip()
        for label in re.findall(r"\\label\{(eq:[^}]+)", body):
            result[label] = hashlib.sha256(normalized.encode()).hexdigest()
    return result


def text_metrics(path: Path) -> dict[str, int]:
    source = path.read_text(encoding="utf-8")
    return {
        "lines": len(source.splitlines()),
        "equation_labels": len(re.findall(r"\\label\{eq:", source)),
        "boxed_occurrences": source.count("\\boxed"),
        "section_headings": len(
            re.findall(r"^\\(?:section|subsection|subsubsection)\{", source, re.MULTILINE)
        ),
    }


def load_module(path: Path, name: str):
    sys.dont_write_bytecode = True
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def assert_count(path: Path) -> int:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return sum(isinstance(node, ast.Assert) for node in ast.walk(tree))


def main() -> int:
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    golden_audit = json.loads(GOLDEN_AUDIT.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}
    checks["schema"] = (
        data["schema_version"] == "phase058-v1013-patch-adjudication-v1"
    )
    checks["boundary"] = (
        data["audit_boundary"]
        == "V1012_TO_V1013_EXACT_PATCH_AND_EXECUTABLE_BEHAVIOR_NOT_EXTERNAL_VALIDATION"
    )

    source_paths = {
        "v1012_code": ROOT / "Claude/docs/v1.0.12/Anode_Fit_v1.0.12.py",
        "v1013_code": ROOT / "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py",
        "v1012_ch1": ROOT / "Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex",
        "v1013_ch1": ROOT / "Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex",
        "v1012_ch2": ROOT / "Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex",
        "v1013_ch2": ROOT / "Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex",
        "v1012_regression": ROOT
        / "Claude/docs/v1.0.12/test_regression_graphite.py",
        "v1013_regression": ROOT
        / "Claude/docs/v1.0.13/test_regression_graphite.py",
        "v1013_golden": ROOT / "Claude/docs/v1.0.13/golden_graphite_ref.npz",
    }
    for name, path in source_paths.items():
        checks[f"hash_{name}"] = sha256(path) == data["source_hashes"][name]

    commit_output = subprocess.run(
        ["git", "log", "--format=%H", "--", "Claude/docs/v1.0.13"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.splitlines()
    checks["lineage_commit_count"] = (
        len(commit_output) == data["lineage"]["v1013_docs_commit_count"]
    )
    checks["lineage_first_commit"] = (
        commit_output[-1] == data["lineage"]["first_v1013_commit"]
    )
    checks["lineage_final_commit"] = (
        commit_output[0] == data["lineage"]["final_v1013_commit"]
    )

    patch_added = 0
    patch_deleted = 0
    for pair in data["paired_text_patch"]:
        added, deleted = patch_numstat(ROOT / pair["old"], ROOT / pair["new"])
        checks[f"patch_{pair['role']}"] = (
            added == pair["added_lines"] and deleted == pair["deleted_lines"]
        )
        patch_added += added
        patch_deleted += deleted
    checks["patch_total_added"] = (
        patch_added == data["paired_text_totals"]["added_lines"]
    )
    checks["patch_total_deleted"] = (
        patch_deleted == data["paired_text_totals"]["deleted_lines"]
    )

    for artifact in data["new_text_artifacts"]:
        checks[f"new_artifact_{Path(artifact['path']).name}"] = (
            len((ROOT / artifact["path"]).read_text(encoding="utf-8").splitlines())
            == artifact["lines"]
        )

    theory = data["theory_patch"]
    for chapter, old_key, new_key in (
        ("chapter_1", "v1012_ch1", "v1013_ch1"),
        ("chapter_2", "v1012_ch2", "v1013_ch2"),
    ):
        section = theory[chapter]
        old_metrics = text_metrics(source_paths[old_key])
        new_metrics = text_metrics(source_paths[new_key])
        for metric in ("lines", "equation_labels", "boxed_occurrences", "section_headings"):
            checks[f"{chapter}_v1012_{metric}"] = (
                old_metrics[metric] == section[f"v1012_{metric}"]
            )
            checks[f"{chapter}_v1013_{metric}"] = (
                new_metrics[metric] == section[f"v1013_{metric}"]
            )

    ch1_old_equations = equation_fingerprints(source_paths["v1012_ch1"])
    ch1_new_equations = equation_fingerprints(source_paths["v1013_ch1"])
    checks["ch1_common_labels"] = (
        len(ch1_old_equations.keys() & ch1_new_equations.keys())
        == theory["chapter_1"]["common_equation_labels"]
    )
    checks["ch1_added_labels"] = (
        sorted(ch1_new_equations.keys() - ch1_old_equations.keys())
        == theory["chapter_1"]["added_equation_labels"]
    )
    checks["ch1_removed_labels"] = (
        sorted(ch1_old_equations.keys() - ch1_new_equations.keys())
        == theory["chapter_1"]["removed_equation_labels"]
    )
    checks["ch1_changed_common_labels"] = (
        sorted(
            label
            for label in ch1_old_equations.keys() & ch1_new_equations.keys()
            if ch1_old_equations[label] != ch1_new_equations[label]
        )
        == theory["chapter_1"]["changed_common_equation_labels"]
    )
    ch2_old_equations = equation_fingerprints(source_paths["v1012_ch2"])
    ch2_new_equations = equation_fingerprints(source_paths["v1013_ch2"])
    checks["ch2_changed_labels"] = (
        sorted(
            label
            for label in ch2_old_equations.keys() & ch2_new_equations.keys()
            if ch2_old_equations[label] != ch2_new_equations[label]
        )
        == theory["chapter_2"]["changed_equation_labels"]
    )

    old_callables = callable_fingerprints(source_paths["v1012_code"])
    new_callables = callable_fingerprints(source_paths["v1013_code"])
    production = data["production_ast"]
    changed_callables = sorted(
        name
        for name in old_callables.keys() & new_callables.keys()
        if old_callables[name] != new_callables[name]
    )
    checks["callable_counts"] = (
        len(old_callables) == production["v1012_callable_count"]
        and len(new_callables) == production["v1013_callable_count"]
    )
    checks["unchanged_callable_count"] = (
        sum(
            old_callables[name] == new_callables[name]
            for name in old_callables.keys() & new_callables.keys()
        )
        == production["unchanged_callable_count"]
    )
    checks["changed_callables"] = changed_callables == production["changed_callables"]
    checks["added_callables"] = (
        sorted(new_callables.keys() - old_callables.keys())
        == production["added_callables"]
    )
    checks["removed_callables"] = (
        sorted(old_callables.keys() - new_callables.keys())
        == production["removed_callables"]
    )

    v12 = load_module(source_paths["v1012_code"], "phase058_patch_v1012")
    v13 = load_module(source_paths["v1013_code"], "phase058_patch_v1013")
    behavior = data["behavior_probe"]
    voltage_g = np.linspace(0.03, 0.34, 1000)
    graphite12 = v12.GraphiteAnodeDischargeDQDV(
        v12.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True
    )
    graphite13 = v13.GraphiteAnodeDischargeDQDV(
        v13.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True
    )
    vector_differences = [
        float(
            np.max(
                np.abs(
                    graphite12.equilibrium(voltage_g, 298.15)
                    - graphite13.equilibrium(voltage_g, 298.15)
                )
            )
        )
    ]
    for direction in (+1, -1):
        for current in (0.02, 0.2, 1.0):
            vector_differences.append(
                float(
                    np.max(
                        np.abs(
                            graphite12.dqdv(
                                voltage_g, 298.15, current, 1.0, direction
                            )
                            - graphite13.dqdv(
                                voltage_g, 298.15, current, 1.0, direction
                            )
                        )
                    )
                )
            )
    vector_differences.append(
        float(
            np.max(
                np.abs(
                    graphite12.entropy_coefficient(voltage_g, 298.15)
                    - graphite13.entropy_coefficient(voltage_g, 298.15)
                )
            )
        )
    )
    checks["graphite_vector_case_count"] = (
        len(vector_differences) == behavior["graphite_vector_case_count"]
    )
    checks["graphite_vector_bit_exact"] = (
        max(vector_differences) == behavior["graphite_vector_max_abs_difference"] == 0.0
    )

    scalar = behavior["shipped_scalar_dqdv_at_0p12v"]
    scalar12 = float(
        np.asarray(graphite12.dqdv(0.12, 298.15, 1.0, 1.0, +1)).reshape(-1)[0]
    )
    scalar13 = float(
        np.asarray(graphite13.dqdv(0.12, 298.15, 1.0, 1.0, +1)).reshape(-1)[0]
    )
    equilibrium_reference = float(
        np.asarray(graphite13.equilibrium(0.11, 298.15)).reshape(-1)[0]
    )
    checks["scalar_v1012"] = math.isclose(
        scalar12, scalar["v1012"], rel_tol=0.0, abs_tol=1.0e-15
    )
    checks["scalar_v1013"] = math.isclose(
        scalar13, scalar["v1013"], rel_tol=0.0, abs_tol=1.0e-15
    )
    checks["scalar_equilibrium_reference"] = math.isclose(
        equilibrium_reference,
        scalar["equilibrium_reference"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )
    checks["scalar_relative_error"] = math.isclose(
        (scalar12 - equilibrium_reference) / equilibrium_reference,
        scalar["v1012_relative_error"],
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    for key, transition in (
        (
            "entropy_n2_at_xi_0p8_v_per_k",
            {"dH_rxn": -13000.0, "dS_rxn": -16.0, "Q": 1.0, "n": 2.0},
        ),
        (
            "entropy_w_only_at_xi_0p8_v_per_k",
            {"dH_rxn": -13000.0, "dS_rxn": -16.0, "Q": 1.0, "w": 0.04},
        ),
    ):
        model12 = v12.GraphiteAnodeDischargeDQDV([transition], Rn=0.0, Cbg=0.0)
        model13 = v13.GraphiteAnodeDischargeDQDV([transition], Rn=0.0, Cbg=0.0)
        center = float(v13.func_U_j(298.15, -13000.0, -16.0))
        width = float(model13._width(transition, 298.15))
        voltage = center + width * math.log(4.0)
        value12 = float(
            np.asarray(model12.entropy_coefficient(voltage, 298.15)).reshape(-1)[0]
        )
        value13 = float(
            np.asarray(model13.entropy_coefficient(voltage, 298.15)).reshape(-1)[0]
        )
        stored = behavior[key]
        checks[f"{key}_v1012"] = math.isclose(
            value12, stored["v1012"], rel_tol=0.0, abs_tol=1.0e-18
        )
        checks[f"{key}_v1013"] = math.isclose(
            value13, stored["v1013"], rel_tol=0.0, abs_tol=1.0e-18
        )
        checks[f"{key}_delta"] = math.isclose(
            value13 - value12, stored["delta"], rel_tol=0.0, abs_tol=1.0e-18
        )

    voltage_c = np.linspace(3.75, 4.15, 1200)
    lco12 = v12.LCOCathodeDQDV(v12.LCO_MSMR_LIT, x=0.5, Rn=0.01, Cbg=0.0)
    lco13 = v13.LCOCathodeDQDV(v13.LCO_MSMR_LIT, x=0.5, Rn=0.01, Cbg=0.0)
    for temperature_text, expected in behavior[
        "lco_direct_s_plus_max_abs_difference"
    ].items():
        temperature = float(temperature_text)
        difference = float(
            np.max(
                np.abs(
                    lco12.dqdv(voltage_c, temperature, 0.2, 1.0, +1)
                    - lco13.dqdv(voltage_c, temperature, 0.2, 1.0, +1)
                )
            )
        )
        checks[f"lco_direct_{temperature_text}"] = math.isclose(
            difference, expected, rel_tol=0.0, abs_tol=1.0e-12
        )
    for temperature_text, expected in behavior[
        "lco_entropy_max_abs_difference_v_per_k"
    ].items():
        temperature = float(temperature_text)
        difference = float(
            np.max(
                np.abs(
                    lco12.entropy_coefficient(voltage_c, temperature)
                    - lco13.entropy_coefficient(voltage_c, temperature)
                )
            )
        )
        checks[f"lco_entropy_{temperature_text}"] = math.isclose(
            difference, expected, rel_tol=0.0, abs_tol=1.0e-15
        )

    mapping = behavior["lco_curve_direction_mapping"]
    mapping_values = {
        "v1012_charge_vs_low_level_s_plus_max_difference": float(
            np.max(
                np.abs(
                    lco12.curve(voltage_c, "charge", 0.2, 1.0, 298.15)
                    - lco12.dqdv(voltage_c, 298.15, 0.2, 1.0, +1)
                )
            )
        ),
        "v1012_discharge_vs_low_level_s_plus_max_difference": float(
            np.max(
                np.abs(
                    lco12.curve(voltage_c, "discharge", 0.2, 1.0, 298.15)
                    - lco12.dqdv(voltage_c, 298.15, 0.2, 1.0, +1)
                )
            )
        ),
        "v1013_charge_vs_low_level_s_plus_max_difference": float(
            np.max(
                np.abs(
                    lco13.curve(voltage_c, "charge", 0.2, 1.0, 298.15)
                    - lco13.dqdv(voltage_c, 298.15, 0.2, 1.0, +1)
                )
            )
        ),
        "v1013_discharge_vs_low_level_s_plus_max_difference": float(
            np.max(
                np.abs(
                    lco13.curve(voltage_c, "discharge", 0.2, 1.0, 298.15)
                    - lco13.dqdv(voltage_c, 298.15, 0.2, 1.0, +1)
                )
            )
        ),
    }
    for key, value in mapping_values.items():
        checks[f"direction_{key}"] = math.isclose(
            value, mapping[key], rel_tol=0.0, abs_tol=1.0e-12
        )

    reassignment = data["lco_default_reassignment"]
    electronic12 = [
        index for index, item in enumerate(v12.LCO_MSMR_LIT) if item.get("electronic")
    ]
    electronic13 = [
        index for index, item in enumerate(v13.LCO_MSMR_LIT) if item.get("electronic")
    ]
    checks["lco_electronic_indices"] = (
        electronic12 == [reassignment["v1012_electronic_transition_index"]]
        and electronic13 == [reassignment["v1013_electronic_transition_index"]]
    )
    checks["lco_x_mit"] = (
        v12.LCO_MSMR_LIT[electronic12[0]]["x_MIT"] == reassignment["v1012_x_mit"]
        and v13.LCO_MSMR_LIT[electronic13[0]]["x_MIT"]
        == reassignment["v1013_x_mit"]
    )
    checks["lco_dh_recenter"] = (
        v12.LCO_MSMR_LIT[0]["dH_rxn"]
        == reassignment["v1012_dh_index_0_j_per_mol"]
        and v13.LCO_MSMR_LIT[0]["dH_rxn"]
        == reassignment["v1013_dh_index_0_j_per_mol"]
        and v12.LCO_MSMR_LIT[1]["dH_rxn"]
        == reassignment["v1012_dh_index_1_j_per_mol"]
        and v13.LCO_MSMR_LIT[1]["dH_rxn"]
        == reassignment["v1013_dh_index_1_j_per_mol"]
    )

    regression = data["regression_and_validation"]
    regression12_text = source_paths["v1012_regression"].read_text(encoding="utf-8")
    regression13_text = source_paths["v1013_regression"].read_text(encoding="utf-8")
    checks["regression_assert_counts"] = (
        assert_count(source_paths["v1012_regression"])
        == regression["v1012_python_assert_count"]
        == 0
        and assert_count(source_paths["v1013_regression"])
        == regression["v1013_python_assert_count"]
        == 0
    )
    checks["regression_default_verify"] = (
        'else "verify"' in regression13_text
        and regression["v1013_default_mode"] == "verify"
    )
    checks["regression_unknown_mode_exit"] = (
        "sys.exit(2)" in regression13_text
        and regression["v1013_unknown_mode_exit_code"] == 2
    )
    checks["regression_code_env"] = (
        "ANODEFIT_CODE" in regression13_text
        and regression["v1013_code_path_environment_override"]
    )
    checks["regression_gold_not_env"] = (
        "ANODEFIT_GOLD" not in regression13_text
        and regression["v1013_golden_path_environment_override"] is False
        and "D:\\Projects\\Project_Anode_Fit" in regression13_text
    )
    checks["regression_changed_paths_uncovered"] = (
        "entropy_coefficient" not in regression13_text
        and "LCOCathodeDQDV" not in regression13_text
        and regression["changed_scalar_path_covered"] is False
        and regression["changed_entropy_paths_covered"] is False
        and regression["changed_lco_defaults_or_direction_covered"] is False
    )
    checks["golden_audit_counts"] = (
        golden_audit["array_count"] == regression["v1013_golden_array_count"]
        and sum(item["bit_exact"] for item in golden_audit["arrays"])
        == regression["current_environment_bit_exact_array_count"]
        and sum(
            item["allclose_rtol1e12_atol1e12"] for item in golden_audit["arrays"]
        )
        == regression["current_environment_allclose_1e12_array_count"]
        and math.isclose(
            max(item["max_abs_diff"] for item in golden_audit["arrays"]),
            regression["maximum_current_environment_absolute_difference"],
            rel_tol=0.0,
            abs_tol=1.0e-30,
        )
    )
    checks["v1012_hardcodes_old_code"] = "v1.0.10" in regression12_text

    claims = data["claim_dispositions"]
    claim_ids = [item["id"] for item in claims]
    checks["claim_count"] = len(claims) == 13
    checks["claim_ids_unique"] = len(claim_ids) == len(set(claim_ids))

    failures = [name for name, passed in checks.items() if not passed]
    print(
        json.dumps(
            {
                "artifact": str(RESULT.relative_to(ROOT)),
                "check_count": len(checks),
                "failures": failures,
                "paired_patch_added": patch_added,
                "paired_patch_deleted": patch_deleted,
                "changed_callables": changed_callables,
                "graphite_vector_max_abs_difference": max(vector_differences),
                "scalar_v1012": scalar12,
                "scalar_v1013": scalar13,
                "lco_direction_mapping": mapping_values,
                "verdict": data["verdict"],
                "gate": (
                    "PASS_P058_V1013_PATCH_ADJUDICATION"
                    if not failures
                    else "FAIL_P058_V1013_PATCH_ADJUDICATION"
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
