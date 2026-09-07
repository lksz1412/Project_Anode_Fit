"""Five-state disposition and lossless carry contract tests."""
import copy
import importlib.util
from pathlib import Path
import unittest


class DispositionTests(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).with_name("dispose_phase068_evidence.py")
        self.assertTrue(path.is_file(), "disposition helper is not implemented")
        spec = importlib.util.spec_from_file_location("dispose", path)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.targets = [{"target_id": "A", "target_kind": "CLAIM",
                         "source": {"blob": "abc", "record_sha256": "d"}}]
        self.rows = [dict(self.targets[0], disposition="REFERENCE_ONLY",
                         rationale="Historical finding", bounded_content="Stored evidence only",
                         evidence=["immutable:path:1"], canonical_owner="PHASE-070",
                         target_phase=70, acceptance_criterion="Preserve original identity",
                         prohibited_promotion="No material or original-paper authority",
                         relation_links=[], whole_commit_adoption=False)]
        self.prior = [{"obligation_id": "OLD", "canonical_owner": "PHASE-071",
                       "target_phase": 71, "acceptance_criterion": "Read original",
                       "state": "OPEN_CARRY", "external_authority_promoted": False}]
        self.carry = {"inherited_active": copy.deepcopy(self.prior), "new_obligations": [],
                      "resolved_subpredicates": [], "target_routes": [
                          {"target_id": "A", "obligation_ids": ["OLD"], "state": "ACTIVE"}]}

    def test_complete_register(self):
        self.assertEqual(self.m.validate_register(self.targets, self.rows), {"REFERENCE_ONLY": 1})

    def test_missing_or_duplicate_target(self):
        for rows in [[], self.rows * 2]:
            with self.assertRaises(ValueError):
                self.m.validate_register(self.targets, rows)

    def test_invalid_disposition(self):
        self.rows[0]["disposition"] = "KEEP"
        with self.assertRaisesRegex(ValueError, "disposition"):
            self.m.validate_register(self.targets, self.rows)

    def test_changed_source(self):
        rows = copy.deepcopy(self.rows)
        rows[0]["source"]["record_sha256"] = "changed"
        with self.assertRaisesRegex(ValueError, "source"):
            self.m.validate_register(self.targets, rows)

    def test_owner_and_acceptance_required(self):
        for key in ["canonical_owner", "acceptance_criterion"]:
            rows = copy.deepcopy(self.rows)
            rows[0][key] = ""
            with self.assertRaisesRegex(ValueError, key):
                self.m.validate_register(self.targets, rows)

    def test_whole_commit_adoption_rejected(self):
        self.rows[0]["whole_commit_adoption"] = True
        with self.assertRaisesRegex(ValueError, "whole.commit"):
            self.m.validate_register(self.targets, self.rows)

    def test_unknown_relation_rejected(self):
        self.rows[0]["relation_links"] = ["MISSING"]
        with self.assertRaisesRegex(ValueError, "relation"):
            self.m.validate_register(self.targets, self.rows)

    def test_inherited_carry_unchanged(self):
        self.assertEqual(self.m.validate_carry(self.prior, self.carry, self.rows)["active"], 1)

    def test_lost_or_changed_inherited_carry(self):
        for value in [[], [dict(self.prior[0], canonical_owner="REPLACEMENT")]]:
            carry = copy.deepcopy(self.carry)
            carry["inherited_active"] = value
            with self.assertRaisesRegex(ValueError, "inherited"):
                self.m.validate_carry(self.prior, carry, self.rows)

    def test_unknown_obligation_route(self):
        self.carry["target_routes"][0]["obligation_ids"] = ["MISSING"]
        with self.assertRaisesRegex(ValueError, "route"):
            self.m.validate_carry(self.prior, self.carry, self.rows)

    def test_inherited_json_types_preserved(self):
        self.carry["inherited_active"][0]["external_authority_promoted"] = 0
        with self.assertRaisesRegex(ValueError, "inherited"):
            self.m.validate_carry(self.prior, self.carry, self.rows)

    def test_new_obligation_is_routed_from_every_origin(self):
        self.carry["new_obligations"] = [dict(self.prior[0], obligation_id="NEW",
                                             origin_target_ids=["A"])]
        with self.assertRaisesRegex(ValueError, "origin route"):
            self.m.validate_carry(self.prior, self.carry, self.rows)

    def test_unverified_target_requires_active_route(self):
        self.rows[0]["disposition"] = "UNVERIFIED"
        self.carry["target_routes"][0] = {"target_id": "A", "obligation_ids": [], "state": "NOT_REQUIRED"}
        with self.assertRaisesRegex(ValueError, "active route"):
            self.m.validate_carry(self.prior, self.carry, self.rows)

    def test_new_obligation_requires_one_owner(self):
        self.carry["new_obligations"] = [{"obligation_id": "NEW", "canonical_owner": ["ONE", "TWO"],
                                        "target_phase": 71, "acceptance_criterion": "support",
                                        "state": "OPEN_CARRY", "external_authority_promoted": False}]
        with self.assertRaisesRegex(ValueError, "canonical_owner"):
            self.m.validate_carry(self.prior, self.carry, self.rows)

    def test_wrong_result_path(self):
        with self.assertRaisesRegex(ValueError, "result path"):
            self.m.validate_result(Path.cwd(), {"result_path": "Codex/AGENTS.md"})

    def test_historical_inherited_phase_is_preserved(self):
        self.targets[0]["target_kind"] = "INHERITED_OBLIGATION"
        self.rows[0]["target_kind"] = "INHERITED_OBLIGATION"
        self.rows[0]["target_phase"] = 65
        self.assertEqual(self.m.validate_register(self.targets, self.rows), {"REFERENCE_ONLY": 1})


if __name__ == "__main__":
    unittest.main(verbosity=2)
