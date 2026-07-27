#!/usr/bin/env python3
"""Independent probes for the v1.0.25.2 physics-conformance audit.

This script reads the accepted v1.0.25.2 source and fit artifacts without
modifying them.  It intentionally does not import the historical fit driver,
because that driver creates/truncates output files at import time.
"""

from __future__ import annotations

import importlib.util
import hashlib
import json
import math
from pathlib import Path
import sys
import warnings

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import isotonic_regression, least_squares
from scipy.signal import savgol_filter


REPO = Path(__file__).resolve().parents[3]
SOURCE = REPO / "Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py"
FIT_ROOT = REPO / "Claude/results/comp_v26_data"
FIT_SUMMARY = FIT_ROOT / "out_versions/summary_versions.json"
FIT_ROUNDED = FIT_ROOT / "out_versions/C_skew/params_blend.json"
BLEND_DATA = REPO / "Claude/results/comp_v24/sintef_data/sigr.csv"


def little_endian_f64_sha256(values: np.ndarray) -> str:
    """Hash a C-contiguous little-endian float64 payload without a header."""
    canonical = np.ascontiguousarray(np.asarray(values, dtype="<f8"))
    return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


def load_module():
    spec = importlib.util.spec_from_file_location("anode_fit_v1025_2_probe", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def savgol_ensemble(data: np.ndarray, ratios=(0.01, 0.02, 0.03)) -> np.ndarray:
    """Exact smoothing operation used by test_skew_regsol_v2.load_dqdv."""
    values = np.asarray(data, dtype=float)
    length = len(values)
    ensemble = [values]
    for ratio in ratios:
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


def load_blend_dqdv() -> tuple[np.ndarray, np.ndarray]:
    """Exact active preprocessing body used by the accepted fit driver."""
    frame = pd.read_csv(BLEND_DATA)
    voltage_column = next(c for c in frame.columns if c.lower().startswith("v"))
    capacity_column = next(c for c in frame.columns if c.lower().startswith("q"))
    voltage = frame[voltage_column].to_numpy(float)
    capacity = frame[capacity_column].to_numpy(float)

    valid = np.isfinite(voltage) & np.isfinite(capacity)
    voltage, capacity = voltage[valid], capacity[valid]
    order = np.argsort(capacity, kind="mergesort")
    voltage, capacity = voltage[order], capacity[order]
    unique_capacity, unique_indices = np.unique(capacity, return_index=True)
    unique_voltage = voltage[unique_indices]
    monotonic_voltage = isotonic_regression(unique_voltage, increasing=True).x

    voltage_low, voltage_high, delta_voltage = 0.060, 0.700, 5.0e-4
    grid = np.arange(voltage_low, voltage_high + 0.5 * delta_voltage, delta_voltage)
    indices = np.searchsorted(monotonic_voltage, grid, side="right") - 1
    rebinned_capacity = np.where(
        indices >= 0,
        unique_capacity[np.clip(indices, 0, len(unique_capacity) - 1)],
        0.0,
    )
    centers = 0.5 * (grid[:-1] + grid[1:])
    derivative = np.diff(rebinned_capacity) / delta_voltage
    keep = np.isfinite(derivative) & (derivative > 0)
    valid_indices = np.flatnonzero(keep)
    if valid_indices.size == 0:
        raise RuntimeError("accepted preprocessing produced no valid dQ/dV segment")
    runs = np.split(valid_indices, np.flatnonzero(np.diff(valid_indices) > 1) + 1)
    longest = max(runs, key=len)
    start, stop = int(longest[0]), int(longest[-1]) + 1
    centers = centers[start:stop]
    derivative = derivative[start:stop]
    derivative = np.abs(savgol_ensemble(derivative))
    return centers, derivative


def transitions_from_stored_8dp(
    parameters: list[float], count: int
) -> tuple[list[dict], float]:
    p = np.asarray(parameters, dtype=float)
    transitions = []
    for index in range(count):
        transitions.append(
            {
                "U": float(p[index]),
                "w": float(p[count + index]),
                "Q": float(p[2 * count + index]),
                "alpha": float(p[3 * count + index]),
            }
        )
    return transitions, float(p[-1])


def transitions_from_rounded(payload: dict) -> tuple[list[dict], float]:
    transitions = [
        {
            "U": float(item["U"]),
            "w": float(item["w"]),
            "Q": float(item["Q"]),
            "alpha": float(item["alpha"]),
        }
        for item in payload["transitions"]
    ]
    return transitions, float(payload["metrics"]["bg"])


def metrics(observed: np.ndarray, predicted: np.ndarray, parameter_count: int) -> dict:
    residual_sum = float(np.sum((observed - predicted) ** 2))
    centered_sum = float(np.sum((observed - observed.mean()) ** 2))
    sample_count = observed.size
    return {
        "R2": 1.0 - residual_sum / centered_sum,
        "BIC": sample_count * math.log(max(residual_sum, 1e-300) / sample_count)
        + parameter_count * math.log(sample_count),
    }


def run() -> dict:
    model = load_module()
    result: dict[str, object] = {
        "source": str(SOURCE.relative_to(REPO)),
        "fit_summary": str(FIT_SUMMARY.relative_to(REPO)),
        "blend_data": str(BLEND_DATA.relative_to(REPO)),
        "blend_data_label": "blend",
        "blend_experimental_protocol": "UNKNOWN",
        "environment": {
            "role": (
                "Phase 044 reconstruction environment; original optimizer "
                "environment is unavailable"
            ),
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": scipy.__version__,
            "array_hash_contract": "C-contiguous little-endian float64 payload; no header",
        },
    }

    # 1. Current default construction and default-background consumption.
    blend_default = model.BlendedAnodeDQDV(0.2)
    result["current_default"] = {
        "graphite_transition_count": len(blend_default.gr_host.transitions),
        "silicon_transition_count": len(blend_default.si_host.transitions),
        "graphite_Cbg": float(blend_default.gr_host.Cbg),
        "silicon_Cbg": float(blend_default.si_host.Cbg),
        "declared_DEFAULT_CBG_GRAPHITE": float(model.DEFAULT_CBG_GRAPHITE),
        "declared_DEFAULT_CBG_SI": float(model.DEFAULT_CBG_SI),
    }

    invalid_case_accepted = False
    invalid_case_error = None
    try:
        invalid_case = model.BlendedAnodeDQDV(0.2, si_case="not-a-real-case")
        invalid_case_accepted = len(invalid_case.si_host.transitions) == 7
    except Exception as exc:  # pragma: no cover - records either behavior
        invalid_case_error = f"{type(exc).__name__}: {exc}"
    result["si_case_validation"] = {
        "invalid_case_accepted": invalid_case_accepted,
        "error": invalid_case_error,
    }

    # 2. Keyless-transition width derivative and thermodynamic round trip.
    keyless = {"U": 0.1, "Q": 1.0}
    keyless_host = model.GraphiteAnodeDischargeDQDV([keyless])
    temperature = 298.15
    delta_temperature = 1.0e-3
    width_fd = (
        float(keyless_host._width(keyless, temperature + delta_temperature))
        - float(keyless_host._width(keyless, temperature - delta_temperature))
    ) / (2.0 * delta_temperature)
    width_analytic = float(keyless_host._dwdT(keyless, temperature))
    x_bar = 0.25
    uoc_fd = (
        float(keyless_host.solve_U_oc(x_bar, temperature + delta_temperature))
        - float(keyless_host.solve_U_oc(x_bar, temperature - delta_temperature))
    ) / (2.0 * delta_temperature)
    entropy_reported = float(keyless_host.entropy_coefficient_x(x_bar, temperature))
    result["keyless_temperature_roundtrip"] = {
        "width_fd_V_per_K": width_fd,
        "width_reported_V_per_K": width_analytic,
        "Uoc_fd_V_per_K": uoc_fd,
        "entropy_reported_V_per_K": entropy_reported,
    }

    # 3. Eager np.where overflow warnings in the nominally stable logistic helper.
    voltage_grid = np.linspace(0.060, 0.300, 1200)
    caught = []
    with warnings.catch_warnings(record=True) as warning_records:
        warnings.simplefilter("always")
        for transition in model.GRAPHITE_MSMR7_LIT:
            n_value = float(transition["w"]) * model.F / (model.R * temperature)
            values = model.func_ksi_eq(
                temperature, voltage_grid, float(transition["U"]), n_value
            )
            if not np.all(np.isfinite(values)):
                caught.append("non-finite-output")
        caught.extend(
            f"{record.category.__name__}: {record.message}"
            for record in warning_records
        )
    result["logistic_warning_probe"] = {
        "warning_count": len(caught),
        "warnings": caught,
    }

    # 4. Rate-time representation and causal-pad edge contracts.
    activation_enthalpy = 50_000.0
    affinity = 4.0 * model.R * temperature
    lag_hour_basis = float(
        model.func_L_q(
            temperature, 1.0, 1.0, activation_enthalpy, 0.0, 0.5, affinity
        )
    )
    lag_second_basis = float(
        model.func_L_q(
            temperature,
            1.0 / 3600.0,
            1.0,
            activation_enthalpy,
            0.0,
            0.5,
            affinity,
        )
    )
    duplicate_voltage = np.asarray([0.10, 0.10, 0.11], dtype=float)
    _, duplicate_pad_points = model._causal_pad(duplicate_voltage, 0.02)
    result["rate_and_causal_contract"] = {
        "same_physical_C_rate_hour_vs_second_Lq_ratio": (
            lag_hour_basis / lag_second_basis
        ),
        "activation_entropy_offset_physical_minus_legacy_at_fixed_enthalpy_J_per_mol_K": (
            -model.R * math.log(3600.0)
        ),
        "single_temperature_apparent_activation_enthalpy_offset_if_entropy_fixed_J_per_mol": (
            model.R * temperature * math.log(3600.0)
        ),
        "duplicate_first_step_pad_points": int(duplicate_pad_points),
        "five_L_residual_fraction": math.exp(-float(model._LAG_PAD_NLV)),
    }

    # 5. Accepted stored-8dp 14-peak fit: direct formula versus release kernel.
    summary = json.loads(FIT_SUMMARY.read_text(encoding="utf-8"))
    stored_fit = summary["C_skew"]["blend"]
    stored_transitions, stored_background = transitions_from_stored_8dp(
        stored_fit["params"], int(stored_fit["N"])
    )
    rounded_payload = json.loads(FIT_ROUNDED.read_text(encoding="utf-8"))
    rounded_transitions, rounded_background = transitions_from_rounded(rounded_payload)

    voltage, observed = load_blend_dqdv()
    stored_host = model.GraphiteAnodeDischargeDQDV(
        stored_transitions, Cbg=stored_background
    )
    stored_prediction = np.asarray(
        stored_host.equilibrium(voltage, temperature), dtype=float
    )
    rounded_host = model.GraphiteAnodeDischargeDQDV(
        rounded_transitions, Cbg=rounded_background
    )
    rounded_prediction = np.asarray(
        rounded_host.equilibrium(voltage, temperature), dtype=float
    )

    # Independent direct formula matching build_two_versions.model_skewlogistic.
    direct_prediction = np.full(voltage.size, stored_background, dtype=float)
    for transition in stored_transitions:
        z = np.clip(
            (voltage - transition["U"]) / transition["w"], -350.0, 350.0
        )
        sigma = 1.0 / (1.0 + np.exp(-z))
        direct_prediction += (
            transition["Q"]
            * transition["alpha"]
            / transition["w"]
            * sigma ** transition["alpha"]
            * (1.0 - sigma)
        )

    profile_grids = {"graphite": 2.5e-4, "silicon": 1.0e-3, "blend": 5.0e-4}
    profile_diagnostics = {}
    for material, grid_step in profile_grids.items():
        profile = summary["C_skew"][material]
        component_count = int(profile["N"])
        parameters = np.asarray(profile["params"], dtype=float)
        widths = parameters[component_count : 2 * component_count]
        alphas = parameters[3 * component_count : 4 * component_count]
        profile_diagnostics[material] = {
            "grid_step_V": grid_step,
            "min_width_V": float(np.min(widths)),
            "max_width_V": float(np.max(widths)),
            "min_width_below_grid_step": bool(np.min(widths) < grid_step),
            "min_alpha": float(np.min(alphas)),
            "max_alpha": float(np.max(alphas)),
            "stored_8dp_alpha_equals_lower_bound": bool(
                np.any(alphas == 0.15)
            ),
            "stored_8dp_alpha_equals_upper_bound": bool(
                np.any(alphas == 8.0)
            ),
            "stored_8dp_width_equals_upper_bound": bool(
                np.any(widths == 0.12)
            ),
        }

    result["accepted_empirical_fit"] = {
        "points": int(voltage.size),
        "parameter_count": int(stored_fit["npar"]),
        "curve_and_background_units": "mAh/V",
        "bic_interpretation": (
            "i.i.d.-Gaussian working-likelihood statistic on smoothed, "
            "correlated residuals; compare only within this preprocessing "
            "and objective"
        ),
        "optimizer_full_precision_available": False,
        "optimizer_prediction_available": False,
        "optimizer_termination_metadata_available": False,
        "optimizer_active_set_status_available": False,
        "builder_required_optimizer_success": False,
        "stored_8dp_background": stored_background,
        "presentation_6dp_background": rounded_background,
        "stored_8dp_metrics_recomputed": metrics(
            observed, stored_prediction, int(stored_fit["npar"])
        ),
        "presentation_6dp_metrics_recomputed": metrics(
            observed, rounded_prediction, int(stored_fit["npar"])
        ),
        "stored_8dp_release_kernel_vs_direct_max_abs": float(
            np.max(np.abs(stored_prediction - direct_prediction))
        ),
        "stored_8dp_vs_presentation_6dp_max_abs": float(
            np.max(np.abs(stored_prediction - rounded_prediction))
        ),
        "builder_from_best_rounded_R2": float(stored_fit["R2"]),
        "builder_from_best_rounded_BIC": float(stored_fit["BIC"]),
        "stored_8dp_profile_diagnostics": profile_diagnostics,
        "sha256_le_f64": {
            "voltage": little_endian_f64_sha256(voltage),
            "observed": little_endian_f64_sha256(observed),
            "stored_8dp_parameters": little_endian_f64_sha256(
                np.asarray(stored_fit["params"], dtype=float)
            ),
            "stored_8dp_prediction": little_endian_f64_sha256(stored_prediction),
            "stored_8dp_residual": little_endian_f64_sha256(
                observed - stored_prediction
            ),
        },
    }

    # 6. Serialized-order equality of current defaults and accepted blend fit.
    #
    # Do not report a component-aligned distance.  The accepted generic fit has
    # no host labels or canonical component ordering, while the physical blend
    # starts from host-specific standalone profiles and rescales Si capacity.
    # Subtracting the two arrays position-by-position is therefore not a
    # permutation- or model-invariant comparison.
    stored_tuples = np.asarray(
        [
            [tr["U"], tr["w"], tr["Q"], tr["alpha"]]
            for tr in stored_transitions
        ],
        dtype=float,
    )
    default_tuples = np.asarray(
        [
            [
                float(tr["U"]),
                float(tr["w"]),
                float(tr["Q"]),
                float(tr.get("alpha", 1.0)),
            ]
            for tr in (
                list(model.DEFAULT_GRAPHITE_TRANSITIONS)
                + list(model.DEFAULT_SI_TRANSITIONS or [])
            )
        ],
        dtype=float,
    )
    result["default_vs_accepted_blend_preset"] = {
        "same_parameter_array_dimensions": (
            stored_tuples.shape == default_tuples.shape
        ),
        "serialized_order_array_equal": bool(
            stored_tuples.shape == default_tuples.shape
            and np.array_equal(stored_tuples, default_tuples)
        ),
        "distance_not_reported": (
            "The generic blend-fit components and host-specific default "
            "components lack a common label/order/scaling contract."
        ),
    }

    # 7. Fit only f_Si and Cbg on the shipped default 7+7 construction.
    #
    # This is not a fair mechanism-selection contest: the default profiles were
    # fitted to standalone host data, whereas the accepted 14-component profile
    # was fitted directly to the blend data.  It is nevertheless a direct test
    # of the narrower documentation claim that the accepted blend fit is wired
    # as the shipped default.
    def default_blend_residual(parameters: np.ndarray) -> np.ndarray:
        silicon_fraction, background = parameters
        default_blend = model.BlendedAnodeDQDV(
            float(silicon_fraction), si_case="sic", Cbg=float(background)
        )
        prediction = np.asarray(
            default_blend.equilibrium(voltage, temperature), dtype=float
        )
        return prediction - observed

    with warnings.catch_warnings():
        # The eager-logistic warning is measured separately above.  Suppress it
        # here so this fit-wiring diagnostic has clean deterministic stdout.
        warnings.simplefilter("ignore", RuntimeWarning)
        default_fit = least_squares(
            default_blend_residual,
            x0=np.asarray([0.5, 0.0], dtype=float),
            bounds=(
                np.asarray([0.0, 0.0], dtype=float),
                np.asarray([0.99, float(np.max(observed))], dtype=float),
            ),
            method="trf",
            max_nfev=10_000,
            xtol=1.0e-14,
            ftol=1.0e-14,
            gtol=1.0e-14,
        )
    default_fit_prediction = observed + default_fit.fun
    background_zero_sweep = {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        for silicon_fraction in (0.1, 0.3, 0.5, 0.75):
            prediction = np.asarray(
                model.BlendedAnodeDQDV(
                    silicon_fraction, si_case="sic", Cbg=0.0
                ).equilibrium(voltage, temperature),
                dtype=float,
            )
            background_zero_sweep[str(silicon_fraction)] = metrics(
                observed, prediction, 1
            )["R2"]

    result["shipped_default_7plus7_on_blend_data"] = {
        "optimization": (
            "unweighted least_squares over f_Si and Cbg only; "
            "bounds f_Si=[0,0.99], Cbg=[0,max(observed)]"
        ),
        "optimized_f_Si": float(default_fit.x[0]),
        "optimized_Cbg": float(default_fit.x[1]),
        "optimized_metrics_two_parameters": metrics(
            observed, default_fit_prediction, 2
        ),
        "Cbg_zero_R2_sweep": background_zero_sweep,
        "comparison_scope": (
            "Tests default wiring, not host-model superiority: standalone "
            "host profiles and the direct blend fit had different objectives."
        ),
    }
    return result


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
