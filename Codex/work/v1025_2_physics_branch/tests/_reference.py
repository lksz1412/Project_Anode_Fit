"""Independent frozen-data reconstruction helpers used only by the tests."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy.optimize import isotonic_regression
from scipy.signal import savgol_filter


TEST_ROOT = Path(__file__).resolve().parent
BRANCH_WORK_ROOT = TEST_ROOT.parent
REPO_ROOT = TEST_ROOT.parents[3]
FIT_SUMMARY = (
    REPO_ROOT
    / "Claude/results/comp_v26_data/out_versions/summary_versions.json"
)
BLEND_DATA = REPO_ROOT / "Claude/results/comp_v24/sintef_data/sigr.csv"

EXPECTED_HASHES = {
    "voltage": "6c7ca15d7b9eaf80561d2d2d834856c9b3076f31f6d7e4e6ce304ddb266020b4",
    "observed": "da0beeb95e2eac332e870e2a342354109f611503d5641a6c3c3045871f9d791e",
    "parameters": "08216da1095a02bcb789a60f577f4afd1d581ad659a8129edaba7dc0dc5910d5",
    "prediction": "53cc3c3795be327b90a5d040497074bc51f5a141d0b7629bd34a60682d71f800",
    "residual": "1b874701ac72403f2836b352386e3c3a4f658c49238fd2fcf0a4931fd79398ec",
}
EXPECTED_R2 = 0.99964941790404
EXPECTED_SOURCE_SHA256 = (
    "e571a66fb9574c4aa7bfdec7acada2eb732029232e7ab83dc7d9645e39fb01e6"
)


def import_model():
    """Import the candidate package without installing it."""

    branch_path = str(BRANCH_WORK_ROOT)
    if branch_path not in sys.path:
        sys.path.insert(0, branch_path)
    import conformance_model

    return conformance_model


def le_f64_sha256(values) -> str:
    canonical = np.ascontiguousarray(np.asarray(values, dtype="<f8"))
    return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


def stored_blend_payload() -> dict:
    payload = json.loads(FIT_SUMMARY.read_text(encoding="utf-8"))
    return payload["C_skew"]["blend"]


def stored_parameter_vector() -> np.ndarray:
    return np.asarray(stored_blend_payload()["params"], dtype=float)


def _savgol_ensemble(data: np.ndarray) -> np.ndarray:
    values = np.asarray(data, dtype=float)
    length = len(values)
    ensemble = [values]
    for ratio in (0.01, 0.02, 0.03):
        window = int(round(length * ratio // 2)) * 2 + 1
        if window <= 3 or window >= length:
            continue
        try:
            ensemble.append(savgol_filter(values, window, 3))
        except Exception:
            pass
        try:
            with np.errstate(divide="ignore", invalid="ignore"):
                ensemble.append(1.0 / savgol_filter(1.0 / values, window, 3))
        except Exception:
            pass
    array = np.asarray(ensemble, dtype=float)
    array[~np.isfinite(array)] = np.nan
    with np.errstate(invalid="ignore"):
        return np.nanmedian(array, axis=0)


def processed_blend_curve() -> tuple[np.ndarray, np.ndarray]:
    """Reproduce the complete active preprocessing body from source data."""

    frame = pd.read_csv(BLEND_DATA)
    voltage_column = next(c for c in frame.columns if c.lower().startswith("v"))
    capacity_column = next(c for c in frame.columns if c.lower().startswith("q"))
    voltage = frame[voltage_column].to_numpy(float)
    capacity = frame[capacity_column].to_numpy(float)

    finite = np.isfinite(voltage) & np.isfinite(capacity)
    voltage, capacity = voltage[finite], capacity[finite]
    order = np.argsort(capacity, kind="mergesort")
    voltage, capacity = voltage[order], capacity[order]
    unique_capacity, unique_indices = np.unique(capacity, return_index=True)
    unique_voltage = voltage[unique_indices]
    monotonic_voltage = isotonic_regression(unique_voltage, increasing=True).x

    delta_voltage = 5.0e-4
    edges = np.arange(0.060, 0.700 + 0.5 * delta_voltage, delta_voltage)
    indices = np.searchsorted(monotonic_voltage, edges, side="right") - 1
    rebinned_capacity = np.where(
        indices >= 0,
        unique_capacity[np.clip(indices, 0, len(unique_capacity) - 1)],
        0.0,
    )
    centers = 0.5 * (edges[:-1] + edges[1:])
    derivative = np.diff(rebinned_capacity) / delta_voltage

    valid_indices = np.flatnonzero(np.isfinite(derivative) & (derivative > 0))
    if valid_indices.size == 0:
        raise RuntimeError("active preprocessing produced no positive segment")
    runs = np.split(valid_indices, np.flatnonzero(np.diff(valid_indices) > 1) + 1)
    longest = max(runs, key=len)
    start, stop = int(longest[0]), int(longest[-1]) + 1
    return centers[start:stop], np.abs(_savgol_ensemble(derivative[start:stop]))


def coefficient_of_determination(observed, predicted) -> float:
    observed_array = np.asarray(observed, dtype=float)
    predicted_array = np.asarray(predicted, dtype=float)
    residual_sum = float(np.sum((observed_array - predicted_array) ** 2))
    centered_sum = float(
        np.sum((observed_array - observed_array.mean()) ** 2)
    )
    return 1.0 - residual_sum / centered_sum


def canonical_release_prediction(voltage) -> np.ndarray:
    """Independent piecewise-logistic reconstruction of the stored profile."""

    voltage_array = np.asarray(voltage, dtype=float)
    parameters = stored_parameter_vector()
    component_count = 14
    prediction = np.full_like(voltage_array, parameters[-1], dtype=float)
    for index in range(component_count):
        center = parameters[index]
        width = parameters[component_count + index]
        area = parameters[2 * component_count + index]
        alpha = parameters[3 * component_count + index]
        z = (voltage_array - center) / width
        sigma = np.empty_like(z)
        nonnegative = z >= 0
        sigma[nonnegative] = 1.0 / (1.0 + np.exp(-z[nonnegative]))
        exp_z = np.exp(z[~nonnegative])
        sigma[~nonnegative] = exp_z / (1.0 + exp_z)
        prediction += (
            area
            * (alpha / width)
            * np.power(sigma, alpha)
            * (1.0 - sigma)
        )
    return prediction


def local_network_expected_w(
    total_charge_c: float,
    electron_stoichiometry: float,
    temperature_k: float,
    forward_flux_s_inverse: float,
    backward_flux_s_inverse: float,
) -> float:
    gas_constant = 8.31446261815324
    faraday = 96485.33212
    return (
        total_charge_c
        / (electron_stoichiometry * faraday)
        * gas_constant
        * temperature_k
        * (forward_flux_s_inverse - backward_flux_s_inverse)
        * math.log(forward_flux_s_inverse / backward_flux_s_inverse)
    )
