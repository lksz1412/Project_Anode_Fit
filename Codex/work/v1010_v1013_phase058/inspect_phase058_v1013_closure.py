#!/usr/bin/env python3
"""Extract structural evidence for the Phase 058 v1.0.13 closure audit."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCES = {
    "chapter_1": ROOT / "Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex",
    "chapter_2": ROOT / "Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex",
}

HEADING_RE = re.compile(
    r"^\\(?P<level>section|subsection|subsubsection)\{(?P<title>.*)\}"
)
PATTERNS = {
    "code_mentions": re.compile(r"\\code\{"),
    "equation_labels": re.compile(r"\\label\{eq:"),
    "citations": re.compile(r"\\cite\{"),
    "assumption_markers": re.compile(r"가정"),
    "fit_markers": re.compile(r"피팅|fit", re.IGNORECASE),
    "placeholder_markers": re.compile(
        r"tier C|placeholder|미배정|근거미발견|신뢰값이 아니라 초기값"
    ),
    "deferral_markers": re.compile(
        r"후속|향후|과제|범위 밖|다루지 않는다|미구현"
    ),
    "validation_markers": re.compile(r"검증|검산|실험|실측|데이터|GITT"),
}


def section_rows(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    headings: list[tuple[int, str, str]] = []
    for number, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match:
            headings.append((number, match.group("level"), match.group("title")))

    rows: list[dict[str, object]] = []
    for index, (start, level, title) in enumerate(headings):
        end = headings[index + 1][0] - 1 if index + 1 < len(headings) else len(lines)
        block = "\n".join(lines[start - 1 : end])
        row: dict[str, object] = {
            "level": level,
            "title": title,
            "start_line": start,
            "end_line": end,
            "source_line_count": end - start + 1,
        }
        for name, pattern in PATTERNS.items():
            row[name] = len(pattern.findall(block))
        rows.append(row)
    return rows


def line_hits(text: str) -> dict[str, list[int]]:
    hits: dict[str, list[int]] = {}
    for name in (
        "placeholder_markers",
        "deferral_markers",
        "assumption_markers",
    ):
        pattern = PATTERNS[name]
        hits[name] = [
            number
            for number, line in enumerate(text.splitlines(), start=1)
            if not line.lstrip().startswith("%") and pattern.search(line)
        ]
    return hits


def main() -> None:
    result: dict[str, object] = {}
    for name, path in SOURCES.items():
        text = path.read_text(encoding="utf-8")
        source_rows = section_rows(text)
        result[name] = {
            "path": str(path.relative_to(ROOT)),
            "source_line_count": len(text.splitlines()),
            "section_count": sum(row["level"] == "section" for row in source_rows),
            "subsection_count": sum(
                row["level"] == "subsection" for row in source_rows
            ),
            "subsubsection_count": sum(
                row["level"] == "subsubsection" for row in source_rows
            ),
            "totals": {
                name_: len(pattern.findall(text))
                for name_, pattern in PATTERNS.items()
            },
            "line_hits": line_hits(text),
            "sections": source_rows,
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
