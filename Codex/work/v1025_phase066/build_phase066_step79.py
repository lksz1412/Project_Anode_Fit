from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
STEP78_COMMIT = "fedb2031fbfabeaba84f86427c35334526234d73"
STEP72_COMMIT = "272b8d331c55448182e96c75363a56061adf58f2"
FIT_PATH = "Codex/results/PHASE_066_DIRECT14_FIT_REPRODUCTION.json"
PROVENANCE_PATH = "Codex/results/PHASE_066_FIT_INPUT_PROVENANCE.json"
VECTOR_PATH = "Codex/results/PHASE_066_OPTIMIZER_STATE_VECTOR_MATRIX.json"
AUTHORITY_PATH = "Codex/results/PHASE_065_SKEW_MATERIAL_AUTHORITY_MATRIX.json"
BUILDER_PATH = "Codex/work/v1025_phase066/build_phase066_step79.py"
OUTPUT_PATH = ROOT / "Codex/results/PHASE_066_EMPIRICAL_PHYSICAL_AUTHORITY_MATRIX.json"
GATE = "PASS_P066_STEP79_EMPIRICAL_PHYSICAL_SEPARATION"


class BuildFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise BuildFailure(f"{code}: {detail}" if detail else code)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True,
                       allow_nan=False, separators=(",", ": ")) + "\n").encode("utf-8")


