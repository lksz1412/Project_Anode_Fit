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
m._REGSOL_XG=np.linspace(1e-4,1.0-1e-4,600)   # 피팅 속도(출하 1200→600; 곡선 형상·R² 무영향, 매끈 유지)
MAXPTS=320                                     # 창내점 상한(regsol 비용 억제; 균등 서브샘플)

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
    if len(Vx)>MAXPTS:                                     # 균등 서브샘플(형상 보존·regsol 비용 억제)
        sel=np.linspace(0,len(Vx)-1,MAXPTS).round().astype(int); Vx,Dx=Vx[sel],Dx[sel]
    NG,NS=len(gr_seed),len(si_seed); area=float(_trapz(Dx,Vx)); p0=[];lo=[];hi=[]
    def push(seed,Ulo,Uhi,wlo,whi):
        for (U,Om,Qf,w,OmLo,OmHi) in seed:                # OmLo/OmHi = 전이별 Ω 경계(자유 or §7분류 부과)
            if kernel=='regsol': p0.extend([U,Om,Qf*area,w]); lo.extend([Ulo,OmLo,1e-6,wlo]); hi.extend([Uhi,OmHi,10*area,whi])
            else:                p0.extend([U,w,Qf*area]);    lo.extend([Ulo,wlo,1e-6]);       hi.extend([Uhi,whi,10*area])
    push(gr_seed,0.05,0.30,0.0008,0.060)
    push(si_seed,0.15,0.60,0.0030,0.080)
    p0.append(max(Dx.min(),1e-6)); lo.append(0.0); hi.append(max(Dx)+1e-9)
    fn=model(NG,NS,kernel)
    popt,_=curve_fit(fn,Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=40000)
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

# ---- 시드: (U, Omega, Q_frac, w, Ω_lo, Ω_hi) ----  2RT(298K)≈4958 J/mol = Ω/RT 2 경계
# 흑연 @5 XRD 5-feature(stage-2L 분리: 3↔2L=0.132 · 2L↔2=0.116).
GR5_free=[(0.210,3000,0.06,0.016,0,20000),(0.170,3000,0.10,0.022,0,20000),(0.132,6000,0.12,0.010,0,20000),
          (0.116,8000,0.20,0.010,0,20000),(0.090,12000,0.45,0.012,0,20000)]        # Ω 완전자유(자발판정)
# §7(sec:broadening) 분류 부과: dilute·4→3·3→2L=고용체(Ω<2RT), 2L→2·2→1=두-상(Ω>2RT). §7 line24 "네 전이가
#   초기값 Ω로 문턱 넘지만 물리적으론 두 전이만 두-상" 을 그대로 강제 → 문건 분류가 데이터와 양립하나 시험.
GR5_con =[(0.210,3000,0.06,0.016,200,4900),(0.170,3000,0.10,0.022,200,4900),(0.132,3000,0.12,0.016,200,4900),
          (0.116,8000,0.20,0.010,4958,20000),(0.090,12000,0.45,0.012,4958,20000)]
GR4=[(0.088,0,0.12,0.004,0,20000),(0.120,0,0.20,0.006,0,20000),(0.142,0,0.30,0.016,0,20000),(0.210,0,0.10,0.006,0,20000)]
# Si @3: a-Si 고용체 + c-Li15Si4 유일 두-상.
SI3_free=[(0.28,2000,0.40,0.050,0,20000),(0.43,8000,0.15,0.006,0,20000),(0.47,2000,0.30,0.050,0,20000)]
SI3_con =[(0.28,2000,0.40,0.050,200,4900),(0.43,8000,0.15,0.006,4958,20000),(0.47,2000,0.30,0.050,200,4900)]
SI3L=[(0.28,0,0.40,0.050,0,20000),(0.43,0,0.15,0.006,0,20000),(0.47,0,0.30,0.050,0,20000)]

# ---- 3방: 로지스틱 baseline · regsol 자유-Ω · regsol §7분류부과 ----
import sys,time
R={}; T0=time.time()
def go(key,*a):
    R[key]=fit(*a); r=R[key]
    print(f"[{time.time()-T0:5.1f}s] {key:6s} R²={r['r2']:.4f} npts={r['npts']} ({r['kernel']})",flush=True)
go('gr_lg','logistic','gr',  (0.086,0.30),0.0005, GR4, [])
go('si_lg','logistic','si',  (0.06,0.55), 0.001,  [],  SI3L)
go('sg_lg','logistic','sigr',(0.05,0.52), 0.0007, GR4, SI3L)
go('gr_rf','regsol',  'gr',  (0.086,0.30),0.0005, GR5_free, [])
go('si_rf','regsol',  'si',  (0.06,0.55), 0.001,  [],  SI3_free)
go('sg_rf','regsol',  'sigr',(0.05,0.52), 0.0007, GR5_free, SI3_free)
go('gr_rc','regsol',  'gr',  (0.086,0.30),0.0005, GR5_con, [])
go('si_rc','regsol',  'si',  (0.06,0.55), 0.001,  [],  SI3_con)
go('sg_rc','regsol',  'sigr',(0.05,0.52), 0.0007, GR5_con, SI3_con)

