#!/usr/bin/env python3
# FF2 figure coordinate computation — exact model-equation evaluation
import math

R = 8.314462618
F = 96485.33212
T = 298.15
w = R*T/F  # V

def logi(z):
    if z >= 0:
        return 1.0/(1.0+math.exp(-z))
    e = math.exp(z)
    return e/(1.0+e)

# ============================================================
# FF2-1: dU_oc/dT(xbar) complete vs simple + Qrev/I  (ch2 synthesis)
# ============================================================
dH = [-11700.0, -13500.0, -13100.0, -13000.0]
dS = [29.0, 0.0, -5.0, -16.0]
Q  = [0.10, 0.12, 0.25, 0.50]
Qtot = sum(Q)
U = [(-dH[j] + T*dS[j])/F for j in range(4)]
print("U_j [V]:", ["%.6f" % u for u in U])

def xi_all(V):
    return [logi((V-U[j])/w) for j in range(4)]

def xbar_of_V(V):
    return sum(Q[j]*x for j, x in enumerate(xi_all(V)))/Qtot

def V_of_xbar(xb, lo=-0.1, hi=0.5):
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if xbar_of_V(mid) < xb: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)

def dUdT(xb, complete=True):
    V = V_of_xbar(xb)
    xs = xi_all(V)
    num = 0.0; den = 0.0
    for j in range(4):
        g = xs[j]*(1-xs[j])/w
        term = dS[j]/F
        if complete:
            z = (V-U[j])/w   # = ln[xi/(1-xi)]
            term += (R/F)*z
        num += Q[j]*g*term
        den += Q[j]*g
    return num/den, V

# --- validation against worked example / tab:qrev ---
print("\n-- validation (tab:qrev / worked example) --")
for xb in [0.10, 0.25, 0.50, 0.75, 0.90]:
    c, V = dUdT(xb, True)
    s, _ = dUdT(xb, False)
    print(f"xbar={xb:.2f}: U_oc={V*1e3:7.1f} mV  complete={c*1e3:+.3f} mV/K  simple={s*1e3:+.3f} mV/K  Qrev/I={-T*c*1e3:+.1f} mV")

# --- curve coordinates ---
print("\n-- FF2-1 curve (xbar, complete[mV/K]) --")
xs_grid = [0.05 + 0.9*i/72 for i in range(73)]
cc = []; ss = []; qq = []
for xb in xs_grid:
    c, V = dUdT(xb, True)
    s, _ = dUdT(xb, False)
    cc.append((xb, c*1e3)); ss.append((xb, s*1e3)); qq.append((xb, -T*c*1e3))
def fmt(pairs, xs=1.0, ys=1.0, prec=4, step=1):
    out = " ".join(f"({p[0]*xs:.{prec}f},{p[1]*ys:.{prec}f})" for p in pairs[::step])
    return out
print("COMPLETE:", fmt(cc, prec=3))
print("\nSIMPLE:", fmt(ss, prec=3))
print("\nQREV:", fmt(qq, prec=2))
# sign change location
for i in range(len(cc)-1):
    if cc[i][1] < 0 <= cc[i+1][1]:
        x0, y0 = cc[i]; x1, y1 = cc[i+1]
        xz = x0 - y0*(x1-x0)/(y1-y0)
        print(f"\nsign change of dU/dT at xbar ≈ {xz:.3f}")
print("levels dS0_j/F [mV/K]:", ["%.3f" % (d/F*1e3) for d in dS])

# ============================================================
# FF2-2: hysteresis gap vs Omega/RT  (ch1 sec04/sec13)
# ============================================================
print("\n-- FF2-2 gap curve --")
def gap_mV(orat):  # orat = Omega/RT
    if orat <= 2.0: return 0.0
    u = math.sqrt(1.0 - 2.0/orat)
    return (2*R*T/F)*(orat*u - 2*math.atanh(u))*1e3
pts = []
grid = [2.0 + 0.05*i for i in range(0, 21)] + [3.1+0.1*i for i in range(0, 26)]
for o in grid:
    pts.append((o, gap_mV(o)))
print("GAP:", " ".join(f"({p[0]:.2f},{p[1]:.2f})" for p in pts))
# cubic asymptote (correct, +8RT/3F u^3) and trap (-4RT/3F u^3) near threshold
asy = []; trap = []
for o in [2.0+0.02*i for i in range(0, 61)]:
    if o <= 2.0: u = 0.0
    else: u = math.sqrt(1-2.0/o)
    asy.append((o, (8*R*T/(3*F))*u**3*1e3))
    trap.append((o, -(4*R*T/(3*F))*u**3*1e3))
print("\nASY:", " ".join(f"({p[0]:.2f},{p[1]:.2f})" for p in asy[::3]))
print("\nTRAP:", " ".join(f"({p[0]:.2f},{p[1]:.2f})" for p in trap[::3]))
print("\nvalidation: gap(4RT) =", f"{gap_mV(4.0):.2f} mV (expect 54.8)")
for Om in [6000., 8000., 10000., 13000.]:
    orat = Om/(R*T)
    print(f"  staging Omega={Om:.0f} J/mol -> Omega/RT={orat:.3f}, gap={gap_mV(orat):.2f} mV")

# ============================================================
# FF2-3: peak shape vs L_V family + two-transition overlap (ch1 sec08/09)
# ============================================================
print("\n-- FF2-3 tail family --")
# peak shape P(V;L) = int_0^inf e^-t bell(V - L t) dt ; bell = xi(1-xi) (w=1)
def bell(v, U0=0.0):
    x = logi(v-U0)
    return x*(1-x)
