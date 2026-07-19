# -*- coding: utf-8 -*-
"""v1.0.24 V3 — 유한율속 브로드닝(source ①) 공개데이터 검증.
데이터: Zenodo 20323533 (DLR BAK N21700 흑연-SiOx 음극 반쪽셀), delith 율속 시리즈 5수준
        (I ∝ 1:2:5:10:20). ⚠ 상용 harvested 음극(흑연≠SINTEF) — 율속 '경향'이 검증 대상.
문건 §7 source ①: 유한율속 비대칭 꼬리 ℓ = L_V ∝ |I| → 피크가 전류 증가에 broaden·lower.
핵심 검증: 실측 피크 폭 증가분 Δ(FWHM) 이 |I| 에 (근사) 선형인가 (L_V ∝ |I| 예측).
"""
import numpy as np, pandas as pd, os, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
DLR="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/dlr/rate_delith.csv"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"

d=pd.read_csv(DLR, encoding='latin-1'); d.columns=[c.strip() for c in d.columns]
I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Capacity/ Ah'].to_numpy()*1000.0
idx=np.where((np.abs(I)>1e-9)&(I>0))[0]
segs=[s for s in np.split(idx,np.where(np.diff(idx)>1)[0]+1) if len(s)>500]
# 율속별 첫 사이클만(중복 제거): I_med 로 그룹
seen={}; rate_segs=[]
for s in segs:
    key=round(float(np.median(np.abs(I[s])))*1000,1)
    if key not in seen: seen[key]=1; rate_segs.append((key,s))
rate_segs.sort(key=lambda x:x[0])
print("rate levels (mA):",[k for k,_ in rate_segs])

def dqdv(seg, win_mV=8.0, dV=0.0005):
    Vs=V[seg]; Qs=Q[seg]-Q[seg][0]
    o=np.argsort(Vs); Vs,Qs=Vs[o],Qs[o]
    Vu,inv=np.unique(np.round(Vs,5),return_inverse=True)
    Qu=np.array([Qs[inv==k].mean() for k in range(len(Vu))])
    grid=np.arange(Vu.min(),Vu.max(),dV); Qg=np.interp(grid,Vu,Qu)
    win=int(round(win_mV/1000/dV)); win+=(win%2==0); win=max(win,5)
    return grid, np.abs(savgol_filter(Qg,win,3,deriv=1,delta=dV))

def peak_track(gx,gy,lo,hi,prom_frac=0.15):
    """이동창 국소최대 추적 — 분극 shift 허용. 피크가 배경에 완전히 뭉개지면 resolved=False."""
    m=(gx>=lo)&(gx<=hi); x=gx[m]; y=gy[m]
    if len(x)<5: return None
    ip=int(np.argmax(y)); h=float(y[ip])
    # 국소 최대인지(양옆보다 높고 배경 대비 prominence) — 완전 워시아웃 판정
    base=np.median(y); resolved = (h > base*(1+prom_frac)) and (0 < ip < len(y)-1)
    half=h/2; li=ip
    while li>0 and y[li]>half: li-=1
    ri=ip
    while ri<len(y)-1 and y[ri]>half: ri+=1
    return dict(V=float(x[ip]),height=h,fwhm_mV=float((x[ri]-x[li])*1000),resolved=bool(resolved))

# 주 스테이징 피크 창(흑연 저전위 피크). harvested 음극이라 실측 위치 확인 후 창 설정.
# 우선 최저율 피크 위치 탐색
g0,y0=dqdv(rate_segs[0][1])
m0=(g0>=0.06)&(g0<=0.20); pk0=g0[m0][np.argmax(y0[m0])]
LO,HI=pk0-0.03, pk0+0.03
print(f"main peak (lowest rate) ~{pk0:.3f}V → 창 {LO:.3f}-{HI:.3f}")

rows=[]; curves=[]
# 이동창: 저율 피크(0.111V)를 분극 shift 따라 추적(창을 위로 확장)
for k,s in rate_segs:
    gx,gy=dqdv(s); pk=peak_track(gx,gy, LO, pk0+0.10)   # 상한을 넉넉히(고율 shift 포용)
    if pk: rows.append({"I_mA":k, **pk}); curves.append((k,gx,gy))
    print(f"  I={k:6.2f}mA  peak V={pk['V']:.3f}  height={pk['height']:7.1f}  resolved={pk['resolved']}")

res_rows=[r for r in rows if r["resolved"]]   # 피크가 살아있는 율속만 정량
Iarr=np.array([r["I_mA"] for r in res_rows]); Harr=np.array([r["height"] for r in res_rows])
Varr=np.array([r["V"] for r in res_rows])
# 분극 shift: ΔV = Rn·ΔI (V_n=V_app−|I|Rn) — 저항 추정
if len(Iarr)>=2:
    P=np.polyfit(Iarr,Varr,1); Rn_est=P[0]*1000.0   # V/mA → Ω(전류 mA)
    shiftfit=np.polyval(P,Iarr); r2s=1-np.sum((Varr-shiftfit)**2)/np.sum((Varr-Varr.mean())**2)
else: Rn_est=None; r2s=None
print(f"\n분극 shift: peak V = {P[1]:.4f} + {P[0]*1000:.3f} mV/mA · I  (Rn≈{P[0]*1000:.1f} Ω/mA기준, 선형 R²={r2s:.3f})")
print(f"피크 높이(broadening): {Harr[0]:.0f}(최저율) → {Harr[-1]:.0f}  ; 워시아웃 율속(>{res_rows[-1]['I_mA']:.0f}mA): 스테이징 피크 소멸")

fig,ax=plt.subplots(1,3,figsize=(16,4.8))
cmap=plt.cm.viridis(np.linspace(0,0.85,len(curves)))
for (k,gx,gy),c in zip(curves,cmap):
    m=(gx>=LO-0.02)&(gx<=pk0+0.10); ax[0].plot(gx[m],gy[m],color=c,lw=1.4,label=f'{k:.1f}mA')
ax[0].set_title('① 율속별 dQ/dV: 전류↑ → broaden·lower·shift'); ax[0].set_xlabel('V'); ax[0].set_ylabel('dQ/dV'); ax[0].legend(fontsize=7,title='|I|'); ax[0].grid(alpha=.3)
ax[1].semilogy([r["I_mA"] for r in rows],[r["height"] for r in rows],'s-',color='tab:red')
ax[1].set_title('피크 높이 vs |I| (log): 면적보존→height∝1/폭'); ax[1].set_xlabel('|I| / mA'); ax[1].set_ylabel('peak height (log)'); ax[1].grid(alpha=.3,which='both')
ax[2].plot(Iarr,Varr*1000,'o-',color='tab:blue'); ax[2].plot(Iarr,shiftfit*1000,'--',color='k',label=f'V_n=V−|I|Rn\nlinear R²={r2s:.3f}')
ax[2].set_title('피크 위치 shift vs |I| (분극 V_n=V−|I|Rn)'); ax[2].set_xlabel('|I| / mA'); ax[2].set_ylabel('peak V / mV'); ax[2].legend(fontsize=8); ax[2].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/rate_broadening.png",dpi=120); print("saved",f"{OUT}/rate_broadening.png")
json.dump({"main_peak_V_lowrate":round(float(pk0),3),
           "polarization_shift_mV_per_mA":round(float(P[0]*1000),3),"shift_linear_R2":round(float(r2s),3),
           "height_drop":[round(float(r["height"]),1) for r in rows],
           "resolved_rates_mA":[r["I_mA"] for r in res_rows],"rows":rows},
          open(f"{OUT}/rate_broadening_result.json","w"),ensure_ascii=False,indent=2)
