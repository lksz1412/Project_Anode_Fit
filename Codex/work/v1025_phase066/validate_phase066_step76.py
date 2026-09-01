from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import math
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
BUILDER_PATH = "Codex/work/v1025_phase066/build_phase066_step76.py"
VALIDATOR_PATH = "Codex/work/v1025_phase066/validate_phase066_step76.py"
DELTA_PATH = "Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json"
ATTESTATION_PATH = "Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json"
RESULT_PATH = "Codex/results/PHASE_066_STEP_076_SOURCE_PROCESS_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"

EXPECTED_PARENT = "f9ee0599ff07d36e4b23547a835549552a51ce26"
EXPECTED_SUBJECT = "audit(phase066): freeze v1025 source process delta"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{BRANCH}"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PROCESS_TIP = "e3e1a634f34b711aa4803fd190fe9120f1755f13"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GATE = "PASS_P066_STEP76_SOURCE_PROCESS"
PERSISTENCE = "PASS_P066_STEP76_PERSISTENCE"
VALIDATOR_SOURCE_POLICY_SHA256_LF = "99aa4786f390e7c52fb83064e09ff1e44bbe7e2afcf731afb144959a8133e45e"
BUILDER_SOURCE_POLICY_SHA256_LF = "aadc318c84d374cfcc8e7d10ac44e7b6a41fc5af41eac793af69cef3b8e2213f"

FINAL_PATHS = [
    BUILDER_PATH,
    VALIDATOR_PATH,
    DELTA_PATH,
    ATTESTATION_PATH,
    RESULT_PATH,
    PARENT_LEDGER_PATH,
    ACTIVE_LEDGER_PATH,
    HANDOVER_PATH,
]
FINAL_SET = set(FINAL_PATHS)
FINAL_STATUS = {
    BUILDER_PATH: "A", VALIDATOR_PATH: "A", DELTA_PATH: "A", ATTESTATION_PATH: "A",
    RESULT_PATH: "A", PARENT_LEDGER_PATH: "M", ACTIVE_LEDGER_PATH: "M", HANDOVER_PATH: "M",
}
ALLOWED_IMPORTS = {
    "__future__", "argparse", "ast", "collections", "copy", "hashlib", "importlib",
    "io", "json", "math", "os", "pathlib", "re", "subprocess", "sys", "types",
    "typing", "PIL", "pypdf",
}
FORBIDDEN_CALLS = {"eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr", "input", "open"}
WRITE_METHODS = {"write_text", "write_bytes", "unlink", "rename", "touch", "mkdir", "rmdir"}
FORBIDDEN_ATTRIBUTES = WRITE_METHODS | {"open", "system", "popen", "import_module"}


class ValidationFailure(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationFailure(code, detail)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True,
                       allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")


def semantic_hash(value: dict[str, Any]) -> str:
    clone = dict(value)
    clone["semantic_sha256"] = ""
    return sha256(canonical_bytes(clone))


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_JSON_DUPLICATE", key)
        result[key] = value
    return result


def _constant(token: str) -> None:
    raise ValidationFailure("E_JSON_NONFINITE", token)


def walk_json(value: Any, depth: int = 0) -> tuple[int, int]:
    require(depth <= 32, "E_JSON_DEPTH", str(depth))
    if isinstance(value, dict):
        total, maximum = 1, depth
        for key, nested in value.items():
            require(isinstance(key, str), "E_JSON_KEY")
            count, observed = walk_json(nested, depth + 1)
            total += count
            maximum = max(maximum, observed)
        return total, maximum
    if isinstance(value, list):
        require(len(value) <= 10000, "E_JSON_ARRAY", str(len(value)))
        total, maximum = 1, depth
        for nested in value:
            count, observed = walk_json(nested, depth + 1)
            total += count
            maximum = max(maximum, observed)
        return total, maximum
    if isinstance(value, float):
        require(math.isfinite(value), "E_JSON_NONFINITE")
    require(value is None or isinstance(value, (str, int, float, bool)), "E_JSON_TYPE")
    return 1, depth


def strict_load(raw: bytes, label: str) -> tuple[dict[str, Any], int, int]:
    require(len(raw) <= 20_000_000, "E_JSON_SIZE", label)
    require(b"\r" not in raw and raw.endswith(b"\n"), "E_JSON_LF", label)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValidationFailure("E_JSON_PARSE", f"{label}:{error}") from error
    require(isinstance(value, dict), "E_JSON_ROOT", label)
    nodes, depth = walk_json(value)
    require(canonical_bytes(value) == raw, "E_JSON_CANONICAL", label)
    require(value.get("semantic_sha256") == semantic_hash(value), "E_JSON_SEMANTIC", label)
    return value, nodes, depth


def load_builder() -> ModuleType:
    path = ROOT / BUILDER_PATH
    spec = importlib.util.spec_from_file_location("p066_step76_builder", path)
    require(spec is not None and spec.loader is not None, "E_BUILDER_SPEC")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def neutralized_source(raw: bytes, constant: str) -> bytes:
    pattern = re.compile(rb'(?m)^' + re.escape(constant.encode("ascii")) + rb' = "[0-9a-f]{64}"$')
    replacement = constant.encode("ascii") + b' = "' + (b"0" * 64) + b'"'
    updated, count = pattern.subn(replacement, raw)
    require(count == 1, "E_SOURCE_POLICY_PIN", constant)
    return updated


class PolicyVisitor(ast.NodeVisitor):
    def __init__(self, kind: str) -> None:
        self.kind = kind
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.subprocess_sites: list[tuple[str, ast.Call]] = []

    @property
    def owner(self) -> str:
        return self.stack[-1] if self.stack else "<module>"

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if alias.name.split(".")[0] not in ALLOWED_IMPORTS:
                self.errors.append(f"import:{alias.name}")
            if alias.asname:
                self.errors.append(f"import-alias:{alias.name}")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        root = (node.module or "").split(".")[0]
        if root not in ALLOWED_IMPORTS:
            self.errors.append(f"from:{node.module}")
        if root in {"subprocess", "os", "importlib"}:
            self.errors.append(f"sensitive-from:{node.module}")
        for alias in node.names:
            if alias.asname:
                self.errors.append(f"from-alias:{node.module}:{alias.name}")

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
            self.errors.append(f"call:{node.func.id}:{self.owner}")
        if isinstance(node.func, ast.Attribute):
            name = node.func.attr
            if name in {"Popen", "call", "check_call", "check_output", "run"}:
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" and name == "run":
                    self.subprocess_sites.append((self.owner, node))
                else:
                    self.errors.append(f"process:{name}:{self.owner}")
            if name in WRITE_METHODS:
                allowed = self.kind == "builder" and self.owner == "atomic_collect_pair"
                if not allowed:
                    self.errors.append(f"write:{name}:{self.owner}")
            if name == "replace" and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                if not (self.kind == "builder" and self.owner == "atomic_collect_pair"):
                    self.errors.append(f"os-replace:{self.owner}")
            if name == "open" and not (isinstance(node.func.value, ast.Name) and
                                        node.func.value.id == "Image"):
                self.errors.append(f"attribute-open:{self.owner}")
            if name in {"system", "popen"} and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                self.errors.append(f"os-process:{name}:{self.owner}")
            if name == "import_module" and isinstance(node.func.value, ast.Name) and node.func.value.id == "importlib":
                self.errors.append(f"dynamic-import:{self.owner}")
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Attribute) and node.value.attr in FORBIDDEN_ATTRIBUTES:
            self.errors.append(f"sensitive-alias:{node.value.attr}:{self.owner}")
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.value, ast.Attribute) and node.value.attr in FORBIDDEN_ATTRIBUTES:
            self.errors.append(f"sensitive-alias:{node.value.attr}:{self.owner}")
        self.generic_visit(node)


