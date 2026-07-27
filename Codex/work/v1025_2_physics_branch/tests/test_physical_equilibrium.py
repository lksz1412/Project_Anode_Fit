"""Physical-host charge-balance and orientation conformance gates."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import unittest

import numpy as np

from _reference import import_model


class PhysicalHostTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = import_model()
        cls.temperature_k = 298.15

    def _transition(self, **overrides):
        arguments = {
            "center_v_ref": 0.1,
            "signed_capacity_mAh": 2.0,
            "orientation": 1,
            "electron_stoichiometry": 1.0,
            "label": "synthetic",
            "evidence_grade": "independently derived",
        }
        arguments.update(overrides)
        return self.model.IdealTransition(**arguments)

    def _host(self, transition=None, **overrides):
        arguments = {
            "name": "synthetic-host",
            "transitions": (transition or self._transition(),),
        }
        arguments.update(overrides)
        return self.model.PhysicalHost(**arguments)

    def test_ideal_transition_uses_fixed_orientation_and_independent_z(self) -> None:
        transition = self._transition(electron_stoichiometry=2.0)
        self.assertAlmostEqual(
            transition.equilibrium_state(transition.center_v_ref, self.temperature_k),
            0.5,
            places=15,
        )
        offset = 0.01
        increasing = transition.equilibrium_state(
            np.asarray(
                [transition.center_v_ref - offset, transition.center_v_ref + offset]
            ),
            self.temperature_k,
        )
        self.assertLess(increasing[0], increasing[1])

        decreasing = self._transition(orientation=-1)
        states = decreasing.equilibrium_state(
            np.asarray(
                [decreasing.center_v_ref - offset, decreasing.center_v_ref + offset]
            ),
            self.temperature_k,
        )
        self.assertGreater(states[0], states[1])

    def test_charge_balance_and_analytic_derivative_match_finite_difference(
        self,
    ) -> None:
        background = self.model.LinearChemicalBackground(
            reference_potential_v=0.1,
            reference_capacity_mAh=0.25,
            chemical_capacitance_mAh_per_v=0.4,
        )
        host = self._host(chemical_background=background)
        voltage = np.linspace(0.06, 0.14, 17)
        step = 1.0e-7
        finite_difference = (
            host.chemical_capacity(voltage + step, self.temperature_k)
            - host.chemical_capacity(voltage - step, self.temperature_k)
        ) / (2.0 * step)
        analytic = host.dchemical_capacity_dv(voltage, self.temperature_k)
        np.testing.assert_allclose(
            analytic,
            finite_difference,
            rtol=2.0e-9,
            atol=2.0e-8,
        )

    def test_scalar_potential_with_temperature_series_preserves_array_shape(
        self,
    ) -> None:
        host = self._host()
        temperatures = np.asarray([280.0, 298.15, 330.0])
        states = host.equilibrium_states(0.1, temperatures)[0]
        capacity = host.chemical_capacity(0.1, temperatures)
        derivative = host.dchemical_capacity_dv(0.1, temperatures)
        for values in (states, capacity, derivative):
            self.assertIsInstance(values, np.ndarray)
            self.assertEqual(values.shape, temperatures.shape)
            self.assertTrue(np.all(np.isfinite(values)))

    def test_implicit_charge_balance_inverts_increasing_and_decreasing_hosts(
        self,
    ) -> None:
        increasing = self._host()
        voltage = increasing.solve_internal_potential(
            1.0, self.temperature_k, (-0.2, 0.4)
        )
        self.assertAlmostEqual(voltage, 0.1, places=10)
        self.assertAlmostEqual(
            increasing.chemical_capacity(voltage, self.temperature_k),
            1.0,
            places=10,
        )

        decreasing = self._host(
            self._transition(orientation=-1),
            name="decreasing-host",
        )
        voltage = decreasing.solve_internal_potential(
            1.0, self.temperature_k, (-0.2, 0.4)
        )
        self.assertAlmostEqual(voltage, 0.1, places=10)
        self.assertAlmostEqual(
            decreasing.chemical_capacity(voltage, self.temperature_k),
            1.0,
            places=10,
        )

    def test_nonmonotonic_charge_balance_is_rejected_as_inadmissible(self) -> None:
        host = self.model.PhysicalHost(
            name="nonmonotonic",
            transitions=(
                self._transition(
                    center_v_ref=-0.08,
                    signed_capacity_mAh=1.0,
                    orientation=1,
                ),
                self._transition(
                    center_v_ref=0.08,
                    signed_capacity_mAh=1.0,
                    orientation=-1,
                ),
            ),
        )
        with self.assertRaisesRegex(ValueError, "monotonic certificate"):
            host.solve_internal_potential(
                target_capacity_mAh=0.5,
                temperature_k=self.temperature_k,
                bracket_v=(-0.3, 0.3),
            )

    def test_unbracketed_target_and_invalid_domains_fail_fast(self) -> None:
        host = self._host()
        with self.assertRaisesRegex(ValueError, "not bracketed"):
            host.solve_internal_potential(
                3.0, self.temperature_k, (-0.2, 0.4)
            )
        with self.assertRaises(ValueError):
            host.chemical_capacity(0.1, 0.0)
        with self.assertRaises(ValueError):
            self._transition(orientation=0)
        with self.assertRaises(ValueError):
            self._transition(electron_stoichiometry=0.0)
        with self.assertRaises(TypeError):
            self._transition().equilibrium_state(
                0.1, self.temperature_k, constants=object()
            )
        with self.assertRaises(ValueError):
            self.model.LinearChemicalBackground(
                chemical_capacitance_mAh_per_v=-0.1
            )
        with self.assertRaises(ValueError):
            self.model.PhysicalHost(name="", transitions=(self._transition(),))

    def test_signed_storage_and_observation_magnitude_are_separate(self) -> None:
        host = self._host(
            self._transition(signed_capacity_mAh=-2.0, orientation=1)
        )
        signed_derivative = np.asarray(
            host.dchemical_capacity_dv(
                np.asarray([0.08, 0.10, 0.12]), self.temperature_k
            )
        )
        self.assertTrue(np.all(signed_derivative < 0.0))

        magnitude = self.model.ObservationContract.magnitude(
            "synthetic magnitude preprocessing"
        )
        fit_values = magnitude.to_fit(signed_derivative)
        self.assertTrue(np.all(fit_values > 0.0))
        with self.assertRaises(self.model.IrrecoverableObservationSignError):
            magnitude.recover_signed(fit_values)

    def test_physical_blend_is_shared_potential_capacity_sum(self) -> None:
        host_one = self._host(name="graphite")
        host_two = self._host(
            self._transition(
                center_v_ref=0.2,
                signed_capacity_mAh=3.0,
                orientation=1,
            ),
            name="silicon",
        )
        blend = self.model.PhysicalHostBlend(
            hosts=(host_one, host_two),
            normalization_basis="synthetic fixed-total-capacity basis",
        )
        voltage = np.linspace(-0.1, 0.3, 31)
        expected = host_one.chemical_capacity(
            voltage, self.temperature_k
        ) + host_two.chemical_capacity(voltage, self.temperature_k)
        np.testing.assert_allclose(
            blend.chemical_capacity(voltage, self.temperature_k),
            expected,
            rtol=0.0,
            atol=0.0,
        )
        target_voltage = 0.16
        target_capacity = blend.chemical_capacity(
            target_voltage, self.temperature_k
        )
        recovered = blend.solve_internal_potential(
            target_capacity, self.temperature_k, (-0.2, 0.4)
        )
        self.assertAlmostEqual(recovered, target_voltage, places=10)
        self.assertTrue(blend.equilibrium_only)

    def test_blend_inverse_rejects_conflicting_host_directions(self) -> None:
        increasing = self._host(name="increasing")
        decreasing = self._host(
            self._transition(orientation=-1),
            name="decreasing",
        )
        blend = self.model.PhysicalHostBlend(
            hosts=(increasing, decreasing),
            normalization_basis="synthetic common basis",
        )
        with self.assertRaisesRegex(ValueError, "directions conflict"):
            blend.solve_internal_potential(
                target_capacity_mAh=2.0,
                temperature_k=self.temperature_k,
                bracket_v=(-0.2, 0.4),
            )

    def test_blend_rejects_mixed_physical_constants_at_construction(self) -> None:
        host_one = self._host(name="reference-constants")
        different_constants = self.model.PhysicalConstants(
            faraday_c_per_mol=96_000.0
        )
        host_two = self._host(
            name="different-constants",
            constants=different_constants,
        )
        with self.assertRaisesRegex(ValueError, "identical PhysicalConstants"):
            self.model.PhysicalHostBlend(
                hosts=(host_one, host_two),
                normalization_basis="synthetic common basis",
            )

    def test_objects_are_immutable_and_construction_order_has_no_effect(self) -> None:
        transition = self._transition()
        host = self._host(transition)
        before = np.asarray(
            host.chemical_capacity(
                np.linspace(0.0, 0.2, 11), self.temperature_k
            )
        )
        with self.assertRaises((FrozenInstanceError, AttributeError, TypeError)):
            transition.center_v_ref = 9.9
        with self.assertRaises((FrozenInstanceError, AttributeError, TypeError)):
            host.name = "mutated"

        # Constructing an unrelated profile with different z/orientation must
        # not alter the already-created host or any process-global constants.
        other = self._host(
            self._transition(
                center_v_ref=-0.4,
                orientation=-1,
                electron_stoichiometry=3.0,
            ),
            name="other",
        )
        other.chemical_capacity(0.0, 350.0)
        after = np.asarray(
            host.chemical_capacity(
                np.linspace(0.0, 0.2, 11), self.temperature_k
            )
        )
        np.testing.assert_array_equal(after, before)


if __name__ == "__main__":
    unittest.main()
