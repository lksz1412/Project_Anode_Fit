# -*- coding: utf-8 -*-
"""BDD(BatteryData_Display) dQ/dV 스무딩 방법론 포팅 — 사용자 요청.
원본: lksz1412/BatteryData_Display  Lib_LKS_BatteryData_99_Backend.py
  (WLD 웨이블릿 denoise · dMSMCD 다척도 중앙차분 slope · savgol 앙상블(왕복공간) · 단/광폭 적응 블렌드)
포팅 원칙: 알고리즘 동형 유지(bn.nanmedian→np.nanmedian, @njit→numpy, units 제거).
왜 필요: 단일 savgol 은 (a) 피크 높이 눌림, (b) dV/dQ↔dQ/dV 왕복 시 피크 왜곡. BDD 는 다척도 중앙차분
  + 왕복공간 savgol 앙상블(median[savgol(x), 1/savgol(1/x)]) + 피크위치 가중 단/광폭 블렌드로 이를 완화.
"""
import numpy as np
from scipy.signal import savgol_filter
try:
    import pywt; _HAVE_PYWT = True
except Exception:
    _HAVE_PYWT = False

# ---------- 1. 웨이블릿 denoise (WLD) — 순환이동 앙상블 ----------
def _wld(y, strength, wavelet='bior6.8', mode='soft'):
    y0 = y[1:].copy(); yp = np.pad(y0, 50, mode='edge')
    rolls = np.full((len(yp), 10), np.nan)
    for j in range(10):
        yr = np.roll(yp, j-5)
        coeffs = pywt.wavedec(yr, wavelet)
        detail = coeffs[-1]
        sigma = np.median(np.abs(detail-np.median(detail)))/0.6745
        thr = sigma*np.sqrt(2*np.log(len(y0)))*strength
        nc = [coeffs[0]] + [pywt.threshold(c, thr, mode=mode) for c in coeffs[1:]]
        yd = pywt.waverec(nc, wavelet)
        yd = yd[:len(yr)] if len(yd) > len(yr) else np.pad(yd, (0, len(yr)-len(yd)), mode='edge')
        rolls[:, j] = np.roll(yd, -(j-5))
    out = y.copy(); out[1:] = np.nanmedian(rolls, axis=1)[50:-50]
    return out

def denoise(y, strength, mode='Normal'):
    if not _HAVE_PYWT or strength <= 0: return np.asarray(y, float)
    ws = ['bior2.8','bior3.9','bior6.8','rbio2.8','rbio3.9','rbio6.8'] if mode=='Normal' else ['bior6.8','rbio6.8']
    return np.nanmedian(np.array([_wld(np.asarray(y,float).copy(), strength, w) for w in ws]), axis=0)

# ---------- 2. dMSMCD — 다척도 중앙차분 slope (dy2/dy1) ----------
def dmsmcd(y1, y2, max_window):
    y1=np.asarray(y1,float); y2=np.asarray(y2,float)
    p1=np.pad(y1,1,mode='edge'); p2=np.pad(y2,1,mode='edge')
    i1=(p1[:-1]+p1[1:])/2; i2=(p2[:-1]+p2[1:])/2
    n=len(y1); S=np.full((n,max_window),np.nan)
    for i in range(max_window):
        j=(i+1)//2
        if i%2==0:
            S[(j+1):-(j+1),i]=((i2[(i+1):]-i2[:-(i+1)])/(i1[(i+1):]-i1[:-(i+1)]))[1:-1]
        else:
            S[j:-j,i]=(y2[(i+1):]-y2[:-(i+1)])/(y1[(i+1):]-y1[:-(i+1)])
    return S

def slope_median(y1, y2, max_window):
    return np.nanmedian(dmsmcd(y1, y2, max_window), axis=1)

