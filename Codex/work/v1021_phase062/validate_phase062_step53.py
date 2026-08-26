#!/usr/bin/env python3
"""Validate Phase 062 Step 53 content, staged boundary, and persistence."""

from __future__ import annotations

import argparse
import ast
import copy
import functools
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Iterable


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json"
RESULT = ROOT / "Codex/results/PHASE_062_STEP_053_STATMECH_TST_REDERIVATION_RESULT.md"
BUILDER = ROOT / "Codex/work/v1021_phase062/build_phase062_step53_statmech_tst.py"
VALIDATOR = ROOT / "Codex/work/v1021_phase062/validate_phase062_step53.py"
ACTIVE_LEDGER = ROOT / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
PARENT_LEDGER = ROOT / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
HANDOVER = ROOT / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "51ccba6c248a3e710e1a4ddd6017c18043f8a7a2"
Q2_COMMIT = "1635bc97fb7bd9c3fabc720e91bf09e5ba31798f"
Q2_PARENT = "b4e939b0547cd4bf73bca30abe10fd164954c277"
Q3_COMMIT = "c7420915dfae8ef076319737bddcc532a86d9505"
SUBJECT = "audit(phase062): rederive v1021 statmech tst"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
R = 8.31446261815324
F = 96485.33212
KB = 1.380649e-23
H = 6.62607015e-34

EXACT_PATHS = [
    "Codex/work/v1021_phase062/build_phase062_step53_statmech_tst.py",
    "Codex/work/v1021_phase062/validate_phase062_step53.py",
    "Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json",
    "Codex/results/PHASE_062_STEP_053_STATMECH_TST_REDERIVATION_RESULT.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
]

SOURCE_SPECS = {
    "Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex": (442, "8982a25beb3b58d406a684cb6a92906e06d1095e", "469f9de88fdedb33c6932e0b75642eab0412b6a05d0167849497cae9d60db765"),
    "Claude/docs/v1.0.21/_sections/ch2_appB_codemap.tex": (74, "e5b3f836d054983e43b74e64b98c1a52dcf05b45", "6c11234e9bf0c275299fcc845993e184e98e5c819f949bb9cb1e6d7920ecf88c"),
    "Claude/docs/v1.0.21/_sections/ch2_sec05_mixing.tex": (243, "93c444066debda6e8baf81b36fe570e7b6e36d2b", "a463f7070892f253e51a5bf8aa1f57ee7cf822079433a46f6a2a909fbd37432c"),
    "Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex": (378, "e97708808c244bc114cffc570f4866419fe2b1e8", "b619a5b8fe7cabe59371c995384331ffa7d1d6e30bc33db0c3c2bd2853d73d17"),
    "Claude/docs/v1.0.21/_sections/ch1_sec08_lag.tex": (131, "909f6d3bce10bef59b4532a4b2b3f7570a8f0631", "4835e52fd35de70d25054c95b0eb078947502afa19259b79c5691a53cbb2f038"),
    "Claude/docs/v1.0.21/_sections/ch1_bib.tex": (64, "dc4ca0780618d5710fd04e74ea87707738ffceba", "dc58338a8abd45116d846c0053ed41265d45b0f37852fafe93b8ecd7488d651d"),
    "Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md": (37, "2d23088e094d93a28b687788b9ac03fa0ab5520c", "b0092e4313ecd228904e865cd93bc00215b7a3740bdc65a3353f05e333f686de"),
    "Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md": (19, "ee86e4a8e74dea13cd01dc8fb8de36bb7119bf12", "b67870551a414f991badf85309da31cca208c77cc85b7399badead1fc1048472"),
    "Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md": (37, "64bdca8830a491e10d45c30fe9d992bb334afe03", "a61856800cf5fa0247ef794c559337ff6c48f1801105ef13647ce625edd2b838"),
}

EXPECTED_TOP = {
    "artifact_kind", "authority_boundary", "claim_rows", "equation_inventory", "findings",
    "gate", "generated_date", "git", "grand_canonical_derivation", "negative_control_contract",
    "patches", "phase", "schema_version", "snapshot_evidence", "source_attestations",
    "source_spans", "status", "step", "summary", "tst_rederivation",
}

EXPECTED_CLAIMS = {
    "P062-S53-GC-001": ("CONDITIONAL_ASSUMPTIONS", "PRESERVE"),
    "P062-S53-GC-002": ("CONFIRMED_INTERNAL_DERIVATION", "PRESERVE"),
    "P062-S53-GC-003": ("CONFIRMED_INTERNAL_DERIVATION", "PRESERVE"),
    "P062-S53-GC-004": ("CONFIRMED_INTERNAL_DERIVATION", "PRESERVE"),
    "P062-S53-GC-005": ("CONFIRMED_INTERNAL_DERIVATION", "PRESERVE"),
    "P062-S53-GC-006": ("CONDITIONAL_ASSUMPTIONS", "CORRECT"),
    "P062-S53-GC-007": ("CONFLICTING", "CORRECT"),
    "P062-S53-GC-008": ("NOT_DERIVED", "UNVERIFIED"),
    "P062-S53-GC-009": ("CONFIRMED_INTERNAL_DERIVATION", "PRESERVE"),
    "P062-S53-GC-010": ("NOT_DERIVED", "CORRECT"),
    "P062-S53-GC-011": ("NOT_DERIVED", "REJECT"),
    "P062-S53-GC-012": ("CONFLICTING", "CORRECT"),
    "P062-S53-GC-013": ("CONDITIONAL_ASSUMPTIONS", "CORRECT"),
    "P062-S53-GC-014": ("CONFLICTING", "CORRECT"),
    "P062-S53-TST-001": ("CONDITIONAL_ASSUMPTIONS", "PRESERVE"),
    "P062-S53-TST-002": ("CONDITIONAL_ASSUMPTIONS", "PRESERVE"),
    "P062-S53-TST-003": ("CONFLICTING", "CORRECT"),
    "P062-S53-TST-004": ("CONDITIONAL_ASSUMPTIONS", "CORRECT"),
    "P062-S53-TST-005": ("CONDITIONAL_ASSUMPTIONS", "PRESERVE"),
    "P062-S53-TST-006": ("CONFLICTING", "CORRECT"),
    "P062-S53-TST-007": ("CONFLICTING", "CORRECT"),
    "P062-S53-TST-008": ("NOT_DERIVED", "UNVERIFIED"),
    "P062-S53-TST-009": ("NOT_DERIVED", "UNVERIFIED"),
    "P062-S53-TST-010": ("NOT_DERIVED", "REJECT"),
    "P062-S53-TST-011": ("CONFLICTING", "CORRECT"),
    "P062-S53-TST-012": ("CONFLICTING", "CORRECT"),
    "P062-S53-TST-013": ("CONFLICTING", "CORRECT"),
}

EXPECTED_CLAIM_SHA256 = {
    "P062-S53-GC-001": "b381c236313d5d67d217121f10332e5cfefdc5c3c7b4f3a78c5682b31a2bad94",
    "P062-S53-GC-002": "d211ecbadd3660a4507a0b154dff69a0e7839feca44c360c88c50b9938727732",
    "P062-S53-GC-003": "e60e63c60affead7ae97f2830dfae420bd57ee3e2b0da10c256f9b712478e605",
    "P062-S53-GC-004": "18e635ca53a770ac6a44ec9e0f80fb60511d682852d7a70c5fe346a60e97e95e",
    "P062-S53-GC-005": "3526e5477eb5aae1b18350f48ab8e3cbcad602311e1fcba3fa781f9a8535cf00",
    "P062-S53-GC-006": "6bfb5c9f417bcbfd19df5dccf8ae4b2aabaddbad56a864bb7e6657a37425849f",
    "P062-S53-GC-007": "8a68f471ebd4231386fda84248a425cd487b769f9e4c84938c63f98cf85dc0ce",
    "P062-S53-GC-008": "1acc2036cc6e7798f828732cad237813d2d836396d163f145ce47032820ed564",
    "P062-S53-GC-009": "fe54364698f876f2f96c9d0c7143acfc57f220c5dd0169f7404a3ab1aba66db2",
    "P062-S53-GC-010": "0ef3f35da84c377fa3007e3dec76783c3f8f3f5dbb73da3406096bbebd3bdd13",
    "P062-S53-GC-011": "d73fea9715ff36acacfbc5def4e3cca19466521012645a8d8878af2b2d9a027f",
    "P062-S53-GC-012": "c16e288fc4953dc707bf89e0e3ac2f992079197dad8e82c2dadfc5af44f23772",
    "P062-S53-GC-013": "9e30db7f1144942762e48528cac12be9d66c9390c741a6750e5a6f7b52c1028f",
    "P062-S53-GC-014": "27a06fe115f3dabecb535e4ef6a75f191aa30e9142d24458fcf46670efeb4ba6",
    "P062-S53-TST-001": "290f763285cac2e37c939735a3016f8a1bcbdd2fde3870856d32e93d733d1dbf",
    "P062-S53-TST-002": "4125bf1c6bb9e2c0e9b4a5972dc5d0ea494477ecb79f93941db43d9a0d55bb57",
    "P062-S53-TST-003": "7ecc69ed9343602ad75b9f267fc306f2220948e85fb5d9338f5e1e301ff4ebd2",
    "P062-S53-TST-004": "3aec02561e606cb2d286f661f7bf488d8d65699d59c6978303815dcd05f5cc4e",
    "P062-S53-TST-005": "43800f378c1c591093b9eff4ac3521fd209c7b3b72e45bbf375ea925af8832c8",
    "P062-S53-TST-006": "9cd9c3dbce9046d0d119e21d945e34c279ecd00d6e7028f710eaea0cb38482c1",
    "P062-S53-TST-007": "3129a37245cc65e864af11d3e59046cc72bd28024882bf3798f387fc603cc8b2",
    "P062-S53-TST-008": "4a905094bf0a9f657692deb6ecd384ecb92582f0a29c8fbf8686a2dbb330d096",
    "P062-S53-TST-009": "a404914bec05ab7b2b5bf1359b22d414c24abcfc655cf481cf72ea5fd2c2743f",
    "P062-S53-TST-010": "2a0817cf9417450de6f8314430eaafd09b6edb116d737d798a4d84ac7fb5b9d1",
    "P062-S53-TST-011": "05ba50c55f7587c65b33fba79e5a8ee856fee39acadc9223c5f4161bfbe51b19",
    "P062-S53-TST-012": "3ab61c060428302db723349dd1ac051cd9ef8e0eb62dedda0e2a064d9a6b1a8c",
    "P062-S53-TST-013": "2f9f3ad40c525bfabfdaf58403496564606e2255012ccbb87ecdadbe7455e408",
}

