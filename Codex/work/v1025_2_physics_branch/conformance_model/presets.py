"""Named, immutable profile entry points."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .empirical import (
    EmpiricalArtifactMetadata,
    EmpiricalEvaluationContract,
    EmpiricalSkewComponent,
    EmpiricalSkewProfile,
    little_endian_f64_sha256,
)
from .observation import ObservationContract


EMPIRICAL_BLEND14_V10252_ARTIFACT = (
    Path(__file__).resolve().parents[3]
    / "results/v1025_2_physics_branch/artifacts/empirical_blend14_v10252.json"
)
_EMPIRICAL_BLEND14_V10252_ARTIFACT_SHA256 = (
    "5f352eb95f0fe70cf4f277d4d3073015d3f43db04cc0471d4c016bf270aaea6a"
)
_EMPIRICAL_BLEND14_V10252_PARAMETER_SHA256 = (
    "08216da1095a02bcb789a60f577f4afd1d581ad659a8129edaba7dc0dc5910d5"
)
_EMPIRICAL_BLEND14_V10252_SOURCE_SHA256 = (
    "e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6"
)


def empirical_blend14_v10252() -> EmpiricalSkewProfile:
    """Load the exact surviving stored-8dp blend14 empirical preset.

    The artifact and its parameter-vector hash are validated on every load.
    No process-global default, mutable toggle, host label, or physical
    interpretation is installed.

    Physics IDs: PHY-004, PHY-007, PHY-012, PHY-028, PHY-029, PHY-030,
    PHY-032.
    """

    artifact_bytes = EMPIRICAL_BLEND14_V10252_ARTIFACT.read_bytes()
    artifact_hash = hashlib.sha256(artifact_bytes).hexdigest()
    if artifact_hash != _EMPIRICAL_BLEND14_V10252_ARTIFACT_SHA256:
        raise ValueError("immutable empirical artifact file hash mismatch")
    payload = json.loads(artifact_bytes.decode("utf-8"))
    if payload["profile_id"] != "empirical_blend14_v10252":
        raise ValueError("unexpected empirical artifact profile_id")
    if payload["source_data"]["sha256"] != _EMPIRICAL_BLEND14_V10252_SOURCE_SHA256:
        raise ValueError("empirical source-data hash contract changed")
    parameter_contract = payload["parameter_contract"]
    parameters = tuple(
        float(value) for value in parameter_contract["parameters_stored_8dp"]
    )
    count = int(parameter_contract["component_count"])
    expected_count = 4 * count + 1
    if len(parameters) != expected_count:
        raise ValueError(
            f"artifact has {len(parameters)} parameters; expected {expected_count}"
        )
    expected_hash = payload["sha256_le_f64_no_header"]["stored_8dp_parameters"]
    if expected_hash != _EMPIRICAL_BLEND14_V10252_PARAMETER_SHA256:
        raise ValueError("empirical parameter hash contract changed")
    observed_hash = little_endian_f64_sha256(parameters)
    if observed_hash != expected_hash:
        raise ValueError("stored-8dp empirical parameter hash mismatch")

    components = tuple(
        EmpiricalSkewComponent(
            center_v=parameters[index],
            width_v=parameters[count + index],
            area_mAh=parameters[2 * count + index],
            alpha=parameters[3 * count + index],
        )
        for index in range(count)
    )
    data_contract = payload["processed_data_contract"]
    optimizer = payload["optimizer_evidence"]
    source_data = payload["source_data"]
    hash_items = tuple(payload["sha256_le_f64_no_header"].items())
    metadata = EmpiricalArtifactMetadata(
        schema_version=payload["schema_version"],
        profile_id=payload["profile_id"],
        classification=payload["classification"],
        evidence_grade=payload["evidence_grade"],
        source_path=source_data["path"],
        source_sha256=source_data["sha256"],
        experimental_protocol=source_data["experimental_protocol"],
        processed_points=int(data_contract["processed_points"]),
        voltage_window_v=tuple(data_contract["voltage_window_v"]),
        voltage_bin_width_v=float(data_contract["voltage_bin_width_v"]),
        residual_contract=data_contract["residual"],
        preprocessing_steps=tuple(data_contract["active_preprocessing"]),
        parameter_order=tuple(parameter_contract["parameter_order"]),
        stored_decimal_places=int(parameter_contract["stored_decimal_places"]),
        array_hash_items=hash_items,
        optimizer_full_precision_available=bool(
            optimizer["full_precision_vector_available"]
        ),
        optimizer_prediction_available=bool(
            optimizer["original_prediction_available"]
        ),
        optimizer_termination_metadata_available=bool(
            optimizer["termination_metadata_available"]
        ),
        optimizer_active_set_status_available=bool(
            optimizer["active_set_status_available"]
        ),
        builder_required_optimizer_success=bool(
            optimizer["builder_required_optimizer_success"]
        ),
        optimizer_search_evidence=tuple(optimizer["declared_search_contract"]),
        authority_note=payload["authority_note"],
    )
    observation = ObservationContract.magnitude(
        payload["observation_contract"]["provenance"]
    )
    profile = EmpiricalSkewProfile(
        components=components,
        background_mAh_per_v=parameters[-1],
        observation_contract=observation,
        metadata=metadata,
        evaluation_contract=EmpiricalEvaluationContract(
            payload["reconstruction"]["evaluation_contract"]
        ),
    )
    if profile.parameter_vector_8dp() != parameters:
        raise ValueError("empirical preset reconstruction changed parameter order")
    return profile
