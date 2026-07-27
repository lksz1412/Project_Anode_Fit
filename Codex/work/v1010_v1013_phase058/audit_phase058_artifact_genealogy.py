#!/usr/bin/env python3
"""Connect Phase 058 PDFs/images to their source and regeneration history."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "Codex" / "results" / "PHASE_058_ARTIFACT_GENEALOGY.json"
EXECUTION = (
    ROOT / "Codex" / "results" / "PHASE_058_LEGACY_ISOLATED_EXECUTION.json"
)

PDFS = [
    (
        f"Claude/docs/{version}/graphite_ica_{chapter}_{version}.pdf",
        f"Claude/docs/{version}/graphite_ica_{chapter}_{version}.tex",
    )
    for version in ("v1.0.10", "v1.0.11", "v1.0.12", "v1.0.13")
    for chapter in ("ch1", "ch2")
]
IMAGES = [
    (
        "Claude/docs/v1.0.10/figs/Anode_Fit_v1.0.10_sample_test.png",
        "Claude/docs/v1.0.10/sample_test_v1010.py",
        "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py",
    ),
    (
        "Claude/docs/v1.0.10/figs/P4_lco_heat_validation.png",
        "Claude/docs/v1.0.10/demo_lco_heat.py",
        "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py",
    ),
    (
        "Claude/docs/v1.0.10/figs/P5_graph_suite.png",
        "Claude/docs/v1.0.10/graph_suite_p5.py",
        "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py",
    ),
    (
        "Claude/docs/v1.0.10/figs/anode_fit_v1_0_10_dqdv.png",
        "Claude/docs/v1.0.10/plot_dqdv.py",
        "Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py",
    ),
    (
        "Claude/docs/v1.0.12/sample_test_v1012.png",
        "Claude/docs/v1.0.12/sample_test_v1012.py",
        "Claude/docs/v1.0.12/Anode_Fit_v1.0.12.py",
    ),
    (
        "Claude/docs/v1.0.13/figs/P4_lco_heat_validation.png",
        "Claude/docs/v1.0.13/demo_lco_heat.py",
        "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py",
    ),
    (
        "Claude/docs/v1.0.13/figs/graph_suite_v1013.png",
        "Claude/docs/v1.0.13/graph_suite_v1013.py",
        "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py",
    ),
    (
        "Claude/docs/v1.0.13/sample_test_v1013.png",
        "Claude/docs/v1.0.13/sample_test_v1013.py",
        "Claude/docs/v1.0.13/Anode_Fit_v1.0.13.py",
    ),
]

MANUAL_DISPOSITIONS = {
    "Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.pdf": {
        "disposition": "SOURCE_AFTER_ARTIFACT_COMMENT_ONLY_VISIBLE_CURRENT",
        "basis": (
            "The only later TeX change is a source comment lineage-name "
            "correction; full render review found no visible stale content."
        ),
    },
    "Claude/docs/v1.0.10/figs/P4_lco_heat_validation.png": {
        "disposition": "STALE_PROVENANCE_MATERIAL_SOURCE_UPDATES",
        "basis": (
            "The stored image predates the generator/model commits; the first "
            "later commit explicitly records the factor-2 entropy correction."
        ),
    },
    "Claude/docs/v1.0.10/figs/anode_fit_v1_0_10_dqdv.png": {
        "disposition": "STALE_PROVENANCE_MATERIAL_MODEL_UPDATES",
        "basis": (
            "The stored overview predates the final v1.0.10 model commit and "
            "was not regenerated after the model lineage changed."
        ),
    },
}


def run(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(arguments),
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=check,
        timeout=30,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def last_commit(path: str) -> dict:
    completed = run(
        "git",
        "log",
        "-1",
        "--format=%H%x09%aI%x09%s",
        "--",
        path,
    )
    commit, authored_at, subject = completed.stdout.rstrip("\n").split("\t", 2)
    return {
        "commit": commit,
        "authored_at": authored_at,
        "subject": subject,
    }


def is_ancestor(older: str, newer: str) -> bool:
    completed = run(
        "git",
        "merge-base",
        "--is-ancestor",
        older,
        newer,
        check=False,
    )
    if completed.returncode not in {0, 1}:
        raise RuntimeError(completed.stderr)
    return completed.returncode == 0


def relation(artifact_commit: str, source_commit: str) -> str:
    if artifact_commit == source_commit:
        return "SAME_COMMIT"
    if is_ancestor(source_commit, artifact_commit):
        return "ARTIFACT_AFTER_SOURCE"
    if is_ancestor(artifact_commit, source_commit):
        return "SOURCE_AFTER_ARTIFACT"
    return "DIVERGED_HISTORY"


def current_blob(path: str) -> str:
    return run("git", "rev-parse", f"HEAD:{path}").stdout.strip()


def regeneration_by_script() -> dict[str, dict]:
    data = json.loads(EXECUTION.read_text(encoding="utf-8"))
    records = {}
    for result in data["results"]:
        if not result["generated_files"]:
            continue
        # Every plotting script in this frozen suite produces one scientific
        # image; matplotlib cache files were excluded by the execution runner.
        records[result["script"]] = result["generated_files"][0]
    return records


def initial_disposition(relations: list[str]) -> str:
    if "DIVERGED_HISTORY" in relations:
        return "DIVERGED_REQUIRES_MANUAL_REVIEW"
    if "SOURCE_AFTER_ARTIFACT" in relations:
        return "SOURCE_AFTER_ARTIFACT_REQUIRES_MANUAL_REVIEW"
    return "ARTIFACT_AT_OR_AFTER_ALL_SOURCES"


def artifact_record(
    artifact_type: str,
    path: str,
    source_paths: list[tuple[str, str]],
    regenerated: dict | None = None,
) -> dict:
    artifact_commit = last_commit(path)
    sources = []
    relations = []
    for role, source_path in source_paths:
        source_commit = last_commit(source_path)
        source_relation = relation(
            artifact_commit["commit"], source_commit["commit"]
        )
        relations.append(source_relation)
        sources.append(
            {
                "role": role,
                "path": source_path,
                "current_blob": current_blob(source_path),
                "last_commit": source_commit,
                "relation_to_artifact_commit": source_relation,
            }
        )

    manual = MANUAL_DISPOSITIONS.get(path)
    disposition = (
        manual["disposition"] if manual else initial_disposition(relations)
    )
    record = {
        "artifact_type": artifact_type,
        "path": path,
        "sha256": sha256(ROOT / path),
        "current_blob": current_blob(path),
        "last_commit": artifact_commit,
        "sources": sources,
        "provenance_disposition": disposition,
        "manual_basis": manual["basis"] if manual else None,
    }
    if regenerated:
        record["isolated_regeneration"] = {
            "generated_path_literal": regenerated["path"],
            "sha256": regenerated["sha256"],
            "size_bytes": regenerated["size_bytes"],
            "stored_hash_bit_exact": regenerated["sha256"] == record["sha256"],
            "interpretation": (
                "BIT_EXACT_RENDER"
                if regenerated["sha256"] == record["sha256"]
                else "NON_BIT_EXACT_RENDER_ENVIRONMENT_OR_SOURCE_DIFFERENCE"
            ),
        }
    return record


def main() -> int:
    regenerated = regeneration_by_script()
    records = []
    for pdf, tex in PDFS:
        records.append(
            artifact_record("PDF", pdf, [("tex_source", tex)])
        )
    for image, generator, model in IMAGES:
        records.append(
            artifact_record(
                "PNG",
                image,
                [("generator", generator), ("model", model)],
                regenerated.get(generator),
            )
        )

    stale = [
        record["path"]
        for record in records
        if record["provenance_disposition"].startswith("STALE_PROVENANCE")
    ]
    regenerated_records = [
        record["isolated_regeneration"]
        for record in records
        if "isolated_regeneration" in record
    ]
    result = {
        "schema_version": "phase058-artifact-genealogy-v1",
        "baseline_commit": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
        "scope": {
            "pdfs": len(PDFS),
            "images": len(IMAGES),
            "artifacts": len(records),
        },
        "artifacts": records,
        "summary": {
            "stale_provenance_count": len(stale),
            "stale_provenance_paths": stale,
            "regenerated_image_count": len(regenerated_records),
            "regenerated_bit_exact_count": sum(
                item["stored_hash_bit_exact"] for item in regenerated_records
            ),
            "regenerated_non_bit_exact_count": sum(
                not item["stored_hash_bit_exact"] for item in regenerated_records
            ),
            "old_blob_body_availability": (
                "PARTIAL_CLONE_MISSING_SOME_HISTORICAL_BLOBS"
            ),
        },
        "interpretation_rules": [
            (
                "A source commit after an artifact commit makes the artifact "
                "provenance-stale unless manual review proves a render-inert change."
            ),
            (
                "A non-bit-exact matplotlib PNG regeneration is not by itself "
                "evidence of a scientific curve difference because fonts, backend, "
                "compression and metadata are environment-sensitive."
            ),
            (
                "An artifact at or after source commits establishes build ordering, "
                "not physical validity."
            ),
        ],
        "validation": {
            "artifact_count_matches_scope": len(records) == 16,
            "all_artifacts_exist": all((ROOT / record["path"]).is_file() for record in records),
            "all_sources_exist": all(
                (ROOT / source["path"]).is_file()
                for record in records
                for source in record["sources"]
            ),
            "all_artifacts_disposed": all(
                bool(record["provenance_disposition"]) for record in records
            ),
        },
    }
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(OUT.relative_to(ROOT)),
                "artifacts": len(records),
                "stale": len(stale),
                "regenerated_bit_exact": result["summary"][
                    "regenerated_bit_exact_count"
                ],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
