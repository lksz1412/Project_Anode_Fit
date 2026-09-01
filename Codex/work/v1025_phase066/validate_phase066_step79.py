from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
STEP78_COMMIT = "fedb2031fbfabeaba84f86427c35334526234d73"
STEP72_COMMIT = "272b8d331c55448182e96c75363a56061adf58f2"
EXPECTED_SUBJECT = "audit(phase066): separate fit and material authority"
BRANCH = "codex/anode-fit-v1025_2-canonical-completion"
UPSTREAM = f"origin/{BRANCH}"
ORIGIN_URL = "https://github.com/lksz1412/Project_Anode_Fit.git"
PROTECTED_BRANCH = "codex/lib-physics-endgame-v1025_2"
PROTECTED_TIP = "fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71"
MAIN_TIP = "4069cb36a8a52b1b88c29d68aa54dcbe915b1618"
FIT_PATH = "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json"
PROVENANCE_PATH = "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json"
VECTOR_PATH = "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json"
AUTHORITY_PATH = "Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json"
BUILDER_PATH = "Codex/work/v1025_phase066/build_phase066_step79.py"
VALIDATOR_PATH = "Codex/work/v1025_phase066/validate_phase066_step79.py"
MATRIX_PATH = "Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json"
RESULT_PATH = "Codex/results/PHASE_066_STEP_079_AUTHORITY_RESULT.md"
PARENT_LEDGER_PATH = "Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md"
ACTIVE_LEDGER_PATH = "Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md"
HANDOVER_PATH = "Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md"
GATE = "PASS_P066_STEP79_EMPIRICAL_PHYSICAL_SEPARATION"
PERSISTENCE = "PASS_P066_STEP79_PERSISTENCE"
EXPECTED_MATRIX_SEMANTIC_SHA256 = "ccf7a972cd5a061840cf83bd3d6861bd3c840361433245d5fbf75ad3445a62ba"
FINAL_PATHS = sorted([
    BUILDER_PATH, VALIDATOR_PATH, MATRIX_PATH, RESULT_PATH,
    PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH,
])


class ValidationFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ValidationFailure(f"{code}: {detail}" if detail else code)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True,
                       allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "E_DUPLICATE_JSON_KEY", key)
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValidationFailure(f"E_NONFINITE_JSON: {value}")


