# T8 fig:widthbudget — the two-phase broadening budget in three narrated stages.
# eq:widthbudget : sigma_sym^2 = sigma_int^2 + sigma_eta^2   (variance-additive, (2) intrinsic (X) (3) ensemble)
#                  ell_tail = L_V,j  (one-sided asymmetric tail length, separate axis, propto |I|)
# Stage (0): equilibrium delta at V=U_j (Maxwell potential).
# Stage (1): + (2) intrinsic logistic-derivative bell, scale w=1:      b1(z) = xi(1-xi),  xi=1/(1+e^-z)
# Stage (2): + (3) ensemble convolution -> same function family, effective scale 1.6 w
#            (sigma_eta = 1.25 sigma_int  ->  sigma_sym/sigma_int = sqrt(1+1.25^2) = 1.6003 =~ 1.6):
#            b2(z) = xi_s(1-xi_s)/1.6,  xi_s = 1/(1+e^{-z/1.6})
# Stage (3): + (1) one-sided exponential tail (L_V = 1.5 w), causal convolution of b2 with
#            k(z)=(1/L) e^{-z/L} Theta(z), evaluated by direct numerical (trapezoid) integration.
import math

def b_intrinsic(z, w=1.0):
    xi = 1.0 / (1.0 + math.exp(-z / w))
    return xi * (1 - xi) / w

sigma_int_over_w = math.pi / math.sqrt(3.0)   # sigma of the logistic-derivative distribution, scale w=1
sigma_eta_over_int = 1.25
scale_ratio = math.sqrt(1 + sigma_eta_over_int ** 2)   # sigma_sym/sigma_int
w2 = scale_ratio   # effective scale of stage-2 bell (w=1 baseline for stage 1)

def b_broadened(z, w=w2):
    xi = 1.0 / (1.0 + math.exp(-z / w))
    return xi * (1 - xi) / w

L_tail = 1.5   # L_V in units of w (baseline intrinsic scale)

def kernel(z, L=L_tail):
    return (1.0 / L) * math.exp(-z / L) if z >= 0 else 0.0

def b_tailed(z, L=L_tail, dz=0.05, zmin=-14.0, zmax=14.0):
    # causal convolution: integral_{-inf}^{z} b_broadened(z') * (1/L) e^{-(z-z')/L} dz'
    n = int(round((z - zmin) / dz))
    total = 0.0
    zp = zmin
    prev = b_broadened(zp) * kernel(z - zp, L)
    for i in range(1, n + 1):
        zp2 = zmin + i * dz
        cur = b_broadened(zp2) * kernel(z - zp2, L)
        total += 0.5 * (prev + cur) * dz
        prev = cur
    return total

zs = [round(-6.0 + 0.5 * i, 2) for i in range(int((10.0 - (-6.0)) / 0.5) + 1)]  # -6..10

pts_b1 = [(z, round(b_intrinsic(z), 4)) for z in zs]
pts_b2 = [(z, round(b_broadened(z), 4)) for z in zs]
pts_b3 = [(z, round(b_tailed(z), 4)) for z in zs]

if __name__ == "__main__":
    print("sigma_int/w =", round(sigma_int_over_w, 4))
    print("scale_ratio sigma_sym/sigma_int (=eff. w2) =", round(scale_ratio, 4))
    print("peak b1(0) =", round(b_intrinsic(0.0), 4), "(expect 0.25)")
    print("peak b2(0) =", round(b_broadened(0.0), 4), "(expect 0.25/1.6003=",
          round(0.25 / w2, 4), ")")
    print("peak b3 max =", round(max(v for _, v in pts_b3), 4),
          "at z=", zs[[v for _, v in pts_b3].index(max(v for _, v in pts_b3))])
    print()
    print("stage-1 (intrinsic, w=1) points:")
    print(pts_b1)
    print()
    print("stage-2 (broadened, w=1.6) points:")
    print(pts_b2)
    print()
    print("stage-3 (broadened + one-sided tail L=1.5) points:")
    print(pts_b3)
