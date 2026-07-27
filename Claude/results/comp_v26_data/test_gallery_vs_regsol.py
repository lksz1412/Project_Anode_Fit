# -*- coding: utf-8 -*-
"""★핵심 질문: regsol 은 '물리 전이 4개' 로 'gallery 7개' 일을 대신하는가?

사용자 지적(2026-07-27): "regsol 은 4피크가 7피크처럼 쪼개지는 것을 모사하는지가 중요한 건데?"
→ v2 는 4종 커널을 같은 N 으로 비교해서 이 질문을 아예 묻지 못했다. 본 v3 는 N 을 스윕한다.

가설의 근거(코드 실물):
  GRAPHITE_STAGING_MSMR6_LIT 는 물리 위치 4개 중 2개를 폭이 크게 다른 쌍으로 쪼갠 것 —
    U=0.128/w=0.0170 + U=0.126/w=0.0022   (같은 위치, 폭 8배)
    U=0.089/w=0.0041 + U=0.089/w=0.0012   (같은 위치, 폭 3배)
  '좁은 코어 + 넓은 날개' = 정칙용액 두-상 커널(Maxwell 평탄 + 고용체 가지)이 원래 하나로 내는 모양.
  → gallery 쌍 쪼개기가 regsol 하나로 흡수되면, regsol 은 '곡선 표현' 이 아니라
    '물리 파라미터 절약' 을 사는 것이고 되살릴 근거가 된다.

판정 규약:
  - 비교는 BIC(파라미터 수 보정). 파라미터 수 = logistic 3N+1 · skew-logistic 4N+1
    · regsol 4N+1 · skew-regsol 5N+1.
  - 핵심 대조 = regsol-4(17p) vs logistic-7(22p) · skew-regsol-4(21p) vs logistic-7(22p).
  - U 는 자유(밴드 X). gallery 근축퇴(같은 U 에 폭 다른 쌍)가 바로 관측 대상이므로
    밴드로 묶으면 검증하려는 현상을 금지하게 된다.
실행: python -X utf8 test_gallery_vs_regsol.py  →  out_v3/
"""
import os, json, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
from scipy.optimize import least_squares
from scipy.signal import find_peaks

from test_skew_regsol_v2 import (load_dqdv, k_logistic, k_skew_logistic, DATA, _TRAPZ)
from regsol_kernel import regsol_dqdv          # ★격자 인공물 제거판(밀도⊛합성곱)
import test_skew_regsol_v2 as V2


def k_regsol(V, U0, Om, Q, w):
    return regsol_dqdv(V, U0, Om, Q, w, 1.0)


def k_skew_regsol(V, U0, Om, Q, w, a):
    return regsol_dqdv(V, U0, Om, Q, w, a)

for _f in ("Malgun Gothic", "Gulim", "NanumGothic"):
    if any(_f.lower() in fn.name.lower() for fn in font_manager.fontManager.ttflist):
        rcParams["font.family"] = _f; break
rcParams["axes.unicode_minus"] = False

R, T = 8.314, 298.15; RT = R * T
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out_v3"); os.makedirs(OUT, exist_ok=True)
LOGP = os.path.join(OUT, "run_v3.log"); open(LOGP, "w", encoding="utf-8").close()


def log(m):
    s = str(m)
    try: print(s, flush=True)
    except UnicodeEncodeError: print(s.encode("ascii", "replace").decode("ascii"), flush=True)
    with open(LOGP, "a", encoding="utf-8") as fh: fh.write(s + "\n")


# 커널 정의: (함수, 전이당 파라미터 수, 추가 파라미터 이름)
KERNELS = {
    "logistic":      (k_logistic,      3, []),
    "skew-logistic": (k_skew_logistic, 4, ["alpha"]),
    "regsol":        (k_regsol,        4, ["Omega"]),
    "skew-regsol":   (k_skew_regsol,   5, ["Omega", "alpha"]),
}
COLORS = {"logistic": "darkorange", "skew-logistic": "slateblue",
          "regsol": "seagreen", "skew-regsol": "crimson"}

