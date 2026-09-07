"""Focused tests for the checkpoint-aware U13 evidence envelope."""

import copy
import importlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True


class AstraEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner_path = Path(__file__).with_name("run_phase068_step94_astra.py")

    def runner(self):
        self.assertTrue(self.runner_path.is_file(), "Checkpoint-aware evidence runner is not implemented")
        return importlib.import_module("run_phase068_step94_astra")

    def test_verify_missing_matrix_reports_named_failure(self):
        runner = self.runner()
        with tempfile.TemporaryDirectory(prefix="u13-missing-") as directory:
            with self.assertRaisesRegex(runner.legacy.ValidationError, "E_MATRIX_MISSING"):
                runner.read_matrix(Path(directory) / "missing.json")

    def test_changed_source_is_rejected(self):
        runner = self.runner()
        with self.assertRaisesRegex(runner.legacy.ValidationError, "E_ASTRA_SOURCE_IDENTITY"):
            runner.check_source_identity("test.py", b"changed", "0" * 64)

    def test_canonical_envelope_roundtrip(self):
        runner = self.runner()
        candidate = {"scope": "test fixture, not a scientific payload"}
        value = runner.envelope(candidate)
        self.assertEqual(value["legacy_candidate"], candidate)
        self.assertEqual(value["step"], 94)
        self.assertEqual(value["checkpoint"], runner.CHECKPOINT)
        self.assertNotEqual(value["execution_parent"], runner.legacy.EXPECTED_PARENT)
        with tempfile.TemporaryDirectory(prefix="u13-envelope-") as directory:
            target = Path(directory) / "matrix.json"
            runner.atomic_create(target, runner.legacy.canonical_bytes(value))
            self.assertEqual(runner.read_matrix(target), value)

    def test_resealed_wrong_checkpoint_is_rejected(self):
        runner = self.runner()
        value = runner.envelope({})
        value["checkpoint"] = "0" * 40
        value["semantic_sha256"] = runner.legacy.semantic_sha(value)
        with self.assertRaisesRegex(runner.legacy.ValidationError, "E_ASTRA_ENVELOPE"):
            runner.check_envelope(value, {})

    def test_unsealed_mutation_is_rejected(self):
        runner = self.runner()
        value = runner.envelope({})
        value["step"] = 95
        with self.assertRaisesRegex(runner.legacy.ValidationError, "E_ASTRA_SEAL"):
            runner.check_envelope(value, {})

    def test_fresh_read_promotion_is_rejected(self):
        runner = self.runner()
        value = runner.envelope({})
        value["read_reuse"] = "FRESH_FULL_READ"
        value["semantic_sha256"] = runner.legacy.semantic_sha(value)
        with self.assertRaisesRegex(runner.legacy.ValidationError, "E_ASTRA_ENVELOPE"):
            runner.check_envelope(value, {})

    def test_writer_refuses_overwrite(self):
        runner = self.runner()
        with tempfile.TemporaryDirectory(prefix="u13-writer-") as directory:
            target = Path(directory) / "matrix.json"
            runner.atomic_create(target, b"first\n")
            with self.assertRaisesRegex(runner.legacy.ValidationError, "E_MATRIX_EXISTS"):
                runner.atomic_create(target, b"second\n")
            self.assertEqual(target.read_bytes(), b"first\n")

    def test_duplicate_json_key_is_rejected(self):
        runner = self.runner()
        with tempfile.TemporaryDirectory(prefix="u13-json-") as directory:
            target = Path(directory) / "matrix.json"
            runner.atomic_create(target, b'{"step":94,"step":95}\n')
            with self.assertRaisesRegex(runner.legacy.ValidationError, "E_JSON_DUPLICATE_KEY"):
                runner.read_matrix(target)

    def test_success_receipt_captures_real_process_output(self):
        runner = self.runner()
        self.assertTrue(hasattr(runner, "captured_receipt"), "Actual process capture is not implemented")
        command = [sys.executable, "-c", "import sys; print('observed output'); print('observed warning', file=sys.stderr)"]
        process = subprocess.run(command, capture_output=True, text=True, check=False)
        receipt = runner.captured_receipt(process)
        self.assertEqual(receipt["exit_code"], process.returncode)
        self.assertEqual(receipt["stdout"], process.stdout)
        self.assertEqual(receipt["stderr"], process.stderr)
        self.assertIn("observed warning", receipt["stderr"])

    def test_failure_receipt_preserves_nonzero_exit_and_stderr(self):
        runner = self.runner()
        self.assertTrue(hasattr(runner, "captured_receipt"), "Actual process capture is not implemented")
        command = [sys.executable, "-c", "import sys; print('partial output'); print('actual failure', file=sys.stderr); sys.exit(7)"]
        process = subprocess.run(command, capture_output=True, text=True, check=False)
        receipt = runner.captured_receipt(process)
        self.assertEqual(receipt["exit_code"], 7)
        self.assertEqual(receipt["stdout"], process.stdout)
        self.assertEqual(receipt["stderr"], process.stderr)
        self.assertIn("actual failure", receipt["stderr"])


if __name__ == "__main__":
    unittest.main()
