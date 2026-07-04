# T6 fig:logistic — equilibrium fraction xi_eq (logistic) and its derivative bell, at 3 temperatures.
# xi_eq(V) = 1/(1 + exp(-(V-U)/w)),  w = n R T / F  (n=1).   [eq:xieq, eq:wbase]
# derivative bell: dxi/dV = xi(1-xi)/w, peak 1/(4w) at center; center slope of logistic = 1/(4w).
import math

R = 8.314462618
F = 96485.33212
n = 1.0
Ts = [268.0, 298.0, 328.0]

def w_of(T):
    return n * R * T / F          # Volts

print("widths w = nRT/F:")
for T in Ts:
    print(f"  T={T:.0f} K  w={w_of(T)*1e3:.3f} mV  peak 1/(4w)={1.0/(4*w_of(T)):.3f} /V")
print()

# plot vs (V-U) in mV, range +-100 mV
xmin_mV, xmax_mV = -100.0, 100.0
N = 81
xs_mV = [xmin_mV + (xmax_mV - xmin_mV) * i / (N - 1) for i in range(N)]

for T in Ts:
    w = w_of(T)
    print(f"--- T={T:.0f} K ---")
    # logistic xi_eq (dimensionless 0..1)
    log_coords = []
    der_coords = []
    for xmV in xs_mV:
        dV = xmV / 1000.0
        z = dV / w
        xi = 1.0 / (1.0 + math.exp(-z))
        der = xi * (1.0 - xi) / w      # /V
        log_coords.append(f"({xmV:.1f},{xi:.4f})")
        der_coords.append(f"({xmV:.1f},{der:.4f})")
    print("  LOGISTIC (x_mV, xi):")
    print("   " + " ".join(log_coords))
    print("  DERIV (x_mV, dxi/dV[/V]):")
    print("   " + " ".join(der_coords))
    print()
