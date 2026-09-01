from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "d091e7881f9f22d5dfe9511427afdf4ef22e3280"
EXPECTED_SUBJECT = "audit(phase066): verify profile default temperature routes"
EXPECTED_BUILDER_SHA256 = "3bc90fab4d8e8d2d826f6174e1ec71b7389bb46daa7609257c05b14ca7baa1cd"
EXPECTED_PROBE_SHA256 = "e8fe2dc290f7c009af519e42bd3202f266f8dcb7daa909e451fa59a0db559f12"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{BRANCH}"
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BUILDER_PATH = "Codex/work/v1025_phase066/build_phase066_step80.py"
VALIDATOR_PATH = "Codex/work/v1025_phase066/validate_phase066_step80.py"
MATRIX_PATH = "Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json"
RUNTIME_PATH = "Codex/results/PHASE_066_RUNTIME_ATTESTATION.json"
RESULT_PATH = "Codex/results/PHASE_066_STEP_080_PROFILE_TEMPERATURE_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
GATE = "PASS_P066_STEP80_PROFILE_DEFAULT_TEMPERATURE_VERIFICATION"
PERSISTENCE = "PASS_P066_STEP80_PERSISTENCE"
SOURCE_PATH = "Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py"
TEST1024_PATH = "Claude/docs/v1.0.25.2/test_gates_v1024.py"
TEST1025_PATH = "Claude/docs/v1.0.25.2/test_gates_v1025.py"
FINAL_PATHS = sorted([
    BUILDER_PATH, VALIDATOR_PATH, MATRIX_PATH, RUNTIME_PATH, RESULT_PATH,
    PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH,
])
ROUTE_IDS = [
    "fresh_default_4_2", "explicit_legacy_4_2", "from_wt_sic_4_2",
    "toggle_skew_7_7", "explicit_skew_7_7", "explicit_xrd_5_2",
    "explicit_msmr6_6_2", "explicit_legacy_4_si7",
    "explicit_skew7_symmetric7", "explicit_legacy_4_elemental2",
    "explicit_legacy_4_siox1", "lco3_electronic_off",
    "lco3_electronic_on", "serialized_regsol_8",
    "serialized_gallery_14", "serialized_skew_14",
]
EXPECTED_COUNTS = {
    "fresh_default_4_2": (4, 2, 6),
    "explicit_legacy_4_2": (4, 2, 6),
    "from_wt_sic_4_2": (4, 2, 6),
    "toggle_skew_7_7": (7, 7, 14),
    "explicit_skew_7_7": (7, 7, 14),
    "explicit_xrd_5_2": (5, 2, 7),
    "explicit_msmr6_6_2": (6, 2, 8),
    "explicit_legacy_4_si7": (4, 7, 11),
    "explicit_skew7_symmetric7": (7, 7, 14),
    "explicit_legacy_4_elemental2": (4, 2, 6),
    "explicit_legacy_4_siox1": (4, 1, 5),
    "lco3_electronic_off": (None, None, 3),
    "lco3_electronic_on": (None, None, 3),
    "serialized_regsol_8": (None, None, 8),
    "serialized_gallery_14": (None, None, 14),
    "serialized_skew_14": (None, None, 14),
}
EXPECTED_TEMP_DEPENDENT = {
    "fresh_default_4_2", "explicit_legacy_4_2", "from_wt_sic_4_2",
    "explicit_xrd_5_2", "explicit_legacy_4_si7",
    "explicit_legacy_4_elemental2", "explicit_legacy_4_siox1",
    "lco3_electronic_off", "lco3_electronic_on",
}
EXPECTED_ROUTE_CLASS = {
    "fresh_default_4_2": "FRESH_PUBLIC_DEFAULT",
    "explicit_legacy_4_2": "EXPLICIT_PRODUCTION_LITERAL",
    "from_wt_sic_4_2": "PUBLIC_ALIAS_FROM_WT",
    "toggle_skew_7_7": "GLOBAL_TOGGLE",
    "explicit_skew_7_7": "EXPLICIT_PRODUCTION_LITERAL",
    "explicit_xrd_5_2": "EXPLICIT_ALTERNATIVE_LITERAL",
    "explicit_msmr6_6_2": "EXPLICIT_ALTERNATIVE_LITERAL",
    "explicit_legacy_4_si7": "EXPLICIT_ALTERNATIVE_LITERAL",
    "explicit_skew7_symmetric7": "DIVERGENT_SOURCE_EXAMPLE",
    "explicit_legacy_4_elemental2": "EXPLICIT_FALLBACK_CASE",
    "explicit_legacy_4_siox1": "EXPLICIT_FALLBACK_CASE",
    "lco3_electronic_off": "PUBLIC_LCO_TOGGLE",
    "lco3_electronic_on": "PUBLIC_LCO_TOGGLE",
    "serialized_regsol_8": "SERIALIZED_HISTORICAL_PROFILE",
    "serialized_gallery_14": "SERIALIZED_HISTORICAL_PROFILE",
    "serialized_skew_14": "SERIALIZED_HISTORICAL_PROFILE",
}
EXPECTED_NEGATIVE_CONTRACT = [
    "fresh_import_after_test_mutation_rejected",
    "test_only_default_promoted_to_public_rejected",
    "omitted_profile_row_rejected",
    "temperature_independent_route_marked_dependent_rejected",
    "order_restoration_failure_rejected",
    "runtime_observation_promoted_to_external_authority_rejected",
    "serialized_regsol_marked_current_kernel_equivalent_rejected",
    "stale_comment_promoted_over_assignment_rejected",
    "probe_source_hash_mismatch_rejected",
    "runtime_argv_mutation_rejected",
    "runtime_unknown_field_rejected",
    "cross_runtime_observation_divergence_rejected",
    "matrix_runtime_field_fabrication_rejected",
]
EXPECTED_DECLARED_SOURCES = {
    "fresh_default_4_2": ["DEFAULT_GRAPHITE_TRANSITIONS", "SI_CASE_SETS[sic]"],
    "explicit_legacy_4_2": ["GRAPHITE_STAGING_LIT", "SIC_LIT"],
    "from_wt_sic_4_2": ["from_wt", "DEFAULT_GRAPHITE_TRANSITIONS", "SI_CASE_SETS[sic]"],
    "toggle_skew_7_7": ["use_skew7_default(True)", "DEFAULT_GRAPHITE_TRANSITIONS", "DEFAULT_SI_TRANSITIONS"],
    "explicit_skew_7_7": ["GRAPHITE_MSMR7_LIT", "SI_MSMR7_SKEW_LIT"],
    "explicit_xrd_5_2": ["GRAPHITE_STAGING_XRD_v1024", "SIC_LIT"],
    "explicit_msmr6_6_2": ["GRAPHITE_STAGING_MSMR6_LIT", "SIC_LIT"],
    "explicit_legacy_4_si7": ["GRAPHITE_STAGING_LIT", "SI_MSMR7_LIT"],
    "explicit_skew7_symmetric7": ["GRAPHITE_MSMR7_LIT", "SI_MSMR7_LIT"],
    "explicit_legacy_4_elemental2": ["GRAPHITE_STAGING_LIT", "SI_ELEMENTAL_LIT"],
    "explicit_legacy_4_siox1": ["GRAPHITE_STAGING_LIT", "SIOX_LIT"],
    "lco3_electronic_off": ["LCO_MSMR_LIT", "include_electronic_entropy=False"],
    "lco3_electronic_on": ["LCO_MSMR_LIT", "include_electronic_entropy=True"],
    "serialized_regsol_8": ["serialized_regsol_8.json"],
    "serialized_gallery_14": ["serialized_gallery_14.json"],
    "serialized_skew_14": ["serialized_skew_14.json"],
}


class ValidationFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationFailure(f"{code}: {detail}" if detail else code)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True,
                       allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_DUPLICATE_JSON_KEY", key)
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValidationFailure(f"E_NONFINITE_JSON: {value}")


def strict_json(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                       parse_constant=reject_constant)
    require(isinstance(value, dict), "E_JSON_ROOT")
    require(canonical_bytes(value) == raw, "E_CANONICAL_JSON")
    observed = value.get("semantic_sha256")
    clone = copy.deepcopy(value)
    clone.pop("semantic_sha256", None)
    expected = sha256(json.dumps(clone, ensure_ascii=False, sort_keys=True,
                                 separators=(",", ":"), allow_nan=False).encode("utf-8"))
    require(observed == expected, "E_SEMANTIC_SHA")
    return value


def git(*args: str) -> bytes:
    cp = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, shell=False, check=False)
    require(cp.returncode == 0, "E_GIT", " ".join(args))
    return cp.stdout


def git_blob(path: str) -> str:
    return git("rev-parse", f"{BASELINE}:{path}").decode().strip()


def git_bytes(path: str) -> bytes:
    return git("cat-file", "blob", f"{BASELINE}:{path}")


def verify_input(binding: dict[str, Any]) -> None:
    require(set(binding) == {"commit", "path", "blob", "sha256", "bytes", "lines"},
            "E_INPUT_SCHEMA")
    require(binding["commit"] == BASELINE, "E_INPUT_COMMIT")
    raw = git_bytes(binding["path"])
    require(binding["blob"] == git_blob(binding["path"]), "E_INPUT_BLOB")
    require(binding["sha256"] == sha256(raw) and binding["bytes"] == len(raw),
            "E_INPUT_RAW")
    require(binding["lines"] == len(raw.decode("utf-8").splitlines()), "E_INPUT_LINES")


def validate_source_ref(record: dict[str, Any]) -> None:
    require(set(record) == {"commit", "path", "blob", "line_start", "line_end", "evidence"},
            "E_SOURCE_REF_SCHEMA")
    require(record["commit"] == BASELINE and record["blob"] == git_blob(record["path"]),
            "E_SOURCE_REF_IDENTITY")
    lines = git_bytes(record["path"]).decode("utf-8").splitlines()
    require(isinstance(record["line_start"], int) and isinstance(record["line_end"], int),
            "E_SOURCE_REF_LINE_TYPE")
    require(1 <= record["line_start"] <= record["line_end"] <= len(lines),
            "E_SOURCE_REF_RANGE")
    require(bool(record["evidence"].strip()), "E_SOURCE_REF_EVIDENCE")


def source_ast_assertions(production: dict[str, Any]) -> None:
    source_text = git_bytes(SOURCE_PATH).decode("utf-8")
    tree = ast.parse(source_text, filename=SOURCE_PATH)
    assignments: dict[str, ast.AST] = {}
    assignment_nodes: dict[str, ast.Assign | ast.AnnAssign] = {}
    functions: dict[str, ast.FunctionDef] = {}
    classes: dict[str, ast.ClassDef] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            assignments[node.targets[0].id] = node.value
            assignment_nodes[node.targets[0].id] = node
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assignments[node.target.id] = node.value
            assignment_nodes[node.target.id] = node
        elif isinstance(node, ast.FunctionDef):
            functions[node.name] = node
        elif isinstance(node, ast.ClassDef):
            classes[node.name] = node
    require(set(production) == {
        "absent_named_routing_apis", "background_constants_runtime_load_count",
        "blended_constructor", "fresh_default_assignments", "from_wt_alias",
        "legacy_function", "literal_profiles", "parse", "source_lines",
        "toggle_function",
    } and production["parse"] == "PASS"
      and production["source_lines"] == len(source_text.splitlines()),
      "E_PRODUCTION_AST_SCHEMA")
    require(ast.unparse(assignments["DEFAULT_GRAPHITE_TRANSITIONS"]) == "GRAPHITE_STAGING_LIT",
            "E_AST_FRESH_GR")
    require(ast.unparse(assignments["DEFAULT_SI_TRANSITIONS"]) == "None", "E_AST_FRESH_SI")
    require("use_skew7_default" in functions and "use_legacy_4transition" not in functions,
            "E_AST_TOGGLE_NAMES")
    expected_literals = {
        "GRAPHITE_STAGING_LIT": 4, "GRAPHITE_STAGING_XRD_v1024": 5,
        "GRAPHITE_STAGING_MSMR6_LIT": 6, "GRAPHITE_MSMR7_LIT": 7,
        "SI_ELEMENTAL_LIT": 2, "SIOX_LIT": 1, "SIC_LIT": 2,
        "SI_MSMR7_LIT": 7, "SI_MSMR7_SKEW_LIT": 7,
    }
    require(set(production["literal_profiles"]) == set(expected_literals), "E_LITERAL_SET")
    for name, count in expected_literals.items():
        literal = ast.literal_eval(assignments[name])
        node = assignment_nodes[name]
        require(production["literal_profiles"][name] == {
            "count": count,
            "keys_union": sorted({key for item in literal for key in item}),
            "has_thermodynamic_center": all(
                "dH_rxn" in item and "dS_rxn" in item for item in literal),
            "has_thermal_width": all("n" in item for item in literal),
            "all_w_only_or_fixed_u": all("U" in item and "w" in item for item in literal),
            "line_start": node.lineno,
            "line_end": node.end_lineno,
        }, "E_LITERAL_RECORD", name)
    require(production["fresh_default_assignments"] == {
        "graphite": "GRAPHITE_STAGING_LIT", "silicon": "None",
        "line_range": [assignment_nodes["DEFAULT_GRAPHITE_TRANSITIONS"].lineno,
                       assignment_nodes["DEFAULT_SI_TRANSITIONS"].end_lineno],
    },
            "E_MATRIX_DEFAULT_ASSIGNMENTS")
    require(production["toggle_function"] == {
        "present": True,
        "name": "use_skew7_default",
        "parameter": {"name": "enable", "annotation": "bool", "default": True},
        "global_names": ["DEFAULT_GRAPHITE_TRANSITIONS", "DEFAULT_SI_TRANSITIONS"],
        "true_assignments": {
            "DEFAULT_GRAPHITE_TRANSITIONS": "GRAPHITE_MSMR7_LIT",
            "DEFAULT_SI_TRANSITIONS": "SI_MSMR7_SKEW_LIT",
        },
        "false_assignments": {
            "DEFAULT_GRAPHITE_TRANSITIONS": "GRAPHITE_STAGING_LIT",
            "DEFAULT_SI_TRANSITIONS": "None",
        },
        "line_range": [1454, 1470],
    }, "E_TOGGLE_SEMANTIC_FIELDS")
    require(production["legacy_function"] == {
        "present": False, "comment_occurrences": source_text.count("use_legacy_4transition"),
    }, "E_LEGACY_COMMENT_ONLY")
    require(production["absent_named_routing_apis"] == {
        "load_profile": "GROUND_NOT_FOUND",
        "from_profile": "GROUND_NOT_FOUND",
        "PROFILE_ALIASES": "GROUND_NOT_FOUND",
        "SAVED_PROFILES": "GROUND_NOT_FOUND",
        "module___all__": "GROUND_NOT_FOUND",
    }, "E_ABSENT_ROUTING_APIS")
    require(production["background_constants_runtime_load_count"] == {
        "DEFAULT_CBG_GRAPHITE": 0, "DEFAULT_CBG_SI": 0,
    }, "E_BACKGROUND_UNUSED")
    blended = classes["BlendedAnodeDQDV"]
    init = next(node for node in blended.body
                if isinstance(node, ast.FunctionDef) and node.name == "__init__")
    from_wt = next(node for node in blended.body
                   if isinstance(node, ast.FunctionDef) and node.name == "from_wt")
    init_text = ast.unparse(init)
    require(production["blended_constructor"] == {
        "line_range": [init.lineno, init.end_lineno],
        "default_graphite_pointer_load": "DEFAULT_GRAPHITE_TRANSITIONS" in init_text,
        "default_si_pointer_load": "DEFAULT_SI_TRANSITIONS" in init_text,
        "si_case_fallback_load": "SI_CASE_SETS" in init_text,
        "explicit_override_precedence": (
            "graphite_transitions is None" in init_text
            and "si_transitions is None" in init_text),
    }, "E_BLENDED_CONSTRUCTOR")
    require(production["from_wt_alias"] == {
        "line_range": [from_wt.lineno, from_wt.end_lineno],
        "returns_constructor": "return cls(" in ast.unparse(from_wt),
    }, "E_FROM_WT_ALIAS")


