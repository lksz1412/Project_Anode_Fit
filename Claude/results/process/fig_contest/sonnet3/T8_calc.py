"""T8 fig:widthbudget -- coordinate generator, 4-panel narration.

Reproduces the chapter's own worked example (l.1560-1566): w_j=1 (normalized),
sigma_eta = 1.25 * sigma_int, exponential tail L_V = 1.5 w_j -- but instead of
citing the chapter's "same family -> effective scale 1.6 w_j" shortcut for the
(2)(x)(3) step, this script does the ACTUAL discrete convolutions:

  stage 1 (delta):            just a vertical arrow (no curve)
  stage 2 (intrinsic (2)):    bell_int(x) = xi(1-xi)/w   [[= logistic density, w=1]]
  stage 3 ((2)(x)(3)):        bell_int numerically convolved with a Gaussian of
                              sigma_eta = 1.25*sigma_int (discrete sum, dx=0.04)
  stage 4 (+(1) tail):        stage-3 curve passed through the SAME causal
                              exponential low-pass recursion as eq:lowpass
                              (rho=exp(-dx/L_V)), L_V = 1.5 w_j -- a one-sided
                              exponential convolution is exactly a first-order
                              IIR filter, so this is the same math as T7, not
                              a separate ad hoc smear.

The chapter's closed-form shortcut (effective scale 1.6 w_j logistic bell) is
also evaluated here and reported alongside the true convolution, so the
figure can show both and the caption can note how close the shortcut is.
"""

import math

w = 1.0
sigma_int = math.pi * w / math.sqrt(3)
eta_ratio = 1.25
sigma_eta = eta_ratio * sigma_int
sigma_sym = math.sqrt(sigma_int**2 + sigma_eta**2)
scale_ratio = sigma_sym / sigma_int
print(f"sigma_int = {sigma_int:.4f}, sigma_eta = {sigma_eta:.4f}, "
      f"sigma_sym = {sigma_sym:.4f} (ratio {scale_ratio:.4f}, chapter quotes 1.6)")

dx = 0.04
xs = [round(-14 + i * dx, 4) for i in range(int(28 / dx) + 1)]


def bell_int(x):
    xi = 1.0 / (1.0 + math.exp(-x / w))
    return xi * (1 - xi) / w


def gaussian(x, sigma):
    return math.exp(-x * x / (2 * sigma * sigma)) / (sigma * math.sqrt(2 * math.pi))


stage1 = [bell_int(x) for x in xs]
area1 = sum(stage1) * dx
print(f"stage 2 (intrinsic bell) area = {area1:.4f} (expect ~1)")

# ---- stage 3: TRUE numerical convolution with Gaussian(sigma_eta) ----
# direct O(N^2) discrete convolution; xs is short enough (~700 pts) to be fast
kernel_half = int(4 * sigma_eta / dx)
kernel_xs = [k * dx for k in range(-kernel_half, kernel_half + 1)]
kernel = [gaussian(k, sigma_eta) for k in kernel_xs]
ksum = sum(kernel) * dx
kernel = [k / ksum for k in kernel]  # renormalize discretized kernel to unit area

stage2 = [0.0] * len(xs)
for i in range(len(xs)):
    acc = 0.0
    for j, k_val in enumerate(kernel):
        src = i - (j - kernel_half)
        if 0 <= src < len(xs):
            acc += k_val * stage1[src]
    stage2[i] = acc * dx
area2 = sum(stage2) * dx
peak2 = max(stage2)
print(f"stage 3 ((2)(x)(3) true convolution) area = {area2:.4f} (expect ~1), peak = {peak2:.4f}")

# closed-form shortcut comparison: logistic bell of scale sigma_sym*sqrt(3)/pi = 1.6*w
w_eff = scale_ratio * w
peak_shortcut = 0.25 / w_eff
print(f"chapter's shortcut: logistic bell w_eff={w_eff:.4f} -> peak {peak_shortcut:.4f} "
      f"(true convolution peak {peak2:.4f}, relative diff {(peak2-peak_shortcut)/peak_shortcut*100:+.2f}%)")

# ---- stage 4: causal exponential tail, L_V = 1.5 w, same recursion as eq:lowpass/T7 ----
L_V = 1.5 * w
rho = math.exp(-dx / L_V)
stage3 = [stage2[0]]
for i in range(1, len(xs)):
    stage3.append(rho * stage3[-1] + (1 - rho) * stage2[i])
area3 = sum(stage3) * dx
peak3 = max(stage3)
peak3_x = xs[stage3.index(peak3)]
print(f"stage 4 (+1 tail) area = {area3:.4f} (mass-conserving low-pass keeps area ~ same), "
      f"peak = {peak3:.4f} at x={peak3_x:.2f} (shifted from 0)")


def subsample(values, lo=-6.5, hi=10.5, step_pts=6):
    out = []
    for i in range(0, len(xs), step_pts):
        if lo <= xs[i] <= hi:
            out.append((xs[i], values[i]))
    return out


for name, arr in [("stage2_intrinsic", stage1), ("stage3_broadened", stage2), ("stage4_tailed", stage3)]:
    pts = subsample(arr)
    print(f"\n== {name} ({len(pts)} points) ==")
    print(" ".join(f"({x:.2f},{y:.4f})" for x, y in pts))
