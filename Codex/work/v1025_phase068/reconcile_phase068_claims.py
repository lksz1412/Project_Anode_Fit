"""Read immutable claim records and validate a typed reconciliation register."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess

BASE = "7141da513c931282cb201ab356d189dab13f50db"
RESULT_PATH = "Codex/results/PHASE_068_STEP_096_FORK_CONFLICT_ADJUDICATION_RESULT.md"
INPUTS = [
    ("PHASE_068_CLAUDE_FORK_DIFF_INVENTORY.json", "c050802be498cddcffccff3be814c59566dd4601",
     [("claims", "CLAUDE_CLAIM", 98), ("supplemental_claim_units", "SUPPLEMENTAL_SOURCE_UNIT", 8)]),
    ("PHASE_068_CODEX_FORK_DIFF_INVENTORY.json", "c78e7ca1e1bbe6889f92f83e52d46798d4fb5c26",
     [("claims", "CODEX_CLAIM", 30)]),
    ("PHASE_068_PHASE044_054_REAUDIT_MATRIX.json", "c5b6e65f1b4889f63d2e1b1f7b3e4b2b88e82931",
     [("judgments", "HISTORICAL_NAMED_TOPIC", 142)]),
    ("PHASE_068_U13_REGSOL_REDERIVATION.json", "7ecd6e86177cbb6a0f8632cb72f4247388d4c05e",
     [("legacy_candidate.analytic.propositions", "U13_PROPOSITION", 7)]),
    ("PHASE_068_CONFORMANCE_MODEL_ADJUDICATION.json", "bd3af86bf461b74d693bf41da12fdbe6c9a5db40",
     [("claims", "STEP95_FINDING", 12), ("contracts", "PHY_CONTRACT", 32)]),
]
CLASSIFICATIONS = {"CONFLICT", "COMPATIBLE", "SUPERSEDED_WITH_EVIDENCE", "OPEN"}


def strict_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result
    value = json.loads(raw, object_pairs_hook=unique)
    json.dumps(value, allow_nan=False)
    return value


def digest(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def records(path, blob, selector, values, kind):
    return [{"id": row["id"], "kind": kind,
             "source": {"commit": BASE, "path": path, "blob": blob,
                        "selector": f"{selector}[{index}]",
                        "record_sha256": digest(row)}}
            for index, row in enumerate(values)]


def collect(root):
    union, original = [], {}
    for filename, expected_blob, groups in INPUTS:
        path = "Codex/results/" + filename
        raw = subprocess.run(["git", "show", f"{BASE}:{path}"], cwd=root,
                             check=True, capture_output=True).stdout
        blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        if blob != expected_blob:
            raise ValueError("source blob mismatch: " + path)
        data = strict_json(raw)
        for selector, kind, count in groups:
            values = data
            for key in selector.split("."):
                values = values[key]
            if len(values) != count:
                raise ValueError("source coverage count: " + selector)
            group = records(path, blob, selector, values, kind)
            for unit, row in zip(group, values):
                if unit["id"] in original:
                    raise ValueError("duplicate source id: " + unit["id"])
                original[unit["id"]] = row
            union.extend(group)
    return union, original


def validate_rows(source, rows):
    expected = {row["id"]: row for row in source}
    if len(expected) != len(source):
        raise ValueError("duplicate source id")
    ids = [row["id"] for row in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate row id")
    if set(ids) != set(expected):
        raise ValueError("coverage missing/extra: " + str(set(ids) ^ set(expected)))
    for row in rows:
        unit = expected[row["id"]]
        if row["kind"] != unit["kind"] or row["source"] != unit["source"]:
            raise ValueError("source identity mismatch: " + row["id"])
        if row["classification"] not in CLASSIFICATIONS:
            raise ValueError("classification: " + row["id"])
        for key in ("reason", "owner", "acceptance"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError(key + ": " + row["id"])
        if not isinstance(row.get("evidence"), list) or not row["evidence"]:
            raise ValueError("evidence: " + row["id"])
        if not all(isinstance(item, str) and item.strip() for item in row["evidence"]):
            raise ValueError("evidence entry: " + row["id"])
        peers = row.get("counterparts")
        if (not isinstance(peers, list) or any(peer not in expected for peer in peers)
                or len(set(peers)) != len(peers) or row["id"] in peers):
            raise ValueError("counterpart: " + row["id"])
        if row.get("scientific_truth_promoted") is not False:
            raise ValueError("scientific promotion: " + row["id"])
    return dict(sorted(Counter(row["classification"] for row in rows).items()))


def validate_result(root, matrix):
    if matrix["result_path"] != RESULT_PATH:
        raise ValueError("result path")
    raw = (root / RESULT_PATH).read_bytes().replace(b"\r\n", b"\n")
    result_hash = hashlib.sha256(raw).hexdigest()
    if result_hash != matrix["result_lf_sha256"]:
        raise ValueError("result identity")
    return result_hash


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--inventory", action="store_true")
    parser.add_argument("--matrix", type=Path)
    args = parser.parse_args()
    union, original = collect(args.root)
    if args.inventory:
        output = {"units": union, "original": original}
    else:
        if args.matrix is None:
            parser.error("--matrix is required without --inventory")
        matrix = strict_json(args.matrix.read_bytes())
        counts = validate_rows(union, matrix["rows"])
        if matrix["source_commit"] != BASE:
            raise ValueError("source commit")
        result_hash = validate_result(args.root, matrix)
        output = {"gate": "PASS_P068_STEP96_FORK_CONFLICT_CONTENT",
                  "units": len(union), "counts": counts, "rows_sha256": digest(matrix["rows"]),
                  "kind_counts": dict(sorted(Counter(row["kind"] for row in union).items())),
                  "source_commit": BASE, "result_lf_sha256": result_hash}
    print(json.dumps(output, ensure_ascii=True, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