def validate_stats(record: dict[str, Any]) -> None:
    require(set(record) == {"size", "min", "max", "sum", "sha256_f64le", "finite"},
            "E_STATS_SCHEMA")
    require(record["size"] == 1401 and record["finite"] is True, "E_STATS_FINITE")
    require(re.fullmatch(r"[0-9a-f]{64}", record["sha256_f64le"]) is not None,
            "E_STATS_HASH")
    for key in ("min", "max", "sum"):
        require(isinstance(record[key], (int, float)), "E_STATS_NUMBER", key)


def builder_tree_and_probe() -> tuple[ast.Module, str]:
    source = (ROOT / BUILDER_PATH).read_text(encoding="utf-8")
    require(sha256(source.encode("utf-8")) == EXPECTED_BUILDER_SHA256,
            "E_BUILDER_SOURCE_SHA")
    tree = ast.parse(source, filename=BUILDER_PATH)
    candidates = [
        node.value for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "PROBE_SOURCE"
    ]
    require(len(candidates) == 1, "E_BUILDER_PROBE_ASSIGNMENT")
    probe = ast.literal_eval(candidates[0])
    require(isinstance(probe, str) and sha256(probe.encode("utf-8"))
            == EXPECTED_PROBE_SHA256, "E_BUILDER_PROBE_LITERAL")
    return tree, probe


def validate_observation(obs: dict[str, Any], route_id: str) -> None:
    require(set(obs) == {
        "analytic_temperature_coefficient", "contributions", "declared_sources",
        "limits", "observation_sha256", "profile", "route_id", "route_kind",
        "serialized_compatibility", "serialized_kernel", "temperature",
    }, "E_OBS_SCHEMA", route_id)
    require(obs["route_id"] == route_id, "E_OBS_ROUTE")
    require(obs["declared_sources"] == EXPECTED_DECLARED_SOURCES[route_id],
            "E_OBS_DECLARED_SOURCES", route_id)
    profile = obs["profile"]
    require(set(profile) == {"Cbg", "f_Si", "graphite_count", "silicon_count",
                             "total_count"}, "E_OBS_PROFILE_SCHEMA", route_id)
    require((profile["graphite_count"], profile["silicon_count"], profile["total_count"])
            == EXPECTED_COUNTS[route_id], "E_OBS_COUNTS", route_id)
    temp = obs["temperature"]
    require(set(temp) == {
        "U_oc_delta_V", "U_oc_x025_V", "curve_high", "curve_low",
        "curve_max_abs_delta", "equilibrium_high", "equilibrium_low",
        "equilibrium_max_abs_delta", "finite_difference_derivative",
        "temperature_dependent_observed", "temperatures_K",
    }, "E_OBS_TEMPERATURE_SCHEMA", route_id)
    require(temp["temperatures_K"] == [288.15, 308.15], "E_OBS_TEMPERATURES")
    expected_dep = route_id in EXPECTED_TEMP_DEPENDENT
    require(temp["temperature_dependent_observed"] is expected_dep,
            "E_OBS_TEMPERATURE_CLASS", route_id)
    for key in ("equilibrium_low", "equilibrium_high", "finite_difference_derivative",
                "curve_low", "curve_high"):
        validate_stats(temp[key])
    if expected_dep:
        require(max(temp["equilibrium_max_abs_delta"], temp["curve_max_abs_delta"]) > 1e-12,
                "E_OBS_DEPENDENT_ZERO", route_id)
    else:
        require(temp["equilibrium_max_abs_delta"] <= 1e-12
                and temp["curve_max_abs_delta"] <= 1e-12,
                "E_OBS_INDEPENDENT_FALSE_POSITIVE", route_id)
    if obs["route_kind"] == "PUBLIC_BLEND":
        require(route_id not in {"lco3_electronic_off", "lco3_electronic_on"}
                and not route_id.startswith("serialized_"), "E_OBS_BLEND_KIND", route_id)
        require(set(obs["contributions"]) == {
            "graphite_high", "graphite_low", "graphite_max_abs_delta",
            "silicon_high", "silicon_low", "silicon_max_abs_delta", "status",
        }, "E_OBS_CONTRIBUTION_SCHEMA", route_id)
        for key in ("graphite_high", "graphite_low", "silicon_high", "silicon_low"):
            validate_stats(obs["contributions"][key])
        require(all(isinstance(obs["contributions"][key], (int, float))
                    for key in ("graphite_max_abs_delta", "silicon_max_abs_delta")),
                "E_OBS_CONTRIBUTION_NUMERIC", route_id)
        require(obs["contributions"]["status"] == "OBSERVED", "E_OBS_CONTRIBUTIONS")
        require(set(obs["limits"]) == {
            "f_Si_zero_bit_exact", "f_Si_zero_max_abs_delta", "status",
        } and obs["limits"]["status"] == "OBSERVED"
                and obs["limits"]["f_Si_zero_bit_exact"] is True
                and obs["limits"]["f_Si_zero_max_abs_delta"] == 0.0,
                "E_OBS_FSI_LIMIT")
        require(set(obs["analytic_temperature_coefficient"]) == {
            "graphite_low", "silicon_low", "status",
        } and obs["analytic_temperature_coefficient"]["status"]
                == "HOSTS_OBSERVED_NO_BLEND_PUBLIC_DELEGATE", "E_OBS_BLEND_TEMP_API")
        validate_stats(obs["analytic_temperature_coefficient"]["graphite_low"])
        validate_stats(obs["analytic_temperature_coefficient"]["silicon_low"])
    elif route_id.startswith("serialized_"):
        require(obs["route_kind"] == "SERIALIZED_POOLED"
                and obs["contributions"] == {"status": "NOT_APPLICABLE"}
                and obs["limits"] == {
                    "f_Si_zero_bit_exact": None, "status": "NOT_APPLICABLE"
                }
                and obs["analytic_temperature_coefficient"] == {
                    "status": "NOT_APPLICABLE"
                },
                "E_OBS_SERIALIZED_SCOPE")
    else:
        require(route_id in {"lco3_electronic_off", "lco3_electronic_on"}
                and obs["route_kind"] == "PUBLIC_LCO"
                and obs["contributions"] == {"status": "NOT_APPLICABLE"}
                and obs["limits"] == {
                    "f_Si_zero_bit_exact": None, "status": "NOT_APPLICABLE"
                }
                and set(obs["analytic_temperature_coefficient"]) == {
                    "high", "low", "status"
                }
                and obs["analytic_temperature_coefficient"]["status"] == "OBSERVED",
                "E_OBS_ANALYTIC_TEMP")
        validate_stats(obs["analytic_temperature_coefficient"]["high"])
        validate_stats(obs["analytic_temperature_coefficient"]["low"])
    if route_id == "serialized_regsol_8":
        require(obs["serialized_kernel"] == "regsol"
                and obs["serialized_compatibility"]
                == "CURRENT_PUBLIC_LOGISTIC_ONLY_KERNEL_METADATA_NOT_DISPATCHED",
                "E_REGSOL_ROUTE_CEILING")
    require(re.fullmatch(r"[0-9a-f]{64}", obs["observation_sha256"]) is not None,
            "E_OBS_SHA")
    clone = copy.deepcopy(obs)
    observed = clone.pop("observation_sha256")
    expected = sha256(json.dumps(clone, ensure_ascii=False, sort_keys=True,
                                 separators=(",", ":"), allow_nan=False).encode("utf-8"))
    require(observed == expected, "E_OBS_SEAL")


