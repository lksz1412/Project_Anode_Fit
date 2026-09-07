#!/usr/bin/env python3
"""Validate Phase 068 Step 92 Codex-fork full-read evidence.

The validator reconstructs the fixed five-commit/six-edge graph directly from
Git objects.  It keeps genealogy events, net paths, blob occurrences, and
unique blob reads as separate denominators.  The one PDF is rendered from its
exact blob in an external temporary directory; the independent 28-page visual
review is recorded separately from machine rendering.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import struct
import subprocess
import sys
import tempfile
from typing import Any, Iterable
from collections import Counter


ROOT = Path(__file__).resolve().parents[3]
SCHEMA_INVENTORY = "P068-STEP92-CODEX-DIFF-1"
SCHEMA_ATTESTATION = "P068-STEP92-FULL-READ-1"
EXPECTED_PARENT = "fdcf509746c27d3bdca233b938222cb65466371a"
EXPECTED_SUBJECT = "audit(phase068): read codex fork history"
CONTENT_TERMINAL = "PASS_P068_STEP92_CODEX_FORK_READ"
PERSISTENCE_TERMINAL = "PASS_P068_STEP92_PERSISTENCE"
PRECOMMIT_MARKER = "P068_STEP92_CODEX_FORK_READ_PRECOMMIT"

ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
ACTIVE_LOCAL_REF = "refs/heads/" + ACTIVE_BRANCH
ACTIVE_TRACKING_REF = "refs/remotes/origin/" + ACTIVE_BRANCH
ACTIVE_LIVE_REF = "refs/heads/" + ACTIVE_BRANCH
ACTIVE_UPSTREAM = "origin/" + ACTIVE_BRANCH
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
PROTECTED_REF = "refs/remotes/origin/codex/lib-physics-endgame-v1025_2"
PROTECTED_LIVE_REF = "refs/heads/codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_REF = "refs/remotes/origin/main"
MAIN_LIVE_REF = "refs/heads/main"
MAIN_TIP = "f0c381bd6dc315ac75cbffa93dd86ce83a37949b"
CLAUDE_REF = "refs/remotes/origin/claude/version-1026-regsol-review-kl88j7"
CLAUDE_LIVE_REF = "refs/heads/claude/version-1026-regsol-review-kl88j7"
CLAUDE_TIP = "e3e1a634f34b711aa4803fd190fe9120f1755f13"
CODEX_REF = "refs/remotes/origin/codex/v1025_2-physics-conformance"
CODEX_LIVE_REF = "refs/heads/codex/v1025_2-physics-conformance"
CODEX_TIP = "11f90544865dd179739ca5bc5062b28c1078e504"
BASE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
ZERO = "0" * 40

COMMITS = (
    "2abf019c7fee9bebd84b49cc9530f6983b08a8fa",
    "eed5d4850215b22ea7775de3365cd3d3cbfc4414",
    "4316d8a5423d0ba229931a3c43c1f833fdc2fe1e",
    "30a874e906f2be72a36efaac7cb8fd8138e7b401",
    CODEX_TIP,
)
EXPECTED_PARENTS = {
    COMMITS[0]: ("ab196b292e14492b647f87a6c0d1d8c9ed0630ab",),
    COMMITS[1]: (COMMITS[0],),
    COMMITS[2]: (COMMITS[1], BASE),
    COMMITS[3]: (COMMITS[2],),
    COMMITS[4]: (COMMITS[3],),
}
EXPECTED_SUBJECTS = {
    COMMITS[0]: "feat: add v1.0.25.3 physics conformance baseline",
    COMMITS[1]: "plan: align conformance review with latest v1.0.25.2",
    COMMITS[2]: "Merge latest v1.0.25.2 lineage for review",
    COMMITS[3]: "docs: add latest v1.0.25.2 alignment review",
    COMMITS[4]: "docs: record latest review handover and verification",
}
EXPECTED_TREES = {
    COMMITS[0]: "592b76f2bdec09e04a92e5407fc5403b37aebe79",
    COMMITS[1]: "a209053ece54977edc96dc7a340ffb1735188383",
    COMMITS[2]: "7a057f6062d59eb6d92f073b3b1ea13370b7e364",
    COMMITS[3]: "8f3a8d1f050cafb8215f8c891fad3e6f8194c449",
    COMMITS[4]: "34cc6332317a96b53891da6c970bbe0dfb81698e",
    "ab196b292e14492b647f87a6c0d1d8c9ed0630ab": "2b66c64fb31c955ae65caf588ef65bd9ada9752a",
    BASE: "fd7f89d7c009f68be2edac6c3e792aa187689a33",
}
EXPECTED_COMMIT_CLOCKS = {
    COMMITS[0]: (1785147286, "+0900", 1785147286, "+0900"),
    COMMITS[1]: (1785151464, "+0800", 1785151464, "+0800"),
    COMMITS[2]: (1785151469, "+0800", 1785151469, "+0800"),
    COMMITS[3]: (1785152065, "+0800", 1785152065, "+0800"),
    COMMITS[4]: (1785152347, "+0800", 1785152347, "+0800"),
}
EDGE_SPECS = (
    ("E1", EXPECTED_PARENTS[COMMITS[0]][0], COMMITS[0], 58),
    ("E2", COMMITS[0], COMMITS[1], 1),
    ("E3", COMMITS[1], COMMITS[2], 6),
    ("E4", BASE, COMMITS[2], 59),
    ("E5", COMMITS[2], COMMITS[3], 8),
    ("E6", COMMITS[3], COMMITS[4], 3),
)
EDGE_RAW = {
    "E1": (9588, "4e3b48d12e3ac4b0eaa57d675e383384a4d6b51faf3b76b6b4b1bb9bd60bdf16", "5d06852990fb42c2238ea51e226501e5a2c0a6424d8c81e448f34385624aa741"),
    "E2": (169, "868569059554252fb594f6db640599c7f52c61db805f9dc08f93ba7568116151", "816c3537b3b55119bacf7de9f35321f613350f419e67a6827cca44e8c54d25b4"),
    "E3": (872, "1f51bae05f8b18b300943e4956bdb563bdb68301bbac9780b7cc28422479d7ff", "8b856ae5513b5dad64612dc2c319c04283f3ebe8b4e69b7b65988bcbb7b9be58"),
    "E4": (9757, "937675b288faafd48cedb6db36a9451a2756cedcc9e88685832db48f799e75dc", "90248e98b7269317e7de8f18b769052796b24054868899a5936a789658b474aa"),
    "E5": (1295, "b3ff1c5846c0a2d84602722f096bde4e09a0c0f84239a18eca86fe7d119b1513", "1e03241fa361f7ee1758e08820461080e30ec7537d4a184a6e9d336f03cbd519"),
    "E6": (493, "abc6de1fbd55ee9820af9800b2c59f5f5b5d99f4ef698c79bfbb3d2806c7c97e", "caba8fe220e2b5b13d10c7763e3cc5f8f194eaf7461ff50bb48a482f867300d6"),
}
NET_RAW = (11389, "f41d3ef025e7eacdf8f9a3590a50a893aac6c3232302693f93bfa7d8fa4d28f9", "66839983750759a6354325da2549cc4b5333c7353842e57e02226b8784529231")
E3_PATHS = (
    "Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md",
    "Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py",
    "Claude/docs/v1.0.25.2/_sections/ch1_sec05b_gr2L.tex",
    "Claude/docs/v1.0.25.2/_sections/ch1_sec18_inputs.tex",
    "Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md",
    "Claude/docs/v1.0.25.2/test_gates_v1024.py",
)

BUILDER = "Codex/work/v1025_phase068/build_phase068_step92.py"
VALIDATOR = "Codex/work/v1025_phase068/validate_phase068_step92.py"
INVENTORY = "Codex/results/PHASE_068_CODEX_FORK_DIFF_INVENTORY.json"
ATTESTATION = "Codex/results/PHASE_068_CODEX_FORK_FULL_READ_ATTESTATION.json"
RESULT = "Codex/results/PHASE_068_STEP_092_CODEX_FORK_REVIEW_RESULT.md"
PARENT_LEDGER = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
SOURCE_IDENTITY_HEADING = "The current pre-JSON implementation identities are:"
FROZEN_BUILDER_IDENTITY = (2409, 68, "ade5c1bbab9cbac05d950b12572e471c494442f6450823d5efd5a587f94dc428")
EXACT_EIGHT = (BUILDER, VALIDATOR, INVENTORY, ATTESTATION, RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)
PRE_JSON_SIX = (BUILDER, VALIDATOR, RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)
GIT_ORDERED_EIGHT = tuple(sorted(EXACT_EIGHT))
EXPECTED_STATUS = {path: ("M" if path in {PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER} else "A") for path in EXACT_EIGHT}
EXPECTED_OLD_MODE = {path: ("100644" if EXPECTED_STATUS[path] == "M" else "000000") for path in EXACT_EIGHT}
PDF_PATH = "output/pdf/Anode_Physics_v1.0.25.3_conformance.pdf"
PDF_BLOB = "485274a7d17e5e332eda856758cb466b692d1c31"
PDF_SHA256 = "9832400c55df88874699a0eaaf0f392da6dcdcd82e9389990b25b62e07978f83"
PDF_VISUAL_ISSUE_PAGES = (4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28)

MAX_JSON_BYTES = 8_000_000
MAX_JSON_NODES = 600_000
MAX_JSON_DEPTH = 64
HEX40 = set("0123456789abcdef")
CONTROL_LINE_SHA256 = {
    (PARENT_LEDGER, "| 068 |"): "e3fd3910156257dcabd192add1bc54fe17088a0855cdeed18f1ca7d11e36342f",
    (ACTIVE_LEDGER, "| 068 |"): "94043ac6a6ab85a37f9c1679a8c0b3de8a33bbfa8d032b6625cb283a58efc8e3",
    (ACTIVE_LEDGER, "| Phase 068 Step 92 |"): "51cf3bdf05e2e7bc8c9e87b7552f74c5ff10f911d4993937da577b5a86af1adb",
    (HANDOVER, "| Phase 068 Step 92 |"): "505fd934ee47c7d7961e838aaae4032d832009fb224df62444cc30d7678e1de4",
}
CONTROL_LINE_SECTION = {
    (PARENT_LEDGER, "| 068 |"): "## Ledger",
    (ACTIVE_LEDGER, "| 068 |"): "## Execution Ledger",
    (ACTIVE_LEDGER, "| Phase 068 Step 92 |"): "## Commit and Push Ledger",
    (HANDOVER, "| Phase 068 Step 92 |"): "## Handover Chain",
}
CONTROL_SECTION_SHA256 = {
    (ACTIVE_LEDGER, "## Next Exact Step"): "4f04278940291ca07c0b4c664ab05826caaf5cf843a9c27a20714b797cdb8d8e",
    (HANDOVER, "## Exact Next Action"): "23eb3a2cd63f1fab231d017df4386bb7100a8c87544ab33645e49b488dca28ce",
}
NEGATIVE_CONTROL_SPECS = (
    {"id":"N92-CONTROL-STALE","predicate":"authoritative marker is current","error":"E_CONTROL_MARKER"},
    {"id":"N92-CONTROL-DUPLICATE","predicate":"authoritative marker is unique","error":"E_CONTROL_MARKER"},
    {"id":"N92-CONTROL-HISTORY","predicate":"marker is in the authoritative location","error":"E_CONTROL_MARKER"},
    {"id":"N92-CONTROL-NEXT","predicate":"next-step section is current and exact","error":"E_CONTROL_SECTION"},
    {"id":"N92-CONTROL-ROW","predicate":"checkpoint row is authoritative","error":"E_CONTROL_ROW"},
    {"id":"N92-SOURCE-IMPORT-ALIAS","predicate":"imports are exact and unaliased","error":"E_SOURCE_IMPORT"},
    {"id":"N92-SOURCE-PROCESS","predicate":"process capability is allowlisted","error":"E_SOURCE_CAPABILITY"},
    {"id":"N92-SOURCE-PROCESS-ALIAS","predicate":"process aliases are forbidden","error":"E_SOURCE_CAPABILITY"},
    {"id":"N92-SOURCE-RUN-ALIAS","predicate":"run aliases are forbidden","error":"E_SOURCE_CAPABILITY"},
    {"id":"N92-SOURCE-ANN-ALIAS","predicate":"annotated sensitive aliases are forbidden","error":"E_SOURCE_CAPABILITY"},
    {"id":"N92-SOURCE-NAMED-ALIAS","predicate":"named-expression sensitive aliases are forbidden","error":"E_SOURCE_CAPABILITY"},
    {"id":"N92-SOURCE-LOADER-ALIAS","predicate":"dynamic loader aliases are forbidden","error":"E_SOURCE_CAPABILITY"},
    {"id":"N92-SOURCE-WRITER-ALIAS","predicate":"writer aliases are forbidden","error":"E_SOURCE_CAPABILITY"},
    {"id":"N92-SOURCE-NESTED-IMPORT","predicate":"nested imports are forbidden","error":"E_SOURCE_IMPORT"},
    {"id":"N92-SOURCE-WRITER","predicate":"undeclared writers are forbidden","error":"E_SOURCE_CAPABILITY"},
    {"id":"N92-SOURCE-PATH-REPLACE","predicate":"destructive Path.replace is forbidden","error":"E_SOURCE_CAPABILITY"},
    {"id":"N92-SOURCE-DYNAMIC-CALL","predicate":"dynamic call targets are forbidden","error":"E_SOURCE_CAPABILITY"},
    {"id":"N92-SOURCE-IDENTITY-PATH-ALIAS","predicate":"reviewed validator identity rejects aliased Path.replace drift","error":"E_SOURCE_IDENTITY"},
    {"id":"N92-SOURCE-IDENTITY-CALLABLE-TRANSPORT","predicate":"reviewed validator identity rejects transported subprocess callable drift","error":"E_SOURCE_IDENTITY"},
    {"id":"N92-SOURCE-IDENTITY-BUILDER-UNREACHABLE","predicate":"reviewed builder identity rejects unreachable direct collector drift","error":"E_SOURCE_IDENTITY"},
    {"id":"N92-BUILDER-CALL","predicate":"builder calls the exact collector","error":"E_BUILDER_CONTRACT"},
    {"id":"N92-BUILDER-DEAD-INDIRECT","predicate":"builder collector references are bound to exact executable contexts","error":"E_BUILDER_CONTRACT"},
    {"id":"N92-GIT-DANGEROUS","predicate":"dangerous Git argv is rejected","error":"E_GIT_ARGV"},
    {"id":"N92-GIT-REF","predicate":"Git refs are literal and allowlisted","error":"E_GIT_ARGV"},
    {"id":"N92-GIT-LIVE","predicate":"live ref argv is literal and allowlisted","error":"E_GIT_ARGV"},
    {"id":"N92-GIT-STAGED","predicate":"staged diff uses the exact full-OID shape","error":"E_GIT_ARGV"},
    {"id":"N92-GIT-ABBREV","predicate":"diff object IDs are full length","error":"E_GIT_ARGV"},
    {"id":"N92-STAGED-BLOB","predicate":"staged diff blob equals index and worktree blob","error":"E_SELFTEST_BLOB_BINDING"},
    {"id":"N92-SNAPSHOT-DIRTY","predicate":"transaction snapshot is unchanged","error":"E_SELFTEST_SNAPSHOT_DRIFT"},
    {"id":"N92-POST-JSON-EXTRA-PATH","predicate":"post-JSON status has no undeclared path","error":"E_POST_JSON_STATUS"},
    {"id":"N92-POST-JSON-STAGED-DRIFT","predicate":"post-JSON status remains five untracked additions and three unstaged modifications","error":"E_POST_JSON_STATUS"},
    {"id":"N92-CONTENT-SNAPSHOT-DRIFT","predicate":"content boundary, porcelain, and exact-eight bytes remain unchanged","error":"E_CONTENT_SNAPSHOT_DRIFT"},
    {"id":"N92-COLLECT-SNAPSHOT-DRIFT","predicate":"pre-JSON boundary, porcelain, and six input bytes remain unchanged before publication","error":"E_COLLECT_SNAPSHOT_DRIFT"},
    {"id":"N92-JSON-DUPLICATE","predicate":"JSON keys are unique","error":"E_JSON_DUPLICATE_KEY"},
    {"id":"N92-JSON-NONFINITE","predicate":"JSON numbers are finite","error":"E_JSON_NONFINITE"},
    {"id":"N92-JSON-DEEP","predicate":"JSON nesting is bounded","error":"E_JSON_SHAPE_LIMIT"},
    {"id":"N92-JSON-CANONICAL","predicate":"JSON bytes are canonical LF form","error":"E_OUTPUT_JSON_FORM"},
    {"id":"N92-DIFF-STATUS","predicate":"diff status is A or M and paths are unique","error":"E_DIFF_STATUS_OR_DUPLICATE"},
    {"id":"N92-COMMIT-DROP","predicate":"all five commits are present in order","error":"E_CONTRACT_COMMITS"},
    {"id":"N92-COMMIT-REPLACE","predicate":"commit identities are frozen","error":"E_CONTRACT_COMMITS"},
    {"id":"N92-PARENT-ORDER","predicate":"merge parent order is frozen","error":"E_CONTRACT_COMMIT_ROWS"},
    {"id":"N92-EDGE-COMBINED","predicate":"six parent edges are preserved separately","error":"E_CONTRACT_EDGES"},
    {"id":"N92-NET-EDGE-CONFUSION","predicate":"69 net paths are distinct from 135 edge events","error":"E_CONTRACT_NET"},
    {"id":"N92-MAIN-DRIFT-INFLATION","predicate":"frozen edge denominator excludes main drift","error":"E_CONTRACT_EDGES"},
    {"id":"N92-PATH-MUTATION","predicate":"edge paths are exact","error":"E_CONTRACT_EDGE_ROWS"},
    {"id":"N92-BLOB-MUTATION","predicate":"edge blob identities are exact","error":"E_CONTRACT_EDGE_ROWS"},
    {"id":"N92-MODE-MUTATION","predicate":"edge modes are exact","error":"E_CONTRACT_EDGE_ROWS"},
    {"id":"N92-STATUS-MUTATION","predicate":"edge statuses are exact","error":"E_CONTRACT_EDGE_ROWS"},
    {"id":"N92-EXTENT-MUTATION","predicate":"raw byte extents are complete and exact","error":"E_CONTRACT_EDGE_ROWS"},
    {"id":"N92-COVERAGE-TRUNCATED","predicate":"every blob read covers byte zero through EOF","error":"E_CONTRACT_COVERAGE"},
    {"id":"N92-PDF-METADATA-ONLY","predicate":"PDF evidence includes all rendered and inspected pages","error":"E_CONTRACT_PDF"},
    {"id":"N92-POINTER-BLOB","predicate":"claim blob pointer binds the declared blob","error":"E_CONTRACT_POINTER_SPEC_BINDING"},
    {"id":"N92-POINTER-PATH","predicate":"claim path pointer binds an occurrence","error":"E_CONTRACT_POINTER_SPEC_BINDING"},
    {"id":"N92-BOUNDARY-UPSTREAM","predicate":"upstream is exact","error":"E_BOUNDARY_UPSTREAM"},
    {"id":"N92-BOUNDARY-LIVE","predicate":"live refs equal frozen refs","error":"E_BOUNDARY_LIVE"},
    {"id":"N92-AUTHORITY-SELFREPORT","predicate":"source self-report is not promoted to truth","error":"E_CONTRACT_AUTHORITY"},
    {"id":"N92-AUTHORITY-PROMOTION","predicate":"scientific truth promotion count remains zero","error":"E_CONTRACT_PROMOTION"},
    {"id":"N92-WHOLE-COMMIT","predicate":"whole-commit adoption count remains zero","error":"E_CONTRACT_PROMOTION"},
    {"id":"N92-UNDECLARED-PATH","predicate":"no undeclared edge path is admitted","error":"E_CONTRACT_EDGE_ROWS"},
    {"id":"N92-WRONG-SUBJECT","predicate":"commit subjects are exact","error":"E_CONTRACT_COMMIT_ROWS"},
    {"id":"N92-WRONG-PARENT","predicate":"commit parents are exact","error":"E_CONTRACT_COMMIT_ROWS"},
    {"id":"N92-MEDIA-COUNT","predicate":"media inventory is exact","error":"E_CONTRACT_MEDIA"},
    {"id":"N92-GAP","predicate":"coverage and parser gap lists are empty","error":"E_CONTRACT_GAPS"},
)


class ValidationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def fail(code: str, detail: str = "") -> None:
    raise ValidationError(code, detail)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def negative_control_registry() -> dict[str, Any]:
    records = [dict(item) for item in NEGATIVE_CONTROL_SPECS]
    return {
        "records": records,
        "ids": [item["id"] for item in records],
        "errors": [item["error"] for item in records],
        "digest": sha256(canonical_bytes(records)),
        "mutation_restoring": True,
        "data_only": True,
    }


def semantic_sha(value: dict[str, Any]) -> str:
    clone = dict(value)
    clone.pop("semantic_sha256", None)
    return sha256(canonical_bytes(clone))


def physical_lines(raw: bytes) -> int:
    return 0 if not raw else raw.count(b"\n") + (0 if raw.endswith(b"\n") else 1)


def parse_source_identity_count(text: str) -> int:
    digits = text.replace(",", "")
    if not digits.isascii() or not digits.isdigit():
        fail("E_SOURCE_IDENTITY", "count")
    value = int(digits)
    if value <= 0 or text != f"{value:,}":
        fail("E_SOURCE_IDENTITY", "count")
    return value


def parse_source_identity_record(lines: list[str], index: int, label: str) -> tuple[int, int, str]:
    if index + 1 >= len(lines):
        fail("E_SOURCE_IDENTITY", "record")
    prefix = f"- {label}: "
    line = lines[index]
    if not line.startswith(prefix):
        fail("E_SOURCE_IDENTITY", "label")
    byte_text, byte_separator, remainder = line[len(prefix):].partition(" bytes, ")
    line_text, line_separator, trailing = remainder.partition(" lines, SHA-256")
    if byte_separator != " bytes, " or line_separator != " lines, SHA-256" or trailing:
        fail("E_SOURCE_IDENTITY", "format")
    hash_line = lines[index + 1]
    if not hash_line.startswith("  `") or not hash_line.endswith("`;"):
        fail("E_SOURCE_IDENTITY", "hash-format")
    digest = hash_line[3:-2]
    if len(digest) != 64 or any(char not in HEX40 for char in digest):
        fail("E_SOURCE_IDENTITY", "hash")
    return parse_source_identity_count(byte_text), parse_source_identity_count(line_text), digest


def parse_reviewed_source_identities(result_text: str) -> dict[str, tuple[int, int, str]]:
    lines = result_text.splitlines()
    if lines.count(SOURCE_IDENTITY_HEADING) != 1:
        fail("E_SOURCE_IDENTITY", "heading")
    if sum(line.startswith("- validator:") for line in lines) != 1 or sum(line.startswith("- builder:") for line in lines) != 1:
        fail("E_SOURCE_IDENTITY", "duplicate-or-missing")
    anchor = lines.index(SOURCE_IDENTITY_HEADING)
    if anchor + 5 >= len(lines) or lines[anchor + 1] != "":
        fail("E_SOURCE_IDENTITY", "layout")
    identities = {
        VALIDATOR: parse_source_identity_record(lines, anchor + 2, "validator"),
        BUILDER: parse_source_identity_record(lines, anchor + 4, "builder"),
    }
    if identities[BUILDER] != FROZEN_BUILDER_IDENTITY:
        fail("E_SOURCE_IDENTITY", BUILDER)
    return identities


def validate_reviewed_source_identity(validator_raw: bytes, builder_raw: bytes, result_text: str) -> tuple[str, str]:
    identities = parse_reviewed_source_identities(result_text)
    decoded: list[str] = []
    for path, raw in ((VALIDATOR, validator_raw), (BUILDER, builder_raw)):
        if (len(raw), physical_lines(raw), sha256(raw)) != identities[path]:
            fail("E_SOURCE_IDENTITY", path)
        try:
            decoded.append(raw.decode("utf-8", "strict"))
        except UnicodeDecodeError:
            fail("E_SOURCE_IDENTITY", f"{path}:utf-8")
    return decoded[0], decoded[1]


def lf_normalize(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def is_hex40(value: str) -> bool:
    return len(value) == 40 and all(char in HEX40 for char in value)


def validate_process_argv(argv: list[str]) -> None:
    if argv and argv[0] == "git":
        validate_git_argv(argv[1:])
        return
    temp_root = Path(tempfile.gettempdir()).resolve()
    if len(argv) == 2 and argv[0] == "pdfinfo":
        source = Path(argv[1]).resolve()
        if source.name == "source.pdf" and source.parent.name.startswith("p068-step92-pdf-") and source.parent.parent == temp_root:
            return
    if len(argv) == 6 and argv[:4] == ["pdftoppm", "-png", "-r", "110"]:
        source = Path(argv[4]).resolve()
        render = Path(argv[5]).resolve()
        if source.name == "source.pdf" and render.name == "page" and source.parent == render.parent and source.parent.name.startswith("p068-step92-pdf-") and source.parent.parent == temp_root:
            return
    fail("E_PROCESS_ARGV", repr(argv))


def run(argv: list[str], *, timeout: int = 300) -> subprocess.CompletedProcess[bytes]:
    validate_process_argv(argv)
    return subprocess.run(argv, cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, shell=False)


def validate_git_argv(args: list[str]) -> None:
    """Accept only the fixed read-only Git shapes used by this validator."""

    fixed: set[tuple[str, ...]] = {
        ("merge-base", BASE, CODEX_TIP),
        ("rev-list", "--reverse", "--topo-order", f"{BASE}..{CODEX_TIP}"),
        ("status", "--porcelain=v1", "-z", "--untracked-files=all"),
        ("rev-parse", "HEAD"),
        ("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"),
        ("remote", "get-url", "origin"),
        ("symbolic-ref", "--quiet", "--short", "HEAD"),
        ("diff", "--quiet", "--"),
        ("diff", "--cached", "--raw", "-z", "--abbrev=40", EXPECTED_PARENT, "--"),
        ("ls-files", "--stage", "-z", "--", *EXACT_EIGHT),
    }
    fixed.update(("show-ref", "--verify", ref) for ref in {
        ACTIVE_LOCAL_REF, ACTIVE_TRACKING_REF, PROTECTED_REF, MAIN_REF, CLAUDE_REF, CODEX_REF,
    })
    fixed.update(("ls-remote", "--exit-code", "origin", ref) for ref in {
        ACTIVE_LIVE_REF, PROTECTED_LIVE_REF, MAIN_LIVE_REF, CLAUDE_LIVE_REF, CODEX_LIVE_REF,
    })
    candidate = tuple(args)
    if candidate in fixed:
        return
    if len(args) == 3 and args[:2] == ["cat-file", "-t"] and is_hex40(args[2]):
        return
    if len(args) == 3 and args[0] == "cat-file" and args[1] in {"blob", "commit"} and is_hex40(args[2]):
        return
    if len(args) == 10 and args[:7] == ["diff-tree", "--no-commit-id", "--raw", "-r", "--abbrev=40", "--no-renames", "-z"] and args[-1] == "--":
        parent, child = args[7], args[8]
        fixed_edges = {(edge[1], edge[2]) for edge in EDGE_SPECS} | {(BASE, CODEX_TIP)}
        if (parent, child) in fixed_edges or (parent == EXPECTED_PARENT and is_hex40(child)):
            return
    fail("E_GIT_ARGV", repr(args))


def git_bytes(args: list[str]) -> bytes:
    validate_git_argv(args)
    proc = run(["git", *args])
    if proc.returncode:
        fail("E_GIT", f"git {args!r}: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout


def git_text(args: list[str]) -> str:
    return git_bytes(args).decode("utf-8", "strict").rstrip("\n")


def object_bytes(oid: str, kind: str) -> bytes:
    if not is_hex40(oid):
        fail("E_OID_FORM", oid)
    if git_text(["cat-file", "-t", oid]) != kind:
        fail("E_OBJECT_TYPE", f"{oid}:{kind}")
    raw = git_bytes(["cat-file", kind, oid])
    actual = hashlib.sha1(kind.encode("ascii") + b" " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    if actual != oid:
        fail("E_OBJECT_IDENTITY", oid)
    return raw


def parse_actor_clock(value: str, field: str) -> tuple[str, int, str]:
    parts = value.rsplit(" ", 2)
    if len(parts) != 3:
        fail("E_COMMIT_ACTOR", field)
    identity, timestamp_raw, timezone = parts
    if not identity or not timestamp_raw.lstrip("-").isdigit():
        fail("E_COMMIT_ACTOR", field)
    if len(timezone) != 5 or timezone[0] not in "+-" or not timezone[1:].isdigit():
        fail("E_COMMIT_TIMEZONE", field)
    hours, minutes = int(timezone[1:3]), int(timezone[3:5])
    if hours > 14 or minutes > 59:
        fail("E_COMMIT_TIMEZONE", field)
    return identity, int(timestamp_raw), timezone


def authenticated_commit_tree(oid: str) -> str:
    raw = object_bytes(oid, "commit")
    header, separator, _ = raw.partition(b"\n\n")
    if separator != b"\n\n":
        fail("E_COMMIT_FORM", oid)
    fields = header.decode("utf-8", "strict").splitlines()
    trees = [line[5:] for line in fields if line.startswith("tree ")]
    if len(trees) != 1 or not is_hex40(trees[0]) or git_text(["cat-file", "-t", trees[0]]) != "tree":
        fail("E_COMMIT_TREE", oid)
    return trees[0]


def parse_commit(oid: str) -> tuple[dict[str, Any], bytes]:
    raw = object_bytes(oid, "commit")
    header, separator, message = raw.partition(b"\n\n")
    if separator != b"\n\n" or not message:
        fail("E_COMMIT_FORM", oid)
    fields = header.decode("utf-8", "strict").splitlines()
    tree = next((line[5:] for line in fields if line.startswith("tree ")), "")
    parents = [line[7:] for line in fields if line.startswith("parent ")]
    author = next((line[7:] for line in fields if line.startswith("author ")), "")
    committer = next((line[10:] for line in fields if line.startswith("committer ")), "")
    if not is_hex40(tree) or git_text(["cat-file", "-t", tree]) != "tree":
        fail("E_COMMIT_TREE", oid)
    author_identity, author_timestamp, author_timezone = parse_actor_clock(author, "author")
    committer_identity, committer_timestamp, committer_timezone = parse_actor_clock(committer, "committer")
    lines = message.decode("utf-8", "strict").splitlines()
    if not lines:
        fail("E_COMMIT_MESSAGE", oid)
    return {
        "fork": "Codex",
        "oid": oid,
        "tree": tree,
        "parents": parents,
        "author": author,
        "author_identity": author_identity,
        "author_timestamp": author_timestamp,
        "author_timezone": author_timezone,
        "committer": committer,
        "committer_identity": committer_identity,
        "committer_timestamp": committer_timestamp,
        "committer_timezone": committer_timezone,
        "subject": lines[0],
        "set_membership": "FROZEN_CODEX_FIVE_COMMIT_SET",
        "raw_bytes": len(raw),
        "raw_sha256": sha256(raw),
        "message_bytes": len(message),
        "message_lines": physical_lines(message),
        "message_sha256": sha256(message),
        "message_final_lf": message.endswith(b"\n"),
        "coverage": {"byte_start": 0, "byte_end": len(raw), "status": "READ_FULL"},
    }, message


def parse_raw_diff(raw: bytes) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    cursor = 0
    while cursor < len(raw):
        record_start = cursor
        meta_end = raw.find(b"\0", cursor)
        if meta_end < 0:
            fail("E_DIFF_FORM", f"meta-nul:{cursor}")
        path_start = meta_end + 1
        path_end = raw.find(b"\0", path_start)
        if path_end < 0:
            fail("E_DIFF_FORM", f"path-nul:{path_start}")
        record_end = path_end + 1
        meta_raw = raw[record_start:meta_end]
        path_raw = raw[path_start:path_end]
        meta = meta_raw.decode("ascii", "strict").split(" ")
        path = path_raw.decode("utf-8", "strict")
        if len(meta) != 5 or not meta[0].startswith(":"):
            fail("E_DIFF_META", repr(meta))
        status = meta[4]
        if status not in {"A", "M"} or path in seen:
            fail("E_DIFF_STATUS_OR_DUPLICATE", f"{status}:{path}")
        seen.add(path)
        records.append({
            "path": path,
            "old_path": path,
            "new_path": path,
            "status": status,
            "old_mode": meta[0][1:],
            "new_mode": meta[1],
            "old_blob": meta[2],
            "new_blob": meta[3],
            "raw_extent": {
                "byte_start": record_start,
                "byte_end": record_end,
                "meta_byte_start": record_start,
                "meta_byte_end": meta_end,
                "path_byte_start": path_start,
                "path_byte_end": path_end,
            },
        })
        cursor = record_end
    if cursor != len(raw) or any(
        item["raw_extent"]["byte_start"] != (0 if index == 0 else records[index - 1]["raw_extent"]["byte_end"])
        for index, item in enumerate(records)
    ):
        fail("E_DIFF_EXTENT")
    return records


def raw_diff(parent: str, child: str) -> tuple[list[dict[str, Any]], bytes]:
    raw = git_bytes(["diff-tree", "--no-commit-id", "--raw", "-r", "--abbrev=40", "--no-renames", "-z", parent, child, "--"])
    return parse_raw_diff(raw), raw


def path_z(records: list[dict[str, str]]) -> bytes:
    return b"".join(item["path"].encode("utf-8") + b"\0" for item in records)


def reconstruct_topology() -> tuple[list[dict[str, Any]], dict[str, bytes], list[dict[str, Any]], list[dict[str, Any]]]:
    if git_text(["merge-base", BASE, CODEX_TIP]) != BASE:
        fail("E_MERGE_BASE")
    revs = git_text(["rev-list", "--reverse", "--topo-order", f"{BASE}..{CODEX_TIP}"]).splitlines()
    if revs != list(COMMITS):
        fail("E_COMMIT_SET", repr(revs))
    commits: list[dict[str, Any]] = []
    messages: dict[str, bytes] = {}
    for oid in COMMITS:
        record, message = parse_commit(oid)
        if tuple(record["parents"]) != EXPECTED_PARENTS[oid] or record["subject"] != EXPECTED_SUBJECTS[oid] or record["tree"] != EXPECTED_TREES[oid]:
            fail("E_COMMIT_IDENTITY", oid)
        commits.append(record)
        messages[oid] = message
    tree_by_commit = {item["oid"]: item["tree"] for item in commits}
    supporting_commits = {BASE}
    supporting_commits.update(parent for _, parent, _, _ in EDGE_SPECS)
    for oid in sorted(supporting_commits):
        if oid not in tree_by_commit:
            tree_by_commit[oid] = authenticated_commit_tree(oid)
        if tree_by_commit[oid] != EXPECTED_TREES[oid]:
            fail("E_COMMIT_TREE", oid)

    net, net_raw = raw_diff(BASE, CODEX_TIP)
    if (len(net_raw), sha256(net_raw), sha256(path_z(net))) != NET_RAW:
        fail("E_NET_FINGERPRINT")
    if len(net) != 69 or any((item["status"], item["old_mode"], item["new_mode"], item["old_blob"]) != ("A", "000000", "100644", ZERO) for item in net):
        fail("E_NET_TOPOLOGY")
    if sum(item["path"].startswith("Codex/") for item in net) != 68 or sum(item["path"] == PDF_PATH for item in net) != 1:
        fail("E_NET_PARTITION")
    net_paths = {item["path"] for item in net}
    for change in net:
        change.update({
            "comparison_base": BASE,
            "commit": CODEX_TIP,
            "net_path_membership": True,
            "old_commit": BASE,
            "old_tree": tree_by_commit[BASE],
            "new_commit": CODEX_TIP,
            "new_tree": tree_by_commit[CODEX_TIP],
        })

    edges: list[dict[str, Any]] = []
    for edge_id, parent, child, expected_count in EDGE_SPECS:
        changes, raw = raw_diff(parent, child)
        expected_bytes, expected_raw_sha, expected_path_sha = EDGE_RAW[edge_id]
        if (len(raw), sha256(raw), sha256(path_z(changes))) != (expected_bytes, expected_raw_sha, expected_path_sha):
            fail("E_EDGE_FINGERPRINT", edge_id)
        if len(changes) != expected_count:
            fail("E_EDGE_COUNT", edge_id)
        parent_index = list(EXPECTED_PARENTS[child]).index(parent) + 1
        for change in changes:
            change.update({
                "commit": child,
                "parent_index": parent_index,
                "parent_oid": parent,
                "net_path_membership": change["path"] in net_paths,
                "old_commit": parent,
                "old_tree": tree_by_commit[parent],
                "new_commit": child,
                "new_tree": tree_by_commit[child],
            })
        edges.append({
            "edge_id": edge_id,
            "parent": parent,
            "parent_tree": tree_by_commit[parent],
            "commit": child,
            "commit_tree": tree_by_commit[child],
            "parent_index": parent_index,
            "path_count": len(changes),
            "status_counts": {key: sum(item["status"] == key for item in changes) for key in ("A", "M")},
            "raw_bytes": len(raw),
            "raw_sha256": sha256(raw),
            "path_z_sha256": sha256(path_z(changes)),
            "coverage": {"byte_start": 0, "byte_end": len(raw), "status": "READ_FULL"},
            "changes": changes,
        })
    if tuple(item["path"] for item in edges[2]["changes"]) != E3_PATHS:
        fail("E_MERGE_FIRST_PARENT_PATHS")
    if not (sum(item["path"].startswith("Codex/") for item in edges[3]["changes"]) == 58 and sum(item["path"] == PDF_PATH for item in edges[3]["changes"]) == 1):
        fail("E_MERGE_SECOND_PARENT_PARTITION")
    e4 = {(item["path"], item["status"], item["old_mode"], item["new_mode"], item["old_blob"], item["new_blob"]) for item in edges[3]["changes"]}
    e1e2 = {(item["path"], item["status"], item["old_mode"], item["new_mode"], item["old_blob"], item["new_blob"]) for edge in edges[:2] for item in edge["changes"]}
    if e4 != e1e2:
        fail("E_MERGE_SECOND_PARENT_COMPOSITION")
    return commits, messages, edges, net


def reject_constant(value: str) -> None:
    fail("E_JSON_NONFINITE", value)


def pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail("E_JSON_DUPLICATE_KEY", key)
        result[key] = value
    return result


def json_shape(value: Any) -> tuple[int, int, int]:
    nodes = 0
    leaves = 0
    max_depth = 0
    stack = [(value, 1)]
    while stack:
        item, depth = stack.pop()
        nodes += 1
        max_depth = max(max_depth, depth)
        if nodes > MAX_JSON_NODES or depth > MAX_JSON_DEPTH:
            fail("E_JSON_SHAPE_LIMIT", f"{nodes}:{depth}")
        if isinstance(item, dict):
            stack.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            stack.extend((child, depth + 1) for child in item)
        else:
            leaves += 1
            if isinstance(item, float) and not math.isfinite(item):
                fail("E_JSON_NONFINITE")
    return nodes, max_depth, leaves


def parse_source_json(raw: bytes) -> dict[str, int | bool]:
    if len(raw) > MAX_JSON_BYTES:
        fail("E_JSON_SIZE", str(len(raw)))
    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs_no_duplicates, parse_constant=reject_constant)
    except ValidationError:
        raise
    except Exception as exc:
        fail("E_JSON_PARSE", str(exc))
    nodes, depth, leaves = json_shape(value)
    return {"strict_parse": True, "nodes": nodes, "max_depth": depth, "leaves": leaves}


def strict_load(raw: bytes) -> dict[str, Any]:
    if len(raw) > MAX_JSON_BYTES or not raw.endswith(b"\n") or b"\r" in raw or raw.count(b"\n") != 1:
        fail("E_OUTPUT_JSON_FORM")
    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs_no_duplicates, parse_constant=reject_constant)
    except ValidationError:
        raise
    except Exception as exc:
        fail("E_OUTPUT_JSON_PARSE", str(exc))
    if not isinstance(value, dict):
        fail("E_OUTPUT_JSON_ROOT")
    json_shape(value)
    if canonical_bytes(value) != raw or value.get("semantic_sha256") != semantic_sha(value):
        fail("E_OUTPUT_JSON_CANONICAL")
    return value


def media_for(paths: list[str]) -> str:
    suffixes = {PurePosixPath(path).suffix.lower() for path in paths}
    if len(suffixes) != 1:
        fail("E_BLOB_MEDIA_AMBIGUOUS", repr(paths))
    return {".md": "markdown", ".json": "json", ".py": "python", ".tex": "tex", ".pdf": "pdf"}.get(next(iter(suffixes)), "other-text")


def png_size(raw: bytes) -> tuple[int, int]:
    if len(raw) < 24 or raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR":
        fail("E_PNG_FORM")
    return struct.unpack(">II", raw[16:24])


def inspect_pdf(raw: bytes) -> dict[str, Any]:
    if len(raw) != 286_990 or sha256(raw) != PDF_SHA256:
        fail("E_PDF_IDENTITY", f"bytes={len(raw)} sha256={sha256(raw)}")
    root: Path | None = None
    try:
        with tempfile.TemporaryDirectory(prefix="p068-step92-pdf-") as directory:
            root = Path(directory).resolve()
            try:
                root.relative_to(ROOT.resolve())
            except ValueError:
                pass
            else:
                fail("E_PDF_TEMP_INSIDE_REPOSITORY")
            source = root / "source.pdf"
            source.write_bytes(raw)
            info_proc = run(["pdfinfo", str(source)])
            if info_proc.returncode:
                fail("E_PDFINFO", info_proc.stderr.decode("utf-8", "replace"))
            info = info_proc.stdout.decode("utf-8", "replace")
            parsed: dict[str, str] = {}
            for line in info.splitlines():
                key, separator, value = line.partition(":")
                if separator:
                    parsed[key.strip()] = value.strip()
            render_prefix = root / "page"
            render_proc = run(["pdftoppm", "-png", "-r", "110", str(source), str(render_prefix)], timeout=600)
            if render_proc.returncode:
                fail("E_PDF_RENDER", render_proc.stderr.decode("utf-8", "replace"))
            pages = []
            rendered = sorted(root.glob("page-*.png"), key=lambda path: int(path.stem.split("-")[-1]))
            for index, page in enumerate(rendered, 1):
                page_raw = page.read_bytes()
                width, height = png_size(page_raw)
                pages.append({"page": index, "bytes": len(page_raw), "sha256": sha256(page_raw), "width_px": width, "height_px": height})
            if len(pages) != 28 or any((row["width_px"], row["height_px"]) != (910, 1287) for row in pages):
                fail("E_PDF_PAGE_GEOMETRY")
            result = {
                "blob": PDF_BLOB,
                "raw_bytes": len(raw),
                "raw_sha256": sha256(raw),
                "pdfinfo": {"pages": int(parsed.get("Pages", "0")), "page_size": parsed.get("Page size"), "page_rotation": int(parsed.get("Page rot", "-1")), "pdf_version": parsed.get("PDF version")},
                "renderer": {"tool": "pdftoppm", "format": "png", "dpi": 110, "page_count": len(pages), "pages": pages},
                "independent_visual_review": {
                    "reviewer_role": "p068_claims_audit",
                    "exact_blob_authenticated": True,
                    "pages_inspected": list(range(1, 29)),
                    "coverage_status": "VISUAL_READ_FULL_28_OF_28",
                    "readability": "READABLE_NO_BLANK_OR_CLIPPED_BODY",
                    "finding_pages": list(PDF_VISUAL_ISSUE_PAGES),
                    "finding": "even pages 4-28 place the first body line or table at the running-header baseline",
                },
                "cleanup_contract": "TEMPORARY_DIRECTORY_CONTEXT_EXIT_AND_RESIDUE_CHECK",
            }
    finally:
        if root is not None and root.exists():
            fail("E_PDF_TEMP_RESIDUE", str(root))
    if result["pdfinfo"] != {"pages":28,"page_size":"595.28 x 841.89 pts (A4)","page_rotation":0,"pdf_version":"1.5"}:
        fail("E_PDF_METADATA", repr(result["pdfinfo"]))
    return result


def source_surface_summary(media: str, text: str, parsed: dict[str, Any]) -> dict[str, Any]:
    lines = text.splitlines()
    nonblank = [index for index, line in enumerate(lines, 1) if line.strip()]
    result: dict[str, Any] = {
        "scan_method": "ALL_NONBLANK_LINES_PLUS_MEDIA_STRUCTURE",
        "nonblank_line_count": len(nonblank),
        "nonblank_line_number_sha256": sha256("\n".join(map(str, nonblank)).encode("ascii")),
        "covered_line_interval": [1, len(lines)],
    }
    if media == "markdown":
        result["heading_count"] = sum(line.lstrip().startswith("#") for line in lines)
        result["table_row_count"] = sum(line.lstrip().startswith("|") for line in lines)
    elif media == "tex":
        result["label_count"] = sum("\\label{" in line for line in lines)
        result["equation_environment_line_count"] = sum("equation" in line or "align" in line for line in lines)
    elif media == "python":
        tree = parsed["tree"]
        result["definition_count"] = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) for node in ast.walk(tree))
        result["assert_count"] = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
        result["ast_node_count"] = sum(1 for _ in ast.walk(tree))
    elif media == "json":
        result.update({key: parsed[key] for key in ("nodes", "max_depth", "leaves")})
    return result


def build_occurrences(edges: list[dict[str, Any]], net: list[dict[str, Any]]) -> list[dict[str, Any]]:
    occurrences: list[dict[str, Any]] = []
    for edge in edges:
        for index, change in enumerate(edge["changes"], 1):
            for side in ("old", "new"):
                oid = change[f"{side}_blob"]
                if oid != ZERO:
                    occurrences.append({"occurrence_id": f"{edge['edge_id']}-{index:03d}-{side}", "scope": "parent_edge", "edge_id": edge["edge_id"], "path_index": index, "commit": change[f"{side}_commit"], "tree": change[f"{side}_tree"], "path": change["path"], "side": side, "blob": oid, "mode": change[f"{side}_mode"]})
    for index, change in enumerate(net, 1):
        for side in ("old", "new"):
            oid = change[f"{side}_blob"]
            if oid != ZERO:
                occurrences.append({"occurrence_id": f"NET-{index:03d}-{side}", "scope": "base_to_tip_net", "edge_id": None, "path_index": index, "commit": change[f"{side}_commit"], "tree": change[f"{side}_tree"], "path": change["path"], "side": side, "blob": oid, "mode": change[f"{side}_mode"]})
    if len(occurrences) != 211:
        fail("E_OCCURRENCE_COUNT", str(len(occurrences)))
    return occurrences


def build_blob_reads(occurrences: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, bytes], dict[str, Any]]:
    by_oid: dict[str, list[dict[str, Any]]] = {}
    for occurrence in occurrences:
        by_oid.setdefault(occurrence["blob"], []).append(occurrence)
    if len(by_oid) != 82:
        fail("E_UNIQUE_BLOB_COUNT", str(len(by_oid)))
    reads: list[dict[str, Any]] = []
    raws: dict[str, bytes] = {}
    pdf_evidence: dict[str, Any] | None = None
    for oid in sorted(by_oid):
        raw = object_bytes(oid, "blob")
        raws[oid] = raw
        occurrences_for_blob = by_oid[oid]
        paths = sorted({item["path"] for item in occurrences_for_blob})
        media = media_for(paths)
        base: dict[str, Any] = {
            "oid": oid,
            "paths": paths,
            "media": media,
            "raw_bytes": len(raw),
            "raw_sha256": sha256(raw),
            "occurrence_ids": [item["occurrence_id"] for item in occurrences_for_blob],
            "occurrence_count": len(occurrences_for_blob),
            "coverage": {"byte_start": 0, "byte_end": len(raw), "status": "READ_FULL"},
        }
        if media == "pdf":
            if oid != PDF_BLOB or paths != [PDF_PATH]:
                fail("E_PDF_BLOB_PATH")
            pdf_evidence = inspect_pdf(raw)
            base.update({"pages": 28, "review_mode": "BINARY_IDENTITY_PLUS_RENDER_PLUS_VISUAL", "page_coverage": [1, 28], "parser": {"pdfinfo": True, "rendered_pages": 28}})
        else:
            try:
                text = raw.decode("utf-8", "strict")
            except UnicodeDecodeError as exc:
                fail("E_TEXT_UTF8", f"{oid}:{exc}")
            parser: dict[str, Any] = {}
            parsed_for_surface: dict[str, Any] = {}
            if media == "json":
                parser = parse_source_json(raw)
                parsed_for_surface = parser
            elif media == "python":
                try:
                    tree = ast.parse(text, filename=paths[0])
                except SyntaxError as exc:
                    fail("E_PYTHON_AST", f"{oid}:{exc}")
                parser = {"ast_parse": True, "ast_node_count": sum(1 for _ in ast.walk(tree))}
                parsed_for_surface = {"tree": tree}
            else:
                parser = {"utf8_decode": True}
            reviewer = "p068_code_quality" if media in {"python", "json"} else "p068_claims_audit"
            base.update({
                "raw_lines": physical_lines(raw),
                "lf_bytes": len(lf_normalize(raw)),
                "lf_sha256": sha256(lf_normalize(raw)),
                "review_mode": "BYTE_ZERO_TO_EOF_PLUS_HUMAN_SEMANTIC_READ",
                "line_coverage": [1, physical_lines(raw)],
                "parser": parser,
                "claim_surface_scan": source_surface_summary(media, text, parsed_for_surface),
                "independent_read_reviewer": reviewer,
            })
        reads.append(base)
    if pdf_evidence is None:
        fail("E_PDF_NOT_FOUND")
    counts = {media: sum(item["media"] == media for item in reads) for media in ("markdown", "json", "python", "tex", "pdf")}
    if counts != {"markdown": 23, "json": 8, "python": 30, "tex": 20, "pdf": 1}:
        fail("E_MEDIA_COUNTS", repr(counts))
    return reads, raws, pdf_evidence


CLAIM_ASSUMPTIONS: dict[str, list[str]] = {
    "C92-01": ["The count five is the frozen reviewed commit set; this claim does not establish parent topology or reachability."],
    "C92-07": ["Counts and default/opt-in status are Phase 054 source reports, not a current rerun."],
    "C92-08": ["Both deltas use the source block's 288.15 K to 308.15 K comparison and its own numerical procedure."],
    "C92-09": ["R-squared and BIC are source-reported reconstruction metrics; the cited block denies default and phase-decomposition authority."],
    "C92-10": ["The number 51 is the source's suite count and does not imply latest-legacy coverage."],
    "C92-11": ["LR-001 through LR-006 are preserved as one cited matrix block; their row dispositions remain source self-reports."],
    "C92-13": ["The pass/rejection dispositions are preserved as a correction-record report pending Step 94 mathematical adjudication."],
    "C92-14": ["The scaling statement is the Phase 054 derivation/report and has not been promoted to external truth."],
    "C92-15": ["The derivative order and failed disposition are copied from one final-matrix row pending Step 94 mathematical adjudication."],
    "C92-16": ["The count two is the number of cited scholarly source blocks, not a claim that only two such blocks exist in the frozen universe."],
    "C92-17": ["The source uses the dimensionless ratio Omega/(RT) and the threshold value 2 under its stated fit limitations."],
    "C92-18": ["The four ratios are copied exactly from the two cited frozen source blocks and are not independently refitted here."],
    "C92-19": ["The reviewer probe used finite float64 inputs and the smallest positive subnormal relaxation scale; no transcript was preserved."],
    "C92-20": ["The reviewer probe used finite float64 inputs and the largest finite electron stoichiometry; no transcript was preserved."],
    "C92-22": ["The count three refers only to the three cited helper source blocks, not to exhaustive heat-model coverage."],
    "C92-27": ["The cited block is a historical validation self-report without an attached current transcript."],
    "C92-28": ["The page finding applies only to the authenticated frozen PDF rendered at 110 dpi."],
}

CLAIM_QUANTITY_BASES: dict[str, dict[str, Any]] = {
    "C92-01": {"quantities": [5], "unit": "commit_message_subject_count", "sign": "nonnegative_count", "basis": "five frozen reviewed commit-message objects"},
    "C92-07": {"quantities": [4, 2, 7, 7], "unit": "transition_count", "sign": "nonnegative_count", "basis": "Phase 054 shipped-default and opt-in source report"},
    "C92-08": {"quantities": [0.5252164419568519, 6.394884621840902e-14], "unit": "source-reported maximum curve delta", "sign": "nonnegative_magnitude", "basis": "288.15 K to 308.15 K; default then opt-in"},
    "C92-09": {"quantities": [0.99964941790404, -4760.653827485789], "unit": ["dimensionless_R_squared", "BIC"], "sign": ["nonnegative", "signed"], "basis": "rounded stored-parameter reconstruction reported by Phase 054"},
    "C92-10": {"quantities": [51], "unit": "test_count", "sign": "nonnegative_count", "basis": "source-reported conformance suite size"},
    "C92-11": {"quantities": [1, 6], "unit": "inclusive_matrix_row_id_range", "sign": "positive_identifier", "basis": "LR-001 through LR-006 source block"},
    "C92-13": {"quantities": [3, 1], "unit": ["reported_pass_disposition_count", "reported_rejection_disposition_count"], "sign": "nonnegative_count", "basis": "four-line correction status block"},
    "C92-14": {"quantities": [2], "unit": "leading_square_root_mass_term_count", "sign": "positive_count", "basis": "two leading mass terms identified in the cited cancellation derivation"},
    "C92-15": {"quantities": [1], "unit": "Omega_derivative_order", "sign": "positive_order", "basis": "the first Omega derivative named by the cited final-matrix row"},
    "C92-16": {"quantities": [2], "unit": "cited_scholarly_source_block_count", "sign": "nonnegative_count", "basis": "two explicitly enumerated claim pointers"},
    "C92-17": {"quantities": [2], "unit": "dimensionless_Omega_over_RT_threshold", "sign": "positive", "basis": "scholarly source claim"},
    "C92-18": {"quantities": [1.916, 2.027, 2.472, 2.604], "unit": "dimensionless_Omega_over_RT", "sign": "positive", "basis": "four graphite transition ratios reported by two cited frozen source blocks"},
    "C92-19": {"quantities": [5e-324], "unit": "coordinate_scale_in_float64", "sign": "positive", "basis": "bounded reviewer probe using the smallest positive subnormal"},
    "C92-20": {"quantities": [sys.float_info.max], "unit": "dimensionless_electron_stoichiometry_in_float64", "sign": "positive", "basis": "bounded reviewer probe using the largest finite float"},
    "C92-22": {"quantities": [3], "unit": "cited_source_block_count", "sign": "nonnegative_count", "basis": "three explicitly enumerated heat-helper line ranges"},
    "C92-27": {"quantities": [9, 4, 5, 51, 16, 15, 183, 32, 28], "unit": "heterogeneous_source_reported_counts", "sign": "nonnegative_count", "basis": "historical verification-result block; no current transcript attached"},
    "C92-28": {"quantities": [28, 13], "unit": ["page_count", "affected_even_page_count"], "sign": "nonnegative_count", "affected_page_interval": [4, 28], "affected_page_parity": "even", "basis": "exact frozen PDF; visual pages 1-28; affected pages 4-28 even"},
}

CLAIM_REFUTING_EVIDENCE: dict[str, list[str]] = {
    "C92-17": ["C92-18-SRC-01"],
}

BOUNDED_RUNTIME_OBSERVATIONS = [
    {
        "id": "OBS92-RUNTIME-01",
        "claim_ids": ["C92-19"],
        "runtimes": ["Python 3.12", "Python 3.14"],
        "transcript_preserved": False,
        "status": "REVIEWER_OBSERVATION_TRANSCRIPT_NOT_PRESERVED",
        "authority_ceiling": "BOUNDED_REVIEWER_OBSERVATION_ONLY",
        "summary": "Finite float64 inputs with the smallest positive subnormal relaxation scale produced a NaN result.",
    },
    {
        "id": "OBS92-RUNTIME-02",
        "claim_ids": ["C92-20"],
        "runtimes": ["Python 3.12", "Python 3.14"],
        "transcript_preserved": False,
        "status": "REVIEWER_OBSERVATION_TRANSCRIPT_NOT_PRESERVED",
        "authority_ceiling": "BOUNDED_REVIEWER_OBSERVATION_ONLY",
        "summary": "Finite float64 inputs with the largest finite electron stoichiometry produced a NaN derivative.",
    },
]


def claim_specs() -> list[dict[str, Any]]:
    # Each item is deliberately atomic. Scientific/content propositions remain
    # self-report or bounded observations; no primary-source truth is promoted.
    def src(kind: str, oid: str, path: str | None, start: int, end: int) -> dict[str, Any]:
        return {"kind": kind, "oid": oid, "path": path, "start": start, "end": end}
    specs = [
        {"id":"C92-01","key":"fixed_codex_subjects","proposition":"The five cited commit-message subject lines record the reviewed Codex fork's five expected subjects.","domain":"repository_topology","sources":[src("commit_message", oid, None, 1, 1) for oid in COMMITS],"self_report":"NOT_SELF_REPORT_TEXTUAL_OBSERVATION","truth":"TEXT_VERIFIED_SUBJECTS_ONLY","owner":"STEP92","route":"CLOSED_STEP92"},
        {"id":"C92-02","key":"baseline_reconstruction_scope","proposition":"The cited commit-message block reports a trusted-lineage reconstruction scope including manuscript, suite, ledgers, and PDF.","domain":"commit_self_report","sources":[src("commit_message", COMMITS[0], None, 1, 3)],"self_report":"SOURCE_AUTHOR_ASSERTION","truth":"TEXT_VERIFIED_CONTENT_UNADJUDICATED","owner":"STEP93","route":"STEP93"},
        {"id":"C92-03","key":"plan_scholarly_boundary","proposition":"The cited plan block states a scholarly-boundary rule: physics-only body text with implementation mapping kept outside it.","domain":"governance","sources":[src("blob","bb6ec16809f28d52718edb70febd867161011f2a","Codex/plans/2026-07-27-v1025_2-physics-conformance-branch-plan.md",5,12)],"self_report":"SOURCE_RULE","truth":"TEXT_VERIFIED","owner":"STEP96","route":"STEP96"},
        {"id":"C92-04","key":"old_handover_no_commit_claim","proposition":"The original handover reported that commit, push, and merge had not been performed.","domain":"historical_workflow","sources":[src("blob","db4f297da66079aa6ee3668529207fc5c6b0b3cb","Codex/results/HANDOVER_V1025_3_CONFORMANCE_BRANCH.md",5,9)],"self_report":"SOURCE_SELF_REPORT","truth":"SUPERSEDED_SELF_REPORT","owner":"STEP93","route":"STEP93"},
        {"id":"C92-05","key":"corrected_branch_state","proposition":"The cited correction status block reports commit and push, and reports no main merge or promotion.","domain":"historical_workflow","sources":[src("blob","07fd4f05cff4419ab1a0060b14c1e498f6841480","Codex/results/HANDOVER_V1025_3_CONFORMANCE_BRANCH_CORRECTION_20260727.md",17,29)],"self_report":"SOURCE_SELF_REPORT","truth":"TEXT_VERIFIED_REPOSITORY_CHECK_STEP93","owner":"STEP93","route":"STEP93"},
        {"id":"C92-06","key":"parallel_noncanonical_candidate","proposition":"The cited correction block classifies the candidate as parallel and non-canonical rather than a v1.0.25.3 canonical successor.","domain":"lineage_status","sources":[src("blob","07fd4f05cff4419ab1a0060b14c1e498f6841480","Codex/results/HANDOVER_V1025_3_CONFORMANCE_BRANCH_CORRECTION_20260727.md",65,76)],"self_report":"SOURCE_AUTHOR_ASSERTION","truth":"TEXT_VERIFIED_CURRENT_PLAN_CONSISTENT","owner":"STEP97","route":"STEP97"},
        {"id":"C92-07","key":"current_default_4_plus_2","proposition":"The cited Phase 054 block reports the shipped default as four graphite transitions plus two Si transitions and 7+7 as opt-in.","domain":"release_wiring","sources":[src("blob","ac944adda05558b612dbd2efe00604d68791156d","Codex/results/PHASE_054_V1025_2_LATEST_LINEAGE_REVIEW_ADDENDUM.md",25,26)],"self_report":"SOURCE_SELF_REPORT","truth":"UNVERIFIED_PENDING_STEP93","owner":"STEP93","route":"STEP93"},
        {"id":"C92-08","key":"temperature_delta_reports","proposition":"The cited Phase 054 source block reports the default and opt-in temperature-change magnitudes 0.5252164419568519 and 6.394884621840902e-14.","domain":"numerical_self_report","sources":[src("blob","ac944adda05558b612dbd2efe00604d68791156d","Codex/results/PHASE_054_V1025_2_LATEST_LINEAGE_REVIEW_ADDENDUM.md",27,29)],"self_report":"SOURCE_SELF_REPORT_NO_CURRENT_RERUN","truth":"UNVERIFIED_PENDING_STEP93","owner":"STEP93","route":"STEP93"},
        {"id":"C92-09","key":"direct14_metrics_boundary","proposition":"The cited Phase 054 source block reports direct14 R-squared and BIC and denies shipped-default or graphite/Si phase-decomposition authority.","domain":"fit_authority","sources":[src("blob","ac944adda05558b612dbd2efe00604d68791156d","Codex/results/PHASE_054_V1025_2_LATEST_LINEAGE_REVIEW_ADDENDUM.md",30,32)],"self_report":"SOURCE_SELF_REPORT","truth":"UNVERIFIED_PENDING_STEP93","owner":"STEP93","route":"STEP93"},
        {"id":"C92-10","key":"suite_not_legacy_validation","proposition":"The cited Phase 054 block reports that 51 conformance tests do not automatically validate the latest legacy implementation.","domain":"test_authority","sources":[src("blob","ac944adda05558b612dbd2efe00604d68791156d","Codex/results/PHASE_054_V1025_2_LATEST_LINEAGE_REVIEW_ADDENDUM.md",33,35)],"self_report":"SOURCE_AUTHOR_ASSESSMENT","truth":"TEXT_VERIFIED_RUNTIME_SCOPE_STEP95","owner":"STEP95","route":"STEP95"},
        {"id":"C92-11","key":"alignment_default_rows","proposition":"The cited six-row matrix block records the source's LR-001 through LR-006 default, opt-in, temperature-path, and selector dispositions.","domain":"release_alignment","sources":[src("blob","9846e4a278c35e00d23d7d3c86604da32c46467e","Codex/results/V1025_2_LATEST_RELEASE_ALIGNMENT_MATRIX.md",18,23)],"self_report":"SOURCE_SELF_REPORT","truth":"UNVERIFIED_PENDING_STEP93","owner":"STEP93","route":"STEP93"},
        {"id":"C92-12","key":"alignment_scholarly_failures","proposition":"The cited final-matrix block reports failure rows for stale public descriptions, scholarly-body implementation history, and obsolete symbols.","domain":"scholarly_boundary","sources":[src("blob","9846e4a278c35e00d23d7d3c86604da32c46467e","Codex/results/V1025_2_LATEST_RELEASE_ALIGNMENT_MATRIX.md",24,26)],"self_report":"SOURCE_REVIEW_FINDING","truth":"CONFIRMED_TEXTUAL_FINDING_STEP92","owner":"STEP96","route":"STEP96"},
        {"id":"C92-13","key":"regular_solution_summary","proposition":"The cited correction block reports passes for area, subcritical gap, and value continuity and rejects its first Omega-derivative divergence statement.","domain":"regular_solution","sources":[src("blob","07fd4f05cff4419ab1a0060b14c1e498f6841480","Codex/results/HANDOVER_V1025_3_CONFORMANCE_BRANCH_CORRECTION_20260727.md",60,63)],"self_report":"SOURCE_SELF_REPORT","truth":"UNVERIFIED_PENDING_STEP94","owner":"STEP94","route":"STEP94"},
        {"id":"C92-14","key":"regular_solution_cancellation","proposition":"The cited Phase 054 block reports finite linear-response scaling from cancellation of two leading square-root mass terms.","domain":"regular_solution","sources":[src("blob","ac944adda05558b612dbd2efe00604d68791156d","Codex/results/PHASE_054_V1025_2_LATEST_LINEAGE_REVIEW_ADDENDUM.md",225,235)],"self_report":"SOURCE_AUTHOR_ASSERTION_WITH_NUMERICAL_REPORT","truth":"UNVERIFIED_PENDING_STEP94","owner":"STEP94","route":"STEP94"},
        {"id":"C92-15","key":"derivative_divergence_rejected","proposition":"The final alignment matrix marks the right-threshold first Omega-derivative divergence claim as failed.","domain":"regular_solution","sources":[src("blob","9846e4a278c35e00d23d7d3c86604da32c46467e","Codex/results/V1025_2_LATEST_RELEASE_ALIGNMENT_MATRIX.md",38,38)],"self_report":"SOURCE_REVIEW_FINDING","truth":"UNVERIFIED_PENDING_STEP94","owner":"STEP94","route":"STEP94"},
        {"id":"C92-16","key":"scholarly_body_history_text","proposition":"The two cited scholarly blocks contain version, default, baseline, or implementation-history text.","domain":"scholarly_boundary","sources":[src("blob","258d8edb28f556ae56b0a160c75385bb94ec4644","Claude/docs/v1.0.25.2/_sections/ch1_sec05b_gr2L.tex",177,184),src("blob","614d63d0e18e5eb7939f2c0ec0bdb9ee4623d1ce","Claude/docs/v1.0.25.2/_sections/ch1_sec18_inputs.tex",28,29)],"self_report":"NOT_SELF_REPORT_TEXTUAL_OBSERVATION","truth":"CONFIRMED_TEXTUAL_FINDING_STEP92","owner":"STEP96","route":"STEP96"},
        {"id":"C92-17","key":"all_marginal_two_phase_claim","proposition":"The cited scholarly block reports all fitted graphite transitions as above the 2RT threshold and marginally two-phase.","domain":"phase_classification","sources":[src("blob","258d8edb28f556ae56b0a160c75385bb94ec4644","Claude/docs/v1.0.25.2/_sections/ch1_sec05b_gr2L.tex",198,206)],"self_report":"SOURCE_AUTHOR_ASSERTION","truth":"CONTRADICTED_BY_REPORTED_VALUES","owner":"STEP96","route":"STEP96"},
        {"id":"C92-18","key":"reported_omega_ratios","proposition":"The two cited frozen source blocks report graphite Omega/RT values [1.916, 2.027, 2.472, 2.604].","domain":"phase_classification","sources":[src("blob","537d2a25326116067a079a978dcd1f272a75ed7b","Claude/docs/v1.0.25.2/ARCHIVE_NOTE.md",187,188),src("blob","7aa93a497eb660d40fbfea43f47960aed750c661","Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md",57,57)],"self_report":"SOURCE_SELF_REPORT","truth":"TEXT_VERIFIED_VALUES_NOT_EXTERNALLY_VALIDATED","owner":"STEP96","route":"STEP96"},
        {"id":"C92-19","key":"dynamics_nonfinite_output","proposition":"The cited dynamics source block contains the arithmetic path associated with a transcript-unpreserved reviewer observation of NaN from finite smallest-subnormal-scale inputs.","domain":"numerical_implementation","sources":[src("blob","8a752ddd16b5020c8d278d359d446b7cbeafade0","Codex/work/v1025_2_physics_branch/conformance_model/dynamics.py",61,92)],"self_report":"REVIEWER_OBSERVATION_TRANSCRIPT_NOT_PRESERVED","truth":"BOUNDED_OBSERVATION_PENDING_STEP95_REPRODUCTION","owner":"STEP95","route":"STEP95","observation_ids":["OBS92-RUNTIME-01"]},
        {"id":"C92-20","key":"physical_nonfinite_derivative","proposition":"The cited physical source block contains the arithmetic path associated with a transcript-unpreserved reviewer observation of NaN from finite largest-stoichiometry inputs.","domain":"numerical_implementation","sources":[src("blob","e29d68e69875c1303ed23c5ea1a30336c32b8ca5","Codex/work/v1025_2_physics_branch/conformance_model/physical.py",146,155)],"self_report":"REVIEWER_OBSERVATION_TRANSCRIPT_NOT_PRESERVED","truth":"BOUNDED_OBSERVATION_PENDING_STEP95_REPRODUCTION","owner":"STEP95","route":"STEP95","observation_ids":["OBS92-RUNTIME-02"]},
        {"id":"C92-21","key":"empirical_density_finiteness","proposition":"The empirical density accepts arbitrary finite positive alpha and width but does not guard overflow or nonfinite output.","domain":"numerical_implementation","sources":[src("blob","0fdba1082c4758088a3fc1f0ddd52eb33bd6b744","Codex/work/v1025_2_physics_branch/conformance_model/empirical.py",126,155)],"self_report":"INDEPENDENT_STATIC_REVIEW","truth":"STATIC_DEFECT_CANDIDATE_STEP95","owner":"STEP95","route":"STEP95"},
        {"id":"C92-22","key":"heat_finiteness","proposition":"The three cited heat-helper source blocks contain finite-input checks and return arithmetic without a consistent nonfinite-result rejection step.","domain":"numerical_implementation","sources":[src("blob","aa80827bc1b72ef3fd6cb79bd665e02d903fec5a","Codex/work/v1025_2_physics_branch/conformance_model/heat.py",17,36),src("blob","aa80827bc1b72ef3fd6cb79bd665e02d903fec5a","Codex/work/v1025_2_physics_branch/conformance_model/heat.py",39,68),src("blob","aa80827bc1b72ef3fd6cb79bd665e02d903fec5a","Codex/work/v1025_2_physics_branch/conformance_model/heat.py",71,117)],"self_report":"INDEPENDENT_STATIC_REVIEW","truth":"STATIC_DEFECT_CANDIDATE_STEP95","owner":"STEP95","route":"STEP95"},
        {"id":"C92-23","key":"complete_suite_command","proposition":"The tests README presents run_all.py as the complete suite command.","domain":"test_operability","sources":[src("blob","f52d7a51b856fcd02283c989a8be08e41c77a251","Codex/work/v1025_2_physics_branch/tests/README.md",3,7)],"self_report":"SOURCE_DOCUMENTATION_ASSERTION","truth":"PREREQUISITES_INCOMPLETE","owner":"STEP95","route":"STEP95"},
        {"id":"C92-24","key":"suite_hidden_prerequisites","proposition":"The reference helper hard-imports NumPy, Pandas, and SciPy and requires exact Claude fixtures including sigr.csv.","domain":"test_operability","sources":[src("blob","81b5fd88fa75a49a6d957842288bc6f4fa1fe343","Codex/work/v1025_2_physics_branch/tests/_reference.py",11,24)],"self_report":"NOT_SELF_REPORT_STATIC_OBSERVATION","truth":"CONFIRMED_STATIC_FINDING_STEP92","owner":"STEP95","route":"STEP95"},
        {"id":"C92-25","key":"clean_candidate_boundary","proposition":"The candidate README calls the package a clean downstream implementation that does not import or modify the release implementation.","domain":"implementation_scope","sources":[src("blob","62ec65b9f3d10c1271e0459fceafb514adbb1dc6","Codex/work/v1025_2_physics_branch/conformance_model/README.md",3,5)],"self_report":"SOURCE_DOCUMENTATION_ASSERTION","truth":"UNVERIFIED_PENDING_STEP95","owner":"STEP95","route":"STEP95"},
        {"id":"C92-26","key":"regular_solution_absent","proposition":"The candidate README says regular-solution equilibrium is absent pending branch, conservation, identifiability, and solver acceptance.","domain":"implementation_scope","sources":[src("blob","62ec65b9f3d10c1271e0459fceafb514adbb1dc6","Codex/work/v1025_2_physics_branch/conformance_model/README.md",23,26)],"self_report":"SOURCE_DOCUMENTATION_ASSERTION","truth":"TEXT_VERIFIED_IMPLEMENTATION_SCOPE_STEP95","owner":"STEP95","route":"STEP95"},
        {"id":"C92-27","key":"suite_success_self_reports","proposition":"The cited historical verification block reports its listed legacy gates, suite, manuscript structure, probes, regular-solution sweep, and existing PDF inspection outcomes.","domain":"historical_validation","sources":[src("blob","07fd4f05cff4419ab1a0060b14c1e498f6841480","Codex/results/HANDOVER_V1025_3_CONFORMANCE_BRANCH_CORRECTION_20260727.md",78,94)],"self_report":"SOURCE_SELF_REPORT_WITHOUT_ATTACHED_CURRENT_TRANSCRIPT","truth":"UNVERIFIED_PENDING_STEPS93_96","owner":"STEP96","route":"STEP96"},
        {"id":"C92-28","key":"pdf_visual_layout","proposition":"The cited PDF places first body content at the running-header baseline on even pages 4 through 28.","domain":"pdf_layout","sources":[src("pdf_page",PDF_BLOB,PDF_PATH,1,28)],"self_report":"INDEPENDENT_EXACT_BLOB_VISUAL_REVIEW","truth":"OBSERVED_VISUAL_FINDING_STEP92","owner":"STEP96","route":"STEP96"},
        {"id":"C92-29","key":"candidate_authority_ceiling","proposition":"The original handover forbids promoting direct14 phase assignment, original optimizer reproduction, and several unimplemented closures to release claims.","domain":"authority_boundary","sources":[src("blob","db4f297da66079aa6ee3668529207fc5c6b0b3cb","Codex/results/HANDOVER_V1025_3_CONFORMANCE_BRANCH.md",57,63)],"self_report":"SOURCE_GOVERNANCE_ASSERTION","truth":"TEXT_VERIFIED_CURRENT_PLAN_CONSISTENT","owner":"STEP97","route":"STEP97"},
        {"id":"C92-30","key":"implementation_language_boundary","proposition":"The test documentation permits implementation symbols only in a designated appendix and keeps paths, commits, work history, and test output external.","domain":"scholarly_boundary","sources":[src("blob","f52d7a51b856fcd02283c989a8be08e41c77a251","Codex/work/v1025_2_physics_branch/tests/README.md",34,36)],"self_report":"SOURCE_RULE","truth":"TEXT_VERIFIED","owner":"STEP96","route":"STEP96"},
    ]
    for spec in specs:
        spec["assumptions"] = CLAIM_ASSUMPTIONS.get(spec["id"], [])
        spec["quantity_unit_sign_basis"] = CLAIM_QUANTITY_BASES.get(spec["id"])
        spec.setdefault("observation_ids", [])
        spec["refuting_evidence_ids"] = CLAIM_REFUTING_EVIDENCE.get(spec["id"], [])
    return specs


def line_slice(raw: bytes, start: int, end: int) -> bytes:
    lines = raw.splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        fail("E_CLAIM_RANGE", f"{start}:{end}:{len(lines)}")
    return b"".join(lines[start - 1:end])


def build_claims(messages: dict[str, bytes], blobs: dict[str, bytes], occurrences: list[dict[str, Any]]) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    occurrence_pairs = {(item["blob"], item["path"]) for item in occurrences}
    for spec in claim_specs():
        pointers = []
        for index, source in enumerate(spec["sources"], 1):
            if source["kind"] == "commit_message":
                if source["oid"] not in messages or source["path"] is not None:
                    fail("E_CLAIM_MESSAGE_POINTER", spec["id"])
                raw = messages[source["oid"]]
                selected = line_slice(raw, source["start"], source["end"])
                pointer = {"source_kind":"commit_message","source_oid":source["oid"],"path":None,"line_start":source["start"],"line_end":source["end"],"page_start":None,"page_end":None,"source_sha256":sha256(raw),"slice_sha256":sha256(selected),"excerpt":selected.decode("utf-8","strict")[:320]}
            elif source["kind"] == "pdf_page":
                if (source["oid"], source["path"]) not in occurrence_pairs or source["oid"] not in blobs or source["start"] < 1 or source["end"] < source["start"] or source["end"] > 28:
                    fail("E_CLAIM_PDF_POINTER", spec["id"])
                raw = blobs[source["oid"]]
                pointer = {"source_kind":"pdf_page","source_oid":source["oid"],"path":source["path"],"line_start":None,"line_end":None,"page_start":source["start"],"page_end":source["end"],"source_sha256":sha256(raw),"slice_sha256":None,"excerpt":None}
            else:
                if source["kind"] != "blob" or (source["oid"], source["path"]) not in occurrence_pairs or source["oid"] not in blobs:
                    fail("E_CLAIM_BLOB_POINTER", spec["id"])
                raw = blobs[source["oid"]]
                selected = line_slice(raw, source["start"], source["end"])
                pointer = {"source_kind":"blob","source_oid":source["oid"],"path":source["path"],"line_start":source["start"],"line_end":source["end"],"page_start":None,"page_end":None,"source_sha256":sha256(raw),"slice_sha256":sha256(selected),"excerpt":selected.decode("utf-8","strict")[:320]}
            pointer["evidence_id"] = f"{spec['id']}-SRC-{index:02d}"
            pointer["coverage_status"] = "EXACT_SLICE_OF_FULLY_READ_SOURCE"
            pointers.append(pointer)
        claims.append({
            "id": spec["id"], "assertion_key": spec["key"], "normalized_proposition": spec["proposition"], "domain": spec["domain"],
            "assumptions": spec["assumptions"], "quantity_unit_sign_basis": spec["quantity_unit_sign_basis"], "claimant_surfaces": pointers,
            "supporting_evidence_ids": [item["evidence_id"] for item in pointers], "refuting_evidence_ids": spec["refuting_evidence_ids"],
            "observation_ids": spec["observation_ids"],
            "self_report_status": spec["self_report"], "truth_status": spec["truth"], "authority_ceiling": "FROZEN_SOURCE_OR_BOUNDED_STEP92_OBSERVATION_ONLY",
            "owner": spec["owner"], "route": spec["route"], "source_self_report_is_not_truth": True, "scientific_truth_promoted": False,
        })
    if [item["id"] for item in claims] != [f"C92-{index:02d}" for index in range(1, 31)]:
        fail("E_CLAIM_IDS")
    return claims


CLAIM_COVERAGE_CATEGORIES = ("commit_message", "plan", "result", "handover", "manuscript", "model", "test", "PDF")


def claim_coverage_category(pointer: dict[str, Any]) -> str:
    kind = pointer.get("source_kind")
    path = pointer.get("path")
    if kind == "commit_message" and path is None:
        return "commit_message"
    if kind == "pdf_page" and path == PDF_PATH:
        return "PDF"
    if kind != "blob" or not isinstance(path, str):
        fail("E_CLAIM_COVERAGE_CATEGORY", repr((kind, path)))
    name = PurePosixPath(path).name
    if "HANDOVER" in name.upper():
        return "handover"
    if path.startswith("Codex/plans/"):
        return "plan"
    if "/tests/" in path:
        return "test"
    if "/conformance_model/" in path:
        return "model"
    if "/manuscript/" in path or path.startswith("Claude/docs/") or PurePosixPath(path).suffix.lower() == ".tex":
        return "manuscript"
    if path.startswith("Codex/results/") or "/results/" in path:
        return "result"
    fail("E_CLAIM_COVERAGE_CATEGORY", path)


def full_read_coverage_category(row: dict[str, Any]) -> str:
    path = row.get("path")
    if row.get("media_role") == "pdf" and path == PDF_PATH:
        return "PDF"
    if not isinstance(path, str):
        fail("E_FULL_READ_COVERAGE_CATEGORY", repr(path))
    name = PurePosixPath(path).name
    if "HANDOVER" in name.upper() or "/handoffs/" in path:
        return "handover"
    if "/plans/" in path:
        return "plan"
    if "/tests/" in path or name.startswith("test_"):
        return "test"
    if "/conformance_model/" in path:
        return "model"
    if "/results/" in path and "/manuscript/" not in path:
        return "result"
    if row.get("media_role") in {"python", "json"}:
        return "model"
    if "/manuscript/" in path or path.startswith("Claude/docs/") or PurePosixPath(path).suffix.lower() == ".tex":
        return "manuscript"
    fail("E_FULL_READ_COVERAGE_CATEGORY", path)


def build_claim_coverage_register(commits: list[dict[str, Any]], full_read_rows: list[dict[str, Any]], claims: list[dict[str, Any]]) -> dict[str, Any]:
    claim_reverse_index: list[dict[str, str]] = []
    for claim in claims:
        for pointer in claim["claimant_surfaces"]:
            claim_reverse_index.append({
                "evidence_id": pointer["evidence_id"],
                "claim_id": claim["id"],
                "category": claim_coverage_category(pointer),
            })
    source_reverse_index = [
        {"source_row_id": f"COMMIT-MESSAGE-{item['oid']}", "category": "commit_message", "source_kind": "commit_message", "commit": item["oid"], "tree": item["tree"], "path": None, "blob": None}
        for item in commits
    ]
    source_reverse_index.extend({
        "source_row_id": item["occurrence_id"],
        "category": full_read_coverage_category(item),
        "source_kind": "blob_occurrence",
        "commit": item["commit"],
        "tree": item["tree"],
        "path": item["path"],
        "blob": item["blob"],
    } for item in full_read_rows)
    categories = []
    for category in CLAIM_COVERAGE_CATEGORIES:
        source_rows = [item for item in source_reverse_index if item["category"] == category]
        claim_rows = [item for item in claim_reverse_index if item["category"] == category]
        categories.append({
            "category": category,
            "source_row_count": len(source_rows),
            "source_row_ids": [item["source_row_id"] for item in source_rows],
            "unique_blob_count": len({item["blob"] for item in source_rows if item["blob"] is not None}),
            "claim_pointer_count": len(claim_rows),
            "claim_ids": sorted({item["claim_id"] for item in claim_rows}),
            "evidence_ids": [item["evidence_id"] for item in claim_rows],
            "coverage_status": "EXACT_SOURCE_AND_CLAIM_REVERSE_INDEX",
        })
    if not all(item["source_row_count"] for item in categories) or not all(item["claim_pointer_count"] for item in categories):
        fail("E_CLAIM_COVERAGE_EMPTY_CATEGORY")
    if len(claim_reverse_index) != len({item["evidence_id"] for item in claim_reverse_index}):
        fail("E_CLAIM_COVERAGE_DUPLICATE_EVIDENCE")
    if len(source_reverse_index) != 216 or len(source_reverse_index) != len({item["source_row_id"] for item in source_reverse_index}):
        fail("E_CLAIM_COVERAGE_SOURCE_REVERSE_INDEX")
    return {
        "category_count": len(CLAIM_COVERAGE_CATEGORIES),
        "category_order": list(CLAIM_COVERAGE_CATEGORIES),
        "source_row_count": len(source_reverse_index),
        "covered_source_row_count": len(source_reverse_index),
        "claim_pointer_count": len(claim_reverse_index),
        "covered_pointer_count": len(claim_reverse_index),
        "categories": categories,
        "source_reverse_index": source_reverse_index,
        "claim_reverse_index": claim_reverse_index,
        "coverage_status": "EXACT_EIGHT_CATEGORY_SOURCE_AND_CLAIM_COMPLETE",
    }


def build_full_read_rows(occurrences: list[dict[str, Any]], reads: list[dict[str, Any]], claims: list[dict[str, Any]], pdf: dict[str, Any]) -> list[dict[str, Any]]:
    reads_by_oid = {item["oid"]: item for item in reads}
    if len(reads_by_oid) != len(reads):
        fail("E_FULL_READ_DUPLICATE_BLOB")
    occurrence_ids = [item["occurrence_id"] for item in occurrences]
    if len(occurrence_ids) != 211 or len(occurrence_ids) != len(set(occurrence_ids)):
        fail("E_FULL_READ_OCCURRENCE_IDS")
    read_occurrence_ids = [occurrence_id for read in reads for occurrence_id in read["occurrence_ids"]]
    if sorted(read_occurrence_ids) != sorted(occurrence_ids):
        fail("E_FULL_READ_BLOB_REVERSE_BINDING")
    claims_by_surface: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for claim in claims:
        for pointer in claim["claimant_surfaces"]:
            if pointer["source_kind"] in {"blob", "pdf_page"}:
                key = (pointer["source_oid"], pointer["path"])
                claims_by_surface.setdefault(key, []).append((claim["id"], pointer["evidence_id"]))
    occurrence_surfaces = {(item["blob"], item["path"]) for item in occurrences}
    if not set(claims_by_surface).issubset(occurrence_surfaces):
        fail("E_FULL_READ_CLAIM_SURFACE_BINDING")
    renderer = pdf.get("renderer", {})
    renderer_summary = {key: renderer.get(key) for key in ("tool", "format", "dpi", "page_count")}
    rows: list[dict[str, Any]] = []
    for occurrence in occurrences:
        read = reads_by_oid.get(occurrence["blob"])
        if read is None or occurrence["occurrence_id"] not in read["occurrence_ids"] or occurrence["path"] not in read["paths"]:
            fail("E_FULL_READ_OCCURRENCE_BLOB_BINDING", occurrence["occurrence_id"])
        if not is_hex40(occurrence.get("commit", "")) or not is_hex40(occurrence.get("tree", "")):
            fail("E_FULL_READ_SOURCE_CONTEXT", occurrence["occurrence_id"])
        surface_links = claims_by_surface.get((occurrence["blob"], occurrence["path"]), [])
        rows.append({
            "occurrence_id": occurrence["occurrence_id"],
            "scope": occurrence["scope"],
            "edge_id": occurrence["edge_id"],
            "path_index": occurrence["path_index"],
            "side": occurrence["side"],
            "commit": occurrence["commit"],
            "tree": occurrence["tree"],
            "path": occurrence["path"],
            "blob": occurrence["blob"],
            "mode": occurrence["mode"],
            "media_role": read["media"],
            "raw_bytes": read["raw_bytes"],
            "raw_sha256": read["raw_sha256"],
            "lf_bytes": read.get("lf_bytes"),
            "lf_sha256": read.get("lf_sha256"),
            "lines": read.get("raw_lines"),
            "pages": read.get("pages"),
            "review_mode": read["review_mode"],
            "coverage": {"bytes": copy.deepcopy(read["coverage"]), "lines": copy.deepcopy(read.get("line_coverage")), "pages": copy.deepcopy(read.get("page_coverage"))},
            "parser": copy.deepcopy(read["parser"]),
            "renderer": copy.deepcopy(renderer_summary) if read["media"] == "pdf" else None,
            "claim_ids": sorted({claim_id for claim_id, _ in surface_links}),
            "evidence_ids": sorted({evidence_id for _, evidence_id in surface_links}),
        })
    return rows


FINDINGS = [
    {"id":"F92-P1-01","severity":"P1","family":"SCHOLARLY_BODY_IMPLEMENTATION_HISTORY","claim_ids":["C92-03","C92-12","C92-16","C92-30"],"disposition":"OPEN_ROUTE_STEP96_NO_SOURCE_REPAIR_IN_STEP92"},
    {"id":"F92-P1-02","severity":"P1","family":"OMEGA_THRESHOLD_OVERGENERALIZATION","claim_ids":["C92-17","C92-18"],"disposition":"OPEN_ROUTE_STEP96_WITH_STEP94_MATH_BOUNDARY"},
    {"id":"F92-P1-03","severity":"P1","family":"PDF_RUNNING_HEADER_COLLISION","claim_ids":["C92-28"],"disposition":"OPEN_ROUTE_STEP96_NO_PDF_REPAIR_IN_STEP92"},
    {"id":"F92-P1-04","severity":"P1","family":"NUMERIC_FINITE_DOMAIN","claim_ids":["C92-19","C92-20","C92-21","C92-22"],"disposition":"OPEN_ROUTE_STEP95_REPAIR_AND_REGRESSION_BEFORE_ADOPTION"},
    {"id":"F92-P2-01","severity":"P2","family":"TEST_PREREQUISITES","claim_ids":["C92-23","C92-24"],"disposition":"OPEN_ROUTE_STEP95_DOCUMENT_AND_PREFLIGHT"},
]


def file_identity(path: str) -> dict[str, Any]:
    raw = (ROOT / path).read_bytes()
    return {"path": path, "bytes": len(raw), "sha256": sha256(raw), "mode": "100644"}


def build_payload_objects() -> tuple[dict[str, Any], dict[str, Any]]:
    commits, messages, edges, net = reconstruct_topology()
    occurrences = build_occurrences(edges, net)
    reads, blob_raws, pdf = build_blob_reads(occurrences)
    claims = build_claims(messages, blob_raws, occurrences)
    full_read_rows = build_full_read_rows(occurrences, reads, claims, pdf)
    claim_coverage_register = build_claim_coverage_register(commits, full_read_rows, claims)
    bounded_runtime_observations = copy.deepcopy(BOUNDED_RUNTIME_OBSERVATIONS)
    negative_controls = negative_control_registry()
    pre_json = [file_identity(path) for path in PRE_JSON_SIX]
    evidence_set = {
        "commits": commits,
        "edges": edges,
        "net": net,
        "occurrences": occurrences,
        "blob_identities": [{key: item[key] for key in ("oid","raw_bytes","raw_sha256","media","occurrence_ids")} for item in reads],
        "full_read_rows": full_read_rows,
        "claims": claims,
        "claim_coverage_register": claim_coverage_register,
        "bounded_runtime_observations": bounded_runtime_observations,
        "negative_control_registry": negative_controls,
    }
    evidence_sha = sha256(canonical_bytes(evidence_set))
    inventory: dict[str, Any] = {
        "schema": SCHEMA_INVENTORY,
        "authority": "REPOSITORY_TOPOLOGY_AND_SOURCE_PROVENANCE_ONLY",
        "expected_parent": EXPECTED_PARENT,
        "branch": ACTIVE_BRANCH,
        "base": BASE,
        "tip": CODEX_TIP,
        "merge_base": BASE,
        "commit_count": len(commits),
        "commits": commits,
        "edge_count": len(edges),
        "edge_path_counts": [item["path_count"] for item in edges],
        "edge_path_event_count": sum(item["path_count"] for item in edges),
        "edges": edges,
        "net_path_count": len(net),
        "net_changes": net,
        "net_partition": {"Codex": 68, "PDF": 1},
        "blob_side_occurrence_count": len(occurrences),
        "blob_occurrences": occurrences,
        "unique_blob_count": len(reads),
        "full_read_row_count": len(full_read_rows),
        "claim_count": len(claims),
        "claim_source_pointer_count": sum(len(item["claimant_surfaces"]) for item in claims),
        "claims": claims,
        "claim_coverage_register": claim_coverage_register,
        "bounded_runtime_observations": bounded_runtime_observations,
        "negative_control_registry": copy.deepcopy(negative_controls),
        "source_findings": FINDINGS,
        "source_finding_counts": {"P0": 0, "P1": 4, "P2": 1},
        "validator_release_review": {"P0": 0, "P1": 0, "P2": 0, "scope": "CURRENT_BYTES_REQUIRED_BEFORE_JSON_COLLECTION"},
        "scientific_truth_promotions": 0,
        "whole_commit_adoptions": 0,
        "pre_json_file_identities": pre_json,
        "attestation_path": ATTESTATION,
        "evidence_set_sha256": evidence_sha,
        "precommit_marker": PRECOMMIT_MARKER,
        "content_terminal": CONTENT_TERMINAL,
    }
    inventory["semantic_sha256"] = semantic_sha(inventory)
    inventory_raw = canonical_bytes(inventory)
    attestation: dict[str, Any] = {
        "schema": SCHEMA_ATTESTATION,
        "authority": "FULL_READ_AND_RENDER_COVERAGE_NOT_EXTERNAL_SCIENTIFIC_TRUTH",
        "expected_parent": EXPECTED_PARENT,
        "base": BASE,
        "tip": CODEX_TIP,
        "commit_object_count": len(commits),
        "commit_objects": commits,
        "edge_count": len(edges),
        "edge_path_event_count": sum(item["path_count"] for item in edges),
        "net_path_count": len(net),
        "blob_side_occurrence_count": len(occurrences),
        "unique_blob_count": len(reads),
        "text_blob_count": sum(item["media"] != "pdf" for item in reads),
        "pdf_blob_count": sum(item["media"] == "pdf" for item in reads),
        "unique_blob_raw_bytes": sum(item["raw_bytes"] for item in reads),
        "text_line_count": sum(item.get("raw_lines", 0) for item in reads),
        "media_counts": {media: sum(item["media"] == media for item in reads) for media in ("markdown","json","python","tex","pdf")},
        "unique_blobs": reads,
        "full_read_row_count": len(full_read_rows),
        "full_read_rows": full_read_rows,
        "pdf_evidence": pdf,
        "negative_control_registry": copy.deepcopy(negative_controls),
        "human_read_partitions": [
            {"reviewer_role":"p068_claims_audit","media":["markdown","tex"],"unique_blob_count":43,"coverage":"BYTE_ZERO_TO_EOF_AND_HUMAN_SEMANTIC_READ"},
            {"reviewer_role":"p068_code_quality","media":["json","python"],"unique_blob_count":38,"coverage":"BYTE_ZERO_TO_EOF_JSON_STRICT_OR_PYTHON_AST_PLUS_HUMAN_SEMANTIC_READ"},
            {"reviewer_role":"p068_claims_audit","media":["pdf"],"unique_blob_count":1,"coverage":"EXACT_BLOB_RENDER_AND_VISUAL_28_OF_28"},
        ],
        "coverage_gaps": [],
        "decode_failures": [],
        "parser_failures": [],
        "renderer_failures": [],
        "claim_count": len(claims),
        "claim_ids": [item["id"] for item in claims],
        "claim_coverage_register_sha256": sha256(canonical_bytes(claim_coverage_register)),
        "evidence_set_sha256": evidence_sha,
        "inventory_path": INVENTORY,
        "inventory_bytes": len(inventory_raw),
        "inventory_sha256": sha256(inventory_raw),
        "pre_json_file_identities": pre_json,
        "temporary_materialization_incident": {"workspace_literal_dollar_tmp_removed": True, "system_temp_prefix_residue_count": 0, "repository_contamination": False},
        "scientific_truth_promotions": 0,
        "precommit_marker": PRECOMMIT_MARKER,
        "content_terminal": CONTENT_TERMINAL,
    }
    attestation["semantic_sha256"] = semantic_sha(attestation)
    validate_payload_contract(inventory, attestation)
    return inventory, attestation


def encoded_raw_change(change: dict[str, Any]) -> bytes:
    required = ("path", "old_path", "new_path", "status", "old_mode", "new_mode", "old_blob", "new_blob", "raw_extent")
    if any(key not in change for key in required) or change.get("old_path") != change.get("path") or change.get("new_path") != change.get("path"):
        fail("E_CONTRACT_EDGE_ROWS")
    try:
        meta = f":{change['old_mode']} {change['new_mode']} {change['old_blob']} {change['new_blob']} {change['status']}".encode("ascii")
        path = change["path"].encode("utf-8")
    except (AttributeError, UnicodeError):
        fail("E_CONTRACT_EDGE_ROWS")
    return meta + b"\0" + path + b"\0"


def validate_raw_extents(changes: list[dict[str, Any]], expected: tuple[int, str, str], code: str) -> None:
    chunks: list[bytes] = []
    cursor = 0
    for change in changes:
        chunk = encoded_raw_change(change)
        meta_end = cursor + chunk.index(b"\0")
        path_start = meta_end + 1
        path_end = cursor + len(chunk) - 1
        extent = {
            "byte_start": cursor,
            "byte_end": cursor + len(chunk),
            "meta_byte_start": cursor,
            "meta_byte_end": meta_end,
            "path_byte_start": path_start,
            "path_byte_end": path_end,
        }
        if change.get("raw_extent") != extent:
            fail(code, change.get("path", ""))
        chunks.append(chunk)
        cursor += len(chunk)
    raw = b"".join(chunks)
    if (len(raw), sha256(raw), sha256(path_z(changes))) != expected or cursor != len(raw):
        fail(code, "fingerprint")


def validate_commit_edge_contract(inventory: dict[str, Any], attestation: dict[str, Any]) -> None:
    commits = inventory.get("commits", [])
    if commits != attestation.get("commit_objects"):
        fail("E_CONTRACT_COMMIT_ROWS", "inventory-attestation")
    commit_fields = {
        "fork", "oid", "tree", "parents", "author", "author_identity", "author_timestamp", "author_timezone",
        "committer", "committer_identity", "committer_timestamp", "committer_timezone", "subject", "set_membership",
        "raw_bytes", "raw_sha256", "message_bytes", "message_lines", "message_sha256", "message_final_lf", "coverage",
    }
    for row, oid in zip(commits, COMMITS):
        clocks = EXPECTED_COMMIT_CLOCKS[oid]
        if set(row) != commit_fields or (
            row.get("fork"), row.get("oid"), row.get("tree"), tuple(row.get("parents", [])), row.get("subject"), row.get("set_membership")
        ) != ("Codex", oid, EXPECTED_TREES[oid], EXPECTED_PARENTS[oid], EXPECTED_SUBJECTS[oid], "FROZEN_CODEX_FIVE_COMMIT_SET"):
            fail("E_CONTRACT_COMMIT_ROWS", oid)
        if (
            row.get("author_identity"), row.get("author_timestamp"), row.get("author_timezone"),
            row.get("committer_identity"), row.get("committer_timestamp"), row.get("committer_timezone"),
        ) != ("Codex <codex@openai.com>", clocks[0], clocks[1], "Codex <codex@openai.com>", clocks[2], clocks[3]):
            fail("E_CONTRACT_COMMIT_ROWS", f"clock:{oid}")
        if row.get("author") != f"{row['author_identity']} {row['author_timestamp']} {row['author_timezone']}" or row.get("committer") != f"{row['committer_identity']} {row['committer_timestamp']} {row['committer_timezone']}":
            fail("E_CONTRACT_COMMIT_ROWS", f"actor:{oid}")
        if row.get("coverage") != {"byte_start": 0, "byte_end": row.get("raw_bytes"), "status": "READ_FULL"} or not isinstance(row.get("message_lines"), int):
            fail("E_CONTRACT_COMMIT_ROWS", f"coverage:{oid}")

    edges = inventory.get("edges", [])
    net = inventory.get("net_changes", [])
    net_paths = {item.get("path") for item in net}
    edge_fields = {"edge_id", "parent", "parent_tree", "commit", "commit_tree", "parent_index", "path_count", "status_counts", "raw_bytes", "raw_sha256", "path_z_sha256", "coverage", "changes"}
    edge_change_fields = {"path", "old_path", "new_path", "status", "old_mode", "new_mode", "old_blob", "new_blob", "raw_extent", "commit", "parent_index", "parent_oid", "net_path_membership", "old_commit", "old_tree", "new_commit", "new_tree"}
    for edge, spec in zip(edges, EDGE_SPECS):
        edge_id, parent, child, count = spec
        parent_index = list(EXPECTED_PARENTS[child]).index(parent) + 1
        if set(edge) != edge_fields or (edge.get("edge_id"), edge.get("parent"), edge.get("parent_tree"), edge.get("commit"), edge.get("commit_tree"), edge.get("parent_index"), edge.get("path_count")) != (edge_id, parent, EXPECTED_TREES[parent], child, EXPECTED_TREES[child], parent_index, count):
            fail("E_CONTRACT_EDGE_ROWS", edge_id)
        changes = edge.get("changes", [])
        if len(changes) != count:
            fail("E_CONTRACT_EDGE_ROWS", f"count:{edge_id}")
        for change in changes:
            if set(change) != edge_change_fields or (
                change.get("commit"), change.get("parent_index"), change.get("parent_oid"), change.get("net_path_membership"),
                change.get("old_commit"), change.get("old_tree"), change.get("new_commit"), change.get("new_tree"),
            ) != (child, parent_index, parent, change.get("path") in net_paths, parent, EXPECTED_TREES[parent], child, EXPECTED_TREES[child]):
                fail("E_CONTRACT_EDGE_ROWS", f"context:{edge_id}")
        validate_raw_extents(changes, EDGE_RAW[edge_id], "E_CONTRACT_EDGE_ROWS")
        expected_status_counts = {key: sum(change.get("status") == key for change in changes) for key in ("A", "M")}
        if edge.get("status_counts") != expected_status_counts or (edge.get("raw_bytes"), edge.get("raw_sha256"), edge.get("path_z_sha256")) != EDGE_RAW[edge_id] or edge.get("coverage") != {"byte_start": 0, "byte_end": EDGE_RAW[edge_id][0], "status": "READ_FULL"}:
            fail("E_CONTRACT_EDGE_ROWS", f"aggregate:{edge_id}")

    net_change_fields = {"path", "old_path", "new_path", "status", "old_mode", "new_mode", "old_blob", "new_blob", "raw_extent", "comparison_base", "commit", "net_path_membership", "old_commit", "old_tree", "new_commit", "new_tree"}
    for change in net:
        if set(change) != net_change_fields or (
            change.get("comparison_base"), change.get("commit"), change.get("net_path_membership"), change.get("old_commit"), change.get("old_tree"), change.get("new_commit"), change.get("new_tree"),
        ) != (BASE, CODEX_TIP, True, BASE, EXPECTED_TREES[BASE], CODEX_TIP, EXPECTED_TREES[CODEX_TIP]):
            fail("E_CONTRACT_NET_ROWS", change.get("path", ""))
    validate_raw_extents(net, NET_RAW, "E_CONTRACT_NET_ROWS")


def validate_payload_contract(inventory: dict[str, Any], attestation: dict[str, Any]) -> None:
    if inventory.get("schema") != SCHEMA_INVENTORY or attestation.get("schema") != SCHEMA_ATTESTATION:
        fail("E_CONTRACT_SCHEMA")
    if inventory.get("expected_parent") != EXPECTED_PARENT or attestation.get("expected_parent") != EXPECTED_PARENT:
        fail("E_CONTRACT_PARENT")
    if inventory.get("commit_count") != 5 or [item.get("oid") for item in inventory.get("commits", [])] != list(COMMITS):
        fail("E_CONTRACT_COMMITS")
    if inventory.get("edge_count") != 6 or inventory.get("edge_path_counts") != [58,1,6,59,8,3] or inventory.get("edge_path_event_count") != 135:
        fail("E_CONTRACT_EDGES")
    if inventory.get("net_path_count") != 69 or inventory.get("net_partition") != {"Codex":68,"PDF":1}:
        fail("E_CONTRACT_NET")
    if inventory.get("blob_side_occurrence_count") != 211 or inventory.get("unique_blob_count") != 82:
        fail("E_CONTRACT_BLOBS")
    expected_negative_controls = negative_control_registry()
    if inventory.get("negative_control_registry") != expected_negative_controls or attestation.get("negative_control_registry") != expected_negative_controls:
        fail("E_CONTRACT_NEGATIVE_REGISTRY")
    validate_commit_edge_contract(inventory, attestation)
    occurrences = inventory.get("blob_occurrences", [])
    if len(occurrences) != 211 or any(not is_hex40(item.get("commit", "")) or not is_hex40(item.get("tree", "")) for item in occurrences):
        fail("E_CONTRACT_OCCURRENCE_SOURCE_CONTEXT")
    if occurrences != build_occurrences(inventory.get("edges", []), inventory.get("net_changes", [])):
        fail("E_CONTRACT_OCCURRENCE_TOPOLOGY_BINDING")
    if attestation.get("text_blob_count") != 81 or attestation.get("pdf_blob_count") != 1 or attestation.get("unique_blob_raw_bytes") != 1_784_404 or attestation.get("text_line_count") != 35_710 or attestation.get("media_counts") != {"markdown":23,"json":8,"python":30,"tex":20,"pdf":1}:
        fail("E_CONTRACT_MEDIA")
    reads = attestation.get("unique_blobs", [])
    if len(reads) != 82 or any(item.get("coverage") != {"byte_start":0,"byte_end":item.get("raw_bytes"),"status":"READ_FULL"} for item in reads):
        fail("E_CONTRACT_COVERAGE")
    if any(item.get("media") != "pdf" and item.get("line_coverage") != [1,item.get("raw_lines")] for item in reads):
        fail("E_CONTRACT_LINE_COVERAGE")
    pdf = attestation.get("pdf_evidence", {})
    if pdf.get("blob") != PDF_BLOB or pdf.get("raw_sha256") != PDF_SHA256 or pdf.get("renderer", {}).get("page_count") != 28 or pdf.get("independent_visual_review", {}).get("pages_inspected") != list(range(1,29)):
        fail("E_CONTRACT_PDF")
    claims = inventory.get("claims", [])
    if inventory.get("claim_count") != 30 or [item.get("id") for item in claims] != [f"C92-{index:02d}" for index in range(1,31)]:
        fail("E_CONTRACT_CLAIMS")
    if inventory.get("claim_source_pointer_count") != 38:
        fail("E_CONTRACT_CLAIM_POINTER_COUNT")
    if any(item.get("scientific_truth_promoted") is not False or item.get("source_self_report_is_not_truth") is not True or not item.get("claimant_surfaces") for item in claims):
        fail("E_CONTRACT_AUTHORITY")
    expected_specs = {item["id"]: item for item in claim_specs()}
    occurrence_pairs = {(item.get("blob"), item.get("path")) for item in occurrences}
    reads_by_oid = {item.get("oid"): item for item in reads}
    commits_by_oid = {item.get("oid"): item for item in inventory.get("commits", [])}
    evidence_ids: set[str] = set()
    for claim in claims:
        claim_id = claim["id"]
        expected = expected_specs[claim_id]
        if (claim.get("assertion_key"), claim.get("normalized_proposition"), claim.get("domain"), claim.get("self_report_status"), claim.get("truth_status"), claim.get("owner"), claim.get("route")) != (expected["key"], expected["proposition"], expected["domain"], expected["self_report"], expected["truth"], expected["owner"], expected["route"]):
            fail("E_CONTRACT_CLAIM_SPEC", claim_id)
        if claim.get("authority_ceiling") != "FROZEN_SOURCE_OR_BOUNDED_STEP92_OBSERVATION_ONLY":
            fail("E_CONTRACT_CLAIM_AUTHORITY", claim_id)
        if claim.get("assumptions") != expected["assumptions"] or claim.get("quantity_unit_sign_basis") != expected["quantity_unit_sign_basis"]:
            fail("E_CONTRACT_CLAIM_BASIS", claim_id)
        if claim.get("quantity_unit_sign_basis") is not None and not claim.get("assumptions"):
            fail("E_CONTRACT_QUANTIFIED_CLAIM_ASSUMPTIONS", claim_id)
        if claim.get("refuting_evidence_ids") != expected["refuting_evidence_ids"] or claim.get("observation_ids") != expected["observation_ids"]:
            fail("E_CONTRACT_CLAIM_LINKS", claim_id)
        surfaces = claim["claimant_surfaces"]
        surface_ids = [item.get("evidence_id") for item in surfaces]
        expected_surface_ids = [f"{claim_id}-SRC-{index:02d}" for index in range(1, len(expected["sources"]) + 1)]
        if len(surfaces) != len(expected["sources"]) or surface_ids != expected_surface_ids or claim.get("supporting_evidence_ids") != surface_ids or len(surface_ids) != len(set(surface_ids)):
            fail("E_CONTRACT_SUPPORT_BINDING", claim_id)
        for pointer, source in zip(surfaces, expected["sources"]):
            evidence_id = pointer.get("evidence_id")
            if not isinstance(evidence_id, str) or evidence_id in evidence_ids:
                fail("E_CONTRACT_EVIDENCE_ID", f"{claim_id}:{evidence_id}")
            evidence_ids.add(evidence_id)
            if pointer.get("coverage_status") != "EXACT_SLICE_OF_FULLY_READ_SOURCE":
                fail("E_CONTRACT_POINTER_COVERAGE", evidence_id)
            kind = pointer.get("source_kind")
            oid = pointer.get("source_oid")
            path = pointer.get("path")
            line_start, line_end = pointer.get("line_start"), pointer.get("line_end")
            page_start, page_end = pointer.get("page_start"), pointer.get("page_end")
            expected_line_start = None if source["kind"] == "pdf_page" else source["start"]
            expected_line_end = None if source["kind"] == "pdf_page" else source["end"]
            expected_page_start = source["start"] if source["kind"] == "pdf_page" else None
            expected_page_end = source["end"] if source["kind"] == "pdf_page" else None
            if (kind, oid, path, line_start, line_end, page_start, page_end) != (source["kind"], source["oid"], source["path"], expected_line_start, expected_line_end, expected_page_start, expected_page_end):
                fail("E_CONTRACT_POINTER_SPEC_BINDING", evidence_id)
            if kind == "commit_message":
                commit = commits_by_oid.get(oid)
                if commit is None or path is not None or pointer.get("source_sha256") != commit.get("message_sha256"):
                    fail("E_CONTRACT_MESSAGE_POINTER", evidence_id)
                if not isinstance(line_start, int) or not isinstance(line_end, int) or line_start < 1 or line_end < line_start or line_end > commit.get("message_lines", 0) or page_start is not None or page_end is not None:
                    fail("E_CONTRACT_MESSAGE_RANGE", evidence_id)
            elif kind == "blob":
                read = reads_by_oid.get(oid)
                if read is None or (oid, path) not in occurrence_pairs or pointer.get("source_sha256") != read.get("raw_sha256"):
                    fail("E_CONTRACT_BLOB_POINTER", evidence_id)
                if not isinstance(line_start, int) or not isinstance(line_end, int) or line_start < 1 or line_end < line_start or line_end > read.get("raw_lines", 0) or page_start is not None or page_end is not None:
                    fail("E_CONTRACT_BLOB_RANGE", evidence_id)
            elif kind == "pdf_page":
                read = reads_by_oid.get(oid)
                max_page = pdf.get("renderer", {}).get("page_count")
                if read is None or read.get("media") != "pdf" or (oid, path) not in occurrence_pairs or pointer.get("source_sha256") != read.get("raw_sha256"):
                    fail("E_CONTRACT_PDF_POINTER", evidence_id)
                if line_start is not None or line_end is not None or not isinstance(max_page, int) or not isinstance(page_start, int) or not isinstance(page_end, int) or page_start < 1 or page_end < page_start or page_end > max_page:
                    fail("E_CONTRACT_PDF_RANGE", evidence_id)
            else:
                fail("E_CONTRACT_POINTER_KIND", f"{evidence_id}:{kind}")
    for claim in claims:
        for evidence_id in claim.get("refuting_evidence_ids", []):
            if evidence_id not in evidence_ids:
                fail("E_CONTRACT_REFUTATION_TARGET", f"{claim['id']}:{evidence_id}")
    full_read_rows = attestation.get("full_read_rows", [])
    expected_coverage_register = build_claim_coverage_register(inventory.get("commits", []), full_read_rows, claims)
    if inventory.get("claim_coverage_register") != expected_coverage_register:
        fail("E_CONTRACT_CLAIM_COVERAGE_REGISTER")
    if attestation.get("claim_coverage_register_sha256") != sha256(canonical_bytes(expected_coverage_register)):
        fail("E_CONTRACT_CLAIM_COVERAGE_BINDING")
    expected_full_read_rows = build_full_read_rows(occurrences, reads, claims, pdf)
    if inventory.get("full_read_row_count") != 211 or attestation.get("full_read_row_count") != 211 or len(full_read_rows) != 211:
        fail("E_CONTRACT_FULL_READ_COUNT")
    if full_read_rows != expected_full_read_rows or [item.get("occurrence_id") for item in full_read_rows] != [item.get("occurrence_id") for item in occurrences]:
        fail("E_CONTRACT_FULL_READ_REVERSE_BINDING")
    if expected_specs["C92-17"]["refuting_evidence_ids"] != ["C92-18-SRC-01"]:
        fail("E_CONTRACT_REFUTATION_BINDING")
    observations = inventory.get("bounded_runtime_observations")
    if observations != BOUNDED_RUNTIME_OBSERVATIONS:
        fail("E_CONTRACT_RUNTIME_OBSERVATIONS")
    observation_by_id = {item.get("id"): item for item in observations}
    if len(observation_by_id) != len(observations):
        fail("E_CONTRACT_OBSERVATION_IDS")
    claim_observation_pairs = {(claim["id"], observation_id) for claim in claims for observation_id in claim.get("observation_ids", [])}
    observation_claim_pairs = {(claim_id, observation["id"]) for observation in observations for claim_id in observation.get("claim_ids", [])}
    if claim_observation_pairs != observation_claim_pairs or claim_observation_pairs != {("C92-19","OBS92-RUNTIME-01"),("C92-20","OBS92-RUNTIME-02")}:
        fail("E_CONTRACT_OBSERVATION_BINDING")
    if any(observation.get("transcript_preserved") is not False or observation.get("authority_ceiling") != "BOUNDED_REVIEWER_OBSERVATION_ONLY" for observation in observations):
        fail("E_CONTRACT_OBSERVATION_AUTHORITY")
    if inventory.get("source_finding_counts") != {"P0":0,"P1":4,"P2":1} or [item.get("id") for item in inventory.get("source_findings", [])] != ["F92-P1-01","F92-P1-02","F92-P1-03","F92-P1-04","F92-P2-01"]:
        fail("E_CONTRACT_FINDINGS")
    if inventory.get("validator_release_review") != {"P0":0,"P1":0,"P2":0,"scope":"CURRENT_BYTES_REQUIRED_BEFORE_JSON_COLLECTION"}:
        fail("E_CONTRACT_RELEASE_REVIEW")
    if inventory.get("scientific_truth_promotions") != 0 or inventory.get("whole_commit_adoptions") != 0 or attestation.get("scientific_truth_promotions") != 0:
        fail("E_CONTRACT_PROMOTION")
    if inventory.get("evidence_set_sha256") != attestation.get("evidence_set_sha256"):
        fail("E_CONTRACT_EVIDENCE_BINDING")
    if attestation.get("inventory_sha256") != sha256(canonical_bytes(inventory)):
        fail("E_CONTRACT_INVENTORY_BINDING")
    if inventory.get("pre_json_file_identities") != attestation.get("pre_json_file_identities"):
        fail("E_CONTRACT_CONTROL_BINDING")
    if any(attestation.get(key) != [] for key in ("coverage_gaps","decode_failures","parser_failures","renderer_failures")):
        fail("E_CONTRACT_GAPS")
    if inventory.get("content_terminal") != CONTENT_TERMINAL or attestation.get("content_terminal") != CONTENT_TERMINAL:
        fail("E_CONTRACT_TERMINAL")


def read_text(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        fail("E_CONTROL_MISSING", path)
    try:
        return target.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail("E_CONTROL_UTF8", f"{path}:{exc}")


def require_tokens(path: str, tokens: Iterable[str]) -> str:
    text = read_text(path)
    for token in tokens:
        if token not in text:
            fail("E_CONTROL_TOKEN", f"{path}:{token}")
    return text


def exact_control_line(path: str, text: str, prefix: str) -> str:
    lines = text.splitlines()
    matches = [(index, line) for index, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        fail("E_CONTROL_ROW", f"{path}:{prefix}:count={len(matches)}")
    index, line = matches[0]
    heading = CONTROL_LINE_SECTION[(path, prefix)]
    headings = [position for position, candidate in enumerate(lines) if candidate == heading]
    if len(headings) != 1:
        fail("E_CONTROL_ROW", f"{path}:{heading}:count={len(headings)}")
    section_start = headings[0]
    section_end = next((position for position in range(section_start + 1, len(lines)) if lines[position].startswith("## ")), len(lines))
    if not section_start < index < section_end:
        fail("E_CONTROL_ROW", f"{path}:{prefix}:outside={heading}")
    if sha256(line.encode("utf-8")) != CONTROL_LINE_SHA256[(path, prefix)]:
        fail("E_CONTROL_ROW", f"{path}:{prefix}:digest")
    return line


def exact_control_section(path: str, text: str, heading: str) -> tuple[str, str | None]:
    lines = text.splitlines(keepends=True)
    starts = [index for index, line in enumerate(lines) if line.rstrip("\n") == heading]
    if len(starts) != 1:
        fail("E_CONTROL_SECTION", f"{path}:{heading}:count={len(starts)}")
    start = starts[0]
    end = next((index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")), len(lines))
    section = "".join(lines[start:end])
    if sha256(section.encode("utf-8")) != CONTROL_SECTION_SHA256[(path, heading)]:
        fail("E_CONTROL_SECTION", f"{path}:{heading}:digest")
    following = None if end == len(lines) else lines[end].rstrip("\n")
    return section, following


def validate_human_control_texts(texts: dict[str, str]) -> None:
    for path, text in texts.items():
        if "\r" in text:
            fail("E_CONTROL_NEWLINE", path)
    result = texts[RESULT]
    for token in (EXPECTED_PARENT, EXPECTED_SUBJECT, "PENDING_AT_PRECOMMIT_BY_DESIGN", PERSISTENCE_TERMINAL, "commit objects read: 5/5", "parent-edge records read: 135/135", "net records read: 69/69", "blob occurrences resolved: 211/211", "unique blobs read: 82/82", "28/28", "P0 0 / P1 4 finding families / P2 1"):
        if token not in result:
            fail("E_CONTROL_TOKEN", f"{RESULT}:{token}")
    result_marker = f"- precommit marker: `{PRECOMMIT_MARKER}`"
    if result.splitlines().count(result_marker) != 1:
        fail("E_CONTROL_MARKER", RESULT)
    if next((line.strip() for line in reversed(result.splitlines()) if line.strip()), "") != CONTENT_TERMINAL:
        fail("E_RESULT_TERMINAL")
    current_marker = f"Current-state marker: `{PRECOMMIT_MARKER}`"
    for path in (PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER):
        lines = texts[path].splitlines()
        marker_lines = [(index, line) for index, line in enumerate(lines) if line.startswith("Current-state marker:")]
        first_heading = next((index for index, line in enumerate(lines) if line.startswith("## ")), len(lines))
        if len(marker_lines) != 1 or marker_lines[0][1] != current_marker or marker_lines[0][0] >= first_heading:
            fail("E_CONTROL_MARKER", f"{path}:{marker_lines!r}")
    for path, prefix in CONTROL_LINE_SHA256:
        exact_control_line(path, texts[path], prefix)
    _, following = exact_control_section(ACTIVE_LEDGER, texts[ACTIVE_LEDGER], "## Next Exact Step")
    if following is not None:
        fail("E_CONTROL_SECTION", f"{ACTIVE_LEDGER}:not-eof")
    _, following = exact_control_section(HANDOVER, texts[HANDOVER], "## Exact Next Action")
    if following != "## Hard-stop Reminder":
        fail("E_CONTROL_SECTION", f"{HANDOVER}:following={following!r}")


def validate_human_controls() -> None:
    validate_human_control_texts({path: read_text(path) for path in (RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)})


def ref_value(ref: str) -> str:
    raw = git_bytes(["show-ref", "--verify", ref]).decode("ascii", "strict").strip().split(" ")
    if len(raw) != 2 or raw[1] != ref or not is_hex40(raw[0]):
        fail("E_REF_FORM", ref)
    return raw[0]


def expected_boundary_snapshot(expected_head: str) -> dict[str, Any]:
    return {
        "branch": ACTIVE_BRANCH,
        "head": expected_head,
        "upstream": ACTIVE_UPSTREAM,
        "origin_url": ORIGIN_URL,
        "cached_refs": {
            ACTIVE_LOCAL_REF: expected_head,
            ACTIVE_TRACKING_REF: expected_head,
            PROTECTED_REF: PROTECTED_TIP,
            MAIN_REF: MAIN_TIP,
            CLAUDE_REF: CLAUDE_TIP,
            CODEX_REF: CODEX_TIP,
        },
        "live_refs": {
            ACTIVE_LIVE_REF: expected_head,
            PROTECTED_LIVE_REF: PROTECTED_TIP,
            MAIN_LIVE_REF: MAIN_TIP,
            CLAUDE_LIVE_REF: CLAUDE_TIP,
            CODEX_LIVE_REF: CODEX_TIP,
        },
    }


def validate_boundary_snapshot(snapshot: dict[str, Any], expected_head: str) -> None:
    expected = expected_boundary_snapshot(expected_head)
    if snapshot.get("branch") != expected["branch"] or snapshot.get("head") != expected["head"]:
        fail("E_BOUNDARY_LOCAL")
    if snapshot.get("upstream") != expected["upstream"] or snapshot.get("origin_url") != expected["origin_url"]:
        fail("E_BOUNDARY_UPSTREAM")
    if snapshot.get("cached_refs") != expected["cached_refs"]:
        fail("E_BOUNDARY_CACHED")
    if snapshot.get("live_refs") != expected["live_refs"]:
        fail("E_BOUNDARY_LIVE")
    if set(snapshot) != set(expected):
        fail("E_BOUNDARY_FIELDS")


def boundary_snapshot() -> dict[str, Any]:
    return {
        "branch": git_text(["symbolic-ref", "--quiet", "--short", "HEAD"]),
        "head": git_text(["rev-parse", "HEAD"]),
        "upstream": git_text(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"]),
        "origin_url": git_text(["remote", "get-url", "origin"]),
        "cached_refs": {
            ref: ref_value(ref)
            for ref in (ACTIVE_LOCAL_REF, ACTIVE_TRACKING_REF, PROTECTED_REF, MAIN_REF, CLAUDE_REF, CODEX_REF)
        },
        "live_refs": {
            ref: live_ref(ref)
            for ref in (ACTIVE_LIVE_REF, PROTECTED_LIVE_REF, MAIN_LIVE_REF, CLAUDE_LIVE_REF, CODEX_LIVE_REF)
        },
    }


def validate_local_boundary(expected_head: str = EXPECTED_PARENT) -> None:
    validate_boundary_snapshot(boundary_snapshot(), expected_head)


def status_entries() -> list[tuple[str, str]]:
    raw = git_bytes(["status", "--porcelain=v1", "-z", "--untracked-files=all"])
    chunks = raw.split(b"\0")
    if chunks and chunks[-1] == b"":
        chunks.pop()
    result = []
    for chunk in chunks:
        if len(chunk) < 4 or chunk[2:3] != b" ":
            fail("E_STATUS_FORM")
        result.append((chunk[:2].decode("ascii", "strict"), chunk[3:].decode("utf-8", "strict")))
    return result


def file_byte_identity_snapshot(paths: Iterable[str]) -> tuple[tuple[str, bool, int | None, str | None], ...]:
    result: list[tuple[str, bool, int | None, str | None]] = []
    for path in paths:
        target = ROOT / path
        if not target.is_file():
            result.append((path, False, None, None))
            continue
        raw = target.read_bytes()
        result.append((path, True, len(raw), sha256(raw)))
    return tuple(result)


def transaction_snapshot(paths: Iterable[str]) -> dict[str, Any]:
    return {
        "boundary": boundary_snapshot(),
        "status": tuple(sorted(status_entries())),
        "file_identities": file_byte_identity_snapshot(paths),
    }


def pre_json_transaction_snapshot() -> dict[str, Any]:
    return transaction_snapshot(PRE_JSON_SIX)


def content_transaction_snapshot() -> dict[str, Any]:
    return transaction_snapshot(EXACT_EIGHT)


def validate_exact_pre_json_status(entries: Iterable[tuple[str, str]]) -> None:
    actual = list(entries)
    expected = [
        ("??" if EXPECTED_STATUS[path] == "A" else " M", path)
        for path in PRE_JSON_SIX
    ]
    if sorted(actual) != sorted(expected):
        fail("E_PRE_JSON_STATUS", repr(actual))


def validate_exact_output_status(entries: Iterable[tuple[str, str]]) -> None:
    actual = list(entries)
    expected = [
        ("??" if EXPECTED_STATUS[path] == "A" else " M", path)
        for path in EXACT_EIGHT
    ]
    if sorted(actual) != sorted(expected):
        fail("E_POST_JSON_STATUS", repr(actual))


def validate_pre_json() -> None:
    validate_local_boundary()
    for path in PRE_JSON_SIX:
        if not (ROOT / path).is_file():
            fail("E_INPUT_MISSING", path)
    for path in (INVENTORY, ATTESTATION):
        if (ROOT / path).exists():
            fail("E_REFUSE_OVERWRITE", path)
    validate_exact_pre_json_status(status_entries())
    validate_human_controls()
    validate_source_guard()


def import_signature(tree: ast.Module) -> tuple[tuple[Any, ...], ...]:
    result: list[tuple[Any, ...]] = []
    imports = sorted((node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))), key=lambda node: (node.lineno, node.col_offset))
    for node in imports:
        if isinstance(node, ast.Import):
            result.append(("import", tuple((alias.name, alias.asname) for alias in node.names)))
        else:
            result.append(("from", node.level, node.module, tuple((alias.name, alias.asname) for alias in node.names)))
    return tuple(result)


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        return None if parent is None else f"{parent}.{node.attr}"
    return None


def is_destructive_path_replace(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "replace"
        and isinstance(node.value, ast.Call)
        and dotted_name(node.value.func) == "Path"
    )


class CapabilityVisitor(ast.NodeVisitor):
    def __init__(self, path: str) -> None:
        self.path = path
        self.functions: list[str] = []
        self.calls: Counter[tuple[str, str]] = Counter()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.functions.append(node.name)
        self.generic_visit(node)
        self.functions.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Call(self, node: ast.Call) -> None:
        if not isinstance(node.func, (ast.Name, ast.Attribute)):
            fail("E_SOURCE_CAPABILITY", f"{self.path}:{node.lineno}:dynamic-call={type(node.func).__name__}")
        target = dotted_name(node.func)
        tail = node.func.attr if isinstance(node.func, ast.Attribute) else (target.rsplit(".", 1)[-1] if target is not None else None)
        owner = ".".join(self.functions) or "<module>"
        if is_destructive_path_replace(node.func):
            fail("E_SOURCE_CAPABILITY", f"{self.path}:{node.lineno}:Path.replace")
        if target in {"eval", "exec", "compile", "open", "__import__"}:
            fail("E_SOURCE_CAPABILITY", f"{self.path}:{node.lineno}:{target}")
        if target == "getattr" and node.args and dotted_name(node.args[0]) in {"os", "subprocess", "tempfile"}:
            fail("E_SOURCE_CAPABILITY", f"{self.path}:{node.lineno}:getattr")
        if target is not None and (
            target.split(".", 1)[0] in {"os", "subprocess", "tempfile"}
            or target == "run"
            or tail in {"run", "Popen", "call", "check_call", "check_output", "open", "write", "write_bytes", "write_text", "unlink", "rename", "link", "symlink_to", "mkdir", "rmdir", "touch", "chmod", "flush"}
        ):
            self.calls[(owner, target)] += 1
        elif tail in {"run", "Popen", "call", "check_call", "check_output", "open", "write", "write_bytes", "write_text", "unlink", "rename", "link", "symlink_to", "mkdir", "rmdir", "touch", "chmod", "flush"}:
            self.calls[(owner, f"<dynamic>.{tail}")] += 1
        self.generic_visit(node)

    def reject_sensitive_alias(self, node: ast.AST, value: ast.AST | None) -> None:
        if value is None:
            return
        target = dotted_name(value)
        tail = value.attr if isinstance(value, ast.Attribute) else (target.rsplit(".", 1)[-1] if target is not None else None)
        if is_destructive_path_replace(value):
            fail("E_SOURCE_CAPABILITY", f"{self.path}:{getattr(node, 'lineno', 0)}:alias=Path.replace")
        if target in {"run", "open", "eval", "exec", "compile", "__import__"} or (target is not None and target.split(".", 1)[0] in {"os", "subprocess", "tempfile"}) or tail in {"run", "Popen", "call", "check_call", "check_output", "open", "write", "write_bytes", "write_text", "unlink", "rename", "link", "symlink_to", "mkdir", "rmdir", "rmtree", "touch", "chmod"}:
            fail("E_SOURCE_CAPABILITY", f"{self.path}:{getattr(node, 'lineno', 0)}:alias={target or tail}")

    def visit_Assign(self, node: ast.Assign) -> None:
        self.reject_sensitive_alias(node, node.value)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.reject_sensitive_alias(node, node.value)
        self.generic_visit(node)

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        self.reject_sensitive_alias(node, node.value)
        self.generic_visit(node)


def validate_module_body(path: str, tree: ast.Module) -> None:
    expected_initializers = {
        "ROOT": ast.dump(ast.parse("ROOT = Path(__file__).resolve().parents[3]").body[0].value, include_attributes=False),
        "GIT_ORDERED_EIGHT": ast.dump(ast.parse("GIT_ORDERED_EIGHT = tuple(sorted(EXACT_EIGHT))").body[0].value, include_attributes=False),
        "HEX40": ast.dump(ast.parse("HEX40 = set('0123456789abcdef')").body[0].value, include_attributes=False),
    }
    for index, node in enumerate(tree.body):
        if index == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            value = node.value
            calls = [item for item in ast.walk(value) if isinstance(item, ast.Call)] if value is not None else []
            target = node.targets[0].id if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) else None
            if calls and not (path == VALIDATOR and target in expected_initializers and ast.dump(value, include_attributes=False) == expected_initializers[target]):
                fail("E_SOURCE_MODULE_BODY", f"{path}:{node.lineno}:initializer")
            continue
        if isinstance(node, ast.If) and index == len(tree.body) - 1:
            test = node.test
            exact_test = isinstance(test, ast.Compare) and isinstance(test.left, ast.Name) and test.left.id == "__name__" and len(test.ops) == 1 and isinstance(test.ops[0], ast.Eq) and len(test.comparators) == 1 and isinstance(test.comparators[0], ast.Constant) and test.comparators[0].value == "__main__"
            exact_body = len(node.body) == 1 and not node.orelse and isinstance(node.body[0], ast.Raise) and isinstance(node.body[0].exc, ast.Call) and dotted_name(node.body[0].exc.func) == "SystemExit" and len(node.body[0].exc.args) == 1 and isinstance(node.body[0].exc.args[0], ast.Call) and dotted_name(node.body[0].exc.args[0].func) == "main" and not node.body[0].exc.args[0].args and not node.body[0].exc.args[0].keywords
            if exact_test and exact_body:
                continue
        fail("E_SOURCE_MODULE_BODY", f"{path}:{node.lineno}:{type(node).__name__}")


def builder_assignment_call(node: ast.AST, target: str) -> ast.Call | None:
    if not isinstance(node, ast.Assign) or len(node.targets) != 1:
        return None
    names = node.targets[0]
    if not isinstance(names, ast.Tuple) or [item.id for item in names.elts if isinstance(item, ast.Name)] != ["inventory", "attestation"] or len(names.elts) != 2:
        return None
    call = node.value
    if not isinstance(call, ast.Call) or dotted_name(call.func) != target or call.args or call.keywords:
        return None
    return call


def validate_builder_sensitive_context(tree: ast.Module) -> None:
    mains = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main"]
    if len(mains) != 1:
        fail("E_BUILDER_CONTRACT", "main")
    tries = [node for node in mains[0].body if isinstance(node, ast.Try)]
    if len(tries) != 1:
        fail("E_BUILDER_CONTRACT", "try")
    body = tries[0].body
    previews = [node for node in body if isinstance(node, ast.If) and dotted_name(node.test) == "args.preview_digests" and not node.orelse]
    if len(previews) != 1:
        fail("E_BUILDER_CONTRACT", "preview-context")
    preview = previews[0]
    deterministic = [(node, builder_assignment_call(node, "contract.deterministic_pair")) for node in preview.body]
    deterministic = [(node, call) for node, call in deterministic if call is not None]
    collectors = [(node, builder_assignment_call(node, "contract.collect_payloads")) for node in body]
    collectors = [(node, call) for node, call in collectors if call is not None]
    if len(deterministic) != 1 or len(collectors) != 1 or body.index(preview) >= body.index(collectors[0][0]):
        fail("E_BUILDER_CONTRACT", "collector-context")
    allowed_refs = {id(deterministic[0][1].func), id(collectors[0][1].func)}
    sensitive_refs = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and dotted_name(node) in {"contract.collect_payloads", "contract.deterministic_pair"}
    ]
    if len(sensitive_refs) != 2 or {id(node) for node in sensitive_refs} != allowed_refs:
        fail("E_BUILDER_CONTRACT", "collector-reference")


def validate_source_texts(validator: str, builder: str) -> None:
    trees: dict[str, ast.Module] = {}
    for path, text in ((VALIDATOR, validator), (BUILDER, builder)):
        try:
            trees[path] = ast.parse(text, filename=path)
        except SyntaxError as exc:
            fail("E_SOURCE_SYNTAX", f"{path}:{exc}")
        validate_module_body(path, trees[path])
    if any(isinstance(node, ast.Name) and node.id == "_PDF" + "_CACHE" and isinstance(node.ctx, ast.Store) for node in ast.walk(trees[VALIDATOR])):
        fail("E_SOURCE_PDF_CACHE")
    expected_validator_imports = (
        ("from", 0, "__future__", (("annotations", None),)),
        ("import", (("argparse", None),)),
        ("import", (("ast", None),)),
        ("import", (("copy", None),)),
        ("import", (("hashlib", None),)),
        ("import", (("json", None),)),
        ("import", (("math", None),)),
        ("import", (("os", None),)),
        ("from", 0, "pathlib", (("Path", None), ("PurePosixPath", None))),
        ("import", (("struct", None),)),
        ("import", (("subprocess", None),)),
        ("import", (("sys", None),)),
        ("import", (("tempfile", None),)),
        ("from", 0, "typing", (("Any", None), ("Iterable", None))),
        ("from", 0, "collections", (("Counter", None),)),
    )
    expected_builder_imports = (
        ("from", 0, "__future__", (("annotations", None),)),
        ("import", (("argparse", None),)),
        ("import", (("sys", None),)),
        ("import", (("validate_phase068_step92", "contract"),)),
    )
    if import_signature(trees[VALIDATOR]) != expected_validator_imports:
        fail("E_SOURCE_IMPORT", VALIDATOR)
    if import_signature(trees[BUILDER]) != expected_builder_imports:
        fail("E_SOURCE_IMPORT", BUILDER)

    validator_visitor = CapabilityVisitor(VALIDATOR)
    validator_visitor.visit(trees[VALIDATOR])
    expected_capabilities = Counter({
        ("run", "subprocess.run"): 1,
        ("validate_process_argv", "tempfile.gettempdir"): 1,
        ("git_bytes", "run"): 1,
        ("inspect_pdf", "tempfile.TemporaryDirectory"): 1,
        ("inspect_pdf", "source.write_bytes"): 1,
        ("inspect_pdf", "run"): 2,
        ("external_payload_pair", "tempfile.TemporaryDirectory"): 1,
        ("external_payload_pair", "target.open"): 1,
        ("external_payload_pair", "handle.write"): 1,
        ("external_payload_pair", "handle.flush"): 1,
        ("external_payload_pair", "os.fsync"): 1,
        ("atomic_temp", "tempfile.mkstemp"): 1,
        ("atomic_temp", "os.fdopen"): 1,
        ("atomic_temp", "handle.write"): 1,
        ("atomic_temp", "handle.flush"): 1,
        ("atomic_temp", "os.fsync"): 1,
        ("atomic_temp", "path.unlink"): 1,
        ("collect_payloads", "tempfile.gettempdir"): 1,
        ("collect_payloads", "os.open"): 1,
        ("collect_payloads", "os.write"): 1,
        ("collect_payloads", "os.link"): 1,
        ("collect_payloads", "temp.unlink"): 2,
        ("collect_payloads", "destination.unlink"): 1,
        ("collect_payloads", "os.close"): 1,
        ("collect_payloads", "lock.unlink"): 1,
        ("staged_snapshot", "run"): 1,
    })
    if validator_visitor.calls != expected_capabilities:
        fail("E_SOURCE_CAPABILITY", repr(validator_visitor.calls - expected_capabilities))

    validate_builder_sensitive_context(trees[BUILDER])
    builder_calls: Counter[tuple[str, str]] = Counter()
    builder_visitor = CapabilityVisitor(BUILDER)
    builder_visitor.visit(trees[BUILDER])
    if builder_visitor.calls:
        fail("E_SOURCE_CAPABILITY", f"{BUILDER}:{builder_visitor.calls!r}")
    functions: list[str] = []

    class BuilderContractVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            functions.append(node.name)
            self.generic_visit(node)
            functions.pop()

        def visit_Call(self, node: ast.Call) -> None:
            target = dotted_name(node.func)
            if target is not None and target.startswith("contract."):
                builder_calls[(".".join(functions) or "<module>", target)] += 1
            self.generic_visit(node)

    BuilderContractVisitor().visit(trees[BUILDER])
    expected_builder_calls = Counter({
        ("run_self_tests", "contract.run_self_tests"): 1,
        ("run_self_tests", "contract.fail"): 2,
        ("main", "contract.validate_source_guard"): 1,
        ("main", "contract.validate_pre_json"): 1,
        ("main", "contract.deterministic_pair"): 1,
        ("main", "contract.sha256"): 4,
        ("main", "contract.collect_payloads"): 1,
    })
    if builder_calls != expected_builder_calls:
        fail("E_BUILDER_CONTRACT", repr(builder_calls - expected_builder_calls))


def validate_source_guard() -> None:
    validator, builder = validate_reviewed_source_identity(
        (ROOT / VALIDATOR).read_bytes(),
        (ROOT / BUILDER).read_bytes(),
        read_text(RESULT),
    )
    validate_source_texts(validator, builder)


def external_payload_pair() -> tuple[bytes, bytes]:
    inventory, attestation = build_payload_objects()
    raw = (canonical_bytes(inventory), canonical_bytes(attestation))
    with tempfile.TemporaryDirectory(prefix="p068-step92-payload-") as directory:
        external_root = Path(directory).resolve()
        try:
            external_root.relative_to(ROOT.resolve())
        except ValueError:
            pass
        else:
            fail("E_PAYLOAD_TEMP_INSIDE_REPOSITORY")
        reread: list[bytes] = []
        for name, payload in (("inventory.json", raw[0]), ("attestation.json", raw[1])):
            target = external_root / name
            with target.open("wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            reread.append(target.read_bytes())
    pair = (reread[0], reread[1])
    if pair != raw or strict_load(pair[0]) != inventory or strict_load(pair[1]) != attestation:
        fail("E_PAYLOAD_ROUNDTRIP")
    return pair


def deterministic_pair() -> tuple[bytes, bytes]:
    pairs = []
    for _ in range(2):
        pairs.append(external_payload_pair())
    if pairs[0] != pairs[1]:
        fail("E_PAYLOAD_NONDETERMINISTIC")
    return pairs[0]


def atomic_temp(destination: Path, raw: bytes) -> Path:
    descriptor, name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
    path = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        if path.read_bytes() != raw:
            fail("E_TEMP_REREAD", destination.as_posix())
        return path
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def collect_payloads() -> tuple[bytes, bytes]:
    validate_pre_json()
    before = pre_json_transaction_snapshot()
    validate_boundary_snapshot(before["boundary"], EXPECTED_PARENT)
    validate_exact_pre_json_status(before["status"])
    inventory_raw, attestation_raw = deterministic_pair()
    require_snapshot_equal(before, pre_json_transaction_snapshot(), "E_COLLECT_SNAPSHOT_DRIFT")
    lock_name = "p068-step92-" + sha256(str(ROOT.resolve()).encode("utf-8"))[:16] + ".lock"
    lock = Path(tempfile.gettempdir()) / lock_name
    descriptor: int | None = None
    temps: list[Path] = []
    published: list[tuple[Path, bytes]] = []
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.write(descriptor, b"P068_STEP92\n")
        for rel, raw in ((INVENTORY,inventory_raw),(ATTESTATION,attestation_raw)):
            destination = ROOT / rel
            temp = atomic_temp(destination, raw)
            temps.append(temp)
            try:
                os.link(temp, destination)
            except FileExistsError:
                fail("E_REFUSE_OVERWRITE_RACE", rel)
            published.append((destination, raw))
            temp.unlink()
            temps.remove(temp)
        validate_content()
        return inventory_raw, attestation_raw
    except FileExistsError:
        fail("E_COLLECT_LOCKED", str(lock))
    except BaseException:
        for destination, raw in reversed(published):
            if destination.is_file() and destination.read_bytes() == raw:
                destination.unlink()
        raise
    finally:
        for temp in temps:
            temp.unlink(missing_ok=True)
        if descriptor is not None:
            os.close(descriptor)
            lock.unlink(missing_ok=True)


def validate_json_payloads() -> tuple[dict[str, Any], dict[str, Any]]:
    stored_raw = ((ROOT / INVENTORY).read_bytes(), (ROOT / ATTESTATION).read_bytes())
    stored = (strict_load(stored_raw[0]), strict_load(stored_raw[1]))
    rebuilt = build_payload_objects()
    if stored_raw != (canonical_bytes(rebuilt[0]), canonical_bytes(rebuilt[1])) or stored != rebuilt:
        fail("E_STORED_PAYLOAD_MISMATCH")
    return stored


def validate_output_files() -> None:
    for path in EXACT_EIGHT:
        if not (ROOT / path).is_file():
            fail("E_OUTPUT_MISSING", path)


def validate_output_payloads() -> None:
    validate_source_guard()
    validate_human_controls()
    validate_json_payloads()


def validate_output_content() -> None:
    validate_output_files()
    validate_output_payloads()


def validate_content() -> None:
    validate_output_files()
    before = content_transaction_snapshot()
    validate_boundary_snapshot(before["boundary"], EXPECTED_PARENT)
    validate_exact_output_status(before["status"])
    validate_output_payloads()
    require_snapshot_equal(before, content_transaction_snapshot(), "E_CONTENT_SNAPSHOT_DRIFT")


def parse_index_diff(raw: bytes) -> list[dict[str, str]]:
    return parse_raw_diff(raw)


def worktree_blob_oid(path: str) -> str:
    raw = (ROOT / path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def index_worktree_snapshot() -> dict[str, dict[str, str]]:
    chunks = git_bytes(["ls-files", "--stage", "-z", "--", *EXACT_EIGHT]).split(b"\0")
    chunks = [chunk for chunk in chunks if chunk]
    result: dict[str, dict[str, str]] = {}
    for chunk in chunks:
        meta, separator, path_raw = chunk.partition(b"\t")
        if separator != b"\t":
            fail("E_STAGE_FORM")
        mode, oid, stage = meta.decode("ascii", "strict").split(" ")
        path = path_raw.decode("utf-8", "strict")
        if path in result:
            fail("E_STAGE_FORM", path)
        result[path] = {"mode": mode, "oid": oid, "stage": stage, "worktree_oid": worktree_blob_oid(path)}
    return result


def validate_blob_bindings(records: list[dict[str, str]], index: dict[str, dict[str, str]], expected_paths: tuple[str, ...], code: str) -> None:
    if tuple(item["path"] for item in records) != expected_paths or set(index) != set(expected_paths):
        fail(code, "paths")
    for item in records:
        row = index[item["path"]]
        if row.get("mode") != "100644" or row.get("stage") != "0" or not is_hex40(row.get("oid", "")) or item.get("new_blob") != row.get("oid") or row.get("worktree_oid") != row.get("oid"):
            fail(code, item["path"])


def require_snapshot_equal(before: dict[str, Any], after: dict[str, Any], code: str) -> None:
    if before != after:
        fail(code)


def staged_snapshot() -> dict[str, Any]:
    raw = git_bytes(["diff", "--cached", "--raw", "-z", "--abbrev=40", EXPECTED_PARENT, "--"])
    return {
        "boundary": boundary_snapshot(),
        "head": git_text(["rev-parse", "HEAD"]),
        "status": tuple(status_entries()),
        "unstaged_clean": run(["git", "diff", "--quiet", "--"]).returncode == 0,
        "raw": raw,
        "records": parse_index_diff(raw),
        "index": index_worktree_snapshot(),
    }


def validate_staged() -> None:
    before = staged_snapshot()
    records = before["records"]
    validate_boundary_snapshot(before["boundary"], EXPECTED_PARENT)
    if before["head"] != EXPECTED_PARENT:
        fail("E_STAGED_HEAD")
    if not before["unstaged_clean"]:
        fail("E_UNSTAGED_DIFF")
    if [item["path"] for item in records] != list(GIT_ORDERED_EIGHT):
        fail("E_STAGED_PATHS", repr([item["path"] for item in records]))
    for item in records:
        path = item["path"]
        if (item["status"],item["old_mode"],item["new_mode"]) != (EXPECTED_STATUS[path],EXPECTED_OLD_MODE[path],"100644"):
            fail("E_STAGED_STATUS", path)
    expected_status = sorted([(("A " if EXPECTED_STATUS[path] == "A" else "M "), path) for path in EXACT_EIGHT])
    if sorted(before["status"]) != expected_status:
        fail("E_STAGED_PORCELAIN", repr(before["status"]))
    validate_blob_bindings(records, before["index"], GIT_ORDERED_EIGHT, "E_STAGED_BLOB_BINDING")
    validate_output_content()
    require_snapshot_equal(before, staged_snapshot(), "E_STAGED_SNAPSHOT_DRIFT")


def live_ref(ref: str) -> str:
    raw = git_bytes(["ls-remote", "--exit-code", "origin", ref]).decode("ascii", "strict").splitlines()
    if len(raw) != 1:
        fail("E_LIVE_REF_COUNT", ref)
    oid, name = raw[0].split("\t")
    if name != ref or not is_hex40(oid):
        fail("E_LIVE_REF_FORM", ref)
    return oid


def persistence_boundary_snapshot() -> dict[str, Any]:
    return {
        "boundary": boundary_snapshot(),
        "branch": git_text(["symbolic-ref", "--quiet", "--short", "HEAD"]),
        "head": git_text(["rev-parse", "HEAD"]),
        "upstream": git_text(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"]),
        "status": tuple(status_entries()),
        "refs": {
            ref: ref_value(ref)
            for ref in (ACTIVE_LOCAL_REF, ACTIVE_TRACKING_REF, PROTECTED_REF, MAIN_REF, CLAUDE_REF, CODEX_REF)
        },
    }


def validate_persistence(expected_commit: str) -> None:
    if not is_hex40(expected_commit):
        fail("E_EXPECTED_COMMIT_FORM")
    before = persistence_boundary_snapshot()
    expected_refs = {
        ACTIVE_LOCAL_REF: expected_commit,
        ACTIVE_TRACKING_REF: expected_commit,
        PROTECTED_REF: PROTECTED_TIP,
        MAIN_REF: MAIN_TIP,
        CLAUDE_REF: CLAUDE_TIP,
        CODEX_REF: CODEX_TIP,
    }
    if before != {"boundary": expected_boundary_snapshot(expected_commit), "branch": ACTIVE_BRANCH, "head": expected_commit, "upstream": ACTIVE_UPSTREAM, "status": (), "refs": expected_refs}:
        fail("E_PERSISTENCE_BOUNDARY", repr(before))
    record, _ = parse_commit(expected_commit)
    if tuple(record["parents"]) != (EXPECTED_PARENT,) or record["subject"] != EXPECTED_SUBJECT:
        fail("E_PERSISTENCE_COMMIT")
    changes, _ = raw_diff(EXPECTED_PARENT, expected_commit)
    if [item["path"] for item in changes] != list(GIT_ORDERED_EIGHT):
        fail("E_PERSISTENCE_PATHS")
    for item in changes:
        path = item["path"]
        if (item["status"],item["old_mode"],item["new_mode"]) != (EXPECTED_STATUS[path],EXPECTED_OLD_MODE[path],"100644"):
            fail("E_PERSISTENCE_STATUS", path)
        if not is_hex40(item["new_blob"]) or object_bytes(item["new_blob"], "blob") != (ROOT / path).read_bytes():
            fail("E_PERSISTENCE_WORKTREE", path)
    validate_source_guard()
    validate_human_controls()
    validate_json_payloads()
    if live_ref(ACTIVE_LIVE_REF) != expected_commit:
        fail("E_LIVE_ACTIVE")
    for ref, tip in ((PROTECTED_LIVE_REF,PROTECTED_TIP),(MAIN_LIVE_REF,MAIN_TIP),(CLAUDE_LIVE_REF,CLAUDE_TIP),(CODEX_LIVE_REF,CODEX_TIP)):
        if live_ref(ref) != tip:
            fail("E_LIVE_PROTECTED", ref)
    require_snapshot_equal(before, persistence_boundary_snapshot(), "E_PERSISTENCE_SNAPSHOT_DRIFT")


def expect_failure(callback: Any, code: str) -> None:
    try:
        callback()
    except ValidationError as exc:
        if exc.code != code:
            fail("E_SELFTEST_CODE", f"{exc.code}!={code}")
    else:
        fail("E_SELFTEST_ACCEPTED", code)


def restoring_payload_negative(inventory: dict[str, Any], attestation: dict[str, Any], mutation: Any) -> Any:
    def callback() -> None:
        saved_inventory, saved_attestation = copy.deepcopy((inventory, attestation))
        try:
            mutation(inventory, attestation)
            validate_payload_contract(inventory, attestation)
        finally:
            inventory.clear()
            inventory.update(saved_inventory)
            attestation.clear()
            attestation.update(saved_attestation)
    return callback


def run_named_negative_controls(callbacks: dict[str, Any], inventory: dict[str, Any], attestation: dict[str, Any]) -> tuple[int, str]:
    ids = [item["id"] for item in NEGATIVE_CONTROL_SPECS]
    if len(ids) != len(set(ids)) or set(callbacks) != set(ids):
        fail("E_SELFTEST_NEGATIVE_REGISTRY", "callback binding")
    for item in NEGATIVE_CONTROL_SPECS:
        before = canonical_bytes({"inventory": inventory, "attestation": attestation})
        try:
            expect_failure(callbacks[item["id"]], item["error"])
        finally:
            after = canonical_bytes({"inventory": inventory, "attestation": attestation})
            if after != before:
                fail("E_SELFTEST_MUTATION_LEAK", item["id"])
    projection = negative_control_registry()
    return len(ids), projection["digest"]


def run_contract_repair_helper_self_tests() -> int:
    """Temp-free RED/GREEN checks for the Step 92 contract repair helpers."""

    tests = 0
    identity, timestamp, timezone = parse_actor_clock("Codex <codex@openai.com> 1785147286 +0900", "author")
    if (identity, timestamp, timezone) != ("Codex <codex@openai.com>", 1785147286, "+0900"):
        fail("E_SELFTEST_ACTOR_CLOCK")
    tests += 1
    raw = b":000000 100644 " + b"0" * 40 + b" " + b"1" * 40 + b" A\0a\0"
    rows = parse_raw_diff(raw)
    if len(rows) != 1 or rows[0].get("raw_extent") != {
        "byte_start": 0,
        "byte_end": len(raw),
        "meta_byte_start": 0,
        "meta_byte_end": raw.index(b"\0"),
        "path_byte_start": raw.index(b"\0") + 1,
        "path_byte_end": len(raw) - 1,
    }:
        fail("E_SELFTEST_RAW_EXTENT")
    tests += 1
    snapshot = expected_boundary_snapshot(EXPECTED_PARENT)
    validate_boundary_snapshot(snapshot, EXPECTED_PARENT)
    tests += 1
    wrong_upstream = copy.deepcopy(snapshot)
    wrong_upstream["upstream"] = "origin/main"
    expect_failure(lambda: validate_boundary_snapshot(wrong_upstream, EXPECTED_PARENT), "E_BOUNDARY_UPSTREAM")
    tests += 1
    stale_live = copy.deepcopy(snapshot)
    stale_live["live_refs"][MAIN_LIVE_REF] = "f" * 40
    expect_failure(lambda: validate_boundary_snapshot(stale_live, EXPECTED_PARENT), "E_BOUNDARY_LIVE")
    tests += 1
    post_json_status = [
        ("??" if EXPECTED_STATUS[path] == "A" else " M", path)
        for path in EXACT_EIGHT
    ]
    validate_exact_output_status(post_json_status)
    tests += 1
    return tests


def inject_before_main(source: str, payload: str) -> str:
    anchor = '\n\nif __name__ == "__main__":\n'
    if source.count(anchor) != 1:
        fail("E_SELFTEST_SOURCE_ANCHOR")
    return source.replace(anchor, payload + anchor, 1)


def run_self_tests() -> int:
    tests = 0
    tests += run_contract_repair_helper_self_tests()
    control_texts = {path: read_text(path) for path in (RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)}
    validate_human_control_texts(control_texts); tests += 1
    stale = dict(control_texts)
    stale[PARENT_LEDGER] = stale[PARENT_LEDGER].replace(
        f"Current-state marker: `{PRECOMMIT_MARKER}`",
        "Current-state marker: `P068_STEP91_CLAUDE_FORK_READ_PRECOMMIT`",
        1,
    )
    expect_failure(lambda: validate_human_control_texts(stale), "E_CONTROL_MARKER"); tests += 1
    duplicate = dict(control_texts)
    duplicate[ACTIVE_LEDGER] = duplicate[ACTIVE_LEDGER].replace(
        f"Current-state marker: `{PRECOMMIT_MARKER}`",
        f"Current-state marker: `{PRECOMMIT_MARKER}`\nCurrent-state marker: `{PRECOMMIT_MARKER}`",
        1,
    )
    expect_failure(lambda: validate_human_control_texts(duplicate), "E_CONTROL_MARKER"); tests += 1
    marker_history_only = dict(control_texts)
    marker_line = f"Current-state marker: `{PRECOMMIT_MARKER}`"
    marker_history_only[HANDOVER] = marker_history_only[HANDOVER].replace(marker_line + "\n", "", 1).replace(
        "## Canonical Chain\n",
        "## Canonical Chain\n" + marker_line + "\n",
        1,
    )
    expect_failure(lambda: validate_human_control_texts(marker_history_only), "E_CONTROL_MARKER"); tests += 1
    stale_next = dict(control_texts)
    stale_next[ACTIVE_LEDGER] = stale_next[ACTIVE_LEDGER].replace(
        "Execute Step 93 only after dual Step 92 persistence",
        "Execute Step 92 only after dual Step 91 persistence",
        1,
    )
    expect_failure(lambda: validate_human_control_texts(stale_next), "E_CONTROL_SECTION"); tests += 1
    correction_only = dict(control_texts)
    checkpoint = next(line for line in correction_only[ACTIVE_LEDGER].splitlines() if line.startswith("| Phase 068 Step 92 |"))
    correction_only[ACTIVE_LEDGER] = correction_only[ACTIVE_LEDGER].replace(checkpoint + "\n", "", 1).replace(
        "## Next Exact Step\n",
        checkpoint + "\n\n## Next Exact Step\n",
        1,
    )
    expect_failure(lambda: validate_human_control_texts(correction_only), "E_CONTROL_ROW"); tests += 1

    validator_raw = (ROOT / VALIDATOR).read_bytes()
    builder_raw = (ROOT / BUILDER).read_bytes()
    validator_source = read_text(VALIDATOR)
    builder_source = read_text(BUILDER)
    validate_reviewed_source_identity(validator_raw, builder_raw, control_texts[RESULT]); tests += 1
    duplicate_identity_result = control_texts[RESULT].replace(
        SOURCE_IDENTITY_HEADING,
        SOURCE_IDENTITY_HEADING + "\n" + SOURCE_IDENTITY_HEADING,
        1,
    )
    builder_identity_record = (
        f"- builder: {FROZEN_BUILDER_IDENTITY[0]:,} bytes, {FROZEN_BUILDER_IDENTITY[1]:,} lines, SHA-256\n"
        f"  `{FROZEN_BUILDER_IDENTITY[2]}`;"
    )
    if control_texts[RESULT].count(builder_identity_record) != 1:
        fail("E_SELFTEST_SOURCE_ANCHOR", "builder-identity")
    missing_identity_result = control_texts[RESULT].replace(builder_identity_record, "", 1)
    malformed_identity_result = control_texts[RESULT].replace(
        f"`{FROZEN_BUILDER_IDENTITY[2]}`",
        f"`{FROZEN_BUILDER_IDENTITY[2].upper()}`",
        1,
    )
    if malformed_identity_result == control_texts[RESULT]:
        fail("E_SELFTEST_SOURCE_ANCHOR", "builder-hash")
    expect_failure(lambda: parse_reviewed_source_identities(duplicate_identity_result), "E_SOURCE_IDENTITY"); tests += 1
    expect_failure(lambda: parse_reviewed_source_identities(missing_identity_result), "E_SOURCE_IDENTITY"); tests += 1
    expect_failure(lambda: parse_reviewed_source_identities(malformed_identity_result), "E_SOURCE_IDENTITY"); tests += 1
    path_replace_source = inject_before_main(validator_source, "\n\ndef injected_replace():\n    Path('a').replace('b')\n")
    container_run_source = inject_before_main(validator_source, "\n\ndef injected_container():\n    (subprocess.run,)[0](['git','status'])\n")
    path_alias_source = inject_before_main(validator_source, "\n\ndef injected_path_alias():\n    p = Path('a')\n    p.replace('b')\n")
    callable_transport_source = inject_before_main(validator_source, "\n\ndef injected_callable_transport():\n    worker = [subprocess.run][0]\n    worker(['git','status'])\n")
    builder_dead_indirect_source = builder_source.replace(
        "inventory, attestation = contract.collect_payloads()",
        "if False:\n            contract.collect_payloads()\n        inventory, attestation = (contract.deterministic_pair,)[0]()",
        1,
    )
    builder_unreachable_source = builder_source.replace(
        "inventory, attestation = contract.collect_payloads()",
        "pair = getattr(contract, \"deterministic_pair\")\n        inventory, attestation = pair()\n        return 0\n        inventory, attestation = contract.collect_payloads()",
        1,
    )
    validate_source_texts(validator_source, builder_source); tests += 1
    expect_failure(
        lambda: validate_source_texts(validator_source.replace("import subprocess\n", "import subprocess as process\n", 1), builder_source),
        "E_SOURCE_IMPORT",
    ); tests += 1
    expect_failure(
        lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_process():\n    subprocess.Popen(['git', 'status'])\n"), builder_source),
        "E_SOURCE_CAPABILITY",
    ); tests += 1
    expect_failure(
        lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_alias():\n    process = subprocess.run\n    process(['git', 'status'])\n"), builder_source),
        "E_SOURCE_CAPABILITY",
    ); tests += 1
    expect_failure(
        lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_worker():\n    worker = run\n"), builder_source),
        "E_SOURCE_CAPABILITY",
    ); tests += 1
    expect_failure(
        lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_annotated_worker():\n    worker: Any = run\n"), builder_source),
        "E_SOURCE_CAPABILITY",
    ); tests += 1
    expect_failure(
        lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_named_worker():\n    if (worker := run):\n        pass\n"), builder_source),
        "E_SOURCE_CAPABILITY",
    ); tests += 1
    expect_failure(
        lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_loader():\n    loader = __import__\n"), builder_source),
        "E_SOURCE_CAPABILITY",
    ); tests += 1
    expect_failure(
        lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_writer_alias():\n    writer = Path('unexpected').write_text\n"), builder_source),
        "E_SOURCE_CAPABILITY",
    ); tests += 1
    expect_failure(
        lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_nested_import():\n    import shutil\n"), builder_source),
        "E_SOURCE_IMPORT",
    ); tests += 1
    expect_failure(
        lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_writer():\n    Path('unexpected').write_text('x')\n"), builder_source),
        "E_SOURCE_CAPABILITY",
    ); tests += 1
    expect_failure(
        lambda: validate_source_texts(
            validator_source,
            builder_source.replace("inventory, attestation = contract.collect_payloads()", "inventory, attestation = contract.deterministic_pair()", 1),
        ),
        "E_BUILDER_CONTRACT",
    ); tests += 1

    validate_git_argv(["diff-tree", "--no-commit-id", "--raw", "-r", "--abbrev=40", "--no-renames", "-z", BASE, CODEX_TIP, "--"]); tests += 1
    validate_process_argv(["git", "diff", "--quiet", "--"]); tests += 1
    expect_failure(lambda: validate_process_argv(["git", "reset", "--hard"]), "E_GIT_ARGV"); tests += 1
    expect_failure(lambda: validate_git_argv(["rev-parse", "--verify", "HEAD"]), "E_GIT_ARGV"); tests += 1
    expect_failure(lambda: validate_git_argv(["ls-remote", "--exit-code", "origin", ACTIVE_LIVE_REF + "^{}"]), "E_GIT_ARGV"); tests += 1
    expect_failure(lambda: validate_git_argv(["diff", "--cached", "--raw", "-z", EXPECTED_PARENT, "--"]), "E_GIT_ARGV"); tests += 1
    expect_failure(lambda: validate_git_argv(["diff-tree", "--no-commit-id", "--raw", "-r", "--abbrev=39", "--no-renames", "-z", BASE, CODEX_TIP, "--"]), "E_GIT_ARGV"); tests += 1
    binding_record = [{"path": "x", "new_blob": "a" * 40}]
    binding_index = {"x": {"mode": "100644", "stage": "0", "oid": "b" * 40, "worktree_oid": "b" * 40}}
    expect_failure(lambda: validate_blob_bindings(binding_record, binding_index, ("x",), "E_SELFTEST_BLOB_BINDING"), "E_SELFTEST_BLOB_BINDING"); tests += 1
    expect_failure(lambda: require_snapshot_equal({"head": "a"}, {"head": "b"}, "E_SELFTEST_SNAPSHOT_DRIFT"), "E_SELFTEST_SNAPSHOT_DRIFT"); tests += 1

    sample = {"schema":"x","semantic_sha256":""}
    sample["semantic_sha256"] = semantic_sha(sample)
    raw = canonical_bytes(sample)
    if strict_load(raw) != sample:
        fail("E_SELFTEST_ROUNDTRIP")
    tests += 1
    expect_failure(lambda: strict_load(b'{"a":1,"a":2}\n'), "E_JSON_DUPLICATE_KEY"); tests += 1
    expect_failure(lambda: strict_load(b'{"a":NaN}\n'), "E_JSON_NONFINITE"); tests += 1
    expect_failure(lambda: strict_load(raw.replace(b"\n", b"\r\n")), "E_OUTPUT_JSON_FORM"); tests += 1
    expect_failure(lambda: parse_raw_diff(b":000000 100644 " + b"0"*40 + b" " + b"1"*40 + b" R100\0a\0"), "E_DIFF_STATUS_OR_DUPLICATE"); tests += 1
    inventory, attestation = build_payload_objects()
    pristine = (canonical_bytes(inventory),canonical_bytes(attestation))
    mutations = [
        (lambda a,b: a.update(edge_path_event_count=134), "E_CONTRACT_EDGES"),
        (lambda a,b: a.update(net_path_count=68), "E_CONTRACT_NET"),
        (lambda a,b: b.update(text_blob_count=80), "E_CONTRACT_MEDIA"),
        (lambda a,b: a.update(scientific_truth_promotions=1), "E_CONTRACT_PROMOTION"),
        (lambda a,b: b.update(coverage_gaps=["gap"]), "E_CONTRACT_GAPS"),
    ]
    for mutate, code in mutations:
        left, right = copy.deepcopy((inventory,attestation))
        mutate(left,right)
        expect_failure(lambda left=left,right=right: validate_payload_contract(left,right), code)
        tests += 1
    if pristine != (canonical_bytes(inventory),canonical_bytes(attestation)):
        fail("E_SELFTEST_MUTATION_LEAK")
    tests += 1

    deep_json = b'{"a":' + b'[' * (MAX_JSON_DEPTH + 1) + b'0' + b']' * (MAX_JSON_DEPTH + 1) + b'}\n'
    upstream_snapshot = expected_boundary_snapshot(EXPECTED_PARENT)
    upstream_snapshot["upstream"] = "origin/main"
    live_snapshot = expected_boundary_snapshot(EXPECTED_PARENT)
    live_snapshot["live_refs"][MAIN_LIVE_REF] = "f" * 40
    post_json_status = [
        ("??" if EXPECTED_STATUS[path] == "A" else " M", path)
        for path in EXACT_EIGHT
    ]
    post_json_extra_path = [*post_json_status, ("??", "unexpected/post-json-path")]
    post_json_staged_drift = [
        (("A " if path == INVENTORY else status), path)
        for status, path in post_json_status
    ]
    content_snapshot_sample = {
        "boundary": expected_boundary_snapshot(EXPECTED_PARENT),
        "status": tuple(sorted(post_json_status)),
        "file_identities": tuple((path, True, 1, "a" * 64) for path in EXACT_EIGHT),
    }
    content_snapshot_drift = copy.deepcopy(content_snapshot_sample)
    content_snapshot_drift["file_identities"] = ((EXACT_EIGHT[0], True, 1, "b" * 64), *content_snapshot_drift["file_identities"][1:])
    pre_json_status = [
        ("??" if EXPECTED_STATUS[path] == "A" else " M", path)
        for path in PRE_JSON_SIX
    ]
    collect_snapshot_sample = {
        "boundary": expected_boundary_snapshot(EXPECTED_PARENT),
        "status": tuple(sorted(pre_json_status)),
        "file_identities": tuple((path, True, 1, "a" * 64) for path in PRE_JSON_SIX),
    }
    collect_snapshot_drift = copy.deepcopy(collect_snapshot_sample)
    collect_snapshot_drift["status"] = (*collect_snapshot_drift["status"], ("??", "unexpected/collect-path"))
    callbacks: dict[str, Any] = {
        "N92-CONTROL-STALE": lambda: validate_human_control_texts(stale),
        "N92-CONTROL-DUPLICATE": lambda: validate_human_control_texts(duplicate),
        "N92-CONTROL-HISTORY": lambda: validate_human_control_texts(marker_history_only),
        "N92-CONTROL-NEXT": lambda: validate_human_control_texts(stale_next),
        "N92-CONTROL-ROW": lambda: validate_human_control_texts(correction_only),
        "N92-SOURCE-IMPORT-ALIAS": lambda: validate_source_texts(validator_source.replace("import subprocess\n", "import subprocess as process\n", 1), builder_source),
        "N92-SOURCE-PROCESS": lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_process():\n    subprocess.Popen(['git', 'status'])\n"), builder_source),
        "N92-SOURCE-PROCESS-ALIAS": lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_alias():\n    process = subprocess.run\n    process(['git', 'status'])\n"), builder_source),
        "N92-SOURCE-RUN-ALIAS": lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_worker():\n    worker = run\n"), builder_source),
        "N92-SOURCE-ANN-ALIAS": lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_annotated_worker():\n    worker: Any = run\n"), builder_source),
        "N92-SOURCE-NAMED-ALIAS": lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_named_worker():\n    if (worker := run):\n        pass\n"), builder_source),
        "N92-SOURCE-LOADER-ALIAS": lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_loader():\n    loader = __import__\n"), builder_source),
        "N92-SOURCE-WRITER-ALIAS": lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_writer_alias():\n    writer = Path('unexpected').write_text\n"), builder_source),
        "N92-SOURCE-NESTED-IMPORT": lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_nested_import():\n    import shutil\n"), builder_source),
        "N92-SOURCE-WRITER": lambda: validate_source_texts(inject_before_main(validator_source, "\n\ndef injected_writer():\n    Path('unexpected').write_text('x')\n"), builder_source),
        "N92-SOURCE-PATH-REPLACE": lambda: validate_source_texts(path_replace_source, builder_source),
        "N92-SOURCE-DYNAMIC-CALL": lambda: validate_source_texts(container_run_source, builder_source),
        "N92-SOURCE-IDENTITY-PATH-ALIAS": lambda: validate_reviewed_source_identity(path_alias_source.encode("utf-8"), builder_raw, control_texts[RESULT]),
        "N92-SOURCE-IDENTITY-CALLABLE-TRANSPORT": lambda: validate_reviewed_source_identity(callable_transport_source.encode("utf-8"), builder_raw, control_texts[RESULT]),
        "N92-SOURCE-IDENTITY-BUILDER-UNREACHABLE": lambda: validate_reviewed_source_identity(validator_raw, builder_unreachable_source.encode("utf-8"), control_texts[RESULT]),
        "N92-BUILDER-CALL": lambda: validate_source_texts(validator_source, builder_source.replace("inventory, attestation = contract.collect_payloads()", "inventory, attestation = contract.deterministic_pair()", 1)),
        "N92-BUILDER-DEAD-INDIRECT": lambda: validate_source_texts(validator_source, builder_dead_indirect_source),
        "N92-GIT-DANGEROUS": lambda: validate_process_argv(["git", "reset", "--hard"]),
        "N92-GIT-REF": lambda: validate_git_argv(["rev-parse", "--verify", "HEAD"]),
        "N92-GIT-LIVE": lambda: validate_git_argv(["ls-remote", "--exit-code", "origin", ACTIVE_LIVE_REF + "^{}"]),
        "N92-GIT-STAGED": lambda: validate_git_argv(["diff", "--cached", "--raw", "-z", EXPECTED_PARENT, "--"]),
        "N92-GIT-ABBREV": lambda: validate_git_argv(["diff-tree", "--no-commit-id", "--raw", "-r", "--abbrev=39", "--no-renames", "-z", BASE, CODEX_TIP, "--"]),
        "N92-STAGED-BLOB": lambda: validate_blob_bindings(binding_record, binding_index, ("x",), "E_SELFTEST_BLOB_BINDING"),
        "N92-SNAPSHOT-DIRTY": lambda: require_snapshot_equal({"head":"a","status":()}, {"head":"a","status":(("M ",VALIDATOR),)}, "E_SELFTEST_SNAPSHOT_DRIFT"),
        "N92-POST-JSON-EXTRA-PATH": lambda: validate_exact_output_status(post_json_extra_path),
        "N92-POST-JSON-STAGED-DRIFT": lambda: validate_exact_output_status(post_json_staged_drift),
        "N92-CONTENT-SNAPSHOT-DRIFT": lambda: require_snapshot_equal(content_snapshot_sample, content_snapshot_drift, "E_CONTENT_SNAPSHOT_DRIFT"),
        "N92-COLLECT-SNAPSHOT-DRIFT": lambda: require_snapshot_equal(collect_snapshot_sample, collect_snapshot_drift, "E_COLLECT_SNAPSHOT_DRIFT"),
        "N92-JSON-DUPLICATE": lambda: strict_load(b'{"a":1,"a":2}\n'),
        "N92-JSON-NONFINITE": lambda: strict_load(b'{"a":NaN}\n'),
        "N92-JSON-DEEP": lambda: strict_load(deep_json),
        "N92-JSON-CANONICAL": lambda: strict_load(raw.replace(b"\n", b"\r\n")),
        "N92-DIFF-STATUS": lambda: parse_raw_diff(b":000000 100644 " + b"0"*40 + b" " + b"1"*40 + b" R100\0a\0"),
        "N92-BOUNDARY-UPSTREAM": lambda: validate_boundary_snapshot(upstream_snapshot, EXPECTED_PARENT),
        "N92-BOUNDARY-LIVE": lambda: validate_boundary_snapshot(live_snapshot, EXPECTED_PARENT),
    }
    payload_mutations: dict[str, Any] = {
        "N92-COMMIT-DROP": lambda a,b: a["commits"].pop(),
        "N92-COMMIT-REPLACE": lambda a,b: a["commits"][0].update(oid="f" * 40),
        "N92-PARENT-ORDER": lambda a,b: a["commits"][2].update(parents=list(reversed(a["commits"][2]["parents"]))),
        "N92-EDGE-COMBINED": lambda a,b: a.update(edge_count=1),
        "N92-NET-EDGE-CONFUSION": lambda a,b: a.update(net_path_count=135),
        "N92-MAIN-DRIFT-INFLATION": lambda a,b: a.update(edge_path_event_count=136),
        "N92-PATH-MUTATION": lambda a,b: a["edges"][0]["changes"][0].update(path="unexpected/path.py", old_path="unexpected/path.py", new_path="unexpected/path.py"),
        "N92-BLOB-MUTATION": lambda a,b: a["edges"][0]["changes"][0].update(new_blob="f" * 40),
        "N92-MODE-MUTATION": lambda a,b: a["edges"][0]["changes"][0].update(new_mode="100755"),
        "N92-STATUS-MUTATION": lambda a,b: a["edges"][0]["changes"][0].update(status="D"),
        "N92-EXTENT-MUTATION": lambda a,b: a["edges"][0]["changes"][0]["raw_extent"].update(byte_end=0),
        "N92-COVERAGE-TRUNCATED": lambda a,b: b["unique_blobs"][0]["coverage"].update(byte_end=b["unique_blobs"][0]["raw_bytes"] - 1),
        "N92-PDF-METADATA-ONLY": lambda a,b: b["pdf_evidence"]["independent_visual_review"].update(pages_inspected=[]),
        "N92-POINTER-BLOB": lambda a,b: a["claims"][0]["claimant_surfaces"][0].update(source_oid="f" * 40),
        "N92-POINTER-PATH": lambda a,b: a["claims"][0]["claimant_surfaces"][0].update(path="unexpected/path.py"),
        "N92-AUTHORITY-SELFREPORT": lambda a,b: a["claims"][0].update(scientific_truth_promoted=True),
        "N92-AUTHORITY-PROMOTION": lambda a,b: a.update(scientific_truth_promotions=1),
        "N92-WHOLE-COMMIT": lambda a,b: a.update(whole_commit_adoptions=1),
        "N92-UNDECLARED-PATH": lambda a,b: a["edges"][0]["changes"].append(copy.deepcopy(a["edges"][0]["changes"][0])),
        "N92-WRONG-SUBJECT": lambda a,b: a["commits"][0].update(subject="wrong subject"),
        "N92-WRONG-PARENT": lambda a,b: a["commits"][0].update(parents=[BASE]),
        "N92-MEDIA-COUNT": lambda a,b: b.update(text_blob_count=80),
        "N92-GAP": lambda a,b: b.update(coverage_gaps=["gap"]),
    }
    callbacks.update({
        control_id: restoring_payload_negative(inventory, attestation, mutation)
        for control_id, mutation in payload_mutations.items()
    })
    named_count, named_digest = run_named_negative_controls(callbacks, inventory, attestation)
    tests += named_count
    print(f"PASS_P068_STEP92_SELF_TESTS {tests} named_negative_count={named_count} named_negative_digest={named_digest}")
    return tests


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--collect", action="store_true")
    modes.add_argument("--content-only", action="store_true")
    modes.add_argument("--verify-staged", action="store_true")
    modes.add_argument("--verify-persistence", action="store_true")
    parser.add_argument("--expected-commit")
    args = parser.parse_args(argv)
    if args.verify_persistence != (args.expected_commit is not None):
        parser.error("--expected-commit is required only with --verify-persistence")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_source_guard()
        tests = run_self_tests()
        if args.collect:
            inventory, attestation = collect_payloads()
            print(f"{CONTENT_TERMINAL} collect=JSON_LAST deterministic=2/2 inventory_bytes={len(inventory)} inventory_sha256={sha256(inventory)} attestation_bytes={len(attestation)} attestation_sha256={sha256(attestation)} self_tests={tests}")
        elif args.content_only:
            validate_content()
            print(f"{CONTENT_TERMINAL} deterministic=2/2 self_tests={tests}")
        elif args.verify_staged:
            validate_staged()
            print(f"{CONTENT_TERMINAL} staged=exact-eight self_tests={tests}")
        else:
            validate_persistence(args.expected_commit)
            print(f"{PERSISTENCE_TERMINAL} commit={args.expected_commit} self_tests={tests}")
        return 0
    except ValidationError as exc:
        print(f"FAIL_P068_STEP92 {exc.code} {exc.detail}".rstrip(), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
