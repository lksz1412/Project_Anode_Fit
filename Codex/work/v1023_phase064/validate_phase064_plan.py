from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import io
import json
import math
import os
import pathlib
import re
import shutil
import stat
import subprocess
import tempfile
from collections import Counter
from typing import Any, Callable

from PIL import Image
from pypdf import PdfReader


ROOT = pathlib.Path(__file__).resolve().parents[3]
PLAN_PATH = "Codex/plans/2026-08-29-phase064-v1023-lineage-detailed-plan.md"
VALIDATOR_PATH = "Codex/work/v1023_phase064/validate_phase064_plan.py"
OUTPUT_PATH = "Codex/results/PHASE_064_PLAN_ACTIVATION_VALIDATION.json"
RESULT_PATH = "Codex/results/PHASE_064_PLAN_ACTIVATION_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"

PLAN = ROOT / PLAN_PATH
VALIDATOR = ROOT / VALIDATOR_PATH
OUTPUT = ROOT / OUTPUT_PATH

EXPECTED_PARENT = "696e6300a63ba47d773ca211362818987790a63f"
EXPECTED_PARENT_PARENT = "6c46cf81bf88394dc23e0b86943297cca1affa89"
EXPECTED_PARENT_SUBJECT = "audit(phase063): close v1022 lineage gate"
EXPECTED_SUBJECT = "docs(phase064): plan v1023 lineage reaudit"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
GATE = "PASS_P064_PLAN_ACTIVATION"
PERSISTENCE = "PASS_P064_PLAN_ACTIVATION_PERSISTENCE"
PLAN_SHA256_LF = "c553993aba0fd653473e4da2b93e219bd45a520a8400716a6e732d2f68bd8f2b"
MANIFEST_SHA256_LF = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
PATH_SET_SHA256 = "7b37fe84d8cbceebafb8801e5489545ace1a7052ed33668ec2ec2200abb422b5"
VALIDATOR_SOURCE_SHA256_LF = "d0abe31e6046fc3d4b1eeab06154a30bdd5e81b9621af577a81b7ff4066f6a98"
VALIDATOR_AST_SHA256 = "b48d694629f0ac81aecfc280b65e87696b8249a970e1b452c2b1dc2ddbc62657"
RUN_PROCESS_SOURCE_SHA256_LF = "a24440c290fe52b6cb9190478c894ef34cacbcb20e647ab3cd41eb30f9ddb8c1"
GIT_SOURCE_SHA256_LF = "be3ad83b1e079727235638fe327a5f9ee03860179828bdf46939bb90d67af945"
GIT_OWNER_SOURCE_SHA256_LF = "85317826c4b008421695c1995015d3b86ca8d6e22936e285426a3bc3f86a0927"

CONTROL_SHA256_LF = {
    RESULT_PATH: "fac2cf0449ba7f1e4a1331faf83abb6fba95788c2c99e1a986fc47e86f2cc87d",
    PARENT_LEDGER_PATH: "ca4ac58c6e9cfc386f74b45e2f51f198e9f4d0ed744c70cae236a4e8f3364e19",
    ACTIVE_LEDGER_PATH: "514a8e91526e23fafac6938afd2d57ee1fe3686d48d88f2198a596e3a5291bfa",
    HANDOVER_PATH: "c8b2ecd1a44cd5b74dcb7d6c7fff8f7c455a3da8e18574eb7e679d45c29894d6",
}

FINAL_PATHS = [
    PLAN_PATH,
    VALIDATOR_PATH,
    OUTPUT_PATH,
    RESULT_PATH,
    PARENT_LEDGER_PATH,
    ACTIVE_LEDGER_PATH,
    HANDOVER_PATH,
]
FINAL_PATH_SET = set(FINAL_PATHS)
NONSELF_PATHS = [path for path in FINAL_PATHS if path != OUTPUT_PATH]

SUPPLEMENTAL = {
    "plan": {
        "path": "Claude/plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md",
        "blob": "ce4b17399f8d7318b4053134959ab77f9038d313",
        "bytes": 20203,
        "lines": 225,
        "sha256": "4c3aedabac00ac657f12bf2dffe6f696017654b883f2798c2d824ee70665b228",
    },
    "jcp147": {
        "path": "Claude/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf",
        "blob": "4fbe2b91b2b3f62cea76feb4272b1e3275dab986",
        "bytes": 2075558,
        "pages": 10,
        "sha256": "47c7c415093bf5e3ee78215d6efa9141e4cd574e74e206cd9e3e863c5da85bd9",
    },
    "extract": {
        "path": "Claude/jcp_extract.txt",
        "blob": "2588ac5da0e9ce4c25141f302a1e33e460ff7966",
        "bytes": 68800,
        "lines": 725,
        "sha256": "200cf715da949fd737dad3e7fb2041e63327cf52a8495748da8a564438d963fb",
    },
}

PROCESS_COMMITS = [
    "9cb1ad900b6b170976fa41f31dd5a2ca8330b2d6",
    "63972cfc0af6ba232a361c3d96fcedc656f647d0",
    "d47d4dbb79fdaba284f15faca62ee9d6a280c3d8",
    "ee0371f74524460e908bb548d10e9592e1807fe9",
    "a722313ac19ece6bb72c87b7cd99e498fca25876",
    "3aa791aeb7357f23dbfb1d232277fd84276ca16b",
    "802673049bc54f0f11282af1334970042584229d",
    "ff840987a99348c092d3ab535c934ac7f303c5b1",
    "b6e51105341696ad97a5d5d6ec0c414c8bd0c62d",
    "4b781d31d31771ee6275805be8931c2a510df010",
    "4d56dc9f78a9aaf5d00e3479298371fde91a170e",
    "ce1e5e7e0b1407f6f5fd366bd30f3c9c8fa41bde",
    "ae6c967830d866e8b45e6087ba128b50790f2840",
    "1ad0e2c70ff213e2fc89ff77d50e74da25080d06",
]


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(code, detail)


