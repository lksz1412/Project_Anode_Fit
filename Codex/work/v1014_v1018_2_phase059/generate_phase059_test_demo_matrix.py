#!/usr/bin/env python3
"""Generate the Phase 059 test/demo assertion and evidence matrix."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
QUEUE = RESULTS / "PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json"
OUTPUT = RESULTS / "PHASE_059_TEST_DEMO_ASSERTION_MATRIX.json"
SUMMARY = RESULTS / "PHASE_059_TEST_DEMO_ASSERTION_REVIEW.md"

LATEST = "Claude/docs/v1.0.18.2"
REG = f"{LATEST}/test_regression_graphite.py"
SAMPLE = f"{LATEST}/sample_test_v1018_2.py"
SUITE = f"{LATEST}/graph_suite_v1018_2.py"
DEMO = f"{LATEST}/demo_lco_heat.py"
PLOT = f"{LATEST}/plot_dqdv.py"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


class LogicNormalizer(ast.NodeTransformer):
    """Remove version/path-only string differences without changing code structure."""

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if isinstance(node.value, str):
            value = node.value
            value = re.sub(
                r"v?1\.0\.\d+(?:\.\d+)?", "<VER>", value, flags=re.IGNORECASE
            )
            value = re.sub(
                r"v10(?:14|15|16|17|18_1|18_2)", "<VTAG>", value
            )
            value = re.sub(
                r"v1_0_(?:14|15|16|17|18_1|18_2)", "<VFILE>", value
            )
            value = re.sub(
                r"\\?Claude\\docs\\<VER>\\[^\"']+", "<PATH>", value
            )
            node.value = value
        return node


def assigned_strings(tree: ast.Module) -> dict[str, str]:
    values: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if not isinstance(node.value, ast.Constant) or not isinstance(
            node.value.value, str
        ):
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                values[target.id] = node.value.value
    return values


def source_segment(source: str, node: ast.AST) -> str:
    return ast.get_source_segment(source, node) or ""


def file_record(queue_record: dict) -> dict:
    path = queue_record["representative_path"]
    raw = (ROOT / path).read_bytes()
    source = raw.decode("utf-8")
    tree = ast.parse(source, filename=path)
    normalized = LogicNormalizer().visit(ast.parse(source, filename=path))
    ast.fix_missing_locations(normalized)

    calls = [
        {
            "name": call_name(node.func),
            "line": node.lineno,
            "source": source_segment(source, node),
        }
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and call_name(node.func)
    ]
    asserts = [
        {
            "line": node.lineno,
            "test": source_segment(source, node.test),
            "message": source_segment(source, node.msg) if node.msg else None,
        }
        for node in ast.walk(tree)
        if isinstance(node, ast.Assert)
    ]
    comparisons = [
        {
            "line": node.lineno,
            "source": source_segment(source, node),
        }
        for node in ast.walk(tree)
        if isinstance(node, ast.Compare)
    ]
    strings = assigned_strings(tree)
    text = source
    family = (
        "sample_test"
        if Path(path).name.startswith("sample_test")
        else "regression"
        if Path(path).name == "test_regression_graphite.py"
        else "graph_suite"
        if Path(path).name.startswith("graph_suite")
        else "demo_lco_heat"
        if Path(path).name == "demo_lco_heat.py"
        else "plot_dqdv"
    )
    evidence_class = (
        "ENFORCED_INTERNAL_REGRESSION"
        if family == "regression"
        else "PRINT_ONLY_VISUALIZATION"
    )
    return {
        "representative_path": path,
        "occurrence_paths": queue_record["occurrence_paths"],
        "git_blob_sha": queue_record["blob_sha"],
        "sha256": sha256_bytes(raw),
        "line_count": len(source.splitlines()),
        "role": queue_record["role"],
        "family": family,
        "logic_normalized_ast_sha256": sha256_bytes(
            ast.dump(normalized, include_attributes=False).encode("utf-8")
        ),
        "evidence_class": evidence_class,
        "assert_count": len(asserts),
        "assertions": asserts,
        "comparison_count": len(comparisons),
        "comparisons": comparisons,
        "print_count": sum(call["name"] == "print" for call in calls),
        "exit_calls": [
            call for call in calls if call["name"] in {"sys.exit", "exit"}
        ],
        "array_equal_calls": [
            call for call in calls if call["name"].endswith("array_equal")
        ],
        "allclose_calls": [
            call
            for call in calls
            if call["name"].endswith("allclose")
            or call["name"].endswith("isclose")
        ],
        "golden_read_calls": [
            call for call in calls if call["name"] in {"np.load", "numpy.load"}
        ],
        "golden_write_calls": [
            call
            for call in calls
            if call["name"] in {"np.savez", "numpy.savez", "np.save"}
        ],
        "figure_write_calls": [
            call for call in calls if call["name"].endswith("savefig")
        ],
        "dynamic_import_calls": [
            call
            for call in calls
            if call["name"].endswith("spec_from_file_location")
            or call["name"].endswith("exec_module")
        ],
        "model_calls": sorted(
            {
                call["name"].split(".")[-1]
                for call in calls
                if call["name"].split(".")[-1]
                in {
                    "equilibrium",
                    "dqdv",
                    "curve",
                    "entropy_coefficient",
                    "reversible_heat",
                    "irreversible_heat",
                    "_resolve_lag_length",
                    "_dwdT",
                    "_S_vib",
                    "_vib_dU",
                    "_vib_dS",
                }
            }
        ),
        "assigned_paths": {
            key: value
            for key, value in strings.items()
            if key in {"CODE", "GOLD", "OUT", "FIGS", "FIGDIR", "HERE"}
        },
        "feature_tokens": {
            token: text.count(token)
            for token in (
                "n_T1",
                "theta_E",
                "L_V",
                "nonmonot",
                "reversal",
                "pulse",
                "experimental",
                "measured",
            )
        },
    }


def anchor(path: str, line: int, needle: str) -> dict:
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
    evidence_class: str,
    disposition: str,
    claim: str,
    implication: str,
    anchors: list[tuple[str, int, str]],
) -> dict:
    return {
        "id": finding_id,
        "title": title,
        "evidence_class": evidence_class,
        "disposition": disposition,
        "claim": claim,
        "implication": implication,
        "source_evidence": [anchor(*item) for item in anchors],
    }


def main() -> None:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    records = [
        file_record(item)
        for item in queue["records"]
        if item["role"] in {"test", "demo"}
    ]
    records.sort(key=lambda item: item["representative_path"])

    families: dict[str, list[dict]] = defaultdict(list)
    logic_groups: dict[str, list[str]] = defaultdict(list)
    for record in records:
        families[record["family"]].append(record)
        logic_groups[record["logic_normalized_ast_sha256"]].append(
            record["representative_path"]
        )

    findings = [
        finding(
            "P059-TD-001",
            "All thirty files contain zero Python assert statements",
            "STATIC_TEST_STRUCTURE",
            "CONFIRMED",
            "The 12 test-role and 18 demo-role blobs contain no ast.Assert node.",
            "Only explicit exit codes or uncaught exceptions can enforce failure.",
            [(REG, 55, "def main")],
        ),
        finding(
            "P059-TD-002",
            "Regression verify enforces bit equality on generated arrays",
            "INTERNAL_REGRESSION",
            "INTERNAL_ONLY",
            "verify compares each current output array with the golden array using np.array_equal and exits nonzero on mismatch.",
            "This protects one numerical baseline but proves neither physical correctness nor experimental agreement.",
            [(REG, 72, "np.array_equal"), (REG, 82, "sys.exit")],
        ),
        finding(
            "P059-TD-003",
            "Area conservation is printed but not gated",
            "PRINT_ONLY_NUMERIC",
            "OVERCLAIM_RISK",
            "The regression harness computes equilibrium area and prints its ratio without including it in all_ok.",
            "The documented area check can fail while the regression process exits successfully.",
            [(REG, 79, "a, q = area_check"), (REG, 80, "AREA check(post)")],
        ),
        finding(
            "P059-TD-004",
            "Capture mode overwrites the golden baseline",
            "MUTATING_TEST_MODE",
            "CONTROL_REQUIRED",
            "capture writes all current outputs directly to GOLD.",
            "Running capture before adjudicating a change can normalize a defect into the baseline.",
            [(REG, 61, 'mode == "capture"'), (REG, 62, "np.savez")],
        ),
        finding(
            "P059-TD-005",
            "Golden path is hard-coded while only code path is overridable",
            "PORTABILITY",
            "CORRECT",
            "ANODEFIT_CODE can redirect the module, but GOLD remains an absolute Windows path.",
            "The harness is not hermetic and cannot be executed reliably on another host without controlled source rewriting or path emulation.",
            [(REG, 15, "ANODEFIT_CODE"), (REG, 17, "GOLD =")],
        ),
        finding(
            "P059-TD-006",
            "Sample tests are report-only visualizations",
            "PRINT_ONLY_VISUALIZATION",
            "NOT_A_GATE",
            "The sample script explicitly labels console verification as report only and always prints DONE.",
            "Finite values and peak counts are not asserted.",
            [(SAMPLE, 106, "report only"), (SAMPLE, 124, "DONE")],
        ),
        finding(
            "P059-TD-007",
            "LCO heat demo has no numeric failure condition",
            "PRINT_ONLY_VISUALIZATION",
            "NOT_A_GATE",
            "The demo prints expected values and a validation-done banner without an enforced comparison.",
            "It demonstrates execution and plotting only.",
            [(DEMO, 22, "기대 ~ -45.7"), (DEMO, 73, "VALIDATION DONE")],
        ),
        finding(
            "P059-TD-008",
            "Graph suite finite, parity, area, and dictionary checks are print-only",
            "PRINT_ONLY_NUMERIC",
            "NOT_A_GATE",
            "The suite collects finite flags and prints errors/ratios/expected labels without sys.exit or assert.",
            "A false finite flag or wrong ratio still exits zero absent an exception.",
            [(SUITE, 137, "round-trip"), (SUITE, 140, "all_finite"), (SUITE, 145, "DONE")],
        ),
        finding(
            "P059-TD-009",
            "Shape and area verdict in plot_dqdv is print-only",
            "PRINT_ONLY_NUMERIC",
            "NOT_A_GATE",
            "The plotted shape predicate and area tolerance are passed to print rather than an assertion.",
            "A false verdict does not fail the process.",
            [(PLOT, 130, "spike ="), (PLOT, 131, "SHAPE OK")],
        ),
        finding(
            "P059-TD-010",
            "Thirty versioned blobs reduce to five unchanged logic families",
            "NORMALIZED_LINEAGE",
            "COPY_FORWARD",
            "After normalizing version/path-only strings, each of the five harness families has the same AST across six releases.",
            "v1.0.16 n(T) and v1.0.18.2 Einstein additions did not receive new dedicated harness logic.",
            [(SUITE, 6, "로직 무변경 원칙")],
        ),
        finding(
            "P059-TD-011",
            "No harness activates n_T1 or theta_E",
            "BRANCH_COVERAGE",
            "MISSING",
            "The complete test/demo corpus contains no n_T1 or theta_E token.",
            "The two headline post-v1.0.15 features are absent from these standard tests and demos.",
            [(SUITE, 17, "'n' 키 보유")],
        ),
        finding(
            "P059-TD-012",
            "Critical production-code branches are untested",
            "BRANCH_COVERAGE",
            "MISSING",
            "No harness enforces nonmonotone/reversal chronology, finite-window prehistory, direct-L_V zero-current behavior, missing n/w fallback, Q-cell unit conversion, or Einstein Tref positivity.",
            "The static code blockers from Step 34.1 can pass the historical suites.",
            [(REG, 25, "def graphite_outputs")],
        ),
        finding(
            "P059-TD-013",
            "No public experimental dataset is loaded",
            "EXTERNAL_VALIDITY",
            "ABSENT",
            "All inputs are synthetic linspace arrays and shipped literal dictionaries; there is no measured-data read path.",
            "The corpus cannot establish material validity, doped high-voltage LCO accuracy, or graphite/Si transferability.",
            [(REG, 27, "np.linspace"), (SAMPLE, 43, "np.linspace")],
        ),
        finding(
            "P059-TD-014",
            "PASS, DONE, and VALIDATION labels exceed enforced evidence",
            "AUTHORITY_LANGUAGE",
            "OVERCLAIMED",
            "Several scripts print completion or validation banners even when their numeric checks are report-only.",
            "Historical handovers can misread successful execution as scientific validation.",
            [(REG, 81, "PASS"), (DEMO, 73, "VALIDATION DONE"), (SUITE, 145, "DONE")],
        ),
        finding(
            "P059-TD-015",
            "Regression comparison ignores extra golden arrays",
            "INTERNAL_REGRESSION",
            "PARTIAL",
            "verify iterates current output keys only and never requires the golden key set to match exactly.",
            "Stale or extra golden arrays do not fail the gate.",
            [(REG, 71, "for k in out")],
        ),
    ]

    family_summary = {
        name: {
            "file_count": len(items),
            "assert_count": sum(item["assert_count"] for item in items),
            "print_count": sum(item["print_count"] for item in items),
            "exit_call_count": sum(len(item["exit_calls"]) for item in items),
            "array_equal_call_count": sum(
                len(item["array_equal_calls"]) for item in items
            ),
            "golden_read_call_count": sum(
                len(item["golden_read_calls"]) for item in items
            ),
            "golden_write_call_count": sum(
                len(item["golden_write_calls"]) for item in items
            ),
            "figure_write_call_count": sum(
                len(item["figure_write_calls"]) for item in items
            ),
            "logic_hashes": sorted(
                {item["logic_normalized_ast_sha256"] for item in items}
            ),
        }
        for name, items in sorted(families.items())
    }
    disposition_counts = Counter(item["disposition"] for item in findings)
    evidence_class_counts = Counter(item["evidence_class"] for item in findings)
    output = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": queue["baseline_commit"],
        "scope": "Phase 059 Step 34.2 all test/demo assertions, tolerances, I/O paths, and untested branches",
        "status": "PASS_P059_TEST_DEMO_ASSERTION_INVENTORY",
        "authority_boundary": (
            "Static test/demo evidence audit. Runtime results are Step 34.3; "
            "internal regression is not theory or experimental validation."
        ),
        "record_count": len(records),
        "test_record_count": sum(item["role"] == "test" for item in records),
        "demo_record_count": sum(item["role"] == "demo" for item in records),
        "total_line_count": sum(item["line_count"] for item in records),
        "total_assert_count": sum(item["assert_count"] for item in records),
        "logic_family_count": len(logic_groups),
        "logic_groups": [
            {"normalized_ast_sha256": key, "paths": value}
            for key, value in sorted(logic_groups.items())
        ],
        "family_summary": family_summary,
        "records": records,
        "finding_count": len(findings),
        "finding_disposition_counts": dict(sorted(disposition_counts.items())),
        "finding_evidence_class_counts": dict(
            sorted(evidence_class_counts.items())
        ),
        "findings": findings,
    }
    OUTPUT.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    family_rows = "\n".join(
        f"| {name} | {item['file_count']} | {item['assert_count']} | "
        f"{item['exit_call_count']} | {item['array_equal_call_count']} | "
        f"{item['golden_write_call_count']} | {item['figure_write_call_count']} |"
        for name, item in family_summary.items()
    )
    finding_rows = "\n".join(
        f"| {item['id']} | {item['evidence_class']} | "
        f"{item['disposition']} | {item['title']} | "
        + "; ".join(
            f"{Path(e['path']).name}:{e['line']}" for e in item["source_evidence"]
        )
        + " |"
        for item in findings
    )
    summary = f"""# Phase 059 test/demo assertion review

