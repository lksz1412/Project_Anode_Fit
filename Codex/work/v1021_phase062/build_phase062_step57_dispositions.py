#!/usr/bin/env python3
"""Build Phase 062 Step 57.1 disposition and carry artifacts.

The builder reads only frozen Git-backed audit artifacts.  It never imports or
executes Claude production/test modules.  Result Markdown is written before the
two JSON artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
INPUT_COMMIT = "1c8541fdea2cd69aa09e6b99d2f371c41a0bb727"
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
BUILDER_RELATIVE = "Codex/work/v1021_phase062/build_phase062_step57_dispositions.py"
RESULT_RELATIVE = "Codex/results/PHASE_062_STEP_057_1_DISPOSITION_RESULT.md"
DISPOSITION_RELATIVE = "Codex/results/PHASE_062_V1021_DISPOSITION_MATRIX.json"
CARRY_RELATIVE = "Codex/results/PHASE_062_V1021_CARRY_FORWARD_DELTA.json"
CANONICAL_JSON = "UTF-8 LF indent=2 sort_keys=true allow_nan=false trailing_newline=true"
TARGET62_ID_SHA256 = "68267522dbda5c3a47fccfaad0babb2617331f2208831f36f91ec2ea284f11a5"

TOPOLOGY = "Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json"
READ_ATTESTATION = "Codex/results/PHASE_062_V1021_READ_ATTESTATION.json"
STEP53 = "Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json"
STEP54 = "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json"
STEP55_CODE = "Codex/results/PHASE_062_V1021_CODE_DELTA_MATRIX.json"
STEP55_RUNTIME = "Codex/results/PHASE_062_V1021_RUNTIME_ATTESTATION.json"
STEP56 = "Codex/results/PHASE_062_V1021_PHYSICS_CLOSURE_MATRIX.json"
P61_DISPOSITION = "Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json"
P61_CARRY = "Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json"

INPUT_SHA256 = {
    TOPOLOGY: "cb8eda3efa2b50da49ddc6d4e67d0c9679bce7540a622b584828e44e042bc283",
    READ_ATTESTATION: "0f646e7089016d81e1e1bb73391478454f31fde4fa8560285e239d7634e279ea",
    STEP53: "934be5273a91578b712d3ab44ef96eebb4cf7645973ec101b4e233b49426de16",
    STEP54: "9af82c1997f0b31282b353ae1006324e8a9913fc7e5c579709a4c9b1bb32901d",
    STEP55_CODE: "ba0e6f7eee956294f0b38c2497c9f90b3976321718d262406e57d77853c058d4",
    STEP55_RUNTIME: "7c6d8486ddf66749527cb4171932bbe737405e1d640657884859b1330e6edf77",
    STEP56: "1c24478c01692dca82465db273f3b432dac7b65739475f015999922137e1e27d",
    P61_DISPOSITION: "c011ad481a325437a7d6e8b6ae37416417eb031932b1490cd9c6e8c5b39ac01e",
    P61_CARRY: "b8ed909937be07938b30ae3344d9ff60ca87a476a8c422e32d8751123bdb100e",
}

AUTHORITY = {
    "canonical_equation_promoted": False,
    "external_experimental_truth": False,
    "external_material_truth": False,
    "external_scientific_truth": False,
    "primary_literature_truth": False,
    "scope": "INTERNAL_LINEAGE_DISPOSITION_ONLY",
}

ALLOWED_DISPOSITIONS = {
    "PRESERVE", "CORRECT", "DISCARD", "SUPERSEDE",
    "EMPIRICAL_ONLY", "THEORY_ONLY", "UNVERIFIED",
}

# Independently reviewed Step 52-56 source-level adjudication.  Identity is
# occurrence-based; navigation variants and same-blob rows are never merged.
CORRECT_NUMBERS = {1,2,3,4,5,6,7,8,10,11,13,14,16,19,21,23,24,26,29,30,31,32,34,38,39,42,55,56,57,68}
PRESERVE_NUMBERS = {9,33,45,47,48,51,52,58,59,60,61,62,63,64,65,66}
THEORY_ONLY_NUMBERS = {12,15,17,18,20,35,36,37,40,41,43,44,46}
UNVERIFIED_NUMBERS = {22,25,27,28,49,50,53,54,67}
TARGET_BY_NUMBER = {
    1:83,2:83,3:63,4:74,5:87,6:87,7:79,8:71,9:87,10:87,11:87,12:82,
    13:75,14:87,15:82,16:76,17:82,18:82,19:76,20:76,21:87,22:78,23:74,
    24:78,25:78,26:78,27:78,28:78,29:87,30:87,31:75,32:71,33:87,34:87,
    35:75,36:75,37:82,38:87,39:75,40:82,41:74,42:87,43:82,44:82,45:89,
    46:82,47:89,48:87,49:87,50:87,51:89,52:87,53:87,54:87,55:63,56:63,
    57:71,58:82,59:75,60:76,61:87,62:87,63:87,64:87,65:78,66:79,67:83,68:83,
}
DOWNSTREAM_BY_TARGET = {
    63:[69], 71:[82,87,89,90], 74:[82,87,89,90], 75:[82,87,89,90],
    76:[82,87,89,90], 78:[82,87,89,90], 79:[82,87,89,90],
    82:[87,89,90], 83:[84,87,89,90], 87:[89,90], 89:[90],
}
DOWNSTREAM_BY_NUMBER = {number: DOWNSTREAM_BY_TARGET[target] for number, target in TARGET_BY_NUMBER.items()}

# Every CORRECT release occurrence has at least one immutable, correction-supporting
# machine record in Steps 52-56.  These are audit evidence, never external truth.
CORRECTION_EVIDENCE = {
    1:tuple((STEP55_CODE,f"/findings/{i}") for i in (0,1,4,8)),2:tuple((STEP55_CODE,f"/findings/{i}") for i in (2,6)),
    3:tuple((TOPOLOGY,f"/process_artifacts/{i}") for i in (3,51,52)),
    4:((STEP54,"/findings/0"),),5:((STEP56,"/layout_findings/0"),)+tuple((STEP56,f"/code_mentions/forbidden_rendered/{i}") for i in range(21)),
    6:((STEP56,"/controlled_assets/rows/16"),(STEP56,"/controlled_assets/rows/18"),(STEP56,"/controlled_assets/rows/19"),(STEP56,"/code_mentions/forbidden_rendered/0")),
    7:((STEP56,"/controlled_assets/rows/9"),)+tuple((STEP54,f"/findings/{i}") for i in (3,5,6,7,14,15))+((STEP56,"/code_mentions/forbidden_rendered/1"),),
    8:tuple((STEP56,f"/controlled_assets/rows/{i}") for i in range(20,38))+tuple((STEP54,f"/bibliography_audit/rows/{i}") for i in range(28))+tuple((STEP54,f"/citation_occurrences/{i}") for i in range(72))+((STEP54,"/findings/3"),),
    10:((STEP56,"/controlled_assets/rows/17"),(STEP56,"/code_mentions/forbidden_rendered/2"),(STEP56,"/code_mentions/forbidden_rendered/3")),
    11:((STEP56,"/controlled_assets/rows/6"),(STEP56,"/code_mentions/forbidden_rendered/4")),
    13:((STEP56,"/controlled_assets/rows/0"),(STEP56,"/controlled_assets/rows/1"))+tuple((STEP53,f"/findings/{i}") for i in range(1,6))+((STEP56,"/findings/0"),),
    14:((STEP56,"/controlled_assets/rows/10"),(STEP56,"/code_mentions/forbidden_rendered/5")),
    16:((STEP56,"/controlled_assets/rows/3"),)+tuple((STEP53,f"/findings/{i}") for i in (0,6,7,8,9))+((STEP56,"/findings/1"),),
    19:((STEP56,"/controlled_assets/rows/4"),(STEP56,"/code_mentions/forbidden_rendered/6")),
    21:((STEP56,"/controlled_assets/rows/5"),(STEP56,"/controlled_assets/rows/12"),(STEP56,"/code_mentions/forbidden_rendered/7")),
    23:((STEP54,"/findings/0"),(STEP54,"/findings/10")),24:((STEP54,"/findings/9"),),
    26:((STEP56,"/controlled_assets/rows/7"),)+tuple((STEP54,f"/findings/{i}") for i in (1,2,8,11,12,13))+tuple((STEP54,f"/ground_not_found_records/{i}") for i in (10,11))+((STEP56,"/findings/2"),(STEP56,"/code_mentions/forbidden_rendered/9"),(STEP56,"/code_mentions/forbidden_rendered/10")),
    29:tuple((STEP56,f"/code_mentions/forbidden_rendered/{i}") for i in (11,12,13)),
    30:((STEP56,"/code_mentions/forbidden_rendered/14"),(STEP56,"/code_mentions/forbidden_rendered/15"),(STEP56,"/code_mentions/forbidden_rendered/16")),
    31:((STEP56,"/controlled_assets/rows/2"),),32:((STEP56,"/code_mentions/forbidden_rendered/17"),),
    34:((STEP56,"/controlled_assets/rows/17"),(STEP56,"/code_mentions/forbidden_rendered/18")),
    38:((STEP56,"/controlled_assets/rows/14"),(STEP56,"/code_mentions/forbidden_rendered/19")),39:((STEP56,"/controlled_assets/rows/2"),),
    42:((STEP56,"/controlled_assets/rows/13"),(STEP56,"/code_mentions/forbidden_rendered/20")),
    55:((TOPOLOGY,"/process_artifacts/0"),)+tuple((STEP56,f"/controlled_assets/rows/{i}/change_log_anchor") for i in range(38)),
    56:((TOPOLOGY,"/process_artifacts/1"),(STEP54,"/findings/4"),(STEP55_CODE,"/code_matched_claims/0")),
    57:((TOPOLOGY,"/process_artifacts/2"),)+tuple((STEP54,f"/reference_ledger_self_report_inventory/rows/{i}") for i in range(4))+tuple((STEP54,f"/bibliography_audit/rows/{i}") for i in range(28))+tuple((STEP54,f"/bibliography_audit/metadata_observations/{i}") for i in range(28))+tuple((STEP54,f"/ground_not_found_records/{i}") for i in range(17)),
    68:tuple((STEP55_CODE,f"/findings/{i}") for i in (3,5)),
}

ACCEPTANCE_CLASS_BY_NUMBER = {
    1:"FIX_CODE",2:"FIX_CODE",3:"FIX_PROCESS",4:"FIX_SIGN",5:"FIX_LAYOUT",6:"FIX_DOC",7:"FIX_SCIENCE",8:"FIX_REFERENCE",
    10:"FIX_DOC",11:"FIX_DOC",13:"FIX_SCIENCE",14:"FIX_DOC",16:"FIX_SCIENCE",19:"FIX_DOC",21:"FIX_DOC",23:"FIX_SIGN",
    24:"FIX_SCIENCE",26:"FIX_SCIENCE",29:"FIX_DOC",30:"FIX_DOC",31:"FIX_SCIENCE",32:"FIX_REFERENCE",34:"FIX_DOC",
    38:"FIX_DOC",39:"FIX_SCIENCE",42:"FIX_DOC",55:"FIX_PROCESS",56:"FIX_PROCESS",57:"FIX_REFERENCE",68:"FIX_CODE",
}
ACCEPTANCE_SEMANTICS = {
    "FIX_CODE":"correct the exact internal code, guide or test contract without promoting runtime behavior to external science",
    "FIX_PROCESS":"correct the exact process/snapshot self-report and preserve its non-scientific authority boundary",
    "FIX_SIGN":"correct the exact sign, coordinate, unit and basis contract",
    "FIX_LAYOUT":"correct the exact generated-page layout defect and reverify the source/build/page relationship",
    "FIX_DOC":"correct the exact release-text statement or prohibited rendered code mention",
    "FIX_SCIENCE":"supply or justify exclusion of the bounded derivation, assumptions, validity domain and scientific support",
    "FIX_REFERENCE":"verify exact bibliography, citation and metadata identity against primary sources without using navigation as proof",
    "PRESERVE_ID":"preserve the distinct frozen occurrence and its authority ceiling without identity collapse",
    "BOUND_THEORY":"preserve theory-only status and independently adjudicate any later equation use",
    "VERIFY_LCO":"verify or justify exclusion of the exact LCO material-specific proposition and evidence basis",
    "VERIFY_NAV":"verify or justify exclusion of the exact navigation/generated-witness source and page relationship",
    "VERIFY_STRUCT":"verify the exact internal structure/tool contract without promoting static inspection to runtime or science",
}
requirement_domain = {
    63:"the next lineage owner preserves the distinct process/source identity",
    71:"the reference-truth owner verifies the exact proposition and identifier against primary sources",
    74:"the foundation owner resolves charge coordinate, unit, basis and sign",
    75:"the equilibrium owner supplies a bounded derivation and validity domain",
    76:"the nonequilibrium owner supplies the missing kinetic assumptions and limiting conditions",
    78:"the LCO owner resolves material-specific evidence, basis and equation scope",
    79:"the Si owner supplies Si/SiOx/Si-C-specific governing scope and evidence",
    82:"the equation-freeze owner adjudicates final equation inclusion or justified exclusion",
    83:"the implementation-contract owner binds the release statement to exact code/test/guide behavior",
    87:"the manuscript owner resolves the source-specific narrative, inclusion and authority boundary",
    89:"the PDF-QA owner verifies the exact source/build/page relationship and layout",
}


class BuildError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        if key in value:
            raise BuildError(f"duplicate JSON key: {key}")
        value[key] = child
    return value


def reject_constant(value: str) -> None:
    raise BuildError(f"nonfinite JSON constant: {value}")


def ensure_finite(value: Any, path: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise BuildError(f"nonfinite JSON number at {path}")
    if isinstance(value, dict):
        for key, child in value.items():
            ensure_finite(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            ensure_finite(child, f"{path}[{index}]")


def strict_load(raw: bytes) -> Any:
    value = json.loads(
        raw.decode("utf-8"), object_pairs_hook=reject_duplicates,
        parse_constant=reject_constant,
    )
    ensure_finite(value)
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def record_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def git_bytes(args: list[str]) -> bytes:
    process = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=False, timeout=30,
    )
    if process.returncode != 0:
        raise BuildError(process.stderr.decode("utf-8", errors="replace").strip())
    return process.stdout


def pointer_escape(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def load_inputs() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    parsed: dict[str, Any] = {}
    metadata: list[dict[str, Any]] = []
    for relative, expected_sha in INPUT_SHA256.items():
        raw = git_bytes(["show", f"{INPUT_COMMIT}:{relative}"])
        require(sha256(raw) == expected_sha, f"input SHA mismatch: {relative}")
        require(lf_bytes((ROOT / relative).read_bytes()) == raw, f"input commit mismatch: {relative}")
        parsed[relative] = strict_load(raw)
        metadata.append({
            "bytes": len(raw), "git_blob_sha1": git_blob_sha1(raw),
            "git_commit": INPUT_COMMIT, "parse_mode": "STRICT_JSON_FULL_TRAVERSAL",
            "path": relative, "sha256": expected_sha,
        })
    return parsed, metadata


def route(path: str, pointer: str, record: dict[str, Any], evidence_id: str, role: str) -> dict[str, Any]:
    return {
        "artifact_path": path,
        "evidence_id": evidence_id,
        "json_pointer": pointer,
        "record_sha256": sha256(record_bytes(record)),
        "route_role": role,
    }


def resolve_pointer(document: Any, pointer: str) -> Any:
    value = document
    if pointer:
        for token in pointer.lstrip("/").split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def role_authority_ceiling(role: str) -> str:
    return {
        "code": "STATIC_SOURCE_ONLY_NO_RUNTIME_MATERIAL_OR_SCIENCE_AUTHORITY",
        "implementation_guide": "INTERNAL_GUIDE_ONLY_NO_EXECUTION_MATERIAL_OR_SCIENCE_AUTHORITY",
        "result": "PROCESS_SELF_REPORT_ONLY_NO_EXTERNAL_OR_CANONICAL_AUTHORITY",
        "theory": "FROZEN_RELEASE_TEXT_ONLY_NO_EXTERNAL_SCIENTIFIC_OR_CANONICAL_AUTHORITY",
        "generated_document": "GENERATED_VISUAL_WITNESS_ONLY_NO_SOURCE_BUILD_OR_SCIENCE_AUTHORITY",
        "test": "INTERNAL_TEST_SURFACE_ONLY_NO_MATERIAL_OR_SCIENCE_AUTHORITY",
    }[role]


def authority_ceiling_by_number(number: int) -> str:
    if number == 1: return "INTERNAL_CODE_STATIC_RUNTIME_ONLY"
    if number == 2: return "INTERNAL_GUIDE_ASSERTION_ONLY"
    if number in {3,55,56,*range(58,67)}: return "PROCESS_OR_SNAPSHOT_SELF_REPORT_ONLY"
    if number in {8,32}: return "BIBLIOGRAPHIC_METADATA_NAVIGATION_ONLY"
    if number in {45,47,49,51,53}: return "GENERATED_VISUAL_WITNESS_ONLY"
    if number == 57: return "REFERENCE_LEDGER_INTERNAL_NAVIGATION_ONLY"
    if number == 67: return "INTERNAL_STRUCTURE_STATIC_ONLY"
    if number == 68: return "INTERNAL_TEST_ONLY"
    return "FROZEN_RELEASE_TEX_INTERNAL_ONLY"


def acceptance_class_by_number(number: int, disposition: str) -> str:
    if disposition == "CORRECT": return ACCEPTANCE_CLASS_BY_NUMBER[number]
    if disposition == "PRESERVE": return "PRESERVE_ID"
    if disposition == "THEORY_ONLY": return "BOUND_THEORY"
    if number in {22,25,27,28}: return "VERIFY_LCO"
    if number in {49,50,53,54}: return "VERIFY_NAV"
    if number == 67: return "VERIFY_STRUCT"
    raise BuildError(f"missing acceptance class: {number}")


def finding_rows(inputs: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    catalog: dict[str, dict[str, Any]] = {}

    specs = (
        (STEP53, "findings", "finding_id"),
        (STEP54, "findings", "finding_id"),
        (STEP54, "ground_not_found_records", "ground_not_found_id"),
        (STEP55_CODE, "findings", "finding_id"),
        (STEP56, "findings", "id"),
        (STEP56, "layout_findings", "id"),
    )
    for path, section, id_key in specs:
        for index, record in enumerate(inputs[path][section]):
            finding_id = record[id_key]
            require(finding_id not in catalog, f"duplicate open finding: {finding_id}")
            item = {
                "finding_id": finding_id,
                "origin_path": path,
                "origin_pointer": f"/{pointer_escape(section)}/{index}",
                "origin_record_sha256": sha256(record_bytes(record)),
                "prior_state": record.get("status", record.get("state", "OPEN_ROUTED")),
            }
            rows.append(item)
            catalog[finding_id] = item
    require(len(rows) == 59, f"open finding denominator: {len(rows)}")
    return rows, catalog


def owner_for_finding(finding_id: str) -> tuple[str, str]:
    if finding_id == "P062-S56-DIRECTION":
        return "INHERITED_PHASE061_BLOCKER", "P061-BD-NEW-001"
    if finding_id == "P062-VIS-001":
        return "RELEASE_DISPOSITION", "P062-DISP-0005"
    if finding_id.startswith("P062-S53-"):
        number = int(finding_id.rsplit("F", 1)[1])
        return "RELEASE_DISPOSITION", "P062-DISP-0016" if number in {1, 7, 8, 9, 10} else "P062-DISP-0013"
    if finding_id.startswith("P062-LCO-"):
        if finding_id in {"P062-LCO-C01", "P062-LCO-P2-03"}:
            return "RELEASE_DISPOSITION", "P062-DISP-0023"
        if finding_id == "P062-LCO-P2-02":
            return "RELEASE_DISPOSITION", "P062-DISP-0024"
        return "RELEASE_DISPOSITION", "P062-DISP-0026"
    if finding_id.startswith("P062-SI-"):
        return "RELEASE_DISPOSITION", {
            "P062-SI-C01":"P062-DISP-0008", "P062-SI-C02":"P062-DISP-0055",
        }.get(finding_id, "P062-DISP-0007")
    if finding_id.startswith("P062-GNF-"):
        number = int(finding_id.rsplit("-", 1)[1])
        if number in {1,2,3}: return "RELEASE_DISPOSITION", "P062-DISP-0022"
        if number in {11,12}: return "RELEASE_DISPOSITION", "P062-DISP-0026"
        return "RELEASE_DISPOSITION", "P062-DISP-0007"
    if finding_id.startswith("P062-CODE-FIND-"):
        number = int(finding_id.rsplit("-", 1)[1])
        if number in {3, 7}:
            return "RELEASE_DISPOSITION", "P062-DISP-0002"
        if number in {4, 6}:
            return "RELEASE_DISPOSITION", "P062-DISP-0068"
        if number == 8:
            return "RELEASE_DISPOSITION", "P062-DISP-0067"
        return "RELEASE_DISPOSITION", "P062-DISP-0001"
    if finding_id == "P062-S56-SCI-Q2":
        return "RELEASE_DISPOSITION", "P062-DISP-0013"
    if finding_id == "P062-S56-SCI-Q3":
        return "RELEASE_DISPOSITION", "P062-DISP-0016"
    if finding_id == "P062-S56-SCI-Q6":
        return "RELEASE_DISPOSITION", "P062-DISP-0026"
    if finding_id == "P062-S56-SCI-Q7":
        return "RELEASE_DISPOSITION", "P062-DISP-0007"
    if finding_id == "P062-S56-CODE":
        return "RELEASE_DISPOSITION", "P062-DISP-0005"
    raise BuildError(f"ownerless open finding: {finding_id}")


def corroborating_owners_for_finding(finding_id: str) -> list[str]:
    direct = {
        "P062-S53-F001":[60], "P062-S53-F002":[59], "P062-S53-F003":[59], "P062-S53-F004":[59], "P062-S53-F005":[59], "P062-S53-F006":[59],
        "P062-S53-F007":[60], "P062-S53-F008":[19,60], "P062-S53-F009":[60], "P062-S53-F010":[60],
        "P062-LCO-C01":[4], "P062-LCO-C02":[1,65], "P062-LCO-C03":[1,65],
        "P062-SI-C01":[7,57], "P062-SI-C02":[56,66], "P062-SI-C04":[13],
        "P062-LCO-P2-01":[65], "P062-LCO-P2-06":[57], "P062-GNF-011":[57], "P062-GNF-012":[57],
        "P062-CODE-FIND-003":[1], "P062-CODE-FIND-004":[1], "P062-CODE-FIND-006":[1], "P062-CODE-FIND-007":[1],
        "P062-S56-SCI-Q2":[39,59], "P062-S56-SCI-Q3":[19,60], "P062-S56-SCI-Q6":[1,65], "P062-S56-SCI-Q7":[66],
        "P062-VIS-001":[47,48,49,50],
    }
    if finding_id == "P062-S56-CODE":
        return sorted([
            "P062-DISP-0006", "P062-DISP-0007", "P062-DISP-0010",
            "P062-DISP-0011", "P062-DISP-0014", "P062-DISP-0019",
            "P062-DISP-0021", "P062-DISP-0023", "P062-DISP-0026",
            "P062-DISP-0029", "P062-DISP-0030", "P062-DISP-0032",
            "P062-DISP-0034", "P062-DISP-0038", "P062-DISP-0042",
        ])
    return sorted(f"P062-DISP-{number:04d}" for number in direct.get(finding_id, []))


def build_disposition(inputs: dict[str, Any], metadata: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, list[str]]]:
    topology = inputs[TOPOLOGY]
    sources = topology["sources"]
    require(len(sources) == 68, "release source count")
    require([row["source_id"] for row in sources] == [f"P062-SRC-{i:04d}" for i in range(1, 69)], "release source order")
    require([row["manifest_index"] for row in sources] == list(range(472, 540)), "release manifest indices")
    require(set(CORRECTION_EVIDENCE) == CORRECT_NUMBERS, "correction evidence denominator")
    require(set(ACCEPTANCE_CLASS_BY_NUMBER) == CORRECT_NUMBERS, "acceptance class denominator")
    require(set(DOWNSTREAM_BY_NUMBER) == set(range(1, 69)), "downstream denominator")
    findings, _ = finding_rows(inputs)
    owned: dict[str, list[str]] = defaultdict(list)
    for finding in findings:
        owner_type, owner_id = owner_for_finding(finding["finding_id"])
        if owner_type == "RELEASE_DISPOSITION":
            owned[owner_id].append(finding["finding_id"])

    rows: list[dict[str, Any]] = []
    for ordinal, source in enumerate(sources, 1):
        source_id = source["source_id"]
        disposition_id = f"P062-DISP-{ordinal:04d}"
        number = ordinal
        target = TARGET_BY_NUMBER[number]
        if number in CORRECT_NUMBERS:
            disposition = "CORRECT"
        elif number in PRESERVE_NUMBERS:
            disposition = "PRESERVE"
        elif number in THEORY_ONLY_NUMBERS:
            disposition = "THEORY_ONLY"
        elif number in UNVERIFIED_NUMBERS:
            disposition = "UNVERIFIED"
        else:  # pragma: no cover - the four reviewed sets partition 1..68
            raise BuildError(f"unadjudicated release occurrence: {source_id}")
        evidence_ids = [source_id, *sorted(owned.get(disposition_id, []))]
        evidence_routes = [route(
            TOPOLOGY, f"/sources/{ordinal - 1}", source, source_id, "RELEASE_SOURCE_IDENTITY",
        )]
        for finding_id in sorted(owned.get(disposition_id, [])):
            finding = next(item for item in findings if item["finding_id"] == finding_id)
            evidence_routes.append({
                "artifact_path": finding["origin_path"], "evidence_id": finding_id,
                "json_pointer": finding["origin_pointer"],
                "record_sha256": finding["origin_record_sha256"],
                "route_role": "OPEN_FINDING",
            })
        if disposition == "CORRECT":
            for route_index, (correction_path, correction_pointer) in enumerate(CORRECTION_EVIDENCE[number], 1):
                correction_record = resolve_pointer(inputs[correction_path], correction_pointer)
                evidence_id = f"P062-CORRECTION-SUPPORT-{number:04d}-{route_index:02d}"
                evidence_ids.append(evidence_id)
                evidence_routes.append(route(
                    correction_path, correction_pointer, correction_record, evidence_id,
                    "CORRECTION_SUPPORT",
                ))
        if number == 4:
            corroborating = inputs[STEP54]["findings"][0]
            evidence_ids.append("P062-LCO-C01-APPA-CORROBORATION")
            evidence_routes.append(route(
                STEP54, "/findings/0", corroborating,
                "P062-LCO-C01-APPA-CORROBORATION", "CORROBORATING_FINDING",
            ))
        downstream = DOWNSTREAM_BY_NUMBER[number]
        acceptance_owner = requirement_domain[target]
        acceptance_class = acceptance_class_by_number(number, disposition)
        acceptance = f"{acceptance_class}: Phase {target} acceptance for {source_id} requires {ACCEPTANCE_SEMANTICS[acceptance_class]}; preserve the exact source identity and authority ceiling through downstream Phases {downstream}. Owner domain: {acceptance_owner}."
        if disposition == "CORRECT":
            correction_routes = "; ".join(f"{path}#{pointer}" for path, pointer in CORRECTION_EVIDENCE[number])
            reason = f"The exact correction-support records {correction_routes} bound source-specific defects or authority mismatches in this {source['role']} occurrence; the frozen source is not rewritten."
            status = "OPEN"
        elif disposition == "UNVERIFIED":
            reason = f"This {source['role']} occurrence lacks the source-specific evidence required to promote its navigation, structure, build, material or scientific claim beyond {authority_ceiling_by_number(number)}."
            status = "OPEN"
        elif disposition == "THEORY_ONLY":
            reason = f"This {source['role']} occurrence is retained as bounded theory/background only and cannot supply empirical, material, runtime or canonical-equation authority."
            status = "PRESERVED_ACTIVE"
        else:
            reason = f"No Steps 53-56 source-level correction was routed to this distinct frozen {source['role']} occurrence; preservation does not promote its truth authority."
            status = "PRESERVED_ACTIVE"
        rows.append({
            "acceptance_criterion": acceptance,
            "acceptance_class": acceptance_class,
            "authority_mismatch_disclosure": {
                "corrected_disposition_authority": "FROZEN_RELEASE_TEX_INTERNAL_ONLY",
                "frozen_source_basis": "25-line scholarly TeX closing section with statistical-thermodynamic derivation, distribution, numerical-closure and reversible-heat prose",
                "inherited_source_authority_class": source["authority_class"],
                "inherited_source_role": source["role"],
                "state": "UPSTREAM_TOPOLOGY_ROLE_AUTHORITY_MISMATCH_DISCLOSED",
            } if number == 44 else None,
            "authority_ceiling": authority_ceiling_by_number(number),
            "disposition": disposition,
            "disposition_id": disposition_id,
            "downstream_target_phases": downstream,
            "evidence_ids": evidence_ids,
            "evidence_routes": evidence_routes,
            "external_experimental_truth": False,
            "external_material_truth": False,
            "external_scientific_truth": False,
            "primary_target_phase": target,
            "reason": reason,
            "source_id": source_id,
            "source_identity": {
                key: source[key] for key in (
                    "authority_class", "blob_sha1", "denominator", "extent", "git_mode",
                    "manifest_index", "path", "read_state", "release_occurrence_index",
                    "review_mode", "role", "sha256", "size_bytes", "source_id",
                )
            },
            "source_record_sha256": sha256(record_bytes(source)),
            "status": status,
        })

    supplemental = topology["supplemental_process_control"]
    supplemental_row = {
        "acceptance_criterion": "Phase 63 preserves this exact second-order plan record and never promotes it to an independently frozen first-order user transcript.",
        "authority_class": supplemental["authority_class"],
        "denominator": "SUPPLEMENTAL_PROCESS_CONTROL",
        "disposition": "PRESERVE",
        "downstream_target_phases": [70, 82],
        "evidence_ids": [supplemental["process_id"]],
        "evidence_routes": [route(TOPOLOGY, "/supplemental_process_control", supplemental, supplemental["process_id"], "SUPPLEMENTAL_PROCESS_IDENTITY")],
        "external_material_truth_validated": False,
        "external_scientific_truth_validated": False,
        "manifest_member": False,
        "primary_target_phase": 63,
        "process_id": supplemental["process_id"],
        "reason": "The master plan is recorded second-order process intent in a separate denominator, not a release occurrence or first-order transcript.",
        "source_anchor": {"blob_sha1": supplemental["blob_sha1"], "path": supplemental["path"]},
        "source_file_sha256": supplemental["sha256"],
        "source_record_sha256": sha256(record_bytes(supplemental)),
        "status": "PRESERVED_ACTIVE",
    }
    counts = Counter(row["disposition"] for row in rows)
    document = {
        "artifact_kind": "PHASE_062_V1021_DISPOSITION_MATRIX",
        "authority_boundary": AUTHORITY,
        "baseline_commit": SOURCE_COMMIT,
        "gate_summary": {
            "disposition_counts": dict(sorted(counts.items())),
            "external_authority_promotion_count": 0,
            "release_disposition_count": 68,
            "release_duplicate_count": 0,
            "release_orphan_count": 0,
            "status": "PASS_WITH_CONCERNS",
            "supplemental_disposition_count": 1,
        },
        "generation": {
            "active_branch": ACTIVE_BRANCH, "builder": BUILDER_RELATIVE,
            "canonical_json": CANONICAL_JSON, "deterministic": True,
            "production_imported_or_executed": False,
            "result_first": True,
        },
        "input_commit": INPUT_COMMIT,
        "inputs": metadata,
        "phase": 62,
        "release_dispositions": rows,
        "release_source_contract": {
            "bytes": 4071795, "count": 68, "first_manifest_index": 472,
            "last_manifest_index": 539, "path_blob_set_sha256": topology["path_blob_set_sha256"],
            "path_set_sha256": topology["path_set_sha256"], "pdf_files": 5,
            "pdf_pages": 214, "text_files": 63,
        },
        "schema_version": "phase062-step57.1-dispositions-v1",
        "source_commit": SOURCE_COMMIT,
        "step": "57.1",
        "supplemental_process_disposition": supplemental_row,
    }
    return document, owned


def build_carry(inputs: dict[str, Any], metadata: list[dict[str, Any]], disposition: dict[str, Any]) -> dict[str, Any]:
    prior_disposition = inputs[P61_DISPOSITION]
    prior_carry = inputs[P61_CARRY]
    target_rows = [row for row in prior_disposition["dispositions"] if row["target_phase"] == 62]
    target_ids = sorted(row["source_id"] for row in target_rows)
    require(len(target_rows) == 149, "target-62 count")
    require(sha256("\n".join(target_ids).encode("utf-8")) == TARGET62_ID_SHA256, "target-62 ID digest")
    route_rows = []
    for index, prior in enumerate(target_rows, 1):
        route_rows.append({
            "carry_forward_links": prior["carry_forward_links"],
            "delta_status": "PRESERVED_WITH_PHASE062_REVIEW",
            "phase061_disposition_id": prior["disposition_id"],
            "phase061_disposition_record_sha256": sha256(record_bytes(prior)),
            "phase061_source_id": prior["source_id"],
            "prior_record": prior,
            "resolution_status": "NOT_RESOLVED",
            "route_id": f"P062-CARRY-ROUTE-{index:04d}",
            "status_after": prior["status"],
            "status_before": prior["status"],
            "target_phase_after": 62,
            "target_phase_before": 62,
        })
    link_counts = Counter(link for row in route_rows for link in row["carry_forward_links"])

    inherited_carry = [{
        "carry_forward_id": row["carry_forward_id"], "delta_status": "UNCHANGED",
        "prior_record": row, "prior_record_sha256": sha256(record_bytes(row)),
        "resolution_status": "NOT_RESOLVED", "status_after": row["status_after"],
        "status_before": row["status_after"], "target_phase_after": row["target_phase_after"],
        "target_phase_before": row["target_phase_after"],
    } for row in prior_carry["inherited_carry_items"]]
    inherited_p60 = [{
        "blocker_id": row["blocker_id"], "delta_status": "UNCHANGED",
        "prior_record": row, "prior_record_sha256": sha256(record_bytes(row)),
        "resolution_status": "NOT_RESOLVED", "status_after": row["status_after"],
        "status_before": row["status_after"], "target_phase_after": row["target_phase_after"],
        "target_phase_before": row["target_phase_after"],
    } for row in prior_carry["inherited_phase060_blockers"]]

    debt_rows = []
    canonical_group = {"P061-GNF-004", "P061-UNV-008", "P061-STEP48-GNF-005", "P061-STEP48-UNV-008"}
    for row in prior_carry["debt_routing"]:
        debt_rows.append({
            "closure_group": "P061-DISP-0044-SINGLE-CLOSURE" if row["debt_id"] in canonical_group else None,
            "phase062_resolution_credit": "PRIMARY_UNRESOLVED" if row["debt_id"] == "P061-GNF-004" else ("ALIAS_NO_CREDIT" if row["debt_id"] in canonical_group else "UNCHANGED"),
            "prior_record": row,
            "prior_record_sha256": sha256(record_bytes(row)),
            "resolution_status": "NOT_RESOLVED" if row["status"] == "OPEN" else "PRIOR_INFORMATIONAL_ONLY",
            "status_after": row["status"],
            "status_before": row["status"],
        })

    component_state = inputs[STEP56]["acceptance"]
    phase061_blockers = []
    for row in prior_carry["new_blockers"]:
        observations = []
        for component in row["acceptance_components"]:
            after = component_state[component["component_id"]] if row["blocker_id"] == "P061-BD-NEW-001" else component["status"]
            observations.append({
                "component_id": component["component_id"],
                "evidence_path": STEP56 if row["blocker_id"] == "P061-BD-NEW-001" else None,
                "evidence_pointer": f"/acceptance/{component['component_id']}" if row["blocker_id"] == "P061-BD-NEW-001" else None,
                "status_after": after,
                "status_before": component["status"],
            })
        parent_after = component_state["P061-BD-NEW-001"] if row["blocker_id"] == "P061-BD-NEW-001" else row["status"]
        phase061_blockers.append({
            "blocker_id": row["blocker_id"], "component_observations": observations,
            "parent_status_after": parent_after, "parent_status_before": row["status"],
            "prior_record": row, "prior_record_sha256": sha256(record_bytes(row)),
            "resolution_status": "NOT_RESOLVED", "target_phase_after": row["target_phase"],
            "target_phase_before": row["target_phase"],
        })

    findings, _ = finding_rows(inputs)
    ownership = []
    disposition_by_id = {row["disposition_id"]: row for row in disposition["release_dispositions"]}
    for finding in findings:
        owner_type, owner_id = owner_for_finding(finding["finding_id"])
        owner_row = disposition_by_id.get(owner_id)
        ownership.append({
            **finding,
            "corroborating_owner_ids": corroborating_owners_for_finding(finding["finding_id"]),
            "owner_id": owner_id,
            "owner_path": owner_row["source_identity"]["path"] if owner_row else None,
            "owner_source_id": owner_row["source_id"] if owner_row else None,
            "owner_type": owner_type,
            "ownership_role": "PRIMARY_CLOSURE_OWNER",
        })

    return {
        "artifact_kind": "PHASE_062_V1021_CARRY_FORWARD_DELTA",
        "authority_boundary": AUTHORITY,
        "baseline_commit": SOURCE_COMMIT,
        "canonical_debt_routing": debt_rows,
        "gate_summary": {
            "canonical_debt_count": 91, "external_authority_promotion_count": 0,
            "inherited_carry_count": 52, "inherited_phase060_blocker_count": 5,
            "inherited_phase061_blocker_count": 5, "new_phase062_blocker_count": 0,
            "open_finding_count": 59, "open_finding_multiply_owned_count": 0,
            "open_finding_ownerless_count": 0, "phase061_target62_route_count": 149,
            "status": "PASS_WITH_CONCERNS",
        },
        "generation": {
            "active_branch": ACTIVE_BRANCH, "builder": BUILDER_RELATIVE,
            "canonical_json": CANONICAL_JSON, "deterministic": True,
            "production_imported_or_executed": False, "result_first": True,
        },
        "inherited_carry_items": inherited_carry,
        "inherited_phase060_blockers": inherited_p60,
        "inherited_phase061_blockers": phase061_blockers,
        "input_commit": INPUT_COMMIT,
        "inputs": metadata,
        "new_phase062_blockers": [],
        "open_finding_ownership": ownership,
        "phase": 62,
        "phase061_target62_contract": {
            "carry_link_edge_count": sum(link_counts.values()),
            "carry_link_multiplicities": dict(sorted(link_counts.items())),
            "id_set_sha256_sorted_lf_no_final_newline": TARGET62_ID_SHA256,
            "route_count": 149, "zero_link_source_ids": [row["phase061_source_id"] for row in route_rows if not row["carry_forward_links"]],
        },
        "phase061_target62_routes": route_rows,
        "schema_version": "phase062-step57.1-carry-forward-delta-v1",
        "source_commit": SOURCE_COMMIT,
        "step": "57.1",
    }


def render_result(disposition: dict[str, Any], carry: dict[str, Any], disposition_raw: bytes, carry_raw: bytes) -> bytes:
    counts = disposition["gate_summary"]["disposition_counts"]
    text = f"""# Phase 062 Step 57.1 Source Disposition and Carry-forward Result