def run_process(
    args: list[str], *, cwd: pathlib.Path = ROOT, input_bytes: bytes | None = None,
    timeout: int = 300, check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    process = subprocess.run(
        args, cwd=cwd, input=input_bytes, capture_output=True, timeout=timeout, check=False,
    )
    if check and process.returncode != 0:
        raise ValidationError(
            "E_SUBPROCESS",
            f"{args!r}: {process.stderr.decode('utf-8', errors='replace')[-1200:]}",
        )
    return process


def git(args: list[str], *, cwd: pathlib.Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run_process(["git", *args], cwd=cwd, check=check)


def git_text(args: list[str], *, cwd: pathlib.Path = ROOT) -> str:
    return git(args, cwd=cwd).stdout.decode("utf-8").strip()


def git_blob(commit: str, path: str, *, cwd: pathlib.Path = ROOT) -> bytes:
    return git(["show", f"{commit}:{path}"], cwd=cwd).stdout


def live_tip(branch: str, *, cwd: pathlib.Path = ROOT) -> str:
    lines = git_text(["ls-remote", "origin", f"refs/heads/{branch}"], cwd=cwd).splitlines()
    require(len(lines) == 1, "E_LIVE_REF", branch)
    return lines[0].split("\t", 1)[0]


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def neutralized_validator_source(raw: bytes) -> bytes:
    normalized = lf_bytes(raw)
    pattern = rb'(?m)^VALIDATOR_SOURCE_SHA256_LF = "[0-9a-f]{64}"$'
    replacement = b'VALIDATOR_SOURCE_SHA256_LF = "' + (b"0" * 64) + b'"'
    neutralized, count = re.subn(pattern, replacement, normalized)
    require(count == 1, "E_SOURCE_HASH_FIELD", str(count))
    return neutralized


def validator_ast_hash(raw: bytes) -> str:
    text = lf_bytes(raw).decode("utf-8")
    for name in ("VALIDATOR_SOURCE_SHA256_LF", "VALIDATOR_AST_SHA256"):
        pattern = rf'(?m)^{name} = "[0-9a-f]{{64}}"$'
        text, count = re.subn(pattern, f'{name} = "' + ("0" * 64) + '"', text)
        require(count == 1, "E_SOURCE_AST_HASH_FIELD", name)
    tree = ast.parse(text, filename=VALIDATOR_PATH)
    return sha256(ast.unparse(tree).encode("utf-8"))


def source_policy_diagnostics(raw: bytes) -> set[str]:
    failures: set[str] = set()
    try:
        tree = ast.parse(lf_bytes(raw).decode("utf-8"), filename=VALIDATOR_PATH)
    except (SyntaxError, UnicodeError):
        return {"E_SOURCE_PARSE"}
    allowed_roots = {
        "__future__", "argparse", "ast", "copy", "hashlib", "io", "json", "math", "os",
        "pathlib", "re", "shutil", "stat", "subprocess", "tempfile", "collections", "typing",
        "PIL", "pypdf",
    }
    allowed_from = {
        "__future__": {"annotations"},
        "collections": {"Counter"},
        "typing": {"Any", "Callable"},
        "PIL": {"Image"},
        "pypdf": {"PdfReader"},
    }
    forbidden_names = {
        "exec", "eval", "compile", "__import__", "open", "getattr", "setattr", "globals",
        "locals", "vars", "input", "breakpoint", "__builtins__",
    }
    forbidden_attributes = {
        "system", "popen", "import_module", "exec_module", "load_module", "spawnl", "spawnle",
        "spawnlp", "spawnlpe", "spawnv", "spawnve", "spawnvp", "spawnvpe", "startfile",
        "execl", "execle", "execlp", "execlpe", "execv", "execve", "execvp", "execvpe",
        "posix_spawn", "posix_spawnp", "fork", "forkpty",
    }
    lines = lf_bytes(raw).splitlines(keepends=True)
    top_functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    top_function_counts = Counter(node.name for node in top_functions)
    if any(count != 1 for count in top_function_counts.values()):
        failures.add("E_SOURCE_DUPLICATE_FUNCTION")
    run_process_nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "run_process"]
    git_nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "git"]
    if (len(run_process_nodes) != 1
            or sha256(b"".join(lines[run_process_nodes[0].lineno - 1:run_process_nodes[0].end_lineno]))
            != RUN_PROCESS_SOURCE_SHA256_LF):
        failures.add("E_SOURCE_RUN_PROCESS_DEFINITION")
    if (len(git_nodes) != 1
            or sha256(b"".join(lines[git_nodes[0].lineno - 1:git_nodes[0].end_lineno]))
            != GIT_SOURCE_SHA256_LF):
        failures.add("E_SOURCE_GIT_DEFINITION")
    pinned_run_process = run_process_nodes[0] if len(run_process_nodes) == 1 else None
    pinned_git = git_nodes[0] if len(git_nodes) == 1 else None
    git_owner_names = (
        "git_text", "git_blob", "live_tip", "status_paths", "repository_snapshot", "manifest_contract",
        "supplemental_contract", "process_contract", "build_payload", "make_git_fixture", "fixture_snapshot",
        "persistence_record", "run_persistence_git_controls", "run_git_controls", "validate_staged",
    )
    git_owner_nodes = {name: [node for node in top_functions if node.name == name] for name in git_owner_names}
    if any(len(nodes) != 1 for nodes in git_owner_nodes.values()):
        failures.add("E_SOURCE_GIT_OWNER_DEFINITION")
    else:
        owner_projection = b"\0".join(
            name.encode("utf-8") + b"\0" + b"".join(lines[nodes[0].lineno - 1:nodes[0].end_lineno])
            for name, nodes in git_owner_nodes.items()
        )
        if sha256(owner_projection) != GIT_OWNER_SOURCE_SHA256_LF:
            failures.add("E_SOURCE_GIT_OWNER_DEFINITION")

    class PolicyVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.functions: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.functions.append(node)
            self.generic_visit(node)
            self.functions.pop()

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            failures.add("E_SOURCE_ASYNC")
            self.functions.append(node)
            self.generic_visit(node)
            self.functions.pop()

        def visit_Import(self, node: ast.Import) -> None:
            if any(alias.asname is not None or alias.name.split(".", 1)[0] not in allowed_roots for alias in node.names):
                failures.add("E_SOURCE_IMPORT")

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            root = (node.module or "").split(".", 1)[0]
            names = {alias.name for alias in node.names}
            if (node.level != 0 or root not in allowed_from or names != allowed_from[root]
                    or any(alias.asname is not None for alias in node.names)):
                failures.add("E_SOURCE_IMPORT")

        def visit_Attribute(self, node: ast.Attribute) -> None:
            if (node.attr.startswith("__") and node.attr.endswith("__")
                    and node.attr not in {"__init__", "__name__", "__setitem__"}):
                failures.add("E_SOURCE_DYNAMIC_EXEC")
            self.generic_visit(node)

        def visit_Name(self, node: ast.Name) -> None:
            current = self.functions[-1] if self.functions else None
            parent = parents.get(node)
            if node.id in forbidden_names:
                failures.add("E_SOURCE_DYNAMIC_EXEC")
            if node.id == "subprocess" and isinstance(node.ctx, ast.Load):
                allowed_reference = False
                if isinstance(parent, ast.Attribute) and parent.value is node:
                    grandparent = parents.get(parent)
                    if parent.attr in {"CompletedProcess", "TimeoutExpired"} and not isinstance(grandparent, ast.Call):
                        allowed_reference = True
                    elif (parent.attr == "run" and current is pinned_run_process
                          and isinstance(grandparent, ast.Call) and grandparent.func is parent):
                        allowed_reference = True
                if not allowed_reference:
                    failures.add("E_SOURCE_SUBPROCESS")
            if node.id == "run_process" and isinstance(node.ctx, ast.Load):
                direct_git_call = isinstance(parent, ast.Call) and parent.func is node and current is pinned_git
                if not direct_git_call:
                    failures.add("E_SOURCE_RUN_PROCESS")
            if node.id == "os" and isinstance(node.ctx, ast.Load):
                direct_allowed_os_call = (
                    isinstance(parent, ast.Attribute) and parent.value is node
                    and parent.attr in {"chmod", "replace"}
                    and isinstance(parents.get(parent), ast.Call) and parents[parent].func is parent
                )
                if not direct_allowed_os_call:
                    failures.add("E_SOURCE_DYNAMIC_EXEC")
            if node.id == "git" and isinstance(node.ctx, ast.Load):
                direct_call = isinstance(parent, ast.Call) and parent.func is node
                allowed_git_nodes = {nodes[0] for nodes in git_owner_nodes.values() if len(nodes) == 1}
                if not direct_call or current not in allowed_git_nodes:
                    failures.add("E_SOURCE_GIT_CALL")
            if node.id in {"git_text", "git_blob"} and isinstance(node.ctx, ast.Load):
                allowed_names = {
                    "git_text": {
                        "live_tip", "repository_snapshot", "manifest_contract", "supplemental_contract",
                        "process_contract", "build_payload", "make_git_fixture", "fixture_snapshot",
                        "persistence_record", "run_persistence_git_controls", "validate_staged",
                    },
                    "git_blob": {"manifest_contract", "supplemental_contract", "persistence_record"},
                }[node.id]
                allowed_nodes = {
                    git_owner_nodes[name][0] for name in allowed_names if len(git_owner_nodes[name]) == 1
                }
                direct_call = isinstance(parent, ast.Call) and parent.func is node
                if not direct_call or current not in allowed_nodes:
                    failures.add("E_SOURCE_GIT_WRAPPER")

        def visit_Call(self, node: ast.Call) -> None:
            current = self.functions[-1] if self.functions else "<module>"
            if isinstance(node.func, ast.Name) and node.func.id in forbidden_names:
                failures.add("E_SOURCE_DYNAMIC_EXEC")
            if isinstance(node.func, ast.Attribute) and node.func.attr in forbidden_attributes:
                failures.add("E_SOURCE_DYNAMIC_EXEC")
            if (isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "subprocess"):
                if node.func.attr != "run" or current is not pinned_run_process:
                    failures.add("E_SOURCE_SUBPROCESS")
            if isinstance(node.func, ast.Name) and node.func.id == "run_process":
                valid_git_wrapper = (
                    current is pinned_git and len(node.args) >= 1 and isinstance(node.args[0], ast.List)
                    and len(node.args[0].elts) >= 1 and isinstance(node.args[0].elts[0], ast.Constant)
                    and node.args[0].elts[0].value == "git"
                )
                if not valid_git_wrapper:
                    failures.add("E_SOURCE_RUN_PROCESS")
            self.generic_visit(node)

    parents = {
        child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)
    }
    PolicyVisitor().visit(tree)
    return failures


