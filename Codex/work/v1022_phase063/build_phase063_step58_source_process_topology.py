#!/usr/bin/env python3
"""Build Phase 063 Step 58 source/process topology and full-read attestation."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import posixpath
import re
import subprocess
from collections import Counter, defaultdict
from io import BytesIO
from pathlib import Path
from typing import Any

from pypdf import PdfReader


REPO = Path(__file__).resolve().parents[3]
BUILDER = Path(__file__).resolve()
MANIFEST = REPO / "Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json"
INTENT = REPO / "Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json"
TOPOLOGY = REPO / "Codex/results/PHASE_063_V1022_SOURCE_PROCESS_TOPOLOGY.json"
ATTESTATION = REPO / "Codex/results/PHASE_063_V1022_READ_ATTESTATION.json"
RESULT = REPO / "Codex/results/PHASE_063_STEP_058_SOURCE_PROCESS_TOPOLOGY_RESULT.md"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
ACTIVATION_COMMIT = "4e7686ec623a2e82a0ef5433e60a8565b0ad039f"
MANIFEST_SHA256 = "60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef"
SUPPLEMENTAL_PATH = "Claude/plans/2026-07-17-v1022-master-plan.md"
SUPPLEMENTAL_BLOB = "f50deee51df77dca8d07a2d9b9fd150fa93309cc"
GIT_TIMEOUT = 120
HUMAN_EVIDENCE_BEGIN = "<!-- P063_STEP58_HUMAN_EVIDENCE_BEGIN -->"
HUMAN_EVIDENCE_END = "<!-- P063_STEP58_HUMAN_EVIDENCE_END -->"

CROSS_VERSION_RELATIONS: tuple[dict[str, Any], ...] = (
    {
        "relation_id": "P063-XVER-001",
        "relation": "RENAMED",
        "v1021_relative_paths": ["Anode_Fit_v1.0.21.py"],
        "v1022_relative_paths": ["Anode_Fit_v1.0.22.py"],
        "process_evidence": [{"path": "Claude/docs/v1.0.22/plans/PLAN_R1_reorg.md", "line_intervals": [[30, 30]]}],
        "basis": "The frozen reorganization plan explicitly identifies the copied v1.0.22 code successor.",
        "authority_ceiling": "REPOSITORY_REPORTED_VERSIONED_SUCCESSOR_ONLY",
    },
    {
        "relation_id": "P063-XVER-002",
        "relation": "RENAMED",
        "v1021_relative_paths": ["results/snapshot_v1021_q7.json"],
        "v1022_relative_paths": ["results/snapshot_v1022_r1.json"],
        "process_evidence": [{"path": "Claude/docs/v1.0.22/plans/PLAN_RA_lineage_audit.md", "line_intervals": [[8, 8]]}],
        "basis": "The frozen lineage-audit plan explicitly records the q7-to-r1 snapshot chain; the builder also records both frozen blobs.",
        "authority_ceiling": "REPOSITORY_REPORTED_VERSIONED_SNAPSHOT_SUCCESSOR_ONLY",
    },
    {
        "relation_id": "P063-XVER-003",
        "relation": "SPLIT",
        "v1021_relative_paths": ["graphite_ica_ch1_v1.0.21.tex", "graphite_ica_ch2_v1.0.21.tex"],
        "v1022_relative_paths": ["ch1_graphite_v1.0.22.tex", "ch2_lco_v1.0.22.tex", "ch3_si_v1.0.22.tex"],
        "process_evidence": [{"path": "Claude/docs/v1.0.22/plans/PLAN_R1_reorg.md", "line_intervals": [[11, 12], [15, 30], [50, 57]]}],
        "basis": "The frozen movement and historical-name tables reassemble two old drivers into three material-centered drivers; this is a source-topology split/restructure, not a byte rename.",
        "authority_ceiling": "REPOSITORY_REPORTED_SOURCE_RESTRUCTURE_ONLY",
    },
    {
        "relation_id": "P063-XVER-004",
        "relation": "SPLIT",
        "v1021_relative_paths": ["_sections/ch1_bib.tex", "_sections/ch2_bib.tex"],
        "v1022_relative_paths": ["_sections/ch1v22_bib.tex", "_sections/ch2v22_bib.tex", "_sections/ch3v22_bib.tex"],
        "process_evidence": [{"path": "Claude/docs/v1.0.22/plans/PLAN_R1_reorg.md", "line_intervals": [[26, 29], [41, 43]]}],
        "basis": "The frozen plan explicitly redistributes the two old chapter bibliographies into three self-contained chapter bibliographies.",
        "authority_ceiling": "REPOSITORY_REPORTED_BIBLIOGRAPHY_RESTRUCTURE_ONLY",
    },
)

OBSERVATIONS = (
    ("P063-OBS-001", "Codex/results/PHASE_057P_V1022_R1_CONTROL_AND_LINEAGE_OBSERVATIONS.md", 214, "0d67dcfa3bbce07f82b5530db699b3795110ea4a2b351a980657191262abaa10"),
    ("P063-OBS-002", "Codex/results/PHASE_057Q_V1022_R1_SNAPSHOT_OBSERVATIONS.md", 130, "d6ed22e77a4d83f33b039de602f8a91d33cbd7f7ee5518ba994403ea78d83513"),
    ("P063-OBS-003", "Codex/results/PHASE_057R_V1022_R2_CH1_COMPLETION_OBSERVATIONS.md", 173, "2be5735eb8bb8b7109a705de0ed7875cbab7586e7fca1eefc2080eb8ef85d0ba"),
    ("P063-OBS-004", "Codex/results/PHASE_057S_V1022_R3_LCO_COMPLETION_OBSERVATIONS.md", 166, "7994051df9c1f4beeb3707b4d57e59da9a31161c1a7d7ca53faa5545f2524d68"),
    ("P063-OBS-005", "Codex/results/PHASE_057T_V1022_R4_MATERIAL_SURVEY_OBSERVATIONS.md", 201, "5fe61fe155bc5136afa18cda999a853a1f865b1f2e5c7c50ad19b533f74ecb6a"),
    ("P063-OBS-006", "Codex/results/PHASE_057U_V1022_R5_RV_SM2_OBSERVATIONS.md", 214, "038f2c2e0b8e827e5c21a9907f2be881e1309fc43a75ca141654377bff69c7b3"),
    ("P063-OBS-007", "Codex/results/PHASE_057V_V1022_FR_A01_A08_A20_OBSERVATIONS.md", 284, "3f67eae26afe10e2c0febdac882d636cd928ab0dbb8c76b6050c56d8cefd7abc"),
    ("P063-OBS-008", "Codex/results/PHASE_057W_V1022_FR_A09_A16_OBSERVATIONS.md", 241, "7b00318e9bc7996f68e2bec53bfbe34bf570eb4b7d3f6e52bba87955e6cf7eb3"),
    ("P063-OBS-009", "Codex/results/PHASE_057X_V1022_FR_A17_A19_A21_A23_OBSERVATIONS.md", 283, "f84dbd3357fc622a2a3f6adc195f179b63ef970bb72a9a3b782c6290b0e69d49"),
    ("P063-OBS-010", "Codex/results/PHASE_057Y_V1022_FR_CONTROL_TRIAGE_EXEC_OBSERVATIONS.md", 198, "bdffda0188bef7e395934f704655ad97d97caccbf3d54fe71b602445be55ccce"),
    ("P063-OBS-011", "Codex/results/PHASE_057Z_V1022_R6_R9_AUD_V23_SURVEY_OBSERVATIONS.md", 259, "79d82adccb8b83878250a4306407a059c21a530dc4ab7f5090718586bc9e2632"),
)

PROCESS_FINDINGS: tuple[dict[str, Any], ...] = (
    {
        "finding_id": "P063-PROC-001",
        "evidence": [{"path": "Claude/plans/2026-07-17-v1022-master-plan.md", "line_intervals": [[3, 3], [47, 47], [64, 64], [74, 74], [95, 95]]}],
        "classification": "PROCESS_RULE",
        "finding": "The supplemental plan repeatedly forbids a merge build; the later trial-merge build wording is repository-reported process history and cannot override those explicit D22-8 boundaries.",
        "authority_ceiling": "REPOSITORY_REPORTED_PROCESS_CONTROL_ONLY",
        "downstream_owner": "Phase 063 Step 62 state/build closure",
    },
    {
        "finding_id": "P063-PROC-002",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/MERGE_READINESS.md", "line_intervals": [[1, 4], [21, 21], [204, 204]]}],
        "classification": "STALE_SELF_REPORT_CONFLICT",
        "finding": "The heading says master-confirmed while the status, conclusion, and footer still identify a draft; this document is not a single unambiguous final-state authority.",
        "authority_ceiling": "SELF_REPORT_AS_OF_LAST_TOUCH_ONLY",
        "downstream_owner": "Phase 063 Step 62 state chronology",
    },
    {
        "finding_id": "P063-PROC-003",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/MERGE_READINESS.md", "line_intervals": [[168, 169]]},
            {"path": "Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md", "line_intervals": [[97, 97], [143, 143]]},
        ],
        "classification": "STALE_PENDING_AFTER_RECORDED_COMPLETION",
        "finding": "MERGE_READINESS retains moyassari_blend2022 as pending, HANDOVER records it complete, and the same HANDOVER later reintroduces a conditional future state.",
        "authority_ceiling": "CONFLICTING_PROCESS_SELF_REPORT_ONLY",
        "downstream_owner": "Phase 063 Step 62 proposal/adoption/state closure",
    },
    {
        "finding_id": "P063-PROC-004",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/HANDOVER_v1.0.22.md", "line_intervals": [[23, 23], [43, 43], [147, 147]]}],
        "classification": "STALE_DRAFT_STATUS",
        "finding": "R9 is described as in progress and the document remains a draft despite later source-history touches; current completion cannot be inferred from this self-report alone.",
        "authority_ceiling": "SELF_REPORT_AS_OF_LAST_TOUCH_ONLY",
        "downstream_owner": "Phase 063 Step 62 state chronology",
    },
    {
        "finding_id": "P063-PROC-005",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/INDEX_v1022.md", "line_intervals": [[4, 5], [142, 146]]}],
        "classification": "STALE_INVENTORY_SELF_REPORT",
        "finding": "The index claims an all-results inventory of 127 files including a pyc cache, but later comp_AUD/v23 history is outside that as-of inventory and the cache is not in the frozen manifest.",
        "authority_ceiling": "HISTORICAL_INDEX_SELF_REPORT_ONLY",
        "downstream_owner": "Phase 063 Step 62 state chronology",
    },
    {
        "finding_id": "P063-PROC-006",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/AUDIT_LINEAGE_v19_v22.md", "line_intervals": [[7, 7], [33, 39], [59, 59]]}],
        "classification": "AUDIT_SCOPE_CEILING",
        "finding": "The audit reports zero unlogged loss while explicitly excluding an exhaustive prose reread; its conclusion is audit self-report constrained by its stated method, not direct full-prose proof.",
        "authority_ceiling": "INTERNAL_AUDIT_SELF_REPORT_ONLY",
        "downstream_owner": "Phase 063 Step 62 review/adoption closure",
    },
    {
        "finding_id": "P063-PROC-007",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/V1022_EXECUTION_LEDGER.md", "line_intervals": [[23, 23]]},
            {"path": "Claude/docs/v1.0.22/results/MERGE_READINESS.md", "line_intervals": [[17, 17]]},
        ],
        "classification": "PROCEDURE_COUNT_CONFLICT",
        "finding": "The execution ledger describes a five-stage merge procedure while MERGE_READINESS summarizes four stages.",
        "authority_ceiling": "CONFLICTING_PROCESS_SELF_REPORT_ONLY",
        "downstream_owner": "Phase 063 Step 62 state/build closure",
    },
)

RELEASE_FINDINGS: tuple[dict[str, Any], ...] = (
    {
        "finding_id": "P063-REL-001",
        "evidence": [{"path": "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "line_intervals": [[3, 9]]}],
        "classification": "STALE_VERSION_HEADER",
        "finding": "The v1.0.22 code file still identifies its release/matched version as v1.0.21 and points its regression narrative at test_gates_v1021.py.",
        "authority_ceiling": "STATIC_SOURCE_OBSERVATION_ONLY",
        "downstream_owner": "Phase 063 Step 61 code/runtime concordance",
    },
    {
        "finding_id": "P063-REL-002",
        "evidence": [{"path": "Claude/docs/v1.0.22/FITTING_GUIDE.md", "line_intervals": [[1, 5], [119, 126]]}],
        "classification": "STALE_VERSION_GUIDE",
        "finding": "The guide remains headed and scoped as v1.0.20 and later describes a v1.0.19 validation suite rather than the frozen v1.0.22 release surface.",
        "authority_ceiling": "STATIC_SOURCE_OBSERVATION_ONLY",
        "downstream_owner": "Phase 063 Step 61 code/runtime concordance",
    },
    {
        "finding_id": "P063-REL-003",
        "evidence": [{"path": "Claude/docs/v1.0.22/_sections/ch1_appB_codemap.tex", "line_intervals": [[4, 8]]}],
        "classification": "STALE_IMPLEMENTATION_REFERENCE",
        "finding": "The designated implementation appendix maps the document to Anode_Fit_v1.0.21.py rather than the frozen v1.0.22 path.",
        "authority_ceiling": "STATIC_SOURCE_OBSERVATION_ONLY",
        "downstream_owner": "Phase 063 Step 61 code/runtime concordance",
    },
    {
        "finding_id": "P063-REL-004",
        "evidence": [{"path": "Claude/docs/v1.0.22/test_gates_v1022.py", "line_intervals": [[35, 35], [48, 48], [603, 605]]}],
        "classification": "STALE_TEST_IDENTITY_LABEL",
        "finding": "The v1.0.22 test names v1020 in its reproduction instruction, local variable, and imported module label even though the path targets Anode_Fit_v1.0.22.py.",
        "authority_ceiling": "STATIC_SOURCE_OBSERVATION_ONLY",
        "downstream_owner": "Phase 063 Step 61 code/runtime concordance",
    },
    {
        "finding_id": "P063-REL-005",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py", "line_intervals": [[601, 617]]},
            {"path": "Claude/docs/v1.0.22/_sections/ch1_sec10_sum.tex", "line_intervals": [[55, 55]]},
        ],
        "classification": "TIME_UNIT_SEAM",
        "finding": "The code-facing path declares C-rate in h^-1 and computes I=cQ, while the thermal prose describes the numerical C-rate as s^-1 and separately states a 3600 SI conversion.",
        "authority_ceiling": "STATIC_CONCORDANCE_OBSERVATION_ONLY",
        "downstream_owner": "Phase 063 Step 59 dimensional rederivation and Step 61 runtime delta",
    },
    {
        "finding_id": "P063-REL-006",
        "evidence": [{"path": "Claude/docs/v1.0.22/_sections/ch3v22_sec05_code.tex", "line_intervals": [[1, 70]]}],
        "classification": "MAIN_BODY_CODE_MENTION_BOUNDARY",
        "finding": "The included Chapter 3 main-body section 3.5 is an implementation requirement specification rather than a designated appendix/companion surface.",
        "authority_ceiling": "STATIC_AND_RENDERED_LAYOUT_OBSERVATION_ONLY",
        "downstream_owner": "Phase 063 Step 62 code-mention boundary and Phase 088 final manuscript policy",
    },
    {
        "finding_id": "P063-REL-007",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/_sections/ch1_appD_si.tex", "line_intervals": []},
            {"path": "Claude/docs/v1.0.22/_sections/ch1_preamble.tex", "line_intervals": []},
            {"path": "Claude/docs/v1.0.22/_sections/ch2_preamble.tex", "line_intervals": []},
        ],
        "classification": "UNREACHED_TEX_SOURCE",
        "finding": "These three TeX sources are manifest members but are not reached by any frozen driver input/include edge; intent to retain or discard is ground-not-found at Step 58.",
        "authority_ceiling": "STATIC_DEPENDENCY_TOPOLOGY_ONLY",
        "downstream_owner": "Phase 063 Step 62 build/state closure",
    },
    {
        "finding_id": "P063-REL-008",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/ch1_graphite_v1.0.22.tex", "line_intervals": []},
            {"path": "Claude/docs/v1.0.22/ch2_lco_v1.0.22.tex", "line_intervals": []},
            {"path": "Claude/docs/v1.0.22/ch3_si_v1.0.22.tex", "line_intervals": []},
        ],
        "classification": "CITATION_CLOSURE_OBSERVATION",
        "finding": "Frozen source closure is 39/39, 15/15, and 34/34 cited-to-defined keys for Chapters 1–3 with no missing, unused, or duplicate keys; this is structural closure, not literature truth.",
        "authority_ceiling": "STATIC_BIBLIOGRAPHY_STRUCTURE_ONLY",
        "downstream_owner": "Phase 063 Step 60 literature authority",
    },
    {
        "finding_id": "P063-REL-009",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/_sections/ch2v22_bib.tex", "line_intervals": [[2, 2]]},
            {"path": "Claude/docs/v1.0.22/_sections/ch3v22_bib.tex", "line_intervals": [[2, 2]]},
        ],
        "classification": "STALE_BIBLIOGRAPHY_COUNT_COMMENT",
        "finding": "The bibliography header comments retain stale counts while the parsed frozen closures contain 15 and 34 keys.",
        "authority_ceiling": "STATIC_SOURCE_OBSERVATION_ONLY",
        "downstream_owner": "Phase 063 Step 60 literature authority",
    },
    {
        "finding_id": "P063-REL-010",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/appendix_phase_separation.pdf", "line_intervals": []},
            {"path": "Claude/docs/v1.0.22/ch1_graphite_v1.0.22.pdf", "line_intervals": []},
            {"path": "Claude/docs/v1.0.22/ch2_lco_v1.0.22.pdf", "line_intervals": []},
            {"path": "Claude/docs/v1.0.22/ch3_si_v1.0.22.pdf", "line_intervals": []},
        ],
        "classification": "PDF_REPRODUCIBILITY_CEILING",
        "finding": "All four frozen PDFs render and expose text on every page, but no cryptographic clean-build reproducibility proof exists at Step 58 and all four documents are untagged.",
        "authority_ceiling": "FROZEN_PDF_VISUAL_AND_METADATA_ONLY",
        "downstream_owner": "Phase 063 Step 62 clean build/page genealogy",
    },
)

ORPHAN_TEX_PATHS = (
    "Claude/docs/v1.0.22/_sections/ch1_appD_si.tex",
    "Claude/docs/v1.0.22/_sections/ch1_preamble.tex",
    "Claude/docs/v1.0.22/_sections/ch2_preamble.tex",
)

COMPETING_FINDINGS: tuple[dict[str, Any], ...] = (
    {
        "finding_id": "P063-COMP-001",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_R2/CHERRYPICK_R2.md", "line_intervals": [[20, 25]]},
            {"path": "Claude/docs/v1.0.22/results/comp_R2/B_bridges/BRIDGE_DRAFTS.md", "line_intervals": [[67, 71]]},
            {"path": "Claude/docs/v1.0.22/results/comp_R2/B_bridges/BRIDGE_RISK.md", "line_intervals": [[36, 39]]},
        ],
        "classification": "DECISION_WITH_UNVERIFIED_PRIMARY_EQUATION",
        "finding": "A bridge-adoption decision coexists with explicit nonverification of the Dreyer, McKinnon, and Bernardi primary equations and equation numbers.",
        "authority_ceiling": "DECISION_AND_CANDIDATE_RECORD_ONLY",
        "phase057_links": ["INTENT-PROV-0112", "INTENT-PROV-0121"],
        "downstream_owner": "Step 60 primary-source adjudication and Step 62 source adoption",
    },
    {
        "finding_id": "P063-COMP-002",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_R3/E_bridges/L5_CHARGEORDER_CHECK.md", "line_intervals": [[22, 29]]},
            {"path": "Claude/docs/v1.0.22/results/comp_R3/CHERRYPICK_R3.md", "line_intervals": [[19, 22]]},
        ],
        "classification": "UNVERIFIED_QUANTITY_AND_SCOPE_MISMATCH",
        "finding": "The 0.47/1.49 J mol^-1 K^-1 values lack primary-text confirmation and retain spin/configurational-category and x=2/3 composition mismatches under a tier-C label.",
        "authority_ceiling": "CANDIDATE_AND_DECISION_RECORD_ONLY",
        "phase057_links": ["INTENT-PROV-0122", "INTENT-PROV-0129"],
        "downstream_owner": "Step 59 LCO thermodynamics and Step 60 literature/quantity authority",
    },
    {
        "finding_id": "P063-COMP-003",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_R4/L2_REGISTER_PREP.md", "line_intervals": [[109, 124]]},
            {"path": "Claude/docs/v1.0.22/results/comp_R4/REPORT_R4_COMPLETE.md", "line_intervals": [[40, 54]]},
        ],
        "classification": "REFERENCE_COMPLETION_CONFLICT",
        "finding": "A requirement to verify all authors conflicts with the later report's claim that the bibliography is fully confirmed and complete.",
        "authority_ceiling": "REVIEW_AND_SELF_REPORT_ONLY",
        "phase057_links": ["INTENT-PROV-0128"],
        "downstream_owner": "Step 60 reference-ledger adjudication",
    },
    {
        "finding_id": "P063-COMP-004",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/comp_R4/REPORT_R4_COMPLETE.md", "line_intervals": [[116, 125]]}],
        "classification": "SELF_REPORTED_EXTENT_MISMATCH",
        "finding": "Reported line counts 145/98/142/186/165 disagree with the frozen manifest extents 122/110/122/176/169.",
        "authority_ceiling": "SELF_REPORT_ONLY",
        "phase057_links": ["INTENT-PROV-0105", "INTENT-PROV-0124"],
        "downstream_owner": "Step 58 process identity; preserved as a resolved topology observation",
    },
    {
        "finding_id": "P063-COMP-005",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_R4/BLEND_ALIGN.md", "line_intervals": [[47, 47], [102, 107]]},
            {"path": "Claude/docs/v1.0.22/results/comp_R4/upgraded/BLEND_UP.md", "line_intervals": [[31, 38]]},
        ],
        "classification": "SURVEY_RESULT_AND_RANGE_CONFLICT",
        "finding": "A zero-document survey result is later replaced by eight documents, while [0,20] union {30} wt% is overstated as a full continuous interval.",
        "authority_ceiling": "REVIEW_SURVEY_ONLY",
        "phase057_links": ["INTENT-PROV-0102", "INTENT-PROV-0125", "INTENT-PROV-0127"],
        "downstream_owner": "Step 60 literature-range adjudication",
    },
    {
        "finding_id": "P063-COMP-006",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_R5/W1/s35_code.tex", "line_intervals": [[13, 19]]},
            {"path": "Claude/docs/v1.0.22/results/comp_R6/R6_REPORT.md", "line_intervals": [[21, 23]]},
            {"path": "Claude/docs/v1.0.22/results/comp_FR/A21_REVIEW.md", "line_intervals": [[74, 90]]},
            {"path": "Claude/docs/v1.0.22/results/comp_FR/A22_REVIEW.md", "line_intervals": [[60, 87]]},
        ],
        "classification": "MASS_CAPACITY_FRACTION_SCOPE_CONFLICT",
        "finding": "A capacity-fraction sweep f_Si in [0,0.3] cannot cover the cited 10–30 wt% anchors; the report also maps 30 wt% to 0.782 while describing the covered capacity-fraction range as approximately 0–0.7.",
        "authority_ceiling": "CANDIDATE_SELF_REPORT_AND_REVIEW_ONLY",
        "phase057_links": ["INTENT-PROV-0101", "INTENT-PROV-0136", "INTENT-PROV-0169"],
        "downstream_owner": "Step 59 composition closure, Step 60 evidence scope, and Step 61 runtime concordance",
    },
    {
        "finding_id": "P063-COMP-007",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_R5/W1/s35_code.tex", "line_intervals": [[46, 50]]},
            {"path": "Claude/docs/v1.0.22/results/comp_R6/R6_REPORT.md", "line_intervals": [[184, 192]]},
            {"path": "Claude/docs/v1.0.22/results/comp_R7/F2_NOTE.md", "line_intervals": [[68, 88]]},
            {"path": "Claude/docs/v1.0.22/results/comp_R7/F2_si_cases.tex", "line_intervals": [[59, 65]]},
        ],
        "classification": "SIOX_PLACEHOLDER_AND_MODEL_GAP",
        "finding": "SiO_x U=0.300 V and width 0.090 V are placeholder/demo values; entropy and finite-rate host switching remain unimplemented model gaps.",
        "authority_ceiling": "CANDIDATE_AND_SELF_REPORT_ONLY",
        "phase057_links": ["INTENT-PROV-0138", "INTENT-PROV-0183", "INTENT-PROV-0184", "INTENT-PROV-0185", "INTENT-PROV-0186"],
        "downstream_owner": "Step 59 SiO_x physics and Step 60 primary-data authority",
    },
    {
        "finding_id": "P063-COMP-008",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/comp_AUD/AUD2_CH2.md", "line_intervals": [[36, 49]]}],
        "classification": "COMMENT_RUNTIME_AND_RANGE_DRIFT",
        "finding": "Comment values xi=0.45/0.93 differ from runtime 0.4443/0.9567, and [0,20] union {30} wt% is called a full interval.",
        "authority_ceiling": "REVIEW_RECORD_ONLY",
        "phase057_links": ["INTENT-PROV-0187"],
        "downstream_owner": "Step 61 canonical prose/runtime concordance",
    },
    {
        "finding_id": "P063-COMP-009",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_AUD/AUD3_CH3.md", "line_intervals": [[17, 20], [59, 63]]},
            {"path": "Claude/docs/v1.0.22/results/comp_AUD/AUD4_CODE.md", "line_intervals": [[31, 37]]},
        ],
        "classification": "COORDINATE_PHASE_AND_GATE_GAP",
        "finding": "f_Si/m_Si label residue and two-phase slope/plateau tension remain, while a central f_Si>0 balance check exists only as an audit calculation outside the regular gate.",
        "authority_ceiling": "REVIEW_RECORD_ONLY",
        "phase057_links": ["INTENT-PROV-0168", "INTENT-PROV-0169", "INTENT-PROV-0170", "INTENT-PROV-0171", "INTENT-PROV-0172", "INTENT-PROV-0187"],
        "downstream_owner": "Step 59 Ch3 rederivation and Step 61 independent runtime gate",
    },
    {
        "finding_id": "P063-COMP-010",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/comp_FR/A06_REVIEW.md", "line_intervals": [[35, 72]]}],
        "classification": "TST_HIGH_TEMPERATURE_LIMIT_CONCERN",
        "finding": "For a finite high-temperature rate constant, q-double-dagger/q-reactant must supply a 1/T factor against the k_B T/h prefactor.",
        "authority_ceiling": "REVIEW_DERIVATION_ONLY",
        "phase057_links": ["INTENT-PROV-0146"],
        "downstream_owner": "Step 59 independent TST rederivation",
    },
    {
        "finding_id": "P063-COMP-011",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/comp_FR/A07_REVIEW.md", "line_intervals": [[29, 68]]}],
        "classification": "SUSCEPTIBILITY_CONDITION_CONCERN",
        "finding": "The exact independent-site susceptibility condition is Omega=0 rather than n=1; 1/n scales peak height while n also changes width.",
        "authority_ceiling": "REVIEW_DERIVATION_ONLY",
        "phase057_links": ["INTENT-PROV-0147"],
        "downstream_owner": "Step 59 independent statistical-mechanics rederivation",
    },
    {
        "finding_id": "P063-COMP-012",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_FR/A08_REVIEW.md", "line_intervals": [[41, 66]]},
            {"path": "Claude/docs/v1.0.22/results/comp_FR/A09_REVIEW.md", "line_intervals": [[49, 115]]},
        ],
        "classification": "BROADENING_AND_BARRIER_LAYER_CONCERN",
        "finding": "The claim that w absorbs all three effects conflicts with a separately modeled L_V, and one reading of the full amplitude plus effective barrier double-counts chi_Omega.",
        "authority_ceiling": "REVIEW_DERIVATION_ONLY",
        "phase057_links": ["INTENT-PROV-0149", "INTENT-PROV-0158"],
        "downstream_owner": "Step 59 broadening/kinetics operator separation",
    },
    {
        "finding_id": "P063-COMP-013",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/comp_FR/A13_REVIEW.md", "line_intervals": [[50, 149], [191, 203]]}],
        "classification": "THERMAL_STATMECH_AND_FIGURE_CONCERN",
        "finding": "An absorption constant is not a high-temperature corner, a mode-count plus one is hidden, a T_ref zero is not identifiability, and a plotted endpoint 1.4574 differs from the reported recomputation 1.4700.",
        "authority_ceiling": "REVIEW_RECOMPUTATION_ONLY",
        "phase057_links": ["INTENT-PROV-0159", "INTENT-PROV-0160", "INTENT-PROV-0161", "INTENT-PROV-0162"],
        "downstream_owner": "Step 59 thermal rederivation and Step 62 figure/source closure",
    },
    {
        "finding_id": "P063-COMP-014",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_FR/A19_REVIEW.md", "line_intervals": [[37, 105]]},
            {"path": "Claude/docs/v1.0.22/results/comp_FR/A20_REVIEW.md", "line_intervals": [[36, 62]]},
        ],
        "classification": "LCO_COORDINATE_AND_ELECTRONIC_SCOPE_CONCERN",
        "finding": "Delithiation coordinate x_bar is conflated with an MIT Li-fraction coordinate, a local MIT term is implemented as a global electronic constant, and a_e<0 implies dU/dT decreases with T.",
        "authority_ceiling": "REVIEW_DERIVATION_ONLY",
        "phase057_links": ["INTENT-PROV-0165", "INTENT-PROV-0166", "INTENT-PROV-0167"],
        "downstream_owner": "Step 59 LCO coordinate/electronic closure",
    },
    {
        "finding_id": "P063-COMP-015",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_FR/A21_REVIEW.md", "line_intervals": [[35, 68]]},
            {"path": "Claude/docs/v1.0.22/results/comp_FR/A22_REVIEW.md", "line_intervals": [[13, 58], [89, 107], [348, 372]]},
            {"path": "Claude/docs/v1.0.22/results/comp_FR/A23_REVIEW.md", "line_intervals": [[40, 117]]},
        ],
        "classification": "CH3_MATERIAL_SOURCE_AND_GATE_CONCERN",
        "finding": "Review records identify category-count drift, a-Si/c-Si and two-phase-slope issues, stale or ghost citations, a missing lag-tail term in a host equation, a G3 background-subtraction concern, and an N6 classification error.",
        "authority_ceiling": "REVIEW_RECORD_ONLY",
        "phase057_links": ["INTENT-PROV-0168", "INTENT-PROV-0169", "INTENT-PROV-0170", "INTENT-PROV-0171", "INTENT-PROV-0172", "INTENT-PROV-0173"],
        "downstream_owner": "Steps 59–62 Ch3 material/source/build adjudication",
    },
    {
        "finding_id": "P063-COMP-016",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/comp_SM2/SM2_DRAFTS/SM2C_two_responses.tex", "line_intervals": [[21, 31]]}],
        "classification": "IMPLICIT_TEMPERATURE_RESPONSE_OMISSION",
        "finding": "The fixed-voltage temperature derivative omits the implicit xi(T,V) response while presenting two responses as simple partial derivatives of the same term.",
        "authority_ceiling": "CANDIDATE_DERIVATION_ONLY",
        "phase057_links": ["INTENT-PROV-0141"],
        "downstream_owner": "Step 59 independent thermodynamic rederivation",
    },
    {
        "finding_id": "P063-COMP-017",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/comp_v23/SURV2_asymptotic_pert.md", "line_intervals": [[38, 43]]}],
        "classification": "KERNEL_OUTPUT_SKEWNESS_CONFLATION",
        "finding": "Exponential-kernel skewness 2 is presented in a way that can be read as the convolved-output skewness, which also depends on the input variance.",
        "authority_ceiling": "REVIEW_SURVEY_ONLY",
        "phase057_links": ["INTENT-PROV-0188"],
        "downstream_owner": "Step 59 mathematical operator adjudication",
    },
    {
        "finding_id": "P063-COMP-018",
        "evidence": [{"path": "Claude/docs/v1.0.22/results/comp_v23/SURV3_convex_inverse.md", "line_intervals": [[47, 50], [80, 84]]}],
        "classification": "CONVEXITY_AND_IDENTIFIABILITY_SCOPE_CONCERN",
        "finding": "Convexity, strict/strong convexity, and unique-root claims are compressed beyond their conditions, and a two-temperature Fisher-information rank deficiency is generalized without its assumptions.",
        "authority_ceiling": "REVIEW_SURVEY_ONLY",
        "phase057_links": ["INTENT-PROV-0188", "INTENT-PROV-0189"],
        "downstream_owner": "Step 59 convexity/identifiability adjudication",
    },
    {
        "finding_id": "P063-COMP-019",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_v23/SURV4_bifurcation_stochastic.md", "line_intervals": [[44, 47]]},
            {"path": "Claude/docs/v1.0.22/results/comp_v23/SURV2_asymptotic_pert.md", "line_intervals": [[75, 86]]},
            {"path": "Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md", "line_intervals": [[28, 31]]},
        ],
        "classification": "CRITICAL_EXPONENT_DESCRIPTION_CONFLICT",
        "finding": "The 3/2 exponent is described both as not specific to mean field and as the mean-field spinodal exponent.",
        "authority_ceiling": "REVIEW_SURVEY_ONLY",
        "phase057_links": ["INTENT-PROV-0188"],
        "downstream_owner": "Step 59 critical-phenomena adjudication",
    },
    {
        "finding_id": "P063-COMP-020",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md", "line_intervals": [[14, 17]]},
            {"path": "Claude/docs/v1.0.22/results/comp_v23/SURV1_integral_transform.md", "line_intervals": [[15, 15], [116, 116], [173, 173], [176, 176]]},
        ],
        "classification": "UNVERIFIED_ORIGINAL_METHOD_PROMOTION",
        "finding": "A Fredholm-ratio core is recommended for promotion while its relation to the original JCP method remains unverified.",
        "authority_ceiling": "REVIEW_SURVEY_ONLY",
        "phase057_links": ["INTENT-PROV-0188", "INTENT-PROV-0191"],
        "downstream_owner": "Step 60 primary-paper method adjudication",
    },
    {
        "finding_id": "P063-COMP-021",
        "evidence": [
            {"path": "Claude/docs/v1.0.22/results/comp_RV/RV1_CH1_REPORT.md", "line_intervals": [[115, 115], [134, 138]]},
            {"path": "Claude/docs/v1.0.22/results/comp_RV/RV2_CH2_REPORT.md", "line_intervals": [[138, 139]]},
        ],
        "classification": "PASS_WITH_EXTERNAL_REFERENCE_GAPS",
        "finding": "H=0/PASS conclusions coexist with missing references 6/7 and unverified tier-4 original numerical values.",
        "authority_ceiling": "REVIEW_RECORD_ONLY",
        "phase057_links": ["INTENT-PROV-0140"],
        "downstream_owner": "Step 60 release/reference adjudication",
    },
)


class BuildError(RuntimeError):
    pass


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def strict_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"non-finite JSON number: {value}")
    return number


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(path: Path) -> Any:
    return strict_json_text(path.read_text(encoding="utf-8"))


def strict_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_constant=reject_constant,
        parse_float=strict_float,
    )


def normalize_lf(data: bytes) -> bytes:
    return data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def projection_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def load_human_review_evidence() -> tuple[dict[str, Any], str]:
    text = RESULT.read_text(encoding="utf-8")
    if text.count(HUMAN_EVIDENCE_BEGIN) != 1 or text.count(HUMAN_EVIDENCE_END) != 1:
        raise BuildError("human-review evidence marker cardinality")
    block = text.split(HUMAN_EVIDENCE_BEGIN, 1)[1].split(HUMAN_EVIDENCE_END, 1)[0].strip()
    if not block.startswith("```json\n") or not block.endswith("\n```"):
        raise BuildError("human-review evidence fence")
    raw = block[len("```json\n"):-len("\n```")]
    evidence = strict_json_text(raw)
    if not isinstance(evidence, dict):
        raise BuildError("human-review evidence root")
    return evidence, sha256(projection_bytes(evidence))


def strip_tex_comments(text: str) -> str:
    cleaned: list[str] = []
    for line in text.splitlines():
        cut = len(line)
        for index, char in enumerate(line):
            if char != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                cut = index
                break
        cleaned.append(line[:cut])
    return "\n".join(cleaned)


def tex_citation_occurrences(path: str, text: str) -> list[dict[str, Any]]:
    cleaned = strip_tex_comments(text)
    pattern = re.compile(r"\\(?P<command>cite[a-zA-Z*]*)(?:\s*\[[^\]]*\]){0,2}\s*\{(?P<keys>[^}]+)\}")
    rows: list[dict[str, Any]] = []
    commands_on_line: Counter[int] = Counter()
    for match in pattern.finditer(cleaned):
        line = cleaned.count("\n", 0, match.start()) + 1
        column = match.start() - cleaned.rfind("\n", 0, match.start())
        commands_on_line[line] += 1
        for key_ordinal, key in enumerate((item.strip() for item in match.group("keys").split(",")), start=1):
            if key:
                rows.append({
                    "key": key,
                    "source_path": path,
                    "line": line,
                    "column": column,
                    "command": match.group("command"),
                    "command_ordinal_on_line": commands_on_line[line],
                    "key_ordinal_within_command": key_ordinal,
                })
    return rows


def tex_bibliography_definitions(path: str, text: str) -> list[dict[str, Any]]:
    cleaned = strip_tex_comments(text)
    pattern = re.compile(r"\\bibitem(?:\s*\[[^\]]*\])?\s*\{([^}]+)\}")
    return [
        {"key": match.group(1).strip(), "source_path": path, "line": cleaned.count("\n", 0, match.start()) + 1}
        for match in pattern.finditer(cleaned)
    ]


def shortest_dependency_routes(root: str, adjacency: dict[str, list[str]]) -> dict[str, list[str]]:
    routes = {root: [root]}
    queue = [root]
    while queue:
        source = queue.pop(0)
        for target in adjacency.get(source, []):
            if target not in routes:
                routes[target] = [*routes[source], target]
                queue.append(target)
    return routes


def git_bytes(*args: str) -> bytes:
    proc = subprocess.run(
        ["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=GIT_TIMEOUT, check=False,
    )
    if proc.returncode:
        raise BuildError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8", errors="strict").strip()


def cat_file_batch(shas: list[str]) -> dict[str, bytes]:
    ordered = list(dict.fromkeys(shas))
    proc = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=REPO,
        input=("\n".join(ordered) + "\n").encode("ascii"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=GIT_TIMEOUT, check=False,
    )
    if proc.returncode:
        raise BuildError(proc.stderr.decode("utf-8", errors="replace"))
    out = proc.stdout
    pos = 0
    blobs: dict[str, bytes] = {}
    for requested in ordered:
        end = out.find(b"\n", pos)
        if end < 0:
            raise BuildError("truncated cat-file header")
        header = out[pos:end].decode("ascii").split()
        pos = end + 1
        if len(header) != 3 or header[1] != "blob":
            raise BuildError(f"unexpected cat-file header: {header}")
        size = int(header[2])
        data = out[pos:pos + size]
        pos += size
        if len(data) != size or out[pos:pos + 1] != b"\n":
            raise BuildError(f"truncated cat-file body: {requested}")
        pos += 1
        blobs[requested] = data
    if pos != len(out):
        raise BuildError("unexpected cat-file trailer")
    return blobs


def partition(path: str) -> str:
    rel = path.removeprefix("Claude/docs/v1.0.22/")
    if rel.startswith("plans/"):
        return "VERSION_PLAN"
    if rel.startswith("results/comp_"):
        return "COMPETING_REVIEW_CANDIDATE"
    if rel.startswith("results/"):
        return "STATUS_MACHINE_PROCESS"
    return "FINAL_RELEASE_SURFACE"


def authority(part: str) -> str:
    return {
        "FINAL_RELEASE_SURFACE": "FROZEN_RELEASE_CONTENT_OR_BUILD_ONLY",
        "VERSION_PLAN": "PROCESS_INTENT_ONLY",
        "STATUS_MACHINE_PROCESS": "SELF_REPORT_OR_MACHINE_STRUCTURE_ONLY",
        "COMPETING_REVIEW_CANDIDATE": "PROPOSAL_REVIEW_EVIDENCE_ONLY",
    }[part]


def competing_authority_subtype(path: str) -> str:
    prefix = "Claude/docs/v1.0.22/results/"
    if not path.startswith(prefix + "comp_"):
        raise BuildError(f"not a competing path: {path}")
    rel = path[len(prefix):]
    task_paths = {
        "comp_FR/BRIEF_FR_A.md", "comp_R2/BRIEF_A.md", "comp_R2/BRIEF_B.md",
        "comp_R2/BRIEF_C.md", "comp_R3/BRIEF_D.md", "comp_R3/BRIEF_E.md",
        "comp_R4/BRIEF_R4.md", "comp_R5/BRIEF_R5.md",
    }
    decision_paths = {
        "comp_R2/CHERRYPICK_R2.md", "comp_R3/CHERRYPICK_R3.md",
        "comp_R5/CHERRYPICK_R5.md", "comp_FR/EXEC_M1.md", "comp_FR/EXEC_M2.md",
        "comp_FR/EXEC_M3.md", "comp_FR/EXEC_M4.md",
        "comp_FR/FR_T_H_TRIAGE_PREP.md", "comp_FR/FR_T_ML_TRIAGE.md",
    }
    self_report_paths = {
        "comp_FR/RESUME_FR.md", "comp_R4/REPORT_R4_COMPLETE.md",
        "comp_R6/R6_REPORT.md", "comp_R8/R8_EXEC.md",
    }
    if rel in task_paths:
        return "T_TASK_OR_BRIEF"
    if rel in decision_paths:
        return "D_DECISION_TRIAGE_OR_EXECUTION_RECORD"
    if rel in self_report_paths:
        return "S_SELF_REPORT_OR_STATUS"
    basename = posixpath.basename(rel)
    if (
        rel.startswith("comp_AUD/")
        or (rel.startswith("comp_FR/") and re.fullmatch(r"A\d{2}_REVIEW\.md", basename))
        or rel.startswith("comp_R4/")
        or rel.startswith("comp_RV/")
        or rel.startswith("comp_v23/")
        or rel in {"comp_SM2/SM2_REMOVAL.md", "comp_SM2/SM2_SURVEY.md"}
    ):
        return "R_REVIEW_OR_SURVEY"
    return "C_CANDIDATE_PROPOSAL_OR_DRAFT"


def attach_finding_source_ids(
    findings: tuple[dict[str, Any], ...], source_by_path: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    attached: list[dict[str, Any]] = []
    for original in findings:
        row = json.loads(json.dumps(original, ensure_ascii=False))
        evidence = row.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            raise BuildError(f"finding lacks per-source evidence: {row.get('finding_id')}")
        paths = [item["path"] for item in evidence]
        missing = [path for path in paths if path not in source_by_path]
        if missing:
            raise BuildError(f"finding paths are not sources: {missing}")
        for item in evidence:
            source = source_by_path[item["path"]]
            item["source_id"] = source["source_id"]
            item["blob_sha1"] = source["blob_sha1"]
        row["source_ids"] = [source_by_path[path]["source_id"] for path in paths]
        row["status_promoted"] = False
        row["external_truth_promoted"] = False
        attached.append(row)
    return attached


def attach_cross_version_relations(
    indexed_v21: list[tuple[int, dict[str, Any]]],
    indexed_v22: list[tuple[int, dict[str, Any]]],
    source_by_path: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    old_by_rel = {version_relative(row["path"], "v1.0.21"): (index, row) for index, row in indexed_v21}
    new_by_rel = {version_relative(row["path"], "v1.0.22"): (index, row) for index, row in indexed_v22}
    old_only = set(old_by_rel) - set(new_by_rel)
    new_only = set(new_by_rel) - set(old_by_rel)
    used_old: set[str] = set()
    used_new: set[str] = set()
    attached: list[dict[str, Any]] = []
    for original in CROSS_VERSION_RELATIONS:
        row = json.loads(json.dumps(original, ensure_ascii=False))
        old_rel = row.pop("v1021_relative_paths")
        new_rel = row.pop("v1022_relative_paths")
        if not set(old_rel).issubset(old_only) or not set(new_rel).issubset(new_only):
            raise BuildError(f"cross-version relation leaves old/new-only namespace: {row['relation_id']}")
        if used_old & set(old_rel) or used_new & set(new_rel):
            raise BuildError(f"cross-version primary relation overlaps: {row['relation_id']}")
        old_sources = []
        for rel in old_rel:
            index, entry = old_by_rel[rel]
            old_sources.append({
                "manifest_index": index,
                "relative_path": rel,
                "path": entry["path"],
                "blob_sha1": entry["blob_sha"],
                "bytes": entry["size_bytes"],
            })
        new_sources = []
        for rel in new_rel:
            index, entry = new_by_rel[rel]
            source = source_by_path[entry["path"]]
            first_add_blob = git_text("rev-parse", f"{source['first_add_commit']}:{entry['path']}")
            new_sources.append({
                "source_id": source["source_id"],
                "manifest_index": index,
                "relative_path": rel,
                "path": entry["path"],
                "blob_sha1": entry["blob_sha"],
                "first_add_commit": source["first_add_commit"],
                "first_add_blob_sha1": first_add_blob,
                "bytes": entry["size_bytes"],
            })
        old_blobs = {item["blob_sha1"] for item in old_sources}
        for item in new_sources:
            item["first_add_matches_relation_source_blob"] = item["first_add_blob_sha1"] in old_blobs
        if row["relation"] == "RENAMED":
            detected: list[dict[str, Any]] = []
            old_paths = {item["path"] for item in old_sources}
            target_paths = {item["path"] for item in new_sources}
            for commit in sorted({item["first_add_commit"] for item in new_sources}):
                raw = git_text(
                    "diff-tree", "--no-commit-id", "--name-status", "-r", "-C",
                    "--find-copies-harder", commit,
                )
                for line in raw.splitlines():
                    cells = line.split("\t")
                    if len(cells) == 3 and cells[1] in old_paths and cells[2] in target_paths:
                        detected.append({
                            "commit": commit,
                            "status": cells[0],
                            "v1021_path": cells[1],
                            "v1022_path": cells[2],
                        })
            if len(detected) != len(new_sources):
                raise BuildError(f"rename copy-detection evidence mismatch: {row['relation_id']}")
            row["git_copy_detection"] = detected
        for evidence in row["process_evidence"]:
            source = source_by_path.get(evidence["path"])
            if source is None:
                raise BuildError(f"cross-version evidence is not a v1.0.22 source: {evidence['path']}")
            evidence["source_id"] = source["source_id"]
            evidence["blob_sha1"] = source["blob_sha1"]
        row["v1021_sources"] = old_sources
        row["v1022_sources"] = new_sources
        row["scientific_truth_promoted"] = False
        row["build_reproducibility_promoted"] = False
        attached.append(row)
        used_old.update(old_rel)
        used_new.update(new_rel)
    return attached, sorted(old_only - used_old), sorted(new_only - used_new)


def build_citation_genealogy(
    sources: list[dict[str, Any]],
    text_by_path: dict[str, str],
    tex_edges: list[dict[str, Any]],
    pdf_root_edges: list[dict[str, Any]],
) -> dict[str, Any]:
    source_by_path = {row["path"]: row for row in sources}
    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in tex_edges:
        if edge["kind"] == "INPUT" and edge["target_state"] == "MANIFEST_MEMBER":
            adjacency[edge["source_path"]].append(edge["resolved_path"])
    for path in adjacency:
        adjacency[path] = sorted(set(adjacency[path]))

    root_rows: list[dict[str, Any]] = []
    all_routes: list[dict[str, Any]] = []
    route_ordinal = 0
    for root_edge in sorted(pdf_root_edges, key=lambda row: row["root_tex_path"]):
        root = root_edge["root_tex_path"]
        dependency_routes = shortest_dependency_routes(root, adjacency)
        citations: list[dict[str, Any]] = []
        definitions: list[dict[str, Any]] = []
        for path in sorted(dependency_routes):
            text = text_by_path.get(path)
            if text is None:
                continue
            citations.extend(tex_citation_occurrences(path, text))
            definitions.extend(tex_bibliography_definitions(path, text))
        citation_by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
        definition_by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for item in citations:
            citation_by_key[item["key"]].append(item)
        for item in definitions:
            definition_by_key[item["key"]].append(item)
        for key in sorted(set(citation_by_key) | set(definition_by_key)):
            route_ordinal += 1
            occurrences = []
            for item in sorted(citation_by_key.get(key, []), key=lambda row: (row["source_path"], row["line"])):
                source = source_by_path[item["source_path"]]
                occurrences.append({
                    "source_id": source["source_id"],
                    "source_path": item["source_path"],
                    "blob_sha1": source["blob_sha1"],
                    "line": item["line"],
                    "column": item["column"],
                    "command": item["command"],
                    "command_ordinal_on_line": item["command_ordinal_on_line"],
                    "key_ordinal_within_command": item["key_ordinal_within_command"],
                    "root_to_source_path": dependency_routes[item["source_path"]],
                })
            definition_rows = []
            for item in sorted(definition_by_key.get(key, []), key=lambda row: (row["source_path"], row["line"])):
                source = source_by_path[item["source_path"]]
                definition_rows.append({
                    "source_id": source["source_id"],
                    "source_path": item["source_path"],
                    "blob_sha1": source["blob_sha1"],
                    "line": item["line"],
                    "root_to_bibliography_path": dependency_routes[item["source_path"]],
                })
            state = "CLOSED" if occurrences and len(definition_rows) == 1 else (
                "UNUSED_DEFINITION" if not occurrences and definition_rows else "MISSING_OR_DUPLICATE_DEFINITION"
            )
            all_routes.append({
                "route_id": f"P063-CITE-{route_ordinal:03d}",
                "root_tex_source_id": root_edge["root_tex_source_id"],
                "root_tex_path": root,
                "pdf_source_id": root_edge["pdf_source_id"],
                "pdf_path": root_edge["pdf_path"],
                "cite_key": key,
                "citation_occurrences": occurrences,
                "bibliography_definitions": definition_rows,
                "closure_state": state,
                "pdf_page": None,
                "pdf_page_mapping_state": "GROUND_NOT_FOUND_NO_SYNCTEX_OR_TAGGED_SOURCE_MAP",
                "pdf_page_mapping_owner": "Phase 063 Step 62 clean build/page genealogy",
                "authority_ceiling": "STATIC_SOURCE_CITATION_TO_BIBLIOGRAPHY_ONLY",
            })
        root_rows.append({
            "root_tex_source_id": root_edge["root_tex_source_id"],
            "root_tex_path": root,
            "pdf_source_id": root_edge["pdf_source_id"],
            "pdf_path": root_edge["pdf_path"],
            "pdf_pages": root_edge["pages"],
            "reachable_tex_source_ids": [source_by_path[path]["source_id"] for path in sorted(dependency_routes)],
            "reachable_tex_paths": sorted(dependency_routes),
            "citation_key_count": len(citation_by_key),
            "bibliography_key_count": len(definition_by_key),
            "missing_keys": len(set(citation_by_key) - set(definition_by_key)),
            "unused_keys": len(set(definition_by_key) - set(citation_by_key)),
            "duplicate_keys": sum(len(rows) - 1 for rows in definition_by_key.values() if len(rows) > 1),
            "page_binding": {
                "root_pdf_pair_state": "CONFIRMED_FROZEN_BLOB_PAIR",
                "page_nodes_ref": "V1022_READ_ATTESTATION.pdf_page_attestations",
                "source_to_page_state": "GROUND_NOT_FOUND",
                "citation_to_page_state": "GROUND_NOT_FOUND",
                "bibitem_to_page_state": "GROUND_NOT_FOUND",
                "reason": "NO_FROZEN_SYNCTEX_AUX_TOC_FLS_LOG_OR_OUT_PAGE_MAP",
                "downstream_owner": "Phase 063 Step 62 Task 62B clean build/page genealogy",
                "authority_ceiling": "FROZEN_SOURCE_PDF_IDENTITY_ONLY",
            },
        })
    command_keys = {
        (
            item["source_path"], item["line"], item["column"],
            item["command_ordinal_on_line"], row["root_tex_path"],
        )
        for row in all_routes for item in row["citation_occurrences"]
    }
    source_line_keys = {
        (item["source_path"], item["line"], row["root_tex_path"])
        for row in all_routes for item in row["citation_occurrences"]
    }
    return {
        "root_routes": root_rows,
        "citation_routes": all_routes,
        "counts": {
            "root_routes": len(root_rows),
            "citation_routes": len(all_routes),
            "citation_occurrences": sum(len(row["citation_occurrences"]) for row in all_routes),
            "citation_commands": len(command_keys),
            "citation_source_lines": len(source_line_keys),
            "bibliography_definitions": sum(len(row["bibliography_definitions"]) for row in all_routes),
            "closed_routes": sum(row["closure_state"] == "CLOSED" for row in all_routes),
            "pdf_page_mapped_routes": sum(row["pdf_page"] is not None for row in all_routes),
            "pdf_page_ground_not_found_routes": sum(row["pdf_page_mapping_state"].startswith("GROUND_NOT_FOUND") for row in all_routes),
        },
        "authority_ceiling": "SOURCE_CITATION_GENEALOGY_ONLY_PDF_PAGE_MAPPING_GROUND_NOT_FOUND",
    }


def version_relative(path: str, version: str) -> str:
    prefix = f"Claude/docs/{version}/"
    if not path.startswith(prefix):
        raise BuildError(f"version path mismatch: {path}")
    return path[len(prefix):]


def parse_change_rows(commit: str) -> list[dict[str, Any]]:
    raw = git_text(
        "diff-tree", "--root", "--no-commit-id", "--name-status", "-r", "-M", "-C",
        commit, "--", "Claude/docs/v1.0.22",
    )
    rows: list[dict[str, Any]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        cells = line.split("\t")
        status = cells[0]
        if len(cells) not in {2, 3}:
            raise BuildError(f"unparsed name-status row {commit}: {line}")
        rows.append({"status": status, "paths": cells[1:]})
    return rows


def commit_role(subject: str, changes: list[dict[str, Any]]) -> str:
    paths = [path for row in changes for path in row["paths"] if path.startswith("Claude/docs/v1.0.22/")]
    has_pdf = any(path.endswith(".pdf") for path in paths)
    has_final = any(partition(path) == "FINAL_RELEASE_SURFACE" for path in paths)
    has_comp = any(partition(path) == "COMPETING_REVIEW_CANDIDATE" for path in paths)
    has_process = any(partition(path) in {"VERSION_PLAN", "STATUS_MACHINE_PROCESS"} for path in paths)
    lowered = subject.lower()
    if has_pdf or lowered.startswith("build("):
        return "BUILD_OR_PDF_CHECKPOINT" if not (has_final and has_process) else "MIXED_SOURCE_PROCESS_BUILD"
    if has_comp and not has_final:
        return "COMPETING_REVIEW_OR_CANDIDATE"
    if has_final and has_process:
        return "MIXED_SOURCE_AND_PROCESS_CHECKPOINT"
    if has_final:
        return "RELEASE_SOURCE_PATCH"
    if has_process:
        return "PROCESS_PLAN_STATUS_OR_MACHINE_RECORD"
    return "VERSION_SUBTREE_METADATA"


def build_history(source_paths: set[str]) -> tuple[
    list[dict[str, Any]], dict[str, list[str]], dict[str, list[dict[str, Any]]],
    dict[str, list[tuple[int, str, str, str]]], list[dict[str, Any]],
]:
    commit_ids = git_text(
        "rev-list", "--reverse", "--topo-order", BASELINE, "--", "Claude/docs/v1.0.22",
    ).splitlines()
    commits: list[dict[str, Any]] = []
    touches: dict[str, list[str]] = defaultdict(list)
    additions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    touch_events: dict[str, list[tuple[int, str, str, str]]] = defaultdict(list)
    projection: list[dict[str, Any]] = []
    for ordinal, commit in enumerate(commit_ids, start=1):
        metadata = git_bytes("show", "-s", "--format=%H%x00%P%x00%an%x00%aI%x00%cI%x00%s", commit)
        fields = metadata.rstrip(b"\n").decode("utf-8", errors="strict").split("\x00", 5)
        if len(fields) != 6 or fields[0] != commit:
            raise BuildError(f"unparsed commit metadata: {commit}")
        _, parents, actor, author_time, committer_time, subject = fields
        changes = parse_change_rows(commit)
        for row in changes:
            roles = ["path"] if len(row["paths"]) == 1 else ["old", "new"]
            for path, event_role in zip(row["paths"], roles):
                if path in source_paths and (not touches[path] or touches[path][-1] != commit):
                    touches[path].append(commit)
                    touch_events[path].append((ordinal, commit, row["status"], event_role))
                if path in source_paths and event_role in {"path", "new"} and row["status"].startswith(("A", "R", "C")):
                    additions[path].append({"commit": commit, "status": row["status"], "source_path": row["paths"][0] if event_role == "new" else None})
        commits.append({
            "event_id": f"P063-COMMIT-{ordinal:03d}",
            "commit": commit,
            "parents": parents.split() if parents else [],
            "repository_actor": actor,
            "author_time": author_time,
            "committer_time": committer_time,
            "subject": subject,
            "process_role": commit_role(subject, changes),
            "changed_paths": changes,
        })
        projection.append({
            "index": ordinal,
            "commit": commit,
            "parents": parents.split() if parents else [],
            "author_time": author_time,
            "committer_time": committer_time,
            "subject": subject,
            "changes": changes,
        })
    return commits, dict(touches), dict(additions), dict(touch_events), projection


def resolve_tex_target(source_path: str, target: str) -> str:
    clean = target.strip()
    if not clean.endswith(".tex"):
        clean += ".tex"
    return posixpath.normpath(posixpath.join(posixpath.dirname(source_path), clean))


def tex_dependencies(path: str, text: str, path_set: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    patterns = (
        ("INPUT", re.compile(r"\\(?:input|include)\{([^}]+)\}")),
        ("EXTERNAL_DOCUMENT", re.compile(r"\\externaldocument(?:\[[^\]]*\])?\{([^}]+)\}")),
    )
    for kind, pattern in patterns:
        for match in pattern.finditer(text):
            resolved = resolve_tex_target(path, match.group(1))
            line = text.count("\n", 0, match.start()) + 1
            rows.append({
                "kind": kind,
                "line": line,
                "raw_target": match.group(1),
                "resolved_path": resolved,
                "target_state": "MANIFEST_MEMBER" if resolved in path_set else "GROUND_NOT_FOUND_IN_V1022_MANIFEST",
            })
    return rows


def build_observations() -> tuple[list[dict[str, Any]], dict[str, str]]:
    rows: list[dict[str, Any]] = []
    by_path: dict[str, str] = {}
    for obs_id, rel, expected_lines, expected_sha in OBSERVATIONS:
        data = (REPO / rel).read_bytes()
        lines = data.decode("utf-8").splitlines()
        observed_sha = sha256(data)
        if len(lines) != expected_lines or observed_sha != expected_sha:
            raise BuildError(f"observation identity mismatch: {rel}")
        rows.append({
            "observation_id": obs_id,
            "path": rel,
            "sha256": observed_sha,
            "physical_lines": len(lines),
            "read_interval": [1, len(lines)],
            "read_status": "READ_FULL",
            "authority_ceiling": "PHASE057_REAUDIT_ROUTING_INPUT_ONLY",
        })
        by_path[rel] = obs_id
    return rows, by_path


def finding_routes(source_rows: list[dict[str, Any]], observation_ids: dict[str, str]) -> list[dict[str, Any]]:
    intent = strict_json(INTENT)
    records = [row for row in intent["records"] if 96 <= row.get("numeric_id", -1) <= 191]
    by_basename: dict[str, list[str]] = defaultdict(list)
    for row in source_rows:
        by_basename[posixpath.basename(row["path"])].append(row["source_id"])
    routes: list[dict[str, Any]] = []
    for record in records:
        block = "\n".join((REPO / record["source_path"]).read_text(encoding="utf-8").splitlines()[record["source_lines"][0] - 1:record["source_lines"][1]])
        candidate_ids: set[str] = set()
        for basename, ids in by_basename.items():
            if basename and basename in block:
                candidate_ids.update(ids)
        routes.append({
            "finding_id": record["claim_id"],
            "numeric_id": record["numeric_id"],
            "observation_source_id": observation_ids[record["source_path"]],
            "observation_lines": record["source_lines"],
            "referenced_actor": record["referenced_actor"],
            "actor_confidence": record["actor_confidence"],
            "candidate_v1022_source_ids": sorted(candidate_ids),
            "route_state": "SOURCE_CANDIDATES_LINKED" if candidate_ids else "OBSERVATION_EVIDENCE_ONLY",
            "status_promoted": False,
            "external_truth_promoted": False,
            "downstream_owner": "Phase 063 Step 63.1 disposition; Phase 071+ for external truth",
        })
    return routes


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    human_evidence, human_evidence_sha256 = load_human_review_evidence()
    if human_evidence.get("schema_version") != 1 or human_evidence.get("evidence_id") != "P063-HUMAN-REVIEW-STEP58-001":
        raise BuildError("human-review evidence schema/identity")
    text_review_by_partition: dict[str, dict[str, Any]] = {}
    for review in human_evidence.get("text_reviews", []):
        for partition_name in review.get("partitions", []):
            if partition_name in text_review_by_partition:
                raise BuildError(f"duplicate text-review partition: {partition_name}")
            text_review_by_partition[partition_name] = review
    pdf_review_by_path = {row["path"]: row for row in human_evidence.get("pdf_reviews", [])}
    if len(pdf_review_by_path) != len(human_evidence.get("pdf_reviews", [])):
        raise BuildError("duplicate PDF human-review path")
    if sha256(normalize_lf(MANIFEST.read_bytes())) != MANIFEST_SHA256:
        raise BuildError("manifest normalized SHA mismatch")
    manifest = strict_json(MANIFEST)
    indexed_v22 = [(index, row) for index, row in enumerate(manifest["entries"], start=1) if row.get("version") == "v1.0.22"]
    indexed_v21 = [(index, row) for index, row in enumerate(manifest["entries"], start=1) if row.get("version") == "v1.0.21"]
    source_paths = {row["path"] for _, row in indexed_v22}
    blobs = cat_file_batch([row["blob_sha"] for _, row in indexed_v22] + [SUPPLEMENTAL_BLOB])
    commits, touches, additions, touch_events, history_projection = build_history(source_paths)
    commit_by_id = {row["commit"]: row for row in commits}

    sources: list[dict[str, Any]] = []
    read_records: list[dict[str, Any]] = []
    pdf_pages: list[dict[str, Any]] = []
    part_counts: Counter[str] = Counter()
    part_bytes: Counter[str] = Counter()
    part_lines: Counter[str] = Counter()
    part_nonblank: Counter[str] = Counter()
    part_pages: Counter[str] = Counter()
    mode_counts: Counter[str] = Counter()
    competing_subtype_counts: Counter[str] = Counter()
    tex_edges: list[dict[str, Any]] = []
    text_by_path: dict[str, str] = {}
    for ordinal, (manifest_index, entry) in enumerate(indexed_v22, start=1):
        path = entry["path"]
        data = blobs[entry["blob_sha"]]
        part = partition(path)
        source_id = f"P063-SRC-{ordinal:04d}"
        history = touches.get(path, [])
        if not history:
            raise BuildError(f"source without history: {path}")
        first_add = additions.get(path, [{}])[0].get("commit", history[0])
        last_touch = history[-1]
        extent = {"bytes": len(data), "lines": 0, "nonblank_lines": 0, "pages": 0}
        structure: dict[str, Any] = {}
        if entry["review_mode"] == "FULL_TEXT":
            text = data.decode("utf-8", errors="strict")
            text_by_path[path] = text
            lines = text.splitlines()
            extent["lines"] = len(lines)
            extent["nonblank_lines"] = sum(bool(line.strip()) for line in lines)
            if entry["extension"] == "tex":
                dependencies = tex_dependencies(path, text, source_paths)
                structure = {
                    "tex_dependencies": dependencies,
                    "citation_occurrences": len(re.findall(r"\\cite[a-zA-Z]*\{[^}]+\}", text)),
                    "bibliography_blocks": text.count("\\begin{thebibliography}"),
                }
                for dependency in dependencies:
                    tex_edges.append({"source_id": source_id, "source_path": path, **dependency})
            read_records.append({
                "source_id": source_id,
                "path": path,
                "review_mode": "FULL_TEXT",
                "read_status": "READ_FULL",
                "human_review_evidence_id": text_review_by_partition.get(part, {}).get("review_id"),
                "physical_interval": [1, len(lines)],
                "physical_lines": len(lines),
                "nonblank_lines": extent["nonblank_lines"],
                "blob_sha1": entry["blob_sha"],
                "sha256": sha256(data),
            })
        elif entry["review_mode"] == "FULL_PDF":
            pdf_review = pdf_review_by_path.get(path)
            if pdf_review is None:
                raise BuildError(f"PDF lacks result-first human-review evidence: {path}")
            reader = PdfReader(BytesIO(data), strict=True)
            extent["pages"] = len(reader.pages)
            if (
                pdf_review.get("blob_sha1") != entry["blob_sha"]
                or pdf_review.get("sha256") != sha256(data)
                or pdf_review.get("pages") != len(reader.pages)
                or pdf_review.get("page_interval") != [1, len(reader.pages)]
            ):
                raise BuildError(f"PDF human-review identity/extent mismatch: {path}")
            for page_number, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text() or ""
                page_findings = [item for item in pdf_review["findings"] if page_number in item.get("pages", [])]
                pdf_pages.append({
                    "source_id": source_id,
                    "path": path,
                    "page": page_number,
                    "extracted_nonblank_characters": len("".join(page_text.split())),
                    "unresolved_literal_question_mark_pairs": page_text.count("??"),
                    "text_extraction_basis": "PYPDF_NONBLANK_COUNT_ONLY_RUNTIME_DEPENDENT_TEXT_HASH_EXCLUDED",
                    "render_status": pdf_review["render_status"],
                    "human_visual_review": pdf_review["human_visual_review"],
                    "human_review_evidence_id": pdf_review["review_id"],
                    "visual_findings": page_findings,
                })
            read_records.append({
                "source_id": source_id,
                "path": path,
                "review_mode": "FULL_PDF",
                "read_status": "READ_FULL",
                "human_review_evidence_id": pdf_review["review_id"],
                "page_interval": [1, len(reader.pages)],
                "pages": len(reader.pages),
                "blob_sha1": entry["blob_sha"],
                "sha256": sha256(data),
                "visual_findings": pdf_review["findings"],
            })
        else:
            raise BuildError(f"unsupported review mode: {entry['review_mode']}")
        if len(data) != entry["size_bytes"]:
            raise BuildError(f"byte extent mismatch: {path}")
        if extent["lines"] and extent["lines"] != entry["extent"]["lines"]:
            raise BuildError(f"line extent mismatch: {path}")
        if extent["pages"] and extent["pages"] != entry["extent"]["pages"]:
            raise BuildError(f"page extent mismatch: {path}")
        row = {
            "source_id": source_id,
            "path": path,
            "blob_sha1": entry["blob_sha"],
            "sha256": sha256(data),
            "manifest_index": manifest_index,
            "partition": part,
            "review_mode": entry["review_mode"],
            "extension": entry["extension"],
            "role": entry["role"],
            "extent": extent,
            "first_add_commit": first_add,
            "first_add_subject": commit_by_id[first_add]["subject"],
            "last_touch_commit": last_touch,
            "last_touch_subject": commit_by_id[last_touch]["subject"],
            "touch_commit_count": len(history),
            "touch_commits": history,
            "authority_ceiling": authority(part),
            "structure": structure,
        }
        if part == "COMPETING_REVIEW_CANDIDATE":
            row["process_authority_subtype"] = competing_authority_subtype(path)
            row["final_adoption_authority"] = False
            competing_subtype_counts[row["process_authority_subtype"]] += 1
        sources.append(row)
        part_counts[part] += 1
        part_bytes[part] += len(data)
        part_lines[part] += extent["lines"]
        part_nonblank[part] += extent["nonblank_lines"]
        part_pages[part] += extent["pages"]
        mode_counts[entry["review_mode"]] += 1

    if set(pdf_review_by_path) != {row["path"] for row in sources if row["review_mode"] == "FULL_PDF"}:
        raise BuildError("PDF human-review evidence/source bijection")
    for review in human_evidence["text_reviews"]:
        selected = [
            row for row in sources
            if row["review_mode"] == "FULL_TEXT" and row["partition"] in review["partitions"]
        ]
        observed = {
            "expected_files": len(selected),
            "expected_bytes": sum(row["extent"]["bytes"] for row in selected),
            "expected_physical_lines": sum(row["extent"]["lines"] for row in selected),
            "expected_nonblank_lines": sum(row["extent"]["nonblank_lines"] for row in selected),
        }
        if any(review.get(key) != value for key, value in observed.items()):
            raise BuildError(f"text human-review denominator mismatch: {review['review_id']}")
        if review.get("line_coverage_contract") != "EACH_SOURCE_1_TO_EOF":
            raise BuildError(f"text human-review coverage contract: {review['review_id']}")
    if any(row["human_review_evidence_id"] is None for row in read_records):
        raise BuildError("manifest read row lacks human-review evidence")

    supplemental_data = blobs[SUPPLEMENTAL_BLOB]
    supplemental_lines = supplemental_data.decode("utf-8").splitlines()
    supplemental = {
        "source_id": "P063-SUP-0001",
        "path": SUPPLEMENTAL_PATH,
        "manifest_member": False,
        "blob_sha1": SUPPLEMENTAL_BLOB,
        "sha256": sha256(supplemental_data),
        "bytes": len(supplemental_data),
        "physical_lines": len(supplemental_lines),
        "nonblank_lines": sum(bool(line.strip()) for line in supplemental_lines),
        "read_interval": [1, len(supplemental_lines)],
        "read_status": "READ_FULL",
        "human_review_evidence_id": human_evidence["supplemental_review"]["review_id"],
        "authority_ceiling": "PROCESS_CONTROL_REPOSITORY_REPORTED_ONLY",
    }
    supplemental_expected = human_evidence["supplemental_review"]
    if (
        supplemental_expected.get("expected_files") != 1
        or supplemental_expected.get("expected_bytes") != supplemental["bytes"]
        or supplemental_expected.get("expected_physical_lines") != supplemental["physical_lines"]
        or supplemental_expected.get("expected_nonblank_lines") != supplemental["nonblank_lines"]
        or supplemental_expected.get("line_coverage_contract") != "EACH_FILE_1_TO_EOF"
    ):
        raise BuildError("supplemental human-review denominator mismatch")

    observations, observation_ids = build_observations()
    observation_review = human_evidence["observation_review"]
    if (
        observation_review.get("expected_files") != len(observations)
        or observation_review.get("expected_physical_lines") != sum(row["physical_lines"] for row in observations)
        or observation_review.get("line_coverage_contract") != "EACH_FILE_1_TO_EOF"
    ):
        raise BuildError("observation human-review denominator mismatch")
    for observation in observations:
        observation["human_review_evidence_id"] = observation_review["review_id"]
    routes = finding_routes(sources, observation_ids)
    v21_by_rel = {version_relative(row["path"], "v1.0.21"): row for _, row in indexed_v21}
    v22_by_rel = {version_relative(row["path"], "v1.0.22"): row for _, row in indexed_v22}
    common = sorted(set(v21_by_rel) & set(v22_by_rel))
    pairs = [{
        "relative_path": rel,
        "v1021_path": v21_by_rel[rel]["path"],
        "v1022_path": v22_by_rel[rel]["path"],
        "v1021_blob": v21_by_rel[rel]["blob_sha"],
        "v1022_blob": v22_by_rel[rel]["blob_sha"],
        "relation": "BYTE_IDENTICAL" if v21_by_rel[rel]["blob_sha"] == v22_by_rel[rel]["blob_sha"] else "MODIFIED",
    } for rel in common]
    shared_blobs = sorted({row["blob_sha"] for _, row in indexed_v21} & {row["blob_sha"] for _, row in indexed_v22})
    shared_edges = []
    for blob in shared_blobs:
        old_paths = sorted(row["path"] for _, row in indexed_v21 if row["blob_sha"] == blob)
        new_paths = sorted(row["path"] for _, row in indexed_v22 if row["blob_sha"] == blob)
        shared_edges.append({"blob_sha1": blob, "v1021_paths": old_paths, "v1022_paths": new_paths})

    pdf_root_edges = []
    source_by_path = {row["path"]: row for row in sources}
    source_id_by_path = {path: row["source_id"] for path, row in source_by_path.items()}
    for row in sources:
        if row["review_mode"] == "FULL_PDF":
            root = row["path"][:-4] + ".tex"
            pdf_root_edges.append({
                "pdf_source_id": row["source_id"],
                "pdf_path": row["path"],
                "root_tex_source_id": source_id_by_path.get(root),
                "root_tex_path": root,
                "root_state": "MANIFEST_MEMBER" if root in source_id_by_path else "GROUND_NOT_FOUND",
                "pages": row["extent"]["pages"],
                "build_authority": "FROZEN_PDF_PAGE_AND_SOURCE_GENEALOGY_ONLY",
            })

    finding_source_by_path = dict(source_by_path)
    finding_source_by_path[SUPPLEMENTAL_PATH] = supplemental
    process_findings = attach_finding_source_ids(PROCESS_FINDINGS, finding_source_by_path)
    release_findings = attach_finding_source_ids(RELEASE_FINDINGS, finding_source_by_path)
    competing_findings = attach_finding_source_ids(COMPETING_FINDINGS, finding_source_by_path)
    cross_relations, removed_relatives, new_relatives = attach_cross_version_relations(
        indexed_v21, indexed_v22, source_by_path,
    )

    def cross_identity(version: str, relative_path: str) -> dict[str, Any]:
        table = v21_by_rel if version == "v1.0.21" else v22_by_rel
        entry = table[relative_path]
        identity = {
            "relative_path": relative_path,
            "path": entry["path"],
            "blob_sha1": entry["blob_sha"],
            "bytes": entry["size_bytes"],
        }
        if version == "v1.0.22":
            identity["source_id"] = source_by_path[entry["path"]]["source_id"]
        return identity

    plan_r1 = source_by_path["Claude/docs/v1.0.22/plans/PLAN_R1_reorg.md"]
    secondary_gnf_relations = [
        {
            "relation_id": "P063-XVER-GNF-001",
            "relation": "DERIVED_OUTPUT_REPARTITION_GNF",
            "v1021_sources": [
                cross_identity("v1.0.21", "graphite_ica_ch1_v1.0.21.pdf"),
                cross_identity("v1.0.21", "graphite_ica_ch2_v1.0.21.pdf"),
            ],
            "v1022_sources": [
                cross_identity("v1.0.22", "ch1_graphite_v1.0.22.pdf"),
                cross_identity("v1.0.22", "ch2_lco_v1.0.22.pdf"),
                cross_identity("v1.0.22", "ch3_si_v1.0.22.pdf"),
            ],
            "process_evidence": [{
                "source_id": plan_r1["source_id"],
                "path": plan_r1["path"],
                "blob_sha1": plan_r1["blob_sha1"],
                "line_intervals": [[45, 48], [50, 57]],
            }],
            "relation_state": "GROUND_NOT_FOUND_EXACT_PAGE_REPARTITION",
            "reason": "No frozen Synctex/AUX/TOC/FLS/LOG/OUT sidecar maps old PDF pages to new PDF pages.",
            "denominator_consuming": False,
            "downstream_owner": "Phase 063 Step 62 Task 62B clean build/page genealogy",
            "authority_ceiling": "FROZEN_PDF_IDENTITY_AND_PROCESS_CORRESPONDENCE_ONLY",
        },
        {
            "relation_id": "P063-XVER-GNF-002",
            "relation": "DIRECT_V1021_TEST_ORIGIN_GNF",
            "v1021_sources": [cross_identity("v1.0.21", "test_gates_v1021.py")],
            "v1022_sources": [cross_identity("v1.0.22", "test_gates_v1022.py")],
            "process_evidence": [{
                "source_id": plan_r1["source_id"],
                "path": plan_r1["path"],
                "blob_sha1": plan_r1["blob_sha1"],
                "line_intervals": [[30, 30]],
            }],
            "relation_state": "GROUND_NOT_FOUND_DIRECT_V1021_COPY_ORIGIN",
            "reason": "The process plan names the v1.0.22 gate but does not establish the v1.0.21 gate as its direct blob origin.",
            "denominator_consuming": False,
            "downstream_owner": "Phase 063 Step 61 code/runtime concordance",
            "authority_ceiling": "VERSIONED_NAME_CORRESPONDENCE_ONLY",
        },
    ]
    page_sidecar_suffixes = (".aux", ".toc", ".synctex", ".synctex.gz", ".fls", ".log", ".out")
    frozen_page_mapping_sidecars = sorted(
        row["path"] for row in sources if row["path"].lower().endswith(page_sidecar_suffixes)
    )
    citation_genealogy = build_citation_genealogy(sources, text_by_path, tex_edges, pdf_root_edges)

    input_edges = [row for row in tex_edges if row["kind"] == "INPUT"]
    external_document_edges = [row for row in tex_edges if row["kind"] == "EXTERNAL_DOCUMENT"]
    targeted_inputs = {row["resolved_path"] for row in input_edges}
    observed_orphans = [path for path in ORPHAN_TEX_PATHS if path not in targeted_inputs]
    if observed_orphans != list(ORPHAN_TEX_PATHS):
        raise BuildError("declared orphan TeX topology changed")

    source_link_projection = []
    for manifest_index, entry in indexed_v22:
        events = touch_events.get(entry["path"], [])
        source_link_projection.append({
            "manifest_index": manifest_index,
            "path": entry["path"],
            "manifest_blob": entry["blob_sha"],
            "final_blob": entry["blob_sha"],
            "first": list(events[0]) if events else None,
            "last": list(events[-1]) if events else None,
            "touch_count": len(events),
        })
    event_counts = Counter(row["status"][0] for commit in commits for row in commit["changed_paths"])
    adjacency_gaps = []
    for previous, current in zip(commits, commits[1:]):
        if previous["commit"] not in current["parents"]:
            adjacency_gaps.append({
                "previous_touch_commit": previous["commit"],
                "current_touch_commit": current["commit"],
                "current_true_parents": current["parents"],
            })
    history_summary = {
        "commit_count": len(commits),
        "all_single_parent": all(len(row["parents"]) == 1 for row in commits),
        "filtered_adjacent_true_parent_count": len(commits) - 1 - len(adjacency_gaps),
        "filtered_adjacency_gaps": adjacency_gaps,
        "path_event_counts": dict(sorted(event_counts.items())),
        "genealogy_projection_sha256": sha256(projection_bytes(history_projection)),
        "commit_actor_projection_sha256": sha256(projection_bytes([
            {
                "event_id": row["event_id"],
                "commit": row["commit"],
                "repository_actor": row["repository_actor"],
                "process_role": row["process_role"],
            }
            for row in commits
        ])),
        "source_link_projection_sha256": sha256(projection_bytes(source_link_projection)),
        "source_history_row_projection_sha256": sha256(projection_bytes([
            {
                "source_id": row["source_id"],
                "path": row["path"],
                "blob_sha1": row["blob_sha1"],
                "first_add_commit": row["first_add_commit"],
                "first_add_subject": row["first_add_subject"],
                "last_touch_commit": row["last_touch_commit"],
                "last_touch_subject": row["last_touch_subject"],
                "touch_commit_count": row["touch_commit_count"],
                "touch_commits": row["touch_commits"],
            }
            for row in sources
        ])),
        "genealogy_projection_contract": "100 rows: index, commit, parents, author_time, committer_time, subject, ordered diff-tree -M -C changes; compact sorted-key UTF-8 JSON without final LF",
        "source_link_projection_contract": "204 manifest-order rows: manifest index/path/blob, frozen final blob, first/last touch tuple and touch count; compact sorted-key UTF-8 JSON without final LF",
    }

    def read_summary(selected: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "files": len(selected),
            "bytes": sum(row["extent"]["bytes"] for row in selected),
            "text_physical_lines": sum(row["extent"]["lines"] for row in selected),
            "text_nonblank_lines": sum(row["extent"]["nonblank_lines"] for row in selected),
            **({
                "pdf_files": sum(row["review_mode"] == "FULL_PDF" for row in selected),
                "pdf_pages": sum(row["extent"]["pages"] for row in selected),
            } if any(row["review_mode"] == "FULL_PDF" for row in selected) else {}),
            "read_status": "READ_FULL",
        }

    partition_read_summary = {
        "FINAL_RELEASE_SURFACE": read_summary([row for row in sources if row["partition"] == "FINAL_RELEASE_SURFACE"]),
        "COMPETING_REVIEW_CANDIDATE": read_summary([row for row in sources if row["partition"] == "COMPETING_REVIEW_CANDIDATE"]),
        "VERSION_PLAN_AND_STATUS_MACHINE_PROCESS": read_summary([
            row for row in sources if row["partition"] in {"VERSION_PLAN", "STATUS_MACHINE_PROCESS"}
        ]),
        "SUPPLEMENTAL_PROCESS_CONTROL": {
            "files": 1,
            "bytes": supplemental["bytes"],
            "text_physical_lines": supplemental["physical_lines"],
            "text_nonblank_lines": supplemental["nonblank_lines"],
            "read_status": "READ_FULL",
        },
    }
    visual_claims = human_evidence["visual_summary_claims"]
    pdf_visual_summary = {
        "rendered_pages": sum(row["render_status"] == "PASS_POPPLER_RENDER" for row in pdf_pages),
        "visually_read_pages": sum(row["human_visual_review"] == "READ_FULL" for row in pdf_pages),
        "pages_without_extracted_text": sum(row["extracted_nonblank_characters"] == 0 for row in pdf_pages),
        "unresolved_literal_question_mark_pairs": sum(row["unresolved_literal_question_mark_pairs"] for row in pdf_pages),
        "documents_untagged": visual_claims["documents_untagged"],
        "clipping_findings": visual_claims["clipping_findings"],
        "overlap_findings": visual_claims["overlap_findings"],
        "missing_glyph_findings": visual_claims["missing_glyph_findings"],
        "broken_formula_findings": visual_claims["broken_formula_findings"],
        "recorded_visual_findings": sum(len(row["findings"]) for row in human_evidence["pdf_reviews"]),
    }

    topology = {
        "schema_version": 1,
        "artifact_kind": "V1022_SOURCE_PROCESS_TOPOLOGY",
        "generated_date": "2026-08-29",
        "phase": 63,
        "step": 58,
        "status": "PASS_SOURCE_PROCESS_IDENTITY_TOPOLOGY",
        "gate": "PASS_P063_STEP58_SOURCE_PROCESS_TOPOLOGY",
        "baseline_commit": BASELINE,
        "activation_commit": ACTIVATION_COMMIT,
        "builder": {"path": BUILDER.relative_to(REPO).as_posix(), "sha256": sha256(normalize_lf(BUILDER.read_bytes()))},
        "manifest": {"path": MANIFEST.relative_to(REPO).as_posix(), "normalized_sha256": MANIFEST_SHA256, "index_interval": [540, 743]},
        "denominator_policy": {
            "manifest_occurrences": 204,
            "supplemental_process_control_occurrences": 1,
            "combined_label": "204 manifest occurrences + 1 supplemental process-control occurrence",
            "denominator_fusion_forbidden": True,
        },
        "counts": {
            "source_occurrences": len(sources),
            "unique_paths": len({row["path"] for row in sources}),
            "unique_blobs": len({row["blob_sha1"] for row in sources}),
            "bytes": sum(row["extent"]["bytes"] for row in sources),
            "review_modes": dict(sorted(mode_counts.items())),
            "text_physical_lines": sum(row["extent"]["lines"] for row in sources),
            "text_nonblank_lines": sum(row["extent"]["nonblank_lines"] for row in sources),
            "pdf_pages": sum(row["extent"]["pages"] for row in sources),
            "partition_counts": dict(sorted(part_counts.items())),
            "partition_bytes": dict(sorted(part_bytes.items())),
            "partition_physical_lines": dict(sorted(part_lines.items())),
            "partition_nonblank_lines": dict(sorted(part_nonblank.items())),
            "partition_pdf_pages": {key: value for key, value in sorted(part_pages.items()) if value},
            "history_commits": len(commits),
            "observation_inputs": len(observations),
            "finding_routes": len(routes),
            "finding_source_candidates": sum(bool(row["candidate_v1022_source_ids"]) for row in routes),
            "finding_observation_only": sum(not row["candidate_v1022_source_ids"] for row in routes),
            "process_findings": len(process_findings),
            "release_findings": len(release_findings),
            "competing_findings": len(competing_findings),
            "competing_authority_subtypes": dict(sorted(competing_subtype_counts.items())),
        },
        "sources": sources,
        "supplemental_process_control": supplemental,
        "commit_genealogy": commits,
        "history_summary": history_summary,
        "cross_version_v1021_v1022": {
            "identity_namespaces": {
                "v1021": {"occurrences": len(indexed_v21)},
                "v1022": {"occurrences": len(indexed_v22)},
            },
            "same_relative_pairs": pairs,
            "same_relative_count": len(pairs),
            "byte_identical_count": sum(row["relation"] == "BYTE_IDENTICAL" for row in pairs),
            "modified_count": sum(row["relation"] == "MODIFIED" for row in pairs),
            "raw_v1022_only_relative_paths": sorted(set(v22_by_rel) - set(v21_by_rel)),
            "raw_v1021_only_relative_paths": sorted(set(v21_by_rel) - set(v22_by_rel)),
            "explicit_relation_rows": cross_relations,
            "explicit_relation_counts": dict(sorted(Counter(row["relation"] for row in cross_relations).items())),
            "not_carried_forward_relative_paths": removed_relatives,
            "removed_not_carried_forward_count": len(removed_relatives),
            "new_relative_paths": new_relatives,
            "new_count": len(new_relatives),
            "shared_blob_edges": shared_edges,
            "shared_blob_count": len(shared_edges),
            "secondary_ground_not_found_relations": secondary_gnf_relations,
            "frozen_page_mapping_sidecars": frozen_page_mapping_sidecars,
            "coverage": {
                "v1021_primary_count": len(pairs) + sum(len(row["v1021_sources"]) for row in cross_relations) + len(removed_relatives),
                "v1022_primary_count": len(pairs) + sum(len(row["v1022_sources"]) for row in cross_relations) + len(new_relatives),
                "v1021_exactly_once": True,
                "v1022_exactly_once": True,
                "same_relative_shared_blob_secondary_overlap": len(shared_edges),
            },
            "primary_partition_contract": "Each v1.0.21 occurrence is exactly one of same-relative, explicit relation source, or removed; each v1.0.22 occurrence is exactly one of same-relative, explicit relation target, or new. Shared-blob edges are secondary and may overlap same-relative rows.",
            "authority_ceiling": "FROZEN_PATH_BLOB_AND_REPOSITORY_REPORTED_RESTRUCTURE_ONLY",
        },
        "tex_structure_summary": {
            "dependency_edges": len(tex_edges),
            "input_occurrences": len(input_edges),
            "unique_input_targets": len({row["resolved_path"] for row in input_edges}),
            "external_document_edges": len(external_document_edges),
            "unresolved_dependency_edges": sum(row["target_state"] != "MANIFEST_MEMBER" for row in tex_edges),
            "manifest_orphan_tex_paths": observed_orphans,
            "citation_closure": [
                {
                    "driver_path": row["root_tex_path"],
                    "cited_keys": row["citation_key_count"],
                    "defined_keys": row["bibliography_key_count"],
                    "missing_keys": row["missing_keys"],
                    "unused_keys": row["unused_keys"],
                    "duplicate_keys": row["duplicate_keys"],
                }
                for row in citation_genealogy["root_routes"]
                if row["citation_key_count"] or row["bibliography_key_count"]
            ],
            "authority_ceiling": "STATIC_SOURCE_STRUCTURE_ONLY_NOT_LITERATURE_TRUTH",
        },
        "tex_dependency_edges": tex_edges,
        "pdf_root_edges": pdf_root_edges,
        "citation_genealogy": citation_genealogy,
        "human_read_findings": {
            "process": process_findings,
            "release": release_findings,
            "competing": competing_findings,
        },
        "competing_phase057_linkage": {
            "direct_origin_or_subject_correspondence": [f"INTENT-PROV-{number:04d}" for number in range(111, 192)],
            "separate_corroboration_candidates": [f"INTENT-PROV-{number:04d}" for number in range(99, 106)],
            "candidate_linked_count": 88,
            "phase057_denominator": 96,
            "not_counted_from_competing_partition_alone": [
                *[f"INTENT-PROV-{number:04d}" for number in range(96, 99)],
                *[f"INTENT-PROV-{number:04d}" for number in range(106, 111)],
            ],
            "status_promoted": False,
            "authority_ceiling": "SUBJECT_OR_CORROBORATION_LINK_ONLY_NOT_ADOPTION_OR_EXTERNAL_TRUTH",
        },
        "phase057_observation_inputs": observations,
        "phase057_finding_routes": routes,
        "authority_boundary": {
            "source_process_identity_only": True,
            "external_scientific_truth_promoted": False,
            "external_material_truth_promoted": False,
            "external_experimental_truth_promoted": False,
            "primary_literature_truth_promoted": False,
            "canonical_selection_promoted": False,
            "proposal_promoted_to_adoption": False,
        },
    }

    attestation = {
        "schema_version": 1,
        "artifact_kind": "V1022_READ_ATTESTATION",
        "generated_date": "2026-08-29",
        "phase": 63,
        "step": 58,
        "status": "PASS_FULL_READ_ATTESTATION",
        "baseline_commit": BASELINE,
        "source_topology_semantic_sha256": sha256(canonical_bytes(topology)),
        "counts": {
            "manifest_records": len(read_records),
            "text_records": sum(row["review_mode"] == "FULL_TEXT" for row in read_records),
            "text_physical_lines": sum(row.get("physical_lines", 0) for row in read_records),
            "text_nonblank_lines": sum(row.get("nonblank_lines", 0) for row in read_records),
            "pdf_records": sum(row["review_mode"] == "FULL_PDF" for row in read_records),
            "pdf_pages": sum(row.get("pages", 0) for row in read_records),
            "pdf_page_attestations": len(pdf_pages),
            "supplemental_records": 1,
            "observation_records": len(observations),
            "observation_physical_lines": sum(row["physical_lines"] for row in observations),
        },
        "manifest_read_records": read_records,
        "pdf_page_attestations": pdf_pages,
        "supplemental_read_record": supplemental,
        "phase057_observation_read_records": observations,
        "human_review_contract": {
            "result_first_evidence_input": {
                "path": RESULT.relative_to(REPO).as_posix(),
                "evidence_id": human_evidence["evidence_id"],
                "semantic_sha256": human_evidence_sha256,
                "evidence_kind": human_evidence["evidence_kind"],
                "evidence_date": human_evidence["evidence_date"],
            },
            "partition_assignments": {
                "FINAL_RELEASE_SURFACE": "P063-HR-RELEASE-TEXT-001 + P063-HR-PDF-001..004",
                "COMPETING_REVIEW_CANDIDATE": "P063-HR-COMPETING-TEXT-001",
                "VERSION_PLAN_AND_STATUS_MACHINE_PROCESS": "P063-HR-PROCESS-TEXT-001",
                "SUPPLEMENTAL_PROCESS_CONTROL": "P063-HR-SUPPLEMENTAL-001",
                "PHASE057_OBSERVATIONS": "P063-HR-OBSERVATION-001",
            },
            "partition_read_summary": partition_read_summary,
            "pdf_visual_summary": pdf_visual_summary,
            "controller_integration_required": True,
            "builder_reexecutes_human_visual_review": False,
            "unread_manifest_intervals": [],
            "unread_pdf_pages": [],
            "authority_ceiling": "READ_COVERAGE_AND_VISIBLE_LAYOUT_ONLY",
        },
        "authority_boundary": "Full text and PDF-page read coverage only; no scientific, material, experimental, adoption or primary-literature truth promotion.",
    }
    return topology, attestation


def output_paths(output_dir: str | None) -> tuple[Path, Path]:
    if output_dir is None:
        return TOPOLOGY, ATTESTATION
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    return directory / TOPOLOGY.name, directory / ATTESTATION.name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    topology, attestation = build()
    topology_path, attestation_path = output_paths(args.output_dir)
    topology_path.write_bytes(pretty_bytes(topology))
    attestation_path.write_bytes(pretty_bytes(attestation))
    print(
        "PASS_P063_STEP58_BUILD "
        f"sources={topology['counts']['source_occurrences']} commits={topology['counts']['history_commits']} "
        f"text_lines={attestation['counts']['text_physical_lines']} pdf_pages={attestation['counts']['pdf_pages']}"
    )


if __name__ == "__main__":
    main()
