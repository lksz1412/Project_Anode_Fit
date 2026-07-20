# -*- coding: utf-8 -*-
"""v1.0.24 최종 코드 — SINTEF 공개 실측(Zenodo 20086298, CC-BY-4.0) 흑연·실리콘·흑연+Si 블렌드 피팅.
   ★[핵심] @3/@5 반영식(Frumkin regsol 커널)을 실제로 태운다:
     - Si  = @3 정칙용액(Frumkin) 커널 'kernel':'regsol' + Ω 자유 → 두-상(Ω>2RT) vs 고용체(Ω<2RT) 자발 분류.
     - 흑연 = @5 XRD 5-feature staging(stage-2L 분리 3↔2L·2L↔2) + regsol 커널(두-상 Ω>2RT).
   대조군으로 기본 로지스틱(bit-exact baseline)도 같이 피팅해 @3/@5 효과를 정직 비교한다.
   반쪽셀 pOCV(C/50, RT). dQ/dV 추출 = BDD 스무딩. 피팅 = scipy.curve_fit. 데이터=리포 CSV(영구보존)."""
import numpy as np, importlib.util, pandas as pd, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False
from scipy.optimize import curve_fit
_trapz=getattr(np,'trapezoid',None) or getattr(np,'trapz',None)
ROOT="/home/user/Project_Anode_Fit/Claude"; DOC=f"{ROOT}/docs/v1.0.24"; CV=f"{ROOT}/results/comp_v24"
DATA=f"{CV}/sintef_data"                                   # ★리포 영구보존 CSV(재다운로드 불필요)
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/sintef"
R_GAS=8.314462618; F_CONST=96485.33212
def load(n,p): s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
m=load("af",f"{DOC}/Anode_Fit_v1.0.24.py"); bdd=load("bdd",f"{CV}/bdd_smoothing.py")
GR=m.GraphiteAnodeDischargeDQDV

def load_delith(k):
    """리포 CSV 우선(영구보존) → 없으면 스크래치 parquet 폴백."""
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

# ---- 모델: kernel='regsol'(@3/@5) 또는 'logistic'(baseline) ----
def model(NG,NS,kernel):
    npar=4 if kernel=='regsol' else 3
    def f(V,*p):
        gr=[];si=[];i=0
        for _ in range(NG):
            if kernel=='regsol': gr.append({'U':p[i],'Omega':p[i+1],'Q':p[i+2],'w':p[i+3],'kernel':'regsol'})
            else:                gr.append({'U':p[i],'w':p[i+1],'Q':p[i+2]})
            i+=npar
        for _ in range(NS):
            if kernel=='regsol': si.append({'U':p[i],'Omega':p[i+1],'Q':p[i+2],'w':p[i+3],'kernel':'regsol'})
            else:                si.append({'U':p[i],'w':p[i+1],'Q':p[i+2]})
            i+=npar
        Cbg=p[i]; Va=np.asarray(V,float)
        out=np.asarray(GR(gr,Cbg=float(Cbg)).equilibrium(Va,298.15),float)
        if si: out=out+np.asarray(GR(si,Cbg=0.0).equilibrium(Va,298.15),float)
        return out
    return f

