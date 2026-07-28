#!/usr/bin/env python3
"""Adjudicate the v1.0.13 -> v1.0.14 manuscript restructuring.

This Step 36.1 audit measures exact source changes, the theory/implementation
boundary, and the semantic role of the new width budget.  It does not edit the
historical manuscript and does not promote its equations to final canon.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
DIFF_DATA = RESULTS / "PHASE_059_THEORY_LINEAGE_DIFF.json"
OUTPUT = RESULTS / "PHASE_059_V1014_REGISTER_BOUNDARY_AUDIT.json"
REPORT = RESULTS / "PHASE_059_V1014_REGISTER_BOUNDARY_REVIEW.md"

DOCUMENTS = {
    "ch1_v1013": ROOT
    / "Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex",
    "ch1_v1014": ROOT
    / "Claude/docs/v1.0.14/graphite_ica_ch1_v1.0.14.tex",
    "ch2_v1013": ROOT
    / "Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex",
    "ch2_v1014": ROOT
    / "Claude/docs/v1.0.14/graphite_ica_ch2_v1.0.14.tex",
}

DIRECT_IDENTIFIER_PATTERNS = [
    re.compile(r"\\code\{"),
    re.compile(r"\\texttt\{"),
    re.compile(r"\bAnode_Fit\b"),
    re.compile(r"\bdict\b"),
    re.compile(r"\bself-test\b", re.IGNORECASE),
]
GENERIC_IMPLEMENTATION_PATTERNS = [
    re.compile(r"코드"),
    re.compile(r"구현"),
    re.compile(r"\bfacade\b", re.IGNORECASE),
]

PHYSICS_EQUATION_CHANGES = {
    "eq:partfn": "single-site grand partition function with internal q(T)",
    "eq:fermifn": "explicit effective chemical-potential difference",
    "eq:sm-factor": "grand-partition notation consistency",
    "eq:sm-mucount": "effective site free energy",
    "eq:sm-occmid": "occupation expression with internal-state contribution",
}
IMPLEMENTATION_BOUNDARY_EQUATION_CHANGES = {
    "eq:LV": "removed code identifier from displayed equation",
    "eq:branch": "typographic code-name cleanup only",
    "eq:peakshape": "typographic code-name cleanup only",
    "eq:reversal": "replaced literal code call by abstract operators",
    "eq:sum": "removed implementation identifier from aggregation equation",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_comment(line: str) -> str:
    """Remove TeX comments while respecting escaped percent signs."""
    for index, char in enumerate(line):
        if char != "%":
            continue
        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        if backslashes % 2 == 0:
            return line[:index]
    return line


def rendered_source_lines(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    records = []
    allowed_code_section = False
    for line_number, raw in enumerate(lines, 1):
        line = strip_comment(raw).strip()
        if not line:
            continue
        if "\\section{구현 대응표}" in line:
            allowed_code_section = True
        if "\\begin{thebibliography}" in line:
            allowed_code_section = False
        # Macro and environment declarations are source machinery, not
        # rendered prose.  Metadata/title/header/date remain in scope.
        if line.startswith("\\newcommand") or line.startswith("\\newtheorem"):
            continue
        records.append(
            {
                "line": line_number,
                "text": line,
                "inside_allowed_code_section": allowed_code_section,
            }
        )
    return records


def implementation_mentions(path: Path) -> dict:
    records = rendered_source_lines(path)
    findings = []
    for record in records:
        direct = [
            pattern.pattern
            for pattern in DIRECT_IDENTIFIER_PATTERNS
            if pattern.search(record["text"])
        ]
        generic = [
            pattern.pattern
            for pattern in GENERIC_IMPLEMENTATION_PATTERNS
            if pattern.search(record["text"])
        ]
        if not direct and not generic:
            continue
        item = dict(record)
        item["direct_identifier_patterns"] = direct
        item["generic_implementation_patterns"] = generic
        navigation_only = (
            not direct
            and (
                "appendix-code" in record["text"]
                or "구현 대응" in record["text"]
            )
        )
        item["classification"] = (
            "ALLOWED_DEDICATED_IMPLEMENTATION_SECTION"
            if record["inside_allowed_code_section"]
            else (
                "OUTSIDE_NAVIGATIONAL_REFERENCE_ALLOWED"
                if navigation_only
                else (
                    "OUTSIDE_DIRECT_IMPLEMENTATION_CONTENT"
                    if direct
                    else "OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING"
                )
            )
        )
        findings.append(item)
    outside = [
        item
        for item in findings
        if not item["inside_allowed_code_section"]
    ]
    allowed = [
        item for item in findings if item["inside_allowed_code_section"]
    ]
    return {
        "path": str(path.relative_to(ROOT)),
        "rendered_noncomment_line_count": len(records),
        "mention_count": len(findings),
        "outside_mention_count": len(outside),
        "outside_navigation_reference_count": sum(
            item["classification"]
            == "OUTSIDE_NAVIGATIONAL_REFERENCE_ALLOWED"
            for item in outside
        ),
        "outside_boundary_violation_count": sum(
            item["classification"]
            != "OUTSIDE_NAVIGATIONAL_REFERENCE_ALLOWED"
            for item in outside
        ),
        "outside_direct_identifier_line_count": sum(
            item["classification"] == "OUTSIDE_DIRECT_IMPLEMENTATION_CONTENT"
            for item in outside
        ),
        "outside_generic_framing_line_count": sum(
            item["classification"]
            == "OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING"
            for item in outside
        ),
        "inside_allowed_section_count": len(allowed),
        "outside_allowed_section": outside,
        "inside_allowed_section": allowed,
    }


def comparison(diff_data: dict, pair_id: str) -> dict:
    item = next(
        entry
        for entry in diff_data["comparisons"]
        if entry["pair_id"] == pair_id
    )
    equations = item["labeled_equations"]
    return {
        "pair_id": pair_id,
        "old_path": item["old_path"],
        "new_path": item["new_path"],
        "old_line_count": item["old_line_count"],
        "new_line_count": item["new_line_count"],
        "net_line_change": item["new_line_count"] - item["old_line_count"],
        "sequence_ratio": item["sequence_ratio"],
        "opcode_line_counts": item["opcode_line_counts"],
        "section_old_count": item["sections"]["old_count"],
        "section_new_count": item["sections"]["new_count"],
        "added_sections": item["sections"]["added"],
        "removed_sections": item["sections"]["removed"],
        "equation_old_count": equations["old_count"],
        "equation_new_count": equations["new_count"],
        "equation_unchanged_count": equations["unchanged_count"],
        "equation_changed_count": equations["changed_count"],
        "equation_added_count": equations["added_count"],
        "equation_removed_count": equations["removed_count"],
        "equation_changed_labels": [
            entry["label"] for entry in equations["changed"]
        ],
        "equation_added_labels": [
            entry["label"] for entry in equations["added"]
        ],
        "equation_removed_labels": [
            entry["label"] for entry in equations["removed"]
        ],
        "exact_unified_diff": item["exact_unified_diff"],
        "exact_unified_diff_sha256": item["exact_unified_diff_sha256"],
    }


def equation_change_dispositions(ch1: dict, ch2: dict) -> list[dict]:
    records = []
    for label in ch1["equation_changed_labels"]:
        if label in PHYSICS_EQUATION_CHANGES:
            records.append(
                {
                    "document": "ch1",
                    "label": label,
                    "class": "PHYSICS_DERIVATION_CHANGE",
                    "basis": PHYSICS_EQUATION_CHANGES[label],
                }
            )
        else:
            records.append(
                {
                    "document": "ch1",
                    "label": label,
                    "class": "IMPLEMENTATION_BOUNDARY_OR_NOTATION_CHANGE",
                    "basis": IMPLEMENTATION_BOUNDARY_EQUATION_CHANGES[label],
                }
            )
    for label in ch1["equation_added_labels"]:
        records.append(
            {
                "document": "ch1",
                "label": label,
                "class": (
                    "PHYSICS_DERIVATION_ADDITION"
                    if label
                    in {
                        "eq:sm-epstilde",
                        "eq:sm-sint",
                        "eq:widthbudget",
                        "eq:psdconv",
                        "eq:gibbsthomson",
                    }
                    else "UNCLASSIFIED_ADDITION"
                ),
                "basis": {
                    "eq:sm-epstilde": "effective site free energy",
                    "eq:sm-sint": "internal-state entropy bridge",
                    "eq:widthbudget": "symmetric variance budget",
                    "eq:psdconv": "particle-size ensemble response",
                    "eq:gibbsthomson": "size-induced equilibrium shift",
                }.get(label, "requires review"),
            }
        )
    for label in ch2["equation_changed_labels"]:
        records.append(
            {
                "document": "ch2",
                "label": label,
                "class": "CROSS_CHAPTER_NOTATION_AND_RIGOR_CHANGE",
                "basis": (
                    "Z1 -> Xi1 grand-canonical notation and effective "
                    "single-site free-energy bridge"
                ),
            }
        )
    return records


def decisions() -> list[dict]:
    return [
        {
            "id": "V1014-36.1-01",
            "topic": "textbook_register",
            "disposition": "PRESERVE_ASSET_NOT_FINAL_AUTHORITY",
            "finding": (
                "The single-site derivation now exposes the grand partition "
                "function, internal q(T), effective site free energy, limiting "
                "cases, and the Ch1/Ch2 bridge; this is a real pedagogical gain."
            ),
            "final_direction": (
                "Preserve the derivational ladder but rederive and source-audit "
                "it before the final manuscript."
            ),
        },
        {
            "id": "V1014-36.1-02",
            "topic": "review_depth",
            "disposition": "PARTIAL",
            "finding": (
                "Ch1 adds broadening mechanisms, a variance budget, PSD "
                "forward integration, and Gibbs-Thomson exclusion, but Ch2 "
                "changes only 18 net lines and no new equation."
            ),
            "final_direction": (
                "Treat v1.0.14 as a Ch1-rich editorial/derivational asset, not "
                "as proof that the two-chapter review-depth target was met."
            ),
        },
        {
            "id": "V1014-36.1-03",
            "topic": "theory_only_boundary",
            "disposition": "FAIL_REQUIRES_CORRECTION",
            "finding": (
                "A dedicated implementation appendix was created, yet rendered "
                "title/header/date and body prose still contain code-first "
                "framing, current-code state, dict, and self-test language."
            ),
            "final_direction": (
                "Allow exact identifiers only in a separately bounded "
                "conformance appendix; remove code-first framing and current "
                "implementation claims from the physics chapters."
            ),
        },
        {
            "id": "V1014-36.1-04",
            "topic": "one_way_theory_to_code",
            "disposition": "PARTIAL",
            "finding": (
                "Moving identifier tables and snippets into one appendix is "
                "structurally correct, but the main text still explains itself "
                "through implementation state rather than only physical logic."
            ),
            "final_direction": (
                "The final code must cite equation/contract IDs; the manuscript "
                "must not derive authority from code behavior."
            ),
        },
        {
            "id": "V1014-36.1-05",
            "topic": "width_budget",
            "disposition": "CORRECT_ROLE_SPLIT_REQUIRED",
            "finding": (
                "Variance addition and the logistic variance/FWHM identities "
                "are mathematically coherent under independent convolution. "
                "However w_j is first the intrinsic nRT/F scale and later the "
                "fitted effective width that already absorbs intrinsic plus "
                "ensemble broadening, so adding sigma_eta can double count."
            ),
            "final_direction": (
                "Use distinct w_int(T), sigma_ens(T,state), and observed/effective "
                "width symbols; let the observation operator combine them once."
            ),
        },
        {
            "id": "V1014-36.1-06",
            "topic": "scientific_validation",
            "disposition": "UNVERIFIED",
            "finding": (
                "The source contains internal numerical-validation and "
                "measurement-grade language but this diff supplies neither "
                "external experimental overlays nor uncertainty."
            ),
            "final_direction": (
                "Keep internal identities as unit tests and reserve validation "
                "language for versioned public data, residuals, uncertainty, "
                "and held-out conditions."
            ),
        },
    ]


def report_text(result: dict) -> str:
    ch1 = result["comparisons"]["ch1"]
    ch2 = result["comparisons"]["ch2"]
    v14_ch1 = result["implementation_boundary"]["ch1_v1014"]
    v14_ch2 = result["implementation_boundary"]["ch2_v1014"]
    leak_rows = "\n".join(
        f"| {item['line']} | {item['classification']} | "
        f"`{item['text'][:160].replace('|', '/')}` |"
        for item in (
            v14_ch1["outside_allowed_section"]
            + v14_ch2["outside_allowed_section"]
        )
    )
    decision_rows = "\n".join(
        f"| {item['id']} | {item['topic']} | {item['disposition']} | "
        f"{item['finding']} |"
        for item in result["decisions"]
    )
    return f"""# Phase 059 v1.0.14 register·본문 경계 재판정

