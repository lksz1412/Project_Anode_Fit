# -*- coding: utf-8 -*-
"""v1.0.24 마스터 피팅 파이프라인 + 출처·데이터·피팅 레지스트리 + 파라미터 분포.
사용자 요청: (1) BDD 스무딩(bdd_smoothing) 사용, (2) 최대한 많은 공개셋 케이스 피팅,
  (3) 출처·데이터·피팅결과 전부 기록(문건), (4) 조건별 피팅변수 분포 정리.
확장 방식: DATASETS 레지스트리에 행 추가(출처 DOI/URL 포함) → 재실행하면 표·분포 자동 갱신.
모델: 출하 GraphiteAnodeDischargeDQDV / LCOCathodeDQDV .equilibrium 직접 호출('w'만=자유폭 MSMR).
"""
import numpy as np, pandas as pd, importlib.util, os, json, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdd_smoothing as bdd
_trapz=getattr(np,'trapezoid',getattr(np,'trapz',None))

SC="/tmp/claude-0/-home-user-Project-Anode-Fit/e8d4cdbc-60e6-548e-b742-1446b8f7a8bd/scratchpad/zenodo_gr"
OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"
af_s=importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af=importlib.util.module_from_spec(af_s); af_s.loader.exec_module(af)
GR=af.GraphiteAnodeDischargeDQDV; LCO=af.LCOCathodeDQDV
QGR,QSI=372.0,3579.0
def fSi_exp(theo): return None if not theo else round(((theo-QGR)/(QSI-QGR))*QSI/theo,3)

# ===== 데이터셋 레지스트리 (출처 포함) =====================================
# dict: label, file, chem, role('anode'/'cathode'), theo(mAh/g|None), cond, NG, NS, win, source
Z1="Zenodo 20086298 (SINTEF, CC-BY-4.0, pOCV C/50, 25C)"
DATASETS=[
 dict(label="Gr_c1",       file="gr_pocv_4ccc47.parquet", chem="graphite", role="anode", theo=372, cond="pOCV/25C", NG=4,NS=0, win=(0.05,0.30), source=Z1),
 dict(label="Gr_c2",       file="gr_pocv_1d5628.parquet", chem="graphite", role="anode", theo=372, cond="pOCV/25C", NG=4,NS=0, win=(0.05,0.30), source=Z1),
 dict(label="Si_c1",       file="si_c1_pocv.parquet",     chem="Si",       role="anode", theo=3579,cond="pOCV/25C", NG=0,NS=3, win=(0.05,0.60), source=Z1),
 dict(label="Si_c2",       file="si_c2_pocv.parquet",     chem="Si",       role="anode", theo=3579,cond="pOCV/25C", NG=0,NS=3, win=(0.05,0.60), source=Z1),
 dict(label="SiGr1_lowSi_c1", file="sigr_aq1_pocv.parquet",chem="SiGr_low", role="anode", theo=510, cond="pOCV/25C", NG=4,NS=2, win=(0.05,0.60), source=Z1),
 dict(label="SiGr1_lowSi_c2", file="sigr1_c2_pocv.parquet",chem="SiGr_low", role="anode", theo=510, cond="pOCV/25C", NG=4,NS=2, win=(0.05,0.60), source=Z1),
 dict(label="SiGr2_highSi_c1",file="sigr_aq2_pocv.parquet",chem="SiGr_high",role="anode", theo=1150,cond="pOCV/25C", NG=4,NS=2, win=(0.05,0.60), source=Z1),
 dict(label="SiGr2_highSi_c2",file="sigr2_c2_pocv.parquet",chem="SiGr_high",role="anode", theo=1150,cond="pOCV/25C", NG=4,NS=2, win=(0.05,0.60), source=Z1),
 dict(label="SiGr3_B_c1",  file="sigr3B_c1_pocv.parquet", chem="SiGr_B",   role="anode", theo=900, cond="pOCV/25C", NG=4,NS=2, win=(0.05,0.60), source=Z1),
 dict(label="SiGr3_B_c2",  file="sigr3B_c2_pocv.parquet", chem="SiGr_B",   role="anode", theo=900, cond="pOCV/25C", NG=4,NS=2, win=(0.05,0.60), source=Z1),
 dict(label="NMC111_c1",   file="nmc111_c1_pocv.parquet", chem="NMC111",   role="cathode",theo=None,cond="pOCV/25C", NG=4,NS=0, win=(3.55,4.28), source=Z1+" ⚠LCO아님(층상 대리)"),
 dict(label="NMC532_c1",   file="nmc532_c1_pocv.parquet", chem="NMC532",   role="cathode",theo=None,cond="pOCV/25C", NG=4,NS=0, win=(3.55,4.28), source=Z1+" ⚠LCO아님(층상 대리)"),
]