def fit(kernel,k,win,dvv,gr_seed,si_seed):
    """gr_seed/si_seed = [(U,Omega,Q_frac,w), ...]. 로지스틱은 Omega 무시."""
    V,Q=load_delith(k); Vx,Dx=dqdv(V,Q,win,dvv)
    NG,NS=len(gr_seed),len(si_seed); area=float(_trapz(Dx,Vx)); p0=[];lo=[];hi=[]
    def push(seed,Ulo,Uhi,wlo,whi):
        for (U,Om,Qf,w) in seed:
            if kernel=='regsol': p0.extend([U,Om,Qf*area,w]); lo.extend([Ulo,0.0,1e-6,wlo]); hi.extend([Uhi,20000.0,10*area,whi])
            else:                p0.extend([U,w,Qf*area]);    lo.extend([Ulo,wlo,1e-6]);      hi.extend([Uhi,whi,10*area])
    push(gr_seed,0.05,0.30,0.0008,0.060)
    push(si_seed,0.15,0.60,0.0030,0.080)
    p0.append(max(Dx.min(),1e-6)); lo.append(0.0); hi.append(max(Dx)+1e-9)
    fn=model(NG,NS,kernel)
    popt,_=curve_fit(fn,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=400000)
    pred=fn(Vx,*popt); r2=1.0-np.sum((Dx-pred)**2)/np.sum((Dx-Dx.mean())**2)
    # 파라미터 분해 + Ω/RT (두-상>2 vs 고용체<2 판정)
    RT=R_GAS*298.15; npar=4 if kernel=='regsol' else 3; i=0; trs=[]; Qg=Qs=0.0
    grc=sic=None; gr=[];si=[]
    for _ in range(NG):
        if kernel=='regsol':
            U,Om,Qj,w=popt[i:i+4]; trs.append(('gr',U,Om/RT,Qj,w)); gr.append({'U':U,'Omega':Om,'Q':Qj,'w':w,'kernel':'regsol'}); Qg+=Qj
        else:
            U,w,Qj=popt[i:i+3]; trs.append(('gr',U,None,Qj,w)); gr.append({'U':U,'w':w,'Q':Qj}); Qg+=Qj
        i+=npar
    for _ in range(NS):
        if kernel=='regsol':
            U,Om,Qj,w=popt[i:i+4]; trs.append(('si',U,Om/RT,Qj,w)); si.append({'U':U,'Omega':Om,'Q':Qj,'w':w,'kernel':'regsol'}); Qs+=Qj
        else:
            U,w,Qj=popt[i:i+3]; trs.append(('si',U,None,Qj,w)); si.append({'U':U,'w':w,'Q':Qj}); Qs+=Qj
        i+=npar
    Cbg=popt[i]
    if NG: grc=np.asarray(GR(gr,Cbg=float(Cbg)).equilibrium(Vx,298.15),float)
    if NS: sic=np.asarray(GR(si,Cbg=0.0).equilibrium(Vx,298.15),float)
    fSi=Qs/(Qg+Qs) if (Qg+Qs)>0 else None
    return dict(Vx=Vx,Dx=Dx,pred=pred,r2=float(r2),NG=NG,NS=NS,npts=len(Vx),grc=grc,sic=sic,fSi=fSi,trs=trs,kernel=kernel)

# ---- 시드: (U, Omega, Q_frac, w) ----
# 흑연 @5 XRD 5-feature(stage-2L 분리: 3↔2L=0.132 · 2L↔2=0.116). Ω 자유(두-상 자발 판정).
GR5=[(0.210,6000,0.06,0.016),(0.170,3000,0.10,0.022),(0.132,10000,0.12,0.010),
     (0.116,10000,0.20,0.010),(0.090,13000,0.45,0.012)]
GR4=[(0.088,0,0.12,0.004),(0.120,0,0.20,0.006),(0.142,0,0.30,0.016),(0.210,0,0.10,0.006)]  # 로지스틱 대조(4전이)
# Si @3 regsol: broad a-Si(Ω<2RT) + c-Li15Si4 sharp(Ω>2RT 두-상).
SI3=[(0.28,2000,0.40,0.050),(0.43,10000,0.15,0.006),(0.47,3000,0.30,0.050)]
SI3L=[(0.28,0,0.40,0.050),(0.43,0,0.15,0.006),(0.47,0,0.30,0.050)]                          # 로지스틱 대조

# ---- @3/@5 regsol 피팅(본선) + 로지스틱 baseline(대조) ----
R={}
R['gr_rs']  = fit('regsol',  'gr',  (0.086,0.30),0.0005, GR5, [])
R['si_rs']  = fit('regsol',  'si',  (0.06,0.55), 0.001,  [],  SI3)
R['sg_rs']  = fit('regsol',  'sigr',(0.05,0.52), 0.0007, GR5, SI3)
R['gr_lg']  = fit('logistic','gr',  (0.086,0.30),0.0005, GR4, [])
R['si_lg']  = fit('logistic','si',  (0.06,0.55), 0.001,  [],  SI3L)
R['sg_lg']  = fit('logistic','sigr',(0.05,0.52), 0.0007, GR4, SI3L)