WLO, WHI = 1e-4, 0.12
_rng = np.random.default_rng(11)


def make_model(kern, N, Vx):
    fn, npb, _ = KERNELS[kern]
    def model(p):
        out = np.full(Vx.size, p[-1])
        for j in range(N):
            out = out + fn(Vx, *[p[j + k * N] for k in range(npb)])
        return out
    return model


def bounds_and_seed(kern, N, Vx, Dx, useeds):
    """파라미터 블록 순서: [U]*N, (커널별 중간블록)*N, ..., bg."""
    A = float(_TRAPZ(Dx, Vx)); lo, hi = float(Vx.min()), float(Vx.max())
    q0, qhi = A / N, 10 * A
    bg0, bghi = float(Dx.min()), float(max(Dx.max(), 1e-9))
    U = list(useeds)
    if kern == "logistic":          # U, w, Q
        p0 = U + [0.004] * N + [q0] * N
        lb = [lo] * N + [WLO] * N + [1e-9] * N
        ub = [hi] * N + [WHI] * N + [qhi] * N
    elif kern == "skew-logistic":   # U, w, Q, alpha
        p0 = U + [0.004] * N + [q0] * N + [1.0] * N
        lb = [lo] * N + [WLO] * N + [1e-9] * N + [0.15] * N
        ub = [hi] * N + [WHI] * N + [qhi] * N + [8.0] * N
    elif kern == "regsol":          # U0, Omega, Q, w
        p0 = U + [2.4 * RT] * N + [q0] * N + [0.004] * N
        lb = [lo] * N + [0.0] * N + [1e-9] * N + [WLO] * N
        ub = [hi] * N + [8 * RT] * N + [qhi] * N + [WHI] * N
    else:                           # skew-regsol: U0, Omega, Q, w, alpha
        p0 = U + [2.4 * RT] * N + [q0] * N + [0.004] * N + [1.0] * N
        lb = [lo] * N + [0.0] * N + [1e-9] * N + [WLO] * N + [0.15] * N
        ub = [hi] * N + [8 * RT] * N + [qhi] * N + [WHI] * N + [8.0] * N
    # ★수정(2026-07-27, N10): 배경 bg 를 실제 파라미터로 append 한다.
    #   종전에는 bg0/bghi 를 계산만 하고 p0/lb/ub 에 넣지 않아, make_model 의 p[-1] 이
    #   자유 배경이 아니라 **직전 블록의 마지막 값**을 aliasing 했다
    #   (logistic → 마지막 Q≈0.76 / regsol → 마지막 w≈0.0016 / skew 계열 → 마지막 alpha).
    #   곧 커널마다 다른 양이 배경 노릇을 해 비교가 교란됐고, 벨리역이 특히 망가졌다.
    #   bg 는 맨 끝에만 붙으므로 커널 블록 인덱스(p[j + k*N])는 영향받지 않는다.
    p0 = p0 + [bg0]
    lb = lb + [min(0.0, bg0)]          # denoise 잔여로 bg0<0 이 나와도 시드가 경계 밖이 되지 않게
    ub = ub + [bghi]
    return (np.clip(np.array(p0, float), lb, ub),
            np.array(lb, float), np.array(ub, float))


def seed_sets(Vx, Dx, N, npeak_pos):
    """U 시드 3전략: (a) 검출 피크 + 보충, (b) 균등, (c) 피크 우선 + 무게중심."""
    lo, hi = float(Vx.min()), float(Vx.max())
    a = list(npeak_pos)[:N]
    while len(a) < N: a.append(lo + (hi - lo) * (len(a) + 0.5) / (N + 1))
    b = list(np.linspace(lo + 0.05 * (hi - lo), hi - 0.05 * (hi - lo), N))
    c = list(npeak_pos)[:N]
    while len(c) < N:                               # 큰 피크 근처를 겹쳐 시드(gallery 쌍 유도)
        c.append(float(npeak_pos[len(c) % max(len(npeak_pos), 1)]) * (1 + 0.01 * len(c)))
    return [a, b, c[:N]]


