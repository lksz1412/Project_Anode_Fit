"""Numerical primitive and observation-map conformance gates."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import unittest
import warnings

import numpy as np

from _reference import import_model


class SafeLogisticTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = import_model()

    def test_extreme_finite_inputs_are_warning_free_and_finite(self) -> None:
        inputs = np.asarray([-1.0e6, -1000.0, 0.0, 1000.0, 1.0e6])
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            result = np.asarray(self.model.safe_logistic(inputs), dtype=float)
        self.assertTrue(np.all(np.isfinite(result)))
        self.assertTrue(np.all(np.diff(result) >= 0.0))
        np.testing.assert_array_equal(result[[0, 2, 4]], [0.0, 0.5, 1.0])

    def test_scalar_and_array_contracts(self) -> None:
        self.assertIsInstance(self.model.safe_logistic(0.0), float)
        result = self.model.safe_logistic(np.asarray([0.0]))
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (1,))

    def test_nan_fails_fast_while_signed_infinity_is_a_valid_limit(self) -> None:
        with self.assertRaises(ValueError):
            self.model.safe_logistic(np.asarray([0.0, np.nan]))
        np.testing.assert_array_equal(
            self.model.safe_logistic(np.asarray([-np.inf, np.inf])),
            [0.0, 1.0],
        )


class ObservationContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = import_model()
        cls.signed_values = np.asarray([-2.0, -0.5, 1.5])

    def test_signed_contract_is_an_identity_and_round_trips(self) -> None:
        contract = self.model.ObservationContract.signed("signed synthetic data")
        fit = contract.to_fit(self.signed_values)
        np.testing.assert_array_equal(fit, self.signed_values)
        np.testing.assert_array_equal(
            contract.recover_signed(fit), self.signed_values
        )
        self.assertTrue(contract.preserves_sign_information)

    def test_fixed_sign_contract_round_trips(self) -> None:
        contract = self.model.ObservationContract.fixed_sign(
            -1, "dataset-wide capacity convention"
        )
        fit = contract.to_fit(self.signed_values)
        np.testing.assert_array_equal(fit, -self.signed_values)
        np.testing.assert_array_equal(
            contract.recover_signed(fit), self.signed_values
        )
        self.assertTrue(contract.preserves_sign_information)

    def test_magnitude_discards_sign_and_has_no_inverse(self) -> None:
        contract = self.model.ObservationContract.magnitude(
            "absolute Savitzky-Golay ensemble"
        )
        np.testing.assert_array_equal(
            contract.to_fit(self.signed_values), np.abs(self.signed_values)
        )
        self.assertFalse(contract.preserves_sign_information)
        with self.assertRaises(self.model.IrrecoverableObservationSignError):
            contract.recover_signed(np.abs(self.signed_values))

    def test_invalid_contract_domains_fail_fast(self) -> None:
        with self.assertRaises(ValueError):
            self.model.ObservationContract.signed("")
        with self.assertRaises(ValueError):
            self.model.ObservationContract.fixed_sign(
                0, "invalid fixed sign"
            )
        with self.assertRaises(ValueError):
            self.model.ObservationContract(
                self.model.ObservationMode.SIGNED,
                "sign is forbidden in identity mode",
                1,
            )
        contract = self.model.ObservationContract.signed("finite values")
        with self.assertRaises(ValueError):
            contract.to_fit([1.0, np.inf])

    def test_contract_is_immutable(self) -> None:
        contract = self.model.ObservationContract.signed("immutable")
        with self.assertRaises((FrozenInstanceError, AttributeError, TypeError)):
            contract.provenance = "mutated"


if __name__ == "__main__":
    unittest.main()
