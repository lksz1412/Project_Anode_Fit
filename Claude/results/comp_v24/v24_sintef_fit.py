# -*- coding: utf-8 -*-
"""v1.0.24 최종 코드 — SINTEF 공개 실측(Zenodo 20086298, CC-BY-4.0) 흑연·실리콘·흑연+Si 블렌드 피팅.
   ★[핵심] @3/@5 반영식을 각자의 실제 코드 경로로 태운다:
     - 흑연 = @5 XRD 5-feature staging(stage-2L 분리: 3↔2L 0.132 · 2L↔2 0.116) — 로지스틱 커널(코드 상수
       GRAPHITE_STAGING_XRD_v1024 가 실제 쓰는 경로; 'kernel':'regsol' 없음). baseline=4-feature 와 대조.
     - Si = @3 정칙용액(Frumkin) 'kernel':'regsol' — a-Si 고용체(Ω<2RT)+c-Li15Si4 두-상(Ω>2RT), §7/@3 분류 부과.
   대조군=기본 로지스틱(bit-exact baseline). 반쪽셀 pOCV(C/50, RT). dQ/dV=BDD 스무딩. 피팅=least_squares(강건·유계).
   데이터=리포 sintef_data/ CSV(영구보존)."""
import numpy as np, importlib.util, pandas as pd, os, warnings
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.optimize import least_squares
_trapz=getattr(np,'trapezoid',None) or getattr(np,'trapz',None)
ROOT="/home/user/Project_Anode_Fit/Claude"; DOC=f"{ROOT}/docs/v1.0.24"; CV=f"{ROOT}/results/comp_v24"
DATA=f"{CV}/sintef_data"; SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/sintef"
R_GAS=8.314462618; F_CONST=96485.33212; RT=R_GAS*298.15; TWORT=2*RT   # 2RT≈4958 J/mol = Ω/RT 2 경계
def load(n,p): s=importlib.util.spec_from_file_location(n,p); mm=importlib.util.module_from_spec(s); s.loader.exec_module(mm); return mm
m=load("af",f"{DOC}/Anode_Fit_v1.0.24.py"); bdd=load("bdd",f"{CV}/bdd_smoothing.py")
GR=m.GraphiteAnodeDischargeDQDV
m._REGSOL_XG=np.linspace(1e-4,1.0-1e-4,300)   # regsol 내부격자(출하 1200→300; 형상·R² 무영향)
MAXPTS=280; MAXNFEV=6000                        # 해상도 유지(gr_5f stage-2L 분해) + 유계반복(블렌드 완주보장)

def load_delith(k):
    csv=f"{DATA}/{k}.csv"
    if os.path.exists(csv):
        d=pd.read_csv(csv); return d['V_vs_Li'].to_numpy(), d['Q_mAh'].to_numpy()
    d=pd.read_parquet(f"{SC}/{k}.parquet")
    I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000.0
    idx=np.where(I>1e-9)[0]; seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    return V[seg], Q[seg]-Q[seg][0]

def dqdv(V,Q,win,dvv):
    gx,gy=bdd.dqdv_grid_bdd(V,Q,dV=dvv); gy=np.abs(gy)
    mk=(gx>=win[0])&(gx<=win[1]); return gx[mk],gy[mk]

# ---- 전이 dict 빌더: 흑연 gk·Si sk 각각 'logistic' or 'regsol' ----
def build(p,NG,NS,gk,sk):
    gr=[];si=[];i=0
    for _ in range(NG):
        if gk=='regsol': gr.append({'U':p[i],'Omega':p[i+1],'Q':p[i+2],'w':p[i+3],'kernel':'regsol'}); i+=4
        else:            gr.append({'U':p[i],'w':p[i+1],'Q':p[i+2]}); i+=3
    for _ in range(NS):
        if sk=='regsol': si.append({'U':p[i],'Omega':p[i+1],'Q':p[i+2],'w':p[i+3],'kernel':'regsol'}); i+=4
        else:            si.append({'U':p[i],'w':p[i+1],'Q':p[i+2]}); i+=3
    return gr,si,p[i]

def modelf(NG,NS,gk,sk):
    def f(V,p):
        gr,si,Cbg=build(p,NG,NS,gk,sk); Va=np.asarray(V,float)
        out=np.asarray(GR(gr,Cbg=float(Cbg)).equilibrium(Va,298.15),float)
        if si: out=out+np.asarray(GR(si,Cbg=0.0).equilibrium(Va,298.15),float)
        return out
    return f

