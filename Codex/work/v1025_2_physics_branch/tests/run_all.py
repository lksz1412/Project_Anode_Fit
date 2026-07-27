#!/usr/bin/env python3
"""Run the complete conformance suite without requiring pytest."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


def main() -> int:
    tests_root = Path(__file__).resolve().parent
    suite = unittest.defaultTestLoader.discover(
        str(tests_root), pattern="test_*.py", top_level_dir=str(tests_root)
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
