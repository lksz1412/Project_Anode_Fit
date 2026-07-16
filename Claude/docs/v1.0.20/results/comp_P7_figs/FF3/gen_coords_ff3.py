# -*- coding: utf-8 -*-
"""FF3 그림 좌표 생성기 — 본문 식 그대로의 수치 평가 + 물리 게이트 검산.
   출력: 각 그림의 plot coordinates 문자열 (stdout) — .tex 조각에 하드코딩용.
"""
import math

R = 8.314462618          # J/(mol K)
F = 96485.33212          # C/mol
h = 6.62607015e-34       # J s
kB = 1.380649e-23        # J/K

def fmt(pairs, nd=4, ndy=4):
    return " ".join(f"({x:.{nd}g},{y:.{ndy}g})" for x, y in pairs)

# ------------------------------------------------------------------
# 공통: 흑연 staging 초기값 (tab:staging) — U_j(T)=(−ΔH+TΔS)/F, w=RT/F (n=1)
# ------------------------------------------------------------------
stag = [  # (이름, dH [J/mol], dS [J/mol K], Q [Q_cell])
    ("4to3",  -11700.0,  29.0, 0.10),
    ("3to2L", -13500.0,   0.0, 0.12),
    ("2Lto2", -13100.0,  -5.0, 0.25),
    ("2to1",  -13000.0, -16.0, 0.50),
]
Qtot = sum(s[3] for s in stag)  # 0.97

def U_j(dH, dS, T):
    return (-dH + T * dS) / F

def xi_eq(U, Uj, w):
    z = (U - Uj) / w
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)

# ==================================================================
# F1. dU_oc/dT(x̄) 프로파일 — eq:implicit 풀이 + eq:weighted/eq:complete
# ==================================================================
def solve_Uoc(xbar, T):
    """sum_j Q_j xi_j(U) = Qtot*xbar 를 U에 대해 이분법."""
    w = R * T / F
    Us = [U_j(dH, dS, T) for _, dH, dS, _ in stag]
    target = Qtot * xbar
    lo, hi = -0.2, 0.6
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        s = sum(Q * xi_eq(mid, Uj, w) for (_, _, _, Q), Uj in zip(stag, Us))
        if s < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def dUdT_profile(xbar, T=298.15, full=True):
    w = R * T / F
    Us = [U_j(dH, dS, T) for _, dH, dS, _ in stag]
    Uoc = solve_Uoc(xbar, T)
    num = den = 0.0
    for (name, dH, dS, Q), Uj in zip(stag, Us):
        xi = xi_eq(Uoc, Uj, w)
        g = xi * (1 - xi) / w
        term = dS / F
        if full:
            term += (R / F) * math.log(xi / (1 - xi))
        num += Q * g * term
        den += Q * g
    return num / den * 1e3, Uoc  # mV/K, V

# --- 게이트 1: Ch2 §2.8 계산 예제 / tab:qrev 재현 ---
gate_rows = [(0.10, 43.5, -0.307), (0.25, 74.4, -0.204), (0.50, 109.0, -0.089),
             (0.75, 148.8, +0.044), (0.90, 195.2, +0.218)]
print("== F1 gate (tab:qrev / worked example) ==")
for xb, Uref_mV, dref in gate_rows:
    d, U = dUdT_profile(xb)
    ds, _ = dUdT_profile(xb, full=False)
    print(f" xbar={xb:4.2f}  U_oc={U*1e3:7.2f} mV (ref {Uref_mV})  "
          f"full={d:+.3f} (ref {dref:+.3f})  simple={ds:+.3f} mV/K")
    assert abs(U * 1e3 - Uref_mV) < 0.25, "U_oc gate FAIL"
    assert abs(d - dref) < 0.004, "full-formula gate FAIL"
ds025, _ = dUdT_profile(0.25, full=False)
assert abs(ds025 - (-0.134)) < 0.004, "simple-formula gate FAIL"
print("   gate PASS")

