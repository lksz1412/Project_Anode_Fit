# -*- coding: utf-8 -*-
"""v1.0.19 그래프 suite — 검증·복원 (V1-V9 핵심 패널). 이론 근거 Ch1·Ch2 (v1.0.19).

[이식 유래] docs/v1.0.10/graph_suite_p5.py (P5 산출) → v1.0.13 → v1.0.14 → v1.0.16
(graph_suite_v1016.py) → 본 파일(v1.0.19 이관 — FITTING_GUIDE §7 의 suite 를 v1.0.19
폴더에 동봉하는 R-P1 C2 조치).
로직 무변경 원칙 — v1.0.16 에서 어긋나는 최소 지점만 수정:
  (1) CODE/OUT 경로: import 대상 = Anode_Fit_v1.0.19.py, 출력 = 본 폴더 figs\
      (스크립트 위치 기준 상대경로 — 어느 cwd 에서도 동일).
  (2) 버전 라벨 현행화: "v1.0.16 코드" → "v1.0.19 코드" (V6 x_MIT=0.85 anchor 동일).
  (3) V4 검증 추가(read-only): 수동 단순식 헬퍼 vs v1.0.19 신규
      entropy_coefficient(..., return_terms=True)['simple'] 일치 확인 print —
      패널 로직·플롯 라인은 v1.0.16 그대로(additive 확인만).
V1-V9 패널 내용·모델 호출은 v1.0.16 판과 동일(케이스 구성 무변경).

[재현] PYTHONIOENCODING=utf-8 python graph_suite_v1019.py
"""
import sys, os
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import importlib.util
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
try:  # 한글 라벨 렌더링 보정 — 실패해도 실행은 계속 (DejaVu fallback)
    matplotlib.rcParams["font.family"] = ["Malgun Gothic", "DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.environ.get("ANODEFIT_CODE", os.path.join(HERE, "Anode_Fit_v1.0.19.py"))
OUT = os.path.join(HERE, "figs", "graph_suite_v1019.png")
spec = importlib.util.spec_from_file_location("anodefit", CODE)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
_trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))
F = m.F

gr = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.0)
lco = m.LCOCathodeDQDV(m.LCO_MSMR_LIT, x=0.5, Rn=0.01, Cbg=0.0)
Vg = np.linspace(0.03, 0.34, 1000)
Vc = np.linspace(3.75, 4.15, 1000)

_finite_log = []  # read-only 검증 수집

def _chk(name, arr):
    ok = bool(np.all(np.isfinite(np.asarray(arr, dtype=float))))
    _finite_log.append((name, ok))
    return arr

fig, ax = plt.subplots(3, 3, figsize=(16, 13))

# V1 — 흑연(방전=탈리튬화) + LCO(충전=탈리튬화) dQ/dV 나란히 — 둘 다 저수준 s=+1
ax[0,0].plot(Vg, _chk("V1 graphite", gr.dqdv(Vg, 298.15, 0.05, 1.0, +1)), 'C0', label="graphite dis")
axb = ax[0,0].twiny(); axb.plot(Vc, _chk("V1 LCO", lco.dqdv(Vc, 298.15, 0.05, 1.0, +1)), 'C3', label="LCO chg")
ax[0,0].set_title("V1  graphite(dis) + LCO(chg) dQ/dV — delithiation s=+1")
ax[0,0].set_xlabel("V anode [V]"); axb.set_xlabel("V cathode [V]", color='C3')
ax[0,0].set_ylabel("dQ/dV")

# V2 — round-trip 복원 parity (입력 ΔS_rxn → func_U_j FD → 회귀 ΔŜ = F·(∂U/∂T)_FD)
T1, T2 = 292.15, 298.15
inp, rec = [], []
for tr in m.GRAPHITE_STAGING_LIT + [t for t in m.LCO_MSMR_LIT if not t.get('electronic')]:
    dS = tr['dS_rxn']
    fd = (float(m.func_U_j(T2, tr['dH_rxn'], dS)) - float(m.func_U_j(T1, tr['dH_rxn'], dS))) / (T2 - T1)
    inp.append(dS); rec.append(F * fd)
_chk("V2 parity", rec)
ax[0,1].plot([-20, 30], [-20, 30], 'k:', lw=0.8)
ax[0,1].scatter(inp, rec, c='C2', zorder=3)
ax[0,1].set_title("V2  round-trip parity  ΔS_in vs ΔŜ=F·(∂U/∂T)_FD"); ax[0,1].set_xlabel("ΔS_rxn input"); ax[0,1].set_ylabel("recovered")
ax[0,1].text(0.05, 0.9, f"max|err|={max(abs(a-b) for a,b in zip(inp,rec)):.2e}", transform=ax[0,1].transAxes, fontsize=9)

# V3 — q_rev(V) 흡·발열 교대
qg = np.asarray(_chk("V3 q_rev graphite", gr.reversible_heat(Vg, 298.15, 1.0)))
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
full = np.asarray(_chk("V4 full", gr.entropy_coefficient(Vg, 298.15)))*1e3
simp = np.asarray(_chk("V4 simple", dUdT_simple(gr, Vg)))*1e3
ax[1,0].plot(Vg, full, 'C0', label="완전식(+config)"); ax[1,0].plot(Vg, simp, 'C1--', label="단순식(중심만)")
ax[1,0].set_title("V4  ∂U/∂T 완전식 vs 단순식 [mV/K]"); ax[1,0].set_xlabel("V [V]"); ax[1,0].set_ylabel("∂U/∂T [mV/K]"); ax[1,0].legend(fontsize=8)
# (3) v1.0.19 return_terms 교차검증(read-only): 수동 단순식 == 코드 'simple' 분리 출력
_terms_v19 = gr.entropy_coefficient(Vg, 298.15, return_terms=True)
v4_xchk = float(np.max(np.abs(np.asarray(_terms_v19['simple'])*1e3 - simp)))
_chk("V4 return_terms simple", _terms_v19['simple'])

