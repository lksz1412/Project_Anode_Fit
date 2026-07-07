"""Anode_Fit 1.0.18.2 dQ/dV 개형 검증 플롯.

use_w_eff 제거(v12=1.0.10) 후 코드가 *정상 종모양* dQ/dV 를 그리는지,
4패널 생성·저장.
(추측 아님 — Anode_Fit 모듈 실제 호출.)
"""
from __future__ import annotations

import importlib.util
import os
from typing import Tuple

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figs")
os.makedirs(FIGDIR, exist_ok=True)


def _load_module(fname: str):
    path = os.path.join(HERE, fname)
    spec = importlib.util.spec_from_file_location("anode_fit_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fwhm_area(V: np.ndarray, y: np.ndarray) -> Tuple[float, float, float]:
    """FWHM [mV], 면적(∫y dV), peak 높이."""
    base = float(np.min(y))
    yk = y - base
    peak = float(np.max(yk))
    area = float(np.sum((y[:-1] + y[1:]) / 2.0 * np.diff(V)))
    half = peak / 2.0
    above = np.where(yk >= half)[0]
    if above.size >= 2:
        fwhm = (V[above[-1]] - V[above[0]]) * 1000.0
    else:
        fwhm = float("nan")
    return fwhm, area, peak + base


def main() -> None:
    af = _load_module("Anode_Fit_v1.0.18.2.py")  # release 1.0.18.2
    Model = af.GraphiteAnodeDischargeDQDV
    STAGING = af.GRAPHITE_STAGING_LIT

    fig, ax = plt.subplots(2, 2, figsize=(15, 9))
    fig.suptitle(
        "Anode_Fit 1.0.18.2 - dQ/dV bell shapes (code actual output)",
        fontsize=13, fontweight="bold",
    )

    # (1) full equilibrium dQ/dV (4 transitions) -> skewed bell
    full = Model(STAGING, x=0.5, Rn=0.01, Cbg=0.05)
    V1 = np.linspace(0.04, 0.26, 1200)
    eq1 = np.asarray(full.equilibrium(V1, T=298.15), dtype=float)
    ax[0, 0].plot(V1, eq1, color="tab:green", lw=2)
    ax[0, 0].set_title("(1) full equilibrium dQ/dV (4 staging transitions) -> bells")
    ax[0, 0].set_xlabel("V [V vs Li/Li+]")
    ax[0, 0].set_ylabel("dQ/dV")
    ax[0, 0].grid(alpha=0.3)

    # (2) single LiC6 transition equilibrium -> bell. default(n=1.0 -> w=RT/F)
    #     vs explicit per-transition w=12 mV (legacy fallback, inert under 'n' precedence)
    import copy
    lic6 = [t for t in STAGING if abs(float(t["U"]) - 0.085) < 0.01]
    single = Model(lic6, x=0.5, Rn=0.01, Cbg=0.0)
    lic6_w = copy.deepcopy(lic6)
    for t in lic6_w:
        t.pop("n", None)  # remove 'n' so explicit 'w'=0.012 is used (radius test)
    single_w = Model(lic6_w, x=0.5, Rn=0.01, Cbg=0.0)
    Vwide = np.linspace(-0.10, 0.28, 3000)   # wide grid for area conservation
    Vshow = np.linspace(0.0, 0.18, 1600)
    eq2 = np.asarray(single.equilibrium(Vshow, T=298.15), dtype=float)
    eq2w = np.asarray(single_w.equilibrium(Vshow, T=298.15), dtype=float)
    _, area2_wide, _ = fwhm_area(Vwide, np.asarray(single.equilibrium(Vwide, T=298.15), float))
    fwhm2, _, _ = fwhm_area(Vshow, eq2)
    fwhm2w, _, _ = fwhm_area(Vshow, eq2w)
    ax[0, 1].plot(Vshow, eq2, color="tab:blue", lw=2, label=f"default n=1.0 (w=RT/F): FWHM {fwhm2:.0f} mV")
    ax[0, 1].plot(Vshow, eq2w, color="tab:gray", lw=2, ls="--", label=f"explicit w=12 mV (legacy): FWHM {fwhm2w:.0f} mV")
    ax[0, 1].set_title(
        "(2) single LiC6 equilibrium -> BELL\n"
        f"default area(wide grid) = Q = {area2_wide:.3f} (conserved)"
    )
    ax[0, 1].set_xlabel("V [V vs Li/Li+]")
    ax[0, 1].set_ylabel("dQ/dV")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)
    area2 = area2_wide

    # (3) observed dQ/dV: discharge vs charge (hysteresis branches)
    V3 = np.linspace(0.04, 0.30, 1200)
    dis = np.asarray(full.dqdv(V3, T=298.15, I_abs=0.1, Q_cell=1.0, s=+1), dtype=float)
    chg = np.asarray(full.dqdv(V3, T=298.15, I_abs=0.1, Q_cell=1.0, s=-1), dtype=float)
    ax[1, 0].plot(V3, dis, color="tab:red", lw=2, label="discharge (s=+1)")
    ax[1, 0].plot(V3, chg, color="tab:purple", lw=2, ls="--", label="charge (s=-1)")
    ax[1, 0].set_title("(3) observed dQ/dV: discharge vs charge (kinetic tail + hysteresis)")
    ax[1, 0].set_xlabel("V [V vs Li/Li+]")
    ax[1, 0].set_ylabel("dQ/dV")
    ax[1, 0].legend(fontsize=9)
    ax[1, 0].grid(alpha=0.3)

    # (4) temperature comparison (equilibrium width follows RT/F)
    V4 = np.linspace(0.0, 0.175, 1400)
    for T, c in [(278.15, "tab:cyan"), (298.15, "tab:blue"), (328.15, "tab:orange")]:
        eq4 = np.asarray(single.equilibrium(V4, T=T), dtype=float)
        f4, a4, _ = fwhm_area(V4, eq4)
        ax[1, 1].plot(V4, eq4, color=c, lw=2, label=f"T={T - 273.15:.0f}C  FWHM {f4:.1f} mV, area {a4:.2f}")
    ax[1, 1].set_title("(4) single LiC6 equilibrium vs temperature (width ~ RT/F)")
    ax[1, 1].set_xlabel("V [V vs Li/Li+]")
    ax[1, 1].set_ylabel("dQ/dV")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    plt.tight_layout(rect=(0, 0, 1, 0.96))
    out = os.path.join(FIGDIR, "anode_fit_v1_0_14_dqdv.png")
    plt.savefig(out, dpi=110)
    print("SAVED:", out)

    # numeric verdict
    full_fwhm, full_area, full_peak = fwhm_area(V1, eq1)
    print(f"(1) full eq dQ/dV: peak={full_peak:.3f}, area={full_area:.3f}")
    print(f"(2) single LiC6 : FWHM={fwhm2:.2f} mV, area(Q)={area2:.4f}  (Q_LiC6={float(lic6[0]['Q'])})")
    print(f"(3) discharge peak max={float(np.max(dis)):.3f}, charge peak max={float(np.max(chg)):.3f}")
    spike = np.any(eq2 < 0) or fwhm2 < 5.0
    print("SHAPE OK (bell, no spike/broken, area conserved):", (not spike) and abs(area2 - float(lic6[0]['Q'])) < 0.02)


if __name__ == "__main__":
    main()
