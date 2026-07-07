"""P4 흑연 회귀 하네스 — 편입 前 골든 캡처 / 편입 後 byte 일치 검증.
사용: python test_regression_graphite.py capture   (편입 前)
      python test_regression_graphite.py verify    (편입 後, np.array_equal bit 일치)
"""
import sys, importlib.util, hashlib
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # cp949 콘솔서도 실행 보장
except Exception:
    pass
import numpy as np
_trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))  # numpy 2.x: trapezoid

import os
CODE = os.environ.get(
    "ANODEFIT_CODE",
    r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.17\Anode_Fit_v1.0.17.py")
GOLD = r"D:\Projects\Project_Anode_Fit\Claude\docs\v1.0.17\golden_graphite_ref.npz"

def load():
    spec = importlib.util.spec_from_file_location("anodefit_under_test", CODE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def graphite_outputs(m):
    """흑연 base 산출 — 편입 전후 동일해야 함(0-diff 게이트)."""
    V = np.linspace(0.03, 0.34, 1000)
    model = m.GraphiteAnodeDischargeDQDV(
        m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
    out = {}
    out["V"] = V
    out["equilibrium_298"] = np.asarray(model.equilibrium(V, T=298.15), dtype=float)
    for s, name in [(+1, "dis"), (-1, "chg")]:
        for I in (0.02, 0.2, 1.0):
            out[f"dqdv_{name}_I{I}"] = np.asarray(
                model.dqdv(V, T=298.15, I_abs=I, Q_cell=1.0, s=s), dtype=float)
    for Tk in (258.15, 298.15, 318.15):
        out[f"dqdv_T{int(Tk)}"] = np.asarray(
            model.dqdv(V, T=Tk, I_abs=0.2, Q_cell=1.0, s=+1), dtype=float)
    Tprof = np.linspace(288.15, 308.15, V.size)
    out["dqdv_TV"] = np.asarray(model.dqdv(V, T=Tprof, I_abs=0.2, Q_cell=1.0, s=+1), dtype=float)
    out["curve_dis_02C"] = np.asarray(
        model.curve(V, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15), dtype=float)
    return out

def area_check(m):
    """면적=Q assert (P1 §4 결함 해소). baseline 제거 후 적분 ≈ ΣQ_j."""
    V = np.linspace(0.03, 0.34, 4000)  # 조밀 격자로 적분 정확도
    model = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.0, Cbg=0.0)
    yeq = np.asarray(model.equilibrium(V, T=298.15), dtype=float)
    area = float(_trapz(yeq, V))
    Qsum = sum(tr['Q'] for tr in m.GRAPHITE_STAGING_LIT)
    return area, Qsum

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    m = load()
    out = graphite_outputs(m)
    if mode not in ("capture", "verify"):
        print(f"unknown mode: {mode!r} (capture|verify)"); sys.exit(2)
    if mode == "capture":
        np.savez(GOLD, **out)
        print(f"GOLDEN CAPTURED: {len(out)} arrays -> {GOLD}")
        for k, v in out.items():
            print(f"  {k:20s} shape={v.shape} sha={hashlib.sha256(v.tobytes()).hexdigest()[:12]}")
        a, q = area_check(m)
        print(f"AREA check: trapz(eq)={a:.6f}  Qsum={q:.6f}  ratio={a/q:.6f}")
    elif mode == "verify":
        gold = np.load(GOLD)
        all_ok = True
        for k in out:
            eq = np.array_equal(out[k], gold[k])   # bit-exact, NOT allclose
            all_ok &= eq
            if not eq:
                md = float(np.max(np.abs(out[k] - gold[k])))
                print(f"  MISMATCH {k}: max_abs_diff={md:.3e}")
            else:
                print(f"  OK  {k}")
        a, q = area_check(m)
        print(f"AREA check(post): trapz(eq)={a:.6f} Qsum={q:.6f} ratio={a/q:.6f}")
        print("=== GRAPHITE 0-DIFF: " + ("PASS ✓" if all_ok else "FAIL ✗") + " ===")
        sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
