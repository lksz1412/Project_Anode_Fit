#!/usr/bin/env python3
"""Generate the Phase 059 mechanical theory-source structure index."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
QUEUE = RESULTS / "PHASE_059_V1014_V1018_2_AUDIT_QUEUE.json"
OUTPUT = RESULTS / "PHASE_059_THEORY_SOURCE_INDEX.json"
SUMMARY = RESULTS / "PHASE_059_THEORY_SOURCE_STRUCTURE_INDEX.md"

SECTION_RE = re.compile(
    r"\\(?P<level>part|chapter|section|subsection|subsubsection)\*?"
    r"\{(?P<title>.*?)\}"
)
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
BEGIN_EQ_RE = re.compile(
    r"\\begin\{(?P<env>equation\*?|align\*?|alignat\*?|gather\*?|"
    r"multline\*?|split|cases)\}"
)
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}")
CITE_RE = re.compile(r"\\cite[a-zA-Z]*\{([^}]+)\}")
MACRO_DEF_RE = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand|DeclareMathOperator)"
)
TEXT_DEF_RE = re.compile(
    r"(정의(?:한다|하면|는|를|:)?)|(라 두(?:자|면))|(로 둔다)|"
    r"(뜻한다)|(define[sd]?\b)",
    re.IGNORECASE,
)
MATH_DEF_RE = re.compile(r"\\equiv|\\coloneqq|:=|\\overset\{\\mathrm\{def\}\}")


def compact(text: str, limit: int = 360) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    return value if len(value) <= limit else value[: limit - 1] + "…"


def git_blob_sha(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def version_for(path: str) -> str:
    match = re.search(r"/(v1\.0\.[^/]+)/", path)
    if not match:
        raise ValueError(f"version not found: {path}")
    return match.group(1)


def family_for(path: str) -> str:
    name = Path(path).name
    if "appendix_phase_separation" in name:
        return "appendix_phase_separation"
    if "_ch1_" in name:
        return "ch1"
    if "_ch2_" in name:
        return "ch2"
    raise ValueError(f"theory family not found: {path}")


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def parse_sections(lines: list[str]) -> list[dict]:
    sections: list[dict] = []
    for index, line in enumerate(lines):
        match = SECTION_RE.search(line)
        if not match:
            continue
        label = None
        for probe in lines[index : min(index + 3, len(lines))]:
            label_match = LABEL_RE.search(probe)
            if label_match:
                label = label_match.group(1)
                break
        sections.append(
            {
                "level": match.group("level"),
                "title": compact(match.group("title"), 240),
                "label": label,
                "line": index + 1,
            }
        )
    return sections


def section_at(sections: list[dict], line: int) -> dict:
    active = {
        "level": "document",
        "title": "preamble/introduction",
        "label": None,
        "line": 1,
    }
    for section in sections:
        if section["line"] > line:
            break
        active = section
    return dict(active)


def parse_equations(lines: list[str], sections: list[dict], path: str) -> list[dict]:
    equations: list[dict] = []
    index = 0
    while index < len(lines):
        begin = BEGIN_EQ_RE.search(lines[index])
        if not begin:
            index += 1
            continue
        env = begin.group("env")
        end_marker = rf"\end{{{env}}}"
        end = index
        while end < len(lines) and end_marker not in lines[end]:
            end += 1
        if end >= len(lines):
            end = index
        body = "\n".join(lines[index : end + 1])
        labels = LABEL_RE.findall(body)
        normalized = compact(body, 100000)
        equations.append(
            {
                "equation_id": (
                    f"{version_for(path)}:{family_for(path)}:"
                    f"{labels[0] if labels else 'unlabeled-L' + str(index + 1)}"
                ),
                "path": path,
                "version": version_for(path),
                "family": family_for(path),
                "line_start": index + 1,
                "line_end": end + 1,
                "environment": env,
                "labels": labels,
                "section": section_at(sections, index + 1),
                "normalized_sha256": hashlib.sha256(
                    normalized.encode("utf-8")
                ).hexdigest(),
                "source_excerpt": compact(body),
                "is_mathematical_definition": bool(MATH_DEF_RE.search(body)),
                "source_read_status": "COMPLETE",
                "physical_adjudication": "PENDING_STEP_33_4_AND_LATER",
            }
        )
        index = end + 1
    return equations


def parse_labels(lines: list[str], sections: list[dict]) -> list[dict]:
    labels: list[dict] = []
    for number, line in enumerate(lines, 1):
        for label in LABEL_RE.findall(line):
            labels.append(
                {
                    "label": label,
                    "line": number,
                    "section": section_at(sections, number),
                }
            )
    return labels


def parse_definitions(
    lines: list[str], sections: list[dict], equations: list[dict]
) -> list[dict]:
    definitions: list[dict] = []
    for number, line in enumerate(lines, 1):
        if MACRO_DEF_RE.search(line):
            definitions.append(
                {
                    "kind": "latex_macro_definition",
                    "line_start": number,
                    "line_end": number,
                    "section": section_at(sections, number),
                    "source_excerpt": compact(line),
                }
            )
        elif TEXT_DEF_RE.search(line):
            definitions.append(
                {
                    "kind": "textual_definition_cue",
                    "line_start": number,
                    "line_end": number,
                    "section": section_at(sections, number),
                    "source_excerpt": compact(line),
                }
            )
    for equation in equations:
        if equation["is_mathematical_definition"]:
            definitions.append(
                {
                    "kind": "mathematical_definition",
                    "line_start": equation["line_start"],
                    "line_end": equation["line_end"],
                    "section": equation["section"],
                    "labels": equation["labels"],
                    "source_excerpt": equation["source_excerpt"],
                }
            )
    definitions.sort(key=lambda item: (item["line_start"], item["kind"]))
    return definitions


def parse_bibliography(lines: list[str]) -> list[dict]:
    bibliography: list[dict] = []
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = BIBITEM_RE.search(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, key) in enumerate(starts):
        end = starts[position + 1][0] - 1 if position + 1 < len(starts) else start
        while end + 1 < len(lines) and "\\end{thebibliography}" not in lines[end + 1]:
            if position + 1 < len(starts):
                break
            end += 1
        body = "\n".join(lines[start : end + 1])
        bibliography.append(
            {
                "key": key,
                "line_start": start + 1,
                "line_end": end + 1,
                "entry": compact(body, 700),
            }
        )
    return bibliography


def parse_citations(lines: list[str]) -> list[dict]:
    occurrences: dict[str, list[int]] = defaultdict(list)
    for number, line in enumerate(lines, 1):
        for group in CITE_RE.findall(line):
            for key in group.split(","):
                cleaned = key.strip()
                if cleaned:
                    occurrences[cleaned].append(number)
    return [
        {"key": key, "occurrence_count": len(locations), "lines": locations}
        for key, locations in sorted(occurrences.items())
    ]


def parse_document(record: dict) -> dict:
    path = record["representative_path"]
    payload = (ROOT / path).read_bytes()
    text = payload.decode("utf-8")
    lines = text.splitlines()
    actual_blob = git_blob_sha(payload)
    if actual_blob != record["blob_sha"]:
        raise SystemExit(f"theory blob mismatch: {path}")
    if len(lines) != record["extent"]["lines"]:
        raise SystemExit(f"theory line mismatch: {path}")

    sections = parse_sections(lines)
    equations = parse_equations(lines, sections, path)
    labels = parse_labels(lines, sections)
    definitions = parse_definitions(lines, sections, equations)
    bibliography = parse_bibliography(lines)
    citations = parse_citations(lines)
    return {
        "blob_sha": actual_blob,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "representative_path": path,
        "occurrence_paths": record["occurrence_paths"],
        "versions": record["versions"],
        "version": version_for(path),
        "family": family_for(path),
        "line_count": len(lines),
        "read_status": "COMPLETE",
        "section_count": len(sections),
        "equation_environment_count": len(equations),
        "label_count": len(labels),
        "definition_cue_count": len(definitions),
        "bibliography_item_count": len(bibliography),
        "citation_key_count": len(citations),
        "citation_occurrence_count": sum(
            citation["occurrence_count"] for citation in citations
        ),
        "code_identifier_token_count": len(
            re.findall(r"\\(?:code|texttt)\{", text)
        ),
        "sections": sections,
        "equations": equations,
        "labels": labels,
        "definitions": definitions,
        "bibliography": bibliography,
        "citations": citations,
    }


def main() -> None:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    records = [record for record in queue["records"] if record["role"] == "theory"]
    records.sort(key=lambda item: item["representative_path"])
    documents = [parse_document(record) for record in records]
    equations = [equation for document in documents for equation in document["equations"]]
    labels = [
        {
            "path": document["representative_path"],
            "version": document["version"],
            "family": document["family"],
            **label,
        }
        for document in documents
        for label in document["labels"]
    ]
    bibliography = [
        {
            "path": document["representative_path"],
            "version": document["version"],
            "family": document["family"],
            **item,
        }
        for document in documents
        for item in document["bibliography"]
    ]
    duplicate_labels = {
        label: count
        for label, count in Counter(item["label"] for item in labels).items()
        if count > 1
    }

    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "scope": "Phase 059 Step 33.3 mechanical theory source index",
        "status": "PASS_P059_THEORY_SOURCE_INDEX",
        "authority_boundary": (
            "Mechanical source structure only; no physical, code-conformance, "
            "bibliographic-validity, or external-validity verdict."
        ),
        "document_count": len(documents),
        "total_lines": sum(document["line_count"] for document in documents),
        "section_count": sum(document["section_count"] for document in documents),
        "equation_environment_count": len(equations),
        "label_occurrence_count": len(labels),
        "definition_cue_count": sum(
            document["definition_cue_count"] for document in documents
        ),
        "bibliography_item_occurrence_count": len(bibliography),
        "unique_bibliography_key_count": len(
            {item["key"] for item in bibliography}
        ),
        "duplicate_label_occurrence_counts": dict(sorted(duplicate_labels.items())),
        "documents": documents,
        "equations": equations,
        "labels": labels,
        "bibliography": bibliography,
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    rows = []
    for document in documents:
        rows.append(
            "| {version} | {family} | {lines} | {sections} | {equations} | "
            "{labels} | {definitions} | {bibitems} | {citations} | {code} |".format(
                version=",".join(document["versions"]),
                family=document["family"],
                lines=document["line_count"],
                sections=document["section_count"],
                equations=document["equation_environment_count"],
                labels=document["label_count"],
                definitions=document["definition_cue_count"],
                bibitems=document["bibliography_item_count"],
                citations=document["citation_occurrence_count"],
                code=document["code_identifier_token_count"],
            )
        )
    summary = """# Phase 059 theory source structure index

