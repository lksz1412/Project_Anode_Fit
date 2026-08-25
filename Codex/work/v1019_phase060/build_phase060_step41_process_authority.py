#!/usr/bin/env python3
"""Build the deterministic Phase 060 Step 41 process-authority matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = ROOT / "Codex/results/PHASE_060_V1019_PROCESS_INTENT_MATRIX.json"
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
NON_PROMOTING_COMPLETION_DECISIONS = {
    "NOT_PROMOTED_STEP42",
    "NOT_PROMOTED_STEP43",
    "NOT_PROMOTED_STEP44",
    "HISTORICAL_CORRECTION_PROCESS_ONLY",
}

PROCESS_SOURCES = [
    ("Claude/plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md", "6b4f6070c2cea5cb80ed3cc2ede769a00910a2ac", "1341dc1c5c1e97901241a690aac1a6c4cb52020d9c03d280bc983eaed46dea16", 79, 64, 14612),
    ("Claude/results/process/V1019_ASSET_CHECKLIST.md", "13738e9162c9f0441d4a18d3a4845ce5986f6eca", "ce3de7012ccafe7ad099ca0fa5dc806d3b3aa38c13baa3247a7747460983adec", 392, 356, 42385),
    ("Claude/results/process/V1019_CH2_ASSET_CHECKLIST.md", "029e5b488b944d2d690b4de578b2d68c44559ee1", "68267df547f2db598a8b1c05ce5444ea6bbcaa35d9e86410565892902f0e202a", 183, 168, 25043),
    ("Claude/results/process/V1019_CH2_FABLE_BRIEF.md", "1545b175f08958a8450b8f7083d53e287cd14d1f", "39224e5747186095c3a6c3c1b1577c7aef8603fe3b98a69c371d53535bf5d7ea", 36, 28, 6041),
    ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", "132f9f264b26a741f00a9e2a3a6c407ad059c9a1", "eb7e373596130689c768604ebbd89c803156ebdca8d69351e420ed0dfe0e0ff2", 48, 35, 6798),
    ("Claude/results/process/V1019_CODE_FABLE_BRIEF.md", "d2da9eae4e43541d2b2f6809c5fcf353aa1336ed", "35aa3c140ad174d0b5246740e1c6c00f42312084d11c81991acfcd4689bbf357", 34, 26, 5989),
    ("Claude/results/process/V1019_CONTINUITY_JUDGMENT.md", "12863c715e3fb6cdb20e2333c7b4799c2cf812cd", "a47e21e2b4df67ef1e9c9e87e19864d2a92a9f3f2b27842fd2edcf56a2bd634b", 40, 33, 3495),
    ("Claude/results/process/V1019_EXECUTION_LEDGER.md", "c53dfb3875211a2063d0732b739e1dcea4158dd7", "2b773feabd816eb3bf1b6d944120bc599f34a9b10fb02ba3fb0f9190dbf30be4", 56, 51, 20541),
    ("Claude/results/process/V1019_FABLE_BRIEF.md", "13db25365eb8597bb268b40cf8ad54d235d52c4c", "065267c1b1261b781a484fc6b08d533b16555809ac27bf707efcd31e75374927", 47, 37, 7073),
    ("Claude/results/process/V1019_FINAL_REVIEW_UNION.md", "1a707a9c9ef8551a14d12b115a6110e9d3a976d6", "66e1b295fba6d122ea4c6f0735e7278086a5f60ee10a6b770d5b007d293f42c6", 53, 43, 6724),
    ("Claude/results/process/V1019_UNION_DEFECTS.md", "aec21103d9e93180f108daf9bd3c03edfddb0435", "dd798889b10835d884dd36668376b9006bd0165d776944b23990e6bf5953536b", 60, 48, 10233),
]

RELEASE_SOURCES = [
    ("Claude/docs/v1.0.19/FITTING_GUIDE.md", "3a404573f6dc9eb296a7ef343421a450eac49232", "2f43e15747594403f54030d800a0179e7039384847a206a40d37a9f199b410be", 135, 104, 24026),
    ("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", "ac88e85adb77d2b191f198f906631b5affe0ef8c", "0fd10b361011480af1c7be4eff6b4f41fce6c2b5d771069ec9ffa6b602fcb1ae", 38, 32, 7995),
    ("Claude/docs/v1.0.19/samples/continuity_scan_report.txt", "c2df9e72ea498541db2e0d178dd441c8d5d9081d", "0ce216ed9f8cdfd655fe6e92e3a74da1c6dc95a14a2d49d995ff64b0b86aa2de", 151, 129, 6474),
    ("Claude/docs/v1.0.19/_sections/ch1_appB_codemap.tex", "ada2cd6ba03a6a386d5702f5edf70762199c4ed2", "fc9a1eda9bb1b1755acf0fa9a7041d975b509acf2f3ec0f3e2f3110980206d3d", 157, 152, 11085),
    ("Claude/docs/v1.0.19/_sections/ch2_appB_codemap.tex", "9a67a1c4c33dc040c86fe9bf6bfc6e386487ffa9", "a0945e77d429eea82cc536bdeb8854d1ffdc669bd888fa8c554ed2124ca31f8e", 69, 63, 5004),
]

WITNESS_SOURCES = [
    ("Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.tex", "f45120801cb7eae113e7aae07065b82a7ea4734c", "be07d638cfadc522f78a31bffc2e05d062bb42bab50f7f4cc78358ed4d29b437", 37, 34, 1987),
]

COMMIT_EVENTS = [
    ("CHR-01", "P1", "7760505808ead4a4bcb54f95d11b7a980cbad9c8", "Ch1 preparation", [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 6, 7), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 42, 43)]),
    ("CHR-02", "P2", "7cfd6bd64a58beea820b13a821becf538d4b7b5c", "Ch1 Fable rewrite", [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 6, 7), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 44, 45)]),
    ("CHR-03", "P3", "34c9665fef40c55939b601e7d170b4c954fcbfa5", "Ch1 ten-review union", [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 6, 7), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 46, 47)]),
    ("CHR-04", "P4", "893ff373425c11f9bc3137b42265d155df4ddd27", "Ch1 final correction", [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 6, 7), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 48, 48)]),
    ("CHR-05", "P5", "06515766bd7e48ed557977c1871a825f24b379da", "Ch1 close", [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 6, 7), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 56, 56)]),
    ("CHR-06", "DOC-LEADS", "5b7f4404539a27f6c9d7063a778011c7f9f560c7", "doc-leads direction correction", [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 6, 7), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 55, 55)]),
    ("CHR-07", "C-P1", "6250d920efae443c6710e641dd2129f7a4c33760", "Ch2 preparation", [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 6, 7), ("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 19, 20)]),
    ("CHR-08", "C-P2", "24883b8aa56cfd0fc5761e3fb8abd13c3b079d4f", "Ch2 Fable rewrite", [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 6, 7), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 49, 50)]),
    ("CHR-09", "C-P3", "2d10a769a0ff81711b2932528390876792efd6c1", "Ch2 ten-review union", [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 6, 7), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 51, 52)]),
    ("CHR-10", "C-P4", "cdaf00cd4941c9910609361a1bfa8c2ace390425", "Ch2 final correction", [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 6, 7), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 53, 53)]),
    ("CHR-11", "C-P5", "a70c77bcc5ae3f33d53c0cf960c393283feb49dd", "Ch2 close", [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 6, 7), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 54, 54)]),
    ("CHR-12", "K-P1", "cb51ca9f2c3a78eb1ce52b1ccf6371ad11ca2de3", "code additive revision", [("Claude/results/process/V1019_EXECUTION_LEDGER.md", 38, 39)]),
    ("CHR-13", "K-P2", "2bf320a52bc78c8d909998eee467a21a0a00b57a", "document-code naming alignment", [("Claude/results/process/V1019_EXECUTION_LEDGER.md", 40, 40)]),
    ("CHR-14", "K-P3", "49e73212a9cb44b955d22ed7881c0cad35a569c6", "sample-image continuity run", [("Claude/results/process/V1019_EXECUTION_LEDGER.md", 41, 41)]),
    ("CHR-15", "R-P1", "6645616d03e6ac4be51a9e8cd9e73b98a3c8408b", "final review corrections", [("Claude/results/process/V1019_EXECUTION_LEDGER.md", 35, 36)]),
    ("CHR-16", "R-P2", "1ad3d20db5736addfe7acbccb74e69411fc773dc", "cycle close", [("Claude/results/process/V1019_EXECUTION_LEDGER.md", 37, 37)]),
]


CLAIM_SPECS: list[dict[str, Any]] = [
    {"claim_id": "CLM-001", "claim_type": "USER_REQUIREMENT", "topic": "Ch1 scope and workflow", "claim": "The recorded user requirement is Ch1-only Fable rewrite, ten-way review, then same-session Fable correction; structure may change while physical/chemical logic is preserved.", "authority_decision": "USER_REQUIREMENT_ONLY", "anchors": [("Claude/plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md", 4, 7), ("Claude/plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md", 15, 19)]},
    {"claim_id": "CLM-002", "claim_type": "PROCESS_EVIDENCE", "topic": "Ch1 five-phase plan", "claim": "The plan defines P1 through P5 with preparation, rewrite, review union, correction, and close gates.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/plans/2026-07-08-v1019-ch1-fable-rewrite-plan.md", 33, 42)]},
    {"claim_id": "CLM-003", "claim_type": "PROCESS_EVIDENCE", "topic": "Ch1 asset inventory", "claim": "The process checklist records 336 Ch1 asset identities extracted as A-001..159 and B2-001..177 by two Sonnet readers plus master verification, with head-to-tail coverage asserted.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_ASSET_CHECKLIST.md", 1, 5), ("Claude/results/process/V1019_ASSET_CHECKLIST.md", 389, 392)]},
    {"claim_id": "CLM-004", "claim_type": "PROCESS_EVIDENCE", "topic": "Ch1 critical anchors", "claim": "The Ch1 checklist identifies twelve critical misunderstanding-prevention anchor families.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_ASSET_CHECKLIST.md", 9, 22)]},
    {"claim_id": "CLM-005", "claim_type": "PROCESS_EVIDENCE", "topic": "Ch1 authoring brief", "claim": "The Fable brief requires the 336 checklist identities and enumerates critical equations, tables, figures, and bibliography targets.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_FABLE_BRIEF.md", 39, 47)]},
    {"claim_id": "CLM-006", "claim_type": "SCIENTIFIC_CLAIM", "topic": "Ch1 union scientific completion", "claim": "The Ch1 union asserts zero physical/chemical/mathematical skeleton errors and zero asset regression after reviewer rederivation.", "authority_decision": "NOT_PROMOTED_STEP44", "anchors": [("Claude/results/process/V1019_UNION_DEFECTS.md", 5, 8)]},
    {"claim_id": "CLM-007", "claim_type": "PROCESS_EVIDENCE", "topic": "Ch1 reviewer roles", "claim": "The Ch1 union records W7 Opus and W10 Fable as independent rederivation roles within a ten-window review.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_UNION_DEFECTS.md", 3, 8)]},
    {"claim_id": "CLM-008", "claim_type": "RUNTIME_CLAIM", "topic": "Ch1 code cross-check", "claim": "The Ch1 union reports five master code checks for identifier use, lag units, LCO entropy sign, representative temperature, and LCO demo ordering.", "authority_decision": "NOT_PROMOTED_STEP43", "anchors": [("Claude/results/process/V1019_UNION_DEFECTS.md", 10, 15)]},
    {"claim_id": "CLM-009", "claim_type": "PROCESS_EVIDENCE", "topic": "Ch1 defect inventory", "claim": "The Ch1 union records 24 defects with severity HIGH 3, MED 8, LOW-MED 3, LOW 9, NOTE 1 and routes U-1 through U-24.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_UNION_DEFECTS.md", 5, 8), ("Claude/results/process/V1019_UNION_DEFECTS.md", 19, 55)]},
    {"claim_id": "CLM-010", "claim_type": "PROCESS_EVIDENCE", "topic": "Ch2 asset inventory", "claim": "The process checklist records 133 Ch2 assets and fifteen critical anchors, attributed to Sonnet full read plus master verification.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_CH2_ASSET_CHECKLIST.md", 1, 4), ("Claude/results/process/V1019_CH2_ASSET_CHECKLIST.md", 180, 183)]},
    {"claim_id": "CLM-011", "claim_type": "USER_REQUIREMENT", "topic": "Ch2 doc-leads rule", "claim": "The Ch2 authoring brief records doc-leads: the document is authoritative and later code should implement it while preserving established assets and implementability.", "authority_decision": "USER_REQUIREMENT_ONLY", "anchors": [("Claude/results/process/V1019_CH2_FABLE_BRIEF.md", 5, 9)]},
    {"claim_id": "CLM-012", "claim_type": "SCIENTIFIC_CLAIM", "topic": "Ch2 union scientific completion", "claim": "The Ch2 union asserts central equations and numerical results were rederived, zero asset regression occurred, and one new sign error CU-1 remained for correction.", "authority_decision": "NOT_PROMOTED_STEP44", "anchors": [("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 5, 8)]},
    {"claim_id": "CLM-013", "claim_type": "PROCESS_EVIDENCE", "topic": "Ch2 reviewer roles", "claim": "The Ch2 union records W4 Opus and W10 Fable as independent rederivation roles within ten review windows.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 1, 8)]},
    {"claim_id": "CLM-014", "claim_type": "SCIENTIFIC_CLAIM", "topic": "CU-1 historical sign correction", "claim": "The Ch2 union identifies a sign conflict in the vibrational entropy prototype and prescribes the positive entropy derivative form.", "authority_decision": "HISTORICAL_CORRECTION_PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 10, 18)]},
    {"claim_id": "CLM-015", "claim_type": "RUNTIME_CLAIM", "topic": "Code brief numeric and API claims", "claim": "The code brief asserts seven numerical groups already align and identifies two additive API gaps: composition-to-OCV solving and term-separated entropy output.", "authority_decision": "NOT_PROMOTED_STEP42", "anchors": [("Claude/results/process/V1019_CODE_FABLE_BRIEF.md", 17, 24)]},
    {"claim_id": "CLM-016", "claim_type": "USER_REQUIREMENT", "topic": "Code regression requirements", "claim": "The code brief requires bit-exact legacy regression, listed numerical reproduction, and a successful self-test.", "authority_decision": "USER_REQUIREMENT_ONLY", "anchors": [("Claude/results/process/V1019_CODE_FABLE_BRIEF.md", 26, 29)]},
    {"claim_id": "CLM-017", "claim_type": "RUNTIME_CLAIM", "topic": "Continuity judgment", "claim": "The process judgment claims all inspected curves were continuous, with zero discontinuities and no logic rereview required.", "authority_decision": "NOT_PROMOTED_STEP42", "anchors": [("Claude/results/process/V1019_CONTINUITY_JUDGMENT.md", 15, 37)]},
    {"claim_id": "CLM-018", "claim_type": "PROCESS_EVIDENCE", "topic": "Phase completion table", "claim": "The process ledger marks Ch1 P1-P5, Ch2 C-P1-C-P5, and K/R tracking rows complete.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_EXECUTION_LEDGER.md", 6, 32)]},
    {"claim_id": "CLM-019", "claim_type": "PROCESS_EVIDENCE", "topic": "Ch1 completion details", "claim": "The process ledger records Ch1 asset, section, page, review, defect, correction, and build completion statements.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_EXECUTION_LEDGER.md", 42, 48), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 56, 56)]},
    {"claim_id": "CLM-020", "claim_type": "PROCESS_EVIDENCE", "topic": "Ch2 completion details", "claim": "The process ledger records Ch2 asset, section, page, review, CU-1 correction, and build completion statements.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_EXECUTION_LEDGER.md", 49, 55)]},
    {"claim_id": "CLM-021", "claim_type": "RUNTIME_CLAIM", "topic": "Code and sample completion", "claim": "The process ledger asserts additive code completion, self-test and regression results, generated images, and bounded continuity outcomes.", "authority_decision": "NOT_PROMOTED_STEP42", "anchors": [("Claude/results/process/V1019_EXECUTION_LEDGER.md", 38, 41)]},
    {"claim_id": "CLM-022", "claim_type": "SCIENTIFIC_CLAIM", "topic": "Final review completion", "claim": "The final review union asserts zero Ch1-Ch2 contradiction, bit-exact document-code alignment, full asset coverage, and zero critical physical errors.", "authority_decision": "NOT_PROMOTED_STEP44", "anchors": [("Claude/results/process/V1019_FINAL_REVIEW_UNION.md", 5, 7)]},
    {"claim_id": "CLM-023", "claim_type": "PROCESS_EVIDENCE", "topic": "Final review defect and correction inventory", "claim": "The final union records version, appendix, fitting demo, API, honesty, and pedagogy corrections assigned to master and Fable roles.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_FINAL_REVIEW_UNION.md", 9, 53)]},
    {"claim_id": "CLM-024", "claim_type": "PROCESS_EVIDENCE", "topic": "Release handover chronology", "claim": "The release handover records Ch1 and Ch2 process artifact counts, defect unions, and the named commit sequence.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 3, 7)]},
    {"claim_id": "CLM-025", "claim_type": "PROCESS_EVIDENCE", "topic": "Release Ch1 stage completion", "claim": "The handover records P1-P5 completion statements and Ch1 asset/reviewer/build counts.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 9, 17)]},
    {"claim_id": "CLM-026", "claim_type": "PROCESS_EVIDENCE", "topic": "Release Ch2 stage completion", "claim": "The handover records C-P1-C-P5 completion statements, CU-1 correction, and Ch2 asset/reviewer/build counts.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 19, 24)]},
    {"claim_id": "CLM-027", "claim_type": "RUNTIME_CLAIM", "topic": "Broad code completion assertion", "claim": "The release root and handover assert that the v1.0.19 code was revised to the document with additive composition entry points and bit-exact regression.", "authority_decision": "NOT_PROMOTED_STEP43", "anchors": [("Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.tex", 6, 7), ("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 26, 27)]},
    {"claim_id": "CLM-028", "claim_type": "UNVERIFIED", "topic": "Release unresolved work", "claim": "The handover leaves LCO temperature restoration, total irreversible heat decomposition, LCO tier-2/3 measured initial values, and appendix integration unresolved.", "authority_decision": "UNVERIFIED", "anchors": [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 34, 38)]},
    {"claim_id": "CLM-029", "claim_type": "RUNTIME_CLAIM", "topic": "Fitting guide implementation boundary", "claim": "The fitting guide describes the additive APIs but explicitly states that multi-temperature LCO electronic temperature restoration remains unimplemented.", "authority_decision": "NOT_PROMOTED_STEP43", "anchors": [("Claude/docs/v1.0.19/FITTING_GUIDE.md", 1, 3), ("Claude/docs/v1.0.19/FITTING_GUIDE.md", 61, 68)]},
    {"claim_id": "CLM-030", "claim_type": "UNVERIFIED", "topic": "LCO tier gaps", "claim": "The fitting guide states that LCO Omega and activation-energy anchors are not found and are only tentative fitting starting scales.", "authority_decision": "UNVERIFIED", "anchors": [("Claude/docs/v1.0.19/FITTING_GUIDE.md", 21, 31)]},
    {"claim_id": "CLM-031", "claim_type": "RUNTIME_CLAIM", "topic": "Bounded numerical scan", "claim": "The stored continuity report records finite grids, zero spike candidates at a 20x local-median threshold, a monotonic bisection output on x_bar 0.02..0.98, and worked-example numbers.", "authority_decision": "NOT_PROMOTED_STEP42", "anchors": [("Claude/docs/v1.0.19/samples/continuity_scan_report.txt", 13, 15), ("Claude/docs/v1.0.19/samples/continuity_scan_report.txt", 17, 129), ("Claude/docs/v1.0.19/samples/continuity_scan_report.txt", 137, 142)]},
    {"claim_id": "CLM-032", "claim_type": "RUNTIME_CLAIM", "topic": "Ch1 implementation mapping", "claim": "The Ch1 code map asserts a one-to-one lookup between document quantities and named implementation entry points, nodes, and additive composition APIs.", "authority_decision": "NOT_PROMOTED_STEP43", "anchors": [("Claude/docs/v1.0.19/_sections/ch1_appB_codemap.tex", 4, 16), ("Claude/docs/v1.0.19/_sections/ch1_appB_codemap.tex", 117, 148)]},
    {"claim_id": "CLM-033", "claim_type": "USER_REQUIREMENT", "topic": "Ch2 future implementation specification", "claim": "The Ch2 code-map appendix says it does not describe current implementation and instead specifies what a later revision must reproduce.", "authority_decision": "USER_REQUIREMENT_ONLY", "anchors": [("Claude/docs/v1.0.19/_sections/ch2_appB_codemap.tex", 7, 22)]},
    {"claim_id": "CLM-034", "claim_type": "PROCESS_EVIDENCE", "topic": "Asset presence boundary", "claim": "Checklist identities and section comments can establish process presence and preservation assertions, but not physical validity or citation truth.", "authority_decision": "PROCESS_ONLY", "anchors": [("Claude/results/process/V1019_ASSET_CHECKLIST.md", 1, 5), ("Claude/results/process/V1019_CH2_ASSET_CHECKLIST.md", 1, 4)]},
    {"claim_id": "CLM-035", "claim_type": "RUNTIME_CLAIM", "topic": "Regression script assertion", "claim": "The fitting guide asserts a 13-of-13 bit-exact golden regression and lists the release validation scripts.", "authority_decision": "NOT_PROMOTED_STEP42", "anchors": [("Claude/docs/v1.0.19/FITTING_GUIDE.md", 110, 124)]},
    {"claim_id": "CLM-036", "claim_type": "UNVERIFIED", "topic": "Graph-suite V7 implementation status", "claim": "The guide labels V7 multi-temperature curvature as valid only after future implementation and describes the present frozen approximation as linear.", "authority_decision": "UNVERIFIED", "anchors": [("Claude/docs/v1.0.19/FITTING_GUIDE.md", 126, 135)]},
]

CH2_DEFECT_CORRECTION_SPECS: list[dict[str, Any]] = [
    {"obligation_id": "DCR-CU-02", "defect_id": "CU-2", "defect_summary": "The union records a site-versus-molar mixed intermediate expression and an unstated chemical-potential cancellation.", "prescribed_correction": "Delete the mixed intermediate expression, or rewrite it with numerator and denominator multiplied by N_A while explicitly showing N_A epsilon_0 minus mu equals mu_0 minus mu equals sF(V-U_j) over RT.", "reviewer_attribution": ["W1-2", "W10-2"], "source_anchor": ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 20, 21)},
    {"obligation_id": "DCR-CU-03", "defect_id": "CU-3", "defect_summary": "The union records literal Ch1 internal label names printed as prose across Ch2.", "prescribed_correction": "Replace prose references of the form 'equation eq:XXX' with descriptive Chapter 1 section-and-equation wording while retaining Ch2-local eqref references.", "reviewer_attribution": ["W3-1", "W9 관련"], "source_anchor": ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 23, 24)},
    {"obligation_id": "DCR-CU-04", "defect_id": "CU-4", "defect_summary": "The union records the Ch2-local eq:Se label colliding with the Ch1 eq:Se label.", "prescribed_correction": "Rename the Ch2-local label, for example to eq:Se-ch2, and add the collision to Appendix A or separate the two references with a footnote.", "reviewer_attribution": ["W9-1"], "source_anchor": ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 26, 27)},
    {"obligation_id": "DCR-CU-05", "defect_id": "CU-5", "defect_summary": "The union records tension between 'sum' wording and an underbrace that labels the unsigned raw entropy term as reversible heat.", "prescribed_correction": "Move the minus sign into the underbraced reversible-heat term, or replace 'sum' with wording that explicitly denotes a signed combination.", "reviewer_attribution": ["W6-1"], "source_anchor": ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 29, 30)},
    {"obligation_id": "DCR-CU-06", "defect_id": "CU-6", "defect_summary": "The union records duplicate transition prose at the end of section 2.6 and start of section 2.7.", "prescribed_correction": "Make the section 2.6 ending a local close and leave the forward transition solely to the section 2.7 opening.", "reviewer_attribution": ["W6-2"], "source_anchor": ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 32, 33)},
    {"obligation_id": "DCR-CU-07", "defect_id": "CU-7", "defect_summary": "The union records an Appendix A 'common error' claim absent from its cited source section and therefore inconsistent with the appendix's pure-republication rule.", "prescribed_correction": "Correct the basis to ssec:sconfig/ssec:dvdt and add the claimed warning to the body, or narrow the appendix wording to a statement already present in the body.", "reviewer_attribution": ["W8-1"], "source_anchor": ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 35, 36)},
    {"obligation_id": "DCR-CU-08", "defect_id": "CU-8", "defect_summary": "The union records an overgeneralized analogy between the Ch1 and Ch2 entropy skeletons.", "prescribed_correction": "Qualify the analogy as limited to configurational centering and distribution separation.", "reviewer_attribution": ["W2-1"], "source_anchor": ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 39, 39)},
    {"obligation_id": "DCR-CU-09", "defect_id": "CU-9", "defect_summary": "The union records an ambiguous singular 'next section' transition spanning two following sections.", "prescribed_correction": "Name both following sections explicitly.", "reviewer_attribution": ["W3-2"], "source_anchor": ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 40, 40)},
    {"obligation_id": "DCR-CU-10", "defect_id": "CU-10", "defect_summary": "The union records that eq:weighted lacks its derivation-A marker.", "prescribed_correction": "Add the derivation-A marker to the title or equivalent heading.", "reviewer_attribution": ["W5-1"], "source_anchor": ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 41, 41)},
    {"obligation_id": "DCR-CU-11", "defect_id": "CU-11", "defect_summary": "The union records that all initial Omega values exceed the two-phase threshold while the prose identifies a specific two-phase transition.", "prescribed_correction": "State that the initial Omega values all exceed 2RT and that transition-specific two-phase identification depends on measured plateau/staging literature and the Ch1 A-106 post-fit basis.", "reviewer_attribution": ["W10-1"], "source_anchor": ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 42, 42)},
]

CONTRADICTION_SPECS: list[dict[str, Any]] = [
    {"contradiction_id": "CTR-001", "title": "Code completed versus future implementation specification", "positions": [
        {"position": "COMPLETED", "anchors": [("Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.tex", 6, 7), ("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 26, 27)]},
        {"position": "FUTURE_REQUIREMENT_NOT_CURRENT_IMPLEMENTATION", "anchors": [("Claude/docs/v1.0.19/_sections/ch2_appB_codemap.tex", 7, 10)]},
    ], "status": "OPEN", "route": ["STEP42_RUNTIME_AND_ARTIFACT_AUDIT", "STEP43_DOCUMENT_TO_REACHABLE_CODE"], "adjudication": "PRESERVE_BOTH_NO_LATEST_OR_MAJORITY_PREFERENCE"},
    {"contradiction_id": "CTR-002", "title": "Broad completion wording versus explicit unimplemented and unresolved code scope", "positions": [
        {"position": "BROAD_CODE_COMPLETION", "anchors": [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 26, 27)]},
        {"position": "LCO_T_RESTORATION_AND_TOTAL_HEAT_UNRESOLVED", "anchors": [("Claude/docs/v1.0.19/FITTING_GUIDE.md", 61, 66), ("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 34, 35)]},
    ], "status": "OPEN", "route": ["STEP42_RUNTIME_AND_ARTIFACT_AUDIT", "STEP43_DOCUMENT_TO_REACHABLE_CODE"], "adjudication": "COMPLETION_MUST_REMAIN_COMPONENT_SCOPED"},
    {"contradiction_id": "CTR-003", "title": "General continuity conclusion versus bounded numerical sampling", "positions": [
        {"position": "GENERAL_NO_REREVIEW_NEEDED", "anchors": [("Claude/results/process/V1019_CONTINUITY_JUDGMENT.md", 15, 37)]},
        {"position": "BOUNDED_GRIDS_AND_THRESHOLD_ONLY", "anchors": [("Claude/docs/v1.0.19/samples/continuity_scan_report.txt", 13, 15), ("Claude/docs/v1.0.19/samples/continuity_scan_report.txt", 17, 129)]},
    ], "status": "OPEN", "route": ["STEP42_RUNTIME_AND_ARTIFACT_AUDIT", "STEP44_PHYSICS_REDERIVATION"], "adjudication": "BOUNDED_OUTPUT_CANNOT_ESTABLISH_GENERAL_PHYSICAL_VALIDITY"},
    {"contradiction_id": "CTR-004", "title": "Zero critical physical-error completion language versus recorded CU-1 sign defect", "positions": [
        {"position": "ZERO_CRITICAL_PHYSICAL_ERRORS", "anchors": [("Claude/results/process/V1019_FINAL_REVIEW_UNION.md", 5, 7)]},
        {"position": "CU1_PHYSICAL_SIGN_ERROR_RECORDED", "anchors": [("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 5, 8), ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 17, 18)]},
    ], "status": "HISTORICAL_CORRECTION_RECORDED_NOT_SCIENTIFICALLY_PROMOTED", "route": ["STEP44_PHYSICS_REDERIVATION"], "adjudication": "RETAIN_PRE_AND_POST_CORRECTION_CLAIMS_WITH_CHRONOLOGY"},
    {"contradiction_id": "CTR-005", "title": "Ch1 severity headline versus detailed defect enumeration", "positions": [
        {"position": "HEADLINE_HIGH3_MED8_LOWMED3_LOW9_NOTE1", "anchors": [("Claude/results/process/V1019_UNION_DEFECTS.md", 5, 8), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 47, 47)]},
        {"position": "ENUMERATED_HIGH3_MED7_LOWMED3_LOW10_NOTE1", "anchors": [("Claude/results/process/V1019_UNION_DEFECTS.md", 19, 55)]},
    ], "status": "OPEN", "route": ["STEP45_1_CLAIM_DEFECT_DISPOSITION"], "adjudication": "PRESERVE_HEADLINE_AND_ENUMERATION_NO_ARITHMETIC_REWRITE"},
    {"contradiction_id": "CTR-006", "title": "Ch2 MEDIUM headline/category slot versus detailed CU enumeration", "positions": [
        {"position": "HEADLINE_HIGH1_MED6_LOW_UNSLOTTED", "anchors": [("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 5, 8), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 52, 52), ("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 7, 7), ("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 22, 22)]},
        {"position": "ENUMERATED_HIGH1_MED5_LOWMED1_LOW4", "anchors": [("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 17, 42), ("Claude/results/process/V1019_EXECUTION_LEDGER.md", 52, 52)]},
    ], "status": "OPEN", "route": ["STEP45_1_CLAIM_DEFECT_DISPOSITION"], "adjudication": "PRESERVE_HEADLINE_AND_ENUMERATION_NO_CATEGORY_REASSIGNMENT"},
]

UNRESOLVED_SPECS: list[dict[str, Any]] = [
    {"unresolved_id": "UNR-001", "item": "Multi-temperature LCO electronic temperature restoration is unimplemented.", "route": "STEP43_DOCUMENT_TO_REACHABLE_CODE", "anchors": [("Claude/docs/v1.0.19/FITTING_GUIDE.md", 61, 66), ("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 26, 27)]},
    {"unresolved_id": "UNR-002", "item": "Total heat irreversible q_irr decomposition remains future work.", "route": "STEP43_DOCUMENT_TO_REACHABLE_CODE", "anchors": [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 34, 35)]},
    {"unresolved_id": "UNR-003", "item": "LCO tier-2/3 Omega and activation-energy measured anchors are not found.", "route": "STEP44_PHYSICS_REDERIVATION_AND_PHASE071_REFERENCE_TRUTH", "anchors": [("Claude/docs/v1.0.19/FITTING_GUIDE.md", 21, 31), ("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 34, 35)]},
    {"unresolved_id": "UNR-004", "item": "The actual reachable code must adjudicate current implementation versus future requirement wording.", "route": "STEP43_DOCUMENT_TO_REACHABLE_CODE", "anchors": [("Claude/docs/v1.0.19/_sections/ch1_appB_codemap.tex", 4, 16), ("Claude/docs/v1.0.19/_sections/ch2_appB_codemap.tex", 7, 22)]},
    {"unresolved_id": "UNR-005", "item": "Continuity output requires independent rerun and broader runtime/artifact inspection.", "route": "STEP42_RUNTIME_AND_ARTIFACT_AUDIT", "anchors": [("Claude/docs/v1.0.19/samples/continuity_scan_report.txt", 13, 15), ("Claude/results/process/V1019_CONTINUITY_JUDGMENT.md", 15, 37)]},
    {"unresolved_id": "UNR-006", "item": "Physical derivations and claimed zero-error outcomes require independent rederivation; literature and DOI truth remain separate.", "route": "STEP44_PHYSICS_REDERIVATION_AND_PHASE071_REFERENCE_TRUTH", "anchors": [("Claude/results/process/V1019_UNION_DEFECTS.md", 5, 8), ("Claude/results/process/V1019_CH2_UNION_DEFECTS.md", 5, 8)]},
    {"unresolved_id": "UNR-007", "item": "Standalone appendix integration remains a user decision.", "route": "USER_DECISION_LATER_PHASE", "anchors": [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 34, 38), ("Claude/results/process/V1019_FINAL_REVIEW_UNION.md", 47, 49)]},
    {"unresolved_id": "UNR-008", "item": "Whether broadening should receive N6a/N6b sublabels remains an optional naming decision.", "route": "STEP45_1_CLAIM_DEFECT_DISPOSITION", "anchors": [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 36, 36), ("Claude/results/process/V1019_UNION_DEFECTS.md", 54, 55)]},
    {"unresolved_id": "UNR-009", "item": "The W2-2 sec:center-eqcond/Uj labels remain harmless orphans with reverse-reference wiring or pruning deferred.", "route": "STEP45_1_CLAIM_DEFECT_DISPOSITION", "anchors": [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 37, 37), ("Claude/results/process/V1019_UNION_DEFECTS.md", 57, 60)]},
    {"unresolved_id": "UNR-010", "item": "Future-physics proposals 2 through 5 remain externally delegated and measurement-pending.", "route": "STEP45_1_CLAIM_DEFECT_DISPOSITION", "anchors": [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 38, 38)]},
    {"unresolved_id": "UNR-011", "item": "The v1.0.16 physics-data obligation remains externally delegated and measurement-pending.", "route": "STEP45_1_CLAIM_DEFECT_DISPOSITION_AND_PHASE071_072_REFERENCE_DATA_TRUTH", "anchors": [("Claude/docs/v1.0.19/HANDOVER_v1.0.19.md", 38, 38)]},
]


def git_bytes(blob_sha1: str) -> bytes:
    proc = subprocess.run(
        ["git", "cat-file", "blob", blob_sha1],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout


def git_path_blob(path: str) -> str:
    proc = subprocess.run(
        ["git", "rev-parse", f"{SOURCE_COMMIT}:{path}"],
        cwd=ROOT,
        check=True,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout.strip()


def git_commit_subject(commit: str) -> str:
    proc = subprocess.run(
        ["git", "show", "-s", "--format=%s", commit],
        cwd=ROOT,
        check=True,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout.strip()


def source_record(spec: tuple[str, str, str, int, int, int], group: str) -> tuple[dict[str, Any], list[str]]:
    path, blob_sha1, expected_sha256, physical, nonblank, size_bytes = spec
    worktree_path = ROOT / Path(path)
    if not worktree_path.is_file():
        raise RuntimeError(f"missing source: {path}")
    committed_blob = git_path_blob(path)
    if committed_blob != blob_sha1:
        raise RuntimeError(
            f"source path/blob mismatch: {SOURCE_COMMIT}:{path}: "
            f"expected={blob_sha1} actual={committed_blob}"
        )
    data = git_bytes(blob_sha1)
    lines = data.decode("utf-8").splitlines()
    actual = (
        hashlib.sha256(data).hexdigest(),
        len(lines),
        sum(1 for line in lines if line.strip()),
        len(data),
    )
    expected = (expected_sha256, physical, nonblank, size_bytes)
    if actual != expected:
        raise RuntimeError(f"source contract mismatch: {path}: expected={expected!r} actual={actual!r}")
    return (
        {
            "path": path,
            "group": group,
            "git_blob_sha1": blob_sha1,
            "sha256": expected_sha256,
            "size_bytes": size_bytes,
            "physical_lines": physical,
            "nonblank_lines": nonblank,
            "read_coverage": [{"start_line": 1, "end_line": physical}],
            "coverage_status": "READ_FULL",
            "authority_boundary": (
                "Process prose is evidence of recorded intent/activity only."
                if group == "PROCESS_INPUT"
                else "Release text is an independent release-source witness, not automatic scientific/runtime truth."
                if group == "RELEASE_INPUT"
                else "Step 40 full-read witness used only to preserve an explicit authority contradiction."
            ),
        },
        lines,
    )


def anchor(path: str, start: int, end: int, lines_by_path: dict[str, list[str]]) -> dict[str, Any]:
    lines = lines_by_path[path]
    if start < 1 or end < start or end > len(lines):
        raise RuntimeError(f"invalid anchor: {path}:{start}-{end}")
    selected = "\n".join(lines[start - 1 : end])
    excerpt = selected.replace("\t", " ")
    if len(excerpt) > 240:
        excerpt = excerpt[:237] + "..."
    return {
        "path": path,
        "start_line": start,
        "end_line": end,
        "anchor_text_sha256": hashlib.sha256(selected.encode("utf-8")).hexdigest(),
        "excerpt": excerpt,
    }


def anchors(specs: list[tuple[str, int, int]], lines_by_path: dict[str, list[str]]) -> list[dict[str, Any]]:
    return [anchor(path, start, end, lines_by_path) for path, start, end in specs]


def build() -> dict[str, Any]:
    source_inventory: list[dict[str, Any]] = []
    lines_by_path: dict[str, list[str]] = {}
    for group, specs in (
        ("PROCESS_INPUT", PROCESS_SOURCES),
        ("RELEASE_INPUT", RELEASE_SOURCES),
        ("CARRIED_STEP40_WITNESS", WITNESS_SOURCES),
    ):
        for spec in specs:
            record, lines = source_record(spec, group)
            source_inventory.append(record)
            lines_by_path[record["path"]] = lines

    claims = []
    for spec in CLAIM_SPECS:
        claim = dict(spec)
        claim["anchors"] = anchors(spec["anchors"], lines_by_path)
        release_anchor_count = sum(
            1 for item in claim["anchors"] if item["path"] in {source[0] for source in RELEASE_SOURCES}
        )
        claim["independent_release_evidence"] = {
            "anchor_count": release_anchor_count,
            "status": (
                "PRESENT_BUT_NOT_INDEPENDENTLY_EXECUTED"
                if release_anchor_count
                else "ABSENT"
            ),
        }
        claims.append(claim)

    defect_correction_records = []
    for spec in CH2_DEFECT_CORRECTION_SPECS:
        item = {
            key: value
            for key, value in spec.items()
            if key != "source_anchor"
        }
        source_evidence = anchor(*spec["source_anchor"], lines_by_path)
        completion_evidence = anchor(
            "Claude/results/process/V1019_EXECUTION_LEDGER.md",
            53,
            53,
            lines_by_path,
        )
        item.update(
            {
                "claim_type": "PROCESS_EVIDENCE",
                "authority_decision": "PROCESS_ONLY_NOT_SCIENTIFIC_OR_RUNTIME_PROOF",
                "defect_evidence": source_evidence,
                "prescribed_correction_evidence": dict(source_evidence),
                "reviewer_evidence": dict(source_evidence),
                "completion_assertion": "The process ledger asserts that C-P4 incorporated CU-1 through CU-11 with zero rejections.",
                "completion_evidence": completion_evidence,
            }
        )
        defect_correction_records.append(item)

    contradictions = []
    for spec in CONTRADICTION_SPECS:
        item = {key: value for key, value in spec.items() if key != "positions"}
        item["positions"] = []
        for position in spec["positions"]:
            item["positions"].append(
                {
                    "position": position["position"],
                    "anchors": anchors(position["anchors"], lines_by_path),
                }
            )
        contradictions.append(item)

    unresolved = []
    for spec in UNRESOLVED_SPECS:
        item = dict(spec)
        item["anchors"] = anchors(spec["anchors"], lines_by_path)
        unresolved.append(item)

    chronology = []
    for event_id, stage, commit, purpose, anchor_specs in COMMIT_EVENTS:
        chronology.append(
            {
                "event_id": event_id,
                "stage": stage,
                "commit": commit,
                "subject": git_commit_subject(commit),
                "purpose": purpose,
                "claim_type": "PROCESS_EVIDENCE",
                "scientific_truth": False,
                "runtime_truth": False,
                "anchors": anchors(anchor_specs, lines_by_path),
            }
        )

    referenced_paths: set[str] = set()
    for claim in claims:
        referenced_paths.update(item["path"] for item in claim["anchors"])
    for item in defect_correction_records:
        referenced_paths.add(item["defect_evidence"]["path"])
        referenced_paths.add(item["completion_evidence"]["path"])
    for contradiction in contradictions:
        for position in contradiction["positions"]:
            referenced_paths.update(item["path"] for item in position["anchors"])
    for item in unresolved:
        referenced_paths.update(anchor_item["path"] for anchor_item in item["anchors"])
    for event in chronology:
        referenced_paths.update(anchor_item["path"] for anchor_item in event["anchors"])
    mandatory_paths = {source[0] for source in PROCESS_SOURCES + RELEASE_SOURCES}
    source_orphans = sorted(mandatory_paths - referenced_paths)
    unsupported_promotions = [
        claim["claim_id"]
        for claim in claims
        if claim["claim_type"] in {"SCIENTIFIC_CLAIM", "RUNTIME_CLAIM"}
        and claim["authority_decision"] not in NON_PROMOTING_COMPLETION_DECISIONS
    ]
    contradiction_unrouted = [item["contradiction_id"] for item in contradictions if not item["route"]]
    required_defect_correction_ids = {spec["obligation_id"] for spec in CH2_DEFECT_CORRECTION_SPECS}
    actual_defect_correction_ids = {item["obligation_id"] for item in defect_correction_records}
    defect_correction_orphans = sorted(required_defect_correction_ids - actual_defect_correction_ids)
    required_unresolved_ids = {spec["unresolved_id"] for spec in UNRESOLVED_SPECS}
    actual_unresolved_ids = {item["unresolved_id"] for item in unresolved}
    unresolved_obligation_orphans = sorted(required_unresolved_ids - actual_unresolved_ids)
    required_contradiction_ids = {spec["contradiction_id"] for spec in CONTRADICTION_SPECS}
    actual_contradiction_ids = {item["contradiction_id"] for item in contradictions}
    contradiction_obligation_orphans = sorted(required_contradiction_ids - actual_contradiction_ids)

    return {
        "schema_version": "phase060-step41-process-authority-v1",
        "phase": 60,
        "step": 41,
        "generation_metadata": {
            "builder": "Codex/work/v1019_phase060/build_phase060_step41_process_authority.py",
            "source_commit": SOURCE_COMMIT,
            "volatile_timestamp": None,
            "ordering": "declared source/claim/chronology order; JSON keys sorted",
            "encoding": "UTF-8",
            "line_metric": "Python splitlines over frozen Git blob bytes",
        },
        "authority_policy": {
            "allowed_claim_types": [
                "USER_REQUIREMENT",
                "PROCESS_EVIDENCE",
                "SELF_ASSERTION",
                "SCIENTIFIC_CLAIM",
                "RUNTIME_CLAIM",
                "UNVERIFIED",
            ],
            "rules": [
                "Commit chronology and process checklists establish PROCESS_EVIDENCE only.",
                "Scientific/runtime completion requires independent release-source evidence and independent execution or rederivation.",
                "Asset presence or preservation assertions do not establish physical validity or citation truth.",
                "Contradictions are preserved and routed; latest-file and majority preference are forbidden.",
                "The bounded continuity scan cannot establish general physical validity.",
            ],
        },
        "source_summary": {
            "process": {"files": 11, "physical_lines": 1028, "nonblank_lines": 889},
            "release": {"files": 5, "physical_lines": 550, "nonblank_lines": 480},
            "carried_step40_witness": {"files": 1, "physical_lines": 37, "nonblank_lines": 34},
            "mandatory_full_read_files": 16,
            "mandatory_full_read_physical_lines": 1578,
        },
        "sources": source_inventory,
        "chronology": chronology,
        "claims": claims,
        "defect_correction_records": defect_correction_records,
        "contradictions": contradictions,
        "unresolved_queue": unresolved,
        "authority_decisions": [
            {"decision_id": "AUT-001", "decision": "ACCEPT_PROCESS_CHRONOLOGY", "scope": "Named stages, recorded reviewer roles, checklists, defect registers, correction records, and verified commit existence only."},
            {"decision_id": "AUT-002", "decision": "NO_SCIENTIFIC_PROMOTION", "scope": "All physical validity, derivation correctness, material claims, and citation truth remain Step 44/Phase 071 work."},
            {"decision_id": "AUT-003", "decision": "NO_RUNTIME_PROMOTION", "scope": "Code behavior, tests, stored/fresh artifacts, and continuity require Step 42 and document-to-reachable-code Step 43."},
            {"decision_id": "AUT-004", "decision": "ASSET_PRESENCE_NOT_VALIDITY", "scope": "336 and 133 are process checklist identities; their presence/preservation assertions are not independent physical or citation validation."},
            {"decision_id": "AUT-005", "decision": "PRESERVE_CONTRADICTIONS", "scope": "All six recorded authority conflicts retain both positions and explicit downstream routes."},
        ],
        "gate_summary": {
            "source_orphans": source_orphans,
            "source_orphan_count": len(source_orphans),
            "defect_correction_orphans": defect_correction_orphans,
            "defect_correction_orphan_count": len(defect_correction_orphans),
            "unresolved_obligation_orphans": unresolved_obligation_orphans,
            "unresolved_obligation_orphan_count": len(unresolved_obligation_orphans),
            "contradiction_obligation_orphans": contradiction_obligation_orphans,
            "contradiction_obligation_orphan_count": len(contradiction_obligation_orphans),
            "duplicate_claim_identity_count": len(claims) - len({claim["claim_id"] for claim in claims}),
            "unsupported_authority_promotions": unsupported_promotions,
            "unsupported_authority_promotion_count": len(unsupported_promotions),
            "contradiction_unrouted": contradiction_unrouted,
            "contradiction_unrouted_count": len(contradiction_unrouted),
            "scientific_claims_promoted": 0,
            "runtime_claims_promoted": 0,
            "next_step": 42,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    data = build()
    payload = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload, encoding="utf-8", newline="\n")
    print(f"WROTE {output.relative_to(ROOT).as_posix() if output.is_relative_to(ROOT) else output}")
    print(
        "COUNTS "
        f"sources={len(data['sources'])} process_lines={data['source_summary']['process']['physical_lines']} "
        f"release_lines={data['source_summary']['release']['physical_lines']} claims={len(data['claims'])} "
        f"defect_corrections={len(data['defect_correction_records'])} "
        f"contradictions={len(data['contradictions'])} unresolved={len(data['unresolved_queue'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
