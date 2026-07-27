#!/usr/bin/env python3
"""Generate Phase 059 production-code AST inventory, exact diffs, and review."""

from __future__ import annotations

import ast
import difflib
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
WORK = ROOT / "Codex" / "work" / "v1014_v1018_2_phase059"
DIFF_DIR = WORK / "code_diffs"
QUEUE = RESULTS / "PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json"
INDEX_OUT = RESULTS / "PHASE_059_PRODUCTION_CODE_INDEX.json"
DIFF_OUT = RESULTS / "PHASE_059_PRODUCTION_CODE_DIFF.json"
REVIEW_OUT = RESULTS / "PHASE_059_PRODUCTION_CODE_REVIEW.md"

CODE_PATHS = [
    "Claude/docs/v1.0.14/Anode_Fit_v1.0.14.py",
    "Claude/docs/v1.0.15/Anode_Fit_v1.0.15.py",
    "Claude/docs/v1.0.16/Anode_Fit_v1.0.16.py",
    "Claude/docs/v1.0.18.2/Anode_Fit_v1.0.18.2.py",
]
COMPARISONS = [
    ("code_v1014_to_v1015", CODE_PATHS[0], CODE_PATHS[1]),
    ("code_v1015_to_v1016", CODE_PATHS[1], CODE_PATHS[2]),
    ("code_v1016_to_v1018_2", CODE_PATHS[2], CODE_PATHS[3]),
]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def name_of_call(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = name_of_call(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def signature_of(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    text = ast.unparse(node.args)
    return f"{prefix} {node.name}({text})"


def function_record(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    owner: str | None = None,
) -> dict:
    qualified_name = f"{owner}.{node.name}" if owner else node.name
    segment = "\n".join(source_lines[node.lineno - 1 : node.end_lineno]) + "\n"
    calls = sorted(
        {
            name_of_call(call.func)
            for call in ast.walk(node)
            if isinstance(call, ast.Call) and name_of_call(call.func)
        }
    )
    string_keys = sorted(
        {
            arg.value
            for call in ast.walk(node)
            if isinstance(call, ast.Call)
            and isinstance(call.func, ast.Attribute)
            and call.func.attr == "get"
            and call.args
            and isinstance((arg := call.args[0]), ast.Constant)
            and isinstance(arg.value, str)
        }
        | {
            sub.slice.value
            for sub in ast.walk(node)
            if isinstance(sub, ast.Subscript)
            and isinstance(sub.slice, ast.Constant)
            and isinstance(sub.slice.value, str)
        }
    )
    return {
        "qualified_name": qualified_name,
        "name": node.name,
        "owner": owner,
        "visibility": (
            "SPECIAL"
            if node.name == "__init__"
            else "PRIVATE"
            if node.name.startswith("_")
            else "PUBLIC"
        ),
        "line_start": node.lineno,
        "line_end": node.end_lineno,
        "signature": signature_of(node),
        "source_sha256": sha256_bytes(segment.encode("utf-8")),
        "calls": calls,
        "transition_keys": string_keys,
    }


def literal_assignments(tree: ast.Module, names: set[str]) -> dict:
    values: dict[str, object] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        value_node = node.value
        for target in targets:
            if isinstance(target, ast.Name) and target.id in names:
                try:
                    values[target.id] = ast.literal_eval(value_node)
                except (ValueError, TypeError):
                    values[target.id] = ast.unparse(value_node)
    return values


def module_record(path: str, blob_sha: str, occurrences: list[str]) -> dict:
    raw = (ROOT / path).read_bytes()
    source = raw.decode("utf-8")
    lines = source.splitlines()
    tree = ast.parse(source, filename=path)
    functions: list[dict] = []
    classes: list[dict] = []
    imports: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(function_record(node, lines))
        elif isinstance(node, ast.ClassDef):
            methods = [
                function_record(child, lines, node.name)
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            functions.extend(methods)
            classes.append(
                {
                    "name": node.name,
                    "line_start": node.lineno,
                    "line_end": node.end_lineno,
                    "bases": [ast.unparse(base) for base in node.bases],
                    "methods": [item["qualified_name"] for item in methods],
                }
            )
    literals = literal_assignments(
        tree,
        {
            "R",
            "F",
            "EV_TO_J",
            "_LAG_RESOLVE_DECAY_CAP",
            "LCO_MSMR_LIT",
            "GRAPHITE_STAGING_LIT",
        },
    )
    datasets = {}
    for name in ("LCO_MSMR_LIT", "GRAPHITE_STAGING_LIT"):
        value = literals.pop(name, None)
        if isinstance(value, list):
            datasets[name] = {
                "transition_count": len(value),
                "transition_key_sets": [
                    sorted(item) for item in value if isinstance(item, dict)
                ],
                "literal_sha256": sha256_bytes(
                    json.dumps(
                        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                    ).encode("utf-8")
                ),
                "values": value,
            }
    return {
        "representative_path": path,
        "occurrence_paths": occurrences,
        "git_blob_sha": blob_sha,
        "sha256": sha256_bytes(raw),
        "byte_count": len(raw),
        "line_count": len(lines),
        "imports": imports,
        "module_constants": literals,
        "classes": classes,
        "functions": functions,
        "public_api": [
            {
                "qualified_name": item["qualified_name"],
                "signature": item["signature"],
            }
            for item in functions
            if item["visibility"] in {"PUBLIC", "SPECIAL"}
        ],
        "datasets": datasets,
    }


def opcode_counts(old_lines: list[str], new_lines: list[str]) -> dict:
    counts = Counter()
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
        None, old_lines, new_lines, autojunk=False
    ).get_opcodes():
        if tag == "equal":
            counts["equal"] += i2 - i1
        elif tag == "replace":
            counts["replace_old"] += i2 - i1
            counts["replace_new"] += j2 - j1
        elif tag == "delete":
            counts["delete"] += i2 - i1
        elif tag == "insert":
            counts["insert"] += j2 - j1
    return dict(sorted(counts.items()))


def exact_anchor(path: str, line: int, needle: str) -> dict:
    lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
    source_line = lines[line - 1]
    if needle not in source_line:
        raise ValueError(f"anchor mismatch {path}:{line}: {needle!r}")
    return {
        "path": path,
        "line": line,
        "needle": needle,
        "source_line": source_line,
    }


def finding(
    finding_id: str,
    title: str,
    disposition: str,
    severity: str,
    claim: str,
    consequence: str,
    required_action: str,
    anchors: list[tuple[str, int, str]],
    contracts: list[str],
) -> dict:
    return {
        "id": finding_id,
        "title": title,
        "disposition": disposition,
        "severity": severity,
        "claim": claim,
        "consequence": consequence,
        "required_action": required_action,
        "source_evidence": [exact_anchor(*item) for item in anchors],
        "contract_ids": contracts,
    }


def main() -> None:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    queue_code = {
        item["representative_path"]: item
        for item in queue["records"]
        if item["role"] == "code"
    }
    modules = [
        module_record(
            path,
            queue_code[path]["blob_sha"],
            queue_code[path]["occurrence_paths"],
        )
        for path in CODE_PATHS
    ]
    index = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": queue["baseline_commit"],
        "scope": "Phase 059 Step 34.1 production code AST/API/default/call inventory",
        "status": "PASS_P059_PRODUCTION_CODE_INDEX",
        "authority_boundary": (
            "Static source inventory only; it does not certify runtime behavior, "
            "test adequacy, theory conformance, or experimental validity."
        ),
        "unique_blob_count": len(modules),
        "occurrence_path_count": sum(len(item["occurrence_paths"]) for item in modules),
        "total_line_count": sum(item["line_count"] for item in modules),
        "modules": modules,
    }
    INDEX_OUT.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    DIFF_DIR.mkdir(parents=True, exist_ok=True)
    module_by_path = {item["representative_path"]: item for item in modules}
    comparisons = []
    for pair_id, old_path, new_path in COMPARISONS:
        old_text = (ROOT / old_path).read_text(encoding="utf-8")
        new_text = (ROOT / new_path).read_text(encoding="utf-8")
        old_lines = old_text.splitlines()
        new_lines = new_text.splitlines()
        patch_text = "".join(
            difflib.unified_diff(
                old_text.splitlines(keepends=True),
                new_text.splitlines(keepends=True),
                fromfile=old_path,
                tofile=new_path,
                n=3,
            )
        )
        patch_path = DIFF_DIR / f"{pair_id}.patch"
        patch_path.write_text(patch_text, encoding="utf-8")
        old_mod = module_by_path[old_path]
        new_mod = module_by_path[new_path]
        old_functions = {
            item["qualified_name"]: item for item in old_mod["functions"]
        }
        new_functions = {
            item["qualified_name"]: item for item in new_mod["functions"]
        }
        common = set(old_functions) & set(new_functions)
        comparisons.append(
            {
                "pair_id": pair_id,
                "old_path": old_path,
                "new_path": new_path,
                "old_blob_sha": old_mod["git_blob_sha"],
                "new_blob_sha": new_mod["git_blob_sha"],
                "old_line_count": len(old_lines),
                "new_line_count": len(new_lines),
                "content_identical": old_text == new_text,
                "opcode_line_counts": opcode_counts(old_lines, new_lines),
                "exact_unified_diff": str(patch_path.relative_to(ROOT)),
                "exact_unified_diff_sha256": sha256_bytes(
                    patch_text.encode("utf-8")
                ),
                "functions_added": sorted(set(new_functions) - set(old_functions)),
                "functions_removed": sorted(set(old_functions) - set(new_functions)),
                "functions_source_changed": sorted(
                    name
                    for name in common
                    if old_functions[name]["source_sha256"]
                    != new_functions[name]["source_sha256"]
                ),
                "public_api_old": old_mod["public_api"],
                "public_api_new": new_mod["public_api"],
                "public_api_changed": old_mod["public_api"] != new_mod["public_api"],
                "dataset_hashes_old": {
                    name: value["literal_sha256"]
                    for name, value in old_mod["datasets"].items()
                },
                "dataset_hashes_new": {
                    name: value["literal_sha256"]
                    for name, value in new_mod["datasets"].items()
                },
            }
        )
    diff_index = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": queue["baseline_commit"],
        "scope": "Phase 059 Step 34.1 exact production-code lineage",
        "status": "PASS_P059_PRODUCTION_CODE_EXACT_DIFF",
        "authority_boundary": (
            "Exact source/AST lineage only; changed code does not imply correct "
            "physics, adequate tests, or external validity."
        ),
        "comparison_count": len(comparisons),
        "copy_forward": [
            {
                "git_blob_sha": queue_code[CODE_PATHS[2]]["blob_sha"],
                "occurrence_paths": queue_code[CODE_PATHS[2]]["occurrence_paths"],
                "meaning": "v1.0.16, v1.0.17, and v1.0.18.1 are one identical production-code blob.",
            }
        ],
        "comparisons": comparisons,
    }
    DIFF_OUT.write_text(
        json.dumps(diff_index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    latest = CODE_PATHS[-1]
    findings = [
        finding(
            "P059-CODE-001",
            "Pointwise grid removal is source-confirmed",
            "PRESERVE",
            "INFO",
            "v1.0.15 removes the work-grid constructor parameters and replaces the low-pass helper with pointwise causal memory.",
            "This satisfies the user's grid-removal architecture direction at source level.",
            "Preserve pointwise evaluation while repairing its trajectory-state contract.",
            [(CODE_PATHS[1], 105, "_causal_memory_pointwise")],
            ["P059-CON-018"],
        ),
        finding(
            "P059-CODE-002",
            "Voltage sorting destroys supplied trajectory order",
            "CORRECT",
            "CRITICAL",
            "dqdv sorts V_n by voltage and reconstructs the result, so the memory state depends on the set of voltages rather than the supplied chronological trajectory.",
            "Repeated, reversal, pulse, and nonmonotone protocols cannot carry their actual history.",
            "Accept an explicit monotone segment/time order and evolve a persistent state without sorting away protocol history.",
            [(latest, 517, "order = np.argsort")],
            ["P059-CON-017", "P059-CON-018"],
        ),
        finding(
            "P059-CODE-003",
            "Finite-window initial state is forced to equilibrium",
            "CORRECT",
            "HIGH",
            "The first lagged occupancy is set equal to the first equilibrium occupancy.",
            "Prehistory and preparation state are erased at every call.",
            "Expose initial internal state or prehistory and test finite-window sensitivity.",
            [(latest, 122, "out[0] =")],
            ["P059-CON-019"],
        ),
        finding(
            "P059-CODE-004",
            "Direct L_V override has no zero-current limit",
            "CORRECT",
            "CRITICAL",
            "A transition-level L_V override is returned before the I <= 0 equilibrium condition.",
            "A fitted nonzero lag can survive when current is zero, contradicting the equilibrium limit.",
            "Interpret direct input as a rate coefficient/state timescale or force L_V(I=0)=0.",
            [(latest, 412, "L_V_override"), (latest, 418, "if I <= 0")],
            ["P059-CON-021"],
        ),
        finding(
            "P059-CODE-005",
            "Local voltage-dependent barrier is frozen at one cutoff affinity",
            "REJECT",
            "CRITICAL",
            "The affinity A is computed once from z_cut, n, R, and T and is constant across the voltage trace.",
            "The realized barrier and lag do not respond locally to electrode potential as required by the originating experiment.",
            "Derive and evaluate a local electrochemical driving-force/barrier relation at each state.",
            [(latest, 430, "A = float(min")],
            ["P059-CON-020"],
        ),
        finding(
            "P059-CODE-006",
            "C-rate and Q_cell unit contract is ambiguous",
            "CORRECT",
            "CRITICAL",
            "curve computes I = c_rate * Q_cell while Q_cell is also accepted as generic charge.",
            "If Q_cell is coulombs rather than ampere-hours, current is wrong by a factor of 3600.",
            "Use distinct Q_cell_Ah and Q_cell_C inputs or an explicit unit conversion.",
            [(latest, 599, "C-rate [1/h]"), (latest, 615, "I_use = c * Q_cell")],
            ["P059-CON-003", "P059-CON-016"],
        ),
        finding(
            "P059-CODE-007",
            "Default thermal width and default dwdT disagree",
            "CORRECT",
            "HIGH",
            "_n_factor returns default n=1 when neither n nor w exists, but _dwdT returns zero whenever n is absent.",
            "The same transition is thermal in dQ/dV and temperature-frozen in reversible heat.",
            "Make the fallback role explicit and use a single width object for w and its derivative.",
            [(latest, 314, "return 1.0"), (latest, 332, "if tr.get('n') is None")],
            ["P059-CON-011", "P059-CON-023"],
        ),
        finding(
            "P059-CODE-008",
            "Lag kinetics collapses local T(V) to one mean temperature",
            "CORRECT",
            "HIGH",
            "The array temperature is averaged to T_rep and the lag length is resolved once per transition.",
            "Nonisothermal local barrier and relaxation dependence are lost even though peak width remains pointwise in T.",
            "Evaluate the state rate locally in time/charge with T(t) rather than one trace-mean lag length.",
            [(latest, 525, "T_rep = float(np.mean"), (latest, 565, "_resolve_lag_length")],
            ["P059-CON-016", "P059-CON-020"],
        ),
        finding(
            "P059-CODE-009",
            "Einstein reference temperature is finite but not positive",
            "CORRECT",
            "MEDIUM",
            "theta_E is checked positive, but theta_E_Tref is checked only for finiteness.",
            "Zero or negative reference temperature can enter exponential/logarithmic thermodynamic formulas.",
            "Validate theta_E_Tref with the positive-temperature guard.",
            [(latest, 369, 'Tref = _finite("theta_E_Tref"')],
            ["P059-CON-030", "P059-CON-031"],
        ),
        finding(
            "P059-CODE-010",
            "LCO electronic entropy is frozen at 298.15 K",
            "EMPIRICAL_ONLY",
            "HIGH",
            "The LCO subclass evaluates the electronic entropy only at a hard-coded reference temperature.",
            "The claimed Sommerfeld temperature scale, implicit composition feedback, and T-squared center shift are absent.",
            "Implement the reaction-specific electronic free energy with explicit x(V,T) coupling and derivatives.",
            [(latest, 794, "T_ref = 298.15")],
            ["P059-CON-036", "P059-CON-038"],
        ),
        finding(
            "P059-CODE-011",
            "High-voltage doped LCO scope is absent from defaults",
            "CORRECT",
            "CRITICAL",
            "The LCO dataset has only three generic transitions ending near 4.05 V and no dopant/state descriptors.",
            "It cannot represent the requested doped high-voltage LCO materials or their degradation/phase constraints.",
            "Build literature/data-backed material-specific LCO parameter/state models through the target voltage window.",
            [(latest, 730, "LCO_MSMR_LIT ="), (latest, 748, "'U': 4.050")],
            ["P059-CON-033", "P059-CON-037"],
        ),
        finding(
            "P059-CODE-012",
            "v1.0.16 through v1.0.18.1 is one code blob",
            "COPY_FORWARD",
            "INFO",
            "The frozen queue maps three version paths to one Git blob.",
            "v1.0.17 and v1.0.18.1 cannot constitute independent production-code progress.",
            "Count them as documentation lineage only.",
            [(CODE_PATHS[2], 1, "# -*- coding: utf-8 -*-")],
            [],
        ),
        finding(
            "P059-CODE-013",
            "Einstein capability is inactive in shipped defaults",
            "INTERNAL_CAPABILITY_ONLY",
            "HIGH",
            "The v1.0.18.2 helpers require theta_E, but neither shipped graphite nor LCO transition dictionaries provide it.",
            "Regression preservation is expected because the new path is dormant; it does not validate material vibrational physics.",
            "Define reaction-specific phonon quantities and validate them on multi-temperature data before activation.",
            [(latest, 344, "te = tr.get('theta_E')"), (latest, 804, "GRAPHITE_STAGING_LIT =")],
            ["P059-CON-030", "P059-CON-032"],
        ),
    ]

    disposition_counts = Counter(item["disposition"] for item in findings)
    severity_counts = Counter(item["severity"] for item in findings)
    comparison_rows = "\n".join(
        f"| {item['pair_id']} | {item['old_line_count']}→{item['new_line_count']} | "
        f"{', '.join(item['functions_added']) or '—'} | "
        f"{', '.join(item['functions_removed']) or '—'} | "
        f"{len(item['functions_source_changed'])} |"
        for item in comparisons
    )
    finding_rows = "\n".join(
        f"| {item['id']} | {item['severity']} | {item['disposition']} | "
        f"{item['title']} | "
        + "; ".join(
            f"{Path(e['path']).name}:{e['line']}" for e in item["source_evidence"]
        )
        + " |"
        for item in findings
    )
    review = f"""# Phase 059 production-code source review

이 문건은 Step 34.1 정적 소스 감사다. runtime test, test adequacy,
theory conformance와 실험 타당성 판정은 후속 단계다.

## 계보

- unique production blobs: {len(modules)}
- occurrence paths: {sum(len(item['occurrence_paths']) for item in modules)}
- fully read lines: {sum(item['line_count'] for item in modules)}
- v1.0.16, v1.0.17, v1.0.18.1은 동일 Git blob이다.

| Pair | Lines | Functions added | Functions removed | Functions source-changed |
|---|---:|---|---|---:|
{comparison_rows}

## 정적 판정

| ID | Severity | Disposition | Finding | Source anchors |
|---|---|---|---|---|
{finding_rows}

## 핵심 결론

1. v1.0.15의 작업격자 퇴출과 점별 memory helper 추가는 exact code
   diff로 확인된다.
2. 그러나 입력 전위를 정렬하므로 실제 protocol chronology가
   사라지고, 첫 상태를 평형으로 강제한다. 현재 memory는 일반적인
   reversal/pulse/history model이 아니다.
3. local potential-dependent barrier 요구는 구현되지 않았다.
   affinity는 전이당 한 cutoff 값으로 동결되고, 비등온 trace의
   kinetics도 평균온도 하나로 축약된다.
4. direct `L_V`는 $I=0$보다 먼저 반환되어 zero-current limit를
   위반할 수 있고, C-rate/Q-cell 단위는 3600배 모호하다.
5. v1.0.16의 default width와 `_dwdT` fallback은 서로 다른
   temperature semantics를 갖는다.
6. v1.0.18.2 Einstein 경로는 내부적으로 추가됐지만 기본 dataset에서
   비활성이다. LCO electronic 항은 298.15 K에 동결돼 있고,
   doped high-voltage LCO scope는 없다.

정적 gate:
`PASS_P059_PRODUCTION_CODE_INDEX`,
`PASS_P059_PRODUCTION_CODE_EXACT_DIFF`.
"""
    REVIEW_OUT.write_text(review, encoding="utf-8")
    review_data = {
        "finding_count": len(findings),
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "severity_counts": dict(sorted(severity_counts.items())),
        "findings": findings,
    }
    # Embed machine-readable review findings alongside the prose through the code index.
    index["review"] = review_data
    INDEX_OUT.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