# V5 — 온도의존 peak 이동
for Tk, c in [(258.15,'C0'), (298.15,'C1'), (318.15,'C3')]:
    ax[1,1].plot(Vg, _chk(f"V5 T={Tk}", gr.dqdv(Vg, Tk, 0.2, 1.0, +1)), c, label=f"{Tk-273.15:+.0f}°C")
ax[1,1].set_title("V5  온도의존 dQ/dV (graphite 0.2C)"); ax[1,1].set_xlabel("V [V]"); ax[1,1].set_ylabel("dQ/dV"); ax[1,1].legend(fontsize=8)

# V6 — 전자항 골 ΔS_e(x): 물리 anchor 0.85(v1.0.19 코드 현행) vs pre-v1.0.14 demo 0.50(참조)
xx = np.linspace(0.2, 1.0, 400)
ax[1,2].plot(xx, _chk("V6 0.85", m.func_dSe_molar(xx, 298.15, 13.0, 0.85, 0.05)), 'C3',
             label="x_MIT=0.85 physical anchor (v1.0.19 코드)")
ax[1,2].plot(xx, _chk("V6 0.50", m.func_dSe_molar(xx, 298.15, 13.0, 0.50, 0.05)), 'C1--',
             label="x_MIT=0.50 pre-v1.0.14 demo (참조)")
ax[1,2].axhline(-46, color='k', lw=0.5, ls=':'); ax[1,2].set_title("V6  전자엔트로피 골 ΔS_e(x) (eq:dSegate)")
ax[1,2].set_xlabel("x in Li_xCoO2"); ax[1,2].set_ylabel("ΔS_e [J/mol·K]"); ax[1,2].legend(fontsize=8)

# V7 — 다온도 T² 곡률(현 동결근사=선형; 주의 라벨 유지)
Ts = np.linspace(278.15, 318.15, 40)
tr_e = [t for t in m.LCO_MSMR_LIT if t.get('electronic')][0]
Uj_code = [float(m.func_U_j(T, tr_e['dH_rxn'], lco._effective_dS_rxn(tr_e, T))) for T in Ts]
_chk("V7 Uj(T)", Uj_code)
ax[2,0].plot(Ts-273.15, np.array(Uj_code)*1e3 - Uj_code[len(Ts)//2]*1e3, 'C1', label="현 코드(T_ref 동결=선형)")
ax[2,0].set_title("V7  LCO 전자전이 U_j(T) (동결근사=선형; T² 곡률 미구현)")
ax[2,0].set_xlabel("T [°C]"); ax[2,0].set_ylabel("ΔU_j [mV]"); ax[2,0].legend(fontsize=8)

# V9 — 면적보존 회귀 (∫equilibrium dV vs ΣQ_j)
Vfine = np.linspace(0.0, 0.4, 5000)
gr0 = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.0, Cbg=0.0)
area = float(_trapz(np.asarray(_chk("V9 equilibrium", gr0.equilibrium(Vfine, 298.15))), Vfine))
Qsum = sum(t['Q'] for t in m.GRAPHITE_STAGING_LIT)
ax[2,1].bar(["∫dQ/dV dV", "ΣQ_j"], [area, Qsum], color=['C0','C2'])
ax[2,1].set_title(f"V9  면적보존 (ratio={area/Qsum:.4f})"); ax[2,1].set_ylabel("charge")

# V8 자리 — q_rev LCO(전자 서명)
ql = np.asarray(_chk("V8 q_rev LCO", lco.reversible_heat(Vc, 298.15, 1.0)))
ax[2,2].plot(Vc, ql, 'C3'); ax[2,2].axhline(0, color='k', lw=0.5, ls=':')
ax[2,2].set_title("V8  LCO q_rev (전자전이 서명)"); ax[2,2].set_xlabel("V [V]"); ax[2,2].set_ylabel("q_rev [W]")

plt.tight_layout()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=100)
print(f"saved: {OUT}")
print(f"V2 round-trip max|err| = {max(abs(a-b) for a,b in zip(inp,rec)):.2e} (기대 ~0)")
print(f"V4 return_terms 교차검증 max|manual simple - code 'simple'| = {v4_xchk:.2e} mV/K (기대 ~0)")
print(f"V9 면적보존 ratio = {area/Qsum:.4f}")
# read-only 검증 — 전 패널 finite + 현행 dict 정합(수정 없음, 확인만)
all_finite = all(ok for _, ok in _finite_log)
for name, ok in _finite_log:
    print(f"  [finite] {name}: {ok}")
print(f"ALL PANELS FINITE: {all_finite}")
print(f"현행 LCO T1 dict x_MIT = {tr_e['x_MIT']} (기대 0.85 — V6 라벨 정합 확인)")
print("=== V1.0.19 GRAPH SUITE DONE ===")