정본일: 2026-07-28

판정: `{result['status']}`

## 결론

v1.0.14는 v1.0.13보다 분명히 나아졌다. Ch1은 단일 자리
대정준 유도를 내부 자유도 $q(T)$와 유효 자리 자유에너지까지
확장하고, broadening 폭 예산과 PSD/Gibbs--Thomson 배제 논리를
식으로 추가했다. 이것은 보존할 교재 자산이다.

그러나 “교재·리뷰 깊이·theory-only 경계를 완결했다”는 주장은
성립하지 않는다. Ch2의 순증은 {ch2['net_line_change']}행이고 새
displayed equation은 0개다. 더 결정적으로 Ch1에 구현 대응 부록을
만들고도 제목·헤더·날짜·본문에 코드 진행, 현 코드, `dict`,
self-test가 남는다. 따라서 v1.0.14는 최종 정본이 아니라
`PRESERVE_ASSET + CORRECT_BOUNDARY` 대상이다.

## Exact diff 규모

| document | lines old→new | net | equations unchanged/changed/added | sequence ratio |
|---|---:|---:|---:|---:|
| Ch1 | {ch1['old_line_count']}→{ch1['new_line_count']} | +{ch1['net_line_change']} | {ch1['equation_unchanged_count']}/{ch1['equation_changed_count']}/{ch1['equation_added_count']} | {ch1['sequence_ratio']:.3f} |
| Ch2 | {ch2['old_line_count']}→{ch2['new_line_count']} | +{ch2['net_line_change']} | {ch2['equation_unchanged_count']}/{ch2['equation_changed_count']}/{ch2['equation_added_count']} | {ch2['sequence_ratio']:.3f} |