EXPECTED_SPANS = {
    "Q2-SIGN": ("Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex", 139, 221, "chemical/electrical potential sign convention and single-class logistic"),
    "Q2-MULTICLASS": ("Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex", 280, 390, "complete Q2 multiclass addition including assumptions, equations, proofs and guards"),
    "Q2-LADDER": ("Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex", 433, 439, "Part 0 ladder cross-reference"),
    "Q2-CODEMAP": ("Claude/docs/v1.0.21/_sections/ch2_appB_codemap.tex", 12, 25, "historical eq:implicit and unique-root implementation bridge"),
    "Q2-MIXING": ("Claude/docs/v1.0.21/_sections/ch2_sec05_mixing.tex", 12, 35, "Chapter 2 implicit balance and derivative bridge"),
    "Q2-CHANGE": ("Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md", 7, 13, "Q2 change-control rows"),
    "Q2-EXEC": ("Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md", 7, 11, "Q2 process row"),
    "Q2-REF": ("Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md", 1, 19, "Q2 source-ledger claim and authority ceiling"),
    "Q3-CORE": ("Claude/docs/v1.0.21/_sections/ch1_sec05_width.tex", 11, 121, "Q3 Eyring/TST equations, assumptions, citations, prose and guards"),
    "Q3-LAG": ("Claude/docs/v1.0.21/_sections/ch1_sec08_lag.tex", 88, 105, "Q3-to-lag bridge and activation H/S use"),
    "Q3-BIB": ("Claude/docs/v1.0.21/_sections/ch1_bib.tex", 5, 15, "Q3 cited bibliography entries"),
    "Q3-CHANGE": ("Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md", 7, 16, "Q3 change-control rows"),
    "Q3-EXEC": ("Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md", 7, 12, "Q3 process row"),
    "Q3-REF": ("Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md", 1, 19, "Q3 source-ledger claim and authority ceiling"),
}

EXPECTED_SECTION_SHA256 = {
    "equation_inventory": "4f43a6ba4cd1fd42a6a1b907e4ad959d618520187627d5c2cdbc5188dc2d9a62",
    "grand_canonical_derivation": "c67954e4933bdce9216bd46952248e7463755b00f493e9a10ca62495a064de7c",
    "tst_rederivation": "22d52956015a596a4dd32fc1176bb434085c76a377ea83a3f2ceb35a48a64465",
    "findings": "64f5fe87803c6cf8a1e704289117ac1542e8519ef71e6dc99321591bfc19b0f4",
    "summary": "75640db46e6993e2633390531182bae7fd5db371e081e8edf1c6201aaa8fe547",
    "negative_control_contract": "638673231f2fc572feb02e2b43a1482310da6879cb7752b1af6acd74277ccabe",
    "patches": "29a4cd4f0762df583a725249dd246de28ba603f5605f6511ae2bf86a3577cbb9",
}

EXPECTED_ARTIFACT_SHA256 = "934be5273a91578b712d3ab44ef96eebb4cf7645973ec101b4e233b49426de16"
EXPECTED_RESULT_SHA256 = "9e96ee4729d888af8c96369fbc5006e3dc4dd7dd0f7ce7cae3904895ce0a85e1"
EXPECTED_BUILDER_SHA256 = "a37b2b2acbaa1666f2cf50a2ea6fcd3042f438ca43e5a0e35806f0676bcc3fbd"
EXPECTED_BUILDER_AST_SHA256 = {
    (3, 12): "ef84608c6d2ea4bdf6fd95d569015d7d91e188ab32974d65e2b5e0a6da60fbcc",
    (3, 14): "740dae609019d94ab3c3fa0565a9e412f6159f14cae5994d73316c04ce4d2bc4",
}
EXPECTED_CONTROL_SHA256 = {
    "active_ledger": "e93cb71a225fc9578852fd76a7814db57d2b8a80b0c9e3635cc3ef6ddc150bcc",
    "parent_ledger": "f5b7a082ee5ecb96f96920c4098fbff299f3109909182eae77aba171fa22e7f7",
    "handover": "a062a0280d07c16ab22b0ed885d4b10b58c789ed1f8dd70b0baae51142a45fc7",
}

EXPECTED_SUMMARY = {
    "claims": 27,
    "derivation_state_counts": {"CONDITIONAL_ASSUMPTIONS": 7, "CONFIRMED_INTERNAL_DERIVATION": 5, "CONFLICTING": 9, "NOT_DERIVED": 6},
    "equations": 12,
    "findings": {"P0": 0, "P1": 5, "P2": 5},
    "next_step": 54,
    "snapshot_nodes": 2285,
    "source_disposition_counts": {"CORRECT": 13, "PRESERVE": 9, "REJECT": 2, "UNVERIFIED": 3},
    "source_files_read_full": 9,
    "source_lines_read_full": 1425,
    "source_spans": 14,
}


def run(args: list[str], *, timeout: int = 30, check: bool = True, binary: bool = False) -> bytes | str:
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=timeout)
    if check and proc.returncode != 0:
        raise RuntimeError(f"command failed {args!r}: {proc.stderr.decode('utf-8', 'replace')}")
    return proc.stdout if binary else proc.stdout.decode("utf-8", "strict").strip()


@functools.lru_cache(maxsize=None)
def git(*args: str, binary: bool = False) -> bytes | str:
    return run(["git", *args], binary=binary)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return sha256(raw)


def strict_load(raw: bytes) -> Any:
    def hook(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate key {key}")
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=hook, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"non-finite {value}")))


def traverse(value: Any) -> tuple[int, int, list[str]]:
    nodes = 0
    max_depth = 0
    errors: list[str] = []
    stack = [(value, 0, "$")]
    while stack:
        item, depth, path = stack.pop()
        nodes += 1
        max_depth = max(max_depth, depth)
        if isinstance(item, float) and not math.isfinite(item):
            errors.append(f"{path}: non-finite")
        elif isinstance(item, dict):
            stack.extend((child, depth + 1, f"{path}.{key}") for key, child in item.items())
        elif isinstance(item, list):
            stack.extend((child, depth + 1, f"{path}[{index}]") for index, child in enumerate(item))
    return nodes, max_depth, errors


def close(actual: Any, expected: float, tol: float) -> bool:
    return isinstance(actual, (int, float)) and math.isfinite(float(actual)) and abs(float(actual) - expected) <= tol


def claim_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = data.get("claim_rows")
    if not isinstance(rows, list):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("claim_id"), str) and row["claim_id"] not in out:
            out[row["claim_id"]] = row
    return out


def independent_microstates(V: float, T: float, weights: list[int], energies: list[float]) -> tuple[float, float]:
    site_energies = [energy for count, energy in zip(weights, energies) for _ in range(count)]
    mu = -F * V
    z = 0.0
    n1 = 0.0
    n2 = 0.0
    for mask in range(1 << len(site_energies)):
        n = mask.bit_count()
        energy = sum(site_energies[i] for i in range(len(site_energies)) if mask & (1 << i))
        weight = math.exp(-(energy - mu * n) / (R * T))
        z += weight
        n1 += n * weight
        n2 += n * n * weight
    mean = n1 / z
    variance = n2 / z - mean * mean
    return mean, variance


def independent_coupled(mu: float, T: float, e1: float, e2: float, interaction: float) -> tuple[float, float]:
    rows = []
    for n1 in (0, 1):
        for n2 in (0, 1):
            n = n1 + n2
            energy = e1 * n1 + e2 * n2 + interaction * n1 * n2
            rows.append((n, math.exp(-(energy - mu * n) / (R * T))))
    z = sum(w for _, w in rows)
    mean = sum(n * w for n, w in rows) / z
    variance = sum(n * n * w for n, w in rows) / z - mean * mean
    return mean, variance


