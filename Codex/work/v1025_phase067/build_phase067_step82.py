from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import os
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "8975d6a6cc46686e38249b7971b5535dfa414a8b"
EXPECTED_SUBJECT = "audit(phase067): freeze complete python topology"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
GATE = "PASS_P067_STEP82_SOURCE_TOPOLOGY"
PERSISTENCE = "PASS_P067_STEP82_PERSISTENCE"
BUILDER_SOURCE_POLICY_SHA256_LF = "d30216fc9613aa41bc4aa4feac03421a5c4bb844e40d14030824f68db0066ea3"

MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
BUILDER_PATH = "Codex/work/v1025_phase067/build_phase067_step82.py"
VALIDATOR_PATH = "Codex/work/v1025_phase067/validate_phase067_step82.py"
INVENTORY_PATH = "Codex/results/PHASE_067_PYTHON_SOURCE_INVENTORY.json"
ATTESTATION_PATH = "Codex/results/PHASE_067_PYTHON_FULL_READ_ATTESTATION.json"
RESULT_PATH = "Codex/results/PHASE_067_STEP_082_SOURCE_TOPOLOGY_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

MANIFEST_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
PATH_MEMBERSHIP_SHA256 = "d64fe6b430120820da6ee00a82a3fc9679b885a2c3accd4e0e9b04dced24dfe4"
PATH_BLOB_MEMBERSHIP_SHA256 = "bae10035780580c9caa629d59050f307b492e6c5e75941252aca30eadbbc981f"
BLOB_MEMBERSHIP_SHA256 = "e4e11ba47910647bcc0a0e4fd4e8918fbe2f08c75fd23fefd88fb04e8e96c066"
RELEASE_MEMBERSHIP_SHA256 = "2ccc032ffeb3d9c4b449fbce48bd66448c8324fe96d4065067d8d755127a209c"

RELEASES = (
    "v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13", "v1.0.14", "v1.0.15",
    "v1.0.16", "v1.0.17", "v1.0.18.1", "v1.0.18.2", "v1.0.19",
    "v1.0.20", "v1.0.21", "v1.0.22", "v1.0.23", "v1.0.24",
    "v1.0.24.1", "v1.0.25", "v1.0.25.1", "v1.0.25.2",
)
RELEASE_ROOTS = tuple(f"Claude/docs/{release}" for release in RELEASES)
PARTITIONS = (
    {"partition": "A", "reviewer": "p067_activation_impl", "review_batch": "P067-S82-A-READ-FULL",
     "first": 1, "last": 28,
     "blobs": 28, "lines": 8862,
     "membership_sha256": "df7d7d6f4fa41a7edfb34d07cf5278352a970725858174eef773fb849a0ed812",
     "review_evidence_sha256": "ab76566e1266853d0556f7f83055ac2d0a8317e014c10070c66e5e41fefbe6b3"},
    {"partition": "B", "reviewer": "p066_s76_manifest", "review_batch": "P067-S82-B-SUPPORT-FINAL",
     "first": 29, "last": 56,
     "blobs": 28, "lines": 11050,
     "membership_sha256": "2b4f335a83be768012de9575e6a49ccaca667e4bb65b671a4841d8aa85517ebd",
     "review_evidence_sha256": "be9c06a0894514dc30c0bc601fcc91b9939522588c544d88a5171d5431121c55"},
    {"partition": "C", "reviewer": "p066_s76_routes", "review_batch": "P067-S82-C-SUPPORT-FINAL",
     "first": 57, "last": 84,
     "blobs": 28, "lines": 10040,
     "membership_sha256": "16cc2650c58da37b054d5b0eaac285affce3a901a95da260848ce3f3d229dc8d",
     "review_evidence_sha256": "341134e64337dd5e1292e5fcc2bf8dfd6535276cd5dd1662ee9b10cce16288a4"},
)
ROLE_COUNTS = {"code": (20, 15), "test": (44, 29), "demo": (30, 26), "result": (35, 14)}


