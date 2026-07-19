# -*- coding: utf-8 -*-
"""v1.0.24 V5 — 모델 문제 vs 원본데이터 문제 판별(통계). 사용자 가설: 잔차의 상당수는 모델이 아니라
원본 데이터 품질(특히 V slope 노이즈=비단조 wobble) 탓.
핵심 실험: 각 셀을 (a) 원본 V, (b) 웨이블릿 denoise V(=데이터 slope 문제 교정) 두 방식으로 dQ/dV 추출·피팅.
  - denoise 가 R² 를 크게 올리고(특히 비단조 심한 셀) → '데이터(slope) 문제'.
  - denoise 무관하게 R² 낮으면 → '모델 문제'(두-상 near-delta 등 구조 한계).
데이터 품질 지표: V 단조율(V_up%)·후진스텝 노이즈. 조건별 통계 → 상관 판정.
※ 단조성 주의(사용자): BDD 미분은 단조 입력 전제. denoise 로 단조성 회복 후 추출(정합).
"""
import numpy as np, pandas as pd, importlib.util, os, sys, json, warnings
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
sys.path.insert(0,"/home/user/Project_Anode_Fit/Claude/results/comp_v24"); import bdd_smoothing as bdd
SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
af_s=importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af=importlib.util.module_from_spec(af_s); af_s.loader.exec_module(af); GR=af.GraphiteAnodeDischargeDQDV; LCO=af.LCOCathodeDQDV
_trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))

# (label, file, role, NG, NS, win)
DS=[("Gr_c1","gr_pocv_4ccc47.parquet","anode",4,0,(0.05,0.30)),
    ("Gr_c2","gr_pocv_1d5628.parquet","anode",4,0,(0.05,0.30)),
    ("Si_c1","si_c1_pocv.parquet","anode",0,3,(0.05,0.60)),
    ("Si_c2","si_c2_pocv.parquet","anode",0,3,(0.05,0.60)),
    ("SiGr1_c1","sigr_aq1_pocv.parquet","anode",4,2,(0.05,0.60)),
    ("SiGr1_c2","sigr1_c2_pocv.parquet","anode",4,2,(0.05,0.60)),
    ("SiGr2_c1","sigr_aq2_pocv.parquet","anode",4,2,(0.05,0.60)),
    ("SiGr2_c2","sigr2_c2_pocv.parquet","anode",4,2,(0.05,0.60)),
    ("SiGr3B_c1","sigr3B_c1_pocv.parquet","anode",4,2,(0.05,0.60)),
    ("SiGr3B_c2","sigr3B_c2_pocv.parquet","anode",4,2,(0.05,0.60)),
    ("NMC111","nmc111_c1_pocv.parquet","cathode",4,0,(3.55,4.28)),
    ("NMC532","nmc532_c1_pocv.parquet","cathode",4,0,(3.55,4.28))]
Ug0=[0.104,0.1415,0.227,0.140]; wg0=[0.0009,0.0011,0.0016,0.018]; Uc0=[3.68,3.75,3.90,4.05]; si_init=[(0.30,0.05),(0.45,0.05),(0.20,0.05)]

def load(path):
    d=pd.read_parquet(os.path.join(SC,path)); I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000
    idx=np.where((np.abs(I)>1e-9)&(I>0))[0]
    if len(idx)==0: return None
    seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    V=V[seg]; Q=Q[seg]-Q[seg][0]
    if len(V)>4000: k=len(V)//4000; V=V[::k]; Q=Q[::k]
    return V,Q
def vquality(V):
    dv=np.diff(V); up=float(np.mean(dv>=0)); back=np.abs(dv[dv<0]); noise=float(np.median(back)*1000) if len(back) else 0.0
    return up,noise
def make_model(NG,NS,role):
    cls=LCO if role=="cathode" else GR
    def f(V,*p):
        i=0;gr=[];si=[]
        for _ in range(NG): gr.append({'U':p[i],'w':p[i+1],'Q':p[i+2]}); i+=3
        for _ in range(NS): si.append({'U':p[i],'w':p[i+1],'Q':p[i+2]}); i+=3
        Cbg=p[i]; Va=np.asarray(V,float); out=np.zeros_like(Va)
        out=out+(np.asarray(cls(gr,Cbg=float(Cbg)).equilibrium(Va,298.15),float) if gr else float(Cbg))
        if si: out=out+np.asarray(GR(si,Cbg=0.0).equilibrium(Va,298.15),float)
        return out
    return f
