# V1013_P21_fig_F1_sm_occ.py — Part 0 fig:sm-occ + fig:sm-logistic-V source data
# Evaluates the ACTUAL equations (no fabricated shapes):
#   (A) theta(x; tau) = 1/(1+exp(x/tau)),  x=(eps0-mu)/kB*T0, tau=T/T0   [eq:sm-occ]
#   (B) xi_eq(V;T)   = 1/(1+exp(-F(V-U)/(R T))), U=0.085 V               [eq:sm-xieq]
# Outputs: TikZ coordinate blocks (stdout) + verification PNGs.
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = 8.314462618      # J/(mol K)
F = 96485.33212      # C/mol
U = 0.085            # V (stage 2->1 initial value, codebox N2)

def tikz(xs, ys, ndig=4):
    pts = " ".join(f"({x:.{ndig}g},{y:.{ndig}g})" for x, y in zip(xs, ys))
    return "coordinates {" + pts + "}"

# ---------- (A) dimensionless single-site occupancy ----------
x = np.linspace(-6, 6, 25)
print("=== (A) theta vs x=(eps0-mu)/kBT0 ===")
for tau in (0.5, 1.0, 2.0):
    th = 1.0/(1.0+np.exp(x/tau))
    print(f"% tau=T/T0={tau}")
    print(tikz(x, th))
# checks
assert abs(1.0/(1.0+np.exp(0.0)) - 0.5) < 1e-12          # theta(x=0)=1/2 all T
assert 1.0/(1.0+np.exp(6/0.5)) < 1e-5                    # beta->inf: step
assert abs(1.0/(1.0+np.exp(6/1e9)) - 0.5) < 1e-6         # beta->0: 1/2

# ---------- (B) electrochemical dress: xi_eq(V;T), theta_eq(V;298K) ----------
V = np.linspace(0.0, 0.20, 26)
print("=== (B) xi_eq vs V (U=0.085 V) ===")
for T in (268.15, 298.15, 328.15):
    xi = 1.0/(1.0+np.exp(-F*(V-U)/(R*T)))
    w = R*T/F
    print(f"% T={T} K, w=RT/F={w*1e3:.2f} mV")
    print(tikz(V, xi))
T0 = 298.15
th298 = 1.0 - 1.0/(1.0+np.exp(-F*(V-U)/(R*T0)))
print("% theta_eq = 1 - xi_eq at T=298.15 K")
print(tikz(V, th298))
# checks
xiU = 1.0/(1.0+np.exp(-F*(U-U)/(R*T0)))
assert abs(xiU-0.5) < 1e-12                              # xi_eq(U)=1/2
assert abs((R*T0/F)*1e3 - 25.69) < 0.02                  # w(298K)=25.7 mV
# slope at center: dxi/dV|_U = F/(4RT)  (bell identity xi(1-xi)=1/4)
h = 1e-6
num = (1/(1+np.exp(-F*(U+h-U)/(R*T0))) - 1/(1+np.exp(-F*(U-h-U)/(R*T0))))/(2*h)
assert abs(num - F/(4*R*T0)) < 1e-3

# ---------- verification PNGs ----------
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
for tau in (0.5, 1.0, 2.0):
    ax[0].plot(x, 1/(1+np.exp(x/tau)), label=f"T/T0={tau}")
ax[0].set_xlabel("(eps0 - mu)/kB T0"); ax[0].set_ylabel("theta")
ax[0].legend(); ax[0].set_title("single-site occupancy [eq:sm-occ]")
for T in (268.15, 298.15, 328.15):
    ax[1].plot(V, 1/(1+np.exp(-F*(V-U)/(R*T))), label=f"T={T:.0f} K")
ax[1].plot(V, th298, "--", label="theta=1-xi (298 K)")
ax[1].axvline(U, color="k", lw=0.5, ls=":")
ax[1].set_xlabel("V [V]"); ax[1].set_ylabel("xi_eq")
ax[1].legend(fontsize=7); ax[1].set_title("xi_eq(V), U=0.085 V [eq:sm-xieq]")
fig.tight_layout()
fig.savefig(r"D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_F1_sm_occ.png", dpi=150)
print("PNG saved. All asserts passed.")
