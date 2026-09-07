#!/usr/bin/env python3
"""Thin atomic no-clobber writer for the U13 independent rederivation."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
import validate_phase068_step94 as contract


def atomic_create(path: Path, raw: bytes) -> None:
    if path.exists():
        contract.fail("E_MATRIX_EXISTS", path.name)
    temporary = path.with_name(path.name + ".tmp")
    descriptor = -1
    created = False
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0), 0o600)
        created = True
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                contract.fail("E_BUILDER_SHORT_WRITE")
            offset += written
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1
        if temporary.read_bytes() != raw:
            contract.fail("E_BUILDER_TEMP_VERIFY")
        os.link(temporary, path)
        if path.read_bytes() != raw:
            contract.fail("E_BUILDER_TARGET_VERIFY")
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if created:
            os.unlink(temporary)


def run_self_tests() -> int:
    tests = contract.run_self_tests()
    with tempfile.TemporaryDirectory(prefix="p068-step94-writer-") as directory:
        target = Path(directory) / "matrix.json"
        atomic_create(target, b"first\n")
        contract.expect_error("E_MATRIX_EXISTS", lambda: atomic_create(target, b"second\n"))
        if target.read_bytes() != b"first\n":
            contract.fail("E_BUILDER_SELFTEST_CLOBBER")
    if len(contract.EXACT_SEVEN) != 7 or list(contract.EXPECTED_STATUS.values()) != ["A","A","A","A","M","M","M"]:
        contract.fail("E_BUILDER_ALLOWLIST")
    return tests + 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--collect", action="store_true")
    modes.add_argument("--preview-digest", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    try:
        contract.validate_source_guard()
        if args.self_test:
            print(f"PASS_P068_STEP94_BUILDER_SELF_TESTS {run_self_tests()}")
            return 0
        raw = contract.validate_pre_json()
        if args.preview_digest:
            with tempfile.TemporaryDirectory(prefix="p068-step94-preview-") as directory:
                path = Path(directory) / "matrix.json"
                atomic_create(path, raw)
                if path.read_bytes() != raw:
                    contract.fail("E_PREVIEW_BYTES")
            print(f"PASS_P068_STEP94_PREVIEW bytes={len(raw)} sha256={contract.sha256(raw)} external_temp_cleanup=True")
            return 0
        atomic_create(contract.ROOT / contract.MATRIX, raw)
        print(f"PASS_P068_STEP94_COLLECT bytes={len(raw)} sha256={contract.sha256(raw)}")
        return 0
    except (contract.ValidationError, OSError) as exc:
        code = exc.code if isinstance(exc, contract.ValidationError) else "E_BUILDER_IO"
        detail = exc.detail if isinstance(exc, contract.ValidationError) else str(exc)
        print(f"FAIL_P068_STEP94_BUILDER {code} {detail}".rstrip(), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
