#!/usr/bin/env python3
"""Build Phase 067 Step 89 fitting-evidence authority records without running fits."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "7b81814017ffd4207cc2a13fabbbe68281075b00"
SUPPLEMENTAL_COMMIT = "e3e1a634f34b711aa4803fd190fe9120f1755f13"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
DATE = "2026-09-06"
SUBJECT = "audit(phase067): separate fitting evidence authority"
GATE = "PASS_P067_STEP89_FITTING_AUTHORITY"
PERSISTENCE = "PASS_P067_STEP89_PERSISTENCE"
MATRIX_PATH = "Codex/results/PHASE_067_FITTING_EVIDENCE_MATRIX.json"
RUNTIME_PATH = "Codex/results/PHASE_067_FITTING_RUNTIME_ATTESTATION.json"

FIT_PROVENANCE = "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json"
FIT_REPRODUCTION = "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json"
OPTIMIZER_STATE = "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json"
EMPIRICAL_AUTHORITY = "Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json"
CARRY_FORWARD = "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json"
PHASE065_AUTHORITY = "Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json"
PARENT_INPUTS = (FIT_PROVENANCE, FIT_REPRODUCTION, OPTIMIZER_STATE,
                 EMPIRICAL_AUTHORITY, CARRY_FORWARD, PHASE065_AUTHORITY)
PARENT_EXPECTED = {
    FIT_PROVENANCE: ("ce8b9b8d6c2941833351f1651ec85b4e9075b96bdcfd1cc93bbc16ccb4e7a6e0",
                     "e56db8c1eb226596d5bee98147444125d030fe969422dd542241eb64692b5a4e"),
    FIT_REPRODUCTION: ("ff8141e7f0d950cfb6f588f41743e7b9221c5f4cb73ecc76522b0beb45a70d80",
                       "567c8b65886851e34fff8e913e6ad81819d8ce022001df6bf20a9b26fce6b029"),
    OPTIMIZER_STATE: ("d9dead0f766abeed899e7357b964719361054d87e31ded971fb3640b3182656e",
                      "86842e6e53164271b70ae4b9410223b9aa40be4d85692c15f669c5c08a5b7418"),
    EMPIRICAL_AUTHORITY: ("2bb07774d5ea59b578dcfc1520a3e524ec32b42ca590a90b5cca967ae63499a1",
                          "ccf7a972cd5a061840cf83bd3d6861bd3c840361433245d5fbf75ad3445a62ba"),
    CARRY_FORWARD: ("847e74956d16cc9bdcc42c36b0ddd1d73ea5ac79464d55461d2e08cf09a60003",
                    "b7847cd1ce29fee7b0304c1ee92e81645ab149949a80aab1d9c6fc77003856c6"),
    PHASE065_AUTHORITY: ("070fccb26410dd62fcf75e2d251420943229ca7e3cdc2ab0fa66e455d58f40e4",
                         "c3518b8aa690c480aad40df07d92d65b2570f2ba79dc6c0e4b15eee8b09de401"),
}

SUPPLEMENTAL_PATHS = (
    "Claude/results/comp_v24/sintef_data/sigr.csv",
    "Claude/results/comp_v24/sintef_data/SOURCES.md",
    "Claude/results/comp_v26_data/build_two_versions.py",
    "Claude/results/comp_v26_data/test_skew_regsol_v2.py",
    "Claude/results/comp_v26_data/bdd_dqdv.py",
    "Claude/results/comp_v26_data/test_gallery_vs_regsol.py",
    "Claude/results/comp_v26_data/out_versions/summary_versions.json",
    "Claude/results/comp_v26_data/out_versions/A_regsol/params_blend.json",
    "Claude/results/comp_v26_data/out_versions/B_gallery/params_blend.json",
    "Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json",
)
ROLES = {
    SUPPLEMENTAL_PATHS[0]: "Direct14 repository-derived real-data CSV candidate",
    SUPPLEMENTAL_PATHS[1]: "saved source and protocol declaration; not raw data or proposition proof",
    SUPPLEMENTAL_PATHS[2]: "static A/B/C comparison reconstruction recipe; not executed in Step 89",
    SUPPLEMENTAL_PATHS[3]: "static real-CSV comparison reconstruction route; filename does not make it demo evidence",
    SUPPLEMENTAL_PATHS[4]: "static BDD-inspired calculation helper; not original-backend equivalence evidence",
    SUPPLEMENTAL_PATHS[5]: "static real-CSV graphite comparison reconstruction route; not executed in Step 89",
    SUPPLEMENTAL_PATHS[6]: "saved rounded A/B/C comparison summary; not runtime evidence",
    SUPPLEMENTAL_PATHS[7]: "saved sorted and rounded A blend profile",
    SUPPLEMENTAL_PATHS[8]: "saved sorted and rounded B blend profile",
    SUPPLEMENTAL_PATHS[9]: "saved sorted and rounded C blend profile",
}
SUPPORT = {
    SUPPLEMENTAL_PATHS[0]: ["E89-REAL-01"],
    SUPPLEMENTAL_PATHS[1]: ["E89-SAVED-DECLARATION-01"],
    SUPPLEMENTAL_PATHS[2]: ["E89-RECON-SOURCE-01"],
    SUPPLEMENTAL_PATHS[3]: ["E89-RECON-SOURCE-02"],
    SUPPLEMENTAL_PATHS[4]: ["E89-RECON-SOURCE-03"],
    SUPPLEMENTAL_PATHS[5]: ["E89-RECON-SOURCE-04"],
    SUPPLEMENTAL_PATHS[6]: [
        "E89-SAVED-SUMMARY-01", "E89-SAVED-A-01", "E89-SAVED-B-01", "E89-SAVED-C-01",
    ],
    SUPPLEMENTAL_PATHS[7]: ["E89-SAVED-A-01"],
    SUPPLEMENTAL_PATHS[8]: ["E89-SAVED-B-01"],
    SUPPLEMENTAL_PATHS[9]: ["E89-SAVED-C-01"],
}
CLASS_ENUM = ("REAL_DATA", "RECONSTRUCTED", "SYNTHETIC", "DEMO", "SAVED_ONLY")
AUTHORITY_FALSE = {
    "canonical_release": False,
    "external": False,
    "held_out": False,
    "identifiability": False,
    "material": False,
    "phase_mechanism": False,
    "publication": False,
    "protocol": False,
    "original_optimizer_state": False,
}


class BuildError(RuntimeError):
    pass


def require(ok: bool, code: str) -> None:
    if not ok:
        raise BuildError(code)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic(value: dict[str, Any]) -> str:
    copy_value = dict(value)
    copy_value.pop("semantic_sha256", None)
    return sha(canonical(copy_value))


def finish(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = semantic(value)
    return value


def strict_json(raw: bytes, code: str) -> dict[str, Any]:
    require(len(raw) <= 8_000_000, code + "_BYTES")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, code + "_DUPLICATE")
            result[key] = value
        return result

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                           parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise BuildError(code + "_PARSE") from exc
    require(isinstance(value, dict), code + "_ROOT")
    stack = [value]
    nodes = 0
    while stack:
        item = stack.pop()
        nodes += 1
        require(nodes <= 600_000, code + "_NODES")
        if isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
        elif isinstance(item, float):
            require(math.isfinite(item), code + "_NONFINITE")
    return value


def git_argv_allowed(args: tuple[str, ...]) -> bool:
    if not args or any(not isinstance(item, str) or "\0" in item or "\n" in item or "\r" in item
                       for item in args):
        return False
    if len(args) == 2 and args[0] == "show":
        if ":" not in args[1]:
            return False
        ref, path = args[1].split(":", 1)
        return (ref == EXPECTED_PARENT and path in PARENT_INPUTS) or \
            (ref == SUPPLEMENTAL_COMMIT and path in SUPPLEMENTAL_PATHS)
    if len(args) == 4 and args[0] == "ls-tree" and args[2] == "--":
        return args[1] in {SUPPLEMENTAL_COMMIT, BASELINE} and args[3] in SUPPLEMENTAL_PATHS
    return False


def git_bytes(args: list[str]) -> bytes:
    require(git_argv_allowed(tuple(args)), "E_GIT_ARGV")
    completed = subprocess.run(["git", *args], cwd=ROOT, check=False,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(completed.returncode == 0, "E_GIT_READ")
    return completed.stdout


def parent_raw(path: str) -> bytes:
    require(path in PARENT_INPUTS, "E_PARENT_PATH")
    return git_bytes(["show", f"{EXPECTED_PARENT}:{path}"])


def parent_json(path: str) -> dict[str, Any]:
    return strict_json(parent_raw(path), "E_PARENT_JSON")


def supplemental_raw(path: str) -> bytes:
    require(path in SUPPLEMENTAL_PATHS, "E_SUPPLEMENTAL_PATH")
    return git_bytes(["show", f"{SUPPLEMENTAL_COMMIT}:{path}"])


def tree_row(ref: str, path: str) -> tuple[str, str]:
    raw = git_bytes(["ls-tree", ref, "--", path]).decode("utf-8").strip()
    parts = raw.split("\t")
    require(len(parts) == 2 and parts[1] == path, "E_TREE_PATH")
    meta = parts[0].split()
    require(len(meta) == 3 and meta[0] == "100644" and meta[1] == "blob"
            and len(meta[2]) == 40, "E_TREE_META")
    return meta[0], meta[2]


def input_record(path: str) -> dict[str, Any]:
    raw = parent_raw(path)
    value = strict_json(raw, "E_INPUT_JSON")
    expected_raw, expected_declared = PARENT_EXPECTED[path]
    require(sha(raw) == expected_raw and value.get("semantic_sha256") == expected_declared,
            "E_INPUT_IDENTITY")
    return {
        "declared_semantic_sha256": value.get("semantic_sha256"),
        "path": path,
        "raw_sha256": sha(raw),
        "semantic_seal_status":
            "DECLARED_BY_PARENT_SCHEMA_RAW_BYTES_PINNED_NOT_RECOMPUTED_STEP89",
        "source_commit": EXPECTED_PARENT,
    }


def supplemental_record(path: str) -> dict[str, Any]:
    mode, oid = tree_row(SUPPLEMENTAL_COMMIT, path)
    baseline_mode, baseline_oid = tree_row(BASELINE, path)
    raw = supplemental_raw(path)
    require((mode, oid) == (baseline_mode, baseline_oid), "E_BASELINE_DRIFT")
    text = raw.decode("utf-8")
    return {
        "baseline_commit": BASELINE,
        "baseline_equal": True,
        "baseline_git_blob_oid": baseline_oid,
        "bounded_role": ROLES[path],
        "bytes": len(raw),
        "containing_commit": SUPPLEMENTAL_COMMIT,
        "git_blob_oid": oid,
        "line_count": len(text.splitlines()),
        "mode": mode,
        "path": path,
        "raw_sha256": sha(raw),
        "supports_evidence_ids": SUPPORT[path],
        "traversal_extent": "1-EOF",
    }


def static_source_check(path: str) -> dict[str, Any]:
    raw = supplemental_raw(path)
    source = raw.decode("utf-8")
    tree = ast.parse(source, filename=path)
    functions = sorted({node.name for node in ast.walk(tree)
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))})
    imports = sorted({alias.name for node in ast.walk(tree)
                      if isinstance(node, ast.Import) for alias in node.names} |
                     {str(node.module) for node in ast.walk(tree)
                      if isinstance(node, ast.ImportFrom)})
    return {
        "ast_parse": "PASS",
        "executed": False,
        "function_count": len(functions),
        "functions": functions,
        "imports": imports,
        "line_count": len(source.splitlines()),
        "path": path,
        "raw_sha256": sha(raw),
        "read_mode": "STATIC_GIT_OBJECT_ONLY",
    }


def real_data_profile() -> dict[str, Any]:
    raw = supplemental_raw(SUPPLEMENTAL_PATHS[0])
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8"), newline="")))
    require(rows and rows[0] == ["V_vs_Li", "Q_mAh"], "E_CSV_HEADER")
    values: list[tuple[float, float]] = []
    for row in rows[1:]:
        require(len(row) == 2, "E_CSV_WIDTH")
        pair = (float(row[0]), float(row[1]))
        require(all(math.isfinite(value) for value in pair), "E_CSV_NONFINITE")
        values.append(pair)
    require(len(values) == 16_735, "E_CSV_ROWS")
    voltages = [row[0] for row in values]
    capacities = [row[1] for row in values]
    require(all(capacities[i] <= capacities[i + 1] for i in range(len(capacities) - 1)),
            "E_CSV_CAPACITY_ORDER")
    return {
        "capacity_max_mAh": max(capacities),
        "capacity_min_mAh": min(capacities),
        "capacity_monotonic_nondecreasing": True,
        "columns": rows[0],
        "data_rows": len(values),
        "equal_voltage_adjacent_pairs": sum(
            voltages[i] == voltages[i + 1] for i in range(len(voltages) - 1)),
        "finite_numeric_rows": len(values),
        "input_nature": "REPOSITORY_DERIVED_REAL_MEASUREMENT_CSV_NOT_ORIGINAL_PARQUET",
        "path": SUPPLEMENTAL_PATHS[0],
        "raw_sha256": sha(raw),
        "strict_csv_traversal": "HEADER_PLUS_16735_ROWS",
        "voltage_decreasing_adjacent_pairs": sum(
            voltages[i] > voltages[i + 1] for i in range(len(voltages) - 1)),
        "voltage_max_V": max(voltages),
        "voltage_min_V": min(voltages),
    }


def evidence_row(identifier: str, evidence_class: str, object_kind: str,
                 paths: list[str], execution_status: str, in_sample_status: str,
                 input_nature: str) -> dict[str, Any]:
    require(evidence_class in CLASS_ENUM, "E_CLASS")
    return {
        "authority": dict(AUTHORITY_FALSE),
        "evidence_class": evidence_class,
        "execution_status": execution_status,
        "id": identifier,
        "in_sample_status": in_sample_status,
        "input_nature": input_nature,
        "object_kind": object_kind,
        "supporting_paths": paths,
    }


def comparison_contracts() -> list[dict[str, Any]]:
    shared = {
        "free_mask": "implicit_all_parameters_free_with_box_bounds",
        "objective": "unweighted_residual=model(V)-D",
        "original_full_optimizer_state": "GROUND_NOT_FOUND",
        "original_initial_vector": "GROUND_NOT_FOUND",
        "resolved_tolerances": "GROUND_NOT_FOUND",
        "restarts_per_strategy": 4,
        "rng_algorithm": "numpy.random.default_rng",
        "rng_seed": 23,
        "seed_and_bounds_dependency": {
            "bounds_initialization_callable": "test_gallery_vs_regsol.bounds_and_seed",
            "path": SUPPLEMENTAL_PATHS[5],
            "seed_strategy_callable": "test_gallery_vs_regsol.seed_sets",
        },
        "seed_strategies": 3,
        "solver": "scipy.optimize.least_squares",
        "source_explicit_options": ["bounds", "max_nfev"],
        "source_max_nfev": 6000,
        "restart_perturbation_multiplier_uniform": [0.75, 1.25],
    }
    specifications = [
        ("A_regsol", "regsol", 8, ["U[N]", "Omega[N]", "Q[N]", "w[N]", "bg"],
         {"Omega": "2.4*R*T", "Q": "area/N", "U": "one_of_three_source_seed_sets",
          "bg": "D_min", "w": 0.004},
         {"Omega": [0.0, "8*R*T"], "Q": [1e-9, "10*area"], "U": ["V_min", "V_max"],
          "bg": ["min(0,D_min)", "max(D_max,1e-9)"], "w": [0.0001, 0.12]}),
        ("B_gallery", "logistic", 14, ["U[N]", "w[N]", "Q[N]", "bg"],
         {"Q": "area/N", "U": "one_of_three_source_seed_sets", "bg": "D_min", "w": 0.004},
         {"Q": [1e-9, "10*area"], "U": ["V_min", "V_max"],
          "bg": ["min(0,D_min)", "max(D_max,1e-9)"], "w": [0.0001, 0.12]}),
        ("C_skew", "skew-logistic", 14,
         ["U[N]", "w[N]", "Q[N]", "alpha[N]", "bg"],
         {"Q": "area/N", "U": "one_of_three_source_seed_sets", "alpha": 1.0,
          "bg": "D_min", "w": 0.004},
         {"Q": [1e-9, "10*area"], "U": ["V_min", "V_max"], "alpha": [0.15, 8.0],
          "bg": ["min(0,D_min)", "max(D_max,1e-9)"], "w": [0.0001, 0.12]}),
    ]
    records = []
    for profile, kernel, components, order, initial, bounds in specifications:
        row = dict(shared)
        row.update({"bounds": bounds, "components_for_blend": components,
                    "initialization_recipe": initial, "kernel": kernel,
                    "parameter_order": order, "profile": profile,
                    "selection_rule": "minimum_cost_even_if_returned_success_is_false",
                    "source_path": SUPPLEMENTAL_PATHS[2]})
        records.append(row)
    return records


def supplemental_route_contracts() -> list[dict[str, Any]]:
    common_orders = {
        "logistic": ["U[N]", "w[N]", "Q[N]", "bg"],
        "regsol": ["U[N]", "Omega[N]", "Q[N]", "w[N]", "bg"],
        "skew-logistic": ["U[N]", "w[N]", "Q[N]", "alpha[N]", "bg"],
        "skew-regsol": ["U[N]", "Omega[N]", "Q[N]", "w[N]", "alpha[N]", "bg"],
    }
    common = {
        "executed_in_step89": False,
        "free_mask": "implicit_all_parameters_free_with_box_bounds",
        "kernel_parameter_orders": common_orders,
        "objective": "unweighted_residual=model(V)-D",
        "resolved_solver_method_loss_jacobian_tolerances": "GROUND_NOT_FOUND",
        "selection_rule": "minimum_cost_even_if_returned_success_is_false",
        "solver": "scipy.optimize.least_squares",
        "source_explicit_options": ["bounds", "max_nfev"],
    }
    skew = dict(common)
    skew.update({
        "bounds_recipe": {
            "Omega": [0.0, "8*R*T"], "Q": [1e-8, "10*area"],
            "U": ["max(V_min,U_seed-uband)", "min(V_max,U_seed+uband)"],
            "alpha": [0.15, 8.0], "bg": [0.0, "max(D_max,1e-9)"],
            "w": [0.0001, 0.10],
        },
        "initialization_recipe": {
            "Omega": "2.4*R*T", "Q": "area/N", "U": "configured_material_transition_list",
            "alpha": 1.0, "bg": "D_min", "w": 0.004,
        },
        "perturbation_multiplier_uniform": [0.7, 1.3],
        "material_run_configurations": [
            {
                "csv": "gr.csv", "fit_window_V": [0.060, 0.300],
                "grid_step_V": 2.5e-4,
                "initial_transition_U_V": [0.104, 0.120, 0.141, 0.190, 0.227],
                "material": "graphite", "u_band_V": 0.012,
                "zoom_window_V": [0.090, 0.240],
            },
            {
                "csv": "si.csv", "fit_window_V": [0.150, 0.700],
                "grid_step_V": 1.0e-3,
                "initial_transition_U_V": [0.260, 0.330, 0.433, 0.470],
                "material": "silicon", "u_band_V": 0.050,
                "zoom_window_V": [0.180, 0.620],
            },
            {
                "csv": "sigr.csv", "fit_window_V": [0.060, 0.700],
                "grid_step_V": 5.0e-4,
                "initial_transition_U_V": [0.096, 0.120, 0.135, 0.224, 0.330, 0.422, 0.470],
                "material": "blend", "u_band_V": 0.020,
                "zoom_window_V": [0.080, 0.520],
            },
        ],
        "restarts": 4,
        "rng_seed": 7,
        "route": "FOUR_KERNEL_MATERIAL_RUNNER",
        "seed_strategy": "one_configured_transition_list_per_material",
        "source_max_nfev": 4000,
        "source_path": SUPPLEMENTAL_PATHS[3],
        "width_bounds_V": [0.0001, 0.10],
    })
    gallery = dict(common)
    gallery.update({
        "bounds_recipe": {
            "Omega": [0.0, "8*R*T"], "Q": [1e-9, "10*area"],
            "U": ["V_min", "V_max"], "alpha": [0.15, 8.0],
            "bg": ["min(0,D_min)", "max(D_max,1e-9)"], "w": [0.0001, 0.12],
        },
        "initialization_recipe": {
            "Omega": "2.4*R*T", "Q": "area/N",
            "U": "one_of_three_peak_uniform_or_peak_overlap_seed_sets",
            "alpha": 1.0, "bg": "D_min", "w": 0.004,
        },
        "material_run_configuration": {
            "csv": "gr.csv", "fit_window_V": [0.060, 0.300],
            "grid_step_V": 2.5e-4, "material": "graphite",
        },
        "perturbation_multiplier_uniform": [0.75, 1.25],
        "restarts_per_strategy": 3,
        "rng_seed": 11,
        "route": "GRAPHITE_TRANSITION_COUNT_SWEEP",
        "seed_strategies": 3,
        "source_max_nfev": 4000,
        "source_path": SUPPLEMENTAL_PATHS[5],
        "sweep_components": {
            "logistic": [3, 4, 5, 6, 7, 8], "regsol": [3, 4, 5, 6, 7],
            "skew-logistic": [3, 4, 5, 6, 7], "skew-regsol": [3, 4, 5, 6],
        },
    })
    return [skew, gallery]


def saved_profile_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    summary = strict_json(supplemental_raw(SUPPLEMENTAL_PATHS[6]), "E_SUMMARY")
    records = []
    checks = []
    for profile, path in zip(("A_regsol", "B_gallery", "C_skew"), SUPPLEMENTAL_PATHS[7:]):
        params = strict_json(supplemental_raw(path), "E_PARAMS")
        blend = summary[profile]["blend"]
        metrics_match = params["metrics"]["R2"] == blend["R2"] and \
            params["metrics"]["BIC"] == blend["BIC"] and \
            params["metrics"]["npar"] == blend["npar"]
        transitions_match = params["transitions"] == blend["transitions"]
        require(metrics_match and transitions_match, "E_SAVED_MISMATCH")
        records.append({
            "authority": "SAVED_ONLY_NOT_ORIGINAL_OPTIMIZER_STATE",
            "flat_parameter_vector": blend["params"],
            "flat_vector_source_rounding": "8_DECIMAL_PLACES",
            "kernel": params["kernel"],
            "material": params["material"],
            "metrics": params["metrics"],
            "profile": profile,
            "source_path": path,
            "summary_metrics_match": True,
            "transition_order": "SORTED_BY_U_NOT_OPTIMIZER_FLAT_ORDER",
            "transition_source_rounding": "6_DECIMAL_PLACES_EXCEPT_DERIVED_DISPLAY_FIELDS",
            "transitions": params["transitions"],
        })
        checks.append({"params_path": path, "profile": profile,
                       "status": "MATCH", "summary_path": SUPPLEMENTAL_PATHS[6]})
    return records, checks


def metadata(artifact: str) -> dict[str, Any]:
    return {
        "artifact": artifact,
        "baseline_commit": BASELINE,
        "branch": BRANCH,
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "expected_parent": EXPECTED_PARENT,
        "expected_subject": SUBJECT,
        "gate": GATE,
        "generated_date": DATE,
        "persistence_terminal": PERSISTENCE,
        "phase": 67,
        "schema_version": "P067-S89-1",
        "step": 89,
        "supplemental_commit": SUPPLEMENTAL_COMMIT,
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    provenance = parent_json(FIT_PROVENANCE)
    reproduction = parent_json(FIT_REPRODUCTION)
    optimizer = parent_json(OPTIMIZER_STATE)
    empirical = parent_json(EMPIRICAL_AUTHORITY)
    carry = parent_json(CARRY_FORWARD)
    phase065 = parent_json(PHASE065_AUTHORITY)
    supplemental = [supplemental_record(path) for path in SUPPLEMENTAL_PATHS]
    source_paths = list(SUPPLEMENTAL_PATHS[2:6])
    source_checks = [static_source_check(path) for path in source_paths]
    saved_profiles, saved_checks = saved_profile_records()

    records = [
        evidence_row("E89-REAL-01", "REAL_DATA", "REPOSITORY_DERIVED_CSV",
                     [SUPPLEMENTAL_PATHS[0]], "READ_STATIC_GIT_OBJECT",
                     "INPUT_ONLY", "REPOSITORY_DERIVED_REAL_MEASUREMENT"),
        evidence_row("E89-SAVED-DECLARATION-01", "SAVED_ONLY", "SOURCE_DECLARATION",
                     [SUPPLEMENTAL_PATHS[1]], "READ_STATIC_GIT_OBJECT",
                     "SOURCE_DECLARATION_ONLY", "DECLARED_REAL_DATA_PROVENANCE_NOT_CRYPTOGRAPHIC_BINDING"),
        evidence_row("E89-RECON-SOURCE-01", "RECONSTRUCTED", "COMPARISON_RECIPE",
                     [SUPPLEMENTAL_PATHS[2]], "NOT_EXECUTED_STEP89",
                     "SOURCE_STATIC_ONLY", "REAL_CSV_RECONSTRUCTION_RECIPE"),
        evidence_row("E89-RECON-SOURCE-02", "RECONSTRUCTED", "COMPARISON_RECIPE",
                     [SUPPLEMENTAL_PATHS[3]], "NOT_EXECUTED_STEP89",
                     "SOURCE_STATIC_ONLY", "REAL_CSV_RECONSTRUCTION_RECIPE"),
        evidence_row("E89-RECON-SOURCE-03", "RECONSTRUCTED", "CALCULATION_HELPER_PORT",
                     [SUPPLEMENTAL_PATHS[4]], "NOT_EXECUTED_STEP89",
                     "SOURCE_STATIC_ONLY", "BDD_INSPIRED_RECONSTRUCTION_SOURCE"),
        evidence_row("E89-RECON-SOURCE-04", "RECONSTRUCTED", "COMPARISON_RECIPE",
                     [SUPPLEMENTAL_PATHS[5]], "NOT_EXECUTED_STEP89",
                     "SOURCE_STATIC_ONLY", "REAL_CSV_RECONSTRUCTION_RECIPE"),
        evidence_row("E89-REPLAY-312", "RECONSTRUCTED", "SEALED_PHASE066_REPLAY",
                     [FIT_REPRODUCTION, OPTIMIZER_STATE], "REUSED_PHASE066_SEALED_RECORD",
                     "BOUNDED_NUMERICAL_REPLAY_NONCONVERGED", "REPOSITORY_DERIVED_REAL_MEASUREMENT"),
        evidence_row("E89-REPLAY-314", "RECONSTRUCTED", "SEALED_PHASE066_REPLAY",
                     [FIT_REPRODUCTION, OPTIMIZER_STATE], "REUSED_PHASE066_SEALED_RECORD",
                     "BOUNDED_NUMERICAL_REPLAY_NONCONVERGED", "REPOSITORY_DERIVED_REAL_MEASUREMENT"),
        evidence_row("E89-SAVED-A-01", "SAVED_ONLY", "ROUNDED_SAVED_PROFILE",
                     [SUPPLEMENTAL_PATHS[6], SUPPLEMENTAL_PATHS[7]], "NOT_EXECUTED_STEP89",
                     "REPORTED_SAVED_METRICS_ONLY", "REAL_CSV_LABEL_WITH_UNSEALED_HISTORICAL_EXECUTION"),
        evidence_row("E89-SAVED-B-01", "SAVED_ONLY", "ROUNDED_SAVED_PROFILE",
                     [SUPPLEMENTAL_PATHS[6], SUPPLEMENTAL_PATHS[8]], "NOT_EXECUTED_STEP89",
                     "REPORTED_SAVED_METRICS_ONLY", "REAL_CSV_LABEL_WITH_UNSEALED_HISTORICAL_EXECUTION"),
        evidence_row("E89-SAVED-C-01", "SAVED_ONLY", "ROUNDED_SAVED_PROFILE",
                     [SUPPLEMENTAL_PATHS[6], SUPPLEMENTAL_PATHS[9]], "NOT_EXECUTED_STEP89",
                     "REPORTED_SAVED_METRICS_ONLY", "REAL_CSV_LABEL_WITH_UNSEALED_HISTORICAL_EXECUTION"),
        evidence_row("E89-SAVED-SUMMARY-01", "SAVED_ONLY", "ROUNDED_SAVED_SUMMARY",
                     [SUPPLEMENTAL_PATHS[6]], "NOT_EXECUTED_STEP89",
                     "REPORTED_SAVED_METRICS_ONLY", "REAL_CSV_LABEL_WITH_UNSEALED_HISTORICAL_EXECUTION"),
    ]
    counts = {label: sum(row["evidence_class"] == label for row in records)
              for label in CLASS_ENUM}
    p79 = next(row for row in empirical["claim_rows"] if row["id"] == "P79-07")
    s72 = next(row for row in phase065["findings"] if row["id"] == "S72-F04")
    active = {row["obligation_id"]: row for row in carry["active_obligations"]}
    obligations = []
    for obligation_id, claim in (("P065-OBL-0054", s72["finding"]),
                                 ("P066-OBL-0120", p79["claim"])):
        prior = active[obligation_id]
        obligations.append({
            "canonical_owner": prior["canonical_owner"],
            "claim": claim,
            "external_authority_promoted": False,
            "next_owner": "P067-STEP90.1-DISPOSITION",
            "obligation_id": obligation_id,
            "origin_identity": prior["origin_identity"],
            "prior_state": prior["state"],
            "semantic_fingerprint": prior["semantic_fingerprint"],
            "step89_disposition": "EXPLICITLY_BOUNDED_NOT_RESOLVED",
        })

    matrix = metadata("PHASE_067_FITTING_EVIDENCE_MATRIX")
    matrix.update({
        "absent_class_records": [
            {"evidence_class": "SYNTHETIC", "scope": "EXACT_REVIEWED_FITTING_INVENTORY",
             "status": "NO_POSITIVE_RECORD_FOUND"},
            {"evidence_class": "DEMO", "scope": "EXACT_REVIEWED_FITTING_INVENTORY",
             "status": "NO_POSITIVE_RECORD_FOUND"},
        ],
        "bounded_obligations": obligations,
        "comparison_source_contracts": comparison_contracts(),
        "direct14_contract": {
            "optimizer": provenance["optimizer_contract"],
            "preprocessing": provenance["preprocessing"],
            "processed_input": provenance["processed_input"],
            "raw_input": provenance["raw_input"],
        },
        "evidence_records": records,
        "exclusive_classification": {
            "counts": counts,
            "enum": list(CLASS_ENUM),
            "exclusive": True,
            "zero_class_interpretation":
                "REVIEWED_FITTING_INVENTORY_ABSENCE_NOT_PROJECT_WIDE_ABSENCE",
        },
        "finite_rate_boundary": {
            "claim": p79["claim"],
            "empirical_ceiling": p79["empirical_ceiling"],
            "physical_authority": p79["physical_authority"],
            "physical_ceiling": p79["physical_ceiling"],
            "status": p79["status"],
        },
        "missing_evidence": {
            "exact_original_parquet_key_checksum": "GROUND_NOT_FOUND",
            "held_out_cells_rates_temperatures": "GROUND_NOT_FOUND",
            "historical_ABC_execution_environment_and_convergence": "GROUND_NOT_FOUND",
            "historical_direct14_optimizer_fields": 25,
            "independent_material_phase_mechanism_evidence": "GROUND_NOT_FOUND",
            "specimen_uuid_composition_binding": "GROUND_NOT_FOUND",
        },
        "phase066_inputs": [input_record(path) for path in PARENT_INPUTS],
        "real_data_object": real_data_profile(),
        "saved_profile_records": saved_profiles,
        "source_comment_execution_conflict": {
            "adjudication": "EXECUTABLE_CALL_PATH_AND_PHASE066_SEAL_CONTROL",
            "claimed_in_docstring": "BDD_DMSMCD_PLUS_WAVELET_PLUS_SAVGOL",
            "executed_by_direct14_preprocessing": "SAVGOL_ENSEMBLE_WITHOUT_BDD_DMSMCD_OR_WAVELET",
            "phase066_wavelet_or_bdd_dmsmcd_used":
                provenance["preprocessing"]["wavelet_or_bdd_dmsmcd_used"],
            "source_path": SUPPLEMENTAL_PATHS[3],
        },
        "supplemental_route_contracts": supplemental_route_contracts(),
        "supplemental_inputs": supplemental,
        "validation": {
            "classification_records": len(records),
            "external_authority_promotions": 0,
            "fresh_fit_executions": 0,
            "supplemental_objects": len(supplemental),
            "unbound_supplemental_objects": 0,
        },
    })
    finish(matrix)

    runtime = metadata("PHASE_067_FITTING_RUNTIME_ATTESTATION")
    runtime.update({
        "authority": {
            "canonical_release": False,
            "external_scientific_validation": False,
            "held_out_validation": False,
            "historical_optimizer_state": False,
            "identifiability": False,
            "material_assignment": False,
            "phase_or_mechanism_identification": False,
            "publication": False,
            "protocol_binding": False,
        },
        "execution_policy": {
            "fresh_historical_fit_execution_count": 0,
            "historical_fit_executed": False,
            "optimizer_call_count_in_step89": 0,
            "phase066_sealed_evidence_reused": True,
            "supplemental_source_executed": False,
            "supplemental_source_read_mode": "STATIC_GIT_OBJECT_ONLY",
        },
        "original_optimizer_state_availability": optimizer["original_optimizer_state_availability"],
        "saved_consistency_checks": saved_checks,
        "sealed_replay_records": optimizer["selected_replay_trials"],
        "static_source_checks": source_checks,
        "step77_external_process_evidence":
            empirical["source_gates"]["step77_external_process_evidence"],
        "step77_runtime_success": reproduction["runtime_success"],
        "step77_selected_trial_converged": reproduction["selected_trial_converged"],
        "validation": {
            "historical_state_ground_not_found": len(optimizer["original_optimizer_state_availability"]),
            "saved_profile_matches": len(saved_checks),
            "sealed_replays_reused": len(optimizer["selected_replay_trials"]),
            "static_sources_parsed_not_executed": len(source_checks),
        },
    })
    finish(runtime)
    return matrix, runtime


def atomic_write(path: str, raw: bytes) -> None:
    require(path in {MATRIX_PATH, RUNTIME_PATH}, "E_WRITE_PATH")
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp-step89")
    temporary.write_bytes(raw)
    os.replace(temporary, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    try:
        matrix, runtime = build()
        if args.preview:
            sys.stdout.buffer.write(canonical({"matrix": matrix, "runtime": runtime}))
        else:
            atomic_write(MATRIX_PATH, canonical(matrix))
            atomic_write(RUNTIME_PATH, canonical(runtime))
            print(GATE)
    except BuildError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
