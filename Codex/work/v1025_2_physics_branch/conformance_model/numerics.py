"""Small numerical primitives with fail-fast domain checks."""

from __future__ import annotations

from typing import TypeAlias

import numpy as np


FloatArray: TypeAlias = np.ndarray
ScalarOrArray: TypeAlias = float | np.ndarray


def safe_logistic(x: ScalarOrArray) -> ScalarOrArray:
    """Return ``1 / (1 + exp(-x))`` without eager-branch overflow.

    Finite values and signed infinities are supported.  NaN is rejected rather
    than silently entering a physical or empirical state.

    Physics IDs: PHY-006, PHY-007, C-001, PHY-032.
    """

    values = np.asarray(x, dtype=np.float64)
    if np.any(np.isnan(values)):
        raise ValueError("safe_logistic input must not contain NaN")

    flat = values.reshape(-1)
    result = np.empty_like(flat)
    positive = flat >= 0.0
    result[positive] = 1.0 / (1.0 + np.exp(-flat[positive]))
    exp_value = np.exp(flat[~positive])
    result[~positive] = exp_value / (1.0 + exp_value)
    reshaped = result.reshape(values.shape)
    if values.ndim == 0:
        return float(reshaped)
    return reshaped


def as_finite_float(name: str, value: float) -> float:
    """Validate and return a scalar finite float."""

    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def as_positive_float(name: str, value: float) -> float:
    """Validate and return a scalar finite value strictly greater than zero."""

    result = as_finite_float(name, value)
    if result <= 0.0:
        raise ValueError(f"{name} must be > 0")
    return result


def finite_array(name: str, values: ScalarOrArray) -> np.ndarray:
    """Return a float64 array and reject every nonfinite value."""

    result = np.asarray(values, dtype=np.float64)
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values")
    return result


def scalarize_like(source: ScalarOrArray, values: np.ndarray) -> ScalarOrArray:
    """Return a Python float when ``source`` was scalar, otherwise an array."""

    if np.asarray(source).ndim == 0:
        return float(np.asarray(values))
    return values
