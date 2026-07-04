# T6 fig:logistic — equilibrium progress xi_eq and its derivative, temperature dependence.
# eq:wbase  : w_j = n_j R T / F   (n_j = 1 here)
# eq:xieq   : xi_eq(V) = 1/(1+exp[-sigma_d (V-U) / w])   (sigma_d=+1, discharge, s.a. eq:logisticsolve)
# derivative : d(xi_eq)/dV = xi_eq(1-xi_eq)/w   -- max at V=U: 1/(4w)  (central slope, "geometric width")
import math

R = 8.314462618
F = 96485.33212
temps = [268.0, 298.0, 328.0]

def w_of_T(T):
    return R * T / F   # volts

def xi_eq(dV, w):
    return 1.0 / (1.0 + math.exp(-dV / w))

def dxi_dV(dV, w):
    xi = xi_eq(dV, w)
    return xi * (1 - xi) / w

# dV grid in mV, convert to V for the formula, report derivative in 1/V
dV_mV = list(range(-100, 101, 10))

results = {}
for T in temps:
    w = w_of_T(T)          # volts
    w_mV = w * 1000.0
    xi_pts = [(dv, round(xi_eq(dv / 1000.0, w), 4)) for dv in dV_mV]
    slope_pts = [(dv, round(dxi_dV(dv / 1000.0, w), 4)) for dv in dV_mV]  # 1/V
    central_slope = 1.0 / (4.0 * w)  # 1/V
    results[T] = dict(w_V=w, w_mV=w_mV, xi_pts=xi_pts, slope_pts=slope_pts,
                       central_slope=central_slope)

if __name__ == "__main__":
    for T in temps:
        r = results[T]
        print(f"T={T} K: w = {r['w_V']:.6f} V = {r['w_mV']:.3f} mV, "
              f"central slope 1/(4w) = {r['central_slope']:.4f} 1/V")
    print()
    for T in temps:
        print(f"--- T={T} K xi_eq(dV[mV]) ---")
        print(results[T]["xi_pts"])
    print()
    for T in temps:
        print(f"--- T={T} K dxi/dV [1/V] (dV[mV]) ---")
        print(results[T]["slope_pts"])