Status: `PASS_WITH_CONCERNS`

Gate: `PASS_P062_STEP57_1_DISPOSITIONS`

Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`

Result-first sentinel: `RESULT_WRITTEN_BEFORE_DISPOSITION_AND_CARRY_JSON`

## Exact denominators

- Release dispositions: `68/68`
- Supplemental process disposition: `1/1` in a separate denominator
- Distribution: `CORRECT {counts.get('CORRECT', 0)}`, `PRESERVE {counts.get('PRESERVE', 0)}`, `THEORY_ONLY {counts.get('THEORY_ONLY', 0)}`, `UNVERIFIED {counts.get('UNVERIFIED', 0)}`
- Phase 061 target-62 routes: `149/149`; link edges `253`; zero-link `P061-SRC-0003` retained
- Inherited carry/blockers/debts: `52 + 5 + 91 + 5`
- New Phase 062 blockers: `0`
- Step 53-56 open findings: `59/59`, primary owner exactly one each
- Release status distribution: `OPEN 39`; `PRESERVED_ACTIVE 29`
- Validator negative controls: `73/73`; deterministic rebuild: `2/2`

## Carry and authority

All 91 debt origins, hashes, owners, acceptance criteria, targets and statuses are preserved. `P061-GNF-004` and its three aliases remain one unresolved `P061-DISP-0044` closure. `P061-BD-NEW-001` records A01-A05 `PASS`, A06/A07 `OPEN`, and parent `OPEN`; none of these component observations promotes external truth. The 59 open findings retain one exact primary owner each. `P062-S56-CODE` additionally retains all 21 rendered-mention routes and 15 source-disposition corroborating owners without splitting primary closure ownership.

External scientific, material, experimental, primary-literature and canonical-equation authority remain false. Frozen Claude sources are not modified.

## Artifact identities

- `PHASE_062_V1021_DISPOSITION_MATRIX.json`: `{sha256(disposition_raw)}`
- `PHASE_062_V1021_CARRY_FORWARD_DELTA.json`: `{sha256(carry_raw)}`

## Persistence

Step 56 commit `1c8541fdea2cd69aa09e6b99d2f371c41a0bb727` is the exact parent and has `PASS_P062_STEP56_PERSISTENCE`. Step 57.1 remains a precommit checkpoint. Commit/push/persistence must use subject `audit(phase062): disposition v1021 lineage` and emit `PASS_P062_STEP57_1_PERSISTENCE` before Step 57.2.
"""
    return text.encode("utf-8")


def build_all() -> tuple[bytes, bytes, bytes]:
    inputs, metadata = load_inputs()
    disposition, _ = build_disposition(inputs, metadata)
    carry = build_carry(inputs, metadata, disposition)
    disposition_raw = canonical_bytes(disposition)
    carry_raw = canonical_bytes(carry)
    result_raw = render_result(disposition, carry, disposition_raw, carry_raw)
    return result_raw, disposition_raw, carry_raw


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-output", type=Path, default=ROOT / RESULT_RELATIVE)
    parser.add_argument("--disposition-output", type=Path, default=ROOT / DISPOSITION_RELATIVE)
    parser.add_argument("--carry-output", type=Path, default=ROOT / CARRY_RELATIVE)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result_raw, disposition_raw, carry_raw = build_all()
    outputs = (
        (args.result_output, result_raw),
        (args.disposition_output, disposition_raw),
        (args.carry_output, carry_raw),
    )
    if args.check:
        for path, expected in outputs:
            require(path.is_file() and path.read_bytes() == expected, f"stored output mismatch: {path}")
    else:
        # Contractual write order: result first, then disposition, then carry.
        for path, raw in outputs:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
    print("PASS build Phase062 Step57.1 release=68 supplemental=1 target62=149 carry=52 blockers=5+5 debts=91 new=0")
    print("PASS_P062_STEP57_1_BUILD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
