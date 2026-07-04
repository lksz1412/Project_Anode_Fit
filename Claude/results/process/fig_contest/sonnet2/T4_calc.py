"""T4 fig:barrier — Eyring reaction-coordinate landscape, anchored heights.

The document defines the *barrier heights* in closed form (eq:bv) but not a
formula for the free-energy landscape shape between reactant/TS/product —
no such function is claimed anywhere in the chapter (this is the same
situation as fig:doublewell, which is explicitly captioned "정성 곡선").
What IS exact here are the five anchor heights below, which follow
directly from eq:bv with a chosen (dimensionless, plot-only) barrier scale
DeltaG_a=0.9, well depth h0=0.1, affinity A=0.6, chi=1/2:

  reactant well   (x=1) = h0
  product well    (x=5) = h0 - A                    [driven force lowers arrival valley]
  TS (common)     (x=3) = h0 + DeltaG_a - chi*A      [forward barrier = DeltaG_a - chi*A]
                        = (h0-A) + DeltaG_a + (1-chi)*A   [reverse barrier = DeltaG_a + (1-chi)*A]
                          <- both formulas must agree (checked below): they do, because a single
                             transition state is shared by both rate constants in eq:bv.

Baseline points at x=0,6 are a common additive offset with no physical
content (visual continuity to the plot edge only, same convention as the
original figure) and shift together with whichever side's well shifts.

Between anchors, a cubic spline is used purely for a smooth line through
these exact heights (not itself a physical equation) -- explicitly stated
in the caption.
"""
import numpy as np
from scipy.interpolate import CubicSpline

DELTA_GA = 0.9
H0 = 0.1
A = 0.6
CHI = 0.5


def anchors(a, chi, h0=H0, dga=DELTA_GA):
    reactant = h0
    product = h0 - a
    ts_fwd = h0 + dga - chi * a
    ts_rev = product + dga + (1 - chi) * a
    assert abs(ts_fwd - ts_rev) < 1e-12, (ts_fwd, ts_rev)
    baseline_L = h0 + 0.45           # cosmetic, matches original fig scale
    baseline_R = baseline_L - a     # shifts down with the product side
    xs = [0, 1, 3, 5, 6]
    ys = [baseline_L, reactant, ts_fwd, product, baseline_R]
    return xs, ys, dict(reactant=reactant, product=product, ts=ts_fwd,
                         fwd_barrier=ts_fwd - reactant, rev_barrier=ts_fwd - product)


def sample(xs, ys, xq):
    cs = CubicSpline(xs, ys)
    return cs(xq)


if __name__ == "__main__":
    xq = np.arange(0, 6.01, 0.5)

    xs_a, ys_a, info_a = anchors(a=0.0, chi=CHI)
    yq_a = sample(xs_a, ys_a, xq)
    print("panel (a) equilibrium, A=0:")
    print("  anchors:", info_a)
    print("  samples:", [(round(float(x), 2), round(float(y), 4)) for x, y in zip(xq, yq_a)])

    xs_b, ys_b, info_b = anchors(a=A, chi=CHI)
    yq_b = sample(xs_b, ys_b, xq)
    print("\npanel (b) driven, A=0.6, chi=0.5:")
    print("  anchors:", info_b)
    print("  forward barrier (DeltaG_a - chi*A) =", DELTA_GA - CHI * A)
    print("  reverse barrier (DeltaG_a + (1-chi)*A) =", DELTA_GA + (1 - CHI) * A)
    print("  samples:", [(round(float(x), 2), round(float(y), 4)) for x, y in zip(xq, yq_b)])
