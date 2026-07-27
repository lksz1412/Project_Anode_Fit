#!/usr/bin/env python3
"""Build the Phase 058 theory source index and seed equation/claim matrix.

This script is intentionally read-only with respect to the historical sources.
It extracts structure and equation locations from the six unique TeX blobs and
writes audit artifacts only under Codex/results.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"

THEORY_PATHS = [
    "Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex",
    "Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex",
    "Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex",
    "Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex",
    "Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex",
    "Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex",
]

SECTION_RE = re.compile(
    r"\\(?P<level>section|subsection|subsubsection)\*?"
    r"\{(?P<title>.*?)\}(?:\\label\{(?P<label>[^}]+)\})?"
)
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
BEGIN_EQ_RE = re.compile(
    r"\\begin\{(?P<env>equation\*?|align\*?|gather\*?|multline\*?)\}"
)
END_EQ_TEMPLATE = r"\\end\{%s\}"


def version_for(path: str) -> str:
    return re.search(r"v1\.0\.\d+", path).group(0)  # type: ignore[union-attr]


def chapter_for(path: str) -> str:
    return "ch1" if "_ch1_" in path else "ch2"


def compact(text: str, limit: int = 340) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    return value if len(value) <= limit else value[: limit - 1] + "…"


def classify_equation(body: str, section_title: str) -> str:
    haystack = f"{section_title} {body}".lower()
    rules = [
        ("observation_and_fitting", ("dqdv", "d q", "peak", "fitting", "피팅")),
        ("thermal_and_entropy", ("entropy", "엔트로피", "s_", "q_rev", "partial u", "partial v")),
        ("hysteresis_and_kinetics", ("hys", "lag", "eyring", "k_j", "activation", "장벽", "저역")),
        ("lco_extension", ("lco", "cat", "mit", "g(e_f", "msmr")),
        ("peak_kernel_and_broadening", ("xi(1-", "xi_j(1-", "width", "broadening", "폭")),
        ("equilibrium_and_statistical_mechanics", ("omega", "partition", "logistic", "theta", "mu", "g(")),
        ("coordinate_and_conservation", ("q_cell", "q_\\cell", "sum_j", "sigma_d", "v_\\app")),
    ]
    for category, needles in rules:
        if any(needle in haystack for needle in needles):
            return category
    return "unclassified_manual_review"


def parse_document(path: str) -> dict:
    source = ROOT / path
    raw = source.read_bytes()
    text = raw.decode("utf-8")
    lines = text.splitlines()

    sections: list[dict] = []
    current_section = {
        "level": "document",
        "title": "preamble/introduction",
        "label": None,
        "line": 1,
    }
    equations: list[dict] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        section_match = SECTION_RE.search(line)
        if section_match:
            current_section = {
                "level": section_match.group("level"),
                "title": compact(section_match.group("title"), 220),
                "label": section_match.group("label"),
                "line": i + 1,
            }
            sections.append(dict(current_section))

        begin = BEGIN_EQ_RE.search(line)
        if begin:
            env = begin.group("env")
            start = i
            end_re = re.compile(END_EQ_TEMPLATE % re.escape(env))
            j = i
            while j < len(lines) and not end_re.search(lines[j]):
                j += 1
            if j >= len(lines):
                j = i
            body = "\n".join(lines[start : j + 1])
            labels = LABEL_RE.findall(body)
            equations.append(
                {
                    "equation_id": (
                        f"{version_for(path)}:{chapter_for(path)}:"
                        f"{labels[0] if labels else 'unlabeled-L' + str(start + 1)}"
                    ),
                    "path": path,
                    "version": version_for(path),
                    "chapter": chapter_for(path),
                    "line_start": start + 1,
                    "line_end": j + 1,
                    "environment": env,
                    "labels": labels,
                    "section": dict(current_section),
                    "category": classify_equation(body, current_section["title"]),
                    "source_excerpt": compact(body),
                    "source_read_status": "COMPLETE",
                    "physical_adjudication": "PENDING_INDEPENDENT_DERIVATION",
                    "code_conformance": "PENDING_STEP_27",
                    "external_validity": "PENDING_LITERATURE_AUDIT",
                }
            )
            i = j
        i += 1

    code_token_count = len(re.findall(r"\\(?:code|texttt)\{", text))
    citation_count = len(re.findall(r"\\cite\{", text))
    return {
        "path": path,
        "version": version_for(path),
        "chapter": chapter_for(path),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "line_count": len(lines),
        "read_coverage": [[1, len(lines)]],
        "read_status": "COMPLETE",
        "section_count": len(sections),
        "equation_environment_count": len(equations),
        "code_identifier_token_count": code_token_count,
        "citation_command_count": citation_count,
        "sections": sections,
        "equations": equations,
    }


def main() -> None:
    documents = [parse_document(path) for path in THEORY_PATHS]
    equations = [eq for doc in documents for eq in doc["equations"]]
    category_counts = Counter(eq["category"] for eq in equations)

    matrix = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "scope": "Phase 058 Step 26 theory source structure and equation inventory",
        "status": "SOURCE_READ_COMPLETE; INDEPENDENT_ADJUDICATION_IN_PROGRESS",
        "source_boundary": (
            "Historical TeX is evidence, not current theory canon. Code references "
            "are counted as a boundary violation under the current user direction."
        ),
        "document_count": len(documents),
        "total_lines": sum(doc["line_count"] for doc in documents),
        "equation_environment_count": len(equations),
        "equation_category_counts": dict(sorted(category_counts.items())),
        "documents": documents,
        "equations": equations,
    }
    output = RESULTS / "PHASE_058_THEORY_EQUATION_CLAIM_MATRIX.json"
    output.write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rows = []
    for doc in documents:
        rows.append(
            "| {version} | {chapter} | {lines} | {sections} | {equations} | "
            "{code_tokens} | {citations} | COMPLETE |".format(
                version=doc["version"],
                chapter=doc["chapter"],
                lines=doc["line_count"],
                sections=doc["section_count"],
                equations=doc["equation_environment_count"],
                code_tokens=doc["code_identifier_token_count"],
                citations=doc["citation_command_count"],
            )
        )
    index_text = """# Phase 058 theory source structure index

This is a mechanical source index, not a physical-validity verdict.

| Version | Chapter | Lines | Sections | Equation envs | Code tokens | Citation commands | Read |
|---|---|---:|---:|---:|---:|---:|---|
{rows}

Totals: {lines} lines, {equations} displayed equation environments.

The full section and equation locations are stored in
`PHASE_058_THEORY_EQUATION_CLAIM_MATRIX.json`.
""".format(
        rows="\n".join(rows),
        lines=sum(doc["line_count"] for doc in documents),
        equations=len(equations),
    )
    (RESULTS / "PHASE_058_THEORY_SOURCE_STRUCTURE_INDEX.md").write_text(
        index_text, encoding="utf-8"
    )


if __name__ == "__main__":
    main()