Ch1의 changed equation 10개 중 5개는 실제 통계역학 유도 변경,
5개는 code identifier를 추상 물리/연산 표기로 바꾼 경계 정리다.
신규 식 5개는 $\\tilde\\varepsilon$, 내부 자유도 엔트로피, 폭 예산,
PSD 적분, Gibbs--Thomson 이동이다. Ch2의 changed equation 2개는
$Z_1\\to\\Xi_1$ 대정준 표기와 같은 단일자리 bridge의 엄밀화다.

## Theory-only 경계

v1.0.14 Ch1의 구현 관련 rendered lines는 전용 구현 부록 안
{v14_ch1['inside_allowed_section_count']}개다. 부록 밖 mention은
{v14_ch1['outside_mention_count']}개이고, 그중 전용 부록으로 보내는
navigation {v14_ch1['outside_navigation_reference_count']}개를 제외한
boundary violation은 {v14_ch1['outside_boundary_violation_count']}개다.
Ch2에는 전용 구현 절이 없으며 violation
{v14_ch2['outside_boundary_violation_count']}개가 남는다.
v1.0.13의 두 장 합계 violation
{result['summary']['v1013_outside_boundary_violation_count']}개에서
v1.0.14의 {result['summary']['v1014_outside_boundary_violation_count']}개로
크게 줄인 것은 실제 개선이지만 0은 아니다. 아래 표는 comments와
TeX macro 정의를 제외한 rendered source만 센 것이다.

