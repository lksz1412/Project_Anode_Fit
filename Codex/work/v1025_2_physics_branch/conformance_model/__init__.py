"""v1.0.25.3 physics-conformance candidate API.

The public types deliberately separate positive empirical observations,
physical equilibrium hosts, and named legacy-compatible rate values.  There is
no mutable default profile and no production regular-solution implementation.
"""

from .constants import PhysicalConstants, SI_CONSTANTS
from .dynamics import (
    CausalInitialState,
    InitialConditionProvenance,
    relax_monotonic_curve,
    relax_time_trajectory,
)
from .empirical import (
    EmpiricalArtifactMetadata,
    EmpiricalEvaluationContract,
    EmpiricalSkewComponent,
    EmpiricalSkewProfile,
    little_endian_f64_sha256,
)
from .heat import (
    HeatDomainError,
    local_network_irreversible_heat_w,
    reversible_heat_generation_w,
    terminal_irreversible_heat_w,
)
from .kinetics import (
    EyringRateSI,
    LegacyCompatibleHourRate,
    c_rate_per_hour_to_per_second,
)
from .numerics import safe_logistic
from .observation import (
    IrrecoverableObservationSignError,
    ObservationContract,
    ObservationMode,
)
from .physical import (
    IdealTransition,
    LinearChemicalBackground,
    PhysicalHost,
    PhysicalHostBlend,
)
from .presets import (
    EMPIRICAL_BLEND14_V10252_ARTIFACT,
    empirical_blend14_v10252,
)


__all__ = [
    "CausalInitialState",
    "EMPIRICAL_BLEND14_V10252_ARTIFACT",
    "EmpiricalArtifactMetadata",
    "EmpiricalEvaluationContract",
    "EmpiricalSkewComponent",
    "EmpiricalSkewProfile",
    "EyringRateSI",
    "HeatDomainError",
    "IdealTransition",
    "InitialConditionProvenance",
    "IrrecoverableObservationSignError",
    "LegacyCompatibleHourRate",
    "LinearChemicalBackground",
    "ObservationContract",
    "ObservationMode",
    "PhysicalConstants",
    "PhysicalHost",
    "PhysicalHostBlend",
    "SI_CONSTANTS",
    "c_rate_per_hour_to_per_second",
    "empirical_blend14_v10252",
    "little_endian_f64_sha256",
    "local_network_irreversible_heat_w",
    "relax_monotonic_curve",
    "relax_time_trajectory",
    "reversible_heat_generation_w",
    "safe_logistic",
    "terminal_irreversible_heat_w",
]