This is a mechanical source index, not a physical-validity or bibliography-validity
verdict. Definition counts are source cues, not acceptance of the definitions.

| Version occurrence | Family | Lines | Sections | Equation envs | Labels | Definition cues | Bibitems | Citation occurrences | Code tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
{rows}

Totals: {documents} unique theory blobs, {lines} lines, {sections} sections,
{equations} displayed equation environments, {labels} label occurrences,
{definitions} definition cues, {bibitems} bibliography-item occurrences and
{bibkeys} unique bibliography keys.

Full locations, content hashes, section ownership, definition cues, citation
locations and bibliography entries are stored in
`PHASE_059_THEORY_SOURCE_INDEX.json`.

Gate: `PASS_P059_THEORY_SOURCE_INDEX`.
""".format(
        rows="\n".join(rows),
        documents=len(documents),
        lines=payload["total_lines"],
        sections=payload["section_count"],
        equations=payload["equation_environment_count"],
        labels=payload["label_occurrence_count"],
        definitions=payload["definition_cue_count"],
        bibitems=payload["bibliography_item_occurrence_count"],
        bibkeys=payload["unique_bibliography_key_count"],
    )
    SUMMARY.write_text(summary, encoding="utf-8")
    print(
        "PASS_P059_THEORY_SOURCE_INDEX "
        f"documents={len(documents)} lines={payload['total_lines']} "
        f"equations={len(equations)}"
    )


if __name__ == "__main__":
    main()