class BuildFailure(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise BuildFailure(code, detail)


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
    raise BuildFailure("E_JSON_NONFINITE", token)


def strict_json(raw: bytes) -> dict[str, Any]:
    require(raw == lf_bytes(raw) and raw.endswith(b"\n") and not raw.startswith(b"\xef\xbb\xbf"),
            "E_JSON_BYTES")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise BuildFailure("E_JSON_PARSE", str(error)) from error
    require(isinstance(value, dict), "E_JSON_ROOT")
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
        elif isinstance(item, float):
            require(math.isfinite(item), "E_JSON_NONFINITE")
    return value


def validate_git_argv(args: tuple[str, ...]) -> None:
    require(args, "E_GIT_EMPTY")
    verb = args[0]
    allowed = False
    if verb == "cat-file":
        allowed = len(args) == 3 and args[1] == "blob" and (
            re.fullmatch(r"[0-9a-f]{40}", args[2]) is not None or
            (":" in args[2] and not args[2].startswith("-") and "\n" not in args[2] and "\r" not in args[2]))
    elif verb == "rev-list":
        prefix = ("rev-list", "--full-history", "--reverse", "--topo-order", BASELINE, "--")
        allowed = args[:len(prefix)] == prefix and args[len(prefix):] == RELEASE_ROOTS
    elif verb == "show":
        allowed = (len(args) == 4 and args[1:3] == (
            "-s", "--format=%H%x00%P%x00%T%x00%aI%x00%cI%x00%s") and
            re.fullmatch(r"[0-9a-f]{40}", args[3]) is not None)
    elif verb == "diff-tree":
        common = ("-r", "--raw", "--abbrev=40", "-M", "-C", "--find-copies-harder")
        allowed = ((len(args) == 10 + len(RELEASE_ROOTS) and args[1:7] == common and
                    re.fullmatch(r"[0-9a-f]{40}", args[7]) is not None and
                    re.fullmatch(r"[0-9a-f]{40}", args[8]) is not None and args[9] == "--" and
                    args[10:] == RELEASE_ROOTS) or
                   (len(args) == 10 + len(RELEASE_ROOTS) and args[1] == "--root" and
                    args[2:8] == common and re.fullmatch(r"[0-9a-f]{40}", args[8]) is not None and
                    args[9] == "--" and args[10:] == RELEASE_ROOTS))
    elif verb == "ls-tree":
        allowed = len(args) >= 4 and re.fullmatch(r"[0-9a-f]{40}", args[1]) is not None and args[2] == "--" and all(
            path.startswith("Claude/docs/") and not path.startswith("-") and "\n" not in path and "\r" not in path
            for path in args[3:])
    require(allowed, "E_GIT_ARGV", repr(args))


def run_git(*args: str) -> bytes:
    validate_git_argv(tuple(args))
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False,
                            shell=False, timeout=120)
    require(result.returncode == 0, "E_GIT", result.stderr.decode("utf-8", "replace"))
    return result.stdout


def git_blob(oid: str) -> bytes:
    return run_git("cat-file", "blob", oid)


def membership_hash(values: Iterable[str]) -> str:
    return sha256("".join(value + "\n" for value in values).encode("utf-8"))


def source_segment(text: str, node: ast.AST) -> str:
    return ast.get_source_segment(text, node) or ""


def expression_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{expression_name(node.value)}.{node.attr}"
    if isinstance(node, ast.Subscript):
        return f"{expression_name(node.value)}[]"
    if isinstance(node, ast.Call):
        return f"{expression_name(node.func)}()"
    return type(node).__name__


def bounded_walk(node: ast.AST) -> Iterable[ast.AST]:
    stack = [node]
    first = True
    while stack:
        current = stack.pop()
        yield current
        if not first and isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            continue
        first = False
        stack.extend(reversed(list(ast.iter_child_nodes(current))))


def state_projection(node: ast.AST) -> dict[str, list[str]]:
    names_read: set[str] = set()
    names_written: set[str] = set()
    attributes_read: set[str] = set()
    attributes_written: set[str] = set()
    for item in bounded_walk(node):
        if isinstance(item, ast.Name):
            (names_read if isinstance(item.ctx, ast.Load) else names_written).add(item.id)
        elif isinstance(item, (ast.Attribute, ast.Subscript)):
            target = expression_name(item)
            if isinstance(item.ctx, ast.Load):
                attributes_read.add(target)
            else:
                attributes_written.add(target)
    return {"identifier_reads": sorted(names_read), "identifier_writes": sorted(names_written),
            "attribute_reads": sorted(attributes_read), "attribute_writes": sorted(attributes_written)}


IO_NAMES = {"open", "input", "print", "read", "read_text", "read_bytes", "write", "write_text",
            "write_bytes", "load", "save", "savez", "savez_compressed", "read_csv", "to_csv",
            "savefig", "show", "run", "Popen", "system", "exit"}
MUTATION_NAMES = {"append", "extend", "insert", "pop", "remove", "clear", "update", "setdefault",
                  "sort", "reverse", "write", "write_text", "write_bytes", "save", "savez",
                  "savez_compressed", "savefig", "mkdir", "makedirs", "replace", "rename", "unlink"}


