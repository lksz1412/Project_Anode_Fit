#!/usr/bin/env python3
"""Build Phase 062 Step 54 LCO/Si literature, unit, and scope evidence.

Only frozen Git objects are read.  The external metadata and proposition checks
are dated observations embedded by the auditor; this builder performs no
network access and does not import or execute the historical production module.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_JSON = ROOT / "Codex/results/PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json"
OUTPUT_MD = ROOT / "Codex/results/PHASE_062_STEP_054_LCO_SI_SCOPE_RESULT.md"

BASELINE = "3b5fd059ed09cdcdde38668c399cb35b8afbcca9"
Q6_COMMIT = "bab65b7290204ec5d64b1c2bbdfb4b30d4c8fd17"
Q6_PARENT = "7316e7915db8727f794614b61f98d4df7f803bfd"
Q7_COMMIT = "9ea5cb23754061261923bab013e279d7f6938723"
Q7_PARENT = Q6_COMMIT
EXPECTED_PARENT = "9dee2f4d6bdde48f248227cdede08d0d307cc8bc"
CHECKED_DATE = "2026-08-27"

R = 8.314
F = 96485.0
KB = 1.380649e-23
EV_TO_J = 1.602176634e-19
T_REF = 298.15

SOURCE_SPECS = [
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_sec11_lcointro.tex", 172, "49233bc845a9e3b810a180f04e270ee467a7a2b0", "0a904e4327bb906de24b517d1ea2b6f3f7b3affcdfd110da3fded3accb13081f"),
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_sec12_lcocenter.tex", 112, "db3bef0185161b51263b8fa0afc6ddc1cf71c62e", "7fd8be513e94cc6c29fa948efc543266bc7dcc3ddb6a7929cb4a8e36d95b2590"),
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_sec13_lcohys.tex", 176, "f49eb5ac3a7e5b23d0852c37c0af4c24ba6da28b", "4e875cd96cbf64a8a7a68505f8c4590fb00dc6b5892c8a0184a2f732221846e5"),
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_sec14_lcodecomp.tex", 105, "f1ec204c1a989ef1b402a84d1cedaafc956b80ec", "10339857f910231823aa6e2b2634f424ef91792d35ed8a815f9174240866f1f9"),
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_sec15_lcoelec.tex", 346, "aabf8002bad41b3f9267dabc1a1def7af900e791", "d312c4b0d1d4b3be20f6b597b5fc197495db08ab3c1f65376271526e97f44c42"),
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_sec16_lcopeak.tex", 68, "742a1ccd58fb334856373d978ccfdee781b2f544", "5af91d815c246f90a8f44cc95000bf8e1ad639c8478e9b3d6257b6c6a454f7cf"),
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_sec17_msmr.tex", 136, "1289d703644e3a69b8801612e351fbc29c63bb8d", "db3637fb03f0f78e8929defec3c752f5ed543634607027b0b9cd97804db4907c"),
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_sec18_inputs.tex", 68, "d7704dde7a396620c0ea968b57a9c567591e1ef9", "e8b762409420960e04c2083816228836311291a3cd4c906fc659eeb591d782a2"),
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_appA_signcheck.tex", 89, "5b9257da753de0dc9ba2ff0829d399281059f999", "83623700efc8d8ed0b7b09d31ed29fd9b3e875d2229d0755d401e94222a66fb3"),
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_appC_navaid.tex", 142, "430aef2a795e3ae59d27752061ae0846c290bd34", "335242dcaab2cfd6510e6a2832e359bb90b9f064c0f456b2f2792b7eabbb4a4a"),
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_appD_si.tex", 91, "c658d67d6e06f0325f6165ff8f08e6eda749b6ef", "f5117b0eeab184c25466d814cc94fe93509eb1f0496e6dc649994f8a2c91f90a"),
    (BASELINE, "Claude/docs/v1.0.21/_sections/ch1_bib.tex", 64, "dc4ca0780618d5710fd04e74ea87707738ffceba", "dc58338a8abd45116d846c0053ed41265d45b0f37852fafe93b8ecd7488d651d"),
    (BASELINE, "Claude/docs/v1.0.21/Anode_Fit_v1.0.21.py", 1152, "7588fe782a027511c2407d9b7caea6ef0ca6c3bd", "d50612413f9f956486594ddafde37776f9592b75e2c8a2266927eaaa23267eaf"),
    (BASELINE, "Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md", 37, "64bdca8830a491e10d45c30fe9d992bb334afe03", "a61856800cf5fa0247ef794c559337ff6c48f1801105ef13647ce625edd2b838"),
    (BASELINE, "Claude/docs/v1.0.21/results/V1021_CHANGE_LOG.md", 37, "2d23088e094d93a28b687788b9ac03fa0ab5520c", "b0092e4313ecd228904e865cd93bc00215b7a3740bdc65a3353f05e333f686de"),
    (BASELINE, "Claude/docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md", 19, "ee86e4a8e74dea13cd01dc8fb8de36bb7119bf12", "b67870551a414f991badf85309da31cca208c77cc85b7399badead1fc1048472"),
    (BASELINE, "Claude/docs/v1.0.21/HANDOVER_v1.0.21.md", 24, "3dd6475884808dfee71062e4706bf4993aa5c699", "19c86771fdf9d15199ebb52d8c851af1d83de2c2efdc39671f4068dc15a6908c"),
    (BASELINE, "Claude/docs/v1.0.20/results/DIRECTION_SI_LCO_REPORT.md", 291, "3c5a20f8609b4a2cd1f9ce85d61c302b59180c50", "eb6ea800c5ef14750b09034c849c25ef5fa6d036d9cbb8e0b19205148825cb69"),
    (BASELINE, "Claude/docs/v1.0.21/results/snapshot_v1021_q6.json", 1372, "87b9ebd79c49ed90f2f82fa9c90befc5ce5d9ef0", "640814e0630e5ef72fccdfbd2688a10110d3f75ba74559a34db2601097223e66"),
    (BASELINE, "Claude/docs/v1.0.21/results/snapshot_v1021_q7.json", 1393, "84f227db3fb70eb8607c39158633040ef3d40fd2", "765412e3602c07965c3e1affe17dd1e75776fdcace824325897a377d21585115"),
    (EXPECTED_PARENT, "Codex/results/PHASE_057O_V1021_Q6_Q7_AND_VERSION_CLOSE_OBSERVATIONS.md", 134, "cf1bdccbd96286ea56993ac4b090f09dd224e2df", "872338e86e503cfd1fb693b7ae267993a25a034ce7acfbc9dcabc5e9d9dbb5be"),
]

LCO_KEYS = [
    "reimers1992", "vanderven1998", "mott1968", "imada1998", "marianetti2004",
    "menetrier1999", "motohashi2009", "xia2007", "reynier2004", "swiderska2019",
    "msmr_origin2017", "bakerverbrugge2018", "msmr2024", "ml2024",
]
SI_KEYS = [
    "wen_huggins1981", "limthongkul2003", "li_dahn2007", "obrovac_christensen2004",
    "chevrier_dahn2009", "beaulieu2001", "sethuraman_stressevo2010",
    "sethuraman_stresspot2010", "liu_sizefracture2012", "obrovac_chevrier2014",
    "verbrugge_lisi2016", "jiang_sihys2020", "larchecahn1973", "koebbing2024",
]
LCO_CITE_KEYS = set(LCO_KEYS) | {"ashcroftmermin1976"}

META = {
    "reimers1992": ("10.1149/1.2221184", "Electrochemical and In Situ X-Ray Diffraction Studies of Lithium Intercalation in LixCoO2", "Journal of The Electrochemical Society", "139", "8", "2091-2097", "1992"),
    "vanderven1998": ("10.1103/PhysRevB.58.2975", "First-principles investigation of phase stability in LixCoO2", "Physical Review B", "58", "6", "2975-2987", "1998"),
    "mott1968": ("10.1103/RevModPhys.40.677", "Metal-Insulator Transition", "Reviews of Modern Physics", "40", "4", "677-683", "1968"),
    "imada1998": ("10.1103/RevModPhys.70.1039", "Metal-insulator transitions", "Reviews of Modern Physics", "70", "4", "1039-1263", "1998"),
    "marianetti2004": ("10.1038/nmat1178", "A first-order Mott transition in LixCoO2", "Nature Materials", "3", "9", "627-631", "2004"),
    "menetrier1999": ("10.1039/a900016j", "The insulator-metal transition upon lithium deintercalation from LiCoO2", "Journal of Materials Chemistry", "9", "5", "1135-1140", "1999"),
    "motohashi2009": ("10.1103/PhysRevB.80.165114", "Electronic phase diagram of the layered cobalt oxide system LixCoO2", "Physical Review B", "80", "16", "165114", "2009"),
    "xia2007": ("10.1149/1.2509021", "Phase Transitions and High-Voltage Electrochemical Behavior of LiCoO2 Thin Films", "Journal of The Electrochemical Society", "154", "4", "A337-A342", "2007"),
    "reynier2004": ("10.1103/PhysRevB.70.174304", "Entropy of Li intercalation in LixCoO2", "Physical Review B", "70", "17", "174304", "2004"),
    "swiderska2019": ("10.1039/c8cp06638h", "Temperature coefficients of Li-ion battery single electrode potentials and related entropy changes - revisited", "Physical Chemistry Chemical Physics", "21", "4", "2115-2120", "2019"),
    "msmr_origin2017": ("10.1149/2.0341708jes", "Thermodynamic Model for Substitutional Materials", "Journal of The Electrochemical Society", "164", "11", "E3243-E3253", "2017"),
    "bakerverbrugge2018": ("10.1149/2.0771816jes", "Multi-Species, Multi-Reaction Model for Porous Intercalation Electrodes: Part I", "Journal of The Electrochemical Society", "165", "16", "A3952-A3964", "2018"),
    "msmr2024": ("10.1149/2754-2734/ad7d1c", "Quantifying the Temperature Dependence of the Multi-Species, Multi-Reaction Model. Part 1", "ECS Advances", "3", "4", "042501", "2024"),
    "ml2024": ("10.1016/j.jmps.2024.105726", "Bridging scales with Machine Learning to study order-disorder transitions in LixCoO2", "Journal of the Mechanics and Physics of Solids", "190", None, "105726", "2024"),
    "wen_huggins1981": ("10.1016/0022-4596(81)90487-4", "Chemical diffusion in intermediate phases in the lithium-silicon system", "Journal of Solid State Chemistry", "37", "3", "271-278", "1981"),
    "limthongkul2003": ("10.1016/S1359-6454(02)00514-1", "Electrochemically-driven solid-state amorphization in lithium-silicon alloys and implications for lithium storage", "Acta Materialia", "51", "4", "1103-1113", "2003"),
    "li_dahn2007": ("10.1149/1.2409862", "An In Situ X-Ray Diffraction Study of the Reaction of Li with Crystalline Si", "Journal of The Electrochemical Society", "154", "3", "A156-A161", "2007"),
    "obrovac_christensen2004": ("10.1149/1.1652421", "Structural Changes in Silicon Anodes during Lithium Insertion/Extraction", "Electrochemical and Solid-State Letters", "7", "5", "A93-A96", "2004"),
    "chevrier_dahn2009": ("10.1149/1.3111037", "First Principles Model of Amorphous Silicon Lithiation", "Journal of The Electrochemical Society", "156", "6", "A454-A458", "2009"),
    "beaulieu2001": ("10.1149/1.1388178", "Colossal Reversible Volume Changes in Lithium Alloys", "Electrochemical and Solid-State Letters", "4", "9", "A137-A140", "2001"),
    "sethuraman_stressevo2010": ("10.1016/j.jpowsour.2010.02.013", "In situ measurements of stress evolution in silicon thin films", "Journal of Power Sources", "195", "15", "5062-5066", "2010"),
    "sethuraman_stresspot2010": ("10.1149/1.3489378", "In Situ Measurements of Stress-Potential Coupling in Lithiated Silicon", "Journal of The Electrochemical Society", "157", "11", "A1253-A1261", "2010"),
    "liu_sizefracture2012": ("10.1021/nn204476h", "Size-Dependent Fracture of Silicon Nanoparticles During Lithiation", "ACS Nano", "6", "2", "1522-1531", "2012"),
    "obrovac_chevrier2014": ("10.1021/cr500207g", "Alloy Negative Electrodes for Li-Ion Batteries", "Chemical Reviews", "114", "23", "11444-11502", "2014"),
    "verbrugge_lisi2016": ("10.1149/2.0581602jes", "Formulation for the Treatment of Multiple Electrochemical Reactions and Associated Speciation for the Lithium-Silicon Electrode", "Journal of The Electrochemical Society", "163", "2", "A262-A271", "2016"),
    "jiang_sihys2020": ("10.1149/1945-7111/abbbba", "Voltage Hysteresis Model for Silicon Electrodes", "Journal of The Electrochemical Society", "167", "13", "130533", "2020"),
    "larchecahn1973": ("10.1016/0001-6160(73)90021-7", "A linear theory of thermochemical equilibrium of solids under stress", "Acta Metallurgica", "21", "8", "1051-1063", "1973"),
    "koebbing2024": ("10.1002/adfm.202308818", "Voltage Hysteresis of Silicon Nanoparticles: Chemo-Mechanical Particle-SEI Model", "Advanced Functional Materials", "34", "7", "2308818", "2024"),
}

# Ordered, normalized publication bylines and complete authoritative titles.
# These fields are proposition-neutral metadata: they do not promote a paper's
# abstract, landing page, or bibliography entry to full-text support.
AUTHORS = {
    "reimers1992": ["J. N. Reimers", "J. R. Dahn"],
    "vanderven1998": ["A. Van der Ven", "M. K. Aydinol", "G. Ceder", "G. Kresse", "J. Hafner"],
    "mott1968": ["N. F. Mott"],
    "imada1998": ["M. Imada", "A. Fujimori", "Y. Tokura"],
    "marianetti2004": ["C. A. Marianetti", "G. Kotliar", "G. Ceder"],
    "menetrier1999": ["M. Ménétrier", "I. Saadoune", "S. Levasseur", "C. Delmas"],
    "motohashi2009": ["T. Motohashi", "T. Ono", "Y. Sugimoto", "Y. Masubuchi", "S. Kikkawa", "R. Kanno", "M. Karppinen", "H. Yamauchi"],
    "xia2007": ["H. Xia", "L. Lu", "Y. S. Meng", "G. Ceder"],
    "reynier2004": ["Y. Reynier", "J. Graetz", "T. Swan-Wood", "P. Rez", "R. Yazami", "B. Fultz"],
    "swiderska2019": ["A. Świderska-Mocek", "E. Rudnicka", "A. Lewandowski"],
    "msmr_origin2017": ["Mark Verbrugge", "Daniel Baker", "Brian Koch", "Xingcheng Xiao", "Wentian Gu"],
    "bakerverbrugge2018": ["D. R. Baker", "M. W. Verbrugge"],
    "msmr2024": ["A. Paul", "K. Wolfe", "M. W. Verbrugge", "B. J. Koch", "J. S. Lowe", "J. Trembly", "J. A. Staser", "T. R. Garrick"],
    "ml2024": ["M. Faghih Shojaei", "J. Holber", "S. Das", "G. H. Teichert", "T. Mueller", "L. Hung", "V. Gavini", "K. Garikipati"],
    "wen_huggins1981": ["C. J. Wen", "R. A. Huggins"],
    "limthongkul2003": ["P. Limthongkul", "Y.-I. Jang", "N. J. Dudney", "Y.-M. Chiang"],
    "li_dahn2007": ["J. Li", "J. R. Dahn"],
    "obrovac_christensen2004": ["M. N. Obrovac", "L. Christensen"],
    "chevrier_dahn2009": ["V. L. Chevrier", "J. R. Dahn"],
    "beaulieu2001": ["L. Y. Beaulieu", "K. W. Eberman", "R. L. Turner", "L. J. Krause", "J. R. Dahn"],
    "sethuraman_stressevo2010": ["V. A. Sethuraman", "M. J. Chon", "M. Shimshak", "V. Srinivasan", "P. R. Guduru"],
    "sethuraman_stresspot2010": ["V. A. Sethuraman", "V. Srinivasan", "A. F. Bower", "P. R. Guduru"],
    "liu_sizefracture2012": ["X. H. Liu", "L. Zhong", "S. Huang", "S. X. Mao", "T. Zhu", "J. Y. Huang"],
    "obrovac_chevrier2014": ["M. N. Obrovac", "V. L. Chevrier"],
    "verbrugge_lisi2016": ["M. W. Verbrugge", "D. R. Baker", "X. Xiao"],
    "jiang_sihys2020": ["Y. Jiang", "G. Offer", "J. Jiang", "M. Marinescu", "H. Wang"],
    "larchecahn1973": ["F. Larché", "J. W. Cahn"],
    "koebbing2024": ["L. Köbbing", "A. Latz", "B. Horstmann"],
}

FULL_TITLES = {
    "reimers1992": "Electrochemical and in situ X-ray diffraction studies of lithium intercalation in LixCoO2",
    "vanderven1998": "First-principles investigation of phase stability in LixCoO2",
    "mott1968": "Metal-Insulator Transition",
    "imada1998": "Metal-insulator transitions",
    "marianetti2004": "A first-order Mott transition in LixCoO2",
    "menetrier1999": "The insulator-metal transition upon lithium deintercalation from LiCoO2: electronic properties and 7Li NMR study",
    "motohashi2009": "Electronic phase diagram of the layered cobalt oxide system LixCoO2 (0 ≤ x ≤ 1)",
    "xia2007": "Phase transitions and high-voltage electrochemical behavior of LiCoO2 thin films grown by pulsed laser deposition",
    "reynier2004": "Entropy of Li intercalation in LixCoO2",
    "swiderska2019": "Temperature coefficients of Li-ion battery single electrode potentials and related entropy changes—revisited",
    "msmr_origin2017": "Thermodynamic Model for Substitutional Materials: Application to Lithiated Graphite, Spinel Manganese Oxide, Iron Phosphate, and Layered Nickel-Manganese-Cobalt Oxide",
    "bakerverbrugge2018": "Multi-Species, Multi-Reaction Model for Porous Intercalation Electrodes: Part I. Model Formulation and a Perturbation Solution for Low-Scan-Rate, Linear-Sweep Voltammetry",
    "msmr2024": "Quantifying the Temperature Dependence of the Multi-Species, Multi-Reaction Model. Part 1: Parameterization for a Meso-Carbon Micro-Bead Graphite",
    "ml2024": "Bridging scales with Machine Learning: From first principles statistical mechanics to continuum phase field computations to study order-disorder transitions in LixCoO2",
    "wen_huggins1981": "Chemical diffusion in intermediate phases in the lithium-silicon system",
    "limthongkul2003": "Electrochemically-driven solid-state amorphization in lithium-silicon alloys and implications for lithium storage",
    "li_dahn2007": "An In Situ X-Ray Diffraction Study of the Reaction of Li with Crystalline Si",
    "obrovac_christensen2004": "Structural Changes in Silicon Anodes during Lithium Insertion/Extraction",
    "chevrier_dahn2009": "First Principles Model of Amorphous Silicon Lithiation",
    "beaulieu2001": "Colossal Reversible Volume Changes in Lithium Alloys",
    "sethuraman_stressevo2010": "In situ measurements of stress evolution in silicon thin films during electrochemical lithiation and delithiation",
    "sethuraman_stresspot2010": "In Situ Measurements of Stress-Potential Coupling in Lithiated Silicon",
    "liu_sizefracture2012": "Size-Dependent Fracture of Silicon Nanoparticles During Lithiation",
    "obrovac_chevrier2014": "Alloy Negative Electrodes for Li-Ion Batteries",
    "verbrugge_lisi2016": "Formulation for the Treatment of Multiple Electrochemical Reactions and Associated Speciation for the Lithium-Silicon Electrode",
    "jiang_sihys2020": "Voltage Hysteresis Model for Silicon Electrodes for Lithium Ion Batteries, Including Multi-Step Phase Transformations, Crystallization and Amorphization",
    "larchecahn1973": "A linear theory of thermochemical equilibrium of solids under stress",
    "koebbing2024": "Voltage Hysteresis of Silicon Nanoparticles: Chemo-Mechanical Particle-SEI Model",
}

REQUIRED_NEGATIVE_CONTROLS = [
    "BIBLIOGRAPHY_AS_PROPOSITION_PROOF",
    "WEB_METADATA_AS_FULLTEXT",
    "UNIT_BASIS_COLLAPSE",
    "TIER_C_TO_MATERIAL_PROMOTION",
    "PURE_LCO_TO_DOPED_LCO_PROMOTION",
    "SI_BRIDGEHEAD_TO_COMPLETE_MODEL",
    "MISSING_SCOPE_ROUTING",
    "EXTERNAL_AUTHORITY_PROMOTION",
    "STATUS_PROMOTION",
    "METADATA_IDENTITY_TAMPER",
    "CITATION_DENOMINATOR_TAMPER",
    "Q6_NUMERIC_TAMPER",
    "Q7_LABEL_DELTA_TAMPER",
    "GNF_ORPHAN",
    "ANCHOR_SLICE_HASH_TAMPER",
    "SEMANTIC_DIGEST_TAMPER",
    "RESULT_FIRST_CONTRACT_TAMPER",
    "SOURCE_CLAIM_MANIFEST_MISSING",
    "SOURCE_CLAIM_MULTI_MAPPED",
    "STRUCTURAL_AS_CLAIM",
    "TIKZ_LOAD_BEARING_OMISSION",
    "MULTILINE_CLAIM_SPLIT",
    "A_OR_B_TIER_TO_C",
    "UNIT_DELETION",
    "CITEKEY_NUMERIC_LEAK",
    "BIBLIOGRAPHY_IDENTITY_TAMPER",
    "PROVENANCE_IDENTITY_TAMPER",
    "SOURCE_ATTESTATION_SCHEMA_TAMPER",
]

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


def run_git(*args: str, binary: bool = False) -> bytes | str:
    proc = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, timeout=30)
    return proc.stdout if binary else proc.stdout.decode("utf-8", "strict").strip()


def git_bytes(commit: str, path: str) -> bytes:
    return run_git("show", f"{commit}:{path}", binary=True)  # type: ignore[return-value]


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def lf_normalized_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def strict_json(raw: bytes) -> Any:
    def hook(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate key: {key}")
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=hook, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def traversal(value: Any) -> dict[str, int]:
    counts = {"nodes": 0, "mapping_objects": 0, "mapping_keys": 0, "lists": 0, "scalars": 0, "max_depth": 0}
    stack = [(value, 0)]
    while stack:
        item, depth = stack.pop()
        counts["nodes"] += 1
        counts["max_depth"] = max(counts["max_depth"], depth)
        if isinstance(item, dict):
            counts["mapping_objects"] += 1
            counts["mapping_keys"] += len(item)
            stack.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            counts["lists"] += 1
            stack.extend((child, depth + 1) for child in item)
        else:
            counts["scalars"] += 1
            if isinstance(item, float) and not math.isfinite(item):
                raise ValueError("non-finite JSON float")
    return counts


def source_attestations() -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    rows = []
    decoded: dict[str, list[str]] = {}
    for commit, path, expected_lines, expected_blob, expected_sha in SOURCE_SPECS:
        raw = git_bytes(commit, path)
        lines = raw.decode("utf-8", "strict").splitlines()
        blob = run_git("rev-parse", f"{commit}:{path}")
        if len(lines) != expected_lines or blob != expected_blob or sha256(raw) != expected_sha:
            raise RuntimeError(f"frozen source identity drift: {path}")
        decoded[path] = lines
        rows.append({
            "commit": commit, "path": path, "git_blob": blob, "raw_sha256": expected_sha,
            "physical_lines": expected_lines, "read_start": 1, "read_end": expected_lines,
            "read_state": "READ_FULL", "decoding": "UTF-8_STRICT",
        })
    return rows, decoded


def frozen_anchor(
    decoded: dict[str, list[str]], path: str, start: int, end: int,
    anchor_state: str = "PRESENT_IN_ADOPTED_RELEASE_TEXT",
) -> dict[str, Any]:
    lines = decoded[path]
    if start < 1 or end < start or end > len(lines):
        raise RuntimeError(f"invalid frozen anchor: {path}:{start}-{end}")
    text = "\n".join(lines[start - 1:end])
    raw = (text + "\n").encode("utf-8")
    return {
        "commit": BASELINE,
        "path": path,
        "line_start": start,
        "line_end": end,
        "anchor_text": text,
        "slice_sha256": sha256(raw),
        "anchor_state": anchor_state,
    }


def reference_ledger_inventory(decoded: dict[str, list[str]]) -> dict[str, Any]:
    path = "Claude/docs/v1.0.21/results/V1021_REFERENCE_LEDGER.md"
    specs = [
        ("P062-LEDGER-0001", 1, 4, "citation-key policy and inherited-ledger claim"),
        ("P062-LEDGER-0002", 6, 10, "inherited reference summary"),
        ("P062-LEDGER-0003", 12, 13, "Q2/Q3 existing-key sufficiency self-report"),
        ("P062-LEDGER-0004", 22, 37, "Q7 Si reference registration and residual debt self-report"),
    ]
    rows = []
    for ledger_id, start, end, statement_scope in specs:
        rows.append({
            "ledger_statement_id": ledger_id,
            "authority_class": "REFERENCE_LEDGER_SELF_REPORT",
            "statement_scope": statement_scope,
            "proposition_authority": False,
            "anchor": frozen_anchor(
                decoded, path, start, end,
                "PRESENT_IN_REFERENCE_LEDGER_SELF_REPORT",
            ),
        })
    return {
        "authority_class": "REFERENCE_LEDGER_SELF_REPORT",
        "source_path": path,
        "physical_lines": len(decoded[path]),
        "statement_denominator": len(rows),
        "rows": rows,
        "adopted_release_text_authority_granted": False,
        "proposition_truth_validated": False,
        "rule": "The reference ledger records process claims and candidate availability; it is not adopted release prose or proposition proof.",
    }


def snapshot_audit() -> dict[str, Any]:
    path6 = "Claude/docs/v1.0.21/results/snapshot_v1021_q6.json"
    path7 = "Claude/docs/v1.0.21/results/snapshot_v1021_q7.json"
    a = strict_json(git_bytes(BASELINE, path6))
    b = strict_json(git_bytes(BASELINE, path7))
    key = "graphite_ica_ch1_v1.0.21.tex"
    labels6 = set(a[key]["labels"])
    labels7 = set(b[key]["labels"])
    return {
        "q6": {"path": path6, "traversal": traversal(a)},
        "q7": {"path": path7, "traversal": traversal(b)},
        "ch1_label_count_q6": len(labels6), "ch1_label_count_q7": len(labels7),
        "actual_added_labels": len(labels7 - labels6),
        "added_label_names": sorted(labels7 - labels6),
        "ledger_claimed_added_labels": 6,
        "added_equation_blocks": len(set(b[key]["eqblocks"]) - set(a[key]["eqblocks"])),
        "bib_count_q6": len(a[key]["bibitems"]), "bib_count_q7": len(b[key]["bibitems"]),
        "authority": "STRUCTURAL_ONLY_NOT_SCIENTIFIC_TRUTH",
    }


def parse_bibliography(lines: list[str]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    wanted = set(LCO_KEYS) | set(SI_KEYS)
    rows = []
    raw_by_key = {}
    for line_no, line in enumerate(lines, 1):
        match = re.search(r"\\bibitem\{([^}]+)\}", line)
        if not match or match.group(1) not in wanted:
            continue
        key = match.group(1)
        frozen_doi = line.split("DOI:", 1)[1].strip().split()[0].rstrip(".;") if "DOI:" in line else None
        raw_by_key[key] = line
        rows.append({
            "key": key, "material_group": "LCO" if key in LCO_KEYS else "SI",
            "path": "Claude/docs/v1.0.21/_sections/ch1_bib.tex", "line": line_no,
            "frozen_entry": line, "frozen_doi": frozen_doi,
            "source_tier": "ADOPTED_RELEASE_BIBLIOGRAPHY", "proposition_authority": False,
        })
    rows.sort(key=lambda row: (row["material_group"], row["line"]))
    return rows, raw_by_key


def metadata_rows(bib_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in bib_rows:
        key = row["key"]
        doi, _title, venue, volume, issue, pages, year = META[key]
        conflict = key == "limthongkul2003"
        out.append({
            "key": key, "material_group": row["material_group"],
            "frozen_doi": row["frozen_doi"], "normalized_doi": doi,
            "normalized_authors": AUTHORS[key], "normalized_title": FULL_TITLES[key],
            "normalized_container": venue,
            "volume": volume, "issue": issue, "page_or_article": pages, "print_year": year,
            "resolver": "CROSSREF_REST_AND_DOI_RESOLVER", "checked_date": CHECKED_DATE,
            "resolver_state": "CONFLICTING_IDENTIFIER" if conflict else "RESOLVED_METADATA_MATCH",
            "publisher_record_state": "TITLE_IDENTIFIER_METADATA_MATCH" if not conflict else "CORRECTED_IDENTIFIER_TITLE_MATCH",
            "primary_fulltext_verified": key == "verbrugge_lisi2016",
            "exact_proposition_anchor_state": (
                "PRIMARY_FULLTEXT_EQS_2_TO_7_CONDITIONAL_MODEL_ONLY" if key == "verbrugge_lisi2016"
                else "PUBLISHER_ABSTRACT_NUMERIC_DISTINCTION" if key == "swiderska2019"
                else "UNVERIFIED_EXTERNAL"
            ),
            "metadata_is_not_proposition_proof": True,
        })
    return out


def release_text_paths() -> list[str]:
    names = run_git("ls-tree", "-r", "--name-only", BASELINE, "Claude/docs/v1.0.21")
    assert isinstance(names, str)
    return sorted(path for path in names.splitlines() if Path(path).suffix.lower() == ".tex")


def citation_occurrences() -> list[dict[str, Any]]:
    relevant = LCO_CITE_KEYS | set(SI_KEYS)
    rows = []
    for path in release_text_paths():
        lines = git_bytes(BASELINE, path).decode("utf-8", "strict").splitlines()
        for line_no, line in enumerate(lines, 1):
            for command_no, match in enumerate(re.finditer(r"\\cite\{([^}]+)\}", line), 1):
                for key_no, key in enumerate((item.strip() for item in match.group(1).split(",")), 1):
                    if key not in relevant:
                        continue
                    rows.append({
                        "occurrence_id": "", "path": path, "line": line_no,
                        "cite_command_index_on_line": command_no, "key_index_in_command": key_no,
                        "key": key, "material_group": "SI" if key in SI_KEYS else "LCO",
                        "line_text": line, "proposition_support_state": "UNVERIFIED_EXTERNAL",
                    })
    rows.sort(key=lambda row: (row["material_group"], row["path"], row["line"], row["cite_command_index_on_line"], row["key_index_in_command"], row["key"]))
    counts = {"LCO": 0, "SI": 0}
    for row in rows:
        group = row["material_group"]
        counts[group] += 1
        row["occurrence_id"] = f"P062-CITE-{group}-{counts[group]:04d}"
    return rows


def source_line_inventory(decoded: dict[str, list[str]]) -> list[dict[str, Any]]:
    paths = [spec[1] for spec in SOURCE_SPECS if (
        "ch1_sec1" in spec[1] or "ch1_appA" in spec[1] or "ch1_appD" in spec[1]
    )]
    number_pattern = re.compile(r"(?<![A-Za-z])[-+~≈]?\d+(?:\.\d+)?(?:\\%|%|\s*mV|\s*V|\s*GPa|\s*nm|\s*K|\s*J|\s*k_B)?")
    cite_pattern = re.compile(r"\\cite\{([^}]+)\}")
    approximation_words = ("tier", "근사", "시연", "placeholder", "가정", "상한", "대표", "초기값", "approx")
    rows = []
    for path in paths:
        material = "SI" if "appD_si" in path else "LCO"
        for line_no, line in enumerate(decoded[path], 1):
            cites = [key.strip() for match in cite_pattern.finditer(line) for key in match.group(1).split(",")]
            values = [value.strip() for value in number_pattern.findall(line)]
            if not cites and not values:
                continue
            rows.append({
                "inventory_id": f"P062-LINE-{len(rows)+1:04d}", "material": material,
                "path": path, "line": line_no, "line_text": line,
                "cite_keys": cites, "numeric_tokens": values,
                "approximation_or_tier_marker": any(word.lower() in line.lower() for word in approximation_words),
                "semantic_status": "LEXICAL_INVENTORY_REQUIRES_CURATED_SCOPE_ROW_FOR_LOAD_BEARING_USE",
            })
    return rows


def tex_without_comment(line: str) -> str:
    """Remove a TeX comment while preserving escaped percent signs."""
    for index, char in enumerate(line):
        if char != "%":
            continue
        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        if backslashes % 2 == 0:
            return line[:index]
    return line


def logical_fragments(parts: list[tuple[int, str]]) -> list[tuple[int, int, str]]:
    joined_parts: list[str] = []
    spans: list[tuple[int, int, int]] = []
    cursor = 0
    for line_no, text in parts:
        normalized = re.sub(r"\s+", " ", text.strip())
        if not normalized:
            continue
        if joined_parts:
            cursor += 1
        start = cursor
        joined_parts.append(normalized)
        cursor += len(normalized)
        spans.append((start, cursor, line_no))
    joined = " ".join(joined_parts)
    if not joined:
        return []
    boundaries = [0]
    split_re = re.compile(
        r"(?<=[.!?])\s+(?=(?:[A-Z가-힣]|\\text|\\emph|\())"
        r"|(?<![\w{\\])(?=\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\)\s)"
        r"|(?=(?:첫째|둘째|셋째|넷째),)",
        re.IGNORECASE,
    )
    for match in split_re.finditer(joined):
        boundaries.extend([match.start(), match.end()])
    boundaries.append(len(joined))
    fragments: list[tuple[int, int, str]] = []
    for start, end in zip(boundaries[0::2], boundaries[1::2]):
        while start < end and joined[start].isspace():
            start += 1
        while end > start and joined[end - 1].isspace():
            end -= 1
        if start >= end:
            continue
        touched = [line_no for lo, hi, line_no in spans if hi > start and lo < end]
        if touched:
            fragments.append((min(touched), max(touched), joined[start:end]))
    return fragments


def source_anchor(decoded: dict[str, list[str]], path: str, start: int, end: int, state: str) -> dict[str, Any]:
    return frozen_anchor(decoded, path, start, end, state)


def identifier_stripped(text: str) -> str:
    command = re.compile(r"\\(?:cite|label|ref|eqref|pageref|autoref|bibitem)\*?\{[^{}]*\}")
    clean = command.sub(lambda match: " " * len(match.group(0)), text)
    registered = re.compile(
        r"(?<![A-Za-z0-9_])(?:"
        + "|".join(re.escape(key) for key in sorted(set(LCO_KEYS) | set(SI_KEYS), key=len, reverse=True))
        + r")(?![A-Za-z0-9_])"
    )
    return registered.sub(lambda match: " " * len(match.group(0)), clean)


def normalized_unit_after(tail: str) -> tuple[str | None, str | None]:
    prefix = r"^\s*(?:(?:\\[,!;:])|(?:\\\s))*\s*\$?\s*"
    patterns = [
        (prefix + r"(?:\[|\()?(J/\(mol(?:\\,|\s)*K\))(?:\]|\))?", "J/(mol K)"),
        (prefix + r"(?:\[|\()?(J/mol)(?:\]|\))?", "J/mol"),
        (prefix + r"((?:k_B\$?/atom|k_\{?B\}?\$?/atom))", "k_B/atom"),
        (prefix + r"((?:\\mathrm\{)?mAh/g(?:\})?)", "mAh/g"),
        (prefix + r"((?:\\mathrm\{)?mV/GPa(?:\})?)", "mV/GPa"),
        (prefix + r"((?:\\mathrm\{)?mV/K(?:\})?)", "mV/K"),
        (prefix + r"(states/\(eV(?:\\cdot|\s)*Co\))", "states/(eV Co)"),
        (prefix + r"(e/eV/atom)", "e/eV/atom"),
        (prefix + r"((?:\\mathrm\{)?GPa(?:\})?)", "GPa"),
        (prefix + r"((?:\\mathrm\{)?mV(?:\})?)", "mV"),
        (prefix + r"((?:\\mathrm\{)?nm(?:\})?)", "nm"),
        (prefix + r"((?:\\mathrm\{)?V/K(?:\})?)", "V/K"),
        (prefix + r"((?:\\mathrm\{V\}|\\mathrm\s+V|V))", "V"),
        (prefix + r"((?:\\mathrm\{K\}|\\mathrm\s+K|K))", "K"),
        (prefix + r"((?:\\mathrm\{J\}|\\mathrm\s+J|J))", "J"),
        (prefix + r"(\\%|%)", "%"),
    ]
    for pattern, normalized in patterns:
        match = re.match(pattern, tail)
        if match:
            return match.group(1), normalized
    return None, None


def numeric_observations(claim_text: str) -> list[dict[str, Any]]:
    clean = identifier_stripped(claim_text)
    number_re = re.compile(
        r"(?:(?P<approx>\\approx|\\sim|≈|~)"
        r"(?P<number>[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
        r"|(?<![A-Za-z_])(?P<plain>[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?))"
    )
    rows = []
    for match in number_re.finditer(clean):
        raw_unit, normalized_unit = normalized_unit_after(clean[match.end():match.end() + 48])
        raw_number = match.group("number") or match.group("plain")
        number = float(raw_number)
        rows.append({
            "raw_token": match.group(0),
            "normalized_numeric": number,
            "approximation": match.group("approx") is not None,
            "raw_unit": raw_unit,
            "normalized_unit": normalized_unit,
        })
    return rows


def claim_semantics(
    path: str, start: int, end: int, claim_text: str,
    source_surface: str, claim_type: str,
) -> dict[str, Any]:
    lower = claim_text.lower()
    material = "SI" if (
        "appD_si" in path
        or any(f"\\bibitem{{{key}}}" in claim_text for key in SI_KEYS)
    ) else "LCO"
    if source_surface == "LEDGER_SELF_REPORT":
        material = "PROCESS"
    cite_keys = [
        key.strip()
        for match in re.finditer(r"\\cite\{([^}]+)\}", claim_text)
        for key in match.group(1).split(",")
    ]
    numbers = numeric_observations(claim_text)
    tier_markers = sorted(set(marker.upper() for marker in re.findall(r"tier\s*[- ]?\s*([abc])", lower)))
    approximation_markers = sorted({
        marker for marker in ("approx", "근사", "가정", "시연", "placeholder", "상한", "대표", "초기값")
        if marker in lower
    })
    role = "SOURCE_PROPOSITION"
    basis = "exact frozen logical proposition occurrence"
    state = "UNVERIFIED_EXTERNAL" if cite_keys else "EXACT_INTERNAL_SOURCE_MATCH"
    evidence_tier = "INTERNAL_DERIVATION" if claim_type == "DISPLAY_EQUATION" else "INTERNAL_RELEASE_CLAIM"
    ceiling = "frozen release proposition occurrence; not external scientific or material truth"
    primary = 79 if material == "SI" else 78
    downstream = [primary, 82]
    if source_surface == "BIBLIOGRAPHY_ENTRY":
        role, evidence_tier, state = "BIBLIOGRAPHY_ENTRY", "METADATA", "UNVERIFIED_EXTERNAL"
        ceiling = "bibliographic identity only; not proposition proof"
        primary, downstream = 71, [71, 79 if material == "SI" else 78, 82]
    elif source_surface == "LEDGER_SELF_REPORT":
        role, evidence_tier, state = "REFERENCE_LEDGER_SELF_REPORT", "LEDGER_SELF_REPORT", "UNVERIFIED_EXTERNAL"
        ceiling = "second-order process self-report only; not adopted release text or proposition proof"
        primary, downstream = 71, [71, 82]
    elif set(tier_markers) == {"A", "B", "C"}:
        evidence_tier = "SOURCE_TIER_TAXONOMY"
        ceiling = "source-stated tier taxonomy only; it grants no proposition-level authority"
    elif "A" in tier_markers:
        evidence_tier = "SOURCE_STATED_TIER_A_UNVERIFIED"
        ceiling = "source-stated tier A; primary proposition remains externally unverified"
    elif "B" in tier_markers:
        evidence_tier = "SOURCE_STATED_TIER_B_UNVERIFIED"
        ceiling = "source-stated tier B; proposition remains externally unverified"
    elif "C" in tier_markers:
        evidence_tier = "TIER_C_MODEL"
        ceiling = "source-stated tier C model/approximation; not material truth"
    elif approximation_markers:
        evidence_tier = "INTERNAL_MODEL_ASSUMPTION"
        ceiling = "internal approximation occurrence; not material truth"
    if path.endswith("ch1_sec15_lcoelec.tex") and start <= 165 <= end and "1.1" in claim_text:
        role = "LCO_MODEL_GATE_INTEGRAL_1P1_KB_PER_ATOM"
        basis = "complete-metal electronic entropy and model MIT gate integral"
        state, primary, downstream = "UNVERIFIED_EXTERNAL", 71, [71, 78, 82]
    elif path.endswith("ch1_sec15_lcoelec.tex") and start <= 166 <= end and "0.18" in claim_text:
        role = "LCO_O3_TOTAL_PARTIAL_MOLAR_0P18_KB_PER_ATOM"
        basis = "O3 configurational plus vibrational plus electronic total partial-molar quantity"
        state, primary, downstream = "UNVERIFIED_EXTERNAL", 71, [71, 74, 78, 82]
    elif path.endswith("ch1_sec13_lcohys.tex") and any(token in claim_text for token in ("도핑", "doped", "Al", "Mg")):
        role, state = "PURE_LCO_TO_DOPED_LCO_PROMOTION", "REJECTED"
        ceiling = "no doped-specific primary support; pure-LCO evidence cannot prove doped LCO"
        primary, downstream = 78, [71, 78, 82]
    elif path.endswith("ch1_sec15_lcoelec.tex") and start <= 340 and end >= 301:
        role, evidence_tier = "LCO_TIER_C_ONE_POINT_DEMONSTRATION", "TIER_C_MODEL"
        ceiling = "tier-C one-point arithmetic only; not material truth"
        primary, downstream = 78, [74, 78, 82]
    elif path.endswith("ch1_appD_si.tex") and start <= 11 and end >= 8:
        role, state = "SI_BRIDGEHEAD_NOT_COMPLETE_MODEL", "REJECTED"
        ceiling = "preliminary bridgehead explicitly lacks a complete Si derivation"
        primary, downstream = 79, [79, 82]
    return {
        "material": material, "semantic_role": role, "claim_type": claim_type,
        "citation_keys": cite_keys, "numeric_observations": numbers,
        "normalized_units": sorted({row["normalized_unit"] for row in numbers if row["normalized_unit"]}),
        "approximation_markers": approximation_markers,
        "source_tier_markers": tier_markers,
        "basis": basis, "validity_domain": "exact frozen proposition occurrence; downstream owner must adjudicate validity",
        "evidence_tier": evidence_tier, "proposition_state": state,
        "authority_ceiling": ceiling, "primary_target_phase": primary,
        "downstream_target_phases": sorted(set(downstream)),
    }


def assemble_text_claims(
    decoded: dict[str, list[str]], path: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    lines = decoded[path]
    claims: list[dict[str, Any]] = []
    classifications: list[dict[str, Any]] = []
    prose: list[tuple[int, str]] = []
    table: list[tuple[int, str]] = []
    tikz_command: list[tuple[int, str]] = []
    in_table = False
    in_tikz = False
    index = 1

    def mark(line_no: int, category: str) -> None:
        classifications.append({"line": line_no, "class": category})

    def emit(start: int, end: int, text: str, claim_type: str) -> None:
        normalized = re.sub(r"\s+", " ", text.strip())
        if not normalized:
            return
        claims.append({
            "source_surface": "ADOPTED_RELEASE_TEXT",
            "path": path, "line_start": start, "line_end": end,
            "claim_text": normalized,
            "claim_text_sha256": sha256((normalized + "\n").encode("utf-8")),
            "anchor": source_anchor(decoded, path, start, end, "PRESENT_IN_ADOPTED_RELEASE_TEXT"),
            **claim_semantics(path, start, end, normalized, "ADOPTED_RELEASE_TEXT", claim_type),
        })

    def flush_prose() -> None:
        nonlocal prose
        for start, end, fragment in logical_fragments(prose):
            claim_type = "CAPTION" if "\\caption" in fragment else "PROSE_PROPOSITION"
            emit(start, end, fragment, claim_type)
        prose = []

    def flush_table() -> None:
        nonlocal table
        if table:
            emit(table[0][0], table[-1][0], " ".join(text for _, text in table), "TABLE_SCIENTIFIC_ROW")
        table = []

    def flush_tikz_command() -> None:
        nonlocal tikz_command
        for start, end, fragment in logical_fragments(tikz_command):
            emit(start, end, fragment, "TIKZ_SCIENTIFIC_DEFINITION")
        tikz_command = []

    forced = {(164, 165), (166, 167)} if path.endswith("ch1_sec15_lcoelec.tex") else set()
    forced_by_start = {start: end for start, end in forced}
    while index <= len(lines):
        if path.endswith("ch1_sec13_lcohys.tex") and index == 124:
            flush_prose()
            semantic = " ".join(tex_without_comment(lines[i - 1]).strip() for i in range(124, 133))
            if semantic.count(";") != 1 or semantic.count("])" ) != 1 or ". " not in semantic:
                raise RuntimeError("curated tier-A/tier-C atomic delimiters drift")
            intro, remainder = semantic.split(". ", 1)
            tier_a, tier_c_remainder = remainder.split(";", 1)
            tier_c, conclusion = tier_c_remainder.split("])", 1)
            for line_no in range(124, 133):
                mark(line_no, "CURATED_ATOMIC_PROPOSITION")
            emit(124, 124, intro + ".", "CURATED_ATOMIC_PROPOSITION")
            emit(124, 126, tier_a, "CURATED_ATOMIC_PROPOSITION")
            emit(126, 128, tier_c + "])", "CURATED_ATOMIC_PROPOSITION")
            emit(128, 132, conclusion, "CURATED_ATOMIC_PROPOSITION")
            index = 133
            continue
        if index in forced_by_start:
            flush_prose()
            end = forced_by_start[index]
            semantic = [tex_without_comment(lines[i - 1]).strip() for i in range(index, end + 1)]
            for line_no in range(index, end + 1):
                mark(line_no, "CURATED_ATOMIC_PROPOSITION")
            emit(index, end, " ".join(part for part in semantic if part), "CURATED_ATOMIC_PROPOSITION")
            index = end + 1
            continue
        line = lines[index - 1]
        stripped = tex_without_comment(line).strip()
        if "\\begin{tikzpicture}" in stripped:
            flush_prose(); mark(index, "STRUCTURAL_TIKZ_BOUNDARY"); in_tikz = True; index += 1; continue
        if in_tikz:
            if "\\end{tikzpicture}" in stripped:
                flush_tikz_command()
                mark(index, "STRUCTURAL_TIKZ_BOUNDARY"); in_tikz = False
            elif tikz_command or re.match(r"^\\(?:node|draw|foreach)\b", stripped):
                mark(index, "TIKZ_SCIENTIFIC_DEFINITION")
                tikz_command.append((index, stripped))
                if ";" in stripped:
                    flush_tikz_command()
            elif stripped:
                mark(index, "STRUCTURAL_TIKZ_FORMAT")
            else:
                mark(index, "COMMENT_OR_BLANK_TIKZ")
            index += 1
            continue
        display_match = re.search(r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}|\\\[", stripped)
        if display_match:
            flush_prose()
            env = display_match.group(1)
            end_token = "\\]" if env is None else f"\\end{{{env}}}"
            start = index
            block: list[str] = []
            while index <= len(lines):
                current = tex_without_comment(lines[index - 1]).strip()
                mark(index, "DISPLAY_BLOCK")
                if current and current not in {
                    f"\\begin{{{env}}}" if env else "\\[", end_token,
                    "\\begin{aligned}", "\\end{aligned}",
                } and not re.fullmatch(r"\\label\{[^}]+\}", current):
                    block.append(current)
                done = end_token in current
                index += 1
                if done:
                    break
            emit(start, index - 1, " ".join(block), "DISPLAY_EQUATION")
            continue
        if re.search(r"\\begin\{(?:tabular|longtable)\}", stripped):
            flush_prose(); mark(index, "STRUCTURAL_TABLE_BOUNDARY"); in_table = True; index += 1; continue
        if in_table:
            if re.search(r"\\end\{(?:tabular|longtable)\}", stripped):
                flush_table(); mark(index, "STRUCTURAL_TABLE_BOUNDARY"); in_table = False
            elif not stripped or re.fullmatch(
                r"\\(?:toprule|midrule|bottomrule|hline|endfirsthead|endhead|endfoot|endlastfoot)",
                stripped,
            ):
                flush_table(); mark(index, "STRUCTURAL_TABLE_FORMAT")
            else:
                mark(index, "TABLE_ROW_SOURCE"); table.append((index, stripped))
                if "\\\\" in stripped:
                    flush_table()
            index += 1
            continue
        if not line.strip():
            flush_prose(); mark(index, "BLANK"); index += 1; continue
        if not stripped:
            flush_prose(); mark(index, "COMMENT_ONLY"); index += 1; continue
        if re.fullmatch(
            r"\\(?:renewcommand|setlength)\{[^}]+\}\{[^}]+\}|"
            r"(?:\\(?:small|footnotesize|scriptsize|centering|toprule|midrule|bottomrule|hline|medskip|smallskip|noindent|clearpage|newpage|appendix))+",
            stripped,
        ):
            flush_prose(); mark(index, "STRUCTURAL_FORMAT"); index += 1; continue
        if re.fullmatch(r"\\(?:begin|end)\{[^}]+\}(?:\[[^]]*\])?(?:\\label\{[^}]+\})?", stripped):
            flush_prose(); mark(index, "STRUCTURAL_ENVIRONMENT"); index += 1; continue
        if re.fullmatch(r"\\(?:label|includegraphics|input)\{[^}]+\}", stripped):
            flush_prose(); mark(index, "STRUCTURAL_COMMAND"); index += 1; continue
        if re.match(r"^\\(?:section|subsection|subsubsection|paragraph|chapter)\*?\{", stripped):
            flush_prose(); mark(index, "STRUCTURAL_HEADING"); index += 1; continue
        if stripped in {"{", "}", "\\", "\\\\"}:
            flush_prose(); mark(index, "STRUCTURAL_DELIMITER"); index += 1; continue
        if stripped.startswith("\\item"):
            flush_prose()
        mark(index, "PROSE_SOURCE")
        prose.append((index, stripped))
        index += 1
    flush_prose(); flush_table()
    class_counts: dict[str, int] = {}
    for item in classifications:
        category = item["class"]
        class_counts[category] = class_counts.get(category, 0) + 1
    if len(classifications) != len(lines) or {row["line"] for row in classifications} != set(range(1, len(lines) + 1)):
        raise RuntimeError(f"line-classification coverage failure: {path}")
    return claims, {
        "path": path, "physical_lines": len(lines), "class_counts": class_counts,
        "line_classification_sha256": sha256(json_bytes(classifications)),
        "claim_atom_count": len(claims),
        "coverage_state": "EVERY_PHYSICAL_LINE_CLASSIFIED_EXACTLY_ONCE",
    }


def source_claim_manifest(decoded: dict[str, list[str]], bib_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []
    for path in CLAIM_TEXT_PATHS:
        path_rows, path_coverage = assemble_text_claims(decoded, path)
        rows.extend(path_rows); coverage.append(path_coverage)
    for bib in sorted(bib_rows, key=lambda row: (row["material_group"], row["line"])):
        path, line_no, claim_text = bib["path"], bib["line"], bib["frozen_entry"]
        rows.append({
            "source_surface": "BIBLIOGRAPHY_ENTRY",
            "path": path, "line_start": line_no, "line_end": line_no,
            "claim_text": claim_text,
            "claim_text_sha256": sha256((claim_text + "\n").encode("utf-8")),
            "anchor": source_anchor(decoded, path, line_no, line_no, "PRESENT_IN_ADOPTED_RELEASE_TEXT"),
            **claim_semantics(path, line_no, line_no, claim_text, "BIBLIOGRAPHY_ENTRY", "BIBLIOGRAPHY_ENTRY"),
        })
    for line_no in REFERENCE_LEDGER_CLAIM_LINES:
        claim_text = decoded[REFERENCE_LEDGER_PATH][line_no - 1].strip()
        rows.append({
            "source_surface": "LEDGER_SELF_REPORT",
            "path": REFERENCE_LEDGER_PATH, "line_start": line_no, "line_end": line_no,
            "claim_text": claim_text,
            "claim_text_sha256": sha256((claim_text + "\n").encode("utf-8")),
            "anchor": source_anchor(decoded, REFERENCE_LEDGER_PATH, line_no, line_no, "PRESENT_IN_REFERENCE_LEDGER_SELF_REPORT"),
            **claim_semantics(REFERENCE_LEDGER_PATH, line_no, line_no, claim_text, "LEDGER_SELF_REPORT", "LEDGER_SELF_REPORT"),
        })
    for index, row in enumerate(rows, 1):
        row["source_claim_id"] = f"P062-SOURCE-CLAIM-{index:04d}"
        row["route_kind"] = "SCOPE"; row["route_id"] = f"P062-SCOPE-{index:04d}"
        row["external_scientific_truth_validated"] = False
        row["external_material_truth_validated"] = False
    return rows, coverage



GNF_OWNER_ANCHORS = {
    "P062-GNF-001": (CLAIM_TEXT_PATHS[4], 176),
    "P062-GNF-002": (CLAIM_TEXT_PATHS[4], 305),
    "P062-GNF-003": (CLAIM_TEXT_PATHS[2], 172),
    "P062-GNF-004": (CLAIM_TEXT_PATHS[9], 73),
    "P062-GNF-005": (CLAIM_TEXT_PATHS[9], 70),
    "P062-GNF-006": (CLAIM_TEXT_PATHS[9], 71),
    "P062-GNF-007": (CLAIM_TEXT_PATHS[9], 72),
    "P062-GNF-008": (CLAIM_TEXT_PATHS[9], 85),
    "P062-GNF-009": (CLAIM_TEXT_PATHS[9], 85),
    "P062-GNF-010": (CLAIM_TEXT_PATHS[9], 86),
    "P062-GNF-011": (CLAIM_TEXT_PATHS[4], 165),
    "P062-GNF-012": (CLAIM_TEXT_PATHS[4], 166),
    "P062-GNF-013": (CLAIM_TEXT_PATHS[9], 17),
    "P062-GNF-014": (CLAIM_TEXT_PATHS[9], 18),
    "P062-GNF-015": (CLAIM_TEXT_PATHS[9], 20),
    "P062-GNF-016": (CLAIM_TEXT_PATHS[9], 41),
    "P062-GNF-017": (CLAIM_TEXT_PATHS[9], 47),
}


def manifest_scope_matrix(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gap_by_claim: dict[str, list[str]] = {}
    for gap_id, (path, line_no) in GNF_OWNER_ANCHORS.items():
        candidates = [
            row for row in manifest
            if row["path"] == path and row["line_start"] <= line_no <= row["line_end"]
        ]
        if not candidates:
            raise RuntimeError(f"GNF owner anchor has no source claim: {gap_id} {path}:{line_no}")
        gap_by_claim.setdefault(candidates[0]["source_claim_id"], []).append(gap_id)
    rows = []
    for claim in manifest:
        quantity: Any = claim["claim_text"]
        value: Any = claim["numeric_observations"]
        unit: Any = claim["normalized_units"]
        if claim["semantic_role"] == "LCO_MODEL_GATE_INTEGRAL_1P1_KB_PER_ATOM":
            quantity, value, unit = "model gate-integrated complete-metal electronic entropy", 1.1, "k_B/atom"
        elif claim["semantic_role"] == "LCO_O3_TOTAL_PARTIAL_MOLAR_0P18_KB_PER_ATOM":
            quantity, value, unit = "O3 total partial-molar entropy quantity", 0.18, "k_B/atom"
        rows.append({
            "scope_id": claim["route_id"], "source_claim_id": claim["source_claim_id"],
            "material": claim["material"], "claim_surface": claim["source_surface"],
            "claim_anchor": claim["anchor"], "ground_not_found_id": None,
            "quantity": quantity, "value": value,
            "unit": unit, "basis": claim["basis"],
            "validity_domain": "exact frozen source occurrence; downstream validity requires owner adjudication",
            "source_surface": claim["source_surface"], "evidence_tier": claim["evidence_tier"],
            "proposition_state": claim["proposition_state"],
            "semantic_role": claim["semantic_role"], "authority_ceiling": claim["authority_ceiling"],
            "external_scientific_truth_validated": False, "external_material_truth_validated": False,
            "primary_target_phase": claim["primary_target_phase"],
            "downstream_target_phases": claim["downstream_target_phases"],
            "evidence_gap_ids": gap_by_claim.get(claim["source_claim_id"], []),
        })
    return rows


def logistic(value: float) -> float:
    if value >= 0:
        e = math.exp(-value)
        return 1.0 / (1.0 + e)
    e = math.exp(value)
    return e / (1.0 + e)


def q6_model_probe(x_bar: float, gate_on: bool, reanchor_off: bool = False) -> dict[str, float]:
    dse = -(math.pi ** 2 / 3.0) * R * (KB * T_REF / EV_TO_J) * (13.0 / 0.05) * 0.25
    dS1 = 6.0 + dse if gate_on else 6.0
    dH1 = -391016.1
    if not gate_on and reanchor_off:
        dH1 = T_REF * dS1 - F * 3.930
    transitions = [
        {"dH": dH1, "dS": dS1, "Q": 0.55},
        {"dH": -375554.4, "dS": -4.0, "Q": 0.30},
        {"dH": -391360.0, "dS": -2.0, "Q": 0.15},
    ]
    for tr in transitions:
        tr["U"] = (-tr["dH"] + T_REF * tr["dS"]) / F
    width = R * T_REF / F
    lo = min(tr["U"] for tr in transitions) - 1.0
    hi = max(tr["U"] for tr in transitions) + 1.0
    for _ in range(220):
        mid = (lo + hi) / 2.0
        charge = sum(tr["Q"] * logistic((mid - tr["U"]) / width) for tr in transitions)
        if charge < x_bar:
            lo = mid
        else:
            hi = mid
    U_oc = (lo + hi) / 2.0
    numerator = simple_numerator = denominator = 0.0
    for tr in transitions:
        xi = logistic((U_oc - tr["U"]) / width)
        g = xi * (1.0 - xi) / width
        weight = tr["Q"] * g
        config = (R / F) * math.log(xi / (1.0 - xi))
        numerator += weight * (tr["dS"] / F + config)
        simple_numerator += weight * tr["dS"] / F
        denominator += weight
    complete = numerator / denominator * 1.0e3
    simple = simple_numerator / denominator * 1.0e3
    return {
        "U_oc_V": U_oc, "complete_mV_per_K": complete,
        "simple_mV_per_K": simple, "config_mV_per_K": complete - simple,
    }


def q6_audit() -> dict[str, Any]:
    dse = -(math.pi ** 2 / 3.0) * R * (KB * T_REF / EV_TO_J) * (13.0 / 0.05) * 0.25
    rows = []
    for x_bar in (0.50, 0.85):
        on = q6_model_probe(x_bar, True)
        off = q6_model_probe(x_bar, False)
        rows.append({
            "x_bar": x_bar, "gate_on": on, "gate_off": off,
            "same_dH_counterfactual_delta": {
                "U_oc_mV": (on["U_oc_V"] - off["U_oc_V"]) * 1.0e3,
                "complete_mV_per_K": on["complete_mV_per_K"] - off["complete_mV_per_K"],
            },
        })
    reanchored_off = q6_model_probe(0.85, False, True)
    on85 = q6_model_probe(0.85, True)
    return {
        "source_input_class": "TIER_C_ONE_POINT_DEMONSTRATION_PLACEHOLDER",
        "temperature_model": "FROZEN_T_REF_CONSTANT_ELECTRONIC_ENTROPY_OFFSET",
        "displayed_inputs": {
            "U_V": [3.93, 3.88, 4.05], "delta_S_rxn_J_per_mol_K": [6.0, -4.0, -2.0],
            "Q_fraction": [0.55, 0.30, 0.15], "x_MIT_Li_content": 0.85,
            "dx_MIT": 0.05, "g_max_states_per_eV_Co": 13.0, "T_K": T_REF,
        },
        "slot_arithmetic": {
            "delta_S_e_J_per_mol_K": dse, "delta_S_eff_J_per_mol_K": 6.0 + dse,
            "slot_slope_mV_per_K": (6.0 + dse) / F * 1.0e3,
            "unit_chain": "states/(eV Co) -> states/(J Co); R*kB and Avogadro basis -> J/(mol K); divide F -> V/K",
            "sign": "NEGATIVE_ELECTRONIC_CORRECTION_IN_INSERTION_REACTION_CONVENTION",
        },
        "independent_recomputation": rows,
        "reanchored_gate_off_at_x_bar_0_85": {
            "rule": "REMOVE_ELECTRONIC_ENTROPY_AND_RECOMPUTE_DH_TO_KEEP_TREF_T1_U_EQUALS_3_930_V",
            "gate_off": reanchored_off,
            "gate_on": on85,
            "delta_U_oc_mV": (on85["U_oc_V"] - reanchored_off["U_oc_V"]) * 1.0e3,
            "delta_complete_mV_per_K": on85["complete_mV_per_K"] - reanchored_off["complete_mV_per_K"],
            "interpretation": "The reported -91 mV is a same-dH counterfactual that breaks the Tref anchoring convention; it is not an isolated physical gate shift.",
        },
        "coordinate_adjudication": {
            "x_bar_role": "GLOBAL_TOTAL_DELITHIATION_FRACTION",
            "x_MIT_role": "LCO_LITHIUM_CONTENT_COORDINATE_IN_GATE_MODEL",
            "gate_argument": "T1_TRANSITION_X_CENTER_FIXED_AT_0.85",
            "gate_depends_on_global_x_bar": False,
            "conclusion": "The source equates unlike coordinates and falsely labels x_bar=0.50 as gate-off; both tested x_bar values use the same T1 electronic offset.",
        },
        "scope_separation": {
            "tier_C_one_point_demo": "AUDITED_INTERNAL_ARITHMETIC_ONLY",
            "multi_temperature_reconstruction": "MISSING_ROUTE_PHASE_078_082",
            "irreversible_heat": "MISSING_ROUTE_PHASE_078_082",
            "doped_high_voltage_LCO": "UNSUPPORTED_PROMOTION_ROUTE_PHASE_071_078",
            "oxygen_redox_loss_surface_reconstruction": "MISSING_ROUTE_PHASE_078_082",
            "structural_transition": "PARTIAL_CITATION_ONLY_ROUTE_PHASE_071_078",
            "experimental_validation": "UNVERIFIED_EXTERNAL_ROUTE_PHASE_071_078",
        },
        "code_output_is_science_authority": False,
        "external_material_truth_validated": False,
    }


def q7_audit(snapshot: dict[str, Any]) -> dict[str, Any]:
    missing = [
        ("SI_SPECIFIC_FREE_ENERGY", 79, [79, 82]),
        ("STRESS_CHEMICAL_POTENTIAL", 79, [79, 82]),
        ("PLASTICITY_DAMAGE", 79, [79, 82]),
        ("INTERFACE_SEI", 79, [79, 82]),
        ("HYSTERESIS_EVOLUTION", 79, [79, 82]),
        ("SIOX_ALLOCATION", 79, [74, 79, 82]),
        ("SIC_ALLOCATION", 79, [79, 82]),
        ("BLEND_ALLOCATION", 80, [74, 79, 80, 82]),
    ]
    return {
        "document_status": "PRELIMINARY_BRIDGEHEAD_NO_COMPLETE_DERIVATION_NO_OWN_DATA",
        "facts_inventory": [
            {"fact": "high_temperature_Li_Si_intermediate_phases", "anchor": [14, 15], "state": "UNVERIFIED_EXTERNAL"},
            {"fact": "room_temperature_amorphization_and_moving_boundary", "anchor": [16, 17], "state": "CONFLICTING_SOURCE_AND_INCOMPLETE_SPATIAL_ANCHOR"},
            {"fact": "Li15Si4_near_50_mV", "anchor": [18, 19], "state": "UNVERIFIED_EXTERNAL"},
            {"fact": "sloping_amorphous_U_of_x", "anchor": [19, 20], "state": "UNVERIFIED_EXTERNAL"},
            {"fact": "about_300_percent_volume_change", "anchor": [20, 21], "state": "PARTIAL_BASIS_NOT_FIXED"},
            {"fact": "stress_minus_1_75_GPa_and_100_to_120_mV_per_GPa", "anchor": [22, 24], "state": "PARTIAL_NUMBERS_NARROWLY_SUPPORTED_DOMINANCE_REJECTED"},
            {"fact": "about_150_nm_first_lithiation_fracture_threshold", "anchor": [25, 25], "state": "PARTIAL_DOMAIN_MUST_BE_NANOPARTICLE_FIRST_LITHIATION"},
            {"fact": "review_overview", "anchor": [26, 26], "state": "REVIEW_NOT_LOAD_BEARING_PRIMARY_PROOF"},
        ],
        "node_map": [
            {"node": "N0", "source_state": "PRESERVE", "audit_state": "PRESERVE_WITH_SIGN_BASIS_RECHECK"},
            {"node": "N1", "source_state": "REINTERPRET", "audit_state": "REINTERPRET"},
            {"node": "N2", "source_state": "REINTERPRET", "audit_state": "REINTERPRET_PLUS_NEW_PHYSICS"},
            {"node": "N3", "source_state": "NEW_PHYSICS", "audit_state": "NEW_PHYSICS_WITH_INVALID_55_MV_GLOBAL_BOUND"},
            {"node": "N4", "source_state": "REINTERPRET", "audit_state": "PHENOMENOLOGICAL_UNANCHORED"},
            {"node": "N5", "source_state": "STRUCTURAL_PRESERVE", "audit_state": "CONDITIONAL_INDEPENDENT_SITE_MODEL_ONLY"},
            {"node": "N6", "source_state": "PARTIAL", "audit_state": "PARTIAL_RECLASSIFICATION_NOT_LEDGERED"},
            {"node": "N7", "source_state": "PARTIAL", "audit_state": "PARTIAL"},
            {"node": "N8", "source_state": "STRUCTURAL_PRESERVE", "audit_state": "UNSUPPORTED_EYRING_PROMOTION"},
            {"node": "N9", "source_state": "PRESERVE", "audit_state": "CHARGE_ACCOUNTING_ONLY_NOT_EXACT_LOGISTIC_INVERSION"},
        ],
        "snapshot_delta": snapshot,
        "general_charge_conservation": "GENERAL_ACCOUNTING_IDENTITY_ONLY",
        "verbrugge_primary_fulltext_adjudication": {
            "url": "https://pdfs.semanticscholar.org/bdc1/6682f377d0cb500a27a825d16806cb5b5427.pdf",
            "pages": "A262-A263", "equations": "2-7",
            "confirmed": "multiple reaction site conservation and logistic-like inversion within the paper's model",
            "limitation": "different j sites are explicitly non-interacting and equilibrium potential uniquely determines each site occupancy",
            "proposition_state": "PARTIAL_CONDITIONAL_MODEL_NOT_ELECTRODE_NEUTRAL_EXACT_THEOREM",
        },
        "regular_solution_gap_adjudication": {
            "source_example": "Omega=4RT gives approximately 55 mV at 298.15 K",
            "correct_scope": "upper branch amplitude only for that fixed Omega and gamma<=1",
            "global_upper_bound": False,
            "counterexamples_mV": {"Omega_over_RT_6": 134.0, "Omega_over_RT_10": 311.0, "Omega_over_RT_20": 788.0},
        },
        "missing_governing_equations": [
            {"scope": scope, "status": "MISSING", "primary_target_phase": primary, "downstream_target_phases": downstream}
            for scope, primary, downstream in missing
        ],
        "governing_equation_conclusion": "NO_SI_SPECIFIC_GOVERNING_EQUATION_IN_V1021",
        "partial_molar_entropy_state": "GROUND_NOT_FOUND_ROUTE_PHASE_071_074_079",
        "external_material_truth_validated": False,
    }


def ground_not_found_records() -> list[dict[str, Any]]:
    lco_paths = [
        "Claude/docs/v1.0.21/_sections/ch1_sec11_lcointro.tex",
        "Claude/docs/v1.0.21/_sections/ch1_sec12_lcocenter.tex",
        "Claude/docs/v1.0.21/_sections/ch1_sec13_lcohys.tex",
        "Claude/docs/v1.0.21/_sections/ch1_sec14_lcodecomp.tex",
        "Claude/docs/v1.0.21/_sections/ch1_sec15_lcoelec.tex",
        "Claude/docs/v1.0.21/_sections/ch1_sec16_lcopeak.tex",
        "Claude/docs/v1.0.21/_sections/ch1_sec17_msmr.tex",
        "Claude/docs/v1.0.21/_sections/ch1_sec18_inputs.tex",
    ]
    si_path = "Claude/docs/v1.0.21/_sections/ch1_appD_si.tex"
    specs = [
        ("P062-GNF-001", "LCO_MULTI_TEMPERATURE_RECONSTRUCTION", lco_paths, 78, [78, 82]),
        ("P062-GNF-002", "LCO_IRREVERSIBLE_HEAT_MODEL", lco_paths, 78, [78, 82]),
        ("P062-GNF-003", "LCO_OXYGEN_REDOX_LOSS_SURFACE_RECONSTRUCTION_MODEL", lco_paths, 78, [71, 78, 82]),
        ("P062-GNF-004", "SI_STRESS_CHEMICAL_POTENTIAL_GOVERNING_EQUATION", [si_path], 79, [71, 79, 82]),
        ("P062-GNF-005", "SI_PLASTICITY_DAMAGE_GOVERNING_EQUATION", [si_path], 79, [79, 82]),
        ("P062-GNF-006", "SI_PARTICLE_SEI_RHEOLOGY_GOVERNING_EQUATION", [si_path], 79, [71, 79, 82]),
        ("P062-GNF-007", "SI_HYSTERESIS_EVOLUTION_ALLOCATION_EQUATION", [si_path], 79, [79, 82]),
        ("P062-GNF-008", "SIOX_CONVERSION_INACTIVE_MATRIX_ALLOCATION", [si_path], 79, [74, 79, 82]),
        ("P062-GNF-009", "SIC_COMPONENT_ALLOCATION", [si_path], 79, [79, 82]),
        ("P062-GNF-010", "GRAPHITE_SI_BLEND_MASS_CAPACITY_CURRENT_ALLOCATION", [si_path], 80, [74, 79, 80, 82]),
        ("P062-GNF-011", "PRIMARY_FULLTEXT_SUPPORT_FOR_MODEL_GATE_INTEGRAL_1_1_KB_PER_ATOM", lco_paths, 71, [71, 78, 82]),
        ("P062-GNF-012", "PRIMARY_FULLTEXT_PROPOSITION_ANCHOR_FOR_O3_TOTAL_PARTIAL_MOLAR_0_18_KB_PER_ATOM", lco_paths, 71, [71, 78, 82]),
        ("P062-GNF-013", "PRIMARY_SOURCE_FOR_SHARP_CORE_SHELL_MOVING_BOUNDARY_ALLOCATION", [si_path], 71, [71, 79, 82]),
        ("P062-GNF-014", "PRIMARY_FULLTEXT_ANCHOR_FOR_LI15SI4_50_MV", [si_path], 71, [71, 74, 79, 82]),
        ("P062-GNF-015", "PRIMARY_EQUATION_OR_FIGURE_FOR_AMORPHOUS_SI_U_OF_X", [si_path], 71, [71, 79, 82]),
        ("P062-GNF-016", "SI_PARTIAL_MOLAR_ENTROPY_DATA", [si_path], 71, [71, 74, 79, 82]),
        ("P062-GNF-017", "SI_SPECIFIC_EYRING_FINITE_RATE_DERIVATION", [si_path], 76, [71, 76, 79, 82]),
    ]
    rows = []
    for record_id, missing_scope, paths, primary, downstream in specs:
        sources = []
        for path in paths:
            raw = git_bytes(BASELINE, path)
            sources.append({
                "commit": BASELINE,
                "path": path,
                "physical_lines": len(raw.splitlines()),
                "raw_sha256": sha256(raw),
                "read_state": "READ_FULL_FOR_SCOPED_ABSENCE_ADJUDICATION",
            })
        rows.append({
            "ground_not_found_id": record_id,
            "missing_scope": missing_scope,
            "status": "GROUND_NOT_FOUND_IN_FROZEN_ADOPTED_RELEASE_SCOPE",
            "search_authority": "INTERNAL_FROZEN_RELEASE_ONLY_NOT_EXTERNAL_ABSENCE",
            "searched_sources": sources,
            "primary_target_phase": primary,
            "downstream_target_phases": downstream,
            "external_scientific_truth_validated": False,
            "external_material_truth_validated": False,
        })
    return rows


def findings() -> list[dict[str, Any]]:
    rows = [
        ("P062-LCO-C01", "P1", "Swiderska +0.83 mV/K is an inferred absolute single-electrode coefficient, while the isothermal Li|LCO cell coefficient is -0.25 mV/K; the frozen +80 J/(mol K) vs-Li derivation has the wrong basis/sign."),
        ("P062-LCO-C02", "P1", "Q6 states x_bar=0.50 is outside the gate and unchanged, but the implementation evaluates the T1 electronic term at fixed x_center=0.85 for every global x_bar."),
        ("P062-LCO-C03", "P1", "Q6 equates global delithiation fraction x_bar with the LCO lithium-content MIT coordinate without a mapping."),
        ("P062-SI-C01", "P1", "Frozen Limthongkul DOI ...00515-4 returns no matching record; the matching primary article DOI is ...00514-1."),
        ("P062-SI-C02", "P1", "Q7 change log and ledger claim +6 labels and 1:1 PASS, while strict snapshots show 247 to 254, or +7."),
        ("P062-SI-C03", "P1", "The blanket statement that Si hysteresis is mechanically dominated is stronger than the cited comparable/substantial and model-specific evidence."),
        ("P062-SI-C04", "P1", "General charge accounting is promoted to an electrode-neutral exact logistic inversion and unique-root structure although the cited model assumes noninteracting site classes."),
        ("P062-SI-C05", "P1", "The approximately 55 mV value at Omega=4RT is treated as a global regular-solution model upper bound; it is only the fixed-Omega branch bound."),
        ("P062-LCO-P2-01", "P2", "The reported -91 mV gate shift holds dH fixed even though dH absorbed the electronic entropy to preserve Tref anchoring; reanchoring nearly removes the Tref voltage shift."),
        ("P062-LCO-P2-02", "P2", "Pure-LCO sources are used for Al/Mg-doped high-voltage LCO claims without doped-specific primary support."),
        ("P062-LCO-P2-03", "P2", "Configurational partial-molar entropy is called rigorously T-independent at fixed x without resolving interacting/order-disorder physics."),
        ("P062-LCO-P2-04", "P2", "The claim that continuous DeltaS(x) data are absent conflicts with the composition-resolved scope of the Reynier record and needs a narrower component-level statement."),
        ("P062-LCO-P2-05", "P2", "g(EF)=13 states/(eV Co) is susceptibility-derived under a Pauli assumption, not a direct tier-A DOS endpoint."),
        ("P062-LCO-P2-06", "P2", "The 0.18 k_B/atom gate-release proposition lacks an exact accessible primary anchor in the frozen ledger."),
        ("P062-SI-P2-01", "P2", "The Si bridgehead adds zero governing-equation blocks and contains no Si-specific free-energy, stress, damage, SEI, or hysteresis law."),
        ("P062-SI-P2-02", "P2", "SiOx, Si-C, and graphite-Si blend capacity/current allocation are absent from Q7 and remain downstream scope."),
    ]
    return [
        {"finding_id": finding_id, "priority": priority, "status": "OPEN_ROUTED", "summary": summary,
         "external_truth_validated": False}
        for finding_id, priority, summary in rows
    ]


def semantic_projection(data: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(data)
    projected.pop("semantic_sha256", None)
    return projected


def build() -> tuple[dict[str, Any], str]:
    attestations, decoded = source_attestations()
    bib_rows, _ = parse_bibliography(decoded["Claude/docs/v1.0.21/_sections/ch1_bib.tex"])
    citations = citation_occurrences()
    snapshot = snapshot_audit()
    source_claims, source_claim_coverage = source_claim_manifest(decoded, bib_rows)
    scope = manifest_scope_matrix(source_claims)
    claim_path_counts = {
        path: sum(row["path"] == path for row in source_claims)
        for path in CLAIM_TEXT_PATHS + [BIBLIOGRAPHY_PATH, REFERENCE_LEDGER_PATH]
    }
    gnf_rows = ground_not_found_records()
    gnf_ids = {row["ground_not_found_id"] for row in gnf_rows}
    linked_gnf = {
        gap_id
        for row in scope
        for gap_id in row["evidence_gap_ids"]
    }
    if gnf_ids != linked_gnf:
        raise RuntimeError(f"scope/GNF bijection drift: {sorted(gnf_ids ^ linked_gnf)}")
    finding_rows = findings()
    data: dict[str, Any] = {
        "schema_version": "phase062-step54-v1",
        "artifact_id": "PHASE_062_V1021_LCO_SI_SCOPE_MATRIX",
        "status": "PASS_WITH_CONCERNS",
        "gate": "PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS",
        "builder_sha256": sha256(lf_normalized_bytes(Path(__file__).read_bytes())),
        "provenance": {
            "baseline_commit": BASELINE, "q6_commit": Q6_COMMIT, "q6_parent": Q6_PARENT,
            "q7_commit": Q7_COMMIT, "q7_parent": Q7_PARENT, "expected_parent": EXPECTED_PARENT,
            "external_observation_date": CHECKED_DATE,
            "frozen_source_modified": False, "production_module_imported_or_executed": False,
        },
        "result_first_contract": {
            "sentinel": "P062_STEP54_RESULT_FIRST_PRECOMMIT",
            "write_order": ["PHASE_062_STEP_054_LCO_SI_SCOPE_RESULT.md", "PHASE_062_V1021_LCO_SI_SCOPE_MATRIX.json"],
            "containing_commit": "PENDING_AT_PRECOMMIT_BY_DESIGN",
            "persistence_claimed": False,
            "step55_blocked_until": "PASS_P062_STEP54_PERSISTENCE",
        },
        "authority_contract": {
            "external_scientific_truth_validated": False,
            "external_material_truth_validated": False,
            "external_experimental_truth_validated": False,
            "canonical_equation_accepted": False,
            "final_manuscript_ready": False,
            "scope": "internal lineage, arithmetic, unit/basis, source-tier, proposition and owner routing",
        },
        "source_attestations": attestations,
        "adopted_release_text_inventory": {
            "authority_class": "ADOPTED_RELEASE_TEXT",
            "claim_row_denominator": sum(row["source_surface"] == "ADOPTED_RELEASE_TEXT" for row in source_claims),
            "present_anchor_rows": sum(row["source_surface"] == "ADOPTED_RELEASE_TEXT" for row in source_claims),
            "ground_not_found_route_rows": 0,
            "scope_ids": [
                row["scope_id"] for row in scope
                if row["source_surface"] == "ADOPTED_RELEASE_TEXT"
            ],
            "rule": "Every classified adopted-release claim occurrence has exactly one scope row; bibliography and V1021 reference-ledger self-report claims remain separate authority classes; lexical cite/numeric rows are navigation only.",
        },
        "reference_ledger_self_report_inventory": reference_ledger_inventory(decoded),
        "bibliography_audit": {
            "rows": bib_rows, "metadata_observations": metadata_rows(bib_rows),
            "denominators": {"total": 28, "LCO": 14, "SI": 14, "resolved_metadata_match": 27, "conflicting_identifier": 1},
            "authority_rule": "Bibliography existence and resolver metadata never prove the cited proposition.",
            "publisher_proposition_observations": [
                {
                    "key": "swiderska2019", "tier": "PUBLISHER", "source_part": "publisher abstract",
                    "url": "https://pubs.rsc.org/en/content/articlelanding/2019/cp/c8cp06638h/unauth",
                    "confirmed_values": {"absolute_LCO_single_electrode_mV_per_K": 0.83, "isothermal_Li_LCO_cell_mV_per_K": -0.25, "absolute_Li_single_electrode_mV_per_K": 1.03},
                    "scope": "numeric distinction only; not a full-text audit",
                },
                {
                    "key": "limthongkul2003", "tier": "PUBLISHER", "source_part": "publisher title/abstract record",
                    "url": "https://www.sciencedirect.com/science/article/pii/S1359645402005141",
                    "confirmed_values": {"correct_doi": "10.1016/S1359-6454(02)00514-1", "pages": "1103-1113"},
                    "scope": "identifier/title/amorphization abstract only",
                },
            ],
        },
        "citation_occurrences": citations,
        "citation_denominators": {
            "total": len(citations), "LCO": sum(row["material_group"] == "LCO" for row in citations),
            "SI": sum(row["material_group"] == "SI" for row in citations),
        },
        "source_line_inventory": source_line_inventory(decoded),
        "source_claim_manifest": source_claims,
        "source_claim_coverage": source_claim_coverage,
        "q6_lco_audit": q6_audit(),
        "q7_si_audit": q7_audit(snapshot),
        "scope_matrix": scope,
        "ground_not_found_records": gnf_rows,
        "material_claim_contract": {
            "source_claim_denominator": len(source_claims),
            "scope_row_denominator": len(scope),
            "scope_id_first": "P062-SCOPE-0001",
            "scope_id_last": f"P062-SCOPE-{len(scope):04d}",
            "ground_not_found_denominator": len(gnf_rows),
            "lexical_inventory_is_navigation_only": True,
            "source_claim_to_scope_bijection": (
                len(source_claims) == len(scope)
                and {row["source_claim_id"] for row in source_claims}
                == {row["source_claim_id"] for row in scope}
                and all(row["route_kind"] == "SCOPE" for row in source_claims)
            ),
            "every_scope_row_has_exact_anchor": all(row["claim_anchor"] is not None for row in scope),
            "all_ground_not_found_records_linked_once": sorted(linked_gnf) == sorted(gnf_ids),
            "claim_counts_by_path": claim_path_counts,
        },
        "routing_summary": {
            "71": "bibliographic identity, DOI, publisher/fulltext and exact proposition anchors",
            "74": "charge, coordinate, capacity, unit, reaction basis and sign",
            "75": "conditional grand-canonical/equilibrium inversion",
            "76": "TST and material-specific kinetics",
            "78": "LCO thermodynamics, structure, electronic/vibrational and experimental scope",
            "79": "Si, SiOx and Si-C thermodynamics/chemo-mechanics",
            "80": "graphite-Si blend allocation and coupling",
            "82": "final equation/domain/source adjudication",
        },
        "findings": finding_rows,
        "finding_summary": {"P0": 0, "P1": 8, "P2": 8},
        "negative_control_contract": {
            "required_ids": REQUIRED_NEGATIVE_CONTROLS,
            "required_count": len(REQUIRED_NEGATIVE_CONTROLS),
            "execution_requirement": "VALIDATOR_EXECUTES_EVERY_REAL_MUTATION_SUBFIXTURE_AND_REQUIRES_SINGLETON_DIAGNOSTIC_PER_ID",
            "stored_pass_claim": False,
        },
    }
    data["semantic_sha256"] = sha256(json_bytes(semantic_projection(data)))
    q6 = data["q6_lco_audit"]
    q7 = data["q7_si_audit"]
    md = f"""# Phase 062 Step 54 - v1.0.21 LCO/Si literature, unit, and scope audit

