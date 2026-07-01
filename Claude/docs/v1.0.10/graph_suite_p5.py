# -*- coding: utf-8 -*-
"""P5 그래프 suite — 검증·복원 (V1-V9 핵심 패널). 이론 근거 Ch1·Ch2."""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import importlib.util
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CODE = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.10\Anode_Fit_v1.0.10.py"
OUT = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.10\figs\P5_graph_suite.png"
spec = importlib.util.spec_from_file_location("anodefit", CODE)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
_trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))
F = m.F

gr = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.0)
lco = m.LCOCathodeDQDV(m.LCO_MSMR_LIT, x=0.5, Rn=0.01, Cbg=0.0)
Vg = np.linspace(0.03, 0.34, 1000)
Vc = np.linspace(3.75, 4.15, 1000)

fig, ax = plt.subplots(3, 3, figsize=(16, 13))

# V1 — 흑연+LCO dQ/dV 나란히(방전)
ax[0,0].plot(Vg, gr.dqdv(Vg, 298.15, 0.05, 1.0, +1), 'C0', label="graphite")
axb = ax[0,0].twiny(); axb.plot(Vc, lco.dqdv(Vc, 298.15, 0.05, 1.0, +1), 'C3', label="LCO")
ax[0,0].set_title("V1  graphite + LCO dQ/dV (discharge)"); ax[0,0].set_xlabel("V anode [V]"); axb.set_xlabel("V cathode [V]", color='C3')
ax[0,0].set_ylabel("dQ/dV")

# V2 — round-trip 복원 parity (입력 ΔS_rxn → func_U_j FD → 회귀 ΔŜ = F·(∂U/∂T)_FD)
T1, T2 = 292.15, 298.15
inp, rec = [], []
for tr in m.GRAPHITE_STAGING_LIT + [t for t in m.LCO_MSMR_LIT if not t.get('electronic')]:
    dS = tr['dS_rxn']
    fd = (float(m.func_U_j(T2, tr['dH_rxn'], dS)) - float(m.func_U_j(T1, tr['dH_rxn'], dS))) / (T2 - T1)
    inp.append(dS); rec.append(F * fd)
ax[0,1].plot([-20, 30], [-20, 30], 'k:', lw=0.8)
ax[0,1].scatter(inp, rec, c='C2', zorder=3)
ax[0,1].set_title("V2  round-trip parity  ΔS_in vs ΔŜ=F·(∂U/∂T)_FD"); ax[0,1].set_xlabel("ΔS_rxn input"); ax[0,1].set_ylabel("recovered")
ax[0,1].text(0.05, 0.9, f"max|err|={max(abs(a-b) for a,b in zip(inp,rec)):.2e}", transform=ax[0,1].transAxes, fontsize=9)

# V3 — q_rev(V) 흡·발열 교대
qg = np.asarray(gr.reversible_heat(Vg, 298.15, 1.0))
ax[0,2].plot(Vg, qg, 'C0'); ax[0,2].axhline(0, color='k', lw=0.5, ls=':')
ax[0,2].fill_between(Vg, qg, 0, where=(qg<0), color='C0', alpha=0.2, label="흡열 ΔS>0")
ax[0,2].fill_between(Vg, qg, 0, where=(qg>0), color='C3', alpha=0.2, label="발열 ΔS<0")
ax[0,2].set_title("V3  graphite q_rev = -I·T·∂U/∂T"); ax[0,2].set_xlabel("V [V]"); ax[0,2].set_ylabel("q_rev [W]"); ax[0,2].legend(fontsize=8)

# V4 — ∂U/∂T 완전식(config 포함) vs 단순식(config 제외)
def dUdT_simple(model, V, T=298.15):
    num = np.zeros_like(V); den = np.zeros_like(V); eps=1e-12
    for tr in model.transitions:
        dS = model._effective_dS_rxn(tr, T)
        U = m.func_U_j(T, tr['dH_rxn'], dS); w = model._width(tr, T); n = model._n_factor(tr, T)
        xi = np.asarray(m.func_ksi_eq(T, V, U, n)); g = xi*(1-xi)/w; Qg = tr['Q']*g
        num += Qg*(dS/F); den += Qg
    return np.where(den>0, num/np.maximum(den,eps), 0.0)
