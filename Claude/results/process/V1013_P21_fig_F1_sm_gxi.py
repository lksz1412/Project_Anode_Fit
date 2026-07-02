# V1013_P21_fig_F1_sm_gxi.py — Part 0 fig:sm-gxi source data
# Evaluates the ACTUAL regular-solution mixing free energy [eq:sm-gxi]:
#   g_mix(xi)/RT = xi ln xi + (1-xi) ln(1-xi) + a * xi(1-xi),  a = Omega/RT
# Family a in {0,1,2,3}; spinodal marks for a=3: xi_s = (1 +- sqrt(1-2/a))/2.
# Outputs: TikZ coordinate blocks (stdout) + verification PNG.
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def gmix(xi, a):
    return xi*np.log(xi) + (1-xi)*np.log(1-xi) + a*xi*(1-xi)

def gpp(xi, a):  # second derivative / RT
    return 1.0/(xi*(1-xi)) - 2.0*a

def tikz(xs, ys, ndig=4):
    pts = " ".join(f"({x:.{ndig}g},{y:.{ndig}g})" for x, y in zip(xs, ys))
    return "coordinates {" + pts + "}"

# dense at edges (log divergence of slope, value -> 0)
xi = np.unique(np.concatenate([
    np.linspace(0.005, 0.06, 6), np.linspace(0.08, 0.92, 22),
    np.linspace(0.94, 0.995, 6)]))
print("=== g_mix(xi)/RT, a=Omega/RT ===")
for a in (0.0, 1.0, 2.0, 3.0):
    print(f"% a=Omega/RT={a}")
    print(tikz(xi, gmix(xi, a)))

# spinodal points for a=3
a = 3.0
u = np.sqrt(1 - 2/a)
xs_m, xs_p = 0.5*(1-u), 0.5*(1+u)
print(f"% spinodal a=3: xi_s-={xs_m:.4f}, xi_s+={xs_p:.4f}, "
      f"g={gmix(xs_m,a):.4f},{gmix(xs_p,a):.4f}")

# checks
assert abs(xs_m-0.2113) < 5e-4 and abs(xs_p-0.7887) < 5e-4   # matches fig:doublewell
assert abs(gpp(xs_m, a)) < 1e-9 and abs(gpp(xs_p, a)) < 1e-9 # g''=0 at spinodal
assert gpp(0.5, 2.0) < 1e-12 and gpp(0.5, 2.0) > -1e-12      # threshold: g''(1/2)=0 at a=2
assert gpp(0.5, 1.9999) > 0 and gpp(0.5, 2.0001) < 0         # convexity flips at a=2
assert abs(gmix(0.3, a) - gmix(0.7, a)) < 1e-12              # xi <-> 1-xi symmetry
# curve values at xi=1/2: -ln2 + a/4
for a_ in (0, 1, 2, 3):
    assert abs(gmix(0.5, a_) - (-np.log(2) + a_/4)) < 1e-12

fig, ax = plt.subplots(figsize=(5.4, 3.6))
xif = np.linspace(0.001, 0.999, 400)
for a_ in (0.0, 1.0, 2.0, 3.0):
    ax.plot(xif, gmix(xif, a_), label=f"Omega/RT={a_:g}")
ax.plot([xs_m, xs_p], [gmix(xs_m, 3), gmix(xs_p, 3)], "ko", ms=4)
ax.annotate("xi_s-", (xs_m, gmix(xs_m, 3)), textcoords="offset points", xytext=(-18, 6))
ax.annotate("xi_s+", (xs_p, gmix(xs_p, 3)), textcoords="offset points", xytext=(6, 6))
ax.set_xlabel("xi"); ax.set_ylabel("g_mix/RT")
ax.legend(fontsize=8); ax.set_title("regular solution g_mix(xi)/RT [eq:sm-gxi]")
fig.tight_layout()
fig.savefig(r"D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_F1_sm_gxi.png", dpi=150)
print("PNG saved. All asserts passed.")
