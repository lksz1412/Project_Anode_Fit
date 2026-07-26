# -*- coding: utf-8 -*-
"""SINTEF 3종(흑연·Si·블렌드) dQ/dV 추출·소재-정확 피팅.
소스: (A) 로컬 기존 CSV comp_v24/sintef_data/{gr,si,sigr}.csv — 항상 있음(다운로드 없어도 3종 결과 보장).
      (B) comp_v26_data/raw/*.parquet — GITT/p-OCV+hold(받으면 자동 추가·프로토콜 비교).
소재 물리(lit_raw/03 B2): 흑연=두-상(regsol Ω≈2–2.5RT) / Si=연속 고용체(broad logistic) / 블렌드=중첩.
방어적: 소스별 독립 try/except, 데이터 플롯 우선, 피팅 best-effort. 실행: python analyze_sintef.py"""
import os, glob, json, traceback
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
from scipy.signal import savgol_filter
from scipy.optimize import least_squares
for _f in ["Malgun Gothic", "Gulim", "NanumGothic"]:
    if any(_f.lower() in fn.name.lower() for fn in font_manager.fontManager.ttflist):
        rcParams['font.family'] = _f; break
rcParams['axes.unicode_minus'] = False
_TRAPZ = getattr(np, 'trapezoid', None) or getattr(np, 'trapz', None)
R, F, T = 8.314, 96485.0, 298.15; RTF = R*T/F  # 25.69 mV
REPO = r"D:\Projects\Project_Anode_Fit\Claude\results"
BASE = os.path.join(REPO, "comp_v26_data"); RAW = os.path.join(BASE, "raw")
OUT = os.path.join(BASE, "out"); os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(BASE, "analyze_log.txt"); open(LOG, "w", encoding="utf-8").write("")
def log(m):
    print(m); open(LOG, "a", encoding="utf-8").write(str(m)+"\n")

# 소재별 창(staging/feature 영역)
WIN = {'graphite': (0.05, 0.30), 'silicon': (0.05, 0.60), 'blend': (0.05, 0.60)}

# ================= BD 앙상블 dQ/dV (dV/dQ 공간 savgol+reciprocal median → adaptive blend) =================
def _sav_ens(data, ratios):
    L = len(data); ens = [data]
    for r in ratios:
        w = int(round(L*r/2))*2+1
        if w <= 3 or w >= L: continue
        try: ens.append(savgol_filter(data, w, 3))
        except Exception: pass
        try: ens.append(1.0/savgol_filter(1.0/data, w, 3))
        except Exception: pass
    return np.nanmedian(np.array(ens), axis=0)
def bd_dqdv(V, Q):
    o = np.argsort(Q); V, Q = np.asarray(V, float)[o], np.asarray(Q, float)[o]
    Qu, ix = np.unique(np.round(Q, 8), return_index=True); Vu = V[ix]
    if len(Qu) < 25: return None, None
    dVdQ = np.gradient(Vu, Qu); dVdQ = np.where(np.abs(dVdQ) < 1e-12, 1e-12, dVdQ)
    ds = _sav_ens(dVdQ, [0.02, 0.03, 0.04]); dw = _sav_ens(dVdQ, [0.03, 0.05, 0.07])
    ratio = np.clip(np.abs(1/dw)/np.nanmax(np.abs(1/dw)), 0, 1)
    dQdV = (1/ds)*(1-ratio) + (1/dw)*ratio
    return Vu, np.abs(dQdV)

# ================= 커널 =================
def logistic_peak(V, U, w, Q):
    s = 1/(1+np.exp(-np.clip((V-U)/w, -350, 350))); return Q*s*(1-s)/w
_XG = np.linspace(1e-4, 1-1e-4, 500)
def _binodal_xa(a):
    if a <= 2: return 0.5
    lo, hi = 1e-6, 0.5-1e-9
    for _ in range(60):
        m = 0.5*(lo+hi)
        if np.log(m/(1-m))+a*(1-2*m) > 0: hi = m
        else: lo = m
    return 0.5*(lo+hi)
