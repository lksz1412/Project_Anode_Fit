#!/usr/bin/env python3
"""Create exact source and equation-label diffs for the Phase 058 theory lineage."""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "Codex" / "work" / "v1010_v1013_phase058" / "theory_diffs"
OUT = ROOT / "Codex" / "results" / "PHASE_058_THEORY_LINEAGE_DIFF.json"

PAIRS = [
    (
        "ch1_v1010_to_v1012",
        "Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex",
        "Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex",
    ),
    (
        "ch1_v1012_to_v1013",
        "Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex",
        "Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex",
    ),
    (
        "ch2_v1010_to_v1012",
        "Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex",
        "Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex",
    ),
    (
        "ch2_v1012_to_v1013",
        "Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex",
        "Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex",
    ),
]

SECTION_RE = re.compile(
    r"\\(?:section|subsection|subsubsection)\*?\{(.*?)\}(?:\\label\{([^}]+)\})?"
)
BEGIN_EQ_RE = re.compile(r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def labeled_equations(lines: list[str]) -> dict[str, dict]:
    equations: dict[str, dict] = {}
    index = 0
    while index < len(lines):
        begin = BEGIN_EQ_RE.search(lines[index])
        if not begin:
            index += 1
            continue
        env = begin.group(1)
        end_marker = rf"\end{{{env}}}"
        end = index
        while end < len(lines) and end_marker not in lines[end]:
            end += 1
        if end >= len(lines):
            end = index
        body = "\n".join(lines[index : end + 1])
        labels = LABEL_RE.findall(body)
        for label in labels:
            equations[label] = {
                "line_start": index + 1,
                "line_end": end + 1,
                "sha256_normalized": hashlib.sha256(
                    normalize(body).encode("utf-8")
                ).hexdigest(),
                "excerpt": normalize(body)[:320],
            }
        index = end + 1
    return equations


def sections(lines: list[str]) -> list[dict]:
    records = []
    for number, line in enumerate(lines, 1):
        match = SECTION_RE.search(line)
        if match:
            records.append(
                {
                    "title": normalize(match.group(1)),
                    "label": match.group(2),
                    "line": number,
                }
            )
    return records


def compare(pair_id: str, old_path: str, new_path: str) -> dict:
    old_lines = (ROOT / old_path).read_text(encoding="utf-8").splitlines()
    new_lines = (ROOT / new_path).read_text(encoding="utf-8").splitlines()
    matcher = difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False)
    opcodes = matcher.get_opcodes()
    opcode_line_counts = {"equal": 0, "replace_old": 0, "replace_new": 0, "delete": 0, "insert": 0}
    for tag, a0, a1, b0, b1 in opcodes:
        if tag == "equal":
            opcode_line_counts["equal"] += a1 - a0
        elif tag == "replace":
            opcode_line_counts["replace_old"] += a1 - a0
            opcode_line_counts["replace_new"] += b1 - b0
        elif tag == "delete":
            opcode_line_counts["delete"] += a1 - a0
        elif tag == "insert":
            opcode_line_counts["insert"] += b1 - b0

    old_equations = labeled_equations(old_lines)
    new_equations = labeled_equations(new_lines)
    common = sorted(set(old_equations) & set(new_equations))
    unchanged = [
        label
        for label in common
        if old_equations[label]["sha256_normalized"]
        == new_equations[label]["sha256_normalized"]
    ]
    changed = [label for label in common if label not in unchanged]
    removed = sorted(set(old_equations) - set(new_equations))
    added = sorted(set(new_equations) - set(old_equations))

    old_sections = sections(old_lines)
    new_sections = sections(new_lines)
    old_section_keys = {(row["label"], row["title"]) for row in old_sections}
    new_section_keys = {(row["label"], row["title"]) for row in new_sections}

    patch_rel = f"Codex/work/v1010_v1013_phase058/theory_diffs/{pair_id}.patch"
    patch = "".join(
        difflib.unified_diff(
            [line + "\n" for line in old_lines],
            [line + "\n" for line in new_lines],
            fromfile=old_path,
            tofile=new_path,
            n=3,
        )
    )
    (ROOT / patch_rel).write_text(patch, encoding="utf-8")
    return {
        "pair_id": pair_id,
        "old_path": old_path,
        "new_path": new_path,
        "old_line_count": len(old_lines),
        "new_line_count": len(new_lines),
        "sequence_ratio": matcher.ratio(),
        "opcode_line_counts": opcode_line_counts,
        "exact_unified_diff": patch_rel,
        "exact_unified_diff_sha256": hashlib.sha256(patch.encode("utf-8")).hexdigest(),
        "sections": {
            "old_count": len(old_sections),
            "new_count": len(new_sections),
            "added": [
                {"label": label, "title": title}
                for label, title in sorted(new_section_keys - old_section_keys, key=str)
            ],
            "removed": [
                {"label": label, "title": title}
                for label, title in sorted(old_section_keys - new_section_keys, key=str)
            ],
        },
        "labeled_equations": {
            "old_count": len(old_equations),
            "new_count": len(new_equations),
            "unchanged_count": len(unchanged),
            "changed_count": len(changed),
            "added_count": len(added),
            "removed_count": len(removed),
            "unchanged_labels": unchanged,
            "changed": [
                {
                    "label": label,
                    "old": old_equations[label],
                    "new": new_equations[label],
                }
                for label in changed
            ],
            "added": [{"label": label, **new_equations[label]} for label in added],
            "removed": [{"label": label, **old_equations[label]} for label in removed],
        },
    }


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    comparisons = [compare(*pair) for pair in PAIRS]
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "status": "PASS_P058_THEORY_EXACT_DIFF",
        "copy_forward": [
            {
                "source_blob": "23aa7f49d98acf27abe47e9cff6a8b372c99d274",
                "paths": [
                    "Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex",
                    "Claude/docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex",
                ],
                "verdict": "CONTENT_IDENTICAL; VERSION_LABEL_NOT_NEW_VALIDATION",
            },
            {
                "source_blob": "ed14b4a1f37749332dff61e0be2ac675cc36a655",
                "paths": [
                    "Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex",
                    "Claude/docs/v1.0.11/graphite_ica_ch2_v1.0.11.tex",
                ],
                "verdict": "CONTENT_IDENTICAL; VERSION_LABEL_NOT_NEW_VALIDATION",
            },
        ],
        "comparisons": comparisons,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
