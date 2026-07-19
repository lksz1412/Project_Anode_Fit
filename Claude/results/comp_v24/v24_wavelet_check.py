# -*- coding: utf-8 -*-
"""웨이블릿 denoise 적용 검증 — 사용자 질문("BDD 핵심=웨이블릿 denoise, 잘 적용됐나?").
(1) 실측 흑연: denoise ON/OFF 피크 높이·위치 보존 확인(soft-threshold 가 tall 피크 안 깎나).
(2) 합성 노이즈: 알려진 피크+노이즈 → BDD(웨이블릿 포함) vs 단일 savgol 회복력 정량(노이즈일 때 진가).
"""
import numpy as np, pandas as pd, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"; OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"

# (1) 실측 흑연 — denoise ON/OFF 피크 보존
d=pd.read_parquet(f"{SC}/gr_pocv_1d5628.parquet"); I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
idx=np.where((np.abs(I)>1e-9)&(I>0))[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
Vs,Qs=V[seg],Q[seg]-Q[seg][0]
gx0,gy0=bdd.dqdv_grid_bdd(Vs,Qs,denoise_deriv=0.0)   # 웨이블릿 OFF
gx1,gy1=bdd.dqdv_grid_bdd(Vs,Qs,denoise_deriv=0.4)   # 웨이블릿 ON(기본)
def peaks(gx,gy):
    out={}
    for lo,hi,n in [(0.095,0.115,"0.10"),(0.135,0.148,"0.14"),(0.22,0.235,"0.22")]:
        m=(gx>=lo)&(gx<=hi); out[n]=round(float(np.nanmax(gy[m])),1)
    return out
print("실측 흑연 피크 높이 — 웨이블릿 OFF:",peaks(gx0,gy0)," ON:",peaks(gx1,gy1))

# (2) 합성: 알려진 dQ/dV(로지스틱-미분 3피크) + 노이즈 → 회복
np.random.seed=None
Vg=np.arange(0.05,0.30,0.0005)
def lg(V,U,w): z=(V-U)/w; return np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)))
truth=np.zeros_like(Vg)
for U,w,A in [(0.104,0.001,0.2),(0.1415,0.0011,0.13),(0.227,0.0016,0.03)]:
    s=lg(Vg,U,w); truth+=A*s*(1-s)/w*0.001
truth=truth/truth.max()*200  # dQ/dV 스케일
# V-Q 역산(적분) + V에 노이즈 주입(사용자 '기울기' 문제 모사)
Qtrue=np.concatenate([[0],np.cumsum((truth[1:]+truth[:-1])/2*np.diff(Vg))])
det=np.array([((i*7919)%1000-500) for i in range(len(Vg))])/500.0
for scale,tag in [(0.002,"noise2mV"),(0.005,"noise5mV")]:
    Vn=Vg+det*scale               # V 에 ±2/5mV 노이즈(비단조 wobble 유발)
    # BDD(웨이블릿 포함)
    gxb,gyb=bdd.dqdv_grid_bdd(Vn,Qtrue,denoise_deriv=0.5)
    # 단일 savgol(기존): V정렬·보간·savgol미분
    o=np.argsort(Vn); Vso,Qso=Vn[o],Qtrue[o]; Vu,iv=np.unique(np.round(Vso,6),return_inverse=True)
    Qu=np.array([Qso[iv==k].mean() for k in range(len(Vu))]); grid=np.arange(Vu.min(),Vu.max(),0.0005); Qgg=np.interp(grid,Vu,Qu)
    ss=np.abs(savgol_filter(Qgg,11,3,deriv=1,delta=0.0005))
    # 오차(truth 대비, 공통격자 보간)
    tb=np.interp(gxb,Vg,truth); es=np.interp(grid,Vg,truth)
    rmse_b=float(np.sqrt(np.nanmean((gyb-tb)**2))); rmse_s=float(np.sqrt(np.nanmean((ss-es)**2)))
    print(f"[{tag}] RMSE(truth대비)  BDD(웨이블릿)={rmse_b:.2f}  단일savgol={rmse_s:.2f}  → BDD가 {rmse_s/rmse_b:.2f}× 우수" if rmse_b>0 else "")

# 그림
fig,ax=plt.subplots(1,2,figsize=(15,5.2))
m=(gx0>=0.08)&(gx0<=0.25)
ax[0].plot(gx0[m],gy0[m],'--',color='tab:orange',lw=1.1,label='웨이블릿 OFF')
m1=(gx1>=0.08)&(gx1<=0.25); ax[0].plot(gx1[m1],gy1[m1],'-',color='k',lw=1.3,label='웨이블릿 ON(기본0.4)')
ax[0].set_title('실측 흑연: 웨이블릿 denoise ON/OFF (피크 보존 확인)'); ax[0].set_xlabel('V'); ax[0].set_ylabel('dQ/dV'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
# 합성 noise5mV 회복 비교
Vn=Vg+det*0.005; gxb,gyb=bdd.dqdv_grid_bdd(Vn,Qtrue,denoise_deriv=0.5)
o=np.argsort(Vn); Vso,Qso=Vn[o],Qtrue[o]; Vu,iv=np.unique(np.round(Vso,6),return_inverse=True)
Qu=np.array([Qso[iv==k].mean() for k in range(len(Vu))]); grid=np.arange(Vu.min(),Vu.max(),0.0005); Qgg=np.interp(grid,Vu,Qu); ss=np.abs(savgol_filter(Qgg,11,3,deriv=1,delta=0.0005))
ax[1].plot(Vg,truth,color='tab:green',lw=2,alpha=.5,label='truth(알려진 dQ/dV)')
ax[1].plot(grid,ss,'--',color='tab:red',lw=.9,label='단일 savgol(노이즈 취약)')
ax[1].plot(gxb,gyb,'-',color='k',lw=1.2,label='BDD(웨이블릿 포함)')
ax[1].set_xlim(0.08,0.25); ax[1].set_title('합성 노이즈(±5mV V wobble) 회복: BDD vs savgol'); ax[1].set_xlabel('V'); ax[1].set_ylabel('dQ/dV'); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/wavelet_denoise_check.png",dpi=120); print("saved wavelet_denoise_check.png")
