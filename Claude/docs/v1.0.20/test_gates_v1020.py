# -*- coding: utf-8 -*-
"""v1.0.20 하드 게이트 하네스 — G1·G2·G3 전건 수치 증빙 (doc-leads: 문건 v1.0.20 부록 B 요구명세).

[G1 하위호환] 신기능(θ_E·n_T1) 전부 미지정 상태에서 v1.0.19 모듈과 동일 입력 그리드 출력 비교
  — 전 경로(흑연 equilibrium/dqdv/curve/entropy_coefficient(+return_terms)/reversible_heat/
    x̄ 진입점 3종/seed_L_V + LCO equilibrium/curve/entropy_coefficient) max|Δ| ≤ 1e-12.
    보조: v1.0.19 골든(golden_graphite_ref.npz, 원 캡처 머신 기준) 대비 ≤ 1e-12
    (본 컨테이너 환경 잡음 기준 P0: ≤ 4.33e-15 — RESULT_P0_setup.md).
[G2 회귀 기준 — ch2_appB B.2, 표시 정밀도 일치] 298.15 K·4-전이 staging·w=RT/F 에서
  U_oc(x̄=0.25)=74.4 mV / ∂U_oc/∂T 완전식 −0.204·단순식 −0.134·config −0.070 mV/K /
  round-trip [U(T+3)−U(T−3)]/6K=−0.204·해석식과 <0.001 µV/K / ΔS=−19.7 J/mol/K·
  Q̇_rev/I=+60.8 mV / tab:qrev 5점(U_oc·∂U/∂T·ΔS·Q̇_rev/I 전 열) / tab:worked 중간값 /
  파생 A: x̄∈[0.05,0.95] 175점 완전식 vs 유한차분(T1=292.15·T2=298.15, 해석식 295.15 K 평가
  — 원 검증 42_numerical_verification.md 규약) 표시 정밀도(≲1e-2 mV/K) 일치·내부 경계 3곳
  연속 블렌드(인접 ΔS⁰/F 사이 값·계단 없음).
[G3 θ_E bit-exact] vib 가산 4곳(equilibrium·dqdv·entropy_coefficient·solve_U_oc)을 소스에서
  제거한 '보정 도입 이전' 변형 모듈을 즉석 생성, θ_E 미지정 v1.0.20 과 전 경로 np.array_equal
  (bit-exact) 대조. + 발효 확인(θ_E=700 K: T_ref 서 불변·T≠T_ref 서 변화·C-62 수치
  −3.74/0/+3.70/+9.14 µV/K).
[부록 — n(T) 전파 증빙(ch1_appB)] n_T1 부재=상수 n bit-exact(값 수준)·발효 시
  ∂w/∂T=(R/F)(n(T)+T·n_T1) 해석=수치 일치·n_T1≠0 round-trip 정합.

[재현] PYTHONIOENCODING=utf-8 python test_gates_v1020.py
  (v1.0.19 폴더는 읽기 전용 사용 — sys.dont_write_bytecode 로 pyc 미생성.
   G3 변형 모듈 임시 파일 위치는 env ANODEFIT_TMP 지정 가능, 기본 tempfile.)
"""
import sys, os, importlib.util, tempfile
sys.dont_write_bytecode = True   # v1.0.19 폴더(읽기 전용 취급)에 __pycache__ 미생성
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CODE_V20 = os.path.join(HERE, "Anode_Fit_v1.0.20.py")
CODE_V19 = os.path.normpath(os.path.join(HERE, "..", "v1.0.19", "Anode_Fit_v1.0.19.py"))
GOLD = os.path.normpath(os.path.join(HERE, "..", "v1.0.19", "golden_graphite_ref.npz"))

G1_TOL = 1e-12          # 게이트 문턱(환경 잡음 P0 4.33e-15 여유 포함)
G2_FD_ANALYTIC_UVK = 1e-3   # round-trip |FD-해석| < 0.001 µV/K (B.2)
G2_DERIVA_MVK = 1e-2        # 파생 A 표시 정밀도 ≲ 1e-2 mV/K
G2_STEP_UVK = 25.0          # 경계 국소 계단 부재: 격자 스텝당 < 25 µV/K
                            # (원 검증 최대 13 µV/K/step; 최소 인접 plateau 간격 52 µV/K 미만)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- 공통 출력셋
