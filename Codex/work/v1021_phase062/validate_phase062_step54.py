#!/usr/bin/env python3
"""Fail-closed validator for Phase 062 Step 54 LCO/Si scope evidence."""

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
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json"
RESULT = ROOT / "Codex/results/PHASE_062_STEP_054_LCO_SI_SCOPE_RESULT.md"
BUILDER = ROOT / "Codex/work/v1021_phase062/build_phase062_step54_lco_si_scope.py"
PARENT_LEDGER = ROOT / "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER = ROOT / "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER = ROOT / "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
EXPECTED_PARENT = "9dee2f4d6bdde48f248227cdede08d0d307cc8bc"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
SUBJECT = "audit(phase062): bound v1021 lco si scope"
EXPECTED_BUILDER_SHA256 = "57162f0431b593be004b0dcf50caf1eafa2d65d6b5d42d9355e4d1ebc9007427"
EXPECTED_GNF_SHA256 = "4ce493ec65baabea417f133ee8187f8008944d71e943a37124d0e6502c26fd07"
EXPECTED_NAVIGATION_SHA256 = "bb816bedae6796fec47d3607c75b17bc5c1baab28a8fd00f21a470c11cf4fb6f"
EXPECTED_BIBLIOGRAPHY_ROWS_SHA256 = "5c12b8c834dce8d3fe0bf38c2498aa98684fa1713101699a57b0f203cd000c77"
EXPECTED_METADATA_ROWS_SHA256 = "7e409ddbe4d38f3a1b56993ea73980ac8db27a9cc86f2df465fc07f5f1574bbc"
EXPECTED_CITATION_ROWS_SHA256 = "941cc91257ad12961d288893ce941e8ae9d7590451239a9322654679a32d843b"
EXPECTED_SOURCE_ATTESTATIONS_SHA256 = "8ae951b7d6ab0e9752b215509ac628441a71371cfde5734f1440c538058d411d"

EXACT_PATHS = {
    "Codex/work/v1021_phase062/build_phase062_step54_lco_si_scope.py",
    "Codex/work/v1021_phase062/validate_phase062_step54.py",
    "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json",
    "Codex/results/PHASE_062_STEP_054_LCO_SI_SCOPE_RESULT.md",
    "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md",
    "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md",
    "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md",
}
LCO_KEYS = {
    "reimers1992", "vanderven1998", "mott1968", "imada1998", "marianetti2004",
    "menetrier1999", "motohashi2009", "xia2007", "reynier2004", "swiderska2019",
    "msmr_origin2017", "bakerverbrugge2018", "msmr2024", "ml2024",
}
SI_KEYS = {
    "wen_huggins1981", "limthongkul2003", "li_dahn2007", "obrovac_christensen2004",
    "chevrier_dahn2009", "beaulieu2001", "sethuraman_stressevo2010",
    "sethuraman_stresspot2010", "liu_sizefracture2012", "obrovac_chevrier2014",
    "verbrugge_lisi2016", "jiang_sihys2020", "larchecahn1973", "koebbing2024",
}
LCO_CITE_KEYS = LCO_KEYS | {"ashcroftmermin1976"}
REQUIRED_CONTRADICTIONS = {
    "P062-LCO-C01", "P062-LCO-C02", "P062-LCO-C03", "P062-SI-C01",
    "P062-SI-C02", "P062-SI-C03", "P062-SI-C04", "P062-SI-C05",
}
REQUIRED_MISSING_SI = {
    "SI_SPECIFIC_FREE_ENERGY", "STRESS_CHEMICAL_POTENTIAL", "PLASTICITY_DAMAGE",
    "INTERFACE_SEI", "HYSTERESIS_EVOLUTION", "SIOX_ALLOCATION", "SIC_ALLOCATION",
    "BLEND_ALLOCATION",
}
ALLOWED_EVIDENCE_TIERS = {
    "INTERNAL_DERIVATION", "INTERNAL_GNF", "INTERNAL_RELEASE_CLAIM", "METADATA",
    "PRIMARY_FULLTEXT", "PUBLISHER", "TIER_C_MODEL", "INTERNAL_MODEL_ASSUMPTION",
    "SOURCE_STATED_TIER_A_UNVERIFIED", "SOURCE_STATED_TIER_B_UNVERIFIED",
    "SOURCE_TIER_TAXONOMY", "LEDGER_SELF_REPORT",
}
ALLOWED_STATES = {
    "EXACT_INTERNAL_SOURCE_MATCH", "PARTIAL", "CONFLICTING", "UNVERIFIED_EXTERNAL",
    "REJECTED",
}
NEGATIVE_IDS = [
    "BIBLIOGRAPHY_AS_PROPOSITION_PROOF", "WEB_METADATA_AS_FULLTEXT",
    "UNIT_BASIS_COLLAPSE", "TIER_C_TO_MATERIAL_PROMOTION",
    "PURE_LCO_TO_DOPED_LCO_PROMOTION", "SI_BRIDGEHEAD_TO_COMPLETE_MODEL",
    "MISSING_SCOPE_ROUTING", "EXTERNAL_AUTHORITY_PROMOTION", "STATUS_PROMOTION",
    "METADATA_IDENTITY_TAMPER", "CITATION_DENOMINATOR_TAMPER", "Q6_NUMERIC_TAMPER",
    "Q7_LABEL_DELTA_TAMPER", "GNF_ORPHAN", "ANCHOR_SLICE_HASH_TAMPER",
    "SEMANTIC_DIGEST_TAMPER", "RESULT_FIRST_CONTRACT_TAMPER",
    "SOURCE_CLAIM_MANIFEST_MISSING", "SOURCE_CLAIM_MULTI_MAPPED",
    "STRUCTURAL_AS_CLAIM", "TIKZ_LOAD_BEARING_OMISSION", "MULTILINE_CLAIM_SPLIT",
    "A_OR_B_TIER_TO_C", "UNIT_DELETION", "CITEKEY_NUMERIC_LEAK",
    "BIBLIOGRAPHY_IDENTITY_TAMPER", "PROVENANCE_IDENTITY_TAMPER",
    "SOURCE_ATTESTATION_SCHEMA_TAMPER",
]

EXPECTED_PROVENANCE = {
    "baseline_commit": BASELINE,
    "q6_commit": "bab65b7290204ec5d64b1c2bbdfb4b30d4c8fd17",
    "q6_parent": "7316e7915db8727f794614b61f98d4df7f803bfd",
    "q7_commit": "9ea5cb23754061261923bab013e279d7f6938723",
    "q7_parent": "bab65b7290204ec5d64b1c2bbdfb4b30d4c8fd17",
    "expected_parent": EXPECTED_PARENT,
    "external_observation_date": "2026-08-27",
    "frozen_source_modified": False,
    "production_module_imported_or_executed": False,
}

CLAIM_TEXT_PATHS = [
    "Claude/docs/v1.0.21/_sections/ch1_sec11_lcointro.tex",
    "Claude/docs/v1.0.21/_sections/ch1_sec12_lcocenter.tex",
    "Claude/docs/v1.0.21/_sections/ch1_sec13_lcohys.tex",
    "Claude/docs/v1.0.21/_sections/ch1_sec14_lcodecomp.tex",
    "Claude/docs/v1.0.21/_sections/ch1_sec15_lcoelec.tex",
    "Claude/docs/v1.0.21/_sections/ch1_sec16_lcopeak.tex",
    "Claude/docs/v1.0.21/_sections/ch1_sec17_msmr.tex",
    "Claude/docs/v1.0.21/_sections/ch1_sec18_inputs.tex",
    "Claude/docs/v1.0.21/_sections/ch1_appA_signcheck.tex",
    "Claude/docs/v1.0.21/_sections/ch1_appD_si.tex",
]
BIBLIOGRAPHY_PATH = "Claude/docs/v1.0.21/_sections/ch1_bib.tex"
REFERENCE_LEDGER_PATH = "Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md"
REFERENCE_LEDGER_CLAIM_LINES = [3, 4, 7, 8, 9, 18, 19, 25, 26, 32, 33, 34, 35, 36, 37]
GNF_OWNER_ANCHORS = {
    "P062-GNF-001": (CLAIM_TEXT_PATHS[4], 176), "P062-GNF-002": (CLAIM_TEXT_PATHS[4], 305),
    "P062-GNF-003": (CLAIM_TEXT_PATHS[2], 172), "P062-GNF-004": (CLAIM_TEXT_PATHS[9], 73),
    "P062-GNF-005": (CLAIM_TEXT_PATHS[9], 70), "P062-GNF-006": (CLAIM_TEXT_PATHS[9], 71),
    "P062-GNF-007": (CLAIM_TEXT_PATHS[9], 72), "P062-GNF-008": (CLAIM_TEXT_PATHS[9], 85),
    "P062-GNF-009": (CLAIM_TEXT_PATHS[9], 85), "P062-GNF-010": (CLAIM_TEXT_PATHS[9], 86),
    "P062-GNF-011": (CLAIM_TEXT_PATHS[4], 165), "P062-GNF-012": (CLAIM_TEXT_PATHS[4], 166),
    "P062-GNF-013": (CLAIM_TEXT_PATHS[9], 17), "P062-GNF-014": (CLAIM_TEXT_PATHS[9], 18),
    "P062-GNF-015": (CLAIM_TEXT_PATHS[9], 20), "P062-GNF-016": (CLAIM_TEXT_PATHS[9], 41),
    "P062-GNF-017": (CLAIM_TEXT_PATHS[9], 47),
}