def fit(V,Q,role,NG,NS,win,denoise):
    Vd=bdd.denoise(V,denoise) if denoise>0 else V
    dvv=0.001 if role=="cathode" else 0.0005
    gx,gy=bdd.dqdv_grid_bdd(Vd,Q,dV=dvv)
    LO,HI=win; m=(gx>=LO)&(gx<=HI); Vx,Dx=gx[m],gy[m]
    if len(Vx)<20: return None
    area=float(_trapz(Dx,Vx)); U0=(Uc0 if role=="cathode" else Ug0)
    p0=[];lo=[];hi=[]
    for j in range(NG):
        if role=="cathode": p0+=[U0[j],0.03,0.25*area];lo+=[LO,0.005,1e-6];hi+=[HI,0.20,10*area]
        else: p0+=[U0[j],wg0[j],0.2*area];lo+=[0.05,0.0008,1e-6];hi+=[0.30,0.060,10*area]
    for j in range(NS): u,w=si_init[j];p0+=[u,w,0.3*area];lo+=[0.15,0.01,1e-6];hi+=[0.58,0.30,10*area]
    p0+=[max(Dx.min(),1e-6)];lo+=[0.0];hi+=[max(Dx)]
    try: popt,_=curve_fit(make_model(NG,NS,role),Vx,Dx,p0=p0,bounds=(lo,hi),maxfev=400000)
    except Exception: return None
    pred=make_model(NG,NS,role)(Vx,*popt)
    return 1.0-np.sum((Dx-pred)**2)/np.sum((Dx-Dx.mean())**2)

rows=[]
for label,f,role,NG,NS,win in DS:
    r=load(f)
    if r is None: continue
    V,Q=r; up,noise=vquality(V)
    r2_raw=fit(V,Q,role,NG,NS,win,0.0)
    r2_dn =fit(V,Q,role,NG,NS,win,1.0)
    rows.append(dict(label=label,role=role,chem=label.split("_")[0],V_up=round(up*100,1),Vnoise_mV=round(noise,3),
                     R2_raw=round(r2_raw,4) if r2_raw else None, R2_denoise=round(r2_dn,4) if r2_dn else None,
                     dR2=round((r2_dn-r2_raw),4) if (r2_raw and r2_dn) else None))
    print(f'{label:10s} V_up={up*100:5.1f}%  R²_raw={r2_raw:.4f}  R²_denoise={r2_dn:.4f}  ΔR²={r2_dn-r2_raw:+.4f}')
json.dump(rows,open(f"{OUT}/model_vs_data_result.json","w"),ensure_ascii=False,indent=1)

# ===== 통계 판정 그림 =====
R=[x for x in rows if x["R2_raw"] is not None]
vup=np.array([x["V_up"] for x in R]); r2r=np.array([x["R2_raw"] for x in R]); r2d=np.array([x["R2_denoise"] for x in R]); dr=np.array([x["dR2"] for x in R])
fig,ax=plt.subplots(1,3,figsize=(17,5.2))
cc={"Gr":"tab:blue","Si":"tab:green","SiGr1":"tab:orange","SiGr2":"tab:red","SiGr3B":"tab:purple","NMC111":"tab:brown","NMC532":"tab:pink"}
for x in R: ax[0].scatter(x["V_up"],x["R2_raw"],c=cc.get(x["chem"],"gray"),s=55)
for x in R: ax[0].annotate(x["label"],(x["V_up"],x["R2_raw"]),fontsize=6)
# 상관계수
if len(R)>2:
    cr=np.corrcoef(vup,r2r)[0,1]; ax[0].set_title(f"R²(raw) vs V단조율  (상관 r={cr:.2f})")
ax[0].set_xlabel("V_up% (데이터 품질=단조율)"); ax[0].set_ylabel("R² (raw)"); ax[0].grid(alpha=.3)
# ΔR² vs V_up: 노이즈 심한(낮은 V_up) 셀이 denoise 로 더 개선되면 데이터 문제
for x in R: ax[1].scatter(x["V_up"],x["dR2"],c=cc.get(x["chem"],"gray"),s=55)
for x in R: ax[1].annotate(x["label"],(x["V_up"],x["dR2"]),fontsize=6)
ax[1].axhline(0,color='k',lw=.6); ax[1].set_xlabel("V_up%"); ax[1].set_ylabel("ΔR²=denoise−raw"); ax[1].set_title("V denoise 개선폭 vs 단조율\n(낮은 단조율서 ↑개선 → 데이터 slope 문제)"); ax[1].grid(alpha=.3)
# raw vs denoise R²
ax[2].plot([0.7,1],[0.7,1],'k--',lw=.6);
for x in R: ax[2].scatter(x["R2_raw"],x["R2_denoise"],c=cc.get(x["chem"],"gray"),s=55)
ax[2].set_xlabel("R² raw"); ax[2].set_ylabel("R² denoise(V)"); ax[2].set_title("V-slope denoise 효과"); ax[2].grid(alpha=.3)
import matplotlib.patches as mp
ax[2].legend(handles=[mp.Patch(color=v,label=k) for k,v in cc.items()],fontsize=7,loc='lower right')
fig.tight_layout(); fig.savefig(f"{OUT}/model_vs_data.png",dpi=120); print("saved model_vs_data.png")
print(f"\n상관 r(V_up, R²_raw)={np.corrcoef(vup,r2r)[0,1]:.3f}  | 평균 ΔR²(denoise)={dr.mean():+.4f}")
