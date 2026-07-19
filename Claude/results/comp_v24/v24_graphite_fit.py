# -*- coding: utf-8 -*-
"""v1.0.24 V2 — 흑연 반쪽셀 실측(Zenodo 20086298 pseudo-OCV, ~C/50 상온) vs 문건 모델 정량 피팅.

핵심 검증(= M-factor 제거 근거):
  문건 §7 브로드닝식은 평형 peak 를 sum_j Q_j·ξ(1-ξ)/w_j (ξ=logistic((V-U_j)/w_j)) 로 쓴다.
  peak 높이 = 0.25·Q_j/w_j (면적 = Q_j 보존). 즉 '높이'는 폭 w_j 와 용량 Q_j 로 결정되지
  전위축 stretch(M) 로 만드는 값이 아니다. 실측 dQ/dV 를 단일 정합 파라미터셋(U_j,w_j,Q_j)으로
  재현할 수 있으면 → dV/dQ 높이 불일치는 브로드닝으로 설명됨 → M 불필요.

절차:
  1) 실측 parquet 2셀 로드, 리튬화(I<0)·탈리튬화(I>0) pseudo-OCV 스윕 분리.
  2) V 균일격자 재보간 후 Savitzky-Golay 미분으로 dQ/dV(V) 산출(깨끗한 미분).
  3) 문건의 '출하 코드'(Anode_Fit_v1.0.23.py) GraphiteAnodeDischargeDQDV.equilibrium 을
     그대로 호출해 4전이 (U_j,w_j,Q_j)+Cbg 를 curve_fit(비선형 최소제곱)으로 실측에 맞춘다.
     (transitions 에 'n' 미부여·'w'만 부여 → _width 가 정확히 w_j 반환 = 문건이 말하는 자유폭.)
  4) 기본(shipped GRAPHITE_STAGING_LIT, n=1 → w=RT/F≈25.7mV, 과대폭) vs 피팅 결과 대조.
  5) 피팅 w_j 가 RT/F 미만(두-상 sharpening)인지, 4피크 위치·상대높이가 재현되는지 보고.
"""
import numpy as np, pandas as pd, importlib.util, os, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
_trapz = getattr(np, 'trapezoid', getattr(np, 'trapz', None))  # numpy 2.x: trapz→trapezoid

SCRATCH = "/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUTDIR  = "/home/user/Project_Anode_Fit/Claude/results/comp_v24"
os.makedirs(OUTDIR, exist_ok=True)
CELLS = {"cell_1d5628": f"{SCRATCH}/gr_pocv_1d5628.parquet",
         "cell_4ccc47": f"{SCRATCH}/gr_pocv_4ccc47.parquet"}
LO, HI = 0.05, 0.30          # 스테이징 창 [V]
RT_F_298 = 8.314*298.15/96485.0  # RT/F @298.15K = 0.02569 V