def strict_json(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                       parse_constant=reject_constant)
    require(isinstance(value, dict) and canonical_bytes(value) == raw, "E_CANONICAL_JSON")
    observed = value.get("semantic_sha256")
    legacy = dict(value)
    legacy.pop("semantic_sha256", None)
    legacy_digest = sha256(json.dumps(legacy, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")).encode("utf-8"))
    value["semantic_sha256"] = ""
    require(observed in {sha256(canonical_bytes(value)), legacy_digest}, "E_SEMANTIC_SHA")
    value["semantic_sha256"] = observed
    return value


def current_semantic_sha256(value: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(value))
    clone["semantic_sha256"] = ""
    return sha256(canonical_bytes(clone))


def git(*args: str) -> bytes:
    process = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=False, check=False,
    )
    require(process.returncode == 0, "E_GIT", " ".join(args))
    return process.stdout


def source(commit: str, path: str) -> tuple[bytes, dict[str, Any]]:
    raw = git("cat-file", "blob", f"{commit}:{path}")
    return raw, strict_json(raw)


def resolve_pointer(document: Any, pointer: str) -> Any:
    require(pointer == "" or pointer.startswith("/"), "E_POINTER_SYNTAX", pointer)
    current = document
    if pointer == "":
        return current
    for raw_token in pointer[1:].split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            require(token.isdigit() and str(int(token)) == token, "E_POINTER_INDEX", pointer)
            index = int(token)
            require(index < len(current), "E_POINTER_RANGE", pointer)
            current = current[index]
        elif isinstance(current, dict):
            require(token in current, "E_POINTER_KEY", pointer)
            current = current[token]
        else:
            raise ValidationFailure(f"E_POINTER_SCALAR: {pointer}")
    return current


def assert_no_missing(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        require(bool(value), "E_EMPTY_OBJECT", path)
        for key, child in value.items():
            assert_no_missing(child, f"{path}/{key}")
    elif isinstance(value, list):
        require(bool(value), "E_EMPTY_LIST", path)
        for index, child in enumerate(value):
            assert_no_missing(child, f"{path}/{index}")
    elif isinstance(value, str):
        require(bool(value.strip()), "E_EMPTY_STRING", path)
    else:
        require(value is not None, "E_NULL", path)


def pointer_id(pointer: dict[str, Any]) -> tuple[str, str, str, str | None]:
    return (pointer["commit"], pointer["path"], pointer["json_pointer"],
            pointer.get("expected_record_id"))


def validate_semantics(matrix: dict[str, Any]) -> None:
    top_keys = {
        "schema_version", "phase", "step", "gate", "expected_parent",
        "generator_identity", "inputs", "source_gates", "claim_rows",
        "aggregate", "authority_ceiling", "semantic_sha256",
    }
    require(set(matrix) == top_keys, "E_TOP_SCHEMA")
    require(matrix["schema_version"] == "phase066-step79-empirical-physical-authority-matrix-v1",
            "E_SCHEMA_VERSION")
    require(matrix["phase"] == 66 and matrix["step"] == 79, "E_PHASE_STEP")
    require(matrix["gate"] == GATE and matrix["expected_parent"] == STEP78_COMMIT, "E_HEADER")
    require(matrix["generator_identity"] == {
        "path": BUILDER_PATH,
        "raw_sha256": sha256((ROOT / BUILDER_PATH).read_bytes()),
    }, "E_GENERATOR")

    expected_inputs = []
    documents: dict[tuple[str, str], dict[str, Any]] = {}
    for commit, path in (
        (STEP78_COMMIT, FIT_PATH),
        (STEP78_COMMIT, PROVENANCE_PATH),
        (STEP78_COMMIT, VECTOR_PATH),
        (STEP72_COMMIT, AUTHORITY_PATH),
    ):
        raw, value = source(commit, path)
        documents[(commit, path)] = value
        expected_inputs.append({
            "commit": commit,
            "path": path,
            "git_blob_sha1": git("rev-parse", f"{commit}:{path}").decode("ascii").strip(),
            "raw_sha256": sha256(raw),
            "bytes": len(raw),
        })
    require(matrix["inputs"] == expected_inputs, "E_INPUT_BINDING")
    fit = documents[(STEP78_COMMIT, FIT_PATH)]
    provenance = documents[(STEP78_COMMIT, PROVENANCE_PATH)]
    vector = documents[(STEP78_COMMIT, VECTOR_PATH)]
    authority = documents[(STEP72_COMMIT, AUTHORITY_PATH)]
    external = {
        run["runtime_label"]: {
            "argv": run["external_process_evidence"]["argv"],
            "cwd": run["external_process_evidence"]["cwd"],
            "exit_code": run["external_process_evidence"]["exit_code"],
            "stdout_sha256": run["external_process_evidence"]["stdout_sha256"],
            "stderr_sha256": run["external_process_evidence"]["stderr_sha256"],
        }
        for run in fit["runtime_reproductions"]
    }
    require(matrix["source_gates"] == {
        "step77_gate": fit["gate"],
        "step77_runtime_success": fit["runtime_success"],
        "step77_selected_trial_converged": fit["selected_trial_converged"],
        "step77_external_process_evidence": external,
    }, "E_SOURCE_GATES")
    require(fit["runtime_success"] is False and fit["selected_trial_converged"] is False,
            "E_SOURCE_RUNTIME_SUCCESS")
    require(set(external) == {"python3.12", "python3.14"}, "E_PROCESS_RUNTIME_SET")
    for runtime, record in external.items():
        require(all("GROUND_NOT_FOUND" in record[field]
                    for field in ("argv", "cwd", "exit_code", "stdout_sha256", "stderr_sha256")),
                "E_PROCESS_EVIDENCE_CEILING", runtime)

    rows = matrix["claim_rows"]
    require(isinstance(rows, list) and len(rows) == 8, "E_ROW_COUNT")
    row_schema = {
        "id", "claim", "claim_class", "source_pointers",
        "dataset_specimen_protocol_basis", "profile_parameter_count",
        "in_sample_metric", "held_out_evidence", "noise_weighting",
        "information_criterion", "identifiability",
        "independent_structural_thermodynamic_support", "empirical_pass",
        "external_authority", "phase_authority", "proposition_authority",
        "physical_authority", "empirical_ceiling", "physical_ceiling",
        "owner", "status",
    }
    nested_schemas = {
        "dataset_specimen_protocol_basis": {"dataset_path", "dataset_kind", "specimen", "protocol", "binding_status", "basis", "voltage_window_V", "points"},
        "profile_parameter_count": {"profile", "components", "free_parameters", "parameter_order", "selected_trial", "selected_trial_converged"},
        "in_sample_metric": {"status", "R2", "BIC", "cost", "peakRMSE", "valleyRMSE", "runtime_curve_agreement_pass"},
        "held_out_evidence": {"status", "held_out_cells", "held_out_rates", "held_out_temperatures"},
        "noise_weighting": {"weighting", "independent_noise_model", "error_covariance"},
        "information_criterion": {"criterion", "value", "scope", "cross_profile_selection_authority"},
        "identifiability": {"status", "stored_vs_replay_vector", "replay_cross_runtime_vector", "curve_objective", "original_optimizer_state"},
        "independent_structural_thermodynamic_support": {"status", "structural_phase_evidence", "species_assignment_evidence", "independent_thermodynamic_evidence"},
    }
    ids = [row["id"] for row in rows]
    require(ids == ["E79-01", "E79-02", "P79-03", "P79-04", "P79-05", "P79-06", "P79-07", "P79-08"],
            "E_ROW_IDS")
    by_id = {row["id"]: row for row in rows}
    expected_claims = {
        "E79-01": "Direct14 numerically reproduces the retained repository-derived CSV within the recorded in-sample tolerances.",
        "E79-02": "The supplied Step 79 evidence establishes a complete competing-profile comparison and a transferable skew mechanism.",
        "P79-03": "The whole-blend Direct14 components or frozen graphite profile labels establish graphite phase, gallery, or species identity.",
        "P79-04": "The Direct14 fit establishes LCO phase, species, or thermodynamic-mechanism authority.",
        "P79-05": "The whole-blend Direct14 fit isolates Si phases or proves a symmetric-Frumkin or width-based Si mechanism.",
        "P79-06": "Direct14 component areas on an absolute-mAh basis establish graphite/Si material fractions or a unique composition.",
        "P79-07": "A whole-curve fit tests finite-rate host independence, current partition, or nonadditive blend behavior.",
        "P79-08": "Bibliographic metadata for asserted Ref. 7 establishes the exact proposition, equation, and graphite applicability.",
    }
    expected_classes = {
        "E79-01": "DIRECT14_SKEW_EMPIRICAL",
        "E79-02": "COMPETING_PROFILE_EMPIRICAL",
        "P79-03": "GRAPHITE_PHASE_GALLERY_AUTHORITY",
        "P79-04": "LCO_PHASE_SPECIES_AUTHORITY",
        "P79-05": "SI_PHASE_MECHANISM_AUTHORITY",
        "P79-06": "BLEND_MATERIAL_FRACTION_AUTHORITY",
        "P79-07": "BLEND_FINITE_RATE_AUTHORITY",
        "P79-08": "REF7_PRIMARY_AUTHORITY",
    }
    expected_status = {
        "E79-01": fit["status"],
        "E79-02": "GROUND_NOT_FOUND",
        "P79-03": "UNVERIFIED",
        "P79-04": "GROUND_NOT_FOUND",
        "P79-05": "UNVERIFIED_OR_CONTRADICTED",
        "P79-06": "UNVERIFIED_INCOMPATIBLE_CAPACITY_KINDS",
        "P79-07": "UNVERIFIED_OR_ABSENT",
        "P79-08": "GROUND_NOT_FOUND",
    }
    expected_owners = {
        "E79-01": "PHASE-066-STEP-079-EMPIRICAL-BOUNDARY",
        "E79-02": "PHASE-069-STEPS-102-104-MODEL-AND-DATA-SYNTHESIS",
        "P79-03": "P071-PRIMARY-SOURCE-ACQUISITION",
        "P79-04": "P071-PRIMARY-SOURCE-ACQUISITION",
        "P79-05": "P071-PRIMARY-SOURCE-ACQUISITION",
        "P79-06": "P071-PRIMARY-SOURCE-ACQUISITION",
        "P79-07": "P067-CODE-HISTORY",
        "P79-08": "PHASE-071-PRIMARY-SOURCE-ACQUISITION",
    }
    expected_ceilings = {
        "E79-01": ("IN_SAMPLE_NUMERICAL_REPLAY_OF_ONE_REPOSITORY_DERIVED_RT_C50_CSV", "NO_PHASE_GALLERY_SPECIES_MATERIAL_OR_MECHANISM_IDENTIFICATION"),
        "E79-02": ("About one-point in-sample improvement is not independent mechanism validation.", "NO_TRANSFERABLE_SKEW_MECHANISM_AUTHORITY"),
        "P79-03": ("WHOLE_BLEND_CALIBRATION_IS_NOT_GRAPHITE_SPECIFIC_VALIDATION", "IMPLEMENTATION_SEEDS_COMPONENTS_BOUNDS_AND_WIDTHS_DO_NOT_IDENTIFY_GRAPHITE_PHASES_OR_GALLERIES"),
        "P79-04": ("DIRECT14_BLEND_FIT_HAS_NO_LCO_EMPIRICAL_SCOPE", "LCO_EXECUTABLE_ROUTE_SCOPE_TRANSFER_AND_REAL_O3_MULTI_TEMPERATURE_SUPPORT_REMAIN_UNVERIFIED_OR_GROUND_NOT_FOUND"),
        "P79-05": ("WHOLE_BLEND_CALIBRATION_DOES_NOT_ISOLATE_SI", "DEMO_COMPONENTS_WIDTH_RATIOS_AND_SYMMETRIC_FRUMKIN_FORM_DO_NOT_PROVE_SI_PHASE_OR_SKEW_MECHANISM"),
        "P79-06": ("Q_IS_COMPONENT_AREA_ON_THE_FITTED_ABSOLUTE_MAH_BASIS_ONLY", "NO_MASS_FRACTION_COMPOSITION_OR_COMMON_REVERSIBLE_CAPACITY_BASIS_AUTHORITY"),
        "P79-07": ("WHOLE_CURVE_IN_SAMPLE_CALIBRATION_ONLY", "NO_I_EQUALS_I_GRAPHITE_PLUS_I_SI_HOST_INDEPENDENCE_OR_NONADDITIVE_FINITE_RATE_AUTHORITY"),
        "P79-08": ("METADATA_IDENTITY_OBSERVATION_ONLY", "NO_PROPOSITION_PAGE_EQUATION_OR_GRAPHITE_APPLICABILITY_AUTHORITY"),
    }
    for row in rows:
        row_id = row.get("id", "UNKNOWN")
        require(set(row) == row_schema, "E_ROW_SCHEMA", row_id)
        for field, schema in nested_schemas.items():
            require(isinstance(row[field], dict) and set(row[field]) == schema,
                    "E_EVIDENCE_AXIS_OMISSION", f"{row_id}:{field}")
        require(row["claim"] == expected_claims[row_id], "E_CLAIM", row_id)
        require(row["claim_class"] == expected_classes[row_id], "E_CLAIM_CLASS", row_id)
        require(row["status"] == expected_status[row_id], "E_STATUS", row_id)
        require(row["owner"] == expected_owners[row_id], "E_OWNER", row_id)
        require((row["empirical_ceiling"], row["physical_ceiling"]) == expected_ceilings[row_id],
                "E_ROW_CEILING", row_id)
        for authority_field in ("external_authority", "phase_authority",
                                "proposition_authority", "physical_authority"):
            require(row[authority_field] is False, "E_AUTHORITY_PROMOTION",
                    f"{row_id}:{authority_field}")
        require(isinstance(row["empirical_pass"], bool), "E_EMPIRICAL_TYPE", row_id)
        require(row["held_out_evidence"]["status"] in {"NOT_TESTED", "NOT_APPLICABLE"},
                "E_IN_SAMPLE_EXTERNAL_PROMOTION", row_id)
        for field in ("held_out_cells", "held_out_rates", "held_out_temperatures"):
            require(row["held_out_evidence"][field] in {"GROUND_NOT_FOUND", "NOT_APPLICABLE"},
                    "E_IN_SAMPLE_EXTERNAL_PROMOTION", f"{row_id}:{field}")
        for field in ("independent_noise_model", "error_covariance"):
            require(row["noise_weighting"][field] in {"GROUND_NOT_FOUND", "NOT_APPLICABLE"},
                    "E_NOISE_PROMOTION", f"{row_id}:{field}")
        support = row["independent_structural_thermodynamic_support"]
        require(support["status"] in {"GROUND_NOT_FOUND", "NOT_APPLICABLE"},
                "E_SUPPORT_PROMOTION", row_id)
        for field in ("structural_phase_evidence", "species_assignment_evidence",
                      "independent_thermodynamic_evidence"):
            require(support[field] in {"GROUND_NOT_FOUND", "NOT_APPLICABLE"},
                    "E_SUPPORT_PROMOTION", f"{row_id}:{field}")
        require(row["dataset_specimen_protocol_basis"]["binding_status"] in {
            provenance["raw_input"]["specimen_protocol_status"], "GROUND_NOT_FOUND"
        }, "E_DATASET_BINDING_PROMOTION", row_id)
        require(row["information_criterion"]["cross_profile_selection_authority"] is False,
                "E_INFORMATION_PROMOTION", row_id)
        require(isinstance(row["source_pointers"], list) and row["source_pointers"],
                "E_SOURCE_POINTER", row_id)
        for source_pointer in row["source_pointers"]:
            require(set(source_pointer) in ({"commit", "path", "json_pointer"},
                                            {"commit", "path", "json_pointer", "expected_record_id"}),
                    "E_POINTER_SCHEMA", row_id)
            key = (source_pointer["commit"], source_pointer["path"])
            require(key in documents, "E_POINTER_INPUT", row_id)
            resolved = resolve_pointer(documents[key], source_pointer["json_pointer"])
            expected_id = source_pointer.get("expected_record_id")
            if expected_id is not None:
                require(isinstance(resolved, dict), "E_POINTER_RECORD", row_id)
                actual_ids = {resolved.get("id"), resolved.get("claim_id"), resolved.get("doi")}
                require(expected_id in actual_ids, "E_POINTER_RECORD_ID", f"{row_id}:{expected_id}")
        assert_no_missing(row)
    require([row["id"] for row in rows if row["empirical_pass"]] == ["E79-01"],
            "E_EMPIRICAL_PASS_SET")

    direct_pointer_set = {
        (STEP78_COMMIT, FIT_PATH, "/status", None),
        (STEP78_COMMIT, FIT_PATH, "/runtime_reproductions/0/metrics", None),
        (STEP78_COMMIT, FIT_PATH, "/runtime_reproductions/1/metrics", None),
        (STEP78_COMMIT, PROVENANCE_PATH, "/raw_input", None),
        (STEP78_COMMIT, PROVENANCE_PATH, "/preprocessing", None),
        (STEP78_COMMIT, PROVENANCE_PATH, "/optimizer_contract", None),
        (STEP78_COMMIT, VECTOR_PATH, "/curve_objective_classification", None),
    }
    require({pointer_id(item) for item in by_id["E79-01"]["source_pointers"]} == direct_pointer_set,
            "E_DIRECT_POINTER_SET")
    required_record_ids = {
        "E79-02": {"M72-GR-08"},
        "P79-03": {"M72-GR-03", "M72-GR-04", "M72-GR-05", "M72-GR-07", "M72-GR-08", "S72-F03"},
        "P79-04": {"M72-LCO-03", "M72-LCO-04", "M72-LCO-07", "S72-F03"},
        "P79-05": {"M72-SI-03", "M72-SI-04", "M72-SI-05", "M72-SI-06", "S72-F03"},
        "P79-06": {"M72-BLEND-01", "M72-BLEND-02", "S72-F03"},
        "P79-07": {"M72-BLEND-04", "M72-BLEND-05", "S72-F04"},
        "P79-08": {"10.1063/1.4802584", "S72-F06"},
    }
    expected_pointer_counts = {
        "E79-02": 3, "P79-03": 13, "P79-04": 4, "P79-05": 12,
        "P79-06": 10, "P79-07": 10, "P79-08": 2,
    }
    for row_id, expected_ids in required_record_ids.items():
        require(len(by_id[row_id]["source_pointers"]) == expected_pointer_counts[row_id],
                "E_POINTER_COUNT", row_id)
        actual_ids = {item.get("expected_record_id") for item in by_id[row_id]["source_pointers"]}
        actual_ids.discard(None)
        require(actual_ids == expected_ids, "E_RECORD_POINTER_SET", row_id)

    run12, run14 = fit["runtime_reproductions"]
    require(run12["metrics"] == run14["metrics"], "E_RUNTIME_METRICS")
    metric = by_id["E79-01"]["in_sample_metric"]
    for key in ("R2", "BIC", "cost", "peakRMSE", "valleyRMSE"):
        require(metric[key] == run12["metrics"][key], "E_METRIC_BINDING", key)
    require(by_id["E79-01"]["dataset_specimen_protocol_basis"] == {
        "dataset_path": provenance["raw_input"]["path"],
        "dataset_kind": provenance["raw_input"]["source_kind"],
        "specimen": provenance["raw_input"]["source_declared_specimen"],
        "protocol": provenance["raw_input"]["source_declared_protocol"],
        "binding_status": provenance["raw_input"]["specimen_protocol_status"],
        "basis": "absolute_mAh_not_mass_normalized",
        "voltage_window_V": [provenance["processed_input"]["V_min"], provenance["processed_input"]["V_max"]],
        "points": provenance["processed_input"]["points"],
    }, "E_DATASET_BINDING")
    require(by_id["E79-01"]["profile_parameter_count"]["components"] == 14 and
            by_id["E79-01"]["profile_parameter_count"]["free_parameters"] == 57 and
            by_id["E79-01"]["profile_parameter_count"]["selected_trial_converged"] is False,
            "E_PROFILE_BINDING")
    require(by_id["E79-01"]["noise_weighting"] == {
        "weighting": provenance["preprocessing"]["weighting"],
        "independent_noise_model": "GROUND_NOT_FOUND",
        "error_covariance": "GROUND_NOT_FOUND",
    }, "E_NOISE_WEIGHTING")
    require(by_id["E79-01"]["information_criterion"] == {
        "criterion": "BIC", "value": run12["metrics"]["BIC"],
        "scope": "IN_SAMPLE_SINGLE_PROFILE_RECORD",
        "cross_profile_selection_authority": False,
    }, "E_INFORMATION_CRITERION")
    ident = by_id["E79-01"]["identifiability"]
    require(ident["status"] == "NOT_ESTABLISHED" and
            ident["stored_vs_replay_vector"] == "NOT_EQUIVALENT" and
            ident["replay_cross_runtime_vector"] == "IDENTICAL" and
            ident["curve_objective"] == "TOLERANCE_EQUIVALENT" and
            ident["original_optimizer_state"] == "GROUND_NOT_FOUND",
            "E_CURVE_IDENTIFIABILITY_PROMOTION")
    require(by_id["E79-02"]["held_out_evidence"]["status"] == "NOT_TESTED" and
            by_id["E79-02"]["information_criterion"]["criterion"] == "GROUND_NOT_FOUND",
            "E_COMPETING_PROFILE_GAP")
    require(by_id["P79-04"]["held_out_evidence"]["status"] == "NOT_APPLICABLE" and
            by_id["P79-04"]["in_sample_metric"]["status"] == "NOT_APPLICABLE",
            "E_LCO_SCOPE")
    require(by_id["P79-08"]["independent_structural_thermodynamic_support"]["status"] ==
            "GROUND_NOT_FOUND", "E_REF7_PRIMARY_TEXT")
    require(authority["metadata_verifications"][5]["owner"] == by_id["P79-08"]["owner"],
            "E_REF7_OWNER")

    require(matrix["aggregate"] == {
        "rows": 8,
        "empirical_pass_true": 1,
        "external_authority_true": 0,
        "phase_authority_true": 0,
        "proposition_authority_true": 0,
        "physical_authority_true": 0,
        "held_out_not_tested": 6,
        "primary_text_ground_not_found": 1,
    }, "E_AGGREGATE")
    ceiling_keys = {
        "in_sample_fit_is_external_validation",
        "component_basis_is_phase_gallery_species_identity",
        "parameter_label_is_material_constant_or_fraction",
        "curve_equivalence_is_identifiability_or_mechanism",
        "metadata_is_proposition_support",
        "room_temperature_fit_is_multi_temperature_authority",
        "empirical_pass_implies_physical_authority",
        "whole_blend_metric_is_material_specific_validation",
        "whole_curve_fit_is_finite_rate_current_partition_test",
    }
    require(set(matrix["authority_ceiling"]) == ceiling_keys and
            all(value is False for value in matrix["authority_ceiling"].values()),
            "E_AUTHORITY_CEILING")
    require(matrix["semantic_sha256"] == current_semantic_sha256(matrix),
            "E_SEMANTIC_RECOMPUTE")
    require(matrix["semantic_sha256"] == EXPECTED_MATRIX_SEMANTIC_SHA256,
            "E_MATRIX_CONTENT_PIN")


def validate_documents() -> None:
    result = (ROOT / RESULT_PATH).read_text(encoding="utf-8")
    for token in (GATE, PERSISTENCE, "GROUND_NOT_FOUND", "NOT_TESTED",
                  "empirical_pass=true", "physical_authority=false", "Step 80"):
        require(token in result, "E_RESULT_TOKEN", token)
    for path in (PARENT_LEDGER_PATH, ACTIVE_LEDGER_PATH, HANDOVER_PATH):
        text = (ROOT / path).read_text(encoding="utf-8")
        require("Step 79" in text and GATE in text and PERSISTENCE in text and
                "Step 80" in text, "E_CONTROL_DOCUMENT", path)


def validate_source_policy() -> None:
    allowed_imports = {
        BUILDER_PATH: {"__future__", "hashlib", "json", "os", "subprocess", "pathlib", "typing"},
        VALIDATOR_PATH: {"__future__", "argparse", "ast", "hashlib", "json", "subprocess", "pathlib", "typing"},
    }
    expected_import_statements = {
        BUILDER_PATH: [
            "from __future__ import annotations", "import hashlib", "import json", "import os",
            "import subprocess", "from pathlib import Path", "from typing import Any",
        ],
        VALIDATOR_PATH: [
            "from __future__ import annotations", "import argparse", "import ast", "import hashlib",
            "import json", "import subprocess", "from pathlib import Path", "from typing import Any, Callable",
        ],
    }
    expected_process_calls = {
        BUILDER_PATH: [
            ("git_blob", "subprocess.run(['git', 'cat-file', 'blob', f'{commit}:{path}'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)"),
            ("git_blob", "subprocess.run(['git', 'rev-parse', f'{commit}:{path}'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)"),
        ],
        VALIDATOR_PATH: [
            ("git", "subprocess.run(['git', *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)"),
            ("local_ref_guard", "subprocess.run(['git', 'show-ref', '--verify', '--quiet', 'refs/heads/main'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)"),
        ],
    }
    expected_mutation_calls = {
        BUILDER_PATH: [
            ("build", "temporary.write_bytes(raw)"),
            ("build", "os.replace(temporary, OUTPUT_PATH)"),
            ("build", "temporary.unlink(missing_ok=True)"),
        ],
        VALIDATOR_PATH: [],
    }
    allowed_string_replace_calls = {
        BUILDER_PATH: [],
        VALIDATOR_PATH: [
            ("resolve_pointer", "raw_token.replace('~1', '/')"),
            ("resolve_pointer", "raw_token.replace('~1', '/').replace('~0', '~')"),
        ],
    }
    sensitive_attributes = {
        "run", "call", "check_call", "check_output", "getoutput", "getstatusoutput", "Popen",
        "open", "write", "writelines", "write_bytes", "write_text", "touch", "mkdir", "rmdir",
        "rename", "replace", "remove", "unlink", "copy", "copy2", "copyfile", "move", "rmtree",
    }
    for path in (BUILDER_PATH, VALIDATOR_PATH):
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
        parents = {child: parent for parent in ast.walk(tree)
                   for child in ast.iter_child_nodes(parent)}

        def owner(node: ast.AST) -> str:
            while node in parents:
                node = parents[node]
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    return node.name
            return "<module>"

        imported = set()
        import_statements: list[str] = []
        process_calls: list[tuple[str, str]] = []
        mutation_calls: list[tuple[str, str]] = []
        sensitive_calls: list[tuple[str, str]] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
                import_statements.append(ast.unparse(node))
            elif isinstance(node, ast.ImportFrom):
                imported.add((node.module or "").split(".")[0])
                import_statements.append(ast.unparse(node))
            if isinstance(node, ast.arg):
                require(node.arg not in {"subprocess", "os", "Path"},
                        "E_SOURCE_RESERVED_SHADOW", f"{path}:{node.arg}")
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                require(node.id not in {"subprocess", "os", "Path"},
                        "E_SOURCE_RESERVED_SHADOW", f"{path}:{node.id}")
            if isinstance(node, ast.Attribute) and node.attr in sensitive_attributes:
                parent = parents.get(node)
                require(isinstance(parent, ast.Call) and parent.func is node,
                        "E_SOURCE_EFFECT_ALIAS", f"{path}:{ast.unparse(node)}")
            if isinstance(node, ast.Attribute):
                require(not (node.attr.startswith("__") and node.attr.endswith("__")),
                        "E_SOURCE_DUNDER_ATTRIBUTE", f"{path}:{node.attr}")
            if isinstance(node, ast.Call):
                require(isinstance(node.func, (ast.Name, ast.Attribute)),
                        "E_SOURCE_INDIRECT_CALL", f"{path}:{ast.unparse(node.func)}")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                require(node.func.id not in {"eval", "exec", "compile", "open", "getattr", "vars",
                                             "globals", "locals", "__import__"},
                        "E_SOURCE_DYNAMIC", f"{path}:{node.func.id}")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                require(node.func.attr not in {"system", "Popen", "popen", "open", "write_text", "touch",
                                               "mkdir", "rmdir", "rename", "remove", "copy", "copy2",
                                               "copyfile", "move", "rmtree", "urlopen", "connect"},
                        "E_SOURCE_EFFECT", f"{path}:{node.func.attr}")
                if node.func.attr in sensitive_attributes:
                    sensitive_calls.append((owner(node), ast.unparse(node)))
                if node.func.attr == "run" and isinstance(node.func.value, ast.Name) and \
                        node.func.value.id == "subprocess":
                    process_calls.append((owner(node), ast.unparse(node)))
                if node.func.attr in {"write_bytes", "unlink"} or \
                        (node.func.attr == "replace" and isinstance(node.func.value, ast.Name) and
                         node.func.value.id == "os"):
                    mutation_calls.append((owner(node), ast.unparse(node)))
        require(imported == allowed_imports[path], "E_SOURCE_IMPORTS", path)
        require(import_statements == expected_import_statements[path],
                "E_SOURCE_IMPORT_STATEMENTS", path)
        require(sorted(process_calls) == sorted(expected_process_calls[path]),
                "E_SOURCE_PROCESS_CALLS", path)
        require(sorted(mutation_calls) == sorted(expected_mutation_calls[path]),
                "E_SOURCE_MUTATION_CALLS", path)
        expected_sensitive = (expected_process_calls[path] + expected_mutation_calls[path] +
                              allowed_string_replace_calls[path])
        require(sorted(sensitive_calls) == sorted(expected_sensitive),
                "E_SOURCE_SENSITIVE_CALLS", path)


def negative_case(matrix: dict[str, Any], name: str,
                  mutation: Callable[[dict[str, Any]], None]) -> None:
    candidate = json.loads(json.dumps(matrix))
    mutation(candidate)
    candidate["semantic_sha256"] = ""
    candidate["semantic_sha256"] = current_semantic_sha256(candidate)
    try:
        validate_semantics(candidate)
    except ValidationFailure:
        return
    raise ValidationFailure(f"E_NEGATIVE_FALSE_PASS: {name}")


def assign(mapping: dict[str, Any], key: str, value: Any) -> None:
    mapping[key] = value


def run_negatives(matrix: dict[str, Any]) -> int:
    cases: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("in-sample-to-external", lambda value: assign(value["claim_rows"][0], "external_authority", True)),
        ("component-to-phase", lambda value: assign(value["claim_rows"][2], "phase_authority", True)),
        ("metadata-to-proposition", lambda value: assign(value["claim_rows"][7], "proposition_authority", True)),
        ("missing-evidence-omission", lambda value: value["claim_rows"][0]["noise_weighting"].pop("error_covariance")),
        ("empirical-pass-to-physical-authority", lambda value: assign(value["claim_rows"][0], "physical_authority", True)),
        ("room-temperature-to-multitemperature", lambda value: assign(value["authority_ceiling"], "room_temperature_fit_is_multi_temperature_authority", True)),
        ("curve-to-identifiability", lambda value: assign(value["claim_rows"][0]["identifiability"], "status", "ESTABLISHED")),
        ("unresolvable-source-pointer", lambda value: assign(value["claim_rows"][2]["source_pointers"][0], "json_pointer", "/missing")),
        ("runtime-success-promotion", lambda value: assign(value["source_gates"], "step77_runtime_success", True)),
        ("owner-omission", lambda value: assign(value["claim_rows"][5], "owner", "")),
        ("nested-unknown-key", lambda value: assign(value["claim_rows"][4]["held_out_evidence"], "unknown", "x")),
        ("aggregate-drift", lambda value: assign(value["aggregate"], "physical_authority_true", 1)),
        ("structural-support-promotion", lambda value: assign(value["claim_rows"][2]["independent_structural_thermodynamic_support"], "structural_phase_evidence", "VERIFIED")),
        ("held-out-cell-promotion", lambda value: assign(value["claim_rows"][0]["held_out_evidence"], "held_out_cells", "VERIFIED")),
        ("dataset-binding-promotion", lambda value: assign(value["claim_rows"][4]["dataset_specimen_protocol_basis"], "binding_status", "EXACT_EXTERNAL_BINDING")),
        ("noise-model-promotion", lambda value: assign(value["claim_rows"][5]["noise_weighting"], "independent_noise_model", "VALIDATED")),
        ("extra-unidentified-pointer", lambda value: value["claim_rows"][1]["source_pointers"].append({"commit": STEP78_COMMIT, "path": FIT_PATH, "json_pointer": "/schema_version"})),
    ]
    for name, mutation in cases:
        negative_case(matrix, name, mutation)
    return len(cases)


def validate_content() -> int:
    matrix = strict_json((ROOT / MATRIX_PATH).read_bytes())
    validate_semantics(matrix)
    validate_documents()
    validate_source_policy()
    return run_negatives(matrix)


def local_ref_guard() -> None:
    require(git("rev-parse", PROTECTED_BRANCH).decode().strip() == PROTECTED_TIP,
            "E_PROTECTED_LOCAL")
    local_main = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", "refs/heads/main"], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False,
    )
    require(local_main.returncode == 1, "E_LOCAL_MAIN")


