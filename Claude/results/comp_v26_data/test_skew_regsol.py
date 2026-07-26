# -*- coding: utf-8 -*-
"""★사용자 지시 정확 이행: 'v1.0.24 regsol 식 + v1.0.25 비대칭(skew) 결합' 커널 테스트.
skew-regsol = regsol(두-상, Ω) + 비대칭 폭(δL≠δR, @2 비대칭을 regsol에 적용).
비교(흑연·블렌드): logistic-4 · regsol-4 · ★skew-regsol-4 · skew-logistic-4.
소재별: 흑연=두-상 커널, 블렌드=흑연 두-상 + Si broad. dQ/dV = BD 앙상블(99_Backend 방식).
실행: python test_skew_regsol.py → out_skew/{graphite,blend}_skewregsol.png + summary_skew.json"""
import os, json, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
from scipy.signal import savgol_filter, find_peaks
from scipy.optimize import least_squares
for _f in ["Malgun Gothic", "Gulim", "NanumGothic"]:
    if any(_f.lower() in fn.name.lower() for fn in font_manager.fontManager.ttflist):
        rcParams['font.family'] = _f; break
rcParams['axes.unicode_minus'] = False
_TRAPZ = getattr(np, 'trapezoid', None) or getattr(np, 'trapz', None)
R, F, T = 8.314, 96485.0, 298.15; RTF = R*T/F
REPO = r"D:\Projects\Project_Anode_Fit\Claude\results"
OUT = os.path.join(REPO, "comp_v26_data", "out_skew"); os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(REPO, "comp_v26_data", "skew_log.txt"); open(LOG, "w", encoding="utf-8").write("")
def log(m): print(m); open(LOG, "a", encoding="utf-8").write(str(m)+"\n")

# ---- BD 앙상블 dQ/dV ----
def _ens(d, rs):
    L = len(d); e = [d]
    for r in rs:
        w = int(round(L*r/2))*2+1
        if 3 < w < L:
            try: e.append(savgol_filter(d, w, 3))
            except Exception: pass
            try: e.append(1.0/savgol_filter(1.0/d, w, 3))
            except Exception: pass
    return np.nanmedian(np.array(e), axis=0)
def bd_dqdv(V, Q):
    o = np.argsort(Q); V, Q = np.asarray(V, float)[o], np.asarray(Q, float)[o]
    Qu, ix = np.unique(np.round(Q, 8), return_index=True); Vu = V[ix]
    if len(Qu) < 25: return None, None
    dVdQ = np.gradient(Vu, Qu); dVdQ = np.where(np.abs(dVdQ) < 1e-12, 1e-12, dVdQ)
    ds = _ens(dVdQ, [0.02, 0.03, 0.04]); dw = _ens(dVdQ, [0.03, 0.05, 0.07])
    ratio = np.clip(np.abs(1/dw)/np.nanmax(np.abs(1/dw)), 0, 1)
    return Vu, np.abs((1/ds)*(1-ratio) + (1/dw)*ratio)

# ---- 커널 ----
_XG = np.linspace(1e-4, 1-1e-4, 500)
def _xa(a):
    if a <= 2: return 0.5
    lo, hi = 1e-6, 0.5-1e-9
    for _ in range(60):
        m = 0.5*(lo+hi)
        if np.log(m/(1-m))+a*(1-2*m) > 0: hi = m
        else: lo = m
    return 0.5*(lo+hi)
def logistic(V, U, w, Q):
    s = 1/(1+np.exp(-np.clip((V-U)/w, -350, 350))); return Q*s*(1-s)/w
def skew_logistic(V, U, wL, wR, Q):        # @2 비대칭 폭 (좌/우 다른 폭)
    w = np.where(V < U, wL, wR); s = 1/(1+np.exp(-np.clip((V-U)/w, -350, 350)))
    return Q*s*(1-s)*(4.0/(wL+wR))
