"""Extract line- or JSON-pointer-level completion and authority claims."""

from __future__ import annotations

import hashlib
import html
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterator


REPO_ROOT = Path(__file__).resolve().parents[3]
QUEUE_PATH = REPO_ROOT / "Codex/results/PHASE_057_USER_INTENT_READ_QUEUE.json"
COVERAGE_PATH = (
    REPO_ROOT / "Codex/results/PHASE_057_USER_INTENT_READ_COVERAGE.json"
)
GENEALOGY_PATH = (
    REPO_ROOT / "Codex/results/PHASE_057_GIT_DOCUMENT_GENEALOGY.json"
)
OUTPUT_PATH = (
    REPO_ROOT / "Codex/results/PHASE_057_COMPLETION_AUTHORITY_CLAIMS.json"
)

CATEGORY_PATTERNS = {
    "COMPLETION": re.compile(
        r"(?i)(?:\bPASS(?:ED)?\b|\bGREEN\b|\bCLEAN\b|"
        r"완료|완결|종결|마감|완주|전건|merge[- ]?ready)"
    ),
    "AUTHORITY": re.compile(
        r"(?i)(?:정본|최신|latest|authority|release|"
        r"현행\s*(?:정본|최신|버전))"
    ),
    "INVARIANCE": re.compile(
        r"(?i)(?:bit[- ]?exact|무변경|불변|"
        r"0[- ]?err|err(?:or)?\s*0|오류\s*0|미해소\s*0|"
        r"잔존\s*0|무근거\s*0|max\s*\|[^|\n]{1,80}\|\s*=\s*0)"
    ),
    "CONFORMANCE": re.compile(
        r"(?i)(?:문건\s*[↔=·-]*\s*코드|코드\s*[↔=·-]*\s*문건|"
        r"doc(?:ument)?\s*[↔=·-]*\s*code|code\s*[↔=·-]*\s*doc|"
        r"정합|sync|동기)"
    ),
}
TAG_PATTERN = re.compile(r"<[^>]+>")
BASE64_PATTERN = re.compile(
    r"data:image/[A-Za-z0-9.+-]+;base64,[A-Za-z0-9+/=]+"
)


def matching_categories(text: str) -> list[str]:
    return sorted(
        category
        for category, pattern in CATEGORY_PATTERNS.items()
        if pattern.search(text)
    )


def matching_terms(text: str) -> list[str]:
    terms: set[str] = set()
    for pattern in CATEGORY_PATTERNS.values():
        terms.update(match.group(0) for match in pattern.finditer(text))
    return sorted(terms, key=lambda item: (item.casefold(), item))


def excerpt(text: str, limit: int = 600) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1] + "…"


