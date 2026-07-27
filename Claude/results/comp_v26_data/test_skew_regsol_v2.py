# -*- coding: utf-8 -*-
"""★사용자 지시 이행(재작성): 'v1.0.24 regsol 식 + v1.0.25 추가분(비대칭) 결합' 커널 테스트.

v1 (test_skew_regsol.py) 폐기 사유 — 결함 3건:
  (1) dQ/dV 를 np.gradient 로 계산했는데 SINTEF V 는 1 uV 양자화(인접 dV 중앙값 8 uV,
      550 쌍은 dV=0) → 0 나눗셈 → dQ/dV 가 1e12 로 발산. 곡선 전체가 무의미했다.
  (2) 비대칭을 dL!=dR 조각폭으로 구현. v1.0.25 가 실제 채택한 것은 alpha 지수형
      (alpha/w)*sigma^alpha*(1-sigma) (Anode_Fit L148-169 func_dxi_eq) — 다른 커널을 시험한 셈.
  (3) skew 커널 정규화가 각각 4x / 2x 틀려 면적=Q 가 깨졌다(v1.0.25 G-alpha2 위반).
  + 피팅 예외를 조용히 삼켜 4종 전부 실패했는데 summary 는 빈 dict 이었다.

본 v2:
  - dQ/dV = BDD(99_Backend) dMSMCD + 웨이블릿 denoise + savgol 앙상블(bdd_dqdv.py)
    → 등장성회귀로 V(Q) 단조화 → 균일 V 격자 재빈닝(양자화 한계 위로 올림).
  - 커널 4종 모두 면적 = Q 정확 보존:
      logistic       : Q*sigma*(1-sigma)/w                    [v1.0.24 기준]
      skew-logistic  : Q*(alpha/w)*sigma^alpha*(1-sigma)      [v1.0.25 C1]
      regsol         : Maxwell 평탄 + 고용체 날개, 폭 w 로 broadening   [v1.0.24]
      ★skew-regsol  : regsol 구조 + alpha 비대칭 broadening    [지시 = 24regsol + 25추가분]
  - 파라미터 수가 다르므로 R^2 단독 비교 금지 → BIC/AIC 병기.
실행: python test_skew_regsol_v2.py
산출: out_v2/{graphite,silicon,blend}_kernels.png · summary_v2.json · report_v2.md
"""
import os, json, time, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
from scipy.optimize import least_squares, isotonic_regression
from scipy.signal import find_peaks
from bdd_dqdv import savgol_ensemble

for _f in ("Malgun Gothic", "Gulim", "NanumGothic"):
    if any(_f.lower() in fn.name.lower() for fn in font_manager.fontManager.ttflist):
        rcParams["font.family"] = _f; break
rcParams["axes.unicode_minus"] = False

R, F, T = 8.314, 96485.0, 298.15
RTF = R * T / F                                   # 25.69 mV
HERE = os.path.dirname(os.path.abspath(__file__))
# 데이터 경로: PC 절대경로 우선, 없으면 리포 상대경로(타 OS·CI 이식).
_D_WIN = r"D:\Projects\Project_Anode_Fit\Claude\results\comp_v24\sintef_data"
_D_REL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "comp_v24", "sintef_data")
DATA = _D_WIN if os.path.isdir(_D_WIN) else os.path.normpath(_D_REL)
OUT = os.path.join(HERE, "out_v2"); os.makedirs(OUT, exist_ok=True)
LOGP = os.path.join(OUT, "run_v2.log"); open(LOGP, "w", encoding="utf-8").close()
_TRAPZ = getattr(np, "trapezoid", None) or np.trapz


def log(m):
    s = str(m)
    try:                                   # 콘솔이 cp949 면 em-dash 등에서 죽는다
        print(s, flush=True)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"), flush=True)
    with open(LOGP, "a", encoding="utf-8") as fh:
        fh.write(s + "\n")