def source_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rows = data.get("source_attestations", [])
    if not isinstance(rows, list) or len(rows) != len(SOURCE_SPECS):
        return ["source_attestation_count"]
    if any(not isinstance(row, dict) for row in rows):
        return ["source_attestation_schema"]
    paths = [row.get("path") for row in rows]
    if len(set(paths)) != len(paths) or set(paths) != set(SOURCE_SPECS):
        errors.append("source_attestation_identity")
    by_path = {row.get("path"): row for row in rows}
    decoded: dict[str, list[str]] = {}
    for path, (line_count, blob, raw_sha) in SOURCE_SPECS.items():
        raw = git("show", f"{BASELINE}:{path}", binary=True)
        assert isinstance(raw, bytes)
        lines = raw.decode("utf-8", "strict").splitlines()
        decoded[path] = lines
        row = by_path.get(path, {})
        actual_blob = git("rev-parse", f"{BASELINE}:{path}")
        if len(lines) != line_count or actual_blob != blob or sha256(raw) != raw_sha:
            errors.append(f"frozen_source:{path}")
        if row != {"commit": BASELINE, "decoding": "UTF-8_STRICT", "git_blob": blob, "path": path, "physical_lines": line_count, "raw_sha256": raw_sha, "read_end": line_count, "read_start": 1, "read_state": "READ_FULL"}:
            errors.append(f"source_attestation:{path}")
    spans = data.get("source_spans", [])
    if not isinstance(spans, list) or len(spans) != len(EXPECTED_SPANS):
        errors.append("source_span_count")
    else:
        if any(not isinstance(row, dict) for row in spans):
            return errors + ["source_span_schema"]
        span_ids = [row.get("span_id") for row in spans]
        if len(set(span_ids)) != len(span_ids) or set(span_ids) != set(EXPECTED_SPANS):
            errors.append("source_span_identity")
        for row in spans:
            sid, path = row.get("span_id"), row.get("path")
            expected = EXPECTED_SPANS.get(sid)
            if expected is None:
                continue
            expected_path, expected_start, expected_end, expected_purpose = expected
            if set(row) != {"span_id", "path", "start_line", "end_line", "line_count", "purpose", "excerpt_sha256", "excerpt"}:
                errors.append(f"source_span_schema:{sid}")
                continue
            if (path, row.get("start_line"), row.get("end_line"), row.get("purpose")) != expected:
                errors.append(f"source_span_metadata:{sid}")
                continue
            start, end = row.get("start_line"), row.get("end_line")
            if path != expected_path or start != expected_start or end != expected_end or row.get("purpose") != expected_purpose or path not in decoded:
                errors.append(f"source_span_metadata:{sid}")
                continue
            if start < 1 or end > len(decoded[path]) or start > end:
                errors.append(f"source_span_range:{sid}")
                continue
            excerpt = "\n".join(decoded[path][start - 1:end]) + "\n"
            if row.get("excerpt") != excerpt or row.get("excerpt_sha256") != sha256(excerpt.encode("utf-8")) or row.get("line_count") != end - start + 1:
                errors.append(f"source_span_body:{sid}")
    return errors


def snapshot_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "Q2": (Q2_COMMIT, "Claude/docs/v1.0.21/results/snapshot_v1021_q2.json"),
        "Q3": (Q3_COMMIT, "Claude/docs/v1.0.21/results/snapshot_v1021_q3.json"),
    }
    rows = data.get("snapshot_evidence", [])
    if not isinstance(rows, list) or len(rows) != 2:
        return ["snapshot_count"]
    if any(not isinstance(row, dict) for row in rows) or [row.get("phase") for row in rows] != ["Q2", "Q3"]:
        errors.append("snapshot_identity_set")
    by_phase = {row.get("phase"): row for row in rows if isinstance(row, dict)}
    for phase, (commit, path) in expected.items():
        row = by_phase.get(phase, {})
        raw = git("show", f"{commit}:{path}", binary=True)
        assert isinstance(raw, bytes)
        parsed = strict_load(raw)
        nodes, depth, finite_errors = traverse(parsed)
        if finite_errors:
            errors.append(f"snapshot_finite:{phase}")
        stored = row.get("traversal", {})
        if row.get("commit") != commit or row.get("path") != path or row.get("git_blob") != git("rev-parse", f"{commit}:{path}") or row.get("raw_sha256") != sha256(raw) or row.get("physical_lines") != len(raw.splitlines()) or row.get("strict_parse") is not True:
            errors.append(f"snapshot_identity:{phase}")
        if stored.get("nodes") != nodes or stored.get("max_depth") != depth or row.get("authority") != "STRUCTURAL_DIFF_ONLY_NOT_SCIENTIFIC_TRUTH":
            errors.append(f"snapshot_traversal:{phase}")
    patches = data.get("patches", [])
    if not isinstance(patches, list) or len(patches) != 2 or any(not isinstance(row, dict) for row in patches):
        return errors + ["patch_cardinality"]
    if [row.get("phase") for row in patches] != ["Q2", "Q3"]:
        errors.append("patch_identity_set")
    patch_map = {row.get("phase"): row for row in patches if isinstance(row, dict)}
    for phase, parent, commit in (("Q2", Q2_PARENT, Q2_COMMIT), ("Q3", Q2_COMMIT, Q3_COMMIT)):
        raw = git("diff", "--no-ext-diff", "--unified=0", parent, commit, binary=True)
        assert isinstance(raw, bytes)
        row = patch_map.get(phase, {})
        if row != {"phase": phase, "parent": parent, "commit": commit, "diff_sha256": sha256(raw)}:
            errors.append(f"patch:{phase}")
    return errors