Ug0=[0.104,0.1415,0.227,0.140]; wg0=[0.0009,0.0011,0.0016,0.018]
Uc0=[3.68,3.75,3.90,4.05]; si_init=[(0.30,0.05),(0.45,0.05),(0.20,0.05)]

def load_delith(path):
    d=pd.read_parquet(os.path.join(SC,path))
    I=d['Current / A'].to_numpy(); V=d['Voltage / V'].to_numpy(); Q=d['Cumulative Capacity / Ah'].to_numpy()*1000.0
    idx=np.where((np.abs(I)>1e-9)&(I>0))[0]
    if len(idx)==0: return None
    seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    return V[seg], Q[seg]-Q[seg][0]

def make_model(NG,NS,role):
    cls=LCO if role=="cathode" else GR
    def f(V,*p):
        i=0; gr=[]; si=[]
        for _ in range(NG): gr.append({'U':p[i],'w':p[i+1],'Q':p[i+2]}); i+=3
        for _ in range(NS): si.append({'U':p[i],'w':p[i+1],'Q':p[i+2]}); i+=3
        Cbg=p[i]; Va=np.asarray(V,float); out=np.zeros_like(Va)
        out = out + (np.asarray(cls(gr,Cbg=float(Cbg)).equilibrium(Va,298.15),float) if gr else float(Cbg))
        if si: out=out+np.asarray(GR(si,Cbg=0.0).equilibrium(Va,298.15),float)
        return out
    return f

def fit_ds(ds):
    r=load_delith(ds["file"])
    if r is None: return dict(label=ds["label"], error="no delith seg")
    V,Q=r; LO,HI=ds["win"]; NG,NS=ds["NG"],ds["NS"]
    dvv=0.001 if ds["role"]=="cathode" else 0.0005
    gx,gy=bdd.dqdv_grid_bdd(V,Q, dV=dvv)                    # ★ BDD 스무딩 사용
    m=(gx>=LO)&(gx<=HI); Vx,Dx=gx[m],gy[m]
    if len(Vx)<20: return dict(label=ds["label"], error="short window")
    area=float(_trapz(Dx,Vx))
    U0=(Uc0 if ds["role"]=="cathode" else Ug0)
    p0=[]; lob=[]; hib=[]
    for j in range(NG):
        if ds["role"]=="cathode": p0+=[U0[j],0.03,0.25*area]; lob+=[LO,0.005,1e-6]; hib+=[HI,0.20,10*area]
        else: p0+=[U0[j],wg0[j],0.2*area]; lob+=[0.05,0.0008,1e-6]; hib+=[0.30,0.060,10*area]
    for j in range(NS):
        u,w=si_init[j]; p0+=[u,w,0.3*area]; lob+=[0.15,0.01,1e-6]; hib+=[0.58,0.30,10*area]
    p0+=[max(Dx.min(),1e-6)]; lob+=[0.0]; hib+=[max(Dx)]
    try: popt,_=curve_fit(make_model(NG,NS,ds["role"]),Vx,Dx,p0=p0,bounds=(lob,hib),maxfev=600000)
    except Exception as e: return dict(label=ds["label"], error=str(e)[:60])
    pred=make_model(NG,NS,ds["role"])(Vx,*popt)
    r2=1.0-np.sum((Dx-pred)**2)/np.sum((Dx-Dx.mean())**2)
    i=0; Ug=[];wg=[];Qg=[];Us=[];ws=[];Qs=[]
    for _ in range(NG): Ug.append(popt[i]);wg.append(popt[i+1]);Qg.append(popt[i+2]);i+=3
    for _ in range(NS): Us.append(popt[i]);ws.append(popt[i+1]);Qs.append(popt[i+2]);i+=3
    Qgr=float(np.sum(Qg)); Qsi=float(np.sum(Qs)); tot=Qgr+Qsi
    # 정렬(전위 오름차순)해서 기록 일관
    gorder=np.argsort(Ug) if NG else []
    sorder=np.argsort(Us) if NS else []
    return dict(label=ds["label"], chem=ds["chem"], role=ds["role"], cond=ds["cond"],
                theo=ds["theo"], source=ds["source"], R2=round(float(r2),4), area=round(area,3),
                U_gr=[round(float(Ug[k]),4) for k in gorder], w_gr_mV=[round(float(wg[k])*1000,2) for k in gorder],
                Q_gr=[round(float(Qg[k]),4) for k in gorder],
                U_si=[round(float(Us[k]),4) for k in sorder], w_si_mV=[round(float(ws[k])*1000,1) for k in sorder],
                Q_si=[round(float(Qs[k]),4) for k in sorder],
                f_Si_fit=round(Qsi/tot,3) if (NG and NS and tot>0) else (1.0 if NG==0 else (0.0 if NS==0 else None)),
                f_Si_exp=fSi_exp(ds["theo"]) if (NG and NS) else None,
                fit=(Vx,Dx,pred))

