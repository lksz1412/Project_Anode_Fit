# -*- coding: utf-8 -*-
"""★사용자 지시(2026-07-27): 두 버전을 만들어 docs 버전 폴더에 넣는다.

  버전 A = regsol : 흑연 **물리 4전이**(XRD staging)가 7-peak 분화를 스스로 모사하는 판
  버전 B = gallery: **로지스틱 흑연 7 + 실리콘 7**(= 14) 경험적 gallery 판

두 판 모두 같은 공개 데이터(SINTEF Zenodo 20086298, CC-BY-4.0)에 같은 절차로 피팅하고,
같은 지표(R²·BIC·피크/벨리 RMSE)로 보고한다 → 회사에서 GitHub 로 나란히 비교 가능.

산출: out_versions/{A_regsol,B_gallery}/*.png + params_*.json + 요약 md 소스
"""
import os, json, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
from scipy.optimize import least_squares
from scipy.signal import find_peaks

from test_skew_regsol_v2 import load_dqdv, k_logistic, k_skew_logistic, DATA, _TRAPZ
from regsol_kernel import regsol_dqdv, binodal

for _f in ("Malgun Gothic", "Gulim", "NanumGothic"):
    if any(_f.lower() in fn.name.lower() for fn in font_manager.fontManager.ttflist):
        rcParams["font.family"] = _f; break
rcParams["axes.unicode_minus"] = False

R, T = 8.314, 298.15; RT = R * T
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out_versions"); os.makedirs(OUT, exist_ok=True)
LOGP = os.path.join(OUT, "build.log"); open(LOGP, "w", encoding="utf-8").close()
_rng = np.random.default_rng(23)


def log(m):
    s = str(m)
    try: print(s, flush=True)
    except UnicodeEncodeError: print(s.encode("ascii", "replace").decode("ascii"), flush=True)
    with open(LOGP, "a", encoding="utf-8") as fh: fh.write(s + "\n")


# ── 소재 설정 ──────────────────────────────────────────────────────────────
MATS = {
    "graphite": dict(csv="gr.csv", win=(0.060, 0.300), dv=2.5e-4, zoom=(0.090, 0.245)),
    "silicon":  dict(csv="si.csv", win=(0.150, 0.700), dv=1.0e-3, zoom=(0.180, 0.620)),
    "blend":    dict(csv="sigr.csv", win=(0.060, 0.700), dv=5.0e-4, zoom=(0.080, 0.520)),
}
WLO, WHI = 1e-4, 0.12


def model_logistic(Vx, N):
    def f(p):
        out = np.full(Vx.size, p[-1])
        for j in range(N):
            out = out + k_logistic(Vx, p[j], p[N + j], p[2 * N + j])
        return out
    return f


def model_skewlogistic(Vx, N):
    """v1.0.25 @2 skew(alpha) 반영판. 블록 순서 = U, w, Q, alpha, bg (bounds_and_seed 와 동일)."""
    def f(p):
        out = np.full(Vx.size, p[-1])
        for j in range(N):
            out = out + k_skew_logistic(Vx, p[j], p[N + j], p[2 * N + j], p[3 * N + j])
        return out
    return f


def model_regsol(Vx, N):
    def f(p):
        out = np.full(Vx.size, p[-1])
        for j in range(N):
            out = out + regsol_dqdv(Vx, p[j], p[N + j], p[2 * N + j], p[3 * N + j], 1.0)
        return out
    return f