# ────────────────────────────── 데이터 → dQ/dV ──────────────────────────────
def load_dqdv(csv, vlo, vhi, dv):
    """등장성회귀로 V(Q) 단조화 → 균일 V 격자 재빈닝 → BDD savgol 앙상블 평활.

    재빈닝이 핵심: 구간 [V, V+dv) 에 들어온 전하량 / dv 는 양자화(1 uV)와 무관하게
    유한하고 물리적으로 정의된 dQ/dV 다. 점별 미분과 달리 두-상 평탄에서도 발산하지 않는다.
    """
    df = pd.read_csv(csv)
    cv = next(c for c in df.columns if c.lower().startswith("v"))
    cq = next(c for c in df.columns if c.lower().startswith("q"))
    V = df[cv].to_numpy(float); Q = df[cq].to_numpy(float)
    ok = np.isfinite(V) & np.isfinite(Q); V, Q = V[ok], Q[ok]
    o = np.argsort(Q, kind="mergesort"); V, Q = V[o], Q[o]
    Qu, ix = np.unique(Q, return_index=True); Vu = V[ix]
    Vm = isotonic_regression(Vu, increasing=True).x        # 노이즈성 V 역행 제거
    grid = np.arange(vlo, vhi + 0.5 * dv, dv)
    j = np.searchsorted(Vm, grid, side="right") - 1        # 각 격자점까지 누적 전하
    Qg = np.where(j >= 0, Qu[np.clip(j, 0, len(Qu) - 1)], 0.0)
    Vc = 0.5 * (grid[:-1] + grid[1:])
    D = np.diff(Qg) / dv
    keep = np.isfinite(D) & (D > 0)
    # ★균일 격자 보존: 유효점의 최장 연속 구간만 취한다(산발 제거는 격자를 깨뜨린다).
    # regsol 커널이 밀도⊛합성곱이라 V 가 균일해야 한다.
    idx = np.flatnonzero(keep)
    if idx.size == 0:
        raise ValueError("유효 dQ/dV 구간이 없다")
    runs = np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1)
    sl = max(runs, key=len)
    Vc, D = Vc[sl[0]: sl[-1] + 1], D[sl[0]: sl[-1] + 1]
    D = np.abs(savgol_ensemble(D, (0.01, 0.02, 0.03)))     # BDD 앙상블(약)
    return Vc, D, float(np.abs(np.diff(np.unique(Vu))).min())


# ────────────────────────────── 커널 4종 ──────────────────────────────
_XG = np.linspace(1e-4, 1 - 1e-4, 240)


def _binodal(a):
    """대칭 정칙용액 binodal x_a: ln(x/(1-x)) + a(1-2x) = 0, a = Omega/RT. a<=2 면 상분리 없음."""
    if a <= 2.0:
        return 0.5
    lo, hi = 1e-9, 0.5 - 1e-12
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if np.log(m / (1 - m)) + a * (1 - 2 * m) > 0: hi = m
        else: lo = m
    return 0.5 * (lo + hi)


def _sig(V, U, w):
    return 1.0 / (1.0 + np.exp(-np.clip((np.asarray(V, float) - U) / w, -350, 350)))


def k_logistic(V, U, w, Q):
    """v1.0.24 기준 커널. 면적 = Q."""
    s = _sig(V, U, w); return Q * s * (1 - s) / w


def k_skew_logistic(V, U, w, Q, a):
    """v1.0.25 C1 (func_dxi_eq): (alpha/w) sigma^alpha (1-sigma). 면적 = Q, 모든 alpha 에서 정확."""
    s = _sig(V, U, w); return Q * (a / w) * s ** a * (1 - s)


def _regsol_Vi(U0, Om):
    """정칙용액 평형 등온선 U(x): 혼화갭 안은 Maxwell 평탄 U0, 밖은 고용체 가지."""
    xa = _binodal(Om / (R * T))
    inside = (_XG > xa) & (_XG < 1 - xa)
    return np.where(inside, U0, U0 - RTF * np.log(_XG / (1 - _XG)) - (Om / F) * (1 - 2 * _XG))


def k_regsol(V, U0, Om, Q, w):
    """v1.0.24 regsol: 등온선을 폭 w 로 broadening. 면적 = Q (원소당 1/N 정규화)."""
    Vi = _regsol_Vi(U0, Om); w = max(w, 1e-9)
    s = _sig(np.asarray(V, float)[:, None], Vi[None, :], w)
    return (Q / _XG.size) * (s * (1 - s) / w).sum(1)


def k_skew_regsol(V, U0, Om, Q, w, a):
    """★지시 커널 = v1.0.24 regsol 구조 + v1.0.25 alpha 비대칭 broadening. 면적 = Q."""
    Vi = _regsol_Vi(U0, Om); w = max(w, 1e-9)
    s = _sig(np.asarray(V, float)[:, None], Vi[None, :], w)
    return (Q / _XG.size) * ((a / w) * s ** a * (1 - s)).sum(1)


# ────────────────────────────── 피팅 ──────────────────────────────
_rng = np.random.default_rng(7)


