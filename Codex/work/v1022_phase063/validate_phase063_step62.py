#!/usr/bin/env python3
"""Validate Phase 063 Step 62 review/adoption/build/state closure."""

from __future__ import annotations

import argparse
import ast
import copy
import functools
import hashlib
import json
import math
import pathlib
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from typing import Any, Callable

from PIL import Image, ImageChops


REPO = pathlib.Path(__file__).resolve().parents[3]
MATRIX_REL = "Codex/results/PHASE_063_V1022_REVIEW_ADOPTION_CLOSURE_MATRIX.json"
RESULT_REL = "Codex/results/PHASE_063_STEP_062_REVIEW_ADOPTION_CLOSURE_RESULT.md"
BUILDER_REL = "Codex/work/v1022_phase063/build_phase063_step62_review_adoption_closure.py"
VALIDATOR_REL = "Codex/work/v1022_phase063/validate_phase063_step62.py"
BUILDER_RAW_SHA256 = "2f0a41d728ca77580d54b67f6c3ab516a9e3b5eb17179107737f1df2cf451b6b"
BUILDER_AST_SHA256 = "88991343d9ed6a6beac4f8ac71edbba5ff14bc99613c47a22f711b1158502ebc"
ACTIVE_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
TOPOLOGY_REL = "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json"
PROVISIONAL_REL = "Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json"

PARENT = "89bd7c7c27a827ec2322db25fe9e2634874c2f9d"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
SUBJECT = "audit(phase063): close v1022 review adoption build"
GATE = "PASS_P063_STEP62_REVIEW_ADOPTION_CLOSURE_WITH_CONCERNS"
PERSISTENCE = "PASS_P063_STEP62_PERSISTENCE"
SENTINEL = "P063_STEP62_RESULT_FIRST_PRECOMMIT"
EXACT_PATHS = [
    BUILDER_REL,
    VALIDATOR_REL,
    MATRIX_REL,
    RESULT_REL,
    ACTIVE_LEDGER,
    PARENT_LEDGER,
    HANDOVER,
]

EXPECTED_FAMILY_COUNTS = {
    "COMP_AUD": 4, "COMP_R6": 1, "COMP_R7": 4, "COMP_R8": 1,
    "COMP_RV": 3, "COMP_SM2": 5, "COMP_V23": 5,
    "FR_CONTROL_TRIAGE_EXEC": 8, "FR_REPORT_A01_A23": 23,
    "R2_A_SEAMS": 5, "R2_B_BRIDGES": 11, "R2_CONTROL": 4,
    "R2_C_STATMECH": 3, "R3_CONTROL": 3, "R3_D_SEAMS": 3,
    "R3_E_BRIDGES": 8, "R4_SURVEY": 7, "R4_UPGRADED": 4,
    "R5_CONTROL": 2, "R5_W1": 7, "R5_W2": 7, "R5_W3": 7,
}
EXPECTED_STATE_GROUPS = {
    "RESOLVED_IN_V1022": {131, 141, 145, 146, 147, 158, 160, 165},
    "OPEN": {101, 103, 104, 111, 114, 115, 118, 119, 126, 127, 130, 133, 134, 135, 136, 137, 138, 139, 142, 148, 150, 151, 153, 155, 156, 157, 159, 161, 162, 163, 166, 167, 168, 169, 170, 171, 172, 177, 179, 183, 184, 185, 186, 190, 191},
    "SUPERSEDED": {108, 180},
    "HISTORICAL_ONLY": {96, 97, 98, 99, 100, 102, 105, 106, 107, 109, 110, 113, 116, 117, 124, 125, 140, 143, 144, 154, 164, 174, 175, 176, 178, 181, 182, 187, 188, 189},
    "UNVERIFIED": {112, 120, 121, 122, 123, 128, 129, 132, 149, 152, 173},
}
EXPECTED_STATES = {
    number: state for state, numbers in EXPECTED_STATE_GROUPS.items() for number in numbers
}
CURRENT_FINAL_EVIDENCE_IDS = {101, 127, 131, 136, 141, 145, 146, 147, 158, 160, 165, 169, 183, 184, 186}
PATCH_CEILING_IDS = {100, 116, 118, 124, 172}
ROLE_KEY = {
    "T_TASK_OR_BRIEF": "task_brief_sources",
    "C_CANDIDATE_PROPOSAL_OR_DRAFT": "proposal_sources",
    "R_REVIEW_OR_SURVEY": "review_sources",
    "D_DECISION_TRIAGE_OR_EXECUTION_RECORD": "decision_sources",
    "S_SELF_REPORT_OR_STATUS": "status_sources",
}
V1022_PREFIX = "Claude/docs/v1.0.22/"
V1022_BUILD_DRIVERS = [
    "appendix_phase_separation.tex",
    "ch1_graphite_v1.0.22.tex",
    "ch2_lco_v1.0.22.tex",
    "ch3_si_v1.0.22.tex",
]
IMPLEMENTATION_APPENDIX_ALLOWLIST = [
    f"{V1022_PREFIX}_sections/ch1_appB_codemap.tex",
    f"{V1022_PREFIX}_sections/ch2_appB_codemap.tex",
]
CH3_MAIN_IMPLEMENTATION_SECTION = f"{V1022_PREFIX}_sections/ch3v22_sec05_code.tex"
FITTING_GUIDE = f"{V1022_PREFIX}FITTING_GUIDE.md"
NONRENDERING_COMMAND_RE = re.compile(
    r"\\(?:label|ref|pageref|eqref|autoref|cref|Cref|input|include)\*?"
    r"(?:\[[^\]]*\])?\{[^{}]*\}"
)
CODE_SCAN_PATTERNS = [
    ("ENGLISH_CODE_OR_COMMAND", re.compile(r"(?i)(?<![A-Za-z])code(?![A-Za-z])")),
    ("LATEX_TEXTTT_COMMAND", re.compile(r"\\texttt\s*\{")),
    ("PYTHON_FILE_SUFFIX", re.compile(r"(?i)\.py\b")),
    ("API_WORD", re.compile(r"(?i)(?<![A-Za-z])API(?![A-Za-z])")),
    ("KOREAN_CODE", re.compile("코드")),
    ("KOREAN_IMPLEMENTATION", re.compile("구현")),
    ("DEFAULT_WORD", re.compile(r"(?i)(?<![A-Za-z])default(?![A-Za-z])")),
]


