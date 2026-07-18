# -*- coding: utf-8 -*-
"""양 버전(v1.0.22·v1.0.23) 샘플 곡선 QA — 물리 타당성 + 연속·매끄러움·미분가능성.
- dQ/dV(ICA) 흑연 평형/동역학 dis·chg, LCO, 블렌드 스윕, (v23) ratio 보정
- DVA(dV/dQ)
- 매끄러움 정량: (1) 유한값(연속) (2) C1 격자세분 테스트(kink=1차도함수 점프가 세분에도 안 줄어듦)
"""
import importlib.util, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

def load(path, name):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

BASE = "/home/user/Project_Anode_Fit/Claude/docs"
v22 = load(f"{BASE}/v1.0.22/Anode_Fit_v1.0.22.py", "af22")
v23 = load(f"{BASE}/v1.0.23/Anode_Fit_v1.0.23.py", "af23")

def c1_refine_test(model_curve_fn, V0, V1, N=1500):
    """C1 매끄러움: 격자 N·2N 에서 1차도함수 최대 점프(=|2차차분|) 비교.
       smooth ⟹ 세분 시 ~½ (수렴), kink ⟹ ~const/증가."""
    def maxjump(N):
        V = np.linspace(V0, V1, N); y = model_curve_fn(V)
        if not np.all(np.isfinite(y)): return np.inf, V, y
        d1 = np.gradient(y, V); d2 = np.abs(np.gradient(d1, V))
        return float(np.max(d2)), V, y
    j1, V, y = maxjump(N); j2, _, _ = maxjump(2*N)
    ratio = (j2/j1) if j1 > 0 and np.isfinite(j1) else np.nan
    return {"finite": bool(np.all(np.isfinite(y))), "maxd2_N": j1, "maxd2_2N": j2,
            "refine_ratio": ratio, "V": V, "y": y,
            "ymin": float(np.min(y)), "ymax": float(np.max(y))}

# ---- 모델 구성 (양 버전 동일 파라미터) ----
def make(mod, kind):
    if kind == "graphite":
        return mod.GraphiteAnodeDischargeDQDV(mod.GRAPHITE_STAGING_LIT)
    if kind == "lco":
        return mod.LCOCathodeDQDV(mod.LCO_MSMR_LIT)
    if kind == "blend":
        return None  # blend below

# 흑연 전위창(V): staging peaks ~0.09~0.21 V
GV = (0.05, 0.25)
# LCO 전위창
LV = (3.85, 4.10)

results = {}
def curve_fn(model, direction, c_rate):
    return lambda V: np.asarray(model.curve(V, direction, c_rate=c_rate, Q_cell=1.0, T=298.15), dtype=float)

# ===== 패널별 QA (v23 기준 + v22 대조) =====
panels = []
for mod, tag in [(v22, "v1.0.22"), (v23, "v1.0.23")]:
    g = make(mod, "graphite"); lco = make(mod, "lco")
    panels.append((tag, "흑연 dQ/dV 평형(c=0) 방전", c1_refine_test(curve_fn(g,'discharge',0.0), *GV)))
    panels.append((tag, "흑연 dQ/dV 동역학(c=1) 방전", c1_refine_test(curve_fn(g,'discharge',1.0), *GV)))
    panels.append((tag, "흑연 dQ/dV 동역학(c=1) 충전", c1_refine_test(curve_fn(g,'charge',1.0), *GV)))
    panels.append((tag, "LCO dQ/dV 평형(c=0) 충전", c1_refine_test(curve_fn(lco,'charge',0.0), *LV)))

# v23 전용: ratio 보정 (해상 regime L_V override)
tr_res = [dict(t) for t in v23.GRAPHITE_STAGING_LIT]
for t in tr_res: t['L_V'] = 0.006   # 해상 regime
g23_off = v23.GraphiteAnodeDischargeDQDV(tr_res)
g23_on  = v23.GraphiteAnodeDischargeDQDV(tr_res, lag_ratio_correction=True)
panels.append(("v1.0.23", "흑연 dQ/dV ratio-OFF(동결) 방전", c1_refine_test(curve_fn(g23_off,'discharge',1.0), *GV)))
panels.append(("v1.0.23", "흑연 dQ/dV ratio-ON(1차보정) 방전", c1_refine_test(curve_fn(g23_on,'discharge',1.0), *GV)))

