import math

R = 8.314462618
F = 96485.33212
temps = [268, 298, 328]
v_mV = [-120, -90, -60, -30, 0, 30, 60, 90, 120]


def xi(v_mv: float, w_mv: float) -> float:
    return 1.0 / (1.0 + math.exp(-v_mv / w_mv))


for T in temps:
    w_mv = R * T / F * 1000.0
    print(f"T={T} K, w={w_mv:.6f} mV")
    print("xi:", " ".join(f"({v:.1f},{xi(v,w_mv):.4f})" for v in v_mV))
    print("dxidV [1/V]:", " ".join(
        f"({v:.1f},{1000.0 * xi(v,w_mv) * (1.0 - xi(v,w_mv)) / w_mv:.4f})" for v in v_mV
    ))