def validate_order_observation(observation: dict[str, Any], permutation: str) -> None:
    require(set(observation) == {"events", "fresh_first", "observation_sha256",
                                 "permutation", "restored_equals_fresh"},
            "E_ORDER_SCHEMA", permutation)
    require(observation["permutation"] == permutation
            and observation["fresh_first"] is True
            and observation["restored_equals_fresh"] is True,
            "E_ORDER_HEADER", permutation)
    expected = {
        "permutation_a": [
            ("fresh_default_before_any_mutation", [4, 2]),
            ("toggle_true", [7, 7]),
            ("explicit_legacy_while_toggled", [4, 2]),
            ("restored_false", [4, 2]),
        ],
        "permutation_b": [
            ("fresh_default_before_any_mutation", [4, 2]),
            ("explicit_skew_before_toggle", [7, 7]),
            ("toggle_true", [7, 7]),
            ("restored_false", [4, 2]),
        ],
    }[permutation]
    events = observation["events"]
    require(len(events) == 4, "E_ORDER_EVENT_COUNT", permutation)
    for event, (label, counts) in zip(events, expected, strict=True):
        require(set(event) == {"counts", "label", "sha256_f64le"}
                and event["label"] == label and event["counts"] == counts
                and re.fullmatch(r"[0-9a-f]{64}", event["sha256_f64le"]) is not None,
                "E_ORDER_EVENT", f"{permutation}:{label}")
    if permutation == "permutation_a":
        require(events[0]["sha256_f64le"] == events[2]["sha256_f64le"]
                == events[3]["sha256_f64le"], "E_ORDER_A_EXPLICIT_OR_RESTORE")
    else:
        require(events[0]["sha256_f64le"] == events[3]["sha256_f64le"]
                and events[1]["sha256_f64le"] == events[2]["sha256_f64le"],
                "E_ORDER_B_EXPLICIT_OR_RESTORE")
    clone = copy.deepcopy(observation)
    observed = clone.pop("observation_sha256")
    expected_sha = sha256(json.dumps(clone, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":"), allow_nan=False).encode("utf-8"))
    require(observed == expected_sha, "E_ORDER_SEAL", permutation)


def validate_runtime(runtime: dict[str, Any]) -> None:
    require(set(runtime) == {"schema", "baseline", "source", "probe_sha256",
                             "process_contract", "runs", "cross_runtime_agreement",
                             "aggregate", "authority_ceiling", "semantic_sha256"},
            "E_RUNTIME_TOP_SCHEMA")
    require(runtime["schema"] == "phase066.step080.runtime-attestation.v1"
            and runtime["baseline"] == BASELINE, "E_RUNTIME_HEADER")
    verify_input(runtime["source"])
    _, probe_source = builder_tree_and_probe()
    require(runtime["probe_sha256"] == sha256(probe_source.encode("utf-8")),
            "E_RUNTIME_PROBE_SHA")
    require(runtime["process_contract"] == {
        "fresh_process_per_route": True,
        "fresh_import_before_any_mutation": True,
        "python_versions": ["3.12", "3.14"],
        "isolated_flags": ["-B", "-I", "-X", "utf8"],
        "working_tree_claude_imported": False,
        "disposable_root_cleanup_completed": True,
    }, "E_PROCESS_CONTRACT")
    runs = runtime["runs"]
    require(len(runs) == 36, "E_RUN_COUNT")
    observed_keys: set[tuple[str, str, str]] = set()
    route_versions: dict[str, set[str]] = {route: set() for route in ROUTE_IDS}
    route_observations: dict[str, dict[str, dict[str, Any]]] = {
        route: {} for route in ROUTE_IDS
    }
    order_count = 0
    for run in runs:
        require(set(run) == {
            "argv", "cwd", "exit_code", "mode", "observation", "python",
            "route_id", "stderr_sha256", "stderr_utf8", "stdout_sha256",
            "stdout_utf8",
        }, "E_RUN_SCHEMA")
        key = (run["python"], run["mode"], run["route_id"])
        require(key not in observed_keys, "E_DUPLICATE_RUN", str(key))
        observed_keys.add(key)
        require(run["python"] in {"3.12", "3.14"} and run["exit_code"] == 0,
                "E_RUN_EXIT")
        require(run["cwd"] == "<DISPOSABLE_ROOT>" and run["stderr_utf8"] == "",
                "E_RUN_NORMALIZATION")
        require(run["argv"] == [
            "<PYTHON>", "-B", "-I", "-X", "utf8", "<PROBE>", "<SOURCE>",
            run["mode"], run["route_id"], "<SERIALIZED_DIR>",
        ], "E_RUN_ARGV", str(key))
        require(run["stdout_sha256"] == sha256(run["stdout_utf8"].encode("utf-8"))
                and run["stderr_sha256"] == sha256(b""), "E_RUN_STREAM_HASH")
        parsed = json.loads(run["stdout_utf8"].strip())
        require(parsed == run["observation"], "E_RUN_STDOUT_BINDING")
        if run["mode"] == "route":
            require(run["route_id"] in ROUTE_IDS, "E_RUN_ROUTE_ID")
            route_versions[run["route_id"]].add(run["python"])
            route_observations[run["route_id"]][run["python"]] = run["observation"]
            validate_observation(run["observation"], run["route_id"])
        else:
            require(run["mode"] == "order"
                    and run["route_id"] in {"permutation_a", "permutation_b"},
                    "E_ORDER_ID")
            order_count += 1
            observation = run["observation"]
            validate_order_observation(observation, run["route_id"])
    require(all(versions == {"3.12", "3.14"} for versions in route_versions.values()),
            "E_ROUTE_RUNTIME_PAIR")
    require(order_count == 4, "E_ORDER_COUNT")
    require(set(runtime["cross_runtime_agreement"]) == set(ROUTE_IDS), "E_AGREEMENT_SET")
    for route, agreement in runtime["cross_runtime_agreement"].items():
        require(route_observations[route]["3.12"] == route_observations[route]["3.14"],
                "E_CROSS_RUNTIME_RECOMPUTED", route)
        require(agreement == {
            "profile_counts_equal": True, "temperature_class_equal": True,
            "numeric_summary_within_1e_12": True, "observation_sha256_equal": True,
        }, "E_CROSS_RUNTIME", route)
    aggregate = runtime["aggregate"]
    require(aggregate["route_runs"] == 32 and aggregate["order_runs"] == 4
            and aggregate["successful_processes"] == 36
            and aggregate["stderr_empty"] == 36
            and aggregate["order_restoration_pass"] is True,
            "E_RUNTIME_AGGREGATE")
    require(set(aggregate["temperature_dependent_routes"]) == EXPECTED_TEMP_DEPENDENT,
            "E_RUNTIME_DEP_SET")
    require(set(aggregate["temperature_independent_routes"])
            == set(ROUTE_IDS) - EXPECTED_TEMP_DEPENDENT, "E_RUNTIME_INDEP_SET")
    require(all(value is False for value in runtime["authority_ceiling"].values()),
            "E_RUNTIME_AUTHORITY_PROMOTION")