def regsol_peak(V, U0, Om, Q, d):
    xa = _binodal_xa(Om/(R*T))
    Vi = np.where((_XG > xa) & (_XG < 1-xa), U0, U0-RTF*np.log(_XG/(1-_XG))-(Om/F)*(1-2*_XG))
    d = max(d, 1e-9); z = np.clip((np.asarray(V, float)[:, None]-Vi[None, :])/(2*d), -350, 350)
    return (Q/_XG.size/np.cosh(z)**2/(4*d)).sum(1)

def _r2(Dx, pred): return float(1-np.sum((Dx-pred)**2)/np.sum((Dx-Dx.mean())**2))
_rng = np.random.default_rng(3)
def _multi_fit(resid, p0, lb, ub, restarts=4, nfev=8000):
    p0, lb, ub = map(lambda a: np.asarray(a, float), (p0, lb, ub))
    best, bc = None, np.inf
    for k in range(restarts):
        st = p0 if k == 0 else np.clip(p0*_rng.uniform(0.6, 1.4, len(p0)), lb, ub)
        try:
            r = least_squares(resid, st, bounds=(lb, ub), max_nfev=nfev)
            if r.cost < bc: bc, best = r.cost, r.x
        except Exception: pass
    return best

# ================= 소재-정확 피팅 =================
def fit_graphite(Vx, Dx, n=4):
    area = float(_TRAPZ(Dx, Vx)); lo, hi = Vx.min(), Vx.max()
    U0 = list(np.linspace(0.085, 0.21, n))
    def M(p): return sum(regsol_peak(Vx, p[j], p[n+j], p[2*n+j], p[3*n+j]) for j in range(n))+p[4*n]
    p0 = U0+[2.4*R*T]*n+[area/n]*n+[0.003]*n+[Dx.min()]
    lb = [lo]*n+[0.5*R*T]*n+[1e-6]*n+[3e-4]*n+[0]; ub = [hi]*n+[6*R*T]*n+[10*area]*n+[0.03]*n+[Dx.max()]
    p = _multi_fit(lambda p: M(p)-Dx, p0, lb, ub, 5)
    if p is None: return None
    return {'kind': 'regsol(두-상)', 'R2': round(_r2(Dx, M(p)), 4), 'pred': M(p),
            'OmRT': [round(p[n+j]/(R*T), 2) for j in range(n)], 'model': M, 'p': p, 'n': n}

def fit_silicon(Vx, Dx, m=3):
    area = float(_TRAPZ(Dx, Vx)); lo, hi = Vx.min(), Vx.max()
    U0 = list(np.linspace(lo+0.04, hi-0.05, m))
    def M(p): return sum(logistic_peak(Vx, p[j], p[m+j], p[2*m+j]) for j in range(m))+p[3*m]
    p0 = U0+[0.05]*m+[area/m]*m+[Dx.min()]
    lb = [lo]*m+[0.01]*m+[1e-6]*m+[0]; ub = [hi]*m+[0.2]*m+[10*area]*m+[Dx.max()]
    p = _multi_fit(lambda p: M(p)-Dx, p0, lb, ub, 5)
    if p is None: return None
    return {'kind': 'broad logistic(고용체)', 'R2': round(_r2(Dx, M(p)), 4), 'pred': M(p),
            'w_mV': [round(p[m+j]*1e3, 1) for j in range(m)], 'model': M, 'p': p, 'n': m}