# ---------- 3. savgol 앙상블 (왕복공간) ----------
def savgol_ensemble(data, ratios, poly=3):
    data=np.asarray(data,float); L=len(data); ens=[data]
    for r in ratios:
        w=int(round(L*r//2,0)*2)+1
        if w<=poly+1 or w>=L: continue
        try: ens.append(savgol_filter(data,w,poly))
        except Exception: pass
        with np.errstate(divide='ignore',invalid='ignore'):
            try:
                inv=1.0/data
                if np.all(np.isfinite(inv)): ens.append(1.0/savgol_filter(inv,w,poly))
            except Exception: pass
    return np.nanmedian(np.array(ens),axis=0)

# ---------- 4. 통합: V-Q 스윕 → dQ/dV·dV/dQ (BDD식) ----------
def dqdv_bdd(t, V, Q, *, denoise_strength=0.0, slope_win_pts=41,
             ratios_shrt=(0.02,0.03,0.04), ratios_wide=(0.03,0.05,0.07), sign=+1,
             dvdq_floor=2e-4):
    """시간정렬 t,V,Q(단조 스윕) → BDD식 dQ/dV(V)·dV/dQ(V).
    dV/dt·dQ/dt = 다척도 중앙차분 median slope → dV/dQ=(dV/dt)/(dQ/dt) → 왕복 savgol 앙상블
      단/광폭 → 피크위치(|1/dVdQ_wide| 큰 곳) 가중 블렌드(피크=광폭 부드럽게, 평지=단폭 보존).
    반환: dict(V, dQdV, dVdQ, dVdQ_shrt, dVdQ_wide)."""
    t=np.asarray(t,float); V=np.asarray(V,float); Q=np.asarray(Q,float)
    if denoise_strength>0:
        V=denoise(V,denoise_strength); Q=denoise(Q,denoise_strength)
    dVdt=slope_median(t,V,slope_win_pts)
    dQdt=slope_median(t,Q,slope_win_pts)
    with np.errstate(divide='ignore',invalid='ignore'):
        dVdQ=dVdt/dQdt
    # 유효(부호 일치·유한) 주구간
    good=np.isfinite(dVdQ)&(dVdQ*sign>0)
    idx=np.where(good)[0]
    if len(idx)<20:
        with np.errstate(divide='ignore',invalid='ignore'):
            return dict(V=V, dQdV=1.0/dVdQ, dVdQ=dVdQ, dVdQ_shrt=dVdQ, dVdQ_wide=dVdQ)
    seg=max(np.split(idx,np.where(np.diff(idx)>1)[0]+1),key=len)
    s,e=int(seg[0]),int(seg[-1])+1
    dVdQ_shrt=dVdQ.copy(); dVdQ_wide=dVdQ.copy()
    dVdQ_shrt[s:e]=savgol_ensemble(dVdQ[s:e],ratios_shrt)
    dVdQ_wide[s:e]=savgol_ensemble(dVdQ[s:e],ratios_wide)
    # 두-상 plateau 에서 dV/dQ→0 → dQ/dV 발산. 물리 상한(dV/dQ 바닥) clip 후 역수(부호 보존).
    def _floor(x):
        xs=np.sign(x); xs[xs==0]=1.0
        return xs*np.maximum(np.abs(x), dvdq_floor)
    dVdQ_shrt_f=_floor(dVdQ_shrt); dVdQ_wide_f=_floor(dVdQ_wide)
    with np.errstate(divide='ignore',invalid='ignore'):
        w=np.abs(1.0/dVdQ_wide_f)
        ratio=np.clip(w/np.nanmax(w[s:e]),0,1)          # 피크(1/dVdQ 큰=dQdV peak)=광폭 가중
        dVdQf=dVdQ_shrt*(1-ratio)+dVdQ_wide*ratio
        dQdVf=1.0/dVdQ_shrt_f*(1-ratio)+1.0/dVdQ_wide_f*ratio
    return dict(V=V, dQdV=dQdVf, dVdQ=dVdQf, dVdQ_shrt=dVdQ_shrt, dVdQ_wide=dVdQ_wide, seg=(s,e))

# ---------- 5b. 피팅용 안정판: 균일 V격자 dQ/dV (BDD 다척도slope + 왕복앙상블, 두-상 특이 회피) ----------
def dqdv_grid_bdd(V, Q, *, dV=0.0005, slope_win_pts=15,
                  ratios=(0.006,0.012,0.02,0.03), denoise_strength=0.0):
    """V-Q 스윕 → 균일 V격자 위 |dQ/dV|(mAh/V). BDD 핵심(다척도 중앙차분 median slope + 왕복공간
    savgol 앙상블)을 V-도메인에서 적용 → 두-상 plateau 시간특이 없이 안정. 단일 savgol 왜곡(피크
    눌림·왕복 편향) 완화. 피팅·파라미터 분포 연구용 표준 추출기.
    반환: (Vgrid, dQdV)."""
    V=np.asarray(V,float); Q=np.asarray(Q,float)
    o=np.argsort(V); Vs,Qs=V[o],Q[o]
    Vu,inv=np.unique(np.round(Vs,6),return_inverse=True)
    Qu=np.array([Qs[inv==k].mean() for k in range(len(Vu))])
    if len(Vu)<10: return Vu, np.zeros_like(Vu)
    grid=np.arange(Vu.min(),Vu.max(),dV); Qg=np.interp(grid,Vu,Qu)
    if denoise_strength>0: Qg=denoise(Qg,denoise_strength)
    # 다척도 중앙차분 median slope: dQ/dV = slope(V→Q)
    dqdv=np.abs(slope_median(grid, Qg, slope_win_pts))
    # NaN(에지) 채움 — 유한값 선형보간
    ok=np.isfinite(dqdv)
    if ok.sum()>=2: dqdv=np.interp(np.arange(len(dqdv)), np.where(ok)[0], dqdv[ok])
    # 왕복공간 savgol 앙상블(피크 눌림/왕복 편향 완화)
    dqdv=np.abs(savgol_ensemble(np.clip(dqdv,1e-9,None), ratios))
    dqdv=np.nan_to_num(dqdv, nan=0.0, posinf=0.0, neginf=0.0)
    return grid, dqdv
