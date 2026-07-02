# V1013_P21_fig_F1_sm_mu.py — Part 0 fig:sm-mu source data
# Evaluates the ACTUAL lattice-gas chemical potential [eq:sm-mu]:
#   (mu(theta) - mu0)/RT = ln[theta/(1-theta)] + a(1-2 theta),  a = Omega/RT
# Family a in {0,2,4}; van der Waals loop for a=4 with spinodal extrema
#   theta_s = (1 +- sqrt(1-2/a))/2 -> 0.1464/0.8536 (a=4), y = -+1.066... wait sign:
#   y(theta_s-) = +1.0657, y(theta_s+) = -1.0657 (checked against fig:hysloop 1.066).
# Outputs: TikZ coordinate blocks (stdout) + verification PNG.
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def mu(th, a):
    return np.log(th/(1-th)) + a*(1-2*th)

def dmu(th, a):  # d(mu/RT)/dtheta
    return 1.0/(th*(1-th)) - 2.0*a

def tikz(xs, ys, ndig=4):
    pts = " ".join(f"({x:.{ndig}g},{y:.{ndig}g})" for x, y in zip(xs, ys))
    return "coordinates {" + pts + "}"

th = np.unique(np.concatenate([
    np.linspace(0.02, 0.10, 6), np.linspace(0.13, 0.87, 20),
    np.linspace(0.90, 0.98, 6)]))
print("=== (mu-mu0)/RT vs theta, a=Omega/RT ===")
for a in (0.0, 2.0, 4.0):
    print(f"% a=Omega/RT={a}")
    print(tikz(th, mu(th, a)))

a = 4.0
u = np.sqrt(1 - 2/a)
ts_m, ts_p = 0.5*(1-u), 0.5*(1+u)
ym, yp = mu(ts_m, a), mu(ts_p, a)
print(f"% extrema a=4: theta_s-={ts_m:.4f} y={ym:.4f}; theta_s+={ts_p:.4f} y={yp:.4f}")

# checks
assert abs(ts_m-0.146447) < 1e-5 and abs(ts_p-0.853553) < 1e-5
assert abs(dmu(ts_m, a)) < 1e-9 and abs(dmu(ts_p, a)) < 1e-9      # extrema = spinodal
assert abs(ym-1.0657) < 5e-4 and abs(yp+1.0657) < 5e-4            # matches fig:hysloop 1.066
assert abs(mu(0.5, a)) < 1e-12                                    # odd symmetry about theta=1/2
assert abs(mu(0.3, a) + mu(0.7, a)) < 1e-12
assert dmu(0.5, 2.0) < 1e-12 and dmu(0.5, 1.999) > 0              # monotone up to a=2
# gap closed form cross-check: max-min = (2/RT-units)[a*u - 2 artanh u]
gap = 2*(a*u - 2*np.arctanh(u))
assert abs((ym - yp) - gap) < 1e-9

fig, ax = plt.subplots(figsize=(5.4, 3.6))
thf = np.linspace(0.005, 0.995, 500)
for a_ in (0.0, 2.0, 4.0):
    ax.plot(thf, mu(thf, a_), label=f"Omega/RT={a_:g}")
ax.plot([ts_m, ts_p], [ym, yp], "ko", ms=4)
ax.annotate("theta_s-", (ts_m, ym), textcoords="offset points", xytext=(6, 4))
ax.annotate("theta_s+", (ts_p, yp), textcoords="offset points", xytext=(-40, -12))
ax.set_ylim(-4, 4)
ax.set_xlabel("theta"); ax.set_ylabel("(mu-mu0)/RT")
ax.legend(fontsize=8); ax.set_title("lattice-gas mu(theta) [eq:sm-mu]")
fig.tight_layout()
fig.savefig(r"D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_F1_sm_mu.png", dpi=150)
print("PNG saved. All asserts passed.")