def fit(kind, N, Vx, Dx, upks, restarts=4, nfev=6000):
    """★스윕(test_gallery_vs_regsol)의 3-시드전략 × restarts 루틴을 그대로 재사용한다.

    단일 시드로는 국소최적에 갇힌다 — 흑연 regsol-4 가 단일시드 BIC 3009 vs 다중시드 2610
    으로 갈렸다(실측). 두 버전을 공정하게 비교하려면 같은 탐색 강도를 써야 한다.
    """
    import test_gallery_vs_regsol as SW
    f = {"logistic": model_logistic, "skew-logistic": model_skewlogistic,
         "regsol": model_regsol}[kind](Vx, N)
    best, bc = None, np.inf
    for useeds in SW.seed_sets(Vx, Dx, N, upks):
        p0, lb, ub = SW.bounds_and_seed(kind, N, Vx, Dx, useeds)
        for j in range(restarts):
            st = p0 if j == 0 else np.clip(p0 * _rng.uniform(0.75, 1.25, p0.size), lb, ub)
            try:
                r = least_squares(lambda q: f(q) - Dx, st, bounds=(lb, ub), max_nfev=nfev)
                if r.cost < bc: bc, best = r.cost, r.x
            except Exception as e:
                log(f"      fit 예외 {type(e).__name__}: {e}")
    if best is None: return None
    P = f(best); n = Dx.size
    rss = float(np.sum((Dx - P) ** 2))
    r2 = 1 - rss / float(np.sum((Dx - Dx.mean()) ** 2))
    bic = n * np.log(max(rss, 1e-300) / n) + best.size * np.log(n)
    pk, _ = find_peaks(Dx, prominence=Dx.max() * 0.04)
    vl, _ = find_peaks(-Dx, prominence=Dx.max() * 0.02)
    def rn(idx, h=5):
        if len(idx) == 0: return float("nan")
        m = np.zeros_like(Dx, bool)
        for i in idx: m[max(0, i - h): i + h] = True
        return float(np.sqrt(np.mean((Dx[m] - P[m]) ** 2)))
    return dict(kind=kind, N=N, npar=int(best.size), R2=round(r2, 5), BIC=round(bic, 1),
                peakRMSE=round(rn(pk), 3), valleyRMSE=round(rn(vl), 3),
                area_model=round(float(_TRAPZ(P, Vx)), 4),
                area_data=round(float(_TRAPZ(Dx, Vx)), 4), bg=round(float(best[-1]), 6),
                params=[round(float(x), 8) for x in best], pred=P)


def to_transitions(kind, N, p):
    """v1.0.25 코드가 그대로 먹는 전이 dict 리스트로 변환."""
    p = np.array(p); out = []
    for j in range(N):
        if kind == "logistic":
            out.append(dict(U=round(float(p[j]), 6), w=round(float(p[N + j]), 6),
                            Q=round(float(p[2 * N + j]), 6)))
        elif kind == "skew-logistic":
            out.append(dict(U=round(float(p[j]), 6), w=round(float(p[N + j]), 6),
                            Q=round(float(p[2 * N + j]), 6),
                            alpha=round(float(p[3 * N + j]), 6)))
        else:
            Om = float(p[N + j])
            out.append(dict(U=round(float(p[j]), 6), Omega=round(Om, 2),
                            Q=round(float(p[2 * N + j]), 6), w=round(float(p[3 * N + j]), 6),
                            Omega_over_RT=round(Om / RT, 3),
                            two_phase=bool(Om > 2 * RT),
                            x_binodal=round(binodal(Om / RT), 4)))
    return sorted(out, key=lambda d: d["U"])


def load(mat):
    c = MATS[mat]
    Vx, Dx, vq = load_dqdv(os.path.join(DATA, c["csv"]), c["win"][0], c["win"][1], c["dv"])
    pk, _ = find_peaks(Dx, prominence=Dx.max() * 0.02)
    upks = list(Vx[pk][np.argsort(-Dx[pk])])
    return Vx, Dx, upks, c


def plot(tag, mat, Vx, Dx, r, color, outdir, extra=None):
    c = MATS[mat]
    fig, ax = plt.subplots(1, 2, figsize=(15.5, 5.4))
    for a, xl in zip(ax, (c["win"], c["zoom"])):
        a.plot(Vx, Dx, color="0.1", lw=2.6, label="실측 dQ/dV", zorder=6)
        a.plot(Vx, r["pred"], lw=2.0, color=color,
               label=f"{tag}  R²={r['R2']:.5f}  BIC={r['BIC']:.0f}  ({r['npar']}p)")
        if extra is not None:
            a.plot(Vx, extra[1], lw=1.5, ls="--", color="0.45", label=extra[0])
        # 전이별 성분
        N = r["N"]; p = np.array(r["params"])
        for j in range(N):
            if r["kind"] == "logistic":
                comp = k_logistic(Vx, p[j], p[N + j], p[2 * N + j])
            elif r["kind"] == "skew-logistic":
                comp = k_skew_logistic(Vx, p[j], p[N + j], p[2 * N + j], p[3 * N + j])
            else:
                comp = regsol_dqdv(Vx, p[j], p[N + j], p[2 * N + j], p[3 * N + j], 1.0)
            a.plot(Vx, comp + p[-1], lw=0.9, alpha=0.55, color=color)
        a.set_xlim(xl); a.set_xlabel("V vs Li"); a.set_ylabel("dQ/dV (mAh/V)"); a.grid(alpha=.3)
        m = (Vx >= xl[0]) & (Vx <= xl[1])
        if m.any(): a.set_ylim(0, Dx[m].max() * 1.15)
        a.legend(fontsize=8)
    ax[0].set_title(f"{mat} — {tag} (가는 선 = 전이별 성분)")
    ax[1].set_title(f"{mat} — 피크역 확대")
    fig.tight_layout()
    pth = os.path.join(outdir, f"{mat}_{tag.split()[0]}.png")
    fig.savefig(pth, dpi=130); plt.close(fig)
    log(f"    saved {os.path.basename(pth)}")
    return pth