12 test blobs와 18 demo blobs 전부의 assertion, comparison, exit,
golden read/write, figure output, import path와 feature token을 AST로
검사했다. 이 단계는 정적 test-evidence 감사이며 runtime 결과가 아니다.

## 구조

- files: {len(records)} (test 12, demo 18)
- lines: {sum(item['line_count'] for item in records)}
- Python `assert`: {sum(item['assert_count'] for item in records)}
- version/path 문자열을 정규화하면 5 logic families × 각 6 releases다.

| Family | Files | Assert | Exit calls | array_equal | Golden writes | Figure writes |
|---|---:|---:|---:|---:|---:|---:|
{family_rows}

## 판정

| ID | Evidence class | Disposition | Finding | Source anchors |
|---|---|---|---|---|
{finding_rows}

## 핵심 결론

1. 실제 실패를 강제하는 것은 regression verify의 current-output
   array별 `np.array_equal`뿐이다. 이는 내부 baseline 보존이다.
2. regression의 area ratio는 출력만 하고 exit 상태에 반영하지
   않는다. capture는 golden을 덮어쓰므로 통제 없이 실행하면 안 된다.
3. sample, demo, graph suite, plot의 finite/parity/area/shape/expected
   값은 모두 출력 또는 그림일 뿐 gate가 아니다.
4. 30 versioned blobs는 5개 logic family의 경로/버전 복사다.
   `n_T1`과 `theta_E`를 활성화하는 표준 test/demo는 하나도 없다.
5. nonmonotone chronology, initial history, direct `L_V`의 $I=0$
   limit, default width derivative, C-rate unit, Einstein Tref와
   high-voltage doped LCO branch도 검사하지 않는다.
6. measured/public dataset을 읽는 경로가 없으므로 이 suite는
   external validity를 전혀 부여하지 않는다.

Gate: `PASS_P059_TEST_DEMO_ASSERTION_INVENTORY`.
"""
    SUMMARY.write_text(summary, encoding="utf-8")


if __name__ == "__main__":
    main()