def validator_source_contract() -> dict[str, Any]:
    raw = VALIDATOR.read_bytes()
    observed_self_hash = sha256(neutralized_validator_source(raw))
    require(observed_self_hash == VALIDATOR_SOURCE_SHA256_LF, "E_SOURCE_SELF_HASH", observed_self_hash)
    observed_ast_hash = validator_ast_hash(raw)
    require(observed_ast_hash == VALIDATOR_AST_SHA256, "E_SOURCE_AST_HASH", observed_ast_hash)
    diagnostics = source_policy_diagnostics(raw)
    require(not diagnostics, "E_SOURCE_POLICY", repr(sorted(diagnostics)))
    return {
        "path": VALIDATOR_PATH,
        "sha256_lf": sha256(lf_bytes(raw)),
        "neutralized_sha256_lf": observed_self_hash,
        "normalized_ast_sha256": observed_ast_hash,
        "ast_policy": "PASS",
        "subprocess_execution": "GIT_WRAPPER_ONLY",
        "production_python_import_or_execution": False,
    }


def run_source_policy_controls(raw: bytes) -> tuple[int, int]:
    cases = [
        ({"E_SOURCE_IMPORT"}, raw + b"\nimport runpy\n"),
        ({"E_SOURCE_DYNAMIC_EXEC"}, raw + b'\nif False:\n    exec(open("Claude/forbidden.py").read())\n'),
        ({"E_SOURCE_SUBPROCESS"}, raw + b'\ndef forbidden_subprocess():\n    subprocess.run(["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_RUN_PROCESS"}, raw + b'\ndef forbidden_wrapper():\n    run_process(["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_IMPORT"}, raw + b'\nfrom subprocess import run\nrun(["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_SUBPROCESS"}, raw + b'\ndef forbidden_popen():\n    subprocess.Popen(["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_SUBPROCESS"}, raw + b'\nrunner_module = subprocess\nrunner_module.Popen(["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_SUBPROCESS"}, raw + b'\nrunner = subprocess.run\nrunner(["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_SUBPROCESS"}, raw + b'\ndef forbidden_default(runner=subprocess.run):\n    runner(["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_DYNAMIC_EXEC", "E_SOURCE_SUBPROCESS"},
         raw + b'\nsubprocess.__dict__["run"](["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_DYNAMIC_EXEC"}, raw + b'\n__builtins__["exec"]("pass")\n'),
        ({"E_SOURCE_RUN_PROCESS"}, raw + b'\nrunner = run_process\nrunner(["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_DUPLICATE_FUNCTION", "E_SOURCE_RUN_PROCESS_DEFINITION", "E_SOURCE_SUBPROCESS"},
         raw + b'\ndef run_process(args, **kwargs):\n    return subprocess.run(["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_RUN_PROCESS_DEFINITION"}, raw.replace(
            b"capture_output=True, timeout=timeout, check=False,",
            b"capture_output=True, timeout=timeout, check=False, shell=True,", 1)),
        ({"E_SOURCE_RUN_PROCESS_DEFINITION"}, raw.replace(
            b"capture_output=True, timeout=timeout, check=False,",
            b'capture_output=True, timeout=timeout, check=False, executable="python",', 1)),
        ({"E_SOURCE_GIT_CALL"}, raw + b'\ngit(["-c", "alias.x=!python Claude/forbidden.py", "x"])\n'),
        ({"E_SOURCE_GIT_CALL"}, raw + b'\ngit(["clean", "-fdx"])\n'),
        ({"E_SOURCE_DYNAMIC_EXEC"}, raw + b'\nos.startfile("Claude/forbidden.py")\n'),
        ({"E_SOURCE_DYNAMIC_EXEC"}, raw + b'\nos.execv("python", ["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_DUPLICATE_FUNCTION", "E_SOURCE_GIT_CALL", "E_SOURCE_GIT_OWNER_DEFINITION"},
         raw + b'\ndef git_text(args, **kwargs):\n    return git(["clean", "-fdx"])\n'),
        ({"E_SOURCE_DUPLICATE_FUNCTION", "E_SOURCE_GIT_CALL", "E_SOURCE_GIT_OWNER_DEFINITION", "E_SOURCE_GIT_WRAPPER"},
         raw + b'\ndef make_git_fixture():\n    return git(["-c", "alias.x=!python Claude/forbidden.py", "x"])\n'),
        ({"E_SOURCE_DYNAMIC_EXEC"}, raw + b'\nos.execl("python", "python", "Claude/forbidden.py")\n'),
        ({"E_SOURCE_DYNAMIC_EXEC"}, raw + b'\nos.execle("python", "python", "Claude/forbidden.py", {})\n'),
        ({"E_SOURCE_GIT_CALL"}, raw + b'\ndef outer():\n    def git_text():\n        return git(["clean", "-fdx"])\n'),
        ({"E_SOURCE_GIT_CALL"}, raw + b'\nclass SpoofGit:\n    def git_text(self):\n        return git(["clean", "-fdx"])\n'),
        ({"E_SOURCE_SUBPROCESS"}, raw + b'\nclass SpoofProcess:\n    def run_process(self):\n        return subprocess.run(["python", "Claude/forbidden.py"])\n'),
        ({"E_SOURCE_DYNAMIC_EXEC"}, raw + b'\nos.__dict__["system"]("python Claude/forbidden.py")\n'),
        ({"E_SOURCE_DYNAMIC_EXEC"}, raw + b'\nos.__getattribute__("system")("python Claude/forbidden.py")\n'),
        ({"E_SOURCE_DYNAMIC_EXEC"}, raw + b'\nos.__dict__["popen"]("python Claude/forbidden.py")\n'),
        ({"E_SOURCE_GIT_WRAPPER"}, raw + b'\ngit_text(["-c", "alias.x=!python Claude/forbidden.py", "x"])\n'),
        ({"E_SOURCE_GIT_WRAPPER"}, raw + b'\ngt = git_text\ngt(["-c", "alias.x=!python Claude/forbidden.py", "x"])\n'),
        ({"E_SOURCE_GIT_WRAPPER"}, raw + b'\ndef forbidden_default(gt=git_text):\n    return gt(["-c", "alias.x=!python Claude/forbidden.py", "x"])\n'),
        ({"E_SOURCE_GIT_WRAPPER"}, raw + b'\ngb = git_blob\n'),
        ({"E_SOURCE_DYNAMIC_EXEC"}, raw + b'\nif False:\n    [x for x in object.__subclasses__() if x.__name__ == "Popen"][0](["python", "Claude/forbidden.py"])\n'),
    ]
    passed = 0
    for wanted, candidate in cases:
        observed = source_policy_diagnostics(candidate)
        require(observed == wanted, "E_SOURCE_POLICY_DIAGNOSTIC", f"{sorted(observed)}!={sorted(wanted)}")
        require(validator_ast_hash(candidate) != VALIDATOR_AST_SHA256, "E_SOURCE_AST_NEGATIVE_ESCAPE")
        passed += 1
    return passed, len(cases)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def semantic_hash(value: dict[str, Any]) -> str:
    projected = copy.deepcopy(value)
    projected.pop("semantic_sha256", None)
    return sha256(canonical_bytes(projected))


def reject_constant(value: str) -> Any:
    raise ValidationError("E_NONFINITE_JSON", value)


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_DUPLICATE_JSON", key)
        result[key] = value
    return result


def strict_load_bytes(raw: bytes, source: str) -> tuple[Any, dict[str, int]]:
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=unique_pairs, parse_constant=reject_constant,
            parse_float=lambda text: _finite_float(text),
        )
    except (UnicodeError, json.JSONDecodeError, OverflowError) as error:
        raise ValidationError("E_STRICT_JSON", source) from error
    counts = {"containers": 0, "scalars": 0, "keys": 0, "max_depth": 0}

    def walk(node: Any, depth: int) -> None:
        counts["max_depth"] = max(counts["max_depth"], depth)
        if type(node) is dict:
            counts["containers"] += 1
            counts["keys"] += len(node)
            for item in node.values():
                walk(item, depth + 1)
        elif type(node) is list:
            counts["containers"] += 1
            for item in node:
                walk(item, depth + 1)
        else:
            counts["scalars"] += 1
            if type(node) is float:
                require(math.isfinite(node), "E_NONFINITE_JSON", source)

    walk(value, 0)
    counts["value_nodes"] = counts["containers"] + counts["scalars"]
    counts["all_nodes"] = counts["value_nodes"] + counts["keys"]
    return value, counts


def _finite_float(text: str) -> float:
    value = float(text)
    require(math.isfinite(value), "E_NONFINITE_JSON", text)
    return value


def nul_paths(raw: bytes) -> set[str]:
    return {item.decode("utf-8") for item in raw.split(b"\0") if item}


def status_paths(cwd: pathlib.Path = ROOT) -> set[str]:
    raw = git(["status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=cwd).stdout
    paths: set[str] = set()
    fields = [item for item in raw.split(b"\0") if item]
    index = 0
    while index < len(fields):
        field = fields[index]
        require(len(field) >= 4, "E_STATUS_PARSE", repr(field))
        paths.add(field[3:].decode("utf-8"))
        if field[:2] in {b"R ", b"C ", b" R", b" C"}:
            index += 1
        index += 1
    return paths


def ref_diagnostics(snapshot: dict[str, Any], active_tip: str, protected_tip: str, main_tip: str) -> set[str]:
    checks = (
        ("E_GIT_BRANCH", snapshot["branch"] == ACTIVE_BRANCH),
        ("E_GIT_UPSTREAM_NAME", snapshot["upstream_name"] == f"origin/{ACTIVE_BRANCH}"),
        ("E_GIT_HEAD", snapshot["head"] == active_tip),
        ("E_GIT_UPSTREAM", snapshot["upstream"] == active_tip),
        ("E_GIT_ACTIVE_TRACKING", snapshot["origin_active"] == active_tip),
        ("E_GIT_ACTIVE_LIVE", snapshot["live_active"] == active_tip),
        ("E_GIT_LOCAL_PROTECTED", snapshot["local_protected"] == protected_tip),
        ("E_GIT_PROTECTED_TRACKING", snapshot["origin_protected"] == protected_tip),
        ("E_GIT_PROTECTED_LIVE", snapshot["live_protected"] == protected_tip),
        ("E_GIT_MAIN_TRACKING", snapshot["origin_main"] == main_tip),
        ("E_GIT_MAIN_LIVE", snapshot["live_main"] == main_tip),
    )
    return {code for code, passed in checks if not passed}


def repository_snapshot(*, allow_activation_dirt: bool) -> dict[str, Any]:
    snapshot = {
        "branch": git_text(["branch", "--show-current"]),
        "head": git_text(["rev-parse", "HEAD"]),
        "upstream_name": git_text(["rev-parse", "--abbrev-ref", "@{upstream}"]),
        "upstream": git_text(["rev-parse", "@{upstream}"]),
        "origin_active": git_text(["rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}"]),
        "live_active": live_tip(ACTIVE_BRANCH),
        "local_protected": git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"]),
        "origin_protected": git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"]),
        "live_protected": live_tip(PROTECTED_BRANCH),
        "origin_main": git_text(["rev-parse", "refs/remotes/origin/main"]),
        "live_main": live_tip("main"),
    }
    diagnostics = ref_diagnostics(snapshot, snapshot["head"], PROTECTED_TIP, MAIN_TIP)
    require(not diagnostics, "E_REPOSITORY_BOUNDARY", repr(sorted(diagnostics)))
    dirt = status_paths()
    if allow_activation_dirt:
        require(not (dirt - FINAL_PATH_SET), "E_EXTRA_DIRT", repr(sorted(dirt - FINAL_PATH_SET)))
    else:
        require(not dirt, "E_PERSISTENCE_DIRTY", repr(sorted(dirt)))
    require(not git_text(["diff", "--name-only", EXPECTED_PARENT, "--", "Claude"]).splitlines(), "E_CLAUDE_TRACKED")
    require(not git_text(["ls-files", "--others", "--exclude-standard", "--", "Claude"]).splitlines(), "E_CLAUDE_UNTRACKED")
    snapshot["only_activation_allowlist_dirty"] = True
    snapshot["claude_diff_count"] = 0
    return snapshot


def stable_repository_projection(snapshot: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(snapshot)
    for key in ("head", "upstream", "origin_active", "live_active"):
        projected[key] = "<OPERATIONAL_ACTIVE_COMMIT_MASKED>"
    projected["operational_active_commit_masked"] = True
    return projected


def manifest_contract() -> dict[str, Any]:
    raw = (ROOT / MANIFEST_PATH).read_bytes()
    require(sha256(lf_bytes(raw)) == MANIFEST_SHA256_LF, "E_MANIFEST_SHA")
    document, traversal = strict_load_bytes(raw, MANIFEST_PATH)
    require(type(document) is dict and type(document.get("entries")) is list, "E_MANIFEST_SCHEMA")
    rows = document["entries"][743:826]
    require(len(rows) == 83, "E_MANIFEST_SLICE", str(len(rows)))
    require(all(row["version"] == "v1.0.23" and "/v1.0.23/" in row["path"] for row in rows), "E_MANIFEST_VERSION")
    require(not any("/v1.0.23/" in row["path"] for row in document["entries"][:743] + document["entries"][826:]), "E_MANIFEST_CONTIGUITY")
    paths = [row["path"] for row in rows]
    require(paths == sorted(paths) and len(set(paths)) == 83, "E_MANIFEST_PATHS")
    path_hash = sha256((json.dumps(paths, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8"))
    require(path_hash == PATH_SET_SHA256, "E_PATH_SET_SHA", path_hash)
    modes = Counter(row["review_mode"] for row in rows)
    roles = Counter(row["role"] for row in rows)
    require(modes == {"FULL_TEXT": 78, "FULL_PDF": 3, "FULL_IMAGE": 2}, "E_REVIEW_MODES", repr(modes))
    require(roles == {"theory": 56, "result": 17, "generated_document": 3, "figure": 2,
                      "code": 1, "test": 2, "implementation_guide": 1, "supporting_document": 1}, "E_ROLES", repr(roles))
    require(sum(row["size_bytes"] for row in rows) == 3338330, "E_MANIFEST_BYTES")
    require(sum(row["extent"]["lines"] for row in rows if row["review_mode"] == "FULL_TEXT") == 12508, "E_TEXT_LINES")
    require(sum(row["extent"]["pages"] for row in rows if row["review_mode"] == "FULL_PDF") == 129, "E_PDF_PAGES")
    blobs: list[str] = []
    pdf_extents: list[dict[str, Any]] = []
    image_extents: list[dict[str, Any]] = []
    for row in rows:
        observed_blob = git_text(["rev-parse", f"{BASELINE}:{row['path']}"])
        require(observed_blob == row["blob_sha"], "E_SOURCE_BLOB", row["path"])
        raw_blob = git_blob(BASELINE, row["path"])
        require(len(raw_blob) == row["size_bytes"], "E_SOURCE_SIZE", row["path"])
        if row["review_mode"] == "FULL_TEXT":
            require(len(raw_blob.decode("utf-8").splitlines()) == row["extent"]["lines"], "E_SOURCE_LINES", row["path"])
        elif row["review_mode"] == "FULL_PDF":
            reader = PdfReader(io.BytesIO(raw_blob), strict=True)
            observed_extent = {"pages": len(reader.pages), "encrypted": bool(reader.is_encrypted)}
            require(observed_extent == row["extent"], "E_SOURCE_PDF_EXTENT", row["path"])
            pdf_extents.append({"path": row["path"], **observed_extent})
        elif row["review_mode"] == "FULL_IMAGE":
            with Image.open(io.BytesIO(raw_blob)) as image:
                observed_extent = {
                    "width": image.width, "height": image.height, "mode": image.mode,
                    "format": image.format, "frames": image.n_frames,
                }
            require(observed_extent == row["extent"], "E_SOURCE_IMAGE_EXTENT", row["path"])
            image_extents.append({"path": row["path"], **observed_extent})
        blobs.append(observed_blob)
    require(len(set(blobs)) == 83, "E_UNIQUE_BLOBS")
    return {
        "manifest_path": MANIFEST_PATH, "manifest_sha256_lf": MANIFEST_SHA256_LF,
        "indices": [744, 826], "source_count": 83, "path_count": 83, "unique_blob_count": 83,
        "bytes": 3338330, "path_set_sha256": path_hash, "review_modes": dict(sorted(modes.items())),
        "text_lines": 12508, "pdf_pages": 129, "roles": dict(sorted(roles.items())),
        "pdf_extents": pdf_extents, "image_extents": image_extents,
        "strict_traversal": traversal,
    }


def supplemental_contract() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for name, spec in SUPPLEMENTAL.items():
        raw = git_blob(BASELINE, spec["path"])
        require(git_text(["rev-parse", f"{BASELINE}:{spec['path']}"]) == spec["blob"], "E_SUPPLEMENTAL_BLOB", name)
        require(len(raw) == spec["bytes"] and sha256(raw) == spec["sha256"], "E_SUPPLEMENTAL_IDENTITY", name)
        if "lines" in spec:
            require(len(raw.splitlines()) == spec["lines"], "E_SUPPLEMENTAL_LINES", name)
        record = {"name": name, **spec}
        if name == "jcp147":
            reader = PdfReader(io.BytesIO(raw), strict=True)
            observed_extent = {"pages": len(reader.pages), "encrypted": bool(reader.is_encrypted)}
            require(observed_extent == {"pages": spec["pages"], "encrypted": False}, "E_SUPPLEMENTAL_PDF_EXTENT", name)
            record["observed_extent"] = observed_extent
        records.append(record)
    return {"count": 3, "separate_from_manifest": True, "records": records}


def process_contract() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for commit in PROCESS_COMMITS:
        require(git(["cat-file", "-e", f"{commit}^{{commit}}"], check=False).returncode == 0, "E_PROCESS_COMMIT", commit)
        require(git(["merge-base", "--is-ancestor", commit, BASELINE], check=False).returncode == 0, "E_PROCESS_ANCESTRY", commit)
        records.append({"commit": commit, "subject": git_text(["show", "-s", "--format=%s", commit])})
    p4_path = "Claude/docs/v1.0.23/results/PHASE_P4_RESULT.md"
    require(git(["cat-file", "-e", f"{BASELINE}:{p4_path}"], check=False).returncode != 0, "E_P4_FABRICATION")
    require(git(["cat-file", "-e", f"{BASELINE}:Claude/docs/v1.0.23/results/PHASE_P0_RESULT.md"], check=False).returncode != 0, "E_P0_FABRICATION")
    return {
        "commit_count": len(records), "records": records,
        "phase_state": {"P0": "COMMIT_LEDGER_EVIDENCE", "P1": "EXECUTED", "P2": "EXECUTED",
                        "P3": "EXECUTED", "P4": "SKIPPED_D3_NOT_APPROVED", "P5": "EXECUTED"},
        "p4_result_present": False, "p0_result_present": False,
    }


def exact_prefixed(lines: list[str], prefix: str, expected: str, code: str) -> None:
    matches = [line for line in lines if line.startswith(prefix)]
    require(matches == [prefix + expected], code, repr(matches))


def control_contract() -> dict[str, Any]:
    documents: dict[str, list[str]] = {}
    for path in (RESULT_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH):
        raw = (ROOT / path).read_bytes()
        require(sha256(lf_bytes(raw)) == CONTROL_SHA256_LF[path], "E_CONTROL_SHA", path)
        documents[path] = raw.decode("utf-8").splitlines()
    result = documents[RESULT_PATH]
    require(result and result[0] == "# Phase 064 v1.0.23 Lineage Reaudit Plan Activation Result", "E_RESULT_H1")
    exact_prefixed(result, "Status: ", "`PASS_PENDING_PERSISTENCE`", "E_RESULT_STATUS")
    exact_prefixed(result, "Gate: ", "`PASS_P064_PLAN_ACTIVATION`", "E_RESULT_GATE")
    exact_prefixed(result, "Containing commit: ", "`PENDING_AT_PRECOMMIT_BY_DESIGN`", "E_RESULT_COMMIT")
    exact_prefixed(result, "Expected parent: ", f"`{EXPECTED_PARENT}`", "E_RESULT_PARENT")
    exact_prefixed(result, "Expected subject: ", f"`{EXPECTED_SUBJECT}`", "E_RESULT_SUBJECT")
    exact_prefixed(result, "Postcommit persistence terminal: ", f"`{PERSISTENCE}`", "E_RESULT_PERSISTENCE")
    parent_rows = [line for line in documents[PARENT_LEDGER_PATH] if line.startswith("| 064 |")]
    active_rows = [line for line in documents[ACTIVE_LEDGER_PATH] if line.startswith("| 064 |")]
    step_rows = [line for line in documents[ACTIVE_LEDGER_PATH] if line.startswith("| Phase 064 plan activation |")]
    handover_rows = [line for line in documents[HANDOVER_PATH] if line.startswith("| Phase 064 detailed plan activation |")]
    require(len(parent_rows) == len(active_rows) == len(step_rows) == len(handover_rows) == 1, "E_CONTROL_ROWS")
    required = (EXPECTED_PARENT, EXPECTED_SUBJECT, GATE, PERSISTENCE, "PENDING_AT_PRECOMMIT_BY_DESIGN", "Step 64")
    for name, row in (("parent", parent_rows[0]), ("active", active_rows[0]), ("step", step_rows[0]), ("handover", handover_rows[0])):
        require(all(token in row for token in required), "E_CONTROL_BINDING", name)
    current = [line for line in documents[HANDOVER_PATH] if line.startswith("15. 현재 Phase 상태:")]
    require(current == ["15. 현재 Phase 상태: Phase 064 `PLAN_ACTIVATION_PENDING_PERSISTENCE`, Current checkpoint: pre-Step 64 `PASS_P064_PLAN_ACTIVATION`"], "E_HANDOVER_CURRENT")
    records = []
    for path in NONSELF_PATHS:
        raw = (ROOT / path).read_bytes()
        records.append({"path": path, "bytes": len(raw), "physical_lines": len(raw.decode("utf-8").splitlines()), "sha256_lf": sha256(lf_bytes(raw))})
    return {"count": 6, "hash_pinned_control_documents": 4,
            "records": sorted(records, key=lambda row: row["path"]),
            "result_first": True, "validation_json_last": True}


def plan_contract() -> dict[str, Any]:
    raw = PLAN.read_bytes()
    require(sha256(lf_bytes(raw)) == PLAN_SHA256_LF, "E_PLAN_SHA")
    text = raw.decode("utf-8")
    headings = [
        "## Summary", "## Current Ground Truth", "## Phase Range", "## Exact Read Inputs",
        "## Non-goals and Scope Guards", "## Implementation Changes", "## Plan Activation Unit — Save Before Step 64",
        "## Phase 064 — v1.0.23 Reaudit", "## Phase Gate", "## Implementation Interfaces",
        "## Test and Validation Plan", "## Stop Conditions", "## Assumptions", "## Correction History",
    ]
    require(all(text.count(heading) == 1 for heading in headings), "E_PLAN_HEADINGS")
    tokens = [
        "누적 Step 범위: 64–69", "Step 64", "Step 65", "Step 66", "Step 67", "Step 68", "Step 69.1", "Step 69.2",
        GATE, "PASS_P064_LINEAGE_G", "CONDITIONAL_P064", "FAIL_P064", PERSISTENCE,
        EXPECTED_PARENT, EXPECTED_SUBJECT, "83", "12,508", "3/129", "FULL_IMAGE=2",
        "GROUND_NOT_FOUND", "10.1063/1.4802005", "10.1063/1.4802584", "P4", "omega_V", "3600",
    ]
    require(all(token in text for token in tokens), "E_PLAN_TOKENS")
    for path in FINAL_PATHS:
        require(text.count(f"`{path}`") >= 1, "E_PLAN_ACTIVATION_PATH", path)
    return {"path": PLAN_PATH, "sha256_lf": PLAN_SHA256_LF, "bytes_lf": len(lf_bytes(raw)),
            "physical_lines": len(text.splitlines()), "headings": headings,
            "cumulative_steps": ["64", "65", "66", "67", "68", "69.1", "69.2"]}


def build_payload(*, committed: bool = False) -> dict[str, Any]:
    snapshot = stable_repository_projection(repository_snapshot(allow_activation_dirt=True))
    if not committed:
        require(git_text(["rev-parse", "HEAD"]) == EXPECTED_PARENT, "E_PREDECESSOR_HEAD")
    require(git_text(["rev-parse", f"{EXPECTED_PARENT}^"]) == EXPECTED_PARENT_PARENT, "E_PREDECESSOR_PARENT")
    require(git_text(["show", "-s", "--format=%s", EXPECTED_PARENT]) == EXPECTED_PARENT_SUBJECT, "E_PREDECESSOR_SUBJECT")
    require(git_text(["diff", "--name-only", BASELINE, "HEAD", "--", "Claude/docs/v1.0.23"]) == "", "E_V1023_BASELINE_DRIFT")
    document: dict[str, Any] = {
        "schema_version": "P064-PLAN-ACTIVATION-1", "phase": "064", "generated_date": "2026-08-29",
        "gate": GATE, "status": "PASS_PENDING_PERSISTENCE", "expected_parent": EXPECTED_PARENT,
        "expected_subject": EXPECTED_SUBJECT, "persistence_terminal": PERSISTENCE,
        "authority": {"internal_plan_inventory_only": True, "external_scientific": False,
                      "external_material": False, "external_experimental": False,
                      "ref6_ref7_primary_method": False, "canonical": False, "publication_ready": False},
        "repository": snapshot, "plan": plan_contract(), "manifest": manifest_contract(),
        "supplemental": supplemental_contract(), "process": process_contract(), "controls": control_contract(),
        "literature_boundary": {
            "jcp147_original_present": True, "jcp147_pages": 10,
            "ref6": {"doi": "10.1063/1.3565476", "original_full_text": "GROUND_NOT_FOUND"},
            "ref7": {"doi": "10.1063/1.4802584", "stale_conflicting_doi": "10.1063/1.4802005", "original_full_text": "GROUND_NOT_FOUND"},
            "phase_gate_ceiling": "CONDITIONAL_P064_UNTIL_REF6_REF7_ORIGINALS_FULL_READ",
        },
        "exact_seven": {"count": 7, "paths": FINAL_PATHS, "result_first": True, "validation_json_last": True},
        "validator_identity": validator_source_contract(),
        "negative_contract": {"semantic": 27, "strict_json": 6, "source_policy": 34,
                              "actual_git": 21, "exact_diagnostics": True},
        "determinism": {"reconstructions": 2, "byte_identical": True},
    }
    document["semantic_sha256"] = semantic_hash(document)
    strict_load_bytes(pretty_bytes(document), "fresh-payload")
    return document


def document_diagnostics(document: Any, expected: dict[str, Any]) -> set[str]:
    if type(document) is not dict or set(document) != set(expected):
        return {"E_SCHEMA"}
    fields = [
        ("E_IDENTITY", ("schema_version", "phase", "generated_date")),
        ("E_GATE", ("gate", "status")), ("E_PARENT", ("expected_parent", "expected_subject")),
        ("E_PERSISTENCE", ("persistence_terminal",)), ("E_AUTHORITY", ("authority",)),
        ("E_REPOSITORY", ("repository",)), ("E_PLAN", ("plan",)), ("E_MANIFEST", ("manifest",)),
        ("E_SUPPLEMENTAL", ("supplemental",)), ("E_PROCESS", ("process",)),
        ("E_CONTROLS", ("controls",)), ("E_LITERATURE", ("literature_boundary",)),
        ("E_EXACT_SEVEN", ("exact_seven",)), ("E_VALIDATOR", ("validator_identity",)),
        ("E_NEGATIVE_CONTRACT", ("negative_contract",)), ("E_DETERMINISM", ("determinism",)),
    ]
    failures = {code for code, keys in fields if any(document[key] != expected[key] for key in keys)}
    if document["semantic_sha256"] != semantic_hash(document):
        failures.add("E_SEMANTIC_HASH")
    return failures


def run_negative_controls(expected: dict[str, Any]) -> tuple[int, int]:
    cases: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = [
        ("E_SCHEMA", lambda d: d.__setitem__("extra", 1), False),
        ("E_IDENTITY", lambda d: d.__setitem__("phase", "065"), True),
        ("E_GATE", lambda d: d.__setitem__("gate", "PASS_P064_LINEAGE_G"), True),
        ("E_PARENT", lambda d: d.__setitem__("expected_parent", "0" * 40), True),
        ("E_PERSISTENCE", lambda d: d.__setitem__("persistence_terminal", "WRONG"), True),
        ("E_AUTHORITY", lambda d: d["authority"].__setitem__("external_scientific", True), True),
        ("E_REPOSITORY", lambda d: d["repository"].__setitem__("live_protected", "0" * 40), True),
        ("E_PLAN", lambda d: d["plan"].__setitem__("sha256_lf", "0" * 64), True),
        ("E_MANIFEST", lambda d: d["manifest"].__setitem__("source_count", 82), True),
        ("E_MANIFEST", lambda d: d["manifest"].__setitem__("text_lines", 12507), True),
        ("E_MANIFEST", lambda d: d["manifest"].__setitem__("pdf_pages", 128), True),
        ("E_MANIFEST", lambda d: d["manifest"]["pdf_extents"][0].__setitem__("pages", 86), True),
        ("E_MANIFEST", lambda d: d["manifest"]["image_extents"][0].__setitem__("width", 1759), True),
        ("E_SUPPLEMENTAL", lambda d: d["supplemental"]["records"][1].__setitem__("pages", 9), True),
        ("E_SUPPLEMENTAL", lambda d: d["supplemental"]["records"][1]["observed_extent"].__setitem__("pages", 9), True),
        ("E_PROCESS", lambda d: d["process"]["phase_state"].__setitem__("P4", "EXECUTED"), True),
        ("E_PROCESS", lambda d: d["process"].__setitem__("p4_result_present", True), True),
        ("E_CONTROLS", lambda d: d["controls"].__setitem__("result_first", False), True),
        ("E_LITERATURE", lambda d: d["literature_boundary"]["ref6"].__setitem__("original_full_text", "JCP147_SUBSTITUTE"), True),
        ("E_LITERATURE", lambda d: d["literature_boundary"]["ref7"].__setitem__("doi", "10.1063/1.4802005"), True),
        ("E_LITERATURE", lambda d: d["literature_boundary"].__setitem__("phase_gate_ceiling", "PASS_P064_LINEAGE_G"), True),
        ("E_EXACT_SEVEN", lambda d: d["exact_seven"]["paths"].pop(), True),
        ("E_VALIDATOR", lambda d: d["validator_identity"].__setitem__("sha256_lf", "0" * 64), True),
        ("E_NEGATIVE_CONTRACT", lambda d: d["negative_contract"].__setitem__("actual_git", 0), True),
        ("E_DETERMINISM", lambda d: d["determinism"].__setitem__("byte_identical", False), True),
        ("E_SEMANTIC_HASH", lambda d: d.__setitem__("semantic_sha256", "0" * 64), False),
        ("E_AUTHORITY", lambda d: d["authority"].__setitem__("ref6_ref7_primary_method", True), True),
    ]
    passed = 0
    for wanted, mutation, rehash in cases:
        candidate = copy.deepcopy(expected)
        mutation(candidate)
        if rehash and set(candidate) == set(expected):
            candidate["semantic_sha256"] = semantic_hash(candidate)
        observed = document_diagnostics(candidate, expected)
        require(observed == {wanted}, "E_NEGATIVE_DIAGNOSTIC", f"{wanted}:{sorted(observed)}")
        passed += 1
    strict_cases = [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}', b'{"x":1e9999}', b'{"x":']
    for raw in strict_cases:
        try:
            strict_load_bytes(raw, "negative")
        except ValidationError as error:
            require(error.code in {"E_DUPLICATE_JSON", "E_NONFINITE_JSON", "E_STRICT_JSON"}, "E_STRICT_NEGATIVE_CODE", error.code)
        else:
            raise ValidationError("E_STRICT_NEGATIVE_ESCAPE")
    return passed, len(cases)


def remove_temp_tree(path: pathlib.Path, prefix: str) -> None:
    resolved = path.resolve()
    temp_root = pathlib.Path(tempfile.gettempdir()).resolve()
    require(resolved.parent == temp_root and resolved.name.startswith(prefix), "E_TEMP_BOUNDARY", str(resolved))

    def clear_readonly(function: Callable[..., Any], target: str, _: Any) -> None:
        os.chmod(target, stat.S_IWRITE)
        function(target)

    shutil.rmtree(resolved, onerror=clear_readonly)
    require(not resolved.exists(), "E_TEMP_CLEANUP", str(resolved))


def make_git_fixture() -> tuple[pathlib.Path, pathlib.Path, pathlib.Path, str, str]:
    prefix = "phase064-plan-git-"
    root = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
    work, origin = root / "work", root / "origin.git"
    try:
        work.mkdir()
        git(["init", "--initial-branch=main"], cwd=work)
        git(["config", "user.email", "phase064@example.invalid"], cwd=work)
        git(["config", "user.name", "Phase 064 Fixture"], cwd=work)
        git(["config", "core.autocrlf", "false"], cwd=work)
        (work / "base.txt").write_bytes(b"base\n")
        (work / "Claude").mkdir()
        (work / "Claude" / "keep.txt").write_bytes(b"protected\n")
        git(["add", "base.txt", "Claude/keep.txt"], cwd=work)
        git(["commit", "-m", "base"], cwd=work)
        base = git_text(["rev-parse", "HEAD"], cwd=work)
        git(["branch", PROTECTED_BRANCH, base], cwd=work)
        git(["branch", ACTIVE_BRANCH, base], cwd=work)
        git(["switch", "-c", "fixture/drift", base], cwd=work)
        git(["commit", "--allow-empty", "-m", "drift"], cwd=work)
        drift = git_text(["rev-parse", "HEAD"], cwd=work)
        git(["switch", ACTIVE_BRANCH], cwd=work)
        git(["init", "--bare", str(origin)], cwd=root)
        git(["remote", "add", "origin", str(origin)], cwd=work)
        git(["push", "origin", "main", PROTECTED_BRANCH, "fixture/drift"], cwd=work)
        git(["push", "-u", "origin", ACTIVE_BRANCH], cwd=work)
        git(["fetch", "origin"], cwd=work)
        git(["branch", "-D", "main"], cwd=work)
        for path in FINAL_PATHS:
            target = work / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((path + "\n").encode("utf-8"))
        git(["add", "--", *FINAL_PATHS], cwd=work)
    except Exception:
        remove_temp_tree(root, prefix)
        raise
    return root, work, origin, base, drift


def fixture_snapshot(work: pathlib.Path, origin: pathlib.Path) -> dict[str, Any]:
    return {
        "branch": git_text(["branch", "--show-current"], cwd=work),
        "head": git_text(["rev-parse", "HEAD"], cwd=work),
        "upstream_name": git_text(["rev-parse", "--abbrev-ref", "@{upstream}"], cwd=work),
        "upstream": git_text(["rev-parse", "@{upstream}"], cwd=work),
        "origin_active": git_text(["rev-parse", f"refs/remotes/origin/{ACTIVE_BRANCH}"], cwd=work),
        "live_active": git_text(["--git-dir", str(origin), "rev-parse", f"refs/heads/{ACTIVE_BRANCH}"], cwd=work),
        "local_protected": git_text(["rev-parse", f"refs/heads/{PROTECTED_BRANCH}"], cwd=work),
        "origin_protected": git_text(["rev-parse", f"refs/remotes/origin/{PROTECTED_BRANCH}"], cwd=work),
        "live_protected": git_text(["--git-dir", str(origin), "rev-parse", f"refs/heads/{PROTECTED_BRANCH}"], cwd=work),
        "origin_main": git_text(["rev-parse", "refs/remotes/origin/main"], cwd=work),
        "live_main": git_text(["--git-dir", str(origin), "rev-parse", "refs/heads/main"], cwd=work),
        "staged": nul_paths(git(["diff", "--cached", "--name-only", "-z"], cwd=work).stdout),
        "unstaged": nul_paths(git(["diff", "--name-only", "-z"], cwd=work).stdout),
        "untracked": nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"], cwd=work).stdout),
        "claude": bool(git(["status", "--porcelain=v1", "--", "Claude"], cwd=work).stdout),
        "index_equal": {path: git(["show", f":{path}"], cwd=work).stdout == (work / path).read_bytes() for path in FINAL_PATHS},
        "diff_check": git(["diff", "--cached", "--check"], cwd=work, check=False).returncode == 0,
    }


def fixture_diagnostics(snapshot: dict[str, Any], active_tip: str, protected_tip: str, main_tip: str) -> set[str]:
    checks = (
        ("E_GIT_STAGED", snapshot["staged"] == FINAL_PATH_SET),
        ("E_GIT_UNSTAGED", not snapshot["unstaged"]),
        ("E_GIT_UNTRACKED", not snapshot["untracked"]),
        ("E_GIT_CLAUDE", not snapshot["claude"]),
        ("E_GIT_INDEX", snapshot["index_equal"] == {path: True for path in FINAL_PATHS}),
        ("E_GIT_DIFF_CHECK", snapshot["diff_check"] is True),
    )
    return ref_diagnostics(snapshot, active_tip, protected_tip, main_tip) | {code for code, passed in checks if not passed}


def persistence_record(cwd: pathlib.Path, expected_commit: str, expected_bytes: dict[str, bytes]) -> dict[str, Any]:
    return {
        "head": git_text(["rev-parse", "HEAD"], cwd=cwd),
        "parent": git_text(["rev-parse", f"{expected_commit}^"], cwd=cwd),
        "subject": git_text(["show", "-s", "--format=%s", expected_commit], cwd=cwd),
        "paths": nul_paths(git(["diff-tree", "--no-commit-id", "--name-only", "-r", "-z", expected_commit], cwd=cwd).stdout),
        "blob_bytes_equal": {
            path: git_blob(expected_commit, path, cwd=cwd) == raw for path, raw in expected_bytes.items()
        },
    }


def persistence_diagnostics(record: dict[str, Any], expected_commit: str, expected_parent: str,
                            expected_subject: str) -> set[str]:
    checks = (
        ("E_PERSISTENCE_HEAD", record["head"] == expected_commit),
        ("E_PERSISTENCE_PARENT", record["parent"] == expected_parent),
        ("E_PERSISTENCE_SUBJECT", record["subject"] == expected_subject),
        ("E_PERSISTENCE_PATHS", record["paths"] == FINAL_PATH_SET),
        ("E_PERSISTENCE_BYTES", record["blob_bytes_equal"] == {path: True for path in FINAL_PATHS}),
    )
    return {code for code, passed in checks if not passed}


def persistence_repository_diagnostics(snapshot: dict[str, Any], commit: str, protected_tip: str,
                                       main_tip: str) -> set[str]:
    checks = (
        ("E_PERSISTENCE_STAGED", not snapshot["staged"]),
        ("E_PERSISTENCE_UNSTAGED", not snapshot["unstaged"]),
        ("E_PERSISTENCE_UNTRACKED", not snapshot["untracked"]),
        ("E_PERSISTENCE_CLAUDE", not snapshot["claude"]),
        ("E_PERSISTENCE_INDEX", snapshot["index_equal"] == {path: True for path in FINAL_PATHS}),
        ("E_PERSISTENCE_DIFF_CHECK", snapshot["diff_check"] is True),
    )
    return ref_diagnostics(snapshot, commit, protected_tip, main_tip) | {code for code, passed in checks if not passed}


def run_persistence_git_controls() -> tuple[int, int]:
    cases = ["positive", "parent", "subject", "path", "blob", "dirty"]
    passed = 0
    for case in cases:
        root, work, origin, base, drift = make_git_fixture()
        try:
            expected_bytes = {path: (work / path).read_bytes() for path in FINAL_PATHS}
            subject = EXPECTED_SUBJECT
            if case == "parent":
                git(["reset", "--soft", drift], cwd=work)
            elif case == "subject":
                subject = "fixture wrong subject"
            elif case == "path":
                (work / "extra.txt").write_bytes(b"extra\n")
                git(["add", "extra.txt"], cwd=work)
            elif case == "blob":
                (work / FINAL_PATHS[0]).write_bytes(b"mutated\n")
                git(["add", FINAL_PATHS[0]], cwd=work)
            git(["commit", "-m", subject], cwd=work)
            commit = git_text(["rev-parse", "HEAD"], cwd=work)
            git(["push", "origin", ACTIVE_BRANCH], cwd=work)
            git(["fetch", "origin"], cwd=work)
            if case == "dirty":
                (work / "extra.txt").write_bytes(b"dirty\n")
            observed = persistence_repository_diagnostics(fixture_snapshot(work, origin), commit, base, base)
            observed |= persistence_diagnostics(
                persistence_record(work, commit, expected_bytes), commit, base, EXPECTED_SUBJECT,
            )
            wanted = {
                "positive": set(),
                "parent": {"E_PERSISTENCE_PARENT"},
                "subject": {"E_PERSISTENCE_SUBJECT"},
                "path": {"E_PERSISTENCE_PATHS"},
                "blob": {"E_PERSISTENCE_BYTES"},
                "dirty": {"E_PERSISTENCE_UNTRACKED"},
            }[case]
            require(observed == wanted, "E_PERSISTENCE_GIT_DIAGNOSTIC",
                    f"{case}:{sorted(observed)}!={sorted(wanted)}")
            passed += 1
        finally:
            remove_temp_tree(root, "phase064-plan-git-")
    return passed, len(cases)


def run_git_controls() -> tuple[int, int]:
    cases: list[tuple[set[str], Callable[[pathlib.Path, pathlib.Path, str, str], None]]] = [
        ({"E_GIT_BRANCH"}, lambda w, o, b, d: git(["branch", "-m", "fixture/wrong"], cwd=w)),
        ({"E_GIT_UPSTREAM_NAME", "E_GIT_UPSTREAM"},
         lambda w, o, b, d: git(["branch", "--set-upstream-to=origin/fixture/drift", ACTIVE_BRANCH], cwd=w)),
        ({"E_GIT_HEAD"}, lambda w, o, b, d: git(["update-ref", f"refs/heads/{ACTIVE_BRANCH}", d], cwd=w)),
        ({"E_GIT_UPSTREAM", "E_GIT_ACTIVE_TRACKING"},
         lambda w, o, b, d: git(["update-ref", f"refs/remotes/origin/{ACTIVE_BRANCH}", d], cwd=w)),
        ({"E_GIT_ACTIVE_LIVE"}, lambda w, o, b, d: git(["--git-dir", str(o), "update-ref", f"refs/heads/{ACTIVE_BRANCH}", d], cwd=w)),
        ({"E_GIT_LOCAL_PROTECTED"}, lambda w, o, b, d: git(["update-ref", f"refs/heads/{PROTECTED_BRANCH}", d], cwd=w)),
        ({"E_GIT_PROTECTED_TRACKING"}, lambda w, o, b, d: git(["update-ref", f"refs/remotes/origin/{PROTECTED_BRANCH}", d], cwd=w)),
        ({"E_GIT_PROTECTED_LIVE"}, lambda w, o, b, d: git(["--git-dir", str(o), "update-ref", f"refs/heads/{PROTECTED_BRANCH}", d], cwd=w)),
        ({"E_GIT_MAIN_TRACKING"}, lambda w, o, b, d: git(["update-ref", "refs/remotes/origin/main", d], cwd=w)),
        ({"E_GIT_MAIN_LIVE"}, lambda w, o, b, d: git(["--git-dir", str(o), "update-ref", "refs/heads/main", d], cwd=w)),
        ({"E_GIT_UNSTAGED", "E_GIT_CLAUDE"}, lambda w, o, b, d: (w / "Claude" / "keep.txt").write_bytes(b"mutated\n")),
        ({"E_GIT_STAGED"}, lambda w, o, b, d: ((w / "extra.txt").write_bytes(b"x\n"), git(["add", "extra.txt"], cwd=w))),
        ({"E_GIT_UNTRACKED"}, lambda w, o, b, d: (w / "extra.txt").write_bytes(b"x\n")),
        ({"E_GIT_UNSTAGED", "E_GIT_INDEX"}, lambda w, o, b, d: (w / FINAL_PATHS[0]).write_bytes(b"mutated\n")),
        ({"E_GIT_DIFF_CHECK"}, lambda w, o, b, d: ((w / FINAL_PATHS[0]).write_bytes(b"bad-space \n"), git(["add", FINAL_PATHS[0]], cwd=w))),
    ]
    passed = 0
    for wanted, mutation in cases:
        root, work, origin, base, drift = make_git_fixture()
        try:
            require(not fixture_diagnostics(fixture_snapshot(work, origin), base, base, base), "E_GIT_BASELINE")
            mutation(work, origin, base, drift)
            observed = fixture_diagnostics(fixture_snapshot(work, origin), base, base, base)
            require(observed == wanted, "E_GIT_DIAGNOSTIC", f"{sorted(observed)}!={sorted(wanted)}")
            passed += 1
        finally:
            remove_temp_tree(root, "phase064-plan-git-")
    persistence_passed, persistence_total = run_persistence_git_controls()
    return passed + persistence_passed, len(cases) + persistence_total


def validate_staged() -> None:
    repository_snapshot(allow_activation_dirt=True)
    require(git_text(["rev-parse", "HEAD"]) == EXPECTED_PARENT, "E_STAGED_PARENT")
    staged = nul_paths(git(["diff", "--cached", "--name-only", "-z"]).stdout)
    unstaged = nul_paths(git(["diff", "--name-only", "-z"]).stdout)
    untracked = nul_paths(git(["ls-files", "--others", "--exclude-standard", "-z"]).stdout)
    require(staged == FINAL_PATH_SET, "E_STAGED_PATHS", repr(sorted(staged)))
    require(not unstaged and not untracked, "E_STAGED_DIRT", repr(sorted(unstaged | untracked)))
    for path in FINAL_PATHS:
        require(git(["show", f":{path}"]).stdout == (ROOT / path).read_bytes(), "E_INDEX_WORKTREE", path)
    require(git(["diff", "--cached", "--check"], check=False).returncode == 0, "E_DIFF_CHECK")


def validate_persistence(expected_commit: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", expected_commit) is not None, "E_EXPECTED_COMMIT")
    repository_snapshot(allow_activation_dirt=False)
    expected_bytes = {path: (ROOT / path).read_bytes() for path in FINAL_PATHS}
    diagnostics = persistence_diagnostics(
        persistence_record(ROOT, expected_commit, expected_bytes),
        expected_commit, EXPECTED_PARENT, EXPECTED_SUBJECT,
    )
    require(not diagnostics, "E_PERSISTENCE_CONTRACT", repr(sorted(diagnostics)))


def read_stored() -> tuple[dict[str, Any], bytes, dict[str, int]]:
    require(OUTPUT.is_file(), "E_VALIDATION_ARTIFACT_MISSING", OUTPUT_PATH)
    raw = OUTPUT.read_bytes()
    document, traversal = strict_load_bytes(raw, OUTPUT_PATH)
    require(pretty_bytes(document) == lf_bytes(raw), "E_OUTPUT_CANONICAL")
    return document, raw, traversal


def atomic_collect(raw: bytes) -> None:
    require(not OUTPUT.exists(), "E_COLLECT_REFUSES_OVERWRITE")
    require(all((ROOT / path).is_file() for path in NONSELF_PATHS), "E_RESULT_FIRST")
    temp_path = OUTPUT.with_name(OUTPUT.name + ".tmp-p064-plan")
    require(not temp_path.exists(), "E_TEMP_EXISTS")
    try:
        temp_path.write_bytes(raw)
        strict_load_bytes(temp_path.read_bytes(), str(temp_path))
        os.replace(temp_path, OUTPUT)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    require(OUTPUT.read_bytes() == raw, "E_OUTPUT_WRITE")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    args = parser.parse_args()
    modes = sum((args.collect, args.content_only, args.verify_staged, args.verify_persistence))
    require(modes == 1, "E_CLI_MODE")
    if not args.collect and not OUTPUT.is_file():
        raise ValidationError("E_VALIDATION_ARTIFACT_MISSING", OUTPUT_PATH)
    first = build_payload(committed=args.verify_persistence)
    second = build_payload(committed=args.verify_persistence)
    first_raw, second_raw = pretty_bytes(first), pretty_bytes(second)
    require(first_raw == second_raw, "E_DETERMINISM", "2/2")
    if args.collect:
        negative_passed, negative_total = run_negative_controls(first)
        policy_passed, policy_total = run_source_policy_controls(VALIDATOR.read_bytes())
        git_passed, git_total = run_git_controls()
        atomic_collect(first_raw)
        print(f"PASS_P064_PLAN_NEGATIVE {negative_passed}/{negative_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
        print(f"PASS_P064_PLAN_SOURCE_POLICY {policy_passed}/{policy_total} self_hash=PINNED")
        print("PASS_P064_PLAN_DETERMINISM 2/2")
        print("PASS_P064_PLAN_ACTIVATION collect=JSON_LAST result_first=true source=83/83")
        return 0
    stored, stored_raw, traversal = read_stored()
    require(not document_diagnostics(stored, first), "E_STORED_DOCUMENT", repr(sorted(document_diagnostics(stored, first))))
    require(stored_raw == first_raw, "E_STORED_BYTES")
    full = args.verify_staged or args.verify_persistence
    if args.run_negative_probes or full:
        negative_passed, negative_total = run_negative_controls(stored)
        policy_passed, policy_total = run_source_policy_controls(VALIDATOR.read_bytes())
        git_passed, git_total = run_git_controls()
        print(f"PASS_P064_PLAN_NEGATIVE {negative_passed}/{negative_total} strict_json=6/6 git_boundary={git_passed}/{git_total}")
        print(f"PASS_P064_PLAN_SOURCE_POLICY {policy_passed}/{policy_total} self_hash=PINNED")
    if args.determinism_check or full:
        print("PASS_P064_PLAN_DETERMINISM 2/2")
    if args.content_only:
        print(f"PASS_P064_PLAN_CONTENT source=83/83 strict_nodes={traversal['all_nodes']}")
    elif args.verify_staged:
        validate_staged()
        print("PASS_P064_PLAN_ACTIVATION_STAGED exact-seven=7/7")
    else:
        require(args.expected_commit is not None, "E_EXPECTED_COMMIT")
        validate_persistence(args.expected_commit)
        print(f"{PERSISTENCE} commit={args.expected_commit}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationError, KeyError, IndexError, TypeError, ValueError, OSError, UnicodeError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        code = error.code if isinstance(error, ValidationError) else type(error).__name__
        print(f"FAIL_P064_PLAN_CONTENT {code}: {error}")
        raise SystemExit(1)