def _fit(resid, p0, lb, ub, k=4, nfev=4000, tag=""):
    p0, lb, ub = (np.asarray(x, float) for x in (p0, lb, ub))
    p0 = np.clip(p0, lb, ub)
    best, bcost, errs = None, np.inf, []
    for j in range(k):
        st = p0 if j == 0 else np.clip(p0 * _rng.uniform(0.7, 1.3, p0.size), lb, ub)
        try:
            r = least_squares(resid, st, bounds=(lb, ub), max_nfev=nfev)
            if r.cost < bcost: bcost, best = r.cost, r.x
        except Exception as e:
            errs.append(f"{type(e).__name__}: {e}")
    if best is None:
        log(f"    !! FIT FAILED [{tag}] {errs[:2]}")          # v1 은 이걸 삼켰다
    return best


def _stats(D, P, npar):
    n = D.size; rss = float(np.sum((D - P) ** 2))
    r2 = 1 - rss / float(np.sum((D - D.mean()) ** 2))
    bic = n * np.log(max(rss, 1e-300) / n) + npar * np.log(n)
    aic = n * np.log(max(rss, 1e-300) / n) + 2 * npar
    return round(r2, 5), round(bic, 1), round(aic, 1), rss


def _region_rmse(D, P):
    pk, _ = find_peaks(D, prominence=D.max() * 0.04)
    vl, _ = find_peaks(-D, prominence=D.max() * 0.02)
    def rn(idx, h=5):
        if len(idx) == 0: return float("nan")
        m = np.zeros_like(D, bool)
        for i in idx: m[max(0, i - h): i + h] = True
        return float(np.sqrt(np.mean((D[m] - P[m]) ** 2)))
    return round(rn(pk), 3), round(rn(vl), 3)


def build_models(Vx, Dx, U0s, wlo, whi, uband):
    """전이 N 개에 대해 커널 4종의 (모델함수, p0, lb, ub, 파라미터수) 를 만든다.

    ★U_j 를 초기 추정 ±uband 밴드에 묶는다. 밴드가 없으면 큰 피크가 최소제곱을 지배해
    전이 여러 개가 한 피크로 몰리고 작은 피크(흑연 0.227 V)가 통째로 누락된다(v2 1회차 실측).
    밴드는 staging 전이 위치가 알려져 있다는 물리 사전지식이며, 커널 간 비교를 공정하게 만든다.
    """
    N = len(U0s); A = float(_TRAPZ(Dx, Vx)); lo, hi = Vx.min(), Vx.max()
    q0, qhi, bg0, bghi = A / N, 10 * A, float(Dx.min()), float(Dx.max())
    w0 = 0.004
    ulb = [max(lo, u - uband) for u in U0s]
    uub = [min(hi, u + uband) for u in U0s]
    M = {}

    def mk(fn, extra_p0, extra_lb, extra_ub, npb):
        def model(p):
            out = np.full(Vx.size, p[-1])
            for j in range(N):
                out = out + fn(Vx, *[p[j + k * N] for k in range(npb)])
            return out
        p0 = list(U0s) + extra_p0 + [bg0]
        lb = list(ulb) + extra_lb + [0.0]
        ub = list(uub) + extra_ub + [max(bghi, 1e-9)]
        return model, p0, lb, ub, len(p0)

    M["logistic"] = mk(k_logistic, [w0] * N + [q0] * N,
                       [wlo] * N + [1e-8] * N, [whi] * N + [qhi] * N, 3)
    M["skew-logistic"] = mk(k_skew_logistic, [w0] * N + [q0] * N + [1.0] * N,
                            [wlo] * N + [1e-8] * N + [0.15] * N,
                            [whi] * N + [qhi] * N + [8.0] * N, 4)
    M["regsol"] = mk(k_regsol, [2.4 * R * T] * N + [q0] * N + [w0] * N,
                     [0.0] * N + [1e-8] * N + [wlo] * N,
                     [8 * R * T] * N + [qhi] * N + [whi] * N, 4)
    M["skew-regsol"] = mk(k_skew_regsol, [2.4 * R * T] * N + [q0] * N + [w0] * N + [1.0] * N,
                          [0.0] * N + [1e-8] * N + [wlo] * N + [0.15] * N,
                          [8 * R * T] * N + [qhi] * N + [whi] * N + [8.0] * N, 5)
    return M


COLORS = {"logistic": "darkorange", "skew-logistic": "slateblue",
          "regsol": "seagreen", "skew-regsol": "crimson"}
ORDER = ["logistic", "skew-logistic", "regsol", "skew-regsol"]