def regsol(V, U0, Om, Q, d):               # v1.0.24 regsol (두-상 Ω)
    xa = _xa(Om/(R*T))
    Vi = np.where((_XG > xa) & (_XG < 1-xa), U0, U0-RTF*np.log(_XG/(1-_XG))-(Om/F)*(1-2*_XG))
    d = max(d, 1e-9); z = np.clip((np.asarray(V, float)[:, None]-Vi[None, :])/(2*d), -350, 350)
    return (Q/_XG.size/np.cosh(z)**2/(4*d)).sum(1)
def skew_regsol(V, U0, Om, Q, dL, dR):     # ★regsol + 비대칭(δL≠δR) = 지시 이행 커널
    xa = _xa(Om/(R*T))
    Vi = np.where((_XG > xa) & (_XG < 1-xa), U0, U0-RTF*np.log(_XG/(1-_XG))-(Om/F)*(1-2*_XG))
    Vc = np.asarray(V, float)[:, None]; d = np.where(Vc < Vi[None, :], max(dL, 1e-9), max(dR, 1e-9))
    z = np.clip((Vc-Vi[None, :])/(2*d), -350, 350)
    return (Q/_XG.size/np.cosh(z)**2*(2.0/(dL+dR))).sum(1)

def _r2(D, P): return float(1-np.sum((D-P)**2)/np.sum((D-D.mean())**2))
_rng = np.random.default_rng(5)
def _fit(resid, p0, lb, ub, k=5, nfev=10000):
    p0, lb, ub = map(lambda a: np.asarray(a, float), (p0, lb, ub)); best, bc = None, np.inf
    for j in range(k):
        st = p0 if j == 0 else np.clip(p0*_rng.uniform(0.6, 1.4, len(p0)), lb, ub)
        try:
            r = least_squares(resid, st, bounds=(lb, ub), max_nfev=nfev)
            if r.cost < bc: bc, best = r.cost, r.x
        except Exception: pass
    return best
def _metrics(Vx, Dx, pred):
    pk, _ = find_peaks(Dx, prominence=Dx.max()*0.04); vl, _ = find_peaks(-Dx, prominence=Dx.max()*0.02)
    def rn(idx, h=6):
        if len(idx) == 0: return 0.0
        m = np.zeros_like(Dx, bool)
        for i in idx: m[max(0, i-h):i+h] = True
        return float(np.sqrt(np.mean((Dx[m]-pred[m])**2)))
    return round(_r2(Dx, pred), 4), round(rn(pk), 2), round(rn(vl), 2)

# ---- 흑연: 4종 커널 피팅 ----
def fit_graphite(Vx, Dx):
    area = float(_TRAPZ(Dx, Vx)); lo, hi = Vx.min(), Vx.max(); U0 = list(np.linspace(0.085, 0.21, 4))
    res = {}
    # logistic-4
    def ML(p): return sum(logistic(Vx, p[j], p[4+j], p[8+j]) for j in range(4))+p[12]
    p = _fit(lambda p: ML(p)-Dx, U0+[0.006]*4+[area/4]*4+[Dx.min()],
             [lo]*4+[8e-4]*4+[1e-6]*4+[0], [hi]*4+[0.06]*4+[10*area]*4+[Dx.max()])
    res['logistic-4'] = (ML, p, 13)
    # regsol-4
    def MR(p): return sum(regsol(Vx, p[j], p[4+j], p[8+j], p[12+j]) for j in range(4))+p[16]
    p = _fit(lambda p: MR(p)-Dx, U0+[2.4*R*T]*4+[area/4]*4+[0.003]*4+[Dx.min()],
             [lo]*4+[0.5*R*T]*4+[1e-6]*4+[3e-4]*4+[0], [hi]*4+[6*R*T]*4+[10*area]*4+[0.03]*4+[Dx.max()])
    res['regsol-4'] = (MR, p, 17)
    # ★skew-regsol-4 (regsol + 비대칭 δL,δR)
    def MSR(p): return sum(skew_regsol(Vx, p[j], p[4+j], p[8+j], p[12+j], p[16+j]) for j in range(4))+p[20]
    p = _fit(lambda p: MSR(p)-Dx, U0+[2.4*R*T]*4+[area/4]*4+[0.003]*4+[0.003]*4+[Dx.min()],
             [lo]*4+[0.5*R*T]*4+[1e-6]*4+[3e-4]*4+[3e-4]*4+[0], [hi]*4+[6*R*T]*4+[10*area]*4+[0.03]*4+[0.03]*4+[Dx.max()])
    res['skew-regsol-4'] = (MSR, p, 21)
    # skew-logistic-4 (@2 비대칭 단독, 참조)
    def MSL(p): return sum(skew_logistic(Vx, p[j], p[4+j], p[8+j], p[12+j]) for j in range(4))+p[16]
    p = _fit(lambda p: MSL(p)-Dx, U0+[0.006]*4+[0.006]*4+[area/4]*4+[Dx.min()],
             [lo]*4+[8e-4]*4+[8e-4]*4+[1e-6]*4+[0], [hi]*4+[0.06]*4+[0.06]*4+[10*area]*4+[Dx.max()])
    res['skew-logistic-4'] = (MSL, p, 17)
    return res

