#!/usr/bin/env python3
"""Targeted probes for the latest accepted v1.0.25.2 source state.

The Phase 044 probe was written against a release state whose global default
was 7+7 skew components.  The accepted v1.0.25.2 lineage later restored the
thermodynamic four-transition graphite default.  This addendum reruns the old
diagnostics without reusing its stale labels and separately measures the
explicit 7+7 opt-in path.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import warnings

import numpy as np
from scipy.optimize import least_squares

import phase044_current_source_probes as phase044


REPO = Path(__file__).resolve().parents[3]
SOURCE = REPO / "Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py"
GATE = REPO / "Claude/docs/v1.0.25.2/test_gates_v1024.py"
IMPLEMENTATION_APPENDIX = (
    REPO
    / "Codex/results/v1025_2_physics_branch/manuscript/"
    "appendices/implementation_interface.tex"
)
TEMPERATURE_LOW_K = 288.15
TEMPERATURE_HIGH_K = 308.15
TEMPERATURE_GRID_V = np.linspace(0.03, 0.34, 1000)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def temperature_probe(model, skew7: bool) -> dict:
    model.use_skew7_default(skew7)
    host = model.GraphiteAnodeDischargeDQDV(
        model.DEFAULT_GRAPHITE_TRANSITIONS,
        x=0.5,
        Rn=0.01,
        Cbg=0.05,
        use_dH_eff=True,
    )
    low = np.asarray(
        host.equilibrium(TEMPERATURE_GRID_V, TEMPERATURE_LOW_K), dtype=float
    )
    high = np.asarray(
        host.equilibrium(TEMPERATURE_GRID_V, TEMPERATURE_HIGH_K), dtype=float
    )
    return {
        "graphite_transition_count": len(host.transitions),
        "transition_key_sets": [
            sorted(str(key) for key in transition)
            for transition in model.DEFAULT_GRAPHITE_TRANSITIONS
        ],
        "temperature_low_K": TEMPERATURE_LOW_K,
        "temperature_high_K": TEMPERATURE_HIGH_K,
        "voltage_min_V": float(TEMPERATURE_GRID_V[0]),
        "voltage_max_V": float(TEMPERATURE_GRID_V[-1]),
        "voltage_points": int(TEMPERATURE_GRID_V.size),
        "max_abs_equilibrium_difference": float(np.max(np.abs(high - low))),
        "all_finite": bool(np.all(np.isfinite(low)) and np.all(np.isfinite(high))),
    }


def invalid_si_case_probe(model, skew7: bool) -> dict:
    model.use_skew7_default(skew7)
    try:
        candidate = model.BlendedAnodeDQDV(0.2, si_case="not-a-real-case")
    except Exception as exc:
        return {
            "accepted": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
    return {
        "accepted": True,
        "error": None,
        "silicon_transition_count": len(candidate.si_host.transitions),
    }


def fit_default_wiring(model, skew7: bool, voltage, observed) -> dict:
    model.use_skew7_default(skew7)

    def residual(parameters: np.ndarray) -> np.ndarray:
        silicon_fraction, background = parameters
        blend = model.BlendedAnodeDQDV(
            float(silicon_fraction), si_case="sic", Cbg=float(background)
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            prediction = np.asarray(
                blend.equilibrium(voltage, 298.15), dtype=float
            )
        return prediction - observed

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        fit = least_squares(
            residual,
            x0=np.asarray([0.5, 0.0], dtype=float),
            bounds=(
                np.asarray([0.0, 0.0], dtype=float),
                np.asarray([0.99, float(np.max(observed))], dtype=float),
            ),
            method="trf",
            max_nfev=10_000,
            xtol=1.0e-14,
            ftol=1.0e-14,
            gtol=1.0e-14,
        )
    prediction = observed + fit.fun
    probe = model.BlendedAnodeDQDV(
        float(fit.x[0]), si_case="sic", Cbg=float(fit.x[1])
    )
    return {
        "profile": (
            "explicit 7+7 skew opt-in"
            if skew7
            else "current release default: graphite 4 + Si sic case 2"
        ),
        "graphite_transition_count": len(probe.gr_host.transitions),
        "silicon_transition_count": len(probe.si_host.transitions),
        "optimization": (
            "unweighted least_squares over f_Si and Cbg only; "
            "bounds f_Si=[0,0.99], Cbg=[0,max(observed)]"
        ),
        "success": bool(fit.success),
        "status": int(fit.status),
        "nfev": int(fit.nfev),
        "optimized_f_Si": float(fit.x[0]),
        "optimized_Cbg": float(fit.x[1]),
        "optimized_metrics_two_parameters": phase044.metrics(
            observed, prediction, 2
        ),
        "comparison_scope": (
            "A wiring diagnostic, not a mechanism-selection contest: the host "
            "profiles and the accepted direct14 blend fit used different "
            "objectives."
        ),
    }


def run() -> dict:
    source_text = SOURCE.read_text(encoding="utf-8")
    gate_text = GATE.read_text(encoding="utf-8")
    appendix_text = IMPLEMENTATION_APPENDIX.read_text(encoding="utf-8")

    # Rerun all earlier implementation diagnostics against the latest source.
    # Only semantically stable fields are carried forward under fresh labels.
    phase044_latest = phase044.run()
    model = phase044.load_module()
    voltage, observed = phase044.load_blend_dqdv()

    try:
        current_temperature = temperature_probe(model, skew7=False)
        skew7_temperature = temperature_probe(model, skew7=True)
        current_invalid_case = invalid_si_case_probe(model, skew7=False)
        skew7_invalid_case = invalid_si_case_probe(model, skew7=True)
        current_fit = fit_default_wiring(model, False, voltage, observed)
        skew7_fit = fit_default_wiring(model, True, voltage, observed)
    finally:
        model.use_skew7_default(False)

    return {
        "scope": {
            "source": str(SOURCE.relative_to(REPO)),
            "source_sha256": sha256(SOURCE),
            "source_lines": len(source_text.splitlines()),
            "accepted_lineage_tip_reviewed": "3b5fd059ed09cdcdde38668c399cb35b8afbcca9",
            "default_correction_commit_in_lineage": (
                "7b342dd88aad6bf9ff08cb3568da374837008ca7"
            ),
            "probe_role": (
                "latest-release wiring audit; not original optimizer replay"
            ),
        },
        "public_symbols": {
            "use_skew7_default_callable": bool(
                callable(getattr(model, "use_skew7_default", None))
            ),
            "use_legacy_4transition_callable": bool(
                callable(getattr(model, "use_legacy_4transition", None))
            ),
        },
        "source_documentation_residue": {
            "use_legacy_4transition_text_occurrences": source_text.count(
                "use_legacy_4transition"
            ),
            "header_claims_default_7gallery": (
                "기본 전이 셋 = 7-gallery skew" in source_text
            ),
            "constructor_doc_claims_default_7gallery": (
                "DEFAULT_GRAPHITE_TRANSITIONS = 7-gallery skew" in source_text
            ),
            "implementation_appendix_uses_removed_symbol": (
                "use_legacy_4transition" in appendix_text
            ),
        },
        "legacy_gate_scope": {
            "gate": str(GATE.relative_to(REPO)),
            "calls_use_skew7_default_false": (
                "use_skew7_default(False)" in gate_text
            ),
            "interpretation": (
                "The legacy gate restores the four-transition path before its "
                "assertions, so a PASS does not independently test whichever "
                "global default was active on module import."
            ),
        },
        "current_release_default": {
            "constructor": phase044_latest["current_default"],
            "temperature_sensitivity": current_temperature,
            "invalid_si_case": current_invalid_case,
            "blend_data_wiring_fit": current_fit,
        },
        "explicit_skew7_opt_in": {
            "temperature_sensitivity": skew7_temperature,
            "invalid_si_case": skew7_invalid_case,
            "blend_data_wiring_fit": skew7_fit,
        },
        "accepted_direct14_profile": phase044_latest["accepted_empirical_fit"],
        "remaining_implementation_probes": {
            "keyless_temperature_roundtrip": phase044_latest[
                "keyless_temperature_roundtrip"
            ],
            "logistic_warning_probe": phase044_latest[
                "logistic_warning_probe"
            ],
            "rate_and_causal_contract": phase044_latest[
                "rate_and_causal_contract"
            ],
        },
        "supersession": {
            "supersedes_old_default_label": (
                "PHASE_044_CURRENT_SOURCE_PROBES.json:"
                "shipped_default_7plus7_on_blend_data"
            ),
            "does_not_supersede": (
                "accepted direct14 reconstruction, array hashes, or the "
                "non-default implementation probes unless explicitly stated"
            ),
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