# ---- 문건 출하 코드 로드 ----
s = importlib.util.spec_from_file_location(
    "af", "/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af = importlib.util.module_from_spec(s); s.loader.exec_module(af)
DEFAULT = af.GRAPHITE_STAGING_LIT
U0 = [tr['U'] for tr in DEFAULT]            # [0.210,0.140,0.120,0.085]
NTR = len(DEFAULT)

# ---- 실측 dQ/dV 추출(균일격자 + Savitzky-Golay) ----
def longest_segment(mask):
    idx = np.where(mask)[0]
    if len(idx) == 0: return None
    segs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    return max(segs, key=len)

def dqdv_savgol(seg, V, Qcum_mAh, dV=0.0005, win_mV=5.0, poly=3):
    """세그먼트 → 균일 V격자 위 |dQ/dV|(mAh/V), Savitzky-Golay 1차 미분."""
    Vs = V[seg].astype(float); Qs = Qcum_mAh[seg].astype(float)
    Qs = Qs - Qs[0]
    order = np.argsort(Vs); Vs, Qs = Vs[order], Qs[order]
    # 중복 V 평균(단조 격자 확보)
    Vu, inv = np.unique(np.round(Vs, 6), return_inverse=True)
    Qu = np.array([Qs[inv == k].mean() for k in range(len(Vu))])
    if len(Vu) < 10: return None, None
    grid = np.arange(Vu.min(), Vu.max(), dV)
    Qg = np.interp(grid, Vu, Qu)
    win = int(round(win_mV/1000.0/dV));  win += (win % 2 == 0)  # 홀수
    win = max(win, poly+2 + ((poly) % 2 == 0))
    if win >= len(Qg): win = len(Qg) - 1 - ((len(Qg)-1) % 2 == 0)
    if win < poly+2: return grid, np.abs(np.gradient(Qg, dV))
    dqdv = savgol_filter(Qg, win, poly, deriv=1, delta=dV)
    return grid, np.abs(dqdv)

# ---- 문건 모델(출하 코드) 예측 함수 — curve_fit 대상 ----
def model_equilibrium(V, *p):
    """p = [U1..U4, w1..w4, Q1..Q4, Cbg] → 출하 equilibrium() 호출."""
    U = p[0:NTR]; w = p[NTR:2*NTR]; Q = p[2*NTR:3*NTR]; Cbg = p[3*NTR]
    trs = [{'U': float(U[j]), 'w': float(w[j]), 'Q': float(Q[j])} for j in range(NTR)]
    g = af.GraphiteAnodeDischargeDQDV(trs, Cbg=float(Cbg))
    return np.asarray(g.equilibrium(np.asarray(V, float), T=298.15), float)

def fit_cell(name, path):
    df = pd.read_parquet(path)
    I = df['Current / A'].to_numpy()
    V = df['Voltage / V'].to_numpy()
    Qcum = df['Cumulative Capacity / Ah'].to_numpy()*1000.0  # mAh
    active = np.abs(I) > 1e-9
    seg_lith = longest_segment(active & (I < 0))
    seg_deli = longest_segment(active & (I > 0))
    out = {"name": name}
    grids = {}
    for tag, seg in (("delith", seg_deli), ("lith", seg_lith)):
        if seg is None: continue
        gV, gd = dqdv_savgol(seg, V, Qcum)
        if gV is None: continue
        grids[tag] = (gV, gd)
        out[f"{tag}_Vrange"] = [float(V[seg].min()), float(V[seg].max())]
        out[f"{tag}_npts"] = int(len(seg))
    # 피팅은 탈리튬화 기준(위 코인셀 관례와 동일 방향; 스테이징 창)
    gV, gd = grids["delith"]
    m = (gV >= LO) & (gV <= HI)
    Vx, Dx = gV[m], gd[m]
    # 실측 스테이징 총면적(용량) → Q 초기값 스케일
    area = float(_trapz(Dx, Vx))
    Qsum0 = sum(tr['Q'] for tr in DEFAULT)
    Qscale = area/Qsum0 if Qsum0 > 0 else area
    p0  = list(U0) + [0.006]*NTR + [tr['Q']*Qscale for tr in DEFAULT] + [max(Dx.min(), 1e-6)]
    lob = [LO]*NTR + [0.0008]*NTR + [1e-6]*NTR + [0.0]   # w floor 0.8mV (FWHM~2.8mV); 실측 최소 FWHM~3.5mV
    hib = [HI]*NTR + [0.060]*NTR + [10*area]*NTR + [max(Dx)*1.0]
    try:
        popt, _ = curve_fit(model_equilibrium, Vx, Dx, p0=p0, bounds=(lob, hib), maxfev=200000)
    except Exception as e:
        out["fit_error"] = str(e); return out, grids, (Vx, Dx, None, None)
    pred = model_equilibrium(Vx, *popt)
    ss_res = float(np.sum((Dx-pred)**2)); ss_tot = float(np.sum((Dx-Dx.mean())**2))
    r2 = 1.0 - ss_res/ss_tot if ss_tot > 0 else float('nan')
    Uf = popt[0:NTR]; wf = popt[NTR:2*NTR]; Qf = popt[2*NTR:3*NTR]; Cbgf = popt[3*NTR]
    # 피크 높이(중심) = 0.25 Q/w
    hpk = [0.25*Qf[j]/wf[j] for j in range(NTR)]
    out.update({
        "area_mAh": area, "R2": r2,
        "U_fit": [round(float(x),4) for x in Uf],
        "w_fit_mV": [round(float(x)*1000,2) for x in wf],
        "w_over_RTF": [round(float(x)/RT_F_298,3) for x in wf],
        "Q_fit": [round(float(x),4) for x in Qf],
        "peakheight_fit": [round(float(x),1) for x in hpk],
        "Cbg_fit": round(float(Cbgf),3),
        "RT_F_mV": round(RT_F_298*1000,2),
    })
    return out, grids, (Vx, Dx, pred, popt)

# ---- 실행 ----
results = {}; panels = {}
for name, path in CELLS.items():
    res, grids, fitpack = fit_cell(name, path)
    results[name] = res; panels[name] = (grids, fitpack)
    print(f"\n=== {name} ===")
    print(json.dumps(res, ensure_ascii=False, indent=2))

# ---- 그림: 각 셀 real vs fitted(+ shipped-default) ----
fig, axes = plt.subplots(len(CELLS), 2, figsize=(14, 5.4*len(CELLS)))
if len(CELLS) == 1: axes = axes.reshape(1, 2)
for r, (name, (grids, fitpack)) in enumerate(panels.items()):
    Vx, Dx, pred, popt = fitpack
    ax = axes[r, 0]
    # 좌: real delith+lith dQ/dV + fitted
    if "delith" in grids:
        gV, gd = grids["delith"]; mm = (gV >= LO) & (gV <= HI)
        ax.plot(gV[mm], gd[mm], color='tab:blue', lw=1.6, label='real delith (savgol)')
    if "lith" in grids:
        gV, gd = grids["lith"]; mm = (gV >= LO) & (gV <= HI)
        ax.plot(gV[mm], gd[mm], color='tab:cyan', lw=1.0, alpha=.6, label='real lith (savgol)')
    if pred is not None:
        Vfine = np.arange(LO, HI, 0.00002)   # 고해상 0.02mV — 매끄러운 모델선(각짐=그림격자 아티팩트 회피)
        ax.plot(Vfine, model_equilibrium(Vfine, *popt), '--', color='k', lw=1.6,
                label=f'doc model FIT (R²={results[name]["R2"]:.3f})')
        for j, Uj in enumerate(results[name]["U_fit"]):
            ax.axvline(Uj, color='gray', ls=':', lw=0.7)
    ax.set_xlabel('Voltage / V'); ax.set_ylabel('dQ/dV / (mAh/V)')
    ax.set_title(f'{name}: real vs doc-model FIT (staging)'); ax.legend(fontsize=8); ax.grid(alpha=.3)
    # 우: shipped-default(n=1, w=RT/F) overlay(면적 정규화) — 과대폭 시연
    ax2 = axes[r, 1]
    if pred is not None:
        gdef = af.GraphiteAnodeDischargeDQDV(DEFAULT)
        Vm = np.linspace(LO, HI, 1500)
        ddef = np.asarray(gdef.equilibrium(Vm, T=298.15), float)
        area_real = results[name]["area_mAh"]
        ddef_scaled = ddef * (area_real / max(_trapz(ddef, Vm), 1e-12))
        ax2.plot(Vx, Dx, color='tab:blue', lw=1.6, label='real delith')
        ax2.plot(Vm, ddef_scaled, '-.', color='tab:red', lw=1.6,
                 label='shipped default (n=1, w=RT/F, area-norm)')
        ax2.plot(Vx, pred, '--', color='k', lw=1.4, label='doc model FIT')
    ax2.set_xlabel('Voltage / V'); ax2.set_ylabel('dQ/dV / (mAh/V)')
    ax2.set_title(f'{name}: shipped-default(too broad) vs FIT'); ax2.legend(fontsize=8); ax2.grid(alpha=.3)
fig.tight_layout()
OUT = f"{OUTDIR}/gr_fit.png"
fig.savefig(OUT, dpi=120); print("\nsaved", OUT)
with open(f"{OUTDIR}/gr_fit_result.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("saved", f"{OUTDIR}/gr_fit_result.json")
