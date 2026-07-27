"""Causal monotonic-curve and time-trajectory conformance gates."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import math
import unittest

import numpy as np

from _reference import import_model


class CausalRelaxationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = import_model()
        cls.initial = cls.model.CausalInitialState(
            value=0.0,
            provenance=cls.model.InitialConditionProvenance.SUPPLIED_STATE,
            description="synthetic known initial state",
        )

    def test_monotonic_curve_constant_target_matches_exact_response(self) -> None:
        voltage = np.asarray([0.0, 1.0, 2.0])
        target = np.ones(3)
        result = self.model.relax_monotonic_curve(
            voltage, target, lag_length_v=1.0, initial=self.initial
        )
        np.testing.assert_allclose(
            result,
            [0.0, 1.0 - math.exp(-1.0), 1.0 - math.exp(-2.0)],
            rtol=2.0e-15,
            atol=2.0e-15,
        )

    def test_decreasing_curve_preserves_supplied_order(self) -> None:
        voltage = np.asarray([2.0, 1.0, 0.0])
        target = np.ones(3)
        result = self.model.relax_monotonic_curve(
            voltage, target, lag_length_v=1.0, initial=self.initial
        )
        np.testing.assert_allclose(
            result,
            [0.0, 1.0 - math.exp(-1.0), 1.0 - math.exp(-2.0)],
            rtol=2.0e-15,
            atol=2.0e-15,
        )

    def test_curve_reversal_duplicate_and_invalid_lag_fail_fast(self) -> None:
        target = np.asarray([0.0, 0.5, 1.0])
        for voltage in (
            np.asarray([0.0, 1.0, 0.5]),
            np.asarray([0.0, 1.0, 1.0]),
        ):
            with self.subTest(voltage=voltage):
                with self.assertRaisesRegex(ValueError, "strictly monotonic"):
                    self.model.relax_monotonic_curve(
                        voltage, target, 0.1, self.initial
                    )
        with self.assertRaises(ValueError):
            self.model.relax_monotonic_curve(
                np.asarray([0.0, 1.0, 2.0]), target, np.inf, self.initial
            )
        with self.assertRaises(ValueError):
            self.model.relax_monotonic_curve(
                np.asarray([0.0, 1.0, 2.0]), target, 0.0, self.initial
            )

    def test_time_trajectory_accepts_target_reversal_without_sorting(self) -> None:
        time = np.asarray([0.0, 0.2, 0.7, 1.5, 2.0])
        target = np.asarray([0.0, 1.0, 0.2, 0.8, 0.1])
        result = self.model.relax_time_trajectory(
            time,
            target,
            relaxation_time_s=0.3,
            initial=self.initial,
        )
        self.assertEqual(result.shape, target.shape)
        self.assertEqual(result[0], self.initial.value)
        self.assertTrue(np.all((result >= 0.0) & (result <= 1.0)))
        # The result follows the acquisition-order recurrence and cannot equal
        # a result obtained by sorting the nonmonotonic target values.
        sorted_result = self.model.relax_time_trajectory(
            time,
            np.sort(target),
            relaxation_time_s=0.3,
            initial=self.initial,
        )
        self.assertFalse(np.array_equal(result, sorted_result))

    def test_trajectory_requires_strict_acquisition_time_order(self) -> None:
        target = np.asarray([0.0, 0.5, 1.0])
        for time in (
            np.asarray([0.0, 1.0, 0.5]),
            np.asarray([0.0, 1.0, 1.0]),
        ):
            with self.subTest(time=time):
                with self.assertRaisesRegex(ValueError, "strictly increasing"):
                    self.model.relax_time_trajectory(
                        time, target, 0.1, self.initial
                    )

    def test_state_domain_shape_and_initial_contract_fail_fast(self) -> None:
        with self.assertRaises(ValueError):
            self.model.CausalInitialState(
                value=1.1,
                provenance="supplied-state",
                description="outside state domain",
            )
        with self.assertRaises(ValueError):
            self.model.CausalInitialState(
                value=0.0,
                provenance="supplied-state",
                description="",
            )
        with self.assertRaises(ValueError):
            self.model.relax_time_trajectory(
                np.asarray([0.0, 1.0]),
                np.asarray([0.0, np.nan]),
                1.0,
                self.initial,
            )
        with self.assertRaises(ValueError):
            self.model.relax_time_trajectory(
                np.asarray([0.0, 1.0, 2.0]),
                np.asarray([0.0, 1.0]),
                1.0,
                self.initial,
            )
        with self.assertRaises(TypeError):
            self.model.relax_time_trajectory(
                np.asarray([0.0, 1.0]),
                np.asarray([0.0, 1.0]),
                1.0,
                None,
            )

    def test_initial_state_is_immutable(self) -> None:
        with self.assertRaises((FrozenInstanceError, AttributeError, TypeError)):
            self.initial.value = 0.5


if __name__ == "__main__":
    unittest.main()
