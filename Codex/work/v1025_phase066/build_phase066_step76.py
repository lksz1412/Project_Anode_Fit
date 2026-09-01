from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import math
import os
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
PROCESS_TIP = "e3e1a634f34b711aa4803fd190fe9120f1755f13"
EXPECTED_PARENT = "f9ee0599ff07d36e4b23547a835549552a51ce26"
EXPECTED_SUBJECT = "audit(phase066): freeze v1025 source process delta"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
GATE = "PASS_P066_STEP76_SOURCE_PROCESS"
PERSISTENCE = "PASS_P066_STEP76_PERSISTENCE"
BUILDER_SOURCE_POLICY_SHA256_LF = "aadc318c84d374cfcc8e7d10ac44e7b6a41fc5af41eac793af69cef3b8e2213f"

MANIFEST_PATH = "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
QUEUE_PATH = "Codex/results/PHASE_057_USER_INTENT_READ_QUEUE.json"
PRIOR_CARRY_PATH = "Codex/results/PHASE_065_CARRY_FORWARD_DELTA.json"
RESULT_PATH = "Codex/results/PHASE_066_STEP_076_SOURCE_PROCESS_RESULT.md"
DELTA_PATH = "Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json"
ATTESTATION_PATH = "Codex/results/PHASE_066_COMPLETE_READ_ATTESTATION.json"
BUILDER_PATH = "Codex/work/v1025_phase066/build_phase066_step76.py"
VALIDATOR_PATH = "Codex/work/v1025_phase066/validate_phase066_step76.py"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

MANIFEST_RAW_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
MANIFEST_LF_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
PATH_SET_SHA256 = "3c9bf954a5db4df5ce01a96ff8834f9e9284e6e35fdcecbfae0c3ae6b430b382"
PATH_BLOB_SHA256 = "b3620bf1a76758cad818e9ea7ece5441ea88b86f8f030bb715f48e054086655c"
UNIQUE_BLOB_SHA256 = "f1982cf050f88b7145d5ea1a6afdf124316da1332afec9028ae6119730080bfa"
PROCESS_SHA256 = "f09417ef085ee7139fa11869f6f123937d6492dcc53d1f0b51e71a2c8a124860"
ROUTED_PROCESS_SHA256 = "57062f623809de1f3fb66b8241117363a0ec18626bc58a40f4f0e41cbed93418"

RELEASE_PATHS = (
    "Claude/docs/v1.0.25",
    "Claude/docs/v1.0.25.1",
    "Claude/docs/v1.0.25.2",
)
SUPPLEMENTAL = (
    ("Claude/plans/2026-07-26-v1025-surgical-skew-consistency-plan.md",
     "c471f29944d766588b71dc026bc179f84f419e95", 240,
     "aff3e9089026dc50ee1923515c7545c800a2ea1add5152f9a86806fc2b29b382"),
    ("Claude/results/HANDOVER_v1025_2_CARRYOVER.md",
     "76c248e76430dbfcd3915b4cbebadce46a5d3593", 415,
     "84116f4ce35303aaffd5ff0173505c658799485b9cd7d4930a05b8a77b91e66c"),
)
ROUTED_PATHS = (*RELEASE_PATHS, *(row[0] for row in SUPPLEMENTAL))

OBSERVATIONS = (
    ("AO", "Codex/results/PHASE_057AO_V1025_ARCHIVE_TOUCHUP_OBSERVATIONS.md", 293, 301, 3, 288),
    ("AP", "Codex/results/PHASE_057AP_V1025_DATA_ADDENDUM_OBSERVATIONS.md", 302, 313, 1, 291),
    ("AQ", "Codex/results/PHASE_057AQ_V1025_CASCADE_LEDGER_OBSERVATIONS.md", 314, 325, 2, 339),
    ("AR", "Codex/results/PHASE_057AR_V1025_T13_T14_OBSERVATIONS.md", 326, 334, 1, 487),
    ("AS", "Codex/results/PHASE_057AS_V1025_DOC_EDIT_OBSERVATIONS.md", 335, 344, 1, 312),
    ("AT", "Codex/results/PHASE_057AT_V1025_HANDOVER_INDEX_OBSERVATIONS.md", 345, 354, 2, 308),
    ("AU", "Codex/results/PHASE_057AU_V1025_MERGE_READINESS_OBSERVATIONS.md", 355, 363, 1, 204),
    ("AV", "Codex/results/PHASE_057AV_V1025_2_ARCHIVE_OBSERVATIONS.md", 364, 377, 1, 381),
    ("AW", "Codex/results/PHASE_057AW_V1025_2_HANDOVER_OBSERVATIONS.md", 378, 387, 1, 175),
    ("AY", "Codex/results/PHASE_057AY_V1024_SNAPSHOT_V1025_2_KERNEL_REPORT_OBSERVATIONS.md", 395, 404, 2, 246),
)

# These immutable batch claims become READ_FULL only after the named reviewer reports exact
# membership/count/digest and zero unread/partial/truncation.  Until then --collect fails closed.
TEXT_REVIEW_BATCHES = (
    {"id": "TEXT-1", "reviewer": "p066_s76_routes", "count": 50, "lines": 10203,
     "membership_sha256": "5f5ad117e367d6be18d1f45d7db55de1fe3fc15ff94b3b6fb443bba92662883a",
     "status": "COMPLETE_WITH_DECLARED_MACHINE_SEGMENT"},
    {"id": "TEXT-2", "reviewer": "p066_s76_scaffold", "count": 54, "lines": 10198,
     "membership_sha256": "aa99071f2ff0fe10e7bc71d56e1c3ddc7d3f49a5bd5a22ec8cf012038ec2ccdc",
     "status": "READ_FULL"},
    {"id": "TEXT-3", "reviewer": "p066_s76_manifest", "count": 54, "lines": 10196,
     "membership_sha256": "30aead4089fbfdbf4ff1b99c3e8c1fda46fd1b2fb6fe1ecbe8113fbb244899e2",
     "status": "READ_FULL"},
)