# --- 곡선 좌표 ---
xs = [0.02 + 0.02 * i for i in range(49)]  # 0.02..0.98
full_pts, simp_pts = [], []
for xb in xs:
    d, _ = dUdT_profile(xb)
    ds, _ = dUdT_profile(xb, full=False)
    full_pts.append((xb, d))
    simp_pts.append((xb, ds))
print("\nF1 full:", fmt(full_pts, 3, 4))
print("\nF1 simple:", fmt(simp_pts, 3, 4))

# 계단(오답) 대비: 지배 전이(비중 최대)의 중심값 레벨
def dominant_level(xb, T=298.15):
    w = R * T / F
    Us = [U_j(dH, dS, T) for _, dH, dS, _ in stag]
    Uoc = solve_Uoc(xb, T)
    best, lev = -1, 0.0
    for (name, dH, dS, Q), Uj in zip(stag, Us):
        xi = xi_eq(Uoc, Uj, w)
        g = Q * xi * (1 - xi) / w
        if g > best:
            best, lev = g, dS / F * 1e3
    return lev

# 스위칭 경계 찾기
edges = []
prev = dominant_level(xs[0])
xprev = xs[0]
for xb in [0.02 + 0.005 * i for i in range(1, 193)]:
    cur = dominant_level(xb)
    if cur != prev:
        edges.append((0.5 * (xprev + xb), prev, cur))
        prev = cur
    xprev = xb
print("\nF1 step edges:", [(round(e[0], 3), round(e[1], 3), round(e[2], 3)) for e in edges])
print("F1 levels dS/F [mV/K]:", [round(dS / F * 1e3, 3) for _, _, dS, _ in stag])

# tab:qrev 5점
print("F1 dots:", [(xb, round(dUdT_profile(xb)[0], 3)) for xb, _, _ in gate_rows])

# ==================================================================
# F2. log10 L_V vs dH_a — eq:Lqfull·eq:LV (기본값: chi=0.5, dS_a=0, A=4RT, n=1)
# ==================================================================
print("\n== F2 ==")
def log10_LV(dHa, T, crate=0.1, dVdq=0.30):
    Tstar = crate * h / kB          # Q_cell=1 정규화, c-rate 숫자 그대로 (§10 규약)
    A_over_RT = 4.0                 # A_cap 상한 활성 (n=1)
    pref = dVdq * (Tstar / T) * math.exp(-0.5 * A_over_RT) / (1.0 + math.exp(-A_over_RT))
    return math.log10(pref) + dHa / (R * T * math.log(10.0))

for T in (268.15, 298.15, 328.15):
    p0 = log10_LV(0.0, T)
    slope = 1.0 / (R * T * math.log(10.0)) * 1e3  # per kJ
    wT = R * T / F
    cross = (math.log10(wT) - p0) / slope * 1.0   # kJ/mol
    print(f" T={T}: intercept={p0:.4f}, slope={slope:.5f}/kJ, w={wT*1e3:.2f} mV, "
          f"cross(L_V=w)={cross:.1f} kJ/mol")
# 게이트 2: §10 — 초기값 창(40–48 kJ/mol)에서 L_V 는 w 보다 압도적으로 작아야 하고
#           가시 문턱은 ≈80 kJ/mol 급 (298 K)
lv40 = 10 ** log10_LV(40000.0, 298.15)
cross298 = (math.log10(R * 298.15 / F) - log10_LV(0.0, 298.15)) / (1.0 / (R * 298.15 * math.log(10)))
print(f"  L_V(40 kJ,298K) = {lv40:.3g} V ;  cross298 = {cross298/1000:.1f} kJ/mol")
assert lv40 < 1e-7 and 70e3 < cross298 < 90e3, "F2 gate FAIL"
print("   gate PASS")
for T in (268.15, 298.15, 328.15):
    pts = [(dh, log10_LV(dh * 1e3, T)) for dh in (20, 100)]
    print(f" F2 line T={T}: {fmt(pts, 4, 4)}")
print(" F2 staging dots (298K):",
      [(dh, round(log10_LV(dh * 1e3, 298.15), 3)) for dh in (48, 46, 44, 40)])