def semantic_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(data) != EXPECTED_TOP:
        errors.append("top_schema")
    if data.get("schema_version") != "1.0.0" or data.get("artifact_kind") != "PHASE_062_STEP_053_STATMECH_TST_REDERIVATION" or data.get("phase") != 62 or data.get("step") != 53:
        errors.append("identity")
    if data.get("status") != "PASS_WITH_CONCERNS" or data.get("gate") != "PASS_P062_STEP53_STATMECH_TST_REDERIVATION":
        errors.append("gate")
    authority = data.get("authority_boundary", {})
    expected_authority = {"internal_derivation_and_frozen_source_alignment": True, "external_scientific_truth": False, "external_material_truth": False, "external_experimental_truth": False, "primary_reference_proposition_support": False, "code_runtime_validation": False, "claude_files_modified": False}
    if authority != expected_authority:
        errors.append("external_authority")
    g = data.get("git", {})
    if g.get("baseline_commit") != BASELINE or g.get("q2_commit") != Q2_COMMIT or g.get("q3_commit") != Q3_COMMIT or g.get("q2_parent") != Q2_PARENT or g.get("q3_parent") != Q2_COMMIT or g.get("expected_precommit_parent") != EXPECTED_PARENT or g.get("containing_commit") != "PENDING_AT_PRECOMMIT_BY_DESIGN" or g.get("commit_subject") != SUBJECT:
        errors.append("git_contract")
    errors.extend(source_errors(data))
    errors.extend(snapshot_errors(data))

    for section, expected_hash in EXPECTED_SECTION_SHA256.items():
        try:
            if canonical_sha256(data.get(section)) != expected_hash:
                errors.append(f"section_semantics:{section}")
        except (TypeError, ValueError):
            errors.append(f"section_semantics:{section}")

    inv = data.get("equation_inventory", [])
    labels = [row.get("label") for row in inv if isinstance(row, dict)] if isinstance(inv, list) else []
    expected_labels = ["eq:sm-mc-factor", "eq:sm-mc-occ", "UNNUMBERED_Q2_CAPACITY_IDENTITY", "eq:sm-mc-balance", "eq:sm-mc-fluc", "eq:implicit", "eq:tst-qrc", "eq:tst-freq", "eq:tst-rate", "eq:tst-dG", "eq:tst-box", "eq:Lqmid2/eq:Lqfull"]
    if labels != expected_labels:
        errors.append("equation_denominator")
    if not isinstance(inv, list) or len(inv) != 12 or any(not isinstance(row, dict) for row in inv) or canonical_sha256(inv) != EXPECTED_SECTION_SHA256["equation_inventory"]:
        errors.append("equation_semantics")

    claim_rows = data.get("claim_rows", [])
    claims = claim_map(data)
    claim_ids = [row.get("claim_id") for row in claim_rows if isinstance(row, dict)] if isinstance(claim_rows, list) else []
    if not isinstance(claim_rows, list) or len(claim_rows) != len(EXPECTED_CLAIMS) or len(set(claim_ids)) != len(claim_ids) or claim_ids != list(EXPECTED_CLAIMS) or set(claims) != set(EXPECTED_CLAIMS):
        errors.append("claim_identity")
    for cid, expected in EXPECTED_CLAIMS.items():
        row = claims.get(cid, {})
        if (row.get("derivation_state"), row.get("source_disposition")) != expected:
            errors.append(f"claim_state:{cid}")
        if row.get("external_support_state") != "UNVERIFIED_EXTERNAL" or row.get("external_scientific_truth") is not False or row.get("external_material_truth") is not False:
            errors.append(f"claim_external:{cid}")
        canonical = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
        if set(row) != {"claim", "claim_id", "conditions_or_correction", "derivation_state", "external_material_truth", "external_scientific_truth", "external_support_state", "source_disposition", "source_span_id"} or sha256(canonical) != EXPECTED_CLAIM_SHA256[cid]:
            errors.append(f"claim_semantics:{cid}")

    gc = data.get("grand_canonical_derivation", {})
    if "dmu/dV=-F" not in gc.get("sign_convention", ""):
        errors.append("wrong_electrical_sign")
    if "Omega=0" not in gc.get("interacting_mean_field_susceptibility", "") or "C;" not in gc.get("capacity_units", "") or gc.get("q2_display_denominator") != {"labeled_snapshot_blocks": 4, "total_q2_added_displays": 5, "unnumbered_capacity_displays": 1}:
        errors.append("grand_contract")
    p = gc.get("numeric_probe", {})
    m = p.get("multiclass", {})
    weights = m.get("weights_Mj")
    energies = m.get("energies_J_per_mol")
    V = m.get("root_V")
    T = p.get("declared_domain", {}).get("T_K")
    target = m.get("target_xbar")
    if weights != [2.0, 3.0, 5.0] or energies != [-4000.0, 0.0, 6000.0] or not isinstance(V, (int, float)) or T != 298.15 or target != 0.41:
        errors.append("missing_class_weight")
    else:
        mean, variance = independent_microstates(float(V), float(T), [2, 3, 5], energies)
        residual = 1.0 - mean / 10.0 - target
        derivative = F * variance / (R * T * 10.0)
        h = 1.0e-7
        mp, _ = independent_microstates(float(V) + h, float(T), [2, 3, 5], energies)
        mm, _ = independent_microstates(float(V) - h, float(T), [2, 3, 5], energies)
        fd = ((1.0 - mp / 10.0) - (1.0 - mm / 10.0)) / (2.0 * h)
        if not close(m.get("normalized_residual"), residual, 2e-13) or not close(m.get("analytic_dresidual_dV_per_V"), derivative, 2e-11) or not close(m.get("finite_difference_dresidual_dV_per_V"), fd, 2e-8) or derivative <= 0:
            errors.append("multiclass_numeric")
    single = p.get("single_class", {})
    closed = (R * 298.15 * math.log(0.37 / 0.63) - 1250.0) / F
    if not close(single.get("closed_root_V"), closed, 1e-14) or not close(single.get("numeric_root_V"), closed, 1e-13):
        errors.append("single_class")
    zero = p.get("zero_weight", {})
    if not close(zero.get("root_with_zero_weight_V"), zero.get("root_after_removal_V", math.inf), 1e-13) or zero.get("all_zero_weights") != "INVALID_NORMALIZATION_NO_EXISTENCE_STATEMENT":
        errors.append("zero_weight")
    dup = p.get("duplicate_energy", {})
    if not close(dup.get("unmerged_root_V"), dup.get("merged_root_V", math.inf), 1e-13) or dup.get("root_uniqueness") != "PRESERVED" or dup.get("parameter_identifiability") != "NOT_IDENTIFIABLE_FROM_ROOT_ALONE":
        errors.append("duplicate_energy")
    degeneracy = p.get("degeneracy", {})
    expected_shift = -R * 298.15 * math.log(4.0)
    if degeneracy.get("occupied_to_empty_ratio") != 4.0 or not close(degeneracy.get("effective_energy_shift_J_per_mol"), expected_shift, 1e-12) or degeneracy.get("rule") != "finite positive degeneracy is absorbed into effective site free energy and preserves monotonicity":
        errors.append("degeneracy")
    finite = p.get("finite_domain", {})
    if finite.get("outside_target_has_bracket") is not False or not (finite.get("image_xbar_min", 1) < finite.get("image_xbar_max", 0) < finite.get("outside_target_xbar", 0)):
        errors.append("finite_domain")
    if p.get("saturation", {}).get("all_variance_zero") != "NON_STRICT_NO_UNIQUENESS_GUARANTEE" or p.get("saturation", {}).get("xbar_zero_or_one_finite_root") is not False:
        errors.append("variance_zero_uniqueness")
    coupled = p.get("coupled_exact", {})
    mean, variance = independent_coupled(500.0, 298.15, -600.0, 900.0, 2400.0)
    if not close(coupled.get("mean_N"), mean, 1e-13) or not close(coupled.get("variance_N"), variance, 1e-13) or coupled.get("product_formula_absolute_error", 0) <= 1e-3 or claims.get("P062-S53-GC-007", {}).get("source_disposition") != "CORRECT":
        errors.append("hidden_interaction")
    if p.get("nonconvex_mean_field", {}).get("unstable_branch_negative_slope") is not True or p.get("nonconvex_mean_field", {}).get("dmu_dtheta_at_half_J_per_mol", 0) >= 0:
        errors.append("hidden_nonconvexity")

    tst = data.get("tst_rederivation", {}).get("numeric_probe", {})
    td = tst.get("temperature_dependent_partition_ratio", {})
    TT = 298.15
    a, b, e0 = 1.5, 200.0, 40000.0
    Lp = a / TT - b / (TT * TT)
    Lpp = -a / (TT * TT) + 2 * b / TT**3
    S = R * TT * Lp
    Hact = e0 + R * TT * TT * Lp
    Cp = R * (2 * TT * Lp + TT * TT * Lpp)
    if not close(td.get("source_R_lnK_J_per_molK"), 0.0, 1e-15) or not close(td.get("correct_delta_S_J_per_molK"), S, 1e-12) or not close(td.get("delta_H_J_per_mol"), Hact, 1e-9) or not close(td.get("delta_Cp_J_per_molK"), Cp, 1e-10) or td.get("entropy_fd_absolute_error", 1) > 1e-7 or td.get("heat_capacity_fd_absolute_error", 1) > 1e-6:
        errors.append("entropy_temperature_derivative")
    const = tst.get("constant_partition_ratio_limit", {})
    if const.get("dlnK_dT_per_K") != 0.0 or not close(const.get("delta_S_J_per_molK"), R * math.log(2.5), 1e-13) or not close(const.get("R_lnK_J_per_molK"), R * math.log(2.5), 1e-13):
        errors.append("constant_partition_ratio")
    rate = tst.get("rate", {})
    kappa = rate.get("kappa")
    expected_rate = 0.37 * KB * TT / H * math.exp(-e0 / (R * TT))
    expected_no_kappa = expected_rate / 0.37
    expected_dlnk = 1.0 / TT + Lp + e0 / (R * TT * TT)
    if (kappa != 0.37 or not close(rate.get("k_TST_per_s"), expected_rate, 1e-8)
            or not close(rate.get("k_HS_per_s"), expected_rate, 1e-8)
            or not close(rate.get("k_if_kappa_omitted_per_s"), expected_no_kappa, 1e-8)
            or not close(rate.get("relative_omission_factor"), 1.0 / 0.37, 1e-12)
            or not close(rate.get("analytic_dlnk_dT_per_K"), expected_dlnk, 1e-14)
            or not close(rate.get("finite_difference_dlnk_dT_per_K"), expected_dlnk, 1e-9)
            or rate.get("HS_roundtrip_relative_error", 1) > 1e-13 or rate.get("dlnk_derivative_absolute_error", 1) > 1e-8):
        errors.append("omitted_transmission_coefficient")
    flux = tst.get("reaction_coordinate_flux", {})
    mass = 4.0e-26
    delta = 1.0e-10
    expected_qrc = math.sqrt(2.0 * math.pi * mass * KB * TT) * delta / H
    expected_moment = math.sqrt(KB * TT / (2.0 * math.pi * mass))
    expected_conditional = 2.0 * expected_moment
    if (not close(flux.get("q_rc"), expected_qrc, 1e-14)
            or not close(flux.get("one_sided_flux_moment_m_per_s"), expected_moment, 1e-12)
            or not close(flux.get("conditional_positive_mean_speed_m_per_s"), expected_conditional, 1e-12)
            or not close(flux.get("conditional_to_flux_moment_ratio"), 2.0, 1e-15)
            or flux.get("relative_error", 1) > 1e-14
            or not close(flux.get("flux_product_per_s"), KB * TT / H, 1e-2)
            or not close(flux.get("kBT_over_h_per_s"), KB * TT / H, 1e-2)):
        errors.append("qrc_cancellation")
    high_t = tst.get("classical_harmonic_high_temperature", {})
    if (high_t.get("reactant_stable_mode_count") != 3
            or high_t.get("reduced_transition_state_stable_mode_count") != 2
            or high_t.get("T1_K") != 600.0 or high_t.get("T2_K") != 1200.0
            or high_t.get("normalized_K_dagger_T1") != 1.0
            or not close(high_t.get("normalized_K_dagger_T2"), 0.5, 1e-15)
            or high_t.get("K_dagger_T_exponent") != -1.0
            or not close(high_t.get("T_times_K_T1_K"), high_t.get("T_times_K_T2_K", math.inf), 1e-15)
            or high_t.get("T_times_K_relative_error") != 0.0
            or high_t.get("equal_partition_ratio_prefactor_T_exponent") != 1.0
            or high_t.get("equal_partition_ratio_is_constant_prefactor_Arrhenius") is not False):
        errors.append("high_temperature_mode_power")
    if claims.get("P062-S53-TST-008", {}).get("derivation_state") != "NOT_DERIVED" or claims.get("P062-S53-TST-008", {}).get("source_disposition") != "UNVERIFIED" or "electrode overpotential/current law" not in data.get("tst_rederivation", {}).get("scope_separation", {}).get("not_derived", []):
        errors.append("state_free_electrode_barrier")
    if claims.get("P062-S53-TST-010", {}).get("derivation_state") != "NOT_DERIVED" or claims.get("P062-S53-TST-010", {}).get("source_disposition") != "REJECT":
        errors.append("tst_to_peak_width_promotion")

    summary = data.get("summary", {})
    if summary != EXPECTED_SUMMARY:
        errors.append("summary")
    findings = data.get("findings", [])
    if not isinstance(findings, list) or len(findings) != 10 or [row.get("severity") for row in findings].count("P1") != 5 or [row.get("severity") for row in findings].count("P2") != 5 or canonical_sha256(findings) != EXPECTED_SECTION_SHA256["findings"]:
        errors.append("finding_rows")
    required = ["wrong_electrical_sign", "missing_class_weight", "variance_zero_uniqueness", "hidden_interaction", "constant_partition_ratio", "omitted_transmission_coefficient", "state_free_electrode_barrier", "tst_to_peak_width_promotion"]
    if data.get("negative_control_contract") != required:
        errors.append("negative_contract")
    return errors


