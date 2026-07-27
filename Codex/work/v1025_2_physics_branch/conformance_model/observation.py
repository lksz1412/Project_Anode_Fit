"""Explicit maps between signed chemical derivatives and fit observations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from .numerics import ScalarOrArray, finite_array, scalarize_like


class ObservationMode(str, Enum):
    """Dataset-level observation transformations."""

    SIGNED = "signed"
    FIXED_SIGN = "fixed-sign"
    MAGNITUDE = "magnitude"


class IrrecoverableObservationSignError(ValueError):
    """Raised when a magnitude observation is asked to recover lost sign."""


@dataclass(frozen=True, slots=True)
class ObservationContract:
    """Immutable signed/fixed-sign/magnitude preprocessing contract.

    ``MAGNITUDE`` deliberately has no inverse.  A positive fitted component
    therefore cannot be used to infer signed storage, reaction orientation, or
    current direction.

    Physics IDs: PHY-001, PHY-004, PHY-007, PHY-029, PHY-030, PHY-032.
    """

    mode: ObservationMode
    provenance: str
    sign: int | None = None

    def __post_init__(self) -> None:
        mode = ObservationMode(self.mode)
        object.__setattr__(self, "mode", mode)
        if not self.provenance.strip():
            raise ValueError("observation provenance must be nonempty")
        if mode is ObservationMode.FIXED_SIGN:
            if self.sign not in (-1, 1):
                raise ValueError("fixed-sign observation requires sign=-1 or +1")
        elif self.sign is not None:
            raise ValueError("sign is only valid for fixed-sign observations")

    @classmethod
    def signed(cls, provenance: str) -> "ObservationContract":
        """Construct an identity map for a signed derivative."""

        return cls(ObservationMode.SIGNED, provenance)

    @classmethod
    def fixed_sign(cls, sign: int, provenance: str) -> "ObservationContract":
        """Construct a dataset-wide fixed-sign map."""

        return cls(ObservationMode.FIXED_SIGN, provenance, sign)

    @classmethod
    def magnitude(cls, provenance: str) -> "ObservationContract":
        """Construct a sign-destroying absolute-magnitude map."""

        return cls(ObservationMode.MAGNITUDE, provenance)

    @property
    def preserves_sign_information(self) -> bool:
        """Whether the signed derivative can be recovered uniquely."""

        return self.mode is not ObservationMode.MAGNITUDE

    def to_fit(self, signed_values: ScalarOrArray) -> ScalarOrArray:
        """Map signed data into the declared fit representation."""

        values = finite_array("signed_values", signed_values)
        if self.mode is ObservationMode.SIGNED:
            result = values.copy()
        elif self.mode is ObservationMode.FIXED_SIGN:
            result = float(self.sign) * values
        else:
            result = np.abs(values)
        return scalarize_like(signed_values, result)

    def recover_signed(self, fit_values: ScalarOrArray) -> ScalarOrArray:
        """Invert a sign-preserving map; magnitude preprocessing is not invertible."""

        values = finite_array("fit_values", fit_values)
        if self.mode is ObservationMode.MAGNITUDE:
            raise IrrecoverableObservationSignError(
                "magnitude preprocessing discarded the signed derivative"
            )
        if self.mode is ObservationMode.FIXED_SIGN:
            result = float(self.sign) * values
        else:
            result = values.copy()
        return scalarize_like(fit_values, result)
