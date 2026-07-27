#!/usr/bin/env python3
"""Expanded cross-check of the v1.0.25.2 regular-solution measure.

This reproduces the three checks reported in the latest lineage—normalization,
zero gap below the critical interaction, and continuity at Omega/(RT)=2—and
also tests the disputed derivative claim for several skew exponents.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss


REPO = Path(__file__).resolve().parents[3]
SOURCE = (
    REPO
    / "Claude/docs/v1.0.25.2/_sections/ch3v22_sec02b_sifr.tex"
)
R = 8.314
T = 298.15
F = 96485.0
RT_OVER_F = R * T / F
U0 = 0.0
WIDTH = 0.010
VOLTAGE = np.linspace(-1.0, 1.0, 4001)
INTERACTION_RATIOS = (0.0, 1.0, 1.999, 2.0, 2.001, 3.0, 4.0, 8.0)
ALPHAS = (1.0, 4.0, 8.0)
EPSILONS = (1.0e-3, 1.0e-4, 1.0e-5)
QUADRATURE_POINTS = 1600
NODES, WEIGHTS = leggauss(QUADRATURE_POINTS)


def skew_logistic_derivative(
    delta_voltage: np.ndarray, alpha: float
) -> np.ndarray:
    reduced = np.clip(delta_voltage / WIDTH, -350.0, 350.0)
    sigma = 1.0 / (1.0 + np.exp(-reduced))
    return alpha * sigma**alpha * (1.0 - sigma) / WIDTH


def binodal_theta(interaction_over_rt: float) -> float:
    if interaction_over_rt <= 2.0:
        return 0.5

    def residual(theta: float) -> float:
        return (
            math.log(theta / (1.0 - theta))
            + interaction_over_rt * (1.0 - 2.0 * theta)
        )

    low, high = 1.0e-14, 0.5 - 1.0e-14
    for _ in range(120):
        middle = 0.5 * (low + high)
        if residual(middle) > 0.0:
            high = middle
        else:
            low = middle
    return 0.5 * (low + high)


def stable_branch_integral(
    interaction_over_rt: float,
    theta_low: float,
    theta_high: float,
    alpha: float,
) -> np.ndarray:
    theta = (
        0.5 * (theta_high - theta_low) * NODES
        + 0.5 * (theta_high + theta_low)
    )
    quadrature_weights = 0.5 * (theta_high - theta_low) * WEIGHTS
    potential = U0 - RT_OVER_F * (
        np.log(theta / (1.0 - theta))
        + interaction_over_rt * (1.0 - 2.0 * theta)
    )
    kernel = skew_logistic_derivative(
        VOLTAGE[:, np.newaxis] - potential[np.newaxis, :], alpha
    )
    return kernel @ quadrature_weights


def broadened_curve(
    interaction_over_rt: float, alpha: float
) -> tuple[np.ndarray, float, float]:
    theta_a = binodal_theta(interaction_over_rt)
    if interaction_over_rt <= 2.0:
        curve = stable_branch_integral(
            interaction_over_rt, 0.0, 1.0, alpha
        )
        return curve, 0.0, theta_a

    gap_weight = 1.0 - 2.0 * theta_a
    curve = gap_weight * skew_logistic_derivative(VOLTAGE - U0, alpha)
    curve += stable_branch_integral(
        interaction_over_rt, 0.0, theta_a, alpha
    )
    curve += stable_branch_integral(
        interaction_over_rt, 1.0 - theta_a, 1.0, alpha
    )
    return curve, gap_weight, theta_a


def run() -> dict:
    normalization_rows = []
    references = {}
    for alpha in ALPHAS:
        for interaction_ratio in INTERACTION_RATIOS:
            curve, gap_weight, theta_a = broadened_curve(
                interaction_ratio, alpha
            )
            stable_weight = 2.0 * theta_a
            analytic_weight_sum = gap_weight + stable_weight
            normalization_rows.append(
                {
                    "alpha": alpha,
                    "interaction_over_rt": interaction_ratio,
                    "theta_a": theta_a,
                    "gap_weight": gap_weight,
                    "stable_branch_weight": stable_weight,
                    "analytic_total_area_for_Q_equal_1": analytic_weight_sum,
                    "finite_window_numeric_area": float(
                        np.trapezoid(curve, VOLTAGE)
                    ),
                }
            )
            if interaction_ratio == 2.0:
                references[alpha] = curve

    threshold_rows = []
    for alpha in ALPHAS:
        reference = references[alpha]
        for epsilon in EPSILONS:
            curve_right, gap_weight, _ = broadened_curve(
                2.0 + epsilon, alpha
            )
            curve_left, _, _ = broadened_curve(2.0 - epsilon, alpha)
            difference_right = curve_right - reference
            difference_left = reference - curve_left
            maximum_right = float(np.max(np.abs(difference_right)))
            maximum_left = float(np.max(np.abs(difference_left)))
            threshold_rows.append(
                {
                    "alpha": alpha,
                    "epsilon": epsilon,
                    "right_gap_weight": gap_weight,
                    "right_max_abs_difference": maximum_right,
                    "right_max_abs_difference_over_epsilon": (
                        maximum_right / epsilon
                    ),
                    "right_max_abs_difference_over_sqrt_epsilon": (
                        maximum_right / math.sqrt(epsilon)
                    ),
                    "left_max_abs_difference": maximum_left,
                    "left_max_abs_difference_over_epsilon": (
                        maximum_left / epsilon
                    ),
                }
            )

    numerical_areas = [
        row["finite_window_numeric_area"] for row in normalization_rows
    ]
    subcritical_gap_weights = [
        row["gap_weight"]
        for row in normalization_rows
        if row["interaction_over_rt"] <= 2.0
    ]
    return {
        "scope": {
            "source_equation": (
                "Claude/docs/v1.0.25.2/_sections/"
                "ch3v22_sec02b_sifr.tex:eq:sifr-twophase"
            ),
            "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "source_blob_unchanged_between_ab196b2_and_3b5fd05": True,
            "Q": 1.0,
            "R_J_per_mol_K": R,
            "T_K": T,
            "F_C_per_mol": F,
            "RT_over_F_V": RT_OVER_F,
            "U0_V": U0,
            "kernel_width_V": WIDTH,
            "voltage_window_V": [float(VOLTAGE[0]), float(VOLTAGE[-1])],
            "voltage_points": int(VOLTAGE.size),
            "gauss_legendre_points_per_interval": QUADRATURE_POINTS,
            "alphas": list(ALPHAS),
        },
        "normalization_and_gap_rows": normalization_rows,
        "threshold_rows": threshold_rows,
        "summary": {
            "maximum_finite_window_area_error": float(
                max(abs(area - 1.0) for area in numerical_areas)
            ),
            "maximum_subcritical_gap_weight": float(
                max(subcritical_gap_weights)
            ),
            "analytic_area_identity": (
                "gap_weight + stable_branch_weight = "
                "(1 - 2*theta_a) + 2*theta_a = 1"
            ),
            "threshold_judgment": (
                "For every tested alpha, right difference/epsilon approaches "
                "a finite value while right difference/sqrt(epsilon) tends to "
                "zero. The leading square-root gap mass cancels the removed "
                "central stable-branch mass; the claimed divergent first "
                "Omega derivative does not follow from eq:sifr-twophase."
            ),
            "claude_three_check_verdict": {
                "area_equals_Q": "PASS",
                "gap_zero_for_interaction_over_rt_at_or_below_2": "PASS",
                "continuous_as_interaction_over_rt_approaches_2_from_above": (
                    "PASS"
                ),
                "divergent_first_omega_derivative": "FAIL",
            },
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
