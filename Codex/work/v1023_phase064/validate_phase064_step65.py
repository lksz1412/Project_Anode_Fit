from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import pathlib
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Callable

import build_phase064_step65_literature_authority as builder
from PIL import Image


ROOT = pathlib.Path(__file__).resolve().parents[3]
EXPECTED_PARENT = "fd8e192f031bb302933d925ceb9ba599a7975837"
EXPECTED_SUBJECT = "audit(phase064): bound v1023 literature authority"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
GATE = "PASS_P064_STEP65_LITERATURE_BOUNDED_GNF"
PERSISTENCE = "PASS_P064_STEP65_PERSISTENCE"

BUILDER_PATH = "Codex/work/v1023_phase064/build_phase064_step65_literature_authority.py"
VALIDATOR_PATH = "Codex/work/v1023_phase064/validate_phase064_step65.py"
MATRIX_PATH = "Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json"
ATTESTATION_PATH = "Codex/results/PHASE_064_V1023_LITERATURE_READ_ATTESTATION.json"
RESULT_PATH = "Codex/results/PHASE_064_STEP_065_LITERATURE_AUTHORITY_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
FINAL_PATHS = [
    BUILDER_PATH,
    VALIDATOR_PATH,
    MATRIX_PATH,
    ATTESTATION_PATH,
    RESULT_PATH,
    PARENT_LEDGER_PATH,
    ACTIVE_LEDGER_PATH,
    HANDOVER_PATH,
]
FINAL_SET = set(FINAL_PATHS)
EXPECTED_DOCUMENT_LF_SHA256 = {
    RESULT_PATH: "eb9abd8b809d8b266689fead41ef207e3016494c721de03dcd9b387be9cc1534",
    PARENT_LEDGER_PATH: "8be83ceae129d716155a482be033359c687376545b62874047f8614f23d0b3a0",
    ACTIVE_LEDGER_PATH: "47ccd9dc04336917935a28fb761c2f0e3b159e967efbc5bb72ff7450ba1e99a1",
    HANDOVER_PATH: "f93d4c9318a0be4b8d5dc65dd6cd9413a15cfccf0642099ca0859e6315a7f142",
}


class ValidationError(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationError(f"{code}: {detail}" if detail else code)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def reject_constant(value: str) -> Any:
    raise ValidationError(f"E_NONFINITE_JSON: {value}")


def finite_float(value: str) -> float:
    result = float(value)
    require(math.isfinite(result), "E_NONFINITE_JSON", value)
    return result


def bounded_int(value: str) -> int:
    require(len(value.lstrip("-")) <= 78, "E_INTEGER_RANGE", value[:80])
    result = int(value)
    require(abs(result) <= 2**256 - 1, "E_INTEGER_RANGE", value[:80])
    return result


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_DUPLICATE_JSON", key)
        result[key] = value
    return result


def strict_load_bytes(raw: bytes, source: str) -> tuple[Any, dict[str, int]]:
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=unique_pairs, parse_constant=reject_constant,
            parse_float=finite_float, parse_int=bounded_int,
        )
    except (UnicodeError, json.JSONDecodeError, OverflowError) as error:
        raise ValidationError(f"E_STRICT_JSON: {source}") from error
    counts = {"containers": 0, "scalars": 0, "keys": 0, "max_depth": 0}

    def walk(node: Any, depth: int) -> None:
        counts["max_depth"] = max(counts["max_depth"], depth)
        if type(node) is dict:
            counts["containers"] += 1
            counts["keys"] += len(node)
            for child in node.values():
                walk(child, depth + 1)
        elif type(node) is list:
            counts["containers"] += 1
            for child in node:
                walk(child, depth + 1)
        else:
            counts["scalars"] += 1
            if type(node) is float:
                require(math.isfinite(node), "E_NONFINITE_JSON", source)

    walk(value, 0)
    counts["value_nodes"] = counts["containers"] + counts["scalars"]
    counts["all_nodes"] = counts["value_nodes"] + counts["keys"]
    return value, counts


def strict_load(path: pathlib.Path) -> tuple[dict[str, Any], dict[str, int], bytes]:
    raw = path.read_bytes()
    value, traversal = strict_load_bytes(raw, path.as_posix())
    require(type(value) is dict, "E_JSON_ROOT", path.as_posix())
    return value, traversal, raw


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    process = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=300, check=False)
    if check and process.returncode != 0:
        raise ValidationError(f"E_SUBPROCESS: {args!r}: {process.stderr.decode('utf-8', errors='replace')[-1000:]}")
    return process


def git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run(["git", *args], check=check)


def git_text(args: list[str]) -> str:
    return git(args).stdout.decode("utf-8").strip()


def live_tip(branch: str) -> str:
    lines = git_text(["ls-remote", "origin", f"refs/heads/{branch}"]).splitlines()
    require(len(lines) == 1, "E_LIVE_REF", branch)
    return lines[0].split("\t", 1)[0]


def semantic_sha(value: dict[str, Any]) -> str:
    return sha256(canonical({key: item for key, item in value.items() if key != "semantic_sha256"}))


def rebind(value: dict[str, Any]) -> None:
    value["semantic_sha256"] = semantic_sha(value)


def exact_keys(value: Any, expected: set[str], errors: set[str], code: str) -> None:
    if type(value) is not dict or set(value) != expected:
        errors.add(code)