def named_check_results(data: dict[str, Any], diagnostics: list[str]) -> tuple[dict[str, bool], dict[str, bool]]:
    """Map each advertised check name to an executed predicate, never a constant count."""
    bad = set(diagnostics)
    gc = data.get("grand_canonical_derivation", {})
    tst_root = data.get("tst_rederivation", {})
    tst = tst_root.get("numeric_probe", {}) if isinstance(tst_root, dict) else {}
    thermo = tst.get("thermodynamic_identities", {}) if isinstance(tst, dict) else {}
    flux = tst.get("reaction_coordinate_flux", {}) if isinstance(tst, dict) else {}
    high_t = tst.get("classical_harmonic_high_temperature", {}) if isinstance(tst, dict) else {}
    symbolic = {
        "single_site_partition": gc.get("single_site") == "Xi_1j=1+exp[-(eps_j-mu)/(R*T)]",
        "product_factorization_scope": gc.get("product") == "Xi=product_j Xi_1j^Mj only for independent/factorized sites",
        "occupation_derivative": gc.get("occupation") == "theta_j=1/[1+exp((eps_j-mu)/(R*T))]",
        "capacity_balance": gc.get("capacity_constraint") == "sum_j Qj*xi_j=Q*xbar with xi_j=1-theta_j, Qj=(F/NA)Mj, Q=sum_j Qj",
        "electrical_sign": "wrong_electrical_sign" not in bad,
        "variance_response": gc.get("response_identity") == "d<N>/dmu_molar=Var(N)/(R*T); per-particle mu uses beta=1/(k_B*T)",
        "strictness_condition": gc.get("uniqueness") == "strict only where the total weighted variance is positive",
        "existence_vs_uniqueness": "finite domains only cover their endpoint image" in gc.get("existence", ""),
        "coupled_variance_identity": "general equilibrium variance identity survives" in gc.get("numeric_probe", {}).get("coupled_exact", {}).get("rule", ""),
        "mean_field_susceptibility": gc.get("interacting_mean_field_susceptibility") == "dtheta/dmu=theta(1-theta)/[R*T-2*Omega*theta(1-theta)]; it is not the Bernoulli response unless Omega=0 or the effective field is held fixed",
        "tst_general_rate": tst_root.get("general_rate") == "single-site pseudo-first-order k(T) [s^-1]=kappa(T)*(k_B*T/h)*K_dagger(T;consistent standard state)*exp[-DeltaE0(T)/(R*T)]",
        "qrc_flux_interpretation": "one-sided moment" in flux.get("rule", "") and "not E[v|v>0]" in flux.get("rule", ""),
        "activation_thermodynamics": thermo == {
            "DeltaG": "DeltaE0(T)-R*T*lnK(T)",
            "DeltaS": "-DeltaE0'(T)+R*lnK(T)+R*T*dlnK/dT",
            "DeltaH": "DeltaE0(T)-T*DeltaE0'(T)+R*T^2*dlnK/dT",
            "DeltaCp": "-T*DeltaE0''(T)+R*(2*T*dlnK/dT+T^2*d2lnK/dT2)",
            "Arrhenius_slope_energy": "E_a=DeltaH_dagger+R*T+R*T^2*dln(kappa)/dT",
        },
        "high_temperature_mode_power": high_t.get("K_dagger_T_exponent") == -1.0 and high_t.get("equal_partition_ratio_prefactor_T_exponent") == 1.0,
        "claim_disposition_registry": "claim_identity" not in bad and not any(code.startswith("claim_semantics:") for code in bad),
    }
    numeric = {
        "multiclass_root_and_residual": "multiclass_numeric" not in bad,
        "microstate_mean_and_variance": "multiclass_numeric" not in bad,
        "central_difference_response": "multiclass_numeric" not in bad,
        "single_class_inverse": "single_class" not in bad,
        "zero_weight": "zero_weight" not in bad,
        "duplicate_energy": "duplicate_energy" not in bad,
        "saturation": "variance_zero_uniqueness" not in bad,
        "finite_domain": "finite_domain" not in bad,
        "degeneracy_shift": "degeneracy" not in bad,
        "coupled_sites": "hidden_interaction" not in bad,
        "nonconvex_branch": "hidden_nonconvexity" not in bad,
        "constant_partition_ratio": "constant_partition_ratio" not in bad,
        "temperature_dependent_entropy": "entropy_temperature_derivative" not in bad,
        "heat_capacity_finite_difference": "entropy_temperature_derivative" not in bad,
        "tst_rate_roundtrip": "omitted_transmission_coefficient" not in bad,
        "kappa_scaling": "omitted_transmission_coefficient" not in bad,
        "qrc_flux_cancellation": "qrc_cancellation" not in bad,
        "conditional_mean_factor_two": "qrc_cancellation" not in bad,
        "harmonic_high_temperature_power": "high_temperature_mode_power" not in bad,
        "dlnk_arrhenius_slope": "omitted_transmission_coefficient" not in bad,
    }
    return symbolic, numeric


def markdown_section(text: str, heading: str) -> str:
    match = re.search(rf"(?m)^{re.escape(heading)}\s*$", text)
    if not match:
        return ""
    start = match.end()
    following = re.search(r"(?m)^##\s+", text[start:])
    return text[start:start + following.start()] if following else text[start:]


def markdown_table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.startswith("|") or re.fullmatch(r"\|(?:\s*:?-+:?\s*\|)+", line) is not None:
            continue
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows[1:] if rows else []


def row_has_conflicting_terminal(row: list[str]) -> bool:
    return any(re.search(r"\b(?:FAIL|BLOCKED|CONDITIONAL)\b", cell) is not None for cell in row)


def current_markdown_documents() -> dict[str, str]:
    return {
        "result": RESULT.read_text(encoding="utf-8"),
        "active_ledger": ACTIVE_LEDGER.read_text(encoding="utf-8"),
        "parent_ledger": PARENT_LEDGER.read_text(encoding="utf-8"),
        "handover": HANDOVER.read_text(encoding="utf-8"),
    }


