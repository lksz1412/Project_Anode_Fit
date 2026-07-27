#!/usr/bin/env python3
"""Create exact source and labeled-equation diffs for Phase 059 theory."""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "Codex" / "work" / "v1014_v1018_2_phase059" / "theory_diffs"
OUT = ROOT / "Codex" / "results" / "PHASE_059_THEORY_LINEAGE_DIFF.json"

PAIRS = [
    (
        f"{family}_{old_tag}_to_{new_tag}",
        f"Claude/docs/{old_version}/{old_name}",
        f"Claude/docs/{new_version}/{new_name}",
    )
    for family, versions in {
        "ch1": [
            (
                "v1013",
                "v1.0.13",
                "graphite_ica_ch1_v1.0.13.tex",
                "v1014",
                "v1.0.14",
                "graphite_ica_ch1_v1.0.14.tex",
            ),
            (
                "v1014",
                "v1.0.14",
                "graphite_ica_ch1_v1.0.14.tex",
                "v1015",
                "v1.0.15",
                "graphite_ica_ch1_v1.0.15.tex",
            ),
            (
                "v1015",
                "v1.0.15",
                "graphite_ica_ch1_v1.0.15.tex",
                "v1016",
                "v1.0.16",
                "graphite_ica_ch1_v1.0.16.tex",
            ),
            (
                "v1016",
                "v1.0.16",
                "graphite_ica_ch1_v1.0.16.tex",
                "v1017",
                "v1.0.17",
                "graphite_ica_ch1_v1.0.17.tex",
            ),
            (
                "v1017",
                "v1.0.17",
                "graphite_ica_ch1_v1.0.17.tex",
                "v1018_1",
                "v1.0.18.1",
                "graphite_ica_ch1_v1.0.18.1.tex",
            ),
            (
                "v1018_1",
                "v1.0.18.1",
                "graphite_ica_ch1_v1.0.18.1.tex",
                "v1018_2",
                "v1.0.18.2",
                "graphite_ica_ch1_v1.0.18.2.tex",
            ),
        ],
        "ch2": [
            (
                "v1013",
                "v1.0.13",
                "graphite_ica_ch2_v1.0.13.tex",
                "v1014",
                "v1.0.14",
                "graphite_ica_ch2_v1.0.14.tex",
            ),
            (
                "v1014",
                "v1.0.14",
                "graphite_ica_ch2_v1.0.14.tex",
                "v1015",
                "v1.0.15",
                "graphite_ica_ch2_v1.0.15.tex",
            ),
            (
                "v1015",
                "v1.0.15",
                "graphite_ica_ch2_v1.0.15.tex",
                "v1016",
                "v1.0.16",
                "graphite_ica_ch2_v1.0.16.tex",
            ),
            (
                "v1016",
                "v1.0.16",
                "graphite_ica_ch2_v1.0.16.tex",
                "v1017",
                "v1.0.17",
                "graphite_ica_ch2_v1.0.17.tex",
            ),
            (
                "v1017",
                "v1.0.17",
                "graphite_ica_ch2_v1.0.17.tex",
                "v1018_1",
                "v1.0.18.1",
                "graphite_ica_ch2_v1.0.18.1.tex",
            ),
            (
                "v1018_1",
                "v1.0.18.1",
                "graphite_ica_ch2_v1.0.18.1.tex",
                "v1018_2",
                "v1.0.18.2",
                "graphite_ica_ch2_v1.0.18.2.tex",
            ),
        ],
        "appendix": [
            (
                "v1014",
                "v1.0.14",
                "appendix_phase_separation.tex",
                "v1015",
                "v1.0.15",
                "appendix_phase_separation.tex",
            ),
            (
                "v1015",
                "v1.0.15",
                "appendix_phase_separation.tex",
                "v1016",
                "v1.0.16",
                "appendix_phase_separation.tex",
            ),
            (
                "v1016",
                "v1.0.16",
                "appendix_phase_separation.tex",
                "v1017",
                "v1.0.17",
                "appendix_phase_separation.tex",
            ),
            (
                "v1017",
                "v1.0.17",
                "appendix_phase_separation.tex",
                "v1018_1",
                "v1.0.18.1",
                "appendix_phase_separation.tex",
            ),
            (
                "v1018_1",
                "v1.0.18.1",
                "appendix_phase_separation.tex",
                "v1018_2",
                "v1.0.18.2",
                "appendix_phase_separation.tex",
            ),
        ],
    }.items()
    for (
        old_tag,
        old_version,
        old_name,
        new_tag,
        new_version,
        new_name,
    ) in versions
]

