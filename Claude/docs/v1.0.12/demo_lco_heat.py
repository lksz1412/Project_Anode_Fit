# -*- coding: utf-8 -*-
"""P4 편입 검증 — LCO 양극 dQ/dV + 가역 발열 + 전자엔트로피 + 그래프."""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # cp949 콘솔서도 실행 보장
except Exception:
    pass
import importlib.util
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CODE = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.10\Anode_Fit_v1.0.10.py"
FIGS = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.10\figs"

spec = importlib.util.spec_from_file_location("anodefit_v1010", CODE)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

print("=== 1. 전자엔트로피 골 깊이 검산 (Ch1 -46 J/mol/K) ===")
dSe_center = float(m.func_dSe_molar(0.50, 298.15, 13.0, 0.50, 0.05))
print(f"  func_dSe_molar(x=x_MIT=0.50) = {dSe_center:.2f} J/mol/K  (기대 ~ -45.7)")
dSe_far = float(m.func_dSe_molar(0.20, 298.15, 13.0, 0.50, 0.05))
print(f"  func_dSe_molar(x=0.20, 창 밖) = {dSe_far:.3f} J/mol/K  (기대 ~ 0)")

print("=== 2. seam 3경로 공유 — LCO 전자전이 dS_eff = dS_rxn + dSe ===")
lco = m.LCOCathodeDQDV(m.LCO_MSMR_LIT, x=0.5, Rn=0.01, Cbg=0.0)
tr_e = m.LCO_MSMR_LIT[1]  # electronic 전이
dS_eff = float(lco._effective_dS_rxn(tr_e, 298.15))
print(f"  전자전이: dS_rxn={tr_e['dS_rxn']:+.1f} + dSe({dSe_center:.1f}) = dS_eff={dS_eff:.2f}")
tr_n = m.LCO_MSMR_LIT[0]  # 비전자 전이
print(f"  비전자전이: dS_eff={float(lco._effective_dS_rxn(tr_n, 298.15)):.2f} (=dS_rxn {tr_n['dS_rxn']:+.1f}, 항등)")
graph = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.0)
print(f"  흑연 base seam 항등: {float(graph._effective_dS_rxn(m.GRAPHITE_STAGING_LIT[0], 298.15)):.2f} (=dS_rxn +29.0)")

print("=== 3. LCO dQ/dV 개형 (방전 σ_d=+1) ===")
Vc = np.linspace(3.75, 4.15, 1200)
y_lco = np.asarray(lco.dqdv(Vc, T=298.15, I_abs=0.05, Q_cell=1.0, s=+1), dtype=float)
peaks_V = [Vc[i] for i in range(1, len(Vc)-1) if y_lco[i] > y_lco[i-1] and y_lco[i] >= y_lco[i+1] and y_lco[i] > 0.5]
print(f"  finite={np.all(np.isfinite(y_lco))} min={y_lco.min():.3f} max={y_lco.max():.3f}")
print(f"  국소 피크 전위(≈전이 U): {[f'{v:.3f}' for v in peaks_V]}  (목표 3.880·3.930·4.050)")

print("=== 4. 가역 발열 q_rev = -I·T·dU/dT (T 한 번) ===")
Vg = np.linspace(0.03, 0.34, 1000)
qg = np.asarray(graph.reversible_heat(Vg, T=298.15, I=1.0), dtype=float)
ql = np.asarray(lco.reversible_heat(Vc, T=298.15, I=1.0), dtype=float)
print(f"  흑연 q_rev: finite={np.all(np.isfinite(qg))} range=[{qg.min():.4f},{qg.max():.4f}] W")
print(f"  LCO  q_rev: finite={np.all(np.isfinite(ql))} range=[{ql.min():.4f},{ql.max():.4f}] W")
# 부호: dU/dT = -q_rev/(I·T). 방전 I>0, dU/dT>0(ΔS>0)→흡열 q<0
dUdT_g = np.asarray(graph.entropy_coefficient(Vg, 298.15))
print(f"  흑연 dU/dT range=[{dUdT_g.min()*1e3:.3f},{dUdT_g.max()*1e3:.3f}] mV/K")

print("=== 5. 그래프 생성 ===")
fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
# (a) 흑연 dQ/dV
for I, lab in [(0.02, "0.02C"), (0.2, "0.2C"), (1.0, "1.0C")]:
    ax[0].plot(Vg, graph.dqdv(Vg, T=298.15, I_abs=I, Q_cell=1.0, s=+1), label=f"dis {lab}")
ax[0].set_title("(a) Graphite anode dQ/dV (discharge)"); ax[0].set_xlabel("V [V]"); ax[0].set_ylabel("dQ/dV"); ax[0].legend(fontsize=8)
# (b) LCO dQ/dV
for I, lab in [(0.02, "0.02C"), (0.05, "0.05C"), (0.2, "0.2C")]:
    ax[1].plot(Vc, lco.dqdv(Vc, T=298.15, I_abs=I, Q_cell=1.0, s=+1), label=f"dis {lab}")
ax[1].set_title("(b) LCO cathode dQ/dV (discharge, MSMR)"); ax[1].set_xlabel("V [V]"); ax[1].set_ylabel("dQ/dV"); ax[1].legend(fontsize=8)
# (c) q_rev
ax[2].plot(Vg, qg, label="graphite q_rev", color="C0")
ax[2].plot(Vc, ql, label="LCO q_rev", color="C3")
ax[2].axhline(0, color="k", lw=0.5, ls=":")
ax[2].set_title("(c) reversible heat q_rev = -I T dU/dT"); ax[2].set_xlabel("V [V]"); ax[2].set_ylabel("q_rev [W]"); ax[2].legend(fontsize=8)
plt.tight_layout()
out = FIGS + r"\P4_lco_heat_validation.png"
plt.savefig(out, dpi=110)
print(f"  saved: {out}")
print("=== P4 VALIDATION DONE ===")