def peakshape(v, L, U0=0.0):
    if L == 0.0: return bell(v, U0)
    # Gauss-Laguerre style: simple composite integration over t in [0, 40]
    n = 4000; tmax = 40.0; h = tmax/n; sacc = 0.0
    for i in range(n+1):
        t = i*h
        wgt = 1.0 if 0 < i < n else 0.5
        sacc += wgt*math.exp(-t)*bell(v - L*t, U0)
    return sacc*h
# family curves
for L in [0.0, 0.75, 1.5, 3.0]:
    xs = [-6 + 16*i/110 for i in range(111)]
    ys = [(v, peakshape(v, L)) for v in xs]
    vmax, pmax = max(ys, key=lambda p: p[1])
    # refine max
    vv = vmax; best = pmax
    for dv in [x/1000 for x in range(-200, 201)]:
        p = peakshape(vmax+dv, L)
        if p > best: best = p; vv = vmax+dv
    print(f"L={L}: max={best:.4f} at V={vv:+.2f}w")
    thin = ys[::4] if L == 0 else ys[::3]
    print(f"P{L}:", " ".join(f"({p[0]:.2f},{p[1]:.4f})" for p in thin))
# two-transition overlap: U=0 and U=6w, equal Q, sum
print("\n-- two-transition sum --")
for L in [0.3, 3.0]:
    xs = [-5 + 19*i/130 for i in range(131)]
    tot = [(v, peakshape(v, L, 0.0) + peakshape(v, L, 6.0)) for v in xs]
    print(f"SUM L={L}:", " ".join(f"({p[0]:.2f},{p[1]:.4f})" for p in tot[::3]))
    # valley depth between peaks
    valley = min([p for p in tot if 0 < p[0] < 6], key=lambda p: p[1])
    pk = max([p for p in tot if -2 < p[0] < 3], key=lambda p: p[1])
    print(f"  L={L}: peak≈{pk[1]:.4f}@{pk[0]:.2f}, valley={valley[1]:.4f}@{valley[0]:.2f}, valley/peak={valley[1]/pk[1]:.3f}")

# ============================================================
# FF2-4: U_1(T) electronic T^2 curvature (ch1 sec15)
# ============================================================
print("\n-- FF2-4 U1(T) --")
kB = 1.380649e-23; eV = 1.602176634e-19
gmax = 13.0; dx = 0.05
a_e = -(math.pi**2/3)*R*(kB/eV)*(gmax/dx)*0.25   # J/(mol K^2), gate center
print("a_e =", f"{a_e:.6f} J/(mol K^2), a_e*298.15 = {a_e*298.15:.2f} J/(mol K) (expect ~ -46)")
dS0 = 80.0  # representative baseline J/(mol K)
Tref = 298.15
Ts = [268.15 + i*2 for i in range(41)]  # 268.15..348.15
lin = [(t, (dS0/F)*(t-Tref)*1e3) for t in Ts]
frozen = [(t, ((dS0 + a_e*Tref)/F)*(t-Tref)*1e3) for t in Ts]
full = [(t, ((dS0/F)*(t-Tref) + (a_e/(2*F))*(t*t-Tref*Tref))*1e3) for t in Ts]
print("LIN:", " ".join(f"({p[0]:.2f},{p[1]:.2f})" for p in lin[::2]))
print("\nFROZEN:", " ".join(f"({p[0]:.2f},{p[1]:.2f})" for p in frozen[::2]))
print("\nFULL:", " ".join(f"({p[0]:.2f},{p[1]:.2f})" for p in full[::2]))
print("\nendpoint slopes (dS0+a_e*T)/F [mV/K]:",
      f"{(dS0+a_e*268.15)/F*1e3:.3f} @268K, {(dS0+a_e*Tref)/F*1e3:.3f} @Tref, {(dS0+a_e*348.15)/F*1e3:.3f} @348K")
print("gap full-lin at 348.15K:", f"{full[-1][1]-lin[-1][1]:.2f} mV")

# ============================================================
# FF2-5: Einstein S_vib(T;thetaE) + dDeltaU_vib/dT (ch2 sec04)
# ============================================================
print("\n-- FF2-5 Einstein --")
def SvibR(u):  # S_vib/R as function of u = thetaE/T
    return -math.log(1-math.exp(-u)) + u/(math.exp(u)-1)
xs = [0.04 + 1.56*i/78 for i in range(79)]  # T/thetaE
sv = [(x, SvibR(1.0/x)) for x in xs]
print("SVIB:", " ".join(f"({p[0]:.3f},{p[1]:.4f})" for p in sv[::2]))
cls = [(x, 1+math.log(x)) for x in xs if 1+math.log(x) > 0]
print("\nCLASSICAL:", " ".join(f"({p[0]:.3f},{p[1]:.4f})" for p in cls[::2]))
print("\noperating point thetaE=700K, T=298.15K: T/thetaE =", f"{298.15/700:.4f}, S/R = {SvibR(700/298.15):.4f}")
# panel (b): dDeltaU_vib/dT = [S_vib(T)-S_vib(Tref)]/F in muV/K for thetaE=500/700/900
print()
for thE in [500.0, 700.0, 900.0]:
    Sref = R*SvibR(thE/Tref)
    pts = [(t, (R*SvibR(thE/t)-Sref)/F*1e6) for t in [258.15+i*2.5 for i in range(42)]]
    print(f"DUV{int(thE)}:", " ".join(f"({p[0]:.2f},{p[1]:.3f})" for p in pts[::2]))
    print()
# validation anchors (text: -3.74 / 0 / +3.70 / +9.14 muV/K at thetaE=700)
Sref = R*SvibR(700/Tref)
for t in [278.15, 298.15, 318.15, 348.15]:
    print(f"  thetaE=700, T={t}: dDU/dT = {(R*SvibR(700/t)-Sref)/F*1e6:+.2f} muV/K")