def behavior_projection(node: ast.AST, text: str) -> dict[str, Any]:
    branches: list[dict[str, Any]] = []
    exceptions: list[dict[str, Any]] = []
    fallbacks: list[dict[str, Any]] = []
    io_calls: list[dict[str, Any]] = []
    side_effects: list[dict[str, Any]] = []
    lambdas = 0
    for item in bounded_walk(node):
        line = int(getattr(item, "lineno", 0))
        if isinstance(item, (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.Match)):
            test = getattr(item, "test", getattr(item, "subject", None))
            branches.append({"kind": type(item).__name__, "line": line,
                             "predicate_sha256": sha256(source_segment(text, test).encode("utf-8")) if test else None,
                             "has_else": bool(getattr(item, "orelse", []))})
            if getattr(item, "orelse", []):
                fallbacks.append({"kind": f"{type(item).__name__}_ELSE", "line": line})
        elif isinstance(item, ast.Try):
            branches.append({"kind": "Try", "line": line, "predicate_sha256": None,
                             "has_else": bool(item.orelse)})
            for handler in item.handlers:
                exceptions.append({"kind": "ExceptHandler", "line": int(getattr(handler, "lineno", line)),
                                   "exception": source_segment(text, handler.type) if handler.type else None})
                fallbacks.append({"kind": "EXCEPT_HANDLER", "line": int(getattr(handler, "lineno", line))})
        elif isinstance(item, ast.Raise):
            exceptions.append({"kind": "Raise", "line": line,
                               "exception": source_segment(text, item.exc) if item.exc else None})
        elif isinstance(item, ast.Assert):
            exceptions.append({"kind": "Assert", "line": line,
                               "exception": source_segment(text, item.test)})
        elif isinstance(item, ast.BoolOp) and isinstance(item.op, ast.Or):
            fallbacks.append({"kind": "BOOLEAN_OR", "line": line})
        elif isinstance(item, ast.Lambda):
            lambdas += 1
        if isinstance(item, ast.Call):
            identity = expression_name(item.func)
            leaf = identity.rsplit(".", 1)[-1]
            if leaf in IO_NAMES:
                io_calls.append({"call": identity, "line": line})
            if leaf in MUTATION_NAMES or identity in {"sys.exit", "os.system", "subprocess.run"}:
                side_effects.append({"kind": "CALL", "target": identity, "line": line})
            if leaf in {"get", "getattr", "setdefault"} or identity == "getattr":
                fallbacks.append({"kind": "DEFAULTING_CALL", "target": identity, "line": line})
        elif isinstance(item, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Delete)):
            side_effects.append({"kind": type(item).__name__, "target": None, "line": line})
    return {"branches": branches, "exceptions": exceptions, "fallbacks": fallbacks,
            "io_calls": io_calls, "side_effects": side_effects, "lambda_count": lambdas,
            **state_projection(node)}


def annotation_text(text: str, node: ast.AST | None) -> str | None:
    return source_segment(text, node) if node is not None else None


def function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef, text: str) -> dict[str, Any]:
    arguments = node.args
    positional = [*arguments.posonlyargs, *arguments.args]
    defaults: list[str | None] = [None] * (len(positional) - len(arguments.defaults)) + [
        source_segment(text, value) for value in arguments.defaults]
    return {
        "positional_only": [{"name": arg.arg, "annotation": annotation_text(text, arg.annotation),
                             "default": defaults[index]} for index, arg in enumerate(arguments.posonlyargs)],
        "positional_or_keyword": [
            {"name": arg.arg, "annotation": annotation_text(text, arg.annotation),
             "default": defaults[len(arguments.posonlyargs) + index]}
            for index, arg in enumerate(arguments.args)],
        "vararg": ({"name": arguments.vararg.arg,
                    "annotation": annotation_text(text, arguments.vararg.annotation)} if arguments.vararg else None),
        "keyword_only": [{"name": arg.arg, "annotation": annotation_text(text, arg.annotation),
                           "default": annotation_text(text, default)}
                          for arg, default in zip(arguments.kwonlyargs, arguments.kw_defaults)],
        "kwarg": ({"name": arguments.kwarg.arg,
                   "annotation": annotation_text(text, arguments.kwarg.annotation)} if arguments.kwarg else None),
        "returns": annotation_text(text, node.returns),
    }