# ==================================================================
# F3. 합산 곡선 dQ/dV = C_bg + Σ Q_j ξ(1−ξ)/w — 268.15 / 298.15 / 328.15 K
# ==================================================================
print("\n== F3 ==")
Cbg = 0.05
def total_dQdV(V, T):
    w = R * T / F
    s = Cbg
    for _, dH, dS, Q in stag:
        xi = xi_eq(V, U_j(dH, dS, T), w)
        s += Q * xi * (1 - xi) / w
    return s

for T in (268.15, 328.15):
    Us = [round(U_j(dH, dS, T), 4) for _, dH, dS, _ in stag]
    print(f" T={T}: centers {Us}, w={R*T/F*1e3:.2f} mV")
Vg = [0.030 + 0.005 * i for i in range(51)]  # 0.030..0.280
for T, tag in ((268.15, "cold"), (328.15, "hot")):
    pts = [(v, total_dQdV(v, T)) for v in Vg]
    print(f"F3 total {tag}:", fmt(pts, 3, 4))
# 298K 전이별 기여(배경 미포함)
w298 = R * 298.15 / F
for name, dH, dS, Q in stag:
    Uj = U_j(dH, dS, 298.15)
    pts = [(v, Q * xi_eq(v, Uj, w298) * (1 - xi_eq(v, Uj, w298)) / w298)
           for v in Vg if abs(v - Uj) < 0.075]
    print(f"F3 comp {name} (U={Uj:.4f}):", fmt(pts, 3, 4))
# 중심 이동량 (268→328, 60 K)
print("F3 center shifts 268→328 [mV]:",
      [round((U_j(dH, dS, 328.15) - U_j(dH, dS, 268.15)) * 1e3, 2) for _, dH, dS, _ in stag])

# ==================================================================
# F4. relaxode 재설계 — eq:lag 인과 기억 적분 실수치 (q 좌표)
# ==================================================================
print("\n== F4 ==")
qc, wq, Lq = 1.2, 0.35, 0.4
def xieq_q(q):  return 1.0 / (1.0 + math.exp(-(q - qc) / wq))
def xilag_q(q, n=4000, span=25.0):
    # (1/L)∫_{-span}^{q} ξ_eq(u) e^{-(q-u)/L} du  (사다리꼴)
    a = q - span
    s = 0.0
    du = (q - a) / n
    for i in range(n + 1):
        u = a + i * du
        val = xieq_q(u) * math.exp(-(q - u) / Lq)
        s += val * (0.5 if i in (0, n) else 1.0)
    return s * du / Lq
qs = [0.0 + 0.1 * i for i in range(35)]
eq_pts  = [(q, xieq_q(q)) for q in qs]
lag_pts = [(q, xilag_q(q)) for q in qs]
r_pts   = [(q, e - l) for (q, e), (_, l) in zip(eq_pts, lag_pts)]
rmax = max(r_pts, key=lambda p: p[1])
# 게이트 3: 0 ≤ ξ_lag ≤ ξ_eq ≤ 1, r ≥ 0
assert all(0 <= l <= e <= 1 + 1e-9 for (_, e), (_, l) in zip(eq_pts, lag_pts)), "F4 gate FAIL"
print(f" r max = {rmax[1]:.4f} at q={rmax[0]:.2f}; gate PASS")
print("F4 xieq:", fmt(eq_pts, 3, 4))
print("F4 xilag:", fmt(lag_pts, 3, 4))
print("F4 r:", fmt(r_pts, 3, 4))
q0 = 2.2
kern = [(u, 0.22 * math.exp(-(q0 - u) / Lq)) for u in
        [q0 - 1.6 + 0.08 * i for i in range(21)]]
print("F4 kernel(q0=2.2, 0.22-scale):", fmt(kern, 3, 4))
print("F4 at q=1.5: xieq=", round(xieq_q(1.5), 4), " xilag=", round(xilag_q(1.5), 4))