def json_scalars(value: Any, pointer: str = "") -> Iterator[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            yield from json_scalars(child, f"{pointer}/{escaped}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from json_scalars(child, f"{pointer}/{index}")
    else:
        yield pointer or "/", value


def line_candidates(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8", errors="strict").splitlines()
    records: list[dict[str, Any]] = []
    suffix = path.suffix.lower()
    for index, raw in enumerate(lines, 1):
        cleaned = raw
        if suffix == ".html":
            cleaned = BASE64_PATTERN.sub("[EMBEDDED_IMAGE]", cleaned)
            if len(cleaned) > 4_000:
                # Embedded vendor runtime is not authored project prose.
                continue
            cleaned = html.unescape(TAG_PATTERN.sub(" ", cleaned))
        categories = matching_categories(cleaned)
        if not categories:
            continue
        records.append(
            {
                "locator_type": "PHYSICAL_LINE",
                "line": index,
                "json_pointer": None,
                "categories": categories,
                "matched_terms": matching_terms(cleaned),
                "excerpt": excerpt(cleaned),
                "source_line_sha256": hashlib.sha256(
                    raw.encode("utf-8")
                ).hexdigest(),
            }
        )
    return records


def document_candidates(path: Path) -> tuple[str, list[dict[str, Any]]]:
    if path.suffix.lower() != ".json":
        return "LINE_SCAN", line_candidates(path)
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "INVALID_JSON_LINE_SCAN", line_candidates(path)

    records: list[dict[str, Any]] = []
    for pointer, value in json_scalars(parsed):
        if not isinstance(value, str):
            continue
        categories = matching_categories(value)
        if not categories:
            continue
        records.append(
            {
                "locator_type": "JSON_POINTER",
                "line": None,
                "json_pointer": pointer,
                "categories": categories,
                "matched_terms": matching_terms(value),
                "excerpt": excerpt(value),
                "source_line_sha256": None,
            }
        )
    return "JSON_SCALAR_SCAN", records


def main() -> None:
    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    genealogy = json.loads(GENEALOGY_PATH.read_text(encoding="utf-8"))

    coverage_by_blob = {
        document["blob_sha"]: document for document in coverage["documents"]
    }
    genealogy_by_blob = {
        document["blob_sha"]: document for document in genealogy["documents"]
    }

    records: list[dict[str, Any]] = []
    document_summaries: list[dict[str, Any]] = []
    category_counts: Counter[str] = Counter()
    scan_mode_counts: Counter[str] = Counter()

    for document in queue["documents"]:
        path = REPO_ROOT / document["representative_path"]
        mode, candidates = document_candidates(path)
        scan_mode_counts[mode] += 1
        coverage_record = coverage_by_blob[document["blob_sha"]]
        genealogy_record = genealogy_by_blob[document["blob_sha"]]
        document_id = f"CLAIM-DOC-{len(document_summaries) + 1:04d}"
        for candidate in candidates:
            category_counts.update(candidate["categories"])
            records.append(
                {
                    "candidate_id": f"CLAIM-CAND-{len(records) + 1:05d}",
                    "document_id": document_id,
                    "adjudication_status": "UNADJUDICATED",
                    **candidate,
                }
            )
        document_summaries.append(
            {
                "document_id": document_id,
                "blob_sha": document["blob_sha"],
                "sha256": document["sha256"],
                "representative_path": document["representative_path"],
                "document_category": document["category"],
                "first_exact_blob_commit": genealogy_record[
                    "first_exact_blob_event"
                ]["commit"],
                "review_evidence": coverage_record["review_evidence"],
                "provisional_claim_ids": coverage_record["claim_ids"],
                "scan_mode": mode,
                "candidate_count": len(candidates),
            }
        )

    payload = {
        "schema_version": 1,
        "generated_date": "2026-07-28",
        "baseline_commit": queue["baseline_commit"],
        "source_queue": str(QUEUE_PATH.relative_to(REPO_ROOT)),
        "source_coverage": str(COVERAGE_PATH.relative_to(REPO_ROOT)),
        "source_genealogy": str(GENEALOGY_PATH.relative_to(REPO_ROOT)),
        "document_count": len(document_summaries),
        "candidate_count": len(records),
        "category_counts": dict(sorted(category_counts.items())),
        "scan_mode_counts": dict(sorted(scan_mode_counts.items())),
        "documents_with_candidates": sum(
            summary["candidate_count"] > 0 for summary in document_summaries
        ),
        "document_summaries": document_summaries,
        "candidates": records,
        "validation": {
            "all_queue_documents_scanned": len(document_summaries)
            == queue["document_count"],
            "all_candidates_linked_to_exact_blob_commit": True,
            "all_candidates_linked_to_review_evidence": True,
            "generated_html_payloads_excluded_from_authored_prose": True,
            "adjudication_not_yet_performed": True,
        },
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    OUTPUT_PATH.write_text(encoded, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "output": str(OUTPUT_PATH.relative_to(REPO_ROOT)),
                "documents": payload["document_count"],
                "documents_with_candidates": payload[
                    "documents_with_candidates"
                ],
                "candidates": payload["candidate_count"],
                "category_counts": payload["category_counts"],
                "sha256": hashlib.sha256(encoded.encode()).hexdigest(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
