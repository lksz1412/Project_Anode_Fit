"""Reuse frozen U13 calculations under an explicit checkpoint-aware contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import subprocess
import sys

sys.dont_write_bytecode = True
import validate_phase068_step94 as legacy
from build_phase068_step94 import atomic_create

ROOT = Path(__file__).resolve().parents[3]
CHECKPOINT = "aedfd408281b97699ba7f75884e7108965ecf547"
EXECUTION_PARENT = "58d752b63b75a4e516e76f848c1e308adeca0e03"
RUNNER = "Codex/work/v1025_phase068/run_phase068_step94_astra.py"
RESULT = "Codex/results/PHASE_068_STEP_094_ASTRA_VERIFICATION_RESULT.md"
SOURCE_HASHES = {
    legacy.VALIDATOR: "658de05f5c652bc381536f4ebc48722b3a6a4f7ae6dd4ef2b3cebfd1a5613eba",
    legacy.BUILDER: "1ae30e36c520bf06c7e724b08480878fb9793051ebad2de6952d0bfd666a990a",
}


def check_source_identity(path: str, raw: bytes, expected: str) -> None:
    if legacy.sha256(legacy.lf_normalize(raw)) != expected:
        legacy.fail("E_ASTRA_SOURCE_IDENTITY", path)


def frozen_candidate() -> dict:
    for path, digest in SOURCE_HASHES.items():
        check_source_identity(path, (ROOT / path).read_bytes(), digest)
    legacy.validate_source_guard()
    value = legacy.expected_matrix()
    identities = []
    for path in legacy.PRE_JSON_SIX:
        raw = legacy.frozen_bytes(CHECKPOINT, path)
        identities.append({"path": path, "raw_bytes": len(raw), "raw_sha256": legacy.sha256(raw),
                           "lf_sha256": legacy.sha256(legacy.lf_normalize(raw)),
                           "lines": legacy.physical_lines(raw)})
    value["pre_json_file_identities"] = identities
    value["semantic_sha256"] = legacy.semantic_sha(value)
    return value


def envelope(candidate: dict) -> dict:
    value = {
        "schema": "P068-STEP94-ASTRA-CHECKPOINT-CONTINUATION-1", "phase": 68, "step": 94,
        "checkpoint": CHECKPOINT, "execution_parent": EXECUTION_PARENT,
        "required_commit_subject": "audit(phase068): complete Astra U13 rederivation verification",
        "content_terminal": "PASS_P068_STEP94_ASTRA_CONTENT",
        "contract": "Codex/plans/2026-09-07-phase068-astra-continuation-detailed-plan.md",
        "runner": RUNNER, "runner_lf_sha256": legacy.sha256(legacy.lf_normalize((ROOT / RUNNER).read_bytes())),
        "verification_result": RESULT,
        "legacy_candidate": candidate,
        "legacy_transaction_authority": "ARCHIVED_STEP93_CERTIFICATE_NOT_CURRENT_HEAD_OR_PERSISTENCE",
        "legacy_pre_json_identity_basis": "CANONICAL_GIT_BLOBS_AT_CHECKPOINT_NOT_CHECKOUT_BYTES",
        "read_reuse": "PRIOR_FULL_READ_ATTESTATIONS_REUSED_AFTER_EXACT_SOURCE_IDENTITY_CHECK_NOT_FRESH_FULL_READ",
        "numeric_execution": "FRESH_REEXECUTION_OF_UNCHANGED_NUMERICAL_ROUTINES_NOT_EXTERNAL_SCIENTIFIC_VALIDATION",
    }
    value["semantic_sha256"] = legacy.semantic_sha(value)
    return value


def read_matrix(path: Path) -> dict:
    if not path.is_file():
        legacy.fail("E_MATRIX_MISSING", path.name)
    raw = path.read_bytes()
    value = legacy.strict_json_loads(raw, label=path.name)
    if legacy.canonical_bytes(value) != raw:
        legacy.fail("E_MATRIX_CANONICAL")
    return value


def check_envelope(value: dict, candidate: dict) -> None:
    if not isinstance(value, dict) or value.get("semantic_sha256") != legacy.semantic_sha(value):
        legacy.fail("E_ASTRA_SEAL")
    if value != envelope(candidate):
        legacy.fail("E_ASTRA_ENVELOPE")


def captured_receipt(process: subprocess.CompletedProcess) -> dict:
    return {"exit_code": process.returncode, "stdout": process.stdout, "stderr": process.stderr}


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(allow_abbrev=False)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--preview", action="store_true")
    modes.add_argument("--collect", action="store_true")
    modes.add_argument("--verify", action="store_true")
    parser.add_argument("--record-runtime", action="store_true")
    args = parser.parse_args(argv)
    if args.record_runtime and not args.verify:
        parser.error("--record-runtime requires --verify")
    try:
        if args.record_runtime:
            runtime = f"{sys.version_info.major}{sys.version_info.minor}"
            if runtime not in ("312", "314"):
                legacy.fail("E_ASTRA_RUNTIME", runtime)
            process = subprocess.run(
                [sys.executable, "-B", str(ROOT / RUNNER), "--verify"], cwd=ROOT,
                stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", check=False,
            )
            receipt = {
                "schema": "P068-STEP94-ASTRA-RUNTIME-2", "python": platform.python_version(),
                "numpy": legacy.np.__version__, "mpmath": legacy.mp.__version__,
                "command": ["python", "-B", RUNNER, "--verify"],
                "command_representation": "PORTABLE_PATHS_SAME_EXECUTABLE_AND_REPOSITORY_ROOT_AS_PARENT",
                "cwd": "repository_root", **captured_receipt(process),
                "runner_lf_sha256": legacy.sha256(legacy.lf_normalize((ROOT / RUNNER).read_bytes())),
                "result_lf_sha256": legacy.file_identity(RESULT)["lf_sha256"],
                "authority": "CAPTURED_NUMERICAL_CHILD_PROCESS_GIT_PERSISTENCE_VERIFIED_SEPARATELY",
            }
            if process.returncode == 0:
                receipt["summary"] = json.loads(process.stdout)
                receipt["matrix_sha256"] = receipt["summary"]["matrix_sha256"]
            receipt_path = ROOT / f"Codex/results/PHASE_068_STEP_094_ASTRA_RUNTIME_{runtime}.json"
            atomic_create(receipt_path, legacy.canonical_bytes(receipt))
            print(process.stdout, end="")
            print(process.stderr, end="", file=sys.stderr)
            return process.returncode
        matrix = ROOT / legacy.MATRIX
        stored = read_matrix(matrix) if args.verify else None
        if args.collect and matrix.exists():
            legacy.fail("E_MATRIX_EXISTS", legacy.MATRIX)
        if not args.preview and not (ROOT / RESULT).is_file():
            legacy.fail("E_ASTRA_RESULT_FIRST", RESULT)
        candidate = frozen_candidate()
        legacy.validate_matrix_payload(candidate, candidate)
        negatives = legacy.run_self_tests(candidate)
        value = envelope(candidate)
        if stored is not None:
            check_envelope(stored, candidate)
        raw = legacy.canonical_bytes(value)
        if args.collect:
            atomic_create(matrix, raw)
        numeric = candidate["numeric"]
        summary = {
            "terminal": "PASS_P068_STEP94_ASTRA_CONTENT" if args.verify else "PASS_P068_STEP94_ASTRA_PREVIEW" if args.preview else "PASS_P068_STEP94_ASTRA_COLLECT",
            "matrix_bytes": len(raw), "matrix_sha256": legacy.sha256(raw),
            "legacy_negative_controls": negatives, "sources": len(candidate["sources"]),
            "propositions": len(candidate["analytic"]["propositions"]),
            "numeric_row_counts": {key: len(rows) for key, rows in numeric.items() if isinstance(rows, list)},
        }
        stdout = json.dumps(summary, sort_keys=True) + "\n"
        print(stdout, end="")
        return 0
    except (legacy.ValidationError, OSError, ValueError) as exc:
        code = exc.code if isinstance(exc, legacy.ValidationError) else "E_ASTRA_IO_OR_VALUE"
        print(f"FAIL_P068_STEP94_ASTRA {code}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