## Outcome

Status: **PASS_WITH_CONCERNS**
Gate: `PASS_P062_STEP54_LCO_SI_SCOPE_WITH_CONCERNS`

Step 54 closes the audit inventory and routing scope; it does **not** accept the frozen LCO/Si science as canonical. The frozen release remains untouched. External scientific truth validated: **false**. External material and experimental truth validated: **false**.

## Full-read and inventory coverage

- Direct READ_FULL attestations: **{len(attestations)}** files, each pinned by commit, Git blob, byte SHA-256, and 1-EOF line coverage.
- Frozen material bibliography: **28/28** rows (**14 LCO + 14 Si**).
- DOI/resolver metadata: **27** matched records and **1 conflicting identifier**.
- Relevant cite-key occurrences in the release: **{len(citations)}** (**{data['citation_denominators']['LCO']} LCO + {data['citation_denominators']['SI']} Si**).
- Lexical cited/numeric source-line inventory: **{len(data['source_line_inventory'])}** rows. This inventory is not proposition proof; load-bearing use requires a curated scope row.
- Atomic source-claim manifest and scope matrix: **{len(source_claims)} / {len(scope)}** rows, exact 1:1 claim-to-scope bijection. Adopted release text contributes **{data['adopted_release_text_inventory']['claim_row_denominator']}** claim atoms; bibliography **28** and reference-ledger self-report **{len(REFERENCE_LEDGER_CLAIM_LINES)}** remain separate authority classes.
- All **{sum(item['physical_lines'] for item in source_claim_coverage)}** physical lines across the eight LCO sections, AppA and AppD were classified exactly once. Pure formatting, environment boundaries, comments and blanks are excluded; scientific TikZ node/draw/axis commands are retained as load-bearing claims.
- Adopted-text claim atoms by path: sec11 **{claim_path_counts[CLAIM_TEXT_PATHS[0]]}**, sec12 **{claim_path_counts[CLAIM_TEXT_PATHS[1]]}**, sec13 **{claim_path_counts[CLAIM_TEXT_PATHS[2]]}**, sec14 **{claim_path_counts[CLAIM_TEXT_PATHS[3]]}**, sec15 **{claim_path_counts[CLAIM_TEXT_PATHS[4]]}**, sec16 **{claim_path_counts[CLAIM_TEXT_PATHS[5]]}**, sec17 **{claim_path_counts[CLAIM_TEXT_PATHS[6]]}**, sec18 **{claim_path_counts[CLAIM_TEXT_PATHS[7]]}**, AppA **{claim_path_counts[CLAIM_TEXT_PATHS[8]]}**, AppD **{claim_path_counts[CLAIM_TEXT_PATHS[9]]}**.
- Explicit frozen-release GNF records: **{len(gnf_rows)}**; lexical cite/numeric inventory remains navigation only.
- V1021 reference-ledger self-report inventory: **{data['reference_ledger_self_report_inventory']['statement_denominator']}** exact statements, independently classified from adopted release text.
- Q6/Q7 strict snapshot traversal: Q6 **{snapshot['q6']['traversal']['nodes']}** nodes, Q7 **{snapshot['q7']['traversal']['nodes']}** nodes.

