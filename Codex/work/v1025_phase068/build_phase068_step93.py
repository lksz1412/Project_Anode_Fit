#!/usr/bin/env python3
"""Single no-clobber writer for the Phase 068 Step 93 reaudit matrix."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
import validate_phase068_step93 as contract  # noqa: E402


def writer_flags() -> int:
    return os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)


def atomic_create(path: Path, raw: bytes) -> None:
    if path.exists():
        contract.fail("E_MATRIX_EXISTS", contract.MATRIX)
    temporary = path.with_name(path.name + ".tmp")
    if temporary.exists():
        contract.fail("E_BUILDER_TEMP_EXISTS", temporary.name)
    descriptor = -1
    try:
        descriptor = os.open(temporary, writer_flags(), 0o600)
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
        # A hard-link publish is the only target creation.  Unlike replace(),
        # it fails if another process created the target after the first check.
        os.link(temporary, path)
        if path.read_bytes() != raw:
            contract.fail("E_BUILDER_TARGET_VERIFY")
        os.unlink(temporary)
    except Exception:
        if descriptor >= 0:
            os.close(descriptor)
        # Never remove the published target by path after a failure: another
        # process could have replaced that directory entry. A surviving target
        # makes the next collection fail closed and remains available for audit.
        if temporary.exists():
            os.unlink(temporary)
        raise


def run_self_tests() -> int:
    tests = contract.run_self_tests()
    if contract.EXACT_SEVEN[:4] != (contract.BUILDER, contract.VALIDATOR, contract.MATRIX, contract.RESULT):
        contract.fail("E_BUILDER_ALLOWLIST")
    tests += 1
    if [contract.EXPECTED_STATUS[path] for path in contract.EXACT_SEVEN] != ["A", "A", "A", "A", "M", "M", "M"]:
        contract.fail("E_BUILDER_STATUS")
    tests += 1
    flags = writer_flags()
    required = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    binary = getattr(os, "O_BINARY", 0)
    if flags & required != required or (binary and flags & binary != binary):
        contract.fail("E_BUILDER_BINARY_FLAGS")
    tests += 1
    selftest_base = (contract.ROOT / "Codex/work/v1025_phase068").resolve()
    if contract.ROOT.resolve() not in selftest_base.parents:
        contract.fail("E_BUILDER_SELFTEST_CONTAINMENT")
    with tempfile.TemporaryDirectory(prefix="p068-step93-writer-", dir=selftest_base) as directory:
        probe = Path(directory) / "matrix.json"
        atomic_create(probe, b"first\n")
        if probe.read_bytes() != b"first\n":
            contract.fail("E_BUILDER_SELFTEST_BYTES")
        try:
            atomic_create(probe, b"second\n")
        except contract.ValidationError as exc:
            if exc.code != "E_MATRIX_EXISTS":
                raise
        else:
            contract.fail("E_BUILDER_SELFTEST_CLOBBER")
        if probe.read_bytes() != b"first\n":
            contract.fail("E_BUILDER_SELFTEST_CLOBBER")
    tests += 1
    print(f"PASS_P068_STEP93_BUILDER_SELF_TESTS {tests}")
    return tests


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--preview-digest", action="store_true")
    modes.add_argument("--collect", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        contract.validate_source_guard()
        if args.self_test:
            run_self_tests()
            return 0
        raw = contract.validate_pre_json()
        if args.preview_digest:
            print(f"PASS_P068_STEP93_PREVIEW bytes={len(raw)} sha256={contract.sha256(raw)}")
            return 0
        target = contract.ROOT / contract.MATRIX
        atomic_create(target, raw)
        if target.read_bytes() != raw:
            contract.fail("E_BUILDER_VERIFY")
        print(f"PASS_P068_STEP93_COLLECT bytes={len(raw)} sha256={contract.sha256(raw)}")
        return 0
    except contract.ValidationError as exc:
        print(f"FAIL_P068_STEP93_BUILDER {exc.code} {exc.detail}".rstrip(), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