class ValidationError(RuntimeError):
    """Fail-closed Step 62 validation error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def run_git(*args: str, text: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=text,
        encoding="utf-8" if text else None, errors="strict" if text else None,
        timeout=120, check=True,
    )
    return proc.stdout


@functools.lru_cache(maxsize=None)
def git_bytes(revision: str, path: str) -> bytes:
    return run_git("show", f"{revision}:{path}", text=False)  # type: ignore[return-value]


def strict_load_bytes(raw: bytes) -> Any:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            if key in result:
                raise ValidationError(f"E_JSON_DUPLICATE_KEY:{key}")
            result[key] = value
        return result

    def constant(value: str) -> None:
        raise ValidationError(f"E_JSON_NONFINITE:{value}")

    def finite_float(value: str) -> float:
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ValidationError(f"E_JSON_NONFINITE:{value}")
        return parsed

    try:
        return json.loads(
            raw.decode("utf-8"), object_pairs_hook=pairs,
            parse_constant=constant, parse_float=finite_float,
        )
    except UnicodeDecodeError as exc:
        raise ValidationError(f"E_JSON_UTF8:{exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"E_JSON_SYNTAX:{exc.msg}") from exc


def strict_load(path: pathlib.Path) -> Any:
    return strict_load_bytes(path.read_bytes())


def traversal_count(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + len(value) + sum(traversal_count(item) for item in value.values())
    if isinstance(value, list):
        return 1 + sum(traversal_count(item) for item in value)
    if isinstance(value, float):
        require(math.isfinite(value), "E_NONFINITE_TRAVERSAL")
    return 1


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def expected_projection() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="p063-step62-projection-") as tmp:
        root = pathlib.Path(tmp)
        matrix = root / "matrix.json"
        result = root / "result.md"
        subprocess.run(
            [sys.executable, "-B", str(REPO / BUILDER_REL), "--matrix", str(matrix), "--result", str(result)],
            cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="strict",
            timeout=240, check=True,
        )
        return strict_load(matrix)


def portable_ast_value(value: Any) -> Any:
    if isinstance(value, ast.AST):
        return {
            "node": type(value).__name__,
            "fields": {
                field: portable_ast_value(item)
                for field, item in ast.iter_fields(value)
                if field != "type_params"
            },
        }
    if isinstance(value, list):
        return [portable_ast_value(item) for item in value]
    if isinstance(value, bytes):
        return {"bytes_hex": value.hex()}
    return value


def portable_ast_sha256(raw: bytes) -> str:
    tree = ast.parse(raw.decode("utf-8"), filename=BUILDER_REL)
    serialized = json.dumps(
        portable_ast_value(tree), ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def validate_builder_source_policy(
    candidate_raw: bytes | None = None,
    *,
    enforce_raw_pin: bool = True,
    enforce_ast_pin: bool = True,
) -> None:
    raw = (REPO / BUILDER_REL).read_bytes() if candidate_raw is None else candidate_raw
    if enforce_raw_pin:
        require(hashlib.sha256(raw).hexdigest() == BUILDER_RAW_SHA256, "E_BUILDER_RAW_SHA256")
    text = raw.decode("utf-8")
    tree = ast.parse(text, filename=BUILDER_REL)
    ast_sha256 = portable_ast_sha256(raw)
    if enforce_ast_pin:
        require(ast_sha256 == BUILDER_AST_SHA256, "E_BUILDER_AST_SHA256")
    allowed_imports = {"__future__", "argparse", "hashlib", "json", "pathlib", "posixpath", "re", "subprocess", "collections", "typing"}
    imported: set[str] = set()
    forbidden_calls: list[str] = []
    subprocess_calls: list[ast.Call] = []
    run_git_node: ast.FunctionDef | ast.AsyncFunctionDef | None = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".", 1)[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"}:
            forbidden_calls.append(node.func.id)
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "subprocess"
        ):
            subprocess_calls.append(node)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "run_git":
            require(run_git_node is None, "E_BUILDER_RUN_GIT_DUPLICATE")
            run_git_node = node
    require(imported <= allowed_imports, f"E_BUILDER_IMPORT_POLICY:{sorted(imported - allowed_imports)}")
    require(not forbidden_calls, f"E_BUILDER_DYNAMIC_EXEC:{forbidden_calls}")
    require("sys.version_info" not in text and "platform.python_version" not in text, "E_BUILDER_VERSION_BRANCH")
    require(run_git_node is not None, "E_BUILDER_RUN_GIT_MISSING")
    require(len(subprocess_calls) == 1, f"E_BUILDER_SUBPROCESS_POLICY:{len(subprocess_calls)}")
    subprocess_call = subprocess_calls[0]
    require(subprocess_call in set(ast.walk(run_git_node)), "E_BUILDER_SUBPROCESS_SCOPE")
    require(
        isinstance(subprocess_call.func, ast.Attribute) and subprocess_call.func.attr == "run",
        "E_BUILDER_SUBPROCESS_API",
    )
    require(
        bool(subprocess_call.args)
        and isinstance(subprocess_call.args[0], ast.List)
        and len(subprocess_call.args[0].elts) == 2
        and isinstance(subprocess_call.args[0].elts[0], ast.Constant)
        and subprocess_call.args[0].elts[0].value == "git"
        and isinstance(subprocess_call.args[0].elts[1], ast.Starred)
        and isinstance(subprocess_call.args[0].elts[1].value, ast.Name)
        and subprocess_call.args[0].elts[1].value.id == "args",
        "E_BUILDER_SUBPROCESS_ARGV",
    )


def split_latex_comment(line: str) -> tuple[str, str]:
    for index, char in enumerate(line):
        if char == "%":
            backslashes = len(line[:index]) - len(line[:index].rstrip("\\"))
            if backslashes % 2 == 0:
                return line[:index], line[index + 1 :]
    return line, ""


def rendered_scan_text(line: str) -> str:
    current = line
    while True:
        updated = NONRENDERING_COMMAND_RE.sub("", current)
        if updated == current:
            return current
        current = updated


def code_token_matches(text: str) -> list[dict[str, Any]]:
    rows = [
        {
            "token_class": token_class,
            "start_column": match.start() + 1,
            "end_column": match.end(),
            "token": match.group(0),
        }
        for token_class, pattern in CODE_SCAN_PATTERNS
        for match in pattern.finditer(text)
    ]
    return sorted(rows, key=lambda row: (row["start_column"], row["end_column"], row["token_class"]))


def code_surface_class(path: str, rendered_state: str) -> tuple[str, str, bool, str]:
    if rendered_state == "COMMENT":
        if path in IMPLEMENTATION_APPENDIX_ALLOWLIST:
            return "IMPLEMENTATION_APPENDIX_COMMENTS", "NONRENDERED_COMMENT_HISTORY", False, "NONRENDERED_COMMENT"
        if "preamble" in pathlib.PurePosixPath(path).name or path in [f"{V1022_PREFIX}{name}" for name in V1022_BUILD_DRIVERS]:
            return "PREAMBLE_OR_DRIVER_COMMENTS", "NONRENDERED_COMMENT_HISTORY", False, "NONRENDERED_COMMENT"
        return "PHYSICS_SOURCE_COMMENTS", "NONRENDERED_COMMENT_HISTORY", False, "NONRENDERED_COMMENT"
    if path == FITTING_GUIDE:
        return "FITTING_GUIDE", "SEPARATE_GUIDE_NOT_PHYSICS_MANUSCRIPT", False, "GUIDE_ONLY"
    if path in IMPLEMENTATION_APPENDIX_ALLOWLIST:
        return "IMPLEMENTATION_APPENDIX_RENDERED", "ALLOWLISTED_DEDICATED_IMPLEMENTATION_SURFACE", False, "DEDICATED_IMPLEMENTATION_APPENDIX"
    if path == CH3_MAIN_IMPLEMENTATION_SECTION:
        return "IMPLEMENTATION_MAIN_BODY_RELOCATION_REQUIRED", "FORBIDDEN_MAIN_BODY_IMPLEMENTATION_SECTION_OPEN", True, "IMPLEMENTATION_MAIN_BODY_RELOCATION_REQUIRED"
    name = pathlib.PurePosixPath(path).name
    if name.endswith("_bib.tex"):
        return "BIBLIOGRAPHY", "BIBLIOGRAPHIC_TOKEN_ONLY", False, "BIBLIOGRAPHY_ONLY"
    if "preamble" in name:
        return "PREAMBLE_NONRENDERED", "NONRENDERED_CONTROL", False, "NONRENDERED_CONTROL"
    return "PHYSICS_MAIN_BODY_RENDERED", "FORBIDDEN_BY_TARGET_MANUSCRIPT_POLICY_OPEN", True, "IMPLEMENTATION_OR_CODE_PROSE"


_CODE_REPLAY_CACHE: tuple[list[dict[str, Any]], list[dict[str, Any]]] | None = None


def replay_code_mention_rows(code: dict[str, Any]) -> None:
    global _CODE_REPLAY_CACHE
    if _CODE_REPLAY_CACHE is not None:
        inventory, rows = _CODE_REPLAY_CACHE
        require(code["reachable_tex_inventory"] == inventory, "E_CODE_REACHABLE_INVENTORY")
        require(code["occurrence_rows"] == rows, "E_CODE_OCCURRENCE_REPLAY")
        return
    queue = [f"{V1022_PREFIX}{name}" for name in V1022_BUILD_DRIVERS]
    seen: set[str] = set()
    inventory: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    while queue:
        path = queue.pop(0)
        if path in seen:
            continue
        raw = git_bytes(BASELINE, path)
        text = raw.decode("utf-8-sig")
        seen.add(path)
        for match in re.finditer(r"\\(?:input|include)\s*\{([^}]+)\}", text):
            target = match.group(1) + ("" if match.group(1).endswith(".tex") else ".tex")
            resolved = posixpath.normpath(f"{V1022_PREFIX}{target}")
            require(resolved.startswith(V1022_PREFIX) and not resolved.startswith(f"{V1022_PREFIX}../"), f"E_CODE_DEPENDENCY_PATH:{path}")
            if resolved not in seen:
                queue.append(resolved)
    require(len(seen) == 53, "E_CODE_REACHABLE_COUNT")
    for path in sorted(seen):
        raw = git_bytes(BASELINE, path)
        text = raw.decode("utf-8-sig")
        blob = str(run_git("rev-parse", f"{BASELINE}:{path}")).strip()
        inventory.append({"path": path, "blob_sha1": blob, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "physical_lines": len(text.splitlines())})
        for line_number, raw_line in enumerate(text.splitlines(), 1):
            rendered, comment = split_latex_comment(raw_line)
            for rendered_state, scan_text in (("RENDERED", rendered_scan_text(rendered)), ("COMMENT", comment)):
                matches = code_token_matches(scan_text)
                if matches:
                    surface, disposition, actionable, manual_class = code_surface_class(path, rendered_state)
                    rows.append({"path": path, "blob_sha1": blob, "line": line_number, "rendered_state": rendered_state, "surface_class": surface, "manual_class": manual_class, "actionable": actionable, "disposition": disposition, "occurrences": len(matches), "token_classes": sorted({row["token_class"] for row in matches}), "token_matches": matches, "source_line_sha256": hashlib.sha256(raw_line.encode("utf-8")).hexdigest(), "scan_text_sha256": hashlib.sha256(scan_text.encode("utf-8")).hexdigest()})
    guide_raw = git_bytes(BASELINE, FITTING_GUIDE)
    guide_blob = str(run_git("rev-parse", f"{BASELINE}:{FITTING_GUIDE}")).strip()
    for line_number, line in enumerate(guide_raw.decode("utf-8-sig").splitlines(), 1):
        matches = code_token_matches(line)
        if matches:
            surface, disposition, actionable, manual_class = code_surface_class(FITTING_GUIDE, "RENDERED")
            rows.append({"path": FITTING_GUIDE, "blob_sha1": guide_blob, "line": line_number, "rendered_state": "RENDERED", "surface_class": surface, "manual_class": manual_class, "actionable": actionable, "disposition": disposition, "occurrences": len(matches), "token_classes": sorted({row["token_class"] for row in matches}), "token_matches": matches, "source_line_sha256": hashlib.sha256(line.encode("utf-8")).hexdigest(), "scan_text_sha256": hashlib.sha256(line.encode("utf-8")).hexdigest()})
    rows.sort(key=lambda row: (row["path"], row["line"], row["rendered_state"]))
    _CODE_REPLAY_CACHE = (inventory, rows)
    require(code["reachable_tex_inventory"] == inventory, "E_CODE_REACHABLE_INVENTORY")
    require(code["occurrence_rows"] == rows, "E_CODE_OCCURRENCE_REPLAY")


def normalized_source_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


@functools.lru_cache(maxsize=None)
def replay_patch_final_survival(commit: str, path: str) -> dict[str, Any]:
    raw = run_git("show", "--format=", "--unified=0", commit, "--", path, text=False)
    assert isinstance(raw, bytes)
    additions: list[dict[str, Any]] = []
    new_line: int | None = None
    for line in raw.decode("utf-8", errors="replace").splitlines():
        if line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", line)
            require(match is not None, f"E_PATCH_HUNK_PARSE:{commit}:{path}")
            new_line = int(match.group(1))
        elif new_line is not None and line.startswith("+") and not line.startswith("+++"):
            normalized = normalized_source_line(line[1:])
            if normalized:
                additions.append({"patch_new_line": new_line, "normalized_sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest()})
            new_line += 1
        elif new_line is not None and line.startswith("-") and not line.startswith("---"):
            continue
        elif new_line is not None and line.startswith(" "):
            new_line += 1
    index: dict[str, list[int]] = {}
    for number, line in enumerate(git_bytes(BASELINE, path).decode("utf-8-sig").splitlines(), 1):
        normalized = normalized_source_line(line)
        if normalized:
            index.setdefault(hashlib.sha256(normalized.encode("utf-8")).hexdigest(), []).append(number)
    survivors = [row | {"frozen_final_line_numbers": index[row["normalized_sha256"]]} for row in additions if row["normalized_sha256"] in index]
    return {"commit": commit, "path": path, "patch_sha256": hashlib.sha256(raw).hexdigest(), "added_nonblank_lines": len(additions), "surviving_added_lines": len(survivors), "survivors": survivors, "final_presence": bool(survivors)}


def expected_content_edge(
    route: dict[str, Any], edge: dict[str, Any], source_by_id: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    start = edge["final_start_line"]
    end = edge["final_end_line"]
    final_lines = git_bytes(BASELINE, edge["path"]).decode("utf-8-sig").splitlines()
    final_slice_hashes = {
        hashlib.sha256(normalized_source_line(line).encode("utf-8")).hexdigest()
        for line in final_lines[start - 1 : end]
        if normalized_source_line(line)
    }
    route_final_edge = next(
        item
        for item in route["final_source_edges"]
        if item["source_id"] == edge["source_id"] and item["path"] == edge["path"]
    )
    patch_content = sorted(
        {
            (
                survivor["normalized_sha256"],
                tuple(
                    line_number
                    for line_number in survivor["frozen_final_line_numbers"]
                    if start <= line_number <= end
                ),
            )
            for patch_row in route_final_edge["patch_final_survival"]
            if patch_row["commit"] == edge["patch_commit"]
            for survivor in replay_patch_final_survival(patch_row["commit"], edge["path"])["survivors"]
            if survivor["normalized_sha256"] in final_slice_hashes
            and any(start <= line_number <= end for line_number in survivor["frozen_final_line_numbers"])
        }
    )
    proposal_index: dict[str, list[dict[str, Any]]] = {}
    for proposal_source_id in route["proposal_sources"]:
        proposal_source = source_by_id[proposal_source_id]
        proposal_lines = git_bytes(BASELINE, proposal_source["path"]).decode("utf-8-sig").splitlines()
        for line_number, line in enumerate(proposal_lines, 1):
            normalized = normalized_source_line(line)
            if not normalized:
                continue
            normalized_sha256 = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
            proposal_index.setdefault(normalized_sha256, []).append(
                {
                    "source_id": proposal_source_id,
                    "path": proposal_source["path"],
                    "blob_sha1": proposal_source["blob_sha1"],
                    "line": line_number,
                    "normalized_sha256": normalized_sha256,
                }
            )
    proposal_evidence = sorted(
        (
            proposal_row
            for normalized_sha256, _ in patch_content
            for proposal_row in proposal_index.get(normalized_sha256, [])
        ),
        key=lambda row: (
            row["source_id"], row["path"], row["blob_sha1"],
            row["line"], row["normalized_sha256"],
        ),
    )
    return (
        [
            {"normalized_sha256": normalized_sha256, "frozen_final_line_numbers": list(line_numbers)}
            for normalized_sha256, line_numbers in patch_content
        ],
        proposal_evidence,
    )


def pdfinfo_fields(path: pathlib.Path) -> dict[str, str]:
    output = subprocess.run(
        ["pdfinfo", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=60, check=True,
    ).stdout
    fields: dict[str, str] = {}
    for line in output.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def render_pdf(pdf: pathlib.Path, target: pathlib.Path) -> list[pathlib.Path]:
    target.mkdir(parents=True, exist_ok=True)
    prefix = target / pdf.stem
    subprocess.run(
        ["pdftoppm", "-png", "-r", "96", str(pdf), str(prefix)],
        capture_output=True, timeout=300, check=True,
    )
    pages = list(target.glob(f"{pdf.stem}-*.png"))
    return sorted(pages, key=lambda path: int(path.stem.rsplit("-", 1)[1]))


def verify_build_replay(data: dict[str, Any]) -> None:
    for executable in ("xelatex", "pdfinfo", "pdftotext", "pdftoppm"):
        require(shutil.which(executable) is not None, f"E_BUILD_TOOL_MISSING:{executable}")
    build = data["build_audit"]
    stored_rows = {row["driver"]: row for row in build["rows"]}
    stored_logs = {row["driver"]: row for row in build["log_diagnostics"]}
    with tempfile.TemporaryDirectory(prefix="p063-step62-build-replay-") as tmp:
        temp_root = pathlib.Path(tmp)
        materialized = temp_root / "materialized"
        frozen_root = temp_root / "frozen-pdf"
        raw_tree = run_git("ls-tree", "-rz", "--full-tree", BASELINE, "--", "Claude/docs/v1.0.22", text=False)
        assert isinstance(raw_tree, bytes)
        entries: list[tuple[str, str]] = []
        for record in raw_tree.split(b"\0"):
            if not record:
                continue
            header, raw_path = record.split(b"\t", 1)
            mode, object_type, oid = header.decode("ascii").split()
            require(object_type == "blob" and mode in {"100644", "100755"}, f"E_BUILD_MANIFEST_ENTRY:{header!r}")
            path = raw_path.decode("utf-8")
            require(path.startswith(V1022_PREFIX) and ".." not in pathlib.PurePosixPath(path).parts, f"E_BUILD_MANIFEST_PATH:{path}")
            blob = run_git("cat-file", "blob", oid, text=False)
            assert isinstance(blob, bytes)
            target = materialized.joinpath(*path.split("/"))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob)
            require(hashlib.sha1(f"blob {len(blob)}\0".encode("ascii") + blob).hexdigest() == oid, f"E_BUILD_RAW_BLOB:{path}")
            entries.append((path, oid))
        require(len(entries) == 204, f"E_BUILD_MANIFEST_COUNT:{len(entries)}")
        pdf_paths = {f"{V1022_PREFIX}{driver.removesuffix('.tex')}.pdf" for driver in V1022_BUILD_DRIVERS}
        require(sum(path in pdf_paths for path, _ in entries) == 4, "E_BUILD_FROZEN_PDF_DENOMINATOR")
        frozen_root.mkdir(parents=True)
        for path in sorted(pdf_paths):
            source = materialized.joinpath(*path.split("/"))
            (frozen_root / pathlib.PurePosixPath(path).name).write_bytes(source.read_bytes())
        non_pdf = [(path, oid) for path, oid in entries if path not in pdf_paths]
        require(len(non_pdf) == 200, "E_BUILD_NONPDF_DENOMINATOR")
        doc_root = materialized.joinpath("Claude", "docs", "v1.0.22")
        exit_codes: dict[str, list[int]] = {driver: [] for driver in V1022_BUILD_DRIVERS}
        for _round in range(1, 4):
            for driver in V1022_BUILD_DRIVERS:
                proc = subprocess.run(
                    ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", driver],
                    cwd=doc_root, capture_output=True, timeout=300,
                )
                exit_codes[driver].append(proc.returncode)
                require(proc.returncode == 0, f"E_BUILD_REPLAY_XELATEX:{driver}:{_round}:{proc.returncode}")
        for path, oid in non_pdf:
            current = materialized.joinpath(*path.split("/")).read_bytes()
            require(hashlib.sha1(f"blob {len(current)}\0".encode("ascii") + current).hexdigest() == oid, f"E_BUILD_REPLAY_SOURCE_MUTATION:{path}")
        differences: list[dict[str, Any]] = []
        total_text_pages = 0
        total_render_exact = 0
        for driver in V1022_BUILD_DRIVERS:
            row = stored_rows[driver]
            stem = driver.removesuffix(".tex")
            built_pdf = doc_root / f"{stem}.pdf"
            frozen_pdf = frozen_root / f"{stem}.pdf"
            require(exit_codes[driver] == row["exit_codes"], f"E_BUILD_REPLAY_EXIT_CODES:{driver}")
            require(hashlib.sha256(built_pdf.read_bytes()).hexdigest() != row["frozen_pdf_sha256"], f"E_BUILD_REPLAY_RAW_PDF_UNEXPECTED_EQUAL:{driver}")
            require(hashlib.sha256(frozen_pdf.read_bytes()).hexdigest() == row["frozen_pdf_sha256"], f"E_BUILD_REPLAY_FROZEN_HASH:{driver}")
            frozen_info = pdfinfo_fields(frozen_pdf)
            built_info = pdfinfo_fields(built_pdf)
            require(int(frozen_info["Pages"]) == row["frozen_pages"] and int(built_info["Pages"]) == row["built_pages"], f"E_BUILD_REPLAY_PAGES:{driver}")
            require(frozen_info["Producer"] == build["build_execution"]["frozen_producer"] and frozen_info["PDF version"] == build["build_execution"]["frozen_pdf_version"], f"E_BUILD_REPLAY_FROZEN_PRODUCER:{driver}")
            require(built_info["Producer"] == build["build_execution"]["rebuilt_producer"] and built_info["PDF version"] == build["build_execution"]["rebuilt_pdf_version"], f"E_BUILD_REPLAY_BUILT_PRODUCER:{driver}")
            frozen_text = subprocess.run(["pdftotext", "-layout", str(frozen_pdf), "-"], capture_output=True, timeout=120, check=True).stdout
            built_text = subprocess.run(["pdftotext", "-layout", str(built_pdf), "-"], capture_output=True, timeout=120, check=True).stdout
            require(frozen_text == built_text and hashlib.sha256(frozen_text).hexdigest() == row["text_sha256"], f"E_BUILD_REPLAY_TEXT:{driver}")
            frozen_text_pages = frozen_text.split(b"\f")
            built_text_pages = built_text.split(b"\f")
            if frozen_text_pages and frozen_text_pages[-1] == b"":
                frozen_text_pages.pop()
            if built_text_pages and built_text_pages[-1] == b"":
                built_text_pages.pop()
            require(frozen_text_pages == built_text_pages and len(frozen_text_pages) == row["built_pages"], f"E_BUILD_REPLAY_PAGE_TEXT:{driver}")
            total_text_pages += len(frozen_text_pages)
            frozen_render = render_pdf(frozen_pdf, temp_root / "render-frozen" / stem)
            built_render = render_pdf(built_pdf, temp_root / "render-built" / stem)
            require(len(frozen_render) == len(built_render) == row["built_pages"], f"E_BUILD_REPLAY_RENDER_COUNT:{driver}")
            driver_diff_pages: list[int] = []
            for page_number, (frozen_png, built_png) in enumerate(zip(frozen_render, built_render), 1):
                frozen_image = Image.open(frozen_png).convert("RGB")
                built_image = Image.open(built_png).convert("RGB")
                require(frozen_image.size == built_image.size, f"E_BUILD_REPLAY_RENDER_SIZE:{driver}:{page_number}")
                frozen_bytes = frozen_image.tobytes()
                built_bytes = built_image.tobytes()
                changed = sum(frozen_bytes[index:index + 3] != built_bytes[index:index + 3] for index in range(0, len(frozen_bytes), 3))
                if changed == 0:
                    total_render_exact += 1
                    continue
                driver_diff_pages.append(page_number)
                bbox = ImageChops.difference(frozen_image, built_image).getbbox()
                total_pixels = frozen_image.width * frozen_image.height
                differences.append({"driver": driver, "page": page_number, "width": frozen_image.width, "height": frozen_image.height, "changed_pixels": changed, "total_pixels": total_pixels, "changed_pixel_fraction": changed / total_pixels, "changed_pixel_percent": 100 * changed / total_pixels, "bbox": list(bbox) if bbox else None, "frozen_png_sha256": hashlib.sha256(frozen_png.read_bytes()).hexdigest(), "built_png_sha256": hashlib.sha256(built_png.read_bytes()).hexdigest()})
            require(driver_diff_pages == row["render_diff_pages"], f"E_BUILD_REPLAY_RENDER_PAGES:{driver}")
            log = doc_root / f"{stem}.log"
            log_row = stored_logs[driver]
            require(len(hashlib.sha256(log.read_bytes()).hexdigest()) == len(log_row["log_sha256"]) == 64, f"E_BUILD_REPLAY_LOG_HASH_FORMAT:{driver}")
            log_lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
            require(len(log_lines) == log_row["log_lines"], f"E_BUILD_REPLAY_LOG_LINES:{driver}")
            diagnostic_patterns = {
                "multiply_defined_label_log_lines": re.compile(r"Label `(?:swiderska2019|LastPage)' multiply defined\."),
                "missing_character_log_lines": re.compile(r"^Missing character:"),
                "overfull_hbox_log_lines": re.compile(r"^Overfull \\hbox"),
                "overfull_vbox_log_lines": re.compile(r"^Overfull \\vbox"),
                "infinite_glue_log_lines": re.compile(r"Infinite glue shrinkage"),
                "font_shape_summary_log_lines": re.compile(r"Some font shapes were not available, defaults substituted\."),
            }
            for key, pattern in diagnostic_patterns.items():
                observed = [number for number, line in enumerate(log_lines, 1) if pattern.search(line)]
                require(observed == log_row[key], f"E_BUILD_REPLAY_LOG_DIAGNOSTIC:{driver}:{key}:{observed}")
        require(total_text_pages == 133 and total_render_exact == 125, "E_BUILD_REPLAY_TOTALS")
        require(differences == build["render_differences"], "E_BUILD_REPLAY_RENDER_LEDGER")
    print("PASS_P063_STEP62_BUILD_REPLAY raw=204/204 source=200/200 runs=12/12 text=133/133 render=125/133 cleanup=PASS")


def source_role(source: dict[str, Any]) -> str:
    role = source.get("process_authority_subtype")
    if role is None and source["partition"] == "STATUS_MACHINE_PROCESS":
        return "S_SELF_REPORT_OR_STATUS"
    require(role in ROLE_KEY, f"E_SOURCE_ROLE_UNKNOWN:{source['source_id']}:{role}")
    return str(role)


def validate_semantics(
    data: dict[str, Any], topology: dict[str, Any], provisional: dict[str, Any],
    projection: dict[str, Any] | None = None,
) -> None:
    require(data["schema"] == "P063_STEP62_REVIEW_ADOPTION_CLOSURE_V1", "E_SCHEMA")
    require(data["phase"] == 63 and data["step"] == 62, "E_PHASE_STEP")
    require(data["input_commit"] == PARENT and data["frozen_baseline"] == BASELINE, "E_INPUT_IDENTITY")
    require(data["gate"] == GATE, "E_GATE")
    require(data["result_first"] == {"sentinel": SENTINEL, "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN"}, "E_RESULT_FIRST")

    source_by_id = {row["source_id"]: row for row in topology["sources"]}
    competing_source = {
        row["source_id"]: row for row in topology["sources"]
        if row["partition"] == "COMPETING_REVIEW_CANDIDATE"
    }
    require(len(competing_source) == 125, "E_TOPOLOGY_COMPETING_DENOMINATOR")
    occurrences = data["competing_occurrences"]
    require(len(occurrences) == 125, "E_OCCURRENCE_COUNT")
    require(len({row["source_id"] for row in occurrences}) == 125, "E_OCCURRENCE_ID_DUPLICATE")
    require({row["source_id"] for row in occurrences} == set(competing_source), "E_OCCURRENCE_ID_COVERAGE")
    for row in occurrences:
        src = competing_source[row["source_id"]]
        require(row["path"] == src["path"], f"E_OCCURRENCE_PATH:{row['source_id']}")
        require(row["blob_sha1"] == src["blob_sha1"] and row["sha256"] == src["sha256"], f"E_OCCURRENCE_BLOB:{row['source_id']}")
        require(row["process_role"] == src["process_authority_subtype"], f"E_OCCURRENCE_ROLE:{row['source_id']}")
        require(row["final_adoption_authority"] is False, f"E_OCCURRENCE_AUTHORITY:{row['source_id']}")
    require(sum(row["physical_lines"] for row in occurrences) == 17072, "E_OCCURRENCE_PHYSICAL")
    require(sum(row["nonblank_lines"] for row in occurrences) == 13926, "E_OCCURRENCE_NONBLANK")
    require(sum(row["bytes"] for row in occurrences) == 1800475, "E_OCCURRENCE_BYTES")

    families = data["proposal_families"]
    require(len(families) == 22, "E_FAMILY_COUNT")
    require({row["family_id"]: row["occurrence_count"] for row in families} == EXPECTED_FAMILY_COUNTS, "E_FAMILY_COUNTS")
    family_ids = [item for row in families for item in row["source_ids"]]
    require(len(family_ids) == len(set(family_ids)) == 125, "E_FAMILY_OCCURRENCE_DUPLICATE")
    require(set(family_ids) == set(competing_source), "E_FAMILY_OCCURRENCE_COVERAGE")
    for row in families:
        require(row["authority_ceiling"] == "FAMILY_GROUPING_ONLY_NO_ADOPTION_INFERENCE", f"E_FAMILY_AUTHORITY:{row['family_id']}")
        require(bool(row["family_decision"]), f"E_FAMILY_DECISION:{row['family_id']}")

    routes = data["adoption_routes"]
    expected_route_ids = {
        "P063-S62-ADOPT-000", "P063-S62-ADOPT-001", "P063-S62-ADOPT-002", "P063-S62-ADOPT-003",
        "P063-S62-ADOPT-004", "P063-S62-ADOPT-005", "P063-S62-ADOPT-006", "P063-S62-ADOPT-007",
        "P063-S62-ADOPT-008", "P063-S62-ADOPT-009", "P063-S62-CHAIN-008", "P063-S62-CHAIN-009",
        "P063-S62-CHAIN-010", "P063-S62-CHAIN-011", "P063-S62-CHAIN-012", "P063-S62-CHAIN-013",
        "P063-S62-CHAIN-014", "P063-S62-CHAIN-014B", "P063-S62-CHAIN-015",
    }
    require(len(routes) == 19 and {row["route_id"] for row in routes} == expected_route_ids, "E_ROUTE_IDS")
    route_competing_coverage: set[str] = set()
    valid_findings = {f"INTENT-PROV-{number:04d}" for number in range(96, 192)}
    for route in routes:
        rid = route["route_id"]
        require(route["finding_ids"] == [row["finding_id"] for row in route["finding_projections"]], f"E_ROUTE_FINDING_PROJECTION:{rid}")
        require(
            route["finding_edge_authority"]
            is any(row["proposal_to_patch_to_final_content_edge"] for row in route["finding_projections"]),
            f"E_ROUTE_FINDING_AUTHORITY:{rid}",
        )
        require(
            route["finding_patch_final_current_state_authority"] is bool(route["finding_projections"]),
            f"E_ROUTE_PATCH_FINAL_AUTHORITY:{rid}",
        )
        require(set(route["related_finding_ids"]) <= valid_findings, f"E_ROUTE_RELATED_FINDING:{rid}")
        require(set(route["finding_ids"]) <= set(route["related_finding_ids"]), f"E_ROUTE_FINDING_SCOPE:{rid}")
        typed_ids: list[str] = []
        for role, key in ROLE_KEY.items():
            for source_id in route[key]:
                require(source_id in source_by_id, f"E_ROUTE_SOURCE_UNKNOWN:{rid}:{source_id}")
                require(source_role(source_by_id[source_id]) == role, f"E_ROUTE_TYPED_ROLE:{rid}:{source_id}")
                typed_ids.append(source_id)
                if source_id in competing_source:
                    route_competing_coverage.add(source_id)
        require(len(typed_ids) == len(set(typed_ids)), f"E_ROUTE_TYPED_DUPLICATE:{rid}")
        require({row["source_id"] for row in route["typed_occurrence_sources"]} == set(typed_ids), f"E_ROUTE_TYPED_ROWS:{rid}")
        if route["decision_sources"]:
            require(route["decision_evidence_state"] == "DIRECT", f"E_ROUTE_DECISION_STATE:{rid}")
            require(route["ground_not_found"] is None, f"E_ROUTE_FALSE_GNF:{rid}")
        else:
            require(route["decision_evidence_state"].startswith("GROUND_NOT_FOUND"), f"E_ROUTE_GNF_STATE:{rid}")
            gnf = route["ground_not_found"]
            require(gnf["searched_universe"] == "ALL_125_COMPETING_REVIEWER_CANDIDATE_OCCURRENCES_FULL_TEXT", f"E_ROUTE_GNF_UNIVERSE:{rid}")
            require(gnf["inspected_source_count"] == 125 and len(gnf["inspected_sources_sha256"]) == 64, f"E_ROUTE_GNF_DENOMINATOR:{rid}")
            require(rid in gnf["query"] and bool(gnf["source_context"]) and bool(gnf["owner"]), f"E_ROUTE_GNF_CONTEXT:{rid}")
        require(route["external_truth"] is False, f"E_ROUTE_EXTERNAL_TRUTH:{rid}")
        if rid == "P063-S62-CHAIN-015":
            require(route["patch_commits"] == [] and route["final_source_edges"] == [], "E_V23_FALSE_ADOPTION")
        for edge in route["final_source_edges"]:
            source = source_by_id[edge["source_id"]]
            require(source["partition"] == "FINAL_RELEASE_SURFACE", f"E_ROUTE_FINAL_PARTITION:{rid}")
            require(edge["path"] == source["path"] and edge["blob_sha1"] == source["blob_sha1"] and edge["sha256"] == source["sha256"], f"E_ROUTE_FINAL_IDENTITY:{rid}")
            expected_survival = [replay_patch_final_survival(row["commit"], edge["path"]) for row in edge["patch_final_survival"]]
            require(edge["patch_final_survival"] == expected_survival, f"E_ROUTE_PATCH_FINAL_REPLAY:{rid}:{edge['path']}")
            presence = any(row["final_presence"] for row in expected_survival)
            require(edge["final_adoption_authority"] is presence and edge["external_truth"] is False, f"E_ROUTE_FINAL_AUTHORITY:{rid}")
            require(edge["final_presence_state"] == ("PATCH_ADDITION_SURVIVES_IN_FROZEN_FINAL" if presence else "PATCH_ADDITION_ABSENT_FROM_FROZEN_FINAL"), f"E_ROUTE_FINAL_PRESENCE:{rid}")
        for finding_projection in route["finding_projections"]:
            require(finding_projection["finding_id"] in route["related_finding_ids"], f"E_ROUTE_PROJECTION_SCOPE:{rid}")
            require(finding_projection["patch_to_final_current_state_edge"] is True and finding_projection["external_truth"] is False, f"E_ROUTE_PROJECTION_AUTHORITY:{rid}")
            require(bool(finding_projection["final_source_edges"]), f"E_ROUTE_PROJECTION_EMPTY:{rid}")
            proposal_edge_observed = False
            for edge in finding_projection["final_source_edges"]:
                lines = git_bytes(BASELINE, edge["path"]).decode("utf-8-sig").splitlines()
                observed_hash = hashlib.sha256("\n".join(lines[edge["final_start_line"] - 1 : edge["final_end_line"]]).encode("utf-8")).hexdigest()
                require(observed_hash == edge["final_slice_sha256"] and bool(edge["surviving_patch_line_numbers"]), f"E_ROUTE_PROJECTION_SLICE:{rid}")
                require(all(edge["final_start_line"] <= number <= edge["final_end_line"] for number in edge["surviving_patch_line_numbers"]), f"E_ROUTE_PROJECTION_LINES:{rid}")
                expected_patch_content, expected_proposal_evidence = expected_content_edge(route, edge, source_by_id)
                require(edge["surviving_patch_content"] == expected_patch_content, f"E_ROUTE_PATCH_CONTENT:{rid}")
                require(edge["proposal_content_evidence"] == expected_proposal_evidence, f"E_ROUTE_PROPOSAL_EVIDENCE:{rid}")
                expected_proposal_edge = bool(expected_proposal_evidence)
                require(edge["patch_to_final_current_state_edge"] is True, f"E_ROUTE_PATCH_EDGE_BOOL:{rid}")
                require(edge["proposal_to_patch_to_final_content_edge"] is expected_proposal_edge, f"E_ROUTE_PROPOSAL_EDGE_BOOL:{rid}")
                require(
                    edge["content_edge_type"]
                    == ("PROPOSAL_PATCH_FINAL_CONTENT_EDGE" if expected_proposal_edge else "PATCH_TO_FINAL_CURRENT_STATE_EDGE"),
                    f"E_ROUTE_CONTENT_EDGE_TYPE:{rid}",
                )
                proposal_edge_observed = proposal_edge_observed or expected_proposal_edge
            require(
                finding_projection["proposal_to_patch_to_final_content_edge"] is proposal_edge_observed,
                f"E_ROUTE_PROJECTION_PROPOSAL_BOOL:{rid}",
            )
    require(route_competing_coverage == set(competing_source), "E_ROUTE_COMPETING_COVERAGE")

    records = {row["claim_id"]: row for row in provisional["records"]}
    topology_routes = {row["finding_id"]: row for row in topology["phase057_finding_routes"]}
    observations = {row["path"]: row for row in topology["phase057_observation_inputs"]}
    findings = data["finding_adjudications"]
    projections_by_finding: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for route in routes:
        for finding_projection in route["finding_projections"]:
            projections_by_finding.setdefault(finding_projection["finding_id"], []).append(
                (route["route_id"], finding_projection)
            )
    require(len(findings) == 96, "E_FINDING_COUNT")
    require([row["numeric_id"] for row in findings] == list(range(96, 192)), "E_FINDING_SEQUENCE")
    for row in findings:
        number = row["numeric_id"]
        finding_id = f"INTENT-PROV-{number:04d}"
        require(row["finding_id"] == finding_id, f"E_FINDING_ID:{number}")
        require(row["state"] == EXPECTED_STATES[number], f"E_FINDING_STATE:{finding_id}")
        require(row["candidate_source_routes"] == topology_routes[finding_id]["candidate_v1022_source_ids"], f"E_FINDING_CANDIDATE_ROUTE:{finding_id}")
        expected_proposals = [source_id for source_id in row["candidate_source_routes"] if source_by_id[source_id]["partition"] == "COMPETING_REVIEW_CANDIDATE"]
        require(row["proposal_sources"] == expected_proposals, f"E_FINDING_PROPOSAL_ROUTE:{finding_id}")
        has_direct_edge = number in CURRENT_FINAL_EVIDENCE_IDS
        require(bool(row["decision_routes"]) is has_direct_edge, f"E_FINDING_DIRECT_EDGE:{finding_id}")
        require(bool(row["final_source_edges"]) is has_direct_edge and row["build_page_edges"] == [], f"E_FINDING_FINAL_EDGE:{finding_id}")
        linked_projections = projections_by_finding.get(finding_id, [])
        expected_patch_edges = [
            {"route_id": route_id} | edge
            for route_id, finding_projection in linked_projections
            for edge in finding_projection["final_source_edges"]
        ]
        expected_proposal_edges = [
            edge for edge in expected_patch_edges
            if edge["proposal_to_patch_to_final_content_edge"]
        ]
        require(row["patch_final_current_state_edges"] == expected_patch_edges, f"E_FINDING_PATCH_FINAL_EDGE:{finding_id}")
        require(row["proposal_patch_final_content_edges"] == expected_proposal_edges, f"E_FINDING_PROPOSAL_CONTENT_EDGE:{finding_id}")
        require(bool(row["patch_final_current_state_edges"]) is has_direct_edge, f"E_FINDING_CONTENT_EDGE:{finding_id}")
        require(all(edge["proposal_to_patch_to_final_content_edge"] is True for edge in row["proposal_patch_final_content_edges"]), f"E_FINDING_CONTENT_EDGE_AUTHORITY:{finding_id}")
        expected_state_basis = (
            "DIRECT_PROPOSAL_PATCH_FINAL_CONTENT_EDGE"
            if expected_proposal_edges
            else (
                "DIRECT_PATCH_FINAL_CURRENT_STATE_EDGE_WITHOUT_PROPOSAL_CONTENT_MATCH"
                if expected_patch_edges
                else (
                    "DIRECT_FINAL_SOURCE_STATE_WITHOUT_SURVIVING_PROPOSAL_PATCH_EDGE"
                    if number in CURRENT_FINAL_EVIDENCE_IDS
                    else "PHASE057_FULLTEXT_OBSERVATION_WITHOUT_SYNTHETIC_ADOPTION_EDGE"
                )
            )
        )
        require(row["state_basis"] == expected_state_basis, f"E_FINDING_STATE_BASIS:{finding_id}")
        require(row["external_truth"] is False, f"E_FINDING_EXTERNAL_TRUTH:{finding_id}")
        require(row["evidence_state"] == "DIRECT" and row["searched_universe"] is None and row["query"] is None, f"E_FINDING_EVIDENCE_STATE:{finding_id}")
        require(bool(row["owner"]) and bool(row["acceptance_criterion"]), f"E_FINDING_ROUTING:{finding_id}")
        require(row["patch_confirmation_required"] is (number in PATCH_CEILING_IDS), f"E_FINDING_PATCH_CEILING:{finding_id}")
        evidence = row["state_evidence"]
        require(bool(evidence), f"E_FINDING_EVIDENCE_EMPTY:{finding_id}")
        source_record = records[finding_id]
        observation = observations[source_record["source_path"]]
        require(evidence[0]["path"] == source_record["source_path"], f"E_FINDING_OBSERVATION_PATH:{finding_id}")
        require(evidence[0]["lines"] == source_record["source_lines"], f"E_FINDING_OBSERVATION_LINES:{finding_id}")
        require(evidence[0]["source_block_sha256"] == source_record["source_block_sha256"], f"E_FINDING_OBSERVATION_HASH:{finding_id}")
        require(evidence[0]["worktree_sha256_attested_by_step58"] == observation["sha256"], f"E_FINDING_ATTESTATION:{finding_id}")
        has_final = any(item["evidence_role"] == "FROZEN_FINAL_SOURCE_CURRENT_STATE" for item in evidence)
        require(has_final is (number in CURRENT_FINAL_EVIDENCE_IDS), f"E_FINDING_FINAL_EVIDENCE:{finding_id}")
    require(Counter(row["state"] for row in findings) == Counter({"HISTORICAL_ONLY": 30, "OPEN": 45, "RESOLVED_IN_V1022": 8, "SUPERSEDED": 2, "UNVERIFIED": 11}), "E_FINDING_STATE_COUNTS")

    build = data["build_audit"]
    require(build["materialization"] == "FROZEN_GIT_RAW_BLOB_BYTES_IN_EXTERNAL_TEMP_DIRECTORY", "E_BUILD_MATERIALIZATION")
    require(build["raw_blob_materialization_verified"] == "204/204", "E_BUILD_RAW_BLOBS")
    require(build["non_pdf_git_object_identity_before_build"] == "200/200" and build["non_pdf_git_object_identity_after_build"] == "200/200", "E_BUILD_SOURCE_MUTATION")
    require(build["drivers"] == 4 and build["passes_per_driver"] == 3 and build["runs_exit_zero"] == "12/12", "E_BUILD_RUNS")
    require(build["frozen_pdf_page_total"] == 133 and build["page_text_equal"] == "133/133", "E_BUILD_PAGES")
    require(build["render_exact"] == "125/133" and build["render_difference_pages"] == 8, "E_BUILD_RENDER")
    require(build["built_pdf_sha256_authority"] == "WITNESS_RUN_ONLY_NOT_REPLAY_INVARIANT; PDF_METADATA_DEPENDS_ON_BUILD_TIME", "E_BUILD_PDF_HASH_AUTHORITY")
    require(build["log_sha256_authority"] == "WITNESS_RUN_ONLY_NOT_REPLAY_INVARIANT; TRANSCRIPT_INCLUDES_RUN_METADATA", "E_BUILD_LOG_HASH_AUTHORITY")
    execution = build["build_execution"]
    require(execution["driver_order"] == ["appendix_phase_separation.tex", "ch1_graphite_v1.0.22.tex", "ch2_lco_v1.0.22.tex", "ch3_si_v1.0.22.tex"], "E_BUILD_EXECUTION_ORDER")
    require(len(execution["run_order"]) == 12 and execution["build_command_argv"] == ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "<driver>"], "E_BUILD_EXECUTION_COMMAND")
    require(execution["host_environment"]["render_dpi"] == 96 and execution["cleanup_required"] is True, "E_BUILD_EXECUTION_ENVIRONMENT")
    require(execution["frozen_producer"] == "xdvipdfmx (20220710)" and execution["rebuilt_producer"] == "MiKTeX-dvipdfmx (20250413)", "E_BUILD_PRODUCER")
    rows = build["rows"]
    require([row["driver"] for row in rows] == ["appendix_phase_separation.tex", "ch1_graphite_v1.0.22.tex", "ch2_lco_v1.0.22.tex", "ch3_si_v1.0.22.tex"], "E_BUILD_DRIVERS")
    require([row["built_pages"] for row in rows] == [8, 83, 25, 17], "E_BUILD_PAGE_ROWS")
    require(all(row["exit_codes"] == [0, 0, 0] and row["undefined_refs"] == 0 and row["undefined_citations"] == 0 for row in rows), "E_BUILD_DIAGNOSTICS")
    require(rows[0]["multiply_defined_labels"] == [], "E_APPENDIX_LABELS")
    require(all(row["multiply_defined_labels"] == ["swiderska2019", "LastPage"] for row in rows[1:]), "E_CHAPTER_LABELS")
    require(rows[3]["missing_glyphs"] == [{"char": "μ", "count": 2, "frozen_and_built_loss": True, "log_lines": [1226, 1227], "pdf_page": 7, "source_blob": "ea88ed0730bb8cbc5f48cd3cacc42fab93f88ded", "source_lines": [70, 73], "source_path": "Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex"}], "E_MISSING_GLYPH")
    require(all(row["raw_pdf_equal"] is False and row["text_equal"] is True for row in rows), "E_BUILD_COMPARISON")
    require([row["render_diff_pages"] for row in rows] == [[], [39, 64, 83], [5, 14, 15], [5, 13]], "E_RENDER_DIFF_PAGES")
    require([row["log_sha256"] for row in build["log_diagnostics"]] == ["183700cb4a40d92e1b31b4f444af52d181b21ce152a63cdba74b58e8dabe21f2", "ced48fbb49b8f7e9e53c4fe80301d99c5b13832c710ffd4307aac43984ccded4", "29f64af94a3ebb6b6fe8ea83b866b82832b5bb592658f1f4d4defce6b1755732", "01ff62a8290e2a6306c5b1428d3d4c7ab4b5d254f0a3b13406e485fefd5733f4"], "E_BUILD_LOG_HASHES")
    require([row["multiply_defined_label_log_lines"] for row in build["log_diagnostics"]] == [[], [929, 932], [930, 933], [931, 935]], "E_BUILD_LABEL_LOG_LINES")
    require(build["log_diagnostics"][3]["missing_character_log_lines"] == [1226, 1227], "E_BUILD_GLYPH_LOG_LINES")
    require(len(build["render_differences"]) == 8 and max(row["changed_pixel_percent"] for row in build["render_differences"]) == 0.08097238639753629, "E_BUILD_RENDER_LEDGER")

    code = data["code_mention_boundary"]
    require(code["policy_pass"] is False and code["external_scientific_authority"] is False, "E_CODE_POLICY_AUTHORITY")
    require(code["implementation_allowlist_exact_paths"] == IMPLEMENTATION_APPENDIX_ALLOWLIST, "E_CODE_ALLOWLIST")
    require(code["misclassified_previous_surface"] == {"path": CH3_MAIN_IMPLEMENTATION_SECTION, "root_driver": "Claude/docs/v1.0.22/ch3_si_v1.0.22.tex", "root_input_line": 27, "appendix_command_before_input": False, "corrected_class": "IMPLEMENTATION_MAIN_BODY_RELOCATION_REQUIRED"}, "E_CODE_CH3_MAIN_BOUNDARY")
    replay_code_mention_rows(code)
    main_class = next(row for row in code["classes"] if row["class"] == "PHYSICS_MAIN_BODY_RENDERED")
    require((main_class["line_rows"], main_class["occurrences"]) == (35, 43), "E_CODE_MAIN_COUNT")
    ch3_class = next(row for row in code["classes"] if row["class"] == "IMPLEMENTATION_MAIN_BODY_RELOCATION_REQUIRED")
    require((ch3_class["line_rows"], ch3_class["occurrences"]) == (23, 37), "E_CODE_CH3_MAIN_COUNT")
    appendix_class = next(row for row in code["classes"] if row["class"] == "IMPLEMENTATION_APPENDIX_RENDERED")
    require((appendix_class["line_rows"], appendix_class["occurrences"]) == (118, 182), "E_CODE_APPENDIX_COUNT")
    refinement = code["physics_main_body_manual_refinement"]
    require(sum(row["line_rows"] for row in refinement["mutually_exclusive_classes"]) == 58, "E_CODE_CLASS_ROWS")
    require(sum(row["occurrences"] for row in refinement["mutually_exclusive_classes"]) == 80, "E_CODE_CLASS_OCCURRENCES")
    require((refinement["actionable_line_rows"], refinement["actionable_occurrences"]) == (58, 80), "E_CODE_ACTIONABLE")
    require((refinement["false_positive_line_rows"], refinement["false_positive_occurrences"]) == (0, 0), "E_CODE_FALSE_POSITIVE")

    state = data["state_chronology"]
    require(len(state["status_sources"]) == 10, "E_STATUS_SOURCE_COUNT")
    require(len(state["commit_chronology"]) == 8, "E_CHRONOLOGY_COUNT")
    require(len(state["conflicts"]) == 11, "E_STATE_CONFLICT_COUNT")
    require([row["conflict_id"] for row in state["conflicts"]] == [f"P063-S62-STATE-{number:03d}" for number in range(1, 12)], "E_STATE_CONFLICT_IDS")
    require(state["precedence_rule"] == "FINAL_SOURCE_AND_COMMIT_CHRONOLOGY_OUTRANK_STALE_SELF_REPORT", "E_STATE_PRECEDENCE")
    counts = data["counts"]
    require(counts["competing_occurrences"] == 125 and counts["proposal_families"] == 22, "E_COUNTS_COMPETING")
    require(counts["competing_physical_lines"] == 17072 and counts["competing_nonblank_lines"] == 13926 and counts["competing_bytes"] == 1800475, "E_COUNTS_EXTENT")
    require(counts["family_occurrences"] == EXPECTED_FAMILY_COUNTS, "E_COUNTS_FAMILY")
    require(counts["finding_adjudications"] == 96 and counts["adoption_routes"] == 19 and counts["build_drivers"] == 4 and counts["state_conflicts"] == 11, "E_COUNTS_CLOSURE")
    require(counts["finding_states"] == {"HISTORICAL_ONLY": 30, "OPEN": 45, "RESOLVED_IN_V1022": 8, "SUPERSEDED": 2, "UNVERIFIED": 11}, "E_COUNTS_STATES")
    require(all(value is False for value in data["authority"].values()), "E_AUTHORITY_PROMOTION")
    require(set(data["authority"]) == {"proposal_as_adoption", "review_as_adoption", "cherrypick_as_source_patch", "build_as_science", "external_scientific", "primary_literature", "material", "experimental", "canonical", "final_release", "publication"}, "E_AUTHORITY_SCHEMA")
    if projection is not None:
        require(data == projection, "E_EXACT_PROJECTION")


def validate_git_evidence(data: dict[str, Any], topology: dict[str, Any]) -> None:
    source_by_id = {row["source_id"]: row for row in topology["sources"]}
    for name, link in data["evidence_links"].items():
        raw = git_bytes(PARENT, link["path"])
        require(link["commit"] == PARENT, f"E_LINK_COMMIT:{name}")
        require(link["git_blob"] == str(run_git("rev-parse", f"{PARENT}:{link['path']}")).strip(), f"E_LINK_BLOB:{name}")
        require(link["sha256"] == hashlib.sha256(raw).hexdigest() and link["bytes"] == len(raw), f"E_LINK_HASH:{name}")
        if link["path"].endswith(".json"):
            require(link["traversal"] == traversal_count(strict_load_bytes(raw)), f"E_LINK_TRAVERSAL:{name}")
    for route in data["adoption_routes"]:
        changed_union: set[str] = set()
        require(len(route["patch_commits"]) == len(route["patch_evidence"]), f"E_PATCH_COUNT:{route['route_id']}")
        for commit, evidence in zip(route["patch_commits"], route["patch_evidence"]):
            require(evidence["commit"] == commit, f"E_PATCH_COMMIT:{route['route_id']}")
            subject = str(run_git("show", "-s", "--format=%s", commit)).rstrip("\r\n")
            changed = str(run_git("diff-tree", "--no-commit-id", "--name-only", "-r", commit, "--", "Claude/docs/v1.0.22")).splitlines()
            require(evidence["subject"] == subject and evidence["changed_paths"] == changed, f"E_PATCH_EVIDENCE:{route['route_id']}:{commit}")
            changed_union.update(changed)
        for edge in route["final_source_edges"]:
            require(edge["path"] in changed_union, f"E_FINAL_EDGE_PATCH_MEMBERSHIP:{route['route_id']}:{edge['path']}")
    for finding in data["finding_adjudications"]:
        for evidence in finding["state_evidence"]:
            raw = git_bytes(evidence["commit"], evidence["path"])
            lines = raw.splitlines(keepends=True)
            start, end = evidence["lines"]
            require(1 <= start <= end <= len(lines), f"E_EVIDENCE_RANGE:{finding['finding_id']}")
            require(evidence["git_blob"] == str(run_git("rev-parse", f"{evidence['commit']}:{evidence['path']}")).strip(), f"E_EVIDENCE_BLOB:{finding['finding_id']}")
            require(evidence["slice_sha256"] == hashlib.sha256(b"".join(lines[start - 1:end])).hexdigest(), f"E_EVIDENCE_SLICE:{finding['finding_id']}")
            if evidence["evidence_role"] == "FROZEN_FINAL_SOURCE_CURRENT_STATE":
                source = source_by_id[evidence["source_id"]]
                require(evidence["commit"] == BASELINE and evidence["final_blob_sha1"] == source["blob_sha1"], f"E_FINAL_EVIDENCE_IDENTITY:{finding['finding_id']}")
                subprocess.run(["git", "merge-base", "--is-ancestor", evidence["patch_commit"], BASELINE], cwd=REPO, check=True, timeout=60)
    for row in data["build_audit"]["rows"]:
        root = source_by_id[row["root_source_id"]]
        pdf = source_by_id[row["pdf_source_id"]]
        require(row["root_blob"] == root["blob_sha1"], f"E_BUILD_ROOT_BLOB:{row['driver']}")
        require(row["frozen_pdf_sha256"] == hashlib.sha256(git_bytes(BASELINE, pdf["path"])).hexdigest(), f"E_BUILD_FROZEN_PDF:{row['driver']}")
    for conflict in data["state_chronology"]["conflicts"]:
        for evidence in conflict["stale_claims"] + conflict["current_evidence"]:
            raw = git_bytes(evidence.get("commit", BASELINE), evidence["path"])
            commit = evidence.get("commit", BASELINE)
            require(evidence["git_blob"] == str(run_git("rev-parse", f"{commit}:{evidence['path']}")).strip(), f"E_STATE_BLOB:{conflict['conflict_id']}")
            require(evidence["source_sha256"] == hashlib.sha256(raw).hexdigest() and evidence["source_bytes"] == len(raw), f"E_STATE_SOURCE_HASH:{conflict['conflict_id']}")
            if evidence["lines"]:
                start, end = evidence["lines"]
                require(1 <= start <= end <= len(raw.splitlines()), f"E_STATE_SPAN:{conflict['conflict_id']}")
                require(evidence["slice_sha256"] == hashlib.sha256(b"".join(raw.splitlines(keepends=True)[start - 1 : end])).hexdigest(), f"E_STATE_SLICE:{conflict['conflict_id']}")
            else:
                require(evidence["slice_sha256"] is None, f"E_STATE_EMPTY_SLICE:{conflict['conflict_id']}")


def validate_recovery_texts(result: str, active: str, parent: str, handover: str, matrix_sha256: str) -> None:
    required = [GATE, SENTINEL, "PENDING_AT_PRECOMMIT_BY_DESIGN", PARENT,
                matrix_sha256, "125/125", "22/22", "96/96",
                "12/12", "8/83/25/17", "58` rows / `80", "8/8", SUBJECT] + EXACT_PATHS
    for token in required:
        require(token in result, f"E_RESULT_TOKEN:{token}")
    result_lines = result.splitlines()
    require([line for line in result_lines if line.startswith("Gate:")] == [f"Gate: `{GATE}`"], "E_RESULT_GATE_LINE")
    require([line for line in result_lines if line.startswith("Terminal:")] == [f"Terminal: `{GATE}`"], "E_RESULT_TERMINAL_LINE")
    gate_surface = [
        line for line in result_lines
        if line.startswith(("Gate:", "Terminal:", "Overall gate:", "Overall status:"))
    ]
    require(gate_surface == [f"Gate: `{GATE}`", f"Terminal: `{GATE}`"], "E_RESULT_GATE_SURFACE")

    active_phase_rows = [line for line in active.splitlines() if line.startswith("| 063 |")]
    active_step_rows = [line for line in active.splitlines() if line.startswith("| Step 62 |")]
    require(len(active_phase_rows) == 1 and len(active_step_rows) == 1, "E_ACTIVE_LEDGER_CURRENT_ROW_COUNT")
    require(all(token in active_phase_rows[0] for token in ("IN_PROGRESS", GATE, "PENDING_AT_PRECOMMIT_BY_DESIGN", "58/80")), "E_ACTIVE_LEDGER_PHASE_ROW")
    require(all(token in active_step_rows[0] for token in (GATE, "PENDING_AT_PRECOMMIT_BY_DESIGN", "58/80", "Step 63.1")), "E_ACTIVE_LEDGER_STEP_ROW")
    require(all("FAIL" not in row and "CONDITIONAL" not in row for row in active_phase_rows + active_step_rows), "E_ACTIVE_LEDGER_CONFLICT")

    parent_rows = [line for line in parent.splitlines() if line.startswith("| 063 |")]
    require(len(parent_rows) == 1, "E_PARENT_LEDGER_CURRENT_ROW_COUNT")
    require(all(token in parent_rows[0] for token in ("IN_PROGRESS", GATE, "PENDING_AT_PRECOMMIT_BY_DESIGN", "58/80")), "E_PARENT_LEDGER_PHASE_ROW")
    require("FAIL" not in parent_rows[0] and "CONDITIONAL" not in parent_rows[0], "E_PARENT_LEDGER_CONFLICT")

    handover_rows = [line for line in handover.splitlines() if line.startswith("| Phase 063 Step 62 |")]
    require(len(handover_rows) == 1, "E_HANDOVER_CURRENT_ROW_COUNT")
    require(all(token in handover_rows[0] for token in (GATE, "PENDING_AT_PRECOMMIT_BY_DESIGN", "58/80", "Step 63.1")), "E_HANDOVER_CURRENT_ROW")
    require("FAIL" not in handover_rows[0] and "CONDITIONAL" not in handover_rows[0], "E_HANDOVER_CONFLICT")
    expected_status = "15. 현재 Phase 상태: Phase 063 `IN_PROGRESS`, Current checkpoint: Step 62 precommit `PASS_P063_STEP62_REVIEW_ADOPTION_CLOSURE_WITH_CONCERNS`"
    require([line for line in handover.splitlines() if line.startswith("15. 현재 Phase 상태:")] == [expected_status], "E_HANDOVER_STATUS_LINE")


def validate_result() -> None:
    subprocess.run(
        [sys.executable, "-B", str(REPO / BUILDER_REL), "--check"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="strict",
        timeout=240, check=True,
    )
    matrix_raw = (REPO / MATRIX_REL).read_bytes()
    validate_recovery_texts(
        (REPO / RESULT_REL).read_text(encoding="utf-8"),
        (REPO / ACTIVE_LEDGER).read_text(encoding="utf-8"),
        (REPO / PARENT_LEDGER).read_text(encoding="utf-8"),
        (REPO / HANDOVER).read_text(encoding="utf-8"),
        hashlib.sha256(matrix_raw).hexdigest(),
    )


def git_boundary_negative_fixture() -> tuple[int, int]:
    with tempfile.TemporaryDirectory(prefix="p063-step62-git-boundary-") as tmp:
        root = pathlib.Path(tmp)
        work = root / "work"
        origin = root / "origin.git"

        def fixture_git(cwd: pathlib.Path, *args: str) -> str:
            return subprocess.run(
                ["git", *args], cwd=cwd, capture_output=True, text=True,
                encoding="utf-8", errors="strict", timeout=60, check=True,
            ).stdout.strip()

        def fixture_git_bytes(cwd: pathlib.Path, *args: str) -> bytes:
            return subprocess.run(
                ["git", *args], cwd=cwd, capture_output=True,
                timeout=60, check=True,
            ).stdout

        def fixture_live(ref: str) -> str:
            return fixture_git(root, "--git-dir", str(origin), "rev-parse", ref)

        expected_paths = [f"evidence-{number}.txt" for number in range(1, 8)]

        def staged_snapshot() -> dict[str, Any]:
            diff_check = subprocess.run(
                ["git", "diff", "--cached", "--check"], cwd=work,
                capture_output=True, timeout=60,
            ).returncode == 0
            return {
                "head": fixture_git(work, "rev-parse", "HEAD"),
                "branch": fixture_git(work, "branch", "--show-current"),
                "upstream_name": fixture_git(work, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"),
                "upstream_commit": fixture_git(work, "rev-parse", "@{u}"),
                "active_tracking": fixture_git(work, "rev-parse", "refs/remotes/origin/active"),
                "active_live": fixture_live("refs/heads/active"),
                "protected_local": fixture_git(work, "rev-parse", "refs/heads/protected"),
                "protected_tracking": fixture_git(work, "rev-parse", "refs/remotes/origin/protected"),
                "protected_live": fixture_live("refs/heads/protected"),
                "main_tracking": fixture_git(work, "rev-parse", "refs/remotes/origin/main"),
                "main_live": fixture_live("refs/heads/main"),
                "staged": fixture_git(work, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines(),
                "unstaged": fixture_git(work, "diff", "--name-only").splitlines(),
                "status": fixture_git(work, "status", "--porcelain=v1", "--untracked-files=all").splitlines(),
                "diff_check": diff_check,
                "claude_status": fixture_git(work, "status", "--porcelain=v1", "--untracked-files=all", "--", "Claude").splitlines(),
                "index_worktree_equal": {
                    path: fixture_git_bytes(work, "show", f":{path}") == (work / path).read_bytes()
                    for path in expected_paths
                },
            }

        def persisted_snapshot(commit: str) -> dict[str, Any]:
            return {
                "head": fixture_git(work, "rev-parse", "HEAD"),
                "parent": fixture_git(work, "rev-parse", f"{commit}^"),
                "subject": fixture_git(work, "show", "-s", "--format=%s", commit),
                "committed": fixture_git(work, "diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines(),
                "branch": fixture_git(work, "branch", "--show-current"),
                "upstream_name": fixture_git(work, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"),
                "upstream_commit": fixture_git(work, "rev-parse", "@{u}"),
                "active_tracking": fixture_git(work, "rev-parse", "refs/remotes/origin/active"),
                "active_live": fixture_live("refs/heads/active"),
                "protected_tracking": fixture_git(work, "rev-parse", "refs/remotes/origin/protected"),
                "protected_local": fixture_git(work, "rev-parse", "refs/heads/protected"),
                "protected_live": fixture_live("refs/heads/protected"),
                "main_tracking": fixture_git(work, "rev-parse", "refs/remotes/origin/main"),
                "main_live": fixture_live("refs/heads/main"),
                "claude_diff": fixture_git(work, "diff", "--name-only", parent, commit, "--", "Claude").splitlines(),
                "claude_status": fixture_git(work, "status", "--porcelain=v1", "--untracked-files=all", "--", "Claude").splitlines(),
                "status": fixture_git(work, "status", "--porcelain=v1", "--untracked-files=all").splitlines(),
                "blob_worktree_equal": {
                    path: fixture_git_bytes(work, "show", f"{commit}:{path}") == (work / path).read_bytes()
                    for path in expected_paths
                },
            }

        work.mkdir()
        fixture_git(work, "init", "--initial-branch=main")
        fixture_git(work, "config", "user.email", "step62-fixture@example.invalid")
        fixture_git(work, "config", "user.name", "Step 62 Fixture")
        (work / "base.txt").write_bytes(b"base\n")
        (work / "Claude").mkdir()
        (work / "Claude" / "keep.txt").write_bytes(b"protected source\n")
        fixture_git(work, "add", "base.txt", "Claude/keep.txt")
        fixture_git(work, "commit", "-m", "base")
        parent = fixture_git(work, "rev-parse", "HEAD")
        fixture_git(work, "branch", "protected", parent)
        fixture_git(work, "branch", "active", parent)
        fixture_git(work, "switch", "-c", "drift", parent)
        fixture_git(work, "commit", "--allow-empty", "-m", "drift")
        drift = fixture_git(work, "rev-parse", "HEAD")
        fixture_git(work, "switch", "active")
        fixture_git(root, "init", "--bare", str(origin))
        fixture_git(work, "remote", "add", "origin", str(origin))
        fixture_git(work, "push", "origin", "main", "protected")
        fixture_git(work, "push", "-u", "origin", "active")
        fixture_git(work, "push", "origin", f"{drift}:refs/heads/drift-witness")
        fixture_git(work, "branch", "-d", "main")
        for path in expected_paths:
            (work / path).write_bytes(f"{path}\n".encode("utf-8"))
        fixture_git(work, "add", *expected_paths)
        validate_staged_boundary(
            staged_snapshot(), expected_parent=parent, expected_branch="active",
            expected_upstream_name="origin/active", expected_protected=parent,
            expected_main=parent, expected_paths=expected_paths,
        )

        passed = 0

        def expect(name: str, diagnostic: str, action: Callable[[], None]) -> None:
            nonlocal passed
            action()
            try:
                validate_staged_boundary(
                    staged_snapshot(), expected_parent=parent, expected_branch="active",
                    expected_upstream_name="origin/active", expected_protected=parent,
                    expected_main=parent, expected_paths=expected_paths,
                )
            except ValidationError as exc:
                observed = str(exc).split(":", 1)[0]
                require(observed == diagnostic, f"E_GIT_FIXTURE_WRONG_DIAGNOSTIC:{name}:{observed}!={diagnostic}")
                passed += 1
            else:
                raise ValidationError(f"E_GIT_FIXTURE_ESCAPED:{name}")

        extra = work / "extra.txt"
        expect(
            "extra_staged_path", "E_STAGED_PATHS",
            lambda: (extra.write_bytes(b"extra\n"), fixture_git(work, "add", "extra.txt")),
        )
        fixture_git(work, "restore", "--staged", "extra.txt")
        extra.unlink()
        expect(
            "active_remote_drift", "E_STAGED_ACTIVE_REMOTE",
            lambda: fixture_git(root, "--git-dir", str(origin), "update-ref", "refs/heads/active", drift),
        )
        fixture_git(root, "--git-dir", str(origin), "update-ref", "refs/heads/active", parent)
        expect(
            "protected_remote_drift", "E_STAGED_PROTECTED_REMOTE",
            lambda: fixture_git(root, "--git-dir", str(origin), "update-ref", "refs/heads/protected", drift),
        )
        fixture_git(root, "--git-dir", str(origin), "update-ref", "refs/heads/protected", parent)
        expect(
            "main_remote_drift", "E_STAGED_MAIN_REMOTE",
            lambda: fixture_git(root, "--git-dir", str(origin), "update-ref", "refs/heads/main", drift),
        )
        fixture_git(root, "--git-dir", str(origin), "update-ref", "refs/heads/main", parent)
        fixture_git(work, "commit", "-m", "wrong subject")
        wrong_commit = fixture_git(work, "rev-parse", "HEAD")
        try:
            validate_persistence_boundary(
                persisted_snapshot(wrong_commit), expected_commit=wrong_commit,
                expected_parent=parent, expected_subject=SUBJECT, expected_branch="active",
                expected_upstream_name="origin/active", expected_protected=parent,
                expected_main=parent, expected_paths=expected_paths,
            )
        except ValidationError as exc:
            observed = str(exc).split(":", 1)[0]
            require(observed == "E_PERSIST_SUBJECT", f"E_GIT_FIXTURE_WRONG_DIAGNOSTIC:subject:{observed}")
            passed += 1
        else:
            raise ValidationError("E_GIT_FIXTURE_ESCAPED:subject")
        fixture_git(work, "commit", "--amend", "-m", SUBJECT)
        persisted_commit = fixture_git(work, "rev-parse", "HEAD")
        fixture_git(work, "push", "origin", "active")
        validate_persistence_boundary(
            persisted_snapshot(persisted_commit), expected_commit=persisted_commit,
            expected_parent=parent, expected_subject=SUBJECT, expected_branch="active",
            expected_upstream_name="origin/active", expected_protected=parent,
            expected_main=parent, expected_paths=expected_paths,
        )
        return passed, 5


def run_negative_probes(
    data: dict[str, Any], topology: dict[str, Any], provisional: dict[str, Any],
    projection: dict[str, Any],
) -> int:
    probes: list[tuple[str, Callable[[dict[str, Any]], None], str]] = []

    def add(name: str, mutator: Callable[[dict[str, Any]], None], diagnostic: str) -> None:
        probes.append((name, mutator, diagnostic))

    add("schema", lambda d: d.__setitem__("schema", "bad"), "E_SCHEMA")
    add("phase", lambda d: d.__setitem__("step", 61), "E_PHASE_STEP")
    add("baseline", lambda d: d.__setitem__("frozen_baseline", "0" * 40), "E_INPUT_IDENTITY")
    add("gate", lambda d: d.__setitem__("gate", "PASS"), "E_GATE")
    add("occurrence_loss", lambda d: d["competing_occurrences"].pop(), "E_OCCURRENCE_COUNT")
    add("occurrence_authority", lambda d: d["competing_occurrences"][0].__setitem__("final_adoption_authority", True), "E_OCCURRENCE_AUTHORITY")
    add("family_count", lambda d: d["proposal_families"][0].__setitem__("occurrence_count", 999), "E_FAMILY_COUNTS")
    add("family_authority", lambda d: d["proposal_families"][0].__setitem__("authority_ceiling", "ADOPTED"), "E_FAMILY_AUTHORITY")
    add("route_loss", lambda d: d["adoption_routes"].pop(), "E_ROUTE_IDS")
    add("route_finding_fabrication", lambda d: d["adoption_routes"][0]["finding_ids"].append("INTENT-PROV-0101"), "E_ROUTE_FINDING_PROJECTION")
    add("route_role", lambda d: d["adoption_routes"][0]["review_sources"].append("P063-SRC-0112"), "E_ROUTE_TYPED_ROLE")
    add("route_decision_promotion", lambda d: d["adoption_routes"][0].__setitem__("decision_evidence_state", "DIRECT"), "E_ROUTE_GNF_STATE")
    add("v23_adoption", lambda d: next(r for r in d["adoption_routes"] if r["route_id"] == "P063-S62-CHAIN-015")["patch_commits"].append("0" * 40), "E_V23_FALSE_ADOPTION")
    add("finding_loss", lambda d: d["finding_adjudications"].pop(), "E_FINDING_COUNT")
    add("finding_state", lambda d: d["finding_adjudications"][0].__setitem__("state", "OPEN"), "E_FINDING_STATE")
    add("finding_adoption_fabrication", lambda d: d["finding_adjudications"][0]["final_source_edges"].append("P063-SRC-0001"), "E_FINDING_FINAL_EDGE")
    add("finding_external", lambda d: d["finding_adjudications"][0].__setitem__("external_truth", True), "E_FINDING_EXTERNAL_TRUTH")
    add("finding_evidence_state", lambda d: d["finding_adjudications"][0].__setitem__("evidence_state", "GNF"), "E_FINDING_EVIDENCE_STATE")
    add("finding_final_evidence", lambda d: d["finding_adjudications"][0]["state_evidence"].append({"evidence_role": "FROZEN_FINAL_SOURCE_CURRENT_STATE"}), "E_FINDING_FINAL_EVIDENCE")
    add("build_materialization", lambda d: d["build_audit"].__setitem__("materialization", "git archive"), "E_BUILD_MATERIALIZATION")
    add("build_source_mutation", lambda d: d["build_audit"].__setitem__("non_pdf_git_object_identity_after_build", "199/200"), "E_BUILD_SOURCE_MUTATION")
    add("build_exit", lambda d: d["build_audit"]["rows"][0].__setitem__("exit_codes", [0, 1, 0]), "E_BUILD_DIAGNOSTICS")
    add("build_page", lambda d: d["build_audit"]["rows"][1].__setitem__("built_pages", 82), "E_BUILD_PAGE_ROWS")
    add("missing_glyph_erasure", lambda d: d["build_audit"]["rows"][3].__setitem__("missing_glyphs", []), "E_MISSING_GLYPH")
    add("render_diff", lambda d: d["build_audit"]["rows"][1].__setitem__("render_diff_pages", []), "E_RENDER_DIFF_PAGES")
    add("code_policy", lambda d: d["code_mention_boundary"].__setitem__("policy_pass", True), "E_CODE_POLICY_AUTHORITY")
    add("code_actionable", lambda d: d["code_mention_boundary"]["physics_main_body_manual_refinement"].__setitem__("actionable_line_rows", 0), "E_CODE_ACTIONABLE")
    add("state_conflict_loss", lambda d: d["state_chronology"]["conflicts"].pop(), "E_STATE_CONFLICT_COUNT")
    add("state_precedence", lambda d: d["state_chronology"].__setitem__("precedence_rule", "SELF_REPORT_FIRST"), "E_STATE_PRECEDENCE")
    add("authority_promotion", lambda d: d["authority"].__setitem__("external_scientific", True), "E_AUTHORITY_PROMOTION")
    add("unknown_top_key", lambda d: d.__setitem__("invented", True), "E_EXACT_PROJECTION")
    add("route_authority_ceiling", lambda d: d["adoption_routes"][0].__setitem__("authority_ceiling", "EXTERNAL_SCIENTIFIC_TRUTH"), "E_EXACT_PROJECTION")
    add("route_gnf_owner", lambda d: d["adoption_routes"][0]["ground_not_found"].__setitem__("owner", ""), "E_ROUTE_GNF_CONTEXT")
    add("patch_survivor", lambda d: d["adoption_routes"][0]["final_source_edges"][0]["patch_final_survival"][0].__setitem__("survivors", []), "E_ROUTE_PATCH_FINAL_REPLAY")
    add("finding_content_edge_loss", lambda d: next(row for row in d["finding_adjudications"] if row["numeric_id"] == 101).__setitem__("patch_final_current_state_edges", []), "E_FINDING_PATCH_FINAL_EDGE")
    add(
        "proposal_edge_fabrication",
        lambda d: next(
            edge
            for route in d["adoption_routes"]
            for projection_row in route["finding_projections"]
            for edge in projection_row["final_source_edges"]
            if not edge["proposal_to_patch_to_final_content_edge"]
        ).__setitem__("proposal_to_patch_to_final_content_edge", True),
        "E_ROUTE_PROPOSAL_EDGE_BOOL",
    )
    add(
        "proposal_evidence_hash",
        lambda d: next(
            edge
            for route in d["adoption_routes"]
            for projection_row in route["finding_projections"]
            for edge in projection_row["final_source_edges"]
            if edge["proposal_content_evidence"]
        )["proposal_content_evidence"][0].__setitem__("normalized_sha256", "0" * 64),
        "E_ROUTE_PROPOSAL_EVIDENCE",
    )
    add("build_pdf_hash", lambda d: d["build_audit"]["rows"][0].__setitem__("built_pdf_sha256", "0" * 64), "E_EXACT_PROJECTION")
    add("build_engine", lambda d: d["build_audit"]["rows"][0].__setitem__("engine", "invented"), "E_EXACT_PROJECTION")
    add("code_occurrence_hash", lambda d: d["code_mention_boundary"]["occurrence_rows"][0].__setitem__("source_line_sha256", "0" * 64), "E_CODE_OCCURRENCE_REPLAY")
    add("state_current_claim", lambda d: d["state_chronology"]["conflicts"][0].__setitem__("current_state", "FAKE_STATE"), "E_EXACT_PROJECTION")
    add("finding_owner", lambda d: d["finding_adjudications"][0].__setitem__("owner", "generic pass"), "E_EXACT_PROJECTION")
    passed = 0
    for name, mutate, expected in probes:
        fixture = copy.deepcopy(data)
        mutate(fixture)
        try:
            validate_semantics(fixture, topology, provisional, projection)
        except ValidationError as exc:
            observed = str(exc).split(":", 1)[0]
            require(observed == expected, f"E_NEGATIVE_WRONG_DIAGNOSTIC:{name}:{observed}!={expected}")
            passed += 1
        else:
            raise ValidationError(f"E_NEGATIVE_ESCAPED:{name}")
    strict_fixtures = {
        "duplicate": b'{"a":1,"a":2}', "nan": b'{"a":NaN}',
        "infinity": b'{"a":Infinity}', "truncated": b'{"a":',
        "trailing": b'{"a":1} x', "overflow": b'{"a":1e9999}',
    }
    for name, raw in strict_fixtures.items():
        try:
            strict_load_bytes(raw)
        except ValidationError:
            passed += 1
        else:
            raise ValidationError(f"E_STRICT_JSON_ESCAPED:{name}")
    matrix_sha256 = hashlib.sha256((REPO / MATRIX_REL).read_bytes()).hexdigest()
    recovery_docs = {
        "result": (REPO / RESULT_REL).read_text(encoding="utf-8"),
        "active": (REPO / ACTIVE_LEDGER).read_text(encoding="utf-8"),
        "parent": (REPO / PARENT_LEDGER).read_text(encoding="utf-8"),
        "handover": (REPO / HANDOVER).read_text(encoding="utf-8"),
    }
    recovery_fixtures = [
        (
            "result_conflict",
            "result",
            f"Terminal: `{GATE}`",
            f"Terminal: `{GATE}`\n\nOverall status: FAIL_P063",
            "E_RESULT_GATE_SURFACE",
        ),
        (
            "active_conflict",
            "active",
            "| 063 | 58–63 |",
            "| 063 | 58–63 | FAIL_P063 |",
            "E_ACTIVE_LEDGER_CONFLICT",
        ),
        (
            "parent_conflict",
            "parent",
            "| 063 | 58–63 |",
            "| 063 | 58–63 | CONDITIONAL_P063 |",
            "E_PARENT_LEDGER_CONFLICT",
        ),
        (
            "handover_conflict",
            "handover",
            "| Phase 063 Step 62 | Step 62 |",
            "| Phase 063 Step 62 | Step 62 | FAIL_P063 |",
            "E_HANDOVER_CONFLICT",
        ),
    ]
    for name, key, needle, replacement, expected in recovery_fixtures:
        mutated = dict(recovery_docs)
        require(mutated[key].count(needle) == 1, f"E_RECOVERY_FIXTURE_TARGET:{name}")
        mutated[key] = mutated[key].replace(needle, replacement, 1)
        try:
            validate_recovery_texts(
                mutated["result"], mutated["active"], mutated["parent"],
                mutated["handover"], matrix_sha256,
            )
        except ValidationError as exc:
            observed = str(exc).split(":", 1)[0]
            require(observed == expected, f"E_RECOVERY_WRONG_DIAGNOSTIC:{name}:{observed}!={expected}")
            passed += 1
        else:
            raise ValidationError(f"E_RECOVERY_ESCAPED:{name}")

    builder_raw = (REPO / BUILDER_REL).read_bytes()
    builder_text = builder_raw.decode("utf-8")
    builder_fixtures = [
        ("raw_pin", builder_raw + b"\n# mutation\n", True, True, "E_BUILDER_RAW_SHA256"),
        (
            "ast_pin",
            builder_text.replace("timeout=60", "timeout=61", 1).encode("utf-8"),
            False, True, "E_BUILDER_AST_SHA256",
        ),
        (
            "subprocess_count",
            builder_text.replace("    proc = subprocess.run(", "    subprocess.run(['git', '--version'])\n    proc = subprocess.run(", 1).encode("utf-8"),
            False, False, "E_BUILDER_SUBPROCESS_POLICY",
        ),
        (
            "subprocess_argv",
            builder_text.replace('["git", *args]', '["cmd", *args]', 1).encode("utf-8"),
            False, False, "E_BUILDER_SUBPROCESS_ARGV",
        ),
    ]
    for name, raw, enforce_raw, enforce_ast, expected in builder_fixtures:
        try:
            validate_builder_source_policy(raw, enforce_raw_pin=enforce_raw, enforce_ast_pin=enforce_ast)
        except ValidationError as exc:
            observed = str(exc).split(":", 1)[0]
            require(observed == expected, f"E_BUILDER_POLICY_WRONG_DIAGNOSTIC:{name}:{observed}!={expected}")
            passed += 1
        else:
            raise ValidationError(f"E_BUILDER_POLICY_ESCAPED:{name}")
    git_boundary_passed, git_boundary_total = git_boundary_negative_fixture()
    passed += git_boundary_passed
    total = len(probes) + len(strict_fixtures) + len(recovery_fixtures) + len(builder_fixtures) + git_boundary_total
    print(
        f"PASS_P063_STEP62_NEGATIVE {passed}/{total} "
        f"strict_json={len(strict_fixtures)}/{len(strict_fixtures)} "
        f"recovery={len(recovery_fixtures)}/{len(recovery_fixtures)} "
        f"builder_policy={len(builder_fixtures)}/{len(builder_fixtures)} "
        f"git_boundary={git_boundary_passed}/{git_boundary_total} singleton=PASS"
    )
    return passed


def determinism_check() -> None:
    with tempfile.TemporaryDirectory(prefix="p063-step62-determinism-") as tmp:
        root = pathlib.Path(tmp)
        outputs: list[tuple[bytes, bytes]] = []
        for run in (1, 2):
            matrix = root / f"matrix-{run}.json"
            result = root / f"result-{run}.md"
            subprocess.run(
                [sys.executable, "-B", str(REPO / BUILDER_REL), "--matrix", str(matrix), "--result", str(result)],
                cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="strict",
                timeout=180, check=True,
            )
            outputs.append((matrix.read_bytes(), result.read_bytes()))
        require(outputs[0] == outputs[1], "E_DETERMINISM_2X")
        require(outputs[0][0] == (REPO / MATRIX_REL).read_bytes() and outputs[0][1] == (REPO / RESULT_REL).read_bytes(), "E_DETERMINISM_STORED")
    print("PASS_P063_STEP62_DETERMINISM 2/2")


def validate_staged_boundary(
    snapshot: dict[str, Any], *, expected_parent: str, expected_branch: str,
    expected_upstream_name: str, expected_protected: str, expected_main: str,
    expected_paths: list[str],
) -> None:
    require(snapshot["head"] == expected_parent, "E_STAGED_PARENT")
    require(snapshot["branch"] == expected_branch, "E_STAGED_BRANCH")
    require(snapshot["upstream_name"] == expected_upstream_name, "E_STAGED_UPSTREAM_NAME")
    require(snapshot["upstream_commit"] == expected_parent, "E_STAGED_UPSTREAM_COMMIT")
    require(snapshot["active_tracking"] == expected_parent and snapshot["active_live"] == expected_parent, "E_STAGED_ACTIVE_REMOTE")
    require(snapshot["protected_local"] == expected_protected, "E_STAGED_PROTECTED_LOCAL")
    require(snapshot["protected_tracking"] == expected_protected and snapshot["protected_live"] == expected_protected, "E_STAGED_PROTECTED_REMOTE")
    require(snapshot["main_tracking"] == expected_main and snapshot["main_live"] == expected_main, "E_STAGED_MAIN_REMOTE")
    require(snapshot["staged"] == sorted(expected_paths), f"E_STAGED_PATHS:{snapshot['staged']}")
    require(snapshot["unstaged"] == [], "E_UNSTAGED_CHANGES")
    status = snapshot["status"]
    require(len(status) == len(expected_paths) and all(line[:2] in {"A ", "M "} for line in status), f"E_STAGED_STATUS:{status}")
    require(snapshot["diff_check"], "E_STAGED_DIFF_CHECK")
    require(not any(path.startswith("Claude/") for path in snapshot["staged"]), "E_STAGED_CLAUDE")
    require(snapshot["claude_status"] == [], "E_STAGED_CLAUDE_STATUS")
    require(snapshot["index_worktree_equal"] == {path: True for path in expected_paths}, "E_STAGED_INDEX_WORKTREE")


def production_index_worktree_equal(path: str) -> bool:
    try:
        indexed = run_git("show", f":{path}", text=False)
    except subprocess.CalledProcessError:
        return False
    return indexed == (REPO / path).read_bytes()


def production_staged_snapshot() -> dict[str, Any]:
    staged = str(run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines()
    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--check"], cwd=REPO,
        capture_output=True, timeout=60,
    ).returncode == 0
    return {
        "head": str(run_git("rev-parse", "HEAD")).strip(),
        "branch": str(run_git("branch", "--show-current")).strip(),
        "upstream_name": str(run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")).strip(),
        "upstream_commit": str(run_git("rev-parse", "@{u}")).strip(),
        "active_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{BRANCH}")).strip(),
        "active_live": live_ref(f"refs/heads/{BRANCH}"),
        "protected_local": str(run_git("rev-parse", f"refs/heads/{PROTECTED_BRANCH}")).strip(),
        "protected_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}")).strip(),
        "protected_live": live_ref(f"refs/heads/{PROTECTED_BRANCH}"),
        "main_tracking": str(run_git("rev-parse", "refs/remotes/origin/main")).strip(),
        "main_live": live_ref("refs/heads/main"),
        "staged": staged,
        "unstaged": str(run_git("diff", "--name-only")).splitlines(),
        "status": str(run_git("status", "--porcelain=v1", "--untracked-files=all")).splitlines(),
        "diff_check": diff_check,
        "claude_status": str(run_git("status", "--porcelain=v1", "--untracked-files=all", "--", "Claude")).splitlines(),
        "index_worktree_equal": {
            path: production_index_worktree_equal(path)
            for path in EXACT_PATHS
        },
    }


def verify_staged() -> None:
    validate_staged_boundary(
        production_staged_snapshot(), expected_parent=PARENT, expected_branch=BRANCH,
        expected_upstream_name=f"origin/{BRANCH}", expected_protected=PROTECTED_TIP,
        expected_main=MAIN_TIP, expected_paths=EXACT_PATHS,
    )
    print("PASS_P063_STEP62_STAGED exact-seven")


def live_ref(ref: str) -> str:
    output = str(run_git("ls-remote", "origin", ref)).strip()
    require(bool(output), f"E_LIVE_REF_MISSING:{ref}")
    return output.split()[0]


def validate_persistence_boundary(
    snapshot: dict[str, Any], *, expected_commit: str, expected_parent: str,
    expected_subject: str, expected_branch: str, expected_upstream_name: str,
    expected_protected: str, expected_main: str, expected_paths: list[str],
) -> None:
    require(len(expected_commit) == 40, "E_EXPECTED_COMMIT_FORMAT")
    require(snapshot["head"] == expected_commit, "E_PERSIST_HEAD")
    require(snapshot["parent"] == expected_parent, "E_PERSIST_PARENT")
    require(snapshot["subject"] == expected_subject, "E_PERSIST_SUBJECT")
    require(snapshot["committed"] == sorted(expected_paths), f"E_PERSIST_PATHS:{snapshot['committed']}")
    require(snapshot["branch"] == expected_branch, "E_PERSIST_BRANCH")
    require(snapshot["upstream_name"] == expected_upstream_name, "E_PERSIST_UPSTREAM_NAME")
    require(snapshot["upstream_commit"] == expected_commit, "E_PERSIST_UPSTREAM")
    require(snapshot["active_tracking"] == expected_commit, "E_PERSIST_TRACKING")
    require(snapshot["active_live"] == expected_commit, "E_PERSIST_LIVE")
    require(snapshot["protected_tracking"] == expected_protected, "E_PROTECTED_TRACKING")
    require(snapshot["protected_local"] == expected_protected, "E_PROTECTED_LOCAL")
    require(snapshot["protected_live"] == expected_protected, "E_PROTECTED_LIVE")
    require(snapshot["main_tracking"] == expected_main, "E_MAIN_TRACKING")
    require(snapshot["main_live"] == expected_main, "E_MAIN_LIVE")
    require(snapshot["claude_diff"] == [], "E_PERSIST_CLAUDE")
    require(snapshot["claude_status"] == [], "E_PERSIST_CLAUDE_STATUS")
    require(snapshot["status"] == [], "E_PERSIST_DIRTY")
    require(snapshot["blob_worktree_equal"] == {path: True for path in expected_paths}, "E_PERSIST_BLOB")


def production_commit_worktree_equal(commit: str, path: str) -> bool:
    try:
        committed = git_bytes(commit, path)
    except subprocess.CalledProcessError:
        return False
    return committed == (REPO / path).read_bytes()


def production_persistence_snapshot(expected_commit: str) -> dict[str, Any]:
    return {
        "head": str(run_git("rev-parse", "HEAD")).strip(),
        "parent": str(run_git("rev-parse", f"{expected_commit}^")).strip(),
        "subject": str(run_git("show", "-s", "--format=%s", expected_commit)).rstrip("\r\n"),
        "committed": str(run_git("diff-tree", "--no-commit-id", "--name-only", "-r", expected_commit)).splitlines(),
        "branch": str(run_git("branch", "--show-current")).strip(),
        "upstream_name": str(run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")).strip(),
        "upstream_commit": str(run_git("rev-parse", "@{u}")).strip(),
        "active_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{BRANCH}")).strip(),
        "active_live": live_ref(f"refs/heads/{BRANCH}"),
        "protected_tracking": str(run_git("rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}")).strip(),
        "protected_local": str(run_git("rev-parse", f"refs/heads/{PROTECTED_BRANCH}")).strip(),
        "protected_live": live_ref(f"refs/heads/{PROTECTED_BRANCH}"),
        "main_tracking": str(run_git("rev-parse", "refs/remotes/origin/main")).strip(),
        "main_live": live_ref("refs/heads/main"),
        "claude_diff": str(run_git("diff", "--name-only", PARENT, expected_commit, "--", "Claude")).splitlines(),
        "claude_status": str(run_git("status", "--porcelain=v1", "--untracked-files=all", "--", "Claude")).splitlines(),
        "status": str(run_git("status", "--porcelain=v1", "--untracked-files=all")).splitlines(),
        "blob_worktree_equal": {
            path: production_commit_worktree_equal(expected_commit, path)
            for path in EXACT_PATHS
        },
    }


def verify_persistence(expected_commit: str) -> None:
    validate_persistence_boundary(
        production_persistence_snapshot(expected_commit), expected_commit=expected_commit,
        expected_parent=PARENT, expected_subject=SUBJECT, expected_branch=BRANCH,
        expected_upstream_name=f"origin/{BRANCH}", expected_protected=PROTECTED_TIP,
        expected_main=MAIN_TIP, expected_paths=EXACT_PATHS,
    )
    print(PERSISTENCE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-build-replay", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    try:
        require((REPO / MATRIX_REL).is_file(), f"E_MATRIX_ARTIFACT_MISSING:{MATRIX_REL}")
        require((REPO / RESULT_REL).is_file(), f"E_RESULT_ARTIFACT_MISSING:{RESULT_REL}")
        data = strict_load(REPO / MATRIX_REL)
        topology = strict_load(REPO / TOPOLOGY_REL)
        provisional = strict_load(REPO / PROVISIONAL_REL)
        require(not (args.verify_staged and args.verify_persistence), "E_MODE_CONFLICT")
        validate_builder_source_policy()
        projection = expected_projection()
        traversal_count(topology)
        traversal_count(provisional)
        validate_semantics(data, topology, provisional, projection)
        validate_git_evidence(data, topology)
        validate_result()
        nodes = traversal_count(data)
        strong_mode = args.verify_staged or args.verify_persistence
        if args.verify_build_replay or strong_mode:
            verify_build_replay(data)
        if args.run_negative_probes or strong_mode:
            run_negative_probes(data, topology, provisional, projection)
        if args.determinism_check or strong_mode:
            determinism_check()
        if args.verify_staged:
            verify_staged()
        elif args.verify_persistence:
            require(bool(args.expected_commit), "E_EXPECTED_COMMIT_REQUIRED")
            verify_persistence(str(args.expected_commit))
        else:
            print(f"{GATE} strict_traversal={nodes}")
        return 0
    except (KeyError, OSError, subprocess.CalledProcessError, ValidationError) as exc:
        print(f"FAIL_P063_STEP62: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