## Decisive LCO findings

1. The publisher abstract for Swiderska distinguishes **+0.83 mV/K** as an inferred absolute LCO single-electrode coefficient from the isothermal **Li|LCO cell coefficient -0.25 mV/K**. The frozen text calls +0.83 a vs-Li half-cell quantity and derives about +80 J/(mol K); that basis/sign transfer is rejected. The corresponding narrow isothermal cell conversion is `F*(-0.25e-3) = -24.12125 J/(mol K)`, subject to Phase 74 reaction-direction adjudication.
2. Q6's slot arithmetic is internally reproducible: `Delta S_e={q6['slot_arithmetic']['delta_S_e_J_per_mol_K']:.9f} J/(mol K)`, `Delta S_eff={q6['slot_arithmetic']['delta_S_eff_J_per_mol_K']:.9f} J/(mol K)`, and `{q6['slot_arithmetic']['slot_slope_mV_per_K']:.9f} mV/K`. The **1.1 k_B/atom model gate integral/complete-metal electronic entropy** is a different quantity from the **0.18 k_B/atom O3 total partial-molar quantity**; their unit, basis, meaning, and evidence gaps are separate rows.
3. The `x_bar=0.50` row is not gate-off. `x_bar` is the global delithiation fraction, while the electronic term is evaluated at the T1 transition's fixed `x_center=0.85`. Independent same-formula recomputation gives gate ON/OFF at x_bar=0.50: `U=3.924249955/4.042610795 V`, slope `-0.312434776/-0.034630812 mV/K`.
4. The reported -91 mV ON/OFF shift holds the electronic-absorbed T1 enthalpy fixed. Reanchoring the gate-off T1 to 3.930 V at Tref changes the x_bar=0.85 voltage by only `{q6['reanchored_gate_off_at_x_bar_0_85']['delta_U_oc_mV']:.9f} mV`; the same-dH shift is not an isolated physical gate effect.
5. Tier-C one-point arithmetic is separated from missing multi-temperature reconstruction, irreversible heat, doped/high-voltage LCO, oxygen redox/loss, structural-transition validation, and experiment. Production output is not scientific authority.