def source_policy_errors(source: str, kind: str) -> list[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ["syntax"]
    visitor = PolicyVisitor(kind)
    visitor.visit(tree)
    expected_owner = "git"
    if len(visitor.subprocess_sites) != 1:
        visitor.errors.append(f"subprocess-count:{len(visitor.subprocess_sites)}")
    else:
        owner, call = visitor.subprocess_sites[0]
        if owner != expected_owner:
            visitor.errors.append(f"subprocess-owner:{owner}")
        keywords = {keyword.arg: keyword.value for keyword in call.keywords if keyword.arg}
        shell = keywords.get("shell")
        check = keywords.get("check")
        if not isinstance(shell, ast.Constant) or shell.value is not False:
            visitor.errors.append("shell-false")
        if not isinstance(check, ast.Constant) or check.value is not False:
            visitor.errors.append("check-false")
        if not call.args or not isinstance(call.args[0], (ast.List, ast.Tuple)):
            visitor.errors.append("subprocess-fixed-list")
        else:
            command = call.args[0]
            first = command.elts[0] if command.elts else None
            if not isinstance(first, ast.Constant) or first.value != "git":
                visitor.errors.append("subprocess-non-git")
    return visitor.errors


def verify_source_policy() -> None:
    builder_raw = (ROOT / BUILDER_PATH).read_bytes()
    validator_raw = (ROOT / VALIDATOR_PATH).read_bytes()
    require(builder_raw == lf_bytes(builder_raw) and validator_raw == lf_bytes(validator_raw),
            "E_SOURCE_LF")
    require(not source_policy_errors(builder_raw.decode("utf-8"), "builder"), "E_BUILDER_POLICY")
    require(not source_policy_errors(validator_raw.decode("utf-8"), "validator"), "E_VALIDATOR_POLICY")
    require(sha256(neutralized_source(builder_raw, "BUILDER_SOURCE_POLICY_SHA256_LF")) ==
            BUILDER_SOURCE_POLICY_SHA256_LF, "E_BUILDER_POLICY_HASH")
    require(sha256(neutralized_source(validator_raw, "VALIDATOR_SOURCE_POLICY_SHA256_LF")) ==
            VALIDATOR_SOURCE_POLICY_SHA256_LF, "E_VALIDATOR_POLICY_HASH")


def validate_git_args(args: tuple[str, ...]) -> None:
    require(args, "E_GIT_EMPTY")
    forbidden = {"-c", "--config-env", "--upload-pack", "--receive-pack", "--exec-path",
                 "--ext-diff", "--textconv", "reset", "checkout", "switch", "commit", "push",
                 "fetch", "merge", "rebase", "update-ref", "clean", "rm", "mv"}
    require(not any(arg in forbidden for arg in args), "E_GIT_FORBIDDEN", repr(args))
    require(not any(arg.startswith(("--config=", "--git-dir", "--work-tree", "--output",
                                    "--textconv="))
                    for arg in args), "E_GIT_OPTION", repr(args))
    require(args[0] in {"cat-file", "rev-parse", "log", "show", "diff-tree", "ls-tree",
                                "status", "diff", "ls-files", "ls-remote", "show-ref"},
            "E_GIT_VERB", args[0])
    if args[0] == "ls-remote":
        allowed_remote = (args == ("ls-remote", "--get-url", "origin") or
                          (len(args) == 4 and args[1:3] == ("--heads", "origin") and
                           args[3].startswith("refs/heads/") and "\n" not in args[3] and
                           "\r" not in args[3]))
        require(allowed_remote, "E_GIT_REMOTE", repr(args))


def git(*args: str, binary: bool = False, check: bool = True) -> bytes | str:
    validate_git_args(tuple(args))
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False,
                            shell=False, timeout=90)
    if check:
        require(result.returncode == 0, "E_GIT", result.stderr.decode("utf-8", "replace"))
    return result.stdout if binary else result.stdout.decode("utf-8").rstrip("\r\n")