| line | class | source excerpt |
|---:|---|---|
{leak_rows}

부록을 참조한다는 일반 문장은 탐색성을 위해 허용할 수 있다. 그러나
코드-first 제목, 현재 구현의 parameter state, `dict`, self-test와
내부 code artifact를 물리 근거처럼 쓰는 문장은 최종 이론 본문에서
제거해야 한다.

## 폭 예산의 판정

새 식의
$\\sigma_\\mathrm{{sym}}^2=\\pi^2w_\\mathrm{{int}}^2/3+
\\sigma_\\eta^2$는 독립 대칭 convolution의 분산 가법으로 타당하고,
logistic 분포의 $\\sigma=\\pi w/\\sqrt3$, FWHM
$=2\\ln(3+2\\sqrt2)w$도 맞다.

문제는 같은 $w_j$를 두 역할로 쓴다는 점이다.

1. 식 안에서는 $w_j=n_jRT/F$인 내재 열폭이다.
2. 이어지는 문장에서는 fitted $w_j$가 내재폭과 ensemble 폭을 이미
   함께 흡수하는 관측 유효폭이다.

둘을 동시에 쓰고 $\\sigma_\\eta$를 다시 더하면 이중계산 가능성이
생긴다. 최종 이론은 $w_\\mathrm{{int}}$, $\\sigma_\\mathrm{{ens}}$,
$L_V$, $w_\\mathrm{{obs}}$를 분리하고 observation operator에서
한 번만 합성해야 한다.

## 판정표

| ID | topic | disposition | finding |
|---|---|---|---|
{decision_rows}

## 다음 단계

