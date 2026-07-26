# -*- coding: utf-8 -*-
"""BDD(Project_BatteryData_Display) 99_Backend 방식 dQ/dV — numpy 이식.

원본: Lib_LKS_BatteryData_99_Backend.py 의 dMSMCD/slope(L84-118) +
      _iteration_savgol_ensemble(L124-134) + _iteration_first 의 shrt/wide 혼합(L156-163).

깨진 구현(test_skew_regsol.py)이 놓친 핵심 = **dMSMCD 다중창 중앙값 미분**.
SINTEF CSV 는 V 가 1 uV 로 양자화돼 있어(인접 dV 중앙값 8 uV, 550 쌍은 dV=0)
단일창 미분(np.gradient)으로 dV/dQ 를 구하면 0 나눗셈 → dQ/dV 가 1e12 로 발산한다.
다중창(1..max_window) 중앙값은 창이 넓어질수록 dV 가 양자화 눈금을 넘어서므로 이를 흡수한다.

시간축이 없는 (V,Q) CSV 에서는 정전류(C/50) 가정으로 t ∝ Q 이므로
BDD 의 dV/dQ = dVdt/dQdt 를 slope(y1=Q, y2=V) 로 직접 대체한다.
"""
import numpy as np
from scipy.signal import savgol_filter

try:
    import pywt
except Exception:  # pywt 부재 시 denoise 는 항등으로 강등(호출부가 경고)
    pywt = None

__all__ = ["dmsmcd_slope", "savgol_ensemble", "denoise", "bdd_dqdv"]


def _wld(y, strength, wavelet="bior6.8", mode="soft"):
    """원본 WLD(L48-69): 10-shift 순환 + universal threshold 웨이블릿 축소, shift 중앙값."""
    y = np.asarray(y, float)
    core = y[1:].copy()
    pad = np.pad(core, 50, mode="edge")
    rolls = np.full((len(pad), 10), np.nan)
    for j in range(10):
        yr = np.roll(pad, j - 5)
        coeffs = pywt.wavedec(yr, wavelet)
        detail = coeffs[-1]
        sigma = np.median(np.abs(detail - np.median(detail))) / 0.6745
        thr = sigma * np.sqrt(2 * np.log(len(core))) * strength
        new = [coeffs[0]] + [pywt.threshold(c, thr, mode=mode) for c in coeffs[1:]]
        rec = pywt.waverec(new, wavelet)
        if len(rec) > len(yr):
            rec = rec[: len(yr)]
        elif len(rec) < len(yr):
            rec = np.pad(rec, (0, len(yr) - len(rec)), mode="edge")
        rolls[:, j] = np.roll(rec, -(j - 5))
    out = y.copy()
    out[1:] = np.nanmedian(rolls, axis=1)[50:-50]
    return out


def denoise(y, strength, mode="Normal"):
    """원본 denoise(L71-78): 여러 웨이블릿의 WLD 결과를 중앙값 결합."""
    if pywt is None:
        return np.asarray(y, float)
    fams = ["bior6.8", "rbio6.8"] if mode == "Speed" else [
        a + b for a in ("bior", "rbio") for b in ("2.8", "3.9", "6.8")]
    return np.nanmedian(np.array([_wld(y, strength, w) for w in fams]), axis=0)


