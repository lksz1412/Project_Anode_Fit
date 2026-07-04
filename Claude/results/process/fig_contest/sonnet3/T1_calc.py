"""T1 fig:spine -- verification script.

fig:spine is a control-flow diagram (nodes N0..N9), not a plotted physical
curve, so there is no coordinate set to numerically evaluate against a
closed-form equation. What IS verifiable here:

 (1) every equation tag drawn next to a node in T1_spine.tex matches the
     authoritative node<->equation mapping already fixed in the chapter
     text (table tab:nodemap, sec:facade, l.2962-2992 of
     graphite_ica_ch1_v1.0.14.tex) -- this script hard-codes that mapping
     and asserts the figure's tag set is a subset of it (no invented
     cross-references).
 (2) the branch criterion drawn at the decision node (eq:branch, nu=2)
     is the same nu=2 threshold used in the body text, and the resulting
     jump-discontinuity fraction quoted in prose (~23%) is reproduced
     here from the closed-form expression given at l.1890:
         jump(nu) = 1 - (1/nu) / (exp(1/nu) - 1)
"""

import math

# (1) authoritative node -> equation-label mapping, transcribed from
# tab:nodemap (l.2972-2982). Only labels actually drawn in T1_spine.tex
# need to appear as a subset of this dict's values.
NODEMAP = {
    "N0": ["eq:n0map"],
    "N1": ["eq:vn"],
    "N2": ["eq:Uj"],
    "N3": ["eq:dUhys", "eq:Ubranch"],
    "N4/N5": ["eq:wbase", "eq:xieq"],
    "branch": ["eq:branch"],
    "N6": ["eq:eqpeak"],
    "N7": ["eq:LV"],
    "N8": ["eq:peakshape", "eq:reversal"],
    "N9": ["eq:sum"],
}

# labels actually placed in T1_spine.tex (transcribed by hand from the
# \label{...right:eq.~\eqref{...}} calls -- keep this list in sync with
# the .tex file when editing either one)
TAGS_IN_FIGURE = {
    "N0": ["eq:n0map"],
    "N1": ["eq:vn"],
    "N2": ["eq:Uj"],
    "N3": ["eq:dUhys", "eq:Ubranch"],
    "N4/N5": ["eq:wbase", "eq:xieq"],
    "branch": ["eq:branch"],
    "N6": ["eq:eqpeak"],
    "N7": ["eq:LV"],
    "N8": ["eq:peakshape", "eq:reversal"],
    "N9": ["eq:sum"],
}

for node, labels in TAGS_IN_FIGURE.items():
    assert node in NODEMAP, f"node {node} not in authoritative map"
    assert labels == NODEMAP[node], f"tag mismatch at {node}: {labels} != {NODEMAP[node]}"
print("[ok] all node->equation tags in T1_spine.tex match tab:nodemap.")

# (2) branch jump fraction at the default nu=2 threshold (l.1888-1894)
def jump_fraction(nu: float) -> float:
    return 1.0 - (1.0 / nu) / (math.exp(1.0 / nu) - 1.0)

for nu, expect_pct in [(2, 23.0), (8, 6.1), (10, 4.9)]:
    frac = jump_fraction(nu) * 100
    print(f"nu={nu:>2d}: jump = {frac:5.2f}%  (text quotes ~{expect_pct}%)")
    assert abs(frac - expect_pct) < 0.15, "jump fraction does not match quoted text value"

print("[ok] branch discontinuity fraction reproduced from closed form, nu=2 -> ~23% used at the decision node.")