def pack(kernel,seed,area):
    """logistic seed=(U,w,Qf) · regsol seed=(U,Om,Qf,w,OmLo,OmHi). U 는 ±0.06 로 자리 고정(전이 붕괴 방지)."""
    p0=[];lo=[];hi=[]
    for s in seed:
        if kernel=='regsol':
            U,Om,Qf,w,OmLo,OmHi=s; p0+=[U,Om,Qf*area,w]; lo+=[max(0.03,U-0.06),OmLo,1e-6,0.0008]; hi+=[U+0.06,OmHi,10*area,0.09]
        else:
            U,w,Qf=s; p0+=[U,w,Qf*area]; lo+=[max(0.03,U-0.06),0.0008,1e-6]; hi+=[U+0.06,0.09,10*area]
    return p0,lo,hi

def fit(gk,sk,k,win,dvv,gr_seed,si_seed,mp=MAXPTS,mf=MAXNFEV):
    V,Q=load_delith(k); Vx,Dx=dqdv(V,Q,win,dvv)
    if len(Vx)>mp:
        sel=np.linspace(0,len(Vx)-1,mp).round().astype(int); Vx,Dx=Vx[sel],Dx[sel]
    NG,NS=len(gr_seed),len(si_seed); area=float(_trapz(Dx,Vx))
    pg,lg,hg=pack(gk,gr_seed,area); ps,ls,hs=pack(sk,si_seed,area)
    p0=pg+ps+[max(Dx.min(),1e-6)]; lo=lg+ls+[0.0]; hi=hg+hs+[max(Dx)+1e-9]
    fn=modelf(NG,NS,gk,sk)
    res=least_squares(lambda p: fn(Vx,p)-Dx, p0, bounds=(lo,hi), max_nfev=mf, ftol=1e-10, xtol=1e-10, gtol=1e-10)
    popt=res.x; pred=fn(Vx,popt); r2=1.0-np.sum((Dx-pred)**2)/np.sum((Dx-Dx.mean())**2)
    gr,si,Cbg=build(popt,NG,NS,gk,sk)
    trs=[]; Qg=Qs=0.0
    for t in gr: Qg+=t['Q']; trs.append(('gr',t['U'],(t['Omega']/RT if 'Omega' in t else None),t['Q']))
    for t in si: Qs+=t['Q']; trs.append(('si',t['U'],(t['Omega']/RT if 'Omega' in t else None),t['Q']))
    grc=np.asarray(GR(gr,Cbg=float(Cbg)).equilibrium(Vx,298.15),float) if NG else None
    sic=np.asarray(GR(si,Cbg=0.0).equilibrium(Vx,298.15),float) if NS else None
    fSi=Qs/(Qg+Qs) if (Qg+Qs)>0 else None
    return dict(Vx=Vx,Dx=Dx,pred=pred,r2=float(r2),NG=NG,NS=NS,npts=len(Vx),grc=grc,sic=sic,fSi=fSi,trs=trs)

# ---- 시드 ----
# 흑연 로지스틱: baseline 4-feature vs @5 5-feature(stage-2L 분리). (U,w,Qf)
GR4=[(0.088,0.004,0.30),(0.120,0.006,0.25),(0.142,0.016,0.30),(0.210,0.006,0.10)]
GR5=[(0.088,0.004,0.30),(0.116,0.006,0.18),(0.132,0.009,0.15),(0.170,0.020,0.10),(0.210,0.006,0.06)]
# Si: baseline 로지스틱 (U,w,Qf) vs @3 regsol §7/@3 분류부과 (U,Om,Qf,w,OmLo,OmHi)
SI3L=[(0.28,0.050,0.40),(0.43,0.006,0.15),(0.47,0.050,0.30)]
SI3R=[(0.28,1500,0.40,0.050,200,4900),(0.43,8000,0.15,0.006,4958,20000),(0.47,1500,0.30,0.050,200,4900)]

import time
R={}; T0=time.time()
def go(key,*a,**kw):
    R[key]=fit(*a,**kw); r=R[key]
    print(f"[{time.time()-T0:5.1f}s] {key:6s} R²={r['r2']:.4f} npts={r['npts']} (gr={a[0]},si={a[1]})",flush=True)
go('gr_bl','logistic','logistic','gr',  (0.086,0.30),0.0005, GR4, [])   # 흑연 baseline(4-feature)
go('gr_5f','logistic','logistic','gr',  (0.086,0.30),0.0005, GR5, [])   # 흑연 @5(5-feature stage-2L)
go('si_bl','logistic','logistic','si',  (0.06,0.55), 0.001,  [],  SI3L) # Si baseline(로지스틱)
go('si_fr','logistic','regsol',  'si',  (0.06,0.55), 0.001,  [],  SI3R) # Si @3(Frumkin regsol)
go('sg_bl','logistic','logistic','sigr',(0.05,0.52), 0.0007, GR4, SI3L) # 블렌드 baseline
go('sg_35','logistic','regsol',  'sigr',(0.05,0.52), 0.0007, GR5, SI3R, mp=200, mf=2500) # 블렌드 @3/@5(유계·경량)