def artifact_errors(matrix: dict[str, Any], attestation: dict[str, Any], human: dict[str, Any]) -> set[str]:
    errors: set[str] = set()

    def add(condition: bool, code: str) -> None:
        if condition:
            errors.add(code)

    expected_matrix = builder.build_matrix(copy.deepcopy(human))
    expected_attestation = builder.build_attestation(copy.deepcopy(human), expected_matrix)
    add(matrix != expected_matrix, "E_MATRIX_REBUILD_BINDING")
    add(attestation != expected_attestation, "E_ATTESTATION_REBUILD_BINDING")

    exact_keys(matrix, {
        "schema_version", "artifact_kind", "phase", "step", "gate", "status", "authority_ceiling",
        "sources", "equation_chain", "applicability", "bibliography_boundaries", "conflicts",
        "open_items", "builder_identity", "semantic_sha256",
    }, errors, "E_MATRIX_SCHEMA")
    add(matrix.get("schema_version") != "1.0.0" or matrix.get("artifact_kind") != "V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX", "E_MATRIX_IDENTITY")
    add(matrix.get("phase") != 64 or matrix.get("step") != 65 or matrix.get("gate") != GATE, "E_MATRIX_GATE")
    add(matrix.get("status") != "PASS_PENDING_PERSISTENCE_WITH_GROUND_NOT_FOUND", "E_MATRIX_STATUS")
    add(matrix.get("authority_ceiling") != builder.AUTHORITY_CEILING, "E_MATRIX_CEILING")
    add(matrix.get("semantic_sha256") != semantic_sha(matrix), "E_MATRIX_SEMANTIC_SHA")

    sources = matrix.get("sources")
    add(type(sources) is not list or len(sources) != 3, "E_SOURCE_COUNT")
    if type(sources) is list and all(type(row) is dict for row in sources):
        by_id = {row.get("source_id"): row for row in sources}
        add(set(by_id) != {"JCP147", "REF6", "REF7"}, "E_SOURCE_IDS")
        if set(by_id) == {"JCP147", "REF6", "REF7"}:
            source_schema_ok = True
            for source_id, expected in builder.EXPECTED_SOURCE_CONTRACTS.items():
                row = by_id[source_id]
                authority_row = row.get("authority")
                identity_row = row.get("bibliographic_identity")
                if type(authority_row) is not dict or type(identity_row) is not dict:
                    errors.add("E_SOURCE_NESTED_SCHEMA")
                    source_schema_ok = False
                    continue
                projected = {
                    **identity_row,
                    "original_full_text_status": authority_row.get("original_full_text_status"),
                    "authority_tier": authority_row.get("tier"),
                    "raw_sha256": authority_row.get("raw_sha256"),
                    "bytes": authority_row.get("bytes"),
                    "pages": authority_row.get("pages"),
                    "pages_read": authority_row.get("pages_read"),
                }
                add(projected != expected, "E_SOURCE_IDENTITY")
                access_expected = builder.EXPECTED_ACCESS_CONTRACTS[source_id]
                access_observed = {
                    "access_url": authority_row.get("access_url"),
                    "license_status": authority_row.get("license_status"),
                }
                add(access_observed != access_expected, "E_SOURCE_ACCESS_CONTRACT")
            if source_schema_ok:
                jcp = by_id["JCP147"]["authority"]
                ref6 = by_id["REF6"]["authority"]
                ref7 = by_id["REF7"]["authority"]
                add(jcp.get("original_full_text_status") != "FULL_TEXT_READ" or jcp.get("pages_read") != 10, "E_JCP_FULL_READ")
                add(jcp.get("raw_sha256") != "47c7c415093bf5e3ee78215d6efa9141e4cd574e74e206cd9e3e863c5da85bd9", "E_JCP_RAW_SHA")
                add(ref6.get("original_full_text_status") != "FULL_TEXT_READ" or ref6.get("pages_read") != 4, "E_REF6_FULL_READ")
                add(ref6.get("raw_sha256") != "c0f2dbefa26731581235da28477f19f07f81f1e897523f6144e272f6b0959460", "E_REF6_RAW_SHA")
                add(ref7.get("original_full_text_status") != "GROUND_NOT_FOUND" or ref7.get("pages_read") != 0, "E_REF7_GNF")
                add(any(ref7.get(key) is not None for key in ("raw_sha256", "bytes", "pages")), "E_REF7_FALSE_FULLTEXT")
                add(by_id["REF7"].get("allowed_use") != "BIBLIOGRAPHIC_METADATA_ONLY", "E_REF7_SCOPE")
                add(by_id["REF7"]["bibliographic_identity"].get("doi") != "10.1063/1.4802584", "E_REF7_DOI")

    equations = matrix.get("equation_chain")
    add(equations != human.get("equations"), "E_EQUATION_HUMAN_BINDING")
    add(type(equations) is not list or [row.get("equation") for row in equations if type(row) is dict] != [str(i) for i in range(32, 40)], "E_EQUATION_SEQUENCE")
    expected_operations = {
        "32": "EXACT_WITHIN_EQ19_EQ20_APPROXIMATED_SYSTEM", "33": "FORMALLY_EXACT_REARRANGEMENT_WITHIN_EQ32",
        "34": "REFERENCE_RATIO_APPROXIMATION", "35": "CONTRACTED_REACTIVITY_MATCH",
        "36": "DERIVED_CONTACT_REACTIVITY", "37": "REFERENCE_RATIO_EVALUATION",
        "38": "CONTRACTED_REACTIVITY_DEFINITION", "39": "APPROXIMATE_CLOSED_EXPRESSION",
    }
    if type(equations) is list:
        for row in equations:
            if type(row) is not dict:
                errors.add("E_EQUATION_SCHEMA")
                continue
            number = row.get("equation")
            add(expected_operations.get(number) != row.get("operation"), "E_EQUATION_OPERATION")
            add(row.get("pdf_page") != 5 or row.get("printed_page") != "144111-4", "E_EQUATION_PAGE")
            projection = row.get("semantic_projection")
            add(type(projection) is not str or sha256(projection.encode("utf-8")) != row.get("semantic_projection_sha256"), "E_EQUATION_PROJECTION_SHA")
            interval = row.get("context_interval")
            if type(interval) is list and len(interval) == 2:
                add(builder.raw_slice_sha(ROOT / builder.JCP_EXTRACT_PATH, interval[0], interval[1]) != row.get("context_locator_sha256"), "E_EQUATION_CONTEXT_LOCATOR")
            else:
                errors.add("E_EQUATION_INTERVAL")

    applicability = matrix.get("applicability")
    add(type(applicability) is not dict, "E_APPLICABILITY_SCHEMA")
    if type(applicability) is dict:
        add(applicability.get("upstream_approximations") != human.get("jcp147_upstream_approximations"), "E_UPSTREAM_HUMAN_BINDING")
        conditions = applicability.get("conditions")
        add(conditions != human.get("jcp147_conditions"), "E_CONDITION_HUMAN_BINDING")
        add(type(conditions) is not list or len(conditions) != 3, "E_CONDITION_COUNT")
        if type(conditions) is list:
            add([row.get("id") for row in conditions if type(row) is dict] != ["JCP147-COND-1", "JCP147-COND-2", "JCP147-COND-3"], "E_CONDITION_IDS")
        add(applicability.get("operation_boundary") != "EQ32_CONDITIONAL_ON_EQ19_EQ20_EQ33_EXACT_WITHIN_EQ32_EQ34_AND_EQ39_APPROXIMATE", "E_OPERATION_BOUNDARY")
        add(applicability.get("domain_transfer_status") != "NOT_YET_AUTHORIZED_PENDING_STEP66_INDEPENDENT_REDERIVATION", "E_DOMAIN_TRANSFER")
        degradation = applicability.get("degradation")
        add(degradation != human.get("jcp147_degradation"), "E_DEGRADATION_HUMAN_BINDING")
        add(type(degradation) is not dict or degradation.get("id") != "JCP147-DEGRADE-1", "E_DEGRADATION")

    bibliography = matrix.get("bibliography_boundaries")
    add(type(bibliography) is not dict, "E_BIB_BOUNDARY")
    if type(bibliography) is dict:
        add(bibliography.get("stale_ledger_is_not_adopted_inventory") is not True, "E_BIB_LEDGER_CONFLATION")
        add(bibliography.get("ref7_annotation_original_full_text_verified") is not False, "E_REF7_ANNOTATION_FALSE_PASS")

    conflicts = matrix.get("conflicts")
    add(conflicts != human.get("conflicts"), "E_CONFLICT_HUMAN_BINDING")
    add(type(conflicts) is not list or len(conflicts) != 1, "E_CONFLICT_COUNT")
    if type(conflicts) is list and len(conflicts) == 1 and type(conflicts[0]) is dict:
        add(conflicts[0].get("candidate_ref7_doi") != "10.1063/1.4802005", "E_WRONG_DOI_CONTROL")
        add(conflicts[0].get("disposition") != "REJECT_AS_REF7_DOI" or conflicts[0].get("actual_article_number") != "164906", "E_WRONG_DOI_DISPOSITION")

    open_items = matrix.get("open_items")
    add(type(open_items) is not list or len(open_items) != 1, "E_OPEN_COUNT")
    if type(open_items) is list and len(open_items) == 1 and type(open_items[0]) is dict:
        add(not open_items[0].get("owner"), "E_OPEN_OWNER")
        add(not open_items[0].get("acceptance_criterion"), "E_OPEN_CRITERION")
        add(open_items[0].get("status") != "OPEN_GROUND_NOT_FOUND", "E_OPEN_STATUS")

    exact_keys(attestation, {
        "schema_version", "artifact_kind", "phase", "step", "gate", "status", "evidence_id",
        "evidence_date", "access_date", "human_evidence_semantic_sha256", "human_evidence",
        "full_reads", "ground_not_found", "strict_traversal", "source_mutation_count",
        "matrix_semantic_sha256", "authority", "semantic_sha256",
    }, errors, "E_ATTESTATION_SCHEMA")
    add(attestation.get("artifact_kind") != "V1023_LITERATURE_READ_ATTESTATION", "E_ATTESTATION_IDENTITY")
    add(attestation.get("phase") != 64 or attestation.get("step") != 65 or attestation.get("gate") != GATE, "E_ATTESTATION_GATE")
    add(attestation.get("human_evidence") != human, "E_HUMAN_EVIDENCE_BINDING")
    add(attestation.get("human_evidence_semantic_sha256") != sha256(canonical(human)), "E_HUMAN_EVIDENCE_SHA")
    add(attestation.get("matrix_semantic_sha256") != matrix.get("semantic_sha256"), "E_MATRIX_ATTESTATION_BINDING")
    add(attestation.get("source_mutation_count") != 0, "E_SOURCE_MUTATION_COUNT")
    add(attestation.get("strict_traversal") != {"source_records": 3, "equation_records": 8, "condition_records": 3, "conflict_records": 1, "upstream_approximation_records": 1}, "E_TRAVERSAL_COUNTS")
    full_reads = attestation.get("full_reads")
    add(type(full_reads) is not list or [row.get("source_id") for row in full_reads if type(row) is dict] != ["JCP147", "REF6"], "E_FULL_READ_IDS")
    gnf = attestation.get("ground_not_found")
    add(type(gnf) is not list or [row.get("source_id") for row in gnf if type(row) is dict] != ["REF7"], "E_GNF_IDS")
    authority = attestation.get("authority")
    add(type(authority) is not dict, "E_AUTHORITY_SCHEMA")
    if type(authority) is dict:
        add(authority.get("ceiling") != builder.AUTHORITY_CEILING, "E_ATTESTATION_CEILING")
        add(authority.get("ref7_method_content_verified") is not False, "E_REF7_METHOD_FALSE_PASS")
        add(authority.get("wrong_ref7_doi_rejected") is not True, "E_WRONG_DOI_NOT_REJECTED")
        add(authority.get("p064_unconditional_pass_allowed") is not False, "E_UNCONDITIONAL_FALSE_PASS")
    add(attestation.get("semantic_sha256") != semantic_sha(attestation), "E_ATTESTATION_SEMANTIC_SHA")
    return errors


