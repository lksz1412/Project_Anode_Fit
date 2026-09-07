#!/usr/bin/env python3
"""Single writer for the two Phase 068 Step 92 JSON artifacts."""

from __future__ import annotations

import argparse
import sys

sys.dont_write_bytecode = True
import validate_phase068_step92 as contract  # noqa: E402


def run_self_tests() -> int:
    tests = contract.run_self_tests()
    if contract.EXACT_EIGHT[:4] != (
        contract.BUILDER,
        contract.VALIDATOR,
        contract.INVENTORY,
        contract.ATTESTATION,
    ):
        contract.fail("E_BUILDER_OUTPUT_ORDER")
    tests += 1
    if [contract.EXPECTED_STATUS[path] for path in contract.EXACT_EIGHT] != ["A", "A", "A", "A", "A", "M", "M", "M"]:
        contract.fail("E_BUILDER_STATUS")
    tests += 1
    print(f"PASS_P068_STEP92_BUILDER_SELF_TESTS {tests}")
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
        contract.validate_source_guard()
        if args.self_test:
            run_self_tests()
            return 0
        if args.preview_digests:
            contract.validate_pre_json()
            inventory, attestation = contract.deterministic_pair()
            print(
                "PASS_P068_STEP92_PREVIEW "
                f"inventory_bytes={len(inventory)} inventory_sha256={contract.sha256(inventory)} "
                f"attestation_bytes={len(attestation)} attestation_sha256={contract.sha256(attestation)}"
            )
            return 0
        inventory, attestation = contract.collect_payloads()
        print(
            "PASS_P068_STEP92_COLLECT "
            f"inventory_bytes={len(inventory)} inventory_sha256={contract.sha256(inventory)} "
            f"attestation_bytes={len(attestation)} attestation_sha256={contract.sha256(attestation)}"
        )
        return 0
    except contract.ValidationError as exc:
        print(f"FAIL_P068_STEP92_BUILDER {exc.code} {exc.detail}".rstrip(), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
