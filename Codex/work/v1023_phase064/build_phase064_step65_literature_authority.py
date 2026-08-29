from __future__ import annotations

import hashlib
import json
import math
import pathlib
import subprocess
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[3]
RESULT_PATH = "Codex/results/PHASE_064_STEP_065_LITERATURE_AUTHORITY_RESULT.md"
MATRIX_PATH = "Codex/results/PHASE_064_V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX.json"
ATTESTATION_PATH = "Codex/results/PHASE_064_V1023_LITERATURE_READ_ATTESTATION.json"
JCP_PDF_PATH = "Claude/JCP_147(14)_144111_(2017) - Effects of external electric field.pdf"
JCP_EXTRACT_PATH = "Claude/jcp_extract.txt"
BIB_PATH = "Claude/docs/v1.0.23/_sections/ch1v22_bib.tex"
GATE = "PASS_P064_STEP65_LITERATURE_BOUNDED_GNF"
STATUS = "PASS_PENDING_PERSISTENCE_WITH_GROUND_NOT_FOUND"
AUTHORITY_CEILING = "CONDITIONAL_P064_REF7_ORIGINAL_FULL_TEXT_GROUND_NOT_FOUND"
EXPECTED_PARENT = "fd8e192f031bb302933d925ceb9ba599a7975837"
EXPECTED_SUBJECT = "audit(phase064): bound v1023 literature authority"
BEGIN = "<!-- P064_STEP65_HUMAN_EVIDENCE_BEGIN -->"
END = "<!-- P064_STEP65_HUMAN_EVIDENCE_END -->"

