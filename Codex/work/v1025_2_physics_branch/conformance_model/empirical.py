"""Positive empirical skew-logistic observation profiles.

Nothing in this module is a chemical occupancy, host assignment, reaction
extent, entropy state, or heat state.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
from types import MappingProxyType
from typing import Mapping

import numpy as np

from .constants import (
    V10252_EMPIRICAL_RECONSTRUCTION_F,
    V10252_EMPIRICAL_RECONSTRUCTION_R,
    V10252_EMPIRICAL_RECONSTRUCTION_T_K,
)
from .numerics import (
    ScalarOrArray,
    as_finite_float,
    as_positive_float,
    finite_array,
    safe_logistic,
    scalarize_like,
)
from .observation import ObservationContract, ObservationMode


class EmpiricalEvaluationContract(str, Enum):
    """Floating-point evaluation contract for an empirical artifact."""

    DIRECT = "direct-empirical"
    V10252_RELEASE_RECONSTRUCTION = "v1.0.25.2-release-reconstruction"


def little_endian_f64_sha256(values: ScalarOrArray) -> str:
    """Hash a C-contiguous little-endian float64 payload without a header."""

    canonical = np.ascontiguousarray(np.asarray(values, dtype="<f8"))
    return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


@dataclass(frozen=True, slots=True)
class EmpiricalArtifactMetadata:
    """Immutable provenance carried with an empirical profile.

    Physics IDs: PHY-028, PHY-029, PHY-030, PHY-032.
    """

    schema_version: str
    profile_id: str
    classification: str
    evidence_grade: str
    source_path: str
    source_sha256: str
    experimental_protocol: str
    processed_points: int
    voltage_window_v: tuple[float, float]
    voltage_bin_width_v: float
    residual_contract: str
    preprocessing_steps: tuple[str, ...]
    parameter_order: tuple[str, ...]
    stored_decimal_places: int
    array_hash_items: tuple[tuple[str, str], ...]
    optimizer_full_precision_available: bool
    optimizer_prediction_available: bool
    optimizer_termination_metadata_available: bool
    optimizer_active_set_status_available: bool
    builder_required_optimizer_success: bool
    optimizer_search_evidence: tuple[str, ...]
    authority_note: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "preprocessing_steps", tuple(self.preprocessing_steps)
        )
        object.__setattr__(self, "parameter_order", tuple(self.parameter_order))
        object.__setattr__(self, "array_hash_items", tuple(self.array_hash_items))
        object.__setattr__(
            self, "optimizer_search_evidence", tuple(self.optimizer_search_evidence)
        )
        if not self.schema_version.strip() or not self.profile_id.strip():
            raise ValueError("schema_version and profile_id must be nonempty")
        if self.processed_points <= 0:
            raise ValueError("processed_points must be > 0")
        low, high = (float(v) for v in self.voltage_window_v)
        if not np.isfinite(low) or not np.isfinite(high) or not low < high:
            raise ValueError("voltage_window_v must be a finite increasing pair")
        object.__setattr__(self, "voltage_window_v", (low, high))
        as_positive_float("voltage_bin_width_v", self.voltage_bin_width_v)
        if self.stored_decimal_places < 0:
            raise ValueError("stored_decimal_places must be >= 0")
        names = [name for name, _ in self.array_hash_items]
        if len(names) != len(set(names)):
            raise ValueError("array hash names must be unique")
        for name, digest in self.array_hash_items:
            if not name or len(digest) != 64:
                raise ValueError("array hashes require a name and SHA-256 digest")

    @property
    def hashes(self) -> Mapping[str, str]:
        """Read-only mapping of canonical array names to SHA-256 digests."""

        return MappingProxyType(dict(self.array_hash_items))


@dataclass(frozen=True, slots=True)
class EmpiricalSkewComponent:
    """One positive, area-preserving skew-logistic observation component.

    ``area_mAh`` is an observation area and is never a signed chemical storage
    coefficient.

    Physics IDs: PHY-004, PHY-007, PHY-009, PHY-029, PHY-032.
    """

    center_v: float
    width_v: float
    area_mAh: float
    alpha: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "center_v", as_finite_float("center_v", self.center_v))
        object.__setattr__(self, "width_v", as_positive_float("width_v", self.width_v))
        area = as_finite_float("area_mAh", self.area_mAh)
        if area < 0.0:
            raise ValueError("area_mAh must be >= 0 for an empirical profile")
        object.__setattr__(self, "area_mAh", area)
        object.__setattr__(self, "alpha", as_positive_float("alpha", self.alpha))

    def cumulative(self, voltage_v: ScalarOrArray) -> ScalarOrArray:
        """Return the unit empirical cumulative coordinate ``sigma**alpha``."""

        voltage = finite_array("voltage_v", voltage_v)
        sigma = np.asarray(
            safe_logistic((voltage - self.center_v) / self.width_v),
            dtype=np.float64,
        )
        result = np.power(sigma, self.alpha)
        return scalarize_like(voltage_v, result)

    def density(self, voltage_v: ScalarOrArray) -> ScalarOrArray:
        """Return the nonnegative unit-area derivative of the cumulative."""

        voltage = finite_array("voltage_v", voltage_v)
        sigma = np.asarray(
            safe_logistic((voltage - self.center_v) / self.width_v),
            dtype=np.float64,
        )
        cumulative = np.power(sigma, self.alpha)
        result = (self.alpha / self.width_v) * cumulative * (1.0 - sigma)
        return scalarize_like(voltage_v, result)


@dataclass(frozen=True, slots=True)
class EmpiricalSkewProfile:
    """Positive empirical observation profile, separate from physical hosts.

    The profile accepts only a magnitude observation contract.  Its component
    amplitudes and cumulative coordinates must not enter physical charge
    balance, entropy, kinetics, or heat calculations.

    Physics IDs: PHY-004, PHY-007, PHY-009, PHY-012, PHY-028, PHY-029,
    PHY-030, PHY-032.
    """

    components: tuple[EmpiricalSkewComponent, ...]
    background_mAh_per_v: float
    observation_contract: ObservationContract
    metadata: EmpiricalArtifactMetadata
    evaluation_contract: EmpiricalEvaluationContract = EmpiricalEvaluationContract.DIRECT

    def __post_init__(self) -> None:
        components = tuple(self.components)
        if not components:
            raise ValueError("an empirical profile requires at least one component")
        if not all(isinstance(item, EmpiricalSkewComponent) for item in components):
            raise TypeError("components must contain only EmpiricalSkewComponent")
        object.__setattr__(self, "components", components)

        background = as_finite_float(
            "background_mAh_per_v", self.background_mAh_per_v
        )
        if background < 0.0:
            raise ValueError(
                "background_mAh_per_v must be >= 0 for a positive observation"
            )
        object.__setattr__(self, "background_mAh_per_v", background)

        if not isinstance(self.observation_contract, ObservationContract):
            raise TypeError("observation_contract must be ObservationContract")
        if self.observation_contract.mode is not ObservationMode.MAGNITUDE:
            raise ValueError(
                "EmpiricalSkewProfile requires an explicit magnitude contract"
            )
        if not isinstance(self.metadata, EmpiricalArtifactMetadata):
            raise TypeError("metadata must be EmpiricalArtifactMetadata")
        object.__setattr__(
            self,
            "evaluation_contract",
            EmpiricalEvaluationContract(self.evaluation_contract),
        )

    @property
    def hashes(self) -> Mapping[str, str]:
        """Read-only canonical hashes carried by the artifact metadata."""

        return self.metadata.hashes

    def parameter_vector_8dp(self) -> tuple[float, ...]:
        """Return ``U, w, area, alpha, background`` in frozen component order."""

        return (
            *(component.center_v for component in self.components),
            *(component.width_v for component in self.components),
            *(component.area_mAh for component in self.components),
            *(component.alpha for component in self.components),
            self.background_mAh_per_v,
        )

    def _evaluation_width(self, component: EmpiricalSkewComponent) -> float:
        if (
            self.evaluation_contract
            is EmpiricalEvaluationContract.V10252_RELEASE_RECONSTRUCTION
        ):
            # Preserve the exact operation order of the surviving release
            # reconstruction.  This is a frozen empirical hash contract, not a
            # temperature-dependent physical width.
            n_value = (
                component.width_v
                * V10252_EMPIRICAL_RECONSTRUCTION_F
                / (
                    V10252_EMPIRICAL_RECONSTRUCTION_R
                    * V10252_EMPIRICAL_RECONSTRUCTION_T_K
                )
            )
            return (
                n_value
                * V10252_EMPIRICAL_RECONSTRUCTION_R
                * V10252_EMPIRICAL_RECONSTRUCTION_T_K
                / V10252_EMPIRICAL_RECONSTRUCTION_F
            )
        return component.width_v

    def evaluate(self, voltage_v: ScalarOrArray) -> ScalarOrArray:
        """Evaluate the frozen positive observation model.

        Summation and multiplication order is preserved for the v1.0.25.2
        reconstruction contract so its archived prediction hash can be tested.
        """

        voltage = finite_array("voltage_v", voltage_v)
        prediction = np.full(voltage.shape, self.background_mAh_per_v, dtype=np.float64)
        for component in self.components:
            width = self._evaluation_width(component)
            sigma = np.asarray(
                safe_logistic((voltage - component.center_v) / width),
                dtype=np.float64,
            )
            cumulative = np.power(sigma, component.alpha)
            derivative = (
                (component.alpha / width) * cumulative * (1.0 - sigma)
            )
            prediction = prediction + component.area_mAh * derivative
        return scalarize_like(voltage_v, prediction)