def validate_matrix(matrix: dict[str, Any], runtime: dict[str, Any]) -> None:
    require(set(matrix) == {"schema", "baseline", "inputs", "source_coverage",
                            "production_ast", "evidence_columns", "route_rows",
                            "default_adjudication", "negative_control_contract",
                            "aggregate", "runtime_binding", "selected_gate",
                            "authority_ceiling", "semantic_sha256"}, "E_MATRIX_TOP_SCHEMA")
    require(matrix["schema"] == "phase066.step080.profile-default-temperature-matrix.v1"
            and matrix["baseline"] == BASELINE and matrix["selected_gate"] == GATE,
            "E_MATRIX_HEADER")
    expected_input_paths = [
        SOURCE_PATH, TEST1024_PATH, TEST1025_PATH,
        "Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md",
        "Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md",
        "Claude/docs/v1.0.25.2/FITTING_GUIDE.md",
        "Claude/results/comp_v26_data/out_versions/A_regsol/params_blend.json",
        "Claude/results/comp_v26_data/out_versions/B_gallery/params_blend.json",
        "Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json",
    ]
    require([binding["path"] for binding in matrix["inputs"]] == expected_input_paths,
            "E_MATRIX_INPUT_SET")
    for binding in matrix["inputs"]:
        verify_input(binding)
    require(matrix["source_coverage"] == {
        "production_python": "READ_FULL_LINES_1_2024",
        "test_gates_v1025": "READ_FULL_LINES_1_398",
        "test_gates_v1024": "READ_FULL_LINES_1_637_DELEGATED_PLUS_AST_CALL_PIN",
        "targeted_release_handover": "LINES_12_75",
        "targeted_archive_history": "LINES_253_364",
        "targeted_fitting_guide": "LINES_29_49",
        "serialized_profile_json": "THREE_FILES_FULL_STRICT_JSON",
    }, "E_SOURCE_COVERAGE")
    source_ast_assertions(matrix["production_ast"])
    require(set(matrix["evidence_columns"]) == {
        "stale_header_comment", "production_assignment", "stale_class_docstring",
        "stale_alpha_comment", "divergent_7_7_pair_examples", "test_mutation",
        "release_handover", "archive_history", "fitting_guide",
    }, "E_EVIDENCE_COLUMNS")
    expected_evidence = {
        "stale_header_comment": (
            "7-gallery defaults and use_legacy_4transition",
            "CONTRADICTED_BY_LATER_PRODUCTION_ASSIGNMENT", SOURCE_PATH, 3, 6),
        "production_assignment": (
            "fresh default is thermodynamic graphite-4 plus si_case fallback",
            "STATIC_PRODUCTION_ROUTE", SOURCE_PATH, 1439, 1470),
        "stale_class_docstring": (
            "constructor docstring says default graphite is 7-gallery",
            "CONTRADICTED_BY_PRODUCTION_ASSIGNMENT_AND_RUNTIME", SOURCE_PATH, 1596, 1601),
        "stale_alpha_comment": (
            "graphite 7-gallery comment says alpha is absent although every literal row carries alpha",
            "CONTRADICTED_WITHIN_ADJACENT_SOURCE", SOURCE_PATH, 1394, 1406),
        "divergent_7_7_pair_examples": (
            "one example pairs graphite skew7 with symmetric Si7 while the confirmed pair names Si skew7",
            "EXPLICIT_ROUTE_REQUIRES_CALLER_CHOICE", SOURCE_PATH, 1396, 1420),
        "test_mutation": (
            "v1024 gate forces use_skew7_default(False) after import",
            "TEST_MUTATION_NOT_FRESH_PUBLIC_DEFAULT", TEST1024_PATH, 70, 79),
        "release_handover": (
            "7/7/14 is explicit seed/switch, not public default; 4 route retains temperature dependence",
            "DOCUMENTED_CORRECTION", "Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md",
            12, 75),
        "archive_history": (
            "U10 default reversal was later withdrawn by U12", "HISTORICAL_SUPERSESSION",
            "Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md", 253, 364),
        "fitting_guide": (
            "w-only is not a multi-temperature profile; n/dH/dS inputs are required",
            "STATIC_GUIDANCE", "Claude/docs/v1.0.25.2/FITTING_GUIDE.md", 29, 49),
    }
    for name, record in matrix["evidence_columns"].items():
        validate_source_ref(record["source"])
        claim, status, path, line_start, line_end = expected_evidence[name]
        require(record["claim"] == claim and record["status"] == status
                and record["source"]["path"] == path
                and record["source"]["line_start"] == line_start
                and record["source"]["line_end"] == line_end,
                "E_EVIDENCE_SEMANTICS", name)
    rows = matrix["route_rows"]
    require([row["route_id"] for row in rows] == ROUTE_IDS, "E_MATRIX_ROUTE_ORDER")
    require([row["id"] for row in rows] == [f"R80-{i:02d}" for i in range(1, 17)],
            "E_MATRIX_ROW_IDS")
    row_schema = {
        "id", "route_id", "route_class", "profile", "declared_sources",
        "serialized_kernel", "serialized_compatibility",
        "temperature_dependent_observed", "equilibrium_max_abs_delta",
        "curve_max_abs_delta", "U_oc_delta_V", "contributions_status",
        "limit_status", "f_Si_zero_bit_exact", "runtime_cross_version",
        "internal_runtime_observed", "external_material_authority",
        "profile_selection_authority", "multi_temperature_experimental_authority",
        "owner",
    }
    for row in rows:
        require(set(row) == row_schema, "E_ROW_SCHEMA", row.get("route_id", "?"))
        route = row["route_id"]
        runtime_observation = next(
            run["observation"] for run in runtime["runs"]
            if run["mode"] == "route" and run["python"] == "3.12"
            and run["route_id"] == route
        )
        expected_owner = ("P067-CODE-HISTORY" if route == "serialized_regsol_8"
                          else "PHASE-069-STEPS-102-104-MODEL-AND-DATA-SYNTHESIS")
        require(row["route_class"] == EXPECTED_ROUTE_CLASS[route]
                and row["profile"] == runtime_observation["profile"]
                and row["declared_sources"] == runtime_observation["declared_sources"]
                and row["temperature_dependent_observed"]
                is runtime_observation["temperature"]["temperature_dependent_observed"]
                and row["equilibrium_max_abs_delta"]
                == runtime_observation["temperature"]["equilibrium_max_abs_delta"]
                and row["curve_max_abs_delta"]
                == runtime_observation["temperature"]["curve_max_abs_delta"]
                and row["U_oc_delta_V"] == runtime_observation["temperature"]["U_oc_delta_V"]
                and row["contributions_status"] == runtime_observation["contributions"]["status"]
                and row["limit_status"] == runtime_observation["limits"]["status"]
                and row["f_Si_zero_bit_exact"]
                == runtime_observation["limits"]["f_Si_zero_bit_exact"]
                and row["owner"] == expected_owner,
                "E_ROW_RUNTIME_FIELDS", route)
        require((row["profile"]["graphite_count"], row["profile"]["silicon_count"],
                 row["profile"]["total_count"]) == EXPECTED_COUNTS[route],
                "E_ROW_COUNTS", route)
        require(row["temperature_dependent_observed"] is (route in EXPECTED_TEMP_DEPENDENT),
                "E_ROW_TEMP_CLASS", route)
        require(row["runtime_cross_version"] == runtime["cross_runtime_agreement"][route],
                "E_ROW_RUNTIME_BINDING", route)
        if route == "serialized_regsol_8":
            require(row["serialized_kernel"] == "regsol"
                    and row["serialized_compatibility"]
                    == "CURRENT_PUBLIC_LOGISTIC_ONLY_KERNEL_METADATA_NOT_DISPATCHED",
                    "E_ROW_SERIALIZED_COMPATIBILITY", route)
        elif route in {"serialized_gallery_14", "serialized_skew_14"}:
            expected_kernel = "logistic" if route == "serialized_gallery_14" else "skew-logistic"
            require(row["serialized_kernel"] == expected_kernel
                    and row["serialized_compatibility"] == "CURRENT_PUBLIC_ROUTE_EXECUTABLE",
                    "E_ROW_SERIALIZED_COMPATIBILITY", route)
        else:
            require(row["serialized_kernel"] is None
                    and row["serialized_compatibility"] == "NOT_APPLICABLE",
                    "E_ROW_SERIALIZED_COMPATIBILITY", route)
        require(row["internal_runtime_observed"] is True
                and row["external_material_authority"] is False
                and row["profile_selection_authority"] is False
                and row["multi_temperature_experimental_authority"] is False
                and bool(row["owner"]), "E_ROW_AUTHORITY", route)
    adjudication = matrix["default_adjudication"]
    require(adjudication == {
        "fresh_public_default": "GRAPHITE_STAGING_LIT_4_PLUS_SIC_LIT_2",
        "fresh_public_default_temperature_dependent": True,
        "skew_7_7_status": "EXPLICIT_OR_TOGGLE_OPT_IN_ONLY",
        "skew_7_7_temperature_dependent": False,
        "test_mutated_default_is_public_default": False,
        "stale_header_or_docstring_is_executable_default": False,
        "global_order_leakage_observed": False,
        "background_constants_auto_applied": False,
    }, "E_DEFAULT_ADJUDICATION")
    require(matrix["aggregate"] == {
        "route_rows": 16, "public_and_explicit_routes": 13, "serialized_routes": 3,
        "temperature_dependent": 9, "temperature_independent": 7,
        "external_authority_true": 0, "profile_selection_authority_true": 0,
        "multi_temperature_experimental_authority_true": 0,
    }, "E_MATRIX_AGGREGATE")
    require(matrix["runtime_binding"] == {
        "path": RUNTIME_PATH, "semantic_sha256": runtime["semantic_sha256"],
        "processes": 36, "cleanup_completed": True,
    }, "E_MATRIX_RUNTIME_BINDING")
    require(matrix["authority_ceiling"] == {
        "internal_static_and_runtime_behavior_verified": True,
        "external_scientific_authority": False, "material_phase_authority": False,
        "profile_selection_authority": False,
        "multi_temperature_experimental_authority": False,
    }, "E_MATRIX_CEILING")
    require(matrix["negative_control_contract"] == EXPECTED_NEGATIVE_CONTRACT,
            "E_NEGATIVE_CONTRACT")


