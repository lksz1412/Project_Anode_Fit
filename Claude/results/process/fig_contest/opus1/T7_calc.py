# T7 fig:reversal — causal tail direction, discharge vs charge (grid reversal).
# Equilibrium bell (direction-invariant):  b(V) = xi_eq(1-xi_eq)/w.   [eq:eqpeak]
# Peak shape with tail:  p(V) = (xi_eq - xi_lag)/L_V.   [eq:peakshape]
# Low-pass recurrence:  xi_lag[i] = rho*xi_lag[i-1] + (1-rho)*xi_eq[i],  rho = exp(-Delta/L_V).  [eq:lowpass]
# Charge (sigma_d=-1): reverse grid, low-pass, reverse back.   [eq:reversal]
# Units: center U=0, w=1 (potential in units of w); L_V = 1.5 w; grid step Delta = 0.05 w.
import math

w   = 1.0
LV  = 1.5
U   = 0.0
Vmin, Vmax, dV = -6.0, 8.0, 0.05
N = int(round((Vmax - Vmin) / dV)) + 1
Vs = [Vmin + dV * i for i in range(N)]
rho = math.exp(-dV / LV)

def logistic(z):
    return 1.0 / (1.0 + math.exp(-z))

def lowpass(seq):
    out = [0.0] * len(seq)
    out[0] = seq[0]
    for i in range(1, len(seq)):
        out[i] = rho * out[i - 1] + (1.0 - rho) * seq[i]
    return out

# discharge sigma_d=+1
xe_d = [logistic((V - U) / w) for V in Vs]
lag_d = lowpass(xe_d)
p_d = [(xe_d[i] - lag_d[i]) / LV for i in range(N)]

# charge sigma_d=-1: xi_eq mirrored, reversal filtering
xe_c = [logistic(-(V - U) / w) for V in Vs]
lag_c = list(reversed(lowpass(list(reversed(xe_c)))))
p_c = [(xe_c[i] - lag_c[i]) / LV for i in range(N)]

# equilibrium bell (same for both)
bell = [xe_d[i] * (1.0 - xe_d[i]) / w for i in range(N)]   # discharge orientation
bell_c = [xe_c[i] * (1.0 - xe_c[i]) / w for i in range(N)]  # identical shape mirrored

# common display scale so peaks are ~2.2 tikz units tall
disp = 2.2 / max(max(bell), max(p_d), max(p_c))
print(f"rho = {rho:.4f}   display scale = {disp:.4f}")
print(f"max bell={max(bell):.4f}  max p_d={max(p_d):.4f}  max p_c={max(p_c):.4f}")
print(f"argmax p_d at V={Vs[p_d.index(max(p_d))]:.2f}  (discharge tail -> higher V)")
print(f"argmax p_c at V={Vs[p_c.index(max(p_c))]:.2f}  (charge tail -> lower V)")
print()

def emit(name, seq, step=4):
    pts = " ".join(f"({Vs[i]:.2f},{seq[i]*disp:.4f})" for i in range(0, N, step))
    print(f"{name}:")
    print(pts)
    print()

emit("DISCHARGE bell (dotted)", bell)
emit("DISCHARGE peak+tail (solid)", p_d)
emit("CHARGE bell (dotted)", bell_c)
emit("CHARGE peak+tail (solid)", p_c)