def document_errors(result: str, parent_ledger: str, active_ledger: str, handover: str) -> set[str]:
    errors: set[str] = set()

    def add(condition: bool, code: str) -> None:
        if condition:
            errors.add(code)

    for path, text in zip(
        (RESULT_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH),
        (result, parent_ledger, active_ledger, handover),
    ):
        add(sha256(text.encode("utf-8")) != EXPECTED_DOCUMENT_LF_SHA256[path], "E_DOCUMENT_EXACT_BYTES")

    result_tokens = [
        GATE, "PASS_PENDING_PERSISTENCE_WITH_GROUND_NOT_FOUND", "CONDITIONAL_P064",
        "10.1063/1.5000882", "10.1063/1.3565476", "10.1063/1.4802584",
        "10.1063/1.4802005", "REJECT_AS_REF7_DOI", "GROUND_NOT_FOUND",
        "Eq. 33은 그 Eq. 32 내부에서 exact rearrangement", "Eq. 39는 근사식", "OPEN_GROUND_NOT_FOUND",
        EXPECTED_PARENT, EXPECTED_SUBJECT, builder.BEGIN, builder.END,
    ]
    for token in result_tokens:
        add(token not in result, "E_RESULT_TOKEN")
    add(result.count(builder.BEGIN) != 1 or result.count(builder.END) != 1, "E_RESULT_EVIDENCE_MARKERS")
    add("Ref. 7 original full-text equation-level method chain." not in result, "E_RESULT_OPEN_SCOPE")

    for text, code in ((parent_ledger, "E_PARENT_LEDGER"), (active_ledger, "E_ACTIVE_LEDGER"), (handover, "E_HANDOVER")):
        for token in ("fd8e192f031bb302933d925ceb9ba599a7975837", GATE, EXPECTED_SUBJECT, "PASS_P064_STEP65_PERSISTENCE", "CONDITIONAL_P064"):
            add(token not in text, code)
    add("Step 64 precommit" in parent_ledger or "Step 64 precommit" in active_ledger, "E_STALE_STEP64_PRECOMMIT")
    add("Current checkpoint: Step 65" not in handover, "E_HANDOVER_CURRENT")
    add("Step 65 eight declared paths" not in active_ledger or "Step 65 eight declared paths" not in handover, "E_NEXT_EXACT_STEP")
    return errors