def expected_failure(fn: Callable[[], None], code: str) -> None:
    try:
        fn()
    except ValidationFailure:
        return
    raise ValidationFailure(f"E_NEGATIVE_ACCEPTED: {code}")


def set_key(record: dict[str, Any], key: str, value: Any) -> None:
    record[key] = value


def mutate_cross_runtime(runtime: dict[str, Any]) -> None:
    run = next(item for item in runtime["runs"]
               if item["mode"] == "route" and item["python"] == "3.14"
               and item["route_id"] == "fresh_default_4_2")
    observation = run["observation"]
    observation["temperature"]["U_oc_delta_V"] += 0.125
    seal_projection = copy.deepcopy(observation)
    seal_projection.pop("observation_sha256")
    observation["observation_sha256"] = sha256(json.dumps(
        seal_projection, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode("utf-8"))
    run["stdout_utf8"] = json.dumps(observation, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":"), allow_nan=False) + "\r\n"
    run["stdout_sha256"] = sha256(run["stdout_utf8"].encode("utf-8"))


def run_negative_controls(matrix: dict[str, Any], runtime: dict[str, Any]) -> int:
    controls: list[tuple[str, Callable[[dict[str, Any], dict[str, Any]], None]]] = [
        ("fresh-after-mutation", lambda m, r: set_key(r["process_contract"], "fresh_import_before_any_mutation", False)),
        ("test-default-promotion", lambda m, r: set_key(m["default_adjudication"], "test_mutated_default_is_public_default", True)),
        ("omitted-profile", lambda m, r: m["route_rows"].pop()),
        ("temperature-false-positive", lambda m, r: set_key(m["route_rows"][3], "temperature_dependent_observed", True)),
        ("order-leakage", lambda m, r: set_key(r["aggregate"], "order_restoration_pass", False)),
        ("runtime-authority-promotion", lambda m, r: set_key(r["authority_ceiling"], "runtime_agreement_is_external_material_validation", True)),
        ("regsol-equivalence-promotion", lambda m, r: set_key(m["route_rows"][13], "serialized_compatibility", "CURRENT_KERNEL_EQUIVALENT")),
        ("stale-comment-promotion", lambda m, r: set_key(m["default_adjudication"], "stale_header_or_docstring_is_executable_default", True)),
        ("probe-sha-mismatch", lambda m, r: set_key(r, "probe_sha256", "0" * 64)),
        ("argv-mutation", lambda m, r: r["runs"][0]["argv"].append("--unexpected")),
        ("run-unknown-field", lambda m, r: set_key(r["runs"][0], "unexpected", True)),
        ("cross-runtime-divergence", lambda m, r: mutate_cross_runtime(r)),
        ("matrix-runtime-fabrication", lambda m, r: set_key(m["route_rows"][0], "U_oc_delta_V", 999.0)),
    ]
    for code, mutate in controls:
        m = copy.deepcopy(matrix)
        r = copy.deepcopy(runtime)
        mutate(m, r)
        expected_failure(lambda m=m, r=r: (validate_runtime(r), validate_matrix(m, r)), code)
    return len(controls)


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = dotted_name(node.value)
        return f"{prefix}.{node.attr}" if prefix is not None else node.attr
    return None


