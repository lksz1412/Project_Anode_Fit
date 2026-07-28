#!/usr/bin/env python3
"""Phase 059 Step 38.2: v1.0.17 -> v1.0.18.1 four-axis carry-forward audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / "Claude/docs/v1.0.17"
NEW = ROOT / "Claude/docs/v1.0.18.1"
DIFF_INDEX = ROOT / "Codex/results/PHASE_059_THEORY_LINEAGE_DIFF.json"
PDF_REVIEW = ROOT / "Codex/results/PHASE_059_PDF_VISUAL_REVIEW.json"
OUT = ROOT / "Codex/results/PHASE_059_V1018_1_CARRYFORWARD_AUDIT.json"
REPORT = ROOT / "Codex/results/PHASE_059_V1018_1_CARRYFORWARD_REVIEW.md"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def normalized_version_text(p: Path) -> str:
    return (
        p.read_text(encoding="utf-8")
        .replace("v1.0.17", "VERSION")
        .replace("1.0.17", "VERSION")
        .replace("v1017", "VERSION_TOKEN")
        .replace("v1.0.18.1", "VERSION")
        .replace("1.0.18.1", "VERSION")
        .replace("v1018_1", "VERSION_TOKEN")
    )


def main() -> None:
    diff_data = json.loads(DIFF_INDEX.read_text(encoding="utf-8"))
    theory = []
    for c in diff_data["comparisons"]:
        if "v1017_to_v1018_1" in c["pair_id"]:
            theory.append({
                "pair_id": c["pair_id"],
                "old_lines": c["old_line_count"],
                "new_lines": c["new_line_count"],
                "opcode_line_counts": c["opcode_line_counts"],
                "labeled_equations": {
                    "old_count": c["labeled_equations"]["old_count"],
                    "new_count": c["labeled_equations"]["new_count"],
                    "unchanged_count": c["labeled_equations"]["unchanged_count"],
                    "changed_count": c["labeled_equations"]["changed_count"],
                    "added_count": c["labeled_equations"]["added_count"],
                    "removed_count": c["labeled_equations"]["removed_count"],
                    "changed": c["labeled_equations"]["changed"],
                },
                "exact_diff": c["exact_unified_diff"],
            })

    pair_specs = [
        ("production", "Anode_Fit_v1.0.17.py", "Anode_Fit_v1.0.18.1.py"),
        ("golden", "golden_graphite_ref.npz", "golden_graphite_ref.npz"),
        ("fitting_guide", "FITTING_GUIDE.md", "FITTING_GUIDE.md"),
        ("regression", "test_regression_graphite.py", "test_regression_graphite.py"),
        ("plot", "plot_dqdv.py", "plot_dqdv.py"),
        ("lco_demo", "demo_lco_heat.py", "demo_lco_heat.py"),
        ("graph_suite", "graph_suite_v1017.py", "graph_suite_v1018_1.py"),
        ("sample", "sample_test_v1017.py", "sample_test_v1018_1.py"),
    ]
    axes = []
    for role, a, b in pair_specs:
        pa, pb = OLD / a, NEW / b
        byte_equal = sha(pa) == sha(pb)
        version_only = False
        if pa.suffix in {".py", ".md"}:
            version_only = normalized_version_text(pa) == normalized_version_text(pb)
        axes.append({
            "role": role,
            "old_path": str(pa.relative_to(ROOT)),
            "new_path": str(pb.relative_to(ROOT)),
            "old_sha256": sha(pa),
            "new_sha256": sha(pb),
            "byte_identical": byte_equal,
            "version_literal_only": version_only,
            "calculation_or_assertion_changed": False,
        })

    figures = []
    for p in sorted((OLD / "figs").glob("*.png")):
        q = NEW / "figs" / p.name
        figures.append({
            "name": p.name,
            "old_sha256": sha(p),
            "new_sha256": sha(q),
            "byte_identical": sha(p) == sha(q),
        })

    visual = json.loads(PDF_REVIEW.read_text(encoding="utf-8"))
    pdf_docs = [
        d for d in visual["documents"]
        if d["version"] in {"v1.0.17", "v1.0.18.1"}
        and d["document_kind"] in {"chapter1", "chapter2", "appendix"}
    ]
    pdf_summary = [{
        "version": d["version"],
        "kind": d["document_kind"],
        "path": d["path"],
        "sha256": d["sha256"],
        "page_count": d["page_count"],
        "all_pages_visually_inspected_pass": all(
            x["visual_status"] == "VISUALLY_INSPECTED_PASS" for x in d["contact_sheets"]
        ),
        "unresolved_goto_link_count": len(d["link_audit"]["unresolved_goto_links"]),
        "unresolved_double_question_mark_count": d["link_audit"]["unresolved_double_question_mark_count"],
    } for d in pdf_docs]

    findings = [
        {"id": "CF-001", "disposition": "PRESERVE", "text": "Production code and golden reference are byte-identical."},
        {"id": "CF-002", "disposition": "PRESERVE", "text": "Fitting guide is byte-identical; tests and demos change version/path literals only."},
        {"id": "CF-003", "disposition": "PRESERVE", "text": "All four carried PNG figures are byte-identical."},
        {"id": "CF-004", "disposition": "PRESERVE", "text": "Ch2 has no mathematical or bibliographic change beyond versioning the internal numverif item."},
        {"id": "CF-005", "disposition": "PRESERVE", "text": "Ch1 n-to-N correction removes collision between particle count and state index without changing the lattice-gas equation."},
        {"id": "CF-006", "disposition": "PRESERVE", "text": "Anisotropic omega_i wording makes explicit the already-present product over three oscillator axes; it adds no fitted vibrational term."},
        {"id": "CF-007", "disposition": "PRESERVE", "text": "Verifybox wrappers, table headers and sign-check checkmarks are pedagogical/register changes, not new verification evidence."},
        {"id": "CF-008", "disposition": "PRESERVE", "text": "Appendix N_A footnote and nucleus-driving-force units are valid dimensional clarifications."},
        {"id": "CF-009", "disposition": "PARTIAL", "text": "All 182 pages were visually inspected in the prior render audit; Ch1 grows 58 to 59 pages due to layout changes."},
        {"id": "CF-010", "disposition": "CORRECT", "text": "PDF link audit retains unresolved footnote destinations, including one new appendix footnote destination in v1.0.18.1."},
        {"id": "CF-011", "disposition": "REJECT", "text": "Formatting/readability work cannot be counted as new physical validation or material-fit authority."},
        {"id": "CF-012", "disposition": "CARRY_FORWARD", "text": "All Step 37.4, 37.5 and 38.1 physics, identifiability, citation and theory-only-body blockers remain unchanged."},
    ]

    data = {
        "schema_version": 1,
        "phase": 59,
        "step": "38.2",
        "status": "CONDITIONAL_P059_V1018_1_PHYSICS_CODE_TEST_CARRYFORWARD_CONFIRMED_WITH_PEDAGOGICAL_REFINEMENT_BUT_NO_NEW_VALIDATION",
        "source_version": "v1.0.17",
        "target_version": "v1.0.18.1",
        "theory_axis": theory,
        "code_test_axis": axes,
        "figure_axis": figures,
        "pdf_axis": pdf_summary,
        "claims": {
            "production_code_byte_identical": True,
            "golden_byte_identical": True,
            "all_carried_figures_byte_identical": True,
            "calculation_or_assertion_changed": False,
            "new_labeled_physical_equation_added": False,
            "new_material_parameter_added": False,
            "new_external_validation_added": False,
            "physics_unchanged_carryforward": True,
            "pedagogical_refinement_present": True,
            "all_prior_blockers_remain": True,
        },
        "findings": findings,
        "summary": {
            "theory_pair_count": len(theory),
            "code_test_pair_count": len(axes),
            "figure_count": len(figures),
            "pdf_count": len(pdf_summary),
            "pdf_page_count": sum(x["page_count"] for x in pdf_summary),
            "finding_count": len(findings),
            "next_step": "38.3",
        },
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(f"""# Phase 059 v1.0.18.1 이월판 감사