def strict_json_probes() -> int:
    probes = [
        (b'{"a":1,"a":2}\n', "E_DUPLICATE_JSON"),
        (b'{"a":NaN}\n', "E_NONFINITE_JSON"),
        (b'{"a":1', "E_STRICT_JSON"),
        (b'{"a":1e9999}\n', "E_NONFINITE_JSON"),
        (b'{"a":999999999999999999999999999999999999999999999999999999999999999999999999999999}\n', "E_INTEGER_RANGE"),
    ]
    passed = 0
    for raw, code in probes:
        try:
            strict_load_bytes(raw, "probe")
        except ValidationError as error:
            require(code in str(error), "E_STRICT_PROBE_WRONG_ERROR", str(error))
            passed += 1
        else:
            raise ValidationError(f"E_STRICT_PROBE_ACCEPTED: {code}")
    return passed


def validate_equation_crops(human: dict[str, Any]) -> int:
    executable = shutil.which("pdftoppm")
    require(executable is not None, "E_PDFTOPPM_MISSING")
    version = run([executable, "-v"], check=False)
    version_text = (version.stdout + version.stderr).decode("utf-8", errors="replace")
    require(version.returncode == 0 and "pdftoppm version 26.05.0" in version_text, "E_PDFTOPPM_VERSION", version_text[:160])
    with tempfile.TemporaryDirectory(prefix="p064-step65-equation-crops-") as directory:
        prefix = pathlib.Path(directory) / "page5"
        process = run([
            executable, "-f", "5", "-l", "5", "-r", "300", "-png", "-singlefile",
            str(ROOT / builder.JCP_PDF_PATH), str(prefix),
        ], check=False)
        require(process.returncode == 0, "E_EQUATION_RENDER", process.stderr.decode("utf-8", errors="replace")[-600:])
        image_path = prefix.with_suffix(".png")
        require(image_path.is_file(), "E_EQUATION_RENDER_OUTPUT")
        with Image.open(image_path) as source:
            page = source.convert("RGB")
            require(page.size == (2475, 3300), "E_EQUATION_PAGE_PIXELS", repr(page.size))
            passed = 0
            for row in human["equations"]:
                pixel_box = row["pixel_box_300dpi"]
                crop = page.crop(tuple(pixel_box))
                require(crop.mode == row["crop_mode"], "E_EQUATION_CROP_MODE", row["equation"])
                require(crop.size == (row["crop_width"], row["crop_height"]), "E_EQUATION_CROP_SIZE", row["equation"])
                require(sha256(crop.tobytes()) == row["crop_raw_pixel_sha256"], "E_EQUATION_CROP_SHA", row["equation"])
                passed += 1
    return passed


