#!/usr/bin/env python3
"""Build Phase 067 Step 85 mutable/default/import/persistence evidence.

Production code is read from frozen Git objects and imported only by isolated
child processes in disposable directories. The controller never imports the
production module and never writes inside Claude/**.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_PARENT = "f00bf2fa8f25c85f0c62cb901912763d98c8f070"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
EXPECTED_SUBJECT = "audit(phase067): separate defaults state persistence"
GATE = "PASS_P067_STEP85_STATE_DEFAULT_IMPORT"
PERSISTENCE = "PASS_P067_STEP85_PERSISTENCE"
GENERATED_DATE = "2026-09-02"
BUILDER_SOURCE_POLICY_SHA256_LF = "1f299dc25d048de3e194bbe6d84ff301a839bd5c8cf8125f59f99489f800052c"

INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
STEP83_PATH = "Codex/results/PHASE_067_STATE_QUANTITY_FLOW_MATRIX.json"
STEP84_PATH = "Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json"
P066_MATRIX_PATH = "Codex/results/PHASE_066_PROFILE_DEFAULT_TEMPERATURE_MATRIX.json"
P066_RUNTIME_PATH = "Codex/results/PHASE_066_RUNTIME_ATTESTATION.json"
P066_CARRY_PATH = "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json"

INPUT_PINS = {
    INVENTORY_PATH: ("b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63", "593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1"),
    ATTESTATION_PATH: ("112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174", "e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9"),
    STEP83_PATH: ("0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8", "c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44"),
    STEP84_PATH: ("54fddbdab2a3cb4666d61c9f9eefe005e8d7c1fa247433fa80f86ef416273e9f", "63acc6de1597a97eda51b1eaa448e7c1396ad374f7ffc5cb2d53103d78a11adc"),
    P066_MATRIX_PATH: ("7bab3f907ab6879fec0854c94f05e7d0b42fc618d6585f2737750e2a2b1b0695", "da615e36ce8df9d16e8ca7dfb69d1a74137510c1212cf2e2fcb53e8850fc2f75"),
    P066_RUNTIME_PATH: ("a5c909105280cf11a72ca9189070feb59c9005a824eeee4f3e161660394539d4", "3a393149d36513233e46ebbdbb0ce36f0393e28cb88e1fd3704cef5bf83fb040"),
    P066_CARRY_PATH: ("847e74956d16cc9bdcc42c36b0ddd1d73ea5ac79464d55461d2e08cf09a60003", "b7847cd1ce29fee7b0304c1ee92e81645ab149949a80aab1d9c6fc77003856c6"),
}

SOURCE_PATH = "Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py"
TEST_PATH = "Claude/docs/v1.0.25.2/test_gates_v1024.py"
WRITER_PATH = "Claude/results/comp_v26_data/build_two_versions.py"
SAVED_PATHS = {
    "A_regsol": "Claude/results/comp_v26_data/out_versions/A_regsol/params_blend.json",
    "B_gallery": "Claude/results/comp_v26_data/out_versions/B_gallery/params_blend.json",
    "C_skew": "Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json",
}

BUILDER_PATH = "Codex/work/v1025_phase067/build_phase067_step85.py"
VALIDATOR_PATH = "Codex/work/v1025_phase067/validate_phase067_step85.py"
MATRIX_PATH = "Codex/results/PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX.json"
RUNTIME_PATH = "Codex/results/PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION.json"
RESULT_PATH = "Codex/results/PHASE_067_STEP_085_STATE_DEFAULT_IMPORT_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
CONTROL_PATHS = (BUILDER_PATH, VALIDATOR_PATH, RESULT_PATH, PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER)
FINAL_PATHS = (BUILDER_PATH, VALIDATOR_PATH, MATRIX_PATH, RUNTIME_PATH, RESULT_PATH,
               PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER)

PYTHON_LAUNCHERS = (("3.12", ("py", "-3.12")), ("3.14", ("py", "-3.14")))
CASE_IDS = (
    "C01_FRESH_BASELINE",
    "C02_EXPLICIT_PROFILE",
    "C03_SKEW_REBIND_EXISTING_FUTURE",
    "C04_INPLACE_TRANSITION_ALIAS",
    "C05_SI_REBIND_SEED_CACHE",
    "C06_ORDINARY_IMPORT_CACHE",
    "C07_EXPLICIT_RELOAD",
    "C08_TWO_SPEC_LOAD_OBJECTS",
    "C09_NEW_PROCESS_RESET",
    "C10_TOGGLE_ORDER_A",
    "C11_TOGGLE_ORDER_B",
    "C12_ALIAS_EXPORT_GNF",
    "C13_SAVED_ROUTE_GNF",
)


class BuildError(RuntimeError):
    pass


def require(condition: bool, diagnostic: str) -> None:
    if not condition:
        raise BuildError(diagnostic)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic_sha(value: dict[str, Any]) -> str:
    clone = copy.deepcopy(value)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def finalize(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = semantic_sha(value)
    return value


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf"), f"E_JSON_BOM:{label}")
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, f"E_JSON_DUPLICATE:{label}:{key}")
            out[key] = value
        return out
    def constant(token: str) -> None:
        raise BuildError(f"E_JSON_NONFINITE:{label}:{token}")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    require(isinstance(value, dict), f"E_JSON_TOP:{label}")
    stack = [(value, 1)]
    nodes = 0
    while stack:
        current, depth = stack.pop()
        nodes += 1
        require(nodes <= 600_000 and depth <= 18, f"E_JSON_BOUNDS:{label}")
        if isinstance(current, dict):
            stack.extend((entry, depth + 1) for entry in current.values())
        elif isinstance(current, list):
            stack.extend((entry, depth + 1) for entry in current)
        elif isinstance(current, float):
            require(math.isfinite(current), f"E_JSON_NONFINITE:{label}")
    return value


def run_git(args: tuple[str, ...]) -> bytes:
    allowed = False
    if len(args) == 2 and args[0] == "show" and ":" in args[1]:
        revision, path = args[1].split(":", 1)
        allowed = revision in {EXPECTED_PARENT, BASELINE} and (
            path in INPUT_PINS or path in {SOURCE_PATH, TEST_PATH, WRITER_PATH, *SAVED_PATHS.values()})
    elif len(args) == 3 and args[:2] == ("cat-file", "blob"):
        allowed = bool(re.fullmatch(r"[0-9a-f]{40}", args[2]))
    elif len(args) == 2 and args[0] == "rev-parse" and ":" in args[1]:
        revision, path = args[1].split(":", 1)
        allowed = revision == BASELINE and path in {SOURCE_PATH, TEST_PATH, WRITER_PATH, *SAVED_PATHS.values()}
    elif len(args) == 4 and args[:3] == ("ls-tree", BASELINE, "--"):
        allowed = args[3] in SAVED_PATHS.values()
    require(allowed, "E_GIT_ARGV")
    cp = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, shell=False,
                        check=False, timeout=90)
    require(cp.returncode == 0, f"E_GIT_READ:{args!r}:{cp.stderr.decode('utf-8', 'replace')}")
    return cp.stdout


def commit_bytes(path: str) -> bytes:
    return run_git(("show", f"{EXPECTED_PARENT}:{path}"))


def baseline_bytes(path: str) -> bytes:
    return run_git(("show", f"{BASELINE}:{path}"))


def blob_bytes(oid: str) -> bytes:
    return run_git(("cat-file", "blob", oid))


def load_input(path: str) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = commit_bytes(path)
    raw_pin, semantic_pin = INPUT_PINS[path]
    require(sha256(raw) == raw_pin, f"E_INPUT_RAW:{path}")
    value = strict_json(raw, path)
    require(value.get("semantic_sha256") == semantic_pin, f"E_INPUT_SEMANTIC_STORED:{path}")
    if path not in {INVENTORY_PATH, ATTESTATION_PATH}:
        clone = copy.deepcopy(value)
        clone.pop("semantic_sha256", None)
        fresh = (sha256(json.dumps(clone, ensure_ascii=False, sort_keys=True,
                                  separators=(",", ":"), allow_nan=False).encode("utf-8"))
                 if path in {P066_MATRIX_PATH, P066_RUNTIME_PATH, P066_CARRY_PATH}
                 else semantic_sha(value))
        require(fresh == semantic_pin, f"E_INPUT_SEMANTIC_FRESH:{path}")
    return value, {"path": path, "raw_sha256": raw_pin, "semantic_sha256": semantic_pin}


def stable_ast(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {"_type": type(value).__name__,
                **{field: stable_ast(getattr(value, field, None)) for field in value._fields}}
    if isinstance(value, list):
        return [stable_ast(item) for item in value]
    if isinstance(value, bytes):
        return {"_bytes_hex": value.hex()}
    if isinstance(value, complex):
        return {"_complex": [value.real, value.imag]}
    if value is Ellipsis:
        return {"_ellipsis": True}
    return value


def anchor(path: str, source: str, node: ast.AST, owner: str) -> dict[str, Any]:
    segment = ast.get_source_segment(source, node) or ""
    return {
        "path": path, "qualified_owner": owner, "ast_kind": type(node).__name__,
        "start_line": int(getattr(node, "lineno", 0)),
        "end_line": int(getattr(node, "end_lineno", getattr(node, "lineno", 0))),
        "source_sha256": sha256(segment.encode("utf-8")),
        "ast_sha256": sha256(canonical_bytes(stable_ast(node))),
    }


def assignment_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        return node.targets[0].id
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return node.target.id
    return None


def source_static() -> dict[str, Any]:
    raw = baseline_bytes(SOURCE_PATH)
    text = raw.decode("utf-8")
    tree = ast.parse(text, filename=SOURCE_PATH)
    assignments = {assignment_name(node): node for node in tree.body if assignment_name(node)}
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    expected = {
        "R": "8.314", "F": "96485.0",
        "R_SI": "8.314462618", "F_SI": "96485.33212",
        "DEFAULT_GRAPHITE_TRANSITIONS": "GRAPHITE_STAGING_LIT",
        "DEFAULT_SI_TRANSITIONS": "None",
        "DEFAULT_CBG_GRAPHITE": "0.55",
        "DEFAULT_CBG_SI": "0.051",
    }
    assignment_rows = []
    for name, expression in expected.items():
        node = assignments.get(name)
        require(node is not None and ast.unparse(node.value) == expression, f"E_ASSIGNMENT:{name}")
        assignment_rows.append({"name": name, "value_expression": expression,
                                "anchor": anchor(SOURCE_PATH, text, node, "<module>")})
    toggle = functions.get("use_skew7_default")
    require(toggle is not None, "E_TOGGLE_ABSENT")
    toggle_text = ast.unparse(toggle)
    for token in ("global DEFAULT_GRAPHITE_TRANSITIONS, DEFAULT_SI_TRANSITIONS",
                  "DEFAULT_GRAPHITE_TRANSITIONS = GRAPHITE_MSMR7_LIT",
                  "DEFAULT_SI_TRANSITIONS = SI_MSMR7_SKEW_LIT",
                  "DEFAULT_GRAPHITE_TRANSITIONS = GRAPHITE_STAGING_LIT",
                  "DEFAULT_SI_TRANSITIONS = None"):
        require(token in toggle_text, f"E_TOGGLE_TOKEN:{token}")
    si_toggle = functions.get("use_si_constants")
    require(si_toggle is not None, "E_SI_TOGGLE_ABSENT")
    si_toggle_text = ast.unparse(si_toggle)
    for token in ("global R, F", "R, F = (R_SI, F_SI)",
                  "R, F = (_R_LEGACY, _F_LEGACY)"):
        require(token in si_toggle_text, f"E_SI_TOGGLE_TOKEN:{token}")
    blend = next(node for node in tree.body if isinstance(node, ast.ClassDef)
                 and node.name == "BlendedAnodeDQDV")
    init = next(node for node in blend.body if isinstance(node, ast.FunctionDef) and node.name == "__init__")
    init_text = ast.unparse(init)
    require("DEFAULT_GRAPHITE_TRANSITIONS if graphite_transitions is None" in init_text,
            "E_INIT_GRAPHITE")
    require("DEFAULT_SI_TRANSITIONS is not None" in init_text, "E_INIT_SI")
    q_gr_default = next(node for node in ast.walk(blend)
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "from_wt")
    q_gr_expression = ast.unparse(q_gr_default.args.defaults[-2])
    require(q_gr_expression == "GRAPHITE_SPECIFIC_CAPACITY", "E_QGR_DEFAULT")
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    absent = {
        "load_profile": "load_profile" not in names,
        "from_profile": "from_profile" not in names,
        "PROFILE_ALIASES": "PROFILE_ALIASES" not in names,
        "SAVED_PROFILES": "SAVED_PROFILES" not in names,
        "module___all__": "__all__" not in assignments,
        "use_legacy_4transition": "use_legacy_4transition" not in names,
    }
    require(all(absent.values()), "E_PRODUCTION_SURFACE_ABSENCE")
    return {
        "path": SOURCE_PATH,
        "blob_oid": run_git(("rev-parse", f"{BASELINE}:{SOURCE_PATH}")).decode().strip(),
        "raw_sha256": sha256(raw), "physical_lines": len(text.splitlines()), "ast_parse": "PASS",
        "assignment_rows": assignment_rows,
        "toggle": {"name": "use_skew7_default",
                   "anchor": anchor(SOURCE_PATH, text, toggle, "use_skew7_default")},
        "si_constants_toggle": {
            "name": "use_si_constants",
            "legacy": {"R": 8.314, "F": 96485.0},
            "si": {"R": 8.314462618, "F": 96485.33212},
            "anchor": anchor(SOURCE_PATH, text, si_toggle, "use_si_constants"),
        },
        "constructor_default_load": anchor(SOURCE_PATH, text, init, "BlendedAnodeDQDV.__init__"),
        "from_wt_q_gr_default": {"expression": q_gr_expression,
                                 "runtime_bound_value": 372.0,
                                 "anchor": anchor(SOURCE_PATH, text, q_gr_default, "BlendedAnodeDQDV.from_wt")},
        "absent_surfaces": absent,
        "header_docstring_conflict": {
            "status": "STALE_PROSE_CONFLICT_EXECUTABLE_ASSIGNMENT_WINS",
            "runtime_adjudication": "STEP85_FRESH_ISOLATED_PROCESS",
        },
    }


SEARCH_NAMES = ("load_profile", "from_profile", "PROFILE_ALIASES", "SAVED_PROFILES",
                "__all__", "use_legacy_4transition", "use_skew7_default",
                "use_si_constants", "R_SI", "F_SI", "_R_LEGACY", "_F_LEGACY")


def full_blob_search(inventory: dict[str, Any]) -> dict[str, Any]:
    rows = []
    all_rows = []
    for record in inventory["blob_records"]:
        oid = record["blob_oid"]
        text = blob_bytes(oid).decode("utf-8")
        tree = ast.parse(text)
        matches = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name, kind = node.name, type(node).__name__
            elif isinstance(node, ast.Name):
                name, kind = node.id, "Name"
            else:
                continue
            if name in SEARCH_NAMES:
                matches.append({"name": name, "kind": kind,
                                "line": int(getattr(node, "lineno", 0))})
        occurrences = [row for row in inventory["occurrence_records"] if row["blob_oid"] == oid]
        projection = {
            "blob_oid": oid, "blob_ordinal": record["ordinal"],
            "occurrence_paths": sorted(row["path"] for row in occurrences),
            "role_projection": sorted({row["role"] for row in occurrences}),
            "matches": sorted(matches, key=lambda row: (row["name"], row["line"], row["kind"])),
        }
        all_rows.append(projection)
        if matches:
            rows.append(projection)
    production_loader_matches = [
        match for row in all_rows if "code" in row["role_projection"]
        for match in row["matches"]
        if match["name"] in {"load_profile", "from_profile", "PROFILE_ALIASES", "SAVED_PROFILES", "__all__"}
    ]
    require(len(all_rows) == 84, "E_SEARCH_BLOBS")
    require(not production_loader_matches, "E_PRODUCTION_LOADER_MATCH")
    return {
        "searched_occurrences": 129,
        "searched_unique_python_blobs": 84,
        "ast_parse_pass": 84,
        "search_names": list(SEARCH_NAMES),
        "searched_exact_names_matches": production_loader_matches,
        "searched_exact_names_status": "GROUND_NOT_FOUND",
        "matched_blob_rows": rows,
        "all_blob_projection_sha256": sha256(canonical_bytes(all_rows)),
    }


def production_projection(inventory: dict[str, Any]) -> dict[str, Any]:
    occurrences = [copy.deepcopy(row) for row in inventory["occurrence_records"]
                   if row["role"] == "code"]
    blob_oids = {row["blob_oid"] for row in occurrences}
    blobs = [copy.deepcopy(row) for row in inventory["blob_records"]
             if row["blob_oid"] in blob_oids]
    require(len(occurrences) == 20 and len(blobs) == len(blob_oids) == 15,
            "E_PRODUCTION_DENOMINATOR")
    bindings = []
    si_rows = []
    for blob in blobs:
        members = [row for row in occurrences if row["blob_oid"] == blob["blob_oid"]]
        bindings.append({
            "blob_oid": blob["blob_oid"], "blob_ordinal": blob["ordinal"],
            "shared_blob_ref": f"P067-S82-B{blob['ordinal']:03d}",
            "occurrence_count": len(members),
            "occurrence_ordinals": [row["ordinal"] for row in members],
            "occurrence_paths": [row["path"] for row in members],
        })
    for row in occurrences:
        raw = blob_bytes(row["blob_oid"])
        tree = ast.parse(raw.decode("utf-8"), filename=row["path"])
        has_si_toggle = any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                            and node.name == "use_si_constants" for node in ast.walk(tree))
        if has_si_toggle:
            si_rows.append({
                "release": row["release"], "ordinal": row["ordinal"],
                "manifest_entry_index": row["manifest_entry_index"], "path": row["path"],
                "blob_oid": row["blob_oid"], "blob_ordinal": row["blob_ordinal"],
                "shared_blob_ref": f"P067-S82-B{row['blob_ordinal']:03d}",
            })
    require([row["release"] for row in si_rows] == ["v1.0.25.1", "v1.0.25.2", "v1.0.25"],
            "E_SI_TOGGLE_RELEASES")
    require(len(si_rows) == 3 and len({row["blob_oid"] for row in si_rows}) == 2,
            "E_SI_TOGGLE_PROJECTION")
    projection = {"occurrences": occurrences, "blobs": blobs,
                  "shared_blob_bindings": bindings}
    return {
        **projection, "occurrence_count": 20, "unique_blob_count": 15,
        "projection_sha256": sha256(canonical_bytes(projection)),
        "use_si_constants_occurrences": si_rows,
        "use_si_constants_occurrence_count": 3,
        "use_si_constants_unique_blob_count": 2,
    }


def saved_profiles() -> list[dict[str, Any]]:
    expected_transition_keys = {
        "A_regsol": ["Omega", "Omega_over_RT", "Q", "U", "two_phase", "w", "x_binodal"],
        "B_gallery": ["Q", "U", "w"],
        "C_skew": ["Q", "U", "alpha", "w"],
    }
    metrics_keys = ["BIC", "R2", "area_data", "area_model", "bg", "npar",
                    "peakRMSE", "valleyRMSE"]
    rows = []
    for route, path in SAVED_PATHS.items():
        raw = baseline_bytes(path)
        value = strict_json(raw, path)
        transitions = value.get("transitions")
        metrics = value.get("metrics")
        require(set(value) == {"material", "kernel", "N", "metrics", "transitions"},
                f"E_SAVED_TOP_SCHEMA:{route}")
        require(type(value["material"]) is str and type(value["kernel"]) is str
                and type(value["N"]) is int, f"E_SAVED_TOP_TYPES:{route}")
        require(isinstance(transitions, list) and isinstance(metrics, dict), f"E_SAVED_SCHEMA:{route}")
        require(sorted(metrics) == metrics_keys and type(metrics["npar"]) is int
                and all(type(metrics[key]) is float for key in metrics if key != "npar"),
                f"E_SAVED_METRICS:{route}")
        require(value["N"] == len(transitions), f"E_SAVED_N:{route}")
        require(all(isinstance(item, dict) and sorted(item) == expected_transition_keys[route]
                    for item in transitions), f"E_SAVED_TRANSITIONS:{route}")
        for item in transitions:
            for key, entry in item.items():
                expected_type = bool if key == "two_phase" else float
                require(type(entry) is expected_type, f"E_SAVED_TRANSITION_TYPE:{route}:{key}")
                if type(entry) is float:
                    require(math.isfinite(entry), f"E_SAVED_TRANSITION_FINITE:{route}:{key}")
        tree_row = run_git(("ls-tree", BASELINE, "--", path)).decode("utf-8").strip()
        meta, tree_path = tree_row.split("\t", 1)
        mode, kind, tree_oid = meta.split()
        require(mode == "100644" and kind == "blob" and tree_path == path,
                f"E_SAVED_TREE:{route}")
        oid = run_git(("rev-parse", f"{BASELINE}:{path}")).decode().strip()
        require(tree_oid == oid, f"E_SAVED_TREE_OID:{route}")
        rows.append({
            "route": route, "path": path,
            "blob_oid": oid, "git_mode": mode,
            "raw_sha256": sha256(raw), "top_keys": sorted(value),
            "material": value["material"], "kernel": value["kernel"], "N": value["N"],
            "transition_count": len(transitions),
            "transition_keysets": [sorted(item) for item in transitions],
            "transition_value_types": [
                {key: type(entry).__name__ for key, entry in sorted(item.items())}
                for item in transitions],
            "finite_numeric_values": True,
            "metrics_keys": sorted(metrics),
            "metrics_value_types": {key: type(entry).__name__
                                    for key, entry in sorted(metrics.items())},
            "metrics_values": metrics,
            "canonical_roundtrip_sha256": sha256(canonical_bytes(value)),
            "strict_parse_canonical_dump_semantic_identity": True,
            "searched_loader_names_status": "GROUND_NOT_FOUND",
            "config_replay_authority": "CONFIG_GENEALOGY_ONLY",
        })
    require([row["transition_count"] for row in rows] == [8, 14, 14], "E_SAVED_COUNTS")
    require([(row["material"], row["kernel"], row["N"]) for row in rows] ==
            [("blend", "regsol", 8), ("blend", "logistic", 14),
             ("blend", "skew-logistic", 14)], "E_SAVED_IDENTITY")
    return rows


def writer_evidence() -> dict[str, Any]:
    raw = baseline_bytes(WRITER_PATH)
    text = raw.decode("utf-8")
    tree = ast.parse(text, filename=WRITER_PATH)
    writes = []
    loads = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        call = ast.unparse(node.func)
        expression = ast.unparse(node)
        if ("write" in call or "dump" in call) and ("params" in expression or "json" in expression.lower()):
            writes.append(anchor(WRITER_PATH, text, node, "<static-owner>"))
        if ("load" in call or "read" in call) and "params_blend" in expression:
            loads.append(anchor(WRITER_PATH, text, node, "<static-owner>"))
    require(writes, "E_WRITER_GROUND")
    return {
        "path": WRITER_PATH,
        "blob_oid": run_git(("rev-parse", f"{BASELINE}:{WRITER_PATH}")).decode().strip(),
        "raw_sha256": sha256(raw), "write_anchors": writes,
        "saved_profile_loader_anchors": loads,
        "classification": "WRITER_EVIDENCE_NOT_PRODUCTION_LOADER",
    }


PROBE_SOURCE = r'''
from __future__ import annotations
import hashlib, importlib, importlib.util, json, os, pathlib, sys

source_dir=pathlib.Path(sys.argv[1]); case=sys.argv[2]; saved_dir=pathlib.Path(sys.argv[3])
sys.path.insert(0,str(source_dir))
m=importlib.import_module('anode_fit_frozen')

def canon(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def counts(obj): return {'graphite':len(obj.gr_host.transitions),'silicon':len(obj.si_host.transitions),'total':len(obj.transitions)}
def rf(mod): return {'R':mod.R,'F':mod.F,'R_is_legacy':mod.R==mod._R_LEGACY,'F_is_legacy':mod.F==mod._F_LEGACY,'R_is_si':mod.R==mod.R_SI,'F_is_si':mod.F==mod.F_SI,'width_298':float(mod.func_w(298.15))}
def seed(obj): return [float(v) for v in obj.gr_host.seed_L_V]
def snap(mod,label):
    model=mod.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0)
    return {'label':label,'counts':counts(model),
            'graphite_legacy':mod.DEFAULT_GRAPHITE_TRANSITIONS is mod.GRAPHITE_STAGING_LIT,
            'graphite_skew':mod.DEFAULT_GRAPHITE_TRANSITIONS is mod.GRAPHITE_MSMR7_LIT,
            'si_none':mod.DEFAULT_SI_TRANSITIONS is None,
            'si_skew':mod.DEFAULT_SI_TRANSITIONS is mod.SI_MSMR7_SKEW_LIT,
            'constants':rf(mod),'graphite_seed_L_V':seed(model)}
def spec_load(name):
    spec=importlib.util.spec_from_file_location(name,source_dir/'anode_fit_frozen.py')
    if spec is None or spec.loader is None: raise RuntimeError('loader unavailable')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

out={'case_id':case,'fresh_first':True,'events':[snap(m,'fresh_before_mutation')],
     'runtime':{'implementation':sys.implementation.name,'version':list(sys.version_info[:3]),
                'pid':os.getpid()},
     'surfaces':{name:hasattr(m,name) for name in
                 ('load_profile','from_profile','PROFILE_ALIASES','SAVED_PROFILES','__all__',
                  'use_legacy_4transition','use_skew7_default','use_si_constants','R_SI','F_SI')}}
if case=='C01_FRESH_BASELINE':
    out['ordinary_reimport_same_object']=importlib.import_module('anode_fit_frozen') is m
    out['from_wt_q_gr_default']=m.BlendedAnodeDQDV.from_wt.__func__.__defaults__[1]
elif case=='C02_EXPLICIT_PROFILE':
    x=m.BlendedAnodeDQDV(0.2,graphite_transitions=m.GRAPHITE_MSMR7_LIT,
                         si_transitions=m.SI_MSMR7_SKEW_LIT,Cbg=0.0)
    out['explicit_counts']=counts(x); out['events'].append(snap(m,'globals_unchanged'))
elif case=='C03_SKEW_REBIND_EXISTING_FUTURE':
    old=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0); old_si=id(old.si_host.transitions)
    m.use_skew7_default(True)
    new=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0)
    out['existing_counts_after_rebind']=counts(old); out['future_counts_after_rebind']=counts(new)
    out['existing_si_identity_stable']=id(old.si_host.transitions)==old_si
    out['future_si_is_copied_from_default']=id(new.si_host.transitions)!=id(m.DEFAULT_SI_TRANSITIONS)
    out['events'].append(snap(m,'future_after_rebind'))
elif case=='C04_INPLACE_TRANSITION_ALIAS':
    old=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0)
    before=counts(old); m.GRAPHITE_STAGING_LIT.append(dict(m.GRAPHITE_STAGING_LIT[-1]))
    out['existing_before']=before; out['existing_after_inplace']=counts(old)
    out['future_after_inplace']=counts(m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0))
elif case=='C05_SI_REBIND_SEED_CACHE':
    old=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0); old_seed=seed(old)
    imported_R,imported_F=m.R,m.F; before=rf(m)
    m.use_si_constants(True); after_true=rf(m)
    dynamic_after=float(m.func_w(298.15)); old_after=seed(old)
    future=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0); future_seed=seed(future)
    m.use_si_constants(False); after_false=rf(m)
    out.update({'legacy_before':before,'si_after_true':after_true,'legacy_after_false':after_false,
                'R_SI':m.R_SI,'F_SI':m.F_SI,'legacy_R':m._R_LEGACY,'legacy_F':m._F_LEGACY,
                'imported_scalar_alias_after_true':{'R':imported_R,'F':imported_F,
                    'follows_rebind':imported_R==after_true['R'] and imported_F==after_true['F']},
                'dynamic_width_after_true':dynamic_after,'existing_seed_before':old_seed,
                'existing_seed_after_true':old_after,'existing_seed_unchanged':old_seed==old_after,
                'future_seed_under_si':future_seed,'future_seed_differs_from_existing':future_seed!=old_seed})
elif case=='C06_ORDINARY_IMPORT_CACHE':
    m.use_skew7_default(True); again=importlib.import_module('anode_fit_frozen')
    out['same_module_object']=again is m; out['events'].append(snap(again,'ordinary_reimport_mutated'))
elif case=='C07_EXPLICIT_RELOAD':
    old=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0); old_seed=seed(old)
    old_gr_id=id(old.gr_host.transitions); old_si_id=id(old.si_host.transitions)
    m.use_skew7_default(True); m.use_si_constants(True); out['events'].append(snap(m,'before_reload'))
    again=importlib.reload(m); out['same_module_object']=again is m
    out['events'].append(snap(again,'after_reload_reset'))
    out['module_dict_reexecuted_defaults_reset']=rf(again)['R_is_legacy'] and out['events'][-1]['counts']['total']==6
    out['existing_transition_identity_stable']=(id(old.gr_host.transitions)==old_gr_id and id(old.si_host.transitions)==old_si_id)
    out['existing_counts_after_reload']=counts(old); out['existing_seed_after_reload']=seed(old)
    out['existing_seed_unchanged']=old_seed==seed(old); out['existing_seed_before_reload']=old_seed
elif case=='C08_TWO_SPEC_LOAD_OBJECTS':
    a=spec_load('step85_a'); b=spec_load('step85_b'); a.use_skew7_default(True)
    out['distinct_objects']=a is not b; out['a_after_toggle']=snap(a,'a_mutated')
    out['b_independent_fresh']=snap(b,'b_fresh')
elif case=='C09_NEW_PROCESS_RESET':
    out['fresh_isolated_process']=out['events'][0]
    out['paired_prior_case_id']='C06_ORDINARY_IMPORT_CACHE'
elif case=='C10_TOGGLE_ORDER_A':
    old=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0); old_seed=seed(old)
    m.use_si_constants(True); out['events'].append(snap(m,'si_then'))
    m.use_skew7_default(True); future=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0)
    out['events'].append(snap(m,'si_then_skew'))
    out['existing_seed_unchanged']=seed(old)==old_seed; out['existing_counts']=counts(old)
    out['future_counts']=counts(future); out['future_seed']=seed(future); out['final_constants']=rf(m)
elif case=='C11_TOGGLE_ORDER_B':
    old=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0); old_seed=seed(old)
    m.use_skew7_default(True); out['events'].append(snap(m,'skew_then'))
    m.use_si_constants(True); future=m.BlendedAnodeDQDV(0.2,si_case='sic',Cbg=0.0)
    out['events'].append(snap(m,'skew_then_si'))
    out['existing_seed_unchanged']=seed(old)==old_seed; out['existing_counts']=counts(old)
    out['future_counts']=counts(future); out['future_seed']=seed(future); out['final_constants']=rf(m)
elif case=='C12_ALIAS_EXPORT_GNF':
    absent_names=('load_profile','from_profile','PROFILE_ALIASES','SAVED_PROFILES','__all__','use_legacy_4transition')
    out['searched_absent_names']=list(absent_names)
    out['all_absent']=all(not out['surfaces'][name] for name in absent_names)
    out['present_toggle_names']=[name for name in ('use_skew7_default','use_si_constants','R_SI','F_SI')
                                 if out['surfaces'][name]]
elif case=='C13_SAVED_ROUTE_GNF':
    rows=[]; metadata=json.loads((saved_dir/'metadata.json').read_text(encoding='utf-8'))
    for route in ('A_regsol','B_gallery','C_skew'):
        raw=(saved_dir/(route+'.json')).read_bytes(); payload=json.loads(raw.decode('utf-8'))
        model=m.GraphiteAnodeDischargeDQDV([dict(t) for t in payload['transitions']],
                                           Cbg=payload['metrics']['bg'])
        meta=metadata[route]
        rows.append({'route':route,'path':meta['path'],'blob_oid':meta['blob_oid'],
                     'git_mode':meta['git_mode'],'raw_sha256':meta['raw_sha256'],
                     'material':payload['material'],'kernel':payload['kernel'],'N':payload['N'],
                     'transition_count':len(model.transitions),'top_keys':sorted(payload),
                     'metrics_keys':sorted(payload['metrics']),'metrics_value_types':meta['metrics_value_types'],
                     'transition_keysets':[sorted(t) for t in payload['transitions']],
                     'transition_value_types':meta['transition_value_types'],
                     'canonical_sha256':hashlib.sha256((canon(payload)+'\n').encode()).hexdigest(),
                     'strict_parse_canonical_dump_semantic_identity':True,
                     'constructor_injection_accepted':len(model.transitions)==payload['N'],
                     'kernel_metadata_dispatched':False,'production_loader_used':False,
                     'config_replay_authority':'CONFIG_GENEALOGY_ONLY'})
    out['saved_routes']=rows
    out['searched_loader_names_absent']=all(not out['surfaces'][name] for name in
                                        ('load_profile','from_profile','PROFILE_ALIASES','SAVED_PROFILES'))
else: raise KeyError(case)
projection=dict(out); projection.pop('runtime',None)
out['observation_sha256']=hashlib.sha256(canon(projection).encode()).hexdigest()
sys.stdout.buffer.write(canon(out).encode('utf-8')+b'\n')
'''


def behavior_projection(value: dict[str, Any]) -> dict[str, Any]:
    clone = copy.deepcopy(value)
    clone.pop("runtime", None)
    return clone


def isolated_runs(saved_rows: list[dict[str, Any]]) -> dict[str, Any]:
    root = Path(tempfile.mkdtemp(prefix="p067_step85_"))
    require(ROOT.resolve() not in root.resolve().parents and root.resolve() != ROOT.resolve(),
            "E_TEMP_INSIDE_REPOSITORY")
    runs: list[dict[str, Any]] = []
    cleanup = False
    try:
        source_dir = root / "source"
        saved_dir = root / "saved"
        source_dir.mkdir()
        saved_dir.mkdir()
        (source_dir / "anode_fit_frozen.py").write_bytes(baseline_bytes(SOURCE_PATH))
        probe = root / "probe_step85.py"
        probe.write_text(PROBE_SOURCE, encoding="utf-8", newline="\n")
        for route, path in SAVED_PATHS.items():
            (saved_dir / f"{route}.json").write_bytes(baseline_bytes(path))
        metadata = {row["route"]: {key: row[key] for key in (
            "path", "blob_oid", "git_mode", "raw_sha256", "metrics_value_types",
            "transition_value_types")} for row in saved_rows}
        (saved_dir / "metadata.json").write_bytes(canonical_bytes(metadata))
        before = {str(path.relative_to(root)).replace("\\", "/"): sha256(path.read_bytes())
                  for path in root.rglob("*") if path.is_file()}
        env = {"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8",
               "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"}
        for version, launcher in PYTHON_LAUNCHERS:
            for invocation_ordinal, case in enumerate(CASE_IDS, 1):
                argv = (*launcher, "-B", "-I", "-X", "utf8", str(probe),
                        str(source_dir), case, str(saved_dir))
                cp = subprocess.run(argv, cwd=root, env=env, capture_output=True, shell=False,
                                    check=False, timeout=180)
                stdout = cp.stdout.decode("utf-8", "strict")
                stderr = cp.stderr.decode("utf-8", "strict")
                lines = [line for line in stdout.splitlines() if line]
                require(cp.returncode == 0, f"E_RUNTIME_EXIT:{version}:{case}:{stderr}")
                require(len(lines) == 1 and stderr == "", f"E_RUNTIME_STREAM:{version}:{case}")
                observation = strict_json(lines[0].encode("utf-8"), f"runtime:{version}:{case}")
                runs.append({
                    "python": version, "case_id": case,
                    "invocation_ordinal": invocation_ordinal,
                    "isolated_child_invocation_id": f"PY{version}-C{invocation_ordinal:02d}",
                    "argv": ["py", f"-{version}", "-B", "-I", "-X", "utf8", "<PROBE>",
                             "<SOURCE_DIR>", case, "<SAVED_DIR>"],
                    "cwd": "<DISPOSABLE_ROOT>", "exit_code": cp.returncode,
                    "timed_out": False, "stdout_sha256": sha256(cp.stdout),
                    "stderr_sha256": sha256(cp.stderr), "stderr_empty": stderr == "",
                    "stdout_is_canonical_observation": cp.stdout == canonical_bytes(observation),
                    "observation": observation,
                })
        after = {str(path.relative_to(root)).replace("\\", "/"): sha256(path.read_bytes())
                 for path in root.rglob("*") if path.is_file()}
        require(before == after, "E_TEMP_INPUT_MUTATION")
        require(not any(path.suffix in {".pyc", ".pyo"} or path.name == "__pycache__"
                        for path in root.rglob("*")), "E_TEMP_CACHE_LEAK")
    finally:
        shutil.rmtree(root, ignore_errors=False)
        cleanup = not root.exists()
    require(cleanup, "E_TEMP_CLEANUP")
    by_version = {
        version: {run["case_id"]: behavior_projection(run["observation"]) for run in runs
                  if run["python"] == version}
        for version, _ in PYTHON_LAUNCHERS
    }
    require(by_version["3.12"] == by_version["3.14"], "E_RUNTIME_CROSS_VERSION")
    p = by_version["3.12"]
    require(p["C01_FRESH_BASELINE"]["events"][0]["counts"] ==
            {"graphite": 4, "silicon": 2, "total": 6}, "E_FRESH_DEFAULT")
    require(p["C03_SKEW_REBIND_EXISTING_FUTURE"]["existing_counts_after_rebind"]["total"] == 6
            and p["C03_SKEW_REBIND_EXISTING_FUTURE"]["future_counts_after_rebind"]["total"] == 14,
            "E_REBIND_EXISTING_FUTURE")
    require(p["C04_INPLACE_TRANSITION_ALIAS"]["existing_after_inplace"]["graphite"] == 5,
            "E_INPLACE_ALIAS")
    c05 = p["C05_SI_REBIND_SEED_CACHE"]
    require(c05["legacy_before"]["R_is_legacy"] and c05["si_after_true"]["R_is_si"]
            and c05["legacy_after_false"]["R_is_legacy"]
            and c05["existing_seed_unchanged"]
            and c05["future_seed_differs_from_existing"]
            and c05["imported_scalar_alias_after_true"]["follows_rebind"] is False,
            "E_SI_CONSTANT_REBIND")
    require(p["C06_ORDINARY_IMPORT_CACHE"]["events"][-1]["counts"]["total"] == 14,
            "E_IMPORT_CACHE")
    require(p["C07_EXPLICIT_RELOAD"]["events"][-1]["counts"]["total"] == 6,
            "E_RELOAD_RESET")
    require(p["C08_TWO_SPEC_LOAD_OBJECTS"]["a_after_toggle"]["counts"]["total"] == 14
            and p["C08_TWO_SPEC_LOAD_OBJECTS"]["b_independent_fresh"]["counts"]["total"] == 6,
            "E_SPEC_ISOLATION")
    require(p["C09_NEW_PROCESS_RESET"]["fresh_isolated_process"]["counts"]["total"] == 6
            and p["C09_NEW_PROCESS_RESET"]["paired_prior_case_id"] ==
            "C06_ORDINARY_IMPORT_CACHE", "E_FRESH_ISOLATED_PROCESS")
    require(p["C10_TOGGLE_ORDER_A"]["future_seed"] == p["C11_TOGGLE_ORDER_B"]["future_seed"]
            and p["C10_TOGGLE_ORDER_A"]["future_counts"] ==
            p["C11_TOGGLE_ORDER_B"]["future_counts"] ==
            {"graphite": 7, "silicon": 7, "total": 14}
            and p["C10_TOGGLE_ORDER_A"]["final_constants"] ==
            p["C11_TOGGLE_ORDER_B"]["final_constants"], "E_TOGGLE_ORDER_CROSS")
    process_pairs = []
    for version, _ in PYTHON_LAUNCHERS:
        c06 = next(run for run in runs if run["python"] == version
                   and run["case_id"] == "C06_ORDINARY_IMPORT_CACHE")
        c09 = next(run for run in runs if run["python"] == version
                   and run["case_id"] == "C09_NEW_PROCESS_RESET")
        pid06 = c06["observation"]["runtime"]["pid"]
        pid09 = c09["observation"]["runtime"]["pid"]
        require(type(pid06) is int and type(pid09) is int and pid06 > 0 and pid09 > 0
                and pid06 != pid09, f"E_PROCESS_PAIR_PID:{version}")
        process_pairs.append({
            "python": version, "mutated_case": "C06_ORDINARY_IMPORT_CACHE",
            "mutated_invocation_id": c06["isolated_child_invocation_id"],
            "mutated_pid": pid06,
            "mutated_total": c06["observation"]["events"][-1]["counts"]["total"],
            "fresh_case": "C09_NEW_PROCESS_RESET",
            "fresh_invocation_id": c09["isolated_child_invocation_id"],
            "fresh_pid": pid09,
            "fresh_total": c09["observation"]["fresh_isolated_process"]["counts"]["total"],
            "pid_distinct": True,
        })
    return finalize({
        "artifact": "PHASE_067_SAVED_ROUTE_RUNTIME_ATTESTATION",
        "schema_version": "phase067-step85-runtime-v1",
        "phase": 67, "step": 85, "generated_date": GENERATED_DATE,
        "baseline_commit": BASELINE, "expected_parent": EXPECTED_PARENT,
        "branch": BRANCH, "expected_subject": EXPECTED_SUBJECT,
        "result_first": True, "json_outputs_last": True,
        "runtime_contract": {
            "controller_imported_production": False,
            "child_process_isolation": "-B -I -X utf8",
            "network_used": False, "repository_runtime_cwd": False,
            "persistent_cache_written": False,
            "disposable_cleanup_completed": cleanup,
            "case_sequence": list(CASE_IDS),
            "bounded_no_cartesian_permutations": True,
        },
        "runs": runs, "process_pair_records": process_pairs,
        "cross_runtime_behavior_equal": True,
        "aggregate": {
            "interpreters": 2, "cases_per_interpreter": len(CASE_IDS),
            "processes": len(runs), "exit_zero": sum(run["exit_code"] == 0 for run in runs),
            "stderr_empty": sum(run["stderr_empty"] for run in runs),
            "timeouts": sum(run["timed_out"] for run in runs), "temp_leaks": 0,
        },
        "authority": {
            "isolated_runtime_behavior": True,
            "saved_config_semantic_parse_and_constructor_acceptance": True,
            "production_saved_loader": False, "original_optimizer_state": False,
            "scientific_truth": False, "material_validity": False,
            "canonical_profile": False, "publication_readiness": False,
        },
    })


def normalized_source_policy(path: str, constant: str) -> str:
    raw = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
    pattern = re.compile(rb"(?m)^(" + constant.encode() + rb" = \")[0-9a-f]{64}(\")$")
    replaced, count = pattern.subn(rb"\g<1>" + b"0" * 64 + rb"\g<2>", raw)
    require(count == 1, f"E_SOURCE_POLICY_CONSTANT:{path}")
    return sha256(replaced)


def control_hashes() -> dict[str, str]:
    return {path: sha256((ROOT / path).read_bytes()) for path in CONTROL_PATHS[2:]}


def build_artifacts(runtime_override: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    input_rows = []
    for path in INPUT_PINS:
        loaded[path], binding = load_input(path)
        input_rows.append(binding)
    inventory = loaded[INVENTORY_PATH]
    source = source_static()
    search = full_blob_search(inventory)
    production = production_projection(inventory)
    saved = saved_profiles()
    writer = writer_evidence()
    runtime = isolated_runs(saved) if runtime_override is None else copy.deepcopy(runtime_override)
    carry = loaded[P066_CARRY_PATH]
    obligation = next(row for row in carry["active_obligations"]
                      if row["obligation_id"] == "P066-OBL-0125")
    observation = next(row for row in carry["step76_80_disposition_records"]
                       if row["observation_id"] == "P066-R80-14")
    require(obligation["origin_identity"] == "P066-R80-14"
            and obligation["target_phase"] == 67 and obligation["state"] == "OPEN_CARRY"
            and obligation["canonical_owner"] == "P067-CODE-HISTORY"
            and observation["state"] == "OPEN_CARRY"
            and observation["evidence_identity_disposition"] == "PRESERVE"
            and observation["disposition"] == "WITHHOLD",
            "E_OWNER_ROUTE")
    matrix = finalize({
        "artifact": "PHASE_067_MUTABLE_STATE_DEFAULT_IMPORT_MATRIX",
        "schema_version": "phase067-step85-default-import-v1",
        "phase": 67, "step": 85, "generated_date": GENERATED_DATE,
        "baseline_commit": BASELINE, "expected_parent": EXPECTED_PARENT,
        "branch": BRANCH, "expected_subject": EXPECTED_SUBJECT,
        "gate": GATE, "precommit_status": "PASS_PENDING_PERSISTENCE",
        "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
        "persistence_terminal": PERSISTENCE,
        "result_first": True, "json_outputs_last": True,
        "inputs": input_rows,
        "source_static": source,
        "complete_python_search": search,
        "production_occurrence_projection": production,
        "saved_profiles": saved,
        "writer_evidence": writer,
        "runtime_binding": {
            "path": RUNTIME_PATH, "semantic_sha256": runtime["semantic_sha256"],
            "processes": runtime["aggregate"]["processes"],
            "cross_runtime_behavior_equal": runtime["cross_runtime_behavior_equal"],
        },
        "case_contract": [
            {"case_id": "C01_FRESH_BASELINE", "class": "FRESH_PROCESS_PUBLIC_DEFAULT", "expected": "4_PLUS_2"},
            {"case_id": "C02_EXPLICIT_PROFILE", "class": "EXPLICIT_NONMUTATING", "expected": "7_PLUS_7_GLOBALS_UNCHANGED"},
            {"case_id": "C03_SKEW_REBIND_EXISTING_FUTURE", "class": "MODULE_GLOBAL_REBIND", "expected": "EXISTING_6_FUTURE_14"},
            {"case_id": "C04_INPLACE_TRANSITION_ALIAS", "class": "CALLER_LIST_ALIAS", "expected": "EXISTING_AND_FUTURE_OBSERVE_APPEND"},
            {"case_id": "C05_SI_REBIND_SEED_CACHE", "class": "SI_CONSTANT_R_F_REBIND_AND_SEED_CACHE", "expected": "LEGACY_TO_SI_DYNAMIC_CHANGE_EXISTING_SEED_STABLE_FALSE_RESTORES"},
            {"case_id": "C06_ORDINARY_IMPORT_CACHE", "class": "SYS_MODULE_CACHE", "expected": "MUTATED_STATE_PERSISTS"},
            {"case_id": "C07_EXPLICIT_RELOAD", "class": "EXPLICIT_REEXECUTION", "expected": "MODULE_DEFAULTS_RESET_EXISTING_OBJECT_STATE_AND_SEED_PERSIST"},
            {"case_id": "C08_TWO_SPEC_LOAD_OBJECTS", "class": "DISTINCT_MODULE_OBJECTS", "expected": "STATE_ISOLATED"},
            {"case_id": "C09_NEW_PROCESS_RESET", "class": "PAIRED_FRESH_ISOLATED_PROCESS", "expected": "C06_MUTATED_14_PID_DISTINCT_C09_FRESH_6"},
            {"case_id": "C10_TOGGLE_ORDER_A", "class": "BOUNDED_TWO_TOGGLE_ORDER", "expected": "SI_THEN_SKEW_FINAL_SI_7_PLUS_7"},
            {"case_id": "C11_TOGGLE_ORDER_B", "class": "BOUNDED_TWO_TOGGLE_ORDER", "expected": "SKEW_THEN_SI_FINAL_SI_7_PLUS_7"},
            {"case_id": "C12_ALIAS_EXPORT_GNF", "class": "CLOSED_VOCABULARY_SOURCE_SEARCH", "expected": "EXACT_SIX_SURFACES_GROUND_NOT_FOUND"},
            {"case_id": "C13_SAVED_ROUTE_GNF", "class": "STRICT_CONFIG_PARSE_DUMP_AND_DIRECT_CONSTRUCTOR_INJECTION", "expected": "8_14_14_SEARCHED_NAMES_ABSENT_NO_LOADER_USED_NO_KERNEL_DISPATCH"},
        ],
        "default_adjudication": {
            "fresh_executable_default": "GRAPHITE_STAGING_LIT_4_PLUS_SIC_LIT_2",
            "header_docstring_7_gallery_default_claim": "STALE_CONFLICT_NOT_EXECUTABLE_AUTHORITY",
            "use_legacy_4transition": "GROUND_NOT_FOUND",
            "use_skew7_default": "PRESENT_MUTABLE_GLOBAL_API",
            "from_wt_q_gr_default_bound_at_definition": 372.0,
            "test_mutated_state_is_fresh_public_default": False,
            "ordinary_reimport_resets_module_state": False,
            "explicit_reload_resets_module_state": True,
            "serialization_roundtrip_is_public_loader": False,
        },
        "owner_resolution": {
            "obligation_id": "P066-OBL-0125", "origin_identity": "P066-R80-14",
            "origin_record_sha256": observation["origin_record_sha256"],
            "prior_disposition": observation["evidence_identity_disposition"],
            "prior_state": observation["state"],
            "prior_serialized_disposition": observation["disposition"],
            "obligation_state": obligation["state"], "target_phase": obligation["target_phase"],
            "resolution": "BOUNDED_CONFIG_PARSE_CONSTRUCTOR_ACCEPTANCE_SEARCHED_EXACT_NAMES_GROUND_NOT_FOUND",
            "resolution_state": "BOUND_NOT_RESOLVED_OR_DISPATCHED",
            "owner": obligation["canonical_owner"],
            "external_authority_promoted": (obligation["external_authority_promoted"]
                                              or observation["external_authority_promoted"]),
        },
        "control_hashes": control_hashes(),
        "source_policy": {
            "builder_neutral_sha256": normalized_source_policy(
                BUILDER_PATH, "BUILDER_SOURCE_POLICY_SHA256_LF"),
            "validator_neutral_sha256": normalized_source_policy(
                VALIDATOR_PATH, "VALIDATOR_SOURCE_POLICY_SHA256_LF"),
        },
        "validation": {
            "step82_129_84_bound": True, "step83_and_step84_pinned": True,
            "production_source_ast": "PASS",
            "complete_python_loader_search_84_of_84": "PASS",
            "fresh_before_mutation": "PASS", "bounded_permutations": "PASS",
            "saved_schema_parse_dump_and_constructor_acceptance": "PASS",
            "owner_direct_binding": "PASS",
            "authority_promotions": 0,
            "required_absent_surface": "SEARCHED_EXACT_NAMES_GROUND_NOT_FOUND",
        },
        "authority": {
            "source_static_defaults": True, "isolated_runtime_behavior": True,
            "config_genealogy": True, "general_test_behavior": False,
            "science": False, "material": False, "canonical_profile": False,
            "publication": False,
        },
    })
    return matrix, runtime


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    require(not path.exists(), f"E_OUTPUT_EXISTS:{path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temp: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("wb", dir=path.parent, prefix=f".{path.name}.",
                                         suffix=".tmp", delete=False) as handle:
            temp = Path(handle.name)
            handle.write(canonical_bytes(value))
        require(temp.resolve().parent == path.parent.resolve(), "E_OUTPUT_TEMP_ESCAPE")
        os.replace(temp, path)
    finally:
        if temp is not None and temp.exists():
            temp.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--collect", action="store_true")
    args = parser.parse_args()
    require(args.preview != args.collect, "E_MODE")
    matrix_a, runtime_a = build_artifacts()
    matrix_b, runtime_b = build_artifacts(runtime_override=runtime_a)
    require(canonical_bytes(matrix_a) == canonical_bytes(matrix_b)
            and canonical_bytes(runtime_a) == canonical_bytes(runtime_b), "E_DETERMINISM")
    if args.collect:
        atomic_write(ROOT / MATRIX_PATH, matrix_a)
        atomic_write(ROOT / RUNTIME_PATH, runtime_a)
    print("PASS_P067_STEP85_BUILD "
          f"mode={'collect' if args.collect else 'preview'} cases={len(CASE_IDS)} "
          f"processes={runtime_a['aggregate']['processes']} "
          f"search={matrix_a['complete_python_search']['searched_unique_python_blobs']}/84 "
          f"matrix_semantic={matrix_a['semantic_sha256']} "
          f"runtime_semantic={runtime_a['semantic_sha256']} determinism=2/2")


if __name__ == "__main__":
    try:
        main()
    except BuildError as exc:
        raise SystemExit(str(exc))