def validate_builder_source_policy() -> None:
    tree, _ = builder_tree_and_probe()
    expected_imports = [
        ("argparse", None), ("ast", None), ("copy", None), ("hashlib", None),
        ("json", None), ("os", None), ("re", None), ("shutil", None),
        ("subprocess", None), ("tempfile", None),
    ]
    observed_imports = [(alias.name, alias.asname)
                        for node in tree.body if isinstance(node, ast.Import)
                        for alias in node.names]
    require(observed_imports == expected_imports, "E_BUILDER_POLICY_IMPORT_SET")
    imports_from = [node for node in tree.body if isinstance(node, ast.ImportFrom)]
    require([(node.module, node.level, [(alias.name, alias.asname) for alias in node.names])
             for node in imports_from] == [
        ("__future__", 0, [("annotations", None)]),
        ("pathlib", 0, [("Path", None)]),
        ("typing", 0, [("Any", None)]),
    ], "E_BUILDER_POLICY_FROM_SET")
    forbidden_named_calls = {
        "eval", "exec", "compile", "open", "input", "__import__", "globals",
        "locals", "vars", "getattr", "setattr", "delattr",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            require(not node.attr.startswith("__"), "E_BUILDER_POLICY_DUNDER")
        elif isinstance(node, ast.Call):
            require(isinstance(node.func, (ast.Name, ast.Attribute)),
                    "E_BUILDER_POLICY_INDIRECT_CALL")
            if isinstance(node.func, ast.Name):
                require(node.func.id not in forbidden_named_calls,
                        "E_BUILDER_POLICY_DYNAMIC_CALL", node.func.id)
    module_calls: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = dotted_name(node.func)
        if name is not None and name.split(".", 1)[0] in {
            "os", "shutil", "subprocess", "tempfile"
        }:
            module_calls.append(name)
    require(sorted(module_calls) == sorted([
        "os.environ.get", "os.replace", "shutil.rmtree", "subprocess.run",
        "tempfile.NamedTemporaryFile", "tempfile.mkdtemp",
    ]), "E_BUILDER_POLICY_MODULE_CALLS")
    subprocess_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                        and dotted_name(node.func) == "subprocess.run"]
    require(len(subprocess_calls) == 1, "E_BUILDER_POLICY_PROCESS_COUNT")
    process_keywords = {keyword.arg: keyword.value for keyword in subprocess_calls[0].keywords}
    require(isinstance(process_keywords.get("shell"), ast.Constant)
            and process_keywords["shell"].value is False
            and isinstance(process_keywords.get("check"), ast.Constant)
            and process_keywords["check"].value is False,
            "E_BUILDER_POLICY_PROCESS_KW")
    mutation_names = {
        "NamedTemporaryFile", "mkdtemp", "mkdir", "open", "remove", "rename",
        "replace", "rmdir", "rmtree", "touch", "unlink", "write", "write_bytes",
        "write_text", "writelines", "copy", "copy2", "copyfile", "move",
    }
    mutation_sites: list[tuple[str, str]] = []
    for function in (node for node in tree.body if isinstance(node, ast.FunctionDef)):
        for node in ast.walk(function):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in mutation_names:
                    mutation_sites.append((function.name, node.func.attr))
    all_mutation_calls = [node for node in ast.walk(tree)
                          if isinstance(node, ast.Call)
                          and isinstance(node.func, ast.Attribute)
                          and node.func.attr in mutation_names]
    require(len(all_mutation_calls) == len(mutation_sites),
            "E_BUILDER_POLICY_TOPLEVEL_MUTATION")
    require(sorted(mutation_sites) == sorted([
        ("atomic_json", "mkdir"), ("atomic_json", "NamedTemporaryFile"),
        ("atomic_json", "write"), ("atomic_json", "replace"),
        ("atomic_json", "unlink"), ("run_attestation", "mkdtemp"),
        ("run_attestation", "write_bytes"), ("run_attestation", "write_text"),
        ("run_attestation", "mkdir"), ("run_attestation", "write_bytes"),
        ("run_attestation", "rmtree"),
    ]), "E_BUILDER_POLICY_MUTATION_SITES")


def validate_validator_source_policy() -> None:
    tree = ast.parse((ROOT / VALIDATOR_PATH).read_text(encoding="utf-8"), filename=VALIDATOR_PATH)
    expected_imports = [
        ("argparse", None), ("ast", None), ("copy", None), ("hashlib", None),
        ("json", None), ("re", None), ("subprocess", None), ("sys", None),
        ("tempfile", None),
    ]
    observed_imports = [(alias.name, alias.asname)
                        for node in tree.body if isinstance(node, ast.Import)
                        for alias in node.names]
    require(observed_imports == expected_imports, "E_POLICY_IMPORT_SET")
    imports_from = [node for node in tree.body if isinstance(node, ast.ImportFrom)]
    require([(node.module, node.level, [(alias.name, alias.asname) for alias in node.names])
             for node in imports_from] == [
        ("__future__", 0, [("annotations", None)]),
        ("pathlib", 0, [("Path", None)]),
        ("typing", 0, [("Any", None), ("Callable", None)]),
    ], "E_POLICY_FROM_SET")
    forbidden_named_calls = {
        "eval", "exec", "compile", "open", "input", "__import__", "globals",
        "locals", "vars", "getattr", "setattr", "delattr",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            require(not node.attr.startswith("__"), "E_POLICY_DUNDER")
        elif isinstance(node, ast.Call):
            require(isinstance(node.func, (ast.Name, ast.Attribute)), "E_POLICY_INDIRECT_CALL")
            if isinstance(node.func, ast.Name):
                require(node.func.id not in forbidden_named_calls,
                        "E_POLICY_DYNAMIC_CALL", node.func.id)
    subprocess_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                        and isinstance(node.func, ast.Attribute)
                        and isinstance(node.func.value, ast.Name)
                        and node.func.value.id == "subprocess"]
    require(len(subprocess_calls) == 2
            and all(node.func.attr == "run" for node in subprocess_calls),
            "E_POLICY_PROCESS_CALLS")
    for node in subprocess_calls:
        keywords = {keyword.arg: keyword.value for keyword in node.keywords}
        require(isinstance(keywords.get("shell"), ast.Constant)
                and keywords["shell"].value is False
                and isinstance(keywords.get("check"), ast.Constant)
                and keywords["check"].value is False,
                "E_POLICY_PROCESS_KW")
    module_calls = [dotted_name(node.func) for node in ast.walk(tree)
                    if isinstance(node, ast.Call)
                    and dotted_name(node.func) is not None
                    and dotted_name(node.func).split(".", 1)[0] in {"subprocess", "tempfile"}]
    require(sorted(module_calls) == sorted([
        "subprocess.run", "subprocess.run", "tempfile.TemporaryDirectory",
    ]), "E_POLICY_MODULE_CALLS")
    file_mutation_names = {
        "NamedTemporaryFile", "mkdtemp", "mkdir", "open", "remove", "rename",
        "replace", "rmdir", "rmtree", "touch", "unlink", "write", "write_bytes",
        "write_text", "writelines", "copy", "copy2", "copyfile", "move",
    }
    require(not [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Attribute)
                 and node.func.attr in file_mutation_names], "E_POLICY_FILE_MUTATION")


