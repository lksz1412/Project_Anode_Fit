"""Tests for the bounded frozen-source execution recorder."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest

RUNNER = Path(__file__).with_name("run_phase068_step95.py")


class RecorderTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(RUNNER.is_file(), "Step95 execution recorder is not implemented")
        spec = importlib.util.spec_from_file_location("step95_recorder", RUNNER)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def test_actual_child_failure_preserves_exit_and_streams(self):
        result = self.mod.capture([sys.executable, "-c",
            "import sys; print('out'); print('err', file=sys.stderr); sys.exit(7)"], Path.cwd())
        self.assertEqual(result["exit_code"], 7)
        self.assertEqual(result["stdout"], "out\n")
        self.assertEqual(result["stderr"], "err\n")

    def test_actual_child_success_is_not_inferred(self):
        result = self.mod.capture([sys.executable, "-c", "print('actual')"], Path.cwd())
        self.assertEqual(result["exit_code"], 0)
        self.assertEqual(result["stdout"], "actual\n")
        self.assertEqual(result["stderr"], "")

    def test_missing_input_and_blob_mutation_are_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            self.assertRaises(FileNotFoundError, self.mod.verify_file, root / "absent", "0" * 40)
            path = root / "fixture"
            path.write_bytes(b"x")
            self.assertRaises(ValueError, self.mod.verify_file, path, "0" * 40)
            oid = hashlib.sha1(b"blob 1\0x").hexdigest()
            self.assertEqual(self.mod.verify_file(path, oid)["bytes"], 1)

    def test_json_write_is_no_clobber_and_strict(self):
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / "receipt.json"
            self.mod.write_new(path, {"exit_code": 0})
            self.assertEqual(json.loads(path.read_text()), {"exit_code": 0})
            self.assertRaises(FileExistsError, self.mod.write_new, path, {})
            self.assertRaises(ValueError, self.mod.write_new, Path(name) / "bad.json", {"x": float("nan")})


if __name__ == "__main__":
    unittest.main(verbosity=2)
