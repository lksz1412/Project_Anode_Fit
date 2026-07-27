"""Separate reversible, terminal-lumped, and local irreversible heat helpers."""

from __future__ import annotations

import math

import numpy as np

from .constants import PhysicalConstants, SI_CONSTANTS
from .numerics import as_finite_float, as_positive_float


class HeatDomainError(ValueError):
    """Raised when a claimed dissipative heat law violates its domain."""


def reversible_heat_generation_w(
    current_a: float,
    temperature_k: float,
    d_equilibrium_potential_dT_v_per_k: float,
) -> float:
    """Return generation-positive reversible heat ``-I*T*dUeq/dT``.

    ``current_a`` must use the same written-forward-reaction convention as
    ``Ueq``.  This helper does not infer a half-cell spatial allocation.

    Physics IDs: PHY-019, PHY-020, PHY-021, PHY-032.
    """

    current = as_finite_float("current_a", current_a)
    temperature = as_positive_float("temperature_k", temperature_k)
    coefficient = as_finite_float(
        "d_equilibrium_potential_dT_v_per_k",
        d_equilibrium_potential_dT_v_per_k,
    )
    return -current * temperature * coefficient


def terminal_irreversible_heat_w(
    current_a: float,
    equilibrium_potential_v: float,
    terminal_potential_v: float,
    *,
    require_nonnegative: bool = True,
    numerical_tolerance_w: float = 1.0e-12,
) -> float:
    """Return bounded terminal-lumped ``I*(U_oc-V)`` in W.

    This excludes rest-time internal relaxation and hidden state-energy
    storage.  It is not a replacement for the local network law.

    Physics IDs: PHY-022, PHY-023, C-008, PHY-032.
    """

    current = as_finite_float("current_a", current_a)
    equilibrium = as_finite_float(
        "equilibrium_potential_v", equilibrium_potential_v
    )
    terminal = as_finite_float("terminal_potential_v", terminal_potential_v)
    tolerance = as_positive_float("numerical_tolerance_w", numerical_tolerance_w)
    power = current * (equilibrium - terminal)
    if require_nonnegative and power < -tolerance:
        raise HeatDomainError(
            "I*(U_oc-V) is negative under the declared dissipative domain"
        )
    if require_nonnegative and power < 0.0:
        return 0.0
    return power


def local_network_irreversible_heat_w(
    transition_charge_c: float,
    electron_stoichiometry: float,
    temperature_k: float,
    forward_flux_s_inverse: float,
    backward_flux_s_inverse: float,
    *,
    constants: PhysicalConstants = SI_CONSTANTS,
) -> float:
    """Return two-state local irreversible power in W.

    Implements
    ``Q/(zF) * R*T * (J+ - J-) * log(J+/J-)`` with strictly positive
    occupancy fluxes in s^-1 and transition charge in coulombs.

    Physics IDs: PHY-005, PHY-014, PHY-022, PHY-023, PHY-032.
    """

    charge = as_positive_float("transition_charge_c", transition_charge_c)
    stoichiometry = as_positive_float(
        "electron_stoichiometry", electron_stoichiometry
    )
    temperature = as_positive_float("temperature_k", temperature_k)
    forward = as_positive_float("forward_flux_s_inverse", forward_flux_s_inverse)
    backward = as_positive_float(
        "backward_flux_s_inverse", backward_flux_s_inverse
    )
    if not isinstance(constants, PhysicalConstants):
        raise TypeError("constants must be PhysicalConstants")

    log_ratio = math.log(forward) - math.log(backward)
    power = (
        charge
        / (stoichiometry * constants.faraday_c_per_mol)
        * constants.gas_constant_j_per_mol_k
        * temperature
        * (forward - backward)
        * log_ratio
    )
    tolerance = (
        128.0
        * np.finfo(np.float64).eps
        * max(1.0, abs(power))
    )
    if power < -tolerance:
        raise HeatDomainError("local entropy production became negative")
    return max(0.0, power)