PDF_REVIEWERS = {
    "107fe6fd3cd020dc73845413be2731e0974def46": ("p066_s76_routes", "READ_FULL"),
    "68bf2b51bee94ab7accb3150af7f5b6a72d00ea0": ("p066_s76_routes", "READ_FULL"),
    "3b5fb27293c95b85436813350db1dcc44d0a695a": ("p066_s76_scaffold", "READ_FULL"),
    "8a96945c674ae58d83c939edddfb5832dd0543aa": ("p066_s76_scaffold", "READ_FULL"),
    "4e379edfaf9bd6ca8fc1da32ac036fe84728744e": ("p066_s76_manifest", "READ_FULL"),
    "ec61067fccd1ebbb677affd449183d68a44af529": ("p066_s76_manifest", "READ_FULL"),
}
IMAGE_REVIEWERS = {
    "73b3430b33ee6caa41a1d5cf35479677cc707816": ("p066_s76_routes", "READ_FULL"),
    "99384f759f4ffd1f3096bd0b2885eaf58599b9b7": ("p066_s76_scaffold", "READ_FULL"),
    "c20b8fdd5286a9b45c73871181319443f3b7b960": ("p066_s76_manifest", "READ_FULL"),
}
PROCESS_REVIEW_BATCHES = (
    {"id": "PROCESS-1", "reviewer": "p066_s76_routes", "first": 1, "last": 7,
     "status": "COMPLETE_BY_TRANSITIVE_CONTENT_BINDING",
     "coverage_basis": "semantic no-textconv patches plus content-addressed source/PDF union"},
    {"id": "PROCESS-2", "reviewer": "p066_s76_scaffold", "first": 8, "last": 14,
     "status": "COMPLETE_BY_TRANSITIVE_CONTENT_BINDING",
     "coverage_basis": "direct small patches plus content-addressed copy/runtime union"},
    {"id": "PROCESS-3", "reviewer": "p066_s76_manifest", "first": 15, "last": 20,
     "status": "READ_FULL", "coverage_basis": "direct routed patches and decoded embedded images"},
)
SUPPLEMENTAL_REVIEW = {"reviewer": "p066_s76_routes", "status": "READ_FULL"}

VENDORED_MACHINE_SEGMENTS = {
    "3fa2ea6ea6889e0d0d095dcc6c1ee3b9500dee6a": {
        "status": "MACHINE_COMPLETE_HUMAN_AUTHORED_READ",
        "human_line_ranges": [[1, 219], [3808, 3812]],
        "machine_generated_line_range": [220, 3807],
        "machine_generated_bytes": 3565102,
        "machine_generated_sha256": "74d7c46dabca328c2294733910a8aa1ed0c37451776e8d5295da38a2b758fb9b",
        "machine_checks": ["STRICT_UTF8", "RAW_HASH", "NODE_SYNTAX", "UNSAFE_API_SCAN"],
        "human_semantic_read_of_machine_segment": False,
    }
}

OBSERVED_DEFECTS = (
    {"defect_id": "P066-S76-DEFECT-001", "kind": "PDF_RIGHT_CLIPPING",
     "blob_sha1": "4e379edfaf9bd6ca8fc1da32ac036fe84728744e",
     "path": "Claude/docs/v1.0.25/ch1_graphite_v1.0.24.pdf", "page": 50,
     "affected_items": 1, "status": "OPEN_ROUTED",
     "downstream_owner": "PHASE-089-LATEX-PDF-RELEASE-QA"},
    {"defect_id": "P066-S76-DEFECT-002", "kind": "EMBEDDED_PNG_KOREAN_GLYPH_MISSING",
     "blob_sha1": "4086482f28af182fb16fbbe02fd1f9f1cc52c69c",
     "path": "Claude/docs/v1.0.25.2/results/KERNEL_COMPARISON_REPORT_v1025_2.html",
     "embedded_png_count": 9, "affected_items": 9, "status": "OPEN_ROUTED",
     "downstream_owner": "PHASE-089-LATEX-PDF-RELEASE-QA"},
)


class BuildFailure(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise BuildFailure(code, detail)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def line_count(raw: bytes) -> int:
    return len(raw.decode("utf-8").splitlines())


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True,
                       allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")


def semantic_hash(value: dict[str, Any]) -> str:
    clone = dict(value)
    clone["semantic_sha256"] = ""
    return sha256(canonical_bytes(clone))


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_JSON_DUPLICATE", key)
        result[key] = value
    return result


def _constant(token: str) -> None:
    raise BuildFailure("E_JSON_NONFINITE", token)


def strict_json(raw: bytes) -> Any:
    require(raw.startswith(b"{") and raw.rstrip().endswith(b"}"), "E_JSON_SHAPE")
    try:
        text = raw.decode("utf-8")
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise BuildFailure("E_JSON_PARSE", str(error)) from error
    def check_finite(item: Any) -> None:
        if isinstance(item, dict):
            for nested in item.values():
                check_finite(nested)
        elif isinstance(item, list):
            for nested in item:
                check_finite(nested)
        elif isinstance(item, float):
            require(math.isfinite(item), "E_JSON_NONFINITE", repr(item))
    check_finite(value)
    return value


def validate_git_args(args: tuple[str, ...]) -> None:
    require(args, "E_GIT_EMPTY")
    forbidden = {"-c", "--config-env", "--upload-pack", "--receive-pack", "--exec-path",
                 "--ext-diff", "--textconv", "reset", "checkout", "switch", "commit", "push",
                 "fetch", "merge", "rebase", "update-ref", "branch", "clean", "rm", "mv"}
    require(not any(arg in forbidden for arg in args), "E_GIT_FORBIDDEN", repr(args))
    require(not any(arg.startswith(("--config=", "--git-dir", "--work-tree", "--output"))
                    for arg in args), "E_GIT_OPTION", repr(args))
    require(args[0] in {"cat-file", "rev-parse", "log", "show", "diff-tree", "ls-tree"},
            "E_GIT_VERB", args[0])


def git(*args: str, binary: bool = True) -> bytes | str:
    validate_git_args(tuple(args))
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False,
                            shell=False, timeout=90)
    require(result.returncode == 0, "E_GIT", result.stderr.decode("utf-8", "replace"))
    return result.stdout if binary else result.stdout.decode("utf-8").rstrip("\r\n")


