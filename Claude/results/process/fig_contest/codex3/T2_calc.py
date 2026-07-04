"""Coordinate source for T2_staging.tex."""

stages = [
    ("stage 4", 0.00, 0.210, [1, 5], "dark"),
    ("stage 3", 1.55, 0.140, [1, 4], "dark"),
    ("stage 2L", 3.10, 0.120, [1, 3, 5], "light"),
    ("stage 2", 4.65, 0.085, [1, 3, 5], "dark"),
    ("stage 1", 6.20, 0.000, [1, 2, 3, 4, 5, 6], "dark"),
]

colw = 0.95
layer_step = 0.60
print("T2 stage columns and nominal transition potentials")
for name, x, u, galleries, shade in stages:
    cx = x + colw / 2
    print(f"{name:>7s}: x0={x:.2f}, center={cx:.2f}, U_init={u:.3f} V, galleries={galleries}, shade={shade}")