def live_refs(active: str) -> None:
    require(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").decode().split()[0] == active,
            "E_ACTIVE_LIVE")
    require(git("ls-remote", "--heads", "origin", f"refs/heads/{PROTECTED_BRANCH}").decode().split()[0] ==
            PROTECTED_TIP, "E_PROTECTED_LIVE")
    require(git("ls-remote", "--heads", "origin", "refs/heads/main").decode().split()[0] == MAIN_TIP,
            "E_MAIN_LIVE")


def validate_staged() -> None:
    require(git("rev-parse", "HEAD").decode().strip() == STEP78_COMMIT, "E_PARENT")
    require(git("branch", "--show-current").decode().strip() == BRANCH, "E_BRANCH")
    require(git("rev-parse", "--abbrev-ref", "@{u}").decode().strip() == UPSTREAM, "E_UPSTREAM_NAME")
    require(git("rev-parse", UPSTREAM).decode().strip() == STEP78_COMMIT, "E_UPSTREAM_PARENT")
    require(git("remote", "get-url", "origin").decode().strip() == ORIGIN_URL, "E_ORIGIN")
    require(git("rev-parse", f"origin/{PROTECTED_BRANCH}").decode().strip() == PROTECTED_TIP and
            git("rev-parse", "origin/main").decode().strip() == MAIN_TIP, "E_TRACKING_PROTECTED")
    require(git("diff", "--cached", "--name-only").decode().splitlines() == FINAL_PATHS, "E_PATHS")
    require(not git("diff", "--name-only").strip() and
            not git("ls-files", "--others", "--exclude-standard").strip(), "E_DIRTY_OUTSIDE_STAGE")
    require(not git("diff", "--cached", "--check").strip(), "E_DIFF_CHECK")
    expected_status = {
        BUILDER_PATH: "A", VALIDATOR_PATH: "A", MATRIX_PATH: "A", RESULT_PATH: "A",
        PARENT_LEDGER_PATH: "M", ACTIVE_LEDGER_PATH: "M", HANDOVER_PATH: "M",
    }
    status = git("diff", "--cached", "--name-status").decode().splitlines()
    require({line.split("\t", 1)[1]: line.split("\t", 1)[0] for line in status} == expected_status,
            "E_STATUS")
    for path in FINAL_PATHS:
        require(git("show", f":{path}") == (ROOT / path).read_bytes(), "E_INDEX_WORKTREE", path)
    live_refs(STEP78_COMMIT)
    local_ref_guard()


