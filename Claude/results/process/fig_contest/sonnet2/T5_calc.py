"""T5 fig:flux — forward/reverse flux lines and their stop-point xi_eq.

Exact evaluation of r+(1-xi) and r-*xi (both are literally straight lines
in xi, so no sampling/interpolation error exists — the tikz \\draw of the
two endpoints IS the exact function). Three affinity cases are overlaid,
each an exact application of detailed balance (eq:db): r+/r- = exp(A/RT).
"""

CASES = {
    "A>0 (2x)":  dict(rp=2.0, rm=1.0),
    "A=0":       dict(rp=1.5, rm=1.5),
    "A<0 (0.5x)": dict(rp=1.0, rm=2.0),
}

if __name__ == "__main__":
    for name, c in CASES.items():
        rp, rm = c["rp"], c["rm"]
        xi_eq = rp / (rp + rm)  # eq:logisticsolve stop point r+(1-xi)=r-*xi
        ratio = rp / rm
        print(f"{name:12s}: r+={rp}, r-={rm}, ratio r+/r-={ratio:.4f}, xi_eq={xi_eq:.4f}")
        # forward line: (0, rp) -> (1, 0); reverse line: (0,0) -> (1, rm)
        print(f"    forward segment: (0,{rp:.2f}) -- (1,0)")
        print(f"    reverse segment: (0,0) -- (1,{rm:.2f})")
    # sanity check against the three canonical fractions used in the caption
    assert abs(CASES["A>0 (2x)"]["rp"] / sum(CASES["A>0 (2x)"].values()) - 2 / 3) < 1e-9
    assert abs(CASES["A=0"]["rp"] / sum(CASES["A=0"].values()) - 1 / 2) < 1e-9
    assert abs(CASES["A<0 (0.5x)"]["rp"] / sum(CASES["A<0 (0.5x)"].values()) - 1 / 3) < 1e-9
    print("\nOK: xi_eq = 2/3, 1/2, 1/3 confirmed exactly for the three overlaid cases.")