EXPECTED_SOURCE_CONTRACTS = {
    "JCP147": {
        "title": "Effects of external electric field and anisotropic long-range reactivity on charge separation probability",
        "authors": ["Kyusup Lee", "Seonghoon Lee", "Cheol Ho Choi", "Sangyoub Lee"],
        "journal": "The Journal of Chemical Physics", "volume": "147", "issue": "14",
        "article_number": "144111", "year": 2017, "doi": "10.1063/1.5000882",
        "original_full_text_status": "FULL_TEXT_READ", "authority_tier": "PRIMARY_VOR_FULL_TEXT",
        "raw_sha256": "47c7c415093bf5e3ee78215d6efa9141e4cd574e74e206cd9e3e863c5da85bd9",
        "bytes": 2075558, "pages": 10, "pages_read": 10,
    },
    "REF6": {
        "title": "Communication: Propagator for diffusive dynamics of an interacting molecular pair",
        "authors": ["Sangyoub Lee", "Chang Yun Son", "Jaeyoung Sung", "Song-Ho Chong"],
        "journal": "The Journal of Chemical Physics", "volume": "134", "issue": "12",
        "article_number": "121102", "year": 2011, "doi": "10.1063/1.3565476",
        "original_full_text_status": "FULL_TEXT_READ", "authority_tier": "PRIMARY_VOR_FULL_TEXT",
        "raw_sha256": "c0f2dbefa26731581235da28477f19f07f81f1e897523f6144e272f6b0959460",
        "bytes": 258112, "pages": 4, "pages_read": 4,
    },
    "REF7": {
        "title": "An accurate expression for the rates of diffusion-influenced bimolecular reactions with long-range reactivity",
        "authors": ["Chang Yun Son", "Jaehoon Kim", "Ji-Hyun Kim", "Jun Soo Kim", "Sangyoub Lee"],
        "journal": "The Journal of Chemical Physics", "volume": "138", "issue": "16",
        "article_number": "164123", "year": 2013, "doi": "10.1063/1.4802584",
        "original_full_text_status": "GROUND_NOT_FOUND", "authority_tier": "OFFICIAL_BIBLIOGRAPHIC_METADATA_ONLY",
        "raw_sha256": None, "bytes": None, "pages": None, "pages_read": 0,
    },
}
EXPECTED_ACCESS_CONTRACTS = {
    "JCP147": {
        "access_url": "local Git blob plus https://doi.org/10.1063/1.5000882",
        "license_status": "AIP_COPYRIGHT_NO_OPEN_REUSE_LICENSE_ASSERTED",
    },
    "REF6": {
        "access_url": "https://aipp.silverchair-cdn.com/aipp/content_public/journal/jcp/134/12/10.1063_1.3565476/4/121102_1_online.pdf",
        "license_status": "AIP_COPYRIGHT_REUSE_LICENSE_NOT_LOCATED",
    },
    "REF7": {
        "access_url": "https://pubs.aip.org/aip/jcp/article/138/16/164123/71188/An-accurate-expression-for-the-rates-of-diffusion",
        "license_status": "CROSSREF_LICENSE_NULL_AIP_PURCHASE_ROUTE",
    },
}
EXPECTED_EQUATION_CONTRACTS = [
    {"equation": "32", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [277, 299], "context_locator_sha256": "ab26cc49eab8969516378a38fb4b95772947aeb97e60b8334d4c917d136716fe", "pdf_bbox_points": [44, 76, 289, 156], "pixel_box_300dpi": [183, 316, 1205, 650], "crop_width": 1022, "crop_height": 334, "crop_mode": "RGB", "crop_raw_pixel_sha256": "9b4bbf896f7d25f30a1ba465942582ee3baf9b002990c5edd8caf97f1fda2a08", "semantic_projection": "EQ32|upstream=EQ19_EQ20_orientation_average_approximation|unknown=Wbar_u(r)|operator=fredholm_second_kind|domains=sigma_to_r+r_to_infinity|kernel=chi*radial_sink*boltzmann_weight", "semantic_projection_sha256": "7a8f428a1754e8c34d8e00461ba81c3041164291df7f94eaf15e008e0b591941", "operation": "EXACT_WITHIN_EQ19_EQ20_APPROXIMATED_SYSTEM"},
    {"equation": "33", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [299, 325], "context_locator_sha256": "e6ca93fa04645e684e3169c4159c78664a67271ee4212612cfb8564b3e1e18f4", "pdf_bbox_points": [44, 195, 289, 265], "pixel_box_300dpi": [183, 812, 1205, 1105], "crop_width": 1022, "crop_height": 293, "crop_mode": "RGB", "crop_raw_pixel_sha256": "250261fbd54b8ef41aae5cffc5458dd766a18bcda6b4da55e33df75f1b4c1af3", "semantic_projection": "EQ33|operation=algebraic_rearrangement_of_EQ32_within_EQ19_EQ20_approximated_system|form=inverse_one_plus_two_ratio_integrals|unknown_ratio=Wbar_u(r1)/Wbar_u(r)", "semantic_projection_sha256": "6154097a54b55d4986f75506d94d201bb0bb115511010baebef3036c8fdf2694", "operation": "FORMALLY_EXACT_REARRANGEMENT_WITHIN_EQ32"},
    {"equation": "34", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [321, 340], "context_locator_sha256": "662ed8054ff5c9fa600b03448dad03d7e131965429d182097eb94c006ba50d8e", "pdf_bbox_points": [95, 390, 289, 409], "pixel_box_300dpi": [395, 1625, 1205, 1705], "crop_width": 810, "crop_height": 80, "crop_mode": "RGB", "crop_raw_pixel_sha256": "93a60a6ea82c6953ae8be893a80bebe7164f2da8f7521ee43bd551f0ea700924", "semantic_projection": "EQ34|closure=replace_unknown_ratio|from=Wbar_u(r1)/Wbar_u(r)|to=Wbar_delta_u(r1)/Wbar_delta_u(r)", "semantic_projection_sha256": "b00bae5cbf79cc55c98c756607999df69379ea53c5cb66e72d06057db07b0ab6", "operation": "REFERENCE_RATIO_APPROXIMATION"},
    {"equation": "35", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [339, 351], "context_locator_sha256": "80ee9beb12075836b0d321f9a465c2cd7c9edf5b0c81af8e06b35bfef1ced722", "pdf_bbox_points": [64, 468, 289, 500], "pixel_box_300dpi": [266, 1950, 1205, 2084], "crop_width": 939, "crop_height": 134, "crop_mode": "RGB", "crop_raw_pixel_sha256": "e67bd01b9ddcd9648e66e6dbd0ed10488ad6552f3d6a1f708a6d1c62ca54a52b", "semantic_projection": "EQ35|definition=equal_boltzmann_weighted_integrated_reactivity|contact_sink=delta(r-sigma)*kappa(mu)/(4*pi*sigma^2)|long_range_sink=S_R(r,mu)", "semantic_projection_sha256": "edb4ab6f329c9e3d91e51ff1175f10a389b0a1c7032a6d72603cc2f93df0f510", "operation": "CONTRACTED_REACTIVITY_MATCH"},
    {"equation": "36", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [351, 359], "context_locator_sha256": "c28c7e8fe442b5cb39ad7798c1d56362e816a0cdc408c1273904aea5583192fb", "pdf_bbox_points": [44, 524, 289, 553], "pixel_box_300dpi": [183, 2183, 1205, 2305], "crop_width": 1022, "crop_height": 122, "crop_mode": "RGB", "crop_raw_pixel_sha256": "26299e3e157ff4edea2481586d9581cb8765c47bac5d4b20e52babd923fea2da", "semantic_projection": "EQ36|solves=EQ35_for_kappa(mu)|integral=4*pi*exp(U1(sigma))*integral_0_infinity[r^2*S_R(r,mu)*exp(-U1(r))dr]", "semantic_projection_sha256": "7e2435e0601ec7644f528b942f856046c516c83fd3d5e5d842c69987f60c948d", "operation": "DERIVED_CONTACT_REACTIVITY"},
    {"equation": "37", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [359, 371], "context_locator_sha256": "73966d067e87b847197bff2a443c7d3bba1690bc4a2b754401ce182d51018708", "pdf_bbox_points": [44, 592, 289, 630], "pixel_box_300dpi": [183, 2466, 1205, 2625], "crop_width": 1022, "crop_height": 159, "crop_mode": "RGB", "crop_raw_pixel_sha256": "bee5dcb83848b11197bd0620458656eb27bcc41352d9b11df91e4189f9e26b43", "semantic_projection": "EQ37|approximation=EQ34_with_EQ25|ratio=delta_sink_survival_ratio|parameters=kappa(mu),D,sigma,chi", "semantic_projection_sha256": "224fe0d58fcdfa611a8d5d36f79d3667971671465db7904437af2d14c892a056", "operation": "REFERENCE_RATIO_EVALUATION"},
    {"equation": "38", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [371, 378], "context_locator_sha256": "00efd93d95945d8f9813479b39e7dc00223b6c7ded44eac3b8c4d8a67929122c", "pdf_bbox_points": [44, 660, 289, 695], "pixel_box_300dpi": [183, 2750, 1205, 2896], "crop_width": 1022, "crop_height": 146, "crop_mode": "RGB", "crop_raw_pixel_sha256": "63946340028fd9d4dac21dd6f8853aa536a0291923b02e2c774fba3a90771978", "semantic_projection": "EQ38|definition=Lambda_rx|integral=4*pi*exp(U1(sigma))*integral_0_infinity[r^2*exp(-U1(r))*angular_average(exp(K*r*mu)*S_R(r,mu))dr]", "semantic_projection_sha256": "2c34839ea0f6ab76386ed21c8c4fc76ca68acf5f17dc5cf1f5e544da9721d83b", "operation": "CONTRACTED_REACTIVITY_DEFINITION"},
    {"equation": "39", "pdf_page": 5, "printed_page": "144111-4", "context_interval": [277, 300], "context_locator_sha256": "65eb943abec1e527efa27e8e692632702fd5bff722dae7e7a75df0920c10ae85", "pdf_bbox_points": [305, 76, 551, 138], "pixel_box_300dpi": [1270, 316, 2296, 575], "crop_width": 1026, "crop_height": 259, "crop_mode": "RGB", "crop_raw_pixel_sha256": "2c08f7a419fc83fcd1475519e98db2a91d27096fe03706d71fff1397e18a6b7f", "semantic_projection": "EQ39|result=approximate_orientation_averaged_ultimate_survival|form=inverse_one_plus_two_radial_integrals|uses=chi,Lambda,EQ37_ratio", "semantic_projection_sha256": "12909edebe442070b6a16a5372ae0f13db350c5b1957086671f2787ea320b807", "operation": "APPROXIMATE_CLOSED_EXPRESSION"},
]
EXPECTED_UPSTREAM = {"equations": ["19", "20"], "pdf_page": 4, "printed_page": "144111-3", "context_interval": [223, 241], "context_locator_sha256": "d56658f43a8751f0a367441f5eeb05988b38aa9a51450c0190d3a3d29da4c6f0", "claim": "direction-resolved survival probabilities are replaced by their orientation average when angular dependence is weak", "downstream_equations": ["21", "22", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]}
EXPECTED_CONDITIONS = [
    {"id": "JCP147-COND-1", "claim": "anisotropic external electric field is not too large", "pdf_page": 6, "printed_page": "144111-5", "extract_interval": [398, 411]},
    {"id": "JCP147-COND-2", "claim": "Onsager distance r_c is large compared with initial separation r", "pdf_page": 6, "printed_page": "144111-5", "extract_interval": [398, 411]},
    {"id": "JCP147-COND-3", "claim": "contact inherent reactivity kappa is small", "pdf_page": 6, "printed_page": "144111-5", "extract_interval": [398, 411]},
]
EXPECTED_DEGRADATION = {"id": "JCP147-DEGRADE-1", "claim": "Eq. 34 reference-ratio accuracy worsens when the reaction zone becomes very broad", "pdf_page": 5, "printed_page": "144111-4", "extract_interval": [380, 388], "raw_slice_sha256": "9d3c57ad152aa5ca9db8389f8fda03bd467353e5e29e05b979d60315b6a70aca"}
EXPECTED_CONFLICTS = [{"id": "P064-LIT-CONFLICT-001", "candidate_ref7_doi": "10.1063/1.4802005", "disposition": "REJECT_AS_REF7_DOI", "actual_article_number": "164906", "actual_title": "The isotropic-to-nematic phase transition in hard helices: Theory and simulation", "authoritative_routes": ["https://doi.org/10.1063/1.4802005", "https://pubs.aip.org/aip/jcp/article/138/16/164906/71301/The-isotropic-to-nematic-phase-transition-in-hard", "https://api.crossref.org/works/10.1063%2F1.4802005"]}]
EXPECTED_READERS = [
    {"reader": "controller", "scope": "JCP147 PDF 10/10; Ref6 official VOR 4/4; official metadata/access routes; integration"},
    {"reader": "Kierkegaard", "scope": "JCP147 PDF 10/10 and extract 1-725"},
    {"reader": "Leibniz", "scope": "Ref6 VOR PDF 4/4, full HTML 1-974 and lawful acquisition routes"},
    {"reader": "Singer", "scope": "Ref7 official metadata, lawful acquisition routes and wrong-DOI negative control"},
]
EXPECTED_BIBLIOGRAPHY_SOURCES = {
    "adopted_bibliography": {
        "path": "Claude/docs/v1.0.23/_sections/ch1v22_bib.tex",
        "blob_sha1": "3f7d417962fb5fced5b420d5e081b2dcabc901d0",
        "raw_sha256": "d0dd060fd635dd9fe1c32c872357d4ce85f106866cf8c378906067f85c5fc9d1",
        "line_interval": [45, 47],
        "raw_slice_sha256": "88f02551a06f7d2fdb7d700606b8f96c15c2dfdccb5220ff0ed46a98ceb2c7ef",
    },
    "jcp147_reference_list": {
        "path": "Claude/jcp_extract.txt",
        "line_interval": [711, 714],
        "ref6_slice_sha256": "69d9a62c07726d929ff95702a65560192d1123b713573485836887239c481219",
        "ref7_slice_sha256": "9b58deba54b319508ae7c95b20e449a2bd4c9a797dad1a52600a8190cc5b3726",
    },
}