def run(name, csv, win, dv, U0s, zoom, uband, wlo=1e-4, whi=0.10):
    log(f"\n[{name}] {os.path.basename(csv)}  window={win} dV={dv*1e3:.2f} mV  N={len(U0s)}"
        f"  U-band=+-{uband*1e3:.0f} mV")
    Vx, Dx, vq = load_dqdv(csv, win[0], win[1], dv)
    log(f"  points={Vx.size}  dQ/dV med={np.median(Dx):.2f} max={Dx.max():.2f}  V-quant={vq*1e6:.1f} uV")
    M = build_models(Vx, Dx, U0s, wlo, whi, uband)
    out = {}
    for key in ORDER:
        model, p0, lb, ub, npar = M[key]
        t0 = time.time()
        p = _fit(lambda q: model(q) - Dx, p0, lb, ub, tag=f"{name}/{key}")
        if p is None: continue
        P = model(p)
        r2, bic, aic, _ = _stats(Dx, P, npar)
        prm, vrm = _region_rmse(Dx, P)
        area = float(_TRAPZ(P, Vx)); areaD = float(_TRAPZ(Dx, Vx))
        out[key] = dict(R2=r2, BIC=bic, AIC=aic, peakRMSE=prm, valleyRMSE=vrm,
                        nparams=npar, area_model=round(area, 4), area_data=round(areaD, 4),
                        params=[round(float(x), 6) for x in p], pred=P)
        log(f"  {key:15s} R2={r2:.5f}  BIC={bic:9.1f}  peakRMSE={prm:8.3f} valleyRMSE={vrm:7.3f}"
            f"  ({npar}p, {time.time()-t0:.0f}s)")

    fig, ax = plt.subplots(1, 2, figsize=(15.5, 5.4))
    for a, xl in zip(ax, (win, zoom)):
        a.plot(Vx, Dx, color="0.1", lw=2.6, label="실측 dQ/dV", zorder=6)
        for k in ORDER:
            if k in out:
                a.plot(Vx, out[k]["pred"], lw=1.7, color=COLORS[k],
                       label=f"{k}  R²={out[k]['R2']:.4f} BIC={out[k]['BIC']:.0f}")
        a.set_xlim(xl); a.set_xlabel("V vs Li"); a.set_ylabel("dQ/dV (mAh/V)"); a.grid(alpha=.3)
        m = (Vx >= xl[0]) & (Vx <= xl[1])
        if m.any(): a.set_ylim(0, Dx[m].max() * 1.15)
        a.legend(fontsize=8)
    ax[0].set_title(f"{name} — 커널 4종 (★skew-regsol = 24regsol + 25비대칭)")
    ax[1].set_title(f"{name} — 피크역 확대")
    fig.tight_layout()
    png = os.path.join(OUT, f"{name}_kernels.png")
    fig.savefig(png, dpi=130); plt.close(fig)
    log(f"  saved {png}")
    return {k: {kk: vv for kk, vv in v.items() if kk != "pred"} for k, v in out.items()}


if __name__ == "__main__":
    log("=== skew-regsol 결합 커널 테스트 v2 (지시 이행 재작성) ===")
    cfg = [
        # (이름, csv, 창, dV, 전이 U0 초기값, 확대창, U 밴드)
        ("graphite", "gr.csv",   (0.060, 0.300), 2.5e-4,
         [0.104, 0.120, 0.141, 0.190, 0.227], (0.090, 0.240), 0.012),
        ("silicon",  "si.csv",   (0.150, 0.700), 1.0e-3,
         [0.260, 0.330, 0.433, 0.470], (0.180, 0.620), 0.050),
        ("blend",    "sigr.csv", (0.060, 0.700), 5.0e-4,
         [0.096, 0.120, 0.135, 0.224, 0.330, 0.422, 0.470], (0.080, 0.520), 0.020),
    ]
    summ = {}
    for name, f, win, dv, U0s, zoom, uband in cfg:
        csv = os.path.join(DATA, f)
        if not os.path.exists(csv):
            log(f"  MISSING {csv}"); continue
        try:
            summ[name] = run(name, csv, win, dv, U0s, zoom, uband)
        except Exception as e:
            import traceback; log(f"  ERR {e}\n{traceback.format_exc()[:1200]}")
    with open(os.path.join(OUT, "summary_v2.json"), "w", encoding="utf-8") as fh:
        json.dump(summ, fh, ensure_ascii=False, indent=2)
    log("\n=== 최종 요약 (BIC 낮을수록 우수 — 파라미터 수 보정) ===")
    for n, d in summ.items():
        if not d: continue
        best = min(d, key=lambda k: d[k]["BIC"])
        log(f"{n:9s} best(BIC) = {best}")
        for k in ORDER:
            if k in d:
                log(f"   {k:15s} R2={d[k]['R2']:.5f} BIC={d[k]['BIC']:9.1f} "
                    f"peak={d[k]['peakRMSE']:8.3f} ({d[k]['nparams']}p)")
    log("DONE")
