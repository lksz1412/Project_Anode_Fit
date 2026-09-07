"""Typed reconciliation coverage tests; no scientific source is executed."""
import copy
import importlib.util
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import unittest


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).with_name("reconcile_phase068_claims.py")
        self.assertTrue(path.is_file(), "reconciliation helper is not implemented")
        spec = importlib.util.spec_from_file_location("reconcile", path)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.source = [{"id": "A", "kind": "CLAIM", "source": {"record_sha256": "abc"}}]
        self.rows = [dict(self.source[0], classification="OPEN", reason="Source unavailable",
                          evidence=["frozen result:1-3"], counterparts=[], owner="Phase071",
                          acceptance="Original claim support", scientific_truth_promoted=False)]

    def test_complete_union_is_accepted(self):
        self.assertEqual(self.module.validate_rows(self.source, self.rows), {"OPEN": 1})

    def test_missing_unit_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "coverage"):
            self.module.validate_rows(self.source, [])

    def test_duplicate_unit_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.module.validate_rows(self.source, self.rows * 2)

    def test_invalid_classification_is_rejected(self):
        self.rows[0]["classification"] = "PASS"
        with self.assertRaisesRegex(ValueError, "classification"):
            self.module.validate_rows(self.source, self.rows)

    def test_changed_source_record_is_rejected(self):
        self.rows = copy.deepcopy(self.rows)
        self.rows[0]["source"]["record_sha256"] = "different"
        with self.assertRaisesRegex(ValueError, "source"):
            self.module.validate_rows(self.source, self.rows)

    def test_open_owner_is_required(self):
        self.rows[0]["owner"] = ""
        with self.assertRaisesRegex(ValueError, "owner"):
            self.module.validate_rows(self.source, self.rows)

    def test_evidence_and_acceptance_are_required(self):
        for key, value in [("evidence", []), ("acceptance", "")]:
            changed = copy.deepcopy(self.rows)
            changed[0][key] = value
            with self.assertRaisesRegex(ValueError, key):
                self.module.validate_rows(self.source, changed)

    def test_unknown_counterpart_is_rejected(self):
        self.rows[0]["counterparts"] = ["MISSING"]
        with self.assertRaisesRegex(ValueError, "counterpart"):
            self.module.validate_rows(self.source, self.rows)

    def test_scientific_promotion_is_rejected(self):
        self.rows[0]["scientific_truth_promoted"] = True
        with self.assertRaisesRegex(ValueError, "promotion"):
            self.module.validate_rows(self.source, self.rows)

    def test_strict_json_rejects_duplicate_and_nonfinite(self):
        for raw in ['{"a":1,"a":2}', '{"a":NaN}', '{"a":1e999}']:
            with self.assertRaises(ValueError):
                self.module.strict_json(raw)

    def test_records_canonical_hash_and_selector(self):
        group = self.module.records("path.json", "blob", "claims", [{"id": "A", "value": 2}], "CLAIM")
        self.assertEqual(group[0]["source"]["selector"], "claims[0]")
        self.assertEqual(group[0]["source"]["record_sha256"],
                         self.module.digest({"id": "A", "value": 2}))

    def test_inventory_cli_survives_cp949_stdout(self):
        root = Path(__file__).resolve().parents[3]
        env = dict(os.environ, PYTHONIOENCODING="cp949")
        run = subprocess.run([sys.executable, "-B", str(Path(__file__).with_name(
            "reconcile_phase068_claims.py")), "--root", str(root), "--inventory"],
            cwd=root, env=env, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr.decode("ascii", errors="replace"))
        self.assertEqual(len(self.module.strict_json(run.stdout)["units"]), 329)

    def test_wrong_result_path_is_rejected_even_with_matching_hash(self):
        self.assertTrue(callable(getattr(self.module, "validate_result", None)),
                        "exact result binding is not implemented")
        root = Path(__file__).resolve().parents[3]
        wrong = "Codex/AGENTS.md"
        matching = hashlib.sha256((root / wrong).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        for path in (wrong, str(root / wrong)):
            with self.assertRaisesRegex(ValueError, "result path"):
                self.module.validate_result(root, {"result_path": path, "result_lf_sha256": matching})

    def test_declared_result_path_and_hash_are_accepted(self):
        self.assertTrue(callable(getattr(self.module, "validate_result", None)),
                        "exact result binding is not implemented")
        root = Path(__file__).resolve().parents[3]
        path = "Codex/results/PHASE_068_STEP_096_FORK_CONFLICT_ADJUDICATION_RESULT.md"
        expected = hashlib.sha256((root / path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        self.assertEqual(self.module.validate_result(root, {
            "result_path": path, "result_lf_sha256": expected}), expected)

    def test_self_counterpart_is_rejected(self):
        self.rows[0]["counterparts"] = ["A"]
        with self.assertRaisesRegex(ValueError, "counterpart"):
            self.module.validate_rows(self.source, self.rows)

    def test_duplicate_counterpart_is_rejected(self):
        other = {"id": "B", "kind": "CLAIM", "source": {"record_sha256": "b"}}
        self.source.append(other)
        self.rows.append(dict(self.rows[0], **other))
        self.rows[0]["counterparts"] = ["B", "B"]
        with self.assertRaisesRegex(ValueError, "counterpart"):
            self.module.validate_rows(self.source, self.rows)


if __name__ == "__main__":
    unittest.main(verbosity=2)