# ===== 매끄러움 판정 규약 캘리브레이션 =====
# C2 smooth ⟹ 이산 2차도함수가 유한 해석값으로 수렴 (세분비→1.0)
# kink(C0) ⟹ 1차도함수 점프 → 2차차분 발산 (세분비→2.0, 세분마다 2배)
def _cal(fn, lbl):
    r = c1_refine_test(fn, -1.0, 1.0, N=2000)
    print(f"  캘리브레이션 {lbl:14} 세분비={r['refine_ratio']:.3f}  (기대: smooth≈1.0 / kink≈2.0)")
print("[판정 규약 캘리브레이션]")
_cal(lambda x: x**2, "x^2 (smooth)")
_cal(lambda x: np.abs(x), "|x| (kink)")

def verdict_of(r):
    if not r["finite"]: return "NON-FINITE ✗"
    rr = r["refine_ratio"]
    if np.isnan(rr): return "FLAT(상수)"
    if rr < 1.4: return "SMOOTH C2 ✓"      # 수렴(유한 2차도함수)
    if rr < 1.8: return "경계 ~C1"
    return "KINK ✗"                          # 발산(1차도함수 점프)

print("\n"+"="*94)
print(f"{'버전':8} {'패널':32} {'유한':5} {'maxd2(N)':>11} {'maxd2(2N)':>11} {'세분비':>7} {'판정'}")
print("-"*94)
allok = True
for tag, name, r in panels:
    v = verdict_of(r); allok = allok and ("✗" not in v)
    print(f"{tag:8} {name:32} {str(r['finite']):5} {r['maxd2_N']:11.3e} {r['maxd2_2N']:11.3e} {r['refine_ratio']:7.3f} {v}")
print("="*94)
print(f">>> 전 패널 유한·매끄러움(kink/발산 0): {'PASS' if allok else 'FAIL'}")
# 물리 값 범위(부호·크기)
print("\n[물리 값 범위]")
for tag, name, r in panels:
    if 'dQ/dV' in name:
        print(f"  {tag} {name:32}: dQ/dV ∈ [{r['ymin']:+.3f}, {r['ymax']:+.3f}]  (peak>0 기대)")

# ===== v22 vs v23 공유경로 동일성 =====
print("\n[v22 vs v23 공유경로 곡선 동일성]")
for direction, c in [('discharge',0.0),('discharge',1.0),('charge',1.0)]:
    V = np.linspace(*GV, 1200)
    y22 = np.asarray(make(v22,'graphite').curve(V,direction,c_rate=c,Q_cell=1.0), dtype=float)
    y23 = np.asarray(make(v23,'graphite').curve(V,direction,c_rate=c,Q_cell=1.0), dtype=float)
    print(f"  흑연 {direction} c={c}: max|v22-v23| = {np.max(np.abs(y22-y23)):.2e}  (기본 off → bit-exact 기대)")

# ===== 그림 렌더 =====
OUT = "/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/results/qa_images"
import os; os.makedirs(OUT, exist_ok=True)