Step 36.2에서 v1.0.14 phase-separation appendix의 regular solution,
spinodal, Cahn--Hilliard, gradient coefficient와 mobility 식을
독립 재유도해 단위·안정성·선형화·경계조건을 검산한다.
"""


def main() -> int:
    source_hashes_before = {
        name: sha256(path) for name, path in DOCUMENTS.items()
    }
    diff_data = json.loads(DIFF_DATA.read_text(encoding="utf-8"))
    ch1 = comparison(diff_data, "ch1_v1013_to_v1014")
    ch2 = comparison(diff_data, "ch2_v1013_to_v1014")
    boundaries = {
        name: implementation_mentions(path)
        for name, path in DOCUMENTS.items()
    }
    source_hashes_after = {
        name: sha256(path) for name, path in DOCUMENTS.items()
    }
    result = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "scope": (
            "Phase 059 Step 36.1 v1.0.13 to v1.0.14 textbook "
            "register, derivation restructuring, width-budget semantics, "
            "and theory-only boundary"
        ),
        "authority_boundary": (
            "Historical manuscript adjudication only; equations and citations "
            "are not promoted to final theory or external validation."
        ),
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "sources_unchanged": source_hashes_before == source_hashes_after,
        "comparisons": {"ch1": ch1, "ch2": ch2},
        "equation_change_dispositions": equation_change_dispositions(ch1, ch2),
        "implementation_boundary": boundaries,
        "width_budget_contract": {
            "intrinsic_variance_identity": (
                "sigma_int^2 = pi^2 w_int^2 / 3"
            ),
            "symmetric_convolution_identity": (
                "sigma_sym^2 = sigma_int^2 + sigma_ens^2"
            ),
            "logistic_fwhm_identity": (
                "FWHM = 2 ln(3 + 2 sqrt(2)) w_int"
            ),
            "identity_disposition": "PRESERVE",
            "semantic_defect": (
                "The same w_j is used as intrinsic n_jRT/F and as an "
                "effective fitted width already absorbing ensemble broadening."
            ),
            "semantic_disposition": "CORRECT_ROLE_SPLIT_REQUIRED",
            "required_final_symbols": [
                "w_int(T,state)",
                "sigma_ens(T,state)",
                "L_V(T,I,state,history)",
                "w_obs",
            ],
        },
        "decisions": decisions(),
        "summary": {
            "ch1_net_line_change": ch1["net_line_change"],
            "ch2_net_line_change": ch2["net_line_change"],
            "ch1_equation_changed_count": ch1["equation_changed_count"],
            "ch1_equation_added_count": ch1["equation_added_count"],
            "ch2_equation_changed_count": ch2["equation_changed_count"],
            "ch2_equation_added_count": ch2["equation_added_count"],
            "physics_derivation_changed_equation_count": sum(
                item["class"] == "PHYSICS_DERIVATION_CHANGE"
                for item in equation_change_dispositions(ch1, ch2)
            ),
            "implementation_boundary_changed_equation_count": sum(
                item["class"]
                == "IMPLEMENTATION_BOUNDARY_OR_NOTATION_CHANGE"
                for item in equation_change_dispositions(ch1, ch2)
            ),
            "physics_derivation_added_equation_count": sum(
                item["class"] == "PHYSICS_DERIVATION_ADDITION"
                for item in equation_change_dispositions(ch1, ch2)
            ),
            "v1014_outside_allowed_implementation_line_count": (
                boundaries["ch1_v1014"]["outside_mention_count"]
                + boundaries["ch2_v1014"]["outside_mention_count"]
            ),
            "v1014_outside_navigation_reference_count": (
                boundaries["ch1_v1014"][
                    "outside_navigation_reference_count"
                ]
                + boundaries["ch2_v1014"][
                    "outside_navigation_reference_count"
                ]
            ),
            "v1014_outside_boundary_violation_count": (
                boundaries["ch1_v1014"]["outside_boundary_violation_count"]
                + boundaries["ch2_v1014"]["outside_boundary_violation_count"]
            ),
            "v1013_outside_boundary_violation_count": (
                boundaries["ch1_v1013"]["outside_boundary_violation_count"]
                + boundaries["ch2_v1013"]["outside_boundary_violation_count"]
            ),
            "v1014_inside_allowed_implementation_line_count": (
                boundaries["ch1_v1014"]["inside_allowed_section_count"]
                + boundaries["ch2_v1014"]["inside_allowed_section_count"]
            ),
            "decision_count": len(decisions()),
            "theory_only_boundary_pass": False,
        },
        "status": (
            "CONDITIONAL_P059_V1014_PEDAGOGICAL_ASSET_WITH_"
            "THEORY_BOUNDARY_AND_WIDTH_ROLE_DEBTS"
        ),
        "next_action": (
            "Run Step 36.2 independent regular-solution, spinodal, "
            "Cahn-Hilliard, gradient, mobility, and boundary-condition "
            "rederivation."
        ),
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    REPORT.write_text(report_text(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "report": str(REPORT.relative_to(ROOT)),
                "status": result["status"],
                "summary": result["summary"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
