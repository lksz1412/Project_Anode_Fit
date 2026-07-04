#!/usr/bin/env python3
# T6 fig:logistic  --  equilibrium fill xi_eq (logistic) and its derivative bell,
# with the temperature dependence of the width  w = n RT/F  (n=1) at T = 268/298/328 K.
#   xi_eq(V) = 1/(1+exp[-(V-U)/w])                         (eq:xieq, sigma_d=+1)
#   dxi/dV  = xi(1-xi)/w,   peak height = 1/(4w) at V=U    (eq:belliden)
#   center tangent slope of xi_eq at V=U is exactly 1/(4w) -> geometric meaning of w.
#   FWHM of bell = 2 ln(3+2 sqrt2) w = 3.5255 w.
import math

R, F = 8.314462618, 96485.33212
n = 1.0
temps = [268.0, 298.0, 328.0]
kFW = 2.0*math.log(3.0+2.0*math.sqrt(2.0))   # 3.52549...

print(f"# FWHM factor 2 ln(3+2 sqrt2) = {kFW:.5f}")
for T in temps:
    w = n*R*T/F
    peak = 1.0/(4.0*w)
    fwhm = kFW*w
    print(f"T={T:.0f}K : w={w*1e3:.3f} mV   peak dxi/dV=1/(4w)={peak:.3f} /V   "
          f"FWHM={fwhm*1e3:.2f} mV   half-max at (V-U)=+-{0.5*fwhm*1e3:.2f} mV")

# ---- emit curves in physical units: x = (V-U) in mV, over -85..+85 mV ----
xs_mV = list(range(-85, 86, 5))
def sig(z): return 1.0/(1.0+math.exp(-z))

for T in temps:
    w = n*R*T/F                       # V
    # xi_eq (dimensionless 0..1)
    scurve = [(x, sig((x*1e-3)/w)) for x in xs_mV]
    # bell dxi/dV in 1/V
    bell   = [(x, sig((x*1e-3)/w)*(1-sig((x*1e-3)/w))/w) for x in xs_mV]
    print(f"\n% T={T:.0f}K  xi_eq (x in mV, y in 0..1):")
    print(" ".join(f"({x},{y:.4f})" for x,y in scurve))
    print(f"% T={T:.0f}K  bell dxi/dV (x in mV, y in 1/V):")
    print(" ".join(f"({x},{y:.4f})" for x,y in bell))

# center tangent for 298K: y = 0.5 + (1/(4w))*(V-U); give two endpoints in mV / xi-units
w298 = n*R*298.0/F
sl = 1.0/(4.0*w298)                    # per Volt
for dx in (-40, 40):
    print(f"# 298K tangent point: (V-U)={dx} mV -> xi={0.5+sl*dx*1e-3:.4f}")
