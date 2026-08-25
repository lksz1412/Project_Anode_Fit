#!/usr/bin/env python3
"""Build deterministic Phase 060 Step 42 code/runtime/artifact evidence.

All executable inputs are materialized from frozen Git blobs in a system-temporary
fixture.  Nothing below writes to ``Claude/**`` in the working tree.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import math
import os
import platform
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageStat


ROOT = Path(__file__).resolve().parents[3]
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
DEFAULT_RUNTIME = ROOT / "Codex/results/PHASE_060_V1019_CODE_TEST_RUNTIME_MATRIX.json"
DEFAULT_ARTIFACT = ROOT / "Codex/results/PHASE_060_V1019_ARTIFACT_AUDIT.json"
RELEASE = "Claude/docs/v1.0.19"
CODE_PATHS = [
    f"{RELEASE}/Anode_Fit_v1.0.19.py",
    f"{RELEASE}/fit_roundtrip_demo.py",
    f"{RELEASE}/graph_suite_v1019.py",
    f"{RELEASE}/test_regression_v1019.py",
]
EXPECTED_CODE_LINES = {
    CODE_PATHS[0]: 1151,
    CODE_PATHS[1]: 368,
    CODE_PATHS[2]: 150,
    CODE_PATHS[3]: 127,
}
NPZ_PATH = f"{RELEASE}/golden_graphite_ref.npz"
SNAPSHOT_PATH = "Claude/docs/v1.0.20/results/snapshot_v1019_baseline.json"
SNAPSHOT_GENERATOR = "Claude/docs/v1.0.20/results/tools_check_structure.py"
PDF_PATHS = [
    f"{RELEASE}/graphite_ica_ch1_v1.0.19.pdf",
    f"{RELEASE}/graphite_ica_ch2_v1.0.19.pdf",
    f"{RELEASE}/appendix_phase_separation.pdf",
]
EXPECTED_PDF_PAGES = {
    PDF_PATHS[0]: 62,
    PDF_PATHS[1]: 25,
    PDF_PATHS[2]: 8,
}
PDF_GENERATORS = {
    PDF_PATHS[0]: f"{RELEASE}/graphite_ica_ch1_v1.0.19.tex",
    PDF_PATHS[1]: f"{RELEASE}/graphite_ica_ch2_v1.0.19.tex",
    PDF_PATHS[2]: f"{RELEASE}/appendix_phase_separation.tex",
}

# Full-read human assertion index.  These are source claims/gates, not automatic
# scientific truth.  Runtime outcomes are independently captured below.
CLAIM_GATE_SPECS: list[dict[str, Any]] = [
    {"id":"MAIN-01","path":CODE_PATHS[0],"lines":[986,995],"kind":"demo_claim","claim_type":"SELF_ASSERTION","gate":"PRINT_ONLY","summary":"seed lag, equilibrium finite, and U(298) target display"},
    {"id":"MAIN-02","path":CODE_PATHS[0],"lines":[996,1004],"kind":"demo_claim","claim_type":"RUNTIME_CLAIM","gate":"FINITE_ONLY","summary":"discharge/charge by three currents; peak and negative flags printed"},
    {"id":"MAIN-03","path":CODE_PATHS[0],"lines":[1006,1016],"kind":"demo_claim","claim_type":"RUNTIME_CLAIM","gate":"ALL_OK","summary":"three temperatures and non-isothermal profile finite"},
    {"id":"MAIN-04","path":CODE_PATHS[0],"lines":[1018,1026],"kind":"demo_claim","claim_type":"RUNTIME_CLAIM","gate":"MAX_DIFF_LT_1E_12_AND_FINITE","summary":"curve facade discharge equals direct dqdv"},
    {"id":"MAIN-05","path":CODE_PATHS[0],"lines":[1027,1030],"kind":"demo_claim","claim_type":"RUNTIME_CLAIM","gate":"FINITE_ONLY","summary":"I_abs override path finite"},
    {"id":"MAIN-06","path":CODE_PATHS[0],"lines":[1032,1045],"kind":"demo_claim","claim_type":"RUNTIME_CLAIM","gate":"PRINT_ONLY","summary":"injected chi split changes charge lag"},
    {"id":"MAIN-07","path":CODE_PATHS[0],"lines":[1047,1056],"kind":"demo_claim","claim_type":"SCIENTIFIC_CLAIM","gate":"PRINT_ONLY","summary":"hysteresis peak split tracks gamma dU_hys"},
    {"id":"MAIN-08","path":CODE_PATHS[0],"lines":[1058,1065],"kind":"demo_claim","claim_type":"SCIENTIFIC_CLAIM","gate":"PRINT_ONLY","summary":"direct-L_V direction reversal"},
    {"id":"MAIN-09","path":CODE_PATHS[0],"lines":[1067,1075],"kind":"demo_claim","claim_type":"RUNTIME_CLAIM","gate":"PRINT_ONLY","summary":"Omega=2RT and gamma-zero reduction displays"},
    {"id":"MAIN-10","path":CODE_PATHS[0],"lines":[1077,1093],"kind":"worked_example","claim_type":"RUNTIME_CLAIM","gate":"FIVE_NUMERIC_TOLERANCES","summary":"x=0.25 B.2 U_oc, entropy terms, and reversible heat"},
    {"id":"MAIN-11","path":CODE_PATHS[0],"lines":[1095,1106],"kind":"worked_example","claim_type":"RUNTIME_CLAIM","gate":"TEN_NUMERIC_TOLERANCES","summary":"five-point qrev table and sign alternation"},
    {"id":"MAIN-12","path":CODE_PATHS[0],"lines":[1108,1114],"kind":"roundtrip","claim_type":"RUNTIME_CLAIM","gate":"FD_ERROR_LT_1E_3_UV_PER_K","summary":"finite-difference versus analytic entropy coefficient"},
    {"id":"MAIN-13","path":CODE_PATHS[0],"lines":[1116,1133],"kind":"guard","claim_type":"RUNTIME_CLAIM","gate":"SEVEN_OF_SEVEN","summary":"invalid-input guards"},
    {"id":"MAIN-14","path":CODE_PATHS[0],"lines":[1135,1148],"kind":"isolation","claim_type":"RUNTIME_CLAIM","gate":"OVERRIDE_ISOLATION","summary":"per-transition override isolation"},
    {"id":"MAIN-15","path":CODE_PATHS[0],"lines":[1150,1151],"kind":"aggregate","claim_type":"SELF_ASSERTION","gate":"SUBSET_CONJUNCTION","summary":"printed overall OK covers only accumulated predicates"},
    {"id":"FIT-01","path":CODE_PATHS[1],"lines":[2,38],"kind":"roundtrip_contract","claim_type":"SELF_ASSERTION","gate":"DOCUMENTED_EXIT_0_OR_1","summary":"synthetic fitting roundtrip and figure contract"},
    {"id":"FIT-02","path":CODE_PATHS[1],"lines":[58,77],"kind":"configuration","claim_type":"PROCESS_EVIDENCE","gate":"CONSTANTS","summary":"T, SNR, seed, truth parameters, and tolerances"},
    {"id":"FIT-03","path":CODE_PATHS[1],"lines":[113,122],"kind":"synthetic_data","claim_type":"RUNTIME_CLAIM","gate":"NO_NOISE_FLOOR_GATE","summary":"Gaussian noisy data and nominal noise floor"},
    {"id":"FIT-04","path":CODE_PATHS[1],"lines":[233,255],"kind":"optimizer_schedule","claim_type":"PROCESS_EVIDENCE","gate":"INTERMEDIATE_LOSSES_PRINT_ONLY","summary":"4-to-8-to-12 staged parameter opening"},
    {"id":"FIT-05","path":CODE_PATHS[1],"lines":[275,275],"kind":"roundtrip_gate","claim_type":"RUNTIME_CLAIM","gate":"MAX_U_ERROR_LE_0_5_MV","summary":"center recovery"},
    {"id":"FIT-06","path":CODE_PATHS[1],"lines":[276,277],"kind":"roundtrip_gate","claim_type":"RUNTIME_CLAIM","gate":"MAX_N_AND_Q_REL_ERROR_LE_0_02","summary":"width and charge recovery"},
    {"id":"FIT-07","path":CODE_PATHS[1],"lines":[278,278],"kind":"roundtrip_gate","claim_type":"RUNTIME_CLAIM","gate":"FINAL_LOSS_LT_1E_4","summary":"normalized loss"},
    {"id":"FIT-08","path":CODE_PATHS[1],"lines":[279,280],"kind":"roundtrip_gate","claim_type":"SELF_ASSERTION","gate":"SUM_Q_RATIO_0_95_TO_1_05","summary":"parameter-sum ratio labelled area conservation"},
    {"id":"FIT-09","path":CODE_PATHS[1],"lines":[281,281],"kind":"roundtrip_gate","claim_type":"RUNTIME_CLAIM","gate":"STRICT_DESCENDING_CENTERS","summary":"center order"},
    {"id":"FIT-10","path":CODE_PATHS[1],"lines":[291,294],"kind":"immutability_gate","claim_type":"RUNTIME_CLAIM","gate":"DATASET_EQUALITY","summary":"imported dataset unchanged"},
    {"id":"FIT-11","path":CODE_PATHS[1],"lines":[294,296],"kind":"aggregate","claim_type":"RUNTIME_CLAIM","gate":"FIT_05_TO_10_CONJUNCTION","summary":"ROUND-TRIP PASS"},
    {"id":"FIT-12","path":CODE_PATHS[1],"lines":[299,364],"kind":"plot_claim","claim_type":"RUNTIME_CLAIM","gate":"PLOT_NOT_PART_OF_EXIT_GATE","summary":"four-panel fit figure"},
    {"id":"FIT-13","path":CODE_PATHS[1],"lines":[365,368],"kind":"fallback","claim_type":"PROCESS_EVIDENCE","gate":"PLOT_FAILURE_WARNING_ONLY","summary":"plot exception does not fail roundtrip"},
    {"id":"GRAPH-V1","path":CODE_PATHS[2],"lines":[56,61],"kind":"plot_claim","claim_type":"RUNTIME_CLAIM","gate":"FINITE_LOG_ONLY","summary":"graphite and LCO dQ/dV"},
    {"id":"GRAPH-V2","path":CODE_PATHS[2],"lines":[63,74],"kind":"roundtrip","claim_type":"RUNTIME_CLAIM","gate":"ERROR_PRINT_ONLY","summary":"entropy finite-difference parity"},
    {"id":"GRAPH-V3","path":CODE_PATHS[2],"lines":[76,81],"kind":"plot_claim","claim_type":"SCIENTIFIC_CLAIM","gate":"FINITE_LOG_ONLY","summary":"graphite reversible-heat sign regions"},
    {"id":"GRAPH-V4","path":CODE_PATHS[2],"lines":[83,100],"kind":"golden_comparison","claim_type":"RUNTIME_CLAIM","gate":"DIFF_PRINT_ONLY","summary":"complete/simple and manual return_terms comparison"},
    {"id":"GRAPH-V5","path":CODE_PATHS[2],"lines":[101,104],"kind":"plot_claim","claim_type":"RUNTIME_CLAIM","gate":"THREE_FINITE_LOGS","summary":"temperature-dependent graphite curves"},
    {"id":"GRAPH-V6","path":CODE_PATHS[2],"lines":[106,113],"kind":"plot_claim","claim_type":"SCIENTIFIC_CLAIM","gate":"FINITE_LOG_ONLY","summary":"electronic entropy trough anchors"},
    {"id":"GRAPH-V7","path":CODE_PATHS[2],"lines":[115,122],"kind":"implementation_boundary","claim_type":"UNVERIFIED","gate":"FINITE_LOG_ONLY","summary":"frozen linear LCO approximation; T-squared curvature unimplemented"},
    {"id":"GRAPH-V9","path":CODE_PATHS[2],"lines":[124,130],"kind":"plot_claim","claim_type":"RUNTIME_CLAIM","gate":"AREA_RATIO_PRINT_ONLY","summary":"finite-window equilibrium area ratio"},
    {"id":"GRAPH-V8","path":CODE_PATHS[2],"lines":[132,135],"kind":"plot_claim","claim_type":"SCIENTIFIC_CLAIM","gate":"FINITE_LOG_ONLY","summary":"LCO reversible-heat signature"},
    {"id":"GRAPH-SUITE","path":CODE_PATHS[2],"lines":[137,150],"kind":"aggregate","claim_type":"RUNTIME_CLAIM","gate":"NO_EXIT_GATE","summary":"saved figure, finite aggregate, anchor display"},
    {"id":"REG-01","path":CODE_PATHS[3],"lines":[2,18],"kind":"regression_contract","claim_type":"SELF_ASSERTION","gate":"SOURCE_CONTRACT","summary":"13-array bit-exact legacy claim"},
    {"id":"REG-02","path":CODE_PATHS[3],"lines":[80,82],"kind":"mode_gate","claim_type":"PROCESS_EVIDENCE","gate":"UNKNOWN_MODE_EXIT_2","summary":"capture or verify only"},
    {"id":"REG-03","path":CODE_PATHS[3],"lines":[85,96],"kind":"capture_guard","claim_type":"RUNTIME_CLAIM","gate":"EXISTING_GOLDEN_EXIT_3","summary":"capture refuses overwrite"},
    {"id":"REG-04","path":CODE_PATHS[3],"lines":[99,104],"kind":"golden_comparison","claim_type":"RUNTIME_CLAIM","gate":"KEY_SET_EQUALITY","summary":"golden and current key sets"},
    {"id":"REG-05","path":CODE_PATHS[3],"lines":[107,115],"kind":"golden_comparison","claim_type":"RUNTIME_CLAIM","gate":"THIRTEEN_ARRAY_EQUAL","summary":"bit-exact arrays, not allclose"},
    {"id":"REG-06","path":CODE_PATHS[3],"lines":[116,117],"kind":"area_claim","claim_type":"RUNTIME_CLAIM","gate":"PRINT_ONLY","summary":"finite-window area ratio"},
    {"id":"REG-07","path":CODE_PATHS[3],"lines":[118,120],"kind":"absence_claim","claim_type":"RUNTIME_CLAIM","gate":"PRINT_ONLY","summary":"theta_E and n_T1 absence"},
    {"id":"REG-08","path":CODE_PATHS[3],"lines":[121,123],"kind":"aggregate","claim_type":"RUNTIME_CLAIM","gate":"REG_04_AND_05_ONLY","summary":"GRAPHITE 0-DIFF PASS"},
]

FINDINGS = {
    "P0": [],
    "P1": [
        "Default transition without n or w has thermal width RT/F but _dwdT returns zero.",
        "Graph suite prints quantitative checks but has no failing aggregate exit gate.",
        "Module overall OK omits several displayed expectations.",
        "Regression PASS excludes area and theta_E/n_T1 absence checks.",
        "Fit area-conservation label gates only the fitted sum-Q ratio, not curve integration.",
        "Broad completion remains component-scoped because LCO-T restoration, total heat decomposition, and LCO tier anchors are unresolved.",
    ],
    "P2": [
        "solve_U_oc does not validate tol/max_iter or fail on iteration exhaustion.",
        "solve_U_oc validates only total Q positivity, not each transition Q.",
        "equilibrium does not validate V or callable-background output finiteness.",
        "Several low-level transition and direction inputs lack uniform finite guards.",
        "Public module helpers expose fewer guards than the class facade.",
        "Fit optimizer fallback hides import diagnostics and does not record optimizer success status.",
        "Fit plot failure is warning-only and does not affect exit status.",
        "Graph manual simple helper omits vib terms and agrees only for the current theta_E-absent dataset.",
        "Regression capture is a mutating path and must remain isolated in a disposable fixture.",
    ],
}

# Human full-read path semantics that cannot be recovered safely from syntax
# alone.  Each record is deliberately bounded to the cited source range.
PATH_SEMANTICS: list[dict[str, Any]] = [
    {"id":"SEM-001","path":CODE_PATHS[0],"lines":[296,340],"category":"default_and_unit","inputs":["transition n", "transition w", "T [K]"],"outputs":["n factor [1]", "width [V]", "dwidth/dT [V/K]"],"state":[],"defaults":["n absent and w absent -> n=1"],"errors":["nonpositive n/width -> ValueError"],"fallbacks":["w may be inverted to n"],"dormant_or_ignored":["w is ignored when n exists"],"side_effects":[]},
    {"id":"SEM-002","path":CODE_PATHS[0],"lines":[253,293],"category":"state","inputs":["transitions", "x", "Rn", "Cbg", "chi_split", "seed T/I/Q"],"outputs":["GraphiteAnodeDischargeDQDV instance", "seed_L_V [V]"],"state":["transitions stored by reference", "constructor parameters", "seed_L_V diagnostic list"],"defaults":["x=0.5", "Rn=0", "Cbg=0", "chi_split=x"],"errors":["constructor scalar/callable validation"],"fallbacks":[],"dormant_or_ignored":["seed_L_V is not consumed by production dqdv"],"side_effects":["eager diagnostic seed computation"]},
    {"id":"SEM-003","path":CODE_PATHS[0],"lines":[450,619],"category":"public_entry","inputs":["V [V]", "T [K]", "I_abs [A]", "Q_cell [Ah]", "direction", "c_rate [1/h]"],"outputs":["dQ/dV [Ah/V]"],"state":[],"defaults":["T=298.15", "I_abs=0", "Q_cell=1", "direction=discharge", "c_rate=0"],"errors":["facade direction validation", "selected scalar finite guards"],"fallbacks":["thermodynamic center falls back to U", "lag falls back to equilibrium peak"],"dormant_or_ignored":["I_abs overrides c_rate", "U ignored when dH_rxn and dS_rxn exist"],"side_effects":[]},
    {"id":"SEM-004","path":CODE_PATHS[0],"lines":[633,840],"category":"public_entry","inputs":["V_n [V] or x_bar [1]", "T [K]", "I [A]", "U_oc/V [V]"],"outputs":["dU/dT [V/K]", "reversible/irreversible heat [W]", "U_oc [V]"],"state":[],"defaults":["T=298.15", "I=1", "tol=1e-13", "max_iter=200"],"errors":["x_bar and bracket validation"],"fallbacks":["automatic U bracket"],"dormant_or_ignored":["irreversible_heat has no caller in four-file scope"],"side_effects":[]},
    {"id":"SEM-005","path":CODE_PATHS[0],"lines":[891,934],"category":"indirect_path","inputs":["transition", "T [K]"],"outputs":["effective dS_rxn [J/mol/K]"],"state":[],"defaults":["electronic entropy evaluated at T_ref=298.15 K"],"errors":[],"fallbacks":[],"dormant_or_ignored":["caller T is ignored by electronic term", "LCO default branch/tail fields absent"],"side_effects":[]},
    {"id":"SEM-006","path":CODE_PATHS[1],"lines":[48,368],"category":"side_effect_and_fallback","inputs":["ANODEFIT_CODE", "fixed synthetic truth", "seed=20250718"],"outputs":["fit gates", "samples/fig_fit_roundtrip.png"],"state":["global _eval_log mutation"],"defaults":["SciPy TRF preferred"],"errors":["exit 1 on fit-gate failure"],"fallbacks":["any SciPy import exception -> pure NumPy Nelder-Mead", "plot exception -> warning only"],"dormant_or_ignored":["fallback unexecuted when SciPy is available"],"side_effects":["optimization on import", "stdout", "directory/PNG creation", "sys.exit"]},
    {"id":"SEM-007","path":CODE_PATHS[2],"lines":[34,150],"category":"side_effect_and_gate","inputs":["ANODEFIT_CODE", "frozen datasets"],"outputs":["nine panels", "figs/graph_suite_v1019.png"],"state":["_finite_log append"],"defaults":[],"errors":["no aggregate failing exit gate"],"fallbacks":[],"dormant_or_ignored":["LCO curve facade direction flip not exercised", "manual simple omits vib terms"],"side_effects":["execution on import", "stdout", "directory/PNG creation"]},
    {"id":"SEM-008","path":CODE_PATHS[3],"lines":[79,123],"category":"golden_gate_and_side_effect","inputs":["mode capture|verify", "golden_graphite_ref.npz"],"outputs":["13-array equality status", "exit 0/1/2/3"],"state":[],"defaults":["mode=verify"],"errors":["unknown mode exit 2", "existing golden capture exit 3"],"fallbacks":[],"dormant_or_ignored":["key order not gated", "area and absence checks printed only"],"side_effects":["capture mode writes NPZ", "stdout", "sys.exit"]},
]

# Filled from the independent 95-page/13-image visual reviewer.  Machine rendering
# remains independently reproduced by this builder.
MANUAL_VISUAL_ATTESTATION: dict[str, Any] = {
    "status": "DONE_WITH_CONCERNS",
    "reviewer_scope": "3 PDFs / 95 pages and 13 unique PNG blobs",
    "pdf_pages_reviewed": 95,
    "unique_images_reviewed": 13,
    "pdf_records": [
        {"path":PDF_PATHS[0],"page_range":[1,62],"pages_reviewed":62,"visual_status":"PASS","blank_text_pages":0,"overlap":0,"clipping":0,"tofu":0,"unreadable":0,"note":"Embedded/subset fonts; visually readable."},
        {"path":PDF_PATHS[1],"page_range":[1,25],"pages_reviewed":25,"visual_status":"PASS","blank_text_pages":0,"overlap":0,"clipping":0,"tofu":0,"unreadable":0,"note":"Embedded/subset fonts; visually readable."},
        {"path":PDF_PATHS[2],"page_range":[1,8],"pages_reviewed":8,"visual_status":"CONCERN_VERSION_LABEL","blank_text_pages":0,"overlap":0,"clipping":0,"tofu":0,"unreadable":0,"note":"Page 1 visibly says v1.0.18.2 draft; its footnote explicitly describes inheritance into v1.0.19."},
    ],
    "image_records": [
        {"path":f"{RELEASE}/figs/P4_lco_heat_validation.png","visual_status":"CONCERN_CLIPPED_TITLE","note":"Panel (c) title is clipped at the right edge."},
        {"path":f"{RELEASE}/figs/anode_fit_v1_0_14_dqdv.png","visual_status":"CONCERN_VERSION_LABEL","note":"Filename says v1_0_14 while visible figure label says 1.0.16."},
        {"path":f"{RELEASE}/figs/graph_suite_v1015.png","visual_status":"PASS","note":"Readable."},
        {"path":f"{RELEASE}/figs/graph_suite_v1016.png","visual_status":"PASS","note":"Readable."},
        {"path":f"{RELEASE}/figs/graph_suite_v1019.png","visual_status":"PASS","note":"Readable."},
        {"path":f"{RELEASE}/samples/fig_Uoc_x.png","visual_status":"PASS","note":"Readable; exact renderer wrapper is GROUND_NOT_FOUND."},
        {"path":f"{RELEASE}/samples/fig_dUdT_x.png","visual_status":"PASS","note":"Readable; exact renderer wrapper is GROUND_NOT_FOUND."},
        {"path":f"{RELEASE}/samples/fig_dqdv_graphite.png","visual_status":"PASS","note":"Readable; exact renderer wrapper is GROUND_NOT_FOUND."},
        {"path":f"{RELEASE}/samples/fig_dqdv_lco.png","visual_status":"PASS","note":"Readable; exact renderer wrapper is GROUND_NOT_FOUND."},
        {"path":f"{RELEASE}/samples/fig_dqdv_temperature.png","visual_status":"PASS","note":"Readable; exact renderer wrapper is GROUND_NOT_FOUND."},
        {"path":f"{RELEASE}/samples/fig_fit_roundtrip.png","visual_status":"PASS","note":"Readable."},
        {"path":f"{RELEASE}/samples/fig_qrev_x.png","visual_status":"PASS","note":"Readable; exact renderer wrapper is GROUND_NOT_FOUND."},
        {"path":f"{RELEASE}/samples/fig_vib_einstein.png","visual_status":"PASS","note":"Readable; exact renderer wrapper is GROUND_NOT_FOUND."},
    ],
    "finding_summary": {"P0":0,"P1":0,"P2":4},
    "findings": [
        {"priority":"P2","id":"VIS-P2-01","finding":"P4 panel (c) title clips at the right edge."},
        {"priority":"P2","id":"VIS-P2-02","finding":"Stored anode filename says v1_0_14 while the visible figure says 1.0.16."},
        {"priority":"P2","id":"VIS-P2-03","finding":"Standalone appendix retains a visible v1.0.18.2 draft title, with inheritance explained only by a source footnote."},
        {"priority":"P2","id":"VIS-P2-04","finding":"Seven K-P3 sample images have reachable numerical kernels/reports but no exact renderer wrapper in the frozen corpus."},
    ],
    "toolchain": {"render_resolution_dpi":144,"inspection":"individual pages/images plus 2x2 PDF contact sheets","python":"3.12.10","git":"2.53.0.windows.2","bsdtar":"3.8.4","poppler":"24.04","pillow":"12.3.0","pypdf":"6.15","pdfplumber":"available"},
    "authority_boundary": "Human visual inspection can establish bounded rendering observations, not scientific truth.",
}


class DuplicateKeyError(ValueError):
    pass


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(key)
        out[key] = value
    return out


def strict_json_bytes(data: bytes) -> Any:
    return json.loads(
        data.decode("utf-8"),
        object_pairs_hook=reject_pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"nonfinite {value}")),
    )


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str, binary: bool = False) -> bytes | str:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, encoding=None if binary else "utf-8",
    )
    return proc.stdout


def path_blob(path: str) -> str:
    return str(git("rev-parse", f"{SOURCE_COMMIT}:{path}")).strip()


def blob_bytes(path: str) -> bytes:
    return bytes(git("cat-file", "blob", path_blob(path), binary=True))


def source_record(path: str) -> dict[str, Any]:
    data = blob_bytes(path)
    return {
        "path": path,
        "git_blob_sha1": path_blob(path),
        "raw_git_blob_sha256": sha256(data),
        "size_bytes": len(data),
        "physical_lines": len(data.decode("utf-8-sig").splitlines()),
        "working_tree_encoding_boundary": "Raw Git blob bytes are canonical; checkout CRLF bytes are not used as source identity.",
        "read_coverage": [1, len(data.decode("utf-8-sig").splitlines())],
    }


def dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{dotted(node.value)}.{node.attr}"
    if isinstance(node, ast.Call):
        return f"{dotted(node.func)}()"
    if isinstance(node, ast.Subscript):
        return f"{dotted(node.value)}[]"
    return type(node).__name__


class DirectCallVisitor(ast.NodeVisitor):
    def __init__(self, root: ast.AST) -> None:
        self.root = root
        self.calls: list[dict[str, Any]] = []

    def visit_Call(self, node: ast.Call) -> None:
        self.calls.append({"line": node.lineno, "callee": dotted(node.func)})
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node is self.root:
            self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if node is self.root:
            self.generic_visit(node)


def unparse(node: ast.AST | None) -> str | None:
    return ast.unparse(node) if node is not None else None


def assignment_targets(node: ast.AST) -> list[str]:
    if isinstance(node, (ast.Tuple, ast.List)):
        values: list[str] = []
        for item in node.elts:
            values.extend(assignment_targets(item))
        return values
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, ast.Attribute):
        return [dotted(node)]
    if isinstance(node, ast.Subscript):
        return [dotted(node)]
    return [unparse(node) or type(node).__name__]


def signature_contract(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    positional = [*node.args.posonlyargs, *node.args.args]
    defaults: list[ast.AST | None] = [None] * (len(positional) - len(node.args.defaults)) + list(node.args.defaults)
    parameters = [
        {
            "name": arg.arg,
            "kind": "POSITIONAL_ONLY" if index < len(node.args.posonlyargs) else "POSITIONAL_OR_KEYWORD",
            "annotation": unparse(arg.annotation),
            "default": unparse(default),
        }
        for index, (arg, default) in enumerate(zip(positional, defaults))
    ]
    if node.args.vararg:
        parameters.append({"name":node.args.vararg.arg,"kind":"VAR_POSITIONAL","annotation":unparse(node.args.vararg.annotation),"default":None})
    for arg, default in zip(node.args.kwonlyargs, node.args.kw_defaults):
        parameters.append({"name":arg.arg,"kind":"KEYWORD_ONLY","annotation":unparse(arg.annotation),"default":unparse(default)})
    if node.args.kwarg:
        parameters.append({"name":node.args.kwarg.arg,"kind":"VAR_KEYWORD","annotation":unparse(node.args.kwarg.annotation),"default":None})
    return {"parameters":parameters,"return_annotation":unparse(node.returns)}


class DirectBehaviorVisitor(ast.NodeVisitor):
    SIDE_EFFECT_NAMES = {
        "print", "sys.exit", "np.savez", "plt.savefig", "fig.savefig",
        "mkdir", "write_text", "write_bytes", "open", "append",
    }

    def __init__(self, root: ast.AST) -> None:
        self.root = root
        self.state_writes: list[dict[str, Any]] = []
        self.raises: list[dict[str, Any]] = []
        self.exception_handlers: list[dict[str, Any]] = []
        self.return_lines: list[int] = []
        self.branch_tests: list[dict[str, Any]] = []
        self.side_effect_calls: list[dict[str, Any]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node is self.root:
            self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if node is self.root:
            self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if node is self.root:
            self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            for name in assignment_targets(target):
                if name.startswith(("self.", "cls.")):
                    self.state_writes.append({"line":node.lineno,"target":name,"value":unparse(node.value)})
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        for name in assignment_targets(node.target):
            if name.startswith(("self.", "cls.")):
                self.state_writes.append({"line":node.lineno,"target":name,"value":unparse(node.value)})
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        for name in assignment_targets(node.target):
            if name.startswith(("self.", "cls.")):
                self.state_writes.append({"line":node.lineno,"target":name,"value":unparse(node.value)})
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise) -> None:
        self.raises.append({"line":node.lineno,"exception":unparse(node.exc),"cause":unparse(node.cause)})
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        for handler in node.handlers:
            self.exception_handlers.append({"line":handler.lineno,"type":unparse(handler.type) or "ANY","name":handler.name})
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        self.return_lines.append(node.lineno)
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self.branch_tests.append({"line":node.lineno,"test":unparse(node.test),"has_else":bool(node.orelse)})
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        name = dotted(node.func)
        leaf = name.rsplit(".", 1)[-1]
        if name in self.SIDE_EFFECT_NAMES or leaf in self.SIDE_EFFECT_NAMES or leaf in {"savefig", "mkdir", "write_text", "write_bytes", "append"}:
            self.side_effect_calls.append({"line":node.lineno,"callee":name})
        self.generic_visit(node)


def definition_record(node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef, qname: str) -> dict[str, Any]:
    record: dict[str, Any] = {
        "kind": "class" if isinstance(node, ast.ClassDef) else "function",
        "qualified_name": qname,
        "start_line": node.lineno,
        "end_line": node.end_lineno,
        "public_entry": not any(part.startswith("_") for part in qname.replace(".<local>.", ".").split(".")),
        "docstring": ast.get_docstring(node, clean=False),
    }
    if isinstance(node, ast.ClassDef):
        record.update({"bases":[unparse(base) for base in node.bases],"signature":{"parameters":[],"return_annotation":None},"state_writes":[],"explicit_raises":[],"exception_handlers":[],"return_lines":[],"branch_tests":[],"side_effect_calls":[]})
        return record
    behavior = DirectBehaviorVisitor(node)
    behavior.visit(node)
    record.update({
        "signature": signature_contract(node),
        "state_writes": behavior.state_writes,
        "explicit_raises": behavior.raises,
        "exception_handlers": behavior.exception_handlers,
        "return_lines": behavior.return_lines,
        "branch_tests": behavior.branch_tests,
        "side_effect_calls": behavior.side_effect_calls,
    })
    return record


def module_state_records(tree: ast.Module) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                for name in assignment_targets(target):
                    records.append({"scope":"module","line":node.lineno,"target":name,"value":unparse(node.value)})
        elif isinstance(node, ast.AnnAssign):
            for name in assignment_targets(node.target):
                records.append({"scope":"module","line":node.lineno,"target":name,"value":unparse(node.value)})
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        for name in assignment_targets(target):
                            records.append({"scope":node.name,"line":child.lineno,"target":name,"value":unparse(child.value)})
                elif isinstance(child, ast.AnnAssign):
                    for name in assignment_targets(child.target):
                        records.append({"scope":node.name,"line":child.lineno,"target":name,"value":unparse(child.value)})
    return records


class ImportContractVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.optional_depth = 0
        self.records: list[dict[str, Any]] = []

    def visit_Try(self, node: ast.Try) -> None:
        self.optional_depth += 1
        for child in [*node.body, *node.handlers, *node.orelse, *node.finalbody]:
            self.visit(child)
        self.optional_depth -= 1

    def visit_Import(self, node: ast.Import) -> None:
        self.records.extend({"line":node.lineno,"module":alias.name,"optional":self.optional_depth > 0} for alias in node.names)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.records.append({"line":node.lineno,"module":node.module or "","optional":self.optional_depth > 0})


def code_index(path: str) -> dict[str, Any]:
    data = blob_bytes(path)
    text = data.decode("utf-8-sig")
    tree = ast.parse(text, filename=path)
    definitions: list[dict[str, Any]] = []
    call_edges: list[dict[str, Any]] = []

    def walk(body: list[ast.stmt], prefix: str = "") -> None:
        for node in body:
            if isinstance(node, ast.ClassDef):
                qname = f"{prefix}{node.name}"
                definitions.append(definition_record(node, qname))
                walk(node.body, f"{qname}.")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qname = f"{prefix}{node.name}"
                definitions.append(definition_record(node, qname))
                visitor = DirectCallVisitor(node)
                visitor.visit(node)
                for call in visitor.calls:
                    call_edges.append({"caller": qname, **call})
                walk([child for child in node.body if isinstance(child, (ast.FunctionDef, ast.ClassDef))], f"{qname}.<local>.")

    walk(tree.body)
    import_visitor = ImportContractVisitor()
    import_visitor.visit(tree)
    imports = import_visitor.records
    return {
        **source_record(path),
        "syntax_parse": "PASS",
        "imports": sorted(imports, key=lambda x: (x["line"], x["module"])),
        "definitions": definitions,
        "call_edges": call_edges,
        "assert_nodes": [{"line":n.lineno} for n in ast.walk(tree) if isinstance(n, ast.Assert)],
        "module_and_class_state": module_state_records(tree),
        "path_semantics": [record for record in PATH_SEMANTICS if record["path"] == path],
    }


def canonical_output(data: bytes, fixture: Path) -> bytes:
    variants = {str(fixture), str(fixture).replace("\\", "/")}
    text = data.decode("utf-8", errors="replace")
    for value in variants:
        text = text.replace(value, "<FIXTURE>")
    return text.replace("\r\n", "\n").encode("utf-8")


def required_match(pattern: str, text: str, label: str) -> re.Match[str]:
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        raise RuntimeError(f"runtime semantic pattern missing: {label}: {pattern}")
    return match


def parse_runtime_semantics(script: str, args: list[str], stdout: bytes) -> dict[str, Any]:
    text = stdout.decode("utf-8")
    if script == "test_regression_v1019.py" and not args:
        gate = required_match(r"GRAPHITE 0-DIFF \(v1\.0\.19 vs golden\): (\d+)/(\d+) (PASS|FAIL)", text, "regression gate")
        area = required_match(r"AREA check: trapz\(eq\)=([0-9.]+)\s+Qsum=([0-9.]+)\s+ratio=([0-9.]+)", text, "regression area")
        absence = required_match(r"theta_E absent in GRAPHITE_STAGING_LIT: (True|False)\s+n_T1 absent: (True|False)", text, "regression absence")
        return {"array_equal_passed":int(gate.group(1)),"array_total":int(gate.group(2)),"printed_gate":gate.group(3),"finite_window_area":float(area.group(1)),"q_sum":float(area.group(2)),"ratio":float(area.group(3)),"theta_E_absent":absence.group(1)=="True","n_T1_absent":absence.group(2)=="True","gate_scope":"array equality only"}
    if script == "test_regression_v1019.py" and args == ["capture"]:
        captured = required_match(r"GOLDEN CAPTURED: (\d+) arrays", text, "fresh capture") if "GOLDEN CAPTURED:" in text else None
        return {
            "overwrite_refused":"REFUSE: golden already exists" in text,
            "fresh_capture_array_count":int(captured.group(1)) if captured else None,
            "gate_scope":"fresh capture" if captured else "existing-golden refusal only",
        }
    if script == "fit_roundtrip_demo.py":
        loss = required_match(r"final L = ([0-9.eE+-]+) < gate", text, "fit loss")
        uerr = required_match(r"max\|U err\| = ([0-9.]+) mV", text, "fit U error")
        nerr = required_match(r"max\|n err\| = ([0-9.]+)%", text, "fit n error")
        qerr = required_match(r"max\|Q err\| = ([0-9.]+)%", text, "fit Q error")
        gate = required_match(r">>> ROUND-TRIP: (PASS|FAIL)", text, "fit aggregate")
        return {"final_loss":float(loss.group(1)),"max_U_error_mV":float(uerr.group(1)),"max_n_error_percent":float(nerr.group(1)),"max_Q_error_percent":float(qerr.group(1)),"printed_gate":gate.group(1),"all_source_gates":gate.group(1)=="PASS","experimental_validation":False}
    if script == "graph_suite_v1019.py":
        v2 = required_match(r"V2 round-trip max\|err\| = ([0-9.eE+-]+)", text, "graph V2")
        v4 = required_match(r"V4 return_terms .* = ([0-9.eE+-]+) mV/K", text, "graph V4")
        v9 = required_match(r"V9 면적보존 ratio = ([0-9.]+)", text, "graph V9")
        finite = required_match(r"ALL PANELS FINITE: (True|False)", text, "graph finite")
        return {"V2_error":float(v2.group(1)),"V4_error_mV_per_K":float(v4.group(1)),"V9_ratio":float(v9.group(1)),"all_logged_panels_finite":finite.group(1)=="True","aggregate_exit_gate":False}
    if script == "Anode_Fit_v1.0.19.py":
        uoc = required_match(r"x=0\.25: U_oc=([0-9.]+) mV", text, "module Uoc")
        terms = required_match(r"complete=([+-]?[0-9.]+) simple=([+-]?[0-9.]+) config=([+-]?[0-9.]+) mV/K", text, "module terms")
        qrev = required_match(r"Qrev/I=([+-]?[0-9.]+) mV", text, "module qrev")
        fd = required_match(r"round-trip \|FD - analytic\| = ([0-9.]+) uV/K", text, "module FD")
        guards = required_match(r"guards fired: (\d+)/(\d+)", text, "module guards")
        overall = required_match(r">>> overall OK: (True|False)", text, "module overall")
        return {"U_oc_x025_mV":float(uoc.group(1)),"complete_mV_per_K":float(terms.group(1)),"simple_mV_per_K":float(terms.group(2)),"config_mV_per_K":float(terms.group(3)),"qrev_per_I_mV":float(qrev.group(1)),"fd_error_uV_per_K":float(fd.group(1)),"guards_passed":int(guards.group(1)),"guards_total":int(guards.group(2)),"printed_overall_ok":overall.group(1)=="True","gate_scope":"subset described by MAIN-15"}
    raise RuntimeError(f"unknown runtime semantic parser: {script} {args!r}")


def run_command(fixture: Path, script: str, args: list[str], expected_exit: int,
                output_rel: str | None) -> dict[str, Any]:
    cwd = fixture / RELEASE
    env = os.environ.copy()
    env.update({
        "PYTHONIOENCODING": "utf-8",
        "PYTHONHASHSEED": "0",
        "SOURCE_DATE_EPOCH": "0",
        "MPLCONFIGDIR": str(fixture / "mplconfig"),
        "ANODEFIT_CODE": str(cwd / "Anode_Fit_v1.0.19.py"),
    })
    proc = subprocess.run(
        [sys.executable, script, *args], cwd=cwd, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=240,
    )
    stdout = canonical_output(proc.stdout, fixture)
    stderr = canonical_output(proc.stderr, fixture)
    output: dict[str, Any] | None = None
    if output_rel:
        path = cwd / output_rel
        output = {
            "path": output_rel.replace("\\", "/"),
            "exists": path.is_file(),
            "size_bytes": path.stat().st_size if path.is_file() else None,
            "sha256": sha256(path.read_bytes()) if path.is_file() else None,
        }
    return {
        "command": ["python", script, *args],
        "cwd": f"<SYSTEM_TEMP>/fixture/{RELEASE}",
        "environment": {"PYTHONIOENCODING":"utf-8","PYTHONHASHSEED":"0","SOURCE_DATE_EPOCH":"0","MPLCONFIGDIR":"<FIXTURE>/mplconfig","ANODEFIT_CODE":"<FIXTURE>/Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py"},
        "exit_code": proc.returncode,
        "expected_exit_code": expected_exit,
        "exit_matches_contract": proc.returncode == expected_exit,
        "stdout_sha256": sha256(stdout),
        "stderr_sha256": sha256(stderr),
        "stdout_size_bytes": len(stdout),
        "stderr_size_bytes": len(stderr),
        "path_normalization": "system fixture root replaced by <FIXTURE>; CRLF normalized to LF before stream hashing",
        "semantic_observations": parse_runtime_semantics(script, args, stdout),
        "generated_output": output,
    }


def materialize_fixture(base: Path, *, include_npz: bool = True) -> Path:
    fixture = base / "fixture"
    paths = [*CODE_PATHS, *([NPZ_PATH] if include_npz else [])]
    for path in paths:
        target = fixture / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob_bytes(path))
    return fixture


def runtime_pass() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="phase060_step42_runtime_") as td:
        fixture = materialize_fixture(Path(td))
        claude_before = str(git("status", "--porcelain", "--", "Claude"))
        before_inputs: dict[str, dict[str, Any]] = {}
        for path in [*CODE_PATHS, NPZ_PATH]:
            target = fixture / path
            stat = target.stat()
            before_inputs[path] = {
                "sha256": sha256(target.read_bytes()),
                "size_bytes": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
                "mode": stat.st_mode,
            }
        cases = [
            ("regression_verify", "test_regression_v1019.py", [], 0, None),
            ("regression_capture_guard", "test_regression_v1019.py", ["capture"], 3, None),
            ("fit_roundtrip", "fit_roundtrip_demo.py", [], 0, "samples/fig_fit_roundtrip.png"),
            ("graph_suite", "graph_suite_v1019.py", [], 0, "figs/graph_suite_v1019.png"),
            ("module_demo", "Anode_Fit_v1.0.19.py", [], 0, None),
        ]
        records = []
        for case_id, script, args, expected, output in cases:
            records.append({"case_id":case_id, **run_command(fixture, script, args, expected, output)})
        immutable = []
        for path in [*CODE_PATHS, NPZ_PATH]:
            target = fixture / path
            data = target.read_bytes()
            stat = target.stat()
            before = before_inputs[path]
            immutable.append({
                "path": path,
                "before_sha256": before["sha256"],
                "after_sha256": sha256(data),
                "before_size_bytes": before["size_bytes"],
                "after_size_bytes": stat.st_size,
                "content_unchanged": before["sha256"] == sha256(data),
                "size_unchanged": before["size_bytes"] == stat.st_size,
                "mtime_ns_unchanged": before["mtime_ns"] == stat.st_mtime_ns,
                "mode_unchanged": before["mode"] == stat.st_mode,
                "matches_frozen_blob": data == blob_bytes(path),
            })
        claude_after = str(git("status", "--porcelain", "--", "Claude"))
        return {
            "cases": records,
            "fixture_source_immutability": immutable,
            "working_tree_claude_status_before": claude_before.splitlines(),
            "working_tree_claude_status_after": claude_after.splitlines(),
            "cleanup_contract": "TemporaryDirectory cleanup on scope exit; no fixture path is serialized.",
        }


def npz_audit() -> dict[str, Any]:
    data = blob_bytes(NPZ_PATH)
    with tempfile.TemporaryDirectory(prefix="phase060_step42_npz_") as td:
        path = Path(td) / "golden.npz"
        path.write_bytes(data)
        arrays = []
        with np.load(path, allow_pickle=False) as archive:
            keys = list(archive.files)
            for order, key in enumerate(keys):
                arr = np.asarray(archive[key])
                finite = np.isfinite(arr)
                arrays.append({
                    "order": order,
                    "key": key,
                    "shape": list(arr.shape),
                    "dtype": arr.dtype.str,
                    "size": int(arr.size),
                    "finite_count": int(finite.sum()),
                    "nan_count": int(np.isnan(arr).sum()),
                    "posinf_count": int(np.isposinf(arr).sum()),
                    "neginf_count": int(np.isneginf(arr).sum()),
                    "minimum": float(np.min(arr)),
                    "maximum": float(np.max(arr)),
                    "range": float(np.max(arr) - np.min(arr)),
                    "raw_array_sha256": sha256(arr.tobytes()),
                })
    fresh_passes = [fresh_npz_capture_pass(), fresh_npz_capture_pass()]
    return {
        "path": NPZ_PATH,
        "git_blob_sha1": path_blob(NPZ_PATH),
        "sha256": sha256(data),
        "size_bytes": len(data),
        "allow_pickle": False,
        "load_status": "PASS",
        "array_count": len(arrays),
        "arrays": arrays,
        "zip_members": npz_member_records(data),
        "fresh_capture": {
            "pass_count": 2,
            "passes": fresh_passes,
            "byte_identical_records": fresh_passes[0] == fresh_passes[1],
            "stored_archive_byte_identical": all(record["archive_sha256"] == sha256(data) and record["archive_size_bytes"] == len(data) for record in fresh_passes),
            "stored_member_order_and_bytes_identical": all(record["zip_members"] == npz_member_records(data) for record in fresh_passes),
        },
    }


def npz_member_records(data: bytes) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
        for order, info in enumerate(archive.infolist()):
            member = archive.read(info.filename)
            records.append({
                "order": order,
                "filename": info.filename,
                "date_time": list(info.date_time),
                "compress_type": info.compress_type,
                "crc32": f"{info.CRC:08x}",
                "file_size": info.file_size,
                "compress_size": info.compress_size,
                "member_sha256": sha256(member),
            })
    return records


def fresh_npz_capture_pass() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="phase060_step42_npz_capture_") as td:
        fixture = materialize_fixture(Path(td), include_npz=False)
        record = run_command(
            fixture,
            "test_regression_v1019.py",
            ["capture"],
            0,
            "golden_graphite_ref.npz",
        )
        captured = (fixture / NPZ_PATH).read_bytes()
        source_unchanged = all((fixture / path).read_bytes() == blob_bytes(path) for path in CODE_PATHS)
        return {
            "runtime": record,
            "archive_sha256": sha256(captured),
            "archive_size_bytes": len(captured),
            "zip_members": npz_member_records(captured),
            "source_code_unchanged": source_unchanged,
            "cleanup_contract": "TemporaryDirectory cleanup on scope exit.",
        }


def count_nodes(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + sum(count_nodes(k) + count_nodes(v) for k, v in value.items())
    if isinstance(value, list):
        return 1 + sum(count_nodes(v) for v in value)
    return 1


def snapshot_regeneration_pass(stored_value: Any, stored_bytes: bytes) -> dict[str, Any]:
    tex_paths = sorted(
        path
        for path in str(git("ls-tree", "-r", "--name-only", SOURCE_COMMIT, "--", RELEASE)).splitlines()
        if path.endswith(".tex")
    )
    if len(tex_paths) != 42:
        raise RuntimeError(f"snapshot regeneration expected 42 TeX files, got {len(tex_paths)}")
    with tempfile.TemporaryDirectory(prefix="phase060_step42_snapshot_") as td:
        base = Path(td)
        for path in [*tex_paths, SNAPSHOT_GENERATOR]:
            target = base / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob_bytes(path))
        generator = base / SNAPSHOT_GENERATOR
        release_root = base / RELEASE
        output = base / "fresh_snapshot.json"
        command = [
            sys.executable,
            str(generator),
            "snapshot",
            str(release_root),
            str(output),
            "graphite_ica_ch1_v1.0.19.tex",
            "graphite_ica_ch2_v1.0.19.tex",
        ]
        proc = subprocess.run(command, cwd=generator.parent, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        fresh_bytes = output.read_bytes() if output.is_file() else b""
        fresh_value = strict_json_bytes(fresh_bytes) if fresh_bytes else None
        normalized = fresh_bytes.replace(b"\r\n", b"\n")
        source_unchanged = all((base / path).read_bytes() == blob_bytes(path) for path in [*tex_paths, SNAPSHOT_GENERATOR])
        return {
            "command": ["python", "tools_check_structure.py", "snapshot", "<V1019_ROOT>", "<TEMP_OUTPUT>", "graphite_ica_ch1_v1.0.19.tex", "graphite_ica_ch2_v1.0.19.tex"],
            "cwd": "<SYSTEM_TEMP>/Claude/docs/v1.0.20/results",
            "exit_code": proc.returncode,
            "stdout_sha256": sha256(canonical_output(proc.stdout, base)),
            "stderr_sha256": sha256(canonical_output(proc.stderr, base)),
            "output_size_bytes": len(fresh_bytes),
            "output_sha256": sha256(fresh_bytes),
            "normalized_lf_sha256": sha256(normalized),
            "strict_json": "PASS" if fresh_value is not None else "FAIL",
            "object_equal_to_stored": fresh_value == stored_value,
            "normalized_byte_equal_to_raw_stored": normalized == stored_bytes,
            "tex_files": len(tex_paths),
            "source_inputs_unchanged": source_unchanged,
            "cleanup_contract": "TemporaryDirectory cleanup on scope exit.",
        }


def snapshot_audit() -> dict[str, Any]:
    data = blob_bytes(SNAPSHOT_PATH)
    value = strict_json_bytes(data)
    roots = []
    for root_name in sorted(value):
        record = value[root_name]
        roots.append({
            "v1019_root": root_name,
            "labels": len(record["labels"]),
            "equation_blocks": len(record["eqblocks"]),
            "boxed_equation_blocks": sum(1 for item in record["eqblocks"].values() if item["boxed"]),
            "asset_unique": record["asset_unique"],
            "bibitems": len(record["bibitems"]),
        })
    regeneration = [snapshot_regeneration_pass(value, data), snapshot_regeneration_pass(value, data)]
    return {
        **source_record(SNAPSHOT_PATH),
        "strict_json": "PASS",
        "recursive_node_count": count_nodes(value),
        "top_level_roots": roots,
        "generator": {**source_record(SNAPSHOT_GENERATOR), "role":"frozen v1.0.19 structural snapshot generator"},
        "regeneration": {
            "pass_count": 2,
            "passes": regeneration,
            "byte_identical_records": regeneration[0] == regeneration[1],
            "object_equal_to_stored": all(record["object_equal_to_stored"] for record in regeneration),
            "normalized_byte_equal_to_raw_stored": all(record["normalized_byte_equal_to_raw_stored"] for record in regeneration),
            "comparison_scope": "42 frozen v1.0.19 TeX files through both v1.0.19 chapter roots",
        },
        "authority_boundary": "Only explicit v1.0.19 structural claims are recorded; Phase 061 content and scientific truth are not adjudicated.",
    }


def dependency_versions() -> dict[str, str]:
    import matplotlib
    import PIL
    try:
        import scipy
        scipy_version = scipy.__version__
    except Exception as exc:  # recorded environment fact, not runtime fallback execution
        scipy_version = f"UNAVAILABLE:{type(exc).__name__}"
    git_version = str(git("--version")).strip()
    return {
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy_version,
        "matplotlib": matplotlib.__version__,
        "pillow": PIL.__version__,
        "git": git_version,
    }


def image_paths() -> list[str]:
    names = str(git("ls-tree", "-r", "--name-only", SOURCE_COMMIT, "--", RELEASE)).splitlines()
    return sorted(path for path in names if path.lower().endswith(".png"))


def image_record(path: str) -> dict[str, Any]:
    data = blob_bytes(path)
    with Image.open(io.BytesIO(data)) as image:
        image.load()
        stat = ImageStat.Stat(image.convert("RGB"))
        return {
            "path": path,
            "git_blob_sha1": path_blob(path),
            "sha256": sha256(data),
            "size_bytes": len(data),
            "format": image.format,
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "frames": getattr(image, "n_frames", 1),
            "rgb_mean": [round(value, 9) for value in stat.mean],
            "rgb_extrema": [list(pair) for pair in stat.extrema],
        }


def render_pdf(path: str, base: Path) -> dict[str, Any]:
    data = blob_bytes(path)
    pdf = base / Path(path).name
    pdf.write_bytes(data)
    info = subprocess.run(["pdfinfo", str(pdf)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info_text = info.stdout.decode("utf-8", errors="replace")
    match = re.search(r"^Pages:\s+(\d+)\s*$", info_text, re.MULTILINE)
    if not match:
        raise RuntimeError(f"pdfinfo page count missing: {path}")
    pages = int(match.group(1))
    prefix = base / (pdf.stem + "_page")
    render = subprocess.run(
        ["pdftoppm", "-r", "144", "-png", str(pdf), str(prefix)],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=240,
    )
    rendered = sorted(base.glob(prefix.name + "-*.png"), key=lambda p: int(p.stem.rsplit("-", 1)[1]))
    page_records = []
    for page_number, image_path in enumerate(rendered, 1):
        image_data = image_path.read_bytes()
        with Image.open(io.BytesIO(image_data)) as image:
            image.load()
            stat = ImageStat.Stat(image.convert("L"))
            page_records.append({
                "page": page_number,
                "sha256": sha256(image_data),
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "mean_gray": round(stat.mean[0], 9),
                "extrema": list(stat.extrema[0]),
            })
    return {
        "path": path,
        "git_blob_sha1": path_blob(path),
        "sha256": sha256(data),
        "size_bytes": len(data),
        "page_count": pages,
        "expected_page_count": EXPECTED_PDF_PAGES[path],
        "render_tool": "pdftoppm -r 144 -png",
        "render_exit_code": render.returncode,
        "render_stdout_sha256": sha256(render.stdout),
        "render_stderr_sha256": sha256(render.stderr),
        "rendered_page_count": len(page_records),
        "pages": page_records,
        "generator": {"status":"DIRECT_TEX_SOURCE","path":PDF_GENERATORS[path],"git_blob_sha1":path_blob(PDF_GENERATORS[path])},
    }


def provenance(path: str) -> dict[str, Any]:
    direct = {
        f"{RELEASE}/figs/P4_lco_heat_validation.png": "Claude/docs/v1.0.18.2/demo_lco_heat.py",
        f"{RELEASE}/figs/anode_fit_v1_0_14_dqdv.png": "Claude/docs/v1.0.16/plot_dqdv.py",
        f"{RELEASE}/figs/graph_suite_v1015.png": "Claude/docs/v1.0.15/graph_suite_v1015.py",
        f"{RELEASE}/figs/graph_suite_v1016.png": "Claude/docs/v1.0.16/graph_suite_v1016.py",
        f"{RELEASE}/figs/graph_suite_v1019.png": f"{RELEASE}/graph_suite_v1019.py",
        f"{RELEASE}/samples/fig_fit_roundtrip.png": f"{RELEASE}/fit_roundtrip_demo.py",
    }
    if path in direct:
        return {"status":"DIRECT_GENERATOR","path":direct[path],"git_blob_sha1":path_blob(direct[path])}
    return {"status":"GROUND_NOT_FOUND","path":None,"reason":"No frozen v1.0.19 generator is reachable from the audited release source."}


def pixel_diff(left_path: str, right_path: str) -> dict[str, Any]:
    left_bytes = blob_bytes(left_path)
    right_bytes = blob_bytes(right_path)
    with Image.open(io.BytesIO(left_bytes)) as left_image, Image.open(io.BytesIO(right_bytes)) as right_image:
        left = np.asarray(left_image.convert("RGBA"))
        right = np.asarray(right_image.convert("RGBA"))
    if left.shape != right.shape:
        differing_pixels = None
        bbox = None
        dimensions_equal = False
    else:
        mask = np.any(left != right, axis=2)
        differing_pixels = int(mask.sum())
        if differing_pixels:
            ys, xs = np.where(mask)
            bbox = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
        else:
            bbox = None
        dimensions_equal = True
    return {
        "left_path": left_path,
        "right_path": right_path,
        "left_git_blob_sha1": path_blob(left_path),
        "right_git_blob_sha1": path_blob(right_path),
        "left_sha256": sha256(left_bytes),
        "right_sha256": sha256(right_bytes),
        "byte_identical": left_bytes == right_bytes,
        "dimensions_equal": dimensions_equal,
        "differing_pixels": differing_pixels,
        "difference_bbox_left_top_right_bottom_exclusive": bbox,
        "authority_boundary": "Pixel identity/difference is visual lineage evidence only.",
    }


def build_artifact_audit(runtime: dict[str, Any]) -> dict[str, Any]:
    images = [image_record(path) for path in image_paths()]
    by_path = {item["path"]: item for item in images}
    fresh = {}
    for case in runtime["runtime"]["passes"][0]["cases"]:
        output = case["generated_output"]
        if output and output["exists"]:
            stored_path = (
                f"{RELEASE}/samples/fig_fit_roundtrip.png"
                if case["case_id"] == "fit_roundtrip"
                else f"{RELEASE}/figs/graph_suite_v1019.png"
            )
            fresh[case["case_id"]] = {
                "stored_path": stored_path,
                "fresh_sha256": output["sha256"],
                "stored_sha256": by_path[stored_path]["sha256"],
                "byte_identical": output["sha256"] == by_path[stored_path]["sha256"] and output["size_bytes"] == by_path[stored_path]["size_bytes"],
            }
    with tempfile.TemporaryDirectory(prefix="phase060_step42_pdf_") as td:
        pdfs = [render_pdf(path, Path(td)) for path in PDF_PATHS]
    witness_path = "Claude/docs/v1.0.20/figs/graph_suite_v1019.png"
    witness = image_record(witness_path)
    stored_graph = by_path[f"{RELEASE}/figs/graph_suite_v1019.png"]
    cross_version_comparisons = [
        pixel_diff(f"{RELEASE}/figs/graph_suite_v1015.png", f"{RELEASE}/figs/graph_suite_v1016.png"),
        pixel_diff(f"{RELEASE}/figs/graph_suite_v1016.png", f"{RELEASE}/figs/graph_suite_v1019.png"),
        pixel_diff(f"{RELEASE}/figs/graph_suite_v1019.png", witness_path),
    ]
    return {
        "schema_version": 1,
        "phase": 60,
        "step": 42,
        "source_commit": SOURCE_COMMIT,
        "authority_policy": {
            "runtime_truth": "Bounded execution results only.",
            "scientific_truth": "NOT_PROMOTED",
            "experimental_validation": "NOT_CLAIMED",
            "stored_visual_agreement": "Does not establish physical validity.",
        },
        "pdf_summary": {"files":len(pdfs),"pages":sum(item["page_count"] for item in pdfs),"rendered_pages":sum(item["rendered_page_count"] for item in pdfs)},
        "pdfs": pdfs,
        "image_summary": {"occurrences":len(images),"unique_blobs":len({item["git_blob_sha1"] for item in images})},
        "images": [{**item,"provenance":provenance(item["path"])} for item in images],
        "fresh_to_stored_comparisons": fresh,
        "cross_version_comparisons": cross_version_comparisons,
        "cross_version_witness": {
            "path": witness_path,
            "git_blob_sha1": witness["git_blob_sha1"],
            "sha256": witness["sha256"],
            "duplicates_v1019_path": stored_graph["path"],
            "byte_identical": witness["git_blob_sha1"] == stored_graph["git_blob_sha1"],
            "review_authority_counted_again": False,
        },
        "manual_visual_attestation": MANUAL_VISUAL_ATTESTATION,
    }


def semantic_runtime_summary(pass_record: dict[str, Any]) -> dict[str, Any]:
    by_id = {case["case_id"]:case["semantic_observations"] for case in pass_record["cases"]}
    return {"regression":by_id["regression_verify"],"capture_guard":by_id["regression_capture_guard"],"fit_roundtrip":by_id["fit_roundtrip"],"graph_suite":by_id["graph_suite"],"module_demo":by_id["module_demo"]}


def build_runtime_matrix() -> dict[str, Any]:
    code = [code_index(path) for path in CODE_PATHS]
    if sum(item["physical_lines"] for item in code) != 1796:
        raise RuntimeError("code coverage total mismatch")
    for item in code:
        if item["physical_lines"] != EXPECTED_CODE_LINES[item["path"]]:
            raise RuntimeError(f"line mismatch {item['path']}")
    first = runtime_pass()
    second = runtime_pass()
    reproducible = first == second
    return {
        "schema_version": 1,
        "phase": 60,
        "step": 42,
        "source_commit": SOURCE_COMMIT,
        "generation": {"builder":"Codex/work/v1019_phase060/audit_phase060_step42_runtime_artifacts.py","ordering":"sorted paths and source order","json":"UTF-8, indent=2, allow_nan=False","temporary_fixture":"system temp from frozen Git blobs","determinism_scope":"Byte-identical rebuild is required only under the recorded Python/dependency/Poppler platform; cross-toolchain byte portability is not claimed."},
        "authority_policy": {
            "runtime_truth": "Fresh bounded execution can promote only the exact executed predicates.",
            "scientific_truth": "NOT_PROMOTED; derivations and external literature remain Step 44/Phase 071.",
            "synthetic_roundtrip": "Internal recoverability only, not experimental validation.",
            "golden_comparison": "Internal regression identity only.",
        },
        "environment": dependency_versions(),
        "code_summary": {
            "files":len(code),
            "physical_lines":sum(item["physical_lines"] for item in code),
            "definitions":sum(len(item["definitions"]) for item in code),
            "public_entries":sum(sum(1 for record in item["definitions"] if record["public_entry"]) for item in code),
            "call_edges":sum(len(item["call_edges"]) for item in code),
            "assert_nodes":sum(len(item["assert_nodes"]) for item in code),
            "module_and_class_state_records":sum(len(item["module_and_class_state"]) for item in code),
            "path_semantic_records":sum(len(item["path_semantics"]) for item in code),
            "semantic_fields":["public_entry","signature.parameters","signature.return_annotation","docstring","state_writes","explicit_raises","exception_handlers","branch_tests","side_effect_calls","module_and_class_state","path_semantics.inputs","path_semantics.outputs","path_semantics.defaults","path_semantics.errors","path_semantics.fallbacks","path_semantics.dormant_or_ignored"],
        },
        "code_index": code,
        "claim_gate_summary": {"records":len(CLAIM_GATE_SPECS),"ids":[item["id"] for item in CLAIM_GATE_SPECS]},
        "claim_gate_index": CLAIM_GATE_SPECS,
        "runtime": {"pass_count":2,"passes":[first,second],"byte_identical_records":reproducible,"semantic_summary":semantic_runtime_summary(first)},
        "golden_npz": npz_audit(),
        "v1020_snapshot_witness": snapshot_audit(),
        "findings": FINDINGS,
        "finding_summary": {"P0":len(FINDINGS["P0"]),"P1":len(FINDINGS["P1"]),"P2":len(FINDINGS["P2"])},
        "routes": {
            "CTR-001":["STEP42_RUNTIME_AND_ARTIFACT_AUDIT","STEP43_DOCUMENT_TO_REACHABLE_CODE"],
            "CTR-002":["STEP42_RUNTIME_AND_ARTIFACT_AUDIT","STEP43_DOCUMENT_TO_REACHABLE_CODE"],
            "CTR-003":["STEP42_RUNTIME_AND_ARTIFACT_AUDIT","STEP44_PHYSICS_REDERIVATION"],
            "UNR-001":"STEP43_DOCUMENT_TO_REACHABLE_CODE",
            "UNR-002":"STEP43_DOCUMENT_TO_REACHABLE_CODE",
            "UNR-003":"STEP44_PHYSICS_REDERIVATION_AND_PHASE071_REFERENCE_TRUTH",
            "UNR-004":"STEP43_DOCUMENT_TO_REACHABLE_CODE",
            "UNR-005":"STEP42_BOUNDED_RERUN_COMPLETE_GENERAL_VALIDITY_NOT_PROMOTED",
            "UNR-006":"STEP44_PHYSICS_REDERIVATION_AND_PHASE071_REFERENCE_TRUTH",
        },
    }


def write_json(path: Path, value: Any) -> None:
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-output", type=Path, default=DEFAULT_RUNTIME)
    parser.add_argument("--artifact-output", type=Path, default=DEFAULT_ARTIFACT)
    args = parser.parse_args()
    runtime = build_runtime_matrix()
    artifact = build_artifact_audit(runtime)
    write_json(args.runtime_output, runtime)
    write_json(args.artifact_output, artifact)
    print(f"WROTE {args.runtime_output} sha256={sha256(args.runtime_output.read_bytes())}")
    print(f"WROTE {args.artifact_output} sha256={sha256(args.artifact_output.read_bytes())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
