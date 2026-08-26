#!/usr/bin/env python3
"""Independent fail-closed validator for Phase 061 Step 49.

The validator does not import the Step 49 builder or any historical production
module.  It independently reads frozen Git blobs, reconstructs the core scholarly
inventory, tests controlled corruptions, and enforces exact-seven persistence.
"""

from __future__ import annotations

import argparse
import ast
import collections
import copy
import hashlib
import json
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


class ValidationError(RuntimeError):
    """Controlled validation failure."""


class DuplicateKeyError(ValidationError):
    """Strict JSON duplicate-key failure."""


class NonFiniteNumberError(ValidationError):
    """Strict JSON non-finite-number failure."""


REPO = Path(__file__).resolve().parents[3]
BUILDER = REPO / "Codex/work/v1020_phase061/build_phase061_step49_citation_authority.py"
VALIDATOR = Path(__file__).resolve()
MATRIX = REPO / "Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json"
RESULT = REPO / "Codex/results/PHASE_061_STEP_049_CITATION_AUTHORITY_RESULT.md"
ACTIVE_LEDGER = REPO / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = REPO / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = REPO / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
TOPOLOGY = REPO / "Codex/results/PHASE_061_V1020_SOURCE_TOPOLOGY.json"
PROCESS = REPO / "Codex/results/PHASE_061_V1020_PROCESS_AUTHORITY_MATRIX.json"
LINEAGE = REPO / "Codex/results/PHASE_061_V1020_LINEAGE_DIFF_MATRIX.json"
SNAPSHOT = REPO / "Codex/results/PHASE_061_V1020_SNAPSHOT_GENEALOGY.json"
CARRY = REPO / "Codex/results/PHASE_060_V1019_CARRY_FORWARD_DELTA.json"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "5cf75ba2fd4e5707c53b164d361f1526c3d31f06"
EXPECTED_SUBJECT = "audit(phase061): bound v1020 citation authority"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"

INPUT_SHA256 = {
    TOPOLOGY: "0af27968b7896d2b5d462be6c9e1143e4e3985ffdd028b7f9f19a33924f9903c",
    PROCESS: "c5aabe37a42da12bfe44e8f7cee9de8a36a7cba7fcffc5aecd68d8832c77b403",
    LINEAGE: "25136896e4c93e509c9d92a748ba1d23337ebe60aa2736e5f569b70f6f1ed914",
    SNAPSHOT: "629995ab5936587840e5944c513ef86a0e82f114dd1d94860b06754fb9fdd414",
    CARRY: "72848094865e0b2cad1110df92e7543dc287607af45dc2346e2040bd65812271",
}
EXPECTED_BUILDER_SHA256 = "275ade652adf1fc187dce23c037c3676fe706be9c8c3c67c43e986baa8bb4025"
EXPECTED_BUILDER_AST_SHA256 = "68e291995552d202ac8357f86c124bca205bce05b807e791836a01dea02422f3"
EXPECTED_MATRIX_SCHEMA_FINGERPRINT = "f04d7963d14a8dffc096a3ba89207dbeb4b4015fd40836ae8a165dee1c75a02d"
EXACT_SEVEN = (
    "Codex/work/v1020_phase061/build_phase061_step49_citation_authority.py",
    "Codex/work/v1020_phase061/validate_phase061_step49.py",
    "Codex/results/PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json",
    "Codex/results/PHASE_061_STEP_049_CITATION_AUTHORITY_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
)
EXPECTED_NEW_BIB_KEYS = {
    "CH1::ashcroftmermin1976", "CH1::bakerverbrugge2018", "CH1::dreyer2011",
    "CH1::imada1998", "CH1::marianetti2004", "CH1::mott1968",
    "CH1::msmr_origin2017", "CH1::vanderven1998",
    "CH2::dahn1991", "CH2::ohzuku1993",
}
EXPECTED_GENUINELY_NEW_SOURCE_KEYS = {
    "CH1::ashcroftmermin1976", "CH1::bakerverbrugge2018", "CH1::dreyer2011",
    "CH1::imada1998", "CH1::marianetti2004", "CH1::mott1968",
    "CH1::msmr_origin2017", "CH1::vanderven1998",
}
EXPECTED_EQUATION_DELTA = {
    "eq:sm-baresum": "NEW", "eq:sm-baremid": "NEW", "eq:sm-bare": "NEW",
    "eq:sm-exch": "NEW", "eq:sm-fdbe": "NEW", "eq:lco-mottcrit": "NEW",
    "eq:lco-slots": "MODIFIED",
}
EXPECTED_CODE_ANCHORS = {
    ("Claude/docs/v1.0.20/_sections/ch1_sec00_intro.tex", 19),
    ("Claude/docs/v1.0.20/_sections/ch1_sec01_n0n1.tex", 38),
    ("Claude/docs/v1.0.20/_sections/ch1_sec03_center.tex", 68),
    ("Claude/docs/v1.0.20/_sections/ch1_sec08_lag.tex", 125),
    ("Claude/docs/v1.0.20/_sections/ch1_sec10_sum.tex", 18),
    ("Claude/docs/v1.0.20/_sections/ch1_sec10_sum.tex", 47),
    ("Claude/docs/v1.0.20/_sections/ch1_sec12_lcocenter.tex", 105),
    ("Claude/docs/v1.0.20/_sections/ch1_sec18_inputs.tex", 29),
    ("Claude/docs/v1.0.20/_sections/ch1_sec18_inputs.tex", 36),
    ("Claude/docs/v1.0.20/_sections/ch1_sec18_inputs.tex", 66),
    ("Claude/docs/v1.0.20/_sections/ch2_appA_traps.tex", 8),
    ("Claude/docs/v1.0.20/_sections/ch2_bib.tex", 20),
    ("Claude/docs/v1.0.20/_sections/ch2_sec04_einstein.tex", 96),
    ("Claude/docs/v1.0.20/_sections/ch2_sec08_synthesis.tex", 95),
}
NEGATIVE_CONTROL_IDS = (
    "citation-fake-doi-certainty", "citation-key-alias-collapse",
    "bibliography-presence-as-support", "equation-hash-as-validity",
    "review-consensus-promotion", "code-leakage-misclassification",
    "citation-drop-occurrence", "citation-duplicate-occurrence",
    "citation-orphan-suppression", "bibliography-drop-entry",
    "bibliography-conflict-suppression", "equation-drop-block",
    "equation-body-swap", "background-claim-drop",
    "background-nonclaim-promotion", "source-attribution-drop",
    "delta-link-swap", "rationale-as-support", "external-truth-promotion",
    "new-debt-alias-reuse", "main-body-code-allowlist-broadening",
    "competitive-candidate-promotion", "strict-json-duplicate-key",
    "strict-json-nonfinite", "cross-input-hash", "cross-baseline-commit",
    "cross-adopted-source-count", "cross-authority-row-coverage",
    "cross-unverified-route", "nested-schema-extra-key",
    "bibliography-text-fabrication", "prose-text-fabrication",
    "attribution-text-fabrication", "code-text-fabrication",
    "authority-semantic-row-swap", "builder-hash-mutation",
)

DISPLAY_ENVIRONMENTS = "equation|align|gather|multline|eqnarray|displaymath"
DISPLAY_RE = re.compile(
    rf"\\begin\{{(?P<env>(?:{DISPLAY_ENVIRONMENTS})\*?)\}}(?P<body>.*?)\\end\{{(?P=env)\}}",
    re.DOTALL,
)
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^{}]+)\}")
CITE_RE = re.compile(
    r"\\(?P<command>cite|citep|citet|citealp|citeauthor|citeyear|parencite|textcite|autocite|footcite|nocite)\*?\s*"
    r"(?:\[[^\]]*\]\s*){0,2}\{(?P<keys>[^{}]+)\}", re.IGNORECASE,
)
ATTRIBUTION_RE = re.compile(
    r"(\\cite|\bdoi\b|근거|출처|참고문헌|문헌|reference|reported|보고(?:하|되|된)|source)",
    re.IGNORECASE,
)
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
EQ_REFERENCE_RE = re.compile(r"(?<![A-Za-z0-9_])eq:[A-Za-z0-9_.:-]+")
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
    return json.loads(data.decode("utf-8"), object_pairs_hook=_object_pairs, parse_constant=_reject_constant)


def strict_load(path: Path) -> Any:
    return strict_load_bytes(path.read_bytes())


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
                raise ValidationError("JSON_NONSTRING_KEY")
            children.append(walk_finite(item))
    else:
        raise ValidationError(f"JSON_TYPE:{type(value).__name__}")
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


def schema_projection(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: schema_projection(item) for key, item in value.items()}
    if isinstance(value, list):
        return [schema_projection(value[0])] if value else []
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    raise ValidationError("SCHEMA_TYPE")