def fit_blend(Vx, Dx, ng=4, ns=2):
    """중첩: 흑연 regsol(0.08–0.22) + Si broad logistic(0.25–0.50)."""
    area = float(_TRAPZ(Dx, Vx)); lo, hi = Vx.min(), Vx.max()
    Ug = list(np.linspace(0.085, 0.21, ng)); Us = [0.30, 0.45][:ns]
    def M(p):
        o = np.full(len(Vx), p[-1]); k = 0
        for j in range(ng): o = o+regsol_peak(Vx, p[k], p[k+1], p[k+2], p[k+3]); k += 4
        for j in range(ns): o = o+logistic_peak(Vx, p[k], p[k+1], p[k+2]); k += 3
        return o
    p0, lb, ub = [], [], []
    for u in Ug: p0 += [u, 2.4*R*T, 0.1*area, 0.003]; lb += [max(lo, u-0.03), 0.5*R*T, 1e-6, 3e-4]; ub += [u+0.03, 6*R*T, 10*area, 0.02]
    for u in Us: p0 += [u, 0.05, 0.15*area]; lb += [u-0.08, 0.02, 1e-6]; ub += [min(hi, u+0.08), 0.2, 10*area]
    p0 += [Dx.min()]; lb += [0]; ub += [Dx.max()]
    p = _multi_fit(lambda p: M(p)-Dx, p0, lb, ub, 5, nfev=12000)
    if p is None: return None
    return {'kind': '중첩(흑연 regsol + Si broad)', 'R2': round(_r2(Dx, M(p)), 4), 'pred': M(p),
            'OmRT_gr': [round(p[4*j+1]/(R*T), 2) for j in range(ng)], 'model': M, 'p': p, 'n': ng+ns}

FITTER = {'graphite': fit_graphite, 'silicon': fit_silicon, 'blend': fit_blend}

# ================= 소스 로딩 =================
def classify(name):
    k = name.lower()
    if 'sigr' in k or 'blend' in k: return 'blend'
    if 'graphite' in k or (k.startswith('gr') and 'sigr' not in k): return 'graphite'
    if 'silicon' in k or k.startswith('si'): return 'silicon'
    return 'unknown'
def proto_of(name):
    k = name.lower()
    if 'gitthold' in k: return 'GITT+hold'
    if 'gitt' in k: return 'GITT'
    if 'ocvhold' in k: return 'pOCV+hold'
    if k.endswith('.csv'): return 'pOCV(local)'
    return 'other'

def dqdv_from_csv(path):
    df = pd.read_csv(path)
    cv = next((c for c in df.columns if 'v' in c.lower()), df.columns[0])
    cq = next((c for c in df.columns if 'q' in c.lower()), df.columns[-1])
    return bd_dqdv(df[cv].to_numpy(float), df[cq].to_numpy(float))
def dqdv_from_parquet(path):
    df = pd.read_parquet(path)
    low = {c.lower(): c for c in df.columns}
    def find(*ks):
        for kk in ks:
            for lc, o in low.items():
                if kk in lc: return o
        return None
    cI, cV, cQ = find('current'), find('voltage'), find('capacity')
    if not (cV and cQ): return None, None
    V = df[cV].to_numpy(float); Q = df[cQ].to_numpy(float)*1000.0
    if cI:
        I = df[cI].to_numpy(float)
        name = os.path.basename(path).lower()
        if 'gitt' in name:  # 평형점 = rest(|I|~0) 끝
            rest = np.abs(I) < 1e-6; idx = np.where(rest)[0]
            if len(idx) > 5:
                segs = np.split(idx, np.where(np.diff(idx) > 1)[0]+1)
                pts = [(Q[s[-1]], V[s[-1]], np.sign(I[s[0]-1]) if s[0] > 0 else 0) for s in segs if len(s) >= 3]
                pts = [p for p in pts if p[2] > 0] or pts
                if len(pts) >= 8:
                    pa = np.array(pts); return bd_dqdv(pa[:, 1], pa[:, 0]-pa[:, 0].min())
        # delith 최장 세그(탈리튬 = I>0)
        d = (np.abs(I) > 1e-9) & (I > 0); ix = np.where(d)[0]
        if len(ix) > 25:
            s = max(np.split(ix, np.where(np.diff(ix) > 1)[0]+1), key=len); V, Q = V[s], Q[s]
    return bd_dqdv(V, Q-Q.min())

# 소스 목록: 로컬 CSV(항상) + parquet(있으면)
SRC = []
for key, mat in [("gr", "graphite"), ("si", "silicon"), ("sigr", "blend")]:
    p = os.path.join(REPO, "comp_v24", "sintef_data", f"{key}.csv")
    if os.path.exists(p): SRC.append((p, mat, 'csv'))
