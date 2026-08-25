#!/usr/bin/env python3
"""Build the Phase 060 Step 43 document-led implementation trace.

The artifact is a bounded conformance map.  It preserves the distinction among
lexical document authority, frozen source behavior, internal source gates, and
scientific or experimental truth.  It does not validate literature or physics.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SOURCE_COMMIT = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
OUTPUT = ROOT / "Codex/results/PHASE_060_V1019_DOC_CODE_TRACE_MATRIX.json"
TOPOLOGY = "Codex/results/PHASE_060_V1019_SOURCE_TOPOLOGY.json"
ATTESTATION = "Codex/results/PHASE_060_V1019_TEX_READ_ATTESTATION.json"
PROCESS = "Codex/results/PHASE_060_V1019_PROCESS_INTENT_MATRIX.json"
RUNTIME = "Codex/results/PHASE_060_V1019_CODE_TEST_RUNTIME_MATRIX.json"
ARTIFACT = "Codex/results/PHASE_060_V1019_ARTIFACT_AUDIT.json"
CODE_PATHS = [
    "Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py",
    "Claude/docs/v1.0.19/fit_roundtrip_demo.py",
    "Claude/docs/v1.0.19/graph_suite_v1019.py",
    "Claude/docs/v1.0.19/test_regression_v1019.py",
]
MAIN_CODE = CODE_PATHS[0]

AUTH_LEXICAL = "LEXICAL_SOURCE_ANCHOR_ONLY_NOT_SCIENTIFIC_TRUTH"
AUTH_CODE = "FROZEN_SOURCE_BEHAVIOR_NOT_SCIENTIFIC_TRUTH"
AUTH_TEST = "INTERNAL_SOURCE_GATE_NOT_EXPERIMENTAL_VALIDATION"
AUTH_ARTIFACT = "STORED_OR_REBUILT_ARTIFACT_NOT_SCIENTIFIC_TRUTH"
AUTH_TRACE = "IMPLEMENTATION_CONFORMANCE_ONLY_EXTERNAL_TRUTH_DEFERRED"

CANDIDATE_KINDS = {
    "DISPLAYED_EQUATION",
    "DEFINITION_CANDIDATE",
    "ASSUMPTION_CANDIDATE",
    "SIGN_UNIT_DECLARATION_CANDIDATE",
    "CODE_MENTION_CANDIDATE",
    "FORWARD_REFERENCE_CANDIDATE",
}

FOCUS_FAMILIES = [
    "CH1_CHARGE_BALANCE",
    "CH1_CENTERS",
    "CH1_HYSTERESIS",
    "CH1_WIDTH",
    "CH1_BROADENING",
    "CH1_LAG_TAIL",
    "CH1_LCO",
    "CH1_MSMR",
    "CH2_PARTITION",
    "CH2_CONFIG",
    "CH2_VIBRATIONAL",
    "CH2_ELECTRONIC",
    "CH2_MIXING",
    "CH2_REVERSIBLE_HEAT",
]


def claim(
    trace_id: str,
    family: str,
    topic: str,
    anchors: list[tuple[str, int, int]],
    summary: str,
    relation: str,
    status: str,
    disposition: str,
    symbols: list[str],
    chain: list[tuple[str, str, int]],
    gates: list[str],
    consumers: list[str],
    execution_state: str = "ACTIVE",
    unit: str = "PASS",
    sign: str = "PASS",
    polarity: str = "DOCUMENT_SPECIFIC",
    test_disposition: str = "INDEXED_SOURCE_GATES_ONLY_NO_AST_ASSERT",
) -> dict[str, Any]:
    return {
        "trace_id": trace_id,
        "claim_id": trace_id.replace("TRC-", "CLM-"),
        "focus_family": family,
        "topic": topic,
        "anchors": anchors,
        "summary": summary,
        "relation": relation,
        "status": status,
        "implementation_disposition": disposition,
        "symbols": symbols,
        "chain": chain,
        "gates": gates,
        "consumers": consumers,
        "execution_state": execution_state,
        "unit": unit,
        "sign": sign,
        "polarity": polarity,
        "test_disposition": test_disposition,
    }


CLAIMS = [
    claim(
        "TRC-CH1-CHARGE-BALANCE", "CH1_CHARGE_BALANCE", "charge balance, polarization, and peak sum",
        [("Claude/docs/v1.0.19/_sections/ch1_sec01_n0n1.tex", 10, 21),
         ("Claude/docs/v1.0.19/_sections/ch1_sec01_n0n1.tex", 158, 183),
         ("Claude/docs/v1.0.19/_sections/ch1_sec06_eqpeak.tex", 8, 29),
         ("Claude/docs/v1.0.19/_sections/ch1_sec10_sum.tex", 5, 14)],
        "c-rate and current conversion, V_n=V_app-sigma_d|I|R_n, positive capacity-weighted peak sum",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV", "GraphiteAnodeDischargeDQDV.dqdv", "GraphiteAnodeDischargeDQDV.curve"],
        [("GraphiteAnodeDischargeDQDV.curve", "self.dqdv", 619)], ["MAIN-04", "REG-05"], ["ART-PDF-CH1", "ART-GOLDEN"]),
    claim(
        "TRC-CH1-CENTER-THERMO", "CH1_CENTERS", "thermodynamic transition center",
        [("Claude/docs/v1.0.19/_sections/ch1_sec03_center.tex", 22, 69)],
        "Delta G=-FU, U=(-Delta H+T Delta S)/F, and direct-U fallback",
        "DIRECT", "ALIGNED", "IMPLEMENTED", ["func_U_j", "GraphiteAnodeDischargeDQDV.equilibrium"],
        [("GraphiteAnodeDischargeDQDV.equilibrium", "func_U_j", 460)], ["MAIN-01", "REG-05"], ["ART-PDF-CH1", "ART-GOLDEN"]),
    claim(
        "TRC-CH1-HYSTERESIS", "CH1_HYSTERESIS", "spinodal hysteresis gap and branch center",
        [("Claude/docs/v1.0.19/_sections/ch1_sec04_hys.tex", 18, 30),
         ("Claude/docs/v1.0.19/_sections/ch1_sec04_hys.tex", 92, 139)],
        "Omega>2RT gap, signed branch center, gamma and h_eta phenomenology",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["func_dU_hys", "func_U_branch", "GraphiteAnodeDischargeDQDV.dqdv"],
        [("GraphiteAnodeDischargeDQDV.dqdv", "func_U_branch", 555), ("func_U_branch", "func_dU_hys", 153)],
        ["MAIN-07", "MAIN-09"], ["ART-PDF-CH1", "ART-GRAPH"], sign="PARTIAL", polarity="DISCHARGE_CENTER_ABOVE_CHARGE"),
    claim(
        "TRC-CH1-WIDTH-LOGISTIC", "CH1_WIDTH", "width and logistic progress",
        [("Claude/docs/v1.0.19/_sections/ch1_sec05_width.tex", 150, 203)],
        "w=nRT/F, direct-w inversion, n(T), and direction-signed logistic",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["func_w", "func_ksi_eq", "GraphiteAnodeDischargeDQDV.dqdv"],
        [("func_ksi_eq", "func_w", 92), ("GraphiteAnodeDischargeDQDV.dqdv", "func_ksi_eq", 562)],
        ["MAIN-10", "MAIN-12", "REG-07"], ["ART-PDF-CH1", "ART-GOLDEN"]),
    claim(
        "TRC-CH1-BROADENING-BUDGET", "CH1_BROADENING", "broadening source budget",
        [("Claude/docs/v1.0.19/_sections/ch1_sec07_broadening.tex", 34, 126),
         ("Claude/docs/v1.0.19/_sections/ch1_sec07_broadening.tex", 179, 262)],
        "rate tail, intrinsic width, and apparent-U ensemble are distinct; inverse reconstruction is prohibited",
        "RELATED_NOT_DIRECT", "PARTIAL", "PARTIAL", ["func_w", "GraphiteAnodeDischargeDQDV.dqdv"], [],
        ["FIT-06", "FIT-08"], ["ART-PDF-CH1", "ART-FIT"], sign="NOT_APPLICABLE", polarity="NOT_APPLICABLE"),
    claim(
        "TRC-CH1-LAG-LENGTH", "CH1_LAG_TAIL", "lag length and kinetic bypass",
        [("Claude/docs/v1.0.19/_sections/ch1_sec08_lag.tex", 18, 23),
         ("Claude/docs/v1.0.19/_sections/ch1_sec08_lag.tex", 35, 74),
         ("Claude/docs/v1.0.19/_sections/ch1_sec08_lag.tex", 88, 126)],
        "positive L_q, cutoff affinity, L_V=|dV/dq|L_q, and direct-L_V bypass",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["func_L_q", "func_dH_a_eff", "func_chi_d", "GraphiteAnodeDischargeDQDV.dqdv"],
        [("GraphiteAnodeDischargeDQDV.dqdv", "self._resolve_lag_length", 566),
         ("GraphiteAnodeDischargeDQDV._resolve_lag_length", "func_L_q", 442)],
        ["MAIN-06", "MAIN-14"], ["ART-PDF-CH1", "ART-GRAPH"]),
    claim(
        "TRC-CH1-TAIL-CAUSAL", "CH1_LAG_TAIL", "causal exponential tail",
        [("Claude/docs/v1.0.19/_sections/ch1_sec09_tail.tex", 20, 64),
         ("Claude/docs/v1.0.19/_sections/ch1_sec09_tail.tex", 95, 144),
         ("Claude/docs/v1.0.19/_sections/ch1_sec09_tail.tex", 168, 190)],
        "direction-reversed causal memory, nonnegative peak, and L_V to zero recovery",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV.dqdv"],
        [("GraphiteAnodeDischargeDQDV.dqdv", "_causal_memory_pointwise", 579)], ["MAIN-08", "REG-05"],
        ["ART-PDF-CH1", "ART-GOLDEN"]),
    claim(
        "TRC-CH1-LOW-CURRENT-HYS-LIMIT", "CH1_HYSTERESIS", "physical low-current limit with hysteresis",
        [("Claude/docs/v1.0.19/_sections/ch1_sec06_eqpeak.tex", 30, 39)],
        "gamma nonzero leaves a branch-centered low-current limit; it is not the reversible baseline",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV.dqdv"],
        [("GraphiteAnodeDischargeDQDV.dqdv", "func_U_branch", 555)], ["MAIN-09"], ["ART-PDF-CH1", "ART-GRAPH"],
        polarity="HYSTERESIS_REMAINS_WHEN_GAMMA_NONZERO"),
    claim(
        "TRC-CH1-REVERSIBLE-BASELINE", "CH1_CHARGE_BALANCE", "branch-free reversible equilibrium baseline",
        [("Claude/docs/v1.0.19/_sections/ch1_appB_codemap.tex", 8, 16)],
        "equilibrium intentionally sums U_j-centered peaks without hysteresis branch shift",
        "DIRECT", "ALIGNED", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV.equilibrium"],
        [("GraphiteAnodeDischargeDQDV.equilibrium", "func_ksi_eq", 465)], ["REG-05"], ["ART-PDF-CH1", "ART-GOLDEN"],
        polarity="REVERSIBLE_BRANCH_FREE_BASELINE"),
    claim(
        "TRC-CH1-LCO-DIRECTION-CENTER", "CH1_LCO", "LCO direction and center",
        [("Claude/docs/v1.0.19/_sections/ch1_sec11_lcointro.tex", 31, 49),
         ("Claude/docs/v1.0.19/_sections/ch1_sec11_lcointro.tex", 83, 120),
         ("Claude/docs/v1.0.19/_sections/ch1_sec12_lcocenter.tex", 34, 86)],
        "LCO charge is delithiation sigma_d=+1; center shares U=(-dH+TdS)/F with integral correction for T-dependent entropy",
        "DIRECT", "PARTIAL", "PARTIAL", ["func_U_j", "LCOCathodeDQDV", "GraphiteAnodeDischargeDQDV.curve"],
        [("GraphiteAnodeDischargeDQDV.curve", "self.dqdv", 619)], ["GRAPH-V1", "GRAPH-V7"],
        ["ART-PDF-CH1", "ART-GRAPH"], sign="PARTIAL", polarity="LCO_CHARGE_IS_DELITHIATION_POSITIVE"),
    claim(
        "TRC-CH1-LCO-HYSTERESIS", "CH1_LCO", "LCO optional hysteresis",
        [("Claude/docs/v1.0.19/_sections/ch1_sec13_lcohys.tex", 27, 39),
         ("Claude/docs/v1.0.19/_sections/ch1_sec13_lcohys.tex", 41, 103)],
        "LCO Omega is unassigned by default and branch physics is dormant until explicit assignment",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["LCOCathodeDQDV", "func_dU_hys", "func_U_branch"],
        [("GraphiteAnodeDischargeDQDV.dqdv", "func_U_branch", 555)], ["GRAPH-V1"], ["ART-PDF-CH1", "ART-GRAPH"],
        execution_state="DORMANT_BY_DEFAULT", sign="PARTIAL"),
    claim(
        "TRC-CH1-LCO-ENTROPY-ELECTRONIC", "CH2_ELECTRONIC", "LCO entropy decomposition and MIT electronic term",
        [("Claude/docs/v1.0.19/_sections/ch1_sec14_lcodecomp.tex", 20, 82),
         ("Claude/docs/v1.0.19/_sections/ch1_sec15_lcoelec.tex", 41, 44),
         ("Claude/docs/v1.0.19/_sections/ch1_sec15_lcoelec.tex", 83, 172)],
        "config/vib/electronic slots, negative insertion electronic entropy, eV-to-J and molar conversion, T-dependent center target",
        "DIRECT", "PARTIAL", "PARTIAL", ["func_dSe_molar", "LCOCathodeDQDV"],
        [("LCOCathodeDQDV._effective_dS_rxn", "func_dSe_molar", 932)], ["GRAPH-V6", "GRAPH-V7"],
        ["ART-PDF-CH1", "ART-LCO-HEAT"], sign="PARTIAL", polarity="INSERTION_ELECTRONIC_ENTROPY_NEGATIVE"),
    claim(
        "TRC-CH1-LCO-PEAK", "CH1_LCO", "LCO peak construction",
        [("Claude/docs/v1.0.19/_sections/ch1_sec16_lcopeak.tex", 8, 65)],
        "positive capacity-weighted LCO bell with center, height, area, and three-transition sum",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["LCOCathodeDQDV", "GraphiteAnodeDischargeDQDV.equilibrium", "GraphiteAnodeDischargeDQDV.dqdv"],
        [("GraphiteAnodeDischargeDQDV.dqdv", "func_ksi_eq", 562)], ["GRAPH-V1"], ["ART-PDF-CH1", "ART-GRAPH"]),
    claim(
        "TRC-CH1-MSMR-MAP", "CH1_MSMR", "MSMR functional mapping",
        [("Claude/docs/v1.0.19/_sections/ch1_sec17_msmr.tex", 9, 67)],
        "MSMR correspondence is functional isomorphism, not identity of physical quantities",
        "RELATED_NOT_DIRECT", "UNVERIFIED", "PARTIAL", ["LCOCathodeDQDV"], [], ["GRAPH-V1"],
        ["ART-PDF-CH1", "ART-GRAPH"], unit="PARTIAL", sign="PARTIAL"),
    claim(
        "TRC-CH1-LCO-FULL-PLUGIN", "CH1_LCO", "full composition-dependent LCO plug-in chain",
        [("Claude/docs/v1.0.19/_sections/ch1_sec17_msmr.tex", 76, 128),
         ("Claude/docs/v1.0.19/_sections/ch1_appB_codemap.tex", 127, 135)],
        "x(xi) to electronic entropy to center to branch to peak is only partly active; current electronic path freezes x_center and T_ref",
        "RELATED_NOT_DIRECT", "PARTIAL", "PARTIAL", ["func_dSe_molar", "LCOCathodeDQDV"], [],
        ["GRAPH-V6", "GRAPH-V7"], ["ART-PDF-CH1", "ART-LCO-HEAT"], unit="PARTIAL", sign="PARTIAL"),
    claim(
        "TRC-CH2-PARTITION-LOGISTIC", "CH2_PARTITION", "partition function to logistic complement",
        [("Claude/docs/v1.0.19/_sections/ch2_sec01_partition.tex", 16, 100)],
        "grand-canonical occupancy theta and delithiation xi=1-theta lead to s=+1 equilibrium logistic",
        "RELATED_NOT_DIRECT", "UNVERIFIED", "PARTIAL", ["func_ksi_eq", "GraphiteAnodeDischargeDQDV.solve_U_oc"],
        [], ["MAIN-12"], ["ART-PDF-CH2", "ART-GOLDEN"], polarity="EQUILIBRIUM_S_POSITIVE_NOT_DIRECTION_SIGMA"),
    claim(
        "TRC-CH2-PARTITION-BW", "CH2_PARTITION", "Bragg-Williams criticality",
        [("Claude/docs/v1.0.19/_sections/ch2_sec01_partition.tex", 103, 135)],
        "Bragg-Williams free energy and Omega=2RT criticality are related to, but not identical with, the implemented hysteresis helper",
        "RELATED_NOT_DIRECT", "UNVERIFIED", "PARTIAL", ["func_dU_hys"], [], ["MAIN-07", "MAIN-09"],
        ["ART-PDF-CH2", "ART-GRAPH"], sign="NOT_APPLICABLE", polarity="NOT_APPLICABLE"),
    claim(
        "TRC-CH2-CONFIGURATIONAL", "CH2_CONFIG", "configurational entropy and no-double-counting rule",
        [("Claude/docs/v1.0.19/_sections/ch2_sec02_config.tex", 11, 68),
         ("Claude/docs/v1.0.19/_sections/ch2_sec02_config.tex", 108, 130)],
        "partial-molar config logarithm is added once to the center standard entropy",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV.entropy_coefficient"],
        [("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._dwdT", 685)],
        ["MAIN-10", "MAIN-12", "GRAPH-V4"], ["ART-PDF-CH2", "ART-GRAPH"]),
    claim(
        "TRC-CH2-VIBRATIONAL-ELECTRONIC", "CH2_VIBRATIONAL", "vibrational and electronic entropy distributions",
        [("Claude/docs/v1.0.19/_sections/ch2_sec03_vibel.tex", 11, 35),
         ("Claude/docs/v1.0.19/_sections/ch2_sec03_vibel.tex", 37, 87)],
        "Bose-Einstein vibrational and Fermi-Dirac electronic terms are distinct from activation entropy",
        "DIRECT", "PARTIAL", "PARTIAL", ["func_dSe_molar", "GraphiteAnodeDischargeDQDV.entropy_coefficient", "LCOCathodeDQDV"],
        [("LCOCathodeDQDV._effective_dS_rxn", "func_dSe_molar", 932)], ["GRAPH-V6", "GRAPH-V7", "REG-07"],
        ["ART-PDF-CH2", "ART-VIB", "ART-LCO-HEAT"], sign="PARTIAL"),
    claim(
        "TRC-CH2-EINSTEIN-ROUNDTRIP", "CH2_VIBRATIONAL", "Einstein vibrational round trip",
        [("Claude/docs/v1.0.19/_sections/ch2_sec04_einstein.tex", 17, 95)],
        "theta_E optional correction preserves T_ref and satisfies dDeltaU/dT=DeltaS/F; absence is bit-exact zero",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV.entropy_coefficient", "GraphiteAnodeDischargeDQDV.equilibrium"],
        [("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._vib_dS", 672),
         ("GraphiteAnodeDischargeDQDV.equilibrium", "self._vib_dU", 460)],
        ["REG-07", "GRAPH-V7"], ["ART-PDF-CH2", "ART-VIB"], test_disposition="NO_DEDICATED_FAILING_SOURCE_GATE_SUPPLEMENTAL_STEP42_PROBE_ONLY"),
    claim(
        "TRC-CH2-MIXING-IMPLICIT", "CH2_MIXING", "charge-conservation implicit solve",
        [("Claude/docs/v1.0.19/_sections/ch2_sec05_mixing.tex", 12, 52)],
        "sum Q_j xi_j(U,T)=Q x_bar, x_bar=1-x, and implicit differentiation",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV.solve_U_oc", "GraphiteAnodeDischargeDQDV.entropy_coefficient_x"],
        [("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.solve_U_oc", 807),
         ("GraphiteAnodeDischargeDQDV.solve_U_oc.<local>._charge", "func_ksi_eq", 766)],
        ["MAIN-10", "MAIN-12"], ["ART-PDF-CH2", "ART-GRAPH"]),
    claim(
        "TRC-CH2-MIXING-WEIGHTED", "CH2_MIXING", "weighted simple and complete entropy coefficient",
        [("Claude/docs/v1.0.19/_sections/ch2_sec05_mixing.tex", 67, 110),
         ("Claude/docs/v1.0.19/_sections/ch2_sec05_mixing.tex", 143, 156)],
        "Q_j g_j weighted center term plus config term gives a continuous blend, not an experimental validation",
        "DIRECT", "ALIGNED", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV.entropy_coefficient", "GraphiteAnodeDischargeDQDV.entropy_coefficient_x"],
        [("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.entropy_coefficient", 808)],
        ["MAIN-10", "MAIN-12", "GRAPH-V4"], ["ART-PDF-CH2", "ART-GRAPH"]),
    claim(
        "TRC-CH2-WIDTH-T-DEPENDENCE", "CH1_WIDTH", "width-temperature state contract",
        [("Claude/docs/v1.0.19/_sections/ch2_sec05_mixing.tex", 54, 65),
         ("Claude/docs/v1.0.19/_sections/ch2_sec05_mixing.tex", 158, 191),
         ("Claude/docs/v1.0.19/_sections/ch2_sec08_synthesis.tex", 31, 35)],
        "n and n(T) propagate dwidth/dT; direct w is frozen; the no-n/no-w default is internally inconsistent",
        "DIRECT", "MISALIGNED", "PARTIAL", ["func_w", "GraphiteAnodeDischargeDQDV.entropy_coefficient"],
        [("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._dwdT", 685)], ["MAIN-10", "MAIN-12", "REG-07"],
        ["ART-PDF-CH2", "ART-GRAPH"], sign="NOT_APPLICABLE", polarity="NOT_APPLICABLE"),
    claim(
        "TRC-CH2-HYSTERESIS-REVERSIBLE", "CH2_MIXING", "reversible branch average versus hysteresis dissipation",
        [("Claude/docs/v1.0.19/_sections/ch2_sec05_mixing.tex", 193, 223)],
        "explicit branch-average entropy is absent; equilibrium-center evaluation is only a symmetric approximation",
        "RELATED_NOT_DIRECT", "ABSENT", "MISSING", ["GraphiteAnodeDischargeDQDV.entropy_coefficient", "GraphiteAnodeDischargeDQDV.irreversible_heat"],
        [], [], ["ART-PDF-CH2"], sign="PARTIAL", test_disposition="NO_SOURCE_GATE_IMPLEMENTATION_ABSENT"),
    claim(
        "TRC-CH2-REVERSIBLE-HEAT", "CH2_REVERSIBLE_HEAT", "Bernardi reversible heat",
        [("Claude/docs/v1.0.19/_sections/ch2_sec07_revheat.tex", 10, 40),
         ("Claude/docs/v1.0.19/_sections/ch2_sec07_revheat.tex", 42, 52)],
        "q_rev=-I T dU_oc/dT with cell-discharge current label distinct from Chapter 1 delithiation label",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV.reversible_heat", "GraphiteAnodeDischargeDQDV.reversible_heat_x"],
        [("GraphiteAnodeDischargeDQDV.reversible_heat", "self.entropy_coefficient", 707),
         ("GraphiteAnodeDischargeDQDV.reversible_heat_x", "self.entropy_coefficient_x", 829)],
        ["MAIN-10", "MAIN-11"], ["ART-PDF-CH2", "ART-GRAPH"], polarity="QREV_EQUALS_NEGATIVE_I_T_DUDT"),
    claim(
        "TRC-CH2-COMPLETE-SYNTHESIS", "CH2_MIXING", "complete synthesis equation",
        [("Claude/docs/v1.0.19/_sections/ch2_sec08_synthesis.tex", 11, 39)],
        "complete/simple/config outputs follow charge solve and feed reversible heat; n or dwidth/dT is an implicit required state",
        "DIRECT", "PARTIAL", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV.entropy_coefficient", "GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "GraphiteAnodeDischargeDQDV.reversible_heat_x"],
        [("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.entropy_coefficient", 808),
         ("GraphiteAnodeDischargeDQDV.reversible_heat_x", "self.entropy_coefficient_x", 829)],
        ["MAIN-10", "MAIN-11", "MAIN-12"], ["ART-PDF-CH2", "ART-GRAPH"]),
    claim(
        "TRC-CH2-REGRESSION-WITNESSES", "CH2_REVERSIBLE_HEAT", "worked-example regression witnesses",
        [("Claude/docs/v1.0.19/_sections/ch2_sec08_synthesis.tex", 41, 105),
         ("Claude/docs/v1.0.19/_sections/ch2_sec08_synthesis.tex", 107, 134),
         ("Claude/docs/v1.0.19/_sections/ch2_appB_codemap.tex", 24, 60)],
        "x_bar=.25 values, five-SOC sign alternation, finite-difference round trip, and theta_E-absence compatibility",
        "DIRECT", "ALIGNED", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV.solve_U_oc", "GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "GraphiteAnodeDischargeDQDV.reversible_heat_x"],
        [("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.solve_U_oc", 807),
         ("GraphiteAnodeDischargeDQDV.reversible_heat_x", "self.entropy_coefficient_x", 829)],
        ["MAIN-10", "MAIN-11", "MAIN-12"], ["ART-PDF-CH2", "ART-GRAPH"]),
    claim(
        "TRC-CH2-DOC-LEADS-BOUNDARY", "CH2_MIXING", "prospective document authority versus current implementation",
        [("Claude/docs/v1.0.19/_sections/ch2_appB_codemap.tex", 7, 22)],
        "Chapter 2 Appendix B is a requirement surface, not evidence of implementation; conformance is independently established from code and gates",
        "DIRECT", "ALIGNED", "IMPLEMENTED", ["GraphiteAnodeDischargeDQDV.solve_U_oc", "GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "GraphiteAnodeDischargeDQDV.reversible_heat_x"],
        [("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.solve_U_oc", 807),
         ("GraphiteAnodeDischargeDQDV.reversible_heat_x", "self.entropy_coefficient_x", 829)],
        ["MAIN-10", "MAIN-11", "MAIN-12"], ["ART-PDF-CH2", "ART-GRAPH"]),
]


# Each DIRECT/non-missing trace is backed by one or more ordered, contiguous
# local call paths.  Multiple paths are alternatives or branches and are never
# flattened into a single fictitious chain.
CHAIN_PATHS: dict[str, list[list[tuple[str, str, int]]]] = {
    "TRC-CH1-CHARGE-BALANCE": [[
        ("GraphiteAnodeDischargeDQDV.curve", "self.dqdv", 619),
        ("GraphiteAnodeDischargeDQDV.dqdv", "func_ksi_eq", 562),
        ("func_ksi_eq", "func_w", 92),
    ]],
    "TRC-CH1-CENTER-THERMO": [[
        ("GraphiteAnodeDischargeDQDV.equilibrium", "func_U_j", 460),
    ]],
    "TRC-CH1-HYSTERESIS": [[
        ("GraphiteAnodeDischargeDQDV.dqdv", "func_U_branch", 555),
        ("func_U_branch", "func_dU_hys", 153),
    ]],
    "TRC-CH1-WIDTH-LOGISTIC": [[
        ("GraphiteAnodeDischargeDQDV.dqdv", "func_ksi_eq", 562),
        ("func_ksi_eq", "func_w", 92),
    ]],
    "TRC-CH1-LAG-LENGTH": [
        [
            ("GraphiteAnodeDischargeDQDV.dqdv", "self._resolve_lag_length", 566),
            ("GraphiteAnodeDischargeDQDV._resolve_lag_length", "func_L_q", 442),
        ],
        [
            ("GraphiteAnodeDischargeDQDV.dqdv", "self._resolve_lag_length", 566),
            ("GraphiteAnodeDischargeDQDV._resolve_lag_length", "self._chi_and_dH_eff", 438),
            ("GraphiteAnodeDischargeDQDV._chi_and_dH_eff", "func_dH_a_eff", 399),
        ],
        [
            ("GraphiteAnodeDischargeDQDV.dqdv", "self._resolve_lag_length", 566),
            ("GraphiteAnodeDischargeDQDV._resolve_lag_length", "self._chi_and_dH_eff", 438),
            ("GraphiteAnodeDischargeDQDV._chi_and_dH_eff", "self._chi_d", 397),
            ("GraphiteAnodeDischargeDQDV._chi_d", "self.chi_split", 390),
        ],
    ],
    "TRC-CH1-TAIL-CAUSAL": [[
        ("GraphiteAnodeDischargeDQDV.dqdv", "_causal_memory_pointwise", 579),
    ]],
    "TRC-CH1-LOW-CURRENT-HYS-LIMIT": [[
        ("GraphiteAnodeDischargeDQDV.dqdv", "func_U_branch", 555),
        ("func_U_branch", "func_dU_hys", 153),
    ]],
    "TRC-CH1-REVERSIBLE-BASELINE": [[
        ("GraphiteAnodeDischargeDQDV.equilibrium", "func_ksi_eq", 465),
        ("func_ksi_eq", "func_w", 92),
    ]],
    "TRC-CH1-LCO-DIRECTION-CENTER": [[
        ("GraphiteAnodeDischargeDQDV.curve", "self.dqdv", 619),
        ("GraphiteAnodeDischargeDQDV.dqdv", "func_U_j", 546),
    ]],
    "TRC-CH1-LCO-HYSTERESIS": [[
        ("GraphiteAnodeDischargeDQDV.dqdv", "func_U_branch", 555),
        ("func_U_branch", "func_dU_hys", 153),
    ]],
    "TRC-CH1-LCO-ENTROPY-ELECTRONIC": [
        [
            ("GraphiteAnodeDischargeDQDV.equilibrium", "self._effective_dS_rxn", 460),
            ("LCOCathodeDQDV._effective_dS_rxn", "func_dSe_molar", 932),
        ],
        [
            ("GraphiteAnodeDischargeDQDV.dqdv", "self._effective_dS_rxn", 546),
            ("LCOCathodeDQDV._effective_dS_rxn", "func_dSe_molar", 932),
        ],
        [
            ("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._effective_dS_rxn", 671),
            ("LCOCathodeDQDV._effective_dS_rxn", "func_dSe_molar", 932),
        ],
    ],
    "TRC-CH1-LCO-PEAK": [
        [
            ("GraphiteAnodeDischargeDQDV.dqdv", "func_ksi_eq", 562),
            ("func_ksi_eq", "func_w", 92),
        ],
        [
            ("GraphiteAnodeDischargeDQDV.equilibrium", "func_ksi_eq", 465),
            ("func_ksi_eq", "func_w", 92),
        ],
    ],
    "TRC-CH2-CONFIGURATIONAL": [[
        ("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._dwdT", 685),
    ]],
    "TRC-CH2-VIBRATIONAL-ELECTRONIC": [
        [("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._vib_dS", 672)],
        [
            ("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._effective_dS_rxn", 671),
            ("LCOCathodeDQDV._effective_dS_rxn", "func_dSe_molar", 932),
        ],
    ],
    "TRC-CH2-EINSTEIN-ROUNDTRIP": [
        [("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._vib_dS", 672)],
        [("GraphiteAnodeDischargeDQDV.equilibrium", "self._vib_dU", 460)],
    ],
    "TRC-CH2-MIXING-IMPLICIT": [[
        ("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.solve_U_oc", 807),
        ("GraphiteAnodeDischargeDQDV.solve_U_oc", "_charge", 773),
        ("GraphiteAnodeDischargeDQDV.solve_U_oc.<local>._charge", "func_ksi_eq", 766),
        ("func_ksi_eq", "func_w", 92),
    ]],
    "TRC-CH2-MIXING-WEIGHTED": [[
        ("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.entropy_coefficient", 808),
        ("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._dwdT", 685),
    ]],
    "TRC-CH2-WIDTH-T-DEPENDENCE": [
        [("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._dwdT", 685)],
        [
            ("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._width", 678),
            ("GraphiteAnodeDischargeDQDV._width", "func_w", 322),
        ],
    ],
    "TRC-CH2-REVERSIBLE-HEAT": [
        [("GraphiteAnodeDischargeDQDV.reversible_heat", "self.entropy_coefficient", 707)],
        [
            ("GraphiteAnodeDischargeDQDV.reversible_heat_x", "self.entropy_coefficient_x", 829),
            ("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.entropy_coefficient", 808),
        ],
    ],
    "TRC-CH2-COMPLETE-SYNTHESIS": [
        [
            ("GraphiteAnodeDischargeDQDV.reversible_heat_x", "self.entropy_coefficient_x", 829),
            ("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.solve_U_oc", 807),
            ("GraphiteAnodeDischargeDQDV.solve_U_oc", "_charge", 773),
            ("GraphiteAnodeDischargeDQDV.solve_U_oc.<local>._charge", "func_ksi_eq", 766),
            ("func_ksi_eq", "func_w", 92),
        ],
        [
            ("GraphiteAnodeDischargeDQDV.reversible_heat_x", "self.entropy_coefficient_x", 829),
            ("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.entropy_coefficient", 808),
            ("GraphiteAnodeDischargeDQDV.entropy_coefficient", "self._dwdT", 685),
        ],
    ],
    "TRC-CH2-REGRESSION-WITNESSES": [
        [
            ("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.solve_U_oc", 807),
            ("GraphiteAnodeDischargeDQDV.solve_U_oc", "_charge", 773),
            ("GraphiteAnodeDischargeDQDV.solve_U_oc.<local>._charge", "func_ksi_eq", 766),
            ("func_ksi_eq", "func_w", 92),
        ],
        [
            ("GraphiteAnodeDischargeDQDV.reversible_heat_x", "self.entropy_coefficient_x", 829),
            ("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.entropy_coefficient", 808),
        ],
    ],
    "TRC-CH2-DOC-LEADS-BOUNDARY": [[
        ("GraphiteAnodeDischargeDQDV.reversible_heat_x", "self.entropy_coefficient_x", 829),
        ("GraphiteAnodeDischargeDQDV.entropy_coefficient_x", "self.solve_U_oc", 807),
        ("GraphiteAnodeDischargeDQDV.solve_U_oc", "_charge", 773),
        ("GraphiteAnodeDischargeDQDV.solve_U_oc.<local>._charge", "func_ksi_eq", 766),
        ("func_ksi_eq", "func_w", 92),
    ]],
}


DYNAMIC_TARGET_OVERRIDES = {
    ("TRC-CH1-LAG-LENGTH", 3, 4): "func_chi_d",
    ("TRC-CH1-LCO-ENTROPY-ELECTRONIC", 1, 1): "LCOCathodeDQDV._effective_dS_rxn",
    ("TRC-CH1-LCO-ENTROPY-ELECTRONIC", 2, 1): "LCOCathodeDQDV._effective_dS_rxn",
    ("TRC-CH1-LCO-ENTROPY-ELECTRONIC", 3, 1): "LCOCathodeDQDV._effective_dS_rxn",
    ("TRC-CH2-VIBRATIONAL-ELECTRONIC", 2, 1): "LCOCathodeDQDV._effective_dS_rxn",
}


BOUNDARY_STATEMENTS: dict[str, tuple[str, str]] = {
    "TRC-CH1-CHARGE-BALANCE": ("c_rate[1/h]*Q_cell[Ah] gives |I|[A]; R_n[ohm] gives polarization[V]; Q_j[Ah]/w_j[V] gives dQ/dV[Ah/V]", "V_n=V_app-sigma_d*|I|*R_n and Q_j*xi*(1-xi)/w_j is nonnegative for Q_j,w_j>0"),
    "TRC-CH1-CENTER-THERMO": ("DeltaH[J/mol], T*DeltaS[J/mol], and F[C/mol] give U_j[V]", "U_j=(-DeltaH+T*DeltaS)/F and dU_j/dT=DeltaS/F"),
    "TRC-CH1-HYSTERESIS": ("Omega and RT[J/mol] divided by F[C/mol] give DeltaU_hys[V]", "Omega<=2RT gives zero; sigma_d=+1 shifts the branch center upward when gamma*h_eta*DeltaU_hys>0"),
    "TRC-CH1-WIDTH-LOGISTIC": ("n is dimensionless and RT/F gives w[V]; logistic argument (V_n-U)/w is dimensionless", "s=+1 makes xi increase with V_n and s=-1 reverses the progress direction"),
    "TRC-CH1-BROADENING-BUDGET": ("intrinsic w, lag L_V, center spread, and apparent standard deviation are all voltage scales[V]", "broadening terms are nonnegative magnitudes; inverse reconstruction is outside the implementation claim"),
    "TRC-CH1-LAG-LENGTH": ("L_q is dimensionless charge fraction and |dV/dq|[V] gives L_V[V]", "I<=0, missing dH_a, or zero dVdq_qa gives zero lag; direct nonnegative L_V bypasses kinetics"),
    "TRC-CH1-TAIL-CAUSAL": ("normalized exponential kernel[1/V] times dV is dimensionless; differentiated progress gives peak[1/V]", "discharge follows increasing V and charge decreasing V; the returned peak contribution is expected nonnegative"),
    "TRC-CH1-LOW-CURRENT-HYS-LIMIT": ("branch shift gamma*h_eta*DeltaU_hys has units[V] and is independent of |I|", "gamma!=0 can preserve charge/discharge center separation as |I| tends to zero"),
    "TRC-CH1-REVERSIBLE-BASELINE": ("equilibrium output is Cbg[Ah/V] plus Q_j[Ah]*xi*(1-xi)/w_j[V]", "equilibrium uses U_j without the sigma_d hysteresis branch shift"),
    "TRC-CH1-LCO-DIRECTION-CENTER": ("LCO center uses the same (-DeltaH+T*DeltaS)/F voltage dimension", "LCO cell charge maps to delithiation sigma_d=+1 at the curve facade"),
    "TRC-CH1-LCO-HYSTERESIS": ("optional LCO Omega[J/mol] produces a branch gap[V] through division by F", "default transitions omit active Omega/gamma; if supplied, Omega>2RT and gamma!=0 activate the signed shift"),
    "TRC-CH1-LCO-ENTROPY-ELECTRONIC": ("DOS conversion and Avogadro scaling produce DeltaS_e[J/(mol K)] and DeltaS_e/F[V/K]", "insertion electronic entropy is negative in the documented convention; the implemented seam freezes T at 298.15 K"),
    "TRC-CH1-LCO-PEAK": ("Q_j[Ah]*xi*(1-xi)/w_j[V] gives LCO dQ/dV[Ah/V]", "positive Q_j and w_j make the logistic bell nonnegative; its integral target is Q_j"),
    "TRC-CH1-MSMR-MAP": ("MSMR variables are mapped by corresponding dimension, not asserted identical", "the mapping is functional isomorphism only; no direct physical sign identity is asserted"),
    "TRC-CH1-LCO-FULL-PLUGIN": ("x is dimensionless, DeltaS_e/F is V/K, and integrated center correction is[V]", "the desired x(xi),T-dependent chain is only partially present and cannot receive a direct sign verdict"),
    "TRC-CH2-PARTITION-LOGISTIC": ("partition exponents and (V-U)/w are dimensionless", "xi=1-theta makes equilibrium xi increase with V under fixed s=+1"),
    "TRC-CH2-PARTITION-BW": ("Omega and RT are molar energies[J/mol] in the critical ratio Omega/(RT)", "Omega=2RT is the documented critical boundary; relation to the helper is not a direct implementation identity"),
    "TRC-CH2-CONFIGURATIONAL": ("R*log(xi/(1-xi))[J/(mol K)] divided by F gives V/K", "the configurational logarithm changes sign at xi=0.5 and must be added exactly once"),
    "TRC-CH2-VIBRATIONAL-ELECTRONIC": ("vibrational/electronic entropy terms are J/(mol K) and enter voltage slope through division by F", "vibrational insertion baseline and electronic insertion convention are negative in the cited document paths"),
    "TRC-CH2-EINSTEIN-ROUNDTRIP": ("theta_E and T are[K]; DeltaS_vib/F is V/K and DeltaU_vib is[V]", "both corrections are zero at T_ref and theta_E absence is the exact zero path"),
    "TRC-CH2-MIXING-IMPLICIT": ("sum Q_j[Ah]*xi_j equals Q_total[Ah]*x_bar; U_oc is[V]", "the charge residual is monotone increasing in U_oc for fixed s=+1"),
    "TRC-CH2-MIXING-WEIGHTED": ("Q_j*g_j has Ah/V and weighted V/K terms yield dU_oc/dT[V/K]", "complete equals simple plus config, with the config logarithm carrying the SOC-dependent sign"),
    "TRC-CH2-WIDTH-T-DEPENDENCE": ("dw/dT has V/K and equals (R/F)*(n(T)+T*dn/dT) on the n path", "the no-n/no-w route is misaligned because width is RT/F while _dwdT returns zero"),
    "TRC-CH2-HYSTERESIS-REVERSIBLE": ("branch-average temperature coefficient would be[V/K] and hysteresis dissipation[W]", "no explicit finite-gap branch-average implementation exists; an exact cancellation sign is not claimed"),
    "TRC-CH2-REVERSIBLE-HEAT": ("I[A]*T[K]*dU/dT[V/K] gives reversible heat[W]", "q_rev=-I*T*dU_oc/dT under the Bernardi cell-current convention"),
    "TRC-CH2-COMPLETE-SYNTHESIS": ("the complete weighted numerator/denominator reduces to V/K and q_rev to W", "the config contribution follows dw/dT*log(xi/(1-xi)); missing width-state information remains partial"),
    "TRC-CH2-REGRESSION-WITNESSES": ("stored U_oc[V], dU/dT[V/K], and q_rev/I[V] witnesses use explicit numerical tolerances", "the five-SOC witness preserves the documented heat/sign alternation and q_rev=-I*T*dU/dT"),
    "TRC-CH2-DOC-LEADS-BOUNDARY": ("the prospective input/output contract declares x_bar, T, U_oc[V], dU/dT[V/K], and q_rev[W]", "document requirements do not determine implementation signs without the independently anchored source path and gates"),
}


OPTIONAL_MEMBERS: dict[str, list[str]] = {
    "seed_T_seed_I_seed_Q_cell": ["seed_T", "seed_I", "seed_Q_cell"],
    "dH_rxn_dS_rxn": ["dH_rxn", "dS_rxn"],
    "Omega_gamma_h_eta": ["Omega", "gamma", "h_eta"],
    "z_cut_A_cap_RT_use_dH_eff": ["z_cut", "A_cap_RT", "use_dH_eff"],
    "electronic_x_center_gmax_xMIT_dxMIT": ["electronic", "x_center", "g_max_eV", "x_MIT", "dx_MIT"],
    "I_abs_Q_cell_T_V": ["I_abs", "Q_cell", "T", "V_app_or_V_n"],
    "U_lo_U_hi": ["U_lo", "U_hi"],
    "tol_max_iter": ["tol", "max_iter"],
}


OPTIONAL_INPUTS = [
    ("transitions", "ACCEPTED_REFERENCE", "PARTIAL", "stored by reference; schema is validated lazily by paths"),
    ("x", "ACCEPTED_VALIDATED_FINITE", "CONDITIONALLY_USED", "fallback for chi; dormant when chi is supplied; 0..1 not enforced"),
    ("chi", "ACCEPTED_VALIDATED_FINITE", "CONDITIONALLY_USED", "computed lag only; 0..1 not enforced"),
    ("chi_split", "ACCEPTED_VALIDATED_CALLABLE", "CONDITIONALLY_USED", "computed lag only; bypassed by direct L_V or zero lag"),
    ("Rn", "ACCEPTED_VALIDATED_NONNEGATIVE", "USED", "polarization in dqdv"),
    ("Cbg", "ACCEPTED_SCALAR_OR_CALLABLE", "USED_WITH_UNVALIDATED_OUTPUT", "equilibrium and dqdv background"),
    ("seed_T_seed_I_seed_Q_cell", "ACCEPTED_VALIDATED", "DIAGNOSTIC_ONLY", "eager seed_L_V; not consumed by production dqdv"),
    ("U", "ACCEPTED_LAZY", "IGNORED_WHEN_DH_DS_PAIR", "fallback center only"),
    ("dH_rxn_dS_rxn", "ACCEPTED_LAZY", "PAIR_CONDITIONALLY_USED", "pair overrides U; incomplete pair falls back to U"),
    ("n", "ACCEPTED_VALIDATED_FINITE", "USED_AND_DOMINATES_W", "thermal width and dwidth/dT"),
    ("w", "ACCEPTED_LAZY", "USED_ONLY_WHEN_N_ABSENT", "ignored and unvalidated when n exists; direct-w dwidth/dT=0"),
    ("n_T1", "ACCEPTED_REQUIRES_N", "CONDITIONALLY_USED", "linear n(T) and dwidth/dT"),
    ("n_T_ref", "ACCEPTED_VALIDATED_FINITE", "CONDITIONALLY_USED", "numerically dormant when n_T1=0"),
    ("theta_E", "ACCEPTED_VALIDATED_POSITIVE", "OPTIONAL_ZERO_WHEN_ABSENT", "vib center and entropy correction"),
    ("theta_E_Tref", "ACCEPTED_VALIDATED_FINITE", "CONDITIONALLY_USED", "used only with theta_E; positivity not enforced"),
    ("L_V", "ACCEPTED_VALIDATED_NONNEGATIVE", "BYPASSES_KINETICS", "overrides I/Q/dH/dS/Omega/chi/dVdq/cutoff path"),
    ("dH_a", "ACCEPTED_LAZY", "CONDITIONALLY_USED", "absence or I<=0 yields zero lag at resolver"),
    ("dS_a", "ACCEPTED_DEFAULT_ZERO", "CONDITIONALLY_USED", "computed kinetic lag only"),
    ("Omega_gamma_h_eta", "ACCEPTED_LAZY", "DORMANT_UNLESS_ACTIVE", "branch requires gamma nonzero and Omega positive"),
    ("dVdq_qa", "ACCEPTED_DEFAULT_ZERO", "CONDITIONALLY_USED", "zero makes computed L_V zero"),
    ("z_cut_A_cap_RT_use_dH_eff", "ACCEPTED_VALIDATED_ON_ACTIVE_PATH", "OVERRIDE_SHADOWS_GLOBAL", "computed lag only"),
    ("electronic_x_center_gmax_xMIT_dxMIT", "ACCEPTED_LAZY", "LCO_OPT_IN", "electronic true requires keys; caller T ignored in favor of 298.15 K"),
    ("direction", "CURVE_VALIDATED", "USED", "LCO facade flips cell label; low-level dqdv s bypasses facade"),
    ("c_rate", "VALIDATED_ONLY_WHEN_USED", "IGNORED_WHEN_I_ABS_PRESENT", "I_abs overrides c_rate"),
    ("I_abs_Q_cell_T_V", "PARTIALLY_VALIDATED", "USED", "array T is pointwise but branch and lag use mean T_rep"),
    ("return_terms", "TRUTHINESS_ONLY", "CONDITIONALLY_USED", "dict complete/simple/config when truthy"),
    ("U_lo_U_hi", "VALIDATED_FINITE_AND_ORDERED", "OPTIONAL_OVERRIDE", "otherwise automatic bracket"),
    ("tol_max_iter", "ACCEPTED_UNVALIDATED", "USED_WITHOUT_EXHAUSTION_FAILURE", "nonpositive or exhausted iteration may return midpoint"),
    ("heat_I", "ACCEPTED_UNVALIDATED", "USED", "finite/sign and q_irr nonnegativity are not enforced"),
]


PRODUCTION_TRACE_MAP = {
    "func_w": ["TRC-CH1-WIDTH-LOGISTIC", "TRC-CH2-WIDTH-T-DEPENDENCE"],
    "func_U_j": ["TRC-CH1-CENTER-THERMO", "TRC-CH1-LCO-DIRECTION-CENTER"],
    "func_ksi_eq": ["TRC-CH1-WIDTH-LOGISTIC", "TRC-CH2-PARTITION-LOGISTIC"],
    "func_L_q": ["TRC-CH1-LAG-LENGTH"],
    "func_dU_hys": ["TRC-CH1-HYSTERESIS", "TRC-CH2-PARTITION-BW"],
    "func_U_branch": ["TRC-CH1-HYSTERESIS", "TRC-CH1-LOW-CURRENT-HYS-LIMIT"],
    "func_dH_a_eff": ["TRC-CH1-LAG-LENGTH"],
    "func_chi_d": ["TRC-CH1-LAG-LENGTH"],
    "func_dSe_molar": ["TRC-CH1-LCO-ENTROPY-ELECTRONIC", "TRC-CH2-VIBRATIONAL-ELECTRONIC"],
    "GraphiteAnodeDischargeDQDV": ["TRC-CH1-CHARGE-BALANCE"],
    "GraphiteAnodeDischargeDQDV.equilibrium": ["TRC-CH1-REVERSIBLE-BASELINE", "TRC-CH1-LCO-PEAK"],
    "GraphiteAnodeDischargeDQDV.dqdv": ["TRC-CH1-CHARGE-BALANCE", "TRC-CH1-HYSTERESIS", "TRC-CH1-TAIL-CAUSAL"],
    "GraphiteAnodeDischargeDQDV.curve": ["TRC-CH1-CHARGE-BALANCE", "TRC-CH1-LCO-DIRECTION-CENTER"],
    "GraphiteAnodeDischargeDQDV.entropy_coefficient": ["TRC-CH2-CONFIGURATIONAL", "TRC-CH2-MIXING-WEIGHTED", "TRC-CH2-WIDTH-T-DEPENDENCE"],
    "GraphiteAnodeDischargeDQDV.reversible_heat": ["TRC-CH2-REVERSIBLE-HEAT"],
    "GraphiteAnodeDischargeDQDV.solve_U_oc": ["TRC-CH2-MIXING-IMPLICIT", "TRC-CH2-REGRESSION-WITNESSES"],
    "GraphiteAnodeDischargeDQDV.entropy_coefficient_x": ["TRC-CH2-COMPLETE-SYNTHESIS", "TRC-CH2-REGRESSION-WITNESSES"],
    "GraphiteAnodeDischargeDQDV.reversible_heat_x": ["TRC-CH2-REVERSIBLE-HEAT", "TRC-CH2-REGRESSION-WITNESSES"],
    "GraphiteAnodeDischargeDQDV.irreversible_heat": ["TRC-CH2-HYSTERESIS-REVERSIBLE"],
    "LCOCathodeDQDV": ["TRC-CH1-LCO-DIRECTION-CENTER", "TRC-CH1-LCO-HYSTERESIS", "TRC-CH1-LCO-ENTROPY-ELECTRONIC"],
}


FINDINGS = {
    "P0": [],
    "P1": [
        {"id": "P1-43-001", "summary": "No-n/no-w uses thermal width RT/F while _dwdT returns zero.", "route": "TRC-CH2-WIDTH-T-DEPENDENCE"},
        {"id": "P1-43-002", "summary": "LCO electronic entropy is frozen at 298.15 K; the documented full T-dependent center curvature is not restored.", "route": "TRC-CH1-LCO-ENTROPY-ELECTRONIC"},
        {"id": "P1-43-003", "summary": "Explicit reversible hysteresis branch averaging is absent; equilibrium-center evaluation is only a bounded approximation.", "route": "TRC-CH2-HYSTERESIS-REVERSIBLE"},
        {"id": "P1-43-004", "summary": "Chapter 2 Appendix B is prospective authority while Chapter 1 Appendix B describes current v1.0.19 behavior.", "route": "TRC-CH2-DOC-LEADS-BOUNDARY"},
        {"id": "P1-43-005", "summary": "Physical low-current hysteresis and the separate branch-free reversible baseline must not be merged.", "route": "TRC-CH1-LOW-CURRENT-HYS-LIMIT"},
        {"id": "P1-43-006", "summary": "Step 42's 444-edge index is definition-body scoped, not the full 882-call module execution graph, and omitted _ok.", "route": "EVIDENCE-SCOPE"},
        {"id": "P1-43-007", "summary": "Graph suite has no aggregate failing exit gate.", "route": "TEST-GRAPH"},
        {"id": "P1-43-008", "summary": "Module overall OK covers only a subset of displayed expectations.", "route": "TEST-MODULE"},
        {"id": "P1-43-009", "summary": "Regression PASS excludes area and theta_E/n_T1 absence checks.", "route": "TEST-REGRESSION"},
        {"id": "P1-43-010", "summary": "Fit area-conservation label gates sum-Q ratio, not curve integration.", "route": "TEST-FIT"},
        {"id": "P1-43-011", "summary": "Broadening ensemble forward averaging and width-budget calculation are not production implementations.", "route": "TRC-CH1-BROADENING-BUDGET"},
        {"id": "P1-43-012", "summary": "The public irreversible heat helper is dormant and no public total-heat composition entry point exists.", "route": "TRC-CH2-REVERSIBLE-HEAT"},
    ],
    "P2": [
        {"id": "P2-43-001", "summary": "solve_U_oc does not validate tol/max_iter or fail on exhaustion."},
        {"id": "P2-43-002", "summary": "solve_U_oc validates only total Q positivity, not every Q_j."},
        {"id": "P2-43-003", "summary": "equilibrium does not validate V or callable Cbg output finiteness."},
        {"id": "P2-43-004", "summary": "Low-level helpers and transition inputs lack uniform finite/range guards."},
        {"id": "P2-43-005", "summary": "Fit optimizer fallback hides import diagnostics and optimizer success."},
        {"id": "P2-43-006", "summary": "Fit plot failure is warning-only."},
        {"id": "P2-43-007", "summary": "Graph manual simple helper omits vib terms."},
        {"id": "P2-43-008", "summary": "Regression capture is mutating and must remain disposable."},
        {"id": "P2-43-009", "summary": "Step 42 SEM-002 incorrectly records chi_split=x instead of chi fallback and func_chi_d default."},
        {"id": "P2-43-010", "summary": "Step 42 SEM-006 records seed 20250718 while source uses 20260713."},
        {"id": "P2-43-011", "summary": "LCO electronic opt-in fields lack an explicit schema/range guard."},
        {"id": "P2-43-012", "summary": "theta_E_Tref is finite-checked but not required positive."},
        {"id": "P2-43-013", "summary": "Code-map name correspondence alone cannot establish direct reachability or scientific identity."},
    ],
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_fingerprint(value: Any) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8"))


def git_bytes(*args: str) -> bytes:
    proc = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout


def blob(path: str) -> bytes:
    return git_bytes("cat-file", "blob", f"{SOURCE_COMMIT}:{path}")


def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def strict_load(path: str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate key {key} in {path}")
            out[key] = value
        return out
    return json.loads((ROOT / path).read_text(encoding="utf-8"), object_pairs_hook=hook,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"nonfinite {value}")))


def line_anchor(path: str, start: int, end: int, kind: str, topology_records: list[dict[str, Any]]) -> dict[str, Any]:
    raw = blob(path)
    lines = raw.decode("utf-8-sig").splitlines()
    if not (1 <= start <= end <= len(lines)):
        raise ValueError(f"invalid anchor {path}:{start}-{end}/{len(lines)}")
    overlap = [x["anchor_id"] for x in topology_records
               if x["path"] == path and x["line_start"] <= end and x["line_end"] >= start]
    return {
        "anchor_id": f"{kind}:{path}:{start}-{end}",
        "path": path,
        "git_blob_sha1": blob_sha1(raw),
        "start_line": start,
        "end_line": end,
        "slice_sha256": sha256_bytes("\n".join(lines[start - 1:end]).encode("utf-8")),
        "topology_anchor_ids": overlap,
        "authority_boundary": AUTH_LEXICAL if kind == "DOC" else AUTH_CODE,
    }


def call_name(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:
        return type(node).__name__


def ast_index(path: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    raw = blob(path)
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()
    tree = ast.parse(text, filename=path)
    definitions: list[dict[str, Any]] = []
    calls: list[dict[str, Any]] = []
    stack: list[str] = []
    ordinal = 0

    class Visitor(ast.NodeVisitor):
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            name = ".".join(stack + [node.name])
            definitions.append(make_def(node, name, "class"))
            stack.append(node.name)
            self.generic_visit(node)
            stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            name = ".".join(stack + [node.name])
            if stack and stack[-1] == "solve_U_oc" and node.name == "_charge":
                name = "GraphiteAnodeDischargeDQDV.solve_U_oc.<local>._charge"
            definitions.append(make_def(node, name, "function"))
            stack.append(node.name)
            self.generic_visit(node)
            stack.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_Call(self, node: ast.Call) -> None:
            nonlocal ordinal
            ordinal += 1
            caller = ".".join(stack) if stack else "<module>"
            if stack == ["GraphiteAnodeDischargeDQDV", "solve_U_oc", "_charge"]:
                caller = "GraphiteAnodeDischargeDQDV.solve_U_oc.<local>._charge"
            calls.append({
                "edge_id": f"EDGE:{path}:{node.lineno}:{node.col_offset}:{ordinal:04d}",
                "path": path,
                "git_blob_sha1": blob_sha1(raw),
                "caller": caller,
                "callee": call_name(node.func),
                "line": node.lineno,
                "col_offset": node.col_offset,
                "ordinal": ordinal,
                "ast_sha256": sha256_bytes(ast.dump(node, include_attributes=False).encode("utf-8")),
                "authority_boundary": AUTH_CODE,
            })
            self.generic_visit(node)

    def make_def(node: ast.AST, name: str, kind: str) -> dict[str, Any]:
        start = node.lineno
        end = node.end_lineno
        return {
            "definition_id": f"DEF:{path}:{name}:{start}-{end}",
            "path": path,
            "git_blob_sha1": blob_sha1(raw),
            "qualified_name": name,
            "kind": kind,
            "start_line": start,
            "end_line": end,
            "slice_sha256": sha256_bytes("\n".join(lines[start - 1:end]).encode("utf-8")),
            "public_entry": not name.split(".")[-1].startswith("_"),
            "authority_boundary": AUTH_CODE,
        }

    Visitor().visit(tree)
    definitions.sort(key=lambda x: (x["start_line"], x["end_line"], x["qualified_name"]))
    calls.sort(key=lambda x: (x["line"], x["col_offset"], x["ordinal"]))
    return definitions, calls


def resolve_edge(all_edges: list[dict[str, Any]], caller: str, callee: str, line: int) -> dict[str, Any]:
    matches = [x for x in all_edges if x["path"] == MAIN_CODE and x["caller"] == caller and x["callee"] == callee and x["line"] == line]
    if len(matches) != 1:
        raise ValueError(f"edge resolution {caller}->{callee}@{line}: {len(matches)}")
    return matches[0]


def resolve_local_callee(caller: str, callee: str, def_by_name: dict[str, dict[str, Any]]) -> str:
    if callee in def_by_name:
        return callee
    if callee == "_charge" and caller == "GraphiteAnodeDischargeDQDV.solve_U_oc":
        return "GraphiteAnodeDischargeDQDV.solve_U_oc.<local>._charge"
    if callee.startswith("self."):
        class_name = caller.split(".", 1)[0]
        candidate = f"{class_name}.{callee[5:]}"
        if candidate in def_by_name:
            return candidate
        inherited = f"GraphiteAnodeDischargeDQDV.{callee[5:]}"
        if inherited in def_by_name:
            return inherited
    raise ValueError(f"local call target unresolved: {caller}->{callee}")


def make_call_paths(trace_id: str, all_edges: list[dict[str, Any]],
                    def_by_name: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    paths: list[dict[str, Any]] = []
    for path_number, path_spec in enumerate(CHAIN_PATHS.get(trace_id, []), 1):
        resolved_edges = [resolve_edge(all_edges, *edge_spec) for edge_spec in path_spec]
        definition_names = [resolved_edges[0]["caller"]]
        dynamic_dispatch = False
        for edge_number, edge in enumerate(resolved_edges, 1):
            override = DYNAMIC_TARGET_OVERRIDES.get((trace_id, path_number, edge_number))
            target = override or resolve_local_callee(edge["caller"], edge["callee"], def_by_name)
            dynamic_dispatch = dynamic_dispatch or override is not None
            if edge_number < len(resolved_edges) and target != resolved_edges[edge_number]["caller"]:
                raise ValueError(
                    f"noncontiguous call path {trace_id} path {path_number}: "
                    f"{target} != {resolved_edges[edge_number]['caller']}"
                )
            definition_names.append(target)
        missing = [name for name in definition_names if name not in def_by_name]
        if missing:
            raise ValueError(f"call path definition anchors missing for {trace_id}: {missing}")
        paths.append({
            "path_id": f"{trace_id}:PATH-{path_number:02d}",
            "edge_ids": [edge["edge_id"] for edge in resolved_edges],
            "definition_chain_ids": [def_by_name[name]["definition_id"] for name in definition_names],
            "definition_chain_names": definition_names,
            "path_disposition": (
                "ORDERED_CONTIGUOUS_DYNAMIC_DISPATCH_PATH" if dynamic_dispatch
                else "ORDERED_CONTIGUOUS_LOCAL_CALL_PATH"
            ),
            "authority_boundary": AUTH_CODE,
        })
    return paths


def is_weak_gate(gate_text: str) -> bool:
    return any(token in gate_text for token in ("PRINT_ONLY", "FINITE_LOG_ONLY", "NO_EXIT_GATE", "SUBSET"))


def source_anchor(path: str, start: int, end: int) -> dict[str, Any]:
    raw = blob(path)
    lines = raw.decode("utf-8-sig").splitlines()
    if not (1 <= start <= end <= len(lines)):
        raise ValueError(f"invalid source anchor {path}:{start}-{end}/{len(lines)}")
    return {
        "path": path,
        "git_blob_sha1": blob_sha1(raw),
        "start_line": start,
        "end_line": end,
        "slice_sha256": sha256_bytes("\n".join(lines[start - 1:end]).encode("utf-8")),
        "authority_boundary": AUTH_LEXICAL if path.endswith(".tex") else AUTH_CODE,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    topology = strict_load(TOPOLOGY)
    runtime = strict_load(RUNTIME)
    artifact = strict_load(ARTIFACT)
    records = topology["content_index"]["records"]

    definitions: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    for path in CODE_PATHS:
        defs, calls = ast_index(path)
        definitions.extend(defs)
        edges.extend(calls)
    def_by_name = {x["qualified_name"]: x for x in definitions if x["path"] == MAIN_CODE}
    runtime_gate_by_id = {x["id"]: x for x in runtime["claim_gate_index"]}

    doc_obligations: list[dict[str, Any]] = []
    trace_rows: list[dict[str, Any]] = []
    load_bearing_topology_ids: set[str] = set()
    for spec in CLAIMS:
        theory = [line_anchor(path, start, end, "DOC", records) for path, start, end in spec["anchors"]]
        for anchor in theory:
            load_bearing_topology_ids.update(anchor["topology_anchor_ids"])
        impl = []
        for symbol in spec["symbols"]:
            item = def_by_name.get(symbol)
            if item is None:
                raise ValueError(f"missing definition for {symbol}")
            impl.append({k: item[k] for k in item})
        call_paths = make_call_paths(spec["trace_id"], edges, def_by_name)
        direct_nonmissing = spec["relation"] == "DIRECT" and spec["implementation_disposition"] != "MISSING"
        if direct_nonmissing and not call_paths:
            raise ValueError(f"DIRECT trace lacks a call path: {spec['trace_id']}")
        path_definition_ids = {
            definition_id for path in call_paths for definition_id in path["definition_chain_ids"]
        }
        impl_by_id = {item["definition_id"]: item for item in impl}
        for definition_id in path_definition_ids:
            item = next(x for x in definitions if x["definition_id"] == definition_id)
            impl_by_id[definition_id] = item
        impl = sorted(impl_by_id.values(), key=lambda x: (x["start_line"], x["end_line"], x["qualified_name"]))
        assertion_gate_ids = [
            gate_id for gate_id in spec["gates"]
            if gate_id in runtime_gate_by_id and not is_weak_gate(runtime_gate_by_id[gate_id]["gate"])
        ]
        if spec["status"] == "ALIGNED" and not assertion_gate_ids:
            raise ValueError(f"ALIGNED trace lacks a source-enforced assertion: {spec['trace_id']}")
        unit_statement, sign_statement = BOUNDARY_STATEMENTS[spec["trace_id"]]
        doc_obligations.append({
            "claim_id": spec["claim_id"],
            "trace_id": spec["trace_id"],
            "focus_family": spec["focus_family"],
            "topic": spec["topic"],
            "summary": spec["summary"],
            "theory_anchors": theory,
            "authority_boundary": AUTH_LEXICAL,
        })
        trace_rows.append({
            "trace_id": spec["trace_id"],
            "claim_id": spec["claim_id"],
            "focus_family": spec["focus_family"],
            "topic": spec["topic"],
            "theory_anchor_ids": [x["anchor_id"] for x in theory],
            "implementation_definition_ids": [x["definition_id"] for x in impl],
            "call_paths": call_paths,
            "test_gate_ids": spec["gates"],
            "assertion_gate_ids": assertion_gate_ids,
            "artifact_consumer_ids": spec["consumers"],
            "relation": spec["relation"],
            "status": spec["status"],
            "implementation_disposition": spec["implementation_disposition"],
            "execution_state": spec["execution_state"],
            "reachability": (
                "CONDITIONALLY_REACHABLE_DEFAULT_DORMANT" if call_paths and spec["execution_state"] == "DORMANT_BY_DEFAULT"
                else "ACTIVE" if call_paths
                else "NOT_REQUIRED_RELATED" if spec["relation"] != "DIRECT"
                else "NO_CHAIN_IMPLEMENTATION_ABSENT"
            ),
            "unit_check": {
                "status": spec["unit"],
                "statement": unit_statement,
                "document_anchor_ids": [x["anchor_id"] for x in theory],
                "implementation_definition_ids": [x["definition_id"] for x in impl],
                "assertion_gate_ids": assertion_gate_ids,
            },
            "sign_check": {
                "status": spec["sign"],
                "polarity": spec["polarity"],
                "statement": sign_statement,
                "document_anchor_ids": [x["anchor_id"] for x in theory],
                "implementation_definition_ids": [x["definition_id"] for x in impl],
                "assertion_gate_ids": assertion_gate_ids,
            },
            "test_evidence_disposition": spec["test_disposition"],
            "scientific_truth": "DEFERRED_TO_STEP44_AND_PHASE071",
            "authority_boundary": AUTH_TRACE,
        })

    candidates = [x for x in records if x["kind"] in CANDIDATE_KINDS]
    candidate_dispositions = [{
        "anchor_id": x["anchor_id"],
        "path": x["path"],
        "line_start": x["line_start"],
        "line_end": x["line_end"],
        "kind": x["kind"],
        "text_sha256": x["text_sha256"],
        "disposition": "OVERLAPS_CURATED_OBLIGATION_ANCHOR" if x["anchor_id"] in load_bearing_topology_ids else "SUPPORTING_OR_OUTSIDE_STEP43_CURATED_SCOPE",
        "trace_ids": [row["trace_id"] for row, doc in zip(trace_rows, doc_obligations)
                      if x["anchor_id"] in {aid for anchor in doc["theory_anchors"] for aid in anchor["topology_anchor_ids"]}],
        "authority_boundary": AUTH_LEXICAL,
    } for x in candidates]

    production_defs = [x for x in definitions if x["path"] == MAIN_CODE and x["public_entry"] and x["start_line"] <= 934]
    support_defs = [x for x in definitions if x["public_entry"] and x["path"] != MAIN_CODE]
    public_entries = []
    for item in production_defs + support_defs:
        scope = "PRODUCTION" if item in production_defs else "SUPPORT_SCRIPT"
        traces = PRODUCTION_TRACE_MAP.get(item["qualified_name"], []) if scope == "PRODUCTION" else []
        public_entries.append({
            "definition_id": item["definition_id"],
            "path": item["path"],
            "qualified_name": item["qualified_name"],
            "lines": [item["start_line"], item["end_line"]],
            "entry_scope": scope,
            "trace_ids": traces,
            "exclusion_reason": None if scope == "PRODUCTION" else "lexical helper in executable test/demo/graph script; not production API",
            "authority_boundary": AUTH_CODE if scope == "PRODUCTION" else AUTH_TEST,
        })

    gates = []
    for item in runtime["claim_gate_index"]:
        raw = blob(item["path"])
        lines = raw.decode("utf-8-sig").splitlines()
        start, end = item["lines"]
        gates.append({
            "gate_id": item["id"],
            "path": item["path"],
            "git_blob_sha1": blob_sha1(raw),
            "start_line": start,
            "end_line": end,
            "slice_sha256": sha256_bytes("\n".join(lines[start - 1:end]).encode("utf-8")),
            "gate_semantics": item["gate"],
            "claim_type": item["claim_type"],
            "enforcement": "WEAK_OR_PRINT_ONLY" if is_weak_gate(item["gate"]) else "SOURCE_ENFORCED_OR_BOUNDED_RUNTIME_GATE",
            "authority_boundary": AUTH_TEST,
        })

    consumers = []
    consumer_name_map = {
        "Claude/docs/v1.0.19/graphite_ica_ch1_v1.0.19.pdf": "ART-PDF-CH1",
        "Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.pdf": "ART-PDF-CH2",
        "Claude/docs/v1.0.19/appendix_phase_separation.pdf": "ART-PDF-APPENDIX",
        "Claude/docs/v1.0.19/figs/graph_suite_v1019.png": "ART-GRAPH",
        "Claude/docs/v1.0.19/samples/fig_fit_roundtrip.png": "ART-FIT",
        "Claude/docs/v1.0.19/figs/P4_lco_heat_validation.png": "ART-LCO-HEAT",
        "Claude/docs/v1.0.19/samples/fig_vib_einstein.png": "ART-VIB",
    }
    generator_anchor_map = {
        "Claude/docs/v1.0.19/graphite_ica_ch1_v1.0.19.pdf": ("Claude/docs/v1.0.19/graphite_ica_ch1_v1.0.19.tex", 1, 43),
        "Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.pdf": ("Claude/docs/v1.0.19/graphite_ica_ch2_v1.0.19.tex", 1, 37),
        "Claude/docs/v1.0.19/appendix_phase_separation.pdf": ("Claude/docs/v1.0.19/appendix_phase_separation.tex", 1, 497),
        "Claude/docs/v1.0.19/figs/P4_lco_heat_validation.png": ("Claude/docs/v1.0.18.2/demo_lco_heat.py", 70, 71),
        "Claude/docs/v1.0.19/figs/anode_fit_v1_0_14_dqdv.png": ("Claude/docs/v1.0.16/plot_dqdv.py", 121, 122),
        "Claude/docs/v1.0.19/figs/graph_suite_v1015.png": ("Claude/docs/v1.0.15/graph_suite_v1015.py", 37, 135),
        "Claude/docs/v1.0.19/figs/graph_suite_v1016.png": ("Claude/docs/v1.0.16/graph_suite_v1016.py", 37, 135),
        "Claude/docs/v1.0.19/figs/graph_suite_v1019.png": ("Claude/docs/v1.0.19/graph_suite_v1019.py", 36, 139),
        "Claude/docs/v1.0.19/samples/fig_fit_roundtrip.png": ("Claude/docs/v1.0.19/fit_roundtrip_demo.py", 49, 363),
    }
    for item in artifact["pdfs"] + artifact["images"]:
        generator = generator_anchor_map.get(item["path"])
        source_record = item.get("generator") or item.get("provenance") or {}
        is_tex_source = source_record.get("status") == "DIRECT_TEX_SOURCE"
        consumers.append({
            "consumer_id": consumer_name_map.get(item["path"], "ART-STORED-" + sha256_bytes(item["path"].encode())[:12]),
            "artifact_path": item["path"],
            "artifact_kind": "PDF" if item in artifact["pdfs"] else "IMAGE",
            "git_blob_sha1": item["git_blob_sha1"],
            "sha256": item["sha256"],
            "ground_status": source_record.get("status", "STORED_WITNESS"),
            "consumer_source_anchors": [source_anchor(*generator)] if generator else [],
            "consumer_anchor_disposition": (
                "EXACT_FROZEN_TEX_SOURCE_ANCHOR" if is_tex_source
                else "EXACT_FROZEN_GENERATOR_ANCHOR" if generator
                else "NO_FROZEN_GENERATOR_GROUND"
            ),
            "authority_boundary": AUTH_ARTIFACT,
        })
    golden = runtime["golden_npz"]
    consumers.append({
        "consumer_id": "ART-GOLDEN",
        "artifact_path": golden["path"],
        "artifact_kind": "NPZ",
        "git_blob_sha1": golden["git_blob_sha1"],
        "sha256": golden["sha256"],
        "ground_status": "INTERNAL_REGRESSION_WITNESS",
        "consumer_source_anchors": [source_anchor("Claude/docs/v1.0.19/test_regression_v1019.py", 79, 123)],
        "consumer_anchor_disposition": "EXACT_FROZEN_CONSUMER_AND_CAPTURE_ANCHOR",
        "authority_boundary": AUTH_ARTIFACT,
    })
    consumers.sort(key=lambda x: x["consumer_id"])

    optional = [{"group_id": f"OPTGRP-{i:03d}", "label": name,
                 "member_names": OPTIONAL_MEMBERS.get(name, [name]), "acceptance": acceptance,
                 "runtime_disposition": disposition, "evidence": evidence,
                 "authority_boundary": AUTH_CODE}
                for i, (name, acceptance, disposition, evidence) in enumerate(OPTIONAL_INPUTS, 1)]

    contradictions = [
        {"contradiction_id": "CTR-43-001", "trace_ids": ["TRC-CH2-DOC-LEADS-BOUNDARY"], "disposition": "PRESERVED_AS_PROSPECTIVE_REQUIREMENT_AND_INDEPENDENTLY_TESTED_IMPLEMENTATION", "gate": "RESOLVED_WITH_AUTHORITY_BOUNDARY", "authority_boundary": AUTH_TRACE},
        {"contradiction_id": "CTR-43-002", "trace_ids": ["TRC-CH2-COMPLETE-SYNTHESIS", "TRC-CH2-WIDTH-T-DEPENDENCE"], "disposition": "N_OR_DWDT_IS_REQUIRED_STATE_NOT_LISTED_IN_SHORT_INPUT_SET", "gate": "OPEN_P1", "authority_boundary": AUTH_TRACE},
        {"contradiction_id": "CTR-43-003", "trace_ids": ["TRC-CH1-LOW-CURRENT-HYS-LIMIT", "TRC-CH1-REVERSIBLE-BASELINE"], "disposition": "DISTINCT_PHYSICAL_LIMIT_AND_DIAGNOSTIC_BASELINE_ROWS", "gate": "RESOLVED_BY_SPLIT", "authority_boundary": AUTH_TRACE},
        {"contradiction_id": "CTR-43-004", "trace_ids": [], "disposition": "STEP42_DEFINITION_BODY_GRAPH_444_REPLACED_BY_STEP43_FULL_AST_882", "gate": "CORRECTED_EVIDENCE_SCOPE", "authority_boundary": AUTH_TRACE},
        {"contradiction_id": "CTR-43-005", "trace_ids": ["TRC-CH1-LAG-LENGTH"], "disposition": "STEP42_SEM002_DEFAULT_TEXT_CORRECTED_TO_CHI_FALLBACK_AND_FUNC_CHI_D", "gate": "CORRECTED_SEMANTIC_RECORD", "authority_boundary": AUTH_TRACE},
        {"contradiction_id": "CTR-43-006", "trace_ids": [], "disposition": "STEP42_SEM006_SEED_CORRECTED_FROM_20250718_TO_SOURCE_20260713", "gate": "CORRECTED_SEMANTIC_RECORD", "authority_boundary": AUTH_TRACE},
    ]

    input_paths = [TOPOLOGY, ATTESTATION, PROCESS, RUNTIME, ARTIFACT]
    input_evidence = [{
        "evidence_id": f"INPUT-{i:02d}", "path": path,
        "sha256": sha256_bytes((ROOT / path).read_bytes()),
        "size_bytes": (ROOT / path).stat().st_size,
        "authority_boundary": AUTH_TRACE,
    } for i, path in enumerate(input_paths, 1)]

    matrix: dict[str, Any] = {
        "schema_version": 2,
        "phase": 60,
        "step": 43,
        "source_commit": SOURCE_COMMIT,
        "generation": {"builder": "Codex/work/v1019_phase060/build_phase060_step43_doc_code_trace.py", "ordering": "stable source/line/id order", "json": "UTF-8 strict finite deterministic", "authority_boundary": AUTH_TRACE},
        "authority_policy": {"document": AUTH_LEXICAL, "implementation": AUTH_CODE, "test": AUTH_TEST, "artifact": AUTH_ARTIFACT, "trace": AUTH_TRACE, "scientific_truth": "DEFERRED_TO_STEP44_AND_PHASE071"},
        "enumerations": {
            "relation": ["DIRECT", "RELATED_NOT_DIRECT", "NOT_APPLICABLE"],
            "status": ["ALIGNED", "PARTIAL", "MISALIGNED", "ABSENT", "UNVERIFIED"],
            "implementation_disposition": ["IMPLEMENTED", "PARTIAL", "MISSING", "NOT_REQUIRED", "UNVERIFIED"],
            "candidate_disposition": ["OVERLAPS_CURATED_OBLIGATION_ANCHOR", "SUPPORTING_OR_OUTSIDE_STEP43_CURATED_SCOPE"],
            "reachability": ["ACTIVE", "CONDITIONALLY_REACHABLE_DEFAULT_DORMANT", "NOT_REQUIRED_RELATED", "NO_CHAIN_IMPLEMENTATION_ABSENT"],
            "execution_state": ["ACTIVE", "DORMANT_BY_DEFAULT"],
            "consumer_anchor_disposition": ["EXACT_FROZEN_TEX_SOURCE_ANCHOR", "EXACT_FROZEN_GENERATOR_ANCHOR", "EXACT_FROZEN_CONSUMER_AND_CAPTURE_ANCHOR", "NO_FROZEN_GENERATOR_GROUND"],
        },
        "input_evidence": input_evidence,
        "candidate_dispositions": candidate_dispositions,
        "document_obligations": doc_obligations,
        "public_entry_obligations": public_entries,
        "implementation_definitions": definitions,
        "call_edge_index": edges,
        "test_gate_index": gates,
        "artifact_consumer_index": consumers,
        "optional_input_disposition_groups": optional,
        "trace_rows": trace_rows,
        "contradiction_routes": contradictions,
        "findings": FINDINGS,
        "fingerprints": {},
        "gate_summary": {},
    }
    matrix["fingerprints"] = {
        "candidate_dispositions": canonical_fingerprint(candidate_dispositions),
        "document_obligations": canonical_fingerprint(doc_obligations),
        "public_entry_obligations": canonical_fingerprint(public_entries),
        "implementation_definitions": canonical_fingerprint(definitions),
        "call_edge_index": canonical_fingerprint(edges),
        "test_gate_index": canonical_fingerprint(gates),
        "artifact_consumer_index": canonical_fingerprint(consumers),
        "optional_input_disposition_groups": canonical_fingerprint(optional),
        "trace_rows": canonical_fingerprint(trace_rows),
        "contradiction_routes": canonical_fingerprint(contradictions),
        "findings": canonical_fingerprint(FINDINGS),
    }
    production_orphans = [x["qualified_name"] for x in public_entries if x["entry_scope"] == "PRODUCTION" and not x["trace_ids"]]
    used_families = {x["focus_family"] for x in trace_rows}
    matrix["gate_summary"] = {
        "candidate_records": len(candidate_dispositions),
        "candidate_disposition_orphan_count": sum(1 for x in candidate_dispositions if not x["disposition"]),
        "curated_overlap_anchor_records": sum(1 for x in candidate_dispositions if x["disposition"] == "OVERLAPS_CURATED_OBLIGATION_ANCHOR"),
        "curated_document_obligations": len(doc_obligations),
        "curated_doc_row_orphan_count": sum(1 for x in doc_obligations if not x["trace_id"]),
        "focus_families_required": len(FOCUS_FAMILIES),
        "focus_family_missing_count": len(set(FOCUS_FAMILIES) - used_families),
        "definitions_full_ast": len(definitions),
        "call_nodes_full_ast": len(edges),
        "step42_definition_records": runtime["code_summary"]["definitions"],
        "step42_definition_body_call_edges": runtime["code_summary"]["call_edges"],
        "public_entries_all": len(public_entries),
        "production_public_entries": len(production_defs),
        "support_public_entries": len(support_defs),
        "public_call_orphan_count": len(production_orphans),
        "source_gates": len(gates),
        "python_assert_nodes": 0,
        "artifact_consumers": len(consumers),
        "optional_disposition_groups": len(optional),
        "optional_member_names": len({member for group in optional for member in group["member_names"]}),
        "invalid_anchor_count": 0,
        "missing_authority_boundary_count": 0,
        "P0": len(FINDINGS["P0"]),
        "P1": len(FINDINGS["P1"]),
        "P2": len(FINDINGS["P2"]),
        "gate_result": "PASS_WITH_CONCERNS",
    }

    payload = json.dumps(matrix, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload, encoding="utf-8", newline="\n")
    print(f"WROTE {output.relative_to(ROOT) if output.is_relative_to(ROOT) else output}")
    print(f"COUNTS candidates={len(candidate_dispositions)} curated_claims={len(trace_rows)} production={len(production_defs)} support={len(support_defs)} definitions={len(definitions)} calls={len(edges)} gates={len(gates)} consumers={len(consumers)} optional_groups={len(optional)}")
    print(f"FINDINGS P0={len(FINDINGS['P0'])} P1={len(FINDINGS['P1'])} P2={len(FINDINGS['P2'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