def fit_one(kern, N, Vx, Dx, peaks, restarts=3, nfev=4000):
    best, bcost = None, np.inf
    model = make_model(kern, N, Vx)
    for useeds in seed_sets(Vx, Dx, N, peaks):
        p0, lb, ub = bounds_and_seed(kern, N, Vx, Dx, useeds)
        for j in range(restarts):
            st = p0 if j == 0 else np.clip(p0 * _rng.uniform(0.75, 1.25, p0.size), lb, ub)
            try:
                r = least_squares(lambda q: model(q) - Dx, st, bounds=(lb, ub), max_nfev=nfev)
                if r.cost < bcost: bcost, best = r.cost, r.x
            except Exception:
                pass
    if best is None: return None
    P = model(best); n = Dx.size
    rss = float(np.sum((Dx - P) ** 2))
    r2 = 1 - rss / float(np.sum((Dx - Dx.mean()) ** 2))
    npar = best.size
    bic = n * np.log(max(rss, 1e-300) / n) + npar * np.log(n)
    return dict(kern=kern, N=N, npar=int(npar), R2=round(r2, 5), BIC=round(bic, 1),
                params=[round(float(x), 6) for x in best], pred=P)


def degeneracy(kern, N, params):
    """gallery 근축퇴 진단: |dU| < 5 mV 인데 폭 비 > 2 인 쌍의 개수."""
    p = np.array(params); U = p[:N]
    w = p[3 * N:4 * N] if kern in ("regsol", "skew-regsol") else p[N:2 * N]
    pairs = []
    for i in range(N):
        for j in range(i + 1, N):
            du = abs(U[i] - U[j]); rw = max(w[i], w[j]) / max(min(w[i], w[j]), 1e-12)
            if du < 0.005 and rw > 2.0:
                pairs.append((round(U[i] * 1e3, 1), round(U[j] * 1e3, 1),
                              round(w[i] * 1e3, 2), round(w[j] * 1e3, 2), round(rw, 1)))
    return pairs


def sweep(name, csv, win, dv, nmax):
    log(f"\n{'='*78}\n[{name}] 전이 수 스윕  window={win}  dV={dv*1e3:.2f} mV")
    Vx, Dx, vq = load_dqdv(csv, win[0], win[1], dv)
    pk, _ = find_peaks(Dx, prominence=Dx.max() * 0.02)
    peaks = list(Vx[pk][np.argsort(-Dx[pk])])
    log(f"  points={Vx.size}  검출 피크 {len(peaks)}개 @ {np.round(np.sort(Vx[pk])*1e3,1)} mV")
    res, preds = [], {}
    for kern, nrange in nmax.items():
        for N in nrange:
            t0 = time.time()
            r = fit_one(kern, N, Vx, Dx, peaks)
            if r is None:
                log(f"  {kern:14s} N={N}  FAILED"); continue
            preds[(kern, N)] = r.pop("pred")
            r["degen_pairs"] = degeneracy(kern, N, r["params"])
            res.append(r)
            log(f"  {kern:14s} N={N}  {r['npar']:2d}p  R2={r['R2']:.5f}  BIC={r['BIC']:9.1f}"
                f"  근축퇴쌍={len(r['degen_pairs'])}  ({time.time()-t0:.0f}s)")
    return Vx, Dx, res, preds