def validate_persistence(commit: str) -> None:
    require(len(commit) == 40 and all(char in "0123456789abcdef" for char in commit), "E_COMMIT")
    require(git("rev-parse", "HEAD").decode().strip() == commit, "E_HEAD")
    require(git("branch", "--show-current").decode().strip() == BRANCH, "E_BRANCH")
    require(git("rev-parse", "--abbrev-ref", "@{u}").decode().strip() == UPSTREAM, "E_UPSTREAM_NAME")
    require(git("remote", "get-url", "origin").decode().strip() == ORIGIN_URL, "E_ORIGIN")
    require(git("rev-parse", f"origin/{PROTECTED_BRANCH}").decode().strip() == PROTECTED_TIP and
            git("rev-parse", "origin/main").decode().strip() == MAIN_TIP, "E_TRACKING_PROTECTED")
    require(git("rev-parse", "HEAD^").decode().strip() == STEP78_COMMIT, "E_COMMIT_PARENT")
    require(len(git("rev-list", "--parents", "-n", "1", "HEAD").decode().split()) == 2,
            "E_SINGLE_PARENT")
    require(git("show", "-s", "--format=%s", "HEAD").decode().strip() == EXPECTED_SUBJECT, "E_SUBJECT")
    require(git("rev-parse", UPSTREAM).decode().strip() == commit, "E_UPSTREAM")
    live_refs(commit)
    local_ref_guard()
    require(git("diff", "--name-only", "HEAD^").decode().splitlines() == FINAL_PATHS,
            "E_COMMITTED_PATHS")
    require(not any(path.startswith("Claude/") for path in FINAL_PATHS), "E_CLAUDE")
    for path in FINAL_PATHS:
        require(git("show", f"HEAD:{path}") == (ROOT / path).read_bytes(), "E_COMMIT_WORKTREE", path)
    require(not git("status", "--porcelain").strip(), "E_DIRTY")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--persistence")
    args = parser.parse_args()
    negatives = validate_content()
    if args.staged:
        validate_staged()
    if args.persistence:
        validate_persistence(args.persistence)
        print(f"{PERSISTENCE} commit={args.persistence} negative={negatives}/17")
    else:
        print(f"{GATE} negative={negatives}/17")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValidationFailure, KeyError, TypeError, ValueError, OSError,
            IndexError, json.JSONDecodeError) as error:
        print(f"FAIL_P066_STEP79 {error}")
        raise SystemExit(1)
