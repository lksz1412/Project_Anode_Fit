#!/usr/bin/env python3
"""Independent validator for Phase 065 Step 72.

The validator rebuilds the TeX citation census from frozen Git blobs, checks
the mathematical invariants and authority ceilings, and enforces the exact
seven-path Git transaction in staged and persistence modes.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "5978da8626406879609b0dd5792f79143015e67f"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
SUBJECT = "audit(phase065): bound v1024 skew material authority"
PASS_CONTENT = "PASS_P065_STEP72_AUTHORITY_WITH_CONCERNS"
PASS_PERSISTENCE = "PASS_P065_STEP72_PERSISTENCE"
MATRIX = Path("Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json")
BUILDER = Path("Codex/work/v1024_phase065/build_phase065_step72.py")
RESULT = Path("Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md")
EXACT_PATHS = sorted([
    str(BUILDER).replace("\\", "/"),
    str(Path("Codex/work/v1024_phase065/validate_phase065_step72.py")).replace("\\", "/"),
    str(MATRIX).replace("\\", "/"),
    str(RESULT).replace("\\", "/"),
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
])
PROJECTION_SHA256 = {
    "material_claims": "3f2e70ed1beb4b4a619d6d04ff7e2260b7f76234451b751c88436c965ee0bb25",
    "derivations": "8392bcaae06f8cc50c528e2df834fa5ae94c7a73d6618a5b21082ce7788537c9",
    "genealogy": "924a251cccba16cdb67b144a1b962e4e235b0e5916680ee5e7313067e9871b3b",
    "bibliographic_conflicts": "f38119098317ae15dc841828db0f4b3c63a9a960649179a547968971f394d8eb",
    "metadata_verifications": "8a9b9de0a71fd9527aa09ed1811a794cf60aedc6e7eb69da06271a82ba7b222c",
    "input_routes": "7baa28b1a231b0dfa438ddd7477051795130da5d8f72811fafd1d93b5f22fc28",
    "non_graft": "59b58778f433bfd5131a4811ec9b54979ab7060a590e7b4ffab5708407cf29bf",
    "authority": "1a6ba2878d924b7bd15267f0ab08488ec3ff52174b9f78b988628fc25be635e1",
}


class AuditError(RuntimeError):
    pass


def fail(code: str, detail: str = "") -> None:
    raise AuditError(f"{code}{': ' + detail if detail else ''}")


def run_process(argv: list[str], *, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        argv, check=False, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=text, encoding="utf-8" if text else None,
    )


def git(*args: str, text: bool = True) -> str | bytes:
    cp = run_process(["git", *args], text=text)
    if cp.returncode:
        err = cp.stderr if text else cp.stderr.decode("utf-8", "replace")
        fail("E_GIT", f"git {' '.join(args)}: {err.strip()}")
    return cp.stdout


def blob(path: str, rev: str = BASELINE) -> bytes:
    return git("show", f"{rev}:{path}", text=False)  # type: ignore[return-value]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_semantic(obj: dict) -> str:
    clone = copy.deepcopy(obj)
    clone.pop("semantic_sha256", None)
    return sha256(json.dumps(clone, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode("utf-8"))


def projection_sha(value) -> str:
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode("utf-8"))


def strict_json_loads(text: str) -> dict:
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out: fail("E_JSON_DUPLICATE_KEY", key)
            out[key] = value
        return out
    def constant(value: str):
        fail("E_JSON_NONFINITE", value)
    value = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    if not isinstance(value, dict): fail("E_JSON_ROOT")
    return value


def strip_tex_comments(text: str) -> str:
    rows = []
    for line in text.splitlines():
        cut = len(line)
        for match in re.finditer(r"%", line):
            i = match.start()
            backslashes = 0
            j = i - 1
            while j >= 0 and line[j] == "\\":
                backslashes += 1
                j -= 1
            if backslashes % 2 == 0:
                cut = i
                break
        rows.append(line[:cut])
    return "\n".join(rows)


def doi_values(text: str) -> list[str]:
    found = re.findall(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.I)
    return [x.rstrip(".,;:)}]\\").lower() for x in found]


def census(paths: list[str], memberships: dict[str, list[str]]) -> dict:
    files = []
    all_bib: list[str] = []
    all_cite: list[str] = []
    all_doi: list[str] = []
    for path in sorted(paths):
        raw = blob(path)
        clean = strip_tex_comments(raw.decode("utf-8"))
        bib = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", clean)
        cite = []
        for group in re.findall(r"\\cite\w*\s*(?:\[[^\]]*\]\s*)*\{([^}]+)\}", clean):
            cite.extend(k.strip() for k in group.split(",") if k.strip())
        dois = doi_values(clean)
        all_bib.extend(bib); all_cite.extend(cite); all_doi.extend(dois)
        files.append({
            "path": path,
            "git_blob": str(git("rev-parse", f"{BASELINE}:{path}")).strip(),
            "sha256": sha256(raw),
            "lines": len(raw.decode("utf-8").splitlines()),
            "closures": sorted(memberships.get(path, [])),
            "bibitem_occurrences": len(bib),
            "citation_occurrences": len(cite),
            "doi_occurrences": len(dois),
            "undefined_keys": sorted(set(cite) - set(bib)),
        })
    return {
        "files": files,
        "summary": {
            "files": len(files),
            "bibitem_occurrences": len(all_bib),
            "unique_bibitem_keys": len(set(all_bib)),
            "citation_occurrences": len(all_cite),
            "unique_citation_keys": len(set(all_cite)),
            "doi_occurrences": len(all_doi),
            "unique_doi_strings": len(set(all_doi)),
            "globally_undefined_keys": sorted(set(all_cite) - set(all_bib)),
            "globally_unused_bibitem_keys": sorted(set(all_bib) - set(all_cite)),
        },
    }


def load_topology() -> dict:
    return json.loads(blob("Codex/results/PHASE_065_SOURCE_PROCESS_TOPOLOGY.json", EXPECTED_PARENT))


def load_first_json_fence(path: str) -> dict:
    text = blob(path, EXPECTED_PARENT).decode("utf-8")
    marker = "```json"
    if marker not in text:
        fail("E_PARENT_JSON_FENCE", path)
    payload = text.split(marker, 1)[1].split("```", 1)[0]
    return strict_json_loads(payload)


def assert_equal(actual, expected, code: str) -> None:
    if actual != expected:
        fail(code, f"expected={expected!r}, actual={actual!r}")


def validate_derivations(obj: dict) -> None:
    d = {row["id"]: row for row in obj["derivations"]}
    assert_equal(sorted(d), ["D72-B1", "D72-B2", "D72-B3", "D72-B4"], "E_DERIVATION_IDS")

    ideal = d["D72-B1"]
    fwhm = 4.0 * math.acosh(math.sqrt(2.0))
    if not math.isclose(ideal["dimensionless_fwhm"], fwhm, rel_tol=0, abs_tol=1e-12):
        fail("E_LOGISTIC_FWHM")
    expected_v = fwhm * 8.31446261815324 * 298.15 / 96485.33212
    if not math.isclose(ideal["test_fwhm_V"], expected_v, rel_tol=0, abs_tol=1e-15):
        fail("E_LOGISTIC_FWHM_DIMENSIONAL")
    assert_equal(ideal["signed_derivative"], "dQ_insert/dV=-(QF/RT)x(1-x)", "E_LOGISTIC_SIGN")
    assert_equal(ideal["signed_area_over_increasing_V"], "-Q", "E_LOGISTIC_SIGNED_AREA")
    assert_equal(ideal["magnitude_area"], "Q", "E_LOGISTIC_MAGNITUDE_AREA")
    # Independent dimensionless quadrature: integral 1/4 sech^2(z/2) dz = 1.
    n = 20000; lo = -20.0; hi = 20.0; h = (hi - lo) / n
    vals = [0.25 / math.cosh((lo + i*h)/2.0)**2 for i in range(n + 1)]
    area = h * (0.5*vals[0] + sum(vals[1:-1]) + 0.5*vals[-1])
    if not math.isclose(area, 1.0, rel_tol=0, abs_tol=1e-8): fail("E_LOGISTIC_QUADRATURE")

    reg = d["D72-B2"]
    assert_equal(reg["critical_omega_over_rt"], 2.0, "E_REGSOL_CRITICAL")
    assert_equal(reg["critical_composition"], 0.5, "E_REGSOL_CRITICAL_X")
    assert_equal(reg["symmetric_binodal_constraints"],
                 "Omega>2RT; 0<xa<1/2; xb=1-xa>1/2", "E_BINODAL_CONSTRAINTS")
    assert_equal(reg["trivial_root_excluded"],
                 "x=1/2 is stationary but is not a coexistence endpoint for Omega>2RT",
                 "E_BINODAL_TRIVIAL_ROOT")
    expected_sp = [(1.0-math.sqrt(1.0-2.0/3.0))/2.0,
                   (1.0+math.sqrt(1.0-2.0/3.0))/2.0]
    for got, exp in zip(reg["spinodal_test_endpoints"], expected_sp):
        if not math.isclose(got, exp, rel_tol=0, abs_tol=1e-15): fail("E_SPINODAL_TEST")
    # Independent nontrivial binodal root and common-tangent test for Omega/(RT)=3.
    def mu3(x: float) -> float: return math.log(x/(1.0-x)) + 3.0*(1.0-2.0*x)
    a, b = 1e-9, 0.49
    for _ in range(120):
        m = (a+b)/2.0
        if mu3(m) > 0: b = m
        else: a = m
    xa = (a+b)/2.0; xb = 1.0-xa
    if not (0 < xa < 0.5 < xb < 1): fail("E_BINODAL_NONTRIVIAL")
    if abs(mu3(xa)) > 1e-12 or abs(mu3(xb)) > 1e-12: fail("E_BINODAL_MU")
    def g3(x: float) -> float:
        return x*math.log(x)+(1.0-x)*math.log(1.0-x)+3.0*x*(1.0-x)
    if abs((g3(xb)-g3(xa))/(xb-xa)) > 1e-12: fail("E_BINODAL_TANGENT")

    skew = d["D72-B3"]
    assert_equal(skew["weight_conditions"], [
        "A is measurable along x(V)", "A>=0 almost everywhere",
        "0<integral A(x(V),V)p0(V)dV<infinity"], "E_SKEW_WEIGHT_CONDITIONS")
    assert_equal(skew["symmetry_preserving_condition"],
                 "A(x(V),V)=A(1-x(V),2U0-V) almost everywhere in V", "E_SKEW_PATH_SYMMETRY")
    assert_equal(skew["symmetry_break_condition"],
                 "The pathwise equality fails on a set of nonzero measure", "E_SKEW_BREAK")
    if "exp[-DeltaG_dagger" not in skew["barrier_closure_example"]:
        fail("E_SKEW_BARRIER_CLOSURE")

    blend = d["D72-B4"]
    assert_equal(blend["selected_basis"], "1 g total active solids", "E_BLEND_SELECTED_BASIS")
    assert_equal(blend["single_declared_basis_required"], True, "E_BLEND_BASIS")
    assert_equal(blend["finite_rate_current_balance"], "I=I_gr+I_Si", "E_BLEND_CURRENT_BALANCE")
    assert_equal(blend["capacity_fraction_si"],
                 "f_Si=m_Si q*_Si/[m_Si q*_Si+m_gr q*_gr]", "E_BLEND_FRACTION")
    m_si, q_si, q_gr = 0.1, 1000.0, 372.0
    f_si = m_si*q_si/(m_si*q_si+(1.0-m_si)*q_gr)
    if not math.isclose(f_si, 0.22999080036798528, abs_tol=1e-15): fail("E_BLEND_NUMERIC")


def validate_material_claims(obj: dict) -> None:
    expected = {
        "graphite": 9, "LCO": 8, "Si": 6, "blend": 5,
    }
    required_keys = {
        "claim_id", "material", "proposition", "derivation_id", "source_tier",
        "exact_anchor", "implementation_state", "default_state", "validation_state",
        "applicability", "status", "supersession", "ceiling", "source_refs",
    }
    allowed_source_tiers = {"FROZEN_INTERNAL_CODE", "FROZEN_INTERNAL_DOCUMENT",
                            "FROZEN_INTERNAL_MIXED"}
    allowed_implementation = {"IMPLEMENTED", "DOCUMENTED_ONLY", "ABSENT"}
    allowed_defaults = {"DISABLED", "PROFILE_DEPENDENT", "NOT_APPLICABLE"}
    allowed_validation = {"GROUND_NOT_FOUND", "EXTERNAL_UNVERIFIED", "SUPERSEDED",
                          "CONTRADICTED", "INTERNAL_ONLY"}
    rows = obj["material_claims"]
    counts = {k: 0 for k in expected}; ids = []
    binding_lines = {r["path"]: r["lines"] for r in obj["source_bindings"]}
    for row in rows:
        if set(row) != required_keys:
            fail("E_MATERIAL_ROW_SCHEMA", row.get("claim_id", "?"))
        claim_id = row["claim_id"]
        ids.append(claim_id)
        if row["material"] not in counts: fail("E_MATERIAL_ENUM", claim_id)
        counts[row["material"]] += 1
        for field in required_keys - {"exact_anchor", "source_refs"}:
            if not isinstance(row[field], str) or not row[field]:
                fail("E_MATERIAL_ROW_FIELDS", f"{claim_id}:{field}")
        if row["derivation_id"] not in {"D72-B1", "D72-B2", "D72-B3", "D72-B4"}:
            fail("E_MATERIAL_DERIVATION_ENUM", claim_id)
        if row["source_tier"] not in allowed_source_tiers:
            fail("E_MATERIAL_SOURCE_TIER_ENUM", claim_id)
        if row["implementation_state"] not in allowed_implementation:
            fail("E_MATERIAL_IMPLEMENTATION_ENUM", claim_id)
        if row["default_state"] not in allowed_defaults:
            fail("E_MATERIAL_DEFAULT_ENUM", claim_id)
        if row["validation_state"] not in allowed_validation:
            fail("E_MATERIAL_VALIDATION_ENUM", claim_id)
        if row["supersession"] not in {"ACTIVE_AUDIT_BOUNDARY", "SUPERSEDED_BY_FINAL_V1024_RECORD"}:
            fail("E_MATERIAL_SUPERSESSION_ENUM", claim_id)
        refs = row.get("source_refs")
        if not isinstance(refs, list) or not refs: fail("E_MATERIAL_SOURCE_REFS", claim_id)
        assert_equal(row["exact_anchor"], refs, "E_MATERIAL_EXACT_ANCHOR")
        for ref in refs:
            path = ref.get("path"); spec = ref.get("lines", "")
            if set(ref) != {"path", "lines"}: fail("E_MATERIAL_REF_SCHEMA", claim_id)
            if path not in binding_lines: fail("E_MATERIAL_UNBOUND_PATH", f"{claim_id}:{path}")
            for part in spec.split(","):
                nums = part.strip().split("-")
                if len(nums) not in (1, 2) or not all(n.isdigit() for n in nums):
                    fail("E_MATERIAL_LINE_SYNTAX", f"{claim_id}:{spec}")
                first = int(nums[0]); last = int(nums[-1])
                if first < 1 or last < first or last > binding_lines[path]:
                    fail("E_MATERIAL_LINE_RANGE", f"{claim_id}:{path}:{part}")
    assert_equal(counts, expected, "E_MATERIAL_COUNTS")
    assert_equal(len(ids), len(set(ids)), "E_MATERIAL_IDS")


PROCESS_APIS = {
    "run", "Popen", "call", "check_call", "check_output", "getoutput",
    "getstatusoutput", "system", "popen",
    "create_subprocess_exec", "create_subprocess_shell", "execv", "execve",
    "execl", "execle", "execlp", "execlpe", "execvp", "execvpe", "fork",
    "forkpty", "posix_spawn", "posix_spawnp",
    "spawnl", "spawnle", "spawnlp", "spawnlpe", "spawnv", "spawnve",
    "spawnvp", "spawnvpe", "startfile",
}
FILESYSTEM_MUTATORS = {
    "write", "write_text", "write_bytes", "writelines", "mkdir", "makedirs",
    "unlink", "remove", "removedirs", "replace", "rename", "renames", "rmdir",
    "touch", "symlink", "symlink_to", "link", "link_to", "move", "copy",
    "copy2", "copyfile", "copytree", "rmtree", "truncate", "mkstemp",
    "NamedTemporaryFile", "TemporaryFile", "fsync", "fdopen", "open", "chmod",
    "copy_into", "move_into", "mknod", "mkfifo", "chown", "lchmod", "lchown",
    "hardlink_to", "mkdtemp", "TemporaryDirectory", "utime", "setxattr",
    "removexattr", "chflags", "lchflags", "chdir", "fchdir", "chroot", "umask",
}
PROTECTED_CALLABLES = {"run_process", "git", "subprocess", "atomic_json_last_collect"}
PROTECTED_BINDINGS = PROTECTED_CALLABLES | {"BUILDER"}
EXECUTION_APIS = {"exec", "eval", "compile", "__import__", "import_module", "run_path", "run_module"}
LOADER_APIS = {
    "spec_from_file_location", "module_from_spec", "exec_module", "find_spec",
    "SourceFileLoader", "SourcelessFileLoader", "ExtensionFileLoader",
    "load_module", "create_module",
}
NETWORK_APIS = {"create_connection", "connect", "connect_ex", "urlopen", "request"}
ENVIRONMENT_APIS = {"putenv", "unsetenv"}
DYNAMIC_DUNDER_APIS = {
    "__call__", "__class__", "__closure__", "__code__", "__delattr__",
    "__func__", "__getattr__", "__getattribute__", "__globals__",
    "__import__", "__self__", "__setattr__", "__subclasses__",
}
READ_ONLY_GIT_COMMANDS = {"branch", "diff", "diff-tree", "ls-remote", "rev-parse", "show", "status"}
SAFE_GIT_DYNAMIC_NAMES = {"PROTECTED_BRANCH", "PROTECTED_TIP", "expected_commit",
                          "expected_tip", "first_commit", "first_parent", "head"}
SAFE_GIT_JOINED_STRINGS = {
    "f'{rev}:{path}'", "f':{path_text}'", "f':{result_path}'", "f':{path}'",
    "f'HEAD:{path}'",
    "f'refs/heads/{PROTECTED_BRANCH}'", "f'refs/heads/{BRANCH}'",
    "f'{BASELINE}^{{commit}}'", "f'origin/{PROTECTED_BRANCH}'", "f'origin/{BRANCH}'",
    "f\"{BASELINE}:{row['path']}\"", "f'{BASELINE}:{path}'",
}
ALLOWED_GIT_OPTIONS = {
    "branch": {"--show-current"},
    "diff": {"--cached", "--check", "--name-only", "--name-status", "--"},
    "diff-tree": {"--name-status", "--no-commit-id", "-r"},
    "ls-remote": {"--heads"},
    "rev-parse": {"--abbrev-ref"},
    "show": {"-s", "--format=%P", "--format=%s"},
    "status": {"--porcelain", "-uall"},
}
EXPECTED_BUILDER_AST_SHA256 = "d4c14a4571c198886545fdb117242faad3a3233391adb676bfdd657552240633"
EXPECTED_ATOMIC_COLLECTOR_AST_SHA256 = "5dbd7d75e71c813f7e88be34e71002db7a7a63b2ab15a9b93821899b5a5ee87c"
EXPECTED_LOADER_AST_SHA256 = "1465458b70ae0099f259476557005d7100ed8e36cc58b82216157b0e27971e2c"
EXPECTED_WRAPPER_AST_SHA256 = {
    "run_process": {
        "2ba87286b25d4a196153182720785d50dc5dd117a2eb9b2a072dfe8f71f3f114",
        "71ef5e4f34eece23052d712047bcd1c5b16523a1c25ffddb914f3d2dbfbece76",
    },
    "git": {
        "87db67c20da6077464e86ab8df3d080052dbfdf9097ee62d1332b5ef93277816",
        "f1c91f134d763a1faa6c1bcf0bb09aa4fbe5e5552500cc4c7c38aa4f491104ff",
    },
}


def call_owner_map(tree: ast.AST) -> dict[ast.Call, str]:
    owners: dict[ast.Call, str] = {}

    class OwnerVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.stack: list[str] = []

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_Call(self, node: ast.Call) -> None:
            owners[node] = self.stack[-1] if self.stack else "<module>"
            self.generic_visit(node)

    OwnerVisitor().visit(tree)
    return owners


def source_policy_errors(source: str, *, require_contract: bool) -> list[str]:
    """Return static-policy violations without importing or executing source."""
    errors: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [f"syntax:{exc.lineno}"]
    owners = call_owner_map(tree)
    deny_imports = {"socket", "urllib", "requests", "http", "httpx", "aiohttp", "ftplib"}
    deny_child_imports = {"asyncio", "builtins", "multiprocessing", "pty"}
    allowed_import_roots = {
        "argparse", "ast", "copy", "hashlib", "importlib", "json", "math",
        "os", "re", "subprocess", "sys", "tempfile",
    }
    subprocess_imports = 0
    definitions: dict[str, int] = {}
    process_counts: dict[str, int] = {}
    run_process_counts: dict[str, int] = {}
    top_level_definitions = {node.name for node in tree.body
                             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    candidate_builder_role = {"build", "guard_output", "atomic_json_last_collect", "main"} \
        <= top_level_definitions and "check_determinism" not in top_level_definitions
    module_builder_assignments = {id(node) for node in tree.body if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "BUILDER" for target in node.targets)}
    parents = {child: parent for parent in ast.walk(tree)
               for child in ast.iter_child_nodes(parent)}

    def target_names(target: ast.AST) -> set[str]:
        if isinstance(target, ast.Name):
            return {target.id}
        if isinstance(target, ast.Starred):
            return target_names(target.value)
        if isinstance(target, (ast.Tuple, ast.List)):
            return set().union(*(target_names(x) for x in target.elts))
        return set()

    def target_root_names(target: ast.AST) -> set[str]:
        if isinstance(target, (ast.Attribute, ast.Subscript)):
            return target_root_names(target.value)
        return target_names(target)

    def pattern_names(pattern: ast.AST) -> set[str]:
        names: set[str] = set()
        for item in ast.walk(pattern):
            if isinstance(item, ast.MatchAs) and item.name:
                names.add(item.name)
            elif isinstance(item, ast.MatchStar) and item.name:
                names.add(item.name)
            elif isinstance(item, ast.MatchMapping) and item.rest:
                names.add(item.rest)
        return names

    def binding_events(scope: ast.AST) -> list[tuple[str, ast.AST]]:
        events: list[tuple[str, ast.AST]] = []
        for item in ast.walk(scope):
            targets: list[ast.AST] = []
            if isinstance(item, ast.Assign):
                targets = list(item.targets)
            elif isinstance(item, (ast.AnnAssign, ast.AugAssign, ast.NamedExpr)):
                targets = [item.target]
            elif isinstance(item, (ast.For, ast.AsyncFor, ast.comprehension)):
                targets = [item.target]
            elif isinstance(item, ast.withitem) and item.optional_vars is not None:
                targets = [item.optional_vars]
            elif isinstance(item, ast.Delete):
                targets = list(item.targets)
            for target in targets:
                for name in target_root_names(target):
                    events.append((name, item))
            if isinstance(item, ast.ExceptHandler) and item.name:
                events.append((item.name, item))
            elif isinstance(item, ast.match_case):
                events.extend((name, item) for name in pattern_names(item.pattern))
        return events

    def ast_unparse_sha(node: ast.AST) -> str:
        return sha256(ast.unparse(node).encode("utf-8"))

    def static_value(node: ast.AST):
        try:
            return ast.literal_eval(node)
        except (ValueError, TypeError, SyntaxError):
            return None

    def is_sensitive_leaf(node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            parent = parents.get(node)
            if isinstance(parent, ast.Attribute) and parent.value is node:
                return False
            return node.id in PROTECTED_CALLABLES or node.id in PROCESS_APIS \
                or node.id in EXECUTION_APIS
        return isinstance(node, ast.Attribute) and (
            node.attr in PROCESS_APIS or node.attr in FILESYSTEM_MUTATORS
            or node.attr in EXECUTION_APIS or node.attr in LOADER_APIS
            or node.attr in NETWORK_APIS or node.attr in ENVIRONMENT_APIS)

    def is_direct_callee_leaf(node: ast.AST) -> bool:
        current = node
        while current in parents and isinstance(parents[current], (ast.Attribute, ast.Subscript)):
            current = parents[current]
        return current in parents and isinstance(parents[current], ast.Call) \
            and parents[current].func is current

    def sensitive_reference(node: ast.AST) -> bool:
        """Find transported callable references, but not the callee of a normal call."""
        if not isinstance(node, ast.AST):
            return False
        if isinstance(node, ast.Name):
            return node.id in PROTECTED_CALLABLES or node.id in PROCESS_APIS \
                or node.id in EXECUTION_APIS
        if isinstance(node, ast.Attribute):
            return node.attr in PROCESS_APIS or node.attr in FILESYSTEM_MUTATORS \
                or node.attr in EXECUTION_APIS or node.attr in LOADER_APIS \
                or node.attr in NETWORK_APIS or node.attr in ENVIRONMENT_APIS
        if isinstance(node, ast.Call):
            return any(sensitive_reference(arg) for arg in node.args) or any(
                sensitive_reference(keyword.value) for keyword in node.keywords)
        if isinstance(node, ast.Dict):
            return any(sensitive_reference(x) for x in (*node.keys, *node.values) if x is not None)
        if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
            return any(sensitive_reference(x) for x in node.elts)
        if isinstance(node, ast.Subscript):
            return sensitive_reference(node.value) or sensitive_reference(node.slice)
        if isinstance(node, ast.Lambda):
            return sensitive_reference(node.body)
        return any(sensitive_reference(child) for child in ast.iter_child_nodes(node))

    for node in ast.walk(tree):
        if is_sensitive_leaf(node) and not is_direct_callee_leaf(node):
            errors.append(f"sensitive-reference-transport:{node.lineno}")
        if isinstance(node, ast.Attribute) and node.attr == "__dict__":
            errors.append(f"dynamic-dict-access:{node.lineno}")
        if isinstance(node, ast.Attribute) and node.attr in {"environ", "environb"}:
            errors.append(f"environment-access:{node.lineno}")
        if isinstance(node, ast.Attribute) and node.attr in DYNAMIC_DUNDER_APIS:
            errors.append(f"dynamic-dunder-access:{node.attr}:{node.lineno}")
        if isinstance(node, ast.Name) and node.id == "__builtins__":
            errors.append(f"dynamic-builtins-access:{node.lineno}")
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            definitions[node.name] = definitions.get(node.name, 0) + 1
            if node.name in PROTECTED_BINDINGS and not (
                    isinstance(parents.get(node), ast.Module)
                    and node.name in {"run_process", "git", "atomic_json_last_collect"}):
                errors.append(f"protected-definition:{node.name}:{node.lineno}")
            if set(a.arg for a in (*node.args.posonlyargs, *node.args.args,
                                   *node.args.kwonlyargs,
                                   *([node.args.vararg] if node.args.vararg else []),
                                   *([node.args.kwarg] if node.args.kwarg else []))) \
                    & PROTECTED_BINDINGS:
                errors.append(f"protected-argument:{node.name}:{node.lineno}")
            defaults = [*node.args.defaults, *node.args.kw_defaults]
            if any(value is not None and sensitive_reference(value) for value in defaults):
                errors.append(f"sensitive-default:{node.name}:{node.lineno}")
            annotations = [arg.annotation for arg in (*node.args.posonlyargs, *node.args.args,
                           *node.args.kwonlyargs) if arg.annotation is not None]
            if node.args.vararg and node.args.vararg.annotation is not None:
                annotations.append(node.args.vararg.annotation)
            if node.args.kwarg and node.args.kwarg.annotation is not None:
                annotations.append(node.args.kwarg.annotation)
            if node.returns is not None:
                annotations.append(node.returns)
            if any(sensitive_reference(value) for value in annotations):
                errors.append(f"sensitive-annotation:{node.name}:{node.lineno}")
            if any(sensitive_reference(value) for value in node.decorator_list):
                errors.append(f"sensitive-decorator:{node.name}:{node.lineno}")
        elif isinstance(node, ast.ClassDef):
            if node.name in PROTECTED_BINDINGS:
                errors.append(f"protected-class-definition:{node.name}:{node.lineno}")
        elif isinstance(node, ast.Lambda):
            lambda_names = {arg.arg for arg in (
                *node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs,
                *([node.args.vararg] if node.args.vararg else []),
                *([node.args.kwarg] if node.args.kwarg else []),
            )}
            if lambda_names & PROTECTED_BINDINGS:
                errors.append(f"protected-lambda-argument:{sorted(lambda_names & PROTECTED_BINDINGS)}:{node.lineno}")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root not in allowed_import_roots:
                    errors.append(f"unexpected-import-root:{root}:{node.lineno}")
                if root in deny_imports:
                    errors.append(f"network-import:{root}:{node.lineno}")
                if root in deny_child_imports:
                    errors.append(f"child-capable-import:{root}:{node.lineno}")
                if root in {"os", "subprocess", "importlib"} and alias.asname is not None:
                    errors.append(f"sensitive-module-alias:{root}:{node.lineno}")
                bound_name = alias.asname or alias.name.split(".")[0]
                if bound_name in PROTECTED_BINDINGS and not (
                        root == "subprocess" and alias.name == "subprocess"
                        and alias.asname is None):
                    errors.append(f"protected-import-binding:{bound_name}:{node.lineno}")
                if root == "subprocess":
                    subprocess_imports += 1
                    if alias.name != "subprocess" or alias.asname is not None:
                        errors.append(f"subprocess-alias:{node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if not (node.module == "__future__"
                    and [(alias.name, alias.asname) for alias in node.names]
                    == [("annotations", None)]) \
                    and not (node.module == "pathlib"
                             and [(alias.name, alias.asname) for alias in node.names]
                             == [("Path", None)]):
                errors.append(f"unexpected-from-import:{node.module}:{node.lineno}")
            if root in deny_imports:
                errors.append(f"network-import:{root}:{node.lineno}")
            if root in deny_child_imports | {"os"}:
                errors.append(f"sensitive-from-import:{root}:{node.lineno}")
            for alias in node.names:
                sensitive_imports = (PROCESS_APIS | FILESYSTEM_MUTATORS | EXECUTION_APIS
                                     | NETWORK_APIS | ENVIRONMENT_APIS | LOADER_APIS)
                if alias.name in sensitive_imports or alias.asname in sensitive_imports:
                    errors.append(f"sensitive-symbol-import:{root}:{alias.name}:{node.lineno}")
                bound_name = alias.asname or alias.name
                if bound_name in PROTECTED_BINDINGS:
                    errors.append(f"protected-from-import-binding:{bound_name}:{node.lineno}")
            if root == "subprocess":
                errors.append(f"subprocess-from-import:{node.lineno}")
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            names = set().union(*(target_names(t) for t in targets))
            protected = names & PROTECTED_BINDINGS
            if protected and not (protected == {"BUILDER"} and id(node) in module_builder_assignments):
                errors.append(f"protected-rebind:{sorted(protected)}:{node.lineno}")
            if sensitive_reference(value):
                errors.append(f"sensitive-alias:{node.lineno}")
        elif isinstance(node, ast.AugAssign):
            names = target_root_names(node.target)
            if names & PROTECTED_BINDINGS:
                errors.append(f"protected-augassign:{sorted(names & PROTECTED_BINDINGS)}:{node.lineno}")
            if sensitive_reference(node.value):
                errors.append(f"sensitive-augassign:{node.lineno}")
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            names = target_names(node.target)
            if names & PROTECTED_BINDINGS:
                errors.append(f"protected-loop-binding:{sorted(names & PROTECTED_BINDINGS)}:{node.lineno}")
        elif isinstance(node, ast.comprehension):
            names = target_names(node.target)
            if names & PROTECTED_BINDINGS:
                errors.append(f"protected-comprehension-binding:{sorted(names & PROTECTED_BINDINGS)}")
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            names = set().union(*(target_names(item.optional_vars) for item in node.items
                                  if item.optional_vars is not None))
            if names & PROTECTED_BINDINGS:
                errors.append(f"protected-with-binding:{sorted(names & PROTECTED_BINDINGS)}:{node.lineno}")
        elif isinstance(node, ast.ExceptHandler) and node.name in PROTECTED_BINDINGS:
            errors.append(f"protected-except-binding:{node.name}:{node.lineno}")
        elif isinstance(node, ast.Match):
            names = set().union(*(pattern_names(case.pattern) for case in node.cases))
            if names & PROTECTED_BINDINGS:
                errors.append(f"protected-match-binding:{sorted(names & PROTECTED_BINDINGS)}:{node.lineno}")
        elif isinstance(node, ast.Delete):
            names = set().union(*(target_root_names(t) for t in node.targets))
            if names & PROTECTED_BINDINGS:
                errors.append(f"protected-delete:{sorted(names & PROTECTED_BINDINGS)}:{node.lineno}")
        elif isinstance(node, ast.Return) and sensitive_reference(node.value):
            errors.append(f"sensitive-return:{node.lineno}")
        elif isinstance(node, (ast.Yield, ast.YieldFrom)) and sensitive_reference(node.value):
            errors.append(f"sensitive-yield:{node.lineno}")

    for node, owner in owners.items():
        func = node.func
        if not isinstance(func, (ast.Name, ast.Attribute)) and sensitive_reference(func):
            errors.append(f"sensitive-indirect-callee:{owner}:{node.lineno}")
        if any(sensitive_reference(arg) for arg in node.args) or any(
                sensitive_reference(keyword.value) for keyword in node.keywords):
            errors.append(f"sensitive-call-transport:{owner}:{node.lineno}")
        if isinstance(func, ast.Attribute):
            if func.attr in PROCESS_APIS:
                process_counts[owner] = process_counts.get(owner, 0) + 1
                exact_subprocess_run = (func.attr == "run" and owner == "run_process"
                                        and isinstance(func.value, ast.Name)
                                        and func.value.id == "subprocess" and node.args
                                        and isinstance(node.args[0], ast.Name)
                                        and node.args[0].id == "argv")
                if not exact_subprocess_run:
                    errors.append(f"process-api:{owner}:{func.attr}:{node.lineno}")
                for keyword in node.keywords:
                    if keyword.arg in {"shell", "executable"}:
                        if keyword.arg == "executable" or not (
                                isinstance(keyword.value, ast.Constant)
                                and keyword.value.value in (False, None)):
                            errors.append(f"process-shell:{node.lineno}")
            elif func.attr in {"system", "popen"} and isinstance(func.value, ast.Name) \
                    and func.value.id == "os":
                errors.append(f"os-process:{func.attr}:{node.lineno}")
            if func.attr in EXECUTION_APIS:
                errors.append(f"dynamic-execution:{owner}:{func.attr}:{node.lineno}")
            if func.attr in NETWORK_APIS:
                errors.append(f"network-api:{owner}:{func.attr}:{node.lineno}")
            if func.attr in ENVIRONMENT_APIS:
                errors.append(f"environment-api:{owner}:{func.attr}:{node.lineno}")
            if func.attr in LOADER_APIS \
                    and func.attr not in {"spec_from_file_location", "module_from_spec",
                                          "exec_module"}:
                errors.append(f"dynamic-loader-api:{owner}:{func.attr}:{node.lineno}")
            string_replace = (func.attr == "replace" and isinstance(func.value, ast.Call)
                              and isinstance(func.value.func, ast.Name)
                              and func.value.func.id == "str")
            if func.attr in FILESYSTEM_MUTATORS and not string_replace \
                    and not (owner == "atomic_json_last_collect" and candidate_builder_role):
                errors.append(f"filesystem-mutation:{owner}:{func.attr}:{node.lineno}")
        elif isinstance(func, ast.Name):
            if func.id in {"getattr", "setattr", "delattr", "globals", "locals", "vars"}:
                errors.append(f"dynamic-namespace-access:{owner}:{func.id}:{node.lineno}")
            if func.id in {"Popen", "call", "check_call", "check_output"}:
                errors.append(f"bare-process:{func.id}:{node.lineno}")
            if func.id == "run_process":
                run_process_counts[owner] = run_process_counts.get(owner, 0) + 1
                good_git_argv = (owner == "git" and node.args
                    and isinstance(node.args[0], ast.List) and len(node.args[0].elts) == 2
                    and isinstance(node.args[0].elts[0], ast.Constant)
                    and node.args[0].elts[0].value == "git"
                    and isinstance(node.args[0].elts[1], ast.Starred)
                    and isinstance(node.args[0].elts[1].value, ast.Name)
                    and node.args[0].elts[1].value.id == "args")
                if not good_git_argv:
                    errors.append(f"run-process-not-git-wrapper:{owner}:{node.lineno}")
            if func.id == "git" and owner != "git":
                command = node.args[0].value if node.args and isinstance(node.args[0], ast.Constant) else None
                if command not in READ_ONLY_GIT_COMMANDS:
                    errors.append(f"git-command-not-read-only:{owner}:{command}:{node.lineno}")
                dangerous = {"-d", "-D", "-m", "-M", "-c", "--delete", "--move",
                             "--output", "--exec", "--upload-pack", "--receive-pack",
                             "--config-env", "--force", "--mirror"}
                static_tokens: list[str] = []
                unsupported_dynamic = False
                for arg in node.args[1:]:
                    if isinstance(arg, ast.Starred):
                        value = static_value(arg.value)
                        if isinstance(value, (list, tuple)):
                            static_tokens.extend(str(item) for item in value)
                        elif not (command == "diff" and isinstance(arg.value, ast.Name)
                                  and arg.value.id == "CONTROL_PATHS"):
                            unsupported_dynamic = True
                    else:
                        value = static_value(arg)
                        if isinstance(value, str):
                            static_tokens.append(value)
                        elif isinstance(arg, ast.Name) and arg.id in SAFE_GIT_DYNAMIC_NAMES:
                            pass
                        elif isinstance(arg, ast.JoinedStr) \
                                and ast.unparse(arg) in SAFE_GIT_JOINED_STRINGS:
                            pass
                        else:
                            unsupported_dynamic = True
                if any(token in dangerous or token.startswith("--output=")
                       for token in static_tokens):
                    errors.append(f"git-mutating-option:{owner}:{node.lineno}")
                allowed_options = ALLOWED_GIT_OPTIONS.get(command, set())
                if any((token.startswith("-") and token not in allowed_options)
                       or token.startswith("ext::") for token in static_tokens):
                    errors.append(f"git-option-or-protocol-not-allowlisted:{owner}:{node.lineno}")
                if unsupported_dynamic:
                    errors.append(f"git-dynamic-option:{owner}:{node.lineno}")
                if command == "branch" and not (
                        len(node.args) == 2 and isinstance(node.args[1], ast.Constant)
                        and node.args[1].value == "--show-current" and not node.keywords):
                    errors.append(f"git-branch-not-query:{owner}:{node.lineno}")
                if command == "ls-remote" and not (
                        len(node.args) == 4
                        and isinstance(node.args[1], ast.Constant)
                        and node.args[1].value == "--heads"
                        and isinstance(node.args[2], ast.Constant)
                        and node.args[2].value == "origin"
                        and ((isinstance(node.args[3], ast.Constant)
                              and node.args[3].value == "refs/heads/main")
                             or (isinstance(node.args[3], ast.JoinedStr)
                                 and ast.unparse(node.args[3]) in {
                                     "f'refs/heads/{PROTECTED_BRANCH}'",
                                     "f'refs/heads/{BRANCH}'",
                                 }))
                        and not node.keywords):
                    errors.append(f"git-ls-remote-not-pinned-origin:{owner}:{node.lineno}")
            if func.id == "open":
                modes = [a.value for a in node.args[1:2] if isinstance(a, ast.Constant)]
                modes += [k.value.value for k in node.keywords
                          if k.arg == "mode" and isinstance(k.value, ast.Constant)]
                if (not modes or any(any(ch in str(mode) for ch in "wax+") for mode in modes)) \
                        and owner != "atomic_json_last_collect":
                    errors.append(f"write-open:{owner}:{node.lineno}")
            if func.id in FILESYSTEM_MUTATORS \
                    and not (owner == "atomic_json_last_collect" and candidate_builder_role):
                errors.append(f"bare-filesystem-mutation:{owner}:{func.id}:{node.lineno}")
            if func.id == "getattr" and len(node.args) >= 2 \
                    and isinstance(node.args[1], ast.Constant) \
                    and node.args[1].value in PROCESS_APIS | FILESYSTEM_MUTATORS:
                errors.append(f"dynamic-sensitive-access:{node.lineno}")
            if func.id in EXECUTION_APIS:
                errors.append(f"dynamic-execution:{owner}:{func.id}:{node.lineno}")

        if isinstance(func, ast.Attribute) and func.attr == "spec_from_file_location":
            exact = (owner == "check_determinism" and len(node.args) >= 2
                     and isinstance(func.value, ast.Attribute) and func.value.attr == "util"
                     and isinstance(func.value.value, ast.Name) and func.value.value.id == "importlib"
                     and isinstance(node.args[0], ast.Constant)
                     and node.args[0].value == "phase065_step72_builder"
                     and isinstance(node.args[1], ast.Name) and node.args[1].id == "BUILDER")
            if not exact:
                errors.append(f"loader-target:{owner}:{node.lineno}")
        if isinstance(func, ast.Attribute) and func.attr == "module_from_spec" \
                and not (owner == "check_determinism" and len(node.args) == 1
                         and isinstance(func.value, ast.Attribute) and func.value.attr == "util"
                         and isinstance(func.value.value, ast.Name) and func.value.value.id == "importlib"
                         and isinstance(node.args[0], ast.Name) and node.args[0].id == "spec"):
            errors.append(f"loader-module:{owner}:{node.lineno}")
        if isinstance(func, ast.Attribute) and func.attr == "exec_module":
            exact = (owner == "check_determinism" and len(node.args) == 1
                     and isinstance(node.args[0], ast.Name) and node.args[0].id == "module"
                     and isinstance(func.value, ast.Attribute) and func.value.attr == "loader"
                     and isinstance(func.value.value, ast.Name) and func.value.value.id == "spec")
            if not exact:
                errors.append(f"loader-exec:{owner}:{node.lineno}")

    if require_contract:
        if subprocess_imports != 1:
            errors.append(f"subprocess-import-count:{subprocess_imports}")
        if definitions.get("run_process") != 1 or definitions.get("git") != 1:
            errors.append("wrapper-definition-count")
        if process_counts != {"run_process": 1}:
            errors.append(f"process-call-map:{process_counts}")
        if run_process_counts != {"git": 1}:
            errors.append(f"wrapper-call-map:{run_process_counts}")
        run_defs = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "run_process"]
        if len(run_defs) == 1:
            if any(name == "argv" for name, _ in binding_events(run_defs[0])):
                errors.append("run-process-argv-rebind")
            if any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                   and isinstance(node.func.value, ast.Name) and node.func.value.id == "argv"
                   and node.func.attr in {"append", "clear", "extend", "insert", "pop", "remove",
                                          "reverse", "sort", "__setitem__", "__delitem__"}
                   for node in ast.walk(run_defs[0])):
                errors.append("run-process-argv-mutation")
            if ast_unparse_sha(run_defs[0]) not in EXPECTED_WRAPPER_AST_SHA256["run_process"]:
                errors.append("run-process-ast-contract")
        git_defs = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "git"]
        if len(git_defs) == 1:
            if any(name == "args" for name, _ in binding_events(git_defs[0])):
                errors.append("git-args-rebind")
            if ast_unparse_sha(git_defs[0]) not in EXPECTED_WRAPPER_AST_SHA256["git"]:
                errors.append("git-ast-contract")
        builder_assignments = [node for node in tree.body if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "BUILDER" for target in node.targets)]
        if len(builder_assignments) > 1:
            errors.append("builder-binding-count")
        elif len(builder_assignments) == 1:
            value = builder_assignments[0].value
            if not (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
                    and value.func.id == "Path" and len(value.args) == 1
                    and isinstance(value.args[0], ast.Constant)
                    and value.args[0].value == "Codex/work/v1024_phase065/build_phase065_step72.py"):
                errors.append("builder-binding-target")
        loader_defs = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                       and node.name == "check_determinism"]
        if loader_defs:
            if len(loader_defs) != 1:
                errors.append("loader-definition-count")
            else:
                calls = [node for node in ast.walk(loader_defs[0]) if isinstance(node, ast.Call)]
                spec_calls = [node for node in calls if isinstance(node.func, ast.Attribute)
                              and node.func.attr == "spec_from_file_location"]
                module_calls = [node for node in calls if isinstance(node.func, ast.Attribute)
                                and node.func.attr == "module_from_spec"]
                exec_calls = [node for node in calls if isinstance(node.func, ast.Attribute)
                              and node.func.attr == "exec_module"]
                if len(spec_calls) != 1 or len(module_calls) != 1 or len(exec_calls) != 1:
                    errors.append("loader-call-count")
                else:
                    spec_call, module_call, exec_call = spec_calls[0], module_calls[0], exec_calls[0]
                    spec_targets = [node for node in ast.walk(loader_defs[0])
                                    if isinstance(node, ast.Assign) and node.value is spec_call]
                    module_targets = [node for node in ast.walk(loader_defs[0])
                                      if isinstance(node, ast.Assign) and node.value is module_call]
                    if not (len(spec_targets) == 1 and target_names(spec_targets[0].targets[0]) == {"spec"}):
                        errors.append("loader-spec-binding")
                    if not (len(module_targets) == 1 and target_names(module_targets[0].targets[0]) == {"module"}):
                        errors.append("loader-module-binding")
                    if not (spec_call.lineno < module_call.lineno < exec_call.lineno):
                        errors.append("loader-order")
                    assigned_names = [name for name, _ in binding_events(loader_defs[0])]
                    if assigned_names.count("spec") != 1 or assigned_names.count("module") != 1:
                        errors.append("loader-role-rebind")
                if ast_unparse_sha(loader_defs[0]) != EXPECTED_LOADER_AST_SHA256:
                    errors.append("loader-ast-contract")
        is_builder = {"build", "guard_output", "atomic_json_last_collect", "main"} <= set(definitions) \
            and "check_determinism" not in definitions
        is_validator = {"check_content", "check_determinism", "git_controls", "main"} <= set(definitions) \
            and "build" not in definitions
        if is_builder == is_validator:
            errors.append("source-role-contract")
        if is_validator and len(builder_assignments) != 1:
            errors.append("validator-builder-binding-count")
        if is_builder and builder_assignments:
            errors.append("builder-unexpected-builder-binding")
        if is_builder:
            collectors = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                          and node.name == "atomic_json_last_collect"]
            if len(collectors) != 1:
                errors.append("atomic-collector-definition-count")
            elif ast_unparse_sha(collectors[0]) != EXPECTED_ATOMIC_COLLECTOR_AST_SHA256:
                errors.append("atomic-collector-ast-contract")
            if ast_unparse_sha(tree) != EXPECTED_BUILDER_AST_SHA256:
                errors.append("builder-whole-ast-contract")
        expected_imports = None
        if is_builder:
            expected_imports = [
                "from __future__ import annotations", "import argparse", "import copy",
                "import hashlib", "import json", "import math", "import os",
                "from pathlib import Path", "import re", "import subprocess", "import tempfile",
            ]
        elif is_validator:
            expected_imports = [
                "from __future__ import annotations", "import argparse", "import ast",
                "import copy", "import hashlib", "import importlib.util", "import json",
                "import math", "import os", "from pathlib import Path", "import re",
                "import subprocess", "import sys",
            ]
        if expected_imports is not None:
            actual_imports = [ast.unparse(node) for node in tree.body
                              if isinstance(node, (ast.Import, ast.ImportFrom))]
            if actual_imports != expected_imports:
                errors.append("module-import-contract")
    return errors


def validate_source_policy(obj: dict) -> int:
    expected_rules = [
        "Read immutable Git blobs at the pinned baseline and expected parent.",
        "Never import or execute frozen Python sources.",
        "Never write Claude/**.",
        "Do not back-import v1.0.25 skew behavior into v1.0.24.",
        "Bibliographic identity does not prove proposition, page, or equation support.",
        "Unavailable primary text remains GROUND_NOT_FOUND with an acquisition owner.",
        "Generate the machine JSON after the human result and controls are staged.",
    ]
    policy = obj["source_policy"]
    assert_equal(policy["rules"], expected_rules, "E_SOURCE_POLICY_RULES")
    assert_equal(policy["network_used_by_builder"], False, "E_SOURCE_POLICY_NETWORK")
    assert_equal(policy["child_process_allowlist"], ["git"], "E_SOURCE_POLICY_CHILD")
    assert_equal(policy["frozen_source_execution"], False, "E_SOURCE_POLICY_EXECUTION")
    assert_equal(policy["claude_tree_written"], False, "E_SOURCE_POLICY_CLAUDE")

    checked_paths = [str(BUILDER),
                     str(Path("Codex/work/v1024_phase065/validate_phase065_step72.py"))]
    for path_text in checked_paths:
        source = Path(path_text).read_text(encoding="utf-8")
        errors = source_policy_errors(source, require_contract=True)
        if errors:
            fail("E_SOURCE_POLICY_STATIC", f"{path_text}:{errors}")
        if path_text == str(BUILDER):
            for token in ("guard_output(args.output)", "result document must be staged",
                          "explicit output must remain below the system temporary directory"):
                if token not in source: fail("E_SOURCE_POLICY_OUTPUT_GUARD", token)

    negative_sources = {
        "direct-run": "import subprocess\ndef x(): subprocess.run(['git','status'])\n",
        "alias": "import subprocess\ndef x():\n r=subprocess.run\n r(['git','status'])\n",
        "getattr-run": "import subprocess\ndef x(): getattr(subprocess,'run')(['git'])\n",
        "popen": "import subprocess\ndef x(): subprocess.Popen(['git'])\n",
        "os-system": "import subprocess, os\ndef x(): os.system('git status')\n",
        "wrapper-owner": "import subprocess\ndef x(): run_process(['git','status'])\n",
        "wrapper-command": "import subprocess\ndef git(): run_process(['python','x.py'])\n",
        "path-write": "import subprocess\nfrom pathlib import Path\ndef x(): Path('x').write_text('x')\n",
        "replace": "import subprocess, os\ndef x(): os.replace('a','b')\n",
        "write-open": "import subprocess\ndef x(): open('x','w')\n",
        "protected-rebind": "import subprocess\nrun_process = subprocess.run\n",
        "protected-delete": "import subprocess\ndef x():\n global git\n del git\n",
        "subprocess-alias": "import subprocess as sp\ndef x(): sp.run(['git'])\n",
        "subprocess-from": "from subprocess import run\ndef x(): run(['git'])\n",
        "container-alias": "import subprocess\nbox=(subprocess.run,)\ndef x(): box[0](['git'])\n",
        "default-alias": "import subprocess\ndef x(cb=subprocess.run): cb(['git'])\n",
        "callback-alias": "import subprocess\ndef f(**kw): pass\nf(callback=subprocess.run)\n",
        "sys-modules": "import subprocess, sys\ndef x(): sys.modules['subprocess'].run(['git'])\n",
        "vars-modules": "import subprocess, sys\ndef x(): vars(sys)['modules']['subprocess'].run(['git'])\n",
        "dynamic-path-open": "import subprocess\nfrom pathlib import Path\ndef x(mode): Path('x').open(mode)\n",
        "io-open": "import subprocess, io\ndef x(): io.open('x','w')\n",
        "redirected-loader": "import subprocess, importlib.util\ndef x(): importlib.util.spec_from_file_location('x','Claude/evil.py')\n",
        "exec-builtin": "import subprocess\ndef x(s): exec(s)\n",
        "dunder-import": "import subprocess\ndef x(): __import__('subprocess').run(['git'])\n",
        "import-module": "import subprocess, importlib\ndef x(): importlib.import_module('subprocess').run(['git'])\n",
        "loader-exec": "import subprocess\ndef x(spec,module): spec.loader.exec_module(module)\n",
        "wrapper-python-payload": "import subprocess\ndef run_process(argv): return subprocess.run(['python','evil.py'])\ndef git(*args): return run_process(['git',*args])\n",
        "wrapper-git-push": "import subprocess\ndef run_process(argv): return subprocess.run(argv)\ndef git(*args): return run_process(['git','push','origin','HEAD'])\n",
        "git-mutation": "import subprocess\ndef x(): git('push','origin','HEAD')\n",
        "builder-local-rebind": "import subprocess\ndef check_determinism():\n BUILDER=Path('Claude/evil.py')\n importlib.util.spec_from_file_location('phase065_step72_builder',BUILDER)\n",
        "broken-loader-chain": "import subprocess\ndef check_determinism():\n spec=importlib.util.spec_from_file_location('phase065_step72_builder',BUILDER)\n module=importlib.util.module_from_spec(object())\n evil.exec_module(module)\n",
        "subprocess-dict-run": "import subprocess\ndef x(): subprocess.__dict__['run'](['git'])\n",
        "subprocess-dict-popen": "import subprocess\ndef x(): subprocess.__dict__['Popen'](['python','evil.py'])\n",
        "constructed-getattr-write": "import subprocess\nfrom pathlib import Path\ndef x(): getattr(Path('x'),'write_'+'text')('x')\n",
        "globals-builder-rebind": "import subprocess\ndef x(): globals().__setitem__('BUILDER','Claude/evil.py')\n",
        "importlib-dict-rebind": "import subprocess, importlib.util\ndef x(): importlib.util.__dict__.__setitem__('spec_from_file_location',lambda *a:None)\n",
        "return-process-callable": "import subprocess\ndef x(): return subprocess.run\n",
        "annotation-process-callable": "import subprocess\ndef x(cb: subprocess.run): return cb\n",
        "return-filesystem-callable": "import subprocess\nfrom pathlib import Path\ndef x(): return Path.write_text\n",
        "yield-process-callable": "import subprocess\ndef x(): yield subprocess.run\n",
        "for-process-callable": "import subprocess\ndef x():\n for cb in (subprocess.run,): cb(['git'])\n",
        "match-process-callable": "import subprocess\ndef x():\n match subprocess.run:\n  case cb: return cb\n",
        "class-base-process": "import subprocess\nclass X(subprocess.run): pass\n",
        "class-decorator-process": "import subprocess\n@subprocess.run\nclass X: pass\n",
        "augassign-process": "import subprocess\nx=[]\nx += [subprocess.run]\n",
        "subprocess-dunder-run": "import subprocess\ndef x(): subprocess.__getattribute__('run')(['git'])\n",
        "path-dunder-write": "import subprocess\nfrom pathlib import Path\ndef x(): Path('x').__getattribute__('write_text')('x')\n",
        "builtins-dunder-import": "import subprocess, builtins\ndef x(): builtins.__getattribute__('__import__')('os').__getattribute__('system')('x')\n",
        "indirect-container-call": "import subprocess\ndef x(): (subprocess.run,)[0](['git'])\n",
        "conditional-popen": "import subprocess\ndef x(flag): (subprocess.Popen if flag else print)(['git'])\n",
        "dynamic-branch-option": "import subprocess\ndef x(flag): git('branch',flag,'main')\n",
        "branch-create": "import subprocess\ndef x(): git('branch','new-name')\n",
        "branch-starred-delete": "import subprocess\ndef x(): git('branch',*['-'+'D','main'])\n",
        "constructed-show-output": "import subprocess\ndef x(): git('show','--out'+'put=Claude/evil','HEAD')\n",
        "conditional-write": "import subprocess\nfrom pathlib import Path\ndef x(flag): (Path('x').write_text if flag else print)('x')\n",
        "path-chmod": "import subprocess\nfrom pathlib import Path\ndef x(): Path('x').chmod(511)\n",
        "loader-container-call": "import subprocess, importlib.util\ndef x(): (importlib.util.spec_from_file_location,) [0]('x','y')\n",
        "os-module-alias-system": "import subprocess, os as safe\ndef x(): safe.system('x')\n",
        "os-from-system": "import subprocess\nfrom os import system\ndef x(): system('x')\n",
        "os-from-popen-alias": "import subprocess\nfrom os import popen as p\ndef x(): p('x')\n",
        "asyncio-subprocess": "import subprocess, asyncio\ndef x(): asyncio.create_subprocess_exec('x')\n",
        "os-posix-spawn": "import subprocess, os\ndef x(): os.posix_spawn('x',['x'],{})\n",
        "os-from-remove-alias": "import subprocess\nfrom os import remove as clean\ndef x(): clean('x')\n",
        "builtins-from-open-alias": "import subprocess\nfrom builtins import open as reader\ndef x(): reader('x','w')\n",
        "protected-class-definition": "import subprocess\nclass subprocess: pass\n",
        "protected-function-definition": "import subprocess\ndef subprocess(): pass\n",
        "protected-import-alias": "import subprocess\nimport os as subprocess\n",
        "dynamic-show-option": "import subprocess\ndef x(flag): git('show',flag,'HEAD')\n",
        "subprocess-getoutput": "import subprocess\ndef x(): subprocess.getoutput('x')\n",
        "subprocess-getstatusoutput": "import subprocess\ndef x(): subprocess.getstatusoutput('x')\n",
        "protected-vararg": "import subprocess\ndef x(*subprocess): return subprocess\n",
        "protected-lambda-argument": "import subprocess\nx=lambda subprocess: subprocess\n",
        "protected-except-binding": "import subprocess\ntry: pass\nexcept Exception as subprocess: pass\n",
        "unexpected-import-root": "import subprocess, operator\ndef x(): operator.attrgetter('system')\n",
        "os-execl": "import subprocess, os\ndef x(): os.execl('x','x')\n",
        "path-move-into": "import subprocess\nfrom pathlib import Path\ndef x(): Path('x').move_into('Claude')\n",
        "path-copy-into": "import subprocess\nfrom pathlib import Path\ndef x(): Path('x').copy_into('Claude')\n",
        "os-mknod": "import subprocess, os\ndef x(): os.mknod('Claude/x')\n",
        "source-file-loader": "import subprocess, importlib.machinery\ndef x(): importlib.machinery.SourceFileLoader('x','Claude/evil.py').load_module()\n",
        "git-ext-diff": "import subprocess\ndef x(): git('diff','--ext-diff','HEAD^','HEAD')\n",
        "git-ext-protocol": "import subprocess\ndef x(): git('ls-remote','ext::helper')\n",
        "git-upload-pack-value": "import subprocess\ndef x(): git('ls-remote','--upload-pack=helper','origin')\n",
        "dynamic-network-loader": "import subprocess, importlib.util\ndef x(): importlib.util.find_spec('socket').loader.load_module('socket').create_connection(('example.com',80))\n",
        "git-ls-remote-ssh": "import subprocess\ndef x(): git('ls-remote','ssh://example/x')\n",
        "git-ls-remote-git": "import subprocess\ndef x(): git('ls-remote','git://example/x')\n",
        "git-helper-environment": "import subprocess, os\nos.environ['GIT_EXTERNAL_DIFF']='helper'\ndef x(): git('diff','HEAD^','HEAD')\n",
        "path-hardlink-to": "import subprocess\nfrom pathlib import Path\ndef x(): Path('Claude/new').hardlink_to('source')\n",
        "tempfile-mkdtemp": "import subprocess, tempfile\ndef x(): tempfile.mkdtemp(dir='Claude')\n",
        "tempfile-directory": "import subprocess, tempfile\ndef x(): tempfile.TemporaryDirectory(dir='Claude')\n",
        "os-utime": "import subprocess, os\ndef x(): os.utime('Claude/x')\n",
        "os-setxattr": "import subprocess, os\ndef x(): os.setxattr('Claude/x','a',b'b')\n",
        "os-removexattr": "import subprocess, os\ndef x(): os.removexattr('Claude/x','a')\n",
        "os-putenv": "import subprocess, os\ndef x(): os.putenv('GIT_EXTERNAL_DIFF','helper')\n",
        "git-helper-environment-bytes": "import subprocess, os\nos.environb[b'GIT_EXTERNAL_DIFF']=b'helper'\ndef x(): git('diff','HEAD^','HEAD')\n",
        "os-chdir": "import subprocess, os\ndef x(): os.chdir('other-tree')\n",
        "os-fchdir": "import subprocess, os\ndef x(fd): os.fchdir(fd)\n",
        "os-chroot": "import subprocess, os\ndef x(): os.chroot('other-tree')\n",
        "os-umask": "import subprocess, os\ndef x(): os.umask(0)\n",
    }
    rejected = {name for name, source in negative_sources.items()
                if source_policy_errors(source, require_contract=False)}
    assert_equal(rejected, set(negative_sources), "E_SOURCE_POLICY_NEGATIVE_PROBES")
    contract_negative_sources = {
        "mutable-run-argv": "import subprocess\ndef run_process(argv):\n argv.clear(); argv.extend(['python','evil.py']); return subprocess.run(argv)\ndef git(*args): return run_process(['git',*args])\n",
        "mutable-git-args": "import subprocess\ndef run_process(argv): return subprocess.run(argv)\ndef git(*args):\n args=('push','origin','HEAD'); return run_process(['git',*args])\n",
        "branch-delete": "import subprocess\ndef run_process(argv): return subprocess.run(argv)\ndef git(*args): return run_process(['git',*args])\ndef x(): git('branch','-D','main')\n",
        "show-output": "import subprocess\ndef run_process(argv): return subprocess.run(argv)\ndef git(*args): return run_process(['git',*args])\ndef x(): git('show','--output=Claude/evil','HEAD')\n",
        "evil-loader-receiver": "import subprocess\ndef check_determinism():\n spec=evil.spec_from_file_location('phase065_step72_builder',BUILDER)\n module=evil.module_from_spec(spec)\n spec.loader.exec_module(module)\n",
        "loader-role-rebind": "import subprocess\ndef check_determinism():\n spec=importlib.util.spec_from_file_location('phase065_step72_builder',BUILDER)\n spec=evil_spec\n module=importlib.util.module_from_spec(spec)\n spec.loader.exec_module(module)\n",
        "missing-source-role": "import subprocess\ndef run_process(argv): return subprocess.run(argv)\ndef git(*args): return run_process(['git',*args])\n",
        "argv-index-mutation": "import subprocess\ndef run_process(argv):\n argv[0]='python'; return subprocess.run(argv)\ndef git(*args): return run_process(['git',*args])\n",
        "argv-slice-mutation": "import subprocess\ndef run_process(argv):\n argv[:]=['python']; return subprocess.run(argv)\ndef git(*args): return run_process(['git',*args])\n",
        "git-args-augassign": "import subprocess\ndef run_process(argv): return subprocess.run(argv)\ndef git(*args):\n args += ('push',); return run_process(['git',*args])\n",
        "protected-for-binding": "import subprocess\ndef run_process(argv):\n for subprocess in [evil]: return subprocess.run(argv)\ndef git(*args): return run_process(['git',*args])\n",
        "git-for-binding": "import subprocess\ndef run_process(argv): return subprocess.run(argv)\ndef git(*args):\n for args in [('push','origin','HEAD')]: return run_process(['git',*args])\n",
        "protected-with-binding": "import subprocess\ndef run_process(argv):\n with evil as argv: return subprocess.run(argv)\ndef git(*args): return run_process(['git',*args])\n",
        "loader-loop-rebind": "import subprocess\ndef check_determinism():\n spec=importlib.util.spec_from_file_location('phase065_step72_builder',BUILDER)\n for spec in [evil_spec]: pass\n module=importlib.util.module_from_spec(spec)\n spec.loader.exec_module(module)\n",
        "loader-member-rebind": "import subprocess\ndef check_determinism():\n spec=importlib.util.spec_from_file_location('phase065_step72_builder',BUILDER)\n spec.loader=evil\n module=importlib.util.module_from_spec(spec)\n spec.loader.exec_module(module)\n",
        "loader-branch-order": "import subprocess\ndef check_determinism(flag):\n if flag:\n  spec=importlib.util.spec_from_file_location('phase065_step72_builder',BUILDER)\n else:\n  module=importlib.util.module_from_spec(spec)\n spec.loader.exec_module(module)\n",
        "builder-augassign": "import subprocess\nBUILDER=Path('Codex/work/v1024_phase065/build_phase065_step72.py')\nBUILDER /= 'evil'\n",
    }
    contract_rejected = {name for name, source in contract_negative_sources.items()
                         if source_policy_errors(source, require_contract=True)}
    assert_equal(contract_rejected, set(contract_negative_sources),
                 "E_SOURCE_POLICY_CONTRACT_NEGATIVE_PROBES")
    builder_source = BUILDER.read_text(encoding="utf-8")
    validator_source = Path(
        "Codex/work/v1024_phase065/validate_phase065_step72.py"
    ).read_text(encoding="utf-8")

    def mutate_once(source: str, old: str, new: str) -> str:
        before, separator, after = source.partition(old)
        if not separator:
            fail("E_SOURCE_POLICY_FULL_SOURCE_ANCHOR", old)
        return before + new + after

    full_source_negative_sources = {
        "builder-duplicate-atomic-owner": mutate_once(builder_source,
            "\ndef build() -> dict:\n",
            "\ndef atomic_json_last_collect(*args, **kwargs):\n"
            "    Path('Claude/evil').write_text('x')\n\ndef build() -> dict:\n"),
        "builder-atomic-arbitrary-write": mutate_once(builder_source,
            "def atomic_json_last_collect(output: Path, obj: dict) -> None:\n",
            "def atomic_json_last_collect(output: Path, obj: dict) -> None:\n"
            "    Path('Claude/evil').write_text('x')\n"),
        "builder-added-chmod": mutate_once(builder_source,
            "\ndef main() -> int:\n",
            "\ndef injected():\n    Path('Claude/evil').chmod(511)\n\ndef main() -> int:\n"),
        "builder-result-first-guard-removed": mutate_once(builder_source,
            "    args = ap.parse_args(); guard_output(args.output); obj = build()\n",
            "    args = ap.parse_args(); obj = build()\n"),
        "builder-result-staged-check-removed": mutate_once(builder_source,
            "        if result_path not in staged:\n"
            "            raise SystemExit(\"result document must be staged before JSON-last collection\")\n",
            ""),
        "builder-json-last-reordered": mutate_once(builder_source,
            "    args = ap.parse_args(); guard_output(args.output); obj = build()\n",
            "    args = ap.parse_args(); obj = build(); guard_output(args.output)\n"),
        "validator-missing-builder-binding": mutate_once(validator_source,
            "BUILDER = Path(\"Codex/work/v1024_phase065/build_phase065_step72.py\")\n",
            ""),
        "validator-loader-member-rebind": mutate_once(validator_source,
            "    module = importlib.util.module_from_spec(spec)\n",
            "    spec.loader = object()\n"
            "    module = importlib.util.module_from_spec(spec)\n"),
        "validator-dynamic-branch": mutate_once(validator_source,
            "git(\"branch\", \"--show-current\")",
            "git(\"branch\", branch_option, \"main\")"),
        "validator-added-import": mutate_once(validator_source,
            "import sys\n", "import sys\nimport builtins\n"),
        "validator-duplicate-atomic-owner": mutate_once(validator_source,
            "\nif __name__ == \"__main__\":\n",
            "\ndef atomic_json_last_collect():\n"
            "    Path('Claude/evil').write_text('x')\n"
            "\nif __name__ == \"__main__\":\n"),
    }
    for name, mutated in full_source_negative_sources.items():
        baseline = builder_source if name.startswith("builder-") else validator_source
        if mutated == baseline:
            fail("E_SOURCE_POLICY_FULL_SOURCE_FIXTURE", name)
        if not source_policy_errors(mutated, require_contract=True):
            fail("E_SOURCE_POLICY_FULL_SOURCE_NEGATIVE", name)
    return (len(negative_sources) + len(contract_negative_sources)
            + len(full_source_negative_sources))


def validate_header_contract(obj: dict, *, semantic: bool = True) -> None:
    expected_top = {
        "schema_version", "generated_date", "artifact_kind", "baseline_commit",
        "expected_parent", "branch", "gate", "authority", "source_policy",
        "control_source_bindings", "source_bindings", "tex_census", "non_graft", "bibliographic_conflicts",
        "genealogy", "derivations", "material_claims", "metadata_verifications",
        "findings", "input_routes", "consumed_parent_evidence", "next_gate",
        "semantic_sha256",
    }
    assert_equal(set(obj), expected_top, "E_TOP_LEVEL_SCHEMA")
    assert_equal(obj.get("schema_version"), "phase065-step72-v1", "E_SCHEMA")
    assert_equal(obj.get("generated_date"), "2026-08-31", "E_GENERATED_DATE")
    assert_equal(obj.get("artifact_kind"), "skew-material-authority-matrix", "E_ARTIFACT_KIND")
    assert_equal(obj.get("baseline_commit"), BASELINE, "E_BASELINE")
    assert_equal(obj.get("expected_parent"), EXPECTED_PARENT, "E_PARENT")
    assert_equal(obj.get("branch"), BRANCH, "E_ARTIFACT_BRANCH")
    assert_equal(obj.get("gate"), PASS_CONTENT, "E_GATE")
    if semantic:
        assert_equal(obj.get("semantic_sha256"), canonical_semantic(obj), "E_SEMANTIC_SHA")
    consumed = obj.get("consumed_parent_evidence", {})
    assert_equal(consumed.get("step70_content_gate"), "PASS_P065_STEP70_PRECOMMIT",
                 "E_STEP70_GATE")
    assert_equal(consumed.get("step70_persistence_terminal"), "PASS_P065_STEP70_PERSISTENCE",
                 "E_STEP70_PERSISTENCE")
    assert_equal(consumed.get("step70_commit"),
                 "d6f680b26fb59c24098f44ed633873a2c6419a4e", "E_STEP70_COMMIT")
    assert_equal(consumed.get("step71_gate"), "PASS_P065_STEP71_STATIC_WITH_CONCERNS",
                 "E_STEP71_GATE")
    assert_equal(consumed.get("step71_persistence_terminal"), "PASS_P065_STEP71_PERSISTENCE",
                 "E_STEP71_PERSISTENCE")
    assert_equal(consumed.get("step71_commit"), EXPECTED_PARENT, "E_STEP71_COMMIT")
    assert_equal(consumed.get("step70_findings_routed"), 26, "E_STEP70_ROUTE_COUNT")
    assert_equal(consumed.get("step71_findings_routed"), 13, "E_STEP71_ROUTE_COUNT")
    assert_equal(consumed.get("total_routes"), 39, "E_TOTAL_ROUTE_COUNT")


def recursive_stats(value, depth: int = 0) -> tuple[int, int]:
    if isinstance(value, float) and not math.isfinite(value):
        fail("E_RECURSIVE_NONFINITE")
    nodes = 1
    max_depth = depth
    children = value.values() if isinstance(value, dict) else value if isinstance(value, list) else []
    for child in children:
        child_nodes, child_depth = recursive_stats(child, depth + 1)
        nodes += child_nodes
        max_depth = max(max_depth, child_depth)
    return nodes, max_depth


def validate_non_graft_contract(obj: dict) -> None:
    non_graft = obj["non_graft"]
    assert_equal(non_graft["undefined_keys"], ["fergusonbazant2014", "guo2016"],
                 "E_NON_GRAFT_KEYS")
    assert_equal(non_graft["candidate"],
                 "Claude/docs/v1.0.24/results/comp_R1/W1/gr_2L.tex", "E_NON_GRAFT_PATH")
    assert_equal(non_graft["decision"], "REJECTED_SOURCE_NOT_GRAFTED",
                 "E_NON_GRAFT_DECISION")
    assert_equal(non_graft["replacement_existing_key"], "persson2010b",
                 "E_NON_GRAFT_REPLACEMENT")


def validate_conflict_contract(obj: dict) -> None:
    conflicts = {row["id"]: row for row in obj["bibliographic_conflicts"]}
    assert_equal(sorted(conflicts), ["B72-C01", "B72-C02"], "E_BIB_CONFLICT_IDS")
    assert_equal(conflicts["B72-C01"]["status"],
                 "INTERNAL_BIBLIOGRAPHIC_IDENTITY_CONFLICT", "E_BIB_TITLE_CONFLICT")
    assert_equal(conflicts["B72-C02"]["adopted_value"], "050539", "E_BIB_ADOPTED_NUMBER")
    assert_equal(conflicts["B72-C02"]["historical_value"], "050520", "E_BIB_HISTORICAL_NUMBER")


def validate_binding_shape(obj: dict) -> None:
    rows = obj["source_bindings"]
    assert_equal(len(rows), 28, "E_BINDING_COUNT")
    paths = []
    for row in rows:
        if set(row) != {"path", "role", "git_blob", "sha256", "lines", "read_status"}:
            fail("E_BINDING_SCHEMA", row.get("path", "?"))
        paths.append(row["path"])
        if not re.fullmatch(r"[0-9a-f]{40}", row["git_blob"]): fail("E_BINDING_BLOB_FORMAT")
        if not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]): fail("E_BINDING_SHA_FORMAT")
        if not isinstance(row["lines"], int) or row["lines"] < 1: fail("E_BINDING_LINES_FORMAT")
        assert_equal(row["read_status"], "READ_FULL", "E_BINDING_READ_STATUS")
    assert_equal(len(paths), len(set(paths)), "E_BINDING_PATH_UNIQUE")


def validate_control_source_bindings(obj: dict) -> None:
    expected = {
        "Codex/work/v1024_phase065/build_phase065_step72.py": "JSON_LAST_BUILDER",
        "Codex/work/v1024_phase065/validate_phase065_step72.py": "INDEPENDENT_VALIDATOR",
        "Codex/results/PHASE_065_STEP_072_SKEW_MATERIAL_AUTHORITY_RESULT.md":
            "RESULT_FIRST_RESULT",
        "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md":
            "PARENT_EXECUTION_LEDGER",
        "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md":
            "CANONICAL_EXECUTION_LEDGER",
        "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md": "ACTIVE_HANDOVER",
    }
    rows = obj["control_source_bindings"]
    assert_equal(len(rows), 6, "E_CONTROL_SOURCE_COUNT")
    by_path = {row["path"]: row for row in rows}
    assert_equal(set(by_path), set(expected), "E_CONTROL_SOURCE_PATHS")
    for path_text, role in expected.items():
        row = by_path[path_text]
        assert_equal(set(row), {"path", "role", "index_blob", "sha256", "size_bytes"},
                     "E_CONTROL_SOURCE_SCHEMA")
        assert_equal(row["role"], role, "E_CONTROL_SOURCE_ROLE")
        raw = Path(path_text).read_bytes()
        index_raw = git("show", f":{path_text}", text=False)
        assert_equal(index_raw, raw, "E_CONTROL_SOURCE_INDEX_WORKTREE")
        assert_equal(row["index_blob"], str(git("rev-parse", f":{path_text}")).strip(),
                     "E_CONTROL_SOURCE_BLOB")
        assert_equal(row["sha256"], sha256(raw), "E_CONTROL_SOURCE_SHA")
        assert_equal(row["size_bytes"], len(raw), "E_CONTROL_SOURCE_SIZE")


def core_invariants(obj: dict) -> int:
    validate_derivations(obj)
    validate_material_claims(obj)
    source_policy_cases = validate_source_policy(obj)
    validate_non_graft_contract(obj)
    validate_conflict_contract(obj)
    validate_binding_shape(obj)
    authority = obj["authority"]
    assert_equal(set(authority), {
        "internal_derivation", "internal_source_genealogy",
        "external_bibliographic_metadata_verified", "controller_metadata_observation_recorded",
        "external_primary_literature_truth", "external_proposition_support", "material_truth",
        "experimental_truth", "runtime_truth", "canonical_manuscript_ready",
        "publication_ready", "v1024_1_independent_corroboration", "ceiling",
    }, "E_AUTHORITY_SCHEMA")
    for key in ("external_bibliographic_metadata_verified", "external_primary_literature_truth",
                "external_proposition_support", "material_truth", "experimental_truth",
                "runtime_truth", "canonical_manuscript_ready", "publication_ready"):
        assert_equal(authority.get(key), False, f"E_AUTHORITY_{key.upper()}")
    assert_equal(authority.get("internal_derivation"), True, "E_AUTHORITY_DERIVATION")
    assert_equal(len(obj["input_routes"]), 39, "E_ROUTE_COUNT")
    ids = [r["route_id"] for r in obj["input_routes"]]
    assert_equal(len(ids), len(set(ids)), "E_ROUTE_UNIQUE")
    expected70 = {f"P065-S70-F{i:02d}" for i in (6,7,8,12,13,14,15,16,17,18,19,20,23,25,27,28,29,30,31,32,33,35,36,38,41,42)}
    expected71 = {f"P065-S71-F{i:02d}" for i in range(1,14)}
    assert_equal(set(ids), expected70 | expected71, "E_ROUTE_IDENTITIES")
    step70_result = load_first_json_fence(
        "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md"
    )
    step70_by_id = {row["id"]: row for row in step70_result["finding_routes"]}
    step71_matrix = strict_json_loads(
        blob("Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json",
             EXPECTED_PARENT).decode("utf-8")
    )
    step71_by_id = {row["finding_id"]: row for row in step71_matrix["findings"]}
    step71_nonruntime_owner = {
        "P065-S71-F12": "P065-STEP75-DISPOSITION",
        "P065-S71-F13": "PHASE-071-PRIMARY-SOURCE-ACQUISITION",
    }
    for row in obj["input_routes"]:
        assert_equal(set(row), {"route_id", "origin_step", "origin_finding",
                                "origin_artifact", "origin_record", "disposition",
                                "owner", "followup_targets", "status"},
                     "E_ROUTE_SCHEMA")
        expected_step = 70 if row["route_id"].startswith("P065-S70-") else 71
        assert_equal(row["origin_step"], expected_step, "E_ROUTE_ORIGIN_STEP")
        assert_equal(row["origin_finding"], row["route_id"].rsplit("-", 1)[1],
                     "E_ROUTE_ORIGIN_FINDING")
        assert_equal(row["disposition"], "PRESERVE_EXACT_ORIGIN_RECORD",
                     "E_ROUTE_DISPOSITION")
        assert_equal(row["status"], "OPEN_CARRIED", "E_ROUTE_STATUS")
        if expected_step == 70:
            origin = step70_by_id[row["route_id"]]
            assert_equal(row["origin_artifact"],
                         "Codex/results/PHASE_065_STEP_070_SOURCE_PROCESS_TOPOLOGY_RESULT.md",
                         "E_ROUTE_ORIGIN_ARTIFACT")
            assert_equal(row["origin_record"], origin, "E_ROUTE_ORIGIN_RECORD")
            assert_equal(row["owner"], origin["owner"], "E_ROUTE_OWNER_EXACT")
            assert_equal(row["followup_targets"], origin["target_steps"],
                         "E_ROUTE_TARGETS_EXACT")
        else:
            origin = step71_by_id[row["route_id"]]
            assert_equal(row["origin_artifact"],
                         "Codex/results/PHASE_065_CODE_PROFILE_DEFAULT_MATRIX.json",
                         "E_ROUTE_ORIGIN_ARTIFACT")
            assert_equal(row["origin_record"], origin, "E_ROUTE_ORIGIN_RECORD")
            expected_owner = step71_nonruntime_owner.get(
                row["route_id"], "P065-STEP73-RUNTIME"
            )
            assert_equal(row["owner"], expected_owner, "E_ROUTE_OWNER_EXACT")
            assert_equal(row["followup_targets"], origin["next_steps"],
                         "E_ROUTE_TARGETS_EXACT")
    genealogy = {r["id"]: r for r in obj["genealogy"]}
    assert_equal(genealogy["G72-01"]["later_state"], "INTRODUCED_IN_V1025", "E_SKEW_FIRST_VERSION")
    assert_equal(genealogy["G72-01"]["first_later_commit"],
                 "edbc4a2c68cda0dd21662cb6dd68ba8bed699a76", "E_SKEW_FIRST_COMMIT")
    assert_equal(genealogy["G72-06"]["v1024_1_state"], "MIRROR_ARCHIVE_ONLY",
                 "E_V1024_1_ARCHIVE_ROLE")
    assert_equal(authority.get("v1024_1_independent_corroboration"), False,
                 "E_V1024_1_CORROBORATION")
    expected_dois = {"10.1149/2754-2734/ad7d1c", "10.1149/1945-7111/ad70d9",
                     "10.1149/1945-7111/ad1d27", "10.1149/1945-7111/ad4823",
                     "10.1016/S1359-6454(02)00514-1", "10.1063/1.4802584",
                     "10.1063/1.4802005"}
    assert_equal({r["doi"] for r in obj["metadata_verifications"]}, expected_dois,
                 "E_METADATA_DOIS")
    assert_equal(len(obj["metadata_verifications"]), len(expected_dois), "E_METADATA_UNIQUE")
    for row in obj["metadata_verifications"]:
        assert_equal(row["artifact_authority"], "UNVERIFIED_EXTERNAL_NO_RAW_RESPONSE",
                     "E_METADATA_AUTHORITY")
    consumed = obj["consumed_parent_evidence"]
    assert_equal(consumed["step70_findings_routed"] + consumed["step71_findings_routed"],
                 consumed["total_routes"], "E_PARENT_ROUTE_SUM")
    findings = obj["findings"]
    assert_equal([row["id"] for row in findings], [f"S72-F{i:02d}" for i in range(1, 7)],
                 "E_FINDING_IDENTITIES")
    allowed_owners = {"P065-STEP74-CONFORMANCE", "P065-STEP73-RUNTIME",
                      "P065-STEP75-DISPOSITION", "P066-LINEAGE",
                      "P071-PRIMARY-SOURCE-ACQUISITION", "P067-CODE-HISTORY",
                      "PHASE-071-PRIMARY-SOURCE-ACQUISITION",
                      "PHASE-072-SCIENTIFIC-REDERIVATION", "PHASE-073-RUNTIME-BOUNDARY",
                      "PHASE-074-DOCUMENT-REPAIR", "PHASE-075-AUTHORITY-DISPOSITION"}
    owners = [row["owner"] for row in findings]
    owners += [row["owner"] for row in obj["input_routes"]]
    owners += [row["owner"] for row in obj["bibliographic_conflicts"]]
    owners += [row["owner"] for row in obj["metadata_verifications"] if "owner" in row]
    if any(owner not in allowed_owners for owner in owners): fail("E_ORPHAN_OWNER")
    return source_policy_cases


def check_content(obj: dict) -> dict:
    validate_header_contract(obj)
    validate_control_source_bindings(obj)
    traversal_nodes, traversal_depth = recursive_stats(obj)
    assert_equal(traversal_nodes, 3436, "E_TRAVERSAL_NODES")
    assert_equal(traversal_depth, 5, "E_TRAVERSAL_DEPTH")
    for key, expected in PROJECTION_SHA256.items():
        assert_equal(projection_sha(obj[key]), expected, f"E_PROJECTION_{key.upper()}")

    topo = load_topology()["tex"]
    paths = list(topo["adopted_closures"]["graphite"]["paths"])
    paths += [p for p in topo["adopted_closures"]["lco"]["paths"] if p not in paths]
    paths += [p for p in topo["adopted_closures"]["si_blend"]["paths"] if p not in paths]
    paths += topo["non_master_paths"]
    memberships: dict[str, list[str]] = {}
    for name, closure in topo["adopted_closures"].items():
        for p in closure["paths"]:
            memberships.setdefault(p, []).append(name)
    rebuilt = census(paths, memberships)
    assert_equal(rebuilt["summary"], obj["tex_census"]["summary"], "E_TEX_CENSUS")
    assert_equal(rebuilt["files"], obj["tex_census"]["files"], "E_TEX_FILES")
    assert_equal(rebuilt["summary"], {
        "files": 90, "bibitem_occurrences": 95, "unique_bibitem_keys": 93,
        "citation_occurrences": 561, "unique_citation_keys": 95,
        "doi_occurrences": 91, "unique_doi_strings": 85,
        "globally_undefined_keys": ["fergusonbazant2014", "guo2016"],
        "globally_unused_bibitem_keys": [],
    }, "E_EXPECTED_CENSUS")

    closures = obj["tex_census"]["closures"]
    expected_closures = {
        "graphite": [34, 44, 44, 138, 44, 37, 36],
        "lco": [13, 15, 15, 77, 15, 16, 16],
        "si_blend": [11, 36, 36, 86, 36, 36, 36],
        "adopted_union": [56, 95, 93, 301, 93, 89, 83],
        "non_master": [34, 0, 0, 260, 41, 2, 2],
    }
    for name, vals in expected_closures.items():
        row = closures[name]
        got = [row[k] for k in ("files", "bibitem_occurrences", "unique_bibitem_keys",
               "citation_occurrences", "unique_citation_keys", "doi_occurrences", "unique_doi_strings")]
        assert_equal(got, vals, f"E_CLOSURE_{name.upper()}")

    source_policy_cases = core_invariants(obj)
    w1 = blob(obj["non_graft"]["candidate"]).decode("utf-8")
    cherry = blob(obj["non_graft"]["decision_source"]).decode("utf-8")
    for token in ("fergusonbazant2014", "guo2016"):
        if token not in w1: fail("E_NON_GRAFT_CANDIDATE_CONTENT", token)
    for token in ("fergusonbazant2014", "guo2016", "persson2010b", "이식금지"):
        if token not in cherry: fail("E_NON_GRAFT_DECISION_CONTENT", token)
    conflicts = {row["id"]: row for row in obj["bibliographic_conflicts"]}
    bib_texts = "\n".join(blob(p).decode("utf-8") for p in (
        "Claude/docs/v1.0.24/_sections/ch1v22_bib.tex",
        "Claude/docs/v1.0.24/_sections/ch2v22_bib.tex",
        "Claude/docs/v1.0.24/_sections/ch3v22_bib.tex"))
    if bib_texts.lower().count("10.1149/2.0341708jes") != 3:
        fail("E_BIB_CONFLICT_DOI_COUNT")
    for fragment in ("Silicon, and Their Alloys", "Iron Phosphate, and Layered"):
        if fragment not in bib_texts: fail("E_BIB_CONFLICT_TITLE", fragment)

    v1024_code = blob("Claude/docs/v1.0.24/Anode_Fit_v1.0.24.py").decode("utf-8")
    v1025_code = blob("Claude/docs/v1.0.25/Anode_Fit_v1.0.24.py").decode("utf-8")
    if "def func_dxi_eq" in v1024_code or re.search(r"['\"]alpha['\"]", v1024_code):
        fail("E_GENEALOGY_V1024_STATIC_ALPHA_ABSENCE")
    for token in ("def func_dxi_eq", "tr.get('alpha')", "alpha_j"):
        if token not in v1025_code: fail("E_GENEALOGY_V1025_STATIC_ALPHA_PRESENCE", token)
    first_commit = "edbc4a2c68cda0dd21662cb6dd68ba8bed699a76"
    first_parent = "2147abfac3fb6c82279aefb2b21c749a521112dc"
    assert_equal(str(git("show", "-s", "--format=%P", first_commit)).strip(), first_parent,
                 "E_GENEALOGY_FIRST_PARENT")
    first_paths = set(str(git("diff", "--name-only", first_parent, first_commit)).splitlines())
    if "Claude/docs/v1.0.25/Anode_Fit_v1.0.24.py" not in first_paths:
        fail("E_GENEALOGY_FIRST_SOURCE_DIFF")

    # Every source binding is independently re-bound to exact Git bytes.
    for row in obj["source_bindings"]:
        raw = blob(row["path"])
        assert_equal(row["git_blob"], str(git("rev-parse", f"{BASELINE}:{row['path']}")).strip(), "E_BINDING_BLOB")
        assert_equal(row["sha256"], sha256(raw), "E_BINDING_SHA")
        assert_equal(row["lines"], len(raw.decode("utf-8").splitlines()), "E_BINDING_LINES")
        assert_equal(row["read_status"], "READ_FULL", "E_BINDING_READ_STATUS")

    # Named semantic probes must fail at the intended diagnostic, not incidentally.
    probes = 0

    def expect_rejection(name: str, mutate, checker, expected: str,
                         *, rehash: bool = True) -> None:
        nonlocal probes
        candidate = copy.deepcopy(obj)
        mutate(candidate)
        if rehash:
            candidate["semantic_sha256"] = canonical_semantic(candidate)
        try:
            checker(candidate)
        except AuditError as exc:
            actual = str(exc).split(":", 1)[0]
            if actual != expected:
                fail("E_NEGATIVE_WRONG_DIAGNOSTIC", f"{name}:{expected}:{actual}")
            probes += 1
            return
        fail("E_NEGATIVE_ESCAPE", name)

    def census_count(candidate: dict) -> None:
        assert_equal(candidate["tex_census"]["summary"]["files"], 90, "E_EXPECTED_CENSUS_FILES")

    def closure_count(candidate: dict) -> None:
        assert_equal(candidate["tex_census"]["closures"]["adopted_union"]["files"], 56,
                     "E_ADOPTED_UNION_FILES")

    cases = [
        ("expected-parent", lambda x: x.__setitem__("expected_parent", "0"*40),
         validate_header_contract, "E_PARENT", True),
        ("artifact-branch", lambda x: x.__setitem__("branch", "other"),
         validate_header_contract, "E_ARTIFACT_BRANCH", True),
        ("baseline-reference", lambda x: x.__setitem__("baseline_commit", "0"*40),
         validate_header_contract, "E_BASELINE", True),
        ("content-gate", lambda x: x.__setitem__("gate", "PASS"),
         validate_header_contract, "E_GATE", True),
        ("semantic-hash", lambda x: x.__setitem__("semantic_sha256", "0"*64),
         validate_header_contract, "E_SEMANTIC_SHA", False),
        ("step70-parent-gate", lambda x: x["consumed_parent_evidence"].__setitem__("step70_content_gate", "PASS"),
         validate_header_contract, "E_STEP70_GATE", True),
        ("step71-parent-gate", lambda x: x["consumed_parent_evidence"].__setitem__("step71_gate", "PASS"),
         validate_header_contract, "E_STEP71_GATE", True),
        ("scientific-authority", lambda x: x["authority"].__setitem__("material_truth", True),
         core_invariants, "E_AUTHORITY_MATERIAL_TRUTH", True),
        ("v1024-1-independence", lambda x: x["authority"].__setitem__("v1024_1_independent_corroboration", True),
         core_invariants, "E_V1024_1_CORROBORATION", True),
        ("route-count", lambda x: x["input_routes"].pop(),
         core_invariants, "E_ROUTE_COUNT", True),
        ("route-identity", lambda x: x["input_routes"][0].__setitem__("route_id", "P065-S70-F99"),
         core_invariants, "E_ROUTE_IDENTITIES", True),
        ("route-origin-record", lambda x: x["input_routes"][0]["origin_record"].__setitem__("severity", "P2"),
         core_invariants, "E_ROUTE_ORIGIN_RECORD", True),
        ("route-owner", lambda x: x["input_routes"][0].__setitem__("owner", "P065-STEP74-CONFORMANCE"),
         core_invariants, "E_ROUTE_OWNER_EXACT", True),
        ("route-followup-target", lambda x: x["input_routes"][0]["followup_targets"].pop(),
         core_invariants, "E_ROUTE_TARGETS_EXACT", True),
        ("logistic-width", lambda x: x["derivations"][0].__setitem__("dimensionless_fwhm", 1.0),
         validate_derivations, "E_LOGISTIC_FWHM", True),
        ("binodal-trivial-root", lambda x: x["derivations"][1].__setitem__("trivial_root_excluded", ""),
         validate_derivations, "E_BINODAL_TRIVIAL_ROOT", True),
        ("skew-measure", lambda x: x["derivations"][2]["weight_conditions"].pop(),
         validate_derivations, "E_SKEW_WEIGHT_CONDITIONS", True),
        ("blend-current", lambda x: x["derivations"][3].__setitem__("finite_rate_current_balance", "I=I_gr"),
         validate_derivations, "E_BLEND_CURRENT_BALANCE", True),
        ("material-count", lambda x: x["material_claims"].pop(),
         validate_material_claims, "E_MATERIAL_COUNTS", True),
        ("material-schema", lambda x: x["material_claims"][0].pop("derivation_id"),
         validate_material_claims, "E_MATERIAL_ROW_SCHEMA", True),
        ("material-line-range", lambda x: (
            x["material_claims"][0]["source_refs"][0].__setitem__("lines", "99999"),
            x["material_claims"][0]["exact_anchor"][0].__setitem__("lines", "99999")),
         validate_material_claims, "E_MATERIAL_LINE_RANGE", True),
        ("metadata-authority", lambda x: x["metadata_verifications"][0].__setitem__("artifact_authority", "VERIFIED"),
         core_invariants, "E_METADATA_AUTHORITY", True),
        ("first-skew-commit", lambda x: x["genealogy"][0].__setitem__("first_later_commit", "0"*40),
         core_invariants, "E_SKEW_FIRST_COMMIT", True),
        ("archive-only-role", lambda x: x["genealogy"][5].__setitem__("v1024_1_state", "IMPLEMENTED"),
         core_invariants, "E_V1024_1_ARCHIVE_ROLE", True),
        ("non-graft-decision", lambda x: x["non_graft"].__setitem__("decision", "GRAFTED"),
         validate_non_graft_contract, "E_NON_GRAFT_DECISION", True),
        ("bibliographic-conflict", lambda x: x["bibliographic_conflicts"][0].__setitem__("status", "VERIFIED"),
         validate_conflict_contract, "E_BIB_TITLE_CONFLICT", True),
        ("source-policy", lambda x: x["source_policy"]["rules"].pop(),
         validate_source_policy, "E_SOURCE_POLICY_RULES", True),
        ("binding-sha", lambda x: x["source_bindings"][0].__setitem__("sha256", "bad"),
         validate_binding_shape, "E_BINDING_SHA_FORMAT", True),
        ("binding-path-identity", lambda x: x["source_bindings"][1].__setitem__("path", x["source_bindings"][0]["path"]),
         validate_binding_shape, "E_BINDING_PATH_UNIQUE", True),
        ("tex-denominator", lambda x: x["tex_census"]["summary"].__setitem__("files", 89),
         census_count, "E_EXPECTED_CENSUS_FILES", True),
        ("closure-denominator", lambda x: x["tex_census"]["closures"]["adopted_union"].__setitem__("files", 55),
         closure_count, "E_ADOPTED_UNION_FILES", True),
    ]
    for name, mutate, checker, expected, rehash in cases:
        expect_rejection(name, mutate, checker, expected, rehash=rehash)
    assert_equal(probes, len(cases), "E_NEGATIVE_PROBES")
    strict_rejects = 0
    for bad in ('{"a":1,"a":2}', '{"x":NaN}', '{"x":Infinity}'):
        try: strict_json_loads(bad)
        except AuditError: strict_rejects += 1
    assert_equal(strict_rejects, 3, "E_STRICT_JSON_PROBES")
    return {"semantic_cases": 39 + len(rebuilt["files"]) + len(obj["material_claims"]),
            "negative_cases": probes, "source_policy_negative_cases": source_policy_cases,
            "strict_json_cases": strict_rejects, "tex_files": 90,
            "traversal_nodes": traversal_nodes, "traversal_depth": traversal_depth}


def check_determinism(matrix_bytes: bytes) -> None:
    if not BUILDER.exists(): fail("E_BUILDER_MISSING")
    spec = importlib.util.spec_from_file_location("phase065_step72_builder", BUILDER)
    if spec is None or spec.loader is None: fail("E_BUILDER_SPEC")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    outputs = []
    for _ in (1, 2):
        obj = module.build()
        outputs.append((json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                   indent=2) + "\n").encode("utf-8"))
    if outputs[0] != outputs[1] or outputs[0] != matrix_bytes:
        fail("E_DETERMINISM")


def git_controls(mode: str, expected_commit: str | None) -> None:
    assert_equal(str(git("branch", "--show-current")).strip(), BRANCH, "E_BRANCH")
    head = str(git("rev-parse", "HEAD")).strip()
    assert_equal(str(git("rev-parse", f"{BASELINE}^{{commit}}")).strip(), BASELINE,
                 "E_BASELINE_OBJECT")
    assert_equal(str(git("rev-parse", PROTECTED_BRANCH)).strip(), PROTECTED_TIP, "E_PROTECTED_LOCAL")
    assert_equal(str(git("rev-parse", f"origin/{PROTECTED_BRANCH}")).strip(), PROTECTED_TIP, "E_PROTECTED_REMOTE")
    assert_equal(str(git("rev-parse", "origin/main")).strip(), MAIN_TIP, "E_MAIN_REMOTE")
    assert_equal(str(git("rev-parse", "--abbrev-ref", "@{upstream}")).strip(),
                 f"origin/{BRANCH}", "E_UPSTREAM_NAME")
    protected_live = str(git("ls-remote", "--heads", "origin", f"refs/heads/{PROTECTED_BRANCH}")).split()
    main_live = str(git("ls-remote", "--heads", "origin", "refs/heads/main")).split()
    active_live_rows = str(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")).split()
    if not protected_live or protected_live[0] != PROTECTED_TIP: fail("E_PROTECTED_LIVE")
    if not main_live or main_live[0] != MAIN_TIP: fail("E_MAIN_LIVE")
    if not active_live_rows: fail("E_ACTIVE_LIVE_MISSING")
    expected_tip = expected_commit if mode == "persistence" else EXPECTED_PARENT
    if not expected_tip: fail("E_EXPECTED_TIP")
    assert_equal(str(git("rev-parse", "@{upstream}")).strip(), expected_tip,
                 "E_ACTIVE_UPSTREAM_TIP")
    assert_equal(str(git("rev-parse", f"origin/{BRANCH}")).strip(), expected_tip,
                 "E_ACTIVE_TRACKING_TIP")
    assert_equal(active_live_rows[0], expected_tip, "E_ACTIVE_LIVE_TIP")
    claude_diff = str(git("diff", "--name-only", PROTECTED_TIP, head, "--", "Claude")).strip()
    assert_equal(claude_diff, "", "E_CLAUDE_DIFF")
    assert_equal(str(git("diff", "--name-only", "--", "Claude")).strip(), "",
                 "E_CLAUDE_UNSTAGED")
    assert_equal(str(git("diff", "--cached", "--name-only", "--", "Claude")).strip(), "",
                 "E_CLAUDE_STAGED")
    if mode == "content":
        assert_equal(head, EXPECTED_PARENT, "E_CONTENT_HEAD")
        return
    if mode == "staged":
        assert_equal(head, EXPECTED_PARENT, "E_STAGED_HEAD")
        name_status = [x.split("\t") for x in str(git("diff", "--cached", "--name-status")).splitlines() if x]
        if any(len(x) != 2 or x[0] not in ("A", "M") for x in name_status): fail("E_STAGED_STATUS")
        staged = sorted(x[1] for x in name_status)
        assert_equal(staged, EXACT_PATHS, "E_STAGED_PATHS")
        expected_status = {p: ("M" if p in {
            "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
            "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
            "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"} else "A") for p in EXACT_PATHS}
        assert_equal({p: s for s, p in name_status}, expected_status, "E_STAGED_STATUS_MAP")
        unstaged = [x for x in str(git("diff", "--name-only")).splitlines() if x]
        assert_equal(unstaged, [], "E_UNSTAGED")
        status = [x for x in str(git("status", "--porcelain", "-uall")).splitlines() if x]
        if len(status) != 7 or any(len(x) < 4 or x[1] != " " or x.startswith("??") for x in status):
            fail("E_STAGED_WORKTREE_STATUS", repr(status))
        assert_equal(str(git("diff", "--cached", "--check")).strip(), "", "E_DIFF_CHECK")
        for path in EXACT_PATHS:
            assert_equal(git("show", f":{path}", text=False), Path(path).read_bytes(), "E_INDEX_WORKTREE_BYTES")
        return
    if not expected_commit: fail("E_EXPECTED_COMMIT_REQUIRED")
    assert_equal(head, expected_commit, "E_PERSIST_HEAD")
    assert_equal(str(git("rev-parse", "HEAD^" )).strip(), EXPECTED_PARENT, "E_PERSIST_PARENT")
    assert_equal(str(git("show", "-s", "--format=%s", "HEAD")).strip(), SUBJECT, "E_SUBJECT")
    changed_rows = [x.split("\t") for x in str(git("diff-tree", "--no-commit-id", "--name-status", "-r", "HEAD")).splitlines() if x]
    if any(len(x) != 2 or x[0] not in ("A", "M") for x in changed_rows): fail("E_COMMIT_STATUS")
    assert_equal(sorted(x[1] for x in changed_rows), EXACT_PATHS, "E_COMMIT_PATHS")
    assert_equal(str(git("rev-parse", "@{upstream}")).strip(), expected_commit, "E_UPSTREAM")
    assert_equal(str(git("rev-parse", f"origin/{BRANCH}")).strip(), expected_commit, "E_TRACKING")
    live_rows = str(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")).split()
    if not live_rows: fail("E_LIVE_REMOTE_MISSING")
    live = live_rows[0]
    assert_equal(live, expected_commit, "E_LIVE_REMOTE")
    assert_equal(str(git("status", "--porcelain")).strip(), "", "E_DIRTY")
    for path in EXACT_PATHS:
        assert_equal(git("show", f"HEAD:{path}", text=False), Path(path).read_bytes(), "E_COMMIT_WORKTREE_BYTES")


def main() -> int:
    ap = argparse.ArgumentParser()
    modes = ap.add_mutually_exclusive_group()
    modes.add_argument("--staged", action="store_true")
    modes.add_argument("--persistence", action="store_true")
    ap.add_argument("--expected-commit")
    args = ap.parse_args()
    mode = "persistence" if args.persistence else "staged" if args.staged else "content"
    try:
        if not MATRIX.exists(): fail("E_MATRIX_MISSING")
        raw = MATRIX.read_bytes()
        if not raw.endswith(b"\n") or raw.startswith(b"\xef\xbb\xbf"):
            fail("E_JSON_ENCODING")
        if b"\r" in raw: fail("E_JSON_NOT_CANONICAL_LF")
        raw_sha = sha256(raw)
        lf_raw = raw
        lf_sha = sha256(lf_raw)
        obj = strict_json_loads(raw.decode("utf-8"))
        stats = check_content(obj)
        if not RESULT.exists(): fail("E_RESULT_DOC_MISSING")
        result_text = RESULT.read_text(encoding="utf-8")
        required_result_tokens = [
            PASS_CONTENT, "PENDING_AT_PRECOMMIT_BY_DESIGN", "0<x_a<1/2",
            "nonzero-measure set", "total active solids 1 g", "I=I_gr+I_Si",
            "합계 28개 row", "UNVERIFIED_EXTERNAL_NO_RAW_RESPONSE",
            "edbc4a2c", "90개 unique TeX blob", "26개와 Step 71 finding 13개",
            "negative mutations 31개", "AST-only execution/filesystem escape 126개",
        ]
        for token in required_result_tokens:
            if token not in result_text: fail("E_RESULT_TOKEN", token)
        if "v1.0.25.1 first implementation" in result_text:
            fail("E_RESULT_SUPERSEDED_FIRST_IMPLEMENTATION")
        for heading in ("## 1. Outcome", "## 2. Recovery and Read Coverage",
                        "## 3. Origin Genealogy", "## 4. Independent Derivations",
                        "## 5. Material-specific Authority Ceilings",
                        "## 6. Citation and DOI Census",
                        "## 7. External Bibliographic Metadata Boundary",
                        "## 8. Findings and Routing", "## 9. Validation Contract",
                        "## 10. Next Exact Action"):
            if result_text.count(heading) != 1: fail("E_RESULT_HEADING", heading)
        for forbidden in ("PENDING_STEP72_MATRIX_", "external_bibliographic_metadata_verified=true",
                          "material_truth=true", "publication_ready=true"):
            if forbidden in result_text: fail("E_RESULT_FORBIDDEN", forbidden)
        handover = Path("Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md").read_text(encoding="utf-8")
        for token in ("Current checkpoint: Step 72 `PASS_PENDING_PERSISTENCE`",
                      "Step 71 commit `5978da8626406879609b0dd5792f79143015e67f`",
                      "semantic/source-policy/strict negatives `31/126/3`"):
            if token not in handover: fail("E_HANDOVER_CURRENT", token)
        canonical_ledger = Path("Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md").read_text(encoding="utf-8")
        if "| Step 72 |" not in canonical_ledger or "semantic/source-policy/strict negatives `31/126/3`" not in canonical_ledger:
            fail("E_CANONICAL_LEDGER_STEP72")
        check_determinism(raw)
        git_controls(mode, args.expected_commit)
        terminal = PASS_PERSISTENCE if mode == "persistence" else PASS_CONTENT
        print(terminal, json.dumps({**stats, "raw_sha256": raw_sha,
                                    "lf_sha256": lf_sha,
                                    "semantic_sha256": obj["semantic_sha256"],
                                    "determinism": "2/2", "mode": mode},
                                   sort_keys=True, separators=(",", ":")))
        return 0
    except (AuditError, json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
