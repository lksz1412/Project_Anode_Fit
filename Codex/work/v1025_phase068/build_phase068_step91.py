#!/usr/bin/env python3
"""Single writer for the two Phase 068 Step 91 JSON artifacts.

The human result and three recovery controls must already be frozen.  This
program refuses existing outputs, reconstructs both payloads twice, and then
publishes inventory followed by attestation through same-directory hard links.
"""

from __future__ import annotations

import argparse
import sys

sys.dont_write_bytecode = True
import validate_phase068_step91 as contract  # noqa: E402


WRITER_SCHEMA = "P068-STEP91-TWO-JSON-WRITER-1"


def raw_pair() -> tuple[bytes, bytes]:
    inventory, attestation = contract.build_payload_objects()
    inventory_raw = contract.canonical_bytes(inventory)
    attestation_raw = contract.canonical_bytes(attestation)
    if contract.strict_load(inventory_raw) != inventory:
        contract.fail("E_BUILDER_INVENTORY_ROUNDTRIP")
    if contract.strict_load(attestation_raw) != attestation:
        contract.fail("E_BUILDER_ATTESTATION_ROUNDTRIP")
    if attestation["inventory_sha256"] != contract.sha256(inventory_raw):
        contract.fail("E_BUILDER_CROSS_BINDING")
    return inventory_raw, attestation_raw


def deterministic_pair() -> tuple[bytes, bytes]:
    external_pair = contract.deterministic_payload_pair()
    if external_pair != raw_pair():
        contract.fail("E_BUILDER_EXTERNAL_PAIR_MISMATCH")
    return external_pair


def collect() -> tuple[bytes, bytes]:
    if WRITER_SCHEMA != contract.COLLECTOR_SCHEMA:
        contract.fail("E_BUILDER_COLLECTOR_SCHEMA")
    return contract.collect_payloads()


def run_self_tests() -> int:
    tests = contract.run_self_tests()
    if WRITER_SCHEMA != "P068-STEP91-TWO-JSON-WRITER-1":
        contract.fail("E_BUILDER_SELF_SCHEMA")
    tests += 1
    if contract.INVENTORY == contract.ATTESTATION:
        contract.fail("E_BUILDER_SELF_PATHS")
    tests += 1
    if set((contract.INVENTORY, contract.ATTESTATION)) - set(contract.EXACT_EIGHT):
        contract.fail("E_BUILDER_SELF_ALLOWLIST")
    tests += 1
    if list(contract.EXPECTED_STATUS.values()) != ["A", "A", "A", "A", "A", "M", "M", "M"]:
        contract.fail("E_BUILDER_SELF_STATUS")
    tests += 1
    if contract.EXPECTED_PARENT != "d54d1a2b2378369cbeaef757309b3ed629491d2c":
        contract.fail("E_BUILDER_SELF_PARENT")
    tests += 1
    print(f"PASS_P068_STEP91_BUILDER_SELF_TESTS {tests}")
    return tests


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--preview-digests", action="store_true")
    modes.add_argument("--collect", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if args.self_test:
            run_self_tests()
            return 0
        if args.preview_digests:
            contract.validate_pre_json()
            inventory_raw, attestation_raw = deterministic_pair()
            print(
                "PASS_P068_STEP91_PREVIEW "
                f"inventory_bytes={len(inventory_raw)} inventory_sha256={contract.sha256(inventory_raw)} "
                f"attestation_bytes={len(attestation_raw)} attestation_sha256={contract.sha256(attestation_raw)}"
            )
            return 0
        inventory_raw, attestation_raw = collect()
        print(
            "PASS_P068_STEP91_COLLECT "
            f"inventory_bytes={len(inventory_raw)} inventory_sha256={contract.sha256(inventory_raw)} "
            f"attestation_bytes={len(attestation_raw)} attestation_sha256={contract.sha256(attestation_raw)}"
        )
        return 0
    except contract.ValidationError as exc:
        print(f"FAIL_P068_STEP91_BUILDER {exc.code} {exc.detail}".rstrip(), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