def seal(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = ""
    value["semantic_sha256"] = sha256(canonical_bytes(value))
    return value


def git_blob(commit: str, path: str) -> tuple[bytes, str]:
    allowed = {
        (STEP78_COMMIT, FIT_PATH),
        (STEP78_COMMIT, PROVENANCE_PATH),
        (STEP78_COMMIT, VECTOR_PATH),
        (STEP72_COMMIT, AUTHORITY_PATH),
    }
    require((commit, path) in allowed, "E_GIT_INPUT_ALLOWLIST", f"{commit}:{path}")
    content = subprocess.run(
        ["git", "cat-file", "blob", f"{commit}:{path}"], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False,
    )
    identity = subprocess.run(
        ["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False,
    )
    require(content.returncode == identity.returncode == 0, "E_GIT_INPUT", path)
    return content.stdout, identity.stdout.decode("ascii").strip()


def strict_json(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw.decode("utf-8"))
    require(isinstance(value, dict) and canonical_bytes(value) == raw, "E_CANONICAL_INPUT")
    observed = value.get("semantic_sha256")
    legacy = dict(value)
    legacy.pop("semantic_sha256", None)
    legacy_digest = sha256(json.dumps(legacy, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")).encode("utf-8"))
    value["semantic_sha256"] = ""
    require(observed in {sha256(canonical_bytes(value)), legacy_digest}, "E_SEMANTIC_INPUT")
    value["semantic_sha256"] = observed
    return value


def input_record(commit: str, path: str, raw: bytes, blob: str) -> dict[str, Any]:
    return {
        "commit": commit,
        "path": path,
        "git_blob_sha1": blob,
        "raw_sha256": sha256(raw),
        "bytes": len(raw),
    }


def pointer(commit: str, path: str, json_pointer: str,
            expected_id: str | None = None) -> dict[str, Any]:
    result = {
        "commit": commit,
        "path": path,
        "json_pointer": json_pointer,
    }
    if expected_id is not None:
        result["expected_record_id"] = expected_id
    return result


def unavailable_dataset(kind: str) -> dict[str, Any]:
    return {
        "dataset_path": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "dataset_kind": kind,
        "specimen": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "protocol": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "binding_status": "GROUND_NOT_FOUND",
        "basis": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "voltage_window_V": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "points": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
    }


def unavailable_profile(profile: str) -> dict[str, Any]:
    return {
        "profile": profile,
        "components": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "free_parameters": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "parameter_order": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "selected_trial": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "selected_trial_converged": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
    }


def unavailable_metric(status: str) -> dict[str, Any]:
    return {
        "status": status,
        "R2": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "BIC": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "cost": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "peakRMSE": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "valleyRMSE": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
        "runtime_curve_agreement_pass": "GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW",
    }


def held_out(status: str) -> dict[str, Any]:
    value = "NOT_APPLICABLE" if status == "NOT_APPLICABLE" else "GROUND_NOT_FOUND"
    return {
        "status": status,
        "held_out_cells": value,
        "held_out_rates": value,
        "held_out_temperatures": value,
    }


def noise(weighting: str) -> dict[str, Any]:
    value = "NOT_APPLICABLE" if weighting == "NOT_APPLICABLE" else "GROUND_NOT_FOUND"
    return {
        "weighting": weighting,
        "independent_noise_model": value,
        "error_covariance": value,
    }


def information(criterion: Any, value: Any, scope: str) -> dict[str, Any]:
    return {
        "criterion": criterion,
        "value": value,
        "scope": scope,
        "cross_profile_selection_authority": False,
    }


def identifiability(status: str, vector: dict[str, Any] | None = None) -> dict[str, Any]:
    if vector is None:
        missing = "NOT_APPLICABLE" if status == "NOT_APPLICABLE" else "GROUND_NOT_FOUND"
        return {
            "status": status,
            "stored_vs_replay_vector": missing,
            "replay_cross_runtime_vector": missing,
            "curve_objective": missing,
            "original_optimizer_state": missing,
        }
    pairwise = {(row["left"], row["right"]): row
                for row in vector["pairwise_vector_classification"]}
    return {
        "status": status,
        "stored_vs_replay_vector": pairwise[("stored_8dp", "python3.12_replay")]["status"],
        "replay_cross_runtime_vector": pairwise[("python3.12_replay", "python3.14_replay")]["status"],
        "curve_objective": vector["curve_objective_classification"]["replay_vs_stored_curve"],
        "original_optimizer_state": vector["vectors"]["original_historical"]["status"],
    }


def independent_support(status: str) -> dict[str, Any]:
    value = "NOT_APPLICABLE" if status == "NOT_APPLICABLE" else "GROUND_NOT_FOUND"
    return {
        "status": status,
        "structural_phase_evidence": value,
        "species_assignment_evidence": value,
        "independent_thermodynamic_evidence": value,
    }


def build_rows(fit: dict[str, Any], provenance: dict[str, Any],
               vector: dict[str, Any], authority: dict[str, Any]) -> list[dict[str, Any]]:
    runs = fit["runtime_reproductions"]
    require([run["runtime_label"] for run in runs] == ["python3.12", "python3.14"],
            "E_RUNTIME_SET")
    require(runs[0]["metrics"] == runs[1]["metrics"], "E_RUNTIME_METRIC_MISMATCH")
    metrics = runs[0]["metrics"]
    raw = provenance["raw_input"]
    processed = provenance["processed_input"]
    optimizer = provenance["optimizer_contract"]
    material = {row["claim_id"]: row for row in authority["material_claims"]}
    findings = {row["id"]: row for row in authority["findings"]}
    metadata = {row["doi"]: row for row in authority["metadata_verifications"]}
    required = {
        "M72-GR-03", "M72-GR-04", "M72-GR-05", "M72-GR-07", "M72-GR-08",
        "M72-LCO-03", "M72-LCO-04", "M72-LCO-07",
        "M72-SI-03", "M72-SI-04", "M72-SI-05", "M72-SI-06",
        "M72-BLEND-01", "M72-BLEND-02", "M72-BLEND-04", "M72-BLEND-05",
    }
    require(required <= set(material), "E_MATERIAL_SOURCE_SET")
    require({"S72-F03", "S72-F04", "S72-F06"} <= set(findings), "E_FINDING_SOURCE_SET")
    require("10.1063/1.4802584" in metadata, "E_REF7_SOURCE")

    direct_dataset = {
        "dataset_path": raw["path"],
        "dataset_kind": raw["source_kind"],
        "specimen": raw["source_declared_specimen"],
        "protocol": raw["source_declared_protocol"],
        "binding_status": raw["specimen_protocol_status"],
        "basis": raw["capacity_basis"],
        "voltage_window_V": [processed["V_min"], processed["V_max"]],
        "points": processed["points"],
    }
    direct_profile = {
        "profile": "Direct14 skew-logistic",
        "components": optimizer["components"],
        "free_parameters": metrics["npar"],
        "parameter_order": optimizer["parameter_order"],
        "selected_trial": runs[0]["best_trial"],
        "selected_trial_converged": fit["selected_trial_converged"],
    }
    direct_metric = {
        "status": "NUMERICAL_AGREEMENT_PASS_SELECTED_TRIAL_NONCONVERGED",
        "R2": metrics["R2"],
        "BIC": metrics["BIC"],
        "cost": metrics["cost"],
        "peakRMSE": metrics["peakRMSE"],
        "valleyRMSE": metrics["valleyRMSE"],
        "runtime_curve_agreement_pass": fit["comparison"]["runtime_curve_agreement_pass"],
    }
    direct_noise = noise(provenance["preprocessing"]["weighting"])
    direct_information = information("BIC", metrics["BIC"], "IN_SAMPLE_SINGLE_PROFILE_RECORD")
    direct_identifiability = identifiability("NOT_ESTABLISHED", vector)
    direct_pointers = [
        pointer(STEP78_COMMIT, FIT_PATH, "/status"),
        pointer(STEP78_COMMIT, FIT_PATH, "/runtime_reproductions/0/metrics"),
        pointer(STEP78_COMMIT, FIT_PATH, "/runtime_reproductions/1/metrics"),
        pointer(STEP78_COMMIT, PROVENANCE_PATH, "/raw_input"),
        pointer(STEP78_COMMIT, PROVENANCE_PATH, "/preprocessing"),
        pointer(STEP78_COMMIT, PROVENANCE_PATH, "/optimizer_contract"),
        pointer(STEP78_COMMIT, VECTOR_PATH, "/curve_objective_classification"),
    ]

    def material_pointers(indices_and_ids: list[tuple[int, str]],
                          finding_index: int, finding_id: str) -> list[dict[str, Any]]:
        return [pointer(STEP72_COMMIT, AUTHORITY_PATH, f"/material_claims/{index}", record_id)
                for index, record_id in indices_and_ids] + [
            pointer(STEP72_COMMIT, AUTHORITY_PATH, f"/findings/{finding_index}", finding_id)
        ]

    whole_blend_metric = {**direct_metric, "status": "WHOLE_BLEND_METRIC_NOT_MATERIAL_SPECIFIC"}
    rows = [
        {
            "id": "E79-01",
            "claim": "Direct14 numerically reproduces the retained repository-derived CSV within the recorded in-sample tolerances.",
            "claim_class": "DIRECT14_SKEW_EMPIRICAL",
            "source_pointers": direct_pointers,
            "dataset_specimen_protocol_basis": direct_dataset,
            "profile_parameter_count": direct_profile,
            "in_sample_metric": direct_metric,
            "held_out_evidence": held_out("NOT_TESTED"),
            "noise_weighting": direct_noise,
            "information_criterion": direct_information,
            "identifiability": direct_identifiability,
            "independent_structural_thermodynamic_support": independent_support("GROUND_NOT_FOUND"),
            "empirical_pass": True,
            "external_authority": False,
            "phase_authority": False,
            "proposition_authority": False,
            "physical_authority": False,
            "empirical_ceiling": "IN_SAMPLE_NUMERICAL_REPLAY_OF_ONE_REPOSITORY_DERIVED_RT_C50_CSV",
            "physical_ceiling": "NO_PHASE_GALLERY_SPECIES_MATERIAL_OR_MECHANISM_IDENTIFICATION",
            "owner": "PHASE-066-STEP-079-EMPIRICAL-BOUNDARY",
            "status": fit["status"],
        },
        {
            "id": "E79-02",
            "claim": "The supplied Step 79 evidence establishes a complete competing-profile comparison and a transferable skew mechanism.",
            "claim_class": "COMPETING_PROFILE_EMPIRICAL",
            "source_pointers": [
                pointer(STEP78_COMMIT, PROVENANCE_PATH, "/source_code/4"),
                pointer(STEP78_COMMIT, PROVENANCE_PATH, "/source_code/5"),
                pointer(STEP72_COMMIT, AUTHORITY_PATH, "/material_claims/7", "M72-GR-08"),
            ],
            "dataset_specimen_protocol_basis": unavailable_dataset("INTERNAL_COMPETING_PROFILE_CALIBRATION"),
            "profile_parameter_count": unavailable_profile("COMPETING_PROFILE_UNIVERSE_GROUND_NOT_FOUND"),
            "in_sample_metric": unavailable_metric("EXACT_COMPETING_PROFILE_METRICS_GROUND_NOT_FOUND"),
            "held_out_evidence": held_out("NOT_TESTED"),
            "noise_weighting": noise("GROUND_NOT_FOUND_IN_STEP79_SOURCE_ROW"),
            "information_criterion": information("GROUND_NOT_FOUND", "GROUND_NOT_FOUND", "GROUND_NOT_FOUND"),
            "identifiability": identifiability("GROUND_NOT_FOUND"),
            "independent_structural_thermodynamic_support": independent_support("GROUND_NOT_FOUND"),
            "empirical_pass": False,
            "external_authority": False,
            "phase_authority": False,
            "proposition_authority": False,
            "physical_authority": False,
            "empirical_ceiling": material["M72-GR-08"]["ceiling"],
            "physical_ceiling": "NO_TRANSFERABLE_SKEW_MECHANISM_AUTHORITY",
            "owner": "PHASE-069-STEPS-102-104-MODEL-AND-DATA-SYNTHESIS",
            "status": "GROUND_NOT_FOUND",
        },
        {
            "id": "P79-03",
            "claim": "The whole-blend Direct14 components or frozen graphite profile labels establish graphite phase, gallery, or species identity.",
            "claim_class": "GRAPHITE_PHASE_GALLERY_AUTHORITY",
            "source_pointers": direct_pointers + material_pointers(
                [(2, "M72-GR-03"), (3, "M72-GR-04"), (4, "M72-GR-05"),
                 (6, "M72-GR-07"), (7, "M72-GR-08")], 2, "S72-F03"),
            "dataset_specimen_protocol_basis": direct_dataset,
            "profile_parameter_count": direct_profile,
            "in_sample_metric": whole_blend_metric,
            "held_out_evidence": held_out("NOT_TESTED"),
            "noise_weighting": direct_noise,
            "information_criterion": direct_information,
            "identifiability": direct_identifiability,
            "independent_structural_thermodynamic_support": independent_support("GROUND_NOT_FOUND"),
            "empirical_pass": False,
            "external_authority": False,
            "phase_authority": False,
            "proposition_authority": False,
            "physical_authority": False,
            "empirical_ceiling": "WHOLE_BLEND_CALIBRATION_IS_NOT_GRAPHITE_SPECIFIC_VALIDATION",
            "physical_ceiling": "IMPLEMENTATION_SEEDS_COMPONENTS_BOUNDS_AND_WIDTHS_DO_NOT_IDENTIFY_GRAPHITE_PHASES_OR_GALLERIES",
            "owner": findings["S72-F03"]["owner"],
            "status": "UNVERIFIED",
        },
        {
            "id": "P79-04",
            "claim": "The Direct14 fit establishes LCO phase, species, or thermodynamic-mechanism authority.",
            "claim_class": "LCO_PHASE_SPECIES_AUTHORITY",
            "source_pointers": material_pointers(
                [(11, "M72-LCO-03"), (12, "M72-LCO-04"), (15, "M72-LCO-07")],
                2, "S72-F03"),
            "dataset_specimen_protocol_basis": unavailable_dataset("NOT_APPLICABLE_DIRECT14_SPECIMEN_HAS_NO_LCO_SCOPE"),
            "profile_parameter_count": unavailable_profile("NOT_APPLICABLE"),
            "in_sample_metric": unavailable_metric("NOT_APPLICABLE"),
            "held_out_evidence": held_out("NOT_APPLICABLE"),
            "noise_weighting": noise("NOT_APPLICABLE"),
            "information_criterion": information("NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE"),
            "identifiability": identifiability("NOT_APPLICABLE"),
            "independent_structural_thermodynamic_support": independent_support("GROUND_NOT_FOUND"),
            "empirical_pass": False,
            "external_authority": False,
            "phase_authority": False,
            "proposition_authority": False,
            "physical_authority": False,
            "empirical_ceiling": "DIRECT14_BLEND_FIT_HAS_NO_LCO_EMPIRICAL_SCOPE",
            "physical_ceiling": "LCO_EXECUTABLE_ROUTE_SCOPE_TRANSFER_AND_REAL_O3_MULTI_TEMPERATURE_SUPPORT_REMAIN_UNVERIFIED_OR_GROUND_NOT_FOUND",
            "owner": findings["S72-F03"]["owner"],
            "status": "GROUND_NOT_FOUND",
        },
        {
            "id": "P79-05",
            "claim": "The whole-blend Direct14 fit isolates Si phases or proves a symmetric-Frumkin or width-based Si mechanism.",
            "claim_class": "SI_PHASE_MECHANISM_AUTHORITY",
            "source_pointers": direct_pointers + material_pointers(
                [(19, "M72-SI-03"), (20, "M72-SI-04"), (21, "M72-SI-05"),
                 (22, "M72-SI-06")], 2, "S72-F03"),
            "dataset_specimen_protocol_basis": direct_dataset,
            "profile_parameter_count": direct_profile,
            "in_sample_metric": whole_blend_metric,
            "held_out_evidence": held_out("NOT_TESTED"),
            "noise_weighting": direct_noise,
            "information_criterion": direct_information,
            "identifiability": direct_identifiability,
            "independent_structural_thermodynamic_support": independent_support("GROUND_NOT_FOUND"),
            "empirical_pass": False,
            "external_authority": False,
            "phase_authority": False,
            "proposition_authority": False,
            "physical_authority": False,
            "empirical_ceiling": "WHOLE_BLEND_CALIBRATION_DOES_NOT_ISOLATE_SI",
            "physical_ceiling": "DEMO_COMPONENTS_WIDTH_RATIOS_AND_SYMMETRIC_FRUMKIN_FORM_DO_NOT_PROVE_SI_PHASE_OR_SKEW_MECHANISM",
            "owner": findings["S72-F03"]["owner"],
            "status": "UNVERIFIED_OR_CONTRADICTED",
        },
        {
            "id": "P79-06",
            "claim": "Direct14 component areas on an absolute-mAh basis establish graphite/Si material fractions or a unique composition.",
            "claim_class": "BLEND_MATERIAL_FRACTION_AUTHORITY",
            "source_pointers": direct_pointers + material_pointers(
                [(23, "M72-BLEND-01"), (24, "M72-BLEND-02")], 2, "S72-F03"),
            "dataset_specimen_protocol_basis": direct_dataset,
            "profile_parameter_count": direct_profile,
            "in_sample_metric": whole_blend_metric,
            "held_out_evidence": held_out("NOT_TESTED"),
            "noise_weighting": direct_noise,
            "information_criterion": direct_information,
            "identifiability": direct_identifiability,
            "independent_structural_thermodynamic_support": independent_support("GROUND_NOT_FOUND"),
            "empirical_pass": False,
            "external_authority": False,
            "phase_authority": False,
            "proposition_authority": False,
            "physical_authority": False,
            "empirical_ceiling": "Q_IS_COMPONENT_AREA_ON_THE_FITTED_ABSOLUTE_MAH_BASIS_ONLY",
            "physical_ceiling": "NO_MASS_FRACTION_COMPOSITION_OR_COMMON_REVERSIBLE_CAPACITY_BASIS_AUTHORITY",
            "owner": findings["S72-F03"]["owner"],
            "status": "UNVERIFIED_INCOMPATIBLE_CAPACITY_KINDS",
        },
        {
            "id": "P79-07",
            "claim": "A whole-curve fit tests finite-rate host independence, current partition, or nonadditive blend behavior.",
            "claim_class": "BLEND_FINITE_RATE_AUTHORITY",
            "source_pointers": direct_pointers + material_pointers(
                [(26, "M72-BLEND-04"), (27, "M72-BLEND-05")], 3, "S72-F04"),
            "dataset_specimen_protocol_basis": direct_dataset,
            "profile_parameter_count": direct_profile,
            "in_sample_metric": {**direct_metric, "status": "WHOLE_CURVE_METRIC_NOT_CURRENT_PARTITION_TEST"},
            "held_out_evidence": held_out("NOT_TESTED"),
            "noise_weighting": direct_noise,
            "information_criterion": direct_information,
            "identifiability": direct_identifiability,
            "independent_structural_thermodynamic_support": independent_support("GROUND_NOT_FOUND"),
            "empirical_pass": False,
            "external_authority": False,
            "phase_authority": False,
            "proposition_authority": False,
            "physical_authority": False,
            "empirical_ceiling": "WHOLE_CURVE_IN_SAMPLE_CALIBRATION_ONLY",
            "physical_ceiling": "NO_I_EQUALS_I_GRAPHITE_PLUS_I_SI_HOST_INDEPENDENCE_OR_NONADDITIVE_FINITE_RATE_AUTHORITY",
            "owner": findings["S72-F04"]["owner"],
            "status": "UNVERIFIED_OR_ABSENT",
        },
        {
            "id": "P79-08",
            "claim": "Bibliographic metadata for asserted Ref. 7 establishes the exact proposition, equation, and graphite applicability.",
            "claim_class": "REF7_PRIMARY_AUTHORITY",
            "source_pointers": [
                pointer(STEP72_COMMIT, AUTHORITY_PATH, "/metadata_verifications/5", "10.1063/1.4802584"),
                pointer(STEP72_COMMIT, AUTHORITY_PATH, "/findings/5", "S72-F06"),
            ],
            "dataset_specimen_protocol_basis": unavailable_dataset("BIBLIOGRAPHIC_METADATA_ONLY"),
            "profile_parameter_count": unavailable_profile("NOT_APPLICABLE"),
            "in_sample_metric": unavailable_metric("NOT_APPLICABLE"),
            "held_out_evidence": held_out("NOT_APPLICABLE"),
            "noise_weighting": noise("NOT_APPLICABLE"),
            "information_criterion": information("NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE"),
            "identifiability": identifiability("NOT_APPLICABLE"),
            "independent_structural_thermodynamic_support": independent_support(
                metadata["10.1063/1.4802584"]["primary_text"]),
            "empirical_pass": False,
            "external_authority": False,
            "phase_authority": False,
            "proposition_authority": False,
            "physical_authority": False,
            "empirical_ceiling": "METADATA_IDENTITY_OBSERVATION_ONLY",
            "physical_ceiling": "NO_PROPOSITION_PAGE_EQUATION_OR_GRAPHITE_APPLICABILITY_AUTHORITY",
            "owner": metadata["10.1063/1.4802584"]["owner"],
            "status": "GROUND_NOT_FOUND",
        },
    ]
    return rows


def build() -> None:
    sources: list[tuple[str, str, bytes, str]] = []
    for commit, path in (
        (STEP78_COMMIT, FIT_PATH),
        (STEP78_COMMIT, PROVENANCE_PATH),
        (STEP78_COMMIT, VECTOR_PATH),
        (STEP72_COMMIT, AUTHORITY_PATH),
    ):
        raw, blob = git_blob(commit, path)
        sources.append((commit, path, raw, blob))
    fit, provenance, vector, authority = [strict_json(item[2]) for item in sources]
    rows = build_rows(fit, provenance, vector, authority)
    result = {
        "schema_version": "phase066-step79-empirical-physical-authority-matrix-v1",
        "phase": 66,
        "step": 79,
        "gate": GATE,
        "expected_parent": STEP78_COMMIT,
        "generator_identity": {
            "path": BUILDER_PATH,
            "raw_sha256": sha256((ROOT / BUILDER_PATH).read_bytes()),
        },
        "inputs": [input_record(*item) for item in sources],
        "source_gates": {
            "step77_gate": fit["gate"],
            "step77_runtime_success": fit["runtime_success"],
            "step77_selected_trial_converged": fit["selected_trial_converged"],
            "step77_external_process_evidence": {
                run["runtime_label"]: {
                    "argv": run["external_process_evidence"]["argv"],
                    "cwd": run["external_process_evidence"]["cwd"],
                    "exit_code": run["external_process_evidence"]["exit_code"],
                    "stdout_sha256": run["external_process_evidence"]["stdout_sha256"],
                    "stderr_sha256": run["external_process_evidence"]["stderr_sha256"],
                }
                for run in fit["runtime_reproductions"]
            },
        },
        "claim_rows": rows,
        "aggregate": {
            "rows": len(rows),
            "empirical_pass_true": sum(row["empirical_pass"] for row in rows),
            "external_authority_true": sum(row["external_authority"] for row in rows),
            "phase_authority_true": sum(row["phase_authority"] for row in rows),
            "proposition_authority_true": sum(row["proposition_authority"] for row in rows),
            "physical_authority_true": sum(row["physical_authority"] for row in rows),
            "held_out_not_tested": sum(row["held_out_evidence"]["status"] == "NOT_TESTED" for row in rows),
            "primary_text_ground_not_found": sum(row["id"] == "P79-08" and row["status"] == "GROUND_NOT_FOUND" for row in rows),
        },
        "authority_ceiling": {
            "in_sample_fit_is_external_validation": False,
            "component_basis_is_phase_gallery_species_identity": False,
            "parameter_label_is_material_constant_or_fraction": False,
            "curve_equivalence_is_identifiability_or_mechanism": False,
            "metadata_is_proposition_support": False,
            "room_temperature_fit_is_multi_temperature_authority": False,
            "empirical_pass_implies_physical_authority": False,
            "whole_blend_metric_is_material_specific_validation": False,
            "whole_curve_fit_is_finite_rate_current_partition_test": False,
        },
    }
    raw = canonical_bytes(seal(result))
    temporary = OUTPUT_PATH.with_name(OUTPUT_PATH.name + ".step79.tmp")
    try:
        temporary.write_bytes(raw)
        os.replace(temporary, OUTPUT_PATH)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"{GATE} rows={len(rows)} empirical_pass=1 physical_authority=0")


if __name__ == "__main__":
    try:
        build()
    except (BuildFailure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL_P066_STEP79_BUILD {error}")
        raise SystemExit(1)
