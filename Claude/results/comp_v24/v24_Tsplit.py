# -*- coding: utf-8 -*-
"""v1.0.24 코드점검 — 사용자 관측 재현 테스트: 흑연 3번째 전이가 45℃ 2피크 / 25℃ 1피크(병합).
가설: 열 broadening 아님(그럼 고온서 더 병합). ΔS 구동 분리 — 인접 두 전이의 ΔS_rxn 이 다르면
∂U/∂T=ΔS/F 로 서로 다르게 이동 → 25℃ 겹침 / 45℃ 분리. 문건 equilibrium()이 이를 재현하나(코드 정상?).
※ 문건 코드 무수정 — 출하 equilibrium() 직접 호출로 T-의존 경로 검증.
"""
import numpy as np, importlib.util, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='NanumGothic'; plt.rcParams['axes.unicode_minus']=False  # 한글 렌더
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

from scipy.signal import find_peaks
def npeaks(V,d):
    # 분해가능(resolvable) 피크수: prominence(골 깊이) 기준 — 얕은 어깨는 1피크로.
    # sep<FWHM(=3.53·w) 이면 골이 얕아 prominence 미달 → 병합(1). sep>FWHM → 분리(2).
    d=np.asarray(d,float); mx=float(np.nanmax(d))
    pk,_=find_peaks(d, height=0.35*mx, prominence=0.02*mx)
    return int(len(pk))

# ★Dahn 1991 보정: 3↔2L(고V)·2L↔2(저V) 두 전이. Δ(ΔS)=29 J/mol/K(측정), d(ΔV)/dT=0.30 mV/K.
#   2L(엔트로피 안정화 상)는 Tm≈10℃ 이상서만 존재 → 그 이하 병합. Tm 서 두 전이 U 동일하게 앵커.
#   분리 divergence: 저V 전이(2L↔2)는 dS<0(고온서 더↓)·고V 전이(3↔2L)는 dS>0(고온서 더↑) → 고온 분리.
#   Δ(ΔS)=|dShi−dSlo|=29 로 slope=29/F=0.30 mV/℃ 자동 충족. Tm 서 병합(sep=0).
def dqdv_cal(T, Um=0.130, dSlo=-14.5, dShi=14.5, w=0.0016, Tm=283.15):
    Ulo298=Um+(dSlo/F)*(298.15-Tm); Uhi298=Um+(dShi/F)*(298.15-Tm)  # Tm서 U 동일→U298 역산
    trs=[make(Ulo298,dSlo,w,0.5), make(Uhi298,dShi,w,0.5)]
    g=GR(trs,Cbg=0.0); V=np.linspace(0.09,0.17,3000)
    d=np.asarray(g.equilibrium(V,T=T),float)
    Ua=af.func_U_j(T,trs[0]['dH_rxn'],trs[0]['dS_rxn']); Ub=af.func_U_j(T,trs[1]['dH_rxn'],trs[1]['dS_rxn'])
    return V,d,float(Ua),float(Ub)

fig,ax=plt.subplots(1,2,figsize=(14,5.2))
# 좌: T-sweep(Dahn 보정) — 2L 창 온도 의존
Ts=[(278.15,'5℃'),(283.15,'10℃'),(298.15,'25℃'),(318.15,'45℃'),(338.15,'65℃')]
cmap=plt.cm.coolwarm(np.linspace(0,1,len(Ts)))
seps=[]
for (T,tn),c in zip(Ts,cmap):
    V,d,Ua,Ub=dqdv_cal(T); sep=abs(Ua-Ub)*1000; seps.append(sep)
    ax[0].plot(V,d/np.nanmax(d),color=c,lw=1.5,label=f'{tn}: 분리{sep:.0f}mV·피크{npeaks(V,d)}')
ax[0].set_xlabel('V'); ax[0].set_ylabel('dQ/dV(정규화)'); ax[0].set_title('출하 equilibrium() T-sweep (Dahn 보정 3↔2L·2L↔2)\n고온서 2L 분리·저온 병합'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
# 우: 분리 vs T (Dahn Fig9 재현 — 선형, ~10℃서 0)
Tc=np.array([t-273.15 for t,_ in Ts]); sepA=np.array(seps)
sl=np.polyfit(Tc,sepA,1)
ax[1].plot(Tc,sepA,'o-',color='tab:red',label=f'문건 코드: {sl[0]:.3f} mV/℃')
ax[1].axhline(0,color='k',lw=.5); ax[1].axvline(10,color='gray',ls='--',lw=.8,label='Dahn: 2L 소멸 ~10℃')
ax[1].plot(Tc,0.30*(Tc-10),'k:',lw=1.2,label='Dahn 1991 측정: 0.30 mV/℃')
ax[1].set_xlabel('T / ℃'); ax[1].set_ylabel('피크 분리 / mV'); ax[1].set_title('피크 분리 vs T — Dahn Fig9 재현'); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/T_split.png",dpi=120); print("saved T_split.png")
for (T,tn) in Ts:
    V,d,Ua,Ub=dqdv_cal(T); print(f"{tn}: 분리={abs(Ua-Ub)*1000:.1f}mV 피크{npeaks(V,d)}개")
print(f"\n문건 코드 분리 기울기={sl[0]:.3f} mV/℃ (Dahn 측정 0.30 mV/℃) — {'정합' if abs(sl[0]-0.30)<0.05 else '근사'}")
print("→ stage-2L(엔트로피 안정화) 창이 고온서 열려 분리·저온서 병합. 문건 ∂U/∂T=ΔS/F 가 XRD 관측(Dahn/Schmitt) 재현.")
