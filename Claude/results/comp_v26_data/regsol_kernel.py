# -*- coding: utf-8 -*-
"""regsol / skew-regsol 커널 — 조성격자 이산화 인공물(꼬리 ripple) 제거판.

문제(사용자 지적 2026-07-27 "왜 regsol 에서만 위글링이 나오냐"):
  regsol dQ/dV = Q * ∫₀¹ κ(V − U(x); w) dx 를 조성격자 합 Σᵢ κ(V − U(xᵢ))·Δx 로 계산하면,
  broadening 폭 w 가 이웃 격자점의 전압 간격 U(xᵢ₊₁)−U(xᵢ) 보다 좁을 때 합이 매끄러운 곡선이
  아니라 빗살(comb)이 된다. 흑연 최급준 전이의 피팅 w ≈ 0.3–0.5 mV 가 정확히 그 조건.
  logistic·skew-logistic 은 해석함수 하나라 이 현상이 없다 — 그래서 regsol 계열에서만 보였다.
  (v1.0.24 원본은 `_REGSOL_XG = ...1200` + 주석 "조밀 격자(꼬리 ripple 억제)" 로 이미 알고 있었다.)

해법: 격자를 키우는 대신 **적분을 분해**한다.
  ① 혼화갭 안(x ∈ [xa, 1−xa]) — U(x) = U0 상수 → 무게 (1−2xa) 의 커널 하나. 격자 무관·정확.
  ② 갭 밖 두 가지 — 조성 밀도를 균일 V 격자에 히스토그램으로 쌓고, 커널과 **합성곱** 1회.
     커널이 (V−U) 만의 함수(병진불변)이므로 이 분해는 근사가 아니라 항등이다.
     x 는 희박극한에서 U ~ −(RT/F)ln x 로 발산하므로 **기하 간격**으로 샘플 —
     그래야 dU 간격이 일정해져 꼬리에서도 빗살이 생기지 않는다.
  → 결과는 조성 샘플 수에 사실상 무관(수렴), 비용은 O(n log n) 로 격자 수와 분리된다.

면적 규약: 창 안에 들어온 전하만 적분되므로 ∫dQ/dV dV ≤ Q (창 밖 희박 꼬리는 누락).
  이는 직접합 방식과 동일한 성질이며, 창을 넓히면 Q 로 수렴한다.
"""
import numpy as np
from scipy.signal import fftconvolve

R, F, T = 8.314, 96485.0, 298.15
RTF = R * T / F

__all__ = ["binodal", "regsol_dqdv", "regsol_density"]


def binodal(a):
    """대칭 정칙용액 binodal x_a: ln(x/(1−x)) + a(1−2x) = 0, a = Ω/RT. a ≤ 2 면 상분리 없음."""
    if a <= 2.0:
        return 0.5
    lo, hi = 1e-12, 0.5 - 1e-13
    for _ in range(90):
        m = 0.5 * (lo + hi)
        if np.log(m / (1 - m)) + a * (1 - 2 * m) > 0: hi = m
        else: lo = m
    return 0.5 * (lo + hi)


def _kernel(dV, w, alpha):
    """평형 미분 종 κ. alpha=1 → 로지스틱 미분, 그 외 → v1.0.25 skew (∫κ dV = 1)."""
    s = 1.0 / (1.0 + np.exp(-np.clip(dV / w, -350.0, 350.0)))
    if alpha == 1.0:
        return s * (1.0 - s) / w
    return (alpha / w) * s ** alpha * (1.0 - s)


def regsol_density(U0, Om, c0, dv, nb, nx=3000):
    """갭 **밖** 고용체 두 가지의 조성 밀도를 균일 전압 빈에 선형 배분(CIC)한다.

    c0 = 0번 빈의 중심, dv = 빈 폭, nb = 빈 개수. 반환 합 ≤ 2·xa(창 밖 누락분 제외).
    단순 histogram 은 U 를 빈 중심으로 반올림해 1차 모멘트를 흘린다 → 선형 배분으로 보존.
    """
    dens = np.zeros(nb)
    xa = binodal(Om / (R * T))
    if xa <= 1e-12:
        return dens
    # 희박측 (0, xa): 꼬리는 기하 간격(U ~ −(RT/F)ln x 라 dU 등간격), 중간은 균등.
    # 기하 단독이면 x→xa 근방이 성겨져 Ω<2RT(갭 없음) 케이스에서 오차가 커진다(실측 1.7%).
    xs = np.unique(np.concatenate([np.geomspace(1e-12, 0.5 * xa, nx // 2),
                                   np.linspace(0.5 * xa, xa, nx - nx // 2)]))
    dx = np.gradient(xs)
    for br, wts in ((xs, dx), (1.0 - xs[::-1], dx[::-1])):
        Ub = U0 - RTF * np.log(br / (1.0 - br)) - (Om / F) * (1.0 - 2.0 * br)
        pos = (Ub - c0) / dv
        k = np.floor(pos).astype(np.int64)
        fr = pos - k
        for kk, ww in ((k, wts * (1.0 - fr)), (k + 1, wts * fr)):
            m = (kk >= 0) & (kk < nb)
            if m.any():
                dens += np.bincount(kk[m], weights=ww[m], minlength=nb)
    return dens


def regsol_dqdv(V, U0, Om, Q, w, alpha=1.0, nx=3000, nsig=14.0):
    """★regsol(alpha=1) / skew-regsol(alpha≠1) dQ/dV. V 는 균일 격자여야 한다.

    갭 항은 닫힌형 κ(V−U0) 로 **해석적으로** 더한다 — 빈에 넣으면 U0 가 최대 dv/2 밀려
    좁은 w 에서 피크가 크게 틀어진다(실측: w=0.4 mV 에서 8.8% 오차).
    """
    V = np.asarray(V, float)
    n = V.size
    if n < 2:
        raise ValueError("V 는 2점 이상 균일 격자여야 한다")
    dv = float(V[1] - V[0])
    w = max(float(w), 1e-9)
    pad = int(np.ceil(nsig * max(w, dv) / dv)) + 2
    nb = n + 2 * pad
    c0 = V[0] - pad * dv

    out = np.zeros(n)
    xa = binodal(Om / (R * T))
    gap_w = max(1.0 - 2.0 * xa, 0.0)
    if gap_w > 0.0:                                   # ① 혼화갭 = 정확한 닫힌형
        out += gap_w * _kernel(V - U0, w, alpha)

    dens = regsol_density(U0, Om, c0, dv, nb, nx=nx)  # ② 고용체 가지 = 밀도 ⊛ 커널
    if dens.any():
        off = (np.arange(2 * pad + 1) - pad) * dv
        ker = _kernel(off, w, alpha)
        # ★fftconvolve 필수: np.convolve 는 O(n·m) 이라 pad ∝ w/dv 가 커지면 폭주한다
        #   (실측 w=120 mV·dv=0.25 mV 에서 1회 805 ms — w=8 mV 대비 2700배 → 피팅이 멈춘다).
        full = fftconvolve(dens, ker, mode="full")    # index i+2·pad ↔ V 격자 i
        out += full[2 * pad: 2 * pad + n]
    return Q * out
