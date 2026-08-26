#!/usr/bin/env python3
"""Build Phase 061 Step 49 citation/background/equation authority evidence.

The builder inventories the 43 adopted v1.0.20 release-source occurrences from
frozen Git blobs.  It never imports or executes historical code and never treats
release text, bibliography presence, review rationale, or an equation hash as
external scientific validation.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


class BuildError(RuntimeError):
    """Controlled evidence-build failure."""


class DuplicateKeyError(BuildError):
    """Strict JSON duplicate-key failure."""


class NonFiniteNumberError(BuildError):
    """Strict JSON non-finite-number failure."""


REPO = Path(__file__).resolve().parents[3]
BASELINE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
INPUT_COMMIT = "5cf75ba2fd4e5707c53b164d361f1526c3d31f06"
GENERATED_DATE = "2026-08-26"

TOPOLOGY_PATH = Path("Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json")
PROCESS_PATH = Path("Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json")
LINEAGE_PATH = Path("Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json")
SNAPSHOT_PATH = Path("Codex/results/PHASE_061_V1020_SNAPSHOT_GENEALOGY.json")
CARRY_PATH = Path("Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json")
DEFAULT_OUTPUT = Path("Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json")

EXPECTED_INPUT_SHA256 = {
    TOPOLOGY_PATH.as_posix(): "0af27968b7896d2b5d462be6c9e1143e4e3985ffdd028b7f9f19a33924f9903c",
    PROCESS_PATH.as_posix(): "c5aabe37a42da12bfe44e8f7cee9de8a36a7cba7fcffc5aecd68d8832c77b403",
    LINEAGE_PATH.as_posix(): "25136896e4c93e509c9d92a748ba1d23337ebe60aa2736e5f569b70f6f1ed914",
    SNAPSHOT_PATH.as_posix(): "629995ab5936587840e5944c513ef86a0e82f114dd1d94860b06754fb9fdd414",
    CARRY_PATH.as_posix(): "72848094865e0b2cad1110df92e7543dc287607af45dc2346e2040bd65812271",
}

DISPLAY_ENVIRONMENTS = "equation|align|gather|multline|eqnarray|displaymath"
DISPLAY_RE = re.compile(
    rf"\\begin\{{(?P<env>(?:{DISPLAY_ENVIRONMENTS})\*?)\}}"
    rf"(?P<body>.*?)\\end\{{(?P=env)\}}",
    re.DOTALL,
)
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^{}]+)\}")
EQ_REFERENCE_RE = re.compile(r"(?<![A-Za-z0-9_])eq:[A-Za-z0-9_.:-]+")
CITE_RE = re.compile(
    r"\\(?P<command>cite|citep|citet|citealp|citeauthor|citeyear|parencite|"
    r"textcite|autocite|footcite|nocite)\*?\s*(?:\[[^\]]*\]\s*){0,2}"
    r"\{(?P<keys>[^{}]+)\}",
    re.IGNORECASE,
)
ATTRIBUTION_RE = re.compile(
    r"(\\cite|\bdoi\b|근거|출처|참고문헌|문헌|reference|reported|보고(?:하|되|된)|source)",
    re.IGNORECASE,
)
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
CODE_RE = re.compile(
    r"(\bPython\b|\bNumPy\b|\bSciPy\b|\bAPI\b|\bpytest\b|"
    r"\bdict\b|\btest_[A-Za-z0-9_]+\b|\b[A-Za-z0-9_]+\.py\b|"
    r"\\texttt\{|\\code\{|코드|구현|메서드|회귀\s*테스트)",
    re.IGNORECASE,
)
STRUCTURAL_PREFIXES = (
    "\\begin", "\\end", "\\label", "\\input", "\\include", "\\section",
    "\\subsection", "\\subsubsection", "\\paragraph", "\\chapter", "\\part",
    "\\documentclass", "\\usepackage", "\\newcommand", "\\renewcommand",
    "\\providecommand", "\\newtheorem", "\\setlength", "\\addtolength", "\\title", "\\author",
    "\\date", "\\maketitle", "\\tableofcontents", "\\bibliographystyle",
)
DESIGNATED_IMPLEMENTATION_PATHS = {
    "Claude/docs/v1.0.20/_sections/ch1_appB_codemap.tex",
    "Claude/docs/v1.0.20/_sections/ch2_appB_codemap.tex",
}
EQUATION_CLASSIFICATIONS = {
    "UNCHANGED": "UNCHANGED_SOURCE_MODEL",
    "MODIFIED": "ALGEBRAIC_RESTATEMENT",
    "NEW": "NEWLY_INTRODUCED_BACKGROUND_RELATION",
}
EQUATION_REVIEW_OVERRIDES = {
    "eq:sm-baresum": {
        "equation_classification": "NEWLY_INTRODUCED_BACKGROUND_RELATION",
        "substantive_delta_class": "NEW",
        "derivation_state": "SELF_CONTAINED_BOUNDED_DERIVATION",
        "review_note": "single-site grand-canonical derivation step added in v1.0.20",
    },
    "eq:sm-baremid": {
        "equation_classification": "NEWLY_INTRODUCED_BACKGROUND_RELATION",
        "substantive_delta_class": "NEW",
        "derivation_state": "SELF_CONTAINED_BOUNDED_DERIVATION",
        "review_note": "single-site grand-canonical derivation step added in v1.0.20",
    },
    "eq:sm-bare": {
        "equation_classification": "ALGEBRAIC_RESTATEMENT",
        "substantive_delta_class": "NEW",
        "derivation_state": "SELF_CONTAINED_BOUNDED_DERIVATION",
        "review_note": "single-site logistic result added with local derivation",
    },
    "eq:sm-exch": {
        "equation_classification": "NEWLY_INTRODUCED_BACKGROUND_RELATION",
        "substantive_delta_class": "NEW",
        "derivation_state": "BACKGROUND_RELATION_WITH_STATED_ASSUMPTIONS",
        "review_note": "exchange-symmetry background relation; primary support unverified",
    },
    "eq:sm-fdbe": {
        "equation_classification": "NEWLY_INTRODUCED_BACKGROUND_RELATION",
        "substantive_delta_class": "NEW",
        "derivation_state": "BACKGROUND_RELATION_WITH_STATED_ASSUMPTIONS",
        "review_note": "FD/BE comparison relation; primary support unverified",
    },
    "eq:lco-mottcrit": {
        "equation_classification": "NEWLY_INTRODUCED_BACKGROUND_RELATION",
        "substantive_delta_class": "NEW",
        "derivation_state": "GROUND_NOT_FOUND_BARE_HEURISTIC",
        "review_note": "W approximately 2zt heuristic lacks a source-local derivation and model-assumption closure",
    },
    "eq:lco-slots": {
        "equation_classification": "UNCHANGED_SOURCE_MODEL",
        "substantive_delta_class": "UNCHANGED_MATHEMATICAL_CONTENT_CROSS_REFERENCE_ONLY",
        "derivation_state": "INHERITED_SOURCE_MODEL_TEXTUAL_CROSS_REFERENCE_CHANGED",
        "review_note": "mathematical assignment is unchanged; only explanatory cross-reference text changed",
    },
}
NEGATIVE_CONTROL_IDS = (
    "citation-fake-doi-certainty",
    "citation-key-alias-collapse",
    "bibliography-presence-as-support",
    "equation-hash-as-validity",
    "review-consensus-promotion",
    "code-leakage-misclassification",
    "citation-drop-occurrence",
    "citation-duplicate-occurrence",
    "citation-orphan-suppression",
    "bibliography-drop-entry",
    "bibliography-conflict-suppression",
    "equation-drop-block",
    "equation-body-swap",
    "background-claim-drop",
    "background-nonclaim-promotion",
    "source-attribution-drop",
    "delta-link-swap",
    "rationale-as-support",
    "external-truth-promotion",
    "new-debt-alias-reuse",
    "main-body-code-allowlist-broadening",
    "competitive-candidate-promotion",
    "strict-json-duplicate-key",
    "strict-json-nonfinite",
    "cross-input-hash",
    "cross-baseline-commit",
    "cross-adopted-source-count",
    "cross-authority-row-coverage",
    "cross-unverified-route",
    "nested-schema-extra-key",
    "bibliography-text-fabrication",
    "prose-text-fabrication",
    "attribution-text-fabrication",
    "code-text-fabrication",
    "authority-semantic-row-swap",
    "builder-hash-mutation",
)


def _reject_constant(value: str) -> None:
    raise NonFiniteNumberError(value)


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def strict_load_bytes(data: bytes) -> Any:
    return json.loads(
        data.decode("utf-8"), object_pairs_hook=_object_pairs, parse_constant=_reject_constant
    )


def walk_finite(value: Any) -> tuple[int, int]:
    nodes, depth = 1, 1
    if isinstance(value, bool) or value is None or isinstance(value, (str, int)):
        return nodes, depth
    if isinstance(value, float):
        if not math.isfinite(value):
            raise NonFiniteNumberError(str(value))
        return nodes, depth
    if isinstance(value, list):
        children = [walk_finite(item) for item in value]
    elif isinstance(value, dict):
        children = []
        for key, item in value.items():
            if not isinstance(key, str):
                raise BuildError("JSON_NONSTRING_KEY")
            children.append(walk_finite(item))
    else:
        raise BuildError(f"JSON_TYPE:{type(value).__name__}")
    if children:
        nodes += sum(item[0] for item in children)
        depth += max(item[1] for item in children)
    return nodes, depth


def lf_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def load_input(path: Path) -> tuple[Any, dict[str, Any]]:
    data = (REPO / path).read_bytes()
    normalized = lf_bytes(data)
    actual = sha256(normalized)
    if actual != EXPECTED_INPUT_SHA256[path.as_posix()]:
        raise BuildError(f"INPUT_HASH:{path.as_posix()}:{actual}")
    parsed = strict_load_bytes(data)
    nodes, depth = walk_finite(parsed)
    return parsed, {
        "path": path.as_posix(),
        "sha256_lf_normalized": actual,
        "physical_lines": len(normalized.splitlines()),
        "nodes": nodes,
        "maximum_depth": depth,
    }


def git_blob_batch(shas: Iterable[str]) -> dict[str, bytes]:
    ordered = list(dict.fromkeys(shas))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=REPO,
        input=("\n".join(ordered) + "\n").encode("ascii"),
        check=False, capture_output=True, timeout=120,
    )
    if proc.returncode:
        raise BuildError(f"GIT_CAT_FILE_BATCH:{proc.returncode}")
    result: dict[str, bytes] = {}
    offset = 0
    for expected in ordered:
        newline = proc.stdout.find(b"\n", offset)
        if newline < 0:
            raise BuildError("GIT_CAT_FILE_HEADER_EOF")
        header = proc.stdout[offset:newline].decode("ascii")
        offset = newline + 1
        parts = header.split()
        if len(parts) != 3 or parts[0] != expected or parts[1] != "blob":
            raise BuildError(f"GIT_CAT_FILE_HEADER:{expected}:{header}")
        size = int(parts[2])
        data = proc.stdout[offset:offset + size]
        offset += size
        if proc.stdout[offset:offset + 1] != b"\n":
            raise BuildError(f"GIT_CAT_FILE_SEPARATOR:{expected}")
        offset += 1
        result[expected] = data
    if proc.stdout[offset:]:
        raise BuildError("GIT_CAT_FILE_TRAILING")
    return result


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def strip_latex_comment(line: str) -> str:
    for index, char in enumerate(line):
        preceding = len(line[:index]) - len(line[:index].rstrip("\\"))
        if char == "%" and preceding % 2 == 0:
            return line[:index]
    return line


def latex_without_comments(text: str) -> str:
    return "\n".join(strip_latex_comment(line) for line in text.splitlines())


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_doi_token(value: str) -> str:
    token = value.rstrip(".;}").lower()
    while token.endswith(")") and token.count(")") > token.count("("):
        token = token[:-1]
    return token


def bibliography_identity_fingerprint(item: dict[str, Any]) -> str:
    body = re.sub(r"\\bibitem(?:\[[^\]]*\])?\{[^{}]+\}", r"\\bibitem{}", item["normalized_body"], count=1)
    normalized = normalize_space(body).casefold()
    return sha256(normalized.encode("utf-8"))


def content_anchor(path: str, line_start: int, line_end: int, content: str) -> dict[str, Any]:
    return {
        "path": path,
        "line_start": line_start,
        "line_end": line_end,
        "sha256_lf_normalized": sha256(lf_bytes(content.encode("utf-8"))),
    }


def chapter_of(path: str) -> str:
    name = Path(path).name
    if name.startswith("ch1_") or "_ch1_" in name or "graphite_ica_ch1_" in name:
        return "CH1"
    if name.startswith("ch2_") or "_ch2_" in name or "graphite_ica_ch2_" in name:
        return "CH2"
    return "NON_CHAPTER"


def surface_class(path: str) -> str:
    name = Path(path).name
    if path.endswith((".py", ".md")):
        return "PACKAGE_COMPANION"
    if path in DESIGNATED_IMPLEMENTATION_PATHS:
        return "DESIGNATED_IMPLEMENTATION_APPENDIX"
    if name in {"graphite_ica_ch1_v1.0.20.tex", "graphite_ica_ch2_v1.0.20.tex"}:
        return "ROOT_WRAPPER"
    if name.endswith("_preamble.tex"):
        return "PREAMBLE"
    if name.endswith("_bib.tex"):
        return "BIBLIOGRAPHY"
    return "SCHOLARLY_MAIN_BODY"


def bibliography_records(text: str, path: str) -> list[dict[str, Any]]:
    clean = latex_without_comments(text)
    matches = list(BIBITEM_RE.finditer(clean))
    records: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(clean)
        boundary = clean.find("\\end{thebibliography}", match.end(), end)
        if boundary >= 0:
            end = boundary
        body = clean[match.start():end].strip()
        doi_sequence = [normalize_doi_token(token) for token in DOI_RE.findall(body)]
        doi_tokens = sorted(set(doi_sequence))
        records.append({
            "key": match.group(1).strip(),
            "body": body,
            "normalized_body": normalize_space(body),
            "doi_tokens": doi_tokens,
            "primary_doi_token": doi_sequence[0] if doi_sequence else None,
            "doi_occurrences": [
                {
                    "doi_token": token,
                    "role": "ENTRY_PRIMARY_IDENTIFIER" if doi_index == 0 else "ANNOTATION_CROSS_REFERENCE",
                    "metadata_verified": False,
                }
                for doi_index, token in enumerate(doi_sequence)
            ],
            "bibliography_source_kind": "INTERNAL_SELF_REPORT" if "내부" in body or "본 연구" in body else "EXTERNAL_METADATA_UNVERIFIED",
            "anchor": content_anchor(path, line_number(clean, match.start()), line_number(clean, end), body),
        })
    return records


def citation_records(text: str, path: str) -> list[dict[str, Any]]:
    clean = latex_without_comments(text)
    lines = clean.splitlines()
    records: list[dict[str, Any]] = []
    for match in CITE_RE.finditer(clean):
        line = line_number(clean, match.start())
        keys = [key.strip() for key in match.group("keys").split(",") if key.strip()]
        context = normalize_space(lines[line - 1] if line <= len(lines) else match.group(0))
        records.append({
            "command": match.group("command").lower(),
            "keys": keys,
            "raw": match.group(0),
            "context": context,
            "signature": f"{match.group('command').lower()}|{','.join(keys)}",
            "exact_signature": f"{match.group('command').lower()}|{','.join(keys)}|{context}",
            "anchor": content_anchor(path, line, line, lines[line - 1] if line <= len(lines) else match.group(0)),
        })
    return records


def bracket_display_spans(text: str) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    index = 0
    while index < len(text) - 1:
        if text[index:index + 2] != r"\[":
            index += 1
            continue
        preceding = 0
        cursor = index - 1
        while cursor >= 0 and text[cursor] == "\\":
            preceding += 1
            cursor -= 1
        if preceding % 2:
            index += 2
            continue
        end = index + 2
        while end < len(text) - 1:
            if text[end:end + 2] == r"\]":
                before = 0
                cursor = end - 1
                while cursor >= 0 and text[cursor] == "\\":
                    before += 1
                    cursor -= 1
                if before % 2 == 0:
                    spans.append((index, end + 2, text[index + 2:end]))
                    index = end + 2
                    break
            end += 1
        else:
            raise BuildError("UNTERMINATED_BRACKET_DISPLAY")
    return spans


def equation_records(text: str, path: str) -> list[dict[str, Any]]:
    clean = latex_without_comments(text)
    candidates: list[tuple[int, int, str, str]] = []
    for match in DISPLAY_RE.finditer(clean):
        candidates.append((match.start(), match.end(), match.group("env"), match.group("body")))
    for start, end, body in bracket_display_spans(clean):
        if not any(a <= start < b for a, b, _, _ in candidates):
            candidates.append((start, end, "bracket-display", body))
    records: list[dict[str, Any]] = []
    for start, end, environment, body in sorted(candidates):
        labels = LABEL_RE.findall(body)
        normalized = normalize_space(LABEL_RE.sub("", body))
        body_hash = sha256(normalized.encode("utf-8"))
        identity = labels[0] if labels else "body:" + body_hash
        records.append({
            "environment": environment,
            "labels": labels,
            "semantic_identity": identity,
            "normalized_body": normalized,
            "body_sha256": body_hash,
            "anchor": content_anchor(path, line_number(clean, start), line_number(clean, end), clean[start:end]),
        })
    return records


def multiset_delta(new: list[dict[str, Any]], old: list[dict[str, Any]], exact_key: str, loose_key: str) -> list[str]:
    exact = collections.Counter(item[exact_key] for item in old)
    loose = collections.Counter(item[loose_key] for item in old)
    result: list[str] = []
    for item in new:
        if exact[item[exact_key]]:
            result.append("UNCHANGED")
            exact[item[exact_key]] -= 1
            loose[item[loose_key]] -= 1
        elif loose[item[loose_key]]:
            result.append("MODIFIED")
            loose[item[loose_key]] -= 1
        else:
            result.append("NEW")
    return result


def prose_candidate(line: str, path: str) -> tuple[str, str] | None:
    clean = normalize_space(strip_latex_comment(line))
    if not clean or clean.startswith(STRUCTURAL_PREFIXES) or clean.startswith("\\bibitem"):
        return None
    if clean in {"{", "}", "\\[", "\\]", "\\(", "\\)"}:
        return None
    if path in DESIGNATED_IMPLEMENTATION_PATHS:
        return "IMPLEMENTATION_ONLY", clean
    letters = len(re.findall(r"[A-Za-z가-힣]", clean))
    if letters < 8:
        return "NON_CLAIM", clean
    return "BACKGROUND_CLAIM", clean


def source_attributions(text: str, path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(text.splitlines(), 1):
        clean = normalize_space(strip_latex_comment(line))
        if clean and ATTRIBUTION_RE.search(clean):
            cite_keys = [key.strip() for match in CITE_RE.finditer(clean) for key in match.group("keys").split(",") if key.strip()]
            doi_tokens = [normalize_doi_token(token) for token in DOI_RE.findall(clean)]
            eq_tokens = EQ_REFERENCE_RE.findall(clean)
            keyword_classes = sorted({
                keyword for keyword in ("근거", "출처", "참고문헌", "문헌", "reference", "reported", "보고", "source")
                if keyword.lower() in clean.lower()
            })
            loose_parts = [*cite_keys, *doi_tokens, *eq_tokens, *keyword_classes]
            rows.append({
                "text": clean,
                "exact_signature": clean,
                "loose_signature": "|".join(loose_parts) if loose_parts else "ATTRIBUTION_GENERIC",
                "citation_keys": cite_keys,
                "doi_tokens": doi_tokens,
                "equation_references": eq_tokens,
                "keyword_classes": keyword_classes,
                "anchor": content_anchor(path, number, number, line),
            })
    return rows


def pair_attribution_delta(new: list[dict[str, Any]], old: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unused = set(range(len(old)))
    result: list[dict[str, Any]] = []
    for item in new:
        exact = next((index for index in sorted(unused) if old[index]["exact_signature"] == item["exact_signature"]), None)
        if exact is not None:
            unused.remove(exact)
            result.append({"delta_class": "UNCHANGED", "old_anchor": old[exact]["anchor"], "old_exact_signature": old[exact]["exact_signature"]})
            continue
        loose = next((index for index in sorted(unused) if old[index]["loose_signature"] == item["loose_signature"]), None)
        if loose is not None:
            unused.remove(loose)
            result.append({"delta_class": "MODIFIED", "old_anchor": old[loose]["anchor"], "old_exact_signature": old[loose]["exact_signature"]})
        else:
            result.append({"delta_class": "NEW", "old_anchor": None, "old_exact_signature": None})
    return result


def code_mentions(text: str, path: str) -> list[dict[str, Any]]:
    allowed = path in DESIGNATED_IMPLEMENTATION_PATHS
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(text.splitlines(), 1):
        clean = normalize_space(strip_latex_comment(line))
        scan = re.sub(r"\\code\{eq:[^{}]+\}", "", clean)
        if scan and not clean.startswith(STRUCTURAL_PREFIXES) and CODE_RE.search(scan):
            rows.append({
                "text": clean,
                "allowed_surface": allowed,
                "disposition": "DESIGNATED_IMPLEMENTATION_APPENDIX" if allowed else "MAIN_BODY_CODE_LEAKAGE_CANDIDATE",
                "anchor": content_anchor(path, number, number, line),
            })
    return rows


def companion_equation_references(text: str, path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(text.splitlines(), 1):
        for match in EQ_REFERENCE_RE.finditer(line):
            token = match.group(0).rstrip(".:-")
            rows.append({
                "equation_reference": token,
                "context": normalize_space(line),
                "anchor": content_anchor(path, number, number, line),
                "surface_class": "PACKAGE_COMPANION",
                "formal_scholarly_citation": False,
                "primary_support_state": "NOT_PRIMARY_SUPPORT",
            })
    return rows


def authority_common(row: dict[str, Any], asset_type: str, delta_class: str, anchor: dict[str, Any]) -> dict[str, Any]:
    return {
        "asset_type": asset_type,
        "chapter": chapter_of(row["v1020"]["path"]),
        "document_root": chapter_of(row["v1020"]["path"]),
        "surface_class": surface_class(row["v1020"]["path"]),
        "source_id": row["step47_authority_source_id"],
        "source_record_sha256": row["v1020"]["sha256_lf_normalized"],
        "delta_id": row["delta_id"],
        "delta_class": delta_class,
        "source_anchor": anchor,
        "process_rationale_link": row["step47_authority"]["evidence_route"],
        "rationale_is_support": False,
        "release_source_is_primary_scientific_support": False,
        "review_approval_is_scientific_support": False,
        "primary_support_state": "UNVERIFIED_EXTERNAL",
        "external_scientific_truth": False,
        "external_material_truth": False,
        "scientific_authority_promoted": False,
        "authority_ceiling": "INTERNAL_RELEASE_TEXT_AND_METADATA_CONSISTENCY_ONLY",
        "carry_forward_links": ["P061-UNV-001", "P061-UNV-002", "P061-UNV-004"],
        "target_phase": 71,
    }


def build() -> dict[str, Any]:
    topology, topology_meta = load_input(TOPOLOGY_PATH)
    process, process_meta = load_input(PROCESS_PATH)
    lineage, lineage_meta = load_input(LINEAGE_PATH)
    snapshot, snapshot_meta = load_input(SNAPSHOT_PATH)
    carry, carry_meta = load_input(CARRY_PATH)
    if topology.get("status") != "PASS_SOURCE_IDENTITY_TOPOLOGY":
        raise BuildError("TOPOLOGY_GATE")
    if process.get("gate") != "PASS_WITH_CONCERNS":
        raise BuildError("PROCESS_GATE")
    if lineage.get("gate") != "PASS_P061_STEP48_LINEAGE_DIFF":
        raise BuildError("LINEAGE_GATE")
    if snapshot.get("gate") != "PASS_P061_STEP48_LINEAGE_DIFF":
        raise BuildError("SNAPSHOT_GATE")
    snapshot_ch1_eq = snapshot.get("baseline_to_final", {}).get("ch1", {}).get("eqblocks", {}).get("count_after")
    snapshot_ch2_eq = snapshot.get("baseline_to_final", {}).get("ch2", {}).get("eqblocks", {}).get("count_after")
    if (snapshot_ch1_eq, snapshot_ch2_eq) != (128, 32):
        raise BuildError("SNAPSHOT_EQUATION_DENOMINATOR")
    carry_summary = carry.get("gate_summary", {})
    if (
        carry_summary.get("carry_forward_expected") != 52
        or carry_summary.get("new_blocker_count") != 5
        or carry_summary.get("acceptance_satisfied_count") != 0
        or carry_summary.get("resolution_status_counts") != {"NOT_RESOLVED": 52}
    ):
        raise BuildError("CARRY_FORWARD_GATE")

    adopted: list[dict[str, Any]] = []
    source_by_path = {item["path"]: item for item in process["source_routes"]}
    for source in lineage["delta_rows"]:
        route = source_by_path[source["v1020"]["path"]]
        if route["source_authority_class"] == "ADOPTED_RELEASE_SOURCE":
            enriched = dict(source)
            enriched["step47_authority_source_id"] = route["source_id"]
            adopted.append(enriched)
    adopted.sort(key=lambda item: item["step47_authority_source_id"])
    if len(adopted) != 43:
        raise BuildError(f"ADOPTED_SOURCE_COUNT:{len(adopted)}")
    if sum(item["v1020"]["path"].endswith(".tex") for item in adopted) != 41:
        raise BuildError("ADOPTED_TEX_COUNT")

    shas: list[str] = []
    for row in adopted:
        shas.append(row["v1020"]["blob_sha1"])
        if row.get("v1019"):
            shas.append(row["v1019"]["blob_sha1"])
    blobs = git_blob_batch(shas)

    source_coverage: list[dict[str, Any]] = []
    all_bib: list[dict[str, Any]] = []
    all_old_bib: list[dict[str, Any]] = []
    all_cites: list[dict[str, Any]] = []
    all_equations: list[dict[str, Any]] = []
    all_prose: list[dict[str, Any]] = []
    all_attributions: list[dict[str, Any]] = []
    all_code: list[dict[str, Any]] = []
    all_companion_equation_references: list[dict[str, Any]] = []

    for row in adopted:
        path = row["v1020"]["path"]
        new_data = lf_bytes(blobs[row["v1020"]["blob_sha1"]])
        if sha256(new_data) != row["v1020"]["sha256_lf_normalized"]:
            raise BuildError(f"NEW_BLOB_HASH:{row['delta_id']}")
        new_text = new_data.decode("utf-8")
        old_text = ""
        if row.get("v1019"):
            old_data = lf_bytes(blobs[row["v1019"]["blob_sha1"]])
            if sha256(old_data) != row["v1019"]["sha256_lf_normalized"]:
                raise BuildError(f"OLD_BLOB_HASH:{row['delta_id']}")
            old_text = old_data.decode("utf-8")

        review_evidence = {
            "evidence_path": "Codex/results/PHASE_061_STEP_049_CITATION_AUTHORITY_RESULT.md",
            "reviewer_partition": "CH1_FULL_READ" if chapter_of(path) == "CH1" else ("CH2_FULL_READ" if chapter_of(path) == "CH2" else "COMPANION_FULL_READ"),
            "reviewed_range": f"1-{len(new_data.splitlines())}",
            "review_mode": "HUMAN_FULL_TEXT_PLUS_INDEPENDENT_FROZEN_BLOB_CROSSCHECK",
            "frozen_source_sha256": sha256(new_data),
        }
        review_evidence["evidence_record_sha256"] = sha256(canonical_json_bytes(review_evidence))
        source_coverage.append({
            "source_id": row["step47_authority_source_id"],
            "delta_id": row["delta_id"],
            "path": path,
            "role": row["v1020"]["role"],
            "surface_class": surface_class(path),
            "comparison_class": row["comparison_class"],
            "physical_lines": len(new_data.splitlines()),
            "sha256_lf_normalized": sha256(new_data),
            "full_text_read": True,
            "review_evidence": review_evidence,
            "inventory_scope": "CITATION_BIB_EQUATION_PROSE_ATTRIBUTION_CODE" if path.endswith(".tex") else "ATTRIBUTION_AND_COMPANION_BOUNDARY",
        })

        attributions = source_attributions(new_text, path)
        old_attributions = source_attributions(old_text, row["v1019"]["path"] if row.get("v1019") else path)
        attribution_delta = pair_attribution_delta(attributions, old_attributions)
        for item, delta in zip(attributions, attribution_delta):
            line = item["anchor"]["line_start"]
            segment_link = None
            for segment_index, segment in enumerate((row.get("text_delta") or {}).get("segments", []), 1):
                if segment["new_line_start"] <= line <= segment["new_line_end"]:
                    segment_link = {
                        "segment_index": segment_index,
                        "segment_sha256": segment["segment_sha256"],
                        "tag": segment["tag"],
                        "old_line_start": segment["old_line_start"],
                        "old_line_end": segment["old_line_end"],
                        "new_line_start": segment["new_line_start"],
                        "new_line_end": segment["new_line_end"],
                    }
                    break
            item.update({
                "source_id": row["step47_authority_source_id"],
                "delta_id": row["delta_id"],
                "chapter": chapter_of(path),
                "surface_class": surface_class(path),
                "delta_class": delta["delta_class"],
                "old_anchor": delta["old_anchor"],
                "old_exact_signature": delta["old_exact_signature"],
                "delta_segment_link": segment_link,
                "authority_disposition": "STRUCTURAL_ATTRIBUTION_ONLY_NOT_PRIMARY_SUPPORT",
                "primary_support_state": "UNVERIFIED_EXTERNAL",
                "external_scientific_truth": False,
            })
        all_attributions.extend(attributions)

        if not path.endswith(".tex"):
            references = companion_equation_references(new_text, path)
            for item in references:
                item.update({"source_id": row["step47_authority_source_id"], "delta_id": row["delta_id"]})
            all_companion_equation_references.extend(references)
            continue

        new_bib = bibliography_records(new_text, path)
        old_bib = bibliography_records(old_text, row["v1019"]["path"] if row.get("v1019") else path)
        for item in old_bib:
            item.update({"chapter": chapter_of(path)})
        all_old_bib.extend(old_bib)
        old_bib_by_key = {item["key"]: item for item in old_bib}
        for item in new_bib:
            old = old_bib_by_key.get(item["key"])
            delta = "NEW" if old is None else ("UNCHANGED" if old["normalized_body"] == item["normalized_body"] else "MODIFIED")
            item.update({"delta_class": delta, "source_id": row["step47_authority_source_id"], "delta_id": row["delta_id"], "chapter": chapter_of(path)})
        all_bib.extend(new_bib)

        new_cites = citation_records(new_text, path)
        old_cites = citation_records(old_text, row["v1019"]["path"] if row.get("v1019") else path)
        cite_delta = multiset_delta(new_cites, old_cites, "exact_signature", "signature")
        for item, delta in zip(new_cites, cite_delta):
            item.update({"delta_class": delta, "source_id": row["step47_authority_source_id"], "delta_id": row["delta_id"], "chapter": chapter_of(path)})
        all_cites.extend(new_cites)

        new_eq = equation_records(new_text, path)
        old_eq = equation_records(old_text, row["v1019"]["path"] if row.get("v1019") else path)
        old_by_identity = {item["semantic_identity"]: item for item in old_eq}
        old_by_body = collections.defaultdict(list)
        for item in old_eq:
            old_by_body[item["body_sha256"]].append(item)
        for item in new_eq:
            old = old_by_identity.get(item["semantic_identity"])
            if old and old["body_sha256"] == item["body_sha256"]:
                delta = "UNCHANGED"
            elif old or old_by_body.get(item["body_sha256"]):
                delta = "MODIFIED"
            else:
                delta = "NEW"
            item.update({"delta_class": delta, "source_id": row["step47_authority_source_id"], "delta_id": row["delta_id"], "chapter": chapter_of(path)})
            override = EQUATION_REVIEW_OVERRIDES.get(item["semantic_identity"])
            item["substantive_delta_class"] = override["substantive_delta_class"] if override else delta
            item["semantic_review_note"] = override["review_note"] if override else "no v1.0.20 textual equation delta requiring manual override"
        all_equations.extend(new_eq)

        code = code_mentions(new_text, path)
        for item in code:
            item.update({"source_id": row["step47_authority_source_id"], "delta_id": row["delta_id"], "chapter": chapter_of(path)})
        all_code.extend(code)

        if row.get("text_delta"):
            for segment_index, segment in enumerate(row["text_delta"]["segments"], 1):
                for offset, line in enumerate(segment["new_lines"]):
                    disposition = prose_candidate(line, path)
                    if disposition is None:
                        continue
                    kind, clean = disposition
                    number = segment["new_line_start"] + offset
                    all_prose.append({
                        "candidate_id": "",
                        "disposition": kind,
                        "text": clean,
                        "source_id": row["step47_authority_source_id"],
                        "delta_id": row["delta_id"],
                        "segment_index": segment_index,
                        "segment_sha256": segment["segment_sha256"],
                        "delta_class": "NEW" if segment["tag"] == "insert" else "MODIFIED",
                        "chapter": chapter_of(path),
                        "anchor": content_anchor(path, number, number, line),
                    })

    for index, row in enumerate(all_prose, 1):
        row["candidate_id"] = f"P061-PROSE-{index:04d}"
    for index, row in enumerate(all_attributions, 1):
        row["statement_id"] = f"P061-ATTR-{index:04d}"

    bib_by_chapter_key: dict[tuple[str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for item in all_bib:
        bib_by_chapter_key[(item["chapter"], item["key"])].append(item)
    cite_key_occurrences: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    orphan_rows: list[dict[str, Any]] = []
    for occurrence_index, cite in enumerate(all_cites, 1):
        cite["occurrence_id"] = f"P061-CITE-{occurrence_index:04d}"
        resolutions: list[dict[str, Any]] = []
        for key in cite["keys"]:
            matches = bib_by_chapter_key.get((cite["chapter"], key), [])
            state = "RESOLVED_EXACTLY_ONCE" if len(matches) == 1 else ("ORPHAN" if not matches else "DUPLICATE_KEY")
            resolutions.append({"key": key, "metadata_resolution": state, "matching_entries": len(matches), "primary_support_state": "UNVERIFIED_EXTERNAL"})
            cite_key_occurrences[(cite["chapter"], key)].append(cite["occurrence_id"])
            if state != "RESOLVED_EXACTLY_ONCE":
                orphan_rows.append({"occurrence_id": cite["occurrence_id"], "chapter": cite["chapter"], "key": key, "state": state, "anchor": cite["anchor"]})
        cite["key_resolutions"] = resolutions

    bibliography_conflicts: list[dict[str, Any]] = []
    for (chapter, key), entries in sorted(bib_by_chapter_key.items()):
        bodies = sorted({item["normalized_body"] for item in entries})
        if len(entries) > 1:
            bibliography_conflicts.append({"chapter": chapter, "key": key, "entry_count": len(entries), "distinct_bodies": len(bodies), "state": "DUPLICATE_IDENTICAL" if len(bodies) == 1 else "CONFLICT"})

    defined_not_cited: list[dict[str, Any]] = []
    for (chapter, key), entries in sorted(bib_by_chapter_key.items()):
        if (chapter, key) not in cite_key_occurrences:
            defined_not_cited.append({
                "chapter": chapter,
                "key": key,
                "entry_anchors": [item["anchor"] for item in entries],
                "state": "DEFINED_NOT_CITED_IN_DOCUMENT_ROOT",
            })

    mixed_style_keys = [
        {"chapter": item["chapter"], "key": item["key"], "anchor": item["anchor"], "auto_rename_allowed": False}
        for item in all_bib
        if re.fullmatch(r"[a-z][a-z0-9_:-]*", item["key"]) is None
    ]

    cross_chapter_key_groups: list[dict[str, Any]] = []
    by_global_key: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for item in all_bib:
        by_global_key[item["key"]].append(item)
    for key, entries in sorted(by_global_key.items()):
        if len({item["chapter"] for item in entries}) > 1:
            doi_sets = sorted({tuple(item["doi_tokens"]) for item in entries})
            cross_chapter_key_groups.append({
                "key": key,
                "chapters": sorted({item["chapter"] for item in entries}),
                "entry_count": len(entries),
                "doi_token_sets": [list(tokens) for tokens in doi_sets],
                "metadata_state": "DOI_TOKEN_CONSISTENT_UNVERIFIED_EXTERNAL" if len(doi_sets) == 1 else "DOI_TOKEN_CONFLICT_OR_MISSING",
                "chapter_scoped_identities_preserved": True,
                "alias_collapsed": False,
            })

    doi_token_index: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    for item in all_bib:
        for token in item["doi_tokens"]:
            doi_token_index[token].append({"chapter": item["chapter"], "key": item["key"]})

    authority_rows: list[dict[str, Any]] = []
    adopted_by_delta = {item["delta_id"]: item for item in adopted}
    for bib_index, item in enumerate(all_bib, 1):
        source = adopted_by_delta[item["delta_id"]]
        auth = authority_common(source, "BIB_ENTRY", item["delta_class"], item["anchor"])
        matches = bib_by_chapter_key[(item["chapter"], item["key"])]
        auth.update({
            "asset_id": f"P061-AUTH-BIB-{bib_index:04d}",
            "bibliography_key": item["key"],
            "metadata_state": "CONSISTENT_PRESENT_UNVERIFIED" if len(matches) == 1 else "DUPLICATE_OR_CONFLICT",
            "derivation_state": "NOT_APPLICABLE",
        })
        authority_rows.append(auth)
    for cite_index, item in enumerate(all_cites, 1):
        source = adopted_by_delta[item["delta_id"]]
        auth = authority_common(source, "CITATION_OCCURRENCE", item["delta_class"], item["anchor"])
        states = {entry["metadata_resolution"] for entry in item["key_resolutions"]}
        auth.update({
            "asset_id": f"P061-AUTH-CITE-{cite_index:04d}",
            "occurrence_id": item["occurrence_id"],
            "citation_keys": item["keys"],
            "metadata_state": "CONSISTENT_PRESENT_UNVERIFIED" if states == {"RESOLVED_EXACTLY_ONCE"} else "ORPHAN_OR_CONFLICT",
            "derivation_state": "NOT_APPLICABLE",
        })
        authority_rows.append(auth)
    for eq_index, item in enumerate(all_equations, 1):
        source = adopted_by_delta[item["delta_id"]]
        auth = authority_common(source, "EQUATION", item["delta_class"], item["anchor"])
        override = EQUATION_REVIEW_OVERRIDES.get(item["semantic_identity"])
        auth.update({
            "asset_id": f"P061-AUTH-EQ-{eq_index:04d}",
            "semantic_identity": item["semantic_identity"],
            "equation_body_sha256": item["body_sha256"],
            "equation_classification": override["equation_classification"] if override else EQUATION_CLASSIFICATIONS[item["delta_class"]],
            "substantive_delta_class": item["substantive_delta_class"],
            "metadata_state": "NOT_APPLICABLE",
            "derivation_state": override["derivation_state"] if override else ("INHERITED_SOURCE_DERIVATION_NOT_REAUDITED" if item["delta_class"] == "UNCHANGED" else "UNVERIFIED_DERIVATION_PROVENANCE"),
            "assumption_state": "UNVERIFIED_EXTERNAL",
            "hash_is_scientific_validity": False,
        })
        authority_rows.append(auth)
    background = [item for item in all_prose if item["disposition"] == "BACKGROUND_CLAIM"]
    for claim_index, item in enumerate(background, 1):
        source = adopted_by_delta[item["delta_id"]]
        auth = authority_common(source, "BACKGROUND_CLAIM", item["delta_class"], item["anchor"])
        auth.update({
            "asset_id": f"P061-AUTH-CLAIM-{claim_index:04d}",
            "candidate_id": item["candidate_id"],
            "metadata_state": "CLAIM_LEVEL_SOURCE_LINK_UNVERIFIED",
            "derivation_state": "UNVERIFIED_CLAIM_PROVENANCE",
        })
        authority_rows.append(auth)
    for attribution_index, item in enumerate(all_attributions, 1):
        source = adopted_by_delta[item["delta_id"]]
        auth = authority_common(source, "SOURCE_ATTRIBUTION_STATEMENT", item["delta_class"], item["anchor"])
        auth.update({
            "asset_id": f"P061-AUTH-ATTR-{attribution_index:04d}",
            "statement_id": item["statement_id"],
            "old_anchor": item["old_anchor"],
            "delta_segment_link": item["delta_segment_link"],
            "metadata_state": "ATTRIBUTION_IDENTITY_INVENTORIED_PRIMARY_SUPPORT_UNVERIFIED",
            "derivation_state": "NOT_APPLICABLE",
            "authority_disposition": item["authority_disposition"],
        })
        authority_rows.append(auth)

    expected_authority_ids = {
        *(f"P061-AUTH-BIB-{index:04d}" for index in range(1, len(all_bib) + 1)),
        *(f"P061-AUTH-CITE-{index:04d}" for index in range(1, len(all_cites) + 1)),
        *(f"P061-AUTH-EQ-{index:04d}" for index in range(1, len(all_equations) + 1)),
        *(f"P061-AUTH-CLAIM-{index:04d}" for index in range(1, len(background) + 1)),
        *(f"P061-AUTH-ATTR-{index:04d}" for index in range(1, len(all_attributions) + 1)),
    }
    actual_authority_ids = [item["asset_id"] for item in authority_rows]
    if len(actual_authority_ids) != len(set(actual_authority_ids)) or set(actual_authority_ids) != expected_authority_ids:
        raise BuildError("AUTHORITY_ASSET_BIJECTION")

    authority_groups: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for item in authority_rows:
        authority_groups[item["asset_type"]].append(item)
    semantic_contracts = (
        (
            "BIB_ENTRY", all_bib,
            lambda item: {
                "bibliography_key": item["key"],
            },
        ),
        (
            "CITATION_OCCURRENCE", all_cites,
            lambda item: {
                "occurrence_id": item["occurrence_id"],
                "citation_keys": item["keys"],
            },
        ),
        (
            "EQUATION", all_equations,
            lambda item: {
                "semantic_identity": item["semantic_identity"],
                "equation_body_sha256": item["body_sha256"],
                "substantive_delta_class": item["substantive_delta_class"],
            },
        ),
        (
            "BACKGROUND_CLAIM", background,
            lambda item: {
                "candidate_id": item["candidate_id"],
            },
        ),
        (
            "SOURCE_ATTRIBUTION_STATEMENT", all_attributions,
            lambda item: {
                "statement_id": item["statement_id"],
                "old_anchor": item["old_anchor"],
                "delta_segment_link": item["delta_segment_link"],
                "authority_disposition": item["authority_disposition"],
            },
        ),
    )
    for asset_type, assets, projection in semantic_contracts:
        rows = authority_groups[asset_type]
        if len(rows) != len(assets):
            raise BuildError(f"AUTHORITY_SEMANTIC_BIJECTION:{asset_type}:COUNT")
        for row, asset in zip(rows, assets):
            expected_semantics = {
                "asset_type": asset_type,
                "source_id": asset["source_id"],
                "delta_id": asset["delta_id"],
                "chapter": asset["chapter"],
                "document_root": asset["chapter"],
                "delta_class": asset["delta_class"],
                "source_anchor": asset["anchor"],
                **projection(asset),
            }
            if any(row.get(key) != value for key, value in expected_semantics.items()):
                raise BuildError(f"AUTHORITY_SEMANTIC_BIJECTION:{asset_type}:{row.get('asset_id')}")

    new_or_modified_expected = (
        sum(item["delta_class"] != "UNCHANGED" for item in all_bib)
        + sum(item["delta_class"] != "UNCHANGED" for item in all_cites)
        + sum(item["delta_class"] != "UNCHANGED" for item in all_equations)
        + len(background)
        + sum(item["delta_class"] != "UNCHANGED" for item in all_attributions)
    )
    new_or_modified_actual = sum(
        row["delta_class"] != "UNCHANGED" for row in authority_rows
    )
    if new_or_modified_expected != new_or_modified_actual:
        raise BuildError("AUTHORITY_ROW_COVERAGE")

    old_global_keys = {item["key"] for item in all_old_bib}
    old_global_doi_tokens = {token for item in all_old_bib for token in item["doi_tokens"]}
    old_global_metadata_fingerprints = {bibliography_identity_fingerprint(item) for item in all_old_bib}
    new_bibliography_occurrences = [item for item in all_bib if item["delta_class"] == "NEW"]
    identity_match_basis = {
        (item["chapter"], item["key"]): [
            *(["GLOBAL_KEY_SPELLING"] if item["key"] in old_global_keys else []),
            *(["ANY_DOI_TOKEN"] if set(item["doi_tokens"]) & old_global_doi_tokens else []),
            *(["NORMALIZED_METADATA_FINGERPRINT"] if bibliography_identity_fingerprint(item) in old_global_metadata_fingerprints else []),
        ]
        for item in new_bibliography_occurrences
    }
    genuinely_new_source_entries = [
        item for item in new_bibliography_occurrences
        if not identity_match_basis[(item["chapter"], item["key"])]
    ]
    new_alias_occurrences = [item for item in new_bibliography_occurrences if item not in genuinely_new_source_entries]
    inherited_debts = [
        item for item in process["unverified_queue"]
        if item["queue_id"] in {"P061-UNV-001", "P061-UNV-002", "P061-UNV-004", "P061-UNV-006"}
    ]
    inherited_carry_projection = [
        {
            "carry_forward_id": item["carry_forward_id"],
            "source_record_sha256": sha256(canonical_json_bytes(item)),
            "prior_record_sha256": item["prior_record_sha256"],
            "status_before": item["status_before"],
            "status_after": item["status_after"],
            "resolution_status": item["resolution_status"],
            "acceptance_satisfied": item["acceptance_satisfied"],
            "target_phase_before": item["target_phase_before"],
            "target_phase_after": item["target_phase_after"],
            "target_horizon_before": item["target_horizon_before"],
            "target_horizon_after": item["target_horizon_after"],
            "category_after": item["category_after"],
            "acceptance_criterion_after": item["acceptance_criterion_after"],
            "authority_boundary_after": item["authority_boundary_after"],
            "source_route_source_id": item["source_route_source_id"],
            "external_scientific_truth_validated": item["external_scientific_truth_validated"],
            "external_material_truth_validated": item["external_material_truth_validated"],
            "step49_resolution_changed": False,
        }
        for item in carry["inherited_items"]
    ]
    inherited_blocker_projection = [
        {
            "blocker_id": item["blocker_id"],
            "source_record_sha256": sha256(canonical_json_bytes(item)),
            "status": item["status"],
            "target_phase": item["target_phase"],
            "target_horizon": item["target_horizon"],
            "category": item["category"],
            "acceptance_criterion": item["acceptance_criterion"],
            "authority_boundary": item["authority_boundary"],
            "source_ids": item["source_ids"],
            "external_scientific_truth_validated": item["external_scientific_truth_validated"],
            "external_material_truth_validated": item["external_material_truth_validated"],
            "step49_resolution_changed": False,
        }
        for item in carry["new_blockers"]
    ]
    new_debts = [
        {
            "queue_id": f"P061-STEP49-NEW-SOURCE-{index:03d}",
            "bibliography_key": key,
            "document_root": item["chapter"],
            "primary_doi_token": item["primary_doi_token"],
            "source_identity_basis": "absent from all v1.0.19 adopted global keys, all DOI tokens, and normalized metadata fingerprints",
            "status": "UNVERIFIED_EXTERNAL",
            "required_evidence": "fresh primary-source read, DOI/metadata resolution, and proposition-level support mapping",
            "target_phase": 71,
            "genuinely_new_source_identity": True,
        }
        for index, item in enumerate(genuinely_new_source_entries, 1)
        for key in [item["key"]]
    ]

    code_violations = [item for item in all_code if not item["allowed_surface"]]
    status = "PASS_WITH_CONCERNS" if orphan_rows or code_violations or new_debts else "PASS"
    gate = "PASS_WITH_CONCERNS_P061_STEP49_CITATION_AUTHORITY" if status == "PASS_WITH_CONCERNS" else "PASS_P061_STEP49_CITATION_AUTHORITY"
    counts = {
        "adopted_source_occurrences": len(adopted),
        "adopted_tex_occurrences": sum(item["v1020"]["path"].endswith(".tex") for item in adopted),
        "source_coverage_rows": len(source_coverage),
        "bibliography_entries": len(all_bib),
        "bibliography_keys_distinct_global_spelling": len({item["key"] for item in all_bib}),
        "bibliography_identities_chapter_scoped": len(bib_by_chapter_key),
        "bibliography_external_entries": sum(item["bibliography_source_kind"] == "EXTERNAL_METADATA_UNVERIFIED" for item in all_bib),
        "bibliography_internal_self_report_entries": sum(item["bibliography_source_kind"] == "INTERNAL_SELF_REPORT" for item in all_bib),
        "doi_tokens_distinct": len(doi_token_index),
        "doi_like_occurrences": sum(len(item["doi_occurrences"]) for item in all_bib),
        "bibliography_records_with_primary_doi": sum(item["primary_doi_token"] is not None for item in all_bib),
        "bibliography_records_without_primary_doi": sum(item["primary_doi_token"] is None for item in all_bib),
        "annotation_cross_reference_doi_occurrences": sum(
            occurrence["role"] == "ANNOTATION_CROSS_REFERENCE"
            for item in all_bib for occurrence in item["doi_occurrences"]
        ),
        "bibliography_delta_classes": dict(sorted(collections.Counter(item["delta_class"] for item in all_bib).items())),
        "citation_occurrences": len(all_cites),
        "citation_key_occurrences": sum(len(item["keys"]) for item in all_cites),
        "citation_keys_distinct_global_spelling": len({key for _, key in cite_key_occurrences}),
        "citation_identities_chapter_scoped": len(cite_key_occurrences),
        "citation_delta_classes": dict(sorted(collections.Counter(item["delta_class"] for item in all_cites).items())),
        "orphan_or_conflict_citation_keys": len(orphan_rows),
        "defined_not_cited_chapter_scoped": len(defined_not_cited),
        "bibliography_conflicts": len(bibliography_conflicts),
        "mixed_style_bibliography_keys": len(mixed_style_keys),
        "displayed_equations": len(all_equations),
        "displayed_equation_environment_blocks": sum(item["environment"] != "bracket-display" for item in all_equations),
        "displayed_bracket_blocks": sum(item["environment"] == "bracket-display" for item in all_equations),
        "equation_delta_classes": dict(sorted(collections.Counter(item["delta_class"] for item in all_equations).items())),
        "equation_substantive_delta_classes": dict(sorted(collections.Counter(item["substantive_delta_class"] for item in all_equations).items())),
        "changed_prose_candidates": len(all_prose),
        "background_claims": len(background),
        "implementation_only_prose": sum(item["disposition"] == "IMPLEMENTATION_ONLY" for item in all_prose),
        "nonclaim_prose": sum(item["disposition"] == "NON_CLAIM" for item in all_prose),
        "source_attribution_statements": len(all_attributions),
        "source_attribution_delta_classes": dict(sorted(collections.Counter(item["delta_class"] for item in all_attributions).items())),
        "companion_equation_reference_occurrences": len(all_companion_equation_references),
        "companion_equation_references_distinct": len({item["equation_reference"] for item in all_companion_equation_references}),
        "code_mentions_total": len(all_code),
        "code_mentions_designated_surface": len(all_code) - len(code_violations),
        "main_body_code_leakage_candidates": len(code_violations),
        "authority_rows": len(authority_rows),
        "new_or_modified_assets_requiring_authority": new_or_modified_expected,
        "new_or_modified_assets_with_authority": new_or_modified_actual,
        "inherited_material_authority_debts": len(inherited_debts),
        "phase060_inherited_carry_items_preserved": len(inherited_carry_projection),
        "phase060_new_blockers_preserved": len(inherited_blocker_projection),
        "new_bibliography_occurrences": len(new_bibliography_occurrences),
        "genuinely_new_source_identity_debts": len(new_debts),
        "new_bibliography_alias_occurrences_not_new_source": len(new_alias_occurrences),
        "external_scientific_promotions": sum(row["scientific_authority_promoted"] for row in authority_rows),
        "negative_controls": len(NEGATIVE_CONTROL_IDS),
    }

    artifact = {
        "artifact_kind": "PHASE_061_V1020_CITATION_AUTHORITY_MATRIX",
        "schema_version": "1.0.0",
        "phase": 61,
        "step": 49,
        "generated_date": GENERATED_DATE,
        "status": status,
        "gate": gate,
        "baseline_commit": BASELINE_COMMIT,
        "input_commit": INPUT_COMMIT,
        "authority_boundary": {
            "ceiling": "INTERNAL_RELEASE_TEXT_AND_METADATA_CONSISTENCY_ONLY",
            "primary_source_truth": "UNVERIFIED_EXTERNAL",
            "bibliography_presence_is_support": False,
            "citation_adjacency_is_support": False,
            "equation_hash_is_validity": False,
            "review_consensus_is_support": False,
            "process_rationale_is_support": False,
            "external_resolution_performed": False,
            "next_authority_phase": 71,
        },
        "observation_inputs": [topology_meta, process_meta, lineage_meta, snapshot_meta, carry_meta],
        "counts": counts,
        "source_coverage": source_coverage,
        "bibliography_entries": all_bib,
        "citation_occurrences": all_cites,
        "citation_key_index": [
            {"chapter": chapter, "key": key, "occurrence_ids": occurrences, "occurrence_count": len(occurrences), "chapter_scoped_identity_preserved": True}
            for (chapter, key), occurrences in sorted(cite_key_occurrences.items())
        ],
        "bibliography_conflicts": bibliography_conflicts,
        "defined_not_cited": defined_not_cited,
        "mixed_style_bibliography_keys": mixed_style_keys,
        "cross_chapter_key_groups": cross_chapter_key_groups,
        "doi_token_index": [
            {"doi_token": token, "bibliography_identities": identities, "primary_metadata_verified": False}
            for token, identities in sorted(doi_token_index.items())
        ],
        "orphan_or_conflict_citations": orphan_rows,
        "displayed_equations": all_equations,
        "changed_prose_candidates": all_prose,
        "source_attribution_statements": all_attributions,
        "companion_equation_references": all_companion_equation_references,
        "code_free_main_body_audit": {
            "policy": "implementation details allowed only in ch1_appB_codemap.tex, ch2_appB_codemap.tex, or non-TeX companion surfaces",
            "designated_tex_paths": sorted(DESIGNATED_IMPLEMENTATION_PATHS),
            "compliance_state": "NONCOMPLIANT_V1020_SOURCE_BASELINE" if code_violations else "PASS",
            "mentions": all_code,
            "main_body_candidates": code_violations,
            "confirmed_policy_violations": code_violations,
            "candidate_is_automatically_confirmed_violation": True,
            "remediation_target_phase": 72,
        },
        "full_read_review_evidence": {
            "ch1": {
                "source_files": 25,
                "current_physical_lines": 3902,
                "full_read": True,
                "old_new_delta_segments_independently_reconstructed": 56,
                "citation_commands": 71,
                "citation_key_occurrences": 96,
                "bibliography_entries": 36,
                "displayed_equations_source_text": 135,
                "displayed_equation_environment_blocks": snapshot_ch1_eq,
                "bracket_displays": 7,
            },
            "ch2": {
                "source_files": 16,
                "current_physical_lines": 1447,
                "full_read": True,
                "old_physical_lines": 1428,
                "old_new_delta_segments_independently_reconstructed": 22,
                "citation_commands": 28,
                "citation_key_occurrences": 34,
                "bibliography_entries": 16,
                "displayed_equations_source_text": 40,
                "displayed_equation_environment_blocks": snapshot_ch2_eq,
                "bracket_displays": 8,
            },
            "companion": {
                "source_files": 2,
                "current_physical_lines": 1289,
                "full_read": True,
                "formal_latex_citations": 0,
                "formal_latex_bibliography_entries": 0,
                "doi_like_occurrences": 0,
                "equation_reference_occurrences": 100,
            },
            "reviewer_conflict_resolution": {
                "conflict": "one global review reported 98 citation commands, 128 key occurrences and CH2::bazant2013 unused",
                "direct_resolution": "frozen source parser plus independent Ch2 full read found the multiline cite at ch2_sec01_partition.tex:105 and the designated-appendix cite at ch2_appB_codemap.tex:53",
                "resolved_counts": "99 citation commands, 130 key occurrences, zero defined-not-cited identities",
                "inference_used": False,
            },
        },
        "bounded_semantic_findings": [
            {
                "finding_id": "P061-STEP49-FINDING-001",
                "severity": "P1",
                "object": "v1.0.20 rendered text contains implementation/code references outside designated Appendix B",
                "state": "CONFIRMED_SOURCE_BASELINE_NONCOMPLIANCE",
                "occurrences": len(code_violations),
                "target_phase": 72,
            },
            {
                "finding_id": "P061-STEP49-FINDING-002",
                "severity": "P1",
                "object": "eq:lco-mottcrit W approximately 2zt heuristic",
                "state": "GROUND_NOT_FOUND_FOR_DERIVATION_AND_MODEL_ASSUMPTIONS",
                "target_phase": 71,
            },
            {
                "finding_id": "P061-STEP49-FINDING-003",
                "severity": "P1",
                "object": "new 0.3 mV rounded-center discrepancy claim in Ch2 Appendix B and synthesis",
                "state": "GROUND_NOT_FOUND_FOR_INDEPENDENT_NUMERICAL_PROVENANCE",
                "target_phase": 71,
            },
            {
                "finding_id": "P061-STEP49-FINDING-004",
                "severity": "P1",
                "object": "Ch2 root comment says implementation complete while Appendix B describes a later implementation requirement",
                "state": "PROCESS_CLAIM_CONTRADICTION_NOT_SCIENTIFIC_SUPPORT",
                "target_phase": 72,
            },
            {
                "finding_id": "P061-STEP49-FINDING-005",
                "severity": "P2",
                "object": "source displayed-equation denominator 175 versus snapshot environment-block denominator 160",
                "state": "DENOMINATORS_SEPARATED_15_BRACKET_DISPLAYS_PRESERVED",
                "target_phase": 61,
            },
        ],
        "authority_rows": authority_rows,
        "inherited_material_authority_debts": inherited_debts,
        "phase060_carry_forward_preservation": {
            "source_artifact": CARRY_PATH.as_posix(),
            "authority_boundary": "all 52 inherited items and 5 Phase060 blockers remain unresolved; Step49 changes no status, target, acceptance, or external-truth flag",
            "inherited_items": inherited_carry_projection,
            "new_blockers": inherited_blocker_projection,
            "all_states_preserved": True,
        },
        "genuinely_new_source_identity_debts": new_debts,
        "new_bibliography_alias_occurrences": [
            {
                "chapter": item["chapter"],
                "bibliography_key": item["key"],
                "primary_doi_token": item["primary_doi_token"],
                "delta_class": item["delta_class"],
                "genuinely_new_source_identity": False,
                "existing_v1019_identity_basis": "+".join(identity_match_basis[(item["chapter"], item["key"])]),
                "anchor": item["anchor"],
            }
            for item in new_alias_occurrences
        ],
        "ground_not_found": [
            {
                "gnf_id": "P061-STEP49-GNF-001",
                "object": "primary-source proposition-level truth for adopted citations and bibliography entries",
                "state": "GROUND_NOT_FOUND_IN_PHASE061_SOURCE_UNIVERSE",
                "target_phase": 71,
            },
            {
                "gnf_id": "P061-STEP49-GNF-002",
                "object": "independent derivation and assumptions for new or modified equations",
                "state": "GROUND_NOT_FOUND_IN_PHASE061_SOURCE_UNIVERSE",
                "target_phase": 71,
            },
        ],
        "unverified_external_queue": [
            {
                "queue_id": "P061-STEP49-UNV-001",
                "object": "all citation-to-proposition support assertions",
                "status": "UNVERIFIED_EXTERNAL",
                "target_phase": 71,
            },
            {
                "queue_id": "P061-STEP49-UNV-002",
                "object": "all equation derivations, assumptions and material-law validity",
                "status": "UNVERIFIED_EXTERNAL",
                "target_phase": 71,
            },
            {
                "queue_id": "P061-STEP49-UNV-003",
                "object": "all background-claim primary support",
                "status": "UNVERIFIED_EXTERNAL",
                "target_phase": 71,
            },
        ],
        "required_negative_controls": list(NEGATIVE_CONTROL_IDS),
    }
    walk_finite(artifact)
    return artifact


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        artifact = build()
        data = canonical_json_bytes(artifact)
        output = REPO / args.output
        if args.check:
            if not output.is_file() or output.read_bytes() != data:
                raise BuildError("OUTPUT_NOT_DETERMINISTIC_OR_MISSING")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
        print(
            f"{artifact['gate']} status={artifact['status']} "
            f"authority_rows={artifact['counts']['authority_rows']} "
            f"citations={artifact['counts']['citation_occurrences']} "
            f"equations={artifact['counts']['displayed_equations']} "
            f"background_claims={artifact['counts']['background_claims']}"
        )
        return 0
    except (BuildError, UnicodeError, OSError, ValueError) as exc:
        print(f"FAIL_P061_STEP49_CITATION_AUTHORITY {type(exc).__name__}:{exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