# ==================================================================
# F5. ΔU^hys 닫힌꼴 (eq:dUhys) — (a) vs Ω @298.15K, (b) vs T (Ω 3값)
# ==================================================================
print("\n== F5 ==")
def dU_hys(Om, T):
    x = 2 * R * T / Om
    if x >= 1:
        return 0.0
    u = math.sqrt(1 - x)
    return 2.0 / F * (Om * u - 2 * R * T * math.atanh(u))
# 게이트 4: fig:hysloop 캡션 — Ω=4RT 에서 2.131 RT/F = 54.8 mV @298.15K
g4 = dU_hys(4 * R * 298.15, 298.15) * 1e3
print(f" gate: dU(4RT,298K) = {g4:.1f} mV (ref 54.8)")
assert abs(g4 - 54.8) < 0.3, "F5 gate FAIL"
print("   gate PASS")
Tc = lambda Om: Om / (2 * R)
twoRT = 2 * R * 298.15
Oms = [twoRT + 1e-6] + [twoRT * (1 + 0.02 * i ** 1.5) for i in range(1, 26)]
Oms = [o for o in Oms if o <= 14000] + [14000]
ptsA = [(o / 1000, dU_hys(o, 298.15) * 1e3) for o in Oms]
print("F5a:", fmt(ptsA, 4, 4))
print("F5a staging dots:", [(o / 1000, round(dU_hys(o * 1.0, 298.15) * 1e3, 1))
                            for o in (6000, 8000, 10000, 13000)])
for Om in (6000, 10000, 13000):
    tc = Tc(Om)
    Ts = [250 + (tc - 250) * (i / 22.0) for i in range(23)]
    pts = [(t, dU_hys(Om, t) * 1e3) for t in Ts]
    print(f"F5b Om={Om} (Tc={tc:.1f}K):", fmt(pts, 4, 4))

# ==================================================================
# F6. Einstein 진동 — eq:Svib-einstein, eq:dUvib 미분 (θ_E=700 K)
# ==================================================================
print("\n== F6 ==")
thE, Tref = 700.0, 298.15
def Svib(T):
    u = thE / T
    return R * (-math.log(1 - math.exp(-u)) + u / (math.exp(u) - 1))
def dSvib_over_F_uV(T):
    return (Svib(T) - Svib(Tref)) / F * 1e6  # μV/K
# 게이트 5: 본문 4수치 −3.74 / 0 / +3.70 / +9.14 μV/K
refs = [(278.15, -3.74), (298.15, 0.0), (318.15, 3.70), (348.15, 9.14)]
for T, ref in refs:
    v = dSvib_over_F_uV(T)
    print(f" T={T}: {v:+.2f} μV/K (ref {ref:+.2f})")
    assert abs(v - ref) < 0.05, "F6 gate FAIL"
print("   gate PASS")
TsA = [60, 80, 100, 130, 160, 200, 240, 280, 320, 360, 400, 460, 520, 600, 700, 800, 900, 1000]
print("F6a Svib/R:", fmt([(t, Svib(t) / R) for t in TsA], 4, 4))
print("F6a classical:", fmt([(t, 1 + math.log(t / thE)) for t in TsA if t >= 260], 4, 4))
TsB = [268.15 + 5 * i for i in range(17)]
print("F6b dSvib/F [uV/K]:", fmt([(t, dSvib_over_F_uV(t)) for t in TsB], 5, 4))

# ==================================================================
# F7. 핵생성 장벽 — ΔG/ΔG* = 3x² − 2x³
# ==================================================================
print("\n== F7 ==")
xs7 = [0.05 * i for i in range(33)]
print("F7 total:", fmt([(x, 3 * x ** 2 - 2 * x ** 3) for x in xs7], 3, 4))
print("F7 surf:",  fmt([(x, 3 * x ** 2) for x in xs7 if 3 * x ** 2 <= 2.3], 3, 4))
print("F7 vol:",   fmt([(x, -2 * x ** 3) for x in xs7 if -2 * x ** 3 >= -2.3], 3, 4))
print("\nALL GATES PASS")
