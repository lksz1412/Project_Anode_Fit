#!/usr/bin/env python3
"""Validate the Phase 059 theory structure index and exact diffs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "Codex" / "results"
INDEX = RESULTS / "PHASE_059_THEORY_SOURCE_INDEX.json"
DIFF = RESULTS / "PHASE_059_THEORY_LINEAGE_DIFF.json"
SUMMARY = RESULTS / "PHASE_059_THEORY_SOURCE_STRUCTURE_INDEX.md"
COVERAGE = RESULTS / "PHASE_059_V1014_V1018_2_TEXT_COVERAGE.json"


def git_blob_sha(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def main() -> None:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    diff = json.loads(DIFF.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    theory_coverage = {
        document["blob_sha"]: document
        for document in coverage["documents"]
        if "/graphite_ica_ch" in document["representative_path"]
        or document["representative_path"].endswith(
            "/appendix_phase_separation.tex"
        )
    }
    checks: list[tuple[str, bool]] = []
    checks.append(("summary exists", SUMMARY.is_file()))
    checks.append(
        ("index gate exact", index["status"] == "PASS_P059_THEORY_SOURCE_INDEX")
    )
    checks.append(
        ("diff gate exact", diff["status"] == "PASS_P059_THEORY_EXACT_DIFF")
    )
    checks.append(("theory document count", index["document_count"] == 17))
    checks.append(("theory line count", index["total_lines"] == 28876))
    checks.append(("coverage theory count", len(theory_coverage) == 17))
    checks.append(
        (
            "index/coverage blobs exact",
            {document["blob_sha"] for document in index["documents"]}
            == set(theory_coverage),
        )
    )
    checks.append(("diff comparison count", diff["comparison_count"] == 17))
    checks.append(
        (
            "v1.0.15-v1.0.16 appendix copy detected",
            any(
                comparison["pair_id"] == "appendix_v1015_to_v1016"
                and comparison["content_identical"]
                for comparison in diff["comparisons"]
            ),
        )
    )

    source_hashes_ok = True
    line_counts_ok = True
    equation_aggregate = 0
    label_aggregate = 0
    definition_aggregate = 0
    bibliography_aggregate = 0
    for document in index["documents"]:
        payload = (ROOT / document["representative_path"]).read_bytes()
        source_hashes_ok &= git_blob_sha(payload) == document["blob_sha"]
        line_counts_ok &= (
            len(payload.decode("utf-8").splitlines()) == document["line_count"]
        )
        equation_aggregate += document["equation_environment_count"]
        label_aggregate += document["label_count"]
        definition_aggregate += document["definition_cue_count"]
        bibliography_aggregate += document["bibliography_item_count"]
    checks.append(("all source hashes exact", source_hashes_ok))
    checks.append(("all source line counts exact", line_counts_ok))
    checks.append(
        (
            "equation aggregate exact",
            equation_aggregate == index["equation_environment_count"],
        )
    )
    checks.append(
        ("label aggregate exact", label_aggregate == index["label_occurrence_count"])
    )
    checks.append(
        (
            "definition aggregate exact",
            definition_aggregate == index["definition_cue_count"],
        )
    )
    checks.append(
        (
            "bibliography aggregate exact",
            bibliography_aggregate
            == index["bibliography_item_occurrence_count"],
        )
    )

    patch_hashes_ok = True
    pair_hashes_ok = True
    for comparison in diff["comparisons"]:
        patch = (ROOT / comparison["exact_unified_diff"]).read_bytes()
        patch_hashes_ok &= (
            hashlib.sha256(patch).hexdigest()
            == comparison["exact_unified_diff_sha256"]
        )
        pair_hashes_ok &= (
            git_blob_sha((ROOT / comparison["old_path"]).read_bytes())
            == comparison["old_blob_sha"]
        )
        pair_hashes_ok &= (
            git_blob_sha((ROOT / comparison["new_path"]).read_bytes())
            == comparison["new_blob_sha"]
        )
    checks.append(("all exact patch hashes", patch_hashes_ok))
    checks.append(("all diff endpoint hashes", pair_hashes_ok))

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}")
    if failed:
        raise SystemExit(f"PHASE 059 THEORY INDEX FAIL: {failed}")
    print(
        "PASS_P059_THEORY_INDEX_AND_DIFF "
        f"checks={len(checks)}/{len(checks)} documents=17 "
        f"equations={index['equation_environment_count']} comparisons=17"
    )


if __name__ == "__main__":
    main()