# ---- 그림: 상단=§7분류부과 regsol 피팅(문건 그대로), 하단=커널 3방 R² 비교 ----
fig=plt.figure(figsize=(18,9)); gs=fig.add_gridspec(2,3,height_ratios=[2.2,1.0])
def draw(a,title,r,showcomp=False):
    a.plot(r['Vx'],r['Dx'],'o',ms=2.0,color='0.4',alpha=.5,label=f"실측 dQ/dV (BDD, {r['npts']}점)")
    a.plot(r['Vx'],r['pred'],'-',color='tab:red',lw=2,label=f"regsol(§7분류 부과) R²={r['r2']:.4f}")
    if showcomp and r['grc'] is not None:
        a.plot(r['Vx'],r['grc'],'--',color='tab:blue',lw=1.1,label='흑연 성분(@5 5-feature)')
        a.plot(r['Vx'],r['sic'],':',color='tab:green',lw=1.5,label=f"Si 성분(@3 Frumkin, f_Si={r['fSi']:.2f})")
    a.set_title(title,fontsize=10); a.set_xlabel('V vs Li'); a.set_ylabel('dQ/dV'); a.legend(fontsize=7.5); a.grid(alpha=.3)
axA=[fig.add_subplot(gs[0,j]) for j in range(3)]; axB=[fig.add_subplot(gs[1,j]) for j in range(3)]
draw(axA[0],'(1) 흑연 반쪽셀 — @5 5-feature + regsol(§7 분류 부과)\nSINTEF Zenodo(실측 pOCV C/50)',R['gr_rc'])
draw(axA[1],'(2) 실리콘 반쪽셀 — @3 Frumkin regsol\n(a-Si 고용체 + c-Li15Si4 두-상)',R['si_rc'])
draw(axA[2],'(3) 흑연+Si 블렌드 — @5+@3 가산',R['sg_rc'],showcomp=True)
# 하단: 커널 3방 R² (로지스틱 / 자유-Ω / §7분류부과) — 단일T 에서 거의 동등함을 보인다
cells=[('흑연',['gr_lg','gr_rf','gr_rc']),('실리콘',['si_lg','si_rf','si_rc']),('블렌드',['sg_lg','sg_rf','sg_rc'])]
labs=['로지스틱\nbaseline','regsol\n자유-Ω','regsol\n§7분류부과']
for a,(nm,keys) in zip(axB,cells):
    vals=[R[k]['r2'] for k in keys]; a.bar(range(3),vals,color=['0.6','tab:orange','tab:red'],alpha=.85)
    for i,v in enumerate(vals): a.text(i,v+0.001,f"{v:.4f}",ha='center',va='bottom',fontsize=7.5)
    a.set_xticks(range(3)); a.set_xticklabels(labs,fontsize=7.5); a.set_ylim(0.90,1.01)
    a.set_ylabel('R²'); a.set_title(f"{nm} — 커널 3방 R² (단일T 거의 동등)",fontsize=9); a.grid(alpha=.3,axis='y')
fig.suptitle('v1.0.24 — SINTEF 실측 @3/@5 반영식(Frumkin regsol) 피팅: 문건 §7/@3 분류 부과 + 커널 3방 R² 비교',fontsize=12.5)
fig.tight_layout(); fig.savefig(f"{CV}/final_fit_sintef.png",dpi=120)

print("="*92)
print(f"{'셀':14s} {'로지스틱baseline':>16s} {'regsol자유Ω':>14s} {'regsol§7분류':>14s}")
for nm,lg,rf,rc in [("흑연(SINTEF)",'gr_lg','gr_rf','gr_rc'),("실리콘(SINTEF)",'si_lg','si_rf','si_rc'),("흑연+Si블렌드",'sg_lg','sg_rf','sg_rc')]:
    print(f"{nm:14s}  R²={R[lg]['r2']:.4f}       R²={R[rf]['r2']:.4f}     R²={R[rc]['r2']:.4f}")
print("-"*92)
print("★자유-Ω 흑연(§7 예측=Ω과다배정, 물리분류 아님): "+" · ".join(f"{t[1]:.3f}V:Ω/RT={t[2]:.1f}" for t in R['gr_rf']['trs']))
print("★§7분류부과 흑연(고용체<2·두-상>2 강제): "+" · ".join(f"{t[1]:.3f}V:Ω/RT={t[2]:.1f}" for t in R['gr_rc']['trs']))
print("★§7분류부과 Si(a-Si고용체+c-Li15Si4두-상): "+" · ".join(f"{t[1]:.3f}V:Ω/RT={t[2]:.1f}" for t in R['si_rc']['trs']))
print("saved: final_fit_sintef.png")