if __name__ == "__main__":
    dirA = os.path.join(OUT, "A_regsol"); os.makedirs(dirA, exist_ok=True)
    dirB = os.path.join(OUT, "B_gallery"); os.makedirs(dirB, exist_ok=True)
    dirC = os.path.join(OUT, "C_skew"); os.makedirs(dirC, exist_ok=True)
    summary = {"A_regsol": {}, "B_gallery": {}, "C_skew": {}}

    # 버전별 소재 구성 —
    #  A: 흑연 regsol 4(물리 staging) · 실리콘 regsol 4(Ω 가 스스로 상분리 여부 판정) · 블렌드 8
    #  B: 흑연 logistic 7 · 실리콘 logistic 7 (=14) · 블렌드 14
    PLAN = [
        ("A_regsol", dirA, "regsol", {"graphite": 4, "silicon": 4, "blend": 8}, "seagreen"),
        ("B_gallery", dirB, "logistic", {"graphite": 7, "silicon": 7, "blend": 14}, "darkorange"),
        ("C_skew", dirC, "skew-logistic", {"graphite": 7, "silicon": 7, "blend": 14}, "slateblue"),
    ]
    for vname, vdir, kind, ns, color in PLAN:
        log(f"\n{'='*78}\n### {vname}  (kernel={kind})")
        for mat, N in ns.items():
            Vx, Dx, upks, _ = load(mat)
            log(f"  [{mat}] N={N}  points={Vx.size}  검출피크={len(upks)}")
            t0 = time.time()
            r = fit(kind, N, Vx, Dx, upks)
            if r is None:
                log(f"    !! FAILED"); continue
            log(f"    R2={r['R2']:.5f}  BIC={r['BIC']:9.1f}  peakRMSE={r['peakRMSE']}"
                f"  valleyRMSE={r['valleyRMSE']}  ({r['npar']}p, {time.time()-t0:.0f}s)")
            plot(f"{kind}-{N}", mat, Vx, Dx, r, color, vdir)
            trs = to_transitions(kind, N, r["params"])
            summary[vname][mat] = {k: v for k, v in r.items() if k != "pred"}
            summary[vname][mat]["transitions"] = trs
            with open(os.path.join(vdir, f"params_{mat}.json"), "w", encoding="utf-8") as fh:
                json.dump({"material": mat, "kernel": kind, "N": N,
                           "metrics": {k: r[k] for k in ("R2", "BIC", "peakRMSE",
                                                         "valleyRMSE", "npar",
                                                         "area_model", "area_data", "bg")},
                           "transitions": trs}, fh, ensure_ascii=False, indent=2)
            if kind == "regsol":
                tp = sum(1 for d in trs if d["two_phase"])
                log(f"    Ω/RT = {[d['Omega_over_RT'] for d in trs]}  → 두-상 판정 {tp}/{N}")

    with open(os.path.join(OUT, "summary_versions.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
    log("\n=== 두 버전 요약 ===")
    for v in summary:
        for mat, d in summary[v].items():
            log(f"  {v:10s} {mat:9s} N={d['N']:2d} {d['npar']:2d}p  R2={d['R2']:.5f}  BIC={d['BIC']:9.1f}")
    log("DONE")