def negative_probes(matrix: dict[str, Any], attestation: dict[str, Any], human: dict[str, Any]) -> int:
    probes: list[tuple[str, str, str, Callable[[dict[str, Any], dict[str, Any]], None]]] = []

    def matrix_probe(name: str, code: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        def apply(m: dict[str, Any], a: dict[str, Any]) -> None:
            mutate(m)
            rebind(m)
            a["matrix_semantic_sha256"] = m["semantic_sha256"]
            rebind(a)
        probes.append((name, code, "matrix", apply))

    def att_probe(name: str, code: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        def apply(m: dict[str, Any], a: dict[str, Any]) -> None:
            mutate(a)
            rebind(a)
        probes.append((name, code, "attestation", apply))

    matrix_probe("false_ref7_present", "E_REF7_GNF", lambda m: m["sources"][2]["authority"].__setitem__("original_full_text_status", "FULL_TEXT_READ"))
    matrix_probe("ref7_raw_sha_fabricated", "E_REF7_FALSE_FULLTEXT", lambda m: m["sources"][2]["authority"].__setitem__("raw_sha256", "0" * 64))
    matrix_probe("wrong_ref7_doi_adopted", "E_REF7_DOI", lambda m: m["sources"][2]["bibliographic_identity"].__setitem__("doi", "10.1063/1.4802005"))
    matrix_probe("wrong_doi_not_rejected", "E_WRONG_DOI_DISPOSITION", lambda m: m["conflicts"][0].__setitem__("disposition", "ACCEPT_AS_REF7_DOI"))
    matrix_probe("omit_eq32", "E_EQUATION_SEQUENCE", lambda m: m["equation_chain"].pop(0))
    matrix_probe("omit_eq33", "E_EQUATION_SEQUENCE", lambda m: m["equation_chain"].pop(1))
    matrix_probe("omit_eq34", "E_EQUATION_SEQUENCE", lambda m: m["equation_chain"].pop(2))
    matrix_probe("omit_eq37", "E_EQUATION_SEQUENCE", lambda m: m["equation_chain"].pop(5))
    matrix_probe("omit_eq39", "E_EQUATION_SEQUENCE", lambda m: m["equation_chain"].pop(7))
    matrix_probe("eq33_approximate", "E_EQUATION_OPERATION", lambda m: m["equation_chain"][1].__setitem__("operation", "REFERENCE_RATIO_APPROXIMATION"))
    matrix_probe("eq39_exact", "E_EQUATION_OPERATION", lambda m: m["equation_chain"][7].__setitem__("operation", "FORMALLY_EXACT_REARRANGEMENT"))
    matrix_probe("equation_projection_mutated", "E_EQUATION_PROJECTION_SHA", lambda m: m["equation_chain"][0].__setitem__("semantic_projection", "tampered"))
    matrix_probe("equation_context_mutated", "E_EQUATION_CONTEXT_LOCATOR", lambda m: m["equation_chain"][2].__setitem__("context_locator_sha256", "0" * 64))
    matrix_probe("equation_interval_self_auth", "E_EQUATION_HUMAN_BINDING", lambda m: m["equation_chain"][2].update({"context_interval": [1, 1], "context_locator_sha256": builder.raw_slice_sha(ROOT / builder.JCP_EXTRACT_PATH, 1, 1)}))
    matrix_probe("equation_crop_sha_mutated", "E_EQUATION_HUMAN_BINDING", lambda m: m["equation_chain"][0].__setitem__("crop_raw_pixel_sha256", "0" * 64))
    matrix_probe("equation_nested_extra", "E_MATRIX_REBUILD_BINDING", lambda m: m["equation_chain"][0].__setitem__("fabricated_extra", True))
    matrix_probe("condition_omitted", "E_CONDITION_COUNT", lambda m: m["applicability"]["conditions"].pop())
    matrix_probe("condition_identity_mutated", "E_CONDITION_IDS", lambda m: m["applicability"]["conditions"][0].__setitem__("id", "tampered"))
    matrix_probe("degradation_omitted", "E_DEGRADATION", lambda m: m["applicability"].__setitem__("degradation", {}))
    matrix_probe("upstream_approximation_omitted", "E_UPSTREAM_HUMAN_BINDING", lambda m: m["applicability"].__setitem__("upstream_approximations", {}))
    matrix_probe("domain_transfer_premature", "E_DOMAIN_TRANSFER", lambda m: m["applicability"].__setitem__("domain_transfer_status", "AUTHORIZED"))
    matrix_probe("bibliography_ledger_conflated", "E_BIB_LEDGER_CONFLATION", lambda m: m["bibliography_boundaries"].__setitem__("stale_ledger_is_not_adopted_inventory", False))
    matrix_probe("ref7_annotation_false_pass", "E_REF7_ANNOTATION_FALSE_PASS", lambda m: m["bibliography_boundaries"].__setitem__("ref7_annotation_original_full_text_verified", True))
    matrix_probe("open_owner_missing", "E_OPEN_OWNER", lambda m: m["open_items"][0].__setitem__("owner", ""))
    matrix_probe("open_criterion_missing", "E_OPEN_CRITERION", lambda m: m["open_items"][0].__setitem__("acceptance_criterion", ""))
    matrix_probe("open_target_scalar", "E_MATRIX_REBUILD_BINDING", lambda m: m["open_items"][0].__setitem__("target", 0))
    matrix_probe("unconditional_ceiling", "E_MATRIX_CEILING", lambda m: m.__setitem__("authority_ceiling", "PASS_P064"))
    matrix_probe("ref6_fullread_false", "E_REF6_FULL_READ", lambda m: m["sources"][1]["authority"].__setitem__("pages_read", 0))
    matrix_probe("ref6_hash_mutated", "E_REF6_RAW_SHA", lambda m: m["sources"][1]["authority"].__setitem__("raw_sha256", "0" * 64))
    matrix_probe("jcp_pages_mutated", "E_JCP_FULL_READ", lambda m: m["sources"][0]["authority"].__setitem__("pages_read", 9))
    matrix_probe("source_authority_scalar", "E_SOURCE_NESTED_SCHEMA", lambda m: m["sources"][0].__setitem__("authority", 0))
    matrix_probe("ref6_title_mutated", "E_SOURCE_IDENTITY", lambda m: m["sources"][1]["bibliographic_identity"].__setitem__("title", "fabricated"))
    matrix_probe("jcp_author_mutated", "E_SOURCE_IDENTITY", lambda m: m["sources"][0]["bibliographic_identity"]["authors"].__setitem__(0, "fabricated"))
    matrix_probe("ref6_access_route_mutated", "E_SOURCE_ACCESS_CONTRACT", lambda m: m["sources"][1]["authority"].__setitem__("access_url", "https://example.invalid/fabricated.pdf"))
    att_probe("human_evidence_mutated", "E_HUMAN_EVIDENCE_BINDING", lambda a: a["human_evidence"].__setitem__("evidence_id", "tampered"))
    att_probe("human_hash_mutated", "E_HUMAN_EVIDENCE_SHA", lambda a: a.__setitem__("human_evidence_semantic_sha256", "0" * 64))
    att_probe("gnf_omitted", "E_GNF_IDS", lambda a: a.__setitem__("ground_not_found", []))
    att_probe("full_read_hash_mutated", "E_ATTESTATION_REBUILD_BINDING", lambda a: a["full_reads"][0].__setitem__("raw_sha256", "0" * 64))
    att_probe("unconditional_pass_allowed", "E_UNCONDITIONAL_FALSE_PASS", lambda a: a["authority"].__setitem__("p064_unconditional_pass_allowed", True))
    att_probe("ref7_method_false_pass", "E_REF7_METHOD_FALSE_PASS", lambda a: a["authority"].__setitem__("ref7_method_content_verified", True))
    att_probe("source_mutation", "E_SOURCE_MUTATION_COUNT", lambda a: a.__setitem__("source_mutation_count", 1))

    passed = 0
    for name, expected, _kind, mutate in probes:
        candidate_matrix = copy.deepcopy(matrix)
        candidate_attestation = copy.deepcopy(attestation)
        mutate(candidate_matrix, candidate_attestation)
        errors = artifact_errors(candidate_matrix, candidate_attestation, human)
        require(expected in errors, "E_NEGATIVE_PROBE_ACCEPTED", f"{name}: {sorted(errors)}")
        passed += 1

    human_probes: list[tuple[str, str, Callable[[dict[str, Any]], None]]] = [
        ("human_equation_self_auth", "E_EQUATION_CONTRACT", lambda h: h["equations"][2].update({"context_interval": [1, 1], "context_locator_sha256": builder.raw_slice_sha(ROOT / builder.JCP_EXTRACT_PATH, 1, 1), "semantic_projection": "FABRICATED", "semantic_projection_sha256": sha256(b"FABRICATED")})),
        ("human_condition_claim", "E_CONDITIONS", lambda h: h["jcp147_conditions"][0].__setitem__("claim", "FABRICATED")),
        ("human_conflict_title", "E_CONFLICT_CONTRACT", lambda h: h["conflicts"][0].__setitem__("actual_title", "FABRICATED")),
        ("human_reader_scope", "E_READER_CONTRACT", lambda h: h["readers"][0].__setitem__("scope", "FABRICATED")),
        ("human_upstream_claim", "E_UPSTREAM_APPROXIMATION", lambda h: h["jcp147_upstream_approximations"].__setitem__("claim", "FABRICATED")),
        ("human_bibliography_provenance", "E_BIBLIOGRAPHY_SOURCE_CONTRACT", lambda h: h["bibliography_sources"]["adopted_bibliography"].update({"path": "FABRICATED", "blob_sha1": "0" * 40, "raw_sha256": "0" * 64, "line_interval": [1, 1]})),
        ("human_source_id_scalar", "E_SOURCE_ID_TYPE", lambda h: h["sources"][0].__setitem__("source_id", [])),
        ("human_bibliography_scalar", "E_BIBLIOGRAPHY_SOURCE_CONTRACT", lambda h: h.__setitem__("bibliography_sources", 0)),
    ]
    for name, expected, mutate in human_probes:
        candidate = copy.deepcopy(human)
        mutate(candidate)
        try:
            builder.validate_evidence(candidate)
        except builder.BuildError as error:
            require(expected in str(error), "E_HUMAN_PROBE_WRONG_ERROR", f"{name}: {error}")
            passed += 1
        else:
            raise ValidationError(f"E_HUMAN_PROBE_ACCEPTED: {name}")
    return passed


def document_negative_probes() -> int:
    docs = [(ROOT / path).read_text(encoding="utf-8") for path in (RESULT_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH)]
    candidates: list[tuple[str, list[str]]] = []
    token_soup = " ".join([
        GATE, "PASS_PENDING_PERSISTENCE_WITH_GROUND_NOT_FOUND", "CONDITIONAL_P064",
        "10.1063/1.5000882", "10.1063/1.3565476", "10.1063/1.4802584", "10.1063/1.4802005",
        "REJECT_AS_REF7_DOI", "GROUND_NOT_FOUND", "Eq. 33은 그 Eq. 32 내부에서 exact rearrangement",
        "Eq. 39는 근사식", "OPEN_GROUND_NOT_FOUND", EXPECTED_PARENT, EXPECTED_SUBJECT,
        builder.BEGIN, builder.END, "Ref. 7 original full-text equation-level method chain.",
        "PASS_P064_STEP65_PERSISTENCE", "Current checkpoint: Step 65", "Step 65 eight declared paths",
        "fd8e192f031bb302933d925ceb9ba599a7975837",
    ])
    candidates.append(("token_soup", [token_soup] * 4))
    for index, name in enumerate(("result", "parent_ledger", "active_ledger", "handover")):
        mutated = list(docs)
        mutated[index] = mutated[index] + "\nFABRICATED\n"
        candidates.append((name, mutated))
    passed = 0
    for name, candidate in candidates:
        errors = document_errors(*candidate)
        require("E_DOCUMENT_EXACT_BYTES" in errors, "E_DOCUMENT_PROBE_ACCEPTED", f"{name}: {sorted(errors)}")
        passed += 1
    return passed


def validate_artifacts() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, int]]:
    matrix, matrix_traversal, matrix_raw = strict_load(ROOT / MATRIX_PATH)
    attestation, attestation_traversal, attestation_raw = strict_load(ROOT / ATTESTATION_PATH)
    require(canonical(matrix) == matrix_raw, "E_MATRIX_CANONICAL_JSON")
    require(canonical(attestation) == attestation_raw, "E_ATTESTATION_CANONICAL_JSON")
    human = builder.load_human_evidence()
    builder.validate_evidence(human)
    builder.validate_local_sources(human)
    crop_count = validate_equation_crops(human)
    errors = artifact_errors(matrix, attestation, human)
    require(not errors, "E_ARTIFACTS", ",".join(sorted(errors)))
    docs = [(ROOT / path).read_text(encoding="utf-8") for path in (RESULT_PATH, PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH)]
    errors = document_errors(*docs)
    require(not errors, "E_DOCUMENTS", ",".join(sorted(errors)))
    traversal = {
        "matrix_all_nodes": matrix_traversal["all_nodes"],
        "attestation_all_nodes": attestation_traversal["all_nodes"],
        "equation_crops": crop_count,
    }
    return matrix, attestation, human, traversal


