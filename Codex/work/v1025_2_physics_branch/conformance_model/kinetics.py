"""SI Eyring rates and explicitly segregated legacy hour-basis values."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .constants import PhysicalConstants, SI_CONSTANTS
from .numerics import (
    ScalarOrArray,
    as_finite_float,
    as_positive_float,
    finite_array,
    scalarize_like,
)


@dataclass(frozen=True, slots=True)
class EyringRateSI:
    """Physical Eyring rate model whose numerical output is in s^-1.

    The transmission factor is explicit and constant over the declared model.
    Temperature-dependent transmission requires a new closure rather than a
    hidden global callback.

    Physics IDs: PHY-014, PHY-015, PHY-016, C-005, C-006, PHY-032.
    """

    activation_enthalpy_j_per_mol: float
    activation_entropy_j_per_mol_k: float
    transmission_factor: float
    constants: PhysicalConstants = SI_CONSTANTS

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "activation_enthalpy_j_per_mol",
            as_finite_float(
                "activation_enthalpy_j_per_mol",
                self.activation_enthalpy_j_per_mol,
            ),
        )
        object.__setattr__(
            self,
            "activation_entropy_j_per_mol_k",
            as_finite_float(
                "activation_entropy_j_per_mol_k",
                self.activation_entropy_j_per_mol_k,
            ),
        )
        object.__setattr__(
            self,
            "transmission_factor",
            as_positive_float("transmission_factor", self.transmission_factor),
        )
        if not isinstance(self.constants, PhysicalConstants):
            raise TypeError("constants must be PhysicalConstants")

    def rate_s_inverse(self, temperature_k: ScalarOrArray) -> ScalarOrArray:
        """Evaluate ``(k_B*T/h)*kappa*exp(dS/R-dH/(R*T))`` in s^-1."""

        temperature = finite_array("temperature_k", temperature_k)
        if np.any(temperature <= 0.0):
            raise ValueError("temperature_k must be > 0")
        exponent = (
            self.activation_entropy_j_per_mol_k
            / self.constants.gas_constant_j_per_mol_k
            - self.activation_enthalpy_j_per_mol
            / (self.constants.gas_constant_j_per_mol_k * temperature)
        )
        with np.errstate(over="ignore", under="ignore"):
            rate = (
                self.constants.boltzmann_j_per_k
                * temperature
                / self.constants.planck_j_s
                * self.transmission_factor
                * np.exp(exponent)
            )
        if not np.all(np.isfinite(rate)) or np.any(rate <= 0.0):
            raise OverflowError(
                "Eyring rate is nonfinite or underflowed; no equilibrium fallback is allowed"
            )
        return scalarize_like(temperature_k, rate)


@dataclass(frozen=True, slots=True)
class LegacyCompatibleHourRate:
    """Named positive historical h^-1 rate magnitude, not a physical SI rate.

    It deliberately has no implicit coercion to float and cannot be consumed by
    :class:`EyringRateSI`.  Call :meth:`to_physical_per_second` to perform the
    explicit 1/3600 conversion.  Signed C-rate conversion belongs only to
    :func:`c_rate_per_hour_to_per_second`.

    Physics IDs: PHY-016, C-006, PHY-032.
    """

    per_hour: float
    provenance: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "per_hour", as_positive_float("per_hour", self.per_hour)
        )
        if not self.provenance.strip():
            raise ValueError("legacy rate provenance must be nonempty")

    def to_physical_per_second(self) -> float:
        """Convert the named historical hour basis to s^-1."""

        return self.per_hour / 3600.0


def c_rate_per_hour_to_per_second(c_rate_per_hour: ScalarOrArray) -> ScalarOrArray:
    """Convert a signed C-rate from h^-1 to s^-1 explicitly."""

    value = finite_array("c_rate_per_hour", c_rate_per_hour)
    result = value / 3600.0
    return scalarize_like(c_rate_per_hour, result)