def markdown_errors(documents: dict[str, str] | None = None) -> list[str]:
    errors: list[str] = []
    docs = current_markdown_documents() if documents is None else documents
    result = docs.get("result", "")
    expected_claim_ids = list(EXPECTED_CLAIMS)
    claim_rows = markdown_table_rows(markdown_section(result, "## 주장별 판정"))
    observed_claim_ids = [row[0].strip("`") for row in claim_rows if len(row) == 4]
    result_contract = (
        sha256(result.encode("utf-8")) == EXPECTED_RESULT_SHA256
        and result.splitlines()[:1] == ["# Phase 062 Step 053 — v1.0.21 대정준 전하 보존·TST 재유도 결과"]
        and all(result.count(section) == 1 for section in ("## 판정", "## 입력과 전문 검독", "## Q2 — 다클래스 대정준 재유도", "## Q3 — TST 재유도와 교정", "## 주장별 판정", "## Findings and routing", "## 검증과 다음 단계"))
        and len(claim_rows) == len(expected_claim_ids)
        and all(len(row) == 4 for row in claim_rows)
        and observed_claim_ids == expected_claim_ids
        and "P0 `0`; P1 `5`; P2 `5`" in result
        and result.count("PASS_P062_STEP53_STATMECH_TST_REDERIVATION") >= 1
        and result.count("PENDING_AT_PRECOMMIT_BY_DESIGN") == 1
        and "FAIL_P062_STEP53" not in result and "BLOCKED_P062_STEP53" not in result
    )
    if not result_contract:
        errors.append("result_contract")

    active = docs.get("active_ledger", "")
    active_phase_rows = [row for row in markdown_table_rows(markdown_section(active, "## Execution Ledger")) if row and row[0] == "062"]
    active_commit_rows = [row for row in markdown_table_rows(markdown_section(active, "## Commit and Push Ledger")) if row and row[0] == "Step 53"]
    active_contract = (
        sha256(active.encode("utf-8")) == EXPECTED_CONTROL_SHA256["active_ledger"]
        and active.splitlines()[:1] == ["# Phase 059–090 Canonical Completion Execution Ledger"]
        and len(active_phase_rows) == 1 and len(active_phase_rows[0]) == 10
        and active_phase_rows[0][1:5] == ["52–57", "plan activation; Step 52 persistence complete; Step 53 precommit complete; Steps 54–57.2 pending", "v1.0.21 reaudit", "IN_PROGRESS"]
        and all(token in active_phase_rows[0][8] for token in ("51ccba6c248a3e710e1a4ddd6017c18043f8a7a2", "PASS_P062_STEP52_PERSISTENCE", "PASS_P062_STEP53_STATMECH_TST_REDERIVATION", "0/5/5", "PENDING_AT_PRECOMMIT_BY_DESIGN"))
        and active_phase_rows[0][9] == "Step 54 blocked until `PASS_P062_STEP53_PERSISTENCE`"
        and not row_has_conflicting_terminal(active_phase_rows[0])
        and len(active_commit_rows) == 1 and len(active_commit_rows[0]) == 6
        and active_commit_rows[0][2:5] == ["`PENDING_AT_PRECOMMIT_BY_DESIGN`", "exact-seven checkpoint prepared", "verify after atomic commit"]
        and all(token in active_commit_rows[0][5] for token in (SUBJECT, EXPECTED_PARENT, "0/5/5", "PASS_P062_STEP53_STATMECH_TST_REDERIVATION", "PASS_P062_STEP53_PERSISTENCE"))
        and all(token in markdown_section(active, "## Next Exact Step") for token in (SUBJECT, EXPECTED_PARENT, "seven declared paths", "PASS_P062_STEP53_PERSISTENCE", "Step 54"))
    )
    if not active_contract:
        errors.append("active_ledger_contract")

    parent = docs.get("parent_ledger", "")
    parent_rows = [row for row in markdown_table_rows(markdown_section(parent, "## Ledger")) if row and row[0] == "062"]
    parent_contract = (
        sha256(parent.encode("utf-8")) == EXPECTED_CONTROL_SHA256["parent_ledger"]
        and parent.splitlines()[:1] == ["# Phase 055–069 전체 계보 재감사 실행 원장"]
        and len(parent_rows) == 1 and len(parent_rows[0]) == 12
        and parent_rows[0][1:7] == ["52–57", "plan activation; Step 52 persistence complete; Step 53 precommit complete; Steps 54–57.2 pending", "lineage E", "v1.0.21 재감사", "IN_PROGRESS", "`Codex/plans/2026-08-27-phase062-v1021-lineage-detailed-plan.md`"]
        and all(token in parent_rows[0][9] for token in ("51ccba6c248a3e710e1a4ddd6017c18043f8a7a2", "PASS_P062_STEP52_PERSISTENCE", "PASS_P062_STEP53_STATMECH_TST_REDERIVATION", "0/5/5", "PENDING_AT_PRECOMMIT_BY_DESIGN"))
        and parent_rows[0][10] == "`PASS_P062_LINEAGE_E` pending"
        and parent_rows[0][11] == "Step 54 after Step 53 persistence; `PASS_P062_STEP53_PERSISTENCE` required"
        and not row_has_conflicting_terminal(parent_rows[0])
    )
    if not parent_contract:
        errors.append("parent_ledger_contract")

    handover = docs.get("handover", "")
    handover_rows = markdown_table_rows(markdown_section(handover, "## Handover Chain"))
    step52 = [row for row in handover_rows if row and row[0] == "Phase 062 Step 52"]
    step53 = [row for row in handover_rows if row and row[0] == "Phase 062 Step 53"]
    handover_contract = (
        sha256(handover.encode("utf-8")) == EXPECTED_CONTROL_SHA256["handover"]
        and handover.splitlines()[:1] == ["# Project Anode Fit Canonical Completion Active Handover"]
        and handover.count("14. 현재 Phase 상태: Phase 062 `IN_PROGRESS`, Current checkpoint: Step 53 precommit Gate") == 1
        and handover.count("15. 현재 result: `Codex/results/PHASE_062_STEP_053_STATMECH_TST_REDERIVATION_RESULT.md`") == 1
        and handover.count("16. 현재 machine evidence: `Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json`") == 1
        and "Current checkpoint: Step 52 precommit Gate" not in handover
        and len(step52) == 1 and len(step52[0]) == 4
        and all(token in step52[0][2] for token in ("51ccba6c248a3e710e1a4ddd6017c18043f8a7a2", "PASS_P062_STEP52_PERSISTENCE"))
        and "PENDING_AT_PRECOMMIT_BY_DESIGN" not in step52[0][2]
        and len(step53) == 1 and len(step53[0]) == 4
        and all(token in step53[0][2] for token in ("PASS_P062_STEP53_STATMECH_TST_REDERIVATION", "0/5/5", "PENDING_AT_PRECOMMIT_BY_DESIGN"))
        and all(token in step53[0][3] for token in ("PASS_P062_STEP53_PERSISTENCE", "Step 54"))
        and not row_has_conflicting_terminal(step52[0]) and not row_has_conflicting_terminal(step53[0])
        and all(token in markdown_section(handover, "## Exact Next Action") for token in (SUBJECT, EXPECTED_PARENT, "exact-seven", "PASS_P062_STEP53_PERSISTENCE", "Step 54"))
        and "P0/P1/P2 `0/3/5`" not in handover
    )
    if not handover_contract:
        errors.append("handover_contract")
    return errors


def markdown_negative_probes() -> tuple[int, int, list[str]]:
    docs = current_markdown_documents()
    token_only = f"Step 53 {SUBJECT} {EXPECTED_PARENT} PASS_P062_STEP53_STATMECH_TST_REDERIVATION PENDING_AT_PRECOMMIT_BY_DESIGN PASS_P062_STEP53_PERSISTENCE Step 54 0/5/5"
    fixtures: list[tuple[str, str, str, Callable[[str], str]]] = [
        ("result-token-only", "result_contract", "result", lambda text: token_only),
        ("result-old-count", "result_contract", "result", lambda text: text.replace("P1 `5`; P2 `5`", "P1 `3`; P2 `5`", 1)),
        ("result-duplicate-claim", "result_contract", "result", lambda text: re.sub(r"(?m)^(\| `P062-S53-GC-001` \|.*)$", r"\1\n\1", text, count=1)),
        ("active-duplicate-phase", "active_ledger_contract", "active_ledger", lambda text: re.sub(r"(?m)^(\| 062 \|.*)$", r"\1\n\1", text, count=1)),
        ("active-conflicting-terminal", "active_ledger_contract", "active_ledger", lambda text: text.replace("| IN_PROGRESS | `Codex/plans/2026-08-27-phase062", "| FAIL | `Codex/plans/2026-08-27-phase062", 1)),
        ("parent-duplicate-phase", "parent_ledger_contract", "parent_ledger", lambda text: re.sub(r"(?m)^(\| 062 \|.*)$", r"\1\n\1", text, count=1)),
        ("handover-stale-top", "handover_contract", "handover", lambda text: text.replace("Current checkpoint: Step 53 precommit Gate", "Current checkpoint: Step 52 precommit Gate", 1)),
        ("handover-duplicate-step53", "handover_contract", "handover", lambda text: re.sub(r"(?m)^(\| Phase 062 Step 53 \|.*)$", r"\1\n\1", text, count=1)),
        ("handover-step52-pending", "handover_contract", "handover", lambda text: text.replace("exact-eight commit `51ccba6c248a3e710e1a4ddd6017c18043f8a7a2`", "exact-eight containing commit `PENDING_AT_PRECOMMIT_BY_DESIGN`", 1)),
    ]
    escaped: list[str] = []
    for name, wanted, document, mutation in fixtures:
        mutated = dict(docs)
        mutated[document] = mutation(mutated[document])
        observed = set(markdown_errors(mutated))
        if wanted not in observed:
            escaped.append(name)
    return len(fixtures) - len(escaped), len(fixtures), escaped


def builder_static_errors(raw_override: bytes | None = None) -> list[str]:
    errors: list[str] = []
    raw = BUILDER.read_bytes() if raw_override is None else raw_override
    normalized_raw = raw.replace(b"\r\n", b"\n")
    if sha256(normalized_raw) != EXPECTED_BUILDER_SHA256:
        errors.append("builder_source_identity")
    try:
        tree = ast.parse(normalized_raw.decode("utf-8", "strict"))
    except Exception:
        return ["builder_ast"]
    runtime = (sys.version_info.major, sys.version_info.minor)
    expected_ast = EXPECTED_BUILDER_AST_SHA256.get(runtime)
    ast_sha = sha256(ast.dump(tree, annotate_fields=True, include_attributes=False).encode("utf-8"))
    if expected_ast is None or ast_sha != expected_ast:
        errors.append("builder_ast_identity")
    allowed_imports = {"__future__", "argparse", "copy", "hashlib", "json", "math", "subprocess", "pathlib", "typing"}
    banned_calls = {"eval", "exec", "compile", "__import__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(alias.name.split(".")[0] not in allowed_imports for alias in node.names):
            errors.append("builder_import_policy")
        if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] not in allowed_imports:
            errors.append("builder_import_policy")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in banned_calls:
            errors.append("builder_dynamic_execution")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
            errors.append("builder_write_target")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {
            "write_bytes", "write_text", "open", "unlink", "rename", "replace", "rmdir", "mkdir",
            "touch", "chmod", "lchmod", "symlink_to", "hardlink_to", "link_to",
        }:
            receiver = node.func.value
            if not (node.func.attr == "write_bytes" and isinstance(receiver, ast.Name) and receiver.id in {"OUTPUT_JSON", "OUTPUT_MD"}):
                errors.append("builder_write_target")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "run_git":
            if not node.args or not isinstance(node.args[0], ast.Constant) or node.args[0].value not in {"show", "rev-parse", "diff"}:
                errors.append("builder_git_policy")
    run_git_functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "run_git"]
    authorized_subprocess_calls: set[int] = set()
    if len(run_git_functions) == 1:
        for node in ast.walk(run_git_functions[0]):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" and node.func.attr == "run":
                authorized_subprocess_calls.add(id(node))
                if not node.args or not isinstance(node.args[0], ast.List) or not node.args[0].elts or not isinstance(node.args[0].elts[0], ast.Constant) or node.args[0].elts[0].value != "git":
                    errors.append("builder_subprocess_policy")
    all_subprocess_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess"
        and node.func.attr in {"run", "Popen", "call", "check_call", "check_output"}
    ]
    if len(authorized_subprocess_calls) != 1 or len(all_subprocess_calls) != 1 or any(id(node) not in authorized_subprocess_calls for node in all_subprocess_calls):
        errors.append("builder_subprocess_policy")
    text = normalized_raw.decode("utf-8", "strict")
    if re.search(r"Claude/docs/[^\n'\"]+\.py", text):
        errors.append("builder_production_import")
    if re.search(r"https?://|git\s+(?:add|commit|push|checkout|switch|reset|clean)\b", text, re.IGNORECASE):
        errors.append("builder_network_or_git_write")
    return sorted(set(errors))