class BuildError(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise BuildError(f"{code}: {detail}" if detail else code)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def semantic_sha(value: dict[str, Any]) -> str:
    payload = {key: item for key, item in value.items() if key != "semantic_sha256"}
    return sha256(canonical(payload))


def bind_semantic_sha(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = semantic_sha(value)
    return value


def git_text(args: list[str]) -> str:
    process = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    require(process.returncode == 0, "E_GIT", process.stderr.decode("utf-8", errors="replace")[-600:])
    return process.stdout.decode("utf-8").strip()


def raw_slice_sha(path: pathlib.Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    require(1 <= start <= end <= len(lines), "E_SLICE_RANGE", f"{path}:{start}-{end}/{len(lines)}")
    return sha256(b"".join(lines[start - 1 : end]))


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, "E_EVIDENCE_DUPLICATE_KEY", key)
        value[key] = item
    return value


def reject_constant(value: str) -> Any:
    raise BuildError(f"E_EVIDENCE_NONFINITE: {value}")


def finite_float(value: str) -> float:
    result = float(value)
    require(math.isfinite(result), "E_EVIDENCE_NONFINITE", value)
    return result


def load_human_evidence() -> dict[str, Any]:
    text = (ROOT / RESULT_PATH).read_text(encoding="utf-8")
    require(text.count(BEGIN) == 1 and text.count(END) == 1, "E_EVIDENCE_MARKERS")
    block = text.split(BEGIN, 1)[1].split(END, 1)[0]
    start = block.find("{")
    finish = block.rfind("}")
    require(start >= 0 and finish > start, "E_EVIDENCE_JSON_BOUNDARY")
    try:
        evidence = json.loads(
            block[start : finish + 1], object_pairs_hook=unique_pairs,
            parse_constant=reject_constant, parse_float=finite_float,
        )
    except (json.JSONDecodeError, OverflowError) as error:
        raise BuildError("E_EVIDENCE_JSON") from error
    require(type(evidence) is dict, "E_EVIDENCE_ROOT")
    return evidence


def validate_evidence(evidence: dict[str, Any]) -> None:
    require(evidence.get("evidence_id") == "P064-HUMAN-LITERATURE-STEP65-001", "E_EVIDENCE_ID")
    require(evidence.get("evidence_date") == "2026-08-29", "E_EVIDENCE_DATE")
    require(evidence.get("access_date") == "2026-08-29", "E_ACCESS_DATE")
    require(evidence.get("authority_ceiling") == AUTHORITY_CEILING, "E_AUTHORITY_CEILING")
    require(evidence.get("source_mutation_count") == 0, "E_SOURCE_MUTATION")
    require(evidence.get("bibliography_sources") == EXPECTED_BIBLIOGRAPHY_SOURCES, "E_BIBLIOGRAPHY_SOURCE_CONTRACT")

    sources = evidence.get("sources")
    require(type(sources) is list and len(sources) == 3 and all(type(row) is dict for row in sources), "E_SOURCE_COUNT")
    source_ids = [row.get("source_id") for row in sources]
    require(all(type(source_id) is str for source_id in source_ids), "E_SOURCE_ID_TYPE")
    by_id = {row["source_id"]: row for row in sources}
    require(set(by_id) == {"JCP147", "REF6", "REF7"}, "E_SOURCE_IDS")
    for source_id, expected in EXPECTED_SOURCE_CONTRACTS.items():
        row = by_id[source_id]
        expected_keys = {"source_id", *expected, *EXPECTED_ACCESS_CONTRACTS[source_id]}
        require(set(row) == expected_keys, "E_SOURCE_SCHEMA", source_id)
        observed = {key: row.get(key) for key in expected}
        require(observed == expected, "E_SOURCE_IDENTITY", source_id)
    for source_id, expected in EXPECTED_ACCESS_CONTRACTS.items():
        observed = {key: by_id[source_id].get(key) for key in expected}
        require(observed == expected, "E_SOURCE_ACCESS_CONTRACT", source_id)

    equations = evidence.get("equations")
    require(equations == EXPECTED_EQUATION_CONTRACTS, "E_EQUATION_CONTRACT")
    for row in equations:
        number = row["equation"]
        require(sha256(row.get("semantic_projection", "").encode("utf-8")) == row.get("semantic_projection_sha256"), "E_EQUATION_SEMANTIC_SHA", number)
        interval = row.get("context_interval")
        require(type(interval) is list and len(interval) == 2, "E_EQUATION_INTERVAL", number)
        require(raw_slice_sha(ROOT / JCP_EXTRACT_PATH, interval[0], interval[1]) == row.get("context_locator_sha256"), "E_EQUATION_CONTEXT_LOCATOR", number)

    conditions = evidence.get("jcp147_conditions")
    require(conditions == EXPECTED_CONDITIONS, "E_CONDITIONS")
    require(raw_slice_sha(ROOT / JCP_EXTRACT_PATH, 398, 411) == "a31e6008b0862eda58ad5072c18b18af7f0f6e093a7eb30340ef5853c067390b", "E_CONDITION_SLICE")
    degradation = evidence.get("jcp147_degradation")
    require(degradation == EXPECTED_DEGRADATION, "E_DEGRADATION")
    require(raw_slice_sha(ROOT / JCP_EXTRACT_PATH, 380, 388) == degradation.get("raw_slice_sha256"), "E_DEGRADATION_SLICE")

    upstream = evidence.get("jcp147_upstream_approximations")
    require(upstream == EXPECTED_UPSTREAM, "E_UPSTREAM_APPROXIMATION")
    require(raw_slice_sha(ROOT / JCP_EXTRACT_PATH, 223, 241) == upstream.get("context_locator_sha256"), "E_UPSTREAM_CONTEXT_LOCATOR")

    conflicts = evidence.get("conflicts")
    require(conflicts == EXPECTED_CONFLICTS, "E_CONFLICT_CONTRACT")
    require(evidence.get("readers") == EXPECTED_READERS, "E_READER_CONTRACT")


def validate_local_sources(evidence: dict[str, Any]) -> None:
    jcp_pdf = ROOT / JCP_PDF_PATH
    extract = ROOT / JCP_EXTRACT_PATH
    bibliography = ROOT / BIB_PATH
    require(sha256(jcp_pdf.read_bytes()) == "47c7c415093bf5e3ee78215d6efa9141e4cd574e74e206cd9e3e863c5da85bd9", "E_JCP_PDF_BYTES")
    require(sha256(extract.read_bytes()) == "cfd8e9f86c2e7937fc648971d455a6a1cd2fb4da4cc5ced48b50f5826f11e6e9", "E_JCP_EXTRACT_BYTES")
    require(sha256(bibliography.read_bytes()) == "d0dd060fd635dd9fe1c32c872357d4ce85f106866cf8c378906067f85c5fc9d1", "E_BIB_BYTES")
    require(git_text(["hash-object", JCP_PDF_PATH]) == "4fbe2b91b2b3f62cea76feb4272b1e3275dab986", "E_JCP_BLOB")
    require(git_text(["hash-object", JCP_EXTRACT_PATH]) == "2588ac5da0e9ce4c25141f302a1e33e460ff7966", "E_EXTRACT_BLOB")
    require(git_text(["hash-object", BIB_PATH]) == "3f7d417962fb5fced5b420d5e081b2dcabc901d0", "E_BIB_BLOB")
    bibliography_source = evidence["bibliography_sources"]["adopted_bibliography"]
    require(raw_slice_sha(bibliography, 45, 47) == bibliography_source.get("raw_slice_sha256"), "E_BIB_SLICE")
    reference_source = evidence["bibliography_sources"]["jcp147_reference_list"]
    require(raw_slice_sha(extract, 711, 712) == reference_source.get("ref6_slice_sha256"), "E_REF6_REFERENCE_SLICE")
    require(raw_slice_sha(extract, 713, 714) == reference_source.get("ref7_slice_sha256"), "E_REF7_REFERENCE_SLICE")


def build_matrix(evidence: dict[str, Any]) -> dict[str, Any]:
    sources = []
    for row in evidence["sources"]:
        sources.append({
            "source_id": row["source_id"],
            "bibliographic_identity": {
                "title": row["title"], "authors": row["authors"], "journal": row["journal"],
                "volume": row["volume"], "issue": row["issue"], "article_number": row["article_number"],
                "year": row["year"], "doi": row["doi"],
            },
            "authority": {
                "tier": row["authority_tier"], "original_full_text_status": row["original_full_text_status"],
                "raw_sha256": row["raw_sha256"], "bytes": row["bytes"], "pages": row["pages"],
                "pages_read": row["pages_read"], "access_url": row["access_url"],
                "license_status": row["license_status"],
            },
            "allowed_use": (
                "EQUATION_LEVEL_METHOD_CONTENT" if row["original_full_text_status"] == "FULL_TEXT_READ"
                else "BIBLIOGRAPHIC_METADATA_ONLY"
            ),
        })
    matrix = {
        "schema_version": "1.0.0",
        "artifact_kind": "V1023_JCP147_REF6_REF7_AUTHORITY_MATRIX",
        "phase": 64,
        "step": 65,
        "gate": GATE,
        "status": STATUS,
        "authority_ceiling": AUTHORITY_CEILING,
        "sources": sources,
        "equation_chain": evidence["equations"],
        "applicability": {
            "upstream_approximations": evidence["jcp147_upstream_approximations"],
            "conditions": evidence["jcp147_conditions"],
            "degradation": evidence["jcp147_degradation"],
            "equation_crop_provenance": {"source_raw_sha256": "47c7c415093bf5e3ee78215d6efa9141e4cd574e74e206cd9e3e863c5da85bd9", "pdf_page": 5, "render_engine": "Poppler pdftoppm 26.05.0", "render_dpi": 300, "page_pixel_size": [2475, 3300], "crop_hash_basis": "RGB_RAW_PIXEL_BYTES"},
            "operation_boundary": "EQ32_CONDITIONAL_ON_EQ19_EQ20_EQ33_EXACT_WITHIN_EQ32_EQ34_AND_EQ39_APPROXIMATE",
            "domain_transfer_status": "NOT_YET_AUTHORIZED_PENDING_STEP66_INDEPENDENT_REDERIVATION",
        },
        "bibliography_boundaries": {
            "adopted_bibliography": evidence["bibliography_sources"]["adopted_bibliography"],
            "printed_reference_list": evidence["bibliography_sources"]["jcp147_reference_list"],
            "stale_ledger_is_not_adopted_inventory": True,
            "ref7_annotation_original_full_text_verified": False,
        },
        "conflicts": evidence["conflicts"],
        "open_items": [{
            "id": "P064-OPEN-REF7-ORIGINAL",
            "status": "OPEN_GROUND_NOT_FOUND",
            "owner": "Phase 064 Step 65 literature acquisition owner, carry to Step 69.1",
            "acceptance_criterion": "DOI-bound AIP VOR or lawful accepted manuscript; access/reuse condition; raw SHA-256; page count; 1-EOF and all-page visual read",
            "target": "Phase 064 Step 69.1 and final Step 69.2 ceiling",
        }],
        "builder_identity": {
            "path": "Codex/work/v1023_phase064/build_phase064_step65_literature_authority.py",
            "result_first_evidence_path": RESULT_PATH,
            "expected_parent": EXPECTED_PARENT,
            "expected_subject": EXPECTED_SUBJECT,
            "network_required_for_rebuild": False,
        },
    }
    return bind_semantic_sha(matrix)


def build_attestation(evidence: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    full_reads = []
    ground_not_found = []
    for row in evidence["sources"]:
        record = {
            "source_id": row["source_id"], "status": row["original_full_text_status"],
            "raw_sha256": row["raw_sha256"], "bytes": row["bytes"], "pages": row["pages"],
            "pages_read": row["pages_read"], "authority_tier": row["authority_tier"],
        }
        if row["original_full_text_status"] == "FULL_TEXT_READ":
            full_reads.append(record)
        else:
            ground_not_found.append(record)
    attestation = {
        "schema_version": "1.0.0",
        "artifact_kind": "V1023_LITERATURE_READ_ATTESTATION",
        "phase": 64,
        "step": 65,
        "gate": GATE,
        "status": STATUS,
        "evidence_id": evidence["evidence_id"],
        "evidence_date": evidence["evidence_date"],
        "access_date": evidence["access_date"],
        "human_evidence_semantic_sha256": sha256(canonical(evidence)),
        "human_evidence": evidence,
        "full_reads": full_reads,
        "ground_not_found": ground_not_found,
        "strict_traversal": {"source_records": 3, "equation_records": 8, "condition_records": 3, "conflict_records": 1, "upstream_approximation_records": 1},
        "source_mutation_count": 0,
        "matrix_semantic_sha256": matrix["semantic_sha256"],
        "authority": {
            "ceiling": AUTHORITY_CEILING,
            "ref7_method_content_verified": False,
            "wrong_ref7_doi_rejected": True,
            "p064_unconditional_pass_allowed": False,
        },
    }
    return bind_semantic_sha(attestation)


def main() -> int:
    evidence = load_human_evidence()
    validate_evidence(evidence)
    validate_local_sources(evidence)
    matrix = build_matrix(evidence)
    attestation = build_attestation(evidence, matrix)
    (ROOT / MATRIX_PATH).write_bytes(canonical(matrix))
    (ROOT / ATTESTATION_PATH).write_bytes(canonical(attestation))
    print(f"PASS_P064_STEP65_BUILD {MATRIX_PATH} {ATTESTATION_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