def dmsmcd_slope(y1, y2, max_window=51):
    """dMSMCD: 창 폭 1..max_window 의 중심차분 기울기 dy2/dy1 을 만들고 창 방향 중앙값.

    원본 dMSMCD(L84-96) 를 그대로 옮긴 것 — 짝수 i 는 midpoint 격자, 홀수 i 는 원 격자.
    """
    y1 = np.asarray(y1, float)
    y2 = np.asarray(y2, float)
    n = len(y1)
    p1 = np.pad(y1, 1, mode="edge")
    p2 = np.pad(y2, 1, mode="edge")
    i1 = (p1[:-1] + p1[1:]) / 2.0
    i2 = (p2[:-1] + p2[1:]) / 2.0

    slopes = np.full((n, max_window), np.nan, dtype=np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        for i in range(max_window):
            j = (i + 1) // 2
            if i % 2 == 0:
                num = i2[(i + 1):] - i2[: -(i + 1)]
                den = i1[(i + 1):] - i1[: -(i + 1)]
                slopes[(j + 1): -(j + 1), i] = (num / den)[1:-1]
            else:
                num = y2[(i + 1):] - y2[: -(i + 1)]
                den = y1[(i + 1):] - y1[: -(i + 1)]
                slopes[j:-j, i] = num / den
    slopes[~np.isfinite(slopes)] = np.nan
    with np.errstate(invalid="ignore"):
        return np.nanmedian(slopes, axis=1)


def savgol_ensemble(data, ratios):
    """원본 _iteration_savgol_ensemble(L124-134): 직접 평활 + 역수 평활의 중앙값 앙상블."""
    L = len(data)
    ens = [np.asarray(data, float)]
    for r in ratios:
        w = int(round(L * r // 2)) * 2 + 1
        if w <= 3 or w >= L:
            continue
        try:
            ens.append(savgol_filter(data, w, 3))
        except Exception:
            pass
        try:
            with np.errstate(divide="ignore", invalid="ignore"):
                ens.append(1.0 / savgol_filter(1.0 / data, w, 3))
        except Exception:
            pass
    arr = np.array(ens, dtype=float)
    arr[~np.isfinite(arr)] = np.nan
    with np.errstate(invalid="ignore"):
        return np.nanmedian(arr, axis=0)


def bdd_dqdv(V, Q, max_window=51, strength=1.0, shrt=(0.02, 0.03, 0.04),
             wide=(0.03, 0.05, 0.07), return_info=False):
    """(V,Q) → (V, dQ/dV). 반환 dQ/dV 는 양수 규약(탈리튬화 세그먼트).

    1) Q 오름차순 정렬 · Q 중복 제거
    2) dMSMCD 다중창 중앙값으로 dV/dQ
    3) 웨이블릿 denoise (원본 L141 — dVdt 에 거는 것과 같은 위치)
    4) 부호 일관 최장 구간만 채택 (원본 L147-153 eff_id/main_chunk)
    5) shrt/wide savgol 앙상블 2종 → 피크 가중 ratio 로 혼합 (원본 L156-163)

    ★계측 한계: V 가 dV_quant 로 양자화돼 있으면 분해 가능한 dQ/dV 에 천장이 있다.
    천장 = (창 폭 x dQ) / dV_quant. 그 위는 측정이 아니라 수치 인공물이므로
    `info['ceiling']` 으로 보고하고 초과점은 잘라낸다(조용한 클램프 X).
    """
    V = np.asarray(V, float)
    Q = np.asarray(Q, float)
    ok = np.isfinite(V) & np.isfinite(Q)
    V, Q = V[ok], Q[ok]
    order = np.argsort(Q, kind="mergesort")
    V, Q = V[order], Q[order]
    Qu, idx = np.unique(Q, return_index=True)
    Vu = V[idx]
    if len(Qu) < 50:
        return (None, None, {}) if return_info else (None, None)

    dVdQ = dmsmcd_slope(Qu, Vu, max_window=max_window)
    fin = np.isfinite(dVdQ)
    if fin.sum() < 50:
        return (None, None, {}) if return_info else (None, None)
    dVdQ[~fin] = np.interp(np.flatnonzero(~fin), np.flatnonzero(fin), dVdQ[fin])
    dVdQ = denoise(dVdQ, strength)

    # (4) 부호 일관 최장 구간
    sign = 1.0 if np.nanmedian(dVdQ) > 0 else -1.0
    eff = np.flatnonzero(dVdQ * sign > 0)
    if len(eff) < 50:
        return (None, None, {}) if return_info else (None, None)
    chunks = np.split(eff, np.flatnonzero(np.diff(eff) > 1) + 1)
    main = max(chunks, key=len)
    sl = slice(int(main[0]), int(main[-1]) + 1)
    Vu, Qu, dVdQ = Vu[sl], Qu[sl], dVdQ[sl]
    # 구간 내 잔여 반대부호는 보간으로 메움(원본은 chunk 내부를 그대로 씀)
    bad = ~(dVdQ * sign > 0)
    if bad.any() and (~bad).sum() > 10:
        dVdQ[bad] = np.interp(np.flatnonzero(bad), np.flatnonzero(~bad), dVdQ[~bad])

    d_shrt = savgol_ensemble(dVdQ, shrt)
    d_wide = savgol_ensemble(dVdQ, wide)
    with np.errstate(divide="ignore", invalid="ignore"):
        inv_wide = np.abs(1.0 / d_wide)
        ratio = np.clip(inv_wide / np.nanmax(inv_wide), 0, 1)
        dQdV = np.abs(1.0 / d_shrt * (1 - ratio) + 1.0 / d_wide * ratio)

    # (★) 계측 분해 천장
    dv_q = np.diff(np.unique(V))
    dv_quant = float(np.min(dv_q[dv_q > 0])) if (dv_q > 0).any() else 0.0
    dq = float(np.median(np.diff(Qu))) if len(Qu) > 1 else 0.0
    ceiling = (max_window * dq / dv_quant) if dv_quant > 0 else np.inf

    keep = np.isfinite(Vu) & np.isfinite(dQdV) & (dQdV <= ceiling)
    info = {"ceiling": ceiling, "dv_quant": dv_quant, "dq_median": dq,
            "n_over_ceiling": int((np.isfinite(dQdV) & (dQdV > ceiling)).sum()),
            "n": int(keep.sum()), "sign": sign}
    if return_info:
        return Vu[keep], dQdV[keep], info
    return Vu[keep], dQdV[keep]
