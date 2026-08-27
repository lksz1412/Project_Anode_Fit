#!/usr/bin/env python3
"""Independent fail-closed validator for Phase 062 Step 57.1."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
ACTIVE_BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
PARENT_COMMIT = "1c8541fdea2cd69aa09e6b99d2f371c41a0bb727"
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
SUBJECT = "audit(phase062): disposition v1021 lineage"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
TARGET62_SHA = "68267522dbda5c3a47fccfaad0babb2617331f2208831f36f91ec2ea284f11a5"

BUILDER = ROOT / "Codex/work/v1021_phase062/build_phase062_step57_dispositions.py"
VALIDATOR = Path(__file__)
DISPOSITION = ROOT / "Codex/results/PHASE_062_V1021_DISPOSITION_MATRIX.json"
CARRY = ROOT / "Codex/results/PHASE_062_V1021_CARRY_FORWARD_DELTA.json"
RESULT = ROOT / "Codex/results/PHASE_062_STEP_057_1_DISPOSITION_RESULT.md"
PARENT_LEDGER = ROOT / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER = ROOT / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = ROOT / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
EXPECTED_PATHS = {str(path.relative_to(ROOT)).replace("\\", "/") for path in (BUILDER, VALIDATOR, DISPOSITION, CARRY, RESULT, PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER)}

TOPOLOGY = "Codex/results/PHASE_062_V1021_SOURCE_PROCESS_TOPOLOGY.json"
READ_ATTESTATION = "Codex/results/PHASE_062_V1021_READ_ATTESTATION.json"
STEP53 = "Codex/results/PHASE_062_V1021_STATMECH_TST_REDERIVATION.json"
STEP54 = "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json"
STEP55_CODE = "Codex/results/PHASE_062_V1021_CODE_DELTA_MATRIX.json"
STEP55_RUNTIME = "Codex/results/PHASE_062_V1021_RUNTIME_ATTESTATION.json"
STEP56 = "Codex/results/PHASE_062_V1021_PHYSICS_CLOSURE_MATRIX.json"
P61_DISPOSITION = "Codex/results/PHASE_061_V1020_DISPOSITION_MATRIX.json"
P61_CARRY = "Codex/results/PHASE_061_V1020_CARRY_FORWARD_DELTA.json"
INPUT_SHA = {
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
CORRECT = {1,2,3,4,5,6,7,8,10,11,13,14,16,19,21,23,24,26,29,30,31,32,34,38,39,42,55,56,57,68}
PRESERVE = {9,33,45,47,48,51,52,58,59,60,61,62,63,64,65,66}
THEORY_ONLY = {12,15,17,18,20,35,36,37,40,41,43,44,46}
UNVERIFIED = {22,25,27,28,49,50,53,54,67}
TARGETS = [83,83,63,74,87,87,79,71,87,87,87,82,75,87,82,76,82,82,76,76,87,78,74,78,78,78,78,78,87,87,75,71,87,87,75,75,82,87,75,82,74,87,82,82,89,82,89,87,87,87,89,87,87,87,63,63,71,82,75,76,87,87,87,87,78,79,83,83]
DOWNSTREAM_BY_TARGET = {63:[69],71:[82,87,89,90],74:[82,87,89,90],75:[82,87,89,90],76:[82,87,89,90],78:[82,87,89,90],79:[82,87,89,90],82:[87,89,90],83:[84,87,89,90],87:[89,90],89:[90]}
DOWNSTREAM = [DOWNSTREAM_BY_TARGET[target] for target in TARGETS]
CORRECTION_EVIDENCE = {
 1:tuple((STEP55_CODE,f"/findings/{i}") for i in (0,1,4,8)),2:tuple((STEP55_CODE,f"/findings/{i}") for i in (2,6)),3:tuple((TOPOLOGY,f"/process_artifacts/{i}") for i in (3,51,52)),4:((STEP54,"/findings/0"),),5:((STEP56,"/layout_findings/0"),)+tuple((STEP56,f"/code_mentions/forbidden_rendered/{i}") for i in range(21)),
 6:((STEP56,"/controlled_assets/rows/16"),(STEP56,"/controlled_assets/rows/18"),(STEP56,"/controlled_assets/rows/19"),(STEP56,"/code_mentions/forbidden_rendered/0")),
 7:((STEP56,"/controlled_assets/rows/9"),)+tuple((STEP54,f"/findings/{i}") for i in (3,5,6,7,14,15))+((STEP56,"/code_mentions/forbidden_rendered/1"),),
 8:tuple((STEP56,f"/controlled_assets/rows/{i}") for i in range(20,38))+tuple((STEP54,f"/bibliography_audit/rows/{i}") for i in range(28))+tuple((STEP54,f"/citation_occurrences/{i}") for i in range(72))+((STEP54,"/findings/3"),),
 10:((STEP56,"/controlled_assets/rows/17"),(STEP56,"/code_mentions/forbidden_rendered/2"),(STEP56,"/code_mentions/forbidden_rendered/3")),11:((STEP56,"/controlled_assets/rows/6"),(STEP56,"/code_mentions/forbidden_rendered/4")),
 13:((STEP56,"/controlled_assets/rows/0"),(STEP56,"/controlled_assets/rows/1"))+tuple((STEP53,f"/findings/{i}") for i in range(1,6))+((STEP56,"/findings/0"),),14:((STEP56,"/controlled_assets/rows/10"),(STEP56,"/code_mentions/forbidden_rendered/5")),
 16:((STEP56,"/controlled_assets/rows/3"),)+tuple((STEP53,f"/findings/{i}") for i in (0,6,7,8,9))+((STEP56,"/findings/1"),),19:((STEP56,"/controlled_assets/rows/4"),(STEP56,"/code_mentions/forbidden_rendered/6")),21:((STEP56,"/controlled_assets/rows/5"),(STEP56,"/controlled_assets/rows/12"),(STEP56,"/code_mentions/forbidden_rendered/7")),
 23:((STEP54,"/findings/0"),(STEP54,"/findings/10")),24:((STEP54,"/findings/9"),),26:((STEP56,"/controlled_assets/rows/7"),)+tuple((STEP54,f"/findings/{i}") for i in (1,2,8,11,12,13))+tuple((STEP54,f"/ground_not_found_records/{i}") for i in (10,11))+((STEP56,"/findings/2"),(STEP56,"/code_mentions/forbidden_rendered/9"),(STEP56,"/code_mentions/forbidden_rendered/10")),
 29:tuple((STEP56,f"/code_mentions/forbidden_rendered/{i}") for i in (11,12,13)),30:tuple((STEP56,f"/code_mentions/forbidden_rendered/{i}") for i in (14,15,16)),31:((STEP56,"/controlled_assets/rows/2"),),32:((STEP56,"/code_mentions/forbidden_rendered/17"),),34:((STEP56,"/controlled_assets/rows/17"),(STEP56,"/code_mentions/forbidden_rendered/18")),38:((STEP56,"/controlled_assets/rows/14"),(STEP56,"/code_mentions/forbidden_rendered/19")),39:((STEP56,"/controlled_assets/rows/2"),),42:((STEP56,"/controlled_assets/rows/13"),(STEP56,"/code_mentions/forbidden_rendered/20")),
 55:((TOPOLOGY,"/process_artifacts/0"),)+tuple((STEP56,f"/controlled_assets/rows/{i}/change_log_anchor") for i in range(38)),56:((TOPOLOGY,"/process_artifacts/1"),(STEP54,"/findings/4"),(STEP55_CODE,"/code_matched_claims/0")),
 57:((TOPOLOGY,"/process_artifacts/2"),)+tuple((STEP54,f"/reference_ledger_self_report_inventory/rows/{i}") for i in range(4))+tuple((STEP54,f"/bibliography_audit/rows/{i}") for i in range(28))+tuple((STEP54,f"/bibliography_audit/metadata_observations/{i}") for i in range(28))+tuple((STEP54,f"/ground_not_found_records/{i}") for i in range(17)),68:tuple((STEP55_CODE,f"/findings/{i}") for i in (3,5)),
}
ACCEPTANCE_CLASS_CORRECT={1:"FIX_CODE",2:"FIX_CODE",3:"FIX_PROCESS",4:"FIX_SIGN",5:"FIX_LAYOUT",6:"FIX_DOC",7:"FIX_SCIENCE",8:"FIX_REFERENCE",10:"FIX_DOC",11:"FIX_DOC",13:"FIX_SCIENCE",14:"FIX_DOC",16:"FIX_SCIENCE",19:"FIX_DOC",21:"FIX_DOC",23:"FIX_SIGN",24:"FIX_SCIENCE",26:"FIX_SCIENCE",29:"FIX_DOC",30:"FIX_DOC",31:"FIX_SCIENCE",32:"FIX_REFERENCE",34:"FIX_DOC",38:"FIX_DOC",39:"FIX_SCIENCE",42:"FIX_DOC",55:"FIX_PROCESS",56:"FIX_PROCESS",57:"FIX_REFERENCE",68:"FIX_CODE"}
ACCEPTANCE_SEMANTICS={"FIX_CODE":"correct the exact internal code, guide or test contract without promoting runtime behavior to external science","FIX_PROCESS":"correct the exact process/snapshot self-report and preserve its non-scientific authority boundary","FIX_SIGN":"correct the exact sign, coordinate, unit and basis contract","FIX_LAYOUT":"correct the exact generated-page layout defect and reverify the source/build/page relationship","FIX_DOC":"correct the exact release-text statement or prohibited rendered code mention","FIX_SCIENCE":"supply or justify exclusion of the bounded derivation, assumptions, validity domain and scientific support","FIX_REFERENCE":"verify exact bibliography, citation and metadata identity against primary sources without using navigation as proof","PRESERVE_ID":"preserve the distinct frozen occurrence and its authority ceiling without identity collapse","BOUND_THEORY":"preserve theory-only status and independently adjudicate any later equation use","VERIFY_LCO":"verify or justify exclusion of the exact LCO material-specific proposition and evidence basis","VERIFY_NAV":"verify or justify exclusion of the exact navigation/generated-witness source and page relationship","VERIFY_STRUCT":"verify the exact internal structure/tool contract without promoting static inspection to runtime or science"}
ACCEPTANCE_DOMAIN = {
 63:"the next lineage owner preserves the distinct process/source identity",71:"the reference-truth owner verifies the exact proposition and identifier against primary sources",
 74:"the foundation owner resolves charge coordinate, unit, basis and sign",75:"the equilibrium owner supplies a bounded derivation and validity domain",
 76:"the nonequilibrium owner supplies the missing kinetic assumptions and limiting conditions",78:"the LCO owner resolves material-specific evidence, basis and equation scope",
 79:"the Si owner supplies Si/SiOx/Si-C-specific governing scope and evidence",82:"the equation-freeze owner adjudicates final equation inclusion or justified exclusion",
 83:"the implementation-contract owner binds the release statement to exact code/test/guide behavior",87:"the manuscript owner resolves the source-specific narrative, inclusion and authority boundary",
 89:"the PDF-QA owner verifies the exact source/build/page relationship and layout",
}
EXPECTED_DISTRIBUTION = Counter({"CORRECT":30,"PRESERVE":16,"THEORY_ONLY":13,"UNVERIFIED":9})
EXPECTED_LINKS = {"P059-CFR-CF-11":141,"P059-CFR-RB-12":93,"P059-CFR-CF-08":5,"P059-CFR-RB-11":5,"P059-CFR-ED-03":3,"P059-CFR-NS-05":3,"P059-CFR-RM-011":3}
EXPECTED_DISPOSITION_SHA = "8789ca7eaca571e9e718f898893878179eff992d860e78e20d68402033d3502e"
EXPECTED_CARRY_SHA = "e5803c9925ca7a95a1e31d43da2aa673a703db87ed1e47ca3d95bb29320bd863"
EXPECTED_BUILDER_LF_SHA = "c086791fc85415f7c856338c1a4ec32f737ede16f81338e9eef75dc30e9d9ea1"
EXPECTED_BUILDER_AST_SHA = "71ba4b7371e440768a25135cb9f6e416fa018364fb9019a597deb5d1abdb8548"
EXPECTED_DISPOSITION_ARTIFACT_SHA = "2a75fe6ef35ee71a0de8c576ef81fa27eadffc0101a90ad6c491c1b8f410f62c"
EXPECTED_CARRY_ARTIFACT_SHA = "9df1a9203d8b9df60232073130e5abec857cfc7a7973bf591bb7d7488e4f2614"
CONTROL_LF_SHA = {
    RESULT: "a8530fc519bccfbba25980f2e4d091031ebfa430e4adcfd42a434537639763e7",
    PARENT_LEDGER: "03019dac2e9081cef1bb89a15dc660811c5f6666f2298982b6a8a89db7ff96d3",
    ACTIVE_LEDGER: "90100f38b23c34181e360cd52a8a7b706e5b1de162e111909e760d735042c98a",
    HANDOVER: "bc6736bf2e203456b88812b196538ab59ee3e6ae69041bd3249631c49d504329",
}

DISP_TOP = {"artifact_kind","authority_boundary","baseline_commit","gate_summary","generation","input_commit","inputs","phase","release_dispositions","release_source_contract","schema_version","source_commit","step","supplemental_process_disposition"}
DISP_ROW = {"acceptance_class","acceptance_criterion","authority_ceiling","authority_mismatch_disclosure","disposition","disposition_id","downstream_target_phases","evidence_ids","evidence_routes","external_experimental_truth","external_material_truth","external_scientific_truth","primary_target_phase","reason","source_id","source_identity","source_record_sha256","status"}
SUPPLEMENTAL_ROW = {"acceptance_criterion","authority_class","denominator","disposition","downstream_target_phases","evidence_ids","evidence_routes","external_material_truth_validated","external_scientific_truth_validated","manifest_member","primary_target_phase","process_id","reason","source_anchor","source_file_sha256","source_record_sha256","status"}
EVIDENCE_ROUTE_ROW = {"artifact_path","evidence_id","json_pointer","record_sha256","route_role"}
OPEN_FINDING_OWNER_ROW = {"corroborating_owner_ids","finding_id","origin_path","origin_pointer","origin_record_sha256","owner_id","owner_path","owner_source_id","owner_type","ownership_role","prior_state"}
CARRY_TOP = {"artifact_kind","authority_boundary","baseline_commit","canonical_debt_routing","gate_summary","generation","inherited_carry_items","inherited_phase060_blockers","inherited_phase061_blockers","input_commit","inputs","new_phase062_blockers","open_finding_ownership","phase","phase061_target62_contract","phase061_target62_routes","schema_version","source_commit","step"}
CARRY_ROUTE_ROW={"carry_forward_links","delta_status","phase061_disposition_id","phase061_disposition_record_sha256","phase061_source_id","prior_record","resolution_status","route_id","status_after","status_before","target_phase_after","target_phase_before"}
INHERITED_WRAPPER_ROW={"carry_forward_id","delta_status","prior_record","prior_record_sha256","resolution_status","status_after","status_before","target_phase_after","target_phase_before"}
BLOCKER_WRAPPER_ROW={"blocker_id","delta_status","prior_record","prior_record_sha256","resolution_status","status_after","status_before","target_phase_after","target_phase_before"}
DEBT_WRAPPER_ROW={"closure_group","phase062_resolution_credit","prior_record","prior_record_sha256","resolution_status","status_after","status_before"}
P61_BLOCKER_ROW={"blocker_id","component_observations","parent_status_after","parent_status_before","prior_record","prior_record_sha256","resolution_status","target_phase_after","target_phase_before"}
COMPONENT_ROW={"component_id","evidence_path","evidence_pointer","status_after","status_before"}
CARRY_GATE_KEYS={"canonical_debt_count","external_authority_promotion_count","inherited_carry_count","inherited_phase060_blocker_count","inherited_phase061_blocker_count","new_phase062_blocker_count","open_finding_count","open_finding_multiply_owned_count","open_finding_ownerless_count","phase061_target62_route_count","status"}
GENERATION_KEYS={"active_branch","builder","canonical_json","deterministic","production_imported_or_executed","result_first"}
TARGET62_CONTRACT_KEYS={"carry_link_edge_count","carry_link_multiplicities","id_set_sha256_sorted_lf_no_final_newline","route_count","zero_link_source_ids"}


class ValidationError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}"); self.code = code


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result: raise ValidationError("JSON_DUPLICATE", key)
        result[key] = value
    return result


def reject_constant(value: str) -> None: raise ValidationError("JSON_NONFINITE", value)


def ensure_finite(value: Any, path: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value): raise ValidationError("JSON_NONFINITE", path)
    if isinstance(value, dict):
        for key, child in value.items(): ensure_finite(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value): ensure_finite(child, f"{path}[{index}]")


def strict_load(raw: bytes) -> Any:
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicates, parse_constant=reject_constant); ensure_finite(value); return value


def canonical_bytes(value: Any) -> bytes: return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
def record_bytes(value: Any) -> bytes: return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
def sha256(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()
def lf_bytes(raw: bytes) -> bytes: return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
def git_blob_sha1(raw: bytes) -> str: return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def canonical_ast_value(value: Any) -> Any:
    """Version-neutral explicit-field AST projection; empty optional fields are omitted."""
    if isinstance(value, ast.AST):
        fields: dict[str, Any] = {}
        for name, child in ast.iter_fields(value):
            projected = canonical_ast_value(child)
            if projected is not None and projected != []:
                fields[name] = projected
        return {"fields": fields, "type": type(value).__name__}
    if isinstance(value, list):
        return [canonical_ast_value(child) for child in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, bytes):
        return {"bytes_hex": value.hex()}
    return {"repr": repr(value)}


def canonical_ast_bytes(node: ast.AST) -> bytes:
    return json.dumps(canonical_ast_value(node), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def git_bytes(args: list[str], cwd: Path = ROOT, timeout: int = 30) -> bytes:
    try: process = subprocess.run(["git", *args], cwd=cwd, capture_output=True, check=False, timeout=timeout)
    except subprocess.TimeoutExpired as error: raise ValidationError("GIT_TIMEOUT", str(args)) from error
    if process.returncode != 0: raise ValidationError("GIT_COMMAND", process.stderr.decode("utf-8", errors="replace").strip())
    return process.stdout


def git_text(args: list[str], cwd: Path = ROOT) -> str: return git_bytes(args, cwd).decode("utf-8").strip()


def load_inputs() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    parsed, metadata = {}, []
    for path, digest in INPUT_SHA.items():
        raw = git_bytes(["show", f"{PARENT_COMMIT}:{path}"])
        if sha256(raw) != digest: raise ValidationError("INPUT_SHA", path)
        if lf_bytes((ROOT / path).read_bytes()) != raw: raise ValidationError("INPUT_COMMIT_BLOB", path)
        parsed[path] = strict_load(raw)
        metadata.append({"bytes":len(raw),"git_blob_sha1":git_blob_sha1(raw),"git_commit":PARENT_COMMIT,"parse_mode":"STRICT_JSON_FULL_TRAVERSAL","path":path,"sha256":digest})
    return parsed, metadata


def expected_disposition(number: int) -> str:
    if number in CORRECT: return "CORRECT"
    if number in PRESERVE: return "PRESERVE"
    if number in THEORY_ONLY: return "THEORY_ONLY"
    if number in UNVERIFIED: return "UNVERIFIED"
    raise ValidationError("DISPOSITION_COVERAGE", str(number))


def resolve_pointer(document: Any, pointer: str) -> Any:
    value = document
    if pointer:
        for token in pointer.lstrip("/").split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def expected_authority(number: int) -> str:
    if number == 1: return "INTERNAL_CODE_STATIC_RUNTIME_ONLY"
    if number == 2: return "INTERNAL_GUIDE_ASSERTION_ONLY"
    if number in {3,55,56,*range(58,67)}: return "PROCESS_OR_SNAPSHOT_SELF_REPORT_ONLY"
    if number in {8,32}: return "BIBLIOGRAPHIC_METADATA_NAVIGATION_ONLY"
    if number in {45,47,49,51,53}: return "GENERATED_VISUAL_WITNESS_ONLY"
    if number == 57: return "REFERENCE_LEDGER_INTERNAL_NAVIGATION_ONLY"
    if number == 67: return "INTERNAL_STRUCTURE_STATIC_ONLY"
    if number == 68: return "INTERNAL_TEST_ONLY"
    return "FROZEN_RELEASE_TEX_INTERNAL_ONLY"


def expected_acceptance_class(number: int, disposition: str) -> str:
    if disposition == "CORRECT": return ACCEPTANCE_CLASS_CORRECT[number]
    if disposition == "PRESERVE": return "PRESERVE_ID"
    if disposition == "THEORY_ONLY": return "BOUND_THEORY"
    if number in {22,25,27,28}: return "VERIFY_LCO"
    if number in {49,50,53,54}: return "VERIFY_NAV"
    if number == 67: return "VERIFY_STRUCT"
    raise ValidationError("ACCEPTANCE_CLASS",str(number))


def expected_acceptance(number: int, source_id: str, disposition: str) -> str:
    target=TARGETS[number-1]; downstream=DOWNSTREAM[number-1]; domain=ACCEPTANCE_DOMAIN[target]; klass=expected_acceptance_class(number,disposition)
    return f"{klass}: Phase {target} acceptance for {source_id} requires {ACCEPTANCE_SEMANTICS[klass]}; preserve the exact source identity and authority ceiling through downstream Phases {downstream}. Owner domain: {domain}."


def expected_reason(number: int, role: str, disposition: str) -> str:
    if disposition == "CORRECT":
        routes="; ".join(f"{path}#{pointer}" for path,pointer in CORRECTION_EVIDENCE[number])
        return f"The exact correction-support records {routes} bound source-specific defects or authority mismatches in this {role} occurrence; the frozen source is not rewritten."
    if disposition == "UNVERIFIED":
        return f"This {role} occurrence lacks the source-specific evidence required to promote its navigation, structure, build, material or scientific claim beyond {expected_authority(number)}."
    if disposition == "THEORY_ONLY":
        return f"This {role} occurrence is retained as bounded theory/background only and cannot supply empirical, material, runtime or canonical-equation authority."
    return f"No Steps 53-56 source-level correction was routed to this distinct frozen {role} occurrence; preservation does not promote its truth authority."


def expected_owner(finding_id: str) -> tuple[str, str]:
    if finding_id == "P062-S56-DIRECTION": return "INHERITED_PHASE061_BLOCKER", "P061-BD-NEW-001"
    if finding_id == "P062-VIS-001": return "RELEASE_DISPOSITION", "P062-DISP-0005"
    if finding_id.startswith("P062-S53-"):
        number=int(finding_id.rsplit("F",1)[1]); return "RELEASE_DISPOSITION", "P062-DISP-0016" if number in {1,7,8,9,10} else "P062-DISP-0013"
    if finding_id.startswith("P062-LCO-"):
        if finding_id in {"P062-LCO-C01","P062-LCO-P2-03"}: return "RELEASE_DISPOSITION","P062-DISP-0023"
        if finding_id == "P062-LCO-P2-02": return "RELEASE_DISPOSITION","P062-DISP-0024"
        return "RELEASE_DISPOSITION","P062-DISP-0026"
    if finding_id.startswith("P062-SI-"):
        return "RELEASE_DISPOSITION", {"P062-SI-C01":"P062-DISP-0008","P062-SI-C02":"P062-DISP-0055"}.get(finding_id,"P062-DISP-0007")
    if finding_id.startswith("P062-GNF-"):
        number=int(finding_id.rsplit("-",1)[1])
        if number in {1,2,3}: return "RELEASE_DISPOSITION","P062-DISP-0022"
        if number in {11,12}: return "RELEASE_DISPOSITION","P062-DISP-0026"
        return "RELEASE_DISPOSITION","P062-DISP-0007"
    if finding_id.startswith("P062-CODE-FIND-"):
        number=int(finding_id.rsplit("-",1)[1])
        if number in {3,7}: return "RELEASE_DISPOSITION","P062-DISP-0002"
        if number in {4,6}: return "RELEASE_DISPOSITION","P062-DISP-0068"
        if number == 8: return "RELEASE_DISPOSITION","P062-DISP-0067"
        return "RELEASE_DISPOSITION","P062-DISP-0001"
    mapping={"P062-S56-SCI-Q2":"P062-DISP-0013","P062-S56-SCI-Q3":"P062-DISP-0016","P062-S56-SCI-Q6":"P062-DISP-0026","P062-S56-SCI-Q7":"P062-DISP-0007","P062-S56-CODE":"P062-DISP-0005"}
    if finding_id in mapping:return "RELEASE_DISPOSITION",mapping[finding_id]
    raise ValidationError("UNKNOWN_FINDING_OWNER",finding_id)


def expected_corroborating_owners(finding_id: str) -> list[str]:
    direct={
        "P062-S53-F001":[60],"P062-S53-F002":[59],"P062-S53-F003":[59],"P062-S53-F004":[59],"P062-S53-F005":[59],"P062-S53-F006":[59],"P062-S53-F007":[60],"P062-S53-F008":[19,60],"P062-S53-F009":[60],"P062-S53-F010":[60],
        "P062-LCO-C01":[4],"P062-LCO-C02":[1,65],"P062-LCO-C03":[1,65],"P062-SI-C01":[7,57],"P062-SI-C02":[56,66],"P062-SI-C04":[13],"P062-LCO-P2-01":[65],"P062-LCO-P2-06":[57],"P062-GNF-011":[57],"P062-GNF-012":[57],
        "P062-CODE-FIND-003":[1],"P062-CODE-FIND-004":[1],"P062-CODE-FIND-006":[1],"P062-CODE-FIND-007":[1],"P062-S56-SCI-Q2":[39,59],"P062-S56-SCI-Q3":[19,60],"P062-S56-SCI-Q6":[1,65],"P062-S56-SCI-Q7":[66],"P062-VIS-001":[47,48,49,50],
    }
    if finding_id == "P062-S56-CODE":
        return sorted([
            "P062-DISP-0006", "P062-DISP-0007", "P062-DISP-0010",
            "P062-DISP-0011", "P062-DISP-0014", "P062-DISP-0019",
            "P062-DISP-0021", "P062-DISP-0023", "P062-DISP-0026",
            "P062-DISP-0029", "P062-DISP-0030", "P062-DISP-0032",
            "P062-DISP-0034", "P062-DISP-0038", "P062-DISP-0042",
        ])
    return sorted(f"P062-DISP-{number:04d}" for number in direct.get(finding_id,[]))


def origin_records(inputs: dict[str, Any]) -> dict[str, tuple[str, str, dict[str, Any]]]:
    specs = ((STEP53,"findings","finding_id"),(STEP54,"findings","finding_id"),(STEP54,"ground_not_found_records","ground_not_found_id"),(STEP55_CODE,"findings","finding_id"),(STEP56,"findings","id"),(STEP56,"layout_findings","id"))
    result = {}
    for path, section, key in specs:
        for index, record in enumerate(inputs[path][section]): result[record[key]] = (path, f"/{section}/{index}", record)
    return result


def content_diagnostics(d: dict[str, Any], c: dict[str, Any], inputs: dict[str, Any], metadata: list[dict[str, Any]]) -> set[str]:
    codes: set[str] = set()
    if set(d) != DISP_TOP: codes.add("DISPOSITION_TOP_SCHEMA")
    if set(c) != CARRY_TOP: codes.add("CARRY_TOP_SCHEMA")
    if codes: return codes
    if any(set(row)!=CARRY_ROUTE_ROW for row in c["phase061_target62_routes"]): codes.add("CARRY_ROUTE_SCHEMA")
    if any(set(row)!=INHERITED_WRAPPER_ROW for row in c["inherited_carry_items"]): codes.add("INHERITED_CARRY_SCHEMA")
    if any(set(row)!=BLOCKER_WRAPPER_ROW for row in c["inherited_phase060_blockers"]): codes.add("PHASE060_BLOCKER_SCHEMA")
    if any(set(row)!=DEBT_WRAPPER_ROW for row in c["canonical_debt_routing"]): codes.add("DEBT_WRAPPER_SCHEMA")
    if any(set(row)!=P61_BLOCKER_ROW for row in c["inherited_phase061_blockers"]): codes.add("PHASE061_BLOCKER_SCHEMA")
    if any(set(component)!=COMPONENT_ROW for row in c["inherited_phase061_blockers"] for component in row["component_observations"]): codes.add("BLOCKER_COMPONENT_SCHEMA")
    if set(c["gate_summary"])!=CARRY_GATE_KEYS: codes.add("CARRY_GATE_SCHEMA")
    if set(c["generation"])!=GENERATION_KEYS: codes.add("CARRY_GENERATION_SCHEMA")
    if set(c["phase061_target62_contract"])!=TARGET62_CONTRACT_KEYS: codes.add("TARGET62_CONTRACT_SCHEMA")
    if codes:return codes
    if d.get("inputs") != metadata or c.get("inputs") != metadata: codes.add("INPUT_FINGERPRINT")
    if d.get("input_commit") != PARENT_COMMIT or c.get("input_commit") != PARENT_COMMIT: codes.add("INPUT_COMMIT")
    for document in (d, c):
        authority = document.get("authority_boundary", {})
        if any(authority.get(key) is not False for key in ("canonical_equation_promoted","external_experimental_truth","external_material_truth","external_scientific_truth","primary_literature_truth")): codes.add("EXTERNAL_PROMOTION")
    sources = inputs[TOPOLOGY]["sources"]; rows = d["release_dispositions"]
    expected_origins=origin_records(inputs)
    if len(rows) != 68: codes.add("RELEASE_COUNT")
    else:
        if any("source_id" not in row for row in rows): codes.add("SOURCE_ID_REQUIRED")
        elif [r["source_id"] for r in rows] != [f"P062-SRC-{i:04d}" for i in range(1,69)]: codes.add("RELEASE_MEMBERSHIP")
        elif any(set(row) != DISP_ROW for row in rows): codes.add("RELEASE_ROW_SCHEMA")
        else:
            for index, (row, source) in enumerate(zip(rows, sources), 1):
                projection = {key:source[key] for key in ("authority_class","blob_sha1","denominator","extent","git_mode","manifest_index","path","read_state","release_occurrence_index","review_mode","role","sha256","size_bytes","source_id")}
                if row["source_id"] != source["source_id"] or row["source_identity"] != projection or row["source_record_sha256"] != sha256(record_bytes(source)): codes.add("RELEASE_IDENTITY"); break
                expected_disclosure={
                    "corrected_disposition_authority":"FROZEN_RELEASE_TEX_INTERNAL_ONLY",
                    "frozen_source_basis":"25-line scholarly TeX closing section with statistical-thermodynamic derivation, distribution, numerical-closure and reversible-heat prose",
                    "inherited_source_authority_class":source["authority_class"],
                    "inherited_source_role":source["role"],
                    "state":"UPSTREAM_TOPOLOGY_ROLE_AUTHORITY_MISMATCH_DISCLOSED",
                } if index == 44 else None
                if row["authority_mismatch_disclosure"] != expected_disclosure: codes.add("AUTHORITY_MISMATCH_DISCLOSURE"); break
                if any(set(route) != EVIDENCE_ROUTE_ROW for route in row["evidence_routes"]): codes.add("EVIDENCE_ROUTE_SCHEMA"); break
                if row["disposition_id"] != f"P062-DISP-{index:04d}" or row["disposition"] != expected_disposition(index): codes.add("DISPOSITION_SEMANTIC"); break
                if row["primary_target_phase"] != TARGETS[index-1]: codes.add("TARGET_SEMANTIC"); break
                if row["downstream_target_phases"] != DOWNSTREAM[index-1]: codes.add("DOWNSTREAM_SEMANTIC"); break
                expected_status = "PRESERVED_ACTIVE" if row["disposition"] in {"PRESERVE","THEORY_ONLY"} else "OPEN"
                if row["status"] != expected_status: codes.add("STATUS_SEMANTIC"); break
                if row["authority_ceiling"] != expected_authority(index): codes.add("AUTHORITY_CEILING"); break
                if row["acceptance_class"] != expected_acceptance_class(index,row["disposition"]): codes.add("ACCEPTANCE_CLASS"); break
                if not row["evidence_ids"] or not row["evidence_routes"] or not row["reason"].strip() or not row["acceptance_criterion"].strip(): codes.add("RELEASE_REQUIRED_FIELD"); break
                if row["acceptance_criterion"] != expected_acceptance(index,source["source_id"],row["disposition"]): codes.add("ACCEPTANCE_SEMANTIC"); break
                if row["reason"] != expected_reason(index,source["role"],row["disposition"]): codes.add("REASON_SEMANTIC"); break
                if set(row["evidence_ids"]) != {route["evidence_id"] for route in row["evidence_routes"]}: codes.add("EVIDENCE_ID_ROUTE_BIJECTION"); break
                expected_open_routes={(path,pointer) for finding_id,(path,pointer,_record) in expected_origins.items() if expected_owner(finding_id)==("RELEASE_DISPOSITION",row["disposition_id"])}
                observed_open_routes={(route.get("artifact_path"),route.get("json_pointer")) for route in row["evidence_routes"] if route.get("route_role")=="OPEN_FINDING"}
                if observed_open_routes != expected_open_routes: codes.add("OPEN_FINDING_EVIDENCE_SET"); break
                unresolved = False
                for evidence_route in row["evidence_routes"]:
                    artifact_path = evidence_route.get("artifact_path")
                    pointer = evidence_route.get("json_pointer")
                    if artifact_path not in inputs or not isinstance(pointer, str): codes.add("EVIDENCE_ARTIFACT_PATH"); unresolved = True; break
                    try: evidence_record = resolve_pointer(inputs[artifact_path], pointer)
                    except (KeyError, IndexError, ValueError, TypeError): codes.add("EVIDENCE_POINTER_UNRESOLVED"); unresolved = True; break
                    if evidence_route.get("record_sha256") != sha256(record_bytes(evidence_record)): codes.add("EVIDENCE_RECORD_TAMPER"); unresolved = True; break
                if unresolved: break
                if index in CORRECT:
                    expected_routes = set(CORRECTION_EVIDENCE[index])
                    observed_routes = {(route.get("artifact_path"), route.get("json_pointer")) for route in row["evidence_routes"] if route.get("route_role")=="CORRECTION_SUPPORT"}
                    if observed_routes != expected_routes: codes.add("CORRECTION_EVIDENCE_SET"); break
                    if any(f"{path}#{pointer}" not in row["reason"] for path, pointer in expected_routes): codes.add("CORRECTION_REASON_BINDING"); break
                if index == 5:
                    expected_mentions = {(STEP56, f"/code_mentions/forbidden_rendered/{mention_index}") for mention_index in range(21)}
                    observed_mentions = {(route.get("artifact_path"), route.get("json_pointer")) for route in row["evidence_routes"] if route.get("route_role")=="CORRECTION_SUPPORT" and route.get("json_pointer","").startswith("/code_mentions/forbidden_rendered/")}
                    if observed_mentions != expected_mentions: codes.add("S56_CODE_MENTION_SET"); break
                if any(row[key] is not False for key in ("external_experimental_truth","external_material_truth","external_scientific_truth")): codes.add("EXTERNAL_PROMOTION"); break
            if Counter(row["disposition"] for row in rows) != EXPECTED_DISTRIBUTION: codes.add("DISPOSITION_DISTRIBUTION")
    sup = d["supplemental_process_disposition"]; expected_sup = inputs[TOPOLOGY]["supplemental_process_control"]
    if set(sup) != SUPPLEMENTAL_ROW: codes.add("SUPPLEMENTAL_SCHEMA")
    elif sup.get("denominator") != "SUPPLEMENTAL_PROCESS_CONTROL" or sup.get("manifest_member") is not False: codes.add("SUPPLEMENTAL_DENOMINATOR")
    elif sup.get("source_anchor") != {"blob_sha1":expected_sup["blob_sha1"],"path":expected_sup["path"]}: codes.add("SUPPLEMENTAL_SOURCE_ANCHOR")
    elif sup.get("source_record_sha256") != sha256(record_bytes(expected_sup)) or sup.get("source_file_sha256") != expected_sup["sha256"]: codes.add("SUPPLEMENTAL_IDENTITY_HASH")
    elif "FIRST_ORDER" in str(sup.get("authority_class", "")): codes.add("USER_TRANSCRIPT_FALSE_PRESENT")
    elif any(set(route) != EVIDENCE_ROUTE_ROW for route in sup.get("evidence_routes", [])): codes.add("SUPPLEMENTAL_ROUTE_SCHEMA")
    elif sup.get("evidence_ids") != ["P062-PROC-SUP-001"] or sup.get("evidence_routes") != [{
        "artifact_path":TOPOLOGY, "evidence_id":"P062-PROC-SUP-001",
        "json_pointer":"/supplemental_process_control",
        "record_sha256":sha256(record_bytes(expected_sup)),
        "route_role":"SUPPLEMENTAL_PROCESS_IDENTITY",
    }]: codes.add("SUPPLEMENTAL_EVIDENCE")
    elif sup.get("process_id")!="P062-PROC-SUP-001" or sup.get("disposition")!="PRESERVE" or sup.get("authority_class")!=expected_sup["authority_class"] or sup.get("primary_target_phase")!=63 or sup.get("downstream_target_phases")!=[70,82] or sup.get("status")!="PRESERVED_ACTIVE": codes.add("SUPPLEMENTAL_CONTRACT")
    elif sup.get("external_scientific_truth_validated") is not False or sup.get("external_material_truth_validated") is not False: codes.add("EXTERNAL_PROMOTION")
    release_contract_clean = not codes

    prior_routes=[r for r in inputs[P61_DISPOSITION]["dispositions"] if r["target_phase"]==62]; routes=c["phase061_target62_routes"]
    if len(routes)!=149: codes.add("TARGET62_COUNT")
    else:
        route_ids=[r.get("phase061_source_id") for r in routes]
        if route_ids != [r["source_id"] for r in prior_routes]: codes.add("TARGET62_MEMBERSHIP")
        elif any(r.get("prior_record")!=old or r.get("phase061_disposition_record_sha256")!=sha256(record_bytes(old)) for r,old in zip(routes,prior_routes)): codes.add("TARGET62_PRIOR_RECORD")
        elif any(r.get("status_before")!=old["status"] or r.get("status_after")!=old["status"] or r.get("resolution_status")!="NOT_RESOLVED" for r,old in zip(routes,prior_routes)): codes.add("TARGET62_FALSE_RESOLUTION")
        if sha256("\n".join(sorted(route_ids)).encode())!=TARGET62_SHA: codes.add("TARGET62_SET_DIGEST")
        if dict(Counter(x for row in routes for x in row.get("carry_forward_links",[])))!=EXPECTED_LINKS: codes.add("TARGET62_LINK_MULTIPLICITY")
        if [r["phase061_source_id"] for r in routes if not r["carry_forward_links"]] != ["P061-SRC-0003"]: codes.add("ZERO_LINK_SOURCE")

    for current_key,count,prior_key,id_key in (("inherited_carry_items",52,"inherited_carry_items","carry_forward_id"),("inherited_phase060_blockers",5,"inherited_phase060_blockers","blocker_id")):
        current,prior=c[current_key],inputs[P61_CARRY][prior_key]
        if len(current)!=count: codes.add("INHERITED_COUNT"); continue
        if any(row.get("prior_record")!=old or row.get("prior_record_sha256")!=sha256(record_bytes(old)) for row,old in zip(current,prior)): codes.add("INHERITED_PRIOR_RECORD")
        if any(row.get("resolution_status")!="NOT_RESOLVED" for row in current): codes.add("INHERITED_FALSE_RESOLUTION")
        if [r.get(id_key) for r in current] != [r[id_key] for r in prior]: codes.add("INHERITED_MEMBERSHIP")
    debts,prior_debts=c["canonical_debt_routing"],inputs[P61_CARRY]["debt_routing"]
    if len(debts)!=91: codes.add("DEBT_COUNT")
    elif any(row.get("prior_record")!=old or row.get("prior_record_sha256")!=sha256(record_bytes(old)) or row.get("status_after")!=old["status"] for row,old in zip(debts,prior_debts)): codes.add("DEBT_PRIOR_CONTRACT")
    else:
        group={r["prior_record"]["debt_id"]:r for r in debts if r.get("closure_group")=="P061-DISP-0044-SINGLE-CLOSURE"}; expected={"P061-GNF-004","P061-UNV-008","P061-STEP48-GNF-005","P061-STEP48-UNV-008"}
        if set(group)!=expected or group["P061-GNF-004"].get("phase062_resolution_credit")!="PRIMARY_UNRESOLVED" or any(group[x].get("phase062_resolution_credit")!="ALIAS_NO_CREDIT" for x in expected-{"P061-GNF-004"}): codes.add("DISP0044_ALIAS_GROUP")
    blockers,prior_blockers=c["inherited_phase061_blockers"],inputs[P61_CARRY]["new_blockers"]
    if len(blockers)!=5: codes.add("PHASE061_BLOCKER_COUNT")
    elif any(r.get("prior_record")!=old or r.get("prior_record_sha256")!=sha256(record_bytes(old)) for r,old in zip(blockers,prior_blockers)): codes.add("PHASE061_BLOCKER_PRIOR")
    else:
        first=blockers[0]; observed={r["component_id"]:r["status_after"] for r in first["component_observations"]}
        if observed!={"A01":"PASS","A02":"PASS","A03":"PASS","A04":"PASS","A05":"PASS","A06":"OPEN","A07":"OPEN"}: codes.add("A01_A07_COMPONENTS")
        if first.get("parent_status_after")!="OPEN" or first.get("resolution_status")!="NOT_RESOLVED" or first.get("target_phase_after")!=82: codes.add("PARTIAL_PARENT_RESOLUTION")
        if len(first["prior_record"]["source_debt_ids"])!=11: codes.add("NEW001_MEMBERSHIP")
    if c["new_phase062_blockers"]!=[]: codes.add("NEW_BLOCKER_COUNT")
    origins=origin_records(inputs); owners=c["open_finding_ownership"]
    if len(owners)!=59: codes.add("OPEN_FINDING_COUNT")
    else:
        if any(set(row) != OPEN_FINDING_OWNER_ROW for row in owners): codes.add("OPEN_FINDING_OWNER_SCHEMA")
        elif any(count > 1 for count in Counter(r.get("finding_id") for r in owners).values()): codes.add("OPEN_FINDING_MULTIPLY_OWNED")
        elif Counter(r.get("finding_id") for r in owners)!=Counter(origins.keys()): codes.add("OPEN_FINDING_OWNERLESS")
        elif any(r.get("origin_path")!=origins[r["finding_id"]][0] or r.get("origin_pointer")!=origins[r["finding_id"]][1] or r.get("origin_record_sha256")!=sha256(record_bytes(origins[r["finding_id"]][2])) for r in owners): codes.add("OPEN_FINDING_ORIGIN")
        elif any(r.get("ownership_role")!="PRIMARY_CLOSURE_OWNER" or not r.get("owner_id") for r in owners): codes.add("OPEN_FINDING_OWNER")
        else:
            disposition_by_id={row["disposition_id"]:row for row in rows}
            release_owner_surface_valid = (
                release_contract_clean
                and
                len(rows) == 68
                and [row.get("disposition_id") for row in rows] == [f"P062-DISP-{index:04d}" for index in range(1,69)]
            )
            for owner in owners:
                if not release_owner_surface_valid:
                    break
                expected_type, expected_id = expected_owner(owner["finding_id"])
                if owner.get("owner_type") == "RELEASE_DISPOSITION" and owner.get("owner_id") not in disposition_by_id:
                    codes.add("OPEN_FINDING_OWNER_EXISTENCE"); break
                if owner.get("owner_type") != expected_type or owner.get("owner_id") != expected_id:
                    codes.add("OPEN_FINDING_OWNER_MAPPING"); break
                expected_corroborating = expected_corroborating_owners(owner["finding_id"])
                if owner.get("corroborating_owner_ids") != expected_corroborating:
                    codes.add("OPEN_FINDING_CORROBORATING_SET"); break
                if expected_type == "RELEASE_DISPOSITION":
                    owner_row=disposition_by_id.get(expected_id)
                    if owner_row is None:
                        codes.add("OPEN_FINDING_OWNER_EXISTENCE"); break
                    if owner.get("owner_path") != owner_row["source_identity"]["path"] or owner.get("owner_source_id") != owner_row["source_id"]:
                        codes.add("OPEN_FINDING_OWNER_BINDING"); break
                    if any(item not in disposition_by_id for item in expected_corroborating):
                        codes.add("OPEN_FINDING_CORROBORATING_EXISTENCE"); break
                elif owner.get("owner_path") is not None or owner.get("owner_source_id") is not None:
                    codes.add("OPEN_FINDING_OWNER_BINDING"); break
    if not codes and EXPECTED_DISPOSITION_SHA!="TO_BE_PINNED" and sha256(record_bytes(rows))!=EXPECTED_DISPOSITION_SHA: codes.add("DISPOSITION_DIGEST")
    carry_projection={k:c[k] for k in ("phase061_target62_routes","inherited_carry_items","inherited_phase060_blockers","canonical_debt_routing","inherited_phase061_blockers","open_finding_ownership","new_phase062_blockers")}
    if not codes and EXPECTED_CARRY_SHA!="TO_BE_PINNED" and sha256(record_bytes(carry_projection))!=EXPECTED_CARRY_SHA: codes.add("CARRY_DIGEST")
    if not codes and sha256(canonical_bytes(d)) != EXPECTED_DISPOSITION_ARTIFACT_SHA: codes.add("DISPOSITION_CANONICAL_DIGEST")
    if not codes and sha256(canonical_bytes(c)) != EXPECTED_CARRY_ARTIFACT_SHA: codes.add("CARRY_CANONICAL_DIGEST")
    return codes


def validate_source_policy(raw: bytes | None = None) -> None:
    raw = BUILDER.read_bytes() if raw is None else raw; normalized = lf_bytes(raw)
    if EXPECTED_BUILDER_LF_SHA != "TO_BE_PINNED" and sha256(normalized) != EXPECTED_BUILDER_LF_SHA: raise ValidationError("BUILDER_DIGEST", "LF")
    tree = ast.parse(normalized.decode("utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in {"eval","exec","compile","__import__","getattr","globals","locals","vars"}: raise ValidationError("BUILDER_AST_POLICY", node.id)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            if any(name.split(".")[0] not in {"__future__","argparse","collections","hashlib","json","math","pathlib","subprocess","typing"} for name in names): raise ValidationError("BUILDER_AST_POLICY", str(names))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" and node.func.attr != "run": raise ValidationError("BUILDER_AST_POLICY", node.func.attr)
    if EXPECTED_BUILDER_AST_SHA != "TO_BE_PINNED" and sha256(canonical_ast_bytes(tree)) != EXPECTED_BUILDER_AST_SHA: raise ValidationError("BUILDER_AST_DIGEST", "AST")


def deterministic_rebuild(current: tuple[bytes, bytes, bytes]) -> None:
    validate_source_policy()
    with tempfile.TemporaryDirectory(prefix="p062_step57_validate_") as tmp:
        base = Path(tmp); observed = []
        for index in (1, 2):
            paths = (base / f"result{index}.md", base / f"disp{index}.json", base / f"carry{index}.json")
            process = subprocess.run(
                [sys.executable, str(BUILDER), "--result-output", str(paths[0]), "--disposition-output", str(paths[1]), "--carry-output", str(paths[2])],
                cwd=ROOT, capture_output=True, text=True, check=False, timeout=120,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE":"1"},
            )
            if process.returncode: raise ValidationError("REBUILD", process.stdout + process.stderr)
            observed.append(tuple(path.read_bytes() for path in paths))
        if observed[0] != observed[1]: raise ValidationError("DETERMINISM", "two runs")
        if tuple(lf_bytes(raw) for raw in observed[0]) != tuple(lf_bytes(raw) for raw in current): raise ValidationError("REBUILD", "stored mismatch")


def run_negative_controls(d: dict[str, Any], c: dict[str, Any], inputs: dict[str, Any], metadata: list[dict[str, Any]]) -> tuple[int, int]:
    controls: list[tuple[str, str, Callable[[], None]]] = [
        ("duplicate_json", "JSON_DUPLICATE", lambda: strict_load(b'{"x":1,"x":2}')),
        ("nonfinite_json", "JSON_NONFINITE", lambda: strict_load(b'{"x":NaN}')),
        ("overflow_json", "JSON_NONFINITE", lambda: strict_load(b'{"x":1e9999}')),
    ]
    base_snapshot={"upstream_name":f"origin/{ACTIVE_BRANCH}","head":PARENT_COMMIT,"upstream_tip":PARENT_COMMIT,"active_tracking":PARENT_COMMIT,"live_active":PARENT_COMMIT,"local_protected":PROTECTED_TIP,"protected_tracking":PROTECTED_TIP,"live_protected":PROTECTED_TIP,"main_tracking":MAIN_TIP,"live_main":MAIN_TIP}
    def add_boundary(name: str, code: str, field: str, value: str) -> None:
        def execute() -> None:
            snapshot=copy.deepcopy(base_snapshot);snapshot[field]=value;observed=boundary_snapshot_diagnostics(snapshot,PARENT_COMMIT)
            if observed!={code}:raise ValidationError("NEGATIVE_DIAGNOSTIC",f"{name}:{sorted(observed)}")
            raise ValidationError(code,name)
        controls.append((name,code,execute))
    add_boundary("wrong_upstream_symbolic","UPSTREAM_SYMBOLIC_NAME","upstream_name","origin/wrong")
    add_boundary("upstream_commit_drift","UPSTREAM_COMMIT_DRIFT","upstream_tip","0"*40)
    add_boundary("active_tracking_drift","ACTIVE_REMOTE_TRACKING_DRIFT","active_tracking","0"*40)
    add_boundary("protected_tracking_drift","PROTECTED_REMOTE_TRACKING_DRIFT","protected_tracking","0"*40)
    add_boundary("main_tracking_drift","MAIN_REMOTE_TRACKING_DRIFT","main_tracking","0"*40)
    def source_policy_tamper() -> None: validate_source_policy(BUILDER.read_bytes()+b"\n# tamper\n")
    controls.append(("unconditional_source_policy_tamper","BUILDER_DIGEST",source_policy_tamper))
    def add(name: str, code: str, mutate: Callable[[dict[str, Any], dict[str, Any]], None]) -> None:
        def execute() -> None:
            left, right = copy.deepcopy(d), copy.deepcopy(c); mutate(left, right)
            observed = content_diagnostics(left, right, inputs, metadata)
            if observed != {code}: raise ValidationError("NEGATIVE_DIAGNOSTIC", f"{name}:{sorted(observed)}")
            raise ValidationError(code, name)
        controls.append((name, code, execute))
    def remove_first_correction(a: dict[str, Any], _b: dict[str, Any]) -> None:
        row=a["release_dispositions"][0]
        route_index=next(i for i,route in enumerate(row["evidence_routes"]) if route["route_role"]=="CORRECTION_SUPPORT")
        evidence_id=row["evidence_routes"][route_index]["evidence_id"]
        row["evidence_routes"].pop(route_index); row["evidence_ids"].remove(evidence_id)
    def mutate_first_correction(a: dict[str, Any], key: str, value: str) -> None:
        route=next(route for route in a["release_dispositions"][0]["evidence_routes"] if route["route_role"]=="CORRECTION_SUPPORT")
        route[key]=value
    def add_extra_correction(a: dict[str, Any], _b: dict[str, Any]) -> None:
        source=next(route for route in a["release_dispositions"][1]["evidence_routes"] if route["route_role"]=="CORRECTION_SUPPORT")
        extra=copy.deepcopy(source); extra["evidence_id"]="P062-CORRECTION-EXTRA"
        a["release_dispositions"][0]["evidence_routes"].append(extra); a["release_dispositions"][0]["evidence_ids"].append(extra["evidence_id"])
    def wrong_cross_row_correction(a: dict[str, Any], _b: dict[str, Any]) -> None:
        route=next(route for route in a["release_dispositions"][0]["evidence_routes"] if route["route_role"]=="CORRECTION_SUPPORT")
        path,pointer=CORRECTION_EVIDENCE[2][0]; route["artifact_path"]=path; route["json_pointer"]=pointer; route["record_sha256"]=sha256(record_bytes(resolve_pointer(inputs[path],pointer)))
    add("missing_release", "RELEASE_COUNT", lambda a,b: a["release_dispositions"].pop())
    add("duplicate_release", "RELEASE_MEMBERSHIP", lambda a,b: a["release_dispositions"].__setitem__(-1, copy.deepcopy(a["release_dispositions"][0])))
    add("disposition_swap", "DISPOSITION_SEMANTIC", lambda a,b: (
        a["release_dispositions"][0].__setitem__("disposition", "PRESERVE"),
        a["release_dispositions"][8].__setitem__("disposition", "CORRECT"),
    ))
    add("target_swap", "TARGET_SEMANTIC", lambda a,b: a["release_dispositions"][0].__setitem__("primary_target_phase", 63))
    add("source_identity", "RELEASE_IDENTITY", lambda a,b: a["release_dispositions"][0]["source_identity"].__setitem__("path", "wrong"))
    add("missing_top_source_id", "SOURCE_ID_REQUIRED", lambda a,b: a["release_dispositions"][0].pop("source_id"))
    add("downstream_collapse", "DOWNSTREAM_SEMANTIC", lambda a,b: a["release_dispositions"][0].__setitem__("downstream_target_phases", [84,87,90]))
    theory_index=next(i for i,row in enumerate(d["release_dispositions"]) if row["disposition"]=="THEORY_ONLY")
    add("theory_only_open", "STATUS_SEMANTIC", lambda a,b: a["release_dispositions"][theory_index].__setitem__("status", "OPEN"))
    unverified_index=next(i for i,row in enumerate(d["release_dispositions"]) if row["disposition"]=="UNVERIFIED")
    add("generic_unverified_phase71", "ACCEPTANCE_SEMANTIC", lambda a,b: a["release_dispositions"][unverified_index].__setitem__("acceptance_criterion", "Phase 71 generic acceptance"))
    add("correction_evidence_missing", "CORRECTION_EVIDENCE_SET", remove_first_correction)
    add("correction_evidence_extra", "CORRECTION_EVIDENCE_SET", add_extra_correction)
    add("correction_evidence_wrong_cross_row", "CORRECTION_EVIDENCE_SET", wrong_cross_row_correction)
    add("correction_evidence_hash", "EVIDENCE_RECORD_TAMPER", lambda a,b: mutate_first_correction(a,"record_sha256","0"*64))
    add("correction_evidence_pointer", "EVIDENCE_POINTER_UNRESOLVED", lambda a,b: mutate_first_correction(a,"json_pointer","/missing"))
    add("external_promotion", "EXTERNAL_PROMOTION", lambda a,b: a["release_dispositions"][0].__setitem__("external_scientific_truth", True))
    add("bibliography_authority_swap", "AUTHORITY_CEILING", lambda a,b: a["release_dispositions"][7].__setitem__("authority_ceiling", "PROCESS_OR_SNAPSHOT_SELF_REPORT_ONLY"))
    add("process_authority_swap", "AUTHORITY_CEILING", lambda a,b: a["release_dispositions"][2].__setitem__("authority_ceiling", "BIBLIOGRAPHIC_METADATA_NAVIGATION_ONLY"))
    add("structure_authority_swap", "AUTHORITY_CEILING", lambda a,b: a["release_dispositions"][66].__setitem__("authority_ceiling", "FROZEN_RELEASE_TEX_INTERNAL_ONLY"))
    add("ch2_closing_process_reversion", "AUTHORITY_CEILING", lambda a,b: a["release_dispositions"][43].__setitem__("authority_ceiling", "PROCESS_OR_SNAPSHOT_SELF_REPORT_ONLY"))
    add("ch2_closing_disclosure_omission", "AUTHORITY_MISMATCH_DISCLOSURE", lambda a,b: a["release_dispositions"][43].__setitem__("authority_mismatch_disclosure", None))
    add("acceptance_class_swap", "ACCEPTANCE_CLASS", lambda a,b: a["release_dispositions"][0].__setitem__("acceptance_class", "FIX_DOC"))
    add("acceptance_generic_collapse", "ACCEPTANCE_SEMANTIC", lambda a,b: a["release_dispositions"][0].__setitem__("acceptance_criterion", "Phase 83 generic acceptance"))
    add("supplemental_fusion", "SUPPLEMENTAL_DENOMINATOR", lambda a,b: a["supplemental_process_disposition"].__setitem__("manifest_member", True))
    add("supplemental_schema", "SUPPLEMENTAL_SCHEMA", lambda a,b: a["supplemental_process_disposition"].__setitem__("external_access_validated", a["supplemental_process_disposition"].pop("external_material_truth_validated")))
    add("supplemental_denominator", "SUPPLEMENTAL_DENOMINATOR", lambda a,b: a["supplemental_process_disposition"].__setitem__("denominator", "RELEASE_SOURCE"))
    add("supplemental_source_anchor", "SUPPLEMENTAL_SOURCE_ANCHOR", lambda a,b: a["supplemental_process_disposition"]["source_anchor"].__setitem__("path", "wrong"))
    add("supplemental_evidence_pointer", "SUPPLEMENTAL_EVIDENCE", lambda a,b: a["supplemental_process_disposition"]["evidence_routes"][0].__setitem__("json_pointer", "/sources/0"))
    add("transcript_promotion", "USER_TRANSCRIPT_FALSE_PRESENT", lambda a,b: a["supplemental_process_disposition"].__setitem__("authority_class", "FIRST_ORDER_USER_TRANSCRIPT_PRESENT"))
    add("missing_target62", "TARGET62_COUNT", lambda a,b: b["phase061_target62_routes"].pop())
    add("target62_prior", "TARGET62_PRIOR_RECORD", lambda a,b: b["phase061_target62_routes"][0]["prior_record"].__setitem__("status", "RESOLVED"))
    add("target62_resolution", "TARGET62_FALSE_RESOLUTION", lambda a,b: b["phase061_target62_routes"][0].__setitem__("resolution_status", "RESOLVED"))
    add("carry_route_extra_key", "CARRY_ROUTE_SCHEMA", lambda a,b: b["phase061_target62_routes"][0].__setitem__("extra",0))
    add("link_multiplicity", "TARGET62_LINK_MULTIPLICITY", lambda a,b: b["phase061_target62_routes"][1]["carry_forward_links"].pop())
    zero_index = next(i for i,row in enumerate(c["phase061_target62_routes"]) if row["phase061_source_id"] == "P061-SRC-0003")
    donor_index = next(i for i,row in enumerate(c["phase061_target62_routes"]) if len(row["carry_forward_links"]) > 1)
    donor_link = c["phase061_target62_routes"][donor_index]["carry_forward_links"][0]
    add("zero_link", "ZERO_LINK_SOURCE", lambda a,b: (
        b["phase061_target62_routes"][zero_index]["carry_forward_links"].append(donor_link),
        b["phase061_target62_routes"][donor_index]["carry_forward_links"].remove(donor_link),
    ))
    add("missing_carry", "INHERITED_COUNT", lambda a,b: b["inherited_carry_items"].pop())
    add("carry_prior", "INHERITED_PRIOR_RECORD", lambda a,b: b["inherited_carry_items"][0]["prior_record"].__setitem__("status_after", "RESOLVED"))
    add("carry_resolution", "INHERITED_FALSE_RESOLUTION", lambda a,b: b["inherited_carry_items"][0].__setitem__("resolution_status", "RESOLVED"))
    add("inherited_carry_missing_key", "INHERITED_CARRY_SCHEMA", lambda a,b: b["inherited_carry_items"][0].pop("delta_status"))
    add("phase060_blocker_extra_key", "PHASE060_BLOCKER_SCHEMA", lambda a,b: b["inherited_phase060_blockers"][0].__setitem__("extra",0))
    add("missing_debt", "DEBT_COUNT", lambda a,b: b["canonical_debt_routing"].pop())
    add("debt_prior", "DEBT_PRIOR_CONTRACT", lambda a,b: b["canonical_debt_routing"][0]["prior_record"].__setitem__("owner_target_phase", 90))
    add("debt_wrapper_extra_key", "DEBT_WRAPPER_SCHEMA", lambda a,b: b["canonical_debt_routing"][0].__setitem__("extra",0))
    alias_index = next(i for i,row in enumerate(c["canonical_debt_routing"]) if row["prior_record"]["debt_id"] == "P061-UNV-008")
    add("alias_credit", "DISP0044_ALIAS_GROUP", lambda a,b: b["canonical_debt_routing"][alias_index].__setitem__("phase062_resolution_credit", "PRIMARY_UNRESOLVED"))
    add("blocker_count", "PHASE061_BLOCKER_COUNT", lambda a,b: b["inherited_phase061_blockers"].pop())
    add("phase061_blocker_extra_key", "PHASE061_BLOCKER_SCHEMA", lambda a,b: b["inherited_phase061_blockers"][0].__setitem__("extra",0))
    add("component_extra_key", "BLOCKER_COMPONENT_SCHEMA", lambda a,b: b["inherited_phase061_blockers"][0]["component_observations"][0].__setitem__("extra",0))
    add("component_false_open", "A01_A07_COMPONENTS", lambda a,b: b["inherited_phase061_blockers"][0]["component_observations"][0].__setitem__("status_after", "OPEN"))
    add("partial_parent", "PARTIAL_PARENT_RESOLUTION", lambda a,b: b["inherited_phase061_blockers"][0].__setitem__("parent_status_after", "RESOLVED"))
    add("new_blocker", "NEW_BLOCKER_COUNT", lambda a,b: b["new_phase062_blockers"].append({"id":"P062-BD-NEW-001"}))
    add("missing_owner", "OPEN_FINDING_COUNT", lambda a,b: b["open_finding_ownership"].pop())
    add("owner_origin", "OPEN_FINDING_ORIGIN", lambda a,b: b["open_finding_ownership"][0].__setitem__("origin_record_sha256", "0"*64))
    add("owner_blank", "OPEN_FINDING_OWNER", lambda a,b: b["open_finding_ownership"][0].__setitem__("owner_id", ""))
    q2_owner_index=next(i for i,row in enumerate(c["open_finding_ownership"]) if row["finding_id"]=="P062-S53-F002")
    add("q2_wrong_owner", "OPEN_FINDING_OWNER_MAPPING", lambda a,b: b["open_finding_ownership"][q2_owner_index].__setitem__("owner_id", "P062-DISP-0016"))
    add("nonexistent_owner", "OPEN_FINDING_OWNER_EXISTENCE", lambda a,b: b["open_finding_ownership"][q2_owner_index].__setitem__("owner_id", "P062-DISP-9999"))
    add("ownerless_finding", "OPEN_FINDING_OWNERLESS", lambda a,b: b["open_finding_ownership"][0].__setitem__("finding_id", "P062-UNKNOWN"))
    add("multiply_owned_finding", "OPEN_FINDING_MULTIPLY_OWNED", lambda a,b: b["open_finding_ownership"][-1].__setitem__("finding_id", b["open_finding_ownership"][0]["finding_id"]))
    s56_code_index=next(i for i,row in enumerate(c["open_finding_ownership"]) if row["finding_id"]=="P062-S56-CODE")
    add("corroborating_owner_set", "OPEN_FINDING_CORROBORATING_SET", lambda a,b: b["open_finding_ownership"][s56_code_index]["corroborating_owner_ids"].pop())
    s53_f001_index=next(i for i,row in enumerate(c["open_finding_ownership"]) if row["finding_id"]=="P062-S53-F001")
    add("ordinary_corroborating_omission", "OPEN_FINDING_CORROBORATING_SET", lambda a,b: b["open_finding_ownership"][s53_f001_index]["corroborating_owner_ids"].clear())
    vis_index=next(i for i,row in enumerate(c["open_finding_ownership"]) if row["finding_id"]=="P062-VIS-001")
    add("ordinary_corroborating_addition", "OPEN_FINDING_CORROBORATING_SET", lambda a,b: b["open_finding_ownership"][vis_index]["corroborating_owner_ids"].append("P062-DISP-0051"))
    add("disposition_unvalidated_scalar", "DISPOSITION_CANONICAL_DIGEST", lambda a,b: a["gate_summary"].__setitem__("status", "PASS"))
    add("carry_unvalidated_scalar", "CARRY_CANONICAL_DIGEST", lambda a,b: b["generation"].__setitem__("deterministic", False))
    add("carry_gate_extra_key", "CARRY_GATE_SCHEMA", lambda a,b: b["gate_summary"].__setitem__("extra",0))
    add("generation_extra_key", "CARRY_GENERATION_SCHEMA", lambda a,b: b["generation"].__setitem__("extra",0))
    add("target62_contract_extra_key", "TARGET62_CONTRACT_SCHEMA", lambda a,b: b["phase061_target62_contract"].__setitem__("extra",0))
    passed = 0
    for name, expected, control in controls:
        try: control()
        except ValidationError as error:
            if error.code != expected: raise ValidationError("NEGATIVE_DIAGNOSTIC", f"{name}: expected {expected}, got {error.code}")
            passed += 1
        else: raise ValidationError("NEGATIVE_ACCEPTED", name)
    return passed, len(controls)


def validate_result_and_controls(disposition_raw: bytes, carry_raw: bytes) -> None:
    for path, expected_sha in CONTROL_LF_SHA.items():
        if sha256(lf_bytes(path.read_bytes())) != expected_sha:
            raise ValidationError("CONTROL_DOCUMENT_DIGEST", path.name)
    text = RESULT.read_text(encoding="utf-8")
    if re.findall(r"(?m)^Gate: `([^`]+)`$", text) != ["PASS_P062_STEP57_1_DISPOSITIONS"]: raise ValidationError("RESULT_GATE", "gate")
    for token in ("Status: `PASS_WITH_CONCERNS`", "Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`", "RESULT_WRITTEN_BEFORE_DISPOSITION_AND_CARRY_JSON", sha256(lf_bytes(disposition_raw)), sha256(lf_bytes(carry_raw)), "149/149", "52 + 5 + 91 + 5", "A06/A07 `OPEN`"):
        if token not in text: raise ValidationError("RESULT_CONTRACT", token)
    for path in (PARENT_LEDGER, ACTIVE_LEDGER, HANDOVER):
        value = path.read_text(encoding="utf-8")
        if "PASS_P062_STEP56_PERSISTENCE" not in value or "PASS_P062_STEP57_1_DISPOSITIONS" not in value or "Step 57.2" not in value: raise ValidationError("CONTROL_DOCUMENT", path.name)
        if re.search(r"(?:FAIL|CONDITIONAL)_P062_STEP57_1_DISPOSITIONS", value): raise ValidationError("CONTROL_CONTRADICTION", path.name)


def nul_set(raw: bytes) -> set[str]: return {x.decode("utf-8").replace("\\", "/") for x in raw.split(b"\0") if x}


def live_tip(branch: str) -> str:
    out = git_text(["ls-remote", "--heads", "origin", f"refs/heads/{branch}"])
    if not out: raise ValidationError("REMOTE_TIP", branch)
    return out.split()[0]


def boundary_snapshot(expected_active: str) -> dict[str,str]:
    return {"upstream_name":git_text(["rev-parse","--abbrev-ref","--symbolic-full-name","@{upstream}"]),"head":git_text(["rev-parse","HEAD"]),"upstream_tip":git_text(["rev-parse","@{upstream}"]),"active_tracking":git_text(["rev-parse",f"refs/remotes/origin/{ACTIVE_BRANCH}"]),"live_active":live_tip(ACTIVE_BRANCH),"local_protected":git_text(["rev-parse",f"refs/heads/{PROTECTED_BRANCH}"]),"protected_tracking":git_text(["rev-parse",f"refs/remotes/origin/{PROTECTED_BRANCH}"]),"live_protected":live_tip(PROTECTED_BRANCH),"main_tracking":git_text(["rev-parse","refs/remotes/origin/main"]),"live_main":live_tip("main")}


def boundary_snapshot_diagnostics(s: dict[str,str], expected_active: str) -> set[str]:
    if s["upstream_name"] != f"origin/{ACTIVE_BRANCH}": return {"UPSTREAM_SYMBOLIC_NAME"}
    if s["head"] != expected_active: return {"PERSISTENCE_HEAD"}
    if s["upstream_tip"] != expected_active: return {"UPSTREAM_COMMIT_DRIFT"}
    if s["active_tracking"] != expected_active: return {"ACTIVE_REMOTE_TRACKING_DRIFT"}
    if s["live_active"] != expected_active: return {"ACTIVE_REMOTE_DIVERGENCE"}
    if s["local_protected"] != PROTECTED_TIP: return {"LOCAL_PROTECTED_DRIFT"}
    if s["protected_tracking"] != PROTECTED_TIP: return {"PROTECTED_REMOTE_TRACKING_DRIFT"}
    if s["live_protected"] != PROTECTED_TIP: return {"PROTECTED_DRIFT"}
    if s["main_tracking"] != MAIN_TIP: return {"MAIN_REMOTE_TRACKING_DRIFT"}
    if s["live_main"] != MAIN_TIP: return {"MAIN_DRIFT"}
    return set()


def validate_live_boundaries(active_tip: str) -> None:
    diagnostics=boundary_snapshot_diagnostics(boundary_snapshot(active_tip),active_tip)
    if diagnostics: raise ValidationError(next(iter(diagnostics)),active_tip)
    if git_text(["diff", "--name-only", SOURCE_COMMIT, "--", "Claude"]): raise ValidationError("CLAUDE_DRIFT", "tracked")


def validate_precommit() -> None:
    if git_text(["branch", "--show-current"]) != ACTIVE_BRANCH: raise ValidationError("ACTIVE_BRANCH", "precommit")
    validate_live_boundaries(PARENT_COMMIT)
    staged = nul_set(git_bytes(["diff", "--cached", "--name-only", "-z"])); unstaged = nul_set(git_bytes(["diff", "--name-only", "-z"])); untracked = nul_set(git_bytes(["ls-files", "--others", "--exclude-standard", "-z"]))
    if staged != EXPECTED_PATHS: raise ValidationError("EXACT_STAGED_SET", str(sorted(staged)))
    if unstaged: raise ValidationError("UNSTAGED_TRACKED", str(sorted(unstaged)))
    if untracked: raise ValidationError("EXTRA_UNTRACKED", str(sorted(untracked)))
    for path in EXPECTED_PATHS:
        if git_bytes(["show", f":{path}"]) != (ROOT / path).read_bytes(): raise ValidationError("STAGED_WORKTREE_MISMATCH", path)
    git_bytes(["diff", "--cached", "--check"])


def validate_persistence(commit: str) -> None:
    if git_text(["branch", "--show-current"]) != ACTIVE_BRANCH: raise ValidationError("ACTIVE_BRANCH", "persistence")
    validate_live_boundaries(commit)
    if git_text(["show", "-s", "--format=%s", commit]) != SUBJECT: raise ValidationError("PERSISTENCE_SUBJECT", commit)
    if git_text(["rev-parse", f"{commit}^"]) != PARENT_COMMIT: raise ValidationError("PERSISTENCE_PARENT", commit)
    changed = set(git_text(["diff-tree", "--no-commit-id", "--name-only", "-r", commit]).splitlines())
    if changed != EXPECTED_PATHS: raise ValidationError("PERSISTENCE_PATHS", str(sorted(changed)))
    if git_text(["status", "--porcelain=v1", "--untracked-files=all"]): raise ValidationError("DIRTY_AFTER_COMMIT", "status")


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--mode", choices=("artifact","precommit","persistence"), default="artifact"); parser.add_argument("--expected-commit"); parser.add_argument("--run-negative-probes", action="store_true"); parser.add_argument("--determinism-check", action="store_true"); args = parser.parse_args()
    try:
        validate_source_policy()
        if not DISPOSITION.is_file() or not CARRY.is_file() or not RESULT.is_file(): raise ValidationError("ARTIFACT_MISSING", "Step57.1")
        disposition_raw, carry_raw = DISPOSITION.read_bytes(), CARRY.read_bytes(); disposition, carry = strict_load(disposition_raw), strict_load(carry_raw)
        if canonical_bytes(disposition) != lf_bytes(disposition_raw) or canonical_bytes(carry) != lf_bytes(carry_raw): raise ValidationError("CANONICAL_JSON", "stored")
        inputs, metadata = load_inputs(); diagnostics = content_diagnostics(disposition, carry, inputs, metadata)
        if diagnostics: raise ValidationError("CONTENT_DIAGNOSTICS", str(sorted(diagnostics)))
        validate_result_and_controls(disposition_raw, carry_raw)
        run_negative = args.run_negative_probes or args.mode in {"precommit","persistence"}; run_determinism = args.determinism_check or args.mode in {"precommit","persistence"}
        negative = run_negative_controls(disposition, carry, inputs, metadata) if run_negative else (0,0)
        if run_determinism: deterministic_rebuild((RESULT.read_bytes(), disposition_raw, carry_raw))
        if run_negative: print(f"PASS negative_controls={negative[0]}/{negative[1]}")
        if run_determinism: print("PASS determinism=2/2 production_imported_or_executed=false")
        if args.mode == "precommit": validate_precommit()
        elif args.mode == "persistence":
            if not args.expected_commit: raise ValidationError("EXPECTED_COMMIT", "required")
            validate_persistence(args.expected_commit)
    except (ValidationError, ValueError, KeyError, TypeError, OSError, UnicodeDecodeError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        print(f"FAIL {error}"); print("FAIL_P062_STEP57_1_DISPOSITIONS"); return 1
    print("PASS release=68 supplemental=1 distribution=30/16/13/9")
    print("PASS target62=149 links=253 carry=52 p060_blockers=5 debts=91 p061_blockers=5 new=0")
    print("PASS open_findings=59 ownerless=0 multiply_owned=0 A01-A05=PASS A06-A07-parent=OPEN")
    print("PASS_P062_STEP57_1_PERSISTENCE" if args.mode == "persistence" else "PASS_P062_STEP57_1_DISPOSITIONS")
    return 0


if __name__ == "__main__": raise SystemExit(main())