def builder_policy_negative_probes() -> tuple[int, int, list[str]]:
    base = BUILDER.read_bytes()
    fixtures = [
        ("unlink", b'\nPath("Codex/results/UNRELATED.md").unlink(missing_ok=True)\n', "builder_write_target"),
        ("rename", b'\nPath("a").rename("b")\n', "builder_write_target"),
        ("unrelated-write", b'\nPath("Codex/results/UNRELATED.md").write_bytes(b"x")\n', "builder_write_target"),
        ("builtin-open", b'\nopen("Codex/results/UNRELATED.md", "w")\n', "builder_write_target"),
        ("network-import", b'\nimport socket\n', "builder_import_policy"),
        ("git-push", b'\nrun_git("push")\n', "builder_git_policy"),
        ("foreign-subprocess", b'\nsubprocess.run(["cmd", "/c", "echo unsafe"])\n', "builder_subprocess_policy"),
        ("dynamic-exec", b'\nexec("pass")\n', "builder_dynamic_execution"),
        ("getattr-subprocess", b'\ngetattr(subprocess, "run")(["git", "push"])\n', "builder_source_identity"),
        ("aliased-subprocess", b'\nrunner = subprocess.run\nrunner(["git", "push"])\n', "builder_source_identity"),
        ("getattr-unlink", b'\ngetattr(Path("Codex/results/UNRELATED.md"), "unlink")(missing_ok=True)\n', "builder_source_identity"),
    ]
    escaped: list[str] = []
    for name, suffix, wanted in fixtures:
        if wanted not in builder_static_errors(base + suffix):
            escaped.append(name)
    return len(fixtures) - len(escaped), len(fixtures), escaped


def builder_portability_probe() -> bool:
    normalized = BUILDER.read_bytes().replace(b"\r\n", b"\n")
    crlf = normalized.replace(b"\n", b"\r\n")
    return builder_static_errors(crlf) == []