# ---- 그림: 상단=@3/@5 반영식 피팅, 하단=baseline↔@3/@5 R² 대조 ----
fig=plt.figure(figsize=(18,9)); gs=fig.add_gridspec(2,3,height_ratios=[2.2,1.0])
def draw(a,title,r,showcomp=False):
    a.plot(r['Vx'],r['Dx'],'o',ms=2.0,color='0.4',alpha=.5,label=f"실측 dQ/dV (BDD, {r['npts']}점)")
    a.plot(r['Vx'],r['pred'],'-',color='tab:red',lw=2,label=f"@3/@5 반영식 피팅 (R²={r['r2']:.4f})")
    if showcomp and r['grc'] is not None:
        a.plot(r['Vx'],r['grc'],'--',color='tab:blue',lw=1.1,label='흑연 성분(@5 5-feature)')
        a.plot(r['Vx'],r['sic'],':',color='tab:green',lw=1.5,label=f"Si 성분(@3 Frumkin, f_Si={r['fSi']:.2f})")
    a.set_title(title,fontsize=10); a.set_xlabel('V vs Li'); a.set_ylabel('dQ/dV'); a.legend(fontsize=7.5); a.grid(alpha=.3)
axA=[fig.add_subplot(gs[0,j]) for j in range(3)]; axB=[fig.add_subplot(gs[1,j]) for j in range(3)]
draw(axA[0],'(1) 흑연 반쪽셀 — @5 XRD 5-feature staging(로지스틱)\nSINTEF Zenodo 20086298(실측 pOCV C/50)',R['gr_5f'])
draw(axA[1],'(2) 실리콘 반쪽셀 — @3 Frumkin regsol\n(a-Si 고용체 Ω<2RT + c-Li15Si4 두-상 Ω>2RT)',R['si_fr'])
draw(axA[2],'(3) 흑연+Si 블렌드 — @5 흑연 + @3 Si 가산',R['sg_35'],showcomp=True)
cmp=[('흑연',[('baseline\n4-feature','gr_bl'),('@5\n5-feature','gr_5f')]),
     ('실리콘',[('baseline\n로지스틱','si_bl'),('@3\nFrumkin','si_fr')]),
     ('블렌드',[('baseline','sg_bl'),('@3/@5','sg_35')])]
for a,(nm,pairs) in zip(axB,cmp):
    vals=[R[k]['r2'] for _,k in pairs]; a.bar(range(len(pairs)),vals,color=['0.6','tab:red'],alpha=.85)
    for i,v in enumerate(vals): a.text(i,v+0.001,f"{v:.4f}",ha='center',va='bottom',fontsize=8)
    a.set_xticks(range(len(pairs))); a.set_xticklabels([l for l,_ in pairs],fontsize=8); a.set_ylim(0.90,1.01)
    a.set_ylabel('R²'); a.set_title(f"{nm} — baseline ↔ @3/@5",fontsize=9.5); a.grid(alpha=.3,axis='y')
fig.suptitle('v1.0.24 — SINTEF 공개 실측 @3(Si Frumkin regsol)·@5(흑연 5-feature staging) 반영식 피팅 (baseline 대조)',fontsize=12.5)
fig.tight_layout(); fig.savefig(f"{CV}/final_fit_sintef.png",dpi=120)

print("="*88)
print(f"{'셀':16s} {'baseline':>12s} {'@3/@5 반영식':>14s}   비고")
print(f"{'흑연(SINTEF)':16s}  R²={R['gr_bl']['r2']:.4f}    R²={R['gr_5f']['r2']:.4f}    (@5=5-feature stage-2L)")
print(f"{'실리콘(SINTEF)':16s}  R²={R['si_bl']['r2']:.4f}    R²={R['si_fr']['r2']:.4f}    (@3=Frumkin regsol)")
print(f"{'흑연+Si블렌드':16s}  R²={R['sg_bl']['r2']:.4f}    R²={R['sg_35']['r2']:.4f}    (@5 흑연+@3 Si)")
print("-"*88)
print("★@3 Si regsol Ω/RT (§7/@3 분류부과 — 두-상>2·고용체<2):")
print("   "+" · ".join(f"{t[1]:.3f}V:Ω/RT={t[2]:.1f}{'(두-상)' if t[2]>2 else '(고용체)'}" for t in R['si_fr']['trs']))
print("saved: final_fit_sintef.png")