for p in sorted(glob.glob(os.path.join(RAW, "*.parquet"))):
    SRC.append((p, classify(os.path.basename(p)), 'parquet'))
log(f"소스 {len(SRC)}개 (CSV {sum(1 for s in SRC if s[2]=='csv')} · parquet {sum(1 for s in SRC if s[2]=='parquet')})")

records = {}
for path, mat, kind in SRC:
    name = os.path.basename(path)
    try:
        Vb, Db = (dqdv_from_csv if kind == 'csv' else dqdv_from_parquet)(path)
        if Vb is None: log(f"[SKIP] {name}: dQ/dV 실패"); continue
        lo, hi = WIN.get(mat, (0, 1)); m = (Vb >= lo) & (Vb <= hi)
        rec = {'mat': mat, 'proto': proto_of(name), 'V': Vb, 'D': Db, 'name': name}
        if m.sum() > 40 and mat in FITTER:
            Vx, Dx = Vb[m], Db[m]; fit = FITTER[mat](Vx, Dx)
            if fit: rec.update(fit=fit, Vx=Vx, Dx=Dx)
            log(f"[OK] {name}: {mat}/{rec['proto']} pts={len(Vb)} " + (f"R²={fit['R2']} ({fit['kind']})" if fit else "fit실패"))
        else:
            log(f"[OK] {name}: {mat}/{rec['proto']} pts={len(Vb)} (창밖·피팅생략)")
        records.setdefault(mat, []).append(rec)
    except Exception as e:
        log(f"[ERR] {name}: {e}\n{traceback.format_exc()[:300]}")

# ================= 소재별 플롯 =================
for mat, recs in records.items():
    if not recs: continue
    lo, hi = WIN.get(mat, (0, 1))
    fig, ax = plt.subplots(1, 2, figsize=(15, 5.6))
    for rec in recs:
        m = (rec['V'] >= lo) & (rec['V'] <= hi)
        ax[0].plot(rec['V'][m], rec['D'][m], lw=1.5, label=rec['proto'])
    ax[0].set_xlim(lo, hi); ax[0].set_xlabel('V vs Li'); ax[0].set_ylabel('dQ/dV (mAh/V)')
    ax[0].set_title(f'{mat} — 프로토콜별 dQ/dV'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
    best = None
    for r in recs:
        if 'fit' in r and (best is None or ('gitt' in r['proto'].lower() and 'gitt' not in best['proto'].lower())):
            best = r
    if best and 'fit' in best:
        f = best['fit']
        ax[1].plot(best['Vx'], best['Dx'], color='0.15', lw=2.4, label=f"data ({best['proto']})")
        ax[1].plot(best['Vx'], f['pred'], '-', color='crimson', lw=1.8, label=f"{f['kind']} R²={f['R2']}")
        ax[1].set_xlim(lo, hi); ax[1].set_xlabel('V vs Li'); ax[1].set_ylabel('dQ/dV (mAh/V)')
        extra = f" · Ω/RT={f.get('OmRT') or f.get('OmRT_gr') or f.get('w_mV','')}"
        ax[1].set_title(f'{mat} — 소재-정확 피팅{extra}'); ax[1].legend(fontsize=9); ax[1].grid(alpha=.3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, f"{mat}_dqdv.png"), dpi=130); plt.close(fig)
    log(f"saved {mat}_dqdv.png")

summary = {m: [{'proto': r['proto'], 'pts': int(len(r['V'])), 'fit_R2': r.get('fit', {}).get('R2'),
                'fit_kind': r.get('fit', {}).get('kind'),
                'OmRT': r.get('fit', {}).get('OmRT') or r.get('fit', {}).get('OmRT_gr')} for r in rs]
           for m, rs in records.items()}
json.dump(summary, open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
log("=== SUMMARY ===\n"+json.dumps(summary, ensure_ascii=False, indent=2))
log("DONE — out/{graphite,silicon,blend}_dqdv.png + summary.json")
