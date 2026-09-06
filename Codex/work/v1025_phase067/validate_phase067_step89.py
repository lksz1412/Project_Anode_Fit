#!/usr/bin/env python3
"""Validate Phase 067 Step 89 fitting-evidence authority separation."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "7b81814017ffd4207cc2a13fabbbe68281075b00"
SUPPLEMENTAL_COMMIT = "e3e1a634f34b711aa4803fd190fe9120f1755f13"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "f0c381bd6dc315ac75cbffa93dd86ce83a37949b"
SUBJECT = "audit(phase067): separate fitting evidence authority"
GATE = "PASS_P067_STEP89_FITTING_AUTHORITY"
PERSISTENCE = "PASS_P067_STEP89_PERSISTENCE"

BUILDER = "Codex/work/v1025_phase067/build_phase067_step89.py"
VALIDATOR = "Codex/work/v1025_phase067/validate_phase067_step89.py"
MATRIX = "Codex/results/PHASE_067_FITTING_EVIDENCE_MATRIX.json"
RUNTIME = "Codex/results/PHASE_067_FITTING_RUNTIME_ATTESTATION.json"
RESULT = "Codex/results/PHASE_067_STEP_089_FITTING_AUTHORITY_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
CANONICAL_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
FINAL_PATHS = (BUILDER, VALIDATOR, MATRIX, RUNTIME, RESULT,
               PARENT_LEDGER, CANONICAL_LEDGER, HANDOVER)
FINAL_STATUS = {path: ("A" if index < 5 else "M")
                for index, path in enumerate(FINAL_PATHS)}

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
SUPPLEMENTAL_EXPECTED = {
    SUPPLEMENTAL_PATHS[0]: (286471, "4b06fefa1bb81de842386c95fbba5bdd431602d4",
                            "e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6"),
    SUPPLEMENTAL_PATHS[1]: (1581, "876e4a675812557dcacbac416ed74ff3c2ad858d",
                            "4fa8bc00535d31fe90cd066af895285341c69938c2e259eaa7609950de2a6649"),
    SUPPLEMENTAL_PATHS[2]: (10662, "d14f98564d1f4723bfcd32c921a3dc9c69149ac9",
                            "70c50cadfe4c8b170612e275fccfbf7714cef42d9889588cf8316629f9db16ab"),
    SUPPLEMENTAL_PATHS[3]: (14621, "c064a11241c07195a11ad12878fa7a3914c1f15b",
                            "90ee96c2717d4b12bc94647da58b715c3974c2336bf03907b77c693adebb0c0c"),
    SUPPLEMENTAL_PATHS[4]: (7539, "c4fc6b997bad2a15617f1c7255708bf736b9e37a",
                            "d3441b15b276ac87c4925c77146a24cdb2e16f1184057f9a17d9d6952daebf2c"),
    SUPPLEMENTAL_PATHS[5]: (12145, "2a826e4b27ddcde3584daaf1e6a8c557011c773a",
                            "3ee4e41b8e6881529e36f4fddeb9d0130605f55955f8ef268ee578f3dd54a574"),
    SUPPLEMENTAL_PATHS[6]: (17754, "c0a475352abe2f2df145442d8ed722d132ab5d03",
                            "edcafd90b91b6515ca12dca3743678055bc021a52cff3a86a2355467afe8dedc"),
    SUPPLEMENTAL_PATHS[7]: (1709, "f40c5d3b4019378c02453189717c19a27cbfac88",
                            "32cddfd8d148407090e117c8e4fdc386c15ac36b8612254fba75c658ab5b0206"),
    SUPPLEMENTAL_PATHS[8]: (1321, "7292f367c4bb03819efec316f01db0df64427d5e",
                            "89befa143dca8d4051ba4627f224608ff3e6fb0500a06fbca2d77409c3d7788f"),
    SUPPLEMENTAL_PATHS[9]: (1669, "c327a56b22a0f2c2c2910b90283088fb7f2c8f13",
                            "c4ba2e46d515eddbbdc4c5d8f3310a9ab90fc8b777e0def0177a22ad127f125e"),
}
SUPPORT_EXPECTED = {
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
AUTHORITY_KEYS = (
    "canonical_release", "external", "held_out", "identifiability", "material",
    "phase_mechanism", "publication", "protocol", "original_optimizer_state",
)
MAX_JSON_BYTES = 8_000_000
MAX_JSON_DEPTH = 64
MAX_JSON_NODES = 600_000
BUILDER_SOURCE_SHA256_LF = "4ddf3cc52811b8a106be2ea9744b4e2fd13a54ede977c1f622e3a59c21034595"
VALIDATOR_NEUTRAL_SHA256_LF = "7b7719e46770232c34ef42bcb7902483feabc6f26d44cf7c373cae443ecc6be0"


class ValidationError(RuntimeError):
    pass


def require(ok: bool, code: str, detail: str = "") -> None:
    if not ok:
        raise ValidationError(code + ((":" + detail) if detail else ""))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def semantic(value: dict[str, Any]) -> str:
    copy_value = dict(value)
    copy_value.pop("semantic_sha256", None)
    return sha(canonical(copy_value))


def typed_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            typed_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(
            typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def strict_load(raw: bytes, label: str, *, generated: bool) -> tuple[dict[str, Any], int, int]:
    require(len(raw) <= MAX_JSON_BYTES, label + "_BYTES")
    nesting = 0
    in_string = False
    escaped = False
    max_lexical_depth = 0
    for byte in raw:
        if in_string:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                in_string = False
        elif byte == 34:
            in_string = True
        elif byte in (91, 123):
            nesting += 1
            max_lexical_depth = max(max_lexical_depth, nesting)
            require(nesting <= MAX_JSON_DEPTH, label + "_DEPTH")
        elif byte in (93, 125):
            nesting -= 1
            require(nesting >= 0, label + "_LEXICAL")
    require(nesting == 0 and not in_string and not escaped, label + "_LEXICAL")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, label + "_DUPLICATE")
            result[key] = value
        return result

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                           parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError,
            RecursionError, MemoryError) as exc:
        raise ValidationError(label + "_PARSE") from exc
    require(isinstance(value, dict), label + "_ROOT")
    nodes = 0
    depth = 0
    stack: list[tuple[Any, int]] = [(value, 0)]
    while stack:
        item, level = stack.pop()
        nodes += 1
        require(nodes <= MAX_JSON_NODES, label + "_NODES")
        require(level <= MAX_JSON_DEPTH, label + "_DEPTH")
        depth = max(depth, level)
        if isinstance(item, dict):
            for key, child in item.items():
                require(isinstance(key, str), label + "_TREE")
                stack.append((key, level + 1))
                stack.append((child, level + 1))
        elif isinstance(item, list):
            for child in item:
                stack.append((child, level + 1))
        elif isinstance(item, float):
            require(math.isfinite(item), label + "_NONFINITE")
        else:
            require(item is None or isinstance(item, (str, int, bool)), label + "_TREE")
    if generated:
        require(raw == canonical(value), label + "_NONCANONICAL")
        require(value.get("semantic_sha256") == semantic(value), label + "_SEMANTIC")
    return value, nodes, max(depth, max_lexical_depth)


def is_oid(value: str) -> bool:
    return re.fullmatch(r"[0-9a-f]{40}", value) is not None


def git_argv_allowed(args: tuple[str, ...]) -> bool:
    if not args or any(not isinstance(item, str) or "\0" in item or "\n" in item or "\r" in item
                       for item in args):
        return False
    fixed = {
        ("rev-parse", "HEAD"),
        ("symbolic-ref", "--quiet", "--short", "HEAD"),
        ("rev-parse", "refs/remotes/origin/main"),
        ("rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"),
        ("status", "--porcelain=v1", "--untracked-files=all"),
        ("diff", "--cached", "--name-only"),
        ("diff", "--cached", "--name-status", "--no-renames", EXPECTED_PARENT, "--"),
        ("diff", "--name-only"),
        ("rev-parse", "@{u}"),
        ("rev-parse", f"refs/remotes/origin/{BRANCH}"),
        ("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"),
        ("ls-files", "--stage", "--", *FINAL_PATHS),
    }
    if args in fixed:
        return True
    if len(args) == 2 and args[0] == "show" and ":" in args[1]:
        ref, path = args[1].split(":", 1)
        return (ref == EXPECTED_PARENT and path in PARENT_INPUTS) or \
            (ref == SUPPLEMENTAL_COMMIT and path in SUPPLEMENTAL_PATHS)
    if len(args) == 4 and args[0] == "ls-tree" and args[2] == "--":
        return args[1] in {SUPPLEMENTAL_COMMIT, BASELINE} and args[3] in SUPPLEMENTAL_PATHS
    if args[:3] == ("diff", "--name-only", PROTECTED_TIP) and len(args) == 6:
        return (args[3] == EXPECTED_PARENT or is_oid(args[3])) and args[4:] == ("--", "Claude")
    if len(args) == 4 and args[:2] == ("show", "--no-patch"):
        return args[2] in {"--format=%P", "--format=%s"} and is_oid(args[3])
    if len(args) == 7 and args[:5] == (
        "diff-tree", "--no-commit-id", "--name-status", "-r", "--no-renames"
    ):
        return is_oid(args[5]) and args[6] == "--"
    if len(args) == 3 + len(FINAL_PATHS) and args[0] == "ls-tree" and args[2] == "--":
        return is_oid(args[1]) and args[3:] == FINAL_PATHS
    return False


def git_bytes(args: list[str], code: str = "E_GIT") -> bytes:
    require(git_argv_allowed(tuple(args)), "E_GIT_ARGV", repr(args))
    completed = subprocess.run(["git", *args], cwd=ROOT, check=False,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(completed.returncode == 0, code, completed.stderr.decode("utf-8", "replace")[:300])
    return completed.stdout


def git_text(args: list[str], code: str = "E_GIT") -> str:
    return git_bytes(args, code).decode("utf-8").strip()


def parent_json(path: str) -> dict[str, Any]:
    require(path in PARENT_INPUTS, "E_PARENT_PATH")
    raw = git_bytes(["show", f"{EXPECTED_PARENT}:{path}"])
    value, _, _ = strict_load(raw,
                              "E_PARENT_JSON", generated=False)
    expected_raw, expected_declared = PARENT_EXPECTED[path]
    require(sha(raw) == expected_raw, "E_PARENT_RAW_PIN", path)
    require(value.get("semantic_sha256") == expected_declared,
            "E_PARENT_DECLARED_SEMANTIC_PIN", path)
    return value


def supplemental_identity(path: str) -> dict[str, Any]:
    require(path in SUPPLEMENTAL_PATHS, "E_SUPPLEMENTAL_PATH")
    tree = git_text(["ls-tree", SUPPLEMENTAL_COMMIT, "--", path], "E_SUPPLEMENTAL_TREE")
    match = re.fullmatch(r"(100644) blob ([0-9a-f]{40})\t(.+)", tree)
    require(match is not None and match.group(3) == path, "E_SUPPLEMENTAL_TREE_ROW", path)
    baseline_tree = git_text(["ls-tree", BASELINE, "--", path], "E_BASELINE_TREE")
    baseline_match = re.fullmatch(r"(100644) blob ([0-9a-f]{40})\t(.+)", baseline_tree)
    require(baseline_match is not None and baseline_match.group(3) == path,
            "E_BASELINE_TREE_ROW", path)
    raw = git_bytes(["show", f"{SUPPLEMENTAL_COMMIT}:{path}"], "E_SUPPLEMENTAL_READ")
    extent, oid, raw_sha = SUPPLEMENTAL_EXPECTED[path]
    require((len(raw), match.group(2), sha(raw)) == (extent, oid, raw_sha),
            "E_SUPPLEMENTAL_PIN", path)
    require(baseline_match.group(2) == match.group(2), "E_BASELINE_SUPPLEMENTAL_DRIFT", path)
    return {
        "baseline_commit": BASELINE,
        "baseline_equal": True,
        "baseline_git_blob_oid": baseline_match.group(2),
        "bytes": len(raw),
        "containing_commit": SUPPLEMENTAL_COMMIT,
        "git_blob_oid": match.group(2),
        "mode": match.group(1),
        "path": path,
        "raw_sha256": sha(raw),
    }


def builder_preview() -> dict[str, Any]:
    completed = subprocess.run([sys.executable, "-B", str(ROOT / BUILDER), "--preview"],
                               cwd=ROOT, check=False, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    require(completed.returncode == 0, "E_BUILDER_PREVIEW",
            completed.stderr.decode("utf-8", "replace")[:500])
    value, _, _ = strict_load(completed.stdout, "E_PREVIEW", generated=False)
    require(set(value) == {"matrix", "runtime"}, "E_PREVIEW_SCHEMA")
    return value


def load_outputs() -> tuple[dict[str, Any], dict[str, Any], int, int]:
    require((ROOT / MATRIX).is_file(), "E_MATRIX_MISSING")
    require((ROOT / RUNTIME).is_file(), "E_RUNTIME_MISSING")
    matrix, mn, md = strict_load((ROOT / MATRIX).read_bytes(), "E_MATRIX", generated=True)
    runtime, rn, rd = strict_load((ROOT / RUNTIME).read_bytes(), "E_RUNTIME", generated=True)
    return matrix, runtime, mn + rn, max(md, rd)


def require_metadata(value: dict[str, Any], artifact: str) -> None:
    require(value.get("artifact") == artifact, "E_ARTIFACT", artifact)
    require(value.get("schema_version") == "P067-S89-1", "E_SCHEMA", artifact)
    require(value.get("phase") == 67 and value.get("step") == 89, "E_PHASE_STEP", artifact)
    require(value.get("baseline_commit") == BASELINE, "E_BASELINE", artifact)
    require(value.get("expected_parent") == EXPECTED_PARENT, "E_PARENT", artifact)
    require(value.get("supplemental_commit") == SUPPLEMENTAL_COMMIT,
            "E_SUPPLEMENTAL_COMMIT", artifact)
    require(value.get("expected_subject") == SUBJECT, "E_SUBJECT", artifact)
    require(value.get("gate") == GATE, "E_GATE", artifact)
    require(value.get("persistence_terminal") == PERSISTENCE, "E_TERMINAL", artifact)
    require(value.get("containing_commit") == "PENDING_AT_PRECOMMIT_BY_DESIGN",
            "E_CONTAINING_COMMIT", artifact)


def validate_core(matrix: dict[str, Any], runtime: dict[str, Any]) -> None:
    require_metadata(matrix, "PHASE_067_FITTING_EVIDENCE_MATRIX")
    require_metadata(runtime, "PHASE_067_FITTING_RUNTIME_ATTESTATION")

    identities = matrix.get("supplemental_inputs")
    require(isinstance(identities, list) and len(identities) == 10,
            "E_SUPPLEMENTAL_COUNT")
    require([row.get("path") for row in identities] == list(SUPPLEMENTAL_PATHS),
            "E_SUPPLEMENTAL_ORDER")
    require(len({row.get("path") for row in identities}) == 10, "E_SUPPLEMENTAL_DUPLICATE")
    for row, path in zip(identities, SUPPLEMENTAL_PATHS):
        expected = supplemental_identity(path)
        for key, observed in expected.items():
            require(row.get(key) == observed, "E_SUPPLEMENTAL_IDENTITY", path + ":" + key)
        require(isinstance(row.get("bounded_role"), str) and row["bounded_role"],
                "E_SUPPLEMENTAL_ROLE", path)
        require(row.get("supports_evidence_ids") == SUPPORT_EXPECTED[path],
                "E_SUPPLEMENTAL_LINK", path)

    provenance = parent_json(FIT_PROVENANCE)
    reproduction = parent_json(FIT_REPRODUCTION)
    optimizer = parent_json(OPTIMIZER_STATE)
    empirical = parent_json(EMPIRICAL_AUTHORITY)
    carry = parent_json(CARRY_FORWARD)
    phase065 = parent_json(PHASE065_AUTHORITY)

    parent_rows = matrix.get("phase066_inputs")
    require(isinstance(parent_rows, list) and
            [row.get("path") for row in parent_rows] == list(PARENT_INPUTS),
            "E_PARENT_INPUT_ROWS")
    for row, path in zip(parent_rows, PARENT_INPUTS):
        expected_raw, expected_declared = PARENT_EXPECTED[path]
        require(row == {
            "declared_semantic_sha256": expected_declared,
            "path": path,
            "raw_sha256": expected_raw,
            "semantic_seal_status":
                "DECLARED_BY_PARENT_SCHEMA_RAW_BYTES_PINNED_NOT_RECOMPUTED_STEP89",
            "source_commit": EXPECTED_PARENT,
        }, "E_PARENT_INPUT_IDENTITY", path)

    contract = matrix.get("direct14_contract")
    require(isinstance(contract, dict), "E_DIRECT14_CONTRACT")
    require(typed_equal(contract.get("raw_input"), provenance.get("raw_input")),
            "E_RAW_INPUT")
    require(typed_equal(contract.get("preprocessing"), provenance.get("preprocessing")),
            "E_PREPROCESSING")
    require(typed_equal(contract.get("processed_input"), provenance.get("processed_input")),
            "E_PROCESSED_INPUT")
    require(typed_equal(contract.get("optimizer"), provenance.get("optimizer_contract")),
            "E_OPTIMIZER_CONTRACT")
    raw_input = contract["raw_input"]
    require(raw_input.get("columns") == ["V_vs_Li", "Q_mAh"], "E_COLUMNS")
    require(raw_input.get("capacity_basis") == "absolute_mAh_not_mass_normalized",
            "E_CAPACITY_BASIS")
    require(raw_input.get("specimen_protocol_status") ==
            "SOURCE_DECLARED_BUT_EXACT_BINDING_GROUND_NOT_FOUND", "E_SPECIMEN_PROTOCOL")
    require(len(raw_input.get("ground_not_found", [])) == 3, "E_RAW_GNF")
    opt = contract["optimizer"]
    require(opt.get("parameter_order") == ["U[14]", "w[14]", "Q[14]", "alpha[14]", "bg"],
            "E_PARAMETER_ORDER")
    require(opt.get("free_mask") ==
            "implicit_all_57_parameters_free; no persisted explicit mask", "E_FREE_MASK")
    require(opt.get("objective") == "source_explicit_unweighted_residual=model(V)-D",
            "E_OBJECTIVE")
    require(opt.get("rng_seed") == 23 and opt.get("solver") ==
            "scipy.optimize.least_squares", "E_SOLVER_SEED")
    require(opt.get("source_explicit_options") == ["bounds", "max_nfev"],
            "E_SOLVER_OPTIONS")
    require(opt.get("historical_resolved_defaults_and_scipy_version") == "GROUND_NOT_FOUND",
            "E_HISTORICAL_TOLERANCE")

    records = matrix.get("evidence_records")
    require(isinstance(records, list) and len(records) == 12, "E_EVIDENCE_RECORDS")
    ids = [row.get("id") for row in records]
    require(all(isinstance(item, str) and item for item in ids) and len(set(ids)) == len(ids),
            "E_EVIDENCE_IDS")
    counts = {label: 0 for label in CLASS_ENUM}
    for row in records:
        classification = row.get("evidence_class")
        require(classification in CLASS_ENUM, "E_CLASS_ENUM", str(classification))
        counts[classification] += 1
        authority = row.get("authority")
        require(isinstance(authority, dict) and set(authority) == set(AUTHORITY_KEYS),
                "E_AUTHORITY_SCHEMA", row["id"])
        require(all(authority[key] is False for key in AUTHORITY_KEYS),
                "E_AUTHORITY_PROMOTION", row["id"])
        require(row.get("in_sample_status") in {
            "INPUT_ONLY", "BOUNDED_NUMERICAL_REPLAY_NONCONVERGED",
            "SOURCE_STATIC_ONLY", "SOURCE_DECLARATION_ONLY",
            "REPORTED_SAVED_METRICS_ONLY",
        }, "E_IN_SAMPLE_STATUS", row["id"])
    require(counts == {"REAL_DATA": 1, "RECONSTRUCTED": 6, "SYNTHETIC": 0,
                       "DEMO": 0, "SAVED_ONLY": 5}, "E_CLASS_COVERAGE")
    summary = matrix.get("exclusive_classification")
    require(isinstance(summary, dict) and summary.get("enum") == list(CLASS_ENUM),
            "E_CLASS_SUMMARY")
    require(summary.get("counts") == counts and summary.get("exclusive") is True,
            "E_CLASS_COUNTS")
    require(summary.get("zero_class_interpretation") ==
            "REVIEWED_FITTING_INVENTORY_ABSENCE_NOT_PROJECT_WIDE_ABSENCE",
            "E_ZERO_CLASS_INTERPRETATION")

    all_record_ids = set(ids)
    for row in identities:
        require(set(row["supports_evidence_ids"]) <= all_record_ids,
                "E_SUPPLEMENTAL_ORPHAN", row["path"])

    saved = matrix.get("saved_profile_records")
    require(isinstance(saved, list) and [row.get("profile") for row in saved] ==
            ["A_regsol", "B_gallery", "C_skew"], "E_SAVED_PROFILES")
    summary_raw = git_bytes(["show", f"{SUPPLEMENTAL_COMMIT}:{SUPPLEMENTAL_PATHS[6]}"])
    summary_json, _, _ = strict_load(summary_raw, "E_SAVED_SUMMARY", generated=False)
    param_paths = SUPPLEMENTAL_PATHS[7:]
    for row, profile, path in zip(saved, ("A_regsol", "B_gallery", "C_skew"), param_paths):
        params, _, _ = strict_load(git_bytes(["show", f"{SUPPLEMENTAL_COMMIT}:{path}"]),
                                   "E_SAVED_PARAMS", generated=False)
        blend = summary_json[profile]["blend"]
        require(set(row) == {
            "authority", "flat_parameter_vector", "flat_vector_source_rounding", "kernel",
            "material", "metrics", "profile", "source_path", "summary_metrics_match",
            "transition_order", "transition_source_rounding", "transitions",
        }, "E_SAVED_SCHEMA", profile)
        require(row.get("source_path") == path, "E_SAVED_PATH", profile)
        require(row.get("metrics") == params.get("metrics"), "E_SAVED_METRICS", profile)
        require(row.get("transitions") == params.get("transitions"),
                "E_SAVED_TRANSITIONS", profile)
        require(row.get("flat_parameter_vector") == blend.get("params") and
                row.get("flat_vector_source_rounding") == "8_DECIMAL_PLACES",
                "E_SAVED_FLAT_VECTOR", profile)
        require(row.get("kernel") == params.get("kernel") and
                row.get("material") == params.get("material"),
                "E_SAVED_IDENTITY", profile)
        require(row.get("transition_order") == "SORTED_BY_U_NOT_OPTIMIZER_FLAT_ORDER" and
                row.get("transition_source_rounding") ==
                "6_DECIMAL_PLACES_EXCEPT_DERIVED_DISPLAY_FIELDS",
                "E_SAVED_ROUNDING", profile)
        require(row.get("summary_metrics_match") is True and
                params["metrics"]["R2"] == blend["R2"] and
                params["metrics"]["BIC"] == blend["BIC"], "E_SAVED_SUMMARY_MATCH", profile)
        require(row.get("authority") == "SAVED_ONLY_NOT_ORIGINAL_OPTIMIZER_STATE",
                "E_SAVED_AUTHORITY", profile)

    comparison = matrix.get("comparison_source_contracts")
    require(isinstance(comparison, list) and len(comparison) == 3,
            "E_COMPARISON_CONTRACTS")
    require([row.get("profile") for row in comparison] ==
            ["A_regsol", "B_gallery", "C_skew"], "E_COMPARISON_ORDER")
    require([row.get("parameter_order") for row in comparison] == [
        ["U[N]", "Omega[N]", "Q[N]", "w[N]", "bg"],
        ["U[N]", "w[N]", "Q[N]", "bg"],
        ["U[N]", "w[N]", "Q[N]", "alpha[N]", "bg"],
    ], "E_COMPARISON_PARAMETER_ORDER")
    comparison_specs = [
        ("regsol", 8,
         {"Omega": "2.4*R*T", "Q": "area/N", "U": "one_of_three_source_seed_sets",
          "bg": "D_min", "w": 0.004},
         {"Omega": [0.0, "8*R*T"], "Q": [1e-9, "10*area"],
          "U": ["V_min", "V_max"], "bg": ["min(0,D_min)", "max(D_max,1e-9)"],
          "w": [0.0001, 0.12]}),
        ("logistic", 14,
         {"Q": "area/N", "U": "one_of_three_source_seed_sets", "bg": "D_min",
          "w": 0.004},
         {"Q": [1e-9, "10*area"], "U": ["V_min", "V_max"],
          "bg": ["min(0,D_min)", "max(D_max,1e-9)"], "w": [0.0001, 0.12]}),
        ("skew-logistic", 14,
         {"Q": "area/N", "U": "one_of_three_source_seed_sets", "alpha": 1.0,
          "bg": "D_min", "w": 0.004},
         {"Q": [1e-9, "10*area"], "U": ["V_min", "V_max"],
          "alpha": [0.15, 8.0], "bg": ["min(0,D_min)", "max(D_max,1e-9)"],
          "w": [0.0001, 0.12]}),
    ]
    comparison_keys = {
        "bounds", "components_for_blend", "free_mask", "initialization_recipe", "kernel",
        "objective", "original_full_optimizer_state", "original_initial_vector",
        "parameter_order", "profile", "resolved_tolerances", "restarts_per_strategy",
        "restart_perturbation_multiplier_uniform", "rng_algorithm", "rng_seed",
        "seed_and_bounds_dependency", "seed_strategies", "selection_rule", "solver",
        "source_explicit_options", "source_max_nfev", "source_path",
    }
    for row, (kernel, components, initial, bounds) in zip(comparison, comparison_specs):
        require(set(row) == comparison_keys, "E_COMPARISON_SCHEMA")
        require(row.get("kernel") == kernel and row.get("components_for_blend") == components,
                "E_COMPARISON_KERNEL_COMPONENTS")
        require(row.get("initialization_recipe") == initial and row.get("bounds") == bounds,
                "E_COMPARISON_INIT_BOUNDS")
        require(row.get("free_mask") == "implicit_all_parameters_free_with_box_bounds" and
                row.get("rng_algorithm") == "numpy.random.default_rng",
                "E_COMPARISON_FREE_RNG")
        require(row.get("objective") == "unweighted_residual=model(V)-D",
                "E_COMPARISON_OBJECTIVE")
        require(row.get("rng_seed") == 23 and row.get("restarts_per_strategy") == 4
                and row.get("seed_strategies") == 3, "E_COMPARISON_SEEDS")
        require(row.get("restart_perturbation_multiplier_uniform") == [0.75, 1.25]
                and row.get("seed_and_bounds_dependency") == {
                    "bounds_initialization_callable":
                    "test_gallery_vs_regsol.bounds_and_seed",
                    "path": SUPPLEMENTAL_PATHS[5],
                    "seed_strategy_callable": "test_gallery_vs_regsol.seed_sets",
                }, "E_COMPARISON_DEPENDENCY")
        require(row.get("solver") == "scipy.optimize.least_squares"
                and row.get("source_explicit_options") == ["bounds", "max_nfev"],
                "E_COMPARISON_SOLVER")
        require(row.get("resolved_tolerances") == "GROUND_NOT_FOUND",
                "E_COMPARISON_TOLERANCE")
        require(row.get("original_initial_vector") == "GROUND_NOT_FOUND"
                and row.get("original_full_optimizer_state") == "GROUND_NOT_FOUND",
                "E_COMPARISON_ORIGINAL_STATE")
        require(row.get("source_max_nfev") == 6000 and
                row.get("selection_rule") == "minimum_cost_even_if_returned_success_is_false" and
                row.get("source_path") == SUPPLEMENTAL_PATHS[2],
                "E_COMPARISON_SOURCE_CONTRACT")

    routes = matrix.get("supplemental_route_contracts")
    require(isinstance(routes, list) and len(routes) == 2,
            "E_SUPPLEMENTAL_ROUTE_CONTRACTS")
    require([row.get("source_path") for row in routes] ==
            [SUPPLEMENTAL_PATHS[3], SUPPLEMENTAL_PATHS[5]],
            "E_SUPPLEMENTAL_ROUTE_PATHS")
    common_route_keys = {
        "bounds_recipe", "executed_in_step89", "free_mask", "initialization_recipe",
        "kernel_parameter_orders", "objective", "perturbation_multiplier_uniform",
        "resolved_solver_method_loss_jacobian_tolerances", "rng_seed", "route",
        "selection_rule", "solver", "source_explicit_options", "source_max_nfev",
        "source_path",
    }
    require(set(routes[0]) == common_route_keys |
            {"material_run_configurations", "restarts", "seed_strategy", "width_bounds_V"},
            "E_SKEW_ROUTE_SCHEMA")
    require(set(routes[1]) == common_route_keys |
            {"material_run_configuration", "restarts_per_strategy", "seed_strategies",
             "sweep_components"},
            "E_GALLERY_ROUTE_SCHEMA")
    orders = {
        "logistic": ["U[N]", "w[N]", "Q[N]", "bg"],
        "regsol": ["U[N]", "Omega[N]", "Q[N]", "w[N]", "bg"],
        "skew-logistic": ["U[N]", "w[N]", "Q[N]", "alpha[N]", "bg"],
        "skew-regsol": ["U[N]", "Omega[N]", "Q[N]", "w[N]", "alpha[N]", "bg"],
    }
    for row in routes:
        require(row.get("executed_in_step89") is False and
                row.get("free_mask") == "implicit_all_parameters_free_with_box_bounds" and
                row.get("kernel_parameter_orders") == orders,
                "E_SUPPLEMENTAL_ROUTE_SCOPE")
        require(row.get("objective") == "unweighted_residual=model(V)-D" and
                row.get("solver") == "scipy.optimize.least_squares" and
                row.get("source_explicit_options") == ["bounds", "max_nfev"],
                "E_SUPPLEMENTAL_ROUTE_SOLVER")
        require(row.get("resolved_solver_method_loss_jacobian_tolerances") ==
                "GROUND_NOT_FOUND" and row.get("selection_rule") ==
                "minimum_cost_even_if_returned_success_is_false",
                "E_SUPPLEMENTAL_ROUTE_CEILING")
    require(routes[0].get("route") == "FOUR_KERNEL_MATERIAL_RUNNER" and
            routes[0].get("rng_seed") == 7 and routes[0].get("restarts") == 4 and
            routes[0].get("source_max_nfev") == 4000 and
            routes[0].get("perturbation_multiplier_uniform") == [0.7, 1.3] and
            routes[0].get("seed_strategy") ==
            "one_configured_transition_list_per_material",
            "E_SKEW_ROUTE_EXECUTION_CONTRACT")
    require(routes[0].get("bounds_recipe") == {
        "Omega": [0.0, "8*R*T"], "Q": [1e-8, "10*area"],
        "U": ["max(V_min,U_seed-uband)", "min(V_max,U_seed+uband)"],
        "alpha": [0.15, 8.0], "bg": [0.0, "max(D_max,1e-9)"],
        "w": [0.0001, 0.10],
    }, "E_SKEW_ROUTE_BOUNDS")
    require(routes[0].get("initialization_recipe") == {
        "Omega": "2.4*R*T", "Q": "area/N", "U": "configured_material_transition_list",
        "alpha": 1.0, "bg": "D_min", "w": 0.004,
    }, "E_SKEW_ROUTE_INITIALIZATION")
    require(routes[0].get("width_bounds_V") == [0.0001, 0.10] and
            routes[0].get("material_run_configurations") == [
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
                    "initial_transition_U_V":
                    [0.096, 0.120, 0.135, 0.224, 0.330, 0.422, 0.470],
                    "material": "blend", "u_band_V": 0.020,
                    "zoom_window_V": [0.080, 0.520],
                },
            ], "E_SKEW_ROUTE_MATERIAL_CONFIGURATIONS")
    require(routes[1].get("route") == "GRAPHITE_TRANSITION_COUNT_SWEEP" and
            routes[1].get("rng_seed") == 11 and
            routes[1].get("restarts_per_strategy") == 3 and
            routes[1].get("seed_strategies") == 3 and
            routes[1].get("source_max_nfev") == 4000 and
            routes[1].get("perturbation_multiplier_uniform") == [0.75, 1.25],
            "E_GALLERY_ROUTE_EXECUTION_CONTRACT")
    require(routes[1].get("bounds_recipe") == {
        "Omega": [0.0, "8*R*T"], "Q": [1e-9, "10*area"],
        "U": ["V_min", "V_max"], "alpha": [0.15, 8.0],
        "bg": ["min(0,D_min)", "max(D_max,1e-9)"], "w": [0.0001, 0.12],
    }, "E_GALLERY_ROUTE_BOUNDS")
    require(routes[1].get("initialization_recipe") == {
        "Omega": "2.4*R*T", "Q": "area/N",
        "U": "one_of_three_peak_uniform_or_peak_overlap_seed_sets",
        "alpha": 1.0, "bg": "D_min", "w": 0.004,
    }, "E_GALLERY_ROUTE_INITIALIZATION")
    require(routes[1].get("material_run_configuration") == {
        "csv": "gr.csv", "fit_window_V": [0.060, 0.300],
        "grid_step_V": 2.5e-4, "material": "graphite",
    }, "E_GALLERY_ROUTE_MATERIAL_CONFIGURATION")
    require(routes[1].get("sweep_components") == {
        "logistic": [3, 4, 5, 6, 7, 8], "regsol": [3, 4, 5, 6, 7],
        "skew-logistic": [3, 4, 5, 6, 7], "skew-regsol": [3, 4, 5, 6],
    }, "E_GALLERY_ROUTE_SWEEP")

    absence = matrix.get("absent_class_records")
    require(absence == [
        {"evidence_class": "SYNTHETIC", "scope": "EXACT_REVIEWED_FITTING_INVENTORY",
         "status": "NO_POSITIVE_RECORD_FOUND"},
        {"evidence_class": "DEMO", "scope": "EXACT_REVIEWED_FITTING_INVENTORY",
         "status": "NO_POSITIVE_RECORD_FOUND"},
    ], "E_ABSENT_CLASSES")
    conflict = matrix.get("source_comment_execution_conflict")
    require(conflict == {
        "adjudication": "EXECUTABLE_CALL_PATH_AND_PHASE066_SEAL_CONTROL",
        "claimed_in_docstring": "BDD_DMSMCD_PLUS_WAVELET_PLUS_SAVGOL",
        "executed_by_direct14_preprocessing": "SAVGOL_ENSEMBLE_WITHOUT_BDD_DMSMCD_OR_WAVELET",
        "phase066_wavelet_or_bdd_dmsmcd_used": False,
        "source_path": "Claude/results/comp_v26_data/test_skew_regsol_v2.py",
    }, "E_SOURCE_COMMENT_CONFLICT")

    obligations = matrix.get("bounded_obligations")
    require(isinstance(obligations, list) and [row.get("obligation_id") for row in obligations] ==
            ["P065-OBL-0054", "P066-OBL-0120"], "E_OBLIGATION_IDS")
    active = {row["obligation_id"]: row for row in carry["active_obligations"]}
    s72 = next(row for row in phase065["findings"] if row["id"] == "S72-F04")
    for row in obligations:
        source = active[row["obligation_id"]]
        require(row.get("origin_identity") == source["origin_identity"], "E_OBLIGATION_ORIGIN")
        require(row.get("canonical_owner") == "P067-CODE-HISTORY", "E_OBLIGATION_OWNER")
        require(row.get("prior_state") == "OPEN_CARRY", "E_OBLIGATION_PRIOR_STATE")
        require(row.get("step89_disposition") == "EXPLICITLY_BOUNDED_NOT_RESOLVED",
                "E_OBLIGATION_DISPOSITION")
        require(row.get("external_authority_promoted") is False, "E_OBLIGATION_PROMOTION")
        require(row.get("next_owner") == "P067-STEP90.1-DISPOSITION",
                "E_OBLIGATION_NEXT_OWNER")
    require(obligations[0].get("claim") == s72["finding"], "E_S72_CLAIM")

    p79 = next(row for row in empirical["claim_rows"] if row["id"] == "P79-07")
    require(matrix.get("finite_rate_boundary", {}).get("claim") == p79["claim"],
            "E_FINITE_RATE_CLAIM")
    require(matrix["finite_rate_boundary"].get("physical_ceiling") == p79["physical_ceiling"],
            "E_FINITE_RATE_CEILING")
    require(matrix["finite_rate_boundary"].get("physical_authority") is False,
            "E_FINITE_RATE_PROMOTION")

    policy = runtime.get("execution_policy")
    require(policy == {
        "fresh_historical_fit_execution_count": 0,
        "historical_fit_executed": False,
        "optimizer_call_count_in_step89": 0,
        "phase066_sealed_evidence_reused": True,
        "supplemental_source_executed": False,
        "supplemental_source_read_mode": "STATIC_GIT_OBJECT_ONLY",
    }, "E_EXECUTION_POLICY")
    sealed = runtime.get("sealed_replay_records")
    require(isinstance(sealed, list) and len(sealed) == 2, "E_REPLAY_COUNT")
    expected_selected = optimizer["selected_replay_trials"]
    require(typed_equal(sealed, expected_selected), "E_REPLAY_RECORDS")
    require([row["runtime_label"] for row in sealed] == ["python3.12", "python3.14"],
            "E_REPLAY_LABELS")
    require(all(row["success"] is False and row["status"] == 0 and row["nfev"] == 6000
                for row in sealed), "E_REPLAY_NONCONVERGED")
    original = runtime.get("original_optimizer_state_availability")
    require(typed_equal(original, optimizer["original_optimizer_state_availability"])
            and len(original) == 25 and all(row["status"] == "GROUND_NOT_FOUND" for row in original),
            "E_ORIGINAL_STATE_GNF")
    require(runtime.get("step77_external_process_evidence") ==
            empirical["source_gates"]["step77_external_process_evidence"],
            "E_PROCESS_EVIDENCE")
    require(runtime.get("step77_runtime_success") is reproduction["runtime_success"] is False,
            "E_RUNTIME_SUCCESS")
    require(runtime.get("step77_selected_trial_converged") is
            reproduction["selected_trial_converged"] is False, "E_TRIAL_CONVERGENCE")
    checks = runtime.get("saved_consistency_checks")
    require(isinstance(checks, list) and len(checks) == 3
            and all(row.get("status") == "MATCH" for row in checks),
            "E_SAVED_CHECKS")
    static_checks = runtime.get("static_source_checks")
    require(isinstance(static_checks, list) and len(static_checks) == 4
            and all(row.get("ast_parse") == "PASS" and row.get("executed") is False
                    for row in static_checks), "E_STATIC_CHECKS")
    require(runtime.get("authority") == {
        "canonical_release": False,
        "external_scientific_validation": False,
        "held_out_validation": False,
        "historical_optimizer_state": False,
        "identifiability": False,
        "material_assignment": False,
        "phase_or_mechanism_identification": False,
        "publication": False,
        "protocol_binding": False,
    }, "E_RUNTIME_AUTHORITY")


def validate_preview(matrix: dict[str, Any], runtime: dict[str, Any]) -> None:
    first = builder_preview()
    second = builder_preview()
    require(typed_equal(first, second), "E_BUILDER_NONDETERMINISTIC")
    require(typed_equal(first["matrix"], matrix), "E_MATRIX_REBUILD")
    require(typed_equal(first["runtime"], runtime), "E_RUNTIME_REBUILD")


def put(mapping: Any, key: Any, value: Any) -> None:
    mapping[key] = value


def negative_controls(matrix: dict[str, Any], runtime: dict[str, Any]) -> int:
    mutations: list[tuple[str, Any]] = []

    def add(label: str, target: str, fn: Any) -> None:
        mutations.append((label, (target, fn)))

    add("supplemental_oid", "matrix", lambda x: put(x["supplemental_inputs"][0], "git_blob_oid", "0" * 40))
    add("supplemental_mode", "matrix", lambda x: put(x["supplemental_inputs"][0], "mode", "100755"))
    add("supplemental_path", "matrix", lambda x: put(x["supplemental_inputs"][0], "path", "wrong"))
    add("supplemental_role", "matrix", lambda x: put(x["supplemental_inputs"][0], "bounded_role", ""))
    add("parent_raw_pin", "matrix", lambda x: put(x["phase066_inputs"][0], "raw_sha256", "0" * 64))
    add("columns", "matrix", lambda x: put(x["direct14_contract"]["raw_input"], "columns", ["V", "Q"]))
    add("capacity_basis", "matrix", lambda x: put(x["direct14_contract"]["raw_input"], "capacity_basis", "specific"))
    add("protocol_promotion", "matrix", lambda x: put(x["direct14_contract"]["raw_input"], "specimen_protocol_status", "VERIFIED"))
    add("parameter_order", "matrix", lambda x: x["direct14_contract"]["optimizer"]["parameter_order"].reverse())
    add("free_mask", "matrix", lambda x: put(x["direct14_contract"]["optimizer"], "free_mask", "explicit"))
    add("objective", "matrix", lambda x: put(x["direct14_contract"]["optimizer"], "objective", "weighted"))
    add("seed", "matrix", lambda x: put(x["direct14_contract"]["optimizer"], "rng_seed", 24))
    add("tolerance", "matrix", lambda x: put(x["direct14_contract"]["optimizer"], "historical_resolved_defaults_and_scipy_version", "KNOWN"))
    add("supplemental_route_seed", "matrix", lambda x: put(x["supplemental_route_contracts"][0], "rng_seed", 23))
    add("supplemental_route_max_nfev", "matrix", lambda x: put(x["supplemental_route_contracts"][1], "source_max_nfev", 6000))
    add("supplemental_route_grid", "matrix", lambda x: put(x["supplemental_route_contracts"][0]["material_run_configurations"][2], "grid_step_V", 1.0e-3))
    add("supplemental_route_transition", "matrix", lambda x: put(x["supplemental_route_contracts"][0]["material_run_configurations"][0]["initial_transition_U_V"], 0, 0.105))
    add("gallery_route_window", "matrix", lambda x: put(x["supplemental_route_contracts"][1]["material_run_configuration"], "fit_window_V", [0.0, 1.0]))
    add("comparison_bound", "matrix", lambda x: put(x["comparison_source_contracts"][0]["bounds"], "w", [0.0, 1.0]))
    add("comparison_dependency", "matrix", lambda x: put(x["comparison_source_contracts"][0]["seed_and_bounds_dependency"], "path", "wrong"))
    add("comparison_perturbation", "matrix", lambda x: put(x["comparison_source_contracts"][0], "restart_perturbation_multiplier_uniform", [0.5, 1.5]))
    add("class_swap", "matrix", lambda x: put(x["evidence_records"][0], "evidence_class", "SAVED_ONLY"))
    add("class_invalid", "matrix", lambda x: put(x["evidence_records"][0], "evidence_class", "HYBRID"))
    add("authority_external", "matrix", lambda x: put(x["evidence_records"][0]["authority"], "external", True))
    add("saved_authority", "matrix", lambda x: put(x["saved_profile_records"][0], "authority", "ORIGINAL"))
    add("saved_metric", "matrix", lambda x: put(x["saved_profile_records"][0]["metrics"], "R2", 1.0))
    add("saved_flat_vector", "matrix", lambda x: put(x["saved_profile_records"][0]["flat_parameter_vector"], 0, 0.0))
    add("obligation_owner", "matrix", lambda x: put(x["bounded_obligations"][0], "canonical_owner", "OTHER"))
    add("obligation_resolve", "matrix", lambda x: put(x["bounded_obligations"][0], "step89_disposition", "RESOLVED"))
    add("finite_rate_promotion", "matrix", lambda x: put(x["finite_rate_boundary"], "physical_authority", True))
    add("fresh_fit", "runtime", lambda x: put(x["execution_policy"], "historical_fit_executed", True))
    add("optimizer_call", "runtime", lambda x: put(x["execution_policy"], "optimizer_call_count_in_step89", 1))
    add("replay_success", "runtime", lambda x: put(x["sealed_replay_records"][0], "success", True))
    add("original_state", "runtime", lambda x: put(x["original_optimizer_state_availability"][0], "status", "AVAILABLE"))
    add("heldout_promotion", "runtime", lambda x: put(x["authority"], "held_out_validation", True))
    add("identifiability_promotion", "runtime", lambda x: put(x["authority"], "identifiability", True))
    add("publication_promotion", "runtime", lambda x: put(x["authority"], "publication", True))

    passed = 0
    for label, (target, mutate) in mutations:
        m = copy.deepcopy(matrix)
        r = copy.deepcopy(runtime)
        mutate(m if target == "matrix" else r)
        try:
            validate_core(m, r)
        except ValidationError:
            passed += 1
        else:
            raise ValidationError("E_NEGATIVE_CONTROL:" + label)
    return passed


def json_controls() -> int:
    cases = [
        b'{"a":1,"a":2}',
        b'{"a":NaN}',
        b'{"a":Infinity}',
        b'{"a":-Infinity}',
        (b'{"a":' + b'[' * 65 + b'0' + b']' * 65 + b'}'),
        b'{"a":1} trailing',
        b'[]',
    ]
    passed = 0
    for raw in cases:
        try:
            strict_load(raw, "E_JSON_CONTROL", generated=False)
        except ValidationError:
            passed += 1
        else:
            raise ValidationError("E_JSON_CONTROL_ACCEPTED")
    return passed


def lf_bytes(raw: bytes) -> bytes:
    return raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def neutral_source_hash(raw: bytes, role: str) -> str:
    text = lf_bytes(raw).decode("utf-8")
    if role == "validator":
        text, count = re.subn(
            r'(?m)^VALIDATOR_NEUTRAL_SHA256_LF = "[0-9a-f]{64}"$',
            'VALIDATOR_NEUTRAL_SHA256_LF = "' + "0" * 64 + '"', text,
        )
        require(count == 1, "E_VALIDATOR_NEUTRAL_SLOT")
    return sha(text.encode("utf-8"))


def source_policy_errors(source: str, role: str) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return ["E_AST_PARSE:" + str(exc)]
    parents = {child: parent for parent in ast.walk(tree)
               for child in ast.iter_child_nodes(parent)}

    expected_imports = {
        "builder": {"argparse", "ast", "csv", "hashlib", "io", "json", "math", "os",
                    "subprocess", "sys"},
        "validator": {"argparse", "ast", "copy", "hashlib", "json", "math", "re",
                      "subprocess", "sys"},
    }[role]
    expected_from = {("__future__", "annotations"), ("pathlib", "Path"), ("typing", "Any")}
    imports: set[str] = set()
    from_imports: set[tuple[str, str]] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if not isinstance(parents.get(node), ast.Module):
                errors.append("E_NESTED_IMPORT")
            for alias in node.names:
                imports.add(alias.name)
                if alias.asname is not None:
                    errors.append("E_IMPORT_ALIAS")
        elif isinstance(node, ast.ImportFrom):
            if not isinstance(parents.get(node), ast.Module) or node.level != 0:
                errors.append("E_NESTED_FROM_IMPORT")
            for alias in node.names:
                from_imports.add((str(node.module), alias.name))
                if alias.asname is not None or alias.name == "*":
                    errors.append("E_FROM_IMPORT_ALIAS")
    if imports != expected_imports:
        errors.append("E_IMPORT_INVENTORY")
    if from_imports != expected_from:
        errors.append("E_FROM_IMPORT_INVENTORY")

    expected_module_bindings = {
        "builder": [
            "ROOT", "BASELINE", "EXPECTED_PARENT", "SUPPLEMENTAL_COMMIT", "BRANCH",
            "DATE", "SUBJECT", "GATE", "PERSISTENCE", "MATRIX_PATH", "RUNTIME_PATH",
            "FIT_PROVENANCE", "FIT_REPRODUCTION", "OPTIMIZER_STATE", "EMPIRICAL_AUTHORITY",
            "CARRY_FORWARD", "PHASE065_AUTHORITY", "PARENT_INPUTS", "PARENT_EXPECTED",
            "SUPPLEMENTAL_PATHS", "ROLES", "SUPPORT", "CLASS_ENUM", "AUTHORITY_FALSE",
        ],
        "validator": [
            "ROOT", "BASELINE", "EXPECTED_PARENT", "SUPPLEMENTAL_COMMIT", "BRANCH",
            "PROTECTED_TIP", "MAIN_TIP", "SUBJECT", "GATE", "PERSISTENCE", "BUILDER",
            "VALIDATOR", "MATRIX", "RUNTIME", "RESULT", "PARENT_LEDGER",
            "CANONICAL_LEDGER", "HANDOVER", "FINAL_PATHS", "FINAL_STATUS",
            "FIT_PROVENANCE", "FIT_REPRODUCTION", "OPTIMIZER_STATE", "EMPIRICAL_AUTHORITY",
            "CARRY_FORWARD", "PHASE065_AUTHORITY", "PARENT_INPUTS", "PARENT_EXPECTED",
            "SUPPLEMENTAL_PATHS", "SUPPLEMENTAL_EXPECTED", "SUPPORT_EXPECTED", "CLASS_ENUM",
            "AUTHORITY_KEYS", "MAX_JSON_BYTES", "MAX_JSON_DEPTH", "MAX_JSON_NODES",
            "BUILDER_SOURCE_SHA256_LF", "VALIDATOR_NEUTRAL_SHA256_LF",
        ],
    }[role]
    module_binding_names: list[str] = []
    for statement in tree.body:
        if isinstance(statement, ast.Assign):
            module_binding_names.extend(
                target.id for target in statement.targets if isinstance(target, ast.Name)
            )
        elif isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            module_binding_names.append(statement.target.id)
    if module_binding_names != expected_module_bindings:
        errors.append("E_MODULE_BINDING_INVENTORY")

    expected_functions = {
        "builder": {
            "require", "sha", "canonical", "semantic", "finish", "strict_json",
            "git_argv_allowed", "git_bytes", "parent_raw", "parent_json", "supplemental_raw",
            "tree_row", "input_record", "supplemental_record", "static_source_check",
            "real_data_profile", "evidence_row", "comparison_contracts",
            "supplemental_route_contracts", "saved_profile_records", "metadata", "build",
            "atomic_write", "main",
        },
        "validator": {
            "require", "sha", "canonical", "semantic", "typed_equal", "strict_load", "is_oid",
            "git_argv_allowed", "git_bytes", "git_text", "parent_json", "supplemental_identity",
            "builder_preview", "load_outputs", "require_metadata", "validate_core",
            "validate_preview", "put", "negative_controls", "json_controls", "lf_bytes",
            "neutral_source_hash", "source_policy_errors", "source_policy_controls",
            "source_policy", "git_argv_controls", "parse_status", "parse_name_status",
            "require_index_modes", "require_tree_modes", "repository_guard",
            "control_documents", "main",
        },
    }[role]
    function_names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    class_names = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
    if set(function_names) != expected_functions or len(function_names) != len(expected_functions):
        errors.append("E_FUNCTION_INVENTORY")
    expected_classes = {"BuildError"} if role == "builder" else {"ValidationError"}
    if set(class_names) != expected_classes or len(class_names) != len(expected_classes):
        errors.append("E_CLASS_INVENTORY")
    expected_nested = {"builder": {"pairs"},
                       "validator": {"pairs", "add", "owner", "unique_line"}}[role]
    all_function_names = [node.name for node in ast.walk(tree)
                          if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if sorted(all_function_names) != sorted(expected_functions | expected_nested):
        errors.append("E_ALL_FUNCTION_INVENTORY")
    all_class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    if sorted(all_class_names) != sorted(expected_classes):
        errors.append("E_ALL_CLASS_INVENTORY")
    default_inventory = {
        node.name: (
            [ast.unparse(value) for value in node.args.defaults],
            [None if value is None else ast.unparse(value)
             for value in node.args.kw_defaults],
        )
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        (node.args.defaults or node.args.kw_defaults)
    }
    expected_defaults = {
        "builder": {},
        "validator": {
            "git_bytes": (["'E_GIT'"], []),
            "git_text": (["'E_GIT'"], []),
            "require": (["''"], []),
            "strict_load": ([], [None]),
        },
    }[role]
    if default_inventory != expected_defaults:
        errors.append("E_FUNCTION_DEFAULT_INVENTORY")
    sensitive_function_hashes = {
        node.name: sha(ast.unparse(node).encode("utf-8"))
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in {
            "atomic_write", "builder_preview", "control_documents", "git_argv_allowed",
            "git_bytes", "git_text", "load_outputs", "repository_guard",
            "require_index_modes", "require_tree_modes", "source_policy",
            "supplemental_identity",
        }
    }
    expected_sensitive_hashes = {
        "builder": {
            "atomic_write": "4d68e874bdf46ae625d6ae6dff550c8d1608386177418ca7a3d4fb0dfedca172",
            "git_argv_allowed": "9fc33c97b6be4a3e67e5c15ecfd6e434f9dc7d2b94f56e788a509e22ac0984cb",
            "git_bytes": "7f80cf6f731a00daf11c721dd98ee10f727555b2c9a1878697e9d88f1916f887",
        },
        "validator": {
            "builder_preview": "c40b60f57ee88db821bb508015bca202485a340d017d2ece632b1329f1cb9170",
            "control_documents": "dc40e0d970afb9f9d13cc5e1d28f7dafcf00767b0c3b15c58982d06e1d1e4f04",
            "git_argv_allowed": "39caaa57bbc3dc715f0cbebbedefb2ce6b8919cd30cbccc14fa747ceb5d5b8ec",
            "git_bytes": "17cb043ee2e6d094d4fbb9a2ecfdc22a690097c4e6dc59bd32394e33cb837cdf",
            "git_text": "c4c1bab8febbc71d3068bc42f586dc54f70c885a641403c126a27495f0e18cb9",
            "load_outputs": "98cb009cf8281b354dc3cb39211276bb3051fc4cf82336e0bc6289a8766f066d",
            "repository_guard": "51c270c717f78c5edc9810c9743a8576e5bbe506b92a43709308700f5b7e8bd7",
            "require_index_modes": "c7ff3d7f4f98239aaf05a55592a40b15760584853d3be7f3407f04db07937e75",
            "require_tree_modes": "b95ff386f00ccec3fd22db69df0d895538619b920416a75e2885da55ab477fba",
            "source_policy": "f71a1010c849f8358b74a0a307410015cad410d65c18c32631c9f8a377b23bdf",
            "supplemental_identity": "5f48e1594849db4d139ad887e535d62294eddcbdb16db21430d44322c4dfce4f",
        },
    }[role]
    if sensitive_function_hashes != expected_sensitive_hashes:
        errors.append("E_SENSITIVE_FUNCTION_HASHES")

    sensitive = {"eval", "exec", "compile", "__import__", "input", "open", "getattr",
                 "setattr", "delattr", "globals", "locals", "vars", "__builtins__"}
    modules = expected_imports
    protected_callables = expected_functions
    allowed_name_calls = {
        "builder": {
            "BuildError", "Path", "SystemExit", "ValueError", "all", "any",
            "atomic_write", "build", "canonical", "comparison_contracts", "dict",
            "evidence_row", "finish", "float", "git_argv_allowed", "git_bytes",
            "input_record", "isinstance", "len", "list", "main", "max", "metadata",
            "min", "next", "parent_json", "parent_raw", "print", "range",
            "real_data_profile", "require", "saved_profile_records", "semantic", "sha",
            "sorted", "static_source_check", "str", "strict_json", "sum",
            "supplemental_raw", "supplemental_record", "supplemental_route_contracts",
            "tree_row", "tuple", "zip",
        },
        "validator": {
            "Path", "SystemExit", "ValidationError", "ValueError", "add", "all", "any",
            "bool", "builder_preview", "canonical", "control_documents", "dict",
            "enumerate", "git_argv_allowed", "git_argv_controls", "git_bytes", "git_text",
            "is_oid", "isinstance", "json_controls", "len", "lf_bytes", "list",
            "load_outputs", "main", "max", "mutate", "negative_controls",
            "neutral_source_hash", "next", "owner", "parent_json", "parse_name_status",
            "parse_status", "print", "put", "repository_guard", "repr", "require",
            "require_index_modes", "require_metadata", "require_tree_modes", "semantic",
            "set", "sha", "sorted", "source_policy", "source_policy_controls",
            "source_policy_errors", "str", "strict_load", "supplemental_identity", "tuple",
            "type", "typed_equal", "unique_line", "validate_core", "validate_preview", "zip",
        },
    }[role]
    allowed_module_attributes = {
        "builder": {
            "argparse": {"ArgumentParser"},
            "ast": {"AsyncFunctionDef", "FunctionDef", "Import", "ImportFrom", "parse", "walk"},
            "csv": {"reader"}, "hashlib": {"sha256"}, "io": {"StringIO"},
            "json": {"JSONDecodeError", "dumps", "loads"}, "math": {"isfinite"},
            "os": {"replace"}, "subprocess": {"PIPE", "run"},
            "sys": {"stderr", "stdout"},
        },
        "validator": {
            "argparse": {"ArgumentParser"},
            "ast": {
                "AST", "AnnAssign", "Assign", "AsyncFunctionDef", "Attribute", "Call",
                "ClassDef", "Del",
                "ExceptHandler", "Expr", "FunctionDef", "Import", "ImportFrom", "Load", "MatchAs",
                "MatchMapping", "MatchStar", "Module", "Name", "Store", "arg",
                "Return", "Try", "iter_child_nodes", "parse", "unparse", "walk",
            },
            "copy": {"deepcopy"}, "hashlib": {"sha256"},
            "json": {"JSONDecodeError", "dumps", "loads"}, "math": {"isfinite"},
            "re": {"fullmatch", "subn"}, "subprocess": {"PIPE", "run"},
            "sys": {"executable", "stderr"},
        },
    }[role]
    forbidden_attrs = {"Popen", "call", "check_call", "check_output", "system", "popen",
                       "spawn", "spawnl", "spawnle", "spawnlp", "spawnlpe", "spawnv",
                       "spawnve", "spawnvp", "spawnvpe", "open", "touch", "write_text",
                       "read_text", "unlink", "rmdir", "remove", "rmtree", "rename", "chmod",
                       "lchmod", "symlink_to", "hardlink_to", "link_to", "copy", "copy_into",
                       "move", "move_into", "stat", "lstat", "exists", "is_dir", "is_symlink",
                       "is_junction", "iterdir", "glob", "rglob", "walk", "readlink",
                       "samefile", "owner", "group", "resolve", "is_mount", "is_socket",
                       "is_fifo", "is_block_device", "is_char_device"}
    protected_fs_attrs = {"open", "touch", "write_text", "write_bytes", "read_text",
                          "read_bytes", "unlink", "rmdir", "rename", "replace", "chmod",
                          "lchmod", "symlink_to", "hardlink_to", "link_to", "mkdir", "is_file",
                          "copy", "copy_into", "move", "move_into", "stat", "lstat", "exists",
                          "is_dir", "is_symlink", "is_junction", "iterdir", "glob", "rglob",
                          "walk", "readlink", "samefile", "owner", "group", "resolve",
                          "is_mount", "is_socket", "is_fifo", "is_block_device",
                          "is_char_device"}
    protected_builtins = {
        "all", "any", "bool", "dict", "enumerate", "float", "isinstance", "len", "list",
        "max", "min", "next", "print", "range", "repr", "set", "sorted", "str", "sum",
        "tuple", "type", "zip",
    }
    module_constants = set(expected_module_bindings)

    def owner(node: ast.AST) -> str:
        current = parents.get(node)
        while current is not None:
            if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return current.name
            current = parents.get(current)
        return "<module>"

    expected_group_calls = {
        "builder": [],
        "validator": [
            ("require_index_modes", "match.group(1)"),
            ("require_index_modes", "match.group(3)"),
            ("require_tree_modes", "match.group(1)"),
            ("require_tree_modes", "match.group(2)"),
            ("supplemental_identity", "baseline_match.group(2)"),
            ("supplemental_identity", "baseline_match.group(2)"),
            ("supplemental_identity", "baseline_match.group(3)"),
            ("supplemental_identity", "match.group(1)"),
            ("supplemental_identity", "match.group(2)"),
            ("supplemental_identity", "match.group(2)"),
            ("supplemental_identity", "match.group(2)"),
            ("supplemental_identity", "match.group(3)"),
        ],
    }[role]

    process_calls: list[tuple[str, str]] = []
    argparse_calls: list[tuple[str, str]] = []
    path_calls: list[str] = []
    fs_calls: list[tuple[str, str, str]] = []
    replace_calls: list[tuple[str, str]] = []
    protected_git_calls: list[tuple[str, str]] = []
    group_calls: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and \
                (node.decorator_list or node.type_params):
            errors.append("E_FUNCTION_DECORATOR_OR_TYPE_PARAMS:" + node.name)
        if isinstance(node, ast.ClassDef):
            if node.decorator_list or node.keywords or node.type_params:
                errors.append("E_CLASS_DECORATOR_KEYWORD_OR_TYPE_PARAMS:" + node.name)
            if [ast.unparse(base) for base in node.bases] != ["RuntimeError"]:
                errors.append("E_CLASS_BASE_INVENTORY:" + node.name)
        protected_names = protected_callables | modules | protected_builtins | \
            module_constants | {"Path"}
        if isinstance(node, ast.arg) and node.arg in protected_names:
            errors.append("E_PROTECTED_ARGUMENT:" + node.arg)
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)) and \
                node.id in protected_names:
            original_module_binding = node.id in module_constants and \
                owner(node) == "<module>" and isinstance(node.ctx, ast.Store)
            original_module_binding = original_module_binding and \
                parents.get(node) in tree.body
            if not original_module_binding:
                errors.append("E_PROTECTED_REBIND:" + node.id)
        if isinstance(node, ast.ExceptHandler) and node.name in \
                protected_names:
            errors.append("E_PROTECTED_EXCEPTION_BINDING:" + str(node.name))
        if isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name in \
                protected_names:
            errors.append("E_PROTECTED_PATTERN_BINDING:" + str(node.name))
        if isinstance(node, ast.MatchMapping) and node.rest in \
                protected_names:
            errors.append("E_PROTECTED_PATTERN_REST:" + str(node.rest))
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id in sensitive:
                errors.append("E_SENSITIVE_NAME:" + node.id)
            if node.id in modules:
                parent = parents.get(node)
                if not isinstance(parent, ast.Attribute) or parent.value is not node:
                    errors.append("E_MODULE_ESCAPE:" + node.id)
            if node.id in protected_callables:
                parent = parents.get(node)
                if not isinstance(parent, ast.Call) or parent.func is not node:
                    errors.append("E_CALLABLE_ESCAPE:" + node.id)
            if node.id == "Path":
                parent = parents.get(node)
                if not isinstance(parent, ast.Call) or parent.func is not node:
                    errors.append("E_PATH_ESCAPE")
        if isinstance(node, ast.Attribute):
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                errors.append("E_ATTRIBUTE_MUTATION:" + node.attr)
            if node.attr.startswith("__"):
                errors.append("E_DUNDER_ATTRIBUTE:" + node.attr)
            if isinstance(node.value, ast.Name) and node.value.id in modules and \
                    node.attr not in allowed_module_attributes[node.value.id]:
                errors.append("E_MODULE_ATTRIBUTE_INVENTORY:" +
                              node.value.id + "." + node.attr)
            if isinstance(node.value, ast.Name) and node.value.id == "subprocess":
                if node.attr not in {"run", "PIPE"}:
                    errors.append("E_SUBPROCESS_ATTRIBUTE:" + node.attr)
                if node.attr == "run" and not (
                    isinstance(parents.get(node), ast.Call) and parents[node].func is node
                ):
                    errors.append("E_BOUND_SUBPROCESS_RUN")
            if isinstance(node.value, ast.Name) and node.value.id == "os":
                if role != "builder" or node.attr != "replace" or not (
                    isinstance(parents.get(node), ast.Call) and parents[node].func is node
                    and owner(node) == "atomic_write"
                ):
                    errors.append("E_OS_ATTRIBUTE:" + node.attr)
            if isinstance(node.value, ast.Name) and node.value.id == "argparse" and \
                    node.attr != "ArgumentParser":
                errors.append("E_ARGPARSE_ATTRIBUTE:" + node.attr)
            if isinstance(node.value, ast.Name) and node.value.id == "argparse" and \
                    node.attr == "ArgumentParser" and not (
                        isinstance(parents.get(node), ast.Call) and parents[node].func is node
                    ):
                errors.append("E_BOUND_ARGUMENT_PARSER")
            if isinstance(node.value, ast.Name) and node.value.id == "sys" and \
                    node.attr not in {"executable", "stdout", "stderr"}:
                errors.append("E_SYS_ATTRIBUTE:" + node.attr)
            if node.attr in protected_fs_attrs:
                parent = parents.get(node)
                if not isinstance(parent, ast.Call) or parent.func is not node:
                    errors.append("E_BOUND_FILESYSTEM_METHOD:" + node.attr)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, (ast.Name, ast.Attribute)):
                errors.append("E_INDIRECT_CALL")
            if any(keyword.arg is None or keyword.arg == "shell" for keyword in node.keywords):
                errors.append("E_DYNAMIC_OR_SHELL_KEYWORD")
            if isinstance(node.func, ast.Name) and node.func.id == "Path":
                path_calls.append(ast.unparse(node))
            if isinstance(node.func, ast.Name) and node.func.id not in allowed_name_calls:
                errors.append("E_NAME_CALL_INVENTORY:" + node.func.id)
            if isinstance(node.func, ast.Name) and node.func.id in {"git_bytes", "git_text"}:
                protected_git_calls.append((owner(node), ast.unparse(node)))
            if isinstance(node.func, ast.Name) and node.func.id in sensitive:
                errors.append("E_SENSITIVE_CALL:" + node.func.id)
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in forbidden_attrs and not (
                    isinstance(node.func.value, ast.Name) and (
                        (node.func.value.id in modules and
                         node.func.attr in allowed_module_attributes[node.func.value.id]) or
                        (node.func.attr == "group" and
                         (owner(node), ast.unparse(node)) in expected_group_calls)
                    )
                    or (node.func.attr == "resolve" and owner(node) == "<module>" and
                        ast.unparse(node) == "Path(__file__).resolve()")
                ):
                    errors.append("E_FORBIDDEN_ATTRIBUTE_CALL:" + node.func.attr)
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                    process_calls.append((owner(node), ast.unparse(node)))
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "argparse" and \
                        node.func.attr == "ArgumentParser":
                    argparse_calls.append((owner(node), ast.unparse(node)))
                    if node.keywords:
                        errors.append("E_ARGUMENT_PARSER_KEYWORDS")
                if node.func.attr in {"read_bytes", "write_bytes", "mkdir", "is_file"}:
                    fs_calls.append((owner(node), node.func.attr, ast.unparse(node)))
                if node.func.attr == "replace":
                    replace_calls.append((owner(node), ast.unparse(node)))
                if node.func.attr == "group":
                    group_calls.append((owner(node), ast.unparse(node)))

    if path_calls != ["Path(__file__)"]:
        errors.append("E_PATH_CONSTRUCTOR_INVENTORY")
    expected_process = {
        "builder": [
            ("git_bytes", "subprocess.run(['git', *args], cwd=ROOT, check=False, "
             "stdout=subprocess.PIPE, stderr=subprocess.PIPE)"),
        ],
        "validator": [
            ("git_bytes", "subprocess.run(['git', *args], cwd=ROOT, check=False, "
             "stdout=subprocess.PIPE, stderr=subprocess.PIPE)"),
            ("builder_preview", "subprocess.run([sys.executable, '-B', str(ROOT / BUILDER), "
             "'--preview'], cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)"),
        ],
    }[role]
    if process_calls != expected_process:
        errors.append("E_PROCESS_INVENTORY")
    if argparse_calls != [("main", "argparse.ArgumentParser()")]:
        errors.append("E_ARGUMENT_PARSER_INVENTORY")
    expected_fs = {
        "builder": [
            ("atomic_write", "mkdir", "target.parent.mkdir(parents=True, exist_ok=True)"),
            ("atomic_write", "write_bytes", "temporary.write_bytes(raw)"),
        ],
        "validator": [
            ("load_outputs", "is_file", "(ROOT / MATRIX).is_file()"),
            ("load_outputs", "is_file", "(ROOT / RUNTIME).is_file()"),
            ("load_outputs", "read_bytes", "(ROOT / MATRIX).read_bytes()"),
            ("load_outputs", "read_bytes", "(ROOT / RUNTIME).read_bytes()"),
            ("source_policy", "read_bytes", "(ROOT / BUILDER).read_bytes()"),
            ("source_policy", "read_bytes", "(ROOT / VALIDATOR).read_bytes()"),
            ("control_documents", "read_bytes", "(ROOT / path).read_bytes()"),
        ],
    }[role]
    if sorted(fs_calls) != sorted(expected_fs):
        errors.append("E_FILESYSTEM_INVENTORY")
    expected_replace = {
        "builder": [("atomic_write", "os.replace(temporary, target)")],
        "validator": [
            ("lf_bytes", "raw.decode('utf-8').replace('\\r\\n', '\\n')"),
            ("lf_bytes", "raw.decode('utf-8').replace('\\r\\n', '\\n').replace('\\r', '\\n')"),
            ("source_policy_controls",
             "validator_source.replace('source_negative = source_policy()\\n        git_controls = git_argv_controls()', 'git_controls = git_argv_controls()\\n        source_negative = source_policy()')"),
            ("source_policy_controls",
             "validator_source.replace('def source_policy() -> int:', '@lambda original: (lambda: 38)\\ndef source_policy() -> int:')"),
            ("source_policy_controls",
             "validator_source.replace('    try:\\n        source_negative = source_policy()\\n        git_controls = git_argv_controls()\\n        parser = argparse.ArgumentParser()', '    if False:\\n        source_negative = source_policy()\\n        git_controls = git_argv_controls()\\n    try:\\n        source_negative = 0\\n        git_controls = 0\\n        parser = argparse.ArgumentParser()')"),
            ("source_policy_controls",
             "validator_source.replace('def control_documents() -> None:', 'def control_documents(_preview=builder_preview()) -> None:')"),
            ("source_policy_controls",
             "builder_source.replace('    require(git_argv_allowed(tuple(args)), \"E_GIT_ARGV\")', '    require(git_argv_allowed(tuple(args)), \"E_GIT_ARGV\")\\n    args[:] = [\"clean\", \"-fd\"]')"),
            ("source_policy_controls",
             "builder_source.replace('    target = ROOT / path', \"    path = '//server/share/outside'\\n    target = ROOT / path\")"),
            ("source_policy_controls",
             "validator_source.replace('def load_outputs() -> tuple[dict[str, Any], dict[str, Any], int, int]:', \"def load_outputs() -> tuple[dict[str, Any], dict[str, Any], int, int]:\\n    MATRIX = '//server/share/payload'\")"),
            ("source_policy_controls",
             "builder_source.replace('os.replace(temporary, target)', \"os.replace(temporary, target)\\n    target.replace('outside')\")"),
            ("source_policy_controls",
             "builder_source.replace('os.replace(temporary, target)', \"os.replace(temporary, target)\\n    os.replace('victim', 'outside')\")"),
            ("parse_status", "line[3:].replace('\\\\', '/')"),
            ("parse_name_status", "parts[1].replace('\\\\', '/')"),
            ("require_index_modes", "match.group(3).replace('\\\\', '/')"),
            ("require_tree_modes", "match.group(2).replace('\\\\', '/')"),
        ],
    }[role]
    if sorted(replace_calls) != sorted(expected_replace):
        errors.append("E_REPLACE_INVENTORY")
    if sorted(group_calls) != sorted(expected_group_calls):
        errors.append("E_GROUP_CALL_INVENTORY")

    expected_git_calls = {
        "builder": [
            ("parent_raw", "git_bytes(['show', f'{EXPECTED_PARENT}:{path}'])"),
            ("supplemental_raw", "git_bytes(['show', f'{SUPPLEMENTAL_COMMIT}:{path}'])"),
            ("tree_row", "git_bytes(['ls-tree', ref, '--', path])"),
        ],
        "validator": [
            ("git_text", "git_bytes(args, code)"),
            ("parent_json", "git_bytes(['show', f'{EXPECTED_PARENT}:{path}'])"),
            ("repository_guard", "git_bytes(['status', '--porcelain=v1', '--untracked-files=all'], 'E_STATUS')"),
            ("repository_guard", "git_text(['diff', '--cached', '--name-only'])"),
            ("repository_guard", "git_text(['diff', '--cached', '--name-status', '--no-renames', EXPECTED_PARENT, '--'])"),
            ("repository_guard", "git_text(['diff', '--name-only'])"),
            ("repository_guard", "git_text(['diff', '--name-only', PROTECTED_TIP, compare_head, '--', 'Claude'])"),
            ("repository_guard", "git_text(['diff-tree', '--no-commit-id', '--name-status', '-r', '--no-renames', commit, '--'])"),
            ("repository_guard", "git_text(['ls-remote', '--heads', 'origin', f'refs/heads/{BRANCH}'], 'E_LIVE_REMOTE')"),
            ("repository_guard", "git_text(['rev-parse', '@{u}'])"),
            ("repository_guard", "git_text(['rev-parse', 'HEAD'], 'E_HEAD')"),
            ("repository_guard", "git_text(['rev-parse', 'refs/remotes/origin/codex/lib-physics-endgame-v1025_2'])"),
            ("repository_guard", "git_text(['rev-parse', 'refs/remotes/origin/main'])"),
            ("repository_guard", "git_text(['rev-parse', f'refs/remotes/origin/{BRANCH}'])"),
            ("repository_guard", "git_text(['show', '--no-patch', '--format=%P', commit], 'E_COMMIT_PARENT')"),
            ("repository_guard", "git_text(['show', '--no-patch', '--format=%s', commit], 'E_COMMIT_SUBJECT')"),
            ("repository_guard", "git_text(['symbolic-ref', '--quiet', '--short', 'HEAD'], 'E_BRANCH')"),
            ("require_index_modes", "git_text(['ls-files', '--stage', '--', *FINAL_PATHS], 'E_INDEX_MODES')"),
            ("require_tree_modes", "git_text(['ls-tree', commit, '--', *FINAL_PATHS], 'E_TREE_MODES')"),
            ("supplemental_identity", "git_bytes(['show', f'{SUPPLEMENTAL_COMMIT}:{path}'], 'E_SUPPLEMENTAL_READ')"),
            ("supplemental_identity", "git_text(['ls-tree', BASELINE, '--', path], 'E_BASELINE_TREE')"),
            ("supplemental_identity", "git_text(['ls-tree', SUPPLEMENTAL_COMMIT, '--', path], 'E_SUPPLEMENTAL_TREE')"),
            ("validate_core", "git_bytes(['show', f'{SUPPLEMENTAL_COMMIT}:{SUPPLEMENTAL_PATHS[6]}'])"),
            ("validate_core", "git_bytes(['show', f'{SUPPLEMENTAL_COMMIT}:{path}'])"),
        ],
    }[role]
    if sorted(protected_git_calls) != sorted(expected_git_calls):
        errors.append("E_GIT_CALL_SITE_INVENTORY")

    module_calls = [ast.unparse(node) for node in ast.walk(tree)
                    if isinstance(node, ast.Call) and owner(node) == "<module>"]
    expected_module_calls = {
        "builder": ["Path(__file__)", "Path(__file__).resolve()", "SystemExit(main())", "main()"],
        "validator": ["Path(__file__)", "Path(__file__).resolve()", "enumerate(FINAL_PATHS)",
                      "SystemExit(main())", "main()"],
    }[role]
    if sorted(module_calls) != sorted(expected_module_calls):
        errors.append("E_MODULE_CALL_INVENTORY")
    if role == "validator":
        main_node = next((node for node in tree.body
                          if isinstance(node, ast.FunctionDef) and node.name == "main"), None)
        if main_node is None:
            errors.append("E_MAIN_ABSENT")
        else:
            if len(main_node.body) != 5 or not isinstance(main_node.body[0], ast.Try) or \
                    not all(isinstance(node, ast.Expr) for node in main_node.body[1:4]) or \
                    not isinstance(main_node.body[4], ast.Return):
                errors.append("E_MAIN_BODY_SHAPE")
            first_try = main_node.body[0] if main_node.body else None
            if not isinstance(first_try, ast.Try) or first_try.orelse or first_try.finalbody or \
                    len(first_try.handlers) != 1:
                errors.append("E_MAIN_FIRST_TRY_SHAPE")
            elif len(first_try.body) < 3 or [ast.unparse(node) for node in first_try.body[:3]] != [
                "source_negative = source_policy()",
                "git_controls = git_argv_controls()",
                "parser = argparse.ArgumentParser()",
            ]:
                errors.append("E_MAIN_POLICY_PREFIX")
            calls = sorted((node for node in ast.walk(main_node) if isinstance(node, ast.Call)),
                           key=lambda node: (node.lineno, node.col_offset))
            call_names = [ast.unparse(node.func) for node in calls]
            if call_names[:2] != ["source_policy", "git_argv_controls"] or \
                    "argparse.ArgumentParser" not in call_names or \
                    call_names.index("source_policy") > call_names.index("argparse.ArgumentParser"):
                errors.append("E_POLICY_ORDER")
    return errors


def source_policy_controls(builder_source: str, validator_source: str) -> int:
    snippets = [
        "import subprocess as sp", "from pathlib import Path as P",
        "def nested():\n    import socket", "runner = subprocess.run",
        "runner = getattr(subprocess, 'run')", "subprocess.__getattribute__('run')",
        "__import__('os')", "(lambda: 1)()",
        "subprocess.run(['x'], shell=True)", "subprocess.run(['x'], shell=bool(1))",
        "subprocess.run(['x'], **{'shell': True})", "subprocess.Popen(['x'])",
        "os.system('x')", "Path('x').open('w')", "Path('x').touch()",
        "Path('x').write_text('x')", "writer = Path('x').write_bytes",
        "Path(r'\\\\server\\share\\x').read_bytes()", "argparse.FileType('w')",
        "argparse.ArgumentParser(fromfile_prefix_chars='@')", "reader = git_bytes",
        "git_bytes(['fetch'])", "source_policy = lambda: 23",
        "def git_argv_allowed(args):\n    return True\ngit_bytes(['fetch'])",
        "breakpoint()", "parser.fromfile_prefix_chars = '@'", "del source_policy",
        "match (lambda: 23):\n    case source_policy:\n        pass",
        "match {}:\n    case {**source_policy}:\n        pass",
        "match []:\n    case [*source_policy]:\n        pass",
        "try:\n    pass\nexcept Exception as source_policy:\n    pass",
        "all = lambda value: True", "bool = lambda value: True", "FINAL_PATHS = ()",
        "AUTHORITY_KEYS = ()", "MAX_JSON_BYTES = 10 ** 100",
        "if True:\n    FINAL_PATHS = ()",
    ]
    passed = 0
    for index, snippet in enumerate(snippets):
        candidate = validator_source + "\n" + snippet + "\n"
        require(bool(source_policy_errors(candidate, "validator")),
                "E_SOURCE_POLICY_CONTROL", str(index))
        passed += 1
    builder_snippets = [
        "io.FileIO('x', 'w').write(b'evil')", "breakpoint()",
        "parser.fromfile_prefix_chars = '@'", "git_bytes(['clean', '-fd'])",
        "(ROOT / 'x').move(ROOT / 'outside')",
        "(ROOT / r'\\\\server\\share\\x').stat()",
    ]
    for index, snippet in enumerate(builder_snippets):
        candidate = builder_source + "\n" + snippet + "\n"
        require(bool(source_policy_errors(candidate, "builder")),
                "E_BUILDER_SOURCE_POLICY_CONTROL", str(index))
        passed += 1
    reordered = validator_source.replace(
        "source_negative = source_policy()\n        git_controls = git_argv_controls()",
        "git_controls = git_argv_controls()\n        source_negative = source_policy()",
    )
    require(reordered != validator_source and bool(source_policy_errors(reordered, "validator")),
            "E_SOURCE_POLICY_ORDER_CONTROL")
    decorated = validator_source.replace(
        "def source_policy() -> int:",
        "@lambda original: (lambda: 38)\ndef source_policy() -> int:",
    )
    require(decorated != validator_source and bool(source_policy_errors(decorated, "validator")),
            "E_SOURCE_POLICY_DECORATOR_CONTROL")
    dead_order = validator_source.replace(
        "    try:\n        source_negative = source_policy()\n"
        "        git_controls = git_argv_controls()\n"
        "        parser = argparse.ArgumentParser()",
        "    if False:\n        source_negative = source_policy()\n"
        "        git_controls = git_argv_controls()\n"
        "    try:\n        source_negative = 0\n"
        "        git_controls = 0\n"
        "        parser = argparse.ArgumentParser()",
    )
    require(dead_order != validator_source and
            bool(source_policy_errors(dead_order, "validator")),
            "E_SOURCE_POLICY_DEAD_ORDER_CONTROL")
    eager_default = validator_source.replace(
        "def control_documents() -> None:",
        "def control_documents(_preview=builder_preview()) -> None:",
    )
    require(eager_default != validator_source and
            bool(source_policy_errors(eager_default, "validator")),
            "E_SOURCE_POLICY_EAGER_DEFAULT_CONTROL")
    git_toctou = builder_source.replace(
        '    require(git_argv_allowed(tuple(args)), "E_GIT_ARGV")',
        '    require(git_argv_allowed(tuple(args)), "E_GIT_ARGV")\n'
        '    args[:] = ["clean", "-fd"]',
    )
    require(git_toctou != builder_source and
            bool(source_policy_errors(git_toctou, "builder")),
            "E_SOURCE_POLICY_GIT_TOCTOU_CONTROL")
    write_toctou = builder_source.replace(
        "    target = ROOT / path",
        "    path = '//server/share/outside'\n    target = ROOT / path",
    )
    require(write_toctou != builder_source and
            bool(source_policy_errors(write_toctou, "builder")),
            "E_SOURCE_POLICY_WRITE_TOCTOU_CONTROL")
    read_toctou = validator_source.replace(
        "def load_outputs() -> tuple[dict[str, Any], dict[str, Any], int, int]:",
        "def load_outputs() -> tuple[dict[str, Any], dict[str, Any], int, int]:\n"
        "    MATRIX = '//server/share/payload'",
    )
    require(read_toctou != validator_source and
            bool(source_policy_errors(read_toctou, "validator")),
            "E_SOURCE_POLICY_READ_TOCTOU_CONTROL")
    path_replace = builder_source.replace(
        "os.replace(temporary, target)",
        "os.replace(temporary, target)\n    target.replace('outside')",
    )
    second_replace = builder_source.replace(
        "os.replace(temporary, target)",
        "os.replace(temporary, target)\n    os.replace('victim', 'outside')",
    )
    require(path_replace != builder_source and bool(source_policy_errors(path_replace, "builder")),
            "E_SOURCE_POLICY_PATH_REPLACE_CONTROL")
    require(second_replace != builder_source and
            bool(source_policy_errors(second_replace, "builder")),
            "E_SOURCE_POLICY_SECOND_REPLACE_CONTROL")
    return passed + 9


def source_policy() -> int:
    builder_raw = (ROOT / BUILDER).read_bytes()
    validator_raw = (ROOT / VALIDATOR).read_bytes()
    builder_source = builder_raw.decode("utf-8")
    validator_source = validator_raw.decode("utf-8")
    builder_errors = source_policy_errors(builder_source, "builder")
    validator_errors = source_policy_errors(validator_source, "validator")
    require(not builder_errors, "E_BUILDER_SOURCE_POLICY", ",".join(builder_errors[:5]))
    require(not validator_errors, "E_VALIDATOR_SOURCE_POLICY", ",".join(validator_errors[:5]))
    require(neutral_source_hash(builder_raw, "builder") == BUILDER_SOURCE_SHA256_LF,
            "E_BUILDER_SOURCE_HASH")
    require(neutral_source_hash(validator_raw, "validator") == VALIDATOR_NEUTRAL_SHA256_LF,
            "E_VALIDATOR_SOURCE_HASH")
    return source_policy_controls(builder_source, validator_source)


def git_argv_controls() -> int:
    good = [
        ("show", f"{EXPECTED_PARENT}:{PARENT_INPUTS[0]}"),
        ("show", f"{SUPPLEMENTAL_COMMIT}:{SUPPLEMENTAL_PATHS[0]}"),
        ("ls-tree", SUPPLEMENTAL_COMMIT, "--", SUPPLEMENTAL_PATHS[0]),
        ("ls-tree", BASELINE, "--", SUPPLEMENTAL_PATHS[0]),
        ("rev-parse", "HEAD"), ("symbolic-ref", "--quiet", "--short", "HEAD"),
        ("status", "--porcelain=v1", "--untracked-files=all"),
        ("diff", "--cached", "--name-status", "--no-renames", EXPECTED_PARENT, "--"),
        ("diff", "--name-only", PROTECTED_TIP, EXPECTED_PARENT, "--", "Claude"),
        ("show", "--no-patch", "--format=%P", EXPECTED_PARENT),
        ("diff-tree", "--no-commit-id", "--name-status", "-r", "--no-renames",
         EXPECTED_PARENT, "--"),
        ("ls-tree", EXPECTED_PARENT, "--", *FINAL_PATHS),
        ("ls-files", "--stage", "--", *FINAL_PATHS),
        ("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"),
    ]
    bad = [
        (), ("fetch",), ("status", "--short"), ("show", f"main:{PARENT_INPUTS[0]}"),
        ("show", f"{EXPECTED_PARENT}:{SUPPLEMENTAL_PATHS[0]}"),
        ("ls-tree", SUPPLEMENTAL_COMMIT, "--", "Claude"),
        ("diff", "--name-only", PROTECTED_TIP, EXPECTED_PARENT, "--", "Claude", "Codex"),
        ("show", "--no-patch", "--format=%P", "HEAD"),
        ("diff-tree", "--no-commit-id", "--name-status", "-r", EXPECTED_PARENT, "--"),
        ("ls-tree", EXPECTED_PARENT, "--", *FINAL_PATHS[:-1]),
        ("ls-remote", "--upload-pack=x", "origin", f"refs/heads/{BRANCH}"),
        ("ls-remote", "--heads", "origin", "refs/heads/main"),
        ("rev-parse", "HEAD\nfetch"), ("show", "--output=x"),
    ]
    require(all(git_argv_allowed(case) for case in good), "E_GIT_ARGV_GOOD_CONTROL")
    require(all(not git_argv_allowed(case) for case in bad), "E_GIT_ARGV_BAD_CONTROL")
    return len(good) + len(bad)


def parse_status(raw: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not raw:
        return rows
    for line in raw.splitlines():
        require(len(line) >= 4, "E_STATUS_PARSE")
        code = line[:2]
        path = line[3:].replace("\\", "/")
        require(path not in rows, "E_STATUS_DUPLICATE")
        rows[path] = code
    return rows


def parse_name_status(raw: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not raw:
        return rows
    for line in raw.splitlines():
        parts = line.split("\t")
        require(len(parts) == 2 and parts[0] in {"A", "M"}, "E_DIFF_PARSE")
        path = parts[1].replace("\\", "/")
        require(path not in rows, "E_DIFF_DUPLICATE")
        rows[path] = parts[0]
    return rows


def require_index_modes() -> None:
    raw = git_text(["ls-files", "--stage", "--", *FINAL_PATHS], "E_INDEX_MODES")
    rows: dict[str, str] = {}
    for line in raw.splitlines():
        match = re.fullmatch(r"([0-9]{6}) ([0-9a-f]{40}) 0\t(.+)", line)
        require(match is not None, "E_INDEX_MODE_PARSE")
        rows[match.group(3).replace("\\", "/")] = match.group(1)
    require(rows == {path: "100644" for path in FINAL_PATHS}, "E_INDEX_MODES")


def require_tree_modes(commit: str) -> None:
    raw = git_text(["ls-tree", commit, "--", *FINAL_PATHS], "E_TREE_MODES")
    rows: dict[str, str] = {}
    for line in raw.splitlines():
        match = re.fullmatch(r"([0-9]{6}) blob [0-9a-f]{40}\t(.+)", line)
        require(match is not None, "E_TREE_MODE_PARSE")
        rows[match.group(2).replace("\\", "/")] = match.group(1)
    require(rows == {path: "100644" for path in FINAL_PATHS}, "E_TREE_MODES")


def repository_guard(mode: str, commit: str | None) -> None:
    head = git_text(["rev-parse", "HEAD"], "E_HEAD")
    require(git_text(["symbolic-ref", "--quiet", "--short", "HEAD"], "E_BRANCH") == BRANCH,
            "E_BRANCH")
    if mode in {"content", "staged"}:
        require(head == EXPECTED_PARENT, "E_HEAD_PARENT")
    else:
        require(commit is not None and re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
                "E_COMMIT_ARG")
        require(head == commit, "E_HEAD_COMMIT")
    require(git_text(["rev-parse", "refs/remotes/origin/main"]) == MAIN_TIP,
            "E_MAIN_TIP")
    require(git_text(["rev-parse", "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"]) ==
            PROTECTED_TIP, "E_PROTECTED_TIP")
    compare_head = commit if commit is not None else EXPECTED_PARENT
    claude = git_text(["diff", "--name-only", PROTECTED_TIP, compare_head, "--", "Claude"])
    require(claude == "", "E_CLAUDE_DRIFT")

    status_raw = git_bytes(
        ["status", "--porcelain=v1", "--untracked-files=all"], "E_STATUS"
    ).decode("utf-8").rstrip("\r\n")
    status = parse_status(status_raw)
    if mode == "content":
        expected = {path: ("??" if index < 5 else " M")
                    for index, path in enumerate(FINAL_PATHS)}
        require(status == expected, "E_CONTENT_STATUS")
        require(git_text(["diff", "--cached", "--name-only"]) == "", "E_CONTENT_STAGED")
    elif mode == "staged":
        expected = {path: ("A " if index < 5 else "M ")
                    for index, path in enumerate(FINAL_PATHS)}
        require(status == expected, "E_STAGED_STATUS")
        diff = parse_name_status(git_text(["diff", "--cached", "--name-status",
                                           "--no-renames", EXPECTED_PARENT, "--"]))
        require(diff == FINAL_STATUS, "E_STAGED_DIFF")
        require(git_text(["diff", "--name-only"]) == "", "E_STAGED_WORKTREE")
        require_index_modes()
    else:
        require(status == {}, "E_PERSISTENCE_DIRTY")
        assert commit is not None
        parent = git_text(["show", "--no-patch", "--format=%P", commit], "E_COMMIT_PARENT")
        subject = git_text(["show", "--no-patch", "--format=%s", commit], "E_COMMIT_SUBJECT")
        require(parent == EXPECTED_PARENT, "E_COMMIT_PARENT")
        require(subject == SUBJECT, "E_COMMIT_SUBJECT")
        diff = parse_name_status(git_text(["diff-tree", "--no-commit-id", "--name-status",
                                           "-r", "--no-renames", commit, "--"]))
        require(diff == FINAL_STATUS, "E_COMMIT_DIFF")
        require_tree_modes(commit)
        require(git_text(["rev-parse", "@{u}"]) == commit, "E_UPSTREAM")
        require(git_text(["rev-parse", f"refs/remotes/origin/{BRANCH}"]) == commit,
                "E_TRACKING")
        live = git_text(["ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"],
                        "E_LIVE_REMOTE")
        require(live == f"{commit}\trefs/heads/{BRANCH}", "E_LIVE_REMOTE")


def control_documents() -> None:
    checks = {
        RESULT: ["# Phase 067 Step 89 Fitting Evidence Authority Result", GATE,
                 EXPECTED_PARENT, SUBJECT, "P065-OBL-0054", "P066-OBL-0120",
                 "EXPLICITLY_BOUNDED_NOT_RESOLVED", "Step 90.1"],
        PARENT_LEDGER: [EXPECTED_PARENT, "Step 89", GATE, SUBJECT, "Step 90.1"],
        CANONICAL_LEDGER: [EXPECTED_PARENT, "Step 89", GATE, SUBJECT, "Step 90.1"],
        HANDOVER: [EXPECTED_PARENT, "Step 89", GATE, SUBJECT, "Step 90.1"],
    }
    for path, tokens in checks.items():
        raw = (ROOT / path).read_bytes()
        require(len(raw) <= 2_000_000, "E_CONTROL_BYTES", path)
        text = raw.decode("utf-8")
        for token in tokens:
            require(token in text, "E_CONTROL_TOKEN", path + ":" + token)
        lines = text.splitlines()

        def unique_line(prefix: str) -> str:
            matches = [line for line in lines if line.startswith(prefix)]
            require(len(matches) == 1, "E_CONTROL_CURRENT_LINE", path + ":" + prefix)
            return matches[0]

        if path in {PARENT_LEDGER, CANONICAL_LEDGER}:
            phase_row = unique_line("| 067 |")
            for token in ("Steps 82–88 persisted", "Step 89", "PASS_PENDING_PERSISTENCE",
                          EXPECTED_PARENT, SUBJECT, GATE, "Step 90.1"):
                require(token in phase_row, "E_CONTROL_PHASE_ROW", path + ":" + token)
            require("Step 88 numerical-guard impact audit pending persistence" not in phase_row,
                    "E_CONTROL_STALE_PHASE_ROW", path)
        if path == CANONICAL_LEDGER:
            step_row = unique_line("| Phase 067 Step 89 |")
            for token in ("PENDING_AT_PRECOMMIT_BY_DESIGN", "A/A/A/A/A/M/M/M",
                          EXPECTED_PARENT, SUBJECT, GATE, PERSISTENCE, "Step 90.1"):
                require(token in step_row, "E_CONTROL_STEP_ROW", token)
        if path == HANDOVER:
            current = unique_line("19. 현재 Phase 상태:")
            current_state = unique_line("- Phase 067 plan activation은 ")
            table_row = unique_line("| Phase 067 Step 89 |")
            for line in (current, current_state, table_row):
                for token in ("Step 89", GATE, "PASS_PENDING_PERSISTENCE", "Step 90.1"):
                    require(token in line, "E_CONTROL_HANDOVER_CURRENT", token)
            require(EXPECTED_PARENT in current and PERSISTENCE in current_state and
                    EXPECTED_PARENT in table_row and SUBJECT in table_row,
                    "E_CONTROL_HANDOVER_IDENTITY")
            require("Step 89 remains blocked" not in current_state and
                    "Step 88 is current" not in current_state,
                    "E_CONTROL_HANDOVER_STALE")
        if path == RESULT:
            require(text.startswith("# Phase 067 Step 89 Fitting Evidence Authority Result\n\n"),
                    "E_CONTROL_RESULT_HEADING")
            gate_index = text.find("## Gate and Next Condition")
            require(gate_index >= 0, "E_CONTROL_RESULT_GATE_SECTION")
            gate_section = text[gate_index:]
            for token in (GATE, PERSISTENCE, "Step 90.1"):
                require(token in gate_section, "E_CONTROL_RESULT_GATE", token)


def main() -> int:
    try:
        source_negative = source_policy()
        git_controls = git_argv_controls()
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--verify-content", action="store_true")
        group.add_argument("--verify-staged", action="store_true")
        group.add_argument("--verify-persistence", metavar="COMMIT")
        args = parser.parse_args()
        mode = "content" if args.verify_content else \
            "staged" if args.verify_staged else "persistence"
        commit = args.verify_persistence if mode == "persistence" else None
        matrix, runtime, nodes, depth = load_outputs()
        validate_core(matrix, runtime)
        validate_preview(matrix, runtime)
        negatives = negative_controls(matrix, runtime)
        json_negative = json_controls()
        control_documents()
        repository_guard(mode, commit)
    except ValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"PASS_P067_STEP89_SOURCE_POLICY {source_negative}/{source_negative} "
          f"git_argv={git_controls}/{git_controls}")
    print(f"PASS_P067_STEP89_CONTROLS semantic={negatives}/{negatives} "
          f"json={json_negative}/{json_negative} nodes={nodes} depth={depth}")
    print(PERSISTENCE if mode == "persistence" else GATE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