# Validator-owned golden inventory.  These digests cover every nested field of
# every claim/scope row, while the checks below independently re-open every Git
# anchor and enforce the known TeX/TikZ/tier/unit boundaries.  The builder is
# never imported and its proposition assembler is not copied here.
GOLDEN_CLAIM_COUNTS = {
    CLAIM_TEXT_PATHS[0]: 66, CLAIM_TEXT_PATHS[1]: 32, CLAIM_TEXT_PATHS[2]: 45,
    CLAIM_TEXT_PATHS[3]: 29, CLAIM_TEXT_PATHS[4]: 109, CLAIM_TEXT_PATHS[5]: 17,
    CLAIM_TEXT_PATHS[6]: 38, CLAIM_TEXT_PATHS[7]: 38, CLAIM_TEXT_PATHS[8]: 28,
    CLAIM_TEXT_PATHS[9]: 37, BIBLIOGRAPHY_PATH: 28, REFERENCE_LEDGER_PATH: 15,
}
GOLDEN_CLAIM_DIGESTS = {
    CLAIM_TEXT_PATHS[0]: "3a7e18348321e135b955f4b54df3b87f8ff7c59a8a6ce771261b4317799703ea",
    CLAIM_TEXT_PATHS[1]: "bf2c09bee45322ce435014ef60f330e29b78da779f254c26e37774f7379bc71f",
    CLAIM_TEXT_PATHS[2]: "b1b4afdf579882813c5d8630737f088f04e9c363a75cb8dc1f04b06c7b3ba3d8",
    CLAIM_TEXT_PATHS[3]: "32662e719eb2cf383f5ac8eaa9517c5b351337bf4d02ff57cf5c693ee196eb7c",
    CLAIM_TEXT_PATHS[4]: "e05a8df3041d4ab61d75301c2d8acfaddf33dfa37ed166297dd0a58b111d1e1a",
    CLAIM_TEXT_PATHS[5]: "be2bea69129574495cd89a5db5383467873a0d63c87ee24d36bad8c5e5de519a",
    CLAIM_TEXT_PATHS[6]: "9bd513cb072985ceb4da2e7216d155a02a25224275c13bafa99a67f78704dc72",
    CLAIM_TEXT_PATHS[7]: "454379ff18d4b6803b9284eb9eb2b45996ec11ff783a47113a414136c936e116",
    CLAIM_TEXT_PATHS[8]: "032a48f566018d85f9fa3603604c3ed873595fc53cca503605517bca873c8f55",
    CLAIM_TEXT_PATHS[9]: "a41e67842158891e5be728d3ed8715a3b0908d4e622ef5a948949de5fa52aea0",
    BIBLIOGRAPHY_PATH: "398ecf2abe94a99b60958f9ff3a0b567de5537745aadb4f8703f73a16c0accfe",
    REFERENCE_LEDGER_PATH: "4cf52b5b2a1d7b02ec7fe097055f8da60f46c0d27d5ba93bffe5e8f0645dd0e2",
}
GOLDEN_SCOPE_DIGESTS = {
    CLAIM_TEXT_PATHS[0]: "cb4d5d15ef706319a2cdbca43f6ce59ec9f8a0735466986125736dbea9147a2b",
    CLAIM_TEXT_PATHS[1]: "6555f8af2ea3146a37e19498dc38910e0bbf5cbdf7bbb5dcfef180bdc75f9a26",
    CLAIM_TEXT_PATHS[2]: "e6fe9c9aec9441435de2febd77a88eef17b243f3c0eee5b713f0c9307ef31a9d",
    CLAIM_TEXT_PATHS[3]: "d32039e35e44509b706ad11f018755f41a2c76184fe0b3bb91d9a25e56eb3667",
    CLAIM_TEXT_PATHS[4]: "7c71d52c53c8227db19098cbe5043016139384e2391091b5f3c2b570c4b477c1",
    CLAIM_TEXT_PATHS[5]: "dd8e63cf0c0ece070b1e4fd0175b781d448d3ee34a310cfa669a2cb3f2e26910",
    CLAIM_TEXT_PATHS[6]: "55b32102aa1eb775f9f26a70fc36c88a334dfa68b6a0b1df664ccd471121e0f2",
    CLAIM_TEXT_PATHS[7]: "40ff78238543bc05566e4b2b38912f605faaba8b8bb23e3ab7faad1ecccb040f",
    CLAIM_TEXT_PATHS[8]: "9d8c8af9ebc8d37134df842502d95d3fe01200c7b9f207c62e38f7f0d47cf61b",
    CLAIM_TEXT_PATHS[9]: "470e21ed1d19996ddeaf4ebe8616ea7b3aaff6b1c4d08836abd2f88787be7e77",
    BIBLIOGRAPHY_PATH: "ef8a484b317006b083d26b35ce502a9bbbe7dd742aedfb586cfe11eadff314c5",
    REFERENCE_LEDGER_PATH: "4cde01377dde10801f9e6a75a9ce6eb4e398008a87b12c5515b06d196c3f37c6",
}
GOLDEN_COVERAGE_DIGESTS = {
    CLAIM_TEXT_PATHS[0]: "b87b1f2679c1c562e3ee1efb73afa5663b866ec1dfcb7295ac6b19ea932f6751",
    CLAIM_TEXT_PATHS[1]: "eab649d82b02785a8ceb428d36b1fef3f982f7175ba024569f9348538bf8e4f0",
    CLAIM_TEXT_PATHS[2]: "a49fda1e95b311baa1e6453e4ca587fbb05547c24d8df03c33a1d9f831214710",
    CLAIM_TEXT_PATHS[3]: "f603c6dddf39d3f4ab0aec93c8c7168966cab9b3110f8244ff77294da906e702",
    CLAIM_TEXT_PATHS[4]: "2465f61c39ae83fc58ab7e3b208e4ccec80ecef1221a654083ba239eca4b5e2c",
    CLAIM_TEXT_PATHS[5]: "2951c658ec6319ae909fb254c6476712c80761ae861cb01fce7eb07644bcc921",
    CLAIM_TEXT_PATHS[6]: "825690e935e0ac68004fe33ce0fdf1a2fb2340e6e84deed22949a1ed1a95ac79",
    CLAIM_TEXT_PATHS[7]: "76d50d48aa78100c7a3c8f3dfd7e1b88bd33ad406565c75e53272382c0848ec8",
    CLAIM_TEXT_PATHS[8]: "37c01d7607ae47b10c8134d677d4a1e49637d8e6a013d472c3af2556d55d0bc4",
    CLAIM_TEXT_PATHS[9]: "d5edb89d9287eb2fbf457436a9fceafbc0383ecb1359540d51139d941464e5c5",
}
GOLDEN_CLAIM_TYPE_COUNTS = {
    "PROSE_PROPOSITION": 293, "TABLE_SCIENTIFIC_ROW": 55, "DISPLAY_EQUATION": 48,
    "TIKZ_SCIENTIFIC_DEFINITION": 32, "BIBLIOGRAPHY_ENTRY": 28,
    "LEDGER_SELF_REPORT": 15, "CURATED_ATOMIC_PROPOSITION": 6, "CAPTION": 5,
}
GOLDEN_SURFACE_COUNTS = {
    "ADOPTED_RELEASE_TEXT": 439, "BIBLIOGRAPHY_ENTRY": 28, "LEDGER_SELF_REPORT": 15,
}
TIKZ_GOLDEN = {
    (CLAIM_TEXT_PATHS[0], 132, 155): (20, "0b73e9b37c8be14b8665b4892a85d66a205c22d21d633723ee612375543c9826"),
    (CLAIM_TEXT_PATHS[4], 269, 283): (12, "0971c35852c1b3b93bc594c4d25cbfce6c70cc46205dd1ed1cf116596e0ba283"),
}

# Independent, full {authors,title} projection SHA-256 for all 28 records.
METADATA_HASHES = {
    "reimers1992":"7828e67f9809de44360434b305380c42957badaf089043266d6ee63bc72634b0",
    "vanderven1998":"5f7aeacc82d7a38f27e0e0068b1740134aacedc9e00d433978e3f1d403a40ce8",
    "mott1968":"00070ca9e528124cfc2b57017d3b96567206c4a7f576f21922e362479dae5ac7",
    "imada1998":"97162ed6d480c5d44c4c1d5bda221853e0e5e9e92310d840f03829cf473df52d",
    "marianetti2004":"f70524f4a9d8f9770abc51d12d496ea399425307c2c234222fb0850826a4690d",
    "menetrier1999":"030a5b35bc8f273bbb2e4a8372f568537ba5a89eaff8faa5fee40d59205ff750",
    "motohashi2009":"bab3030c4f4e95774e7cc36fd5343a7bd12f84adbe3b0b4c6e8e845915cbc350",
    "xia2007":"a418e744213525b01a2a4b728271f4843a4b79cd3436630a33eed22e10ea20b3",
    "reynier2004":"82e69f21a6fdf763350e1622b0e75fe47671c68dc3bb2a70de46835e680b30ed",
    "swiderska2019":"a0a39908fe4e47f8b125f2a9bc2d9e3f78481db2922f6628ac1be964bb1f5fe1",
    "msmr_origin2017":"f8b1eda6378b3e0961cd8c4a87d67c031d881ff4a3f9222c5f63964d1b0ad22e",
    "bakerverbrugge2018":"328a8cb67d0f4b252a5b7e5547f52b77e97ec1b2da32aec8dee18bb242b457b1",
    "msmr2024":"706989ba41819e1d5882a459b6095ab0088de08727aa67b95b47bf5cc5ff20d1",
    "ml2024":"b9aaab73b7b09fc40cca9fd09cc031013c9665983f9d0d9acfc6196c461298d7",
    "wen_huggins1981":"617d4c5432450498811fcc375d17500e1673f34f5c76d9129dacfed71b917790",
    "limthongkul2003":"521a2edcd5bf0434568339e4dccd2543b654c3c88494f88aeffc4e3bed5bebed",
    "li_dahn2007":"e3a2ff6cd6fd8a0c8f9c04d989ccec9d5b4ece701b0e872a19d61ec5549949e5",
    "obrovac_christensen2004":"e0d4f93b23360d42f6cf038b3078a853ed234b0bece427146ee67872e901560e",
    "chevrier_dahn2009":"522c0fbaa2f612dc6000525c02d5ccc9a5e607828de9bb5cf93df8f33470b549",
    "beaulieu2001":"0b65ef70022ab16b336b07e37d23dea29077bc67c068d7cbe7b23bd847f0f9fb",
    "sethuraman_stressevo2010":"8ebb16b192edc9a57e6523f6a30b4510feb5791ba74ffe504309cc4d4de4703d",
    "sethuraman_stresspot2010":"0c06c57e7491cb9e790cafc8ad3233e096d1e85be11da0115b106d00ab009443",
    "liu_sizefracture2012":"691d43eda7eb23fc1ded684583110d4664c01eeacd8e6a8eb73dce4ebfd50fa7",
    "obrovac_chevrier2014":"32b3ab28e4622b43ecd39406ce2c23d4fbd150e110f1fddb0a21de7bd3100394",
    "verbrugge_lisi2016":"aad6cb3c00a7f015b2b3c0aaef38dfa8d60bde39477ecbb97718cb330c2aa85a",
    "jiang_sihys2020":"5917a031257b8d48d6ee2e793ba92be898792f33f5853d6608e164d8ff4c7a3d",
    "larchecahn1973":"c94f8cb02d8ebba735a2c1ea93b8d0f73a30dd0d591af97f8ea8efea6e36da8a",
    "koebbing2024":"d165057b3773cb5e1d90b390653b24460e9b4a56001df5aa8b6fd8ca6aac3f47",
}
LEDGER_HASHES = {
    "P062-LEDGER-0001":"dc313a245d6a5fdfcb21d3a6befa6b7ce89fbc27da68f7cec2ce74fe8d96e965",
    "P062-LEDGER-0002":"32dee504e677f03b19cbdba4e4444df99eab9836eef04f7fdafdeef0ced0ed5b",
    "P062-LEDGER-0003":"e7de9fa03661626374f8f277d5d446329987f5b702fb091fabfbc052f5c8d231",
    "P062-LEDGER-0004":"f0315b85b7e515969136491e41604fdac5724fcf336d56bc2d008f50420dd7fc",
}


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_normalized_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def lf_sha256(raw: bytes) -> str:
    return sha256(lf_normalized_bytes(raw))


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def compact_hash(value: Any) -> str:
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
    return sha256(raw)


