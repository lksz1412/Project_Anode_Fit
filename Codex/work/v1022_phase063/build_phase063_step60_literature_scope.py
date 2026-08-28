#!/usr/bin/env python3
"""Build Phase 063 Step 60 literature, quantity, and scope evidence.

The builder reads the frozen v1.0.22 Git objects and committed Codex audit
artifacts.  It does not contact the network, import production code, modify
Claude/**, or promote bibliography metadata to proposition-level truth.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


REPO = Path(__file__).resolve().parents[3]
BUILDER = Path(__file__).resolve()
TOPOLOGY = REPO / "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json"
STEP59 = REPO / "Codex/results/PHASE_063_V1022_EQUATION_MATERIAL_REDERIVATION.json"
PRIOR_SCOPE = REPO / "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json"
RESULT = REPO / "Codex/results/PHASE_063_STEP_060_LITERATURE_SCOPE_RESULT.md"
OUTPUT = REPO / "Codex/results/PHASE_063_V1022_LITERATURE_SCOPE_MATRIX.json"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "07a0f3ead16a072550919b86d1d41580682fd92d"
GATE = "PASS_P063_STEP60_LITERATURE_SCOPE_WITH_CONCERNS"
EVIDENCE_BEGIN = "<!-- P063_STEP60_LITERATURE_EVIDENCE_BEGIN -->"
EVIDENCE_END = "<!-- P063_STEP60_LITERATURE_EVIDENCE_END -->"
F = 96485.33212
F_MAH_PER_MOL = F / 3.6

DISPLAY_ENVS = ("equation", "align", "gather", "multline", "flalign", "alignat")
DISPLAY_BEGIN_RE = re.compile(
    r"\\begin\{(?P<environment>"
    + "|".join(
        re.escape(environment)
        for base in DISPLAY_ENVS
        for environment in (base, base + "*")
    )
    + r")\}"
)
DOI_RE = re.compile(r"(?i)(?<![A-Za-z0-9])10\.\d{4,9}/[-._;()/:A-Z0-9]+")
CITE_RE = re.compile(
    r"\\(?P<command>cite[a-zA-Z*]*)\s*(?:\[[^\]]*\]\s*){0,2}\{(?P<keys>[^{}]+)\}",
    re.MULTILINE,
)
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{(?P<key>[^{}]+)\}")
NUMBER_RE = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
UNIT_RE = re.compile(
    r"(?i)(?:mAh\s*/\s*g|Ah\s*/\s*g|mV\s*/\s*(?:K|GPa)|"
    r"(?:J|kJ)\s*/\s*\(?mol(?:\\,|\s)*K\)?|(?:micro|\\mu|μ)\s*V\s*/\s*K|"
    r"(?:mV|V|eV|K|GPa|MPa|Pa|nm|\\mu m|μm|cm\^?\{?2\}?/s|s\^?\{-?1\}?|h\^?\{-?1\}?|wt\\?%|\\?%))"
)
MATERIAL_RE = re.compile(
    r"(?i)(?:graphite|LiC_?\{?6\}?|LiCoO|LCO|cobalt oxide|silicon|"
    r"SiO(?:_?\{?x\}?)?|Si--C|Si-C|Si/graphite|graphite.?Si|"
    r"Li_?\{?15\}?Si_?\{?4\}?|dop(?:ed|ant|ing)|oxygen redox|charge.?order)"
)

PARTITION_CEILING = {
    "FINAL_RELEASE_SURFACE": "FROZEN_RELEASE_ASSERTION_OCCURRENCE_ONLY",
    "VERSION_PLAN": "PROCESS_INTENT_ONLY",
    "STATUS_MACHINE_PROCESS": "SELF_REPORT_OR_MACHINE_STRUCTURE_ONLY",
    "COMPETING_REVIEW_CANDIDATE": "PROPOSAL_REVIEW_CANDIDATE_ONLY",
    "SUPPLEMENTAL_PROCESS_CONTROL": "PROCESS_CONTROL_REPOSITORY_REPORTED_ONLY",
}

AUTHORITY_AXIS_KEYS = (
    "bibliographic_existence",
    "fulltext_method",
    "exact_equation",
    "exact_value_unit_basis",
    "sample_material_composition_protocol",
    "current_model_mapping",
    "external_experimental_support",
)
LEXICAL_AUTHORITY_PROFILE_ID = "P063-AXIS-LEXICAL-UNVERIFIED"
LEXICAL_AUTHORITY_PROFILE = {
    "bibliographic_existence": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "fulltext_method": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "exact_equation": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "exact_value_unit_basis": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "sample_material_composition_protocol": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "current_model_mapping": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
    "external_experimental_support": "NOT_ESTABLISHED_BY_LEXICAL_OCCURRENCE",
}


class BuildError(RuntimeError):
    """A controlled builder failure."""


def run_git(*args: str, binary: bool = False) -> bytes | str:
    proc = subprocess.run(
        ["git", *args], cwd=REPO, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode:
        raise BuildError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout if binary else proc.stdout.decode("utf-8", "strict").strip()


def git_bytes(commit: str, path: str) -> bytes:
    value = run_git("show", f"{commit}:{path}", binary=True)
    assert isinstance(value, bytes)
    return value


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def normalized_bytes(path: Path) -> bytes:
    text = path.read_bytes().decode("utf-8", "strict")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def compact_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def strict_load_bytes(raw: bytes) -> Any:
    def pairs_hook(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise BuildError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value: str) -> None:
        raise BuildError(f"non-finite JSON constant: {value}")

    return json.loads(raw, object_pairs_hook=pairs_hook, parse_constant=reject_constant)


def strict_load(path: Path) -> Any:
    return strict_load_bytes(path.read_bytes())


def parse_manual_evidence() -> tuple[dict[str, Any], str]:
    text = RESULT.read_text(encoding="utf-8")
    if text.count(EVIDENCE_BEGIN) != 1 or text.count(EVIDENCE_END) != 1:
        raise BuildError("Step 60 result must contain one literature evidence block")
    block = text.split(EVIDENCE_BEGIN, 1)[1].split(EVIDENCE_END, 1)[0].strip()
    if not block.startswith("```json\n") or not block.endswith("\n```"):
        raise BuildError("Step 60 evidence block must be a fenced JSON object")
    value = strict_load_bytes(block[len("```json\n"):-len("\n```")].encode("utf-8"))
    if not isinstance(value, dict):
        raise BuildError("Step 60 evidence root must be an object")
    return value, sha256(compact_bytes(value))


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def line_interval(text: str, start: int, end: int) -> tuple[int, int]:
    return line_number(text, start), line_number(text, max(start, end - 1))


def is_escaped(text: str, offset: int) -> bool:
    backslashes = 0
    cursor = offset - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def find_unescaped_token(text: str, token: str, start: int = 0) -> int:
    cursor = text.find(token, start)
    while cursor >= 0 and is_escaped(text, cursor):
        cursor = text.find(token, cursor + 1)
    return cursor


def markdown_tex_delimited_math_spans(text: str) -> list[tuple[int, int, str]]:
    r"""Parse Markdown math with flanking tokens and structural-boundary recovery."""
    spans: list[tuple[int, int, str]] = []
    line_offset = 0
    state: str | None = None
    start = -1
    previous_line = ""
    physical_lines = text.splitlines(keepends=True)
    for line_index, physical_line in enumerate(physical_lines):
        line = physical_line.rstrip("\r\n")
        stripped = line.lstrip()
        previous_stripped = previous_line.lstrip()
        structural_boundary = (
            line_index > 0
            and state == "INLINE_DOLLAR"
            and (
                not line.strip()
                or previous_stripped.startswith("|")
                or stripped.startswith("|")
                or stripped.startswith("#")
                or stripped.startswith("```")
                or stripped.startswith("~~~")
            )
        )
        if structural_boundary:
            spans.append((start, start + 1, "UNPAIRED_INLINE_DOLLAR"))
            state, start = None, -1
        index = 0
        while index < len(line):
            if state is None:
                if line.startswith(r"\(", index) and not is_escaped(line, index):
                    state, start, index = "INLINE_PAREN", line_offset + index, index + 2
                    continue
                if line[index] == "$" and not is_escaped(line, index):
                    if line.startswith("$$", index):
                        state, start, index = "DISPLAY_DOLLAR", line_offset + index, index + 2
                    elif index + 1 < len(line) and not line[index + 1].isspace():
                        state, start, index = "INLINE_DOLLAR", line_offset + index, index + 1
                    else:
                        spans.append((
                            line_offset + index,
                            line_offset + index + 1,
                            "UNPAIRED_INLINE_DOLLAR",
                        ))
                        index += 1
                    continue
            elif state == "INLINE_PAREN":
                if line.startswith(r"\)", index) and not is_escaped(line, index):
                    spans.append((start, line_offset + index + 2, state))
                    state, start, index = None, -1, index + 2
                    continue
                if line[index] == "$" and not is_escaped(line, index):
                    spans.append((
                        line_offset + index,
                        line_offset + index + 1,
                        "UNPAIRED_INLINE_DOLLAR",
                    ))
                    index += 1
                    continue
            elif state == "INLINE_DOLLAR":
                if line[index] == "$" and not is_escaped(line, index):
                    spans.append((start, line_offset + index + 1, state))
                    state, start, index = None, -1, index + 1
                    continue
            elif state == "DISPLAY_DOLLAR":
                if line.startswith("$$", index) and not is_escaped(line, index):
                    spans.append((start, line_offset + index + 2, state))
                    state, start, index = None, -1, index + 2
                    continue
                if line[index] == "$" and not is_escaped(line, index):
                    spans.append((
                        line_offset + index,
                        line_offset + index + 1,
                        "UNPAIRED_INLINE_DOLLAR",
                    ))
                    index += 1
                    continue
            index += 1
        previous_line = line
        line_offset += len(physical_line)
    if state is not None:
        opening_width = 2 if state in {"INLINE_PAREN", "DISPLAY_DOLLAR"} else 1
        syntax = (
            "UNPAIRED_INLINE_DOLLAR"
            if state == "INLINE_DOLLAR"
            else f"UNTERMINATED_{state}"
        )
        spans.append((start, start + opening_width, syntax))
    return spans


def tex_delimited_math_spans(text: str, path: str) -> list[tuple[int, int, str]]:
    r"""Statefully parse $, $$ and \( delimiters, including adjacent $...$$...$."""
    if path.lower().endswith(".md"):
        return markdown_tex_delimited_math_spans(text)
    spans: list[tuple[int, int, str]] = []
    state: str | None = None
    start = -1
    index = 0
    while index < len(text):
        if state is None:
            if text.startswith(r"\(", index) and not is_escaped(text, index):
                state, start, index = "INLINE_PAREN", index, index + 2
                continue
            if text[index] == "$" and not is_escaped(text, index):
                if text.startswith("$$", index):
                    state, start, index = "DISPLAY_DOLLAR", index, index + 2
                else:
                    state, start, index = "INLINE_DOLLAR", index, index + 1
                continue
        elif state == "INLINE_PAREN":
            if text.startswith(r"\)", index) and not is_escaped(text, index):
                spans.append((start, index + 2, state))
                state, start, index = None, -1, index + 2
                continue
        elif state == "INLINE_DOLLAR":
            if text[index] == "$" and not is_escaped(text, index):
                spans.append((start, index + 1, state))
                state, start, index = None, -1, index + 1
                continue
        elif state == "DISPLAY_DOLLAR":
            if text.startswith("$$", index) and not is_escaped(text, index):
                spans.append((start, index + 2, state))
                state, start, index = None, -1, index + 2
                continue
        index += 1
    if state is not None:
        opening_width = 2 if state in {"INLINE_PAREN", "DISPLAY_DOLLAR"} else 1
        spans.append((start, start + opening_width, f"UNTERMINATED_{state}"))
    return spans


def normalize_doi(token: str) -> str:
    value = token.strip().rstrip(".,;:").lower()
    while value.endswith(")") and value.count("(") < value.count(")"):
        value = value[:-1]
    return value


def source_texts(topology: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    rows: list[dict[str, Any]] = []
    texts: dict[str, str] = {}
    for source in topology["sources"]:
        if source["review_mode"] != "FULL_TEXT":
            continue
        path = source["path"]
        raw = git_bytes(BASELINE, path)
        blob = run_git("rev-parse", f"{BASELINE}:{path}")
        assert isinstance(blob, str)
        if blob != source["blob_sha1"] or sha256(raw) != source["sha256"]:
            raise BuildError(f"frozen source identity drift: {path}")
        text = raw.decode("utf-8", "strict")
        lines = text.splitlines()
        if len(lines) != source["extent"]["lines"]:
            raise BuildError(f"frozen source line drift: {path}")
        texts[path] = text
        rows.append({
            "source_id": source["source_id"],
            "path": path,
            "partition": source["partition"],
            "role": source["role"],
            "extension": source["extension"],
            "git_blob": blob,
            "raw_sha256": source["sha256"],
            "bytes": len(raw),
            "physical_lines": len(lines),
            "read_interval": [1, len(lines)],
            "read_state": "READ_FULL_IN_STEP58_REPLAYED_FROM_FROZEN_GIT_BLOB",
            "manifest_member": True,
            "authority_ceiling": PARTITION_CEILING[source["partition"]],
        })

    supplemental = topology["supplemental_process_control"]
    path = supplemental["path"]
    raw = git_bytes(BASELINE, path)
    blob = run_git("rev-parse", f"{BASELINE}:{path}")
    assert isinstance(blob, str)
    if blob != supplemental["blob_sha1"] or sha256(raw) != supplemental["sha256"]:
        raise BuildError(f"frozen supplemental source identity drift: {path}")
    text = raw.decode("utf-8", "strict")
    lines = text.splitlines()
    if len(lines) != supplemental["physical_lines"]:
        raise BuildError(f"frozen supplemental source line drift: {path}")
    texts[path] = text
    rows.append({
        "source_id": supplemental["source_id"],
        "path": path,
        "partition": "SUPPLEMENTAL_PROCESS_CONTROL",
        "role": "SUPPLEMENTAL_PROCESS_CONTROL",
        "extension": Path(path).suffix.lower(),
        "git_blob": blob,
        "raw_sha256": supplemental["sha256"],
        "bytes": len(raw),
        "physical_lines": len(lines),
        "read_interval": [1, len(lines)],
        "read_state": "READ_FULL_IN_STEP58_REPLAYED_FROM_FROZEN_GIT_BLOB",
        "manifest_member": False,
        "authority_ceiling": PARTITION_CEILING["SUPPLEMENTAL_PROCESS_CONTROL"],
    })
    return rows, texts


def extract_citations(
    source_rows: list[dict[str, Any]], texts: dict[str, str],
) -> tuple[list[dict[str, Any]], int]:
    by_path = {row["path"]: row for row in source_rows}
    rows: list[dict[str, Any]] = []
    commands = 0
    for path in sorted(texts):
        source = by_path[path]
        text = texts[path]
        for match in CITE_RE.finditer(text):
            commands += 1
            start_line, end_line = line_interval(text, match.start(), match.end())
            for key_ordinal, raw_key in enumerate(match.group("keys").split(","), start=1):
                key = raw_key.strip()
                if not key:
                    raise BuildError(f"empty citation key at {path}:{start_line}")
                rows.append({
                    "citation_occurrence_id": f"P063-S60-CITE-{len(rows) + 1:05d}",
                    "source_id": source["source_id"],
                    "path": path,
                    "partition": source["partition"],
                    "git_blob": source["git_blob"],
                    "start_line": start_line,
                    "end_line": end_line,
                    "command": match.group("command"),
                    "command_ordinal": commands,
                    "key_ordinal_within_command": key_ordinal,
                    "cite_key": key,
                    "command_sha256": sha256(match.group(0).encode("utf-8")),
                    "authority_ceiling": source["authority_ceiling"],
                })
    return rows, commands


def extract_bibliography(
    source_rows: list[dict[str, Any]], texts: dict[str, str],
) -> list[dict[str, Any]]:
    by_path = {row["path"]: row for row in source_rows}
    rows: list[dict[str, Any]] = []
    for path in sorted(texts):
        source = by_path[path]
        text = texts[path]
        matches = list(BIBITEM_RE.finditer(text))
        for ordinal, match in enumerate(matches):
            next_start = matches[ordinal + 1].start() if ordinal + 1 < len(matches) else len(text)
            line_end = text.find("\n", match.end(), next_start)
            end = line_end if line_end >= 0 else next_start
            body = text[match.start():end].rstrip() + "\n"
            start_line, end_line = line_interval(text, match.start(), end)
            dois = sorted({normalize_doi(item.group(0)) for item in DOI_RE.finditer(body)})
            rows.append({
                "bibliography_occurrence_id": f"P063-S60-BIB-{len(rows) + 1:05d}",
                "source_id": source["source_id"],
                "path": path,
                "partition": source["partition"],
                "git_blob": source["git_blob"],
                "start_line": start_line,
                "end_line": end_line,
                "cite_key": match.group("key").strip(),
                "doi_values": dois,
                "body_sha256": sha256(body.encode("utf-8")),
                "body": body,
                "authority_ceiling": source["authority_ceiling"],
                "external_metadata_validated": False,
                "fulltext_proposition_validated": False,
            })
    return rows


def extract_manual_unkeyed_references(
    source_rows: list[dict[str, Any]], texts: dict[str, str],
) -> list[dict[str, Any]]:
    """Inventory the five A1--A5 references outside the bibitem/cite graph."""
    path = "Claude/docs/v1.0.22/appendix_phase_separation.tex"
    source = {row["path"]: row for row in source_rows}.get(path)
    text = texts.get(path)
    if source is None or text is None or source["source_id"] != "P063-SRC-0056":
        raise BuildError("manual bibliography source identity drift")
    marker = r"\section*{참고문헌}"
    begin_marker = r"\begin{enumerate}[label={[A\arabic*]},leftmargin=3.2em]"
    end_marker = r"\end{enumerate}"
    if text.count(marker) != 1 or text.count(begin_marker) != 1 or text.count(end_marker) != 1:
        raise BuildError("manual bibliography block cardinality drift")
    section_start = text.index(marker)
    block_start = text.index(begin_marker, section_start) + len(begin_marker)
    block_end = text.index(end_marker, block_start)
    item_matches = list(re.finditer(r"(?m)^\\item\s", text[block_start:block_end]))
    if len(item_matches) != 5:
        raise BuildError(f"manual bibliography item cardinality drift: {len(item_matches)}")
    rows: list[dict[str, Any]] = []
    for ordinal, match in enumerate(item_matches, start=1):
        start = block_start + match.start()
        end = (
            block_start + item_matches[ordinal].start()
            if ordinal < len(item_matches) else block_end
        )
        body = text[start:end].rstrip() + "\n"
        start_line, end_line = line_interval(text, start, end)
        rows.append({
            "manual_reference_occurrence_id": f"P063-S60-MANREF-{ordinal:05d}",
            "manual_label": f"A{ordinal}",
            "source_id": source["source_id"],
            "path": path,
            "partition": source["partition"],
            "git_blob": source["git_blob"],
            "start_line": start_line,
            "end_line": end_line,
            "doi_values": sorted({
                normalize_doi(item.group(0)) for item in DOI_RE.finditer(body)
            }),
            "body_sha256": sha256(body.encode("utf-8")),
            "body": body,
            "cite_key": None,
            "citation_route": None,
            "authority_ceiling": source["authority_ceiling"],
            "authority_axis_profile_id": LEXICAL_AUTHORITY_PROFILE_ID,
            "authority_axes_assigned": True,
            "external_metadata_validated": False,
            "fulltext_proposition_validated": False,
        })
    return rows


def extract_dois(
    source_rows: list[dict[str, Any]], texts: dict[str, str],
) -> list[dict[str, Any]]:
    by_path = {row["path"]: row for row in source_rows}
    rows: list[dict[str, Any]] = []
    for path in sorted(texts):
        source = by_path[path]
        text = texts[path]
        lines = text.splitlines()
        for match in DOI_RE.finditer(text):
            start_line, end_line = line_interval(text, match.start(), match.end())
            rows.append({
                "doi_occurrence_id": f"P063-S60-DOI-{len(rows) + 1:05d}",
                "source_id": source["source_id"],
                "path": path,
                "partition": source["partition"],
                "git_blob": source["git_blob"],
                "start_line": start_line,
                "end_line": end_line,
                "raw": match.group(0),
                "normalized": normalize_doi(match.group(0)),
                "line_text": lines[start_line - 1],
                "line_sha256": sha256((lines[start_line - 1] + "\n").encode("utf-8")),
                "authority_ceiling": "FROZEN_DOI_STRING_OCCURRENCE_ONLY",
                "resolver_validated_in_step60": False,
                "proposition_support_validated": False,
            })
    return rows


def display_equation_spans(text: str, path: str) -> list[tuple[int, int, str]]:
    """Inventory every unescaped display-environment and bracket opener."""
    spans: list[tuple[int, int, str]] = []
    for match in DISPLAY_BEGIN_RE.finditer(text):
        if is_escaped(text, match.start()):
            continue
        environment = match.group("environment")
        end_token = rf"\end{{{environment}}}"
        end_start = find_unescaped_token(text, end_token, match.end())
        if end_start < 0:
            raise BuildError(
                f"unterminated {environment} at {path}:{line_number(text, match.start())}"
            )
        spans.append((match.start(), end_start + len(end_token), environment))
    cursor = 0
    while True:
        start = find_unescaped_token(text, r"\[", cursor)
        if start < 0:
            break
        end_start = find_unescaped_token(text, r"\]", start + 2)
        if end_start < 0:
            raise BuildError(
                f"unterminated bracket display at {path}:{line_number(text, start)}"
            )
        spans.append((start, end_start + 2, "bracket"))
        cursor = end_start + 2
    return sorted(spans, key=lambda item: (item[0], item[1], item[2]))


def extract_equation_candidates(
    source_rows: list[dict[str, Any]], texts: dict[str, str],
) -> list[dict[str, Any]]:
    by_path = {row["path"]: row for row in source_rows}
    rows: list[dict[str, Any]] = []
    for path in sorted(texts):
        source = by_path[path]
        text = texts[path]
        ordinals: Counter[int] = Counter()
        for start, end, environment in display_equation_spans(text, path):
            start_line, end_line = line_interval(text, start, end)
            ordinals[start_line] += 1
            body = text[start:end]
            last_newline = text.rfind("\n", 0, end)
            rows.append({
                "equation_candidate_id": f"P063-S60-EQ-{len(rows) + 1:05d}",
                "source_id": source["source_id"],
                "path": path,
                "partition": source["partition"],
                "git_blob": source["git_blob"],
                "start_line": start_line,
                "end_line": end_line,
                "ordinal_within_start_line": ordinals[start_line],
                "start_column": start - text.rfind("\n", 0, start),
                "end_column": end - last_newline - 1,
                "environment": environment,
                "labels": re.findall(r"\\label\{([^{}]+)\}", body),
                "body": body,
                "body_sha256": sha256(body.encode("utf-8")),
                "authority_ceiling": source["authority_ceiling"],
                "authority_axis_profile_id": LEXICAL_AUTHORITY_PROFILE_ID,
                "authority_axes_assigned": True,
                "exact_equation_externally_validated": False,
            })
    return rows


def extract_line_claim_candidates(
    source_rows: list[dict[str, Any]], texts: dict[str, str],
) -> list[dict[str, Any]]:
    by_path = {row["path"]: row for row in source_rows}
    rows: list[dict[str, Any]] = []
    for path in sorted(texts):
        source = by_path[path]
        for line_number_value, line in enumerate(texts[path].splitlines(), start=1):
            kinds: list[str] = []
            if DOI_RE.search(line):
                kinds.append("DOI_METADATA")
            if BIBITEM_RE.search(line):
                kinds.append("BIBLIOGRAPHY_RECORD")
            if CITE_RE.search(line):
                kinds.append("CITATION")
            if NUMBER_RE.search(line) and UNIT_RE.search(line):
                kinds.append("NUMERIC_QUANTITY")
            if MATERIAL_RE.search(line):
                kinds.append("MATERIAL_SCOPE")
            if not kinds:
                continue
            rows.append({
                "claim_candidate_id": f"P063-S60-CLM-{len(rows) + 1:05d}",
                "source_id": source["source_id"],
                "path": path,
                "partition": source["partition"],
                "git_blob": source["git_blob"],
                "line": line_number_value,
                "candidate_kinds": sorted(kinds),
                "line_sha256": sha256((line + "\n").encode("utf-8")),
                "text": line,
                "authority_ceiling": source["authority_ceiling"],
                "claim_occurrence_inventory_state": "INVENTORIED_AUTHORITY_BOUNDED_NOT_SEMANTICALLY_NORMALIZED",
                "authority_axis_profile_id": LEXICAL_AUTHORITY_PROFILE_ID,
                "authority_axes_assigned": True,
                "semantic_claim_adjudicated": False,
            })
    return rows


def extract_tex_delimited_math_candidates(
    source_rows: list[dict[str, Any]], texts: dict[str, str],
) -> list[dict[str, Any]]:
    r"""Inventory TeX-syntax $, $$ and \( math across every text source."""
    by_path = {row["path"]: row for row in source_rows}
    rows: list[dict[str, Any]] = []
    for path in sorted(texts):
        source = by_path[path]
        text = texts[path]
        ordinals: Counter[int] = Counter()
        for start, end, syntax in tex_delimited_math_spans(text, path):
            start_line, end_line = line_interval(text, start, end)
            ordinals[start_line] += 1
            body = text[start:end]
            last_newline = text.rfind("\n", 0, end)
            rows.append({
                "tex_math_candidate_id": f"P063-S60-TEXMATH-{len(rows) + 1:05d}",
                "source_id": source["source_id"],
                "path": path,
                "partition": source["partition"],
                "git_blob": source["git_blob"],
                "start_line": start_line,
                "end_line": end_line,
                "ordinal_within_start_line": ordinals[start_line],
                "start_column": start - text.rfind("\n", 0, start),
                "end_column": end - last_newline - 1,
                "syntax": syntax,
                "body": body,
                "body_sha256": sha256(body.encode("utf-8")),
                "authority_ceiling": source["authority_ceiling"],
                "claim_occurrence_inventory_state": "INVENTORIED_AUTHORITY_BOUNDED_NOT_SEMANTICALLY_NORMALIZED",
                "authority_axis_profile_id": LEXICAL_AUTHORITY_PROFILE_ID,
                "authority_axes_assigned": True,
                "semantic_claim_adjudicated": False,
            })
    return rows


def bibliography_conflicts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_key: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    by_doi: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_key[row["cite_key"]].append(row)
        for doi in row["doi_values"]:
            by_doi[doi].append(row)
    key_variants = []
    for key, values in sorted(by_key.items()):
        bodies = sorted({row["body_sha256"] for row in values})
        doi_sets = sorted({tuple(row["doi_values"]) for row in values})
        if len(bodies) > 1 or len(doi_sets) > 1:
            key_variants.append({
                "cite_key": key,
                "occurrence_ids": [row["bibliography_occurrence_id"] for row in values],
                "body_variants": len(bodies),
                "doi_set_variants": [list(value) for value in doi_sets],
                "state": "VERSION_OR_PROPOSAL_VARIANT_REQUIRES_MANUAL_ADJUDICATION",
                "external_metadata_validated": False,
            })
    doi_multi_keys = []
    for doi, values in sorted(by_doi.items()):
        keys = sorted({row["cite_key"] for row in values})
        if len(keys) > 1:
            doi_multi_keys.append({
                "doi": doi,
                "cite_keys": keys,
                "occurrence_ids": [row["bibliography_occurrence_id"] for row in values],
                "state": "SHARED_DOI_ACROSS_KEYS_REQUIRES_MANUAL_ADJUDICATION",
            })
    multi_doi_entries = [
        {"bibliography_occurrence_id": row["bibliography_occurrence_id"],
         "cite_key": row["cite_key"], "doi_values": row["doi_values"]}
        for row in rows if len(row["doi_values"]) > 1
    ]
    return {
        "same_key_variant_groups": key_variants,
        "same_doi_multiple_key_groups": doi_multi_keys,
        "multiple_doi_single_entry_occurrences": multi_doi_entries,
        "interpretation": "These are frozen internal identity conflicts or revision variants; they are not external metadata verdicts.",
    }


def quantity_checks() -> dict[str, Any]:
    molar_mass_si = 28.0855
    molar_mass_sio = 44.0849
    si_li375 = 3.75 * F_MAH_PER_MOL / molar_mass_si
    si_li44 = 4.4 * F_MAH_PER_MOL / molar_mass_si
    sio_li28125 = 2.8125 * F_MAH_PER_MOL / molar_mass_sio
    slope = 0.83e-3
    return {
        "faraday_constant_C_per_mol": F,
        "faraday_capacity_mAh_per_mol_e": F_MAH_PER_MOL,
        "lco_slope_mV_per_K": 0.83,
        "lco_slope_implied_reaction_entropy_J_per_molK": F * slope,
        "lco_basis_rule": "The arithmetic F*dU/dT is valid only after electrode/reaction direction and versus-Li sign are fixed.",
        "charge_order_0p47_implied_microV_per_K": 0.47 / F * 1.0e6,
        "charge_order_1p49_implied_microV_per_K": 1.49 / F * 1.0e6,
        "si_Li3p75Si_mAh_per_g": si_li375,
        "si_Li4p4Si_mAh_per_g": si_li44,
        "sio_2p8125_e_per_SiO_mAh_per_g": sio_li28125,
        "si_c_first_charge_ICE_fraction": 3117.0 / 3801.0,
        "si_c_first_charge_ICE_percent": 100.0 * 3117.0 / 3801.0,
        "capacity_basis_rule": "Theoretical, first-lithiation, first-delithiation/reversible, cycle-specific retained and active-mass-normalized capacities are distinct.",
        "external_truth_validated": False,
    }


def input_record(path: Path, expected_gate: str) -> dict[str, Any]:
    value = strict_load(path)
    if not isinstance(value, dict) or value.get("gate") != expected_gate:
        raise BuildError(f"input gate drift: {path.relative_to(REPO).as_posix()}")
    return {
        "path": path.relative_to(REPO).as_posix(),
        "raw_sha256": sha256(path.read_bytes()),
        "semantic_sha256": value.get("semantic_sha256"),
        "gate": value["gate"],
        "authority_ceiling": "PRIOR_INTERNAL_AUDIT_ROUTE_ONLY",
    }


def semantic_projection(data: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(data)
    projected.pop("semantic_sha256", None)
    return projected


def build() -> dict[str, Any]:
    topology = strict_load(TOPOLOGY)
    evidence, evidence_sha = parse_manual_evidence()
    if not isinstance(topology, dict):
        raise BuildError("Step 58 topology root")
    if topology.get("gate") != "PASS_P063_STEP58_SOURCE_PROCESS_TOPOLOGY":
        raise BuildError("Step 58 topology gate drift")
    if topology.get("baseline_commit") != BASELINE:
        raise BuildError("Step 58 topology baseline drift")

    source_rows, texts = source_texts(topology)
    citations, citation_commands = extract_citations(source_rows, texts)
    bibliography = extract_bibliography(source_rows, texts)
    manual_references = extract_manual_unkeyed_references(source_rows, texts)
    doi_rows = extract_dois(source_rows, texts)
    equations = extract_equation_candidates(source_rows, texts)
    claim_candidates = extract_line_claim_candidates(source_rows, texts)
    tex_delimited_math = extract_tex_delimited_math_candidates(source_rows, texts)
    conflicts = bibliography_conflicts(bibliography)

    source_partition_counts = dict(sorted(Counter(row["partition"] for row in source_rows).items()))
    bibliography_partition_counts = dict(sorted(Counter(row["partition"] for row in bibliography).items()))
    citation_partition_counts = dict(sorted(Counter(row["partition"] for row in citations).items()))
    doi_partition_counts = dict(sorted(Counter(row["partition"] for row in doi_rows).items()))
    equation_partition_counts = dict(sorted(Counter(row["partition"] for row in equations).items()))
    tex_delimited_math_partition_counts = dict(sorted(Counter(
        row["partition"] for row in tex_delimited_math
    ).items()))
    claim_kind_counts = dict(sorted(Counter(
        kind for row in claim_candidates for kind in row["candidate_kinds"]
    ).items()))
    findings = evidence.get("findings")
    if not isinstance(findings, list):
        raise BuildError("manual evidence findings must be a list")
    literature_claims = evidence.get("literature_claims")
    material_scope = evidence.get("material_scope_ledger")
    if not isinstance(literature_claims, list) or not isinstance(material_scope, list):
        raise BuildError("manual literature/material evidence missing")

    data: dict[str, Any] = {
        "schema_version": 1,
        "artifact_kind": "V1022_LITERATURE_QUANTITY_SCOPE_AUTHORITY",
        "generated_date": "2026-08-29",
        "phase": 63,
        "step": 60,
        "status": "PASS_WITH_CONCERNS",
        "gate": GATE,
        "baseline_commit": BASELINE,
        "expected_parent": EXPECTED_PARENT,
        "builder": {
            "path": BUILDER.relative_to(REPO).as_posix(),
            "normalized_sha256": sha256(normalized_bytes(BUILDER)),
            "raw_sha256": sha256(BUILDER.read_bytes()),
            "newline_policy": "LF_ONLY",
        },
        "input_artifacts": {
            "step58_topology": input_record(
                TOPOLOGY, "PASS_P063_STEP58_SOURCE_PROCESS_TOPOLOGY"
            ),
            "step59_rederivation": input_record(
                STEP59, "PASS_P063_STEP59_EQUATION_MATERIAL_REDERIVATION_WITH_CONCERNS"
            ),
            "phase062_material_scope": input_record(
                PRIOR_SCOPE, "PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS"
            ),
        },
        "result_first_contract": {
            "result_path": RESULT.relative_to(REPO).as_posix(),
            "evidence_semantic_sha256": evidence_sha,
            "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
            "persistence_claimed": False,
            "step61_blocked_until": "PASS_P063_STEP60_PERSISTENCE",
        },
        "denominator_policy": {
            "manifest_sources": "204 manifest occurrences; 200 FULL_TEXT and 4 FULL_PDF",
            "supplemental_source": "One separately identified supplemental process-control source is replayed but remains outside the 204-source manifest denominator.",
            "claim_candidates": "Deterministic lexical navigation rows are not proposition-level adjudications.",
            "bibliography_occurrences": "Repeated keys and proposal revisions remain occurrences; no deduplication erases provenance.",
        },
        "counts": {
            "manifest_text_sources": sum(row["manifest_member"] for row in source_rows),
            "supplemental_text_sources": sum(not row["manifest_member"] for row in source_rows),
            "all_reviewed_text_sources": len(source_rows),
            "source_partition_counts": source_partition_counts,
            "manifest_physical_lines": sum(row["physical_lines"] for row in source_rows if row["manifest_member"]),
            "supplemental_physical_lines": sum(row["physical_lines"] for row in source_rows if not row["manifest_member"]),
            "all_physical_lines": sum(row["physical_lines"] for row in source_rows),
            "citation_commands": citation_commands,
            "citation_key_occurrences": len(citations),
            "citation_partition_counts": citation_partition_counts,
            "bibliography_occurrences": len(bibliography),
            "manual_unkeyed_bibliography_occurrences": len(manual_references),
            "all_bibliography_record_occurrences": len(bibliography) + len(manual_references),
            "bibliography_partition_counts": bibliography_partition_counts,
            "bibliography_unique_keys": len({row["cite_key"] for row in bibliography}),
            "doi_occurrences": len(doi_rows),
            "doi_unique_normalized": len({row["normalized"] for row in doi_rows}),
            "doi_partition_counts": doi_partition_counts,
            "equation_candidates": len(equations),
            "equation_partition_counts": equation_partition_counts,
            "tex_delimited_math_candidates": len(tex_delimited_math),
            "tex_delimited_math_partition_counts": tex_delimited_math_partition_counts,
            "claim_candidate_lines": len(claim_candidates),
            "claim_candidate_kind_memberships": claim_kind_counts,
            "manual_literature_claims": len(literature_claims),
            "manual_material_scope_rows": len(material_scope),
            "findings": len(findings),
        },
        "source_read_attestations": source_rows,
        "final_release_citation_genealogy": topology["citation_genealogy"],
        "citation_occurrences_all_text_partitions": citations,
        "bibliography_occurrences_all_text_partitions": bibliography,
        "manual_unkeyed_bibliography_occurrences": manual_references,
        "doi_occurrences_all_text_partitions": doi_rows,
        "equation_candidates_all_text_partitions": equations,
        "tex_delimited_math_candidates_all_text_partitions": tex_delimited_math,
        "claim_candidate_lines_all_text_partitions": claim_candidates,
        "authority_axis_profiles": {
            LEXICAL_AUTHORITY_PROFILE_ID: {
                "axis_states": LEXICAL_AUTHORITY_PROFILE,
                "applies_to": [
                    "equation_candidates_all_text_partitions",
                    "tex_delimited_math_candidates_all_text_partitions",
                    "claim_candidate_lines_all_text_partitions",
                    "manual_unkeyed_bibliography_occurrences",
                ],
                "semantic_claim_adjudicated": False,
                "external_truth_promoted": False,
            }
        },
        "bibliography_identity_conflicts": conflicts,
        "manual_literature_scope_evidence": evidence,
        "independent_quantity_checks": quantity_checks(),
        "findings": findings,
        "finding_summary": dict(sorted(Counter(row["priority"] for row in findings).items())),
        "authority_boundary": {
            "frozen_source_modified": False,
            "network_contacted_by_builder": False,
            "bibliographic_existence_externally_validated": False,
            "fulltext_method_validated": False,
            "exact_equation_externally_validated": False,
            "exact_quantity_basis_externally_validated": False,
            "material_protocol_externally_validated": False,
            "model_mapping_externally_validated": False,
            "external_experimental_truth_validated": False,
            "primary_literature_truth_validated": False,
            "canonical_equation_accepted": False,
            "final_manuscript_ready": False,
            "downstream_owner": "Phase 071 primary literature truth; Phases 074-082 canonical derivation/material closure",
        },
    }
    data["semantic_sha256"] = sha256(compact_bytes(semantic_projection(data)))
    return data


def output_path(output_dir: str | None) -> Path:
    if output_dir is None:
        return OUTPUT
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    return directory / OUTPUT.name


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    data = build()
    path = output_path(args.output_dir)
    path.write_bytes(pretty_bytes(data))
    counts = data["counts"]
    print(
        "PASS_P063_STEP60_BUILD "
        f"sources={counts['all_reviewed_text_sources']} bib={counts['bibliography_occurrences']} "
        f"cites={counts['citation_key_occurrences']} doi={counts['doi_occurrences']} "
        f"equations={counts['equation_candidates']} texmath={counts['tex_delimited_math_candidates']} "
        f"claims={counts['claim_candidate_lines']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