results=[]; fits={}
for ds in DATASETS:
    r=fit_ds(ds); fits[ds["label"]]=r.pop("fit",None); results.append(r)
    print(f'{r["label"]:18s} R²={r.get("R2","--"):>6} f_Si={r.get("f_Si_fit")}/{r.get("f_Si_exp")}  {r.get("error","")}')

# ===== 레지스트리 저장(CSV + JSON) =====
json.dump(results, open(f"{OUT}/fit_registry.json","w"), ensure_ascii=False, indent=1)
rows=[]
for r in results:
    if "error" in r: continue
    rows.append(dict(label=r["label"],chem=r["chem"],role=r["role"],cond=r["cond"],theo=r["theo"],R2=r["R2"],
        U_gr=";".join(map(str,r["U_gr"])), w_gr_mV=";".join(map(str,r["w_gr_mV"])),
        U_si=";".join(map(str,r["U_si"])), w_si_mV=";".join(map(str,r["w_si_mV"])),
        f_Si_fit=r["f_Si_fit"], f_Si_exp=r["f_Si_exp"], source=r["source"]))
pd.DataFrame(rows).to_csv(f"{OUT}/fit_registry.csv", index=False)
print("saved fit_registry.csv / .json  (N=",len(rows),")")

# ===== 파라미터 분포 분석 (조건/화학별) =====================================
import warnings; warnings.filterwarnings("ignore")
ok=[r for r in results if "error" not in r]
# 흑연 스테이징 피크: U 근접 클러스터(0.104/0.142/0.227 + shoulder)로 라벨 부여
def cluster_label(u):
    for lo,hi,name in [(0.09,0.115,"2→1(0.10)"),(0.13,0.155,"3→2L(0.14)"),(0.20,0.24,"4→3(0.22)")]:
        if lo<=u<=hi: return name
    return "shoulder/기타"
gr_pts=[]  # (chem, peak_label, U, w_mV)
for r in ok:
    if r["role"]!="anode": continue
    for U,w in zip(r["U_gr"],r["w_gr_mV"]): gr_pts.append((r["chem"],cluster_label(U),U,w))
si_pts=[]  # (chem, U, w_mV)
for r in ok:
    for U,w in zip(r.get("U_si",[]),r.get("w_si_mV",[])): si_pts.append((r["chem"],U,w))
cat_pts=[]  # (chem, U, w_mV) 양극
for r in ok:
    if r["role"]!="cathode": continue
    for U,w in zip(r["U_gr"],r["w_gr_mV"]): cat_pts.append((r["chem"],U,w))

fig,ax=plt.subplots(2,2,figsize=(15,10))
# (a) 흑연 U 분포 by 피크 클러스터
labels=["2→1(0.10)","3→2L(0.14)","4→3(0.22)","shoulder/기타"]
for i,lab in enumerate(labels):
    us=[p[2] for p in gr_pts if p[1]==lab]
    ax[0,0].scatter([i]*len(us),us,alpha=.6,s=30)
ax[0,0].set_xticks(range(len(labels))); ax[0,0].set_xticklabels(labels,fontsize=8,rotation=15)
ax[0,0].set_ylabel("U_j / V"); ax[0,0].set_title(f"흑연 스테이징 U_j 분포 (전 anode {len([r for r in ok if r['role']=='anode'])}셀)"); ax[0,0].grid(alpha=.3)
# (b) 흑연 w 분포 by 피크 (log)
for i,lab in enumerate(labels):
    ws=[p[3] for p in gr_pts if p[1]==lab]
    ax[0,1].scatter([i]*len(ws),ws,alpha=.6,s=30)
