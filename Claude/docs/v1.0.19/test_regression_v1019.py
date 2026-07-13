# -*- coding: utf-8 -*-
"""v1.0.19 흑연 회귀 하네스 — 골든(golden_graphite_ref.npz) 대조 13/13 bit-exact 검증.

[무엇을] `Anode_Fit_v1.0.19.py` 를 import 해 골든 캡처와 동일한 13 케이스
  (V 격자 · equilibrium@298 · dqdv 충/방전×C-rate 6종 · 온도 3종 · 비등온 T(V) ·
   curve facade)를 재산출하고, 본 폴더의 `golden_graphite_ref.npz` 와
  `np.array_equal`(bit-exact, allclose 아님)로 전수 대조한다.
[왜] FITTING_GUIDE §6 "흑연 회귀 0-diff" 게이트의 v1.0.19 실행체 —
  v1.0.19 의 additive 확장(x̄ 진입점 solve_U_oc·entropy_coefficient_x·
  reversible_heat_x·return_terms)이 기존 흑연 경로를 1 bit 도 건드리지 않았음과,
  θ_E(vib Einstein)·n_T1(n(T)) **키 부재 시 bit-exact** 승계를 실증한다
  (GRAPHITE_STAGING_LIT 는 두 키 모두 미보유 — 부재 경로가 곧 골든 경로).
[재현] PYTHONIOENCODING=utf-8 python test_regression_v1019.py            (verify 기본)
        PYTHONIOENCODING=utf-8 python test_regression_v1019.py capture   (골든 재캡처 —
        기존 골든 존재 시 거부; 의도적 수치 변경 시에만 ledger 기록 후 골든 삭제·재캡처)

계보: v1.0.18.2 test_regression_graphite.py 의 v1.0.19 이관(케이스 구성 무변경,
  경로만 스크립트 위치 기준 + 골든 덮어쓰기 방지 가드 추가).
"""
import sys, os, importlib.util, hashlib
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # cp949 콘솔서도 실행 보장
except Exception:
    pass
import numpy as np
_trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))  # numpy 2.x: trapezoid

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.environ.get("ANODEFIT_CODE", os.path.join(HERE, "Anode_Fit_v1.0.19.py"))
GOLD = os.path.join(HERE, "golden_graphite_ref.npz")


def load():
    spec = importlib.util.spec_from_file_location("anodefit_under_test", CODE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def graphite_outputs(m):
    """흑연 base 산출 13 케이스 — 골든 캡처와 동일 구성(0-diff 게이트)."""
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
    """면적=Q assert — baseline 제거 후 ∫dQ/dV dV ≈ ΣQ_j (eq:eqpeak 면적보존)."""
    V = np.linspace(0.03, 0.34, 4000)  # 조밀 격자로 적분 정확도
    model = m.GraphiteAnodeDischargeDQDV(m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.0, Cbg=0.0)
    yeq = np.asarray(model.equilibrium(V, T=298.15), dtype=float)
    area = float(_trapz(yeq, V))
    Qsum = sum(tr['Q'] for tr in m.GRAPHITE_STAGING_LIT)
    return area, Qsum


def absence_check(m):
    """θ_E(vib)·n_T1(n(T)) 키 부재 확인 — 부재 = bit-exact 승계 경로의 전제."""
    has_theta = any('theta_E' in tr for tr in m.GRAPHITE_STAGING_LIT)
    has_nT1 = any('n_T1' in tr for tr in m.GRAPHITE_STAGING_LIT)
    return has_theta, has_nT1


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if mode not in ("capture", "verify"):
        print(f"unknown mode: {mode!r} (capture|verify)"); sys.exit(2)
    m = load()
    out = graphite_outputs(m)
    if mode == "capture":
        if os.path.exists(GOLD):
            print(f"REFUSE: golden already exists — will not overwrite:\n  {GOLD}\n"
                  "  (의도적 수치 변경 시에만 ledger 기록 후 기존 골든을 수동 이동/삭제하고 재캡처)")
            sys.exit(3)
        np.savez(GOLD, **out)
        print(f"GOLDEN CAPTURED: {len(out)} arrays -> {GOLD}")
        for k, v in out.items():
            print(f"  {k:20s} shape={v.shape} sha={hashlib.sha256(v.tobytes()).hexdigest()[:12]}")
        a, q = area_check(m)
        print(f"AREA check: trapz(eq)={a:.6f}  Qsum={q:.6f}  ratio={a/q:.6f}")
        return

    # ---- verify ----
    gold = np.load(GOLD)
    keys_gold = set(gold.files)
    keys_now = set(out.keys())
    if keys_gold != keys_now:
        print(f"KEY-SET MISMATCH: golden={sorted(keys_gold)} vs now={sorted(keys_now)}")
        sys.exit(1)
    all_ok = True
    n_pass = 0
    for k in gold.files:
        eq = np.array_equal(out[k], gold[k])   # bit-exact, NOT allclose
        all_ok &= eq
        if not eq:
            md = float(np.max(np.abs(out[k] - gold[k])))
            print(f"  MISMATCH {k}: max_abs_diff={md:.3e}")
        else:
            n_pass += 1
            print(f"  OK  {k}")
    a, q = area_check(m)
    print(f"AREA check: trapz(eq)={a:.6f}  Qsum={q:.6f}  ratio={a/q:.6f}")
    has_theta, has_nT1 = absence_check(m)
    print(f"theta_E absent in GRAPHITE_STAGING_LIT: {not has_theta}  "
          f"n_T1 absent: {not has_nT1}  (부재 경로 = 골든 경로, bit-exact 전제)")
    print(f"=== GRAPHITE 0-DIFF (v1.0.19 vs golden): {n_pass}/{len(gold.files)} "
          + ("PASS" if all_ok else "FAIL") + " ===")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