full = np.asarray(gr.entropy_coefficient(Vg, 298.15))*1e3
simp = dUdT_simple(gr, Vg)*1e3
ax[1,0].plot(Vg, full, 'C0', label="완전식(+config)"); ax[1,0].plot(Vg, simp, 'C1--', label="단순식(중심만)")
ax[1,0].set_title("V4  ∂U/∂T 완전식 vs 단순식 [mV/K]"); ax[1,0].set_xlabel("V [V]"); ax[1,0].set_ylabel("∂U/∂T [mV/K]"); ax[1,0].legend(fontsize=8)

# V5 — 온도의존 peak 이동
for Tk, c in [(258.15,'C0'), (298.15,'C1'), (318.15,'C3')]:
    ax[1,1].plot(Vg, gr.dqdv(Vg, Tk, 0.2, 1.0, +1), c, label=f"{Tk-273.15:+.0f}°C")
ax[1,1].set_title("V5  온도의존 dQ/dV (graphite 0.2C)"); ax[1,1].set_xlabel("V [V]"); ax[1,1].set_ylabel("dQ/dV"); ax[1,1].legend(fontsize=8)

# V6 — 전자항 골 ΔS_e(x): x_MIT=0.50(코드 시연) vs 0.85(물리 anchor)
xx = np.linspace(0.2, 1.0, 400)
ax[1,2].plot(xx, m.func_dSe_molar(xx, 298.15, 13.0, 0.50, 0.05), 'C1', label="x_MIT=0.50 (코드 tier-C)")
ax[1,2].plot(xx, m.func_dSe_molar(xx, 298.15, 13.0, 0.85, 0.05), 'C3', label="x_MIT=0.85 (물리 anchor)")
ax[1,2].axhline(-46, color='k', lw=0.5, ls=':'); ax[1,2].set_title("V6  전자엔트로피 골 ΔS_e(x) (eq:dSegate)")
ax[1,2].set_xlabel("x in Li_xCoO2"); ax[1,2].set_ylabel("ΔS_e [J/mol·K]"); ax[1,2].legend(fontsize=8)

# V7 — 다온도 T² 곡률(현 동결근사=선형; 주의 라벨)
Ts = np.linspace(278.15, 318.15, 40)
tr_e = [t for t in m.LCO_MSMR_LIT if t.get('electronic')][0]
Uj_code = [float(m.func_U_j(T, tr_e['dH_rxn'], lco._effective_dS_rxn(tr_e, T))) for T in Ts]
ax[2,0].plot(Ts-273.15, np.array(Uj_code)*1e3 - Uj_code[len(Ts)//2]*1e3, 'C1', label="현 코드(T_ref 동결=선형)")
ax[2,0].set_title("V7  LCO 전자전이 U_j(T) (동결근사=선형; T² 곡률 미구현)")
ax[2,0].set_xlabel("T [°C]"); ax[2,0].set_ylabel("ΔU_j [mV]"); ax[2,0].legend(fontsize=8)

# V9 — 면적보존 회귀 (∫equilibrium dV vs ΣQ_j)
Vfine = np.linspace(0.0, 0.4, 5000)
gr0 = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.0, Cbg=0.0)
area = float(_trapz(np.asarray(gr0.equilibrium(Vfine, 298.15)), Vfine))
Qsum = sum(t['Q'] for t in m.GRAPHITE_STAGING_LIT)
ax[2,1].bar(["∫dQ/dV dV", "ΣQ_j"], [area, Qsum], color=['C0','C2'])
ax[2,1].set_title(f"V9  면적보존 (ratio={area/Qsum:.4f})"); ax[2,1].set_ylabel("charge")

# V8 자리 — q_rev LCO(전자 서명)
ql = np.asarray(lco.reversible_heat(Vc, 298.15, 1.0))
ax[2,2].plot(Vc, ql, 'C3'); ax[2,2].axhline(0, color='k', lw=0.5, ls=':')
ax[2,2].set_title("V8  LCO q_rev (전자전이 서명)"); ax[2,2].set_xlabel("V [V]"); ax[2,2].set_ylabel("q_rev [W]")

plt.tight_layout()
plt.savefig(OUT, dpi=100)
print(f"saved: {OUT}")
print(f"V2 round-trip max|err| = {max(abs(a-b) for a,b in zip(inp,rec)):.2e} (기대 ~0)")
print(f"V9 면적보존 ratio = {area/Qsum:.4f}")
print("=== P5 GRAPH SUITE DONE ===")