def negative_probes(data: dict[str, Any]) -> tuple[int, int, list[str]]:
    probes: list[tuple[str, Callable[[dict[str, Any]], None], str]] = []
    def add(name: str, mutation: Callable[[dict[str, Any]], None], wanted: str) -> None:
        probes.append((name, mutation, wanted))
    def row(d: dict[str, Any], cid: str) -> dict[str, Any]:
        return next(r for r in d["claim_rows"] if r["claim_id"] == cid)
    def move_span_with_consistent_body(d: dict[str, Any]) -> None:
        target = d["source_spans"][0]
        path = target["path"]
        raw = git("show", f"{BASELINE}:{path}", binary=True)
        assert isinstance(raw, bytes)
        excerpt = raw.decode("utf-8", "strict").splitlines()[0] + "\n"
        target.update({"start_line": 1, "end_line": 1, "line_count": 1, "purpose": "tampered but self-consistent", "excerpt": excerpt, "excerpt_sha256": sha256(excerpt.encode("utf-8"))})
    add("wrong-sign", lambda d: d["grand_canonical_derivation"].__setitem__("sign_convention", "mu rises with V"), "wrong_electrical_sign")
    add("missing-weight", lambda d: d["grand_canonical_derivation"]["numeric_probe"]["multiclass"].__setitem__("weights_Mj", [1.0, 1.0, 1.0]), "missing_class_weight")
    add("variance-zero-unique", lambda d: d["grand_canonical_derivation"]["numeric_probe"]["saturation"].__setitem__("all_variance_zero", "STRICT_UNIQUE"), "variance_zero_uniqueness")
    add("hidden-interaction", lambda d: row(d, "P062-S53-GC-007").__setitem__("source_disposition", "PRESERVE"), "hidden_interaction")
    add("hidden-nonconvex", lambda d: d["grand_canonical_derivation"]["numeric_probe"]["nonconvex_mean_field"].__setitem__("unstable_branch_negative_slope", False), "hidden_nonconvexity")
    add("constant-ratio", lambda d: d["tst_rederivation"]["numeric_probe"]["constant_partition_ratio_limit"].__setitem__("dlnK_dT_per_K", 1.0), "constant_partition_ratio")
    add("omit-kappa", lambda d: d["tst_rederivation"]["numeric_probe"]["rate"].__setitem__("kappa", 1.0), "omitted_transmission_coefficient")
    add("state-free-electrode", lambda d: row(d, "P062-S53-TST-008").__setitem__("derivation_state", "CONFIRMED_INTERNAL_DERIVATION"), "state_free_electrode_barrier")
    add("tst-width", lambda d: row(d, "P062-S53-TST-010").__setitem__("source_disposition", "PRESERVE"), "tst_to_peak_width_promotion")
    add("external-promotion", lambda d: row(d, "P062-S53-TST-009").__setitem__("external_scientific_truth", True), "claim_external:P062-S53-TST-009")
    add("equation-drop", lambda d: d["equation_inventory"].pop(), "equation_denominator")
    add("equation-semantics", lambda d: d["equation_inventory"][0].update({"path": "WRONG", "lines": [1, 1], "internal_result": "WRONG"}), "equation_semantics")
    add("source-span-body", lambda d: d["source_spans"][0].__setitem__("excerpt", "tampered"), "source_span_body:Q2-SIGN")
    add("source-span-metadata", move_span_with_consistent_body, "source_span_metadata:Q2-SIGN")
    add("source-sha", lambda d: d["source_attestations"][0].__setitem__("raw_sha256", "0" * 64), "source_attestation:Claude/docs/v1.0.21/_sections/ch1_sec02b_part0.tex")
    add("snapshot-authority", lambda d: d["snapshot_evidence"][0].__setitem__("authority", "SCIENTIFIC_TRUTH"), "snapshot_traversal:Q2")
    add("single-class", lambda d: d["grand_canonical_derivation"]["numeric_probe"]["single_class"].__setitem__("closed_root_V", 0.0), "single_class")
    add("zero-weight", lambda d: d["grand_canonical_derivation"]["numeric_probe"]["zero_weight"].__setitem__("all_zero_weights", "UNIQUE"), "zero_weight")
    add("duplicate-energy", lambda d: d["grand_canonical_derivation"]["numeric_probe"]["duplicate_energy"].__setitem__("parameter_identifiability", "IDENTIFIED"), "duplicate_energy")
    add("degeneracy", lambda d: d["grand_canonical_derivation"]["numeric_probe"]["degeneracy"].__setitem__("effective_energy_shift_J_per_mol", 0.0), "degeneracy")
    add("gc-symbolic", lambda d: d["grand_canonical_derivation"].__setitem__("single_site", "WRONG"), "section_semantics:grand_canonical_derivation")
    add("entropy", lambda d: d["tst_rederivation"]["numeric_probe"]["temperature_dependent_partition_ratio"].__setitem__("correct_delta_S_J_per_molK", 0.0), "entropy_temperature_derivative")
    add("flux", lambda d: d["tst_rederivation"]["numeric_probe"]["reaction_coordinate_flux"].__setitem__("relative_error", 1.0), "qrc_cancellation")
    add("flux-conditional", lambda d: d["tst_rederivation"]["numeric_probe"]["reaction_coordinate_flux"].__setitem__("conditional_to_flux_moment_ratio", 1.0), "qrc_cancellation")
    add("high-temperature", lambda d: d["tst_rederivation"]["numeric_probe"]["classical_harmonic_high_temperature"].__setitem__("K_dagger_T_exponent", 0.0), "high_temperature_mode_power")
    add("tst-rate-value", lambda d: d["tst_rederivation"]["numeric_probe"]["rate"].__setitem__("k_TST_per_s", 1e99), "omitted_transmission_coefficient")
    add("tst-thermo", lambda d: d["tst_rederivation"]["numeric_probe"]["thermodynamic_identities"].__setitem__("DeltaS", "WRONG"), "section_semantics:tst_rederivation")
    add("finding-body", lambda d: d["findings"][0].__setitem__("summary", "WRONG"), "finding_rows")
    add("summary", lambda d: d["summary"].__setitem__("claims", 23), "summary")
    add("summary-state-counts", lambda d: d["summary"]["derivation_state_counts"].__setitem__("CONFLICTING", 0), "summary")
    add("extra-patch", lambda d: d["patches"].append(copy.deepcopy(d["patches"][0])), "patch_cardinality")
    add("duplicate-claim", lambda d: d["claim_rows"].append(copy.deepcopy(d["claim_rows"][0])), "claim_identity")
    escaped = []
    for name, mutation, wanted in probes:
        mutated = copy.deepcopy(data)
        mutation(mutated)
        diagnostics = semantic_errors(mutated)
        if wanted not in diagnostics:
            escaped.append(name)
    strict_cases = [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":1e999}', b'{"x":-1e999}']
    for index, raw in enumerate(strict_cases):
        try:
            value = strict_load(raw)
            _, _, finite_errors = traverse(value)
            if not finite_errors:
                escaped.append(f"strict-{index}")
        except (ValueError, json.JSONDecodeError):
            pass
    return len(probes) + len(strict_cases) - len(escaped), len(probes) + len(strict_cases), escaped


def staged_errors() -> list[str]:
    errors: list[str] = []
    if git("branch", "--show-current") != ACTIVE_BRANCH:
        errors.append("active_branch")
    if git("rev-parse", "HEAD") != EXPECTED_PARENT:
        errors.append("wrong_expected_parent")
    if git("rev-parse", "@{u}") != EXPECTED_PARENT:
        errors.append("wrong_precommit_upstream")
    if git("rev-parse", f"refs/heads/{PROTECTED_BRANCH}") != PROTECTED_TIP:
        errors.append("precommit_local_protected")
    staged = [line for line in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if line]
    if sorted(staged) != sorted(EXACT_PATHS):
        errors.append("exact_seven_staged")
    status = str(git("status", "--porcelain=v1", "--untracked-files=all")).splitlines()
    changed = sorted(line[3:].replace("\\", "/") for line in status if len(line) >= 4)
    if changed != sorted(EXACT_PATHS):
        errors.append("exact_seven_worktree")
    for path in EXACT_PATHS:
        staged_raw = git("show", f":{path}", binary=True)
        if not isinstance(staged_raw, bytes) or staged_raw != (ROOT / path).read_bytes().replace(b"\r\n", b"\n"):
            errors.append(f"staged_worktree_bytes:{path}")
    try:
        git("diff", "--check")
    except RuntimeError:
        errors.append("worktree_diff_check")
    try:
        git("diff", "--cached", "--check")
    except RuntimeError:
        errors.append("cached_diff_check")
    remote_heads = live_remote_heads()
    if remote_heads.get(f"refs/heads/{ACTIVE_BRANCH}") != EXPECTED_PARENT:
        errors.append("precommit_live_active")
    if remote_heads.get(f"refs/heads/{PROTECTED_BRANCH}") != PROTECTED_TIP:
        errors.append("precommit_live_protected")
    if remote_heads.get("refs/heads/main") != MAIN_TIP:
        errors.append("precommit_live_main")
    if str(git("status", "--porcelain=v1", "--untracked-files=all", "--", "Claude")):
        errors.append("precommit_claude_drift")
    return errors


def live_remote_heads() -> dict[str, str]:
    output = str(git(
        "ls-remote", "--heads", "origin",
        f"refs/heads/{ACTIVE_BRANCH}", f"refs/heads/{PROTECTED_BRANCH}", "refs/heads/main",
    ))
    rows: dict[str, str] = {}
    for line in output.splitlines():
        fields = line.split()
        if len(fields) == 2:
            rows[fields[1]] = fields[0]
    return rows


def persistence_errors(expected_commit: str) -> list[str]:
    errors: list[str] = []
    if git("branch", "--show-current") != ACTIVE_BRANCH:
        errors.append("persistence_branch")
    head = str(git("rev-parse", "HEAD"))
    if head != expected_commit:
        errors.append("persistence_head")
        return errors
    if git("rev-parse", "HEAD^") != EXPECTED_PARENT:
        errors.append("persistence_parent")
    if git("show", "-s", "--format=%s", "HEAD") != SUBJECT:
        errors.append("persistence_subject")
    if git("rev-parse", f"refs/heads/{PROTECTED_BRANCH}") != PROTECTED_TIP:
        errors.append("persistence_local_protected")
    paths = [line for line in str(git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD")).splitlines() if line]
    if sorted(paths) != sorted(EXACT_PATHS):
        errors.append("persistence_paths")
    if str(git("status", "--porcelain=v1", "--untracked-files=all")):
        errors.append("persistence_dirty")
    remote_heads = live_remote_heads()
    if git("rev-parse", "@{u}") != head or git("rev-parse", f"origin/{ACTIVE_BRANCH}") != head or remote_heads.get(f"refs/heads/{ACTIVE_BRANCH}") != head:
        errors.append("persistence_active_remote")
    if remote_heads.get(f"refs/heads/{PROTECTED_BRANCH}") != PROTECTED_TIP:
        errors.append("persistence_protected_remote")
    if remote_heads.get("refs/heads/main") != MAIN_TIP:
        errors.append("persistence_main_remote")
    if str(git("status", "--porcelain=v1", "--untracked-files=all", "--", "Claude")):
        errors.append("persistence_claude_drift")
    try:
        git("diff", "HEAD^", "HEAD", "--check")
    except RuntimeError:
        errors.append("persistence_diff_check")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-only", action="store_true")
    parser.add_argument("--run-negative-probes", action="store_true")
    parser.add_argument("--determinism-check", action="store_true")
    parser.add_argument("--verify-staged", action="store_true")
    parser.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    errors: list[str] = []
    if args.verify_staged and args.verify_persistence:
        print("FAIL_P062_STEP53_STATMECH_TST_REDERIVATION mutually exclusive repository modes")
        return 2
    try:
        raw = ARTIFACT.read_bytes()
        if sha256(raw) != EXPECTED_ARTIFACT_SHA256:
            errors.append("artifact_sha256")
        data = strict_load(raw)
        nodes, depth, finite_errors = traverse(data)
        errors.extend(finite_errors)
        errors.extend(builder_static_errors())
        semantic_diagnostics = semantic_errors(data)
        errors.extend(semantic_diagnostics)
        errors.extend(markdown_errors())
        symbolic_checks, numeric_checks = named_check_results(data, semantic_diagnostics)
        symbolic_failures = [name for name, passed in symbolic_checks.items() if not passed]
        numeric_failures = [name for name, passed in numeric_checks.items() if not passed]
        errors.extend(f"symbolic_check:{name}" for name in symbolic_failures)
        errors.extend(f"numeric_check:{name}" for name in numeric_failures)
    except Exception as exc:
        print(f"FAIL_P062_STEP53_STATMECH_TST_REDERIVATION exception={exc}")
        return 1
    if args.run_negative_probes:
        passed, total, escaped = negative_probes(data)
        if escaped:
            errors.append(f"negative_escaped:{escaped}")
        print(f"PASS_P062_STEP53_NEGATIVE_CONTROLS {passed}/{total}" if not escaped else f"FAIL_P062_STEP53_NEGATIVE_CONTROLS {passed}/{total} escaped={escaped}")
        md_passed, md_total, md_escaped = markdown_negative_probes()
        if md_escaped:
            errors.append(f"markdown_negative_escaped:{md_escaped}")
        print(f"PASS_P062_STEP53_MARKDOWN_NEGATIVE_CONTROLS {md_passed}/{md_total}" if not md_escaped else f"FAIL_P062_STEP53_MARKDOWN_NEGATIVE_CONTROLS {md_passed}/{md_total} escaped={md_escaped}")
        policy_passed, policy_total, policy_escaped = builder_policy_negative_probes()
        if policy_escaped:
            errors.append(f"builder_policy_negative_escaped:{policy_escaped}")
        print(f"PASS_P062_STEP53_BUILDER_POLICY_NEGATIVE_CONTROLS {policy_passed}/{policy_total}" if not policy_escaped else f"FAIL_P062_STEP53_BUILDER_POLICY_NEGATIVE_CONTROLS {policy_passed}/{policy_total} escaped={policy_escaped}")
        portability_passed = builder_portability_probe()
        if not portability_passed:
            errors.append("builder_crlf_portability")
        print("PASS_P062_STEP53_BUILDER_PORTABILITY 1/1" if portability_passed else "FAIL_P062_STEP53_BUILDER_PORTABILITY 0/1")
    if args.determinism_check:
        det = 0
        for _ in range(2):
            proc = subprocess.run([sys.executable, str(BUILDER), "--check"], cwd=ROOT, capture_output=True, text=True, timeout=60)
            if proc.returncode == 0 and "PASS_P062_STEP53_BUILD_DETERMINISM" in proc.stdout:
                det += 1
        if det != 2:
            errors.append("determinism")
        print(f"PASS_P062_STEP53_DETERMINISM {det}/2" if det == 2 else f"FAIL_P062_STEP53_DETERMINISM {det}/2")
    if args.verify_staged:
        errors.extend(staged_errors())
        if not errors:
            print("PASS_P062_STEP53_STAGED")
    if args.verify_persistence:
        if not args.expected_commit or not re.fullmatch(r"[0-9a-f]{40}", args.expected_commit):
            errors.append("expected_commit_required")
        else:
            errors.extend(persistence_errors(args.expected_commit))
            if not errors:
                print("PASS_P062_STEP53_PERSISTENCE")

    symbolic_passed = len(symbolic_checks) - len(symbolic_failures)
    numeric_passed = len(numeric_checks) - len(numeric_failures)
    print(f"PASS_P062_STEP53_SYMBOLIC_CHECKS {symbolic_passed}/{len(symbolic_checks)}" if not symbolic_failures else f"FAIL_P062_STEP53_SYMBOLIC_CHECKS {symbolic_passed}/{len(symbolic_checks)} failed={symbolic_failures}")
    print(f"PASS_P062_STEP53_NUMERIC_CHECKS {numeric_passed}/{len(numeric_checks)}" if not numeric_failures else f"FAIL_P062_STEP53_NUMERIC_CHECKS {numeric_passed}/{len(numeric_checks)} failed={numeric_failures}")
    print(f"PASS_P062_STEP53_JSON_TRAVERSAL nodes={nodes} depth={depth}")
    if errors:
        print(f"FAIL_P062_STEP53_STATMECH_TST_REDERIVATION errors={len(errors)}")
        for error in errors[:80]:
            print(f"ERROR {error}")
        return 1
    print("PASS_P062_STEP53_STATMECH_TST_REDERIVATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