SECTION_RE = re.compile(
    r"\\(?:part|chapter|section|subsection|subsubsection)\*?\{(.*?)\}"
    r"(?:\\label\{([^}]+)\})?"
)
BEGIN_EQ_RE = re.compile(
    r"\\begin\{(equation\*?|align\*?|alignat\*?|gather\*?|multline\*?|split|cases)\}"
)
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def git_blob_sha(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


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
        for label in LABEL_RE.findall(body):
            equations[label] = {
                "line_start": index + 1,
                "line_end": end + 1,
                "sha256_normalized": hashlib.sha256(
                    normalize(body).encode("utf-8")
                ).hexdigest(),
                "excerpt": normalize(body)[:360],
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
    old_payload = (ROOT / old_path).read_bytes()
    new_payload = (ROOT / new_path).read_bytes()
    old_lines = old_payload.decode("utf-8").splitlines()
    new_lines = new_payload.decode("utf-8").splitlines()
    matcher = difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False)
    opcodes = matcher.get_opcodes()
    line_counts = {
        "equal": 0,
        "replace_old": 0,
        "replace_new": 0,
        "delete": 0,
        "insert": 0,
    }
    for tag, old_start, old_end, new_start, new_end in opcodes:
        if tag == "equal":
            line_counts["equal"] += old_end - old_start
        elif tag == "replace":
            line_counts["replace_old"] += old_end - old_start
            line_counts["replace_new"] += new_end - new_start
        elif tag == "delete":
            line_counts["delete"] += old_end - old_start
        elif tag == "insert":
            line_counts["insert"] += new_end - new_start

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

    patch_rel = (
        f"Codex/work/v1014_v1018_2_phase059/theory_diffs/{pair_id}.patch"
    )
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
        "old_blob_sha": git_blob_sha(old_payload),
        "new_blob_sha": git_blob_sha(new_payload),
        "old_line_count": len(old_lines),
        "new_line_count": len(new_lines),
        "content_identical": old_payload == new_payload,
        "sequence_ratio": matcher.ratio(),
        "opcode_line_counts": line_counts,
        "exact_unified_diff": patch_rel,
        "exact_unified_diff_sha256": hashlib.sha256(
            patch.encode("utf-8")
        ).hexdigest(),
        "sections": {
            "old_count": len(old_sections),
            "new_count": len(new_sections),
            "added": [
                {"label": label, "title": title}
                for label, title in sorted(
                    new_section_keys - old_section_keys, key=str
                )
            ],
            "removed": [
                {"label": label, "title": title}
                for label, title in sorted(
                    old_section_keys - new_section_keys, key=str
                )
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
            "added": [
                {"label": label, **new_equations[label]} for label in added
            ],
            "removed": [
                {"label": label, **old_equations[label]} for label in removed
            ],
        },
    }


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    comparisons = [compare(*pair) for pair in PAIRS]
    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "status": "PASS_P059_THEORY_EXACT_DIFF",
        "authority_boundary": (
            "Exact text/equation-label lineage only; change does not imply "
            "scientific progress or validation."
        ),
        "comparison_count": len(comparisons),
        "content_identical_comparison_count": sum(
            comparison["content_identical"] for comparison in comparisons
        ),
        "comparisons": comparisons,
    }
    OUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "PASS_P059_THEORY_EXACT_DIFF "
        f"comparisons={len(comparisons)} "
        f"identical={payload['content_identical_comparison_count']}"
    )


if __name__ == "__main__":
    main()