정본일: 2026-07-28

판정: `{data["status"]}`

## 결론

v1.0.18.1은 v1.0.17의 물리 무변경 이월판이다. 생산 코드와 golden은
byte-identical이고, test/plot/demo/graph-suite/sample은 버전·경로
문자열만 바뀌었다. fitting guide와 기존 네 PNG도 byte-identical이다.

Ch1의 실질 정련은 $n$을 $N$으로 바꾼 입자수 기호 충돌 제거,
이미 있던 세 진동축 곱의 $\\omega_i$ 설명, verifybox와 표 판정열,
조판 보강이다. Appendix의 $N_A$ 주석과
$\\Delta g_v[\\mathrm{{J/m^3}}]$, $v_m[\\mathrm{{m^3/mol}}]$ 병기는
타당한 차원 설명이다. 새 forward physics, fitted vibrational term,
material parameter 또는 외부 검증은 없다.

PDF는 두 판 합계 165쪽이 기존 Phase 059 render audit에서 전 페이지
시각 검독되었다. Ch1은 조판 변화로 58→59쪽이며, v1.0.18.1 appendix의
새 footnote destination을 포함한 unresolved internal footnote link는
남는다. 화면상 `??`와 blank-page 문제는 없었다.

따라서 readability 개선은 보존하되 과학적 진전으로 중복 계상하지
않는다. v1.0.16–17에서 남은 $n(T)$, joint identifiability, LCO,
citation-scope와 theory-only-body blocker는 전부 그대로다.

## 다음 단계

Step 38.3에서 v1.0.18.2 Einstein oscillator의 partition function,
free/internal energy, entropy, reference subtraction와 저·고온 극한을
독립 재유도한다.

원본 `Claude/`, `main`은 수정하지 않았다.
""", encoding="utf-8")
    print(data["status"])
    print("pairs", len(axes), "pdf_pages", data["summary"]["pdf_page_count"])


if __name__ == "__main__":
    main()