def validate_determinism() -> int:
    expected = {path: (ROOT / path).read_bytes() for path in (MATRIX_PATH, ATTESTATION_PATH)}
    for _ in range(2):
        human = builder.load_human_evidence()
        builder.validate_evidence(human)
        builder.validate_local_sources(human)
        matrix = builder.build_matrix(copy.deepcopy(human))
        attestation = builder.build_attestation(copy.deepcopy(human), matrix)
        observed = {MATRIX_PATH: canonical(matrix), ATTESTATION_PATH: canonical(attestation)}
        require(observed == expected, "E_BUILDER_NONDETERMINISTIC")
    return 2


def staged_paths() -> set[str]:
    return set(filter(None, git_text(["diff", "--cached", "--name-only", "--diff-filter=ACMR"]).splitlines()))


def commit_paths(commit: str) -> set[str]:
    return set(filter(None, git_text(["diff-tree", "--no-commit-id", "--name-only", "-r", commit]).splitlines()))


def validate_common_git() -> None:
    require(git_text(["branch", "--show-current"]) == ACTIVE_BRANCH, "E_ACTIVE_BRANCH")
    require(git_text(["rev-parse", PROTECTED_BRANCH]) == PROTECTED_TIP, "E_PROTECTED_LOCAL")
    require(git_text(["rev-parse", f"origin/{PROTECTED_BRANCH}"]) == PROTECTED_TIP, "E_PROTECTED_TRACKING")
    require(live_tip(PROTECTED_BRANCH) == PROTECTED_TIP, "E_PROTECTED_LIVE")
    require(git_text(["rev-parse", "origin/main"]) == MAIN_TIP, "E_MAIN_TRACKING")
    require(live_tip("main") == MAIN_TIP, "E_MAIN_LIVE")
    require(not git_text(["status", "--porcelain", "--", "Claude"]), "E_CLAUDE_MUTATION")


