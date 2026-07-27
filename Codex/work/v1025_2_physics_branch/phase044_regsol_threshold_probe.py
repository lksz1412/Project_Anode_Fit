#!/usr/bin/env python3
"""Probe the broadened regular-solution curve at Omega/(RT) -> 2+.

This implements the measure written in v1.0.25.2 equation
``eq:sifr-twophase``.  It tests the manuscript claim that the broadened curve
has a divergent derivative with respect to Omega solely because the Maxwell
gap mass opens as a square root.
"""

from __future__ import annotations

import json
import math

import numpy as np
from numpy.polynomial.legendre import leggauss


R = 8.314
T = 298.15
F = 96485.0
RT_OVER_F = R * T / F
U0 = 0.0
WIDTH = 0.010
VOLTAGE = np.linspace(-0.12, 0.12, 1201)
EPSILONS = (1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5, 3e-6)
QUADRATURE_POINTS = 1600
NODES, WEIGHTS = leggauss(QUADRATURE_POINTS)


def logistic_derivative(delta_voltage: np.ndarray) -> np.ndarray:
    reduced = np.clip(delta_voltage / WIDTH, -350.0, 350.0)
    sigma = 1.0 / (1.0 + np.exp(-reduced))
    return sigma * (1.0 - sigma) / WIDTH


def binodal_theta(interaction_over_rt: float) -> float:
    if interaction_over_rt <= 2.0:
        return 0.5

    def residual(theta: float) -> float:
        return (
            math.log(theta / (1.0 - theta))
            + interaction_over_rt * (1.0 - 2.0 * theta)
        )

    low, high = 1.0e-14, 0.5 - 1.0e-14
    for _ in range(100):
        middle = 0.5 * (low + high)
        if residual(middle) > 0.0:
            high = middle
        else:
            low = middle
    return 0.5 * (low + high)


def stable_branch_integral(
    interaction_over_rt: float, theta_low: float, theta_high: float
) -> np.ndarray:
    theta = (
        0.5 * (theta_high - theta_low) * NODES
        + 0.5 * (theta_high + theta_low)
    )
    weights = 0.5 * (theta_high - theta_low) * WEIGHTS
    potential = U0 - RT_OVER_F * (
        np.log(theta / (1.0 - theta))
        + interaction_over_rt * (1.0 - 2.0 * theta)
    )
    kernel = logistic_derivative(
        VOLTAGE[:, np.newaxis] - potential[np.newaxis, :]
    )
    return kernel @ weights


def broadened_curve(interaction_over_rt: float) -> tuple[np.ndarray, float]:
    theta_a = binodal_theta(interaction_over_rt)
    if interaction_over_rt <= 2.0:
        return stable_branch_integral(interaction_over_rt, 0.0, 1.0), 0.0

    gap_weight = 1.0 - 2.0 * theta_a
    curve = gap_weight * logistic_derivative(VOLTAGE - U0)
    curve += stable_branch_integral(interaction_over_rt, 0.0, theta_a)
    curve += stable_branch_integral(
        interaction_over_rt, 1.0 - theta_a, 1.0
    )
    return curve, gap_weight


def run() -> dict:
    reference, _ = broadened_curve(2.0)
    rows = []
    for epsilon in EPSILONS:
        curve, gap_weight = broadened_curve(2.0 + epsilon)
        difference = curve - reference
        maximum = float(np.max(np.abs(difference)))
        rows.append(
            {
                "epsilon": epsilon,
                "gap_weight": gap_weight,
                "max_abs_difference": maximum,
                "max_abs_difference_over_epsilon": maximum / epsilon,
                "max_abs_difference_over_sqrt_epsilon": (
                    maximum / math.sqrt(epsilon)
                ),
                "rms_difference_over_epsilon": (
                    float(np.sqrt(np.mean(difference * difference))) / epsilon
                ),
            }
        )

    return {
        "source_equation": (
            "Claude/docs/v1.0.25.2/_sections/"
            "ch3v22_sec02b_sifr.tex:200-220"
        ),
        "constants": {
            "R_J_per_mol_K": R,
            "T_K": T,
            "F_C_per_mol": F,
            "RT_over_F_V": RT_OVER_F,
            "U0_V": U0,
            "logistic_width_V": WIDTH,
            "voltage_min_V": float(VOLTAGE[0]),
            "voltage_max_V": float(VOLTAGE[-1]),
            "voltage_points": int(VOLTAGE.size),
            "gauss_legendre_points_per_interval": QUADRATURE_POINTS,
            "curve_units_for_Q_equal_1": "1/V",
        },
        "reference_at_interaction_over_rt_2": {
            "finite_window_area": float(np.trapezoid(reference, VOLTAGE)),
            "maximum": float(np.max(reference)),
        },
        "rows": rows,
        "judgment": (
            "max_abs_difference/epsilon converges to a finite value while "
            "max_abs_difference/sqrt(epsilon) tends to zero; the leading "
            "sqrt gap-mass term cancels the removed central-branch mass."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