## Decisive Si findings

1. The frozen Limthongkul DOI `10.1016/S1359-6454(02)00515-4` does not identify the cited paper. The matching record is **10.1016/S1359-6454(02)00514-1**, Acta Materialia 51(4), 1103-1113. The frozen row is preserved as evidence and routed to Phase 71 for correction.
2. Q6 to Q7 Ch1 labels are **247 -> 254**, or **+7**. The change log and execution ledger say +6 and 1:1 PASS; that structural claim is conflicting.
3. General charge accounting survives, but exact logistic-weighted inversion and uniqueness are conditional on noninteracting site classes. Verbrugge 2016 equations 2-7 explicitly state this assumption; the bridgehead's electrode-neutral promotion is rejected.
4. The approximately 55 mV value at `Omega=4RT` is not a global regular-solution upper bound over Omega. It is only the fixed-Omega branch bound (and gamma<=1 branch scaling).
5. The blanket “mechanical contribution is dominant” wording is stronger than the narrow sources, and Eyring-tail universality has no Si-specific source or derivation.
6. No Si-specific governing equation in v1.0.21: **No Si-specific governing equation** was added (`equation-block delta = {snapshot['added_equation_blocks']}`). Free energy, stress chemical potential, plasticity/damage, interface/SEI, hysteresis, SiOx, Si-C, and blend allocation remain missing and routed.

