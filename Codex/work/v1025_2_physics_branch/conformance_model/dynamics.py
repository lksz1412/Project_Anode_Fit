"""Causal relaxation APIs for monotonic curves and time-ordered trajectories."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from .numerics import as_finite_float, as_positive_float, finite_array


class InitialConditionProvenance(str, Enum):
    """Allowed explicit origins of a causal initial state."""

    SUPPLIED_STATE = "supplied-state"
    MEASURED_PREHISTORY = "measured-prehistory"
    ASYMPTOTIC_PREHISTORY = "asymptotic-prehistory"


@dataclass(frozen=True, slots=True)
class CausalInitialState:
    """Explicit causal boundary state; no duplicated-point padding fallback.

    Physics IDs: PHY-003, PHY-017, PHY-032.
    """

    value: float
    provenance: InitialConditionProvenance
    description: str

    def __post_init__(self) -> None:
        value = as_finite_float("initial state", self.value)
        if not 0.0 <= value <= 1.0:
            raise ValueError("initial state must be within [0, 1]")
        object.__setattr__(self, "value", value)
        object.__setattr__(
            self, "provenance", InitialConditionProvenance(self.provenance)
        )
        if not self.description.strip():
            raise ValueError("initial-state description must be nonempty")


def _validate_state_series(name: str, values: np.ndarray) -> np.ndarray:
    state = finite_array(name, values)
    if state.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if state.size < 2:
        raise ValueError(f"{name} must contain at least two points")
    if np.any((state < 0.0) | (state > 1.0)):
        raise ValueError(f"{name} must remain within [0, 1]")
    return state


def _relax_piecewise_linear(
    coordinate: np.ndarray,
    target_state: np.ndarray,
    relaxation_scale: float,
    initial: CausalInitialState,
) -> np.ndarray:
    """Exact first-order response to a linearly interpolated target."""

    if not isinstance(initial, CausalInitialState):
        raise TypeError("initial must be an explicit CausalInitialState")
    result = np.empty_like(target_state)
    result[0] = initial.value
    for index in range(1, target_state.size):
        step = float(coordinate[index] - coordinate[index - 1])
        ratio = step / relaxation_scale
        decay = float(np.exp(-ratio))
        one_minus_decay = float(-np.expm1(-ratio))
        if ratio < 1.0e-4:
            phi = ratio * ratio * (
                0.5
                - ratio / 6.0
                + ratio * ratio / 24.0
                - ratio * ratio * ratio / 120.0
            )
        else:
            phi = ratio + float(np.expm1(-ratio))
        target_slope = (
            target_state[index] - target_state[index - 1]
        ) / step
        result[index] = (
            result[index - 1] * decay
            + target_state[index - 1] * one_minus_decay
            + target_slope * relaxation_scale * phi
        )
    tolerance = 256.0 * np.finfo(np.float64).eps
    if np.any(result < -tolerance) or np.any(result > 1.0 + tolerance):
        raise RuntimeError("causal relaxation left the admissible state interval")
    return np.clip(result, 0.0, 1.0)


def relax_monotonic_curve(
    voltage_v: np.ndarray,
    target_state: np.ndarray,
    lag_length_v: float,
    initial: CausalInitialState,
) -> np.ndarray:
    """Relax a strictly monotonic single-branch curve in voltage distance.

    Input order is preserved.  Duplicate points, reversals, nonfinite lag, and
    a missing initial/prehistory contract fail explicitly.  Reversal or rest
    data belongs to :func:`relax_time_trajectory`.

    Physics IDs: PHY-003, PHY-009, PHY-017, C-005, PHY-032.
    """

    voltage = finite_array("voltage_v", voltage_v)
    target = _validate_state_series("target_state", target_state)
    if voltage.ndim != 1 or voltage.shape != target.shape:
        raise ValueError("voltage_v and target_state must be equal-length 1-D arrays")
    increments = np.diff(voltage)
    if not (np.all(increments > 0.0) or np.all(increments < 0.0)):
        raise ValueError(
            "voltage_v must be strictly monotonic; trajectory data must keep time order"
        )
    lag = as_positive_float("lag_length_v", lag_length_v)
    distance = np.concatenate(
        (np.asarray([0.0]), np.cumsum(np.abs(increments), dtype=np.float64))
    )
    return _relax_piecewise_linear(distance, target, lag, initial)


def relax_time_trajectory(
    time_s: np.ndarray,
    target_state: np.ndarray,
    relaxation_time_s: float,
    initial: CausalInitialState,
) -> np.ndarray:
    """Relax a target in acquisition-time order without voltage sorting.

    The target may reverse or remain constant.  Time must be strictly
    increasing, and the supplied order is never rearranged.

    Physics IDs: PHY-001, PHY-003, PHY-014, PHY-017, PHY-025, PHY-032.
    """

    time = finite_array("time_s", time_s)
    target = _validate_state_series("target_state", target_state)
    if time.ndim != 1 or time.shape != target.shape:
        raise ValueError("time_s and target_state must be equal-length 1-D arrays")
    increments = np.diff(time)
    if not np.all(increments > 0.0):
        raise ValueError("time_s must be strictly increasing in acquisition order")
    relaxation_time = as_positive_float(
        "relaxation_time_s", relaxation_time_s
    )
    return _relax_piecewise_linear(time - time[0], target, relaxation_time, initial)
