"""Equilibrium physical-host charge balance with fixed state orientation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from .constants import PhysicalConstants, SI_CONSTANTS
from .numerics import (
    ScalarOrArray,
    as_finite_float,
    as_positive_float,
    finite_array,
    safe_logistic,
    scalarize_like,
)


def _scalar_if_joint_scalar(
    values: np.ndarray, first: ScalarOrArray, second: ScalarOrArray
) -> ScalarOrArray:
    """Scalarize only when both independent inputs were scalar."""

    if np.asarray(first).ndim == 0 and np.asarray(second).ndim == 0:
        return float(np.asarray(values))
    return values


@dataclass(frozen=True, slots=True)
class IdealTransition:
    """Independent-site ideal transition with fixed orientation and ``z``.

    ``signed_capacity_mAh`` is
    :math:`a_j=(partial Q_chem/partial xi_j)` in the declared electrode
    convention.  ``orientation`` is the fixed sign of state change with
    increasing internal potential.  Neither is inferred from observed peak
    width or from an empirical magnitude fit.

    Physics IDs: PHY-001, PHY-002, PHY-005, PHY-006, PHY-009, PHY-019,
    PHY-021, PHY-032.
    """

    center_v_ref: float
    signed_capacity_mAh: float
    orientation: int
    electron_stoichiometry: float = 1.0
    reference_temperature_k: float = 298.15
    d_center_dT_v_per_k: float = 0.0
    label: str = ""
    evidence_grade: str = "not identified"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "center_v_ref", as_finite_float("center_v_ref", self.center_v_ref)
        )
        object.__setattr__(
            self,
            "signed_capacity_mAh",
            as_finite_float("signed_capacity_mAh", self.signed_capacity_mAh),
        )
        if self.orientation not in (-1, 1):
            raise ValueError("orientation must be fixed at -1 or +1")
        object.__setattr__(
            self,
            "electron_stoichiometry",
            as_positive_float(
                "electron_stoichiometry", self.electron_stoichiometry
            ),
        )
        object.__setattr__(
            self,
            "reference_temperature_k",
            as_positive_float(
                "reference_temperature_k", self.reference_temperature_k
            ),
        )
        object.__setattr__(
            self,
            "d_center_dT_v_per_k",
            as_finite_float(
                "d_center_dT_v_per_k", self.d_center_dT_v_per_k
            ),
        )
        if not self.evidence_grade.strip():
            raise ValueError("evidence_grade must be nonempty")

    def center_v(self, temperature_k: ScalarOrArray) -> ScalarOrArray:
        """Return the declared fixed-state transition center."""

        temperature = finite_array("temperature_k", temperature_k)
        if np.any(temperature <= 0.0):
            raise ValueError("temperature_k must be > 0")
        result = self.center_v_ref + self.d_center_dT_v_per_k * (
            temperature - self.reference_temperature_k
        )
        return scalarize_like(temperature_k, result)

    def equilibrium_state(
        self,
        internal_potential_v: ScalarOrArray,
        temperature_k: ScalarOrArray,
        *,
        constants: PhysicalConstants = SI_CONSTANTS,
    ) -> ScalarOrArray:
        """Return the bounded ideal-lattice equilibrium state."""

        if not isinstance(constants, PhysicalConstants):
            raise TypeError("constants must be PhysicalConstants")
        potential = finite_array("internal_potential_v", internal_potential_v)
        temperature = finite_array("temperature_k", temperature_k)
        if np.any(temperature <= 0.0):
            raise ValueError("temperature_k must be > 0")
        center = np.asarray(self.center_v(temperature), dtype=np.float64)
        exponent = (
            self.orientation
            * self.electron_stoichiometry
            * constants.faraday_c_per_mol
            * (potential - center)
            / (constants.gas_constant_j_per_mol_k * temperature)
        )
        result = np.asarray(safe_logistic(exponent), dtype=np.float64)
        return _scalar_if_joint_scalar(
            result, internal_potential_v, temperature_k
        )

    def dstate_dv(
        self,
        internal_potential_v: ScalarOrArray,
        temperature_k: ScalarOrArray,
        *,
        constants: PhysicalConstants = SI_CONSTANTS,
    ) -> ScalarOrArray:
        """Return the signed ideal-state derivative with respect to ``V_n``."""

        temperature = finite_array("temperature_k", temperature_k)
        if np.any(temperature <= 0.0):
            raise ValueError("temperature_k must be > 0")
        state = np.asarray(
            self.equilibrium_state(
                internal_potential_v, temperature, constants=constants
            ),
            dtype=np.float64,
        )
        slope = (
            self.orientation
            * self.electron_stoichiometry
            * constants.faraday_c_per_mol
            / (constants.gas_constant_j_per_mol_k * temperature)
        )
        result = slope * state * (1.0 - state)
        return _scalar_if_joint_scalar(
            result, internal_potential_v, temperature_k
        )


@dataclass(frozen=True, slots=True)
class LinearChemicalBackground:
    """Minimal explicit chemical-storage background.

    This object belongs to :math:`Q_bg^chem`; it is not an observation
    baseline.  A more complex free-energy closure must use a different
    physical type rather than overloading an empirical constant.

    Physics IDs: PHY-004, PHY-010, PHY-011, PHY-032.
    """

    reference_potential_v: float = 0.0
    reference_capacity_mAh: float = 0.0
    chemical_capacitance_mAh_per_v: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "reference_potential_v",
            as_finite_float("reference_potential_v", self.reference_potential_v),
        )
        object.__setattr__(
            self,
            "reference_capacity_mAh",
            as_finite_float("reference_capacity_mAh", self.reference_capacity_mAh),
        )
        capacitance = as_finite_float(
            "chemical_capacitance_mAh_per_v",
            self.chemical_capacitance_mAh_per_v,
        )
        if capacitance < 0.0:
            raise ValueError(
                "chemical_capacitance_mAh_per_v must be >= 0; "
                "use signed transition storage for orientation"
            )
        object.__setattr__(self, "chemical_capacitance_mAh_per_v", capacitance)

    def capacity(self, internal_potential_v: ScalarOrArray) -> ScalarOrArray:
        """Evaluate the signed chemical-background capacity."""

        potential = finite_array("internal_potential_v", internal_potential_v)
        result = self.reference_capacity_mAh + self.chemical_capacitance_mAh_per_v * (
            potential - self.reference_potential_v
        )
        return scalarize_like(internal_potential_v, result)

    def derivative(self, internal_potential_v: ScalarOrArray) -> ScalarOrArray:
        """Return ``dQ_bg^chem/dV_n`` in mAh/V."""

        potential = finite_array("internal_potential_v", internal_potential_v)
        result = np.full(
            potential.shape,
            self.chemical_capacitance_mAh_per_v,
            dtype=np.float64,
        )
        return scalarize_like(internal_potential_v, result)


def _solve_monotonic_inverse(
    capacity: Callable[[float], float],
    derivative: Callable[[np.ndarray], np.ndarray],
    certified_direction: int,
    target_capacity_mAh: float,
    bracket_v: tuple[float, float],
    *,
    absolute_tolerance_v: float,
    max_iterations: int,
) -> float:
    """Bisection with an explicit monotonic-admissibility gate."""

    target = as_finite_float("target_capacity_mAh", target_capacity_mAh)
    if len(bracket_v) != 2:
        raise ValueError("bracket_v must contain exactly (low, high)")
    low = as_finite_float("bracket_v[0]", bracket_v[0])
    high = as_finite_float("bracket_v[1]", bracket_v[1])
    if not low < high:
        raise ValueError("bracket_v must be strictly increasing")
    tolerance = as_positive_float("absolute_tolerance_v", absolute_tolerance_v)
    if max_iterations <= 0:
        raise ValueError("max_iterations must be > 0")

    probe = np.linspace(low, high, 257, dtype=np.float64)
    slope = np.asarray(derivative(probe), dtype=np.float64)
    if slope.shape != probe.shape or not np.all(np.isfinite(slope)):
        raise ValueError("capacity derivative must be finite on the inversion bracket")
    scale = max(1.0, float(np.max(np.abs(slope))))
    numerical_zero = 64.0 * np.finfo(np.float64).eps * scale
    if certified_direction not in (-1, 1):
        raise ValueError("certified_direction must be -1 or +1")
    if (
        certified_direction > 0
        and np.any(slope < -numerical_zero)
    ) or (
        certified_direction < 0
        and np.any(slope > numerical_zero)
    ):
        raise ValueError(
            "chemical-capacity derivative violates its analytic sign certificate"
        )

    f_low = float(capacity(low)) - target
    f_high = float(capacity(high)) - target
    if not np.isfinite(f_low) or not np.isfinite(f_high):
        raise ValueError("capacity must be finite at both bracket endpoints")
    if f_low == 0.0:
        return low
    if f_high == 0.0:
        return high
    if np.signbit(f_low) == np.signbit(f_high):
        raise ValueError("target capacity is not bracketed")

    for _ in range(max_iterations):
        midpoint = 0.5 * (low + high)
        f_midpoint = float(capacity(midpoint)) - target
        if not np.isfinite(f_midpoint):
            raise ValueError("capacity became nonfinite during inversion")
        if f_midpoint == 0.0 or 0.5 * (high - low) <= tolerance:
            return midpoint
        if np.signbit(f_midpoint) == np.signbit(f_low):
            low, f_low = midpoint, f_midpoint
        else:
            high, f_high = midpoint, f_midpoint
    raise RuntimeError("chemical-capacity inversion did not converge")


@dataclass(frozen=True, slots=True)
class PhysicalHost:
    """Equilibrium host with physical states and signed chemical capacity.

    The host has no empirical skew components, observation baseline, finite-rate
    fallback, or branch-dependent state reorientation.

    Physics IDs: PHY-001, PHY-002, PHY-005, PHY-006, PHY-010, PHY-011,
    PHY-013, PHY-019, PHY-032.
    """

    name: str
    transitions: tuple[IdealTransition, ...]
    chemical_background: LinearChemicalBackground = field(
        default_factory=LinearChemicalBackground
    )
    constants: PhysicalConstants = SI_CONSTANTS

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("physical host name must be nonempty")
        transitions = tuple(self.transitions)
        if not transitions:
            raise ValueError("a physical host requires at least one transition")
        if not all(isinstance(item, IdealTransition) for item in transitions):
            raise TypeError("transitions must contain only IdealTransition")
        object.__setattr__(self, "transitions", transitions)
        if not isinstance(self.chemical_background, LinearChemicalBackground):
            raise TypeError(
                "chemical_background must be LinearChemicalBackground"
            )
        if not isinstance(self.constants, PhysicalConstants):
            raise TypeError("constants must be PhysicalConstants")

    def equilibrium_states(
        self, internal_potential_v: ScalarOrArray, temperature_k: ScalarOrArray
    ) -> tuple[ScalarOrArray, ...]:
        """Return each physical state without assigning an empirical alpha."""

        return tuple(
            transition.equilibrium_state(
                internal_potential_v, temperature_k, constants=self.constants
            )
            for transition in self.transitions
        )

    def chemical_capacity(
        self, internal_potential_v: ScalarOrArray, temperature_k: ScalarOrArray
    ) -> ScalarOrArray:
        """Evaluate ``Q_bg^chem + sum(a_j*xi_j)`` in mAh."""

        potential = finite_array("internal_potential_v", internal_potential_v)
        result = np.asarray(
            self.chemical_background.capacity(potential), dtype=np.float64
        )
        for transition in self.transitions:
            state = np.asarray(
                transition.equilibrium_state(
                    potential, temperature_k, constants=self.constants
                ),
                dtype=np.float64,
            )
            result = result + transition.signed_capacity_mAh * state
        return _scalar_if_joint_scalar(
            result, internal_potential_v, temperature_k
        )

    def dchemical_capacity_dv(
        self, internal_potential_v: ScalarOrArray, temperature_k: ScalarOrArray
    ) -> ScalarOrArray:
        """Differentiate the signed equilibrium charge balance with respect to ``V_n``."""

        potential = finite_array("internal_potential_v", internal_potential_v)
        result = np.asarray(
            self.chemical_background.derivative(potential), dtype=np.float64
        )
        for transition in self.transitions:
            derivative = np.asarray(
                transition.dstate_dv(
                    potential, temperature_k, constants=self.constants
                ),
                dtype=np.float64,
            )
            result = result + transition.signed_capacity_mAh * derivative
        return _scalar_if_joint_scalar(
            result, internal_potential_v, temperature_k
        )

    def monotonic_direction_certificate(self) -> int:
        """Return an analytic global sign certificate for ``dQ_chem/dV_n``.

        A mixed set of signed derivative coefficients is not silently accepted
        on the strength of a finite sampling grid.  Such a host needs a
        separately proved EOS/admissibility closure before inverse use.
        """

        coefficients = [
            self.chemical_background.chemical_capacitance_mAh_per_v,
            *(
                transition.signed_capacity_mAh * transition.orientation
                for transition in self.transitions
            ),
        ]
        has_positive = any(value > 0.0 for value in coefficients)
        has_negative = any(value < 0.0 for value in coefficients)
        if has_positive and has_negative:
            raise ValueError(
                "mixed signed derivative coefficients lack a global monotonic certificate"
            )
        if not has_positive and not has_negative:
            raise ValueError("chemical-capacity inverse is globally non-unique")
        return 1 if has_positive else -1

    def solve_internal_potential(
        self,
        target_capacity_mAh: float,
        temperature_k: float,
        bracket_v: tuple[float, float],
        *,
        absolute_tolerance_v: float = 1.0e-12,
        max_iterations: int = 200,
    ) -> float:
        """Solve the implicit equilibrium charge balance on a declared bracket."""

        temperature = as_positive_float("temperature_k", temperature_k)
        return _solve_monotonic_inverse(
            lambda voltage: float(self.chemical_capacity(voltage, temperature)),
            lambda voltage: np.asarray(
                self.dchemical_capacity_dv(voltage, temperature), dtype=np.float64
            ),
            self.monotonic_direction_certificate(),
            target_capacity_mAh,
            bracket_v,
            absolute_tolerance_v=absolute_tolerance_v,
            max_iterations=max_iterations,
        )


@dataclass(frozen=True, slots=True)
class PhysicalHostBlend:
    """Equilibrium-only sum of physical hosts at one internal potential.

    ``normalization_basis`` is mandatory so a raw sum cannot silently be
    presented as a fixed-total-mass or fixed-total-capacity blend.

    Physics IDs: PHY-002, PHY-010, PHY-011, PHY-012, PHY-013, PHY-032.
    """

    hosts: tuple[PhysicalHost, ...]
    normalization_basis: str

    def __post_init__(self) -> None:
        hosts = tuple(self.hosts)
        if len(hosts) < 2:
            raise ValueError("PhysicalHostBlend requires at least two hosts")
        if not all(isinstance(host, PhysicalHost) for host in hosts):
            raise TypeError("hosts must contain only PhysicalHost")
        names = [host.name for host in hosts]
        if len(names) != len(set(names)):
            raise ValueError("physical host names must be unique within a blend")
        reference_constants = hosts[0].constants
        if any(host.constants != reference_constants for host in hosts[1:]):
            raise ValueError(
                "all physical hosts in a blend must use identical PhysicalConstants"
            )
        if not self.normalization_basis.strip():
            raise ValueError("normalization_basis must be explicit and nonempty")
        object.__setattr__(self, "hosts", hosts)

    @property
    def equilibrium_only(self) -> bool:
        """The blend intentionally exposes no additive finite-rate shortcut."""

        return True

    def chemical_capacity(
        self, internal_potential_v: ScalarOrArray, temperature_k: ScalarOrArray
    ) -> ScalarOrArray:
        """Sum host capacities at a shared internal potential."""

        potential = finite_array("internal_potential_v", internal_potential_v)
        result = np.zeros(potential.shape, dtype=np.float64)
        for host in self.hosts:
            result = result + np.asarray(
                host.chemical_capacity(potential, temperature_k), dtype=np.float64
            )
        return _scalar_if_joint_scalar(
            result, internal_potential_v, temperature_k
        )

    def dchemical_capacity_dv(
        self, internal_potential_v: ScalarOrArray, temperature_k: ScalarOrArray
    ) -> ScalarOrArray:
        """Sum host chemical-capacity derivatives at shared ``V_n``."""

        potential = finite_array("internal_potential_v", internal_potential_v)
        result = np.zeros(potential.shape, dtype=np.float64)
        for host in self.hosts:
            result = result + np.asarray(
                host.dchemical_capacity_dv(potential, temperature_k),
                dtype=np.float64,
            )
        return _scalar_if_joint_scalar(
            result, internal_potential_v, temperature_k
        )

    def monotonic_direction_certificate(self) -> int:
        """Return a shared global inverse-direction certificate for all hosts."""

        directions = tuple(
            host.monotonic_direction_certificate() for host in self.hosts
        )
        if len(set(directions)) != 1:
            raise ValueError(
                "host derivative directions conflict; pooled inverse is inadmissible"
            )
        return directions[0]

    def solve_internal_potential(
        self,
        target_capacity_mAh: float,
        temperature_k: float,
        bracket_v: tuple[float, float],
        *,
        absolute_tolerance_v: float = 1.0e-12,
        max_iterations: int = 200,
    ) -> float:
        """Solve the pooled equilibrium charge balance on a declared bracket."""

        temperature = as_positive_float("temperature_k", temperature_k)
        return _solve_monotonic_inverse(
            lambda voltage: float(self.chemical_capacity(voltage, temperature)),
            lambda voltage: np.asarray(
                self.dchemical_capacity_dv(voltage, temperature), dtype=np.float64
            ),
            self.monotonic_direction_certificate(),
            target_capacity_mAh,
            bracket_v,
            absolute_tolerance_v=absolute_tolerance_v,
            max_iterations=max_iterations,
        )
