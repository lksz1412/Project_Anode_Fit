"""Coordinate source for T6_logistic.tex."""

from math import exp

R = 8.31446261815324
F = 96485.33212
temps = [268, 298, 328]
voltages_mv = [-120, -90, -60, -30, 0, 30, 60, 90, 120]


def xi_eq(v_mv: float, temp_k: float) -> float:
    w_mv = R * temp_k / F * 1000.0
    return 1.0 / (1.0 + exp(-v_mv / w_mv))


print("T6 logistic coordinates: x = Delta V [mV] / 25")
for temp in temps:
    w_mv = R * temp / F * 1000.0
    xi_coords = []
    der_coords = []
    for v in voltages_mv:
        xi = xi_eq(v, temp)
        dxi_dv = xi * (1.0 - xi) / (w_mv / 1000.0)
        xi_coords.append(f"({v/25.0:.2f},{1.8*xi:.4f})")
        der_coords.append(f"({v/25.0:.2f},{0.13*dxi_dv:.4f})")
    print(f"T={temp} K, w={w_mv:.3f} mV")
    print("xi  " + " ".join(xi_coords))
    print("der " + " ".join(der_coords))
