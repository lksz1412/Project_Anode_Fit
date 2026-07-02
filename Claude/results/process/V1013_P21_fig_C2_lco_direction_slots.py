from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def xi_eq(v_grid, center, width, sigma):
    """Evaluate the direction-slotted logistic progress variable."""
    return 1.0 / (1.0 + np.exp(-sigma * (v_grid - center) / width))


def main():
    out_dir = Path(__file__).resolve().parent
    out_png = out_dir / "V1013_P21_fig_C2_lco_direction_slots.png"

    center = 4.00
    width = 0.035
    v_grid = np.linspace(3.82, 4.18, 900)

    xi_plus = xi_eq(v_grid, center, width, +1)
    xi_minus = xi_eq(v_grid, center, width, -1)
    peak_plus = xi_plus * (1.0 - xi_plus) / width
    peak_minus = xi_minus * (1.0 - xi_minus) / width

    symmetry_error = np.max(np.abs(xi_minus - (1.0 - xi_plus)))
    peak_error = np.max(np.abs(peak_minus - peak_plus))

    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.2), constrained_layout=True)

    axes[0].plot(v_grid, xi_plus, color="#1b6ca8", lw=2.2, label="sigma=+1")
    axes[0].plot(v_grid, xi_minus, color="#c43b3b", lw=2.2, ls="--", label="sigma=-1")
    axes[0].axvline(center, color="0.35", lw=1.0, ls=":")
    axes[0].set_xlabel("V vs Li (V)")
    axes[0].set_ylabel("xi_eq")
    axes[0].set_title("Progress variable")
    axes[0].legend(frameon=False, loc="center right")
    axes[0].text(3.835, 0.88, "LCO charge -> +1", fontsize=8)
    axes[0].text(3.835, 0.79, "LCO discharge -> -1", fontsize=8)

    axes[1].plot(v_grid, peak_plus, color="#1b6ca8", lw=2.2, label="sigma=+1")
    axes[1].plot(v_grid, peak_minus, color="#c43b3b", lw=2.2, ls="--", label="sigma=-1")
    axes[1].axvline(center, color="0.35", lw=1.0, ls=":")
    axes[1].set_xlabel("V vs Li (V)")
    axes[1].set_ylabel("xi(1-xi)/w")
    axes[1].set_title("Peak magnitude")
    axes[1].legend(frameon=False, loc="upper right")
    axes[1].text(3.835, peak_plus.max() * 0.78, "same peak shape", fontsize=8)

    for ax in axes:
        ax.grid(True, color="0.88", lw=0.8)
        ax.set_xlim(v_grid.min(), v_grid.max())

    fig.suptitle(
        "LCO direction slot: complement in xi, invariant peak magnitude",
        fontsize=10,
    )
    fig.savefig(out_png, dpi=200)
    print(f"wrote {out_png}")
    print(f"complement_error={symmetry_error:.3e}")
    print(f"peak_error={peak_error:.3e}")


if __name__ == "__main__":
    main()
