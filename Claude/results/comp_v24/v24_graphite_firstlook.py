# -*- coding: utf-8 -*-
"""v1.0.24 V2 first-look — 흑연 반쪽셀 실측(Zenodo 20086298 pseudo-OCV C/50) vs 문건 모델.
목적: 우리 식이 실측 dQ/dV 개형(피크 위치·폭·높이)을 설명하나 첫 육안 대조.
"""
import numpy as np, pandas as pd, importlib.util
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

# ---- 실측 로드 ----
GR = "/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr/gr_pocv_1d5628.parquet"
df = pd.read_parquet(GR)
t = df['Test Time / s'].to_numpy(); I = df['Current / A'].to_numpy()
V = df['Voltage / V'].to_numpy(); Qcum = df['Cumulative Capacity / Ah'].to_numpy()*1000.0  # mAh
step = df['Step Index / 1'].to_numpy()

# pseudo-OCV 스윕 구간: |I|>0 인 연속 구간 중 가장 긴 것(리튬화/탈리튬화 각 방향)
active = np.abs(I) > 1e-9
# 방향별 분리: 리튬화(graphite 충전, V↓) I<0 ; 탈리튬화 I>0
def longest_segment(mask):
    idx = np.where(mask)[0]
    if len(idx)==0: return None
    splits = np.where(np.diff(idx)>1)[0]
    segs = np.split(idx, splits+1)
    return max(segs, key=len)
seg_lith = longest_segment(active & (I<0))   # 리튬화
seg_deli = longest_segment(active & (I>0))   # 탈리튬화

def dqdv_of(seg, smooth=51):
    Vs = V[seg]; Qs = Qcum[seg]
    # V 단조 방향으로 정렬
    order = np.argsort(Vs); Vs=Vs[order]; Qs=Qs[order]
    # 중복 V 제거(평균)
    Vu, inv = np.unique(np.round(Vs,5), return_inverse=True)
    Qu = np.array([Qs[inv==k].mean() for k in range(len(Vu))])
    # 평활 미분 dQ/dV
    from numpy import gradient
    if len(Vu) > smooth:
        # 이동평균 평활
        k = np.ones(smooth)/smooth
        Qsm = np.convolve(Qu, k, mode='same')
    else: Qsm = Qu
    dqdv = np.gradient(Qsm, Vu)
    return Vu, np.abs(dqdv)

Vl, dl = dqdv_of(seg_lith) if seg_lith is not None else (None,None)
Vd, dd = dqdv_of(seg_deli) if seg_deli is not None else (None,None)
print(f"리튬화 스윕: {len(seg_lith) if seg_lith is not None else 0} pts, V {V[seg_lith].min():.3f}~{V[seg_lith].max():.3f}" if seg_lith is not None else "리튬화 없음")
print(f"탈리튬화 스윕: {len(seg_deli) if seg_deli is not None else 0} pts, V {V[seg_deli].min():.3f}~{V[seg_deli].max():.3f}" if seg_deli is not None else "탈리튬화 없음")

# ---- 문건 모델 ----
s = importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af = importlib.util.module_from_spec(s); s.loader.exec_module(af)
g = af.GraphiteAnodeDischargeDQDV(af.GRAPHITE_STAGING_LIT)
Vm = np.linspace(0.05, 0.30, 2000)
dqdv_model_eq = np.asarray(g.equilibrium(Vm, T=298.15), dtype=float)  # 평형(브로드닝 w_j)

# 스테이징 구간(0.05~0.30V) 실측 피크 위치 확인
def peaks_in(Vx, dx, lo=0.05, hi=0.30):
    m=(Vx>=lo)&(Vx<=hi); Vx=Vx[m]; dx=dx[m]
    if len(Vx)<5: return []
    # 국소 최대
    pk=[]
    for i in range(2,len(dx)-2):
        if dx[i]==max(dx[i-2:i+3]) and dx[i]>0.15*np.nanmax(dx):
            pk.append((round(float(Vx[i]),3), round(float(dx[i]),1)))
    return pk
print("실측 탈리튬화 피크(0.05-0.30V):", peaks_in(Vd, dd) if Vd is not None else "n/a")
print("문건 모델 GRAPHITE_STAGING_LIT U_j:", [t.get('U') for t in af.GRAPHITE_STAGING_LIT])

# ---- 그림: 실측 vs 모델 (스테이징 구간) ----
fig, ax = plt.subplots(1, 2, figsize=(14, 5.2))
# 좌: 전체 V-Q pseudo-OCV
ax[0].plot(Qcum*1000, V, '.', ms=0.5, alpha=0.4)
ax[0].set_xlabel('Cumulative Capacity / mAh'); ax[0].set_ylabel('Voltage / V'); ax[0].set_title('graphite half-cell pseudo-OCV (raw, Zenodo 20086298)'); ax[0].grid(alpha=.3)
# 우: dQ/dV 실측 vs 모델 (스테이징 0.05-0.30V, 각자 최대로 정규화)
if Vd is not None:
    m=(Vd>=0.05)&(Vd<=0.30)
    ax[1].plot(Vd[m], dd[m]/np.nanmax(dd[m]), label='real (delith, norm)', lw=1.5)
if Vl is not None:
    m=(Vl>=0.05)&(Vl<=0.30)
    ax[1].plot(Vl[m], dl[m]/np.nanmax(dl[m]), label='real (lith, norm)', lw=1.0, alpha=.6)
ax[1].plot(Vm, dqdv_model_eq/np.nanmax(dqdv_model_eq), '--', color='k', label='doc model eq (norm)', lw=1.5)
ax[1].set_xlabel('Voltage / V'); ax[1].set_ylabel('dQ/dV (normalized)'); ax[1].set_title('dQ/dV: real vs doc model (staging region)'); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
fig.tight_layout()
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24/gr_firstlook.png"
import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=120); print("saved", OUT)
