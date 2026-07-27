"""SI rate-unit, reversible-heat, and dissipation conformance gates."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import math
import unittest

import numpy as np

from _reference import import_model, local_network_expected_w


class RateUnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = import_model()

    def test_c_rate_hour_to_second_conversion_is_exact(self) -> None:
        self.assertEqual(
            self.model.c_rate_per_hour_to_per_second(1.0), 1.0 / 3600.0
        )
        np.testing.assert_array_equal(
            self.model.c_rate_per_hour_to_per_second(
                np.asarray([-2.0, 0.0, 3.0])
            ),
            np.asarray([-2.0, 0.0, 3.0]) / 3600.0,
        )
        with self.assertRaises(ValueError):
            self.model.c_rate_per_hour_to_per_second(np.inf)

    def test_legacy_hour_rate_requires_an_explicit_conversion(self) -> None:
        legacy = self.model.LegacyCompatibleHourRate(
            per_hour=3600.0,
            provenance="named frozen hour-basis regression",
        )
        self.assertEqual(legacy.to_physical_per_second(), 1.0)
        with self.assertRaises((FrozenInstanceError, AttributeError, TypeError)):
            legacy.per_hour = 1.0
        with self.assertRaises(ValueError):
            self.model.LegacyCompatibleHourRate(1.0, "")
        for invalid_rate in (0.0, -1.0, np.inf):
            with self.subTest(invalid_rate=invalid_rate):
                with self.assertRaises(ValueError):
                    self.model.LegacyCompatibleHourRate(
                        invalid_rate, "invalid magnitude"
                    )

    def test_eyring_rate_matches_the_si_formula(self) -> None:
        temperature = 315.0
        enthalpy = 45_000.0
        entropy = -12.0
        transmission = 0.37
        rate_model = self.model.EyringRateSI(
            activation_enthalpy_j_per_mol=enthalpy,
            activation_entropy_j_per_mol_k=entropy,
            transmission_factor=transmission,
        )
        constants = self.model.SI_CONSTANTS
        expected = (
            constants.boltzmann_j_per_k
            * temperature
            / constants.planck_j_s
            * transmission
            * math.exp(
                entropy / constants.gas_constant_j_per_mol_k
                - enthalpy
                / (constants.gas_constant_j_per_mol_k * temperature)
            )
        )
        self.assertAlmostEqual(
            rate_model.rate_s_inverse(temperature), expected, places=13
        )
        np.testing.assert_allclose(
            rate_model.rate_s_inverse(np.asarray([300.0, 315.0])),
            [
                (
                    constants.boltzmann_j_per_k
                    * value
                    / constants.planck_j_s
                    * transmission
                    * math.exp(
                        entropy / constants.gas_constant_j_per_mol_k
                        - enthalpy
                        / (constants.gas_constant_j_per_mol_k * value)
                    )
                )
                for value in (300.0, 315.0)
            ],
            rtol=2.0e-15,
            atol=0.0,
        )

    def test_eyring_invalid_or_unrepresentable_domains_fail_fast(self) -> None:
        with self.assertRaises(ValueError):
            self.model.EyringRateSI(1.0, 1.0, 0.0)
        model = self.model.EyringRateSI(1.0e9, 0.0, 1.0)
        with self.assertRaises(OverflowError):
            model.rate_s_inverse(298.15)
        with self.assertRaises(ValueError):
            model.rate_s_inverse(0.0)


class HeatConventionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = import_model()

    def test_reversible_heat_uses_generation_positive_minus_sign(self) -> None:
        self.assertAlmostEqual(
            self.model.reversible_heat_generation_w(
                current_a=2.0,
                temperature_k=300.0,
                d_equilibrium_potential_dT_v_per_k=1.0e-3,
            ),
            -0.6,
            places=15,
        )
        self.assertAlmostEqual(
            self.model.reversible_heat_generation_w(
                current_a=-2.0,
                temperature_k=300.0,
                d_equilibrium_potential_dT_v_per_k=1.0e-3,
            ),
            0.6,
            places=15,
        )

    def test_terminal_lumped_heat_enforces_nonnegative_domain(self) -> None:
        self.assertAlmostEqual(
            self.model.terminal_irreversible_heat_w(
                current_a=2.0,
                equilibrium_potential_v=1.0,
                terminal_potential_v=0.8,
            ),
            0.4,
            places=15,
        )
        self.assertEqual(
            self.model.terminal_irreversible_heat_w(0.0, 1.0, 0.8),
            0.0,
        )
        with self.assertRaises(self.model.HeatDomainError):
            self.model.terminal_irreversible_heat_w(2.0, 0.8, 1.0)
        self.assertAlmostEqual(
            self.model.terminal_irreversible_heat_w(
                2.0, 0.8, 1.0, require_nonnegative=False
            ),
            -0.4,
            places=15,
        )

    def test_local_entropy_production_matches_network_law_and_is_nonnegative(
        self,
    ) -> None:
        arguments = {
            "transition_charge_c": 360.0,
            "electron_stoichiometry": 1.0,
            "temperature_k": 300.0,
            "forward_flux_s_inverse": 2.0,
            "backward_flux_s_inverse": 0.5,
        }
        expected = local_network_expected_w(
            arguments["transition_charge_c"],
            arguments["electron_stoichiometry"],
            arguments["temperature_k"],
            arguments["forward_flux_s_inverse"],
            arguments["backward_flux_s_inverse"],
        )
        actual = self.model.local_network_irreversible_heat_w(**arguments)
        self.assertAlmostEqual(actual, expected, places=14)
        self.assertGreater(actual, 0.0)

        reverse = self.model.local_network_irreversible_heat_w(
            transition_charge_c=360.0,
            electron_stoichiometry=1.0,
            temperature_k=300.0,
            forward_flux_s_inverse=0.5,
            backward_flux_s_inverse=2.0,
        )
        self.assertAlmostEqual(reverse, expected, places=14)
        self.assertEqual(
            self.model.local_network_irreversible_heat_w(
                360.0, 1.0, 300.0, 1.0, 1.0
            ),
            0.0,
        )

    def test_local_entropy_production_rejects_invalid_flux_or_charge(self) -> None:
        for arguments in (
            (0.0, 1.0, 300.0, 1.0, 1.0),
            (360.0, 0.0, 300.0, 1.0, 1.0),
            (360.0, 1.0, 0.0, 1.0, 1.0),
            (360.0, 1.0, 300.0, 0.0, 1.0),
            (360.0, 1.0, 300.0, 1.0, -1.0),
        ):
            with self.subTest(arguments=arguments):
                with self.assertRaises(ValueError):
                    self.model.local_network_irreversible_heat_w(*arguments)


if __name__ == "__main__":
    unittest.main()