def plot_sweep(name, Vx, Dx, res, preds):
    fig, ax = plt.subplots(1, 2, figsize=(15.5, 5.6))
    for kern in KERNELS:
        pts = sorted([(r["N"], r["BIC"]) for r in res if r["kern"] == kern])
        if pts:
            ax[0].plot([p[0] for p in pts], [p[1] for p in pts], "o-",
                       color=COLORS[kern], lw=2, ms=6, label=kern)
    ax[0].set_xlabel("전이 수 N"); ax[0].set_ylabel("BIC (낮을수록 우수)")
    ax[0].set_title(f"{name} — 전이 수 대 BIC : regsol 이 N 을 줄여주는가?")
    ax[0].grid(alpha=.3); ax[0].legend(fontsize=9)

    # 핵심 대조: logistic 최량 vs regsol-4 vs skew-regsol-4
    ax[1].plot(Vx, Dx, color="0.1", lw=2.6, label="실측 dQ/dV", zorder=6)
    show = []
    lg = [r for r in res if r["kern"] == "logistic"]
    if lg: show.append(min(lg, key=lambda r: r["BIC"]))
    for kern in ("regsol", "skew-regsol", "skew-logistic"):
        c = [r for r in res if r["kern"] == kern and r["N"] == 4]
        if c: show.append(c[0])
    for r in show:
        ax[1].plot(Vx, preds[(r["kern"], r["N"])], lw=1.8, color=COLORS[r["kern"]],
                   label=f"{r['kern']}-{r['N']} ({r['npar']}p) R²={r['R2']:.4f} BIC={r['BIC']:.0f}")
    ax[1].set_title(f"{name} — 물리 4전이 커널 vs logistic 최량 gallery")
    ax[1].set_xlabel("V vs Li"); ax[1].set_ylabel("dQ/dV (mAh/V)")
    ax[1].grid(alpha=.3); ax[1].legend(fontsize=8)
    fig.tight_layout()
    p = os.path.join(OUT, f"{name}_sweep.png"); fig.savefig(p, dpi=130); plt.close(fig)
    log(f"  saved {p}")


if __name__ == "__main__":
    log("=== regsol = gallery 쌍 쪼개기의 물리적 대체인가? (전이 수 스윕) ===")
    nmax = {"logistic":      range(3, 9),
            "skew-logistic": range(3, 8),
            "regsol":        range(3, 8),
            "skew-regsol":   range(3, 7)}
    allres = {}
    for name, f, win, dv in [("graphite", "gr.csv", (0.060, 0.300), 2.5e-4)]:
        Vx, Dx, res, preds = sweep(name, os.path.join(DATA, f), win, dv, nmax)
        plot_sweep(name, Vx, Dx, res, preds)
        allres[name] = res

        log(f"\n--- [{name}] 핵심 대조 ---")
        def get(k, N):
            c = [r for r in res if r["kern"] == k and r["N"] == N]
            return c[0] if c else None
        lg = [r for r in res if r["kern"] == "logistic"]
        blg = min(lg, key=lambda r: r["BIC"]) if lg else None
        if blg: log(f"  logistic 최량      : N={blg['N']} ({blg['npar']}p) R2={blg['R2']:.5f} BIC={blg['BIC']}")
        for k in ("regsol", "skew-regsol", "skew-logistic"):
            r = get(k, 4)
            if r and blg:
                verdict = "★대체 성공" if r["BIC"] <= blg["BIC"] else "대체 실패"
                log(f"  {k:14s} N=4 ({r['npar']:2d}p) R2={r['R2']:.5f} BIC={r['BIC']:9.1f}"
                    f"  vs logistic-{blg['N']} → {verdict} (dBIC={r['BIC']-blg['BIC']:+.1f})")
        log(f"\n--- [{name}] gallery 근축퇴(같은 U·다른 폭) 검출 ---")
        for r in sorted(res, key=lambda r: (r["kern"], r["N"])):
            if r["degen_pairs"]:
                log(f"  {r['kern']:14s} N={r['N']}: {r['degen_pairs']}")

    with open(os.path.join(OUT, "sweep_v3.json"), "w", encoding="utf-8") as fh:
        json.dump(allres, fh, ensure_ascii=False, indent=2)
    log("DONE")