def schema_contract_fingerprint(value: Any) -> str:
    """Fingerprint every nested keyset/type at an index-independent JSON path."""
    rows: set[tuple[str, str, tuple[str, ...]]] = set()

    def visit(item: Any, path: str) -> None:
        if isinstance(item, bool):
            kind = "bool"
        elif item is None:
            kind = "null"
        elif isinstance(item, int):
            kind = "int"
        elif isinstance(item, float):
            kind = "float"
        elif isinstance(item, str):
            kind = "str"
        elif isinstance(item, dict):
            kind = "dict"
        elif isinstance(item, list):
            kind = "list"
        else:
            raise ValidationError("SCHEMA_TYPE")
        keys = tuple(sorted(item)) if isinstance(item, dict) else ()
        rows.add((path, kind, keys))
        if isinstance(item, dict):
            for key, child in item.items():
                visit(child, f"{path}.{key}")
        elif isinstance(item, list):
            for child in item:
                visit(child, f"{path}[]")

    visit(value, "$")
    projection = sorted((path, kind, list(keys)) for path, kind, keys in rows)
    encoded = (json.dumps(projection, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    return sha256(encoded)


def run_git_bytes(args: list[str], code: str, timeout: int = 60) -> bytes:
    proc = subprocess.run(["git", *args], cwd=REPO, check=False, capture_output=True, timeout=timeout)
    if proc.returncode:
        raise ValidationError(f"{code}:{proc.returncode}")
    return proc.stdout


def run_git_text(args: list[str], code: str, timeout: int = 60) -> str:
    return run_git_bytes(args, code, timeout).decode("utf-8").strip()


def git_blobs(shas: Iterable[str]) -> dict[str, bytes]:
    ordered = list(dict.fromkeys(shas))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=REPO,
        input=("\n".join(ordered) + "\n").encode("ascii"),
        check=False, capture_output=True, timeout=120,
    )
    if proc.returncode:
        raise ValidationError(f"GIT_CAT_FILE:{proc.returncode}")
    result: dict[str, bytes] = {}
    offset = 0
    for expected in ordered:
        newline = proc.stdout.find(b"\n", offset)
        if newline < 0:
            raise ValidationError("GIT_BLOB_HEADER_EOF")
        parts = proc.stdout[offset:newline].decode("ascii").split()
        offset = newline + 1
        if len(parts) != 3 or parts[0] != expected or parts[1] != "blob":
            raise ValidationError("GIT_BLOB_HEADER")
        size = int(parts[2])
        result[expected] = proc.stdout[offset:offset + size]
        offset += size
        if proc.stdout[offset:offset + 1] != b"\n":
            raise ValidationError("GIT_BLOB_SEPARATOR")
        offset += 1
    if proc.stdout[offset:]:
        raise ValidationError("GIT_BLOB_TRAILING")
    return result


def strip_comment(line: str) -> str:
    for index, char in enumerate(line):
        preceding = len(line[:index]) - len(line[:index].rstrip("\\"))
        if char == "%" and preceding % 2 == 0:
            return line[:index]
    return line


def clean_latex(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def chapter(path: str) -> str:
    name = Path(path).name
    if name.startswith("ch1_") or "_ch1_" in name or "graphite_ica_ch1_" in name:
        return "CH1"
    if name.startswith("ch2_") or "_ch2_" in name or "graphite_ica_ch2_" in name:
        return "CH2"
    return "NON_CHAPTER"


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def normalize_doi_token(value: str) -> str:
    token = value.rstrip(".;}").lower()
    while token.endswith(")") and token.count(")") > token.count("("):
        token = token[:-1]
    return token


def bibliography_identity_fingerprint(item: dict[str, Any]) -> str:
    body = re.sub(r"\\bibitem(?:\[[^\]]*\])?\{[^{}]+\}", r"\\bibitem{}", item["normalized_body"], count=1)
    return sha256(normalize_space(body).casefold().encode("utf-8"))


def content_anchor(path: str, line_start: int, line_end: int, content: str) -> dict[str, Any]:
    return {
        "path": path,
        "line_start": line_start,
        "line_end": line_end,
        "sha256_lf_normalized": sha256(lf_bytes(content.encode("utf-8"))),
    }


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


def semantic_bibliography_records(text: str, path: str) -> list[dict[str, Any]]:
    clean = clean_latex(text)
    matches = list(BIBITEM_RE.finditer(clean))
    records: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(clean)
        boundary = clean.find("\\end{thebibliography}", match.end(), end)
        if boundary >= 0:
            end = boundary
        body = clean[match.start():end].strip()
        doi_sequence = [normalize_doi_token(token) for token in DOI_RE.findall(body)]
        records.append({
            "key": match.group(1).strip(),
            "body": body,
            "normalized_body": normalize_space(body),
            "doi_tokens": sorted(set(doi_sequence)),
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


def semantic_citation_records(text: str, path: str) -> list[dict[str, Any]]:
    clean = clean_latex(text)
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
        preceding = len(text[:index]) - len(text[:index].rstrip("\\"))
        if preceding % 2:
            index += 2
            continue
        end = index + 2
        while end < len(text) - 1:
            if text[end:end + 2] == r"\]":
                before = len(text[:end]) - len(text[:end].rstrip("\\"))
                if before % 2 == 0:
                    spans.append((index, end + 2, text[index + 2:end]))
                    index = end + 2
                    break
            end += 1
        else:
            raise ValidationError("BRACKET_DISPLAY_UNTERMINATED")
    return spans


def semantic_equation_records(text: str, path: str) -> list[dict[str, Any]]:
    clean = clean_latex(text)
    candidates = [(match.start(), match.end(), match.group("env"), match.group("body")) for match in DISPLAY_RE.finditer(clean)]
    for start, end, body in bracket_display_spans(clean):
        if not any(begin <= start < finish for begin, finish, _, _ in candidates):
            candidates.append((start, end, "bracket-display", body))
    records: list[dict[str, Any]] = []
    for start, end, environment, body in sorted(candidates):
        labels = LABEL_RE.findall(body)
        normalized = normalize_space(LABEL_RE.sub("", body))
        body_hash = sha256(normalized.encode("utf-8"))
        records.append({
            "environment": environment,
            "labels": labels,
            "semantic_identity": labels[0] if labels else "body:" + body_hash,
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
    clean = normalize_space(strip_comment(line))
    if not clean or clean.startswith(STRUCTURAL_PREFIXES) or clean.startswith("\\bibitem"):
        return None
    if clean in {"{", "}", "\\[", "\\]", "\\(", "\\)"}:
        return None
    if path in DESIGNATED_IMPLEMENTATION_PATHS:
        return "IMPLEMENTATION_ONLY", clean
    if len(re.findall(r"[A-Za-z가-힣]", clean)) < 8:
        return "NON_CLAIM", clean
    return "BACKGROUND_CLAIM", clean


def semantic_source_attributions(text: str, path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(text.splitlines(), 1):
        clean = normalize_space(strip_comment(line))
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


def semantic_code_mentions(text: str, path: str) -> list[dict[str, Any]]:
    allowed = path in DESIGNATED_IMPLEMENTATION_PATHS
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(text.splitlines(), 1):
        clean = normalize_space(strip_comment(line))
        scan = re.sub(r"\\code\{eq:[^{}]+\}", "", clean)
        if scan and not clean.startswith(STRUCTURAL_PREFIXES) and CODE_RE.search(scan):
            rows.append({
                "text": clean,
                "allowed_surface": allowed,
                "disposition": "DESIGNATED_IMPLEMENTATION_APPENDIX" if allowed else "MAIN_BODY_CODE_LEAKAGE_CANDIDATE",
                "anchor": content_anchor(path, number, number, line),
            })
    return rows


def semantic_companion_equation_references(text: str, path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(text.splitlines(), 1):
        for match in EQ_REFERENCE_RE.finditer(line):
            rows.append({
                "equation_reference": match.group(0).rstrip(".:-"),
                "context": normalize_space(line),
                "anchor": content_anchor(path, number, number, line),
                "surface_class": "PACKAGE_COMPANION",
                "formal_scholarly_citation": False,
                "primary_support_state": "NOT_PRIMARY_SUPPORT",
            })
    return rows


def bracket_displays(text: str) -> list[str]:
    rows: list[str] = []
    index = 0
    while index < len(text) - 1:
        if text[index:index + 2] != r"\[":
            index += 1
            continue
        preceding = len(text[:index]) - len(text[:index].rstrip("\\"))
        if preceding % 2:
            index += 2
            continue
        end = index + 2
        while end < len(text) - 1:
            if text[end:end + 2] == r"\]":
                before = len(text[:end]) - len(text[:end].rstrip("\\"))
                if before % 2 == 0:
                    rows.append(text[index + 2:end])
                    index = end + 2
                    break
            end += 1
        else:
            raise ValidationError("BRACKET_DISPLAY_UNTERMINATED")
    return rows


def bib_records(text: str) -> dict[str, str]:
    clean = clean_latex(text)
    matches = list(BIBITEM_RE.finditer(clean))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(clean)
        closing = clean.find("\\end{thebibliography}", match.end(), end)
        if closing >= 0:
            end = closing
        key = match.group(1).strip()
        if key in result:
            raise ValidationError(f"DUPLICATE_BIB:{key}")
        result[key] = normalize_space(clean[match.start():end].strip())
    return result


def cite_records(text: str) -> list[tuple[str, tuple[str, ...], str]]:
    clean = clean_latex(text)
    lines = clean.splitlines()
    result: list[tuple[str, tuple[str, ...], str]] = []
    for match in CITE_RE.finditer(clean):
        line = clean.count("\n", 0, match.start()) + 1
        keys = tuple(key.strip() for key in match.group("keys").split(",") if key.strip())
        context = normalize_space(lines[line - 1] if line <= len(lines) else match.group(0))
        result.append((match.group("command").lower(), keys, context))
    return result


def equation_records(text: str) -> list[tuple[str, str, str]]:
    clean = clean_latex(text)
    env_rows: list[tuple[int, int, str, str]] = [
        (match.start(), match.end(), match.group("env"), match.group("body"))
        for match in DISPLAY_RE.finditer(clean)
    ]
    rows: list[tuple[str, str, str]] = []
    for _, _, env, body in env_rows:
        labels = LABEL_RE.findall(body)
        normalized = normalize_space(LABEL_RE.sub("", body))
        identity = labels[0] if labels else "body:" + sha256(normalized.encode("utf-8"))
        rows.append((identity, sha256(normalized.encode("utf-8")), env))
    for body in bracket_displays(clean):
        normalized = normalize_space(LABEL_RE.sub("", body))
        rows.append(("body:" + sha256(normalized.encode("utf-8")), sha256(normalized.encode("utf-8")), "bracket-display"))
    return rows


def independent_expected() -> dict[str, Any]:
    inputs = {path: strict_load(path) for path in INPUT_SHA256}
    for path, expected_hash in INPUT_SHA256.items():
        if sha256(lf_bytes(path.read_bytes())) != expected_hash:
            raise ValidationError(f"INPUT_HASH:{path.name}")
    process, lineage, snapshot, carry = inputs[PROCESS], inputs[LINEAGE], inputs[SNAPSHOT], inputs[CARRY]
    snapshot_counts = (
        snapshot["baseline_to_final"]["ch1"]["eqblocks"]["count_after"],
        snapshot["baseline_to_final"]["ch2"]["eqblocks"]["count_after"],
    )
    if snapshot_counts != (128, 32):
        raise ValidationError("SNAPSHOT_EQUATION_DENOMINATOR")
    source_by_path = {row["path"]: row for row in process["source_routes"]}
    adopted = []
    for row in lineage["delta_rows"]:
        route = source_by_path[row["v1020"]["path"]]
        if route["source_authority_class"] == "ADOPTED_RELEASE_SOURCE":
            adopted.append((route, row))
    adopted.sort(key=lambda item: item[0]["source_id"])
    if len(adopted) != 43:
        raise ValidationError("ADOPTED_COUNT")
    shas: list[str] = []
    for _, row in adopted:
        shas.append(row["v1020"]["blob_sha1"])
        if row.get("v1019"):
            shas.append(row["v1019"]["blob_sha1"])
    blobs = git_blobs(shas)

    coverage: list[dict[str, Any]] = []
    bib: dict[tuple[str, str], str] = {}
    citations: list[tuple[str, str, tuple[str, ...], str]] = []
    equations: list[tuple[str, str, str, str]] = []
    semantic_bib: list[dict[str, Any]] = []
    semantic_old_bib: list[dict[str, Any]] = []
    semantic_cites: list[dict[str, Any]] = []
    semantic_equations: list[dict[str, Any]] = []
    semantic_prose: list[dict[str, Any]] = []
    semantic_attributions: list[dict[str, Any]] = []
    semantic_code: list[dict[str, Any]] = []
    semantic_companion: list[dict[str, Any]] = []
    equation_delta: dict[str, str] = {}
    new_bib: set[str] = set()
    companion_eq_refs = 0
    for route, row in adopted:
        path = row["v1020"]["path"]
        data = lf_bytes(blobs[row["v1020"]["blob_sha1"]])
        if sha256(data) != row["v1020"]["sha256_lf_normalized"]:
            raise ValidationError("SOURCE_HASH")
        text = data.decode("utf-8")
        coverage.append({"source_id": route["source_id"], "delta_id": row["delta_id"], "path": path, "sha256": sha256(data), "lines": len(data.splitlines())})
        old_text = ""
        old_path = row["v1019"]["path"] if row.get("v1019") else path
        if row.get("v1019"):
            old_text = lf_bytes(blobs[row["v1019"]["blob_sha1"]]).decode("utf-8")

        current_attributions = semantic_source_attributions(text, path)
        old_attributions = semantic_source_attributions(old_text, old_path)
        attribution_delta = pair_attribution_delta(current_attributions, old_attributions)
        for item, delta in zip(current_attributions, attribution_delta):
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
                "source_id": route["source_id"], "delta_id": row["delta_id"],
                "chapter": chapter(path), "surface_class": surface_class(path),
                "delta_class": delta["delta_class"], "old_anchor": delta["old_anchor"],
                "old_exact_signature": delta["old_exact_signature"], "delta_segment_link": segment_link,
                "authority_disposition": "STRUCTURAL_ATTRIBUTION_ONLY_NOT_PRIMARY_SUPPORT",
                "primary_support_state": "UNVERIFIED_EXTERNAL", "external_scientific_truth": False,
            })
        semantic_attributions.extend(current_attributions)

        if not path.endswith(".tex"):
            references = semantic_companion_equation_references(text, path)
            for item in references:
                item.update({"source_id": route["source_id"], "delta_id": row["delta_id"]})
            semantic_companion.extend(references)
            companion_eq_refs += len(references)
            continue
        root = chapter(path)
        current_bib = bib_records(text)
        for key, body in current_bib.items():
            identity = (root, key)
            if identity in bib:
                raise ValidationError("ROOT_BIB_DUPLICATE")
            bib[identity] = body
        current_cites = cite_records(text)
        citations.extend((root, command, keys, context) for command, keys, context in current_cites)
        current_eq = equation_records(text)
        equations.extend((root, identity, body_hash, env) for identity, body_hash, env in current_eq)
        old_bib = bib_records(old_text)
        for key in current_bib:
            if key not in old_bib:
                new_bib.add(f"{root}::{key}")
        old_eq = {identity: body_hash for identity, body_hash, _ in equation_records(old_text)}
        old_bodies = set(old_eq.values())
        for identity, body_hash, _ in current_eq:
            if identity in old_eq and old_eq[identity] == body_hash:
                delta = "UNCHANGED"
            elif identity in old_eq or body_hash in old_bodies:
                delta = "MODIFIED"
            else:
                delta = "NEW"
            if delta != "UNCHANGED":
                equation_delta[identity] = delta

        new_bib_rows = semantic_bibliography_records(text, path)
        old_bib_row_list = semantic_bibliography_records(old_text, old_path)
        for item in old_bib_row_list:
            item["chapter"] = root
        semantic_old_bib.extend(old_bib_row_list)
        old_bib_rows = {item["key"]: item for item in old_bib_row_list}
        for item in new_bib_rows:
            old = old_bib_rows.get(item["key"])
            item.update({
                "delta_class": "NEW" if old is None else ("UNCHANGED" if old["normalized_body"] == item["normalized_body"] else "MODIFIED"),
                "source_id": route["source_id"], "delta_id": row["delta_id"], "chapter": root,
            })
        semantic_bib.extend(new_bib_rows)

        new_cite_rows = semantic_citation_records(text, path)
        old_cite_rows = semantic_citation_records(old_text, old_path)
        for item, delta in zip(new_cite_rows, multiset_delta(new_cite_rows, old_cite_rows, "exact_signature", "signature")):
            item.update({"delta_class": delta, "source_id": route["source_id"], "delta_id": row["delta_id"], "chapter": root})
        semantic_cites.extend(new_cite_rows)

        new_equation_rows = semantic_equation_records(text, path)
        old_equation_rows = semantic_equation_records(old_text, old_path)
        old_by_identity = {item["semantic_identity"]: item for item in old_equation_rows}
        old_body_hashes = {item["body_sha256"] for item in old_equation_rows}
        for item in new_equation_rows:
            old = old_by_identity.get(item["semantic_identity"])
            delta = "UNCHANGED" if old and old["body_sha256"] == item["body_sha256"] else ("MODIFIED" if old or item["body_sha256"] in old_body_hashes else "NEW")
            substantive = "UNCHANGED_MATHEMATICAL_CONTENT_CROSS_REFERENCE_ONLY" if item["semantic_identity"] == "eq:lco-slots" else delta
            item.update({
                "delta_class": delta, "source_id": route["source_id"], "delta_id": row["delta_id"],
                "chapter": root, "substantive_delta_class": substantive,
            })
        semantic_equations.extend(new_equation_rows)

        code_rows = semantic_code_mentions(text, path)
        for item in code_rows:
            item.update({"source_id": route["source_id"], "delta_id": row["delta_id"], "chapter": root})
        semantic_code.extend(code_rows)

        for segment_index, segment in enumerate((row.get("text_delta") or {}).get("segments", []), 1):
            for offset, source_line in enumerate(segment["new_lines"]):
                disposition = prose_candidate(source_line, path)
                if disposition is None:
                    continue
                kind, clean = disposition
                number = segment["new_line_start"] + offset
                semantic_prose.append({
                    "candidate_id": "", "disposition": kind, "text": clean,
                    "source_id": route["source_id"], "delta_id": row["delta_id"],
                    "segment_index": segment_index, "segment_sha256": segment["segment_sha256"],
                    "delta_class": "NEW" if segment["tag"] == "insert" else "MODIFIED",
                    "chapter": root, "anchor": content_anchor(path, number, number, source_line),
                })

    for index, item in enumerate(semantic_prose, 1):
        item["candidate_id"] = f"P061-PROSE-{index:04d}"
    for index, item in enumerate(semantic_attributions, 1):
        item["statement_id"] = f"P061-ATTR-{index:04d}"
    for index, item in enumerate(semantic_cites, 1):
        item["occurrence_id"] = f"P061-CITE-{index:04d}"
    old_global_keys = {item["key"] for item in semantic_old_bib}
    old_global_doi_tokens = {token for item in semantic_old_bib for token in item["doi_tokens"]}
    old_global_metadata_fingerprints = {bibliography_identity_fingerprint(item) for item in semantic_old_bib}
    new_semantic_bib = [item for item in semantic_bib if item["delta_class"] == "NEW"]
    genuine_source_keys = {
        f"{item['chapter']}::{item['key']}"
        for item in new_semantic_bib
        if item["key"] not in old_global_keys
        and not (set(item["doi_tokens"]) & old_global_doi_tokens)
        and bibliography_identity_fingerprint(item) not in old_global_metadata_fingerprints
    }
    alias_source_keys = {f"{item['chapter']}::{item['key']}" for item in new_semantic_bib} - genuine_source_keys
    cited_identities = {(root, key) for root, _, keys, _ in citations for key in keys}
    return {
        "inputs": inputs,
        "adopted": adopted,
        "coverage": coverage,
        "bib": bib,
        "citations": citations,
        "equations": equations,
        "semantic_bib": semantic_bib,
        "genuine_source_keys": genuine_source_keys,
        "alias_source_keys": alias_source_keys,
        "semantic_cites": semantic_cites,
        "semantic_equations": semantic_equations,
        "semantic_prose": semantic_prose,
        "semantic_attributions": semantic_attributions,
        "semantic_code": semantic_code,
        "semantic_companion": semantic_companion,
        "new_bib": new_bib,
        "equation_delta": equation_delta,
        "cited_identities": cited_identities,
        "companion_eq_refs": companion_eq_refs,
        "snapshot_eq_counts": snapshot_counts,
        "carry": carry,
    }


def promoted(value: Any) -> bool:
    forbidden_true = {
        "external_scientific_truth", "external_material_truth",
        "external_scientific_truth_validated", "external_material_truth_validated",
        "scientific_authority_promoted", "release_source_is_primary_scientific_support",
        "review_approval_is_scientific_support", "rationale_is_support",
        "hash_is_scientific_validity", "primary_metadata_verified", "metadata_verified",
    }
    if isinstance(value, dict):
        for key, child in value.items():
            if key in forbidden_true and child is not False:
                return True
            if key == "primary_support_state" and child not in {"UNVERIFIED_EXTERNAL", "NOT_PRIMARY_SUPPORT"}:
                return True
            if promoted(child):
                return True
    elif isinstance(value, list):
        return any(promoted(item) for item in value)
    return False


def add_if(diagnostics: set[str], condition: bool, code: str) -> None:
    if condition:
        diagnostics.add(code)


def content_diagnostics(matrix: Any, expected: dict[str, Any]) -> set[str]:
    diagnostics: set[str] = set()
    if not isinstance(matrix, dict):
        return {"MATRIX_SCHEMA"}
    walk_finite(matrix)
    add_if(diagnostics, schema_contract_fingerprint(matrix) != EXPECTED_MATRIX_SCHEMA_FINGERPRINT, "NESTED_SCHEMA_CONTRACT")
    required_top = {
        "artifact_kind", "schema_version", "phase", "step", "generated_date", "status", "gate",
        "baseline_commit", "input_commit", "authority_boundary", "observation_inputs", "counts",
        "source_coverage", "bibliography_entries", "citation_occurrences", "citation_key_index",
        "bibliography_conflicts", "defined_not_cited", "mixed_style_bibliography_keys",
        "cross_chapter_key_groups", "doi_token_index", "orphan_or_conflict_citations",
        "displayed_equations", "changed_prose_candidates", "source_attribution_statements",
        "companion_equation_references", "code_free_main_body_audit", "full_read_review_evidence",
        "bounded_semantic_findings", "authority_rows", "inherited_material_authority_debts",
        "phase060_carry_forward_preservation", "genuinely_new_source_identity_debts",
        "new_bibliography_alias_occurrences",
        "ground_not_found", "unverified_external_queue", "required_negative_controls",
    }
    add_if(diagnostics, set(matrix) != required_top, "MATRIX_SCHEMA")
    add_if(diagnostics, matrix.get("artifact_kind") != "PHASE_061_V1020_CITATION_AUTHORITY_MATRIX", "MATRIX_CONTRACT")
    add_if(diagnostics, matrix.get("schema_version") != "1.0.0" or matrix.get("phase") != 61 or matrix.get("step") != 49, "MATRIX_CONTRACT")
    add_if(diagnostics, matrix.get("status") != "PASS_WITH_CONCERNS" or matrix.get("gate") != "PASS_WITH_CONCERNS_P061_STEP49_CITATION_AUTHORITY", "MATRIX_CONTRACT")
    add_if(diagnostics, matrix.get("baseline_commit") != BASELINE or matrix.get("input_commit") != EXPECTED_PARENT, "CROSS_BASELINE_COMMIT")
    boundary = matrix.get("authority_boundary", {})
    add_if(diagnostics, boundary.get("primary_source_truth") != "UNVERIFIED_EXTERNAL" or boundary.get("external_resolution_performed") is not False or boundary.get("next_authority_phase") != 71, "UNVERIFIED_ROUTE")
    add_if(diagnostics, any(boundary.get(key) is not False for key in (
        "bibliography_presence_is_support", "citation_adjacency_is_support", "equation_hash_is_validity",
        "review_consensus_is_support", "process_rationale_is_support",
    )), "AUTHORITY_PROMOTION")

    observation = matrix.get("observation_inputs", [])
    observed_hashes = {row.get("path"): row.get("sha256_lf_normalized") for row in observation if isinstance(row, dict)}
    wanted_hashes = {path.relative_to(REPO).as_posix(): digest for path, digest in INPUT_SHA256.items()}
    add_if(diagnostics, observed_hashes != wanted_hashes, "CROSS_INPUT_HASH")
    add_if(diagnostics, matrix.get("required_negative_controls") != list(NEGATIVE_CONTROL_IDS), "NEGATIVE_CONTROL_CONTRACT")

    counts = matrix.get("counts", {})
    exact_counts = {
        "adopted_source_occurrences": 43, "adopted_tex_occurrences": 41,
        "source_coverage_rows": 43, "bibliography_entries": 52,
        "bibliography_identities_chapter_scoped": 52, "bibliography_keys_distinct_global_spelling": 48,
        "bibliography_external_entries": 51, "bibliography_internal_self_report_entries": 1,
        "citation_occurrences": 99, "citation_key_occurrences": 130,
        "citation_identities_chapter_scoped": 52, "citation_keys_distinct_global_spelling": 48,
        "orphan_or_conflict_citation_keys": 0, "defined_not_cited_chapter_scoped": 0,
        "bibliography_conflicts": 0, "mixed_style_bibliography_keys": 2,
        "doi_like_occurrences": 47, "doi_tokens_distinct": 40,
        "bibliography_records_with_primary_doi": 44, "bibliography_records_without_primary_doi": 8,
        "annotation_cross_reference_doi_occurrences": 3,
        "displayed_equations": 175, "displayed_equation_environment_blocks": 160,
        "displayed_bracket_blocks": 15, "companion_equation_reference_occurrences": 100,
        "companion_equation_references_distinct": 37, "changed_prose_candidates": 237,
        "background_claims": 230, "implementation_only_prose": 6, "nonclaim_prose": 1,
        "source_attribution_statements": 226, "main_body_code_leakage_candidates": 14,
        "authority_rows": 782, "new_or_modified_assets_requiring_authority": 347,
        "new_or_modified_assets_with_authority": 347, "phase060_inherited_carry_items_preserved": 52,
        "phase060_new_blockers_preserved": 5, "new_bibliography_occurrences": 10,
        "genuinely_new_source_identity_debts": 8, "new_bibliography_alias_occurrences_not_new_source": 2,
        "external_scientific_promotions": 0, "negative_controls": 36,
    }
    for key, value in exact_counts.items():
        add_if(diagnostics, counts.get(key) != value, "COUNT_CONTRACT")
    add_if(diagnostics, counts.get("bibliography_delta_classes") != {"MODIFIED": 7, "NEW": 10, "UNCHANGED": 35}, "BIB_DELTA")
    add_if(diagnostics, counts.get("citation_delta_classes") != {"MODIFIED": 5, "NEW": 30, "UNCHANGED": 64}, "CITATION_DELTA")
    add_if(diagnostics, counts.get("equation_delta_classes") != {"MODIFIED": 1, "NEW": 6, "UNCHANGED": 168}, "EQUATION_DELTA")
    add_if(diagnostics, counts.get("source_attribution_delta_classes") != {"MODIFIED": 15, "NEW": 43, "UNCHANGED": 168}, "ATTRIBUTION_COVERAGE")
    add_if(diagnostics, expected["snapshot_eq_counts"] != (128, 32) or counts.get("displayed_equation_environment_blocks") != sum(expected["snapshot_eq_counts"]), "SNAPSHOT_EQUATION_DENOMINATOR")

    coverage = matrix.get("source_coverage")
    expected_coverage = expected["coverage"]
    if not isinstance(coverage, list) or len(coverage) != 43:
        diagnostics.add("SOURCE_COVERAGE")
    else:
        projected = [(row.get("source_id"), row.get("delta_id"), row.get("path"), row.get("sha256_lf_normalized"), row.get("physical_lines")) for row in coverage]
        wanted = [(row["source_id"], row["delta_id"], row["path"], row["sha256"], row["lines"]) for row in expected_coverage]
        add_if(diagnostics, projected != wanted or any(row.get("full_text_read") is not True for row in coverage), "SOURCE_COVERAGE")
        for row in coverage:
            evidence = row.get("review_evidence", {})
            core = {key: value for key, value in evidence.items() if key != "evidence_record_sha256"}
            if (
                evidence.get("evidence_path") != "Codex/results/PHASE_061_STEP_049_CITATION_AUTHORITY_RESULT.md"
                or evidence.get("reviewed_range") != f"1-{row.get('physical_lines')}"
                or evidence.get("frozen_source_sha256") != row.get("sha256_lf_normalized")
                or evidence.get("evidence_record_sha256") != sha256(canonical_json_bytes(core))
            ):
                diagnostics.add("FULL_READ_EVIDENCE")
        surface_counts = collections.Counter(row.get("surface_class") for row in coverage)
        add_if(diagnostics, surface_counts != collections.Counter({"SCHOLARLY_MAIN_BODY": 33, "PACKAGE_COMPANION": 2, "DESIGNATED_IMPLEMENTATION_APPENDIX": 2, "ROOT_WRAPPER": 2, "PREAMBLE": 2, "BIBLIOGRAPHY": 2}), "SURFACE_PARTITION")

    bib_rows = matrix.get("bibliography_entries")
    if not isinstance(bib_rows, list) or len(bib_rows) != 52:
        diagnostics.add("BIB_COVERAGE")
    else:
        identities = [(row.get("chapter"), row.get("key")) for row in bib_rows]
        add_if(diagnostics, len(set(identities)) != 52 or set(identities) != set(expected["bib"]), "BIB_COVERAGE")
        new_keys = {f"{row['chapter']}::{row['key']}" for row in bib_rows if row.get("delta_class") == "NEW"}
        add_if(diagnostics, new_keys != EXPECTED_NEW_BIB_KEYS or new_keys != expected["new_bib"], "BIB_DELTA")
        add_if(diagnostics, sum(len(row.get("doi_occurrences", [])) for row in bib_rows) != 47, "DOI_METADATA")
        add_if(diagnostics, any(row.get("bibliography_source_kind") not in {"EXTERNAL_METADATA_UNVERIFIED", "INTERNAL_SELF_REPORT"} for row in bib_rows), "DOI_METADATA")
        add_if(diagnostics, bib_rows != expected["semantic_bib"], "BIB_SEMANTIC_PROJECTION")
    add_if(diagnostics, matrix.get("bibliography_conflicts") != [], "BIB_CONFLICT")
    add_if(diagnostics, matrix.get("defined_not_cited") != [], "CITATION_RESOLUTION")
    mixed = matrix.get("mixed_style_bibliography_keys", [])
    add_if(diagnostics, {(row.get("chapter"), row.get("key")) for row in mixed} != {("CH2", "msmr_partI"), ("CH2", "msmr_partII")} or any(row.get("auto_rename_allowed") is not False for row in mixed), "BIB_KEY_STYLE")
    cross = matrix.get("cross_chapter_key_groups", [])
    add_if(diagnostics, {row.get("key") for row in cross} != {"bazant2013", "dahn1991", "ohzuku1993", "reynier2003"} or any(row.get("alias_collapsed") is not False for row in cross), "CROSS_ROOT_ALIAS")

    cite_rows = matrix.get("citation_occurrences")
    if not isinstance(cite_rows, list) or len(cite_rows) != 99:
        diagnostics.add("CITATION_COVERAGE")
    else:
        ids = [row.get("occurrence_id") for row in cite_rows]
        add_if(diagnostics, len(set(ids)) != 99, "CITATION_COVERAGE")
        actual_pairs = [(row.get("chapter"), row.get("command"), tuple(row.get("keys", [])), row.get("context")) for row in cite_rows]
        add_if(diagnostics, actual_pairs != expected["citations"], "CITATION_COVERAGE")
        cite_projection = [{key: value for key, value in row.items() if key != "key_resolutions"} for row in cite_rows]
        add_if(diagnostics, cite_projection != expected["semantic_cites"], "CITATION_SEMANTIC_PROJECTION")
        add_if(diagnostics, any(any(item.get("metadata_resolution") != "RESOLVED_EXACTLY_ONCE" for item in row.get("key_resolutions", [])) for row in cite_rows), "CITATION_RESOLUTION")
    add_if(diagnostics, matrix.get("orphan_or_conflict_citations") != [], "CITATION_RESOLUTION")
    index_rows = matrix.get("citation_key_index", [])
    index_ids = {(row.get("chapter"), row.get("key")) for row in index_rows}
    add_if(diagnostics, len(index_rows) != 52 or index_ids != expected["cited_identities"] or any(row.get("chapter_scoped_identity_preserved") is not True for row in index_rows), "CROSS_ROOT_ALIAS")

    eq_rows = matrix.get("displayed_equations")
    if not isinstance(eq_rows, list) or len(eq_rows) != 175:
        diagnostics.add("EQUATION_COVERAGE")
    else:
        projection = [(row.get("chapter"), row.get("semantic_identity"), row.get("body_sha256"), row.get("environment")) for row in eq_rows]
        add_if(diagnostics, collections.Counter(projection) != collections.Counter(expected["equations"]), "EQUATION_BODY")
        equation_projection = [{key: value for key, value in row.items() if key != "semantic_review_note"} for row in eq_rows]
        add_if(diagnostics, equation_projection != expected["semantic_equations"], "EQUATION_SEMANTIC_PROJECTION")
        delta = {row["semantic_identity"]: row["delta_class"] for row in eq_rows if row.get("delta_class") != "UNCHANGED"}
        add_if(diagnostics, delta != EXPECTED_EQUATION_DELTA or delta != expected["equation_delta"], "EQUATION_DELTA")
        lco = next((row for row in eq_rows if row.get("semantic_identity") == "eq:lco-slots"), {})
        add_if(diagnostics, lco.get("substantive_delta_class") != "UNCHANGED_MATHEMATICAL_CONTENT_CROSS_REFERENCE_ONLY", "EQUATION_CLASSIFICATION")
    add_if(diagnostics, expected["companion_eq_refs"] != 100 or len(matrix.get("companion_equation_references", [])) != 100, "COMPANION_BOUNDARY")

    prose = matrix.get("changed_prose_candidates")
    if not isinstance(prose, list) or len(prose) != 237:
        diagnostics.add("PROSE_COVERAGE")
    else:
        ids = [row.get("candidate_id") for row in prose]
        add_if(diagnostics, len(set(ids)) != 237 or collections.Counter(row.get("disposition") for row in prose) != collections.Counter({"BACKGROUND_CLAIM": 230, "IMPLEMENTATION_ONLY": 6, "NON_CLAIM": 1}), "PROSE_COVERAGE")
        add_if(diagnostics, prose != expected["semantic_prose"], "PROSE_SEMANTIC_PROJECTION")
    attribution_rows = matrix.get("source_attribution_statements", [])
    if not isinstance(attribution_rows, list) or len(attribution_rows) != 226:
        diagnostics.add("ATTRIBUTION_COVERAGE")
    else:
        statement_ids = [row.get("statement_id") for row in attribution_rows]
        add_if(diagnostics, statement_ids != [f"P061-ATTR-{index:04d}" for index in range(1, 227)] or len(set(statement_ids)) != 226, "ATTRIBUTION_COVERAGE")
        add_if(diagnostics, collections.Counter(row.get("delta_class") for row in attribution_rows) != collections.Counter({"UNCHANGED": 168, "NEW": 43, "MODIFIED": 15}), "ATTRIBUTION_COVERAGE")
        add_if(diagnostics, attribution_rows != expected["semantic_attributions"], "ATTRIBUTION_SEMANTIC_PROJECTION")
        add_if(diagnostics, any(row.get("delta_segment_link") is None for row in attribution_rows if row.get("delta_class") != "UNCHANGED"), "ATTRIBUTION_DELTA")
        add_if(diagnostics, any(row.get("primary_support_state") != "UNVERIFIED_EXTERNAL" or row.get("external_scientific_truth") is not False for row in attribution_rows), "AUTHORITY_PROMOTION")

    code = matrix.get("code_free_main_body_audit", {})
    anchors = {(row.get("anchor", {}).get("path"), row.get("anchor", {}).get("line_start")) for row in code.get("confirmed_policy_violations", [])}
    add_if(diagnostics, code.get("compliance_state") != "NONCOMPLIANT_V1020_SOURCE_BASELINE" or anchors != EXPECTED_CODE_ANCHORS, "CODE_FREE_POLICY")
    add_if(diagnostics, code.get("designated_tex_paths") != [
        "Claude/docs/v1.0.20/_sections/ch1_appB_codemap.tex",
        "Claude/docs/v1.0.20/_sections/ch2_appB_codemap.tex",
    ] or code.get("remediation_target_phase") != 72, "CODE_FREE_POLICY")
    add_if(diagnostics, code.get("mentions") != expected["semantic_code"] or code.get("main_body_candidates") != [row for row in expected["semantic_code"] if not row["allowed_surface"]] or code.get("confirmed_policy_violations") != [row for row in expected["semantic_code"] if not row["allowed_surface"]], "CODE_SEMANTIC_PROJECTION")
    add_if(diagnostics, matrix.get("companion_equation_references") != expected["semantic_companion"], "COMPANION_SEMANTIC_PROJECTION")

    auth = matrix.get("authority_rows")
    if not isinstance(auth, list) or len(auth) != 782:
        diagnostics.add("AUTHORITY_COVERAGE")
    else:
        ids = [row.get("asset_id") for row in auth]
        add_if(diagnostics, len(set(ids)) != 782, "AUTHORITY_COVERAGE")
        types = collections.Counter(row.get("asset_type") for row in auth)
        add_if(diagnostics, types != collections.Counter({"BIB_ENTRY": 52, "CITATION_OCCURRENCE": 99, "EQUATION": 175, "BACKGROUND_CLAIM": 230, "SOURCE_ATTRIBUTION_STATEMENT": 226}), "AUTHORITY_COVERAGE")
        add_if(diagnostics, sum(row.get("delta_class") != "UNCHANGED" for row in auth) != 347, "AUTHORITY_COVERAGE")
        expected_asset_ids = {
            *(f"P061-AUTH-BIB-{index:04d}" for index in range(1, 53)),
            *(f"P061-AUTH-CITE-{index:04d}" for index in range(1, 100)),
            *(f"P061-AUTH-EQ-{index:04d}" for index in range(1, 176)),
            *(f"P061-AUTH-CLAIM-{index:04d}" for index in range(1, 231)),
            *(f"P061-AUTH-ATTR-{index:04d}" for index in range(1, 227)),
        }
        add_if(diagnostics, set(ids) != expected_asset_ids, "AUTHORITY_COVERAGE")
        attr_auth = [row for row in auth if row.get("asset_type") == "SOURCE_ATTRIBUTION_STATEMENT"]
        add_if(diagnostics, [row.get("statement_id") for row in attr_auth] != [f"P061-ATTR-{index:04d}" for index in range(1, 227)], "ATTRIBUTION_COVERAGE")
        add_if(diagnostics, any(row.get("source_id") not in {route["source_id"] for route, _ in expected["adopted"]} or row.get("target_phase") != 71 for row in auth), "AUTHORITY_ROUTE")
        add_if(diagnostics, promoted(auth), "AUTHORITY_PROMOTION")
        eq_auth = {row.get("semantic_identity"): row for row in auth if row.get("asset_type") == "EQUATION"}
        add_if(diagnostics, eq_auth.get("eq:lco-mottcrit", {}).get("derivation_state") != "GROUND_NOT_FOUND_BARE_HEURISTIC", "EQUATION_CLASSIFICATION")
        add_if(diagnostics, eq_auth.get("eq:sm-bare", {}).get("equation_classification") != "ALGEBRAIC_RESTATEMENT", "EQUATION_CLASSIFICATION")
        coverage_by_source = {row["source_id"]: row for row in expected["coverage"]}
        asset_contracts = (
            ("BIB_ENTRY", bib_rows if isinstance(bib_rows, list) else [], {"bibliography_key": "key"}),
            ("CITATION_OCCURRENCE", cite_rows if isinstance(cite_rows, list) else [], {"occurrence_id": "occurrence_id", "citation_keys": "keys"}),
            ("EQUATION", eq_rows if isinstance(eq_rows, list) else [], {"semantic_identity": "semantic_identity", "equation_body_sha256": "body_sha256", "substantive_delta_class": "substantive_delta_class"}),
            ("BACKGROUND_CLAIM", [row for row in prose if row.get("disposition") == "BACKGROUND_CLAIM"] if isinstance(prose, list) else [], {"candidate_id": "candidate_id"}),
            ("SOURCE_ATTRIBUTION_STATEMENT", attribution_rows if isinstance(attribution_rows, list) else [], {"statement_id": "statement_id", "old_anchor": "old_anchor", "delta_segment_link": "delta_segment_link", "authority_disposition": "authority_disposition"}),
        )
        for asset_type, assets, field_map in asset_contracts:
            rows = [row for row in auth if row.get("asset_type") == asset_type]
            if len(rows) != len(assets):
                diagnostics.add("AUTHORITY_SEMANTIC_BIJECTION")
                continue
            for row, asset in zip(rows, assets):
                source = coverage_by_source.get(asset.get("source_id"), {})
                expected_fields = {
                    "asset_type": asset_type,
                    "source_id": asset.get("source_id"),
                    "delta_id": asset.get("delta_id"),
                    "chapter": asset.get("chapter"),
                    "document_root": asset.get("chapter"),
                    "delta_class": asset.get("delta_class"),
                    "source_anchor": asset.get("anchor"),
                    "source_record_sha256": source.get("sha256"),
                    **{authority_key: asset.get(asset_key) for authority_key, asset_key in field_map.items()},
                }
                if any(row.get(key) != value for key, value in expected_fields.items()):
                    diagnostics.add("AUTHORITY_SEMANTIC_BIJECTION")
                    break

    carry = matrix.get("phase060_carry_forward_preservation", {})
    prior = expected["carry"]
    inherited = carry.get("inherited_items", [])
    blockers = carry.get("new_blockers", [])
    if len(inherited) != 52 or len(blockers) != 5 or carry.get("all_states_preserved") is not True:
        diagnostics.add("CARRY_PRESERVATION")
    else:
        for actual, source in zip(inherited, prior["inherited_items"]):
            if (
                actual.get("carry_forward_id") != source["carry_forward_id"]
                or actual.get("source_record_sha256") != sha256(canonical_json_bytes(source))
                or actual.get("status_before") != source["status_before"]
                or actual.get("status_after") != source["status_after"]
                or actual.get("resolution_status") != "NOT_RESOLVED"
                or actual.get("acceptance_satisfied") is not False
                or actual.get("category_after") != source["category_after"]
                or actual.get("acceptance_criterion_after") != source["acceptance_criterion_after"]
                or actual.get("authority_boundary_after") != source["authority_boundary_after"]
                or actual.get("source_route_source_id") != source["source_route_source_id"]
                or actual.get("step49_resolution_changed") is not False
            ):
                diagnostics.add("CARRY_PRESERVATION")
                break
        for actual, source in zip(blockers, prior["new_blockers"]):
            if (
                actual.get("blocker_id") != source["blocker_id"]
                or actual.get("source_record_sha256") != sha256(canonical_json_bytes(source))
                or actual.get("status") != "OPEN"
                or actual.get("category") != source["category"]
                or actual.get("acceptance_criterion") != source["acceptance_criterion"]
                or actual.get("authority_boundary") != source["authority_boundary"]
                or actual.get("source_ids") != source["source_ids"]
                or actual.get("step49_resolution_changed") is not False
            ):
                diagnostics.add("CARRY_PRESERVATION")
                break
    debts = matrix.get("genuinely_new_source_identity_debts", [])
    debt_keys = {f"{row.get('document_root')}::{row.get('bibliography_key')}" for row in debts}
    add_if(diagnostics, len(debts) != 8 or debt_keys != EXPECTED_GENUINELY_NEW_SOURCE_KEYS or debt_keys != expected["genuine_source_keys"] or any(row.get("genuinely_new_source_identity") is not True or row.get("status") != "UNVERIFIED_EXTERNAL" or row.get("target_phase") != 71 or row.get("source_identity_basis") != "absent from all v1.0.19 adopted global keys, all DOI tokens, and normalized metadata fingerprints" for row in debts), "NEW_DEBT_IDENTITY")
    aliases = matrix.get("new_bibliography_alias_occurrences", [])
    alias_keys = {f"{row.get('chapter')}::{row.get('bibliography_key')}" for row in aliases}
    add_if(diagnostics, alias_keys != {"CH2::dahn1991", "CH2::ohzuku1993"} or alias_keys != expected["alias_source_keys"] or any(row.get("genuinely_new_source_identity") is not False or not row.get("existing_v1019_identity_basis") for row in aliases), "NEW_DEBT_IDENTITY")
    queue = matrix.get("unverified_external_queue", [])
    add_if(diagnostics, len(queue) != 3 or any(row.get("status") != "UNVERIFIED_EXTERNAL" or row.get("target_phase") != 71 for row in queue), "UNVERIFIED_ROUTE")
    add_if(diagnostics, promoted(matrix), "AUTHORITY_PROMOTION")
    # A single controlled corruption must emit one canonical diagnostic.  These
    # precedence rules suppress only derivative failures caused by the same
    # corrupted row; independent baseline failures still fail the gate.
    if "NESTED_SCHEMA_CONTRACT" in diagnostics:
        diagnostics -= {
            "BIB_SEMANTIC_PROJECTION", "CITATION_SEMANTIC_PROJECTION",
            "EQUATION_SEMANTIC_PROJECTION", "PROSE_SEMANTIC_PROJECTION",
            "ATTRIBUTION_SEMANTIC_PROJECTION", "CODE_SEMANTIC_PROJECTION",
            "COMPANION_SEMANTIC_PROJECTION", "AUTHORITY_SEMANTIC_BIJECTION",
        }
    if "AUTHORITY_PROMOTION" in diagnostics:
        diagnostics -= {"BIB_SEMANTIC_PROJECTION", "AUTHORITY_SEMANTIC_BIJECTION"}
    cascade_precedence = {
        "CITATION_COVERAGE": {"CITATION_SEMANTIC_PROJECTION", "AUTHORITY_SEMANTIC_BIJECTION"},
        "BIB_COVERAGE": {"BIB_SEMANTIC_PROJECTION", "AUTHORITY_SEMANTIC_BIJECTION"},
        "EQUATION_COVERAGE": {"EQUATION_SEMANTIC_PROJECTION", "AUTHORITY_SEMANTIC_BIJECTION"},
        "EQUATION_BODY": {"EQUATION_SEMANTIC_PROJECTION", "AUTHORITY_SEMANTIC_BIJECTION"},
        "PROSE_COVERAGE": {"PROSE_SEMANTIC_PROJECTION", "AUTHORITY_SEMANTIC_BIJECTION"},
        "ATTRIBUTION_COVERAGE": {"ATTRIBUTION_SEMANTIC_PROJECTION", "AUTHORITY_SEMANTIC_BIJECTION"},
        "AUTHORITY_ROUTE": {"AUTHORITY_SEMANTIC_BIJECTION"},
        "AUTHORITY_COVERAGE": {"ATTRIBUTION_COVERAGE", "AUTHORITY_SEMANTIC_BIJECTION"},
    }
    for primary, derivatives in cascade_precedence.items():
        if primary in diagnostics:
            diagnostics -= derivatives
    return diagnostics


CONTROL_DIAGNOSTIC = {
    "citation-fake-doi-certainty": "AUTHORITY_PROMOTION",
    "citation-key-alias-collapse": "CROSS_ROOT_ALIAS",
    "bibliography-presence-as-support": "AUTHORITY_PROMOTION",
    "equation-hash-as-validity": "AUTHORITY_PROMOTION",
    "review-consensus-promotion": "AUTHORITY_PROMOTION",
    "code-leakage-misclassification": "CODE_FREE_POLICY",
    "citation-drop-occurrence": "CITATION_COVERAGE",
    "citation-duplicate-occurrence": "CITATION_COVERAGE",
    "citation-orphan-suppression": "CITATION_RESOLUTION",
    "bibliography-drop-entry": "BIB_COVERAGE",
    "bibliography-conflict-suppression": "BIB_COVERAGE",
    "equation-drop-block": "EQUATION_COVERAGE",
    "equation-body-swap": "EQUATION_BODY",
    "background-claim-drop": "PROSE_COVERAGE",
    "background-nonclaim-promotion": "PROSE_COVERAGE",
    "source-attribution-drop": "ATTRIBUTION_COVERAGE",
    "delta-link-swap": "AUTHORITY_ROUTE",
    "rationale-as-support": "AUTHORITY_PROMOTION",
    "external-truth-promotion": "AUTHORITY_PROMOTION",
    "new-debt-alias-reuse": "NEW_DEBT_IDENTITY",
    "main-body-code-allowlist-broadening": "CODE_FREE_POLICY",
    "competitive-candidate-promotion": "AUTHORITY_ROUTE",
    "strict-json-duplicate-key": "STRICT_JSON_DUPLICATE",
    "strict-json-nonfinite": "STRICT_JSON_NONFINITE",
    "cross-input-hash": "CROSS_INPUT_HASH",
    "cross-baseline-commit": "CROSS_BASELINE_COMMIT",
    "cross-adopted-source-count": "COUNT_CONTRACT",
    "cross-authority-row-coverage": "AUTHORITY_COVERAGE",
    "cross-unverified-route": "UNVERIFIED_ROUTE",
    "nested-schema-extra-key": "NESTED_SCHEMA_CONTRACT",
    "bibliography-text-fabrication": "BIB_SEMANTIC_PROJECTION",
    "prose-text-fabrication": "PROSE_SEMANTIC_PROJECTION",
    "attribution-text-fabrication": "ATTRIBUTION_SEMANTIC_PROJECTION",
    "code-text-fabrication": "CODE_SEMANTIC_PROJECTION",
    "authority-semantic-row-swap": "AUTHORITY_SEMANTIC_BIJECTION",
    "builder-hash-mutation": "BUILDER_SECURITY",
}


def mutate_for_control(control: str, value: dict[str, Any]) -> None:
    if control == "citation-fake-doi-certainty":
        value["bibliography_entries"][0]["doi_occurrences"][0]["metadata_verified"] = True
    elif control == "citation-key-alias-collapse":
        value["citation_key_index"] = value["citation_key_index"][:-1]
    elif control == "bibliography-presence-as-support":
        value["authority_rows"][0]["primary_support_state"] = "VERIFIED_PRIMARY"
    elif control == "equation-hash-as-validity":
        next(row for row in value["authority_rows"] if row["asset_type"] == "EQUATION")["hash_is_scientific_validity"] = True
    elif control == "review-consensus-promotion":
        value["authority_rows"][0]["review_approval_is_scientific_support"] = True
    elif control == "code-leakage-misclassification":
        value["code_free_main_body_audit"]["compliance_state"] = "PASS"
    elif control == "citation-drop-occurrence":
        value["citation_occurrences"].pop()
    elif control == "citation-duplicate-occurrence":
        value["citation_occurrences"].append(copy.deepcopy(value["citation_occurrences"][0]))
    elif control == "citation-orphan-suppression":
        value["citation_occurrences"][0]["key_resolutions"][0]["metadata_resolution"] = "ORPHAN"
    elif control == "bibliography-drop-entry":
        value["bibliography_entries"].pop()
    elif control == "bibliography-conflict-suppression":
        value["bibliography_entries"].append(copy.deepcopy(value["bibliography_entries"][0]))
        value["bibliography_entries"][-1]["normalized_body"] += " conflict"
    elif control == "equation-drop-block":
        value["displayed_equations"].pop()
    elif control == "equation-body-swap":
        value["displayed_equations"][0]["body_sha256"] = "0" * 64
    elif control == "background-claim-drop":
        index = next(i for i, row in enumerate(value["changed_prose_candidates"]) if row["disposition"] == "BACKGROUND_CLAIM")
        value["changed_prose_candidates"].pop(index)
    elif control == "background-nonclaim-promotion":
        next(row for row in value["changed_prose_candidates"] if row["disposition"] == "NON_CLAIM")["disposition"] = "BACKGROUND_CLAIM"
    elif control == "source-attribution-drop":
        value["source_attribution_statements"].pop()
        value["source_attribution_statements"].append(copy.deepcopy(value["source_attribution_statements"][0]))
    elif control == "delta-link-swap":
        value["authority_rows"][0]["source_id"] = "P061-SRC-9999"
    elif control == "rationale-as-support":
        value["authority_rows"][0]["rationale_is_support"] = True
    elif control == "external-truth-promotion":
        value["authority_rows"][0]["external_scientific_truth"] = True
    elif control == "new-debt-alias-reuse":
        value["genuinely_new_source_identity_debts"][1]["bibliography_key"] = value["genuinely_new_source_identity_debts"][0]["bibliography_key"]
    elif control == "main-body-code-allowlist-broadening":
        value["code_free_main_body_audit"]["designated_tex_paths"].append("Other/path/ch1_appB_codemap.tex")
    elif control == "competitive-candidate-promotion":
        value["authority_rows"][0]["source_id"] = "COMPETITIVE-CANDIDATE"
    elif control == "cross-input-hash":
        value["observation_inputs"][0]["sha256_lf_normalized"] = "0" * 64
    elif control == "cross-baseline-commit":
        value["baseline_commit"] = "0" * 40
    elif control == "cross-adopted-source-count":
        value["counts"]["adopted_source_occurrences"] = 42
    elif control == "cross-authority-row-coverage":
        value["authority_rows"].pop()
        value["authority_rows"].append(copy.deepcopy(value["authority_rows"][0]))
    elif control == "cross-unverified-route":
        value["unverified_external_queue"][0]["target_phase"] = 72
    elif control == "nested-schema-extra-key":
        value["bibliography_entries"][0]["unexpected_key"] = "forbidden"
    elif control == "bibliography-text-fabrication":
        value["bibliography_entries"][0]["body"] = "fabricated"
    elif control == "prose-text-fabrication":
        value["changed_prose_candidates"][0]["text"] = "fabricated"
    elif control == "attribution-text-fabrication":
        value["source_attribution_statements"][0]["text"] = "fabricated"
    elif control == "code-text-fabrication":
        value["code_free_main_body_audit"]["confirmed_policy_violations"][0]["text"] = "fabricated"
    elif control == "authority-semantic-row-swap":
        rows = [row for row in value["authority_rows"] if row["asset_type"] == "BIB_ENTRY"]
        rows[0]["bibliography_key"] = rows[1]["bibliography_key"]
    elif control == "builder-hash-mutation":
        return
    else:
        raise ValidationError(f"UNIMPLEMENTED_CONTROL:{control}")


def run_negative_controls(matrix: dict[str, Any], expected: dict[str, Any]) -> tuple[int, int]:
    if content_diagnostics(matrix, expected):
        raise ValidationError("NEGATIVE_BASELINE_NOT_CLEAN")
    passed = 0
    for control in NEGATIVE_CONTROL_IDS:
        wanted = CONTROL_DIAGNOSTIC[control]
        if control == "strict-json-duplicate-key":
            try:
                strict_load_bytes(b'{"x":1,"x":2}')
                observed = set()
            except DuplicateKeyError:
                observed = {"STRICT_JSON_DUPLICATE"}
        elif control == "strict-json-nonfinite":
            try:
                strict_load_bytes(b'{"x":NaN}')
                observed = set()
            except NonFiniteNumberError:
                observed = {"STRICT_JSON_NONFINITE"}
        elif control == "builder-hash-mutation":
            observed = builder_security_diagnostics(lf_bytes(BUILDER.read_bytes()) + b"\n# controlled mutation\n")
        else:
            mutated = copy.deepcopy(matrix)
            mutate_for_control(control, mutated)
            observed = content_diagnostics(mutated, expected)
        if observed != {wanted}:
            print(f"FAIL NEGATIVE_{control} wanted={wanted} observed={sorted(observed)}")
        else:
            passed += 1
    return passed, len(NEGATIVE_CONTROL_IDS)


def determinism_check(stored: bytes) -> tuple[int, int]:
    with tempfile.TemporaryDirectory(prefix="p061_step49_") as temp:
        first = Path(temp) / "one.json"
        second = Path(temp) / "two.json"
        for output in (first, second):
            proc = subprocess.run([sys.executable, str(BUILDER), "--output", str(output)], cwd=REPO, check=False, capture_output=True, timeout=120)
            if proc.returncode:
                raise ValidationError(f"BUILDER_DETERMINISM:{proc.returncode}:{proc.stdout.decode('utf-8', errors='replace')}")
        one, two = first.read_bytes(), second.read_bytes()
    return int(one == two), int(one == stored)


def read_optional(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.is_file() else None


def control_document_diagnostics() -> set[str]:
    diagnostics: set[str] = set()
    result = read_optional(RESULT)
    active = read_optional(ACTIVE_LEDGER)
    parent = read_optional(PARENT_LEDGER)
    handover = read_optional(HANDOVER)
    common = (
        "Step 49", "PASS_WITH_CONCERNS_P061_STEP49_CITATION_AUTHORITY",
        "PENDING_AT_PRECOMMIT_BY_DESIGN", EXPECTED_SUBJECT, "Step 50", "persistence",
    )
    if result is None or any(token not in result for token in common) or "PHASE_061_V1020_CITATION_AUTHORITY_MATRIX.json" not in result:
        diagnostics.add("RESULT_CONTRACT")
    for text, code in ((active, "ACTIVE_LEDGER_CONTRACT"), (parent, "PARENT_LEDGER_CONTRACT"), (handover, "HANDOVER_CONTRACT")):
        if text is None or any(token not in text for token in common):
            diagnostics.add(code)
    if active is not None and (EXPECTED_PARENT not in active or "PASS_P061_STEP48_PERSISTENCE" not in active):
        diagnostics.add("ACTIVE_LEDGER_CONTRACT")
    if handover is not None and (EXPECTED_PARENT not in handover or "PASS_P061_STEP48_PERSISTENCE" not in handover):
        diagnostics.add("HANDOVER_CONTRACT")
    return diagnostics


def parse_porcelain_z(data: bytes) -> set[str]:
    paths: set[str] = set()
    fields = data.split(b"\0")
    index = 0
    while index < len(fields) and fields[index]:
        field = fields[index].decode("utf-8")
        status, path = field[:2], field[3:]
        paths.add(path.replace("\\", "/"))
        index += 1
        if status[0] in {"R", "C"}:
            index += 1
    return paths


def remote_tip(branch: str) -> str:
    text = run_git_text(["ls-remote", "--heads", "origin", f"refs/heads/{branch}"], "LS_REMOTE")
    return text.split()[0] if text else ""


def live_evidence() -> dict[str, Any]:
    return {
        "branch": run_git_text(["branch", "--show-current"], "BRANCH"),
        "head": run_git_text(["rev-parse", "HEAD"], "HEAD"),
        "upstream": run_git_text(["rev-parse", "@{u}"], "UPSTREAM"),
        "active_remote": remote_tip(ACTIVE_BRANCH),
        "protected_local": run_git_text(["rev-parse", f"origin/{PROTECTED_BRANCH}"], "PROTECTED_LOCAL"),
        "protected_remote": remote_tip(PROTECTED_BRANCH),
        "main_local": run_git_text(["rev-parse", "origin/main"], "MAIN_LOCAL"),
        "main_remote": remote_tip("main"),
        "dirty": parse_porcelain_z(run_git_bytes(["status", "--porcelain=v1", "-z", "--untracked-files=all"], "STATUS")),
        "staged": set(run_git_text(["diff", "--cached", "--name-only"], "STAGED").splitlines()),
        "unstaged": set(run_git_text(["diff", "--name-only"], "UNSTAGED").splitlines()),
        "claude_diff": set(run_git_text(["diff", "--name-only", f"origin/{PROTECTED_BRANCH}", "--", "Claude"], "CLAUDE_DIFF").splitlines()),
        "claude_untracked": set(run_git_text(["ls-files", "--others", "--exclude-standard", "--", "Claude"], "CLAUDE_UNTRACKED").splitlines()),
    }


def repository_diagnostics(evidence: dict[str, Any], verify_staged: bool) -> set[str]:
    diagnostics: set[str] = set()
    add_if(diagnostics, evidence["branch"] != ACTIVE_BRANCH, "ACTIVE_BRANCH")
    add_if(diagnostics, evidence["head"] != EXPECTED_PARENT or evidence["upstream"] != EXPECTED_PARENT or evidence["active_remote"] != EXPECTED_PARENT, "PRECOMMIT_PARENT")
    add_if(diagnostics, evidence["protected_local"] != PROTECTED_TIP or evidence["protected_remote"] != PROTECTED_TIP, "PROTECTED_BRANCH")
    add_if(diagnostics, evidence["main_local"] != MAIN_TIP or evidence["main_remote"] != MAIN_TIP, "MAIN_BRANCH")
    add_if(diagnostics, evidence["dirty"] != set(EXACT_SEVEN), "WORKTREE_EXACT_SEVEN")
    add_if(diagnostics, bool(evidence["claude_diff"] or evidence["claude_untracked"]), "CLAUDE_IMMUTABLE")
    if verify_staged:
        add_if(diagnostics, evidence["staged"] != set(EXACT_SEVEN), "STAGING_EXACT_SEVEN")
        add_if(diagnostics, bool(evidence["unstaged"]), "STAGING_UNSTAGED")
    return diagnostics


def persistence_diagnostics(evidence: dict[str, Any]) -> set[str]:
    diagnostics: set[str] = set()
    head = evidence["head"]
    add_if(diagnostics, evidence["branch"] != ACTIVE_BRANCH, "ACTIVE_BRANCH")
    add_if(diagnostics, head == EXPECTED_PARENT, "PERSISTENCE_HEAD")
    if head != EXPECTED_PARENT:
        parent = run_git_text(["rev-parse", f"{head}^"], "PERSISTENCE_PARENT")
        subject = run_git_text(["show", "-s", "--format=%s", head], "PERSISTENCE_SUBJECT")
        files = set(run_git_text(["diff-tree", "--no-commit-id", "--name-only", "-r", head], "PERSISTENCE_FILES").splitlines())
        add_if(diagnostics, parent != EXPECTED_PARENT, "PERSISTENCE_PARENT")
        add_if(diagnostics, subject != EXPECTED_SUBJECT, "PERSISTENCE_SUBJECT")
        add_if(diagnostics, files != set(EXACT_SEVEN), "PERSISTENCE_EXACT_SEVEN")
    add_if(diagnostics, evidence["upstream"] != head or evidence["active_remote"] != head, "PERSISTENCE_REMOTE")
    add_if(diagnostics, bool(evidence["dirty"] or evidence["staged"] or evidence["unstaged"]), "PERSISTENCE_CLEAN")
    add_if(diagnostics, evidence["protected_local"] != PROTECTED_TIP or evidence["protected_remote"] != PROTECTED_TIP, "PROTECTED_BRANCH")
    add_if(diagnostics, evidence["main_local"] != MAIN_TIP or evidence["main_remote"] != MAIN_TIP, "MAIN_BRANCH")
    add_if(diagnostics, bool(evidence["claude_diff"] or evidence["claude_untracked"]), "CLAUDE_IMMUTABLE")
    return diagnostics


def canonical_ast_sha256(tree: ast.AST) -> str:
    """Serialize AST fields explicitly so Python 3.12/3.14 hash identically."""
    def project(value: Any) -> Any:
        if isinstance(value, ast.AST):
            return {
                "node": type(value).__name__,
                "fields": {field: project(getattr(value, field, None)) for field in value._fields},
            }
        if isinstance(value, list):
            return [project(item) for item in value]
        if isinstance(value, bytes):
            return {"bytes_hex": value.hex()}
        if value is Ellipsis:
            return {"ellipsis": True}
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        raise ValidationError(f"AST_VALUE_TYPE:{type(value).__name__}")

    encoded = json.dumps(project(tree), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded)


def builder_security_diagnostics(source_override: bytes | None = None) -> set[str]:
    diagnostics: set[str] = set()
    source_bytes = lf_bytes(BUILDER.read_bytes() if source_override is None else source_override)
    text = source_bytes.decode("utf-8")
    if sha256(source_bytes) != EXPECTED_BUILDER_SHA256:
        diagnostics.add("BUILDER_SECURITY")
    try:
        tree = ast.parse(text, filename=str(BUILDER))
    except SyntaxError:
        diagnostics.add("BUILDER_SECURITY")
        return diagnostics
    ast_hash = canonical_ast_sha256(tree)
    if ast_hash != EXPECTED_BUILDER_AST_SHA256:
        diagnostics.add("BUILDER_SECURITY")
    allowed_imports = {
        "__future__", "argparse", "collections", "hashlib", "json", "math", "re",
        "subprocess", "sys", "pathlib", "typing",
    }
    subprocess_calls = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name.split(".")[0] not in allowed_imports for alias in node.names):
                diagnostics.add("BUILDER_SECURITY")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in allowed_imports:
                diagnostics.add("BUILDER_SECURITY")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__", "getattr", "setattr"}:
                diagnostics.add("BUILDER_SECURITY")
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                subprocess_calls += 1
                argv = node.args[0] if node.args else None
                literal_argv = [item.value for item in argv.elts] if isinstance(argv, ast.List) and all(isinstance(item, ast.Constant) and isinstance(item.value, str) for item in argv.elts) else None
                keyword_names = {item.arg for item in node.keywords}
                if node.func.attr != "run" or literal_argv != ["git", "cat-file", "--batch"] or "shell" in keyword_names:
                    diagnostics.add("BUILDER_SECURITY")
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id in {"os", "sys"} and node.attr in {"system", "popen", "modules", "path"}:
            diagnostics.add("BUILDER_SECURITY")
    if subprocess_calls != 1:
        diagnostics.add("BUILDER_SECURITY")
    return diagnostics


def validate(run_controls: bool, run_determinism: bool, verify_staged: bool, verify_persistence: bool) -> tuple[set[str], dict[str, tuple[int, int]], dict[str, Any]]:
    diagnostics: set[str] = set()
    counters: dict[str, tuple[int, int]] = {}
    if not all(path.is_file() for path in (BUILDER, VALIDATOR, MATRIX)):
        return {"REQUIRED_ARTIFACT_MISSING"}, counters, {}
    expected = independent_expected()
    matrix = strict_load(MATRIX)
    nodes, depth = walk_finite(matrix)
    diagnostics |= content_diagnostics(matrix, expected)
    diagnostics |= builder_security_diagnostics()
    diagnostics |= control_document_diagnostics()
    if run_controls and not diagnostics:
        counters["controls"] = run_negative_controls(matrix, expected)
        add_if(diagnostics, counters["controls"][0] != counters["controls"][1], "NEGATIVE_CONTROLS")
    if run_determinism and not diagnostics:
        same_runs, stored_equal = determinism_check(MATRIX.read_bytes())
        counters["determinism"] = (same_runs + stored_equal, 2)
        add_if(diagnostics, same_runs != 1 or stored_equal != 1, "DETERMINISM")
    evidence = live_evidence()
    if verify_persistence:
        diagnostics |= persistence_diagnostics(evidence)
    else:
        diagnostics |= repository_diagnostics(evidence, verify_staged)
    counters["strict_json"] = (2, 2)
    return diagnostics, counters, {"nodes": nodes, "depth": depth, "evidence": evidence}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-controls", action="store_true")
    parser.add_argument("--skip-determinism", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    args = parser.parse_args()
    try:
        diagnostics, counters, meta = validate(
            run_controls=not args.skip_controls,
            run_determinism=not args.skip_determinism,
            verify_staged=args.verify_staged,
            verify_persistence=args.verify_persistence,
        )
    except (ValidationError, DuplicateKeyError, NonFiniteNumberError, UnicodeError, OSError, ValueError) as exc:
        print(f"FAIL_P061_STEP49_CITATION_AUTHORITY {type(exc).__name__}:{exc}")
        return 1
    for name, (passed, total) in counters.items():
        label = name.upper()
        print(f"PASS_P061_STEP49_{label} {passed}/{total}")
    if diagnostics:
        print("FAIL " + " ".join(sorted(diagnostics)))
        print(f"FAIL_P061_STEP49_CITATION_AUTHORITY diagnostics={len(diagnostics)}")
        return 1
    label = "PERSISTENCE" if args.verify_persistence else ("STAGED" if args.verify_staged else "PRECOMMIT")
    print(f"PASS_P061_STEP49_{label} matrix_nodes={meta['nodes']} depth={meta['depth']}")
    print("PASS_WITH_CONCERNS_P061_STEP49_CITATION_AUTHORITY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
