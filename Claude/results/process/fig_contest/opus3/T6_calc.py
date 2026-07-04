# -*- coding: utf-8 -*-
# T6 fig:logistic (opus3) — equilibrium progress xi_eq (logistic) and its derivative bell,
# on a PHYSICAL potential axis (V - U_j) in mV, at three temperatures (268/298/328 K).
# eq:xieq :  xi_eq = 1/(1+exp(-(V-U_j)/w)),  w = n RT/F  (n=1, discharge sigma_d=+1).
# derivative (eq:belliden):  dxi/dV = xi(1-xi)/w ;  center slope = 1/(4w);  FWHM = 2 ln(3+2sqrt2) w.
import numpy as np

R = 8.314462618
F = 96485.33212
n = 1.0
temps = [268.0, 298.0, 328.0]

dV = np.linspace(-0.080, 0.080, 33)  # V - U_j in volts

print("T[K]   w[mV]   1/(4w)[1/V]  peak_bell[1/V]  FWHM[mV]")
for T in temps:
    w = n * R * T / F
    slope = 1.0 / (4.0 * w)
    fwhm = 2.0 * np.log(3.0 + 2.0 * np.sqrt(2.0)) * w
    print(f"{T:.0f}  {w*1e3:7.3f}  {slope:10.4f}  {0.25/w:12.4f}  {fwhm*1e3:8.3f}")

for T in temps:
    w = n * R * T / F
    xi = 1.0 / (1.0 + np.exp(-dV / w))
    bell = xi * (1.0 - xi) / w  # 1/V
    print(f"\n% ---- T={T:.0f} K,  w={w*1e3:.3f} mV ----")
    print("% S-curve (x=mV, y=xi_eq):")
    print(" ".join(f"({x*1e3:.1f},{v:.4f})" for x, v in zip(dV, xi)))
    print("% derivative bell (x=mV, y=dxi/dV in 1/V):")
    print(" ".join(f"({x*1e3:.1f},{b:.4f})" for x, b in zip(dV, bell)))