ax[0,1].axhline(25.69,color='gray',ls='--',lw=.8,label="RT/F=25.7mV"); ax[0,1].set_yscale('log')
ax[0,1].set_xticks(range(len(labels))); ax[0,1].set_xticklabels(labels,fontsize=8,rotation=15)
ax[0,1].set_ylabel("w_j / mV (log)"); ax[0,1].set_title("흑연 w_j 분포 (두-상=sharp·shoulder=broad)"); ax[0,1].legend(fontsize=8); ax[0,1].grid(alpha=.3,which='both')
# (c) Si U-w 분포 by chem
chems=sorted(set(p[0] for p in si_pts))
cmap=plt.cm.tab10(np.linspace(0,1,max(len(chems),1)))
for c,col in zip(chems,cmap):
    us=[p[1] for p in si_pts if p[0]==c]; ws=[p[2] for p in si_pts if p[0]==c]
    ax[1,0].scatter(us,ws,label=c,color=col,alpha=.7,s=40)
ax[1,0].set_xlabel("Si U_j / V"); ax[1,0].set_ylabel("Si w_j / mV"); ax[1,0].set_title("Si host U–w 분포 (조성별)"); ax[1,0].legend(fontsize=8); ax[1,0].grid(alpha=.3)
# (d) f_Si fit vs expected
fx=[r["f_Si_exp"] for r in ok if r.get("f_Si_exp") is not None]
fy=[r["f_Si_fit"] for r in ok if r.get("f_Si_exp") is not None]
fl=[r["label"] for r in ok if r.get("f_Si_exp") is not None]
ax[1,1].plot([0,1],[0,1],'k--',lw=.8,label="y=x")
ax[1,1].scatter(fx,fy,s=50,c='tab:red')
for x,y,l in zip(fx,fy,fl): ax[1,1].annotate(l.replace("_c1","").replace("_c2","'"),(x,y),fontsize=6)
ax[1,1].set_xlabel("f_Si 기대(metadata)"); ax[1,1].set_ylabel("f_Si 피팅"); ax[1,1].set_title("f_Si: 피팅 vs metadata"); ax[1,1].legend(fontsize=8); ax[1,1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/param_distributions.png",dpi=120); print("saved param_distributions.png")

# ===== 분포 통계 요약(마크다운) =====
def stats(vals):
    v=np.array([x for x in vals if x is not None and np.isfinite(x)])
    return (len(v), round(float(np.mean(v)),4), round(float(np.std(v)),4), round(float(np.min(v)),4), round(float(np.max(v)),4)) if len(v) else (0,None,None,None,None)
lines=["# 흑연 스테이징 피크 파라미터 분포 (전 anode 셀)",""]
lines.append("| 피크 | N | U 평균 | U std | U min–max | w 평균(mV) | w std | w min–max |")
lines.append("|---|---:|---:|---:|---|---:|---:|---|")
for lab in labels:
    us=[p[2] for p in gr_pts if p[1]==lab]; ws=[p[3] for p in gr_pts if p[1]==lab]
    nu=stats(us); nw=stats(ws)
    if nu[0]: lines.append(f"| {lab} | {nu[0]} | {nu[1]} | {nu[2]} | {nu[3]}–{nu[4]} | {nw[1]} | {nw[2]} | {nw[3]}–{nw[4]} |")
open(f"{OUT}/param_dist_stats.md","w").write("\n".join(lines))
print("saved param_dist_stats.md")

# ===== 자동 레지스트리 마크다운(출처+피팅 전건) =====
ml=["<!-- 자동생성: v24_master_fit.py — 데이터 추가 시 재실행하면 갱신 -->",
    f"## 피팅 레지스트리 (N={len(ok)} 셀·조건)","",
    "| # | label | chem | role | 조건 | R² | U_gr(V) | w_gr(mV) | U_si(V) | w_si(mV) | f_Si(fit/exp) | 출처 |",
    "|--:|---|---|---|---|--:|---|---|---|---|---|---|"]
for i,r in enumerate(ok,1):
    ml.append(f"| {i} | {r['label']} | {r['chem']} | {r['role']} | {r['cond']} | {r['R2']} | "
              f"{r['U_gr']} | {r['w_gr_mV']} | {r.get('U_si',[])} | {r.get('w_si_mV',[])} | "
              f"{r.get('f_Si_fit')}/{r.get('f_Si_exp')} | {r['source']} |")
open(f"{OUT}/fit_registry.md","w").write("\n".join(ml))
print("saved fit_registry.md")