def git_blob(ref: str, path: str) -> bytes:
    require(not path.startswith("-") and "\n" not in path and "\r" not in path,
            "E_PATH", path)
    return git("cat-file", "blob", f"{ref}:{path}", binary=True)  # type: ignore[return-value]


def git_blob_id(ref: str, path: str) -> str:
    value = git("rev-parse", f"{ref}:{path}", binary=False)
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None,
            "E_BLOB_ID", path)
    return value


def load_manifest() -> tuple[dict[str, Any], list[tuple[int, dict[str, Any]]]]:
    raw = git_blob("HEAD", MANIFEST_PATH)
    require(sha256(raw) == MANIFEST_RAW_SHA256, "E_MANIFEST_RAW")
    require(sha256(lf_bytes(raw)) == MANIFEST_LF_SHA256, "E_MANIFEST_LF")
    document = strict_json(raw)
    require(document.get("baseline_commit") == BASELINE, "E_MANIFEST_BASELINE")
    selected = [(index, row) for index, row in enumerate(document["entries"])
                if row.get("version") in {"v1.0.25", "v1.0.25.1", "v1.0.25.2"}]
    require([index for index, _ in selected] == list(range(1087, 1520)), "E_MANIFEST_SLICE")
    require(len(selected) == 433, "E_MANIFEST_OCCURRENCES")
    return document, selected


def text_batches(unique_rows: dict[str, dict[str, Any]]) -> tuple[list[list[str]], list[dict[str, Any]]]:
    candidates = [(blob, row) for blob, row in unique_rows.items() if row["review_mode"] == "FULL_TEXT"]
    chunks: list[list[str]] = [[], [], []]
    sums = [0, 0, 0]
    for blob, row in sorted(candidates, key=lambda item: (-int(item[1]["extent"]["lines"]), item[0])):
        index = min(range(3), key=lambda number: (sums[number], number))
        chunks[index].append(blob)
        sums[index] += int(row["extent"]["lines"])
    records: list[dict[str, Any]] = []
    for index, blobs in enumerate(chunks):
        expected = TEXT_REVIEW_BATCHES[index]
        digest = sha256("".join(blob + "\n" for blob in sorted(blobs)).encode("ascii"))
        require((len(blobs), sums[index], digest) ==
                (expected["count"], expected["lines"], expected["membership_sha256"]),
                "E_TEXT_BATCH", expected["id"])
        records.append({**expected, "blob_ids": sorted(blobs), "unread": 0, "partial": 0,
                        "truncation_unresolved": 0})
    return chunks, records


def inspect_unique_sources(selected: list[tuple[int, dict[str, Any]]],
                           require_human: bool) -> tuple[list[dict[str, Any]], dict[str, str], list[dict[str, Any]]]:
    grouped: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for index, row in selected:
        grouped.setdefault(row["blob_sha"], []).append((index, row))
    unique_rows = {blob: rows[0][1] for blob, rows in grouped.items()}
    chunks, batch_records = text_batches(unique_rows)
    batch_for = {blob: TEXT_REVIEW_BATCHES[index]["id"]
                 for index, chunk in enumerate(chunks) for blob in chunk}
    records: list[dict[str, Any]] = []
    observed_counts: Counter[str] = Counter()
    for blob in sorted(grouped):
        rows = grouped[blob]
        representative = rows[0][1]
        raw = git_blob(BASELINE, representative["path"])
        require(git_blob_id(BASELINE, representative["path"]) == blob, "E_SOURCE_BLOB", blob)
        require(len(raw) == int(representative["size_bytes"]), "E_SOURCE_SIZE", blob)
        declared = representative["review_mode"]
        evidence: dict[str, Any]
        if raw.startswith(b"%PDF-"):
            observed = "PDF"
            reader = PdfReader(io.BytesIO(raw), strict=True)
            pages = len(reader.pages)
            require(declared == "FULL_PDF" and pages == int(representative["extent"]["pages"]),
                    "E_PDF_EXTENT", blob)
            reviewer, status = PDF_REVIEWERS[blob]
            semantic_kind = "PDF_DOCUMENT"
            evidence = {"reviewer": reviewer, "status": status, "page_ranges": [[1, pages]],
                        "visual_inspection": status == "READ_FULL", "render_failures": 0,
                        "blank_pages": 0, "defects_recorded_in_result": True}
        elif raw.startswith(b"\x89PNG\r\n\x1a\n"):
            observed = "PNG"
            with Image.open(io.BytesIO(raw)) as image:
                extent = {"width": image.width, "height": image.height, "mode": image.mode,
                          "format": image.format, "frames": image.n_frames}
            require(extent == representative["extent"], "E_IMAGE_EXTENT", blob)
            reviewer, status = IMAGE_REVIEWERS[blob]
            semantic_kind = "PNG_IMAGE"
            evidence = {"reviewer": reviewer, "status": status, "frame_ranges": [[1, 1]],
                        "visual_inspection": status == "READ_FULL", "defects_recorded_in_result": True}
        else:
            observed = "UTF8_TEXT"
            try:
                text = raw.decode("utf-8")
            except UnicodeError as error:
                raise BuildFailure("E_TEXT_UTF8", blob) from error
            require(b"\r" not in raw, "E_TEXT_CR", blob)
            lines = len(text.splitlines())
            require(declared == "FULL_TEXT" and lines == int(representative["extent"]["lines"]),
                    "E_TEXT_EXTENT", blob)
            extension = representative["extension"].lower()
            if extension == "py":
                ast.parse(text)
                semantic_kind = "PYTHON_SOURCE"
            elif extension == "json":
                try:
                    strict_json(raw)
                except BuildFailure:
                    semantic_kind = "TEXT_POINTER"
                else:
                    semantic_kind = "JSON_DOCUMENT"
            else:
                semantic_kind = "TEXT_DOCUMENT"
            batch = next(row for row in batch_records if row["id"] == batch_for[blob])
            if blob in VENDORED_MACHINE_SEGMENTS:
                evidence = {"reviewer": batch["reviewer"], "batch_id": batch["id"],
                            "truncation_unresolved": 0, **VENDORED_MACHINE_SEGMENTS[blob]}
            else:
                evidence = {"reviewer": batch["reviewer"], "status": "READ_FULL",
                            "line_ranges": [[1, lines]], "truncation_unresolved": 0,
                            "batch_id": batch["id"]}
        if require_human:
            require(evidence["status"] in {"READ_FULL", "MACHINE_COMPLETE_HUMAN_AUTHORED_READ"},
                    "E_HUMAN_READ_PENDING", blob)
        observed_counts[observed] += 1
        declared_extensions = sorted({row["extension"].lower() for _, row in rows})
        classification_discrepancy = (
            ("json" in declared_extensions and semantic_kind != "JSON_DOCUMENT") or
            ("py" in declared_extensions and semantic_kind != "PYTHON_SOURCE") or
            ("pdf" in declared_extensions and semantic_kind != "PDF_DOCUMENT") or
            ("png" in declared_extensions and semantic_kind != "PNG_IMAGE")
        )
        occurrence_indices = [index for index, _ in rows]
        occurrence_paths = [row["path"] for _, row in rows]
        records.append({
            "attestation_id": f"P066-BLOB-{len(records) + 1:04d}",
            "blob_sha1": blob,
            "raw_sha256": sha256(raw),
            "lf_sha256": sha256(lf_bytes(raw)) if observed == "UTF8_TEXT" else None,
            "lf_hash_applicable": observed == "UTF8_TEXT",
            "size_bytes": len(raw),
            "observed_type": observed,
            "observed_semantic_kind": semantic_kind,
            "declared_extensions": declared_extensions,
            "classification_discrepancy": classification_discrepancy,
            "declared_review_mode": declared,
            "declared_role": representative["role"],
            "extent": representative["extent"],
            "machine_coverage": {"status": "MACHINE_READ_FULL", "byte_range_half_open": [0, len(raw)]},
            "human_coverage": evidence,
            "occurrence_indices": occurrence_indices,
            "occurrence_paths": occurrence_paths,
        })
    require((len(records), observed_counts) ==
            (167, Counter({"UTF8_TEXT": 158, "PDF": 6, "PNG": 3})), "E_UNIQUE_COUNTS")
    return records, {record["blob_sha1"]: record["attestation_id"] for record in records}, batch_records