# ---- 그림: 상단=@3/@5 regsol 피팅, 하단=Ω/RT 막대(두-상>2 vs 고용체<2) ----
fig=plt.figure(figsize=(18,9)); gs=fig.add_gridspec(2,3,height_ratios=[2.3,1.0])
def draw(a,title,r,showcomp=False):
    a.plot(r['Vx'],r['Dx'],'o',ms=2.0,color='0.4',alpha=.5,label=f"실측 dQ/dV (BDD, {r['npts']}점)")
    a.plot(r['Vx'],r['pred'],'-',color='tab:red',lw=2,label=f"@3/@5 regsol 피팅 (R²={r['r2']:.4f})")
    if showcomp and r['grc'] is not None:
        a.plot(r['Vx'],r['grc'],'--',color='tab:blue',lw=1.1,label='흑연 성분(@5 5-feature)')
        a.plot(r['Vx'],r['sic'],':',color='tab:green',lw=1.5,label=f"Si 성분(@3 Frumkin, f_Si={r['fSi']:.2f})")
    a.set_title(title,fontsize=10); a.set_xlabel('V vs Li'); a.set_ylabel('dQ/dV'); a.legend(fontsize=7.5); a.grid(alpha=.3)
def bars(a,title,r):
    xs=range(len(r['trs'])); vals=[t[2] for t in r['trs']]; cols=['tab:red' if v>2 else 'tab:green' for v in vals]
    a.bar(xs,vals,color=cols,alpha=.8); a.axhline(2.0,color='k',ls='--',lw=1)
    a.text(0.02,0.92,'Ω/RT=2 (두-상↔고용체 경계)',transform=a.transAxes,fontsize=7.5,va='top')
    a.set_xticks(list(xs)); a.set_xticklabels([f"{t[0]}\n{t[1]:.3f}V" for t in r['trs']],fontsize=7)
    a.set_ylabel('Ω/RT'); a.set_title(title,fontsize=9); a.grid(alpha=.3,axis='y')
axA=[fig.add_subplot(gs[0,j]) for j in range(3)]; axB=[fig.add_subplot(gs[1,j]) for j in range(3)]
draw(axA[0],'(1) 흑연 반쪽셀 — @5 5-feature+regsol\nSINTEF Zenodo(실측 pOCV C/50)',R['gr_rs'])
draw(axA[1],'(2) 실리콘 반쪽셀 — @3 Frumkin regsol\nSINTEF(고용체 Ω<2RT + c-Li15Si4 Ω>2RT)',R['si_rs'])
draw(axA[2],'(3) 흑연+Si 블렌드 — @5+@3 가산\nSINTEF',R['sg_rs'],showcomp=True)
bars(axB[0],'흑연 전이별 Ω/RT (빨강=두-상>2)',R['gr_rs'])
bars(axB[1],'Si 전이별 Ω/RT (c-Li15Si4=두-상)',R['si_rs'])
bars(axB[2],'블렌드 전이별 Ω/RT',R['sg_rs'])
fig.suptitle('v1.0.24 — SINTEF 실측 @3(Si Frumkin)·@5(흑연 5-feature stage-2L) 반영식 피팅 + Ω/RT 두-상 분류',fontsize=13)
fig.tight_layout(); fig.savefig(f"{CV}/final_fit_sintef.png",dpi=120)

print("="*84)
print(f"{'셀':20s} {'@3/@5 regsol':>14s} {'로지스틱 baseline':>16s}   전이(gr/Si)")
for lab,rk,lk in [("흑연(SINTEF)",'gr_rs','gr_lg'),("실리콘(SINTEF)",'si_rs','si_lg'),("흑연+Si 블렌드",'sg_rs','sg_lg')]:
    rr=R[rk]; rl=R[lk]
    print(f"{lab:20s}  R²={rr['r2']:.4f}      R²={rl['r2']:.4f}       {rr['NG']}/{rr['NS']}")
print("-"*84)
print("★Ω/RT 두-상(>2) vs 고용체(<2) — @3/@5 물리가 실측에서 자발적으로 갈리는지:")
for lab,rk in [("흑연",'gr_rs'),("Si",'si_rs'),("블렌드",'sg_rs')]:
    tags=[f"{t[0]}@{t[1]:.3f}V:Ω/RT={t[2]:.1f}{'(두-상)' if t[2]>2 else '(고용체)'}" for t in R[rk]['trs']]
    print(f"  {lab:6s}: "+" · ".join(tags))
print("saved: final_fit_sintef.png")
