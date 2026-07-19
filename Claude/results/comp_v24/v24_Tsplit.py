# -*- coding: utf-8 -*-
"""v1.0.24 코드점검 — 사용자 관측 재현 테스트: 흑연 3번째 전이가 45℃ 2피크 / 25℃ 1피크(병합).
가설: 열 broadening 아님(그럼 고온서 더 병합). ΔS 구동 분리 — 인접 두 전이의 ΔS_rxn 이 다르면
∂U/∂T=ΔS/F 로 서로 다르게 이동 → 25℃ 겹침 / 45℃ 분리. 문건 equilibrium()이 이를 재현하나(코드 정상?).
※ 문건 코드 무수정 — 출하 equilibrium() 직접 호출로 T-의존 경로 검증.
"""
import numpy as np, importlib.util, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
af_s=importlib.util.spec_from_file_location("af","/home/user/Project_Anode_Fit/Claude/docs/v1.0.23/Anode_Fit_v1.0.23.py")
af=importlib.util.module_from_spec(af_s); af_s.loader.exec_module(af); GR=af.GraphiteAnodeDischargeDQDV
F=96485.0; OUT="/home/user/Project_Anode_Fit/Claude/results/comp_v24"

# 인접 두 전이(3번째 전이 영역 ~0.14V), 25℃에 근접(0.140/0.1425), ΔS_rxn 상이(+·−)
# U(298)=(−dH+298·dS)/F 로 dH 역산. 폭은 두-상 sharp(w=0.0011, T-동결) — 'n' 미부여.
def make(U298,dS,w,Q):
    dH=298.15*dS - U298*F   # U(298)=(−dH+298.15·dS)/F 만족
    return {'dH_rxn':float(dH),'dS_rxn':float(dS),'w':float(w),'Q':float(Q)}
def dqdv_at(dS_A,dS_B,T):
    trs=[make(0.1400,dS_A,0.0011,0.5), make(0.1425,dS_B,0.0011,0.5)]
    g=GR(trs, Cbg=0.0); V=np.linspace(0.125,0.16,3000)
    d=np.asarray(g.equilibrium(V,T=T),float)
    # 실제 두 전이의 U_j(T) 출력
    Ua=af.func_U_j(T,trs[0]['dH_rxn'],trs[0]['dS_rxn']); Ub=af.func_U_j(T,trs[1]['dH_rxn'],trs[1]['dS_rxn'])
    return V,d,float(Ua),float(Ub)

def npeaks(V,d):
    # 국소최대 개수(배경 대비)
    n=0
    for i in range(2,len(d)-2):
        if d[i]==max(d[i-2:i+3]) and d[i]>0.3*np.nanmax(d): n+=1
    return n

fig,ax=plt.subplots(1,2,figsize=(14,5.2))
for k,(dSA,dSB,lab) in enumerate([(40.0,-40.0,'ΔS 상이(+40/−40)'),(0.0,0.0,'ΔS 동일(대조군)')]):
    for T,c,tn in [(298.15,'tab:blue','25℃'),(318.15,'tab:red','45℃')]:
        V,d,Ua,Ub=dqdv_at(dSA,dSB,T)
        ax[k].plot(V,d,color=c,lw=1.5,label=f'{tn}: U={Ua*1000:.1f}/{Ub*1000:.1f}mV, 피크{npeaks(V,d)}개')
    ax[k].set_xlabel('V'); ax[k].set_ylabel('dQ/dV'); ax[k].set_title(f'출하 equilibrium() T-의존: {lab}'); ax[k].legend(fontsize=8); ax[k].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/T_split.png",dpi=120); print("saved T_split.png")
# 정량
for dSA,dSB in [(40,-40),(0,0)]:
    _,d25,Ua25,Ub25=dqdv_at(dSA,dSB,298.15); _,d45,Ua45,Ub45=dqdv_at(dSA,dSB,318.15)
    sep25=abs(Ua25-Ub25)*1000; sep45=abs(Ua45-Ub45)*1000
    print(f"ΔS=({dSA},{dSB}): 25℃ 분리={sep25:.1f}mV 피크{npeaks(*dqdv_at(dSA,dSB,298.15)[:2])} | 45℃ 분리={sep45:.1f}mV 피크{npeaks(*dqdv_at(dSA,dSB,318.15)[:2])}")
print("\n해석: ΔS 상이 → 고온서 분리 확대(∂U/∂T=ΔS/F). 문건 equilibrium() T-경로 정상 작동 = 관측 재현 가능.")
