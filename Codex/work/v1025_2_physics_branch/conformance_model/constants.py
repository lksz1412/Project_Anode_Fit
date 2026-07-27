"""Immutable physical constants used by the conformance implementation."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True, slots=True)
class PhysicalConstants:
    """CODATA-2018 exact/standard constants; no process-global switching.

    Physics IDs: PHY-005, PHY-015, PHY-016, PHY-022, PHY-032.
    """

    gas_constant_j_per_mol_k: float = 8.31446261815324
    faraday_c_per_mol: float = 96485.33212
    boltzmann_j_per_k: float = 1.380649e-23
    planck_j_s: float = 6.62607015e-34

    def __post_init__(self) -> None:
        for name in (
            "gas_constant_j_per_mol_k",
            "faraday_c_per_mol",
            "boltzmann_j_per_k",
            "planck_j_s",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and > 0")
            object.__setattr__(self, name, value)


SI_CONSTANTS = PhysicalConstants()


# These constants exist only to reproduce the surviving v1.0.25.2 empirical
# prediction hash.  They are not selectable physical constants and are never
# used by PhysicalHost, EyringRateSI, or any heat calculation.
V10252_EMPIRICAL_RECONSTRUCTION_R = 8.314
V10252_EMPIRICAL_RECONSTRUCTION_F = 96485.0
V10252_EMPIRICAL_RECONSTRUCTION_T_K = 298.15