def regenerate_and_compare() -> None:
    with tempfile.TemporaryDirectory(prefix="p066_step80_validator_") as temporary:
        out = Path(temporary) / "out"
        cp = subprocess.run([sys.executable, "-B", "-X", "utf8",
                             str(ROOT / BUILDER_PATH), "--output-dir", str(out)],
                            cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=False, check=False)
        require(cp.returncode == 0, "E_REGEN_EXIT", cp.stderr.decode("utf-8", "replace"))
        require((out / Path(MATRIX_PATH).name).read_bytes() == (ROOT / MATRIX_PATH).read_bytes(),
                "E_MATRIX_DETERMINISM")
        require((out / Path(RUNTIME_PATH).name).read_bytes() == (ROOT / RUNTIME_PATH).read_bytes(),
                "E_RUNTIME_DETERMINISM")


def validate_documents() -> None:
    required = {
        RESULT_PATH: [GATE, "4+2", "7+7", "36/36", "GROUND_NOT_FOUND", PERSISTENCE],
        PARENT_LEDGER_PATH: [GATE, "76–80", "Step 80"],
        ACTIVE_LEDGER_PATH: [GATE, "Step 80"],
        HANDOVER_PATH: [GATE, "Step 81.1", "Step 80"],
    }
    for path, markers in required.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for marker in markers:
            require(marker in text, "E_DOCUMENT_MARKER", f"{path}: {marker}")
    combined = "\n".join((ROOT / path).read_text(encoding="utf-8")
                           for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH))
    require("Step 79 exact-seven persistence pending" not in combined
            and "Step 80 starts only after" not in combined,
            "E_STALE_HANDOVER")


def validate_git(precommit: bool, expected_commit: str | None) -> None:
    require(git("remote", "get-url", "origin").decode().strip() == ORIGIN_URL, "E_ORIGIN")
    require(git("branch", "--show-current").decode().strip() == BRANCH, "E_BRANCH")
    require(git("rev-parse", f"origin/{PROTECTED_BRANCH}").decode().strip() == PROTECTED_TIP,
            "E_PROTECTED_TIP")
    require(git("rev-parse", "origin/main").decode().strip() == MAIN_TIP, "E_MAIN_TIP")
    live_lines = git("ls-remote", "--heads", "origin", BRANCH,
                     PROTECTED_BRANCH, "main").decode().splitlines()
    live = {ref: commit for commit, ref in (line.split() for line in live_lines)}
    require(live == {
        f"refs/heads/{BRANCH}": git("rev-parse", "HEAD").decode().strip(),
        f"refs/heads/{PROTECTED_BRANCH}": PROTECTED_TIP,
        "refs/heads/main": MAIN_TIP,
    }, "E_LIVE_REMOTE_SET")
    require(git("rev-parse", "@{upstream}").decode().strip()
            == git("rev-parse", "HEAD").decode().strip(), "E_PRECOMMIT_UPSTREAM")
    require(not git("diff", "--name-only", BASELINE, "--", "Claude"), "E_CLAUDE_DRIFT")
    if precommit:
        require(git("rev-parse", "HEAD").decode().strip() == EXPECTED_PARENT, "E_PRECOMMIT_HEAD")
        staged = sorted(git("diff", "--cached", "--name-only").decode().splitlines())
        require(staged == FINAL_PATHS, "E_STAGED_PATHS", str(staged))
        require(not git("diff", "--name-only", "--", *FINAL_PATHS), "E_UNSTAGED_FINAL")
        require(not git("diff", "--name-only"), "E_UNSTAGED_TRACKED")
        require(not git("ls-files", "--others", "--exclude-standard"), "E_UNTRACKED")
    else:
        require(expected_commit is not None
                and re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None,
                "E_EXPECTED_COMMIT")
        head = git("rev-parse", "HEAD").decode().strip()
        require(head == expected_commit, "E_PERSISTENCE_HEAD")
        require(git("rev-parse", "HEAD^").decode().strip() == EXPECTED_PARENT,
                "E_PERSISTENCE_PARENT")
        require(git("show", "-s", "--format=%s", "HEAD").decode().strip() == EXPECTED_SUBJECT,
                "E_PERSISTENCE_SUBJECT")
        changed = sorted(git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").decode().splitlines())
        require(changed == FINAL_PATHS, "E_PERSISTENCE_PATHS")
        require(git("rev-parse", "@{upstream}").decode().strip() == head, "E_UPSTREAM")
        remote = git("ls-remote", "--heads", "origin", BRANCH).decode().split()
        require(len(remote) == 2 and remote[0] == head, "E_LIVE_REMOTE")
        require(not git("status", "--porcelain=v1"), "E_DIRTY")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    if args.persistence:
        require(args.expected_commit is not None
                and re.fullmatch(r"[0-9a-f]{40}", args.expected_commit) is not None,
                "E_EXPECTED_COMMIT")
    else:
        require(args.expected_commit is None, "E_PRECOMMIT_EXPECTED_COMMIT")
    validate_validator_source_policy()
    validate_builder_source_policy()
    matrix = strict_json((ROOT / MATRIX_PATH).read_bytes())
    runtime = strict_json((ROOT / RUNTIME_PATH).read_bytes())
    validate_runtime(runtime)
    validate_matrix(matrix, runtime)
    negatives = run_negative_controls(matrix, runtime)
    validate_documents()
    regenerate_and_compare()
    validate_git(not args.persistence, args.expected_commit)
    if args.persistence:
        print(f"{PERSISTENCE} commit={args.expected_commit} negative={negatives}/{negatives}")
    else:
        print("PASS_P066_STEP80_VALIDATION "
              f"routes={len(ROUTE_IDS)} processes={runtime['aggregate']['successful_processes']} "
              f"negative={negatives}/{negatives} deterministic=2/2 gate={GATE}")


if __name__ == "__main__":
    try:
        main()
    except ValidationFailure as exc:
        raise SystemExit(str(exc))