def validate_precommit_git() -> None:
    validate_common_git()
    require(git_text(["rev-parse", "HEAD"]) == EXPECTED_PARENT, "E_PRECOMMIT_PARENT")
    require(git_text(["rev-parse", "@{upstream}"]) == EXPECTED_PARENT, "E_PRECOMMIT_UPSTREAM")
    require(git_text(["rev-parse", "--symbolic-full-name", "@{upstream}"]) == f"refs/remotes/origin/{ACTIVE_BRANCH}", "E_PRECOMMIT_UPSTREAM_NAME")
    require(git_text(["rev-parse", f"origin/{ACTIVE_BRANCH}"]) == EXPECTED_PARENT, "E_PRECOMMIT_TRACKING")
    require(live_tip(ACTIVE_BRANCH) == EXPECTED_PARENT, "E_PRECOMMIT_LIVE")
    require(staged_paths() == FINAL_SET, "E_EXACT_EIGHT_STAGED", repr(sorted(staged_paths())))
    require(not git_text(["diff", "--name-only", "--", *FINAL_PATHS]), "E_FINAL_PATH_UNSTAGED")
    status_paths = set()
    for line in git_text(["status", "--porcelain"]).splitlines():
        if line:
            status_paths.add(line[3:].replace("\\", "/"))
    require(status_paths == FINAL_SET, "E_WORKTREE_SCOPE", repr(sorted(status_paths)))
    require(git(["diff", "--cached", "--check"], check=False).returncode == 0, "E_DIFF_CHECK")
    for path in FINAL_PATHS:
        require(git_text(["rev-parse", f":{path}"]) == git_text(["hash-object", f"--path={path}", path]), "E_INDEX_BYTES", path)