def parse_name_status(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        status, path = line.split("\t", 1)
        require(status in {"A", "M"} and path not in result, "E_STATUS_PARSE", line)
        result[path] = status
    return result


def parse_porcelain(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        require(len(line) >= 4, "E_PORCELAIN", line)
        status, path = line[:2], line[3:]
        result[path] = status
    return result


def artifact_errors(delta: dict[str, Any], attestation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    def check(condition: bool, label: str) -> None:
        if not condition:
            errors.append(label)
    for document, artifact in ((delta, "PHASE_066_SOURCE_PROCESS_DELTA"),
                               (attestation, "PHASE_066_COMPLETE_READ_ATTESTATION")):
        check(document.get("schema_version") == "P066-S76-1", f"schema:{artifact}")
        check(document.get("artifact") == artifact, f"artifact:{artifact}")
        check(document.get("phase") == 66 and document.get("step") == 76, f"phase:{artifact}")
        check(document.get("baseline_commit") == BASELINE and document.get("process_tip") == PROCESS_TIP,
              f"baseline:{artifact}")
        check(document.get("expected_parent") == EXPECTED_PARENT and
              document.get("expected_subject") == EXPECTED_SUBJECT, f"commit:{artifact}")
        check(document.get("gate") == GATE and document.get("persistence_terminal") == PERSISTENCE,
              f"gate:{artifact}")
        check(document.get("result_first") is True and document.get("json_pair_last") is True,
              f"order:{artifact}")
        authority = document.get("authority", {})
        check(authority == {"canonical_release": False, "external_scientific": False,
                            "fit_reproduced": False, "inventory_and_read_coverage": True,
                            "material_authority": False, "optimizer_state_recovered": False,
                            "publication_ready": False, "v1025_2_build_evidence": False},
              f"authority:{artifact}")
    summary = delta.get("source_summary", {})
    check(summary.get("slice_indices_zero_based") == [1087, 1519], "slice")
    check((summary.get("occurrences"), summary.get("unique_blobs"),
           summary.get("occurrence_bytes"), summary.get("unique_bytes")) ==
          (433, 167, 26391541, 12483701), "source-counts")
    check(summary.get("versions") == {"v1.0.25": 143, "v1.0.25.1": 144, "v1.0.25.2": 146},
          "versions")
    check(summary.get("unique_review_modes") == {"FULL_IMAGE": 3, "FULL_PDF": 6, "FULL_TEXT": 158},
          "modes")
    check((summary.get("unique_text_lines"), summary.get("unique_pdf_pages")) == (30597, 308),
          "extents")
    check((summary.get("path_set_sha256"), summary.get("path_blob_sha256"),
           summary.get("unique_blob_sha256")) ==
          ("3c9bf954a5db4df5ce01a96ff8834f9e9284e6e35fdcecbfae0c3ae6b430b382",
           "b3620bf1a76758cad818e9ea7ece5441ea88b86f8f030bb715f48e054086655c",
           "f1982cf050f88b7145d5ea1a6afdf124316da1332afec9028ae6119730080bfa"), "set-hashes")
    occurrences = delta.get("occurrences", [])
    check(len(occurrences) == 433, "occurrence-count")
    check([row.get("manifest_index") for row in occurrences] == list(range(1087, 1520)), "indices")
    check(len({row.get("path") for row in occurrences}) == 433, "occurrence-unique")
    unique = attestation.get("machine_blob_attestations", [])
    check(len(unique) == 167 and len({row.get("blob_sha1") for row in unique}) == 167, "unique-blobs")
    check(Counter(row.get("observed_type") for row in unique) ==
          {"UTF8_TEXT": 158, "PDF": 6, "PNG": 3}, "observed-types")
    discrepancies = [row for row in unique if row.get("classification_discrepancy") is True]
    check(len(discrepancies) == 1 and discrepancies[0].get("blob_sha1") ==
          "d46e5c2d147c8c16b7c1fdde132fc41c71d6a1b1" and
          discrepancies[0].get("observed_semantic_kind") == "TEXT_POINTER" and
          discrepancies[0].get("declared_extensions") == ["json"], "classification")
    check(all(row.get("machine_coverage", {}).get("status") == "MACHINE_READ_FULL" for row in unique),
          "machine-read")
    human_statuses = Counter(row.get("human_coverage", {}).get("status") for row in unique)
    check(human_statuses == {"READ_FULL": 166, "MACHINE_COMPLETE_HUMAN_AUTHORED_READ": 1},
          "human-read")
    bindings = attestation.get("occurrence_bindings", [])
    check(len(bindings) == 433 and len({row.get("manifest_index") for row in bindings}) == 433,
          "bindings")
    check([{key: row.get(key) for key in ("manifest_index", "path", "blob_sha1", "attestation_id")}
           for row in occurrences] == bindings, "binding-projection")
    deltas = delta.get("pairwise_deltas", [])
    expected_delta = [("v1.0.25", "v1.0.25.1", {"shared": 143, "same": 133, "changed": 10,
                                                  "added": 1, "removed": 0}),
                      ("v1.0.25.1", "v1.0.25.2", {"shared": 144, "same": 133, "changed": 11,
                                                    "added": 2, "removed": 0}),
                      ("v1.0.25", "v1.0.25.2", {"shared": 143, "same": 127, "changed": 16,
                                                  "added": 3, "removed": 0})]
    check([(row.get("from_version"), row.get("to_version"), row.get("counts")) for row in deltas] ==
          expected_delta, "delta-counts")
    check(all(len(row.get("records", [])) == row["counts"]["shared"] + row["counts"]["added"] +
              row["counts"]["removed"] for row in deltas), "delta-records")
    check(all(record.get("new_provenance") is not None
              for row in deltas for record in row.get("records", []) if record.get("status") in {"CHANGED", "ADDED"}),
          "new-provenance")
    check(all(record.get("old_provenance") is not None
              for row in deltas for record in row.get("records", []) if record.get("status") in {"CHANGED", "REMOVED"}),
          "old-provenance")
    stale = delta.get("stale_pdf_pairs", [])
    check(len(stale) == 3 and all(row.get("pdf_blob_equal") is True and
                                  row.get("candidate_tex_blob_equal") is False and
                                  row.get("v1025_2_build_evidence") is False for row in stale), "stale-pdf")
    narrative = delta.get("narrative", {})
    check((narrative.get("manifest_documents"), narrative.get("manifest_lines"),
           narrative.get("supplemental_documents"), narrative.get("supplemental_lines"),
           narrative.get("expanded_documents"), narrative.get("expanded_lines")) ==
          (40, 9019, 2, 655, 42, 9674), "narrative")
    process = delta.get("process", {})
    check((process.get("release", {}).get("count"), process.get("routed", {}).get("count"),
           len(process.get("records", []))) == (17, 20, 20), "process")
    check(process.get("release", {}).get("sha256_lf") ==
          "f09417ef085ee7139fa11869f6f123937d6492dcc53d1f0b51e71a2c8a124860", "process-hash")
    check(process.get("routed", {}).get("sha256_lf") ==
          "57062f623809de1f3fb66b8241117363a0ec18626bc58a40f4f0e41cbed93418", "routed-hash")
    check(Counter(row.get("human_coverage", {}).get("status") for row in process.get("records", [])) ==
          {"COMPLETE_BY_TRANSITIVE_CONTENT_BINDING": 14, "READ_FULL": 6}, "process-read")
    expected_process_attestations = {
        "batches": process.get("review_batches", []),
        "records": [{"ordinal": row.get("ordinal"), "commit": row.get("commit"),
                     "patch_sha256_lf": row.get("patch_sha256_lf"),
                     "patch_lines": row.get("patch_lines"),
                     "human_coverage": row.get("human_coverage")}
                    for row in process.get("records", [])],
    }
    check(attestation.get("process_read_attestations") == expected_process_attestations,
          "process-attestations")
    routes = delta.get("phase057_routes", {})
    check((routes.get("document_count"), routes.get("document_lines"), routes.get("ao_aw_count"),
           routes.get("ay_count"), routes.get("ay_new_count"), routes.get("duplicate_count"),
           routes.get("ax_scope_leak_count")) == (10, 1919, 95, 10, 0, 0, 0), "routes")
    route_records = routes.get("records", [])
    check(len(route_records) == 105 and len({row.get("observation_id") for row in route_records}) == 105,
          "route-records")
    ay = [row for row in route_records if 395 <= row.get("numeric_id", -1) <= 404]
    check(Counter(row.get("current_state") for row in ay) == {"OPEN_CARRY": 8, "BOUNDED_HISTORICAL": 2},
          "ay-state")
    check(all(row.get("external_authority_promoted") is False for row in route_records), "route-authority")
    check(attestation.get("narrative_document_attestations") == narrative, "narrative-attestations")
    check(attestation.get("routing_observation_attestations") ==
          {"documents": routes.get("documents", []),
           "intent_ids": [row.get("observation_id") for row in route_records]},
          "route-attestations")
    coverage = attestation.get("coverage_summary", {})
    check(coverage == {"image_blobs": 3, "images_visual_inspected": 3, "inspection_errors": 0,
                       "narrative_documents": 42, "narrative_lines": 9674, "output_truncation_unresolved": 0,
                       "pdf_blobs": 6, "pdf_pages": 308, "release_commits": 17,
                       "routed_commits": 20, "routing_documents": 10, "routing_duplicate_ids": 0,
                       "routing_intent_ids": 105, "source_occurrence_orphans": 0,
                       "source_occurrences_read": 433, "source_occurrences_total": 433,
                       "text_blobs": 158, "text_lines": 30597, "unique_blobs_partial": 0,
                       "unique_blobs_read": 167, "unique_blobs_total": 167, "unique_blobs_unread": 0,
                       "unread_process_diffs": 0}, "coverage")
    check(attestation.get("delta_semantic_sha256") == delta.get("semantic_sha256"), "cross-semantic")
    expected_defects = [
        {"affected_items": 1, "blob_sha1": "4e379edfaf9bd6ca8fc1da32ac036fe84728744e",
         "defect_id": "P066-S76-DEFECT-001", "downstream_owner": "PHASE-089-LATEX-PDF-RELEASE-QA",
         "kind": "PDF_RIGHT_CLIPPING", "page": 50,
         "path": "Claude/docs/v1.0.25/ch1_graphite_v1.0.24.pdf", "status": "OPEN_ROUTED"},
        {"affected_items": 9, "blob_sha1": "4086482f28af182fb16fbbe02fd1f9f1cc52c69c",
         "defect_id": "P066-S76-DEFECT-002", "downstream_owner": "PHASE-089-LATEX-PDF-RELEASE-QA",
         "embedded_png_count": 9, "kind": "EMBEDDED_PNG_KOREAN_GLYPH_MISSING",
         "path": "Claude/docs/v1.0.25.2/results/KERNEL_COMPARISON_REPORT_v1025_2.html",
         "status": "OPEN_ROUTED"},
    ]
    check(delta.get("observed_defects") == expected_defects and
          attestation.get("observed_defects") == expected_defects, "defects")
    check(all(not value for value in attestation.get("validation", {}).values()), "attestation-zero")
    check(delta.get("validation") == {"authority_promotions": 0, "ay_new_duplicates": 0,
                                      "classification_discrepancies": 1,
                                      "duplicate_occurrences": 0, "occurrence_orphans": 0,
                                      "provenance_not_found": 0, "unread_process_patches": 0},
          "delta-zero")
    return errors


def verify_manifest_projection(builder: ModuleType, delta: dict[str, Any], attestation: dict[str, Any]) -> None:
    _, selected = builder.load_manifest()
    manifest_rows = [row for _, row in selected]
    occurrences = delta["occurrences"]
    require(len(manifest_rows) == len(occurrences) == 433, "E_MANIFEST_PROJECTION")
    for (index, source), record in zip(selected, occurrences):
        prefix = f"Claude/docs/{source['version']}/"
        expected = {"manifest_index": index, "ordinal": index + 1, "version": source["version"],
                    "path": source["path"], "relative_path": source["path"][len(prefix):],
                    "blob_sha1": source["blob_sha"], "git_mode": source["git_mode"],
                    "size_bytes": source["size_bytes"], "extension": source["extension"],
                    "role": source["role"], "review_mode": source["review_mode"],
                    "extent": source["extent"], "candidate_tex_paths": source.get("candidate_tex_paths", [])}
        require(all(record.get(key) == value for key, value in expected.items()),
                "E_MANIFEST_RECORD", source["path"])
    source_records = {row["blob_sha1"]: row for row in attestation["machine_blob_attestations"]}
    for blob, record in source_records.items():
        path = record["occurrence_paths"][0]
        raw = builder.git_blob(BASELINE, path)
        require(builder.git_blob_id(BASELINE, path) == blob and sha256(raw) == record["raw_sha256"] and
                 len(raw) == record["size_bytes"], "E_SOURCE_BYTES", blob)
    rebuilt_sources, rebuilt_bindings, rebuilt_batches = builder.inspect_unique_sources(selected, True)
    require(rebuilt_sources == attestation["machine_blob_attestations"], "E_SOURCE_ATTESTATION_BINDING")
    require(rebuilt_batches == attestation["text_review_batches"], "E_TEXT_BATCH_BINDING")
    require(rebuilt_bindings == {row["blob_sha1"]: row["attestation_id"] for row in rebuilt_sources},
            "E_SOURCE_BINDING_MAP")
    rebuilt_deltas = builder.pairwise_deltas(occurrences)
    require(rebuilt_deltas == delta["pairwise_deltas"], "E_PROVENANCE_BINDING")
    rebuilt_routes = builder.phase057_routes(True)
    require(rebuilt_routes == delta["phase057_routes"], "E_ROUTE_BINDING")


def verify_process_projection(builder: ModuleType, delta: dict[str, Any]) -> None:
    process = delta["process"]
    require(builder.process_commits(True) == process, "E_PROCESS_BINDING")
    for row in process["records"]:
        commit = row["commit"]
        header = builder.git("show", "-s", "--format=%P%x00%aI%x00%cI%x00%s", commit, binary=True)
        require(isinstance(header, bytes), "E_PROCESS_HEADER", commit)
        parts = header.rstrip(b"\r\n").decode("utf-8").split("\0", 3)
        require([parts[0].split(), parts[1], parts[2], parts[3]] ==
                [row["parents"], row["author_time"], row["committer_time"], row["subject"]],
                "E_PROCESS_METADATA", commit)
        patch = builder.git("show", "--format=", "--no-color", "--no-ext-diff", "--no-textconv",
                            "--find-renames", "--find-copies", commit, "--", *builder.ROUTED_PATHS,
                            binary=True)
        require(isinstance(patch, bytes) and sha256(patch) == row["patch_sha256_raw"] and
                sha256(lf_bytes(patch)) == row["patch_sha256_lf"], "E_PROCESS_PATCH", commit)


def verify_controls(delta: dict[str, Any], attestation: dict[str, Any]) -> None:
    inputs = delta["inputs"]
    require(inputs == attestation["inputs"], "E_INPUT_BINDING")
    for key, path in (("result", RESULT_PATH), ("builder", BUILDER_PATH), ("validator", VALIDATOR_PATH),
                      ("parent_ledger", PARENT_LEDGER_PATH), ("active_ledger", ACTIVE_LEDGER_PATH),
                      ("handover", HANDOVER_PATH)):
        raw = (ROOT / path).read_bytes()
        require(raw == lf_bytes(raw) and raw.endswith(b"\n"), "E_CONTROL_LF", path)
        record = inputs.get(key)
        require(record == {"path": path, "sha256_lf": sha256(raw),
                           "lines": len(raw.decode("utf-8").splitlines())}, "E_CONTROL_BINDING", path)
    result = (ROOT / RESULT_PATH).read_text(encoding="utf-8")
    require("Status: `PASS_PENDING_PERSISTENCE`" in result and
            f"Selected Gate: `{GATE}`" in result and "PENDING_REVIEW" not in result,
            "E_RESULT_STATUS")
    for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH):
        lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
        rows = [line for line in lines if line.startswith("| 066 |")]
        cells = rows[0].split("|") if len(rows) == 1 else []
        require(len(rows) == 1 and len(cells) > 3 and cells[3].strip() == "76" and
                "PASS_PENDING_PERSISTENCE" in rows[0] and GATE in rows[0] and
                PERSISTENCE in rows[0] and "Step 77" in rows[0], "E_LEDGER_ROW", path)
    handover = (ROOT / HANDOVER_PATH).read_text(encoding="utf-8")
    require("Phase 066 Step 76" in handover and GATE in handover and PERSISTENCE in handover and
            "Step 77" in handover, "E_HANDOVER")


def run_semantic_controls(delta: dict[str, Any], attestation: dict[str, Any]) -> tuple[int, int]:
    cases: list[tuple[str, Any]] = [
        ("phase", lambda d, a: d.update({"phase": 65})),
        ("counts", lambda d, a: d["source_summary"].update({"occurrences": 432})),
        ("versions", lambda d, a: d["source_summary"]["versions"].update({"v1.0.25": 142})),
        ("occurrence", lambda d, a: d["occurrences"].pop()),
        ("human", lambda d, a: a["machine_blob_attestations"][0]["human_coverage"].update({"status": "UNREAD"})),
        ("binding", lambda d, a: a["occurrence_bindings"][0].update({"attestation_id": "bad"})),
        ("delta", lambda d, a: d["pairwise_deltas"][0]["counts"].update({"changed": 9})),
        ("provenance", lambda d, a: next(row for row in d["pairwise_deltas"][0]["records"]
                                         if row["status"] in {"CHANGED", "ADDED"}).update(
                                             {"new_provenance": None})),
        ("stale", lambda d, a: d["stale_pdf_pairs"][0].update({"v1025_2_build_evidence": True})),
        ("narrative", lambda d, a: d["narrative"].update({"expanded_lines": 9673})),
        ("process", lambda d, a: d["process"]["release"].update({"count": 16})),
        ("route", lambda d, a: d["phase057_routes"].update({"ay_new_count": 1})),
        ("authority", lambda d, a: d["authority"].update({"external_scientific": True})),
        ("coverage", lambda d, a: a["coverage_summary"].update({"unique_blobs_unread": 1})),
        ("cross", lambda d, a: a.update({"delta_semantic_sha256": "0" * 64})),
    ]
    passed = 0
    for label, mutation in cases:
        candidate_delta, candidate_attestation = copy.deepcopy(delta), copy.deepcopy(attestation)
        mutation(candidate_delta, candidate_attestation)
        candidate_delta["semantic_sha256"] = semantic_hash(candidate_delta)
        candidate_attestation["semantic_sha256"] = semantic_hash(candidate_attestation)
        require(artifact_errors(candidate_delta, candidate_attestation), "E_NEGATIVE_ESCAPE", label)
        passed += 1
    return passed, len(cases)


def run_strict_json_controls() -> tuple[int, int]:
    cases = [b'{"a":1,"a":2}\n', b'{"a":NaN}\n', b'{"a":Infinity}\n', b'{"a":1e9999}\n',
             b'{"a":1} trailing\n', b'{"a":"\xff"}\n']
    passed = 0
    for raw in cases:
        try:
            strict_load(raw, "negative")
        except (ValidationFailure, UnicodeError, json.JSONDecodeError):
            passed += 1
        else:
            raise ValidationFailure("E_STRICT_ESCAPE")
    return passed, len(cases)


def run_builder_json_controls(builder: ModuleType) -> tuple[int, int]:
    cases = [b'{"a":1,"a":2}\n', b'{"a":NaN}\n', b'{"a":Infinity}\n', b'{"a":1e9999}\n',
             b'{"a":1} trailing\n', b'{"a":"\xff"}\n']
    passed = 0
    for raw in cases:
        try:
            builder.strict_json(raw)
        except (builder.BuildFailure, UnicodeError, json.JSONDecodeError):
            passed += 1
        else:
            raise ValidationFailure("E_BUILDER_JSON_ESCAPE")
    return passed, len(cases)


def run_policy_controls() -> tuple[int, int]:
    attacks = [
        "import socket\ndef git(): subprocess.run(['git','status'],shell=False,check=False)",
        "import os as x\ndef git(): subprocess.run(['git','status'],shell=False,check=False)",
        "def git(): eval('1'); subprocess.run(['git','status'],shell=False,check=False)",
        "def git(): exec('x=1'); subprocess.run(['git','status'],shell=False,check=False)",
        "def git(): __import__('os'); subprocess.run(['git','status'],shell=False,check=False)",
        "def git(): getattr(subprocess,'run')(['git']); subprocess.run(['git'],shell=False,check=False)",
        "def git(): subprocess.Popen(['git']); subprocess.run(['git'],shell=False,check=False)",
        "def git(): subprocess.run('git status',shell=True,check=False)",
        "def git(): subprocess.run(['git'],shell=False,check=True)",
        "def other(): subprocess.run(['git'],shell=False,check=False)",
        "def atomic_collect_pair(): open('x','w')\ndef git(): subprocess.run(['git'],shell=False,check=False)",
        "def other(p): p.write_bytes(b'x')\ndef git(): subprocess.run(['git'],shell=False,check=False)",
        "from subprocess import run\ndef git(): subprocess.run(['git'],shell=False,check=False)",
        "import subprocess as sp\ndef git(): subprocess.run(['git'],shell=False,check=False)",
        "def git(): subprocess.run(['git'],shell=False,check=False)\ndef x(): compile('1','','exec')",
        "def git(): subprocess.run(['python','x.py'],shell=False,check=False)",
        "def x(p): w=p.write_bytes; w(b'x')\ndef git(): subprocess.run(['git'],shell=False,check=False)",
        "def x(p): p.open('wb').write(b'x')\ndef git(): subprocess.run(['git'],shell=False,check=False)",
        "def x(): os.system('echo x')\ndef git(): subprocess.run(['git'],shell=False,check=False)",
        "def x(): importlib.import_module('socket')\ndef git(): subprocess.run(['git'],shell=False,check=False)",
    ]
    passed = 0
    for source in attacks:
        if source_policy_errors("import subprocess\n" + source, "builder"):
            passed += 1
        else:
            raise ValidationFailure("E_POLICY_ESCAPE", str(passed))
    git_attacks = [
        ("reset", "--hard"), ("checkout", "HEAD"), ("-c", "alias.x=!echo", "x"),
        ("log", "--output=x"), ("show", "--textconv", "HEAD:x"),
        ("status", "--work-tree=/tmp"), ("push", "origin"), ("fetch", "origin"),
        ("update-ref", "-d", "refs/heads/main"), ("clean", "-fd"),
        ("show", "--textconv=true", "HEAD:x"), ("ls-remote", "ext::sh -c echo"),
    ]
    for args in git_attacks:
        try:
            validate_git_args(args)
        except ValidationFailure:
            passed += 1
        else:
            raise ValidationFailure("E_GIT_POLICY_ESCAPE", repr(args))
    return passed, len(attacks) + len(git_attacks)


def verify_content() -> tuple[dict[str, Any], dict[str, Any], int, int]:
    verify_source_policy()
    delta_raw = (ROOT / DELTA_PATH).read_bytes()
    attestation_raw = (ROOT / ATTESTATION_PATH).read_bytes()
    delta, delta_nodes, delta_depth = strict_load(delta_raw, DELTA_PATH)
    attestation, attestation_nodes, attestation_depth = strict_load(attestation_raw, ATTESTATION_PATH)
    errors = artifact_errors(delta, attestation)
    require(not errors, "E_ARTIFACT", repr(errors[:8]))
    builder = load_builder()
    verify_manifest_projection(builder, delta, attestation)
    verify_process_projection(builder, delta)
    verify_controls(delta, attestation)
    return delta, attestation, delta_nodes + attestation_nodes, max(delta_depth, attestation_depth)


def verify_content_worktree() -> None:
    status_text = git("status", "--porcelain=v1", "--untracked-files=all")
    require(isinstance(status_text, str), "E_STATUS")
    status = parse_porcelain(status_text)
    require(set(status) == FINAL_SET, "E_CONTENT_PATHS", repr(sorted(set(status) ^ FINAL_SET)))
    require(not any(path.startswith("Claude/") for path in status), "E_CLAUDE_DIRT")


def verify_staged() -> None:
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    require(branch == BRANCH, "E_BRANCH", str(branch))
    require(git("rev-parse", "HEAD") == EXPECTED_PARENT, "E_STAGED_PARENT")
    require(git("rev-parse", UPSTREAM) == EXPECTED_PARENT, "E_STAGED_UPSTREAM")
    cached = git("diff", "--cached", "--name-status", "--no-renames", "HEAD")
    require(isinstance(cached, str) and parse_name_status(cached) == FINAL_STATUS, "E_STAGED_PATHS")
    require(git("diff", "--name-only") == "", "E_UNSTAGED")
    require(git("ls-files", "--others", "--exclude-standard") == "", "E_UNTRACKED")
    require(git("diff", "--cached", "--check") == "", "E_DIFF_CHECK")
    for path in FINAL_PATHS:
        staged = git("show", f":{path}", binary=True)
        require(isinstance(staged, bytes) and staged == (ROOT / path).read_bytes(), "E_STAGED_BYTES", path)


def canonical_origin(value: str) -> str:
    text = value.lower().replace("\\", "/")
    text = re.sub(r"^[^@]+@", "", text)
    text = re.sub(r"^[a-z]+://", "", text)
    text = text.removesuffix(".git").strip("/")
    return text


def verify_persistence(commit: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None, "E_EXPECTED_COMMIT")
    require(git("rev-parse", "--abbrev-ref", "HEAD") == BRANCH, "E_BRANCH")
    require(git("rev-parse", "HEAD") == commit, "E_HEAD")
    require(git("rev-parse", f"{commit}^") == EXPECTED_PARENT, "E_COMMIT_PARENT")
    require(git("show", "-s", "--format=%s", commit) == EXPECTED_SUBJECT, "E_COMMIT_SUBJECT")
    changed = git("diff-tree", "--no-commit-id", "--name-status", "--no-renames", "-r",
                  f"{commit}^", commit)
    require(isinstance(changed, str) and parse_name_status(changed) == FINAL_STATUS, "E_COMMIT_PATHS")
    require(git("status", "--porcelain") == "", "E_WORKTREE_DIRTY")
    require(git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}") == UPSTREAM,
            "E_UPSTREAM")
    require(git("rev-parse", UPSTREAM) == commit, "E_TRACKING")
    live = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    require(isinstance(live, str) and live.split("\t", 1)[0] == commit, "E_LIVE_REMOTE")
    origin = git("ls-remote", "--get-url", "origin")
    require(isinstance(origin, str) and canonical_origin(origin) == "github.com/lksz1412/project_anode_fit",
            "E_ORIGIN")
    protected = git("show-ref", "--verify", "--hash", "refs/heads/codex/lib-physics-endgame-v1025_2")
    require(protected == PROTECTED_TIP, "E_PROTECTED")
    protected_live = git("ls-remote", "--heads", "origin",
                         "refs/heads/codex/lib-physics-endgame-v1025_2")
    require(isinstance(protected_live, str) and protected_live.split("\t", 1)[0] == PROTECTED_TIP,
            "E_PROTECTED_LIVE")
    main = git("show-ref", "--verify", "--hash", "refs/remotes/origin/main")
    require(main == MAIN_TIP, "E_MAIN")
    main_live = git("ls-remote", "--heads", "origin", "refs/heads/main")
    require(isinstance(main_live, str) and main_live.split("\t", 1)[0] == MAIN_TIP,
            "E_MAIN_LIVE")
    require(git("diff", "--name-only", PROTECTED_TIP, "--", "Claude") == "", "E_CLAUDE_DRIFT")
    for path in FINAL_PATHS:
        committed = git("show", f"{commit}:{path}", binary=True)
        require(isinstance(committed, bytes) and committed == (ROOT / path).read_bytes(),
                "E_COMMITTED_BYTES", path)


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--content-only", action="store_true")
    modes.add_argument("--verify-staged", action="store_true")
    modes.add_argument("--verify-persistence", action="store_true")
    modes.add_argument("--hardening-selftest", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    require((args.verify_persistence and args.expected_commit is not None) or
            (not args.verify_persistence and args.expected_commit is None), "E_EXPECTED_COMMIT_MODE")
    if args.hardening_selftest:
        builder = load_builder()
        policy_passed, policy_total = run_policy_controls()
        strict_passed, strict_total = run_strict_json_controls()
        builder_passed, builder_total = run_builder_json_controls(builder)
        print(f"PASS_P066_STEP76_HARDENING source_git={policy_passed}/{policy_total} strict_json={strict_passed}/{strict_total} builder_json={builder_passed}/{builder_total}")
        return 0
    delta, attestation, nodes, depth = verify_content()
    semantic_passed, semantic_total = run_semantic_controls(delta, attestation)
    strict_passed, strict_total = run_strict_json_controls()
    builder_passed, builder_total = run_builder_json_controls(load_builder())
    policy_passed, policy_total = run_policy_controls()
    print(f"PASS_P066_STEP76_CONTROLS semantic={semantic_passed}/{semantic_total} strict_json={strict_passed}/{strict_total} builder_json={builder_passed}/{builder_total} source_git={policy_passed}/{policy_total}")
    print(f"PASS_P066_STEP76_CONTENT occurrences=433 unique=167 text=158/30597 pdf=6/308 image=3 process=17/20 nodes={nodes} depth={depth} provenance=SOURCE_BOUND_52 fresh_provenance_replay=52/52")
    if args.content_only:
        verify_content_worktree()
        print(f"{GATE} mode=CONTENT_ONLY")
    elif args.verify_staged:
        verify_staged()
        print(f"{GATE} mode=STAGED exact-eight=8/8")
    else:
        verify_persistence(args.expected_commit or "")
        print(f"{PERSISTENCE} commit={args.expected_commit}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationFailure, KeyError, IndexError, TypeError, ValueError, OSError,
            UnicodeError, subprocess.TimeoutExpired) as error:
        code = error.code if isinstance(error, ValidationFailure) else type(error).__name__
        print(f"FAIL_P066_STEP76 {code}: {error}")
        raise SystemExit(1)