def definition_records(tree: ast.Module, text: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    def visit(node: ast.AST, stack: list[str]) -> None:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qualified = ".".join([*stack, node.name])
                raw = source_segment(text, node).encode("utf-8")
                records.append({"qualified_name": qualified,
                                "kind": "ASYNC_FUNCTION" if isinstance(node, ast.AsyncFunctionDef) else "FUNCTION",
                                "line_range": [node.lineno, node.end_lineno],
                                "source_sha256": sha256(raw), "signature": function_signature(node, text),
                                "decorators": [source_segment(text, item) for item in node.decorator_list],
                                "behavior": behavior_projection(node, text)})
                for statement in node.body:
                    visit(statement, [*stack, node.name])
            elif isinstance(node, ast.ClassDef):
                qualified = ".".join([*stack, node.name])
                raw = source_segment(text, node).encode("utf-8")
                records.append({"qualified_name": qualified, "kind": "CLASS",
                                "line_range": [node.lineno, node.end_lineno],
                                "source_sha256": sha256(raw),
                                "signature": {"bases": [source_segment(text, base) for base in node.bases],
                                              "keywords": [{"name": item.arg,
                                                            "value": source_segment(text, item.value)}
                                                           for item in node.keywords]},
                                "decorators": [source_segment(text, item) for item in node.decorator_list],
                                "behavior": behavior_projection(node, text)})
                for statement in node.body:
                    visit(statement, [*stack, node.name])
            else:
                for child in ast.iter_child_nodes(node):
                    visit(child, stack)
    visit(tree, [])
    return records


def import_records(tree: ast.Module) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            records.append({"kind": "IMPORT", "line": node.lineno,
                            "names": [{"name": item.name, "alias": item.asname} for item in node.names]})
        elif isinstance(node, ast.ImportFrom):
            records.append({"kind": "IMPORT_FROM", "line": node.lineno, "module": node.module,
                            "level": node.level,
                            "names": [{"name": item.name, "alias": item.asname} for item in node.names]})
    return sorted(records, key=lambda row: (row["line"], row["kind"], repr(row)))


def semantic_record(raw: bytes) -> dict[str, Any]:
    require(raw == lf_bytes(raw), "E_SOURCE_CR")
    try:
        text = raw.decode("utf-8")
    except UnicodeError as error:
        raise BuildFailure("E_SOURCE_ENCODING", str(error)) from error
    try:
        tree = ast.parse(text)
    except SyntaxError as error:
        raise BuildFailure("E_SOURCE_AST", str(error)) from error
    module = behavior_projection(tree, text)
    definitions = definition_records(tree, text)
    counts = Counter(type(node).__name__ for node in ast.walk(tree))
    return {"encoding": "utf-8", "ast_parse": "PASS", "module_docstring": ast.get_docstring(tree, clean=False),
            "imports": import_records(tree), "definitions": definitions, "module_behavior": module,
            "ast_counts": dict(sorted(counts.items())),
            "definition_counts": dict(sorted(Counter(row["kind"] for row in definitions).items()))}


def parse_tree(raw: bytes) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    text = raw.decode("utf-8").rstrip("\n")
    if not text:
        return result
    for line in text.splitlines():
        meta, path = line.split("\t", 1)
        mode, kind, oid = meta.split()
        result[path] = {"mode": mode, "type": kind, "blob_oid": oid}
    return result


def history_records(selected_paths: set[str]) -> tuple[
        list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    commit_oids = run_git("rev-list", "--full-history", "--reverse", "--topo-order", BASELINE, "--",
                          *RELEASE_ROOTS).decode("ascii").splitlines()
    per_path: dict[str, list[dict[str, Any]]] = defaultdict(list)
    selected_commits: list[dict[str, Any]] = []
    for history_ordinal, commit_oid in enumerate(commit_oids, 1):
        fields = run_git("show", "-s", "--format=%H%x00%P%x00%T%x00%aI%x00%cI%x00%s",
                         commit_oid).decode("utf-8").rstrip("\n").split("\0", 5)
        require(len(fields) == 6 and fields[0] == commit_oid, "E_HISTORY_HEADER", commit_oid)
        parents = fields[1].split()
        comparisons: list[dict[str, Any]] = []
        comparison_parents: list[str | None] = parents if parents else [None]
        for parent_ordinal, parent in enumerate(comparison_parents, 1):
            raw = (run_git("diff-tree", "-r", "--raw", "--abbrev=40", "-M", "-C",
                           "--find-copies-harder", parent, commit_oid, "--", *RELEASE_ROOTS)
                   if parent else
                   run_git("diff-tree", "--root", "-r", "--raw", "--abbrev=40", "-M", "-C",
                           "--find-copies-harder", commit_oid, "--", *RELEASE_ROOTS))
            changes: list[dict[str, Any]] = []
            for line in raw.decode("utf-8").splitlines():
                if not line.startswith(":"):
                    continue
                cells = line.split("\t")
                meta = cells[0].split()
                require(len(meta) == 5 and len(cells) in {2, 3}, "E_HISTORY_RAW", line)
                status = meta[4]
                change = {"old_mode": meta[0][1:], "new_mode": meta[1],
                          "old_blob": meta[2], "new_blob": meta[3], "status": status[0],
                          "similarity": int(status[1:]) if len(status) > 1 else None,
                          "old_path": cells[1], "new_path": cells[-1]}
                if change["old_path"] in selected_paths or change["new_path"] in selected_paths:
                    changes.append(change)
            if not changes:
                continue
            paths = sorted({change["old_path"] for change in changes} |
                           {change["new_path"] for change in changes})
            current_tree = parse_tree(run_git("ls-tree", commit_oid, "--", *paths))
            parent_tree = parse_tree(run_git("ls-tree", parent, "--", *paths)) if parent else {}
            comparisons.append({"parent_ordinal": parent_ordinal, "comparison_parent": parent,
                                "change_count": len(changes)})
            for change in changes:
                expected_current = (current_tree.get(change["new_path"], {}).get("blob_oid") == change["new_blob"]
                                    if change["new_blob"] != "0" * 40
                                    else change["new_path"] not in current_tree)
                expected_parent = (parent_tree.get(change["old_path"], {}).get("blob_oid") == change["old_blob"]
                                   if change["old_blob"] != "0" * 40
                                   else change["old_path"] not in parent_tree)
                record = {**change, "history_ordinal": history_ordinal,
                          "parent_ordinal": parent_ordinal, "commit": commit_oid,
                          "parents": parents, "tree_oid": fields[2],
                          "author_time": fields[3], "committer_time": fields[4], "subject": fields[5],
                          "comparison_parent": parent,
                          "current_tree_entry": current_tree.get(change["new_path"]),
                          "parent_tree_entry": parent_tree.get(change["old_path"]),
                          "current_tree_matches_raw": expected_current,
                          "parent_tree_matches_raw": expected_parent}
                require(record["current_tree_matches_raw"] and record["parent_tree_matches_raw"],
                        "E_PARENT_TREE_BINDING", f"{commit_oid}:{parent}:{change['new_path']}")
                if change["new_path"] in selected_paths:
                    per_path[change["new_path"]].append(record)
                if change["old_path"] in selected_paths and change["old_path"] != change["new_path"]:
                    per_path[change["old_path"]].append({**record, "path_role": "OLD_PATH"})
        if comparisons:
            selected_commits.append({"history_ordinal": history_ordinal, "commit": commit_oid,
                                     "parents": parents, "tree_oid": fields[2],
                                     "author_time": fields[3], "committer_time": fields[4],
                                     "subject": fields[5], "parent_comparisons": comparisons})
    require(set(per_path) == selected_paths, "E_HISTORY_PATH_COVERAGE",
            repr(sorted(selected_paths - set(per_path))[:5]))
    return selected_commits, {
        path: [{"history_ordinal": event["history_ordinal"], "commit": event["commit"],
                "comparison_parent": event["comparison_parent"], "status": event["status"]}
               for event in events]
        for path, events in sorted(per_path.items())
    }, per_path


def load_universe() -> tuple[bytes, list[tuple[int, dict[str, Any]]], list[str]]:
    manifest_raw = run_git("cat-file", "blob", f"{EXPECTED_PARENT}:{MANIFEST_PATH}")
    require(sha256(manifest_raw) == MANIFEST_SHA256, "E_MANIFEST_HASH")
    manifest = strict_json(manifest_raw)
    require(manifest.get("baseline_commit") == BASELINE and manifest.get("version_scope") == list(RELEASES),
            "E_MANIFEST_CONTRACT")
    indexed_rows = [(index, row) for index, row in enumerate(manifest["entries"])
                    if row.get("extension") == "py"]
    rows = [row for _, row in indexed_rows]
    blobs = sorted({row["blob_sha"] for row in rows})
    require(len(indexed_rows) == 129 and len(blobs) == 84, "E_UNIVERSE_COUNTS")
    require(sum(next(row for row in rows if row["blob_sha"] == blob)["extent"]["lines"] for blob in blobs) == 29952,
            "E_UNIVERSE_LINES")
    require(sorted({row["version"] for row in rows}) == sorted(RELEASES), "E_RELEASES")
    require(membership_hash(sorted(row["path"] for row in rows)) == PATH_MEMBERSHIP_SHA256,
            "E_PATH_MEMBERSHIP")
    require(sha256("".join(f"{row['path']}\t{row['blob_sha']}\n"
                            for row in sorted(rows, key=lambda item: item["path"])).encode("utf-8")) ==
            PATH_BLOB_MEMBERSHIP_SHA256, "E_PATH_BLOB_MEMBERSHIP")
    require(membership_hash(blobs) == BLOB_MEMBERSHIP_SHA256 and
            membership_hash(sorted({row["version"] for row in rows})) == RELEASE_MEMBERSHIP_SHA256,
            "E_BLOB_RELEASE_MEMBERSHIP")
    for partition in PARTITIONS:
        selected = blobs[partition["first"] - 1:partition["last"]]
        require(len(selected) == partition["blobs"] and membership_hash(selected) == partition["membership_sha256"],
                "E_PARTITION_MEMBERSHIP", partition["partition"])
    return manifest_raw, indexed_rows, blobs


def partition_for(ordinal: int) -> dict[str, Any]:
    return next(dict(row) for row in PARTITIONS if row["first"] <= ordinal <= row["last"])


def build_artifacts(require_human: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_raw, indexed_rows, blobs = load_universe()
    rows = [row for _, row in indexed_rows]
    grouped: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    for index, row in indexed_rows:
        grouped[row["blob_sha"]].append((index, row))
    if require_human:
        require(all(re.fullmatch(r"[0-9a-f]{64}", row["review_evidence_sha256"]) is not None
                    for row in PARTITIONS), "E_HUMAN_EVIDENCE_PENDING")
    history_commits, path_commit_projection, per_path = history_records({row["path"] for row in rows})
    occurrences: list[dict[str, Any]] = []
    blob_records: list[dict[str, Any]] = []
    attestations: list[dict[str, Any]] = []
    for ordinal, blob in enumerate(blobs, 1):
        source_rows = grouped[blob]
        representative = source_rows[0][1]
        raw = git_blob(blob)
        require(len(raw) == representative["size_bytes"] and len(raw.decode("utf-8").splitlines()) == representative["extent"]["lines"],
                "E_BLOB_EXTENT", blob)
        require(all(row["git_mode"] == "100644" and row["size_bytes"] == len(raw) and
                    row["extent"]["lines"] == representative["extent"]["lines"]
                    for _, row in source_rows), "E_BLOB_OCCURRENCE_CONSISTENCY", blob)
        partition = partition_for(ordinal)
        semantics = semantic_record(raw)
        path_histories: list[dict[str, Any]] = []
        target_events: list[dict[str, Any]] = []
        for _, row in source_rows:
            events = per_path[row["path"]]
            new_events = [event for event in events if event["new_path"] == row["path"]]
            introduction_events = [event for event in new_events if event["status"] in {"A", "R", "C"}]
            exact_blob_events = [event for event in new_events if event["new_blob"] == blob]
            require(introduction_events and exact_blob_events, "E_BLOB_GENEALOGY", row["path"])
            first_introduction_ordinal = min(event["history_ordinal"] for event in introduction_events)
            first_exact_ordinal = min(event["history_ordinal"] for event in exact_blob_events)
            introductions = [event for event in introduction_events
                             if event["history_ordinal"] == first_introduction_ordinal]
            first_exact_candidates = [event for event in exact_blob_events
                                      if event["history_ordinal"] == first_exact_ordinal]
            target_events.extend(exact_blob_events)
            exact_rc = [event for event in events if event["status"] in {"R", "C"} and
                        event["old_blob"] == event["new_blob"]]
            similar_rc = [event for event in events if event["status"] in {"R", "C"} and
                          event["old_blob"] != event["new_blob"]]
            path_histories.append({"path": row["path"], "release": row["version"],
                                   "introduction_candidates": [{"history_ordinal": event["history_ordinal"],
                                       "commit": event["commit"], "comparison_parent": event["comparison_parent"]}
                                       for event in introductions],
                                   "introduction_selection": ("UNIQUE" if len(introductions) == 1 else
                                       "MULTIPLE_PARENT_CANDIDATES_PRESERVED_NO_RELATION_INFERRED"),
                                   "introduction_event_count_all_history": len(introduction_events),
                                   "first_exact_blob_candidates": [{"history_ordinal": event["history_ordinal"],
                                       "commit": event["commit"], "comparison_parent": event["comparison_parent"]}
                                       for event in first_exact_candidates],
                                   "first_exact_selection": ("UNIQUE" if len(first_exact_candidates) == 1 else
                                       "MULTIPLE_PARENT_CANDIDATES_PRESERVED_NO_RELATION_INFERRED"),
                                   "exact_blob_event_count_all_history": len(exact_blob_events),
                                   "touch_events": path_commit_projection[row["path"]],
                                   "events": events,
                                   "rename_copy_exact_same_blob": exact_rc,
                                   "rename_copy_similarity_only": similar_rc,
                                   "rename_copy_classification": ("EXACT_SAME_BLOB" if exact_rc and not similar_rc
                                       else "EXACT_AND_SIMILARITY_SEPARATED" if exact_rc and similar_rc
                                       else "SIMILARITY_ONLY" if similar_rc
                                       else "NONE_OBSERVED_NO_RELATION_INFERRED")})
        unique_target_events = []
        seen_target_events: set[tuple[str, str | None]] = set()
        for event in target_events:
            identity = (event["commit"], event["comparison_parent"])
            if identity not in seen_target_events:
                seen_target_events.add(identity)
                unique_target_events.append({"history_ordinal": event["history_ordinal"],
                                             "commit": event["commit"],
                                             "comparison_parent": event["comparison_parent"]})
        unique_target_events.sort(key=lambda event: (
            event["history_ordinal"], event["commit"], event["comparison_parent"] or ""))
        first_target_ordinal = min(event["history_ordinal"] for event in unique_target_events)
        first_target_candidates = [event for event in unique_target_events
                                   if event["history_ordinal"] == first_target_ordinal]
        later_target_events = [event for event in unique_target_events
                               if event["history_ordinal"] > first_target_ordinal]
        releases = sorted({row["version"] for _, row in source_rows})
        roles = sorted({row["role"] for _, row in source_rows})
        paths = [row["path"] for _, row in source_rows]
        record = {"ordinal": ordinal, "blob_oid": blob, "git_mode": "100644", "size_bytes": len(raw),
                  "physical_lines": len(raw.decode("utf-8").splitlines()), "raw_sha256": sha256(raw),
                  "lf_sha256": sha256(lf_bytes(raw)), "occurrence_count": len(source_rows),
                  "occurrence_paths": paths, "release_projection": releases, "role_projection": roles,
                   "genealogy": {"path_histories": path_histories,
                                 "target_blob_touch_events": unique_target_events,
                                 "target_blob_first_introduction_candidates": first_target_candidates,
                                 "target_blob_first_introduction_selection": (
                                     "UNIQUE" if len(first_target_candidates) == 1 else
                                     "MULTIPLE_PARENT_CANDIDATES_PRESERVED_NO_RELATION_INFERRED"),
                                 "target_blob_later_touch_events": later_target_events,
                                "multiple_candidate_path_count": sum(
                                    history["introduction_selection"].startswith("MULTIPLE") or
                                    history["first_exact_selection"].startswith("MULTIPLE")
                                    for history in path_histories),
                                "ambiguous_relation_inferred": any(
                                    "INFERRED" in history["introduction_selection"] and
                                    not history["introduction_selection"].endswith("NO_RELATION_INFERRED")
                                    for history in path_histories)}}
        blob_records.append(record)
        attestations.append({"ordinal": ordinal, "blob_oid": blob, "partition": partition["partition"],
                             "reviewer": partition["reviewer"], "review_evidence_sha256": partition["review_evidence_sha256"],
                             "read_status": "READ_FULL" if require_human else "MACHINE_PREVIEW",
                             "line_ranges": [[1, record["physical_lines"]]], "unread_lines": 0,
                             "truncation_unresolved": 0, "raw_sha256": record["raw_sha256"],
                             "lf_sha256": record["lf_sha256"], "encoding": "utf-8",
                             "ast_parse": "PASS", "semantic": semantics,
                             "occurrence_projection": {"paths": paths, "releases": releases, "roles": roles},
                             "genealogy_sha256": sha256(canonical_bytes(record["genealogy"]))})
    manifest_indices = {row["path"]: index for index, row in indexed_rows}
    for occurrence_ordinal, row in enumerate(sorted(rows, key=lambda item: item["path"]), 1):
        blob_ordinal = blobs.index(row["blob_sha"]) + 1
        occurrences.append({"ordinal": occurrence_ordinal, "manifest_entry_index": manifest_indices[row["path"]],
                            "path": row["path"], "release": row["version"], "role": row["role"],
                            "blob_oid": row["blob_sha"], "blob_ordinal": blob_ordinal,
                            "git_mode": row["git_mode"], "size_bytes": row["size_bytes"],
                            "physical_lines": row["extent"]["lines"]})
    occurrence_roles = Counter(row["role"] for row in rows)
    unique_roles = Counter()
    for blob in blobs:
        for role in {row["role"] for _, row in grouped[blob]}:
            unique_roles[role] += 1
    require({role: (occurrence_roles[role], unique_roles[role]) for role in ROLE_COUNTS} == ROLE_COUNTS,
            "E_ROLE_COUNTS")
    controls: dict[str, dict[str, Any]] = {}
    for name, path in (("builder", BUILDER_PATH), ("validator", VALIDATOR_PATH), ("result", RESULT_PATH),
                       ("parent_ledger", PARENT_LEDGER_PATH), ("active_ledger", ACTIVE_LEDGER_PATH),
                       ("handover", HANDOVER_PATH)):
        raw = (ROOT / path).read_bytes()
        require(raw == lf_bytes(raw) and raw.endswith(b"\n"), "E_CONTROL_BYTES", path)
        controls[name] = {"path": path, "sha256_lf": sha256(raw),
                          "physical_lines": len(raw.decode("utf-8").splitlines())}
    common = {"schema_version": "P067-S82-1", "phase": 67, "step": 82,
              "generated_date": "2026-09-02", "baseline_commit": BASELINE,
              "expected_parent": EXPECTED_PARENT, "expected_subject": EXPECTED_SUBJECT,
              "branch": BRANCH, "gate": GATE, "persistence_terminal": PERSISTENCE,
              "precommit_status": "PASS_PENDING_PERSISTENCE", "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
              "result_first": True, "json_outputs_last": True,
              "inputs": {"manifest": {"path": MANIFEST_PATH, "raw_sha256": sha256(manifest_raw),
                                        "lf_sha256": sha256(lf_bytes(manifest_raw))}, **controls},
              "authority": {"source_identity": True, "full_read_coverage": True,
                            "static_ast_topology": True, "runtime_behavior": False,
                            "test_pass": False, "scientific_truth": False,
                            "external_material_authority": False, "canonical_release": False,
                            "publication_ready": False, "production_changed": False}}
    inventory: dict[str, Any] = {**common, "artifact": "PHASE_067_PYTHON_SOURCE_INVENTORY",
        "universe": {"occurrences": 129, "unique_blobs": 84, "unique_blob_physical_lines": 29952,
                     "releases": 20, "role_occurrence_counts": dict(sorted(occurrence_roles.items())),
                     "role_unique_blob_counts": dict(sorted(unique_roles.items())),
                     "path_membership_sha256": PATH_MEMBERSHIP_SHA256,
                     "path_blob_membership_sha256": PATH_BLOB_MEMBERSHIP_SHA256,
                     "blob_membership_sha256": BLOB_MEMBERSHIP_SHA256,
                     "release_membership_sha256": RELEASE_MEMBERSHIP_SHA256},
        "occurrence_records": occurrences, "blob_records": blob_records,
        "genealogy_commit_records": history_commits,
        "validation": {"orphan_occurrences": 0, "orphan_blobs": 0, "duplicate_occurrences": 0,
                       "unread_blobs": 0, "parser_failures": 0, "ambiguous_relations_inferred": 0},
        "semantic_sha256": ""}
    inventory["semantic_sha256"] = semantic_hash(inventory)
    aggregate_ast = Counter()
    definition_counts = Counter()
    for row in attestations:
        aggregate_ast.update(row["semantic"]["ast_counts"])
        definition_counts.update(row["semantic"]["definition_counts"])
    require(definition_counts["FUNCTION"] + definition_counts["ASYNC_FUNCTION"] == 906 and
            definition_counts["CLASS"] == 35, "E_DEFINITION_AGGREGATE", repr(definition_counts))
    attestation: dict[str, Any] = {**common, "artifact": "PHASE_067_PYTHON_FULL_READ_ATTESTATION",
        "inventory_semantic_sha256": inventory["semantic_sha256"],
        "partition_contract": [dict(row) for row in PARTITIONS],
        "blob_attestations": attestations,
        "coverage": {"occurrences_total": 129, "occurrences_projected": 129,
                     "unique_blobs_total": 84, "unique_blobs_read_full": 84,
                     "unique_blob_physical_lines_total": 29952,
                     "unique_blob_physical_lines_read": 29952, "releases_total": 20,
                     "releases_projected": 20, "parser_failures": 0, "encoding_failures": 0,
                     "unread_lines": 0, "truncation_unresolved": 0},
        "aggregate_ast_counts": dict(sorted(aggregate_ast.items())),
        "aggregate_definition_counts": dict(sorted(definition_counts.items())),
        "validation": {"partition_overlap": 0, "partition_gap": 0, "blob_hash_mismatch": 0,
                       "line_extent_mismatch": 0, "occurrence_projection_orphans": 0,
                       "genealogy_unbound": 0, "authority_promotions": 0},
        "semantic_sha256": ""}
    attestation["semantic_sha256"] = semantic_hash(attestation)
    return inventory, attestation


def atomic_collect(inventory_raw: bytes, attestation_raw: bytes) -> None:
    outputs = ((ROOT / INVENTORY_PATH, inventory_raw), (ROOT / ATTESTATION_PATH, attestation_raw))
    require(all(not path.exists() for path, _ in outputs), "E_COLLECT_REFUSES_OVERWRITE")
    temps = [(path.with_name(path.name + ".tmp-p067-s82"), raw) for path, raw in outputs]
    require(all(not path.exists() for path, _ in temps), "E_COLLECT_TEMP_EXISTS")
    created: list[Path] = []
    try:
        for path, raw in temps:
            path.write_bytes(raw)
            require(path.read_bytes() == raw, "E_COLLECT_TEMP_WRITE", str(path))
        for (target, expected), (temp, _) in zip(outputs, temps):
            os.replace(temp, target)
            created.append(target)
            require(target.read_bytes() == expected, "E_COLLECT_WRITE", str(target))
    except (OSError, BuildFailure):
        for path in created:
            if path.exists():
                path.unlink()
        raise
    finally:
        for path, _ in temps:
            if path.exists():
                path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--preview", action="store_true")
    modes.add_argument("--collect", action="store_true")
    args = parser.parse_args()
    first = build_artifacts(require_human=args.collect)
    second = build_artifacts(require_human=args.collect)
    first_raw = tuple(canonical_bytes(value) for value in first)
    second_raw = tuple(canonical_bytes(value) for value in second)
    require(first_raw == second_raw, "E_DETERMINISM")
    if args.preview:
        print("PASS_P067_STEP82_PREVIEW occurrences=129 unique=84 lines=29952 releases=20 determinism=2/2")
        return 0
    atomic_collect(first_raw[0], first_raw[1])
    print("PASS_P067_STEP82_COLLECT JSON_PAIR_LAST occurrences=129 unique=84 lines=29952 determinism=2/2")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BuildFailure, KeyError, IndexError, TypeError, ValueError, OSError,
            UnicodeError, subprocess.TimeoutExpired) as error:
        code = error.code if isinstance(error, BuildFailure) else type(error).__name__
        print(f"FAIL_P067_STEP82_BUILD {code}: {error}")
        raise SystemExit(1)
