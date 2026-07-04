import math


cases = [
    ("A/RT=-ln2", 0.5),
    ("A/RT=0", 1.0),
    ("A/RT=ln2", 2.0),
    ("A/RT=ln3", 3.0),
]

for label, ratio in cases:
    xi = ratio / (ratio + 1.0)
    flux = ratio * (1.0 - xi)
    print(f"{label}: r+/r-={ratio:.4f}, xi_eq={xi:.4f}, flux={flux:.4f}")
    print(f"forward: (0,{ratio:.4f}) (1,0)")
    print("reverse: (0,0) (1,1)")