def render_version(mod, tag, fname, with_ratio=False):
    g = make(mod,'graphite'); lco = make(mod,'lco')
    fig, ax = plt.subplots(2, 3, figsize=(16, 9)); fig.suptitle(f"Anode_Fit {tag} — sample curves QA", fontsize=14)
    Vg = np.linspace(*GV, 2000); Vl = np.linspace(*LV, 2000)
    # 1 흑연 평형 vs 동역학 방전
    ax[0,0].plot(Vg, g.curve(Vg,'discharge',c_rate=0.0,Q_cell=1.0), label='eq (c=0)')
    ax[0,0].plot(Vg, g.curve(Vg,'discharge',c_rate=1.0,Q_cell=1.0), label='kinetic (c=1)')
    ax[0,0].set_title('graphite dQ/dV discharge'); ax[0,0].set_xlabel('V'); ax[0,0].legend(); ax[0,0].grid(alpha=.3)
    # 2 흑연 충전
    ax[0,1].plot(Vg, g.curve(Vg,'charge',c_rate=1.0,Q_cell=1.0), color='C3')
    ax[0,1].set_title('graphite dQ/dV charge (c=1)'); ax[0,1].set_xlabel('V'); ax[0,1].grid(alpha=.3)
    # 3 DVA (dV/dQ vs Q)
    dqdv = np.asarray(g.curve(Vg,'discharge',c_rate=0.0,Q_cell=1.0), dtype=float)
    Q = np.concatenate([[0],np.cumsum((dqdv[1:]+dqdv[:-1])/2*np.diff(Vg))])
    with np.errstate(divide='ignore'): dvdq = 1.0/np.where(dqdv>1e-6, dqdv, np.nan)
    ax[0,2].plot(Q, dvdq, color='C2'); ax[0,2].set_title('graphite DVA dV/dQ (eq)'); ax[0,2].set_xlabel('Q'); ax[0,2].set_ylim(0, np.nanpercentile(dvdq,98)); ax[0,2].grid(alpha=.3)
    # 4 LCO
    ax[1,0].plot(Vl, lco.curve(Vl,'charge',c_rate=0.0,Q_cell=1.0), color='C4')
    ax[1,0].set_title('LCO dQ/dV charge (eq)'); ax[1,0].set_xlabel('V'); ax[1,0].grid(alpha=.3)
    # 5 블렌드 스윕
    for m_si in [0.0,0.1,0.2,0.3]:
        b = _mkblend(mod,m_si)
        if b is not None:
            ax[1,1].plot(Vg, b.curve(Vg,'discharge',c_rate=0.0,Q_cell=1.0), label=f'{int(m_si*100)}wt%')
    ax[1,1].set_title('blend dQ/dV (m_Si sweep)'); ax[1,1].set_xlabel('V'); ax[1,1].legend(fontsize=8); ax[1,1].grid(alpha=.3)
    # 6 ratio (v23만) or 2차도함수 매끄러움 시각화
    if with_ratio:
        ax[1,2].plot(Vg, g23_off.curve(Vg,'discharge',c_rate=1.0,Q_cell=1.0), label='ratio OFF (frozen)')
        ax[1,2].plot(Vg, g23_on.curve(Vg,'discharge',c_rate=1.0,Q_cell=1.0), '--', label='ratio ON (1st corr)')
        ax[1,2].set_title('graphite ratio option (L_V/w=0.3)'); ax[1,2].legend(fontsize=8)
    else:
        y = np.asarray(g.curve(Vg,'discharge',c_rate=1.0,Q_cell=1.0),dtype=float)
        ax[1,2].plot(Vg, np.gradient(np.gradient(y,Vg),Vg), color='gray'); ax[1,2].set_title('d2(dQ/dV)/dV2 (smooth=no spike)')
    ax[1,2].set_xlabel('V'); ax[1,2].grid(alpha=.3)
    fig.tight_layout(rect=[0,0,1,0.97]); p=f"{OUT}/{fname}"; fig.savefig(p, dpi=110); plt.close(fig); return p

def _mkblend(mod, m_si):
    try:
        return mod.BlendedAnodeDQDV.from_wt(m_si)   # classmethod → 모델 반환 (C-052 환산)
    except Exception as e:
        print("blend build fail", m_si, e); return None

p22 = render_version(v22, "v1.0.22", "qa_v1022.png", with_ratio=False)
p23 = render_version(v23, "v1.0.23", "qa_v1023.png", with_ratio=True)
print(f"\n렌더: {p22}\n      {p23}")