def traversal(value: Any) -> dict[str, int]:
    counts = {"nodes":0,"mapping_objects":0,"mapping_keys":0,"lists":0,"scalars":0,"max_depth":0}
    stack = [(value, 0)]
    while stack:
        item, depth = stack.pop()
        counts["nodes"] += 1
        counts["max_depth"] = max(counts["max_depth"], depth)
        if isinstance(item, dict):
            counts["mapping_objects"] += 1
            counts["mapping_keys"] += len(item)
            stack.extend((v, depth + 1) for v in item.values())
        elif isinstance(item, list):
            counts["lists"] += 1
            stack.extend((v, depth + 1) for v in item)
        else:
            counts["scalars"] += 1
            if isinstance(item, float) and not math.isfinite(item):
                fail("non-finite JSON float")
    return counts


def strict_json(raw: bytes) -> Any:
    def hook(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                fail(f"duplicate JSON key: {key}")
            out[key] = value
        return out
    value = json.loads(raw, object_pairs_hook=hook, parse_constant=lambda x: fail(f"non-finite JSON: {x}"))
    traversal(value)
    return value


def run_git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, check=False, capture_output=True,
                          text=True, encoding="utf-8", errors="strict", timeout=30)
    if check and proc.returncode:
        fail(f"git {' '.join(args)} failed rc={proc.returncode}: {proc.stderr.strip()}")
    return proc.stdout.rstrip("\r\n")


@functools.lru_cache(maxsize=None)
def git_bytes(commit: str, path: str) -> bytes:
    proc = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, check=False,
                          capture_output=True, timeout=30)
    if proc.returncode:
        fail(f"missing Git object {commit}:{path}")
    return proc.stdout


def decoded_lines(raw: bytes) -> list[str]:
    for encoding in ("utf-8", "cp949"):
        try:
            return raw.decode(encoding, "strict").splitlines()
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", "replace").splitlines()


