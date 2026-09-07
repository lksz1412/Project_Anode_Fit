"""Immutable five-state target coverage and lossless carry validation."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
from reconcile_phase068_claims import strict_json, digest

BASE = "f9feef379d597d320cb5692ed2eda739a336d02f"
RESULT_PATH = "Codex/results/PHASE_068_STEP_097_FORK_DISPOSITION_RESULT.md"
REGISTER_PATH = "Codex/results/PHASE_068_FORK_DISPOSITION_REGISTER.json"
CARRY_PATH = "Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json"
INPUTS = {
    "PHASE_068_CLAUDE_FORK_DIFF_INVENTORY.json": "c050802be498cddcffccff3be814c59566dd4601",
    "PHASE_068_CLAUDE_FORK_FULL_READ_ATTESTATION.json": "bc4ae1018b7406014f5a08bf82dc2380c8e07a4f",
    "PHASE_068_CODEX_FORK_DIFF_INVENTORY.json": "c78e7ca1e1bbe6889f92f83e52d46798d4fb5c26",
    "PHASE_068_CODEX_FORK_FULL_READ_ATTESTATION.json": "183cc3535ae3968a5b0b7f79870a1f1dd05dbcb3",
    "PHASE_068_PHASE044_054_REAUDIT_MATRIX.json": "c5b6e65f1b4889f63d2e1b1f7b3e4b2b88e82931",
    "PHASE_068_U13_REGSOL_REDERIVATION.json": "7ecd6e86177cbb6a0f8632cb72f4247388d4c05e",
    "PHASE_068_CONFORMANCE_MODEL_ADJUDICATION.json": "bd3af86bf461b74d693bf41da12fdbe6c9a5db40",
    "PHASE_068_FORK_CONFLICT_MATRIX.json": "6d8da1b58832fa8ce55d3714b1eb591eb163dfa7",
    "PHASE_067_CARRY_FORWARD_DELTA.json": "996a9b621d657f4081197f1c34b536483c0234c1",
}
STATES = {"ADOPT", "REWRITE", "REFERENCE_ONLY", "REJECT", "UNVERIFIED"}


def collect(root):
    data = {}
    for name, expected_blob in INPUTS.items():
        raw = subprocess.run(["git", "show", BASE + ":Codex/results/" + name],
                             cwd=root, check=True, capture_output=True).stdout
        actual = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        if actual != expected_blob:
            raise ValueError("input blob: " + name)
        data[name] = strict_json(raw)
    targets, original = [], {}

    def add_record(name, selector, row, target_id, kind):
        source = {"commit": BASE, "path": "Codex/results/" + name,
                  "blob": INPUTS[name], "selector": selector, "record_sha256": digest(row)}
        targets.append({"target_id": target_id, "target_kind": kind, "source": source})
        original[target_id] = row

    name = "PHASE_068_FORK_CONFLICT_MATRIX.json"
    for i, row in enumerate(data[name]["rows"]):
        add_record(name, f"rows[{i}]", row, row["id"], row["kind"])
    for name, key in [("PHASE_068_CLAUDE_FORK_DIFF_INVENTORY.json", "findings"),
                      ("PHASE_068_CODEX_FORK_DIFF_INVENTORY.json", "source_findings")]:
        for i, row in enumerate(data[name][key]):
            add_record(name, f"{key}[{i}]", row, row["id"], "FORK_FINDING")
    name = "PHASE_067_CARRY_FORWARD_DELTA.json"
    prior = data[name]["active_obligations"]
    for i, row in enumerate(prior):
        add_record(name, f"active_obligations[{i}]", row, row["obligation_id"], "INHERITED_OBLIGATION")
    pool = {}

    def add_file(path, blob, occurrence):
        if path and blob and blob != "0" * 40:
            pool.setdefault((path, blob), []).append(occurrence)

    a = data["PHASE_068_CLAUDE_FORK_DIFF_INVENTORY.json"]
    at = data["PHASE_068_CLAUDE_FORK_FULL_READ_ATTESTATION.json"]
    b = data["PHASE_068_CODEX_FORK_DIFF_INVENTORY.json"]
    for i, row in enumerate(at["blob_occurrences"]):
        add_file(row["path"], row["blob"], f"claude_occurrences[{i}]")
    for i, row in enumerate(b["blob_occurrences"]):
        add_file(row["path"], row["blob"], f"codex_occurrences[{i}]")
    for claim in a["claims"]:
        for i, surface in enumerate(claim["claimant_surfaces"]):
            if surface["source_kind"] == "blob":
                add_file(surface["path"], surface["source_oid"], f"{claim['id']}-surface[{i}]")
    groups = [
        ("step93sources", data["PHASE_068_PHASE044_054_REAUDIT_MATRIX.json"]["sources"]),
        ("step94sources", data["PHASE_068_U13_REGSOL_REDERIVATION.json"]["legacy_candidate"]["sources"]),
        ("step95sources", data["PHASE_068_CONFORMANCE_MODEL_ADJUDICATION.json"]["source_identities"]),
    ]
    for prefix, group in groups:
        for i, row in enumerate(group):
            add_file(row["path"], row["blob"], f"{prefix}[{i}]")
    for i, ((path, blob), links) in enumerate(sorted(pool.items()), 1):
        target_id = f"FILE97-{i:03d}"
        row = {"id": target_id, "path": path, "blob": blob, "occurrence_links": links}
        targets.append({"target_id": target_id, "target_kind": "FILE_BLOB",
                        "source": {"path": path, "blob": blob, "record_sha256": digest(row)}})
        original[target_id] = row
    if len(prior) != 222 or len(pool) != 95 or len(targets) != 655:
        raise ValueError("input denominator")
    return targets, original, data


def nonempty(row, key):
    if not isinstance(row.get(key), str) or not row[key].strip():
        raise ValueError(key + ": " + str(row.get("target_id", row.get("obligation_id"))))


def validate_register(targets, rows):
    expected = {row["target_id"]: row for row in targets}
    ids = [row["target_id"] for row in rows]
    if len(expected) != len(targets) or len(set(ids)) != len(ids) or set(ids) != set(expected):
        raise ValueError("target coverage or duplicate")
    for row in rows:
        target = expected[row["target_id"]]
        if row["target_kind"] != target["target_kind"] or row["source"] != target["source"]:
            raise ValueError("source identity: " + row["target_id"])
        if row["disposition"] not in STATES:
            raise ValueError("disposition: " + row["target_id"])
        for key in ["rationale", "bounded_content", "canonical_owner",
                    "acceptance_criterion", "prohibited_promotion"]:
            nonempty(row, key)
        minimum_phase = 55 if row["target_kind"] == "INHERITED_OBLIGATION" else 68
        if type(row.get("target_phase")) is not int or not minimum_phase <= row["target_phase"] <= 90:
            raise ValueError("target_phase")
        if not isinstance(row.get("evidence"), list) or not row["evidence"]:
            raise ValueError("evidence")
        if not all(isinstance(item, str) and item.strip() for item in row["evidence"]):
            raise ValueError("evidence entry")
        links = row.get("relation_links")
        if (not isinstance(links, list) or any(item not in expected for item in links)
                or len(set(links)) != len(links) or row["target_id"] in links):
            raise ValueError("relation")
        if row.get("whole_commit_adoption") is not False:
            raise ValueError("whole-commit adoption")
    return dict(sorted(Counter(row["disposition"] for row in rows).items()))


def validate_carry(prior, carry, rows):
    inherited = carry["inherited_active"]
    original = {row["obligation_id"]: row for row in prior}
    current = {row["obligation_id"]: row for row in inherited}
    if len(current) != len(inherited) or digest(current) != digest(original):
        raise ValueError("inherited carry changed/lost/duplicated")
    active = dict(current)
    known_targets = {row["target_id"] for row in rows}
    for row in carry["new_obligations"]:
        oid = row["obligation_id"]
        if oid in active:
            raise ValueError("duplicate obligation")
        for key in ["canonical_owner", "acceptance_criterion"]:
            nonempty(row, key)
        if type(row.get("target_phase")) is not int or not 68 <= row["target_phase"] <= 90:
            raise ValueError("target_phase")
        if row.get("state") != "OPEN_CARRY" or row.get("external_authority_promoted") is not False:
            raise ValueError("new obligation state/authority")
        origins = row.get("origin_target_ids")
        if not isinstance(origins, list) or not origins or any(x not in known_targets for x in origins):
            raise ValueError("new obligation origin")
        active[oid] = row
    routes = carry["target_routes"]
    route_map = {row["target_id"]: row for row in routes}
    if len(route_map) != len(routes) or set(route_map) != known_targets:
        raise ValueError("target route coverage")
    for row in rows:
        route = route_map[row["target_id"]]
        links = route["obligation_ids"]
        if not isinstance(links, list) or len(set(links)) != len(links) or any(x not in active for x in links):
            raise ValueError("obligation route")
        if row["disposition"] in {"UNVERIFIED", "REWRITE", "REJECT"} and not links:
            raise ValueError("active route required")
        if (links and route["state"] != "ACTIVE") or (not links and route["state"] != "NOT_REQUIRED"):
            raise ValueError("route state")
    for obligation in carry["new_obligations"]:
        for target_id in obligation["origin_target_ids"]:
            if obligation["obligation_id"] not in route_map[target_id]["obligation_ids"]:
                raise ValueError("new obligation origin route")
    for row in carry["resolved_subpredicates"]:
        for key in ["resolution", "remaining_scope"]:
            nonempty(row, key)
        if not row.get("evidence") or not row.get("target_ids"):
            raise ValueError("resolved evidence")
        if any(x not in known_targets for x in row["target_ids"]):
            raise ValueError("resolved target")
    return {"inherited": len(inherited), "new": len(active) - len(inherited),
            "active": len(active), "target_routes": len(routes)}


def validate_result(root, artifact):
    if artifact["result_path"] != RESULT_PATH:
        raise ValueError("result path")
    raw = (root / RESULT_PATH).read_bytes().replace(b"\r\n", b"\n")
    result_hash = hashlib.sha256(raw).hexdigest()
    if result_hash != artifact["result_lf_sha256"]:
        raise ValueError("result identity")
    return result_hash


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    root = Path.cwd()
    targets, original, data = collect(root)
    if args.inventory:
        output = {"targets": targets, "original": original,
                  "inherited_active": data["PHASE_067_CARRY_FORWARD_DELTA.json"]["active_obligations"]}
    else:
        if not args.validate:
            parser.error("choose --inventory or --validate")
        register = strict_json((root / REGISTER_PATH).read_bytes())
        carry = strict_json((root / CARRY_PATH).read_bytes())
        if register["source_commit"] != BASE or carry["source_commit"] != BASE:
            raise ValueError("source commit")
        counts = validate_register(targets, register["rows"])
        summary = validate_carry(data["PHASE_067_CARRY_FORWARD_DELTA.json"]["active_obligations"],
                                 carry, register["rows"])
        result_hash = validate_result(root, register)
        if validate_result(root, carry) != result_hash or register["carry_sha256"] != digest(carry):
            raise ValueError("carry identity")
        output = {"gate": "PASS_P068_STEP97_DISPOSITION", "targets": len(targets),
                  "counts": counts, "carry": summary, "rows_sha256": digest(register["rows"]),
                  "carry_sha256": digest(carry), "result_lf_sha256": result_hash}
    print(json.dumps(output, ensure_ascii=True, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