def output_set(m):
    """v1.0.19/v1.0.20/변형 모듈 공통 산출 사전 — 신기능 전부 미지정(θ_E·n_T1 無)."""
    V = np.linspace(0.03, 0.34, 1000)
    xg = np.linspace(0.05, 0.95, 91)
    Tprof = np.linspace(288.15, 308.15, V.size)
    model = m.GraphiteAnodeDischargeDQDV(
        m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
    out = {}
    out["seed_L_V"] = np.asarray(model.seed_L_V, dtype=float)
    out["equilibrium_298"] = np.asarray(model.equilibrium(V, T=298.15), dtype=float)
    for s, name in [(+1, "dis"), (-1, "chg")]:
        for I in (0.02, 0.2, 1.0):
            out[f"dqdv_{name}_I{I}"] = np.asarray(
                model.dqdv(V, T=298.15, I_abs=I, Q_cell=1.0, s=s), dtype=float)
    for Tk in (258.15, 298.15, 318.15):
        out[f"dqdv_T{int(Tk)}"] = np.asarray(
            model.dqdv(V, T=Tk, I_abs=0.2, Q_cell=1.0, s=+1), dtype=float)
    out["dqdv_TV"] = np.asarray(model.dqdv(V, T=Tprof, I_abs=0.2, Q_cell=1.0, s=+1), dtype=float)
    out["curve_dis_02C"] = np.asarray(
        model.curve(V, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15), dtype=float)
    out["dqdv_scalarV"] = np.asarray([model.dqdv(0.12, T=298.15, I_abs=0.2, Q_cell=1.0, s=+1)])
    # V_n 진입점 발열 경로(하위호환 유지 대상 — ch2_appB B.1)
    out["entropy_V_298"] = np.asarray(model.entropy_coefficient(V, 298.15), dtype=float)
    out["entropy_V_TV"] = np.asarray(model.entropy_coefficient(V, Tprof), dtype=float)
    rt = model.entropy_coefficient(V, 298.15, return_terms=True)
    for k in ("complete", "simple", "config"):
        out[f"entropy_V_terms_{k}"] = np.asarray(rt[k], dtype=float)
    out["revheat_V"] = np.asarray(model.reversible_heat(V, 298.15, I=1.0), dtype=float)
    # x̄ 진입점 3종(ch2_appB B.1)
    out["Uoc_x"] = np.asarray(model.solve_U_oc(xg, 298.15), dtype=float)
    tx = model.entropy_coefficient_x(xg, 298.15, return_terms=True)
    for k in ("U_oc", "complete", "simple", "config"):
        out[f"entropy_x_terms_{k}"] = np.asarray(tx[k], dtype=float)
    out["qrev_x"] = np.asarray(model.reversible_heat_x(xg, 298.15, I=1.0), dtype=float)
    # LCO 서브클래스 경로(seam·전자항 — 흑연 무섭동 확인 대상)
    VL = np.linspace(3.75, 4.15, 800)
    lco = m.LCOCathodeDQDV(m.LCO_MSMR_LIT, Rn=0.005, Cbg=0.0)
    out["lco_eq_298"] = np.asarray(lco.equilibrium(VL, T=298.15), dtype=float)
    out["lco_curve_chg"] = np.asarray(
        lco.curve(VL, direction="charge", c_rate=0.2, Q_cell=1.0, T=298.15), dtype=float)
    out["lco_curve_dis"] = np.asarray(
        lco.curve(VL, direction="discharge", c_rate=0.2, Q_cell=1.0, T=298.15), dtype=float)
    out["lco_entropy"] = np.asarray(lco.entropy_coefficient(VL, 298.15), dtype=float)
    return out


def compare_sets(a, b):
    """두 출력셋 비교 — (전건 bit-exact 여부, 전 키 max|Δ|, 불일치 목록)."""
    assert set(a.keys()) == set(b.keys())
    worst = 0.0
    all_bit = True
    bad = []
    for k in a:
        eq = np.array_equal(a[k], b[k])
        d = float(np.max(np.abs(a[k] - b[k]))) if a[k].shape == b[k].shape else np.inf
        worst = max(worst, d)
        if not eq:
            all_bit = False
            bad.append((k, d))
    return all_bit, worst, bad


def golden_outputs(m):
    """v1.0.19 회귀 하네스(test_regression_v1019.py graphite_outputs)와 동일 13 케이스."""
    V = np.linspace(0.03, 0.34, 1000)
    model = m.GraphiteAnodeDischargeDQDV(
        m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
    out = {"V": V}
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


# ---------------------------------------------------------------- G1
def gate_G1(m19, m20):
    print("=" * 74)
    print("G1: backward-compat  v1.0.20 vs v1.0.19  (new features all unspecified)")
    out19 = output_set(m19)
    out20 = output_set(m20)
    all_bit, worst, bad = compare_sets(out19, out20)
    print(f"  compared arrays: {len(out19)}  bit-exact(np.array_equal): {all_bit}  "
          f"max|diff|: {worst:.3e}")
    for k, d in bad:
        print(f"    MISMATCH {k}: max|diff|={d:.3e}")
    ok_main = (worst <= G1_TOL)
    # 보조: v1.0.19 골든 npz(원 캡처 머신) 대비 — 환경 잡음 확인(회귀 하네스 동일 13 케이스)
    gold = np.load(GOLD)
    gout = golden_outputs(m20)
    worst_g = 0.0
    n_exact = 0
    for k in gold.files:
        d = float(np.max(np.abs(gout[k] - gold[k])))
        worst_g = max(worst_g, d)
        n_exact += int(np.array_equal(gout[k], gold[k]))
    print(f"  [aux] golden npz ({len(gold.files)} arrays, other-machine capture): "
          f"max|diff|={worst_g:.3e}  bit-exact {n_exact}/{len(gold.files)} "
          f"(P0 env-noise ref 4.33e-15)")
    ok = ok_main and (worst_g <= G1_TOL)
    print(f"  G1 RESULT: {'PASS' if ok else 'FAIL'}  "
          f"(module-vs-module {worst:.3e} <= {G1_TOL:.0e}; golden {worst_g:.3e} <= {G1_TOL:.0e})")
    return ok, worst, worst_g, all_bit


# ---------------------------------------------------------------- G2
def _disp(v, fmt):
    return format(v, fmt)


def gate_G2(m):
    print("=" * 74)
    print("G2: regression reference values (ch2_appB B.2, display-precision match)")
    ok = True
    model = m.GraphiteAnodeDischargeDQDV(
        m.GRAPHITE_STAGING_LIT, x=0.5, Rn=0.01, Cbg=0.05, use_dH_eff=True)
    F = m.F

    # --- (a)-(e) worked example, x̄=0.25 · 298.15 K -------------------------
    t = model.entropy_coefficient_x(0.25, 298.15, return_terms=True)
    Uoc = t["U_oc"]; comp = t["complete"]; simp = t["simple"]; conf = t["config"]
    dS = F * comp
    qrev = model.reversible_heat_x(0.25, 298.15, I=1.0)
    rows = [
        ("U_oc [mV]",            Uoc * 1e3,  ".1f",  "74.4"),
        ("dU/dT complete [mV/K]", comp * 1e3, "+.3f", "-0.204"),
        ("dU/dT simple  [mV/K]",  simp * 1e3, "+.3f", "-0.134"),
        ("dU/dT config  [mV/K]",  conf * 1e3, "+.3f", "-0.070"),
        ("dS = F*dU/dT [J/mol/K]", dS,        "+.1f", "-19.7"),
        ("Qrev/I = -T*dU/dT [mV]", qrev * 1e3, "+.1f", "+60.8"),
    ]
    for label, val, fmt, want in rows:
        got = _disp(val, fmt)
        hit = (got == want)
        ok &= hit
        print(f"  {label:26s} value={val:+.6f}  display={got}  doc={want}  {'OK' if hit else 'FAIL'}")

    # round-trip 유한차분 (B.2)
    fd = (model.solve_U_oc(0.25, 298.15 + 3.0) - model.solve_U_oc(0.25, 298.15 - 3.0)) / 6.0
    rt_uVK = abs(fd - comp) * 1e6
    got = _disp(fd * 1e3, "+.3f")
    hit = (got == "-0.204") and (rt_uVK < G2_FD_ANALYTIC_UVK)
    ok &= hit
    print(f"  round-trip [U(T+3)-U(T-3)]/6K = {fd*1e3:+.6f} mV/K (display {got}, doc -0.204); "
          f"|FD-analytic| = {rt_uVK:.3e} uV/K (< {G2_FD_ANALYTIC_UVK}) {'OK' if hit else 'FAIL'}")

    # --- tab:worked 중간값(전이별) -----------------------------------------
    print("  --- tab:worked per-transition intermediates (x=0.25, 298.15 K) ---")
    T0 = 298.15
    xi_doc = ["0.005", "0.072", "0.143", "0.395"]
    g_doc = ["0.19", "2.61", "4.77", "9.30"]
    sh_doc = ["0.003", "0.051", "0.193", "0.753"]
    ds_doc = ["+0.301", "+0.000", "-0.052", "-0.166"]
    cf_doc = ["-0.458", "-0.220", "-0.154", "-0.037"]
    xi_l, g_l, Qg_l, cf_l, ds_l = [], [], [], [], []
    for tr in m.GRAPHITE_STAGING_LIT:
        U_j = m.func_U_j(T0, tr["dH_rxn"], tr["dS_rxn"])
        w = m.func_w(T0, tr["n"])
        xi = float(m.func_ksi_eq(T0, Uoc, U_j, tr["n"]))
        g = xi * (1.0 - xi) / w
        xi_l.append(xi); g_l.append(g); Qg_l.append(tr["Q"] * g)
        ds_l.append(tr["dS_rxn"] / F)
        cf_l.append((tr["n"] * m.R / F) * np.log(xi / (1.0 - xi)))
    den = sum(Qg_l)
    hit_den = (_disp(den, ".2f") == "6.18")
    ok &= hit_den
    print(f"    sum Q_j g_j = {den:.4f} /V (display {den:.2f}, doc 6.18) {'OK' if hit_den else 'FAIL'}")
    for j in range(4):
        got = (_disp(xi_l[j], ".3f"), _disp(g_l[j], ".2f"), _disp(Qg_l[j] / den, ".3f"),
               _disp(ds_l[j] * 1e3, "+.3f"), _disp(cf_l[j] * 1e3, "+.3f"))
        want = (xi_doc[j], g_doc[j], sh_doc[j], ds_doc[j], cf_doc[j])
        hit = (got == want)
        ok &= hit
        print(f"    j={j}: xi={got[0]}({want[0]}) g={got[1]}({want[1]}) share={got[2]}({want[2]}) "
              f"dS/F={got[3]}({want[3]}) config={got[4]}({want[4]}) {'OK' if hit else 'FAIL'}")

    # --- tab:qrev 5점(전 열: U_oc·dU/dT·dS·Qrev/I) --------------------------
    print("  --- tab:qrev 5-point (298.15 K, full columns) ---")
    tabq = {0.10: ("43.5", "-0.307", "-29.6", "+91.5"),
            0.25: ("74.4", "-0.204", "-19.7", "+60.8"),
            0.50: ("109.0", "-0.089", "-8.6", "+26.6"),
            0.75: ("148.8", "+0.044", "+4.3", "-13.2"),
            0.90: ("195.2", "+0.218", "+21.0", "-64.9")}
    for xb, (u_w, d_w, s_w, q_w) in tabq.items():
        tt = model.entropy_coefficient_x(xb, 298.15, return_terms=True)
        q = model.reversible_heat_x(xb, 298.15, I=1.0)
        got = (_disp(tt["U_oc"] * 1e3, ".1f"), _disp(tt["complete"] * 1e3, "+.3f"),
               _disp(F * tt["complete"], "+.1f"), _disp(q * 1e3, "+.1f"))
        hit = (got == (u_w, d_w, s_w, q_w))
        ok &= hit
        print(f"    x={xb:.2f}: U_oc={got[0]}({u_w})  dU/dT={got[1]}({d_w})  "
              f"dS={got[2]}({s_w})  Qrev/I={got[3]}({q_w})  {'OK' if hit else 'FAIL'}")

    # --- 파생 A: 175점 전 범위 완전식 vs 유한차분 + 내부 경계 3곳 연속 -------
    print("  --- derived A: 175-pt full-range complete vs FD + 3-boundary continuity ---")
    T1, T2 = 292.15, 298.15
    Tm = 0.5 * (T1 + T2)                     # 295.15 K — 원 검증 규약(해석식 평가 온도)
    xg = np.linspace(0.05, 0.95, 175)
    U1 = model.solve_U_oc(xg, T1)
    U2 = model.solve_U_oc(xg, T2)
    fd = (U2 - U1) / (T2 - T1)
    tm = model.entropy_coefficient_x(xg, Tm, return_terms=True)
    err_c = np.abs(fd - tm["complete"]) * 1e3    # mV/K
    err_s = np.abs(fd - tm["simple"]) * 1e3
    cfg = tm["config"] * 1e3
    hit = bool(np.max(err_c) <= G2_DERIVA_MVK)
    ok &= hit
    print(f"    complete vs FD: max={np.max(err_c):.3e} mV/K  mean={np.mean(err_c):.3e} "
          f"(gate <= {G2_DERIVA_MVK} mV/K, display precision) {'OK' if hit else 'FAIL'}")
    print(f"    [ref] simple vs FD: max={np.max(err_s):.4f} mV/K (doc grid-max ~0.18; span-dep)")
    print(f"    [ref] config span: [{np.min(cfg):+.3f}, {np.max(cfg):+.3f}] mV/K "
          f"(doc ~[-0.21,+0.14]; span-dep)")
    # 내부 경계 3곳: 인접 봉우리 중심의 x̄ 중점에서 (i) 인접 ΔS⁰/F 사이 값(블렌드),
    # (ii) 국소 계단 부재(격자 스텝당 변화 < G2_STEP_UVK)
    peaks = []
    for tr in m.GRAPHITE_STAGING_LIT:
        U_j = m.func_U_j(Tm, tr["dH_rxn"], tr["dS_rxn"])
        xpk = sum(t2["Q"] * float(m.func_ksi_eq(Tm, U_j, m.func_U_j(Tm, t2["dH_rxn"], t2["dS_rxn"]), t2["n"]))
                  for t2 in m.GRAPHITE_STAGING_LIT) / sum(t2["Q"] for t2 in m.GRAPHITE_STAGING_LIT)
        peaks.append((xpk, tr["dS_rxn"] / F * 1e3))     # (x̄_peak, plateau [mV/K])
    peaks.sort()
    dstep = np.abs(np.diff(tm["complete"])) * 1e6       # µV/K per grid step
    for i in range(3):
        (xa, da), (xb_, db) = peaks[i], peaks[i + 1]
        xmid = 0.5 * (xa + xb_)
        vmid = float(model.entropy_coefficient_x(xmid, Tm)) * 1e3
        lo, hi = min(da, db), max(da, db)
        blend = (lo < vmid < hi)
        k = int(np.argmin(np.abs(xg - xmid)))
        near = dstep[max(0, k - 5):k + 5]
        nostep = bool(np.max(near) < G2_STEP_UVK)
        hit = blend and nostep
        ok &= hit
        print(f"    boundary {i+1}: x_mid={xmid:.3f}  dU/dT={vmid:+.4f} mV/K in "
              f"({lo:+.3f},{hi:+.3f})? {blend}  local max step={np.max(near):.1f} uV/K "
              f"(< {G2_STEP_UVK}) {'OK' if hit else 'FAIL'}")
    print(f"    [ref] global max per-step change: {np.max(dstep):.1f} uV/K "
          f"(175-pt grid; original 181-pt verification: max 13 uV/K/step)")
    print(f"  G2 RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------- G3
_VIB_PATCHES = [  # '보정 도입 이전' 소스 변형(발생 횟수 고정 — 어긋나면 즉시 FAIL)
    (" + self._vib_dU(tr, T)", "", 3),        # equilibrium·entropy_coefficient·solve_U_oc
    (" + self._vib_dU(tr, T_prog)", "", 1),   # dqdv
    ("dS0 + self._vib_dS(tr, T)", "dS0", 1),  # entropy_coefficient
]


def gate_G3(m20):
    print("=" * 74)
    print("G3: theta_E bit-exact  (unspecified path == pre-correction code)")
    ok = True
    src = open(CODE_V20, encoding="utf-8").read()
    for pat, rep, n_want in _VIB_PATCHES:
        n = src.count(pat)
        if n != n_want:
            print(f"  FAIL: patch pattern {pat!r} count {n} != {n_want} (source drift)")
            return False
        src = src.replace(pat, rep)
    tmpdir = os.environ.get("ANODEFIT_TMP") or tempfile.mkdtemp(prefix="anodefit_g3_")
    os.makedirs(tmpdir, exist_ok=True)
    vpath = os.path.join(tmpdir, "Anode_Fit_v1020_previb_variant.py")
    with open(vpath, "w", encoding="utf-8") as f:
        f.write(src)
    m_pre = load(vpath, "anodefit_previb")
    out20 = output_set(m20)
    outpre = output_set(m_pre)
    all_bit, worst, bad = compare_sets(out20, outpre)
    ok &= all_bit
    print(f"  v1.0.20(no theta_E) vs pre-correction variant: arrays={len(out20)}  "
          f"bit-exact={all_bit}  max|diff|={worst:.3e}  {'OK' if all_bit else 'FAIL'}")
    for k, d in bad:
        print(f"    MISMATCH {k}: max|diff|={d:.3e}")

    # 발효 확인: theta_E=700 K 부여 — T_ref(298.15) 불변·T=318.15 변화 + C-62 수치
    trs = [dict(t) for t in m20.GRAPHITE_STAGING_LIT]
    trs[3]["theta_E"] = 700.0
    V = np.linspace(0.03, 0.34, 1000)
    mth = m20.GraphiteAnodeDischargeDQDV(trs, x=0.5, Rn=0.01, Cbg=0.05)
    mno = m20.GraphiteAnodeDischargeDQDV(
        [dict(t) for t in m20.GRAPHITE_STAGING_LIT], x=0.5, Rn=0.01, Cbg=0.05)
    same_ref = np.array_equal(mth.equilibrium(V, 298.15), mno.equilibrium(V, 298.15))
    d318 = float(np.max(np.abs(mth.equilibrium(V, 318.15) - mno.equilibrium(V, 318.15))))
    eff = same_ref and (d318 > 0.0)
    ok &= eff
    print(f"  effectiveness: theta_E=700K on tr[3] -> T_ref outputs equal: {same_ref}; "
          f"T=318.15K max|diff|={d318:.3e} (>0) {'OK' if eff else 'FAIL'}")
    # C-62: dDeltaU_vib/dT = DeltaS_vib(T)/F @ 278.15/298.15/318.15/348.15 (doc -3.74/0/+3.70/+9.14 uV/K)
    c62_doc = {278.15: "-3.74", 298.15: "+0.00", 318.15: "+3.70", 348.15: "+9.14"}
    for Tk, want in c62_doc.items():
        v = float(mth._vib_dS(trs[3], Tk)) / m20.F * 1e6   # uV/K
        got = _disp(v, "+.2f")
        hit = (got == want) or (want == "+0.00" and got in ("+0.00", "-0.00"))
        ok &= hit
        print(f"    C-62 dDU_vib/dT @T={Tk}: {v:+.4f} uV/K (display {got}, doc {want}) "
              f"{'OK' if hit else 'FAIL'}")
    print(f"  G3 RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------- 부록: n(T) 전파 증빙
def check_nT(m):
    print("=" * 74)
    print("APPENDIX: n(T)=n+n_T1*(T-T_ref) propagation evidence (ch1_appB)")
    ok = True
    V = np.linspace(0.03, 0.34, 1000)
    base = [dict(t) for t in m.GRAPHITE_STAGING_LIT]
    with0 = [dict(t, n_T1=0.0) for t in m.GRAPHITE_STAGING_LIT]
    mb = m.GraphiteAnodeDischargeDQDV(base, x=0.5, Rn=0.01, Cbg=0.05)
    m0 = m.GraphiteAnodeDischargeDQDV(with0, x=0.5, Rn=0.01, Cbg=0.05)
    pairs = [
        ("equilibrium_298", mb.equilibrium(V, 298.15), m0.equilibrium(V, 298.15)),
        ("dqdv_dis_0.2", mb.dqdv(V, 298.15, 0.2, 1.0, +1), m0.dqdv(V, 298.15, 0.2, 1.0, +1)),
        ("entropy_V", mb.entropy_coefficient(V, 298.15), m0.entropy_coefficient(V, 298.15)),
        ("Uoc_x", mb.solve_U_oc(np.linspace(0.05, 0.95, 31), 298.15),
                  m0.solve_U_oc(np.linspace(0.05, 0.95, 31), 298.15)),
    ]
    for k, a, b in pairs:
        eq = np.array_equal(np.asarray(a), np.asarray(b))
        ok &= eq
        print(f"  n_T1=0.0 == absent (value bit-exact) {k}: {eq}")
    # 발효: n_T1=5e-4 — ∂w/∂T 해석 vs 중심차분(2차식이라 이론상 정확 일치)
    tr = dict(m.GRAPHITE_STAGING_LIT[3], n_T1=5e-4)
    mx = m.GraphiteAnodeDischargeDQDV([tr], x=0.5, Rn=0.0, Cbg=0.0)
    T0, dT = 298.15, 0.5
    dw_an = float(mx._dwdT(tr, T0))
    dw_fd = float((mx._width(tr, T0 + dT) - mx._width(tr, T0 - dT)) / (2 * dT))
    rel = abs(dw_an - dw_fd) / abs(dw_an)
    hit = rel < 1e-9
    ok &= hit
    print(f"  n_T1=5e-4: dw/dT analytic={dw_an:.9e} V/K  centered-FD={dw_fd:.9e}  "
          f"rel-diff={rel:.2e} (<1e-9) {'OK' if hit else 'FAIL'}")
    # 발효: round-trip 정합 — config 계수 (R/F)(n(T)+T·n_T1) 가 솔버·완전식에 동반 전파
    trs = [dict(t, n_T1=5e-4) for t in m.GRAPHITE_STAGING_LIT]
    mr = m.GraphiteAnodeDischargeDQDV(trs, x=0.5, Rn=0.01, Cbg=0.05)
    fd = (mr.solve_U_oc(0.25, T0 + 3.0) - mr.solve_U_oc(0.25, T0 - 3.0)) / 6.0
    an = mr.entropy_coefficient_x(0.25, T0)
    d_uVK = abs(fd - an) * 1e6
    hit = d_uVK < 1e-2
    ok &= hit
    print(f"  n_T1=5e-4 round-trip @x=0.25: FD={fd*1e3:+.6f} analytic={an*1e3:+.6f} mV/K  "
          f"|diff|={d_uVK:.3e} uV/K (<1e-2) {'OK' if hit else 'FAIL'}")
    print(f"  n(T) RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


def main():
    m19 = load(CODE_V19, "anodefit_v1019")
    m20 = load(CODE_V20, "anodefit_v1020")
    print(f"v1.0.19: {CODE_V19}\nv1.0.20: {CODE_V20}\nnumpy {np.__version__}, python {sys.version.split()[0]}")
    g1, w_mod, w_gold, bit = gate_G1(m19, m20)
    g2 = gate_G2(m20)
    g3 = gate_G3(m20)
    nt = check_nT(m20)
    print("=" * 74)
    print(f">>> SUMMARY: G1 {'PASS' if g1 else 'FAIL'} (module max|d|={w_mod:.1e}, "
          f"golden max|d|={w_gold:.1e}, bit-exact={bit}) | G2 {'PASS' if g2 else 'FAIL'} | "
          f"G3 {'PASS' if g3 else 'FAIL'} | n(T) {'PASS' if nt else 'FAIL'}")
    sys.exit(0 if (g1 and g2 and g3 and nt) else 1)


if __name__ == "__main__":
    main()
