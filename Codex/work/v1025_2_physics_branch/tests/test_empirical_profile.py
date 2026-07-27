"""Frozen direct14 empirical-profile reconstruction and area gates."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import json
import unittest

import numpy as np

from _reference import (
    EXPECTED_HASHES,
    EXPECTED_R2,
    EXPECTED_SOURCE_SHA256,
    BLEND_DATA,
    canonical_release_prediction,
    coefficient_of_determination,
    import_model,
    le_f64_sha256,
    processed_blend_curve,
    stored_parameter_vector,
)

EXPECTED_ARTIFACT_SHA256 = (
    "5f352eb95f0fe70cf4f277d4d3073015d3f43db04cc0471d4c016bf270aaea6a"
)
EXPECTED_BUILDER_DEPENDENCIES = {
    "Claude/results/comp_v26_data/test_skew_regsol_v2.py":
        "90ee96c2717d4b12bc94647da58b715c3974c2336bf03907b77c693adebb0c0c",
    "Claude/results/comp_v26_data/bdd_dqdv.py":
        "d3441b15b276ac87c4925c77146a24cdb2e16f1184057f9a17d9d6952daebf2c",
    "Claude/results/comp_v26_data/regsol_kernel.py":
        "ed10c8fc2029e874803ff3b9d208817fb735b75ca71f8e8fd2fe3631870c455e",
    "Claude/results/comp_v24/sintef_data/gr.csv":
        "0deb5d1222ca944eaf128c39ca5b35f59929219a6d9445771088baf2222c39d9",
    "Claude/results/comp_v24/sintef_data/si.csv":
        "8b02c776bc34e8410d86fead875d485905b78b28351ca6b295e433b78ff43ac6",
}


class EmpiricalBlend14ReconstructionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = import_model()
        cls.profile = cls.model.empirical_blend14_v10252()
        cls.voltage, cls.observed = processed_blend_curve()
        cls.prediction = np.asarray(cls.profile.evaluate(cls.voltage), dtype=float)

    def test_profile_is_explicitly_empirical_magnitude_only(self) -> None:
        self.assertIsInstance(self.profile, self.model.EmpiricalSkewProfile)
        self.assertEqual(len(self.profile.components), 14)
        self.assertEqual(
            self.profile.observation_contract.mode,
            self.model.ObservationMode.MAGNITUDE,
        )
        self.assertFalse(
            self.profile.observation_contract.preserves_sign_information
        )
        self.assertIn("EMPIRICAL CURVE REFERENCE", self.profile.metadata.classification)
        self.assertEqual(self.profile.metadata.experimental_protocol, "UNKNOWN")
        self.assertFalse(self.profile.metadata.optimizer_full_precision_available)
        self.assertFalse(self.profile.metadata.optimizer_prediction_available)
        self.assertFalse(
            self.profile.metadata.optimizer_termination_metadata_available
        )
        self.assertFalse(self.profile.metadata.optimizer_active_set_status_available)
        self.assertFalse(self.profile.metadata.builder_required_optimizer_success)

    def test_immutable_artifact_freezes_full_builder_dependency_chain(self) -> None:
        artifact_path = self.model.EMPIRICAL_BLEND14_V10252_ARTIFACT
        artifact_bytes = artifact_path.read_bytes()
        self.assertEqual(
            hashlib.sha256(artifact_bytes).hexdigest(),
            EXPECTED_ARTIFACT_SHA256,
        )
        payload = json.loads(artifact_bytes.decode("utf-8"))
        observed_dependencies = {
            item["path"]: item["sha256"] for item in payload["source_artifacts"]
        }
        repository_root = artifact_path.parents[4]
        for path, expected_hash in EXPECTED_BUILDER_DEPENDENCIES.items():
            with self.subTest(path=path):
                self.assertEqual(observed_dependencies[path], expected_hash)
                self.assertEqual(
                    hashlib.sha256(
                        (repository_root / path).read_bytes()
                    ).hexdigest(),
                    expected_hash,
                )
        note = payload["builder_dependency_chain_note"]
        self.assertIn("global RNG", note)
        self.assertIn("no v1.0.26 scientific authority", note)
        self.assertIn("does not restore optimizer reproducibility", note)

    def test_stored_8dp_parameter_vector_and_hash_are_exact(self) -> None:
        parameters = np.asarray(self.profile.parameter_vector_8dp(), dtype=float)
        np.testing.assert_array_equal(parameters, stored_parameter_vector())
        self.assertEqual(parameters.size, 57)
        self.assertEqual(
            le_f64_sha256(parameters), EXPECTED_HASHES["parameters"]
        )
        self.assertEqual(
            self.profile.hashes["stored_8dp_parameters"],
            EXPECTED_HASHES["parameters"],
        )

    def test_processed_input_hashes_are_reproduced_independently(self) -> None:
        self.assertEqual(
            hashlib.sha256(BLEND_DATA.read_bytes()).hexdigest(),
            EXPECTED_SOURCE_SHA256,
        )
        self.assertEqual(self.profile.metadata.source_sha256, EXPECTED_SOURCE_SHA256)
        self.assertEqual(self.voltage.size, 1280)
        self.assertEqual(
            le_f64_sha256(self.voltage), EXPECTED_HASHES["voltage"]
        )
        self.assertEqual(
            le_f64_sha256(self.observed), EXPECTED_HASHES["observed"]
        )
        self.assertEqual(
            self.profile.hashes["processed_voltage"], EXPECTED_HASHES["voltage"]
        )
        self.assertEqual(
            self.profile.hashes["processed_observation"],
            EXPECTED_HASHES["observed"],
        )

    def test_curve_prediction_residual_hashes_and_r2_are_exact(self) -> None:
        residual = self.observed - self.prediction
        self.assertEqual(
            le_f64_sha256(self.prediction), EXPECTED_HASHES["prediction"]
        )
        self.assertEqual(
            le_f64_sha256(residual), EXPECTED_HASHES["residual"]
        )
        self.assertEqual(
            self.profile.hashes["stored_8dp_reconstructed_prediction"],
            EXPECTED_HASHES["prediction"],
        )
        self.assertEqual(
            self.profile.hashes["stored_8dp_reconstructed_residual"],
            EXPECTED_HASHES["residual"],
        )
        self.assertAlmostEqual(
            coefficient_of_determination(self.observed, self.prediction),
            EXPECTED_R2,
            places=14,
        )

    def test_release_reconstruction_agrees_with_independent_direct_formula(
        self,
    ) -> None:
        direct = canonical_release_prediction(self.voltage)
        self.assertLessEqual(
            float(np.max(np.abs(self.prediction - direct))),
            1.5e-14,
        )

    def test_profile_area_is_sum_of_positive_component_areas(self) -> None:
        voltage = np.linspace(-4.0, 4.0, 400_001)
        density = (
            np.asarray(self.profile.evaluate(voltage), dtype=float)
            - self.profile.background_mAh_per_v
        )
        integrated_area = float(np.trapezoid(density, voltage))
        expected_area = sum(component.area_mAh for component in self.profile.components)
        self.assertGreaterEqual(float(np.min(density)), 0.0)
        self.assertAlmostEqual(integrated_area, expected_area, places=8)

    def test_component_density_is_unit_area_and_nonnegative(self) -> None:
        component = self.model.EmpiricalSkewComponent(
            center_v=0.1,
            width_v=0.02,
            area_mAh=7.5,
            alpha=0.35,
        )
        voltage = np.linspace(-4.0, 4.0, 400_001)
        density = np.asarray(component.density(voltage), dtype=float)
        self.assertGreaterEqual(float(np.min(density)), 0.0)
        self.assertAlmostEqual(float(np.trapezoid(density, voltage)), 1.0, places=9)
        self.assertAlmostEqual(
            component.cumulative(voltage[-1]) - component.cumulative(voltage[0]),
            1.0,
            places=12,
        )

    def test_invalid_empirical_domains_fail_fast(self) -> None:
        component_arguments = {
            "center_v": 0.1,
            "width_v": 0.02,
            "area_mAh": 1.0,
            "alpha": 1.0,
        }
        for changes in (
            {"width_v": 0.0},
            {"width_v": -0.1},
            {"area_mAh": -1.0},
            {"alpha": 0.0},
            {"center_v": np.nan},
        ):
            with self.subTest(changes=changes):
                arguments = component_arguments | changes
                with self.assertRaises(ValueError):
                    self.model.EmpiricalSkewComponent(**arguments)
        with self.assertRaises(ValueError):
            self.profile.evaluate([0.1, np.nan])
        with self.assertRaises(ValueError):
            self.model.EmpiricalSkewProfile(
                components=self.profile.components,
                background_mAh_per_v=self.profile.background_mAh_per_v,
                observation_contract=self.model.ObservationContract.signed(
                    "signed data are not an empirical magnitude preset"
                ),
                metadata=self.profile.metadata,
            )

    def test_profile_and_metadata_are_immutable_and_call_order_independent(
        self,
    ) -> None:
        snapshot = self.prediction.copy()
        with self.assertRaises((FrozenInstanceError, AttributeError, TypeError)):
            self.profile.background_mAh_per_v = 99.0
        with self.assertRaises((FrozenInstanceError, AttributeError, TypeError)):
            self.profile.components[0].center_v = 99.0
        with self.assertRaises(TypeError):
            self.profile.hashes["stored_8dp_parameters"] = "0" * 64

        # Construct and evaluate unrelated physical/rate objects.  No public
        # operation may mutate the named empirical preset or module defaults.
        transition = self.model.IdealTransition(0.2, 3.0, -1, 2.0)
        host = self.model.PhysicalHost("unrelated", (transition,))
        host.chemical_capacity(np.asarray([0.1, 0.2]), 330.0)
        self.model.EyringRateSI(45_000.0, -10.0, 0.5).rate_s_inverse(330.0)
        reloaded = self.model.empirical_blend14_v10252()
        np.testing.assert_array_equal(reloaded.evaluate(self.voltage), snapshot)


class PublicAPIContractTest(unittest.TestCase):
    def test_required_symbols_are_exported_at_package_top_level(self) -> None:
        model = import_model()
        required = {
            "safe_logistic",
            "EmpiricalSkewComponent",
            "EmpiricalSkewProfile",
            "empirical_blend14_v10252",
            "ObservationContract",
            "IdealTransition",
            "LinearChemicalBackground",
            "PhysicalHost",
            "PhysicalHostBlend",
            "CausalInitialState",
            "relax_monotonic_curve",
            "relax_time_trajectory",
            "EyringRateSI",
            "LegacyCompatibleHourRate",
            "c_rate_per_hour_to_per_second",
            "reversible_heat_generation_w",
            "terminal_irreversible_heat_w",
            "local_network_irreversible_heat_w",
        }
        missing = sorted(name for name in required if not hasattr(model, name))
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