def run(csv, name, win):
    df = pd.read_csv(csv); cv = next(c for c in df.columns if 'v' in c.lower()); cq = next(c for c in df.columns if 'q' in c.lower())
    Vb, Db = bd_dqdv(df[cv].to_numpy(float), df[cq].to_numpy(float))
    m = (Vb >= win[0]) & (Vb <= win[1]); Vx, Dx = Vb[m], Db[m]
    fits = fit_graphite(Vx, Dx)
    out = {}
    for k, (M, p, npar) in fits.items():
        if p is None: continue
        pred = M(p); r2, prm, vrm = _metrics(Vx, Dx, pred)
        out[k] = {'R2': r2, 'peakRMSE': prm, 'valleyRMSE': vrm, 'nparams': npar, 'pred': pred}
        log(f"  {name} {k:16s} R²={r2}  peakRMSE={prm}  valleyRMSE={vrm}  ({npar}p)")
    # 플롯
    fig, ax = plt.subplots(1, 2, figsize=(15, 5.6)); cols = {'logistic-4': 'darkorange', 'regsol-4': 'seagreen', 'skew-regsol-4': 'crimson', 'skew-logistic-4': 'slateblue'}
    for a in ax:
        a.plot(Vx, Dx, color='0.15', lw=2.4, label='real dQ/dV', zorder=5)
        for k, v in out.items(): a.plot(Vx, v['pred'], lw=1.7, color=cols.get(k, 'gray'), label=f"{k} R²={v['R2']}")
        a.set_xlabel('V vs Li'); a.set_ylabel('dQ/dV (mAh/V)'); a.grid(alpha=.3)
    ax[0].set_xlim(win); ax[0].set_title(f'{name} — 4종 커널 (★skew-regsol = regsol+비대칭)'); ax[0].legend(fontsize=8)
    z = (0.06, 0.17) if name == 'graphite' else (0.08, 0.17)
    ax[1].set_xlim(z); mz = (Vx >= z[0]) & (Vx <= z[1])
    if mz.any(): ax[1].set_ylim(0, Dx[mz].max()*1.1)
    ax[1].set_title(f'{name} — 피크역 확대 (일치도)'); ax[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, f"{name}_skewregsol.png"), dpi=130); plt.close(fig)
    log(f"saved {name}_skewregsol.png")
    return {k: {kk: vv for kk, vv in v.items() if kk != 'pred'} for k, v in out.items()}

log("=== skew-regsol 결합 커널 테스트 (사용자 지시 이행) ===")
summ = {}
D = os.path.join(REPO, "comp_v24", "sintef_data")
for csv, name, win in [(os.path.join(D, "gr.csv"), "graphite", (0.05, 0.30)),
                       (os.path.join(D, "sigr.csv"), "blend", (0.05, 0.30))]:
    if os.path.exists(csv):
        log(f"[{name}] {csv}")
        try: summ[name] = run(csv, name, win)
        except Exception as e:
            import traceback; log(f"  ERR {e}\n{traceback.format_exc()[:400]}")
json.dump(summ, open(os.path.join(OUT, "summary_skew.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
log("=== SUMMARY ===\n"+json.dumps(summ, ensure_ascii=False, indent=2)); log("DONE")