def validate_persistence_git(expected_commit: str) -> None:
    validate_common_git()
    head = git_text(["rev-parse", "HEAD"])
    require(head == expected_commit, "E_PERSISTENCE_EXPECTED_COMMIT")
    require(git_text(["rev-parse", "HEAD^"]) == EXPECTED_PARENT, "E_PERSISTENCE_PARENT")
    require(git_text(["show", "-s", "--format=%s", "HEAD"]) == EXPECTED_SUBJECT, "E_PERSISTENCE_SUBJECT")
    require(git_text(["rev-parse", "@{upstream}"]) == head, "E_PERSISTENCE_UPSTREAM")
    require(git_text(["rev-parse", "--symbolic-full-name", "@{upstream}"]) == f"refs/remotes/origin/{ACTIVE_BRANCH}", "E_PERSISTENCE_UPSTREAM_NAME")
    require(git_text(["rev-parse", f"origin/{ACTIVE_BRANCH}"]) == head, "E_PERSISTENCE_TRACKING")
    require(live_tip(ACTIVE_BRANCH) == head, "E_PERSISTENCE_LIVE")
    require(commit_paths(head) == FINAL_SET, "E_PERSISTENCE_EXACT_EIGHT")
    require(not git_text(["status", "--porcelain"]), "E_PERSISTENCE_DIRTY")
    for path in FINAL_PATHS:
        require(git_text(["rev-parse", f"HEAD:{path}"]) == git_text(["hash-object", f"--path={path}", path]), "E_PERSISTENCE_BYTES", path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("artifact", "precommit", "persistence"), default="precommit")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    matrix, attestation, human, traversal = validate_artifacts()
    strict_count = strict_json_probes()
    negative_count = negative_probes(matrix, attestation, human) + document_negative_probes()
    determinism_count = validate_determinism()
    if args.mode == "precommit":
        require(args.expected_commit is None, "E_UNEXPECTED_COMMIT_ARGUMENT")
        validate_precommit_git()
    elif args.mode == "persistence":
        require(type(args.expected_commit) is str and len(args.expected_commit) == 40, "E_EXPECTED_COMMIT_ARGUMENT")
        validate_persistence_git(args.expected_commit)
    else:
        require(args.expected_commit is None, "E_UNEXPECTED_COMMIT_ARGUMENT")
    print(f"PASS_P064_STEP65_NEGATIVE {negative_count}/{negative_count} strict_json={strict_count}/{strict_count}")
    print(f"PASS_P064_STEP65_TRAVERSAL matrix={traversal['matrix_all_nodes']} attestation={traversal['attestation_all_nodes']} equation_crops={traversal['equation_crops']}/8")
    print(f"PASS_P064_STEP65_DETERMINISM {determinism_count}/{determinism_count}")
    if args.mode == "persistence":
        print(PERSISTENCE)
    elif args.mode == "precommit":
        print(GATE)
    else:
        print("PASS_P064_STEP65_ARTIFACT_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