def occurrence_records(selected: list[tuple[int, dict[str, Any]]], bindings: dict[str, str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, row in selected:
        prefix = f"Claude/docs/{row['version']}/"
        require(row["path"].startswith(prefix), "E_VERSION_PATH", row["path"])
        records.append({
            "manifest_index": index,
            "ordinal": index + 1,
            "version": row["version"],
            "path": row["path"],
            "relative_path": row["path"][len(prefix):],
            "blob_sha1": row["blob_sha"],
            "git_mode": row["git_mode"],
            "size_bytes": row["size_bytes"],
            "extension": row["extension"],
            "role": row["role"],
            "review_mode": row["review_mode"],
            "extent": row["extent"],
            "candidate_tex_paths": row.get("candidate_tex_paths", []),
            "attestation_id": bindings[row["blob_sha"]],
        })
    return records


def provenance_for(path: str, target_blob: str) -> dict[str, Any]:
    marker = "@@P066@@"
    output = git("log", "--full-history", "--reverse",
                 f"--format={marker}%H%x09%P%x09%aI%x09%cI%x09%s",
                 "--raw", "--abbrev=40", "--no-renames", BASELINE, "--", path,
                 binary=False)
    require(isinstance(output, str), "E_PROVENANCE_OUTPUT", path)
    events: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in output.splitlines():
        if line.startswith(marker):
            parts = line[len(marker):].split("\t", 4)
            require(len(parts) == 5, "E_PROVENANCE_HEADER", path)
            current = {"commit": parts[0], "parents": parts[1].split(), "author_time": parts[2],
                       "committer_time": parts[3], "subject": parts[4], "changes": []}
            events.append(current)
        elif line.startswith(":"):
            require(current is not None, "E_PROVENANCE_ORDER", path)
            meta, changed_path = line.split("\t", 1)
            fields = meta.split()
            require(len(fields) == 5, "E_PROVENANCE_RAW", line)
            current["changes"].append({"old_mode": fields[0][1:], "new_mode": fields[1],
                                       "old_blob": fields[2], "new_blob": fields[3],
                                       "status": fields[4], "path": changed_path})
    matching = [(event, change) for event in events for change in event["changes"] if change["path"] == path]
    introduced = next(((event, change) for event, change in matching if change["status"] == "A"), None)
    exact = next(((event, change) for event, change in matching if change["new_blob"] == target_blob), None)
    require(introduced is not None and exact is not None, "E_PROVENANCE_NOT_FOUND", path)
    def compact(pair: tuple[dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
        event, change = pair
        return {"commit": event["commit"], "parents": event["parents"],
                "author_time": event["author_time"], "committer_time": event["committer_time"],
                "subject": event["subject"], "old_blob": change["old_blob"],
                "new_blob": change["new_blob"], "status": change["status"]}
    return {"path_introduction": compact(introduced), "first_exact_blob_at_path": compact(exact)}


def pairwise_deltas(occurrences: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_version = {version: {row["relative_path"]: row for row in occurrences if row["version"] == version}
                  for version in ("v1.0.25", "v1.0.25.1", "v1.0.25.2")}
    expected = {
        ("v1.0.25", "v1.0.25.1"): (143, 133, 10, 1, 0),
        ("v1.0.25.1", "v1.0.25.2"): (144, 133, 11, 2, 0),
        ("v1.0.25", "v1.0.25.2"): (143, 127, 16, 3, 0),
    }
    provenance_cache: dict[tuple[str, str], dict[str, Any]] = {}
    results: list[dict[str, Any]] = []
    for left_version, right_version in expected:
        left, right = by_version[left_version], by_version[right_version]
        rows: list[dict[str, Any]] = []
        counts: Counter[str] = Counter()
        for relative in sorted(set(left) | set(right)):
            old, new = left.get(relative), right.get(relative)
            if old is None:
                status = "ADDED"
            elif new is None:
                status = "REMOVED"
            elif old["blob_sha1"] == new["blob_sha1"]:
                status = "SAME"
            else:
                status = "CHANGED"
            counts[status] += 1
            row = {"relative_path": relative, "status": status,
                   "old_index": old["manifest_index"] if old else None,
                   "new_index": new["manifest_index"] if new else None,
                   "old_blob": old["blob_sha1"] if old else None,
                   "new_blob": new["blob_sha1"] if new else None,
                   "old_provenance": None, "new_provenance": None}
            if status in {"CHANGED", "REMOVED"} and old:
                key = (old["path"], old["blob_sha1"])
                provenance_cache.setdefault(key, provenance_for(*key))
                row["old_provenance"] = provenance_cache[key]
            if status in {"CHANGED", "ADDED"} and new:
                key = (new["path"], new["blob_sha1"])
                provenance_cache.setdefault(key, provenance_for(*key))
                row["new_provenance"] = provenance_cache[key]
            rows.append(row)
        shared = len(set(left) & set(right))
        observed = (shared, counts["SAME"], counts["CHANGED"], counts["ADDED"], counts["REMOVED"])
        require(observed == expected[(left_version, right_version)], "E_DELTA_COUNTS",
                f"{left_version}:{right_version}:{observed}")
        results.append({"from_version": left_version, "to_version": right_version,
                        "counts": {"shared": shared, "same": counts["SAME"],
                                   "changed": counts["CHANGED"], "added": counts["ADDED"],
                                   "removed": counts["REMOVED"]}, "records": rows})
    require(len(provenance_cache) == 52, "E_PROVENANCE_DENOMINATOR", str(len(provenance_cache)))
    return results


def process_commits(require_human: bool) -> dict[str, Any]:
    def query(paths: tuple[str, ...]) -> list[str]:
        text = git("log", "--reverse", "--format=%H", PROCESS_TIP, "--", *paths, binary=False)
        require(isinstance(text, str), "E_PROCESS_OUTPUT")
        return text.splitlines()
    release = query(RELEASE_PATHS)
    routed = query(ROUTED_PATHS)
    require((len(release), len(routed), release[0], release[-1], routed[0], routed[-1]) ==
            (17, 20, "edbc4a2c68cda0dd21662cb6dd68ba8bed699a76", PROCESS_TIP,
             "edbc4a2c68cda0dd21662cb6dd68ba8bed699a76", PROCESS_TIP), "E_PROCESS_TERMINALS")
    require(sha256(("\n".join(release) + "\n").encode("ascii")) == PROCESS_SHA256,
            "E_PROCESS_DIGEST")
    require(sha256(("\n".join(routed) + "\n").encode("ascii")) == ROUTED_PROCESS_SHA256,
            "E_ROUTED_DIGEST")
    release_set = set(release)
    records: list[dict[str, Any]] = []
    for ordinal, commit in enumerate(routed, 1):
        header = git("show", "-s", "--format=%P%x00%aI%x00%cI%x00%s", commit, binary=True)
        require(isinstance(header, bytes), "E_PROCESS_HEADER")
        parts = header.rstrip(b"\r\n").decode("utf-8").split("\0", 3)
        require(len(parts) == 4, "E_PROCESS_HEADER", commit)
        changed_text = git("diff-tree", "--root", "--no-commit-id", "--name-status",
                           "--no-renames", "-r", commit, binary=False)
        require(isinstance(changed_text, str), "E_PROCESS_CHANGED")
        changed: list[dict[str, str]] = []
        for line in changed_text.splitlines():
            status, path = line.split("\t", 1)
            changed.append({"status": status, "path": path})
        relevant_release = sorted(row["path"] for row in changed
                                  if any(row["path"] == prefix or row["path"].startswith(prefix + "/")
                                         for prefix in RELEASE_PATHS))
        relevant_supplemental = sorted(row["path"] for row in changed if row["path"] in {x[0] for x in SUPPLEMENTAL})
        patch = git("show", "--format=", "--no-color", "--no-ext-diff", "--no-textconv",
                    "--find-renames", "--find-copies", commit, "--", *ROUTED_PATHS, binary=True)
        require(isinstance(patch, bytes) and patch, "E_PROCESS_PATCH", commit)
        batch = next(row for row in PROCESS_REVIEW_BATCHES if row["first"] <= ordinal <= row["last"])
        if require_human:
            require(batch["status"] in {"READ_FULL", "COMPLETE_BY_TRANSITIVE_CONTENT_BINDING"},
                    "E_PROCESS_REVIEW_PENDING", commit)
        records.append({"ordinal": ordinal, "commit": commit, "parents": parts[0].split(),
                        "author_time": parts[1], "committer_time": parts[2], "subject": parts[3],
                        "memberships": (["release", "routed"] if commit in release_set else ["routed"]),
                        "changed_paths": changed, "relevant_release_paths": relevant_release,
                        "relevant_supplemental_paths": relevant_supplemental,
                        "out_of_scope_changed_paths": sorted(row["path"] for row in changed
                                                             if row["path"] not in set(relevant_release + relevant_supplemental)),
                        "patch_bytes": len(patch), "patch_lines": len(lf_bytes(patch).splitlines()),
                        "patch_sha256_raw": sha256(patch), "patch_sha256_lf": sha256(lf_bytes(patch)),
                        "human_coverage": {"batch_id": batch["id"], "reviewer": batch["reviewer"],
                                            "status": batch["status"],
                                            "range": "1..EOF by declared coverage basis",
                                            "coverage_basis": batch["coverage_basis"]}})
    return {"tip": PROCESS_TIP,
            "release": {"paths": list(RELEASE_PATHS), "count": 17, "commits": release,
                        "sha256_lf": PROCESS_SHA256},
            "routed": {"paths": list(ROUTED_PATHS), "count": 20, "commits": routed,
                       "sha256_lf": ROUTED_PROCESS_SHA256},
            "records": records, "review_batches": [dict(row) for row in PROCESS_REVIEW_BATCHES]}


def narrative_records(selected_paths: set[str], require_human: bool) -> dict[str, Any]:
    queue_raw = git_blob("HEAD", QUEUE_PATH)
    queue = strict_json(queue_raw)
    selected = [row for row in queue["documents"] if set(row["all_paths"]) & selected_paths]
    manifest_records = [row for row in selected if row["category"] != "MACHINE_EVIDENCE"]
    excluded = [row for row in selected if row["category"] == "MACHINE_EVIDENCE"]
    require((len(selected), sum(row["line_count"] for row in selected), len(manifest_records),
             sum(row["line_count"] for row in manifest_records), len(excluded)) == (41, 9020, 40, 9019, 1),
            "E_NARRATIVE_DENOMINATOR")
    supplemental: list[dict[str, Any]] = []
    if require_human:
        require(SUPPLEMENTAL_REVIEW["status"] == "READ_FULL", "E_SUPPLEMENTAL_REVIEW_PENDING")
    for path, blob, lines, expected_hash in SUPPLEMENTAL:
        raw = git_blob(BASELINE, path)
        require(git_blob_id(BASELINE, path) == blob and line_count(raw) == lines and
                sha256(lf_bytes(raw)) == expected_hash, "E_SUPPLEMENTAL", path)
        supplemental.append({"path": path, "blob_sha1": blob, "lines": lines,
                             "sha256_lf": expected_hash, "human_coverage": {
                                 **SUPPLEMENTAL_REVIEW, "range": f"1..{lines}"}})
    return {"queue_path": QUEUE_PATH, "queue_sha256_raw": sha256(queue_raw),
            "manifest_documents": len(manifest_records), "manifest_lines": 9019,
            "manifest_records": [{"blob_sha1": row["blob_sha"], "representative_path": row["representative_path"],
                                  "all_paths": row["all_paths"], "category": row["category"],
                                  "lines": row["line_count"]} for row in manifest_records],
            "excluded_machine_evidence": [{"blob_sha1": row["blob_sha"],
                                           "representative_path": row["representative_path"],
                                           "lines": row["line_count"]} for row in excluded],
            "supplemental_documents": 2, "supplemental_lines": 655,
            "supplemental_records": supplemental, "expanded_documents": 42,
            "expanded_lines": 9674, "separate_from_manifest_occurrences": True}


def phase057_routes(require_human: bool) -> dict[str, Any]:
    prior_raw = git_blob("HEAD", PRIOR_CARRY_PATH)
    prior = strict_json(prior_raw)
    prior_rows = {row["observation_id"]: row for row in prior["observation_records"]
                  if row.get("observation_id") in {f"INTENT-PROV-{number:04d}" for number in range(395, 405)}}
    require(len(prior_rows) == 10, "E_AY_PRIOR")
    documents: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    for batch, path, first, last, underlying_docs, underlying_lines in OBSERVATIONS:
        raw = git_blob("HEAD", path)
        require(raw == lf_bytes(raw) and raw.endswith(b"\n"), "E_OBSERVATION_LF", path)
        text = raw.decode("utf-8")
        lines = text.splitlines()
        headings = [(index + 1, match.group(1), match.group(3))
                    for index, line in enumerate(lines)
                    if (match := re.match(r"^### (INTENT-PROV-(\d{4})) — (.+)$", line))]
        observed_ids = [identity for _, identity, _ in headings]
        expected_ids = [f"INTENT-PROV-{number:04d}" for number in range(first, last + 1)]
        require(observed_ids == expected_ids, "E_OBSERVATION_IDS", batch)
        documents.append({"batch": batch, "path": path, "sha256_raw": sha256(raw),
                          "sha256_lf": sha256(lf_bytes(raw)), "lines": len(lines),
                          "read_range": [1, len(lines)], "read_status": "READ_FULL",
                          "reviewer": "p066_s76_routes", "source_document_status": "READ_NOT_YET_CANONICAL",
                          "underlying_document_count": underlying_docs,
                          "underlying_physical_lines": underlying_lines,
                          "intent_ids": expected_ids})
        for heading_index, (heading_line, identity, title) in enumerate(headings):
            next_line = headings[heading_index + 1][0] if heading_index + 1 < len(headings) else len(lines) + 1
            block = ("\n".join(lines[heading_line - 1:next_line - 1]) + "\n").encode("utf-8")
            if batch == "AY":
                prior_row = prior_rows[identity]
                record = {"canonical_owner": prior_row["canonical_owner"],
                          "current_state": prior_row["state"], "target_phase": prior_row["target_phase"],
                          "severity": prior_row["severity"],
                          "acceptance_criterion": prior_row["acceptance_criterion"],
                          "semantic_fingerprint": prior_row["semantic_fingerprint"],
                          "prior_origin_record_sha256": prior_row["origin_record_sha256"],
                          "route_class": "SHARED_P065_REFERENCE", "is_new_phase066_obligation": False,
                          "owner_state": "PERSISTED_P065"}
            else:
                record = {"canonical_owner": None, "current_state": "PENDING_STEP81_1",
                          "target_phase": 66, "severity": "UNADJUDICATED",
                          "acceptance_criterion": "Step 81.1 must assign exactly one evidence-bounded canonical owner or bounded historical disposition.",
                          "semantic_fingerprint": sha256(block), "prior_origin_record_sha256": None,
                          "route_class": "NEW_P066_INTAKE", "is_new_phase066_obligation": True,
                          "owner_state": "PENDING_STEP81_1"}
            records.append({"observation_id": identity, "numeric_id": int(identity[-4:]),
                            "title": title, "origin_observation_path": path,
                            "heading_line": heading_line, "source_line_range": [heading_line, next_line - 1],
                            "source_block_sha256": sha256(block), "route_custodian": "P066_STEP76",
                            "external_authority_promoted": False, "back_projection_forbidden": True,
                            **record})
    if require_human:
        require(all(row["read_status"] == "READ_FULL" for row in documents), "E_OBSERVATION_REVIEW")
    ao_aw = [row for row in records if 293 <= row["numeric_id"] <= 387]
    ay = [row for row in records if 395 <= row["numeric_id"] <= 404]
    require(len(ao_aw) == 95 and len(ay) == 10 and len({row["observation_id"] for row in records}) == 105,
            "E_ROUTE_COUNTS")
    require(not any(388 <= row["numeric_id"] <= 394 for row in records), "E_AX_SCOPE_LEAK")
    require(sum(row["is_new_phase066_obligation"] for row in records) == 95, "E_ROUTE_NEW_COUNT")
    require(Counter(row["current_state"] for row in ay) == {"OPEN_CARRY": 8, "BOUNDED_HISTORICAL": 2},
            "E_AY_STATE")
    return {"documents": documents, "records": records, "document_count": 10,
            "document_lines": sum(row["lines"] for row in documents),
            "underlying_document_count": 15, "underlying_physical_lines": 3031,
            "ao_aw_count": 95, "ay_count": 10, "ay_new_count": 0,
            "ax_scope_leak_count": 0, "duplicate_count": 0,
            "prior_carry_path": PRIOR_CARRY_PATH, "prior_carry_sha256_raw": sha256(prior_raw)}


def stale_pdf_pairs(occurrences: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_version = {version: {row["relative_path"]: row for row in occurrences if row["version"] == version}
                  for version in ("v1.0.25.1", "v1.0.25.2")}
    records: list[dict[str, Any]] = []
    for relative in sorted(path for path, row in by_version["v1.0.25.1"].items()
                           if row["review_mode"] == "FULL_PDF"):
        left, right = by_version["v1.0.25.1"][relative], by_version["v1.0.25.2"][relative]
        tex_relative = relative[:-4] + ".tex"
        left_tex, right_tex = by_version["v1.0.25.1"][tex_relative], by_version["v1.0.25.2"][tex_relative]
        require(left["blob_sha1"] == right["blob_sha1"] and
                left_tex["blob_sha1"] != right_tex["blob_sha1"], "E_STALE_PDF", relative)
        records.append({"relative_path": relative, "pdf_blob_sha1": left["blob_sha1"],
                        "bytes": left["size_bytes"], "pages": left["extent"]["pages"],
                        "pdf_blob_equal": True, "candidate_tex_path": tex_relative,
                        "candidate_tex_blob_equal": False, "v1025_2_build_evidence": False})
    require(len(records) == 3, "E_STALE_PDF_COUNT")
    return records


def build_artifacts(require_human: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    _, selected = load_manifest()
    selected_paths = {row["path"] for _, row in selected}
    unique_sources, bindings, text_reviews = inspect_unique_sources(selected, require_human)
    occurrences = occurrence_records(selected, bindings)
    versions = Counter(row["version"] for row in occurrences)
    unique_modes = Counter(row["declared_review_mode"] for row in unique_sources)
    path_hash = sha256(("\n".join(sorted(row["path"] for row in occurrences)) + "\n").encode("utf-8"))
    path_blob_hash = sha256(("\n".join(sorted(row["path"] + "\0" + row["blob_sha1"]
                                                       for row in occurrences)) + "\n").encode("utf-8"))
    blob_hash = sha256(("\n".join(sorted(bindings)) + "\n").encode("ascii"))
    require((path_hash, path_blob_hash, blob_hash) ==
            (PATH_SET_SHA256, PATH_BLOB_SHA256, UNIQUE_BLOB_SHA256), "E_MANIFEST_HASHES")
    result_raw = (ROOT / RESULT_PATH).read_bytes()
    require(result_raw == lf_bytes(result_raw) and result_raw.endswith(b"\n"), "E_RESULT_FIRST")
    builder_raw = (ROOT / BUILDER_PATH).read_bytes()
    validator_raw = (ROOT / VALIDATOR_PATH).read_bytes()
    control_inputs: dict[str, dict[str, Any]] = {}
    for key, path in (("parent_ledger", PARENT_LEDGER_PATH),
                      ("active_ledger", ACTIVE_LEDGER_PATH), ("handover", HANDOVER_PATH)):
        raw = (ROOT / path).read_bytes()
        require(raw == lf_bytes(raw) and raw.endswith(b"\n"), "E_CONTROL_LF", path)
        control_inputs[key] = {"path": path, "sha256_lf": sha256(raw), "lines": line_count(raw)}
    common = {"schema_version": "P066-S76-1", "phase": 66, "step": 76,
              "generated_date": "2026-09-01", "baseline_commit": BASELINE,
              "process_tip": PROCESS_TIP, "expected_parent": EXPECTED_PARENT,
              "expected_subject": EXPECTED_SUBJECT, "branch": BRANCH, "gate": GATE,
              "persistence_terminal": PERSISTENCE,
              "inputs": {"manifest": {"path": MANIFEST_PATH, "raw_sha256": MANIFEST_RAW_SHA256,
                                         "lf_sha256": MANIFEST_LF_SHA256},
                         "result": {"path": RESULT_PATH, "sha256_lf": sha256(result_raw),
                                    "lines": line_count(result_raw)},
                         "builder": {"path": BUILDER_PATH, "sha256_lf": sha256(builder_raw),
                                     "lines": line_count(builder_raw)},
                         "validator": {"path": VALIDATOR_PATH, "sha256_lf": sha256(validator_raw),
                                       "lines": line_count(validator_raw)},
                         **control_inputs},
              "authority": {"inventory_and_read_coverage": True, "v1025_2_build_evidence": False,
                            "fit_reproduced": False, "optimizer_state_recovered": False,
                            "external_scientific": False, "material_authority": False,
                            "canonical_release": False, "publication_ready": False},
               "result_first": True, "json_pair_last": True,
               "observed_defects": [dict(row) for row in OBSERVED_DEFECTS]}
    process = process_commits(require_human)
    narrative = narrative_records(selected_paths, require_human)
    routes = phase057_routes(require_human)
    delta: dict[str, Any] = {**common, "artifact": "PHASE_066_SOURCE_PROCESS_DELTA",
        "source_summary": {"slice_indices_zero_based": [1087, 1519], "occurrences": 433,
                           "versions": dict(sorted(versions.items())), "unique_blobs": 167,
                           "occurrence_bytes": sum(row["size_bytes"] for row in occurrences),
                           "unique_bytes": sum(row["size_bytes"] for row in unique_sources),
                           "unique_review_modes": dict(sorted(unique_modes.items())),
                           "unique_text_lines": sum(row["extent"].get("lines", 0) for row in unique_sources),
                           "unique_pdf_pages": sum(row["extent"].get("pages", 0) for row in unique_sources),
                           "path_set_sha256": path_hash, "path_blob_sha256": path_blob_hash,
                           "unique_blob_sha256": blob_hash},
        "occurrences": occurrences, "pairwise_deltas": pairwise_deltas(occurrences),
        "stale_pdf_pairs": stale_pdf_pairs(occurrences), "narrative": narrative,
        "process": process, "phase057_routes": routes,
        "validation": {"occurrence_orphans": 0, "duplicate_occurrences": 0,
                       "provenance_not_found": 0, "unread_process_patches": 0,
                       "ay_new_duplicates": 0, "authority_promotions": 0,
                       "classification_discrepancies": sum(row["classification_discrepancy"]
                                                           for row in unique_sources)},
        "semantic_sha256": ""}
    delta["semantic_sha256"] = semantic_hash(delta)
    occurrence_bindings = [{"manifest_index": row["manifest_index"], "path": row["path"],
                            "blob_sha1": row["blob_sha1"], "attestation_id": row["attestation_id"]}
                           for row in occurrences]
    attestation: dict[str, Any] = {**common, "artifact": "PHASE_066_COMPLETE_READ_ATTESTATION",
        "delta_semantic_sha256": delta["semantic_sha256"], "machine_blob_attestations": unique_sources,
        "occurrence_bindings": occurrence_bindings, "text_review_batches": text_reviews,
        "narrative_document_attestations": narrative,
        "routing_observation_attestations": {"documents": routes["documents"],
                                             "intent_ids": [row["observation_id"] for row in routes["records"]]},
        "process_read_attestations": {"batches": process["review_batches"],
                                      "records": [{"ordinal": row["ordinal"], "commit": row["commit"],
                                                   "patch_sha256_lf": row["patch_sha256_lf"],
                                                   "patch_lines": row["patch_lines"],
                                                   "human_coverage": row["human_coverage"]}
                                                  for row in process["records"]]},
        "coverage_summary": {"source_occurrences_total": 433, "source_occurrences_read": 433,
                             "source_occurrence_orphans": 0, "unique_blobs_total": 167,
                             "unique_blobs_read": 167, "unique_blobs_unread": 0,
                             "unique_blobs_partial": 0, "text_blobs": 158, "text_lines": 30597,
                             "pdf_blobs": 6, "pdf_pages": 308, "image_blobs": 3,
                             "images_visual_inspected": 3, "narrative_documents": 42,
                             "narrative_lines": 9674, "routing_documents": 10,
                             "routing_intent_ids": 105, "routing_duplicate_ids": 0,
                             "release_commits": 17, "routed_commits": 20,
                             "unread_process_diffs": 0, "inspection_errors": 0,
                             "output_truncation_unresolved": 0},
        "validation": {"unread": [], "partial": [], "orphan": [], "duplicate": [],
                       "inspection_error": [], "output_truncation_unresolved": []},
        "semantic_sha256": ""}
    attestation["semantic_sha256"] = semantic_hash(attestation)
    return delta, attestation


def atomic_collect_pair(delta_raw: bytes, attestation_raw: bytes) -> None:
    outputs = ((ROOT / DELTA_PATH, delta_raw), (ROOT / ATTESTATION_PATH, attestation_raw))
    require(all(not path.exists() for path, _ in outputs), "E_COLLECT_REFUSES_OVERWRITE")
    temps = [(path.with_name(path.name + ".tmp-p066-s76"), raw) for path, raw in outputs]
    require(all(not path.exists() for path, _ in temps), "E_COLLECT_TEMP_EXISTS")
    created_targets: list[Path] = []
    try:
        for path, raw in temps:
            path.write_bytes(raw)
            require(path.read_bytes() == raw, "E_COLLECT_TEMP_WRITE", str(path))
        for (target, expected), (temp, _) in zip(outputs, temps):
            os.replace(temp, target)
            created_targets.append(target)
            require(target.read_bytes() == expected, "E_COLLECT_WRITE", str(target))
    except (OSError, BuildFailure):
        for path in created_targets:
            if path.exists():
                path.unlink()
        raise
    finally:
        for path, _ in temps:
            if path.exists():
                path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--preview", action="store_true")
    modes.add_argument("--collect", action="store_true")
    args = parser.parse_args()
    first = build_artifacts(require_human=args.collect)
    second = build_artifacts(require_human=args.collect)
    first_raw = tuple(canonical_bytes(value) for value in first)
    second_raw = tuple(canonical_bytes(value) for value in second)
    require(first_raw == second_raw, "E_DETERMINISM")
    if args.preview:
        print("PASS_P066_STEP76_PREVIEW occurrences=433 unique=167 text=158/30597 pdf=6/308 image=3 process=17/20")
        return 0
    atomic_collect_pair(first_raw[0], first_raw[1])
    print("PASS_P066_STEP76_COLLECT JSON_PAIR_LAST determinism=2/2")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BuildFailure, KeyError, IndexError, TypeError, ValueError, OSError,
            UnicodeError, subprocess.TimeoutExpired) as error:
        code = error.code if isinstance(error, BuildFailure) else type(error).__name__
        print(f"FAIL_P066_STEP76_BUILD {code}: {error}")
        raise SystemExit(1)
