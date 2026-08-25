#!/usr/bin/env python3
"""Build the Phase 060 Step 40 frozen source/topology evidence artifact.

The independent full-text reviews are represented only as coverage/evidence
claims.  Inventory, hashes, lexical anchors, include topology and predecessor
comparison are reconstructed from frozen Git objects through the already-red
Step 40 validator contract.  No Claude source is opened for writing.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


REPO = Path(__file__).resolve().parents[3]
VALIDATOR = REPO / "Codex/work/v1019_phase060/validate_phase060_step40_source_topology.py"
DEFAULT_OUTPUT = REPO / "Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json"


def load_validator_contract() -> ModuleType:
    spec = importlib.util.spec_from_file_location("phase060_step40_contract", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator contract: {VALIDATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def review_evidence(
    source: dict[str, Any],
    attestation_summary: dict[str, Any],
    attestation_by_path: dict[str, dict[str, Any]],
) -> tuple[list[str], str, list[dict[str, int]], str]:
    path = source["path"]
    if not path.endswith(".tex"):
        return (
            ["P060-STEP40-GIT-BLOB-INVENTORY-ONLY"],
            "INVENTORIED_ONLY",
            [],
            "Git-blob identity and extent inventory only; content review belongs to its scheduled later Step",
        )

    attested = attestation_by_path[path]
    physical_lines = attested["physical_lines"]
    if path.endswith("appendix_phase_separation.tex"):
        evidence = ["P060-STEP40-READ-FULL-STANDALONE-1-FILE-497-LINES"]
    elif "/_sections/ch1_" in path or path.endswith(
        "graphite_ica_ch1_v1.0.19.tex"
    ):
        evidence = ["P060-STEP40-READ-FULL-CH1-25-FILES-3711-LINES"]
    else:
        evidence = ["P060-STEP40-READ-FULL-CH2-16-FILES-1428-LINES"]
    return (
        evidence
        + [
            "P060-STEP40-READ-ATTESTATION-SHA256:"
            + attestation_summary["sha256"],
            f"P060-STEP40-READ-FULL-PATH:{path}:1-{physical_lines}",
            "P060-STEP40-LEXICAL-CONTENT-INDEX",
        ],
        attested["coverage_status"],
        attested["actual_coverage"],
        "Full source-content and lexical-topology evidence only; scientific truth, build success and implementation conformance remain unverified",
    )


def materialize_sources(
    expected: list[dict[str, Any]],
    attestation_summary: dict[str, Any],
    attestation_by_path: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for source in expected:
        evidence, status, coverage, authority = review_evidence(
            source, attestation_summary, attestation_by_path
        )
        result.append(
            {
                **source,
                "actual_coverage": coverage,
                "coverage_status": status,
                "evidence": evidence,
                "authority_boundary": authority,
            }
        )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the Phase 060 Step 40 source/topology artifact."
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Output JSON path; relative paths resolve from the repository root.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    if not output.is_absolute():
        output = REPO / output

    contract = load_validator_contract()
    expected_sources = contract.load_expected_sources()
    attestation_summary, attestation_by_path = contract.load_read_attestation(
        expected_sources
    )
    topology = contract.build_expected_topology(expected_sources)
    content_index = contract.build_expected_content_index(expected_sources)
    predecessor = contract.build_expected_predecessor_comparison(
        expected_sources, topology
    )
    diagnostics = contract.build_expected_diagnostics(
        expected_sources, topology, content_index
    )
    counts = contract.build_expected_counts(
        expected_sources,
        topology,
        content_index,
        predecessor,
    )
    artifact = {
        "schema_version": 1,
        "generated_date": "2026-08-26",
        "phase": 60,
        "step": 40,
        "artifact_kind": contract.ARTIFACT_KIND,
        "baseline_commit": contract.BASELINE,
        "authority_boundary": contract.AUTHORITY_BOUNDARY,
        "counts": counts,
        "sources": materialize_sources(
            expected_sources, attestation_summary, attestation_by_path
        ),
        "read_attestation": attestation_summary,
        "include_topology": topology,
        "content_index": content_index,
        "predecessor_comparison": predecessor,
        "diagnostics": diagnostics,
        "protection": contract.expected_protection(),
    }
    serialized = json.dumps(
        artifact, ensure_ascii=False, indent=2, sort_keys=True
    ).encode("utf-8") + b"\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(serialized)
    try:
        label = output.resolve().relative_to(REPO.resolve()).as_posix()
    except ValueError:
        label = str(output.resolve())
    print(f"WROTE {label}")
    print(
        "COUNTS "
        f"sources={len(artifact['sources'])} "
        f"tex={counts['tex_files']} "
        f"tex_lines={counts['tex_physical_lines']} "
        f"edges={counts['include_edges']} "
        f"lexical_records={counts['content_index_records']}"
    )
    print(f"SHA256 {hashlib.sha256(serialized).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
