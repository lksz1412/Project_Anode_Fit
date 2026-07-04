"""Coordinate source for T5_flux.tex."""

cases = [
    ("A<0", 1.0, 2.0),
    ("A=0", 1.5, 1.5),
    ("A>0", 2.0, 1.0),
]

print("T5 flux intersections: r_plus(1-xi) = r_minus xi")
for name, rp, rm in cases:
    xi = rp / (rp + rm)
    flux = rp * (1.0 - xi)
    print(f"{name}: r_plus={rp:.1f}, r_minus={rm:.1f}, xi_eq={xi:.4f}, flux={flux:.4f}")
