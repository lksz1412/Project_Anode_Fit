# -*- coding: utf-8 -*-
"""v1.0.18.1 그래프 suite — 검증·복원 (V1-V9 핵심 패널). 이론 근거 Ch1·Ch2 (v1.0.18.1).

[이식 유래] docs/v1.0.10/graph_suite_p5.py (P5 산출) → v1.0.13(graph_suite_v1013.py, v1.0.13 P6.1 이식)
→ v1.0.14 승계(본 파일 — v1.0.14 P1.1 복사 후 버전 문자열 현행화).
로직 무변경 원칙 — v1.0.14 에서 어긋나는 최소 지점만 수정:
  (1) CODE/OUT 경로: v1.0.10 → v1.0.18.1 (import 대상 = Anode_Fit_v1.0.18.1.py, 출력 = v1.0.18.1\\figs).
  (2) V6 라벨 현행화: 현행 LCO_MSMR_LIT 는 loop B 재정렬로 x_MIT=0.85(물리 anchor)가 코드값 —
      0.85 = "physical anchor (v1.0.18.1 코드 현행)", 0.50 = "pre-v1.0.14 demo (참조)" 로 라벨 교체
      (구판 라벨은 0.50 을 "코드 tier-C"로 지목 — 현행 코드와 불일치라 그대로 두면 오독).
  (3) V1 LCO 방향 라벨: 저수준 dqdv(s=+1) 의 물리 = 탈리튬화 = LCO 하프셀 '충전'(Ch1 boxed
      eq:lco-sigmaslot) — 구판 제목 "discharge" 는 R9_B D1 과 동일 계열 라벨-물리 불일치라 정정
      (호출 자체는 무변경 — s=+1 유지, 흑연은 방전=탈리튬화라 기존 라벨 그대로).
  (4) 렌더링 보정: 한글 라벨 폰트(Malgun Gothic) 지정 + unicode minus off (Windows tofu 방지).
  (5) read-only 검증 print: 전 패널 배열 finite 확인 추가(모델 호출·수치 로직 무변경).
v1.0.14 신설 가드와의 정합: 모든 dqdv/equilibrium/entropy 호출이 배열 스윕(1000/5000점)이라
스칼라 평형 강제(퇴화 스팬 가드)와 무충돌, 데이터셋 전 전이가 'n' 키 보유라 'w'-단독 config
게이트 경로도 미발동 — 배열 호출 정리 필요 0건(전수 확인).
"""
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
try:  # (4) 한글 라벨 렌더링 보정 — 실패해도 실행은 계속 (DejaVu fallback = Ŝ 등 라틴 확장 글리프)
    matplotlib.rcParams["font.family"] = ["Malgun Gothic", "DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False
except Exception:
    pass

CODE = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.18.1\Anode_Fit_v1.0.18.1.py"
OUT = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.18.1\figs\graph_suite_v1018_1.png"
spec = importlib.util.spec_from_file_location("anodefit", CODE)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
_trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))
F = m.F

gr = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.0)
lco = m.LCOCathodeDQDV(m.LCO_MSMR_LIT, x=0.5, Rn=0.01, Cbg=0.0)
Vg = np.linspace(0.03, 0.34, 1000)
Vc = np.linspace(3.75, 4.15, 1000)

_finite_log = []  # (5) read-only 검증 수집

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

# V5 — 온도의존 peak 이동
for Tk, c in [(258.15,'C0'), (298.15,'C1'), (318.15,'C3')]:
    ax[1,1].plot(Vg, _chk(f"V5 T={Tk}", gr.dqdv(Vg, Tk, 0.2, 1.0, +1)), c, label=f"{Tk-273.15:+.0f}°C")
ax[1,1].set_title("V5  온도의존 dQ/dV (graphite 0.2C)"); ax[1,1].set_xlabel("V [V]"); ax[1,1].set_ylabel("dQ/dV"); ax[1,1].legend(fontsize=8)

# V6 — 전자항 골 ΔS_e(x): 물리 anchor 0.85(v1.0.18.1 코드 현행) vs pre-v1.0.14 demo 0.50(참조)
xx = np.linspace(0.2, 1.0, 400)
ax[1,2].plot(xx, _chk("V6 0.85", m.func_dSe_molar(xx, 298.15, 13.0, 0.85, 0.05)), 'C3',
             label="x_MIT=0.85 physical anchor (v1.0.18.1 코드)")
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
plt.savefig(OUT, dpi=100)
print(f"saved: {OUT}")
print(f"V2 round-trip max|err| = {max(abs(a-b) for a,b in zip(inp,rec)):.2e} (기대 ~0)")
print(f"V9 면적보존 ratio = {area/Qsum:.4f}")
# (5) read-only 검증 — 전 패널 finite + 현행 dict 정합(수정 없음, 확인만)
all_finite = all(ok for _, ok in _finite_log)
for name, ok in _finite_log:
    print(f"  [finite] {name}: {ok}")
print(f"ALL PANELS FINITE: {all_finite}")
print(f"현행 LCO T1 dict x_MIT = {tr_e['x_MIT']} (기대 0.85 — V6 라벨 정합 확인)")
print("=== V1.0.18.1 GRAPH SUITE DONE ===")