## Findings and authority ceiling

- P0/P1/P2: **0/8/8**.
- `PASS_WITH_CONCERNS` means the inventory, internal arithmetic checks, contradictions, and owner routing are complete enough for downstream repair. It is not a scientific/material PASS.
- Required actual-mutation negative controls: **{len(REQUIRED_NEGATIVE_CONTROLS)}/{len(REQUIRED_NEGATIVE_CONTROLS)} contract cases**, including a missing source claim and a duplicate/multi-mapped source claim. The precommit validator must execute every case and report singleton rejection; no stored `ENFORCED` string is accepted as evidence.
- Validator-only staged/index and CRLF identity boundary controls: **2/2**. They do not mutate the real Git index or repository files.
- Primary owners are Phase 71/74/75/76/78/79/80/82 as recorded in the matrix. Phase 82 owns final equation and validity-domain freezing.

## Validation and recovery record

- Builder SHA-256: `{data['builder_sha256']}`
- Artifact semantic SHA-256: `{data['semantic_sha256']}`
- Expected parent: `{EXPECTED_PARENT}`
- Q6/Q7 commits: `{Q6_COMMIT}` / `{Q7_COMMIT}`
- External observation date: `{CHECKED_DATE}`
- Result-first sentinel: `P062_STEP54_RESULT_FIRST_PRECOMMIT`
- Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN` (persistence is not claimed)

This result was generated before the machine matrix under the result-first precommit contract. Both execution ledgers and the active handover complete the Step 54 recovery set. Commit/push and persistence verification are separate gate actions; Step 55 remains blocked until `PASS_P062_STEP54_PERSISTENCE`.
"""
    return data, md


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data, md = build()
    raw_json = json_bytes(data)
    raw_md = md.encode("utf-8")
    if args.check:
        if not OUTPUT_JSON.is_file() or not OUTPUT_MD.is_file():
            print("FAIL_P062_STEP54_DETERMINISM missing output")
            return 1
        with tempfile.TemporaryDirectory(prefix="p062-step54-result-first-") as tmp:
            temp_root = Path(tmp)
            temp_result = temp_root / OUTPUT_MD.name
            temp_json = temp_root / OUTPUT_JSON.name
            if temp_json.exists():
                raise RuntimeError("fresh result-first temp JSON unexpectedly exists")
            temp_result.write_bytes(raw_md)
            result_first_observed = temp_result.is_file() and not temp_json.exists()
            temp_json.write_bytes(raw_json)
            if not result_first_observed:
                print("FAIL_P062_STEP54_DETERMINISM result-first chronology")
                return 1
            if temp_result.read_bytes() != OUTPUT_MD.read_bytes() or temp_json.read_bytes() != OUTPUT_JSON.read_bytes():
                print("FAIL_P062_STEP54_DETERMINISM byte drift")
                return 1
        print("PASS_P062_STEP54_DETERMINISM outputs=2/2 result_first=RESULT_THEN_JSON")
        return 0
    # Task 54D requires the human recovery result to exist before its machine
    # companion is materialized.  The containing commit remains explicitly
    # pending; write chronology is not persistence evidence.
    OUTPUT_MD.write_bytes(raw_md)
    print(f"WROTE {OUTPUT_MD.relative_to(ROOT).as_posix()}")
    if data["result_first_contract"]["sentinel"] != "P062_STEP54_RESULT_FIRST_PRECOMMIT":
        raise RuntimeError("result-first sentinel drift")
    OUTPUT_JSON.write_bytes(raw_json)
    print(f"WROTE {OUTPUT_JSON.relative_to(ROOT).as_posix()}")
    print(f"citations={len(data['citation_occurrences'])} scope_rows={len(data['scope_matrix'])}")
    print("result_first=RESULT_THEN_JSON persistence_claimed=false")
    print(data["gate"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
