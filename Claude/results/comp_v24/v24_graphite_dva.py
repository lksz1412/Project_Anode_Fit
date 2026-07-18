# -*- coding: utf-8 -*-
"""v1.0.24 V2 보강 — DVA(dV/dQ) 관점 M-factor 제거 직접 시연.
사용자 M-factor 는 dV/dQ 피크 '높이' 불일치를 전위축 stretch 로 때운 것.
주장: dQ/dV 피크를 올바른 폭 w_j 로 맞추면(=문건 브로드닝식) dV/dQ 높이가 저절로 맞아 M 불필요.
  - real dV/dQ = d V / d(capacity)  (실측 V-Q 직접 미분)
  - model dV/dQ = 1 / (fitted equilibrium dQ/dV)  (M 없음)
  - 대조군: shipped default(w=RT/F) 의 dV/dQ — 과대폭 → dQ/dV 낮음 → dV/dQ 과대 (=사용자가 M 넣던 상황)
"""
import numpy as np, pandas as pd, importlib.util, json, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
_trapz = getattr(np, 'trapezoid', getattr(np, 'trapz', None))

SCRATCH = "/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUTDIR  = "/home/user/Project_Anode_Fit/Claude/results/comp_v24"
LO, HI = 0.05, 0.30
RT_F = 8.314*298.15/96485.0

s = importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af = importlib.util.module_from_spec(s); s.loader.exec_module(af)
DEFAULT = af.GRAPHITE_STAGING_LIT
fit = json.load(open(f"{OUTDIR}/gr_fit_result.json"))["cell_1d5628"]
U = np.array(fit["U_fit"]); w = np.array(fit["w_fit_mV"])/1000.0; Q = np.array(fit["Q_fit"]); Cbg = fit["Cbg_fit"]

# ---- 실측 delith V-Q ----
df = pd.read_parquet(f"{SCRATCH}/gr_pocv_1d5628.parquet")
I = df['Current / A'].to_numpy(); V = df['Voltage / V'].to_numpy()
Qc = df['Cumulative Capacity / Ah'].to_numpy()*1000.0
idx = np.where(np.abs(I)>1e-9)[0]; segs = np.split(idx, np.where(np.diff(idx)>1)[0]+1)
seg = max([sg for sg in segs if (I[sg]>0).all()], key=len)
Vs = V[seg]; Qs = Qc[seg]-Qc[seg][0]
o = np.argsort(Qs); Qs, Vs = Qs[o], Vs[o]           # capacity 단조 정렬
Qu, inv = np.unique(np.round(Qs,6), return_inverse=True)
Vu = np.array([Vs[inv==k].mean() for k in range(len(Qu))])
# capacity 균일격자 + savgol dV/dQ
dQg = 0.002
grid = np.arange(Qu.min(), Qu.max(), dQg)
Vg = np.interp(grid, Qu, Vu)
win = int(round(0.05/dQg)); win += (win%2==0)
dvdq_real = savgol_filter(Vg, win, 3, deriv=1, delta=dQg)   # V/mAh
mV_win = (Vg>=LO)&(Vg<=HI)

# ---- 모델 dV/dQ (fitted, M 없음) : dQ/dV(V) → dV/dQ, capacity(V) ----
def dqdv_of(trs, Cbg_):
    g = af.GraphiteAnodeDischargeDQDV(trs, Cbg=Cbg_)
    Vm = np.linspace(LO, HI, 4000)
    d = np.asarray(g.equilibrium(Vm, T=298.15), float)
    cap = np.concatenate([[0],np.cumsum((d[1:]+d[:-1])/2*np.diff(Vm))])  # capacity(V) mAh
    return Vm, d, cap
trs_fit = [{'U':float(U[j]),'w':float(w[j]),'Q':float(Q[j])} for j in range(len(U))]
Vm, d_fit, cap_fit = dqdv_of(trs_fit, Cbg)
dvdq_fit = 1.0/np.clip(d_fit, 1e-6, None)   # V/mAh (M 없음)

# 대조군: shipped default(w=RT/F), 동일 스테이징 용량으로 면적(=capacity) 정규화 후 역수
g0 = af.GraphiteAnodeDischargeDQDV(DEFAULT); d0 = np.asarray(g0.equilibrium(Vm,T=298.15),float)
area0 = float(_trapz(d0, Vm))
scale0 = (cap_fit[-1]/max(area0,1e-12))   # fit 과 동일 총용량으로 스케일(면적보존 → dQ/dV↔dV/dQ 공정 비교)
d0s = d0*scale0
dvdq_def = 1.0/np.clip(d0s, 1e-6, None)

# ---- 그림 ----
fig, ax = plt.subplots(1, 2, figsize=(14,5.4))
# 좌: dV/dQ vs V — real vs model-fit(no M) (전위축 직접 비교, capacity offset 회피)
Vreal = Vg[mV_win]; dvdq_r = dvdq_real[mV_win]*1000
keep = dvdq_r > 0                      # 플래토 경계 savgol 음수 overshoot 제거(물리: delith dV/dQ>0)
ax[0].plot(Vreal[keep], dvdq_r[keep], color='tab:blue', lw=1.4, label='real dV/dQ (delith)')
ax[0].plot(Vm, dvdq_fit*1000, '--', color='k', lw=1.6, label='doc model FIT dV/dQ (NO M)')
ax[0].set_ylim(0, 120)
ax[0].set_xlim(LO, HI)
ax[0].set_xlabel('Voltage / V'); ax[0].set_ylabel('dV/dQ / (mV/mAh)')
ax[0].set_title('DVA(dV/dQ) vs V: real vs doc-model FIT (no M-factor)'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
# 우: dV/dQ vs V — fit(no M) vs shipped-default(broad→inflated dV/dQ = M 넣던 상황)
ax[1].plot(Vm, dvdq_fit*1000, '--', color='k', lw=1.6, label='FIT dV/dQ (correct width, NO M)')
ax[1].plot(Vm, dvdq_def*1000, '-.', color='tab:red', lw=1.5, label='shipped default (w=RT/F, too broad)')
ax[1].set_ylim(0, 60)
ax[1].set_xlabel('Voltage / V'); ax[1].set_ylabel('dV/dQ / (mV/mAh)')
ax[1].set_title('why M existed: too-broad dQ/dV → inflated dV/dQ valleys'); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
fig.tight_layout()
OUT=f"{OUTDIR}/gr_dva_Mremoval.png"; fig.savefig(OUT, dpi=120); print("saved", OUT)

# 수치 요약
pk_real = np.nanmax(dvdq_real[mV_win]*1000)
print(f"real dV/dQ staging valley/peak span (mV/mAh): min {np.nanmin(dvdq_real[mV_win]*1000):.2f}  max {pk_real:.2f}")
print(f"model FIT dV/dQ span: min {np.nanmin(dvdq_fit*1000):.2f}  max {np.nanmax(dvdq_fit*1000):.2f}")
print(f"shipped default dV/dQ min (valley bottom, inflated): {np.nanmin(dvdq_def*1000):.2f} mV/mAh")
print(f"fit valley bottoms(at dQ/dV peaks) = 1/height: {[round(1000/h,3) for h in fit['peakheight_fit']]} mV/mAh")