def semantic_projection(data: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(data)
    projected.pop("semantic_sha256", None)
    return projected


def refresh_digest(data: dict[str, Any]) -> None:
    data["semantic_sha256"] = sha256(canonical_bytes(semantic_projection(data)))


def assert_close(actual: Any, expected: float, tol: float) -> None:
    if not isinstance(actual, (int, float)) or isinstance(actual, bool) or not math.isfinite(float(actual)) or abs(float(actual) - expected) > tol:
        fail(f"numeric mismatch: {actual!r} != {expected!r}")


def validate_builder_boundary() -> None:
    raw = lf_normalized_bytes(BUILDER.read_bytes())
    if sha256(raw) != EXPECTED_BUILDER_SHA256:
        fail("builder fixed SHA mismatch; refusing execution")
    tree = ast.parse(raw.decode("utf-8", "strict"), filename=str(BUILDER))
    banned = {"requests", "urllib", "http", "ftplib", "socket", "numpy", "pandas", "importlib"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(a.name.split(".")[0] in banned for a in node.names):
            fail("builder prohibited import")
        if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in banned:
            fail("builder prohibited import-from")
        if isinstance(node, ast.Call):
            name = node.func.id if isinstance(node.func, ast.Name) else ""
            attr = node.func.attr if isinstance(node.func, ast.Attribute) else ""
            if name in {"eval", "exec", "compile", "__import__"} or attr in {"system", "popen"}:
                fail(f"builder dynamic execution: {name or attr}")
    text = raw.decode("utf-8", "strict")
    if "import Claude" in text or "from Claude" in text or "Claude." in text:
        fail("builder production import boundary violated")


def source_attestation_diagnostics(data: dict[str, Any]) -> set[str]:
    code = "SOURCE_ATTESTATION_SCHEMA_TAMPER"
    errors: set[str] = set()
    rows = data.get("source_attestations", [])
    required_keys = {
        "commit", "path", "git_blob", "raw_sha256", "physical_lines",
        "read_start", "read_end", "read_state", "decoding",
    }
    if (not isinstance(rows, list) or len(rows) != 21
            or compact_hash(rows) != EXPECTED_SOURCE_ATTESTATIONS_SHA256):
        errors.add(code)
        return errors
    seen: set[tuple[str, str]] = set()
    for row in rows:
        try:
            if not isinstance(row, dict) or set(row) != required_keys or row.get("decoding") != "UTF-8_STRICT":
                errors.add(code)
                continue
            identity = (row["commit"], row["path"])
            if identity in seen:
                errors.add(code)
                continue
            seen.add(identity)
            raw = git_bytes(*identity)
            raw.decode("utf-8", "strict")
            lines = raw.splitlines()
            if (row["read_state"] != "READ_FULL" or row["read_start"] != 1
                    or row["read_end"] != len(lines) or row["physical_lines"] != len(lines)
                    or row["raw_sha256"] != sha256(raw)
                    or row["git_blob"] != run_git("rev-parse", f"{row['commit']}:{row['path']}")):
                errors.add(code)
        except (KeyError, TypeError, UnicodeDecodeError, ValidationError):
            errors.add(code)
    required = {
        (BASELINE,"Claude/docs/v1.0.21/_sections/ch1_sec15_lcoelec.tex"),
        (BASELINE,"Claude/docs/v1.0.21/_sections/ch1_appD_si.tex"),
        (BASELINE,"Claude/docs/v1.0.21/_sections/ch1_bib.tex"),
        (BASELINE,"Claude/docs/v1.0.21/Anode_Fit_v1.0.21.py"),
        (BASELINE,"Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md"),
        (BASELINE,"Claude/docs/v1.0.21/results/snapshot_v1021_q6.json"),
        (BASELINE,"Claude/docs/v1.0.21/results/snapshot_v1021_q7.json"),
    }
    if not required <= seen:
        errors.add(code)
    return errors


def validate_source_attestations(data: dict[str, Any]) -> None:
    errors = source_attestation_diagnostics(data)
    if errors:
        fail(f"source attestation diagnostics: {sorted(errors)}")


def anchor_is_exact(anchor: Any, expected_state: str = "PRESENT_IN_ADOPTED_RELEASE_TEXT") -> bool:
    if not isinstance(anchor, dict):
        return False
    try:
        lines = decoded_lines(git_bytes(anchor["commit"], anchor["path"]))
        start, end = anchor["line_start"], anchor["line_end"]
        if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start or end > len(lines):
            return False
        selected = lines[start - 1:end]
        raw = ("\n".join(selected) + "\n").encode("utf-8")
        return (anchor.get("anchor_state") == expected_state
                and anchor.get("anchor_text") == "\n".join(selected)
                and anchor.get("slice_sha256") == sha256(raw))
    except (KeyError, TypeError, ValidationError):
        return False


def rows_for_path(rows: list[dict[str, Any]], path: str) -> list[dict[str, Any]]:
    return [row for row in rows if isinstance(row, dict) and row.get("path") == path]


def covering_rows(manifest: list[dict[str, Any]], path: str, line: int) -> list[dict[str, Any]]:
    return [row for row in manifest if (
        isinstance(row, dict) and row.get("path") == path
        and isinstance(row.get("line_start"), int) and isinstance(row.get("line_end"), int)
        and row["line_start"] <= line <= row["line_end"]
    )]


def claim_boundary_diagnostics(manifest: list[dict[str, Any]]) -> set[str]:
    errors: set[str] = set()
    structural = re.compile(
        r"^\\(?:renewcommand|setlength|centering|footnotesize|small|appendix|"
        r"begin\{(?:tabular|longtable)\}|endfirsthead|endhead|qquad|end\{aligned\})"
    )
    if any(structural.match(str(row.get("claim_text", "")).strip()) for row in manifest if isinstance(row, dict)):
        errors.add("STRUCTURAL_AS_CLAIM")
    structural_lines = {
        (CLAIM_TEXT_PATHS[0], 52), (CLAIM_TEXT_PATHS[0], 53),
        (CLAIM_TEXT_PATHS[8], 4), (CLAIM_TEXT_PATHS[8], 18),
        (CLAIM_TEXT_PATHS[8], 22), (CLAIM_TEXT_PATHS[8], 54), (CLAIM_TEXT_PATHS[8], 58),
    }
    if any(covering_rows(manifest, path, line) for path, line in structural_lines):
        errors.add("STRUCTURAL_AS_CLAIM")

    for (path, start, end), (count, digest) in TIKZ_GOLDEN.items():
        rows = [row for row in manifest if (
            isinstance(row, dict) and row.get("path") == path
            and row.get("claim_type") == "TIKZ_SCIENTIFIC_DEFINITION"
            and isinstance(row.get("line_start"), int) and isinstance(row.get("line_end"), int)
            and row["line_start"] >= start and row["line_end"] <= end
        )]
        if len(rows) != count or compact_hash(rows) != digest:
            errors.add("TIKZ_LOAD_BEARING_OMISSION")

    multiline = [
        (CLAIM_TEXT_PATHS[0], 153, 155, "TIKZ_SCIENTIFIC_DEFINITION"),
        (CLAIM_TEXT_PATHS[1], 64, 65, "PROSE_PROPOSITION"),
        (CLAIM_TEXT_PATHS[4], 144, 149, "DISPLAY_EQUATION"),
        (CLAIM_TEXT_PATHS[4], 164, 165, "CURATED_ATOMIC_PROPOSITION"),
        (CLAIM_TEXT_PATHS[4], 166, 167, "CURATED_ATOMIC_PROPOSITION"),
    ]
    for path, start, end, claim_type in multiline:
        rows = [row for row in manifest if (
            isinstance(row, dict) and row.get("path") == path and row.get("line_start") == start
            and row.get("line_end") == end and row.get("claim_type") == claim_type
        )]
        if len(rows) != 1:
            errors.add("MULTILINE_CLAIM_SPLIT")

    tier_fixtures = [
        (CLAIM_TEXT_PATHS[1], 64, ["B"], "SOURCE_STATED_TIER_B_UNVERIFIED"),
        (CLAIM_TEXT_PATHS[2], 126, ["A"], "SOURCE_STATED_TIER_A_UNVERIFIED"),
        (CLAIM_TEXT_PATHS[4], 122, ["A"], "SOURCE_STATED_TIER_A_UNVERIFIED"),
    ]
    for path, line, markers, tier in tier_fixtures:
        rows = [row for row in covering_rows(manifest, path, line)
                if row.get("source_tier_markers") == markers and row.get("evidence_tier") == tier]
        if len(rows) != 1:
            errors.add("A_OR_B_TIER_TO_C")
    if any(("A" in row.get("source_tier_markers", []) or "B" in row.get("source_tier_markers", []))
           and row.get("evidence_tier") == "TIER_C_MODEL" for row in manifest if isinstance(row, dict)):
        errors.add("A_OR_B_TIER_TO_C")

    unit_fixtures = [
        (CLAIM_TEXT_PATHS[2], 28, 4958.0, "J/mol"),
        (CLAIM_TEXT_PATHS[8], 59, 12000.0, "J/mol"),
        (CLAIM_TEXT_PATHS[9], 20, 300.0, "%"),
        (CLAIM_TEXT_PATHS[9], 20, 10.0, "%"),
        (CLAIM_TEXT_PATHS[4], 165, 1.1, "k_B/atom"),
        (CLAIM_TEXT_PATHS[4], 166, 0.18, "k_B/atom"),
    ]
    for path, line, value, unit in unit_fixtures:
        observations = [obs for row in covering_rows(manifest, path, line)
                        for obs in row.get("numeric_observations", []) if isinstance(obs, dict)]
        if sum(obs.get("normalized_numeric") == value and obs.get("normalized_unit") == unit
               for obs in observations) != 1:
            errors.add("UNIT_DELETION")

    registered_keys = LCO_KEYS | SI_KEYS
    observed_registered: set[str] = set()
    for row in manifest:
        if not isinstance(row, dict):
            continue
        text = str(row.get("claim_text", ""))
        observations = row.get("numeric_observations", [])
        raw_tokens = {str(obs.get("raw_token")) for obs in observations if isinstance(obs, dict)}
        for key in registered_keys:
            if not re.search(rf"(?<![A-Za-z0-9_]){re.escape(key)}(?![A-Za-z0-9_])", text):
                continue
            observed_registered.add(key)
            suffix_match = re.search(r"(\d+)$", key)
            leaked_suffix = suffix_match.group(1)[1:] if suffix_match and len(suffix_match.group(1)) > 1 else ""
            if leaked_suffix and leaked_suffix in raw_tokens:
                errors.add("CITEKEY_NUMERIC_LEAK")
    if observed_registered != registered_keys:
        errors.add("CITEKEY_NUMERIC_LEAK")
    return errors


def reconstruct_bibliography_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(decoded_lines(git_bytes(BASELINE, BIBLIOGRAPHY_PATH)), 1):
        match = re.search(r"\\bibitem\{([^}]+)\}", line)
        if not match or match.group(1) not in LCO_KEYS | SI_KEYS:
            continue
        key = match.group(1)
        frozen_doi = line.split("DOI:", 1)[1].strip().split()[0].rstrip(".;") if "DOI:" in line else None
        rows.append({
            "key": key,
            "material_group": "LCO" if key in LCO_KEYS else "SI",
            "path": BIBLIOGRAPHY_PATH,
            "line": line_no,
            "frozen_entry": line,
            "frozen_doi": frozen_doi,
            "source_tier": "ADOPTED_RELEASE_BIBLIOGRAPHY",
            "proposition_authority": False,
        })
    return sorted(rows, key=lambda row: (row["material_group"], row["line"]))


def reconstruct_citation_occurrences() -> list[dict[str, Any]]:
    names = run_git("ls-tree", "-r", "--name-only", BASELINE, "Claude/docs/v1.0.21")
    paths = sorted(path for path in names.splitlines() if Path(path).suffix.lower() == ".tex")
    rows: list[dict[str, Any]] = []
    relevant = LCO_CITE_KEYS | SI_KEYS
    for path in paths:
        for line_no, line in enumerate(decoded_lines(git_bytes(BASELINE, path)), 1):
            for command_no, match in enumerate(re.finditer(r"\\cite\{([^}]+)\}", line), 1):
                for key_no, key in enumerate((item.strip() for item in match.group(1).split(",")), 1):
                    if key not in relevant:
                        continue
                    rows.append({
                        "occurrence_id": "", "path": path, "line": line_no,
                        "cite_command_index_on_line": command_no,
                        "key_index_in_command": key_no, "key": key,
                        "material_group": "SI" if key in SI_KEYS else "LCO",
                        "line_text": line, "proposition_support_state": "UNVERIFIED_EXTERNAL",
                    })
    rows.sort(key=lambda row: (
        row["material_group"], row["path"], row["line"],
        row["cite_command_index_on_line"], row["key_index_in_command"], row["key"],
    ))
    counts = {"LCO": 0, "SI": 0}
    for row in rows:
        group = row["material_group"]
        counts[group] += 1
        row["occurrence_id"] = f"P062-CITE-{group}-{counts[group]:04d}"
    return rows


def bibliography_diagnostics(data: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    bib = data.get("bibliography_audit", {})
    rows = bib.get("rows", [])
    keys = LCO_KEYS | SI_KEYS
    if (len(rows) != 28 or {r.get("key") for r in rows if isinstance(r, dict)} != keys
            or compact_hash(rows) != EXPECTED_BIBLIOGRAPHY_ROWS_SHA256
            or rows != reconstruct_bibliography_rows()):
        errors.add("BIBLIOGRAPHY_IDENTITY_TAMPER")
    if any(r.get("source_tier") != "ADOPTED_RELEASE_BIBLIOGRAPHY" for r in rows if isinstance(r, dict)):
        errors.add("BIBLIOGRAPHY_IDENTITY_CONTRACT")
    if any(r.get("proposition_authority") is not False for r in rows if isinstance(r, dict)):
        errors.add("BIBLIOGRAPHY_AS_PROPOSITION_PROOF")
    metadata = bib.get("metadata_observations", [])
    by_key = {r.get("key"): r for r in metadata if isinstance(r, dict)}
    if (len(metadata) != 28 or set(by_key) != keys
            or compact_hash(metadata) != EXPECTED_METADATA_ROWS_SHA256):
        errors.add("METADATA_IDENTITY_TAMPER")
    for key, expected in METADATA_HASHES.items():
        row = by_key.get(key)
        if row is None:
            continue
        authors, title = row.get("normalized_authors"), row.get("normalized_title")
        good = (isinstance(authors, list) and bool(authors)
                and all(isinstance(v, str) and v.strip() for v in authors)
                and isinstance(title, str) and bool(title.strip()))
        if not good or compact_hash({"authors":authors,"title":title}) != expected:
            errors.add("METADATA_IDENTITY_TAMPER")
        expected_fulltext = key == "verbrugge_lisi2016"
        if row.get("primary_fulltext_verified") is not expected_fulltext or row.get("metadata_is_not_proposition_proof") is not True:
            errors.add("WEB_METADATA_AS_FULLTEXT")
    conflict = [r for r in metadata if isinstance(r, dict) and r.get("resolver_state") == "CONFLICTING_IDENTIFIER"]
    if len(conflict) != 1 or conflict[0].get("key") != "limthongkul2003" or conflict[0].get("normalized_doi", "").lower() != "10.1016/s1359-6454(02)00514-1":
        errors.add("LIMTHONGKUL_IDENTITY_CONTRACT")
    if sum(r.get("resolver_state") == "RESOLVED_METADATA_MATCH" for r in metadata if isinstance(r, dict)) != 27:
        errors.add("METADATA_IDENTITY_TAMPER")
    occ = data.get("citation_occurrences", [])
    ids = [r.get("occurrence_id") for r in occ if isinstance(r, dict)]
    if (len(occ) != 72 or len(ids) != len(set(ids))
            or sum(r.get("material_group") == "LCO" for r in occ if isinstance(r, dict)) != 54
            or sum(r.get("material_group") == "SI" for r in occ if isinstance(r, dict)) != 18
            or data.get("citation_denominators") != {"total":72,"LCO":54,"SI":18}
            or compact_hash(occ) != EXPECTED_CITATION_ROWS_SHA256
            or occ != reconstruct_citation_occurrences()):
        errors.add("CITATION_DENOMINATOR_TAMPER")
    if "BIBLIOGRAPHY_AS_PROPOSITION_PROOF" in errors:
        errors.discard("BIBLIOGRAPHY_IDENTITY_TAMPER")
    if "WEB_METADATA_AS_FULLTEXT" in errors:
        errors.discard("METADATA_IDENTITY_TAMPER")
    return errors


def claim_contract_diagnostics(data: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    manifest = data.get("source_claim_manifest", [])
    coverage = data.get("source_claim_coverage", [])
    scope = data.get("scope_matrix", [])
    if not isinstance(manifest, list) or not isinstance(coverage, list) or not isinstance(scope, list):
        return {"SOURCE_CLAIM_MANIFEST_MISSING"}
    expected_total = sum(GOLDEN_CLAIM_COUNTS.values())
    expected_claim_ids = [f"P062-SOURCE-CLAIM-{index:04d}" for index in range(1, expected_total + 1)]
    expected_scope_ids = [f"P062-SCOPE-{index:04d}" for index in range(1, expected_total + 1)]
    actual_manifest_ids = [row.get("source_claim_id") for row in manifest if isinstance(row, dict)]
    actual_claim_ids = [row.get("source_claim_id") for row in scope if isinstance(row, dict)]
    actual_scope_ids = [row.get("scope_id") for row in scope if isinstance(row, dict)]

    precise = claim_boundary_diagnostics(manifest)
    errors |= precise
    if len(manifest) != expected_total or actual_manifest_ids != expected_claim_ids:
        errors.add("SOURCE_CLAIM_MANIFEST_MISSING")
    if len(scope) == expected_total - 1:
        errors.add("MISSING_SCOPE_ROUTING")
    elif (len(scope) != expected_total
          or len(actual_claim_ids) != len(set(actual_claim_ids))
          or len(actual_scope_ids) != len(set(actual_scope_ids))
          or actual_claim_ids != expected_claim_ids
          or actual_scope_ids != expected_scope_ids):
        errors.add("SOURCE_CLAIM_MULTI_MAPPED")

    anchor_error = False
    allowed_surfaces = set(GOLDEN_SURFACE_COUNTS)
    for index, row in enumerate(manifest, 1):
        if not isinstance(row, dict):
            errors.add("SOURCE_CLAIM_MANIFEST_MISSING")
            continue
        expected_state = (
            "PRESENT_IN_REFERENCE_LEDGER_SELF_REPORT"
            if row.get("source_surface") == "LEDGER_SELF_REPORT"
            else "PRESENT_IN_ADOPTED_RELEASE_TEXT"
        )
        anchor = row.get("anchor")
        if (row.get("source_surface") not in allowed_surfaces
                or row.get("route_kind") != "SCOPE"
                or row.get("route_id") != f"P062-SCOPE-{index:04d}"
                or row.get("source_claim_id") != f"P062-SOURCE-CLAIM-{index:04d}"
                or row.get("external_scientific_truth_validated") is not False
                or row.get("external_material_truth_validated") is not False):
            errors.add("SOURCE_CLAIM_MANIFEST_MISSING")
        if (not isinstance(row.get("claim_text"), str)
                or row.get("claim_text_sha256") != sha256((row.get("claim_text", "") + "\n").encode("utf-8"))):
            errors.add("SOURCE_CLAIM_MANIFEST_MISSING")
        if (not anchor_is_exact(anchor, expected_state)
                or not isinstance(anchor, dict)
                or (row.get("path"), row.get("line_start"), row.get("line_end")) != (
                    anchor.get("path"), anchor.get("line_start"), anchor.get("line_end")
                )):
            anchor_error = True
    if anchor_error:
        errors.add("ANCHOR_SLICE_HASH_TAMPER")

    manifest_digest_error = False
    for path, count in GOLDEN_CLAIM_COUNTS.items():
        rows = rows_for_path(manifest, path)
        if len(rows) != count or compact_hash(rows) != GOLDEN_CLAIM_DIGESTS[path]:
            manifest_digest_error = True
    type_counts = {name: sum(row.get("claim_type") == name for row in manifest if isinstance(row, dict))
                   for name in GOLDEN_CLAIM_TYPE_COUNTS}
    surface_counts = {name: sum(row.get("source_surface") == name for row in manifest if isinstance(row, dict))
                      for name in GOLDEN_SURFACE_COUNTS}
    if type_counts != GOLDEN_CLAIM_TYPE_COUNTS or surface_counts != GOLDEN_SURFACE_COUNTS:
        manifest_digest_error = True
    by_coverage = {row.get("path"): row for row in coverage if isinstance(row, dict)}
    if len(coverage) != len(CLAIM_TEXT_PATHS) or set(by_coverage) != set(CLAIM_TEXT_PATHS):
        manifest_digest_error = True
    else:
        for path, digest in GOLDEN_COVERAGE_DIGESTS.items():
            if compact_hash(by_coverage[path]) != digest:
                manifest_digest_error = True
    if manifest_digest_error and not precise and not anchor_error and len(manifest) == expected_total:
        errors.add("SOURCE_CLAIM_MANIFEST_MISSING")

    scope_digest_error = False
    scope_by_claim = {row.get("source_claim_id"): row for row in scope if isinstance(row, dict)}
    if len(scope_by_claim) == expected_total and len(manifest) == expected_total:
        for path in GOLDEN_CLAIM_COUNTS:
            path_scope = [scope_by_claim.get(row.get("source_claim_id")) for row in rows_for_path(manifest, path)]
            if None in path_scope or compact_hash(path_scope) != GOLDEN_SCOPE_DIGESTS[path]:
                scope_digest_error = True
    else:
        scope_digest_error = True
    gnfs = data.get("ground_not_found_records", [])
    if compact_hash(gnfs) != EXPECTED_GNF_SHA256:
        errors.add("GNF_ORPHAN")
    gnf_ids = [f"P062-GNF-{i:03d}" for i in range(1, 18)]
    by_gnf = {r.get("ground_not_found_id"): r for r in gnfs if isinstance(r, dict)}
    if len(gnfs) != 17 or set(by_gnf) != set(gnf_ids):
        errors.add("GNF_ORPHAN")
    for row in by_gnf.values():
        if row.get("external_scientific_truth_validated") is not False or row.get("external_material_truth_validated") is not False:
            errors.add("EXTERNAL_AUTHORITY_PROMOTION")
        if row.get("search_authority") != "INTERNAL_FROZEN_RELEASE_ONLY_NOT_EXTERNAL_ABSENCE" or row.get("status") != "GROUND_NOT_FOUND_IN_FROZEN_ADOPTED_RELEASE_SCOPE":
            errors.add("GNF_ORPHAN")
        for source in row.get("searched_sources", []):
            try:
                raw = git_bytes(source["commit"], source["path"])
                if source.get("raw_sha256") != sha256(raw) or source.get("physical_lines") != len(raw.splitlines()):
                    errors.add("GNF_ORPHAN")
            except (KeyError, TypeError, ValidationError):
                errors.add("GNF_ORPHAN")
    links: list[str] = []
    for index, row in enumerate(scope, 1):
        if not isinstance(row, dict):
            errors.add("MISSING_SCOPE_ROUTING")
            continue
        if row.get("source_surface") not in allowed_surfaces or row.get("claim_surface") not in allowed_surfaces:
            errors.add("SCOPE_SEMANTIC_CONTRACT")
        if row.get("evidence_tier") not in ALLOWED_EVIDENCE_TIERS or row.get("proposition_state") not in ALLOWED_STATES:
            errors.add("SCOPE_SEMANTIC_CONTRACT")
        if row.get("external_scientific_truth_validated") is not False or row.get("external_material_truth_validated") is not False:
            errors.add("EXTERNAL_AUTHORITY_PROMOTION")
        primary, targets = row.get("primary_target_phase"), row.get("downstream_target_phases")
        if not isinstance(primary, int) or not isinstance(targets, list) or primary not in targets:
            errors.add("SCOPE_SEMANTIC_CONTRACT")
        anchor, gid = row.get("claim_anchor"), row.get("ground_not_found_id")
        if anchor is None or gid is not None:
            errors.add("MISSING_SCOPE_ROUTING")
        expected_state = "PRESENT_IN_REFERENCE_LEDGER_SELF_REPORT" if row.get("claim_surface") == "LEDGER_SELF_REPORT" else "PRESENT_IN_ADOPTED_RELEASE_TEXT"
        if anchor is not None and not anchor_is_exact(anchor, expected_state):
            errors.add("ANCHOR_SLICE_HASH_TAMPER")
        gaps = row.get("evidence_gap_ids")
        if not isinstance(gaps, list):
            errors.add("SCOPE_SEMANTIC_CONTRACT")
        else:
            links.extend(gaps)
        claim = manifest[index - 1] if index <= len(manifest) and isinstance(manifest[index - 1], dict) else {}
        if claim and (
            row.get("scope_id") != claim.get("route_id")
            or row.get("source_claim_id") != claim.get("source_claim_id")
            or row.get("claim_surface") != claim.get("source_surface")
            or row.get("source_surface") != claim.get("source_surface")
            or row.get("claim_anchor") != claim.get("anchor")
            or row.get("semantic_role") != claim.get("semantic_role")
            or row.get("evidence_tier") != claim.get("evidence_tier")
            or row.get("proposition_state") != claim.get("proposition_state")
            or row.get("authority_ceiling") != claim.get("authority_ceiling")
        ):
            scope_digest_error = True
    if len(links) != 17 or set(links) != set(gnf_ids) or any(v not in gnf_ids for v in links):
        errors.add("GNF_ORPHAN")
    expected_contract = {
        "source_claim_denominator": expected_total,
        "scope_row_denominator": expected_total,
        "scope_id_first": "P062-SCOPE-0001",
        "scope_id_last": f"P062-SCOPE-{expected_total:04d}",
        "ground_not_found_denominator": 17,
        "lexical_inventory_is_navigation_only": True,
        "source_claim_to_scope_bijection": True,
        "every_scope_row_has_exact_anchor": True,
        "all_ground_not_found_records_linked_once": True,
        "claim_counts_by_path": {
            path: GOLDEN_CLAIM_COUNTS[path] for path in sorted(GOLDEN_CLAIM_COUNTS)
        },
    }
    if data.get("material_claim_contract") != expected_contract:
        errors.add("MISSING_SCOPE_ROUTING")
    inventory = data.get("adopted_release_text_inventory", {})
    adopted_scope_ids = [row.get("route_id") for row in manifest
                         if isinstance(row, dict) and row.get("source_surface") == "ADOPTED_RELEASE_TEXT"]
    if (inventory.get("authority_class") != "ADOPTED_RELEASE_TEXT"
            or inventory.get("claim_row_denominator") != 439
            or inventory.get("present_anchor_rows") != 439
            or inventory.get("ground_not_found_route_rows") != 0
            or inventory.get("scope_ids") != adopted_scope_ids
            or "exactly one scope row" not in inventory.get("rule", "")):
        errors.add("MISSING_SCOPE_ROUTING")
    by_role: dict[str, list[dict[str, Any]]] = {}
    for row in scope:
        if isinstance(row, dict):
            by_role.setdefault(str(row.get("semantic_role")), []).append(row)
    one_rows = by_role.get("LCO_MODEL_GATE_INTEGRAL_1P1_KB_PER_ATOM", [])
    one = one_rows[0] if len(one_rows) == 1 else {}
    if not (one.get("value") == 1.1 and one.get("unit") == "k_B/atom"
            and one.get("quantity") == "model gate-integrated complete-metal electronic entropy"
            and one.get("basis") == "complete-metal electronic entropy and model MIT gate integral"
            and one.get("evidence_gap_ids") == ["P062-GNF-011"]):
        errors.add("UNIT_BASIS_COLLAPSE")
    point_rows = by_role.get("LCO_O3_TOTAL_PARTIAL_MOLAR_0P18_KB_PER_ATOM", [])
    point18 = point_rows[0] if len(point_rows) == 1 else {}
    if not (point18.get("value") == 0.18 and point18.get("unit") == "k_B/atom"
            and point18.get("quantity") == "O3 total partial-molar entropy quantity"
            and point18.get("basis") == "O3 configurational plus vibrational plus electronic total partial-molar quantity"
            and point18.get("evidence_gap_ids") == ["P062-GNF-012"]):
        errors.add("UNIT_BASIS_COLLAPSE")
    tier_c_rows = by_role.get("LCO_TIER_C_ONE_POINT_DEMONSTRATION", [])
    if not tier_c_rows or any(row.get("evidence_tier") != "TIER_C_MODEL" or "not material truth" not in row.get("authority_ceiling", "") for row in tier_c_rows):
        errors.add("TIER_C_TO_MATERIAL_PROMOTION")
    pure_rows = by_role.get("PURE_LCO_TO_DOPED_LCO_PROMOTION", [])
    if not pure_rows or any(row.get("proposition_state") != "REJECTED" or "doped" not in row.get("authority_ceiling", "").lower() for row in pure_rows):
        errors.add("PURE_LCO_TO_DOPED_LCO_PROMOTION")
    bridge_rows = by_role.get("SI_BRIDGEHEAD_NOT_COMPLETE_MODEL", [])
    if not bridge_rows or any(row.get("proposition_state") != "REJECTED" or "complete Si derivation" not in row.get("authority_ceiling", "") for row in bridge_rows):
        errors.add("SI_BRIDGEHEAD_TO_COMPLETE_MODEL")
    precise_scope_codes = {
        "UNIT_BASIS_COLLAPSE", "TIER_C_TO_MATERIAL_PROMOTION",
        "PURE_LCO_TO_DOPED_LCO_PROMOTION", "SI_BRIDGEHEAD_TO_COMPLETE_MODEL",
        "MISSING_SCOPE_ROUTING", "ANCHOR_SLICE_HASH_TAMPER",
        "SOURCE_CLAIM_MANIFEST_MISSING",
        "STRUCTURAL_AS_CLAIM", "TIKZ_LOAD_BEARING_OMISSION", "MULTILINE_CLAIM_SPLIT",
        "A_OR_B_TIER_TO_C", "UNIT_DELETION", "CITEKEY_NUMERIC_LEAK",
    }
    if scope_digest_error and not (errors & precise_scope_codes) and "SOURCE_CLAIM_MULTI_MAPPED" not in errors:
        errors.add("SCOPE_SEMANTIC_CONTRACT")
    return errors


def ledger_diagnostics(data: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    inv = data.get("reference_ledger_self_report_inventory", {})
    if (inv.get("authority_class") != "REFERENCE_LEDGER_SELF_REPORT"
            or inv.get("source_path") != "Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md"
            or inv.get("statement_denominator") != 4
            or inv.get("adopted_release_text_authority_granted") is not False
            or inv.get("proposition_truth_validated") is not False):
        errors.add("LEDGER_RELEASE_AUTHORITY_CONFLATION")
    rows = inv.get("rows", [])
    by_id = {r.get("ledger_statement_id"):r for r in rows if isinstance(r, dict)}
    if len(rows) != 4 or set(by_id) != set(LEDGER_HASHES):
        errors.add("LEDGER_RELEASE_AUTHORITY_CONFLATION")
    for sid, expected in LEDGER_HASHES.items():
        row = by_id.get(sid)
        if row is None or compact_hash(row) != expected or not anchor_is_exact(row.get("anchor"), "PRESENT_IN_REFERENCE_LEDGER_SELF_REPORT"):
            errors.add("LEDGER_RELEASE_AUTHORITY_CONFLATION")
    return errors


def q6_q7_diagnostics(data: dict[str, Any]) -> set[str]:
    errors: set[str] = set()
    try:
        q6 = data["q6_lco_audit"]
        assert_close(q6["slot_arithmetic"]["delta_S_e_J_per_mol_K"], -45.678261885287384, 5e-12)
        assert_close(q6["slot_arithmetic"]["delta_S_eff_J_per_mol_K"], -39.678261885287384, 5e-12)
        assert_close(q6["slot_arithmetic"]["slot_slope_mV_per_K"], -0.4112376212394402, 5e-12)
        rows = {float(r["x_bar"]):r for r in q6["independent_recomputation"]}
        for x, state, expected in ((.5,"gate_on",3.924249955),(.5,"gate_off",4.042610795),(.85,"gate_on",4.009535354),(.85,"gate_off",4.100834215)):
            assert_close(rows[x][state]["U_oc_V"], expected, 5e-9)
        coord = q6["coordinate_adjudication"]
        if (coord.get("gate_argument") != "T1_TRANSITION_X_CENTER_FIXED_AT_0.85"
                or coord.get("x_bar_role") != "GLOBAL_TOTAL_DELITHIATION_FRACTION"
                or coord.get("gate_depends_on_global_x_bar") is not False):
            fail("Q6 coordinate mismatch")
    except (ValidationError, KeyError, TypeError, ValueError):
        errors.add("Q6_NUMERIC_TAMPER")
    try:
        q7 = data["q7_si_audit"]; delta = q7["snapshot_delta"]
        if (delta["ch1_label_count_q6"],delta["ch1_label_count_q7"],delta["actual_added_labels"],delta["ledger_claimed_added_labels"],delta["added_equation_blocks"]) != (247,254,7,6,0):
            fail("Q7 delta mismatch")
        if {r["scope"] for r in q7["missing_governing_equations"]} != REQUIRED_MISSING_SI:
            fail("Q7 missing scopes")
        if q7["governing_equation_conclusion"] != "NO_SI_SPECIFIC_GOVERNING_EQUATION_IN_V1021":
            fail("Q7 conclusion")
    except (ValidationError, KeyError, TypeError, ValueError):
        errors.add("Q7_LABEL_DELTA_TAMPER")
    return errors


def authority_diagnostics(data: dict[str, Any]) -> set[str]:
    errors: set[str] = set(); auth = data.get("authority_contract", {})
    for key in ("external_scientific_truth_validated","external_material_truth_validated",
                "external_experimental_truth_validated","canonical_equation_accepted","final_manuscript_ready"):
        if auth.get(key) is not False:
            errors.add("EXTERNAL_AUTHORITY_PROMOTION")
    if data.get("status") != "PASS_WITH_CONCERNS" or data.get("gate") != "PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS":
        errors.add("STATUS_PROMOTION")
    expected_rf = {"sentinel":"P062_STEP54_RESULT_FIRST_PRECOMMIT",
        "write_order":["PHASE_062_STEP_054_LCO_SI_SCOPE_RESULT.md","PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json"],
        "containing_commit":"PENDING_AT_PRECOMMIT_BY_DESIGN","persistence_claimed":False,
        "step55_blocked_until":"PASS_P062_STEP54_PERSISTENCE"}
    if data.get("result_first_contract") != expected_rf:
        errors.add("RESULT_FIRST_CONTRACT_TAMPER")
    expected_neg = {"required_ids":NEGATIVE_IDS,"required_count":28,
        "execution_requirement":"VALIDATOR_EXECUTES_EVERY_REAL_MUTATION_SUBFIXTURE_AND_REQUIRES_SINGLETON_DIAGNOSTIC_PER_ID",
        "stored_pass_claim":False}
    if data.get("negative_control_contract") != expected_neg:
        errors.add("NEGATIVE_CONTROL_CONTRACT")
    if data.get("finding_summary") != {"P0":0,"P1":8,"P2":8}:
        errors.add("FINDING_CONTRACT")
    findings = {r.get("finding_id") for r in data.get("findings", []) if isinstance(r, dict)}
    if not REQUIRED_CONTRADICTIONS <= findings:
        errors.add("FINDING_CONTRACT")
    return errors


def content_diagnostics(data: dict[str, Any], *, check_digest: bool = True) -> set[str]:
    errors: set[str] = set()
    if data.get("schema_version") != "phase062-step54-v1" or data.get("artifact_id") != "PHASE_062_V1021_LCO_SI_SCOPE_MATRIX":
        errors.add("SCHEMA_CONTRACT")
    provenance = data.get("provenance", {})
    if provenance != EXPECTED_PROVENANCE:
        errors.add("PROVENANCE_IDENTITY_TAMPER")
    if data.get("builder_sha256") != EXPECTED_BUILDER_SHA256:
        errors.add("BUILDER_IDENTITY_CONTRACT")
    navigation = data.get("source_line_inventory", [])
    if len(navigation) != 504 or compact_hash(navigation) != EXPECTED_NAVIGATION_SHA256:
        errors.add("NAVIGATION_CONTRACT")
    elif any(row.get("semantic_status") != "LEXICAL_INVENTORY_REQUIRES_CURATED_SCOPE_ROW_FOR_LOAD_BEARING_USE" for row in navigation):
        errors.add("NAVIGATION_CONTRACT")
    errors |= bibliography_diagnostics(data)
    errors |= source_attestation_diagnostics(data)
    errors |= claim_contract_diagnostics(data)
    errors |= ledger_diagnostics(data)
    errors |= q6_q7_diagnostics(data)
    errors |= authority_diagnostics(data)
    if check_digest and data.get("semantic_sha256") != sha256(canonical_bytes(semantic_projection(data))):
        errors.add("SEMANTIC_DIGEST_TAMPER")
    return errors


def singleton_diagnostics(data: dict[str, Any], wanted: str) -> set[str]:
    del wanted
    return content_diagnostics(data)


def run_negative_controls(data: dict[str, Any]) -> list[str]:
    baseline = content_diagnostics(data)
    if baseline:
        fail(f"negative baseline not clean: {sorted(baseline)}")
    cases: list[tuple[str, Any]] = []
    cases.append((NEGATIVE_IDS[0],lambda d:d["bibliography_audit"]["rows"][0].__setitem__("proposition_authority",True)))
    cases.append((NEGATIVE_IDS[1],lambda d:d["bibliography_audit"]["metadata_observations"][0].__setitem__("primary_fulltext_verified",True)))
    def collapse(d: dict[str, Any]) -> None:
        r = next(x for x in d["scope_matrix"] if x["semantic_role"] == "LCO_MODEL_GATE_INTEGRAL_1P1_KB_PER_ATOM")
        r.update(value=.18,quantity="O3 total partial-molar entropy quantity",basis="configurational plus vibrational plus electronic total partial-molar quantity in the O3 region")
    cases.append((NEGATIVE_IDS[2],collapse))
    cases.append((NEGATIVE_IDS[3],lambda d:next(x for x in d["scope_matrix"] if x["semantic_role"]=="LCO_TIER_C_ONE_POINT_DEMONSTRATION").__setitem__("authority_ceiling","material truth confirmed")))
    cases.append((NEGATIVE_IDS[4],lambda d:next(x for x in d["scope_matrix"] if x["semantic_role"]=="PURE_LCO_TO_DOPED_LCO_PROMOTION").__setitem__("proposition_state","EXACT_INTERNAL_SOURCE_MATCH")))
    cases.append((NEGATIVE_IDS[5],lambda d:next(x for x in d["scope_matrix"] if x["semantic_role"]=="SI_BRIDGEHEAD_NOT_COMPLETE_MODEL").__setitem__("proposition_state","EXACT_INTERNAL_SOURCE_MATCH")))
    cases.append((NEGATIVE_IDS[6],lambda d:d["scope_matrix"].pop(30)))
    cases.append((NEGATIVE_IDS[7],lambda d:d["authority_contract"].__setitem__("external_material_truth_validated",True)))
    cases.append((NEGATIVE_IDS[8],lambda d:d.__setitem__("status","PASS")))
    cases.append((NEGATIVE_IDS[9],[
        lambda d:d["bibliography_audit"]["metadata_observations"][0].__setitem__("normalized_authors",[]),
        lambda d:d["bibliography_audit"]["metadata_observations"][0].__setitem__("normalized_doi","10.0/fake"),
        lambda d:d["bibliography_audit"]["metadata_observations"][0].__setitem__("page_or_article","FAKE"),
    ]))
    cases.append((NEGATIVE_IDS[10],[
        lambda d:d["citation_occurrences"].pop(),
        lambda d:d["citation_occurrences"][0].__setitem__("key","mott1968"),
        lambda d:d["citation_occurrences"][0].__setitem__("line",9999),
        lambda d:d["citation_occurrences"][0].__setitem__("line_text","FAKE"),
    ]))
    cases.append((NEGATIVE_IDS[11],lambda d:d["q6_lco_audit"]["slot_arithmetic"].__setitem__("delta_S_e_J_per_mol_K",0.0)))
    cases.append((NEGATIVE_IDS[12],lambda d:d["q7_si_audit"]["snapshot_delta"].__setitem__("actual_added_labels",6)))
    cases.append((NEGATIVE_IDS[13],lambda d:d["ground_not_found_records"].pop()))
    cases.append((NEGATIVE_IDS[14],lambda d:next(x for x in d["scope_matrix"] if x["claim_anchor"] is not None)["claim_anchor"].__setitem__("slice_sha256","0"*64)))
    cases.append((NEGATIVE_IDS[15],lambda d:d.__setitem__("semantic_sha256","0"*64)))
    cases.append((NEGATIVE_IDS[16],lambda d:d["result_first_contract"].__setitem__("write_order",list(reversed(d["result_first_contract"]["write_order"])))))
    cases.append((NEGATIVE_IDS[17],lambda d:d["source_claim_manifest"].pop()))
    def multi_map(d: dict[str, Any]) -> None:
        row = copy.deepcopy(next(row for row in d["scope_matrix"] if not row["evidence_gap_ids"]))
        row["scope_id"] = d["scope_matrix"][-1]["scope_id"]
        d["scope_matrix"].append(row)
    cases.append((NEGATIVE_IDS[18],multi_map))
    def structural_claim(d: dict[str, Any]) -> None:
        row = d["source_claim_manifest"][0]
        row["claim_text"] = r"\renewcommand{\arraystretch}{1.3}"
        row["claim_text_sha256"] = sha256((row["claim_text"] + "\n").encode("utf-8"))
    cases.append((NEGATIVE_IDS[19], structural_claim))
    def omit_tikz(d: dict[str, Any]) -> None:
        row = next(row for row in d["source_claim_manifest"]
                   if row["path"] == CLAIM_TEXT_PATHS[0] and row["line_start"] == 132)
        row["claim_type"] = "PROSE_PROPOSITION"
    cases.append((NEGATIVE_IDS[20], omit_tikz))
    def split_multiline(d: dict[str, Any]) -> None:
        row = next(row for row in d["source_claim_manifest"]
                   if row["path"] == CLAIM_TEXT_PATHS[1] and row["line_start"] == 64)
        row["line_end"] = 64
        lines = decoded_lines(git_bytes(BASELINE, CLAIM_TEXT_PATHS[1]))
        text = lines[63]
        row["anchor"].update(line_end=64, anchor_text=text,
                             slice_sha256=sha256((text + "\n").encode("utf-8")))
    cases.append((NEGATIVE_IDS[21], split_multiline))
    def promote_ab_to_c(d: dict[str, Any]) -> None:
        claim = next(row for row in d["source_claim_manifest"]
                     if row["path"] == CLAIM_TEXT_PATHS[1] and row["line_start"] == 64)
        claim["evidence_tier"] = "TIER_C_MODEL"
        next(row for row in d["scope_matrix"] if row["source_claim_id"] == claim["source_claim_id"])["evidence_tier"] = "TIER_C_MODEL"
    cases.append((NEGATIVE_IDS[22], promote_ab_to_c))
    def delete_unit(d: dict[str, Any]) -> None:
        claim = next(row for row in d["source_claim_manifest"]
                     if row["path"] == CLAIM_TEXT_PATHS[2]
                     and any(obs.get("normalized_numeric") == 4958.0 for obs in row["numeric_observations"]))
        observation = next(obs for obs in claim["numeric_observations"] if obs.get("normalized_numeric") == 4958.0)
        observation["normalized_unit"] = None
        claim["normalized_units"].remove("J/mol")
        scoped = next(row for row in d["scope_matrix"] if row["source_claim_id"] == claim["source_claim_id"])
        next(obs for obs in scoped["value"] if obs.get("normalized_numeric") == 4958.0)["normalized_unit"] = None
        scoped["unit"].remove("J/mol")
    cases.append((NEGATIVE_IDS[23], delete_unit))
    def leak_cite_key_digits(d: dict[str, Any]) -> None:
        adopted = next(row for row in d["source_claim_manifest"] if "beaulieu2001" in row["citation_keys"])
        ledger = next(row for row in d["source_claim_manifest"]
                      if row["source_surface"] == "LEDGER_SELF_REPORT" and "wen_huggins1981" in row["claim_text"])
        for claim, token, value in ((adopted, "001", 1.0), (ledger, "981", 981.0)):
            fake = {"raw_token":token, "normalized_numeric":value, "approximation":False,
                    "raw_unit":None, "normalized_unit":None}
            claim["numeric_observations"].append(fake)
            next(row for row in d["scope_matrix"] if row["source_claim_id"] == claim["source_claim_id"])["value"].append(copy.deepcopy(fake))
    cases.append((NEGATIVE_IDS[24], leak_cite_key_digits))
    cases.append((NEGATIVE_IDS[25],[
        lambda d:d["bibliography_audit"]["rows"][0].__setitem__("frozen_doi","10.0/fake"),
        lambda d:d["bibliography_audit"]["rows"][0].__setitem__("frozen_entry","FAKE"),
    ]))
    cases.append((NEGATIVE_IDS[26],lambda d:d["provenance"].__setitem__("q7_commit","0"*40)))
    cases.append((NEGATIVE_IDS[27],lambda d:d["source_attestations"][0].__setitem__("decoding","CP949_REPLACE")))
    if [case_id for case_id, _ in cases] != NEGATIVE_IDS:
        fail("negative case identity/order mismatch")
    passed: list[str] = []
    for case_id, fixture in cases:
        mutators = fixture if isinstance(fixture, list) else [fixture]
        for subfixture, mutator in enumerate(mutators, 1):
            clone = copy.deepcopy(data); mutator(clone)
            if case_id != "SEMANTIC_DIGEST_TAMPER": refresh_digest(clone)
            observed = singleton_diagnostics(clone, case_id)
            if observed != {case_id}:
                fail(f"negative {case_id}[{subfixture}/{len(mutators)}]: observed={sorted(observed)}")
        passed.append(case_id)
    return passed


def validate_markdown_and_controls(data: dict[str, Any]) -> None:
    result = RESULT.read_text(encoding="utf-8")
    tokens = ["# Phase 062 Step 54","Status: **PASS_WITH_CONCERNS**",
        "Gate: `PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS`","Frozen material bibliography: **28/28** rows",
        "**482 / 482** rows, exact 1:1 claim-to-scope bijection",
        "Adopted release text contributes **439** claim atoms",
        "**28/28 contract cases**","Validator-only staged/index and CRLF identity boundary controls: **2/2**","1.1 k_B/atom model gate integral",
        "0.18 k_B/atom O3 total partial-molar quantity","P062_STEP54_RESULT_FIRST_PRECOMMIT",
        "PENDING_AT_PRECOMMIT_BY_DESIGN","Step 55 remains blocked until `PASS_P062_STEP54_PERSISTENCE`",
        "External scientific truth validated: **false**",data["semantic_sha256"],data["builder_sha256"]]
    for token in tokens:
        if result.count(token) != 1:
            fail(f"result token cardinality: {token}")
    docs = {PARENT_LEDGER.name:PARENT_LEDGER.read_text(encoding="utf-8"),
            ACTIVE_LEDGER.name:ACTIVE_LEDGER.read_text(encoding="utf-8"),
            HANDOVER.name:HANDOVER.read_text(encoding="utf-8")}
    required = {
        PARENT_LEDGER.name:["| 062 | 52–57 |","source claims `482`","atomic scope `482` with exact 1:1 bijection","GNF `17`","required mutation controls `28`","boundary controls `2/2`","P062_STEP54_RESULT_FIRST_PRECOMMIT"],
        ACTIVE_LEDGER.name:["| 062 | 52–57 |","| Step 54 |","source claims 482","atomic scope 482 with exact 1:1 bijection","required actual-mutation controls `28/28`","boundary controls `2/2`","P062_STEP54_RESULT_FIRST_PRECOMMIT"],
        HANDOVER.name:["Current checkpoint: Step 54 precommit Gate","PHASE_062_STEP_054_LCO_SI_SCOPE_RESULT.md","PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json",f"exact-seven commit `{EXPECTED_PARENT}` pushed and remote-verified","| Phase 062 Step 54 | Step 54 |","source claims `482` (adopted text `439` + bibliography `28` + ledger self-report `15`), atomic scope `482` with exact 1:1 bijection","required actual-mutation controls `28/28`","boundary controls `2/2`"],
    }
    for name, tokens in required.items():
        for token in tokens:
            expected_count = 1
            if name == ACTIVE_LEDGER.name and token in {"P062_STEP54_RESULT_FIRST_PRECOMMIT", "boundary controls `2/2`"}:
                expected_count = 2
            if name == HANDOVER.name and token == "boundary controls `2/2`":
                expected_count = 2
            if docs[name].count(token) != expected_count:
                fail(f"control {name} token cardinality: {token}")
        if any(stale in docs[name] for stale in (
            "scope rows `50`", "scope rows 50", "scope `50`", "scope 50",
            "source claims `1108`", "source claims 1108", "adopted text `1065`",
            "required mutation controls `19`", "required actual-mutation controls `19/19`",
            "required mutation controls `25`", "required actual-mutation controls `25/25`",
        )):
            fail(f"control {name} stale scope denominator")
    if "Phase 062 Step 53 | Step 53 | precommit" in docs[HANDOVER.name]:
        fail("handover stale Step 53 precommit row")


def changed_paths() -> set[str]:
    paths: set[str] = set()
    for args in (("diff","--name-only"),("diff","--cached","--name-only"),("ls-files","--others","--exclude-standard")):
        paths.update(line for line in run_git(*args).splitlines() if line)
    return paths


def staged_index_diagnostics(cached: set[str], unstaged: set[str]) -> set[str]:
    errors: set[str] = set()
    if cached != EXACT_PATHS:
        errors.add("STAGED_EXACT_SEVEN_MISMATCH")
    if unstaged:
        errors.add("STAGED_WORKTREE_INDEX_DIVERGENCE")
    return errors


def run_boundary_controls() -> list[str]:
    staged_code = "STAGED_WORKTREE_INDEX_DIVERGENCE"
    if staged_index_diagnostics(set(EXACT_PATHS), set()):
        fail("boundary clean staged state rejected")
    staged_observed = staged_index_diagnostics(set(EXACT_PATHS), {next(iter(EXACT_PATHS))})
    if staged_observed != {staged_code}:
        fail(f"boundary staged singleton mismatch: {sorted(staged_observed)}")

    raw = BUILDER.read_bytes()
    normalized = lf_normalized_bytes(raw)
    crlf = normalized.replace(b"\n", b"\r\n")
    if (lf_sha256(raw) != lf_sha256(crlf)
            or ast.dump(ast.parse(normalized.decode("utf-8", "strict")), include_attributes=False)
            != ast.dump(ast.parse(lf_normalized_bytes(crlf).decode("utf-8", "strict")), include_attributes=False)
            or lf_sha256(normalized + b"# semantic mutation\n") == lf_sha256(raw)):
        fail("boundary CRLF-equivalent identity mismatch")
    return [staged_code, "CRLF_EQUIVALENT_BUILDER_IDENTITY"]


def validate_git_state(mode: str, staged: bool) -> None:
    if run_git("branch","--show-current") != BRANCH: fail("active branch mismatch")
    head = run_git("rev-parse","HEAD")
    if run_git("rev-parse","origin/codex/lib-physics-endgame-v1025_2") != PROTECTED_TIP or run_git("rev-parse","origin/main") != MAIN_TIP:
        fail("local protected/main tip drift")
    if run_git("diff","--name-only",PROTECTED_TIP,"--","Claude") or run_git("ls-files","--others","--exclude-standard","--","Claude"):
        fail("Claude boundary drift")
    if mode == "precommit":
        if head != EXPECTED_PARENT: fail(f"precommit parent mismatch: {head}")
        observed = changed_paths()
        if observed != EXACT_PATHS: fail(f"precommit exact-seven dirt mismatch: {sorted(observed ^ EXACT_PATHS)}")
        if run_git("diff","--check"): fail("working diff check failed")
        if staged:
            cached = {line for line in run_git("diff","--cached","--name-only").splitlines() if line}
            unstaged = {line for line in run_git("diff","--name-only").splitlines() if line}
            staged_errors = staged_index_diagnostics(cached, unstaged)
            if staged_errors: fail(f"staged state diagnostics: {sorted(staged_errors)}")
            if run_git("diff","--cached","--check"): fail("cached diff check failed")
    else:
        if run_git("show","-s","--format=%s","HEAD") != SUBJECT or run_git("rev-parse","HEAD^") != EXPECTED_PARENT:
            fail("persistence subject/parent mismatch")
        committed = {line for line in run_git("diff-tree","--no-commit-id","--name-only","-r","HEAD").splitlines() if line}
        if committed != EXACT_PATHS: fail(f"persistence exact-seven mismatch: {sorted(committed ^ EXACT_PATHS)}")
        if run_git("status","--porcelain=v1"): fail("persistence worktree not clean")
        upstream = run_git("rev-parse","@{upstream}")
        live = subprocess.run(["git","ls-remote","origin",f"refs/heads/{BRANCH}"],cwd=ROOT,check=False,
            capture_output=True,text=True,encoding="utf-8",errors="strict",timeout=30)
        remote = live.stdout.split()[0] if live.returncode == 0 and live.stdout.split() else ""
        if not (head == upstream == remote): fail("local/upstream/live-origin mismatch")
        for ref, expected in (("codex/lib-physics-endgame-v1025_2",PROTECTED_TIP),("main",MAIN_TIP)):
            p = subprocess.run(["git","ls-remote","origin",f"refs/heads/{ref}"],cwd=ROOT,check=False,
                capture_output=True,text=True,encoding="utf-8",errors="strict",timeout=30)
            observed = p.stdout.split()[0] if p.returncode == 0 and p.stdout.split() else ""
            if observed != expected: fail(f"live protected drift: {ref}")


def run_builder_determinism() -> int:
    validate_builder_boundary()
    for attempt in range(2):
        proc = subprocess.run([sys.executable,str(BUILDER),"--check"],cwd=ROOT,check=False,
            capture_output=True,text=True,encoding="utf-8",errors="strict",timeout=90)
        if proc.returncode or "PASS_P062_STEP54_DETERMINISM outputs=2/2 result_first=RESULT_THEN_JSON" not in proc.stdout:
            fail(f"builder determinism {attempt+1} failed: {proc.stdout.strip()} {proc.stderr.strip()}")
    return 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",choices=("precommit","persistence"),default="precommit")
    parser.add_argument("--staged",action="store_true")
    args = parser.parse_args()
    try:
        for path in (ARTIFACT,RESULT,BUILDER,PARENT_LEDGER,ACTIVE_LEDGER,HANDOVER):
            if not path.is_file(): fail(f"missing surface: {path.relative_to(ROOT).as_posix()}")
        validate_builder_boundary()
        raw = ARTIFACT.read_bytes(); data = strict_json(raw)
        if canonical_bytes(data) != raw: fail("artifact not canonical UTF-8 LF JSON")
        validate_source_attestations(data)
        errors = content_diagnostics(data)
        if errors: fail(f"content diagnostics: {sorted(errors)}")
        validate_markdown_and_controls(data)
        validate_git_state(args.mode,args.staged)
        passed = run_negative_controls(data)
        boundary = run_boundary_controls()
        determinism = run_builder_determinism()
        topology = traversal(data)
        for case_id in passed: print(f"PASS negative={case_id}")
        print(f"PASS_P062_STEP54_NEGATIVE_CONTROLS {len(passed)}/28 singleton=true subfixtures=34")
        print(f"PASS_P062_STEP54_BOUNDARY_CONTROLS {len(boundary)}/2 staged_index=true crlf_identity=true")
        print(f"PASS_P062_STEP54_DETERMINISM {determinism}/2 result_first=RESULT_THEN_JSON")
        print("PASS_P062_STEP54_CONTENT bibliography=28/28 citations=72 source_claims=482 adopted_text=439 bibliography_claims=28 ledger_claims=15 scope=482 bijection=true gnf=17")
        print(f"PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS mode={args.mode} json_nodes={topology['nodes']} max_depth={topology['max_depth']}")
        if args.mode == "persistence": print("PASS_P062_STEP54_PERSISTENCE")
        return 0
    except (ValidationError,KeyError,TypeError,ValueError,json.JSONDecodeError,subprocess.TimeoutExpired) as exc:
        print(f"FAIL_P062_STEP54: {exc}",file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
